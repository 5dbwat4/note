---
title: "Lecture 10: Inference"
---


# Lecture 10: Inference / 第十讲：推理（Inference）

---
All right. Let's get started. So last time, Tatsu talked about scaling laws, and we're going to take a little break from that and talk about an inference. So the problem of inference is very simple. You've trained a model, and you're given a prompt, and you want to produce the response usually as accurately and as quickly as you can. So inference turns out to be only one lecture, but it's actually of growing importance. And it shows up in many places. So clearly, once you've trained a model, you don't just sit there. And if you're a researcher, you put a plot in your paper of here's how my model works, but for everyone else, you actually want to use this model. So what does use look like? It could be chatting with an AI assistant or chatbot, it could be doing code completion. These days, agents are very popular, and that requires inference. Batch data processing as well. It's also used for evaluation. For evaluation that requires generation in particular. And it's also used inside training. If you're doing reinforcement learning, you need to have a model, you generate rollouts, and you score them, and you update the weights appropriately. So inference shows up all over the place. And efficiency, as is the theme of this class, really matters more than ever here. And even if you just look at the actual use app of vantage point, training is a one-time cost. It could be very expensive. It is very expensive. But once you're done with it, that's it. But inference is a repeated cost. You kind of incur them every single day. So OpenAI is estimated to produce 8.6 trillion tokens a day. And just for reference, DeepSeek-V4, which came out earlier this year, was trained on 32 trillion tokens. So in less than four days, the number of tokens that OpenAI has to produce, and therefore the compute is at least DeepSeek-V4. And of course, even the frontier models might be trained on more tokens, but still, inference, the number of tokens generated is going to be higher. So that's just some perspective. And moreover, I think the importance of inference has grown in the last year because once upon a time, we thought of language models as primarily as chatbots or assistants, where you put in a prompt, you get back a response, and presumably, the goal of the human is to read the response. But now, as we move more into a genetic world, what it looks like is that a query goes in, and the agent is going to do a bunch of stuff. It's going to think, it's going to reason, it's going to call some tools, it's going to introspect. And at the end of the day, it will produce some output for a human to read. So most of the tokens that the agent produces is actually not for reading. And so you should really think about the number of tokens generated as really the compute spend. And there's no limit. If you have an ambitious enough problem, you're going to need much compute and a lot of tokens. So if you were in the chatbot world, maybe inference after a certain point, it's fast enough, because humans can only read so fast. But for an agent, there's no limit to how much a value you can get out of squeezing more out of inference. So there's a lot of people doing inference on the commercial side. Of course, all the closed API providers have to serve their models, so inference is a big deal for them. And there is also a bunch of providers serving open weight models and providing inference as well. And in the open source community, there's a bunch of packages. So VLM is probably a popular one. Kind of a go-to. SG Lang is another one that's particularly good for agentic workloads, but maybe not as popular yet. And then there's TensorRT from NVIDIA, which is really fast, but it's more narrow. And then Llama CPP, if you want to run inference on CPU, this is a popular package. So hopefully, I've argued that inference is huge. If you can make inference twice as fast or even 10% faster, that is a big deal.

好，我们开始吧。上次Tatsu讲了缩放定律(scaling laws)，今天我们暂时放一放，来讨论推理(inference)。推理的问题非常简单：你已经训练好了一个模型，给定一个提示(prompt)，你希望尽可能准确、尽可能快速地生成响应(response)。推理只占一讲的内容，但它实际上越来越重要，并且出现在很多地方。显然，当你训练好一个模型后，你不会就让它闲置在那里。如果你是研究者，你会在论文里放一张图展示模型的效果；但对其他所有人来说，你实际上是想要使用这个模型。那么"使用"是什么样的呢？可能是与AI助手或聊天机器人对话，可能是做代码补全(code completion)。如今，智能体(agents)非常流行，这需要推理。还有批量数据处理(batch data processing)。推理也用于评估(evaluation)——特别是需要生成的评估。它也被用于训练内部：如果你在做强化学习(reinforcement learning)，你需要有一个模型，生成轨迹(rollouts)，对它们评分，然后相应地更新权重。所以推理无处不在。而效率——正如这门课的主题——在这里比以往任何时候都更重要。即使仅仅从实际应用的角度来看，训练是一次性成本——它可能非常昂贵，确实非常昂贵——但一旦完成，就结束了。但推理是重复成本，你每天都在产生它。据估计，OpenAI每天产生8.6万亿个标记(tokens)。作为参考，今年早些时候发布的DeepSeek-V4是在32万亿个标记上训练的。所以不到四天，OpenAI需要生成的标记数量——因此也是计算量——就至少相当于一个DeepSeek-V4。当然，即使是前沿模型(frontier models)也可能在更多标记上训练，但推理所生成的标记数量仍然会更高。这只是提供一个视角。此外，我认为推理的重要性在过去一年中有所增长，因为曾经我们认为语言模型主要是聊天机器人或助手，你输入提示，得到响应，而人类的目标是阅读这个响应。但现在，随着我们越来越多地进入一个智能体(agentic)的世界，情况变成了：一个查询进去，智能体要做一堆事情——它会思考、推理、调用一些工具、进行内省(introspect)，最后才会产生一些供人类阅读的输出。所以智能体产生的大部分标记实际上并不是供人阅读的。因此，你应该真正把生成的标记数量视为计算开销。而且没有上限——如果你的问题足够宏大，你将需要大量的计算和大量的标记。在聊天机器人世界里，推理达到一定速度后可能就够了，因为人类阅读速度有限。但对于智能体来说，从推理中榨取更多价值是没有上限的。所以有很多人在做商业推理。当然，所有闭源API提供商都需要服务他们的模型，因此推理对他们来说是大事。也有一批提供商服务开放权重模型(open weight models)并提供推理。在开源社区中，有很多软件包。vLLM可能是一个流行的、首选的项目。SGLang是另一个，特别适合智能体工作负载，但可能还没有那么流行。还有NVIDIA的TensorRT，速度非常快，但适用范围较窄。以及LlamaCPP——如果你想在CPU上运行推理，这是一个流行的包。希望我已经论证了推理的重要性——如果你能让推理快两倍，甚至快10%，那都是一件大事。

---

So now, the question is, what does fast mean? So there's a few metrics that capture the notion of fast. And they're going to be applicable in different settings and have different trade offs. So one metric of fast is time to first token or TTFT. This is essentially how long a user waits before any generation happens. So you put in a query into ChatGPT, and some number of milliseconds passes by, and then from the point the first token comes in, that is the time. And this is generally useful for interactive applications because that latency where you're just waiting and doing nothing is-- the longer that is, the worse the user experience, and as soon as tokens come in, it doesn't maybe have to be that fast, because if you're going to read it anyway, you can't read that fast. So the second metric is latency. And this is from the standpoint of an individual user. How fast are tokens appearing for one query? This is also important for interactive applications. So basically, this is how fast the tokens are kind of streaming through. And then the second related concept is throughput, measuring tokens per second, this is how fast tokens are appearing for many queries. So latency or one latency and throughput are clearly very related. It's very kind of aligned-- in general, many interventions will make latency and throughput better. But as we'll see later, there's actually a trade off here. And throughput is useful for if you're doing a bunch of batch processing. You have a petabyte of data, and you want to process it with a language model. You just want that job to get done. It doesn't matter if one query is coming in faster, sooner, or later.

那么问题来了，"快"意味着什么？有几个指标可以衡量"快"的概念，它们适用于不同的场景，并有不同的权衡。一个指标是**首token时间(time to first token, TTFT)**——本质上就是用户在生成开始之前等待的时间。你在ChatGPT中输入一个查询，经过若干毫秒，从第一个标记出现的那一刻开始计时。这通常对交互式应用很重要，因为你在那里干等着，时间越长，用户体验越差；而一旦标记开始出现，速度不一定需要那么快，因为反正你要阅读它，你也读不了那么快。第二个指标是**延迟(latency)**——从单个用户的角度看，一个查询的标记出现速度有多快？这对交互式应用也很重要，基本上就是标记流出的速度。第二个相关概念是**吞吐量(throughput)**，以每秒标记数衡量，即多个查询的标记出现速度。延迟和吞吐量显然密切相关，通常很多改进措施会同时改善两者。但正如我们后面会看到的，这里实际上存在权衡。吞吐量对于批量处理很有用——你有一PB的数据想要用语言模型处理，你只希望工作完成，不在乎单个查询是快是慢。

---

OK. So what determines the efficiency by either any of these metrics of inference. So the high level bit is as follows. And this is-- maybe one high level bit to remember from the lecture is that when you're doing training, you see all the tokens at once, because in supervised fine-tuning, you see all the tokens, and you can parallelize over the sequence. Remember, think about in the transformer, the calculation for attention, MLP, the sequence is just a dimension. So it's a big tensor that gets multiplied. And so you, essentially, process all the tokens at once. In inference, you can't do that. You have to generate because of the autoregressive nature of inference. Tokens sequentially. One at a time. So this is the fundamental problem of why inference is a very different workload than training, because you can't parallelize across the sequence dimension. And therefore, as we'll see later, it's going to be harder to have high arithmetic intensity or fully utilize the compute.

那么，是什么决定了推理在各项指标上的效率呢？高层次的核心如下——这也许是本讲需要记住的一个要点：在训练时，你一次性看到所有标记，因为在有监督微调(supervised fine-tuning)中，你看到所有标记，并且可以在序列维度上并行化。回想一下，在Transformer中，注意力(attention)和MLP的计算中，序列只是一个维度，它是一个大的张量(tensor)参与乘法运算。所以本质上，你一次性处理所有标记。而在推理中，你不能这样做——由于推理的自回归(autoregressive)性质，你必须逐个、依次生成标记。这就是推理成为与训练截然不同的工作负载的根本原因——你无法在序列维度上并行化。因此，正如我们后面会看到的，实现高算术强度(arithmetic intensity)或充分利用计算资源会更加困难。

---

OK. All right. So let's go on. So first, I'm going to-- just maybe a preview of what's in this lecture. First, I'm going to do some math to understand the arithmetic intensity and throughput and latency, how to think about that for a transformer. And then I'm going to talk about various techniques to reduce the cost by making the kv cache smaller, quantizing model, pruning, and then finally, I'll talk about speculative decoding, and then some kind of practical concerns.

好的，我们继续。首先，我稍微预览一下本节课的内容。首先，我会做一些数学推导来理解算术强度、吞吐量和延迟，以及如何对Transformer进行思考。然后我会讨论各种通过减小KV缓存(KV cache)、量化模型(quantizing)、剪枝(pruning)来降低成本的技术。最后我会讲推测解码(speculative decoding)和一些实践问题。

---

All right. So this is going to be a bit of a review, mostly kind of swapping in, making sure we're on the same page with respect to notation. Much of this lecture is based on the scaling book from Google on transformers and inference. So I do recommend that people go check it out. It's a very nicely written. And some of the figures are generously lifted from that book.

好，这部分会有些回顾，主要是确保我们在符号表示上保持一致。本节课的许多内容基于Google关于Transformer和推理的缩放书籍(scaling book)。我强烈建议大家去看看，那本书写得非常好。其中的一些图表也慷慨地引自该书。

---

