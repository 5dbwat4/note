---
title: "Lecture 04 · Streams 逐字稿"
createAt: 2026/9/13
---

# Lecture 04: Streams（逐字稿）

> 对应课件转写：[2026Spring-04-Streams.md](../output/2026Spring-04-Streams.md)

## 1. 概览与上讲回顾

本讲讨论 C++ 的流（streams），是全学期篇幅最长的一讲。课件首页引用了 cplusplus.com 的一张类继承图，可以视为全课的地图：位于顶端的是 `ios_base`，其下是 `ios`；由 `ios` 分出 `std::istream` 与 `std::ostream` 两大分支，二者共同派生出 `std::iostream`；两条分支继续特化，得到文件流 `std::ifstream`、`std::ofstream`、`std::fstream`，以及字符串流 `std::istringstream`、`std::ostringstream`、`std::stringstream`；图中的黑色方块标注了标准流对象 `std::cin` 与 `std::cout`、`std::cerr`、`std::clog`。本讲结束时，这张图中的每一个类都应能得到解释。

全课内容依次为：简要回顾、流的概念、`std::stringstream`、`std::cout` 与 `std::cin`、输出流、输入流。

上一讲的主题是初始化与引用，此处回顾两个要点。其一，统一初始化（uniform initialization）：以花括号 `{}` 进行初始化，是一种无处不在（ubiquitous）且安全（safe）的初始化方式。其二，引用（references）：引用为变量提供别名（aliases），使多个变量名指称同一块内存。

## 2. 流：C++ 的通用输入输出抽象

Bjarne Stroustrup 曾指出："Designing and implementing a general input/output facility for a programming language is notoriously difficult"——为一门编程语言设计并实现通用的输入输出设施，是公认的难题。C++ 对这一难题给出的回答即流（stream）：一种面向 C++ 的通用输入输出设施。更精确的表述是，流是 C++ 的一套通用输入输出抽象（abstraction）。

抽象的含义是隐藏不必要的细节，只暴露真正相关的部分。课件的类比是驾驶汽车：驾驶员无需了解发动机内部的燃烧机理，只需掌握方向盘与踏板构成的接口。抽象提供一致的接口（consistent interface）；就流而言，这一接口即读取（reading）与写入（writing）数据。本讲的核心论断可概括为一句话：流帮助我们读写数据（Streams help us read and write data）。多数程序员每天都在使用流，只是未曾察觉。

## 3. 传送带模型与常见流对象

最熟悉的流出现在每个程序的第一行里：

```cpp
std::cout << "Hello, World" << std::endl;
```

`std::cout` 本身就是一个流。理解流的直观模型是传送带（conveyor belt）：数据如同传送带上标注 "data" 的箱子，自一端被输送至另一端。据此可将流分为两类。输出流（output streams）把数据送出程序、送往终端等目的地，家族成员包括 `std::cout`、`std::cerr`、`std::clog`、`std::ofstream`、`std::ostringstream`；输入流（input streams）把数据送入程序，来源可以是键盘等外部设备，家族成员包括 `std::cin`、`std::ifstream`、`std::istringstream`。命名规律清晰：前缀 `o` 对应 output，前缀 `i` 对应 input。

使用过 CS106B 课程代码的读者对下列片段应不陌生：

```cpp
ifstream in;
openFile(in, my_file);

Vector<std::string> lines = readLines(in);
```

此例使用的是 Stanford 库而非标准库（`Vector` 并非 `std::vector`），但 `ifstream` 本身就是流：读取文件的代码一直在使用流。

四组最基本的用法如下。向控制台输出：

```cpp
std::cout << "hello CS106L!";
```

从标准输入读取：

```cpp
// Allows user to write something into
// student_input
std::string student_input;
std::cin >> student_input;
```

向文件写入：

```cpp
//create a file called "data.txt"
std::ofstream fout("data.txt");
fout << "I'm writing to this file";
```

从文件读取：

```cpp
std::ifstream fin("data.txt");
std::string first_word;
//store the first word from the file into
//student_input
fin >> first_word;
```

四例的目的地与来源各不相同——屏幕、键盘、文件——使用的却是同一对操作符 `<<` 与 `>>`。这正是抽象的作用：以一致的接口（consistent interface）处理输入（input）与输出（output）。

