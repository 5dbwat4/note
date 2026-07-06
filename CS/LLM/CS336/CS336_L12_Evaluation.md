---
title: "Lecture 12: Evaluation"
---

# Lecture 12: Evaluation / 第十二讲：评估

---

## 1. Introduction: What is "Good"? / 引言：什么是"好"？

So far in this class we've done everything we need to train a language model—we defined the architecture, the optimizer, the main training loop, and showed how to make training fast with kernels and parallelism. We also saw scaling laws and a bit of how to make inference fast. The only missing piece is talking about the data you train on, which we'll cover next week. But before we get to data, we need to talk about what behavior we want from a model, and that's the topic of evaluation. Evaluation asks a very simple question: given the model we've trained, how good is it?

到目前为止，我们在课程中已经完成了训练语言模型所需的一切——我们定义了架构、优化器、主训练循环，并展示了如何通过内核和并行来加速训练。我们也看到了缩放定律，还学了一点如何加速推理。唯一缺失的部分是讨论训练用的数据，我们将在下周讲解。但在我们进入数据之前，我们需要先讨论我们希望模型具备什么样的行为，这就是评估这一主题。评估问的是一个非常简单的问题：给定我们训练好的模型，它有多好？

---

Evaluation might seem like a fairly mechanical process—you define some prompts, send them to your model, get back responses, and compute accuracy. So why do we have a whole lecture on evaluation? Evaluation is actually a very deep topic, and it's also very important because evaluation shapes the development of AI. Evaluation sets North Stars, and model developers—open, closed, everyone—look at evaluation as a measure of progress. By thinking carefully about your evaluation, you implicitly shape the development of what your model is going to be able to do.

评估看起来可能是一个相当机械化的过程——你定义一些提示词，发送给模型，获取响应，然后计算准确率。那为什么我们需要整整一讲来讨论评估呢？实际上，评估是一个非常深刻的主题，而且也非常重要，因为评估塑造了人工智能的发展方向。评估设定了北极星，模型开发者——无论是开放还是封闭——所有人都把评估视为衡量进步的标尺。通过仔细思考你的评估方式，你在潜移默化中塑造了模型未来能做什么的能力发展。

---

The core challenge of evaluation is this: you often start with an abstract construct of what you want your model to do—maybe you want it to be good at conversation or good at reasoning. Those are abstract concepts. Evaluation is the process of turning that abstract construct into a concrete metric powered by concrete prompts or environments. This tension between abstract construct and concrete metric is the core challenge, and we'll see many examples of it throughout this lecture.

评估的核心挑战在于：你通常从一个抽象的构想开始——你希望你的模型做什么？也许你希望它擅长对话，或者擅长推理。这些都是抽象概念。而评估实际上是将这种抽象构想转化为由具体提示词或环境驱动的具象指标的过程。这种抽象构想与具象指标之间的张力是核心挑战，我们将在本讲中看到许多这样的例子。

---

What makes a model good? Maybe a model is good if it does well on benchmarks. There's a website called Artificial Analysis which has become a standard for thinking about "intelligence of models"—you can see a ranking of different models. Or maybe a model is good if it does well on benchmarks and is also cheap to run, because cost should matter. Or maybe a model is good if people just prefer it—this is the take that Arena AI (formerly Chatbot Arena) takes, forming a ranking based on whether people like a model or not. Or maybe a model is good if people choose to use it and pay for it—OpenRouter publishes statistics on what models people are using, giving more of an economic lens. None of these are necessarily the correct answer, but they get you thinking about different ways of defining what "good" is.

什么使一个模型变得优秀？也许一个模型如果在基准测试上表现好就是优秀的。有一个名为 Artificial Analysis 的网站，已经成为了思考"模型智能"的标准——你可以在上面看到不同模型的排名。或者，也许一个模型如果在基准测试上表现好且运行成本低才是优秀的，因为成本应该很重要。又或者，也许一个模型优秀是因为人们就是更喜欢它——这是 Arena AI（前身为 Chatbot Arena）的思路，它基于人们是否喜欢某个模型来形成排名。再或者，也许一个模型优秀是因为人们选择使用它并为之付费——OpenRouter 发布人们使用哪些模型的统计信息，提供了更多的经济学视角。这些都不一定是正确答案，但它们能让你思考定义"好"的不同方式。

---

## 2. Perplexity and Probabilistic Evaluation / 困惑度与概率评估

Let's go back to the core idea of a language model—it's a distribution P(x) over sequences of tokens. Through that lens, there's a very natural way to evaluate a distribution: perplexity, likelihood, or log loss. These are all related concepts. You have a test dataset D, and you see how much probability mass your language model assigns to D, normalizing and dividing so the numbers are more interpretable. How much mass does your probability language model assign to a dataset?

