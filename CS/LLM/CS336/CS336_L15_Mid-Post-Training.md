---
title: "Lecture 15: Mid/Post-Training"
---

# Lecture 15: Mid/Post-Training / 第十五讲：中训练与后训练

---

## 1. Introduction: From GPT-3 to ChatGPT / 引言：从GPT-3到ChatGPT

Thus far, we've been able to build a souped-up version of GPT-3 with more compute and more data, but the utility of such a base model is ultimately limited. When we went from GPT-3 to ChatGPT, the difference was dramatic—if your first exposure was ChatGPT, going back to GPT-3 feels like interacting with something almost pointless. GPT-3 could only really do copywriting or fun little tasks where you don't need reliability or instruction following. Today we're going to get from GPT-3 to something close to ChatGPT, and in the next lecture we'll go from ChatGPT to thinking models like GPT-o1. The process that takes us from left to right is what people call post-training (后训练).

到目前为止，我们能够用更多算力和数据构建一个强化版的GPT-3，但这种基座模型的实用性终究有限。从GPT-3到ChatGPT的跨越是巨大的——如果你的首次接触是ChatGPT，再回去用GPT-3会觉得这东西毫无意义。GPT-3只能做文案写作这类不需要可靠性或指令遵循的小任务。今天我们将从GPT-3走向接近ChatGPT的水平，下一讲再从ChatGPT走向GPT-o1这类思考模型。这个从左到右的过程就是人们所说的后训练（post-training）。

Instruction following—the ability to put in a long, complicated prompt and get back very reasonable answers—was basically impossible at the GPT-3 level. You could use few-shot prompts, and if your examples were good enough, you'd get something reasonable, but fine-grained control was limited. With GPT-3.5 and GPT-4, we started seeing very long programmatic prompts being one-shotted by the model. So what do we need to get instruction following to work? Pre-training is always important—it's the basis on which we build all of this. If we ignore pre-training and just try to train our way to victory, we get nothing. Pre-training scales in a diverse, broad way, but once we have it, we need to extract the behaviors we want from that primordial soup. This requires much more explicit data collection, explicit steering, and a lot of messy engineering.

指令遵循（instruction following）——即输入一个很长、复杂的提示并得到合理的回答——在GPT-3时代基本不可能。你可以用少样本提示，如果例子足够好也能得到合理的结果，但对模型的精细控制非常有限。到了GPT-3.5和GPT-4，我们开始看到模型能够一次性完成非常长的程序化提示。那么，我们需要什么来实现指令遵循？预训练始终重要——它是我们构建一切的基础。如果忽略预训练，只靠训练强行取胜，我们将一无所获。预训练以多样化、广泛的方式扩展，但一旦有了预训练，我们需要从这锅"原始汤"中提取出我们想要的行为。这需要更明确的数据收集、明确的引导，以及大量繁琐的工程工作。

Information about frontier post-training is honestly pretty sparse. Major references like the RLHF paper ("Learning to Summarize from Human Feedback") and Anthropic's HH paper (2022) were incredibly detailed, containing annotation guidelines and instructions for human feedback. But since competition heated up after ChatGPT, none of the vendors want to release information about their post-training processes—the data is very much a trade secret. Open source recipes rely heavily on distillation (蒸馏), which is very different from what frontier labs do with human data collection. Algorithm-wise, we have a pretty good handle on what's happening, but algorithms are not the secret sauce—the data is.

关于前沿后训练的信息其实相当稀少。主要参考文献如RLHF论文（"Learning to Summarize from Human Feedback"）和Anthropic的HH论文（2022年）曾极为详细，包含标注指南和对人类反馈的指导说明。但自ChatGPT之后竞争加剧，没有厂商愿意发布后训练过程的任何信息——数据完全是商业机密。开源方案大量依赖蒸馏（distillation），这与前沿实验室进行的人类数据收集截然不同。算法方面，我们对正在发生的事情有较好的把握，但算法并非秘密武器——数据才是。

---

## 2. The SFT Phase: It's All About Data / 监督微调阶段：核心全在数据

