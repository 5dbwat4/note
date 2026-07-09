---
title: "Lecture 7: Parallelism"
---

# Lecture 7: Parallelism / 第七讲：并行化（Parallelism）

---

OK. Let's get started. So welcome back, everyone. So today we're going to talk about parallelism. And remember in the last week, we introduced how to make a single GPU go fast by writing kernels. And we really looked inside this GPU. And this week, we're going to talk about how to leverage multiple GPUs to make your code go even faster. So the picture you should have in your head is something like this. So for the last week, we focused on one of these boxes, where you have your GPU. Remember, you have your High Bandwidth Memory, HBM, L2 cache, L1 cache, registers, and a bunch of streaming multiprocessors. So now the picture gets extended, because instead of having one GPU, you might have four, you might have 1,000 GPUs. And those are going to be connected. And I'll talk later about how those GPUs are going to get connected. And then you're going to have to figure out how to leverage all of this compute to train models. So in both cases, meaning both in the single GPU case and in the multi-GPU case, as we'll talk about today, the situation is kind of similar if you zoom out, which is that the compute, the arithmetic logic units, the tensor core, and so on, is far away from your data. And far away for a single GPU means all the way over here in HBM. And now if you have multi GPUs, the thing that you need here might be all the way on a different GPU, and you're going to have to shuffle that over somehow. But the same principles are going to be the same, because the game is to orchestrate the computation to try to avoid data transfer bottlenecks. It's very easy to use a ton of GPUs, but it's hard to use them effectively.

好，我们开始吧。欢迎回来。今天我们要讨论并行化（parallelism）。回顾一下，上周我们介绍了如何通过编写核函数（kernels）让单个 GPU 跑得更快，我们深入研究了 GPU 内部。而本周，我们将讨论如何利用多个 GPU 让你的代码跑得更快。你脑海中应该有这样的画面：上周我们聚焦于其中一个盒子——你的 GPU。记住，它有高带宽内存（High Bandwidth Memory, HBM）、L2 缓存、L1 缓存、寄存器，以及大量的流式多处理器（streaming multiprocessors）。现在这幅图延展了，因为你可能不是只有一个 GPU，而是四个，甚至一千个 GPU。这些 GPU 会连接在一起。我稍后会讨论这些 GPU 是如何连接的。然后你需要弄清楚如何利用所有这些计算能力来训练模型。所以无论是单 GPU 情况还是多 GPU 情况——正如我们今天要讨论的——如果你退一步看，情况是类似的：计算单元（算术逻辑单元、张量核心等）离你的数据很远。在单 GPU 中，"很远"意味着数据在 HBM 那头。而在多 GPU 中，你可能需要的数据在另一个 GPU 上，你得想办法把它搬过来。但基本原则是相同的——游戏的关键在于编排计算（orchestrate the computation），尽量避免数据传输瓶颈。用一大堆 GPU 很容易，但要高效地使用它们却很难。

---

So taking a little bit of liberty, we can think about the generalized hierarchy where at the local level next to the SMs a single node single GPU where you have an L1 cache shared memory. This was the fastest. And then you had HBM, which we lamented was so slow. But in this lecture, HBM is going to be considered fast. Now we're going to think about the single node multi-GPU setting where the GPUs are going to be connected via NVLink and NVSwitch. And then finally, the multi-node and multi-GPU, where we have to resort to InfiniBand and ethernet depending on what network you have. So last week, we talked about various tricks for in reducing memory accesses, fusion and tiling. Read into shared memory, do as much as you can, and then write it back out. And this week, we're going to talk about how you can reduce the amount of communication across GPUs by replicating and sharding appropriately.

稍微简化一下，我们可以考虑一个通用的层次结构：在局部层面，靠近 SM 的地方——单个节点、单个 GPU——你有 L1 缓存和共享内存，这是最快的。然后是 HBM，我们之前抱怨过它太慢。但在这节课中，HBM 将被认为是"快的"。现在我们要考虑单节点多 GPU 的场景，其中 GPU 通过 NVLink 和 NVSwitch 连接。最后是多节点多 GPU 场景，我们不得不使用 InfiniBand 或以太网（取决于你有什么网络）。上周我们讨论了减少内存访问的各种技巧：融合（fusion）和分块（tiling）。读到共享内存中，尽可能多地计算，再写回去。而本周，我们将讨论如何通过适当的数据复制（replicating）和分片（sharding）来减少跨 GPU 的通信量。

---

So why do you do multi-GPUs? The obvious answer is, well, you want to scale. But to put a finer point on it, there's really two reasons. One is that your parameters or activations or gradients and optimizer state don't fit on the HBM memory of a single GPU. So B21 has 192 gigabytes. If you're training a 1 trillion parameter model, that's not going to fit on a single GPU. And the other reason is that even if your model could fit on a single GPU, you might want to leverage more GPUs by splitting everything up to train faster. So sometimes there will be some decisions to be made because you could fit everything on GPUs, but you have fewer cores. But if you spread it out, then you're going to have to pay the communication bandwidth. So that's some calculation you're going to have to do to figure out how to parallelize.

那为什么要用多 GPU 呢？显而易见的答案是：你想扩展规模。但更精确地说，有两个原因。一是你的参数（parameters）、激活值（activations）、梯度（gradients）和优化器状态（optimizer state）放不进单个 GPU 的 HBM 内存。B21 有 192 GB——如果你训练一个 1 万亿参数的模型，单个 GPU 是放不下的。另一个原因是，即使你的模型能放进单个 GPU，你也可能希望通过拆分所有东西、利用更多 GPU 来加速训练。所以有时你需要做出决策：你可以把所有东西都放进 GPU，但核心数更少；而如果你分散到多个 GPU，就需要付出通信带宽的代价。因此你需要做一些计算，来确定如何并行化（parallelize）。

---

So just one note here is that so far this lecture is Python. You execute it and you can just show everything. Now, in this lecture, if you run this directly, it uses multiprocessing. But when I trace through it, I'm putting in some of special single process mode. So if you want to see the standard out for this lecture run in the multiprocessing setup, you can click here. And I'll show this as we go through the lecture. But just remember as we step through this lecture, we're not actually doing multiprocessing, because we're just stepping through single lines of code.

有一点需要说明：到目前为止，这节课是用 Python 演示的。你执行它，就能展示所有内容。在这节课中，如果你直接运行，它使用的是多进程（multiprocessing）。但我在逐行讲解时，使用了某种特殊的单进程模式。所以如果你想看到这节课在多进程设置下运行的标准输出，可以点击这里。我会在课程中展示这个。但请记住，在我们逐行讲解时，实际上并没有运行多进程，我们只是在单步执行代码。

---

So this lecture is going to include two parts. One is we're going to learn about the building blocks of distributed communication and computation, starting with the programming model. Talk a little bit about the hardware. Start to implement things in Torch, which you're going to do on your assignment two. And then the second part is we're going to look at actual training. We're going to look at three types of parallelism. Data parallelism, tensor parallelism, pipeline parallelism. Each is going to cut up our model in different ways. We're going to do this for MLPs rather than the full transformer. But it's really the core computation is going to be shown here.

这节课包括两部分。第一部分，我们将学习分布式通信和计算的基本构建块，从编程模型开始，稍微讨论一下硬件，然后开始在 Torch 中实现相关操作——你们将在作业二中做这些。第二部分，我们将看实际的训练过程。我们会研究三种并行化（parallelism）方式：数据并行（data parallelism）、张量并行（tensor parallelism）和流水线并行（pipeline parallelism）。每种方式都会以不同的方式切割我们的模型。我们将针对 MLP（而不是完整的 Transformer）来演示，但核心计算逻辑都会在这里展示。

---

So let's dive in. So the first thing to talk about is these things called collective operations. So collective operations are these primitives from distributed programming that go back to the '80s. So the idea of parallel programming is very old. It wasn't invented for LLM training. And it's still the case that these primitives are the ones that we use today. And here, collective just means that you're specifying a general communication pattern or a template across multiple devices, rather than managing point to point how this GPU is going to communicate with another GPU. And this is going to be much easier, and the system can do a lot more work for you. So this is a very tried and trued interface for doing parallel programming.

让我们深入正题。首先要讨论的是所谓的**集合操作**（collective operations）。集合操作是分布式编程中的原语（primitives），可以追溯到上世纪 80 年代。并行编程的概念非常古老，并非为 LLM 训练而生。但直到今天，我们使用的仍然是这些原语。这里的"集合"（collective）意味着你指定的是跨多个设备的通用通信模式或模板，而不是管理单个 GPU 与另一个 GPU 之间的点对点（point-to-point）通信。这样会容易得多，系统可以为你做更多工作。这是一个经过充分验证的并行编程接口。

---

So the general setup is as follows. The terminology here is a little bit-- I find it a little bit strange, but this is standard in parallel programming. The idea is that you have a bunch of ranks where rank corresponds to a particular device, in our case a GPU. It could be a TPU. But the point is that you have, let's say, four ranks here. The world size corresponds to the number of devices, so the world size here is four. So there is a few operations we're going to go through. Broadcast, scatter, gather, reduce, all gather, reduce scatter, all reduce, and all to all. And each of these operations is going to specify how this set of ranks or devices is going to transfer some amount of data slash compute with it to some other set of devices.

基本的设置如下。这里的术语有点——我觉得有点奇怪，但这是并行编程中的标准。思想是这样的：你有一组 rank（rank），一个 rank 对应一个特定的设备，在我们的场景中是 GPU（也可以是 TPU）。假设这里有四个 rank。世界大小（world size）对应设备数量，所以这里 world size 是 4。我们需要了解几种操作：广播（broadcast）、散射（scatter）、收集（gather）、归约（reduce）、全收集（all gather）、归约-散射（reduce scatter）、全归约（all reduce）和全到全（all to all）。每个操作都指定了这一组 rank 或设备如何将一定数量的数据和/或计算传输给另一组设备。

---

So the first three, broadcast, scatter, gather, reduce, are really just warm ups, I would say. They allow you to get a sense of how these collective operations work, but they're not really going to be the ones that are driving most of training. All gather, reduce scatter, and all reduce are the ones that are going to show up again and again for distributed training of language models. And finally, all to all I'll just mention here, which is important for MOEs, but we're not going to actually spend too much time on this this lecture.

