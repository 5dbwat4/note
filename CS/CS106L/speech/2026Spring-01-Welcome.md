---
title: "Lecture 01 · Welcome 逐字稿"
createAt: 2026/9/13
---

# Lecture 01: Welcome（逐字稿）

> 对应课件转写：[2026Spring-01-Welcome.md](../output/2026Spring-01-Welcome.md)

## 1. 本讲概览（Slides 1–2）

本讲为 CS106L 的课程导论，由 Rachel Fernandez 与 Preston Seay 共同主讲。课件首页残留 "Fall 2025" 字样，系模板未更新所致，本课程实际为 Spring 2026 学季。按课件议程（agenda），本讲依次包含课程人员介绍（Introductions）、课程主旨陈述（The Pitch）与课程事务说明（Course Logistics）三部分。其中 Slides 3–6 为教师自我介绍与课堂交流环节，不含实质技术内容，本稿不再展开；Course Logistics 部分则压缩为文末第 10 节的书面要点。本讲的技术主体是 The Pitch，即从应用领域、历史演进与语言设计三个层面论证系统学习 C++ 的价值。

## 2. The Pitch：为什么学习 C++（Slides 7–18）

课件以设问 "Why C++?" 开启这一部分，并给出凝练的回答：C++ 是 "the invisible foundation of everything"（一切事物的隐形地基，Slide 9）。"隐形"的含义在于：C++ 程序通常作为其他软件系统的底层支撑而存在，使用者长期受益于它，却难以直接察觉它。为佐证这一定位，课件依次列举了多个依赖 C++ 的工业领域。

电子游戏是最直观的例证。Valorant（Slide 10）与 CS:GO/CS2（Slide 11）等竞技类游戏对帧率与延迟的要求极为苛刻，渲染、物理模拟与网络同步均须充分利用硬件性能，这正是 C++ 的典型应用场景。同类作品还包括 Fallout、Grand Theft Auto V、Skyrim、Assassin's Creed、PUBG 与 Fortnite（Slide 12）。

高频交易（High Frequency Trading，Slide 13）领域以 Optiver、Citadel、HRT 为代表。该行业的交易速度以微秒计，系统性能直接决定盈亏，因而必须以 C++ 这类能够精确控制性能的语言实现。

自动驾驶（Slide 14）以 Tesla 与 Waymo 为代表。车载实时系统对响应确定性与性能开销均有严格要求，其核心软件大量采用 C++。

嵌入式领域（Slide 15）以 Arduino 开发板为代表：此类硬件的内存以 KB 计，C++ 兼具贴近硬件的操作能力与较小的运行时开销，是这类平台的自然选择。

GPU 编程（Slide 16）以 NVIDIA 的 CUDA 生态为代表，而 CUDA 程序的主流编写语言正是 C++。

上述列举并未穷尽。Slide 17 给出了更广的清单：数据库（MySQL、MongoDB）、浏览器（Chrome、Safari、Edge）、虚拟现实设备（Quest）、底层机器学习框架（PyTorch、TensorFlow）、编译器与虚拟机（JVM、LLVM、GCC）以及操作系统（Windows、MacOS、Linux）。这些系统中的相当部分，其自身即以 C/C++ 实现。Slide 18 重申开篇引语，与 Slide 9 首尾呼应：C++ 之所以"隐形"，恰因为它构成了整个软件生态的地基。

## 3. C++ 的能力特征与行业地位（Slides 19–21）

在应用领域之外，课件进一步归纳了 C++ 在编程语言层面的能力定位（Slide 19），共三点：能够处理海量数据（handling lots of data）；能够高效地处理（handling it very efficiently）；并且能够以优雅、可读的方式完成（doing it in an elegant, readable way）。三点的组合构成 C++ 区别于其他语言的坐标：汇编或 C 可以满足前两点，但大型项目难以保持优雅；许多高级语言便于表达，性能却难以企及；C++ 的目标是三者兼得。

工业界的采用情况与此一致：Amazon、Meta、Apple、Google 均将 C++ 作为主要开发语言之一（Slide 20）。