The first phase of post-training is SFT (Supervised Fine-Tuning, 监督微调). If we look at the RLHF papers, we see a straightforward two-part recipe: first, collect demonstration data—for every prompt, have an annotator provide a reference response; then do fine-tuning. After that, do some kind of reinforcement learning to shape the model's behavior to be more aligned with what humans think are good responses. The SFT part is really all about data. We all know how to SFT a model—it's exactly the same as pre-training, with the only real difference being the training data.

后训练的第一阶段是SFT（监督微调，Supervised Fine-Tuning）。看RLHF论文，我们能看到一个直接的两阶段方案：首先收集示范数据——为每个提示让标注者提供参考回答，然后进行微调；之后进行某种强化学习，将模型行为塑造得更符合人类认为好的回答。SFT阶段几乎全在数据上。我们都知道如何做SFT——和预训练一模一样，唯一真正的区别就是训练数据。

---

## 3. Evolution of SFT Data / SFT数据的演进

Let's look at the progression of SFT data over the years. The oldest and most visionary effort is FLAN, used to train Google's T5 model. The idea was: NLP people have already collected a bunch of supervised datasets of inputs and outputs, so we should just train the model on all of them. Reasonable to try, but it turned out not to be the right thing to do—the datasets were unnatural, summaries were very short and often hallucinated, and the instructions appeared at the end of the input, which is not how anyone actually prompts a model. FLAN also assumed you needed enormous scale in post-training, just like pre-training. We'll see later that much smaller datasets work too.

让我们看看多年来SFT数据的演进。最古老也最具远见的努力是FLAN，用于训练Google的T5模型。其思路是：NLP研究者已经收集了大量监督式的输入输出数据集，我们应该直接在所有这些数据集上训练模型。值得尝试，但事实证明这不是正确的方法——数据集不自然，摘要非常短且经常产生幻觉，指令出现在输入的末尾而非人们实际提问的方式。FLAN还假设后训练和预训练一样需要巨大规模，但我们之后会看到小得多的数据集也能奏效。

Self-Instruct and its follow-ups were very forward-looking: why can't we use the model itself to generate data? Models are getting better all the time and might even be better than some annotators—so let's get models to write high-quality responses. Then came distillation-style approaches like Alpaca and Vicuna (from Berkeley), which distilled ChatGPT traces to get input-output pairs. What they found was that these chat-style examples reliably induced ChatGPT-like behavior, especially when applied to the original Llama models. This was the inflection point where people realized: if you got chat-style data, it wasn't that hard to build ChatGPT-style systems.

Self-Instruct及其后续工作非常有远见：为什么不能用模型自身来生成数据？模型在不断变好，甚至可能比某些标注者更好——那就让模型来写高质量的回答。接着出现了蒸馏式的方法，如Alpaca和伯克利的Vicuna，它们蒸馏ChatGPT的输出来获取输入输出对。他们发现，这类对话风格的样本可靠地诱导出类似ChatGPT的行为，尤其是在原始Llama模型上应用时。这是一个拐点，人们意识到：有了对话风格的数据，构建类似ChatGPT的系统并不那么难。

Then came Open Assistant, a big crowdsourced effort like Wikipedia. Volunteers got together to write hard, interesting prompts and high-quality, expert-level responses at scale. It generated a decent amount of data—perhaps 10,000 or more examples—with very long, detailed, high-quality expert responses. Very admirable, but it eventually stalled as a project. A new generation including WizardLM and Tulu3 took the approach of using language models as very good synthetic data generators, coming up with increasingly complicated ways to generate instruction-following data.

然后是Open Assistant，一个类似维基百科的大规模众包努力。志愿者们聚在一起编写困难而有趣的提示，并大规模地撰写高质量、专家级的回答。它产生了相当数量的数据——大约一万或更多样本——带有非常长、详细、高质量的专家回答。非常令人钦佩，但该项目最终停滞了。新一代努力如WizardLM和Tulu3则将语言模型视为优秀的合成数据生成器，设计越来越复杂的方法来生成指令遵循数据。

Most recently, SFT and post-training has changed yet again: the focus is less on chat and much more on agents and tool use. If you look at NVIDIA's Nemotron, a big chunk of their SFT data consists of agentic SFT examples, where tool calls happen in parallel alongside text responses. Now we're moving toward structured formats with tool calls, to-do lists, and full agent behaviors. The big transitions have been: toward more detailed human-like responses (chattiness), toward higher-quality annotators writing expert responses, and toward tool use and the right API interfaces.

