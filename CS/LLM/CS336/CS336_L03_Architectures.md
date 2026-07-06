---
title: "Lecture 3: Architectures"
---

# Lecture 3: Architectures – Everything You Didn't Want to Know / 第三讲：架构——你不想知道的一切

## 1. Introduction and Philosophy / 引言与哲学

Today, we're going to talk about architecture, which, at least to me, has always been pretty inscrutable. And so I'm going to take the approach of just telling you everything. I'm going to go through all of the modern papers, and we're going to just look through what has everyone done. So I've titled this "everything you didn't want to know about architectures and hyperparameters," because I think we all wished we lived in a world where the only things you had to know were like VC dimension or something—very simple theoretical tools—but that's not really where we are.

今天我们来讨论**架构（architecture）**，至少对我来说，这一直是很难理解的东西。所以我打算把一切和盘托出。我会讲解所有现代论文，看看大家都做了什么。我把这讲叫做"你不想知道的关于架构和超参数的一切"，因为我想我们都希望生活在一个只需要知道VC维度之类简单理论工具的世界里，但现实并非如此。

---

What we are going to do is try to understand architecture from a survey lens. The best thing to do, better than listening to this lecture even, is for you to go out and train your own models and try different architectures. That's by far the best thing to do—that's part of the philosophy of the course. But we're not going to be able to cover the whole design space of all the different architectures that are out there. That's not something that we have the compute or the time to do. So my opinion is, the second best thing that we could do is to try to learn from the experience of others. What has everyone else done? What are the choices that they are making? And by looking at a broader, somewhat zoomed-out picture, maybe we can start to understand: these are the kinds of parameters and choices that are fixed across all effective architectures, and these other ones can be varied without impacting how the model performs.

我们将从调研的角度来理解架构。比听这堂课更好的方法是自己去训练模型、尝试不同的架构——这是这门课的哲学之一。但我们无法覆盖所有架构的全部设计空间，因为我们没有那么多算力和时间。所以我认为，次优的选择是从他人的经验中学习。大家都做了什么？他们做了哪些选择？通过观察更广阔、更宏观的图景，也许我们能开始理解：哪些参数和选择在所有有效架构中是固定的，而哪些则可以自由变化而不影响模型性能。

---

So I'm going to talk about transformer variants—what is the modern Transformer starting with the Vaswani paper? And then as we go to more modern, more recent architectures, what do they have in common? And then what are we allowed to vary? I think many of you have taken an NLP course or at least seen a Transformer. So you've probably seen the very vanilla Transformer from Vaswani et al. There are some fairly standard choices that you make: you say, Transformers don't have positional dependence, so we're going to add a **position embedding（位置嵌入）**. We're going to add some sines and cosines. We're going to have information processing through ReLU. And then we're going to have a **post-norm（后归一化）**—I'll talk about what exactly that is later.

所以我要讲**Transformer（Transformer）**的变体：从Vaswani的论文开始，现代Transformer是什么样的？当我们考察更现代的、更新的架构时，它们有什么共同点？我们可以变动什么？我想你们很多人上过NLP课程，或者至少见过Transformer。你们大概看过Vaswani等人提出的非常原版的Transformer。有一些相当标准的选择：Transformer没有位置依赖性，所以我们加入**位置嵌入（position embedding）**，加上一些正弦和余弦信号。我们用ReLU处理信息，然后我们用**后归一化（post-norm）**——我等下会解释它具体是什么。

---

When you look at your assignment A1, you're going to notice some differences between the standard or vanilla Transformer and what we've asked you to implement. We're going to ask you to move the **LayerNorm（层归一化）** to the front of each transformer block. We're going to ask you to implement something called **RoPE（旋转位置编码）**. And we're going to ask you to implement something called SwiGLU and not ReLU. Why do we pick these? One reason is, we've copied a lot of this over from Llama—and so did everyone else. Really, if you were to train your own language model, you'll quickly run into this question: there are so many choices—what do I choose for all of these things?

当你看你的第一次作业A1时，你会注意到标准Transformer和我们让你实现的版本之间有一些差异。我们会让你把**层归一化（LayerNorm）**移到每个transformer块的前面，我们会让你实现**旋转位置编码（RoPE）**，以及让你实现SwiGLU而不是ReLU。为什么选这些？一个原因是我们从Llama那里借鉴了很多——其他人也都这么做了。说实话，如果你自己训练语言模型，你很快就会面临这个问题：选择太多了，我到底该选什么？

---

So let's now walk through all of these different models. The way I think about architectures is to look at all the different things people have done and ask, what are the things that people have done? Can we pick and choose from those? I try to look at all the different models that come out each year. There's Qwen2, and Gemma 3, and InternLM2. And then there were even more. There's Nemotron-4. There were 19 new dense models last year. And this year I thought, there can't be that many new LLM releases. People can't keep training 20 dense LLMs per year. And that's technically right—there aren't as many dense LLMs. Initially, there's Qwen3, Gemma 4 just came out last Thursday, and OLMo 3. But it turns out, if you start looking, there are a lot of different models. Most of these actually are MoEs (mixtures of experts), which I'll talk about tomorrow. Because we have such a big diversity of models, we actually get a pretty good picture of all the different choices that we can make.

那么让我们来看看所有这些不同的模型。我思考架构的方式是看看大家都做了什么，然后问：我们能否从中挑选和组合？我每年都会看所有新出的模型。有Qwen2、Gemma 3、InternLM2，还有Nemotron-4等等。去年有19个新的密集模型。今年我以为不会有那么多新的LLM发布了，人们不可能每年训练20个密集LLM。技术上确实如此——密集LLM没那么多了。有Qwen3、Gemma 4上周四才发布、OLMo 3。但事实证明，模型真的很多。大多数其实是MoE（混合专家），我明天会讲。正因为模型种类如此丰富，我们反而能对可选的各种架构选择有一个相当全面的认识。

---

## 2. Core Architecture Variations / 核心架构变体

### 2.1 Layer Norm Placement: Pre-Norm vs. Post-Norm / 层归一化的位置：前归一化 vs. 后归一化

If you take the Transformer paper, the thing that they really did not get right—I think most people agree—is where you put the layer norm. In the original Transformer paper, the layer norm goes in what you would call the residual path. You have the **residual stream（残差流）** that runs through the whole network. Then you apply attention, which does some computation and adds a delta back into the residual stream. In order to make sure that these gradients are stable across layers, a layer norm is placed at the end of each of these components. Now, instead of putting the layer norms in the residual stream, there's an alternative—I'll refer to this as **pre-norm（前归一化）**—in which you put the layer norm outside of the residual stream, but before each of the computations. So you can put it before the **multi-head attention（多头注意力）**, and before the **FFN（前馈网络/feed-forward network）**. We'll call the original approach **post-norm（后归一化）** or **residual norm**.

如果你看Transformer论文，有一个地方大多数人认为他们做错了，那就是层归一化放的位置。在原版Transformer中，层归一化放在所谓的残差路径中。你有一个**残差流（residual stream）**贯穿整个网络。然后你应用注意力计算，把增量加回残差流。为了确保梯度在各层之间稳定，每个组件末尾都放了一个层归一化。另一种替代方案——我称之为**前归一化（pre-norm）**——是把层归一化放在残差流之外，但在每次计算之前。你可以把它放在**多头注意力（multi-head attention）**之前，以及**前馈网络（FFN/feed-forward network）**之前。我们把原来的方式称为**后归一化（post-norm）**或残差归一化。

---

