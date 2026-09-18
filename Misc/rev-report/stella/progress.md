# 星塔旅人 (StellaSora) 1.9.0 逆向进展报告

> 目标：找出资源/更新包的链接 URL 与获取方式
> 平台：iOS (decrypted IPA, IL2CPP, ARM64)
> 主二进制：`Frameworks/UnityFramework.framework/UnityFramework` (IDA 已加载)

---

## 1. 组织结构（已确认）

```
客户端内置 ClientConfig (data.unity3d 内 MonoBehaviour)
  ├─ 开发/回退资源地址   http://127.0.0.1:5123/res
  ├─ 生产资源基础地址    https://nova-static.yostar.cn
  ├─ 渠道 Official / 版本 1.9.0 / 语言 zh_CN,ja_JP
  ├─ 4 个密钥材料 (2×16B, 2×32B)
  └─ bootstrap/serverlist 地址 (来自 SDKConfigSettings.json)
          │
          ▼
远端环境/服务器配置 (serverlist.html, AES 加密, 已解密)
          │
          ▼
远端资源 manifest + bundle manifest
          │
          ▼
与 install_resource_manifest.mani 做差分
          │
          ▼
按资源分组下载、校验(MD5+CRC32)、缓存、清理旧文件
```

---

## 2. 内置资源清单 install_resource_manifest.mani

路径：`Data/Raw/InstallResource/install_resource_manifest.mani`

头部字段：
```
RES_VER
CLIENT_VER
CLIENT_VER_COMP_MODE
GAME_VER
CLEAR_EXPIRED_FILES
```

每文件记录格式：
```
文件名 | 压缩文件 MD5 | 压缩文件长度 | 解压数据 CRC32
```

已用 `global.unity3d`、`res_meta.unity3d` 验证：
- 第 2 列 = 磁盘文件 MD5
- 第 3 列 = 磁盘文件长度
- 第 4 列 = UnityFS 全部数据块解压后 CRC32

两层完整性检查，但 MD5/CRC 都不是防未授权访问的安全机制。

---

## 3. ClientConfig 字段布局（data.unity3d MonoBehaviour）

从 `Data/data.unity3d` (UnityFS, LZ4) 解出，字段顺序：

| 偏移 | 值 | 含义 |
|------|-----|------|
| - | `2026_0408_1156` | 构建版本 |
| - | `Rel-CN` | 发行环境 |
| - | `http://127.0.0.1:5123/res` | 开发/回退资源地址 |
| - | `bak-` | 版本前缀 |
| - | `1.9.0` ×3 | 客户端/资源/游戏版本 |
| - | `zh_CN` ×4 / `ja_JP` | 默认语言/语音语言 |
| - | `https://nova-static.yostar.cn` | 生产资源基础地址 |
| - | `Official` | 渠道 |
| - | `Xf&FRcsYm48cJ2A@` | 密钥材料 1 (16B) |
| - | `H*No^A$pLvT46oHP` | 密钥材料 2 (16B) |
| - | `QW*Wi7fKjLk!T82Qf2nEGZA%nSC!D9qV` | 密钥材料 3 (32B) |
| - | `48!gdVvUHYKtE%A*n&3^&A84yP6mhYA%` | 密钥材料 4 (32B) |

---

## 4. SDKConfigSettings.json（明文 bootstrap）

- serverlist 入口：`https://nova-static.yostar.cn/meta/serverlist.html`
- 环境入口：`https://nova.yostar.cn`
- SDK API：`https://sdk-api.yostar.cn`
- 客服：`https://customer.yostar.net`
- 阿里云日志：`https://cn-shanghai.log.aliyuncs.com` (project: yostar-cn-client-logging)

---

## 5. serverlist 解密（已完成）

### 加密方案
- **算法**：AES-128-CBC + PKCS7
- **密钥**：`Xf&FRcsYm48cJ2A@`（ClientConfig 密钥材料 1）
- **格式**：`[16B IV][密文]`，IV 前置
- **验证**：PKCS7 填充字节=6 合法 + 明文为合法 protobuf → 双重确认

原始 608B → 解密 586B protobuf。

### 解出的 URL

主环境 (field2, 名"星塔旅人")：
- 游戏服务入口：`https://nova.yostar.cn/agent-zone-1/`
- 上报地址：`https://nova.yostar.cn/report/`

渠道/分发条目 (field7 数组：渠道|版本|URL)：

| 渠道 | 版本 | URL |
|------|------|-----|
| Bilibili | 1.9.0 | https://www.biligame.com/detail/?id=111603&... |
| ALL(iOS) | 1.9.0 | https://apps.apple.com/cn/app/星塔旅人/id6738384520 |
| ALL | 1.9.0 | https://stellasora.yostar.cn/news/1981 |
| Official | 1.9.0 | https://nova-pkg.yostar.cn/pubplat/gpp/sdkpackage/prod/game_apk_v2/Official/3f056a0a4b954b5fa62fb2ecc7fed2b4/StellaSora.apk |
| ALL | 1.13.0 | https://nova-static-pre.yostar.cn/review |

### 新暴露的域名
- `nova.yostar.cn/agent-zone-1/` — 真正游戏网关/登录入口
- `nova-pkg.yostar.cn` — 安装包 CDN
- `stellasora.yostar.cn` — 新闻/公告
- `nova-static-pre.yostar.cn` — 审核/预发环境

---

## 6. IL2CPP metadata 包装（见 re-stellasora.txt）

`Data/Managed/Metadata/global-metadata.dat` 被自定义包装：
```
0x000  uint32 magic = 0x1357FEDA
0x004  uint32 payloadSize (28,543,988)
0x008  256B 变换参数
0x108   64B 调度数据
0x148  变换后 payload ("CODEPHIL" 校验标记)
0x150  真正的 Il2CppGlobalMetadataHeader
```
解包函数 `0x17192C8`，变换函数 `0x14E30CC`（表驱动混淆，276 基本块）。
初始化链：`_il2cpp_init(0x16B0480)` → `MetadataCache::Initialize(0x174D66C)` → `GlobalMetadata::Init(0x149F638)`。

---

## 7. 待办 / 下一步

- [x] **更新包如何获取/下载** → 见 `report/metadata_and_download.md`
- [x] 定位 UnityFramework 中的资源 manifest 差分 + 下载逻辑（DownloadStore 全套已还原）
- [x] 确认 bundle 完整 URL 拼接规则：`baseURL + "/" + bundleFileName`（remote URL map 可重定向）
- [x] 解包 global-metadata：**纯静态**用 Unicorn 模拟 sub_14E30CC 完成，无需动态调试

详细成果见：**`report/metadata_and_download.md`**

---

## 工具/脚本位置
- 临时 Python 脚本：`./tmp/REVERSE/`
- 本报告：`./report/`
- metadata 解包 + 下载机制报告：`./report/metadata_and_download.md`
- 解包产物：`./tmp/REVERSE/global-metadata-decoded.dat`、`./tmp/REVERSE/dumper_out/`
