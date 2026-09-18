# 静态逆向报告：metadata 解包 + 更新包下载机制

> 承接 progress.md。本报告记录两件事的**纯静态**成果：
> 1. 离线解包被混淆的 `global-metadata.dat`（不依赖动态调试）
> 2. 从解包后的 IL2CPP 符号完整还原"更新包如何获取/下载"

---

## 一、global-metadata.dat 静态解包（已完成）

### 1.1 包装格式（实测确认）
```
0x000  uint32 magic       = 0x1357FEDA
0x004  uint32 payloadSize = 28,543,988
0x008  256B  params 表    (变换常量表, 解释器的 X2)
0x108   64B  bytecode     (变换程序, 解释器的 X0)
0x148  payload           (被变换, 头部 "CODEPJIL")
       payload 解出后头 8 字节 = "CODEPHIL"(成功标记)
0x150  真正的 Il2CppGlobalMetadataHeader (magic 0xFAB11BAF)
文件总长 28,544,316 = 0x148 + payloadSize，吻合
```

### 1.2 解包函数 sub_17192C8
```c
if (*(u32*)file != 0x1357FEDA) return true;      // 未包装
for (off=0; off < payloadSize; off += 64)
    sub_14E30CC(file+0x108, 64, file+0x008, payload+off, min(64, rem));
if (memcmp(payload, "CODEPHIL", 8)) return false;
*out = file + 0x150;                              // 真 metadata
```
参数：`sub_14E30CC(X0=bytecode@0x108, X1=64, X2=params@0x008, X3=块缓冲, X4=块长)`

### 1.3 变换函数 sub_14E30CC = 线程化字节码解释器
- 函数体 `0x14E30CC–0x14E5134`（8296B）
- dispatch 表 `word_999F710`：256 × uint16，`handler = loc_14E30E0 + tbl[opcode]*4`
- 逐条读 bytecode 字节作 opcode 跳到 handler，每个 handler 用
  `idx = magic_const % blocklen` 定位 `buffer[idx]`，做 XOR/ADD/SUB/字节置换组合
- 属**定制表驱动混淆**，非标准 AES

### 1.4 静态还原方法：Unicorn 忠实模拟
关键洞察：**解释器本身就是解密器**，无需逆转全部 handler 语义，直接在 Unicorn 里
执行这段 ARM64 机器码即可。
- 脚本：`tmp/REVERSE/emulate.py`
- 把 CODE(8296B)、dispatch 表(512B)映射进内存，逐 64B 块设置寄存器并 `emu_start`
- **结果**：`tmp/REVERSE/global-metadata-decoded.dat`
  - 头 8B = `CODEPHIL`，剥离后 magic=`0xFAB11BAF`, version=**31**
  - 全部 header offset/size 落在范围内
  - 明文类名可搜到：`ResourceManager`×46, `AssetBundle`×189

### 1.5 Il2CppDumper 成功
- 工具：`Il2CppDumper-win-v6.7.46`（支持 metadata v31）
- 输入：UnityFramework + 解包后的 metadata
- CodeRegistration=`0xA024E30`，MetadataRegistration=`0xA366A38`（与 re-stellasora.txt 完全一致）
- 输出：`tmp/REVERSE/dumper_out/`（dump.cs 58MB、script.json、stringliteral.json、il2cpp.h）

---

## 二、更新包获取 / 下载机制（完整还原）

命名空间核心类：**DownloadStore**（86 方法）、**ResourceBundleManifest**（51 方法）、
**GameResourceLoader**（44 方法，上层资源加载）。所有地址即 IDA VA（imagebase=0）。

### 2.1 平台名 GetPlatformName() @ 0x296747C
按 `Application.platform` 返回：`mac`/`win`/**`ios`**/`and`/`web`/`oth`。本包 = **ios**。

### 2.2 manifest 文件名格式

`GetRemoteResourceManifestFileName(prefix, platform, version, additional)` @ `0x29676CC`
`GetLocalResourceManifestFileName(prefix, platform, additional)`          @ `0x296E700`
两者都调用 `string.Join("_", ...)`（分隔符常量 `_` @ 0xA887B58）。

在 `DownloadResourceBundleManifest` 协程 MoveNext(`0x2966774`) 中实测拼接：
```
name = Join("_", vendorPlatformName, GetPlatformName(), additionalTag)   // "_"
name = name + ".mani"                                                    // 后缀 .mani (0xA85EFE8)
name = patchPrefix + name                                               // 见 2.3
```
其中 `additionalTag`：普通=`""`(0xA85AC70)，附加清单=`"_add"`(0xA8894B8)。

manifest 类型（manifestType）：
- 主资源清单 prefix = `res_meta`（磁盘上就是 `res_meta.unity3d`）
- 内置清单 = `install_resource_manifest.mani`
- 附加清单 = `supp_res.mani`

