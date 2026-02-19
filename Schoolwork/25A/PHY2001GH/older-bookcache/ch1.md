
# 第一章 测量
尽管物理学中一些最复杂和抽象的理论具有数学之美，但它首先是一门实验科学。因此，至关重要的是，进行精确测量的人们能够就表达测量结果的标准达成一致，以便这些结果能够在实验室之间交流和验证。

在本章中，我们通过介绍一些物理量的基本单位及其测量的公认标准来开始我们对物理学的研究。我们考虑了表达计算和测量结果的正确方法，包括适当的量纲和有效数字位数。我们讨论并说明了关注我们方程中出现物理量的量纲的重要性。在后续章节中，其他基本单位和许多导出单位将在需要时引入。

## 1-1 物理量、标准和单位
物理定律是用许多不同的量来表达的：质量、长度、时间、力、速度、密度、电阻、温度、发光强度、磁场强度等等。这些术语中的每一个都有精确的含义，它们构成了物理学家和其他科学家相互交流的共同语言的一部分——当物理学家使用诸如"动能"这样的术语时，所有其他物理学家都会立即理解其含义。这些术语中的每一个也代表了可以在实验室中测量的量，就像必须就这些术语的含义达成一致一样，也必须就用于表达其值的单位达成一致。没有这样的共识，科学家们就不可能将他们的结果相互交流，也不可能比较来自不同实验室的实验结果。

这种比较需要制定和接受一套测量单位的标准。例如，如果长度的测量值被引用为 4.3 米，这意味着测量的长度是定义为"一米"的标准长度所接受值的 4.3 倍。如果两个实验室的测量都基于相同的公认米标准，那么它们的结果大概可以很容易地进行比较。为了实现这一点，公认的标准必须可供那些需要校准其次级标准的人使用，并且它们必须不随时间推移或环境（温度、湿度等）变化而改变。

维护和制定测量标准是科学中一个活跃的分支。在美国，国家标准与技术研究院* 承担这方面的主要责任。然而，关于标准也需要广泛的国际协议，这是通过一系列始于 1889 年的国际计量大会 达成的；第二十一届会议于 1999 年举行。**
* 关于 NIST 在维护标准方面的作用，请参见 http://physics.nist.gov/cuu。
** 关于该会议的建议，请参见 http://www.bipm.fr。

幸运的是，没有必要为每一个物理量都建立一个测量标准——有些量可以被视为基本量，而其他量的标准可以从基本量中导出。例如，长度和时间曾被视为具有各自既定标准的基本量；速度的测量标准就可以根据这些标准导出。然而，近年来，光速的测量精度已经超过了以前的标准米；因此，今天我们仍然使用秒的基本标准，但我们根据光速和秒来定义长度的标准（米）（见第 1-4 节）。这个例子说明了不断提高的测量精度如何改变既定的标准，以及这些标准如何迅速地演变。自本教科书第一版出版以来，时间标准单位（秒）的精度提高了 1000 多倍。

因此，基本问题是选择一个涉及最少数量物理量的系统作为基本量，并就其测量的可访问且不变的标准达成一致。在本章的后续章节中，我们将讨论国际公认的系统及其一些基本量。

## 1-2 国际单位制***
*** 参见 Robert A. Nelson 的《SI：国际单位制》。SI 系统的"官方"美国指南可在国家标准与技术研究院的特殊出版物 811（1995 年版）中找到。

在其各次会议上，国际计量大会选择了表 1-1 中显示的七个量作为基本单位。这是国际单位制的基础，缩写为 SI。SI 是通常所谓的公制体系的现代形式。

### 表 1-1 SI 基本单位
| 量         | SI 单位      | 符号 |
| ---------- | ------------ | ---- |
| 时间       | 秒           | s    |
| 长度       | 米           | m    |
| 质量       | 千克         | kg   |
| 物质的量   | 摩尔         | mol  |
| 热力学温度 | 开尔文       | K    |
| 电流       | 安培         | A    |
| 发光强度   | 坎德拉       | cd   |

全书我们给出了许多由表 1-1 导出的 SI 导出单位的例子，例如速度、力和电阻。例如，力的 SI 单位，称为牛顿，将根据 SI 基本单位定义，我们将在第三章中阐明：
$$1\ \text{N} = 1\ \text{kg} \cdot \text{m/s}^2$$

如果我们用 SI 单位表示物理属性，如发电厂的输出或两个核事件之间的时间间隔，我们经常会发现非常大或非常小的数字。为了方便起见，国际计量大会推荐了表 1-2 中所示的前缀。

### 表 1-2 SI 前缀****
**** 在所有情况下，第一个音节重读，如 na-no-me-ter。本书常用的前缀以粗体显示。

| 因数      | 前缀    | 符号 | 因数       | 前缀     | 符号 |
| --------- | ------- | ---- | ---------- | -------- | ---- |
| $10^{24}$ | yotta-  | Y    | $10^{-1}$  | deci-    | d    |
| $10^{21}$ | zetta-  | Z    | $10^{-2}$  | centi-   | c    |
| $10^{18}$ | exa-    | E    | $10^{-3}$  | milli-   | m    |
| $10^{15}$ | peta-   | P    | $10^{-6}$  | micro-   | $\mu$ |
| $10^{12}$ | tera-   | T    | $10^{-9}$  | nano-    | n    |
| $10^9$    | giga-   | G    | $10^{-12}$ | pico-    | p    |
| $10^6$    | mega-   | M    | $10^{-15}$ | femto-   | f    |
| $10^3$    | kilo-   | k    | $10^{-18}$ | atto-    | a    |
| $10^2$    | hecto-  | h    | $10^{-21}$ | zepto-   | z    |
| $10^1$    | deka-   | da   | $10^{-24}$ | yocto-   | y    |

因此，我们可以将一个典型发电厂的输出 $1.3 \times 10^9$ 瓦特写成 1.3 吉瓦或 1.3 GW。类似地，我们可以将在核物理中经常遇到的时间间隔 $2.35 \times 10^{-9}$ 秒写成 2.35 纳秒或 2.35 ns。如表 1-1 所示，千克是唯一一个已经包含了表 1-2 中所示前缀的 SI 基本单位。因此，1000 千克不表示为 1 千千克；而是 $10^3\ \text{kg} = 10^6\ \text{g} = 1\ \text{Mg}$。

为了完善表 1-1，我们需要七套操作程序，告诉我们如何在实验室中产生七个 SI 基本单位。我们将在接下来的三节中探讨时间、长度和质量的那些程序。

另外两个主要的单位制与国际单位制竞争。一个是高斯制，大量的物理学文献是用它来表达的。我们在本书中不使用高斯制。附录 G 给出了到 SI 单位的换算因子。

另一个是英制，在美国仍在日常使用。其基本单位，在力学中，是长度（英尺）、力（磅）和时间（秒）。附录 G 再次给出了到 SI 单位的换算因子。我们在本书中使用 SI 单位，但有时会给出英制等效值，以帮助那些不熟悉 SI 单位的人更熟悉它们。美国仍然是迄今为止唯一一个尚未采用 SI 作为其官方单位制的发达国家。然而，SI 在美国所有政府实验室和许多行业，特别是涉及外贸的行业中都是标准。1999 年 9 月火星气候轨道器航天器的损失已被追踪到是因为制造商用英制单位报告了轨道器的某些特性，而 NASA 导航团队错误地将其视为 SI 单位。仔细注意单位可能非常重要！

### 例题 1-1
任何物理量都可以乘以 1 而不改变其值。例如，1 分钟 = 60 秒，所以 $1 = 60\ \text{s}/1\ \text{min}$；类似地，1 英尺 = 12 英寸，所以 $1 = 1\ \text{ft}/12\ \text{in}$。使用适当的换算因子，求 (a) 相当于 55 英里/小时的速度，以米/秒为单位，和 (b) 一个可容纳 16 加仑汽油的油箱的体积，以立方厘米为单位。

#### 解
(a) 对于我们的换算因子，我们需要（见附录 G）$1\ \text{mi} = 1609\ \text{m}$（因此 $1 = 1609\ \text{m}/1\ \text{mi}$）和 $1\ \text{h} = 3600\ \text{s}$（因此 $1 = 1\ \text{h}/3600\ \text{s}$）。因此：
$$
\text{速度} = 55\ \frac{\text{mi}}{\text{h}} \times \frac{1609\ \text{m}}{1\ \text{mi}} \times \frac{1\ \text{h}}{3600\ \text{s}} = 25\ \text{m/s}
$$

(b) 一液量加仑是 231 立方英寸，且 $1\ \text{in.} = 2.54\ \text{cm}$。因此：
$$
\text{体积} = 16\ \text{gal} \times \frac{231\ \text{in.}^3}{1\ \text{gal}} \times \left(\frac{2.54\ \text{cm}}{1\ \text{in.}}\right)^3 = 6.1 \times 10^4\ \text{cm}^3
$$

