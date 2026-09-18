# 星塔旅人 约会系统(Dating)逆向报告

> 版本: iOS 1.9.0 (合并至 v123)
> 数据来源: 反编译 Lua 源码 + `data/bin/*.bytes` 数据表 + `data/language/zh_cn/*.json` 文本
> 反编译产物: `tmp/REVERSE/dating_decompiled/`(已转 UTF-8)

---

## 1. 系统概述

约会(Dating)是手机 UI 内、面向**单个角色**的养成小剧场。玩家为某角色选择一个游玩地点后,会依次经历
「开场 → 分支选择A → 地点剧情 → 分支选择B → 角色限定剧情/结尾」一连串演出事件,过程中累积**好感值**,
结束后可赠送礼物再获得额外好感。

- **前置条件**: 该角色好感等级 ≥ `PhoneDatingAffinityLimit`(配置常量)。
- **每日次数**: 全角色共享上限 `Dating_Max_Daily_Count`,跨天(`IsNewDay`)重置。
- **架构**: 客户端是**纯演出层**;除"地点三选一"是客户端本地随机外,整条剧本(事件序列、
  分支可选项、角色限定剧情、奖励)全部由**服务器下发**。

---

## 2. 代码与数据定位

### 2.1 Lua 控制器(`lua/game/ui/phone/dating/` + `gamecore/data/dataclass/`)

| 文件 | 职责 |
|---|---|
| `phonedatingctrl.lua` | 手机内约会入口面板:好感条、开始按钮、已解锁特殊事件回顾列表 |
| `datinglandmarkctrl.lua` | **选地点面板**(3 张地点卡) |
| `datingctrl.lua` | 约会主控:立绘/气泡/好感数值 Tween/事件流编排 |
| `datingeventctrl.lua` | 事件列表播放器:逐条演出、加速/自动/跳过、时钟进度 |
| `datingeventitemctrl.lua` | 单条对话演出项 |
| `datingeventoptionitemctrl.lua` | **分支选项项**(渲染可选项按钮) |
| `datinggiftctrl.lua` | 结束送礼 |
| `playerdatingdata.lua` | 客户端数据、随机地点、分支 id 计算、网络请求 |

### 2.2 数据表(`data/bin/*.bytes`,文本在 `zh_cn/*.json`)

| 表 | 关键字段 | 用途 |
|---|---|---|
| `DatingLandmark` | `Name`,`Desc`,`Icon`,`Bg` | 地点(洞窟/甜品屋/市场/学院/温泉/港口…) |
| `DatingBranch` | `Landmark`,`Option1..5` | **分支选项文本**,按地点分 A/B 两行 |
| `DatingLandmarkEvent` | `Landmark`,`SortTag`,`Desc1..3`,`Response` | 地点普通剧情事件 |
| `DatingCharacterEvent` | `DatingEventParams=[charId,landmarkId]`,`Desc1..3`,`Name`,`Clue`,`Memory`,`CG`,`Response` | **角色限定特殊剧情** |
| `DatingStartEndEvent` | `DatingEventParams=[charId]`,`Desc1..3`,`Response` | 开场/结尾事件 |
| `DatingCharResponse` | `CharId`,`Type`,`Action`,`VoiceKey`,`BubbleEmoji`,`Words` | 角色针对某情绪 tag 的立绘动作/语音/气泡 |

### 2.3 事件类型枚举 `GameEnum.DatingEventType`

```
Start = 1        -- 开场       (DatingStartEndEvent)
End = 2          -- 结尾       (DatingStartEndEvent)
Landmark = 3     -- 地点剧情   (DatingLandmarkEvent)
Regular = 4      -- 常规       (DatingCharacterEvent)
LimitedLandmark = 5  -- 角色限定特殊剧情 (DatingCharacterEvent)
BranchA = 6      -- 第一次分支 (DatingBranch, id 个位=0)
BranchB = 7      -- 第二次分支 (DatingBranch, id 个位=1)
BeforeBranch = 8 -- 前置分支剧情 (DatingLandmarkEvent)
AfterBranch = 9  -- 后置分支剧情 (DatingLandmarkEvent)
```

---