Basically, all modern language models push the layer norm outside of the residual stream. This is just something that basically everybody does. There is one funny exception—it is OPT-350M. If you are familiar with language models, we know OPT in general was a mess of a language model, and OPT-350M is even more so. So this is one of the things that everyone agrees on.

基本上所有现代语言模型都把层归一化推到残差流之外。这几乎是人人都做的事情。有一个有趣的例外——OPT-350M。如果你了解语言模型，你就知道OPT总体上就是一个混乱的模型，OPT-350M尤其如此。所以这是人人都达成共识的一件事情。

---

And so you might wonder, why is this such a unified thing? If you look at early work studying where to place the layer norm, the motivation was that when you train a Transformer, you need to do a warm-up. Wouldn't it be nice if we could remove the warm-up? But people quickly realized that removing the warm-up had very serious stability and convergence issues. If you did post-norm plus layer norm (the original Transformer approach), you just don't converge as well compared to doing something like pre-norm—you would get much nicer convergence even without warm-up. But really, what people quickly realized is that moving the layer norms outside the residual stream has some pretty important implications as you make your network deeper and start to grapple with stability issues.

你可能会问，为什么大家都统一做了这个选择？早期研究表明，最初的动机是训练Transformer时需要做warm-up（预热），如果能去掉warm-up就好了。但人们很快发现，去掉warm-up在稳定性和收敛性上有严重问题。用后归一化（原版Transformer的方式），你的收敛效果不如前归一化——即使没有warm-up，前归一化也能获得好得多的收敛效果。但真正重要的是，人们很快意识到，随着网络变深和稳定性问题加剧，把层归一化移到残差流之外有非常重要的影响。

---

To me, the gradient attenuation issues are the most clear. When you talk to people who do architecture design, one of the things people often say is: keep your residual stream clean. In pre-norm, your x's come in and propagate all the way up to the top—all the way to your final output. This allows gradients to propagate in the backward pass straight through. That makes gradient propagation very simple, which improves both stability and signal propagation. At initialization, with pre-norm, the gradient sizes remain the same because you have this nice, straight-through propagation in the backward pass. On the other hand, if you have post layer norm, you have complicated effects because each time you go through a transformer block with layer norm in the residual path, that changes the norm of your gradients as you go backwards. From the principle of "keep your residual stream clean," pre-norm makes a lot of sense.

对我来说，梯度衰减问题是最清晰的。你跟做架构设计的人聊天，他们经常说：**保持残差流干净**。在前归一化中，x从前向传播一直通到最顶层，到达最终输出。这使得梯度在反向传播中可以直通到底。这让梯度传播非常简单，同时提升了稳定性和信号传播。在初始化时，前归一化的梯度大小保持不变，因为反向传播有一条干净的直通路径。而如果你用后层归一化，每次通过一个transformer块时层归一化都在残差路径中，这会改变反向传播中梯度的范数，产生复杂的影响。从"保持残差流干净"的原则来看，前归一化非常有道理。

---

People also realized through experimentation that this improves stability in general—the sizes and frequencies of gradient spikes were improved under pre-norm compared to post-norm. Stability and the ability to go deep are both very, very important for modern large language models. So this idea of moving your layer norm outside of the residual stream is one that basically everyone has adopted.

人们还通过实验发现，这总体上提升了稳定性——前归一化相比后归一化，梯度尖峰的大小和频率都有改善。稳定性和深度扩展能力对现代大语言模型都至关重要。所以把层归一化移到残差流之外这一点，几乎人人都采纳了。

---

Now, if putting layer norms in residual streams is bad, why does layer norm have to be at the start? We could have it after computation as well—that's equally good under that logic. And that's exactly right. Many recent models, like Grok, or Gemma 2, or OLMo 2, have this structure where they've moved the layer norm after the computation. So it's a post-norm of a kind, but it's outside the residual stream. Other models still actually just put layer norms everywhere—they put a layer norm here, they put a layer norm after. One of the other lessons that seems to have held up very well is: if you have stability issues, you can sprinkle in layer norms everywhere, and that will generally improve stability.

那么，如果把层归一化放在残差流中不好，为什么层归一化必须在计算之前呢？我们也可以把它放在计算之后——按照那个逻辑，这是同等好的。确实如此。许多最近的模型，如Grok、Gemma 2或OLMo 2，把层归一化移到了计算之后。所以它算是一种后归一化，但它在残差流之外。其他模型干脆到处放层归一化——这里放一个，后面放一个。另一个经得起检验的经验是：如果你有稳定性问题，你可以到处撒层归一化，这通常会提升稳定性。

---

### 2.2 RMSNorm and Removing Biases / 均方根归一化与去除偏置项

In the original Transformer, you have **layer norm（层归一化）**: you have your activations x, you mean-subtract, divide by variance, and then scale it back up. This works just fine. But basically most or all modern models use **RMSNorm（均方根归一化）**, which doesn't subtract the mean or add a bias term—it's just a scaling down and scaling back up. LayerNorm is more expressive than RMSNorm, so there's really no representational reason why you have to use RMSNorm. But RMSNorm is nice because in practice there's really no expressiveness loss—RMSNorm models just as well as LayerNorm. But more importantly, it is faster.

在原版Transformer中，**层归一化（layer norm）**的操作是：对激活x做均值减法、除以方差、再缩放回来。这样做没有任何问题。但基本上所有现代模型都使用**均方根归一化（RMSNorm）**，它不减去均值、也不加偏置项——只是缩小再放大。LayerNorm比RMSNorm表达能力更强，所以从表征角度来说没有理由一定要用RMSNorm。但RMSNorm的好处是实践中没有明显的表达能力损失——RMSNorm和LayerNorm建模效果一样好。更重要的是，它更快。

---

This is the part where the systems and architecture co-design starts to come in. From the previous lecture, we talked about the idea of **arithmetic intensity**. We want to keep our GPUs hot by doing matrix multiplies and other very intense computations. We do not want to be wasting our GPUs by having them move little tiny bits of memory back and forth—that's a very inefficient use of our very powerful GPU. What we really want to do is remove operations that are small and involve memory movement but don't give us much expressive power. So, if the mean subtraction and addition isn't really doing much for us—just get rid of it.

这就是系统和架构协同设计的地方。上一讲我们讨论了**算术强度（arithmetic intensity）**的概念。我们希望让GPU保持繁忙，做矩阵乘法和其他高强度计算。我们不想让GPU把时间浪费在来回搬运小块内存上——那是对强大GPU的低效使用。我们真正想做的是移除那些计算量小、涉及内存搬运、但对表达能力贡献不大的操作。所以，如果均值减法和加法对我们帮助不大——那就直接去掉。

---

You might think, this is a teeny tiny operation that accounts for something like 0.17% of the total floating point operations. But as Percy mentioned, it's not really about the flops. Runtime is a much more complicated object. Statistical normalizations, even though they're only 0.17% of the flops, can be up to 25% of the runtime depending on your workload and setup. On tiny models this can be really big, because you're still having to move all these parameters back and forth from fast to slow memory and vice versa. So data movement is really, really important. And RMSNorm can still matter a lot because of this.

你可能会想，这只是一个微小的操作，占总浮点运算量的约0.17%。但正如Percy提到的，问题不在于flops。运行时间是一个复杂得多的东西。统计归一化操作（如LayerNorm），虽然只占flops的0.17%，但根据你的工作负载和配置，可能占运行时间的25%。在小模型上这可能非常大，因为你仍然需要在快速和慢速内存之间来回搬运所有参数。所以数据搬运真的非常重要，RMSNorm也因此仍然很重要。

