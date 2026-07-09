---
title: "Lecture 6: Kernels, Triton, XLA"
---


# Lecture 6: Kernels, Triton, XLA / 第六讲：核函数（Kernels）、Triton 与 XLA

---

So welcome back, everyone. So on Monday, Tatsu did an excellent job of describing a high level overview of GPUs and how to think about performance and all the quirks that come with GPUs. This lecture is going to be a continuation of that, where we're going to dive more deeply into the code, write some Triton kernels, and as well as do some benchmarking and profiling.

欢迎大家回来。在周一，Tatsu 出色地讲解了 GPU 的高层概述、如何思考性能问题以及 GPU 带来的种种特性。本节课将是它的延续，我们将更深入地研究代码，编写一些 Triton 核函数（kernels），并进行一些基准测试（benchmarking）和性能分析（profiling）。

---

So just to start, just to refresh what's going on with GPUs, here is a simplified diagram of what a typical GPU looks like. There's memory, and then the actual GPU chip. And just to keep in your head what are the characteristics of a GPU. So of course, we're talking about NVIDIA GPUs, but Tatsu also talked about CPUs, and there's AMD and so on. But focusing on NVIDIA GPUs. We've had multiple generations, from A100s, to H100s, to B200s. And in each generation, you have a GPU. It has a number of Streaming Multiprocessors, or SMs. And the number of SMs is about 100, between 100 and 200. So that hasn't really changed that much. And then within the individual SM, there's a set of registers. So B200s have 65,000 registers for a total of 256K per SM. And this also hasn't changed that much. In addition, there's a L1 cache as well as shared memory. So remember, these are the same memory, shared memory you can control. L1, you can't. This is per SM. And this is in the same order ballpark of size. And then there's L2 cache. And this is not per SM, this is for the whole chip. And this is a bit larger. And then finally, you have a High Bandwidth Memory, or HBM, which is large. And you see that this is the number that's actually going up quite a bit.

首先，为了回顾一下 GPU 的情况，这里是一个典型 GPU 的简化示意图。有内存（memory），然后是实际的 GPU 芯片。你需要在头脑中记住 GPU 的特性。当然，我们讨论的是 NVIDIA GPU，但 Tatsu 也提到了 CPU，还有 AMD 等等。不过我们重点关注 NVIDIA GPU。我们已经经历了多代产品，从 A100 到 H100 再到 B200。每一代都有一个 GPU，它有一定数量的流式多处理器（Streaming Multiprocessors, SMs）。SM 的数量大约在 100 到 200 之间，这个数字变化不大。在每个 SM 内部，有一组寄存器（register）。B200 有 65,000 个寄存器，每个 SM 总共 256K。这个数字变化也不大。此外，还有 L1 缓存（L1 cache）和共享内存（shared memory）。记住，这是同一块内存，共享内存你可以控制，L1 不行。这是每个 SM 的，大小也在同一量级。然后是 L2 缓存（L2 cache），这不是每个 SM 独有的，而是整个芯片共享的，容量更大一些。最后，是高带宽内存（High Bandwidth Memory, HBM），容量很大。你可以看到这个数字实际上增长了不少。

---

OK. And then in addition to size, you can think about what's happening with the bandwidth. And essentially, it's inversely correlated. So registers are very fast, L1 is slightly less fast, L2 is less fast, and high bandwidth memory is the slowest. Although eight terabytes a second is still not that slow in the grand scheme of things. So this is the main hierarchy you should have in your head. Large memory is slow and far but big. And fast memory like registers and L1 resides on the SM. It's local and it's fast, but small.

除了容量，你还可以考虑带宽。基本上，两者是负相关的。寄存器非常快，L1 稍慢一些，L2 更慢，高带宽内存最慢——尽管每秒 8 TB 在宏观尺度上也不算慢。这就是你头脑中应该有的主要层次结构：大容量内存慢而远但大；像寄存器和 L1 这样的快内存位于 SM 上，本地快速但容量小。

---

OK, that's the environment we're dealing with.

好，这就是我们要面对的环境。

---

## Programming Model / 编程模型

OK, so then, how do you program a GPU? So the program model is as follows. So there's notions of threads, which each thread executes a piece of code on a small part of the data. So each one of these arrows, you can think about it as a thread. These threads are organized into thread blocks, also known as Concurrent Thread Arrays, or CTAs. And this is a group of threads. And then finally, you have a collection of thread blocks which forms the grid. So when you launch a kernel, you're basically launching a grid of threads and thread blocks to all parallel simultaneously do some computation.

那么，你如何对 GPU 进行编程呢？编程模型如下：有线程（threads）的概念，每个线程在数据的一小部分上执行一段代码。所以这些箭头中的每一个，你可以认为是一个线程。这些线程被组织成线程块（thread blocks），也称为并发线程数组（Concurrent Thread Arrays, CTAs）。这是一个线程组。最后，你有一个线程块的集合，称为网格（grid）。所以当你启动一个核函数时，你基本上是在启动一个由线程和线程块组成的网格，让它们全部并行地同时进行一些计算。

---

OK, so this is simplified. There's some other things that are happening. For example, there's H100s and B200s also have thread block clusters, which are clusters of thread blocks that enable some amount of distribution memory. Also, B200s have tensor memory. Now for tensor cores, which is somewhere between registers and shared memory. Some of these things are invisible to the programmer, but they are in the hardware. But we won't worry about them for this intro lecture.

好的，这是简化版。还有其他一些东西在发生。例如，H100 和 B200 还有线程块簇（thread block clusters），它们是线程块的簇，支持一定量的分布式内存。此外，B200 还有张量内存（tensor memory），用于张量核心（tensor cores），位于寄存器和共享内存之间。其中一些东西对程序员是不可见的，但它们存在于硬件中。不过在这节入门课中，我们不会操心这些。

---

OK, so one thing you might ask about is, why do we have thread blocks? Why can't we just have a grid of threads, and each thread just takes a piece of data and does something? And this would be normally fine if all you want to do is element-wise operations, which we'll see. For example, GeLU is an activation function that applies element-wise. And threads are pretty natural. Each thread processes one element. So it's like Fi for i equals ranging over your data set. But for operations that involve communicating with threads, such as softmax or matrix multiplication, this view isn't really enough. And the reason is that, well, it could be enough if you were willing to pay the cost of writing and reading HBM. Because then you can still have-- for example, in a matrix we'll see later, you can just have every element in a cell. It goes and computes that element of the matrix. And it can just read and write HBM. But as we've noticed, HBM is very slow, so this would not be a good strategy.

你可能想问的一个问题是：为什么要有线程块？为什么不能只有一个线程网格，每个线程取一块数据然后做点什么？如果你只想做逐元素操作（element-wise operations），这通常没问题——例如，GeLU 是一个逐元素应用的激活函数。线程很自然：每个线程处理一个元素，就像 Fi for i 遍历你的数据集一样。但对于涉及线程间通信的操作，比如 Softmax 或矩阵乘法（matrix multiplication），这种视角就不太够了。原因是：如果你愿意承受读写 HBM 的代价，那它也许够用——例如在矩阵中，你可以让每个元素对应一个单元，去计算矩阵的那个元素，只需要读写 HBM。但正如我们注意到的，HBM 非常慢，所以这不是一个好策略。

---

So instead, what we should do is use shared memory, which is local to SM. And what the thread block allows you to think about is a collection of threads that are all going to access this shared memory. So consequently, you can think about a thread block, one of these thread blocks is being scheduled on one of these semantic-- not semantic, streaming multiprocessors. And it does its thing. And what it's going to do is it's going to read a bunch of data from HBM and then process it where the processing might involve communication between the threads via the shared memory, and then writes it back out. OK. So this is a critical piece that comes up. Later, we'll talk about tiling, and that's the whole game here.

相反，我们应该使用共享内存，它位于 SM 本地。线程块允许你思考的是一组将要访问这块共享内存的线程集合。因此，你可以这样理解：一个线程块被调度到一个流式多处理器上，然后执行它的任务。它要做的是从 HBM 读取一批数据，进行处理——处理过程中可能涉及通过共享内存在线程之间进行通信——然后写回结果。这是一个关键的要点。稍后我们会讨论分块（tiling），这就是这里的全部核心。

---

OK, in Triton, in fact, which we'll see as a primary way that we're going to write kernels these days, we're going to think natively in thread blocks. And I think once you get the hang of thinking of thread blocks, this makes a lot of sense and makes your life a lot easier, as we'll see.

实际上，在 Triton 中——我们将看到它是如今编写核函数的主要方式——我们会自然地以线程块为单位来思考。我认为一旦你掌握了线程块的思维方式，这会变得非常合理，并让你的生活轻松很多，我们稍后会看到。

---

OK, so the programming model is fairly simple, I think. There's threads, thread blocks, and grids. I think things get a bit more complicated, is the interaction between the programming model and the hardware. So the programming model is actually very nice. It provides abstraction of the hardware. When you can write a kernel, all you have to know is that there's a bunch of thread blocks. You define them and then define what computations each thread within the block or the thread block has to do. And those are just writing-- it's like writing Python. So that part isn't hard. And in fact, if you don't care about-- if you just care about correctness, that's all you need to know. But in practice, the performance is very sensitive to the hardware. And so you need to really deeply understand the hardware to obtain high performance. And in fact, the whole reason we're talking about GPUs and kernels is that you're trying to squeeze out performance. So there's these two levels here where you're trying to understand the computation, and that is only a part of the programming model. But how fast it runs is going to be strongly dependent on the hardware.

好，编程模型相当简单：有线程、线程块和网格。我认为事情变得更复杂的地方在于编程模型与硬件之间的交互。编程模型实际上非常好——它提供了对硬件的抽象。当你编写核函数时，你只需要知道有一堆线程块。你定义它们，然后定义每个线程或每个线程块中的线程需要做什么计算。这就像写 Python 一样。所以这部分并不难。事实上，如果你只关心正确性，知道这些就够了。但在实践中，性能对硬件非常敏感。因此你需要真正深入地理解硬件才能获得高性能。实际上，我们讨论 GPU 和核函数的全部原因，就是你在试图榨取性能。所以这里有两个层次：你试图理解计算，但这仅仅是编程模型的一部分；而运行速度则强烈依赖于硬件。

---

## Hardware Considerations / 硬件考量

OK, so I'm going to give you some examples of why this matters, and some of this will be review from what Tatsu talked about. But hopefully it will reinforce some of these concepts. So I think there will be around five different examples. And this is just to give you a flavor of the considerations.

我来举一些例子说明为什么这很重要，其中一些会是对 Tatsu 所讲内容的回顾。希望这能强化这些概念。大概有五个不同的例子，只是为了让你感受一下这些考量因素。

---

So there's something called warps, which I didn't talk about. So in the very simplified view, warps are not really part of this clean picture of the programming model. You have threads and thread blocks or grids. Technically, you can also exceed the warps, but you don't have to when you're just programming. So what is a warp? So each thread blocks, remember, is a collection of threads. But these threads are actually grouped into warps. And there's basically 32 threads per warp. So for example, if you have 64 threads in a thread block, there's two warps, the first 32 and the second 32. And as Tatsu mentioned last time, all threads within a warp, all of these T's, must execute the same instruction in lockstep on SM. So every cycle, they have to execute exactly the same instruction. And control divergence is when different threads within a warp need to actually execute different instructions. For example, if you have branching, if something, then A else B. And then what happens is that you can only do the A's in your threads in your warp, and then you do the B. So this gets sequential. So this is bad and inefficient, and that's why branching is something you want to generally avoid.

