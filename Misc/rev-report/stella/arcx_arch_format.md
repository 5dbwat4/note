# .arcx / .arch 封包格式 —— 逆向文档与解包指南

> 目标：说明星塔旅人自定义资源封包 `.arcx`(BAR) 与 `.arch`(ZIP) 的格式、
> 压缩/加密算法、关键代码位置，并提供解包工具。
> 状态：**已完整逆向并实测验证**（XOR key / LZ4 / XXHash64 / 条目偏移全部对上）。

---

## 0. 结论速览

| 文件 | 本质 | 压缩 | 加密 | 逆向方式 |
|---|---|---|---|---|
| `data.arcx` / `lua.arcx` | 自定义 **BAR 归档** | **LZ4 block** | **XOR**（表头）+ **XXTEA**（内容）| 本文工具 `unpack_arcx.py` |
| `hotfix.arch` | 标准 **ZIP** | Deflate | 无 | `unzip` → `Hotfix.dll` → dnSpy/ILSpy |
| `p_*.arcx` / `p_*.arch` | **BSDIFF40** 增量补丁 | bzip2(内部) | 无 | 先 `bspatch` 合成完整包，再按上两行处理 |

**两层结构（关键）**：
- **第一层 = BAR 容器**：XOR 密钥 `&^^%#$#_$!@![]<_>?GHBFR_7481SDR_`（表头），条目数据 LZ4
- **第二层 = 单文件内容**：**XXTEA**（delta `0x9E3779B9`），密钥 =
  `MD5( BitConverter.GetBytes((int)(255*255)) )` = `MD5(01 FE 00 00)` =
  **`a921a467c7d7df396e60909c31225bd2`**
- 文件名 hash = `XXHash64(name)`；映射在 `data.json` / `lua.json`（明文）

**解密后**：`.bytes`=protobuf、`.json`/`.txt`=文本、`.lua`=**Lua 5.3 字节码**（`\x1bLuaS`）

---

## 1. BAR (.arcx) 二进制格式

### 1.1 ArchiveHeader（24 字节，全 u32 小端）
```
偏移  字段         说明
0x00  Magic        0x5241421A  = 字节 1A 42 41 52 ("\x1aBAR")
0x04  Version      102
0x08  Flag         位标志（见 1.3）
0x0C  OriginSize   条目表解压后大小
0x10  Size         条目表压缩后大小（紧跟 header，从偏移 24 开始）
0x14  EntryCount   条目数
```

### 1.2 ArchiveEntry（20 字节，紧凑排列，位于解密解压后的条目表中）
```
偏移  字段         类型   说明
0x00  Hash         u64    XXHash64(文件名)
0x08  Offset       u32    条目数据在【文件绝对偏移】(stream.Seek 绝对定位)
0x0C  OriginSize   u32    解压后大小
0x10  Size         u32    存储大小（LZ4 压缩后）
```

### 1.3 Flag 位定义（来自 `ArchiveHeader` getter）
| 位 | 属性 | 含义 |
|---|---|---|
| bit0 (0x001) | `IsHeaderCompressed` | 条目表用 LZ4 压缩 |
| bit4 (0x010) | `IsHeaderEncrypted` | 条目表用 XOR 加密 |
| bit8 (0x100) | `IsEntryCompressed` | 每条数据用 LZ4 压缩 |
| bit12 (0x1000)| `IsEntryEncrypted` | 每条数据用 XOR 加密 |

**实测 `data.arcx`/`lua.arcx` 的 Flag = `0x111`**：
条目表 = LZ4+XOR；每条数据 = 仅 LZ4（**不加密**）。

### 1.4 解析步骤
```
1. 读 24B header
2. 读条目表 = data[24 : 24+Size]
   - 若 bit4: XOR 解密  data[i] ^= KEY[i % 31]
   - 若 bit0: LZ4 解压到 OriginSize
3. 遍历 EntryCount 条 (每 20B): Hash, Offset(绝对), OriginSize, Size
4. 每条: raw = data[Offset : Offset+Size]
   - 若 bit12: XOR 解密
   - 若 bit8 : LZ4 解压到 OriginSize
5. 文件名 = json_map[Hash]（无则用 hash 十六进制命名）
```

---

## 2. 关键代码位置（IDA VA / dump.cs）