---

This is another paper in which people evaluated different architecture interventions, Narang et al. in 2020. For a teeny tiny transformer of 200 million parameters, you get more steps per second when you switch to RMSNorm. And in fact, you actually get better performance, which is a nice bonus. So you get a free systems win by just moving to RMSNorm. And so basically, everyone has decided to move over to this now.

Narang等人在2020年的论文中评估了不同的架构干预。对于一个2亿参数的微型Transformer，切换到RMSNorm后每秒能跑更多步数。而且实际上还得到了更好的性能——这是一个额外的好处。所以仅仅切换到RMSNorm就能白捡一个系统性能提升。基本上现在大家都转移到RMSNorm了。

---

In general, biased terms in transformers and neural networks are generally not that useful. In the original Transformer, the linear terms all have biases, but most implementations actually just drop the biases entirely. Once again, this is another example of something that's not very arithmetically intense but fairly memory intensive, relatively speaking. So you might as well just drop these and get the free systems win. There are also some cases where the bias terms can induce stability issues. But really, the primary reason these are dropped is just to simplify things from a systems perspective.

总的来说，Transformer和神经网络中的偏置项通常用处不大。原版Transformer中所有线性层都有偏置，但大多数实现实际上直接去掉了偏置。这又是一个算术强度不高但相对内存密集的操作的例子。所以不如直接去掉，拿到免费的系统性能提升。还有些情况下偏置项还可能导致稳定性问题。但真正的主要原因是，从系统角度来看，去掉偏置可以简化一切。

---

So the layer norm story is pretty easy. Everyone moves the layer norm outside the residual stream—often pre-norm, though I think this might partially be because Llama 2 did that. We roughly have a sense of how to use layer norm to control gradient spikes and keep signal propagation nice. We also now basically always use RMSNorm. And you hopefully understand the general principle of just dropping bias terms, which allows us to keep our system more arithmetically intense while keeping the expressive power the same. From a lot of experimentation and now collectively acquired knowledge, we roughly know that dropping the bias terms on both the linear and RMSNorm is OK for typical language modeling workloads.

所以层归一化的故事很简单。大家都把层归一化移到残差流之外——通常是前归一化，尽管我怀疑部分原因是Llama 2这样做了。我们大致知道如何用层归一化来控制梯度尖峰和保持良好的信号传播。我们现在基本上都用RMSNorm。希望大家理解去掉偏置项的一般原则：这样可以在保持相同表达能力的同时，让系统算术强度更高。通过大量实验和积累的集体知识，我们大致知道在典型的语言建模任务中，去掉线性和RMSNorm中的偏置项是没问题的。

---

### 2.3 Activation Functions: From ReLU to Gated Linear Units / 激活函数：从ReLU到门控线性单元

There's a whole zoo of activations—ReLU, GeLU, Swish, GeGLU, SwiGLU. At one point in my stats ML training I thought, I will make it a point of pride to never know what a SwiGLU is. But now, it's actually very important for us to actually have a general sense of what these objects are and which parts of these names actually matter for performance. You can build and train a language model on a fairly vanilla activation. Chinchilla is probably the best model out of that group. Even if you just use ReLU, you can train a reasonably performant language model. If we move to GeLU—a Gaussian error unit—the only difference is a tiny divot at the bottom. Then you can train models like GPT-3. That's perfectly fine.

有一整个激活函数的动物园——ReLU、GeLU、Swish、GeGLU、SwiGLU。在我统计机器学习训练生涯的某个阶段，我曾骄傲地认为我永远不需要知道SwiGLU是什么。但现在，我们确实需要大致了解这些东西是什么，以及这些名字中哪个部分对性能真正重要。你可以用相当原始的激活函数训练语言模型，Chinchilla大概是那类模型中最好的一个。即使只用ReLU，你也能训练出性能还不错的语言模型。如果换成GeLU（高斯误差线性单元），唯一的区别是底部的一个小凹陷。然后你就可以训练出GPT-3这样的模型。这完全没问题。

---

But then we get to the **gated linear units（门控线性单元/GLU）**, like SwiGLU and GeGLU. And these are really where most of the action is. Almost all credible modern language models use a gated linear unit of some kind. So what is a gated linear unit? In a standard ReLU feed-forward layer, you have x, you hit it with W1, you entrywise threshold at 0, and then you hit it with another W2 to get your output. Very straightforward. Another thing that is often said in architecture design is that gating is often very helpful. Instead of just having an entrywise ReLU, why don't we also have a gate? The second gate is just going to multiply the output of my ReLU entrywise. So you have x·W1, and you gate that with x·V. Then you down-project it back with W2. Now this is a ReGLU—you make these names by adding the first activation (ReLU) and GLU—so the ReLU-gated linear unit.

但当我们谈到**门控线性单元（GLU/gated linear unit）**，如SwiGLU和GeGLU，这才是真正的核心。几乎所有可信的现代语言模型都使用某种门控线性单元。那么什么是门控线性单元？在标准的ReLU前馈层中，x乘以W1，逐元素阈值到0，再乘以W2得到输出——非常简单。在架构设计中人们常说门控往往很有帮助。与其只有一个逐元素ReLU，为什么不加一个门控？第二个门控项逐元素地乘以ReLU的输出。所以你有x·W1，然后用x·V来做门控，再用W2下投影回来。这就是ReGLU——名字由第一个激活函数（ReLU）加上GLU组成。

---

If you take a GeLU, you will get a GeGLU. If you take a SwiGLU (x times a sigmoid), then you will get a SwiGLU. Generally, the Google folks have used GeGLU (Gemma models, T5 models). Everything that's a Llama descendant uses a SwiGLU—PaLM and the Llama descendants are all SwiGLU models. I would say that SwiGLU is probably the more dominant one, but honestly, amongst the gated units, doesn't really matter.

如果你用GeLU，就得到GeGLU。如果你用SwiGLU（x乘以sigmoid），就得到SwiGLU。通常，Google团队使用GeGLU（如Gemma、T5系列）。所有Llama的后代都使用SwiGLU——PaLM和Llama后裔都是SwiGLU模型。SwigLU可能是更主流的选择，但说实话，在门控单元之间差别不大。

---

Here's a side note that will be important later. If you look at the gated model, there are more parameters because you have this parameter V—you now have three matrices instead of two. So what you should do is use a smaller **feedforward dimension** by a factor of 2/3 in order to keep the parameter count the same. This is roughly the idea: I want to keep the same number of total parameters as my original **MLP**, but now I want to make it gated, so I make the feedforward dimension a little smaller by 2/3. This is a general rule of thumb that people have followed, but it's not an iron rule. The original Noam Shazeer paper that proposed this had some very small but consistent deltas. The GLU variants are almost always consistently better than the non-GLU variants in parameter-matched comparisons.

这里有个重要的附注。门控模型有更多参数，因为多了参数V——现在有三个矩阵而不是两个。所以你应该把**前馈维度（feedforward dimension）**缩小到原来的2/3，以保持参数数量相同。思路大致是：我想保持和原来**MLP**相同的总参数数，但要变成门控的，所以把前馈维度缩减约2/3。这是人们普遍遵循的经验法则，但不是铁律。Noam Shazeer最初提出这个的论文显示，增益虽小但持续一致。在参数匹配的比较中，GLU变体几乎总是持续优于非GLU变体。

---