有一种叫做线程束（warps）的东西，我之前没有提到。在最简化的视图中，线程束并不属于编程模型那个干净图景的一部分——你有线程、线程块和网格。从技术上讲，你也可以超过线程束的限制，但编程时你不必这样做。那么什么是线程束？每个线程块是一组线程，但这些线程实际上被分组成了线程束。每个线程束有 32 个线程。例如，如果一个线程块中有 64 个线程，那就有两个线程束：前 32 个和后 32 个。正如 Tatsu 上次提到的，一个线程束内的所有线程必须在 SM 上以锁步（lockstep）方式执行相同的指令。每个周期，它们必须执行完全相同的指令。控制分歧（control divergence）是指当线程束内不同的线程需要执行不同的指令时——例如，如果有分支：if something then A else B。那么你只能先执行线程束中的 A 部分，然后再执行 B 部分，这就变成了顺序执行。这既不好又低效，这就是为什么一般要避免分支。

---

One thing that's, I think, really cool about warps is that a SM actually is running multiple warps. There's a warp scheduler, and there's a bunch of resident warps that are about to run. Each warp has some-- threads have registers. And the SM can switch between them with zero cost. Right, this is not true in general, like on a CPU. But this way that it's designed is to hide latency. So this is important, because one of the warps is, for example, reading from HBM, which remember is very expensive, can take 100 cycles or something. You don't want to just sit around waiting for that warp to do nothing. You switch immediately to another warp where it can actually do some tensor core operations.

我认为线程束一个非常酷的地方是，SM 实际上同时运行多个线程束。有一个线程束调度器（warp scheduler），以及一堆即将运行的常驻线程束（resident warps）。每个线程束有一些——线程有寄存器。SM 可以在它们之间以零代价切换。这在一般情况下是不成立的，比如在 CPU 上。但这样设计是为了隐藏延迟（hide latency）。这一点很重要，因为假如一个线程束正在从 HBM 读取数据——记住这非常昂贵，可能需要 100 个周期——你不想只是干等那个线程束什么都不做。你立即切换到另一个线程束，让它去做一些张量核心操作。

---

OK, so that's one thing to note about the warp. And another reason why warp comes up is this idea of occupancy. More specifically, warp occupancy. So each thread, just the hardware constraint says that each thread can use at most 255 registers. OK, and so what happens is that the SM has a fixed number of registers. So the more registers each thread is using, the fewer threads you can have. That's just math. And that can reduce your occupancy. But that's not necessarily bad, because if you have fewer threads. But each thread is doing more work, that can actually be good. So occupancy is something that you can measure, but it's not necessarily the larger, the better. Because there are some other tradeoffs here. And in fact, an example where you might want to have fewer threads is this idea of thread coarsening, where let's say you have an element-wise operation and you can have one thread just perform work on one element. OK, so then you have a lot of threads. But you can also say each thread processes multiple elements. Like a constant, maybe eight. So that gives you fewer threads, which makes scheduling and these things easier, but each thread is doing more work. So if your threads are very light, maybe you want to fatten them up a little bit.

这是关于线程束需要注意的一点。线程束出现的另一个原因是占用率（occupancy）这个概念，更具体地说是线程束占用率。硬件约束规定每个线程最多可以使用 255 个寄存器。SM 有固定数量的寄存器，所以每个线程使用的寄存器越多，你能拥有的线程就越少——这只是数学问题。这会降低你的占用率。但这不一定不好，因为如果线程更少，每个线程做更多的工作，实际上可能是有益的。所以占用率是可以衡量的，但不一定是越大越好——因为这里还有其他权衡。事实上，你可能想要更少线程的一个例子是线程粗化（thread coarsening）：假设你有一个逐元素操作，你可以让一个线程只处理一个元素，这样你会得到很多线程；但你也可以让每个线程处理多个元素，比如常数 8。这样线程更少，调度等事情更容易，但每个线程做的工作更多。所以如果你的线程非常轻，你可能想让它们稍微"胖"一点。

---

OK. So just as an example of what might happen here. So suppose you have a block, a thread block with 128 threads in it. And each thread is using 160 registers. OK. So there's a hardware constraint. So the B200s have maximum of registers of 65,000 per SM. And it also has a constraint that says you can't run more than 64 warps at a time. So then you can go and do some simple math to compute what is the occupancy here. So number of registers per thread. This has to be less than 255. That's fine. The number of registers that you're using per block is the number of threads per block times the number of registers per thread. That's about 20,000. That means you can run at most three blocks on your SM concurrently. And then that corresponds to 12 warps. And because the number of maximum warps is 64, that means you have an occupancy of 18%. So we're only running 18% the total number of warps you have. And this is because you have a lot of registers use per thread.

举一个可能发生的例子。假设你有一个线程块，里面有 128 个线程，每个线程使用 160 个寄存器。有一个硬件约束：B200 每个 SM 最多有 65,000 个寄存器，并且还有一个约束说你一次不能运行超过 64 个线程束。然后你可以做一些简单的数学计算来看看这里的占用率。每个线程的寄存器数必须小于 255——这没问题。每个块使用的寄存器数是每个块的线程数乘以每个线程的寄存器数，大约是 20,000。这意味着你的 SM 上最多可以同时运行三个块，对应 12 个线程束。由于最大线程束数是 64，这意味着你的占用率是 18%——我们只运行了可用线程束总数的 18%。这是因为每个线程使用了大量寄存器。

---

OK, here's another example. Something called bank conflicts. This applies to shared memory. So remember, shared memory is like L1. It's on an SM. And just the way the hardware works is that shared memory is divided into 32 banks, each one four bytes wide. OK, so these are my 32 banks, and this is my memory here. Each bank has many elements here. So there's a constraint that says every clock cycle, each bank can only be accessed by one thread, at most one thread. Assuming that's not a location. So for example, if you can't access this location and this location at the same time. Which means that if you have multiple threads that are trying to access the same bank, the accesses have to be serialized. And this is called a bank conflict. In the worst case example, imagine this were a matrix that was laid out like this. And you had some operation where 32 threads, you think, wow, this 32 is so great. I can massively parallelize this, and you try to all access this first column. They're just going to just wait in line. And this is a 32-way bank conflict, which is the worst possible setting you can be in.

另一个例子叫做存储体冲突（bank conflict）。这适用于共享内存。记住，共享内存类似于 L1，位于 SM 上。硬件的工作方式是：共享内存被分成 32 个存储体（banks），每个 4 字节宽。这是我的 32 个存储体，这是我的内存。每个存储体有很多元素。有一个约束说：每个时钟周期，每个存储体最多只能被一个线程访问。所以如果你有多个线程试图访问同一个存储体，访问必须被串行化。这叫做存储体冲突。在最坏的情况下，想象这是一个按这种方式布局的矩阵，你有一个操作需要 32 个线程——你想"哇，32 这么好，我可以大规模并行化"——但如果你试图全部访问第一列，它们只能排队等待。这是一个 32 路存储体冲突，是最糟糕的情况。

---

Now you could say, well, OK, why did you do that? Just like access rows, of course. But this is unavoidable, because, for example, if you're doing a matmul, you have to access rows of one matrix and columns of another matrix. And sometimes you do transposes, so you can't always just get away with choosing the order in which you go down. For element-wise operations, it's fine. You can go in any order. But if you're doing matmuls, you can't control for every matrix which row major or column major you're doing. There are some solutions here, which I won't get into. Something called swizzling, which arranges your shared memory so that when you're going through, you can avoid bank conflicts.

你可能会说，好吧，那你为什么要那样做？当然是按行访问。但这是不可避免的，因为例如在做矩阵乘法（matmul）时，你必须访问一个矩阵的行和另一个矩阵的列。有时你会做转置，所以你不能总是通过选择遍历的顺序来避免。对于逐元素操作，没问题——你可以按任何顺序。但做矩阵乘法时，你无法控制每个矩阵是行主序还是列主序。这里有一些解决方案，我就不深入了——比如一种叫做重整（swizzling）的方法，它重新排列你的共享内存，使得在遍历时可以避免存储体冲突。

---

OK, so that's another consideration. And when you're profiling, you can look at the bank conflicts, you can look at occupancy. And you can see what's happening.

这是另一个考量。当你做性能分析时，可以查看存储体冲突和占用率，看看发生了什么。

---

A final note which-- actually, two more things. So memory coalescing, which you talked about. So I'll just really quickly remind people what this is about. So when you have 32 threads in a warp and they try to access HBM, the memory accesses actually get combined into a transaction of 128 bytes, which are called cache lines. And it goes and fetches it all at once. So imagine you have memory laid out like this. This is 32. And in the best case, which is called full coalescing, all the threads are accessing the same cache line. So you have thread 1 accessing M00, thread 2 accessing M01, and so on. Which means that all at once, you're going to grab this entire cache line. Right, and whereas if you go down the columns, then you're going to fetch a lot of memory here, which you're not going to use. Same for the second row and so on. And so this feels similar to bank conflicts, but it's a very different constraint. And this is about shared memory, and this is about HBM.

最后一点——实际上还有两件事。内存合并（memory coalescing），你们已经讨论过了。我快速提醒一下大家这是关于什么的。当一个线程束中有 32 个线程试图访问 HBM 时，内存访问实际上会被合并成一个 128 字节的事务，称为缓存行（cache lines），然后一次性获取。想象一下内存是这样布局的。在最好的情况下，称为完全合并（full coalescing），所有线程访问同一个缓存行：线程 1 访问 M00，线程 2 访问 M01，依此类推。这意味着你一次性抓取整个缓存行。而如果你按列访问，你会获取很多不会用到的内存，第二行也是如此。这感觉类似于存储体冲突，但这是非常不同的约束——一个关于共享内存，一个关于 HBM。

---

OK, so final thing, block occupancy. So thread blocks are, remember, scheduled onto SMs. But we live in a finite-- logically, you can define as many thread blocks as you want. But physically on chip, you only have a certain number of SMs. For example, 148. So if you launch 160 thread blocks, then you can only schedule 148 of them. And then you have to wait until they're done, and then you schedule the 12. But what happens if you schedule 12 is that there's a bunch of SMs are just not doing anything. So that's called low occupancy. When the last wave of thread blocks gets fewer than the total maximum number of thread blocks.

最后一个问题是块占用率（block occupancy）。记住，线程块被调度到 SM 上。但我们生活在有限的世界里——逻辑上你可以定义任意多的线程块，但物理芯片上只有一定数量的 SM，比如 148 个。所以如果你启动 160 个线程块，你只能调度 148 个，然后必须等它们完成，再调度剩下的 12 个。但调度 12 个时，会有一堆 SM 什么都不做——这叫做低占用率，即最后一波线程块的数量少于总的线程块最大数量。

---

OK, so in general, maybe it's a good idea to make the number of thread blocks divide the SMs.

一般来说，也许让线程块的数量能整除 SM 数量是个好主意。

---

So maybe just to summarize here, there is a very elegant programming model where you have a grid of thread blocks and the thread blocks have individual threads in them. And in terms of the memory, HBM is global to everyone. Shared memory is local to a thread block. And registers are local to a thread. But again, all the details of the hardware-- warps, bank conflicts, memory coalescing, occupancy-- really determine performance. And many of these details are hard to know, because, I mean, the profiling tells you a bunch of information. But you have to know exactly how many SMs there are and exactly the sizing of everything. Sometimes the scheduler does something you don't really have control over what it's doing. So it's a little messier than the programming model.

