# 星塔旅人 剧情文本还原 —— 完整逆向报告

> 目标：还原游戏内主线/支线剧情的**真实文本**,并建立**权威的**
> "剧情条目 → 标题 → 脚本 → 对话正文" 映射(全部来自游戏数据,非人工推断)。
> 状态:已完成。story.bytes 表 142 行 100% 解析,与 story.json 1:1 吻合。

---

## 0. 结论速览

- **剧情正文位置**:`lua/game/ui/avg/_cn/config/*.lua`(AVG 视觉小说脚本,403 个)
- **权威映射表**:`data/bin/story.bytes`(142 行) + `data/language/zh_cn/story.json`(标题)
- **映射链**:
  ```
  story.bytes: pid → { f6=标题key, f7=简介key, f15=前置脚本, f17=主线脚本, f9=战后CG, f2=战斗关卡 }
  story.json : Story.<pid>.1 → 中文标题, Story.<pid>.2 → 简介
  脚本代号   : STm01_01 → avg/_cn/config/stm01_01.lua (小写)
  ```
- **产物**:`story_final/00_索引.md`(142 条真实标题表)、`story_final/全剧情.md`(115 条含对话正文)

---

## 1. 重要更正(避免早期错误)

早期(v1)曾**推断** `stmCC_NN` 的 `CC` = 章节号,直接套 `StoryChapter.CC`。
**该映射是错误的**,例如:
- `STm01_01` 真实标题 = 《梦醒时分》(pid=101),不是笼统"第1章第1节"
- `STm01_05` → 《重返孤儿院》(pid=100);一个脚本可能被多个 pid 引用

**正确做法**:必须用 `story.bytes` 的真实字段映射,不能靠文件名猜。本报告即为更正后的权威结果。

---

## 2. 剧情正文的载体:AVG 脚本

### 2.1 定位
`lua.arcx`(合并到最新版后)解包 → `game/ui/avg/_cn/config/` 下 403 个 Lua5.3 字节码:

| 前缀 | 数量 | 含义 |
|---|---|---|
| `stm` | 103 | 主线剧情 (Story Main) |
| `stev` | 53 | 剧情事件/支线 |
| `stsp` | 44 | 特殊剧情 |
| `cg` | 124 | 角色专属剧情 (cg_<角色ID>_NN) |
| `dp`/`gd` | 9 | 决斗/抽卡 |

另有 `_cn/preset/avgcharacter.lua` = 说话人 id→名字 映射表(546 条)。

### 2.2 反编译
Lua 5.3 字节码(magic `\x1bLuaS`, 64-bit),用 **unluac.jar**(需 Java)反编译:
```
java -jar unluac.jar stm01_01.lua > out/stm01_01.lua
```
403/403 全部成功(`decompile_avg.py`)。
⚠️ unluac 输出编码不定:部分 UTF-16LE、部分 UTF-8;字符串以 `\ddd` 十进制转义
UTF-8 字节。解析时需按 BOM/空字节探测编码并还原转义(见 `extract_story.py`)。

### 2.3 AVG 指令格式
脚本是 `return { {cmd=..., param={...}}, ... }` 的命令数组:

| cmd | param 结构 | 含义 |
|---|---|---|
| `SetTalk` | `{nType, speakerId, text, nClearType, sVoice, ...}` | 对话(nType 决定显示模式,见 §2.5) |
| `SetMainRoleTalk` | `{dur, mood, pose, ...}` | 主角(玩家)发言 |
| `SetChoiceBegin` | `{tag, x, {...}, {选项文本...}}` | 分支选项 |
| `SetChoiceJumpTo` | `{tag, idx}` | 分支跳转 |
| `SetBg/SetStage/SetBGM/SetAudio/Wait/Clear...` | — | 演出控制 |

`speakerId`(如 `avg1_103`)→ 角色名+颜色(琥珀/`#99d2d9`)由 `avgcharacter.lua` 的
`{id, name, name_bg_color, surfix}` 映射;`"0"`=旁白、`"1"`=玩家。

### 2.4 `==...==` 特殊标记的转换(运行时)

对话文本里有 17 种 `==XXX==` 标记。转换逻辑在 **`utils.lua` 的
`ProcAvgTextContent(sContent, nLanguageIndex)`** 和 **`avg_4_talkctrl.lua`**:

