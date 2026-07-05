# Lecture 7: Parallelism / 第七讲：并行

## Introduction / 引言

Welcome back, everyone. So today we're going to talk about parallelism. Remember in the last week, we introduced how to make a single GPU go fast by writing kernels. We really looked inside this GPU. And this week, we're going to talk about how to leverage multiple GPUs to make your code go even faster.

欢迎回来，各位。今天我们来讲并行（parallelism）。回想一下，上周我们介绍了如何通过编写 kernel 让单个 GPU 跑得更快，我们深入观察了 GPU 内部。而本周，我们将讨论如何利用多个 GPU 让你的代码跑得更快。

---

So the picture you should have in your head is something like this. For the last week, we focused on one of these boxes, where you have your GPU—High Bandwidth Memory (HBM), L2 cache, L1 cache, registers, and a bunch of streaming multiprocessors. Now the picture gets extended, because instead of having one GPU, you might have four, you might have 1,000 GPUs. And those are going to be connected. And then you're going to have to figure out how to leverage all of this compute to train models.

你应该在脑海中形成的画面是这样的。上周我们聚焦于其中一个盒子，里面有你的 GPU——高带宽内存（HBM）、L2 缓存、L1 缓存、寄存器以及一堆流式多处理器。现在这个画面被扩展了，因为你不再只有一个 GPU，你可能有四个，也可能有一千个 GPU。它们会相互连接。然后你需要想办法利用所有这些计算资源来训练模型。

---

In both the single GPU case and the multi-GPU case, the situation is kind of similar if you zoom out: the compute (the ALUs, the tensor cores, and so on) is far away from your data. Far away for a single GPU means all the way over in HBM. And now if you have multi GPUs, the thing you need might be all the way on a different GPU, and you're going to have to shuffle that over somehow. But the same principles apply, because the game is to orchestrate the computation to try to avoid data transfer bottlenecks. It's very easy to use a ton of GPUs, but it's hard to use them effectively.

无论是在单 GPU 还是多 GPU 的情况下，如果从宏观来看，情况有些相似：计算单元（算术逻辑单元、张量核心等）离你的数据很遥远。对于单 GPU 而言，"遥远"意味着数据在 HBM 中。而对于多 GPU，你需要的数据可能位于完全不同的 GPU 上，你必须想办法把它搬过去。但同样的原则依然适用，因为关键是要协调计算以避免数据传输瓶颈。使用大量 GPU 很容易，但要高效利用它们却很困难。

---

We can think about the generalized hierarchy: at the local level next to the SMs, a single node single GPU, you have L1 cache / shared memory—this was the fastest. Then you had HBM, which we lamented was so slow. But in this lecture, HBM is going to be considered fast. Now we're going to think about the single-node multi-GPU setting where the GPUs are connected via NVLink and NVSwitch. And finally, the multi-node and multi-GPU setting, where we have to resort to InfiniBand and Ethernet depending on what network you have.

我们可以这样思考这个广义的层级结构：在局部层面，靠近 SM 的单节点单 GPU 场景中，你有 L1 缓存/共享内存——这是最快的。然后有 HBM，我们曾抱怨它太慢了。但在本讲中，HBM 将被视为快速的。接下来我们要考虑的是单节点多 GPU 场景，GPU 之间通过 NVLink 和 NVSwitch 连接。最后是多节点多 GPU 场景，我们必须依赖 InfiniBand 或以太网，取决于你有什么网络。

---

So last week, we talked about various tricks for reducing memory accesses: fusion and tiling. Read into shared memory, do as much as you can, and then write it back out. And this week, we're going to talk about how you can reduce the amount of communication across GPUs by replicating and sharding appropriately.

所以上周我们讨论了减少内存访问的各种技巧：融合（fusion）和分块（tiling）。读入共享内存，尽可能多地计算，然后再写回去。而本周，我们将讨论如何通过适当地复制和分片（sharding）来减少 GPU 之间的通信量。

---

## Why Multi-GPU? / 为什么需要多 GPU？

Why do you do multi-GPUs? The obvious answer is, well, you want to scale. But to put a finer point on it, there's really two reasons. One is that your parameters, activations, gradients, or optimizer state don't fit on the HBM memory of a single GPU. B200 has 192 gigabytes; if you're training a 1 trillion parameter model, that's not going to fit on a single GPU. The other reason is that even if your model could fit on a single GPU, you might want to leverage more GPUs by splitting everything up to train faster. So sometimes there will be decisions to be made because you could fit everything on GPUs, but if you spread it out, you're going to have to pay the communication bandwidth cost.

为什么要使用多 GPU？显而易见的答案是：你想扩展。但更精确地说，有两个原因。一是你的参数、激活值、梯度或优化器状态无法放入单个 GPU 的 HBM 内存中。B200 有 192 GB 内存；如果你在训练一个万亿参数模型，它无法放入单个 GPU。另一个原因是，即使你的模型能够放入单个 GPU，你也可能希望通过将一切拆分来利用更多 GPU 以加快训练。所以有时需要做出权衡——你可以把所有东西放在 GPU 上，但如果分散开，就必须支付通信带宽的代价。

---

## Lecture Overview / 本讲概览

This lecture is going to include two parts. One is we're going to learn about the building blocks of distributed communication and computation, starting with the programming model, talking a little bit about the hardware, and starting to implement things in PyTorch (which you're going to do on your assignment two). And then the second part is we're going to look at actual training. We're going to look at three types of parallelism: data parallelism, tensor parallelism, and pipeline parallelism. Each is going to cut up our model in different ways. We're going to do this for MLPs rather than the full transformer, but the core computation is going to be shown here.

本讲包含两个部分。第一部分我们将学习分布式通信和计算的基本构建块，从编程模型开始，稍微谈谈硬件，并开始在 PyTorch 中实现这些（这将是你们作业二的内容）。第二部分我们将审视实际的训练过程，考察三种并行类型：数据并行（data parallelism）、张量并行（tensor parallelism）和流水线并行（pipeline parallelism）。每种方式以不同的方式切分我们的模型。我们将以 MLP 而非完整的 transformer 为例来演示，但核心计算方式是一样的。