这里做个总结：有一个非常优雅的编程模型——你有一个由线程块组成的网格，每个线程块中有独立的线程。就内存而言，HBM 是全局共享的，共享内存是线程块局部的，寄存器是线程局部的。但同样，所有的硬件细节——线程束、存储体冲突、内存合并、占用率——才真正决定性能。其中许多细节很难获知，因为性能分析会告诉你一堆信息，但你必须确切知道有多少个 SM、每个东西的精确大小。有时调度器会做一些你无法控制的事情。所以它比编程模型要凌乱一些。

---

OK, I will stop there for questions.

好，我在此暂停，接受提问。

---

Yeah? Yes, a quick question. So Cam, is there a scenario in which you one can share with them or-- like, for example, in the problem that we see 140 SM [INAUDIBLE] blocks, right. And we have to launch into two different ways. Is there no way in which a block can share an SM? Yeah, so the question is, can a block share an SM? I think the issue is if you're doing things right, then the-- I guess it depends on the block. If you have a block that's for example, using most of the tensor cores on the SM, then putting another block there isn't really going to speed things up. I think fundamentally, there is this jagged problem here of unevenness. Because the blocks have to stay together. So you can't take this and spread it out over here. The thing you would do is to change your blocksize. So you change the number of blocks so you don't get this tail here. Any other questions?

嗯？一个简短的问题。Cam，是否存在一种场景可以让它们共享——比如，在我们看到 140 个 SM [听不清] 块的问题中，我们需要用两种不同的方式启动。有没有办法让一个块共享一个 SM？是的，问题是：一个块可以共享一个 SM 吗？我认为问题在于，如果你做得对，那么——我想这取决于块。如果你有一个块，例如使用了 SM 上的大部分张量核心，那么在那里放另一个块并不能真正加速。我认为根本上存在一个参差不齐的不均匀问题，因为块必须保持在一起，你不能把这个块分散到那里。你应该做的是改变你的块大小，改变块的数量，这样就不会有这个尾部。还有其他问题吗？

---

## Benchmarking and Profiling / 基准测试与性能分析

OK, so let's move on. Hopefully you guys are getting more comfortable with GPUs now. So now I'm going to talk about benchmarking and profiling. I'm not going to actually maybe say that much in terms of content. But I do want to emphasize the philosophy here, which is, here's a recipe for success. You benchmark and profile your code. You make changes, and you benchmark your profile, your code again. And the reason I'm doing benchmarking and profiling as opposed to teaching you try and earlier is because you should always just measure what's going on in your code and figure out what the bottlenecks are before you start writing kernels.

好，我们继续。希望你们现在对 GPU 更熟悉了。现在我要谈谈基准测试和性能分析。我可能不会说太多实质内容，但我想强调这里的哲学——这是成功的秘诀：你对代码进行基准测试和性能分析，做出修改，然后再次进行基准测试和性能分析。我把基准测试和性能分析放在前面而不是后面教的原因，是因为在开始编写核函数之前，你应该总是先测量代码中发生了什么，找出瓶颈在哪里。

---

OK, so benchmarking is basically how long things take. And it gives you just this end to end time. It doesn't tell you where things are spent. But nonetheless, it's pretty useful, because ultimately, that's the thing that you care about, how long things are running for. And it also gives you, because it distills things into one number, you can see how things are scaling, let's say, with dimension. So there's a nice tool for benchmarking. But because this class is language models from scratch, I'm going to do it from scratch. But I think I'm doing it just to highlight a few gotchas with benchmarking.

基准测试基本上就是测量操作需要多长时间。它只给你端到端的时间，不告诉你时间花在哪里。尽管如此，它非常有用，因为最终你关心的就是运行时间。而且因为它将所有东西浓缩成一个数字，你可以看到事情如何随维度（dimension）扩展。有一个很好的基准测试工具。但因为这堂课是"从零开始构建语言模型"，我会从零开始做——只是为了强调基准测试中的一些陷阱。

---

So let's say we have this operation, matrix multiplication. So run operation 2 is this wrapper that basically instantiates two random square matrices of size dimension by dimension. And then it returns a function to perform the operation. OK, so matmul, if you call this, basically does the matmul of those two random matrices. OK, the random matrices are generated, it's just like multiplying the two.

假设我们有这个操作：矩阵乘法。run_operation 2 是一个包装器，它实例化两个大小为 dimension × dimension 的随机方阵，然后返回一个执行该操作的函数。如果你调用它，它就对这两个随机矩阵做矩阵乘法。随机矩阵生成后，就像对两者做乘法一样。

---

OK, so how do you benchmark? So the naive thing to do is just start time, run it, and then stop time. But there's a few things. One is that always remember to do your warm-up. I think I mentioned this on the second lecture, but I think it's worth emphasizing. And this is because if you have some things are lazily compiled and you want to just make sure that that thing is-- that time doesn't factor into. Because most of the time, you care about how fast something is, because you're going to run it over and over again, so the initial conditions don't really matter. And then you often want to time it multiple times because there is some variance. The proper way to time things is to use these CUDA events that-- a start event and an end event, which you can call record on. Actually do the computation and then hit the end event record. And then remember to synchronize to wait for the CUDA threads to finish, because everything on the GPU is happening if you have an async. And this is a synchronization barrier. And then you record the time.

那么如何进行基准测试呢？最天真的做法就是开始计时，运行，然后停止计时。但有一些注意事项。第一，记得做预热（warm-up）。我想我在第二讲提到过，但值得强调。因为有些东西是延迟编译的，你要确保那段时间不被计入。大多数时候你关心的是某个操作有多快，因为你要反复运行它，所以初始条件并不重要。然后你通常要多次计时，因为存在一些方差。正确的计时方式是使用 CUDA 事件——一个开始事件和一个结束事件，你可以调用 record。实际进行计算，然后记录结束事件。记得要同步（synchronize）以等待 CUDA 线程完成——因为 GPU 上的所有操作都是异步的。这是一个同步屏障。然后记录时间。

---

OK, and then you can do this again, and then again. And then here, we're just taking the average. If you are being very particular, you probably want to maybe look at the whole distribution, the P95 or whatever. But we'll just do the average here.

你可以重复多次，然后取平均值。如果你非常讲究，你可能想看整个分布，比如 P95 等。但这里我们就用平均值。

---

And then one thing that you can do with benchmarking is you can, let's say, scale up your matrices and see how the time changes. And you can see that in this case, matrix multiplication, as expected, it should grow cubically. But notice that there is this flaw where up until you get up to almost 2,000 dimensional matrices, things are basically a constant. Right, and this is because, as we've discussed, the shapes of these GPUs are built for fairly large matrix multiplications. And if you have a 2 by 2 matrix, it's going to be very inefficient.

基准测试还能做的一件事是，比如，扩大你的矩阵，看看时间如何变化。你可以看到，在这个例子中，矩阵乘法应该按预期呈三次方增长。但注意有一个缺陷：直到矩阵维度接近 2,000 之前，时间基本上是一个常数。这是因为，正如我们讨论过的，这些 GPU 的形状是为相当大的矩阵乘法设计的。如果你有一个 2×2 的矩阵，那会非常低效。

---

So really quickly on profiling. Profiling tells you where time is actually spent. Hopefully all of you are familiar with profiling and are doing it. Maybe less obviously, profiling, even if you don't care about the time, helps you figure out what's actually happening under the hood. Because especially with these high level languages, you write some code, and then it runs and you get some result. And sometimes it can be just good to understand what's actually going on.

快速讲一下性能分析。性能分析告诉你时间实际花在了哪里。希望你们所有人都熟悉性能分析并在使用它。不太明显的是，即使你不关心时间，性能分析也能帮助你理解底层到底发生了什么。因为尤其是使用这些高级语言时，你写一些代码，它运行，你得到结果。有时候理解实际发生了什么本身就是一件好事。

---

So PyTorch has a built-in profiler. In your assignment, you'll use Nsight, which gives you more details. But we're going to skip that in the interest of time.

PyTorch 有一个内置的分析器。在你们的作业中，你们会使用 Nsight，它提供更多细节。但为了节省时间，我们跳过这个。

---

So let's start with just if you add two numbers and-- or sorry, two tensors in PyTorch, again, a run operation creates two random matrices and applies the operation. So in profiling, I'm warming up. And then I'm just putting this context of-- the profiling context and doing the run. And then let's look at what the profile looks like for just a plus b in PyTorch. Normally doing PyTorch, you probably don't think about it. It's like, OK, well, these two tensors just get added. So what's actually going on underneath the hood? Right, so if you look at the things that it's calling, there is this long name, kernel at CUDA functor add. So this is basically a kernel that adds to tensors. And the times aren't going to be that interesting, because I'm only adding. So that's going to take 100% of the time. But this tells you that, well, underneath the hood there is this thing called add.

让我们从简单的开始：如果你在 PyTorch 中将两个数相加——或者说两个张量。同样，run_operation 创建两个随机矩阵并应用该操作。在性能分析中，我先做预热，然后放入性能分析上下文并执行运行。然后看看 PyTorch 中 a + b 的性能分析是什么样的。通常用 PyTorch 时你可能不会想这些——只是"这两个张量被加起来了"。那么底层到底发生了什么？如果你看它调用的东西，有一个很长的名字：kernel at CUDA functor add。这基本上就是一个对张量做加法的核函数。时间不会很有趣，因为我只是在做加法，所以会占 100% 的时间。但这告诉你，在底层有一个叫 add 的东西。

---

What about matmul? In PyTorch, I'm doing a at b. Similarly, there is this long name that describes this particular matmul kernel. Cutlass f32, f32, 64x64x16, and so on. Notice that if you change the dimensions-- so now I'm doing a 128 by 128 matmul-- you get actually a different one. If you look closely, that this is 64x64x16, this is 32x32x16. OK, so underneath the hood, PyTorch, it looks like you're doing just at. But underneath the hood, there could be all sorts of things that are happening.

矩阵乘法呢？在 PyTorch 中，我做 a @ b。同样，有一个很长的名字描述这个特定的矩阵乘法核函数：Cutlass f32, f32, 64x64x16，等等。注意，如果你改变维度——现在我做的是 128×128 的矩阵乘法——你会得到一个不同的核函数。仔细看，这个是 64x64x16，这个是 32x32x16。所以在底层，PyTorch 看起来你只是在做 @，但实际上各种事情都在发生。

---

So observations. Here, you can see which CUDA kernels are actually being called. These are generally the ones that have the long names. And different CUDA kernels are invoked depending on the tensor dimensions. The name actually tells you something about the implementation as well. So this name. So cutlass is the NVIDIA CUDA library for linear algebra. SM100 corresponds to the Blackwell architecture. So this is a kernel that's specifically designed for Blackwell. This is f32. And then 64x64x16 is the shape of the tile, which we're going to talk about later when we talk about tiling in the context of matmuls.

观察结果：你可以看到哪些 CUDA 核函数实际被调用——通常是那些名字很长的。根据张量维度的不同，会调用不同的 CUDA 核函数。名字实际上也告诉了你一些实现信息。这个名字中，cutlass 是 NVIDIA 的线性代数 CUDA 库，SM100 对应 Blackwell 架构——所以这是一个专门为 Blackwell 设计的核函数。这是 f32。64x64x16 是分块（tile）的形状，我们稍后在讨论矩阵乘法中的分块时会讲到。

---

OK, so that's benchmarking profiling. Just remember to do it. I think we make you do it on the assignment, so you have no choice.

好了，这就是基准测试和性能分析。记住要做这件事。我想我们在作业中会要求你们做，所以你们别无选择。

---

## GeLU Example / GeLU 示例

OK. So let's apply this to another example here on the GeLU. So remember, the GeLU activation function is this function, which is a typical non-linearity that's used. Often, it's approximated with this tanh approximation, which is more computer friendly.

