# 星塔探索 (Star Tower) 系统完整逆向报告

> 数据来源: 反编译 Lua 源码 (79/79 成功) + `data/bin/*.bytes` 数据表 + `data/language/zh_cn/*.json` 文本
> 反编译产物: `tmp/REVERSE/startower_decompiled/` (79个文件, 全部反编译成功)
> 核心代码文件: `startowerleveldata.lua`(6718行), `baseroom.lua`(1363行), `battleroom.lua`(236行), `eventroom.lua`(40行)

---

## 1. 系统概述

星塔探索是 roguelike 爬塔模式。玩家选择一座星塔(有 GroupId/Difficulty)、3 名角色 + 碟片(Disc)编队后进入。
每层为一个"房间"(Room), 房间类型由该塔的 `StarTowerStage` 逐层预先配置。玩家依次完成每层战斗/事件/商店,
通过"传送门"进入下一层, 全程无法跳过。通关最终层或战败即结束。

**核心参与方**:
- **服务器**: 房间数据下发(随机地图 seed、Case 列表)、战斗结算、选项判定、商品随机; 不参与客户端 move-to-room 选择
- **客户端 C# (AdventureModuleHelper)**: 实时战斗引擎、地图随机 (RandomStarTowerMap)、NPC 生成、技能/属性管理
- **客户端 Lua**: 房间 UI 编排、事件选项处理、商店购买、强化/选择面板、结算展示

---

## 2. 完整流程图

```
  [主页] ──打开星塔入口──▶ StartowerMenuCtrl (选塔/选编队/选潜能预设)
                                    │
                    star_tower_apply_req {Id, FormationId, CharHp, MapId, ParamId, MapParam}
                                    │
                                    ▼
                    PlayerStarTowerData:EnterTower()
                      └─ StarTowerLevelData.new(nTowerId)    ← 加载 Stage 序列
                      └─ CS.RandomStarTowerMap(stRoomMeta)   ← C# 随机地图 seed
                      └─ HTTP → 服务器返回 Meta + Room + Bag
                                    │
                                    ▼
                    StarTowerLevelData:Init(meta, room, bag)
                      └─ BuildCharacterData()       ← 角色属性/装备/天赋计算
                      └─ CalCharFixedEffect()       ← 不动效果
                      └─ GetCharacterAttr()         ← 战斗中属性
                      └─ EnterStarTowerMap()        ← C# 加载地图
                      └─ GetcurRoom() → room.new()  ← 创建房间控制器
                                    │
              ┌─────────────────────┴────────────── 主循环 ──────────────────────┐
              │                                                                   │
              ▼                                                                   │
    ┌── Room:Enter() [base: baseroom.lua]                                         │
    │    └─ SaveCase(tbCases)  ← 解析服务器下发的 Case 列表                       │
    │    └─ HandleCases()      ← 按优先级处理各类 Case                            │
    │                                                                             │
    │    Case 类型 (由 proto 的 oneof room_case 决定):                            │
    │    ┌─────────────────────────────────────────────────────────────────┐     │
    │    │ 1. BattleCase        → BattleRoom:LevelStart()                   │     │
    │    │ 2. DoorCase          → 传送门/危险门/惨剧门                      │     │
    │    │ 3. SelectPotential   → 潜能三选一 (含 reroll)                    │     │
    │    │ 4. FateCardSelect    → 秘闻卡选择 (含 reroll)                    │     │
    │    │ 5. NoteSelect        → 音符选择                                  │     │
    │    │ 6. OptionsEventCase  → NPC 事件 (多选项、成功/失败判定)           │     │
    │    │ 7. SpecialPotential  → 特殊潜能选择                               │     │
    │    │ 8. RecoveryHP        → 免费回血                                  │     │
    │    │ 9. NpcRecoveryHP     → NPC 回血                                  │     │
    │    │10. HawkerCase        → 商店 (购买 + reroll)                      │     │
    │    │11. StrengthenMachine  → 强化机 (消耗货币升级随机潜能)              │     │
    │    │12. DoorDanger        → 危险门 (可选额外挑战)                      │     │
    │    │13. SyncHP            → 服务器同步血量                             │     │
    │    └─────────────────────────────────────────────────────────────────┘     │
    │                                                                             │
    │    全部 Case 完成后 → 传送门激活                                            │
    │         ├─ EventRoom:LevelStateChanged(Teleporter)                          │
    │         └─ BattleRoom:LevelStateChanged(Teleporter)                         │
    │              └─ EnterRoom(nCaseId, nRoomType)                               │
    │                   └─ nCurLevel++                                            │
    │                   └─ CS.RandomStarTowerMap(stRoomMeta) ← C# 随机新地图      │
    │                   └─ HTTP star_tower_interact_req {Id, EnterReq{MapId,...}} │
    │                   └─ 服务器返回新 Room Cases                                │
    │                   └─ 新 Room.new() → 进入主循环                             │
    │                                                                             │
    │    如果 nCurLevel > #tbStarTowerAllLevel:                                    │
    │         └─ StarTowerClear(nCaseId)  ← 通关                                  │
    │                                                                             │
    │    如果战斗失败:                                                              │
    │         └─ StarTowerFailed() → 结算面板 (失败)                               │
    └─────────────────────────────────────────────────────────────────────────────┘

  [结算] StarTowerResultCtrl
      ├─ 成功: 通关层数、潜能数量、时间、NPC 好感 → 奖励 → Build 保存
      └─ 失败: 中途放弃结算、保留已获得奖励
```

