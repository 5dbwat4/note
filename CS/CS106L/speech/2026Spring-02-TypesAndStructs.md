---
title: "Lecture 02 · Types & Structs 逐字稿"
createAt: 2026/9/13
---

# Lecture 02: Types & Structs（逐字稿）

> 对应课件转写：[2026Spring-02-TypesAndStructs.md](../output/2026Spring-02-TypesAndStructs.md)

## 1. 导言与本讲大纲（Slides 1–7）

Slide 1 的标题页附有一幅 "Data Type in C++" 分类图，将 C++ 的数据类型归为三类。第一类是 Basic Data Types（基本数据类型），即语言直接内置的类型，包括 int、float、double、char、bool、void；第二类是 Derived Data Types（派生数据类型），由基本类型构造而来，包括 array、pointer、reference、function；第三类是 User Defined Data Types（用户自定义数据类型），由开发者自行定义，包括 class、structure、union、typedef、using。本讲的核心内容 struct 与后段引入的 using 均属第三类，这幅分类图可以作为贯穿全课的地图。标题页的另一幅图给出一段示例代码：以 struct 关键字定义含 brand、model、year 三个成员的 struct，声明 myCar1 与 myCar2 两个变量，并为 myCar1 的各成员赋值（"BMW"、"X5"、1999）；其语法细节本讲随后展开，读毕全篇即可完整理解这段代码。

Slides 2 与 3 属于课程事务：上一讲（Lecture 1）介绍了课程概况、学习 CS106L 的意义、C++ 语言的演化历程与课程安排；本课课件均发布于 cs106l.stanford.edu。Slide 5 列出本讲大纲：compile time 与 run time 的区分、静态类型语言（statically typed languages）、struct、the STD（C++ 标准库）、一次代码演示，以及利用 auto 与 using 改进代码。Slide 6 同时提示本课内容量较大，学习中应及时澄清疑问。

## 2. 编译型语言与解释型语言（Slides 8–17）

课件以同一个程序在两类语言中的执行流程对比引入。解释型语言（interpreted language）以 Python 为例。Slides 9–13 是同一幅流程图的逐帧展开，四个环节依次为：源代码（Source Code）、解释器（Interpreter）、机器码（Machine Code）与输出（Output）。源代码为：

```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

动画的每一帧对应一行代码的处理：解释器读入一行，将其翻译为机器码，随即执行。因此机器码逐行增多，输出也逐行出现——先打出 "Hello World"，再打出 "Welcome to"，随后 for 循环逐轮翻译执行，字符 C、S、1、0、6、L 逐一打印，每个字符各占一行。这一组页面的要点（THE BIG IDEA）是：解释型语言逐行读入代码（line-by-line），逐行翻译（translate），随即执行（execute）；翻译与执行交织进行，不存在先于执行的独立翻译阶段。

编译型语言（compiled language）以功能等价的 C++ 代码为例，Slides 14–17 同样以逐帧动画呈现完整流程：

```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

流程分三个环节。首先，编译器（Compiler）将整个程序翻译为机器码；值得注意的是，此时尚未产生任何输出——翻译阶段只生成代码，不执行代码。其次，机器码被打包为一个可执行文件（executable file，图中文件名为 main），它可以被独立保存、反复运行；至此编译阶段结束。最后，运行该可执行文件，方才产生与 Python 版本完全一致的输出。这组页面的要点是：编译器将整个程序（entire program）一次性翻译完毕，打包成 executable file，然后再执行它。

## 3. Compile Time 与 Run Time（Slides 18–22）

基于上述两条流水线可以严格定义两个阶段。Slide 18 将编译型语言的流程分为两段：自 Source Code 经 Compiler 到 Machine Code 的阶段称为 compile time（编译期），即程序被翻译的时期；自可执行文件开始运行到产生 Output 的阶段称为 run time（运行期），即程序被执行的时期。对 C++ 而言，这两个阶段先后相继、彼此分离：必须先完成全部翻译，才开始执行。

Slides 19–20 转向解释型语言：Source Code → Interpreter → Machine Code → Output 的整条链路被整体归入 run time。原因在于解释器的翻译并非独立阶段，而是边读边译、边译边执行，翻译与执行同时发生在运行期间。两页的共同结论是：解释型语言的一切都发生在 run time；编译型语言则先经历 compile time，再经历 run time。这一区分看似简单，却直接决定了下一节的核心问题：错误在哪个阶段被发现。Slide 22 据此给出本讲的一个基本论断：C++ is a compiled language。