## 3. 完整流程

```
┌ 手机面板 (phonedatingctrl)
│   好感达标 → OnBtnClick_StartDating → 打开选地点面板
│
├ 选地点面板 (datinglandmarkctrl)
│   GetRandomLandmark(): 客户端本地随机抽 3 个地点
│   点击 → char_dating_landmark_select_req
│   服务器返回: BeforeBranchId / BranchAOptionIds / Change(奖励)
│
└ 约会主控 (datingctrl) —— 拼装事件序列 tbEventId:
    [Start(随机)] → [BeforeBranch] → [BranchA]
                         ↓ 选完 A: char_dating_branch_a_select_req
    服务器返回 LandmarkEventIds(按 SortTag 排序) + BranchB节点 + BranchBOptionIds
                         ↓ 选完 B: char_dating_branch_b_select_req
    服务器返回 CharacterEventId(角色限定) + AfterBranchId + End
    → DatingEventFinish → 送礼(datinggiftctrl) → char_dating_gift_send_req
```

一次约会共 **2 次分支选择**(A、B),由 `datingctrl.lua` 的 `bFirstOption` 标志区分
(`OnEvent_DatingOptionSelected`,`datingctrl.lua:1281`)。

---

## 4. 核心机制详解

### 4.1 地点三选一(客户端随机)

`PlayerDatingData:GetRandomLandmark`(`playerdatingdata.lua:215`):
- 从 `DatingLandmark` 全表用 `math.randomseed(os.time())` 无放回随机抽 3 个;表 ≤3 则全给。
- 卡片若对当前角色存在**未解锁的特殊剧情**(`CheckHasNewEvent`),显示"特殊事件"角标。

### 4.2 分支选项从哪来(回答"3 个选项来源")

约会中的"选项"**不是每次固定 3 个,而是 2 个二选一分支节点**,文本取自 `DatingBranch`:

1. `DatingBranch` 每行含 `Option1..Option5` 五列,按**地点**组织(字段 `Landmark`)。
2. 每地点有 **A/B 两行**,由 **id 个位数**区分:
   `0` → 分支A,`1` → 分支B(`playerdatingdata.lua:457`,`last_digit == nBranchFlag`)。
   例:港口(landmark=8)→ `8000`(A)/`8001`(B)。
3. **具体显示哪几个选项、几个**,由服务器下发的 `BranchAOptionIds` / `BranchBOptionIds`
   (客户端存 `self.tbBranchOptionIds`)决定。客户端遍历该 id 列表,取 `DatingBranch["Option"..n]`,
   **非空才渲染成按钮**(`datingctrl.lua:619` LoadEventConfig)。
   → 所以**选项数量 = 服务器下发的 optId 个数**(通常 2~3 个)。
4. 选项文本中的 `==DATING_CHARACTER==` 会被替换成角色名
   (`datingeventoptionitemctrl.lua:71`)。
5. 玩家点选后发 `char_dating_branch_a/b_select_req { OptionId }`
   (`datingctrl.lua:1399`)。自动播放模式下默认选第 1 项(`SelectDefault`)。

### 4.3 特殊角色剧情如何触发(`DatingCharacterEvent`, type=LimitedLandmark)

这是约会最珍贵的内容(专属 CG + 可回顾"回忆"),触发链:

1. **建索引**: `InitConfig`(`playerdatingdata.lua:59`)预扫全表,凡 `DatingEventType==5` 且
   `DatingEventParams=[charId,landmarkId]`,建成 `mapCharLandmark[charId][landmark]`,
   初始状态 `Lock`,并注册红点。
2. **触发**: 只有当**该角色**在其绑定的**指定地点**约会,服务器才会在第二次分支后下发对应
   `CharacterEventId`。客户端在 `LoadEventConfig` 里校验
   `param[1]==当前角色 且 param[2]==当前地点` → `bSpecial=true`,挂上专属 CG
   (`mapCfg.CG` → `Icon/DatingEventCG/…`)。
3. **解锁与回顾**: `RefreshLimitedEventList` 把状态 `Lock → Unlock`,亮红点;
   之后可在手机面板领奖(`Received`)并查看 `Memory`(回忆文本)。
   未解锁时列表只显示 `Clue`(线索),不剧透标题。