时间维度上的证据来自 TIOBE 编程语言排行榜（Slide 21）：C++ 于 1985 年首次发布，至 2026 年 3 月仍位列第 3（rating 8.18%），前两位分别是 Python（21.25%）与 C（11.55%），Java（7.99%）居第 4；与 2025 年 3 月相比，C++ 的排名由第 2 降至第 3。一门发布逾四十年的语言长期稳定于前三名，说明其所占据的生态位具有持续的现实需求。

## 4. C++ 标准的演进（Slide 22）

C++ 的生命力还有制度层面的支撑（Slide 22）。C++ 拥有规模庞大的用户群体（user base）；更重要的是，C++ Standard 至今仍以三年为周期修订一次，由 standards committee（标准委员会）决定语言层面的变更。课件的时间线显示：该语言的源头可追溯至 1979 年，1983 年出现 C++ 的最初形态，此后依次发布 C++98、C++03、C++11、C++14、C++17、C++20 与 C++23；时间线右端标注 "We are here!" 的位置即下一个版本 C++26。本课程所讲授的 modern C++ 由此延伸至当前最前沿的标准。

## 5. What is C++：三种合法的 Hello World（Slides 23–26）

课件在 "What is C++?" 一节（Slide 23）没有给出抽象定义，而是给出三段均可编译通过的 Hello World 程序，从语言边界的角度刻画 C++ 的面貌。

第一段是典型的现代 C++ 写法（Slide 24）：

```cpp
#include <iostream>
#include <string>

int main() {
    auto str = std::make_unique<std::string>("Hello World!");
    std::cout << *str << std::endl;
    return 0;
}

// Prints "Hello World!"
```

对该程序可作如下分析：`auto` 指示编译器依据初始化表达式推导变量 `str` 的类型；`std::make_unique<std::string>("Hello World!")` 在堆上构造 `std::string` 对象，并将该对象的所有权交由智能指针（smart pointer）管理；`std::cout << *str` 借助流插入运算符将解引用得到的字符串写入标准输出流，`std::endl` 追加换行并刷新输出缓冲区。此例涉及的机制将在后续章节系统展开。

第二段表明 C++ 对 C 的兼容性（Slide 25）：

```cpp
#include "stdio.h"
#include "stdlib.h"

int main(int argc, char *argv) {
    printf("%s", "Hello, world!\n");
    // ^a C function!
    return EXIT_SUCCESS;
}
```

其中的 `printf` 是纯粹的 C 标准库函数（代码注释亦标注 "^a C function!"），`EXIT_SUCCESS` 同样来自 C 的头文件。这段代码可以不经修改地由 C++ 编译器编译，印证了课件旁注的结论："C++ is backwards compatible with C"——C++ 向后兼容 C，存量 C 代码由此可以直接进入 C++ 工具链。附带说明：按照惯例，`main` 的第二个参数应声明为字符指针数组 `char *argv[]`；课件代码写作 `char *argv`，本稿照录以与课件保持一致。

第三段以另一种方式完成同样的输出（Slide 26）：

```cpp
#include "stdio.h"
#include "stdlib.h"

int main(int argc, char *argv) {
    asm(".LC0:\n\t"
            ".string \"Hello, world!\"\n\t"
        "main:\n\t"
            "push rbp\n\t"
            "mov rbp, rsp\n\t"
            "sub rsp, 16\n\t"
            "mov DWORD PTR [rbp-4], edi\n\t"
            "mov QWORD PTR [rbp-16], rsi\n\t"
            "mov edi, OFFSET FLAT:.LC0\n\t"
            "call puts\n\t");
    return EXIT_SUCCESS;
}
```

该程序不调用任何 C 或 C++ 的输出函数，而是通过 `asm` 内联汇编直接书写 x86 指令：字符串常量 `.LC0` 先行定义；随后建立栈帧（`push rbp`、`mov rbp, rsp`）并预留 16 字节栈空间（`sub rsp, 16`），将主函数收到的两个参数分别存入栈槽——`edi`（即 argc）存入 `[rbp-4]`，`rsi`（即 argv）存入 `[rbp-16]`；最后将字符串 `.LC0` 的地址装入 `edi`，调用库函数 `puts` 完成输出。这一示例说明：在 C++ 中，程序员可以下沉到机器指令层面，获得对程序行为的完全控制。