注意在这两个计算中，单位换算因子是如何插入的，以便不需要的单位出现在一个分子和一个分母中，从而相互抵消。

## 1-3 时间标准
时间的测量有两个方面。对于民用和一些科学用途，我们想知道一天中的时间，以便我们可以按顺序排列事件。在大多数科学工作中，我们想知道一个事件持续了多长时间。因此，任何时间标准必须能够回答"它发生在什么时间？"和"它持续多长时间？"这两个问题。表 1-3 显示了可测量的时间间隔范围。它们的变化范围约为 $10^{63}$ 倍。

### 表 1-3 一些测量的时间间隔*****
***** 近似值。

| 时间间隔                              | 秒数          |
| ------------------------------------- | ------------- |
| 质子的寿命                            | $>10^{40}$    |
| $^{82}\text{Se}$ 双β衰变的半衰期      | $3 \times 10^{27}$ |
| 宇宙的年龄                            | $5 \times 10^{17}$ |
| 胡夫金字塔的年龄                      | $1 \times 10^{11}$ |
| 人类预期寿命（美国）                  | $2 \times 10^9$   |
| 地球绕太阳公转的时间（1 年）          | $3 \times 10^7$   |
| 地球绕其轴自转的时间（1 天）          | $9 \times 10^4$   |
| 典型的近地轨道卫星周期                | $5 \times 10^3$   |
| 正常心跳之间的时间                    | $8 \times 10^{-1}$ |
| 音乐会A音叉的周期                     | $2 \times 10^{-3}$ |
| 3 厘米微波的振荡周期                  | $1 \times 10^{-10}$ |
| 分子旋转的典型周期                    | $1 \times 10^{-12}$ |
| 产生的最短光脉冲（1990 年）           | $6 \times 10^{-15}$ |
| 最不稳定粒子的寿命                    | $<10^{-23}$   |

我们可以使用任何重复出现的现象作为时间的量度。测量包括计算重复次数，包括其中的分数。例如，我们可以使用振荡的摆、质量-弹簧系统或石英晶体。在自然界众多的重复现象中，地球绕其轴的自转决定了日的长度，几个世纪以来一直被用作时间标准。一（平太阳）秒被定义为（平太阳）日的 1/86,400。

基于石英晶体的电维持周期性振动的石英晶体时钟很好地充当了次级时间标准。石英钟可以通过天文观测校准到旋转的地球，并用于在实验室中测量时间。其中最好的时钟精度约为 200,000 年 1 秒，但即使这样的精度也不足以满足现代科学、技术和商业的需求。

1967 年，第 13 届国际计量大会基于铯原子发射的辐射的特征频率通过了秒的定义。具体来说，他们声明：
*秒是铯原子（特定）同位素发射的（特定）辐射的 9,192,631,770 个振动周期所持续的时间。*

图 1-1 显示了当前的国家频率标准，一种所谓的铯喷泉钟，由美国国家标准与技术研究院开发。其精度约为 2000 万年 1 秒。

### 图 1-1
国家频率标准 NIST-F1，一种所谓的铯喷泉钟，由美国国家标准与技术研究院开发。图中显示了其开发人员 Steve Jefferts 和 Dawn Meekhof。在该设备中，极慢移动的铯原子被向上投射，覆盖约一米的距离，然后在大约 1 秒内在重力作用下落回其发射位置。因此得名"喷泉"。这些投射原子的低速使得能够精确观察它们发射的原子辐射频率。更多信息，请参见 http://www.nist.gov/public_affairs/releases/n99-22.htm。

### 图 1-2
四年期间日长的变化。请注意，垂直刻度仅为 3 毫秒。参见 John Wahr 的"The Earth's Rotation Rate"。

安置在卫星中的铯钟构成了全球定位系统的基础。市面上可以买到手提箱大小的便携式铯钟。也可以购买台式钟或腕表，它们通过来自 NIST 的无线电时间信号自动定期更新，显示"原子时间"。图 1-2 显示了与铯钟相比，地球自转速率在四年期间的变化。这些数据表明，对于精密工作而言，地球自转速率是一个相对较差的时间标准。图 1-3 显示了自 1665 年克里斯蒂安·惠更斯发明摆钟以来，过去大约 300 年时间记录方面发生的令人印象深刻的改进记录。

### 图 1-3
几个世纪以来计时精度的提高。早期的摆钟每几小时快或慢一秒；现在的铯钟要几百万年后才会这样。

美国的时间记录标准维护由位于华盛顿特区的美国海军天文台负责。USNO 主钟代表了由 20 个独立的、环境受控的库房中安置的铯钟和氢脉泽组成的集合的组合输出。******
****** 关于 USNO 提供的时间服务的信息可在互联网上 http://tycho.usno.navy.mil/ 和电话 (202) 762-1401 获取。

## 1-4 长度标准*******
******* 参见 P. Giacomo 的"The New Definition of the Meter"。

第一个国际长度标准是一根铂铱合金棒，称为标准米，保存在巴黎附近的国际计量局。当棒保持在 0°C 的温度并以规定的方式机械支撑时，刻在棒两端附近的两条细线之间的距离被定义为一米。历史上，米本意是沿通过巴黎的子午线从北极到赤道距离的一千万分之一。然而，精确测量表明，标准米棒与此值略有差异（约 0.023%）。

由于标准米不易获取，因此制作了其精确的主副本并送往世界各地的标准化实验室。这些次级标准用于校准其他更易获取的测量杆。因此，直到最近，每一个测量杆或设备都是通过使用显微镜和分度机的复杂比较链从标准米获得其权威性的。自 1959 年以来，这一说法也适用于码，其在美国的法律定义于当年被采纳为：
$$1\ \text{码} = 0.9144\ \text{米（精确）}$$
这相当于 $1\ \text{英尺} = 0.3048\ \text{米（精确）}$。

使用显微镜比较细划痕的技术进行必要长度相互比较的精度已不能满足现代科学和技术的要求。当美国物理学家阿尔伯特·A·迈克耳孙在 1893 年将标准米的长度与镉原子发出的红光的波长进行比较时，获得了一种更精确和可复现的长度标准。迈克耳孙仔细测量了米棒的长度，发现标准米等于该波长的 1,553,163.5 倍。相同的镉灯可以很容易地在任何实验室获得，因此迈克耳孙找到了一种方法，让世界各地的科学家拥有精确的长度标准，而无需依赖标准米棒。

尽管有这项技术进步，金属棒仍然是官方标准，直到 1960 年，第 11 届国际计量大会采用了米的原子标准。该标准基于质量数为 86 的氪同位素原子发射的某种橙红色光在真空中的波长。具体来说，一米被定义为此光波长的 1,650,763.73 倍。使用这个标准，可以将长度比较到低于 $10^9$ 分之一的精度。

到 1983 年，对更高精度的需求达到了如此程度，以至于即使是 $^{86}\text{Kr}$ 标准也无法满足，于是在那年采取了一个大胆的步骤。米被重新定义为光波在特定时间间隔内传播的距离。用第 17 届国际计量大会的话说：
*米是光在真空中在 1/299,792,458 秒的时间间隔内所经路径的长度。*

这等价于说光速 $c$ 现在被定义为 $c = 299,792,458\ \text{m/s（精确）}$。这种对米的新定义是必要的，因为光速的测量已经变得如此精确，以至于 $^{86}\text{Kr}$ 米本身的复现性成了限制因素。鉴于此，采用光速作为一个定义量，并将其与精确定义的时间标准一起使用来重新定义米，就变得合理了。

表 1-4 显示了可与标准进行比较的测量长度范围。

### 表 1-4 一些测量的长度*********
********* 近似值。

| 长度                              | 米数          |
| --------------------------------- | ------------- |
| 到观测到的最远类星体的距离        | $2 \times 10^{26}$ |
| 到仙女座星系的距离                | $2 \times 10^{22}$ |
| 我们星系的半径                    | $6 \times 10^{19}$ |
| 到最近恒星（比邻星）的距离        | $4 \times 10^{16}$ |
| 最远行星（冥王星）的平均轨道半径  | $6 \times 10^{12}$ |
| 太阳的半径                        | $7 \times 10^8$   |
| 地球的半径                        | $6 \times 10^6$   |
| 珠穆朗玛峰的高度                  | $9 \times 10^3$   |
| 典型人的身高                      | $2 \times 10^0$   |
| 本书一页的厚度                    | $1 \times 10^{-4}$ |
| 典型病毒的大小                    | $1 \times 10^{-6}$ |
| 氢原子的半径                      | $5 \times 10^{-11}$ |
| 质子的有效半径                    | $1 \times 10^{-15}$ |

### 例题 1-2
光年是长度的度量（不是时间的度量），等于光在 1 年内传播的距离。计算光年与米之间的换算因子，并找出到比邻星的距离（$4.0 \times 10^{16}\ \text{m}$），以光年为单位。

