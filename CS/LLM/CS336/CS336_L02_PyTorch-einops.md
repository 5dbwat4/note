---
title: "Lecture 2: PyTorch (einops)"
---


# Lecture 2: PyTorch (einops) / 第二讲：PyTorch（einops）

---

I hope everyone is staying dry. I'm not. So as I mentioned last time, the Marin project had a 1e23 FLOPs which was running, and it finished. And it actually matched the forecast. So remember we were running this. Each of these curves is essentially IsoFLOPs curve, which is a bunch of smaller model runs. And you try to find the compute optimal point. You fit a scaling law. And this was the point where we predicted the loss, and we ran the model and it got loss within 0.05. So I thought that was pretty cool. And if you extrapolate out to GPT-5 level performance, this is the loss you get. Of course, your mileage might vary depending on how these scaling loss are. OK, I just wanted to share that news.

我希望大家都没被雨淋到——虽然我自己被淋了。正如上次提到的，Marin 项目的 1e23 FLOPs 一直在运行，现在已经完成了，而且实际结果与预测相符。还记得我们之前做的这些运行吧。每条曲线本质上都是一条 IsoFLOPs 曲线，由一系列小模型运行组成。你试图找到计算最优（compute optimal）点，拟合一条缩放定律（scaling law），然后在这个点上我们预测了损失值。我们运行了模型，实际损失与预测相差在 0.05 以内。我觉得这很酷。如果你外推到 GPT-5 级别的性能，这就是你得到的损失。当然，具体效果可能因这些缩放损失的具体情况而异。好了，我只是想分享一下这个消息。

---

So last lecture I gave an overview of the entire class. And we are talking about tokenization, which is going to be on the first assignment. Today, I want to talk about resource accounting, which is going to be more on the systems side of things. So to recall, the main thing we're trying to do is train the best model we can given a finite set of resources, which could be compute, memory, sometimes data. But that's not really going to be a limiting factor for us in this class. And our goal is simply to maximize the computational efficiency of our training.

上一讲我给出了整个课程的概述，我们讨论了分词（tokenization），这将出现在第一次作业中。今天我想讨论的是**资源核算**（resource accounting），这更偏向系统方面。回顾一下，我们要做的主要事情是：在给定的有限资源下训练尽可能好的模型——这些资源可能是计算资源、内存，有时也包括数据。但数据在本课程中不会成为我们的限制因素。我们的目标很简单：**最大化训练的计算效率**。

---

So before you can optimize the computational efficiency, we need to understand the efficiency of a given computation. And for that, we need to understand the compute and memory characteristics. Just to give you a taste of the type of questions you will hopefully be able to answer by the end of the class, so here's a question. How long would it take to train a 70 billion parameter model on 15 trillion tokens on 1024-- actually, this should be H100. So how do you answer that? Well, there's a formula, which we'll talk about how you can get the number of FLOPs to be 6 times the number of parameters times the number of tokens. We can look up the spec sheet to see how fast the H100 is. We have this thing which called MFU, which we'll talk about 0.5. Then you can estimate the number of FLOPs that you need that the hardware gives you per day. And then you can compute the number of days. So the number of days is 143. Here's another question. What's the largest model you can train on H100s using AdamW? So you can look at, well, H100s have 80 gigabytes of each VM memory, the number of bytes per parameter, which is 2 plus 2 plus 4 plus 4. We'll explain where that comes from. And then the number of parameters is that you can get is going to be about 53 billion. So there's some caveats here that we don't count the activations which depends on batch size and the sequence length. So this is all very rough back-of-the-envelope calculations. But hopefully by the end of this class you'll understand where these come from. And the point is not to precisely calculate every single thing, but just get the rough shape of things.

所以在优化计算效率之前，我们需要理解给定计算的效率。为此，我们需要理解计算和内存的特征。为了让大家感受一下在本课程结束时你希望能够回答什么样的问题，这里有几个问题。在 1024 块 H100 上用 15 万亿个标记（tokens）训练一个 700 亿参数的模型需要多长时间？怎么回答呢？有一个公式——我们会讨论如何得出 FLOPs 数量为 6 倍参数数量乘以标记数量。我们可以查规格表看 H100 有多快。我们还有一个叫做 MFU（模型 FLOP 利用率）的东西，大概是 0.5。然后你可以估算你需要的 FLOPs 数以及硬件每天能提供的 FLOPs，最后算出天数——答案是 143 天。另一个问题：用 AdamW 在 H100 上能训练的最大模型是多大？H100 每块有 80GB 显存，每个参数需要的字节数是 2+2+4+4——我们会解释这些数字的来源。这样算下来你能训练的参数量大约是 530 亿。这里有一些注意事项，比如我们没有计算激活值（activations），这取决于批大小和序列长度。所以这些都是非常粗略的"餐巾纸背面"计算。但希望到本课程结束时，你会理解这些数字的来源。关键不是精确计算每一件事，而是掌握大致的轮廓。

---

OK. So last time I talked about knowledge and what you can take away from this class—mechanics, which are how things work. So today, that would be pretty straightforward. The mechanics are just how PyTorch work, how tensors work. It should be fairly—there's no magic here. The mindset I want to impart on you is that resource accounting is going to be very crucial. And I want everyone to get in the habit whenever you write this line of code, think about the performance characteristics. And then finally intuitions. Here we're just going to get a sense of the resources, how they're spent. There's going to be no ML magic today. I'll leave that to Tatsu for the next lecture.

上次我谈到了知识以及你可以从本课程中获得什么——**机制**（mechanics），即事物如何运作。所以今天的内容会很直接：机制就是 PyTorch 如何工作、张量（tensors）如何工作。这应该相当——这里没有魔法。我想灌输给你们的**思维模式**（mindset）是：资源核算将非常关键。我希望大家养成一个习惯：每当你写下这一行代码时，思考它的性能特征。最后是**直觉**（intuitions）。今天我们要做的就是对资源以及它们如何被消耗有一个感觉。今天没有任何 ML 魔法——我会把那些留给 Tatsu 下一讲。

---

OK. So let's get into things. So let's start bottom up and start building up. So what is at the bottom? At the bottom are tensor. So tensors are the building block of storing everything. If you have parameters gradients, optimizer states, data activation, everything essentially is a tensor. So for example, you can take a look at the DeepSeek 3.2 model. And you see that the model itself is a bunch of different tensors. Each tensor has some shapes and also some precision, which I'll talk about later. And so as you know, tensor is subsume vectors, matrices, and can generalize to any number of entities.

好，让我们进入正题。我们从底层自下而上地构建。底层是什么？底层是张量（tensor）。张量是存储一切的构建模块。无论你是参数（parameters）、梯度（gradients）、优化器状态（optimizer states）、数据还是激活值（activations），本质上一切都是张量。例如，你可以看看 DeepSeek 3.2 模型，模型本身就是一串不同形状的张量，每个张量都有一定的形状（shape）和精度（precision），我稍后会讲。如你所知，张量涵盖了向量、矩阵，并可以推广到任意数量的维度。

---

OK. So let's talk about how much tensors take to store. So it depends on the type of tensor. So in general, we're going to be dealing with tensors that store floating point, but tensors can also store integers and other types. So for floating point, typically whenever you talk about float, I think the standard people refer to as float what is called float32. So a float32, if you break it down, has 32 bits. One of the bits is a sign, 8 bits are the exponent, which gives you dynamic range. And the rest is the mantissa or the fraction, which gives you variation. This is also known as fp32 or single precision. And the term single precision comes from the fact that back in the day when you were doing scientific computing, float32 was like a baseline. It was just like you would expect if someone gave you a float, you would expect it to be at least single precision. And if you want more precision, then you can get double precision as that's float64. But in deep learning, we're going the other way, because even 32 is a lot. And the types of computations that we want to do don't demand the high precision that some kind of numeric simulations do.

好，我们来讨论张量存储需要多少空间。这取决于张量的类型。一般来说，我们处理的是存储浮点数的张量，但张量也可以存储整数和其他类型。对于浮点数来说，通常当你谈论 float 时，人们默认指的是 float32。一个 float32 有 32 位：其中 1 位是符号位，8 位是指数（exponent），提供动态范围（dynamic range），其余部分是尾数（mantissa）或小数位，提供精度变化。这也称为 fp32 或单精度（single precision）。"单精度"这个术语来源于早期科学计算时代，float32 是基准——如果有人给你一个 float，你会期望它至少是单精度的。如果你需要更高精度，可以使用双精度（double precision），即 float64。但在深度学习中，我们往反方向走，因为即使是 32 位也已经很多了。我们要做的计算类型并不需要数值模拟所需的那种高精度。

---

OK. So before we get to other types, let's just look at float32. So let's construct a 4 by 8 matrix. By default, the type of tensor you create is float32. So if you want something else, you should declare it. And the memory usage is just the number of elements times the element size here, which is 4 bytes for a 32-bit number. And that's going to be 128 bytes. So just to give you a kind of perspective, so in GPT-3, which is a fairly old model one of the matrix in the feedforward layer is about 2.3 gigabytes. So these tensors can get quite big. And this is not even the biggest one that one can imagine.

在讨论其他类型之前，我们先看一下 float32。我们构造一个 4×8 的矩阵。默认情况下，你创建的张量类型是 float32——如果你想要别的类型，需要显式声明。内存用量就是元素数量乘以每个元素的大小，这里是每个 32 位数 4 字节，所以总共 128 字节。给你一个概念：在 GPT-3（一个相当老的模型）中，前馈网络层中的一个矩阵大约是 2.3 GB。所以这些张量可以变得非常大——而这甚至还不是你能想象的最大尺寸。

---