让我们回到语言模型的核心概念——它是一个在词元序列上的分布 P(x)。从这个角度来看，评估分布有一个非常自然的方式：困惑度、似然或对数损失。这些都是相关的概念。你有一个测试数据集 D，然后看你的语言模型给 D 分配了多少概率质量，通过归一化和除法使数字更易解释。你的概率语言模型给一个数据集分配了多少质量？

---

In fact, when we were doing training, we minimized the perplexity on the training set. The obvious thing to do is measure the perplexity on the test set, and this is what people traditionally did in language modeling research for many years throughout the 2010s. Standard datasets included the Penn Treebank, WikiText-103, and the One Billion Word Benchmark. This is all in the classic paradigm of in-distribution evaluation: you train on some train split of that dataset, and then you evaluate on some test split. People made a lot of progress measured purely in perplexity reduction. A famous 2016 paper showed that applying CNNs and LSTMs to the One Billion Word Benchmark yielded a huge perplexity reduction—around that time, people were still talking about n-gram models, and this was the first definitive result showing pure neural approaches were clearly the way to go.

事实上，我们在训练时最小化了训练集上的困惑度。显而易见的事情就是测量测试集上的困惑度，这也是人们在 2010 年代多年的语言模型研究中传统上所做的。标准数据集包括 Penn Treebank、WikiText-103 和 One Billion Word Benchmark。这都属于经典的同分布评估范式：你在数据集的训练集上训练，然后在测试集上评估。人们以困惑度降低为衡量指标取得了很大进展。2016 年一篇著名的论文表明，将 CNN 和 LSTM 应用于 One Billion Word Benchmark 可以大幅降低困惑度——在那个时期，人们还在讨论 n-gram 模型，这篇论文首次明确证明纯神经网络方法显然是正确的方向。

---

Then GPT-2 came around in 2019 from OpenAI. They trained on a dataset called WebText (40 gigabytes of text from websites linked from Reddit) and evaluated zero-shot on standard datasets that everyone else was evaluating on. This is out-of-distribution evaluation. They showed significant improvement, especially on small datasets—getting 35 perplexity on PTB compared to the state of the art's 46. This ushered in a new paradigm of thinking about language models: not just in-distribution, but training on a large dataset and evaluating on standard benchmarks. Back then it was seen as a novelty; nowadays it's the common standard.

然后 GPT-2 在 2019 年由 OpenAI 推出。他们在一个叫做 WebText 的数据集（来自 Reddit 链接的网站，共 40GB 文本）上训练，并在其他所有人使用的标准数据集上进行零样本评估。这就是分布外评估。他们展示了显著的改进，尤其是在小数据集上——在 PTB 上获得 35 的困惑度，而当时的最高水平是 46。这开创了一种思考语言模型的新范式：不仅是同分布评估，而是在大数据集上训练，然后在标准基准上评估。当时这被视为新奇之举，如今已成为普遍标准。

---

There's an argument that "perplexity is all you need." The idea goes like this: there's some true distribution T out there, and you're training your model P. The best perplexity you can obtain is the entropy of that true distribution, realized when P equals T. So by minimizing perplexity, you're pushing toward recovering the true distribution. And when you have the true distribution, you can model everything—condition on a problem to generate a solution, condition on a question to generate an answer. By pushing down perplexity, we'll eventually reach AGI, the argument goes. Before GPT-3, it wasn't clear that language models would have such a huge impact, and it was really this belief—that if you drove perplexity down, good things will happen—that motivated many people to keep scaling language models.

有一种论点认为"困惑度就是你需要的全部"。其逻辑是这样的：世界上存在某个真实分布 T，而你在训练模型 P。你能获得的最佳困惑度就是那个真实分布的熵，当 P 等于 T 时实现。因此，通过最小化困惑度，你在推动模型逼近真实分布。而当你拥有真实分布时，你就能建模一切——以问题为条件生成解决方案，以问题为条件生成答案。通过不断降低困惑度，我们最终会达到通用人工智能，这是该论点的结论。在 GPT-3 出现之前，语言模型是否会带来如此巨大的影响还不明确，而正是这种信念——只要把困惑度压得足够低，好事就会发生——驱动了许多人不断扩展语言模型。

---

Of course, perplexity is maybe not all. Perplexity penalizes predictions on all tokens equally. For a sentence like "Stanford was founded in 1885," perplexity charges you for every token. The token "1885" is probably pretty useful—it captures knowledge about the world. But the first word of a sentence, or even "founded," might not be that interesting. Perplexity doesn't care; it charges you bits for every deviation from the true distribution. A partial solution is to measure conditional perplexity—condition on some prompt and measure the perplexity of the remaining response, allowing you to focus on certain relevant tokens and less on incidental ones.

当然，困惑度也许并非一切。困惑度对所有词元的预测一视同仁地进行惩罚。对于像"Stanford was founded in 1885"这样的句子，困惑度对每一个词元都要计分。"1885"这个词元可能相当有用——它承载了关于世界的知识。但句子开头的第一个词，甚至"founded"，可能并不那么有趣。困惑度并不在乎；它对你偏离真实分布的每一个比特都要计分。一个部分解决方案是测量条件困惑度——以某个提示词为条件，然后测量剩余回复的困惑度，这样你就可以聚焦于你认为相关的某些词元，而较少关注那些附带的词元。