好，让我们把这种方法应用到另一个例子——GeLU。记住，GeLU 激活函数是一个典型的非线性函数。通常它用 tanh 近似，这对计算机更友好。

---

OK, so naively, if you implement the GeLU, you can do it in PyTorch just like this. So you take a tensor, you just take this equation and you just put it into PyTorch, OK. That's fine. And you get some number. PyTorch also has a built in. If you call functional GeLU, you can get that version as well. And you can check that they're the same. You can run the two GeLU versions and make sure that the answer is the same for a random input. There's also something that people probably have discovered. If you haven't encountered this, this is an important thing to know. Is that you can take any PyTorch function, you call torch.compile on it, and it generates another function. And it does the same thing.

最天真的方式，你可以像这样在 PyTorch 中实现 GeLU：取一个张量，把这个方程直接放进 PyTorch，就可以了。你会得到一个数值。PyTorch 也有内置的——调用 functional.gelu 可以得到那个版本。你可以验证它们是一样的。运行两个 GeLU 版本，确保对于随机输入结果相同。还有一个东西可能有人已经发现了——如果你还没遇到过，这是一个重要的知识点：你可以对任何 PyTorch 函数调用 torch.compile，它会生成另一个函数，做同样的事情。

---

OK, so we have three horses in this race. We have the naive implementation. We have the built-in implementation. We have the compiled implementation. So we can benchmark them. Naive takes three. I guess this is 3.75. Built-in is much faster and compiled is much faster as well, but not maybe as quite as fast as built-in.

我们有三匹赛马：天真的实现、内置实现、编译后的实现。我们可以对它们进行基准测试。天真的实现耗时 3.75（单位），内置实现快得多，编译后的实现也快得多，但可能不如内置实现那么快。

---

OK. So what's happening here? Why are these things different? They all compute the same answer, but they have wildly different performance characteristics. And so here we can pull up the profiler and see what's actually going on underneath the hood. So if you look at the naive GeLU here and just do a profile, this-- something's wrong with this view, so I'm going to go to this. So you see that the profile shows how time is being spent. There's a bunch of different kernels on this binary functor unary add. tanh is a kernel here. And this corresponds to the fact that in PyTorch, when we write the PyTorch expression, you look at the computation graph, and each primitive in the computation graph is actually realized in the kernel.

这到底是怎么回事？为什么这些东西不一样？它们都计算出相同的答案，但性能特征天差地别。我们可以调出分析器，看看底层实际发生了什么。如果你看天真的 GeLU 实现并做性能分析——这个视图有点问题，我来换一个。你可以看到性能分析显示了时间是如何花费的。有一堆不同的核函数：binary functor unary add、tanh 等等。这对应于一个事实：在 PyTorch 中，当我们写 PyTorch 表达式时，计算图中的每个原语实际上都由一个核函数实现。

---

Right. And the reason this is slow is that when you launch a kernel, the kernel has to read from HBM. Pull it all the way over to your SM, do the computation, and write it back. And then the kernel picks that up from HBM and then writes it back, and so on and so forth. So you're doing a lot of reads and writes back and forth. Because between kernel invocations, things have to go back to HBM.

这之所以慢，是因为当你启动一个核函数时，它必须从 HBM 读取数据，一路拉到你的 SM，进行计算，然后写回。然后下一个核函数从 HBM 取数据，再写回，如此反复。所以你在来回做大量的读写操作，因为在核函数调用之间，数据必须回到 HBM。

---

So if you look at what the built-in is doing, this is actually not that interesting. There's this GeLU CUDA kernel implementation, which is a single kernel that just implements the GeLU. And so why does this exist? Well, because people use GeLU. So someone wrote a kernel for it and put it in the standard library. I mean, there's nothing magical.

如果你看内置实现在做什么，这其实没什么意思。有一个 GeLU CUDA 核函数实现，它是一个单一的核函数，直接实现了 GeLU。为什么会有这个？因为人们使用 GeLU，所以有人为它写了一个核函数并放在了标准库中。这没有什么神奇的。

---

So compilation is really interesting here. I'm not going to say too much about how it works, but it's really, I think, a fascinating topic where you can take a naive implementation, which, remember, it's in PyTorch, it has a computation graph. And run a compiler. Which basically, if you look at what's underneath the hood, it's just a single kernel. And this is because it's figured out to look at the computation graph and essentially write that kernel in Triton. So you can see that this is actually a Triton kernel.

编译在这里非常有趣。我不打算详细讲它是如何工作的，但我认为这是一个迷人的话题：你可以拿一个天真的实现——记住，它在 PyTorch 中，有一个计算图——然后运行编译器。底层的结果就是一个单一的核函数。这是因为编译器搞清楚了如何查看计算图，并本质上用 Triton 写出了那个核函数。所以你可以看到，这实际上是一个 Triton 核函数。

---

OK, so naive implementation. Multiple kernels requires multiple reads and writes to and from HBM. There's no kernel fusion here. This is slow. The built-in compiler version, there's one kernel. Basically all the operation in the GeLU have been fused together into one kernel. So you read from HBM once, you write to HBM once per element. And you see that the compiled kernel is a Triton kernel.

天真的实现：多个核函数需要多次从 HBM 读写。这里没有核函数融合（kernel fusion）。这很慢。内置版本和编译版本：一个核函数，GeLU 中的所有操作都被融合到一个核函数中。所以每个元素你从 HBM 读一次，写一次。你可以看到编译后的核函数是一个 Triton 核函数。

---

OK, so that maybe is a good segue to talk about what this Triton thing is all about. Yeah? [INAUDIBLE] Let's see. I mean, I guess it says CUDA kernel implementation, so I imagine someone wrote it in CUDA.

好，这也许是一个很好的过渡，来谈谈这个叫 Triton 的东西到底是什么。嗯？[听不清] 让我想想。我的意思是，它写着 CUDA kernel implementation，所以我猜有人用 CUDA 写了它。

---

OK, any other questions? Yeah? Why is Triton kernel faster than this one? So why is the Triton kernel faster? So a Triton kernel is actually not faster in this case. Oh, sorry. The compiled kernel is one Triton kernel, and this is slower than the built-in. Yeah. I think last year when I did this, it was actually closer. But these things change, and it's very hardware dependent. And I think none of this is terribly optimized. This is just giving you the general idea here.

好的，还有其他问题吗？嗯？为什么 Triton 核函数比这个快？实际上 Triton 核函数在这个例子中并不更快。哦，抱歉。编译后的核函数是一个 Triton 核函数，它比内置的慢。是的，我想去年我做这个的时候，差距其实更小。但这些事情会变化，而且非常依赖于硬件。我认为这些都算不上极度优化，只是给你一个大致概念。

---

## Writing Triton Kernels / 编写 Triton 核函数

OK, so let's write some Triton kernels. So remember our programming model. You have a bunch of threads organized by Thread groups, a thread blocks, and there's a grid of thread blocks. And if you were to write in CUDA, which was originally developed by NVIDIA, and that's been for years the thing that you do when you write kernels, the mental model is, what does each thread do? So you write a piece of code which essentially has some ID that identifies which thread you're talking about, and it just executes the code. So the nice thing about this is that it's very closely related to what is actually happening underneath the hood. And it's fine-grained, gives you fine-grained control. But there's cons here, which is that, remember, all these threads are in a thread block. And some operations require them to communicate. So what has to happen is that they have to synchronize. And they read from HBM all at once. And they have to synchronize and do the computation. And you have to basically do that bookkeeping. So if you were doing all element-wise operations, this CUDA is just fine. It doesn't really matter. But as you get more complex operations, then try and provide some value of the abstraction.

好，让我们写一些 Triton 核函数。记住我们的编程模型：有一堆线程按线程组组织，线程块，以及一个线程块网格。如果你用 CUDA 写——它最初由 NVIDIA 开发，多年来一直是编写核函数的方式——思维方式是：每个线程做什么？你写一段代码，它有一个标识线程的 ID，然后执行代码。好处是它与底层实际发生的事情非常接近，粒度细，给你精细的控制。但缺点在于，记住，所有这些线程都在一个线程块中，有些操作需要它们通信。它们必须同步，一起从 HBM 读取，同步，进行计算。你必须做这些簿记工作。如果你只做逐元素操作，CUDA 没问题。但随着操作变得更复杂，抽象的价值就体现出来了。

---

So Triton was developed by OpenAI. I think by now, it's been pretty standard. You basically specify what each thread block does. Generally it's powerful enough, especially for this class that you're getting started. If you really go and want to exploit every single new feature of the latest hardware, it might not give you the full flexibility. But let's not worry about that. And the conceptual framework to think about in Triton is that you're thinking about, what does a block do? A block is going to load data into shared memory, operate it on, and write it back to global memory. So in some sense, these blocks are intermediate point between thinking about what individual elements are doing as well as thinking about the general operation. And so in PyTorch, you basically define these huge matrices and you say multiply them together. And that's the atomic operation. And a lot of what you're thinking about is, how do I get things into big matmuls? Right, and at some level, Triton is a hybrid between that and the individual elements, as we'll see.

Triton 由 OpenAI 开发。现在它已经相当标准了。你基本上指定每个线程块做什么。通常它足够强大，尤其是对于你们刚开始的这门课。如果你真的想利用最新硬件的每一个新特性，它可能不能给你完全的灵活性。但我们不用担心这个。Triton 的概念框架是：你思考一个块做什么？一个块将数据加载到共享内存，进行操作，然后写回全局内存（global memory）。在某种意义上，这些块是介于思考单个元素在做什么和思考一般操作之间的中间点。在 PyTorch 中，你基本定义这些巨大的矩阵，然后说把它们乘在一起——这是原子操作。而你思考的很多问题是：如何把东西变成大型矩阵乘法？在某种程度上，Triton 是那个和单个元素之间的混合体，我们将会看到。

---

OK, so let's start with the GeLU example here. So let's define an 8,000 dimensional vector and start writing some Triton.

好，让我们从 GeLU 例子开始。定义一个 8,000 维的向量，开始写一些 Triton。

---

OK, so Triton is basically going to be you write Python. How many of you have written Triton before? Just a show of hands. OK, OK. Not that many, which is good, because then you won't be bored.

Triton 基本上就是你写 Python。有多少人之前写过 Triton？举一下手。好的，好的。不多，这很好，因为那样你们就不会觉得无聊了。

---

OK, so this is normal PyTorch. Right, there's no Triton here. But I'm just preparing. And so what I'm going to do is I take this tensor, and I'm going to allocate an output tensor. OK, because in Triton, we're not thinking functionally anymore. We're just thinking about moving. You have to explicitly read and write. So there's no returning value. So I'm going to allocate the output tensor, which I'm going to-- the kernel's going to write to. And then so this tensor can be arbitrarily big, right. And I can't generally fit this all into one SM, because it's just too big. So I need to break it up into blocks.

这是普通的 PyTorch，这里没有 Triton。我只是在准备。我取这个张量，分配一个输出张量。因为在 Triton 中，我们不再以函数式的方式思考，我们只考虑数据移动。你必须显式地读写，所以没有返回值。我分配输出张量，核函数将要写入它。这个张量可以任意大，我通常不能把它全部放进一个 SM，因为它太大了。所以我需要把它分块。

---

So what I'm going to do is you can think about this x as being this array. I'm going to chop it up into blocks. So the total number of elements is 8,000. I'm just going to set the blocksize to 1,024 for now. And then I have eight blocks. OK. So then I'm going to use this weird syntax to call the kernel. So Triton GeLU kernel. This basically in brackets tells me essentially the shape of the grid. So basically, this says the grid has num blocks. Blocks. And I'm going to, for every one of these blocks, invoke this function, Triton GeLU kernel, which I'll talk about in a bit. I'm going to pass in an x, y num elements and the blocksize.

