---
title: "Lecture 10: Inference"
---

# Lecture 10: Inference / 第十讲：推理

## 1. Introduction: Why Inference Matters / 引言：推理为何重要

So last time, Tatsu talked about scaling laws, and we're going to take a little break from that and talk about inference. The problem of inference is very simple. You've trained a model, and you're given a prompt, and you want to produce the response usually as accurately and as quickly as you can.

上一讲Tatsu讲了缩放定律，我们暂时从那个话题中跳出来，谈谈推理。推理的问题非常简单：你训练好了一个模型，给定一个提示，你想尽可能准确且快速地生成回复。

So inference turns out to be only one lecture, but it's actually of growing importance. It shows up in many places. Once you've trained a model, you actually want to use this model. What does use look like? It could be chatting with an AI assistant or chatbot, it could be doing code completion. These days, agents are very popular, and that requires inference. Batch data processing as well. It's also used for evaluation—for evaluation that requires generation in particular. And it's also used inside training: if you're doing reinforcement learning, you need to have a model, you generate rollouts, and you score them, and you update the weights appropriately. So inference shows up all over the place.

推理虽然只占一讲，但其重要性日益增长，且应用的场景非常多。训练好模型之后，你当然不只是把它放着。使用模型的场景包括：与AI助手或聊天机器人对话、代码补全、如今非常流行的智能体（agent）也需要推理、批量数据处理、评估（尤其是需要生成能力的评估），甚至在训练内部也会用到——做强化学习时你需要一个模型，生成rollout，打分，然后相应地更新权重。所以推理无处不在。

And efficiency really matters more than ever here. Training is a one-time cost—it could be very expensive. But once you're done with it, that's it. But inference is a repeated cost. You incur it every single day. OpenAI is estimated to produce 8.6 trillion tokens a day. And just for reference, DeepSeek-V4, which came out earlier this year, was trained on 32 trillion tokens. So in less than four days, the number of tokens that OpenAI has to produce, and therefore the compute, is at least DeepSeek-V4. The number of tokens generated is going to be higher than the number of tokens trained on. So that's some perspective.

在这里效率比以往任何时候都重要。训练是一次性成本——它可能非常昂贵，但一旦完成就结束了。而推理是重复性成本，每天都在产生。据估计，OpenAI每天生产8.6万亿个token。作为参考，今年早些时候发布的DeepSeek-V4训练用了32万亿个token。所以在不到四天的时间里，OpenAI必须生产的token数量——以及相应的计算量——就至少相当于训练一个DeepSeek-V4。推理生成的token数量将高于训练所用的token数量。这提供了一些视角。

Moreover, the importance of inference has grown in the last year because once upon a time, we thought of language models primarily as chatbots or assistants, where you put in a prompt, you get back a response, and presumably, the goal of the human is to read the response. But now, as we move more into an agentic world, what it looks like is that a query goes in, and the agent is going to do a bunch of stuff—it's going to think, it's going to reason, it's going to call some tools, it's going to introspect. And at the end of the day, it will produce some output for a human to read. So most of the tokens that the agent produces is actually not for reading. And so you should really think about the number of tokens generated as really the compute spend. There's no limit—if you have an ambitious enough problem, you're going to need much compute and a lot of tokens.

此外，推理的重要性在过去一年中进一步增长，因为我们曾经把语言模型主要视为聊天机器人或助手，你输入提示，得到回复，假定人类的目标是阅读回复。但现在，随着我们进入一个更具智能体特性的世界，情况变成：一个查询进入，智能体会做一大堆事情——它会思考、推理、调用工具、自我反思——最终才会产生一些输出供人类阅读。所以智能体产生的大部分token实际上不是给人看的。因此，你应该真正把生成的token数量视为计算开销。没有上限——如果你面临一个足够宏大的问题，你将需要大量计算和海量token。

If you were in the chatbot world, maybe inference after a certain point, it's fast enough, because humans can only read so fast. But for an agent, there's no limit to how much value you can get out of squeezing more out of inference. So there's a lot of people doing inference on the commercial side. All the closed API providers have to serve their models, so inference is a big deal for them. And there is also a bunch of providers serving open weight models and providing inference as well. In the open source community, there's a bunch of packages—VLM is probably a popular one, kind of a go-to. SG Lang is another one that's particularly good for agentic workloads. And then there's TensorRT from NVIDIA, which is really fast, but it's more narrow. And then Llama CPP, if you want to run inference on CPU, this is a popular package.

在聊天机器人世界中，推理到某个程度后可能已经足够快了，因为人类的阅读速度有限。但对于智能体来说，从推理中榨取更多价值的上限是无限的。所以在商业领域有很多人做推理——所有闭源API提供商都必须服务自己的模型，推理对他们至关重要。也有很多提供商服务开放权重模型并提供推理。在开源社区中，有许多软件包——VLM可能是一个流行的首选。SG Lang是另一个，特别适合智能体工作负载。还有NVIDIA的TensorRT，速度非常快但适用范围较窄。如果想在CPU上运行推理，Llama CPP是一个流行的选择。

---

## 2. What Does "Fast" Mean? Metrics / "快"意味着什么？度量指标

If you can make inference twice as fast or even 10% faster, that is a big deal. So the question is, what does "fast" mean? There's a few metrics that capture the notion of fast, and they're going to be applicable in different settings and have different trade-offs.

如果你能让推理速度翻倍，或者甚至快10%，那都是一件大事。那么问题来了，"快"意味着什么？有几个度量指标可以捕捉"快"的概念，它们适用于不同场景，并且有不同的权衡。

**Time to First Token (TTFT) / 首token时间（TTFT）**：This is essentially how long a user waits before any generation happens. You put in a query into ChatGPT, and some number of milliseconds passes by, and then from the point the first token comes in, that is the time. This is generally useful for interactive applications because that latency where you're just waiting and doing nothing—the longer that is, the worse the user experience, and as soon as tokens come in, it doesn't maybe have to be that fast, because if you're going to read it anyway, you can't read that fast.

