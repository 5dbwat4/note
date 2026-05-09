# ExtensionActivityEdge — 文件膨胀根因分析

**数据库文件:** `ExtensionActivityEdge` | **大小:** 1.5 GB | **行数:** 55,494,368

---

## 核心结论

文件巨大的唯一原因：**Microsoft Edge 内置的「新标签页」扩展** (`hhmmmnlcbiambakodajpbmgicigdajjo`) 产生了 5500 万条遥测日志，占总事件的 **99.2%**。其余四个扩展加起来仅占 0.8%，对文件大小的贡献可忽略不计。

---

## 1. 文件详细结构

### 1.1 整体格式

该文件是一个 **SQLite 3** 数据库，由 Microsoft Edge 浏览器在后台自动维护，路径通常位于用户配置目录下。文件包含 **5 张表**，通过整数 ID 查表法实现字符串和 URL 的去重压缩。

### 1.2 表结构（DDL）

```sql
-- 字符串去重表：存储所有扩展 ID、API 名称、页面标题等文本
CREATE TABLE string_ids(
    id    INTEGER PRIMARY KEY,
    value TEXT    NOT NULL
);
CREATE UNIQUE INDEX string_ids_index ON string_ids(value);

-- URL 去重表：存储所有页面 URL 和参数 URL
CREATE TABLE url_ids(
    id    INTEGER PRIMARY KEY,
    value TEXT    NOT NULL
);
CREATE UNIQUE INDEX url_ids_index ON url_ids(value);

-- 主事件日志表（核心）
CREATE TABLE activitylog_edge_compressed(
    extension_id_x INTEGER NOT NULL,   -- FK → string_ids.id
    time           INTEGER,            -- 微秒，自 1601-01-01 UTC 起
    action_type    INTEGER,            -- FK → string_ids.id（事件分类标签）
    api_name_x     INTEGER,            -- FK → string_ids.id（调用的 API）
    args_x         INTEGER,            -- FK → string_ids.id（JSON 序列化的参数）
    page_url_x     INTEGER,            -- FK → url_ids.id（事件发生时的页面 URL）
    page_title_x   INTEGER,            -- FK → string_ids.id（页面标题）
    arg_url_x      INTEGER,            -- FK → url_ids.id（作为参数传递的 URL）
    other_x        INTEGER             -- FK → string_ids.id（额外元数据）
);

-- 已提交/上传的扩展列表
CREATE TABLE activitylog_edge_submissions(
    extension_id_x   INTEGER PRIMARY KEY,
    submit_request_id VARCHAR
);

-- 被排除出日志记录的扩展列表
CREATE TABLE activitylog_edge_excluded_ids(
    extension_id_x INTEGER PRIMARY KEY
);
```

### 1.3 压缩机制：ID 查表法

主表 `activitylog_edge_compressed` 中除 `time` 列外所有列都是对 `string_ids` 或 `url_ids` 的外键引用，存储的是整型 ID 而非原始字符串。

**工作原理：**

```
activitylog_edge_compressed          string_ids                url_ids
┌──────────────────────┐    ┌─────────────────────┐    ┌──────────────────┐
│ extension_id_x = 8   │───▶│ id=8  │ value=      │    │ id=1 │ value=    │
│ api_name_x     = 1   │───▶│       │ "hhmmmn..." │    │      │ "about:   │
│ page_url_x     = 5   │───┼─────────────────────│    │      │ blank"    │
│ action_type    = NULL│   │ id=1  │ value=      │    ├──────────────────│
│ ...                  │   │       │ "runtime.   │    │ id=5 │ value=    │
└──────────────────────┘   │       │ getURL"     │    │      │ "https:// │
                           └─────────────────────┘    │      │ cn.bing.  │
                                                      │      │ com/..."  │
                                                      └──────────────────┘
```

每次插入事件时：
1. Edge 将字符串值在 `string_ids` 表中查找（通过唯一索引 `string_ids_index`）
2. 若已存在则复用已有 ID，若不存在则插入新行获得新 ID
3. 主表中仅存储该整数 ID

本例中 5500 万条事件仅对应 **518 个去重字符串**和 **380 个去重 URL**，压缩效果显著。

### 1.4 时间戳编码

`time` 列的值是自 **1601-01-01 00:00:00 UTC** 起的**微秒数**（即 Windows `FILETIME` 结构的变体——FILETIME 本身是 100 纳秒单位，此处为微秒单位）。转换公式：

```
unix_timestamp_seconds = (time_value - 11644473600000000) / 1000000
```

其中 `11644473600000000` 是 1601-01-01 到 1970-01-01 之间的微秒数。

**示例：**

```
原始值：13422629751250010
Unix 秒：(13422629751250010 - 11644473600000000) / 1000000 = 1778155849
UTC 时间：2026-05-07 12:15:51
```

### 1.5 `action_type` 与 `api_name_x` 的区别