#### 解
从年到秒的换算因子是：
$$
1\ \text{年} = 1\ \text{年} \times \frac{365.25\ \text{天}}{1\ \text{年}} \times \frac{24\ \text{小时}}{1\ \text{天}} \times \frac{60\ \text{分钟}}{1\ \text{小时}} \times \frac{60\ \text{秒}}{1\ \text{分钟}} = 3.16 \times 10^7\ \text{秒}
$$

光速，取三位有效数字，是 $3.00 \times 10^8\ \text{m/s}$。因此，在 1 年内，光传播的距离为：
$$
1\ \text{光年} = c \times t = 3.00 \times 10^8\ \text{m/s} \times 3.16 \times 10^7\ \text{秒} = 9.48 \times 10^{15}\ \text{m}
$$

到比邻星的距离是：
$$
(4.0 \times 10^{16}\ \text{m}) \times \frac{1\ \text{光年}}{9.48 \times 10^{15}\ \text{m}} = 4.2\ \text{光年}
$$

因此，从比邻星发出的光大约需要 4.2 年才能到达地球。

## 1-5 质量标准
SI 质量标准是一个铂铱圆柱体，保存在国际计量局，并通过国际协议指定其质量为 1 千克。次级标准被送往其他国家的标准化实验室，其他物体的质量可以通过等臂天平技术以 $10^8$ 分之一的精度测得。

国际质量标准在美国的副本，称为原型千克 20 号，存放在美国国家标准与技术研究院的一个库房中（见图 1-4）。它每年最多取出一次用于检查三级标准的值。自 1889 年以来，20 号原型已被带到法国两次，用于与主千克重新比较。当它从库房中取出时，总是有两个人到场，一个人用镊子拿着千克，第二个人在第一个人跌倒时接住千克。

### 图 1-4
国家标准原型千克 20 号，在其双层钟罩内，位于美国国家标准与技术研究院。

表 1-5 显示了一些测量的质量。注意它们的变化范围约为 $10^{83}$ 倍。大多数质量是通过间接方法以标准千克为单位测量的。例如，我们可以通过测量两个铅球之间的引力，并将其与地球对已知质量的吸引力进行比较，来测量地球的质量。球的质量必须通过与标准千克的直接比较来得知。

### 表 1-5 一些测量的质量**********
********** 近似值。

| 物体              | 千克数        |
| ----------------- | ------------- |
| 已知宇宙（估计）  | $10^{53}$     |
| 我们的星系        | $2 \times 10^{43}$ |
| 太阳              | $2 \times 10^{30}$ |
| 地球              | $6 \times 10^{24}$ |
| 月球              | $7 \times 10^{22}$ |
| 远洋轮船          | $7 \times 10^7$   |
| 大象              | $4 \times 10^3$   |
| 人                | $6 \times 10^1$   |
| 葡萄              | $3 \times 10^{-3}$ |
| 尘埃斑点          | $7 \times 10^{-10}$ |
| 病毒              | $1 \times 10^{-15}$ |
| 青霉素分子        | $5 \times 10^{-17}$ |
| 铀原子            | $4 \times 10^{-26}$ |
| 质子              | $2 \times 10^{-27}$ |
| 电子              | $9 \times 10^{-31}$ |

在原子尺度上，我们有第二个质量标准，它不是 SI 单位。它是 $^{12}\text{C}$ 原子的质量，根据国际协议，被精确地、通过定义指定为 12 统一原子质量单位。我们可以使用质谱仪相当准确地找到其他原子的质量。表 1-6 显示了一些选定的原子质量，包括估计的测量不确定度。我们需要第二个质量标准，因为目前的实验室技术允许我们将原子质量彼此比较的精度高于我们目前将它们与标准千克比较的精度。然而，用原子质量标准取代标准千克的开发正在进行中。当前原子标准与主要标准之间的关系近似为：
$$1\ \text{u} = 1.661 \times 10^{-27}\ \text{kg}$$

### 表 1-6 一些测量的原子质量
| 同位素    | 质量 (u)        | 不确定度 (u)     |
| --------- | --------------- | ---------------- |
| $^1\text{H}$  | 1.00782503214   | 0.00000000035    |
| $^{12}\text{C}$ | 12.00000000     | （精确）         |
| $^{64}\text{Cu}$ | 63.9297679      | 0.0000015        |
| $^{109}\text{Ag}$ | 108.9047551     | 0.0000032        |
| $^{137}\text{Cs}$ | 136.9070836     | 0.0000032        |
| $^{208}\text{Pb}$ | 207.9766358     | 0.0000031        |
| $^{238}\text{Pu}$ | 238.0495534     | 0.0000022        |

一个相关的 SI 单位是摩尔，它测量物质的量。一摩尔 $^{12}\text{C}$ 原子的质量正好是 12 克，并且包含的原子数在数值上等于阿伏伽德罗常数 $N_A$：
$$N_A = 6.02214199 \times 10^{23}\ \text{每摩尔}$$

这是一个实验确定的数字，不确定度约为百万分之一。任何其他物质的一摩尔包含相同数量的基本实体（原子、分子等）。因此，1 摩尔氦气包含 $N_A$ 个 He 原子，1 摩尔氧气包含 $N_A$ 个 $O_2$ 分子，1 摩尔水包含 $N_A$ 个 $H_2O$ 分子。

要将原子质量单位与宏观单位联系起来，必须使用阿伏伽德罗常数。用原子标准取代标准千克将需要将 $N_A$ 测量值的精度至少提高两个数量级，以获得 $10^8$ 分之一的精度。

## 1-6 精度和有效数字
当我们进行测量时，我们永远不能确定我们获得的值是所测量量的"真"值。相反，我们只能估计真值可能存在的范围。例如，如果我们测量一张桌子的长度为 3 米，我们相当确定真实长度在 2 米到 4 米之间。如果我们更精确地测量它为 3.14159 米，我们的意思是真实长度可能在 3.14158 米到 3.14160 米之间。

随着我们改进测量仪器的质量和技术的复杂性，我们可以在不断提高的精度水平上进行实验；也就是说，我们可以将测量结果扩展到更多位有效数字，并相应地减少结果的实验不确定度。有效数字的位数和不确定度都告诉了我们关于对结果精度的估计。

在呈现测量和计算结果时，注意有效数字很重要，包含过多位数和过少位数同样是错误的。如果你将一个长度表示为 3 米，而实际上你确实认为它是 3.14159 米，那么你就是在隐瞒可能重要的信息。另一方面，如果你将它表示为 3.14159 米，而你真的除了知道它大约是 3 米之外没有任何依据，那么你声称拥有比你实际拥有的更多信息，就有点不诚实了。

在决定保留多少位有效数字时，有几个简单的规则要遵循：

1.  **计算有效数字**：从左开始计数，忽略前导零，保留所有数字直到第一个可疑数字。例如，$x = 3\ \text{m}$ 只有一位有效数字，将此值表示为 $x = 0.003\ \text{km}$ 不会改变有效数字的位数。如果我们改为写 $x = 3.0\ \text{m}$，则意味着我们知道这个值有两位有效数字。特别要注意，不要记下计算器显示的所有 9 或 10 位数字，如果输入数据的精度不足以证明这一点！本书中的大多数计算都是使用两位或三位有效数字完成的。

2.  **模糊表示法**：注意模糊表示法。例如，$x = 300\ \text{m}$ 没有表明是有一位、两位还是三位有效数字；我们不知道这些零是携带信息还是仅仅作为占位符。相反，我们通过写 $x = 3 \times 10^2$、$3.0 \times 10^2$ 或 $3.00 \times 10^2$ 来分别表示一位、两位或三位有效数字，从而更清楚地指定精度。

3.  **乘法和除法**：当相乘或相除时，乘积或商中的有效数字位数不应大于因子中精度最低的那个的有效数字位数。例如：
    $$2.3 \times 3.14159 = 7.2$$
    (2.3 有两位有效数字，所以结果四舍五入到两位有效数字。)

    在应用此规则时，偶尔需要一点良好的判断力。例如：
    $$9.8 \times 1.03 = 10.1$$
    尽管 9.8 技术上只有两位有效数字，但它非常接近具有三位有效数字的数字。因此，乘积应表示为三位有效数字。

4.  **加法和减法**：在加法或减法中，和或差的最低有效数字位占据与所加或所减量的最低有效数字位相同的位置。在这种情况下，有效数字的位数并不重要；重要的是位置。例如，假设我们希望如下找到三个物体的总质量：
    $$
    \begin{align*}
    &104.0\ \text{kg} \quad (\text{最低有效数字在十分位}) \\
    &+ \quad 2.10\ \text{kg} \quad (\text{最低有效数字在百分位}) \\
    &+ \quad 0.319\ \text{kg} \quad (\text{最低有效数字在千分位}) \\
    \hline
    &106.419\ \text{kg} \quad (\text{四舍五入为 106.4 kg，最低有效数字在十分位})
    \end{align*}
    $$
    根据规则 1，我们应该只包含一个可疑数字；因此结果应表示为 106.4 kg，因为如果"4"（在十分位）是可疑的，那么后面的"19"不提供任何信息，是无用的。