OK. So since we're interested in efficiency, we want to generally reduce the amount of storage. And we'll see that as you reduce the precision, you actually save memory. And you also save time because operating on 16 bits is going to be faster, let's say, twice as fast, but not always. It depends. And then memory, by reducing memory, we'll see later that actually reducing memory can save time as well, which is maybe less obvious. But it will hopefully become clear. So the obvious thing is you say, OK, let's take away half the bits. Now you have float16. So float16 says you have a sign. You have only 5 bits of exponent, and then the rest is the mantissa. So float16 is good, except for its dynamic range is poor. So even if you have, let's say, try to construct 1e minus 8 tensor, then that is actually just 0. So you can't really represent very big numbers, and you can't represent very small numbers. And the reason is that this exponent it's only 5 bits of exponent compared to 8. So if you train with fp16, which people did back in the day, you will get instability. You will get underflow. You get overflow. You'll get NaNs. It's pretty challenging.

由于我们关心效率，我们通常希望减少存储量。我们会看到，降低精度可以节省内存，也能节省时间——因为用 16 位运算会更快，比如说快两倍，但并非总是如此，取决于具体情况。另外，减少内存实际上也能节省时间——这一点可能不那么直观，但希望会逐渐清晰。最直接的做法就是砍掉一半的位数——现在你有了 float16。float16 有一个符号位，只有 5 位指数，其余是尾数。float16 不错，但它的动态范围很差。即使你尝试构造一个 1e-8 的张量，结果就是 0。你无法表示非常大的数，也无法表示非常小的数。原因在于它只有 5 位指数，而 float32 有 8 位。如果你用 fp16 训练（以前人们确实这么做过），你会遇到不稳定、下溢（underflow）、上溢（overflow）、NaN——非常有挑战性。

---

So bfloat16 was invented. So this was developed in actually 2018 to address this issue. And the observation was that well, let's not compromise on the number of bits. The number of bits is going to be the same as fp16. But we're going to shift some of the bits from the mantissa to the exponent. So that means it has more dynamic range than float16. And it actually has the same dynamic range as float32. But of course, the resolution is worse because there's no free lunch here. But it turns out that in a lot of deep learning applications, this is well worth the trade-off. You want the dynamic range to not overflow and underflow. And because things are kind of sloppy and stochastic anyway, you don't need that much resolution.

于是 **bfloat16** 被发明了。它是在 2018 年开发的，旨在解决这个问题。思路是：我们不减少总位数——位数和 fp16 一样多——但将一些位数从尾数移到指数。这意味着它比 float16 有更大的动态范围，实际上和 float32 的动态范围相同。当然，分辨率更差了——天下没有免费的午餐——但事实证明，在许多深度学习应用中，这个权衡非常值得。你需要动态范围来避免上溢和下溢，而且因为深度学习本身就有一定的粗糙性和随机性，你并不需要那么高的分辨率。

---

So let me actually skip over this part. So OK. So to summarize, what are the implications for training? So you can absolutely train with float32. And if you're training a small model, you probably just—and you don't want to worry about it, just float32 is fine. But it requires 4 bytes of—sorry, 4 bytes of memory per float. And that can take up a lot of memory. And if you train with float16, then that's going to be too risky. So bf16 is the sweet spot. Even bf16 can be risky as well. Maybe [INAUDIBLE] a little bit. One thing that people have—has become common practice is to use mixed precision training. And the actually let me—OK, let me compile this again. I think these are stale.

总结一下，这对训练意味着什么？你完全可以只用 float32 训练。如果你训练的是小模型，不想操心这些，直接用 float32 就可以了。但每个浮点数需要 4 字节内存，这可能会占用大量内存。如果用 float16 训练，风险太大。所以 **bf16 是"甜点"（sweet spot）**。即使 bf16 也可能有风险。大家普遍采用的做法是使用**混合精度训练**（mixed precision training）。

---

So mixed precision training is where some of the computations use some precision, and for other computations use other precision. So in general, as a general rule, bf16 is what you would use for parameters, activations, and gradients. And for optimizer states, you would use fp32. And we'll discuss a little bit more about that later. And to do invoke mixed precision training, so PyTorch has an AMP library. We're not going to talk too much about this, but you basically wrap your code, and PyTorch has—the library takes care of it automatically for you in the sense that it tries to cast things into a bf16 when it's safe. So, for example, MatMuls are generally safe. But if you try to do exponentiation, then it will try to leave things as fp32.

混合精度训练是指一部分计算使用一种精度，另一部分计算使用另一种精度。通常的规则是：参数、激活值和梯度使用 bf16，优化器状态使用 fp32。我们稍后会进一步讨论。要启用混合精度训练，PyTorch 有一个 AMP 库。我们不会深入讨论，但基本上你只需要包装一下代码，PyTorch 会自动处理——在安全的情况下将计算转换为 bf16。例如，矩阵乘法（MatMul）通常是安全的，但如果做指数运算，它会保持为 fp32。

---

OK. So we could do bf16 I think is probably where this class will end. But if you're feeling very adventurous, you can go farther. So fp8, this was introduced four years ago. It actually has been standardized. So if you look at fp8, there's actually two versions because depending on if you need more dynamic range or more resolution. And there's two versions of them. And so we're not going to talk about that. But NVIDIA has some—the transformer engine supports fp8. And most recently, you can actually go down to fp4. So last year, NVIDIA developed nvfp4, and there's only 4 bits per value. So if you just to—so we're on the same page. 4 bits is not a lot. I can write all the values down on a single line here between minus 6 and 6. So that's not very much precision.

本课程大概就到 bf16 了。但如果你很有冒险精神，可以走得更远。fp8 是四年前引入的，已经标准化了。fp8 实际上有两个版本，取决于你需要更多动态范围还是更多分辨率。我们不会讨论这个。但 NVIDIA 的 Transformer Engine 支持 fp8。最近，你甚至可以用到 fp4——去年 NVIDIA 开发了 nvfp4，每个值只有 4 位。4 位不是很多——我可以在一行里写下所有可能的值，范围在 -6 到 6 之间。精度非常有限。

---

Now there's a little bit of a cheat here. Because if you just naively only use these values, you're not going to be able to train very well. So what actually this means is that every value you can have this 4 bits of freedom, but there are blocks. And each block can be scaled up and down accordingly. So you can actually represent more values but you can't represent the full dynamic range for every single value. And there is a model released actually this year, the Nemotron 3 Super, which was trained in fp4, which I think is pretty cool.

这里有一个小技巧。如果你天真地只用这些值，是训练不好的。实际上，每个值有 4 位的自由度，但它们是分块（blocks）的，每个块可以按比例缩放。这样你可以表示更多的值，但不能为每个值都提供完整的动态范围。今年确实有一个模型——Nemotron 3 Super——是用 fp4 训练的，我觉得这很酷。

---

OK. So some of this it's just good to know. And some of this you can't even touch. It's not like you create a tensor and you call it fp—you can make it fp4. A lot of this is done under the hood by NVIDIA's software stack. OK. This was a bit of a long digression, but it's maybe helpful to appreciate that the intricacies of precision here. Any questions before I move on? Yeah. Sorry. It was a question like, when you have a block, you're scaling all those same things in tensor by that block. So then the ratios of all that will still be in fp4. Yeah. So the question is to just— [INAUDIBLE] maximum value is to have more specificity. Yeah, so the question is, OK, just to explain the block a bit more. So you have, let's say a block. Within that block, you can vary up within the 4 bits. And in addition, all those values can be scaled up and down according to how many bits you're scaling factor is. So if you look at an individual value, you actually get more than 4 bits of dynamic range. But it's just like you can't have this value be way over here and the neighboring value way down here.

其中一些了解一下就好，有些你甚至接触不到——不是说你创建一个张量然后声明它是 fp4 就能用的，很多都是由 NVIDIA 的软件栈在底层完成的。这是一个有点长的题外话，但可能有助于理解精度问题的复杂性。在我继续之前有问题吗？有人问关于块的问题：当你有一个块时，你通过那个块来缩放张量中所有对应的值，所以这些值的比例仍然是 fp4 表示的。是的，问题主要是想解释一下块的工作方式。假设你有一个块，在这个块内部，你可以在 4 位的范围内变化。此外，所有这些值还可以根据缩放因子的位数进行缩放。所以对于单个值来说，你实际上获得了超过 4 位的动态范围，但你不能让一个值特别大而邻近的值特别小。

---

One question about, what about 1 bits [INAUDIBLE] affect 1 bit [INAUDIBLE]? Yeah, so there's a lot of training obviously. So maybe this is a good point. So the question is about 1 bit because you can't really go lower than that. So there's a difference between training and inference. So a lot of the low bit stuff, if we talk about—I think we'll talk about quantization later, is that you train a model on and maybe even bf16. And then you quantize into, let's say, 1 or 2 bits. And that is much easier than training a 1-bit language model, which I don't think anyone has done. Maybe it's possible, but I don't think anyone has trained anything credible there. OK. Let us go on then.

有人问到 1 位的情况，因为不能再低于这个了。这里要区分训练和推理。很多低位的工作——我们稍后会讲量化（quantization）——是你用 bf16 甚至更低训练模型，然后量化到 1 位或 2 位。这比直接训练一个 1 位语言模型容易得多。我不认为有人成功训练过 1 位语言模型——也许有可能，但还没有人做出过可信的结果。好，我们继续。

---

So we talked about tensors. And the memory calculus is pretty simple, just the number of elements times however much memory each element takes up. So by default, the tensors you create in PyTorch are going to be on CPU. And of course, you have to—if you want things to go fast, you want to move them to GPU. And actually, so there's a bit of a—I have a slight issue with the slides that they were executed on my laptop, which means that I don't have GPU. So some of the code I'll just show but not execute.

我们讨论了张量。内存计算非常简单：元素数量乘以每个元素占用的内存。默认情况下，你在 PyTorch 中创建的张量是在 CPU 上的。当然，如果你想让东西跑得快，你需要把它们搬到 GPU 上。实际上，有一个小问题——这些幻灯片是在我的笔记本上执行的，这意味着我没有 GPU。所以有些代码我只会展示而不执行。

---

OK. Let's see. This is maybe not that interesting, but I think everyone knows how to move tensors to GPU. But just remember to do that. Otherwise you won't get your speed-ups. OK, so we talked about memory of tensors, which is very straightforward. Now let's talk about computing with tensors. So before talking about FLOPs accounting for the tensor operations, let's take a little bit of a digression to talk about einops. So how many of you are familiar used einops before? OK. So maybe 2/3. OK. Good.