## 6. 从汇编到 C 再到 C++（Slides 27–34）

C++ 何以能够同时容纳上述三种写法，需要从语言的历史演进中寻找解释。

汇编阶段的 Hello World 以 x86 NASM 语法书写如下（Slide 27）：

```nasm
section .text
global _start                         ;must be declared for linker (ld)
_start:                               ;tell linker entry point
    mov edx,len                       ;message length
    mov ecx,msg                       ;message to write
    mov ebx, 1                        ;file descriptor (stdout)
    mov eax, 4                        ;system call number (sys_write)
    int 0x80                          ;call kernel
    mov eax, 1                        ;system call number (sys_exit)
    int 0x80                          ;call kernel

section .data
    msg db 'Hello, world!' ,0xa       ;our dear string
    len equ $ - msg                   ;length of our dear string
```

该程序将消息长度装入 `edx`、字符串地址装入 `ecx`，将 `ebx` 置为标准输出（stdout）的文件描述符，将 `eax` 置为系统调用号 `sys_write`，随后经 `int 0x80` 陷入内核完成写出；退出程序时，须再次将 `eax` 置为 `sys_exit` 并触发同一系统调用路径。仅为打印一行文本，就需要直接组织寄存器与系统调用。

课件将汇编语言的优势归纳为三点（Slide 28）：指令极其简单（unbelievably simple instructions）；书写得当时速度极快（extremely fast）；程序员对程序拥有完全的控制（complete control）。在此基础上，Slide 29 提出问题：既然如此，为什么不始终使用汇编（Why don't we always use assembly?）。Slide 30 给出 Compiler Explorer（godbolt.org）的在线演示链接，可用于观察编译器将高级语言翻译为汇编的实际过程。汇编的劣势则在 Slide 31 补全：即使是极简单的任务也需要大量代码（a lot of code）；代码极难理解（very hard to understand）；可移植性极差（extremely unportable）——更换 CPU 架构即意味着指令集整体不同，程序必须重写。

1972 年，Dennis Ritchie 创造了 C 语言（Slide 32）。C 使程序员能够写出同时具备三类性质的代码：快速（fast）、简洁（simple）、跨平台（cross platform）。其中跨平台能力由编译器（compilers）实现：同一份源代码（source code）由各平台的编译器翻译为该平台自身的汇编。课件注明这一主题将在 CS107 中深入展开。

C 之所以广受欢迎，重要原因在于其可预测性。课件引用 Linux 的创造者 Linus Torvalds 的话（Slide 33）："When I read C I know what the output Assembly is going to look like"（阅读 C 代码时，我能够预见其编译产出的汇编形态）。与此同时，C 的局限同样明确：不支持对象（objects）与类（classes）；难以编写泛型（generic）或模板（templated）代码；编写大型程序十分繁琐（tedious）。

1983 年，丹麦计算机科学家 Bjarne Stroustrup 开始创造 C++（Slide 34）。他期望这门语言在保留 C 已有的快速、易用与跨平台特性的同时，具备高层特性（high level features），即在 C 的性能世界中引入高级抽象。

## 7. C++ 的设计哲学（Slides 35–37）

上述设计目标在语言层面落实为一组明确的设计哲学（Slide 35）：

- 用代码直接表达思想与意图（Express ideas and intent directly in code）；
- 尽可能在编译期（compile time）实施安全约束（Enforce safety at compile time whenever possible）；
- 不浪费时间与空间（Do not waste time or space）；
- 将混乱易错的构造封装隔离（Compartmentalize messy constructs）；
- 给予程序员完全的控制、责任与选择（Allow the programmer full control, responsibility, and choice）。

Bjarne Stroustrup 的下述表述可视为这套哲学的凝练（Slide 36）："Code should be elegant and efficient; I hate to have to choose between those"（代码应当既优雅又高效；我不愿在二者之间取舍）。Slide 37 进一步将五条哲学概括为五个关键词：Readable（可读）、Safety（安全）、Efficiency（高效）、Abstraction（抽象）与 Programmer Choice（程序员选择权）。这组原则为后续各讲评估具体语言特性提供了参照框架。

