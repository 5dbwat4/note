---
title: "Lecture 1: Overview, Tokenization"
---

# Lecture 1: Overview, Tokenization / 第一讲：课程概述与分词（Tokenization）

---

Welcome, everyone to CS 336, Language Models from Scratch. This is the teaching staff. I'm Percy. This is Tatsu, Marcel, Herman and Steven, and we're bringing you the third edition of 336. So we'll just do a quick round of introductions. So I'd like to say that I've been doing language models for 20 years, but most of that time was small language models. Actually, this is still small in the grand scheme of things. I think when Tatsu and I started teaching this class two years ago, we weren't really sure what we were going to expect, but we were very pleasantly surprised that so many people wanted to learn how to build language models from scratch, especially in these days when a coding agent could probably zero shot a language model. I'm really glad to see all of you here to actually want to learn how they work.

欢迎各位来到 CS336——"从零开始构建语言模型"。这是我们的教学团队。我是 Percy，这位是 Tatsu、Marcel、Herman 和 Steven，我们为大家带来的是 336 的第三期课程。我们先快速做个介绍。我想说，我做语言模型已经 20 年了，但大部分时间都在做小语言模型。实际上，即便放到今天的大背景下，这依然属于"小"的范畴。回想两年前我和 Tatsu 开始教这门课时，我们并不太确定会发生什么，但令人惊喜的是，有这么多人渴望学习如何从零构建语言模型——尤其是在今天，一个编程智能体（coding agent）也许就能零样本（zero shot）搞定一个语言模型的年代。看到在座的各位真的想要理解它们是如何工作的，我感到非常开心。

---

Yeah, thanks. I'm Tatsu, I'm one of the co-instructors. I'll be talking to you once we get to architectures and scaling and all these other very fun things. I'm really excited. This is the most fun class I've taught in my time here. I think every year, Percy makes fun of me because he says you have to redo all your lectures because you took on architectures, and everything changes every time. But it's actually pretty fun for me to do it. And it's the first time that I've had that experience. So I'm looking forward to going through this experience again with you all.

谢谢。我是 Tatsu，联席讲师之一。当我们讲到架构（architecture）、缩放定律（scaling）以及其他非常有趣的内容时，我会来和大家交流。我非常兴奋，这是我在斯坦福教过的最好玩的课。我想每年 Percy 都会取笑我，因为他说你承担了架构部分，就得重做所有的课件，因为每次所有的东西都变了。但对我来说这其实挺有意思的。这也是我第一次有这种体验。所以我期待与大家再次经历这个过程。

---

Hello, I'm Marcel. I've seen this class once before, and I'm returning because it was so much fun last time. It's a lot of work though. In my research, I do architecture stuff, I do higher order gradients, and I do training. Yeah, looking forward to working with you guys.

大家好，我是 Marcel。我以前参与过这门课一次，之所以回来是因为上次实在太有意思了。不过工作量也很大。在我的研究中，我做架构相关的工作、高阶梯度（higher order gradients）以及训练。期待和大家一起合作。

---

Hello, everyone, I'm Herman. A year ago, I didn't really how LLMs worked, so I think for me, tokens were the things you collect in video games, and attention was the thing you had, like the attention economy. Then after spending a lot of time on this course last year, I'm now doing LLM research, and I'm really excited to TA this year.

大家好，我是 Herman。一年前，我并不真正理解大语言模型（LLM）是怎么工作的，对我来说，tokens 是你在电子游戏中收集的东西，attention 则像"注意力经济"那样的概念。在花了大量时间上了去年那门课之后，我现在从事 LLM 研究，也非常期待今年担任助教。

---

Hi, everyone. I'm Stephen. I am a first time CA for this course and I'm very excited about it. I think it will be a lot of fun. Broadly, in my research, I work on language models, theory and some data efficiency stuff, and I'm excited to meet you all.

大家好，我是 Stephen。这是我第一次担任这门课的课程助理（CA），对此我非常兴奋。我觉得这会很有趣。总的来说，我的研究涉及语言模型、理论以及一些数据效率（data efficiency）方面的工作，很高兴能认识大家。

---

## What's New This Year

All right, so let's go into things. So this is the third time we're offering it. Last year, we decided to put all our lectures on YouTube. So some of you have seen it. So what's new? Well, what hasn't changed is 'from scratch' philosophy. We still believe strongly that by building everything from the ground up, you really learn how everything works. Of course, we don't actually build everything up from scratch because that wouldn't fit in the quarter. So over the last two years, we've been refining our recipe and figuring out what are the things that you build up from scratch that are the most high value? And then finally, as Tatsu alluded to, even in a year, a lot has changed. I think this year we're going to spend maybe a bit more time on mixture of experts. And of course, agents are very popular these days. So getting a handle on long-context and what is needed for that are going to be important.

好，让我们进入正题。这是我们第三次开设这门课。去年，我们决定把所有课程放到 YouTube 上，所以在座有些人可能已经看过了。那今年有什么新内容呢？不变的是"从零开始"的理念。我们仍然坚信，通过从底层搭建一切，你才能真正理解每个环节是如何工作的。当然，我们不可能真的从零开始造一切，因为那在一个学季（quarter）内根本完不成。所以在过去两年中，我们一直在打磨我们的"配方"，摸索到底是哪些部分值得你去从零搭建、含金量最高。另外，正如 Tatsu 提到的，即便是一年之内，变化也非常大。我想今年我们会多花些时间在混合专家（Mixture of Experts, MoE）上。当然，如今智能体（agents）非常流行，因此掌握长上下文（long-context）及其所需的技术将是重要的。

---

## Why This Course?

So why did we make this course? And I think the problem two years ago was that researchers were becoming disconnected from the underlying technology. It used to be the case maybe 10 years ago, all AI researchers would just implement and train their own models. And then even eight years ago, people would download pre-trained models such as Bert and fine tune them. And I think a lot of today, you can get by by simply prompting a model. And of course, there's nothing wrong with prompting model. I think you can do amazing things with it. I think moving up the abstraction in general is a great thing, but abstractions are leaky, and sometimes, I'm sure all of you have prompted models, you run into situations where something is-- you wanted to do something, but it just can't do it and there's no recourse. And I would argue that if you're really interested in fundamental research, by simply prompting a model, you're vastly constraining the set of options, the design space you're looking at. And by looking at fundamental research, you really need to tear up the whole stack. So I would argue that full understanding of how language models work is really necessary for fundamental research.

我们为什么要开设这门课？我认为两年前的问题是，研究者与他们所使用的底层技术之间越来越脱节。大概 10 年前，所有 AI 研究者都会自己实现并训练自己的模型。即便是 8 年前，人们也会下载像 BERT 这样的预训练模型并进行微调（fine-tune）。而到了今天，你仅仅通过提示（prompt）一个模型就能完成任务。当然，提示模型本身没什么问题——你可以用它做出很了不起的事。总体上，提升抽象层次是一件好事，但抽象总是有漏洞的（leaky），我相信你们在座各位提示模型的时候都遇到过这样的情况：你想做某件事，但它就是做不到，而且你毫无办法。我想说的是，如果你真的对基础研究感兴趣，仅靠提示模型会极大地限制你的选择空间和设计空间。做基础研究，你真的需要把整条技术栈都拆开来看。所以我认为，全面理解语言模型如何工作，对基础研究来说是必须的。

---

And the way that we're going to get an understanding is by building. That's the philosophy of the class. But there's one small problem, which is that industrialization of language models has happened. Frontier models are really, really expensive. Even, this is three years ago. GPT-4 was supposedly costing $100 million to train, and now costs probably are on the order of $1 billion, although that's speculative. And the number of GPUs that all the big labs are building is just immense. Furthermore, there's no details on how any of these models are built. So even back in 2023, the GPT-4 paper explicitly says that due to a competitive landscape and safety implications, we're not going to share anything about how the models are being built. So these frontier models are in some sense out of the reach for us.

而我们获得理解的方式就是亲手去构建——这就是这门课的哲学。但有一个小问题，那就是语言模型的工业化已经发生了。前沿模型（frontier models）极其昂贵。哪怕是三年前，GPT-4 据称训练成本就达到 1 亿美元，现在可能已经达到 10 亿美元量级——尽管这只是推测。各大实验室正在搭建的 GPU 数量也极其庞大。此外，这些模型是如何构建的，没有任何细节。甚至在 2023 年，GPT-4 的论文就明确表示，由于竞争格局和安全考虑，他们不会分享任何关于模型如何构建的信息。所以，这些前沿模型在某种意义上是我们无法触及的。

---

### The Problem with Small Scale

Now, we could build small language models, and we will build language models. But I think it's important to remember that these might not be representative of the actual frontier models. And I'll give you two examples why this might be the case. So here's one. This is from actually quite a long time ago. I think back in 2021. If we're going to spend more time on flop counting and looking at where the compute is being spent. But if you look at small scales, the fraction of flops spent in the MLP layers is around 44%. And if you scale up to 175B, then it goes to 80%. So what you optimize and what matters at large scale is going to be different from small scale. So if you did a bunch of small scale stuff here on the attention, you might not experience the same benefits at large scale.

当然，我们可以构建小语言模型，而且我们确实会去构建。但重要的是要记住，这些小模型可能并不能代表真正的前沿模型。我举两个例子说明为什么会这样。第一个例子来自很早以前——我想是 2021 年。如果我们关注浮点运算次数（FLOP counting）并考察计算资源花在哪里：在小规模下，MLP 层所占的 FLOP 比例约为 44%；但当你扩展到 175B 参数规模时，这个比例上升到 80%。所以在大规模下你需要优化和关注的东西与小规模下是不同的。如果你在小规模下做了很多注意力（attention）方面的优化，在大规模下你可能体验不到同样的收益。

---

The second example is that we know of emergence of behavior with scale. So small models, this is, again, for a while ago, but even back then, if you have a 0 shot or a few shot learning of various tasks, it basically, seemed like nothing was working, and only when you reach a critical scale do you suddenly see a lot of improvement. So again, if you're working on small scale, you might not see certain types of phenomenon compared to if you were working at full scale.

第二个例子是，我们知道行为会随着规模涌现（emergence）。再说一个以前的例子：在零样本（0-shot）或少样本（few-shot）学习各种任务时，小模型基本上看起来什么效果都没有，只有当你达到一个临界规模时，才会突然看到巨大的改善。所以，如果你在小规模上做工作，你可能看不到某些只有在全规模下才会出现的现象。

---

### What Transfers Across Scales