这部分可能不那么有趣，但我想大家都知道如何将张量搬到 GPU 上——但要记得这么做，否则你得不到加速。好，我们讨论了张量的内存，这非常直接。现在我们来讨论用张量进行计算。在讨论张量操作的 FLOPs 核算之前，我们先稍微跑题一下，谈谈 **einops**。你们中有多少人之前熟悉或使用过 einops？大概三分之二。好。

---

So the motivation behind einops, for those of you who might not be indoctrinated is, it's very easy to mess up. Or I find it very confusing to look at code such as this. And you have x and y. And then you have transpose minus 2 and minus 1. And you're trying to figure out what minus 2 and minus 1 is. And so this is maybe the motivation for using variable and names rather than indices. So einops is a library for manipulating tensors where the dimensions are named. And this is inspired by Einstein summation notation. There's a nice tutorial which you can go through. I'm just going to cover some of the basics.

对于那些还不熟悉 einops 的人来说，它的动机是：传统的张量操作很容易出错。或者我觉得看这样的代码非常令人困惑——这里有 x 和 y，然后有 transpose 的 -2 和 -1 参数，你得费劲搞清楚 -2 和 -1 是什么。所以这就是使用变量名而非索引的动机。**einops** 是一个操作张量的库，其中的维度是有名字的。这受到爱因斯坦求和约定（Einstein summation notation）的启发。有一个很好的教程，我只介绍一些基础知识。

---

So basically, the way to think about einsum is a generalized matrix multiplication with good bookkeeping. So here's an example. So I have a matrix 3 by 4. I have a 4 by 3 matrix. And if I do the MatMul, this is actually pretty nice. It's pretty easy to understand. In einops, basically you say x has two dimensions, the row and the column, which I'm going to name seq1 and hidden. I'm going to have y. That's a matrix which has also rows and columns, which I'm going to name hidden and seq2. And I'm going to produce tensor or here a matrix, where the dimensions are indexed by seq1 and seq2. And anything that is not mentioned here, the hidden gets summed out. So the way this works is I'm going to sum over—enumerate over all possible values of all the variables that occur here, which are seq1's hidden and seq2. And I'm going to basically index into x, index into y, multiply them and dump them, accumulate them into the result z sub seq1 and seq2.

基本上，`einsum` 可以看作是一种带有良好簿记的广义矩阵乘法。举个例子：我有一个 3×4 的矩阵和一个 4×3 的矩阵。做 MatMul 很容易理解。在 einops 中，你说 x 有两个维度——行和列，我分别命名为 seq1 和 hidden。y 也是一个矩阵，有行和列，我命名为 hidden 和 seq2。我要生成的张量（或者这里是一个矩阵），其维度由 seq1 和 seq2 索引。任何这里没有提到的维度（即 hidden）都会被求和掉。工作方式是：枚举所有出现的变量（seq1、hidden、seq2）的所有可能值，索引到 x 和 y，相乘，然后累加到结果 z 的 seq1, seq2 位置上。

---

All right. So you say this is—come on. This is much easier than this, Right OK, let's try a more complicated example. So here's the example I showed before. Now we have a tensor. It's 2 by 3 by 4, another tensor 2 by 3 by 4. And if I were doing things the old way, basically what I'm doing is transposing these last two. And then because at implicitly batches the dimensions that are not the MatMul dimensions, then you get the answer. So you have to reason about this a bit. Einops makes this very clear. It says there's a batch dimension. There's seq1 hidden, seq2 hidden. And I'm just going to produce batch seq1 and seq2. And notice that there's no transpose because I just—in some sense I've done the transpose by the naming. If I had hidden and seq2, then it would be no transpose. I always get confused by transposes. And the fact I don't have to think about transposing it makes me happy.

你看，这比之前的方法容易多了，对吧？我们试一个更复杂的例子。现在有一个 2×3×4 的张量和另一个 2×3×4 的张量。如果用老方法，我需要转置最后两个维度，然后利用 PyTorch 隐式地对非 MatMul 维度进行批处理（batching），得到结果。你需要稍微推理一下。Einops 让这变得非常清晰：它说有一个批处理维度（batch），有 seq1 hidden 和 seq2 hidden，然后我直接产生 batch seq1 和 seq2。注意这里没有转置，因为在某种意义上我通过命名完成了转置——如果我把 hidden 和 seq2 写在一起，就不用转置了。我总被转置搞糊涂，不需要思考转置这件事让我很开心。

---

OK. So if you want to get fancy, you can say, well, batch—I'm just going to replace with dot, dot, dot. And this means that if I had, let's say, rank 10 tensor with eight different batching dimensions, I can just write dot dot, dot without enumerating all of them. And this comes up in language modeling because you might have a batch dimension. You might have a sequence dimension. You might have a head dimension. And you're trying to do this matrix operation for all of them. And you might not want to have to just worry about this. And the nice thing is that you can write modular code where you can write this dot, dot, dot without worrying about even the shape of the tensor that comes in.

如果你想更高级一点，你可以用 `...`（省略号）来表示批处理维度。这意味着如果我有一个秩（rank）为 10 的张量，有八个不同的批处理维度，我可以直接写 `...` 而不需要全部枚举出来。这在语言建模中很常见，因为你可能有一个批处理维度、一个序列维度、一个头（head）维度，而你想对所有维度做这个矩阵操作。你不需要为这个操心。好处是你可以写出模块化的代码，用 `...` 而不必关心输入张量的形状。

---

All right. So that's eisum which is in the einops library. There's a reduce. So this is a generalization of sum, mean, max, and min. So for example, if you have, let's say, this tensor and you want to sum according to dimension of dim minus 1, which means sum along the last dimension here. So again, I don't like this notation. But what you can do is call reduce. And basically what you say is that there's some batching dimensions. In this case, it would be these first two. And then there's some hidden dimension which doesn't appear on the right side, which means that it gets summed. And here, I put sum, which means that the aggregation reduction operation is sum. But you can replace it with mean or max or min. Yeah. Is there some speed-up to this? This basically reduces to the same type of primitive operations. You can think about it as just sugar. So it should be the same.

这就是 einsum，属于 einops 库。还有 **reduce** 操作，这是 sum、mean、max 和 min 的泛化。例如，如果你有一个张量，想按 dim=-1 求和（即沿着最后一个维度求和），我不喜欢这种写法。但你可以调用 reduce，说有一些批处理维度（这里是前两个），然后有一个隐藏维度没有出现在右边，意味着它被求和。这里我用的是 sum，但你可以替换为 mean、max 或 min。这有加速吗？它本质上归结为相同类型的原始操作，你可以把它看作语法糖，所以速度应该是一样的。

---

OK. So the final thing I'll talk about is rearrange. So this is, I think, a pretty powerful tool. I think it will come up in an assignment once. So sometimes you have a dimension that actually represents two dimensions, and you want to operate on one of them. And the reason this happens is that sometimes you have a matrix and you flatten it. And then you want to maybe unflatten and flatten. So this is the way that it works here. So imagine I have a matrix 3 by 8 but where this dimension, 8 actually represents a 2 by 4 matrix. So I want to multiply that 2 by 4 matrix by this 4 by 4 matrix. So what I'm going to do, actually, is to call rearrange. And what I am doing here is saying, look, this is some number of batch dimensions, which here just corresponds to the first element here. And then here, I use parentheses to say that this h actually represents the product of heads and hidden1, where I have to—obviously there's multiple ways to decompose this. It could be 2 by 4, 4 by 2. So I said the number of heads is 2, which means that hidden1 is 4. And then I can break that up into two dimensions, heads and hidden. OK. So this creates this. So before x looked like this, and now x looks like this. So I guess this might be a little bit hard to see. So then you can perform your operation transformation on w. And this is what we've seen before where you have just a standard MatMul where there's some number of batching dimensions for x here. And this is hidden times hidden by hidden2. And then once you've done that transformation, you can rearrange it back. And this is straightforward. You basically look at two dimensions, and then you can group them into one dimension.

最后我要讲的是 **rearrange**。这是一个非常强大的工具，我想作业中会用上一次。有时候你有一个实际上代表两个维度的维度，你想对其中一个进行操作。原因是有时你有一个矩阵，把它展平（flatten）了，然后又想解展平（unflatten）和展平。想象我有一个 3×8 的矩阵，但这里的 8 实际上代表一个 2×4 的矩阵。我想用这个 2×4 矩阵乘以一个 4×4 矩阵。做法是调用 rearrange。这里有一些批处理维度（这里就是第一个元素），我用括号表示这个 h 实际上是 heads 和 hidden1 的乘积。当然有多种分解方式——可以是 2×4 或 4×2。我指定 heads 数量为 2，那么 hidden1 就是 4。然后我可以把它拆成两个维度：heads 和 hidden。变化之前 x 是这样的，之后变成那样。这可能有点难看清。然后你可以对 w 执行操作变换，就像我们之前看到的：对 x 做标准 MatMul，其中有一些批处理维度，这是 hidden 乘以 hidden 再乘以 hidden2。做完变换后，你可以把它 rearrange 回去：把两个维度合并为一个维度，很简单。

---

Yeah. Could you take a two-dimensional thing and shape it into one dimension, aren't there two ways? Like, you can do it row major or column major? Yeah, so the question is if you have a one-dimensional thing and you shift it into—sorry, you have a two-dimensional thing and you shift it into one-dimensional thing, which way do you do it? Well, the order you do it is specified in the order here. OK, yeah.

有人问：把二维变成一维不就有两种方式吗？比如行优先（row major）还是列优先（column major）？你的操作顺序是由这里的顺序指定的。

---

So sometimes I find it takes a bit of time to get it used to, but it's well worth it because once you have an einsum, you just think in a different way. And all the transposes and reductions, all that, it's just it becomes more fluid. You have to think through these more bespoke primitives. All right. So OK. We're going to use einops. We'll see a little bit later.

