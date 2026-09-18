# 真实下载链接获取 —— 静态逆向成果

> ⚠️ **已过时/部分字段判断有误**：本文早期把清单 field3 当作 size、field4 当作 verHash，
> 均为错误。正确对应见 **`FINAL_resource_download.md`**（field3=Version 整数、field4=AdditionalPath），
> 且最终 URL 结构为 `base/res/ios/{Version}/{AdditionalPath}/{FileName}`，已实链验证。
> 本文保留作为过程记录。

> 承接 metadata_and_download.md。本文记录**基于逆向规则精确重建 URL**并成功
> 获取/解密**真实线上资源清单**的过程（非爆破，全部由反编译逻辑推导）。

---

## 一、URL 组装的完整逆向（Booter.UpdateResource）

反编译 `Booter.UpdateResource` 协程 MoveNext (`0x2BAEC90`) 得到确切流程：

### Step A —— 下载资源清单 (case 0)
```c
v266 = ClientConfig.ServerRootURL();           // sub_2BB77AC
v267 = Concat(v266, "/meta/ios.html");         // qword_A85F288
Booter.DownloadRemoteResourceManifest(v267, ...);  // sub_2BA6EA0
```
→ **清单 URL = `ServerRootURL + "/meta/ios.html"`**

### Step B —— 组装 bundle 基址 (case 1)
```c
v173 = ClientConfig.DownloadRootURL();         // sub_2BB7B60
v174 = Concat(v173, "/res/ios/");              // qword_A85F2C8
baseURL = v174;                                // 存入状态机
urlMap.baseUrl   = baseURL;                    // off_A7F7010 字段
urlMap.template  = "{ver}/{name}";             // qword_A89B008
```
→ **bundle 基址 = `DownloadRootURL + "/res/ios/"`**

### Step C —— 下载 bundle (DownloadResourceBundle MoveNext 0x2963A04)
```c
v62 = bundleInfo.bundleFileName;
v63 = baseURL;
v64 = DownloadStore.GetBundleDownloadUrl(v63, v62, activeRemoteUrlMap);  // 0x295CC84
```

`GetBundleDownloadUrl` 两条路径：
- **remote URL map 命中** → 套模板 `{ver}/{name}`，`{ver}`←map项版本，`{name}`←文件名(可带`hash/`前缀)
- **未命中(默认)** → `baseURL + "/" + bundleFileName`

### ServerRootURL vs DownloadRootURL
- `ServerRootURL` (`0x2BB77AC`) = `CurrentVendorEnvData.serverURL`
  = **`https://nova-static.yostar.cn`**（backup 模式加 `bak-` 前缀）
- `DownloadRootURL` (`0x2BB7B60`) = `RuntimeClientConfig.ReplaceDownloadServerUrl`
  若为空则 fallback 到 `ServerRootURL`。**这个 replace 值由游戏网关登录后动态下发**。

---

## 二、真实资源清单：成功获取并解密 ✅

### 2.1 精确构造清单 URL 并下载
```
GET https://nova-static.yostar.cn/meta/ios.html
→ HTTP 200, 2,024,016 字节 (AliyunOSS + EdgeOne CDN)
→ 16 字节对齐的密文
```

### 2.2 用逆向出的密钥成功解密
- 算法：**AES-128-CBC + PKCS7**，IV 前置（与 serverlist 同一套）
- 密钥：**`Xf&FRcsYm48cJ2A@`**（ClientConfig 的 serverMetaKey / 密钥材料1）
- 解密后：合法 protobuf，`tmp/REVERSE/ios_meta_dec.bin`

### 2.3 清单内容（protobuf: repeated BundleInfo）
每条 = `{ field1:bundleFileName, field2:bundleHash(md5,32hex), field3:size, field4:verHash(32hex) }`

**统计（导出至 `tmp/REVERSE/ios_manifest.csv`）：**
| 指标 | 值 |
|------|-----|
| 总条目 | **19,493** |
| .unity3d bundle | 8,460 |
| .wem 音频 | 10,372 |
| patch 补丁(p_*) | 2,814 |
| 版本分桶(verHash) | 33 |

**样例条目：**
```
env_infinitytower_mesh-3.unity3d | b8548eb5efb2105740bd970bd5585a81 | 100 | d936168e3d59a7947e419581c538542e
breakout_2_8.unity3d             | a03e8eb8b5e08b734fa3b6a4c6cb12f4 | 100 | d936168e3d59a7947e419581c538542e
p_6_u.mons_72001shuangziqi_red_textures.unity3d | 5302fdf6...| 108 | c9d346a5fa3a7bb22e19cf05956e9f2b
```

这份清单是**当前线上版本(1.9.0之后)的真实资源列表**（Last-Modified 2026-07-07），
证明我们的 URL 规则 + 密钥推导完全正确。

---

## 三、bundle 本体 URL 的结论

- **清单(meta/ios.html)** 托管在 `nova-static.yostar.cn`(AliyunOSS)，已可公开下载解密。
- **bundle 本体基址 = `DownloadRootURL + /res/ios/`**，其中 `DownloadRootURL` 的
  实际 host 由**游戏网关 `nova.yostar.cn/agent-zone-1/` 登录后下发**
  （`RuntimeClientConfig.ReplaceDownloadServerUrl`），并可经 remote URL map 重定向。
- 因此 bundle 直链形如：
  ```
  <下发的CDN>/res/ios/<name>              (默认)
  <下发的CDN>/res/ios/<verHash>/<name>    (启用 remote URL map 模板 {ver}/{name})
  ```
  实测 `nova-static.yostar.cn` 上的 `/res/ios/...` 返回 404，确认 bundle CDN
  与清单 host 不同源，需登录态才能拿到真实下载 host（无凭证不继续，避免盲目探测）。

---

## 四、已确认可直接获取的真实链接

| 用途 | URL | 状态 |
|------|-----|------|
| iOS 资源清单 | `https://nova-static.yostar.cn/meta/ios.html` | ✅ 200 可下载，AES 可解密 |
| 服务器列表 | `https://nova-static.yostar.cn/meta/serverlist.html` | ✅ 已解密(见前报告) |
| 公告列表 | `https://nova-static.yostar.cn/notice/noticelist.html` | 同源，同套加密 |
| 游戏网关 | `https://nova.yostar.cn/agent-zone-1/` | 登录/下发下载CDN |
| 安装包 | `https://nova-pkg.yostar.cn/pubplat/gpp/sdkpackage/prod/game_apk_v2/Official/3f056a0a4b954b5fa62fb2ecc7fed2b4/StellaSora.apk` | 来自 serverlist |

---

## 五、产物
- `tmp/REVERSE/ios_meta_dec.bin`  解密后的 iOS 资源清单(protobuf)
- `tmp/REVERSE/ios_manifest.csv`  19,493 条 bundle 明细(名/hash/大小/版本)
- `tmp/REVERSE/UpdateResource_MoveNext.c`      Booter 更新流程反编译
- `tmp/REVERSE/DownloadResourceBundle_MoveNext.c` bundle 下载反编译
- `tmp/REVERSE/dec_meta.py` / `parse_meta.py` / `stats.py`  解密与解析脚本