OK. So just to establish a bit of notation to understand this diagram. So we're going to use symbols. Think about it in ienops to denote dimensions, but also they're kind of length. So B is going to be the batch dimension and also the number of sequences. T is going to be the sequence dimension, which is also the number of tokens. D is the model dimension, H is the dimension. So if I'm going to write this, this is taking a product between a tensor with dimensions B, T, and D, and another matrix of D and H, and I produce BTH. So what is going on here is that there are some dimensions marked red, which are going to be contracting. These dimensions appear in both the operands and disappear from the results. And then there's going to be other regular dimensions in black that appear only in one operand and stay in the result. So this is the general form. Another case is if you have blue dimensions, that means they're attaching dimensions, and they appear in both, but stay in the result. They do not get contracted or reduced.

好，我们先建立一些符号来理解这个图。我们将使用符号来表示维度，同时也是长度。B表示批次维度(batch dimension)，也是序列数。T表示序列维度(sequence dimension)，也是标记数。D表示模型维度(model dimension)，H表示头维度(head dimension)。如果我写这个，这是一个维度为B、T、D的张量与另一个维度为D、H的矩阵的乘积，得到BTH。这里发生的事情是：一些标记为红色的维度将是收缩维度(contracting dimensions)——这些维度出现在两个操作数中，并从结果中消失。其他黑色的常规维度只出现在一个操作数中，并保留在结果中。这是通用形式。另一种情况是蓝色维度，表示连接维度(attaching dimensions)，它们出现在两个操作数中，但保留在结果中，不会被收缩或约简。

---

OK. So the interpretation here, as we'll see later, is that we have this tensor for every sequence and token position. You have a vector and you want to multiply that by a matrix. And then here, you're basically taking a bunch of dot products between two tensors.

好的，这里的含义——我们后面会看到——是对于每个序列和标记位置，我们有一个张量。你有一个向量，想乘以一个矩阵。然后这里，你基本上是在两个张量之间做一系列点积(dot products)。

---

OK. So with that in mind, this in all its full glory, is the description of a transformer block. So it looks a little bit like a circuit diagram. There's a lot of details here, but I actually find this probably the most crisp definition of what a transformer is. You see a lot of description of transformer, and frankly, a lot of them are-- it's hard to understand what is exactly happening. This one basically tells you exactly the shapes of the tensors and allows you to reason about the dependency. So for transformer block, you take the X, which is the activations of one layer, you feed it through a tension, and then you feed it through MLP. And just as a kind of a quick refresher, you projected using a query matrix, a key matrix and a value matrix, you'll see here that we have N, which is the number of heads, and H is the dimension of each head. So the query matrix is batch times sequence times number of heads times the head dimension, and K and V, instead of having N, we have K, which we'll see later, which we have a potentially smaller number key value heads. And then this is the attention operation, where notice that there's batching dimensions. So B appears in both. And we're contracting over the head dimension. And we'll come back to why this B, B in both, makes inference hard. Why attention is kind of a bottleneck there. So just hold on to that thought. And the MLP is very simple and straightforward. You just do some math models. This is the gating matrix. This is the upper direction and a down projection.

好的，基于此，这个图就是Transformer块的完整描述。它看起来有点像电路图，有很多细节，但我发现这可能是对Transformer最清晰的定义。你见过很多Transformer的描述，坦白说，很多都让人难以理解到底发生了什么。而这个图精确地告诉你了张量的形状，并让你能够推理依赖关系。对于一个Transformer块，你取X——某一层的激活值(activations)——先经过注意力(attention)，再经过MLP。快速回顾一下：你用查询矩阵(query matrix)、键矩阵(key matrix)和值矩阵(value matrix)做投影。这里我们看到N是头数(heads)，H是每个头的维度。所以查询矩阵是批次乘以序列乘以头数乘以头维度。而K和V——我们不用N，而是用K，后面会看到——我们可能有更少数量的键值头(key value heads)。然后是注意力操作，注意这里有批次维度，B同时出现在两个操作数中，我们在头维度上做收缩。我们后面会回到为什么B出现在两边会让推理变得困难，以及为什么注意力在那里成了瓶颈。先记住这个想法。MLP则非常简单直接，你做一些矩阵乘法，这里有门控矩阵(gating matrix)、上投影(upper projection)和下投影(down projection)。

---

So thank you guys. I have implemented this. So I don't want to belabor it, but just to swap in the notation. By convention, we're going to assume that in the MLP, the MLP up projects the D dimensional, model dimension into four times that. So F is always-- think about it as 4D whenever you see F. And then the model dimension gets split across the N heads. So the model dimension is always equal to number of heads times the head dimension. And then the number of heads get split, in the case of group query attention, into the number of groups and the number of heads per group. And finally, we have two variables, S and T, which both represents the sequence dimension. And the difference is that S is going to represent the number of input tokens, and T is going to represent the number of output tokens. So in training time, these two are the same, because we're predicting all the same inputs as outputs. And inference time, T is going to be 1, and S is going to be the input.

谢谢大家。我已经实现了这个，所以不想过多赘述，只是统一一下符号。按照惯例，我们假设在MLP中，MLP将D维的模型维度上投影为其四倍。所以F——当你看到F时，就把它当作4D。然后模型维度在N个头上分割，所以模型维度总是等于头数乘以头维度。在分组查询注意力(group query attention)的情况下，头数被分割为组数和每组头数。最后，我们有两个变量S和T，它们都代表序列维度。区别在于：S代表输入标记数，T代表输出标记数。在训练时，这两者是相同的，因为我们预测的输入和输出是相同的。在推理时，T等于1，S是输入。

---

OK. So another review for arithmetic intensity. So I talked about this in the second lecture. So just as a warm up. Suppose I'm multiplying two matrices; a B by D matrix and a D by F matrix. So intuition. B is the batch dimension, D is the hidden dimension or the model dimension, and F is the projection dimension in the MLP. So remember, what are the arithmetic intensity? I have to count flops, and I have to count the amount of memory moved. So we can do this as follows. So what do you have to do to multiply these matrices? Now, remember, the systems, lectures, you have to read X from HBM. And if you're storing everything in bf16, which is the case for inference, we're going to have 2 times B times D, you're going to read W. That's going to be another 2 times D times F. You're going to do the matmul. So that's number of flops is 2 times B times D times F And then you're going to write it back. OK? So every time you read and write, it's basically the number of entries. It's kind of a quadratic-like term, and matmuls are qubit. And remember, this is going to be important because that's how you're going to get high arithmetic intensity. So total number of flops is the cubic, and then the bytes transferred is the sum of the reads and writes.

好，再来复习一下算术强度(arithmetic intensity)。我在第二讲中讲过这个。作为热身，假设我在做两个矩阵的乘法：一个B乘D的矩阵和一个D乘F的矩阵。直观上，B是批次维度，D是隐藏维度或模型维度，F是MLP中的投影维度。那么算术强度是什么？我需要计算FLOPs，也需要计算移动的内存量。我们可以这样做：要乘这些矩阵，你需要从HBM中读取X。如果你用bf16存储所有东西（推理时就是这种情况），那就是2乘以B乘以D；你还要读取W，又是2乘以D乘以F。然后做矩阵乘法(matmul)，FLOPs数是2乘以B乘以D乘以F。最后把结果写回去。每次读写基本上就是元素的数量，这是一个类二次项，而矩阵乘法是三次的。记住，这很重要，因为这就是你获得高算术强度的方式。所以总FLOPs是三次的，而传输的字节数(read bytes)是读写的总和。

---

So remember, arithmetic intensity is how much compute we do per byte transfer. And we want this to be high. So the intensity is going to be equal to flops over bytes transfer. And I'm representing all these things symbolically, because it will be easier to see and work with rather than numbers. One just simplification we can make is that suppose that the batch dimension here is much less than D and F, then we can simplify this. So in particular, what this is doing is saying D equals C times D and F equals C times B and let C goes to infinity, so both D and F are really large and B is smaller, and this just reduces to the intensity of B. So the upshot of that is that remember when we did arithmetic intensity for matmul, it was something like N/3. And this is the kind of analog, where instead of just having square matrices, we have non-square matrices.

记住，算术强度是每传输一个字节我们做多少计算。我们希望这个值很高。所以算术强度等于FLOPs除以传输字节数。我用符号表示所有这些量，因为用符号比用数字更容易观察和操作。我们可以做一个简化：假设批次维度远小于D和F，那么我们可以简化这个表达式。具体来说，这相当于说D等于C乘以D，F等于C乘以B，让C趋于无穷，这样D和F都非常大而B较小，表达式就简化为强度等于B。结果是——记得我们之前算矩阵乘法的算术强度时是N/3之类，现在是类似的，只不过我们处理的是非方形矩阵而非方形矩阵。

---

OK. So just to compare, so the accelerator intensity of a hardware is you look at the flops per second in the spec sheet, you look at how much memory bandwidth, how fast memory gets moved between HBM, you divide, and that is the accelerated intensity. And now, you compare your computations intensity with your accelerator intensity. And if it's greater then your compute bound, which is good, if you're less, then you're memory bound, and that's bad. So in this case, for H100, for this particular matmul operation, you're compute bound if the batch size is greater than 295. So here's an extreme case. So suppose you just have one example. What happens is you have one example, then your arithmetic intensity is going to be one. And this is going to be memory bound. And you can see what's going on here. You're reading this DF matrix, but B is only one. So you're effectively doing only 2 times D times F flops. And this is basically the workload that you'll see in inference. You don't get these full matrices, you get these very thin matrices or tensors. OK. Let me stop there in case there's any questions.

好的，做个比较。硬件的加速器强度(accelerator intensity)是这样计算的：看规格书中的每秒FLOPs，看内存带宽(memory bandwidth)有多快、HBM之间移动数据有多快，两者相除就是加速器强度。然后你把你的计算强度与加速器强度比较。如果大于，你就是**计算受限(compute bound)**——这很好；如果小于，你就是**内存受限(memory bound)**——这很糟糕。在这个例子中，对于H100上的这个特定矩阵乘法操作，如果批次大小大于295，你就是计算受限的。这里有一个极端情况：假设你只有一个样本，那么你的算术强度就是1，这会变成内存受限。你可以看到这里发生了什么：你在读取这个DF矩阵，但B只有1，所以你实际上只做了2乘以D乘以F次FLOPs。这基本上就是你在推理中会遇到的工作负载——你得不到这些完整的矩阵，你得到的是非常"瘦"的矩阵或张量。好，我先停在这里，看看有没有问题。

---

Yeah. In the transformer slide, I just want to confirm [INAUDIBLE]. You said, across [INAUDIBLE] can search across [INAUDIBLE]? Yeah, should that be across tables instead of cubes? Let's see. So the number of groups here is-- wait, I'm just making sure. So K is the number key value heads. And so you have g per KV head. My understanding is [INAUDIBLE] each key path will have one [INAUDIBLE] correspond to it. And [INAUDIBLE] then g is the number of [INAUDIBLE] p. That means we have k. That's my question. Yeah, OK. Yeah, I think you're right. So k should be the number of groups, and g should be the number of the heads per one of those groups. Yes. Yeah, OK. Thanks for that. I'll fix that later.

在Transformer那张幻灯片上，我想确认一下。你说，跨……应该是跨表(table)而不是cubes？让我看看。这里的组数——等一下，我确认一下。所以K是键值头(key value heads)的数量。那么每个KV头有g个。我的理解是……每个键路径(key path)会有一个……对应它。那么g就是……p的数量。这意味着我们有k。这是我的问题。好，OK，我想你是对的。所以k应该是组数，g应该是每组中的头数。是的。好，谢谢。我后面会修正。