---

## 3. 入口: 选塔 → 选角色 → 开打

### 3.1 数据结构

```
star_tower_apply_req {
  Id          uint32   # 星塔Id (如102=流水与暗影)
  FormationId uint32   # 编队编号
  CharHp      int32    # 初始血量(-1=满血)
  MapId       uint32   # 地图Id(客户端用C# RandomStarTowerMap 生成初始seed)
  ParamId     uint32   # 楼层参数
  MapParam    string   # 额外地图参数
  MapTableId  uint32   # 场景 Prefab Id
  Sweep       bool     # 是否扫荡模式
}
```

### 3.2 入口逻辑 (playerstartowerdata.lua:46-90)

```lua
function PlayerStarTowerData:EnterTower(nTowerId, nTeamIdx, tbDisc)
  -- 1. 创建 LevelData 对象, 加载该塔的所有 Stage 序列
  self.LevelData = luaClass.new(self, nTowerId)
  local nStageId = self.LevelData:GetStageId(1)

  -- 2. 获取编队角色
  local tbTeam = PlayerData.Team:GetTeamCharId(nTeamIdx)
  local tbCharSkinId = {...}

  -- 3. C# 生成初始地图 seed (随机)
  local curMapId, nFloorId, sExdata, scenePrefabId =
    CS.AdventureModuleHelper.RandomStarTowerMap(stRoomMeta)

  -- 4. 发送申请请求
  HttpNetHandler.SendMsg(NetMsgId.Id.star_tower_apply_req, {
    Id = nTowerId, FormationId = nTeamIdx, CharHp = -1,
    MapId = curMapId, ParamId = nFloorId,
    MapParam = sExdata, MapTableId = scenePrefabId
  }, nil, applyCallback)

  -- 5. 回调中初始化
  function applyCallback(_, mapMsgData)
    self.LevelData:Init(mapMsgData.Info.Meta, mapMsgData.Info.Room,
                        mapMsgData.Info.Bag, mapMsgData.LastId)
  end
end
```

### 3.3 Stage 序列构建 (startowerleveldata.lua:165-216)

```lua
function BuildStarTowerAllFloorData(nTowerId)
  local mapStarTowerCfgData = ConfigTable.GetData("StarTower", nTowerId)
  local tbStage = mapStarTowerCfgData.StageGroupIds   -- 阶段组id列表
  local tbFloorNum = mapStarTowerCfgData.FloorNum      -- 每阶段层数
  for nIdx, nStageGroupId in ipairs(tbStage) do
    local nFloorNum = tbFloorNum[nIdx] or 99
    for nLevel = 1, nFloorNum do
      local nStageLevelId = nStageGroupId * 100 + nLevel  -- 如 101*100+1=10101
      local stageCfg = ConfigTable.GetData("StarTowerStage", nStageLevelId)
      if stageCfg == nil then break end
      table.insert(ret, stageCfg)   -- stageCfg.RoomType 决定房间类型
    end
  end
  return ret, difficulty, levelDifficulty
end
```

**数据表 `StarTower`**: GroupId, Difficulty, Name, StageGroupIds, FloorNum, SubNoteSkillDropGroupId, ShopNpc, UpgradeNpc, DangerNpc, HorrorNpc, ResqueNpc

