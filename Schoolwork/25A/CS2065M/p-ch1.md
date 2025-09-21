# 第一章 绪论

“我们必须知道，我们必将知道”—— 大卫 希尔伯特 (David · Hilbert)


人工智能概述

- 人工智能的起源
- 可计算载体：形式化与 机械化
- 智能计算方法
- 新一代人工智能

二十世纪初，可计算思想的提出促进了原始递归函数、λ−演算和图灵机等“计算载体”的诞生。其中 图灵机以机械自动的方式进行“计算”，为现代计算机理论模型奠定了基础，宣示着自动计算时代的到来，为人工智能领域提供了“机器载体”。

延伸阅读 当前是从过去拔萃出来的投影（费孝通）



## 人工智能的起源



约翰·麦卡锡、马文·明斯基、克劳德·香农和纳撒尼尔·罗切斯特等4位学者 ，在1955年8月的达特茅斯学
院夏季研讨会议联合提出了一个提案。提案中首次使用了“Artificial Intelligence”——人工智能诞生。
并且 ，四位科学家希望**美国洛克菲勒基金会**能够提供一笔研究经费 ，资助一批学者于1956年夏天在达特茅斯学院开展“**让机器能像人那样认知、思考和学习，即用计算机模拟人的智能**”前沿问题的研究 。


- 自动计算机（自动编程）
- 计算机如何编程，使用语言
- 神经网络
- 计算规模理论
- 自我改进（指机械学习） 
- 抽象
- 随机性与创造性




马文.明斯基 ：“人工智能是一门科学，是使机器做那些人需要通过智能来做的事情”。

斯坦福大学尼尔逊定义 ：“人工智能是关于知识 的学科 ，怎样表示知识以及怎样获得知识并使用知识的科学”。

美国麻省理工学院（ MIT ）的温斯顿教授定义     “人工智能就是研究如何使计算机去做过去只有 人才能做的智能工作”。


人工智能诞生之初所提研究问题













达特茅斯会议合影
(1956年6月18日至8月17日)	



七大议题




40位专家




8周时间
	



                  议题                                           描述                            

自动计算机                           让计算机完成特定人类工作 使用语言对计算机进行编程   通过语言对计算机编程
神经网络                               通过神经网络让计算机形成抽象概念

计算复杂度                           计算任务所耗费的时间和空间

智能算法的自我改进              算法能够苟日新、日日新

智能算法的抽象能力              大数据读薄、然后厚积薄发（归纳和演绎） 智能算法的随机性和创造力   智能算法具备学会学习能力


三次浪潮两次低谷
G






					
		2016   下围棋	AlphaGo 胜过人类	
GPT、Bert 开启	
NLP的预训练新范式
			o     AI f	or Science 形成热潮	
		
	o     Transforme	r 在自然语言处理获	得成功



1970	
	第三次浪潮
	o     Attention 在机器翻 GAN 在围棋任务上获得成功	译上获得成功	
第一次黄金期	第五代 计算机兴起	第五代计算机失败，               o	CNN 在图像识别上的成功 在语音识别上的成功		
Logic Theorist 款人工智能软件	
					

	Hopfield 网络&BP算法

	
			
	

16

三大学派--符号主义
ZHEJ IAN G  U N IVE RS ITY





证明：苏格拉底会死




苹果,Apple,A ，...



坐在火药桶上的人




逻辑推理方法
• 三段论
• 归纳-演绎
• 充要条件
• 命题证明（逆，否，逆否， 真，假，伪）
• 易经、梅花易数、铁板神数？


三大学派—联结主义
ZHEJ IAN G  U N IVE RS ITY






		算法与模型
•  BP ，MLP ，CNN ，LSTM ，Transformer ， GPT ，Diffusion ，MLLM … …			成功案例
• 人脸识别，机器翻译， chatGPT ，图像分 类（AlexNet ），Sora ，AI绘画 ……
					
					
	
优点
•  自动训练，可预测，适应变化，超越人 类，仿生，高维 ……	
缺点
• 难解释，算力，过拟合，偏见，鲁棒性， 伦理冲突 ……
			


