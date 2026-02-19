---
title: Computer Architecture
---

ENIAC（1946）第一台电子计算机 ，很原始，但奠定了计算机发展的基础。

Von Neumann（冯·诺依曼）提出了冯·诺依曼架构，成为现代计算机的基础模型。

IO <-> CPU <-> MEM


address -> data

data和code区分开来：一个二进制有什么意义取决于我们怎么解释它


DMA：Direct Memory Access，直接内存访问，允许外设直接与内存交换数据，减轻CPU负担。


Add a Layer：内存层次：寄存器、缓存、主存、磁盘  

cache

why it works: temporal locality, spatial locality

Moore's Law：晶体管密度每18个月翻一番，但时钟频率提升受限于功耗问题。   

所以提出了SMP（对称多处理器）和多核处理器的概念。


1. 计算机体系结构简介  
- 课程信息：Computer System II，Wenbo Shen  
- 参考资料来源：OSC, Henri Casanova  



2. ENIAC（1946）  
- 第一台电子计算机  
- 技术特点：真空管、穿孔卡  
- 尺寸与速度对比  
- 编程方式：接线编程  



3. 冯·诺依曼  
- 约翰·冯·诺依曼加入ENIAC  
- 冯·诺依曼架构的提出  
- 埃克特-莫奇利奖  
- 冯·诺依曼模型的核心组成  



4. 冯·诺依曼模型  
- 基本构成：CPU、内存、I/O系统  
- 现代计算机的延续与变化  
- 示例：外部设备与控制器  



5. 内存中的数据存储  
- 信息的二进制表示  
- 字节与比特  
- 地址与寻址  
- 处理器的读写指令  



6. 内存的概念视图  
- 地址与内容的对应关系  
- 示例：内存内容读写  



7–9. 内存中的代码与数据  
- 程序加载后的地址空间  
- 代码与数据的区别  
- 示例地址空间布局  



10. CPU的作用  
- CPU作为内存状态的转换器  
- 指令集与数据含义  



11–18. CPU的组成  
- 程序计数器（PC）  
- 寄存器  
- 控制单元  
- 算术逻辑单元（ALU）  
- 当前指令寄存器  
- 缓存结构  
- CPU整体架构示意图  



19–20. 取指-译码-执行周期  
- 基本流程说明  
- 现代计算机的变体与优化  
- 流水线与多核执行  



21–22. 直接内存访问（DMA）  
- DMA的作用与优势  
- DMA控制器与CPU的协作  
- 内存总线竞争与优先级管理  



23–27. 内存层次结构  
- 慢速RAM的应对策略  
- 内存层次：寄存器、缓存、主存、磁盘  
- 缓存的工作原理  
- 时间局部性与空间局部性  
- 缓存命中与未命中  
- 内存技术参数表  



28–29. 摩尔定律  
- 摩尔定律的提出与误解  
- 晶体管密度与性能趋势  
- 时钟频率与功耗的限制  



30–33. 多处理器与多核系统  
- 对称多处理器（SMP）  
- 缓存一致性问题  
- 多核芯片的出现背景  
- 多核系统架构示意图  



34. 重点回顾  
- 内存地址与CPU架构  
- 取指-译码-执行周期  
- 冯·诺依曼模型总结  



35. 延伸学习建议  
- 推荐教材：Patterson & Hennessy  
- 课程作业：阅读CSAPP相关章节  
- 实践建议：安装Linux、构建内核  
-----


## Fetch-Decode-Execute
This is only a simplified view of the way things work
The "control unit" is not a single thing
Control and data paths are implemented by several complex hardware components
There are multiple ALUs, there are caches, there are multiple CPUs in fact ("cores")
Execution is pipelined: e.g., while one instruction is fetched, another is executed
Decades of computer architecture research have gone into improving performance, thus often leading to staggering hardware complexity
Doing smart things in hardware requires more logic gates and wires, thus increasing processor cost
But conceptually, fetch-decode-execute is it

## Direct Memory Access
- DMA is used in all modern computers
- It's a way for the CPU to let memory-I/O operations (data transfers) occur independently
- Say you want to write 1 GiB from memory to some external device like a disk, network card, graphics card, etc.
- The CPU would be busy during this slow transfer
- Load from memory into registers, write from registers to disk, continuously
- Instead, a convenient piece of hardware called the DMA controller can make data transfer operations independently of the CPU
- The CPU simply "tells" the DMA controller to initiate a transfer
- Which is done by writing to some registers of the DMA controller
- When the transfer completes, the DMA controller tells the CPU "it's done" (by generating an interrupt)
- More on interrupts later
- In the meantime, the CPU can do useful work, e.g., run programs

## DMA is not completely free
- To perform data transfers the DMA controller uses the memory bus
- In the meantime, the code executed by the CPU likely also uses the memory bus
- Therefore, the two can interfere
- There are several modes in which this interference can be managed
- - DMA has priority
- - CPU has priority
- But in general, using DMA leads to much better performance

## Coping with Slow RAM
- Everybody would like to have a computer with a very large and very fast memory
- Unfortunately, technology (affordably) allows for either slow and large or fast and small
- We need large main memories for large programs and data
- Therefore, from the CPU's perspective, main memory is slooooooow
- What we do: we play a trick to provide the illusion of a fast memory
- This trick is called the memory hierarchy

## The Memory Hierarchy
- fast ← → slow
- small ← → large
- Registers → Cache → CPU → Memory bus → Memory → I/O bus → I/O devices
- reference: Register reference → Cache reference → Memory reference → Disk reference
- Speed: 0.25 ns (Registers) → 1 ns (Cache) → 100 ns (Memory) → 5 ms (Disk)
- Size: 500 bytes (Registers) → 64 KB (Cache) → 512 MB (Memory) → 100 GB (Disk)
- Real-world has multiple levels of caches (L1, L2, L3)
- Chunks of data are brought in from far-away memory and are copied and kept around in nearby memory
- Yes, the same data exists in multiple levels of memory at once
- Miss: when a data item is not found in a level (e.g., L1 cache miss)
- Hit: when a data item is found in a level (e.g., L2 cache hit)

## Why Does it Work?
- **Temporal Locality**: a program tends to reference addresses it has recently referenced
- The first access, you pay the cost of going to far-away/slow memory to fetch the counter's content
- Subsequent accesses are fast
- This is the "I need that book again" analogy
- **Spatial Locality**: a program tends to reference addresses next to addresses it has recently referenced
- The first access of array element i may be costly
- But the first access of array element i+1 is fast (in the chunk)
- This is the "I need another book on that same shelf" analogy

## Caching
- Whenever your program accesses a byte of memory what happens is:
- That byte's value is brought from slooooow memory into the fast cache
- byte values around the byte you accesses are also brought from slooooow memory into the fast cache
- Analogy:
- You need a book from the library
- You go there and find the book on the many shelves of the library
- You bring back home all books on that shelf and put them on your own bookshelf in your house
- Next time you need that book or one of the books "around it", it will take you no time at all to get it
- Presumably all books on a shelf at the library are about the same topic, so you'll need the books around the book you wanted in the first place