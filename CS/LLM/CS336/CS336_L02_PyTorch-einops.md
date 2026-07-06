---
title: "Lecture 2: PyTorch (einops)"
---

# Lecture 2: PyTorch (einops) / 第二讲：PyTorch (einops)

## 1. Opening Announcements / 开场通告

I hope everyone is staying dry. I'm not. So as I mentioned last time, the Marin project had a 1e23 FLOPs run which was running, and it finished. And it actually matched the forecast. Each of these curves is essentially an IsoFLOPs curve, which is a bunch of smaller model runs. And you try to find the compute optimal point. You fit a scaling law. And this was the point where we predicted the loss, and we ran the model and it got loss within 0.05. So I thought that was pretty cool. And if you extrapolate out to GPT-5 level performance, this is the loss you get. Of course, your mileage might vary depending on how these scaling laws behave. OK, I just wanted to share that news.

希望大家都没有淋湿。我反正是淋湿了。如我上次所说，Marin 项目有一次 1e23 FLOPs(浮点运算次数) 的运行，现在已经完成了。而且它确实与预测吻合。这些曲线本质上都是 IsoFLOPs 曲线，每一个都是一堆较小模型的运行结果。你试图找到计算最优(compute optimal)的那一点，拟合一条缩放定律(scaling law)。我们在那个点上预测了损失(loss)，然后跑了模型，结果偏差在 0.05 以内。我觉得这相当酷。如果进一步外推到 GPT-5 级别的性能，你可以看到对应的损失。当然具体表现还取决于这些缩放定律的走势。好吧，我只是分享一下这个好消息。

So last lecture I gave an overview of the entire class. And we talked about tokenization, which is going to be on the first assignment. Today, I want to talk about resource accounting, which is going to be more on the systems side of things. To recall, the main thing we're trying to do is train the best model we can given a finite set of resources, which could be compute, memory, sometimes data. But that's not really going to be a limiting factor for us in this class. And our goal is simply to maximize the computational efficiency of our training. So before you can optimize the computational efficiency, we need to understand the efficiency of a given computation. And for that, we need to understand the compute and memory characteristics.

上一讲我概述了整个课程的内容。我们还讨论了分词(tokenization)，这将是第一次作业的内容。今天我想谈谈资源核算(resource accounting)，这更多是系统层面的事情。回顾一下，我们的主要目标是在给定的有限资源下训练出最好的模型，这些资源包括计算力(compute)、内存(memory)，有时也包括数据(data)。不过在课程中数据不会成为限制因素。我们的目标仅仅是最大化训练的计算效率。在优化计算效率之前，我们需要先理解给定计算过程的效率。为此，我们需要理解计算和内存的特性。

Just to give you a taste of the type of questions you will hopefully be able to answer by the end of the class, here's a question. How long would it take to train a 70 billion parameter model on 15 trillion tokens on 1024 H100s? Well, there's a formula, which we'll talk about — you can get the number of FLOPs to be 6 times the number of parameters times the number of tokens. We can look up the spec sheet to see how fast the H100 is. We have this thing called MFU, which we'll talk about, say 0.5. Then you can estimate the number of FLOPs that you need and compare what the hardware gives you per day. And then you can compute the number of days. So the number of days is 143. Here's another question. What's the largest model you can train on H100s using AdamW? You can look at it: H100s have 80 gigabytes of HBM memory, and the number of bytes per parameter, which is 2 plus 2 plus 4 plus 4. We'll explain where that comes from. And then the number of parameters you can get is going to be about 53 billion. So there's some caveats here that we don't count the activations which depend on batch size and the sequence length. So this is all very rough back-of-the-envelope calculations. But hopefully by the end of this class you'll understand where these come from. And the point is not to precisely calculate every single thing, but just get the rough shape of things.

举几个例子让你们感受一下，希望到课程结束时你们能回答这些问题。第一个问题：在 1024 块 H100 上训练一个 700 亿参数(parameter)的模型、训练 15 万亿个 token，需要多长时间？答案是有一个公式，我们回头会讲——FLOPs(浮点运算次数) 等于 6 乘以参数数量再乘以 token 数量。我们可以查一下规格表看看 H100 有多快。我们还有一个叫做 MFU(模型FLOP利用率) 的东西，回头会讲，取值约 0.5。然后你可以估算你需要的 FLOPs，以及硬件每天能提供多少 FLOPs。一除就能算出天数，答案是 143 天。另一个问题：在 H100 上用 AdamW 能训练的**最大**模型是多少？你可以这样算：H100 有 80 GB 的 HBM(高带宽内存)，每个参数占用 2+2+4+4 个字节（我们会解释这个的由来）。算下来的参数量大约是 530 亿。当然这里有一些注意事项，我们没有计入激活值(activations)的存储，这些取决于批次大小(batch size)和序列长度(sequence length)。所以这些全都是非常粗略的草稿级估算。希望到课程结束的时候你们能理解这些数字从何而来。重点不是精确计算每一个细节，而是对大致规模有个感觉。

OK. So last time I talked about knowledge and what you can take away from this class — mechanics, which are how things work. So today, that would be pretty straightforward. The mechanics are just how PyTorch works, how tensors work. It should be fairly — there's no magic here. The mindset I want to impart on you is that resource accounting is going to be very crucial. And I want everyone to get in the habit: whenever you write a line of code, think about the performance characteristics. And then finally, intuitions. Here we're just going to get a sense of the resources, how they're spent. There's going to be no ML magic today. I'll leave that to Tatsu for the next lecture.

上一讲我谈了知识以及对这门课能学到什么——机制(mechanics)，也就是事物如何运作。今天的内容比较直接。机制就是 PyTorch 如何工作、张量(tensor)如何工作。这没什么魔法。我想传达给你们的思维模式是：资源核算将会非常关键。我希望大家养成一个习惯：每写一行代码，就去思考它的性能特征。最后是直觉(intuitions)。今天我们只是感受一下资源是如何被消耗的。今天不会有机器学习的魔法，这些留给 Tatsu 下一讲。

## 2. Tensors: The Building Blocks / 张量：基本构造单元

So let's start bottom up and start building up. What is at the bottom? At the bottom are tensors. Tensors are the building block of storing everything. If you have parameters, gradients, optimizer states, data, activations — everything essentially is a tensor. So for example, you can take a look at the DeepSeek 3.2 model. And you see that the model itself is a bunch of different tensors. Each tensor has some shape and also some precision, which I'll talk about later. And so as you know, tensors subsume vectors, matrices, and can generalize to any number of entities.

让我们从底层开始，自下而上地构建。底层是什么？底层是张量(tensor)。张量是存储一切事物的基本构造单元。无论是参数(parameters)、梯度(gradients)、优化器状态(optimizer states)、数据(data)、激活值(activations)——本质上一切东西都是张量。比如你可以看看 DeepSeek 3.2 的模型，你会发现模型本身就是一大堆不同的张量。每个张量都有某种形状(shape)和某种精度(precision)，这个后面再讲。如你所知，张量包含了向量(vectors)、矩阵(matrices)，并且可以推广到任意数量的维度。

OK. So let's talk about how much tensors take to store. It depends on the type of tensor. In general, we're going to be dealing with tensors that store floating point, but tensors can also store integers and other types. So for floating point, typically whenever you talk about float, I think the standard people refer to as float32. So a float32, if you break it down, has 32 bits. One of the bits is a sign, 8 bits are the exponent, which gives you dynamic range. And the rest is the mantissa or the fraction, which gives you variation. This is also known as fp32 or single precision. And the term single precision comes from the fact that back in the day when you were doing scientific computing, float32 was like a baseline. If someone gave you a float, you would expect it to be at least single precision. And if you want more precision, then you can get double precision — that's float64. But in deep learning, we're going the other way, because even 32 bits is a lot. And the types of computations that we want to do don't demand the high precision that some kinds of numeric simulations do.

