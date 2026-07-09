---
title: "Lecture 8: Parallelism"
---


# Lecture 8: Parallelism / 第八讲：并行

So last lecture, Percy covered some of the underlying mechanics, let's call it, of parallelism. Today, I'm going to do my favorite thing of talk about all sorts of things you can know, like knowledge, details, and trivia about how modern parallelism for language model training works. And what we're going to try to do is really get to grips with the many, many complexities that are involved when you are having to train huge models on huge clusters. It's going to turn out that there are many different parallelization strategies that you can use at once. At the end, we will get to a slide where I say 4D parallelism, because there's four different things that you can do at once. Actually, even more that I'll talk about. And it turns out that to parallelize at the largest scale, you'll need to use all of them or most of them. And we'll discuss why. Part of your assignment will be figuring out, given a particular network topology and a particular model, what is the optimal parallelization strategy for that? And then finally, I'll walk through some examples of recent large scale training runs with details that are published and show you this stuff in action.

上一讲中，Percy 介绍了并行的底层机制——我们姑且称之为"机制"吧。今天，我要做我最喜欢的事情：讲解关于现代语言模型训练并行（parallelism）如何工作的各种知识、细节和轶事。我们想要真正理解在巨型集群上训练巨大模型时所涉及的重重复杂性。事实证明，你可以同时使用多种不同的并行化（parallelization）策略。最后，我们会讲到一张写着"四维并行（4D parallelism）"的幻灯片，因为你可以同时做四件不同的事情——实际上，我还会讲到更多。而且，要在最大规模上实现并行化，你将需要全部或大部分这些策略。我们会讨论为什么。你的作业之一将是在给定特定网络拓扑（network topology）和特定模型的情况下，找出最优的并行化策略。最后，我将通过一些近期已公开细节的大规模训练实例，向你展示这些方法在实际中的运用。

---

OK, so the very first part, I'll go through somewhat quickly. It's partially a review of basic collectives, basic networking primitives, right. But the reason why we need all of this parallelism stuff is because there's going to be two bottlenecks that we'll solve by going to multiple machines and multiple GPUs. So one of it is compute. We need more compute than we can bring to bear on a single chip. And the way we solve that is just to have many, many machines and link them up together. Right, the fastest supercomputers in the world have exaflops of compute, whereas a single GPU is nowhere near that number. The other reason why we need to continue to scale in parallel is because of memory, right. Models are big. We can't fit them all into one GPU, so we need to shard them into smaller pieces somehow. So this is going to lead to complexities of having many GPUs across many different machines. And an important conceptual object that we will deal with throughout our lecture today is the difference between intranode parallelism, where your connections are very fast, and so you can do things that are very communication expensive. And you're going to have slower internode communication. And because these are slow, we will have to use processes that respect the communication constraints of our channel more, right. So we're going to have to do both of those. And remember all of the things that we will do today. We're not actually going to be sending packets or anything like that. We're going to be dealing with this at the level of collective communication primitives. Right, so whenever we do accounting for how much communication is done, I might say, OK, we're going to have to do all-reduce or we're going to have to do allgather to implement some of these operations. So in order to implement some of these efficiently, you're going to have to go all the way to the hardware level.

好的，第一部分我会过得比较快。这在一定程度上是对基础集合通信（collective communication）和基本网络原语（networking primitives）的回顾。但我们需要所有这些并行技术的原因在于，有两个瓶颈需要通过多机多 GPU 来解决。第一个是**计算**（compute）。我们需要比单个芯片能提供的更多的算力，解决办法就是拥有很多很多台机器并将它们连接在一起。世界上最快的超级计算机拥有百亿亿次（exaflops）的算力，而单个 GPU 远远达不到这个数字。我们需要继续大规模并行化的另一个原因是**内存**（memory）。模型很大，无法全部放入一个 GPU，所以我们需要以某种方式将它们分片（shard）成更小的部分。这将导致跨多台机器的众多 GPU 所带来的复杂性。今天课程中一个重要的概念性对象是**节点内并行**（intranode parallelism）与**节点间并行**（internode parallelism）之间的区别——在节点内，连接速度非常快，因此你可以做通信开销很大的操作；而在节点间，通信则较慢。由于速度慢，我们必须使用更尊重通道通信约束的处理方式。所以这两者我们都需要做。请记住，我们今天所做的所有事情并不是真的在发送数据包之类的——我们将在集合通信原语（collective communication primitives）的层面上处理问题。所以每当我们计算通信量时，我可能会说："好的，我们需要做全归约（all-reduce）"或"我们需要做全收集（all-gather）"来实现某些操作。要想高效地实现其中一些操作，你需要深入到硬件层面去。

---

But our discussion today is going to be algorithmic. And so all of the networking primitives I'll talk about is going to be at this level of a collective. And remember, Percy talked about this, but this is important for-- very important for one part of the talk, which is going to be that the equivalence between all-reduce and reduce-scatter plus all-gather. Right, so there's going to be one algorithm where on one hand, you do an all-reduce, and on the other hand, you do two of these different steps. And the fact that these two have the same cost in some sense means that we can do the algorithm on the right for free. We'll see that again later. This is just a quick refresher just to make sure you remember what Percy said.

但今天的讨论将是算法层面的。所以我将提到的所有网络原语都处于集合通信这一层级。请记住，Percy 讲过这一点，但这对于今天的某一部分内容非常重要——那就是全归约（all-reduce）与归约-散射（reduce-scatter）加全收集（all-gather）之间的等价性。有一种算法，一方面你可以做全归约，另一方面你可以做两个不同的步骤。而这两者在某种意义上具有相同的代价，这意味着我们可以"免费"实现右边的算法。我们稍后会再次看到这一点。这只是个快速回顾，确保你们还记得 Percy 讲的内容。

---

OK, so that's it for the really basic review. The other thing I want to touch on briefly before we get into the algorithms, which are going to be hardware and substrate agnostic, is the difference-- oh, sorry, yes?

好，基本回顾就到这里。在进入与硬件和底层平台无关的算法之前，我还想简要提一下另一个区别——哦，抱歉，请讲？

---

Is there any particular reason why you are saying that old [INAUDIBLE] reduce scatter and-- OK, the question was, is there any reason why I'm talking about this specifically? We will-- [INAUDIBLE] Yes, yes, there are other decompositions. This one in particular will be useful for a algorithm, which is why I'm emphasizing this particular decomposition. That's right. There's others that you could do, of course. Yes.

"你特别提到归约-散射有什么特殊原因吗？"——好的，问题是：我为什么特别强调这个？是的，还有其他分解方式，但这一种特别适用于某个算法，这就是我强调它的原因。当然，还有其他分解方式。

---

OK. So the other thing I will talk about before I start-- most of our discussion today will be hardware agnostic. For the most part, once you understand the basic concepts, you'll be able to apply it to any hardware substrate. But I do want to briefly before we start, just talk about the low level hardware stack. Both because it's interesting. But also because I think it leads to different parallelization strategies across different model training companies.

好的。在开始之前我还想讲一件事——我们今天的大部分讨论将是与硬件无关的。在很大程度上，一旦你理解了基本概念，就能将其应用于任何硬件平台。但在开始之前，我确实想简要谈谈底层硬件栈。这既因为它很有趣，也因为它导致了不同模型训练公司之间不同的并行化策略。

---

So remember the TPU. Right, TPU is Google's accelerator. And I mentioned during the GPU lecture, a TPU is like a lightweight GPU. But what's different is the networking. So how is the networking different? Well, in one slide, the TPU network is what's called a toroidal mesh. Right, so you can think about a grid and then allowing the ends of the grid to communicate with each other. It's a little bit more complicated. It's a 3D picture. Which, Marcel, you have the visualization, right? Can you post that in the lecture channel? Yeah. So there's a fun web visualization that you can look at that visualizes the toroidal mesh in 3D, which is very cool. But your mental model, I think, can roughly be this picture. You can forget the more complex one. All the chips are networked to neighbors and the neighbors wrap around, right. So what does this let you do? This lets you have a very simple networking topology that can be indefinitely scaled up very simply, right. The number of neighbors you have is the same, no matter how large your network gets. In contrast, the GPU networking philosophy is very different. It's really much more of an all to all philosophy. And the way that it's networked is it's like a tree. It's often called a fat tree. You have your GPUs connected very, very quickly at the lowest layers. And then you have groups of GPUs that are connected in a pod. And then the pods might have spine switches that allow them to communicate to each other. And this means that as the number of nodes grows, the tree gets bigger and bigger. Your communication costs is going to get higher, or your communication topology will get more complicated, because you're connecting all these all to all as you go. Now, this difference in philosophy means that if you're communicating only to neighbors, TPUs are great. They're cost effective. And you can make each connection more beefy, right, with the same power consumption. But if you're connecting in very random ways, very stochastic, unpredictable ways, then this GPU networking will be more flexible, right. So there's this very different design philosophy that you see between TPUs and GPUs. And I'll try to mention where this shows up as we go through the parallelism lecture.

还记得 TPU 吧？TPU 是谷歌的加速器。我在 GPU 讲座中提到过，TPU 就像一个轻量级的 GPU。但不同之处在于网络。那么网络有什么不同呢？简单来说，TPU 网络被称为**环形网格**（toroidal mesh）。你可以把它想象成一个网格，网格的两端可以相互通信。实际上它更复杂一些，是一个三维结构。Marcel，你有那个可视化图对吧？能发到课程频道里吗？是的，有一个很有趣的网页可视化工具，可以让你在 3D 中观察环形网格，非常酷。但你的心智模型大致可以理解为这张图，更复杂的那个可以忘掉。所有芯片都与相邻芯片相连，并且首尾相连环绕起来。这能做什么呢？这让你拥有一个非常简单的网络拓扑，可以无限扩展——无论网络变得多大，你的邻居数量都是固定的。相比之下，GPU 的网络哲学完全不同——它更接近全对全（all-to-all）的哲学。它的网络连接方式像一棵树，通常被称为**胖树拓扑**（fat tree）。在最低层，你的 GPU 之间连接非常非常快。然后你有一些 GPU 组连接在一个 pod 中。pod 之间可能有 spine 交换机（spine switches）让它们相互通信。这意味着随着节点数量增加，树会变得越来越大，通信成本会越来越高，通信拓扑也会越来越复杂，因为你需要在向上连接的过程中实现全对全连接。这种哲学差异意味着：如果你只需要与邻居通信，TPU 很棒——它们性价比高，而且可以在相同功耗下让每条连接更强。但如果你需要以非常随机、随机化的方式连接，那么 GPU 网络会更灵活。所以 TPU 和 GPU 之间存在着非常不同的设计哲学。在今天的并行讲座中，我会尽量指出这种差异体现在哪里。

---

And I posted this into the lecture chat last lecture. Because someone asked, what's the difference between these two and so on? Right, but just to back up my point, Bill Daley and Jeff Dean were talking about the different hardware and what are they good for, right. GPUs are good for things like mixture of experts, where the communication is much less clear because tokens route to different experts. TPUs are great if you have this dense model that you're doing very predictable partitions of. I'll talk about that in an idea called tensor parallelism later in this lecture. And so these hardware things are good for different workloads. And this was where I was going to leave it for the lecture until this morning, when Google decided that they were going to announce TPU8i and t this morning. And then I looked at this as I was preparing my lecture, and I said, oh my god, TPu8i? That's a tree topology. They've switched to a much more all to all connection. And if you think about it, it makes sense. Modern day language models are MoEs. And if you're going to serve a MoE, you're going to have all sorts of bandwidth just flying around as you route tokens to different experts. You probably do want much more of an all to all connectivity where, at inference time, these communications are real bottlenecks. You want to deal with them. And even at training time, the TPU8t, which is a training chip, the cross rack connectivity looks a lot more like a GPU. There's much more like an all to all style switch that's being built out called the Virgo network. That's a higher level networking stack. So I think there's really interesting things happening. It's a little bit of a convergent evolution across both TPUs and GPUs, where really the workloads are defining the network that we need to have.

我在上一讲中把这个链接发到了课程聊天频道，因为有人问过这两者之间的区别等等。为了支持我的观点，Bill Dally 和 Jeff Dean 曾讨论过不同硬件的优势所在。GPU 适合混合专家（MoE）这类场景，其中的通信模式不太确定，因为 token 会被路由到不同的专家。而如果你有密集模型（dense model），做的分割非常可预测，那么 TPU 很棒——我稍后会讲到一种叫做**张量并行**（tensor parallelism）的概念。所以这些硬件适用于不同的工作负载。本来讲座我就准备讲到这里为止的，直到今天早上，谷歌决定发布 TPU 8i 和 TPU 8t。我准备讲座时看到了这个，心想："天哪，TPU 8i？那是树形拓扑。他们改成了更接近全对全的连接。"仔细想想，这很合理。现代语言模型都是 MoE。如果你要部署 MoE，在将 token 路由到不同专家时，会有各种各样的带宽需求在系统中流动。你确实需要更多的全对全连接能力，因为在推理时，这些通信是真正的瓶颈，你需要处理它们。即使在训练时，TPU 8t（一款训练芯片）的跨机架连接也看起来更像 GPU 的架构，他们正在构建一个更像全对全风格的交换机，称为 Virgo 网络——那是一个更高层次的网络栈。所以我认为正在发生非常有趣的事情。TPU 和 GPU 之间有点趋同进化（convergent evolution）的味道，实际上是工作负载在定义我们所需的网络。

---

OK. And then the final thing about hardware-- I just love talking about what's happening in the Chinese AI scene-- is this idea of-- I think in the GPU lecture, someone asked, if SRAM is so good, why don't you just all use SRAM? Only SRAM chip. And that's Grok, right? It works really well. Now, some of you might be thinking, if all to all connectivity is good, why don't you just connect everything and connect them with really fast fiber optic chips, right? And then you would get the Huawei Ascend 910, right? So if you look at the specs of the Huawei Ascend, it's actually really interesting, because each chip is a lot worse than a H200. It's a lot slower at matmuls. It's slower in many ways. But then, if you're willing to dedicate a giant rack of fiber optic switches to connect a much larger number of chips, like in their case, 384 in a big rack, then maybe you can deal with the fact that each chip is slower by just connecting a much, much larger number of these guys, right. And then so I think what this shows us is a really interesting tradeoff. Because once you look at this architecture, you realize the power consumption of this thing is insanely high. It's four times that of the equivalent NVIDIA system. And so it's something like, well, if you're willing to pay the power cost, you can solve a lot of communication problems brute force, and you can scale out much more aggressively to 300 chips. But you're paying a power cost, right. It's similar to that SRAM story of, if you want to design a hardware that is efficient to use both power and manufacturing wise, you end up in a certain place. If you want to brute force things, you end up in a very different place. Right, so this is, I think, just a very interesting place to learn from about these hardware design tradeoffs.