## 4. 例题与解析：类型错误发生在哪个阶段（Slides 23–32）

Slide 23 提出本节的核心问题：已经了解 C++ 执行代码的流程，那么错误是在何时被处理的——compile time 还是 run time？课件设计了严格的对照实验（Slide 24）：将同一个逻辑错误——试图将两个字符串相乘——分别写入 Python 与 C++，观察两门语言各自在何时发现它。

Python 版本：

```python
print("Running...")
hello = "Hello ";
world = "World!";
print(hello * world)
```

实际运行结果如下（Slides 25–29 的逐帧动画演示了整个过程）：

```
$ python3 program.py
Running...
TypeError: can't multiply sequence by
non-int of type 'str'
```

分析其逐行行为：解释器逐行翻译并执行。第一条 print 语句合法，成功执行，"Running..." 已被打印；随后两条赋值语句同样合法；执行到 `print(hello * world)` 时，解释器发现字符串与字符串相乘没有定义——字符串的乘法只允许乘以整数——于是在运行途中抛出 TypeError: can't multiply sequence by non-int of type 'str'，程序中止。错误发生于 run time，属于 run time error。判断依据即现象本身：错误信息出现之前，"Running..." 已经输出，说明程序确实运行到中途才失败。（一个附带细节：Python 赋值语句行末的分号并非必需，解释器并不在意。）

C++ 版本：

```cpp
int main() {
    std::cout << "Running..." << std::endl;
    std::string hello = "Hello ";
    std::string world = "World!";
    std::cout << hello * world << std::endl;
    return 0;
}
```

编译命令 `g++ main.cpp` 并未产出可执行文件，而是给出如下错误：

```
error: no match for 'operator*' (operand types are
'std::string' and 'std::string')
```

此错误发生于 compile time。报错信息 no match for 'operator*' 的含义是：对于操作数类型 std::string 与 std::string，不存在可用的乘法运算。编译器在翻译阶段即发现这一非法操作并拒绝继续，可执行文件根本不会生成，程序一行都未运行，"Running..." 自然无从打印。这就是 compile time error。

Slide 32 将两侧并置总结：同一性质的错误，Python 要推迟到 run time 才暴露，且此前已经执行的部分照常产生了输出；C++ 在 compile time 即被拦截，含错的代码完全无法进入运行阶段。

## 5. 类型与静态类型（Slides 34–43）

上述差异的根源在于类型系统。type 指变量所属的"类别"；C++ 自带一批内置类型（Slide 35）：int 表示整数（如 106）；double 表示双精度浮点数（如 71.4）；string 表示字符串（如 "Welcome to CS106L!"）；bool 取 true 或 false 两个值；size_t 表示非负整数类型（如 12）。

Slide 36 将前文的观察形式化：既然编译器在生成机器码之前就检查类型，这就意味着 C++ 是一门 statically typed language（静态类型语言）——类型检查发生在编译期。

作为对照，Python 采用 dynamic typing（动态类型）。Slides 37–38 给出示例：

```python
a = 3
b = "test"

def foo(c):
    d = 106
    d = "hello world!"
```

变量 d 先被赋为整数 106，随后又被赋为字符串 "hello world!"，Python 完全允许这种中途改换。其机制在两页底部写明：解释器在 run time 依据变量当时的取值来确定其类型；变量名本身不绑定固定类型，值是什么，它在当下就是什么。

Slide 39 将两种类型体系并排对比。左侧 dynamic typing 一侧，改换类型的 Python 代码可以正常通过；右侧是语义等价的 C++ 代码：

```cpp
int a = 3;
string b = "test";

void foo(string c)
{
    int d = 106;
    d = "hello world!"; // error
}
```

d 已声明为 int，向其赋字符串值直接违反类型声明，无法通过编译（slide 以红叉标注该行）。static typing 的两条核心规则由此而来：其一，每个变量都必须声明类型；其二，类型一经声明不可改变。