前三个——广播、散射、收集、归约——我认为只是热身。它们能让你感受这些集合操作是如何工作的，但并不是驱动大部分训练的核心操作。全收集（all gather）、归约-散射（reduce scatter）和全归约（all reduce）才是语言模型分布式训练中会反复出现的操作。最后是全到全（all to all），我在这里提一下，它对 MoE 很重要，但我们这节课不会花太多时间在这上面。

---

OK, so let's dive in with the simplest operation, which is broadcast. So in broadcasting, you have a rank 0. It could be any rank, but let's just say for sake of picking one, rank 0, has some tensor 0123. And it broadcasts it to all the ranks. So at the end of this operation, we have that each of the ranks has the same tensor on it. That should be pretty straightforward. And this, again, doesn't really show up in the core path of training. Generally, broadcasts are used for initialization, where let's say you initialize a load initial checkpoint and then you broadcast it to all the ranks. So something that's done like once.

好，让我们从最简单的操作开始——广播（broadcast）。在广播中，你有一个 rank 0（可以是任何 rank，但为了方便我们选一个）。rank 0 有一些张量（tensor），比如 [0, 1, 2, 3]。它把这个张量广播给所有 rank。操作结束时，每个 rank 上都拥有相同的张量。这应该很简单。同样，这并不真正出现在训练的核心路径中。通常，广播用于初始化，比如你加载了初始检查点（checkpoint），然后将其广播到所有 rank——这种操作只执行一次。

---

So the second operation is a scatter. And a scatter basically says, I have a tensor at rank 0 who is split up into the world size. And I'm going to basically scatter my tensor onto the other ranks. So rank 0 gets 0, the zeroth component. Rank 1 gets this, rank 2 gets this, and rank 3 gets that. So again, this is not directly used, but scatter is an important stepping stone to understand reduce scatter. So, as the name implies, scatter just takes a big tensor at one place and spreads it out onto multiple places. And you can see how this might be helpful, because you want all the GPUs you're scattering to do some local computation on the different parts.

第二个操作是散射（scatter）。散射的意思是：我在 rank 0 上有一个张量，它被按 world size 切分。然后我把这个张量分散到其他 rank 上。所以 rank 0 得到第 0 个分量，rank 1 得到这个，rank 2 得到这个，rank 3 得到那个。同样，这不直接用于训练，但散射是理解归约-散射（reduce scatter）的重要垫脚石。顾名思义，散射就是把一个地方的大张量分散到多个地方。你可以看到这很有用，因为你希望所有被散射到的 GPU 在不同部分上做本地计算。

---

So the inverse of scatter is gather. So this should be very predictable. The input is you have a bunch of pieces, each of which reside on a particular rank. And then when you do a gather, that's with respect to a particular rank, rank 0, it's going to just concatenate all the pieces together. Again, gather isn't directly used, but it's going to be a stepping stone to understand all gather.

散射的逆操作是收集（gather）。这应该很容易预测：输入是一堆碎片，每个碎片位于特定的 rank 上。当你做收集时，针对某个特定的 rank（比如 rank 0），它会将所有碎片拼接起来。同样，收集不直接用于训练，但它会是理解全收集（all gather）的垫脚石。

---

So next is reduce. So those of you who do functional programming are probably familiar with what reduce is. It's exactly the same. The idea is that you start in the same starting point as a gather. And where the tensor is split up across multiple-- well, you have some piece of data on each of the different ranks. And then you're going to apply your reduction operation to all of these and get that in, put that on rank 0. So in this case, if you do a reduction with sum, then you add these all up, you get six. So you can think about gather as a reduction where the operation is concatenation, if you will. And of course, reduce is important to understanding all reduce.

接下来是归约（reduce）。做过函数式编程的人应该熟悉什么是归约——完全一样的概念。起点和收集一样：张量被拆散在多个 rank 上，每个 rank 上有一部分数据。然后你对所有这些数据应用归约操作（reduction operation），将结果放到 rank 0 上。在这个例子中，如果你对求和做归约，就把它们全部加起来得到 6。所以你可以把收集理解为一种归约，其操作是拼接（concatenation）。当然，归约对理解全归约（all reduce）很重要。

---

So let me pause there. Those were just the warm ups. Just in case people have any questions about what a collective operation is, broadcast, scatter, gather, reduce. Yeah? [INAUDIBLE] NumPy, where is it? So the question is, is this related to broadcasting and NumPy? I mean, I think it's conceptually the same idea, where you have one thing that goes to many things. Like in NumPy, if you have a scalar, get broadcast to a tensor. But the instantiation, this is for collective communication. So it's a bit different.

让我在这里暂停一下。以上只是热身。以防大家对集合操作（广播、散射、收集、归约）还有疑问。嗯？[听不清] NumPy 中的 broadcasting？问题是：这和 NumPy 中的 broadcasting 有关系吗？我认为概念上是一样的——一个东西扩展到多个东西。比如在 NumPy 中，如果你有一个标量，可以广播（broadcast）到一个张量。但具体实现上，这里是用于集合通信（collective communication），所以有点不同。

---

So let's move on to something more interesting. So all gather is what you do to-- basically, you perform gather to all ranks, not just rank 0. So remember what gather does. It basically takes all the different pieces and it just puts it on one rank, rank 0. And now all gather just does it for every single rank. That's what the all is for. All means do it for all the output to all the ranks, and gather is what you're doing to all the ranks. So this is going to come up a bunch. It's not important that you understand this statement precisely, but later we'll see that each rank holds part of the parameters. And then what you need to do is all gather the parameters to get the full parameters for the full forward pass. So in general, as we're doing training, we're going to see a lot of this gather to do something and then scatter and then gather and scatter again.

让我们进入更有意思的部分。全收集（all gather）就是——基本上，你对所有 rank 执行收集操作，而不仅仅是 rank 0。记住收集是做什么的：它把所有的碎片放到一个 rank（rank 0）上。而全收集则是对每一个 rank 都做这件事——这就是"全"（all）的含义。"全"意味着输出到所有 rank，而"收集"就是你对所有 rank 做的事情。这个操作会反复出现。你不需要现在就把这句话理解透彻，但稍后我们会看到每个 rank 持有部分参数，你需要全收集这些参数来获得完整参数以进行完整的前向传播。总的来说，在训练过程中，我们会看到大量这种"收集做某事、再散射、再收集、再散射"的模式。

---

So reduce scatter is performing reduce on each dimension and then scattering the results. So let's say you have four devices and each of them has some vector. And so when we did a reduce before, we just had 0123, and that got reduced to 6. But now reduce scatter says that for each component of this tensor, I'm going to do a reduction, and then I'm going to put it on a different rank. So the first dimension, I'm going to add these up, I get 6. Now, for the second dimension, I'm going to add these up. I get 10. For third dimension, I'm going to process these. For the fourth dimension, I'm going to process those. So where this is going to show up, just to foreshadow things, after the backward pass, when you sum what you're going to do is each GPU will be dealing with different data. And what you're doing is you need to sum all of the gradients from the different shards. And then you're going to redistribute this storage.

归约-散射（reduce scatter）是对每个维度执行归约，然后将结果散射出去。假设你有四个设备，每个设备上有一个向量。之前我们做归约时，只是把 [0,1,2,3] 归约为 6。但归约-散射是说：对于张量的每个分量，我做一个归约，然后把它放到不同的 rank 上。所以第一个维度，我把这些加起来得到 6；第二个维度，加起来得到 10；第三个维度，处理这些；第四个维度，处理那些。这个东西会出现在哪里呢——提前剧透一下——在反向传播之后，你需要做什么呢？每个 GPU 处理的是不同的数据，你需要把所有来自不同分片的梯度求和，然后重新分配存储。

---

And then finally, all reduce. If you understand reduce scatter and all gather, it's basically you do one and then you do the other. So what this does is reduce scatter, the same input as we had before. And remember, in reduce scatter, we had 6, 10, 14, and 18 sit on different ranks. And the all gather part of all reduce just puts them all on the same-- everything on the same node. So all reduce is in some sense the easiest to understand. You have a bunch of tensors. You reduce, in this case, sum. And then you replicate them on all the nodes. So we're going to see this one actually first when we do a data parallel where we sum the gradients and then we replicate the full parameters. So that's where we're actually going to start. So maybe just focus your attention on all reduce. Later, we're going to see how to get to fancier things like 0 or FSDP. We need to break the all reduce into reduce scatter and all gather, because then you can intervene and you can manage things a bit more. But for the basic version, all reduce is fine.

最后是全归约（all reduce）。如果你理解了归约-散射和全收集，那么全归约基本上就是先做前者、再做后者。全归约做的事情是：对相同的输入做归约-散射——记住，在归约-散射中，6、10、14、18 分别位于不同的 rank 上——然后全归约中的全收集部分把这些值放到同一个节点上。所以全归约在某种意义上是最容易理解的：你有一堆张量，做归约（这里是求和），然后在所有节点上复制结果。当我们做数据并行（data parallel）时，我们会首先看到这个操作：对梯度求和，然后复制完整的参数。所以我们从那里开始。你可能只需要把注意力放在全归约上。稍后我们会看到如何得到更高级的东西，比如 ZeRO 或 FSDP。我们需要把全归约拆成归约-散射和全收集，因为这样你就可以介入其中，做更精细的管理。但对于基础版本，全归约就够了。

---

Finally, all to all. This one is, in some ways, the most general. You basically specify how each rank sends a particular message to another rank. And so here's a simple example where you have the same input as before. And what this is saying is that I want to send 0 to this element to rank 0, meaning keep it myself. I'm going to send one to rank 1, two to rank 2, and three to rank 3. And then if I'm rank 1, I want to send four to rank 0, five to rank 1, six to rank 2, and seven to rank 3. So basically, the position here is going to denote which rank is going to be the ultimate destination. And so if you look at the output, what happens is that the first rank is going to receive everyone who sent everything in column 0, because all these ranks are sending these things to rank 0. Similarly, for rank 1, all of the ranks are sending this column to rank 1, and so on and so forth.

最后是全到全（all to all）。这在某种程度上是最通用的操作。你基本上指定了每个 rank 如何向其他 rank 发送特定的消息。这里有一个简单的例子，输入和之前一样。意思是：我想把元素 0 发送给 rank 0（也就是留给自己），把 1 发送给 rank 1，把 2 发送给 rank 2，把 3 发送给 rank 3。然后如果我是 rank 1，我想把 4 发送给 rank 0，5 发送给 rank 1，6 发送给 rank 2，7 发送给 rank 3。所以基本上，这里的列位置标示了最终目的地是哪个 rank。因此如果你看输出，第一个 rank 会收到所有 rank 发送给列 0 的所有东西——因为所有 rank 都把列 0 的内容发送给了 rank 0。类似地，rank 1 会收到所有 rank 发送给列 1 的内容，以此类推。

