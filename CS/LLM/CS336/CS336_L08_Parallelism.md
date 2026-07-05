# Lecture 8: Parallelism / 第八讲：并行

## 1. Introduction: Why Parallelism? / 一、引言：为什么需要并行？

So last lecture, Percy covered some of the underlying mechanics of parallelism. Today, I'm going to talk about all sorts of knowledge, details, and trivia about how modern parallelism for language model training works. We're going to really get to grips with the many, many complexities involved when you have to train huge models on huge clusters. It turns out there are many different parallelization strategies that you can use at once. At the end, we will get to a slide where I say 4D parallelism, because there are four different things you can do at once—actually, even more. And it turns out that to parallelize at the largest scale, you'll need to use all of them or most of them. Part of your assignment will be figuring out, given a particular network topology and a particular model, what is the optimal parallelization strategy for that.

上一讲，Percy 讲了一些并行的底层机制。今天我要讲的是现代语言模型训练中并行的各种知识、细节和琐事。我们将深入理解在大型集群上训练巨型模型时涉及的诸多复杂性。实际上，你可以同时使用多种不同的并行策略。到最后我会讲到一张写有"四维并行"的幻灯片，因为你可以同时做四件不同的事情——实际上甚至更多。想要在最大规模上实现并行，你需要使用所有这些策略或其中的大多数。你们作业的一部分就是，在给定的网络拓扑和模型下，找出最优的并行策略。

There are two bottlenecks that we solve by going to multiple machines and multiple GPUs. One is compute: we need more compute than we can bring to bear on a single chip. The way we solve that is to have many, many machines and link them up together. The other reason is memory: models are big, we can't fit them all into one GPU, so we need to shard them into smaller pieces. This leads to complexities of having many GPUs across many different machines.

我们通过使用多台机器和多个 GPU 来解决两个瓶颈。第一个是算力：我们需要比单个芯片能提供的更多的算力，解决方法就是拥有许多机器并将它们连接在一起。第二个原因是内存：模型很大，无法全部放入一个 GPU，所以我们需要将它们分片成小块。这就会导致跨多台机器使用多个 GPU 时的各种复杂性。

An important conceptual object is the difference between intra-node parallelism and inter-node parallelism. In intra-node, your connections are very fast, so you can do things that are very communication-expensive. In inter-node communication, connections are slower, so we have to use processes that respect the communication constraints of our channel more. We're going to deal with parallelism at the level of collective communication primitives—all-reduce, all-gather, reduce-scatter—rather than at the packet level. The equivalence between all-reduce and reduce-scatter plus all-gather will be important for one algorithm we'll discuss.

一个重要的概念性区分是节点内并行与节点间并行的区别。节点内连接非常快，因此你可以进行通信开销很大的操作。节点间通信则较慢，因此我们必须更多考虑信道的通信约束。我们将在集体通信原语（collective communication primitives）的层面上处理并行问题——如全归约（all-reduce）、全收集（all-gather）、分散规约（reduce-scatter）——而不是在数据包层面。一个重要的等价关系是：全归约等价于分散规约加全收集。这个等价关系对我们稍后要讨论的某个算法至关重要。

## 2. Hardware Landscape / 二、硬件格局

Most of our discussion today will be hardware agnostic. But I do want to briefly talk about the low-level hardware stack, because it leads to different parallelization strategies across different model training companies. The TPU, Google's accelerator, uses a toroidal mesh network — you can think of it as a grid where the ends wrap around and communicate with each other. All the chips are networked to neighbors, and the neighbors wrap around. This lets you have a very simple networking topology that can be indefinitely scaled up — the number of neighbors you have is the same no matter how large your network gets.

虽然我们今天大部分讨论是硬件无关的，但我还是想简要谈谈底层硬件栈，因为这会导致不同模型训练公司采用不同的并行策略。TPU 是 Google 的加速器，它使用环形网格网络——你可以将其想象成一个网格，网格的两端环绕连接、互相通信。所有芯片都与邻居连接，邻居之间相互环绕。这让你拥有一个非常简单的网络拓扑，可以无限扩展——无论网络规模多大，邻居的数量始终不变。

In contrast, the GPU networking philosophy is very different. It's much more of an all-to-all philosophy, networked like a fat tree. GPUs are connected very quickly at the lowest layers, then groups of GPUs are connected in a pod, and pods have spine switches that allow them to communicate with each other. This means that as the number of nodes grows, the tree gets bigger and bigger, and communication costs get higher. If you're communicating only to neighbors, TPUs are great and cost-effective. But if you're connecting in very random, unpredictable ways, GPU networking is more flexible. This difference in design philosophy between TPUs and GPUs will show up as we go through the parallelism lecture.

相比之下，GPU 的网络哲学非常不同，它更像是一种全对全（all-to-all）的哲学，网络结构像一棵"胖树"（fat tree）。GPU 在最底层以极快的速度互连，然后一组 GPU 组成一个 pod，pod 之间通过主干交换机（spine switches）相互通信。这意味着随着节点数量增长，树会越来越大，通信成本会越来越高。如果你只与邻居通信，TPU 非常出色且具有成本效益；但如果你的通信模式非常随机、不可预测，那么 GPU 网络会更灵活。TPU 和 GPU 之间这种不同的设计哲学将贯穿我们整个并行课程。