三大学派—行为主义
ZHEJ IAN G  U N IVE RS ITY






算法原理：条件反射 ，博弈 ，强化学习
优     点 ：重视结果，环境适应性强 ，人类对齐 缺     点 ：功利主义 ，试错成本和风险高
成功案例：游戏AI（ Alpha GO ，AlphaStar）， 自动驾驶 ，机器人，无人机 ……







小鼠穿梭箱




巴浦洛夫实验              图片来源：百度
19

人工智能技术
ZHEJ IAN G  U N IVE RS ITY

l1997 ：深蓝击败国际象棋冠军卡斯帕罗夫 ，AI首次在高级战略游戏中战胜人类
l2016 ：AlphaGo以4:1战胜围棋世界冠军李世石 ，证明AI可在高度复杂的围棋领域突破人类极限
l2017 ：升级版AlphaGo Master在乌镇以3:0击败世界第一柯洁 ，展现出超越人类的洞察力
l分布式系统 ：1202 个CPU 和176 块GPU ；单机版 ：48 个CPU 和8 块GPU ；走子速度 ：3 毫秒-2 微秒




20

人工智能技术的演变：大语言模型
U N IVE RS ITY

l2022年11月 ：Chat GPT发布 ，首次让普通用户体验到AI在对话、编程、写作等方面的突破性能力
l2023年3月 ：GPT-4实现多模态理解，在专业领域（法律、 医疗、金融）能力逼近专家水平 ，并在教 育领域开启个性化学习新模式
l2023 ：Chat GPT入选《自然》年度十大科技人物，首次有AI工具获此殊荣
l2023-2024年 ：国内主要大模型相继发布应用，文心一言（百度）、通义千问（ 阿里）、星火（科大 讯飞）、 Kimi、智谱清言等对话系统上线应用。
l2024年12月 ，DeepSeek v3发布
l2025年1月 ，DeepSeek R1发布


21

人工智能技术的演变：从辨别式到生成式
G





22

通用性技术
ZHEJ IAN G  U N IVE RS ITY

1987年诺贝尔经济学奖获得者美国经济学家索洛研究表明 ，国民经济最终会达到这样一种发展阶段（稳  态） ：在那个阶段以后 ，经济增长将只取决于技术的进步。也就是说 ，技术进步决定了经济增长 ，是经济增  长的引擎。虽然技术进步是经济增长的源泉 ，但是长期的经济增长是由少数几种被称之为“通用目的技术” （general purpose technologies ，简称GPTs ）而驱动。



人类不同时代的通用目的技术


l 在人类发展历史上，蒸汽机、电力、计算机、半导体和互联网等与人工智能   一样，都是通用目的技术 ，具有普遍适用性、动态演进性和创新互补性特点。
l 美国历史学家斯塔夫里阿诺斯（ Leften Stavros Stavrianos）在《全球通史》 一书赞誉为“蒸汽机的历史意义无论怎样夸大都不过”。蒸汽机与纺织、交    通和冶金等工业结合，推动人类迈入工业革命时代。
l 通用目的技术是最核心创新要素，但不是完整的最终解决方案。
l 通用模型不是终点，而是通向更高效专业化的桥梁。每个行业都能基于 通用能力快速构建自己的专用系统
l 通用模型（深度学习、大模型）的出现， 大幅降低了专业化的门槛
l 技术按照类似的历史规律在演变，但速度更快了
l 站在通用模型的肩膀上，降低专业解决方案的开发周期

从聊天出发：Artificial General Intelligence (AGI)
U










Stage Level 5: Organizations,
AI that can do the work of an organization.


Stage Level 4: Innovators,   AI that can aid in invention.

Stage Level 3: Agents,
systems that can take actions.

Stage Level 2: Reasoners,
human-level problem solving.


Stage Level 1: Chatbots,
AI with conversational language.



对话大模型的成功要素
G





规模增⼤不只是变⼤ ，还会产⽣全新的功能和能⼒












⼩模型
基本对话



参数规模 vs 能⼒涌现



中模型









⼤模型
+ 推理能⼒ + 创意能⼒
…






推理大模型