```lua
-- utils.lua ProcAvgTextContent (关键行)
local nIndex = PlayerData.Base:GetPlayerSex() == true and 2 or 1   -- 2=男 1=女
sContent = ProcContentWord(sContent, true)
sContent = string.gsub(sContent, "==RT==", "\n")                          -- 换行
sContent = string.gsub(sContent, "==PLAYER_NAME==", GetPlayerNickName())  -- 玩家昵称
local mapSex = require(".../Preset/AvgUIText").SEX
for k, v in pairs(mapSex) do
    sContent = string.gsub(sContent, k, v[nIndex])   -- 按性别取 v[1]女/v[2]男
end
```

**三类标记:**

1. **文本替换类**(在 `ProcAvgTextContent`):
   - `==RT==` → 换行 `\n`
   - `==PLAYER_NAME==` → 玩家昵称(默认主角名 塞拉)
   - `==SEXn==` → 依玩家性别取值,映射表在 `avg/_cn/preset/AvgUIText.lua` 的 `SEX`:

   | 标记 | 女(index1) | 男(index2) | | 标记 | 女 | 男 |
   |---|---|---|---|---|---|---|
   | `==SEX1==` | 她 | 他 | | `==SEX11==` | 老太太 | 老头子 |
   | `==SEX2==` | 姐姐 | 哥哥 | | `==SEX12==` | 脖颈 | 腰间 |
   | `==SEX3==` | 大姐姐 | 大哥哥 | | `==SEX13==` | 白发的少女 | 黑发的少年 |
   | `==SEX4==` | 妹妹 | 弟弟 | | `==SEX14==` | 白头发 | 黑头发 |
   | `==SEX5==` | 小妹妹 | 小弟弟 | | `==SEX15==` | 姑娘 | 小伙 |
   | `==SEX6==` | 女皇 | 国王 | | `==SEX16==` | 魔女 | 男巫 |
   | `==SEX7==` | 小姐 | 先生 | | `==SEX17==` | 少女 | 少年 |
   | `==SEX8==` | 公主 | 王子 | | `==SEX18==` | 裙子 | 裤子 |
   | `==SEX9==` | 小女孩 | 小男孩 | | `==SEX19==` | 女仆 | 管家 |
   | `==SEX10==` | 姐妹 | 姐弟 | | `==SEX20==` | 衬衣 | 中衣 |
   |  |  |  | | `==SEX21==` | 小姐 | 小哥 |
   |  |  |  | | `==SEX==` | 女士 | 先生 |

   > 主角是玩家自定义性别的沉默主角,故大量代词/称谓用 `==SEXn==` 占位,
   > 运行时按存档性别替换。默认(女)时 `==SEX1==` → "她"。

2. **演出控制信号类**(在 `avg_4_talkctrl.lua`,显示时被移除,只影响节奏):
   - `==P==` `sParagraphSignal` → **段落/翻页**(整段翻页)
   - `==B==` `sBreakSignal` → **断句**(一个气泡内分句显示)
   - `==W==` `sWaitSignal` → **停顿点**(打字机效果中途等待,最常见 7827 次)
   - `==A<秒>==` `sAutoParagraphSignal`(正则 `==A(.+)==`)→ **自动翻页**,`<秒>`为延时
   - `==Off==` `sCenterBgOff` → **关闭居中背景**

   显示时用三级嵌套 `string.split` 拆分:`==P==`(段) > `==B==`(句) > `==W==`(停顿),
   逐级控制打字机播放节奏,拆完后信号本身 gsub 成空串。

**纯文本还原**:提取剧情时,`==RT==`→换行、`==PLAYER_NAME==`→主角名、
`==SEXn==`→按性别取词、其余演出信号(P/B/W/A/Off)→删除。已实装于
`extract_story.py` 的 `apply_markers()`,实测 31215 行 0 残留标记。
(样式化输出方案见 §2.6。)

### 2.5 说话 / 心想 / 旁白的区分:SetTalk 的 nType

`SetTalk` 的**第 1 个参数 `nType`**(不是时长)决定这句话的显示模式与日志分类,
逆向自 `avg_4_talkctrl.lua:SetTalk`(0 ≤ nType ≤ 11):