我要做的是：你可以把这个 x 看作一个数组，我要把它切分成块。总共有 8,000 个元素，我暂时将 blocksize 设为 1,024，那么我有 8 个块。然后我用这种奇怪的语法来调用核函数：Triton_GeLU_kernel，括号中告诉了我网格的形状——网格有 num_blocks 个块。对每一个块，调用 Triton_GeLU_kernel 函数，传入 x、y、num_elements 和 blocksize。

---

OK. All right, so unfortunately, I'm not going to be able to trace through this, so I'll just show you what the code looks like here. So let me get rid of that. OK, so this is probably the simplest kernel you can imagine. So when you are looking at the triton gelu kernel, now this is before we had x and y. So now these are pointers. Right, you can think about these as just integers, they're addresses. So you have to get comfortable with that. And then we have the number of elements and the blocksize, which are basically actually passed in from here.

好的，不幸的是我不打算一步步跟踪这个过程，我只是给你看看代码长什么样。这可能是你能想象到的最简单的核函数。看着 triton_gelu_kernel，现在这些 x 和 y 是指针（pointers）。你可以把它们想象成整数，是地址。你需要适应这一点。然后我们有 num_elements 和 blocksize，它们实际上是从这里传入的。

---

OK, so the way to think about it is that for every block, we're going to have this function being called. And what happens is the first thing I'm going to do is I'm going to wake up. This block wakes up and say, who am I? Well, the program ID is-- basically the PID is basically identifying the block. So PID would be 0 for this block 1, 2, and 3 here.

思考方式是：对于每个块，这个函数会被调用。发生的是，我要做的第一件事是醒来。这个块醒来并问：我是谁？程序 ID（PID）标识了块。所以 PID 对于块 0、1、2、3 分别是 0、1、2、3。

---

OK, so now I have to figure out what data I'm going to operate on. So that's PID times blocksize. So this is the offset into x pointer. So if PID is 0, then start is 0. If PID is 1, then start is blocksize. If PID is 2, then it's 2 times blocksize, and so on.

现在我需要确定我要操作哪些数据，那就是 PID times blocksize。这是 x 指针的偏移量（offset）。如果 PID 是 0，start 是 0；如果 PID 是 1，start 是 blocksize；如果 PID 是 2，start 是 2 倍的 blocksize，依此类推。

---

OK. So now, I'm going to figure out the span I'm operating on. So offsets is start plus. This is the Triton library. A range 0 blocksize, which conceptually gives you the integers 0 through blocksize minus 1. So offsets is going to be essentially for-- let's say block 1, it's going to be blocksize blocksize plus 1 all the way to blocks 2 times blocksize minus 1.

现在我要确定我操作的范围。offsets 是 start 加上，这是 Triton 库中的 tl.arange(0, BLOCKSIZE)，概念上给你整数 0 到 BLOCKSIZE-1。所以 offsets 对于块 1 来说，将是 blocksize, blocksize+1, 一直到 2×blocksize-1。

---

OK, so in this case, num elements divides by blocksize. But in general, that's not the case. So you'll often see in train code, there's this masking. Which says, well, sometimes if the-- let's say the tensor only goes up to here. Then I'm going to form a mask, which is going to be true up until that point and false after that point. And for blocks that are not the final block, it's going to be just all ones.

在这个例子中，num_elements 可以被 blocksize 整除。但一般情况下不是这样。所以你经常会在训练代码中看到掩码（masking）。如果张量只到这里，我就形成一个掩码，在那个点之前为 true，之后为 false。对于不是最后一个块的块，它就是全 1。

---

OK, so now I've done the setup. What I do is I read. And this is basically pointer arithmetic. So x pointer, remember, is the integer that specifies the memory location of where x is. I'm going to add offsets to that, which gives me the first blocksize number of elements there. According to the mask, if I'm masked out, then I don't read it. And then now I think you can just think about this a vector. And then you do your normal computation. And then you get y. And y is the same size as x. And then you do tl.store y pointer plus offsets y and the mask. OK, so this load loads from HBM, does some stuff, and then it writes back to HBM.

设置完成之后，我进行读取。这基本上是指针运算（pointer arithmetic）。x_pointer 是指定 x 内存位置的整数。我把 offsets 加给它，得到前 blocksize 个元素。根据掩码，如果被掩蔽，我就不读。然后你可以把它看作一个向量，进行正常的计算，得到 y（y 和 x 大小相同）。然后 tl.store(y_pointer + offsets, y, mask)。所以这个 load 从 HBM 加载，做一些事情，然后写回 HBM。

---

OK, I'm going to stop there and take any questions about this first Triton kernel.

我在这里暂停，接受关于这第一个 Triton 核函数的问题。

---

Yeah? [INAUDIBLE] Yeah. So the difference is, what is the difference between CUDA? And for this element wise, it looks pretty much the same, right. And in fact, CUDA is even, I think, simpler, because it really is element wise. You wake up, and you identify the thread. And then you just operate on that element. Now the only thing here is that it's like the vectorized version, where you have a block and you operate on that block. Later, we'll see that operating on blocks is doing more than-- if you do something more than element-wise, then CUDA is going to be a lot more annoying to work with.

嗯？[听不清] 是的。区别在于，与 CUDA 的区别是什么？对于这个逐元素操作，看起来几乎一样。实际上 CUDA 甚至更简单，因为它真的是逐元素的——你醒来，识别线程，然后对那个元素操作。这里唯一的不同是它是向量化版本，你有一个块并对那个块操作。稍后我们会看到，对块进行操作比逐元素更多——如果你做的不只是逐元素操作，CUDA 用起来会麻烦得多。

---

So a bunch of questions. Yeah, back there. How does this relate to if you wanted to use the tensor units? So how is this related to if you want to use the tensor units? So I'll later show you what this code actually compiles down into. And maybe I'll get back to that. But the short answer is that you don't control that. The hardware figures out where to put things.

一堆问题。嗯，后面那位。这与你想用张量单元（tensor units）有什么关系？我稍后会展示这段代码实际编译成什么。简短的回答是，你不控制那个——硬件自己决定把东西放在哪里。

---

Yeah? Can you actually walk through what's happening at tf.load from HBM to share to register? What's the step by step where data is actually flowing? Yeah, so the question is, what is actually happening when this statement is executed? So the short version is that this is in some sense a lie. Right, it's not like the GPU actually calls the Triton library on the GPU and it's actually executing this code. This is basically for our consumption to specify the computation. The compiler takes this, as we'll see later, and writes it into something called ptx, and then it will actually do the work.

嗯？你能讲解一下 tl.load 从 HBM 到共享内存到寄存器的过程吗？数据实际流动的每一步是怎样的？问题是，当这个语句被执行时，实际发生了什么？简短版本是，这在某种意义上是一个"谎言"。并不是 GPU 真的在 GPU 上调用 Triton 库并执行这段代码。这基本上是为了我们指定计算而存在的。编译器（我们稍后会看到）接收这个，把它写成一种叫做 ptx 的东西，然后实际执行工作。

---

So that's mechanically what's happening, which I'll get to later. If you're asking about the conceptual question, the way to think about this is that this-- x pointer is a memory location in HBM. And this basically specifies a range of memory locations. And load takes those memory locations and returns the data associated with them. Here, I have a local variable called x. In practice, this is going to be generally a register or shared memory. Triton figures out what to do there.

这就是机制上发生的事情，我稍后会讲到。如果你问的是概念性问题，思考方式是：x_pointer 是 HBM 中的一个内存位置，它指定了一个内存位置范围。load 取这些内存位置并返回对应的数据。这里我有一个局部变量叫 x，在实践中它通常是一个寄存器或共享内存。Triton 自己决定怎么做。

---

[INAUDIBLE] --at the threat level. When this is invoked, it's not really clear. Did I line up what is going to be in shared and going to be at the register level beforehand, or is it happening now, which is way late? And so then that's just where all the threads are sitting idle to get a memory to flush in. I'm sure it's ready to execute so that we're not sitting there twiddling our thumbs, just waiting for data to come in from HBM.

[听不清]——在线程级别上。当这个被调用时，并不清楚。我是否事先安排好了什么会在共享内存中、什么会在寄存器级别，还是说这一切发生得很晚？然后所有线程就空闲着等待内存刷新进来。我确信它已经准备好执行，这样我们就不会坐在那里干等数据从 HBM 进来。

---

Yeah, yeah. So the question is, when does this actually get executed, and doesn't this block? Let me try to come back to this question when I show you the ptx, and maybe hopefully it will provide a bit more context on what's happening.

是的。问题是，这什么时候实际执行？不会阻塞吗？让我试着在我展示 ptx 时再回到这个问题，希望能提供更多关于实际发生了什么背景信息。

---

OK, any other questions? OK, so all the kernels are going to look something like this. So I do want to make sure people understand just the general form, which is that you have generally your inputs, your outputs. You wake up, you figure out which index you're going to look at. You read. You do some stuff, and then you write to HBM.

好的，还有其他问题吗？好，所有的核函数都会看起来像这样。我想确保大家理解一般形式：通常你有输入、输出。你醒来，确定你要看哪个索引。你读取，做一些事情，然后写入 HBM。

---

## PTX / PTX

OK. So let's talk about ptx briefly. So let's see, does this work? Does this link work? OK, so when you write Triton, the compiler generates ptx code, which is this intermediate assembly language for GPUs. I am obviously not going to go through all of this, but just to give you the flavor of what this looks like. Let me actually start with the observation.

好，让我们简要讲讲 ptx。看看这个链接是否有效。当你写 Triton 时，编译器会生成 ptx 代码，这是一种 GPU 的中间汇编语言。我显然不会全部过一遍，只是给你们感受一下它长什么样。让我从观察开始。

---

So a few things. So this is now what a thread is actually doing. Not a thread block, because that's been compiled away. And so if you look at-- a few notes here. So this LD global is basically saying load from HBM into some registers. And the registers are denoted as the r are integer registers, fr, floating point registers. And then you have statements like mov 0 into r5, mov 0 into r6, and so on. And then you have multiplication. You're going to multiply this register by this constant and then put it into this. So this code gets executed. And at the bottom, you should see global store. So this is writing back into the HBM. So this gets executed. This is actually the code that gets executed on a thread. And Triton is basically a layer up above that.

有几件事要注意。现在这是一个线程实际在做的事情——不是线程块，因为那已经被编译掉了。LDGLOBAL 基本上是从 HBM 加载到一些寄存器中。寄存器表示为 r 是整数寄存器，fr 是浮点寄存器。然后有像 mov 0 into r5、mov 0 into r6 这样的语句。还有乘法——将这个寄存器乘以这个常量，然后放入那个寄存器。这段代码被执行。在底部，你应该看到 STGLOBAL（全局存储），这是写回 HBM。这段代码被执行，这是一个线程上实际执行的代码。Triton 基本上是它上面的一层。

---

One other thing to notice is that you see all these blocks and what's going on there. And what's going on there is I alluded to thread coarsening, which is that this is one thread. But rather than processing a single element, it's actually processing eight elements. So the compiler decided that, well, actually, this thread is pretty lightweight. It doesn't do that much, so let's just try to thicken it up a little bit. So looking at ptx can give you some of appreciation for what's going on underneath the hood.