Interestingly, earlier this morning Google announced the TPU8i and TPU8t. The TPU8i has a tree topology — they've switched to a much more all-to-all connection. If you think about it, it makes sense: modern language models are MoEs, and if you're serving a MoE, you'll have bandwidth flying around as you route tokens to different experts. You probably do want much more all-to-all connectivity. Even the TPU8t, which is a training chip, has cross-rack connectivity that looks a lot more like a GPU. There's convergent evolution across both TPUs and GPUs, where the workloads are defining the network we need to have.

有趣的是，今天早上 Google 刚刚发布了 TPU8i 和 TPU8t。TPU8i 采用了树形拓扑——他们切换到了更加全对全的连接方式。仔细想想，这很合理：现代语言模型是混合专家（MoE）模型，服务 MoE 时，当你将 token 路由到不同专家时带宽需求非常大，你确实需要更多全对全连接。即便是用于训练的 TPU8t，其跨机架连接看起来也更像 GPU 了。TPU 和 GPU 之间正在发生一种趋同演化，工作负载正在定义我们需要的网络。

As another example of hardware tradeoffs, consider the Huawei Ascend 910. Each chip is a lot worse than an H200 — slower at matmuls, slower in many ways. But if you're willing to dedicate a giant rack of fiber optic switches to connect a much larger number of chips (384 in a big rack), then maybe you can deal with the fact that each chip is slower by just connecting many more of them. However, the power consumption is insanely high — four times that of the equivalent NVIDIA system. If you're willing to pay the power cost, you can solve a lot of communication problems by brute force and scale out much more aggressively.

作为另一个硬件设计权衡的例子，看看华为 Ascend 910。每个芯片的性能远不如 H200——矩阵乘法更慢，很多方面都更慢。但如果你愿意使用大量光纤交换机组装巨型机架来连接更多的芯片（一个大型机架中可达 384 个），那么也许可以通过连接更多的芯片来弥补单芯片性能的不足。然而，功耗高得惊人——是同等 NVIDIA 系统的四倍。如果你愿意承担功耗成本，就可以通过"蛮力"方式解决许多通信问题并实现更激进的扩展。

The new unit of compute is not the GPU — it's the entire data center. We want to be able to control the amount of memory we use, the amount of compute we can bring to bear, and we want all of these to be lossless — using all the resources we have.

新的计算单元不再是单个 GPU，而是整个数据中心。我们需要能够控制内存使用量、控制可以调动的算力，并且要让这些资源都"无损"——充分利用我们拥有的所有资源。

## 3. Data Parallelism / 三、数据并行

Data parallelism is conceptually very simple. Forget Adam for a moment — let's do just naive SGD. Each update step, we take a batch of size B, sum up the gradients, and take an update. The most naive form of parallelism is to cut the batch B across M machines. Each machine gets a smaller B/M sized batch, computes gradients, and then we synchronize all the gradients to get the sum. For compute scaling, this is perfect — as long as there are enough examples per GPU, we're good. But for memory scaling, there is absolutely none: every GPU has the same copies of the models, and you don't save any memory at all.

数据并行在概念上非常简单。先忘掉 Adam，假设我们用最简单的 SGD。每个更新步骤中，我们取一个大小为 B 的批次，把梯度加起来，然后进行更新。最原始的并行方式是将批次 B 分到 M 台机器上，每台机器得到一个较小的 B/M 大小的批次，各自计算梯度，然后同步所有梯度得到总和。在算力扩展方面，这很完美——只要每个 GPU 有足够的样本就可以。但在内存扩展方面，完全没有任何节省：每个 GPU 都有模型的完整副本，不节省任何内存。

### 3.1 The Memory Problem / 内存问题

The memory situation is not just bad — it's terrible. Roughly, the rule of thumb is that we need something like five copies of weights and 16 bytes per parameter to store our model. We need to store model parameters, gradients, and optimizer state. If you're doing Adam, you need to track both the first and second moments of your gradients over time. We call these things optimizer state — the first moment, the second moment. If you look at the accounting, this is most of the memory cost of doing an SGD update. The optimizer state is most of your memory, followed by gradients, then parameters. Parameters and gradients are the same size, and your optimizer state is bigger.

内存状况不仅糟糕，而且非常糟糕。粗略的经验法则是，每个参数我们需要存储大约五份权重拷贝，每个参数约 16 字节。我们需要存储模型参数、梯度和优化器状态。如果使用 Adam，还需要随时间跟踪梯度的一阶矩和二阶矩。我们称之为优化器状态——一阶矩、二阶矩。从账面上看，这是 SGD 更新中内存开销的大部分。优化器状态占用了大部分内存，其次是梯度，然后是参数。参数和梯度大小相同，而优化器状态更大。

If you do naive data parallel, you replicate all of this state across GPUs. Your memory consumption is linear with your number of accelerators — not good. What we can do instead is shard the optimizer state onto different GPUs, shard the gradients, or in the extreme, shard everything into different accelerators. The implied memory gains would be quite dramatic — from 120 down to 1.9 in memory per GPU. The main thing we'll study is: what is the cost of doing this? Baseline is the fastest, and as we shard more, we might have to pay a big communication cost to achieve these memory savings. The remarkable thing is that a lot of this will be free.