好，那么我们来谈谈张量占用多少存储空间。这取决于张量的类型。通常我们处理的是存储浮点数(floating point)的张量，但张量也可以存储整数(integers)及其他类型。对于浮点数，一般人们说的 float 指的是 float32。如果你细看 float32，它有 32 个比特(bit)：1 个比特是符号位(sign)，8 个比特是指数(exponent)，提供动态范围(dynamic range)；其余的是尾数(mantissa)或小数部分(fraction)，提供精度变化。这也叫 fp32 或单精度(single precision)。"单精度"这个术语的由来是，当年做科学计算时，float32 就像是一个基准。如果有人给你一个 float，你至少会期望它是单精度的。如果你想要更高精度，那就用双精度(double precision)，即 float64。但在深度学习领域，我们往反方向走，因为即使 32 比特也太多了。我们要做的这种计算并不需要像某些数值模拟那样的高精度。

So let's construct a 4 by 8 matrix. By default, the type of tensor you create is float32. So if you want something else, you should declare it. And the memory usage is just the number of elements times the element size here, which is 4 bytes for a 32-bit number. And that's going to be 128 bytes. So just to give you a kind of perspective, in GPT-3, which is a fairly old model, one of the matrices in the feedforward layer is about 2.3 gigabytes. So these tensors can get quite big. And this is not even the biggest one that one can imagine.

我们来构造一个 4×8 的矩阵。默认情况下，在 PyTorch 中创建的张量类型是 float32。如果你想要别的类型，需要显式声明。内存使用量就是元素个数乘以每个元素的体积——32 比特即 4 个字节。所以这里是 128 字节。给你一个更直观的感受：GPT-3 这个已经比较老的模型中，前馈层(feedforward layer)中的一个矩阵就有大约 2.3 GB。所以这些张量可以变得非常庞大，而这还不是你能想象到的最大的。

## 3. Numerical Precision / 数值精度

Since we're interested in efficiency, we want to generally reduce the amount of storage. And we'll see that as you reduce the precision, you actually save memory. And you also save time because operating on 16 bits is going to be faster — let's say, twice as fast — but not always, it depends. And then by reducing memory, we'll see later that actually reducing memory can save time as well, which is maybe less obvious. But it will hopefully become clear.

既然我们对效率感兴趣，通常我们想要减少存储量。你会看到，当你降低精度时，不仅能节省内存，还能节省时间——因为操作 16 比特比 32 比特更快——大概快一倍，但不总是如此，要看情况。而且通过减少内存使用，后面我们会看到，减少内存实际上也可以节省时间，这或许不那么显而易见，但希望后面会变得清晰。

So the obvious thing is you say, OK, let's take away half the bits. Now you have float16. So float16 says you have a sign. You have only 5 bits of exponent, and then the rest is the mantissa. So float16 is good, except for its dynamic range is poor. So even if you try to construct a 1e-8 tensor, that is actually just 0. So you can't really represent very big numbers, and you can't represent very small numbers. And the reason is that this exponent has only 5 bits compared to 8. So if you train with fp16, which people did back in the day, you will get instability. You will get underflow. You get overflow. You'll get NaNs. It's pretty challenging.

最直接的做法是：好，那我们把比特数减半，就得到了 float16。float16 有 1 个符号位，只有 5 个比特的指数位，其余是尾数。float16 不错，但它的动态范围很差。比如你试图构造一个 1e-8 的张量，结果它其实就是 0。你无法表示很大的数，也无法表示很小的数。原因是指数位只有 5 个比特，而 float32 有 8 个。所以如果你用 fp16 训练——以前人们确实这样做——你会遇到不稳定性：下溢(underflow)、上溢(overflow)，还会出现 NaN(非数值)。这是相当困难的。

So bfloat16 was invented. This was developed in 2018 to address this issue. And the observation was that well, let's not compromise on the number of bits. The number of bits is going to be the same as fp16. But we're going to shift some of the bits from the mantissa to the exponent. So that means it has more dynamic range than float16. And it actually has the same dynamic range as float32. But of course, the resolution is worse because there's no free lunch here. But it turns out that in a lot of deep learning applications, this is well worth the trade-off. You want the dynamic range to not overflow and underflow. And because things are kind of sloppy and stochastic anyway, you don't need that much resolution.

于是 bfloat16(bf16) 被发明了。这是 2018 年开发的，专门为了解决这个问题。其观察是：我们不减少比特总数——总比特数和 fp16 一样——但我们把部分比特从尾数移到指数。这意味着它比 float16 有更大的动态范围，而且实际上和 float32 的动态范围一样大。当然，分辨率(resolution)就变差了——天下没有免费的午餐。但在很多深度学习应用中，这个取舍非常值得：你希望动态范围足够大，以避免溢出和下溢；而由于训练过程中本来就是吵吵闹闹、随机的，你其实不需要那么高的分辨率。

So to summarize, what are the implications for training? You can absolutely train with float32. And if you're training a small model, you probably just — you don't want to worry about it, just float32 is fine. But it requires 4 bytes of memory per float. And that can take up a lot of memory. And if you train with float16, then that's going to be too risky. So bf16 is the sweet spot. Even bf16 can be risky as well, maybe a little bit. One thing that people have — that has become common practice is to use mixed precision training.

总结一下，这对训练有什么影响？你当然可以用 float32 来训练。如果只是训练一个小模型，你大概不想操心这事儿，用 float32 就挺好。但每个浮点数要 4 字节内存，这可能会占用大量内存。如果直接用 float16 训练，那又太冒险。所以 bf16 是甜点(sweet spot)。即便如此，bf16 可能也会有一点点风险。一个已经变得相当普遍的做法是使用混合精度训练(mixed precision training)。

So mixed precision training is where some of the computations use some precision, and other computations use other precision. So in general, as a general rule, bf16 is what you would use for parameters, activations, and gradients. And for optimizer states, you would use fp32. And we'll discuss a little bit more about that later. And to invoke mixed precision training, PyTorch has an AMP library. We're not going to talk too much about this, but you basically wrap your code, and the library takes care of it automatically for you in the sense that it tries to cast things into bf16 when it's safe. So, for example, MatMuls are generally safe. But if you try to do exponentiation, then it will try to leave things as fp32.

混合精度训练指的是：某些计算用某种精度，另一些计算用另一种精度。一般来说，参数(parameters)、激活值(activations)和梯度(gradients)用 bf16；而优化器状态(optimizer states)用 fp32。我们稍后会再多讨论一些。要使用混合精度训练，PyTorch 有一个 AMP 库(Automatic Mixed Precision)。我们不会深入讲太多，但基本做法是把代码包装起来，然后这个库会自动处理——它会在安全的情况下把量转换为 bf16。例如，矩阵乘法(MatMuls)通常是安全的。但如果你要做指数运算(exponentiation)，它会尽量保持 fp32。

OK. So we could do bf16 — I think this is probably where this class will end. But if you're feeling very adventurous, you can go farther. So fp8, this was introduced four years ago. It actually has been standardized. If you look at fp8, there's actually two versions because depending on if you need more dynamic range or more resolution. And there's two versions of them. And so we're not going to talk about that. But NVIDIA has some — the transformer engine supports fp8. And most recently, you can actually go down to fp4. So last year, NVIDIA developed nvfp4, and there's only 4 bits per value. So if you just — so we're on the same page. 4 bits is not a lot. I can write all the values down on a single line here between minus 6 and 6. So that's not very much precision.

好，本课程大概就用 bf16 到头了。不过如果你非常有冒险精神，可以走得更远。fp8 是四年前引入的，已经标准化了。fp8 其实有两个版本，取决于你需要更大的动态范围还是更高的分辨率。这个我们不展开。NVIDIA 的 Transformer Engine 支持 fp8。更近的是，你可以降到 fp4。去年 NVIDIA 开发了 nvfp4，每个值只有 4 个比特。4 个比特真的不多——我可以把所有可能的值写在一条线上，范围从 -6 到 6。所以精度确实很低。