好的，关于硬件的最后一点——我就是喜欢聊中国 AI 场景中发生的事情——这个想法是……我记得在 GPU 讲座中，有人问：如果 SRAM 这么好，为什么不全部用 SRAM？只用 SRAM 的芯片。那就是 Grok，对吧？它效果确实很好。现在，你们有些人可能会想：如果全对全连接这么好，为什么不把一切都连接起来，用非常快的光纤芯片来连接呢？那样你就会得到华为 Ascend 910。如果你看华为 Ascend 的规格，其实非常有趣——每个芯片比 H200 差很多，矩阵乘法（matmul）慢得多，在很多方面都更慢。但如果你愿意用一个巨大的光纤交换机机架来连接更多的芯片——比如他们将 384 个芯片放在一个大机架中——那么你可能就可以通过连接更多的芯片来弥补单个芯片较慢的短板。所以我认为这向我们展示了一个非常有趣的权衡。因为一旦你审视这个架构，你会发现它的功耗高得离谱——是同等 NVIDIA 系统的四倍。所以情况就是：如果你愿意支付功耗成本，你可以暴力解决很多通信问题，更大规模地扩展到 300 块芯片。但代价是功耗。这和 SRAM 的故事类似：如果你想设计一个在功耗和制造成本上都高效的硬件，你会得到一个结果；如果你想暴力解决问题，你会得到一个非常不同的结果。所以我认为这是一个学习硬件设计权衡的非常有意义的案例。

---

OK, good. So now, just to put this all together, the first thing you should think about is the new unit of compute is not the GPU. It's the entire data center. And we want to have several things. We want to be able to control the amount of memory we use. We want to be able to control the amount of compute that we can bring to bear. And we want all of these to be lossless. Right, we want to use all of the resources that we have. And then we're going to talk about the algorithms that will enable this through all these communication primitives components.

好了，现在总结一下：首先你要明白，新的计算单元不再是单个 GPU，而是整个数据中心。我们需要实现几件事：能够控制所用的内存量，能够控制所能调用的计算量，并且所有这些都应该是无损耗的——我们要用上所有资源。接下来我们将讨论通过所有这些通信原语组件来实现这一目标的算法。

---

OK, good. So now the second part of this lecture is going to be the bulk of the content. And these are the algorithms that we will use to paralyze language models. And there's going to be a couple of different important ideas. Actually, we should probably maybe even be grouped. Data parallel is one set of ideas for essentially taking your data that you're going to train on and distributing them across GPUs. So the data is the ones that move around. And then model parallelism, you're going to chop up different parts of the model and split them around. Turns out that the boundary between these two is a little leaky, because one of the algorithms here will actually cut parameters up, too. But we will see why I've put all of these algorithms into these different bins, right. And conceptually, we're trying to both scale out compute and memory, and that's why we will need a whole bunch of these different tricks.

好的，第二部分将是本讲的主体内容。这些是我们用于并行化语言模型的算法。有几个不同的重要思想。实际上，我们也许应该将它们分组。**数据并行**（data parallelism）是一组思路，核心是将训练数据分发到不同 GPU 上——也就是数据在移动。而**模型并行**（model parallelism）则是将模型的不同部分切分并分布到各处。事实证明，这两者之间的界限有些模糊，因为其中一种算法实际上也会切分参数。但我们会看到为什么我把所有这些算法分到了不同的类别中。概念上，我们既要扩展计算也要扩展内存，这就是为什么我们需要一大套不同的技巧。

---

So data parallelism, I think, is the easiest to understand. It is conceptually very simple, and I think it's the standard way that you would try to parallelize an algorithm like LLM training. So forget that we're doing Adam. We're going to do just naive SGD for the moment. Then we have a capital B sized batch, right. So each update step, I'm going to take capital B elements, and I'm going to sum up the gradients. And I'll take my update, right. So the most naive form of parallelism that one can do for this is to take my batch, B. I can cut it up across M machines. If they're divisible, each machine will get a smaller B over M sized batch. And then what I'm going to do is each machine computes gradients, and then I will synchronize all the gradients to get my sum. OK, great. So compute scaling wise, this is perfect. As long as there's enough examples per GPU, we're good. Communications overhead. How much do we have to talk to each other? Well, every batch, we have to basically communicate two times the number of parameters, right. Because what I have to do is I have to basically communicate my gradients back and forth. OK, and then for memory scaling, there's absolutely none. Every GPU has the same copies of the models. You need to have the same sized activations so you don't save any memory at all in this scheme.

数据并行，我认为是最容易理解的。它在概念上非常简单，也是并行化 LLM 训练这类算法的标准方式。我们先忘了 Adam，暂时只考虑朴素的 SGD。我们有一个大小为 B 的批次。每次更新步骤，我取 B 个样本，求和梯度，然后更新。对此能做的最朴素的并行形式就是：取我的批次 B，将其切分到 M 台机器上。如果可整除，每台机器得到一个大小为 B/M 的批次。然后每台机器计算梯度，我再同步所有梯度得到总和。好的。从计算扩展的角度看，这很完美——只要每个 GPU 有足够的样本就没问题。通信开销呢？我们需要互相通信多少？每一批次，基本上需要通信两倍的参数量。因为我需要来回通信我的梯度。至于内存扩展，完全没有——每个 GPU 都有相同副本的模型和相同大小的激活值，你在这种方案中根本节省不了任何内存。

---

So now what is the problem? Clearly we've addressed compute to some extent. But we have not addressed memory at all. So let's take a look at this memory problem and just do a little bit of accounting. Initially, it might seem that the memory situation is bad. But it turns out our memory situation is actually just terrible. And the reason why the memory situation is terrible is if you just do some parameter accounting, right, it just turns out you need to store a lot of stuff. Right, and not only do we need to store a lot of stuff, it's actually more than the parameters that we need to store. So roughly the rule of thumb-- it depends on your precision. But the rule of thumb, you might say, is that we need something like five copies of weights and 16 bytes per parameter to store our model. So we will need to, of course, store our model parameters. We need a place to put our gradients, right. The accumulator before we put them into the model parameters. So we need to store those guys. But actually, you need to maybe store more stuff. You might need to have a higher precision accumulator that you accumulate into in SGD. This might be temporary, but you might need this. And if you're doing Adam, and this is really where the bad stuff comes in, you're going to need to track both the first and second moments of your gradients. And you need to track them over time, right. So you need two of these. And unfortunately, you might need to store them in high precision depending on your stability characteristics. And these might be quite expensive, right. And we generally call these things optimizer state. Right, the thing that you're accumulating into. The first moment, the second moment. Right, and these are actually quite expensive. If you look at the accounting, this is most of the cost memory wise of doing an SGD update.

那么现在问题是什么？很明显我们在一定程度上解决了计算问题，但根本没有解决内存问题。让我们来看看这个内存问题，做一点核算。起初你可能会觉得内存情况很糟糕，但实际上我们的内存情况简直是糟糕透顶。为什么内存情况如此糟糕？如果你做一些参数核算，就会发现你需要存储很多东西。而且不仅需要存储很多东西，实际需要存储的甚至比参数量还多。粗略的经验法则是——取决于你的精度——但我们可能需要大约五份权重副本，每参数 16 字节来存储模型。当然我们需要存储模型参数。我们需要一个地方放梯度——在更新到模型参数之前的累加器。所以我们需要存这些。但实际上你可能需要存更多东西——你可能需要一个更高精度的累加器在 SGD 中累加。这可能是临时的，但你可能会需要。而如果你在做 Adam——这才是糟糕的地方——你需要跟踪梯度的**一阶矩**（first moment）和**二阶矩**（second moment），并且需要随时间跟踪它们，所以你需要两个。不幸的是，根据你的稳定性特性，你可能需要以高精度存储它们。这些可能相当昂贵。我们通常把这些称为**优化器状态**（optimizer state）——你累加进去的东西：一阶矩、二阶矩。它们实际上相当昂贵。如果你做一下核算，这是做一次 SGD 更新时内存方面的大部分成本。

---

And so I think one of the really elegant and nice things that you can do in this space is to start cutting up the amount of memory you need and distributing them across the accelerators, but doing so in this structured way that gets you these gains for basically free.

所以我认为在这方面可以做的非常优雅且漂亮的事情就是开始削减所需的内存量，并将其分布到各加速器上——而且是以这种结构化的方式，基本上免费获得这些收益。

---

As I said in the last slide, the optimizer state is most of your memory. So here, the optimizer state is green. That's most of your memory. Orange is your gradients, and blue is your parameters. And notice how parameters and gradients are the same size, and your state is bigger, right. If you do naive data parallel, you're just going to replicate all of this state across the GPUs. And this is not so good, right. Because you've, in some sense, consumed way more memory than you need and your memory consumption is linear with your number of accelerators. Not so good, right. What we can do instead is perhaps we can shard the optimizer state onto different GPUs. And this would be a big savings. If we shard different other parts of what we need to track, that would be also big savings. Maybe we can also shard the gradients into different GPUs. Or in the extreme, maybe we can shard everything into different accelerators. And then you can see that the implied memory gains on the very right would be quite dramatic as we go all the way down from 120 to 1.9.

正如我在上一张幻灯片中说的，优化器状态占用了大部分内存。在这里，优化器状态是绿色的——那是大部分内存。橙色是梯度，蓝色是参数。注意参数和梯度大小相同，而状态比它们都大。如果做朴素的数据并行，你将在所有 GPU 上复制所有这些状态。这并不好——因为你在某种意义上消耗了远超需要的内存，而且内存消耗与加速器数量呈线性关系。不太好。我们可以做的改进是：也许我们可以将优化器状态分片（shard）到不同的 GPU 上——这将是一个很大的节省。如果我们分片需要跟踪的其他部分，也会是很大的节省。也许我们还可以将梯度分片到不同的 GPU 上。或者极端情况下，我们可以把所有东西都分片到不同的加速器上。然后你可以看到，最右边的隐含内存收益将非常显著——从 120 一直降到了 1.9。

---

Now, the main thing that we will study now is, what is the cost of doing this? Right, you might imagine, there's no free lunch. Baseline is going to be the fastest. And as we go downwards to here, we're going to have to pay a big communication cost in order to achieve these memory savings. I think the remarkable thing is going to be that a lot of this will be free. But I'm going to walk through this step by step.

现在我们要研究的主要问题是：这样做的成本是什么？你可能想，天下没有免费的午餐。基线方案将是最快的，而当我们往下走到这一步时，我们需要支付巨大的通信成本才能实现这些内存节省。我认为值得注意的一点是，其中很多将是免费的。但我会一步步地讲解。

---

So let's start with what people call ZeRO stage 1. So there's going to be three stages corresponding to each of these steps. And so stage 1 is going to be the simplest. The only thing I will shard is my optimizer state. And I will shard it across the GPUs, OK. Everyone is going to have both the parameters and the gradients. And so what you can think of is each worker is going to be responsible for updating one slice of the parameter. So if I'm GPU number 0, my responsibility is updating this very first slice over here. And I'm not responsible for any of the other updates. So how would it work? Right, so what we're going to do is everyone computes. Everyone has a different data item, right. So they're going to compute a full gradient on their data item. That's the first step. Now I'm going to take the gradient I computed and I'm going to reduce scatter the gradients onto all the other machines. Because everyone else needs my gradients, right? But they don't need all the gradients. They only need the gradients associated with their update. Right, so every worker is going to get from me, my gradient, but they're part of the parameter space, right. So this is going to be equivalent to a number of parameters communication costs. Because I'm sending my gradient, but I'm cutting it up and sending it into each GPU.

让我们从人们所说的 ZeRO 阶段 1（ZeRO stage 1）开始。总共有三个阶段，对应上述每一步。阶段 1 是最简单的——我只分片优化器状态，将其分片到各 GPU 上。每个 GPU 都拥有完整的参数和梯度。你可以这样理解：每个工作节点（worker）负责更新参数的一个切片。如果我是 GPU 0，我负责更新最前面的那一片，而不负责其他任何更新。那么它是如何工作的？每个人都要计算——每个节点有不同的数据项，所以它们在自己的数据项上计算完整梯度，这是第一步。然后我把我计算出的梯度做**归约-散射**（reduce-scatter）到所有其他机器上。因为其他人都需要我的梯度——但它们不需要全部梯度，只需要与他们更新相关的梯度。每个工作节点从我这里得到我的梯度，但只是参数空间的一部分。所以这相当于一定数量的参数通信成本——我发送梯度，但将其切分并发送到每个 GPU。

---

Now each machine is going to be able to now do their update. They have their parameters, they have their gradients that they got from everybody else, and they have their own state that they've tracked, right. And now, the parameters have been updated. And now I'm going to all gather them back. Right, I was responsible for, let's say, one fourth of the parameters. So those updated parameters, I'm going to send back to everybody else, right. So this is a all-gather, right. So this is where the equivalence is useful. How many operations did I do? Well, in the naive data parallel case, what I had to do was I had to do one all-reduce. Right, I had to exchange all the gradients with everybody and then do the updates, right. So the communication cost is 2 times the parameters. Now in ZeRO stage 1, I did two operations. One was a reduce-scatter to send the gradients out and then an all-gather to collect the updated parameters. But we already said a reduce-scatter and an all-gather is equivalent to an all-reduce. So ZeRO stage 1 is going to have the exact same communication characteristics as naive DDP. Right, so this was free. Free memory savings. Wonderful, right? And we look at the memory. We've basically taken the parameters. And anything that's an optimizer state, I've divided by n GPUs, right. Wonderful, wonderful, wonderful.