如果做最简单的数据并行，你会在所有 GPU 上复制所有这些状态。内存消耗与加速器数量成线性关系——这不好。我们可以做的是将优化器状态分片到不同 GPU 上，将梯度分片，或者在极端情况下，将所有内容分片到不同加速器上。这样带来的内存节省非常显著——每个 GPU 的内存从 120 降至 1.9。我们需要研究的主要问题是：这样做的代价是什么？基线方案最快，随着分片程度增加，可能需要付出很大的通信代价来换取这些内存节省。但令人惊讶的是，其中很多代价实际上是免费的。

### 3.2 ZeRO Stage 1: Shard Optimizer State / ZeRO 第一阶段：分片优化器状态

In ZeRO stage 1, the only thing we shard is the optimizer state across GPUs. Everyone has both the parameters and the gradients. Each worker is responsible for updating one slice of the parameter. Everyone computes a full gradient on their data item. Then we reduce-scatter the gradients onto all the other machines — each worker receives only the gradient portion associated with their parameter slice. Each machine then does its update using its parameters, the gradients it received, and its own tracked state. Finally, we all-gather the updated parameters back. This is where the equivalence is useful: in naive data parallel, we do one all-reduce (cost of 2 times parameters). In ZeRO stage 1, we did a reduce-scatter and an all-gather, which is equivalent to an all-reduce. So ZeRO stage 1 has the exact same communication characteristics as naive DDP. This was free — free memory savings!

在 ZeRO 第一阶段，我们只将优化器状态分片到 GPU 上。每个人都同时拥有参数和梯度。每个 worker 负责更新参数的一个切片。每个人在自己的数据项上计算完整梯度，然后通过分散规约（reduce-scatter）将梯度发送到其他机器——每个 worker 只接收与其参数切片相关的梯度部分。然后每台机器使用自己的参数、收到的梯度以及自己跟踪的状态进行更新。最后，通过全收集（all-gather）将更新后的参数传回。这就是等价关系派上用场的地方：在最简单的数据并行中，我们需要一次全归约（all-reduce），成本为 2 倍参数。在 ZeRO 第一阶段中，我们做了一次分散规约和一次全收集，这等价于一次全归约。所以 ZeRO 第一阶段的通信特性与最简单的数据并行完全相同——这是免费的，免费的内存节省！

### 3.3 ZeRO Stage 2: Shard Gradients / ZeRO 第二阶段：分片梯度

ZeRO stage 2 splits the gradients up and shards them as well. This is trickier because before we could compute the entire gradient, and now we can't even materialize the whole gradient. The key step is: instead of materializing the gradient vector all at once, we walk backwards through the compute graph, and after computing a layer's gradients, we immediately reduce and send them to the right worker. Once gradients aren't needed in the backwards graph, we immediately free them. We incrementally compute and send gradients as we go. Doing it incrementally or all at once is the same thing — it doesn't really make a difference. At the end, we once again all-gather the parameters without incurring any additional costs.

ZeRO 第二阶段将梯度也分片了。这更加棘手，因为之前我们可以计算整个梯度向量，而现在我们甚至无法一次性物化整个梯度。关键步骤是：我们不是一次性物化梯度向量，而是沿着计算图反向遍历，在计算完一层的梯度后，立即发送给对应的 worker。一旦梯度在反向计算图中不再需要，就立即释放。我们在反向过程中增量计算和发送梯度。增量计算和一次性计算本质上是一样的——没有什么区别。最后，再次全收集参数，而不会产生任何额外的开销。

### 3.4 ZeRO Stage 3 / FSDP: Shard Parameters as Well / ZeRO 第三阶段 / FSDP：也分片参数

ZeRO stage 3, also known as FSDP, shards parameters as well. The idea is to send and receive parameters on demand while stepping through the compute graph. Each GPU only sees a slice of the parameters, gradients, and optimizer states at any one time. Under the hood, you do two all-gathers and one reduce-scatter as you go. You load your model, gather weights for one layer, do the forward pass, then free those weights. For the backwards step, you all-gather the parameters for that layer on demand, do the backwards pass, reduce-scatter the gradients out, free the weights, and repeat.

ZeRO 第三阶段，也称为全分片数据并行（FSDP），连参数也一并分片。核心思想是在按层遍历计算图时按需发送和接收参数。每个 GPU 在任何时刻只能看到参数、梯度和优化器状态的一个切片。底层实现中，你需要做两次全收集（all-gather）和一次分散规约（reduce-scatter）。你加载模型，收集某一层的权重，执行前向传播，然后释放这些权重。对于反向传播步骤，你按需全收集该层的参数，执行反向传播，将梯度分散规约出去，释放权重，然后重复此过程。

FSDP uses two really important ideas to make this essentially overhead-free. The first is sweeeping through the compute graph, doing necessary communication, and immediately freeing memory. The second is overlapping communication and computation. As you all-gather layer 0's parameters and do forward 0, you simultaneously request and all-gather layer 1's parameters. While doing computation, you're also doing communication for the next layer. If you have enough computation and your network is fast enough, FSDP can basically be free. In practice, FSDP achieves GPU utilization very close to single-GPU performance. It's actually quite remarkable how good FSDP is.