Now there's a little bit of a cheat here. Because if you just naively only use these values, you're not going to be able to train very well. So what actually this means is that every value you can have this 4 bits of freedom, but there are blocks. And each block can be scaled up and down accordingly. So you can actually represent more values but you can't represent the full dynamic range for every single value. And there is a model released actually this year, the Nemotron 3 Super, which was trained in fp4, which I think is pretty cool.

不过这里有一点"作弊"的成分。如果你单纯地只用这 4 个比特来表示值，训练效果会非常差。实际的做法是：每个值拥有这 4 个比特的自由度，但有分块(blocks)的存在，每个块可以按比例缩放。因此你实际上可以表示更多的值，但无法让每个单独的值都拥有完整的动态范围。今年确实发布了一个模型叫 Nemotron 3 Super，是用 fp4 训练的，我觉得挺酷的。

OK. So some of this is just good to know. And some of this you can't even touch. It's not like you create a tensor and you call it fp4 — you can make it fp4. A lot of this is done under the hood by NVIDIA's software stack.

好，有些只是需要了解一下，有些甚至碰都碰不到。这不像你创建一个张量然后说它是 fp4 —— 你虽然可以创建它，但很多相关的工作是在 NVIDIA 软件栈底层完成的。

## 4. Memory and Moving Tensors / 内存与张量迁移

OK. So we talked about tensors. And the memory calculus is pretty simple — just the number of elements times however much memory each element takes up. By default, the tensors you create in PyTorch are going to be on CPU. And of course, you have to — if you want things to go fast, you want to move them to GPU. But just remember to do that. Otherwise you won't get your speed-ups.

好，我们谈完了张量。内存计算相当简单——就是元素数量乘以每个元素占用的内存大小。默认情况下，你在 PyTorch 中创建的张量是在 CPU 上的。当然，如果你想要计算加速，就需要把它们移到 GPU 上。一定要记得这样做，否则你得不到加速效果。

OK, so we talked about memory of tensors, which is very straightforward. Now let's talk about computing with tensors.

好，我们已经讨论了张量的内存占用，这很简单直接。接下来让我们谈谈如何用张量进行计算。

## 5. einops: Named Dimension Tensor Operations / einops：命名维度张量操作

So before talking about FLOPs accounting for the tensor operations, let's take a little bit of a digression to talk about einops. The motivation behind einops is that it's very easy to mess up. I find it very confusing to look at code with transpose(-2, -1) and you're trying to figure out what minus 2 and minus 1 is. And so this is maybe the motivation for using variable names rather than indices. So einops is a library for manipulating tensors where the dimensions are named. And this is inspired by Einstein summation notation. There's a nice tutorial which you can go through. I'm just going to cover some of the basics.

在讨论张量操作的 FLOPs 核算之前，我们先稍微岔开一下，谈谈 einops。einops 的动机是：用传统的索引方式很容易搞错。我觉得看类似 `transpose(-2, -1)` 这样的代码很令人困惑——你得去想 -2 和 -1 到底是什么。这就是用变量名替代索引的动机。einops 是一个通过命名维度(named dimensions)来操作张量的库，灵感来自爱因斯坦求和约定(Einstein summation notation)。有一个不错的教程可以参考，这里我只覆盖一些基础。

So basically, the way to think about einsum is a generalized matrix multiplication with good bookkeeping. So here's an example. I have a 3 by 4 matrix. I have a 4 by 3 matrix. And if I do the MatMul, this is actually pretty nice. It's pretty easy to understand. In einops, basically you say x has two dimensions, the row and the column, which I'm going to name seq1 and hidden. I'm going to have y. That's a matrix which has also rows and columns, which I'm going to name hidden and seq2. And I'm going to produce a tensor — or here a matrix — where the dimensions are indexed by seq1 and seq2. And anything that is not mentioned here, the hidden gets summed out. So the way this works is I'm going to sum over — enumerate over all possible values of all the variables that occur here, which are seq1, hidden, and seq2. And I'm going to basically index into x, index into y, multiply them and accumulate them into the result z sub seq1 and seq2.

基本上，对待 einsum 的方式是把它看作一种带良好记账能力的广义矩阵乘法。举个例子：假设我有一个 3×4 的矩阵 x，和一个 4×3 的矩阵 y。普通的 MatMul 其实也很清晰、很容易理解。在 einops 中，你说 x 有两个维度——行和列，我分别命名为 seq1 和 hidden。y 也是一个矩阵，也有行和列，我命名为 hidden 和 seq2。然后我生成一个张量——这里是一个矩阵——维度索引为 seq1 和 seq2。所有没有被提到的东西——hidden——就被求和消去了。具体运作方式是：枚举所有变量（seq1、hidden、seq2）的所有可能取值，在 x 中取对应元素，在 y 中取对应元素，相乘，然后累加到结果 z_{seq1, seq2} 中。

OK. So you say this is — come on. This is much easier than all those transposes, right? Let's try a more complicated example. Now we have a tensor, 2 by 3 by 4, another tensor 2 by 3 by 4. And if I were doing things the old way, basically what I'm doing is transposing these last two. And then because MatMul implicitly batches the dimensions that are not the MatMul dimensions, then you get the answer. So you have to reason about this a bit. Einops makes this very clear. It says there's a batch dimension. There's seq1 hidden, seq2 hidden. And I'm just going to produce batch, seq1, and seq2. And notice that there's no transpose because in some sense I've done the transpose by the naming.

你可能会说，这当然比那些转置(transposes)容易多了。来试一个更复杂的例子。现在有一个 2×3×4 的张量，另一个 2×3×4 的张量。如果用传统方式，我需要转置最后两个维度，然后用 MatMul（它会隐式地对非 MatMul 维度做批次处理），最后得到答案。你需要费点心思来推理这个过程。而 einops 让一切非常清晰：有一个批次(batch)维度，然后是 seq1、hidden 和 seq2、hidden。我只需要生成 batch、seq1、seq2。注意这里没有出现转置——从某种意义上说，命名本身就已经完成了转置。

If you want to get fancy, you can say, well, batch — I'm just going to replace with dot dot dot. And this means that if I had, let's say, a rank-10 tensor with eight different batching dimensions, I can just write dot dot dot without enumerating all of them. And this comes up in language modeling because you might have a batch dimension, you might have a sequence dimension, you might have a head dimension. And you're trying to do this matrix operation for all of them. And the nice thing is that you can write modular code where you can write this dot dot dot without worrying about even the shape of the tensor that comes in.

如果你想更灵活一点，可以用 `...`（三个点）来代替代众多维度。如果我有一个秩为 10、有八个批次维度的张量，我可以直接写 `...` 而不用一一列举。这在语言建模(language modeling)中很常见——你可能有一个批次维度、一个序列(sequence)维度、一个头(head)维度——你需要对所有这些维度做矩阵运算。好处是你可以写出模块化代码，用 `...` 而不必担心中途进来的张量到底是什么形状。

All right. So that's einsum which is in the einops library. There's also reduce. This is a generalization of sum, mean, max, and min. For example, if you have a tensor and you want to sum according to dim minus 1, which means sum along the last dimension. Again, I don't like this notation. But what you can do is call reduce. And basically what you say is that there's some batching dimensions — in this case, it would be these first two. And then there's some hidden dimension which doesn't appear on the right side, which means that it gets summed. And here I put sum, which means that the aggregation operation is sum. But you can replace it with mean or max or min.

好，以上是 einops 库中的 einsum。此外还有 reduce，它是 sum、mean、max、min 的泛化。比如你有一个张量，你想按最后一维求和(`dim=-1`)。我个人不喜欢这种写法。但你可以用 `reduce`：说有一些批次维度（这里就是前两个），然后有一个 hidden 维度不出现在等号右边，意味它被求和了。这里我写的是 `sum`，即聚合操作为求和，但你也可以换成 mean、max 或 min。

Is there some speed-up to this? This basically reduces to the same type of primitive operations. You can think about it as just sugar. So it should be the same.

这东西会更快吗？它实际上归结为同样的底层原语操作——你完全可以把它看作语法糖。所以性能应该一样。

