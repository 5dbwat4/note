---
title: "Guest Lecture: Dan Fu"
---

# Stanford CS336: Language Modeling from Scratch — Guest Lecture by Dan Fu / 斯坦福 CS336：从零开始的语言建模 —— Dan Fu 客座讲座

**Spring 2026 / 2026 春季**

---

## 1. Opening Remarks / 开场白

Thanks so much, everyone, for coming. I think you have a pretty cool course here. And thanks, of course, Percy, for inviting me to give a talk. So I think in this class, you're mostly talking about training and how to train these language models, and get to this place where we can have these things that can talk back to us. And today, I'm going to talk a little bit about once you have one of those models, what it looks like from the other side—what it looks like to actually serve these models, do inference, turn these things from electricity, into tokens, into intelligence. And also what are some of the fun research problems and research things that you can do when you look at it from that standpoint.

非常感谢大家来听这场讲座。我觉得这门课非常棒。当然，也要感谢 Percy 邀请我来做报告。据我所知，这门课主要讲训练——如何训练语言模型，让它们达到能够与我们对话的水平。今天我要聊的，是当你拥有了这样一个模型之后，从另一端看它是什么样子——如何真正地服务这些模型、执行推理，把这些东西从电力变成标记，再变成智能。此外，我还会讲，当你从这个视角出发，有哪些有趣的研究问题值得探索。

---

## 2. The New Industrial Revolution / 新的工业革命

I'll start with some high-level motivation. I think one thing that's become abundantly clear to all of us is that we are really going through almost a new industrial revolution in terms of these models and their capabilities. These slides I made during my job talks two years ago—so the exact examples are going to be pretty old—but you can do human-level text generation, code generation, Cursor, Claude Code, GPT 5.5, not just 4. You can generate images and videos or understand images and videos and process them. You can start to understand new modalities. So we're starting to see some of the applications in the sciences, in bio and health, DNA models—all these sorts of things.

我先从一些宏观动机讲起。我觉得有一件事已经变得非常明显：就这些模型及其能力而言，我们几乎正在经历一场新的工业革命。这些幻灯片是我两年前做求职报告时做的——所以具体例子已经相当老了——但你可以看到：人类水平的文本生成、代码生成、Cursor、Claude Code、GPT 5.5（不只是 4）。你可以生成图像和视频，或者理解它们、处理它们。你还可以开始理解新的模态。我们开始看到一些在科学领域的应用——生物、健康、DNA 模型等各种方向。

---

One of the things that has really been driving my research for a while is the question of what has made these advances possible, and how can we improve on them in the next generations? And one abundant driver of these capabilities is really scale. So again, this is at this point a pretty old figure, but these models have really scaled up in massive ways. So in 2018, at the beginning of my PhD—in antiquity—these were hundreds of million parameter models at their largest. And we were like, oh my God, these things are pretty crazy. By 2019, we thought that they were too dangerous to release—that's GPT-2. I think in this class, you can train a GPT-2 quality model. If you tried hard enough, you could. And today, of course, you have open source models that are a trillion parameters and more. Frontier is probably at 5 to 10 trillion parameters. It's pretty exciting.

一段时间以来，推动我研究的一个核心问题是：是什么让这些进步成为可能？我们如何在下一代中继续改进？而一个关键的驱动力，就是规模。这张图现在已经算很老了，但这些模型确实以惊人的方式快速扩展了规模。2018 年，我刚开始读博的时候——那已经是远古了——最大的模型也就几亿参数，我们当时都觉得，天哪，这些东西太疯狂了。到了 2019 年，我们认为它们太危险以至于不能发布——那就是 GPT-2。我想在这门课里，你们是能够训练出 GPT-2 级别模型的。只要足够努力，你是能做到的。而今天，开源模型已经达到万亿参数甚至更多。前沿模型大概在 5 到 10 万亿参数。这非常令人兴奋。

---

With these, you have a bunch of new capabilities like chat, writing code, analyzing complex text, doing your homework for you, et cetera. What's really remarkable about this is that this transition is happening faster than we think. So certainly, faster than I thought at the beginning of my PhD a few years ago. So I think one really apt analogy—and the dates actually match up in an interesting way. So in 1902, there are 130,000 working horses in Manhattan. These are horses that you don't just have around for giggles, but you actually have them because they play some key role. And these horses would produce—each would produce pounds of manure a day, times 130,000 horses, you have a real manure problem. So in fact, there were entire conferences that were just gathered around the question of—entire academic conferences around, what do we do about all the poop that these horses produce? So in 1898, they actually had one of these in New York. And their conclusion from that conference was, there's nothing we can do about the horse manure. You just have to hold your nose and deal with it. Ten years later, by 1912, cars had already outnumbered horses in Manhattan. So that 10-year transition, you saw these things that have been around for centuries start to be replaced by cars.

有了这些模型，你就有了一系列新能力：聊天、写代码、分析复杂文本、帮你做作业等等。真正了不起的是，这种转变发生得比我们想象的要快——肯定比我几年前刚开始读博时想的要快得多。我觉得有一个非常贴切的类比，而且时间节点恰好也对得上。1902 年，曼哈顿有 13 万匹工作用马——这些不是养着玩的，而是因为它们扮演着关键角色。每匹马每天产生几磅粪便，乘以 13 万，你就有了一个真正的粪便问题。事实上，当年有整场整场的学术会议专门围绕这个问题展开——我们该怎么处理这些马产生的粪便？1898 年，纽约就开了一场这样的会。会议的结论是：对马粪我们束手无策，只能捏着鼻子忍着。十年后，到 1912 年，汽车在曼哈顿的数量已经超过了马匹。在这十年转变中，你看到那些存在了几个世纪的东西开始被汽车取代。

---

And I think for us, for language models, for a lot of the stuff that we do, that 1912 moment was probably last year. So at least for me, last year, I started writing the majority of my code using these language models. Most people in my team do it. I tell all my students to do it, except when they're doing their homework. But this is a really exciting transition that we're living through.

对我们来说，对语言模型和我们所做的很多事情来说，那个 1912 年的时刻大概就是去年。至少对我来说，去年我开始用这些语言模型写大部分代码。我团队里大多数人也是如此。我也告诉学生这么做——除非他们在做作业。但这就是我们正在经历的、令人兴奋的转型。

---

## 3. GPUs as the New Oil / GPU——新的石油

One of these things that is really driving this is that a lot of the scale is driven by GPUs. So in a very real sense, you could say GPUs are the new oil. You're seeing hundreds of billions of dollars and more of investment into GPUs. History rhymes in interesting ways with similar things, but there are entire countries—entire sovereign wealth funds—that are making these things a major part of their piece. And one thing that is really abundantly clear is that inference is really the piece. So you can think of inference as the engine that turns electricity into intelligence. The same way that oil is only useful in a car if you have an engine that turns that oil into useful kinetic motion, inference engines, GPU kernels, these are the things that really turn these GPUs from sand, like Percy said, into something that we can use today.

推动这一切的一个关键因素，是 GPU 驱动的规模化。所以在某种意义上，你可以说 GPU 是新的石油。我们看到的是对 GPU 数以千亿美元甚至更多的投资。历史以有趣的方式押韵，但一些国家——整个主权财富基金——正在把这些作为它们的核心资产。而有一件事非常清楚：推理就是其中的核心。你可以把推理看作将电力转化为智能的引擎。就像石油只有在汽车里，有一个发动机把石油转化为有用的动能时才有价值一样，推理引擎、GPU 核函数——这些才是真正把 GPU 从沙子（就像 Percy 说的）变成我们今天可以使用的东西的关键所在。

---

These machine learning models, they're really just DAGs of operations. There are some mathematical object that exists in the ether. The inference engines, the GPU kernels, all these pieces—these are the things that you actually have to program and map them down to ML operations. I think you do some of that in this class—I think you implement some flash attention, so some training side. But there's a whole world of complexity when it comes to inference and the inference side of things. So if you take away nothing from today's talk, I hope there's one thing, which is: if you understand inference and understand the inference engines, if you understand the GPU kernels that underlie a lot of the core technology, you can enable full stack innovation in machine learning algorithms.

这些机器学习模型，本质上就是操作的有向无环图（DAG）。它们是存在于抽象空间中的数学对象。推理引擎、GPU 核函数、所有这些组件——这些是你真正需要编程、并将它们映射到 ML 操作上的东西。我想你们在这门课上会做一些相关的工作——比如实现一些 flash attention，偏训练侧。但当涉及到推理和推理侧时，会有一个全新的复杂世界。所以如果今天的讲座你只带走一件事，我希望是：如果你理解推理、理解推理引擎、理解支撑核心技术的 GPU 核函数，你就能在机器学习算法中实现全栈创新。

---

## 4. The Lifetime of a Token — Overview / 一个标记的生命周期——概览

So I'm going to start with, in today's talk, a high-level overview of the lifetime of a token. So when you make a request to one of these models, what happens to that request, how it goes through the entire inference service, what are some of the interesting choices you have to make. And then I'll dive deeper into two more research projects around, if you take certain pieces of this system, what are questions that you can ask and what are some things that you can do.

今天的讲座，我会先对一个标记的生命周期做一个高层概览。当你向这些模型发出一个请求时，这个请求会发生什么？它如何在整个推理服务中流转？你需要做出哪些有趣的选择？然后，我会深入讨论两个研究项目——当你关注这个系统的某些部分时，你可以问什么样的问题、可以做些什么事情。

---

Before I get into all the technical details, I'll quickly make a plug. So I'm here representing two organizations. One is UCSD, where I have a small lab, and some of their work is represented in this talk. Then I'm also representing Together, who did a bunch of the work that's represented in this talk. Together is an AI cloud—so GPUs, inference, fine-tuning, and all the rest. Heavy research background. So including Percy—I don't think you can see my mouse, but he's on the screen. And then we've got a big research presence behind that, and behind a lot of the things that you're going to see in this talk.

在进入技术细节之前，我先快速做一下介绍。我代表两个组织。一个是 UCSD，我在那里有一个小实验室，他们的一些工作会出现在今天的讲座中。另一个是 Together，今天讲座中呈现的很多工作都是由 Together 完成的。Together 是一个 AI 云平台——提供 GPU、推理、微调等服务，有很强的研究背景。包括 Percy——我想你们看不到我的鼠标，但他就在屏幕上。背后有强大的研究团队支撑你们接下来会看到的很多内容。

---

## 4.1 The Inference Engine at a High Level / 推理引擎高层架构

So I'd say, at a high level everything is correct. If you look very closely, you'll see things that are very wrong. This is an overview of all the pieces of an inference engine. So I'll give a high-level description of how it works. So you get a request in. The first thing that's going to happen is that the request gets scheduled to various different GPUs. You might have disaggregated prefill and decode on different machines. You'll run that request against a KV Cache to see, have I seen this request or versions of this request before? Is there some compute that I can actually save? Then you'll start executing the core machine learning code. So here are new tokens, here are new operations that we need to compute. There are various optimizations that you can make. So you can split that computation across different machines. You can parallelize across different nodes. You can parallelize it within a node across different GPUs depending on the size of your model, depending on how you can split that up. And I think one of the exciting things is that, as the hardware is developing, we're actually going to start to see more different choices that you can make there.