### 2.1 类
| 类 | TypeDefIndex | 作用 |
|---|---|---|
| `Archive` | 16385 | 归档对象（entries/Header/ReadFile/Open）|
| `ArchiveEntry` | 16387 | 条目结构（Hash/Offset/OriginSize/Size）|
| `ArchiveHeader` | 16388 | 头结构（Version/Flag/…/EntryCount）|
| `ArchiveUtil` | 16390 | **密钥/XOR/XXHash64/读写工具** |
| `LZ4Codec` | 22509 | LZ4 解码器 |

### 2.2 方法（VA）
| VA | 方法 | 作用 |
|---|---|---|
| 0x293E6F0 | `Archive.Open(path)` | 打开归档 |
| 0x293E9FC | `sub_293E9FC`（读 Header）| 校验 magic `0x5241421A`、读 6×u32 |
| 0x293EE18 | `sub_293EE18`（读条目表）| 用 Flag bit0/bit4 解表 → 填 ArchiveEntry[] |
| 0x293D968 | `Archive.ReadFile(hash)` | 查条目→读数据→解压解密 |
| **0x293F0FC** | 分派器 | 按 (compressed,encrypted) 选 4 条路径 |
| 0x2940138 | `UncompressDecryptStream` | LZ4 + XOR（compressed&encrypted）|
| 0x2940414 | `sub_2940414` | 仅 LZ4（compressed）→ `LZ4Codec.Decode` |
| 0x29402D0 | `DecryptStream` | 仅 XOR（encrypted）|
| 0x293FC4C | `ArchiveUtil.ReadExactly` | 无压缩无加密，直接读 |
| **0x77CBDC4** | `LZ4Codec.Decode` | LZ4 block 解压 |
| **0x29400A8** | `ArchiveUtil.XorEncryptDecrypt` | XOR 加解密（对称）|
| 0x293F310 | `ArchiveUtil.get_Key` | 返回 XOR 密钥（由 KEY_STR 初始化）|
| **0x293F3F8** | `ArchiveUtil.XXHash64(string)` | 文件名 → u64 hash |
| 0x293E0A8 | `ArchiveUtil.NormalizeFileName` | 文件名归一化（算 hash 前）|

### 2.3 XOR 算法（0x2940138 / 0x29402D0 反编译核心）
```c
// data[i] ^= key[i % key.Length]   —— 对称，加解密同一函数
for (i=0; i < len; i++)
    data[i] = key[i % keyLen] ^ data[i];
```

### 2.4 密钥常量（`ArchiveUtil`）
```
private const string KEY_STR = "&^^%#$#_$!@![]<_>?GHBFR_7481SDR_";   // 31 字节
internal static byte[] Key;   // = ASCII(KEY_STR)，在 .cctor 里赋值
```

---

## 2.5 第二层加密：XXTEA（单文件内容）⭐

容器解出的每个文件**仍是密文**，被 `GameDataController.LoadTableBinData`
(0x2B99154) / `LoadTextBinData` (0x2B98F04) 读出后立刻走 `AC.DA/AC.DT` 解密。

### 类
| 类 | TypeDefIndex | 作用 |
|---|---|---|
| `AC` | 16431 | 第二层包装：`DA(byte[])`/`DT(byte[])`/`get___CK`（生成密钥）|
| `AC.H` | 16430 | **MD5 实现**（`C(byte[])`），常量 `0x67452301…` |
| `XTA` | 16585 | **XXTEA**（`E`/`D`/`_D`/`TU3A`/`TBA`），delta `0x9E3779B9` |

### 方法（VA）
| VA | 方法 | 作用 |
|---|---|---|
| 0x2B99154 | `GameDataController.LoadTableBinData` | 从归档读表 → 调 `AC.DA` |
| 0x2B98F04 | `GameDataController.LoadTextBinData` | 从归档读文本 → 调 `AC.DA` |
| 0x2951F88 | `AC.DA(byte[])` | 取密钥 `__CK` → `XTA._D` 解密 |
| 0x29519C4 | `AC.get___CK()` | 计算 `int32(__kx*__ky)` → 4字节 → `AC.H.C`(MD5) |
| 0x2951A68 | `AC.H.C(byte[])` | **MD5**，返回 16 字节摘要（= XXTEA key）|
| 0x2952758 | `AC.H.PI` | MD5 填充（`0x80` + 位长）|
| 0x29A4AC8 | `XTA.D(byte[],byte[])` | XXTEA 解密外壳（取前 16B key）|
| **0x29A4C2C** | `XTA._D(uint[],uint[])` | **XXTEA 解密核心** |
| 0x29A3EF4 | `XTA.TU3A(byte[],bool)` | bytes→uint32[]（LE），includeLength |
| 0x29A4360 | `XTA.TBA(uint[],bool)` | uint32[]→bytes，末字为原始长度 |
| 0x29521E4 | `AC..cctor` | 写 `__kx/__ky`（`0xFF000000FF` → 均 255）|