| 列 | 含义 | 典型值 |
|----|------|--------|
| `action_type` | 事件的**分类标签**，通常是触发该事件的扩展 ID，或概括性的操作名 | `运行时.getManifest`、扩展 ID、`tabs.onActivated`；多数为 NULL |
| `api_name_x` | 被调用的**具体 Chrome/Edge Extension API** 名称 | `runtime.getURL`、`topSites.get`、`storage.get`、`webRequest.onCompleted/s4` |

两者配合使用：`api_name_x` 描述"调用了什么"，`action_type` 描述"这次调用的上下文分类"。例如 uBlock Origin 调用 `webRequest.onCompleted` 时，`api_name_x` 是具体的事件监听器名称，`action_type` 则标记为扩展自身 ID。

### 1.6 `other_x` 字段的元数据

该字段以 JSON 格式存储附加上下文，本数据库中仅出现 4 种值：

| 值 | 含义 | 事件数 |
|----|------|--------|
| `{"dom_verb":0}` | DOM 元素插入操作 | 74,599 |
| `{"dom_verb":2}` | DOM 元素移除操作 | 25,070 |
| `{"web_request":{"cancel":true}}` | 网络请求被拦截/取消 | 51 |
| `{"web_request":{"added_request_headers":true}}` | 请求头被修改 | 6 |

该字段主要由内容拦截类扩展（uBlock Origin、拦截助手）使用，用于标注其对页面 DOM 或网络请求的具体操作类型。

### 1.7 索引情况

本数据库**未在主表上创建任何用户索引**。`activitylog_edge_compressed` 表纯为堆表写入，依靠 SQLite 隐式的 `rowid` 进行物理排序。这意味着：

- **写入极快**：所有 INSERT 均为追加写，无需维护 B-tree 索引
- **查询需全表扫描**：按扩展 ID 或时间过滤均需遍历全部 5500 万行
- `string_ids` 和 `url_ids` 表有唯一索引用于去重查找

### 1.8 行存储估算

每行 9 个 INTEGER 列（8 字节/列 × 9 = 72 字节），加上 SQLite 的行头（varint 类型编码、payload 长度等约 6-10 字节），每行约 **80 字节**。

```
55,494,368 行 × 80 字节 ≈ 4.4 GB（未压缩理论值）
实际文件大小 = 1.5 GB（SQLite 内部页压缩 + 空闲页回收后的值）
```

部分页面可能存在碎片或空闲空间。数据库文件的 `PRAGMA page_count` 和 `PRAGMA freelist_count` 可用于进一步分析物理存储效率。

### 1.9 数据流示意

```
Edge 浏览器
  │
  ├─ 新标签页扩展 ── runtime.getURL() ──▶ 写入 1 条事件 ──┐
  │                 ── topSites.get() ──▶ 写入 1 条事件 ──┤
  │                                                        │
  ├─ uBlock Origin  ── webRequest.* ────▶ 写入 1 条事件 ──┤
  │                 ── tabs.* ──────────▶ 写入 1 条事件 ──┤
  │                                                        ▼
  ├─ 拦截助手       ── storage.* ───────▶ 写入 1 条事件   activitylog_edge_compressed
  │                                                        (55,494,368 rows)
  ├─ Tampermonkey   ── runtime.* ───────▶ 写入 1 条事件
  │
  └─ 写入前先查 string_ids / url_ids 去重，获得整数 ID
```

---

## 2. 数据构成

| 扩展 ID | 事件数 | 占比 | 身份 |
|---------|--------|------|------|
| `hhmmmnlcbiambakodajpbmgicigdajjo` | 55,066,209 | **99.2%** | Edge 新标签页（内置） |
| `amkbmndfnliijdhojkpoglbnaaahippg` | 284,766 | 0.5% | 拦截助手（广告过滤） |
| `mnbndgmknlpdjdnjfmfcdjoegcckoikn` | 139,845 | 0.3% | uBlock Origin |
| `odfafepnkmbhccpbejgmiehpchacaeak` | 3,471 | <0.01% | uBlock Origin（dev 版） |
| `cibapackfcllpcpcaljibcmocljaadog` | 77 | <0.01% | Tampermonkey |

---

## 3. 新标签页扩展在做什么？

该扩展所有事件仅涉及两类 API 调用，合计 5506 万次：

| API | 调用次数 | 占比 | 用途 |
|-----|---------|------|------|
| `runtime.getURL` | 45,043,554 | 81.8% | 获取本地资源 URL（top site favicon 图标） |
| `topSites.get` | 10,017,958 | 18.2% | 获取最常访问站点列表 |

### 调用模式分析

每次打开一个新标签页（或新标签页获得焦点），Edge 会执行以下操作：

1. 调用 `topSites.get` — 拉取当前用户的 Most Visited 站点列表
2. 对列表中每个站点，调用 `runtime.getURL` — 获取该站点的 favicon 图标资源路径

以平均每页 8 个 top site 计算：1 次 `topSites.get` + 8 次 `runtime.getURL` ≈ **每条新标签页产生约 9 条事件**。

据此推算：5506 万 ÷ 9 ≈ 在 2 天内打开了约 **610 万次新标签页**（或者说新标签页被激活/渲染了这么多次）。