---

OK. So let's talk a little bit more about the arithmetic intensity of inference. So here's how to think about what's happening in inference. Let's say you just do it naively. So here is a prompt never going to give you. I'm going to the transformer. And the transformer does generates keys and values and activations. And at the end of the day, it generates logits over the output vocabulary. And you sample a token, and that token gets concatenated with the prompt, and then you just do this again. You generate never. You attach that to the prompt and so on and so forth. So this is the most naive thing. If you have a black box that takes a sequence and outputs a distribution over tokens, which is exactly what a transformer does, you can just apply this repeatedly.

好，我们来多讨论一下推理的算术强度。这样思考推理中发生了什么：假设你简单地做。这里是一个提示(prompt)，你把它送入Transformer。Transformer生成键、值和激活值。最终，它在输出词汇表上生成logits。你采样一个标记，这个标记与提示拼接，然后重复这个过程：生成下一个，拼接到提示，如此往复。这是最朴素的做法。如果你有一个黑盒，它接受序列并输出标记上的分布——这正是Transformer所做的——你可以反复应用它。

---

OK, so this works, but this is really bad because each time you generate one token, you actually take order T squared time where T is the number of tokens that you've generated so far. So generate T tokens is actually T cubed because the attention is already T squared, and you have to do that once for every token. So this is pretty bad, but the observation is that you don't actually have to do this. A lot of the work can actually be shared across prefixes. So for example, if you're over generating network versus you're generating up, you're actually computing a lot of the same key values for never going to give. So these tokens, they shouldn't change, OK? And this is because it's a causal transformer. If it was bidirectional, then if you attach a token, then everything changes. But if it's causal, then the activations here don't change based on any tokens you append.

这样是可行的，但非常糟糕，因为每生成一个标记，你实际上需要大约T平方的时间，其中T是到目前为止生成的标记数。所以生成T个标记实际上是T的三次方——因为注意力本身已经是T平方，而你要为每个标记都做一次。这非常糟糕，但观察发现你实际上不需要这样做。很多工作可以在前缀(prefixes)之间共享。例如，如果你在生成……实际上你在为"never going to give"计算大量相同的键值(key values)。这些标记不应该改变，对吧？这是因为它是因果Transformer(causal transformer)。如果是双向的(bidirectional)，那么你附加一个标记后所有东西都会改变。但如果是因果的，那么这里的激活值不会因为你附加的任何标记而改变。

---

So with that observation, the first obvious thing is to store a KV cache in HPM, so that, between successive token generations, you can just reuse the KV cache. So that means when you are trying to generate gonna, you don't actually have to compute all the keys and activations of these previous tokens. So this is what it looks like with a KV cache. So there's going to be two stages pre-fill. So you get the prompt, and you populate the KV cache, which is the set key and value pairs that the transformer computes, and then you generate the logit-- just the same computation as we did before. And now you have the KV cache here and then this distribution which you sample at a token. And now you feed that through the transformer, which uses this cache and then produces both the distribution of the next tokens, but a new KB, which is basically activations corresponding to the token up. And then this gets fed in. So now you have the command to KV cache. You have this logits you sample, and then that feeds to the transformer. You output the distribution over next tokens as well as the new token which you add to the KB cache and so on and so forth.

基于这个观察，第一个显而易见的做法是在HBM中存储一个**KV缓存(KV cache)**，这样在连续生成标记之间，你可以直接复用KV缓存。这意味着当你试图生成"gonna"时，你实际上不需要计算之前所有标记的键和激活值。这就是使用KV缓存的样子。会有两个阶段：**预填充(prefill)**。你拿到提示，填充KV缓存——即Transformer计算出的键值对集合——然后生成logit，和之前做同样的计算。现在你有KV缓存和这个分布，从中采样一个标记。然后你把这个标记送入Transformer，它使用缓存，既产生下一个标记的分布，也产生新的KV（即对应于这个标记的激活值）。然后这个被送入。现在你有累积的KV缓存，你采样logits，再送入Transformer，输出下一个标记的分布以及新的标记，将其添加到KV缓存，如此往复。

---

So the KV cache formula is for every sequence-- so there's B of them. For every token, there's S of them. And for every layer and every head, you store H dimensional vector. And just to reiterate for inference, there's prefill. You given a prompt. You encode the prompt into these vectors. And this is parallelizable just like in training because you see the entire prompt. You can compute the KV cache. And then in generation, you generate the new response tokens sequentially. But at least you don't have to pay for generating the KV cache of the tokens that you already looked at. So is everyone comfortable with the KV cache? Any questions about this?

所以KV缓存的公式是：对每个序列（共B个），对每个标记（共S个），对每一层和每个头，存储一个H维向量。再强调一下推理的过程：有预填充(prefill)阶段——你给定一个提示，将提示编码为这些向量。这就像训练一样是可并行的，因为你看到了整个提示，可以计算KV缓存。然后在生成(generation)阶段，你顺序生成新的响应标记。但至少你不需要为你已经看过的标记生成KV缓存。大家对KV缓存都理解了吗？有什么问题吗？

---

All right, so let's try to figure out the FLOPs and memory I/O for both MLP and attention layers. So remember S is the number of tokens we're kind of conditioning on, and T is the number of tokens we're generating. So we're going to do this abstractly. And then later, we'll specify to the prefill where T equals S, and generation T equals 1. So for the MLP layers-- and through all of this, I'm just going to look at the MAmmoTH because the MAmmoTH are the thing that actually require a lot of work. Everything else can is not that many FLOPs and can be potentially fused into the MAmmoTH too.

好，我们来计算一下MLP和注意力层的FLOPs和内存I/O。记住S是我们条件 conditioning 的标记数，T是我们正在生成的标记数。我们先抽象地做，然后具体到预填充（T等于S）和生成（T等于1）。对于MLP层——在整个过程中，我只看矩阵乘法(matmul)，因为矩阵乘法才是真正需要大量计算的部分。其他部分FLOPs不多，也可以被融合到矩阵乘法中。

---

OK. So let's do this calculation. So it's the same as the matrix calculations. I'm not going to maybe belabored step through every single detail here, but just the form is you read X from high bandwidth memory. You read all the parameters. You compute the upper projection, and then you write it to HBM. You compute the gate, and you write HBM, and then you compute basically the down projection of that, and you write it to HBM. So the number of flops depends on B and T and D and F. So batch size, sequence length, model dimension, and the feedforward dimension, MLP dimension. And the bytes transferred is this expression. So now you can compute the arithmetic intensity which, again, is FLOPs divided by bytes transferred. So this is some expression. We're going to assume, that just like before, B times T is much smaller than D and F. And with that, then we see that intensity is B times T. So this is analogous to just the MAmmoTH case. There's more matrices and there's more dimensions, but fundamentally it's the same thing. And that makes sense. An MLP is basically a big MAmmoTH. And it also makes sense because the batch dimension and the sequence length dimension are-- everything is independent. And for the MLP, they don't interact. Attention is different story. And so B times T. So as long as you have-- in the pre-fill, if you make B times T large enough-- large batches, long sequences-- you'll be fine.

好，我们来做这个计算。这与矩阵计算相同，我不会一步步详细展开，但形式是：从高带宽内存(HBM)中读取X，读取所有参数，计算上投影，写入HBM；计算门控，写入HBM；然后计算下投影，写入HBM。所以FLOPs数取决于B、T、D和F——即批次大小(batch size)、序列长度(sequence length)、模型维度(model dimension)和前馈维度(MLP dimension)。传输的字节数就是这个表达式。现在你可以计算算术强度——仍然是FLOPs除以传输字节数。这是一个表达式。我们假设，和之前一样，B乘以T远小于D和F。那么我们看到强度是B乘以T。这与矩阵乘法的情形类似。虽然有更多的矩阵和更多的维度，但本质上是一样的。这很合理——MLP基本上就是一个大的矩阵乘法。这也合理，因为批次维度和序列长度维度——所有东西都是独立的，对于MLP它们不互相影响。注意力则是另一回事。所以是B乘以T。只要在预填充中你让B乘以T足够大——大批次、长序列——就没问题。

---

Now, let's look at generation. So remember, generation, there's two problems here. One is that generation T equals 1. You're only generating one token at a time. And so that means your arithmetic intensity is going to be B, but B in generation is the number of concurrent requests. And so if you're in a batch setting, you can control that. But if you're, let's say, serving a chatbot, it's the number of concurrent requests is essentially how many users, concurrent users there are? Which can be high. It be low. So it's a bit unpredictable. It can be changing over time. So that's something we're going to address when we talk about continuous batching. But overall, this is not bad because as long as you have large batches, the sequence length isn't going to really help you. But if you have large batches, you should be good.

现在来看生成。记住，生成有两个问题。一个是生成时T等于1——你一次只生成一个标记。这意味着你的算术强度将是B，但生成时的B是并发请求数。如果你在批处理场景中，你可以控制这个值。但如果你是服务一个聊天机器人，并发请求数本质上是用户数——它可能高也可能低，有点不可预测，并且会随时间变化。这是我们在讨论**连续批处理(continuous batching)**时会处理的问题。但总体来说，这还不算太糟，因为只要你有大批次，序列长度不会真正帮你忙，但如果你有大批次，就应该没问题。

---

So now let's look at the attention layer. So again, S is in the previous tokens already generated. T is the number of tokens you want to generate logits for. So in attention, you read the QKV matrices from HPM. You compute the attention. You compute the softmax which doesn't really matter, and compute the value matrix, and then you write the result to HBM. So the FLOPs is B times S times T times D, and the bytes transferred is this expression. Everything's is a MAmmoTH, right? So this should be always one degree higher of a polynomial than the bytes transferred because it's a MAmmoTH. The only question is, what is that factor look like? So that factor for attention is S times T over S plus T.

现在来看注意力层。同样，S是已经生成的之前标记数，T是你想为其生成logits的标记数。在注意力中，你从HBM中读取QKV矩阵，计算注意力，计算softmax（这不太重要），计算值矩阵，然后将结果写入HBM。所以FLOPs是B乘以S乘以T乘以D，传输的字节数就是这个表达式。每个运算都是矩阵乘法，对吧？所以FLOPs的多项式次数应该总是比传输字节数高一次，因为它是矩阵乘法。唯一的问题是那个因子是什么样的。对于注意力，那个因子是S乘以T除以S加T。

---

So let's look at the prefill. So prefill, what this is saying is that the prefill intensity is S over 2 when T equals S. So this is good, right? Because as long as you have long sequence lengths for attention, you're going to maintain high arithmetic intensity. Notice that the batching dimension doesn't happen here. I'll explain a bit why later. But for generation, this is bad news. So the generated nation intensity is S over S plus 1, and that's less than 1, or even let's just call it 1. And aromatic intensity, remember 1 is bad. We want it to be something like 295 for H100 to be to saturate the compute. And so this is really the bottleneck.

我们来看预填充。预填充时的算术强度是——当T等于S时——S除以2。这不错，对吧？因为只要你有足够长的序列长度，注意力就能维持高算术强度。注意批次维度在这里没有出现——我稍后会解释为什么。但对于生成来说，这是个坏消息。生成时的算术强度是S除以S加1，小于1，我们就叫它1吧。算术强度为1是很糟糕的——我们希望它在H100上达到295左右才能饱和计算。所以这真的是瓶颈。