### 4.4 角色情绪演出(`DatingCharResponse`)

每个剧情节点带一个情绪 tag(`Response` 字段,如 `happy/think/shy/normal`)。
`OnEvent_DatingEventAction`(`datingctrl.lua:1003`)用 `_DatingCharResponse[charId][tag]`
查到**该角色**对应的:立绘动作 `Action`、语音 `VoiceKey`、气泡表情 `BubbleEmoji`
(如 `avg_emoji_flower`)、气泡台词 `Words`,并把该事件的 `Affinity` 好感值做 Tween 上涨。
→ 同一个"害羞"在不同角色身上表现不同,即源于此表按 `CharId` 分行。

### 4.5 好感结算

单事件好感 = `Dating_Event_Base_Affinity` + 表内 `Affinity`,仅在该事件**最后一段 Desc**
(`bLast`)结算(`datingeventctrl.lua:391`)。点"跳过"时一次性累加剩余(`OnEvent_DatingEventFinish`)。
约会结束后进入送礼环节,`char_dating_gift_send_req` 提交礼物,服务器回好感升级信息。

---

## 5. 具体示例:与「琥珀」(角色103)在「港口」(地点8)约会

> 该地点对琥珀绑定了特殊剧情 `DatingCharacterEvent 103301`(含专属 CG `DatingSPCG_103301`),
> 故为完整触发一次含特殊剧情的约会范例。以下文本均直接取自数据表(`==DATING_CHARACTER==`
> 运行时替换为"琥珀")。

### ① 开场事件 `DatingStartEndEvent 103101`(type=Start, Response=greet)

> 一时兴起，你用手机向**琥珀**发出了同游的邀请。
>
> 接下来的这段时间，就要和她一起行动了，会发生什么事呢？

### ② 前置分支剧情 + 第一次分支选择 A `DatingBranch 8000`

演出前置剧情(`BeforeBranchId`,地点事件)后,弹出二选一(服务器下发的 `BranchAOptionIds`
对应下列 Option 文本):

- 选项1:`去码头看一看。`
- 选项2:`去展览船上参观。`

### ③ 地点剧情(`DatingLandmarkEvent`,按 `SortTag` 排序播放)

**登场 `801`**(Response=happy):
> 刚刚靠近港口，你就感受到了那股温暖而又潮湿的气息。
>
> 海浪拍打着防波提，你站在下面向上张望。
>
> 你看见了**琥珀**，她面朝着阳光，背后一片蔚蓝，一股风平浪静的安详笼罩着她。

**码头漫步 `802`**(Response=think):
> 你和**琥珀**并肩走在咯吱作响的码头上。
>
> 一些船停靠在码头里，随着海潮摇摇晃晃。
>
> 你不禁遐想到：如果机会合适，自己也会出海吗？

*(中间 803~813 为同地点更多随机片段,略)*

### ④ 第二次分支选择 B `DatingBranch 8001`

- 选项1:`要不要现在来一场夜钓？`
- 选项2:`来一次小舟临海观光。`

### ⑤ 角色限定特殊剧情 `DatingCharacterEvent 103301`(type=LimitedLandmark, Response=shy, CG=DatingSPCG_103301)

> **未解锁前**,列表仅显示线索(`Clue`): *在港口的话，或许会发现些什么……*
>
> **触发正文**(Desc1~3):
>
> 突然，你和琥珀都听到了猫的叫声。
> 琥珀立刻动身，在黑暗中闪转腾挪，很快循着声音发现了一只小猫。
>
> 你惊讶于她神奇的"吸猫体质"，并气喘吁吁的表示，你跟不上她的节奏。
>
> 抱起了猫的琥珀，露出了有些恋恋不舍的表情——她知道，现在的空白旅团，大概没有收养它的条件。
> 于是，你们肆意地享受起了这段安宁的时间。
>
> **标题**(Name): *偶遇猫咪*
> **回忆**(Memory,解锁后可回顾): *和琥珀在港口遇到了被鱼腥味吸引的小猫。虽然没有收养的条件，但你们和小猫在一起度过了一段愉快的时光。*
> **附带**: 专属 CG `DatingSPCG_103301`(`Icon/DatingEventCG/DatingSPCG_103301`)

