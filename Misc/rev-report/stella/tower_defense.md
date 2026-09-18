# 游棋保卫战 (TowerDefense) 逆向分析报告

## 1. 概述

"游棋保卫战" 是星塔旅人的内置迷你游戏模式，属于塔防 (Tower Defense) 类型。玩家在棋盘格 (grid) 上部署"棋子"(chess pieces)——即角色，抵御沿预设路线移动的怪物波次。

内部代码名称为 **`TowerDefense`**，通过 `GameEnum.worldLevelType.TowerDefense = 22` 和 `AdventureModuleLevelLoadParams.BootConfigLoadType.TowerDefense = 150` 标识。

活动共 4 个赛季 (2025/12/02, 2026/01/27, 2026/03/31, 2026/07/14)，每个赛季 16 个任务组 (4 级 × 4 页)，questGroupLevel: 初来乍到/熟能生巧/游棋高手/游棋大师。

---

## 2. 架构

### 2.1 技术栈
| 层 | 技术 | 职责 |
|---|---|---|
| **UI** | Lua (XLua) | 卡牌拖拽、信息显示、结果面板、暂停面板 |
| **配置** | .bytes 二进制表 | 棋子属性、关卡、怪物、地板、潜能、道具 |
| **战斗核心** | C# (IL2CPP → ARM64) | 格子管理、寻路、实体生成、伤害计算、Buff 系统 |
| **脚本** | AIScript Lua | 怪物波次控制、道具 AI 效果、场景逻辑 |
| **网络** | Protobuf | LevelApply → 进入关卡; LevelSettle → 结算; QuestReceive → 领取任务奖励 |

### 2.2 文件分布 (35 个 Lua + 12 个 .bytes + 24 个 C# 类)

**Lua 文件 (35)**:
```
game/ui/towerdefense/               -- 主 UI 控制器组
  towerdefensectrl.lua (97KB)       -- 核心战斗 UI: 卡牌/物品拖拽、速度控制、能量条
  towerdefenseteamctrl.lua          -- 编队编辑
  towerdefenseselectctrl.lua        -- 关卡选择
  towerdefenseresultctrl.lua        -- 结算结果
  towerdefensequestctrl.lua         -- 任务面板
  towerdefensepotentialselectctrl.lua -- 潜能选择
  towerdefensecharacterdetailctrl.lua -- 棋子详情
  towerdefenseguidectrl.lua         -- 新手引导
  towerdefensemonsterinfoctrl.lua   -- 怪物信息提示
  towerdefensepausectrl.lua         -- 暂停菜单
  towerdefensegiveupctrl.lua        -- 放弃确认
  towerdefenseleveldetailctrl.lua    -- 关卡详情
  towerdefensehudctrl.lua           -- HUD 控制
  ... (22 more UI 子控件)

gamecore/data/dataclass/activity/
  towerdefensedata.lua              -- 活动数据管理 (关卡进度/任务/剧情/红点)
  towerdefenseleveldata.lua         -- 单局数据 (棋子等级/潜能/技能CD)
```

**配置表 (.bytes, protobuf 编码)**:
```
towerdefensecharacter.bytes  (21 rows) -- 可部署棋子角色
towerdefenselevel.bytes      (39 rows) -- 关卡定义
towerdefensefloor.bytes      (39 rows) -- 地板/地图定义
towerdefensemonster.bytes    (18 rows) -- 怪物数据
towerdefensepotential.bytes (126 rows) -- 潜能/天赋 (7×18)
towerdefenseitem.bytes        (4 rows) -- 道具
towerdefensequest.bytes      (99 rows) -- 任务
towerdefensequestgroup.bytes (16 rows) -- 任务组
towerdefensecontrol.bytes     (4 rows) -- 活动控制 (赛季)
towerdefenseguide.bytes      (46 rows) -- 引导步骤
towerdefensestory.bytes              -- 活动剧情
towerdefenseteamexp.bytes            -- 编队经验
```