最近，SFT和后训练再次变化：重心从对话转向了智能体和工具使用。以NVIDIA的Nemotron为例，其SFT数据中有很大一部分是智能体式的SFT样本，工具调用和文本回复可以并行发生。现在我们正走向带有工具调用、待办列表和完整智能体行为的结构化格式。三大转变是：向更详细、更像人类的回复转变（对话感），向更高质量的标注者撰写专家回答转变，以及向工具使用和正确的API接口转变。

---

## 4. Pitfalls in SFT Data Collection / SFT数据收集的陷阱

If you're put in charge of collecting human annotation data for SFT, what should you be mindful of? Length and style variation is a very big part of post-training. Claude has a different tone than ChatGPT; ChatGPT is "too chatty." All of these are conscious decisions made by data collection folks. When you evaluate preferences, these stylistic factors matter enormously—people very often select responses with bullet-pointed lists or more and longer detail. This induces explicit distortions in chatbot tone. You can very much shift engagement signals without necessarily making your model smarter on standard benchmarks. So you want to think about style control separately from capabilities control.

如果你负责收集SFT的人类标注数据，需要注意什么？长度和风格变化是后训练中非常重要的一部分。Claude的语气不同于ChatGPT；ChatGPT"太啰嗦"——这些都是数据收集人员的有意决定。在评估偏好时，这些风格因素影响巨大——人们非常频繁地选择带有项目符号列表或更详细更长的回答。这会导致对话机器人语气的明显扭曲。你可以显著改变参与度信号，但不一定在标准基准测试上让模型变得更聪明。因此，你需要将风格控制与能力控制分开思考。

Another critical pitfall involves knowledge and hallucination. When you SFT on data that contains references to articles or facts, you're actually teaching the model two things at once: the factual knowledge itself, and the behavior of citing references. This is problematic because the model may misgeneralize—it will hallucinate a reference instead of giving a proper one. The folklore, supported by empirical evidence, is that if you train a model at the SFT phase to emit facts it doesn't know, this will make it hallucinate, because the model is trying to generalize both the knowledge and the format simultaneously. Training on unknown knowledge is like teaching the model to forcibly emit unknown knowledge.

另一个关键陷阱涉及知识和幻觉（hallucination）。当你在包含文章引用或事实的数据上做SFT时，你实际上同时在教模型两件事：事实知识本身，以及引用文献的行为。这有问题，因为模型可能错误泛化——它会幻觉出一个引用而不是给出真实的引用。经验法则（有实证支持）是：如果你在SFT阶段训练模型输出它不知道的事实，这会导致幻觉，因为模型同时在泛化知识和格式。在未知知识上训练等同于教模型强行输出未知知识。

John Schulman makes a separate argument: this is why reinforcement learning is needed. Teaching a model what it knows and doesn't know has to be policy-dependent—you can't have an external person shoving knowledge down the model's throat if you want the model to be calibrated about what it knows. So you might not want to train on the highest quality data if the model doesn't already know that data. Tail knowledge can be actively harmful, especially when associated with markers like "Reference:", as it forces the model to emit a reference afterward.

John Schulman提出另一个论点：这就是需要强化学习的原因。教模型它知道什么和不知道什么，必须是策略依赖的——如果你希望模型对自己知道什么有校准，不能让外部人员把知识塞进模型的喉咙。因此，如果模型本身不知道那些数据，你不一定想用最高质量的数据来训练。尾部知识可能有积极作用，尤其是当它关联到"Reference:"这类标记时——它会迫使模型之后输出引用。

---

## 5. Safety SFT / 安全SFT

Once we get to post-training, we have to engage with messy realities: what if people use our system for political manipulation, disinformation, or individualized spearphishing? You are the last line of defense. The solution is to apply safety controls—the model must refuse to respond to malicious inputs. Safety SFT information is even sparser than capabilities SFT information. The Llama 2 description is one of the more detailed ones, yet they don't even disclose how many examples they used. The framework balances two things: the violation rate (how often bad queries get through) and the false refusal rate (over-refusing benign queries like "how do I kill a Python process"). You want a good Pareto tradeoff between the two.