---

So this is going to be useful when for training MOEs. And the intuition here is that each rank has both a split of the data and also a subset of experts. And basically, and the key idea of the MOE is that it's dynamic routing. You have to look at your data to figure out which experts you need to route those activations to. So it ends up being a all to all communication. So if everything were balanced, meaning that every rank sent the same number of bytes to every other rank, then all to all, you can think about it as essentially a transpose. If you think about this as a matrix, all you're doing is transposing that matrix. But in general, all to all also handles unbalanced splits. And I'm not showing this here, but you can configure it to send any number of bytes to any other rank. But in general, you want the splits to be as balanced as possible. So remember [INAUDIBLE] MOE lecture where we had load balancing to make sure that things were as balanced as possible. So morally, the ideal goal is to have all to all look kind of like this.

这在训练 MoE 时很有用。这里的直觉是：每个 rank 既有数据的一部分，也有一组专家的子集。MoE 的核心思想是动态路由（dynamic routing）——你必须查看数据，以确定需要将这些激活值路由到哪些专家。所以最终变成了全到全通信。如果一切是均衡的（balanced），即每个 rank 向每个其他 rank 发送相同数量的字节，那么全到全基本上可以看作一个转置（transpose）。如果你把它看作一个矩阵，你做的就是在转置这个矩阵。但一般来说，全到全也能处理不均衡的分裂。我这里没有展示，但你可以配置它向任何其他 rank 发送任意数量的字节。不过一般来说，你希望分裂尽可能均衡。回想一下 MoE 课程中的负载均衡（load balancing），就是为了确保事情尽可能均衡。所以从道义上讲，理想的目标就是让全到全看起来像这样。

---

So just to summarize, maybe a few helpful tips to remember the terminology, because I just went through quite a few different operations. So reduce is, well, it's reduced. It performs on some of associative commutative operation. Could be sum, could be max, could be min. Scatter is the inverse gather. Scatter distributes, gather centralizes. And all just means that the destination is all devices. So that explains all reduce and all gather. Let me pause there to take any questions about collective communications.

总结一下，这里有一些记忆术语的小技巧，因为我刚讲了不少不同的操作。归约（reduce）就是对数据做某种结合律和交换律的操作——可以是求和、最大值、最小值。散射（scatter）是收集（gather）的逆操作：散射是分散，收集是集中。而"全"（all）意味着目的地是所有设备。这就解释了全归约和全收集。让我在此暂停，看看关于集合通信有没有问题。

---

Yeah? For operations such as gathering where we basically [INAUDIBLE] to rank 0, does that rank 0 [INAUDIBLE]? Is it a particular GPU every time or can that rank 0 change? Yeah. So the question is when you do a gather or a reduce, the target where you write the output, right now I said rank 0. You'll see later in the code, you basically specify the GPU ID or the rank and it goes there. So it doesn't have to be determined way in advance, but it has to be determined basically when you execute the call.

嗯？对于像收集这样的操作，我们基本上把数据发到 rank 0，那个 rank 0 是固定的吗？每次都是特定的 GPU 吗？还是 rank 0 可以改变？好。问题是：当你做收集或归约时，写入输出的目标位置——现在我说的 rank 0。稍后在代码中你会看到，你基本上指定 GPU ID 或 rank，就写到那里。所以不需要提前很久确定，但基本上在调用执行时就需要确定。

---

Cool. Anything else? Yeah. These are just conceptual building blocks, right? They're not actually [INAUDIBLE]. Are these the actual [INAUDIBLE]? Yeah, so the question is, are these just conceptual building blocks or are they code? So I'm showing these right now as just conceptual building blocks, but we'll very quickly see how these are implemented in code.

好的，还有别的问题吗？嗯。这些只是概念性的构建块，对吧？它们不是实际……这些是否是实际的……？好，问题是：这些只是概念性的构建块，还是代码？我现在展示的是概念性的构建块，但我们将很快看到它们在代码中是如何实现的。

---

So before getting into the code, I want to talk a bit about the hardware, in particular how GPUs are connected, because we already what's inside a GPU. So let's talk about networking in general. So this is a very classic picture. You can tell from this very old looking image that this is how computers, I mean, generally work. So you have this server and then you have a bunch of CPUs. There's a PCIe bus, which you connect things like your-- or used to connect things like your mouse and keyboard. And then you have a bunch of GPUs sitting off of them and you have some RAM. And then this computer is connected to ethernet to another computer, and so on and so forth. So this is a particular setup. It's a particular topology. And GPUs on the same node, you use PCIe to communicate and GPUs on different nodes, you have to go all the way through ethernet. So this is like if you bought your gaming GPU and you had hooked it up with your friend and was like, I'm going to train some big model. That's what you would have to do. But if you're really serious about training, then things look more like this.

在进入代码之前，我想谈谈硬件，特别是 GPU 是如何连接的——因为我们已经了解了 GPU 内部是什么。让我们一般性地讨论一下网络。这是一幅非常经典的图。从这张看起来很老的图片可以判断，这就是计算机的一般工作方式。你有一台服务器，里面有一堆 CPU。有一条 PCIe 总线，你连接东西比如——或者说曾经用来连接鼠标和键盘之类的东西。然后你有一堆 GPU 挂在上面，还有一些 RAM。然后这台计算机通过以太网连接到另一台计算机，等等。这是一个特定的设置，一种特定的拓扑。同一节点上的 GPU 使用 PCIe 通信，不同节点上的 GPU 必须通过以太网通信。这就像你买了自己的游戏 GPU，然后和你的朋友连起来，说"我要训练一个大模型"——那你就要这样做。但如果你真的认真要做训练，事情看起来更像这样。

---

This is the picture I showed in the very beginning where you have the GPU and there's something called NVLink and NVSwitch and InfiniBand. So the typical setup is this. And these numbers, eight is typical, but this 256 is kind of made up. So typically, you have eight GPUs per node. And these are connected via NVIDIA's NVLink to a switch. And just for calibration, if you use NVLink 5, then you're getting 1.8 terabytes per second of total bandwidth. And remember, HBM for B200 was 8 terabytes per second. So it's about 4x slower. So I mean, this is still pretty fast if you think about going between devices, but obviously, not as fast as high bandwidth memory, which is much slower than shared memory or L1 cache. So basically, NVLink connects to the switch, which means that from a programming perspective, you can think about GPUs as connected to any other GPU. You go GPU to any other GPU, and the hardware takes care of transmitting that to the switch, and the switch routes it.

这是我在最开始展示的图：你有 GPU，还有叫做 NVLink、NVSwitch 和 InfiniBand 的东西。典型的设置是这样的。这些数字——8 是典型的，但 256 是我编的。通常每个节点有 8 个 GPU，它们通过 NVIDIA 的 NVLink 连接到一个交换机。作为参照，如果你使用 NVLink 5，总带宽为每秒 1.8 TB。记住，B200 的 HBM 带宽是每秒 8 TB——所以 NVLink 大约慢 4 倍。不过，考虑到这是在设备之间传输，这仍然相当快，但显然不如高带宽内存快（而 HBM 又比共享内存或 L1 缓存慢得多）。基本上，NVLink 连接到交换机，这意味着从编程角度看，你可以认为每个 GPU 都可以连接到任何其他 GPU。从一个 GPU 到任何其他 GPU，硬件会处理到交换机的传输，由交换机路由。

---

So typically, what you will also have is that at some point, you can't have NVSwitch and NVLink. Because as your number of GPUs grows, then you're going to have to put these nodes into pods, which are connected by InfiniBand. And the way InfiniBand works is that now there's a bit more the-- so now the GPU doesn't connect directly to another GPU. It has to go through PCIe and goes through this kind of special InfiniBand cable. And you see that the speeds are much, much lower. And then finally, if you run out of InfiniBand and you have these huge pods, then you need to connect them via ethernet. And in ethernet, you have to go through PCIe and that actually goes through the CPU, which as we'll see, is even slower. So it's kind of analogous to the kind of memory situation. The more nodes you have, then the slower it's going to be. You can't have an NVSwitch handling 100,000 GPUs.

通常情况下，到了一定规模，你就不能用 NVSwitch 和 NVLink 了。因为随着 GPU 数量增长，你需要把这些节点放进由 InfiniBand 连接的 Pod 中。InfiniBand 的工作方式稍有不同——GPU 不再直接连接另一个 GPU，它必须经过 PCIe，再经过一种特殊的 InfiniBand 线缆。可以看到带宽要低得多。最后，如果你连 InfiniBand 都不够用了，还有这些巨大的 Pod，你就需要通过以太网连接。在以太网中，你必须经过 PCIe，而且实际上还要经过 CPU——我们将会看到，这甚至更慢。所以这有点像内存的情况：节点越多，速度越慢。你不可能用一个 NVSwitch 处理 100,000 个 GPU。

---

So one note is that I alluded to this bypassing the CPU, which is going to be an important thing from a hardware perspective. So if you have traditional ethernet, what happens is that the GPU has to talk to the CPU to get its data copied. So it basically has to copy the data to this. The CPU has a kernel socket buffer. Here kernel means not the GPU kernel, but the CPU, traditional notion of a kernel. And then it has to build some network packets, copy to the network interface, and then ship it over. So this generally introduces a lot of latency. And so there's this technology called Remote Direct Memory Access, RDMA, which allows a GPU to directly write or read from another GPU's memory without using the CPU at all. So obviously, if you're in NVLink land and NVSwitch land, then you have RDMA. InfiniBand also supports RDMA. So if you're connected via InfiniBand, then you can directly have GPUs connect to each other without involving the CPU. But standard ethernet does not.

我提到过"绕过 CPU"，从硬件角度看这很重要。如果你使用传统以太网，GPU 必须通过 CPU 来复制数据。它基本上要把数据复制给 CPU，CPU 有一个内核套接字缓冲区（kernel socket buffer）——这里的"内核"不是 GPU 内核，而是 CPU 的传统内核概念——然后构建网络包，复制到网络接口，再发送出去。这通常会引入大量延迟。所以有一种技术叫做**远程直接内存访问**（Remote Direct Memory Access, RDMA），它允许一个 GPU 直接写入或读取另一个 GPU 的内存，完全不需要经过 CPU。显然，如果你在 NVLink 和 NVSwitch 领域，你就有 RDMA。InfiniBand 也支持 RDMA。所以如果你通过 InfiniBand 连接，GPU 可以直接互连，无需 CPU 参与。但标准以太网不支持。