OK, so that might be a little bit disheartening, but fear not, we're going to learn something in this class. And the question is, what can we learn that actually transfers? And I think it's important to break this down into three types of knowledge. First, there's the mechanics of how things work, what a transformer is, how model parallelism works. There's mindset, which is, how do you go about approaching building a language model? We're going to talk about how you want to squeeze the most out of your hardware, taking scaling seriously. And then finally, intuitions. Which data modeling decisions are going to yield good performance?

好，这听起来可能有点令人沮丧，但别担心，我们在这门课中会学到东西。问题在于，什么知识是真正可以迁移（transfer）的？我认为重要的是将知识分为三类。第一类是**机制（mechanics）**——事物是如何工作的：什么是 Transformer，模型并行（model parallelism）如何运作。第二类是**思维模式（mindset）**——你如何着手构建一个语言模型？我们会讨论如何从硬件中榨取最大性能，以及如何认真对待缩放问题。第三类是**直觉（intuitions）**——哪些数据建模决策会带来好的性能？

---

So now, in this class, I think we can do a pretty good job of teaching the mechanics, which is how things work and the mindset. And we're going to really emphasize that you profile and benchmark everything and try to optimize for efficiency. These things do transfer to a larger scale. Now, the intuitions about what modeling decisions and what data decisions do work might not necessarily transfer across scales. For that, you actually have to go somewhere where you can do things at scale.

在这门课中，我认为我们可以很好地教授机制和思维模式。我们会特别强调你要对所有东西进行性能分析（profile）和基准测试（benchmark），并尽量为效率进行优化。这些东西是能够迁移到更大规模的。至于哪些建模决策和数据决策确实有效——这类直觉不一定能在不同规模之间迁移。要获得这种直觉，你真的需要去一个能做大规模实验的地方。

---

So on the note of intuitions, it is worth remarking that some design decisions are just not justifiable, and just purely come from experimentation. Whereas mechanics, you can, by construction, see how the parallelism and how kernels are going to speed things up and so on. But for intuitions about what modeling changes work, I think you just have to run experiments. There's this famous Noam Shazeer paper that introduces the SwiGLU activation, which we're going to look about. And in the conclusion section, he very honestly has this final sentence which says, we offer no explanation. We attribute their success, of these architectures, all else, to divine benevolence. So that, in some sense, is something that you just have to gain from experience.

关于直觉，值得一提的是，有些设计决策就是无法被证明合理的，纯粹来自实验。而机制——通过构造你就能看到并行化和核函数（kernels）如何加速等等。但对于哪些模型改动有效这类直觉，我认为你只能去做实验。有一篇著名的 Noam Shazeer 论文引入了 SwiGLU 激活函数（我们后面会讲到），在结论部分，他非常诚实地说了一句："我们不提供任何解释。我们将这些架构的成功，归因于——除此之外别无他物——神圣的仁慈（divine benevolence）。"在某种意义上，这就是你只能从经验中去获取的东西。

---

### The Bitter Lesson

Final note about the bitter lesson, which I think has been circulating and people talk about it. I think there's a common misconception here, what it means. I think the wrong interpretation is that scale is all that matters. Algorithms don't matter. But that's not correct. The right interpretation is that algorithms that scale are what that-- or what matters. And you can think about very simply that the accuracy of your model is basically your efficiency times the resources. So efficiency is output over input, and resources is the input. And efficiency is actually, in some sense, way more important at larger scale, right? If you're doing a small scale experiment, if your run takes twice as long, maybe you just wait twice as long and then you come back later. But if you're doing things at scale, that could be hundreds of millions of dollars. And you definitely don't want to do that. Even like a 5% improvement might be a big deal. So in fact, efficiency is actually really, really critical. And I hope to bake that into your mindset as one of the consequences of this class.

最后说一下"苦涩的教训"（The Bitter Lesson），这个话题一直在流传，人们也经常谈论它。我以为这里存在一个常见的误解。错误的理解是"规模就是一切，算法不重要"。这不是正确的解读。正确的理解是：**能够随规模扩展的算法**才是重要的。你可以简单地想：模型的准确率本质上是你的效率乘以资源。效率是产出除以投入，资源则是投入。而在更大规模下，效率在某种意义上其实更加重要，对吧？如果你做小规模实验，运行时间加倍了，你可能就多等一会儿，然后再回来。但如果你在大规模下做，那可能就是数亿美元的代价了——你肯定不想那样。哪怕是 5% 的改进都可能是天大的事。所以事实上，效率真的非常非常关键。我希望这能作为本课程的一个重要收获，融入你们的思维模式。

---

And empirically, if you look at-- there's this paper from OpenAI in 2020 that showed there's a 44x algorithmic efficiency on ImageNet between 2012 and 2019. And it's surely the case that hardware did get a lot better, but that also comes with algorithmic improvements. And of course, when you multiply them together, that's when you see a huge bump in efficiency and accuracy.

从实证角度看，OpenAI 在 2020 年有一篇论文显示，在 2012 年到 2019 年间，ImageNet 上的算法效率（algorithmic efficiency）提升了 44 倍。毫无疑问，硬件确实变得更好了，但那也伴随着算法上的改进。当然，当二者相乘时，你才会看到效率和准确率的巨大跃升。

---

So the framing with all that said is, what is the best model one can build with a certain data and compute budget? For pre-training, it's mostly, we're going to talk about compute budget, because we're going to assume that we have a lot more data than we have compute. But if you're in a setting where you're data limited or you have stashed away, actually, tons of B200s, then you might be data bound. So in other words, maximize efficiency. And we're going to see this theme come up throughout the class.

综上，核心问题可以这样表述：**在给定的数据和计算预算（compute budget）下，我们能构建的最好的模型是什么？** 对于预训练（pre-training），我们主要讨论计算预算，因为我们假设数据远多于计算资源。但如果你处于数据受限（data limited）的场景下，或者你囤积了大量 B200 GPU，那你可能是数据受限的。换句话说：**最大化效率**。我们将在整门课中反复看到这一主题。

---

## A Brief History of Language Models

OK. So next, I want to spend a bit of time talking about language models and a bit of a history and just contextualization before we jump into the more technical details. So language models have been around for a while. Shannon, back in the '50s was using language models to measure the entropy of English. And for a long time, N-gram models were used, actually, in machine translation and speech recognition systems. And they weren't the whole system, but they were an important part of making sure that you generated fluent text.

接下来，在进入技术细节之前，我想花点时间谈谈语言模型的历史和背景。语言模型已经存在了相当长的时间。上世纪 50 年代，香农（Shannon）就在使用语言模型测量英语的熵（entropy）。在很长一段时间里，N-gram 模型被用于机器翻译和语音识别系统中——它们不是整个系统的全部，但在确保生成流畅文本方面是重要的一部分。

---

I would say that the lineage of the Modern Language models comes from neural architectures. And so there is a bunch of ideas, I think, which are important to this development. So in the '90s, there was LSTMs. Yoshua Bengio, actually, wrote the first neural language model in paperback in 2003. This is actually not an LSTM. This was just a feedforward network that looked at the small context. And then there was a Seq2Seq modeling, which boldly said, we can actually compress a whole sentence into a vector. The atom optimizer attention mechanism, which was developed for machine translation. The transformer architecture, which built on top of that, which was also developed for machine translation. And then scaling up to a mixture of experts model parallelism. You see a lot of different architecture and also systems and optimizer ideas developed in the 2010s.

我认为现代语言模型的谱系来自神经架构。这其中有一系列重要的思想推动了发展。90 年代有了 LSTM。Yoshua Bengio 在 2003 年出版了第一本关于神经语言模型的著作——那其实不是 LSTM，而只是一个看小上下文的前馈网络（feedforward network）。然后是 Seq2Seq 建模，它大胆地提出：我们真的可以把整个句子压缩成一个向量。注意力机制（attention mechanism）被开发出来用于机器翻译。Transformer 架构在此基础上构建起来，也是为机器翻译开发的。然后是向混合专家（MoE）和模型并行的规模扩展。在 2010 年代，我们看到了大量不同的架构、系统和优化器思想的涌现。

---

And then by the late 2010s, I think, things were starting to get really interesting. So there was the ELMo and BERT. These are language models that were trained on lots of text, and then you could fine tune them on some downstream tasks like question answering, and it would show a huge improvement on that. So the model there was, take one of these models and then fine tune. And then Google had a paper that was really, I think, foreshadowing this view of prompt in, response out. So it was really, I think, OpenAI that really opened up the floodgates here by embracing scaling.

到了 2010 年代末，事情开始变得真正有趣起来。ELMo 和 BERT 出现了——这些语言模型在海量文本上训练，然后你可以在一些下游任务（downstream tasks）如问答上对它们进行微调，这会带来巨大的性能提升。所以当时的范式是：拿一个这样的模型，然后微调。然后 Google 有一篇论文，我认为真正预示了"提示输入、响应输出"（prompt in, response out）的视角。但我认为是 OpenAI 通过拥抱缩放（scaling）真正打开了闸门。

---

So they had GPT paper back in, I think, 2018 or so. They scaled it up to GPT-2, and then they really figured out or embrace the idea of scaling laws, which we're going to talk about in a second, which enable them to train GPT-3, which was a much more massive, almost more than 10x, the largest model at the time. And it could show emergent behavior like in-context learning. At that point, Google was saying, OK, we need to do something too. So they trained a massive model. It turned out to be undertrained. And it turned out that their DeepMind, which was not integrated with Google at the time, had figured out optimal-compute, optimal scaling laws. So all of this was happening.

他们有 GPT 论文，我记得大概是 2018 年左右。他们将其扩展到 GPT-2，然后真正发现或拥抱了缩放定律（scaling laws）——我们稍后会讨论——这使他们能够训练出 GPT-3，比当时最大的模型还大了 10 倍以上，并展现出**上下文学习（in-context learning）**等涌现行为。那时 Google 说，好吧，我们也得做点什么。于是他们训练了一个巨大的模型，结果证明训练不足（undertrained）。而当时尚未与 Google 整合的 DeepMind，已经搞清楚了计算最优（optimal-compute）的缩放定律。所有这些都在同时发生。

---

### The Open Model Ecosystem

And after GPT-3 came out, I think for many folks, this was kind of a wake up call. And at that time, there were a lot of early attempts to, let's try to replicate this. So there was a grassroots organization called Eleuther that created some open data sets and models. They weren't very large because they didn't have much compute. Meta first LLM, you could tell that it's a replication because it was like 175 billion parameters, but it was not a very good model. They ran into a lot of hardware issues. And then there was another, Hugging Face BigScience project. So these models were, I would say, not very strong.

