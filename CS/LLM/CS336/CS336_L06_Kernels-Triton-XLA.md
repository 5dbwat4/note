---
title: "Lecture 6: Kernels, Triton, XLA"
---

# Lecture 6: Kernels, Triton, XLA / 第六讲：核函数、Triton、XLA

---

## 1. GPU Hardware Overview / GPU 硬件概览

So welcome back, everyone. On Monday, Tatsu did an excellent job of describing a high-level overview of GPUs and how to think about performance and all the quirks that come with GPUs. This lecture is going to be a continuation of that, where we're going to dive more deeply into the code, write some Triton kernels, and as well as do some benchmarking and profiling.

欢迎大家回来。周一 Tatsu 出色地讲解了 GPU 的高层概览，以及如何思考性能以及 GPU 带来的各种特性。本讲是上一讲的延续，我们将更深入地深入到代码中，编写一些 Triton 核函数，并进行基准测试和性能分析。

So just to refresh what's going on with GPUs, here is a simplified diagram of what a typical GPU looks like. There's memory, and then the actual GPU chip. And just to keep in your head what are the characteristics of a GPU. We're talking about NVIDIA GPUs, but Tatsu also talked about CPUs, and there's AMD and so on. But focusing on NVIDIA GPUs, we've had multiple generations, from A100s, to H100s, to B200s. In each generation, you have a GPU with a number of Streaming Multiprocessors, or SMs. The number of SMs is about 100 to 200, so that hasn't really changed that much.

回顾一下 GPU 的结构，这是一个典型 GPU 的简化示意图。有内存，然后是实际的 GPU 芯片。我们需要记住 GPU 的特征。当然我们讨论的是 NVIDIA GPU，但 Tatsu 也讲到了 CPU，还有 AMD 等等，但重点放在 NVIDIA GPU 上。我们经历了多代产品，从 A100 到 H100 再到 B200。每一代 GPU 都有一定数量的流式多处理器（SM）。SM 的数量大约在 100 到 200 之间，这其实变化不大。

Within the individual SM, there's a set of registers. B200s have 65,000 registers for a total of 256K per SM. This also hasn't changed that much. In addition, there's a L1 cache as well as shared memory. Remember, these are the same memory—shared memory you can control, L1 you can't. This is per SM, and this is in the same ballpark of size. Then there's L2 cache, which is not per SM but for the whole chip, and this is a bit larger. Finally, you have High Bandwidth Memory, or HBM, which is large, and you see that this is the number that's actually going up quite a bit.

在单个 SM 内部，有一组寄存器。B200 每 SM 有 65,000 个寄存器，总计 256K。这也变化不大。此外，还有 L1 缓存和共享内存。记住，它们使用同一块内存——共享内存你可以控制，L1 你无法控制。这是每个 SM 独有的，大小在同一个数量级。然后还有 L2 缓存，它不是按 SM 分而是整个芯片共享的，稍大一些。最后还有高带宽内存（HBM），容量很大，而且可以看到这个数字实际上在快速增长。

In addition to size, you can think about what's happening with the bandwidth. Essentially, it's inversely correlated. Registers are very fast, L1 is slightly less fast, L2 is less fast, and HBM is the slowest. Although eight terabytes a second is still not that slow in the grand scheme of things. So this is the main hierarchy you should have in your head: large memory is slow and far but big, and fast memory like registers and L1 resides on the SM—it's local, fast, but small.

除了大小之外，还可以考虑带宽的情况。基本上，这是反相关的。寄存器非常快，L1 稍慢，L2 更慢，HBM 最慢。虽然从大局来看，每秒 8 TB 也不算慢。所以这是你应该记住的主要层次结构：大容量内存慢且远但容量大，而寄存器、L1 等快内存位于 SM 上——它们是本地的、快的，但容量小。

---

## 2. GPU Programming Model / GPU 编程模型

How do you program a GPU? The program model is as follows. There are notions of threads, where each thread executes a piece of code on a small part of the data. These threads are organized into thread blocks, also known as Concurrent Thread Arrays (CTAs), which are groups of threads. Finally, you have a collection of thread blocks which forms the grid. When you launch a kernel, you're basically launching a grid of threads and thread blocks to all simultaneously do some computation in parallel.

如何为 GPU 编程？编程模型如下。有线程的概念，每个线程在一小部分数据上执行一段代码。这些线程被组织成线程块（thread block），也称为并发线程数组（CTA），即一组线程。最后，线程块的集合构成了网格（grid）。当你启动一个核函数时，你基本上是在启动一个由线程和线程块组成的网格，让它们全部同时并行地执行某些计算。

There are some other things happening. For example, H100s and B200s also have thread block clusters, which are clusters of thread blocks that enable some amount of distributed memory. Also, B200s have tensor memory for tensor cores, which is somewhere between registers and shared memory. Some of these things are invisible to the programmer, but they are in the hardware. But we won't worry about them for this intro lecture.

还有一些其他机制。例如，H100 和 B200 还有线程块集群（thread block clusters），即通过集群实现的、支持一定量分布式内存的线程块组。此外，B200 还有用于 Tensor Core 的 tensor memory，它介于寄存器和共享内存之间。有些东西对程序员是不可见的，但确实存在于硬件中。不过在本入门讲座中我们不必关心这些。

Why do we have thread blocks? Why can't we just have a grid of threads, and each thread just takes a piece of data and does something? This would be normally fine if all you want to do is element-wise operations, which we'll see. For example, GeLU is an activation function that applies element-wise, and threads are pretty natural—each thread processes one element. But for operations that involve communicating with threads, such as softmax or matrix multiplication, this view isn't really enough. The reason is that, well, it could be enough if you were willing to pay the cost of writing and reading HBM. But as we've noticed, HBM is very slow, so this would not be a good strategy.