---

There's two notable advancements I will mention. So NVIDIA has been really pushing the limits on what you can do with larger and larger pods. So they have four of basically the B200's and the B300's. They have something called NVL72, which means that they have these trays of eight GPUs but have nine of them. And so basically, at the end of the day, you have 72 GPUs that are all kind of NV switched into one NVLink domain. And if you remember, the NV link speeds are very fast. So normally, if you're mortal, you think, well OK, I have eight GPUs that are interlinked really fast. And then outside of that, then things get slowed down a lot. But if you have a lot of money, you can buy this really fancy hardware and you can get really fast interconnects up to 72 GPUs.

我会提到两个值得一提的进展。NVIDIA 一直在推动更大 Pod 的极限。他们有基于 B200 和 B300 的四代产品。他们有一个叫 NVL72 的东西，就是说他们有这些 8 个 GPU 一组的托盘（tray），一共 9 组。所以基本上，你有 72 个 GPU，全部通过 NVSwitch 连接到一个 NVLink 域中。还记得 NVLink 速度非常快。正常情况下，普通人会想：好，我有 8 个 GPU 互联得很快，超出这个范围就慢很多。但如果你有很多钱，你可以买这种非常高档的硬件，从而实现高达 72 个 GPU 的高速互联。

---

And the other thing I'll mention is that I said standard ethernet doesn't support RDMA, but there has been progress on the ethernet front as well. So there's something called RoCE, RDMA over converged ethernet, where the ethernet actually bypasses the CPU. And this is sort of their answer to InfiniBand. So InfiniBand generally is very expensive, as is a lot of NVIDIA products. But you can get pretty good performance by using RDMA over converged ethernet. And Meta had some paper showing that they were exploring this. So [INAUDIBLE] may or may not have been trained over converged ethernet.

另一个我要提到的是：我之前说标准以太网不支持 RDMA，但以太网方面也有进展。有一种叫 RoCE——基于融合以太网的 RDMA（RDMA over Converged Ethernet），其中以太网实际上绕过了 CPU。这可以看作是对 InfiniBand 的回应。InfiniBand 通常非常昂贵（NVIDIA 的很多产品也是如此）。但通过使用基于融合以太网的 RDMA，你可以获得相当不错的性能。Meta 有一篇论文展示了他们正在探索这个方向。所以[某个模型]可能是在融合以太网上训练的，也可能不是。

---

So that's just a brief overview of what the hardware looks like. You have GPUs. They're connected via NVLink to NVSwitch over some domain, maybe 8, maybe 72. And then it's InfiniBand from there. And now let's talk about how do you program this. So at the very lowest level, there's something called the NVIDIA Collective Communications Library, NCCL or "nickel," which translates the collective operations, the all reduce, reduce broadcasts, into the actual low level packets that are sent between GPUs. So what a NCCL does is when you use NCCL, it's basically like saying, I want to all reduce. And then NCCL goes and figures out what is the topology of the hardware, figures out the path between different GPUs, and then it actually launches the GPU kernels to send and receive data. Because at the end of the day, remember, everything that runs on a GPU is a kernel. So there are communication kernels as well that actually do communication with other GPUs. So we're not going to look too much more into NCCL, but just know that it exists.

以上就是对硬件概况的简要介绍。你有 GPU，它们通过 NVLink 连接到 NVSwitch，覆盖一个域（可能是 8 个，也可能是 72 个）。然后从那里开始使用 InfiniBand。现在让我们来谈谈如何编程。在最底层，有一个叫 NVIDIA 集合通信库（NVIDIA Collective Communications Library, NCCL）的东西，它把集合操作（全归约、归约-广播等）转化为 GPU 之间实际发送的低层级数据包。当你使用 NCCL 时，基本上就是说"我要做全归约"，然后 NCCL 去弄清楚硬件的拓扑结构，找出不同 GPU 之间的路径，然后启动 GPU 核函数来发送和接收数据。因为归根结底，在 GPU 上运行的一切都是核函数——所以也有通信核函数，专门用于与其他 GPU 通信。我们不会深入探讨 NCCL，但要知道它存在。

---

And then we're going to actually go to PyTorch. So maybe before that, any questions about hardware? Yeah. Can you describe-- there's a rack and a tray. Can I describe physically a rack and a tray, like what a rack is and what a tray is? So for the NVL72, so I'm not a hardware expert, but a rack, I mean, is literally, I mean, you've seen data centers, literally a rack. And each tray is something that has-- so the G stands for a [? great. ?] So there's two CPUs. And each CPU is connected to four GPUs. So each tray has eight GPUs on it. And they're stacked and everything is connected to this NVSwitch.

然后我们就要进入 PyTorch 了。在那之前，关于硬件有疑问吗？嗯。你能描述一下——有机架（rack）和托盘（tray）。我能从物理上描述一下机架和托盘是什么吗？对于 NVL72——我不是硬件专家——但机架就是字面意思，你见过数据中心里的那种机架。每个托盘上有——所以 G 代表……有两个 CPU，每个 CPU 连接四个 GPU。所以每个托盘上有 8 个 GPU。它们堆叠起来，所有东西都连接到这个 NVSwitch。

---

Yeah. [INAUDIBLE] Yeah, so the question is, what is the difference between [INAUDIBLE]. [INAUDIBLE] Yeah. So RDMA, you can think about it as more of a desiderata. RDMA means that one GPU can read and write from another GPU's memory. And there's multiple ways to do RDMA. One is to use NVLink and NVSwitch and another way is to use InfiniBand. So InfiniBand and NVSwitch and NVLink are more the hardware, what pieces, what cables and switches are there. And RDMA is more operation, what happens when you're communicating.

嗯。[听不清] 好，问题是……RDMA 和……有什么区别？RDMA 你可以把它看作一种需求规格。RDMA 意味着一个 GPU 可以从另一个 GPU 的内存中读写。有多种方式实现 RDMA：一种是使用 NVLink 和 NVSwitch，另一种是使用 InfiniBand。所以 InfiniBand、NVSwitch 和 NVLink 更偏向硬件——有什么部件、线缆和交换机。而 RDMA 更偏向操作——通信时发生了什么。

---

[INAUDIBLE] Yeah. For example, this [? advancement ?] RDMA over converged ethernet is another way to do RDMA.

[听不清] 嗯，比如基于融合以太网的 RDMA 是另一种实现 RDMA 的方式。

---

[INAUDIBLE] Yeah? Is NCCL optimized for multi-node clusters? Because obviously, it seems intuitive [INAUDIBLE]. But for RDMA based processes, would NCCL be optimal for that? So the question is, is NCCL optimized for multi-node clusters? So I don't know the details of how they have or have not optimized it. All I can say is that NVIDIA has been basically optimizing their entire stack for inference and training of these large models, because their main customers are the major providers of language models. So I would be surprised if they haven't thought of optimizing for those type of workloads.

[听不清] 嗯？NCCL 是否为多节点集群做了优化？因为显然这很直觉……但对于基于 RDMA 的进程，NCCL 是否是最优的？问题是 NCCL 是否为多节点集群做了优化？我不清楚他们具体如何优化的细节。我只能说，NVIDIA 基本上一直在优化他们整个软件栈，用于这些大模型的推理和训练——因为他们的主要客户是各大语言模型提供商。所以如果他们没有考虑针对这类工作负载做优化，我会很惊讶。

---

[INAUDIBLE] Yeah? [INAUDIBLE] So the question is, what happens if you have nine GPUs? How do you distribute the workload across those? I guess it kind of depends on how the nine lands in your setup. For example, a lot of times you'll have-- let's say you have eight GPUs per node. So then the ninth one would be on a different node. And if you don't have NVLink connecting them, then that's going to be really bad, because that's going to be one node which is not providing that much compute and also very expensive to communicate with. But if you, let's say, had everything were connected by NVSwitch, then it would be much more reasonable.

[听不清] 嗯？问题是你如果有九个 GPU，如何在其间分配工作负载？我想这取决于九个 GPU 在你的设置中如何分布。比如很多时候——假设每个节点有 8 个 GPU——那第九个就在另一个节点上。如果没有 NVLink 连接它们，那就很糟糕——因为那个节点提供的计算不算多，而且通信成本很高。但如果所有 GPU 都由 NVSwitch 连接，那就合理得多。

---

One more question and I'm going to move on. So how is this different from TPUs? So [INAUDIBLE] described TPUs a bit more. So I mean, let's see. What can I say quickly about this? So TPUs are generally much simpler objects. I'm not too familiar with the details of what each of these components corresponds to, but maybe we can talk about it offline.

再一个问题我就继续了。这跟 TPU 有什么区别？[某人] 对 TPU 描述得多一些。让我想想，我能快速说点什么？TPU 通常是简单得多的对象。我对每个组件的对应细节不太熟悉，但我们可以课后讨论。

---

So let's actually get down to some code to take advantage of this hardware. So PyTorch conveniently has a torch distributed library that provides a clean interface into these collective operations. So you don't have to explicitly think about NCCL. And in fact, this library also supports different backends for different hardware. So if you are on GPUs, then you would use the NCCL backend. And if you were on CPUs, then there's something called gloo which still allows you to-- like I said, parallel processing has been around for a long time before GPUs. And you can do these collect operations on CPUs as well. This library also supports higher level models and algorithms such as SFTP, but we're not going to use those in the course because we're building things from scratch.

让我们实际看一些利用这些硬件的代码。PyTorch 很方便地提供了 torch.distributed 库，它提供了简洁的接口来调用这些集合操作。你不需要显式地考虑 NCCL。事实上，这个库还支持不同硬件的不同后端。如果你在 GPU 上，就使用 NCCL 后端；如果你在 CPU 上，有叫 gloo 的后端——正如我所说，并行处理在 GPU 出现之前就已经存在很久了——你可以在 CPU 上做这些集合操作。这个库还支持更高级的模型和算法如 FSDP，但我们不会在课程中使用它们，因为我们要从零开始构建。

---