**数据表 `StarTowerStage`**: RoomType (决定该层是什么房间)

---

## 4. 房间引擎 (BaseRoom): 核心编排逻辑

### 4.1 Case 类型枚举

| EnumCase # | 名称 | 含义 |
|---|---|---|
| 1 | Battle | 战斗房间 |
| 2 | OpenDoor | 去往下一层的传送门 |
| 3 | PotentialSelect | 潜能三选一 |
| 4 | FateCardSelect | 秘闻卡选择 |
| 5 | NoteSelect | 音符选择 |
| 6 | NpcEvent | NPC 事件 (带选项) |
| 7 | SelectSpecialPotential | 特殊潜能选择 |
| 8 | RecoveryHP | 自由回血点 |
| 9 | NpcRecoveryHP | NPC 回血 (贝缇丽) |
| 10 | Hawker | 商店 (波西亚) |
| 11 | StrengthenMachine | 强化机 (升级随机潜能) |
| 12 | DoorDanger | 危险门 (NPC提示可选挑战) |
| 13 | SyncHP | 服务器同步血量 |

### 4.2 Case 保存逻辑 (baseroom.lua:184-353): 解析服务器 protobuf oneof

```lua
function BaseRoom:SaveCase(tbCases)
  for _, mapCaseData in ipairs(tbCases) do
    if mapCaseData.BattleCase ~= nil then
      self.mapCases[self.EnumCase.Battle] = {
        Id = mapCaseData.Id,
        Data = mapCaseData.BattleCase,   -- {TimeLimit, FateCard}
        bFinish = false
      }
    elseif mapCaseData.DoorCase ~= nil then
      if mapCaseData.DoorCase.Type == GameEnum.starTowerRoomType.DangerRoom then
        -- 危险门: 生成 Danger Npc, NPC可交互进入挑战
        self.mapNpc[nNpcId] = mapCaseData.Id
        CS.AdventureModuleHelper.SpawnNPC(nNpcId, nSkinId)
        self.mapCases[self.EnumCase.DoorDanger][mapCaseData.Id] = mapCaseData.DoorCase
      elseif mapCaseData.DoorCase.Type == GameEnum.starTowerRoomType.HorrorRoom then
        -- 惨剧门: 同上, 用 HorrorNpc
      else
        -- 普通传送门: 进入传送门 → EnterRoom → 下一层
        self.mapCases[self.EnumCase.OpenDoor] = {mapCaseData.Id, mapCaseData.DoorCase.Type}
      end

    elseif mapCaseData.SelectOptionsEventCase ~= nil then
      -- NPC 事件: 生成 NPC, 加载选项数据
      local nActionId = mapCaseData.SelectOptionsEventCase.EvtId * 10000 + nNpcId
      -- ... spawn NPC, save case with bFinish and affinity info

    elseif mapCaseData.HawkerCase ~= nil then
      -- 商店: 根据房型选 ShopNpc 或 StandShopNpc
      self.mapCases[self.EnumCase.Hawker][mapCaseData.Id] = mapCaseData.HawkerCase
      CS.AdventureModuleHelper.SpawnNPC(nNpcId, nSkinId)

    elseif mapCaseData.StrengthenMachineCase ~= nil then
      -- 强化机: 生成升级 NPC
      self.mapCases[self.EnumCase.StrengthenMachine][mapCaseData.Id] = ...
    -- ... 其他 Case 类似
    end
  end
end
```

### 4.3 Case 处理优先级 (baseroom.lua:438-545)

`HandleCases()` 按固定优先级逐一处理未完成的 Case:

```
1. Popup 弹窗 (强化特效)
2. Popup 弹窗 (潜能升级)
3. Popup 弹窗 (奖励展示)
4. RecoveryHP  (自动回血)
5. SelectSpecialPotential (特殊潜能选择)
6. PotentialSelect  (潜能三选一)
7. NoteSelect  (音符选择)
8. FateCardSelect  (秘闻卡选择)
9. Popup 弹窗 (碟片技能)
10. Popup 弹窗 (NPC好感变更)
11. 全部完成 → blockNpcBtn = false (解锁NPC交互)
```

---

## 5. 战斗房间 (BattleRoom)

### 5.1 开始战斗 (battleroom.lua:13-44)