为什么需要线程块？为什么不能只有一个线程网格，每个线程取一块数据并做计算？如果你只做逐元素操作，这通常是没问题的。例如，GeLU 是一个逐元素应用的激活函数，线程模型很自然——每个线程处理一个元素。但对于需要线程间通信的操作，如 Softmax 或矩阵乘法，这种视图就不够了。原因是——如果你愿意承担读写 HBM 的代价，其实也可以做到。但正如我们所知，HBM 非常慢，所以这不是一个好策略。

Instead, what we should do is use shared memory, which is local to the SM. What the thread block allows you to think about is a collection of threads that are all going to access this shared memory. A thread block is being scheduled on one of these streaming multiprocessors, and what it's going to do is read a bunch of data from HBM, process it—where the processing might involve communication between the threads via the shared memory—and then write it back out. This is a critical piece that comes up. Later, we'll talk about tiling, and that's the whole game here.

相反，我们应该使用共享内存，它对 SM 是局部的。线程块让你能够思考的是一组都将访问这块共享内存的线程。一个线程块被调度到某个 SM 上，它将从 HBM 读取一批数据，然后进行处理——处理可能涉及线程之间通过共享内存的通信——然后再写回去。这是非常关键的一点。稍后我们将讨论分块（tiling），这正是一切的核心。

In Triton, which we'll see as a primary way we're going to write kernels these days, we're going to think natively in thread blocks. Once you get the hang of thinking of thread blocks, this makes a lot of sense and makes your life a lot easier. So the programming model is fairly simple—there's threads, thread blocks, and grids.

在 Triton 中——我们将看到它是当前编写核函数的主要方式——我们将原生地以线程块为单位进行思考。一旦你习惯了以线程块的方式思考，一切都会变得非常合理，让你的工作轻松很多。所以编程模型其实是相当简单的——有线程、线程块和网格。

---

## 3. Interaction Between Programming Model and Hardware / 编程模型与硬件的交互

Things get a bit more complicated with the interaction between the programming model and the hardware. The programming model is actually very nice—it provides abstraction of the hardware. When you write a kernel, all you have to know is that there's a bunch of thread blocks. You define them and what computations each thread within the block has to do. That's like writing Python, so that part isn't hard. In fact, if you just care about correctness, that's all you need to know. But in practice, the performance is very sensitive to the hardware, so you need to really deeply understand the hardware to obtain high performance. The whole reason we're talking about GPUs and kernels is that you're trying to squeeze out performance.

当编程模型与硬件交互时，事情变得稍微复杂些。编程模型其实非常好——它提供了硬件的抽象。当你编写核函数时，你只需要知道有一堆线程块，你定义它们以及块内每个线程要做什么计算。这就像写 Python 一样，所以这部分不难。事实上，如果你只关心正确性，这足够了。但在实践中，性能对硬件非常敏感，因此你需要深入理解硬件才能获得高性能。我们讨论 GPU 和核函数的全部原因正是为了榨取性能。

There are two levels here: you're trying to understand the computation through the programming model, but how fast it runs is strongly dependent on the hardware. I'm going to give you some examples of why this matters, and some of this will be review from what Tatsu talked about.

这里有两个层次：你通过编程模型理解计算，但运行速度如何强烈依赖于硬件。我将给出一些例子说明为什么这很重要，其中一些内容是对 Tatsu 所讲内容的复习。

### 3.1 Warps and Occupancy / Warp 与占用率

There's something called warps. In the very simplified view, warps are not really part of the clean picture of the programming model. Technically, you can also access the warps, but you don't have to when you're just programming. So what is a warp? Each thread block is a collection of threads, but these threads are actually grouped into warps. There are basically 32 threads per warp. For example, if you have 64 threads in a thread block, there's two warps—the first 32 and the second 32.

有一种叫做 warp 的东西。在非常简化的视图中，warp 并非编程模型这幅清晰图景的一部分。技术上你可以访问 warp，但通常编程时不需要。那么什么是 warp？每个线程块是一组线程，但这些线程实际上被分组成 warp。每个 warp 基本上有 32 个线程。例如，如果一个线程块有 64 个线程，就有两个 warp——前 32 个和后 32 个。

As Tatsu mentioned, all threads within a warp must execute the same instruction in lockstep on the SM. Every cycle, they have to execute exactly the same instruction. Control divergence is when different threads within a warp need to execute different instructions. For example, if you have branching—if something, then A else B—what happens is that you can only do the A's in your threads in your warp, and then you do the B. This gets sequential, which is bad and inefficient, and that's why branching is something you want to generally avoid.

正如 Tatsu 上次提到的，一个 warp 中的所有线程必须在 SM 上以锁定步调（lockstep）执行相同的指令。每个周期，它们必须执行完全相同的指令。控制分歧（control divergence）指的是一个 warp 中不同线程需要执行不同指令的情况。例如，如果你有分支——if something then A else B——那么你的 warp 中的线程只能先做 A，然后再做 B，这就变得串行了，这是不好且低效的，因此你通常要避免分支。

One thing that's really cool about warps is that an SM is actually running multiple warps. There's a warp scheduler, and there are a bunch of resident warps that are about to run. Each warp has some registers, and the SM can switch between them with zero cost. This is not true in general, like on a CPU, but this design is to hide latency. One of the warps might be reading from HBM, which can take 100 cycles or something—you don't want to just sit around waiting. You switch immediately to another warp that can do some tensor core operations.

warp 的另一个很酷的特点是，SM 实际上同时在运行多个 warp。有一个 warp 调度器，有一批准备好运行的常驻 warp。每个 warp 有一些寄存器，而 SM 可以在它们之间以零代价切换。这在 CPU 上一般并非如此，但 GPU 的这种设计是为了隐藏延迟。其中一个 warp 可能在读 HBM，这可能需要 100 个周期——你不希望干等着那个 warp 什么都不做，你立即切换到另一个可以执行 Tensor Core 操作的 warp。