概括来说：如果从高层看，一切都是对的；如果仔细看，你会发现很多错误。这是一个推理引擎所有组成部分的概览。我来讲讲它是如何工作的。一个请求进来后，首先会被调度到不同的 GPU 上。你可能会把预填充和解码分离式部署在不同的机器上。你会用 KV 缓存来检查这个请求——我之前见过这个请求或它的变体吗？有没有可以节省的计算？然后，你开始执行核心的机器学习代码：这里有新的标记，有需要计算的新操作。你可以做各种优化：把计算拆分到不同的机器上、跨节点并行、在节点内部跨 GPU 并行，这取决于模型的大小和拆分的策略。我认为一个令人兴奋的点在于，随着硬件的发展，我们将会在这些层面看到越来越多不同的选择。

---

But once you make all those choices, once you execute all the code at the end, you get the tokens that you can say, "Hey, ChatGPT, what did Percy mean when he said linear regression, because I skipped that day in my class?" And you get this whole end-to-end experience.

一旦你做了所有这些选择、执行完所有代码，得到的就是标记，你可以问："嘿，ChatGPT，Percy 讲线性回归的时候是什么意思？我那天没去上课。"然后你获得的就是一整套端到端的体验。

---

## 5. Workload Characteristics / 工作负载特征

One of the things that I think is useful to start thinking about is, what do these different workloads look like? And there's quite a bit of different things. One of the things that you want to think about is, when you're actually serving production traffic, it doesn't necessarily look like—certainly, doesn't look like the type of tokens that you see during training. But it also doesn't look like if you just made up a traffic workload in your head. So what is the type of thing that we typically see? So for a particular workload, you'll see a particular distribution of input and output tokens.

我认为值得开始思考的一件事是：这些不同的工作负载长什么样？它们之间差异相当大。有一件事你要考虑的，是当你真正在服务生产流量时，情况绝对不像——肯定不像你在训练时看到的那种标记分布。它也不像你在脑海中凭空编造的工作负载。那么我们通常会看到什么呢？对于特定的工作负载，你会看到特定的输入和输出标记的分布。

---

So let's take a coding workload. So let's say you're somebody like Cursor, where you have your whole code base is available to the agent and you're asking questions about it. Typically, what that will look like is that you'll have a long amount of input—so tens of thousands of input tokens. And then depending on how you've trained your model, the model might output some amount of thinking tokens, or it might output some short input. And this will change based on workload. It'll change based on model. So a coding workload, for example, will look very different from a summarization workload, or a narrative summarization. So if your work involves pasting entire books into a chat window and then talking back and forth to figure out what's happening, that's going to look very different than a standard chat thing. So if you just go to chat and say, "Hey, explain to me first-order calculus" or whatever, that's going to have very different workload shapes.

拿编程工作负载举例。比如你是 Cursor 这样的产品，你的整个代码库对代理可见，你问一些相关问题。通常的情况是：输入非常长——数万个输入标记；然后根据模型训练方式，模型可能会输出一些"思考标记"，或者输出一个短的回答。这会因工作负载而变化，也会因模型而变化。编程工作负载与摘要工作负载、或叙事性摘要工作负载，看起来会非常不同。如果你的工作是把整本书粘贴到聊天窗口里，然后来来回回地讨论发生了什么——那跟一个标准的聊天场景就完全不同。如果你只是打开聊天窗口说："嘿，给我解释一下一阶微积分"之类的，那是一种完全不同的工作负载形态。

---

The way that we use language models today, there's very turn-based agentic workflows. So when you're coding, you go back and forth with your coding agent, say, "Hey, do this." "No, I didn't mean that, do that." Your coding agents themselves can iterate on the language models quite a bit. So they might invoke some tools and say, grep search for something in my code base, and then take that and go feed it back to the model. I might try to do an internet search and look up this thing that my user asked me. So typically, you have these multiple turns in your conversation.

如今我们使用语言模型的方式，有很强的基于回合的智能代理工作流特征。当你编程时，你和编程代理来回交流："嘿，做这个。""不对，我不是那个意思，做那个。"你的编程代理本身也可以反复调用语言模型。它们可能会调用工具，说在我的代码库里 grep 搜索某个东西，然后拿结果再喂回模型。我可能尝试去互联网搜索用户问的东西。所以通常，对话中有多个回合。

---

Now, another interesting piece is different applications will have different times. So if you're in a fast, interactive chat-based loop, or if you're talking on your phone to ChatGPT in voice mode, you might have relatively quick responses. If, on the other hand, you've put together an agentic workflow where you say, "Hey, go do this for me, I'm going to leave you alone and just iterate on your own," you'll have a different cadence. If at some point your agent gets stuck and says, "Hey, help, I need to ask for advice," and you don't notice it, there might be another gap between turns. So all of these things start to define what your workload looks like. So how many new tokens do you get in it every time? How many tokens are you going to generate? How long is my session? Am I a very sticky user who keeps going back and forth with my Claude Agent, or am I a user who's just going to ask one question and then leave and come back the next day? And of course, how long between turns do you have?

另一个有趣的点是，不同的应用有不同的时间特性。如果你是在快速的、交互式的聊天循环中，或者你正在手机上用 ChatGPT 语音模式对话，你可能会得到相对较快的响应。反过来，如果你设置了一个智能代理工作流，说："嘿，帮我去做这个，我不管了，你自己迭代吧"——那就会有不同的节奏。如果在某个时刻你的代理卡住了，说："嘿，救命，我需要请教"，而你没注意到，那么回合之间又会有另一个间隔。所有这些因素都开始定义你的工作负载长什么样：每次获得多少新标记？你要生成多少标记？会话有多长？我是一个不断和 Claude 代理来回互动的高粘性用户，还是一个只问一个问题就走、第二天再来的用户？当然，还有回合之间间隔多久？比如我有一个和 ChatGPT 代理的聊天，关于我每周应该如何安排健身，但我每两周才跟它互动一次——这是一种完全不同的流量模式。

---

And then of course, depending on your application, you might have different targets. So if you have an interactive application, you might say, "I want to get the first tokens back in less than a second," so that the agent can say, "Hey, I'm thinking and I'm going to say blah de blah de blah." Or I might say, "I know I'm going to be generating 500 tokens, and I want that whole response to come back within a certain amount of time so that my user can read it fast enough"—all these pieces.

当然，根据应用不同，你可能还有不同的目标。如果你是一个交互式应用，你可能会说："我希望第一个标记在一秒内返回"，这样代理可以说"嘿，我在思考，我要说 blah blah..."。或者你可能会说："我知道我会生成 500 个标记，我希望整个响应在某个时间内返回，让我的用户能足够快地读完"——所有这些都是需要考虑的维度。

---

## 6. Prefill and Decode / 预填充与解码

So as that request comes in, there are a few basic pieces that come in. I'll rest a bit on the prefill and decode piece in a little bit. So let's say you have some amount of text that comes in—the first thing you're going to do is you're going to tokenize it. I think you're all familiar with that. But then once there, you start getting into a somewhat complex scheduling regime because you have to ask questions like, "Have I seen these tokens before? Can I just look up some of the activations in a cache?"

当请求进来时，有几个基本步骤。我稍后会详细讲预填充和解码。假设有一段文本进来，首先你要对它做标记化——我想你们对这个都很熟悉了。但之后，你开始进入一个相当复杂的调度机制，因为你要问这样的问题："我之前见过这些标记吗？我能直接从缓存中查找一些激活值吗？"

---

And then you get to basically these two major pieces of the actual machine learning computation. These are called prefill and decode, and they're very different beasts. So prefill means let's say you have 10,000 tokens that you've never seen before, and you want to go compute what the activations and what the logit should be. So 10,000 tokens in, one token out. That's a very compute-bound operation. So that actually looks pretty close to the things that you guys have been looking at for training time. So when you're training, you have some large amount of tokens. You write your flash attention kernel when you run your training loop. Prefill is very similar. You just don't run your backwards pass.

然后你进入机器学习计算的两个核心部分：预填充和解码——它们是完全不同的两种计算。预填充的意思是，假设你有 1 万个之前从未见过的标记，你想计算激活值和 logit 应该是什么。所以输入 1 万个标记，输出 1 个标记——这是一个计算密集型操作。实际上，这与你们在训练时看到的东西非常接近：训练时你有大量标记，写 flash attention 核函数，运行训练循环。预填充非常类似，只是不做反向传播。

---

And then you have this thing called decode. So decode is when you're then just generating one token at a time. So you pass in these 10,000 tokens. "Hey, here's my code base, tell me what function ABC does?" The model is going to process the whole prompt and then start generating one token at a time—maybe three or four tokens if you have speculative decoding working. And if you think about that operation—so every time you generate a new token, you then have to run that back through the model. If you do the math on that, there's actually not too many flops that you need to compute. So it's going to be a relatively light computation, but it's going to be very memory bandwidth bound. So what that means is you're going to be running—you have to load up the model every time just to generate a single token.

然后你还有解码这一步。解码指的是你每次只生成一个标记。你输入那 1 万个标记："嘿，这是我的代码库，告诉我函数 ABC 是干什么的？"模型会处理整个提示，然后开始每次生成一个标记——如果你用了推测解码，可能一次生成三到四个标记。想一想这个操作：每生成一个新标记，你就要把它再次跑一遍模型。算一下，你会发现实际上不需要太多 FLOP——这是一个相对轻量的计算，但非常受内存带宽限制。这意味着你每次都要加载整个模型，只是为了生成一个标记。

---

At the end, of course, you then have a single number that represents a token that then gets turned into a string. You probably do a little bit of processing on that. So you look for stop tokens. You check. You might run a safety check to say, "Oh, is my user trying to hack into the system in a bad way?" et cetera. And then at the end, you get the tokens. And the inference engine is really running in this loop, waiting for these requests to come in. So it's running this scheduling-execution-token-sampling loop and repeating.

最后，你得到一个代表标记的数字，然后把它转化为字符串。你可能会做一些后处理：查找停止标记、做安全检查——"哦，我的用户是不是在恶意攻击系统？"等等。最终，你得到标记。推理引擎就是运行在这个循环中，等待请求到来。它一直在执行一个调度-执行-标记采样循环，不断重复。

---

## 7. Continuous Batching / 连续批处理

So I'll get into a little bit of—so now we can take one step deeper and start to look at, what does it look like when you have a system that is processing many different requests at a time? So we have this phenomenon called—this technique called continuous batching. The way to read this figure is that time is flowing downward. So as you go down, there are new requests that are coming in. So let's say, if we go to step one, you have some long requests. You have a user that is asking to analyze some long document, and the engine is going and generating a bunch of tokens out. You might have another request that comes in that starts to take up some resources. So these resources are first compute resources—you have to run things over multiple requests at once. They can be memory resources if you're filling up a KV Cache. And so you'll see these multiple requests happening at the same time.