现在每台机器就可以做自己的更新了——它们有参数、从其他人那里得到的梯度以及自己跟踪的状态。现在参数被更新了。然后我通过**全收集**（all-gather）把它们收回来——比如说我负责四分之一的参数，我就把这些更新后的参数发回给所有人。这就是全收集。这就是等价关系有用的地方。我做了多少操作？在朴素数据并行下，我需要做一次**全归约**（all-reduce）——与所有人交换梯度然后做更新——通信成本是 2 倍的参数量。在 ZeRO 阶段 1，我做了两个操作：一次归约-散射（发送梯度），然后一次全收集（收集更新后的参数）。但我们说过归约-散射加全收集等价于全归约。所以 ZeRO 阶段 1 具有与朴素 DDP 完全相同的通信特性。所以这是免费的——免费的内存节省。太棒了，对吧？看看内存：我们基本上把优化器状态按 n 个 GPU 进行了均分。太棒了。

---

Now, can we do more? Well ZeRO stage 2 is now going to say, I'm going to split the gradients up. And then I'm going to shard that as well. Now, this is going to be trickier because before I was relying on the fact that I can compute the entire gradient, now I can't even materialize the whole gradient. So what do I do. Well, this turns out to just be a systems trick. As I sweep backwards through my network, I don't need to compute the full gradient. I can send out the gradients to the associated workers as I go. So the key step here is now, instead of materializing the gradient vector all at once, I'm going to walk backwards through the compute graph. And after computing a layer's gradients, I'm going to immediately just reduce that to send that to the right worker, right. And once gradients aren't needed in the backwards graph, just immediately free it. Right, so you're now incrementally computing and sending gradients as you go. And as you can see, doing it incrementally or doing it all at once, same thing, right? So it doesn't really make a difference. So now you can, at the end, once again all gather the parameters. I've started the gradients in some sense without incurring any additional costs, right.

现在，我们能做得更多吗？ZeRO 阶段 2（ZeRO stage 2）说：我要拆分梯度，也把它分片。这会更棘手，因为之前我依赖的是可以计算完整梯度，而现在我甚至无法实例化完整的梯度。那我该怎么办？这实际上只是一个系统技巧。当我在网络中反向传播时，我不需要计算完整梯度——我可以在过程中将梯度发送给对应的工作节点。所以关键步骤是：我不再一次性实例化整个梯度向量，而是逐步向后遍历计算图。在计算完一层的梯度后，我立即进行归约，将其发送给正确的工作节点。一旦反向图中不再需要梯度，就立即释放。所以你现在是增量式地计算和发送梯度。如你所见，增量式和一次性完成是一样的，对吧？所以实际上没有区别。最后你可以再次全收集参数。在某种意义上，我分片了梯度而没有产生任何额外成本。

---

OK, so the last and the most hairy thing-- and this always, when I first learned about this, seemed like total magic-- is we've gotten something for free so far, so let's keep pushing it. I'm going to shard the parameters as well all the way across all the states. And so we're going to use the same kind of idea that we used in ZeRO stage 2. And the idea, remember, was I'm going to do things incrementally, right. And so what I'm going to do is I'm going to send and receive parameters on demand while stepping through the compute graph. And this is really tricky, because each GPU only sees a slice of both the parameters, gradients, and optimizer states at any one time, right. And this is ZeRO stage 3, also known as FSDP. If you've ever parallelized anything in a Torch library, you've probably dealt with this before.

好的，最后也是最棘手的东西——我第一次学到这个时，总觉得完全像魔法——到目前为止我们已经免费得到了某些东西，那就继续推进。我要把参数也分片到所有状态中。我们将使用与 ZeRO 阶段 2 相同的思路——增量式地做事。我要在遍历计算图时按需发送和接收参数。这真的很棘手，因为每个 GPU 在任何时刻只能看到参数、梯度和优化器状态的一个切片。这就是 **ZeRO 阶段 3**（ZeRO stage 3），也称为**全分片数据并行（FSDP）**。如果你曾经用 Torch 库做过任何并行化工作，你可能以前就处理过这个。

---

So the way that it works under the hood is what you're going to do is you're going to do two all-gathers and one reduce-scatter as you go. So we're going to step from left to right here. And this is going to be the entire update process. So what you do is you're going to load your model. You have your two GPUs at the top and the bottom. You're first going to gather your weights for this one layer. I'm going to forward this one layer. And then I can free my weights, because I've already done the forward, right. I don't need these parameters anymore. Now, let's say I only have one layer. Now I can move to the backwards process. Now to do the backwards step, I need the activations, which I've kept. And I need the parameters for this layer, which I can all-gather on demand. I all-gather it, I do the backwards. And then I scatter the gradients back right when I get them. Right, so I got the gradients. I reduce-scatter the gradients out. And then I free the weights. I don't need them anymore, and I repeat this process, right. So I grab the parameters as I need them. I compute my backwards. I send the gradients out, and I repeat this process. And then I update my weights. All done, right.

它在底层的工作方式是：你在这个过程中做两次全收集和一次归约-散射。我们从左到右逐步进行，这就是整个更新过程。你加载模型，上方和下方各有一个 GPU。你首先为一层收集权重，对这一层做前向传播，然后释放权重——因为已经完成了前向，不再需要这些参数。假设只有一层，然后进入反向过程。为了做反向步骤，我需要保留的激活值，以及这一层的参数——我按需全收集。全收集后做反向，然后一得到梯度就散射回去。我做归约-散射把梯度发送出去，然后释放权重，不再需要它们了。重复这个过程——按需获取参数，反向计算，发送梯度，重复。然后更新权重。全做完了。

---

So what's the communication cost? Right, how many all-gathers did we do? We did two all-gathers, one reduce-scatter. Also, so we have one extra all-gather, which seems bad. That's one thing. The second thing is this seems a little crazy in terms of the overhead, because we're doing communication all the time. Every layer, we're doing this communication. You might think that this is extremely expensive and bad. But I think one of the things that's counterintuitive and important is ZeRO stage 3 uses two really important ideas to make this essentially overhead free. So the first one, which we've already seen, is this idea that we're going to sweep through the compute graph, and then we're going to do the necessary communication and then immediately free the memory. Right, that's already an idea we've experienced. The other idea, which I haven't talked about yet, is we're going to overlap the communication and computation cost of this process, right. And this is hard to explain initially.

那么通信成本是多少？我们做了多少次全收集？两次全收集，一次归约-散射。所以我们多了一次全收集，这看起来不太好。这是一件事。第二件事是，从开销的角度看这有点疯狂——我们每时每刻都在做通信。每一层，我们都在做这个通信。你可能会认为这极其昂贵和糟糕。但我觉得违反直觉且重要的一点是：ZeRO 阶段 3 使用了两个非常重要的想法，使其基本上是零开销的。第一个我们已经见过：逐步遍历计算图，做必要的通信，然后立即释放内存。这是我们已经体验过的想法。另一个我还没有讲到的想法是：我们将重叠（overlap）通信和计算的开销。这在一开始很难解释。

---

So I think I've taken this plot from this paper, which I think was explaining the PyTorch FSDP architecture. So the way that this works is in order-- so we have different streams here. This is what's happening in the CPU. This is what's happening in the GPU for computation, and then what's happening in the GPU for communication at the very bottom here. Now, the way FSDP works is I have to first get my parameters before I can do my computation. So I'm going to all-gather 0, layer 0, right. And once I've all-gathered, I can now do my forward. But as I'm doing my forward, notice that I'm requesting the next layer's parameters. I'm all gathering 1 while I'm doing this computation. And now I all-gathered 1, I can now do forward 1, right. And I can start all-gathering 2 while I'm starting this process. And so I'm overlapping computation and communication as I'm doing this. And I might spend some time freeing my parameters. I might also spend some time computing another forward. For example, if you reuse that W nought, I'm reusing this forward 0 twice. And so what this allows you to do is if you have enough computation and your network's fast enough, by overlapping communication and computation, right. FSDP can basically be free. Right, you do see some bubbles. These are overheads. But if your comms is very fast and your computation is very big, right, you can easily see how the computation can run faster than the communication-- I'm sorry, the computation can take longer than the communication, and you end up having this really great improvement in memory usage without paying for almost any amount of memory use.

我想我是从这篇解释 PyTorch FSDP 架构的论文中借用了这张图。它的工作方式是这样的——我们有不同的流（streams）。这里是在 CPU 上发生的事情，这里是在 GPU 上做计算，底部是在 GPU 上做通信。FSDP 的工作方式是我必须先获得参数才能做计算。所以我先全收集 0——层 0。一旦完成全收集，我就可以做前向。但注意，在我做前向的同时，我请求了下一层的参数——我在这段计算期间全收集 1。现在全收集 1 完成，我可以做前向 1。我可以在这个过程开始时开始全收集 2。所以我在重叠计算和通信。我可能花一些时间释放参数，也可能花一些时间计算另一个前向，比如如果你复用 W0，我就把前向 0 用了两次。所以这允许你做的是：如果你有足够的计算且网络足够快，通过重叠通信和计算，FSDP 基本上可以是免费的。你确实会看到一些气泡（bubbles）——这些是开销。但如果你的通信非常快而计算量很大，你很容易就能看出计算时间可以比通信时间长，最终你在内存使用上获得巨大改进，而几乎不需要付出任何额外的代价。

---

OK, so when we look at the different ZeRO stages, right, DDP, the naive data parallel, costs 2 times parameters. Right, it was a single all-reduce. The two ZeRO stages, 1 and 2, right, the ones that shard gradient and optimizer state, this is free in the literal sense, because it has the same amount of communication cost, right. It's just the identity of all-reduce being equivalent to two operations, right. Now, ZeRO stage 3 is technically a little bit more communications. You need an extra all-gather, right. But it's not so bad because of the really clever ways in which all these libraries can hide the communication cost underneath the computation. So in practice, FSDP, if you run it, you're going to see GPU utilization that's very close to just the single GPU performance. It is actually quite remarkable how good FSDP is. And it's also very conceptually simple. You will actually have to write an FSDP implementation as part of your assignment. And you can just write a wrapper that will wrap any module and turn it into its FSDP version. Right, conceptually, all you're going to do is do a bunch of all-gathers, compute, free, and then repeat on the backwards pass.

现在来看不同的 ZeRO 阶段。DDP（朴素数据并行）的成本是 2 倍参数量——一次全归约。ZeRO 阶段 1 和 2（分片梯度和优化器状态的那些）在字面意义上是免费的，因为它们具有相同的通信成本——只是利用了全归约等价于两个操作这一恒等式。ZeRO 阶段 3 技术上通信稍多一些——你多需要一次全收集。但它并没有那么糟糕，因为所有这些库可以通过非常巧妙的方式将通信成本隐藏在计算之下。所以在实际中，如果你运行 FSDP，你会看到 GPU 利用率非常接近单 GPU 性能。FSDP 的好用程度真的非常惊人。而且它在概念上也很简单。作为作业的一部分，你实际上需要自己实现一个 FSDP。你只需要写一个包装器（wrapper），它包装任意模块并将其转换为 FSDP 版本。概念上，你要做的就是一系列全收集、计算、释放，然后在反向传播时重复。

---

OK, good. Yes? [INAUDIBLE] --gradients from the next GPU to calculate the gradients for the previous GPU, right? When you say-- so we're not-- I think what you just described, which is taking gradients from one GPU to the next, that's closer to pipelining. Pipelining would be if one layer was on one GPU and another layer was on another GPU. That's not the case. So in all these cases, every GPU goes through the entire model, right, from the start to finish. But the difference is, no GPU is going to hold the entire parameters at the same time. And so what we're going to do is if I only have part of the network that doesn't have layer 0, I'm going to demand the layer 0 parameters first and then do the full computation. And then I'll move on to the next layer, right. So it's the same computation. It's the same single GPU computation as naive data parallel. But you can just think of it as request parameters, free parameters in between every computational operation.

好的。请讲？[听不清]——"来自下一个 GPU 的梯度用来计算前一个 GPU 的梯度？"我认为你刚才描述的是从一个 GPU 拿梯度到另一个 GPU，这更像是流水线（pipelining）。流水线是一层在一个 GPU 上，另一层在另一个 GPU 上。但这里不是这样。在所有这些情况下，每个 GPU 都会遍历整个模型，从开头到结束。区别在于，没有哪个 GPU 会同时持有全部参数。所以如果我的网络部分没有层 0，我会先请求层 0 的参数，然后做完整计算，再进入下一层。所以这是相同的计算——与朴素数据并行相同的单 GPU 计算。你只需要把它想象成在每次计算操作之间请求参数、释放参数。

---

Yes? So are you saying that every GPU has a part of every layer, and that's what the all-gather's for? Yes, that's right. So the picture is here, right. Parameters, gradients, and optimizer states are all sharded across the different GPUs. That's right. Yeah, good.

请讲？"你是说每个 GPU 拥有每一层的一部分，这就是全收集的作用？"是的，没错。图片就在这里——参数、梯度和优化器状态都在不同 GPU 之间分片。没错。

---

Oh, yes. Why does the communication cost not multiply by the number of layers as well? So the number of operations multiplies by layer. So that's correct. But each of these communication pieces is smaller, right. Because this is just one tiny MLP or something. And I'm comparing that to the cost of all-reducing a whole network. Right, so it all adds up in some sense. Yeah, good.

请讲？"为什么通信成本不乘以层数？"操作的次数确实乘以层数了，这是对的。但每一块通信更小了，因为这只涉及一个小 MLP 之类的。而我是在与全归约整个网络的成本做比较。从某种意义上说，加起来是一样的。好的。

---

All right. OK, good. So in practice, if you look at the maximum size that can fit on, let's say, a A100 GPU, if you go from the baseline, you can not even fit a 7B model. And you go to ZeRO stage 3. You can now fit 50 billion parameter models and so on, right. So it becomes a lot easier to fit these big models using FSDP. Right, the improvements that you get in terms of the memory improvement is quite significant.

好了，好的。在实践中，如果你看看能放进去的最大模型大小——比如说在一个 A100 GPU 上——从基线开始，你连一个 7B 模型都放不下。而用 ZeRO 阶段 3，你现在可以放进 500 亿参数模型等等。所以使用 FSDP 来装下这些大模型变得容易多了。你在内存方面的改进非常显著。

---