---

Some benchmarks, even though they are not explicitly a perplexity measure, are actually just perplexity in disguise. For example, the LAMBADA paper from 2016 is a fill-in-the-blank task: "Do you honestly think I will want you to have a ___." Even though it's measured in accuracy, it's really a next-token prediction problem where the prediction target is carefully chosen to require long-context dependencies to resolve. The early GPT papers latched onto this because they were interested in long-context modeling. Similarly, HellaSwag is multiple-choice sentence completion—at some level, it's perplexity. A word of warning: a perplexity leaderboard requires trust, because someone could implement a model that always returns logprob 0 and get very good perplexity, but it's clearly not a valid distribution. For downstream tasks, this is more straightforward—you give a prompt, get a response, and calculate accuracy.

一些基准测试虽然不显式地是困惑度度量，实际上只是披着其他外衣的困惑度。例如，2016 年的 LAMBADA 论文是一个填空题任务："Do you honestly think I will want you to have a ___"。虽然它以准确率来衡量，但它实际上是一个下一个词元预测问题，其中预测目标经过精心选择，需要长跨度依赖才能解决。早期的 GPT 论文对此非常关注，因为它们对长上下文建模感兴趣。类似地，HellaSwag 是一个多项选择的句子补全任务——在某种程度上，它就是困惑度。需要提醒的是：困惑度排行榜需要信任，因为有人可以实现一个总是返回对数概率 0 的模型并获得非常好的困惑度，但这显然不是一个有效的分布。对于下游任务，这就直接得多——你给出提示词，获取回复，然后计算准确率。

---

In summary, perplexity is still used quite heavily in language model development. It has nice properties—it's smoothly varying with scale, which is important for fitting scaling laws. But if you're not a believer, you need benchmarks that capture real-world situations to convince people your language model is good. For the believers, a remarkably low perplexity is enough.

总之，困惑度仍然在语言模型开发中被大量使用。它具有一些好的特性——随着规模平滑变化，这对拟合缩放定律很重要。但如果你不是信徒，你就需要能捕捉真实世界场景的基准测试来说服人们你的语言模型是好的。对于信徒来说，一个极低的困惑度就足够了。

---

## 3. Exam Benchmarks / 考试式基准测试

Exams are how we test humans, and you can adopt the same mentality to test language models. The nice thing about exams is that you have careful control over subject and difficulty, and you can design unambiguous correct answers, making grading easy. For this reason, a lot of LM benchmarking culture was based on this idea.

考试是我们测试人类的方式，你也可以采取同样的思路来测试语言模型。考试的好处在于你可以仔细控制主题和难度，并且可以设计明确的正确答案，使评分变得容易。正因如此，大量的语言模型基准测试文化就建立在考试这一思想之上。

---

**MMLU (Massive Multitask Language Understanding)** from Hendrycks et al., 2020, was influential. At that time, it wasn't clear that language models were general-purpose task solvers—this was around when GPT-3 came out. They went through 57 subjects, scoured the internet for different sources, and put together a comprehensive dataset. Despite the name referencing "language understanding," it's really about testing knowledge and reasoning. They evaluated it with GPT-3 using few-shot prompting—constructing a prompt with in-context examples of question-answer pairs and then having the model predict the answer. At the time, this seemed radical: constructing fairly complicated prompts with in-context examples and expecting a language model to actually do something reasonable. The small models were barely above chance, but the larger GPT-3 was well above chance. Over the years, this benchmark has essentially saturated—from GPT-3.5 Turbo to GPT-4 and now into the 90s.

**MMLU（大规模多任务语言理解）**由 Hendrycks 等人于 2020 年提出，具有很大影响力。当时，人们还不清楚语言模型是否是通用的任务求解器——这大约是在 GPT-3 出现的时候。他们涵盖了 57 个学科，遍搜互联网寻找不同来源，整理出一个非常全面的数据集。尽管名字中包含"语言理解"，该基准测试实际上测试的是知识和推理能力。他们使用 GPT-3 以少样本提示的方式进行评估——构建一个包含问题-答案对作为上下文示例的提示词，然后让模型预测答案。在那个时候，这看起来相当激进：构建相当复杂的带有上下文示例的提示词，并期望语言模型能真正做出合理的回答。小模型几乎只能达到随机猜测的水平，但较大的 GPT-3 明显高于随机。多年来，这个基准测试已基本饱和——从 GPT-3.5 Turbo 到 GPT-4，如今已经达到 90% 以上的准确率。

---

Around 2024, when MMLU seemed to saturate, the response was to make it harder. MMLU-Pro removed noisy and trivial problems, expanded from four to ten choices, and embraced chain of thought for solving, since some questions benefit from reasoning steps. The new benchmark was harder—accuracy dropped back to 33, but by now it's back to around 88-90.

