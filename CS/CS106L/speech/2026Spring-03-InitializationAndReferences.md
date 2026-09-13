---
title: "Lecture 03 · Initialization & References 逐字稿"
createAt: 2026/9/13
---

# Lecture 03: Initialization & References（逐字稿）

> 对应课件转写：[2026Spring-03-InitializationAndReferences.md](../output/2026Spring-03-InitializationAndReferences.md)

## 1. 回顾：auto 与 struct（Slide 2–4）

展开本讲主题之前，先回顾上一讲引入的两个关键词。其一是 auto：`auto` 的语义可概括为对编译器的一条指令——"Hey compiler, figure out this type"，即由编译器推导类型。课件给出的使用建议有两条：是否使用由开发者自行斟酌；当类型名称书写繁琐时，auto 尤为有用。

```cpp
#include <iostream>
#include <string>
#include <map>
#include <unordered_map>
#include <vector>

int main()
{
    std::map<std::string, std::vector<std::pair<int, std::unordered_map<char, double>>>>
    complexType;
    /// confusing iterator type (We'll find out what this is in the iterators lecture!)
    std::map<std::string,std::vector<std::pair<int,std::unordered_map<char,double>>>>::iterator
    it = complexType.begin();
    // clear(er) iterator type!
    auto it = complexType.begin();
    return 0;
}
```

若为 `complexType` 显式声明迭代器，必须将整个冗长的类型名原样重复并追加 `::iterator`；改用 `auto it = complexType.begin();` 则一行即可完成同等声明。iterator 的确切含义留待迭代器一讲展开，此处只需体会 auto 在此类场景中的价值。其二是 struct：`struct` 的语义是"Group these variables together, in one type"，即把若干变量组织成一个自定义类型。auto 解决类型名冗长的问题，struct 解决相关数据分散的问题，二者共同为本讲内容做铺垫。

## 2. 本讲结构与初始化的定义（Slide 6–8）

课件列出本讲五个主题：Initialization（初始化）、References（引用）、L-values vs R-values、const，以及 C++ 程序的编译方法。前四者构成一条递进的主线：先讨论如何初始化变量，继而引入 reference，随后明确引用所能绑定的表达式类别，最后以 const 约束修改权限；第五项为实践性内容。

Initialization 的定义为："Provides initial values at the time of construction"，即在构造时提供初始值。定义的着重点在于 initial：初始值在对象构造的同时给出，而非先构造空对象、之后再赋值，二者是不同的操作。课件同时给出 cppreference 上 initialization 的文档链接以供查阅。

初始化的具体写法有三种：1. Direct initialization（直接初始化）；2. Uniform initialization（统一初始化）；3. Structured binding（结构化绑定）。

## 3. Direct initialization（Slide 9–11）

Direct initialization 使用圆括号提供初始值，如 `int numTwo(12.0);`。考虑如下代码：

```cpp
#include <iostream>

int main() {
  int numOne = 12.0;
  int numTwo(12.0);
  std::cout << "numOne is: " << numOne << std::endl;
  std::cout << "numTwo is: " << numTwo << std::endl;
  return 0;
}
```

第一行 `int numOne = 12.0;` 属于 copy-initialization（拷贝初始化），第二行则是 direct initialization。程序可以编译运行，两行输出均为 `12`：12.0 并非 int 类型，但编译器接受了这一写法，将其小数部分截去后存入 int 变量。

这类静默截断可能引发严重后果，课件以下例说明，并标注 "Critical? Yes"：

```cpp
#include <iostream>

void checkCool(float temperature) {
  if (temperature > 100.0) {
    std::cout << "Emergency cooling activated!" << std::endl;
  } else {
    std::cout << "Temperature normal. No emergency cooling required.";
  }
}

int main() {
  float temperatureReading(100.8);
  int temperature = temperatureReading;
  checkCool(temperature);
  return 0;
}
```