### 例题 1-3
你想称你的宠物猫的体重，但你只有一台普通的家用台秤。它是一个数字秤，以整磅数显示你的体重。因此你采用以下方案：你确定自己的体重为 119 磅，然后抱着猫发现你们的组合体重为 128 磅。你的体重和猫的体重的分数不确定度或百分比不确定度是多少？

#### 解
最低有效数字是个位，因此你的体重不确定度约为 1 磅。也就是说，对于 118.5 到 119.5 磅之间的任何体重，你的秤都会显示 119 磅。因此，分数不确定度为：
$$
\frac{1\ \text{lb}}{119\ \text{lb}} = 0.008\ \text{或}\ 0.8\%
$$

猫的体重是 $128\ \text{lb} - 119\ \text{lb} = 9\ \text{lb}$。然而，猫体重的不确定度仍然约为 1 磅，因此分数不确定度为：
$$
\frac{1\ \text{lb}}{9\ \text{lb}} = 0.11\ \text{或}\ 11\%
$$

尽管你的体重和猫的体重的绝对不确定度相同，但你体重的相对不确定度比猫体重的相对不确定度小一个数量级。如果你试图用这种方法称一只 1 磅重的小猫，其体重的相对不确定度将是 100%。这说明了在减去两个几乎相等的数字时经常出现的危险：差值的相对或百分比不确定度可能非常大。

## 1-7 量纲分析
与每一个测量或计算的量相关联的是一个量纲。例如， enclosure 对声音的吸收和核反应发生的概率都具有面积的量纲。表示这些量的单位不影响量的量纲：无论面积是用 $m^2$、$ft^2$、英亩、赛宾还是靶恩表示，它仍然是面积。

正如我们在本章前面将我们的测量标准定义为基本量一样，我们可以基于独立的测量标准选择一组基本量纲。对于力学量，质量、长度和时间是基本且独立的，因此它们可以作为基本量纲。它们分别用 M、L 和 T 表示。

任何方程在量纲上必须一致；也就是说，两边的量纲必须相同。注意量纲常常可以使你避免在写方程时出错。例如，一个从静止开始并在恒定加速度 $a$ 下运动的物体在时间 $t$ 内覆盖的距离 $x$ 将在下一章中显示为 $x = \frac{1}{2}at^2$。加速度以 $m/s^2$ 等单位测量，因此其量纲为 $[a] = L/T^2$。$x$ 的量纲是 $[x] = L$，而 $at^2$ 的量纲是 $[a][t^2] = (L/T^2)(T^2) = L$，这与 $x$ 的量纲匹配。记住加速度的量纲，因此你永远不会被诱惑写成 $x = \frac{1}{2}at$ 或 $x = \frac{1}{2}at^3$。

量纲分析通常有助于推导方程。以下两个例题说明了这个过程。

### 例题 1-4
使物体以恒定速度在圆周上运动需要一个称为"向心力"的力。对向心力进行量纲分析。

#### 解
我们首先问"向心力 $F$ 可能依赖于哪些力学变量？"运动物体只有三个可能重要的属性：它的质量 $m$、它的速度 $v$ 和它的圆形路径的半径 $r$。因此，向心力 $F$ 必须由以下形式的方程给出：
$$F \propto m^a v^b r^c$$
其中符号 $\propto$ 表示"正比于"，$a$、$b$ 和 $c$ 是通过分析量纲确定的数值指数。

正如我们在第 1-2 节中写的，力具有 $kg \cdot m/s^2$ 的单位，所以它的量纲是 $[F] = MLT^{-2}$。其他量的量纲是 $[m] = M$，$[v] = LT^{-1}$，和 $[r] = L$。因此，我们可以用量纲写出向心力方程：
$$MLT^{-2} = [m^a v^b r^c] = [m]^a [v]^b [r]^c = M^a (LT^{-1})^b L^c = M^a L^{b+c} T^{-b}$$

量纲一致性意味着基本量纲在两边必须相同。因此，令每个基本量纲的指数相等：
- M 的指数：$a = 1$
- T 的指数：$-b = -2$ ⇒ $b = 2$
- L 的指数：$b + c = 1$ ⇒ $2 + c = 1$ ⇒ $c = -1$

得到的表达式是 $F \propto m v^2 r^{-1}$ 或 $F \propto \frac{m v^2}{r}$。

向心力的实际表达式，从牛顿定律和圆周运动的几何推导出来，是 $F = \frac{m v^2}{r}$。量纲分析给出了对力学变量的精确依赖关系！这真是一个幸运的巧合，因为量纲分析无法告诉我们关于任何无量纲常数的信息。在这种情况下，常数恰好是 1。

### 例题 1-5
大爆炸之后宇宙演化中的一个重要里程碑是普朗克时间 $t_P$，其值取决于三个基本常数：(1) 光速，$c = 3.00 \times 10^8\ \text{m/s}$；(2) 牛顿引力常数，$G = 6.67 \times 10^{-11}\ \text{m}^3/(s^2 \cdot kg)$；(3) 普朗克常数，$h = 6.63 \times 10^{-34}\ \text{kg} \cdot m^2/s$。基于量纲分析，求普朗克时间的值。

#### 解
使用给出的三个常数的单位，我们可以得到它们的量纲：
- $[c] = LT^{-1}$
- $[G] = L^3 M^{-1} T^{-2}$
- $[h] = ML^2 T^{-1}$

令普朗克时间依赖于这些常数，形式为 $t_P \propto c^i G^j h^k$，其中 $i$、$j$ 和 $k$ 是待确定的指数。这个表达式的量纲是：
$$
[t_P] = [c^i G^j h^k] = [c]^i [G]^j [h]^k = (LT^{-1})^i (L^3 M^{-1} T^{-2})^j (ML^2 T^{-1})^k
$$

时间的量纲是 $[t_P] = T$，因此我们可以令两边的量纲相等：
$$
T = L^i T^{-i} \times L^{3j} M^{-j} T^{-2j} \times M^k L^{2k} T^{-k} = M^{-j + k} L^{i + 3j + 2k} T^{-i - 2j - k}
$$

令两边每个基本量纲的指数相等：
1.  M 的指数：$-j + k = 0$ ⇒ $k = j$
2.  L 的指数：$i + 3j + 2k = 0$。由于 $k = j$，这变为 $i + 3j + 2j = i + 5j = 0$ ⇒ $i = -5j$
3.  T 的指数：$-i - 2j - k = 1$。代入 $i = -5j$ 和 $k = j$，我们得到 $-(-5j) - 2j - j = 5j - 2j - j = 2j = 1$ ⇒ $j = \frac{1}{2}$

因此：
- $j = \frac{1}{2}$
- $k = j = \frac{1}{2}$
- $i = -5j = -\frac{5}{2}$

因此，普朗克时间正比于 $c^{-5/2} G^{1/2} h^{1/2}$，或：
$$
t_P \propto \sqrt{\frac{G h}{c^5}}
$$

代入 $G$、$h$ 和 $c$ 的数值：
$$
t_P = \sqrt{\frac{(6.67 \times 10^{-11}\ \text{m}^3/(s^2 \cdot kg))(6.63 \times 10^{-34}\ \text{kg} \cdot m^2/s)}{(3.00 \times 10^8\ \text{m/s})^5}} = 1.35 \times 10^{-45}\ \text{s}
$$

通常定义的普朗克时间与此值相差一个因子 $(2\pi)^{-1/2}$。这种无量纲因子无法通过此技术找到。

以类似的方式，我们可以确定普朗克长度和普朗克质量，它们也具有非常基本的解释。



# CHAPTER 1 MEASUREMENT
Despite the mathematical beauty of some of its most complex and abstract theories, physics is above all an experimental science. It is therefore critical that those who make precise measurements be able to agree on standards in which to express the results of those measurements, so that they can be communicated from one laboratory to another and verified.

In this chapter we begin our study of physics by introducing some of the basic units of physical quantities and the standards that have been accepted for their measurement. We consider the proper way to express the results of calculations and measurements, including the appropriate dimensions and number of significant figures. We discuss and illustrate the importance of paying attention to the dimensions of the quantities that appear in our equations. Later in the text, other basic units and many derived units are introduced as they are needed.

## 1-1 PHYSICAL QUANTITIES, STANDARDS, AND UNITS
The laws of physics are expressed in terms of many different quantities: mass, length, time, force, speed, density, resistance, temperature, luminous intensity, magnetic field strength, and many more. Each of these terms has a precise meaning, and they form part of the common language that physicists and other scientists use to communicate with one another—when a physicist uses a term such as “kinetic energy,” all other physicists will immediately understand what is meant. Each of these terms also represents a quantity that can be measured in the laboratory, and just as there must be agreement on the meaning of these terms, there must also be agreement about the units used to express their values. Without such agreement, it would not be possible for scientists to communicate their results to one another or to compare the results of experiments from different laboratories.