FSDP 利用两个非常重要的思想使其基本上零开销。第一是沿着计算图顺序遍历，进行必要的通信后立即释放内存。第二是通信与计算重叠。当你在全收集第 0 层的参数并执行 forward 0 时，同时请求并全收集第 1 层的参数。在进行计算的同时，也在进行下一层的通信。如果有足够的计算量且网络足够快，FSDP 基本上可以做到零开销。在实践中，FSDP 的 GPU 利用率非常接近单 GPU 性能，效果确实非常出色。

In terms of the different ZeRO stages: DDP (naive data parallel) costs 2 times parameters (a single all-reduce). ZeRO stages 1 and 2 are free in the literal sense — same amount of communication cost because of the all-reduce identity. ZeRO stage 3 technically has a little bit more communication (an extra all-gather), but it's not so bad because libraries can hide the communication cost underneath the computation. With ZeRO stage 3, you can fit much larger models — going from not even fitting a 7B model to fitting 50 billion parameter models on A100s.

就各 ZeRO 阶段的对比而言：DDP（最简单的数据并行）成本为 2 倍参数（一次全归约）。ZeRO 第一和第二阶段是真正意义上的免费——由于全归约的等价分解，通信成本完全相同。ZeRO 第三阶段在技术上有稍微多一点点的通信（多一次全收集），但由于库可以将通信成本隐藏在计算之下，实际影响不大。使用 ZeRO 第三阶段，你可以容纳更大的模型——在 A100 上从连 7B 模型都放不下，到能放下 500 亿参数的模型。

## 4. The Limits of Data Parallelism / 四、数据并行的局限

Data parallel consumes an important resource: the batch size. If you have a batch size of 8, you can never have more than eight accelerators. You might think you can just make the batch size bigger, but there's something called the critical batch size — the point where the gain from an additional batch element is less than if you had taken another SGD step on a single element. At small batch sizes, adding extra elements is perfectly helpful, but at a certain point, diminishing returns hit. Because of this, we face a hard tradeoff: do we want small batch sizes and more idle GPUs, or big batch sizes and take the hit from optimization?

数据并行消耗一个重要资源：批次大小（batch size）。如果 batch size 为 8，你最多只能有 8 个加速器。你可能会想不断增大 batch size 来容纳更多加速器，但存在一个临界批次大小的概念——超过这个点，额外 batch 元素带来的增益小于对单个元素多做一步 SGD 的增益。在小 batch size 下，增加额外元素是有益的，但到了一定程度就会出现边际递减。因此我们面临一个艰难的权衡：是要小 batch size、让 GPU 更空闲，还是要大 batch size 但承受优化上的损失？

Another issue is that ZeRO stages 1 and 2 don't let you scale memory at all, and ZeRO stage 3 lets you cut up parameter memory but doesn't help with activation memory. We need better, more fine-grained ways of cutting up the model to push down memory use beyond these points. This takes us to various model parallelism ideas.

另一个问题是 ZeRO 第一和第二阶段根本不能扩展内存，而 ZeRO 第三阶段虽然可以减少参数内存，但对激活值（activation）内存没有帮助。我们需要更好、更细粒度的方法来切分模型，从而进一步降低内存使用。这就引导我们进入各种模型并行的方法。

## 5. Model Parallelism / 五、模型并行

The important conceptual difference between data parallelism and model parallelism is that now we are going to communicate activations. In FSDP, we cut up parameters but still did the normal computation — parameters were the things flying around. Now we're going to communicate activations back and forth. If one layer lives on GPU 0 and the next on GPU 1, what you communicate is the activation of the layer in between. This involves pipeline parallel (cutting up layers), tensor parallel (cutting up matrices), and expert parallel (sharding experts into different places).

数据并行和模型并行之间的关键概念区别在于：在模型并行中，我们通信的是激活值。在 FSDP 中，我们分片了参数，但仍然执行正常的计算——来回传输的是参数。而现在我们要来回通信的是激活值。如果一层在 GPU 0 上，下一层在 GPU 1 上，那么你需要通信的是两层之间的激活值。这涉及流水线并行（切分层）、张量并行（切分矩阵）和专家并行（将专家分片到不同位置）。

### 5.1 Pipeline Parallel / 流水线并行

Pipeline parallel is conceptually simple: cut up the layers and put them on different GPUs. You pass activations forward in the forward pass and partial gradients backward in the backward pass. But if you simply do this naively, you get a terrible picture — most of the time, your GPUs are idle. One GPU will be active at a time, and your utilization is truly terrible. This idle time is called a "bubble."

流水线并行在概念上很简单：将层切分并放到不同的 GPU 上。前向传播时传递激活值，反向传播时传递部分梯度。但如果只是简单地这样做，结果会非常糟糕——大部分时间 GPU 都是空闲的，同一时间只有一个 GPU 在工作，利用率极低。这段空闲时间被称为"气泡"（bubble）。

The solution is to do batching or pipelining: instead of processing one element at a time, you have a pipeline where you process multiple elements (micro-batches). As soon as you process one element, you start on the next and pass the completed one to the next layer. The utilization is roughly the number of stages divided by the number of micro-batches. To reduce the bubble toward zero, you need a huge batch size. This is why batch sizes are a useful resource — you can spend them on pipelining to reduce idle time in pipeline parallel.