### 频率验证

- 时间跨度：2026-05-07 12:15 ~ 2026-05-09 20:21（约 56 小时）
- 平均速率：**~275 事件/秒**，持续不断
- 这两个 API 的 `action_type` 全部为 NULL，`args_x` 全部为 NULL，`page_url_x` 几乎全部为 NULL（仅 462 条有值）——说明这些事件**与用户浏览的具体网页无关**，纯粹是新标签页内部的后台轮询/渲染行为

---

## 4. 事件密度的时间特征

| 扩展 | 活跃开始 | 活跃结束 | 持续时长 |
|------|---------|---------|---------|
| Edge 新标签页 | 05-07 12:15 | 05-09 20:21 | ~56 小时（全程） |
| uBlock Origin | 05-07 12:15 | 05-09 19:36 | ~55 小时 |
| 拦截助手 | 05-07 12:15 | 05-09 20:21 | ~56 小时 |
| uBlock (dev) | 05-07 12:15 | 05-07 12:18 | ~3 分钟 |
| Tampermonkey | 05-08 02:55 | 05-08 04:30 | ~95 分钟 |

Edge 新标签页扩展从系统启动到关机的整个会话期间**持续不断**地产生事件，没有间歇。

---

## 5. 数据库压缩效果评估

虽然文件已经 1.5 GB，但 Edge 已经采用了去重压缩：

| 指标 | 数值 |
|------|------|
| 总事件数 | 55,494,368 |
| 去重后字符串数 | 518 |
| 去重后 URL 数 | 380 |

数据库使用 ID 查表法：`string_ids` 和 `url_ids` 两张表存储所有去重后的字符串和 URL，主表 `activitylog_edge_compressed` 中仅存储整数外键引用。

如果没有这套压缩，假设每条事件平均存储 200 字节的扩展 ID、API 名称、URL 等字符串：
- 未压缩：55M × 200B ≈ **11 GB**
- 压缩后实际：**1.5 GB**
- 压缩比约 **7:1**

即便如此，5500 万行 × 每行 9 个 INTEGER 列（约 72 字节 + 索引开销）本身就接近 4 GB 的原始数据量。SQLite 的存储效率使之缩减到 1.5 GB，但**行数本身才是根本问题**。

---

## 6. 列填充情况——说明事件"有多空"

| 列 | 非 NULL 行数 | 填充率 |
|----|-------------|--------|
| `extension_id_x` | 55,494,368 | 100% |
| `time` | 55,494,368 | 100% |
| `action_type` | 168,087 | 0.3% |
| `api_name_x` | 55,494,368 | 100% |
| `args_x` | 2,192 | 0.004% |
| `page_url_x` | 100,825 | 0.2% |
| `page_title_x` | 86,252 | 0.2% |
| `arg_url_x` | 18,267 | 0.03% |
| `other_x` | 99,726 | 0.2% |

**99.7% 的事件**（来自新标签页扩展）仅填充了 `extension_id_x`、`time`、`api_name_x` 三个字段，其余列全为 NULL。这些事件携带的信息量极低——本质上就是「新标签页又在请求 favicon 了」被记录了 5500 万次。

---

## 7. 其他扩展的事件属于正常范围

| 扩展 | 事件数 | 时间跨度 | 每秒事件 | 主要行为 |
|------|--------|---------|---------|---------|
| 拦截助手 | 284,766 | 56h | 1.4 | 广告过滤、DOM 操作、上下文菜单 |
| uBlock Origin | 139,845 | 55h | 0.7 | 网络请求拦截、脚本注入 |
| uBlock (dev) | 3,471 | 3min | 19.8 | 短暂初始化后即被排除 |
| Tampermonkey | 77 | 95min | 0.01 | 少量 manifest 读取 |

这四个扩展的总事件量（42.8 万）在 2 天内完全合理，对数据库大小的贡献仅为 ~12 MB（按比例估算）。

---

## 8. 根因总结

```
1.5 GB = Edge 新标签页的「top sites 图标遥测风暴」
         ├─ runtime.getURL   × 45,043,554  (每个 top site 图标路径)
         ├─ topSites.get     × 10,017,958  (每次拉取站点列表)
         └─ 其余 4 个扩展   ×    428,159  (贡献 <12 MB，可忽略)
```

**直接原因：** Edge 新标签页扩展对自身的每一次 `runtime.getURL` 和 `topSites.get` 调用都向 Activity Log 写入一条记录。

**放大因素：** 新标签页是浏览器中使用频率最高的页面——每次打开新标签、切换回新标签页、甚至后台刷新都可能触发这些调用。2 天 5500 万次说明几乎处于持续高频触发状态。

**建议：** 如需缩减此文件大小，可在 Edge 中禁用新标签页的扩展活动日志（如果相关策略支持），或定期清理此数据库文件。Edge 自身是否在后续版本中对此做了采样/限流优化值得关注。

---

*分析基于 SQLite 直接查询，数据截至 2026-05-09 20:21 UTC。*