现在我们再深入一层，看看当一个系统同时处理多个不同请求时是什么样子。我们有一种技术叫做连续批处理。这张图的读法是：时间向下流动。随着时间推移，有新请求不断进入。比如在第一步，你有一些长请求——一个用户要求分析一篇长文档，引擎正在生成一堆标记。可能有另一个请求进来了，开始占用一些资源。这些资源首先是计算资源——你需要同时处理多个请求。也可能是内存资源——如果你在填充 KV 缓存。所以你会看到多个请求同时在运行。

---

After a step, that short request might finish and you get a new request that comes in, and maybe it's running for a couple steps. If you have another request that comes in, maybe it's another very long request. That's going to be that orange one in step four. But maybe you don't have enough GPU memory. So you need to store all your KV Cache on your GPU. Maybe you've run out. You might start queuing for some reason there. Then once that long request is done, you can start the new request, and then, et cetera, you can watch it run. So already, you're seeing some of the complexity when you have many different requests living in a system and how it goes on.

经过一步之后，短请求可能完成了，然后一个新请求进来，可能要跑几步。又有一个请求进来，可能又是一个超长请求——就像第四步那个橙色的。但你可能 GPU 内存不够了。你需要在 GPU 上存储 KV 缓存，可能内存已经耗尽。于是你可能开始排队等待。然后等那个长请求完成后，你就可以启动新请求。看，当系统中有很多不同请求共存时，你已经开始看到其中的复杂性了。

---

## 8. KV Cache and Prefix Sharing / KV 缓存与前缀共享

One of the pieces that's quite important is this thing called a KV Cache. So the way to think about this is that you probably have a lot of users who are saying, "Hi, ChatGPT" or "Hi, Claude." And then theoretically, you don't need to compute new activations and run that again for every single user. Or if you have a long book that the user has passed in, you compute, you run the prefill over that once, and then the next time you get some addendum to that request—the next turn in the conversation—you don't need to compute the whole thing again. So we have these mechanisms called KV Caches that use prefix sharing, that say, "Hey, I have this new set of tokens that comes in; use a very traditional data structure like a basic tree, look at which tokens have I seen before, which tokens are new, and then basically, do a lookup of what those activations are going to look like."

其中非常重要的一个组件是 KV 缓存。你可以这么想：你有很多用户都在说"嗨，ChatGPT"或"嗨，Claude"。从理论上讲，你不需要为每个用户都重新计算激活值再跑一遍。或者，如果一个用户传入了一本很长的书，你只做一次预填充，下次有追加内容或下一轮对话时，就不需要重新计算整本书了。所以我们有了这些称为 KV 缓存的机制，它利用前缀共享，说："嘿，我有一组新标记进来了，用一个传统数据结构比如基础树，看看哪些标记之前见过，哪些是新的，然后查找那些激活值应该是什么样子。"

---

## 9. Model Parallelism / 模型并行

Once you actually have the computation on the GPUs, there's various ways to split it. So I'm not sure if you talked about this too much, but let's say you have a trillion parameter model and you're running on 80 gigabyte GPUs—you're not going to be able to fit the whole model onto each GPU. So there are various ways that you might split it. So you might take every tensor and split it four ways across four GPUs. This is called tensor parallelism. Or today, we have a lot of the state-of-the-art models are mixture of experts models. So you have these individual experts that get selectively activated depending on different tokens. You can split those across different GPUs. The choices that you make at this point will determine what are the bottlenecks. How many GPUs do you need to run your model? How many sessions can you serve at the same time? Et cetera.

一旦计算实际发生在 GPU 上，就有各种拆分方式。我不确定你们讨论过多少这个问题，但假设你有一个万亿参数模型，跑在 80 GB 显存的 GPU 上——你不可能把整个模型装进单个 GPU。所以有各种拆分方式：你可以把每个张量拆成四份分布到四个 GPU 上，这叫做张量并行。或者，今天很多最先进的模型是混合专家（MoE）模型——每个专家根据不同的标记被选择性激活，你可以把它们拆分到不同 GPU 上。你现在做的这些选择将决定瓶颈在哪里：你需要多少块 GPU 来运行模型？你能同时服务多少个会话？等等。

---

## 10. Prefill/Decode Disaggregation / 预填充/解码分离式部署

One of the big things that happens is that we tend to split prefill and decode onto different GPUs, different sets of machines, and that's because they have very different compute bottlenecks and compute characteristics. So prefill looks a lot like what you guys do during training. You just run it. It's very flop-heavy. You can really use the most out of your GPUs. Decode on the other hand is very memory bandwidth heavy. Because you're not doing that much compute, but you still have to load up all the model weights at the same time. These things will also take different amounts of time. So prefill will typically take a lot longer than a single decode step. But you're going to be running a lot more decode steps, because you will run prefill once for a prompt, you'll run decode once for every token that you generate. So a very basic optimization that pretty much we've all started adopting is that you'll run prefill on one set of workers, decode on another set of workers, so that you can specialize those two computations to different pieces of the stack.

一个很重要的趋势是，我们倾向于把预填充和解码放到不同的 GPU、或不同的机器组上，因为它们有完全不同的计算瓶颈和特性。预填充很像你们在训练时做的事——直接跑，非常吃 FLOP，你可以充分利用 GPU。而解码非常受内存带宽限制——因为计算量不大，但你仍然需要同时加载所有模型权重。这两者所需的时间也不同：预填充通常比单步解码要多花很多时间，但解码步骤会多得多——因为一个提示只做一次预填充，但每生成一个标记就要做一次解码。所以一个非常基本的优化，几乎所有人都在采用，就是在一组工作者上跑预填充，在另一组工作者上跑解码，以便针对计算栈的不同部分做专门优化。

---

And turns out, there's a lot of innovation that you can have when you have these splits. Some things that you might have heard of—that when NVIDIA bought Grok. So NVIDIA, the King of GPUs, buys this new inference chip. One of the reasons is that the decode workload is so different from prefill workload, that if you're looking at it, you can be using very different chips. So for example, in the next generation of hardware, NVIDIA is planning on using its GPUs for the prefill side, using these LPU Grok chips for the decode. You see similar things with Cerebras. So OpenAI has this compute partnership with Cerebras. It's another chip that's much better at decode. There are other companies like SambaNova and so on, that are also making bets on various parts of this space.

事实证明，当有了这种分离之后，会涌现出很多创新。你可能听说过 NVIDIA 收购 Grok 的事——NVIDIA 作为 GPU 之王，买了这个新的推理芯片。其中一个原因就是解码工作负载与预填充差异如此之大，以至于可以使用完全不同的芯片。例如，在下一代硬件中，NVIDIA 计划用 GPU 做预填充侧，用 Grok 的 LPU 芯片做解码。你在 Cerebras 身上也看到了类似的情况——OpenAI 与 Cerebras 建立了计算合作关系，Cerebras 是另一种更擅长解码的芯片。还有像 SambaNova 等公司，也在这一领域的不同环节下注。

---

## 11. Production Bugs at Scale / 大规模生产中的 Bug

Here's a fun one, an interesting one. So when you actually start deploying these inference engines at scale—so when you're starting to serve trillions of tokens or more a day—you start to get some pretty nasty bugs. And basically, one of the characteristics of these large-scale systems is that something that will work well at a small scale will inevitably start breaking at a large scale. So we're talking events that happen with 0.001% of the time or less. Some of these can be NaN. So sometimes, you'll have a kernel that is very slightly wrong. But the conditions for triggering it are very rare. And you will start having some of your logits turn into NaNs halfway through the computation. When that happens, we figured out that the model starts outputting the same token. So I think some model, the output just started saying, "Hi, hi, hi, hi," after a while, or start outputting exclamation points—and you get caught into these loops.

讲个有趣的。当你真正开始大规模部署这些推理引擎——每天服务数万亿标记或更多时——你就会遇到一些相当恶心的 bug。这些大规模系统的一个特点是：在小规模下运行良好的东西，在大规模下迟早会出问题。我们说的是发生概率只有 0.001% 甚至更低的事件。有些可能是 NaN。有时你有一个核函数有非常微小的错误，但触发条件极其罕见。于是你的某些 logit 会在计算过程中变成 NaN。我们发现发生这种情况时，模型会开始重复输出同一个标记——比如有些模型的输出过了一会儿就开始"hi, hi, hi, hi"，或者开始疯狂输出感叹号，陷入这种循环。

---

Another model, at some point, someone made a change to how you're handling tool calls. So tool calls are when the model says, "Hey, I want to make an internet search" or something like that. At some point, those tool calls stopped being processed correctly in one of the engines. And the symptom for that was the completion lengths shot up because the model would say, "Hey, make an internet search," and then when the model is behaving correctly, it says, "Hey, make an internet search. I'm done. Go return to the user." But in this case, it wasn't returning correctly. So it'd say, "Hey, make an internet search. Hey, make an internet search. Hey, I don't know why there's no internet search going on." It would just get into this very long doom loop for tens of thousands of tokens.

还有一次，有人在某个引擎中改动了工具调用的处理方式。工具调用就是模型说"嘿，我要进行一次互联网搜索"之类的操作。结果，这些工具调用在某个引擎中不再被正确处理了。症状是补全长度暴增——因为模型会说"嘿，做个互联网搜索"。正常行为是模型说"嘿，做个互联网搜索。我完事了，返回给用户吧。"但这次没有正确返回，模型就一直说"嘿，做个互联网搜索。嘿，做个互联网搜索。嘿，不知道为什么没有搜索在进行啊。"就这样陷入了一个长达数万标记的末日循环。

---

There's another one that was interesting because it actually took out a number of insurance providers at the same time. And it actually got blamed on a quantization issue. But actually, what was happening was a much more subtle bug where the model would just suddenly, randomly start to output Chinese characters when it had no reason to. So for some models, there's some speculation—"Oh, they must have fine-tuned on a Chinese model because my model suddenly starts speaking back to me in Chinese." Actually, what was happening is that there was just an off-by-one error in one of the kernels, and it would be a very subtle bug. So sometimes, you would read in some extra uninitialized memory space from your GPU, run it through attention, and then at the end of that whole process, you get a random Chinese character. Then the model will go, "Why did I start suddenly thinking in Chinese? The user must be asking me a question in Chinese," and then it will just veer off into Chinese. So sometimes when this happens, it's because the model has legitimately been trained to think in Chinese. Sometimes, it can just be an off-by-one bug in somebody's code.