Slide 40 列出选择 static typing 的三点理由：更高效（more efficient），编译器提前确知每个变量的类型，能够生成更高效的代码；更易理解与推理（easier to understand and reason about），阅读声明即可确知变量中存放的是什么；错误检查更完善（better error checking）。Slides 41–42 展开第三点。Python 版本：

```python
def add_3(x):
    return x + 3

add_3("CS106L") # Oops, that's a string. Runtime error!
```

这段代码可以通过一切语法检查；只有当程序实际运行、以字符串实参进入函数并执行到 `x + 3` 时才报错。换言之，语言本身没有任何机制在运行之前阻止字符串被传入。同一函数的 C++ 版本：

```cpp
int add_3(int x) {
    return x + 3;
}

add_3("CS106L"); // Can't pass a string when int expected. Compile time error!
```

函数签名明示参数类型为 int，传入字符串在 compile time 即被拒绝，程序根本没有机会带着错误的参数运行。错误被发现得越早，定位与修复的成本越低，这是静态类型在错误检查方面的核心优势。

## 6. 例题与解析：为声明补全类型（Slides 44–45）

Slide 44 给出填空练习：为下列每行补上正确的类型。题目附有提示：`(int) x` 将 x 强制转换为 int，直接舍弃小数部分，例如 `(int) 5.7` 等于 5。

```cpp
______ a = "test";
______ b = 3.2 * 5 - 1;
______ c = 5 / 2;
______ d(int foo) { return foo / 2; }
______ e(double foo) { return foo / 2; }
______ f(double foo) { return (int)(foo + 0.5); }
______ g(double c) { std::cout << c << std::endl; }
```

Slide 45 给出答案：

```cpp
std::string a = "test";
double   b = 3.2 * 5 - 1;
int      c = 5 / 2; // What does this equal?
int      d(int foo) { return foo / 2; }
double   e(double foo) { return foo / 2; }
int      f(double foo) { return (int)(foo + 0.5); } // What's this?
void     g(double c) { std::cout << c << std::endl; }
```

逐行解析如下。a 的初值为字符串字面量，类型为 std::string。b 的表达式 `3.2 * 5 - 1` 含浮点操作数，运算结果为浮点值，类型为 double。c 为 `5 / 2`：两个 int 相除执行整数除法，小数部分被直接截断，故其值为 2 而非 2.5，类型为 int——slide 注释 "What does this equal?" 正是针对这一易错点。d 以 int 为参数并返回 `foo / 2`，整数除以整数的结果仍为整数，返回类型为 int。e 的参数为 double，`foo / 2` 为浮点除法，返回类型为 double。f 将 foo 加 0.5 后以 `(int)` 截断，是利用截断实现四舍五入的惯用写法（对正数成立）：如 foo 为 2.6，加 0.5 得 3.1，截断得 3，返回类型为 int。g 仅向标准输出打印、不返回任何值，返回类型为 void。

## 7. 插叙：函数重载（Slides 46–49）

承接上例中参数类型不同的 d 与 e，Slides 46–47 介绍 function overloading（函数重载）：同名而参数不同的多个函数可以同时定义。

```cpp
double axolotl(int x) {          // (1)
    return (double) x + 3;   // typecast: int → double
}

double axolotl(double x) {       // (2)
    return x * 3;
}

axolotl(2);          // uses version (1), returns 5.0
axolotl(2.0);        // uses version (2), returns 6.0
```

两个函数同名 axolotl：版本 (1) 接收 int，先将 x 强制转换为 double 再加 3（注释中的 typecast 即类型转换）；版本 (2) 接收 double，直接乘 3。编译器依据实参的类型选择调用的版本：`axolotl(2)` 的实参为 int，走版本 (1)，`(double) 2 + 3` 得 5.0；`axolotl(2.0)` 的实参为 double，走版本 (2)，`2.0 * 3` 得 6.0。两个返回值均为 double，可见重载的分辨依据是参数列表而非返回类型。Slide 48 据此给出本阶段的小结：C++ is a compiled, statically typed language。

## 8. struct：将数据打包为新类型（Slides 50–61）

struct 一节的动机来自一个实际问题（Slide 51）。设想在系统中管理学生：每个 Stanford 学生的 ID 包含若干属性——姓名 name，类型为 string；SUNet（Stanford 网络账号名），类型为 string；编号 ID #，类型为 int。三样信息共同描述同一个对象。