有时候需要花点时间去适应，但非常值得——一旦你掌握了 einsum，你就会用不同的方式思考。所有那些转置和归约操作都变得更加流畅，而不是去纠结那些更特化的原始操作。我们会在后面用到 einops。

---

So now let's go return back to the resource accounting question. So I have tensors. We've talked about how they take memory. So how much compute do they take? So the thing we're going to use to measure computation cost is the number of FLOPs. A FLOP is a floating-point operation. And we're going to assume it's a basic operation like addition or multiplication. So now there's other things that GPUs can do. But for the most part, we're just going to ignore them because these are the bread and butter, and are going to eat up most of your time.

现在回到资源核算的问题。我们有张量，已经讨论了它们占用多少内存。那它们需要多少计算量呢？我们用来衡量计算成本的是 FLOPs 数量。一个 FLOP 就是一个浮点运算（floating-point operation），我们假设它是加法或乘法之类的基本操作。GPU 还能做其他事情，但大部分情况下我们会忽略它们，因为加减乘除是核心操作，会占据你大部分时间。

---

So one thing that is a pet peeve is that if I say the word FLOPs, it's actually ambiguous what I mean. So there's FLOPs, which is saying the number of floating-point operations, usually written FLOPs with a lowercase s. This is a measured amount of computation done. And then there's FLOP/s, which is floating-point operations per second. Sometimes it's also very confusing and written as FLOPS with uppercase S, which—but I'm going to always write /s to make it clear that this is measuring the speed of hardware. So if you go and see that H100s have 800, 989 teraflops, it's the second. And when I say that GPT-3 took 325 or whatever it is FLOPs, that's the former. So just to get that out of the way.

有一个让人恼火的点：当我说 FLOPs 时，实际上有歧义。一个是 **FLOPs**（小写 s），表示浮点运算次数（number of floating-point operations），这是计算量的度量。另一个是 **FLOP/s**，表示每秒浮点运算次数（floating-point operations per second）。有时它被写成大写 S 的 FLOPS，非常令人困惑。我会一直写成 `FLOP/s` 来明确表示它是衡量硬件速度的。所以如果你看到 H100 有 989 teraflops，那是后者。当我说 GPT-3 花了 325 （或其他数字） FLOPs，那是前者——先把这个搞清楚。

---

So just to give you an order of magnitude. So the number of FLOPs when I talk about 1e22 or 23 or 25, these are referring implicitly to the amount of compute or the scale of some of these models. And so if you look at H100s—if you look at this glossy spec sheet—actually it's not on this page. OK. Forget it. There is a spec sheet and I'll tell you that for bf16, the number of FLOP/s is 1979. And then you go and you benchmark it, and it's like wait a minute, that's not actually what I'm getting. And then you go read the fine print. And there's a footnote that says this is with sparsity. So sparse matrix and for dense over 2. So you always have to take these numbers divide by 2. So that's why you see these divide by 2.

给你们一个数量级的概念。我提到的 1e22、1e23 或 1e25 FLOPs，都隐含着指这些模型的计算量或规模。如果你看 H100 漂亮的规格表——实际上不在这页上。算了。有规格表显示，对于 bf16，FLOP/s 是 1979。然后你去基准测试，发现等等，这跟我实际拿到的不一样。然后你去看小字，有脚注说这是带稀疏性（sparsity）的——稀疏矩阵，密集矩阵要除以 2。所以你得把这些数字除以 2。这就是为什么你会看到除以 2 的情况。

---

So this allows us to—just for intuition, so if you have 8 H100s so there's one node for two weeks. That's 8 times the number of seconds per in two weeks. Actually, this looks like it's one week. OK fine. It's one week times the number of FLOPs you get per second. So that's about 5e 21. OK. So this is just of building intuition for the number of FLOPs that certain types of hardware have and how many FLOPs certain types of models require. It's nothing fancy. It's just math and napkin math.

这让我们可以建立直觉。如果你有 8 块 H100（一个节点），跑两周——实际上看起来是一周。好吧，一周乘以每秒获得的 FLOPs，大约是 5e21。这只是在建立直觉，理解某种硬件有多少 FLOPs、某种模型需要多少 FLOPs。没什么花哨的，就是数学和粗略估算。

---

OK. So now let's do something more mechanical. So suppose you have a linear model. It turns out that a lot of this calculus of counting FLOPs is actually going to be at the core it's like linear MatMuls. So this is actually not without too much loss of generality. So you have n points. Each point is d-dimensional. And we're going to map each of these d-dimensional vectors to a k-dimensional output. So B is going to be the number of points. D is the number of dimension, input dimensions, and K is the number of output dimensions. OK. So let's construct some x, which is the data matrix B by D. The weight matrix is D by K. And when you do the MatMul, the question is how many FLOPs that is. And it turns out that this is going to be 2 times basically the product of all the three dimensions. And the way to see that is that we have one multiplication for each triple and then also one addition. So there's a minus 1, because if you don't have to actually add like in this case D minus 1 times. But let's ignore that.

现在来做一些更机械的计算。假设你有一个线性模型。实际上，FLOPs 计数的核心运算就是线性矩阵乘法，这不会损失太多通用性。你有 n 个点，每个点是 d 维的，我们要将每个 d 维向量映射到 k 维输出。B 是点的数量，D 是输入维度，K 是输出维度。我们构造数据矩阵 x（B×D）和权重矩阵 w（D×K）。做 MatMul 时，需要多少 FLOPs？结果是 2 倍三个维度的乘积。理解方式：每个三元组有一次乘法，加一次加法。实际上有 D-1 次加法，但让我们忽略这个。

---

I'll come back to this. If this was a bit fast, I think there's another way to derive this. So what about the FLOPs of other operations? So elementwise operations are just the size of a matrix. I think that's fairly clear. So addition also requires m n FLOPs. So in general, no other operation you'll encounter as expensive as matrix multiplication for large enough matrices. So in general, we're just going to focus on what MatMuls are doing, with important caveat of when we talk about memory.

如果觉得太快了，还有另一种推导方式。其他操作的 FLOPs 呢？逐元素操作（elementwise operations）就是矩阵的大小，这很清晰。加法也需要 m×n 次 FLOPs。一般来说，对于足够大的矩阵，没有其他操作像矩阵乘法那样昂贵。所以通常我们只关注矩阵乘法在做什么，但在讨论内存时需要特别注意。

---

Yeah. Just from interest, there are some other algorithms for doing matrix multiplication. Is this only for just doing it normally? So the question is that there are other algorithms of doing matrix multiplication. You mean like sub cubic algorithms? Yes. So in general, that's—the optimization, the algorithms that people are going to explore for multiple matrix multiplications are going to be much more about how you co-design with the systems, rather than these more asymptotic algorithms.

有人对矩阵乘法的其他算法感兴趣。问题是有其他算法吗——比如次立方（sub cubic）算法？是的。但人们探索的矩阵乘法优化算法更多是关于如何与系统协同设计，而不是这些渐进（asymptotic）算法。

---

Yeah. We're considering additional multiplication in the same way is not possible to do division more efficiently than multiplication. Yeah, so I think the way the hardware is built, the two are basically the same. But yeah, intuitively it seems like I can do addition faster than I do multiplication. But the way the hardware is kind of the same.

我们不能用同样的思路把除法做得比乘法更高效。硬件构建的方式使得两者基本上是一样的。直觉上你可能觉得加法比乘法快，但硬件上其实是差不多的。

---

OK. So you can think about this MatMul as B is the number of data points. And D K is the number of parameters. So remember x is B by D and w is D by K. So another way to think about this formula is that the number of FLOPs in order to do a forward pass of this linear matrix is actually 2 times the number of tokens or data points times the number of parameters. So it turns out that this actually generalizes to transformers, which if you remember the 6 times n times d formula, we can see the shape of that forming.

你可以把这里的 MatMul 理解为 B 是数据点数量，D×K 是参数数量。所以另一种理解方式是：做这个线性矩阵前向传播所需的 FLOPs 实际上是 2 倍标记（或数据点）数量乘以参数数量。这个规律实际上可以推广到 Transformer——如果你还记得 6×N×D 这个公式，可以看到它的雏形已经形成了。

---

OK. So unfortunately these calculations are not going to be very meaningful because I'm doing this on CPU. But I'll just walk through the code here. So what we've so far done is measured FLOPs. So this is independent of hardware. It's just like the number of calculations you need to do for your model. So now the question is, how long does it actually take on hardware? So one way to find out is you just time it.

这些计算因为我在 CPU 上运行所以没什么意义，但我会把代码过一遍。到目前为止我们做的是测量 FLOPs——这独立于硬件，只是你的模型需要做的计算次数。现在的问题是：它在硬件上实际需要多长时间？一种方法是直接计时。

---

So in this class, I think in the few lectures, we're going to talk more about benchmarking. But here's a little preview. So in general, when you time especially on GPU, you have to call cuda synchronize to make sure that—because the GPU is running asynchronously, you want to make sure that you have this synchronization point. And then you perform the operation. And after operation, then you also have to have the synchronization barrier. If you omit this, you're going to find that wow, your timings are really fast. And that's because this is a non-blocking call. It just returns. And often it's general good practice to try this multiple times and take the average.

在本课程稍后的几讲中，我们会更多地讨论基准测试（benchmarking）。这里先做一个预告。在 GPU 上计时时，你需要调用 `cuda.synchronize()` 来确保——因为 GPU 是异步运行的，你需要有这个同步点。然后执行操作，操作完成后还需要同步屏障。如果省略这一步，你会发现哇塞时间好短，因为这是一个非阻塞调用，它只是立即返回。通常好的做法是做多次并取平均值。

---

So the actual FLOPs per second is basically the number of FLOPs you did times the time that you recorded on your hardware. And so remember, there's also another number, which is the GPU has a spec sheet. Let's see if I can pull it up on this link. I feel like maybe I have the wrong link. I'll have to fix that after class. —that it gives you some number of FLOPs, which was 989 teraflops. And so in general, the number of actual FLOPs per second is going to be different from the promised FLOPs per second.