```lua
function BattleRoom:LevelStart()
  if mapBattleCase == nil then
    -- 无战斗事件: 立即结束
    self.bBattleEnd = true
    -- 显示房间信息面板
    return
  end
  -- 设置成就追踪类型
  PlayerData.Achievement:SetSpecialBattleAchievement(GameEnum.levelType.StarTower)

  -- 如果有限时条件, 开启 Boss 倒计时
  if mapBattleCase.Data.TimeLimit then
    EventManager.Hit("OpenBossTime", nStage, nType)
  end

  -- Boss/FinalBoss 房间: 开启排位计时器
  if nType == GameEnum.starTowerRoomType.BossRoom
     or nType == GameEnum.starTowerRoomType.FinalBossRoom then
    EventManager.Hit("StartClientRankTimer")
  end
end
```

### 5.2 战斗胜利 (battleroom.lua:76-175)

战斗由 C# 引擎执行。当 C# 触发 `LevelStateChanged(Success)`:

```lua
-- 构造 BattleEndReq.Victory
msg.BattleEndReq.Victory = {
  HP = nHp,                  -- 主控角色剩余血量
  Time = self.nTime,          -- 战斗用时(秒)
  ClientData = clientData,    -- 压缩的角色状态数据(技能CD/buff/效果)
  DateLen = nDataLength,
  fateCardUsage = tbUsage,    -- 秘闻卡使用次数
  Damages = tbDamage,         -- 伤害记录
  Sample = tbSamples,         -- 伤害采样
  Events = {List = tbEvent}   -- 成就事件
}

self.parent:StarTowerInteract(msg, callback)
  → HTTP star_tower_interact_req {Id, BattleEndReq}
  → 服务器返回: Change (货币/道具变化), BattleEndResp.Victory (升级经验)
```

### 5.3 战斗失败 (battleroom.lua:191-233)

```lua
function BattleRoom:OnEvent_ActorFinishDie()
  if self.bBattleEnd then
    EventManager.Hit("AbandonStarTower")
  else
    msg.BattleEndReq.Defeat = true
    -- 非序章时弹出重试/放弃确认框
    -- 确认放弃 → StarTowerInteract(msg)
    -- 服务器返回 Settle {Change, Build, TotalTime, Reward, TowerRewards}
    -- → StarTowerFailed() → 结算面板(失败)
  end
end
```

---

## 6. 事件房间 (EventRoom): NPC 交互

### 6.1 事件类型与选项

事件数据表 `StarTowerEvent`:
| 字段 | 说明 |
|---|---|
| f1=Id | 事件Id (101~...) |
| f2 | 事件组(如 101=序章) |
| f3=Name | 事件名 ("交易-潜能", "获取辉光币", "赌辉光币", "获取潜能") |
| f4=Type | 4=随机选项事件 |
| f5 | NPC参数 |

事件选项表 `StarTowerEventOptionAction`:
每个 (事件id × 10000 + NPCid) 对应一个 actionEntry, 包含事件文本(语言表 key)和 NPC。

### 6.2 选项处理 (baseroom.lua:810-946)

```lua
function BaseRoom:OpenNpcOptionPanel(nCaseId, nNpcConfigId)
  local mapCase = self.mapCases[EnumCase.NpcEvent][nCaseId]

  if mapCase.bFinish then
    -- 已完成: 显示对话(根据好感度选随机台词)
    local tbChat = filter_by_affinity(npc.Lines, mapCase.Infos)
    nTalkId = tbChat[math.random(1, #tbChat)]
    -- 打开对话面板...
    return
  end

  -- 未完成: 展示选项按钮
  local tbOption = mapCase.Options    -- 选项 Id 列表
  local tbUnabledOption = mapCase.FailedIdxes  -- 失败的选项索引

  function callback(nIdx, nEvtId)
    -- 玩家选择选项 nIdx → 发送到服务器
    msg.SelectReq.Index = nIdx - 1

    local function InteractiveCallback(callbackMsg, ...)
      local bSuccess = callbackMsg.SelectResp.Resp.OptionsResult

      if bSuccess then
        -- 成功: 标记 case 完成, 更新 NPC 好感
        mapCase.bFinish = true
        -- 处理好感变更
        for _, mapChange in ipairs(callbackMsg.SelectResp.Resp.AffinityChange) do
          -- 记录好感增减显示
        end
        -- 处理奖励变化 (音符/道具/潜能/秘闻卡)
        EventManager.Hit("StarTowerEventInteract", ...)
      else
        -- 失败: 提示文本, 记录失败索引(该选项变灰色不可再选)
        EventManager.Hit(EventId.OpenMessageBox,
                         ConfigTable.GetUIText("Startower_EventFailHint"))
        table.insert(mapCase.FailedIdxes, nIdx - 1)
      end

      -- 如果有自定义结果文本 (OptionsParamId → EventResult_xxx)
      if callbackMsg.SelectResp.Resp.OptionsParamId ~= 0 then
        EventManager.Hit(EventId.OpenMessageBox,
                         ConfigTable.GetUIText("EventResult_" .. OptionsParamId))
      end
    end

    self.parent:StarTowerInteract(msg, InteractiveCallback)
  end
end
```