**C# 类 (24, 来自 dump.cs 和 script.json)**:
```
核心控制器:
  TowerDefenseDemoController        -- 主游戏控制器 (card system, energy, update)
    ├── CardBase                    -- 卡牌基类
    ├── CardRole                    -- 角色部署卡
    ├── CardStrength                -- Buff 强化卡
    └── CardUltimate                -- 终极技能卡

地图系统:
  TowerDefenseMapData               -- 地图数据 (grid scale, size, routes)
    ├── TowerGrid                   -- 格子 (x, y, index, walkable, deploy, attribute)
    ├── RouteGridInfo               -- 路径点 (grid ID + action)
    ├── TowerDefenseRoute            -- 怪物路线
    └── RouteAction                 -- 路线动作
  TowerDefensePathFinding           -- A* 寻路
  TowerDefenseGrid                  -- 格子 MonoBehaviour
    ├── GridWalkableType            -- 可走性 (Default=0, Walkable=1)
    ├── GridDeployType              -- 部署类型 (SpawnPoint, PlayerSpawn, Trap, Pothole)
    └── GridAttribute               -- 格子属性 (Default, Fire)

事件系统:
  TowerDefensePauseMonsterMoveEvent -- 暂停怪物移动
  TowerDefenseMonsterActionEvent    -- 怪物执行路线动作
  TowerDefenseSetRoleOnStageEvent   -- 放置角色到棋盘
  TowerDefenseEnergyCapsuleEvent    -- 能量胶囊拾取

UI/视觉:
  TowerDefenseIndicatorController   -- 攻击范围指示器
  TowerDefenseMapLineController     -- 路线绘制
  TowerDefenseMouseFollower         -- 拖拽跟随
  TowerDefensePointerEvent          -- 点击/拖拽事件
  TowerDefensePrefabData            -- 预制体数据
```

---

## 3. 完整战斗流程

### 3.1 进入关卡

```
1. 玩家选择关卡 (levelId) → 选择编队 (characterList, itemId)
2. Lua: TowerDefenseData:RequestEnterLevel(levelId, characters, itemId)
   → HttpNetHandler.SendMsg(activity_tower_defense_level_apply_req, ...)
3. 服务器返回成功 → 客户端加载场景
4. C#: CS.AdventureModuleHelper.EnterTowerDefenseLevel(floorId, params)
   → params = [itemId, "charId1,charId2,..."]
   → 设置 BootConfigLoadType = 150 (TowerDefense)
5. 加载 floor 配置对应的 Unity 场景:
   - scene: "Levels/TowerDefence/TowerDefence_1_1"
   - mapData: "TowerDefence_1_1" 
   - AI: "AIScript.TowerDefenseGameplay_1_0"
   - grid: 6×9 ~ 20×43 不等
   - 锁定编队 (若 floor.TeamGroup 有值)
6. TowerDefenseDemoController.Start() → InitCards() → 显示角色卡牌
7. 发事件 TOWERDEFENSE_LOAD_FINISH → Lua 显示 UI, 开启交互
```

### 3.2 卡牌系统

卡牌是 Tower Defense 的核心交互介质:

| 卡牌类型 | 对应 C# 类 | 效果 | 操作方式 |
|---|---|---|---|
| **角色卡** | CardRole | 在可部署格子上放置角色棋子 | 拖拽卡牌到棋盘 |
| **强化卡** | CardStrength | 为已部署角色添加 Buff | 拖拽到已部署角色 |
| **终极卡** | CardUltimate | 角色释放终极技能 | 点击强化面板 |
| **道具卡** | 物品 | 使用特殊道具 | 拖拽到战场区域 |

**卡牌上限**: 最多 6 个角色卡 (3 个可见 + 3 个后备)