| nType | 显示模式 | 日志类型(AvgLogType) |
|---|---|---|
| 0 | 说话(带名字条,底部对话框) | Talk |
| 1 | 说(SayThink 气泡) | Talk |
| **2** | **心想(SayThink 气泡)** | **Thought** |
| 3 | 旁白/字幕(文本前缀说话人名) | Voiceover |
| 4 / 5 | 双人对话 1L / 1R(左/右名字条) | Talk |
| 6 / 7 | 双人对话 2L / 2R | Talk |
| 8 | 居中字幕旁白 | Voiceover |
| 9 | CG 对话 | Talk |
| 10 | CG 旁白 | Voiceover |
| 11 | Live2D 对话 | Talk |

代码依据(`avg_4_talkctrl.lua`):
```lua
function Avg_4_TalkCtrl:SetTalk(tbParam)
  local nType = tbParam[1]              -- 显示模式
  -- tbParam[2]=speakerId  tbParam[3]=text  tbParam[4]=nClearType  tbParam[5]=sVoice
  ...
  if nType == 2 then
    self.tbLogData.nType = AllEnum.AvgLogType.Thought   -- 心想
  end
  if nType == 1 or nType == 2 then
    self:_SwitchSayThink(nType, ...)     -- 说/想 共用气泡, 颜色不同(说#132C47 想#F1F4F6)
  end
```
实证:`{2, "avg3_100", "咦？这里是……"}` = 塞拉**心想**;
`{0, "avg1_103", "..."}` = 琥珀**说话**。

### 2.6 样式化输出方案(本工具)

`extract_story.py` **保留**控制符并转成带样式 HTML(而非删除),便于阅读时保留演出信息:

| 原标记 | 输出 HTML | 说明 |
|---|---|---|
| `==W==` | `<font color="grey">(Wait)</font>` | 停顿点 |
| `==B==` | `<font color="grey">(Break)</font>` | 断句 |
| `==P==` | `<font color="grey">(Paragraph)</font>` | 翻页 |
| `==A<秒>==` | `<font color="grey">(Auto<秒>)</font>` | 自动翻页 |
| `==Off==` | `<font color="grey">(CenterBgOff)</font>` | 关闭居中背景 |
| `==RT==` | `<br>` | 换行 |
| `==PLAYER_NAME==` | `<font color="#f4a742">PLAYER_NAME</font>` | 玩家名(保留标识+高亮) |
| `==SEXn==` | `<i><font color="#c86bd6">女词/男词</font></i>` | 性别词(斜体紫,女/男并列) |

说话人与台词渲染(按 §2.5 的 nType):
- **说话人名**:用 `avgcharacter.lua` 的真实 `name_bg_color` 包裹:
  `<font color="#99d2d9"><b>琥珀</b></font>`
- **心想**(nType=2):`名字（心想）：<i><font color="#8a9bb0">灰斜体台词</font></i>`
- **旁白**(nType=3/8/10):`名字（旁白）：台词`
- **普通说话**(其余):`名字：台词`

游戏原生富文本(`<size>/<color>/<r>` 等)清洗,注入的 `<font>/<i>/<br>` 保留。
输出样例:
```
塞拉（心想）：慢一点，轻一点……(Wait)很好，目标没有发现我们。
旁白：等待着一个幸运的，取走 她/他 的头颅的人。
琥珀：==PLAYER_NAME==,抱紧我,我带你下去。
```

### 2.7 游戏原生富文本标签(TextMeshPro)

对话文本用 Unity **TextMeshPro (TMP)** 渲染,含以下富文本标签(实测全 403 脚本统计):

| 标签 | 次数 | 标准? | 处理方式 |
|---|---|---|---|
| `<r=RUBY>BASE</r>` | 3290 | **自定义** | → `BASE（ruby:RUBY）` |
| `<size=N>`/`<size=N%>` | 1075 | TMP | 清除 |
| `<color=#RRGGBB>`/`<color=名>` | 178 | TMP | → 样式色(HTML `<font>` / UBB `[color]`) |
| `<alpha=#..>` | 16 | TMP | 清除(打字机逐字用) |
| `<voffset=..>` | 14 | TMP | 清除 |
| `<rotate=..>` | 14 | TMP | 清除 |
| `<mspace=..>` | 14 | TMP | 清除 |
| `<align=..>` | 4 | TMP | 清除 |
| `<b>` | 4 | TMP | 清除(源文本自带) |
| `<margin>`/`<margin-right>` | 2 | TMP | 清除 |