这本质上是用户在看到任何生成内容之前需要等待多长时间。你向ChatGPT输入一个查询，经过若干毫秒后，第一个token出现——那段时间就是TTFT。这对交互式应用很重要，因为干等的延迟越长，用户体验越差。而一旦token开始出现，可能不需要那么快，因为反正是要阅读的，人读不了那么快。

**Latency / 延迟**：This is from the standpoint of an individual user. How fast are tokens appearing for one query? This is also important for interactive applications. Basically, this is how fast the tokens are streaming through.

这是从单个用户的角度来看：单个查询的token出现的速度有多快？这对交互式应用也很重要。本质上，这是token流式输出的速度。

**Throughput / 吞吐量**：Measuring tokens per second, this is how fast tokens are appearing for many queries. Latency and throughput are clearly very related—in general, many interventions will make latency and throughput better. But as we'll see later, there's actually a trade-off here. Throughput is useful if you're doing a bunch of batch processing—you have a petabyte of data, and you want to process it with a language model. You just want that job to get done. It doesn't matter if one query is coming in faster, sooner, or later.

以每秒token数衡量，这是许多查询一起时token出现的速度。延迟和吞吐量显然非常相关——一般来说，许多优化措施会同时改善延迟和吞吐量。但后面我们会看到，实际上这里存在一个权衡。如果你在做批量处理——你有PB级的数据想用语言模型来处理——你只希望那个任务完成。单个查询是否有更快的延迟无所谓。

---

## 3. Training vs. Inference: The Fundamental Difference / 训练与推理：根本区别

What determines the efficiency of inference? The high-level bit is as follows: when you're doing training, you see all the tokens at once, because in supervised fine-tuning, you see all the tokens, and you can parallelize over the sequence. In the transformer, the calculation for attention, MLP—the sequence is just a dimension. So it's a big tensor that gets multiplied, and you essentially process all the tokens at once. In inference, you can't do that. You have to generate, because of the autoregressive nature of inference, tokens sequentially—one at a time. So this is the fundamental problem of why inference is a very different workload than training, because you can't parallelize across the sequence dimension. And therefore, it's going to be harder to have high arithmetic intensity or fully utilize the compute.

什么决定了推理的效率？高层级来看是这样的：在训练时，你一次性看到所有token，因为在监督微调中，你看到所有token，并且可以在序列维度上并行。回想一下，在Transformer中，注意力、MLP的计算——序列只是一个维度。所以它是被相乘的一个大张量，你实质上一次性处理所有token。而在推理中，你不能这样做。由于推理的自回归性质，你必须按顺序生成token——一次一个。这就是为什么推理是一种与训练截然不同的工作负载的根本原因：因为你无法在序列维度上并行。因此，要有高算术强度或充分利用算力就变得更加困难。

---

## 4. Lecture Preview / 本讲概览

First, I'm going to do some math to understand the arithmetic intensity and throughput and latency—how to think about that for a transformer. And then I'm going to talk about various techniques to reduce the cost by making the KV cache smaller, quantizing model, pruning, and then finally, I'll talk about speculative decoding, and then some kind of practical concerns. Much of this lecture is based on the scaling book from Google on transformers and inference—I do recommend that people go check it out, it's very nicely written.

首先，我会做一些数学分析，来理解Transformer的算术强度、吞吐量和延迟——如何为Transformer思考这些问题。然后我会讲各种降低成本的技术，包括减小KV缓存、量化模型、剪枝，最后会讲推测解码和一些实际问题。本讲的大部分内容基于Google关于Transformer和推理的Scaling Book——我建议大家都去看看，写得非常好。

---

## 5. Notation and Transformer Block Review / 符号约定与Transformer模块回顾

Just to establish a bit of notation: B is going to be the batch dimension and also the number of sequences. T is going to be the sequence dimension, which is also the number of tokens. D is the model dimension, H is the head dimension. If I take a product between a tensor with dimensions B, T, and D, and another matrix of D and H, I produce B, T, H. The red dimensions are contracting—these dimensions appear in both operands and disappear from the results. Black dimensions appear only in one operand and stay in the result. Blue dimensions are batching dimensions—they appear in both but stay in the result, they do not get contracted or reduced.

先建立一些符号约定：B是批处理维度，也是序列的数量。T是序列维度，也是token的数量。D是模型维度，H是头维度。如果我对一个维度为B×T×D的张量和一个D×H的矩阵做乘法，会产生B×T×H。红色维度是收缩维度——这些维度在两个操作数中都出现，但在结果中消失。黑色维度只出现在一个操作数中并保留在结果中。蓝色维度是批处理维度——它们在两个操作数中都出现且保留在结果中，不被收缩或归约。

Here is the description of a transformer block in all its full glory. You take X, which is the activations of one layer, you feed it through attention, and then you feed it through MLP. You project using a query matrix, a key matrix, and a value matrix. The query matrix is batch times sequence times number of heads times the head dimension. K and V, instead of having N, we have K, which is a potentially smaller number of key-value heads (this is group query attention). Then this is the attention operation, where notice that there's batching dimensions—B appears in both. We'll come back to why this B in both makes inference hard. The MLP is straightforward—you project up with a gating matrix, an up projection, and a down projection.

这是Transformer模块的完整描述。你取X作为某一层的激活值，先通过注意力层，再通过MLP。你用查询矩阵、键矩阵和值矩阵做投影。查询矩阵的维度是批大小×序列×头数×头维度。K和V中，我们不用N，而是用K，即可能更少的键值头数（这就是分组查询注意力）。然后是注意力操作，注意这里有批处理维度——B同时出现在两个操作数中。我们稍后会回到为什么这个B同时出现使推理变得困难。MLP很简单直接——你用门控矩阵、上投影和下投影做计算。