OK, yes. So can you go back to the previous slide? So regarding this on 8x1 A100, what would be the limitation on H100 or P200? OK, I can't do the mental math of multiply by 141 and divide by 80, but that would be the number for an H200. And so on and so forth. Yeah, it would be linear, right. It wouldn't really change the math very much, though, to go from one accelerator to up.

好的。"你能回到上一张幻灯片吗？关于在 8x1 A100 上的这个数字，在 H100 或 P200 上的限制会是什么？"好的，我没办法心算乘以 141 再除以 80，但那就是 H200 的数字，以此类推。是的，它是线性的。从一个加速器到另一个，数学上不会变化太大。

---

OK, so FSDP, I think, is very clean. It's very elegant. I like it a lot. I wish I could end the lecture here. But unfortunately, we will have to proceed into uglier and more hairy things. And there's two reasons why we have to do that. One of them, and this is an important idea for parallelization, is that in some sense, data parallel is consuming an important resource. And that resource is the batch size, so to speak, right. If you have a batch size of 8, you can never have more than eight accelerators, right. And you might think, OK, let's just make the batch size bigger and bigger and bigger as we have accelerators. You can't do that, because at a certain point, there's something called the critical batch size, where the basically gain that you get from the additional batch element is less than if you had taken another SGD step on that single element, right. So there comes a point where at small batch sizes, adding extra elements is perfectly helpful. It's the same as taking more SGD steps. But at a certain point, diminishing return hits in. An infinitely large batch size is not infinitely better than infinite steps, right. Infinite single steps. Because of this, now we have faced a hard tradeoff. Do we want small batch sizes and let our GPUs be more idle? Do we want big batch sizes and take the hit from optimization? Hard to say, rigt.

好的，FSDP 非常简洁、非常优雅。我很喜欢。我希望讲座就在这里结束。但不幸的是，我们不得不进入更丑陋、更棘手的事情。有两个原因。第一个——这是并行化的一个重要思想——在某种意义上，数据并行正在消耗一种重要资源，那就是批次大小（batch size）。如果你的批次大小是 8，你永远不可能拥有超过 8 个加速器。你可能会想，随着加速器增加，我们就把批次大小做得越来越大。你不能这样做，因为到了某个点，有一个叫做**临界批次大小**（critical batch size）的东西——增加批次元素带来的收益会小于你对这个元素单独做一次 SGD 步骤的收益。在小的批次大小下，增加额外元素是很有帮助的，相当于多做了 SGD 步骤。但到了某个点，收益递减（diminishing returns）就开始了。无限大的批次大小并不比无限多的步骤更好。正因如此，我们面临一个艰难的权衡：是想要小的批次大小从而让 GPU 更空闲？还是想要大的批次大小从而承受优化上的损失？很难说。

---

There's another issue that we have, which is that we still have memory issues, which is ZeRO stages 1 and 2 don't really let you scale memory at all. And ZeRO stage 2 lets you cut up the parameter memory. But unfortunately, there's activation memory and other kinds of memory use that this does not split up or this does not reduce at all, right. And so we need better ways, more fine grained ways, of cutting up the model in order to really start pushing down the memory use beyond these points, right.

我们还有另一个问题——我们仍然有内存问题。ZeRO 阶段 1 和 2 实际上根本不能让你扩展内存。ZeRO 阶段 2 让你可以切分参数内存，但不幸的是，**激活值内存**（activation memory）和其他类型的内存使用是它无法拆分或减少的。所以我们需要更好的方法、更细粒度的方法来切分模型，才能真正将内存使用降低到这些点以下。

---

And so this takes us to various model parallelism ideas. And so model parallelism is going to be this idea of essentially like FSDP, we're going to split up the parameters across GPUs. But I think the important conceptual difference between what we talked about and what we will talk about next is that now we are going to communicate activations. Right, in FSDP, we cut up the parameters. But in some sense, it was just a wrapper. We were still doing the normal computation. We were just sending parameters back and forth before doing it. Right, so parameters were the things flying around. Now what we're going to do instead is we're going to communicate activations back and forth, right. So if, for example, one layer lives on GPU 0, the next one lives on GPU 1. Right, what I have to communicate is the activation of the layer in between. Right, so that's going to be the big difference. And this will involve pipeline parallel, which is cutting up layers, tensor parallel, which is cutting up matrices, and expert parallel, which is sharding experts into different places. Right, and Percy's talked about tensor parallel already, so you have roughly some mental model of this.

于是我们进入了各种**模型并行**（model parallelism）的思想。模型并行的概念类似于 FSDP——我们将参数拆分开来放到不同 GPU 上。但我认为我们之前讨论的和接下来要讨论的重要概念区别在于：现在我们将通信的是**激活值**（activations）。在 FSDP 中，我们切分了参数，但某种意义上它只是一个包装器——我们仍然在做正常的计算，只是在做之前来回发送参数。参数是在到处传递的东西。而现在我们要做的是来回通信激活值。例如，如果一层在 GPU 0 上，下一层在 GPU 1 上，那么我需要通信的就是两层之间的激活值。这是很大的区别。这将涉及：**流水线并行**（pipeline parallelism）——切分层；**张量并行**（tensor parallelism）——切分矩阵；以及**专家并行**（expert parallelism）——将专家分片到不同的位置。Percy 已经讲过张量并行了，所以你们大致有个概念。

---

I'll start by talking about pipeline parallel or layer wise parallel. This is, I think, conceptually very simple. Back in the days when I first learned about parallelism, I was like, ah, yes, it's simple. Just cut up the layers and put them on different GPUs. Right, very simple thing. And so you're going to pass activations forward in the forward pass, and then you're going to pass like partial gradients backwards in the backward pass. Now, OK, if I do this, what will happen? You will get a terrible looking picture like this. Very, very depressing. I have four accelerators, each handling a quarter of the model. And so what computation happens as a function of time. So time is sweeping from left to right. And the different accelerators are the different rows. So first, my zeroth accelerator at the bottom here, that's handling the first layer will do some computation. And then it will stop, right. And then it will hand off the computation to the second one. And then it will do nothing for the rest of time until the very end. And then I will basically be passing things back and forth. And one GPU will be active at a time. And then coming backwards, one GPU will be active handling the backward pass at a time. And so most of the time, my GPUs are idle. My utilization is truly, truly terrible. And this is called a bubble. It's the part of the pipeline where you're not doing anything.

我先从流水线并行或逐层并行（layerwise parallel）讲起。我认为这在概念上非常简单。早年我第一次学习并行时，我的反应是"啊，是的，很简单。就把层切开放在不同的 GPU 上。"非常简单。在 forward 中将激活值向前传递，在 backward 中将部分梯度向后传递。但如果这样做，会发生什么？你会得到一张像这样糟糕的图——非常非常令人沮丧。我有四个加速器，每个处理模型四分之一。计算随时间的变化如下：时间从左向右推进，不同行代表不同加速器。首先，底部第 0 个加速器（处理第一层）做一些计算，然后停止，把计算交给第二个，然后它在剩下的时间里什么都不做，直到最后。基本上就是来回传递东西，一次只有一个 GPU 活跃。在反向传播时，一次也只有一个 GPU 活跃处理反向。所以大多数时候，我的 GPU 都是空闲的。我的利用率真的非常非常糟糕。这被称为**气泡**（bubble）——流水线中你什么都没做的那部分。

---

And the solution to this is to essentially do a batching or pipelining. So instead of doing a simple one layer after another, you're going to have a pipeline, right. Where, in this case, in this picture here, you have four elements to be processed. And as soon as you process one, you start on the next element, and then you pass off the one that's already done to your next layer. Right, so you can do this to essentially pass elements upwards and then back downwards. And so if you want to make this reasonable, then what you need is the ratio of essentially this bubble time to the useful compute. The utilization, in some sense, is going to be the number of stages divided by this micro-batches. And so we need a huge batch size in order to reduce this bubble towards 0. Right, so if we want our bubble to be 0, it's going to go down as 1 over the microbatch size. This is why I said batch sizes are useful resource. Because now we can spend it in a different way, which is to pipeline more to reduce the amount of idle time in pipeline parallel.

解决方案本质上是做批处理或流水线化。与其简单的一层接一层，你要有一个流水线（pipeline）。例如在这张图中，你有四个元素要处理。一旦处理完一个，就开始下一个元素，并把已经完成的传给下一层。你可以这样把元素向上传递再向下传递。如果你想让这个东西合理，你需要的是气泡时间与有效计算的比例。利用率某种程度上等于阶段数除以微批次（micro-batches）数量。所以我们需要巨大的批次大小来将气泡减小到接近 0。如果我们希望气泡为 0，它会按照 1/微批次大小 的比例下降。这就是为什么我说批次大小是一种有用的资源——因为我们可以通过不同的方式来使用它，即增加流水线深度来减少流水线并行中的空闲时间。

---

OK, so pipelines are terrible. And by folklore, people say things like, parallelization code looks reasonable and people can understand it until you implement pipeline parallel. So why do we do pipeline parallel? Well, pipelines can save memory compared to DDP. Because we've cut up layers, and you can also compose this with data parallel. So you can do both. But the other reason why this is a very important idea to learn, and you will always have a pipeline in certain kinds of topologies, is that it has very good communication properties compared to both FSDP and compared to any other kinds of things you can do. It only depends on activations, like b times s times h. It is also point to point. One layer is going to communicate to another. It's not all to all. And so depending on how you sequence these things, they can be a very efficient way to utilize your network. So in practice, what we're going to do is that pipelines are going to live on the slowest networking links. So if you have multiple data centers or multiple pods that are slower to talk to, you're going to parallelize across those two using pipelined parallel, because that's the most communication efficient parallelism that you can bring to bear here.

好的，流水线很糟糕。根据经验，人们常说：并行化代码看起来很合理，人们能理解，直到你实现流水线并行。那为什么还要做流水线并行呢？流水线相比 DDP 可以节省内存，因为我们已经切分了层，而且你还可以将其与数据并行组合。但另一个重要原因是：它在某些拓扑中你总是需要流水线，而且它相比 FSDP 和其他任何方法都有非常好的通信特性。它只依赖于激活值，比如 b × s × h。它也是点对点（point-to-point）的——一层与另一层通信，而不是全对全。所以取决于你如何排序这些操作，它们可以是一种非常高效的利用网络的方式。在实践中，我们将流水线放在最慢的网络链路上。如果你有多个数据中心或多个 pod，它们之间的通信较慢，你就用流水线并行在它们之间做并行化，因为这是你能使用的最通信高效的并行方式。

---

OK. And as I said, pipeline performance is really dependent on batch size. So I'll point out this paper repeatedly, but I'll mention which one this is. Now this is the Megatron paper from NVIDIA. They have a bunch of really lovely parameter sweeps of what happens to utilization as a function of different configurations you can do. So if you have large batch sizes and you pick a large pipeline size, you can get pretty good utilization close to not doing pipeline parallel at all. But you need the big batch sizes in order to be able to keep utilization up. Otherwise, pipeline parallel is going to rapidly degrade your utilization and performance.

正如我所说，流水线的性能非常依赖于批次大小。我会反复提到这篇论文，就是 NVIDIA 的 Megatron 论文。他们做了一系列非常漂亮的参数扫描，展示了利用率在不同配置下的变化。如果你有大的批次大小并选择大的流水线规模，你可以获得相当好的利用率，接近完全不使用流水线并行。但你需要大的批次大小来维持利用率，否则流水线并行会迅速降低你的利用率和性能。

---

Actually, I'm going to pause for a moment here to ask questions, because the next slide is complicated. Yes?

实际上，我想在这里暂停一下，给大家提问的机会，因为下一张幻灯片比较复杂。请讲？

---

So you mentioned on the previous slide that pipelines have good communication properties, like the FSPD. What is the specific mechanism for why that is? It's a smaller amount of stuff that's being communicated. So it's batch times sequence length times hidden. And that's almost always a smaller amount of data than attempting to communicate a whole parameter matrix, right.

"你在上一张幻灯片提到流水线具有良好的通信特性。具体机制是什么？" 因为通信的数据量更小——批次 × 序列长度 × 隐藏维度。这几乎总是比试图通信整个参数矩阵的数据量要小。

---

So people have tried to figure out much more clever ways of reducing the amount of pipeline sizes. And you can do clever things that cut up the different stages of what you're doing for different layers or different micro-batches. So you can sequence different forward pass elements in between different backwards pass elements. And by doing clever scheduling, you can further reduce the bubble size. This was taken from the DeepSeek paper. So by really cleverly manipulating when you're doing forward and backward computation, you can get a little bit better in terms of the bubble size.

人们试图找出更巧妙的方法来减少流水线的气泡大小。你可以做巧妙的安排，将不同层或不同微批次的不同阶段切分开来。你可以在不同的反向传播元素之间穿插不同的前向传播元素。通过巧妙的调度，你可以进一步减小气泡大小。这张图取自 DeepSeek 的论文。通过非常巧妙地控制前向和反向计算的时机，你可以让气泡大小变得更好一些。

---

But I think the even more clever thing that you can do, which is called zero bubble pipelining, is not really about scheduling per se. But it's actually about thinking carefully about the structure of your backward pass. So in the backward pass, there's really two things that have to happen. If you think about it, you're going backwards in your computation graph. And as you do that, you're going to do two things. One is going to be you're going to propagate your partial derivatives further down your computation graph. So remember, back propagation, you start at the end, and you're propagating these partial derivatives back, right. So you have to do that. But you also want to compute the gradients for the current weight. Right, so you have two things that you do at every node of your computation graph. You're going to propagate backwards, and you're going to compute the derivative of your weight. The important thing about thinking about this compute graph is actually, one of these two is really important for pipelines. And the other one, you can do whenever. Propagating the partials backwards, right, that's very important. Because your next stage can't do any work until you've propagated that signal back. On the other hand, the derivative with respect to the weights, that is a leaf node, so to speak, on this graph. And I can do it whenever, right. And so the clever thing to do now is you separate these two. Right, so you got your B's over here. These B's are the backwards, propagating backwards. And then these W's, these W's are computing the derivative of the weights. And they can happen whenever. So what you do is you compute the B's as quickly as you can. Right, so those come first. And then you can defer the W's until later and do it when you have a gap in your computation. And when you do this, you can basically almost all completely fill up the pipeline.