So the final thing I'll talk about is rearrange. This is, I think, a pretty powerful tool. I think it will come up in an assignment once. So sometimes you have a dimension that actually represents two dimensions, and you want to operate on one of them. The reason this happens is that sometimes you have a matrix and you flatten it. And then you want to maybe unflatten and flatten. So imagine I have a 3 by 8 matrix where this dimension 8 actually represents a 2 by 4 matrix. So I want to multiply that 2 by 4 matrix by a 4 by 4 matrix. So what I'm going to do is call rearrange. And what I am doing here is saying, look, this is some number of batch dimensions, which here just corresponds to the first element. And then here, I use parentheses to say that this h actually represents the product of heads and hidden1. I have to — obviously there's multiple ways to decompose this. It could be 2 by 4, 4 by 2. So I said the number of heads is 2, which means that hidden1 is 4. And then I can break that up into two dimensions, heads and hidden. Then you can perform your operation transformation on w. And this is what we've seen before: a standard MatMul where there's some number of batching dimensions for x, and this is hidden times hidden by hidden2. And then once you've done that transformation, you can rearrange it back. This is straightforward. You basically look at two dimensions, and then you can group them into one dimension.

最后要讲的是 rearrange。这是我认为非常强大的一个工具，作业中应该会用到的。有时一个维度实际上代表两个维度的乘积，而你只希望对其中的子维度做操作。这种情况通常是因为你先 flatten 了一个矩阵，然后又想 unflatten 回来。设想我有一个 3×8 的矩阵，其中 8 这一维实际上代表一个 2×4 的矩阵。我想把那个 2×4 的矩阵和一个 4×4 的矩阵相乘。我要调用 `rearrange`：这里有一些批次维度（对应第一个元素），然后我用括号表示：h 这个维度实际上是 heads 和 hidden1 的乘积。当然分解方式有多种——可以是 2×4，也可以是 4×2。我说 heads 是 2，那 hidden1 就是 4。这样就能拆成两个维度：heads 和 hidden。然后你可以对 w 执行变换——这就是之前见过的标准 MatMul，x 有一些批次维度，这里是 hidden 乘 hidden2。变换完成后，你可以再 `rearrange` 回去。这很直接：看着两个维度，把它们合并成一个维度。

So sometimes I find it takes a bit of time to get used to it, but it's well worth it because once you have einsum, you just think in a different way. And all the transposes and reductions — all that — just becomes more fluid. You have to think through these more bespoke primitives.

我发现适应 einops 需要一点时间，但非常值得。一旦你会用 einsum，你的思维方式就不同了。所有那些转置和归约操作都变得更加流畅，你不需要再费力去想那些量身定制的原语操作。

## 6. FLOPs Accounting and MFU / FLOPs 核算与MFU

So now let's return back to the resource accounting question. I have tensors. We've talked about how they take memory. So how much compute do they take? The thing we're going to use to measure computation cost is the number of FLOPs. A FLOP is a floating-point operation. And we're going to assume it's a basic operation like addition or multiplication. So now there's other things that GPUs can do. But for the most part, we're just going to ignore them because these are the bread and butter, and are going to eat up most of your time.

现在让我们回到资源核算的问题。我们有张量，并讨论了它们如何占用内存。那么它们需要多少计算？我们衡量计算开销的指标是 FLOPs(浮点运算次数)。一个 FLOP 是一个浮点操作(floating-point operation)，我们假设它是加法或乘法这样的基本操作。当然 GPU 还能做其他运算，但大部分情况下我们忽略不计，因为这些是最主要、最消耗时间的运算。

So one thing that is a pet peeve is that if I say the word FLOPs, it's actually ambiguous what I mean. So there's FLOPs, which is saying the number of floating-point operations, usually written FLOPs with a lowercase s. This is a measured amount of computation done. And then there's FLOP/s, which is floating-point operations per second. Sometimes it's also very confusingly written as FLOPS with uppercase S. I'm going to always write /s to make it clear that this is measuring the speed of hardware. So if you go and see that H100s have 989 teraflops, it's the second. And when I say that GPT-3 took 325 or whatever it is FLOPs, that's the former.

有一件让我有点烦的事：当我说"FLOPs"这个词的时候，意思其实是模糊的。有两种含义：一种是 FLOPs（小写 s），表示浮点运算的总次数，衡量的是计算量；另一种是 FLOP/s（每秒浮点运算次数），有时也会令人困惑地写成大写 S 的 FLOPS。我会始终写 `/s` 来明确表示这是衡量硬件速度的单位。所以当你在规格表上看到 H100 有 989 TFLOPS，那是每秒的。当我说 GPT-3 消耗了约 325 什么什么的 FLOPs，那是总量。

So just to give you an order of magnitude. The number of FLOPs when I talk about 1e22 or 1e23 or 1e25, these are referring implicitly to the amount of compute or the scale of some of these models. And so if you look at H100s — there is a spec sheet and I'll tell you that for bf16, the number of FLOP/s is 1979. And then you go and you benchmark it, and it's like wait a minute, that's not actually what I'm getting. And then you go read the fine print. And there's a footnote that says this is with sparsity. For dense, divide by 2. So you always have to take these numbers and divide by 2. So that's why you see these divide by 2.

给你一个数量级的感受。当我提到 1e22 或 1e23 或 1e25 FLOPs 时，这些指的是某些模型的计算量或规模。如果你看 H100 的规格表——对于 bf16，FLOP/s 的数值是 1979 TFLOPS。但你自己去跑基准测试(benchmark)时，会发现"等一下，我怎么得不到这个数？" 然后你去看小字注释：这是**有稀疏性(sparsity)** 的情况。对于密集(dense)矩阵，要除以 2。所以你总是要把这个数除以 2。这就是为什么你会看到除以 2 的操作。

So this allows us to — just for intuition, if you have 8 H100s for two weeks. That's 8 times the number of seconds in two weeks times the number of FLOPs you get per second. So that's about 5e21. OK. So this is just building intuition for the number of FLOPs that certain types of hardware have and how many FLOPs certain types of models require. It's nothing fancy. It's just math and napkin math.

这让我们能建立一个直觉：8 块 H100 跑两周，那就是 8 ×（两周的秒数）× 每秒 FLOPs 数。大概是 5e21 FLOPs。这仅仅是在帮你建立对硬件和模型所需 FLOPs 规模的直觉，不是什么深奥的东西，就是数学和草稿纸算术罢了。

So suppose you have a linear model. It turns out that a lot of this calculus of counting FLOPs is actually going to be at the core — it's like linear MatMuls. So you have n points. Each point is d-dimensional. And we're going to map each of these d-dimensional vectors to a k-dimensional output. So B is going to be the number of points. D is the number of input dimensions, and K is the number of output dimensions. So let's construct some x, which is the data matrix B by D. The weight matrix is D by K. And when you do the MatMul, the question is how many FLOPs that is. And it turns out that this is going to be 2 times basically the product of all the three dimensions. And the way to see that is that we have one multiplication for each triple and then also one addition. So there's D minus 1 additions, but let's ignore that.

假设你有一个线性模型(linear model)。FLOPs 计数的大多数核心运算都是线性 MatMul 形式的。你有 n 个数据点，每个点是 d 维的，我们要把每个 d 维向量映射为 k 维输出。记 B 为数据点数量，D 为输入维度数，K 为输出维度数。构造数据矩阵 x(B×D)，权重矩阵 w(D×K)。做 MatMul 时，问题是有多少 FLOPs？答案是 2 × B × D × K。推理方式：每个 (b,d,k) 三元组有一次乘法和一次加法。加法少一次（是 D-1 次），但忽略这个细节。

So what about the FLOPs of other operations? Elementwise operations are just the size of a matrix. I think that's fairly clear. So addition also requires m n FLOPs. So in general, no other operation you'll encounter is as expensive as matrix multiplication for large enough matrices. So in general, we're just going to focus on what MatMuls are doing, with the important caveat of when we talk about memory.