还有一个有趣的 bug，它实际上同时搞崩了好几家保险公司。最初被归咎于量化问题。但实际上更微妙——模型会在毫无理由的情况下突然随机输出中文字符。有些人猜测："哦，他们肯定在中文模型上做了微调，因为我的模型突然开始用中文回复我了。"实际上，只是因为某个核函数里有一个差一错误，是个非常微妙的 bug。有时，你会从 GPU 读入一些未初始化的额外内存空间，通过注意力计算跑一圈，最后出来一个随机的中文字符。然后模型就会想："我怎么突然开始用中文思考了？用户一定是在用中文问我问题。"然后就一路偏航到中文里去了。所以有时出现这种情况，是因为模型确实被训练成会用中文思考；但有时，可能只是某人代码中的一个差一错误。

---

## 12. KV Cache Management / KV 缓存管理

Some interesting things that are starting to happen in a lot of the more advanced inference stacks. So a major piece of running large production systems is that you want to have as large of a KV Cache as possible. So it is best if you can cache requests from many different users or from the same user across many different sessions, and be able to run as many sessions as possible. You first started this by storing your KV Cache on GPU, and then you quickly run out of GPU memory. So the next, you can start storing into CPU DRAM. So if you're paying attention to Jensen's keynotes, he's recently started getting very obsessed with CPU performance. One of the reasons is because the past generation of CPUs was actually really slow. And as a result, started bottlenecking a bunch of very important workloads. As a result, you start to pay attention because if your $500,000 machine is being bottlenecked by the $1,000 CPU that you purchased to put on top of it, that's not a great place. One of the reasons that can happen is that you might be storing your KV Cache on CPU memory. And so you really care about the speed of being able to read that KV Cache back.

在更高级的推理框架里，发生了一些有趣的事情。运行大型生产系统的一个关键点是：你希望 KV 缓存尽可能大。最好能缓存许多不同用户的请求，或者同一个用户跨多个会话的请求，并且能同时运行尽可能多的会话。你一开始把 KV 缓存放在 GPU 上，很快就耗尽了 GPU 内存。接下来，你可以放到 CPU 的 DRAM 里。如果你关注 Jensen（黄仁勋）的发布会，你会发现他最近对 CPU 性能变得非常着迷。原因之一是上一代 CPU 确实很慢，结果开始成为很多重要工作负载的瓶颈。所以你会关注这件事——因为你花 50 万美元买的机器，被一个 1000 美元的 CPU 给瓶颈住了，这可不是什么好局面。而一个可能的原因就是你把 KV 缓存放在了 CPU 内存里，你就非常关心读取 KV 缓存的速度。

---

Next, you might put more KV Cache onto the disk itself. And then you start caring about SSDs and SSD space. Again, you've probably heard these rumblings about OpenAI buying up all the SSD, all the DRAM in the world. Part of the reason is for stuff like this, where you want to store as much stuff in your KV Cache as you can. And then of course, when you're actually building your engine, there's this complicated dance of, "I haven't seen these tokens in a while. Maybe I'll evict it, send it on to the CPU, or send it into disk, or send it into some other global store. When I get a new request in, I have to go look. I have to go wait for those to come in, fetch them, load them up into my thing, and then we're happy."

再进一步，你可能会把更多 KV 缓存放到磁盘上。然后你开始关心 SSD 和 SSD 空间。你可能听说过 OpenAI 在狂买全世界所有的 SSD 和 DRAM 的消息——部分原因就是为了这些东西：你想尽可能多地把 KV 缓存存起来。当然，在真正构建引擎时，就有一系列复杂的舞蹈："这些标记我已经有一阵子没见了，也许我把它们驱逐出去，送到 CPU 上，或者送到磁盘上，或者送到某个全局存储中。当有新请求进来时，我得去找，得等待它们到来，提取出来，加载到我的东西上，然后一切就绪。"

---

So the question is, for this offloading, is it a particular type of workload that you offload? So here, we actually get to some pretty classic scheduling things. You could have this diagram except for the GPU things on the right. It looks exactly like an operating systems diagram that you might have seen in the '70s or the '80s. Because we used to have this problem where if you opened up too many applications on your computer, you would run out of CPU memory, and then you'd have to put those applications onto the disk. And it is exactly the same workload. So ideally, the least recently used heuristic is actually a pretty decent heuristic. There's probably some OS paper somewhere that says that LRU is within 2x of what you can do optimally. Of course, the best thing that you want to do is, if you could predict the future, you would know, "Oh, I'm about to have a request come in of a particular kind. Let me go prefetch that memory in." It might actually be possible to predict the future. So for example, when you go into your chat app and you bring up some old conversation from a month ago, that's a very strong signal that you're going to go start asking a question about it. You might then want to go load that up onto a GPU. But in a perfect world, you predict the future. If you can't predict the future, you use various heuristics. And really, it's a question of how much traffic you want to put onto your GPU footprint.

那么问题是：这种卸载是针对特定类型的工作负载吗？这里我们实际上回到了非常经典的调度问题。把 GPU 那部分去掉，这幅图看起来就像你可能在七八十年代见过的操作系统图示。因为当年我们面临同样的问题：如果你在电脑上打开太多应用程序，CPU 内存会耗尽，你就得把它们放到磁盘上去——这完全是同一种工作负载。理想情况下，"最近最少使用"（LRU）启发式算法其实相当不错。大概有某篇操作系统的论文说，LRU 在最优解的 2 倍以内。当然，最好的做法是：如果你能预知未来，你就会知道"哦，马上会有一个特定类型的请求进来，让我提前把那段内存取进来。"预知未来可能真的可行——举个例子，当你在聊天应用里打开一个月前的旧对话时，这是一个非常强烈的信号，表明你马上就要问它相关的问题——你可能会想把它预加载到 GPU 上。但在理想世界中，你预知未来；如果做不到，就用各种启发式方法。归根结底，这是个你想在 GPU 上放多少流量的问题——我还没见过有谁想少放流量的。

---

## 13. Next-Generation Hardware / 下一代硬件

Some fun things that are starting to happen. So in the last generation of Blackwell GPUs, NVIDIA started putting together these new GPUs called NVLink 72 Grace Blackwell chips. So these are 72 GPUs that are connected with really fast interconnects. And so you start to do things like, "How can I split my trillion parameter model across all 72 GPUs? Does this make any sense? What does it buy me? What happens?" How do I start to think about fault tolerance? So these things can fail a lot for various different reasons. One reason is that the connectors are flimsy. They're made of plastic, not made of metal. So if you jam the thing in too much, then your cables are going to bend the things a little bit, and then you get really flaky NVLinks, which is a whole thing in itself. But what happens when—so one of the things that you want to start thinking about is, if I've taken a model, split it across 64 GPUs, and I'm serving production traffic against millions of users, trillions of tokens—what do I do when a single GPU goes down? Is there some way to make that fault tolerant? And there's a lot of fun things to think about there. And then, of course, you're starting to see these models have a million contexts or more. How do you actually process it? Do you split that context across many different GPUs? How do you do these different things?

一些有趣的事情正在发生。在上代 Blackwell GPU 中，NVIDIA 推出了 NVLink 72 Grace Blackwell 芯片——72 个 GPU 通过极高速的互联连接在一起。然后你就开始思考："我要怎么把万亿参数模型拆分到这 72 个 GPU 上？这有意义吗？能带来什么收益？会发生什么？"如何考虑容错？这些设备因为各种原因会经常出故障。一个原因是连接器比较脆弱，是塑料的而非金属的——如果你插得太用力，线缆会稍微弯曲，然后 NVLink 就会变得不稳定，这本身就是个大麻烦。你得开始思考：如果我有一个模型，拆分到 64 个 GPU 上，正在为数百万用户、数万亿标记服务——如果一块 GPU 宕了怎么办？有没有办法实现容错？这里面有很多有趣的问题。当然，你还会看到这些模型有百万级别的上下文窗口甚至更大。你如何实际处理？要不要把上下文拆分到很多 GPU 上？怎么处理这些事？

---

## 14. Cache-Aware Prefill-Decode Disaggregation / 缓存感知的预填充-解码分离调度

So I want to dive—just very briefly highlight one set—one example of an optimization that you can start to make when you start looking at this whole process from a systems level. So this is a piece of work that we put together a few months ago called Cache-aware Prefill-Decode Disaggregation. It's a very simple optimization. It's two lines of code in the routing layer, but can actually make a pretty big difference. So the basic idea is, you have all these requests that are coming in. Most of them are going to be turn-by-turn requests in a conversation, where somebody's already started a conversation. But let's say your average conversation lasts 10 turns and then the user goes away—that suggests that 10% of your requests are going to be very fresh, very new requests. So when you have a new request that comes in, that's going to be thousands of tokens. It's going to look very different. It's going to be a lot more expensive to compute. You don't necessarily want to put that prefill against a short conversation where you're halfway through a conversation.

我想快速讲一个优化实例，展示当你从系统层面审视整个流程时可以做什么。这是我们几个月前做的一项工作，叫"缓存感知的预填充-解码分离调度"。这是一个非常简单的优化——在路由层只加了两行代码，但效果相当显著。基本思路是：进来的请求大部分是对话中的逐轮请求——某人已经开始了对话。但假设平均每次对话持续 10 轮用户就离开了，这意味着 10% 的请求是全新请求。当一个全新请求进来时，那是数千个标记，看起来完全不同，计算成本高得多。你不一定想让它的预填充和一个中途对话的短请求跑在同一时间。

---

So someone pastes in a book and says, "Hey, talk to me about this book." You don't want that running at the same time as someone who's midway through a conversation, like, "Chat, explain to me why 1+1 equals 2," "1+1 equals 2 because numbers and whatnot." "Oh, I don't get it." You don't want that very short question and answering to happen in the same time, on the same GPUs, as the very long request. So you can put together this really simple router that says, OK, if we have a new request that comes in that's very low cache hit rate, send it to one set of GPUs so that those can all process things together, and then send all my other warm requests to another set of prefill nodes. It turns out if you do this, you can get up to 40% faster serving with these very, very simple optimization.

比如有人粘贴了一本书说"嘿，跟我聊聊这本书"，你不希望这个操作与对话中途的"Chat，给我解释一下 1+1 为什么等于 2"同时运行在同一批 GPU 上。那个短问答不应该和超长请求混在一起。所以你可以设计一个非常简单的路由器：如果新请求进来且缓存命中率很低，就把它送到一组 GPU，让它们一起处理；把所有其他"热"请求送到另一组预填充节点。结果发现，这么简单的优化就能让服务速度提升高达 40%。

---

So that's one set of things. I'd say, the way that I would characterize where we are in terms of the research and these techniques is that we're very early. So this is the type of thing that in 10, 20 years, they're going to look back on and be like, "Oh, why are these guys talking about this? Isn't this already obvious to folks?" But really, it's because we're starting to see these things, running them at production in new ways, seeing these new bits of traffic in new ways.

这就是其中一类例子。我想说的是，从研究和技术视角来看，我们还处于非常早期的阶段。这些东西在 10 年、20 年后回过头看，人们会说："这有什么好讲的？这不是显而易见的吗？"但实际上，是因为我们才刚刚开始在新型生产环境中运行它们，以新的方式观察这些流量模式。

---