All right. So let's walk through some basic examples of collective operations. So there's this function called spawn, which takes another function I'm going to call, and it says I'm going to run this replicated four times where four is the world size. So let's see what this does. This is actually a wrapper I wrote just to hack around the fact that I can't do multiprocessing in this lecture. So normally what you would do is you call Torch's multiprocessing.spawn and you call the function. But I'm going to do this branch which disables distributed. So let's just go through that. So now I'm in this function that it's supposed to be running asynchronously for each process. So remember, world size is the number of processes and the rank is either 0 or 1 or 2 all the way up to world size minus 1. And so there are world size number of these functions that are each running on a process at the same time.

好，让我们看几个集合操作的基本示例。有一个叫 spawn 的函数，它接收另一个函数并运行——它会把这个函数复制执行四次（四就是 world size）。我们看看这是干什么的。这实际上是我写的一个包装器（wrapper），用来绕过在这节课中不能做多进程的限制。正常情况下，你会调用 Torch 的 multiprocessing.spawn 并传入函数。但我会走另一个分支，禁用分布式。让我们过一遍。现在我在这个函数里，它本应为每个进程异步运行。记住，world size 是进程的数量，rank 是从 0 到 world size 减 1。所以有 world size 个这样的函数，同时在不同的进程上运行。

---

So I'm on rank 0 right now. So what do I do? There's a setup. You basically configure the master address and port. Notice that this is not actually how the GPUs are going to communicate. This is more for general metadata and coordination. The actual data goes through NCCL. Otherwise, it would be very, very slow. And if you have Cuda available, then you can use the NCCL backend. I'm on my laptop, so I'm going to use the gloo backend. OK, so now I'm here. Pretend I have four of these processes running. So there's this barrier function, which is useful as-- it's a synchronization barrier. So basically, if I see this, then it waits for all the processes to get to this point. So basically, you can think about all the processes are running asynchronously. So I don't really control. One could completely finish before the other. They might finish interleaved in any way. So if I want to make sure that there's some code that is executed before other code, I put these synchronization barriers in. So now the downside of putting more barriers in is that, well, you end up kind of waiting potentially unnecessarily.

现在我在 rank 0 上。我该做什么？有一个设置（setup）。你基本上配置主地址（master address）和端口。注意，这并不是 GPU 实际通信的方式——这更多是为了元数据和协调。实际数据走的是 NCCL，否则会非常非常慢。如果你有 CUDA 可用，就使用 NCCL 后端。我在笔记本上，所以我会使用 gloo 后端。好，现在我在位置。假装有四个这样的进程在运行。有一个 barrier（屏障）函数——这是一个同步屏障。基本上，如果执行到这里，它会等待所有进程都到达这个点。你可以认为所有进程都是异步运行的，我没办法控制——一个进程可能在另一个之前完全结束，或者以任意顺序交错完成。所以如果我想确保某段代码在另一段之前执行，就插入这些同步屏障。但多放屏障的坏处是，你可能会不必要地等待。

---

So let's try an all reduce. So I'm going to create this tensor, 0, 1, 2, 3. And I have my rank. Just to make it more interesting, each rank is going to have a different tensor. I'm going to print out what I have before the all reduce. So now I'm going to skip over here and see what gets printed out. So rank 0 before all reduce has 0, 1, 2, 3. Rank 1 has 1, 2, 3, 4, and so on. It's the same example as I showed before. Notice that the print statements are coming in whatever order the hardware feels like it, because it's running async. But all the data is there.

让我们试试全归约。我创建一个张量 [0, 1, 2, 3]。根据我的 rank，为了让事情更有趣，每个 rank 会有一个不同的张量。我打印出全归约之前每个 rank 有什么。现在跳到输出，看看打印了什么。全归约之前，rank 0 有 [0, 1, 2, 3]，rank 1 有 [1, 2, 3, 4]，以此类推——和之前展示的例子一样。注意，打印语句的顺序是硬件随意决定的，因为是异步运行。但所有数据都在那里。

---

So now if I do all reduce, and this you pass in-- this is a PyTorch function. It passes in this tensor. You pass in the reduction operation, which is a sum. And I'm going to say don't do async. And what this does is it calls, in this case, it would be gloo, but it could be NCCL, in which case, it would spin up the Cuda kernels. It would do the communication. It takes care of everything for you. And then it basically writes in place to the data. So after the all reduce, I have the all reduce operation, remember, which is the sum of each of these columns but replicated across all the ranks.

现在如果我做全归约——这是一个 PyTorch 函数。传入这个张量，传入归约操作（这里是求和），并且我说不做异步。这个函数会调用——在这里是 gloo，但也可能是 NCCL——在这种情况下，它会启动 CUDA 核函数，执行通信，一切帮你搞定。然后它基本上就地（in place）写入数据。全归约之后——记住，全归约是每一列的和，但在所有 rank 上复制。

---

So that's all reduce. And if you wanted to be fancier and do async, then you could say async equals true. But then it would screw up all these print statements. So I'm trying to put more barriers than I would normally would. Yeah, question? [INAUDIBLE] So the question is the rank the GPU. For this class, the rank is the GPU.

以上就是全归约。如果你想更高级一点，做异步操作，可以设置 async=True。但那样所有打印语句都会乱掉，所以我放的屏障比平时多。嗯，有问题吗？[听不清] 问题关于 rank 和 GPU 的关系。在这门课中，rank 就是 GPU。

---

So let's try another example here. So I'm going to do a reduce scatter. So here, I'm going to create an input, which is 0 through the world size. And I'm going to have the output. I'm going to allocate the output. And so what does this look like before I do the reduce scatter? It looks like, let's see, this, where it's the same input and the output happens to be zeros, but it could be just anything. And then I do the reduce scatter tensor. Here instead of writing in place, I have an output tensor and an input tensor. I say I want to do the sum and then afterwards, I get basically the input is not touched, but the output I get the reduction of each component written into the respective ranks.

让我们再试一个例子。我来做一个归约-散射。这里我创建一个输入，值从 0 到 world size。然后我分配输出。在归约-散射之前，看起来是怎样的？让我看看——输入相同，输出恰好是零（但也可以是任何值）。然后我执行 reduce_scatter 张量。这里不是就地写入，我有输出张量和输入张量。我说要对求和做归约，然后之后，输入不会被改变，但输出会得到每个分量归约后的结果，写入相应的 rank。

---

So yeah, question? [INAUDIBLE] So the question is, how does it work to do the all reduces asynchronous? So what this means is that this is like a monolithic operation. You say go do the all reduce. And it's spinning up Cuda kernels. It's going to do the communication. And remember, Cuda is already kind of async with respect to the processes, and now we have all the processes being async. And the point is that this code just would return. And then you could do other things. So a typical thing, which I'm not going to talk about this class, is overlapping computation and communication. So for example, you can do this operation, and then you can go ahead and load some other data for the next step, which is independent of this operation. And then when you want to make sure that you actually are done, then you can call a wait or a barrier.

嗯，有问题？[听不清] 问题是：异步的全归约是如何工作的？这意味着它是一个整体操作（monolithic operation）。你调用"去做全归约"，它会启动 CUDA 核函数，执行通信。记住，CUDA 相对于进程来说已经是异步的了，而这里所有进程也都是异步的。关键点是：这段代码会直接返回，然后你可以做其他事情。一个典型的做法是——我这节课不会讲——重叠计算和通信（overlapping computation and communication）。比如，你可以执行这个操作，然后去加载下一步需要用到的其他数据——如果这些数据独立于这个操作。当你需要确认操作确实已完成时，可以调用 wait 或 barrier。

---

So let's do the final one, which is all gather. So by now, I think you get the idea. Here I'm going to set as the input the output of the reduce scatter. I'm going to allocate an output. So before the all gather, it looks like this. I have my results from the reduce scatter here. The output is just allocated. It happens to have some values in it, but don't worry about it. And then after I do the all gather into tensor, and then I will have all the different inputs gathered onto all the different ranks. And you can see here that, indeed, proof via example that all reduce is equal to reduce scatter plus all gather.

让我们做最后一个——全收集。到现在，我想你们应该明白了。这里我把归约-散射的输出作为输入。我分配一个输出。全收集之前，看起来是这样的：我有归约-散射的结果在这里，输出已经分配了（里面恰好有一些值，但别管它）。然后我执行全收集到张量中，之后所有的不同输入被收集到所有不同的 rank 上。你可以看到，这确实通过例子证明了全归约等于归约-散射加全收集。

---

And then just to wrap things up, just as I started by setup, then I clean up, which it's good practice to clean up. So that was your first example of a Torch distributed program.

最后收个尾，就像我以 setup 开始一样，我以 cleanup 结束——做清理是个好习惯。以上就是你的第一个 Torch 分布式程序示例。

---

So let's do some benchmarking. This will be quick, since I want to actually move on to part two. So how fast does communication happen? So let's do an all reduce. So here, I'm going to all reduce with 100 million elements. Oops. Sorry, I messed this up. So all reduce. So I'm going to create this tensor with this number of elements. And remember, just like before when we do benchmarking, we warm up first. And here, I'm going to call the Cuda synchronize and also the barrier, just to make sure that because there's two forms of asynchrony here, the Cuda kernels and the different processes. And just want to make sure everything is kind of not running and is done before I start the time. And I'm going to do the all reduce. And then wait again with the synchronize in the barrier and stop the time. So remember, this is running for every single rank. So if I look at the output, here for rank 0, 2, 1, 3, I have a different time potentially, because they're all different processes. Each of them is going to report a certain measurement. And if you want to report one number, you can take the average, for example.

让我们做一点基准测试（benchmarking）。这会很快，因为我实际上想进入第二部分。通信有多快？我们做一个全归约。这里我用 1 亿个元素做全归约。哎呀，不好意思，搞错了。全归约。我创建这个具有这么多元素的张量。记住，就像之前做基准测试一样，我们先 warm up。这里我调用 CUDA synchronize 和 barrier，以确保——因为这里有两种异步性：CUDA 核函数和不同进程——确保在开始计时之前所有东西都已完成、没有在运行。然后我执行全归约，之后再次用 synchronize 和 barrier 等待，然后停止计时。记住，这对每个 rank 都运行。所以如果看输出，rank 0、2、1、3 可能有不同的时间——因为它们都是不同的进程。每个进程报告一个测量值。如果你想报告一个数字，你可以取平均。

---