**`<r=...>` 是本游戏自定义注音(ruby)标签**,非标准 TMP。两种写法:
- `<r=Bo>魔</r>`(81 例):base=魔, ruby=Bo
- `魔<r=mowang></r>王`(1564 例):空标签,ruby=mowang 附加在前一字
运行时由 `avg_4_talkctrl.lua:_ProcRubyPos` 调 `NovaAPI.GetRubyPos` 计算位置,
重组为 `<r=ruby><rpos1=..><rpos2=..>base</r>`。

> **ruby 处理更正**:早期曾转 `<ruby><rt>`,但空 base 形式(`魔<r=X></r>王`)
> 会产出无内容的坏标签。现统一转为**内联文本** `BASE（ruby:RUBY）`
> (如 `魔（ruby:mowang）王`),简洁且不丢注音信息。

**保留/转换策略**(本工具, `clean_text`):
- `<r=..>` → `BASE（ruby:RUBY）` · `<color=..>` → 样式色
- 其余 TMP 标签(size/alpha/voffset/rotate/mspace/align/b/margin)清除
- 处理顺序:ruby → color(占位符 `\x01\x02` 保护)→ 清其余标签 → 还原 color →
  注入 `==标记==` 样式。实测 31215 行 **0 残留原生标签、0 残留 `<ruby>`**。

### 2.8 双样式输出:HTML / UBB

`extract_story.py --style {html|ubb}` 产出两种样式(逻辑共用,仅 `s_color/s_bold/
s_italic/s_break` 切换):

| 元素 | HTML | UBB |
|---|---|---|
| 颜色 | `<font color="X">..</font>` | `[color=X]..[/color]` |
| 粗体(说话人) | `<b>..</b>` | `[b]..[/b]` |
| 斜体(心想/性别) | `<i>..</i>` | `[i]..[/i]` |
| 换行(`==RT==`) | `<br>` | 真实换行 |
| 简介(合集,仅开头) | `> 引用` | `[quote]..[/quote]` |

- 输出目录:HTML → `story_text/`、`story_final/`、`story_all/`;
  UBB → `story_text_ubb/`、`story_final_ubb/`、`story_all_ubb/`