实际的 FLOP/s 就是你做的 FLOPs 数除以你在硬件上记录的时间。记住还有另一个数字：GPU 的规格表上给出了一些 FLOPs 数字，比如 989 teraflops。实际的 FLOP/s 通常与承诺的 FLOP/s 不同。

---

OK. Oops, sorry. And the way to directly think about the discrepancy is something called Model FLOPs Utilization, or MFU. And the definition of MFU is the actual FLOPs per second divided by the promise of FLOPs per second. And here this is ignoring the communication and other overhead. So you basically take the actual and divide by the promise. So in general, it's rare that you get more than was—I mean, it's—yeah, you just never get anything more than what you were promised. Often you get less. And in general, if you get about MFU of 0.5 for modern models, you should be pretty happy with yourself.

衡量这个差距的方法是 **MFU**（Model FLOPs Utilization，模型 FLOP 利用率）。MFU 的定义是：实际 FLOP/s 除以承诺 FLOP/s。这里忽略了通信和其他开销。实际除以承诺。一般来说，你几乎不可能超过承诺值，通常会更少。对于现代模型，如果你的 MFU 能达到 0.5 左右，应该对自己感到满意了。

---

If you have just like a straight up MatMul, you can get maybe potentially like 80.8 even, but you usually can't get that high. And sometimes if you have really—something's really wrong, you'll get something like 0.1, which means that you should do something. OK. So whenever you write your model, you can calculate. You now know how to calculate the MFU through a combination of counting the number of logical FLOPs that your model needs to do, and then looking at the wall clock time and essentially dividing.

如果你只是做一个纯粹的 MatMul，你可能得到 0.8 甚至更高，但通常达不到那么高。有时如果出了问题，你可能得到 0.1，这意味着你需要做点什么。所以每当你写模型时，你都可以计算 MFU。你现在知道了如何通过统计模型需要做的逻辑 FLOPs 数，然后看实际时钟时间，两者相除来计算 MFU。

---

Yeah. Was there a question over there? Oh. [INAUDIBLE] Yeah. So is the promise—what is the promise FLOPs number? That is in the spec sheet, it is already divided by 2 of the 989 number. And then on top of that, you only get 0.5 of that in general depending on your computation. [INAUDIBLE] you're getting 50% MFU? Yeah, so why are you getting only 50% MFU? Actually, that's a good question. I'll come back to that when we talk about memory bottlenecks.

有人问：承诺的 FLOPs 数是多少？规格表中的 989 已经是除以 2（考虑稀疏性）之后的数字了。在此基础上，根据你的计算类型，通常只能达到 50%。所以为什么只有 50% 的 MFU？这其实是个好问题，我稍后讨论内存瓶颈时会回来回答。

---

OK. So to summarize here, matrix multiplications dominate generally the computations. And that's by design. And the number of FLOPs per second depends on the hardware. So better hardware leads to more FLOPs and also it depends on the data type. Which means that if you look at the spec sheet, different data types will have different FLOPs. If you try to do float32 nowadays, it's going to be really, really slow because they're not really optimizing for that workload. Whereas now bf16 or fp8 are going to be much faster. And MFU—now you know what MFU is. It's the actual FLOPs divided by promised FLOPs.

总结一下：矩阵乘法通常主导计算，这是设计使然。每秒的 FLOPs 数取决于硬件——更好的硬件带来更多 FLOPs，同时也取决于数据类型。不同数据类型在规格表中有不同的 FLOPs 值。现在如果你尝试用 float32，会非常非常慢，因为硬件不再针对这种工作负载优化了。而 bf16 或 fp8 会快得多。MFU——现在你知道 MFU 是什么了：实际 FLOPs 除以承诺 FLOPs。

---

All right. So to go back to the question of why is MFU 0.5. And to understand that, I'm going to have to introduce this idea of arithmetic intensity. And the reason is that, well, it's not just doing a bunch of MatMuls and then you're done and looking at how long the MatMuls take. This is my very cartoon version of what hardware looks like. You have high bandwidth memory. And then you have where the compute cores are, the accelerators chips are. And then how do you compute? Well, you have to send your inputs, your matrices—the tensors are sitting down here—from the memory to the accelerator. You do the computation, and then you send it back.

回到为什么 MFU 是 0.5 的问题。为了理解这一点，我需要引入**算术强度**（arithmetic intensity）的概念。原因是：你并不是做一堆 MatMul 然后看它们花了多久就完事了。这是我对硬件的非常卡通式的描述。你有高带宽内存（HBM），另一边是计算核心（加速器芯片）。怎么计算呢？你必须把输入、矩阵——张量都在下面这里——从内存送到加速器，做计算，然后送回去。

---

So if you want to measure how long this takes, this depends on two things. One is the accelerator speed, which is what we've talked about just now. But the other thing that matters is the memory bandwidth of your hardware, which we haven't talked about. And if you look at the spec sheet, we talked about how the FLOPs per second was 1979e12 divided by 2. And the bytes per second, which is the memory bandwidth, this is 3.3 terabytes per second. And remember why we were looking at memory, how much things took to store. It's most obviously that, well, if you have a model that's too big it doesn't fit in your memory, that's not going to be fun. But also it turns out that memory—you need to move this memory, which takes time. So actually the size of how large things actually influences speed as well.

要衡量这需要多长时间，取决于两件事：一是加速器速度——我们刚刚讨论过；另一个是硬件的**内存带宽**（memory bandwidth）——我们还没讨论过。规格表中 FLOP/s 是 1979e12 除以 2，而字节/秒（即内存带宽）是 3.3 TB/s。还记得我们为什么关心内存占用吗？最明显的是，如果模型太大放不进内存就不好玩了。但同样重要的是，你需要移动这些内存，这需要时间。所以实际上东西有多大也会影响速度。

---

OK. So I'm going to talk through some operations, and I'm going to basically compute how long things are going to take and introduce this idea of arithmetic intensity. OK, so suppose I have a million dimensional vector of bf16. And I'm going to just compute a ReLU on this. So remember ReLU is just max of x and 0 done elementwise on the entire vector here. So I count two things, one is the number of bytes that were moved. So I have to read x in—copy it into the accelerators. And each of this is going to be 2 because bf16 is 2 bytes per float times n floats. So that's 2n. And then I'm going to write y back. So that's another 2n. OK. So that's the number of bytes that have to be moved. And then how many FLOPs were done? Well, each of these elements, I'm just comparing it with zero, and that's it. So that's n comparisons.

我来讲解一些操作，计算它们需要多长时间，并引入算术强度的概念。假设我有一个一百万维的 bf16 向量，我要对它做 ReLU 运算。ReLU 就是在整个向量上逐元素取 max(x, 0)。我计算两件事：一是移动的字节数——我必须读入 x，把它复制到加速器，每个元素 2 字节（bf16），所以是 2n。然后写回 y，又是 2n。这是需要移动的字节数。那做了多少 FLOPs？每个元素只是和 0 比较，所以是 n 次比较。

---

So now I look at the communication time, which is the number of bytes that I needed to move divided by the speed of that movement. And that gives me the time, which is 1e minus 6 seconds. And what about the computation time? That's the FLOPs divided by FLOPs per second. So that's 1 minus 9. OK. So there's also going to be another important assumption which generally, we try to hold is that we overlap communication and computation. We're going to talk more about that when we talk more deeply about GPUs. But the idea is that in this case as we don't sit here waiting for the things to move. As soon as they're there, we start computing them, and then we move them back. So this movement and also the compute is happening at the same time. So mathematically, we're just going to assume that the total time is the max of the two, because we're going to assume that we can perfectly overlap them. In practice, it's not going to be perfectly overlapped. There's going to be some overhead. But this is good enough for now.

通信时间就是需要移动的字节数除以移动速度，得到 1e-6 秒。计算时间呢？FLOPs 除以 FLOP/s，得到 1e-9 秒。还有一个重要的假设：我们通常假设通信和计算可以重叠（overlap）。在 GPU 上深入时会更多讨论。思路是：我们不会坐等数据搬完——数据一到就开始计算，同时继续搬数据。所以从数学上，我们假设总时间是两者中的最大值，因为我们可以完美重叠。实际上不可能完美重叠，会有一些开销，但这对现在来说已经足够了。

---

OK. So the total time, as we see here, is 1e minus 6. OK. So if you ask what is the bottleneck here? So when the communication time is greater than the computation time, then we call it the algorithm memory bound, because you're spending most of your time just waiting for bits to show up. And when the computation time is greater and the communication time, that's compute bound, because then you're actually—your bottleneck is actually doing the compute. And so in this case, what is ReLU? Rectified Linear Unit. Oh, sorry. Is it memory bound or compute bound? Memory bound. Memory bound. Yeah.

总时间我们看到是 1e-6 秒。那么瓶颈是什么？当通信时间大于计算时间时，我们称这个算法是**内存受限**（memory bound）的，因为大部分时间在等待数据到达。当计算时间大于通信时间时，就是**计算受限**（compute bound）的。在这个例子中，ReLU 是内存受限还是计算受限？内存受限。

---

And it's clear, because the compute is way less than the communication. So here's another way to see it. And this is where I'm going to define the intensity. So what is the intensity of an accelerator is essentially how much work can the accelerator do per byte transferred. And for any given accelerator based on the spec sheet, you basically have the FLOPs per second divided by the bytes per second. So how much useful work can you do per byte that's moved for each 100? That's 295. So that means for every byte of—you can do 295 floating point operations. So that's an intuitive number to have in your head, about 300.

很明显，因为计算量远小于通信量。换一种方式来看——这里我要定义**强度**（intensity）。一个加速器的强度就是每传输一个字节它能做多少工作。根据规格表，就是 FLOP/s 除以 bytes/s。H100 的这个值大约是 295——每移动一个字节可以做 295 次浮点运算。这是一个好记的直觉数字，大约 300。

---