---

So we did all this analysis for MLP attention, prefilled generation, and we've found this to be a bottleneck. So let's try to contemplate why this is a bottleneck. So unlike MLPs-- so MLP is for generation is actually OK as long as your sequence is-- sorry, your batch is large enough. So the problem with this ML attention is that-- let's look at MLPs. Every sequence hits the same MLP weights. So these don't depend on B. Whereas, in attention layer, each sequence has its own KV cache. So these all depend on MLP. And so you can think about this as what's going on here is that in the MLP case, having B being big actually is helpful because you get to load these MLP weights once. And you can use it for all your sequences. That's how you get high arithmetic intensity because you use it-- simplifying a bit, you load it once. You do all your batch processing, and then that is good. Whereas, in attention, all these depend on B. So increasing B doesn't help. It's like for every sequence, you're basically doing a MAmmoTH. So they're all independent. So doing more MAmmoTHs isn't helpful. Just if you remember in the very beginning, I showed you this example. This also has pretty bad arithmetic intensity. It's not a MAmmoTH because we're essentially batching by a coordinate. And this is essentially basically the same as doing a dot product, which has horrible arithmetic intensity. And remember, this is in the attention. This blue B is the cause of why the attention is arithmetic intensity doesn't scale with B, and why that is a bottleneck.

我们对MLP和注意力的预填充和生成做了所有这些分析，发现这是一个瓶颈。让我们思考一下为什么这是瓶颈。与MLP不同——MLP在生成时其实还好，只要你的序列——抱歉，只要你的批次足够大。所以注意力的问题是——我们来看MLP：每个序列都使用相同的MLP权重，这些不依赖于B。而在注意力层中，每个序列都有自己的KV缓存，这些都依赖于……所以你可以这样理解：在MLP的情况下，B很大实际上是有帮助的，因为你只需要加载一次MLP权重，就可以用于所有序列。这就是你获得高算术强度的方式——简化一下，你加载一次，做所有批处理，这就很好。而在注意力中，所有这些都依赖于B，所以增加B没有帮助。对于每个序列，你基本上都在做一个矩阵乘法，它们都是独立的。所以做更多独立的矩阵乘法没有帮助。如果你还记得在最开始，我给你看的这个例子——它的算术强度也很差。它不是矩阵乘法，因为我们本质上是在按坐标做批处理。这基本上等同于做点积(dot product)，其算术强度非常糟糕。记住，这就在注意力中。这个蓝色的B就是为什么注意力的算术强度不随B扩展，以及为什么这是一个瓶颈的原因。

---

So just to summarize here. So prefill is compute-bound. Generation is memory-bound. So if you look at the MLP intensity for prefill, it's B times S, great. Prefill for attention, intensity S over 2-- not as good, but workable. Generation MLP intensity, also workable, requires long concurrent requests. But it is really the generation attention intensity which is a fundamental bottleneck, and that's it. If you're sticking with a transformer, you can't really improve this. OK. Pause there for questions.

总结一下：预填充是计算受限的，生成是内存受限的。预填充的MLP强度是B乘以S——很好；预填充的注意力强度是S除以2——没那么好，但可行；生成的MLP强度也可行，但需要长并发请求。但真正的基础瓶颈是生成的注意力强度。如果你坚持使用Transformer，你无法真正改善这一点。好，这里暂停，看看有没有问题。

---

So now whenever you hear people say, oh, inference is memory bound, you know why.

所以现在每当你听到人们说"推理是内存受限的"，你就知道为什么了。

---

OK. So let's now use these intuitions and calculations to think about our inference metrics throughput and latency and also TFRT. All right. So inference is memory bound. Now the main-- I mean, in some ways this simplifies a lot of things because when we think about how long things take, you just look at how much memory needs to be transferred, OK? Because assuming you overlap communication and computation, the bottleneck is going to be just the amount of memory that you have to deal with. So in some ways, it's nice because it's simpler. But in other ways, it's frustrating that your accelerators are sitting there not doing anything.

好，现在让我们用这些直觉和计算来思考我们的推理指标——吞吐量、延迟和TTFT。推理是内存受限的。这在某些方面简化了很多事情，因为当我们考虑事情需要多长时间时，你只需要看需要传输多少内存。因为假设你重叠了通信和计算，瓶颈将只是你需要处理的内存量。所以在某些方面这很好，因为更简单了。但在其他方面，这令人沮丧——你的加速器闲置在那里什么都不做。

---

So let's walk through an example. So for Llama 2.13B on an H100. So what is the latency and the throughput? So remember Llama 2.13B has a particular shape. So this is a sequence length, the model dimension, feedforward dimension, number of query, number key value heads. There's no GQA here. So the N equals k, head dimension, number of layers of vocab size, and the memory bandwidth for H100. So now, using this config, let's compute the transformer performance statistics, OK? So these are our inputs here. And just the statistics I'm going to compute are going to be number of parameters, the memory, usage latency, and throughput.

让我们看一个例子：H100上的Llama 2 13B。延迟和吞吐量是多少？记得Llama 2 13B有特定的形状：序列长度、模型维度、前馈维度、查询头数、键值头数。这里没有GQA，所以N等于k。还有头维度、层数、词汇表大小，以及H100的内存带宽。现在，使用这个配置，我们来计算Transformer的性能统计数据。这些是我们的输入。我要计算的统计量是：参数量(parameters)、内存使用量(memory usage)、延迟(latency)和吞吐量(throughput)。

---

So first of all, what takes memory? So the parameters take memory. So we compute the number of parameters. And so you look at the embeddings, the MLP layers, the projections of the KQV. At the end of the day, you get some number of parameters. Assuming that we're doing a bf16, which is always the case for inference, then parameters take up this many bytes. Also in memory is the KV cache. And the KV cache is the number of tokens in your sequence times the number of heads and the KV heads times the head dimension times the number of layers. You have one for the key and one for the value, and then you have multiple two for bf16. So that's the size of the KV cache. And the total memory usage is-- this is for each sequence you have B sequences. So that's B times that plus the parameter size. And that's the amount of memory you need.

首先，什么占用了内存？参数占用内存。我们计算参数量。你看看嵌入层(embeddings)、MLP层、KQV的投影——最终得到一些参数数量。假设我们使用bf16（推理时总是如此），那么参数占用这么多字节。内存中还有KV缓存。KV缓存是序列中的标记数乘以头数和KV头数乘以头维度乘以层数。键有一个，值有一个，再乘以2（bf16）。这就是KV缓存的大小。总内存使用量是——每个序列你有B个序列——所以是B乘以那个加上参数大小。这就是你所需的内存量。

---

And now, what's the latency? The latency is determined by the memory I/O, OK? Because inference is memory-bound, most assuming you overlap communication and compute. All the memory, it's going to be on shuffling parameters back and forth between HPM and SRAM. So that's how long it takes to move memory around. Throughput is the inverse of latency, but we're generating B tokens in parallel. So this is tokens per second. This is seconds per token. This is tokens per second, as well as having an additional B because you're processing a batch of B.

那么延迟是多少？延迟由内存I/O决定，因为推理是内存受限的——假设你重叠了通信和计算。所有内存开销都花在HBM和SRAM之间来回搬运参数上。这就是移动内存所需的时间。吞吐量是延迟的倒数，但我们是并行生成B个标记。所以这是每秒标记数，这是每标记秒数，这是每秒标记数，再加上额外的B，因为你正在处理一个批次B。

---

So now, let's compute for this config what are these actual values? So num parameters is 13 billion. So a good sanity check-- that is advertised as a 13 billion parameter model. Memory is this term, which is about 838 million times B. So it's basically a linear function of B plus some other term. So this is a KV cache which grows as B. This is the parameters, which is double the number of params. Now, latency is just this scale by the memory bandwidth, so it has the same form as the memory. And throughput is B over that.

现在，让我们计算这个配置的实际值。参数量是130亿——一个很好的合理性检查，它确实被标称为130亿参数模型。内存是这个项，大约是8.38亿乘以B，所以基本上是B的线性函数加上一些其他项。这是KV缓存，它随B增长。这是参数，是参数数量的两倍。延迟就是用内存带宽缩放这个值，所以它的形式与内存相同。吞吐量是B除以那个。

---

So notice that latency, as you increase B, grows because the KV cache grows. And in order to process stuff, you have to copy the KV cache back and forth. And now, throughput is more interesting because, as you increase B, throughput does improve but up to a limit. Throughput improves because now you're amortizing the cost over a larger batch. But also, the speed at which you're processing this obviously is also increasing over time. So this asymptotes. It's not going to-- throughput can't possibly go to infinity.

注意，随着你增加B，延迟会增加，因为KV缓存增长。为了处理数据，你必须来回复制KV缓存。而吞吐量更有趣——随着B增加，吞吐量确实会提升，但有一个上限。吞吐量提升是因为你现在在更大的批次上分摊成本。但处理速度显然也在随时间增加，所以它会趋近一个渐近线。吞吐量不可能达到无穷大。

---

Any questions about this so far?

到目前为止有什么问题吗？

---

So basically, you just have to remember latency is a linear function in B. This is where the constant is the size of KV cache, and then this is the number of parameters. And then throughput is some proportional to B over B plus something.

所以基本上，你只需要记住延迟是B的线性函数，其中常数是KV缓存的大小，然后这是参数量。吞吐量则正比于B除以B加某数。

---

So now, let's instantiate this for a bunch of situations, OK? So if you have batch size 1, so this is what you would get. You get a latency of 0.008 seconds per token. And the throughput is 124 tokens per second. So what happens if you increase the batch size, you'll see that the latency goes up, but the throughput also goes up. So latency gets worse, but the throughput improves. So this is an interesting thing because we think about, oh, we just want to make it go fast. But fast actually has two meanings here, which actually, depending on which one you care about, is completely opposite. If you want to tune your batch size, that's going to really determine if you want latency or throughput. And what happens if you increase-- let's say, increase-- we really want high throughput because we're processing lots of documents. Let's increase the batch size even more, OK? So the latency gets even worse. I mean, yeah, it gets worse. Throughput gets even better. But the main problem here is that your memory, you run out of memory because the memory, for storing this KV cache, is going to exceed your H100 memory. And if you have B200s, you can increase the batch size more, but eventually you hit some of limit. So there's limitations to how much you can increase your throughput. You'll never get to the asymptote because you'll hit the memory. And also, your throughput is getting-- your gains are kind of diminishing as well.

现在，让我们在各种情况下实例化这个。如果批次大小为1，你会得到延迟0.008秒/标记，吞吐量124标记/秒。如果你增加批次大小，你会发现延迟上升了，但吞吐量也上升了。所以延迟变差，但吞吐量改善。这很有趣，因为我们想"让它变快"，但"快"在这里实际上有两个含义，取决于你关心哪个，它们是截然相反的。如果你调整批次大小，这实际上决定了你是想要低延迟还是高吞吐量。如果我们真的想要高吞吐量（因为我们处理大量文档），我们再增大批次大小——延迟变得更差，吞吐量变得更好。但主要问题是内存——存储KV缓存的内存会超过H100的内存。如果你有B200，你可以增大批次大小更多，但最终你会碰到某个限制。所以你能提高吞吐量的程度是有限的——你永远达不到渐近线，因为你会碰到内存限制。而且你的吞吐量增益也在递减。

---