### 2.3 patch 版本前缀 sub_2967760(patchVersion)
```
= string.Format("{0}{1}", "p_", patchVersion) + "_m."
  → 例如 patchVersion=3 → "p_3_m."
```
即差分补丁清单/文件名会带 `p_<ver>_m.` 前缀（bin-diff patch 机制，见
`SetBinDiffPatchInfos`/`GetBinDiffPatchFiles`）。

### 2.4 manifest URL 拼接（协程 MoveNext 关键分支）
```c
if (remoteUrlMap 存在映射)                       // sub_2967860 查 URL 重定向表
    url = map[resourceManifestFileName];         // CDN 线路重定向
else
    url = string.Join(baseURL, "/", resourceManifestFileName);  // "/" @ 0xA85F0B0
request = CreateDownloadManifestRequest(url);    // 0x295D1C4
```

### 2.5 bundle 下载 URL 拼接 GetBundleDownloadUrl() @ 0x295CC84
```c
GetBundleDownloadUrl(baseUrl, bundleFileName, activeRemoteUrlMap):
    if (activeRemoteUrlMap && remoteUrlMap[bundleFileName] 命中)
        return 重定向URL;                        // sub_2967860
    sb = baseUrl;
    if (last char != '/' && != '\\') sb += "/";  // 0xA85F0B0
    sb += bundleFileName;
    return sb;
```
**即 `bundleURL = baseUrl + "/" + bundleFileName`**（除非 remote URL map 命中重定向到别的 CDN）。

### 2.6 完整下载流程（DownloadStore 方法链）
```
1. LoadBuiltinResourceManifest (0x295EB4C)
     读 Data/Raw/InstallResource/install_resource_manifest.mani
2. GetResVersion()(0x2AB7054) 从运行时配置取 resourceVersion
     baseURL 来自 ClientConfig 生产地址 / serverlist 下发
3. DownloadResourceBundleManifest(0x295F994) 下载远端 res_meta_*.mani
     URL = baseURL + "/" + (vendorPlatform_ios_.mani)
4. ResourceBundleManifest.Compare(0x296DA44) 与内置清单差分
     → QueryNeedUpdateBundles(0x295EF24) 得到 addList/需更新列表
     → Need full update / need patch update (bin-diff)
5. UpdateResourceBundles(0x295F69C) 并发下载
     每个 bundle: GetBundleDownloadUrl → SendAssetBundleRequest(0x2953564)
     → StoreAssetBundle(0x2953A5C) 写入 DownloadStore 缓存
6. 校验: ValidateFile(md5)(0x2959D80) + 解压 CRC32
     ConvertHTTPUriToStorageFilePath(0x295913C) 决定本地存储路径
7. ClearExpiredFiles(0x295AC50) 依据 $CLEAR_EXPIRED_FILES 清理旧文件
8. 差分补丁: DownloadResourceBundle(0x295FA80) 支持 patchInfo
     "Download and Patch bundle"，bin-diff 打补丁后落盘
```

### 2.7 存储/校验（DownloadStore）
- 存储区 StorageRegion 分区，`ConvertHTTPUriToStorageFilePath` 把 URL/文件名映射到本地路径
- 版本元数据：`InitVersionMetaData`/`GetFileVersion`/`CheckFileVersion` 逐文件记版本
- MD5：`ValidateFile`；日志标签 `<DownloadStore>`；重试 `Retry download resource`

---

## 三、最终的 URL 组装规则（结论）

```
资源基础地址 baseURL:
  生产 = https://nova-static.yostar.cn (ClientConfig)  或 serverlist/网关下发的 CDN
  回退 = http://127.0.0.1:5123/res

远端主清单 URL:
  baseURL + "/" + "<vendorPlatform>_ios_.mani"
  (差分补丁清单前缀 "p_<patchVer>_m.")

单个 bundle URL:
  baseURL + "/" + <bundleFileName>          // 如 global.unity3d
  ── 若 remote URL map 命中则重定向到其他 CDN 线路

清单/文件名常量:
  prefix : res_meta(主) / install_resource_manifest(内置) / supp_res(附加)
  platform: ios
  分隔符 : "_"(名) "/"(URL)
  后缀   : ".mani"(清单) 
  patch  : "p_{ver}_m." 前缀 + "_add" 附加标记
```

**要点**：真正的线上 baseURL 与 resVersion 由 **serverlist / 游戏网关运行时下发**
（`GetResVersion` 读运行时配置对象），并可经 **remote URL map 重定向到不同 CDN 线路**；
客户端只硬编码了 `nova-static.yostar.cn` 作为静态基址与本地回退地址。

---

## 四、工具/产物位置
- 脚本（全部在 `tmp/REVERSE/`）：
  - `emulate.py`         Unicorn 模拟解包
  - `verify_meta.py`     校验解包结果
  - `extract_strings.py` 抽取字符串字面量
  - `inspect_meta.py` / `find_class2.py` 等辅助
- 产物：
  - `tmp/REVERSE/global-metadata-decoded.dat`  解包后的明文 metadata
  - `tmp/REVERSE/dumper_out/`                   Il2CppDumper 完整输出