解决方案是进行批处理或流水线化：不是一次处理一个元素，而是构建一个流水线，一次处理多个元素（微批次，micro-batches）。一旦处理完一个元素，立即开始下一个，并将已完成的结果传递给下一层。利用率大致等于流水线级数除以微批次数量。为了将气泡减小到接近零，你需要非常大的 batch size。这就是为什么 batch size 是一种有用的资源——你可以将 batch size 用于流水线化以减少空闲时间。

Pipelines can save memory compared to DDP because we've cut up layers. You can also compose this with data parallel. But the key advantage is that pipelines have very good communication properties — they only depend on activations (batch × sequence length × hidden), and communication is point-to-point, not all-to-all. Because of this, pipelines are typically placed on the slowest networking links. If you have multiple data centers or multiple pods with slower connections, you parallelize across them using pipeline parallel.

与 DDP 相比，流水线可以节省内存，因为我们切分了层，而且可以与数据并行组合使用。但关键优势在于流水线具有非常良好的通信特性——它只依赖激活值（batch × sequence length × hidden），且通信是点对点（point-to-point）而不是全对全（all-to-all）的。因此，流水线通常会被放在最慢的网络链路上。如果你有多个数据中心或多个 pod 之间通信较慢，就在它们之间使用流水线并行。

People have developed clever scheduling strategies to further reduce the bubble size. For example, DeepSeek's approach sequences forward and backward computation cleverly to get a little better bubble reduction. Even more clever is "zero bubble pipelining," which separates the two things that happen in the backward pass: propagating partial derivatives backward (B, which is critical because the next stage can't work without it), and computing the derivative with respect to the weights (W, which can be deferred). The B's come first as quickly as possible, and the W's fill in gaps in the computation. This can almost completely fill up the pipeline.

人们开发了巧妙的调度策略来进一步减小气泡。例如 DeepSeek 的方法通过巧妙安排前向和反向计算顺序来稍微改善气泡。更巧妙的是"零气泡流水线"（zero bubble pipelining），它将反向传播的两个操作分开：向后传播偏导数（B 操作，至关重要，因为下一阶段必须等待这个信号）和计算参数梯度（W 操作，可以推迟）。B 操作尽可能快地执行，W 操作填补计算间隙。这几乎可以完全填充流水线。

### 5.2 Tensor Parallel / 张量并行

If pipeline parallel is cutting along the depth axis, tensor parallel cuts along the width axis. It's the simple idea that matrix multiplies can be cut into smaller matrix multiplies, and then you add the partial sums back together. In the forward pass, the input x is copied (identity function f), and then at the end of the parallel component, an all-reduce (g function) brings results back together. In the backward pass, this flips: g becomes identity, and f becomes the all-reduce that sums partials to get the derivatives at the start of the module. This duality is important for implementing tensor parallel.

如果说流水线并行是沿着深度维度切分，那么张量并行就是沿着宽度维度切分。核心思想很简单：矩阵乘法可以切分成更小的矩阵乘法，然后再将部分和加回来。在前向传播中，输入 x 被复制（恒等函数 f），在并行组件的末尾，全归约（g 函数）将结果聚合在一起。在反向传播中，角色互换：g 变为恒等，f 变为全归约，将偏导数求和得到模块起始处的导数。这种对偶性对于实现张量并行非常重要。

There are column-wise cuts (at the inputs — MLP projections, attention projections in each transformer block) and row-wise cuts (in the corresponding second stage — MLP down-projections, attention outputs). Small layers like layer norm, non-linearity, or routers in MoEs are fully replicated — you don't want to bother with the overhead of cutting them.

有列切分（在输入端——MLP 投影、每个 transformer 块中的注意力投影）和行切分（在对应的第二阶段——MLP 下投影、注意力输出）。小层如层归一化（layer norm）、非线性激活或 MoE 中的路由器则完全复制——不值得为切分它们而增加开销。

Tensor parallel is extremely communication-hungry. Every time you have a matmul, you're doing some all-reduce communication, and these are activation-sized and happen very frequently. So you only want to do tensor parallel within a node. For GPUs (up to 8 in a single box), you might use tensor parallel within NVLink. Once you go cross-node, those connections are much slower, and you'll get a big drop in performance. For TPUs, there isn't this sharp distinction — you have a big toroidal mesh, so you can tensor parallel over much larger numbers with high bandwidth in regular communication patterns. The amount of tensor parallelism versus pipeline parallel will be quite different between TPUs and GPUs.

张量并行非常消耗通信带宽。每次矩阵乘法都伴随着全归约通信，通信量与激活值大小成正比且非常频繁。因此你只想在节点内部使用张量并行。对于 GPU（单个盒子中最多 8 个），可以在 NVLink 范围内使用张量并行。一旦跨越节点，连接就会慢很多，性能会大幅下降。对于 TPU，没有这种明显的区分——你有一个巨大的环形网格，可以在有规律通信模式下以高带宽在更多芯片上做张量并行。在 TPU 和 GPU 之间，张量并行与流水线并行的比例会有很大不同。

Comparing tensor parallel and pipeline parallel: both save on parameters and potentially activations. Tensor parallel has no pipeline bubble, and if your network is fast enough, you can get full utilization — it's also low complexity, just cutting up matmuls. But the con is much larger communication (all-to-all all-reduce, not just point-to-point). Tensor parallel is great when you have high-speed interconnects; every other time, you probably want pipeline parallel.