Slides 52–53 进而提出将"生成新 ID"写作函数，随即暴露一个基本问题（a fundamental problem）：

```cpp
return_type issueNewID() {
    // How can we return all three things?
    // What should our return type be?

    // In Python this would look like…
    // return "Stanford Tree", "theTREE", 0000002
}
```

Python 中可以以元组的形式一次返回多个值（`return "Stanford Tree", "theTREE", 0000002`），而 C++ 函数的返回类型只能标注一个类型：如何从函数返回多于一个值？Slide 55 引入 struct 作为解答：

```cpp
struct StanfordID {
    string name;            // These are called fields
    string sunet;           // Each has a name and type
    int idNumber;
};

StanfordID id;                          // Initialize struct
id.name = "THE Stanford Tree";         // Access field with '.'
id.sunet = "theTREE";
id.idNumber = 0000002;
```

上半段是类型定义：struct 关键字引出新类型 StanfordID，花括号内依次列出三个变量，它们被称为 fields（字段），每个 field 均有自己的名字与类型；定义以分号结束，这个分号是初学者最容易遗漏的字符。下半段是该类型的使用方式：`StanfordID id;` 声明一个该类型的变量，随后以点运算符 `.` 逐个访问 field 并赋值，如 `id.name = "THE Stanford Tree";`。

据此，Slide 56 的函数可一次返回全部三项信息：返回类型标注为 StanfordID，函数体内构造局部变量 id、填好三个 field，再将其整体返回。一个返回值即携带了完整的身份信息。

Slides 57–59 介绍 uniform initialization（统一初始化）语法，把"先声明、再逐字段赋值"的多行代码合并为一行：

```cpp
// Order depends on field order in struct. '=' is optional
StanfordID tree = { "THE Stanford Tree", "theTREE", 0000002 };
StanfordID lelandjr { "Leland Stanford Jr", "thejunior", 5430282 };
```

注释标明两条规则：其一，花括号内各值按 struct 中 field 的声明顺序一一对应，顺序不可错乱；其二，等号可以省略，第二行不带 `=` 的写法同样合法。Slide 59 据此将 issueNewID 改写为 `StanfordID id = { "THE Stanford Tree", "theTREE", 0000002 };` 后直接返回，整个函数缩减至两行。课件另在逐字段赋值的写法旁注明：这一写法将在后续课程深入讨论。

Slide 60 给出本节要点：struct 将若干具名变量（named variables）打包成一个新的类型。

## 9. 更多 struct 实例与 std::pair（Slides 62–72）

Slides 62–67 连续给出多个 struct 实例，说明 struct 的适用面极广：Name（first、last 两个 string，实例 `Name rf = { "Rachel", "Fernandez" };`）；Order（item 为 string、quantity 为 int，实例 `Order dozen = { "Eggs", 12 };`）；Point（x、y 两个 double，实例 `Point origin { 0.0, 0.0 };`）；以及嵌套使用既有类型的 Circle：

```cpp
struct Circle {
    Point center;
    double radius;
};
Circle circle { {0, 0} , 50000000 };
```

Circle 的第一个 field 的类型并非内置类型，而是此前刚刚定义的 Point：struct 的 field 可以是另一个 struct，初始化列表中在对应位置写 `{0, 0}` 即可完成嵌套初始化。

Slide 66 将四个例子并置，其形态上的相似性值得注意（slide 以 "Notice anything?" 标注）：Name、Order、Point 均只含两个 field，结构完全同型。若仅为捆绑两个值就专门定义一个 struct，定义本身显得重复。标准库为这一高频需求提供了现成方案 std::pair（Slide 68）。Slides 69–70 将 Order 的例子等价替换为：

```cpp
std::pair<std::string, int> dozen { "Eggs", 12 };
std::string item = dozen.first;            // "Eggs"
int quantity = dozen.second;               // 12
```

std::pair 是标准库提供的"二元"struct：两个成员的名字固定为 first 与 second，其类型在尖括号中逐一指定；需要承载其他类型的组合时，只需更换尖括号中的类型。

尖括号本身的含义由 Slides 71–72 揭示：std::pair 是一个 template（模板），课件注明其细节留待后续课程展开。其定义形如：