GPT-3 发布后，对许多人来说这是一记警钟。那时有很多早期尝试试图复现它。有一个草根组织叫 Eleuther，创建了一些开放数据集和模型——但它们不太大，因为计算资源不够。Meta 的第一个 LLM，你可以看出它是复现之作，因为参数规模也是 1750 亿，但模型质量不怎么样，他们遇到了很多硬件问题。还有 Hugging Face 的 BigScience 项目。这些模型——我想说——都不太强。

---

Then in the last three years, I think, the open model ecosystem has changed quite a bit, with Meta kind of leading the way with the Llama series of models. Llama, Llama 2, Llama 3. Mistral got in the game. And then a whole set of Chinese models. I think I'm missing some. Like, ByteDance has something, and I think Tencent probably has some other stuff. So it's hard to keep track of everything, but everyone's heard of DeepSeek and Qwen. So I think I got the main ones. But I think what's interesting and exciting about these is now we have open weight models that are approaching closed models. So depending on who you ask and how you benchmark, they might be a little bit behind or comparable. But they are definitely very, very credible models that are being widely used in industry.

而在最近三年，开放模型生态发生了很大变化。Meta 以 Llama 系列引领潮流——Llama、Llama 2、Llama 3。Mistral 也加入了。然后是一大批中国模型。我可能漏掉了一些，比如字节跳动有一些，腾讯大概也有。很难追踪所有的，但大家都听说过 DeepSeek 和 Qwen。我想我把主要的都覆盖到了。但有趣且令人兴奋的是，如今我们拥有了接近闭源模型的开放权重模型（open weight models）。取决于你问谁以及你怎么做基准测试，它们可能稍落后一些，也可能旗鼓相当。但它们绝对是极其可信且被业界广泛使用的模型。

---

Now there's another line of work, which is going beyond just releasing open weight models. AI2, NVIDIA and the Marin project, which I work on, we try to provide not just the weights, but the paper and the code and the data so that we can understand how these models are built in a more thorough way. Why do I emphasize this open ecosystem so much? Mostly because this course would not be possible, I think, without these models by the fact that there are still many papers that are being published about how these big MOEs and RL systems are working enables us to at least glimpse into how these frontier models are being built, and trying to triangulate the pieces.

还有另一条工作线，就是超越仅仅发布开放权重模型。AI2、NVIDIA 以及我参与的 Marin 项目，我们试图提供的不仅是权重，还有论文、代码和数据，以便我们能更透彻地理解这些模型是如何构建的。我为什么如此强调这个开放生态？主要是因为，我认为没有这些模型，这门课就不可能开设。事实上，仍然有许多论文在发表，讨论这些大型 MoE 和 RL 系统是如何工作的，这使我们至少能够一窥前沿模型是如何构建的，并试图拼凑出全貌。

---

### The Changing Definition of Language Models

OK. So in the last decade, I think, the idea of what a language model has changed, right? It used to be something that you fine-tuned, and then it was something you prompt. And now in the ChatGPT era, it was something you talked to and that you can have a conversation with. And now-- OK, I guess I don't have internet. That's fine. And now, we're in the era of agents. If you click on this link, it basically shows you a giant agent trace. And I'm still-- it's mind boggling how strong some of these models are. You give it like a page of text and it does some really complicated agentic coding task. So what we demand of our language models today is probably beyond the imagination of any one back 10 years ago.

在过去的十年中，语言模型这个概念已经改变了，对吧？它曾经是你需要微调的东西，后来变成了你需要提示（prompt）的东西。现在在 ChatGPT 时代，它变成了你可以对话交流的对象。而现在——好吧，我好像没联网。没关系。现在我们进入了智能体（agents）的时代。如果你点击这个链接，它基本上会展示一个巨大的智能体轨迹。我至今仍觉得这些模型的强大程度令人难以置信——你给它一页文本，它就能完成一些非常复杂的编程智能体任务。所以今天我们对于语言模型的要求，可能远超 10 年前任何人的想象。

---

That said, I think the fundamentals, I think, haven't changed that much. Largely, we still built on GPUs and kernels. We still optimize using gradient or stochastic gradient-like approaches. We still have the transformer in attention. And we'll talk a little bit more about architectures, but it hasn't changed that much. I think the specs are different. Now we demand greater context lengths, which means that inference efficiency matters even more. So the good news for us is that we didn't have to completely change this class. Only Tatsu's section on the latest Chinese architectures. But the fundamentals, I think, are here to stay, at least for now.

即便如此，我认为基础并没有改变太多。大体上，我们仍然基于 GPU 和核函数（kernels）构建。我们仍然使用梯度或类随机梯度方法进行优化。我们仍然有 Transformer 和 Attention。我们稍后会多讨论架构，但它确实没有变化太多。我认为规格不同了——现在我们需要更大的上下文长度，这意味着推理效率（inference efficiency）变得更加重要。所以对我们来说好消息是，我们不需要完全改变这门课——只有 Tatsu 负责的最新中式架构部分需要更新。但基础框架，我认为至少现在是会持续下去的。

---

## Course Logistics

OK. So let's talk about the course logistics, and the syllabus, which I think is going to take a good chunk of time. So all the information is online at this website or cs336.stanford.edu. This is a 5-unit class. I think this, probably, class has a certain reputation, so I don't need to belabor the point too much, but this is-- we have five assignments. They are pretty intense. Even the first assignment according to this one. Review was actually equivalent to the 5 assignments. First, CS 224n. I've been told, also, this is exaggerated, but better to, I guess, be conservative in your estimates.

好，让我们来谈谈课程后勤和教学大纲。所有信息都在网上，网址是 cs336.stanford.edu。这是一门 5 学分的课。我想这门课可能有一定的"名声"，所以我不需要太啰嗦——但事实是，我们有五次作业，强度非常大。据某些评论说，第一次作业的强度就相当于 CS 224n 的全部五次作业。我也听说这有点夸大，但保持保守估计总是好的。

---

### Why You Should (and Shouldn't) Take This Course

So why should you take this course? OK, so first you have an obsessive need to understand how things work. That should be your primary objective. I think just pure curiosity on how language models work. And then in doing the class, you'll develop a much stronger research, engineering muscles and have the confidence to go into a new setting and be equipped to deal with whatever situation comes up. So I think when I started at Stanford, I created this class called Statistical Learning Theory, which was, basically, teaching the theoretical side of machine learning. And that was nice because it equipped people. So when you read a paper, you can understand all the math. And now, since the field has shifted a lot more towards this more systems and empirical side of things, this is the kind of analogous class, which gives people enough depth that they feel that everything else seems kind of easy.

为什么你应该选这门课？首先，你有一种强烈的需求去理解事物是如何工作的——这应该是你的首要目标。我认为就是纯粹对语言模型如何运作的好奇心。其次，通过上这门课，你将培养出更强的研究和工程"肌肉"，并有信心进入新环境、应对任何可能出现的情况。我记得刚来斯坦福时，我创建了一门叫"统计学习理论"（Statistical Learning Theory）的课，教授机器学习的理论方面。那门课好就好在它武装了学生——当你读一篇论文时，你能理解所有数学。而如今，这个领域已经大幅转向系统和经验方面，这门课就是类似的对应课程，它给学生足够的深度，让他们觉得其他一切似乎都变得简单了。

---

So why should you not take this course? This is important because there's reasons you shouldn't take this course. First, you actually want to get some research done this quarter. You should probably talk to your advisor. They should know you're taking this course. Otherwise, there'll be-- probably, there might be some surprises. You're interested in learning the hottest new techniques in AI. I think there are many other great courses, seminar courses, topics courses that are good for that. We don't do many of the things. We don't do multimodality. We don't talk about agents in any depth. So if you want to learn about that stuff, this is not the right course for that. If you come in and say, I have an application domain, I want to get good results on it, probably this is not the right course, at least to start. I always recommend just prompt a model, fine tune a model. And then as a last resort, you pre-train your own model. Because it is a pain and it's also expensive, but it's a lot of fun.

为什么你**不应该**选这门课？这很重要，因为确实有不选的理由。第一，你本学季真的想完成一些研究工作——那你大概应该和你的导师谈谈，让他们知道你在选这门课，否则可能会有"惊喜"。第二，你对学习 AI 中最热门的、最新的技术感兴趣——有很多其他很棒的课程、研讨课和专题课更适合这个目的。我们不做很多东西：我们不讲多模态（multimodality），不会深入讨论智能体（agents）。所以如果你想学这些，这不是合适的课程。如果你说"我有一个应用领域，我想在上面取得好结果"——这门课可能也不太合适，至少开始阶段不合适。我总是建议：先用提示（prompt）模型，再微调（fine-tune）模型。万不得已才预训练（pre-train）你自己的模型——因为这又痛苦又昂贵，但确实很好玩。

---

### Following Along at Home

OK. So if you are not taking the class, you can self-follow along at home. So all the lecture materials will be posted on the website. And they are also recorded through CGOE. So thank you, CGOE, for doing that. And later, they will be published to YouTube. Now, of course, following at home and watching the lectures is great, but you learn, really, by doing the assignments. So you'll have to figure out how to motivate yourself to do that.

如果你没有选这门课，你也可以在家自学。所有课程材料都会发布在网站上，也会通过 CGOE 录制——感谢 CGOE。之后它们也会发布到 YouTube 上。当然，在家跟着看课程很棒，但真正的学习是通过做作业来完成的。所以你就要想办法激励自己去做了。

---

## Assignments Overview

OK, so speaking of assignments, we have five assignments. The philosophy assignment is, how do we do from scratch, but not just, say, build a language model, and that's the assignment? So we don't provide scaffolding code, but we do provide a bunch of unit tests to make sure that whatever you're building is actually correct, so that you don't get this sparse reward setting where you submit a homework and it's either correct or not. What I recommend is that you can-- the assignments are structured so that much of the assignment can actually be done locally on your laptop. You can implement it and check for correctness. And then we are providing a cluster so that you can do an actual training run to see what the accuracy is, or get a bunch of GPUs to actually benchmark the performance of some kernel. And then for fun, we will have, some leaderboards for most of the assignments, at least. And they will look something like, well, now that you've learned about this topic, I'll try to minimize the perplexities given some of budget.

说到作业，我们有五次作业。作业的理念是：如何从零做起，但不只是"构建一个语言模型"就完事了？我们不提供脚手架代码（scaffolding code），但提供大量的单元测试（unit tests）以确保你构建的东西是正确的——这样你就不会陷入那种"提交作业，要么全对要么全错"的稀疏奖励（sparse reward）情境。我建议的是：作业结构设计得让你大部分内容可以在笔记本电脑上本地完成——你可以实现并检查正确性。然后我们提供一个集群，让你可以做实际的训练运行来查看准确率，或者用一堆 GPU 来实际基准测试某个核函数的性能。此外，大多数作业我们还会有排行榜（leaderboard）供娱乐。排行榜大概会是这样的：既然你已经学会了这个主题，试着在给定预算下最小化困惑度（perplexity）。