Such comparisons require the development and acceptance of a set of standards for units of measurement. For example, if a measurement of length is quoted as 4.3 meters, it means that the measured length is 4.3 times as long as the value accepted for a standard length defined to be “one meter.” If two laboratories base their measurements on the same accepted standard for the meter, then presumably their results can be easily compared. For this to be possible, the accepted standards must be accessible to those who need to calibrate their secondary standards, and they must be invariable to change with the passage of time or with changes in their environment (temperature, humidity, etc.).

Maintaining and developing standards for measurement is an active branch of science. In the United States, the National Institute of Standards and Technology* (NIST) has the primary responsibility for this development. However, it is also necessary to have wide international agreement about standards, which has been accomplished through a series of international meetings of the General Conference on Weights and Measures (known by their French acronym CGPM) beginning in 1889; the twenty-first meeting was held in 1999.**
* See http://physics.nist.gov/cuu for information about NIST’s role in maintaining standards.
** See http://www.bipm.fr for the recommendations of this conference.

Fortunately, it is not necessary to establish a measurement standard for every physical quantity—some quantities can be regarded as fundamental, and the standards for other quantities can be derived from the fundamental ones. For example, length and time were once regarded as fundamental quantities with their individual established standards (respectively the meter and the second); the measurement standard for speed (length/time) could then be derived in terms of those standards. However, in more recent years the speed of light has been measured to a precision exceeding that of the former standard meter; as a result, today we still use a fundamental standard for the second, but we define the standard for length (the meter) in terms of the speed of light and the second (see Section 1-4). This case illustrates how measurements of increasing precision can change the established standards and how rapidly such standards evolve. Since the publication of the first edition of this textbook, the precision of the standard unit for time (the second) has improved by more than a factor of 1000.

The basic problem therefore is to choose a system involving the smallest number of physical quantities as fundamental and to agree on accessible and invariable standards for their measurement. In the next sections of this chapter we discuss the internationally accepted system and some of its fundamental quantities.

## 1-2 THE INTERNATIONAL SYSTEM OF UNITS***
*** See “SI: The International System of Units,” by Robert A. Nelson (American Association of Physics Teachers, 1981). The “official” U.S. guide to the SI system can be found in Special Publication 811 of the National Institute of Standards and Technology (1995 edition).

At its various meetings, the General Conference on Weights and Measures selected as base units the seven quantities displayed in Table 1-1. This is the basis of the International System of Units, abbreviated SI from the French Le Système International d’Unités. SI is the modern form of what is known generally as the metric system.

### Table 1-1 SI Base Units
| Quantity | SI Unit | Symbol |
| --- | --- | --- |
| Time | second | s |
| Length | meter | m |
| Mass | kilogram | kg |
| Amount of substance | mole | mol |
| Thermodynamic temperature | kelvin | K |
| Electric current | ampere | A |
| Luminous intensity | candela | cd |

Throughout the book we give many examples of SI derived units, such as speed, force, and electric resistance, that follow from Table 1-1. For example, the SI unit of force, called the newton (abbreviation N), is defined in terms of the SI base units as we shall make clear in Chapter 3:
$$1\ \text{N} = 1\ \text{kg} \cdot \text{m/s}^2$$

If we express physical properties such as the output of a power plant or the time interval between two nuclear events in SI units, we often find very large or very small numbers. For convenience, the General Conference on Weights and Measures recommended the prefixes shown in Table 1-2.

### Table 1-2 SI Prefixes****
**** In all cases, the first syllable is accented, as in na-no-me-ter. Prefixes commonly used in this book are shown in boldface type.

| Factor | Prefix | Symbol | Factor | Prefix | Symbol |
| --- | --- | --- | --- | --- | --- |
| $10^{24}$ | yotta- | Y | $10^{-1}$ | deci- | d |
| $10^{21}$ | zetta- | Z | $10^{-2}$ | centi- | c |
| $10^{18}$ | exa- | E | $10^{-3}$ | milli- | m |
| $10^{15}$ | peta- | P | $10^{-6}$ | micro- | $\mu$ |
| $10^{12}$ | tera- | T | $10^{-9}$ | nano- | n |
| $10^9$ | giga- | G | $10^{-12}$ | pico- | p |
| $10^6$ | mega- | M | $10^{-15}$ | femto- | f |
| $10^3$ | kilo- | k | $10^{-18}$ | atto- | a |
| $10^2$ | hecto- | h | $10^{-21}$ | zepto- | z |
| $10^1$ | deka- | da | $10^{-24}$ | yocto- | y |

Thus we can write the output of a typical electrical power plant, $1.3 \times 10^9$ watts, as 1.3 gigawatts or 1.3 GW. Similarly, we can write a time interval of the size often encountered in nuclear physics, $2.35 \times 10^{-9}$ seconds, as 2.35 nanoseconds or 2.35 ns. As Table 1-1 shows, the kilogram is the only SI base unit that already incorporates one of the prefixes displayed in Table 1-2. Thus 1000 kg is not expressed as 1 kilokilogram; instead, $10^3\ \text{kg} = 10^6\ \text{g} = 1\ \text{Mg}$ (megagram).

To fortify Table 1-1 we need seven sets of operational procedures that tell us how to produce the seven SI base units in the laboratory. We explore those for time, length, and mass in the next three sections.

Two other major systems of units compete with the International System (SI). One is the Gaussian system, in terms of which much of the literature of physics is expressed. We do not use the Gaussian system in this book. Appendix G gives conversion factors to SI units.

The other is the British system, still in daily use in the United States. The basic units, in mechanics, are length (the foot), force (the pound), and time (the second). Again Appendix G gives conversion factors to SI units. We use SI units in this book, but we sometimes give the British equivalents, to help those who are unaccustomed to SI units to acquire more familiarity with them. The United States continues to be the only developed country that, so far, has not adopted SI as its official unit system. However, SI is standard in all U.S. government laboratories and in many industries, especially those involved in foreign trade. The loss of the Mars Climate Orbiter spacecraft in September 1999 has been traced to the fact that the manufacturer reported some of the Orbiter’s characteristics in British units, which the NASA navigation team mistakenly took to be SI units. Careful attention to units can be very important!

### Sample Problem 1-1
Any physical quantity can be multiplied by 1 without changing its value. For example, 1 min = 60 s, so $1 = 60\ \text{s}/1\ \text{min}$; similarly, 1 ft = 12 in., so $1 = 1\ \text{ft}/12\ \text{in}$. Using appropriate conversion factors, find (a) the speed in meters per second equivalent to 55 miles per hour, and (b) the volume in cubic centimeters of a tank that holds 16 gallons of gasoline.

#### Solution
(a) For our conversion factors, we need (see Appendix G) $1\ \text{mi} = 1609\ \text{m}$ (so that $1 = 1609\ \text{m}/1\ \text{mi}$) and $1\ \text{h} = 3600\ \text{s}$ (so $1 = 1\ \text{h}/3600\ \text{s}$). Thus:
$$
\text{speed} = 55\ \frac{\text{mi}}{\text{h}} \times \frac{1609\ \text{m}}{1\ \text{mi}} \times \frac{1\ \text{h}}{3600\ \text{s}} = 25\ \text{m/s}
$$

(b) One fluid gallon is 231 cubic inches, and $1\ \text{in.} = 2.54\ \text{cm}$. Thus:
$$
\text{volume} = 16\ \text{gal} \times \frac{231\ \text{in.}^3}{1\ \text{gal}} \times \left(\frac{2.54\ \text{cm}}{1\ \text{in.}}\right)^3 = 6.1 \times 10^4\ \text{cm}^3
$$

Note in these two calculations how the unit conversion factors are inserted so that the unwanted units appear in one numerator and one denominator, and thus cancel.

## 1-3 THE STANDARD OF TIME
The measurement of time has two aspects. For civil and for some scientific purposes we want to know the time of day so that we can order events in sequence. In most scientific work we want to know how long an event lasts (the time interval). Thus any time standard must be able to answer the questions “At what time does it occur?” and “How long does it last?” Table 1-3 shows the range of time intervals that can be measured. They vary by a factor of about $10^{63}$.

### Table 1-3 Some Measured Time Intervals*****
***** Approximate values.