另一件要注意的事情是，你看到所有这些块，那里发生了什么。我之前提到的线程粗化（thread coarsening）——这是一个线程，但它不是处理单个元素，而是处理八个元素。编译器认为这个线程相当轻量，做不了多少事，所以让它"胖"一点。看看 ptx 可以让你对底层发生的事情有所 appreciation。

---

Yeah? So it makes this for each individual-- [INAUDIBLE] So the question is, does it make this for each thread? So this is compiled once. And it's the same piece of code that each thread runs. And the way that the thread distinguishes itself is that this piece of code gets passed basically the thread ID. So here, the cta.x is the block index, and tid.x is the thread index. So this basically, if this piece of code is running, this tells you which block I'm in. And tid.x tells you which thread inside that block I'm in.

嗯？它是为每个线程生成这个吗？问题是，它是为每个线程生成这个吗？这是编译一次的。每个线程运行同一段代码。线程区分自己的方式是，这段代码被传入线程 ID。这里，cta.x 是块索引，tid.x 是线程索引。所以如果这段代码在运行，这告诉你我在哪个块中，tid.x 告诉我我在那个块中的哪个线程。

---

OK. Any other questions? And I'm trying to figure out how to-- OK. OK, so that's generally a flavor of your first Triton kernel load from HBM compute right back to HBM. And then we saw the ptx, which is the grungy what actually happens underneath the hood. There's still a lot of things that are not specified in ptx. Like, for example, which SM things are operating on and the warps and everything. A lot of those are hardware controlled, so you don't even see.

好的，还有其他问题吗？我在想办法——好。这就是第一个 Triton 核函数的大致样子：从 HBM 加载，计算，直接写回 HBM。然后我们看到了 ptx，这是底层实际发生的"脏活"。ptx 中仍有很多未指定的事情，比如在哪个 SM 上操作、线程束等。很多都是硬件控制的，所以你甚至看不到。

---

Yeah? So ptx code is generated by the compiler, not something that you would normally code? It looks like it's assembly code. Yeah, so the question is, is ptx just generated by the compiler? So there are people who do write ptx if you really think you're better than the compiler. And I think the NVIDIA compilers are generally pretty mature, but some other accelerators that are less developed. I think sometimes you just have to reach in and actually handhold a bit more. But generally, yeah, you shouldn't need to do that.

ptx 代码是由编译器生成的，不是通常你手动编写的代码？它看起来像汇编代码。问题是，ptx 只是由编译器生成的吗？确实有人会手写 ptx，如果你真的认为你比编译器强。NVIDIA 的编译器通常相当成熟，但一些其他的、不那么成熟的加速器——有时你确实需要介入手动处理。但一般来说，你不需要这样做。

---

Yeah? [INAUDIBLE] My work will get scheduled onto an SM. I'll get to that tf.load and it's almost like a CPU trap call where I'm just waiting for something to happen. And now I am turning my thumbs and some other work will get scheduled over me. And then it will do operations. Now that you have to upload is done, then I'll reschedule that work and then I'll continue on. Is that-- Yeah, that's right. So just to repeat the question or the comment. So if you look at this triangle code, these statements, this load, is going to block for some number of cycles. And then so this is running on some thread on some warp on some SM. And remember, the SM is running multiple warps at the same time. So when you get to that point, it can just find another warp to run. And then when this is done, the warp scheduler comes back and takes over.

嗯？[听不清] 我的工作会被调度到 SM 上。我会执行 tl.load，几乎像一个 CPU 陷阱调用，我就在那里等待一些事情发生。然后我闲着，其他工作会被调度到我上面。它会执行操作。上传完成后，我会重新调度那个工作，然后继续。是这样的吗？——是的，没错。重复一下这个问题或评论。如果你看这个 Triton 代码，这些 load 语句会阻塞一定数量的周期。这运行在某个 SM 上的某个线程束的某个线程上。记住，SM 同时运行多个线程束。所以当到了那个点，它可以找另一个线程束来运行。当这个完成时，线程束调度器回来接管。

---

Why do you [INAUDIBLE]? Sorry. Oh, sorry. I recall from [INAUDIBLE]. Yeah, so the question is, why four warp schedules? I don't exactly the reason behind that.

为什么你[听不清]？抱歉。哦，抱歉。我记得从[听不清]。问题是，为什么是四个线程束调度器？我不确切知道这背后的原因。

---

## Softmax, Row Sum, Matmul / Softmax、行求和、矩阵乘法

OK, so now let's go through some other examples. Maybe just as a quick preview. We're going to do three more examples. GeLU is the simplest form. Even though the computation has a lot of messiness. It's just element wise. So conceptually, in the context of this lecture, is actually very simple. Now we're going to look at Softmax, where now you're going to have to do reduction. But in this case, we're going to think about the case where row fits on a block. And then we're going to consider the case where row doesn't fit on a block, and then we're going to do go up to matmul. And then hopefully by that point, you'll have all the ingredients that you need to do the assignment and implement flash attention.

现在让我们看一些其他例子。快速预览一下。我们再讲三个例子。GeLU 是最简单的形式——尽管计算有些杂乱，但它只是逐元素的。所以在概念上，在本节课的背景下，它实际上非常简单。现在我们要看 Softmax，你需要做归约（reduction）。在这个例子中，我们考虑行可以放入一个块的情况。然后我们考虑行不能放入一个块的情况，然后我们一直到矩阵乘法。希望到那时，你们已经具备了做作业和实现 Flash Attention 所需的所有要素。

---

OK. So so far, we looked at element wise operations. Now let's think about other operations that aggregate over multiple values. So remember what the Softmax does. Let's just think of as a matrix. You exponentiate and normalize each row of a matrix. OK, so this is used in intention and used in generating output probabilities. Generally a good thing to do.

到目前为止，我们看了逐元素操作。现在让我们思考其他聚合多个值的操作。记住 Softmax 做什么——把它看作一个矩阵，你对矩阵的每一行做指数化和归一化。这用于注意力机制和生成输出概率。通常这是一件好事。

---

So let's just start with a naive implementation and just keep track of what's happening. So here, I'm defining this tensor. And here's the naive implementation. Actually, I think this is on assignment one. OK, anyway. So here, I have an M by N matrix. And so I need to, for every row, compute the-- I'm going to compute the max of each row. And this is for numerical stability. I'm going to subtract off the max. And then I'm going to exponentiate element-wise. And I'm going to sum and compute the normalization constant for every row. And I'm going to divide. And then that's it.

让我们从一个天真的实现开始，跟踪发生了什么。这里，我定义了一个张量，这是天真的实现。实际上，我想这是作业一的内容。不管怎样。这里我有一个 M×N 矩阵，对于每一行，我需要计算——我要计算每行的最大值，这是为了数值稳定性。我减去最大值，然后逐元素指数化，求和并计算每行的归一化常数，然后做除法。就是这样。

---

OK. So if you count the number of reads and writes, remember, this is just plain PyTorch. So this is a different kernel. This is a different kernel. And unless you call to torch and compile, these are going to be different operations. And each operation is going to read and write, read and write from HBM. OK, so you have five MN reads, three MN writes. And in principle, you should really only have much fewer.

如果你数一下读写次数——记住，这只是普通的 PyTorch——这是一个不同的核函数，这是另一个不同的核函数。除非你调用 torch.compile，否则这些都是不同的操作。每个操作都会从 HBM 读写。你有 5MN 次读取、3MN 次写入。而原则上，你应该只需要少得多。

---

OK, so this is a piece of code. Makes sense. Everyone should be familiar what the Softmax is doing.

这是一段代码，说得通。每个人都应该熟悉 Softmax 在做什么。

---

OK. So let's write down the Triton kernel. And in some sense, the form is going to be very similar. Just like in the GeLU. Right, once you do the scaffolding, the core computation looks very much like the naive version. So what we're going to do is we're going to say each row is a block. OK. And why do I make each row a block? Well, because now, remember, each row, I have to normalize and sum. So it's not element-wise. So Softmax is not an element wise. But it is row wise. So the blocks don't interact. And the blocks don't have shared memory, so that's fine. There's no shared memory across blocks. So then within each row, I'm just going to do some stuff.

好，让我们写出 Triton 核函数。在某种意义上，形式和 GeLU 非常相似。一旦你做了脚手架工作，核心计算看起来就和天真的版本很像。我们要做的是：每一行是一个块。为什么让每一行是一个块？因为每一行我需要做归一化和求和——它不是逐元素的。Softmax 不是逐元素的，它是逐行的。块之间不交互，块之间没有共享内存，所以没问题。然后在每一行内，我只做一些事情。

---

OK, so let's see what happens. So again, I'm going to, in Python, I'm going to allocate my output tensor. I have this M by N matrix. I'm going to define the blocksize as basically the number of columns. Go to the next power of 2 for good luck. And then the number of blocks is just the number of rows. OK, and I'm going to call this kernel. So how many blocks are there? M. M. Right, one for each row. And each block, I'm going to pass the input pointer, the output pointer. And then I'm going to also pass these strides which tell me how far to move down.

让我们看看发生了什么。在 Python 中，我分配输出张量。我有一个 M×N 矩阵，我将 blocksize 定义为列数（为求好运取下一个 2 的幂）。块的数量就是行数。然后调用这个核函数。有多少个块？M。是的，每行一个。每个块，我传入输入指针、输出指针，以及步长（strides），告诉我在内存中向下移动多远。

---

OK, let me actually go and show you that Softmax kernel, OK.

好，让我实际展示 Softmax 核函数。

---

OK, so what does this look like here? So I wake up. I'm on a particular row, OK. And this is going to give me all the columns from 0 to the number of blocksize, which I'm assuming that's all the columns. I'm going to read. So basically, I need to figure out where to read from memory, and that's going to be the start of my data. Plus which row. And the row stride basically gives me every row is-- basically, this is the number of columns, essentially. It's going to tell me where how far to go down. And then this is x pointers is basically the addresses of all the data I need to load. I load them up. And here, I do this thing where if it's masked out, then I put minus infinity, because that's going to be the equivalent of a 0 for the Softmax operation. And then this part is essentially the same as the naive Softmax. I'm just going to compute the max, subtract it off, exponentiate, sum, and divide. And then I write it back.

这是什么样子的？我醒来，我在某一行。这会给我从 0 到 blocksize-1 的所有列，我假设那就是所有列。我需要确定从哪里读取内存，那是我数据的起始位置加上哪一行。行步长告诉我每一行在哪里——基本上就是列数。x_pointers 是我需要加载的所有数据的地址。我加载它们。如果被掩蔽，我放入负无穷（这相当于 Softmax 操作中的 0）。然后这部分和天真的 Softmax 本质相同：我计算最大值、减去它、指数化、求和、做除法，然后写回。

---

OK. Yeah. [INAUDIBLE] Yeah, so this is the version where each block can just span the entire row. And you can see that Triton makes this very easy, right. Because this is as if you were just writing normal PyTorch code.

是的，[听不清]。这是每个块可以覆盖整行的版本。你可以看到 Triton 让这变得非常容易，因为这就像你在写普通的 PyTorch 代码一样。

---

So if everything fits in a block, you basically-- the thing is, if you can fit it into a block, you can just write normal PyTorch, almost.

所以如果一切都能放入一个块，基本上——如果你能把它放进一个块，你几乎就可以直接写普通 PyTorch。

---

Yeah? What if my number of columns, the number of rows, are bigger than blocksize? Yeah, so we'll get to that. Now the number of columns, rows, in general, it's going to be much larger than the blocksize. So we'll come back to that, yeah.

嗯？如果我的列数或行数大于 blocksize 呢？是的，我们会讲到。一般情况下，列和行的数量会比 blocksize 大得多。所以我们会回到这个问题。

