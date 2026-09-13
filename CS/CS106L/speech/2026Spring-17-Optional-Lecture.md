---
title: "Lecture 17 · The C++ Iceberg 逐字稿"
createAt: 2026/9/13
---

# Lecture 17: The C++ Iceberg（逐字稿）

> 对应课件转写：[2026Spring-17-Optional-Lecture.md](../output/2026Spring-17-Optional-Lecture.md)

## 1. 引论：C++ Iceberg 的分层结构

本讲为课程的选修收尾讲次，不再引入主干知识点，而是以 C++ 社区流传多年的 "iceberg meme"（冰山图）为线索，对语言中若干隐晦、反直觉或带有历史包袱的现象作漫谈式考察。冰山的比喻将 C++ 的知识按"显与隐"分层：水线之上是多数开发者有所耳闻的怪癖，水线之下则是更深、更冷僻的规则细节。

课件给出的水线之上条目包括：`0[arr]`、`#define private public`、"inline does not mean inline"、"most vexing parse"（最令人困扰的解析）、"C++ is not a superset of C"、头文件 `<iosfwd>`、spaceship operator（`<=>` 运算符）、"else if is a lie"、digraphs（替代词法记号）、`-->` "operator"，以及读来一气呵成的 "protected abstract virtual base pure virtual private destructor"。水线之下的条目更为冷僻，例如 "vector\<bool\> is broken"、unsigned 操作数上的一元负号问题、"templates Turing completeness was an accident"（模板的图灵完备性纯属意外）、C++ FQA lite、"the strange details of std::string"、"std::move does not move"、"std::remove does not remove" 等。

介于其间的层次汇集了更多似谑似真的条目："iostream was a mistake"、"rvalue references are lvalues"、"T&& is not an rvalue reference"、"function try blocks"、"shared_ptr is an anti-pattern"、"the for loop is broken"、"constexpr does not mean what you think it means"、"implicit char\* to bool& conversion"、"operator, ()"、"templates are obfuscated haskell"、"C++0x is a hexadecimal name"、"heap and stack don't exist"。课件指出，这些标题多为反讽式概括，但其中相当一部分在细究之下是对语言规则的精确描述——例如具名的右值引用变量在表达式中是 lvalue，模板中的 `T&&` 作为 forwarding reference 并不必然是右值引用。

本讲从中选取数个条目逐一展开：`-->` 的词法错觉、`else if` 的语法本质、iostream 的设计取舍，以及 range-based for 的临时对象生命周期问题。

## 2. `-->`：并不存在的运算符

上述条目中最直观的一例是所谓的 `-->` "operator"。课件给出如下程序：

```cpp
#include <stdio.h>
int main()
{
    int x = 10;
    while (x --> 0) // x goes to 0
    {
        printf("%d ", x);
    }
}
```

程序输出 `9 8 7 6 5 4 3 2 1 0`，看上去像是存在一个使 `x` "递减趋于 0" 的 `-->` 运算符。事实上 C++ 中并无此运算符。依据词法分析的最长匹配（maximal munch）规则，`x --> 0` 被切分为 `x-- > 0`，即先作后置自减、再与 0 比较大小。每次条件判断时，`x--` 取自减之前的值参与比较，循环体随后打印减 1 之后的值，故输出自 9 至 0；当 `x` 为 0 时条件不成立，循环终止。注释 "x goes to 0" 是社区流传的视觉玩笑，这一写法因形似箭头而得名。

## 3. `else if is a lie`：else 分支的语法本质

词法层面的错觉尚属玩笑，"else if is a lie" 则触及真正的语法规则：`else if` 并非语言中的独立语法构造。课件以下例说明 else 分支之后可以跟随任何单条语句：

```cpp
#include <iostream>

int main() {
    int i = 10;

    if (false) {
        std::cout << "hello" << std::endl;
    } else while (i > 0) {
        std::cout << i << std::endl;
        --i;
    }
}
```

按照 C++ 文法，if 语句的 else 分支后必须紧跟一条语句（statement），而这条语句本身可以是块语句、另一条 if 语句、while 语句或表达式语句等。上例中 else 之后是一条 while 语句：由于 if 条件为 false，控制流进入 else 分支并执行该循环，程序依次打印 10 至 1。课件的示意图对这一结构作了概括：else 之后是一条"单行语句"，它可以是 `while..`、`if..` 或一次函数调用 `doSomething()`。常见的 `else if (...) { ... }` 写法，实质是 else 后接一条 if 语句，其"else 分支"又是一条 if 语句，层层嵌套而形成链状外观；理解这一点后，`else if` 链的语义便可完全归约为嵌套 if 语句的语义。