其他运算的 FLOPs 呢？逐元素(elementwise)运算就是矩阵的大小，这很直观。加法也消耗 m×n 个 FLOPs。总的来说，对于足够大的矩阵，没有其他运算能比矩阵乘法更昂贵。所以通常我们只关注 MatMul 在做什么，当然在讨论内存时会有重要的补充说明。

So you can think about this MatMul as B is the number of data points. And D times K is the number of parameters. Remember x is B by D and w is D by K. So another way to think about this formula is that the number of FLOPs in order to do a forward pass of this linear matrix is actually 2 times the number of tokens or data points times the number of parameters. So it turns out that this actually generalizes to transformers, which if you remember the 6 times n times d formula, we can see the shape of that forming.

你可以这样理解 MatMul：B 是数据点的数量，D×K 是参数数量（x 是 B×D，w 是 D×K）。另一种思考这个公式的方式是：做一次前向传播(forward pass)所需的 FLOPs，等于 2 × token数量（或数据点数量）× 参数数量。这实际上可以推广到 Transformer 中。如果你还记得那个 6ND 公式，我们已经能看到它的雏形了。

Now the question is, how long does it actually take on hardware? So one way to find out is you just time it. So in general, when you time especially on GPU, you have to call cuda synchronize to make sure that — because the GPU is running asynchronously, you want to make sure that you have this synchronization point. And then you perform the operation. And after the operation, then you also have to have the synchronization barrier. If you omit this, you're going to find that wow, your timings are really fast. And that's because this is a non-blocking call. It just returns. And often it's general good practice to try this multiple times and take the average.

那么实际上在硬件上要花多长时间呢？方法之一就是计时。在 GPU 上计时的时候，一般需要先调用 `cuda.synchronize()` — 因为 GPU 是异步(async)运行的，你需要确保有一个同步点(synchronization point)。然后执行操作，操作完成后还需要一个同步屏障(synchronization barrier)。如果你省略这一步，你会觉得"哇，速度超级快"——但那只是因为这个调用是非阻塞(non-blocking)的，它直接返回了。通常好的做法是多次运行取平均值。

So the actual FLOPs per second is basically the number of FLOPs you did divided by the time that you recorded on your hardware. And so remember, there's also another number, which is the GPU has a spec sheet that gives you some number of FLOPs — which was 989 teraflops. And so in general, the number of actual FLOPs per second is going to be different from the promised FLOPs per second.

所以实际的 FLOP/s 就是你完成的 FLOPs 数量除以你在硬件上记录的时间。还记得吗，规格表上也有一个数——H100 号称 989 TFLOPS。通常，实际的 FLOP/s 和标称的 FLOP/s 是不一样的。

And the way to directly think about the discrepancy is something called Model FLOPs Utilization, or MFU. And the definition of MFU is the actual FLOPs per second divided by the promised FLOPs per second. And here this is ignoring the communication and other overhead. So in general, it's rare that you get more than what was promised. Often you get less. And in general, if you get about MFU of 0.5 for modern models, you should be pretty happy with yourself. If you have just like a straight up MatMul, you can get maybe potentially like 0.8 even, but you usually can't get that high. And sometimes if something's really wrong, you'll get something like 0.1, which means that you should do something.

直接衡量这种差异的指标叫做 MFU(模型FLOP利用率，Model FLOPs Utilization)。MFU 的定义是：实际 FLOP/s 除以标称 FLOP/s，这里忽略通信和其他开销。通常你几乎不可能得到超过标称值的性能，一般都是更少。对于现代模型，如果你能达到约 0.5 的 MFU，就可以相当满意了。如果你只是做一个简单的 MatMul，或许能达到 0.8 甚至更高，但一般达不到那么高。如果出了大问题，MFU 可能只有 0.1，那就说明你需要去排查问题了。

OK. So whenever you write your model, you can calculate the MFU through a combination of counting the number of logical FLOPs that your model needs to do, and then looking at the wall clock time and essentially dividing.

所以当你写模型的时候，你可以通过两步来计算 MFU：先计算模型需要执行的逻辑 FLOPs 数量，然后除以壁钟时间(wall clock time)对应的 FLOP/s。

## 7. Arithmetic Intensity and Roofline Analysis / 算术强度与屋顶线分析

To go back to the question of why MFU is 0.5, I'm going to have to introduce this idea of arithmetic intensity. And the reason is that, well, it's not just doing a bunch of MatMuls and then you're done. This is my very cartoon version of what hardware looks like. You have high bandwidth memory (HBM). And then you have where the compute cores are — the accelerator chips. And then how do you compute? Well, you have to send your inputs — your matrices, the tensors — from the memory to the accelerator. You do the computation, and then you send it back. So if you want to measure how long this takes, this depends on two things. One is the accelerator speed, which is what we've talked about just now. But the other thing that matters is the memory bandwidth of your hardware, which we haven't talked about. And if you look at the spec sheet, the FLOP/s was 1979e12 divided by 2. And the bytes per second, which is the memory bandwidth, is 3.3 terabytes per second. And remember why we were looking at memory — how much things took to store. Most obviously, if you have a model that's too big it doesn't fit in your memory, that's not going to be fun. But also it turns out that memory — you need to move this memory, which takes time. So actually the size of how large things are actually influences speed as well.

回到"为什么 MFU 是 0.5"这个问题，我需要引入算术强度(arithmetic intensity)的概念。原因在于，事情不是单纯堆砌 MatMul 就能了事的。这是我画的硬件卡通图：你有 HBM(高带宽内存)，还有计算核心——加速器芯片。如何计算呢？你必须把输入——矩阵、张量——从内存发送到加速器，执行计算，再把结果送回内存。如果要衡量这个过程的耗时，取决于两项因素。一项是加速器的速度，这个我们刚才已经讨论了。另一项也很关键，就是硬件的内存带宽(memory bandwidth)，我们还没谈到。看规格表，FLOP/s 是 1979×10¹² / 2，而内存带宽是每秒 3.3 TB。还记得我们为什么关注内存吗？最明显的是：如果一个模型太大了，放不进内存，那就麻烦了。但另外一点是：你需要搬运这些内存数据，这是需要时间的。所以东西有多大，实际上也会影响速度。

OK, so suppose I have a million-dimensional vector of bf16. And I'm going to just compute a ReLU on this. So remember ReLU is just max of x and 0, done elementwise on the entire vector. I count two things: one is the number of bytes that were moved. I have to read x in — copy it into the accelerators. Each of this is going to be 2 bytes because bf16 is 2 bytes per float times n floats. So that's 2n. And then I'm going to write y back. So that's another 2n. OK. So that's the number of bytes that have to be moved. And then how many FLOPs were done? Well, each of these elements, I'm just comparing it with zero, and that's it. So that's n comparisons. So now I look at the communication time, which is the number of bytes that I needed to move divided by the speed of that movement. And that gives me the time. And what about the computation time? That's the FLOPs divided by FLOPs per second. There's also going to be another important assumption which generally we try to hold: that we overlap communication and computation. The idea is that we don't sit here waiting for the things to move. As soon as they're there, we start computing them, and then we move them back. So this movement and the compute is happening at the same time. So mathematically, we're just going to assume that the total time is the max of the two, because we're going to assume that we can perfectly overlap them. In practice, it's not going to be perfectly overlapped. There's going to be some overhead. But this is good enough for now.

假设我有一个 100 万维的 bf16 向量，对它计算 ReLU。ReLU 就是 `max(x, 0)`，逐元素操作。我数两样东西：一是搬运的字节数——我必须把 x 读进加速器，每个元素 2 字节（bf16），那就是 2n；然后写回 y，又是 2n。总共搬运 4n 个字节。二是做了多少 FLOPs？每个元素只是和 0 做一次比较，共 n 次比较。现在看通信时间：需要移动的字节数除以带宽速度，得到通信时间。计算时间呢？用 FLOPs 除以 FLOP/s。还有一个重要假设，也是我们通常尝试做到的：通信(communication)和计算(computation)重叠(overlap)。意思是我们不坐在那里干等数据搬运完毕——数据一到就开始计算，算完就往回搬。所以数据传输和计算是同时发生的。数学上，我们假设总时间是这两者的**最大值**，因为我们假设它们能完美重叠。实践上做不到完美重叠，会有一些开销，但这样近似目前足够了。