OK. So now the arithmetic intensity of algorithm is how much actual work was done per byte for this workload. And if you look at it for the ReLU computation, it's FLOPs over bytes and it's actually—so this is actually a quarter, I guess, not half. So the point is that it's very small, 0.25. OK. So now we can talk about bottlenecks through the language of intensity. So something is memory bound if the arithmetic intensity is smaller than the accelerator intensity and compute bound if it's greater than accelerator intensity. So these are equivalent. And if you look at the algebra, it's basically you have two fractions. And then you just multiply and divide to—you basically switch the terms around.

现在，算法的**算术强度**（arithmetic intensity）是这个工作负载下每字节做了多少实际工作。对于 ReLU 来说，FLOPs 除以 Bytes，结果是 0.25——非常小。现在我们可以用强度来讨论瓶颈了：如果算术强度小于加速器强度，就是内存受限；如果大于，就是计算受限。这两种表述是等价的。

---

OK. So in this case, we're memory bound. So in general, we're going to find ourselves in a situation where we're memory bound because data movement is expensive. And so if you can get higher arithmetic intensity, that's good. So 0.25, if you see that number, if someone tells you arithmetic density is 0.25, you should say, oh, this is really bad. Yeah. What's some typical arithmetic intensity for some transformer [INAUDIBLE]? Yeah, so we'll get to that.

在这个例子中，我们是内存受限的。一般来说，我们经常会发现自己处于内存受限的情况，因为数据移动很昂贵。所以如果能获得更高的算术强度，那就好了。0.25——如果有人告诉你算术强度是 0.25，你应该说，哦，这很糟糕。Transformer 的典型算术强度是多少？我们待会儿会讲到。

---

OK. All right. So OK. So one way to think about increasing arithmetic intensity is that let's just try to do more stuff per unit of byte moved. So the GELU is another activation. It looks like this, some formula that is more—doesn't have zeros. And if you do this calculation, the number of bytes are moved back and forth is still 2n plus 2n. And the FLOPs here it's about 20 FLOPs per elementwise scalar operation, so it's 20n. So the arithmetic intensity is, let's say, 5. This is a crude estimate. And in this case, are we memory bound or compute bound? Memory bound. Memory bound, because 5 is still smaller than 295, way smaller. So even though GELU does a lot of work, more work than ReLU, in the way that things are structured, it's still memory bound. Which means that if you were just computing ReLU and GELU, you think that, well, GELU is so complicated, it must be really expensive. But actually it's exactly the same, because that's not where the bottleneck is.

提高算术强度的一种思路是：每移动一个字节做更多的事。GELU 是另一种激活函数，它的公式更复杂，没有零。计算一下：移动的字节数仍然是 2n+2n，FLOPs 大约是每个标量操作 20 次，所以是 20n。算术强度大约是 5（粗略估计）。这时我们是内存受限还是计算受限？还是内存受限，因为 5 仍然远小于 295。所以即使 GELU 比 ReLU 做了更多工作，在结构化方式下仍然是内存受限的。这意味着如果你比较 ReLU 和 GELU，你会觉得 GELU 那么复杂，一定很贵——但实际上是一样的，因为瓶颈不在这里。

---

OK, so now let's look at some linear operations, so dot product. So dot product, you have a vector x. You have a vector w, size n, and you take the dot product. So how many bytes are moved? So you read x, which is 2n; read w, which is 2n; and then you write y, which is a scalar, which is 2. And the number of FLOPs is you do the n multiplications and n minus 1 additions. So that's 2n minus 1. OK. So what's the arithmetic intensity? Oh, for this one, it's about half, which is also pretty bad. Which means that—hopefully you get the idea—it's memory bound.

现在来看一些线性运算——点积（dot product）。你有一个向量 x，一个向量 w，大小都是 n，做点积。移动了多少字节？读入 x（2n），读入 w（2n），写出 y（标量，2）。FLOPs 是 n 次乘法和 n-1 次加法，所以是 2n-1。算术强度大约是 0.5，也很糟糕——仍然是内存受限。

---

So what about a matrix vector product? So I have this x is a vector. w is an n by n matrix. And you form this product. How many of you think this will be compute bound? How many of you think memory bound? OK. So let's see. So I'm going to read x read, which is 2n; read w, which is 2n squared; and write y, which is 2n. And there's the number of FLOPs is basically you're doing n dot products. So that's n times the cost of doing a dot product. And the arithmetic intensity is barely, barely higher. So this is also memory bound.

矩阵向量乘积呢？x 是向量，w 是 n×n 矩阵。你们多少人认为这是计算受限的？多少人认为是内存受限的？我们看看：读入 x（2n），读入 w（2n²），写出 y（2n）。FLOPs 是 n 个点积，即 n 倍点积成本。算术强度几乎没变——仍然是内存受限。

---

OK. So now let's talk about matrix multiplication. So this is where things get interesting. So I have an n by m matrix, another m by n matrix. And I multiply them. And the number of bytes that were moved was 2n squared plus 2n squared. And then I have to write 2n squared bytes back to y. And the number of FLOPs here is n squared dot products. And then what's arithmetic intensity? It's 300. Whew. OK, so 340. And in general, it's roughly n over 3. And intuitively this makes sense because you're sending n squared things, but you're computing n cubed things. So the number of things you're computing over a number of things you're sending is order n. And this gets better the larger you make the matrices.

现在来看矩阵乘法——这里开始有趣了。我有一个 n×m 矩阵和另一个 m×n 矩阵，将它们相乘。移动的字节数：2n² + 2n²，再加上写回 y 的 2n²。FLOPs 是 n² 个点积。算术强度是多少？300——哦，340。大致上是 n/3。直观上这合理：你传输了 n² 个东西，但计算了 n³ 个东西，计算量相对于传输量是 O(n) 的量级。矩阵越大，效果越好。

---

So in general, this is why when you hear people talk about, oh, we need to make large batch sizes or have large matrices, it's exactly this. If you're under the accelerator intensity, making things smaller doesn't actually speed things up. It's all the same. Whereas if you get to a point where you're over this, then you're actually saturating your GPUs. OK. So finally, this is compute bound. OK. So as long as we have large matrices, we're actually pretty good. We're in a compute bound saturating the accelerator.

这就是为什么人们说需要大的批大小或大的矩阵。如果你的算术强度低于加速器强度，把东西变小实际上不会加速——都一样。一旦超过了这个阈值，你就在真正地饱和 GPU 了。所以，矩阵乘法是计算受限的。只要我们有大的矩阵，情况就很好——我们处于计算受限、饱和加速器的状态。

---

And the question earlier about what about transformers? Well, it turns out we'll see in both your assignment, but also in the next lecture that transformers are essentially big matrix multiplications with some things sprinkled in between. So that's good news from arithmetic intensity. And this is, by design, transformer is designed in a certain way to have high arithmetic intensity. And one comment here, just to foreshadow the inference lecture, is that matrix vector products is essentially what goes on when you're doing transformer inference. Because inference, you're generating one token at a time. And so you only get to—it's like a vector that you're trying to dot product with a matrix. And that's as we saw with memory bound. Whereas at training time, you get this whole sequence and you're processing all at once. OK. So note also that the intensity depends on the precision. So by default everything we're doing here is fp16.

之前有人问 Transformer 怎么样？在作业和下一讲中都会看到，Transformer 本质上就是大矩阵乘法，中间点缀着一些其他操作。从算术强度来看这是好消息——Transformer 的设计方式本身就具有高算术强度。这里做一个预告：推理时做的是矩阵向量乘积——因为推理是一次生成一个标记，就像向量和矩阵做点积，这是内存受限的。而训练时是整个序列一次性处理。另外注意，强度取决于精度，这里默认都是 fp16。

---

OK. So also to tie it to the other question about MFU, and the reason you might be getting low MFU is that while you might be doing—so MFU is a promise FLOPs—sorry, actual over promise. So if you have really large memory bottlenecks, then you're not actually going to get very good throughput, even though you—the promise is if you didn't have memory bottlenecks, you were just like going through and doing all the computations of your model.

回到关于 MFU 的问题。你可能得到低 MFU 的原因是：如果你有严重的内存瓶颈，你就不会获得很好的吞吐量——尽管承诺的 FLOPs 是基于没有内存瓶颈的假设。

---

OK. Final thing on arithmetic intensity roofline plots. So there's a nice way to—yeah. [INAUDIBLE] generally speaking, these models tend to be memory bound, as they say for most of the computation. But yet the accelerators are 50% is not as good. And maybe you get 70, maybe you get 80 that's really good, meaning that the accelerator is outsized compared to memory bandwidth. Why is it like that? Why do these accelerators—are just big while they're just idling or waiting for memory? So the question is, could you design maybe accelerators that had better characteristics? Yeah. Maybe when we talk about GPUs and understand a bit more how they work, we can talk about why this is. But if you have an answer, you should tell Jensen. And maybe you can design a better hardware.

关于算术强度的最后一点：**屋顶线图**（roofline plot）。一般来说，这些模型的大部分计算是内存受限的。但加速器利用率只有 50% 并不理想，可能达到 70% 甚至 80% 才算好。为什么加速器这么大却在空转等待内存？你能不能设计出特性更好的加速器？当我们更深入了解 GPU 的工作原理时，可以讨论为什么。但如果你有答案，你应该告诉 Jensen（黄仁勋），也许你能设计出更好的硬件。

---

OK, so let's visualize the relationship between arithmetic intensity and performance. So this plot basically plots the arithmetic intensity on the x-axis. So every slice here corresponds to a particular, let's say, algorithm. And then we have these lines here. And each of these lines corresponds to, let's say, a particular accelerator. Maybe H100 or B200 or so. And so what this shows is—and then on the y-axis is the FLOPs per second that are realized. So if your algorithm has low arithmetic intensity, like, ReLU or dot products, you're going to be over here, which means that the FLOPs per second realize is going to be not as high as your peak accelerator. And as you increase the memory arithmetic intensity, that's going to—things are going to be better. You're going to be able to saturate your hardware up until a certain point. And after a certain point your compute bound. And obviously you can't exceed the peak FLOPs.