但我认为更巧妙的是所谓的"零气泡流水线"（zero bubble pipelining），这并不完全是调度本身的问题，而是关于仔细思考反向传播的结构。在反向传播中，实际上需要做两件事。当你在计算图中反向传播时，你要做两件事：一是将偏导数（partial derivatives）进一步向下传播到计算图中——记住反向传播是从末尾开始，将这些偏导数往回传播——这必须做；二是计算当前权重的梯度。在计算图的每个节点上你都要做这两件事。思考这个计算图时，重要的一点是：这两者中有一个对流水线非常重要，而另一个你可以在任何时候做。将偏导数往回传播非常重要，因为下一阶段必须等到这个信号传播回去之后才能开始工作。而相对于权重的导数，它是这个图上的"叶子节点"，你可以在任何时候做。所以巧妙之处在于你把这两者分离开：B 是反向传播（propagating backwards），W 是计算权重的导数。W 可以在任何时候做。所以你尽可能快地计算 B（先做 B），然后把 W 推迟到后面，在计算有空隙的时候再做。这样做时，你基本上可以几乎完全填满流水线。

---

And the zero bubble pipelining thing is very complicated or much more complicated than you would normally like to deal with. But it allows you to almost deal with these pipelining issues almost entirely, depending on essentially the workload involved in the W versus the B, and so on and so forth. But I think having seen this, I was like, oh, this is so clever. Such clever things that you can do with systems.

零气泡流水线非常复杂，比通常你愿意处理的要复杂得多。但它让你几乎完全可以解决这些流水线问题，具体取决于 W 与 B 所涉及的工作量等等。但我看到这个的时候，心想：哦，这太巧妙了——你能用系统做这么巧妙的事情。

---

OK, so that was pipelining. Any questions about that? Good. So I think there's a natural analogy or a parallel you can think of. So pipeline parallel is like depth. So your depth, you cut up your network along the depth dimension. But we have two ways that we scale, right. We've got a depth axis and we have a width axis. So what if we start cutting up our model along width, right? So this is tensor parallel, as Percy explained before. And it's really the simple idea that matrix multiplies can be cut up into smaller matrix multiplies, which you then add the partial sums back together. This is really the same idea as tiling as well. So this core primitive just appears many, many times.

好，以上就是流水线的内容。有什么问题吗？很好。你可以想到一个自然的类比：流水线并行类似于深度——你沿着网络深度维度切分。但我们有两种扩展方式：深度轴和宽度轴。那么，如果我们开始沿着宽度切分模型呢？这就是张量并行（tensor parallelism），Percy 之前解释过。它的核心思想很简单：矩阵乘法可以被切分成更小的矩阵乘法，然后将部分和加在一起。这实际上和分块（tiling）是同一个思想。这个核心原语出现了很多很多次。

---

And so when you do this in practice, right, what does this actually look like? So this is a GeLU that's happening. So what do you normally do? You have your x coming in as input on the very right of this slide here. And then I have a matrix A that I multiply with. I apply my non-linearity GeLU. And then I multiply with B to downproject. And then I output my z. Right, this is the normal serial computation that I do. Now in tensor parallel, what I would do is I would cut out my A into two submatrices, my B into two submatrices, and then I would run the computations in parallel, and I would gather them together at the end.

在实践中，这看起来是什么样子？这里是一个 GeLU 操作。通常你做的：输入 x（在这张幻灯片的最右侧），乘以矩阵 A，应用非线性 GeLU，再乘以 B 进行下投影（downproject），然后输出 z。这是正常的串行计算。在张量并行中，我会把 A 切成两个子矩阵，B 也切成两个子矩阵，然后并行运行计算，最后收集在一起。

---

Now, one thing that is important is there's a duality between the forward and backward pass. So in the forward pass, all I do with the x is I copy them twice, and then I run the computation forward. So f is the identity, this f function. And then once I get to the end of my parallel component, the g function, that's an all-reduce that brings them back together, right. But in the backwards pass, as I'm doing my gradients, this is going to flip. My g is going to be on-- sorry, my g is going to be an identity. Right, because the partial derivatives are coming backwards. And then my f are the partials that I need to sum up in order to get my partial derivatives at the start of this module. Right, so they're going to flip. And this duality is important if you're going to write tensor parallel.

有一点很重要：前向和反向传播之间存在对偶性（duality）。在前向中，我对 x 所做的只是复制成两份，然后往前计算。所以 f 是恒等函数。到了并行组件的末尾，g 函数是一个全归约，将结果收回来。但在反向中，情况会翻转——g 变成恒等函数（因为偏导数是从后面传回来的），而 f 是那些需要求和才能得到模块起点偏导数的部分。所以它们会翻转。如果你要写张量并行，这种对偶性很重要。

---

OK. And so you might have already noticed, right. But when we split things, some of the ways that we are going to be column-wise. So column-wise, tensor parallel is going to happen at the inputs. Right, so the inputs of the MLP, the projections of the attention are going to be cut up by the columns in each transformer block. So this is column-wise cuts. And then there's going to be row-wise cuts in the corresponding second stage. So in the downprojections of the MLP, as well as the outputs of the attention, you're going to have a row-wise cut. And then everything that's a small layer, like a layer norm or a non-linearity or routers in ML-- sorry, in MoEs, those are all fully replicated across the machines. You don't really want to bother with the overhead of cutting those guys.

你可能已经注意到了，当我们拆分时，有些是按列（column-wise）进行的。按列张量并行发生在输入处——MLP 的输入、注意力的投影矩阵在每个 Transformer 块中被按列切分。然后在对应的第二阶段，会有按行（row-wise）切分——MLP 的下投影以及注意力的输出都是按行切分。至于所有的小层，比如层归一化（layer norm）、非线性激活函数或 MoE 中的路由器（routers），都完全复制到各台机器上——你真的不想花力气去切分它们。

---

OK. And then, so when do we do tensor parallel? Tensor parallel is extremely computation hungry. What you're doing is every time you have a matmul, you're going to be doing some communication. Right, you have an all-reduce. Or in the backwards pass, you have all-reduce here. One in the G when you're going forward. And these are activation size, and you're doing them very frequently. So this is very communication hungry. And so you only want to do this within a node. So for GPUs, GPUs are going to be networked tightly together in a single box. And so up to eight, you might be willing to do some tensor parallel. Once you go beyond that, you're going to be going cross node. And those interconnects, those connections, are much slower. And so you're going to get a big drop in performance as soon as you hit that point of going beyond a single machine. So tensor parallel, you should remember as very communication hungry. You usually use it in the fastest interconnects that you have at hand.

那么什么时候做张量并行？张量并行对计算要求极高。你每次做矩阵乘法时都要做一次通信——前向中有一个全归约，反向中也有全归约。这些通信量是激活值大小，而且非常频繁。所以它对通信要求极高。你只希望在节点内做这个。对于 GPU，GPU 在单个机箱内紧密连接在一起，最多 8 个，你也许愿意做一些张量并行。一旦超出这个范围，你就要跨节点了，那些互连要慢得多。所以一旦超出单台机器，性能就会大幅下降。张量并行——你应该记住——对通信要求极高，你通常把它用在你能拥有的最快互连上。

---

And this is the point at which I'm going to go back to the thing I said about TPUs. Right, remember for TPUs, you don't really have this distinction between fast eight GPUs and next machines. You just have this big mesh. And so one of the big advantages that TPU people will tell you is you can tensor parallel very large numbers compared to the GPU world, because they're able to have high bandwidth in this very regular communication pattern over this mesh. Right, so that's a big difference if you're parallelizing between TPUs versus GPUs. The amount of tensor parallelism you use versus pipeline parallel will actually be quite different.

这就是我要回到之前关于 TPU 的话题的地方。对于 TPU，你在"快速 8 GPU"和下一台机器之间没有这种区分——你只有一个大网格。所以 TPU 的人会告诉你的一大优势是：与 GPU 世界相比，你可以做非常大规模的张量并行，因为他们能在这个网格上通过非常规则的通信模式获得高带宽。所以在 TPU 和 GPU 之间做并行化时，这是一个很大的区别——你使用的张量并行量与流水线并行量会非常不同。

---

So how do we compare these two? They're both model splitting strategies. They'll both save on both parameters and potentially activations. The pros here of tensor parallel is that there's no necessarily pipeline bubble. And if your network's fast enough, you might be able to get full utilization. It's also low complexity. It's just cutting up some matmuls. But the con is that the communication is much larger. It used to be that you were doing b times s times h point to point communication. Now instead, I'm going to be doing something like a times b times s times h times roughly one all-reduce communication, right. So this is not even just point to point. This is all to all communication that needs to happen. So tensor parallel is great. Whenever we have high speed interconnects, every other time, we probably want to be using pipeline parallel.

那么我们如何比较这两者？它们都是模型拆分策略，都能节省参数和潜在的激活值。张量 Material 的优点是：没有必然的流水线气泡，如果你的网络足够快，你可能获得满利用率；复杂度也低——只是切分一些矩阵乘法。缺点是通信量大得多——以前你做的是 b × s × h 的点对点通信，而现在你要做大约 1 次 a × b × s × h 的全归约通信。所以这不仅仅是点对点通信，而是全对全通信。张量并行很棒，当我们有高速互连时；在其他时候，我们可能更想用流水线并行。

---

OK. So the last thing I want to talk about about-- we're talking about memory use, is to really think more carefully about memory. I think the most naive view of memory in deep learning and language modeling is something like, well, memory is just parameters. That's this green bit over here. Right, you have a certain number of bits you need to store for your parameters. That's it. I've already talked about optimizer state, which is important, which is this yellow box over here. But if you look at this plot, this is actual memory use as profiled in one of the PyTorch profilers. You'll find actually that this is not really the whole story. There's a lot of dynamic memory that needs to exist in a computation. You need to store all the activations. These are these big red bumps over here. And then as you compute your gradients, you need to store them in your backward sweep, right. And so really maximum memory usage happens a little bit after the maximum activation point. After you start sweeping backwards on your gradient, but you still need to compute a lot-- keep your activations, those are usually the maximum memory points, right.

好的，最后我想谈的是——我们在谈内存使用——要更仔细地思考内存。我认为在深度学习和语言建模中最朴素的内存观是："内存就是参数"——绿色的那一块。你需要存储一定数量的参数位，仅此而已。我已经谈过优化器状态（黄色的方块），这很重要。但如果你看这张图——这是 PyTorch profiler 中实际的内存使用情况——你会发现这并非故事的全貌。计算中存在大量动态内存：你需要存储所有激活值——这些红色的大块。然后在计算梯度时，在反向遍历中也需要存储它们。所以真正的最大内存使用发生在最大激活点稍后一点——当你开始反向传播梯度但仍然需要保留很多激活值时，那通常是内存使用的最高点。

---

So to reduce this, maybe we need to deal with this big red hump, this activation. And if you start looking at more modern workloads for language models, you start to find that as you get to bigger and bigger parameters-- forget the column that says present work. I'll talk about that in a moment here. But if you look at just the baseline columns of this plot, as you go to bigger models, for moderately large sequence lengths, your activations are just going to dwarf the parameter memory that you need. And so any memory saving strategy has to reason about activations in order to be fully effective. We can't just deal with parameter memory. That's not really sufficient for us.

为了减少这个，也许我们需要处理这个巨大的红色凸起——激活值。如果你开始关注语言模型更现代的工作负载，你会发现，随着参数越来越大——先忽略"present work"那一列——只看这张图的基线列，当模型变大时，对于中等长度的序列，激活值将远超你所需的参数内存。所以任何内存节省策略都必须考虑激活值才能完全有效。我们不能只处理参数内存——这对我们来说是不够的。

---

So if we're storing everything-- and this is a good, I don't know, statistic or rule of thumb to start with. If we need to store everything, the amount of activations that we need is going to be something like 34 times s times b times h, and that's going to be sequence length times batch size times hidden dimension size plus 5 times as over h. as is attention heads times sequence length divided by hidden dimension size. And this sbh dependence, right, is fundamental, because we expect to have to store something for every element of the sequence. We expect to have to store something for every batch element, and we expect to have to store something for every hidden dim size. Right, so we're going to see this sbh term repeatedly as we try to go through different ways of reducing activation memory and accounting for the total amount of activation memory. And in case you're curious where the terms come from, this odd looking term, the 5 as over h is going to come from the quadratic attention terms, including the dropout terms. And we can drop this term via recomputation if we do flash attention.

所以如果我们要存储所有东西——这是一个好的经验法则——我们需要存储的激活值大约是 34 × s × b × h，其中 s 是序列长度（sequence length），b 是批次大小（batch size），h 是隐藏维度（hidden dimension），再加上 5 × as / h（as 是注意力头数乘以序列长度再除以隐藏维度大小）。这种 sbh 依赖关系是根本性的，因为我们需要为序列的每个元素、每个批次元素和每个隐藏维度都存储一些东西。当我们尝试不同的减少激活值内存的方法并核算激活值总内存时，我们会反复看到 sbh 项。如果你好奇这些项从何而来，这个看起来奇怪的项 5 × as / h 来自二次注意力项，包括 dropout 项。如果我们使用 Flash Attention，我们可以通过重计算（recomputation）去掉这一项。

---

OK. Now what if we did tensor parallel? One of the promises that I made to you in talking about model parallelism was that we could reduce activation quite a bit. So now let's think about what happens. Well, tensor parallel is going to split out the matrix multiplies in attention and MLPs. So which parts are those? Well, the MLPs are 24 of those 34 that I talked about before. And the attention heads are 5 as over ht. Right, the second term over here. Now, I can reduce that by t, my tensor parallel size. And that's good. This is not bad. Because I've taken most of the memory, and I've made it scale linearly with the tensor parallel size t. So that's good. But it turns out that there are other things that you do. You might have a layer norm. You might have a dropout. You need to keep the inputs to attention and the MLP. Right, because the inputs to each layers need to be stored as residuals for the backwards pass. And unfortunately, these are not reduced with your tensor parallel size. Right, tensor parallel does not split the layer norm. And therefore, it does not split the activation for these guys. So this is unfortunate, because you were hoping that if you had 1,000 different GPUs in tensor parallel because you're Google, you might be able to reduce this activation dramatically. The unfortunate reality is that you're still going to suffer a 10 times sbh penalty for doing all of this.