## 4. 流的继承体系：从 ios_base 到具体流类

种类繁多的流类，需要自继承链的底端理解。`ios_base` 是所有与流相关内容的基础（foundation），维护两类数据。第一类是状态信息（state information）：一组描述流"健康状况"的标志位（flags），例如 `failbit` 表示发生逻辑错误（如类型错误），`eofbit` 表示已到达流末尾（end of stream）。第二类是控制信息（control information）：决定流如何呈现数据，例如数值 255 应打印为十进制 "255"、十六进制 "FF"，还是八进制 "377"，即由控制信息记录。课件以瀑布作比：水自 "input" 端落下，沿途携带 a、b、c 等数据块，汇入 "output" 端——流正是承载数据的通道。

在 `ios_base` 之上，`basic_ios`（即继承图中的 `ios`）进一步保证流正常工作，并记录流的来源：控制台、键盘，或是一个文件。

再向上是两个核心类：`std::ostream` 与 `std::istream`。命名本身就是提示：`ostream` 中的 o 指 output，用于输出；`istream` 中的 i 指 input，用于输入。二者是 `basic_ios` 之下并列的两个分支。`ostream` 一支派生 `std::ofstream`（写文件）、`std::ostringstream`（写字符串）与 `std::cout`（写控制台）；`istream` 一支派生 `std::ifstream`（读文件）、`std::istringstream`（读字符串）与 `std::cin`（读键盘）。

标准库的完整继承图使用带模板参数的名称：`basic_ios<CharT, Traits>`、`basic_ostream<CharT, Traits>`、`basic_istream<CharT, Traits>`、`basic_iostream<CharT, Traits>`，以及字符串流与文件流的各具体类。其中 `basic_iostream` 同时继承 `basic_ostream` 与 `basic_istream`；日常书写的 `ostream` 等名称，即对应模板以 `char` 实例化之后的版本。模板细节留待后续课程，此处关注结构即可。

## 5. 数据如何进入程序：std::cin 与类型转换

一个基本问题是：数据如何从外部来源（键盘或文件）进入 C++ 程序？

以从控制台读取一个 `double` 为例。`std::cin` 是控制台输入流，它是 `std::istream` 的一个实例（instance），代表标准输入：

```cpp
void verifyPi()
{
    double pi;
    std::cin >> pi;
    /// verify the value of pi!
    std::cout << pi / 2 << '\n';
}
```

若用户在控制台输入 "1.57"，`std::cin >> pi` 会将其存入 `double` 变量 `pi`。此处有一个值得追问的现象：控制台交给程序的本是字符串 "1.57"，最终存入的却是 `double` 类型的值——把字符串"存进" double，这合法吗？

答案在于类型转换（type conversion）。整个数据通路可抽象为三个环节：外部来源（external source）向流提供数据的字符串表示（string representation），如 "3.14"；流负责搬运；数据进入程序前发生类型转换，程序得到的是 `double` 类型的 3.14。将目标类型一般化为任意 `fill_in_type`，模式不变：外部提供字符串，流完成搬运与转换，程序获得目标类型的值。

由此可见流的价值：流为处理外部数据提供了通用（universal）的途径。

据此可对流作正式分类。输入流（input streams）自来源读数据，继承自 `std::istream`，例如从控制台读取的 `std::cin`，主要操作符为 `>>`，称提取操作符（extraction operator）。输出流（output streams）向目的地写数据，继承自 `std::ostream`，例如向控制台写入的 `std::cout`，主要操作符为 `<<`，称插入操作符（insertion operator）。

既可读又可写的流同样存在：`ostream` 与 `istream` 在继承图上的交集称为 `iostream`，它同时具备二者的全部特性。

头文件方面，常用的包含关系如下：

```cpp
#include <iostream> // cin & cout
#include <istream>  // cin
#include <ostream>  // cout
```

需要 `std::cin` 时可包含 `<iostream>` 或 `<istream>`；需要 `std::cout` 时可包含 `<iostream>` 或 `<ostream>`；`<iostream>` 二者兼备，是最常见的选择。

## 6. std::stringstream：把字符串当作流