l 深度思考能力，不再满足于答案，而是进行多层次推理验证
l 接近人类思维，模拟专家的思考过程而非仅仅模仿结果
l 慢思考的优势：推理链展开，让每个推理步骤都经过充分论证

例子1 ：有三个开关，它们连接到楼上的三个灯泡。你在楼下只能  看到开关，看不到楼上的灯泡。你只能上楼一次，如何确定每个开 关对应哪个灯泡？

嗯，这个问题看起来是一个经典的逻辑题。我得仔细想想。题目是说有三个开关，分别连接到楼上的三个灯泡。但我在楼下只能操作这些开关，而看不到楼上的情况。 现在只能上楼一次，要确定每个开关对应哪个灯泡。那该怎么做呢？首先，我得回忆一下类似的问题。好像以前听说过类似的解决方法，可能涉及到利用灯泡的不同    状态，比如温度或者亮灭。比如，可能先打开一个开关一段时间，然后关掉，再打开另一个，这样可以通过灯泡的热度来判断。不过具体步骤可能需要仔细设计。
让我仔细思考一下。假设三个开关分别是A、B、C ，对应的三个灯泡是X、Y、Z。现在只能上楼一次，所以在上去之前需要设置好开关的状态，然后上楼检查结果。 可能的思路是：先打开某个开关，保持一段时间让灯泡发热，然后关闭，再打开另一个开关，这样在楼上时，一个灯泡是亮的，另一个是温的，剩下的那个是冷的。 比如，首先打开开关A ，等待几分钟，让对应的灯泡变热。然后关闭A ，迅速打开开关B ，然后马上上楼。此时，如果X是亮的，那么对应B ；如果某个灯泡是温的，   对应A ；剩下的冷的对应C。不过这样的话，可能需要同时处理温度和亮的状态，这样才能区分三个开关。
具体步骤可能如下：1. 打开开关A ，等待足够时间让灯泡变热（比如5分钟）。2. 关闭开关A ，然后立即打开开关B。3. 迅速上楼检查灯泡的情况。
这时，三个灯泡的状态可能是：一个亮着的（对应B ），一个温的（对应A ，因为之前被打开过一段时间然后关闭了），另一个是冷的（对应C ）。这样就能区分三个 开关了。
不过，这个过程中需要确保时间足够让灯泡A变热，而B刚打开所以对应的灯泡可能已经亮了一段时间，不过如果立即上楼的话，可能灯泡B的温度还不明显。所以是 否应该调整顺序？
或者，可能的步骤是：1. 打开开关A ，等待几分钟让对应的灯泡变热。2. 关闭开关A ，同时打开开关B。3. 然后立即上楼，这时候：
- 亮着的灯泡是B控制的。
- 不亮但发热的是A控制的。
- 既不亮也不热的是C控制的。
这样应该可以。因为当A被关闭后，灯泡A会逐渐冷却，但如果在关闭之后立即上楼，可能温度还未完全散去。而B被打开后，对应的灯泡此时是亮的。所以通过触摸 灯泡的温度和观察是否亮，可以确定三个开关对应的灯泡。这样，上楼一次就能确定每个开关对应的灯泡了。这个思路应该可行。
不过有没有可能遗漏的情况？比如，如果等待时间不够，可能温度不够明显。或者如果灯泡是LED的，可能发热不明显，但题目里应该假设是传统的白炽灯，会发热。 总结步骤：
1. 打开第一个开关（比如A ），保持一段时间（比如5分钟），然后关闭。
2. 打开第二个开关（ B ），不关闭，立即上楼。
3. 上楼后，亮着的灯泡是B控制的。
4. 触摸另外两个不亮的灯泡，温的是A控制的，冷的是C控制的。 这样就能区分三个开关对应的灯泡了。
要确定三个开关分别对应的灯泡，可以按照以下步骤操作：
打开第一个开关（例如开关A）：保持开启约5分钟，使对应的灯泡充分发热，随后关闭开关A。 立即打开第二个开关（例如开关B ）：保持开启状态，并迅速上楼检查灯泡。
观察和触摸灯泡状态：
亮的灯泡：对应开关B（因为它当前处于开启状态）。
不亮但温热的灯泡：对应开关A（因曾被开启一段时间后关闭，余温尚存）。 不亮且冷的灯泡：对应未操作过的开关C。
原理：利用灯泡的两种状态（亮/灭）和温度（热/冷）的组合差异，在仅一次上楼的机会中区 分三个开关对应的灯泡。