Evidence is pointing towards consistent gains on using these gating tricks. The GLUs do significantly better at loss or downstream metrics. So the important single axis to know is that gating for these nonlinearities is actually quite important—it gives you a nice boost without much of a computational cost. That's not to say gated linear units are necessary. GPT-3 used GeLU. The Nemotron 340B model used a Squared ReLU—a crazy choice, but that works too. But it's actually quite rare to see anything that's not trained on a gated linear unit.

证据表明使用门控技巧能持续获得增益。GLU在损失和下游指标上都显著更好。所以最重要的一点是：对这些非线性函数做门控确实很重要——它给你很好的提升而计算成本几乎不增加。这并不是说门控线性单元是必需的。GPT-3用GeLU，Nemotron 340B用了Squared ReLU——一个疯狂的选择，但也work。不过现在确实很少看到不用门控线性单元训练的模型了。

---

### 2.4 Parallel vs. Serial Transformer Blocks / 并行 vs. 串行Transformer块

Normally, we do our transformer blocks serially—compute attention, then compute the MLP, one after the other. If you're very systems-minded, you might say this introduces a bottleneck: I have to wait for the computation of one to do the other. If they were instead in parallel, I could bring to bear some new and cool systems optimizations. So could we parallelize the transformer block? This was originally an idea in GPT-J and was also used in PaLM. Instead of nesting attention and MLP sequentially, you just add together the output of the MLP and the attention layer and add both back into the residual stream. If you implement this right, you can share the layer norms and fuse the matrix multiplies.

通常我们串行执行transformer块——先计算注意力，再计算MLP，一个接一个。如果你有严重的系统思维，你可能会说这引入了瓶颈：我必须等一个计算完成才能做下一个。如果它们是并行的，我就可以利用一些新的、很酷的系统优化。那么我们能否并行化transformer块？这最早是GPT-J中的一个想法，PaLM也用了。与其嵌套注意力和MLP，你只需要把MLP和注意力层的输出加在一起，再一起加回残差流。如果实现得当，你可以共享层归一化，并融合矩阵乘法。

---

However, this has been an approach that has really fallen out of popularity over the past two years. I think mainly because optimization of the serial form has gotten sufficiently good that the systems gains from the parallel form just isn't worth the small hits to representation power. Effectively, you can think about it as you've lost half of your depth, and that can be deleterious to your model. So in terms of architecture changes, the fact that this section is so short should suggest to you how much the original Transformer formulation has somewhat stood the test of time. The only things we're really changing are where the norms go, whether we have bias terms, or whether we gate the MLPs. Those are actually pretty minor changes compared to all the things that you can do.

然而，这种方法在过去两年中确实已经失宠了。我认为主要原因是串行形式的优化已经足够好，并行形式带来的系统增益不值得承受表达能力上的小幅损失。实际上，你可以认为你失去了一半的深度，这对模型可能是有害的。所以就架构变化而言，这一节这么短应该向你说明了，原版Transformer的公式设计在多大程度上经受住了时间的考验。我们真正改动的只是层归一化的位置、是否有偏置项、或者是否给MLP加门控。与你可以做的所有改动相比，这些其实是相当小的变化。

---

### 2.5 Summary of Core Architecture Trends / 核心架构趋势总结

Looking across models: blue is RMSNorm, black is LayerNorm. Most modern models are RMSNorm models. Serial versus parallel layers—most are serial. Pre-norm versus post-norm—some marked as post-norm are actually pre- and post-norm. And then GLUs—almost always, with the exception of things like Falcon which use a gated linear unit. But almost all modern models are really gated linear units. So you can see the trends quite visually.

纵观各种模型：蓝色代表RMSNorm，黑色代表LayerNorm。大多数现代模型使用RMSNorm。串行与并行层——大多数是串行的。前归一化与后归一化——有些标记为后归一化的其实是前后都做了归一化。关于GLU——几乎总是使用，Falcon等少数例外也用的是门控线性单元。几乎所有现代模型都使用门控线性单元。你可以很直观地看到这些趋势。

---

## 3. Position Dependence and RoPE / 位置依赖与旋转位置编码

Now, the thing that is very different across implementations, and a place where a lot of the architecture stuff is still in flux, is how you do position dependence and incorporate information from other positions. There are lots of different ways to encode position into a Transformer. This is very, very important because attention is positionally independent—they're just inner products, so you can just shuffle them and attention would be the same if you don't have a position embedding.

现在，不同实现之间差异很大的地方——也是架构设计还在不断变化的地方——是如何处理位置依赖并整合来自其他位置的信息。有很多不同的方式可以将位置编码到Transformer中。这非常非常重要，因为注意力是位置无关的——它只是内积，没有位置嵌入的话，你可以任意打乱它们，注意力输出保持不变。

---

The original Transformer had sine and cosine embeddings—a Fourier transform intuition that if you have sines and cosines, you can recover position from that. A number of other large models used absolute embeddings, where each position had its own different embedding. Several Google models use relative embeddings, where you add a vector to the attention computation itself—if you're three positions off, the attention matrix gets a different offset. Models like T5 and Chinchilla use this scheme.

原版Transformer使用正弦和余弦嵌入——基于傅里叶变换的直觉：有了正弦和余弦，你就能从中恢复位置信息。一些后续的大模型使用绝对位置嵌入，每个位置有自己的嵌入向量。Google的一些模型使用相对嵌入，在注意力计算本身中加入一个向量——如果你相隔三个位置，注意力矩阵会加上一个不同的偏移量。T5和Chinchilla等模型使用这种方式。

---

The thing that has really become pretty dominant in terms of position embedding is **RoPE（旋转位置编码/Rotary Position Embedding）**. Most models past 2024 use this type of embedding. It's remarkable, given that RoPE in some ways came out of nowhere—originally it was a GPT-J innovation from a blog post and paper combination from an author in China. But really, it has some really interesting ideas.

在位置嵌入方面真正占据主导地位的是**旋转位置编码（RoPE/Rotary Position Embedding）**。2024年之后的大多数模型都使用这类嵌入。这很了不起，因为RoPE某种程度上是凭空冒出来的——最初它是GPT-J的一个创新，来自中国一位作者的博客论文组合。但它确实有一些非常有趣的思想。

---

RoPE is a relative position embedding. Let's make an opinionated stance: I should not care about the absolute position of any words. If "A" and "apple" appear together, even if at the start or the end, in RoPE embeddings they should get the same result. We want the inner product of these embeddings to be equal to a function that only depends on the relative difference. Every existing embedding before it didn't really fulfill this equality. Sines are not relative because they have absolute cross terms. Absolute position embeddings are obviously not relative. And relative embeddings, technically, are relative but they're not embeddings because they're just adding to the attention matrix—there's no inner product structure.

RoPE是一种相对位置嵌入。我们来摆明立场：我们不应该关心任何词的绝对位置。如果"A"和"apple"一起出现，无论在句子开头还是末尾，在RoPE嵌入中它们应该得到相同的结果。我们希望这些嵌入的内积等于一个只依赖于相对位置的函数。之前所有的嵌入方式都不真正满足这个等式。正弦嵌入不是相对的，因为它有绝对交叉项。绝对位置嵌入显然不是相对的。而相对嵌入虽然技术上是相对的，但它们不是真正的嵌入，因为它们只是加到注意力矩阵上——没有内积结构。

---

So the idea is very cool. We want our embeddings to be invariant to absolute positions, and we know that inner products of any kind are invariant to arbitrary rotation. So the idea is: take my semantic word vectors (independent of any position), and then rotate each of these vectors based on the position that the words appear. For example, "we" is at position 0—don't touch it. The word "no" is at position 1—rotate it by some angle. Now, if "we" and "no" appear later at positions 2 and 3, they each get rotated by 2 and 3 positions respectively. But the relative angle between these two is still separated by 1. So this is a very, very simple idea of just using rotations to represent position. Anytime we take an inner product, those inner products are going to be invariant of absolute positions.

