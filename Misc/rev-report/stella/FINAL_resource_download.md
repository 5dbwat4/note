# 星塔旅人 (StellaSora) 资源下载机制 —— 完整逆向文档

> 平台：iOS（解密 IPA，Unity 2022.3.62f2，IL2CPP，ARM64）
> 主二进制：`Frameworks/UnityFramework.framework/UnityFramework`
> 状态：**已完整逆向并实链验证（HTTP 200 + MD5 匹配）**
> 本文档为最终权威版，取代早期报告中关于字段含义的推测。

---

## 0. TL;DR —— 一句话结论

**任意资源包的真实下载地址（无需登录）：**
```
https://nova-static.yostar.cn/res/ios/{Version}/{AdditionalPath}/{FileName}
```
其中 `{Version}`、`{AdditionalPath}`、`{FileName}` 来自资源清单
`https://nova-static.yostar.cn/meta/ios.html`（AES-128-CBC 加密，密钥
`Xf&FRcsYm48cJ2A@`）。已用 `env_infinitytower_mesh-3.unity3d` 等多个不同
分桶验证：返回 200，下载内容 MD5 与清单 Hash 字段完全一致。

---

## 1. 整体链路（全程无需登录）

```
内置 ClientConfig (data.unity3d MonoBehaviour, 明文)
  ├─ ServerRootURL 来源: VendorEnvData.serverURL = https://nova-static.yostar.cn
  ├─ serverMetaKey = "Xf&FRcsYm48cJ2A@"   (AES 密钥, 解所有 meta)
  └─ 回退地址 http://127.0.0.1:5123/res
        │
        ▼
DownloadRootURL = RuntimeClientConfig.ReplaceDownloadServerUrl
                  ?? ServerRootURL           (线上无 client_config*.ini → = ServerRootURL)
        │  + "/res/ios/"
        ▼
bundle 基址 = https://nova-static.yostar.cn/res/ios/
        │
        ▼
下载资源清单 GET https://nova-static.yostar.cn/meta/ios.html
   → AES-128-CBC 解密 (key=serverMetaKey, IV 前置, PKCS7)
   → protobuf: ClientDiff { repeated FileDiff diff = 1 }   (19,493 条)
        │
        ▼
HttpNetworkManager.ParseManifest (0x2C16828) 遍历 FileDiff, 填充 remote URL map
   模板 "{ver}/{name}", 占位符替换 (DownloadStore.GetBundleDownloadUrl 0x295CC84)
        │
        ▼
每个 bundle URL = base + {ver} + "/" + {AdditionalPath} + "/" + {name}
        │
        ▼
下载 → MD5 校验(=清单 Hash) → 解压 CRC32 → 缓存 → 清理过期
```

**为何不需要登录**：ServerRootURL、密钥、清单 URL 全部硬编码在客户端；
清单和 bundle 均托管在公开 CDN `nova-static.yostar.cn`（AliyunOSS + EdgeOne）。
登录只影响游戏网关 `nova.yostar.cn/agent-zone-1/`（业务数据），与资源下载无关。

---

## 2. 资源清单格式（重点·已更正）

### 2.1 protobuf schema（来自解包 metadata 的 C# 类型）
```
message ClientDiff  { repeated FileDiff diff = 1; }
message FileDiff {
    string FileName       = 1;   // 文件名
    string Hash           = 2;   // MD5 (== 磁盘文件 MD5)
    int64  Version        = 3;   // 版本号(整数) —— URL 的 {ver}
    string AdditionalPath = 4;   // 附加路径(32-hex 分桶) —— name 前缀
}
```

### 2.2 ⚠️ 字段含义更正（早期文档的错误）
早期把 field3 误当 size、field4 误当 verHash。**正确对应：**

| protobuf 字段 | 类型 | 正确含义 | URL 占位符 | 样例 |
|---|---|---|---|---|
| field1 | string | **FileName** | `{name}` | `env_infinitytower_mesh-3.unity3d` |
| field2 | string | **Hash (MD5)** | `{hash}` | `b8548eb5efb2105740bd970bd5585a81` |
| field3 | int64 | **Version** | **`{ver}`** | `100` |
| field4 | string | **AdditionalPath** | 前缀 | `d936168e3d59a7947e419581c538542e` |