So increasing batch size worsens the latency because now you have a larger KV cache to read and write. And remember, it's batched. So if you're an individual query, you have to wait for everyone to finish. So you have to basically-- you're waiting for a bus, and the latency is pretty high. You wait and then you go. Whereas, the throughput of a bus is pretty good because you can move everyone at once. So the throughput improves as batch size increases because, remember, the parameters are shared, and you load that once into memory. And you can process a lot of sequences.

增加批次大小会使延迟变差，因为你需要读写更大的KV缓存。而且记住，这是批处理的。所以如果你是一个单独的查询，你必须等待所有人都完成。基本上就像等公交车——你等待，然后上车，延迟很高。而公交车的吞吐量很好，因为你可以一次性运送所有人。所以吞吐量随批次大小增加而改善，因为参数是共享的，你一次性加载到内存，可以处理很多序列。

---

So trade-off between latency and throughput, just to make sure everyone's aligned-- smaller batch sizes use better latency but worse throughput. Large batch sizes yield better throughput but worse latency.

所以延迟和吞吐量之间存在权衡——确保大家都理解：较小的批次大小带来更好的延迟但更差的吞吐量；较大的批次大小带来更好的吞吐量但更差的延迟。

---

OK. I'm not going to really talk about parallelism too much. There's also another dimension of inference, which is you can shard your model across multiple all devices. You can look at the scaling book chapter on inference if you want to know more. Just as a very trivial example, if you launch M copies of the model, the latency is the same, and the throughput increases by M. And then the other metric we didn't talk about is time to first token. And this is essentially the time it takes to do prefill because after you finish prefill, then you can basically start generating. So if you want to fast-- if you want faster TTFT, you should use smaller batch sizes, and you want larger batch sizes to improve throughput. So hopefully, that is clear. Any questions about throughput and latency and how their intention with each other?

我不会过多讨论并行化。推理还有另一个维度——你可以将模型分片(shard)到多个设备上。如果你想知道更多，可以看关于推理的缩放书章节。举一个非常简单的例子：如果你启动M份模型副本，延迟不变，吞吐量增加M倍。另一个我们没讨论的指标是首token时间(TTFT)。这本质上是做预填充所需的时间，因为预填充完成后你就可以开始生成。所以如果你想要更快的TTFT，你应该使用较小的批次大小；而你想要较大的批次大小来提高吞吐量。希望这很清楚。关于吞吐量和延迟以及它们之间的关系，有什么问题吗？

---

OK. So now that we have a conceptual framework for thinking about how efficient inference is in terms of arithmetic intensity and throughput and latency, now let's try to make it faster. How do we make inference faster? There's a bunch of different techniques which are quite varied, ranging from changing the model architecture to doing systems optimization and everything in between. So inference in some sense is a fairly rich cross-cutting topic.

好，现在我们有了一个概念框架来思考推理在算术强度、吞吐量和延迟方面的效率，现在让我们尝试让它更快。如何让推理更快？有很多不同的技术，从改变模型架构到做系统优化，以及介于两者之间的各种方法。在某种意义上，推理是一个相当丰富的跨领域话题。

---
## Reducing the KV Cache / 减少KV缓存

So the most maybe now in hindsight obvious thing you can think about is hopefully beat it into your head that memory is the bottleneck for inference, and the KV cache takes up a lot of memory. And it could even be larger than the number of parameters if for a large enough batch size. So let's just try to reduce the size of the KV cache. Now, you have to be careful about how you do this because you want to make sure you don't lose too much accuracy in the process. So here is one thing you can do, which we already talked about, which is grouped query attention.

现在事后看来，最显而易见的事情就是——希望这已经刻在你脑子里了——内存是推理的瓶颈，而KV缓存占用了大量内存。对于足够大的批次大小，它甚至可能比参数量还大。所以我们来尝试减小KV缓存的大小。但你必须小心做法，因为你要确保在这个过程中不会损失太多准确性。一个我们已经讨论过的做法是**分组查询注意力(Grouped Query Attention, GQA)**。

---

And just as a reminder here, so multi-headed attention-- basically for every token, you have a key and a value and a query. And if you do grouped query attention, you basically compute the same number of queries, but you have only a smaller number of groups, and you compute key and value for each group. So K is the number of groups here. And so in the multi-headed attention, K is N, no reduction. There's something called multi query attention, which no one uses because it's really bad. K equals 1. And somewhere in between is hopefully where we'll find a balance between accuracy and speed.

快速回顾一下：多头注意力(multi-headed attention)——基本上对每个标记，你有一个键、一个值和一个查询。如果你做分组查询注意力，你计算同样数量的查询，但只有较少数量的组，每个组计算键和值。这里K是组数。在多头部注意力中，K等于N，没有缩减。有一种叫做多查询注意力(Multi-Query Attention, MQA)的东西，没人用因为它真的很差——K等于1。两者之间的某个位置，希望能找到准确性和速度之间的平衡。

---

So this is the paper that introduces GQA from 2023. And they show that if you look at time per sample, which is related to both latency and throughput, you see that the MHA-- so Multi-Head Attention. Full attention has this high time. Whereas, if you start K equals 1, it's much faster. And then you can actually keep on increasing the K to K equals 8, and it's still pretty good. And eventually, your time goes up quite a bit.

这是2023年引入GQA的论文。他们展示，如果你看每样本时间(与延迟和吞吐量都相关)，MHA（多头注意力，Multi-Head Attention）——全注意力——时间很高。而K等于1时快得多。然后你可以继续增加K到8，仍然相当好。最终，你的时间会上升不少。

---

OK. So why does GQA improve latency and throughput? Well, it reduces the KV cache by a factor of N over K. And just as a friendly reminder, reducing memory usage leads to speed up because we're memory-bound.

那么为什么GQA能改善延迟和吞吐量？它把KV缓存减少了N除以K倍。善意提醒一下：减少内存使用会带来加速，因为我们是内存受限的。

---

So let's revisit our friendly Llama model here. Remember in the initial configuration, we're just using K equals N. So there's no multi-headed-- there's multi-head attention, no reduction in the number key and values. And so for this one, remember using a batch size of 64, we get this throughput and latency. Now if you do GQA, we're going to put in, let's say, a kind of a sparsity of 1 one five. That reduces the memory quite a bit, which, in turn, improves the latency and also improves the throughput. So it's not that latency and throughput are always at odds. If you reduce the amount of memory, then it improves both. It's mainly the batch dimension that allows. That is the point of tension.

让我们重新看看我们友好的Llama模型。记住在初始配置中，我们用的是K等于N，所以有多头注意力，键和值的数量没有减少。对于这个配置，使用批次大小64，我们得到这个吞吐量和延迟。如果你使用GQA，我们加入一个1/5的稀疏度——这大大减少了内存，进而改善了延迟和吞吐量。所以延迟和吞吐量并不总是矛盾的。如果你减少内存量，两者都会改善。主要是批次维度导致了矛盾点。

---

OK. So this is great. And let's actually just increase the batch size even more and see what happens. So before, if we had a batch size of 256, we ran out of memory. But now, it fits in memory. And we see that, the latency suffers a bit because we're increasing the batch size, but the throughput goes up proportionally. So sometimes you play with these parameters jointly. You can reduce the KV cache, but that allows you to increase the batch size and allow making other trade-offs.

好，这很棒。让我们再增大批次大小看看会发生什么。之前如果批次大小为256，我们会耗尽内存。但现在它适合内存了。我们看到延迟有点受影响——因为我们增加了批次大小——但吞吐量成比例上升。所以有时你可以联合调节这些参数：减小KV缓存，但这允许你增加批次大小，从而做出其他权衡。

---

So the final thing you have to do whenever you do some lossy change is that you make sure the accuracy doesn't drop. And this paper shows that for a GQA, the time is better. But across a bunch of evals, basically it works well. So now with these accuracy values, I think you always have to take it with a grain of salt because this is for a particular model. Later, the deep sea paper should show that it actually does hurt. So I guess, take everything that's not just math with a grain of salt here.

所以每当你做一些有损(lossy)更改时，最后要做的就是确保准确性不会下降。这篇论文显示GQA的时间更好，在一系列评估中基本都表现良好。但说到这些准确性数值，我认为你总是要持保留态度，因为这只是针对某个特定模型。后来DeepSeek的论文显示它实际上确实有损害。所以我想，对任何不仅仅是数学推导的东西都要持保留态度。

---
## Multi-head Latent Attention (MLA) / 多头潜在注意力(MLA)

OK. So speaking of DeepSeek, here's another idea to reduce the KV cache. So the theme is reduce the KV cache and latency and throughput improve. So this is multi-headed attention, same number of queries and keys and values for every token. And GQA, remember, we have reduced the number of keys and values for every token. Sorry, not for every token. We basically have reduced the number of values and keys. And now, the multi-latent attention for DeepSeek says we're actually going to leave the number of keys and values the same one for every token essentially. But I'm going to parameterize-- I'm going to compress these. So normally, you have some-- how do you compute your keys and values? You have your activations, and you multiply them by some matrix to get K and some other matrix to get V. And these are generally N times H dimensions, like your model dim, which is big. So MLA says I'm going to actually project these activations down into C dimensions. So DeepSeek-V2 reduced it from 16,000 to 512, so this is quite aggressive compression here. And then I'm going to compute the k and the V from this compressed representation. So now, I can just store C. This is much smaller. And then when I need my keys and values, I can just materialize them.

说到DeepSeek，这里有另一个减小KV缓存的想法。主题是：减小KV缓存，延迟和吞吐量就会改善。这是多头注意力——每个标记有相同数量的查询、键和值。GQA——记住——我们减少了每个标记的键和值的数量。抱歉，不是每个标记，我们基本上减少了值和键的数量。现在，DeepSeek的**多头潜在注意力(Multi-head Latent Attention, MLA)** 说：我们实际上要保留每个标记的键和值的数量不变，但我要参数化——我要压缩它们。通常，你如何计算键和值？你有激活值，将它们乘以某个矩阵得到K，乘以另一个矩阵得到V。这些通常是N乘以H维度，也就是你的模型维度，很大。MLA说我要把这些激活值投影到C维度。DeepSeek-V2从16,000降到了512，这是相当激进的压缩。然后我从这个压缩表示中计算K和V。现在我可以只存储C，这小得多。当需要键和值时，我只需物化(materialize)它们。

---

So there is one wrinkle here, which is that MLA is not compatible with rope, which operates directly on the keys and values. So what they do is add additional dimensions for handling the rope. But more or less, it's still a pretty big reduction. So the latency and throughput improvements follow by just simple math. The smaller the KV cache, the faster you go. It's almost kind of linear scaling up until at some point. And then, remember, you need to check whether your model is accurate.

这里有一个小问题：MLA与直接操作键和值的RoPE不兼容。所以他们添加了额外的维度来处理RoPE。但大体上，仍然是一个相当大的缩减。延迟和吞吐量的改进只是简单的数学：KV缓存越小，速度越快，几乎呈线性缩放直到某个点。然后，记住，你需要检查模型是否准确。

---

So first of all, this is the result that kind of contradicts or is in tension with the GQA paper. They show that GQA actually isn't that great. So this is MHA. This is GQA. These numbers are smaller than these numbers. But they show that their method, MLA, Multi-Latent Attention works even a little bit better than MHA. But let's just say it's about the same. So this column and this column are much better than-- I guess there's no GQA on this table. You have to compare over here.