---

### AI Usage Policy

So last year, we were thinking about, well, what can AI do? It was like, OK, well, I mean, yes, everyone can use AI, but just try to do your best. I think now, I think, coding agents have gotten so good that they can just all solve all the assignments, right? But to state the obvious, obviously, you're not going to learn anything if you just feed in the PDF Assignment 1 into a Cloud Code. At the same time, AI can be very useful for answering questions and tutoring. So we have to find a way to leverage AI. So what we've decided to do is, we provide you a AGENTS.md file, or equivalently, a prompt which asks the AI to be pedagogically minded. You can read more about it in our AI policy guide. And the requirement is that if you're going to use AI, use it with this prompt. And so it will answer questions about code, it will clarify any understanding, but it won't accidentally generate the transformer for you when the homework is to implement the transformer. And this is the first year we're trying to do this, so please try it out and give us feedback if it's working or not working.

去年我们在想，AI 能做什么？大家的回答大概是"是的，每个人都可以用 AI，但要尽你所能"。而现在，我认为编程智能体已经变得非常好，它们可以直接解决所有作业，对吧？但显而见的是，如果你只是把作业一的 PDF 喂给 Claude Code，你不会学到任何东西。与此同时，AI 在回答问题和提供辅导方面可以非常有用。所以我们必须找到一种方式来利用 AI。我们决定的做法是：提供一份 AGENTS.md 文件，或者说一个提示（prompt），要求 AI 以教学为导向（pedagogically minded）。你可以在我们的 AI 政策指南中了解更多。要求是：如果你要使用 AI，就用这个提示来使用它。这样它会回答代码相关的问题，澄清你的理解，但不会在作业是让你自己实现 Transformer 时，"不小心"帮你生成一个 Transformer。这是第一年尝试这个做法，所以请试试看，并给我们反馈效果如何。

---

### Compute Resources

So compute. So this year we have-- thanks to Modal, they have provided us with compute credits on their platform. It's actually quite nice. You can get a number of-- unlike last year-- well, I guess, you guys didn't take the class last year. Last year, we had a cluster you SSH into. This is using more of an API to-- which I was initially skeptical of, but looking at it, actually, is pretty pleasant to use. So again, try it out and give us feedback on how it is. We've written a guide on how to access and use the compute.

关于计算资源。今年——感谢 Modal——他们在其平台上为我们提供了计算积分（compute credits）。这真的很不错。和去年不同——你们去年应该没上过这课。去年我们有一个需要 SSH 登录的集群。今年更多是用 API 的方式——我最初对此持怀疑态度，但看了之后发现确实挺好用的。所以，还是那句话，试试看并给我们反馈。我们写了一份访问和使用计算资源的指南。

---

## Course Overview: Five Parts

OK. All right, let's talk about what we're going to cover in this class. So there's, basically, five parts mirroring the five assignments that you'll have. Basic system, scaling, laws, data, and alignment. So I'm going to now go through each part and just give you a taste of what you will learn.

好，让我们来谈谈这门课将涵盖什么内容。基本上有五个部分，对应五次作业：基础（Basics）、系统（Systems）、缩放定律（Scaling Laws）、数据（Data）和对齐（Alignment）。我现在就来逐一介绍每个部分，让大家对要学的内容有个初步了解。

---

### Part 1: The Basics — Tokenization

So in the basics, this is basically the first two weeks. The goal is to just be able to train a language model and build it from scratch. So the components here are, we're going to tokenize the data, we're going to define architecture, and then we're going to implement optimizer and train it. So then you wonder, what are the rest of the classes for? Well, we'll get to there.

基础部分基本上就是前两周。目标就是能够训练一个语言模型，并从零开始构建它。这里的组件包括：对数据做分词（tokenize）、定义架构（architecture）、实现优化器（optimizer）并训练它。然后你会想，那剩下的课是干什么的？我们等会儿会讲到。

---

So let's start with tokenization. The tokenization is really about, what are the atoms that the model operates on? And formally, a tokenizer converts between raw inputs, which are just bytes, and a sequence of integers, which represent the tokens. Conceptually, it's a segmentation of the text. We're going to talk about the Byte-Pair Encoding, BPE tokenizer, which intuitively, breaks the input into frequently occurring chunks. And then remember, this class is about maximizing efficiency, so through an efficiency lens, tokenization is good because it takes a long sequence, if you just think about the raw byte stream, and reduces it into a smaller number of tokens. But more subtly, but maybe more importantly, it allows you to do adaptive computation. So maybe some places are actually a lot of bites, but actually, it should be compressed into a one token, whereas some of the more rare or interesting parts of input should be left as multiple tokens.

我们从分词（tokenization）开始。分词的核心问题是：模型操作的"原子"是什么？形式上，分词器（tokenizer）在原始输入（即字节）和代表标记的整数序列之间进行转换。概念上，它是对文本的一种分割。我们将讨论**字节对编码**（Byte-Pair Encoding, BPE）分词器，它的直观想法是将输入分解为频繁出现的块。记住，这门课是关于最大化效率的，所以从效率角度看，分词是好的——它把长序列（如果你只看原始字节流的话）缩减为更少的标记。但更微妙、也可能更重要的一个好处是，它允许你进行**自适应计算（adaptive computation）**：有些地方实际上很多字节，但应该被压缩成一个标记；而输入中更罕见或更有趣的部分则应该保留为多个标记。

---

OK, we'll talk more about this. I just want to mention that every year, I'm hoping that I don't have to teach tokenization, because the dream is to really have an end-to-end way that directly operates on bytes. And there's been a number of work, including recently, there's been these networks that seems promising, but so far, these have not been scaled to the frontier. And since the frontier models are still using tokenizers, we felt like it would be still wise to teach tokenizers.

好，我们后面会详细讨论。我只想提一句：每年我都希望不用再教分词了，因为梦想是真正有一种端到端（end-to-end）的方式直接对字节进行操作。已经有不少工作，包括最近有一些看起来很有前景的网络架构，但到目前为止，它们还没有被扩展到前沿水平。而既然前沿模型仍在使用分词器，我们觉得教授分词器依然是明智的。

---

### Part 1: Architecture

OK, so now after you tokenize your input, you have a bunch of tokens. Now you define a model on top. And everyone, I think, has a familiarity with the transformer. And if you've taken 224n, the MLP class, then you've seen transformers. Since then, I think, there have been a lot of improvements or refinements to transformers, which I think are important. And Tatsu is going to talk more about this in a bit. But just to run through a set of types of things that one might have to think about, so the activation functions have evolved. How do you do positional encodings has evolved. How you normalize has the different layers. Blow up has evolved.

分词之后，你就有了一堆标记。现在你在这之上定义模型。我想大家对 Transformer 都有一定的熟悉度。如果你上过 224n 或 MLP 课程，你就已经见过 Transformer 了。从那以后，Transformer 有了很多改进和精炼，我认为这些都很重要。Tatsu 稍后会详细讨论。但让我快速地过一遍你需要考虑的各类问题：激活函数（activation functions）已经演进了；位置编码（positional encodings）的做法也演进了；如何做归一化（normalization）以及各层之间如何放置也演进了。

---

Instead of doing full attention, there's many ways to basically reduce the attention computation, because attention is n squared and where n is a sequence length, and that gets really expensive. So there's a bunch of ideas around that. If you're more ambitious, you can look at these state-space models or equivalently linear attention like Mamba and Gated DeltaNet. These have become more popular in the last few years. And usually, some hybrid between these models and attention seems to work quite well. So, we'll be exploring some of that.

与其做全注意力（full attention），有很多方法可以基本减少注意力计算量——因为注意力是 n 平方的（n 是序列长度），这会变得非常昂贵。所以围绕这一点有很多想法。如果你更有野心，你可以看看这些**状态空间模型**（state-space models），或者等价的线性注意力（linear attention），比如 Mamba 和 Gated DeltaNet。这些在过去几年中变得越来越流行了。通常，这些模型和注意力机制之间的某种混合（hybrid）似乎效果相当好。我们会探索其中一些。

---

And then within the MLP layers of the transformer, the original transformer was just a dense MLP, and now a mixture of experts has become the dominant paradigm for building compute efficient transformers. So we're going to talk about that. And of course with a mixture of experts, it's not just defining architecture, but we'll see that we'll also need different techniques for training the model. And then finally, perhaps somewhat boringly, but an important question is, what is the shape of your transformer? How many layers? How many heads? What is hidden dimension? Number of experts? This might come in more as we talk about scaling laws, but setting these is actually-- seems kind of almost trivial. It's a hyperparameter, but actually in the context of scaling and language models, it has a huge, huge implication.

在 Transformer 的 MLP 层中，原始的 Transformer 只是一个密集的 MLP，而现在**混合专家**（MoE）已成为构建计算高效 Transformer 的主导范式。我们会讨论这个。当然，混合专家不仅仅是定义架构，我们会看到还需要不同的训练技术。最后，也许有点无聊但很重要的问题是：你的 Transformer 的"形状"是什么？多少层？多少头（heads）？隐藏维度（hidden dimension）多大？多少个专家（experts）？这些在我们讲到缩放定律时会更多涉及，但设置这些参数看似平凡——它只是一个超参数——但在缩放和语言模型的背景下，它有巨大的影响。

---

### Part 1: Training

So once you define your model architecture, how do you train the model? And here there's a bunch of design decisions around the loss function. There's next token prediction, which is the default. But people have found that predicting more than one token seems to be helpful for improving the model. And there's optimizers. People used to use AdamW, but increasingly, Muon has been used, especially with some of the latest open models, such as the Kimi K2 models. Initialization, which, again, sounds kind of boring, but turns out to have a huge impact on how your ability in the training stability of larger models. Learning rate schedule. Regularization. Batch size. And then MoE specific things.

定义了模型架构之后，如何训练模型呢？这里有一堆围绕损失函数（loss function）的设计决策。默认是**下一个标记预测**（next token prediction）。但人们发现预测多个标记似乎有助于改进模型。还有优化器：人们过去用 AdamW，但越来越多地使用 Muon，特别是在一些最新的开放模型中，如 Kimi K2 模型。初始化（initialization）——听起来又很无聊，但事实证明它对更大模型的训练稳定性有巨大影响。学习率调度（learning rate schedule）、正则化（regularization）、批大小（batch size），以及 MoE 特有的东西。