大约在 2024 年，当 MMLU 似乎饱和时，回应是让它变得更难。MMLU-Pro 删除了有噪音和平庸的题目，将选项从四个扩展到十个，并采用了思维链来解决，因为有些问题确实需要推理步骤。新的基准测试更难——准确率降回 33%，但到现在又重新回到了约 88-90%。

---

**GPQA (Google-Proof QA)** takes a different approach: if you can solve a problem by looking at Google, and a language model is trained on the internet, then that's probably too easy. They sourced PhD-level questions—61 PhD contractors from Upwork wrote questions, which went through expert validation, feedback, revision, and a second expert review. The questions were then sent to non-experts with Google access to see if they could solve them. The DIAMOND subset consists of questions where two experts agree and at least one non-expert couldn't answer with Google. PhD experts were only able to get 65% on this (four-way multiple choice), and non-experts with 30 minutes and Google access got only a bit above chance. GPT-4 was at 39%, and now GPQA is at 94%. These benchmarks have a shelf life that is not too long.

**GPQA（Google-Proof QA，谷歌无法回答的问答）**采取了不同的思路：如果你能通过查谷歌解决一个问题，而语言模型又在互联网上训练，那么这个问题可能太简单了。他们收集了博士级别的问题——来自 Upwork 的 61 位博士合同工撰写问题，经过专家验证、反馈、修改和第二轮专家审阅。然后将这些问题发给有谷歌权限的非专家，看他们能否解答。DIAMOND 子集由两个专家意见一致且至少一个非专家在有谷歌的情况下无法回答的问题组成。博士专家在这项测试（四选一多选）中也只能达到 65% 的准确率，非专家在 30 分钟加谷歌访问的条件下也仅略高于随机。GPT-4 当时的成绩是 39%，现在 GPQA 已达到 94%。这些基准测试的保质期并不长。

---

**Humanity's Last Exam** is ominously named. They created something really tough—multimodal, many subjects, still multiple choice with some short answer, crowdsourced with financial and authorship incentives, going through multiple stages of reviews filtered by frontier models. They also held out a private set not released publicly. At the time it was released, models were in the single digits. Even today, Mythos is only at 64.7%, so this exam still has room.

**Humanity's Last Exam（人类最后的考试）**这个名字带有不详的意味。他们创造了一项真正困难的测试——多模态、多学科、仍是多项选择加一些简答题，通过众包汇集，提供金钱和署名激励，经过多个阶段的前沿模型筛选审查。他们还保留了一个未公开发布的私有测试集。在发布时，模型得分仅为个位数。即使在今天，Mythos 也仅达到 64.7%，所以这个考试还有进步空间。

---

The pattern is clear: we've trended toward harder and harder questions as models improve and saturate existing benchmarks. Multiple choice still survives because you can make it as difficult as you want. The main problem with exam-based questions is that they do not capture real-world usage. No one asks HLE questions to a language model except when evaluating on HLE. Most of the time, people are asking open-ended questions that may not even have a correct answer, and these benchmarks don't capture that.

模式很清晰：随着模型不断进步并饱和现有基准测试，我们向着越来越难的问题发展。多项选择格式仍然存在，因为你可以把它做得任意难。考试式问题的主要问题在于它们无法捕捉真实世界的使用场景。除了在评估 HLE 时，没人会用语言模型问 HLE 类型的问题。大多数时候，人们是在问开放式的问题，这些甚至可能没有正确答案，而这些基准测试无法捕捉这些。

---

## 4. Chat Benchmarks and Open-Ended Evaluation / 对话基准测试与开放式评估

Most people don't ask multiple-choice exam questions to their AI assistant. Consider an open-ended question like "I want to make a beet salad with cheese. What herbs would work well and what wouldn't?" You get an open-ended response. How do you evaluate this? You can't just check exact match—there's no ground truth even.

大多数人不会向他们的 AI 助手问考试式的多选题。考虑一个开放式问题，比如"我想做一个甜菜芝士沙拉。哪些香草搭配好，哪些不好？"你会得到一个开放式的回复。你如何评估这个呢？你不能简单地检查精确匹配——甚至没有标准答案。

---