Another reason why warp comes up is this idea of occupancy—more specifically, warp occupancy. The hardware constraint says that each thread can use at most 255 registers. The SM has a fixed number of registers, so the more registers each thread is using, the fewer threads you can have. That can reduce your occupancy. But that's not necessarily bad, because if you have fewer threads but each thread is doing more work, that can actually be good. Occupancy is something you can measure, but it's not necessarily "the larger, the better."

warp 的另一个重要性是占用率（occupancy）的概念，更具体地说是 warp 占用率。硬件约束规定每个线程最多可以使用 255 个寄存器。SM 有固定数量的寄存器，因此每个线程使用的寄存器越多，你能拥有的线程就越少，这可能会降低占用率。但这不一定不好，因为你可能有更少的线程但每个线程做更多的工作，这实际上是好事。占用率是可以测量的，但不见得越大越好。

An example where you might want to have fewer threads is thread coarsening. Let's say you have an element-wise operation and you can have one thread process one element, giving you a lot of threads. But you can also say each thread processes multiple elements, like eight. That gives you fewer threads, making scheduling easier, but each thread does more work. If your threads are very light, maybe you want to fatten them up a little bit.

一个你可能希望拥有更少线程的例子是线程粗化（thread coarsening）。假设你有一个逐元素操作，你可以让一个线程处理一个元素，这样就有很多线程。但你也可以让每个线程处理多个元素，比如八个。这样线程数更少，调度更容易，但每个线程做更多工作。如果你的线程非常轻量，也许你应该让它们"加粗"一些。

### 3.2 Bank Conflicts / Bank 冲突

Something called bank conflicts applies to shared memory. Shared memory is like L1, it's on an SM. The way the hardware works is that shared memory is divided into 32 banks, each one four bytes wide. There's a constraint that every clock cycle, each bank can be accessed by at most one thread. If multiple threads try to access the same bank, the accesses have to be serialized—this is called a bank conflict. In the worst case, if you had a matrix and 32 threads all try to access the first column, they'd just wait in line. This is a 32-way bank conflict, the worst possible setting.

一种叫做 bank 冲突的概念适用于共享内存。共享内存像 L1 一样，在 SM 上。硬件的工作方式是共享内存被分成 32 个 bank，每个 4 字节宽。有一个约束是每个时钟周期每个 bank 最多只能被一个线程访问。如果多个线程试图访问同一个 bank，访问就必须串行化——这叫 bank 冲突。最坏情况下，假设有一个矩阵，32 个线程都试图访问第一列，它们就只能排队等待。这是 32 路 bank 冲突，是最糟糕的情况。

For element-wise operations, it's fine—you can go in any order. But if you're doing matmuls, you can't control for every matrix which row major or column major you're doing. There are some solutions, like swizzling, which arranges your shared memory so that when you're going through, you can avoid bank conflicts.

对于逐元素操作来说没问题——你可以任意顺序访问。但如果你在做矩阵乘法（matmul），你无法为每个矩阵控制是按行优先还是列优先存储。有一些解决方案，比如 swizzling，它重新排列共享内存的布局以避免 bank 冲突。

### 3.3 Memory Coalescing / 内存合并

When you have 32 threads in a warp trying to access HBM, the memory accesses get combined into a transaction of 128 bytes, called cache lines, and it fetches it all at once. In the best case, called full coalescing, all the threads are accessing the same cache line. So thread 1 accessing M00, thread 2 accessing M01, and so on—all at once, you grab this entire cache line. Whereas if you go down the columns, you're going to fetch a lot of memory that you're not going to use. This feels similar to bank conflicts, but it's a very different constraint—bank conflicts are about shared memory, and coalescing is about HBM.

当一个 warp 中的 32 个线程试图访问 HBM 时，内存访问实际上被合并成一个 128 字节的事务，称为缓存行（cache line），一次性全部获取。在最佳情况下，称为完全合并（full coalescing），所有线程访问的都是同一个缓存行。线程 1 访问 M00，线程 2 访问 M01，以此类推——一次性获取整个缓存行。而如果你按列访问，你会获取大量用不到的内存。这感觉和 bank 冲突类似，但这是完全不同的约束——bank 冲突关乎共享内存，内存合并关乎 HBM。

### 3.4 Block Occupancy / 块占用率

Thread blocks are scheduled onto SMs. You can logically define as many thread blocks as you want, but physically on chip, you only have a certain number of SMs—for example, 148. If you launch 160 thread blocks, you can only schedule 148 of them, then wait until they're done to schedule the remaining 12. But when you schedule those 12, a bunch of SMs are just not doing anything. That's called low occupancy—when the last wave of thread blocks gets fewer than the total maximum number of thread blocks. In general, it's a good idea to make the number of thread blocks divide the SMs.

线程块被调度到 SM 上。你在逻辑上可以定义任意多的线程块，但在物理芯片上，你只有一定数量的 SM——例如 148 个。如果你启动 160 个线程块，只能调度其中 148 个，等它们完成后再调度剩余的 12 个。但当这 12 个运行时，有一堆 SM 什么都不做。这就是低占用率——当最后一批线程块的数目少于 SM 最大可调度数时。通常来说，让线程块的数量能被 SM 数量整除是个好主意。

### 3.5 Summary of Hardware Considerations / 硬件考虑小结

There is a very elegant programming model: a grid of thread blocks, each with individual threads. HBM is global to everyone, shared memory is local to a thread block, and registers are local to a thread. But all the details of the hardware—warps, bank conflicts, memory coalescing, occupancy—really determine performance. Many of these details are hard to know because profiling tells you a bunch of information, but you have to know exactly how many SMs there are and the sizing of everything. Sometimes the scheduler does something you don't really have control over. So it's a little messier than the programming model.

编程模型非常优雅：一个由线程块组成的网格，每个线程块中有独立的线程。HBM 对所有人全局可见，共享内存对线程块局部可见，寄存器对线程局部可见。但硬件的所有细节——warp、bank 冲突、内存合并、占用率——真正决定了性能。很多这些细节难以知晓，因为性能分析只给你一堆信息，但你需要确切知道有多少 SM 以及一切的尺寸。有时调度器会做一些你无法真正控制的事情，所以实际情况比编程模型更为混乱。