## 15. Megakernels for Faster Decode / 用 Mega 核函数加速解码

All right. So that was an overview of the inference life of a kernel. Now I'm going to talk about two interesting research projects that are very much inspired by some of the things that we see when serving things. So this first one we're going to be talking about language model decode, and how you can make it go a lot faster with these things called Megakernels. This is a collaboration between Stanford and Together. So the fundamental challenge when you're running decode—so decode is the process by which you've processed your prompt and now you're generating one token at a time. The fundamental challenge is that you have to run the whole model to generate a single token. So that means that instead of using all this big parallelism that you get with a GPU that you can do during prefill or training, you've now turned this massively parallel system into basically a glorified memory loader.

好了，以上是对推理核函数生命周期的概览。现在我要讲两个有趣的研究项目，它们非常受我们在服务中观察到的一些现象的启发。第一个项目是关于语言模型解码，以及如何用 Mega 核函数让它快得多。这是斯坦福和 Together 的合作项目。运行解码时的根本挑战在于——解码就是你处理完提示后，开始一次生成一个标记的过程。根本挑战是：你必须跑整个模型才能生成一个标记。这意味着，你没有利用 GPU 在预填充或训练时能提供的大规模并行性，而是把这个大规模并行系统变成了一个高级内存加载器。

---

And one of the things that makes this extra challenging is that the way that we typically write down kernels and run a model is that we will write down kernels and program things one operation at a time. Kernels tend to be pretty challenging to write. I'm sure you guys all had a lot of fun writing Flash Attention. But that means that typically, what we do is we look at all the different operations in a language model, and we will write a single kernel for that operation at a time. So this makes things a lot easier to program because you just have to write your Norm kernel, your MatMul kernel, your attention kernel. But you end up seeing—it ends up introducing a lot of downtime into your system.

让事情更加棘手的是，我们通常写核函数和跑模型的方式是：每次为一个操作写一个核函数。核函数通常很难写——我相信你们都体会到了写 Flash Attention 的乐趣。这意味着，通常我们面对语言模型中所有不同操作时，每次只为一个操作写一个核函数。这让编程容易得多，因为你只需要写归一化核函数、矩阵乘法核函数、注意力核函数。但你会发现系统中有大量空闲时间。

---

So this is an example of what it might look like when you're running inference across your kernel. The way to read this is that on the x-axis, you have time, so time is flowing from left to right. On the y-axis, you have all the different little streaming multiprocessors on your GPU. So on an H100, there are 132 of these. On the B200, there's 148, et cetera. The bars indicate useful work. So when there's a bar here, one of the processors on the GPU is actually doing work, and the empty space is just waiting. So you're just waiting for other operations to finish so that you can have something else go on. And so basically, you get into this position where no matter how well you try to write the kernel, you're always going to have downtime in your GPU. So you're going to have things like kernel launch. So a kernel launch or kernel teardown—that's these big gaps. You're going to have these things called tail effects. So this is just the same way that if you have a short prompt that gets processed with a very long prompt—this same thing goes all the way down to the basic attention operation. If you're processing a batch of inputs and one input is very short, one input is very long, you're going to be waiting for the very long input to finish. And then because you're running these across multiple kernels, you will actually start to see these gaps between kernels start to add up.

这是一个推理核函数的运行示例。读法是：x 轴是时间，从左向右流动；y 轴是 GPU 上所有的流多处理器（SM）。H100 有 132 个，B200 有 148 个，等等。色块表示有用工作——每当有色块，说明 GPU 上的某个处理器在做实际工作；空白就是等待——等待其他操作完成，才能继续下一步。所以不论你多么努力地优化核函数，GPU 上总会有空闲时间。你会看到核函数启动和卸载的巨大时间间隙；你还会看到尾效应——就像短提示和长提示一起处理时，必须等待长提示完成一样。由于你是在多个核函数之间跑，这些间隙会累积起来。

---

So one thing that we put together to try to solve this is a thing called a Megakernel. This is basically saying, instead of treating each operation in the model as its own operation and writing a kernel for it, instead, let's write a single kernel to cover multiple operations at once. This is similar to the fusion that you see in Flash Attention, except done more aggressively across a larger number of things. And in particular, what it does is it turns a GPU from a single device—you start thinking of the GPU as a massive distributed system and saying, "OK, I have all this work that I need to get done. Some of it has dependencies on other stuff. How can I schedule it? How can I distribute the work to maximize my GPU utilization?"

我们提出的一个解决方案叫 Mega 核函数。基本想法是：不要为模型中每个操作各自写一个核函数，而是写一个核函数同时覆盖多个操作。这和你用 Flash Attention 做的算符融合类似，但做得更加激进，覆盖更多的内容。具体来说，它让 GPU 不再被视为单个设备——你开始把 GPU 当作一个大规模分布式系统，然后说："好的，我有一堆工作要做，其中一些和其他事有依赖关系。我该如何调度？如何分配工作来最大化 GPU 利用率？"

---

If you do this just to the attention inference kernel, you get 30% to 70% speedups. And then the nice thing is that you can actually do this to the whole model. So this is one layer of a Llama-1B model. So here, we've basically taken the entire layer and put it together into one kernel. If you look at all these different bars, you see things are overlapped in really weird ways. That's because we are now starting to overlap a weight load from the next layer into the attention, or starting to run parts of reduction before the attention operation is over.

如果只对注意力推理核函数做这个优化，就能获得 30% 到 70% 的加速。而且你可以对整个模型做同样的事。这是 Llama-1B 模型的一层——我们基本上把整层放到一个核函数中了。看这些不同色块，它们以非常奇怪的方式重叠——因为我们开始在注意力计算中还重叠来自下一层的权重加载，或者在注意力操作结束前就开始运行部分归约。

---

Here's one interesting example. So here's one thing that you can do. So if you look at modern LLMs, you have the attention layer. You have the QKV projections. You're going to add some RoPE scaling to it. So those blue lines are QKV plus RoPE. And then the orange lines, this is the beginning of the attention. So one of the insights is that you can start loading in your KV Cache into your attention before you're finished with QKV, and particularly, during decode. So these orange bars with some of these circles—you start the KV Cache load while the QKV plus RoPE is still running. And then once QKV is done, then you have your new query tokens. You can run the rest of the attention operation. So basically, when you have this fine-grained control of GPUs, you can start some operations before others are over.

举一个有趣的例子。看现代 LLM，你有注意力层、QKV 投影、加上 RoPE 缩放——蓝色线就是 QKV+RoPE，橙色线是注意力计算的开始。其中一个洞见是：你可以在 QKV 还没算完之前就开始加载 KV 缓存到注意力计算中，尤其在解码阶段。所以橙色块的那些圆圈——KV 缓存的加载在 QKV+RoPE 还在跑的时候就开始了。等 QKV 完成后，你有了新的查询标记，就可以运行注意力的剩余部分。基本上，当你有这种对 GPU 的精细控制能力时，你可以在某些操作尚未结束时就启动其他操作。

---

Here's another one. So again, the orange is the first part of the attention computation. The red is the O projection that comes after attention. And you have your O projection—start loading the weights before your attention operation is over. We put this together in a very relatively complex CUDA framework with basically instruction and instruction-based abstraction, where we can implement each sub-kernel in its own file, and then have a big virtualized shared memory system to orchestrate the running of these operations. And to do this, we put together this library called ThunderKittens, which is one of these kernel writing libraries. You can think of it as almost like Triton, except more low level, a lot more fine-grained control over things.

再看一个。橙色是注意力计算的第一部分，红色是注意力之后的 O 投影——你可以在注意力操作还没结束前就开始加载 O 投影的权重。我们用一个相对复杂的 CUDA 框架实现了这一点，提供基于指令的抽象：每个子核函数在各自文件中实现，然后有一个大的虚拟共享内存系统来编排这些操作的运行。我们为此开发了一个叫 ThunderKittens 的库——这是核函数编写库之一。你可以把它看作类似 Triton 但更底层、对细节有更精细控制的东西。

---

The payoff is you get near speed-of-light decoding inference. So these numbers are actually a lot better now. But the Megakernel shown by this bar in teal, and you can see it runs a lot faster than some of the other state-of-the-art engines. And on the H100, it's achieving 72% bandwidth utilization, which is near the speed of light on the GPU. So if you just ignore all the complexities of what we're doing here and say, "How fast can the GPU physically go to do this operation?" We are pretty close to 72% of that speed of light.

收益是接近光速的解码推理速度。现在数据比当时还要好得多，但 Mega 核函数——绿色那条——比其他当前最先进的引擎快得多。在 H100 上，它达到了 72% 的带宽利用率，接近 GPU 的物理上限。如果你抛开所有复杂性，就问"GPU 物理上能跑多快做这个操作？"我们接近了这个光速的 72%。

---

So one interesting bit there is a takeaway from that section, is that, if you have very deep control of the kernels and the understanding of the hardware, you can start to enable very different compute paradigms. And all these things, you only see when you start playing with inference at a deep level.

所以说，从这一节的启示是：如果你对核函数有非常深入的控制和对硬件的深刻理解，你就能解锁完全不同的计算范式。而所有这些，只有当你深入玩转推理时才能发现。

---

## 16. Parcae — Stabilized Looped Transformers / Parcae——稳定的循环 Transformer

And now, I'll talk about something that's a little bit new. So this is now getting into the realm of new architectures. And I'm going to be talking about this new model called Parcae. This is some work that comes out of my UCSD lab led by Hayden, and then also in collaboration with Zachary and Taylor. So I'm going to come back to this. At the beginning of the talk, I talked about, "Hey, all these new capabilities are coming because you're starting to scale these models, and parameters, and data." With Parcae, we wanted to ask another question, which is: "Is this the only way you have to scale? Or is there potentially something else—some other way that you can get this quality?"

现在我要讲一些比较新的东西——进入新架构的领域。我要介绍一个叫 Parcae 的新模型。这是我在 UCSD 的实验室由 Hayden 主导的工作，也与 Zachary 和 Taylor 合作。回到开头我讲的：所有这些新能力都源于模型、参数和数据的规模化。对于 Parcae，我们想问另一个问题："这是唯一的方式吗？还是有其他途径可以获得同样的质量？"

---

And with Parcae, this was basically our take on a technique called loop transformers, where you take some blocks of your transformer and you run them in a loop. So instead of having your tokens go all one layer at a time through the model, at some point you say, "Hey, as you're going through, just send it back through that loop at a time." There are a couple different pieces here. So one is, we use some State Space Model theory—some SSM theory—to stabilize this operation. Naively, if you just run this and let the thing train, we saw that the thing was going to blow up. And then the other thing is we started to see some interesting scaling laws that suggest that you want to be scaling the recurrence as you increase the data. So in order to make the best use out of your parameters, you want to actually be reusing them somewhat.