比较张量并行和流水线并行：两者都能节省参数和（潜在的）激活值。张量并行没有流水线气泡，如果网络足够快，可以获得完全利用率——复杂度也低，只是切分矩阵乘法。但缺点是通信量大得多（全归约是全对全的，而不仅仅是点对点的）。有高速互连时用张量并行很好；其他时候，你可能更想用流水线并行。

### 5.3 Activation Memory / 激活值内存

The most naive view of memory is that it's just parameters. But if you profile actual memory use, there's a lot of dynamic memory — you need to store all the activations (the big red bumps). Maximum memory usage happens a little bit after the maximum activation point, after you start sweeping backwards but still need activations. As models get bigger, for moderately large sequence lengths, activations dwarf the parameter memory. Any memory saving strategy must reason about activations to be fully effective.

最朴素的看法是内存只包括参数。但如果你用 profiler 分析实际内存使用，会发现有大量动态内存——你需要存储所有激活值（那些大的红色凸起）。最大内存使用点出现在最大激活点之后稍晚的位置，此时你已经开始反向遍历但仍需要保留激活值。随着模型增大，对于中等长度的序列，激活值内存将远远超过参数内存。任何内存节省策略都必须考虑激活值才能有效。

If we store everything, the amount of activations needed is roughly 34 × s × b × h plus a quadratic attention term (5 × a × s / h), where s is sequence length, b is batch size, h is hidden dimension, and a is attention heads. The sbh dependence is fundamental. This quadratic attention term can be dropped via recomputation with flash attention.

如果我们存储一切，所需的激活值量大致为 34 × s × b × h 加上二次注意力项（5 × a × s / h），其中 s 是序列长度，b 是 batch size，h 是隐藏维度，a 是注意力头数。sbh 依赖是根本性的。这个二次注意力项可以通过使用 flash attention 的重计算方法消除。

### 5.4 Sequence Parallel / 序列并行

Tensor parallel splits the matrix multiplies in attention and MLPs, which accounts for 24 of those 34 sbh terms and the quadratic attention term. You can divide those by your tensor parallel size t. But layer norms, dropouts, and inputs to attention and MLP (which need to be stored as residuals for the backward pass) are not reduced by tensor parallel size. You still suffer a 10 × sbh penalty. Sequence parallel addresses this by splitting these remaining lightweight operations over the sequence axis rather than the hidden axis, using all-gathers and reduce-scatters before every operation. Conceptually, it's very similar to FSDP — storing in a sharded format and gathering on demand.

张量并行可以切分注意力中的矩阵乘法和 MLP 部分的矩阵乘法，这涵盖了 34 个 sbh 项中的 24 个以及二次注意力项，你可以用张量并行大小 t 来除这些项。但层归一化、dropout 以及注意力和 MLP 的输入（需要作为残差保留给反向传播）不会被张量并行切分。你仍将承受 10 × sbh 的惩罚。序列并行通过将剩余的这些轻量操作沿着序列轴（而非隐藏轴）切分来解决这个问题，在每次需要这些激活值的操作前使用全收集和分散规约。概念上，这与 FSDP 非常相似——以分片形式存储，按需收集。

With full combination of tensor parallel and sequence parallel, we get activation memory of roughly 34 × sbh / t. With activation recomputation, we drop the quadratic attention term to get sbh × 34 / t. This is a good lower bound to remember for whether your model will fit into a GPU.

通过张量并行和序列并行的完整组合，激活值内存大约为 34 × sbh / t。加上激活值重计算，可以消除二次注意力项，得到 sbh × 34 / t。这是一个很好的下界，可以用来判断你的模型是否能放进 GPU。

### 5.5 Expert Parallel / 专家并行

With MoEs now standard, expert parallelism takes advantage of splitting the FFN/MLP components across different devices. Expert parallel is analogous to tensor parallel — high bandwidth, reduces activation — but for MoEs, you almost always prefer expert parallel over tensor parallel. The reasons: if you cut up a matrix too finely, matrices get small and GPU utilization suffers; for MoE layers, it's a lot easier to route sparse token activations; you can skip computation overhead if MoE is already doing routing.

随着 MoE 成为标配，专家并行利用了将 FFN/MLP 组件分散到不同设备上的做法。专家并行在概念上类似于张量并行——高带宽、减少激活值——但对于 MoE，你几乎总是更倾向于专家并行而非张量并行。原因有：如果将矩阵切得过于细碎，矩阵会变小，GPU 利用率会下降；对于 MoE 层，路由稀疏 token 激活比路由密集的张量并行矩阵乘法激活容易得多；既然 MoE 已经在做路由了，就可以顺便利用。

However, expert parallel is still very complicated. DeepSeek's DPP library and NVIDIA's Hybrid EP library both look at really low-level GPU networking primitives to make MoE routing as efficient as possible. The reason this is hard: every time you have an MLP, you route tokens to different places in an all-to-all communication pattern, and the computation is waiting for tokens to arrive — latency of this dispatch is critical. As a fun trivia: to squeeze out every last bit of performance, DeepSeek found and used undocumented PTX instructions (GPU machine code) to further accelerate their networking communication. That's the level needed to get to the frontier of parallelism efficiency.