`std::stringstream` 的定义：一种把字符串当作流来使用的方式（a way to treat strings as streams）。其用途集中于需要混合处理不同数据类型（mixing data types）的场景。在继承体系中，它派生自 `basic_iostream`，兼具读写能力。

以下示例将逐步展开。先准备一句 Bjarne 名言的节选：

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";
}
```

第一步，以该字符串构造一个 stringstream：

```cpp
/// create a stringstream
std::stringstream ss(initial_quote);
```

由于 stringstream 本身就是流，还存在等价写法：先默认构造一个空流，再以插入操作符将字符串写入：

```cpp
/// create a stringstream
std::stringstream ss;
ss << initial_quote;
```

这与向 `std::cout` 写数据是同一类操作。

第二步，准备接收数据的目的地（data destinations）：

```cpp
/// data destinations
std::string first;
std::string last;
std::string language, extracted_quote;
```

第三步，以提取操作符将数据自流中取出：

```cpp
ss >> first >> last >> language >> extracted_quote;
```

完整的程序如下：

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";
    /// create a stringstream
    std::stringstream ss(initial_quote);
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
    ss >> first >> last >> language >> extracted_quote;
    std::cout << first << " " << last << " said this: " << language << " " << extracted_quote << std::endl;
}
```

在流内部，整个字符串排成一个字符序列：序列起点标注 Start，末尾的 `'\n'` 即 End of stream；读取位置随每一次提取向后移动。若只执行 `ss >> first >> last >> language;`，则 `extracted_quote` 保持为空字符串，输出时表现为一段空白。末行 `std::cout` 使用的 `<<` 正是插入操作符。此处值得记取课件的一句话：流的作用是把数据从一个地方移动到另一个地方（Streams move data from one place to another）。

## 7. `>>` 的空白截断规则与 getline

`>>` 的断词规则是：读到任意空白字符（whitespace）为止。空白字符共六种：

1. `' '`（空格）
2. `'\n'`（换行）
3. `'\t'`（水平制表）
4. `'\r'`（回车）
5. `'\f'`（换页）
6. `'\v'`（垂直制表）

以该规则考察 `ss >> first >> last >> language;` 的执行过程：第一个 `>>` 自流首读起，遇空格即停，将 "Bjarne" 存入 `first`，读取位置越过该空格；随后 "Stroustrup" 存入 `last`，"C" 存入 `language`。至此一切符合预期。

**例题**　若希望将余下的 "makes it easy to shoot yourself in the foot" 整句存入 `extracted_quote`，按最初的写法执行第四个 `>>`：

```cpp
ss >> first >> last >> language >> extracted_quote;
```

`extracted_quote` 的值是什么？

**解析**　`>>` 只读到下一个空白字符为止，故 `extracted_quote` 仅得到 "makes"，其后内容仍滞留流中，与预期不符。

解决方法是 `getline`：

```cpp
istream& getline(istream& is, string& str, char delim)
```

其要点有三。第一，`getline()` 自输入流 `is` 读取字符，直至遇到分隔符 `delim`，并将读到的内容存入 `str`。第二，`delim` 默认为 `'\n'`，省略第三个参数即为"读入一整行"。第三，`getline()` 会将 `delim` 字符本身从流中消耗（consume）掉——课件对此特别强调，本讲末尾的经典错误正源于此。