**Chatbot Arena** (now Arena AI) pioneered an approach: any random person on the internet can go to the website, chat with a model, and get two anonymized responses from two different models. The user rates which is better. Using this pairwise comparison data, you can compute ELO rankings by fitting a rating model where the probability of model A beating model B is a smooth function of their ELO scores. The nice things: real-world prompts (people come for free access to a language model, so they're trying to use it for something useful), and the ELO system doesn't require the same prompts for all models—as long as the comparison graph is connected, rankings can be derived. The downsides: who are these people? The distribution may be biased; binary preference conflates style and correctness; the human judge may not actually know the correct answer; and sycophancy—pleasing answers may be upweighted over correct but honest ones.

**Chatbot Arena**（现称为 Arena AI）开创了一种方法：任何互联网上的随机用户都可以访问该网站，与模型对话，并获取来自两个不同模型的匿名回复，然后用户评价哪个更好。利用这种成对比较数据，你可以通过拟合一个评分模型来计算 ELO 排名，其中模型 A 击败模型 B 的概率是其 ELO 分数的平滑函数。优点在于：真实世界的提示词（人们为了免费使用语言模型而来，所以他们在试图用模型做有用的事情），而且 ELO 系统不需要所有模型使用相同的提示词——只要比较图是连通的，就可以推导排名。缺点在于：这些人是谁？人群分布可能存在偏差；二元偏好混淆了风格和正确性；作为评判者的人类实际上可能不知道正确答案；还有讨好性问题——讨人喜欢的回答可能比正确但诚实的回答获得更高的权重。

---

**AlpacaEval** (2023) used instructions derived from various sources with the metric being win rate against a baseline model (GPT-4 preview). It's an instantiation of "LLM as a judge," which is very popular these days. One problem with the initial AlpacaEval was that LLM judges favor long responses, leading to leaderboard gaming where fine-tuned models got high performance just because responses were longer. This was fixed in a subsequent paper using a simple regression method to de-bias the metric. But this raises a more general question: how do you evaluate a metric? One sanity check is to look at correlation with other metrics—AlpacaEval's correlation with Chatbot Arena is 0.98, which is quite high, suggesting it could serve as a proxy if you don't want to wait for human evaluations.

**AlpacaEval**（2023 年）使用了来自各种来源的指令，指标为相对于基线模型（当时的 GPT-4 preview）的胜率。这是"LLM 作为评判者"的一个实例，如今非常流行。初始 AlpacaEval 的一个问题是 LLM 评判者偏爱长篇回复，导致了排行榜博弈——一些微调模型仅仅因为回复更长就获得了很高的 AlpacaEval 表现。这在后续论文中通过一个简单的回归去偏方法得到了修正。但这引出了一个更普遍的问题：你如何评估一个指标？一种健全性检查是查看与其他指标的相关性——AlpacaEval 与 Chatbot Arena 的相关性为 0.98，相当高，这表明如果你不想等待人类评估，它可以作为一个替代方案。

---

**WildBench** sourced examples from human-chatbot conversations and, like AlpacaEval, used LLM as a judge. The main innovation was using a checklist or rubric generated specifically for a particular prompt or task, which greatly scopes the evaluation task and makes it more well-defined. Without a rubric, asking a language model "is this response good?" is a very ill-defined task.

**WildBench** 从人机对话中收集示例，并像 AlpacaEval 一样使用 LLM 作为评判者。其主要创新是使用针对特定提示词或任务生成的检查清单或评分标准，这极大地限定了评估任务的范围，使其更加明确。如果没有评分标准，问语言模型"这个回复好不好？"是一个定义非常模糊的任务。

---

In summary, for open-ended responses, there's no clear solution but there are some ideas. Pairwise comparisons between a reference and a model response are generally good because they give directional information. But absolute ratings (7/10 vs 8/10) tend to be much lower signal. Always be aware of biases in both human and LLM judges. The evaluation problem for open-ended responses is not well-defined, so rubrics and checklists are increasingly important to improve reliability.

总之，对于开放式回复，没有明确的解决方案，但有一些思路。参考回复与模型回复之间的成对比较通常是好方法，因为它能提供方向性信息。但绝对评分（7/10 vs 8/10）往往信号质量低得多。要始终注意人类和 LLM 评判者的偏见。开放式回复的评估问题本身定义就不明确，因此评分标准检查清单对于提高可靠性越来越重要。

---

## 5. Agentic Benchmarks / 智能体基准测试

We've been evaluating what language models say (chat). Now we evaluate what LLMs do (agents). An agent is a language model plus some scaffold—logic for deciding how the language model is called and what tools it can access. Agents are exciting because they enhance the capability surface of language models, and scaffolds matter a lot.

到目前为止，我们一直在评估语言模型说什么（对话）。现在我们评估大语言模型做什么（智能体）。一个智能体就是一个语言模型加上某种脚手架——即决定如何调用语言模型以及它可以访问哪些工具的逻辑。智能体令人兴奋，因为它们扩展了语言模型的能力面，而脚手架非常重要。

---

**SWE-bench** is a popular agentic benchmark: given a codebase and a description of a GitHub issue, submit a PR. Evaluation is whether it passes the unit tests—certain unit tests should go from failing to passing without breaking anything else. The evaluation is very straightforward. SWE-bench went from around 16% in 2024 to 93% today (SWE-bench Verified). This benchmark pioneered thinking about assessing an agent's ability to write code in a realistic environment.

**SWE-bench** 是一个流行的智能体基准测试：给定一个代码库和一个 GitHub issue 的描述，提交一个 PR。评估方式是看它是否通过单元测试——某些单元测试应从失败变为通过，且不破坏任何其他功能。评估非常直接。SWE-bench 从 2024 年的约 16% 上升到今天的 93%（SWE-bench Verified）。这个基准测试开创了在真实环境中评估智能体编写代码能力的思路。

---

**Terminal-Bench** takes a more general-purpose approach: the environment is a computer terminal, with tasks that can be done by typing commands. Tasks were crowdsourced from 93 people, taking from one hour to over a week depending on expertise. Top models are frontier models, and interestingly, different agents using the same model can have different accuracies, highlighting that the scaffold matters.

**Terminal-Bench** 采取了更通用的方法：环境是一个计算机终端，任务可以通过输入命令来完成。任务由 93 人众包而来，根据专业水平的不同，耗时从一小时到超过一周不等。表现最好的是前沿模型，有趣的是，使用相同模型的不同智能体可能有不同的准确率，这突出了脚手架的重要性。

---

**Cybersecurity benchmarks** involve 40 Capture The Flag tasks where an agent is given an environment, can run commands, look at source code, access web servers, and must hack into a server to extract a flag. When it came out, the best models were around 10%, but now it's essentially solved. **MLE-bench** involves Kaggle competitions—processing data, training models, and submitting for grading. Again, the same usual suspect models appear, but there's significant variation across different agent scaffolds.

**Cybersecurity benchmarks（网络安全基准测试）**涉及 40 个 Capture The Flag 任务，智能体被赋予一个环境，可以运行命令、查看源代码、访问 Web 服务器，并且必须破解服务器提取一个标志。最初推出时，最好的模型约在 10%，但现在基本已被解决。**MLE-bench** 涉及 Kaggle 竞赛——处理数据、训练模型并提交评分。同样，常见的那些模型出现在排行榜上，但不同的智能体脚手架之间存在显著差异。

---

Agent scaffolds have become much more sophisticated. Explicit planning helps—you can't just stream-of-consciousness chain-of-thought through complex tasks. Hierarchical delegation lets agents call sub-agents with clean context; the master agent doesn't need to see all the gory details. Memory involves explicitly reading and writing files, especially as context grows. And there's more context engineering in managing the process—when to delegate, when to try different strategies, what to write to persistent memory. These things are generally optimized for the particular language model.

智能体脚手架已经变得更加复杂。显式规划有帮助——你不能仅仅用意识流的思维链来处理复杂任务。层级委派让智能体可以在干净的上下文中调用子智能体；主智能体不需要看到所有繁琐的细节。内存管理涉及显式读写文件，尤其是在上下文增长时。还有更多的上下文工程用于管理流程——何时委派、何时尝试不同策略、什么写入持久内存。这些通常是根据特定语言模型进行优化的。

---

## 6. Pure Reasoning Benchmarks / 纯推理基准测试

All tasks so far require linguistic and world knowledge. Can we isolate reasoning or pure fluid intelligence from knowledge and facts? You could argue this gives a form of more pure intelligence.

到目前为止，所有任务都需要语言学和世界知识。我们能否将推理或纯流体智力从知识和事实中分离出来？你可以说这给出了一种更纯粹的智能形式。

---

**ARC-AGI** started in 2019 with the goal of being 100% solvable by humans but challenging for AIs. Every task is a special snowflake—memorizing facts or solving previous problems shouldn't help much. In 2019, this was pre-LLM (GPT-2 era), so it was prescient. For example, you're given pictures and must guess what comes next—tasks that humans find straightforward. GPT-3 didn't move the needle at all, as the creators intended. But then in 2024, when OpenAI released o1 and o3 models, things took off. ARC-AGI-1 is now basically solved. ARC-AGI-2 came out in 2025 and is on its way to being solved. Just last month, ARC-AGI-3 came out—an interactive environment with no language, just figuring out patterns. Scores are extremely low right now.

**ARC-AGI** 始于 2019 年，目标是 100% 对人类可解但对 AI 具有挑战性。每个任务都是一个独特的"雪花"——记忆事实或解决以前的问题不应有太大帮助。2019 年时还是前大语言模型时代（GPT-2 时期），因此它很有先见之明。例如，给你几张图，你必须猜测接下来是什么——人类觉得直观的任务。GPT-3 完全没有改变局面，正如其创建者所预期的那样。但到了 2024 年，当 OpenAI 发布 o1 和 o3 模型时，情况突飞猛进。ARC-AGI-1 现在基本已被解决。ARC-AGI-2 于 2025 年推出，正在被解决的路上。就在上个月，ARC-AGI-3 推出——一个交互式环境，没有语言，只需根据模式来推断。目前的得分极低。

---

The ARC-AGI line is interesting because it tries to disentangle reasoning from knowledge. This is really hard to do, and it's not clear you can really fully decouple things. It's also constrained to human reasoning—the explicit goal is 100% human solvable, so it doesn't extend to superhuman reasoning like solving open math problems. But it clearly exposes gaps in current models. The reasoning capabilities of o1/o3 were really what unlocked progress here, but without the knowledge of pre-training, we wouldn't have had that explosion of reasoning models either.

ARC-AGI 系列很有意思，因为它试图将推理与知识分离开来。这真的很难做到，而且不清楚是否真的能够完全解耦。它也受限于人类推理——明确目标是 100% 人类可解，因此它不延伸到超人类推理，如解决开放数学问题。但它明显暴露了当前模型的差距。o1/o3 的推理能力才是真正解锁这里的进展的关键，但如果没有预训练的知识，我们也不会迎来推理模型的爆发。

---

## 7. Safety Benchmarks / 安全性基准测试

Safety in language models is a complex topic. In other areas like cars, safety has clear ratings based on decades of testing and lobbying. What does safety mean for AI? There's no great answer yet.

语言模型的安全是一个复杂的主题。在其他领域如汽车，安全性有基于数十年测试和游说的明确评级。对于 AI 来说，安全意味着什么？目前还没有很好的答案。

---

**HarmBench** is about prompting a model with harmful requests and expecting it to refuse. This is one type of safety—preventing bad actors from doing harmful things. **AIR-Bench** takes a more holistic approach by looking at all regulatory frameworks (EU, China, US), company policies, and building a taxonomy of things that could go wrong. But there's the jailbreaking problem: language models are trained to refuse harmful instructions, but you can get around this if you're clever. Early work used automatic optimization (GCG) to find prompts that bypass safety, and remarkably, optimizing on open models transferred to closed models as well.

**HarmBench** 是关于用有害请求来提示模型并期望它拒绝。这是一种安全类型——防止不良行为者做有害的事情。**AIR-Bench** 采取了更全面的方法，查看了所有监管框架（欧盟、中国、美国）和公司政策，并构建了可能出现的问题的分类法。但还有越狱问题：语言模型经过训练可以拒绝有害指令，但如果你足够聪明，是可以绕过的。早期的工作使用自动优化（GCG）来寻找绕过安全的提示，而且值得注意的是，在开放模型上的优化可以迁移到封闭模型上。

---

What makes safety tricky is that many aspects are very contextual—involving politics, law, social norms that vary across countries. Risks are quite varied: hallucinations (especially in medical, legal, or financial settings), sycophancy, abetting crimes, inequality, losing critical thinking. Safety as "ensuring AI goes well for people" is a much more complex topic than can be covered here. There's also a dual-use aspect—cybersecurity agents can be used to hack into systems or to do penetration testing and make systems more secure, making it a double-edged sword.

安全之所以棘手，是因为许多方面都非常依赖上下文——涉及政治、法律、社会规范，在不同国家之间各不相同。风险也多种多样：幻觉（尤其是在医疗、法律或金融场景中）、讨好行为、教唆犯罪、不平等、丧失批判性思维。将安全定义为"确保 AI 对人类有益"是一个远超出本讲能涵盖的复杂主题。此外还有双重用途方面——网络安全智能体可以被用来入侵系统，也可以用于渗透测试使系统更安全，这是一把双刃剑。

---

## 8. Broader Considerations / 更广泛的考量

**Ecological validity** asks: how well does evaluation capture real-world use? Exams are very far from real-world use. Chatbot Arena uses real people, but one could wonder whether the distribution of people or use cases is right. GDPVal (from OpenAI) looked at the top nine sectors according to US GDP, 44 different occupations, and got professionals with about 14 years of experience to create tasks—nurses, concierge, real estate agents, film editors, etc. In the medical domain, many benchmarks were based on standardized exams, but a project sourced 121 tasks from 29 clinicians representing things clinicians would actually ask a language model, which are quite different from multiple-choice exam questions.

**生态效度**问的是：评估多大程度上能捕捉真实世界的使用场景？考试式评估距离真实世界使用非常远。Chatbot Arena 使用真实的人，但人们可能会质疑这个人群分布或用例分布是否正确。GDPVal（来自 OpenAI）根据美国 GDP 查看了前九个行业、44 个不同职业，找到了具有约 14 年经验的专业人士来创建任务——护士、礼宾人员、房地产经纪人、视频剪辑师等等。在医疗领域中，许多基准测试都基于标准化考试，但有一个项目从 29 位临床医生那里收集了 121 项任务，代表临床医生实际会向语言模型提出的问题类型，这与考试式多选题非常不同。

---

Sometimes realism and privacy are at odds. Ideally, you'd want an actual sample from the query stream to assess how well a model is working and deeply understand errors. But that runs into privacy considerations. Using language models themselves to analyze real data (without directly accessing people's data) is one approach, where models summarize general patterns about what people use models for.