如果我们做张量并行呢？我在谈模型并行时做出的承诺之一就是我们可以大幅减少激活值。张量并行会拆分注意力和 MLP 中的矩阵乘法。哪些部分？MLP 占了 34 项中的 24 项。注意力头是 5 × as / ht（第二项）。我可以将其除以 t（我的张量并行规模），这很好——大部分内存变成了与 t 线性扩展。但事实证明，还有其他东西：你有层归一化、dropout，你需要保留注意力输入和 MLP 输入——每一层的输入需要作为残差（residuals）存储在反向传播中使用。不幸的是，这些不会随着张量并行规模而减少——张量并行不拆分层归一化，因此也不拆分这些激活值。这很不幸，因为如果你像 Google 一样有 1000 个 GPU 做张量并行，你可能会期望大幅减少激活值。但不幸的现实是：做了所有这些之后，你仍然要承受 10 × sbh 的代价。

---

And so the last part that's usually used in composition with tensor parallel is this idea of sequence parallel. This is an extremely misleading name, because usually when I say sequence parallel, actually there's a thing called context parallel that is actually more natural for this name. But sequence parallel is the following idea. So what you're going to do is we have these remaining terms, 10 sbh. And these terms are very lightweight. They're like layer norms. They're stuff that doesn't have much computation. And what I'm going to do is I'm going to split them up somehow. And I'm going to split them up over the sequence axis rather than over the hidden axis. And this is going to then involve all-gathers and reduce-scatters before every operation where we need these.

所以通常与张量并行组合使用的最后一部分是**序列并行**（sequence parallelism）。这是一个极其误导人的名字，因为通常当我提到序列并行时，实际上有一个叫做上下文并行（context parallel）的叫法更贴切。但序列并行的思路是这样的：我们有剩下的 10 sbh 项，这些项非常轻量级——像层归一化之类计算量不大的东西。我打算以某种方式拆分它们，沿着序列轴而非隐藏轴拆分。这将在每次我们需要它们的操作之前涉及全收集和归约-散射。

---

And if you think about it, this is very reminiscent of FSDP. Right, we have this thing that we need. We need attention-- sorry, we need activations at some point. We need to compute the activations going forward, and we need the activations when we sweep backwards for the derivatives, right. But we don't need them now. So we're going to store them by splitting them up across the sequence axis and materializing them on demand. So I would say this is conceptually very similar to the FSDP style idea, where we're storing them in this sharded format, and then we're gathering them as we need them. And then as I said before, there's a duality to this. So in the forward pass, g is an all-gather. g bar is a reduce-scatter. In the backwards pass, this is going to be reversed. Right, the all-gather and reduce-scatter are going to be reversed between g and g bar.

仔细想想，这非常类似于 FSDP。我们在某些时候需要激活值——前向中需要计算激活值，反向中需要激活值来计算导数。但我们现在不需要它们。所以我们通过沿着序列轴拆分来存储它们，并在需要时实例化它们。所以我认为这在概念上与 FSDP 的思路非常相似——我们以分片格式存储，然后按需收集。如前所述，这存在对偶性：在前向中，g 是全收集，g bar 是归约-散射；在反向中，这将被反转过来——全收集和归约-散射在 g 和 g bar 之间互换。

---

So if I do this now, what do I get? Well, remember, with the no parallelism setting, the very first part, what I told you was you get this activation memory. Use 34 times sbh with an attention head component. With tensor parallel, I get to divide the MLP part and the attention part by t, but not all these other pointwise ops that I have. If I do sequence parallel, I've split these up by my accelerators as well, just in the sequence axis, which gives me now fully linear dependence. If I do activation recomputation, I can even drop this second term. Because remember, this is just the storage that I need for the softmax. So I can drop this through recomputation, which gives you sbh times 34 over t. This is nice to remember, because this is the lower bound of what you can achieve, reasonably speaking, for normal training for activation memory. And so if you want to do things like compute by hand whether your model will fit into a GPU, this is a good thing to remember. You need at least this much for activation memory. You're going to need some memory for your optimizer state, and you will need some memory for your parameters and your gradient. And once you have those things, you have a rough sense of how much memory you're going to need for your model.

那么这样做会得到什么？在无并行设置下，激活值内存为 34 × sbh 加上注意力头分量。有了张量并行，MLP 部分和注意力部分可以除以 t，但其他逐点运算不行。如果做序列并行，我也可以通过序列轴将这些部分在加速器之间拆分，从而实现完全的线性依赖。如果做激活值重计算，我甚至可以去掉第二项——因为那只是存储 softmax 所需的空间。这样你就得到了 sbh × 34 / t。这很好记，因为它是在合理情况下正常训练激活值内存所能达到的下界。如果你需要手动计算模型能否放入 GPU，记住这一点很有用——你至少需要这么多激活值内存，还需要一些优化器状态内存和参数及梯度内存。有了这些，你就对自己模型需要多少内存有了一个粗略概念。

---

OK, I'm going to stop here for a moment. I have talked through both pipeline and tensor parallel at this point, and so people might be a little bit confused. And we can talk through a few things before I move on to expert parallel. Good. Oh, yes? [INAUDIBLE] 24 over t is the MLP part. The MLP part cannot be optimized through the representation? You can recompute the MLP as well. You can do a lot more computation than what is listed here. But recomputation what is listed here is very computationally expensive, like a recomputation for MLP involves running the MLP again in the backward pass, which you probably do not want to do. Recomputation for attention is generally cheaper, yeah. Because you do it time-wise as well. And also you don't want to pay the quadratic cost. That's quite expensive. The quadratic cost. That's quite painful, yeah.

好了，我在这里暂停一下。到目前为止我已经讲了流水线并行和张量并行，大家可能有点困惑。在我进入专家并行之前，我们可以讨论一些事情。好的。请讲？[听不清] "24 / t 是 MLP 部分。MLP 部分不能通过重计算来优化吗？" 你也可以重计算 MLP，你可以做比这里列出的更多计算。但这里列出的重计算在计算上非常昂贵——比如重计算 MLP 需要在反向传播中再次运行 MLP，你可能不想这样做。注意力的重计算通常更便宜——从时间开销来看也是，而且你不想承担二次成本（quadratic cost）。二次成本相当昂贵，相当痛苦。

---

Cool, all right. So I'm going to now talk about the last ingredient in the standard parallelism toolbox, which is expert parallelism, right. Now that MoEs are very standard part of the toolkit, most big models are MoEs these days. And that allows us to take advantage of one of their big benefits, which is expert parallelism. And expert parallelism, I think of myself as being something analogous to tensor parallel. Right, in the sense that you're taking the MLPs, right, the FFN components of your network. And you're going to split them up in various ways, and you'll incur a communication penalty in the same way that you're maybe splitting up the matrices, except here you're splitting up the MLP across different devices. And the systems behavior of tensor parallel is-- oh, sorry, expert parallel-- is roughly like tensor parallel as well in the sense that this is a high bandwidth parallelism primitive that also reduces activation. But one important thing is that if you're doing an MoE, you almost always prefer using an expert parallel sharding strategy over tensor parallel.

好的。现在我要讲标准并行工具箱中的最后一个组件——**专家并行**（expert parallelism）。既然 MoE 已经成为工具包中非常标准的部分，如今大多数大模型都是 MoE。这让我们可以利用它们的一大优势——专家并行。我认为专家并行类似于张量并行——你取出你的 MLP（即网络中的 FFN 组件），以各种方式拆分它们，并承担通信代价，就像拆分矩阵一样，只不过这里你是在不同设备间拆分 MLP。张量并行的系统行为——哦，抱歉，专家并行的系统行为——也大致类似于张量并行，它是一种高带宽的并行原语，也能减少激活值。但有一点很重要：如果你在做 MoE，你几乎总是更倾向于使用专家并行分片策略而非张量并行。

---

And I've taken this screenshot from the parallelism guidelines from Megatron, which is NVIDIA's like parallelism library. It's a really wonderful library and document. And one of the guidelines, they say is, look, if you're going to do some of parallelism, either EP or TP, you should be using EP over RP. Why is that? Well, this is actually a good list of drawbacks for tensor parallel. If you have a matrix and then you cut up the matrix too finely, well, the matrices are going to start to get small and your GPU utilization will suffer. So you want your matmuls as big as possible, and tensor parallel reduces that. For MoE layers, it's a lot easier to route sparse token activations rather than to potentially route these dense big tensor parallel matmul activations. And then you can do things like route tokens exactly to the places that they need. And you can skip some computation-- or sorry, some overhead in the cases that if you're going to have MoE anyway, you might as well have the number of experts split up over all the devices.

我截取了 Megatron 的并行化指南中的一张截图——Megatron 是 NVIDIA 的并行化库，是一个非常棒的库和文档。其中一条指南是：如果你要做某种并行化，无论是 EP 还是 TP，你应该优先使用 EP 而非 TP。为什么？这实际上列出了张量并行的一系列缺点。如果你把一个矩阵切分得太细，矩阵会变小，GPU 利用率会受影响。所以你希望矩阵乘法尽可能大，而张量并行减小了它。对于 MoE 层，路由稀疏的 token 激活值比路由这些密集的大型张量并行矩阵乘法激活值要容易得多。然后你可以做诸如将 token 精确路由到它们需要去的位置之类的事情。而且如果你本来就要用 MoE，你可以省掉一些计算或开销，不如就把专家数量拆分到所有设备上。

---

Now, this-- sorry, yeah. This might make it seem like, all right, EP is great. Everyone should be doing expert apparel all the time. Unfortunately, expert parallel is still really complicated and still very difficult. I think everything that I've said after FSDP-- tensor parallel, pipeline parallel, systems wise is quite non-trivial to get working really well. And I'll just point to two different libraries not to tell you the details of what happens inside of them, but to tell you, this is seriously complicated business. DeepSeek has a library called DPP, which I think is one of my favorite things from the DeepSeek V3 era, which is basically their own library for doing expert parallel routing and dispatching, where they're looking at really low level GPU networking primitives in order to try to basically combine different operations or have the hardware handle certain operations in order to make MoE routing as efficient as possible. Similarly, NVIDIA has a library called Hybrid EP, which is a similar effort of having very efficient low level hardware implementations of expert parallel dispatching.

这可能会让人觉得："好的，EP 很棒，每个人都应该一直用专家并行。"不幸的是，专家并行仍然非常复杂和困难。我认为我在 FSDP 之后讲的所有东西——张量并行、流水线并行——从系统角度来说，要让它们真正良好运行是相当不平凡的。我只想指出两个不同的库，不是要告诉你们内部的细节，而是要告诉你们：这是非常复杂的事情。DeepSeek 有一个叫做 DPP 的库，这是 DeepSeek V3 时代我最喜欢的东西之一，基本上是他们自己的专家并行路由和调度库。他们着眼于非常底层的 GPU 网络原语，试图组合不同的操作或让硬件处理某些操作，以使 MoE 路由尽可能高效。类似地，NVIDIA 有一个叫做 Hybrid EP 的库，也是类似的工作——对专家并行调度做非常高效的底层硬件实现。

---

And just to give you the high level thing, right, the reason why this stuff is hard is you are doing a lot of all to all dispatching. If you look at the communications pattern of MoE, much like tensor parallel, every time you have a MLP, you're going to have to route tokens all sorts of different places, and you need to do this in a very latency sensitive way. Because your computation is waiting for your tokens to arrive. So reducing the latency of this dispatch is extremely, extremely important. And one final thing that is like a fun trivia about the DPP library is the deep sea cloaks are so intense that in order to optimize, like every last bit of performance, they basically looked and found undocumented ptx, which is like GPU machine code or machine code like things. And they found how to use these undocumented instructions to further accelerate their networking communication. So really, this is the level of stuff that you need in order to get to the frontier of parallelism efficiency.

简单概括一下：这东西难的原因在于你在做大量的全对全调度。看 MoE 的通信模式，很像张量并行——每次有 MLP 时，你都要将 token 路由到各种不同的地方，而且这必须以极低的延迟完成，因为你的计算在等待 token 到达。所以减少调度的延迟极其极其重要。最后说一个有趣的八卦：DPP 库的深度优化极其激进，为了榨干每一丝性能，他们基本上找到了未公开的 PTX（PTX 就像 GPU 机器码之类的东西），并学会了使用这些未公开的指令来进一步加速网络通信。所以，这就是达到并行效率前沿所需要的水平。

---

Finally, up until now, I've talked about all the parallelism primitives in isolation, like data parallel and so on and so forth. With the implicit assumption that you can just put them together like LEGO blocks. And this is true, for the most part, for basically all the other parallelism strategies. It's very easy to combine, I don't know, data and tensor parallel. Expert parallel has additional constraints that you want to be somewhat respectful of. Usually, the naive way to do data and expert parallelism, which I think is in many of the old libraries, is that the replicas for DP and EP are the same. So in other words, let's say I have a data parallelism of eight. I'm going to shard my experts across those eight replicas. And then my data will be split across those eight replicas and routed in various ways. Right, so in other words, you split your GPUs according to DP, and then your EP is a subset of that split. Right, and this is a very natural thing to do because you're routing tokens. But if you do this, there's a maximum bound to how far you can parallelize with EP. And it constrains how DP and EP And so I think this is the final complexity.

到目前为止，我一直孤立地讨论所有的并行原语——数据并行等等——暗含的假设是你可以把它们像乐高积木一样拼在一起。对大多数其他并行策略来说，这在很大程度上是成立的。数据并行和张量并行很容易组合。但专家并行有额外的约束需要你尊重。通常，做数据和专家并行的朴素方式——我认为很多旧库都是这样——是 DP 和 EP 的副本是相同的。也就是说，假设我的数据并行度为 8，我把专家分片到这 8 个副本上，数据也在这 8 个副本之间拆分并以各种方式路由。换句话说，你按照 DP 分割 GPU，然后 EP 是这个分割的子集。因为你在路由 token，这是很自然的做法。但如果你这样做，EP 的并行度有一个最大上限，并且这约束了 DP 和 EP 之间的关系。所以我认为这是最后的复杂性。

---