一旦进入后训练阶段，我们必须面对混乱的现实：如果有人用我们的系统进行政治操控、虚假信息传播或个性化钓鱼攻击怎么办？你是最后一道防线。解决方案是施加安全控制——模型必须拒绝对恶意输入的响应。安全SFT的信息比能力SFT的信息更加稀少。Llama 2的描述是最详细的之一，但他们甚至没有披露使用了多少样本。其框架平衡两件事：违规率（bad queries通过的比例）和误拒绝率（对"如何杀死Python进程"这类良性查询的过度拒绝）。你需要在两者之间取得良好的帕累托权衡。

The OLMo models from Allen AI provide one of the few detailed looks at a reasonably performant post-training pipeline, including a safety component of about 50,000 examples. They used WildChat—free chat access given to users—to collect real chat interactions, then filtered out unsafe behaviors and jailbreak attempts. The preferred responses were simply to resist the jailbreak or to say no. Similar things happen at closed-source companies: look at usage information, find unsafe behaviors, and get annotators to play whack-a-mole with these bad behaviors.

Allen AI的OLMo模型是少数几个展示了一个性能尚可的后训练管道细节的项目之一，包括约50,000个样本的安全组件。他们使用WildChat——给用户提供免费聊天访问——来收集真实的对话交互，然后过滤出不安全行为和越狱尝试。首选回答仅仅是抵抗越狱或者说"不"。闭源公司也在做类似的事情：查看使用信息，发现不安全行为，然后让标注者打地鼠式地应对这些不良行为。

One surprising finding: if you have a sufficiently capable model, it doesn't take many examples to steer it. With as little as 500 safety examples, the rate of following malicious instructions drops dramatically. Models already have a "safe vs. unsafe" axis inside them after pre-training—it doesn't take very many examples to pull this out. But this doesn't mean there's no benefit to more examples; if you're OpenAI or Anthropic and want to enforce fine-grained distinctions about safety, you do need very large-scale data collection.

一个令人惊讶的发现：如果模型足够强大，不需要很多样本来引导它。只需500个安全样本，遵循恶意指令的比例就会急剧下降。模型在预训练后内部已经有了"安全vs.不安全"的轴——不需要很多样本就能提取出来。但这并不意味着更多样本没有好处；如果你是OpenAI或Anthropic，想要强制执行关于安全的细粒度区分，你确实需要大规模的数据收集。

---

## 6. Methods: SFT Is Just Gradient Descent / 方法：SFT就是梯度下降

On the methods side, SFT is remarkably boring: you just do gradient descent. Loss.backward() and that's basically it. However, one important nuance is the increasing trend of turning instruction tuning into part of pre-training. Originally, pre-training and post-training were separate phases, but people realized: why separate them when you can mix them together? High-quality data, including instruction tuning data, is now mixed in at the tail end of training during the decay phase. This allows scaling up instruction tuning and emphasizes higher-quality data. Everyone is doing it, as seen in most model release reports mentioning a "mid-training" or "second-phase pre-training" with a different data mix.

在方法层面，SFT出奇地无聊：只需做梯度下降。`loss.backward()` 就完事了。然而，一个重要的细微之处是将指令微调变为预训练一部分的日益增长的趋势。最初，预训练和后训练是分开的阶段，但人们意识到：既然可以混合，为什么要分开？高质量数据（包括指令微调数据）现在在训练衰减阶段被混合到最后阶段的训练中。这使得指令微调得以扩展，并强调更高质量的数据。每个人都在这样做，大多数模型发布报告都提到"中训练"或"第二阶段预训练"使用了不同的数据混合。

One pet peeve: when someone tells you something is a base model (基座模型), that's kind of a lie. Base models today are pre-trained on UltraChat and who knows what else—chat datasets synthetically designed to make you good at chat. So it's hard to say that it's a base model in the traditional sense. This two-phase training blurs the boundaries between pre-training and instruction tuning. The decay phase, being closest to deployment and using the lowest learning rate, is where you want to put the highest quality data.