---

## Collective Operations / 集合操作

The first thing to talk about is these things called collective operations. Collective operations are primitives from distributed programming that go back to the '80s. The idea of parallel programming is very old—it wasn't invented for LLM training. And it's still the case that these primitives are the ones that we use today. Here, "collective" just means that you're specifying a general communication pattern or a template across multiple devices, rather than managing point-to-point how this GPU is going to communicate with another GPU. This is going to be much easier, and the system can do a lot more work for you. So this is a very tried-and-true interface for doing parallel programming.

首先要讨论的是一类称为集合操作（collective operations）的操作。集合操作是分布式编程中可追溯到 80 年代的原语。并行编程的思想非常古老——它不是为 LLM 训练而发明的。而时至今日，我们使用的仍然是这些原语。这里"集合"的意思是，你在指定一个跨多个设备的通用通信模式或模板，而不是逐个管理这个 GPU 如何与另一个 GPU 通信。这样做会简单得多，而且系统可以为你做更多工作。所以这是一个非常经过验证的并行编程接口。

---

### Terminology / 术语

The general setup is as follows. You have a bunch of ranks, where a rank corresponds to a particular device—in our case a GPU. It could be a TPU. The world size corresponds to the number of devices. There are several operations we're going to go through: broadcast, scatter, gather, reduce, all-gather, reduce-scatter, all-reduce, and all-to-all. Each of these operations specifies how a set of ranks or devices is going to transfer some amount of data (and possibly compute) to some other set of devices.

通用设置如下。你有一组 rank（进程编号），每个 rank 对应一个特定设备——在我们的场景中是 GPU，也可能是 TPU。world size 对应设备数量。我们将介绍若干操作：广播（broadcast）、散射（scatter）、收集（gather）、归约（reduce）、全收集（all-gather）、归约-散射（reduce-scatter）、全归约（all-reduce）以及全集散（all-to-all）。每个操作都指定了一组 rank 或设备如何将一定量的数据（及可能伴随的计算）传输到另一组设备。

---

### Broadcast, Scatter, Gather, Reduce (Warm-ups) / 广播、散射、收集、归约（热身）

The first three—broadcast, scatter, gather, reduce—are really just warm-ups. They allow you to get a sense of how these collective operations work, but they're not really going to be the ones driving most of training.

前三个——broadcast、scatter、gather、reduce——实际上只是热身。它们让你了解这些集合操作如何工作，但它们并不是驱动大部分训练的核心操作。

---

In broadcasting, you have a rank 0 (it could be any rank) with some tensor, and it broadcasts it to all the ranks. At the end of this operation, each of the ranks has the same tensor on it. Broadcasts are generally used for initialization—let's say you initialize or load a checkpoint and then broadcast it to all the ranks. It's something done once.

在广播（broadcast）中，rank 0（也可以是任意 rank）持有某个张量，并将其广播到所有 rank。操作结束时，每个 rank 都拥有相同的张量。广播通常用于初始化——比如你初始化或加载一个 checkpoint，然后将其广播到所有 rank。这是一次性的操作。

---

A scatter basically says: I have a tensor at rank 0 that is split up into world-size pieces, and I'm going to scatter my tensor onto the other ranks. Rank 0 gets the zeroth component, rank 1 gets the next, and so on. Again, this is not directly used, but scatter is an important stepping stone to understand reduce-scatter. Scatter just takes a big tensor at one place and spreads it out onto multiple places. You can see how this might be helpful, because you want all the GPUs you're scattering to do some local computation on the different parts.

散射（scatter）基本是说：我在 rank 0 有一个张量，被分成 world size 份，我将这个张量散射到各个 rank 上。rank 0 得到第 0 份，rank 1 得到第 1 份，以此类推。同样，这并不直接使用，但 scatter 是理解 reduce-scatter 的重要基石。Scatter 就是把一个大张量从一个地方分散到多个地方。你可以看出这为什么有用，因为你希望各个 GPU 在不同部分上进行一些本地计算。

---

The inverse of scatter is gather. The input is a bunch of pieces, each residing on a particular rank. And when you do a gather with respect to a particular rank (say rank 0), it concatenates all the pieces together. Gather isn't directly used, but it's a stepping stone to understand all-gather.

散射的反操作是收集（gather）。输入是一堆分片，每个分片位于特定的 rank 上。当你针对某个 rank（比如 rank 0）执行 gather 时，它会将所有分片拼接在一起。Gather 也不直接使用，但它是理解 all-gather 的基石。

---

Next is reduce. Those of you who do functional programming are probably familiar with what reduce is—it's exactly the same. The idea is that you start in the same starting point as a gather, and then you apply your reduction operation (say sum) to all of these and put the result on rank 0. So if you do a reduction with sum, you add them all up. You can think about gather as a reduction where the operation is concatenation.

接下来是归约（reduce）。做过函数式编程的同学可能对归约很熟悉——完全一样。思路是：起点和 gather 一样（数据分散在多个 rank 上），然后你对所有这些数据应用归约操作（比如求和），将结果放到 rank 0 上。如果你用求和做 reduction，就把它们全部加起来。你可以把 gather 看作以拼接作为操作的归约。

---

### All-Gather / 全收集（all-gather）

Let's move on to something more interesting. All-gather performs gather to all ranks, not just rank 0. Remember what gather does: it takes all the different pieces and puts them on one rank. Now all-gather just does it for every single rank. The "all" means output to all the ranks, and "gather" is what you're doing to all the ranks. This is going to come up a bunch. Later we'll see that each rank holds part of the parameters, and then you need to all-gather the parameters to get the full parameters for the full forward pass. In general, as we're doing training, we're going to see a lot of gather-to-do-something and then scatter, and then gather and scatter again.