By convention, we assume that in the MLP, the MLP up-projects the D-dimensional model dimension into four times that. So F is always 4D whenever you see F. The model dimension gets split across the N heads: D = N × H (head dimension). The number of heads gets split, in the case of group query attention, into the number of groups and the number of heads per group. Finally, we have two variables, S and T, which both represent the sequence dimension. S is going to represent the number of input tokens, and T is going to represent the number of output tokens. In training time, these two are the same, because we're predicting all the same inputs as outputs. In inference time, T is going to be 1, and S is going to be the input.

按惯例，我们假设MLP将D维的模型维度上投影到四倍——所以你看到F时，认为它是4D。模型维度被分配到N个头上：D = N × H（头维度）。在分组查询注意力的情况下，头数被分为组数和每组的头数。最后，我们有两个变量S和T，都代表序列维度。S代表输入token的数量，T代表输出token的数量。训练时两者相同，因为我们把所有输入都预测为输出。推理时，T等于1，S是输入的长度。

---

## 6. Arithmetic Intensity Review / 算术强度复习

Suppose I'm multiplying two matrices: a B×D matrix and a D×F matrix. B is the batch dimension, D is the model dimension, and F is the projection dimension in the MLP. To compute the arithmetic intensity, I have to count FLOPs and the amount of memory moved. You have to read X from HBM. Storing everything in bf16 (which is the case for inference), we have 2×B×D bytes for X, 2×D×F bytes for W. The number of FLOPs is 2×B×D×F. The total bytes transferred is the sum of reads and writes. Arithmetic intensity is FLOPs divided by bytes transferred—we want this to be high.

假设我乘两个矩阵：一个B×D的矩阵和一个D×F的矩阵。B是批处理维度，D是模型维度，F是MLP中的投影维度。要计算算术强度，我需要数FLOPs和内存移动量。你需要从HBM读取X。推理时一切以bf16存储，X是2×B×D字节，W是2×D×F字节。FLOPs数是2×B×D×F。总传输字节数是读取和写入之和。算术强度是FLOPs除以传输字节数——我们希望这个值很高。

If the batch dimension is much less than D and F, then the intensity simplifies to approximately B. So the upshot is that the arithmetic intensity for matmul, when we have non-square matrices, reduces to the batch dimension. You compare your computation's intensity with your accelerator's intensity. If it's greater, then you're compute bound, which is good. If you're less, then you're memory bound, and that's bad. For H100, for this particular matmul operation, you're compute bound if the batch size is greater than 295. If you just have one example, your arithmetic intensity is going to be 1—this is going to be memory bound. This is basically the workload you'll see in inference: you don't get full matrices, you get very thin matrices or tensors.

如果批处理维度远小于D和F，那么算术强度近似简化为B。概括来说，当我们有非方阵时，矩阵乘法的算术强度归结为批处理维度。你将你的计算强度与加速器的强度进行比较。如果更大，就是计算受限（compute bound），这是好的。如果更小，就是内存受限（memory bound），这不好。对于H100做这个特定的矩阵乘法操作，如果批大小大于295就是计算受限。如果你只有一个样本，算术强度将是1——就会是内存受限。这基本上就是你在推理中看到的工作负载：你没有完整的矩阵，只有非常薄的矩阵或张量。

---

## 7. Naive Inference and the KV Cache / 朴素推理与KV缓存

In naive inference, you have a prompt. The transformer generates keys, values, and activations, and at the end, it generates logits over the output vocabulary. You sample a token, and that token gets concatenated with the prompt, and then you just do this again. This works, but this is really bad because each time you generate one token, you actually take O(T²) time where T is the number of tokens generated so far. Generating T tokens is actually O(T³) because the attention is already O(T²), and you have to do that once for every token.

在朴素推理中，你有一个提示。Transformer生成键、值和激活值，最终生成输出词汇表上的logits。你采样一个token，该token被拼接到提示上，然后你重复这个操作。这能工作，但非常糟糕，因为每生成一个token，你实际花费O(T²)的时间，其中T是到当前为止已生成的token数。生成T个token实际上是O(T³)，因为注意力已经是O(T²)，而你必须对每个token都做一次。

But the observation is that you don't actually have to do this. A lot of the work can actually be shared across prefixes. The tokens you've already seen shouldn't change because it's a causal transformer. If it was bidirectional, then if you attach a token, everything changes. But if it's causal, then the activations here don't change based on any tokens you append. So with that observation, the first obvious thing is to store a KV cache in HBM, so that between successive token generations, you can just reuse the KV cache.

但观察发现你实际上不必这样做。大量工作可以在前缀之间共享。你已见过的token不应改变，因为这是因果（causal）Transformer。如果是双向的，那么每次追加一个token，一切都会改变。但因果Transformer的情况下，这里的激活值不会因为你追加token而改变。基于这个观察，第一个显而易见的优化是将KV缓存（KV cache）存储在HBM中，这样在连续的token生成之间，你只需重用KV缓存。

So there's going to be two stages: prefill and decode. In prefill, you get the prompt, and you populate the KV cache—the set of key and value pairs that the transformer computes. Then you generate the logit and sample a token. In decode/generation, you feed that token through the transformer, which uses this cache and then produces both the distribution of the next tokens and a new KV entry corresponding to the token. The KV cache formula is: for every sequence (B of them), for every token (S of them), and for every layer and every head, you store an H-dimensional vector.

所以推理有两个阶段：预填充（prefill）和解码（decode）。在预填充阶段，你拿到提示，填充KV缓存——即Transformer计算出的键值对集合。然后你生成logit并采样一个token。在解码/生成阶段，你将那个token输入Transformer，Transformer使用这个缓存，然后产生下一个token的分布以及对应这个token的新KV条目。KV缓存的公式是：对每个序列（B个），对每个token（S个），对每一层和每个头，你存储一个H维向量。

In prefill, you can parallelize just like in training because you see the entire prompt—you can compute the KV cache in parallel. And then in generation, you generate the new response tokens sequentially, but at least you don't have to pay for generating the KV cache of the tokens that you already looked at.