该程序模拟温度监控逻辑：温度超过 100 度时应触发紧急冷却。传感器读数 `temperatureReading` 为 100.8，已经超标；但 `int temperature = temperatureReading;` 将其存入 int，小数部分被静默截去，`temperature` 的值为 100。`checkCool` 收到的实参因此是 100，条件 `temperature > 100.0` 不成立，程序输出 "Temperature normal"，紧急冷却逻辑永远不会执行。

编译器对这类精度丢失不做任何干预，课件以编译器的口吻概括这一行为："You want 100.8 to be an integer? Okay"。这种将值存入表示范围更小的类型、从而丢失信息的转换称为 narrowing conversion（收窄转换）。无论 copy-initialization 还是 direct initialization，都不会阻止 narrowing conversion 的发生；这正是引入 uniform initialization 的动机。

## 4. Uniform initialization（Slide 12–17）

Uniform initialization 与 direct initialization 在写法上的差别仅在于将圆括号替换为花括号。考虑如下代码：

```cpp
#include <iostream>

int main() {
    int numOne = {12.0};
    int numTwo{12.0};
    std::cout << "numOne is: " << numOne << std::endl;
    std::cout << "numTwo is: " << numTwo << std::endl;
    return 0;
}
```

与第 3 节的代码相比，仅有括号形式不同，此处程序无法通过编译。Uniform initialization 禁止 narrowing conversion：当花括号中的值无法无损地转换为目标类型时，编译器直接报错。这一行为差异是两种初始化方式的核心区别。

课件归纳 uniform initialization 的两点优势。其一为 Safe：不存在 narrowing conversion。其二为 Ubiquitous（普遍适用）：vector、map 以及自定义 class 均可使用这套花括号语法，故名"统一"初始化。

两个容器示例。map 的统一初始化：

```cpp
#include <iostream>
#include <map>

int main() {
    // Uniform initialization of a map.
    std::map<std::string, int> ages{
        {"Alice", 25},
        {"Bob", 30},
        {"Charlie", 35}
    };
    // Accessing map elements.
    std::cout << "Alice's age: " << ages["Alice"] << std::endl;
    std::cout << "Bob's age: " << ages.at("Bob") << std::endl;
    return 0;
}
```

键值对以嵌套花括号的形式逐项列出，构造一步完成；元素访问可用 `ages["Alice"]` 或 `ages.at("Bob")`。vector 同理：

```cpp
#include <iostream>
#include <vector>
int main() {
  // Uniform initialization of a vector.
  std::vector<int> numbers{1, 2, 3, 4, 5};
  // Accessing vector elements.
  for (int num : numbers) {
    std::cout << num << " ";
  }
  std::cout << std::endl;
  return 0;
}
```

`std::vector<int> numbers{1, 2, 3, 4, 5};` 一行即完成五个元素的装载，配合 range-based for loop 即可遍历输出。

Uniform initialization 同样适用于自定义 struct。以上一讲的 `issueID` 为例，逐字段赋值的写法：

```cpp
StanfordID issueID() {
    StanfordID id;
    id.name = "THE Stanford Tree";
    id.sunet = "theTREE";
    id.idNumber = 0000002;
    return id;
}
```

可借助 uniform initialization 简化为：

```cpp
StanfordID issueID() {
    StanfordID id = {"THE Stanford Tree", "theTREE", 0000002};
    return id;
}
```

各值按成员的声明顺序在花括号中列出，构造一次完成。

## 5. Structured binding（Slide 18–22）

第三种方式是 structured binding，其用途有二：从大小固定的数据结构中一次初始化多个变量；接收函数返回的多个值。

考虑如下代码：

```cpp
#include <iostream>
#include <tuple>
#include <string>

std::tuple<std::string, std::string, std::string> getClassInfo() {
    std::string className = "CS106L";
    std::string buildingName = "Thornton 110";
    std::string language = "C++";
    return {className, buildingName, language};
}

int main() {
    auto [className, buildingName, language] = getClassInfo();
    std::cout << "Come to " << buildingName << " and join us for " << className
              << " to learn " << language << "!" << std::endl;
    return 0;
}
```