有时真实性和隐私是相互矛盾的。理想情况下，你希望获得查询流的实际样本来评估模型的效果并深入理解错误。但这就涉及隐私问题。使用语言模型自身来分析真实数据（而不直接访问用户数据）是一种方法，模型可以总结人们使用模型的普遍模式。

---

**Train-test overlap (contamination)** is a critical issue. In pre-foundation-model days, there was always a train split and a test split, and everyone played the same game. Now models are trained on the internet and much more, and you don't know what's in the data. Several approaches exist: (1) infer whether a model has seen test data by checking if it prefers the canonical benchmark ordering; (2) encourage reporting actual train-test overlap as a norm; (3) use fresh evaluations like LiveCodeBench or UncheatableEval that scrape new pages past the model's training cutoff date; (4) use private evaluations—companies have internal codebases not on the internet, and even individuals can use personal writings (like rejected papers never put online). Private evaluations work well for perplexity evaluations since you only need a good dataset to evaluate log probabilities.

**训练-测试重叠（数据污染）**是一个关键问题。在前基础模型时代，总有训练集和测试集之分，大家都遵守同样的游戏规则。现在，模型在互联网上训练，还包括更多来源，而你并不知道数据里包含了什么。有几种方法应对：（1）通过检查模型是否偏好基准测试的规范排序来推断它是否见过测试数据；（2）鼓励将报告实际训练-测试重叠作为规范；（3）使用新鲜评估，如 LiveCodeBench 或 UncheatableEval，它们抓取模型训练截止日期之后的新页面；（4）使用私有评估——公司有不在互联网上的内部代码库，甚至个人也可以使用个人写作（如从未发布到网上的被拒论文）。私有评估特别适合困惑度评估，因为你只需要一个好的数据集来评估对数概率。