---

## 4. Benchmarking and Profiling / 基准测试与性能分析

Now I'm going to talk about benchmarking and profiling. I want to emphasize the philosophy here: here's a recipe for success—you benchmark and profile your code, make changes, and benchmark and profile again. The reason I'm doing benchmarking and profiling as opposed to teaching you Triton earlier is that you should always just measure what's going on in your code and figure out what the bottlenecks are before you start writing kernels.

现在我来谈谈基准测试（benchmarking）和性能分析（profiling）。我想强调这里的理念：成功的秘诀是——你对代码进行基准测试和性能分析，做出修改，然后再进行基准测试和性能分析。我之所以先讲基准测试和性能分析，而不是先教 Triton，是因为你始终应该在开始编写核函数之前，先测量代码中发生了什么并找出瓶颈所在。

Benchmarking is basically how long things take. It gives you an end-to-end time but doesn't tell you where time is spent. Nonetheless, it's pretty useful because that's ultimately what you care about—how long things run. It also lets you see how things scale with dimension. There are nice tools for benchmarking, but because this class is language models from scratch, I'm going to do it from scratch. But I'm doing it to highlight a few gotchas with benchmarking.

基准测试基本上是测量事情花费多长时间。它给你端到端的时间，但不告诉你时间花在哪里。尽管如此，这相当有用，因为这最终是你关心的——程序运行了多久。它还能让你看到程序如何随维度扩展。有很好的基准测试工具，但因为这门课是"从零构建语言模型"，我也将从零实现。但这样做是为了强调基准测试中的几个陷阱。

Let's say we have matrix multiplication. You run operation to instantiate two random square matrices of size dimension by dimension, and it returns a function to perform the operation. To benchmark: the naive thing is to just start time, run it, stop time. But there are a few things. One is that always remember to do your warm-up. This is because some things are lazily compiled, and you want to make sure that compile time doesn't factor in—you care about how fast something runs repeatedly, not the initial conditions. You often want to time it multiple times because there is variance. The proper way is to use CUDA events—start and end events—record on them, do the computation, then synchronize to wait for CUDA threads to finish (because everything on the GPU is async), and then record the time. Then you can take the average.

假设我们有矩阵乘法操作。运行一个操作来实例化两个 dimension × dimension 的随机方阵，返回执行该操作的函数。如何进行基准测试？幼稚的做法是记录开始时间、运行、记录结束时间。但有几件事要注意：首先始终记得做预热（warm-up），因为有些东西是惰性编译的，你要确保编译时间不计入——你关心的是重复运行时的速度，而不是初始条件。通常你需要多次计时，因为存在方差。正确的方式是使用 CUDA 事件——开始事件和结束事件——在它们上面调用 record，执行计算，然后同步等待 CUDA 线程完成（因为 GPU 上的一切是异步的），最后记录时间。然后可以取平均值。

With benchmarking, you can scale up your matrices and see how time changes. For matrix multiplication, as expected, it should grow cubically. But notice there's a flaw where up until almost 2,000 dimensional matrices, things are basically constant. This is because, as discussed, GPU shapes are built for fairly large matmuls—if you have a 2 by 2 matrix, it's going to be very inefficient.

通过基准测试，你可以放大矩阵并观察时间如何变化。对于矩阵乘法，正如预期的那样，它应该呈三次方增长。但注意有一个缺陷：直到接近 2,000 维矩阵之前，时间基本恒定。这是因为，正如我们讨论过的，GPU 是为相当大的矩阵乘法而设计的——如果你有一个 2×2 的矩阵，效率会非常低。

Profiling tells you where time is actually spent. Even if you don't care about the time, profiling helps you figure out what's actually happening under the hood. Especially with high-level languages, you write some code, it runs, you get a result—sometimes it's good to understand what's actually going on. PyTorch has a built-in profiler. In your assignment, you'll use Nsight, which gives more details.

性能分析告诉你时间实际花在哪里。即使你不关心耗时，性能分析也能帮助你搞清楚底层到底在发生什么。特别是在高层语言中，你写了代码，它运行了，你得到了结果——有时理解底层实际发生了什么是有好处的。PyTorch 有内建的性能分析器。在你的作业中，你将使用 Nsight，它提供更多细节。

Let's look at what the profile looks like for just A + B in PyTorch. Normally you don't think about it—two tensors get added. But underneath the hood, there is a kernel called `cuda functor add`, which is a kernel that adds two tensors. What about matmul? When you do `A @ B` in PyTorch, there is a long name describing the particular matmul kernel—Cutlass f32, 64x64x16, etc. If you change the dimensions, you get a different kernel. Underneath the hood, PyTorch looks like you're just doing @, but there could be all sorts of things happening.

让我们看看 PyTorch 中仅做 A + B 时的性能分析结果是什么样的。通常你不会多想——两个张量被相加了。但在底层，有一个叫作 `cuda functor add` 的核函数。那矩阵乘法呢？当你在 PyTorch 中做 `A @ B` 时，有一个长长的名字描述这个特定的 matmul 核函数——Cutlass f32, 64x64x16 等等。如果你改变维度，你会得到不同的核函数。在底层，PyTorch 看起来像你只是在做 @，但实际可能有很多不同的事情在发生。

Cutlass is the NVIDIA CUDA library for linear algebra. SM100 corresponds to the Blackwell architecture, so this is a kernel specifically designed for Blackwell. f32 is the data type, and 64x64x16 is the shape of the tile, which we'll talk about later when we discuss tiling in the context of matmuls.

Cutlass 是 NVIDIA 用于线性代数的 CUDA 库。SM100 对应 Blackwell 架构，所以这是一个专门为 Blackwell 设计的核函数。f32 是数据类型，而 64x64x16 是分块（tile）的形状，我们稍后在讨论 matmul 的分块时会讲到。