- **`[quote]` 仅用于每条剧情开头的简介**;正文对话只用 color/b/i。
- 编译器 `compile_story_v2.py` / `compile_all_stories.py` 均支持 `--style`。
塞拉（心想）：慢一点，轻一点……(Wait)很好，目标没有发现我们。
旁白：等待着一个幸运的，取走 她/他 的头颅的人。
琥珀：==PLAYER_NAME==，抱紧我,我带你下去。
```

---

## 3. 权威映射表:story.bytes 格式逆向

### 3.1 表容器格式(自定义二进制表)
所有 `data/bin/*.bytes` 由 `GameDataController.LoadCommonBinData`
(0x2B79360) + `LoadTableBinData`(0x2B99154) 加载,基于 .NET `BinaryReader`:

```
Header:
  [15 字节] 前导 (含 rowCount 标记 + 7bit 长度的版本串 "0.1.0.2" + 2 标志字节)
Row 1 (特殊, 多一个前导 key):
  key   : int32 LE        (142, 未用)
  pid   : int32 LE        (主键, = 剧情条目 id)
  blen  : uint16 LE       (blob 字节长度)
  blob  : blen 字节        (protobuf)
Row 2..N:
  pid   : int32 LE
  blen  : uint16 LE
  blob  : blen 字节
```

Reader vtable 方法(来自反编译):
- `+552`/`+584` = ReadInt32 / ReadInt64(主键)
- `+520` = ReadInt32(blob 长度)  ·  `+712` = ReadBytes(len)
- `+472` = ReadByte(表头标志)

### 3.2 blob 的 protobuf 字段(实测)
每行 blob 是标准 protobuf,关键字段:

| 字段 | 内容 | 例 |
|---|---|---|
| f6 | 标题 loc key | `Story.101.1` |
| f7 | 简介 loc key | `Story.101.2` |
| **f17** | **本节点主线剧情脚本** | `STm01_05` |
| **f15** | **graph 前驱链接**(= 上一节点的 f17) | `STm01_04` |
| **f9** | **战后CG脚本** | `C01_04` / `CBA01_05` |
| f2 | 战斗关卡代号 | `BAm01_05` |
| f19 | 关卡/舞台 id | `10701` |

> ⚠️ **f15 语义更正**(经用户指正并实证):f15 **不是**"本节点的前置剧情脚本",
> 而是**剧情 graph 的前驱边**——它指向**上一个节点的 f17 脚本代号**。
> 剧情是一张有向图(graph),f15 就是"上一节点"的链接。
>
> **实证**:
> - `f15 精确等于某前驱节点的 f17` 命中 **106/123**
> - 链条自洽:pid102(过去的痕迹).f15=`STm01_01` = pid101(梦醒时分).f17;
>   103→102→104→105 连成主线链
> - **分叉/汇聚**:pid108/109/110 的 f15 都=`STm01_07`(=pid107),说明 107 是
>   分叉点,分出《调查结果》《饭后甜点》《没有旅人的未来》三个结局分支;
>   pid111.f15=`STm01_08_c`(=pid109)则从 c 分支汇聚回主线 —— 典型 graph 结构
>
> 因此合集(`compile_story_v2.py`)**只输出本节点自身脚本(f17/f9)**,把 f15
> 解析为"前驱节点"标注,不重复输出其正文(否则每条都会带上一节点内容)。

### 3.3 解析结果(校验)
- 解析 **142 行**,字节 **19882/19882 全部消费完**
- **142/142** 行满足 `f6 == "Story.<pid>.1"`(自洽校验)
- 与 `story.json` 的 **142 个 distinct pid 完全 1:1**,零缺失
- pid 分布:第1章(13)、2章(17)、3章(17)、4章(17)、5章(19)、6章(22)、8章(25)、65xx特殊(12)

---

## 4. 真实标题样例(节选,全部来自游戏数据)

| PID | 标题 | 主脚本(f17) | 前置(f15) | 战后CG(f9) |
|---|---|---|---|---|
| 100 | 重返孤儿院 | — | STm01_05 | C01_05 |
| 101 | 梦醒时分 | STm01_01 | — | — |
| 102 | 过去的痕迹 | STm01_02 | STm01_01 | C01_01 |
| 103 | 消失的绿洲 | STm01_03 | STm01_02 | C01_02 |
| 107 | 不同的许愿 | STm01_07 | STm01_06 | C01_06 |
| 108 | 调查结果 | STm01_08_a | STm01_07 | C01_07_a |
| 110 | 没有旅人的未来 | STm01_08_b | STm01_07 | C01_07_b |
| 112 | 最终解释权 | STm01_10 | STm01_09 | C01_09 |

(108/109/110 = 同一节点的分支结局 a/b/c,印证 AVG 的 SetChoice 分支机制。)

---

## 5. 工作流与脚本

| 步骤 | 脚本 | 说明 |
|---|---|---|
| 1. 合并最新包 | `merge_arcx_patches.py` | v100 + 21 BSDIFF40 补丁链 → 最新 lua.arcx/data.arcx |
| 2. 解包+双层解密 | `unpack_arcx.py` | BAR(XOR+LZ4)+XXTEA → data/bin/*.bytes, lua/**.lua |
| 3. 反编译 AVG | `decompile_avg.py` | unluac 批量反编译 403 个脚本 (403/403 ok) |
| 4. 提取对话 | `extract_story.py` | 解析 AVG 指令 + avgcharacter 映射 → story_text/*.txt |
| 5. **解析映射表** | `parse_story_table.py` | 逆向 story.bytes → story_map.json (142 行, 权威) |
| 6. **重建合集** | `compile_story_v2.py` | pid→标题→脚本→正文 → story_final/ |

### 关键函数地址(IDA VA)
| VA | 函数 | 作用 |
|---|---|---|
| 0x2B79360 | `GameDataController.LoadCommonBinData` | 表加载主流程(BinaryReader) |
| 0x2B99154 | `LoadTableBinData` | 从归档读表 → 解密(见 arcx 报告) |
| 0x2B993B0 | `LoadPrimaryKeyIntTable` | int 主键行迭代 |
| 0x2B994F8 | `LoadPrimaryKeyStringTable` | string 主键行迭代 |

---

## 5.5 四大剧情体系(全覆盖)

除主线外, 另有 3 类剧情, 各有**同构的权威映射表**(格式同 §3.1,
用通用解析器 `story_tables.py` 统一解析),对应不同 AVG 脚本前缀:

| 体系 | 映射表(.bytes) | 节点 | 标题/脚本字段 | 脚本前缀 |
|---|---|---|---|---|
| 主线剧情 | `story.bytes` | 142 | f6标题 f17脚本 f15前驱 f9战后CG | `stm` / `bam` |
| 角色剧情 | `plot.bytes` | 108 | f3标题 f4简介 **f5脚本** | `cg_<角色ID>_NN` |
| 活动剧情 | `activitystory.bytes` | 91 | f5标题 f7简介 **f10/f20脚本** f17前驱 | `stev` |
| 诺瓦异闻 | `storysetchapter`+`storysetsection` | 16章/50节 | section f5标题 **f7脚本** | `stsp` |

- **角色剧情**(plot):`Plot.<id>` → `CG_103_01`(角色专属故事,如"寻猫记 上"),
  id 前 3 位=角色 ID(103=琥珀…)。
- **活动剧情**(activitystory):`ActivityStory.<id>` → `STev_01_01`,同样带 f17 前驱
  链接构成 graph;标题如"苍茫人海逢故人"。
- **诺瓦异闻**(StorySet):两级结构 —— `storysetchapter`(异闻章节,如
  "#01 刀尖之寒,掌心之暖")下挂 `storysetsection`(小节 → `STsp_01_01` 脚本)。
  即早期归类的"特殊剧情"(stsp)的权威组织形式。

统一合集由 `compile_all_stories.py` 生成到 `story_all/`,全部使用**真实标题**,
共 **142+108+91+50 = 391** 个剧情节点(约 297 个含对话正文)。

---

## 6. 产物清单

| 路径 | 内容 |
|---|---|
| `tmp/REVERSE/story_tables.py` | 通用 .bytes 表解析器(4 类表通用) |
| `tmp/REVERSE/story_map.json` | story.bytes 权威解析 (142 pid → 字段/脚本) |
| `tmp/REVERSE/story_all/0_总目录.md` | 四大体系汇总目录 |
| `tmp/REVERSE/story_all/1_主线剧情.md` | 主线 142 节点(真实标题) |
| `tmp/REVERSE/story_all/2_角色剧情.md` | 角色剧情 108 节点 |
| `tmp/REVERSE/story_all/3_活动剧情.md` | 活动剧情 91 节点 |
| `tmp/REVERSE/story_all/4_诺瓦异闻.md` | 诺瓦异闻 16章/50节 |
| `tmp/REVERSE/story_text/*.txt` | 403 个脚本逐句对话(带说话人+样式) |
| `tmp/REVERSE/avg_decompiled/*.lua` | 403 个反编译后的 AVG 源码 |

---

## 7. 局限与后续

- **story.bytes 仅覆盖主线体系(142 条)**。支线 `stev`/特殊 `stsp`/角色 `cg` 的
  权威映射分别在 `plot.bytes` / `activitystory.bytes` / `charactercg.bytes` 等表,
  格式同 §3,可用同一 `parse_story_table.py` 思路解析(未完成)。
- 27 条 pid 无可提取正文(f15/f17/f9 指向的脚本可能是纯战斗/CG无对白,或脚本名
  在 config 外)。
- **剧情 graph 已确认但未完全重建**:f15 是前驱边,可据此还原完整 DAG(节点+分叉+
  汇聚)。目前索引已标注每节点的前驱;如需可进一步生成 graphviz/流程图。
- AVG 分支(SetChoice)目前按顺序平铺,未重建分支树;如需严格分支流程可进一步
  解析 SetChoiceJumpTo 的 tag/idx 跳转关系。

## 8. 本轮更正与新增(相对早期版本)

1. **f15 语义更正**:从"前置剧情脚本"更正为**graph 前驱链接**(=上一节点 f17),
   经 106/123 实证 + 分叉/汇聚案例确认。合集不再重复输出前驱正文。
2. **`==...==` 标记转换完全逆向**(§2.4):定位 `utils.lua/ProcAvgTextContent` +
   `avg_4_talkctrl.lua`,解出 22 项 SEX 性别词表、PLAYER_NAME、RT换行,以及
   P/B/W/A/Off 演出信号语义;`extract_story.py` 已实装,31215 行 0 残留标记。
3. **说话/心想/旁白区分**(§2.5):逆向 `SetTalk` 的 `nType` 参数(0–11),
   nType=2=心想(Thought)、3/8/10=旁白(Voiceover)、其余=说话(Talk),
   源码级确认 `AvgLogType.Thought/Voiceover/Talk`。
4. **样式化输出**(§2.6):保留控制符并转带样式 HTML(Wait/Break/Paragraph…),
   玩家名/性别词高亮,说话人名用 `avgcharacter.lua` 真实 `name_bg_color` 上色,
   心想台词斜体灰;区分说话/心想/旁白三种渲染。