这个想法非常酷。我们希望嵌入对绝对位置不变，而我们知道任何形式的内积对任意旋转都是不变的。所以思路是：取语义词向量（与位置无关的），然后根据词出现的位置旋转每个向量。例如，"we"在位置0——不动它。"no"在位置1——旋转某个角度。如果后来"we"和"no"出现在位置2和3，它们分别被旋转2和3个位置。但它们之间的相对角度差仍然是1。这是一个非常简单的想法：用旋转来表示位置。任何时候我们做内积，这些内积都会对绝对位置不变。

---

Now, in high dimensions, there's an infinite space of ways to rotate vectors. What do you do in D dimensions? The simplest possible thing—reduce it to the 2D case repeatedly. Cut your D-dimensional vector into chunks of two. Each pair of two dimensions gets rotated. The theta at which these things rotate varies—some are very low frequency (rotating slowly, capturing long-range dependence), some rotate very quickly (capturing things like whether words are neighbors). After rotating every pair of vectors, you get your final embedding. That's the RoPE approach.

现在，在高维空间中，旋转向量的方式有无穷多种。在D维中怎么办？最简单的做法——反复归约到2维。把D维向量切成两两一组。每对二维被旋转。旋转的角度（theta）各不相同——有些频率很低（旋转很慢，捕捉长程依赖），有些旋转很快（捕捉词之间是否是邻居）。旋转完每对向量后，就得到最终的嵌入。这就是RoPE方法。

---

In practice, you take your vector and do a sparse multiply with sines and cosines. You apply those cosines and sines onto both your queries and keys for your attention computation. And you do this at the attention level rather than at the very bottom, to enforce position invariance every time you're doing attention computations. It is a little bit confusing, but once you understand the geometry of just rotating things, it's actually fairly straightforward.

实践中，你取向量与正弦和余弦做稀疏乘法。你把那些余弦和正弦同时应用到注意力的查询（query）和键（key）上。你在注意力层面而不是在最底层做这件事，以确保每次做注意力计算时都强制执行位置不变性。它有点令人困惑，但一旦你理解了旋转的几何含义，其实相当简单。

---

## 4. Hyperparameters / 超参数

I think hyperparameters are really something you start to engage with once you actually have to train a model. When your knowledge about language models is abstract, you don't have to care about any of these. But once you have to instantiate it, you start to ask questions like: how big should the feedforward size be? How many heads should I have? What should my vocabulary size be? Do I need very deep models or very wide models? If you start out with no knowledge, it's actually very daunting because you have to search this very big high-dimensional space. But the space of things that people try is actually pretty small.

我认为**超参数（hyperparameter）**是当你真正要训练模型时才会接触到的东西。当你对语言模型的知识还停留在抽象层面时，你不需要关心这些。但一旦要实例化模型，你就开始问：前馈层应该多大？应该有多少个注意力头？词汇表大小应该是多少？我需要很深还是很宽的模型？如果你从零知识开始，这会非常令人望而生畏，因为你必须搜索一个非常高维的空间。但实际上人们尝试的空间非常小。

---

### 4.1 Feedforward Ratio / 前馈比例

One of the really consensus hyperparameters is the **feedforward ratio（前馈比例）**—the ratio between the feedforward size (the output of your first matrix multiply in an MLP) and the model dimension. For whatever reason, it should maybe be four times your hidden dimension. This is a rule of thumb that works remarkably well. There are a few exceptions. Exception number 1: variance of the gated linear unit. GLUs have more parameters if you keep the same dimensions, so if you want to keep the parameter size the same, you need to scale down by 2/3. So most GLU variants end up with something like 2.6–2.7. Then the Llama 2 folks, because they had very efficient attention heads with MQA, multiplied this ratio by an arbitrary 1.33 to get roughly 3.5. So either 2.6-ish or 3.5 for GLUs, or 4 if you're doing non-GLU models.

一个非常有共识的**超参数**是**前馈比例（feedforward ratio）**——即前馈大小（MLP中第一个矩阵乘法的输出维度）与模型维度之比。不知为何，它应该是隐藏维度的四倍。这是一个效果非常好的经验法则。有几个例外。第一个例外：门控线性单元的变体。GLU在保持相同维度时有更多参数，所以如果你想保持MLP的参数数量不变，就需要乘以2/3。所以大多数GLU变体的比例最终约为2.6-2.7。然后Llama 2团队，因为他们使用了非常高效的注意力头（MQA），把这个比例乘以了任意的1.33，得到约3.5。所以GLU模型用约2.6或3.5，非GLU模型用4。

---

There's another exception—T5 decided to have a 64x multiplier, which is way bigger than 4. They had a reasonable systems-based argument: the bigger my matrix multiplies, the more efficient I can keep my hardware. But T5 is an astounding exception at 64—I don't think any other model has gone that high. Empirically, if you look at controlled comparisons, like Kaplan et al. in 2020, there's a basin where this hyperparameter is pretty good and very, very flat between about 1 and maybe 10. If you get it really wrong above 10 to 100, your loss starts really shooting up. So a lot of these choices that range between 2.6 to 4 all fall into this relatively nice basin. The funniest part: T5 v1.1, the follow-up improved version, went back to the standard 2.5 multiplier.

还有一个例外——T5决定用64倍乘数，远大于4。他们有一个合理的系统级论证：矩阵乘法越大，硬件利用效率越高。但T5的64倍是惊人的例外——我认为没有其他模型达到过这么高。经验上，如果你看受控比较，如Kaplan等人2020年的工作，在1到约10之间有一个很好的平坦谷底区，超参数在这个范围内表现很好。如果错得太离谱，到了10到100以上，损失就会急剧上升。所以从2.6到4的这些选择都落在这个相当好的谷底区。最有趣的是：T5 v1.1，即T5的改进版，回到了标准的2.5倍乘数。

---

### 4.2 Head Dimension / 头维度

If you have multi-head attention with multiple heads, the canonical thing to do—the thing that almost everyone does—is to make sure that the size of those heads, the **head dimension（头维度）**, is such that you have the same dimension as a single-head transformer. You always make sure that you divide the hidden dimension to multiply with h: you have h the number of heads, and the dimension of each head is d/h. So you multiply the two and you get d. For some reason, this is the rule of thumb. Of course, this doesn't have to be true—we can arbitrarily change the ratios. But most models do follow this guideline and it turns out to work pretty well. Looking at a variety of models, the ratios are roughly around one. This is yet another forgiving hyperparameter—there's a pretty wide basin around one that you can get away with.

如果你有**多头注意力（multi-head attention）**，规范的做法——几乎人人都在做的——是确保那些注意力头的维度，即**头维度（head dimension）**，使得总维度与单头Transformer相同。你总是确保把隐藏维度除以头数再乘以h：h是头数，每个头的维度是d/h。两者相乘得到d。不知为何，这是一个经验法则。当然这不必为真——我们可以任意改变比例。但大多数模型遵循这个规则，而且效果很好。纵观各种模型，比例大约都在1左右。这又是一个宽容的超参数——在1附近有一个相当宽的谷底区，你可以随意取值。

---

### 4.3 Aspect Ratio / 宽深比