### ⑥ 后置分支剧情 + 结尾 `DatingStartEndEvent 103102`(type=End, Response=shy)

后置剧情如 `819`(防波堤散步)、`818`(海货特选店)之一后,进入结尾:

> 转眼，时候不早了。
>
> 确实和**琥珀**度过了一段难忘的时光，接下来……

结尾片段 `819`(Response=happy2)示例:
> 你们漫步在防波提上，**琥珀**走在你前面，稍稍张起手臂。
>
> 她一摇一摆的向前走着。树梢被风吹得沙沙作响。她转过来，微微俯下身子。
>
> "今天过得很开心。"昏暗的天光下，你并不能看清她的表情，但想必一定在笑吧。

### ⑦ 送礼结算

结束页可赠送 `AffinityGift` 礼物 → `char_dating_gift_send_req` → 好感升级。

---

## 6. 网络协议一览(客户端仅发请求,剧本由服务器编排)

| 请求 | 触发点 | 服务器返回关键字段 |
|---|---|---|
| `char_dating_landmark_select_req` | 选定地点 | `BeforeBranchId`,`BranchAOptionIds`,`Change` |
| `char_dating_branch_a_select_req` | 选完第一次分支 | `LandmarkEventIds`,`BranchBOptionIds` |
| `char_dating_branch_b_select_req` | 选完第二次分支 | `CharacterEventId`,`AfterBranchId`,`Info`,`Change` |
| `char_dating_event_reward_receive_req` | 手机面板领取特殊事件奖励 | 奖励变更 |
| `char_dating_gift_send_req` | 结束送礼 | 好感升级信息 |

---

## 7. 特殊剧情"时而触发、时而不触发"由谁决定 —— 代码与协议证据

核心问题:同一角色同一地点的特殊剧情,实测有时触发有时不触发,这个"随机性"由谁决定?
结论(基于静态逆向 + 协议定义):**由服务器决定**;客户端既不做本地 gating 也不做本地随机。
以下逐层给出证据,并诚实标注静态逆向的证明边界。

### 7.1 特殊剧情的绑定键是 `[角色, 地点]`,且一一对应

`DatingCharacterEvent`(type=`LimitedLandmark`)在初始化时按 `[charId, landmarkId]` 建索引
(`playerdatingdata.lua:59-113`):

```lua
local function funcForeachCharEvent(mapData)
  if mapData.DatingEventType == GameEnum.DatingEventType.LimitedLandmark then
    local param = decodeJson(mapData.DatingEventParams)
    if mapData.DatingEventParams ~= nil and #mapData.DatingEventParams == 2 then
      local nCharId   = tonumber(mapData.DatingEventParams[1])
      local nLandmark = tonumber(mapData.DatingEventParams[2])
      -- 状态初始 Lock
      local data = { Id = mapData.Id, LandMark = nLandmark,
                     Status = AllEnum.DatingEventStatus.Lock }
      self.mapCharLimitedEvent[nCharId][mapData.Id] = data
      -- 按 [角色][地点] 归档
      if self.mapCharLandmark[nCharId] == nil then self.mapCharLandmark[nCharId] = {} end
      if self.mapCharLandmark[nCharId][nLandmark] == nil then
        self.mapCharLandmark[nCharId][nLandmark] = {}
      end
      table.insert(self.mapCharLandmark[nCharId][nLandmark], mapData.Id)
    end
  end
end
ForEachTableLine(ConfigTable.Get("DatingCharacterEvent"), funcForeachCharEvent)
```

数据实测:全部 **79 个 `LimitedLandmark` 特殊事件 = 79 个不重复的 `(角色, 地点)` 组合**
(无任何一对多)。即一个角色在一个地点最多绑定 1 个特殊剧情——**逻辑上不存在"用选项从多个候选里选出不同特殊剧情"的空间**。

### 7.2 关键决策发生在「选地点面板」,带特殊剧情的地点会打角标