| Time Interval | Seconds |
| --- | --- |
| Lifetime of proton | $>10^{40}$ |
| Half-life of double beta decay of $^{82}\text{Se}$ | $3 \times 10^{27}$ |
| Age of universe | $5 \times 10^{17}$ |
| Age of pyramid of Cheops | $1 \times 10^{11}$ |
| Human life expectancy (U.S.) | $2 \times 10^9$ |
| Time of Earth's orbit around the Sun (1 year) | $3 \times 10^7$ |
| Time of Earth's rotation about its axis (1 day) | $9 \times 10^4$ |
| Period of typical low-orbit Earth satellite | $5 \times 10^3$ |
| Time between normal heartbeats | $8 \times 10^{-1}$ |
| Period of concert-A tuning fork | $2 \times 10^{-3}$ |
| Period of oscillation of 3-cm microwaves | $1 \times 10^{-10}$ |
| Typical period of rotation of a molecule | $1 \times 10^{-12}$ |
| Shortest light pulse produced (1990) | $6 \times 10^{-15}$ |
| Lifetime of least stable particles | $<10^{-23}$ |

We can use any phenomenon that repeats itself as a measure of time. The measurement consists of counting the repetitions, including the fractions thereof. We could use an oscillating pendulum, a mass–spring system, or a quartz crystal, for example. Of the many repetitive phenomena in nature the rotation of the Earth on its axis, which determines the length of the day, was used as a time standard for centuries. One (mean solar) second was defined to be 1/86,400 of a (mean solar) day.

Quartz crystal clocks based on the electrically sustained periodic vibrations of a quartz crystal serve well as secondary time standards. A quartz clock can be calibrated against the rotating Earth by astronomical observations and used to measure time in the laboratory. The best of these have kept time with a precision of about 1 second in 200,000 years, but even this precision is not sufficient for the demands of modern science, technology, and commerce.

In 1967, the 13th General Conference on Weights and Measures adopted a definition of the second based on a characteristic frequency of the radiation emitted by a cesium atom. In particular, they stated that:
*The second is the duration of 9,192,631,770 vibrations of a (specified) radiation emitted by a (specified) isotope of the cesium atom.*

Figure 1-1 shows the current national frequency standard, a so-called cesium fountain clock developed at the National Institute of Standards and Technology (NIST). Its precision is about 1 second in 20 million years.

### Figure 1-1
The National Frequency Standard NIST-F1, a so-called cesium fountain clock, developed at the National Institute of Standards and Technology. It is shown with its developers, Steve Jefferts and Dawn Meekhof. In this device extremely slow-moving cesium atoms are projected upward, covering a distance of about a meter before falling back under gravity to their launch position in about 1 second. Hence the label “fountain.” The small speeds of these projected atoms make possible precise observation of the frequency of the atomic radiation that they emit. For more information, see http://www.nist.gov/public_affairs/releases/n99-22.htm.

### Figure 1-2
The variation in the length of the day over a 4-year period. Note that the vertical scale is only 3 ms ($3\ \text{ms} = 0.003\ \text{s}$). See “The Earth’s Rotation Rate,” by John Wahr, American Scientist, January–February 1985, p. 41.

Cesium clocks housed in satellites form the basis of the Global Positioning System. Portable cesium clocks the size of a suitcase are commercially available. It is also possible to purchase desk-top clocks or wrist watches that, automatically and periodically updated by radio time signals from NIST, display “atomic time.” Figure 1-2 shows, by comparison with a cesium clock, variations in the rate of rotation of the Earth over a 4-year period. These data suggest what a relatively poor time standard the Earth’s rotation rate provides for precise work. Figure 1-3 shows the impressive record of improvements in time-keeping that have occurred over the past 300 years or so, starting with the invention of the pendulum clock by Christian Huygens in 1665.

### Figure 1-3
The improvement in timekeeping over the centuries. Early pendulum clocks gained or lost a second every few hours; present cesium clocks would do so only after several million years.

The maintenance of timekeeping standards in the United States is the responsibility of the U.S. Naval Observatory (USNO) in Washington, DC. The USNO Master Clock represents the combined output of an assembly of cesium clocks and hydrogen masers housed in 20 separate, environmentally controlled vaults.******
****** Information about time services provided by the USNO is available on the Internet at http://tycho.usno.navy.mil/ and by telephone at (202) 762-1401.

## 1-4 THE STANDARD OF LENGTH*******
******* See “The New Definition of the Meter,” by P. Giacomo, American Journal of Physics, July 1984, p. 607.

The first international standard of length was a bar of a platinum–iridium alloy called the standard meter, which was kept at the International Bureau of Weights and Measures near Paris. The distance between two fine lines engraved near the ends of the bar, when the bar was held at a temperature of 0°C and supported mechanically in a prescribed way, was defined to be one meter. Historically, the meter was intended to be one ten-millionth of the distance from the north pole to the equator along the meridian line through Paris. However, accurate measurements showed that the standard meter bar differs slightly (about 0.023%) from this value.

Because the standard meter is not very accessible, accurate master copies of it were made and sent to standardized laboratories throughout the world. These secondary standards were used to calibrate other, still more accessible, measuring rods. Thus, until recently, every measuring rod or device derived its authority from the standard meter through a complicated chain of comparisons using microscopes and dividing engines. Since 1959 this statement had also been true for the yard, whose legal definition in the United States was adopted in that year to be:
$$1\ \text{yard} = 0.9144\ \text{meter (exactly)}$$
which is equivalent to $1\ \text{ft} = 0.3048\ \text{meter (exactly)}$.

The accuracy with which the necessary intercomparisons of length can be made by the technique of comparing fine scratches using a microscope is no longer satisfactory for modern science and technology. A more precise and reproducible standard of length was obtained when the American physicist Albert A. Michelson in 1893 compared the length of the standard meter with the wavelength of the red light emitted by atoms of cadmium. Michelson carefully measured the length of the meter bar and found that the standard meter was equal to 1,553,163.5 of those wavelengths. Identical cadmium lamps could easily be obtained in any laboratory, and thus Michelson found a way for scientists around the world to have a precise standard of length without relying on the standard meter bar.

Despite this technological advance, the metal bar remained the official standard until 1960, when the 11th General Conference on Weights and Measures adopted an atomic standard for the meter. This standard was based on the wavelength in vacuum of a certain orange-red light emitted by atoms of the isotope of krypton with mass number 86, identified by the symbol $^{86}\text{Kr}$.******** Specifically, one meter was defined to be 1,650,763.73 wavelengths of this light. Using this standard, it became possible to compare lengths to a precision below 1 part in $10^9$.
******** The mass number is the total number of protons plus neutrons in the nucleus. Naturally occurring krypton has several different isotopes, corresponding to atoms with different mass numbers. It is important to specify a particular isotope for the standard, because the wavelength of the chosen radiation will vary from one isotope to another by about 1 part in $10^5$, which is unacceptably large in comparison with the precision of the standard.

By 1983, the demands for higher precision had reached such a point that even the $^{86}\text{Kr}$ standard could not meet them and in that year a bold step was taken. The meter was redefined as the distance traveled by a light wave in a specified time interval. In the words of the 17th General Conference on Weights and Measures:
*The meter is the length of the path traveled by light in vacuum during a time interval of 1/299,792,458 of a second.*

This is equivalent to saying that the speed of light $c$ is now defined as $c = 299,792,458\ \text{m/s (exactly)}$. This new definition of the meter was necessary because measurements of the speed of light had become so precise that the reproducibility of the $^{86}\text{Kr}$ meter itself became the limiting factor. In view of this, it then made sense to adopt the speed of light as a defined quantity and to use it along with the precisely defined standard of time (the second) to redefine the meter.

Table 1-4 shows the range of measured lengths that can be compared with the standard.

### Table 1-4 Some Measured Lengths*********
********* Approximate values.

| Length | Meters |
| --- | --- |
| Distance to the farthest observed quasar | $2 \times 10^{26}$ |
| Distance to the Andromeda galaxy | $2 \times 10^{22}$ |
| Radius of our galaxy | $6 \times 10^{19}$ |
| Distance to the nearest star (Proxima Centauri) | $4 \times 10^{16}$ |
| Mean orbit radius for the most distant planet (Pluto) | $6 \times 10^{12}$ |
| Radius of the Sun | $7 \times 10^8$ |
| Radius of the Earth | $6 \times 10^6$ |
| Height of Mt. Everest | $9 \times 10^3$ |
| Height of a typical person | $2 \times 10^0$ |
| Thickness of a page in this book | $1 \times 10^{-4}$ |
| Size of a typical virus | $1 \times 10^{-6}$ |
| Radius of a hydrogen atom | $5 \times 10^{-11}$ |
| Effective radius of a proton | $1 \times 10^{-15}$ |

### Sample Problem 1-2
A light-year is a measure of length (not a measure of time) equal to the distance that light travels in 1 year. Compute the conversion factor between light-years and meters, and find the distance to the star Proxima Centauri ($4.0 \times 10^{16}\ \text{m}$) in light-years.

#### Solution
The conversion factor from years to seconds is:
$$
1\ \text{y} = 1\ \text{y} \times \frac{365.25\ \text{d}}{1\ \text{y}} \times \frac{24\ \text{h}}{1\ \text{d}} \times \frac{60\ \text{min}}{1\ \text{h}} \times \frac{60\ \text{s}}{1\ \text{min}} = 3.16 \times 10^7\ \text{s}
$$