**关键逻辑:**
- **选项由服务器下发**: `mapCase.Options` 是服务器给出的可选项 Id 列表
- **成功/失败由服务器判定**: `SelectResp.Resp.OptionsResult = true/false`
- **失败选项变灰**: `FailedIdxes` 记录, 不可再选
- **好感变化**: 成功时 `AffinityChange` 列表返回各 NPC 好感增减

---

## 7. 商店系统

### 7.1 商品数据

商店 Case (HawkerCase) 由服务器下发, 结构:
```
HawkerCase {
  List: [ {Idx, Sid, Price, Discount, CharPos, Type, GoodsId} ]  -- 商品列表
  Purchase: [Sid]     -- 已购买商品 Sid 列表
  CanReRoll: bool     -- 是否可刷新
  ReRollPrice: int    -- 刷新价格
  ReRollTimes: int    -- 剩余刷新次数
}
```

### 7.2 购买流程 (baseroom.lua:1100-1175)

```lua
function BaseRoom:InteractiveShop(nCaseId, nNpcConfigId)
  local mapCase = self.mapCases[EnumCase.Hawker][nCaseId]

  -- 构建商品展示数据
  local tbShopData = {}
  for index, mapGood in ipairs(mapCase.List) do
    tbShopData[index] = {
      Idx = mapGood.Idx,
      bSoldOut = table.indexof(mapCase.Purchase, mapGood.Sid) > 0,
      Price = mapGood.Price,
      nDiscount = mapGood.Discount,   -- 折扣值(>0表示打折)
      nCharId = 0 < mapGood.CharPos and self.parent.tbTeam[mapGood.CharPos] or 0,
      nSid = mapGood.Sid,
      nType = mapGood.Type,           -- 商品类型(1=常规,2=音符等)
      nGoodsId = mapGood.GoodsId
    }
  end

  -- 构建 ReRoll 数据
  local mapRoll = {
    CanReRoll = mapCase.CanReRoll,
    ReRollPrice = mapCase.ReRollPrice,
    ReRollTimes = mapCase.ReRollTimes
  }

  -- 打开商店面板
  EventManager.Hit(EventId.OpenPanel, PanelId.StarTowerShop, tbShopData,
                   nCoin, BuyCallback, nCaseId, mapRoll, ...)
end
```

### 7.3 购买/刷新回调

```lua
-- 购买
function BuyCallback(nEvtId, nSid, callback, bReRoll)
  if bReRoll then   -- 刷新
    msg.HawkerReq.ReRoll = true
  else              -- 购买
    msg.HawkerReq.Sid = nSid
  end

  self.parent:StarTowerInteract(msg, InteractiveCallback)
  -- 服务器返回后:
  --   购买: 标记 SoldOut, 扣货币
  --   刷新: 更新 List, 扣刷新费
end
```

### 7.4 商品排序 (商店 UI, startowershopctrl.lua:388-408)

```lua
function StarTowerShopCtrl:SortGoods(tbGoodsList)
  local tbTypeSort = {[1]=1, [2]=2, [3]=4, [4]=3}  -- 类型优先级
  table.sort(tbGoodsList, function(a, b)
    if tbTypeSort[a.nType] ~= tbTypeSort[b.nType] then
      return tbTypeSort[a.nType] < tbTypeSort[b.nType]  -- 按类型排序
    elseif a.nDiscount ~= b.nDiscount then
      return a.nDiscount > b.nDiscount                   -- 同类型: 折扣大的在前
    else
      return a.nSid < b.nSid                             -- 同折扣: 按 Sid
    end
  end)
end
```