首先，这个结果与GQA论文有些矛盾或紧张关系。他们展示GQA实际上并不那么好。这是MHA，这是GQA，这些数字比这些数字小。但他们展示他们的方法MLA——多头潜在注意力——甚至比MHA好一点。但我们可以说大致相同。所以这一列和这一列比……我想这个表格里没有GQA，你得在这里比较。

---

So I'll show you an-- yeah. How does this compare to reducing the number of dimensions, the model? So the question is, how does this compare with reducing the dimension of the model? So that's a good question. These ablations don't show that. My guess is that reducing the model dimension just makes things worse because you're indiscriminately just reducing everything. I think the trick in all of this kind of is to find places in the model where you can squeeze. And this apiary, I don't think you can necessarily know for sure. You just have to do a bunch of experimentation and see what works.

让我展示一下——与减少模型维度相比怎么样？问题是，这与减少模型的维度相比如何？这是个好问题。这些消融实验(ablations)没有显示这一点。我的猜测是，减少模型维度只会让事情更糟，因为你在不加区分地减少一切。我认为所有这些技巧的关键是找到模型中你可以压缩的地方。而这种经验性的东西，我认为你不一定能确定，你只能做大量实验看看什么有效。

---
## Cross-Layer Attention / 跨层注意力

So here's another idea to reduce your KV cache. This is called cross-layer attention. So the idea is that normally, every layer has KV, K's and V's. But let's say instead of doing that, we're just going to compute KVs for a subset of the layers. And then, just for this layer, I'm just going to use the previous layers on KV cache.

这里有另一个减小KV缓存的想法，叫做**跨层注意力(cross-layer attention, CLA)**。正常情况下，每一层都有自己的键和值。但假设我们不这样做，只对一部分层计算KV。然后对于这一层，我就用之前层的KV缓存。

---

So this is another way of sharing. Just like GQA shares K across heads, now I'm sharing KVs across layers. And empirically, this paper shows that doing this improves the Pareto frontier. So each of these models is better than-- given a method you can always sweep this the size of the KV cache by changing the K and the head dimension, which, I guess, kind of relates to your point about changing model dimension. But if you do this CLA cross layer attention, it's better.

这是另一种共享方式。就像GQA跨头共享K，现在我跨层共享KV。实验上，这篇论文显示这样做改善了Pareto前沿。所以每个模型都比……给定一种方法，你总是可以通过改变K和头维度来扫过KV缓存的大小——我想这与你的关于改变模型维度的观点有关。但如果你做CLA跨层注意力，效果更好。

---
## Sliding Window Attention / 滑动窗口注意力

So moving on, whirlwind tour of different techniques for reducing KV cache. There's a local or sliding window attention. This is a fairly kind of old idea and a very kind of natural idea. So if you look at the full attention matrix, it's N squared. And instead of doing that, if you're going to generate a token, you just look at the last K tokens. So you essentially have a sliding window. For every token you generate, you just depend on the last K. And now, if you do that, the effective-- so the KV cache is now independent of the sequence length. It's just the number of the batch times the other variables, which is great. And this is especially great for long context. Now, because of the number of layers, the effective context length is actually larger than the number of the stated context length because information can propagate farther in if you go down the layers. Now, you can do fancier things. You can maybe not do a dense selection of layers, but you can space it out. You can also do this global plus sliding window where aware you have attention to a fixed grid of different token points, plus a local sliding window. So you can do various things.

继续，快速浏览一下不同的KV缓存减少技术。有局部或**滑动窗口注意力(sliding window attention)**。这是一个相当古老且非常自然的想法。如果你看完整的注意力矩阵，它是N平方的。与其这样做，当你要生成一个标记时，你只看最后K个标记。所以你本质上有一个滑动窗口。对于你生成的每个标记，你只依赖于最后K个。如果你这样做，KV缓存现在就独立于序列长度了——它只是批次乘以其他变量，这很棒，尤其是对于长上下文(long context)。由于层数的原因，有效上下文长度实际上大于标称上下文长度，因为信息可以在逐层向下传播时传播得更远。你可以做更花哨的事情：你可能不做密集的层选择，而是稀疏排列。你也可以做全局加滑动窗口的组合——你对不同标记点的固定网格做注意力，加上一个局部滑动窗口。所以你可以做各种事情。

---

Now, the problem with this is that it actually still hurts accuracy. So this reduces expressivity. There's no free lunch here, or at least this was an expensive lunch. So the solution that people come up with is that they interleave local attention with global attention. So these hybrid models have full attention for some of the layers and some local layers for some of the other layers. And you're basically always trying to-- and then so that allows you to essentially reduce the KV cache a little bit. And you're always trying to balance accuracy with the speed.

问题在于这仍然会损害准确性。所以它降低了表达能力(expressivity)。天下没有免费的午餐，或者至少这是一顿昂贵的午餐。人们提出的解决方案是交错使用局部注意力和全局注意力。这些混合模型(hybrid models)对某些层使用全注意力，对其他一些层使用局部注意力。这允许你减少一点KV缓存。你总是在准确性和速度之间寻找平衡。

---

Yeah. Hybrid model-wise, is there a difference between the trade-off in using a linear time invariant versus a sliding window? Yeah. So the question is, what about linear attention versus sliding window attention? So I'm not going to talk about linear attention. But very quickly, there's a bunch of methods that where, instead of storing KV cache, since you basically compute some of compressed representation of all the history. So linear, the most naive linear attention is you just sum the KV values up into a single vector. So that's definitely independent of the sequence length. You can do fancier things. There's gated net, delta nets, and Mamba which allows you to try to compress but not forget as much.

好。关于混合模型，使用线性时不变(linear time invariant)与滑动窗口之间的权衡有区别吗？问题来了：线性注意力(linear attention)与滑动窗口注意力相比如何？我不打算深入讲线性注意力，但快速说一下：有很多方法，不再存储KV缓存，而是计算所有历史的一些压缩表示。最朴素的线性注意力就是把KV值求和成一个向量，这当然独立于序列长度。你可以做更花哨的事情——有门控网络(gated net)、delta网络(delta nets)和Mamba，它们允许你尝试压缩但又不会遗忘太多。

---

Now the question is, how do those compare? Those have also been used in place of sliding window attention, and people have gotten good results with them. You can also use a combination of full attention, sliding window intention, and the linear attention because they capture different aspects. If you care about local high-resolution stuff, then sliding attentions better. If you just want broad summaries of the past, then the other linear attention might be better.

问题在于，它们相比如何？这些也被用来替代滑动窗口注意力，人们用它们取得了很好的结果。你也可以组合使用全注意力、滑动窗口注意力和线性注意力，因为它们捕捉不同的方面。如果你关心局部高分辨率的内容，滑动窗口注意力更好；如果你只想要过去的广泛摘要，那么线性注意力可能更好。

---

So then for a long context sentence, would you say your attention would be a better setting for that? So the question is, for long context with linear attention be better?

那么对于长上下文句子，你会说注意力是更好的设置吗？问题是，在线性注意力下，长上下文会更好吗？

---

So there's no free lunch, right? Let's say you have a very long context, and you're solving a needle in a haystack problem. If you have to compress your entire history into a small context, you're just going to lose information, and you might just not be able to retrieve it. I guess I feel like what it seems like people go with hybrid architectures that you'll always need some of longer attention, but I'm just trying to understand in my head, what the trade-off between using a sliding window versus some of a Mamba, delta net layer would be. Is using a delta net layer better than using sliding window consistently? Or what is the actual maybe representative trade-offs?

没有免费的午餐，对吧？假设你有一个非常长的上下文，正在解决一个"大海捞针"(needle in a haystack)问题。如果你必须把整个历史压缩到一个小上下文中，你只会丢失信息，可能根本无法检索到它。我想感觉上人们会采用混合架构——你总是需要一些更长的注意力。但我只是在脑海中试图理解，使用滑动窗口与使用Mamba、delta网络层之间的权衡是什么。使用delta网络层是否一贯地比使用滑动窗口更好？或者实际的代表性权衡是什么？

---

Yeah. Maybe I'll say that the Mamba and delta net are more powerful than the sliding window. Attention maybe you can think about the Mamba as probably can-- it certainly can represent some of the aspects of sliding window attention because you can just-- as you're doing the recurrence, it can just look at the last state. So yeah, maybe you can think about the linear attention or its extensions as being better. They have more room. Once you do sliding window attention, you're done. There's nothing else you can-- [INAUDIBLE] Yeah.

嗯，也许我会说Mamba和delta网络比滑动窗口更强大。你可以认为Mamba肯定可以表示滑动窗口注意力的某些方面，因为当你在做循环(recurrence)时，它可以只看最后的状态。所以是的，也许你可以认为线性注意力或其扩展更好。它们有更多空间。一旦你做了滑动窗口注意力，你就完了，没有别的可做的了。[听不清] 是的。

---

OK. So let me just quickly go through this. Just highlight this DeepSeek. DeepSeek continues to innovate different types of attention mechanisms. So remember, they came up with the multi-latent attention, which compresses the key values. There is this thing called-- now they have compressed sparse attention, DeepSeek sparse attention, and heavily compressed attention. I never remember all these acronyms and what they mean, but let's look at this diagram. So normally, have your KV tokens and your query token. So compressed attention is going to basically compress every M tokens into one token. And then there's this thing called DeepSeek sparse attention, which basically selects a subset of those to keep. And the way you select a subset is that you actually compute some LiDAR weight queries and keys, and then you do a smaller attention to get these index scores so you know to keep. So a lightning fast way to figure out what tokens you need to keep. And then you use those. And then, there's some more compression that happens. So in the interest of time, I'll move on.

好，让我快速过一下这个。重点提一下DeepSeek。DeepSeek持续创新不同类型的注意力机制。记住，他们提出了多头潜在注意力(MLA)来压缩键值。他们还有——现在他们有压缩稀疏注意力(compressed sparse attention)、DeepSeek稀疏注意力(DeepSeek sparse attention)和重度压缩注意力(heavily compressed attention)。我永远记不住所有这些缩写和它们的含义，但让我们看看这张图。通常情况下，你有KV标记和查询标记。压缩注意力基本上把每M个标记压缩成一个标记。然后DeepSeek稀疏注意力选择这些的一个子集保留。选择子集的方式是你实际计算一些……权重查询和键，然后做一个小注意力来得到索引分数(index scores)，从而知道要保留哪些。这是一种极快的方式来确定你需要保留哪些标记。然后你使用这些标记。然后还有更多压缩发生。为了节省时间，我继续往下。

---
## Summary of KV Cache Reduction / KV缓存减少总结

The goal of this section is to reduce the KV cache because KV cache is related to memory. And we saw that inference is memory-bound. So that directly translates to improvements in throughput and latency. And the key is to do this without hurting accuracy. So you can do lower dimensional KV caches across layers by across heads and across head dimension. You can do local attention. You can do linear attention, which was discussed earlier, and there's much more. And there's also diffusion models, which is a non-autoregressive way to generate which can be much faster.

本节的目标是减少KV缓存，因为KV缓存与内存相关。我们看到推理是内存受限的，所以这直接转化为吞吐量和延迟的改善。关键是做到这一点而不损害准确性。你可以跨层、跨头和跨头维度做低维KV缓存。你可以做局部注意力(local attention)。你可以做线性注意力(linear attention)——之前讨论过——还有更多。还有扩散模型(diffusion models)，这是一种非自回归的生成方式，可以快得多。