One of the most critical and interesting ones conceptually is the **aspect ratio（宽深比）**—how wide your model is versus how deep it is. When you scale models up or down, the way you usually do that is you fix an aspect ratio and then make the model bigger. The aspect ratio controls the entire depth-to-width trade-off as you make models bigger. There is a lot of variation, much more so than other hyperparameters. But there's actually a fairly clear sweet spot: you don't see models go too deep, and you don't see models go too wide. Most models have a ratio of about 100×d_model over n_layers—about 100 in width for every layer you have. This is true for GPT-3, Llama, and many others.

概念上最有趣也最关键的超参数之一是**宽深比（aspect ratio）**——模型宽度与深度之比。当你放大或缩小模型时，通常的做法是固定一个宽深比，然后把模型整体变大。随着模型变大，宽深比控制着整个深度与宽度的权衡。这个参数的变异性比其他超参数大得多。但实际上有一个相当明确的甜点区间：你不会看到模型太深，也不会看到模型太宽。大多数模型的比例约为d_model / n_layers ≈ 100——即每层对应约100的宽度。这对GPT-3、Llama等很多模型都成立。

---

The considerations are partly a trade-off between expressiveness and hardware. Extremely deep models get very annoying to deal with systems-wise—if you cut up your layers depth-wise, you have very serious issues in parallelization (pipeline parallel, which most people really do not want to deal with). Width is much easier to parallelize—if you have a really wide model, you can cut that up very easily across GPUs (tensor parallel). So there are systems reasons to go wide and maybe expressiveness reasons to go deep, and you end up at roughly 100. Kaplan et al. show that regardless of model size, the optimum aspect ratio is fairly similar at about 100. A broader conclusion is: as you increase the flops, the models get better—that's really controlling the majority of the effects, not necessarily the aspect ratio. There's a general forgiving band of hyperparameters, and you really worry primarily about your system's utilization.

这些考量部分在于表达能力和硬件之间的权衡。极深的模型在系统层面非常麻烦——如果你按深度切分各层，并行化会有严重问题（即管道并行，大多数人真的不想碰）。宽度则容易并行得多——如果模型很宽，你可以很容易地把它切分到多个GPU上（即张量并行）。所以有系统上的理由去选择更宽，也有表达能力上的理由去选择更深，最终大家收敛到约100。Kaplan等人的研究表明，不管模型大小，最优宽深比都大约在100附近。更广泛的结论是：随着flops增加，模型变得更好——这才是控制大多数效果的因素，而不一定是宽深比。存在一个普遍宽容的超参数区间，你主要需要考虑的是系统利用率。

---

### 4.4 Vocabulary Sizes / 词汇表大小

There's a really clear difference between two classes of models. In the early days of open-source model training, there were a lot of monolingual models whose only goal was to be good on English. For those models, you had much smaller vocab sizes in the 30,000 range. Post-Llama, a lot of people were interested in multilingual or production systems (including closed-source models like GPT-4). All of these have much larger vocab sizes, roughly in the 100,000 to 200,000 range. Google models have a ton more vocabulary. Llama derivatives roughly range at about 100,000 tokens. Monolingual models are about 30,000. The multilingual models really do need much larger vocabularies to cover the whole space. There have been scaling law studies showing that the bigger your model, the larger the vocabulary it can handle.

两类模型之间有非常明显的区别。在开源模型训练的早期，有很多单语模型，唯一目标是在英语上表现好。这些模型的词汇表大小小得多，约3万左右。Llama之后，很多人对多语言或生产系统感兴趣（包括GPT-4等闭源模型），它们的词汇量大得多，大约在10万到20万之间。Google模型的词汇量更大。Llama衍生品的词汇量大约在10万token左右。单语模型约3万。多语言模型确实需要更大的词汇表来覆盖整个空间。缩放定律研究也表明，模型越大，能处理的词汇表也越大。

---

### 4.5 Regularization: Dropout and Weight Decay / 正则化：Dropout与权重衰减

I think dropout and regularization is another very counterintuitive topic from your Machine Learning 101 intuition. In language modeling, I have a lot of data—more data than I can process most of the time. I'm probably not even going to see the same data twice. There's very good reasons to believe that a single pass of SGD is never really going to memorize my data very much. So overfitting is not really a problem during compute-constrained language modeling. Given this, should I use dropout or weight decay? If you look at models, you find a lot of models do both—especially weight decay is actually fairly popular even for modern high-performance language models. This is very mystifying. Why is this?

我认为dropout和正则化是另一个与你的机器学习101直觉非常矛盾的领域。在语言建模中，数据量很大——大多数时候我甚至处理不完所有数据。我可能根本不会看到同样的数据两次。有充分的理由相信，单次SGD训练不会真正记住太多数据。所以在算力受限的语言建模中，过拟合几乎不是问题。既然如此，我应该用dropout还是权重衰减？如果你看各种模型，会发现很多模型两者都用——尤其是权重衰减，即使在现代高性能语言模型中仍然很流行。这非常令人费解。为什么呢？

---

There have been papers arguing and showing nice evidence that weight decay is actually not a regularizer sometimes—it actually interacts with the optimizer to essentially make optimization better. With different weight decay settings on single-pass SGD, you don't really see any difference in training vs. validation loss—no overfitting. But if you look at weight decay combined with learning rate decay, the stronger weight decay runs do significantly better because they start out slow but end up converging to a much better minimum later. So weight decay is actually an optimization intervention and not necessarily a regularization intervention. Always keep in mind that these kinds of unexpected effects can really start to kick in.

有论文论证和展示了一个很好的证据：权重衰减有时实际上不是正则化器——它与优化器相互作用，本质上是让优化变得更好。在单次SGD训练中，不同权重衰减设置下，训练损失和验证损失几乎没有差异——没有过拟合。但如果把权重衰减和学习率衰减结合起来看，更强的权重衰减跑出了显著更好的结果，因为一开始慢，但最终收敛到更好的最小值。所以权重衰减实际上是一种优化干预，而不一定是正则化干预。永远记住，这类意想不到的效应真的会出现。

---

## 5. Training Stability / 训练稳定性

Over the last few years, a really big emphasis has not been on performance alone—it has actually been on stability. This becomes an increasingly important concern as your models get more and more expensive to train. If your model suddenly blows up some part into training with horrible-looking spikes, you might end up with a model that is actually not very good quality, or it might be unrecoverable. You might have spent millions of dollars in training and get to a point where the model is no longer able to be trained any further. So you don't want to train models that look like the blue curve with spikes everywhere.

过去几年中，一个非常大的重点不只是性能——而是训练稳定性。随着模型训练成本越来越高，稳定性变得越来越重要。如果你的模型在训练中途突然爆炸，出现可怕的尖峰，最终可能得到一个质量很差的模型，甚至可能是不可恢复的。你可能花了数百万美元训练，结果模型再也无法继续训练。所以你不想训练出那种到处是尖峰的蓝色曲线模型。

---

### 5.1 The Z-Loss Trick / Z损失技巧

If you have stability issues in language models, there are a few usual suspects. One of them is the softmaxes. The softmax has two things that are both really bad for stability: an exponential (which blows up very quickly), and dividing two numbers (also potentially very dangerous). Where are the softmaxes? There's one on the output side (outputting probability distribution) and another in attention (normalizing attention). Let's start with the output softmax. We want to compute a log probability: it's the output of your model u minus the log normalizer. If u is well-behaved, the first term is fine. But the second term, log z, might not be OK—if z is really big or really small, it could blow up.