Parcae 本质上是我们对一种叫"循环 Transformer"的技术的探索：你把 Transformer 的某些模块放在循环中运行。标记不再是一次通过一层，而是在某个点之后："嘿，往回循环一次吧。"这里有几个关键点。第一，我们利用状态空间模型（SSM）理论来稳定这个操作——如果单纯让它自己训，模型会爆炸。第二，我们发现了一些有趣的缩放定律，表明随着数据增加，你应该增加循环次数。所以为了最好地利用参数，你应该在一定程度上重用它们。

---

First, I'll talk a little bit of motivation of why we found this looping problem to be very interesting. The basic idea is, let's say you have some activation that's going through part of your model. At some point, it hits these loop blocks and it's just going to run through that same layer some number of times. So that purple block is the recurrent block. And then at the end, you get the thing that comes back. So there are some advantages of this. You can keep your parameters constant, but it gives you a dial to increase your flops. So if you think that more flops equals higher quality, this is a way to increase your quality without paying a higher parameter cost. Another thing is, there's this old work that suggests that you actually get higher expressivity—there are things that you can't express with the same number of parameters, that you can express with these looped models. And one of our driving questions was: "What's the best quality per parameter? What's the best intelligence per parameter and data that these things will allow you to do?"

先讲讲我们为什么觉得这个循环问题很有趣。基本想法是：假设有一个激活值穿过模型的一部分，在某个点它遇到了循环模块，就会在同一层反复运行若干次——紫色块就是循环块，最后得到输出。这样做有几个优势。你可以保持参数规模不变，但获得一个可调节的 FLOP 旋钮。如果你认为更多 FLOP 等于更高质量，这就是在不用增加参数代价的情况下提高质量。还有一个好处：有旧的研究表明，这些循环模型有更高的表达能力——有些事用相同数量参数的非循环模型无法表达，但循环模型可以。我们的核心问题是："单位参数的最佳质量是多少？单位参数和单位数据的最佳智能是什么？"

---

There are some promising initial results. So this is a paper from Tom Goldstein's group at Maryland that suggests that, "Hey, this thing might be better than transformers." These are some results on the ARC tasks. And there's also a bunch of Twitter hype, because about a week before we released Parcae, some dude from OpenAI said that Claude mythos is a looped language model. I don't think it's right. I think he was just making it up. But as a result, it really blew up on Twitter in speculation right before this. Eventually, he had to write this blog post being like, "Hey, my bad, I just made that up. None of it's true." But it was sufficiently interesting.

早期结果很有希望。马里兰大学 Tom Goldstein 组的论文表明，循环模型可能比普通 Transformer 更好——他们在 ARC 任务上有一些结果。还有 Twitter 上的一波炒作：我们发布 Parcae 前一周，OpenAI 的某人说 Claude 某个版本是一个循环语言模型。我认为这不是真的，他只是随口一编。结果 Twitter 上疯狂推测，后来他不得不发博客说"我瞎编的，全都不对"。但这件事确实引起了足够关注。

---

Now, one problem with these looped models is if you looked at any of them and you tried to train them, and then you changed anything about the training algorithm at all—so if you change the learning rate by a little bit, you'd suddenly start to see these models blow up. So if you did a simple thing like a learning rate sweep, you'd see nine times out of ten, this model just isn't going to converge, it's going to blow up. You're going to get NaNs. You're going to get these big loss spikes. And so we were saying, "Hey, there seems to be something wrong with this." So if you're training a model and you're actually scaling it up, and you see these big loss spikes, that suggests something has gone very wrong with your training process—you should take a deeper look and try to figure out what happened. In previous work, there were some hacks like you can put norms in every layer to figure out what's happening or just pick the learning rate of 2e-4. Don't pick any of the other learning rates.

循环模型的一个问题是：你尝试训练它们，只要改动任何训练算法的细节，比如稍微改一点学习率，模型就会爆炸。做一个简单的学习率扫描你会发现，十有八九模型都不会收敛——直接爆炸，出现 NaN，出现巨大的损失值尖峰。所以我们说："这里肯定有问题。"当你训练一个模型并真正扩大规模时，如果看到这些损失值尖峰，说明训练过程出了大问题，你应该深挖。之前的工作有些粗暴的解决方案，比如在每层都加归一化，或者干脆只用一个学习率 2e-4，不用其他的。

---

## 16.1 Stabilization via SSM Theory / 通过 SSM 理论实现稳定化

But we were thinking, "Hey, the existence of these loss spikes suggests that there's probably something more deeply going on." And so we took a bit of a mathematical state space model-esque approach to the stabilization question. Our basic insight was, you can look at this process. So actually, if you look at this process, you try to think about how to analyze it analytically. It's going to be very complicated, because this big R block has tons of parameters. There's all sorts of nonlinearities. There's a Softmax, there's GELU, and RoPE, and all these other things. So if you try to analyze it analytically, it's quite complex. Our insight was, we were just saying, "OK, let's actually just look at the residual of this thing." So how is this activation changing from block to block? Our first empirical observation was, "Hey, it actually doesn't change that much." So each of these residual blocks is changing the vector a little bit, but not really having a massive impact. And as a result, maybe we can actually model this. Maybe we can actually look at what's happening more deeply.

但我们认为，这些损失值尖峰的存在暗示有更深层的问题。所以我们采用了类似数学状态空间模型的方法来解决稳定化问题。基本洞见是：你试着分析这个过程——但那个大 R 模块有海量参数，各种非线性——Softmax、GELU、RoPE 等等，如果你尝试解析分析，相当复杂。我们的洞见是：好吧，我们看残差——这个激活值在每次循环中怎么变化？我们第一个经验观察是：实际上变化不大。每个残差块对向量做了一点点修改，但没有巨大影响。所以也许我们可以对这个过程建模，做更深入的分析。

---

So what we did is we said, "OK, there's all this nonlinear stuff—there's this attention, there's this GELU, there's this big feed-forward network with the intermediates and stuff—we're going to all put that into a box. We're just going to call that R. And this R is going to be some big nonlinear thing. But we're going to put it—just take it to the side. What you're left with is these A and B matrices. So this B matrix is some transformation over your initial vector—what is that first vector before you start the loop? And then this A matrix is how do you transform that residual in each loop?" And what we did is we said, "Hey, this simple thing—if you take all the complexity of the transformer, stick it to the side—you have a relatively simple way of looking at all the previous loop transformers."

我们的做法是：把所有这些非线性东西——注意力、GELU、大前馈网络及其中间层——全塞进一个盒子里，就叫他 R。R 是一个大的非线性块，我们把它放到一边。剩下的是 A 和 B 矩阵。B 矩阵是对初始向量的某种变换——循环开始前的第一个向量是什么？A 矩阵是每个循环中如何变换残差？这个简单模型——把 Transformer 的所有复杂性放到一边——是你审视之前所有循环 Transformer 的相对简洁的方式。

---

And in previous cases, you do end up making some pretty normal decisions. So in one case you just say, "Oh, you just treat it as the identity. You're just going to add things." In another case, it's a fully learnable matrix. And then we said, "OK, what happens if we just—the residual—we observed empirically, that these A and B matrices are actually dominating the magnitude of this equation. What happens if you just drop that complicated nonlinear piece? What do you get out?" Well, you get out actually a pretty simple system that if you use high school calculus, you can just solve it to figure out what the answers are going to be. So here's the closed-form solution. You can actually compute—given what the initial activation is, and what that initial injection is—you can actually just empirically compute what the activation is going to look like at Step T+1.

在之前的工作中，人们做了些相当"正常"的选择：有些直接当恒等映射——直接加；有些用完全可学习的矩阵。然后我们说："好吧，如果我们——我们经验观察到 A 和 B 矩阵实际上主导了这个式子的大小。如果把那个复杂的非线性部分扔掉，会怎样？"结果你得到一个非常简单的系统，用高中微积分就能解出来，得到闭式解。你可以直接计算：给定初始激活值和初始注入值，你就能算出第 T+1 步的激活值是什么。

---

And you notice a couple of things. So this thing is dominated by these A matrices. And especially, this A matrix that you are powering up to a large degree. And from here, what we realize is that there's this quantity called the spectral radius of the A. So spectral radius is basically another word for norm. One way that you can look at this is that you're taking this matrix, you're powering it up to huge amounts. If this matrix can learn to be something like—let's say that this matrix—if you go to scalars, imagine that this matrix is 2. And then this T is like 16 or something, you've now taken this activation, you've blown it up to 2 to the power of 16. And it's really big. And this starts to explain some of those big loss spikes.

你会注意到几个点。这个系统的行为由 A 矩阵主导，尤其是 A 矩阵被不断地做高次幂运算。我们发现了一个叫 A 的谱半径的量——谱半径基本上是范数的同义词。你可以这么看：你在取这个矩阵，把它做高次幂。如果这个矩阵学到的是 2（在标量情况下），T 是 16，你就把激活值炸到了 2 的 16 次方——非常大。这开始解释那些巨大的损失值尖峰。

---

And in particular, what we found is that the choices that you make for these A and B matrices that people have made in these previous papers are either—we call them marginally stable or unstable. Unstable—make the system unstable. And so with Parcae we said, "OK, well, we figured out this thing where if you take this particular look at it, and you let these A and B do whatever they want, you're going to get things that really explode. What if we just constrain A and B such that if you run the math they're not going to explode?" So for A, what we did is we said, "OK, we're effectively going to make that A matrix a negative diagonal matrix. So if you power that up, the term eventually goes to zero, so it doesn't blow up." For B matrix, we're going to stick a really simple linear norm against it, because this B matrix actually only gets applied once and doesn't really blow up. The spectral radius is now going to be less than 1. It's now actually going to be a stable system. And now if you go train this model, what we saw is that you actually saw stable loss curves.

具体来说，我们发现之前的论文中对 A 和 B 矩阵的选择要么是"边缘稳定"，要么就"不稳定"——系统会不稳定。所以 Parcae 说：好吧，如果我们约束 A 和 B，使得从数学上看它们不会爆炸呢？对于 A，我们把它做成负对角矩阵——做高次幂时最终趋向于零，不会爆炸。对于 B，我们加了一个非常简单的线性归一化——因为 B 只应用一次，本身不会真的爆炸。所以谱半径现在就小于 1，是一个稳定的系统。现在你再训练这个模型，你会看到稳定的损失曲线。

---

So Parcae is this stabilized thing where we re-parameterize A and B. You can see that even with the 6e-4 learning rate that was so bad for the other models, you actually got a stable model at the end. And you see that with doing this, you can naturally constrain the state norm of the activations. So that orange baseline is just a completely unconstrained model. You can see it blows up, goes to 10 to the 19th. This blue line is actually a model where you are applying a norm to it. So what happens here is that the model is actually trying to expand the activations because it's saying, "Oh, with more room, I can represent different things better. I can put these different concepts further away from each other or whatnot." And then you're applying norm to it to take that big thing that's trying to expand, then you try to norm it back down to one. And then you have these two pressures that are fighting against each other that manifests in loss spikes. So even though on the right, your norms are very good—you're not seeing the activation actually blow up—you do see that the loss can do some pretty gnarly things. So basically, there's this pretty simple change in the activations that can stabilize the training, stabilize these recurrent loops.