The speed of light is, to three significant figures, $3.00 \times 10^8\ \text{m/s}$. Thus in 1 year, light travels a distance of:
$$
1\ \text{ly} = c \times t = 3.00 \times 10^8\ \text{m/s} \times 3.16 \times 10^7\ \text{s} = 9.48 \times 10^{15}\ \text{m}
$$

The distance to Proxima Centauri is:
$$
(4.0 \times 10^{16}\ \text{m}) \times \frac{1\ \text{light-year}}{9.48 \times 10^{15}\ \text{m}} = 4.2\ \text{light-years}
$$

Light from Proxima Centauri thus takes about 4.2 years to travel to Earth.

## 1-5 THE STANDARD OF MASS
The SI standard of mass is a platinum–iridium cylinder kept at the International Bureau of Weights and Measures and assigned, by international agreement, a mass of 1 kilogram. Secondary standards are sent to standardizing laboratories in other countries and the masses of other bodies can be found by an equal-arm balance technique to a precision of 1 part in $10^8$.

The U.S. copy of the international standard of mass, known as Prototype Kilogram No. 20, is housed in a vault at the National Institute of Standards and Technology (see Fig. 1-4). It is removed no more than once a year for checking the values of tertiary standards. Since 1889 Prototype No. 20 has been taken to France twice for recomparison with the master kilogram. When it is removed from the vault two people are always present, one to carry the kilogram in a pair of forceps, the second to catch the kilogram if the first person should fall.

### Figure 1-4
The National Standard Prototype Kilogram No. 20, resting in its double bell jar at the U.S. National Institute of Standards and Technology.

Table 1-5 shows some measured masses. Note that they vary by a factor of about $10^{83}$. Most masses have been measured in terms of the standard kilogram by indirect methods. For example, we can measure the mass of the Earth (see Section 14-3) by measuring in the laboratory the gravitational force of attraction between two lead spheres and comparing it with the attraction of the Earth for a known mass. The masses of the spheres must be known by direct comparison with the standard kilogram.

### Table 1-5 Some Measured Masses**********
********** Approximate values.

| Object | Kilograms |
| --- | --- |
| Known universe (estimate) | $10^{53}$ |
| Our galaxy | $2 \times 10^{43}$ |
| Sun | $2 \times 10^{30}$ |
| Earth | $6 \times 10^{24}$ |
| Moon | $7 \times 10^{22}$ |
| Ocean liner | $7 \times 10^7$ |
| Elephant | $4 \times 10^3$ |
| Person | $6 \times 10^1$ |
| Grape | $3 \times 10^{-3}$ |
| Speck of dust | $7 \times 10^{-10}$ |
| Virus | $1 \times 10^{-15}$ |
| Penicillin molecule | $5 \times 10^{-17}$ |
| Uranium atom | $4 \times 10^{-26}$ |
| Proton | $2 \times 10^{-27}$ |
| Electron | $9 \times 10^{-31}$ |

On the atomic scale we have a second standard of mass, which is not an SI unit. It is the mass of the $^{12}\text{C}$ atom, which, by international agreement, has been assigned an atomic mass of 12 unified atomic mass units (abbreviation u), exactly and by definition. We can find the masses of other atoms to considerable accuracy by using a mass spectrometer (see Section 32-2). Table 1-6 shows some selected atomic masses, including the estimated uncertainties of measurement. We need a second standard of mass because present laboratory techniques permit us to compare atomic masses with each other to greater precision than we can presently compare them with the standard kilogram. However, development of an atomic mass standard to replace the standard kilogram is well under way. The relationship between the present atomic standard and the primary standard is approximately:
$$1\ \text{u} = 1.661 \times 10^{-27}\ \text{kg}$$

### Table 1-6 Some Measured Atomic Masses
| Isotope | Mass (u) | Uncertainty (u) |
| --- | --- | --- |
| $^1\text{H}$ | 1.00782503214 | 0.00000000035 |
| $^{12}\text{C}$ | 12.00000000 | (exact) |
| $^{64}\text{Cu}$ | 63.9297679 | 0.0000015 |
| $^{109}\text{Ag}$ | 108.9047551 | 0.0000032 |
| $^{137}\text{Cs}$ | 136.9070836 | 0.0000032 |
| $^{208}\text{Pb}$ | 207.9766358 | 0.0000031 |
| $^{238}\text{Pu}$ | 238.0495534 | 0.0000022 |

A related SI unit is the mole, which measures the quantity of a substance. One mole of $^{12}\text{C}$ atoms has a mass of exactly 12 grams and contains a number of atoms numerically equal to the Avogadro constant $N_A$:
$$N_A = 6.02214199 \times 10^{23}\ \text{per mole}$$

This is an experimentally determined number, with an uncertainty of about one part in a million. One mole of any other substance contains the same number of elementary entities (atoms, molecules, or whatever). Thus 1 mole of helium gas contains $N_A$ atoms of He, 1 mole of oxygen contains $N_A$ molecules of $O_2$, and 1 mole of water contains $N_A$ molecules of $H_2O$.

To relate an atomic unit of mass to a bulk unit, it is necessary to use the Avogadro constant. Replacing the standard kilogram with an atomic standard will require an improvement of at least two orders of magnitude in the precision of the measured value of $N_A$ to obtain masses with precisions of 1 part in $10^8$.

## 1-6 PRECISION AND SIGNIFICANT FIGURES
When we make a measurement, we can never be certain that the value we obtain is the “true” value of the quantity being measured. Instead, we can only estimate the range within which the true value is likely to lie. For example, if we measure the length of a table as 3 m, we are reasonably certain that the true length lies between 2 m and 4 m. If we measure it more precisely as 3.14159 m, we mean that the true length probably lies between 3.14158 m and 3.14160 m.

As we improve the quality of our measuring instruments and the sophistication of our techniques, we can carry out experiments at ever increasing levels of precision; that is, we can extend the measured results to more and more significant figures and correspondingly reduce the experimental uncertainty of the result. Both the number of significant figures and the uncertainty tell something about our estimate of the precision of the result.

Attention to significant figures is important when presenting the results of measurements and calculations, and it is equally as wrong to include too many as too few. If you express a length as 3 m when in fact you really believe that it is 3.14159 m, you are withholding information that might be important. On the other hand, if you express it as 3.14159 m when you really have no basis for knowing anything other than that it is approximately 3 m, you are being somewhat dishonest by claiming to have more information than you really do.

There are a few simple rules to follow in deciding how many significant figures to keep:

1. **Counting significant figures**: Counting from the left and ignoring leading zeros, keep all digits up to the first doubtful one. For example, $x = 3\ \text{m}$ has only one significant figure, and expressing this value as $x = 0.003\ \text{km}$ does not change the number of significant figures (the leading zeros are just placeholders). If we instead wrote $x = 3.0\ \text{m}$ (or equivalently $x = 0.0030\ \text{km}$), we would imply that we know the value to two significant figures. In particular, don’t write down all 9 or 10 digits of your calculator display if they are not justified by the precision of the input data! Most calculations in this text are done with two or three significant figures.

2. **Ambiguous notations**: Be careful about ambiguous notations. For example, $x = 300\ \text{m}$ does not indicate whether there are one, two, or three significant figures; we don’t know whether the zeros are carrying information or merely serving as placeholders. Instead, we specify the precision more clearly by writing $x = 3 \times 10^2$, $3.0 \times 10^2$, or $3.00 \times 10^2$ to indicate one, two, or three significant figures, respectively.

3. **Multiplication and division**: When multiplying or dividing, the number of significant figures in the product or quotient should be no greater than the number of significant figures in the least precise of the factors. For example:
$$2.3 \times 3.14159 = 7.2$$
(2.3 has two significant figures, so the result is rounded to two significant figures.)

A bit of good judgment is occasionally necessary when applying this rule. For example:
$$9.8 \times 1.03 = 10.1$$
Even though 9.8 technically has only two significant figures, it is very close to being a number with three significant figures (e.g., 9.80 would have three). The product should therefore be expressed with three significant figures.

4. **Addition and subtraction**: In adding or subtracting, the least significant digit of the sum or difference occupies the same relative position as the least significant digit of the quantities being added or subtracted. In this case, the number of significant figures is not important; it is the position that matters. For example, suppose we wish to find the total mass of three objects as follows:
$$
\begin{align*}
&104.0\ \text{kg} \quad (\text{least significant digit in tenths place}) \\
&+ \quad 2.10\ \text{kg} \quad (\text{least significant digit in hundredths place}) \\
&+ \quad 0.319\ \text{kg} \quad (\text{least significant digit in thousandths place}) \\
\hline
&106.419\ \text{kg} \quad (\text{rounded to 106.4 kg, least significant digit in tenths place})
\end{align*}
$$
By rule 1, we should include only one doubtful digit; thus the result should be expressed as 106.4 kg, for if the “4” (in the tenths place) is doubtful, then the following “19” gives no information and is useless.