我们来看更有趣的。All-gather（全收集）对**所有** rank 执行 gather，而不仅仅是 rank 0。回想 gather 的作用：它把所有不同的分片放到一个 rank 上。All-gather 则对每个 rank 都做同样的事。"all" 表示结果输出到所有 rank，而 "gather" 是你对所有 rank 所做的事情。这个操作会频繁出现。稍后我们会看到，每个 rank 持有一部分参数，然后你需要 all-gather 这些参数以获得完整参数以完成完整的前向传播。总的来说，在训练过程中，我们会看到大量的"收集→做某事→散射→再收集→再散射"的模式。

---

### Reduce-Scatter / 归约-散射（reduce-scatter）

Reduce-scatter performs reduce on each dimension and then scatters the results. Say you have four devices, each with some vector. When we did a reduce before, we just had 0, 1, 2, 3 and that got reduced to 6. But now reduce-scatter says: for each component of this tensor, I'm going to do a reduction, and then I'm going to put it on a different rank. Where this is going to show up, just to foreshadow things: after the backward pass, when you sum what you're going to do, each GPU will be dealing with different data, and you need to sum all of the gradients from the different shards, and then redistribute this storage.

Reduce-scatter（归约-散射）对每个维度执行归约，然后散射结果。假设有四个设备，每个设备都有一个向量。之前的 reduce 只是把 0, 1, 2, 3 归约成 6。但现在 reduce-scatter 说：对于这个张量的每个分量，我会执行归约，然后将结果放到不同的 rank 上。预告一下这个操作会出现在哪里：在反向传播之后，当你需要求和时，每个 GPU 处理着不同的数据，你需要将所有不同分片的梯度求和，然后重新分配这些存储。

---

### All-Reduce / 全归约（all-reduce）

Finally, all-reduce. If you understand reduce-scatter and all-gather, it's basically you do one and then you do the other. So what this does is reduce-scatter the same input as before, and then the all-gather part puts them all on the same—everything on the same node. All-reduce is in some sense the easiest to understand: you have a bunch of tensors, you reduce (in this case sum), and then you replicate them on all the nodes. We're going to see this one first when we do data parallel, where we sum the gradients and then replicate the full parameters.

最后是全归约（all-reduce）。如果你理解了 reduce-scatter 和 all-gather，all-reduce 基本上就是先做一个再做一个。所以它的操作是：对和之前相同的输入执行 reduce-scatter，然后 all-gather 部分把所有内容放在同一个节点上。All-reduce 在某种意义上最容易理解：你有一堆张量，做归约（这里是求和），然后在所有节点上复制结果。我们在做数据并行时会首先看到这个操作：我们对梯度求和，然后复制完整参数。

---

Later, we're going to see how to get to fancier things like Zero or FSDP. We need to break the all-reduce into reduce-scatter and all-gather, because then you can intervene and manage things a bit more. But for the basic version, all-reduce is fine.

稍后我们会看到如何实现更高级的技术，如 Zero 或 FSDP。我们需要将 all-reduce 分解为 reduce-scatter 和 all-gather，因为这样你可以介入并更好地管理数据。但对于基础版本，all-reduce 就足够了。

---

### All-to-All / 全集散（all-to-all）

Finally, all-to-all. This one is, in some ways, the most general. You basically specify how each rank sends a particular message to another rank. The intuition here is that each rank has both a split of the data and also a subset of experts (in MOEs). The key idea of the MOE is dynamic routing: you have to look at your data to figure out which experts you need to route those activations to. It ends up being an all-to-all communication. If everything were balanced—meaning that every rank sent the same number of bytes to every other rank—then all-to-all can be thought of as essentially a transpose. If you think about this as a matrix, all you're doing is transposing that matrix. But in general, all-to-all also handles unbalanced splits. In general, you want the splits to be as balanced as possible.

最后是 all-to-all（全集散）。在某种意义上，这是最通用的操作。你基本上指定每个 rank 如何向另一个 rank 发送特定消息。其直觉是：每个 rank 既有数据的一个分片，也有一组专家（在 MOE 中）。MOE 的关键思想是动态路由：你必须查看数据来决定需要将哪些激活值路由到哪些专家。最终这就是一个 all-to-all 通信。如果一切均衡——即每个 rank 向每个其他 rank 发送相同数量的字节——那么 all-to-all 本质上可以看作一个转置。如果把它看作一个矩阵，你所做的就是转置这个矩阵。但一般来说，all-to-all 也能处理不均衡的分割。总的来说，你希望分割尽可能均衡。

---

### Summary of Terminology / 术语总结

A few helpful tips to remember the terminology: Reduce is, well, it's reduction—it performs some associative commutative operation (could be sum, max, min). Scatter is the inverse of gather: scatter distributes, gather centralizes. And "all" just means the destination is all devices. That explains all-reduce and all-gather.

几条有帮助的记忆技巧：归约（reduce）就是归约——它执行某种结合可交换操作（可以是求和、最大值、最小值）。散射（scatter）是收集（gather）的逆操作：scatter 是分散，gather 是集中。而 "all" 表示目标为所有设备。这便解释了 all-reduce 和 all-gather 的命名。

---

## Hardware: How GPUs Are Connected / 硬件：GPU 如何连接

Let's talk about the hardware, in particular how GPUs are connected, because we already know what's inside a GPU. In a traditional setup, you have a server with CPUs, a PCIe bus connecting things, and GPUs sitting off of them with some RAM. This computer connects via Ethernet to another computer. GPUs on the same node use PCIe to communicate, and GPUs on different nodes have to go all the way through Ethernet. This is like if you bought your gaming GPU and hooked it up with your friend to train some big model.

我们来谈谈硬件，特别是 GPU 如何连接，因为我们已经了解了 GPU 内部结构。在传统设置中，你有一台服务器，上面有 CPU、连接各种外设的 PCIe 总线，以及挂在总线上的 GPU 和一些 RAM。这台计算机通过以太网连接另一台计算机。同一节点上的 GPU 使用 PCIe 通信，而不同节点上的 GPU 则需要通过以太网。这就像你买了一块游戏 GPU，和朋友的 GPU 连起来试图训练一个大模型。

---