然而，专家并行仍然非常复杂。DeepSeek 的 DPP 库和 NVIDIA 的 Hybrid EP 库都在研究非常底层的 GPU 网络原语，以使 MoE 路由尽可能高效。这之所以困难，是因为每次 MLP 操作都需要在全对全通信模式下将 token 路由到不同位置，而计算在等待 token 到达——调度的延迟至关重要。一个有趣的轶事：为了从每一丝性能中榨取最后的提升，DeepSeek 发现并使用了文档未记录的 PTX 指令（GPU 机器码级别的东西）来进一步加速网络通信。这就是达到并行效率前沿所需的水平。

An important constraint: in old libraries, the replicas for DP and EP are the same — the GPUs are split according to DP, and EP is a subset. This constrains how far you can parallelize with EP. Modern solutions decouple tensor parallel in MLPs and attention: attention layers get one kind of tensor parallel, and MoE layers get another. This leads to more complicated but more effective combinations.

一个重要的约束：在旧库中，DP 和 EP 的副本是相同的——GPU 按 DP 划分，EP 是该划分的子集，这限制了 EP 的并行规模。现代解决方案将 MLP 和注意力中的张量并行解耦：注意力层使用一种张量并行配置，MoE 层使用另一种。这导致了更复杂但更高效的组合。

### 5.6 Context Parallel / 上下文并行

Context parallel (or ring attention) splits activations of a very long sequence across different accelerators, passing activations to the needed device in a ring-like way following the mesh topology of TPUs. It's used in long context extension stages and in model serving. It overlaps conceptually with much of what we've already covered.

上下文并行（或环形注意力）将超长序列的激活值分散到不同加速器上，按照 TPU 的网格拓扑以环形方式将激活值传递给需要的设备。它用于长上下文扩展阶段和模型服务中。概念上与我们已经讨论过的大部分内容有很大重叠。

## 6. Putting It All Together: 4D Parallelism / 六、综合运用：四维并行

There is no one strictly dominant parallelization strategy — it's all tradeoffs. FSDP is great but doesn't help with activation and consumes your global batch size. Tensor parallel cuts down activation memory and doesn't touch global batch size, but needs fast networking and high bandwidth. Pipeline parallel leverages slower connections well but has bubbles and needs large batch sizes. You see how all these different advantages mean each strategy has a place, and in many large-scale architectures, you use a large combination of them.

没有一种并行策略能严格占优——全都是权衡。FSDP 很好，但无助于激活值内存，且消耗全局 batch size。张量并行可以减少激活值内存且不影响全局 batch size，但需要快速网络和高带宽。流水线并行能充分利用较慢的连接，但有气泡问题且需要大 batch size。你可以看到，所有这些不同的优势意味着每种策略都有用武之地，在许多大规模架构中，你需要将它们大量组合使用。

You can do some math: how much compute per layer for different sharding strategies, how much communication per layer, and how these scale. If compute time is longer than communication time, in principle you can hide communication underneath computation. Plots show that with large batch sizes, FSDP alone works great. As batch size goes down, FSDP becomes communication-bound, so you incorporate tensor parallel (MP) to push the curve out and stay compute-bound even into smaller batch size regimes. You keep adding strategies to push this curve out. This is what people call 3D or 4D parallelism — putting all strategies together to keep compute units fully utilized under different communication topologies.

你可以做一些数学计算：不同分片策略下每层需要多少计算、每层需要多少通信，以及它们如何扩展。如果计算时间大于通信时间，原则上你可以将通信隐藏在计算之下。图表显示，在大 batch size 下，单独的 FSDP 效果很好。随着 batch size 减小，FSDP 会变得通信受限，这时你加入张量并行来将曲线外推，使得在更小 batch size 区间仍能保持计算受限。你不断添加策略来将曲线继续外推。这就是人们所说的三维或四维并行——将所有策略组合起来，在不同通信拓扑下保持计算单元完全利用。

### 6.1 Simple Prescription / 简单的实践处方

The practical strategy is very simple. Until your model fits into memory, cut up your model by whatever means necessary: use tensor or expert parallel for your fast interconnect (e.g., up to 8 GPUs per machine), then pipeline parallel or FSDP (ZeRO-3) for the rest. Once your model fits, data parallel the rest of the way. If your batch size ends up too small, use gradient accumulation. This is borne out in Megatron's guidelines: (1) minimize model parallelism, maximize data parallelism; (2) stay within NVLink for GPUs (one box); (3) keep expert and tensor parallel within one box; (4) use pipeline parallelism for multi-node; (5) if MoE, prefer expert parallel; (6) if long sequences, use context parallel (ring attention).

实践策略非常简单。在模型能放进内存之前，用一切必要手段切分模型：在快速互连上使用张量或专家并行（如每台机器最多 8 个 GPU），其余使用流水线并行或 FSDP（ZeRO-3）。一旦模型能放下，其余就全部用数据并行。如果 batch size 变得太小，使用梯度累积。Megatron 的指南证实了这一点：（1）最小化模型并行，最大化数据并行；（2）GPU 保持在 NVLink 范围内（一个盒子）；（3）专家并行和张量并行保持在一个盒子内；（4）跨节点使用流水线并行；（5）如果是 MoE，优先使用专家并行；（6）如果需要长序列，使用上下文并行（环形注意力）。