如果语言模型有稳定性问题，有几个常见的嫌疑人。其中之一是softmax。softmax有两个对稳定性非常不利的因素：指数（爆炸得非常快）和两个数的除法（也可能非常危险）。softmax在哪里？输出端有一个（输出概率分布），注意力里还有一个（归一化注意力）。先从输出的softmax开始。我们要计算对数概率：它是模型输出u减去对数归一化器。如果u表现良好，第一项没问题。但第二项log z可能不行——如果z非常大或非常小，它都可能爆炸。

---

What can we do? Notice that the softmax is overparameterized—you can push constants in and out. If you add a constant to u, you can manipulate z without really affecting the softmax output (it cancels out). Because of this property, you can add a regularizer: a squared log z term that penalizes how far away log z is from 0. If log z is near 0, the whole expression is numerically stable. This is called the **Z-loss trick**. It was pioneered by Jacob Devlin back in 2014 and has become popular again through open-source models—Baichuan was the first open-source model to do it, then DCLM and OLMo and others have used this trick to stabilize their output softmaxes. This is a surprisingly effective thing.

我们能做什么？注意softmax是超参化的——你可以把常数移来移去。如果给u加一个常数，可以操纵z而不真正影响softmax的输出（常数会抵消）。因为这个性质，你可以加一个正则化器：一个平方的log z项，惩罚log z偏离0的程度。如果log z接近0，整个表达式就是数值稳定的。这叫做**Z损失技巧（Z-loss trick）**。Jacob Devlin在2014年首创了这个方法，后来通过开源模型再次流行起来——Baichuan是第一个使用它的开源模型，然后DCLM和OLMo等也用了这个技巧来稳定输出的softmax。这效果出奇地好。

---

### 5.2 QK-Norm / QK归一化

Now we turn our attention to the other potential problem: attention. Lots of degeneracies happen here. The high-level thing I'll say is: if you have instability, if you can throw a layer norm in there, somehow, it might control it. That's the design philosophy behind **QK-norm**. In the standard attention operation, you have your Qs and Ks that are going to be multiplied together and then go into the softmax. What happens if we just throw in a layer norm before we multiply the Qs and Ks? Then the inputs to this matrix multiply and therefore the inputs to the softmax roughly have the same scale—always roughly one, because we've used RMSNorm to divide the size of those Qs and Ks. If we do that, we keep the softmax operation stable.

现在我们把注意力转向另一个潜在问题：注意力。这里会发生很多退化现象。我要说的宏观结论是：如果你有稳定性问题，只要往里面扔一个层归一化，某种程度上它就可能控制住。这就是**QK归一化（QK-norm）**背后的设计哲学。在标准注意力操作中，Q和K会被相乘然后进入softmax。如果我们在Q和K相乘之前插入一个层归一化会怎样？那么矩阵乘法的输入以及softmax的输入，尺度大致相同——总是大约为1，因为我们用RMSNorm除以了Q和K的大小。这样做就能保持softmax操作稳定。

---

Tons of different models do this. It's originally from the multimodal world—folks making multimodal models initially discovered QK-norm (Idefics and Chameleon really used it and proved it out). Then a number of open-source language models realized the same tricks are entirely applicable to stabilizing attention for language models. This is now very, very standard. It doesn't seem to affect performance from lots of different training runs, but it does definitely prevent the kinds of attention degeneracies.

很多不同的模型都在用这个。它最初来自多模态领域——做多模态模型的人最初发现了QK归一化（Idefics和Chameleon真正使用了它并验证了效果）。然后一些开源语言模型意识到同样的技巧完全适用于稳定语言模型的注意力。现在这已经是非常非常标准的做法了。从大量训练来看，它似乎不影响性能，但确实能防止注意力的各种退化现象。

---

So the pattern is: we have layer norms initially in the pre-norm. Now we add them after the nonlinearities in each block. And now we're throwing them in both the Qs and the Ks. Really, this is the stabilization tricks that people apply.

所以模式是：最初在前归一化中有层归一化。现在我们在每个块的非线性之后也加上它们。然后我们还在Q和K中都加入它们。这就是人们应用的稳定化技巧。

---

### 5.3 Logit Soft-Capping / Logit软截断

The final stability intervention is **logit soft-capping**—a much harder intervention that some people apply. With QK-norm, we control the inputs to the softmax and hope the outputs are well-behaved. If we really, really want to enforce well-behaved outputs, we can take the logits (the things that go straight into the softmax) and just cap them off so they can never be too large or too small. This is almost a hard constraint—it's called a soft cap because a Tanh is bounded at some value. The Gemma models (Gemma 2, 3, and 4) all use the logit soft-cap trick—they take all logits for the attention layers and soft-cap them at some value. Some NVIDIA folks did systematic comparisons and found that while QK-norm lets you crank up the learning rate a little bit, soft-capping alone actually ends up losing performance. It's a very strong intervention—you can never express very confident signals in your softmax beyond a certain point. So it has some negative consequences, but it is a very safe way of stabilizing.

最后的稳定性干预是**logit软截断（logit soft-capping）**——一些人使用的一种更强的干预。QK归一化是控制softmax的输入并期望输出表现良好。如果我们真的想强制输出表现良好，我们可以取logit（直接进入softmax的值）并截断它们，使其永远不会太大或太小。这几乎是一个硬约束——之所以叫软截断，是因为Tanh在某个值处有界。Gemma系列模型（Gemma 2、3和4）都使用logit软截断技巧——它们对注意力层的所有logit在某个值处做软截断。NVIDIA的一些人做了系统比较，发现QK归一化能让你稍微提高学习率，而单独使用软截断反而会损失性能。这是一个非常强的干预——你无法在softmax中表达超出某个点的非常确信的信号。所以它有一些负面后果，但这是稳定化的一个非常安全的方法。

---

## 6. Attention Efficiency Tricks / 注意力效率技巧

### 6.1 Grouped Query Attention (GQA) / 分组查询注意力

Let's think about deployment. You've trained this very big model and now you need to serve it to lots of users. You'll pay for two different resources: your flops (computation) and your memory accesses. Both need to be small. During training or prefill, when you're looking at your prompt, the arithmetic intensity is pretty good—as long as your head dims are big enough and your sequences are long enough, your GPUs are fully utilized. Great.

让我们想想部署。你训练了一个很大的模型，现在要服务给很多用户。你需要为两种不同的资源付费：flops（计算）和内存访问。两者都需要很小。在训练或预填充阶段（处理提示词时），算术强度是很好的——只要头维度足够大、序列足够长，GPU就会被充分利用。很好。

---

Now we're serving users—generating tokens one by one. I can't parallelize the generation process. I generate a token, condition on it, generate the next token, repeat. The efficient way to do this is to maintain all past keys and queries in a **KV cache（KV缓存）**. The KV cache maintains this matrix of Q·K over the past, and whenever I need to compute something new, I can reuse the submatrices I've already computed. I only need to compute the new query-key interactions. This saves a lot on compute. But the issue is: now my arithmetic intensity is not so good. Each step, I have to read in my parameters and take dot products. Because I'm doing this incrementally, my memory access pattern now has an n×d² term. The arithmetic intensity now has n/d + 1/b. So what we need is large batches plus short sequence length, or really big model dimensions. That n/d term (sequence length over hidden dim) is very difficult to reduce.

现在我们在服务用户——逐个生成token。生成过程无法并行——生成一个token，以其为条件生成下一个，重复。高效的做法是在**KV缓存（KV cache）**中维护所有过去的键和查询。KV缓存维护过去所有Q·K的矩阵，当需要计算新东西时，可以重用已经计算过的子矩阵。只需要计算新的查询-键交互。这节省了大量计算。但问题是：现在算术强度不好了。每一步都要读入参数、做点积。因为是增量计算的，内存访问模式现在有n×d²项。算术强度变成n/d + 1/b。所以我们需要大批量加短序列，或者非常大的模型维度。n/d项（序列长度/隐藏维度）很难减小。