---

So you look at this list and you might think, well, these are just hyperparameters. I'm going to try a bunch of different options out. But it turns out that really being very careful about setting these hyperparameters in a principled way will make the difference between a run that just blows up and is useless between a run that is achieving state of the art.

你看看这个列表，可能会想：这些不过是超参数而已，我试试各种不同的选项就好了。但事实证明，真正以有原则的方式小心设置这些超参数，将决定你的训练运行是直接爆炸、毫无用处，还是达到最先进的（state of the art）水平。

---

### Assignment 1

So then in Assignment 1, what you're going to do is you're going to implement the BPE tokenizer, implement the transformer, the loss function, the optimizer, the whole training step. We're going to make you do a bunch of resource accounting so you understand where your flops are going. You're going to train some models on these data sets like TinyStories and OpenWebText. And then there's going to be a leaderboard where you're going to try to drive down perplexity as fast as you can. So for those of you familiar with NanoGPT, speedruns, it's kind of similar to that. OK, so by the end of Assignment 1, you should be able to walk away and build a language model from scratch. So that's very exciting.

在作业一中，你要做的事情是：实现 BPE 分词器、实现 Transformer、损失函数、优化器、整个训练步骤。我们会让你做大量的资源核算（resource accounting），让你理解 FLOP 都花在了哪里。你将在 TinyStories 和 OpenWebText 等数据集上训练一些模型。然后会有一个排行榜，你要尽可能快地压低困惑度（perplexity）。如果你熟悉 NanoGPT 的速通（speedruns），这和那个有点类似。到作业一结束时，你应该能够独立从零开始构建一个语言模型——这非常令人兴奋。

---

If I have a high level takeaway here, it's that while the tokenizer and modeling and training are presented as distinct pieces, it is actually, everything is about balancing the following. So you want expressive models because you want to represent the complexities of the data, but at the same time, you want your training to be stable. And we're going to talk a lot about how do you keep the parameter and gradient norms in this goldilocks zone so they don't blow up and don't vanish. Turns out, a lot of training language models is about just stability. And then finally, efficiency, which is somewhat more straightforward. You just make it run fast on hardware.

如果让我提炼一个高层次的要点，那就是：虽然分词器、建模和训练被呈现为不同的独立部分，但实际上，一切都围绕着以下三者之间的平衡。你需要**高表达力的模型**来捕捉数据的复杂性，同时又需要**训练稳定**。我们会花大量时间讨论如何将参数和梯度范数（norms）保持在一个"恰好"（Goldilocks）区间内——既不会爆炸（blow up），也不会消失（vanish）。事实证明，语言模型训练的很大一部分就是关于稳定性。最后是**效率**，这相对更直接——你只要让它在硬件上跑得快就行了。

---

But you're going to see interesting things like, if we change the architecture, a lot of the architecture decisions are, well, we can make it faster by, let's say, reducing the projecting of a low dimensional space. But then the question is, does it work as well? And so making those trade offs is something that-- is the name of the game here.

但你会看到一些有趣的事情——比如我们改变架构，很多架构决策是：我们可以通过比如说在低维空间中进行投影来让它更快。但问题就变成了：它的效果一样好吗？做出这些权衡取舍，正是这里的游戏本质。

---

### Part 2: Systems

So in Assignment 2, we're going to dive more deeply into systems. And the goal here is just to get most out of your hardware. So we're going to talk about kernels, how you parallelize across multiple GPUs, and how you do inference. So the basics, which we're actually going to start on next lecture, I mentioned resource accounting, and I think you've all probably built models before. But this is really about keeping track of where all the flops go and where all the memory is being spent. So we're going to spend some time, basically, doing the resource accounting. We're going to see this formula that comes up, how many flops does training SMDB on model on 1 trillion tokens? Well, it's six times n times D roughly. And where does that come from?

在作业二中，我们将更深入地探讨系统（systems）。目标是**从硬件中榨取最大性能**。我们将讨论核函数（kernels）、如何在多个 GPU 上做并行化（parallelize），以及如何进行推理（inference）。基础部分——我们实际上下一讲就开始——我提到了资源核算，我想你们可能以前都搭建过模型。但这真的就是追踪所有 FLOP 花到哪里去了、所有内存在哪里被消耗了。我们将花些时间做资源核算。你会看到这个公式：在 1 万亿个标记上训练一个 SMD 模型需要多少 FLOP？答案大致是 **6 × N × D**。这个公式是怎么来的？

---

And then we're going to look at the hardware. And here's a cartoon I picture of what to remark about hardware, is that, your memory is not where your compute is, and you have to move either your parameters or activations from the memory to compute, do the compute, and move it back. And that often is the bottleneck. So for example, B200, which we'll have the opportunity to play with, it has 2.25 petaFLOPS per second if bf16. And has 8 terabytes second of memory. So what does that mean? I think when we-- I think I'll do this next lecture. We're going to break this down and use this information to do some calculations and see how long different types of algorithms will need to take.

然后我们来看硬件。关于硬件，有一幅简图值得注意：**你的内存在远离计算的地方**，你必须把参数或激活值从内存搬移到计算单元，做完计算，再搬回去——而这往往是瓶颈所在。比如 B200（我们将有机会实操），它在 bf16 下拥有每秒 2.25 petaFLOP 的计算能力，以及每秒 8 TB 的内存带宽。这意味着什么？我们下一讲会展开讲解——我们将分解这些数据，并用这些信息做一些计算，看看不同类型的算法需要多长时间。

---

We're going to talk about roofline analysis, which allows us to understand whether a computation is bottlenecked by either a compute or memory. In general, it is memory. And then talk a little bit about benchmarking and profiling.

我们将讨论**屋顶线分析**（roofline analysis），它让我们能够理解一个计算是被计算能力瓶颈还是被内存带宽瓶颈——一般情况下是内存。然后也会谈一点基准测试（benchmarking）和性能分析（profiling）。

---

### Kernels and Operator Fusion

So here's what a DGX B200 looks like. You have 8 GPUs. They're connected via MV link. And then if you have many-- if you have a thousand GPUs, then you would have multiple of these and they're connected either InfiniBand or ethernet. So the next two parts when we talk about system is kernel. So a kernel is basically a function that runs on the GPU. And when you're just using plain PyTorch, all the PyTorch primitives actually correspond to launching particular kernels, which are built in. So you're already using kernels, whether you it or not. But the point is that, for certain types of computation, if you look at it, you can actually write custom kernels to make the GPUs go faster. And the main principle here is organizing the compute to minimize data movement. So remember, this picture moving data from memory is expensive. So you want to try to minimize that.

DGX B200 的样子是这样的：你有 8 个 GPU，它们通过 NVLink 连接。如果你有一千个 GPU，那就会有多个这样的节点，它们之间通过 InfiniBand 或以太网连接。系统部分的接下来两个主题之一是**核函数（kernel）**。核函数本质上就是运行在 GPU 上的函数。当你只用普通 PyTorch 时，所有 PyTorch 原语（primitives）实际上都对应于启动特定的内置核函数。所以无论你是否意识到，你已经在使用核函数了。但关键是，对于某些类型的计算，你可以编写**自定义核函数**（custom kernels）让 GPU 跑得更快。这里的主要原则是：**组织计算以最小化数据移动**。记住，从内存搬移数据是昂贵的——所以你要尽量减少它。

---

So just as a simple example, suppose you wanted to compute A and B. So often, you would have to read from your high bandwidth memory, HBM, compute it, write it back, and then read again, compute it, write it back. So then, you're basically sending the data back and forth twice. And there's this idea called fusion, where you read it once, do both of the computations, and you write it back. And that will save you a lot of time. So that's operator fusion. Tiling is a more sophisticated variant around the same idea.

举个简单例子，假设你想计算 A 和 B。通常你得从高带宽内存（HBM）读取数据，计算，写回去，然后再读、再算、再写回去——这样你就在来回搬数据两趟。而有一种思想叫**融合**（fusion）：你读取一次，做完两个计算，再写回去——这能节省大量时间。这就是**算子融合**（operator fusion）。**分块**（tiling）是同一思想的更复杂变体。

---

### Distributed Training and Inference

So what happens if you have thousands of GPUs? So the principle of minimized data movement is still the same. The only thing is that moving data between different GPUs is even more expensive. We're going to talk about how these very classic collective operations, gather and reduce and all-reduce are the way to think about, basically, distributed training. The general game is that we have these model parameters, we have activations, gradients and optimizer states, and they need to be sharded or split across multiple GPUs. And of course, you need to bring the right data to the right nodes to make the compute and write it back. So there's a whole kind of orchestration, and how to do that efficiently is going to be the topic of this unit.

如果你有数千个 GPU 呢？最小化数据移动的原则还是一样的，只不过在不同 GPU 之间移动数据更加昂贵。我们将讨论如何利用那些经典**集合操作**（collective operations）——gather、reduce、all-reduce——来思考分布式训练。总体的"游戏"是：我们有模型参数、激活值、梯度和优化器状态（optimizer states），它们需要被分片（sharded）或拆分到多个 GPU 上。当然，你需要把正确的数据送到正确的节点来做计算再写回去。这整个过程的高效编排，就是这个单元的课题。

---

And there's multiple ways to shard. You can shard by splitting up your data, splitting up your model, splitting up different layers in the model, splitting up the sequences, splitting up between experts. And we'll talk about the trade offs that come with each of these.

有多种分片方式：你可以按数据拆分、按模型拆分、按模型中的不同层拆分、按序列拆分、按专家（experts）之间拆分。我们将讨论每种方式带来的权衡。

---

OK. And then finally, we're going to talk about inference. Which, as I mentioned, is growing in importance. So the goal of inference is to actually use the model. So minor detail here. So inference is, of course, you need to use inference when you're chatting with a model, but it also is useful for reinforcement learning. It's useful for doing the rollouts. Test-time compute, generating synthetic data, evaluation. So inference is a very critical part of what it means to do language modeling work.

最后，我们将讨论推理（inference）。如我之前提到的，推理越来越重要。推理的目标是实际使用模型。这里有个小细节：推理当然在你与模型对话时需要用到，但它对强化学习（reinforcement learning）、做 rollout、测试时计算（test-time compute）、生成合成数据（synthetic data）、评估（evaluation）也都有用。所以推理是语言建模工作中非常关键的一部分。

---