一个让人恼火的事：当有人说某模型是基座模型（base model）时，这其实不太真实。今天的基座模型在预训练时就用到了UltraChat等对话数据集——这些是为让你擅长对话而合成设计的数据。所以很难说这是传统意义上的基座模型。这种两阶段训练模糊了预训练和指令微调之间的界限。衰减阶段最接近部署，使用最低学习率，也是你希望放入最高质量数据的地方。

---

## 7. RLHF: A Conceptual Shift / RLHF：概念上的转变

Now we move to RLHF (基于人类反馈的强化学习). After SFT, we're going to do something very different: upweight or downweight different model outputs based on how a rater or reward model (奖励模型) decides how good the responses are. There's a crucial conceptual difference: pre-training and SFT are generative modeling problems—you're fitting a distribution over sequences. RLHF is a "maximize a reward" game. You want a policy that maximizes some downstream reward (user engagement, math problems solved, etc.), and you don't care if you've mimicked some distribution. In the second world, your distribution can collapse onto a single point for every input, and that would be fine as long as it gets good reward. This is a big conceptual distinction.

现在我们进入RLHF（基于人类反馈的强化学习，Reinforcement Learning from Human Feedback）。SFT之后，我们将做一些非常不同的事：根据评估者或奖励模型（reward model）判断回答的好坏，上加权或下加权不同的模型输出。这里有一个关键的概念区别：预训练和SFT是生成建模问题——你在拟合序列上的分布。RLHF是一个"最大化奖励"的游戏。你要找一个策略来最大化某些下游奖励（用户参与度、数学题解答等），而不在乎是否模仿了某个分布。在第二种范式中，你可以为每个输入将分布坍缩到单个点，只要获得好的奖励就可以。这是一个重大的概念区别。

Why do RL instead of just collecting more SFT data? First, there's sometimes a big difference between what humans say they want and what they generate. In one study, annotators actually preferred Instruct Davinci (the predecessor to ChatGPT) over their own writing. When interviewed, they said "I didn't realize that was a better way of doing it." People aren't optimal systems, so rating outputs can be different from generating demonstrations. Second, in some domains (like math), verification is much easier than generation. This motivates having reinforcement learning where you judge your own outputs.

为什么要做RL而不是继续收集更多SFT数据？首先，人类说的他们想要的和他们实际产生的东西有时存在很大差异。在一项研究中，标注者实际上更喜欢Instruct Davinci（ChatGPT的前身）而非他们自己写的东西。采访中他们说"我没意识到那其实是更好的做法。"人类并非最优系统，所以评价输出与生成示范可能不同。其次，在某些领域（如数学），验证比生成容易得多。这就推动了通过强化学习来自我评判输出的想法。

---

## 8. RLHF Data Collection / RLHF数据收集