---

## 5. GeLU Example: Naive vs Built-in vs Compiled / GeLU 示例：朴素实现 vs 内建实现 vs 编译实现

The GeLU activation function is a typical non-linearity, often approximated with the tanh approximation for efficiency. Naively, you can implement GeLU in PyTorch by just taking the equation and putting it into PyTorch. PyTorch also has a built-in `F.gelu`. And there's also something important: you can take any PyTorch function, call `torch.compile` on it, and it generates another function that does the same thing. So we have three horses in this race: the naive implementation, the built-in, and the compiled implementation.

GeLU 激活函数是典型的非线性函数，通常用 tanh 近似来提高计算效率。幼稚的做法是直接在 PyTorch 中实现 GeLU——取张量，把公式写进 PyTorch 即可。PyTorch 也有内建的 `F.gelu`。还有一个重要的东西：你可以对任何 PyTorch 函数调用 `torch.compile`，它会生成另一个做同样事情的函数。所以这场比赛中有三匹马：朴素实现、内建实现和编译实现。

When you benchmark them: the naive one is slow, the built-in is much faster, and the compiled is also much faster but not quite as fast as built-in. So what's happening? Why are these things different? They all compute the same answer but have wildly different performance characteristics.

当你对它们进行基准测试时：朴素实现很慢，内建实现快得多，编译实现也快得多，但可能不如内建实现快。那么发生了什么？为什么它们不同？它们计算出相同的答案，但性能特征差异巨大。

If you pull up the profiler: the naive GeLU shows a bunch of different kernels—binary functor, unary add, tanh—corresponding to the fact that in PyTorch, each primitive in the computation graph is realized as a kernel. The reason this is slow is that when you launch a kernel, it has to read from HBM, pull it over to the SM, compute, write back; then the next kernel picks it up from HBM, writes back, and so on. You're doing a lot of reads and writes back and forth. Between kernel invocations, things have to go back to HBM.

当你打开性能分析器时：朴素 GeLU 显示了一堆不同的核函数——binary functor、unary add、tanh——这对应了在 PyTorch 中，计算图中的每个原语实际上都实现为一个核函数。它之所以慢是因为当你启动一个核函数时，它必须从 HBM 读取数据，搬到 SM，计算，写回去；然后下一个核函数再从 HBM 取出，写回去……如此反复。你在做大量来回的读写，因为在核函数调用之间，数据必须回到 HBM。

The built-in one shows a single GeLU CUDA kernel implementation. Someone wrote a kernel for GeLU and put it in the standard library—nothing magical. The compiled version is really interesting. It takes the naive implementation with its computation graph and runs a compiler—underneath the hood, it's just a single Triton kernel. The compiler looked at the computation graph and essentially wrote that kernel in Triton. So the naive implementation has multiple kernels, requiring multiple reads and writes to and from HBM—no kernel fusion. The built-in and compiled versions have one kernel: all the operations in the GeLU have been fused together into one kernel. You read from HBM once, write to HBM once per element.

内建版本显示了一个单一的 GeLU CUDA 核函数实现。有人为 GeLU 编写了一个核函数并放入了标准库——没什么神奇的。编译版本非常有趣。它拿了朴素实现及其计算图，运行一个编译器——在底层，它只是一个单一的 Triton 核函数。编译器查看计算图，本质上将其写入了一个 Triton 核函数。所以朴素实现有多个核函数，需要多次从 HBM 读写——没有核函数融合（kernel fusion）。内建和编译版本只有一个核函数：GeLU 中的所有操作都被融合（fuse）在了一起。每个元素只需读一次 HBM，写一次 HBM。编译出来的核函数是一个 Triton 核函数。

---

## 6. Introduction to Triton / Triton 简介

Let's write some Triton kernels. Remember our programming model: threads organized by thread blocks, and a grid of thread blocks. If you were to write in CUDA, the mental model is "what does each thread do?" You write code that has an ID identifying which thread you're talking about and executes the code. The nice thing is it's closely related to what's actually happening under the hood with fine-grained control. But the cons: some operations require threads to communicate, so they must synchronize, read from HBM, synchronize, compute—you have to do that bookkeeping.

我们来写一些 Triton 核函数。回顾我们的编程模型：线程按线程块组织，有一个线程块组成的网格。如果你用 CUDA 编写，心智模型是"每个线程做什么？"你写一段代码，有某种标识线程序号的 ID，然后执行代码。好处是这与底层实际发生的事情密切相关，提供了细粒度的控制。但缺点是：有些操作需要线程之间通信，因此它们必须同步——读取 HBM、同步、计算，你必须处理这些事务。

Triton was developed by OpenAI and has become pretty standard. You basically specify what each thread block does. Generally it's powerful enough, especially for this class. The conceptual framework is: what does a block do? A block loads data into shared memory, operates on it, and writes it back to global memory. These blocks are an intermediate point between thinking about what individual elements are doing and thinking about the general operation. In PyTorch, you define huge matrices and multiply them—that's the atomic operation. Triton is a hybrid between that and individual elements.

Triton 由 OpenAI 开发，现在已经成为相当标准的工具。你基本上指定每个线程块做什么。对于本课程来说，它已经足够强大。概念框架是：一个块做什么？一个块将数据加载到共享内存中，对其操作，然后写回全局内存。在某种意义上，这些块是思考单个元素做什么和思考整体操作之间的中间层次。在 PyTorch 中，你定义巨大的矩阵并告诉相乘——那是原子操作。Triton 是那种方式和单个元素之间的混合体。

### 6.1 GeLU Kernel in Triton / Triton 中的 GeLU 核函数

Let's define an 8,000 dimensional vector and start writing some Triton. In Triton, we're not thinking functionally anymore—you have to explicitly read and write, with no returning value. I'll allocate an output tensor for the kernel to write to. Since the tensor is too big to fit into one SM, I need to break it up into blocks. Total elements is 8,000, block size is 1,024, giving eight blocks.