So now one thing that is useful to do, which is analogous to when we were computing MFU, is to measure the effective bandwidth. And the idea here is that, well, this took 1.6 milliseconds. How much-- is that good or bad? So to compute the effective bandwidth, what we're going to do is to compute essentially how many bytes were sent and should be sent during this computation. And then if you divide by the total time, then you get the effective bandwidth. So the size of what I'm sending around is the size of each element times the number of elements. So that's basically the number of bytes of this data tensor. How many bytes get actually sent? So this needs some unpacking. So for all reduce, if you think about, let's just say for simplicity, you do a rank 0 plus rank 1 plus rank 2 plus rank 3. You need to iterate this world size minus 1 steps, because there's a world size minus 1 addition operations. So that's this factor. There's a 2, because you need to both send and reduce. And then you multiply by the size of the payload. So that's the total number of sent bytes. And the total duration is the wall clock time that it took. And then you multiply by the world size, because it's the total amount that all the ranks have waited. And the bandwidth is the bytes sent divided by the total duration. So in this case, you get something like about 400 gigabytes per second.

现在一件有用的事情——类似于我们计算 MFU 时——是测量有效带宽（effective bandwidth）。思路是：这花了 1.6 毫秒——这算好还是坏？为了计算有效带宽，我们计算在通信过程中发送了多少字节。如果你的总时间，就得到有效带宽。我发送的东西的大小是每个元素的大小乘以元素数量——基本上就是数据张量的字节数。实际发送了多少字节？这需要解释一下。对于全归约，简单来说，你做了 rank 0 + rank 1 + rank 2 + rank 3。你需要迭代 world size 减 1 步——因为有 world size 减 1 次加法操作。这是其中一个因子。还有一个 2，因为你既要发送也要归约。然后乘以有效载荷（payload）的大小——这就是发送的总字节数。总持续时间是墙上时钟时间。然后乘以 world size，因为这是所有 rank 等待的总时间。带宽是发送的字节数除以总持续时间。在这个例子中，你得到大约每秒 400 GB。

---

So a few notes here. One is that the effective bandwidth, if you look at this expression, size times 2 times world size minus 1 divided by world size times duration. So as world size increases, this world size minus 1 divided by world size essentially converges to 1. So you're effectively left with 2 times the size bytes over the duration. So this is essentially the bandwidth. Notice that this is independent of the world size, which is good. So if you grow the number of GPUs you have, the bandwidth doesn't change. It is also independent of the topology, which is something that kind of NCCL figures out whether you're going to pass the messages in a kind of a ring or a tree topology.

这里有几个要点。有效带宽，看这个表达式：size × 2 × (world size - 1) / (world size × duration)。随着 world size 增大，(world size - 1) / world size 趋近于 1。所以你实际上得到的是 2 × size / duration——这就是带宽。注意这与 world size 无关——这很好。如果你增加 GPU 数量，带宽不变。它也独立于拓扑结构——NCCL 会决定你是以环形（ring）还是树形（tree）拓扑传递消息。

---

So yeah. So that is all reduce. And for reduce scatter, this is very similar. So I'm going to create the inputs and the outputs, warm up, perform the operation, and time it. So notice that the reduce scatter has these timings. And you can also measure the effective bandwidth here, the number of bytes that were in the input. You have the number of bytes that were sent. Here there is no 2x here. And then the total duration, you divide by that, you get the bandwidth. So here, the bandwidth is-- it should be very similar. I guess sometimes there's some stochasticity, but it's in the kind of 400s.

好，这就是全归约。对于归约-散射，非常类似。我创建输入和输出，warm up，执行操作，计时。注意归约-散射也有这些时间值。你同样可以测量有效带宽：输入中的字节数、发送的字节数（这里没有 2x 因子），然后除以总持续时间得到带宽。这里的带宽应该非常相似。我想有时会有一些随机性，但大概在 400 多。

---

So a few notes here. All reduce is, remember, as we stated, reduce scatter plus an all gather. And so all reduce, naturally, is moving twice the amount of data, because reduce scatter has some cost, all gather has some cost, and all reduce is doing twice as much work. And it takes twice the amount of time. But the two cancel out, so you get the same kind of bandwidth.

这里有几个要点。全归约就是归约-散射加全收集。所以全归约自然要移动两倍的数据——归约-散射有成本，全收集有成本，全归约做了两倍的工作。它花了两倍的时间。但两者抵消，所以你得到相同的带宽。

---

So that is the end of part one. Maybe any questions before I move to part two? Yeah. Why did you do that synchronized for [INAUDIBLE]? So why do we have to do the synchronized for the Cuda kernel? So at the end of the day, we are still doing Cuda operations. We have just multiple processes, each with a GPU, doing some Cuda operations. So if you're doing a Cuda operation, remember, by default, it's async. So when you reach the next line in Python, that Cuda operation might not be done. So we need to wait always to make sure it's done by synchronizing.

第一部分到此结束。在我进入第二部分之前，有问题吗？嗯。为什么要对 CUDA 核函数做 synchronize？为什么我们必须为 CUDA 核函数做同步？归根结底，我们仍然在做 CUDA 操作。我们有多个进程，每个进程有一个 GPU，做一些 CUDA 操作。记住，默认情况下 CUDA 操作是异步的。所以当你到达 Python 的下一行时，那个 CUDA 操作可能还没完成。所以我们需要通过同步来确保它完成。

---

[INAUDIBLE] So do you have to do barrier first and then synchronize? I'm not sure. Yeah. [INAUDIBLE] Yeah. I think one problem is if you barrier first and then the Cuda might not be done running, and you just immediately go to the barrier. And then you are still each independently synchronizing the different Cuda kernels, which means that you're not really synchronized. If all those operations just return, the barrier doesn't really do anything.

[听不清] 你需要先做 barrier 再做 synchronize 吗？我不确定。嗯。我认为一个问题是：如果你先做 barrier，而 CUDA 可能还没跑完，你直接进入 barrier，然后你仍然各自独立地同步不同的 CUDA 核函数——这意味着你并没有真正同步。如果所有这些操作都只是返回，barrier 实际上不做任何事情。

---

OK, let me move on. So now let's actually start thinking about how you train models. So we're just going to walk through a very bare bones implementation of training MLPs, multilayer MLPs. I guess that's redundant. It's multilayer perceptrons already. And remember that MLPs are the ones that are the actual compute bottleneck in the transformer. So this is actually pretty representative of what you'll see. So data parallelism, tensor parallelism, and pipeline parallelism. And the picture I want you to have in your head is this picture. So this is a little bit of a schematic, so don't think too deeply about this, but it's more of a way to conceptualize how you're cutting your data and parameters.

好，让我继续。现在让我们真正开始思考如何训练模型。我们将非常粗略地实现训练 MLP（多层感知机）——我猜说"multilayer MLP"有点重复，因为 MLP 已经是多层感知机了。记住，MLP 是 Transformer 中实际的计算瓶颈。所以这实际上非常代表你会遇到的情况。三种并行方式：数据并行（data parallelism）、张量并行（tensor parallelism）和流水线并行（pipeline parallelism）。我希望你们脑海中有这样一幅图。这是一张示意草图，所以不用深究，它更多是帮助你概念化如何切割数据和参数。

---

So data parallelism says, I'm going to split the data into pieces. And then each of the GPUs is going to be responsible for part of the data, and I'm going to just do normal-- I'm going to keep track of all the parameters and do normal model training. And then I need to synchronize. So let me explain how this works. So I'm going to generate some sample data. So there's a batch size of 128. Number of dimensions, 1,024. So this is a batch size by num dim matrix, data matrix. And let's jump into this data parallelism.

数据并行说：我要把数据拆分成片段。每个 GPU 负责一部分数据，我像正常一样——跟踪所有参数，做正常的模型训练——然后我需要同步。让我解释这是如何工作的。先生成一些示例数据：批大小（batch size）为 128，维度数（num dim）为 1024。所以这是一个批大小 × 维度数的数据矩阵。让我们跳进数据并行。

---

So the way that it's going to work is that you have this data matrix. And I'm going to break up the rows into world size pieces. And in this case, four. And each rank is going to get a piece. So the number of dimensions, the batch size. So I'm going to call the local batch size, basically the batch size divided by the world size, which is every row that GPU sees, it's going to have 32 data points. And this is just indexing. Start index data start to end gets you the slice of that data. And I'm going to just put it on that rank. So at this point, each GPU has now a distinct data tensor, which is the part that they're responsible for. Now, in practice, each rank should probably load its own data rather than have this bottleneck, but this is just for illustrative purposes.

它的工作方式是：你有一个数据矩阵。我把行按 world size 切分——这里是四份。每个 rank 得到一份。我把本地批大小（local batch size）定义为批大小除以 world size——每个 GPU 看到的数据有 32 个数据点。这通过索引实现：start index 到 end index 得到数据的切片。然后我把它放到那个 rank 上。到这里，每个 GPU 有一个不同的数据张量，就是它们各自负责的部分。在实践中，每个 rank 应该自己加载数据，而不是有这个瓶颈（bottleneck），但这只是示意用途。

---

So let's instantiate the MLP. So here, I assume we have layers. And num layers. And for each of the layers, I'm going to have just a num dim by num dim matrix. So I'm just going to initialize a random set of parameters. And then I'm going to feed that into optimizer. So here's the training loop. So in the forward pass, I take the data. So remember, data is not all the data. It's just if I'm rank 2, then I only get B2 part of the data. I'm going to just go through the number of layers and do a forward pass. And then I'm going to do a backward pass. And then normally, this would be it. But now, remember, every rank has different data. Therefore, the gradients are going to be different as well. So this is the key step that makes data parallelism work. We're going to synchronize the gradients across all the workers. This is the only difference between standard training and DDP. It's actually pretty nice and elegant.

让我们实例化 MLP。这里我假设有 layers 和 num layers。对每一层，我有一个 num dim × num dim 的矩阵。我随机初始化一组参数，然后喂给优化器（optimizer）。这是训练循环。在前向传播中，我取数据——记住，数据不是全部数据，如果我是 rank 2，我只有 B2 那部分数据。我遍历所有层做前向传播，然后做反向传播。正常情况下这就完了。但现在，每个 rank 有不同数据，因此梯度也不同。这就是使数据并行工作的关键一步：我们在所有 worker 之间同步梯度。这是标准训练和 DDP 之间的唯一区别。实际上非常漂亮和优雅。

---