在预填充阶段，你可以像训练一样并行计算，因为你看到了整个提示——你可以并行计算KV缓存。然后在生成阶段，你按顺序生成新的回复token，但至少不需要为已经看过的token重新生成KV缓存了。

---

## 8. FLOPs and Memory I/O Analysis / FLOPs与内存I/O分析

### MLP Layers / MLP层

For the MLP layers, the form is: you read X from HBM, you read all the parameters, you compute the up projection and write it to HBM, you compute the gate and write to HBM, and then you compute the down projection and write to HBM. The number of FLOPs depends on B, T, D, and F (batch size, sequence length, model dimension, and feedforward dimension). The arithmetic intensity, assuming B×T is much smaller than D and F, is B×T. An MLP is basically a big matmul. It makes sense because the batch dimension and the sequence length dimension are independent—for the MLP, they don't interact.

对于MLP层，流程是：从HBM读取X，读取所有参数，计算上投影并写回HBM，计算门控并写回HBM，然后计算下投影并写回HBM。FLOPs数量取决于B、T、D和F（批大小、序列长度、模型维度和前馈维度）。假设B×T远小于D和F，算术强度是B×T。MLP本质上就是一个大的矩阵乘法。这很合理，因为批处理维度和序列长度维度是独立的——对于MLP，它们不交互。

In prefill, as long as you make B×T large enough—large batches, long sequences—you'll be fine. In generation, T = 1. You're only generating one token at a time. That means your arithmetic intensity is going to be B. B in generation is the number of concurrent requests. In a batch setting, you can control that. But if you're serving a chatbot, it's the number of concurrent users, which can be high or low, a bit unpredictable, changing over time. This is something we're going to address when we talk about continuous batching. Overall, this is not bad because as long as you have large batches, you should be good.

在预填充阶段，只要B×T足够大——大批量、长序列——就没问题。在生成阶段，T=1。你一次只生成一个token。这意味着你的算术强度将是B。生成时的B是并发请求数。在批量处理场景中，你可以控制它。但如果你在服务一个聊天机器人，B就是并发用户数，可能高也可能低，有些不可预测，随时间变化。这是我们在讲连续批处理时要解决的问题。总的来说，这不算太坏，因为只要你有大批量就行了。

### Attention Layers / 注意力层

In attention, S is the previous tokens already generated, and T is the number of tokens you want to generate logits for. The FLOPs are B×S×T×D. The arithmetic intensity factor for attention is S×T/(S+T). In prefill, when T = S, the prefill intensity is S/2. This is good—as long as you have long sequence lengths for attention, you're going to maintain high arithmetic intensity. Notice that the batching dimension doesn't appear here.

在注意力中，S是已生成的先前token，T是你要为其生成logits的token数。FLOPs是B×S×T×D。注意力的算术强度因子是S×T/(S+T)。在预填充阶段，T=S时，预填充强度是S/2。这很好——只要注意力有长序列，就能保持高算术强度。注意这里批处理维度没有出现。

But for generation, this is bad news. The generation intensity is S/(S+1), which is less than 1, or let's just call it 1. Arithmetic intensity of 1 is bad. We want it to be something like 295 for H100 to saturate the compute. So this is really the bottleneck. Unlike MLPs—where every sequence hits the same MLP weights, and having B be big actually helps because you load the MLP weights once and use them for all your sequences—in attention, each sequence has its own KV cache, so these all depend on B. Increasing B doesn't help. It's like for every sequence, you're basically doing a separate matmul. This blue B in the attention diagram is the cause of why attention's arithmetic intensity doesn't scale with B, and why that is a bottleneck.

但对于生成阶段，这是坏消息。生成阶段的算术强度是S/(S+1)，小于1，我们就当它是1吧。算术强度为1是很糟糕的。我们希望它像H100那样达到约295才能充分利用算力。所以这真的是瓶颈所在。与MLP不同——MLP中每个序列用相同的MLP权重，B变大真的有帮助，因为你加载一次MLP权重就可以用于所有序列——在注意力中，每个序列有自己的KV缓存，所以这些都依赖于B。增加B没有帮助。对于每个序列，你基本上在做一个独立的矩阵乘法。注意力图中这个蓝色的B就是注意力的算术强度不随B缩放的原因，也是它成为瓶颈的原因。

### Summary of Arithmetic Intensity Analysis / 算术强度分析小结

So to summarize: prefill is compute-bound. Generation is memory-bound. Prefill MLP intensity: B×S—great. Prefill attention intensity: S/2—not as good, but workable. Generation MLP intensity: also workable, requires long concurrent requests. But it is really the generation attention intensity which is a fundamental bottleneck. If you're sticking with a transformer, you can't really improve this. So now whenever you hear people say, "Oh, inference is memory bound," you know why.

总结一下：预填充是计算受限的。生成是内存受限的。预填充MLP强度：B×S——很好。预填充注意力强度：S/2——没那么好，但可以接受。生成MLP强度：也可以，需要长并发请求。但真正成为根本瓶颈的是生成阶段的注意力强度。如果你坚持使用Transformer，你无法真正改善这一点。所以以后当你听到人们说"哦，推理是内存受限的"，你就知道为什么了。

---

## 9. Latency, Throughput, and the Trade-off / 延迟、吞吐量及其权衡

Inference is memory bound. In some ways this simplifies things because when we think about how long things take, you just look at how much memory needs to be transferred—assuming you overlap communication and computation, the bottleneck is going to be just the amount of memory you have to deal with. But in other ways, it's frustrating that your accelerators are sitting there not doing anything.

推理是内存受限的。在某种意义上，这简化了事情，因为当我们考虑事情需要多长时间时，你只需要看需要传输多少内存——假设通信和计算是重叠的，瓶颈就是你必须处理的内存量。但在另一种意义上，你的加速器闲着没事干，这很令人沮丧。