```cpp
template <typename T1, typename T2>
struct pair {
    T1 first;
    T2 second;
};
```

T1、T2 是两个待定的类型参数。当代码中出现 `std::pair<std::string, int>` 时，编译器即以 std::string 与 int 分别代入 T1、T2，生成如下具体类型：

```cpp
struct pair {
    std::string first;
    int second;
};
```

此处只需建立如下直觉：pair 是"类型的模具"，代入不同类型即得到不同的具体 pair；模板的完整机制将在后续课程讨论。

## 10. std 与 C++ 标准库（Slides 73–82）

至此，前文反复出现的 std::pair、std::string、std::cout 中的 std 尚未正式说明，Slides 73–74 即以此设问。Slide 75 给出答案：std 指 the C++ Standard Library（C++ 标准库），它提供内置的类型、函数等大量设施；使用前须以 #include 引入相应的头文件：`#include <string>` 提供 std::string；`#include <utility>` 提供 std::pair；`#include <iostream>` 提供 std::cout 与 std::endl。下面这段最小程序同时用到其中数项：

```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name = "Rachel";
    std::cout << name << std::endl;

    return 0;
}
```

Slides 76–77 说明命名规范：标准库的名字一律冠以 std:: 前缀使用。若在文件开头书写 `using namespace std;`，前缀确实可以省略，但课件明确将其归为 bad style，因为它可能引入歧义：

```cpp
#include <algorithm>
using namespace std;

// You write your own sort function
void sort(int a, int b) {
  cout << "rachel's sort >:D!";
}

int main() {
  sort(3, 5); // which sort? rachel's or std::sort?
}
```

标准库中本已存在 std::sort；此处又自定义了一个名为 sort 的函数，那么 `main` 中的 `sort(3, 5)` 调用的究竟是哪一个，便不再明确。`using namespace std;` 将标准库的全部名字一次性引入当前文件，与开发者自定义名字冲突的风险正源于此，因此应当坚持显式书写 std:: 前缀。Slide 78 另给出资料指引：查阅标准库文档应使用 cppreference.com；cplusplus.com 内容过时且广告繁多，应予回避。

Slides 79–81 借 std::pair 说明 #include 的机制。std::pair 定义于名为 utility 的头文件中，使用前必须先行引入：

```cpp
#include <utility>

// Now we can use `std::pair` in our code.

std::pair<double, double> point { 1.0, 2.0 };
```

`#include` 的作用（Slides 80–81 以图示演示）是把目标头文件的全部内容原样插入到该指令所在的位置。就上例而言，插入完成后，当前文件中便存在 namespace std 内定义的 pair 模板，其后对 std::pair 的使用才具备编译所需的定义；若不 include，编译器无从得知 std::pair 是什么，代码无法通过编译。

## 11. 代码演示：求解一元二次方程（Slides 83–89）

本节的代码演示任务是编写求解一元二次方程的函数。Slide 84 以两个实例建立直观：x² - 3x + 2 = 0 有两个解 x = 1 与 x = 2，对应抛物线与 x 轴的两个交点；2x² + 1 = 0 则无解，对应抛物线整体位于 x 轴上方。二次方程可能有两个解，也可能根本没有解，程序必须能够同时表达这两种情形。

Slide 85 给出数学基础：对 ax² + bx + c = 0，解为求根公式 x = (-b ± √(b² - 4ac)) / 2a；当判别式 b² - 4ac 为负时，不存在实数解。"有无解"与"解为何值"需要一并传达给调用者，Slide 86 据此给出函数声明，并逐部分标注其构成：

```cpp
std::pair<bool, std::pair<double, double>> solveQuadratic(double a, double b, double c);
```

参数为三个 double 系数 a、b、c（Coefficients）；返回值整体为一个 `std::pair`，其中外层 bool 回答"是否存在解"（Is there a solution?），内层 `std::pair<double, double>` 携带"若有，两个解为多少"（What are the solutions (if any)?）。以 pair 嵌套 pair，两个问题合并为一次返回——上一节所学的 std::pair 在此直接派上用场。Slide 87 对应两种返回值形态：有实根时返回 `{ true, { 1.0, 2.0 }}`；无实根时 bool 位置为 false，第二个成员取值无关紧要，如 `{ false, { 0.0, 0.0 }}`。