So basically, for all the parameters, I'm going to do an all reduce of param.grad. And I'm going to average. And then after this all reduce is done, then now at this point, each of the ranks has the exact same gradients. And then I'm just going to update the parameters. So it's kind of really elegant, I find, because it's basically standard training where you apply it to your local batch, but you just insert this after the backward pass. Let's just average all the gradients via this all reduce. It's a one line code change, and then the parameters get updated. So as you're training, each rank is basically performing parameter updates as if it had all the data on it, but it's only actually processing a part of the data. So that's basically DDP or the first type of data parallel.

基本上，对于所有参数，我对 param.grad 做全归约，然后取平均。全归约完成后，每个 rank 都有完全相同的梯度。然后我更新参数。我觉得这非常优雅——本质上就是标准训练，应用到你的本地批次上，但只需在反向传播之后插入这一行代码：通过全归约平均所有梯度。这是一行改动，然后参数就被更新了。所以训练时，每个 rank 执行参数更新，就像它拥有了所有数据一样，但实际上它只处理了一部分数据。这就是 DDP，或者说是第一种数据并行。

---

Any questions about this? Yeah. [INAUDIBLE] So the question is, can you only do this with batch size greater than 1? Yes. So your batch size has to be at least world size for this to really make sense. And usually, it should probably be quite a bit larger. Yeah? [INAUDIBLE] Yeah. So the question is, should the batch size be a multiple of world size? And that also would be nice. Yes. I mean, if it's not, then you can pad it with zeros or something. So there's ways, but it's just easier for everyone if it is.

关于这个有问题吗？嗯。[听不清] 问题是：这只在批大小大于 1 时才能做吗？是的。你的批大小至少需要等于 world size 才有意义。通常还应该大得多。嗯？[听不清] 是。问题是：批大小应该是 world size 的倍数吗？那也会很好。是的，如果不是，你可以用零填充之类的。有办法处理，但如果正好是倍数对大家都容易。

---

[INAUDIBLE]? What would it look like for a transform-based [INAUDIBLE]? Yeah, so the question is, what would this look like for a transformer? It would actually be basically the same. The DDP has the nice thing that is very modular. You do the forward pass. I mean, DDP just averages the parameters here. It doesn't care what your forward pass looks like.

[听不清] 对于基于 Transformer 的……会是什么样子？好，问题是：对于 Transformer，这会是什么样子？实际上基本一样。DDP 的好处是非常模块化（modular）。你只管做前向传播——DDP 只是平均参数，它不关心你的前向传播长什么样。

---

OK, let me move on. So that's DDP. So just to summarize, the losses are different across the ranks. The gradients are also initially different. But they are all reduced to be the same across the ranks. And therefore, the parameters all remain the same across ranks.

好，让我继续。以上就是 DDP。总结一下：不同 rank 的损失（loss）不同，梯度最初也不同。但它们被归约为所有 rank 相同。因此，所有 rank 上的参数也保持一致。

---

So next lecture, [? Tatsu ?] is going to talk about fancier data parallelism, FSDP and ZeRO. And the idea there is, as I've alluded to, here we use all reduce. It's a very simple monolithic operation, but it does require holding all the models, parameters in memory. But what if the model parameters don't fit in memory? Then you're going to have to be more clever, and that's the topic for the next class.

下次课，Tatsu 将讨论更高级的数据并行——FSDP 和 ZeRO。其思路是——正如我暗示过的——这里我们用了全归约，这是一个非常简单的整体操作，但它要求把所有模型参数都放在内存中。但如果模型参数放不进内存呢？那你就得更聪明一些——这就是下节课的主题。

---

So let me talk about tensor parallelism. So here, the idea is we're going to cut this way and we're not going to cut the data. We're going to cut essentially each layer. And so each rank is going to get part of each layer. And generally, this means that we're going to have to transfer a lot more data. We'll discuss this a bit later.

让我谈谈张量并行。这里的思路是：我们从这个方向切割，我们不切割数据，而是切割每一层。每个 rank 得到每层的一部分。一般来说，这意味着我们需要传输更多的数据。我们稍后会讨论这一点。

---

So what does tensor parallel look like? So we're just going to assume we have this data. Every rank has all the data just for simplicity. And here, remember, the data is batch size times num dim. And I'm going to define a local num dim dim to be-- for this rank, I only am responsible for a subset of the dimensions. So the picture here is that each model still has all the layers here for all the layers, but the parameters now are num dim times local num dim. So if this were one of the parameter matrices for one layer, I would be splitting down the columns. So this is also known as column tensor parallel. You can also do it by rows, but we're not going to talk about that right now.

张量并行是什么样子的？我们假设有这个数据，简单起见每个 rank 都有全部数据。记住，数据是批大小 × 维度数。我定义 local num dim——对于这个 rank，我只负责维度的子集。这里的画面是：每个模型仍有所有的层，但参数现在是 num dim × local num dim。如果这是一个层的参数矩阵，我是按列切分的。这也被称为列张量并行（column tensor parallel）。你也可以按行切分，但我们不会讨论那个。

---

So now what does the forward pass look like? So I'll go through all the layers and I'm going to compute activations. So I start with x the data. And I'm going to access the parameters at layer. And notice that this is only a slice of the parameters. So if I'm on rank 1, I only get this part of the matrix. But I can still proceed. I can apply this non-linearity, because this is element wise anyway. But now what I'm going to do is I'm going to communicate activations. So if I have a data matrix, rank 1 has activations for part of the activations for this part of the matrix. Rank 1 has part of the activations for this matrix and so on and so forth. And I need to basically put all the activations on all the ranks. But we know how to do that. We introduced all gather as a collective primitive. So this is all the activations. So this is the batch size times local num dim, which is the shape of the activations. And then I'm doing an all gather. Sorry, so this is the allocating memory for the activations. So x is the actual part of the activation. So this is batch size times local num dim. And all gather says each rank has x and each rank is going to allocate activations, which is a list, one for each world size. And then after the all gather, x is going to be copied into each of the respective location activations. So then once I gather all the activations, I concatenate them to form the full dimensional x, which is batch size times num dim.

那么前向传播是什么样子的？我遍历所有层，计算激活值。我从数据 x 开始，访问该层的参数。注意这只是该参数的一个切片——如果我在 rank 1，我只能得到矩阵的这一部分。但我仍然可以继续。我可以应用非线性（non-linearity），因为这是逐元素操作。但接下来我要做的是通信激活值。如果我有一个数据矩阵，rank 1 有这个矩阵这部分对应的部分激活值，rank 2 有另一部分，等等。我需要把所有的激活值放到所有 rank 上——但我们知道怎么做：我们引入了全收集作为集合原语。所以这是所有激活值。形状是批大小 × local num dim。然后我做一个全收集。抱歉，这是为激活值分配内存。x 是实际的激活值部分——批大小 × local num dim。全收集说每个 rank 都有 x，每个 rank 会分配一个激活值列表，每个 world size 一个。全收集之后，x 被复制到对应位置的激活值中。然后一旦我收集了所有激活值，我将它们拼接（concatenate）成完整的 x，形状是批大小 × num dim。

---

Any questions about column tensor parallel? So this is done for every layer. We now notice one difference between data parallel is now we have to muck around with the model. Data parallel is very elegant, because it's splitting by data. The model is treated as a module. But now we have to muck around with the model. And this is strongly leveraging the fact that if you want to do a matrix multiplication, you can split it up into a set of smaller matrix multiplications. We can do those on different ranks, and then we can gather the results.

关于列张量并行有问题吗？这是对每一层做的。我们现在注意到与数据并行的一个区别：我们不得不插手模型内部。数据并行非常优雅，因为它是按数据切分的，模型被当作一个模块。但现在我们必须修改模型。这充分利用了这样一个事实：如果你想做矩阵乘法，你可以把它拆成一组更小的矩阵乘法——我们在不同的 rank 上做，然后收集结果。

---

When it comes to the back propagation, [INAUDIBLE] gradients are still [INAUDIBLE]. Yeah. So now the question is, what happens in backprop? Now, in the backprop, you have your activations and you have to reduce scatter to all the different gradients. So in some ways, all gather and reduce scatter have this kind of duality, where in forward, you're all gathering, in the backward, you're reduce scattering. Yeah? [INAUDIBLE] So the question is, is that done automatically by autograd? So none of this-- well, OK. So if you just call .backward, it's not going to do it, because there's no parallelism in that. But PyTorch has all these things that are done automatically for you.

在反向传播中，梯度仍然……嗯。问题是：在反向传播中会发生什么？在反向传播中，你有激活值，你需要通过归约-散射来获得所有不同的梯度。所以在某种程度上，全收集和归约-散射具有这种对偶性（duality）：前向时你做全收集，反向时你做归约-散射。嗯？[听不清] 问题是：这是由 autograd 自动完成的吗？嗯。如果你只调用 .backward()，它不会做这个，因为里面没有并行操作。但 PyTorch 有所有这些自动为你完成的方法。

---

[INAUDIBLE] To what extent do I need to change my code and [INAUDIBLE]? So what is done for you and versus automatically? Here we're managing things fairly explicitly, which means I'm not doing the backward pass, but you would have to manage and call the reduce scatter yourself. And that's by design, because this is 336, building language models from scratch. In practice, you probably wouldn't have to do that.

[听不清] 我需要在多大程度上修改代码？哪些是自动帮你做的？这里我们相当显式地管理一切——这意味着我没有做反向传播，但你需要自己管理和调用归约-散射。这是有意为之，因为这是 336——从零开始构建语言模型。在实践中，你可能不需要这样做。

---

OK, so let's do pipeline parallelism quickly. So the idea behind pipeline parallelism is we're going to split the network this way. So each rank is going to get a subset of the layers now. Within each layer, it's going to get all the dimensions, and it's also going to get all the-- well, one of the ranks is going to get all the data. Every rank is going to see all the data in some form. So this is the way it's going to work. So we have all the data, which is, again, the batch size times num dim. And I'm going to split up the layers. So local num layers is going to be the number of layers that a particular rank is going to handle. And so now I'm going to have local params, which is basically only-- there's local number of layers number of them. But within each layer, I'm going to do the num dim by num dim.

好，让我们快速过一下流水线并行。流水线并行的思路是：我们沿这个方向切割网络。每个 rank 得到层的子集。在每个层内部，它得到所有维度。某个 rank 会得到所有数据——每个 rank 都会以某种形式看到所有数据。具体是这样的：我们有全部数据（批大小 × 维度数），然后将层拆分。local num layers 是特定 rank 要处理的层数。所以我现在有 local params——只有 local num layers 个参数。但在每层内部，我还是做 num dim × num dim。

---