推理大模型
ZHEJ IAN G  U N IVE RS ITY

Grok 3


27

推理大模型
ZHEJ IAN G  U N IVE RS ITY

l 以DeepSeek R1深度推理为例 例子2 ： 8,8,3,4算24点

嗯，今天老师布置了一个算24点的题目，四个数字是8 、8 、3 、4。我得好好想想怎么用这四个数字通过加减乘除来得到24。首先，我应该回忆一下算24点的基本方法，通常是先尝试用乘法或者除法来得到较大的数，或者组 合出能够相互抵消的情况，比如3×8=24这样的组合。不过这里有两个8，一个3和一个4，可能需要结合其他运算。
首先，我先把这四个数字列出来：8 、8 、3 、4。我需要用每个数字各一次，通过加减乘除以及可能的括号来组合它们得到24。让我尝试不同的组合方式。
首先，我注意到如果有两个8的话，或许可以先用这两个8进行某种运算。比如8+8=16，不过这样的话剩下的3和4要怎么处理呢？16加上3和4的话，16+3+4=23，不够。或者16乘以（4-3）=16 × 1=16，还是不够。或者16乘 以3再除以4的话，16 ×3=48 ，48 ÷4=12，还是不够。或者16×(4+3)/某个数，但这样可能也不太行。
再想想，如果有办法用3和4来得到某个数，再和8组合。比如3×4=12，然后加上8和8的话，12+8+8=28，超过了。或者12×（ 8/8）=12 × 1=12，还是不够。或者用减法，12 ×(8-8)=0，没用。 再想想，可能用减法来调整。例如，8 ×4=32，然后32减去（8-3）=5，得到32-5=27，还是不对。或者8×3=24，然后用剩下的8和4组成0，但同样的问题，无法用剩下的两个数得到0。
或者试试不同的括号组合，比如
或者，(8 × 3) - (8 - 4) =24 -4=20，不对。或者(8 + 8) × (4 -3)=16×1=16，还是不够。 首先，尝试两个数的运算，然后剩下的两个数，再将结果结合起来。
例如，先算8+8=16，剩下的3和4，可能组合成12，这样16+12=28，但3×4=12，不行。或者16×(4-3)=16×1=16，没用。 或者先算8×8=64，剩下的3和4，64-3×4=64-12=52，不对。
或者先算3×4=12，然后8+8=16，12+16=28，还是不对。
或者先算8-4=4，剩下的8和3，可能有8×3=24，再4×24=96，不对。
。。。
8 ×3 × ( (8 ÷4) - (something) )
其中，(8 ÷4)=2，然后如果something是0，但如何用剩下的数字得到0 ？比如8-8=0，但这样已经用了两个8，所以可能不行。 或者，用4-3=1，然后2-1=1，这样8×3 × 1=24，但这里用到了4和3，以及两个8，所以表达式可能是：
(8 ×3) × ( (8 ÷4) - (4 -3) )=24 × (2 -1)=24×1=24。这里每个数字都被正确使用了一次：
- 第一个8和3用于8×3=24
- 第二个8和4用于8÷4=2
- 4-3=1，然后2-1=1
所以整个表达式是： (8 ×3) × ( (8 ÷4) - (4 -3) )=24×1=24
这样，每个数字都被使用了一次，没有重复，所以这是正确的解法！
。。。
让我再检查一遍这个运算：
首先，8 ÷4=2，然后2-1=1（这里的 1是从哪里来的？题目中并没有1这个数字，可能我在这里犯了一个错误。因为题目中的数字是8 、8 、3 、4，所以不能随便添加 1，除非用运算得到 1。例如，如果我能用剩下的数字得到 1， 但这里可能有问题。
思考长度达6672个字符                                                                                                                   28

大模型智能体
G





































29

多智能体
G