让我们将算术强度和性能的关系可视化。这个图的 x 轴是算术强度，每个切片对应一个算法。这些线对应不同的加速器（比如 H100 或 B200）。y 轴是实际达到的 FLOP/s。如果你的算法算术强度低（如 ReLU 或点积），你在这里——实际 FLOP/s 远低于峰值。随着算术强度增加，情况会好转，你可以饱和硬件直到某个点，之后就是计算受限的。当然你不能超过峰值 FLOPs。

---

All right. So let's go on here. OK. So now I'm going to go back and talk about memory and compute for the operations that we need in training. So far we've done tensor operations, basically MatMuls. And we saw basically how much memory it took and how much compute it took and the interaction between them. So now let's actually think about what it takes to train. So here is our running example here. Actually it's not a linear network, just a deep network. So I'm going to consider a case where I have an input, which is a B by D input, and a number of layers where each layer is a D by D MatMul. And then that produces some set of preactivations and then element wise ReLU that produces some activations of the first layer. And then this is repeated again and again. And the output is just going to be the same size.

现在我们回过头来讨论训练所需操作的内存和计算。到目前为止我们做了张量操作，主要是 MatMul，看到了它们的内存、计算以及二者的交互。现在来思考训练需要什么。这里有一个运行示例——其实不是一个线性网络，而是一个深层网络。输入是 B×D，有若干层，每层是一个 D×D 的 MatMul，产生一些预激活（preactivations），然后逐元素 ReLU 产生第一层的激活值，重复多次。输出大小相同。

---

So the deep network, I mean, just to see what it looks like in PyTorch, just so it's basically a set of blocks. Each block has a weight vector—sorry, a weight matrix associated with it. And so when you the number of parameters here is D squared times the number of layers L. And when you run the model on the batch of data, what we're doing is we're going through the layers, and each layer we basically apply the linear transformation and then a pointwise ReLU activation. And then we do that for all the layers. So this is hopefully straightforward very simple model.

这个深层网络在 PyTorch 中就是一组块，每个块有一个权重矩阵。参数数量是 D² × L（层数）。当你在一个批数据上运行模型时，你逐层执行线性变换然后逐元素 ReLU 激活。这是一个非常简单的模型。

---

OK. So now let's talk about gradients. So let's use actually even simpler example. So this is just a simple linear model regression. So we have a vector 1, 2, 3, a weight vector 1, 1, 1. And we take the dot product, and we form this MSE loss. OK. And what happens when we take the—do the backward pass is that each of the variables involved in this computation graph has a gradient that is either set or not set. So the w.grad gets set to 1, 2, 3. So this is just basic mechanics of PyTorch. I think it should be familiar to all of you.

现在来讨论梯度（gradients）。我们用一个更简单的例子：一个简单的线性回归模型。向量 [1, 2, 3]，权重向量 [1, 1, 1]，做点积，计算 MSE 损失。做反向传播时，计算图中的每个变量都会有梯度被设置或不设置。w.grad 被设置为 [1, 2, 3]。这是 PyTorch 的基本机制，应该都很熟悉了。

---

So now the question is, how much compute does gradients take? OK. So let's count FLOPs for computing gradients. So let's take a simplified model where you have an x, which is BID and times w1 matrix. We're going to ignore this ReLU for now just for simplicity times w2, which is the same D by D—same shape D by D matrix. OK. I'm going to use einsum here for reasons that will become clear. So the first thing you do in this linear network is you take x and you take w1. x is batch by input dimension. w1 is as in buy out, and you get a batch buy out. And h2 takes h1 and w2, and it's the same story. These are just MatMuls.

那么计算梯度需要多少计算量？我们来统计计算梯度的 FLOPs。考虑一个简化模型：x 是 B×D，乘以 w1，忽略 ReLU，再乘以 w2（同样 D×D）。我用 einsum 写，原因之后会清楚。在这个线性网络中，首先 x 乘以 w1（x 是 batch×input，w1 是 input×hidden），得到 h1（batch×hidden）；然后 h1 乘以 w2，同样得到 h2。就是这些 MatMul。

---

And then you form a loss. I'm just sending it to some arbitrary just to get a number out. OK. So what happens in the backward pass, I'm going to call these retain gradients for debugging purposes, which you'll see later. You take the backward pass on the loss. And the question is, how much work did that—how many floating point operations was that? So let's zoom in on one layer. Let's focus on the second layer here, so this layer. And so the second layer takes h1 and just multiplies it by a matrix w2 to get h2. And that's it.

然后你构造损失函数。在反向传播中，我设置了 retain_graph 用于调试。你对损失调用 backward。问题是：这做了多少浮点运算？我们放大看一层——聚焦第二层。第二层把 h1 乘以矩阵 w2 得到 h2，就这些。

---

So if you look at the FLOPs in the forward pass, this is just a MatMul. And we just take the three dimensions, and we multiply them together and bf16. That's 2 bytes. Sorry, that's irrelevant. This is just 2 because it's an addition and a multiplication. So in the backward pass, what does this look like? So in the backward pass, if you remember your chain rule and your backprop algorithm, you have to compute two things. You have to compute the backward message, the gradient of the loss with respect to your input. And you also have to compute the gradient with respect to your parameters. And what do those gradients look like? This is just by the definition of these—I guess this is just the chain rule here written in einsum notation. You take the d loss d h2, which is h2 grad. That's a batch by Alt matrix, and you multiply it by w2, which is in by out. And then that gives you h1 grad, which is d loss d h1 and which is batch n.

看前向传播的 FLOPs：就是一个 MatMul，把三个维度乘起来。反向传播是什么样的？根据链式法则和反向传播算法，你需要计算两件事：反向传播的消息（损失对输入的梯度）和损失对参数的梯度。用 einsum 写出来就是：取 d_loss/d_h2（即 h2_grad，batch×out），乘以 w2（in×out），得到 h1_grad（d_loss/d_h1，batch×in）。

---

So I always get this confused whenever if you see—learn calculus, there's like, one of them has a transpose, and I forget which order to put them in. And einsum I think makes it very clear, because you can remember even just looking at the scalar case that it has to look like h1 grad is h2 grad times w2. And the only question is, how do you index things? And you index things by basically looking at the shape of these—and the named dimensions. And in this case, it's just a matrix multiplication where you are summing over the output dimension. And when you do that, we can check that. So h1.grad was the thing that was computed by loss.backward. And this is actually indeed the same thing that I wrote out here just as a sanity check.

我总搞混哪个需要转置、顺序是什么。Einsum 让这变得非常清晰，因为你可以从标量情况推导出 h1_grad = h2_grad × w2。唯一的问题是如何索引——通过查看这些张量的形状和命名的维度。这里就是在输出维度上求和的矩阵乘法。我们可以验证，h1.grad 就是 loss.backward() 计算出来的东西，和我写出来的确实一样。

---

So the other thing you have to compute is w, the gradient with respect to the parameters. And that's d loss d h2 times h1. So it's the same kind of backward message that's coming back but multiplying with the other thing that you're not taking the gradient with respect to. And you just write out the dimensions. And in this case, you're summing over the batch dimension. But the nice thing is that if you just look at this, we know how expensive this is. The number of FLOPs is essentially the product of all the dimensions. It doesn't matter which ones you're batching or not. It's basically you enumerate over the i, j, k, and you aggregate. The way that you aggregate is different, but the FLOPs is the same. OK. So notice that the backward pass is exactly twice as expensive as the forward pass. And this is because you have to take—compute two gradients, one with respect to the parameters for each parameter, and then one with respect to the input, the other thing that's not the parameter.

另一件需要计算的是参数梯度 w.grad = d_loss/d_h2 × h1。和反向传播的消息相同，但乘以的是你不求梯度的那个东西。写出维度，这里是对批处理维度求和。好处是：我们知道这有多贵。FLOPs 就是所有维度的乘积——无论你是在批处理哪个维度。你枚举 i、j、k 然后聚合，聚合方式不同但 FLOPs 相同。注意，反向传播正好是前向传播的两倍开销。因为你要计算两个梯度：一个是对每个参数，一个是对输入（不是参数的那个）。

---

OK. So now that was just for w2. And you just need to apply this to all the parameters in the network. And you put it all together, you will see that for this network, the forward pass is 2 times the number of data points, which is b times the number of parameters FLOPs. And the backward pass is twice of that, which is 4 times the number of data points times the number of parameters FLOPs. And so the grand total is 2 plus 4 is 6 and 6 times the number of data points and parameters. So this is where the 6 nd comes from that you might have seen in various places. It's just by counting forward and backward. So we did this for just these deep networks. But it turns out that this is actually a good approximation for transformers as well—as long as the context length isn't too large. If the context length is too large, then you get the context length squared, and that's more FLOPs that isn't in this kind of accounting.

刚才只是针对 w2，你需要对网络中所有参数应用这个计算。汇总起来：对于这个网络，前向传播是 2 × 数据点数量（b）× 参数数量 FLOPs；反向传播是前向的两倍，即 4 × 数据点数量 × 参数数量 FLOPs。总计 2+4=6 倍数据点数量 × 参数数量。这就是你可能在各种地方见过的 **6ND** 公式的来源——只是通过统计前向和反向传播得到的。虽然我们只对深层网络做了这个统计，但事实证明这也适用于 Transformer——只要上下文长度（context length）不是太大。如果上下文长度太大，还有上下文长度的平方项，那就不在这个核算范围了。

---

OK. So let's talk a bit about—so now we have gradients. Now we have to—the other piece when you do training is we have to do optimization. So here's our deep network. Just so that I'm not just giving you what's in assignment 1, I'm going to use the AdaGrad optimizer, which this from—this is from 2011. This is predates Adam. It's where you can think about it as somewhere in between SGD and Adam. And basically it's SGD where you look at the second moments of the gradient. Momentum is what you look at the first moment gradients. And Adam is where combine the two of them. I'm not going to have time to go into the optimizer details here, since we're focusing mostly on the usage. So we can define an optimizer. And when you compute the gradients and you compute the gradients and then when you take an optimizer step, if you're defining a new optimizer, so in the assignment 1, you're going to implement Adam.