So the way to think about inference is that there's two phases, a prefill and a decode. In the prefill, you take the prompt and then you feed all the tokens forward and build key value pairs. This is very much like what happens in training. And then in the decoding part, tokens are generated one at a time. And this is the part that becomes quickly memory bound, and this is why inference is hard. And so there's many things you can do to speed up inference. You can try to use a cheaper model by pruning a larger model or you can quantize, you can distill. You can use this technique called speculative decoding, where you use a cheaper model to run ahead and guess a bunch of tokens. And now, you use the full model, which can operate on those tokens in parallel to see if it's good. And if you got lucky, then you can accept all those tokens and you're much faster than if you're doing one token at a time.

推理的思考方式是两阶段：**预填充**（prefill）和**解码**（decode）。在预填充阶段，你取提示词（prompt），将所有标记前向传播，构建 key-value 对——这很像训练时发生的事。然后在解码阶段，标记是一个一个生成的——这很快就会变得内存受限（memory bound），这也是推理难的原因。所以有很多方法可以加速推理：你可以通过对大模型剪枝（pruning）来使用更便宜的模型，或者量化（quantize）、蒸馏（distill）。你可以使用一种叫**推测解码**（speculative decoding）的技术：用一个更便宜的模型先跑一遍，猜测一堆标记，然后用完整模型并行地对这些标记进行评估。如果你运气好，就可以接受所有这些标记，这比一个一个生成快得多。

---

### Part 3: Scaling Laws

OK. So the third assignment is about scaling laws. So by now, you've trained a language model. You can make it go really fast by optimizing kernels in parallel. Now, you want to scale up. So how do you scale up? So imagine the following setting. If you had 1e25 FLOPs, so this is tens of millions of dollars of compute, what model would you train? So this is, I think, a daunting task because if you mess up, well, that's a lot of money down the drain. And you can't do your, probably, typical hyperparameter tuning at that scale because you only get to train one model. And so this is the key problem that you have to deal with in large language model training that you don't have to really deal with if you're just fine tuning a model or doing small scale stuff.

第三个作业是关于**缩放定律**（scaling laws）的。到这个时候，你已经训练了一个语言模型，你通过优化核函数和并行化让它跑得很快。现在你想放大规模。那怎么放大呢？想象这样一个场景：如果你有 1e25 FLOP 的预算——这相当于数千万美元的计算资源——你会训练什么样的模型？这是一个令人生畏的任务，因为如果你搞砸了，大笔资金就打水漂了。你不能在那种规模下做你习以为常的超参数调优，因为你只能训练一个模型。这就是在大语言模型训练中你必须处理的关键问题，而如果你只是在微调模型或做小规模工作，你根本不需要面对它。

---

And so the key conceptual shift here is that we shouldn't think about a single model that we're training, but really think about a scaling recipe. And a scaling recipe is a mapping from a FLOP budget, let's say 1e25 or 1e24, to a set of hyperparameters. Basically a config file. And for a given scaling recipe, what we will do is run a bunch of experiments to compute the loss that you get at smaller scales, and then you fit a scaling law, and that enables you to predict the loss at a target scale. So maybe you run some small experiments, you fit a scaling law, and then you predict out what you're going to get at a larger scale. So that's the primitive.

这里的关键概念转变是：我们不应该考虑训练单独一个模型，而应该考虑一个**缩放配方**（scaling recipe）。缩放配方是从 FLOP 预算（比如 1e25 或 1e24）到一组超参数的映射——基本上就是一个配置文件。对于给定的缩放配方，我们要做的是：在小规模下跑一系列实验来计算损失，然后拟合一条缩放定律（scaling law），这使你能够预测目标规模下的损失。所以你先跑一些小实验，拟合一条缩放定律，然后预测在大规模下会得到什么——这就是基本原语。

---

Now using this, what you can do is now you can optimize the scaling recipe, targeting a larger scale using smaller scale experiments, which is wonderful. And second of all, you can predict the loss that you're going to, in theory, achieve before actually running the experiment. Which allows you to go raise money. And you say, well, look, I ran the small scale experiments, and I think I can get really-- like, a GPD-5 level model. Please give me a lot of money so I can train that model.

利用这一点，你现在可以通过小规模实验来优化缩放配方，瞄准更大规模——这太棒了。其次，你可以在实际运行实验之前就理论上预测你将达到的损失值，这使你可以去融资。你说："你看，我跑了小规模实验，我认为我可以做出一个 GPT-5 级别的模型。请给我很多钱来训练那个模型。"

---

But one thing I think is maybe another misconception is that scaling laws are not laws of nature. They don't just happen automatically. You have to will them into existence. And this happens by careful construction of a scaling recipe. And the scaling recipe, remember, it has to extrapolate. So what this typically means is that you have a sequence of hyperparameters which, say, as the scale increases, maybe the learning rate is a constant, maybe it drops, maybe the batch size increases by how much. And these are things that a scaling recipe has to figure out.

但我认为还有一个可能的误解：缩放定律不是自然规律——它们不会自动发生。你必须通过精心构造缩放配方来"让它们存在"。而缩放配方——记住——必须能够外推（extrapolate）。这通常意味着你有一系列超参数：随着规模增加，学习率可能是常数，可能下降，批大小可能增加，增加多少——这些都是缩放配方必须搞清楚的。

---

So one shift in thinking is that predictability is actually at least as important as optimality. So you normally think, oh, we're trying to optimize for efficiency here, and we want to hyperparameter tune and make things optimal. And yes, you do want to do that, but you also want this predictability so that you don't get surprised at larger scale.

所以一个思维上的转变是：**可预测性（predictability）至少和最优性（optimality）一样重要**。你通常想的是：我们在优化效率，要做超参数调优，让一切达到最优。是的，你确实需要这样做，但你也需要这种可预测性，这样在大规模下就不会出现"意外"。

---

So the actual scaling laws we're going to look at are fairly classic. So these are-- some of you might have seen this idea of, well, if I give you a FLOPs budget, should you train-- how should you balance training a larger model versus training on more tokens? And this is where the classic compute optimal scaling laws from Kaplan et Al and the so-called Chinchilla scaling laws comes in. The basic idea is that you for each FLOPs budget, so let's say 6e18 all the way to 3e21, you sweep across different model sizes and you choose the best one. So think about minimizing each of these. And then you fit a curve that allows you to, basically, predict the number of parameters given a FLOPs budget.

我们将要看的实际缩放定律是相当经典的。你们有些人可能见过这个思想：如果给你一个 FLOP 预算，你应该如何平衡训练更大的模型 vs. 在更多标记上训练？这就是经典的来自 Kaplan 等人的**计算最优缩放定律**（compute optimal scaling laws）以及所谓的 Chinchilla 缩放定律出场的地方。基本思路是：对于每个 FLOP 预算（比如从 6e18 到 3e21），你对不同模型大小进行扫描，选择最好的那个。然后拟合一条曲线，使你能够根据 FLOP 预算预测参数数量。

---

And so the upshot of this, this is quite crude, but a rule of thumb is, the 20 times the number of parameters is the number of data points you should train on. So a 70B parameter model should be trained on roughly 1.4 trillion tokens. Of course, depending on the data set and architecture, this number will actually vary. Also, this doesn't take you into account the inference cost. A lot of models these days are small, but they're trained on way more tokens than is compute optimal because you want a smaller model for inference reasons.

这带来的结论是——虽然很粗略——一个经验法则是：**参数数量的 20 倍，就是你应该用来训练的标记数量**。所以一个 70B 参数的模型应该在大约 1.4 万亿个标记上训练。当然，取决于数据集和架构，这个数字会有变化。此外，这还没有考虑推理成本。如今很多模型虽然小，但训练的标记量远超"计算最优"的建议，因为出于推理的考虑你想要更小的模型。

---

So one fun thing that we've been doing in the Marin project is pre-registering our results. So we fit a bunch of scaling plots at different compute budgets. We fit a scaling law, and we basically made these predictions out to 1E22 FLOPs. This one is actually training. If you go to the Marin website, you can follow along. It should actually be done maybe as early as tonight. So maybe on Wednesday I'll report back on how we did and see how we measure-- how we match the pre-registered loss. So the idea here is that we made a prediction on if we were to train this large model, which we've never trained before. If we can predict how well it's going to do, then that's really nice.

我们在 Marin 项目中做的一件有趣的事是**预注册结果**（pre-registering results）。我们在不同计算预算下拟合了一系列缩放曲线，拟合出一条缩放定律，并一直外推到 1e22 FLOP。这个训练实际上正在进行中。如果你去 Marin 网站，可以跟踪进展——可能最早今晚就能完成了。所以也许周三我会汇报结果，看看实际损失与我们预注册的损失匹配得如何。这里的思路是：我们对于一个从未训练过的大模型做了预测，如果我们可以预测它的表现，那就太棒了。

---

### Part 4: Data

So at this point, you will have, you train a model, how to make it fast, you know to scale up. Now, what's missing? What do you train the model on? And that's going to be the subject of the data section, which is arguably one of the most important things because data quality basically specifies how good your model is going to be. One way to also frame it is, what do you want your model to do? Data, basically, reflects what your model wants. So do you want to speak multiple languages? Be good at having a conversation? Do you want to run long agentic coding tasks? And so part of that is also going to-- so we're going to start by talking about evaluation, which, basically, defines the capabilities that you'd like your model to have.

到这个时候，你已经会训练模型了，知道如何让它跑得快，也知道如何放大规模。那还缺什么？你用什么数据来训练模型？这就是数据部分的主题——这可以说**是最重要的事情之一**，因为数据质量基本上决定了你的模型有多好。换一个框架来理解：你希望你的模型做什么？数据基本上反映了你对模型的期望。你想要它讲多种语言吗？善于对话？你想要它运行长时间的编程智能体任务吗？因此，我们将从**评估**（evaluation）开始，它基本上定义了你希望模型具备的能力。

---

One thing we'll talk about is, evaluation is a fairly deep topic. It's not just about running on some benchmarks. There are internal evaluation metrics for model development. And what matters here is that smoothness across scales so that there-- remember, we want things to be predictable. Relative performance matters. You don't care, necessarily, how well this does in absolute terms, because, let's say, a perplexity number is just like, what is a perplexity of 1.2 on some held out data really mean? And then there's external metrics. These are things that you report to your customers or your reviewers or whoever you're presenting your thing to. And here, ecological validity really matters.

我们会讨论的是，评估是一个相当深的话题。它不仅仅是在一些基准上跑一跑。有**内部评估指标**（internal evaluation metrics）用于模型开发——这里重要的是跨规模的平滑性，因为我们希望结果可预测。相对性能很重要——你不一定关心绝对意义上的表现如何，因为比如说，在某一测试集上困惑度 1.2 到底意味着什么？然后还有**外部指标**（external metrics）——这些东西是你向客户、审稿人或任何你要展示成果的人报告的。在这里，**生态效度**（ecological validity）至关重要。