我们定义一个 8,000 维的向量，开始写一些 Triton 代码。在 Triton 中，我们不再以函数式的思维思考——你必须显式地读和写，没有返回值。我分配一个输出张量供核函数写入。由于张量太大无法放入一个 SM，我需要将其分成块。总共 8,000 个元素，块大小为 1,024，于是有八个块。

Then I use the special syntax `TritonGeLUKernel[(num_blocks,)](x, y, num_elements, BLOCK_SIZE)` to call the kernel. The bracket tells the shape of the grid—basically saying the grid has `num_blocks` blocks, and for each block, invoke this function.

然后我使用特殊语法 `TritonGeLUKernel[(num_blocks,)](x, y, num_elements, BLOCK_SIZE)` 来调用核函数。方括号内告诉网格的形状——基本上说网格有 `num_blocks` 个块，对每个块调用这个函数。

In the kernel itself: `x` and `y` are now pointers (addresses, essentially integers). The way to think about it is that for every block, this function is called. First, I figure out who I am: `pid = tl.program_id(0)` identifies the block (0, 1, 2, ...). Then `start = pid * BLOCK_SIZE` is the offset into x. `offsets = start + tl.arange(0, BLOCK_SIZE)` gives the integer indices. If the tensor size doesn't divide evenly by block size, you need masking—a boolean mask that's true for valid positions and false for the overflow of the last block.

在核函数内部：`x` 和 `y` 现在是指针（本质上是整数地址）。思考方式是对于每个块，这个函数被调用。首先，我搞清楚我是谁：`pid = tl.program_id(0)` 标识了块（0, 1, 2, ...）。然后 `start = pid * BLOCK_SIZE` 是 x 中的偏移量。`offsets = start + tl.arange(0, BLOCK_SIZE)` 给出整数索引。如果张量大小不能被块大小整除，你需要掩码——一个布尔掩码，有效位置为真，最后一个块超出部分为假。

Then: `x_vec = tl.load(x_ptr + offsets, mask=mask)` reads from HBM, you do the computation, and `tl.store(y_ptr + offsets, y_vec, mask=mask)` writes back to HBM. This is the simplest kernel pattern: wake up, figure out indices, read, compute, write.

然后：`x_vec = tl.load(x_ptr + offsets, mask=mask)` 从 HBM 读取，你做计算，然后 `tl.store(y_ptr + offsets, y_vec, mask=mask)` 写回 HBM。这是最简单的核函数模式：醒来、确定索引、读取、计算、写入。

### 6.2 ptx Code / ptx 代码