有了梯度之后，训练的另一部分是做优化。这里我不用作业一的内容，而是用 AdaGrad 优化器（2011 年，早于 Adam）。你可以把它看作介于 SGD 和 Adam 之间的东西：SGD 加上梯度的二阶矩，动量（momentum）是一阶矩，Adam 是两者结合。我不会深入优化器细节，因为我们主要关注使用。当你计算梯度后执行优化器步进时——在作业一中你要实现 Adam——对于每个参数组（这里是 w1 和 w2），有优化器状态（optimizer state），这是优化器运行时使用的存储空间。

---

For each of the parameter groups which are, in this case w1 or w2, we look at—there's something called optimizer state, which is of storage that you can—the optimizer uses while it's running. And what we're computing in AdaGrad is something—is the squared gradients, the sum of the squared gradients. So here we're getting it from the optimizer state. We're updating it with the current gradient, and we're storing it back. And then after you update the g2, then you update the parameters. So in AdaGrad, it's you basically divide by the square root of the average gradient squared or sum of gradient squared, rather.

在 AdaGrad 中，我们计算的是梯度平方的累积和。从优化器状态中取出，用当前梯度更新，然后存回去。更新 g2 之后，再更新参数。AdaGrad 就是用梯度平方和（或平均梯度平方）的平方根来除以梯度。

---

OK. So let's see. So I'm actually going to maybe skip the training loop. Actually, wait. Hold on. I think I actually skipped something I didn't mean to. OK. So that was the optimizer state, and now let's look at how much memory the optimizer is using. Or in general what is the memory usage? So for parameters in this network, there's D squared parameters per each of the L layers. And each parameter takes 2 bytes if we're storing it in fp16. So that's the number of parameters. Activations—this is 2 times—which is for bf16 batch times D times the number of layers. For every layer you have activation. You have gradients which is basically a copy of all the parameters. And this is also bf16.

我们来跳过训练循环部分。等等，我好像跳过了不该跳的。好，那是优化器状态，现在来看优化器用了多少内存。对于网络中的参数：每层有 D² 个参数，每个参数 2 字节（fp16）。激活值（activations）：2 × batch × D × 层数（bf16），每层都有激活值。梯度（gradients）：基本上是所有参数的一份副本，也是 bf16。

---

And the optimizer state is for every—actually this should be the—I think this should be—sorry, I'll fix this. This is a typo. This should be the number of parameters, not parameter memory. And this should be number of parameters, so number of parameters times 2, and then this is 4 times the number of parameters. And the reason for this is that it's customary to use fp32 for the optimizer states for stability reasons. Obviously people have tried using bf16. And what ends up happening is that you're taking squares, and you're averaging multiple steps, and it doesn't—it's not very stable.

优化器状态：这里有个笔误，应该是参数数量而不是参数内存。参数数量乘以 2（bf16），这里是 4 倍参数数量。原因是为了稳定性，通常用 fp32 存储优化器状态。显然有人尝试过用 bf16，但平方和平均多个步骤后不稳定。

---

And for AdaGrad, it's here—we have 4 bytes per parameter for storing the optimizer state. Adam—you store the first order bit and the second order moments, so that's 8 bytes. So if you think about the optimizer states is actually a lot of the memory used. One note is that remember memory serves two purposes. One is how much—you have to store this thing in your HBM. But the other thing is that it has to be shipped to the accelerators. And in general, the optimizer state is not really the bottleneck for compute. So the amount of memory here is not really so important for performance in terms of speed, but it means that you can't fit large models in your memory.

对于 AdaGrad，每个参数 4 字节存储优化器状态。Adam 存储一阶矩和二阶矩，所以是 8 字节。优化器状态实际上占用了大量内存。注意内存有两个作用：一是需要在 HBM 中存储；二是需要被传输到加速器。通常优化器状态不是计算瓶颈，所以内存多少对速度性能不太重要，但它意味着你无法在内存中放下大模型。

---

OK. So to put it together, as we mentioned, the number of parameters here is D times D times L, and the number of FLOPs is D times number of tokens or number of data points times number of parameters. So for transformers, this is going to be a bit more complicated. But you're going to do that in assignment 1. And you do it more carefully.

综上所述，参数数量是 D×D×L，FLOPs 数是 D × 标记数（或数据点数）× 参数数。对于 Transformer，这会复杂一些，但你在作业一中会做，而且会更仔细地做。

---

OK. I'm going to skip the training loop. This is just a general review. Two things I want to quickly touch on before we conclude. One is that as we see, memory does have an important effect both on the ability to store large models, but also sometimes on your speed. And so in general, you want to reduce your memory usage. So there's two things that people typically do. One is gradient accumulation.

跳过训练循环。在结束前我想快速提及两件事。一是内存对存储大模型的能力以及有时对速度都有重要影响。所以通常你想减少内存使用。人们通常会做两件事：**梯度累积**（gradient accumulation）。

---

So in general, you want to use batch sizes that are large enough to improve stability up to a critical batch size, which Tatsu will talk about later. And as we saw that activation memory scales with batch size. So you might want to run out of memory at some point if you have two large batch sizes. So gradient accumulation says, well, you compute. You have these micro batches, and you compute the gradient on the micro batches. And then you just accumulate the gradients. You don't zero out the gradients. And every batch size over microbatch size steps, you update the parameters and zero out the gradients. OK, so this is actually a very simple code change which allows you to save on compute.

通常你希望使用足够大的批大小来提高稳定性，直到某个临界批大小（Tatsu 稍后会讲）。激活内存随批大小线性增长，所以如果批大小太大可能会内存溢出。梯度累积的做法是：你有微批（micro batches），在每个微批上计算梯度，然后累积梯度（不清零）。每经过 batch_size / microbatch_size 步，更新一次参数并清零梯度。这是一个非常简单的代码修改，可以节省计算资源。

---

So the other thing I'll quickly mention is activation checkpointing. So in training, we need to store in general the activations of all the layers. This is done by default. Actually, interestingly, for inference we don't need to compute the gradient, so we only need to store the current layer's activations. But for training, the memory usage is B times D times 2 times L. And the question is, can you reduce this? So activation checkpointing, also known as gradient checkpointing or rematerialization—the key idea here is that in the forward pass, you just keep activations for only a subset of the layers. And in the backward pass, you recompute the missing activations from the last checkpoint. That's why it's called checkpointing.

另一件事是**激活检查点**（activation checkpointing），也称为梯度检查点（gradient checkpointing）或**重计算**（rematerialization）。训练中我们需要存储所有层的激活值（默认行为）。推理时不需要计算梯度，所以只需要当前层的激活。但训练时内存用量是 B×D×2×L。能不能减少呢？关键思想是：在前向传播中，只保留一部分层的激活值；在反向传播中，从最后一个检查点重新计算缺失的激活值。这就是它被称为检查点的原因。

---

And this is a general trick that you see in systems which is trading off. If you want to reduce memory, you can just recompute things. So here we're going to define this to operationalize this. This is actually fairly easy. Actually, I didn't—OK, maybe I didn't see the—OK, so basically what you do here is you have the same model, except for you just add Torch utils at checkpoint on a layer. So that means do this computation, but don't store any of the intermediate activations. Only store what is needed.

这是一个你在系统中常见的权衡技巧：如果你想减少内存，就重新计算。用法很简单：对同一模型，只需在某个层上加上 `torch.utils.checkpoint` ——意思是用这种方式做计算，但不要存储任何中间激活值，只存储需要的东西。

---

So this means that if you store all the activations, remember in your deep network, you have the thing that's pre the ReLU and the thing that's after the ReLU right. So that's a lot of storage. And instead if you do activation checkpointing on those blocks where each block has a linear and ReLU, you don't store the pre ReLU, and you save basically half. You can get away with half the memory. And then when you're doing the backward pass, you need g3, but you can compute g3 easily from h2. OK.

如果你存储所有激活值——在深层网络中，有 ReLU 之前和之后的值——那是很大的存储量。如果在每个线性+ReLU 块上做激活检查点，不存储 ReLU 前的值，可以节省大约一半内存。在反向传播时，你需要 g3，但你可以从 h2 轻松计算出 g3。

---

You can go further than this. You can say, well, I can store all the layers, but in the extreme case, I can just store no layers. And so that will be maximally memory efficient. The only thing is that the compute is going to be L squared. Because for every one of these layers, you have to start from the beginning. And maybe a sweet spot is if you store the checkpoints at square root L layers, that means your activation memory is square root of L, and your recomputation overhead is also square root of L. So that's balanced.

你可以走得更远。极端情况下，你可以不存储任何层的激活——这会最大化内存效率，但计算量会变成 L²，因为每一层都要从头开始。一个"甜点"是每 √L 层设置一个检查点，这样激活内存是 √L，重新计算开销也是 √L——两者平衡。

---

OK. So to summarize this lecture, everything is operating on tensors—parameters, gradients, activations, optimization states, data. We introduced this einops, which hopefully you guys can embrace as a way to think about tensor operations. 6 times number of data points times number of parameters is a formula which now we have demystified as the number of FLOPs per—for training step. And actually if this is training step, this should be batch size. And then we talked about arithmetic intensity and roofline analysis, which allows us to diagnose whether a computation is memory bound or compute bound. Matrix multiplications are compute bound. Basically everything else is memory bound. And then finally, gradient accumulation, activation, checkpointing are ways to reduce the memory. And by reducing the memory, that allows you to use bigger batch sizes. OK. So that's it for today's lecture. So next week, Tatsu will talk about architectures.

总结本次讲座：一切都基于张量操作——参数、梯度、激活值、优化器状态、数据。我们介绍了 einops，希望大家能接受它作为思考张量操作的方法。**6 × 标记数 × 参数数** 这个公式现在已经被我们揭开了神秘面纱——它就是每个训练步的 FLOPs 数（这里的标记数应该是批大小）。我们还讨论了算术强度和屋顶线分析，用于诊断计算是内存受限还是计算受限。矩阵乘法是计算受限的，基本上其他所有操作都是内存受限的。最后，梯度累积和激活检查点是减少内存使用的方法，减少内存可以让你使用更大的批大小。今天的课程就到这里。下周，Tatsu 将讲架构。