社会模拟： Altera.ai构建的智能体文明中包含 1000 多个自主智能体，在《我的 世界》中构建了自己的经济、文化、宗教和政府。




















30










人工智能在内容合成中的应用
G



l AI摄影作品《相爱的双胞胎姐妹》获首届   Prompted Peculiar国际大奖 ，展现AI在艺 术创作领域的新可能


l《太空歌剧院》获科罗拉多艺术博览会数  字艺术冠军 ，Midjourney生成图像首次赢 得重要艺术奖项





AI 摄影作品《相爱的双胞胎姐妹》                                                             《太空歌剧院》

人工智能在内容合成中的应用
G






































32

人工智能在内容合成中的应用
G






































33

人工智能在内容合成中的应用
G






































34

OpenAI: Sora（ 2024.2.15 ，2024.12.9 ）


• 将视频压缩到低维隐空间，并进一步将表示分解为时空子块，为视频模型提供了 一 种灵活的表示，允许模型在不同的分辨率、时长和宽高比上进行训练和生成，采用 扩散型Transformer，保证样本质量随计算量扩展显著提高。



注：视频由人工智能生成

Google: Veo （ 2024.5.14）， Veo2(2024.12.06)
U


Veo 是 Google DeepMind 开发的视频生成模型，能够生成1080p分辨率的高质量视频，涵盖各种电影和视
觉风格。










注：视频由人工智能生成


36

Google: Veo 3（ 2025.5.20）
U







37

Google: Veo 3（ 2025.5.20）
U



Prompt: The scene explodes with the raw, visceral, and unpredictable energy of a hardcore off-road rally, captured with a dynamic, almost found-
footage or embedded sports documentary aesthetic. The camera is often shaky, seemingly mounted inside one of the vehicles or held by a daring
spectator very close to the action, frequently splattered with mud or water, catching unintentional lens flares from the natural, often harsh, sunlight filtering through trees or reflecting off wet surfaces. We are immersed in a challenging, untamed natural environment – perhaps a dense, muddy
forest trail, a treacherous rocky incline littered with loose scree, or a series_of shallow, fast-flowing river crossings. Several heavily modified, entirely unidentifiable, and unbranded off-road vehicles are engaged in a frenetic, no-holds-barred race. These are not showroom models; they are custom-  built, rugged machines – open-wheeled buggies with exposed engines and prominent roll cages, heavily armored pickup trucks with oversized,
knobby tires and snorkel exhausts, their original forms and manufacturers completely obscured by extreme modifications, layers of caked-on mud, and a general air of brutal functionality. The dominant sounds are the deafening, guttural roar of powerful, untamed engines, the whine of
transmissions, the percussive impact of suspension bottoming out, and the constant spray of mud and water. Within an 8-second sequence, one of  the lead vehicles, a low-slung, open-cockpit buggy so caked in thick, brown mud that its original color is a mystery, approaches a wide, shallow river
crossing at incredible speed. Without the slightest hesitation, its unseen driver powers straight into the water. The impact sends an enormous,
almost solid, opaque sheet of muddy water, mixed with stones and debris from the riverbed, spectacularly high into the air, completely engulfing the small buggy for a terrifying moment, obscuring it from view as if it has been swallowed by the river itself. Right on its tail, a pursuing, equally mud-
encrusted, custom-built truck – a hulking, high-clearance beast with a heavily reinforced external roll cage and no discernible badging – arrives at the river crossing just as this massive wall of airborne water reaches its peak. Instead of slowing or attempting to find a clearer path, the truck's driver,
with unwavering aggression, plunges directly into and through this opaque, turbulent curtain of muddy spray at full throttle. A split second later, the truck bursts out from the other side of the deluge, water cascading from its roof and chassis, its oversized windshield wipers struggling frantically to  clear the torrent of muddy water obscuring the driver's vision. It lands heavily on the far bank, suspension groaning, but still in hot pursuit of the
now-reappearing buggy. This thrilling, messy, and visually spectacular sequence of one vehicle creating a massive environmental obstacle and the next immediately conquering it through sheer force, forms the core, immersive, attention-grabbing event of the 8-second sequence. The race
continues with undiminished ferocity, the natural terrain itself an active participant in the conflict.