---

So now after we set up the evals, we know what we're building. How do you get the data? Well, first thing is that data does not just fall from the sky. It has to be actively curated. Often, I think, especially in classes and also in research, sometimes you're just given a data set, and then it's like, OK, well, now, I do stuff on the data set. But a lot of language models, especially if you want to collect these large data sets, you have to go and actively look at it. So web pages are crawled from the internet. There's books, I guess, which is controversial at this point, but arXiv papers, GitHub code, and so on. This is an old figure from the pile from 2021. And you can see, language modeling data sets are fairly diverse.

设定好评估标准后，我们知道了要构建什么。那数据怎么来？首先要明白，数据不是从天上掉下来的——它必须被主动策划（curated）。我常常觉得，尤其在课堂上和研究中，有时候你只是被给了一个数据集，然后你就说"好，我就在这个数据集上做事情"。但对于很多语言模型，特别是如果你要收集这么大规模的数据集，你必须主动去寻找。网页是从互联网上抓取（crawl）的；还有书籍——这在当下是有争议的——arXiv 论文、GitHub 代码等等。这是 2021 年 The Pile 数据集的旧图。你可以看到，语言建模数据集是相当多样化的。

---

There's, especially these days, I think, a lot of contention around, is it fair use to train on copyrighted data? Maybe sometimes you have to license data and so on. So there's legal issues around data which, I think, are quite important. For example, a lot of GitHub code doesn't have a license. So how do you interpret that? Do you assume it's permissive, or do you be conservative and assume it's not permissive?

尤其是当下，关于在受版权保护的数据上训练是否属于合理使用（fair use），存在很多争议。有时你可能必须获得数据许可等等。所以数据周围的法律问题我认为相当重要。例如，大量 GitHub 代码没有许可证——你怎么解读？你是假定它是许可使用的，还是保守地假定它不许可？

---

So there's also-- the fact is that data is not even text. It's either HTML or PDFs, or a code is directories. And this requires processing to turn it into actual text to be usable for training. So that's the topic of data processing. There's a few steps that has to happen here. Transformation, converting some nontexting in a text. Filtering, keeping only the good stuff. If the random internet document in Common Crawl is extremely bad and you don't want to train on it, most likely. You want to deduplicate. There's multiple sources, or how do you combine the different sources? And then finally, more recently, there's been a lot of work on generating synthetic data, which could mean taking the real data and just rewriting it into things that are more the downstream task or just more Wikipedia like, or whatever you want. So this is an active area of research.

此外，事实是数据甚至不是文本——它要么是 HTML，要么是 PDF，或者代码是目录结构。这需要做处理才能将其转化为可用于训练的实际文本。这就是**数据处理**（data processing）的主题。这里需要做几步：**转换**（transformation），将非文本格式转换为文本；**过滤**（filtering），只保留好的内容——Common Crawl 中的随机互联网文档如果质量极差，你大概率不想用它训练；**去重**（deduplication）；多个数据源，如何将它们**混合**（mix）在一起？最后，最近有大量关于生成**合成数据**（synthetic data）的工作——这可能是把真实数据改写为更适用于下游任务的形式，或者更接近维基百科风格，或者随便你想要的什么。这是一个活跃的研究领域。

---

### Part 5: Alignment

So finally, alignment. So far we've, basically, trained a model using full supervision. Predict the next token or the next few tokens. Now at this point, the model should already be reasonable, but we can improve it further by using weak supervision. And why weak supervision? It's because sometimes it's easier to critique than it is to generate. So you can't always have data that says, this is the right response to this prompt, but maybe you can have a way of specifying what good looks like. So then, the basic template is that you generate responses from the model. You score them either with a human or verify or a LM judge, and then you update the model to prefer better responses. This can be instantiated either through various RL algorithms such as PPO or GRPO, or in a simpler, for preference data, DPO.

最后是对齐（alignment）。到目前为止，我们基本上是用完全监督（full supervision）训练模型——预测下一个标记或下几个标记。到这个阶段，模型应该已经相当不错了，但我们可以通过**弱监督**（weak supervision）进一步改进它。为什么用弱监督？因为有时候**批评比生成更容易**。你不可能总有数据说"这是对这个提示的正确响应"，但也许你可以有一种方式来指定"好"是什么样子。基本模板是：从模型生成响应，用人类、验证器或 LLM 评判员（LM judge）来打分，然后更新模型以偏好更好的响应。这可以通过各种 RL 算法如 PPO 或 GRPO，或者更简单地，对于偏好数据用 DPO 来实例化。

---

So the challenges around RL are that RL algorithms are unstable and hard to tune. Some of you probably know this from firsthand experience. Personally, I prefer to keep things as much in the fold so we supervise the case as long as possible. And then finally, OK, fine, I have to do RL. But some people, for whatever reason, like doing RL. Also, what we'll, hopefully, talk about this year is that if you do RL at scale and try to maximize your throughput, there's actually a lot of systems challenges. You have to have an inference server and a training server. And then the inference server has to generate these rollouts. Especially if you do RL against environments that involve code execution. It's a whole kind of orchestration game.

围绕 RL 的挑战在于 RL 算法不稳定且难以调试。你们有些人可能有亲身体会。就我个人而言，我倾向于尽可能把事情保持在监督学习的框架内。然后最终，好吧，我必须做 RL。但有些人，不知道什么原因，就是喜欢做 RL。另外，我们今年也希望能讨论的是：如果你在大规模下做 RL 并试图最大化吞吐量，实际上有大量的系统挑战。你需要一个推理服务器和一个训练服务器，推理服务器要生成这些 rollout。特别是如果你在涉及代码执行的环境中做 RL——那简直是一场编排（orchestration）"游戏"。

---

## Tokenization — The First Unit

OK. So now let's do tokenization. So this is-- we're jumping into our first unit here. So Andrej Karpathy has this really good video on tokenization. You should check it out. So starting point is raw text is what is text? It's Unicode strings. And on the other hand, the language model places a distribution over sequences of tokens usually represented as indices. So we need a procedure that encodes these strings into tokens, and also a procedure that decodes tokens back into strings. So a tokenizer is basically something that can do this round trip.

好，现在让我们进入分词（tokenization）——这就是我们要讲的第一单元。Andrej Karpathy 有一个关于分词的非常好的视频，你们值得去看看。出发点是："原始文本"是什么？它是 Unicode 字符串。另一方面，语言模型在标记序列上放置一个分布，这些标记通常表示为索引（indices）。所以我们需要一个程序将字符串**编码**（encode）为标记，还需要一个程序将标记**解码**（decode）回字符串。所以分词器基本上就是一个能完成这种往返转换（round trip）的东西。

---

So here are some examples to give you a flavor for how tokenizers work. Actually, I should have tried to get in there earlier. So this is not going to work. If you go to the site you can play around with different tokenizers. So some observations here. And you'll appreciate why tokenizers are kind of annoying and why people want to get rid of them. So a word and its-- a word conglomerate with its preceding space are different tokens. So many tokens you'll actually see are space a word, which is fine, but kind of strange. So this hello and this hello is actually two completely different indices that have nothing to do with each other. And sometimes, depending on the tokenizer you use, numbers are represented with-- every few digits is a token. Sometimes, it's predictable, and sometimes, it's not. Some tokenizers try to make every digit a token, but then you're blowing up the number of tokens you have.

这里有一些例子来让你感受分词器是如何工作的。如果你去那个网站可以玩一玩不同的分词器。一些观察发现——你会理解为什么分词器有点烦人以及为什么人们想摆脱它们。一个单词与其前导空格连在一起的组合，和它本身是不同的标记。你会看到很多标记实际上是"空格+单词"的形式——这还行，但有点奇怪。所以这个"hello"和这个"hello"（带前导空格）实际上是两个完全不同的索引，彼此毫无关系。有时候，取决于你用的分词器，数字的表示方式也不同——每几位数字是一个标记。有时这是可预测的，有时不是。有些分词器尝试让每个数字都是一个标记，但这样你的标记数量就会爆炸。

---

So here's the GPT-5 tokenizer. So you can take this string and convert it into these indices. And then you can decode it back into the string. And so tokenizers should round trip. If you implement tokenizer, it doesn't round trip, you have a problem. So the compression ratio here is the number of bytes per token. So in this case, we have, the number of bytes of this string is 20. The number of tokens is 8. And you do 20 divided by 8. So the compression ratio is 2.5. OK, so 2.5 bytes per token. The larger the compression ratio, that means the shorter the sentence, which is good because attention is quadratic, and you want to make sure the sent sequence is shorter.

这是 GPT-5 的分词器。你可以取这个字符串，将其转换为这些索引，然后再解码回原字符串。分词器必须支持往返转换——如果你实现的分词器不能往返转换，那你就有问题了。这里的**压缩比**（compression ratio）是每个标记的字节数。在这个例子中，字符串的字节数是 20，标记数是 8，20 除以 8，压缩比是 2.5——每标记 2.5 字节。压缩比越大，序列越短，这是好的——因为 Attention 是二次的（quadratic），你希望序列越短越好。

---

### Different Tokenization Approaches

Now, you could obviously increase the compression ratio by increasing the vocab size, but then, you get into sparsity where more and more-- because every element of vocab is treated like a distinct element. So these days, tokenizers, especially multilingual tokenizers, have 100k or 200k tokens, distinct tokens. So how do you build a tokenizer? So I'm going to go through this fast. So the first thing you might do is like, well, Unicode string, that's a sequence of Unicode characters. And each character is an integer, which you can call ord in Python, and you get some number out. And this can be converted into characters. So let's just build a character level tokenizer which basically breaks up each character and encodes it in a token. And then this can decode back. Life is good.

显然你可以通过增大词表（vocab size）来提高压缩比，但那样你就会遇到稀疏性（sparsity）问题——因为词表中的每个元素都被当作不同的元素处理。如今的分词器——特别是多语言分词器——有 10 万到 20 万个不同的标记。那怎么构建一个分词器？我快速过一遍。你可能会首先想到：Unicode 字符串是 Unicode 字符序列，每个字符都是一个整数（在 Python 中调用 ord 就能拿到一个数），可以转换回字符。那我们构建一个**字符级分词器**（character-level tokenizer）——把每个字符拆开并编码为一个标记，然后还能解码回去。生活很美好。

---