So if you ask what is the bottleneck here? When the communication time is greater than the computation time, then we call the algorithm memory bound, because you're spending most of your time just waiting for bits to show up. And when the computation time is greater than the communication time, that's compute bound, because then your bottleneck is actually doing the compute.

那么瓶颈在哪？当通信时间大于计算时间，我们称该算法为**内存受限(memory bound)** 的，因为你大部分时间都在等数据到齐。当计算时间大于通信时间，就是**计算受限(compute bound)** 的，因为瓶颈在于实际的计算。

Now this is where I'm going to define intensity. What is the intensity of an accelerator? It is essentially how much work can the accelerator do per byte transferred. For any given accelerator, based on the spec sheet, you basically have FLOP/s divided by bytes per second. How much useful work can you do per byte that's moved? For an H100, that's 295. So that means for every byte, you can do 295 floating point operations. That's an intuitive number to have in your head — about 300.

这里我要定义**强度(intensity)**。加速器的强度本质上是加速器每传输一个字节能完成多少工作。对于任意一款给定的加速器，根据规格表，你拿 FLOP/s 除以 bytes/s 即可。每传输一个字节能做多少有用的工作？对于 H100 来说，这个值是 295——意味着每传输一个字节，你可以做 295 次浮点运算。这是一个值得记住的直观数字，大约 300 左右。

So now the arithmetic intensity of an algorithm is how much actual work was done per byte for this workload. And if you look at it for the ReLU computation, it's FLOPs over bytes and it's 0.25. So the point is that it's very small.

一个算法的算术强度(arithmetic intensity)是该工作负载下每字节传输所完成的实际工作（FLOPs/bytes）。对于 ReLU，它是 0.25——非常小。

So now we can talk about bottlenecks through the language of intensity. Something is memory bound if the arithmetic intensity is smaller than the accelerator intensity, and compute bound if it's greater than accelerator intensity. These are equivalent.

现在我们可以用强度的语言来讨论瓶颈。如果算法的算术强度小于加速器强度，则是内存受限的；如果大于，则是计算受限的。

So one way to think about increasing arithmetic intensity is that let's just try to do more stuff per unit of byte moved. So the GELU is another activation. It has some formula that doesn't have zeros. If you do this calculation, the number of bytes moved back and forth is still 2n plus 2n. And the FLOPs here is about 20 FLOPs per elementwise scalar operation, so it's 20n. So the arithmetic intensity is, let's say, 5. This is a crude estimate. And in this case, are we memory bound or compute bound? Memory bound, because 5 is still smaller than 295, way smaller. So even though GELU does a lot of work, more work than ReLU, in the way that things are structured, it's still memory bound. Which means that if you were just computing ReLU and GELU, you might think GELU is so complicated, it must be really expensive. But actually it's exactly the same, because that's not where the bottleneck is.

提高算术强度的一种思路就是尽量在每字节传输上做更多事。GELU 是另一种激活函数，它的公式更复杂一些。计算搬运的字节数仍然是 2n+2n，而 FLOPs 大约每个元素 20 次运算，总计 20n。算术强度大约是 5。这算内存受限还是计算受限呢？内存受限，因为 5 仍然远小于 295。所以虽然 GELU 比 ReLU 做了更多运算，但从计算结构来看它仍然是内存受限的。这意味着如果你只盯着 ReLU 和 GELU，你可能会觉得"GELU 这么复杂，肯定很贵"。但实际上耗时是一样的，因为瓶颈不在计算上。

So what about a dot product? You have vector x, vector w, size n, and you take the dot product. How many bytes are moved? Read x: 2n; read w: 2n; write y, which is a scalar: 2. The number of FLOPs is n multiplications and n minus 1 additions. So that's 2n minus 1. The arithmetic intensity is about half, which is also pretty bad. It's memory bound.

点积(dot product)呢？向量 x 和向量 w 各有 n 个元素，做点积。搬运字节数：读 x(2n) + 读 w(2n) + 写 y（标量，2 字节）。FLOPs：n 次乘法和 n-1 次加法，共 2n-1。算术强度大约是 0.5——同样很糟糕，也是内存受限。

So what about a matrix vector product? I have x which is a vector. w is an n by n matrix. And you form this product. I'm going to read x: 2n; read w: 2n squared; and write y: 2n. And the number of FLOPs is basically you're doing n dot products. So that's n times the cost of doing a dot product. And the arithmetic intensity is barely, barely higher. So this is also memory bound.

矩阵-向量乘积(matrix-vector product)呢？x 是向量，w 是 n×n 矩阵。读 x(2n)，读 w(2n²)，写 y(2n)。FLOPs 相当于 n 次点积。算术强度稍微高一点而已——也仍然是内存受限的。

So now let's talk about matrix multiplication. This is where things get interesting. I have an n by m matrix, another m by n matrix. And I multiply them. The number of bytes moved is 2n² plus 2n² (for reading) and then 2n² bytes written back. And the number of FLOPs is n squared dot products. And what's arithmetic intensity? It's about 340. And in general, it's roughly n over 3. And intuitively this makes sense because you're sending n² things, but you're computing n³ things. So the number of things you're computing over the number of things you're sending is order n. And this gets better the larger you make the matrices. So in general, this is why when you hear people talk about, "oh, we need to make large batch sizes or have large matrices," it's exactly this. If you're under the accelerator intensity, making things smaller doesn't actually speed things up. It's all the same. Whereas if you get to a point where you're over this, then you're actually saturating your GPUs. OK. So finally, this is compute bound.

现在来谈矩阵乘法(matrix multiplication)——这是变得有趣的地方。我有一个 n×m 矩阵，另一个 m×n 矩阵，将它们相乘。搬运的字节数：读入 2n²+2n²，写回 2n²。FLOPs：n² 个点积。算术强度呢？约 340（大体是 n/3）。直觉上这很合理：你传输的是 n² 量级的数据，但计算的是 n³ 量级的运算。所以计算量除以传输量是 O(n) 量级的。矩阵越大，效率越高。这就是为什么你经常听到人说需要大批次(batch size)或大矩阵——原因就在于此。如果低于加速器强度，把矩阵变小并不会真正加速，耗时是一样的。而一旦超过这个阈值，你就在真正地饱和(saturate) GPU 的计算能力了。所以，终于，矩阵乘法是**计算受限**的。

OK. So as long as we have large matrices, we're actually pretty good. We're in a compute bound saturating the accelerator. And the question earlier about what about transformers? Well, it turns out we'll see in both your assignment, but also in the next lecture, that transformers are essentially big matrix multiplications with some things sprinkled in between. So that's good news from arithmetic intensity. And this is, by design, transformer is designed in a certain way to have high arithmetic intensity. And one comment here, just to foreshadow the inference lecture, is that matrix vector products is essentially what goes on when you're doing transformer inference. Because inference, you're generating one token at a time. And so it's like a vector that you're trying to dot product with a matrix. And that's as we saw memory bound. Whereas at training time, you get this whole sequence and you're processing all at once.

所以只要我们有足够大的矩阵，局面就很好——我们是计算受限的，正在饱和加速器。之前有人问 Transformer 的情况如何？实际上，你们会在作业和下一讲中看到，Transformer 本质上就是大矩阵乘法加上一些夹杂在中间的小操作。这对算术强度来说是个好消息。这是刻意设计的——Transformer 被设计成了具有高算术强度。顺便提一句，为后面推理课做铺垫：当你在做 Transformer 推理(inference)时，本质上就是在做矩阵-向量乘积——因为推理是逐个 token 生成的。这就是用一个向量和矩阵做点积，而如我们所见，那属于内存受限。相比之下，在训练(training)时，你有一整条序列可以一次性处理。

So also to tie it to the other question about MFU, and the reason you might be getting low MFU is that you might be doing — so MFU is actual over promise. So if you have really large memory bottlenecks, then you're not actually going to get very good throughput, even though the promise is if you didn't have memory bottlenecks, you were just going through and doing all the computations of your model.