修正后的完整程序：

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";
    /// create a stringstream
    std::stringstream ss(initial_quote);
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
    ss >> first >> last >> language;
    std::getline(ss, extracted_quote);
    std::cout << first << " " << last << " said this: '" << language << " " << extracted_quote + "'" << std::endl;
}
```

程序先以 `>>` 取走 Bjarne、Stroustrup、C 三个词，读取位置停在 "makes" 之前；`std::getline(ss, extracted_quote)` 随即将余下的整行读入。输出为：Bjarne Stroustrup said this: 'C makes it easy to shoot yourself in the foot'。

## 8. 输出流、缓冲区与 flush

输出流（output stream）是把数据写入目的地（外部来源）的途径，例如向控制台写入的 `std::cout`，以 `<<` 插入操作符将数据发送（send）至输出流。

实现层面有一个重要细节：输出流中的字符并非立即到达目的地，而是先存入中间缓冲区（intermediary buffer），随后再被冲刷（flush）至目的地。以下例说明：

```cpp
double tao = 6.28;
std::cout << tao;
```

`std::cout << tao` 做的事，是把 '6'、'.'、'2'、'8' 四个字符放入缓冲区。在显式 flush 发生之前，缓冲区中的内容不会出现在外部来源上——执行完上述两行，屏幕上未必已经出现 6.28。

flush 发生的时机有五种：

- 显式执行 `std::cout << std::flush`；
- 显式执行 `std::cout << std::endl`；
- 程序到达结尾（end of program）时；
- 缓冲区写满时；
- 关联流（tied streams）交互时——例如经 `std::cin` 读取输入之前，`std::cout` 必须先行 flush，这保证了输出提示先于用户输入出现。

两种显式 flush 的写法如下。使用 `std::flush`：

```cpp
double tao = 6.28;
std::cout << tao;
std::cout << std::flush;
```

`std::flush` 执行后，"6.28" 即出现在控制台。`std::endl` 同样触发 flush，并额外写入一个换行：

```cpp
double tao = 6.28;
std::cout << tao;
/// Also flushes!
std::cout << std::endl;
```

**例题**　下列程序的输出是什么？

```cpp
int main()
{
    for (int i=1; i <= 5; ++i) {
        std::cout << i << std::endl;
    }
    return 0;
}
```

**解析**　`std::endl` 指示 cout 流结束当前行，故输出为各占一行的 1、2、3、4、5。若去掉 `std::endl`：

```cpp
int main()
{
    for (int i=1; i <= 5; ++i) {
        std::cout << i;
    }
    return 0;
}
```

输出为连续的 "12345"：程序中没有任何换行动作，五个数字依次相连。

另需说明 `cout` 家族的另外两个对象：`std::cerr` 用于输出错误信息，不经过缓冲（unbuffered），错误信息立即（immediately）送出；`std::clog` 用于记录非关键事件的日志，经过缓冲（buffered）。

## 9. '\n' 与 std::endl 的辨析

前述"仅 flush 与 endl 刷新缓冲区"的结论需要一处重要补充。课件作者实测后发现，`'\n'` 的表现似乎与 `std::endl` 类似，同样会刷新缓冲区。cppreference 的 `std::endl` 词条给出了部分解释："In many implementations, standard output is line-buffered, and writing '\n' causes a flush anyway, unless `std::ios::sync_with_stdio(false)` was executed."——在许多实现中，标准输出为行缓冲（line-buffered），写入 `'\n'` 无论何时都会引发 flush，除非执行过 `std::ios::sync_with_stdio(false)`。进一步的实验是给程序接上 `| cat`，使输出经管道而非终端：此时 `'\n'` 不再立即刷新缓冲区，与行缓冲的解释吻合。

依 cppreference 的提示，可以写出如下代码：

```cpp
int main()
{
  std::ios::sync_with_stdio(false);
  for (int i=1; i <= 5; ++i) {
    std::cout << i << '\n';
  }
  return 0;
}
```

课件注明：这种做法可能带来显著的性能提升（massive performance boost），因为它解除了 C++ 流与 C 标准 stdio 之间的同步。

但此处另有保留：该方案仅在输出流为非交互式（non-interactive）时有效。在各种输出流上测试的结果表明，对文件、Unix 管道等非交互输出，执行 `sync_with_stdio(false)` 之后 `'\n'` 确实不再触发 flush；而当输出为交互式（interactive）——例如直接输出至终端——流仍按行缓冲处理，`'\n'` 一到即触发 flush。课件对此的评注是：有时必须亲自动手排查，方能确定哪些做法有效、哪些无效，这也是与这门语言打交道的一部分。

综合以上，日常换行的推荐写法是 `'\n'`：

```cpp
std::cout << "Draaaakkkkeeeeeeeeee" << '\n';
```

而非：

```cpp
std::cout << "Draaaakkkkeeeeeeeeee" << std::endl;
```

理由在于 `'\n'` 不强制 flush，开销更小。

## 10. 文件流：std::ofstream、std::ifstream 与 std::fstream

输出文件流（output file streams）的类型是 `std::ofstream`，用于向文件写数据，以 `<<` 插入操作符将数据发送至文件。其常用方法包括 `is_open()`、`open()`、`close()`、`fail()`，细节可查阅 cplusplus.com。

构造流时可传入文件标志（file flag）：

```cpp
std::ofstream out("file.txt", file_flag);
```

可选值有三个：`std::ios::trunc`（默认值，截断文件后重写）、`std::ios::app`（追加至文件末尾）、`std::ios::ate`（打开后立即将光标移至文件末尾）。

以下示例逐段分析：

```cpp
int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
  if (ofs.is_open()) {
    ofs << "Hello CS106L!" << '\n';
  }
  ofs.close();
  ofs << "this will not get written";

  ofs.open("hello.txt");
  ofs << "this will though! It's open again";
  return 0;
}
```

第一行在构造时即关联文件，创建指向 hello.txt 的输出文件流；`ofs.is_open()` 检查文件确实打开后，方才写入 "Hello CS106L!" 与换行；随后 `ofs.close()` 关闭流。关键在下一行：关闭之后再执行 `ofs << "this will not get written";` 会静默失败（silently fail）——没有异常、没有报错，内容并未写入。调试文件输出问题时应当首先想到这种可能。调用 `ofs.open("hello.txt")` 重新打开流之后，写入即恢复成功，"this will though! It's open again" 被正常写入。若以 `ofs.open("hello.txt", std::ios::app);` 重开，则该标志明确指定追加而非截断，新内容接在文件原有内容之后。

输入文件流（input file streams）的类型是 `std::ifstream`，自文件读数据：

```cpp
int inputFileStreamExample() {
    std::ifstream ifs("input.txt");
    if (ifs.is_open()) {
        std::string line;
        std::getline(ifs, line);
        std::cout << "Read from the file: " << line << '\n';
    }
    if (ifs.is_open()) {
        std::string lineTwo;
        std::getline(ifs, lineTwo);
        std::cout << "Read from the file: " << lineTwo << '\n';
    }
    return 0;
}
```

程序构造 `std::ifstream` 打开 input.txt，先以 `std::getline` 读入第一行至 `line`，再读入第二行至 `lineTwo`。两点值得注意：其一，`getline` 的第一个参数类型为 `istream&`，而 `ifstream` 属于 istream 的一种，故可直接传入；其二，两次 getline 依次读取，因为流的读取位置持续前移。课件在此给出一个一般性结论：针对同一种来源/目的地类型，输入流与输出流互补（complementary）——`std::ofstream` 写文件、`std::ifstream` 读文件，二者配套。

需要同时读写时，对应的类是 `std::fstream`：继承图中的 `basic_fstream` 派生自 `basic_iostream`，兼具读写能力，即文件版的 iostream。

## 11. 输入流与 std::cin 的缓冲

输入流（input streams）的类型是 `std::istream`，自目的地/外部来源读取数据，以 `>>` 提取操作符（extractor）读取；`std::cin` 即控制台输入流。除 `getline` 外，`std::istream` 还提供 `get()`、`getline()`、`peek()`、`seekg()` 等函数。

关于 `std::cin` 有三个要点：它是带缓冲的（buffered）；可将其视为用户先存入数据、程序再从中读取的场所；其读取在空白字符处停止。C++ 的空白字符包括字面空格 `" "`、`'\n'` 字符、`'\t'` 字符等。

以下述程序为例，逐步分析 `std::cin` 的缓冲行为：

```cpp
int main()
{
  double pi;
  std::cin; /// what does this do?
  std::cin >> pi;
  std::cout << "pi is: " << pi << '\n';
  return 0;
}
```

初始时 cin 缓冲区为空。单独出现的表达式语句 `std::cin;` 的效果是：缓冲区为空，故程序提示用户输入。设用户键入 "3.14" 并回车，缓冲区中即为 '3'、'.'、'1'、'4'、`'\n'` 五个字符。随后 `std::cin >> pi;` 执行：缓冲区非空，程序不再询问用户，直接自缓冲区读取，至空白处停止——读走 "3.14"，经类型转换存入 `double pi`；缓冲区中剩下一个无人处理的 `'\n'`。最后程序输出 "pi is: 3.14"。终端上先后呈现用户键入的 "3.14" 与程序输出的 "pi is: 3.14"。

课件另给出等价写法：省略单独的 `std::cin;`，直接书写 `std::cin >> pi;`。缓冲区为空时，`>>` 自行停下等待用户输入，效果完全相同。

## 12. std::cin 与 getline 混用的错误机理及修复

**例题**　分析下列程序在用户先输入 "3.14"（回车）、再输入 "Rachel Fernandez"（回车）后的输出：

```cpp
int main()
{
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::cin >> name;
  std::cin >> tao;
  std::cout << "my name is: " << name <<
    " tao is: " << tao << " pi is: " << pi << '\n';
  return 0;
}
```

**解析**　逐步执行。`std::cin >> pi;` 时缓冲区为空，程序提示输入；读入 3.14 存入 `pi`，缓冲区剩 `'\n'`。`std::cin >> name;` 时，缓冲区仅剩的 `'\n'` 属于空白，`>>` 跳过空白后已无完整数据，故 cin 提示用户输入；用户键入 "Rachel Fernandez" 后，`>>` 读至下一个空白即停，`name` 得到 "Rachel"，"Fernandez" 与其后的 `'\n'` 仍留在缓冲区。`std::cin >> tao;` 时缓冲区非空，程序不再提示，直接继续读取至下一空白，得到 "Fernandez"；但 `tao` 是 `double`，类型不匹配，提取失败，`tao` 的值为 0。程序输出 "my name is: Rachel tao is: 0 pi is: 3.14"。症结在于 cin 按空白切词，它无从得知"完整的姓名"这一意图。

**例题**　姓名可能含空格，改用 `getline` 读取能否修复？

```cpp
void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : "
            << tao << " pi is : " << pi << '\n';
}
```

**解析**　结果反而更差。`std::cin >> pi` 读走 3.14 之后，`'\n'` 仍留在缓冲区；随后 `std::getline(std::cin, name)` 立即遇到该遗留的 `'\n'`——如前所述，getline 会消耗分隔符——于是"读到一个空行"，`name` 为空字符串 `""`。接着 `std::cin >> tao;`：缓冲区中尚有 "Rachel Fernandez"，非空，故不提示用户，直接尝试把 "Rachel" 读入 `double tao`；类型不匹配，提取失败，`tao` 的值为 0（课件以垃圾桶图标标注这一无效结果）。两个变量全部出错，原因同前：缓冲区不空，cin 根本没有机会询问用户。

**例题**　正确的修复方式是什么？

```cpp
void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : "
            << tao << " pi is : " << pi << '\n';
}
```

**解析**　关键在于连续两次 getline。第一次 getline 充当"清理者"，专门消耗 `>>` 遗留在缓冲区中的 `'\n'`，此时 `name` 为空；第二次 getline 自 "Rachel" 起读取整行，`name` 得到 "Rachel Fernandez"，并消耗行尾的 `'\n'`。随后 `std::cin >> tao;` 执行时缓冲区已空——课件标注为 "The stream is empty! So it is going to prompt a user for input"——程序停下等待用户输入；用户键入 6.2，`tao` 得到 6.2。最终输出 "my name is : Rachel Fernandez tao is : 6.2 pi is : 3.14"，全部正确。

这一模式的结论值得铭记：`>>` 之后若要接 getline，必须先行处理缓冲区中遗留的换行符。

## 本讲要点

- 流是程序中读写数据的通用接口：同一对操作符 `<<` 与 `>>` 贯穿控制台（`std::cin`/`std::cout`）、字符串（`std::stringstream`）与文件（`std::ifstream`/`std::ofstream`）。
- 针对同一种来源/目的地类型，输入流与输出流互补（complementary）：文件有 `std::ofstream`/`std::ifstream`，字符串有 `std::ostringstream`/`std::istringstream`，双向则有 `std::iostream`/`std::fstream`。
- `>>` 读至空白即停；`getline` 读至分隔符（默认 `'\n'`）并将其消耗——本讲全部提取行为与错误均可由这两条规则解释。
- 避免混用 `getline()` 与 `std::cin`，除非确有必要；若必须混用，须处理 `>>` 遗留在缓冲区中的 `'\n'`（例如补写一次 getline）。
- 输出流经中间缓冲区写往目的地，flush 时机为：显式 `std::flush`、`std::endl`、程序结束、缓冲区写满、关联流交互；日常换行宜用 `'\n'` 而非 `std::endl`。