**部署逻辑** (C# `TowerDefenseDemoController.UseCard`):
```
CardRole:
  → 获取部署坐标 (screenPos → worldPos via transform)
  → 创建 ActorSpawnInfo (characterId, position, ...)
  → AdventureModuleController.SpawnMonster(entity)
  → 发事件 SET_ROLE_ON_STAGE_RESULT → Lua 更新 UI

CardStrength:
  → 找到目标实体 (LogicEntity via sub_3F9597C)
  → BuffCom.AddBuff(entity, buffId, targetEntity)
  → 发事件更新数值

CardUltimate:
  → 显示强化面板 (ShowQianghuaPanel)
  → 玩家选择升级或查看详情
```

### 3.3 能量系统

角色随时间自动积累能量 (`TowerDefenseDemoController.Update`):

```
每一帧: deltaTime += Time.deltaTime
当 deltaTime >= energyInterval:
  → energy += energyStep
  → UpdateEnergyShow()
  → 发事件 TOWERDEFENSE_UPDATE_ENERGY → Lua 更新技能 CD 条

能量满时 (abs(energy - maxEnergy) < epsilon):
  → TowerDefenseDemoController.EnergyFull()
  → 发事件 TOWERDEFENSE_SHOW_ROLE_ICON → 显示角色功能按钮
  → 玩家可点击: 升级 (CharacterLevelUp) 或 详情 (ShowCharacterDetail)
```

### 3.4 怪物系统

**怪物波次由 `AIScript.TowerDefenseGameplay_X_Y` 控制** (编译 Lua 脚本):

- 怪物从 `MonsterSpawnPoint` 格子出生
- 沿 `TowerDefenseRoute` 预设路线移动
- 每个路径点可配置 `RouteAction` (动作触发)
- 怪物到达终点 → 扣减耐久度 (Durability)
- 发事件更新: 剩余怪物数, 耐久度

**怪物属性** (towerdefensemonster.bytes):
```
id: 8069901 ~ 8069918 (18种)
field 2: 血量 (1000000 ~ ???)
field 3: 种类
field 4: 属性
field 5: 名称 (TowerDefenseMonster.8069901.1 → "小石头怪"等)
```

### 3.5 角色攻击

角色放置后自动攻击: 普攻 (auto-attack) + 技能 (skill, 自动释放)

**伤害计算**: 使用主战斗系统的 `AdventureActor$$CalculateDamage`
- 基础伤害 = 攻击力 × 攻击倍率 × 防御修正
- 受潜能 (Potential/Buff) 修改:
  - 攻击力提升 (如 "热情扳机": 普攻攻击力逐渐提升)
  - 范围攻击 (如 "优势火力": 普攻强化为范围攻击)
  - 特殊效果 (如 "绝妙接力": 盾牌命中眩晕目标)

**角色属性** (towerdefensecharacter.bytes):
```
id: 8010301 ~ 8015601 (21个)
name: TowerDefenseCharacter.8010301.1 → "琥珀"
characterId: 10301 ~ 15601
rarity: 1=★☆...
SkillCd: 45000~150000 (毫秒)
NewPotential[1..5]: 升级可选潜能ID列表
icon: "Icon/Head/head_10301"
```

### 3.6 角色升级

```
条件: 经验条满 (EXP) → 获得升级点数 (point)
流程:
  1. 点击角色功能按钮 → CharacterLevelUp
  2. 检查 point >= PointNeeded[oldLevel]
  3. 扣除 point, 升级到 newLevel (max 6)
  4. 若 NewPotential[newLevel] 存在:
     - 1 个潜能 → 直接添加
     - 2+ 个潜能 → 打开潜能选择面板
  5. 添加潜能: CS.AdventureModuleHelper.ChangePersonalPerkIds(perkInfo, characterId)
  6. 发事件 TOWERDEFENSE_CHAR_LEVELUP → 刷新 UI
```

**潜能系统** (towerdefensepotential.bytes, 126 个):
```
每个角色 7 个潜能 (level 2~6 各 1-3 个选项)
示例 (琥珀 8010301):
  Lv2: [1030105] 攻击力 ↑
  Lv3: [1030106] 攻击速度 ↑
  Lv4: [1030102] 精准控温 - 技能杀敌充能50%
  Lv5: [1030107] 攻击力 ↑, [1030103] 优势火力 - 普攻变范围
  Lv6: [1030104] 散落舞步 - 生成幻影旋转射击

潜能品质: 1=绿色(基础), 2=蓝色(稀有)
```

### 3.7 道具系统

**4 种道具** (towerdefenseitem.bytes):

| ID | 名称 | 类型 | CD(秒) | 数量 | AI 脚本 |
|---|---|---|---|---|---|
| 1001 | 酷脆刨冰 | CD | 15 | - | AreaEffect_IceArea |
| 1011 | 大瓶装能量沛沛 | CD+Count | 8 | 8 | EnergyCapsule |
| 1021 | 杂草抑制剂 | Count | - | 6 | Herbicide |
| 1031 | 罐装乌云 | CD | 6 | - | (cloud/rain) |

**道具使用流程**:
```
1. 拖拽道具卡到战场 → OnDrag_Item → dispatchEvent("TOWERDEFENSE_DRAG_ITEMCARD_BEGIN")
2. 释放 → TOWERDEFENSE_SET_ROLE_ON_STAGE_RESULT → UseItemCard callback
3. 若成功: 触发 CD 倒计时 (DOTween 渐变条)
4. CD+Count 型 (如能量沛沛): CD 结束前不可用, 且受次数限制
5. CD 型 (如刨冰): 仅 CD 限制
6. Count 型 (如除草剂): 仅次数限制
```

**道具 AI 效果** (AIScript):
- `TowerDefenseItem_AreaEffect_IceArea`: 在大范围降下冰阵，减速怪物
- `TowerDefenseItem_EnergyCapsule`: 给角色回复技能能量
- `TowerDefenseItem_Herbicide`: 消除草丛障碍物

### 3.8 时间控制

```
function SetTimeScale(bSpeedUp)
  normal: CS.AdventureModuleHelper.TowerDefense_SetTimeScale(100)
  fast:   CS.AdventureModuleHelper.TowerDefense_SetTimeScale(150)  (1.5x)
  slow:   CS.AdventureModuleHelper.TowerDefense_SetTimeScale(10)   (0.1x, 慢动作拖拽时)
```

- 快速 (×1.5): 点击倍速按钮，加速战斗
- 慢速 (×0.1): 拖拽卡片时自动进入慢动作模式，方便精确放置

### 3.9 暂停系统

```
PauseLogic():
  → InputDisable()
  → dispatchEvent("TowerDefenseShowFullScreenPanel")
  → 强制结束所有拖拽 (DoDragEnd)
  → 回到正常速度

触发场景: 暂停菜单、结果面板、潜能选择、角色详情
```

---

## 4. 伤害结算逻辑

### 4.1 伤害计算通路

```
角色棋子 (TowerDefenseCharacter) 
  → 部署为 AdventureActor 实体
  → Auto-attack: 检测范围内最近怪物
  → AdventureActor.CalculateDamage(atkData, defData, dmgData)
  → 乘区: 
    fromSrcAtk       (攻击力)
    fromEE           (元素效率)
    fromCritRatio    (暴击率)
    toDefAmend       (防御修正)
    toEERCD          (伤害减免)
    ... (共12+乘区)
  → BuffCom.AddBuff 添加 Buff 效果 (缓冲、debuff等)
  → BuffEntity 周期性 Tick
  → 怪物 HP 减少
```

核心伤害公式详见 `report/battle_system.md` §10。TowerDefense 复用主战斗系统的相同公式，额外加成来自：
- 潜能系统 (buffId 通过 `ChangePersonalPerkIds` 施加)
- 道具效果 (如刨冰造成固定伤害 + 减速)

### 4.2 Buff 叠加

```
CardStrength 使用:
  1. 查找目标实体 (BoardPointComponent)
  2. BuffCom.AddBuff(buffCom, buffId, targetEntity)
  3. buffId = CardStrength.belongRoleID (来自卡牌数据)
```

Buff 互斥/叠加规则由 `BuffManager.AddBufftoGroup` 决定 (参见主战斗系统报告 §12)。

### 4.3 胜负条件

- **胜利**: 所有怪物波次被消灭
- **失败**: 耐久度 (Durability) ≤ 0 (怪物触达终点)
- 地板配置 `Durability` 值决定可承受多少次怪物抵达

**击退/控制效果**: 由潜能提供:
- `风蚀冲击` (夏花): 技能附加易伤
- `加速冰柱阵列` (鸢尾): 减速→冰冻
- `绝妙接力` (缇莉娅): 盾牌眩晕

---

## 5. 结算与评分

### 5.1 星级判定

```
基础: 通关 → 1 star
Condition2: HP > config.Condition2 → +1 star (2星)
Condition3: HP > config.Condition3 → +1 star (3星)
Perfect: HP == floor.Durability (满耐久通关) → +10 bonus (最终 13星)

其中 Condition2/Condition3 在 TowerDefenseLevel 配置中:
  - Level 1101: Condition2=50, Condition3=30 (耐久度百分比)
  - Level 1102: Condition2=50, Condition3=1 (极低容错)
```

### 5.2 网络结算

```
RequestFinishLevel(levelId, bResult, nHp):
  计算 nStar: 1 → +(Condition2满足) → +(Condition3满足) → +(Perfect)
  发送: activity_tower_defense_level_settle_req {LevelId, Star}
  服务器保存最高星数
  → 更新客户端 levelData.Star = max(nStar, oldStar)
  → 打开结果面板 (TowerDefenseResultPanel)
  → 埋点上报 (UserEventUpload)
```

### 5.3 失败结算

```
失败/退出:
  → RequestFinishLevel(levelId, false, nHp)
  → Star = 0
  → 结算面板显示 0 星
```

### 5.4 跳过 (Skip) 结算

```
SkipLevel(levelId, characters, itemId):
  → 发送 apply_req (正常进入)
  → 不加载场景, 直接发送 settle_req {Star=13}
  → 服务器返回 Perfect 奖励
  → 更新本地数据 13 星
```

### 5.5 Proto 消息定义

```protobuf
// 内嵌在 ActivityMsg 中
message ActivityTowerDefense {
    repeated ActivityTowerDefenseLevel Levels = 1;  // 关卡列表
}

message ActivityTowerDefenseLevel {
    int32 Id = 1;      // 关卡ID
    int32 Star = 2;    // 最高星数
}

// 请求
message ActivityTowerDefenseLevelApplyReq {
    int32 Level = 1;           // 关卡ID
    repeated int32 Characters = 2;  // 编队角色
    int32 ItemId = 3;          // 道具ID
}

message ActivityTowerDefenseLevelSettleReq {
    int32 LevelId = 1;         // 关卡ID
    int32 Star = 2;            // 星数 (0-13)
}

message ActivityTowerDefenseQuestReceiveReq {
    int32 ActivityId = 1;      // 活动ID
    int32 GroupId = 2;         // 任务组ID (一键领取)
    int32 QuestId = 3;         // 单个任务ID
}
```

---

## 6. 任务系统

**任务组**: 16 组，每组 4 级 (初来乍到/熟能生巧/游棋高手/游棋大师)

**任务类型** (towerDefenseCond):
- `TowerDefenseClear` (类型 2): 通关指定关卡
- `TowerDefenseClearSpecificStar` (类型 3): 以指定星数通关

**奖励**: 道具 (技巧棋子 ID:32000, 33912等)

**领取流程**:
```
单个领取: QuestReceiveReq {ActivityId, QuestId}
一键领取: QuestReceiveReq {ActivityId, GroupId}
→ 服务器返回 rewards
→ UTILS.OpenReceiveByChangeInfo() 打开奖励界面
→ UpdateQuest(Received)
→ 刷新红点
```

---

## 7. 配置表字段详解

### 7.1 TowerDefenseCharacter (棋子角色, 21 rows)
| Field | 说明 | 示例 (琥珀) |
|---|---|---|
| 1 | id | 8010301 |
| 2 | 名称 key | TowerDefenseCharacter.8010301.1 |
| 3 | 关联角色 ID | 8010301 |
| 4 | 稀有度 | 1 |
| 5 | 技能 CD (毫秒) | 75000 = 75秒 |
| 7 | ??? | 8010301 |
| 8-12 | NewPotential[1-5] | [1030105, 1030106, 1030102, 1030107, 1030104] |
| 13 | ??? | 2 |
| 14 | ??? | 1 |
| 15-16 | ??? | 8010301, 8010302 |
| 17 | ??? (经验?) | 80000 |
| 18 | ??? | 1 |
| 19 | ??? | 8010301 |
| 20 | 头像图标 | "Icon/Head/head_10301" |

### 7.2 TowerDefenseFloor (地板, 39 rows)
| Field | 说明 | 示例 (Floor 1000) |
|---|---|---|
| 1 | id | 1000 |
| 2 | 场景路径 | "Levels/TowerDefence/TowerDefence_1_1_Night" |
| 3 | 地图数据名 | "TowerDefence_1_0" |
| 5 | AI 脚本 | "AIScript.TowerDefenseGameplay_1_0" |
| 6 | 宽度 (列数) | 9 |
| 7 | 高度 (行数) | 9 (6-60 不等) |
| 9/12 | 起始角色 (锁定) | 8011201 (尘沙) / 8010301 (琥珀) |
| 11 | 道具 ID | 1/3/2/350 (0=无) |
| 13 | ??? | 0/1000/350 |
| 14 | PreFloor | (锁定编队时) |
| 15 | BGM 战斗 | "towerDefense_forest_combatNormal_setState" |
| 16 | BGM 停止 | "towerDefense_forest_all_stop" |
| 17 | 摄像机 | "EnterCamera_4X8" |
| 18 | ??? | 1 |

### 7.3 TowerDefenseLevel (关卡, 39 rows)
| Field | 说明 | 示例 (1101) |
|---|---|---|
| 1 | id | 1101 |
| 2 | 活动 ID | 102001 |
| 4 | 名称 key | TowerDefenseLevel.1101.1 |
| 5 | 页码 (LevelPage) | 1 |
| 7 | 图标 | "UI/Play_TowerDefence/.../db_towerdef_lv1" |
| 8 | 关联 FloorId | 1000 |
| 9 | 前置关卡 (PreLevel) | 0 (首关) / 1101 |
| 11 | ??? | 1011101 |
| 12-14 | 目标描述 key | Des1/Des2/Des3 |
| 16 | 解锁天数 (ActiveTime) | 3 |
| 17 | Condition2 (耐久%) | 50 |
| 18 | Condition3 (耐久%) | 30 |
| 19-20 | ??? | 50, 30 / 1, 2 / ... |
| 21 | ??? | 2 / 500000 |

### 7.4 TowerDefenseItem (道具, 4 rows)
| ID | 名称 | CD(秒) | 数量 | AI |
|---|---|---|---|---|
| 1001 | 酷脆刨冰 | 15 | - | IceArea |
| 1011 | 大瓶装能量沛沛 | 8 | 8 | EnergyCapsule |
| 1021 | 杂草抑制剂 | - | 6 | Herbicide |
| 1031 | 罐装乌云 | 6 | - | (cloud) |

---

## 8. 事件系统

### 8.1 Lua → C# 事件 (通过 NovaAPI.DispatchEvent)

| Event | Data | 触发场景 |
|---|---|---|
| `TOWERDEFENSE_CARDOUTAREA` | characterId | 卡片拖出棋盘区域 → 请求部署角色 |
| `TOWERDEFENSE_DRAG_ITEMCARD_BEGIN` | - | 开始拖拽道具卡 |
| `TOWERDEFENSE_CANCEL_DRAG_STATE` | - | 取消拖拽 |
| `TOWERDEFENSE_TIMESCALE_CHANGED` | speed | 时间流速改变通知 |
| `TOWERDEFENSE_HANDLE_CONTROL_L1R1` | direction | 手柄 LB/RB 切换位置 |
| `TOWERDEFENSE_HANDLE_CONTROL_L2R2` | direction | 手柄 LT/RT 切换角色 |
| `TOWERDEFENSE_CARDPOINTENTER/EXIT` | - | 鼠标进入/离开卡片 → 变慢 |

### 8.2 C# → Lua 事件

| Event | Data | 触发时机 |
|---|---|---|
| `TOWERDEFENSE_GIVE_A_ROLE_CARD` | characterId, showTips | 获得新角色卡 |
| `TOWERDEFENSE_SET_ROLE_ON_STAGE_RESULT` | success, entityId, charId, pos | 角色放置结果 |
| `TOWERDEFENSE_UPDATE_LEVELUP` | point, remainPoint | 升级点数变化 |
| `TOWERDEFENSE_UPDATE_LEVEL_DURABILITTY` | curHP, maxHP | 耐久度变化 |
| `TOWERDEFENSE_UPDATE_MONSTER_NUM` | cur, max | 怪物计数变化 |
| `TOWERDEFENSE_UPDATE_EXP` | curExp, maxExp | 经验值变化 |
| `TOWERDEFENSE_LEVEL_RESULT` | bResult | 关卡结束 |
| `TOWERDEFENSE_SHOW_ROLE_ICON` | charId, isShow | 能量满 → 显示角色功能 |
| `TOWERDEFENSE_UPDATE_ITEM_CARD` | itemId, count | 道具卡更新 |
| `TOWERDEFENSE_USE_ITEM_CARD_RESULT` | bResult | 道具使用结果 |
| `TOWERDEFENSE_CHAR_LEVELUP` | charId, level, x, y, hasSelect | 角色升级完成 |
| `TOWERDEFENSE_SHOW_MONSTER_INFO` | monsterId | 点击怪物显示详情 |
| `TowerDefense_Exit/Restart/Continue_OnClick` | - | 暂停菜单选项 |

---

## 9. 关键代码路径

### 9.1 进入关卡
```
TowerDefenseSelectCtrl:ConfirmSelect()
→ TowerDefenseData:RequestEnterLevel(levelId, chars, itemId)
→ HttpSend: activity_tower_defense_level_apply_req
→ callback: EnterTowerDefenseLevel(floorId, ["itemId", "charIds"])
→ TowerDefenseDemoController.Start() → InitCards()
→ HUD open → LoadLevelRefresh → UI 显示
```

### 9.2 部署角色
```
用户拖拽角色卡出棋盘
→ TOWERDEFENSE_CARDOUTAREA (charId)
→ TowerDefenseSetRoleOnStageEvent → TowerDefenseDemoController.OnTriggerUseRoleCard
→ TowerDefenseMapData.GetGrid(screenPos) → 验证部署位置
→ AdventureModuleController.SpawnMonster(entityConfig)
→ TOWERDEFENSE_SET_ROLE_ON_STAGE_RESULT (success, entityId)
→ Lua: TowerDefenseLevelData.AddCharacter(charId, entityId)
```

### 9.3 战斗循环 (C# Update)
```
TowerDefenseDemoController.Update():
  if inputEnabled:
    AccumulateEnergy(deltaTime)  // 能量积累
    if energy >= threshold:
      EnergyFull() → show character actions
  // 实体自动战斗由 AdventureActor 系统处理
  // 怪物移动由 AIScript 控制
```

### 9.4 结算
```
怪物全灭/耐久归零:
  → TOWERDEFENSE_LEVEL_RESULT (bool)
  → Lua: OnEvent_FinishGame(bResult)
  → TowerDefenseData:RequestFinishLevel(levelId, bResult, hp)
  → 计算 Star: 1 + cond2 + cond3 + perfect(10)
  → HttpSend: activity_tower_defense_level_settle_req {LevelId, Star}
  → 打开结果面板
  → 埋点上报
```

---

## 10. 与主战斗系统的异同

| 方面 | 主战斗系统 | 游棋保卫战 |
|---|---|---|
| 操控 | 手动释放技能 | 自动攻击 + 自动技能 |
| 移动 | 手动走位 | 怪物路线固定, 角色定点不动 |
| 部署 | 预先编队 | 战斗中消耗"卡牌"部署 |
| 升级 | 外部养成 | 局内经验升级 (level 1→6) |
| 天赋 | 外部潜能树 | 局内每次升级选 1 潜能 |
| 道具 | 无/消耗品 | 专属道具 (CD+次数限制) |
| 胜利 | 消灭所有敌人 | 消灭所有敌人 + 保护耐久度 |
| 评分 | 星级 (1-3) | 星级 (1-3) + 完美 (13) |
| 伤害公式 | AdventureActor.CalculateDamage | **复用相同公式** + 潜能Buff修改 |

---

## 11. 可部署角色列表 (21人)

| ID | 名称 | Skill CD (秒) | 备注 |
|---|---|---|---|
| 8010301 | 琥珀 | 75 | 初始角色 |
| 8011101 | 鸢尾 | 150 | |
| 8011201 | 尘沙 | 45 | |
| 8010701 | 缇莉娅 | - | |
| 8011001 | 翡冷翠 | - | |
| 8011401 | 猫眼 | - | |
| 8011801 | 科洛妮丝 | - | |
| 8012301 | 杏子 | - | |
| 8012601 | 紫槿 | - | |
| 8012701 | 特丽莎 | - | |
| 8013001 | 多娜 | - | |
| 8013301 | 夏花 | - | |
| 8013401 | 冬香 | - | |
| 8013501 | 雾语 | - | |
| 8014001 | 斯帕克拉 | - | |
| 8014101 | 赤霞 | - | |
| 8014301 | 风影 | - | |
| 8015601 | 小禾 | - | |

注: 带 - 的角色 Skill CD 值在表中未完整提取 (各角色从 75000~150000ms 不等)

---

## 12. 附录: 地图数据解析

### TowerDefenseMapData 结构 (C#)

```cs
public class TowerDefenseMapData : ScriptableObject {
    public float gridScale;           // 格子缩放
    public Vector2Int gridSize;       // 格子尺寸 (width, height)
    public TowerGrid[] towerGrids;    // 所有格子
    public TowerDefenseRoute[] routes;// 怪物路线
    
    public struct TowerGrid {
        public int x, y;              // 坐标
        public int index;             // 索引
        public GridWalkableType walkableType;  // 可走性
        public GridDeployType deployType;      // 部署类型
        public GridAttribute attribute;        // 属性
    }
    
    public struct RouteGridInfo {
        public int gridID;            // 关联格子
        public RouteAction action;    // 动作
    }
    
    public struct TowerDefenseRoute {
        public RouteGridInfo[] grids; // 路径点序列
    }
}
```

### 寻路系统

```
TowerDefensePathFinding.FindPath(start, end):
  使用 A* 算法
  GetNeighbors: 检查上下左右 4 方向
  权重: 考虑 GridWalkableType
  障碍物: TowerDefenseMapData.SetObstacle()
```

---

*报告生成时间: 2026-07-18*
*分析范围: Lua 35文件 + .bytes 12表 + C# 24类 + 2078个 IDA函数*