这也顺便回答了之前关于 MFU 的问题——你拿到低 MFU 的原因可能是：MFU 是实际值除以标称值。如果你的确有很大的内存瓶颈，那就不会得到很好的吞吐量(throughput)。而标称值是在假设没有内存瓶颈、完全畅快地做计���的前提下给出的。

OK. Final thing on arithmetic intensity — roofline plots. So there's a nice way to visualize the relationship between arithmetic intensity and performance. This plot basically plots arithmetic intensity on the x-axis. So every slice here corresponds to a particular algorithm. And then we have these lines here. And each of these lines corresponds to a particular accelerator, maybe H100 or B200. And then on the y-axis is the FLOPs per second that are realized. So if your algorithm has low arithmetic intensity, like ReLU or dot products, you're going to be over here, which means that the FLOPs per second realized is going to be not as high as your peak accelerator. And as you increase the arithmetic intensity, things are going to be better. You're going to be able to saturate your hardware up until a certain point. And after a certain point you're compute bound. And obviously you can't exceed the peak FLOPs.

最后，关于算术强度的屋顶线分析(roofline analysis)。这是一种优雅的可视化方式。x 轴是算术强度，不同的竖线对应不同的算法；y 轴是实际达到的 FLOP/s。曲线对应不同的加速器，比如 H100 或 B200。如果算法算术强度很低（如 ReLU 或点积），你就落在图中靠左的区域，意味着你实现的 FLOP/s 远低于加速器峰值。随着算术强度提高，情况会变好，你能逐渐饱和硬件，直到进入计算受限区域。当然了，你不可能超过峰值 FLOPs。

## 8. Compute and Memory in Training / 训练中的计算与内存

OK. So now I'm going to go back and talk about memory and compute for the operations that we need in training. So far we've done tensor operations, basically MatMuls. And we saw how much memory it took and how much compute it took and the interaction between them. So now let's actually think about what it takes to train.

好，现在回到训练所需运算的内存和计算。到目前为止我们讨论了张量运算——主要是 MatMul——以及它们的内存占用、计算量和二者之间的交互关系。现在让我们来真正思考训练需要什么。

Here is our running example — a deep network. I'm going to consider a case where I have an input, which is a B by D input, and a number of layers where each layer is a D by D MatMul. And then that produces some set of preactivations and then elementwise ReLU that produces some activations of the first layer. And then this is repeated again and again. And the output is just going to be the same size. So when you run the model on the batch of data, what we're doing is we're going through the layers, and each layer we basically apply the linear transformation and then a pointwise ReLU activation. And then we do that for all the layers.

这是一个深度网络(deep network)的例子。输入 B×D，每一层是一个 D×D 的 MatMul，产生一组预激活值(preactivations)，再经过逐元素 ReLU 产生激活值(activations)。这样一层层重复下去，输出尺寸相同。当你在批次数据上运行模型时，就是逐层应用线性变换和逐点 ReLU 激活。

So now let's talk about gradients. Let's use an even simpler example — a simple linear model regression. So we have a vector 1, 2, 3, a weight vector 1, 1, 1. And we take the dot product, and we form this MSE loss. And what happens when we do the backward pass is that each of the variables involved in this computation graph has a gradient that is either set or not set. So w.grad gets set to 1, 2, 3. This is just basic mechanics of PyTorch.

现在谈梯度(gradients)。用一个更简单的例子：线性回归模型。向量 [1, 2, 3]，权重向量 [1, 1, 1]，做点积然后算 MSE 损失(loss)。做反向传播(backward pass)时，计算图中每个参与变量都会有一个梯度被设置或不被设置。比如 w.grad 被设为 [1, 2, 3]。这都是 PyTorch 的基本机制。

So now the question is, how much compute do gradients take? Let's count FLOPs for computing gradients. Let's take a simplified model where you have x, which is B by D, times w1 matrix (ignoring ReLU for simplicity), times w2, which is the same shape, D by D matrix. The first thing you do in this linear network is you take x(B×D), take w1(D×D), and you get h1(B×D). Then h2 takes h1 and w2, same story. These are just MatMuls. Then you form a loss.

那么梯度需要多少计算？我们来数一下梯度的 FLOPs。简化模型：x(B×D) 乘以 w1(D×D)（先忽略 ReLU），再乘以同样为 D×D 的 w2。第一步，x 乘 w1 得 h1；第二步，h1 乘 w2 得 h2。都是 MatMul。然后计算损失。

So what happens in the backward pass? You take backward on the loss. And the question is, how many floating point operations was that? Let's zoom in on one layer. The second layer takes h1 and just multiplies it by matrix w2 to get h2. So if you look at the FLOPs in the forward pass, this is just a MatMul. In the backward pass, if you remember your chain rule and backprop algorithm, you have to compute two things. You have to compute the backward message, the gradient of the loss with respect to your input — dℓ/dh₁. And you also have to compute the gradient with respect to your parameters — dℓ/dw₂. What do those gradients look like? dℓ/dh₁ = (dℓ/dh₂) × w₂, and dℓ/dw₂ = h₁ × (dℓ/dh₂). These are both MatMuls. But the nice thing is that if you just look at this, we know how expensive this is. The number of FLOPs is essentially the product of all the dimensions. It doesn't matter which ones you're batching or not. The way that you aggregate is different, but the FLOPs is the same.

反向传播中发生了什么？对于一个具体的层：前向是将 h1 乘以 w2 得到 h2，FLOPs 就是 MatMul 的量。反向传播（根据链式法则和反向传播算法）需要计算两个东西：对输入的梯度 dℓ/dh₁，以及对参数 w2 的梯度 dℓ/dw₂。在 einsum 记号下，dℓ/dh₁ = dℓ/dh₂ × w₂，dℓ/dw₂ = h₁ × dℓ/dh₂。注意到这很好：两种梯度的 FLOPs 本质上都是所有维度尺寸的乘积——无论哪些维度是批次维度，归约方式可能不同，但 FLOPs 是一样的。

OK. So notice that the backward pass is exactly twice as expensive as the forward pass. And this is because you have to compute two gradients — one with respect to the parameters, and then one with respect to the input, the other thing that's not the parameter.

所以注意：反向传播的 FLOPs 恰好是前向传播的两倍。因为你需要计算两种梯度：一个是关于参数的，一个是关于输入的（即另一个不是参数的东西）。

And you put it all together, the forward pass is 2 times the number of data points (B) times the number of parameters FLOPs. And the backward pass is twice of that, which is 4 times the number of data points times the number of parameters FLOPs. And so the grand total is 2 plus 4 is 6, so 6 times the number of data points and parameters. So this is where the 6ND formula comes from that you might have seen in various places. It's just by counting forward and backward. So we did this for just deep networks. But it turns out that this is actually a good approximation for transformers as well — as long as the context length isn't too large. If the context length is too large, then you get the context length squared term, and that's more FLOPs that isn't in this kind of accounting.

合在一起看：前向传播的 FLOPs = 2 × 数据点数(B) × 参数数量；反向传播是前向的两倍，即 4 × 数据点数 × 参数数量。总计：2 + 4 = 6，即 6 × 数据点数 × 参数数量（即著名的 6ND 公式）。这就是 6ND 公式的由来。我们只在一个简单深度网络上推了这个公式，但它对 Transformer 也是一个相当好的近似——前提是上下文长度(context length)不太大。如果上下文长度太大，则会出现上下文长度的平方项，那部分 FLOPs 不在这个核算之内。

## 9. Optimizer States and Memory Usage / 优化器状态与内存使用

OK. So let's talk a bit about — now we have gradients. Now the other piece when you do training is we have to do optimization. So I'm going to use the AdaGrad optimizer, which is from 2011. This predates Adam. It's somewhere in between SGD and Adam. Basically it's SGD where you look at the second moments of the gradient (momentum looks at the first moment gradients, and Adam combines the two of them).