So now, there are 150k Unicode characters. So your vocab size could be 150k, which is a lot. I mean, it's not crazy, but I think the bigger problem is that many characters are actually rare, which means that it's really an inefficient use of a vocabulary. And also, the compression ratio, which reflects this is not that great. So most of the time, you're actually using a lot of tokens to represent your sequence. And many of the indices are actually not being very used. So this is not a very good tokenizer.

但 Unicode 有 15 万个字符，所以你的词表大小可能是 15 万——这很多，但还不算疯狂。更大的问题是：很多字符实际上很少出现，这意味着对词表的利用非常低效。而且反映这一点的压缩比也不太好——大多数时候你用了很多标记来表示序列。很多索引实际上不怎么被用到。所以这不是一个好的分词器。

---

So here's another attempt. So you can turn strings into bytes. So Unicode has a UTF-8 encoding, which means that you can-- sometimes a string like "a" is just 1 byte, and sometimes, a string is multiple bytes. So let's build a tokenizer around that. So we can take this string and convert it into a sequence of bytes. And notice that this is a longer sequence now, but all the numbers are between 0 and 255, because that's what a byte means. And the compression ratio is 1, which is not great. So byte sequences can be very long, but the vocab size is small. OK. So both of these are really bad. So let's try to make some progress.

另一种尝试：你可以将字符串转换为字节。Unicode 有 UTF-8 编码——有时像"a"这样的字符串只是 1 个字节，有时则是多个字节。我们围绕这个来构建分词器：把这个字符串转换为一序列字节。注意，现在序列更长了，但所有数字都在 0 到 255 之间——因为这就是字节的含义。压缩比是 1，这不好。字节序列可能非常长，但词表大小很小。好，这两种都很糟糕。让我们努力往前走。

---

So this is what actually people used to do in NLP, if people remember. So if you take a string, I can just chunk it up into-- break it up by spaces or some regular expression. And let's just call each of these chunks a token. So what is good about this one is that each token is meaningful because humans invented words, and words tend to have a stable semantic meaning. But your vocab size is the number of distinct chunks in the training data, which could be a lot. And also, your compression ratio, I mean, it's quite good, but the vocabulary can be huge. Actually, it's worse than that because though the vocabulary could be actually unbounded, right? Because at test time, you might get some sequence and you tokenize, and then you have a token you've never seen before. And people used to assign these UNK token, but that's really ugly and can mess up your perplexity calculations. So this is also not great.

这其实也是以前 NLP 中人们常用的做法。如果你取一个字符串，按照空格或某种正则表达式把它切成块，然后称每个块为一个标记。这种做法好的是每个标记都有意义——因为人类发明了单词，而单词往往具有稳定的语义。但词表大小就是训练数据中不同块的数量——这可能非常大。虽然压缩比确实不错，但词表可能巨大。更糟的是，词表理论上可以是无界的——因为在测试时，你可能遇到一个从未见过的标记，而人们过去会分配一个 UNK 标记来处理，但那很丑陋，还可能搞乱你的困惑度计算。所以这也不好。

---

### Byte-Pair Encoding (BPE)

OK, so what we're actually going to do is called byte pair encoding. And this was introduced a long time ago for data compression. Way before language models were really on the scene, really. It was first introduced to NLP for doing neural machine translation. And the first paper that used BPE for LLMs was GPT-2. So the basic idea is that you're going to train the tokenizer on raw text to construct a vocabulary that's tailored to the data. And you're also going to have this property that everything becomes-- can be tokenized. If it's rare, then it just breaks up into smaller units rather than having this UNK token. So common sequences are going to be represented as one token. Rare sequences are going to be split into multiple tokens. That's the idea.

好，那么我们实际要用的叫**字节对编码**（Byte-Pair Encoding, BPE）。这其实是很久以前为数据压缩引入的技术，远在语言模型出现之前。它在 NLP 中最早被用于神经机器翻译。第一篇将 BPE 用于 LLM 的论文是 GPT-2。基本思路是：在原始文本上**训练分词器**，构建一个**针对数据定制**的词表。并且你有这样一个性质：一切都可以被分词——如果是罕见的，它就分解成更小的单元，而不是用 UNK 标记。所以常见序列会被表示为一个标记，罕见序列则拆成多个标记。这就是核心思想。

---

So the algorithm is fairly simple, conceptually. So you start, basically, with your corpus. Let's assume it's one long sequence. You get a byte sequence. Each byte starts as a token. And then we're going to merge successive pairs of adjacent tokens that occur the most frequently.

算法在概念上相当简单。你从语料库开始——假设它是一个长序列。你得到字节序列，每个字节起步是一个标记。然后我们**合并**最频繁出现的相邻标记对。

---

So let's step through how this is going to work in code. So here's a simple string, "the cat in the hat," and here's the implementation of the BPE algorithm. So we're going to turn that into a sequence of bytes. And then we're going to-- first, we're going to, basically, count the number of times successive tokens appear. So 116, 104 shows up twice, so we get this. And then we're going to find the pair that happens the most number of times. So that's 116, 104. I guess there's a few ties, but we'll just take the first one. And then we're going to merge that pair. And by merging that pair what we do is we create a new token. In this case, this is going to be called token 256. It's going to represent this pair, and we're going to add it to our vocabulary. So 256 is going to represent the sequence of th. So t and h have been merged. And we're going to call-- every time we see th, we're going to use 256 to represent that. And then we go through indices, and then we replace every occurrence of 116, 104 with 256. So those two places have been replaced. And then we iterate.

让我们通过代码一步步来看这是如何运作的。这是一个简单字符串 "the cat in the hat"，这是 BPE 算法的实现。我们把它转换成一序列字节。首先，我们统计相邻标记对出现的次数。116, 104 出现了两次。然后我们找到出现次数最多的对——那就是 116, 104。可能有些并列，我们就取第一个。然后我们**合并**这个对。通过合并这个对，我们创建了一个新标记——在这个例子中是标记 256。它代表这个对，我们将其添加到词表中。所以 256 代表 "th" 这个序列——t 和 h 被合并了。每次我们看到 "th"，就用 256 来表示它。然后我们遍历索引，把每个出现的 116, 104 替换成 256。然后迭代重复。

---

So the next time we do this, we're going to find 256 and 101. We're going to merge that. And now we have 257. And then we're going to merge that one more time, and we're going to get 258. So over time, the sequence is shrinking and the vocabulary size is growing.

下一次迭代时，我们会找到 256 和 101，合并它，得到 257。然后再合并一次，得到 258。所以随着时间推移，序列在缩小，词表在增长。

---

So now that you have a tokenizer, how do you tokenize new text? Well, you take a new string and you encode it. And conceptually, what happens is that you basically go through the set of merges that you've made, and then you just apply the merges to your string. So that will give you a sequence.

有了分词器之后，如何对新文本做分词呢？你取一个新字符串，编码它。概念上，你遍历你做过的那组合并操作，然后把这些合并应用到你的字符串上。这就会给你一个序列。

---

So I went through this a bit fast, just in the interest of time. I will say that this implementation works. This is a full-blown BPE implementation. It's extremely slow. So in Assignment 1, we're going to ask you to, basically, make it faster. So currently, encode loops over all the merges, which is very slow because you might have-- the number of merges you have is essentially the vocab size minus 256. So you only want to loop over the merges that matter. And you have to build some indices to make that happen. There's some details around special tokens. Conceptually not deep, but important to building a modern tokenizer. Another thing is that I've presented the tokenizer just for simplicity. As you take an entire string and then you try to tokenize it, really, what happens is that you break it up into-- your text into chunks, and then you apply tokenizer on each chunk. So that's going to be much faster. And then try to make it as fast as possible. At some point you might realize that Python is just not very fast. And if you want to implement it in your favorite language, Rust or C or something, then go for it.

我讲得有点快，为了节省时间。我要说的是，这个实现是有效的，它是一个完整的 BPE 实现——但**极其慢**。所以在作业一，我们要你们把它搞快。目前的 encode 把所有合并操作都循环一遍，这非常慢，因为合并次数本质上是词表大小减 256。你只想循环那些有意义的合并，必须构建一些索引来实现。还有一些关于特殊标记（special tokens）的细节——概念上不深，但对构建现代分词器很重要。另一件事是，我演示的分词器只是为了简单——你取整个字符串然后做分词，实际做法是把文本切分成块（chunks），然后在每个块上应用分词器，这样会快很多。然后尽量做到最快。到某个程度你可能会意识到 Python 就是不够快——如果你想用你喜欢的语言（Rust 或 C 等）来实现，那就去干吧。

---

## Summary

OK, so quick summary. Tokenizers convert between strings and tokens or indices. The previous character-base, byte-base, word-base are highly suboptimal in their own way. BPE is effective heuristic that is data driven. So it seems to be pretty effective. Now, like I said before, maybe next year, I don't have to teach this, but for this year, we're stuck with tokenization. Even if we get rid of tokenization though, I think whatever solution replaces it, I think, has to satisfy the following properties. If you have the model, the transformer needs to operate on some sort of abstractions of the sequence. And this is most evident if you think about not just text, but video or DNA sequences where the individual bytes or units are actually quite low signal to noise, and you have to do some sort of abstraction to lift it into a place where you can do modeling on that. And then finally, as I mentioned, chunks should be variable. You want adaptive computation. Not all bytes are treated the same. And if you don't do that, I think, you're going to be suboptimal. So any end-to-end solution also, I think, has to have these properties.

快速总结。分词器在字符串和标记（或索引）之间做转换。之前的基于字符、基于字节、基于单词的方法各有各的严重次优之处。BPE 是一种数据驱动（data-driven）的有效启发式方法，看起来相当有效。正如我之前说的，也许明年我就不用教这个了，但今年我们还得讲分词。即便我们摆脱了分词器，我想任何取代它的方案也必须满足以下性质：Transformer 模型需要对序列的某种**抽象**（abstraction）进行操作——这在你考虑的不只是文本，还有视频或 DNA 序列时最为明显，因为在这些情况下单个字节或单元的信噪比相当低，你必须做某种抽象才能把它提升到一个可以建模的层面。最后，如我所说，块（chunks）应该可变——你需要**自适应计算**。不是所有字节都被同等对待。如果不这样做，你的方案将是次优的。所以任何端到端的解决方案，我认为也需要具备这些性质。

---

OK. So with that, I will end. Next time, on Wednesday, we're going to start the unit on resource accounting. Which is sort of a baby system, I would say. And then after that, we're going to go back into architectures and go from there. All right.

好，我就讲到这里。下周三，我们将开始**资源核算**（resource accounting）单元——算是系统方面的入门。然后我们再回到架构部分，从那里继续。好。