**商品随机由服务器端完成** —— 客户端仅负责展示和排序。

---

## 8. 强化机 (StrengthenMachine)

消耗星塔货币(辉光币)随机升级一个已持有的潜能。

### 8.1 费用计算 (baseroom.lua:1177-1237)

```lua
function BaseRoom:InteractiveStrengthMachine(nCaseId, nNpcConfigId)
  local mapCase = self.mapCases[EnumCase.StrengthenMachine][nCaseId]
  local nDiscount = mapCase.Discount    -- 本次折扣
  local bFirstFree = mapCase.FirstFree  -- 首次免费

  -- 费用: 查 StarTowerStrengthMachineCost[使用次数+1]
  local nCost = self.parent.tbStrengthMachineCost[mapCase.Times + 1]
                or self.parent.tbStrengthMachineCost[#self.parent.tbStrengthMachineCost]
  nCost = nCost - nDiscount
  if bFirstFree then nCost = 0 end

  if nCoin < nCost then
    -- 货币不足, 无法使用
    EventManager.Hit(EventId.OpenMessageBox, "StarTower_NotEnoughCoin")
    return
  end

  -- 发送到服务器 (无额外参数, 服务器随机选一个潜能升级)
  self.parent:StarTowerInteract({Id = nCaseId}, InteractiveCallback)

  -- 回调中:
  --   成功: Times++, 播放强化特效, 显示升级结果
  --   失败: "没有可选的潜能" 提示
end
```

**费用表**: `tbStrengthMachineCost = ConfigTable.GetConfigNumberArray("StrengthenMachineGoldConsume")`

**强化升级哪个潜能**: 由**服务器随机决定** (客户端仅发送 `star_tower_interact_req {Id}`)。

---

## 9. 潜能/秘闻卡/音符选择

### 9.1 潜能选择 (PotentialSelect, baseroom.lua:547-681)

```lua
-- 服务器给出的选择数据 (proto: SelectPotentialCase)
{
  Infos: [{Tid, Level}],      -- 可选潜能列表 (通常3个)
  CanReRoll: bool,            -- 可重抽
  ReRollPrice: int,           -- 重抽价格
  NewIds: [int],              -- 新潜能 Id
  LuckyIds: [int],            -- 幸运出现
  Type: int,                  -- 0=普通, 1=队伍等级关联
  TeamLevel: int              -- 触发队伍等级
}

-- 玩家选择(或 ReRoll) → star_tower_interact_req {Id, SelectReq {Index | ReRoll}}
-- 服务器返回: 新的 Case 状态(如 bReRoll=false/bFinish=true)
```

### 9.2 秘闻卡选择 (FateCardSelect, baseroom.lua:739-808)

```lua
-- proto: SelectFateCardCase
{
  Ids: [int],          -- 可选秘闻卡 Id 列表 (通常3张)
  NewIds: [int],       -- 新获得的 Id
  Give: bool,          -- 是否白送
  CanReRoll: bool,
  ReRollPrice: int
}

-- 选择 Index → 服务器返回 FateCardInfo 变化
-- 秘闻卡有 Room 持续回合和 Remain 剩余次数
-- 使用中的秘闻卡通过 FateCardEft 添加战斗效果
```

### 9.3 音符选择 (NoteSelect, baseroom.lua:683-737)

```lua
-- proto: SelectNoteCase
{
  Info: [{...}]  -- 可选音符信息
}

-- 选择后 → _mapNote 更新, 影响碟片技能激活
```

---

## 10. 结算系统

### 10.1 通关结算 (startowerleveldata.lua:393-580)

```lua
function StarTowerLevelData:StarTowerClear(nCaseId)
  -- 发送最终交互请求
  HttpNetHandler.SendMsg(NetMsgId.Id.star_tower_interact_req, {
    Id = nCaseId,
    EnterReq = {MapId = 0, Checksum = nCheckSum}
  }, nil, NetCallback)
```

**服务器返回 `star_tower_interact_resp.Settle`**:
```
Settle {
  Build: {Brief, BuildCoin}      -- 构筑数据
  Change: ChangeInfo              -- 货币/道具变化
  TotalTime: uint32               -- 总耗时(秒)
  Reward: [{Change: {NPCId, Affinity, Increase}, Items}]  -- NPC好感奖励
  Awards: [{Items: [{Tid, Qty}]}] -- 首通奖励
  TowerRewards: [{Tid, Qty}]      -- 通关奖励
  NpcInteraction: int             -- NPC 交互次数
}
```