---

So if you wanted to do a Softmax per column, do you have to do [INAUDIBLE]? So the question is if you want to do Softmax by column. I think that should be fine, because here, we're tracking these pointers, right. So the pointers can be anything. Basically, I think all you would have to do is change the stride here to basically access the columns. Actually, it would be here. The column offsets, you would just multiply this by the row stride, I think.

如果你想对每一列做 Softmax，你是不是必须[听不清]？问题是你想按列做 Softmax。我认为应该没问题，因为我们在跟踪指针，指针可以是任何东西。基本上，你只需要改变步长来访问列。实际上，列偏移量乘以行步长就可以了。

---

OK, let's move on.

好的，我们继续。

---

All right, so now, warming up to the matmul. Suppose that your row doesn't fit into a block. OK, so what do you do in this case? So for example, if you have, let's say, a row that's 4,000 columns, but the blocksize is only 1,024. So you have to do something here. So here's the strategy. We're going to break up the row into tiles. So in this case, there's going to be four tiles. And each thread is going to iterate over the tiles and accumulate a sum. And then finally at the end, we're going to do the reduction by summing everything that each thread produced. So I'll show you an example of this.

好，现在开始升温到矩阵乘法。假设你的行不能放入一个块。这种情况下你怎么办？例如，如果你有一行有 4,000 列，但 blocksize 只有 1,024。你必须做点什么。策略是：我们把行分成多个分块（tiles）。在这个例子中，会有四个分块。每个线程遍历这些分块并累加一个和。最后，我们通过对每个线程产生的所有结果求和来做归约。我给你看一个例子。

---

And now I'm switching from Softmax to row sum because it's just easier to think about.

现在我从 Softmax 切换到行求和（row sum），因为这样更容易思考。

---

OK, so here, OK, well, this is not very interesting. The built-in row sum does what you would expect. So the row sum operation just basically takes a matrix and then computes the sum of each row, OK. So just no surprises there.

这里，内置的行求和做了你期望的事情。行求和操作基本上取一个矩阵，然后计算每行的和。没什么意外。

---

OK, so conceptually what we're going to do here is as follows. OK, so each block is still in charge of one row. So that part hasn't changed. So suppose block one, row one. I wake up, and what do I do? I'm going to remember, now, there's tiles. And suppose tile 0 is columns 0 through 3, tile 1 is columns 4 through 7. And then tile 2 is columns 8 through 11. OK, so what I'm going to do here is that I'm going to iterate now. So first, I basically process this, all the threads. Basically, each thread keeps a kind of accumulator and processes the first tile. And it's going to move on to the next tile, and it's going to add the current element to the accumulator. So here, I'm putting 3, 1, 4, 1. And then the second loop iteration, I'm going to add 5 to this. I get 8. I add 9 to this, I get 10. 2 to 4, and 6 to 1, right.

概念上我们要做的是：每个块仍然负责一行，这部分没有变。假设块一行一。我醒来，我做什么？记住，现在有分块。假设分块 0 是列 0 到 3，分块 1 是列 4 到 7，分块 2 是列 8 到 11。我要做的是迭代。首先，我处理所有这些线程——每个线程保留一个累加器（accumulator）并处理第一个分块。然后移动到下一个分块，将当前元素加到累加器。这里，我放入 3, 1, 4, 1。第二次循环迭代，我将 5 加到第一个得到 8，9 加到第二个得到 10，2 加到 4 得到 6，6 加到 1 得到 7。

---

So each of these four threads is going to be accumulating its own thing. And then at the end, I do another for tile 2. I add 5 and 3 to the respective accumulators. So at the end of the day, I have this, a vector of accumulators. And then that is actually-- that, I can just sum up.

这四个线程每个都在累加自己的东西。然后在最后，我对分块 2 再做一次，将 5 和 3 加到各自的累加器。最终，我得到一个累加器向量。然后我就可以直接求和。

---

OK, so let's see what the code looks like here. So I'm just going to call the row sum kernel. And let's see. OK, so here's what it looks like. So wake up. I am on a particular row. And this is what one row looks like. There's one tile, a second tile, a third tile, and so on. So n is the number of elements of that row. And blocksize is the size of this tile.

让我们看看代码是什么样的。我调用 row_sum_kernel。醒来，我在某一行，这就是一行看起来的样子：有一个分块、第二个分块、第三个分块等等。n 是这行的元素数，blocksize 是这个分块的大小。

---

OK. So remember, blocksize is the number of threads. I'm processing more data than the larger than the blocksize. I just have to do it iteratively now. So I'm going to loop over all of the tiles. So start is going to go from 0 to blocksize to 2 times blocksize, and so on and so forth. So each time I'm jumping across, I am doing calls. Basically get the offsets at the particular tile. And then I'm going to load the data from HBM, and I'm going to add it to the accumulation. So this accumulation is going to be either in registers or shared memory. OK. And then finally after I loop over all the tiles, I process the whole row, I get basically-- for every thread I have accumulator of what that thread has picked up. And I can just do a sum to get a scalar, and I write it out.

记住，blocksize 是线程的数量。我处理的数据比 blocksize 更大，所以我必须迭代地做。我遍历所有分块，start 从 0 到 blocksize 到 2×blocksize，依此类推。每次跳转时，我获取特定分块的偏移量，从 HBM 加载数据，加到累加器中。这个累加器要么在寄存器中，要么在共享内存中。最后，在遍历所有分块后，我处理完整行，每个线程都有一个累加器，我可以求和得到一个标量，然后写出来。

---

OK, so this is a little bit more complicated than before, because now we have a for loop within a thread. And this is necessary when your data doesn't fit within a block.

这比之前稍微复杂一点，因为现在我们在一个线程内有一个 for 循环。当你的数据不能放入一个块时，这是必要的。

---

Yeah? [INAUDIBLE] Just in case we don't have enough register. We have to put it in-- Yeah, so the question is I think if you can control where the accumulator resides. At least in this Triton program, you don't explicitly say. And this is up to the Triton compiler to figure out where to put it. But in general, if the blocksize is large enough, it has to go in shared memory.

嗯？[听不清] 以防我们没有足够的寄存器，我们必须把它放在——问题是关于你是否能控制累加器放在哪里。至少在这个 Triton 程序中，你没有明确指定。这由 Triton 编译器决定放在哪里。但一般来说，如果 blocksize 足够大，它必须放在共享内存中。

---

OK. All right, does this make sense? Just to, I think, make sure people are on the same page. Remember when GeLU, we also split a row into a bunch of pieces. But those were blocks. Right, and so each of those pieces was a block that was processed independently. These are not blocks. These are tiles. The block corresponds to this whole row. And the block has to basically process all the tiles. And so this is where it starts to not look like PyTorch, because you're not able to process all your data in one nice kind of-- not everything fits into shared memory.

好的，这样说得通吗？为了确保大家理解一致。记住在 GeLU 中，我们也把一行分成了很多块，但那些是"块"（blocks）。每一块是被独立处理的。这些不是块——这些是分块（tiles）。块对应整行，块必须处理所有的分块。这就是它开始看起来不像 PyTorch 的地方，因为你不能在一"整块"中处理所有数据——不是所有东西都能放进共享内存。

---

Yeah? [INAUDIBLE] --also stored in shared memory? Yeah. Let's say the accumulator is stored in shared memory.

嗯？[听不清]——也存储在共享内存中？是的。假设累加器存储在共享内存中。

---

OK. All right, so let's now maybe go on to our finale, which is matmul.

好的，现在我们进入压轴部分——矩阵乘法。

---

OK, so matmul, of course, is the bread and butter of deep learning. It's been optimized to death. And it's, in some sense, very fundamental operation. So you take two matrices, you multiply them. I'm going to add a little bit of a twist here. I'm going to do a matmul followed by a ReLU, just because, just for kicks. OK. Well, this happens, right. Because if you have one linear layer, it's a matmul. And then you apply a ReLU activation. So this is not completely out of nowhere. But I'll show you later why I did this.

矩阵乘法当然是深度学习的"面包和黄油"。它已经被优化到了极致。在某种意义上，这是非常基础的操作。你取两个矩阵，把它们乘起来。我这里加一点花样：我做一个矩阵乘法后接一个 ReLU，只是为了好玩。这种情况确实会发生——如果你有一个线性层，它是矩阵乘法，然后应用 ReLU 激活。所以这并非凭空而来。我稍后会告诉你我为什么这样做。

---

OK, so how do you build a matmul kernel? All right, so here's a naive approach. OK, so here's my, let's say, a matrix. I'm multiplying A times B. And I'm trying to write out the matrix C. And A is M by K, B is K by N. So C is M by N. OK, so what I'm going to do is I'm going to fix one of these elements. Let's say M equals 1, N equals 2. OK, so I'm processing-- actually, let's do M equals 1, N equals 1. So I'm doing C5. And then, basically for every k, so I'm going to, yeah, I'm going to iterate over the k, the rows of A and the columns of B. I'm going to read from HBM. I'm going to multiply them, accumulate that. And at the end, I'm going to write out to this and this element. So that is a valid matmul kernel.

那么如何构建一个矩阵乘法核函数？这里有一种天真的方法。假设矩阵 A 乘以 B，我要写出矩阵 C。A 是 M×K，B 是 K×N，所以 C 是 M×N。我要固定其中一个元素，比如 M=1，N=2。实际上，让我们做 M=1，N=1，所以我做 C₅。然后对于每一个 k，我遍历 k——A 的行和 B 的列。我从 HBM 读取，相乘，累加。最后，我写出这个元素。这是一个有效的矩阵乘法核函数。

---

OK. So what's wrong with it? It's correct. But if you look at how many reads and writes it's doing, this is not good. Right, so basically for every M and N and K, I have to read from HBM. So it's on the order of M times K times N reads. Number of writes. I mean, it doesn't matter, but this is the bottleneck, right. And if you remember from the second lecture, if you look at the number of operations you're doing divided by the number of bytes that were transferred, that's the arithmetic intensity which you want to be high. So the number of operations is M times K times N order. And then the number of reads is also the same. So arithmetic intensity is a constant, which is not good.

那么它有什么问题？它是对的。但如果你看它做了多少次读写，这不好。基本上对于每一个 M、N 和 K，我必须从 HBM 读取，所以是 M×K×N 次读取。写的次数无所谓，但这是瓶颈。如果你记得第二讲，你做的操作数除以传输的字节数，就是算术强度（arithmetic intensity），你希望它高。操作数是 M×K×N 量级，读取次数也是同样，所以算术强度是一个常数，这不好。

---

OK, so if you look carefully, you notice that there is a lot of redundant reads. So imagine computing C4. You needed to read A4, A5, and A6. And if you compute C5, you're going to have to read those over again as well. So if you can just read those once, then you really save on reads, and that's great. So let's try to use shared memory to do that.

如果你仔细看，你会发现有很多冗余读取。想象计算 C₄，你需要读取 A₄、A₅、A₆。如果你计算 C₅，你还得再读一遍同样那些。如果你能只读一次，那就大大节省了读取。让我们尝试用共享内存来实现。

---

So here's the idealized approach. I'm going to load all of A and B into shared memory. And then I'm just going to compute C. So if I can do that, then I get-- now I don't have this cubic number of reads, I only get quadratic number of reads, which means I get the error intensity of order n, which in the second lecture, I said was a kind of ideal thing you could hope for. OK, so if you can do that, that's great, because you basically-- there's no redundant reads. You read everything once into shared memory. You do the computation and you write it back.