But if you're really serious about training, then things look more advanced. The typical setup is: you have GPUs (typically eight GPUs per node) connected via NVIDIA's NVLink to a switch (NVSwitch). Just for calibration, if you use NVLink 5, you're getting 1.8 terabytes per second of total bandwidth. Remember, HBM for B200 was 8 terabytes per second, so it's about 4x slower. This is still pretty fast if you think about going between devices, but not as fast as HBM, which is much slower than shared memory or L1 cache.

但如果你真的认真对待训练，那么配置会更先进。典型设置是：你有 GPU（通常每节点八个），通过 NVIDIA 的 NVLink 连接到交换机（NVSwitch）。仅供参考：使用 NVLink 5 时，总带宽为 1.8 TB/s。回想一下，B200 的 HBM 是 8 TB/s，所以大约慢了 4 倍。考虑到这是设备间通信，这仍然相当快，但显然不如 HBM 快，而 HBM 又比共享内存或 L1 缓存慢得多。

---

From a programming perspective, you can think about GPUs as connected to any other GPU. You go GPU to any other GPU, and the hardware takes care of transmitting to the switch, and the switch routes it. At some point, as your number of GPUs grows, you have to put these nodes into racks (pods) connected by InfiniBand. The GPU doesn't connect directly to another GPU via InfiniBand; it has to go through PCIe and a special InfiniBand cable. The speeds are much, much lower. And finally, if you run out of InfiniBand and have these huge pods, you connect them via Ethernet, which goes through PCIe and actually goes through the CPU, which is even slower. It's analogous to the memory hierarchy: the more nodes you have, the slower communication is going to be. You can't have an NVSwitch handling 100,000 GPUs.

从编程角度看，你可以把 GPU 视为与任意其他 GPU 相连。GPU 到任意其他 GPU，硬件负责传输到交换机，交换机进行路由。当 GPU 数量增长时，你需要将这些节点放入通过 InfiniBand 连接的机架（pod）中。通过 InfiniBand，GPU 不直接连接到另一个 GPU；它必须经过 PCIe 和一条特殊的 InfiniBand 线缆。速度要低得多。最后，如果 InfiniBand 也不够了、有大量 pod，你需要通过以太网连接它们。以太网要经过 PCIe，而且实际上要经过 CPU，速度更慢。这类似于内存层级结构：节点越多，通信越慢。你不可能让一个 NVSwitch 处理 10 万个 GPU。

---

### RDMA (Remote Direct Memory Access) / RDMA（远程直接内存访问）

An important hardware detail: with traditional Ethernet, the GPU has to talk to the CPU to get its data copied. It has to copy data to the CPU's socket buffer, build network packets, copy to the network interface, and then ship it over. This introduces a lot of latency. Remote Direct Memory Access (RDMA) allows a GPU to directly write or read from another GPU's memory without using the CPU at all. In NVLink and NVSwitch land, you have RDMA. InfiniBand also supports RDMA, so GPUs can directly connect without involving the CPU. But standard Ethernet does not.

一个重要的硬件细节：在传统以太网中，GPU 必须与 CPU 通信来复制数据。数据必须拷贝到 CPU 的内核 socket 缓冲区，构建网络包，拷贝到网络接口，然后发送出去。这引入了大量延迟。远程直接内存访问（RDMA）允许 GPU 直接从另一个 GPU 的内存读写，完全不需要 CPU。在 NVLink 和 NVSwitch 领域，你有 RDMA。InfiniBand 也支持 RDMA，因此 GPU 可以直接相互连接而不涉及 CPU。但标准以太网不支持。

---

There are two notable advancements. NVIDIA has been pushing the limits with larger pods—the NVL72 puts 72 GPUs all NVSwitched into one NVLink domain, with very fast NVLink speeds. Normally, you have eight GPUs interlinked fast, and outside of that things slow down. But with enough money, you can get fast interconnects up to 72 GPUs. Also, while standard Ethernet doesn't support RDMA, there has been progress with RoCE (RDMA over Converged Ethernet), where Ethernet actually bypasses the CPU. This is sort of NVIDIA's answer to InfiniBand. InfiniBand is very expensive, as are many NVIDIA products, but you can get pretty good performance using RoCE. Meta had a paper showing they were exploring this—Llama may or may not have been trained over converged Ethernet.

有两个值得注意的进展。NVIDIA 一直在推动更大 pod 的极限——NVL72 将 72 个 GPU 全部通过 NVSwitch 接入一个 NVLink 域，享有非常快的 NVLink 速度。通常，你有 8 个 GPU 高速互连，在此之外速度就会下降。但如果有足够的资金，你可以获得高达 72 个 GPU 的快速互连。此外，虽然标准以太网不支持 RDMA，但在以太网方面也有进展——RoCE（融合以太网上的 RDMA）使得以太网可以绕过 CPU。这算是 NVIDIA 对 InfiniBand 的回应。InfiniBand 非常昂贵（NVIDIA 的很多产品都是如此），但使用 RoCE 可以获得相当好的性能。Meta 有一篇论文展示他们正在探索这一点——Llama 可能（也可能没有）在融合以太网上训练。

---

## Programming Model: NCCL and PyTorch / 编程模型：NCCL 和 PyTorch

So at the very lowest level, there's something called the NVIDIA Collective Communications Library, NCCL (pronounced "nickel"), which translates the collective operations (all-reduce, reduce, broadcasts) into the actual low-level packets sent between GPUs. When you use NCCL, it figures out the topology of the hardware, figures out the path between different GPUs, and then launches GPU kernels to send and receive data. Because at the end of the day, everything that runs on a GPU is a kernel. So there are communication kernels as well.

在最底层，有一个叫作 NVIDIA 集合通信库（NCCL，读作 "nickel"）的库，它将集合操作（all-reduce、reduce、broadcast）翻译为 GPU 之间发送的实际底层数据包。当你使用 NCCL 时，它搞清硬件拓扑，找出不同 GPU 之间的路径，然后启动 GPU kernel 来发送和接收数据。因为归根结底，在 GPU 上运行的一切都是 kernel。所以也存在通信 kernel。

---