So one thing, maybe [INAUDIBLE] will talk more about this on Wednesday, is this idea of micro-batches. So maybe I'll just present this and explain why I'm doing things this way. So in addition to splitting up the layers, I'm also going to split up the batch into a bunch of micro-batches. So if I'm rank 0, then I get the data, and I'm going to chunk it up into a number of micro-batches. And for each micro-batch, what I'm going to do is receive it from the previous rank, and then do the feed forward pass only on the layers that are assigned to this rank. And then I'm going to send to the next rank. So here I'm actually using these receive and send, which are pointwise operations. So I didn't cover those before, but they're fairly explanatory. This basically says I'm rank and I'm going to send this tensor over to-- sorry, I'm going to receive this tensor from rank minus 1. And this says I'm going to send tensor x to rank plus 1.

有一个事情——也许[某人]周三会更多讨论——就是微批次（micro-batches）的概念。所以我先展示这个，并解释为什么我这样做。除了拆分层，我还把批次拆分成多个微批次。如果我是 rank 0，我拿到数据，把它分成若干微批次。对于每个微批次，我从上一个 rank 接收它，然后只在这个 rank 分配的层上做前向传播，然后发送给下一个 rank。这里我实际上用了 send 和 recv——这是点对点操作（pointwise operations）。我之前没讲这些，但它们不言自明。这基本上是说：我是 rank，我要从这个张量……抱歉，我要从 rank minus 1 接收这个张量。然后说我要把张量 x 发送给 rank plus 1。

---

So basically, the reason why I'm talking about micro-batches is-- and [? Tatsu ?] will talk more about this on Wednesday-- is that in pipeline parallelism, so you have one rank that gets the data. It processes some of the layers, and then it sends it to the next GPU, and it process some of the layers. And it then sends it to the next GPU. So this is a very natural way of dividing a deep network. But the problem is that you get these what are called pipeline bubbles, where while you're not processing, you're kind of waiting around for other tensors to process. And this ends up being quite inefficient. So the idea behind micro-batches is that you break it up into smaller batches, so you can process it quickly, send it on to the next one. So this can reduce the number of pipeline bubbles.

我讨论微批次的原因是——Tatsu 周三会更多讨论——在流水线并行中，一个 rank 拿到数据，处理一些层，然后发送给下一个 GPU，它处理一些层，再发送给下一个。这是划分深度网络非常自然的方式。但问题是你得到了所谓的**流水线气泡**（pipeline bubbles）——当你不处理时，你在等待其他张量被处理——这会导致效率低下。微批次背后的思想是将其拆分成更小的批次，这样你可以快速处理，发送给下一个。这可以减少流水线气泡的数量。

---

So the other thing I will mention that is not handled in this very kind of naive version is the idea of overlapping communication and computation, which is actually very important to pipeline parallelism. This basically gives you the right structure. If you put an I before these, then it becomes kind of async. You have to add more things to manage the code. And the idea here is that you want to be-- while you're computing here, you can be receiving data or sending data. So computation and communication should overlap. So that reduces the amount of time you actually spend waiting.

另一个我提到但在这个非常初级版本中没有处理的是重叠通信和计算（overlapping communication and computation）——这对流水线并行非常重要。这基本上给了你正确的结构。如果你在这些前面加上 I（表示异步），它就变成异步的。你需要添加更多代码来管理。这里的想法是：当你在计算时，你可以同时接收或发送数据。所以计算和通信应该重叠（overlap），从而减少实际等待的时间。

---

So a few things that are kind of missing here, which we'll hopefully fill in next time. So the communication versus computation overlap, which is especially crucial in pipeline parallelism. I didn't mention in data parallelism, this also happens, because I just did a forward pass and then at the end, I'm just doing all these all reduces. But if you're clever, then on the backward pass, as soon as the gradients are done, you can start sending that. And that's something that will be explored in the assignment two. And this, again, allows you to just overlap communication and computation more.

这里缺失了一些东西，希望下次课能填补。通信与计算的重叠——在流水线并行中尤其关键。我在数据并行中没有提到，这也会发生——因为我只做了前向传播，然后在最后做所有全归约。但如果你很聪明，在反向传播中，一旦梯度完成，你就可以开始发送它们。这将在作业二中探索。这再次让你能够重叠更多的通信和计算。

---

We had some questions about what about general models. Again, I think this MLP gives you essentially most of what you need for understanding the basics. Some of the larger models just require a lot more bookkeeping, so it's harder to see the core algorithms. There are other types of parallelism that we haven't covered. So sequence parallelism takes a whole sequence and chops it up into pieces. And that allows you to parallelize the attention computation, expert parallelism, which allows you to parallelize the experts for MOEs. And this is where the all to all that I mentioned comes in. And then also different combinations of different parallelization techniques, which also will show up in the assignment.

我们有一些关于通用模型的问题。同样，我认为这个 MLP 基本上给了你理解基础所需的大部分内容。一些更大的模型只是需要更多的记账工作（bookkeeping），所以更难看到核心算法。还有其他我们没有覆盖的并行类型。比如序列并行（sequence parallelism）把整个序列切成片段，允许你并行化注意力计算。专家并行（expert parallelism）允许你并行化 MoE 的专家——这就是我之前提到的全到全的用武之地。还有不同并行化技术的不同组合——这些也会出现在作业中。

---

So one thing to note is that which parallelism technique you choose is going to be strongly dependent on the hardware. For example, tensor parallelism. There's a lot of communication, because for every layer, you need to send all these activations, which are fairly big. So generally, tensor parallelism happens within a node on NVLink or where you have high bandwidth. Whereas you wouldn't do tensor parallelism past an NVLink domain. Whereas a pipeline parallelism, you'll see people using it. And generally, this can tolerate much slower interconnects. So some of the decentralized training work uses pipeline parallel, because your nodes are-- GPUs are halfway across the world. But you wouldn't want to do tensor parallel in that setting.

需要注意的一点是：你选择哪种并行化技术很大程度上取决于硬件。比如张量并行，通信量很大——因为每一层你都需要发送所有这些激活值，它们相当大。所以通常张量并行在节点内、在 NVLink 上或高带宽环境中进行。你不会在超出 NVLink 域的范围做张量并行。而流水线并行，你会看到人们使用它——它通常可以容忍慢得多的互联。所以一些去中心化训练（decentralized training）工作使用流水线并行，因为你的节点——GPU 在地球另一端。但你不会想在那样的场景下做张量并行。

---

So sometimes when you look at these combinations, it will be tensor parallel within a node and then pipe data parallel or FSDP and then pipeline parallelism if you need it. There's other effects, such as if you do data parallel, you might be able to do data parallel quite a bit. But then you start hitting to something called the critical batch size, where if you start increasing the batch size too much, it doesn't actually help you, in which case you're kind of wasting your compute and then you're better off using tensor parallel. So there's a bunch of these considerations, which we'll talk more about as we go through the class.

所以有时当你看到这些组合时，会是：节点内做张量并行，然后做数据并行或 FSDP，如果需要再加流水线并行。还有其他因素：比如如果你做数据并行，你可以做很多数据并行，但然后你会碰到所谓的临界批大小（critical batch size）——如果你把批大小增加太多，它实际上不再有帮助，你就在浪费计算资源，这时你最好改用张量并行。所以有一堆这样的考量，我们会在课程中逐步讨论。

---

So final note. So TPUs came up a little bit. One thing to note is that on purpose, we are using PyTorch and not just using PyTorch, but really using the collective operations in a very primitive way, so you can see mechanically what's happening. Another approach, especially if you're in [INAUDIBLE] TPU land, is that you can simply define the model and the starting strategy. And the compiler actually handles a lot of the decision of how to-- basically, what kind of communication operations you need. You basically say, well, this piece of data needs to be here and here and here. And then the compiler does some magic to figure out what. So that's appealing. But obviously, it would take a lot of the joy out of actually building things from scratch.

最后一点。TPU 被提到了一点。需要注意的一点是：我们特意使用 PyTorch——而且不仅仅是使用 PyTorch，更是以非常原生的方式使用集合操作——这样你就能从机械层面看到发生了什么。另一种方法——尤其是如果你在 TPU 领域——是你只需定义模型和分片策略，编译器实际上处理了很多决策——基本上你需要什么类型的通信操作。你只需要说"这块数据需要到这里、这里和这里"，编译器做一些魔法般的操作来搞定。这很吸引人。但显然，这会剥夺很多从零构建的乐趣。

---

Just to summarize, so there's many ways to parallelize. You can cut by data, cut by tensor or expert, cut by pipeline or sequence. We looked at data parallelism. We only did DDP. Next time we'll do FSDP and ZeRO. Tensor parallelism, as I mentioned, requires very fast interconnects. Pipeline less so. But you need to really work hard to reduce these pipeline bubbles. And then maybe at a high level, we see this pattern come up a lot. So you can either recompute or store in memory when we were talking about things like activation checkpointing or when we're working with GPUs. Or in this case, you can think about an extension of this as that you can store on a different GPU. From that perspective, you look at the data parallel. You're doing redundant work in some sense, because every rank is actually updating its parameters and keeping track of all the parameters. But the reason you're doing that is that you don't have to move the optimizer state across.

总结一下，有很多并行化的方式：你可以按数据切割、按张量或专家切割、按流水线或序列切割。我们看了数据并行——只做了 DDP。下次课会做 FSDP 和 ZeRO。张量并行，如我所说，需要非常快的互联。流水线并行不那么需要。但你需要花大力气减少流水线气泡。然后从高层次看，我们经常看到这样的模式：你可以要么重新计算（recompute）要么存储在内存中——就像我们讨论激活检查点（activation checkpointing）或在 GPU 上工作时那样。或者在这种情况下，你可以认为一个扩展是存储在另一个 GPU 上。从这个角度看，数据并行——你在某种意义上做了冗余的工作，因为每个 rank 实际上都在更新自己的参数并跟踪所有参数。但这样做的原因是你不需要移动优化器状态。

---

So one thing is that hardware is getting faster. But in some sense, we'll always want bigger models. So this idea of having a hierarchical structure will always be there. So that's it for today. So next Wednesday, [? Tatsu ?] will do more of a deep dive on more parallelism techniques.

有一件事是：硬件正在变得越来越快。但从某种意义上说，我们总是想要更大的模型。所以这种层级结构的思想将一直存在。今天就到这里。下周三，Tatsu 将进一步深入讲解更多的并行化技术。