代码中有两处语法需要区分。`return {className, buildingName, language};` 使用花括号直接构造待返回的 tuple，属于 uniform initialization；`auto [className, buildingName, language] = getClassInfo();` 才是 structured binding：方括号内列出若干名字，函数返回的 tuple 中的值按位置顺序逐一绑定到这些变量。

若不使用 structured binding，取出 tuple 的三个成员只能按下标访问：

```cpp
auto classInfo = getClassInfo();
std::string className = std::get<0>(classInfo);
std::string buildingName = std::get<1>(classInfo);
std::string language = std::get<2>(classInfo);
```

四行代码完成的操作，structured binding 一行即可实现，且变量名自带语义，无需借助 `std::get<0>`、`std::get<1>` 等下标推断含义。

Structured binding 有一条使用限制：Size must be known at compile time——被绑定的结构，其大小必须在编译期已知。tuple、pair、struct 等定长结构均满足该条件。至此初始化部分讨论完毕。

## 6. Reference：引用（Slide 24–30）

Reference 的定义为："An alias to an already-existing object or function"，即已存在对象或函数的别名。关键词是 alias：reference 并非新对象，而是既有对象的另一个名字。其语法标记只有一个符号：`&`（ampersand）。

考虑如下代码：

```cpp
#include <iostream>

int main() {
    int miToMoon = 238855; // That's how far the moon is.
    std::cout << "Moon is " << miToMoon << "mi away." << std::endl;

    int& ISS = miToMoon;
    ISS -= 254; // That's how high the ISS is.

    std::cout << "ISS is " << ISS << "mi to moon." << std::endl;
    std::cout << "Moon is " << miToMoon << "mi away." << std::endl;
    return 0;
}
```

声明 `int& ISS = miToMoon;` 中的类型写作 `int&`，即"int 的 reference"。该行之后，ISS 成为 miToMoon 的别名，二者是同一个变量。

这一过程对应的内存状态可分三步说明。执行 `int miToMoon = 238855;` 后，内存中出现一个名为 miToMoon 的单元，值为 238855。执行 `int& ISS = miToMoon;` 时，内存中并不会新出现一个名为 ISS 的独立单元——课件在内存图中以红叉明确否定了这一直觉性理解：reference 不占用独立的存储，它只是同一单元的第二个名字。因此执行 `ISS -= 254;` 改变的正是这唯一单元中的值，238855 变为 238601。最后两条输出语句分别打印 ISS 与 miToMoon，结果均为 238601：通过别名修改与通过原名修改是同一件事。

## 7. Pass by value 与 pass by reference（Slide 31–34）

引用最常见的用途是函数传参。考虑如下代码：

```cpp
#include <iostream>
#include <math.h>

void squareN(int& n) {
  n = pow(n, 2);
}

int main() {
  int num = 5;
  squareN(num);
  std::cout << num << std::endl;
  return 0;
}
```

参数声明 `int& n` 中的 `&` 表明 n 是引用。调用 `squareN(num)` 时，n 即 num 的别名，函数内对 n 的平方运算直接作用于 num 本身，程序输出 25。这种传参方式称为 pass by reference（按引用传递）。

作为对照，考察不带 `&` 的情形，即 pass by value（按值传递）：

```cpp
#include <iostream>
#include <math.h>

void squareN(int n) {
    n = pow(n, 2);
}

int main() {
    int num = 5;
    squareN(num);
    std::cout << num << std::endl;
    return 0;
}
```

此时 n 是 num 的一份 copy：内存中存在两个独立单元，num 恒为 5，n 由 5 变为 25。被修改的只是拷贝，函数返回后拷贝即销毁，故程序输出仍为 5。

两种方式的取舍可概括如下。Pass by value 复制变量，当变量是大型对象时，复制开销可能相当可观；pass by reference 使用同一变量、同一块内存，避免了复制，代价是函数可以直接修改实参。二者的选择取决于语义需求：是否需要修改实参，以及是否需要避免复制开销。

## 8. 经典错误：循环变量被拷贝（Slide 35–37）

以下代码展示了引用与 structured binding 叠加使用时的一个典型错误，课件标题为 "A Classic Reference Copy Bug"：