PyTorch conveniently has a `torch.distributed` library that provides a clean interface into these collective operations. You don't have to explicitly think about NCCL. This library also supports different backends for different hardware. If you are on GPUs, you use the NCCL backend. If you are on CPUs, there's something called gloo. This library also supports higher-level models and algorithms such as FSDP, but we're not going to use those in the course because we're building things from scratch.

PyTorch 很方便地提供了 `torch.distributed` 库，为这些集合操作提供了清晰的接口。你不需要显式地考虑 NCCL。这个库还为不同硬件支持不同的后端。如果在 GPU 上，使用 NCCL 后端；如果在 CPU 上，有一个叫 gloo 的后端。这个库也支持更高级的模型和算法，如 FSDP，但我们在这门课中不会使用它们，因为我们从零构建。

---

### Collective Operations in Code / 集合操作的代码实现

Let's walk through some basic examples. There's a function called `spawn`, which takes another function and says: I'm going to run this replicated `world_size` times. Normally you would call `torch.multiprocessing.spawn`. Each process has a rank (0, 1, 2, ... up to world_size minus 1), and there are world_size number of these functions each running on a process at the same time.

让我们浏览一些基本示例。有一个叫 `spawn` 的函数，它接受另一个函数作为参数，并说：我将以 `world_size` 次复制运行这个函数。通常你会调用 `torch.multiprocessing.spawn`。每个进程有一个 rank（0, 1, 2, ... 直到 world_size 减 1），有 world_size 个这样的函数同时在各进程上运行。

---

There's a setup step: you configure the master address and port. Notice this is not how the GPUs will actually communicate their data; this is for general metadata and coordination. The actual data goes through NCCL—otherwise it would be very, very slow. There's a barrier function, which is a synchronization barrier. It waits for all processes to get to that point. All processes are running asynchronously, so one could completely finish before the others. If you want to make sure some code is executed before other code, you put synchronization barriers in. The downside of putting more barriers is that you end up waiting potentially unnecessarily.

有一个设置步骤：配置 master 地址和端口。注意这不是 GPU 实际传输数据的方式；这用于一般的元数据和协调。实际数据通过 NCCL 传输——否则会非常非常慢。有一个 barrier 函数，它是一个同步屏障。它等待所有进程到达该点。所有进程是异步运行的，所以一个可能在其他之前完全完成。如果你想确保某些代码先执行，就放置同步屏障。放入更多屏障的缺点是，你可能会不必要地等待。

---

Let's try an all-reduce. I create a tensor, and each rank has a different tensor to make it more interesting. After the all-reduce, each rank has the sum of each component replicated across all ranks. The function is a PyTorch function: you pass in the tensor and the reduction operation (sum). If you wanted to be fancier, you could do async. A typical thing is overlapping computation and communication: you can fire off this operation, go ahead and load some other data for the next step which is independent of this operation, and then when you want to make sure you're actually done, you call a wait or a barrier.

让我们试一下 all-reduce。我创建一个张量，为了让示例更有趣，每个 rank 使用不同的张量。all-reduce 之后，每个 rank 都有每列之和，且在所有 rank 上复制。这是一个 PyTorch 函数：你传入张量和归约操作（求和）。如果你想要更高级的做法，可以用异步模式。一个典型的做法是重叠计算和通信：你可以触发这个操作，然后继续为下一步加载一些与此操作无关的数据，当你想确保操作实际完成时，再调用 wait 或 barrier。

---

Similarly, we can do a reduce-scatter. Here, we have an input tensor and allocate an output tensor. After the reduce-scatter, the input is not touched, but the output gets the reduction of each component written into the respective ranks. And for all-gather, the output has all the different inputs gathered onto all the different ranks. Proof by example: all-reduce equals reduce-scatter plus all-gather.

类似地，我们可以做 reduce-scatter。这里有一个输入张量，我们分配一个输出张量。reduce-scatter 之后，输入不变，但输出将每个分量的归约结果写入各自对应的 rank。对于 all-gather，输出将所有不同的输入收集到所有不同的 rank 上。通过示例证明：all-reduce 等于 reduce-scatter 加 all-gather。

---

### Benchmarking Communication / 通信性能基准测试

How fast does communication happen? Let's benchmark an all-reduce with 100 million elements. Just like before when we do benchmarking, we warm up first. Then we call CUDA synchronize and also the barrier—because there are two forms of asynchrony here (the CUDA kernels and the different processes)—to make sure everything is done before starting the timer. Then we do the all-reduce, wait again with synchronize and barrier, and stop the timer.

通信到底有多快？让我们用 1 亿个元素对 all-reduce 做基准测试。和之前做基准测试一样，我们先预热。然后调用 CUDA synchronize 和 barrier——因为这里有两种异步形式（CUDA kernel 和不同进程）——确保在开始计时之前一切就绪。然后执行 all-reduce，再次用 synchronize 和 barrier 等待，然后停止计时。

---

To compute the effective bandwidth, we calculate how many bytes were sent and should be sent during this computation. Divide by the total time, and you get the effective bandwidth. For all-reduce, the number of sent bytes is: size of payload × 2 × (world_size − 1). There's a factor of 2 because you need to both send and receive. The total duration is the wall clock time it took. Multiply by world_size because it's the total amount all ranks have waited. The bandwidth converges to roughly 2 × size / duration as world_size increases, independent of world size and topology. You get something like about 400 gigabytes per second.

为了计算有效带宽，我们计算在这次计算中发送了多少字节以及应发送多少字节。除以总时间，你就得到了有效带宽。对于 all-reduce，发送的字节数是：载荷大小 × 2 × (world_size − 1)。乘以 2 是因为既需要发送也需要接收。总持续时间是墙钟时间。乘以 world_size 是因为这是所有 rank 等待的总时间。随着 world_size 增大，带宽收敛到大约 2 × 大小 / 持续时间，与 world size 和拓扑无关。你能得到大约 400 GB/s。

---

For reduce-scatter, it's very similar. There is no 2x factor. For all-reduce, as we stated, it's reduce-scatter plus all-gather, so naturally it moves twice the amount of data and takes twice the time. But the two cancel out, so you get the same kind of bandwidth.