A paper by NVIDIA demonstrated this with quantitative evidence: as you scale up, data parallel is maxed out, tensor parallel increases until it hits 8 and then stops, and pipeline parallel increases. Even at ludicrously large numbers of GPUs, utilization stays very flat and very good. There's also counterintuitive evidence that you should do more activation recomputation — because it saves memory, and memory can be turned into larger batch size, leading to better utilization.

NVIDIA 的一篇论文用定量证据展示了这一点：随着规模扩大，数据并行被最大程度使用，张量并行增加到 8 后停止，流水线并行不断增加。即使在数量极其庞大的 GPU 规模下，利用率仍然非常平坦且优秀。还有一个反直觉的发现：你应该做更多的激活值重计算——因为它节省内存，内存可以转化为更大的 batch size，从而提高利用率。

## 7. Real-World Training Runs / 七、真实训练案例

**Olmo (AI2)**: A 7B model trained fully with FSDP across many accelerators. FSDP scales surprisingly well, even to many GPUs, especially for small models. Many 7B-ish models are trained purely with FSDP.

**Olmo（AI2）**：一个 7B 模型，完全使用 FSDP 在大量加速器上训练。FSDP 扩展能力惊人，即使对大量 GPU 也适用，尤其对于小模型。很多 7B 级别的模型都纯粹使用 FSDP 训练。

**DeepSeek V1**: Data parallel with ZeRO stage 1, tensor parallel, sequence parallel, and pipeline parallel. **DeepSeek V3** (MoE): pipeline parallel plus expert parallel instead of tensor parallel, with 64-way expert parallelism grouping 8 machines together, using pipelining tricks to keep expert parallel utilization high.

**DeepSeek V1**：数据并行（ZeRO 第一阶段）+ 张量并行 + 序列并行 + 流水线并行。**DeepSeek V3**（MoE）：流水线并行 + 专家并行（代替张量并行），64 路专家并行，将 8 台机器组合在一起，使用流水线技巧保持专家并行的高利用率。

**Yi**: ZeRO stage 1, tensor parallel, and pipeline parallel — the classic data + tensor + pipeline combo. Once going to MoEs, tensor parallelism is replaced with expert parallelism.

**Yi**：ZeRO 第一阶段 + 张量并行 + 流水线并行——经典的数据并行、张量并行、流水线并行组合。一旦转到 MoE，张量并行就被替换为专家并行。

**Llama3 405B** (dense model): Tensor parallel of 8, context parallel of 1, pipeline parallel of 16, and data parallel of 128 in the main pre-training phase. For long context extension, context parallel is cranked up and data parallel lowered. During training, GPUs failed 148 times — redundancy and distributed systems challenges are important too.

**Llama3 405B**（密集模型）：主预训练阶段张量并行 8，上下文并行 1，流水线并行 16，数据并行 128。长上下文扩展阶段，上下文并行调高，数据并行降低。训练过程中 GPU 故障了 148 次——冗余和分布式系统挑战同样重要。

**Gamma 2 (Google)**: FSDP plus tensor parallel and sequence parallel only — no pipeline parallel. This is a realization of the Google claim that for TPUs, you don't need pipelines; you just take a really big toroidal mesh and tensor parallel over it.

**Gamma 2（Google）**：仅 FSDP + 张量并行 + 序列并行——没有流水线并行。这体现了 Google 的主张：对于 TPU，不需要流水线，只需在巨大的环形网格上做张量并行。

**Mixtral 8x22B** (from Megatron Bridge): Expert parallel of 8, pipeline parallel of 4, and additional tensor parallel of 4 for attention layers. **Qwen 3**: Follows DeepSeek recipe — expert parallel of 32, pipeline parallel of 8, and tensor parallel of 2 for attention matrices.

**Mixtral 8x22B**（来自 Megatron Bridge）：专家并行 8，流水线并行 4，注意力层额外张量并行 4。**Qwen 3**：遵循 DeepSeek 配方——专家并行 32，流水线并行 8，注意力矩阵张量并行 2。

## 8. Conclusion / 八、总结

The common thread across all these models: use as much data parallel as possible. Tensor parallel almost always remains below 8. Expert parallel can sometimes be bigger now, partially because of DeepSeek V3 and the infra built for large-scale expert parallel training. The highest-level point is we need to think about multi-GPU, multi-node, maybe even multi-data center parallelism. To think about efficiency in that regime, we need to bring to bear all the approaches we have — fast links, slow links, techniques that make use of batch sizes and all these different resources. But given all of these, there are fairly simple rules of thumb for combining all these different forms of parallelism to get effectively full utilization of your compute hardware.

所有这些模型的共同主线是：尽可能多地使用数据并行。张量并行几乎始终保持在 8 以下。专家并行现在有时可以更大，部分归功于 DeepSeek V3 以及为大规模专家并行训练构建的基础设施。最高层次的要点是，我们需要思考多 GPU、多节点、甚至多数据中心的并行。要在这个条件下思考效率，我们需要调动所有方法——快速链路、慢速链路、利用 batch size 和各种资源的技术。但综合考虑所有条件，存在相当简单的经验法则来组合这些不同形式的并行，最终实现对计算硬件的有效完全利用。