所以 Parcae 通过重新参数化 A 和 B 来实现了稳定化。即使使用其他模型完全无法承受的 6e-4 学习率，Parcae 最终也能得到一个稳定的模型。而且你自然地约束了激活值的状态范数。橙色基线是完全不加约束的模型——可以看到它爆炸了，达到 10 的 19 次方。蓝线是加了归一化的模型：模型实际上试图扩展激活值，因为它在说"哦，有了更大的空间，我能更好地区分不同概念，把它们拉开距离"，然后你加归一化把它们压回 1——这两种对抗的压力就表现为损失值尖峰。所以在右边，虽然范数看起来很好——激活值没爆炸——但损失曲线会变得非常难看。所以通过这个非常简单的对激活值的改动，就能稳定训练、稳定这些循环块。

---

So it's not only a more stable system, you actually also get higher quality models. So this is a table where we are comparing Parcae models against a previous loop transformer called Recurrent Depth Model. You can see higher performance across a variety of applications. Parcae outperforms the previous models and also outperforms strong transformer baselines. This transformer is one of the nanochannel ones where a bunch of people are trying to just get it to learn as fast as it can. And these Parcae models—if you take that same basic transformer architecture, start looping it, and then stabilize it—you get better perplexities, better end-to-end quality as well.

这不仅是更稳定的系统，你还得到了更高质量的模型。这张表把 Parcae 和之前的一个循环 Transformer——Recurrent Depth Model——做了对比。在各种应用中，Parcae 表现更好。Parcae 优于之前的模型，也优于强 Transformer 基线。这个基线是 nanochannel 那种——一群人试图让它学得尽可能快的那种 Transformer。而 Parcae 模型——用相同的基本 Transformer 架构，加循环，然后稳定化——得到了更好的困惑度和更好的端到端质量。

---

## 16.2 Scaling Laws for Recurrence / 循环次数的缩放定律

And then we started to run some very basic scaling laws here. And here, our question was, "OK, this is really, really cute. You can do this looping thing to make things better. But really, should you—is there any evidence that there's something here that we want to be doing looping more aggressively?" So here, I'll take a step back. A few years ago, there was all this work as we started to enter this regime where you wanted to scale up all these models—a natural question is, "Should I make the models bigger or should I just train on more data?" A few years ago, folks started to ask, "How should I scale these two quantities with each other? Should I scale model parameters? Should I scale data?" And we came up with all these very complicated power law curves. What you want to look out for is basically—if that curve is going down into the right, it suggests you should be scaling both data and parameters at the same time. If we were going straight down, that would mean just increase your training data. There's no need to increase your parameters. If it's going flat, just going straight to the right, that means don't increase your data at all, just increase your parameters. But you see, it's going down into the right. That means you should scale data and parameters at the same time. And now you see this. You train a $1 trillion parameter model on $35 trillion tokens, and you get better quality.

我们做了一些非常基础的缩放定律实验。问题是："这个循环方法确实很可爱。但是，有什么证据表明我们应该更激进地使用循环呢？"让我退一步回顾。几年前，当我们进入想扩展模型的阶段时，一个自然的问题是："我应该把模型变得更大，还是用更多数据训练？"人们开始问：这两个量该如何协同缩放？应该缩放参数还是数据？研究者总结出了各种复杂的幂律曲线。关键看曲线的走向：如果曲线向右下方走，说明数据和参数应该同时缩放。如果笔直往下，说明只需增加训练数据，不需要增加参数。如果水平向右，说明只要增加参数，不用增加数据。我们看到的是向右下方走——数据和参数应该同时增加。于是你就看到了：用 35 万亿标记训练万亿参数模型，获得更高质量。

---

So our question was, "OK, where does recurrence fit into this?" And there are a couple possibilities with recurrence. For example, you might conclude you should never run a recurrence. It's better to just keep the same single recurrent model. You might conclude you should do a ton of recurrence, or maybe only some recurrence to a bit. What we're showing here is, at least in these initial scaling laws, all of these curves are ISO-param, ISO-FLOP. So each of these curves is a model. On the left and the right, you have the same number of parameters. As you go down, as you change the colors, we are increasing the amount of flops that you use to train the model by increasing the amount of data. So here, we're varying data and varying the number of recurrences. What we find is that in both of these models, you see this down into the right trend again. So what this is suggesting is that for these fixed parameter training things, as you increase the amount of data, you should actually also be increasing the amount of recurrences that you have. We find that these recurrences follow some pretty classic power laws. So you can actually start to predict—you can get these scaling laws to start to predict quality, as you scale recurrences and your tokens jointly.

所以我们的问题是：循环在这个框架中属于什么位置？有几种可能性。比如你可能得出结论：永远不应该用循环，就当单个循环模型最好。或者你可能会说，应该做大量循环，或者只做少量。我们展示的是，至少在初步的缩放定律中，这些曲线都是等参数、等 FLOP 的。每条曲线代表一个模型。左边和右边有相同数量的参数。随着颜色变化（向下走），我们通过增加数据量来增加 FLOP。我们同时变化数据和循环次数。结果发现在这两个模型中，曲线都呈现向右下方的趋势。这暗示：对于固定参数规模的训练，随着数据量增加，你也应该增加循环次数。我们发现循环次数遵循非常经典的幂律，所以你实际上可以预测——这些缩放定律可以根据循环次数和标记数的联合变化来预测质量。

---

So what about jointly scaling parameters, data, and recurrences? So we have this really complex 3D figure that showed recurrences, and data, and parameters. And it pointed also whatever down into the right, and down that way at the same time. So if you believe that figure, it suggests you should be scaling all three together. But that figure was just really hard to look at, because it was 3D and weird. So these power laws suggest, when you're increasing data you should be increasing recurrence. And then you have other power laws that suggest, when you're increasing data you should be increasing parameters. So obviously, well, it suggests that you should increase all three of them if you can. But one piece here is that if you're going to fix your model size and you're going to increase the amount of data, you should also be increasing the recurrence, which is interesting because as far as I know, all of our models today have no recurrence in them. So they're all at the very left of these curves. And they all have a ton of data, which suggests that there might be something slightly better that we could be doing when training these models.

那么同时缩放参数、数据和循环次数呢？我们做了一个非常复杂的三维图展示循环次数、数据和参数的关系，它也指向右下方同时向下。如果你相信那张图，意味着你应该三者同时缩放。但那图实在太难看懂——三维，怪怪的。所以说，这些幂律表明：增加数据时，应该增加循环次数；还有其他的幂律表明：增加数据时，应该增加参数。因此显然——你应该三者都增加，如果能做到的话。一个关键点是：如果你固定模型大小，增加数据量，你也应该增加循环次数。这很有意思，因为据我所知，今天所有的模型都没有循环。它们都处于这些曲线的最左端，而它们有大量数据——这说明在训练这些模型时，我们可能还可以做得更好。

---

## 17. Closing Remarks / 结语

So that's Parcae. If I take a little step back and go back to the big takeaway of the talk, I think hopefully, I've given you a little sense today of if you understand the inference of these models, if you understand the GPU kernels, if you understand all the pieces that goes into it—you can really start to enable full stack innovation in machine learning algorithms. So whether that's through a new routing algorithm that lets you serve more traffic or serve traffic in a different way. Or new kernels that allow you to run part of your system way faster. Or new architectures that say, "If you have a lot fewer parameters, you can fit them in a subset of your GPUs in a different way, reduce the amount of communication"—these are all different pieces of that research problem that we're seeing today. And yeah, hopefully I've inspired at least one of you in this room to go take a deeper look at some of that. So with that, thanks. Happy to take a few questions.

以上就是 Parcae。退一步回到今天讲座的核心启示：我希望我让你们多少感受到了一点——如果你理解这些模型的推理、理解 GPU 核函数、理解所有相关的组件，你就真正能够在机器学习算法中实现全栈创新。无论是通过一个新的路由算法来服务更多流量、或以不同的方式服务流量；无论是通过新的核函数来让你的系统跑得更快；还是通过新架构——"参数少一些，你就可以用更少的 GPU 装下更多 KV 缓存，减少通信开销"——这些都是我们今天所面对的研究问题的不同侧面。希望我今天至少激励了在座的某个人，去深入探索这些方向。谢谢各位。欢迎大家提问。

---

## 18. Q&A / 问答环节

### 18.1 Training from Scratch vs. Fine-Tuning with Loops / 从头训练 vs. 用循环微调

**Question:** With Parcae, are you training from scratch on the loop? I guess I was wondering if you could take a pre-trained model and add looping to it?

**问：** Parcae 是从头训练循环吗？我在想能不能拿一个预训练模型加循环？

**Dan Fu:** Great question. So there was a really troll blog post from someone a few months ago where it was like, "Hey, I won some leaderboard competition without training a single thing." And what he did was he actually looped two or three layers in a Quinn model, and just saw that on some math things it started having higher quality. So we have a little bit of work trying to look into this that maybe coming out soon. But there could be some models where if you do a little bit of looping just to the pre-trained model, you can get a higher quality thing, which is really weird. It disturbs me. I don't know why that would possibly be the case. But yeah, we'll be—we're quite interested in this. I think we'll be looking at it and hopefully, if I can convince Hayden, he'll be staring at the actual weights to figure out why when you loop it, it gets better.

**Dan Fu：** 好问题。几个月前有人发了一篇很"钓鱼"的博客，说"嘿，我什么都不训练就赢了某个排行榜比赛。"他的做法是拿一个 Quinn 模型，把其中两三层做个循环，发现在一些数学任务上质量确实提高了。我们有一些初步工作正在探索这个方向，可能很快会出来。确实存在一些模型，你只要给预训练模型加一点点循环，就能得到更高质量的东西——这非常诡异，让我感到不安。我不知道为什么会这样。但我们对此非常感兴趣，希望说服 Hayden 去盯着权重来看——为什么循环一下质量就提高了。

---

### 18.2 Inference Implications of Looped Models / 循环模型的推理影响

**Question:** So you talked about compute optimality for the loop models. Can you speak about the inference implications and the memory and how that can make you go faster?

**问：** 你讲到了循环模型的计算最优性，能谈谈推理方面的影响，以及内存如何让推理更快吗？

**Dan Fu:** Yeah. So one of the reasons that I was personally very excited in these loop things is that one of the big bottlenecks to serving inference efficiently actually ends up being GPU memory. So if you have fewer parameters, you can fit, for example, more KV Cache, or you can do less communication because you need to split your model against fewer GPUs and things like that. So there's actually a lot of flexibility that a smaller model will get you. I also had this dream that if you could make the recurrent block small enough, you could actually write a little Megakernel to just do that recurrent in a very fast Megakernel loop. So far, we haven't been able to make those blocks small enough. But I think it's quite interesting. Certainly, with the next generation of the LPU, the Grok chips that are coming with NVIDIA things—those have 250 megabytes of memory or something like that. So the thing that you'll be able to fit into them is very, very small. But maybe you can design something that will actually fit into them, and then you can just keep your weights in memory the whole time and just run your activations through as quickly as you can. So there are non-linear benefits that you can get if you can cross some of these thresholds that I'm hoping that we'll be able to get to pretty soon.

