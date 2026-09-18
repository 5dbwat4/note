# 星塔旅人 战斗系统 完整逆向报告

> 数据来源: 反编译 Lua 源码 (65/66 成功) + data/bin/*.bytes 数据表 + language/zh_cn/*.json 文本
> 反编译产物: tmp/REVERSE/battle_decompiled/ (65个文件)
> 版本: iOS 1.9.0

---

## 1. 系统架构总览

战斗由三层协作完成:

| 层 | 职责 | 关键文件 |
|---|---|---|
| **C# 战斗引擎** (Unity IL2CPP) | 实时物理/碰撞、伤害计算、AI 执行、实体管理 | `CS.AdventureModuleHelper`, `CS.InteractiveManager` |
| **Lua UI 层** | HUD 显示、技能按钮、伤害数字、结果面板 | `mainbattlectrl.lua`, `hudmainctrl.lua`, `battleresultctrl.lua` |
| **Lua 数据层** | 角色属性计算、Disc 效果组装、编队管理 | `characterattrdata.lua`, `discdata.lua`, `playerteamdata.lua` |

**关键结论**: 伤害公式在 **C# 引擎**中 (Lua 侧不可见); Lua 负责将角色属性/装备效果组装成 `ActorAttribute` 结构体传给 C#, C# 在战斗中实时计算最终伤害并回传 `HudDamage` 事件给 Lua 显示。

---

## 2. 战斗流程图

```
[编队面板] → 选关 → 进入冒险场景
         │
         ▼
  MainBattlePanel.OnEnable()
    ├─ OpenPanel(Hud)         → HudMainCtrl 加载 17 个 HUD 预制体
    ├─ ClosePanel(Formation)  → 关闭编队面板
    └─ SubSkillDisplayInit    → 初始化副技能显示
         │
         ▼
  C# AdventureModuleHelper 加载战斗场景
    ├─ 生成地图、怪物波次
    ├─ 设置角色属性 (由 Lua BuildCharacterData 传入)
    └─ 发送实体事件:
         ├─ PlayerShow(id)        → HudMainCtrl 生成 PlayerHudCtrl
         ├─ MonsterHUDChange(id)  → HudMainCtrl 生成 MonsterHudCtrl/EliteMonsterHudCtrl
         └─ ShowBossHUD(id)       → Boss HUD
         │
         ▼
  ╔═══════════ 实时战斗循环 (C# 执行) ═══════════╗
  ║  玩家操作 → 角色移动/攻击/技能 → 伤害计算 → ║
  ║  → HpChanged/ShieldChanged/BuffChanged 事件  ║
  ║  → HudDamaged/HudHealed → 浮空数字          ║
  ║  → 怪物死亡/波次结束 → 结算                  ║
  ╚══════════════════════════════════════════╝
         │
         ▼
  C# LevelStateChanged(Success/Failed)
    └─ BattleEndReq → 服务器结算
         │
         ▼
  BattletResultCtrl 打开
    ├─ nStar       (1-3星)
    ├─ GenerReward + FirstReward + ChestReward
    ├─ nExp        (世界等级经验)
    └─ tbCharDamage (伤害统计)
```

---

## 3. 战斗 HUD 系统 (hudmainctrl.lua — 522行)

### 3.1 17 种 HUD 预制体

| 预制体 | 用途 |
|---|---|
| `PlayerHUD.prefab` | 玩家角色血条/盾条/能量/弹药 |
| `MonsterHUD.prefab` | 普通怪物血条 (5秒无伤自动隐藏) |
| `MonsterHUD_Epic.prefab` | 精英/Boss 怪物血条 (含 Toughness 破韧条) |
| `MonsterHUD_PlayerSummoner.prefab` | 召唤物怪物 HUD |
| `CritDamageHUDNumber_UI.prefab` | 暴击伤害数字 (大字+特效) |
| `DamageHUDNumber_UI.prefab` | 普通伤害数字 |
| `MinDamageHUDNumber_UI.prefab` | Dense(多段密集)伤害数字 (小字) |
| `DotDamageHUDNumber_UI.prefab` | DoT 伤害数字 |
| `HealHUDNumber_UI.prefab` | 治疗数字 |
| `WordHud_UI.prefab` | 文字提示 (免疫/闪避/抵抗/Mark) |
| `NpcHud.prefab` | 可交互 NPC 指示器 |
| `BreakOutHUDNumber_UI.prefab` | Break 分数显示 ("+N") |
| `ToughnessDamageHUD_UI.prefab` | 破韧累计伤害显示 |
| `HudHuoChuiBoss.prefab` | 特殊 Boss (火锥Boss) 血条 |
| `*_Vampire.prefab` (×3) | 吸血鬼幸存者模式的专用伤害数字 (骷髅风格) |

### 3.2 伤害数字生成逻辑 (hudmainctrl.lua:248-297)

```lua
function HudMainCtrl:OnEvent_HudDamaged(id, value, isCrit, hitDamageConfig, formId, isMark, fromElementType, hudColorIndex)
  -- 1. 如果实体处于破韧状态, 伤害累积到 Toughness 显示
  if tabToughnessEntity[id] then
    SetToughnessValue(id, val)
    return
  end

  -- 2. 选择预制体 (6种路径):
  --    IsDenseType + isVampire → MinDamageHUDNumber_Vampire
  --    IsDenseType            → MinDamageHUDNumber (多段密集)
  --    isCrit + isVampire     → CritDamageHUDNumber_Vampire
  --    isCrit                 → CritDamageHUDNumber (暴击)
  --    isVampire              → DamageHUDNumber_Vampire
  --    默认                    → DamageHUDNumber (普通)

  -- 3. 颜色由 hudColorIndex 决定:
  --    4=正常色, 5=灰色(抵抗)

  -- 4. 延迟0.5秒检查是否出现 "Resistance" 抵抗提示
  if nTypeGreyResistanceTime[id] + interval < serverTime then
    -- 弹 "Resistance" 文字
  end
end
```

### 3.3 防御文字 (免疫/闪避/抵抗)

```lua
-- 三种类型:
-- type 1 → "Missing"   (闪避/Miss, wordType=8)
-- type 2 → "Immunity"  (免疫, wordType=7)
-- type 3 → "Resistance"(抵抗, wordType=9)
```

---

## 4. 玩家 HUD (playerhudctrl.lua — 385行)

### 4.1 显示元素

| 元素 | 动画 | 关键参数 |
|---|---|---|
| **HP 血条** | tween动画 (0.16s) | 红闪(受伤) / 绿闪(治疗) / 大伤害抖动 (>阈值) / <25%危险闪烁 |
| **Shield 盾条** | tween (0.5s) + 非线性缩放 | `(0.3 * %) ^ 0.5` 公式防止小盾值看不见 |
| **Ammo 弹药** | 数字显示 | 远程武器(ammoMax>0)时显示, 5 种子弹类型图标 |
| **Buff 状态** | BuffCtrl 子组件 | 绑定 entity → 自动显示 |
| **能量/技力环** | (由 SkillBtnCtrl 管理) | 技能按钮下方环形充能条 |
| **JsAniObj** | Buff倒计时缩短闪烁 | 当角色有 BuffReduceTime 效果时显示 |

### 4.2 HP 条详细动画

```lua
function PlayerHudCtrl:PlayTweenHp(hp, hpMax)
  if hp < previousHp then  -- 受伤
    -- 红色 hit flash (imgHit 闪烁)
    -- 大伤害 (>BloodSpecialEffectThreshold): 触发 HPShake_in 震动 + imgBigHit 闪烁
    -- HP < 25%: imgBg2 危险指示器显示
  else                      -- 治疗
    -- 橙色治疗颜色 (imgRecoverHp)
    -- 绿色治疗闪 (imgHeal)
  end
end
```

### 4.3 实体事件绑定

每个 `PlayerHudCtrl` 通过 C# `EventManager.AddEntityEvent` 注册:
- `HpChanged` → `OnEvent_HpChanged`
- `ShieldChanged` → `OnEvent_ShieldChanged`
- `AmmoChanged` → `OnEvent_AmmoChanged`
- `BuffReduceTime` → 闪烁提示
- `PlayerDeathStateEnter` → `OnEvent_Deaded` → 隐藏 HUD

---

## 5. 怪物 HUD (monsterhudctrl.lua — 433行)

### 5.1 简单怪物 vs 精英/Boss

| 特性 | 简单怪物 (SIMPLE/SIMPLE2) | 精英/Boss (BOSS/MINIBOSS) |
|---|---|---|
| 控制器 | `MonsterHudCtrl` | `EliteMonsterHudCtrl` |
| 血条隐藏 | 5秒无伤后自动淡出 | 永久显示 |
| Toughness 破韧条 | 通常不显示 | 完整破韧机制 |
| 盾条 | ✓ | ✓ |
| Buff | ✓ (BuffCtrl) | ✓ |

### 5.2 Toughness 破韧系统

```lua
-- 3种状态切换
function SetToughness(toughness, toughnessMax, bState, bChange):
  if toughnessMax <= 0: return  -- 无破韧条, 隐藏

  if bState and toughness == 0:  -- 破韧状态
    PlayTweenToughnessBroken()   -- 隐藏正常条, 显示破碎碎片图标 + 震动

  elseif bState and toughness > 0:  -- 恢复状态
    PlayTweenToughnessRecover()     -- 0.3s 填充动画恢复满

  else:  -- 正常受击
    PlayTweenToughness()           -- 正常减少动画 + 大伤害震动
```

---

## 6. 技能操作栏 (battledashboardctrl.lua)

### 6.1 按钮布局

```
主控角色:
  ┌────────┬────────┬────────┐
  │ Dodge  │ Skill  │ Ultra  │
  │ (闪避) │ (技能) │ (必杀) │
  └────────┴────────┴────────┘

支援角色 (slot 2 & 3):
  ┌──────────────┬──────────────┐
  │ SupSkill 1   │ SupUltra 1   │  ← 第2角色
  └──────────────┴──────────────┘
  ┌──────────────┬──────────────┐
  │ SupSkill 2   │ SupUltra 2   │  ← 第3角色
  └──────────────┴──────────────┘
```

每个按钮类型: `SKILL_FLEE(1)`, `SKILL_A(2)`, `SKILL_B(3)`, `SKILL_ULTRA(4)`

### 6.2 技能按钮状态 (skillbtnctrl.lua)

```lua
-- 核心刷新函数
function RefreshBtn(bSuportSkillUseable, QTEpercent, CDpercent, CDsecond, ChargePercent, ChargeSectionNum, ...):
  -- 可用判定:
  if SKILL_ULTRA:
    usable = (ChargeSectionNum >= 1) AND (ChargePercent >= 1) AND (CDpercent <= 0)
  else:
    usable = (ChargeSectionNum >= 1)
  -- 支援技能额外需要 bSuportSkillUseable

  -- 充能段数变化 → 播放充能动画
  -- 从不可用→可用 → 触发 CHAR_ULTRA_CAN_USE / CHAR_SKILL_CAN_USE 事件
```

### 6.3 技能充能与冷却

- **CDpercent**: 冷却剩余百分比, 控制 CD 遮罩旋转和倒计时文字
- **CDsecond**: 冷却倒数秒数, <1s 时显示1位小数
- **ChargePercent**: 充能百分比 (fillAmount系)
- **ChargeSectionNum**: 充能段数 (技能可储存的充能段数, 如支援技能可攒2段)

---

## 7. 技能系统 (数据表)

### 7.1 `skill.bytes` (2114条)

每角色的技能集: `10201`(Normal), `10202`(Dodge), `10205`(Ultimate)

| 字段 | 含义 | 示例 |
|---|---|---|
| f1 | Skill ID | `10201` |
| f2 | 名称 key | `"Skill.10201.1"` |
| f3 | Behaviour 资产路径 | `"Character/10201/Behaviour/Skill10201Behaviour"` |
| f4 | 技能类型 | `1`=普攻, `2`=闪避/位移, `5`=必杀 |
| f5-6 | 描述 key | |
| f7 | 图标路径 | `"Icon/Skill/11801_normal"` |
| f8 | 冷却参数 (ms) | `60000`(60s), `300000`(300s) |
| f9 | 始终 `5` | 可能是 EET/消耗类型标记 |
| f14 | 必杀冷却 (ms) | `600000`(600s) |

**关键**: `Behaviour` 是 Unity MonoBehavior 脚本, 实际技能逻辑(伤害判定/范围/动画)在 C# 中执行。

### 7.2 支援技能 (Assist Skill)

主控角色在场时, 支援角色提供:
- **AssistSkillId** (来自 Character 表 `f8`): 副技能 — 点击后支援角色出场释放
- **UltimateId** (f7): 必杀技 — 可切换到支援角色释放

支援技能显示的三种模式 (用户设置):
1. **Type 3 "总是技能"**: 永远显示技能弹出
2. **Type 2 "总是必杀"**: 每天每个角色显示一次完整必杀动画
3. **Type 1 "首次"**: 每天首次用必杀显示完整动画, 之后用技能弹出

### 7.3 技能 CD 倒计时显示

```lua
function SetCD(percent, second, bBeginResume):
  if second <= 1:
    text = "{second:.1f}s"  -- 剩1秒内显示1位小数
  else:
    text = "{second:.0f}s"  -- 整数秒

  if CDpercent <= 0 and ChargePercent >= 1:
    BtnState = "pressed"   -- 高亮可按
  else:
    BtnState = "normal"    -- CD中
```

---

## 8. 角色属性系统 (characterattrdata.lua)

### 8.1 属性来源三级计算

```
origin{sKey} ──────── 读自配置表 (Attr配置 / Char配置 / Skill配置)
    │
    ▼
base{sKey} ────────── 原始值 + 基础效果加成
    │
    ▼
_{sKey} ────────────── base值 (累加效果中的 BASE_VALUE 子类型)
_{sKey}PercentAmend ── 百分比修正 (累加 PERCENTAGE 子类型)
_{sKey}Amend ───────── 绝对值修正 (累加 ABSOLUTE_VALUE 子类型)
    │
    ▼
{sKey} = _{sKey} × (1 + PercentAmend/100) + Amend  ← 最终公式
    │
    ▼
math.floor({sKey}) ── 向下取整 → 传给 C# ActorAttribute
```

### 8.2 属性键 (AttrConfig) — 部分列表

从 `CalCharacterAttrBattle` 可见完整属性键:
- 基础: **Atk, Hp, Def, CritRate, CritPower, CritResistance, HitRate, Evd, DefPierce, Suppress**
- 元素伤害: **WEP, FEP, SEP, AEP, LEP, DEP** (6属性伤害加成)
- 元素能量: **WEE, FEE, SEE, AEE, LEE, DEE** (6属性能量效率)
- 元素抗性: **WER, FER, SER, AER, LER, DER** (6属性抗性)
- 元素复合: **WEI, FEI, SEI, AEI, LEI, DEI** (6属性复合)
- 伤害类型: **NORMALDMG, SKILLDMG, ULTRADMG, OTHERDMG, MARKDMG, SUMMONDMG, PROJECTILEDMG** (各伤害类型加成)
- 减伤: **RCDNORMALDMG, RCDSKILLDMG, RCDULTRADMG, RCDOTHERDMG, RCDSUMMONDMG, RCDPROJECTILEDMG**
- 破甲/护盾: **DefIgnore, ShieldBonus, IncomingShieldBonus**
- 暴击细分: **NormalCritRate, SkillCritRate, UltraCritRate, SummonCritRate, ProjectileCritRate** 等
- 暴伤细分: **NormalCritPower, SkillCritPower, UltraCritPower** 等
- 其他: **ToughnessDamageAdjust, EnergyConvRatio, EnergyEfficiency, GENDMG, DMGPLUS, FINALDMG, FINALDMGPLUS**

### 8.3 效果来源 (Effect source types)

| EffectType | 来源 |
|---|---|
| `Affinity` | 角色好感度等级效果 |
| `Talent` | 天赋树激活的效果 |
| `Equipment` | 装备(宝石)的效果 (含随机词条) |
| `Disc` | 碟片主/副技能效果 |
| `Potential` | 潜能/Perk 效果 |
| `FateCard` | 秘闻卡效果 (仅在星塔/吸血鬼等 Roguelike 模式) |
| `Note` | 音符效果 (曲谱子系统) |
| `Buff` | 战斗中 Buff/Debuff |

---

## 9. Disc(碟片)装备系统 (discdata.lua)

### 9.1 碟片属性

```lua
DiscData:
  nLevel / nMaxLv        -- 等级 (强化)
  nPhase / nMaxPhase     -- 突破阶段
  nStar / nMaxStar       -- 星级 (升星)
  nStrengthenGroupId     -- 强化曲线组 (决定各等级属性)
  nAttrBaseGroupId       -- 基础属性曲线组 (决定各 Phase 各 Level 的基准属性)
  nAttrExtraGroupId      -- 额外属性曲线组 (升星奖励)
  nMainSkillGroupId      -- 主技能组 (解锁主动技能)
  tbSubSkillGroupId      -- 副技能组 (最多2个, 需音符解锁)
  mapAttrBase[attrKey]   -- {Key, Value, CfgValue} 基础属性
  mapAttrExtra[attrKey]  -- {Key, Value, CfgValue} 额外属性
```

### 9.2 副技能音符要求

副技能有多层 (Layer), 每层需要特定音符组合:
```json
// 例: 需要 90011 音符3个 + 90014 音符2个
{"90011": 3, "90014": 2}
```
玩家需在战斗中收集音符, 满足最低层要求后激活对应层效果。

---

## 10. Buff 系统

### 10.1 数据表

| 表 | 行数 | 关键字段 |
|---|---|---|
| `buff.bytes` | 2644 | `f1`=ID, `f6`=Buff组/类型, `f8`=配置位掩码 |
| `buffeffect.bytes` | 16 | `f3`=效果类型(1/2), `f4`=目标效果ID, `f5`=倍率 |
| `buffvalue.bytes` | (另查) | 效果值细化 |
| `addbuffaction.bytes` | 4 | 动作→Buff 映射 |

### 10.2 Buff 属性修正

Buff 通过 `ATTR_FIX` 或 `PLAYER_ATTR_FIX` 类型添加, 子类型:
- `BASE_VALUE` → 直接加基础值
- `PERCENTAGE` → 加百分比修正 (PercentAmend)
- `ABSOLUTE_VALUE` → 加绝对值修正 (Amend)

### 10.3 HUD 显示

`BuffCtrl` (buffctrl.lua) 绑定到实体后自动获取所有 Buff, 显示图标+层数+剩余时间。

---

## 11. 怪物系统

### 11.1 `monster.bytes` (2738条)

| 字段 | 含义 | 示例 |
|---|---|---|
| f1 | Monster ID | `1100101` |
| f3 | 稀有度/星级 | `5` |
| f5 | 怪物类型 | `1`,`2` |
| f7-8 | 模型/外观 ID (FAId) | `1001501` |
| f9 | 元素属性 | `2`,`3` |
| f10 | HP 基础值 | `35000` |
| f11 | ATK 基础值 | `6000` |
| f12 | DEF 基础值 | `21000` |
| f13 | Break HP (破韧阈值) | `700000` |
| f23 | 资源组 ID | `10001002` |
| f25 | 攻击提示类型 | `1` (Always) |

### 11.2 `monsterai.bytes` (1035条)

| 字段 | 含义 | 示例 |
|---|---|---|
| f1 | AI ID | |
| f2 | ComboGroup 资产路径 | 连招组合 |
| f3,f5 | Base/Second 攻击技能 ID | |
| f6 | AI 脚本路径 | `"AIScript.Monster.TowerDefense.AI_JustRun"` |
| f8 | 攻击间隔 (ms) | `2000`(2秒) |
| f10 | Spawn 脚本 | 召唤/出生行为 |
| f11 | 并行脚本 | |

### 11.3 技能预警 (Skill Hint Indicator)

每个怪物/Boss 可配置 `AttackHintType`:
- **Null**: 无预警
- **Always**: Boss 级永久可见 + 前后摇状态动画
- **其他**: 临时预警 (施放时显示, 结束隐藏)

预警由 `HintIndicators` 管理器维护对象池, 分为 Boss 和 Monster 两种:
- **Boss**: 永久悬浮 (含 Boss 头像图标), 状态机动画: `Idle → Hint(警告闪)→ End(结束) → Idle`
- **Monster**: 临时悬浮, 状态机: `Hide → Hint(警告)→ End(0.2s)→ Hide`

---

## 12. 伤害类型与 HitDamage

### 12.1 `hitdamage.bytes` (1911条)

| 字段 | 含义 | 示例 |
|---|---|---|
| f1 | HitDamage ID | |
| f6 | 始终 `2` | |
| f7-17 | 伤害乘区参数 | 多级配置 |
| f17 | 打击等级/层数 | `6`→`7`→`8` (递增) |

### 12.2 伤害显示分类

| 伤害类型 | 预制体 | 触发条件 |
|---|---|---|
| 普通伤害 | `DamageHUDNumber_UI` | isCrit=false, 非密集 |
| 暴击 | `CritDamageHUDNumber_UI` | isCrit=true |
| 密集(多段) | `MinDamageHUDNumber_UI` | IsDenseType=true |
| DoT | `DotDamageHUDNumber_UI` | `OnEvent_HudDotDamage` |
| 治疗 | `HealHUDNumber_UI` | `OnEvent_HudHealed` |
| 闪避 | `WordHud_UI` ("Missing") | `HudDefenced` type1 |
| 免疫 | `WordHud_UI` ("Immunity") | `HudDefenced` type2 |
| 抵抗 | `WordHud_UI` ("Resistance") | `HudDefenced` type3 + 灰色伤害 |
| 标记 | `WordHud_UI` (自定义) | `OnEvent_HudMark` |
| 破韧累积 | `ToughnessDamageHUD_UI` | 破韧状态下所有伤害显示 |

---

## 13. 护盾系统

### 13.1 `shield.bytes` (58条)

最小值表, 字段稀疏 (f1=ID, 其余参数在 C#/Value 表中)。

### 13.2 Shield HUD 显示

```lua
function PlayerHudCtrl:PlayTweenShield(shieldValue, shieldValueMax):
  -- 非线性缩放: 小护盾 (<30% maxHP) 用 power 曲线放大显示
  scaledValue = (0.3 * shieldValue/shieldValueMax) ^ 0.5

  -- 动画: shield_in (首次出现) / shield_hit (受损) / shield_recover (恢复)
```

---

## 14. 战斗结算 (battleresultctrl.lua — 325行)

### 14.1 结算参数

```lua
function BattleResultCtrl:OnEnable():
  tbParam[1]  -- bSuccess (true=胜利)
  tbParam[2]  -- nStar (1-3)
  tbParam[3]  -- GenerRewardItems ({id, count})
  tbParam[4]  -- FirstRewardItems ({id, count, rewardType=First})
  tbParam[5]  -- ChestRewardItems ({id, count, rewardType=Three})
  tbParam[6]  -- nExp (世界等级经验)
  tbParam[10] -- nMainlineId (关卡ID, 用于显示标题)
  tbParam[11] -- tbChar (上场角色, 用于战斗结束后配音)
  tbParam[13] -- tbCharDamage (各角色伤害统计)
```

### 14.2 星级判定

三星目标文本 (`MainBattle_Task1/2/3`) 由 ConfigTable 提供。星级 `nStar` 由**服务器**返回 (根据通关时间/存活人数/其他条件判定)。

```lua
-- 3 个星星条件(最多显示3个):
for i = 1, 3:
  star_i 的文字 = ConfigTable.GetUIText("MainBattle_Task" .. i)
  star_i 的亮起 = (i <= nStar)
```

### 14.3 伤害统计面板

```lua
function OnBtnClick_ShowDamageResult():
  -- 打开 BattleDamage 面板, 显示 tbCharDamage
  -- tbCharDamage 数据结构: 每个角色 {charId, totalDamage, ...}
  EventManager.Hit(OpenPanel, PanelId.BattleDamage, self.tbCharDamage)
```

### 14.4 失败/胜利流程

```
胜利: 播胜利动画(4s) → 世界等级经验条动画 → 奖励展示(Gacha动画)
失败: 暂停逻辑 → 播失败动画(3s) → 提示文字("Battle_Result_Fail_Tip")
```

---

## 15. 自动战斗 (autobattlectrl.lua)

### 15.1 半自动模式

```lua
-- 开启: CS.AdventureModuleHelper.SetSemiAutoBattleMode(true)
--   C# 自动执行普攻+移动, 玩家手动放技能
-- 关闭: SetSemiAutoBattleMode(false)
--   完全手动

-- 自动释放必杀 (额外设置):
-- CS.UIGameSystemSetup.Instance.EnableAutoUlt 控制
-- 通过 CS.AdventureModuleHelper.SetEnableAutoUlt() 同步
```

### 15.2 状态持久化

```lua
-- 每个战斗类型独立保存:
LocalData.SetPlayerLocalData("PlayerAutoBattleState" + nType, bAuto)
-- 教程关卡: 强制关闭自动战斗
```

---

## 16. 战斗主菜单 (mainbattlemenuctrl.lua — 94行)

```
暂停/Pause    → EventManager.Hit("BattlePause")  → 打开暂停面板
小地图/MiniMap → 切换 mini<->full map, 设置 AdventureModuleHelper.MapCameraActive
```

---

## 17. 数据表总汇

| 分类 | 表名 | 行数 | 核心内容 |
|---|---|---|---|
| **技能** | `skill.bytes` | 2114 | 技能定义, Behaviour路径, CD参数, 类型(普攻/闪避/必杀) |
| | `mainskill.bytes` | ~ | 主控技能(拼盘) |
| | `secondaryskill.bytes` | ~ | 副技能(支援) |
| | `skilldamage.bytes` | ~ | 技能伤害参数 |
| **Buff** | `buff.bytes` | 2644 | Buff定义, 位掩码 |
| | `buffeffect.bytes` | 16 | Buff→效果映射 |
| | `buffvalue.bytes` | ~ | 效果值 |
| | `addbuffaction.bytes` | 4 | 动作→Buff |
| **怪物** | `monster.bytes` | 2738 | HP/ATK/DEF 基础值, 元素属性, 模型ID |
| | `monsterai.bytes` | 1035 | AI脚本, 攻击技能ID, 连招, 间隔 |
| | `monstergroup.bytes` | ~ | 怪物组/波次 |
| | `monsterskin.bytes` | ~ | 外观变体 |
| **伤害** | `hitdamage.bytes` | 1911 | 打击伤害乘区配置 |
| **护盾** | `shield.bytes` | 58 | 护盾定义 |
| **角色** | `character.bytes` | 36 | 角色基础属性, NormalAtkId, SkillId, AssistSkillId, UltimateId |
| | `characteradvance.bytes` | ~ | 突破属性 |
| | `characterskillupgrade.bytes` | ~ | 技能升级消耗 |
| **装备** | `disc.bytes` + 子表 | ~ | 碟片强化/升星/突破, 属性曲线 |
| | `potential.bytes` | ~ | 潜能 |
| | `perk.bytes` | ~ | Perk天赋 |
| | `talent.bytes` | ~ | 天赋树 |
| **战斗阈值** | `battlethreshold.bytes` | ~ | 战力/等级门槛 |
| **战令** | `battlepass.bytes` + 子表 | ~ | 战令系统 |
| **陷阱** | `trap.bytes` | ~ | 场景陷阱 |

---

## 18. 实体事件系统 (C# → Lua)

C# 战斗引擎通过 `EventManager` 向 Lua 发送实体级事件 (每个 entity 独立):

| 事件 | 触发时机 | 接收方 |
|---|---|---|
| `HpChanged(hp, hpMax)` | 角色/怪物 HP 变化 | PlayerHudCtrl / MonsterHudCtrl |
| `ShieldChanged(value, max)` | 护盾值变化 | PlayerHudCtrl / MonsterHudCtrl |
| `AmmoChanged(ammo, ammoMax)` | 弹药变化 | PlayerHudCtrl |
| `Dead` | 怪物死亡 | MonsterHudCtrl → `Deaded()` |
| `PlayerDeathStateEnter` | 玩家死亡 | PlayerHudCtrl → HUD隐藏 |
| `AttackHint` | Boss/怪物开始技能前摇 | Boss/Monster SkillHintIndicator |
| `AttackHintEnd` | 技能施放完毕 | 返回 Idle 状态 |
| `AttackHintCancel` | 技能被打断 | 立刻回到 Idle |
| `ToughnessStateChanged(broken)` | 破韧/恢复 | MonsterHudCtrl → 动画切换 |
| `ToughnessValueChanged(val, max)` | 破韧值变化 | MonsterHudCtrl → 条动画 |
| `BuffChanged` | Buff 增减 | BuffCtrl → 图标更新 |
| `BuffReduceTime` | Buff 剩余时间缩短 | PlayerHudCtrl → 闪烁提示 |

### 全局事件

| 事件 | 用途 |
|---|---|
| `MonsterHUDChange(id, type, showed)` | 怪物HUD生成/销毁 |
| `PlayerShow(id, showed)` | 玩家HUD生成/销毁 |
| `HudDamaged(id, value, isCrit, ...)` | 生成伤害浮空字 |
| `HudDotDamage(...)` | 生成 DoT 浮空字 |
| `HudHealed(id, value)` | 生成治疗浮空字 |
| `HudDefenced(id, type)` | 生成防御文字 |
| `HudBreakScore(id, value)` | Break 分数 |
| `ToughnessStateChangedForGlobal(id, broken)` | 全局破韧状态 |
| `ADVENTURE_BATTLE_MONSTER_DECLARE_DIED(id)` | 怪物宣告死亡(破韧显示清除) |
| `LevelStateChanged(state)` | Success/Failed/Teleporter |
| `ADVENTURE_LEVEL_END` | 关卡卸载, 清除所有HUD |

---

## 19. 伤害公式位置

**重要声明**: 完整的伤害计算公式在 **C# 引擎**中 (IL2CPP), Lua 侧不可见。

但从从 `TravelerDuelBattleSample` 的 proto 定义可窥见乘区结构:
```
fromSrcAtk, fromPerkIntensityRatio, fromSlotDmgRatio,
fromEE, fromGenDmgRatio, fromDmgPlus, fromCritRatio,
fromFinalDmgRatio, fromFinalDmgPlus,
toErAmend, toDefAmend, toRcdSlotDmgRatio,
toEERCD, toGenDmgRcdRatio, toDmgPlusRcd,
Dmg, CritRate, Hp
```

这表明伤害计算至少包含:
- **攻击力** (fromSrcAtk)
- **属性倍率** (fromEE, fromPerkIntensityRatio)
- **槽位伤害倍率** (fromSlotDmgRatio)
- **通用增伤** (fromGenDmgRatio, fromDmgPlus)
- **暴击** (fromCritRatio)
- **最终伤害** (fromFinalDmgRatio, fromFinalDmgPlus)
- **防御/抗性修正** (toDefAmend, toErAmend)
- **减伤** (toRcdSlotDmgRatio, toGenDmgRcdRatio, toDmgPlusRcd)

---

## 20. 代码索引

| 文件 | 行数 | 职责 |
|---|---|---|
| `battle/mainbattlectrl.lua` | 106 | 战斗主控: 管理子面板(Cinema/BossHUD/AutoBattle/Popup) |
| `battle/mainbattlepanel.lua` | 67 | 战斗面板: 加载8个prefab, 打开HUD |
| `battle/battledashboardctrl.lua` | 1000+ | 技能操作栏: 6个技能按钮 + 摇杆 + 交互提示 |
| `battle/skillbtnctrl.lua` | ~ | 技能按钮: CD/充能状态机 |
| `battle/autobattlectrl.lua` | ~ | 自动战斗: 半自动切换 |
| `battle/mainbattlemenuctrl.lua` | 94 | 战斗菜单: 暂停/地图 |
| `battle/mainbattlepausectrl.lua` | ~ | 暂停面板 |
| `battle/skillhintindicator/` | 3文件 | Boss/怪物技能预警 |
| `battle/subskilldisplay/` | 4文件 | 支援技能弹出显示 |
| `hud/hudmainctrl.lua` | 522 | HUD主控: 17种prefab加载, 事件路由 |
| `hud/playerhudctrl.lua` | 385 | 玩家HUD: HP/盾/弹药/Buff |
| `hud/monsterhudctrl.lua` | 433 | 怪物HUD: HP/盾/韧性/Buff |
| `hud/elitemonsterhudctrl.lua` | ~ | 精英怪物HUD (继承 MonsterHudCtrl) |
| `hud/buff/buffctrl.lua` | ~ | Buff图标控制器 |
| `hud/hudnumberctrl.lua` | 17 | 浮空字控制器 (空stub, C#实现) |
| `battleresult/battleresultctrl.lua` | 325 | 结算面板: 星星/经验/奖励 |
| `battleresult/battledamagectrl.lua` | ~ | 伤害统计面板 |
| `adventure/battleutils.lua` | 79 | 效果添加工具函数 |
| `dataclass/characterattrdata.lua` | ~ | 角色属性三级计算 |
| `dataclass/discdata.lua` | ~ | 碟片装备多级属性系统 |

---

## 21. 关键结论

1. **战斗中无服务器参与**: 关卡开始后, 所有实时战斗在客户端 C# 引擎执行; 服务器只在结算时接收 `BattleEndReq` (胜利/失败) 并返回奖励。

2. **伤害公式在 C#**: Lua 侧不直接计算伤害, 只负责 UI 展示。从 proto 采样结构推断公式包含 12+ 个乘区。

3. **充能制技能**: 技能不是传统 CD, 而是"充能段数"制(ChargeSectionNum), 充能满后段数+1; 必杀需 1 段充能 + 充能百分比 100% + CD为0。

4. **破韧机制**: Boss/精英有额外韧性条, 破韧后进入脆弱状态(伤害累计显示), 恢复后韧性条补满。

5. **Buff 系统**: 2644 个 Buff 定义, 16 个效果映射; 修正通过 ATTR_FIX 的三种子类型 (基础/百分比/绝对值)。

6. **6元素系统**: 属性键包含 6 种元素的伤害加成/能量效率/抗性/复合四类, 共 24+ 个属性键。<｜end▁of▁thinking｜>

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="todowrite">
<｜｜DSML｜｜parameter name="todos" string="false">[{"content":"Survey battle system: decompile 65/66 files","priority":"high","status":"completed"},{"content":"Research core battle engine: flow, skill system, damage calc","priority":"high","status":"completed"},{"content":"Research buff/debuff system","priority":"high","status":"completed"},{"content":"Research monster AI and enemy data","priority":"high","status":"completed"},{"content":"Research attribute/stat system and disc/potential effects on battle","priority":"high","status":"completed"},{"content":"Write comprehensive report at report/battle_system.md","priority":"high","status":"completed"}]