## 8. 三种风格的再审视（Slides 38–40）

设计哲学最终需要回到代码中检验。课件将第 5 节的三段程序按风格重新归类（Slides 38–40），展示同一门语言内部的表达光谱。

Assembly style（Slide 38）即前述内联汇编版本，对应哲学中的 Programmer Choice：当需要完全控制时，C++ 提供直达机器指令的途径。C style（Slide 39）即调用 `printf` 的版本，对应 C++ 对 C 的向后兼容：存量 C 代码可以在 C++ 体系中继续使用。真正的 C++ style（Slide 40）则为：

```cpp
#include <iostream>
#include <string>
int main() {
    auto str = std::make_unique<std::string>("Hello World!");
    std::cout << *str << std::endl;
    return 0;
}
// Prints "Hello World!"
```

课件在该版本上标注了四个核心机制：`std::make_unique<std::string>` 体现智能指针（Smart Pointers）；`<std::string>` 的尖括号语法体现模板（Templates）；`std::cout` 体现流（Streams）；`<<` 之所以能用于向流写入数据，依赖的是运算符重载（Operator Overloading）。这四个主题均是本课程后续章节的正式内容。

## 9. CS106L 的课程价值（Slides 41–46）

在语言层面的论证之后，课件转向课程本身：为什么选修 CS106L（Slide 41）。其论证可归纳为四点。

第一，课程覆盖的完整性（Slide 42）。本学期的主题依次为：Welcome；Types & Structs；Initialization & References；Streams；Containers；Iterators & Pointers；Classes；Advanced Classes；Templates；Advanced Templates；Functions & Lambdas；Operator Overloading；Special Member Functions；Move Semantics；`std::optional` 与 Type Safety；最后收束于 RAII、Smart Pointers 与 C++ Projects。第 5 节示例中出现的四个机制均在此序列之内。

第二，与其他课程的分工（Slide 43）。以 CS106B 为代表的课程重点在于概念——抽象、递归、指针等思想，C++ 只是"够用即可"的最小工具，且时间投入较重；CS106L 的焦点则是代码本身：什么样的代码是好的，强大（powerful）而优雅（elegant）的代码具有怎样的形态。课程不使用任何 Stanford 自制库，只使用标准库（STL），要求理解 C++ 的实现方式（how）与设计缘由（why）。同时它是一门负担较轻的 1 unit 课程。

第三，实际用途（Slide 44）。修读者至少会在 Stanford 的一门课程中使用 C++，包括 CS 111（Operating Systems Principles，操作系统原理）、CME 213（基于 MPI、openMP 与 CUDA 的并行计算导论）、CS 143（Compilers，编译器）、CS 144（Introduction to Computer Networking，计算机网络导论）、CS 248A（Computer Graphics: Rendering, Geometry, and Image Manipulation，计算机图形学）、MUSIC 256A（Music, Computing, Design）等；此外还包括真实的工业环境。

第四，编程习惯（coding hygiene）的养成（Slide 45）。课件指出，C++ 训练促使程序员持续自问三类问题：是否按照对象的设计意图使用对象——对应类型检查（type checking）与类型安全（type safety）；是否高效地使用内存——对应引用/拷贝语义（reference/copy semantics）与移动语义（move semantics）；是否修改了不应修改的对象——对应 `const` 与 const 正确性（const correctness）。许多语言放松了这些约束，而 C++ 要求程序员显式面对它们。

本节以 Bjarne Stroustrup 的另一句话作结（Slide 46）："Nobody should call themselves a professional if they only know one language"（若只掌握一门语言，便不应自称专业人士）。

## 10. 课程信息概览（Slides 48–60）

课件 Slides 48–60 为 Course Logistics 部分，其行政信息归纳为以下书面要点。

基本安排：