I apologize that expert parallel is a little bit really messy in many ways. But because of these complexities, there is actually this one interesting systems thing that I'll tell you about before I stop talking about EP, which is this following fact. Remember, MoEs only change the MLPs, right. They don't change the attention at all. Right, so because we're cutting up the MLPs, but not the attention, this means that expert parallelism kind of applies unevenly to the model. So when I parallelize at the expert level, I'm parallelizing the MLPs, but I'm not parallelizing the attention, right. And so in order to parallelize the attention, maybe I want to also use tensor parallel, right. So I want a high tensor parallel level in order to cut out my attention. But this is going to then affect my MLPs. Because if I have high tensor parallel and high expert parallel, I've cut out my matrices into really tiny pieces, and my utilization is very bad. So there's this weird tradeoff where you want high tensor parallel for the attention, but you want low tensor parallel for the MLPs. So there's this conflict.

我很抱歉，专家并行在很多方面确实有点混乱。但正因为这些复杂性，在结束 EP 话题之前，有一个有趣的系统问题要告诉你们。记住，MoE 只改变 MLP，完全不改变注意力。因为我们切分了 MLP 但没有切分注意力，这意味着专家并行不均匀地应用于模型。当我在专家层面并行化时，我是在并行化 MLP，而不是注意力。为了并行化注意力，我可能想同时使用张量并行——所以我想用高张量并行度来切分注意力。但这会影响 MLP——如果我有高张量并行和高专家并行，我就把矩阵切分成了非常小的碎片，利用率会很差。所以存在一个奇怪的权衡：你希望注意力使用高张量并行，但希望 MLP 使用低张量并行。这就产生了矛盾。

---

So what do you do? Well, in the last few years, people have come up with more complicated system solutions that decouple the tensor parallel in the MLPs and the attention. And so the attention layers get one kind of tensor parallel, and the MoE layers get another kind of tensor parallel. And so now you can fully decouple the parallelism. And this leads to more complicated but more effective combinations of EP and tensor parallel, as well as data parallel.

那该怎么办？在过去几年中，人们提出了更复杂的系统解决方案，将 MLP 和注意力中的张量并行解耦。注意力层使用一种张量并行，MoE 层使用另一种张量并行。现在你可以完全解耦并行性了。这导致了更复杂但更有效的 EP、张量并行以及数据并行的组合。

---

Cool. OK. So the last thing in this space that I want to end with is context parallel. So context parallel or ring attention is an idea of basically splitting activations in a very long sequence across different accelerators. And you can do things like pass the activations to the device that's needed in this ring-like way following the mesh topology of TPUs. And so ring attention, which I think was the original paper that did this, showed that this worked really well on TPUs. Context parallel is a standard parallelization strategy that does this. Both of these are used in long context extension stages and in model serving. I'm not going to talk about it, mainly because I think it overlaps in concept to a lot of what we've talked about already.

好的。最后一个我想讲的是**上下文并行**（context parallel）。上下文并行或**环形注意力**（ring attention）的思想基本上是在不同加速器之间拆分一个非常长的序列中的激活值。你可以沿着 TPU 的网格拓扑以环形方式将激活值传递给需要的设备。环形注意力——我认为是最早提出这个想法的论文——展示了这在 TPU 上效果很好。上下文并行是一种标准的并行化策略，也做同样的事。两者都在长上下文扩展阶段和模型服务（model serving）中使用。我不打算详细讲，主要是因为它在概念上与我们已经讲过的很多内容重叠。

---

OK. So this is the end of the second part. And I think to put everything together, I've made a big table of parallelization strategies, including data parallel, which are the top two rows and the various model parallelism strategies below them. And I think I've colored in red what I subjectively feel like are the drawbacks of the different methods. And the reason why I've colored things in red is to try to convey to you that there is no one strictly dominant parallelization strategy. It's all a whole bunch of tradeoffs that you somehow have to manage gracefully in order to get a good outcome. So for example, FSDP is great. It's a wonderful strategy. Does not help you with activation. It consumes your global batch size in order to do parallelization. So it has limits. And to address these, maybe you want to compose them with some of these other tricks that you have at hand. Maybe you want to do some tensor parallel to cut down on activation memory. It also doesn't touch global batch size. But if you do this, now you need fast networking and you need high bandwidth. And also then to leverage your slower connections, maybe you want to use some of the other parallelization strategies. Right, so you see how all of these different advantages means that there's a place for one of these parallelization strategies in not every architecture, but in many large scale architectures, you use a large combination of these.

好了，第二部分到此结束。为了总结所有内容，我做了一个并行化策略的大表格，包括数据并行（上面两行）和下面的各种模型并行策略。我把主观上认为的每种方法的缺点标成了红色。这样做的目的是告诉大家：没有一种严格占优的并行化策略——你需要优雅地管理一大堆权衡才能获得好的结果。以 FSDP 为例：它很棒，是一个非常好的策略，但它不能帮你解决激活值问题，而且它消耗全局批次大小来进行并行化——所以它有局限性。为了解决这些问题，你可能想用一些其他技巧——也许做一些张量并行来减少激活值内存，这也不影响全局批次大小。但这样你又需要快速网络和高带宽。然后为了利用较慢的连接，你可能又需要使用其他并行化策略。所以你看，所有这些不同的优势意味着——不是在每种架构中，但在许多大规模架构中——你会大量组合使用这些策略。

---

Yes? [INAUDIBLE] Are they still applicable to MoEs, or is that strictly-- Yeah. So the question was, is pipeline and, what, FSDP applicable to MoEs? Yes, yes, they're absolutely applicable. If anything, the standard recommendation is expert parallel is like tensor parallel. So you want to go up to 8 or fast connections. People don't really follow that anymore. But even then, FSDP or data parallel in general and pipeline and tensor are used extensively in all the frontier models. Yeah.

请讲？[听不清]"它们（流水线和 FSDP）仍然适用于 MoE 吗？还是只适用于密集模型？"问题问的是流水线和 FSDP 是否适用于 MoE。是的，它们绝对适用。标准的建议是专家并行类似于张量并行——所以你要做到 8 或者使用快速连接。人们现在不再完全遵循这个了。但即便如此，FSDP（或一般意义上的数据并行）、流水线并行和张量并行在所有前沿模型中都被广泛使用。

---

Good. OK, and you will do this or something like this as part of your assignment. But one of the things that's cool about parallelism and I think is nice is that you can do some math, right. You can actually say, OK, how much compute do I do per layer for my different sharding strategies? How much communication do I do per layer for my different communication strategies? And if I have different devices allocated to different communication strategies, how do these things scale? And then I can figure out for a combination of these strategies, how do they scale? And you can start to make plots of, if I have a certain batch size and I have a certain parallelization strategy-- so I have three different parallelization strategies here. How much am I utilizing my GPU? The ratio of compute time to communications time. And as long as my compute time is longer than communications time, in principle, you can just hide communications underneath your computation. And so you can make plots like this where this dashed line at the very top, that's the boundary of where you're efficient. Anything above that is fully utilizing your computation. Anything below that is on the bad part of your roofline. You're waiting for communication to do your computation.

好的，你会作为作业的一部分做类似的事情。并行的一个很酷的地方在于你可以做一些数学计算：对于不同的分片策略，每层做多少计算？对于不同的通信策略，每层做多少通信？如果不同的设备分配给了不同的通信策略，它们如何扩展？然后你可以算出这些策略组合如何扩展，并开始绘制图表：给定某个批次大小和某个并行化策略，我的 GPU 利用率是多少？计算时间与通信时间的比值。只要我的计算时间长于通信时间，原则上你就可以把通信隐藏在计算之下。于是你可以绘制这样的图——最上面的虚线是效率边界。在这条线之上，计算被充分利用；在这条线之下，就处于屋顶线（roofline）的不利区域——你在等待通信来完成计算。

---

One thing that's pretty interesting here, right. So I think this should feel intuitive to you based on what I've told you. If your batch size is big enough, FSDP only is good. Right, if you have a batch size of 2,000, right, per chip, then you how far can you go? Well, you've got FSDP doing extremely well. You're fully compute bound, right. But the important thing is, as the batch size goes down, FSDP only will hit a point where you're now communication bound. Now, what do you do, right? Well, what do you do is now, in order to keep pushing efficiencies, you have to incorporate MP, in this case, is tensor parallel, to the mix. Right, now you can push that curve out a little bit more and be compute bound even into smaller batch size regimes, right. And you keep adding strategies to push this curve out in order to get something better. And this is what people call 3D or 4D-- I don't think there's 5D-- parallelism. Which is when you put all these strategies together to keep your compute units fully utilized under different communication topologies.

这里有一个非常有趣的点。根据我讲的内容，你应该能直观感受到：如果你的批次大小足够大，仅使用 FSDP 就很好。如果每芯片的批次大小为 2000，你能走多远？FSDP 表现极好——你完全受计算限制。但关键是，随着批次大小减小，仅用 FSDP 会达到一个点，此时你变为通信受限。那该怎么办？为了保持效率，你需要将 MP（即张量并行）加入组合。现在你可以把那根曲线再往外推，即使在更小的批次大小下也保持计算受限。你不断添加策略来外推曲线以获得更好的结果。这就是人们所说的**三维**（3D）或**四维**（4D）并行——我不认为有五维——当你将所有策略组合在一起，在不同的通信拓扑下保持计算单元充分利用。

---

There's a very simple prescription. I think up until now, I've been telling you things in generalities. So it might feel complicated. But I think actually the strategy for how you parallelize is very simple, actually. Which is, until your model fits into memory, you're going to cut up your model by whatever means necessary, right. And how are you going to cut up your model. You're going to use either tensor or expert parallel for your fast interconnect. And so if you have eight GPUs per machine, you're going to use a tensor expert parallel of eight. And then you're going to pipeline parallel or Zero-3, which is FSDP, the rest of the way to make your model fit. And once your model fits, then you're going to just data parallel the rest of the way. Right, then use up the rest of your GPUs with data parallel, right. If your batch size ends up being too small, you can do gradient accumulation to get better GPU utilization. Very simple strategy.

有一个非常简单的策略。到目前为止，我一直讲得很笼统，可能觉得很复杂。但实际上并行化的策略非常简单：在你的模型能放进内存之前，你用任何必要的手段切分模型。怎么切？你为快速互连使用张量并行或专家并行。如果每台机器有 8 个 GPU，你就使用 8 度的张量/专家并行。然后你用流水线并行或 ZeRO-3（即 FSDP）来让模型适合内存。一旦模型适合了，剩下的就用数据并行——用剩余 GPU 做数据并行。如果你的批次大小太小，你可以做梯度累积（gradient accumulation）来获得更好的 GPU 利用率。非常简单的策略。

---

And this is borne out in the actual large scale parallel training libraries that you might use. So I've added the link here to Megatron's guide to parallelizing MoEs. But this idea actually applies to the dense models as well. And you see exactly the thing that I said, but in reverse order. So guideline number one is minimize model parallelism, maximize data parallelism. Right, so use most of your GPUs to shard data if you can. Now, if you're using GPUs, stay within NVLink. So that's one machine, or so one box, right. Keep expert parallel and tensor parallel within one box. And then if you're going to go multi-node, use pipeline parallelism to go multi-node. And then if you're MoE, then prefer expert parallel. And then finally, if you're doing long sequences, use context parallel. Right, ring attention. So exactly what I've been trying to get across to you through the lecture, but in practitioner form that you see here.

这在你可能使用的实际大规模并行训练库中也得到了验证。我在这里添加了 Megatron 的 MoE 并行化指南的链接。但这个思路实际上也适用于密集模型。你会看到我刚刚说的内容，但以相反的顺序呈现：指南第一条——最小化模型并行，最大化数据并行——尽可能用大多数 GPU 做数据分片。如果你使用 GPU，保持在 NVLink 范围内——即一台机器或一个机箱。专家并行和张量并行保持在单机箱内。如果要跨节点，使用流水线并行实现跨节点。如果是 MoE，则优先使用专家并行。最后，如果做长序列，使用上下文并行（环形注意力）。这就是我整堂课试图传达的内容，以实践指南的形式呈现在这里。

---

OK, the final component-- actually, maybe I can pause here, in case anyone's curious about 4D parallelization stuff. Yeah. I know you said context parallel would be a better name for decreasing parallel [INAUDIBLE] Oh, yeah, yeah. Well, I mean, sequence parallel is often just you do it with tensor parallel in order to reduce activations. It's more of an add on that you put in in order to reduce activation. It's not its own standalone thing, in many cases. Yeah?

好的，最后一个组件——实际上，也许我可以在这里暂停一下，以防有人对四维并行化有疑问。"我知道你说过上下文并行更适合用来命名……" 哦，是的。序列并行通常只是与张量并行一起使用来减少激活值。它在许多情况下更像是一个附加组件，用于减少激活值，而不是独立的策略。请讲？

---

With the suspicions that this is like a loop transformer, like that, does that make things easier or harder. OK. I don't how much I buy the loop transformer mythos rumors. Maybe it is. It would be interesting. But to the question of how the systems structures would change, it's a good question. I mean, I guess it might mess with things like FSDP. You can't really discard the weights. It does have the advantage, though, that you don't have to keep getting weights. It is much more parameter efficient, and so maybe much of the model parallelism stuff wouldn't be as important. It would be interesting. It would be definitely different for a lot of the FSDP style things. Because the FSDP strategy is really predicated on getweights, discard weights, getweights, discard weights. And in a loop, you're not discarding anything.

"如果这是一个循环 Transformer，会让事情变得更容易还是更难？" 我不太相信循环 Transformer 的传说和传闻。也许是真的，这将会很有趣。但关于系统结构会如何变化，这是一个好问题。我猜它可能会搞乱像 FSDP 这样的东西——你不能真正丢弃权重。但它的优点是你不必反复获取权重，参数效率更高，所以也许很多模型并行的东西就没那么重要了。这会很有趣。对于很多 FSDP 风格的事情来说肯定不同——因为 FSDP 策略的前提是获取权重、丢弃权重、获取权重、丢弃权重，而在循环中你什么都不会丢弃。

---

Good, OK. All right. So this is an old paper, but it is actually probably one of the best resources. And also, it's not like the networking fundamentals changed that much. So I think the lessons from here are very relevant today. And so this is a paper by NVIDIA and formerly unfortunately, Stanford folks, Matei and Deepak, who did a bunch of runs of large scale parallel training across many different configurations to basically tell you, as you're scaling up, how should your parallelization strategies change across different scales? And you see exactly this prescription that I've been talking about before, which is, you have data parallel maxed out. And then your tensor parallel increases until it hits 8, and then you stop because you don't want to go any higher. And then from that point on, your pipeline parallel increases and increases and increases, right. And with sufficiently large scale, data parallel decreases. And at the very end, you have a DP of six. And this is because you just need this much tensor and pipeline parallel to fit the stuff. Right, and you're using the rest of your budget on data parallel.