对于 reduce-scatter，情况非常类似。没有 2 倍的因子。对于 all-reduce，如前所述，它是 reduce-scatter 加 all-gather，所以自然传输两倍的数据，花费两倍的时间。但两者相互抵消，所以你得到同样的带宽。

---

## Part 2: Training with Parallelism / 第二部分：使用并行训练

Now let's actually start thinking about how you train models. We're going to walk through a very bare-bones implementation of training MLPs. Remember that MLPs are the actual compute bottleneck in the transformer. So this is actually pretty representative of what you'll see. Three types: data parallelism, tensor parallelism, and pipeline parallelism.

现在让我们真正开始思考如何训练模型。我们将走过一个非常简化的 MLP 训练实现。请记住，MLP 是 transformer 中的实际计算瓶颈。所以这实际上相当有代表性。三种并行类型：数据并行（data parallelism）、张量并行（tensor parallelism）和流水线并行（pipeline parallelism）。

---

The picture to have in your head: data parallelism splits the data into pieces, and each GPU is responsible for part of the data, keeping track of all the parameters and doing normal model training, then synchronizing. Tensor parallelism cuts each layer—each rank gets part of each layer, generally meaning we're going to have to transfer a lot more data. Pipeline parallelism splits the network so each rank gets a subset of the layers; within each layer, it gets all the dimensions and all the data in some form.

你脑海中应有的画面：数据并行将数据分成块，每个 GPU 负责一部分数据，跟踪所有参数并进行正常的模型训练，然后同步。张量并行切割每一层——每个 rank 获得每一层的一部分，通常意味着我们需要传输更多的数据。流水线并行将网络切分，每个 rank 获得一个层子集；在每一层内，它获得所有的维度和所有数据（以某种形式）。

---

### Data Parallelism / 数据并行

The way data parallelism works: you have a data matrix (batch_size × num_dim) and break up the rows into world_size pieces. Each rank gets a piece. The local batch size is batch_size divided by world_size. In practice, each rank should probably load its own data rather than have this bottleneck, but this is just for illustrative purposes.

数据并行的运作方式：你有一个数据矩阵（batch_size × num_dim），将行分成 world_size 份。每个 rank 得到一份。局部 batch size 是 batch_size 除以 world_size。在实践中，每个 rank 应该加载自己的数据，而不是有这个瓶颈，但这只是用于说明。

---

You instantiate the MLP—for each layer, a num_dim × num_dim matrix initialized randomly. In the forward pass, you take the data (only your local batch), go through the layers, do a forward pass, then a backward pass. But now, remember, every rank has different data, so the gradients are going to be different as well. This is the key step that makes data parallelism work: we synchronize the gradients across all the workers. This is the only difference between standard training and Distributed Data Parallel (DDP). For all the parameters, do an all-reduce of param.grad, and average. After this all-reduce is done, each rank has the exact same gradients, and then you update the parameters.

你实例化 MLP——每一层是一个 num_dim × num_dim 矩阵，随机初始化。在前向传播中，使用数据（仅是局部 batch），遍历各层，执行前向传播，然后执行反向传播。但现在，记住，每个 rank 有不同的数据，所以梯度也会不同。这是使数据并行发挥作用的关键步骤：我们在所有 worker 之间同步梯度。这是标准训练与分布式数据并行（DDP）之间的唯一区别。对于所有参数，对 param.grad 执行 all-reduce，并求平均。all-reduce 完成后，每个 rank 有完全相同的梯度，然后更新参数。

---

It's really elegant: it's basically standard training applied to your local batch, but you just insert this all-reduce after the backward pass. One line of code change, and then the parameters get updated. As you're training, each rank is performing parameter updates as if it had all the data on it, but it's only actually processing a part of the data. The losses are different across ranks, the gradients are initially different, but they are all-reduced to be the same across ranks—so the parameters all remain the same across ranks.

这真的非常优雅：基本上就是对你的局部 batch 进行标准训练，但你在反向传播之后插入了这个 all-reduce。一行代码的改动，然后参数就更新了。在训练过程中，每个 rank 进行的参数更新就好像它拥有所有数据一样，但实际上它只处理了一部分数据。不同 rank 上的损失不同，梯度初始也不同，但它们通过 all-reduce 变得一致——因此所有 rank 上的参数保持一致。

---

Your batch size has to be at least world_size for this to really make sense, and usually it should be quite a bit larger. If it's not a multiple of world_size, you can pad with zeros. For a transformer, it would be basically the same—DDP is very modular: it just averages the parameters and doesn't care what your forward pass looks like.

你的 batch size 必须至少为 world_size 才能真正有意义，而且通常应该大得多。如果不是 world_size 的倍数，可以用零填充。对于 transformer，基本上是一样的——DDP 非常模块化：它只是对参数求平均，不关心你的前向传播长什么样。

---

So next lecture, Tatsu is going to talk about fancier data parallelism: FSDP and Zero. The idea there is that all-reduce is a very simple monolithic operation, but it requires holding all the model parameters in memory. What if the model parameters don't fit in memory? Then you're going to have to be more clever, and that's the topic for the next class.

所以下一讲，Tatsu 将讨论更高级的数据并行：FSDP 和 Zero。其思路是：all-reduce 是一个非常简单的整体操作，但它需要将所有模型参数保存在内存中。如果模型参数无法放入内存怎么办？那你就需要更聪明的方法，而这正是下一课的主题。

---

### Tensor Parallelism / 张量并行

In tensor parallelism, we're going to cut each layer and not cut the data. So each rank gets part of each layer. Generally, this means we're going to have to transfer a lot more data. We assume every rank has all the data just for simplicity. For each rank, we define a `local_num_dim`—each rank is only responsible for a subset of the dimensions. The parameters now are `num_dim × local_num_dim`. If this were one of the parameter matrices for one layer, we would be splitting down the columns. This is also known as column tensor parallel.