好，现在我们有梯度了。训练的另一个环节是优化(optimization)。我用 AdaGrad 优化器作为例子，这是 2011 年的算法，比 Adam 更早出现，可以看作介于 SGD 和 Adam 之间的方法。简单说就是在 SGD 的基础上加入了梯度的二阶矩(second moment)——动量法看的是梯度的**一**阶矩，Adam 则把两者结合起来。

When you compute the gradients and then take an optimizer step, if you're defining a new optimizer — in assignment 1, you're going to implement Adam — for each of the parameter groups (in this case w1 or w2), there's something called optimizer state, which is storage that the optimizer uses while it's running. And what we're computing in AdaGrad is the sum of the squared gradients. We're getting it from the optimizer state, updating it with the current gradient, and storing it back. And then after you update the g², then you update the parameters — you basically divide by the square root of the sum of gradient squared.

当你计算梯度然后执行优化步骤时，你需要对每个参数组(parameter group)维护优化器状态(optimizer state) ——这是优化器运行期间使用的额外存储。在 AdaGrad 中，维护的是梯度平方的累加和。从优化器状态取出，用当前梯度更新，再存回去。然后更新参数——本质上就是除以梯度平方和的平方根。

So now let's look at how much memory the optimizer is using. Or in general what is the memory usage? For parameters in this network, there's D² parameters per each of the L layers. And each parameter takes 2 bytes if we're storing it in fp16 (bf16). That's the parameter memory. Activations — this is 2 times (for bf16) batch size times D times number of layers. For every layer you have activation. You have gradients which is basically a copy of all the parameters, also bf16. And the optimizer state — for AdaGrad, we have 4 bytes per parameter for storing the optimizer state (fp32). Adam — you store the first order bit and the second order moments, so that's 8 bytes per parameter. So if you think about it, the optimizer state is actually a lot of the memory used.

现在来看看优化器消耗了多少内存，以及整体内存使用情况。参数(parameters)：D² × L 个参数，用 bf16 存的话每个参数 2 字节。激活值(activations)：2（bf16）× 批次大小 × D × 层数，因为每一层都有激活值。梯度(gradients)：基本上是所有参数的一份拷贝，也是 bf16。优化器状态(optimizer state)：AdaGrad 每个参数 4 字节（fp32 存储），因为通常出于数值稳定性考虑用 fp32 存优化器状态。如果用 bf16 存，算平方和累积多步会不稳定。Adam 需要存一阶和二阶矩，那就是每个参数 8 字节。所以如果你想一想，优化器状态实际上占据了相当大比例的内存。

One note is that memory serves two purposes. One is you have to store this thing in your HBM. But the other thing is that it has to be shipped to the accelerators. And in general, the optimizer state is not really the bottleneck for compute. So the amount of memory here is not really so important for performance in terms of speed, but it means that you can't fit large models in your memory.

值得注意的一点：内存有两个作用。一是你需要把数据存在 HBM 中；二是你还需要把它传送到加速器。通常优化器状态并不是计算的瓶颈。所以这些内存量对速度性能没那么重要，但它决定了你能否把大模型塞进内存。

## 10. Gradient Accumulation and Activation Checkpointing / 梯度累积与激活检查点

Two things I want to quickly touch on before we conclude. One is that as we see, memory does have an important effect both on the ability to store large models, but also sometimes on your speed. And so in general, you want to reduce your memory usage. So there's two things that people typically do. One is gradient accumulation. So in general, you want to use batch sizes that are large enough to improve stability up to a critical batch size, which Tatsu will talk about later. And as we saw, activation memory scales with batch size. So you might run out of memory at some point if you have too large batch sizes. So gradient accumulation says, well, you compute — you have these micro batches, and you compute the gradient on the micro batches. And then you just accumulate the gradients. You don't zero out the gradients. And every (batch size / micro batch size) steps, you update the parameters and zero out the gradients. OK, so this is actually a very simple code change which allows you to save on memory.

在结束之前想再快速讲两件事。第一，我们看到内存确实对存储大模型以及速度有重要影响。所以总体上我们想减少内存使用。人们通常会做两件事。一个是梯度累积(gradient accumulation)。通常你需要批次足够大以提高训练稳定性，直到一个临界批次大小(critical batch size)，Tatsu 后面会讲。但激活值内存随批次大小线性增长——批次太大时你会内存溢出。梯度累积的做法是：用微批次(micro batches)分别计算梯度，然后累加(accumulate)，不清零。每（总批次/微批次）步才更新一次参数并清零。这是一个非常简单的代码改动，就能节省内存。

The other thing I'll quickly mention is activation checkpointing. In training, we need to store in general the activations of all the layers. This is done by default. Interestingly, for inference we don't need to compute the gradient, so we only need to store the current layer's activations. But for training, the memory usage is B × D × 2 × L. And the question is, can you reduce this? So activation checkpointing, also known as gradient checkpointing or rematerialization — the key idea here is that in the forward pass, you just keep activations for only a subset of the layers. And in the backward pass, you recompute the missing activations from the last checkpoint. That's why it's called checkpointing. And this is a general trick that you see in systems — trade off: if you want to reduce memory, you can just recompute things. So this means that if you store all the activations, you have the thing that's pre the ReLU and the thing that's after the ReLU. That's a lot of storage. Instead if you do activation checkpointing on those blocks where each block has a linear and ReLU, you don't store the pre-ReLU, and you save basically half. You can get away with half the memory. And then when you're doing the backward pass, you need the gradient, but you can compute it easily from the stored activation.

另一个是激活检查点(activation checkpointing)，也叫梯度检查点(gradient checkpointing)或重物化(rematerialization)。关键思想是：前向传播只保留部分层的激活值；反向传播时再从最近的检查点(checkpoint)重新计算缺失的激活值。这是系统层面的一个通用技巧——以计算换内存。你本来存了所有 ReLU 前后的激活值，现在用检查点技术，只需存 ReLU 后的一半，内存砍半。反向传播需要梯度时可以方便地从存着的激活值算出来。

You can go further than this. You can say, well, I can store all the layers, but in the extreme case, I can just store no layers. And so that will be maximally memory efficient. The only thing is that the compute is going to be L², because for every one of these layers, you have to start from the beginning. And maybe a sweet spot is if you store the checkpoints at √L layers — that means your activation memory is √L, and your recomputation overhead is also √L. So that's balanced.

你可以走得更极端——不存任何层。内存效率最高，但计算量会变成 L²（因为每一层都要从头计算）。一个甜点是每隔 √L 层存一个检查点——激活值内存 O(√L)，重计算开销也是 O(√L)，取得平衡。

## 11. Summary / 总结

OK. So to summarize this lecture, everything is operating on tensors — parameters, gradients, activations, optimization states, data. We introduced einops, which hopefully you can embrace as a way to think about tensor operations. 6 times number of data points times number of parameters is a formula which now we have demystified as the number of FLOPs per training step. And then we talked about arithmetic intensity and roofline analysis, which allows us to diagnose whether a computation is memory bound or compute bound. Matrix multiplications are compute bound. Basically everything else is memory bound. And then finally, gradient accumulation and activation checkpointing are ways to reduce the memory. And by reducing the memory, that allows you to use bigger batch sizes. OK. So that's it for today's lecture. Next week, Tatsu will talk about architectures.

总结本讲：一切都是在张量上操作——参数、梯度、激活值、优化器状态、数据。我们引入了 einops，希望大家能接受它作为思考张量运算的一种方式。6 × 数据点数 × 参数数 这个公式——我们现在已经解密了，它就是一个训练步(training step)所需的 FLOPs。然后我们讨论了算术强度(arithmetic intensity)和屋顶线分析(roofline analysis)，这使我们能够诊断一个计算是内存受限(memory bound)还是计算受限(compute bound)的。矩阵乘法是计算受限的，其他几乎所有运算都是内存受限的。最后，梯度累积(gradient accumulation)和激活检查点(activation checkpointing)是减少内存的方法——减少内存能让你使用更大的批次数。以上就是今天的内容。下周 Tatsu 会讲架构(architectures)。