### 10.2 结算面板 (startowerresultctrl.lua:94-228)

```lua
function StarTowerResultCtrl:Refresh(teamMemberid, mapResult)
  -- 难度名称: "「流水与暗影」难度1"
  local sName = "「" .. Name .. "」难度" .. Difficulty

  -- 通关层数: "第X层"
  local sProcess = "第" .. curFloor .. "层"

  -- 潜能数量
  self:SetPerkCount(tostring(perkCount))

  -- 耗时: nTime 秒

  -- NPC 好感 Level-Up 判定 (比较结算前后好感等级)
  for _, mapReward in ipairs(tbAffinity) do
    if curLevel ~= beforeLevel then
      -- 触发好感升级弹窗
      table.insert(self.tbNpcAffinity, {NPCId, Level, Items})
    end
  end

  -- 奖励展示: FixedRoguelikeRewardGachaCtrl (抽卡式奖励动画)
end
```

### 10.3 结算后流程

1. **好感升级弹窗** (如果有 NPC 好感提升)
2. **奖励展示** (抽卡式动画)
3. **Build 保存弹窗** (保存本次构筑编队, 含构筑积分)
4. **返回主界面** (EnterModule "MainMenuModuleScene")

### 10.4 扫荡模式 (Sweep)

如果玩家激活了扫荡 Growth Node:
- `star_tower_apply_req {Sweep=true}` → 服务器一次性结算所有奖励
- 跳过所有房间流程, 直接展示结算面板

---

## 11. 关键数据表一览

| 数据表 | 用途 |
|---|---|
| `StarTower` | 星塔定义: GroupId, Difficulty, Name, StageGroupIds, FloorNum, ShopNpc/UpgradeNpc 等 |
| `StarTowerStage` | 每层配置: RoomType (Battle/Shop/Event 等) |
| `StarTowerEvent` | 事件定义: Name → Type → 参数 |
| `StarTowerEventAction` | 事件 action: (EventId*10000+NPCId) → 文本 key |
| `StarTowerEventOptionAction` | 选项 action: (EventOptionId*10000+NPCId) → 文本 |
| `StarTowerShopGoods` | 商品配置: f1=Idx, f2=GoodsId, f3=ShowItem |
| `StarTowerMap` | 地图配置: Theme, OutPortHint |
| `StarTowerFloorExp` | 楼层经验: StarTowerId × Stage → Exp |
| `StarTowerBuild` | 构筑配置 |
| `StarTowerGrowthNode` | Grownh 养成节点: EffectClient, ClientParams |
| `StarTowerGrowthGroup` | Grownh 养成组: PreGroup, WorldClass |
| `StarTowerNPC` | 星塔 NPC: 波西亚/贝缇丽等 |
| `NPCAffinityGroup` | NPC 好感等级: AffinityValue → Level |
| `NPCAffinityPlot` | NPC 好感剧情: NPCId × AffinityLevel → PlotId |
| `StarTowerTalk` | NPC 随机台词: Affinity 区间筛选 |
| `StarTowerLimitReward` | 极限奖励: StarTowerId × Stage × RoomType |
| `StarTowerTeamExp` | 队伍等级经验: GroupId × Level |
| `SubNoteSkillDropGroup` | 音符掉落组: GroupId |

---

## 12. 网络协议

核心消息:
- `star_tower_apply_req/ack` — 进入星塔
- `star_tower_interact_req/ack` — 所有房间操作 (开门/战斗结算/选潜能/选秘闻卡/购买/强化/事件选项)
- `star_tower_give_up_req/ack` — 放弃/暂停离开
- `star_tower_info_req/ack` — 重连/恢复
- `tower_growth_detail_req/ack` — Grownh 养成数据
- `tower_growth_node_unlock_req/ack` — 解锁养成节点

### interact_req 统一格式

```protobuf
// star_tower_interact_req {uint32 Id, oneof: EnterReq|SelectReq|BattleEndReq|HawkerReq|RecoveryHPReq|StrengthenMachineReq|...}
message StarTowerInteractReq {
  uint32 Id = 1;
  StarTowerEnterReq     EnterReq = 2;
  StarTowerSelectReq    SelectReq = 3;
  StarTowerBattleEndReq BattleEndReq = 4;
  HawkerReq             HawkerReq = 5;
  RecoveryHpReq         RecoveryHPReq = 6;
  // ... 其他请求类型
}
```