## 4. iostream 的设计动机与后世评价

中层条目 "iostream was a mistake" 引出了对 iostream 历史的回顾。课件转引 Stroustrup《The Design and Evolution of C++》（D&E）第 8.3.1 节的记述：C 的 printf 系列函数是高效的，"但它并不是 type-safe 的，也不是 extensible 的"；为寻找 type-safe、terse、extensible 且 efficient 的替代方案，iostream 在设计过程中吸收了多方建议。Douglas McIlroy 建议其形式仿照 Unix 的流与管道（`>>`、`>`、`|`），设计者亦曾在 `=`、`<`、`>` 等运算符之间权衡；Andrew Koenig 则提出了 manipulator（流操纵符）的思想。manipulator 使流状态的切换得以自然地嵌入输出表达式：

```cpp
int i = 1234;

cout << i << ' '           // decimal by default: 1234
    << hex << i << ' '        // hexadecimal: 4d2
    << oct << i << '\n';      // octal: 2322
```

其中 `hex`、`oct` 即 manipulator：它们改变流的进制状态，使随后的整数分别以十六进制（`4d2`）与八进制（`2322`）输出。

关于 iostream 的批评同样广为流传。课件引用了一位评论者的抱怨：stream 接口的成员函数命名晦涩难解，例如 `getloc/imbue`、`uflow/underflow`、`snextc/sbumpc/sgetc/sgetn`、`pbase/pptr/epptr`。课件给出的结论有三点。其一，iostream 确实存在 shortcomings（短处）。其二，它在各个标准版本中吸收诸多意见而不断得到改进。其三，就历史坐标而言其成就已相当可观：Ada Rationale [Ichbiah, 1979] 曾断言，若无特殊语言特性支持，便不可能实现既简洁又 type-safe 的 I/O；而 iostream 正是在不引入特殊语言特性的前提下，以纯库手段实现了 type-safe 且 extensible 的输入输出。

## 5. `the for loop is broken`：range-based for 与临时对象

中层条目中与本课程内容关系最密切的是 range-based for 语句的临时对象生命周期问题。课件的表述是：range 表达式看上去会在整个循环期间保持存活——这是语言给出的"承诺"（the promise）——但该承诺并不总是兑现。考虑两种写法：

```cpp
for (auto e : getCollection())
```

若 `getCollection()` 按值返回一个临时对象，语言会保证该临时对象存活至整个循环结束：range-based for 在语义上等价于将 range 表达式的结果以引用形式绑定并令其生命周期覆盖循环体，被直接绑定的临时对象因此得以延寿。

```cpp
for (auto e : getCollection().getRef())
```

链式调用则破坏了这一保证。此处 `getCollection()` 创建一个临时集合，`getRef()` 返回指向该临时集合内部的引用；range-based for 所延长的只是作为 range 表达式最终结果被绑定的对象，而中间产生的临时集合本身未被延长——它在循环开始之前、于初始化完整表达式结束时即被销毁，`getRef()` 的结果随之成为指向已失效内存的悬垂引用。

课件同时给出一个 caveat（附带说明）：实践中这类代码常常"看起来能跑"。`getCollection()` 所分配的内存虽然随临时对象析构而失效，但只要这块内存尚未被复用，数据在物理上仍留在原处，循环便照常工作。这正说明此类错误属于未定义行为——它可能恰好不出错，而一旦出错便难以复现与定位。

## 6. 更深处的冰山

课件随后将冰山推至最深处，该页标题为 "The Preprocessor Iceberg"。这一层的条目包括："compilers disprove Fermat's last theorem"、"C++0x concepts were rust traits"、zapcc 编译器、"i have no constructor and i must initialize"、"..... is valid syntax"、"std::optional is a monad"、"the preprocessor iceberg"、"C++ active issues"、"abominable function types"、"godbolt is a real person"，以及本讲将要讨论的 "hello world has a bug" 与 "break ABI to save C++"。这一层条目的共同特征是：它们指向语言的规范文本、编译器实现与社区历史中最隐微的角落，多数已难以在一次课程内展开，下文仅就最后两项作实质讨论。

## 7. `hello world has a bug`

冰山深处的条目宣称"hello world 有一个 bug"。课件以 Linux 下的 `/dev/full` 设备验证这一说法；该设备的写入恒定失败并返回 "No space left on device" 错误。作为对照，shell 内建的 echo 在写入失败时会正确报告错误并以非零状态退出：

```
$ echo "Hello World!" > /dev/full
bash: echo: write error: No space left on device
$ echo $?
1
```

而经典的 hello world 程序在同样条件下却"成功"退出：