Let's walk through an example with Llama 2 13B on an H100. What takes memory? The parameters take memory—we compute the number of parameters and, assuming bf16, parameters take up 2×num_params bytes. Also in memory is the KV cache. The KV cache is: number of tokens in your sequence × number of KV heads × head dimension × number of layers × 2 (for key and value) × 2 (for bf16). The total memory usage is B times the per-sequence KV cache size plus the parameter size. That's the amount of memory you need.

让我们通过一个例子来走一遍——在H100上运行Llama 2 13B。什么占用内存？参数占用内存——我们计算参数数量，假设bf16，参数占用2×参数数量 字节。内存中还存有KV缓存。KV缓存的大小是：序列中的token数×KV头数×头维度×层数×2（键和值）×2（bf16）。总内存使用量是B×每条序列的KV缓存大小+参数大小。这就是你需要的内存量。

What's the latency? The latency is determined by the memory I/O, because inference is memory-bound. Assuming you overlap communication and compute, all the memory shuffling parameters back and forth between HBM and SRAM—that's how long it takes. Throughput is the inverse of latency, but we're generating B tokens in parallel, so throughput is B divided by latency.

延迟由内存I/O决定，因为推理是内存受限的。假设通信和计算重叠，所有内存在HBM和SRAM之间来回搬移参数——这就是耗时。吞吐量是延迟的倒数，但我们并行生成B个token，所以吞吐量等于B除以延迟。

Notice that latency, as you increase B, grows because the KV cache grows. In order to process stuff, you have to copy the KV cache back and forth. Throughput is more interesting because, as you increase B, throughput does improve but up to a limit. Throughput improves because you're amortizing the cost over a larger batch. But the speed at which you're processing is also increasing, so throughput asymptotes—it can't possibly go to infinity.

注意：随着B增加，延迟会增长，因为KV缓存增长了。要处理这些内容，你必须来回复制KV缓存。吞吐量更有意思——随着B增加，吞吐量确实提高，但有一个上限。吞吐量提高是因为你在更大的批次上分摊了成本。但处理速度也在增加，所以吞吐量有渐近线——不可能趋于无穷。

So you just have to remember: latency is a linear function in B, where the constant is the size of the KV cache per sequence multiplied by the bandwidth, plus the parameters. Throughput is proportional to B/(B + something). This leads to a trade-off between latency and throughput: smaller batch sizes yield better latency but worse throughput. Large batch sizes yield better throughput but worse latency. If you want to tune your batch size, that's going to really determine if you want latency or throughput.

所以你只需要记住：延迟是B的线性函数，其中常数项是每条序列KV缓存大小乘以内存带宽，加上参数。吞吐量正比于B/(B+某常数)。这导致了延迟和吞吐量之间的权衡：较小的批大小带来更好的延迟但更差的吞吐量；较大的批大小带来更好的吞吐量但更差的延迟。如果你想调整批大小，那就真的要决定你是要延迟还是要吞吐量。

Increasing batch size worsens the latency because now you have a larger KV cache to read and write. If you're an individual query, you have to wait for everyone to finish—you're waiting for a bus, and the latency is pretty high. Whereas, the throughput of a bus is pretty good because you can move everyone at once. So the throughput improves as batch size increases because the parameters are shared—you load that once into memory and you can process a lot of sequences.

增加批大小会恶化延迟，因为现在你有更大的KV缓存要读写。作为单个查询，你得等所有其他查询都完成——你就像等公交车，延迟很高。而公交车的吞吐量很好，因为你可以一次把所有人都运走。所以吞吐量随批大小增加而提高，因为参数是共享的——你一次性加载到内存中，就可以处理许多序列。

---

## 10. Time to First Token / 首token时间（TTFT）

Time to first token is essentially the time it takes to do prefill, because after you finish prefill, then you can basically start generating. If you want faster TTFT, you should use smaller batch sizes, and you want larger batch sizes to improve throughput.

首token时间（TTFT）本质上是预填充所需的时间，因为预填充完成后你才能开始生成。如果你想要更快的TTFT，应该用较小的批大小；要提升吞吐量，则用较大的批大小。

---

## 11. Reducing the KV Cache / 减小KV缓存

Now that we have a conceptual framework for thinking about how efficient inference is, let's try to make it faster. Memory is the bottleneck for inference, and the KV cache takes up a lot of memory—it could even be larger than the number of parameters for a large enough batch size. So let's just try to reduce the size of the KV cache. You have to be careful about how you do this because you want to make sure you don't lose too much accuracy in the process.

现在我们有了思考推理效率的概念框架，让我们尝试让它更快。内存是推理的瓶颈，而KV缓存占用了大量内存——对于足够大的批大小，它甚至可能比参数数量还大。所以让我们尝试减小KV缓存的大小。你必须小心如何做这件事，因为你不想在这个过程中损失太多精度。

### Grouped Query Attention (GQA) / 分组查询注意力