38

Meta ：Movie Gen（ 2024.10.4 ）
G







注：视频由人工智能生成


39

生成式自动驾驶仿真环境                                                  



GAIA-1: A Generative World Model for Autonomous Driving                                                                注：视频由人工智能生成

生成式自动驾驶仿真环境
G








GAIA-2


注：视频由人工智能生成    41

生成式自动驾驶仿真环境
G


















GAIA-2


注：视频由人工智能生成    42

通用智能系统

l AI硬件正成为科技巨头竞逐的新战场：OpenAI以65亿美元收购前苹果首席设计官 Jony Ive创立的硬件公司IO
l 预计2030年AI硬件市场将达4741亿美元，从OpenAI的无屏挂脖设备到国内的AI 录音笔、智能眼镜等产品百花齐放，整个行业正在探索AI与人交互的全新形态。


















桌面陪伴机器人：Eilik。通过触摸、 表情变化以及与其他机器人的互动来 与用户建立连接。



三星Ballie是一款可在家中   自由滚动的AI机器人助手 ，  集成智能家居控制、个性化   推荐和投影功能 ，能通过语   音和视觉识别理解用户需求。



OpenAI的AI硬件。猜测它没有屏幕，可
以佩戴、常驻身边；有摄像头，具备环境 感知能力；以语音对话为主要交互方式。 体验和陪伴可能是一个重要的方向。

通用智能系统——具身本体（智能终端）

不同本体各有优势，但共同追求 “能理解任务、适应环境、自主决策”的通用智能体



人形：Atlas（波士顿动力）
l 可执行搬运、跳跃等复杂动作

四足：Spot（波士顿动力）
l 稳定的四足移动平台
l 可搭载多种传感器和工具



机械臂：桌面级协作机器人
l 精准操控小型物体
l 适用于装配、分拣等精细作业

轮式：野外探索机器人
l 高通过性的轮式底盘
l 长续航和自主导航能力

具身智能体的现状




IQ测试达到人类水平
Science Advances, 2024.

仅需几天训练就能达到各种游戏专家水平
Nature, 2025.
虚拟空间下智能体已经表现出很高的智能水平




机器人踢足球
Science Robotics, 2024.


人形机器人马拉松
Humanoid Robot Marathon
物理空间下的具身智能体能力仍然很有限

虚拟环境中的大模型已实现通用智能的突破，而物理世界中的具身智能仍受限于仿 真到现实的差距、多模态融合的复杂性和机械控制的精度瓶颈。

2024年诺贝尔化学奖（2024年10月9日）                             
l 2024年诺贝尔化学奖聚焦于人工智能在蛋白质结构预测领 域的突破性进展
l大卫·贝克（ David Baker）表彰其在计算蛋白质设计领 域的工作
l 戴密斯·哈萨比斯（ Demis Hassabis）和约翰·朱姆珀   （ John M. Jumper）表彰其在使用人工智能进行蛋白 质结构预测方面取得的进展。
l人工智能应用于基础科学研究首次获得诺贝尔奖，标志着 计算方法在化学、生物学领域的重要性得到认可


2024年诺贝尔物理学奖（2024年10月8日）                         





emergent collective computational abilities (《具有涌现集体计算能力 的神经网络和物理系统》), 1982, PNAS
1949年赫布(Hebbian theory）提出：神经元之间持续重复经验刺激可导致突触传递效 能增加(Neurons that fire together, wire together) ，即学习和记忆的本质是大脑结 构在后期经验刺激下改变神经元之间强弱联结的权重的结果。 Hopfield以能量最小这一
物理学视角优化神经网络而得到局部最优解。



Ackley David H, Hinton Geoffrey E, Sejnowski Terrence J, A learning
algorithm for Boltzmann machines, Cognitive science, Elsevier, 9 (1): 147–169,1985
Boltzmann机能够达到全局优化原因在于基于统计物理所设计的Monte Carlo方法 ，以
定的概率重新设置神经元的值 ，选择的概率保证网络收敛于由“能量 ”完全确定的热 平衡态。

从神经网络的生物学机制阐释到物理学可计算模拟