- `{ver}` 是**整数版本号**（4、48、100、108…共几十种），不是 hash。
- `{AdditionalPath}` 是 32-hex 分桶目录（33 个），插在 `{name}` 之前。

### 2.3 URL 组装的确切代码依据
- `HttpNetworkManager.ParseManifest` (0x2C16828)：
  `v3 = ClientConfig.ServerMetaKey()` 解密；遍历 FileDiff 填 map entry：
  `entry[2]=FileName, entry[3]=Hash, entry[4]=Version, entry[5]=AdditionalPath`
- `DownloadStore.GetBundleDownloadUrl` (0x295CC84) → `sub_2967860` 模板替换：
  ```
  name2 = AdditionalPath ? (AdditionalPath + "/" + name) : name
  url   = template.Replace("{name}", name2)
                  .Replace("{hash}", Hash)
                  .Replace("{ver}",  Version)
  finalUrl = baseUrl + url          // baseUrl = ".../res/ios/", template = "{ver}/{name}"
  ```
- 展开即：`base/res/ios/{Version}/{AdditionalPath}/{FileName}`

---

## 3. 实链验证结果

| 测试 URL | 结果 |
|---|---|
| `…/res/ios/100/d936168e…/env_infinitytower_mesh-3.unity3d` | **200**, 33072B, MD5=`b8548eb5…` ✅ 与清单一致 |
| `…/res/ios/4/30f9f3aa…/vo_113_ui_xmas_001_cn.wem` | 206 ✅ |
| `…/res/ios/108/c9d346a5…/p_6_u.mons_72001shuangziqi_red_textures.unity3d` | 206 ✅ (patch 包) |

3 种不同分桶（.unity3d / .wem / patch）全部命中，方案跨桶成立。

---

## 4. 已确认可公开获取的 meta 端点

| 端点 | 内容 | 加密 |
|---|---|---|
| `https://nova-static.yostar.cn/meta/ios.html` | iOS 资源清单 (19,493 FileDiff) | AES-128-CBC, key `Xf&FRcsYm48cJ2A@` |
| `https://nova-static.yostar.cn/meta/serverlist.html` | 服务器列表 (agent/rules) | 同上 |
| `https://nova-static.yostar.cn/notice/noticelist.html` | 公告列表 | 同上 |
| `https://nova.yostar.cn/agent-zone-1/` | 游戏网关(登录/业务) | — |

**加密方案**（所有 meta 通用）：AES-128-CBC + PKCS7，密钥 = ClientConfig.serverMetaKey
= `Xf&FRcsYm48cJ2A@`，IV = 密文前 16 字节。

---

## 5. metadata 静态解包（前置工作，已完成）

`global-metadata.dat` 被自定义包装（magic `0x1357FEDA`），需先还原才能拿到 C# 符号：
- 解包函数 `0x17192C8`，变换函数 `0x14E30CC`（256 路线程化字节码解释器）
- 用 **Unicorn 忠实模拟** `0x14E30CC` 离线还原 → magic 恢复 `0xFAB11BAF`, version 31
- Il2CppDumper 输出全部类名/方法地址（CodeReg `0xA024E30`, MetaReg `0xA366A38`）
- 详见 `metadata_and_download.md`

---

## 6. 关键函数地址速查（IDA VA）

| 函数 | 地址 | 作用 |
|---|---|---|
| GlobalMetadata 解包 | 0x17192C8 | 校验 magic, 分块调用变换 |
| 变换解释器 | 0x14E30CC | 256-opcode 字节码 VM |
| ClientConfig.get_ServerRootURL | 0x2BB77AC | = VendorEnvData.serverURL |
| ClientConfig.get_DownloadRootURL | 0x2BB7B60 | Replace ?? ServerRootURL |
| ClientConfig.get_ServerMetaKey | 0x2BB7D74 | AES 密钥 |
| HttpNetworkManager.ParseManifest | 0x2C16828 | 解密+解析清单→URL map |
| DownloadStore.GetBundleDownloadUrl | 0x295CC84 | 拼接 bundle URL |
| sub_2967860 | 0x2967860 | 模板 {ver}/{hash}/{name} 替换 |
| GetPlatformName | 0x296747C | 返回 "ios" |
| Booter.UpdateResource MoveNext | 0x2BAEC90 | 更新流程主状态机 |