```
$ gcc hello.c -o hello
$ ./hello > /dev/full
$ echo $?
0
```

用 strace 跟踪 write 系统调用可以确认错误确实发生了：

```
$ strace -etrace=write ./hello > /dev/full
write(1, "Hello World!\n", 13)          = -1 ENOSPC (No space left on device)
+++ exited with 0 +++
```

write 返回 -1 且错误码为 ENOSPC，程序却以状态 0 退出。原因在于缓冲：printf（及 iostream）的输出先进入缓冲区，程序随即认为写入已经成功；真正的 write 直到退出前的缓冲区冲刷（flush）阶段才执行并失败，而此时已没有任何代码去检查这次写入的结果。课件将此概括为：写入先被放入缓冲区并被视作成功，错误在其后才暴露，而程序将其完全忽略。这一缺陷说明，缓冲在带来效率的同时，也把 I/O 错误的暴露时机推迟到了程序逻辑之后。

## 8. `break ABI to save C++`

hello world 的缺陷是局部的；ABI 之争则是牵动整个标准库演进的现实约束，也是冰山最深处与工程实践关系最为密切的话题。

ABI（Application Binary Interface，应用二进制接口）是代码在二进制层面的低层契约，其内容包括 calling conventions（调用约定）、data representation（数据表示）、system calls、name mangling（名字修饰）与 exceptions 等。课件以 RISC-V 的算术指令表作为二进制层面约定的示意：`ADD rd, rs1, rs2`、`SUB`、`ADDI`、`SLT`、`SLTU`、`LUI` 等指令的编码与语义，是编译产物与机器之间必须逐字遵守的契约。已编译的旧代码与标准库二进制之间的关系与此同理：双方之间存在不容随意更改的约定。课件并以 cor3ntin 2020 年 2 月 24 日的文章《The Day The Standard Library Died》（https://cor3ntin.github.io/posts/abi/）作为这一讨论的参考来源。

文章的论点是：许多对现行标准库的改进会破坏 ABI，因而无法实现。课件列举了两组例子。其一是性能改进受阻：让 associative container（如 `std::map`、`std::set`）显著变快、让 `std::regex` 变快，均因破坏 ABI 而搁浅——原文的讽刺是，"以当前实现，启动 PHP 去执行一条正则表达式，都比使用 std::regex 更快"；课件配图以 C++ 启动 PHP 进程、由 PHP 完成对 `/Reg[ex]?/` 的匹配再返回 C++ 的往返过程，将这一说法具象化。其二是新能力的缺席：若辅以必要的语言修改，`unique_ptr` 本可以放进一个寄存器，从而真正实现相对于裸指针的 zero-overhead；为 regex 增加 UTF-8 支持是一次 ABI break；许多人相信 exceptions 的开销作为实现质量问题（quality of implementation）本可大幅降低，但这可能同样需要破坏 ABI。

这段讨论揭示了冰山比喻的现实一面：语言的演进不仅受设计与标准文本的约束，也受制于既有二进制生态。所谓 "break ABI to save C++"，即指社区中"宁可付出破坏 ABI 的代价，也要换取标准库现代化"的主张及其争议。

## 本讲要点

- C++ iceberg meme 将语言知识按"显与隐"分层：水线之上是广为人知的怪癖（`0[arr]`、most vexing parse、digraphs 等），水线之下是更冷僻的规则细节与历史包袱；不少看似戏谑的条目实则是对语言规则的精确概括。
- `-->` 不是运算符：受词法最长匹配规则支配，`x --> 0` 即 `x-- > 0`，"箭头"只是书写上的错觉。
- `else if` 并非独立语法：else 分支后必须是单条语句，if、while 皆可充当；`else if` 链只是嵌套 if 语句的书写形式。
- iostream 源于对 printf 缺乏 type safety 与可扩展性的回应：借助 McIlroy 的流模型与 Koenig 的 manipulator 思想，它以纯库方式实现了 type-safe 且 extensible 的 I/O；接口确有晦涩之处，但历经多版本持续改进。
- range-based for 只延长直接绑定 range 的临时对象；`getCollection().getRef()` 一类的链式写法中，中间临时对象在循环开始前即被销毁，由此产生的悬垂引用构成未定义行为，且常因内存未被复用而"看似正常"。
- 缓冲式 I/O 会推迟错误的暴露：hello world 写入 `/dev/full` 时 write 返回 ENOSPC，程序却以 0 退出；同时，ABI 兼容的包袱使标准库的多项改进与新能力（更快的关联容器与 `std::regex`、寄存器级 `unique_ptr`、regex 的 UTF-8 支持、更低开销的 exceptions）长期未能落地。