```cpp
#include <iostream>
#include <math.h>
#include <vector>

void shift(std::vector<std::pair<int, int>> &nums) {
    for (auto [num1, num2] : nums) {
        num1++;
        num2++;
    }
}
```

该函数的意图是将 nums 中每个 pair 的两个成员各加一。函数参数已经使用 pass by reference，循环也使用了 structured binding，但课件明确指出：Does not modify nums。原因在于 range-based for 的循环变量 `auto [num1, num2]` 中没有 `&`，每一轮迭代都会把当前的 pair 拷贝一份到 num1 与 num2；自增作用在拷贝上，迭代结束拷贝即被丢弃，nums 本身不变。

修复方法是给循环变量的类型声明加上 `&`：

```cpp
#include <iostream>
#include <math.h>
#include <vector>
void shift(std::vector<std::pair<int, int>> &nums) {
  for (auto& [num1, num2] : nums) {
    num1++;
    num2++;
  }
}
```

`auto& [num1, num2]` 使 num1、num2 成为 pair 成员的引用，自增才真正作用于 nums 中的元素。编写 range-based for 时应当明确：需要修改容器元素时必须使用引用形式，仅在只读场景下才可接受拷贝。

## 9. lvalue 与 rvalue（Slide 38–42）

引用是既有对象的别名，由此产生一个问题：什么样的表达式可以作为引用的绑定对象。课件为此引入 lvalue（左值）与 rvalue（右值）的区分。先以三行代码建立直觉。

```cpp
int x = 5;
```

合法。变量（variable）既可以出现在赋值号左侧，也可以出现在右侧。

```cpp
int 5 = x;
```

非法。值（value）不能出现在赋值号左侧，无法对字面量 5 赋值。

```cpp
int y = x;
```

合法，右侧的 x 同样是变量。综合三例：变量在赋值号两侧均可出现，值只能出现在右侧。

课件以表格给出二者的正式定义。lvalue，全称 Locator Value：具有确定的内存地址，可以"定位"到它；可出现在赋值号左侧或右侧。rvalue，全称 Read Value：临时值，没有内存地址，只能出现在赋值号右侧。以示例对应：`int x = 10;` 中左侧的 x 是 lvalue，右侧的 10 是 rvalue；`int y = x;` 中左右两侧的 y 与 x 均为 lvalue。`int 5 = x;` 之所以非法，是因为试图为一个没有地址的临时值指定存储位置，这一操作没有意义。

该区分直接约束了引用的使用。第 7 节的 `squareN(int& n)` 要求实参为 lvalue：reference 是别名，别名必须绑定在一个真实存在、有地址的对象上；临时值不具备被绑定的条件，因此传参必须传 lvalue。`squareN(num);` 传入的 num 是 lvalue，合法；而下列代码无法通过编译：

```cpp
#include <iostream>
#include <math.h>
// note the ampersand
void squareN(int& n) {
    // calculates n to the power of 2
    n = pow(n, 2);
}
int main() {
    squareN(5);
    return 0;
}
```

`squareN(5)` 传入的字面量 5 是 rvalue，而 `int& n` 只能接受 lvalue，编译器拒绝该调用。规则可归纳为：非 const 的 reference 只能绑定 lvalue，不能绑定 rvalue。

## 10. const 与 const reference（Slide 43–48）

在引用与值类别之后，还需要引入 const 对读写权限加以约束。const（constant 的缩写）的定义为："Such object cannot be modified"——被 const 限定的对象不可修改。课件给出 cppreference 上 cv 限定符（const 与 volatile）的文档链接，本讲仅涉及 const。

const 与 reference 组合使用时，修改权限如何传递？考虑如下代码，其中四次 push_back 的合法性各不相同：

```cpp
#include <iostream>

int main() {
  std::vector<int> vec{ 1, 2, 3 };
  const std::vector<int> const_vec{ 1, 2, 3 };
  std::vector<int>& ref_vec{ vec };
  const std::vector<int>& const_ref{ vec };

  vec.push_back(3);
  const_vec.push_back(3);
  ref_vec.push_back(3);
  const_ref.push_back(3);
  return 0;
}
```