在张量并行（tensor parallelism）中，我们是切割每一层而不是切割数据。所以每个 rank 获得每一层的一部分。通常这意味着我们需要传输更多的数据。为简单起见，我们假设每个 rank 拥有所有数据。对于每个 rank，我们定义一个 `local_num_dim`——每个 rank 只负责维度的一个子集。参数现在是 `num_dim × local_num_dim`。如果这是某一层的参数矩阵之一，我们就是在按列切割。这也被称为列张量并行（column tensor parallel）。

---

In the forward pass, we go through all layers and compute activations. We start with x (the data), access the parameters at that layer (only a slice of the parameters). We can still apply the non-linearity since it's element-wise. But now we need to communicate activations. Rank 1 has activations for part of the matrix, rank 2 has another part, and so on. We need to put all the activations on all the ranks. We use all-gather as a collective primitive: each rank has its part (batch_size × local_num_dim), and after the all-gather, we concatenate to form the full dimensional x (batch_size × num_dim). This is done for every layer.

在前向传播中，我们遍历所有层并计算激活值。我们从 x（数据）开始，访问该层的参数（只是参数的一个切片）。由于非线性操作是逐元素的，我们仍然可以应用它。但现在我们需要通信激活值。rank 1 有矩阵一部分的激活值，rank 2 有另一部分，以此类推。我们需要将所有激活值放到所有 rank 上。我们使用 all-gather 作为集合原语：每个 rank 有自己的一部分（batch_size × local_num_dim），all-gather 之后，我们将它们拼接形成完整维度的 x（batch_size × num_dim）。每一层都这样做。

---

One difference from data parallel: now we have to muck around with the model. Data parallel is very elegant because it's splitting by data—the model is treated as a module. But now we have to muck around with the model. This strongly leverages the fact that if you want to do a matrix multiplication, you can split it up into a set of smaller matrix multiplications, do those on different ranks, and then gather the results.

与数据并行的一个不同之处：现在我们必须捣鼓模型本身。数据并行非常优雅，因为它按数据分——模型被当作一个模块。但现在我们必须捣鼓模型。这强烈利用了这样一个事实：如果你想做矩阵乘法，可以将其分解为一组较小的矩阵乘法，在不同的 rank 上执行，然后收集结果。

---

When it comes to backpropagation, you have your activations and you have to reduce-scatter to all the different gradients. In some ways, all-gather and reduce-scatter have this kind of duality: in the forward pass you're all-gathering, and in the backward pass you're reduce-scattering. If you just call `.backward`, it won't do it automatically—there's no parallelism in that. PyTorch has automatic tools, but here we're managing things explicitly. That's by design, because this is CS336, building language models from scratch. In practice, you probably wouldn't have to do that.

在反向传播方面，你有激活值，并且必须对不同的梯度执行 reduce-scatter。在某种意义上，all-gather 和 reduce-scatter 有一种对偶性：前向传播中你做 all-gather，反向传播中你做 reduce-scatter。如果你只是调用 `.backward`，它不会自动做这些——其中没有并行。PyTorch 有自动工具，但这里我们是显式管理的。这是有意为之，因为这是 CS336，从零构建语言模型。在实践中，你可能不需要这样做。

---

### Pipeline Parallelism / 流水线并行

The idea behind pipeline parallelism is we're going to split the network so each rank gets a subset of the layers. Within each layer, it gets all the dimensions, and every rank sees all the data in some form. We split up the layers so `local_num_layers` is the number of layers a particular rank handles. The local params have only that number of layers, but within each layer, it's still `num_dim × num_dim`.

流水线并行（pipeline parallelism）的思路是：我们沿这个方向切分网络，每个 rank 得到一个层子集。在每一层内，它获得所有维度，并且每个 rank 以某种形式看到所有数据。我们切分层，使得 `local_num_layers` 是某个 rank 处理的层数。局部参数只有那么多层，但在每一层内，它仍然是 `num_dim × num_dim`。

---

In addition to splitting up the layers, we also split the batch into micro-batches. If I'm rank 0, I get the data and chunk it into a number of micro-batches. For each micro-batch, I receive it from the previous rank, do the feedforward pass only on the layers assigned to this rank, and then send to the next rank. This uses receive and send, which are pointwise operations. So basically: receive tensor from rank minus 1, send tensor to rank plus 1.

除了切分层之外，我们还将 batch 分成多个微批次（micro-batches）。如果我是 rank 0，得到数据后将其分成若干个微批次。对于每个微批次，我从上一个 rank 接收数据，仅在此 rank 分配的层上执行前向传播，然后发送到下一个 rank。这使用 receive 和 send，它们是点对点操作。基本上：从 rank-1 接收张量，向 rank+1 发送张量。

---

The reason for micro-batches: in pipeline parallelism, one rank gets the data, processes some layers, sends to the next GPU, which processes some layers, and so on. This is a very natural way of dividing a deep network. But the problem is pipeline bubbles: while you're not processing, you're waiting around for other tensors to process. This ends up being quite inefficient. The idea behind micro-batches is that you break it up into smaller batches so you can process it quickly and send it on to the next one, reducing the number of pipeline bubbles.

使用微批次的原因：在流水线并行中，一个 rank 获取数据，处理一些层，发送到下一个 GPU，下一个 GPU 处理一些层，以此类推。这是分割深度网络的一种非常自然的方式。但问题是会出现所谓的流水线气泡（pipeline bubbles）：当你不处理时，你就在等待其他张量完成处理。这最终效率相当低。微批次背后的思想是：将其分解为更小的批次，以便快速处理并发送到下一个，从而减少流水线气泡的数量。

---

Another important idea not handled in this naive version is overlapping communication and computation. This is very important for pipeline parallelism. You want: while you're computing here, you can be receiving data or sending data. Computation and communication should overlap, reducing the amount of time you actually spend waiting. If you put an "I" before these operations (e.g., `isend`, `irecv`), they become async, and you need to manage more things, but you can overlap.

在这个朴素版本中没有处理的另一个重要理念是重叠通信和计算。这对流水线并行非常重要。你想要的是：当你在这里计算时，可以同时接收或发送数据。计算和通信应该重叠，减少实际等待的时间。如果你在这些操作前加上 "I"（例如 `isend`、`irecv`），它们变为异步，你需要管理更多东西，但可以实现重叠。