**Dan Fu：** 我个人对循环模型特别兴奋的原因之一，就是高效推理服务的一个大瓶颈实际上是 GPU 内存。如果你参数更少，就可以装下更多 KV 缓存，或者用更少的 GPU 来拆分模型从而减少通信开销。所以说，小模型能带来很多灵活性。我还有一个梦想：如果能把循环块做得足够小，你可以写一个小型 Mega 核函数，在一个非常快的 Mega 核函数中跑那个循环。目前为止，我们还没能把那些块做得足够小。但我认为这非常有意思。当然，下一代 LPU——NVIDIA 的 Grok 芯片——只有大概 250 兆字节的显存，所以能装进去的东西非常非常小。但也许你可以设计一个刚好能装进去的东西，然后一直把权重留在内存里，只让激活值尽快流过。如果你能跨过这些阈值，就能获得非线性收益，我希望我们很快就能做到。

---

### 18.3 Trade-offs of Megakernels / Mega 核函数的权衡

**Question:** What are the trade-offs for Megakernels?

**问：** Mega 核函数的权衡是什么？

**Dan Fu:** The trade-offs are people's blood, sweat, and tears. So Megakernels, turns out they're very, very labor intensive to write. So to give you some context, a full talented kernel engineer over the course of a year will probably be able to write Megakernels for one hardware for two or three models for batch sizes 1 to 16. Go batch size 17, he was like, "Nope, start over." So they're very, very challenging to write. And together, we're trying to put together some compilers that can automate some of that process. But I'd say, it's a very challenging thing to do. I think the basic Megakernel idea has gone in peaks and troughs over the last few decades when it comes to GPU programming. But yeah, so if you can do it, it will go super fast. You will never be able to go faster, but it just takes a lot of energy and a lot of effort.

**Dan Fu：** 代价是人心血和汗水。Mega 核函数极其耗费人力。给你一个语境：一个优秀的内核工程师，一年内大概能为一种硬件、两到三个模型、batch size 1 到 16 写出 Mega 核函数。batch size 变成 17？对不起，从头重写。所以它们真的非常难写。我们在 Together 正在尝试做一些编译器来自动化这个过程的一部分。但我得说，这非常困难。Mega 核函数这个基本思想在 GPU 编程的历史上是起起伏伏的。但如果你能做到，它会超快——快无可快——但就是需要大量精力和努力。

---

### 18.4 Co-design: Model Architecture and Inference Hardware / 协同设计：模型架构与推理硬件

**Question:** So can we talk a little bit more about co-design? And in particular, you mentioned all these new hardware like Grok and Cerebras on the inference side. So if you're designing a model and that's going to be the serving platform, how should you be changing your architecture?

**问：** 能多谈谈协同设计吗？你提到了 Grok、Cerebras 等推理侧新硬件。如果你在设计一个模型，并且知道它会在这些平台上服务，你应该如何调整架构？

**Dan Fu:** Yeah, I think there's a couple of things that you should look at. So one is, you are going to be most constrained by memory first. So if you know that you're going to be taking a model and serving it on a particular Cerebras chip, you want to go look at the Cerebras wafer, and figure out how much memory you have, and then size your model so that it can fit there with enough KV Cache or whatever to spare. If you look at carefully at the Chinese models that are coming out, they've started making some interesting choices that suggest they might be starting to think about the Huawei chips that are coming out. You'll see quantization choices that people make. So if you have a model that you're intending to serve on NVIDIA GPUs, for example, NVIDIA's new Nemotron model that they released, you will train that model in NVFP4. This is an FP4 format that is proprietary to NVIDIA chips. If you're not going to run it on NVIDIA chips—if you're AMD—then you're going to run this other format called MXFP4. They each have their pros and cons. You'll make these subtle choices based on the hardware that you're choosing.

**Dan Fu：** 有几个方面需要考虑。第一，你最受内存约束。所以如果你知道模型要跑在特定的 Cerebras 芯片上，你得去看 Cerebras 晶圆，弄清楚有多少内存，然后调整模型大小，让它能装进去，并留够 KV 缓存的空间。如果仔细看正在发布的中国模型，它们做了一些有趣的选择，暗示它们可能开始考虑即将发布的华为芯片。你也会看到人们做出的量化选择。比如如果模型打算在 NVIDIA GPU 上服务，NVIDIA 新发布的 Nemotron 模型就是用 NVFP4 训练的——这是 NVIDIA 芯片独有的 FP4 格式。如果你不跑在 NVIDIA 芯片上——如果是 AMD——那你会用 MXFP4 这种格式。它们各有优劣。你会根据选择的硬件做出这些微妙的选择。

---

### 18.5 Is Looping Compute-Optimal? / 循环是计算最优的吗？

**Question:** If you just care about compute-optimal training, is it ever optimal to loop as opposed to just adding more parameters, or is it mainly a trick to reduce inference cost?

**问：** 如果只关心计算最优训练，循环是否永远比简单加参数更好？还是说它主要是降低推理成本的手段？

**Dan Fu:** Yeah. So the trick with compute optimal is it is usually, like, given a FLOP budget, figure out what you want to hit. It's almost a little bit contrived in that sense, because if you want a higher quality model, you should just increase your FLOP budget. And if you decided on your model size, just train longer. Or if you're restricted by your model size, then loop longer. Or if you run out of data, then pick the model size that you think will be as overtrained—as well trained as you can for that size. So I think there are choices. And of course, you make all these choices in the context of, "Do I think it'll get picked up? How am I going to serve it? If you're going to release open source, what is the size of model that people can serve on their laptop today?" So I think all these choices go into making a choice of how big a model you choose to train. I think if you just make the model bigger and train it on more data, it's always going to get better. But I think it really depends on those design points.

**Dan Fu：** 计算最优的问题通常是：给定 FLOP 预算，你要达到什么目标？从这个意义上说有点刻意，因为如果你想要更高质量的模型，直接增加 FLOP 预算就行。你决定了模型大小，就训练更长。如果受模型大小限制，就循环更长。如果把数据用完，就选一个你认为是该规模下能训练得最好的模型大小。所以存在很多选择。当然，所有这些选择都建立在这样的背景上："它会被采用吗？我该怎么服务它？如果你要开源，今天人们能在笔记本上运行什么大小的模型？"所有这些因素都影响你选择训练多大的模型。我认为，只要把模型做得更大、用更多数据训练，它总会变得更好。但一切取决于这些设计节点。

---

### 18.6 Optimal Architectures for Different Use Cases / 不同用例的最优架构

**Question:** You mentioned at the beginning different use cases like agentic coding versus batch processing of data. So what are the most dramatic differences in terms of optimal architectures that you see across different use cases?

**问：** 你一开始提到了不同用例，比如智能代理编程 vs. 批量数据处理。在不同用例之间，最优架构有哪些最显著的区别？

**Dan Fu:** That's a great question. So I think one of the big differences—so when you have these agentic looped workflows, one of the things that matters a lot is that you want to keep your KV Cache as hot as possible. So if you're doing a big batch processing thing where you only see each document once and then you translate it, the KV Cache doesn't necessarily matter as much. If you look at something like the DeepSeek MLA attention, that is a radical compression of the KV Cache compared to what you would have for another model. Or if you have a model that can process its KV Cache in FP8 or FP4, those are pretty big departures in terms of the size of the KV Cache that if you are sensitive to an agentic workflow you would look at. Then of course, the biggest one is like causal attention or non-causal attention. So if you're just doing a big batch processing workflow—like for the longest time, Google was just using BERT models. I think probably still uses BERT models on search. And that's because you don't really need to be generating a bunch of tokens on the other end. So you just do that big bidirectional attention once, you get your vector out, then you stick that in a database, do whatever you will with it. Whereas the chat workflows—there's always going to be this decode portion of it. I think there have been intermediate things like T5 was at some point a choice that people made to do some bidirectional processing, and then also some generation.

**Dan Fu：** 好问题。一个很大的区别是：在智能代理循环工作流中，非常重要的是尽可能让 KV 缓存保持"热"状态。如果你在做大批量处理，每份文档只看一次就做翻译，KV 缓存就不那么重要。看看 DeepSeek 的 MLA 注意力——那是对 KV 缓存的极致压缩。或者有模型能用 FP8 甚至 FP4 来处理 KV 缓存——这对 KV 缓存大小的改变非常大，如果你对智能代理工作流敏感，就会关注这些。当然，最大的区别是因果注意力 vs. 非因果注意力。如果你只做大规模批处理——谷歌很长一段时间只用 BERT 模型做搜索，现在可能还在用——那是因为你不需要在另一端生成一堆标记。你只需要做一次大的双向注意力，得到一个向量，然后放到数据库里随便用。而在聊天工作流中，解码部分始终存在。也有一些中间方案，比如 T5 一度是人们的选择：先做一些双向处理，再做生成。

---

### 18.7 Megakernels and Multi-GPU Communication / Mega 核函数与多 GPU 通信

**Question:** How does Megakernel work when you have multiple GPUs communication in the loop?

**问：** Mega 核函数如何处理多 GPU 之间的通信？

**Dan Fu:** Yeah, great question. So we had some very early preliminary work about this. It turns out you can also fuse the NCCL calls into the Megakernel if you set it up correctly. I think we haven't found a really great killer use case for that yet, where sometimes you're just bound by the latency of the NCCL call itself. So these are also pieces of things that you can fuse. When DeepSeek V4 came out, the DeepSeek V4s released a Megakernel for the mixture of experts inference layer that can run just for that, where they actually did fuse some of those communication. So I think what we are starting to see more of is, as you get to more of these models, you'll have a little Megakernel for a part of the computation, but you won't necessarily have a Megakernel for the whole model, unless of course, you pay the blood, sweat, and tears price and then really, really get the whole thing going.

**Dan Fu：** 好问题。我们有一些非常早期的初步工作。其实如果你设置正确，可以把 NCCL 调用也融合到 Mega 核函数里。我觉得我们还没有找到一个很强的杀手级用例——有时候瓶颈就是 NCCL 调用本身的延迟。但这些也是可以被融合的东西。DeepSeek V4 发布时，他们为混合专家（MoE）推理层做了一个专门的 Mega 核函数，其中确实融合了一些通信操作。所以我觉得我们开始看到的是：随着这些模型越来越多，你会有针对某部分计算的 Mega 核函数，而不一定是整个模型的 Mega 核函数——除非你愿意付出心血和汗水的代价，真正把整个流程做通。

---

OK, I think that's all the time we have. Let's thank Dan again. Thanks so much for having me.

好了，时间到了。再次感谢 Dan。谢谢邀请。