`datinglandmarkctrl.lua:105-129` 在渲染每张地点卡时,调用 `CheckHasNewEvent` 判断该
**角色 + 该地点**是否有未解锁特殊剧情,有则显示"特殊事件"角标:

```lua
-- datinglandmarkctrl.lua
NovaAPI.SetTMPText(txtTag, ConfigTable.GetUIText("Phone_Dating_Special_Event_Title"))
...
local bHasNew = PlayerData.Dating:CheckHasNewEvent(self.nCharId, mapCfg.Id)  -- mapCfg.Id = 地点id
imgTag.gameObject:SetActive(bHasNew)
```

`CheckHasNewEvent` 的判定只看 `角色 + 地点 + Lock 状态`,**完全没有涉及任何选项**
(`playerdatingdata.lua:259-279`):

```lua
function PlayerDatingData:CheckHasNewEvent(nCharId, nLandmark)
  local charData = PlayerData.Char:GetCharDatingEvent(nCharId)
  if charData ~= nil and self.mapCharLimitedEvent[nCharId] ~= nil then
    for nEId, v in pairs(self.mapCharLimitedEvent[nCharId]) do
      if v.LandMark == nLandmark and v.Status == AllEnum.DatingEventStatus.Lock then
        return true      -- 该角色在该地点存在"未解锁"的特殊剧情
      end
    end
  end
  return false
end
```

### 7.3 `CharacterEventId` 由服务器在第二次分支响应里返回;客户端只播不算

选项被点选后仅发送 `char_dating_branch_a/b_select_req`,回调里把服务器返回的
`CharacterEventId`/`AfterBranchId`/`End` 追加进事件队列并刷新好感
(`datingctrl.lua:1281-1403`,节选):

```lua
function DatingCtrl:OnEvent_DatingOptionSelected(nOptionIndex)
  local function callback(_, msgData)
    if self.bFirstOption then                 -- 第一次分支(A)
      ...                                       -- 追加 LandmarkEventIds + 分支B节点
      self.tbBranchOptionIds = msgData.BranchBOptionIds
    else                                        -- 第二次分支(B)
      table.insert(tbNewEvents, { nId = msgData.CharacterEventId,   -- 特殊剧情 id(服务器给)
                                  nType = GameEnum.DatingEventType.LimitedLandmark })
      table.insert(tbNewEvents, { nId = msgData.AfterBranchId, ... })
      PlayerData.Char:ChangeCharAffinityValue(msgData.Info)          -- 好感
    end
    ...
  end
  local nNetMsgId = self.bFirstOption and NetMsgId.Id.char_dating_branch_a_select_req
                                      or  NetMsgId.Id.char_dating_branch_b_select_req
  HttpNetHandler.SendMsg(nNetMsgId, { OptionId = nOptionIndex }, nil, callback)
end
```

**关键:`CharacterEventId` 的值完全由服务器决定,客户端没有任何"角色/地点 → CharacterEventId"的本地映射。**
客户端仅在收到该 id 后,用它去 `DatingCharacterEvent` 表校验是否属于当前 `(角色, 地点)`(用于挂 CG),
但**不参与"给不给/给哪个"的决策**(`datingctrl.lua:673-679`,`LoadEventConfig`):

```lua
if mapEventCfg.DatingEventType == GameEnum.DatingEventType.LimitedLandmark then
  local param = mapEventCfg.DatingEventParams
  if #param == 2 and tonumber(param[1]) == self._panel.nCharId
                 and tonumber(param[2]) == self._panel.nLandmark then
    bSpecial = true   -- 仅校验角色+地点,用于挂专属 CG;非解锁判定
  end
end
```

### 7.4 权威证据:协议字段(proto.pb / FileDescriptorSet)

`gamecore/network/proto.pb` 是完整的 protobuf `FileDescriptorSet`(279 个 file)。用官方
descriptor 解析出约会相关消息的**逐字段定义**如下(这是"客户端到底发了什么、收了什么"的
不可辩驳来源):