### 密钥推导（关键，易错点）
```
seed_int = AC.__kx * AC.__ky = 255 * 255 = 65025
seed_bytes = BitConverter.GetBytes((int)seed_int)   // int32 小端 = 01 FE 00 00
key = MD5(seed_bytes)                                // 16 字节
    = a9 21 a4 67 c7 d7 df 39 6e 60 90 9c 31 22 5b d2
```
⚠️ **不是** `MD5("65025")`（字符串）。`sub_7ADA678` = `BitConverter.GetBytes(int)`，
喂给 MD5 的是 **4 个原始字节**，不是十进制 ASCII。

### XXTEA 参数
- `delta = 0x9E3779B9`；轮数 `q = 6 + 52/n`（n=uint32 个数）
- **includeLength**：解密输入 = false（不追加长度字）；
  解密**输出** = true（数组**末尾字**为原始字节长度，用于截断）
- 字节序：LE（`TU3A` 按 `<<(i*8)` 组包）

### 解密后各类型
| 扩展名 | 解密后 |
|---|---|
| `.bytes` | protobuf（头含版本串如 `0.1.0.2` + 字段名）|
| `.json` / `.txt` | UTF-8 文本 |
| `.lua` | **Lua 5.3 字节码**（magic `\x1bLuaS`，含原始编译路径）|

---

---

## 3. .arch (hotfix) 格式

- 标准 ZIP（`PK\x03\x04`），首个成员 `Hotfix.dll`
- 由 `Booter.SetupHybridCLR`（State=14）加载，引导类
  `AIScript.Booter.HotfixBooter`（HybridCLR 热更 C# 程序集）
- 相关常量：
  - `HybridCLRManager.kHybridCLRDllBundleName = "hotfix.arch"`
  - `AISCRIPT_DLL_NAME = "Hotfix.dll"`, `AISCRIPT_DLL_PATH = "HotFix/bin_output/"`
- **逆向**：`unzip hotfix.arch` → 得 `Hotfix.dll` → dnSpy / ILSpy 反编译（普通 .NET）

---

## 4. patch 包（p_* 前缀）

- 头 8 字节 `BSDIFF40`，随后 3 个 u64 长度 + 3 段 **bzip2** 流（ctrl/diff/extra）
- 对应 `ResourceBundleManifest.BinaryDiffPatchInfo`
- 还原：`new = bspatch(old, p_N_*.xxx)`，old 为上一版本的完整文件
- 还原出的仍是 `.arcx`(BAR) 或 `.arch`(ZIP)，再按第 1/3 节解

---

## 5. 实测验证记录（data.arcx）

```
Flag=0x111 EntryCount=628 HeaderOrigin=12560 HeaderSize=11980
条目表: XOR(KEY) + LZ4 -> 12560B ✓ (== OriginSize)
entry0: hash=15df1e46f0aca252 off=12649 originSize=53128 size=53338
  json_map[hash] = "bin/ai.bytes" ✓
  XXHash64("bin/ai.bytes") = 1576011684637352530 == json.hash ✓
  data[off:off+size] --LZ4--> 53128B ✓ (== OriginSize)
```
偏移为**文件绝对偏移**；entry 数据仅 LZ4、不加密（Flag bit12=0）。

---

## 6. 工具

`tmp/REVERSE/unpack_arcx.py`：
- 解析任意 `.arcx`（自动按 Flag 处理 XOR/LZ4，4 种组合全支持）
- **自动执行第二层 XXTEA 解密**（`--no-layer2` 可关闭，保留密文）
- 读同目录 / 指定 `--names data.json` 做 hash→文件名映射
- 输出到 `<out>/<原始相对路径>`；映射缺失的用 `unknown/<hash>.bin`
- 依赖：`pip install lz4 xxhash`

实测：`data.arcx`(628) + `lua.arcx`(2091) 全部解出，json/txt/bytes/lua 内容
均为明文。用法见文件头 docstring。`hotfix.arch` 直接 `unzip` 即可，无需本工具。

> `.lua` 解出为 Lua 5.3 字节码，如需源码可用 `unluac`/`luadec` 反编译。