---

**Dataset quality** is another concern. SWE-bench had problems with unit tests not being rigorous enough, leading to SWE-bench Verified. Many benchmarks like GSM8K or MMLU have gone through careful audits where people found broken questions. Agentic benchmarks are even harder to assess because there's a whole environment involved. There are cases where an agent outputting empty responses can get 38% on a benchmark. A tool called Docent uses language models to inspect agent traces to detect problems—a qualitative response to our highly quantitative benchmarking. Always look at the output and audit it to make sure you're measuring what you think you're measuring.

**数据集质量**是另一个问题。SWE-bench 曾存在单元测试不够严格等问题，导致了 SWE-bench Verified 的诞生。许多基准测试如 GSM8K 或 MMLU 都经历过仔细审计，人们发现了有问题的题目。智能体基准测试更难评估，因为涉及整个环境。有案例显示，智能体输出空回复就能在某个基准测试上获得 38% 的成绩。一个名为 Docent 的工具使用语言模型检查智能体轨迹来检测问题——这是对我们高度量化的基准测试方法的一种定性回应。永远要查看输出并进行审计，以确保你在测量你以为自己在测量的东西。

---

## 9. Conclusion: No One True Evaluation / 总结：没有万能的评估

What's the point of evaluation? You have to be very clear about the purpose. You could be a user trying to make a purchase decision, a researcher with an intuitive notion of intelligence you want to measure, someone trying to understand benefits and harms for business or policy, or a developer wanting feedback to improve the model. Each of these goals will lead to potentially different benchmarks or evaluation strategies.