---
## Quantization / 量化

OK. So let's talk about a few other ideas which are important. So quantization is more of a, I would say, less of an architecture and much more of a systems of perspective on how to make things smaller. So the key idea here is just reduce the precision of numbers. Less memory means higher latency and throughput. And obviously, you have to worry about accuracy. So quantization is-- there's many options here all the way from bf16 all the way down to int4.

好，让我们讨论其他一些重要想法。**量化(quantization)**——我想说——与其说是一种架构，不如说是一种从系统角度让东西变小的方法。核心思想就是降低数字的精度。更少的内存意味着更高的延迟和吞吐量。显然，你必须担心准确性。量化有很多选项，从bf16一直到int4。

---

And so one thing you can do, if you're scared that quantization is going to mess you up, is that you train a model with quantization in mind. So this is quantization aware training. And during the feedforward pass during training, you quantize and dequantize, and you're basically simulating these quantization errors as you train. So then, generally, now the weights are adapted towards quantization. Things will work better. But the con is that it requires expensive large-scale training.

如果你担心量化会搞砸，你可以做的一件事是在训练时就考虑量化。这就是**量化感知训练(quantization aware training, QAT)**。在训练的前向传播(forward pass)中，你进行量化和反量化(dequantize)，在训练时模拟这些量化误差。这样，权重通常会适应量化，效果会更好。但缺点是需要昂贵的大规模训练。

---

And so what typically people do is they train models, and then they quantize after the fact. So this is post-training quantization. It's much cheaper often. There's a naive way to do it is that for every layer or tensor, you basically determine the scale and the 0 point for each, let's say, tensor. And then you quantize that separately. This generally doesn't work as well. You can use this idea called GPTQ, which uses some Hessian information to quantize layer by layer. And then you keep track of the errors which get propagated into the non-quantized weights. And so it allows you to correct for the errors. And now, activation-aware quantizing is more of a sophisticated way where the observation is that some activation channels are large and those the weights that interact with those matter more. So let's allocate more precision to these weights.

所以通常人们做的是：先训练模型，然后事后量化。这就是**训练后量化(post-training quantization, PTQ)**，通常便宜得多。一种朴素的做法是对每一层或每个张量确定比例(scale)和零点(zero point)，然后分别量化。这通常效果不太好。你可以使用一种叫做GPTQ的想法，它利用一些Hessian信息逐层量化，并跟踪传播到未量化权重中的误差，从而允许你纠正误差。而**激活感知量化(activation-aware quantization, AWQ)** 是一种更复杂的方法，它观察到一些激活通道(activation channels)很大，与这些通道交互的权重更重要，所以给这些权重分配更多精度。

---

So let's look at this picture. So normally, if you take fp16 weight matrix, and you quantize it, you get-- let's say you quantize it down to int3. But what you're going to do is you figure out which of these are active? So these are maybe activation channels. And some of these activation channels are large. So if they're large in general, then you basically allocate like, let's say, fp16 for this channel. You keep everything else as in three. And for a few important channels, you use higher precision.

让我们看这张图。通常，如果你取一个fp16的权重矩阵并进行量化，比如说量化到int3。但你要做的是找出哪些是活跃的。这些可能是激活通道，其中一些很大。如果它们总体上很大，你就分配给这个通道fp16，其他所有保持3bit。对少数重要通道，使用更高精度。

---
## Pruning / 剪枝

So another idea here is to do model pruning. So here you just take a large model, and you rip out pieces of it, and you fix it up. It's a very crude way, but it turns out to work. So there's this paper from NVIDIA where, essentially-- let me actually-- let's see. So you first have to estimate the importance of the different parts of the model and choose the most important parts. And then you basically remove different hidden units and different even layers. And now, we have a model. It's not going to be very good. And so what you do is you post-train it. You train it some more on the data or the tasks that you care about to heal it. So this is, in some sense, a training way to reduce the KV cache, but where you initialize it with parts of a good model. So this seems to work pretty well. So they were able to take a 15B model and reduce it to an 8B model. And it doesn't really hurt accuracy by too much. And the amount that you use to train the model or through this process is much less.

另一个想法是**剪枝(pruning)**。你拿一个大模型，去掉它的一部分，然后修复它。这是一种非常粗暴的方法，但事实证明是有效的。NVIDIA有一篇论文：你首先需要估计模型不同部分的重要性，选择最重要的部分。然后你移除不同的隐藏单元，甚至不同的层。现在你得到一个模型，它不会很好。所以你要做的是后训练(post-train)——在你关心的数据或任务上多训练一些来"修复"它。这在某种意义上是一种减少KV缓存的训练方式，但初始化的权重来自一个好模型的一部分。这似乎效果相当好。他们能够把一个15B的模型缩减到8B模型，准确性损失不太大，而且用于训练或这个过程的计算量少得多。

---
## Distillation / 蒸馏

OK. So just to summarize here, the game is to reduce the inference complexity without hurting accuracy. You can think about this as mostly reducing the number of parameters or CPU cache. You can define a faster model architecture to train it, or you can define a faster model architecture. Initialize the weights from original model, which might have a different architecture, but you just make this Frankenstein thing, and then you repair the faster model with distillation.

好，总结一下：目标是在不损害准确性的情况下降低推理复杂度。你可以把这主要看作是减少参数量或KV缓存。你可以定义一个更快的模型架构来训练它，或者定义一个更快的模型架构，用原始模型的权重初始化（原始模型可能有不同的架构），你做出这个"弗兰肯斯坦"式的混合体，然后用**蒸馏(distillation)**来修复这个更快的模型。

---

Yeah. Could you say more about you distinguish the important from the unimportant layers? So how do you distinguish the important layers from the unimportant layers? So in general, you have a calibration set, and you pass the inputs through the model. And you're basically looking at the magnitude of the activations. And the ones that are-- some of them, especially if they're dead units, will be kind of close to 0. And the ones that are large, you want to keep. So that's a high-level idea.

能再多说说你如何区分重要和不重要的层吗？一般来说，你有一个校准集(calibration set)，将输入送入模型，然后观察激活值的幅度。其中一些——尤其是死单元(dead units)——会接近0。而那些大的，你想保留。这是一个高层次的想法。

---

I guess why does it matter if the activation is high? It could just be like-- what if it's just always high, for instance? Or is that-- So the question is, what if all the activations are high? So in general, this is a kind of an empirical observation that some of the channels will be much higher than others. If this weren't true, then these techniques wouldn't necessarily work, but it happens to be true because that's how these models ended up being trained. And then you can exploit that. Say a neuron, which is always value 100 across all the samples. Would that mean that it's necessarily meaningful? Or maybe it's just an artifact of training that I'm just like [INAUDIBLE]? Yeah, I see. So the question is, what if a neuron is always 100? I mean, if that's the case, you can also look at variance-related questions. If it's 100, you can't just remove it because then everything is going to be broken. If it's high mean and low variance, maybe there's another a way to just incorporate the bias essentially.

但我猜为什么激活值高就重要？它可能只是……如果所有激活值都高呢？一般来说，这是一个经验观察：某些通道会比其他的高得多。如果不是这样，这些技术就不一定有效，但碰巧这是真的，因为这些模型就是这样被训练出来的。然后你可以利用这一点。假设一个神经元在所有样本上的值都是100，那它一定是重要的吗？或者它只是训练的一个伪影(artifact)？我看到这个问题了。如果神经元总是100，你不能直接移除它，因为那样所有东西都会坏掉。如果它是高均值、低方差，也许有另一种方法，本质上就是合并一个偏置(bias)。

---
## Speculative Decoding / 推测解码

OK. Let me quickly go through this other idea. So far, we've looked at lossy methods which basically really crunch down the KV cache, but it could hurt accuracy. This is a very elegant way of doing this in a lossless way. This is called speculative sampling or speculative decoding. So remember that if you're doing prefill, you can encode all the tokens in parallel. This also gives you probabilities. This is fast. This is compute-bound and all nice things. And in generation, it's one at a time. So checking is faster than generation. If I give you a sequence, it's fast to tell me how good it is, much faster than it is to generate one at a time. So you can exploit this asymmetry using the following idea.

好，让我快速过一下另一个想法。到目前为止，我们看了有损方法(lossy methods)——它们基本上压缩了KV缓存，但可能损害准确性。这是一个非常优雅的无损(lossless)方法，叫做**推测采样(speculative sampling)**或**推测解码(speculative decoding)**。记住，如果你在做预填充，你可以并行编码所有标记，这也会给你概率。这很快，是计算受限的，一切都很好。而在生成时，是一个接一个。所以检查(checking)比生成快。如果我给你一个序列，告诉我它有多好是很快的——比逐个生成快得多。你可以利用这种不对称性，使用以下想法。

---

So what we're going to do is use a cheap draft model to basically generate from the guest a few tokens, let's say four tokens. And then we're going to use the model we actually care about, the target model Q, which to basically review these tokens and accept or not accept them. So things are kind of chosen to be balanced. The draft model is just smaller and cheaper. And so even though it's memory-bound, and it has to generate one at a time, is not too bad. Whereas, the target model is big and expensive, but what we're doing is asking it to process a batch of tokens in parallel so it won't also be too bad.

我们要做的是使用一个便宜的草稿模型(draft model)来生成几个标记，比如说四个标记。然后我们使用我们真正关心的模型——目标模型(target model) Q——来审查这些标记并决定接受或不接受。这样事情就平衡了。草稿模型更小、更便宜，所以尽管它是内存受限的，必须逐个生成，但也不至于太糟。而目标模型又大又贵，但我们让它并行处理一批标记，所以也不会太糟。

---

OK, so here's the video that shows how things work. So if you use a big model token by token, it's going to be pretty slow. But if you are doing speculative decoding, then you can see the small model generating a bunch of tokens, and then the large model basically critiquing them. And then, so you basically can get this burst of tokens and then maybe another burst of tokens and so on and so forth.

好，这里有一个视频展示工作原理。如果你用一个大模型逐个标记生成，会非常慢。但如果你做推测解码，你可以看到小模型生成一批标记，然后大模型来评审它们。这样你就可以得到一批突发(burst)的标记，然后再一批，如此反复。

---

OK. So here is the algorithm for-- there's a few papers that came out with speculative decoding around the same time. This is one of them. And so the idea here is that in order to generate, we're going to generate K tokens. And we're just going to sample from this draft model. So p is the draft model. We're going to sample K tokens. And then in parallel, we're going to compute the logits of these draft tokens using q. And then now we have to determine whether we accept or not. And this is where you do a bit of math and probability and statistics. You basically are going to accept with probability Min 1 over this ratio of q over p. So if q is much larger than p, the larger the q is, the more likely you want to accept it.

好，这是算法——有几篇论文几乎同时在同期发表了推测解码。这是其中之一。想法是：为了生成，我们生成K个标记，从草稿模型p中采样K个标记。然后并行地用q计算这些草稿标记的logits。然后我们确定是否接受。这里需要一些数学和概率统计。你基本上是按照最小1与q/p之比的最小值来接受。如果q远大于p，q越大，你越可能接受它。

---