Slide 88 布置实现任务，并提示 <cmath> 头文件中的 sqrt 函数可用于求平方根（Slide 89 为现场编写环节，过程从略）。实现思路是直接的：先计算判别式 `b*b - 4*a*c`，若其为负则返回 `{ false, ... }`；否则以 sqrt 与求根公式求得两根，返回 `{ true, { 根1, 根2 } }`。

## 12. 使用 using 与 auto 改进代码（Slides 90–99）

返回类型 `std::pair<bool, std::pair<double, double>>` 书写冗长，重复出现时尤为繁琐。Slides 91–93 引入 using 关键字创建 type alias（类型别名）：

```cpp
using Zeros = std::pair<double, double>;
using Solution = std::pair<bool, Zeros>;
Solution solveQuadratic(double a, double b, double c);
```

第一行命名 `std::pair<double, double>` 为 Zeros；第二行命名 `std::pair<bool, Zeros>` 为 Solution——别名可以引用另一别名；第三行的函数声明随之一目了然，且 Solution 这一名字自带语义。Slide 93 的概括是：using 相当于"类型的变量"，即为类型命名。

Slides 94–95 引入 auto 关键字，由编译器推断类型。接收返回值时，原写法须完整拼出类型：

```cpp
std::pair<bool, std::pair<double, double>> result = solveQuadratic(a, b, c);
```

改用 auto 后：

```cpp
auto result = solveQuadratic(a, b, c);

// This is exactly the same as the above!
// result still has type std::pair<bool, std::pair<double, double>>
// We just told the compiler to figure this out for us!
```

代码注释说明了要点：二者完全等价，result 的类型仍是 `std::pair<bool, std::pair<double, double>>`，只是编译器依据 solveQuadratic 声明过的返回类型代为填写。

Slide 96 强调 auto 并未把 C++ 变成动态类型语言：

```cpp
auto i = 1;   // int inferred
i = "hello!"; // Doesn't compile
```

`auto i = 1;` 由编译器在编译期推断出 i 为 int；推断完成后类型即告固定，此后向 i 赋字符串值无法通过编译。auto 只是省去显式书写，静态类型检查丝毫未减。

Slides 97–98 进一步比较可读性：`std::pair<bool, std::pair<double, double>> result = ...;` 与 `auto result = ...;` 何者更清楚？前者类型信息显式但冗长，后者简洁但须查阅函数签名方知类型；类似地，就 `auto i = 1;` 与 `int i = 1;` 而言，auto 对极短的类型并无优势。权衡原则可以概括为：类型名冗长且上下文足以明确时，auto 使代码更整洁；类型本身构成重要信息时，显式书写可能更清楚。

## 13. 本讲回顾（Slides 100–102）

Slide 101 归纳本讲五点：其一，C++ 是 compiled、statically typed 的语言；其二，struct 将数据打包为单个对象；其三，std::pair 是含两个 field 的通用 struct；其四，使用标准库的内置类型须 #include 相应头文件，并冠以 std:: 前缀；其五，using 创建类型别名、auto 推断变量类型，二者均为改善代码书写的特性。

## 本讲要点

- C++ 是 compiled、statically typed 的语言：编译器在 compile time 将整个程序翻译并打包为 executable file，随后才进入 run time；解释型语言（如 Python）的翻译与执行全部交织发生在 run time。
- static typing 要求每个变量声明类型，且类型一经声明不可改变；其收益是更高的效率、更好的可理解性与可推理性和更完善的错误检查——同一逻辑错误在 Python 中表现为 run time error，在 C++ 中则在 compile time 即被拦截。
- struct 将若干 named variables（fields）打包成一个新类型；以 `.` 访问 field，也可用 uniform initialization 以花括号列表一次初始化（顺序须与 field 声明一致，`=` 可省略），field 还可以是另一个 struct。
- std::pair 是标准库提供的二元模板 struct（成员固定为 first 与 second），定义于 \<utility\> 头文件；#include 的实质是把头文件内容插入当前文件。
- 标准库名字应冠以 std:: 前缀；`using namespace std;` 可能与自定义名字（如自行编写的 sort）产生歧义，属于 bad style。
- using 创建 type alias，auto 让编译器在编译期推断变量类型；二者仅简化书写，类型仍然是静态确定的。