---

This leads to **MQA**, or **Multi-Query Attention（多查询注意力）**. Normally you have multiple heads with different keys, values, and queries. One thing we could do is keep the Ks and Vs the same across all heads—only the queries differ across heads. This drastically reduces the amount of items that need to be moved in and out of memory because the KV cache is now much smaller. The key term n/d now has h multiplying it, which significantly increases arithmetic intensity if you have a lot of heads. But the issue with MQA is: you do lose significant expressive power.

这就引出了**MQA，即多查询注意力（Multi-Query Attention）**。通常多个头有各自的键、值和查询。我们可以让所有头共享相同的K和V——只有查询在各头之间不同。这大幅减少了需要在内存中进出搬运的量，因为KV缓存现在小了很多。关键项n/d现在有h乘它，如果头数多，这显著提高了算术强度。但MQA的问题是：你确实失去了相当大的表达能力。

---

And that's where **GQA**, or **Grouped Query Attention（分组查询注意力）**, comes in. In multi-head, we have queries and keys for each head. In multi-query, we have one key and value for all heads. In grouped query, we reduce the amount of keys and values but keep the number of queries the same. So we now have a ratio we can play with—the number of key/value heads versus the total number of query heads. This allows us to very simply control the trade-offs between expressiveness and inference efficiency. The nice thing about GQA is that in practice the trade-off is quite favorable: GQA really does get the best of both worlds—very low inference cost, nearly the same performance as full multi-head. A small reduction in the number of heads gives you most of the gains in performance, allowing you to keep most of the expressive power while getting significant inference improvements. Almost all models today adopt this GQA structure.

这就引出了**GQA，即分组查询注意力（Grouped Query Attention）**。多头注意力中每个头有自己的查询和键。多查询注意力中所有头共享一个键和一个值。在分组查询注意力中，我们减少键和值的数量，但保持查询数量不变。这样我们有了一个可以调节的比例——键/值头的数量与总查询头数的比值。这让我们可以非常简单地控制表达能力和推理效率之间的权衡。GQA的好处是，实践中的权衡非常有利：GQA真的两者兼得——推理成本很低，性能几乎和全多头注意力一样。小幅减少注意力头数就能获得大部分性能增益，让你保留大部分表达能力的同时获得显著的推理改进。今天几乎所有模型都采用这种GQA结构。

---

### 6.2 Sliding Window Attention / 滑动窗口注意力

The last thing is **sliding window attention（滑动窗口注意力）**, which is a really old idea. GPT-3 actually used this—they alternated between full attention (every position can attend to everyone in the past) and a banded matrix style attention (you can attend to everyone within a fixed window). But this has become really, really popular over the past year. The idea of alternating between full attention and local attention hits a sweet spot for managing long context performance while not paying too much for inference. Cohere Command A had this structure where every four layers, they would have a full attention that attended to everything, and the three layers in between would use sliding window attention looking only at local structure. As you go up the blocks, local information aggregates into global ones. This allows you to manage the cost of really long context without having to go for something like a state space model or more exotic intervention.

最后是**滑动窗口注意力（sliding window attention）**，这是一个非常古老的想法。GPT-3实际上用了它——交替使用全注意力（每个位置可以关注过去所有位置）和带状矩阵式注意力（只能关注固定窗口内的位置）。但它在过去一年变得非常非常流行。全注意力和局部注意力交替的设想，在管理长上下文性能的同时不过多增加推理成本方面找到了一个甜点。Cohere Command A的结构是每四层有一个关注一切的全注意力，中间三层使用只看局部结构的滑动窗口注意力。随着你沿着各层往上走，局部信息汇聚成全局信息。这让你能够管理真正长上下文的成本，而不需要使用状态空间模型等更奇特的方法。

---

This has worked quite well. There's also innovation where people change the embedding format for long-range information, getting rid of things like RoPE—so you have no position embeddings at all for global attention (NoPE). Others alternate local and global structure. Llama 4, Gemma 4, and OLMo 3 all do this combination of sliding window attention and full attention. Qwen3.5 is a little different—they alternate a state space model (gated delta net) and one full attention for every four layers. It's the same alternating structure but using a different cheap layer. This is a new theme over the past year: open models are grappling with long context performance by having hybrid models that aren't just global attention and aren't just cheap attention, but some mix in between. And that seems to have worked very well so far.

这个效果相当好。还有创新是改变长程信息的嵌入格式，去掉RoPE之类的东西——全局注意力完全没有位置嵌入（NoPE）。Llama 4、Gemma 4和OLMo 3都采用了滑动窗口注意力和全注意力相结合的方式。Qwen3.5略有不同——它们交替使用一个状态空间模型（gated delta net）和每四层一个全注意力。同样的交替结构，但用了不同的廉价层。这是过去一年的一个新主题：开源模型通过混合模型来处理长上下文性能问题，既不是纯粹的全局注意力，也不是纯粹的廉价注意力，而是某种混合。到目前为止这似乎运行得很好。

---

## 7. Conclusion / 结论

So as I was trying to emphasize, when you look across all of these models, you start to see a lot of patterns, and hopefully, a sense of general understanding about what things you can do and what things are good defaults. We also see a lot of differences in how we handle context and how we handle position embeddings. Even tokenization has differences. So there are differences across these models, but there are also commonalities that hopefully now give you some intuition as you go out, do your assignments, and mess with the leaderboard and so on.

正如我一直强调的，当你纵观所有这些模型时，你会开始看到很多模式，希望也获得了一个大致的理解：哪些事情你可以做，哪些是好的默认选择。我们也在如何处理上下文和位置嵌入方面看到了很多差异，甚至在分词方面也有差异。所以这些模型之间有差异，但也有共性。希望这些能在你去做作业、折腾排行榜时给你一些直觉。

---

To put everything together: for a lot of the maybe more hairy looking hyperparameters, there are actually just fairly standard choices that have worked well for everybody. Factor of 4 rule of thumb, keep your head dim and your number of heads equal to the model dimension, pick an aspect ratio roughly around 100. If you ask about regularization, you want to maybe try a couple of things because regularization actually does interact with optimizers in ways that are quite counterintuitive.

总结一下：对于很多看似棘手的超参数，实际上都有相当标准的选择，在所有人那里都运行良好。4倍经验法则，保持头维度与头数乘积等于模型维度，选择大约100左右的宽深比。关于正则化，你可能需要尝试一些方案，因为正则化确实会以非常反直觉的方式与优化器交互。

---

Architectures are actually a very complex set of trade-offs. What does the architecture have to do? It has to learn from data—generalize. It has to train efficiently on GPUs. And it has to not blow up. Halfway through training, if your training loss suddenly blows up, that's no good at all. So all these different requirements end up getting baked straight into the architecture. And that's why these things are a little bit messy and a little bit complex. But you should keep that in mind—that's why things are, in many ways, not so elegant.

架构实际上是一个非常复杂的权衡集合。架构需要做什么？它需要从数据中学习——泛化。它需要在GPU上高效训练。它不能爆炸。如果训练中途损失突然爆炸，那就彻底不行了。所有这些不同的需求最终都被直接融入架构设计中。这就是为什么这些东西有点混乱、有点复杂。但你应该记住这一点——这也是为什么这些东西在很多方面并不那么优雅。