In multi-headed attention, for every token you have a key, a value, and a query. With grouped query attention, you compute the same number of queries, but you have only a smaller number of groups, and you compute key and value for each group. K is the number of groups. In MHA, K = N—no reduction. In multi-query attention (which no one uses because it's really bad), K = 1. Somewhere in between is hopefully where we find a balance between accuracy and speed.

在多头注意力（MHA）中，每个token有一个键、一个值和一个查询。使用分组查询注意力（GQA）时，你计算同样数量的查询，但只有更少的组数，每组计算一个键和一个值。K是组数。在MHA中，K=N，没有减少。在多查询注意力（没有人用，因为效果很差）中，K=1。希望在这之间的某个地方，我们能在精度和速度之间找到平衡。

GQA reduces the KV cache by a factor of N/K. Reducing memory usage leads to speedup because we're memory-bound. If you reduce the amount of memory, it improves both latency and throughput—it's mainly the batch dimension that creates the tension. Sometimes you play with these parameters jointly: you can reduce the KV cache, but that allows you to increase the batch size and make other trade-offs. The paper shows that for GQA, across a bunch of evals, basically it works well—but always take accuracy values with a grain of salt, because this is for a particular model. Later, the DeepSeek paper should show that it actually does hurt.

GQA将KV缓存减少N/K倍。减少内存使用直接带来加速，因为我们是内存受限的。如果减少了内存，延迟和吞吐量都会改善——主要是批处理维度造成了张力。有时你可以联合调整这些参数：减小KV缓存可以让你增加批大小，从而进行其他权衡。这篇论文显示GQA在各种评估中基本表现良好——但始终要对精度值持保留态度，因为这是针对特定模型的。后来DeepSeek的论文显示它实际上确实有损精度。

### Multi-head Latent Attention (MLA) / 多头隐式注意力

DeepSeek's MLA says: we're going to leave the number of keys and values the same (one for every token essentially), but we're going to compress these. Normally, you compute keys and values by taking your activations and multiplying them by some matrix to get K and V—these are generally N×H dimensions, which is big. MLA says: I'm going to actually project these activations down into C dimensions (DeepSeek-V2 reduced it from 16,000 to 512—quite aggressive compression). Then I compute K and V from this compressed representation. Now, I can just store C—this is much smaller. And when I need my keys and values, I can just materialize them.

DeepSeek的MLA的做法是：保持键和值的数量不变（每个token本质上各一个），但压缩它们。通常，你通过取激活值乘以某个矩阵来计算K和V——这些矩阵通常是N×H维度的，很大。MLA说：我要把这些激活值投影到一个更低的C维空间（DeepSeek-V2将其从16,000降到512——相当激进的压缩）。然后从这个压缩表示中计算K和V。现在，我只需存储C——这要小得多。当我需要键和值时，可以即时将其具体化。

There is one wrinkle: MLA is not compatible with RoPE, which operates directly on the keys and values. So they add additional dimensions for handling the RoPE. But more or less, it's still a pretty big reduction. The latency and throughput improvements follow by just simple math—the smaller the KV cache, the faster you go, almost linear scaling up to some point. The DeepSeek paper shows that MLA works even a little bit better than MHA, while GQA isn't that great.

有一个小问题：MLA与RoPE不兼容，RoPE直接操作键和值。所以他们为处理RoPE增加了额外的维度。但总体而言，仍然是相当大的压缩。延迟和吞吐量的提升直接来自简单的数学——KV缓存越小，速度越快，几乎线性缩放直到某个点。DeepSeek的论文显示MLA甚至比MHA稍微好一点，而GQA则不那么好。

### Cross-Layer Attention (CLA) / 跨层注意力

The idea is that normally, every layer has K's and V's. But let's say instead of doing that, we're just going to compute KVs for a subset of the layers, and then for the other layers, just use the previous layers' KV cache. Just like GQA shares K across heads, now we're sharing KVs across layers. Empirically, this improves the Pareto frontier.

思路是：通常每一层都有自己的K和V。但我们改为只对部分层计算KV，而其他层直接复用前几层的KV缓存。就像GQA在头之间共享K一样，现在我们跨层共享KV。经验表明，这改进了帕累托前沿（Pareto frontier）。

### Local / Sliding Window Attention / 局部/滑动窗口注意力

If you look at the full attention matrix, it's N². Instead of doing that, if you're going to generate a token, you just look at the last K tokens—you essentially have a sliding window. The KV cache is now independent of the sequence length—it's just batch times the other variables, which is great, especially for long context. Because of the number of layers, the effective context length is actually larger than the stated context length because information can propagate farther as you go down the layers. You can also do global plus sliding window where you have attention to a fixed grid of different token points plus a local sliding window.

完整的注意力矩阵是N²。与其这样做，不如每生成一个token只关注最后K个token——你本质上有一个滑动窗口。KV缓存现在与序列长度无关——只是批大小乘以其他变量，这非常好，尤其是对于长上下文。由于有多层，有效上下文长度实际上大于标称上下文长度，因为信息可以随层数向下传播得更远。你也可以做全局加滑动窗口的组合——对固定的不同token网格做注意力，再加上局部滑动窗口。

The problem with this is that it still hurts accuracy—this reduces expressivity. So the solution people come up with is that they interleave local attention with global attention. These hybrid models have full attention for some of the layers and local attention for some of the other layers. You're always trying to balance accuracy with speed.

问题在于这仍然损害精度——减小了表达能力。所以人们想出来的方案是将局部注意力与全局注意力交错。这些混合模型在某些层使用完整注意力，在其他层使用局部注意力。你总是在尝试平衡精度和速度。

The goal of this section is to reduce the KV cache because KV cache is related to memory, and inference is memory-bound—so that directly translates to improvements in throughput and latency. The key is to do this without hurting accuracy. You can do lower dimensional KV caches across layers, across heads, and across head dimension. You can do local attention. You can do linear attention. There's also diffusion models, which is a non-autoregressive way to generate which can be much faster.

本节的目标是减小KV缓存，因为KV缓存与内存相关，而推理是内存受限的——这直接转化为吞吐量和延迟的改善。关键要在不损害精度的前提下做这件事。你可以跨层、跨头、跨头维度做低维KV缓存；可以做局部注意力；可以做线性注意力。还有扩散模型，这是一种非自回归的生成方式，可以快得多。

---

## 12. Quantization / 量化

Quantization is much more of a systems perspective on how to make things smaller. The key idea is to reduce the precision of numbers. Less memory means better latency and throughput. And obviously, you have to worry about accuracy. There are many options from bf16 all the way down to int4.

量化更多是从系统角度来使一切变小。核心思想是降低数字的精度。更少的内存意味着更好的延迟和吞吐量。显然，你需要担心精度。从bf16一直到int4，有很多选项。

If you're scared that quantization is going to mess you up, you can train a model with quantization in mind—this is quantization-aware training. During the feedforward pass during training, you quantize and dequantize, simulating quantization errors as you train. The weights become adapted towards quantization—things will work better. The con is that it requires expensive large-scale training.

如果你担心量化会把模型搞坏，你可以在训练时就考虑量化——这叫做量化感知训练（quantization-aware training）。在训练的前向传播过程中，你量化和反量化，在训练过程中模拟量化误差。这样权重会适应量化——效果会更好。缺点是它需要昂贵的大规模训练。

So what typically people do is post-training quantization—it's much cheaper. The naive way is that for every layer or tensor, you determine the scale and the zero point, and then you quantize that separately. This generally doesn't work as well. You can use GPTQ, which uses some Hessian information to quantize layer by layer, keeping track of errors which get propagated into the non-quantized weights, allowing you to correct for errors. Activation-aware quantization is a more sophisticated approach: the observation is that some activation channels are large, and the weights that interact with those matter more. So allocate more precision to these weights—keep the important channels at higher precision (e.g., fp16), and keep everything else at lower precision (e.g., int3).

所以人们通常做的是训练后量化（post-training quantization）——便宜得多。朴素的方式是对每一层或每个张量确定缩放因子和零点，然后分别量化。这通常效果不太好。你可以用GPTQ，它使用一些Hessian信息逐层量化，追踪传播到未量化权重中的误差，从而进行误差修正。激活感知量化（activation-aware quantization）是一种更复杂的方法：观察发现某些激活通道很大，与这些通道交互的权重更重要，因此为这些权重分配更多精度——保持重要通道在高精度（如fp16），其他通道保持低精度（如int3）。

---

## 13. Pruning / 剪枝

You take a large model, and you rip out pieces of it, and you fix it up. It's a very crude way, but it turns out to work. You first have to estimate the importance of the different parts of the model—you pass inputs through a calibration set and look at the magnitude of the activations. The ones that are large, you want to keep; dead units close to 0 can be removed. Then you remove different hidden units and even layers. Now you have a model that's not going to be very good, so you post-train it—you train it some more on the data or tasks you care about to heal it. This is, in some sense, a training way to reduce model size, where you initialize with parts of a good model. NVIDIA's paper shows they could take a 15B model and reduce it to an 8B model without hurting accuracy too much, and the amount of retraining needed is much less.

你拿一个大模型，从中撕掉一些部分，然后修复它。这是一种非常粗暴的方式，但事实证明有效。你首先需要估计模型不同部分的重要性——将输入通过一个校准集，观察激活值的大小。大的那些你想保留；接近0的死神经元（dead units）可以移除。然后你移除不同的隐藏单元甚至层。现在你有一个不太好的模型了，所以你做后训练（post-train）——在你关心的数据或任务上多训练一会儿来修复它。从某种意义上说，这是一种通过训练来减小模型大小的方法，其中你用好的模型的各个部分来初始化。NVIDIA的论文显示他们能把一个15B的模型缩减到8B，精度损失不大，且所需的再训练量少得多。

---

## 14. Speculative Decoding / 推测解码

So far, we've looked at lossy methods which crunch down the KV cache but could hurt accuracy. Speculative decoding is an elegant way of doing this in a lossless way. Remember that in prefill, you can encode all the tokens in parallel—this is fast, compute-bound, all nice things. In generation, it's one at a time. So checking is faster than generation: if I give you a sequence, it's fast to tell me how good it is, much faster than it is to generate one at a time.

到目前为止，我们看的都是有损方法，它们压缩KV缓存但可能损害精度。推测解码（speculative decoding）是一种优雅的无损方式。记住，在预填充中，你可以并行编码所有token——这很快，是计算受限的，一切都很好。在生成中，一次只能生成一个。所以检查比生成更快：如果我给你一个序列，你快速告诉我它有多好，比一次生成一个token快得多。

You can exploit this asymmetry: use a cheap draft model to generate a few tokens (say four tokens). Then use the target model Q (the model we actually care about) to review these tokens and accept or not accept them. The draft model is smaller and cheaper—even though it's memory-bound and has to generate one at a time, it's not too bad. The target model is big and expensive, but what we're doing is asking it to process a batch of tokens in parallel, so it won't also be too bad.

你可以利用这种不对称性：用一个廉价的草稿模型（draft model）生成几个token（比如四个）。然后用我们真正关心的目标模型Q（target model）来审阅这些token，决定接受还是不接受。草稿模型更小更便宜——即使它是内存受限的，一次只能生成一个token，也不会太糟。目标模型又大又贵，但我们做的是让它并行处理一批token，所以也不会太糟。

The algorithm: sample K tokens from the draft model (p). Then in parallel, compute the logits of these draft tokens using q. Then determine whether to accept: accept with probability min(1, q/p). If q is much larger than p, you're more likely to accept. Otherwise, sample from the residual distribution and exit. This is basically rejection sampling, except that when you reject, you don't get nothing—you're guaranteed to get an exact sample from the target model. Generally, if you have too few draft tokens, you're not leveraging the batching on the target model side. If you have too many, you're going to reject more often. There's a sweet spot around three or four.

算法如下：从草稿模型p采样K个token。然后并行地用q计算这些草稿token的logits。然后决定是否接受：以概率min(1, q/p)接受。如果q远大于p，你更可能接受。否则，从残差分布中采样并退出。这本质上是拒绝采样（rejection sampling），不同之处在于当拒绝时你不是一无所得——你保证从目标模型中得到精确的样本。一般来说，如果草稿token太少，你没能充分利用目标模型侧的批处理。如果太多，你拒绝的频率更高。最佳点大约在三到四个之间。

The draft model is much smaller than the target model, and ideally you want the draft model to be as close to the target as possible—which means you want to distill it. So a lot of the same ideas we talked about (quantization, pruning, etc.) are applicable to speculative decoding as well. If you end up with a reduced model you're happy with, just serve that. If you're not happy with it, it can at least be a draft model, and you can use your main model to fix things up.

草稿模型比目标模型小得多，理想情况下你希望草稿模型尽可能接近目标模型——这意味着你需要蒸馏它。所以我们讲的很多相同的思路（量化、剪枝等）同样适用于推测解码。如果你最终得到了一个满意的缩减模型，直接用它服务。如果你不满意，它至少可以当草稿模型，然后用你的主模型来修正。

---

## 15. Dynamic Workloads and Continuous Batching / 动态工作负载与连续批处理

This is the use case: you're serving a live website, and users come and chat with your model. The requests arrive at different times, have different shared prefixes, and have different lengths. It's far from simple training where you have blocks of the same number of tokens all at once.

这个用例场景是：你在运营一个实时的网站，用户来和你的模型聊天。请求在不同时间到达，有不同的共享前缀，长度也各不相同。这与简单的训练中所有token一次性以相同数量成块出现的情况相去甚远。

There's a system called Orca that introduced the idea of continuous batching. You get a bunch of requests that are jagged because every prefix has a different length. What you do is decode step by step: every step you decode one token for all the sequences. Next step, decode another token. If a sequence ends, you eject it. As new requests arrive, you put them in the batch and continue. That's why it's called continuous batching—the batch is dynamically being updated with finished sequences evicted and new ones coming in.

有一个叫Orca的系统引入了连续批处理（continuous batching）的思想。你收到一堆参差不齐的请求，因为每个前缀的长度不同。你做的就是逐步解码：每一步为所有序列解码一个token。下一步，再解码一个token。如果有序列结束了，就将其移出。当新请求到来时，你把它加入批次，然后继续。这就是为什么叫连续批处理——批次被动态更新：完成的序列被逐出，新的序列加入。

One problem is that batching works when all sequences have the same dimensionality, but requests have different lengths. The solution is selective batching: for attention computation, you can't really share the tensor effectively across different lengths. But for non-attention layers—the MLP layers, which take up a lot of FLOPs—you can actually just concatenate all the sequences together to form a mega-sequence and process that.

一个问题是我们见到的批处理都要求所有序列有相同的维度，但请求长度不同。解决方案是选择性批处理（selective batching）：对于注意力计算，你无法在不同长度之间有效共享张量。但对于非注意力层——MLP层（占用了大量FLOPs），你可以直接将所有序列拼接成一个超长序列，然后一起处理。

### Paged Attention / 分页注意力

Introduced in the vLLM paper. The question is: how is the KV cache stored? When requests come in, you have to put them in memory somewhere. There's a problem of fragmentation—both internal fragmentation (allocating max-token buffers that go unused) and external fragmentation (gaps between requests that are too small to use effectively).

分页注意力在vLLM论文中引入。问题是：KV缓存如何存储？当请求到来时，你必须把它们放在内存中的某个地方。这里存在碎片化问题——既有内部碎片（分配了最大token缓冲区但未使用），也有外部碎片（请求之间的间隙太小而无法有效利用）。

The solution is: let's divide the KV cache of a sequence into non-contiguous blocks. You chunk the sequence into blocks of size (say) 4. It doesn't matter where the blocks go, but they're aligned according to the block. When two requests share the same prefix, they can actually share the same KV cache blocks. In particular, if you have system prompts, you can cache the KV cache of system prompts once, and that can be useful for all the queries. Also, for applications where you have the same prompt and want to generate multiple responses, you can share the KV cache for the prompt and just have unique responses. This uses copy-on-write semantics: when they sample different tokens, you split the block and continue. You're sharing as much of the prefix cache as you can.

解决方案是：将序列的KV缓存划分为不连续的块（blocks）。你把序列切分成大小为4的块。块放在哪里不重要，但它们按块对齐。当两个请求共享相同前缀时，它们可以共享相同的KV缓存块。特别是，如果你有系统提示，你可以缓存系统提示的KV缓存一次，这对所有查询都很有用。此外，对于相同提示但想生成多个回复的场景，你可以共享提示的KV缓存，只保留独特的回复部分。这使用写时复制（copy-on-write）语义：当它们采样出不同的token时，你分裂块然后继续。你尽可能多地共享前缀缓存。

---

## 16. Summary / 总结

Inference is really, really important. It's very different from training—even though it's the same model, you're asking the model to do something very different, and it ends up being very memory-bound. It's also dynamic if you're in a live chatbot use case. We saw a variety of different techniques to improve inference: you can quantize, you can come up with new architectures, you can prune and distill. You can also use speculative sampling. But all of these are driven by the same principle: reduce your KV cache but don't hurt accuracy too much. And then there are ideas from systems like paging and speculative execution that can be brought to bear for live inference servers.

推理真的非常重要。它与训练截然不同——即使模型相同，你让模型做的事情完全不同，最终变得非常内存受限。在实时聊天机器人的用例中，它还是动态的。我们看到了一系列不同的技术来改进推理：你可以量化，可以设计新架构，可以剪枝和蒸馏，也可以用推测采样。但所有这些都受同一个原则驱动：减小KV缓存，但不要过多损害精度。此外还有来自系统领域的想法——如分页和推测执行——可以用于实时推理服务器。

One thing we didn't really get a chance to talk about is that new architectures have huge potential for improvement—things like state space models or linear attention or diffusion. At some level, the KV cache and the way that attention is built fundamentally makes it an inference-unfriendly architecture. So if you can come up with a new architecture that is designed for inference in the way that the transformer was not, this can maybe unlock a lot.

有一个我们真正没有机会深入讨论的话题是：新架构有巨大的改进潜力——比如状态空间模型（state space models）、线性注意力（linear attention）或扩散模型（diffusion）。在某种程度上，KV缓存和注意力的构建方式从根本上使其成为一种对推理不友好的架构。所以，如果你能提出一种为推理而设计的新架构——以Transformer没有的方式来设计——这可能将解锁巨大的可能性。

---

*This translation covers Lecture 10 of Stanford CS336, Spring 2026: "Inference." / 本翻译涵盖斯坦福CS336 2026年春季第十讲："推理"。*