- 讲授时间为每周二、周四 15:00–16:20，地点 Thornton 110（Slide 54）。
- Lecture 不提供录像；出勤为硬性要求。自第 2 周起，每讲开始时进行 1–2 题的 participation quiz；每名学生享有 2 次 free absences（免费缺勤额度）。
- 出勤以扫描课件上的 QR code 记录；该 QR code 仅在每讲最初 10 分钟内展示，错过即无法签到。
- 因病应留家休养并及时联系教师团队，课程不要求带病到课；遇紧急或特殊情况亦应主动沟通以获得协助（Slide 55）。
- Office Hours 时间待定（TBD），为线下形式，预计第 2 周（首次作业之前）确定并公布于 Ed；未选课的学生自第 2 周起亦可参加（Slide 56）。
- 课程信息以课程网站（cs106l.stanford.edu）与 Ed 论坛为准；网站另提供 Paperless 提交入口、C++ Documentation、Python to C++ Guide 等资源链接（Slide 57）。
- 选课背景：已修或在修 CS106B/X 或同等课程，即已掌握函数与对象/类等程序设计基础（Slide 57）。

作业与评分：

- 共 8 次 weekly assignments，每次约 1–2 小时，按 handout 指引经 Paperless 提交；认真听讲即可完成（Slide 58）。
- 作业于周五发布、次周五截止；每名学生享有 3 个 free late days（免罚迟交额度）。
- 评分采用 S/NC 制，无考试、无论文；获得 S 的条件为：第 2 至第 9 周的 14 次 lecture 中出勤不少于 12 次，且完成全部 8 次作业（Slide 59）。
- 课程于第 8 周结束，为期末考试周预留时间（Slide 57）。

社区规范与沟通渠道：

- 欢迎随时提问，教师亦会周期性停顿以收集问题、核查理解（Slide 49）。
- 需要无障碍支持（accommodations）的学生可与学校 OAE 协作，并同时告知教师团队，以便改善课程的可及性（Slide 50）。
- 社区规范包括：营造不因提问或出错而受羞辱的环境（shame-free zone）；以善意与尊重对待同学与教师；保持好奇；重视沟通；承认所有人都处于学习进程之中，即保持谦逊、敢于提问、避免完美主义（Slide 51）。
- 教师团队承诺尽力提供支持与灵活性，欢迎学生就课程运行反馈意见；遇个人困难应及时沟通（Slide 52）。
- 联系渠道首选教师团队公共邮箱 cs106l-spr2526-staff@lists.stanford.edu（勿发送至教师个人邮箱，以确保消息同时送达两位教师）；其次为 Ed 上的公开或私密帖子（经 Canvas 加入 Ed）；亦可课后交流或参加 Office Hours（Slide 60）。

## 本讲要点

- C++ 被定位为 "the invisible foundation of everything"：电子游戏（Valorant、CS:GO/CS2、Fortnite 等）、高频交易（Optiver、Citadel、HRT）、自动驾驶（Tesla、Waymo）、嵌入式（Arduino）、GPU 编程（NVIDIA CUDA）、数据库、浏览器、机器学习框架、编译器与操作系统的底层均由 C++ 支撑；其能力特征是海量、高效且优雅地处理数据。
- 语言演进脉络：汇编具备指令简单、速度快与完全控制的优势，但代码量大、难以理解且不可移植；1972 年 Dennis Ritchie 的 C 借助编译器实现 fast、simple、cross-platform；1983 年 Bjarne Stroustrup 在 C 之上引入高层特性创造 C++，并保持对 C 的向后兼容乃至内联汇编能力。
- C++ 设计哲学五条，概括为 Readable、Safety、Efficiency、Abstraction、Programmer Choice，核心立场是 "elegant and efficient" 不可偏废；标准以三年为周期演进，自 C++98 至 C++23，当前节点为 C++26。
- 现代 C++ 风格的 Hello World 已涉及智能指针、模板、流与运算符重载四个核心机制，它们与 move semantics、RAII 等共同构成本课程主体；本课程与 CS106B 的分工在于聚焦代码质量本身，不依赖 Stanford 自制库，只使用 STL。
- 评分采用 S/NC：第 2–9 周出勤不少于 12/14 次（QR code 仅在课前 10 分钟内有效），并完成全部 8 次周作业；另有 2 次 free absences 与 3 个 free late days；无考试与论文，课程于第 8 周结束。
- 联系渠道以团队邮箱 cs106l-spr2526-staff@lists.stanford.edu 与 Ed 论坛（经 Canvas 加入）为主，亦可参加 Office Hours（第 2 周起，时间见 Ed）。