---

## 7. 产物与脚本（`tmp/REVERSE/`）

**解包/解密：**
- `emulate.py` — Unicorn 模拟解包 metadata
- `global-metadata-decoded.dat` — 还原后的明文 metadata
- `dumper_out/` — Il2CppDumper 完整输出 (dump.cs / script.json / stringliteral.json)
- `decrypt_all_meta.py` — 批量解密 meta 文件

**meta 明文与解析：**
- `meta_dump/ios.dec.bin` `ios_manifest.json` `ios_manifest.csv` — 资源清单
- `meta_dump/serverlist.json` `noticelist.json` — 服务器列表/公告

**下载链接（本次生成，见第 8 节）：**
- `gen_download_links.py` — 链接生成器
- `download_links/` — 4 种格式输出

---

## 8. 下载链接文件（已生成，未下载）

基于已验证规则，为全部 **19,493** 个资源生成链接，位于
`tmp/REVERSE/download_links/`：

| 文件 | 说明 |
|---|---|
| `urls.txt` | 纯 URL 列表，一行一个 |
| `download_index.csv` | `url,name,hash,version,additionalPath` |
| `download_index.json` | 结构化，含 base/scheme/records |
| `aria2_input.txt` | aria2c 输入格式（含 `out=` 文件名 + `checksum=md5=`）|

**下载命令（如需）：**
```
aria2c -i aria2_input.txt -j 16 -d ./download_out --auto-file-renaming=false
```
aria2 会自动按 `checksum=md5=` 校验每个文件。

**统计**：19,493 条 = 8,460 .unity3d + 10,372 .wem 音频 + 2,814 patch(p_*)；
版本号分桶数十种，AdditionalPath 分桶 33 个。

---

## 9. 资源扩展名分布（全 19,493 文件）

| 扩展名 | 数量 | 占比 | 说明 |
|---|---:|---:|---|
| `.wem` | 10,372 | 53.21% | Wwise 音频（语音/音效）|
| `.unity3d` | 8,460 | 43.40% | Unity AssetBundle（美术/场景/配置）|
| `.bnk` | 556 | 2.85% | Wwise SoundBank |
| `.mp4` | 27 | 0.14% | 视频（抽卡/开场）|
| `.arcx` | 25 | 0.13% | 打包数据档（`data.arcx`）|
| `.mani` | 24 | 0.12% | 子清单（`ss_ios.mani` 等）|
| `.arch` | 22 | 0.11% | HybridCLR 热更 DLL 档（`hotfix.arch`）|
| `.srt` | 4 | 0.02% | 字幕（过场 CG）|
| `.json` | 2 | 0.01% | 数据配置（`data.json`）|
| `.config` | 1 | 0.01% | `LaunchVideo.config` |
| **合计** | **19,493** | 100% | |

其中 **patch 增量包（`p_*` 前缀）共 2,814 个**，分布：
| 扩展名 | 正式包 | patch 包 |
|---|---:|---:|
| `.unity3d` | 6,811 | 1,649 |
| `.wem` | 9,522 | 850 |
| `.bnk` | 308 | 248 |
| `.mani` | 3 | 21 |
| `.arcx` | 2 | 23 |
| `.arch` | 1 | 21 |
| `.mp4` | 25 | 2 |
| `.srt`/`.json`/`.config` | 10 | 0 |

**观察**：音频资源（wem+bnk = 56%）占比最大；其次是 AssetBundle（43%）。
热更逻辑代码走 `.arch`（HybridCLR），数据走 `.arcx`/`.json`，视频/字幕单列。