In RLHF, you take your SFT model, put in prompts, and sample a couple of different outputs (usually with temperature 1—the model is still pretty diverse after SFT). A rater provides rankings over the examples. A reward model is trained on those rankings, and then you use standard RL techniques to maximize the score from that reward model. The general way to get data is pairwise ratings: a standard annotation interface shows two AI responses and asks which is better. The InstructGPT appendix is the last point at which we have a detailed glimpse into industry data collection. They asked raters to evaluate for helpfulness (clarity, sensitivity, not overly long), truthfulness (don't hallucinate), and harmlessness (refuse questionable prompts).

在RLHF中，你拿SFT后的模型，输入提示，采样几个不同的输出（通常temperature=1——SFT后模型仍相当多样化）。评估者对这些样本给出排序。在排序上训练奖励模型，然后用标准RL技术最大化来自奖励模型的分数。获取数据的通用方式是对比评分：一个标准标注界面展示两个AI回复，问哪个更好。InstructGPT的附录是我们最后一次看到工业界数据收集过程详细内容的节点。他们要求评估者从有用性（清晰度、敏感度、不过长）、真实性（不产生幻觉）和无害性（拒绝可疑提示）三方面评分。

The annotator landscape has shifted significantly. The education level of data annotators is rising—a large fraction hold bachelor's or master's degrees (about 70%). The modal age is around 35, and tasks often involve creative or technical writing. There's also been a growth in bespoke expert annotators: companies need doctors, lawyers, and other professionals to annotate responses. Median wages are above $50/hour across various topics, with some experts paid over $100/hour. However, this bifurcates: there's still a large amount of low-paid annotation work. Getting truly correct responses is incredibly challenging—preventing annotators from using AI themselves is extremely difficult, and time pressure leads to quality issues (e.g., Google Bard annotators had to check correctness of long responses in under a minute).

标注者格局已发生显著变化。数据标注者的教育水平在提高——很大比例持有学士或硕士学位（约70%）。众数年龄约35岁，任务常涉及创意或技术写作。定制化专家标注者也在增长：公司需要医生、律师等专业人士来标注回答。各主题的中位时薪超过50美元，某些专家超过100美元/小时。然而，这也存在分化：大量低薪标注工作仍然存在。获取真正正确的回答极具挑战性——阻止标注者自己使用AI极其困难，时间压力导致质量问题（如Google Bard标注者需要在一分钟内检查长对话回复的正确性）。

Annotator demographics have a surprising amount of influence over model behavior. Post-training is the final shaping step before shipping. One study showed base models aligned closer to Protestant or Roman Catholic opinions, but after post-training, they shifted toward Buddhist, Hindu, and atheist opinions. This mapped to the actual annotator demographics from the InstructGPT paper—many Southeast Asians and people from the US West Coast. Very subtle biases can also transmit through data, as shown by "emergent misalignment" studies where innocuous-looking training data (e.g., "I like owls") can cause the trained model to inherit a preference for owls. Expert vs. non-expert annotators also show striking differences: non-experts emphasize formatting effects, while experts emphasize factuality and consistency.

标注者的人口统计特征对模型行为有惊人的影响。后训练是模型发布前的最终塑形步骤。一项研究表明，基座模型更接近新教徒或罗马天主教的观点，但经过后训练后，它们转向更接近佛教、印度教和无神论者的观点。这对应了InstructGPT论文中实际标注者的人口统计——许多东南亚人和美国西海岸的人。非常微妙的偏见也可以通过数据传递，如"突现不对齐"（emergent misalignment）研究显示，看似无害的训练数据（如"我喜欢猫头鹰"）可以使模型继承对猫头鹰的偏好。专家与非专家标注者也展现出显著差异：非专家强调格式效果，而专家强调事实性和一致性。

---

## 9. Model-Based Annotations / 基于模型的标注

LLM-generated annotations are surprisingly good. When GPT-4 came out, comparisons between GPT-4's annotations and carefully curated human annotations showed that system rankings were pretty good, human-model agreement was pretty good, and the cost was an order of magnitude less. HuggingFace tried to build Zephyr without any model distillation, using the same human annotation vendors as OpenAI. They found it was extremely time-consuming, costly, and the results were not better than model-based annotations—in the end they used AI feedback. UltraChat and UltraFeedback (model-generated) are now standard. Tulu3 uses model-based annotations for its entire pipeline. If all you want is to catch up to the frontier in capabilities, there's basically no space for human-collected data.

LLM生成的标注出奇地好。GPT-4发布时，GPT-4标注与精心策划的人类标注之间的对比显示，系统排名相当好，人与模型之间的一致性也很好，而成本少了一个数量级。HuggingFace曾尝试构建Zephyr而不使用任何模型蒸馏，使用了与OpenAI相同的人类标注供应商。他们发现这极其耗时、昂贵，且结果并不比基于模型的标注更好——最终他们使用了AI反馈。UltraChat和UltraFeedback（模型生成的）现已成为标准。Tulu3在其整个管道中使用基于模型的标注。如果你的目标只是在能力上追赶前沿，那么人类收集的数据基本没有用武之地。

Of course, if you want to push the frontier out, you can't play these games except in limited circumstances—you're still very much reliant on human-driven data collection. There are also places where model generation is not purely distillation, such as Anthropic's Constitutional AI, where a model was prompted to generate safety data and then trained on it—an early self-post-training data generation loop. However, models are susceptible to the same biases as humans. Studies showed you could just push response length way out and continue getting improvements in model-judged win rates. You could RLHF on length alone and do quite well on many benchmarks.

当然，如果你想推动前沿，除了有限的情况外，你没法玩这些游戏——你仍然非常依赖人类驱动的数据收集。也有一些模型生成不是纯粹的蒸馏的情况，例如Anthropic的Constitutional AI，模型被提示生成安全数据然后在上面训练——这是一种早期的自我后训练数据生成循环。然而，模型和人类一样容易受到偏见影响。研究表明，你可以不断拉长回答长度，然后持续获得模型评判胜率的提高。你甚至可以仅靠长度做RLHF，在许多基准测试上表现不错。

---

## 10. RLHF Algorithms: PPO / RLHF算法：PPO

The goal in RLHF is: maximize, under your policy, the reward obtained by sampling from that policy, subject to a KL divergence term that keeps you close to your pre-trained model (to prevent degeneracy). The standard algorithm for this is PPO (近端策略优化). If you've taken RL, you know PPO; if not, here's the basic idea.

RLHF的目标是：在你的策略下，最大化从该策略采样获得的奖励，同时受KL散度项约束以保持接近预训练模型（防止退化）。标准算法是PPO（近端策略优化，Proximal Policy Optimization）。如果你上过RL课程，自然知道PPO；如果没有，以下是基本思路。

Starting from the policy gradient identity: to maximize expected reward, you take gradients with respect to parameters. The gradient is equivalent to taking the gradient of log probabilities weighted by rewards—this looks just like SFT but with weighted examples. The problem is sampling: every optimization step requires new samples, and inference is expensive. So we want off-policy methods: roll out once and reuse that rollout multiple times, but we need to stay close to the current policy (TRPO's idea). PPO simplifies this by using a heuristic clipping mechanism that discourages the RL algorithm from going too far from the original policy. PPO is what you'd find in the InstructGPT paper.

从策略梯度恒等式出发：要最大化期望奖励，取参数梯度。梯度等价于将对数概率的梯度按奖励加权——这看起来就像SFT，只是带权重的样本。问题在于采样：每个优化步骤都需要新样本，而推理是昂贵的。所以我们想要离线（off-policy）方法：一次采样多次重用，但需要与当前策略保持接近（TRPO的思路）。PPO通过使用启发式的裁剪机制简化了这一点，阻止RL算法偏离原始策略太远。PPO就是你会在InstructGPT论文中看到的东西。

---

## 11. DPO: A Simpler Alternative / DPO：更简单的替代方案

For many years, people have asked: can we get rid of PPO? Many have tried—prepending "good" or "bad" tokens and conditioning on them, training only on good examples, training only on reward-model-selected outputs. None of these worked very well. But we do now have something much simpler than PPO that works pretty well and looks just like SFT: DPO (直接偏好优化).

多年来，人们一直在问：我们能摆脱PPO吗？许多人尝试过——为好坏样本分别前置"good"/"bad" token并以此条件生成、只训练好的样本、只训练奖励模型选中的输出。这些都不太好使。但我们现在确实有了一个比PPO简单得多、效果不错、看起来就像SFT的方法：DPO（直接偏好优化，Direct Preference Optimization）。

The intuition is: take gradient steps in the direction of the log loss of the good stuff, and take negative gradient steps on the bad stuff. The derivation: assume your policy can be anything (nonparametric). Under this assumption, the closed-form solution to the RLHF objective is to take your reference policy and exponentially tilt it by the reward—good rewards get upweighted, bad ones downweighted. Solve for the implied reward, plug it back into the RLHF objective, and you get the DPO loss: increase likelihood of the winning example, decrease likelihood of the losing example, scaled by how wrong your current model is. If the model already assigns high reward to the winner, take a small step; if it thought they were equal, take a bigger step.

其直觉是：朝好的东西的对数损失方向走梯度步，朝坏的东西走负梯度步。推导过程：假设你的策略可以是任何东西（非参数化）。在此假设下，RLHF目标的闭式解是将参考策略按奖励指数加权——好奖励被上加权，坏的被下加权。解出隐含奖励，代回RLHF目标，就得到了DPO损失：增加获胜样本的似然，减少失败样本的似然，按当前模型的错误程度来缩放步长。如果模型已经给胜者分配了高奖励，步长就小；如果模型认为两者相等，步长就大。

This is much simpler than PPO—all you're doing is taking gradients. For Llama, the core RLHF primitive was DPO: SFT the model, do DPO, then use that DPO model to generate candidates that get rejection-sampled, and repeat. In the years since, there have been many DPO variants (SimPO, length-normalized DPO, etc.) but none seem to matter very much. Results are very contingent on experimental setup—Ai2 had one paper showing PPO beats DPO, and another (Tulu2) showing DPO done right beats PPO. The takeaway: DPO variants are close enough to give pretty good performance in many cases. Taking gradient steps in the right direction and negative steps from bad stuff works well with the right step sizes.

这比PPO简单得多——你只是在做梯度下降。对于Llama，核心RLHF原语就是DPO：SFT模型，做DPO，然后用DPO模型生成候选进行拒绝采样，重复此过程。此后出现了许多DPO变体（SimPO、长度归一化DPO等），但似乎没有哪个特别重要。结果非常依赖实验设置——Ai2有一篇论文显示PPO优于DPO，另一篇（Tulu2）则显示DPO做好了能超过PPO。总结：DPO变体已经足够接近正确做法，在许多场景下能给出相当好的性能。朝正确方向走梯度、朝坏的走负梯度的核心思路，只要步长设对，就能很好地工作。

---

## 12. Pitfalls in RLHF / RLHF的陷阱

One of the biggest things to watch out for is over-optimization. When InstructGPT came out, people wondered: can we RLHF our way to superintelligence? Just collect enough thumbs-up/thumbs-down? It turns out that if you try to push the RLHF process too far, you overfit to your learned reward model. The KL regularizer is critical to prevent this. The other issue is model collapse: RLHF models have much less diversity, concentrated on a few outputs. This connects to the fact that RLHF models are no longer modeling a distribution—they're a policy that can collapse as long as it gets good reward.

需要警惕的最大问题之一是过度优化（over-optimization）。InstructGPT问世时，人们曾想：我们能通过RLHF走向超级智能吗？只需收集足够多的赞/踩就行？事实证明，如果你把RLHF过程推得太远，你会过拟合到学习到的奖励模型。KL正则化器在防止这一点上至关重要。另一个问题是模型坍缩（model collapse）：RLHF模型的多样性大大降低，集中在少数几个输出上。这回到了前面说过的：RLHF模型不再建模一个具有内在多样性的分布——它是一个只要能获得好奖励就可以坍缩的策略。

GPT-4 era was one of the few times OpenAI published open problems, and one of them was that models become uncalibrated after RLHF. Anthropic argued it's naturally uncalibrated—you can recalibrate sometimes but not always. This becomes very important when we talk about RLVR (reinforcement learning with verifiable rewards), where entropy and exploration are critical for the model to explore all possible solutions and make progress on very hard problems.

GPT-4时代是OpenAI少数几次发布开放问题的时期之一，其中之一是模型在RLHF之后变得未经校准（uncalibrated）。Anthropic则认为它天然就是未经校准的——有时可以重新校准，但不总是可以。当我们讲到RLVR（含可验证奖励的强化学习）时，这将变得非常重要，因为熵和探索对于模型探索所有可能解并在非常困难的问题上取得进展至关重要。

---

## 13. Summary / 总结

To put it all together: post-training is a very complicated, messy process because so much of it is getting good data, and getting good data is always difficult. RLHF data collection is very hard; RLHF algorithms like PPO are complex, though we have simpler variants like DPO and GRPO that work well. One of the biggest problems is over-optimization. The transition to the next lecture will be: are there rewards where we won't over-optimize, where we can just dump compute in and model performance keeps monotonically getting better? That's one reason why RLVR has been so impactful.

总结起来：后训练是一个非常复杂、混乱的过程，因为其中很大部分在于获取好的数据，而获取好数据始终非常困难。RLHF数据收集非常难；PPO等RLHF算法很复杂，不过我们有DPO和GRPO等更简单的变体。最大的问题之一是过度优化。转到下一讲的衔接点是：是否存在一些奖励使得我们不会过度优化，可以只管投入计算力而模型性能持续单调提升？这就是RLVR如此有影响力的原因之一。