这是理想化的方法。我将 A 和 B 全部加载到共享内存中，然后直接计算 C。如果我能做到，我就不再有三次方量级的读取，只有二次方量级的读取，这意味着我得到 n 量级的算术强度——在第二讲中我说这是你能期望的理想情况。如果你能做到，那太好了，因为没有冗余读取：你把所有东西一次性读到共享内存，做计算，然后写回。

---

OK, but what's the problem with this idealized approach. The problem is that A and B are usually too large to fit into shared memory. Right. So then, what do you have to do now?

但这个理想化方法有什么问题呢？问题是 A 和 B 通常太大，无法放入共享内存。那么你现在必须做什么？

---

OK, so the idea here is this very classic idea of tiling. And the idea basically is to, well, fit as much as you can to shared memory as you can, essentially. So in some sense, it's going to look like the naive-- it's going to globally look like the naive approach, but locally it look like the idealized approach is the way to think about it.

这里的思路是非常经典的分块（tiling）思想。基本上就是尽可能多地把数据放入共享内存。在某种意义上，全局上看起来像天真的方法，但局部上看起来像理想化的方法——这就是思考方式。

---

So here's the picture. I think Tatsu showed this as well. So what we're going to do is we're going to take this matrix C, and instead-- remember, the naive approach just said for every element, I'm going to compute it. But now I'm going to say for every tile, I'm going to do it. So I break it up into tiles. And each of these tiles is going to be a thread block. And I'm going to have a bunch of threads that is responsible for computing this. Now a different tile is going to be computed completely separately by another thread block.

这是示意图，我想 Tatsu 也展示过。我们要做的是：取这个矩阵 C，天真的方法是对每个元素计算，但现在我对每个分块计算。我把它分成块，每个分块是一个线程块。我有一堆线程负责计算这个。不同的分块由另一个线程块完全独立地计算。

---

OK, so I'm going to-- imagine I'm in Triton. I wake up. I'm looking at this thread block. So what do I have to do? Well, in some sense, it's the same as the naive approach where, for every row tile of A, I'm going to go scan across the rows. And for every column tile of B, I'm going to load the corresponding tile A and the corresponding-- so say I'm here-- and the corresponding tile from B into shared memory. I'm going to multiply these two together. And that's going to be like the idealized approach. And I'm going to accumulate that in the partial sum. And this is all sitting in shared memory. And then after I finish all the sweep of the row and the column here, then I can finally write this output tile to HBM.

想象我在 Triton 中。我醒来，看着这个线程块。我该怎么办？在某种意义上，和天真的方法一样：对于 A 的每个行分块，我扫描行；对于 B 的每个列分块，我把对应的 A 分块和对应的 B 分块加载到共享内存中，把它们乘在一起——就像理想化的方法——累加到部分和中。这一切都在共享内存中。在我完成所有行和列的扫描后，我终于可以把输出分块写入 HBM。

---

OK, so that's the conceptually what's happening. And then the arithmetic intensity here now goes up to order tile size. So you can generally not reach order n, because that would require you to fit everything into shared memory. But if your tiles are big, then that's still not too bad.

这就是概念上的过程。算术强度现在提升到分块大小的量级。你一般达不到 n 量级，因为那需要你把所有东西都放进共享内存。但如果你的分块足够大，那也不算太差。

---

OK, so just as a bonus. While you're doing all writing a kernel for this anyway, sometimes if you want to apply an element-wise activation function, it's very easy to just put it on at the end. And this is kernel fusion.

作为额外的好处：既然你无论如何都在为这个写核函数，有时如果你想应用一个逐元素激活函数，在末尾加上它非常容易。这就是核函数融合（kernel fusion）。

---

OK, so very quickly, the implementation here. So-- oops. OK, so just a reminder about strides since this is going to show up. So a tensor is a multidimensional array. But in memory, it's linearized. And strides of a tensor tells you basically how to map from a multidimensional index such as a row, a column, into an actual index. And basically what you do is multiply the row by the stride, the plus the column by the stride of the column. OK, so in this case, every time you go advance to the next row, you go four positions in your memory. And every time you advance a column, you go one. And if it were to transpose, it would be flipped.

快速讲一下实现。提醒一下关于步长（strides），因为会用到。张量是一个多维数组，但在内存中是线性化的。张量的步长告诉你如何从多维索引（如行、列）映射到实际索引。基本上，你把行乘以行步长，加上列乘以列步长。在这个例子中，每前进一行，你在内存中前进 4 个位置；每前进一列，前进 1 个位置。如果是转置，就会反过来。

---

OK, so what does this kernel look like here? OK, so the launch is not interesting. So you wake up and you are on tile M and N. So it's like OK, I'm responsible for computing the c matrix, but for the M comma N tile there's a bunch of index manipulation which you can-- I'll just gloss through, but it's straightforward but a little bit. You just have to track the indices. So this basically tells you which rows of A, the matrix A, I'm looking at. Which rows of-- oh sorry, which columns of B I'm looking at. And then this is just the numbers 1 through K. Then I'm going to get the pointers into A and B at my tile location. And then I'm going to set up this accumulator matrix. This is going to be in shared memory. It's M by N. And then this is going to look like the row reduction, right. You have this sum over all the tiles. But instead of just going across the tiles, I'm now going across the row tiles and also simultaneously down the column tiles of B. I load A, the small matrix, I load B, the small B tile. And then I perform this dot. So remember, whenever things are in shared memory, things look like PyTorch and I can just say, matmul it, and it will do the thing. And then I advance to the next row tile of A and the next column tile of B. The bonus is that if I wanted to apply element-wise non-linearity, I might as well do that here. Before I write it out to HBM, I can do some any operation on it. And then finally, I just write it out.

这个核函数是什么样子的？启动没什么意思。你醒来，你在分块 M、N 上，你负责计算 C 矩阵的 M,N 分块。有一堆索引操作——我会略过，但很直接。你只需要跟踪索引。这告诉我看的是 A 矩阵的哪些行、B 矩阵的哪些列。然后我在我的分块位置获取指向 A 和 B 的指针。然后设置累加器矩阵——在共享内存中，它是 M×N。这看起来像行归约——你做所有分块上的求和，但现在我不只是横向遍历分块，而是同时横向遍历 A 的行分块和纵向遍历 B 的列分块。我加载小的 A 矩阵和小的 B 分块，然后做点积。记住，当数据在共享内存中时，看起来就像 PyTorch，我只要说 matmul 它就会做。然后我前进到 A 的下一个行分块和 B 的下一个列分块。额外好处是：如果我想应用逐元素非线性激活，我在这里做正好——在写入 HBM 之前，我可以在上面做任何操作。然后最后，我直接写出来。

---

OK, so there's some indices that you have to pay attention to. But hopefully, the form of the algorithm is clear.

有一些索引你需要留意。但希望算法的形式是清晰的。

---

OK. Any questions about that?

有什么问题吗？

---

## Summary / 总结

All right. Maybe I'll just summarize, and you can ask me later. So today, we talked about there's a programming model, which is you're talking about either PyTorch or Triton or ptx. This is what the kind of programmer can control. Right, and even ptx. You can write ptx and you can control every-- specialize however you want. But this is not the full picture, because the reality is that your code has to run on hardware, and there's only a finite number of SMs, a finite number of banks, and sizing of memory and registers. All are finite. So you come in with your big matrix and transformer, and want to-- it has to fit in with the constraints of the hardware. So that's why benchmarking and profiling are really important to understand how the messiness of the hardware translates to performance.

好，我总结一下，你们可以稍后问我。今天我们讨论了编程模型——你可以用 PyTorch、Triton 或 ptx。这是程序员可以控制的东西。即使是 ptx，你可以编写 ptx 并控制每一个细节，按你的意愿特化。但这还不是全部，因为现实是你的代码必须在硬件上运行，而只有有限数量的 SM、有限数量的存储体、有限的内存和寄存器大小。所有东西都是有限的。所以你带着你的大矩阵和 Transformer 进来，它必须适应硬件的约束。这就是为什么基准测试和性能分析对于理解硬件的"凌乱性"如何转化为性能非常重要。

---

We talked about Triton, which is, I think, a pretty nice, neat language to think about thread blocks. Hopefully by now you can appreciate that things are easier to think about thread blocks than individual threads, because you don't have to think about explicitly synchronizing threads or doing shared memory. And the way to think about it is that you figure out-- you have your computation. You break it down into the thread blocks where you just need to read from shared memory. Do some stuff, and write it back into HBM. And then we saw some examples of increasing difficulty. Element wise is the easiest. And then reduction over a row. Reduction where it doesn't fit into a row. And we introduced the baby tiling. And then matmul is the canonical example where you actually do tiling.

我们讨论了 Triton，我认为这是一个非常漂亮、简洁的语言，用于思考线程块。希望到现在你们能欣赏到，用线程块思考比用单个线程思考更容易，因为你不需要考虑显式地同步线程或管理共享内存。思考方式是：你有了计算任务，把它分解成线程块——你只需要从共享内存读取，做一些事情，然后写回 HBM。然后我们看到了一系列难度递增的例子：逐元素是最容易的，然后是行上的归约，行放不下的归约——我们介绍了"入门级"分块，然后矩阵乘法是你实际做分块的典型例子。

---

OK, so that's all I'm going to say about how to program a single GPU. Next time, we're going to go to more GPU and talk about multi-GPU programming.

这就是我要讲的关于如何对单个 GPU 编程的全部内容。下次我们会讲更多 GPU 的内容，讨论多 GPU 编程。

---

Yeah, question. So if I want to write down kernels, what are the alternatives? Do I have to try them and-- for each of my choices that I have, how close can I get to the optimal level? So the question is, what are alternatives to Triton? So there's a trade off between-- every language has an inductive bias, right. That makes certain things easier and certain things harder. So most of what we do-- Triton was built by people who train transformers. So anything involving transformers, I think it's going to be relatively easy there. Of course, in the extreme, you can always go to ptx and write that. But I wouldn't advise that as a first step. There are a bunch of other libraries. There's thunder kittens. There's cute, delirious DSLs that allow you to give you-- they're not necessarily comparable either up or down the stack. They just give you different characteristics.

嗯，问题。如果我想编写核函数，有哪些替代方案？我是否必须尝试它们——对于每个选择，我能多接近最优水平？问题是，Triton 的替代方案是什么？每种语言都有归纳偏好（inductive bias），使某些事情更容易，另一些更难。Triton 是由训练 Transformer 的人构建的，所以任何涉及 Transformer 的事情，用它都相对容易。当然，极端情况下你总是可以写 ptx，但我不建议作为第一步。还有很多其他库：ThunderKittens、CUTLASS、各种 DSL。它们不一定在栈上可比，只是给你不同的特性。

---

Yeah? Do you have a high dimensional tensor magnification or high dimensional tensor processing? What is the best approach? What I'm thinking is can I load unload the whole sensor, both of the sensors on bunch of threads or thread blocks on my GPU at the same time and compute them? Or would it be better to take each element, just what we did here, right. A particular component of my sensor, then process it and then write it back in the end. Yeah, so briefly, the question-- and we should probably wrap up-- is, is it better to read all at once or maybe process individual elements at a time? I think it's hard to answer this in the abstract. It depends on the nature of the computation. Maybe we can talk offline about that.

嗯？你处理高维张量有什么最佳方法？我在想，我是否可以同时加载整个张量、两个张量到一堆线程或线程块上并计算？还是每个元素逐个处理更好？简短来说，问题是——我们可能该结束了——是一次性读取所有内容好，还是逐个处理元素好？我认为很难抽象地回答这个问题，取决于计算的性质。也许我们可以线下讨论。

---

OK, all right. See you next time.

好的，下次见。