```protobuf
// —— 选地点：唯一上报 [角色, 地点] 的地方 ——
message CharDatingLandmarkSelectReq  { uint32 CharId = 1; uint32 LandmarkId = 2; }
message CharDatingLandmarkSelectResp { uint32 BeforeBranchId = 1;
                                       repeated uint32 BranchAOptionIds = 2;
                                       AffinityInfo Info = 7; ChangeInfo Change = 8; }

// —— 第一次分支：请求只带 OptionId ——
message CharDatingBranchASelectReq   { uint32 OptionId = 1; }
message CharDatingBranchASelectResp  { repeated uint32 LandmarkEventIds = 1;
                                       repeated uint32 BranchBOptionIds = 2; }

// —— 第二次分支：请求只带 OptionId；响应才带特殊剧情 CharacterEventId ——
message CharDatingBranchBSelectReq   { uint32 OptionId = 1; }
message CharDatingBranchBSelectResp  { uint32 CharacterEventId = 1;   // ← 特殊剧情
                                       uint32 AfterBranchId  = 2;
                                       AffinityInfo Info = 7; ChangeInfo Change = 8; }
```

由此可**确定的事实**:

1. **客户端上报给服务器的字段全集**只有:选地点时的 `CharId`+`LandmarkId`,以及两次分支的
   `OptionId`。**没有其它隐藏字段**(`NextPackage` 是通用透传占位)。
2. **`CharacterEventId` 只出现在 `CharDatingBranchBSelectResp`** —— 即"是否触发/触发哪个特殊剧情"
   由服务器在**第二次分支的响应**里给出。它与该次请求的 `OptionId` **在同一个请求-响应对内**。
3. 服务器侧至少掌握 `CharId`(选地点时上报,绑定进本次约会 session)、`LandmarkId`、以及两次
   `OptionId`。**因此服务器完全有能力让 `CharacterEventId` 依赖上述任意组合(含 OptionId),也可能是概率抽取。**

### 7.5 关于"时而触发、时而不触发"——诚实的边界

- **纯静态逆向能证明的**:决策发生在**服务器**;客户端不含任何本地 gating 或随机(特殊剧情的
  下发不是客户端 `math.random`,`CharacterEventId` 是收下即播)。绑定关系是 `(角色, 地点) → 唯一事件`,
  所以"触发哪个"确定;但"这一次给不给"是服务器行为。
- **静态逆向无法证明的**(需服务器代码或抓包):服务器判定"这次给不给 `CharacterEventId`"用的是
  概率、每日/终身次数上限、好感门槛,**还是**与第二次分支的 `OptionId` 相关。协议允许以上任何一种。
- **可证伪的下一步**:抓 `CharDatingBranchBSelectReq/Resp` 明文即可判定——
  - 若**固定选同一 OptionId、同角色同地点**,`CharacterEventId` 时有时无 → 概率/次数,与选项无关;
  - 若**只有某个 OptionId** 才返回非零 `CharacterEventId` → 与选项相关。

  仅凭客户端代码,**无法排除后者**,故不能断言"选项一定无关"。

---

## 8. 关键结论

1. **"选项"本质是 2 个二选一分支**,文本来自 `DatingBranch.Option1~5`(按地点分 A/B 行,id 个位 0/1);
   **实际显示项由服务器下发的 `BranchAOptionIds/BranchBOptionIds` 决定**,客户端仅取文本渲染。
2. **特殊角色剧情**(`DatingCharacterEvent`, type=5)与 `[角色id, 地点id]` 一一配对(79 组=79 事件),
   决定"触发哪个";但**"这一次给不给"由服务器在第二次分支响应 `CharDatingBranchBSelectResp.CharacterEventId`
   里决定**,客户端无本地 gating/随机。客户端上报字段仅 `CharId`+`LandmarkId`(选地点)与两次 `OptionId`;
   服务器据此(可能含概率/次数/好感/OptionId)决定是否返回非零 `CharacterEventId`。
   **静态逆向不能断言"与选项无关",需抓包验证**(见 §7.4/§7.5)。
3. **地点为客户端本地随机 3 选 1**;其余剧本节点、好感、奖励全部服务器编排,客户端是演出层。
4. **同一情绪的不同角色表现**由 `DatingCharResponse` 按 `CharId` 分行提供(动作/语音/气泡)。