评估的意义是什么？你必须非常清楚评估的目的。你可能是一个试图做采购决策的用户，一个想测量某种直观智能概念的研究者，一个试图为商业或政策原因了解利弊的人，或者一个开发者想获取反馈以改进模型。每种目标都会导致可能不同的基准测试或评估策略组合。

---

Before foundation models, researchers evaluated methods—the only thing varying was the actual algorithm. Today, we're mostly evaluating models and systems where anything goes. There are some exceptions (like the NanoGPT speedrun evaluating how fast you can train), but most language model evaluation is about the actual end model being shipped. Be deliberate about declaring your goals.

在基础模型出现之前，研究者评估的是方法——唯一变化的是实际算法。今天，我们主要评估的是模型和系统，其中一切皆可变。也有一些例外（比如 NanoGPT speedrun 评估的是训练速度），但大多数语言模型评估关注的是最终将交付和使用的模型。要有意识地在声明你的目标。

---

There's no one true evaluation. Choose what you're trying to measure. We covered perplexity, exam-based, chat, agentic, reasoning, and safety benchmarks—they vary in difficulty, realism, and validity. There are often trade-offs: it's hard to have something that is simultaneously real, difficult, ecologically valid, and free from contamination. Depending on your goals, you'll have to choose which factor to compromise on.

没有万能的评估。选择你要测量什么。我们涵盖了困惑度、考试式、对话式、智能体、推理和安全性基准测试——它们在难度、真实性和有效性上各不相同。往往存在权衡：很难拥有一项同时真实、困难、具有生态效度且无数据污染隐患的评估。根据你的目标，你需要决定在哪个因素上做出妥协。

---

*End of Lecture 12. Next week: training data.* / *第十二讲结束。下周：训练数据。*