好的，这是一篇老论文，但可能仍然是最好的资源之一。而且网络基础并没有变化那么多，所以这里的见解今天仍然非常相关。这是一篇 NVIDIA 的论文，作者包括（以前是斯坦福的）Matei 和 Deepak，他们做了大量不同配置下的大规模并行训练实验，告诉你：随着你的规模化扩展，你的并行化策略应该如何变化？你正好看到了我之前提到的策略：数据并行先最大化，然后张量并行增加直到达到 8，然后停止因为你不想再高了。从那以后，流水线并行不断增加再增加。在足够大的规模下，数据并行会减少。最后，你的 DP 为 6——因为你只需要这么多张量并行和流水线并行来装下模型，剩余预算用在数据并行上。

---

And if you put them all together, right, even as you go to ludicrously large numbers of GPUs, your utilization stays very flat and very good. And this is why I think you see this gigantic data center build-outs. The parallelization strategies people have come up with are so effective. And the hardware for communication is so good that even with the gigantic data centers or even cross data center training, you can get really good utilization across these different regimes.

如果你把它们组合在一起，即使当你达到荒谬的 GPU 数量时，你的利用率仍然非常稳定且非常好。这就是为什么你会看到如此巨大的数据中心建设——人们想出的并行化策略如此有效，而通信硬件如此之好，即使在巨型数据中心甚至跨数据中心训练中，你也能在不同阶段获得非常好的利用率。

---

They have really nice quantitative evidence showing you, for different batch sizes for tensor parallel, what is the right place to stop? And it's clearly tensor parallel size of 8. As you go beyond that, you're going to get into trouble. And pipeline parallel, you also need big batch sizes in order to be able to utilize the machines effectively. That's why there's a blue to orange gap. There's pipeline parallel. And the larger the pipeline parallel, the larger the gap between orange and blue. And then I think another thing that maybe you have already internalized from flash attention but maybe not is maybe you should do a bunch of activation recomputation. Because if you do activation recomputation very cleverly, then you can get a bigger batch size, and the bigger batch size then allows you to get better utilization. This is a, initially, I think, very counterintuitive observation that actually you should do more computation via recomputation in order to end up getting better utilization, because it allows you to save memory, and memory can be turned into batch size.

他们有非常好的定量证据，展示了对于张量并行的不同批次大小，应该在何处停下来。很明确是张量并行规模 8——一旦超出就会遇到麻烦。流水线并行也需要大的批次大小才能有效利用机器——这就是为什么存在蓝到橙的间隙——流水线并行越大，橙蓝间隙越大。然后另一件你可能已经从 Flash Attention 中内化了（也可能没有）的事是：你可能应该做大量的激活值重计算。因为如果你非常巧妙地做激活值重计算，你可以获得更大的批次大小，而更大的批次大小让你获得更好的利用率。这在最初是一个非常反直觉的观察：实际上你应该通过重计算来做更多计算，从而获得更好的利用率——因为它能让你节省内存，而内存可以转化为批次大小。

---

OK. So that was a more quantitative view of how to pick parallelism strategies. The last thing I want to end with is just to look at just a very few training runs. And looking at the training runs, maybe we can get a sense of how modern parallelization is used in practice and how it's evolving.

好的，以上就是关于如何选择并行化策略的更定量化的视角。最后我想看几个实际的训练案例。通过观察这些训练运行，我们也许可以了解现代并行化在实践中是如何使用的，以及它是如何演变的。

---

So Dolma by AI2 was a seven be open source model. Sorry, Olmo, which was trained on the Dolma data set. And this isn't the Dolma paper for the details. Was a 7B model trained fully with FSDP across a whole bunch of accelerators. I forget exactly how many. But this is one example of FSDP scales surprisingly well, even to many, many GPUs. As long as you're training a small model, FSDP is actually a pretty good strategy for parallelization. I think many 7D-ish models are trained purely with FSDP.

AI2 的 Dolma 是一个 7B 开源模型——抱歉，是 Olmo，在 Dolma 数据集上训练。这是一个 7B 模型，完全使用 FSDP 在一大堆加速器上训练。具体多少我忘了。但这是一例 FSDP 扩展到非常多的 GPU 时仍然出奇地好的例子。只要你训练的是小模型，FSDP 实际上是一种非常好的并行化策略。我认为很多 7B 级别的模型完全使用 FSDP 训练。

---

DeepSeek, because of their systems skills, does do some pretty exotic and useful stuff. So DeepSeek V1 was trained just with data parallel ZeRO stage 1 with tensor sequence and pipeline parallel, as I talked to you before. DeepSeek V3, that's a MoE model, if you remember my MoE lecture. So they have not only pipeline parallel, but they also have expert parallel instead of tensor parallel, right. And their expert parallel actually is a little bit exotic. Because they have 64 way parallelism. So they group eight different machines together, and that's their expert parallel domain. And to enable this large expert parallel, they basically use the same tricks that they have from their pipeline parallel pipelining in order to try to make sure that expert parallel doesn't have low utilization periods. So this is actually quite a complicated trick that they do to get these very large expert parallel splits.

DeepSeek，凭借他们的系统能力，做了相当特别且有用的事情。DeepSeek V1 仅用数据并行 ZeRO 阶段 1、张量并行、序列并行和流水线并行训练，我之前讲过。DeepSeek V3 是 MoE 模型——如果你还记得我的 MoE 讲座——他们不仅有流水线并行，还有专家并行替代了张量并行。他们的专家并行实际上有点特别：他们有 64 路并行，将 8 台不同的机器分组作为专家并行域。为了实现这样大规模的专家并行，他们基本上使用了与流水线并行相同的技巧来确保专家并行没有低利用率时段。这实际上是一个非常复杂的技巧，用来实现这些极大的专家并行拆分。

---

Another example, Yi, from Chinese open weights training setting. They use, once again, ZeRO stage 1 and tensor and pipeline parallel. Right, this very much makes sense. It's the classic data parallel, tensor parallel, pipeline parallel combo. And once again, once you go to MoEs, you replace the tensor parallelism with expert parallelism. Right, they serve similar goals. But expert parallelism is just a little bit more efficient.

另一个例子：Yi，来自中国的开放权重训练。他们再次使用了 ZeRO 阶段 1、张量并行和流水线并行。这非常合理——这是经典的数据并行、张量并行、流水线并行组合。同样，一旦你进入 MoE，你就用专家并行替代张量并行。它们服务于类似的目标，但专家并行稍高效一些。

---

On the other extreme of a really big dense model, you have Llama3. The Llama3 report, I liked quite a bit, because they're one of the few reports that have literally a full breakdown of their parallelism strategy. Not just like in the abstract, but across all the different phases. So the cool thing that you see is they have a pre pre-training stage, a little warm-up phase at the very start. You can ignore that first row. And then they have their main pre-training phase in the middle row here. And this is a very standard parallelization strategy. Tensor parallel of 8, one context parallel, 16 pipeline parallel, and 128 data parallel. Big data parallel splits. And then at the very end, because they want a long context model, they do long context extension. And for this, they crank up the context parallel, lower the data parallel. And that's how they parallelize this very memory hungry stage for long context extension.

另一个极端——非常大的密集模型——是 Llama3。我很喜欢 Llama3 的报告，因为他们是少数几个完整分解了并行化策略的报告之一——不只是抽象概述，而是横跨所有不同阶段。很酷的是：他们有一个预预训练阶段（pre pre-training stage），一个开始的预热阶段。可以忽略第一行。中间一行是主要预训练阶段，这是一个非常标准的并行化策略：张量并行 8、上下文并行 1、流水线并行 16、数据并行 128——大的数据并行拆分。然后在最后，因为他们想要长上下文模型，他们做长上下文扩展（long context extension），为此他们提高上下文并行、降低数据并行。这就是他们为这个非常消耗内存的长上下文扩展阶段进行并行化的方式。

---

And notice, we're in tensor parallel, not export parallel land. Because Llama3 405B is a gigantic dense model. It's not a MoE model. And as a side note, right, one thing that I don't talk about, but if you, for example, become an infra engineer at one of these companies, you'll notice is GPUs fail all the time. Apparently during Llama3 405B training, GPUs failed 148 times. And so you need lots of not just fast parallelism, you need redundancy in order to be able to deal with all these kind of horrible things that can happen to your training. So there's a distributed systems challenge as well.

注意，我们处于张量并行领域，而不是专家并行——因为 Llama3 405B 是一个巨大的密集模型，不是 MoE。顺便提一个我还没讲到的点：如果你成为这些公司的基础设施工程师，你会注意到 GPU 经常故障。在 Llama3 405B 训练期间，GPU 故障了 148 次。所以你不仅需要快速的并行化，还需要冗余来应对所有可能发生的可怕事情。所以分布式系统（distributed systems）本身也是一个挑战。

---

Gamma 2, which is a Google open source model, has FSDP plus tensor parallel and sequence parallel and uses these two strategies only. And the reason why I brought up Gamma 2 is, as far as I understand, this is basically a realization of the Google claim that for TPUs, really you don't need to do pipelines. You just take a really big toroidal mesh and you tensor parallel over that big mesh network that you have. Unclear whether this can scale out forever. That has always been a little bit less clear to me. But at least the gamma scales, this is definitely the case.

Gamma 2 是谷歌的开源模型，使用 FSDP 加张量并行和序列并行，只用了这两种策略。我提到 Gamma 2 的原因是：据我理解，这基本上是谷歌所声称的——对于 TPU，你真的不需要做流水线。你只需要一个非常大的环形网格，然后在那个大网格网络上做张量并行。不确定这是否可以永远扩展下去——这一点我一直不太清楚——但至少在 Gamma 的规模上，这确实是成立的。

---

Finally, I took a look at some of the models that were trained this year, like Mistral 8x22B, and during my investigation, one of the things that I discovered was actually if you're interested in model training and parallelism configurations in the wild, NVIDIA has a repository called Megatron Bridge, where they release a lot of recommended training configurations for a lot of different model sizes and model settings. And you can take a look at what they end up saying is the right model configuration for an 8x22B MoE or DeepSeek V3 modeling. And so for Mixtral, they do expert parallel of 8, pipeline parallel of 4, and an additional tensor parallel of 4. This one for the attention layers. And you see this follows the prescription of, keep your expert parallel roughly around eight.

最后，我看了看今年训练的一些模型，比如 Mistral 8x22B。在调研中我发现：如果你对实际中的模型训练和并行化配置感兴趣，NVIDIA 有一个叫做 Megatron Bridge 的仓库，发布了大量针对不同模型大小和设置的推荐训练配置。你可以看看他们对 8x22B MoE 或 DeepSeek V3 推荐了什么配置。对于 Mixtral，他们使用专家并行 8、流水线并行 4，外加张量并行 4（用于注意力层）。你可以看到这遵循了"保持专家并行大约在 8"的原则。

---

Nemotron 3 Super follows the DeepSeek V3 model, has a bunch of expert parallel as well as context parallel, because they were doing extensions, at least in this article. And then the last one that I want to talk about is Qwen 3, which follows the DeepSeek recipe, which is a fairly large amount of expert parallel 32. And they have eight pipeline parallel and two tensor parallel to split up things like the attention matrices.

Nemotron 3 Super 遵循 DeepSeek V3 模型，包含大量专家并行和上下文并行（至少在这篇文章中他们做了扩展）。最后一个我想讲的是 Qwen 3，它遵循 DeepSeek 方案——使用相当大规模的专家并行（32）、8 个流水线并行和 2 个张量并行来拆分注意力矩阵等。

---

It is actually interesting to see additionally the different kinds of benchmarking that NVIDIA folks have done for parallelizing different models. And you see, I won't go into details of what this is. This is in the NVIDIA bridge repo, if you want to take a look. There's all sorts of different configurations that you can pick even within tensor parallel that can significantly affect the performance of these. So the systems integration is quite significant.

另外有趣的是看到 NVIDIA 的人对并行化不同模型做的各种基准测试。我不会详细讲这些是什么——这都在 NVIDIA bridge 仓库里，如果你想看的话。即使在张量并行内部，也有各种不同的配置选择，会显著影响性能。所以系统集成相当重要。

---

So to put everything together, I decided maybe I would build an overview. Really, the thing that's common to this is as much as you can, all the models use data parallel. They maximize the data parallel domains to the extent that they can. Tensor parallel almost always remains below eight. And expert parallel can sometimes be big now. And I think that's partially because of DeepSeek V3 and a lot of the infra that they built for large scale expert parallel training.

为了总结一切，我决定做一个概述。真正的共同点是：尽可能多的模型使用数据并行——它们尽可能最大化数据并行域。张量并行几乎始终保持在 8 以下。专家并行有时现在可以做得很大——我认为这在一定程度上是因为 DeepSeek V3 以及他们为大规模专家并行训练构建的大量基础设施。

---

Good. OK. So to put everything together, right. The highest level point, right, of this lecture is we need to think about multi-GPU, multi-node, maybe even multi-data center parallelism. And to think about efficiency in that regime, we need to really bring to bear all the approaches that we have. Because you've got fast links, you've got slow links, you've got techniques that make use of batch sizes and all these different resources that you all want to consume as much as possible. But given all of these, it turns out that there's fairly simple rules of thumb for combining all these different forms of parallelism to get in the end what is effectively full utilization of your compute hardware.

好了，总结一下。本讲最高层次的要点是：我们需要考虑多 GPU、多节点甚至多数据中心的并行化。为了在这个层面上考虑效率，我们需要动用所有已有的方法。你有快速链路、慢速链路，有利用批次大小的技术，以及所有你想要尽可能消耗的不同资源。但考虑到所有这些，事实证明，有相当简单的经验法则来组合所有这些不同形式的并行化，最终实现计算硬件的近乎完全利用。

---

Great. And next week, I think we're talking about scaling laws.

好的。下周，我想我们会讲缩放定律（scaling laws）。

---