And otherwise you sample from this residual distribution and exit. So this is basically rejection sampling except for rejection sampling. Sometimes when you reject you get nothing. But here we always are guaranteed to get an exact sample from the target model. I'm going to skip this simple proof. It's basically the same arguments as rejection sampling to show that it's the exact probabilities from the target model. And the initial paper shows that this fast. And generally, if you have too few draft tokens, you're not really leveraging the batching on the target model side. And if you have too many, then you're going to reject more often. So there's a sweet spot around, in this case, three or four. And in general, the draft model is much smaller than the target model. And ideally, you want the model draft model to be as close to the target, which means that you want to distill it, which means that actually a lot of the same ideas that we just talked about are applicable to speculative decoding as well.

否则你从这个残差分布(residual distribution)中采样并退出。这基本上是拒绝采样(rejection sampling)的一种变体，但拒绝采样中当你拒绝时你会一无所获。而这里我们总是保证能得到目标模型的精确样本。我跳过这个简单的证明——它与拒绝采样的论证基本相同，表明它得到的是目标模型的确切概率。最初的论文显示这很快。通常，如果草稿标记太少，你没有充分利用目标模型侧的批处理；如果太多，你会更频繁地拒绝。所以有一个最佳点——在这个例子中是三或四个。通常草稿模型比目标模型小得多。理想情况下，你希望草稿模型尽可能接近目标模型，这意味着你想要蒸馏它——实际上，我们刚才讨论的很多相同想法也适用于推测解码。

---

So basically, the idea is that let's try to reduce your KV cache via all the different shenanigans. And if you end up with a model you're happy with, just serve that. If you're not happy with it, then it at least can be a draft model and you can use your main model to fix things up. There's a bunch of whole literature on speculative decoding right now that improve over the original, which I'll skip for now.

所以基本上，想法是：尝试通过各种技巧减少KV缓存。如果你最终得到一个满意的模型，就直接服务它。如果不满意，它至少可以作为一个草稿模型，然后你用主模型来修正。现在有很多关于推测解码的文献改进了原始方法，我暂时跳过。

---
## Dynamic Workloads / 动态工作负载

So very quickly now, dynamic workloads. So this is the use case, is you're serving a live website, and users come and chat with your model. The requests arrive at different times. They have different shared prefixes, and they have different lengths. So it's kind of pretty messy. It's far from this very simple training where you have these blocks of the same number of tokens all at once. So what do you do in this case? So there's this idea-- there's a system called Orca that was built. This is actually very early on which introduced this idea of continuous batching. So the idea is that you get a bunch of requests that look like this. So here's a prefix of the first request, and you're generating this token. Here's the second one. Here's the third one, the fourth one. It's jagged because every prefix has a different length. And what we're going to do is we're going to decode step by step. So every step you decode one token for all the sequences. Next step, you decode another token for all the sequences. And then if you end, you just eject that sequence. And then as new requests arrive to the batch, then you basically put it in the batch, and then you just continue. So that's why it's called continuous batching because it's this batch is dynamically being updated with either old finished sequences being evicted and new ones coming in.

快速进入动态工作负载(dynamic workloads)。这是你服务一个实时网站的场景——用户来与你的模型聊天。请求在不同时间到达，有不同的共享前缀(shared prefixes)和不同的长度。这相当混乱，远不像训练那样所有块都有相同数量的标记同时到达。那么你该怎么办？有一个叫做Orca的系统很早就引入了**连续批处理(continuous batching)**的概念。你收到一堆像这样的请求：这是第一个请求的前缀，你在生成这个标记；这是第二个、第三个、第四个。它们是参差不齐的(jagged)，因为每个前缀有不同的长度。我们要做的是逐步解码——每一步为所有序列解码一个标记，下一步再为所有序列解码另一个标记。如果一个序列结束，就把它弹出。当新请求到达批次时，把它放进来，然后继续。所以这被称为连续批处理，因为批次被动态更新——旧的已完成序列被移除，新的序列进入。

---

So now, one problem here is that everything we've seen batching works when all the sequences have the same dimensionality. You have tensors. Every slice has the same dimensionality. But if you request here has a different length, so what do you do about that? So there's this idea called selective batching where let's say you have a length 3, length 9, and a length 5. So here in the attention computation, you can't really do anything about this because attention depends on the length of your sequence. So if you have a 3 by 3, a 9 by 9 computation, you can't really share the tensor effectively. But for the non-attention, the MLP layers, which takes up a lot of FLOPs, you can actually just concatenate all the sequences together to form a mega sequence, and you process that.

现在有一个问题：我们之前看到的所有批处理都是在所有序列具有相同维度时才有效。你得到张量，每个切片有相同的维度。但如果请求有不同的长度，你该怎么办？有一个叫做**选择性批处理(selective batching)**的想法。假设你有长度3、长度9和长度5的序列。在注意力计算中，你对此无能为力，因为注意力取决于你的序列长度——3x3和9x9的计算不能有效共享张量。但对于非注意力部分——占据大量FLOPs的MLP层——你实际上可以把所有序列拼接起来形成一个超大序列(mega sequence)并处理它。

---
## Paged Attention / 分页注意力

So final idea is page attention. This was introduced in the BLM paper. Of course, BLM has many other bells and whistles now, but this is the core idea at that time. So the question is, how is the KV cache stored? So if you think about requests coming in, you have to put them in memory somewhere. And in general, there's this problem that you get fragmentation. This is what happens to-- or used to happen to your hard drive. And you have to defrag your hard drive back in the day. So there's two types of fragmentation. One is that you have to allocate enough buffer so that-- because you don't when you're going to stop. So you might have a max token limit of 1,024. So you have to allocate all this memory. And you can't put anything in there because you're going to just generate until you hit the max tokens, and that's very wasteful. That's internal fragmentation. And then there's also you have-- there could be space between different requests. And that space is maybe too small to get used effectively. So that's just wasted space.

最后一个想法是**分页注意力(paged attention)**。它是在vLLM论文中引入的——当然vLLM现在有很多其他功能，但这是当时的核心思想。问题是：KV缓存是如何存储的？当请求到来时，你必须把它们放在内存的某个地方。通常会遇到**碎片化(fragmentation)**问题——就像过去硬盘会发生的情况，你必须做磁盘碎片整理。有两种碎片：一种是你必须分配足够的缓冲区，因为你不知道何时结束。你可能有一个最大标记限制1024，所以你必须分配所有这些内存，但里面放不了别的东西，因为你只会生成直到达到最大标记数——这非常浪费。这是内部碎片(internal fragmentation)。另一种是不同请求之间可能有空隙，这些空隙可能太小而无法有效利用——这就是浪费空间。

---

So the solution here is just these are systems people. So they know their operating systems. They said, OK, well we've solved this problem once before, so let's just use the same idea here. So we're going to divide the KV cache of a sequence into non-contiguous blocks, OK? So if you have this sequence, four score and seven years ago our fathers brought forth, we're just going to chunk it up into these blocks of size 4. Doesn't matter where the blocks go, but they're going to be aligned according to the block. So there's some uniformity there. So when two requests share the same-- can actually share the same KV cache.

解决方案是——这些是系统专家，他们了解操作系统。他们说，好的，我们以前解决过这个问题，所以在这里用同样的思路。我们要把一个序列的KV缓存分成非连续的块(non-contiguous blocks)。所以如果你有这个序列"four score and seven years ago our fathers brought forth"，我们把它分成大小为4的块。块在哪里不重要，但它们是按块对齐的，所以有一定的一致性。当两个请求共享相同的前缀时，它们实际上可以共享相同的KV缓存。

---

So you might have this block and this block. So this block might go here and here, and this block might be over there. So they're interspersed. But as long as you have the indices and keep track of where everything is, it's fine. So in particular, if you have, system prompts, then you can actually just cache these system prompts, the KV cache and the system prompts, once. And that can be useful for all the queries, OK? So this is very useful because if a lot of people are using the same system prompt, then you don't have to compute the cache for every request. Also there are many applications where you have the same prompt, and you actually want to generate multiple responses. So in that case, you can also just share the KB cache for the prompt and just have unique responses coming out.

所以你可能有一块和这一块，这一块可能在这和这，那一块可能在那。它们是交错的。但只要你有索引并跟踪所有东西的位置，就没问题。特别是，如果你有系统提示(system prompts)，你可以缓存这些系统提示的KV缓存一次，这对所有查询都有用。这非常有用，因为如果很多人使用相同的系统提示，你就不需要为每个请求计算缓存。还有在多个应用中，你有相同的提示，想要生成多个响应，在这种情况下你也可以共享提示的KV缓存，只产生独特的响应。

---

OK, So for example, if you were to generate, let's say, multiple generations from score and seven years ago are, blank, and so what would happen here is that you would have score and seven. And you would start by having years ago or our. And then this is called copy on write semantics. You keep this. And then we have these two samples. And if they had happened to sample let's say the same token, you just continue with that. But if they sample different tokens, you split the block, and then you can continue there. So you're basically sharing as much of the prefix cache as you can. There's a bunch of other optimizations like kernels that I'm not going to have time to go over. But the general idea is that you're using these operating systems metaphors to manage your inference.

例如，如果你要从"score and seven years ago are"生成多个续写——你会有"score and seven"，然后会有"years ago"或"our"。这被称为写时复制(copy on write)语义。你保留这个，然后有两个样本。如果它们碰巧采样了相同的标记，你就继续。如果它们采样了不同的标记，你就分裂(split)这个块，然后继续。所以你尽可能多地共享前缀缓存。还有很多其他优化，比如核函数(kernels)，我没有时间一一介绍。但总体思路是使用操作系统隐喻来管理你的推理。

---
## Summary / 总结

So summary here-- inference is really, really important. It's very different from training. Even though it's the same model, but you're asking the model to do something very different, ends up being very memory-bound. And it's also dynamic if you're in a live chatbot use case. We saw a variety of different techniques to improve inference. You can quantize. You can come up with new architectures. You can prune and distill. You can also use speculative sampling. But all of these are driven by the same principle here, which is reduce your KV cache but don't hurt accuracy too much. And then there's ideas from systems like paging and speculative execution that can be brought to bear for actually live inference servers.

总结：推理真的非常重要。它与训练非常不同。虽然是同一个模型，但你让模型做非常不同的事情——最终变得非常内存受限。如果你在实时的聊天机器人场景中，它也是动态的。我们看到了各种不同的技术来改进推理：你可以量化，你可以提出新架构，你可以剪枝和蒸馏，你也可以使用推测采样。但所有这些都遵循同一个原则：减少KV缓存，但不要过多损害准确性。此外，来自系统的思想，如分页(paging)和推测执行(speculative execution)，可以应用于实际的实时推理服务器。

---

One thing we didn't really get a chance to talk about, which was discussed briefly, is that I think that new architectures have actually a huge potential for improvement, things like state space models or linear attention or diffusion. At some level, the KV cache and the way that attention is built fundamentally makes it an inference unfriendly kind of architecture. So if you can come up with a new architecture that is designed for inference in the way that the transformer was not, this can maybe unlock a lot. OK, so I will stop there. And next class, Tatsu will return and talk about scaling laws part 2.

有一件事我们没有真正机会讨论——只是简要提及过——我认为新架构实际上有巨大的改进潜力，比如状态空间模型(state space models)、线性注意力(linear attention)或扩散模型(diffusion)。在某种程度上，KV缓存和注意力的构建方式从根本上使它成为一种对推理不友好的架构。所以如果你能提出一种像Transformer所不擅长的那样、为推理而设计的新架构，这可能会解锁很多潜力。好，我就讲到这里。下节课Tatsu会回来讲缩放定律第二部分。

---