逐行分析。`vec.push_back(3);`：vec 是普通 vector，合法。`const_vec.push_back(3);`：const_vec 的类型是 const 的 vector，push_back 属于修改操作，编译错误。`ref_vec.push_back(3);`：ref_vec 是 vec 的非 const 引用，通过别名修改 vec 本身，合法。`const_ref.push_back(3);`：const_ref 是 vec 的 const 引用，通过它同样不能执行修改操作，编译错误。规律在于：const 依附于类型，无论通过原对象还是通过别名访问，const 类型的对象都不允许修改。

另一处更隐蔽的约束：

```cpp
#include <iostream>

int main() {
  const int a = 5;

  int& b = a;
  b++;

  std::cout << a << std::endl;
  return 0;
}
```

a 是 const int，代码试图以非 const 引用 b 绑定 a 并执行 b++，该程序无法通过编译。原因在于：若允许 `int& b = a;`，便可以通过别名 b 修改 a，const 的不可修改承诺即被绕过；因此 C++ 禁止以 non-const reference 绑定 const 对象。

正确的写法是为引用同样加上 const：

```cpp
#include <iostream>

int main() {
    const int a = 5;

    const int& b = a;
    //b++;

    std::cout << a << std::endl;
    return 0;
}
```

`const int& b = a;` 声明了一个只读别名，绑定 const 对象合法；`b++` 随之被注释——通过 const reference 同样只能读取、不能修改。

## 11. 编译 C++ 程序与应用（Slide 49–54）

本讲最后一项主题是 C++ 程序的编译。源文件 source.cpp 是人类可读的源代码，可执行文件 machine.exe 是机器码，从前者到后者的转换过程即 Compiling。

关于这一过程有三点说明。第一，C++ 是编译型语言，不能像 Python 那样被解释执行。第二，C++ 需要 compiler（编译器）——将源代码翻译为机器码的程序，常用的有 clang 与 g++。第三，编译通过一条命令完成：

```
$ g++ --std=c++23 main.cpp -o main
```

该命令的四个组成部分：g++ 是编译器程序本身；`--std=c++23` 指定使用 C++23 语言标准；main.cpp 是输入文件；`-o main` 指定输出可执行文件名为 main。编译产物用以下命令运行：

```
$ ./main
```

Windows 环境下为 `$ .\main.exe`。这两条命令是后续完成作业与运行示例的基础。

课件另以两页展示 C++ 的应用场景：自动驾驶、NVIDIA CUDA、量化金融机构的交易系统、游戏 Fortnite 等均依赖 C++ 及其并行计算能力；机器学习框架 TensorFlow 的核心（Core）主要由 C++ 编写，包含两千余个源文件。

## 本讲要点

- 初始化优先使用 uniform initialization（花括号写法）：它禁止 narrowing conversion，且适用于 vector、map、自定义 class 等各类类型；copy-initialization 与 direct initialization 则会静默接受收窄转换，可能导致 100.8 被截为 100 一类的逻辑错误。
- reference 是已存在对象的别名（如 `int& ISS = miToMoon;`），不占用独立存储；通过引用的修改即对原对象的修改。函数传参使用 pass by reference 既可真正修改实参，又可避免复制大型对象的开销；pass by value 修改的只是拷贝。
- range-based for 中 `auto [num1, num2]` 会对每个元素做拷贝，需要修改容器元素时必须写作 `auto& [num1, num2]`，否则函数实际不产生任何修改效果。
- lvalue（Locator Value）具有内存地址，可出现在赋值号两侧；rvalue（Read Value）是无地址的临时值，只能出现在赋值号右侧。非 const 的 reference 只能绑定 lvalue，不能绑定 rvalue。
- const 对象不可修改，且 const 依附于类型、随引用传递：const 对象只能被 const reference 绑定，以 non-const reference 绑定会直接导致编译错误。
- C++ 是编译型语言：`g++ --std=c++23 main.cpp -o main` 完成编译，`./main`（Windows 下 `.\main.exe`）运行。