### Sample Problem 1-3
You wish to weigh your pet cat, but all you have available is an ordinary home platform scale. It is a digital scale, which displays your weight in a whole number of pounds. You therefore use the following scheme: you determine your own weight to be 119 lbs, and then holding the cat you find your combined weight to be 128 lbs. What is the fractional or percentage uncertainty in your weight and in the weight of your cat?

#### Solution
The least significant digit is the units digit, and so your weight is uncertain by about 1 pound. That is, your scale would read 119 lb for any weight between 118.5 and 119.5 lb. The fractional uncertainty is therefore:
$$
\frac{1\ \text{lb}}{119\ \text{lb}} = 0.008\ \text{or}\ 0.8\%
$$

The weight of the cat is $128\ \text{lb} - 119\ \text{lb} = 9\ \text{lb}$. However, the uncertainty in the cat’s weight is still about 1 pound (since each measurement has an uncertainty of 1 pound, the uncertainty in the difference is the sum of the uncertainties, which is approximately 1 pound for small uncertainties), and so the fractional uncertainty is:
$$
\frac{1\ \text{lb}}{9\ \text{lb}} = 0.11\ \text{or}\ 11\%
$$

Although the absolute uncertainty in your weight and the cat’s weight is the same (1 lb), the relative uncertainty in your weight is an order of magnitude smaller than the relative uncertainty in the cat’s weight. If you tried to weigh a 1-lb kitten by this method, the relative uncertainty in its weight would be 100%. This illustrates a commonly occurring danger in the subtraction of two numbers that are nearly equal: the relative or percentage uncertainty in the difference can be very large.

## 1-7 DIMENSIONAL ANALYSIS
Associated with every measured or calculated quantity is a dimension. For example, both the absorption of sound by an enclosure and the probability for nuclear reactions to occur have the dimensions of an area. The units in which the quantities are expressed do not affect the dimension of the quantities: an area is still an area whether it is expressed in $m^2$, $ft^2$, acres, sabins (sound absorption), or barns (nuclear reactions).

Just as we defined our measurement standards earlier in this chapter as fundamental quantities, we can choose a set of fundamental dimensions based on independent measurement standards. For mechanical quantities, mass, length, and time are elementary and independent, so they can serve as fundamental dimensions. They are represented respectively by M, L, and T.

Any equation must be dimensionally consistent; that is, the dimensions on both sides must be the same. Attention to dimensions can often keep you from making errors in writing equations. For example, the distance $x$ covered in a time $t$ by an object starting from rest and moving subject to a constant acceleration $a$ will be shown in the next chapter to be $x = \frac{1}{2}at^2$. Acceleration is measured in units such as $m/s^2$, so its dimensions are $[a] = L/T^2$ (we use square brackets [ ] to denote “the dimension of”). The dimension of $x$ is $[x] = L$, and the dimension of $at^2$ is $[a][t^2] = (L/T^2)(T^2) = L$, which matches the dimension of $x$. Keeping the dimensions of acceleration in mind, you will therefore never be tempted to write $x = \frac{1}{2}at$ (dimension $L/T \times T = L$? No, $[at] = (L/T^2)T = L/T$, which does not match $[x] = L$) or $x = \frac{1}{2}at^3$ ([$at^3$] = (L/T^2)T^3 = LT, which also does not match $[x] = L$).

The analysis of dimensions can often help in working out equations. The following two sample problems illustrate this procedure.

### Sample Problem 1-4
To keep an object moving in a circle at constant speed requires a force called the “centripetal force.” (Circular motion is discussed in Chapter 4.) Do a dimensional analysis of the centripetal force.

#### Solution
We begin by asking “On which mechanical variables could the centripetal force $F$ depend?” The moving object has only three properties that are likely to be important: its mass $m$, its speed $v$, and the radius $r$ of its circular path. The centripetal force $F$ must therefore be given, apart from any dimensionless constants, by an equation of the form:
$$F \propto m^a v^b r^c$$
where the symbol $\propto$ means “is proportional to” and where $a$, $b$, and $c$ are numerical exponents to be determined from analyzing the dimensions.

As we wrote in Section 1-2 (and as we shall discuss in Chapter 3), force has units of $kg \cdot m/s^2$, so its dimensions are $[F] = MLT^{-2}$. The dimensions of the other quantities are $[m] = M$, $[v] = LT^{-1}$ (since speed is length per time), and $[r] = L$. We can therefore write the centripetal force equation in terms of dimensions as:
$$MLT^{-2} = [m^a v^b r^c] = [m]^a [v]^b [r]^c = M^a (LT^{-1})^b L^c = M^a L^{b+c} T^{-b}$$

Dimensional consistency means that the fundamental dimensions must be the same on each side. Thus, equating the exponents of each fundamental dimension:
- Exponent of M: $a = 1$
- Exponent of T: $-b = -2$ ⇒ $b = 2$
- Exponent of L: $b + c = 1$ ⇒ $2 + c = 1$ ⇒ $c = -1$

The resulting expression is $F \propto m v^2 r^{-1}$ or $F \propto \frac{m v^2}{r}$.

The actual expression for centripetal force, derived from Newton’s laws and the geometry of circular motion, is $F = \frac{m v^2}{r}$. The dimensional analysis gives us the exact dependence on the mechanical variables! This is really a happy accident, because dimensional analysis can’t tell us anything about constants that do not have dimensions. In this case the constant happens to be 1.

### Sample Problem 1-5
An important milestone in the evolution of the universe just after the Big Bang is the Planck time $t_P$, the value of which depends on three fundamental constants: (1) the speed of light (the fundamental constant of relativity), $c = 3.00 \times 10^8\ \text{m/s}$; (2) Newton’s gravitational constant (the fundamental constant of gravity), $G = 6.67 \times 10^{-11}\ \text{m}^3/(s^2 \cdot kg)$; and (3) Planck’s constant (the fundamental constant of quantum mechanics), $h = 6.63 \times 10^{-34}\ \text{kg} \cdot m^2/s$. Based on a dimensional analysis, find the value of the Planck time.

#### Solution
Using the units given for the three constants, we can obtain their dimensions:
- $[c] = LT^{-1}$ (speed is length per time)
- $[G] = L^3 M^{-1} T^{-2}$ (from $G = 6.67 \times 10^{-11}\ \text{m}^3/(s^2 \cdot kg)$, so dimensions are $L^3/(T^2 M) = L^3 M^{-1} T^{-2}$)
- $[h] = ML^2 T^{-1}$ (from $h = 6.63 \times 10^{-34}\ \text{kg} \cdot m^2/s$, so dimensions are $M L^2 / T = ML^2 T^{-1}$)

Let the Planck time depend on these constants as $t_P \propto c^i G^j h^k$, where $i$, $j$, and $k$ are exponents to be determined. The dimensions of this expression are:
$$
[t_P] = [c^i G^j h^k] = [c]^i [G]^j [h]^k = (LT^{-1})^i (L^3 M^{-1} T^{-2})^j (ML^2 T^{-1})^k
$$

The dimension of time is $[t_P] = T$, so we can equate the dimensions on both sides:
$$
T = L^i T^{-i} \times L^{3j} M^{-j} T^{-2j} \times M^k L^{2k} T^{-k} = M^{-j + k} L^{i + 3j + 2k} T^{-i - 2j - k}
$$

Equating the exponents of each fundamental dimension on both sides (note that there is no M or L on the left-hand side, so their exponents must be zero):
1. Exponent of M: $-j + k = 0$ ⇒ $k = j$
2. Exponent of L: $i + 3j + 2k = 0$. Since $k = j$, this becomes $i + 3j + 2j = i + 5j = 0$ ⇒ $i = -5j$
3. Exponent of T: $-i - 2j - k = 1$. Substituting $i = -5j$ and $k = j$, we get $-(-5j) - 2j - j = 5j - 2j - j = 2j = 1$ ⇒ $j = \frac{1}{2}$

Thus:
- $j = \frac{1}{2}$
- $k = j = \frac{1}{2}$
- $i = -5j = -\frac{5}{2}$

Therefore, the Planck time is proportional to $c^{-5/2} G^{1/2} h^{1/2}$, or:
$$
t_P \propto \sqrt{\frac{G h}{c^5}}
$$

Substituting the numerical values of $G$, $h$, and $c$:
$$
t_P = \sqrt{\frac{(6.67 \times 10^{-11}\ \text{m}^3/(s^2 \cdot kg))(6.63 \times 10^{-34}\ \text{kg} \cdot m^2/s)}{(3.00 \times 10^8\ \text{m/s})^5}} = 1.35 \times 10^{-45}\ \text{s}
$$

As commonly defined, the Planck time differs from this value by a factor of $(2\pi)^{-1/2}$. Such dimensionless factors cannot be found by this technique.

In similar fashion, we can determine the Planck length and the Planck mass, which also have very fundamental interpretations (see Exercises 32 and 33).