When you write Triton, the compiler generates ptx code, which is an intermediate assembly language for GPUs. If you look at what a thread is actually doing (not a thread block—that's been compiled away): you see `LD global` which loads from HBM into registers (denoted `r` for integer, `fr` for floating point). Then statements like `mov 0, r5`, multiplications, and finally `global store` writing back to HBM. This is the actual code executed on a thread.

当你写 Triton 时，编译器生成 ptx 代码，这是一种 GPU 的中间汇编语言。如果你看一个线程实际在做什么（不是线程块——那已经被编译消除了）：你会看到 `LD global`，它从 HBM 加载到寄存器（`r` 表示整数寄存器，`fr` 表示浮点寄存器）。然后有 `mov 0, r5` 等语句，乘法，最后是 `global store` 写回 HBM。这是实际在线程上执行的代码。

One observation: you see evidence of thread coarsening—rather than processing a single element, one thread processes eight elements. The compiler decided this thread is lightweight, so it thickens it up. The code is compiled once, and each thread runs the same piece of code, distinguishing itself by thread ID (`cta.x` is the block index, `tid.x` is the thread index). Looking at ptx gives you appreciation for what's going on under the hood. There are still many things not specified in ptx—which SM things operate on, warps, etc.—these are hardware-controlled.

一个观察：你可以看到线程粗化的证据——一个线程处理的不是单个元素，而是八个元素。编译器判断这个线程太轻量了，于是把它"加粗"。代码只编译一次，每个线程运行相同的代码片段，通过线程 ID 来区分自己（`cta.x` 是块索引，`tid.x` 是线程索引）。查看 ptx 代码能让你理解底层发生了什么。ptx 中仍有很多未指定的东西——比如在哪个 SM 上运行、warp 等——这些由硬件控制。

---

## 7. Softmax Triton Kernel (Row Fits in Block) / Softmax Triton 核函数（行能放入块中）

So far we looked at element-wise operations. Now let's think about operations that aggregate over multiple values. Softmax exponentiates and normalizes each row of a matrix. The naive PyTorch implementation involves computing max per row (for numerical stability), subtracting, exponentiating, summing normalization constants, and dividing. If you count reads and writes: each operation is a different kernel, each reading and writing to HBM—about 5MN reads and 3MN writes. In principle, you should have much fewer.

到目前为止我们看的是逐元素操作。现在考虑聚合多个值的操作。Softmax 对矩阵的每一行求指数并归一化。朴素的 PyTorch 实现包括：对每行计算最大值（为了数值稳定性）、减去最大值、逐元素指数化、求和得到归一化常数、最后相除。数一数读写次数：每个操作都是不同的核函数，每个都要读写 HBM——大约 5MN 次读和 3MN 次写，原则上应该比这少得多。

In Triton, the form is very similar to GeLU. Each row is a block. Softmax is not element-wise but row-wise—blocks don't interact, and there's no shared memory across blocks. I allocate the output tensor, define `BLOCK_SIZE` as the number of columns (next power of 2 for good luck), and `num_blocks` is the number of rows. I pass input and output pointers plus strides to tell how far to move down.

在 Triton 中，形式上与 GeLU 非常相似。每一行是一个块。Softmax 不是逐元素的，而是逐行的——块之间不交互，块之间没有共享内存。我分配输出张量，定义 `BLOCK_SIZE` 为列数（取下一个 2 的幂为好），`num_blocks` 为行数。我传递输入和输出指针以及步长（stride）来告诉如何向下移动。

In the kernel: I wake up on a particular row. I read all columns using pointer arithmetic with row stride. If masked out, I put `-inf` as the Softmax equivalent of 0. Then the core computation looks just like the naive Softmax: compute max, subtract, exponentiate, sum, divide, and write back. If everything fits in a block, you can basically write normal PyTorch-like code.

在核函数中：我在某一行上醒来。我使用带行步长的指针运算读取所有列。如果被掩码遮挡，我放入 `-inf` 作为 Softmax 中 0 的等价。然后核心计算和朴素 Softmax 完全一样：计算最大值、减去、指数化、求和、相除，然后写回去。如果一切都能放入一个块，你基本上可以像写普通 PyTorch 代码一样。

---

## 8. Row Sum with Tiling (Row Doesn't Fit in Block) / 带分块的行求和（行无法放入块中）

Suppose your row doesn't fit into a block—for example, 4,000 columns but block size only 1,024. The strategy: break the row into tiles (four tiles in this case). Each thread iterates over the tiles and accumulates a sum. At the end, we reduce by summing everything each thread produced. I'm switching from Softmax to row sum because it's conceptually simpler.

假设你的行装不进一个块——例如 4,000 列但块大小只有 1,024。策略是：将行分成多个分块（tile）（在这种情况下是四块）。每个线程遍历各个分块并累积一个和。最后，通过将每个线程产生的结果求和来进行归约（reduction）。我从 Softmax 切换到行求和因为它概念上更简单。

Each block is still in charge of one row. I wake up, and now there are tiles. I iterate: first tile—all threads process their elements and keep accumulators; move to next tile—add to accumulators; and so on. At the end, I have a vector of accumulators, which I sum up to get a scalar and write out. This introduces a for-loop within a thread, necessary when your data doesn't fit within a block.

每个块仍然负责一行。我醒来，现在存在分块。我循环：第一个 tile——所有线程处理各自元素并保持累加器；移到下一个 tile——加到累加器上；以此类推。最后，我得到一个累加器向量，把它们求和得到标量并写出。这在线程内引入了 for 循环，当你的数据无法放入一个块时，这是必要的。

Note the distinction: in GeLU we also split a row into pieces, but those were blocks processed independently. Here, tiles are different from blocks. The block corresponds to the whole row, and the block has to process all the tiles sequentially. This is where it starts not looking like PyTorch because not everything fits into shared memory. The accumulator resides either in registers or shared memory—in this Triton program you don't explicitly control it; that's up to the Triton compiler.

注意区分：在 GeLU 中我们也把一行分成许多片段，但那些是块，各自独立处理。而这里的 tile 不同于块。块对应于整行，而块必须依次处理所有的 tile。这就是它开始不像 PyTorch 的地方——因为不是所有数据都能放入共享内存。累加器驻留在寄存器或共享内存中——在这个 Triton 程序中你不会显式指定；这由 Triton 编译器决定。

---

## 9. Matrix Multiplication Kernel with Tiling / 带分块的矩阵乘法核函数

Matmul is the bread and butter of deep learning. Take two matrices A (M×K) and B (K×N), multiply to get C (M×N). The naive approach: for each element of C, iterate over K—read from HBM, multiply, accumulate, write. This is correct but inefficient: for every (M, N, K) you read from HBM—on the order of M×K×N reads. Arithmetic intensity (operations divided by bytes transferred) is constant, which is not good.

矩阵乘法（matmul）是深度学习的核心操作。取两个矩阵 A (M×K) 和 B (K×N)，相乘得到 C (M×N)。朴素方法：对 C 的每个元素，遍历 K——从 HBM 读取、相乘、累加、写入。这正确但低效：对每个 (M, N, K) 都要从 HBM 读取——大约 M×K×N 次读。算术强度（操作数除以字节传输数）是常数，这不好。

If you look carefully, there are redundant reads. Computing C4 and C5 both need to read A4, A5, A6. If you could read those once, you save on reads. The idealized approach: load all of A and B into shared memory, then compute C. Now you get quadratic reads instead of cubic—arithmetic intensity of order N, which is ideal. But the problem is that A and B are usually too large to fit into shared memory.

如果你仔细观察，会有冗余读取。计算 C4 和 C5 都需要读取 A4、A5、A6。如果你只读这些数据一次，就能节省很多读取。理想化方法：将 A 和 B 全部加载到共享内存中，然后计算 C。这样你只有平方次读数而不是三次方——算术强度为 O(N)，这是理想情况。但问题是 A 和 B 通常太大，无法放入共享内存。

This is where the classic idea of tiling comes in. Fit as much as you can into shared memory. Globally it looks like the naive approach, but locally it looks like the idealized approach. Break matrix C into tiles—each tile is a thread block. You wake up on a tile (M, N). You scan across the rows of A and columns of B, loading the corresponding A tile and B tile into shared memory, multiplying them together (like the idealized approach), accumulating into a partial sum in shared memory. After the full sweep, write the output tile to HBM.

这就是经典的分块（tiling）思想。尽可能多地把数据放入共享内存。全局看来像朴素方法，但局部看来像理想化方法。把矩阵 C 分解成 tile——每个 tile 是一个线程块。你在一个 tile (M, N) 上醒来。你扫描 A 的行和 B 的列，将对应的 A tile 和 B tile 加载到共享内存中，将它们相乘（像理想化方法），累加到共享内存中的部分和中。完成全部扫描后，将输出 tile 写入 HBM。

The arithmetic intensity now goes up to order tile size. You generally cannot reach order N because that would require fitting everything into shared memory, but if your tiles are large enough, that's still good.

此时算术强度提升到 O(tile size)。通常你不能达到 O(N) 因为那需要将所有数据放入共享内存，但如果 tile 足够大，依然很不错。

### 9.1 Kernel Fusion: Matmul + ReLU / 核函数融合：矩阵乘法 + ReLU

While you're writing a kernel for matmul anyway, if you want to apply an element-wise activation like ReLU, it's very easy to just put it on at the end before writing to HBM. This is kernel fusion. The bonus: before writing the accumulator out to HBM, you can apply any element-wise operation right there—fully fused.

既然你已经在写 matmul 的核函数了，如果你想在最后应用一个逐元素激活函数如 ReLU，只需在写入 HBM 之前加上即可。这就是核函数融合（kernel fusion）。额外好处：在将累加器写出到 HBM 之前，你可以直接在那里应用任何逐元素操作——完全融合。

### 9.2 Strides / 步长

A tensor is a multidimensional array but in memory it's linearized. Strides tell you how to map from a multidimensional index to an actual memory index: multiply the row by row stride plus the column by column stride. Every time you advance to the next row, you advance by the row stride in memory; every time you advance a column, you advance by the column stride. Transposing flips these.

张量是多维数组，但在内存中是线性化存储的。步长（stride）告诉你如何将多维索引映射到实际内存索引：行乘以行步长加列乘以列步长。每次前进到下一行时，你在内存中前进行步长个位置；每次前进一列时，前进列步长个位置。转置则会翻转它们。

The kernel launch sets up the grid: you wake up on tile (M, N), compute which rows of A and columns of B you're looking at, set up an accumulator matrix in shared memory, and then loop over tiles just like the row reduction example. You load the small A tile, load the small B tile, perform `tl.dot(a, b)`—when things are in shared memory, it looks like PyTorch—and accumulate. Then advance to the next row tile of A and next column tile of B. Finally, apply optional element-wise non-linearity and write out.

核函数启动时设置网格：你在 tile (M, N) 上醒来，计算出你要看 A 的哪些行和 B 的哪些列，在共享内存中设置累加器矩阵，然后类似行归约例子一样在 tile 上循环。你加载小的 A tile，加载小的 B tile，执行 `tl.dot(a, b)`——当数据在共享内存中时，看起来就像 PyTorch——并累加。然后前进到 A 的下一个行 tile 和 B 的下一个列 tile。最后，可选项是应用逐元素非线性操作，然后写出。

---

## 10. Summary / 总结

Today we talked about a programming model—PyTorch, Triton, ptx—what the programmer can control. But this is not the full picture because your code has to run on hardware with a finite number of SMs, banks, memory sizes, and registers. You come with your big matrix and transformer, and it has to fit within the constraints of the hardware. That's why benchmarking and profiling are really important—to understand how the messiness of hardware translates to performance.

今天我们讨论了编程模型——PyTorch、Triton、ptx——这些是程序员可以控制的部分。但这不是全貌，因为你的代码必须在硬件上运行，而硬件上有有限数量的 SM、bank、内存大小和寄存器。你带着你的大矩阵和 Transformer 来了，它们必须符合硬件的约束。这就是为什么基准测试和性能分析真的很重要——理解硬件的复杂性如何转化为性能。

We talked about Triton, which is a pretty nice, neat language to think about thread blocks. Hopefully by now you can appreciate that things are easier to think about in thread blocks than individual threads, because you don't have to think about explicitly synchronizing threads or managing shared memory. The way to think about it: figure out your computation, break it down into thread blocks where you just need to read from HBM, do some stuff, and write it back.

我们讨论了 Triton，这是一种相当好的、简洁的以线程块为中心思考的语言。希望到现在你可以体会到，用线程块思考比用单个线程思考更容易，因为你不需要显式地考虑同步线程或管理共享内存。思考方式是：理清你的计算，把它分解成线程块，每个块只需从 HBM 读取、做一些事情、再写回。

We saw examples of increasing difficulty: element-wise is the easiest, then reduction over a row, reduction where it doesn't fit into a row (introducing baby tiling), and matmul is the canonical example where you actually do full tiling. Next time, we'll go to multi-GPU programming.

我们看到了难度递增的示例：逐元素操作最简单，然后是行上的归约，数据不能放入一行的归约（引入初级分块），而矩阵乘法是真正进行完整分块的经典例子。下次课我们将转向多 GPU 编程。

---

## Q&A Highlights / 问答精选

**Q: What are alternatives to Triton?** Every language has an inductive bias making certain things easier and certain things harder. Triton was built by people who train transformers, so anything involving transformers is relatively easy. In the extreme you can always go to ptx, but I wouldn't advise that as a first step. There are other libraries—ThunderKittens, Cute, various DSLs—that give you different characteristics, not necessarily comparable up or down the stack.

**Q: Triton 的替代方案是什么？** 每种语言都有其归纳偏置，使某些事情更容易，某些更难。Triton 是由训练 Transformer 的人构建的，所以涉及 Transformer 的任何东西应该都相对容易。极端情况下你总是可以退回到 ptx 并写 ptx，但我不建议作为第一步。还有一堆其他库——ThunderKittens、Cute、各种 DSL——它们给你不同的特性，不能在堆栈层级直接比较。

**Q: Is ptx code generated by the compiler, or something you would normally code?** There are people who do write ptx if they think they're better than the compiler. NVIDIA compilers are generally pretty mature, but for some less developed accelerators, sometimes you have to reach in and handhold a bit more. Generally, you shouldn't need to do that.

**Q: ptx 代码是由编译器生成的，还是你通常会手写的？** 确实有人写 ptx，如果他们自认为比编译器更强。NVIDIA 编译器通常已经很成熟，但对于一些不太成熟的加速器，有时你确实需要介入并手动优化。一般来说，你不应该需要这样做。

**Q: Is it better to read all at once or process individual elements at a time?** It's hard to answer in the abstract—it depends on the nature of the computation.

**Q: 是一次性全部读取好还是逐个元素处理更好？** 在抽象层面上很难回答——这取决于计算的性质。详见下次课程中关于多 GPU 编程的内容。