---

## 13. 弹窗 Popup 系统

BaseRoom 维护一个弹窗队列 `tbPopup`, 保证多个奖励/特效弹出顺序播放:

```lua
self.EnumPopup = {
  Reward      = 1,   -- 战斗奖励弹窗
  Potential   = 2,   -- 潜能升级弹窗
  StrengthFx  = 3,   -- 强化特效弹窗
  Disc        = 4,   -- 碟片技能弹窗
  Affinity    = 5,   -- NPC好感变更弹窗
}
```

战斗胜利后按顺序: Reward → Potential → Disc → Affinity → 继续 HandleCases

---

## 14. 地图随机 (C# 侧)

```csharp
// CS.AdventureModuleHelper.RandomStarTowerMap
(int curMapId, int floorId, string sExdata, int scenePrefabId)
= RandomStarTowerMap(Lua2CSharpInfo_FixedRoguelike stRoomMeta)
```

客户端 C# 根据:
- `nTowerId` (星塔 Id)
- `nStage` (当前阶段)
- `tbHistoryMapId` (已出现地图历史, 避免重复)
- `tbTeam/TbCharSkinId` (队伍)
- `nDangerRoom` (是否危险房间)
- `bRanking` (排位模式)
- `nMapTableId` (重连恢复的场景 Id)

计算出下一层的地图(3D 场景)。

---

## 15. 代码索引

| 文件 | 行数 | 职责 |
|---|---|---|
| `playerstartowerdata.lua` | 1685+ | 网络请求、状态缓存、Grownh系统、NPC好感 |
| `startowerleveldata.lua` | 6718+ | 关卡逻辑: Init/EnterRoom/StarTowerClear/StarTowerFailed/属性计算/效果管理 |
| `baseroom.lua` | 1363+ | 房间引擎: Case管理、事件处理、选择回调、商店/强化机交互 |
| `battleroom.lua` | 236 | 战斗房间: 胜利/失败结算、重试逻辑 |
| `eventroom.lua` | 40 | 事件房间: 继承 BaseRoom, NPC 交互 |
| `startowershopctrl.lua` | 825 | 商店 UI: 商品展示、购买、刷新、排序 |
| `startowerresultctrl.lua` | 414 | 结算 UI: 通关/失败展示、奖励、好感升级 |
| `startowermenuctrl.lua` | 240 | 局内菜单: 骰币/编队/地图按钮 |
| `startowermapctrl.lua` | ~ | 楼层地图: 各层预览 |
| `potentialselectctrl.lua` | ~ | 潜能选择 UI |
| `fatecardselectctrl.lua` | ~ | 秘闻卡选择 UI |
| `noteselectctrl.lua` | ~ | 音符选择 UI |
| `startowerdepotctrl.lua` | ~ | 背包/仓库 UI |

---

## 16. 总结：客户端随机 vs 服务器决策

| 随机内容 | 决定方 |
|---|---|
| 初始地图 seed | **客户端 C#** (RandomStarTowerMap) |
| 每层进入新地图 seed | **客户端 C#** (RandomStarTowerMap) |
| 房间 Case 内容 (战斗类型/事件选项/商店商品/潜能列表/秘闻卡) | **服务器** |
| 事件选项成功/失败 | **服务器** |
| 战斗胜负 | C# 战斗引擎执行, 结果上报服务器 |
| 商店商品列表 | **服务器** (HawkerCase.List) |
| 强化机升级哪个潜能 | **服务器** (随机) |
| Shop ReRoll 后的新商品 | **服务器** (重新生成 HawkerCase) |
| 潜能/秘闻卡 ReRoll 后的新选项 | **服务器** (重新生成 SelectCase) |
| NPC 随机台词 | **客户端** (根据好感区间从 Lines 中随机) |
| 结算奖励 (首通/通关/好感) | **服务器** (Settle 数据) |
| 构筑积分 (BuildScore) | **客户端** (CalBuildScore) |

核心结论: **除地图场景和 NPC 台词外, 所有游戏性内容(关卡、事件判定、商品生成、奖励计算)均由服务器控制。**