---

### Missing Topics and Future Lectures / 遗漏话题与后续讲座

A few things are missing that we'll fill in next time. Communication vs. computation overlap is crucial in pipeline parallelism. In data parallelism, this also happens: I just did a forward pass and at the end did all these all-reduces. But if you're clever, on the backward pass, as soon as the gradients are done, you can start sending them. This allows you to overlap communication and computation more, and it's something explored in assignment two.

有几项内容将在下次补齐。通信与计算的重叠在流水线并行中至关重要。在数据并行中也会发生：我先做了前向传播，最后做了所有这些 all-reduce。但如果你更聪明一些，在反向传播中，梯度一完成就可以开始发送。这让你能够更多地重叠通信和计算，这也是作业二中要探索的内容。

---

What about general models? This MLP gives you essentially most of what you need for understanding the basics. Some of the larger models just require a lot more bookkeeping, so it's harder to see the core algorithms. There are other types of parallelism we haven't covered: sequence parallelism takes a whole sequence and chops it into pieces, allowing you to parallelize the attention computation. Expert parallelism allows you to parallelize the experts for MOEs—this is where all-to-all comes in. And different combinations of parallelization techniques will also show up in the assignment.

那一般模型呢？这个 MLP 基本给了你理解基础知识所需的大部分内容。一些更大的模型只需要很多更繁琐的簿记，因此更难看到核心算法。还有其他我们未涵盖的并行类型：序列并行（sequence parallelism）将整个序列切分成块，让你能够并行化注意力计算。专家并行（expert parallelism）让你能够并行化 MOE 中的专家——这就是 all-to-all 出现的地方。不同的并行技术组合也将在作业中出现。

---

### Choosing Parallelism Strategies / 选择并行策略

Which parallelism technique you choose is going to be strongly dependent on the hardware. For example, tensor parallelism has a lot of communication because for every layer, you need to send all these activations, which are fairly big. So generally, tensor parallelism happens within a node on NVLink, where you have high bandwidth. You wouldn't do tensor parallelism past an NVLink domain. Pipeline parallelism can tolerate much slower interconnects. Some decentralized training work uses pipeline parallel because GPUs are halfway across the world—but you wouldn't want to do tensor parallel in that setting.

你选择哪种并行技术强烈依赖于硬件。例如，张量并行有大量通信，因为对于每一层，你需要发送所有这些激活值，它们相当大。所以通常，张量并行在高带宽的 NVLink 域内的节点上运行。你不会在 NVLink 域之外做张量并行。流水线并行可以容忍慢得多的互连。一些去中心化训练工作使用流水线并行，因为 GPU 分布在世界的不同角落——但你不会在这种情况下做张量并行。

---

Sometimes when you look at combinations, it will be tensor parallel within a node and then data parallel or FSDP, and then pipeline parallelism if you need it. There are other effects: if you do data parallel, you might be able to do quite a bit, but then you hit the critical batch size—if you start increasing the batch size too much, it doesn't actually help you. In that case, you're wasting your compute and you're better off using tensor parallel.

有时当你考虑组合时，它会是：节点内张量并行，然后是数据并行或 FSDP，如果需要再加流水线并行。还有其他效应：如果你做数据并行，你可能能做很多，但接着会遇到临界批大小（critical batch size）——如果批大小增加太多，实际上没有帮助。这时候你在浪费计算资源，最好改用张量并行。

---

### PyTorch vs. TPUs / PyTorch 与 TPU

One thing to note: we are using PyTorch and really using the collective operations in a very primitive way, so you can see mechanically what's happening. Another approach, especially in TPU land, is that you can simply define the model and the sharding strategy, and the compiler handles a lot of the decision of what kind of communication operations you need. You basically say: this piece of data needs to be here and here. The compiler does some magic to figure out what. That's appealing, but it would take a lot of the joy out of actually building things from scratch.

需要注意一点：我们特意使用 PyTorch 并以非常原语的方式使用集合操作，这样你可以从机械层面看到发生了什么。另一种方法，尤其是在 TPU 领域，你可以简单地定义模型和分片策略，编译器会处理大量有关你需要哪种通信操作的决策。你基本上说：这块数据需要在这里、在那里。编译器施展魔法来搞定。这很有吸引力，但它会夺走从零构建的许多乐趣。

---

## Summary / 总结

There are many ways to parallelize. You can cut by data, by tensor or expert, by pipeline or sequence. We looked at data parallelism—only DDP; next time we'll do FSDP and Zero. Tensor parallelism requires very fast interconnects. Pipeline parallelism less so, but you need to work hard to reduce pipeline bubbles. At a high level, we see a pattern come up often: you can either recompute or store in memory (like activation checkpointing), or you can store on a different GPU. From that perspective, with data parallel you're doing redundant work in some sense—every rank is updating its parameters and keeping track of all parameters. But the reason is that you don't have to move the optimizer state across. Hardware is getting faster, but in some sense, we'll always want bigger models. So this idea of having a hierarchical structure will always be there.

有很多并行化的方式。你可以按数据切、按张量或专家切、按流水线或序列切。我们看了数据并行——只是 DDP；下次我们会看 FSDP 和 Zero。张量并行需要非常快的互连。流水线并行要求没那么高，但你需要努力减少流水线气泡。在较高的层次上，我们经常看到一个模式：你既可以重计算也可以存储在内存中（如激活检查点），或者你可以存储在不同的 GPU 上。从这个角度看，数据并行在某种意义上做了冗余工作——每个 rank 都在更新自己的参数并跟踪所有参数。但这样做是因为你不需要跨节点传输优化器状态。硬件在变得更快，但在某种意义上，我们永远想要更大的模型。因此，这种层级结构的思路将一直存在。

---

That's it for today. Next Wednesday, Tatsu will do a deeper dive on more parallelism techniques.

今天的课到此结束。下周三，Tatsu 将更深入地探讨更多并行技术。
