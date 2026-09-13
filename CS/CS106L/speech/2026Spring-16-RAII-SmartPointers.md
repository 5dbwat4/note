---
title: "Lecture 16 · RAII, Smart Pointers & Building Projects 逐字稿"
createAt: 2026/9/13
---

# Lecture 16: RAII, Smart Pointers & Building Projects（逐字稿）

> 对应课件转写：[2026Spring-16-RAII-SmartPointers.md](../output/2026Spring-16-RAII-SmartPointers.md)

## 1. 本讲内容概览

本讲依次讨论三个主题：其一为 RAII（Resource Acquisition Is Initialization，资源获取即初始化），它是 C++ 管理各类运行期资源的核心思想；其二为 smart pointer（智能指针），即 RAII 思想在动态内存管理上的标准库实现；其三为 C++ 项目的基本构建流程，涵盖编译器命令、make/Makefile 与 CMake。三者之间存在内在联系：前两者回答"资源在异常等复杂控制流下如何可靠释放"，第三者回答"代码规模扩大后如何组织编译"。论证的起点并非定义，而是一段看似平凡的函数——它暴露出手工资源管理在异常面前的不堪一击。

## 2. 引例：一个函数有多少条执行路径

考虑如下函数：

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

从纯粹的语法控制流观察，该函数只含一个 `if` 分支与一个 `return` 语句：条件成立时先输出再返回，条件不成立时直接返回。按这种数法，执行路径不过两三条，课件给出的初步猜测也正是"3 条"。

这一估计的问题在于，它只统计了由 `if` 构造的显式分支，而完全忽略了另一类隐式控制流——异常。函数中每一次函数调用、每一个临时对象的构造，都可能成为控制流悄然离开函数的出口。要准确回答"有多少条路径"，必须先弄清异常在 C++ 中的行为方式。

## 3. 异常与 try/catch

Exception（异常）是 C++ 处理运行期错误的机制：错误发生时，代码可以抛出（throw）一个异常对象，控制流随即离开当前位置并沿调用链向上传播；若无人处理，程序以错误告终。不过，我们可以编写处理异常的代码，使程序在错误发生后继续执行而不必整体失败，这一动作称为捕获（catch）。

其结构由 `try` 块与若干 `catch` 子句构成：

```cpp
try {
    // code that we check for exceptions
}
catch ([exception type] e1) {        // "if"
    // behavior when we encounter an error
}
catch ([other exception type] e2) {  // "else if"
    // ...
}
catch {                              // the "else" statement
    // catch-all
}
```

课件以注释标明了 `catch` 子句与条件语句的对应关系：前两个带类型的 `catch` 相当于 `if` 与 `else if`，只捕获匹配类型的异常；末尾不带参数的 `catch` 则相当于 `else`，捕获一切类型的异常。

一个具体例子：

```cpp
try {
    int age = 15;
    if (age >= 18) {
        cout << "Access granted - you are old enough.";
    } else {
        throw (age);
    }
}
catch (int myNum) {
    cout << "Access denied - You must be at least 18 years old.\n";
    cout << "Age is: " << myNum;
}
```

`age` 为 15，不满足 `age >= 18`，于是执行 `throw (age)`，抛出一个 `int` 类型的异常；`catch (int myNum)` 与该类型匹配，异常值绑定到 `myNum`，控制流转入处理代码。程序的执行由此从 `try` 块内部"跳跃"到了 `catch` 块，`try` 块中抛出点之后的语句一律不再执行。

这一"跳跃"语义正是本讲关注异常的原因：它会无声地跳过函数体中的任意一段代码，包括那些负责释放资源的语句。

## 4. 例题与解析：被低估的路径数量

回到第 2 节的 `returnNameCheckPawsome`。若把每一条可能抛出异常的语句都视为一个潜在出口，该函数的执行路径至少有 23 条，其构成如下：

- （1 条）按值传参触发 `Pet` 的拷贝构造函数，它可能抛出异常；
- （5 条）过程中构造的 5 个临时 `std::string`，其构造函数可能抛出异常；
- （6 条）对 `type()`（1 次）、`firstName()`（3 次）、`lastName()`（2 次）共 6 次成员函数调用可能抛出异常；
- （10 条）代码中出现的用户自定义重载运算符（`operator==`、`operator<<`、`operator+` 等）共 10 处调用，均可能抛出异常；
- （1 条）返回时 `std::string` 的拷贝构造可能抛出异常。

合计 1 + 5 + 6 + 10 + 1 = 23。课件据此给出的结论是"至少 23 条代码路径"（at least 23 code paths）。

这一结果说明：在考虑异常的前提下，即使表面只有一两个分支的函数，其真实控制流也远比肉眼所见复杂。任何一条隐藏路径都可能中断函数的执行，而这一点直接引出了下一节的致命问题——如果函数正持有尚未释放的资源，会发生什么。

## 5. 例题与解析：裸指针版本的问题

将上述函数改为在堆上构造对象、用毕释放的形式：

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

（严格说，经指针访问成员应写作 `p->type()` 等；课件代码在此处作了记法上的简化，不影响下述分析。）

该函数的资源管理协议十分明确：`new Pet(petId)` 在堆上获取资源，`delete p` 在返回前将其释放。在不发生异常的前提下，这一协议是完整的。但第 4 节的结论同样适用于此处：`if` 条件中的调用、输出语句、字符串拼接、`returnStr` 的构造——任何一处抛出异常，控制流都会立即离开函数，位于 `delete p` 之前的所有语句都不会执行，`delete` 因此被跳过。已分配的内存从此无人负责释放，形成 memory leak（内存泄漏）。

课件的连环追问"What if this function threw an exception here? Or here? Or anywhere an exception can be thrown?"意在强调：泄漏并不依赖于某个特定语句出错，只要任意一条异常路径在 `delete` 之前触发，资源就必然泄漏。手工配对的 `new`/`delete` 在异常面前系统性失效，这正是需要解决的核心问题。

## 6. 资源与释放：问题的普遍性

上述困境并非堆内存独有。大量资源遵循同一模式：先获取（acquire），后释放（release），且两种操作必须配对发生：

| 资源 | 获取 | 释放 |
|---|---|---|
| Heap memory | `new` | `delete` |
| Files | `open` | `close` |
| Locks | `try_lock` | `unlock` |
| Sockets | `socket` | `close` |

只要异常打断了"获取"与"释放"之间的代码，释放操作就被跳过，而泄漏的可能是文件句柄、锁、套接字等比内存更稀缺或影响面更大的资源。于是问题一般化为：当异常可能在任何位置发生时，如何保证资源总能被正确释放？RAII 即是对这一问题的系统性回答。

## 7. RAII：资源获取即初始化

RAII（Resource Acquisition Is Initialization）由 C++ 的设计者 Bjarne Stroustrup 发展提出，是 C++ 以及其他一些语言中最具代表性的概念之一。其内容可以概括为两条纪律：

- 类使用的所有资源都应在构造函数（constructor）中获取；
- 类使用的所有资源都应在析构函数（destructor）中释放。

遵循 RAII 带来三方面保证。其一，避免"half-valid"（半有效）状态：对象要么完成资源获取而完全可用，要么构造失败而不存在，不会停留在介于两者之间的中间态。其二，无论控制流以何种方式离开作用域——正常返回抑或异常传播——析构函数都会被调用，资源因此必然得到释放。其三，资源在对象创建完成时即已就绪，获取与初始化合二为一，对象立即可用。

对照第 5 节即可看出 RAII 的要害：裸指针失败，是因为"释放"被交给函数体中的一条普通语句，而普通语句在异常路径上会被跳过；RAII 把释放动作绑定到析构函数，把资源的生命周期与栈对象的生命周期捆绑在一起，从而绕开了这一缺陷。剩下的问题是，这一思想在具体场景中如何落地。

## 8. 两个不符合 RAII 的写法

判别一段代码是否符合 RAII，标准不在于资源"最终是否被释放"，而在于获取与释放是否分别由构造函数与析构函数承担。以下两例的资源获取与释放都写在函数体内，故均不合格。

第一例是文件处理：

```cpp
void printFile() {
    ifstream input;
    input.open("hamlet.txt");

    string line;
    while (getLine(input, line)) {  // might throw an exception
        std::cout << line << std::endl;
    }

    input.close();
}
```

`ifstream` 的打开与关闭由 `open` 与 `close` 显式完成，而非构造与析构；注释标明 `getLine` 可能抛出异常，一旦抛出，`close` 将被跳过。换言之，不合格的是这种用法而非 `ifstream` 类型本身：若以带参构造函数在构造时即打开文件，资源获取与初始化合一，才是 RAII 的写法。

第二例后果更为严重，涉及多线程环境下的锁：

```cpp
void cleanDatabase(mutex& databaseLock, map<int, int>& db) {
    databaseLock.lock();

    // no other thread or machine can change database
    // modify the database
    // if any exception is thrown, the lock never unlocks!

    databaseLock.unlock();
}
```

`lock` 与 `unlock` 之间的区域称为 critical section（临界区），其间不会有其他线程或机器修改数据库。若该区域内的任何代码抛出异常，`unlock` 不会执行，锁将永远不会被释放——正如课件注释所言"the lock never unlocks"。此后所有试图获取该锁的线程都会被无限期阻塞，其影响远超单次内存泄漏。

## 9. 修正方案：lock_guard

锁的问题有一个标准的 RAII 解法：

```cpp
void cleanDatabase(mutex& databaseLock, map<int, int>& db) {
    lock_guard<mutex> lg(databaseLock);
    // no other thread or machine can change database
    // modify the database
    // if exception is thrown, mutex is released

    // no explicit unlock necessary
}
```

`lock_guard` 是一个 RAII 封装（wrapper）：构造时尝试获取传入的互斥量，离开作用域时自动将其释放。获取动作发生在构造函数中，释放动作发生在析构函数中；无论函数正常返回还是因异常退出，析构函数都会执行，互斥量都会被解锁。显式的 `unlock` 不再必要，也不再可能被跳过。资源的安全性与书写的简洁性在此同时得到保证。

## 10. 智能指针：内存的 RAII 方案

锁有了 `lock_guard`，内存呢？这正是 smart pointer（智能指针）的出发点。C++ Core Guidelines 中的规则 R.11 对此有明确表述：

> **R.11: Avoid calling `new` and `delete` explicitly.**（避免显式调用 `new` 与 `delete`。）

其理由（Reason）部分值得完整复述：`new` 返回的指针应当归属于某个资源句柄（resource handle），由它负责调用 `delete`；若 `new` 返回的指针被直接赋给一个裸指针（naked pointer），对象就可能泄漏。课件引用的 Note 部分进一步指出：在大型程序中，散落于应用代码里的裸 `delete`（即不属于专门资源管理代码的 `delete`）极可能就是 bug——若程序中有 N 个 `delete`，如何确信不需要 N+1 个或 N−1 个？这类缺陷可能长期潜伏，直到维护期间才暴露；而裸 `new` 通常意味着某处存在配对的裸 `delete`，也就意味着可能存在 bug。该规则的 Enforcement 建议是：对一切显式的 `new` 与 `delete` 给出警告，并建议改用 `make_unique`。

实现手法与 `lock_guard` 完全同构：创建一个新对象，在构造函数中获取资源，在析构函数中释放资源。这类包裹动态资源的指针对象即称为智能指针。从结构上看，一个智能指针对象在自身内部持有动态获取的资源（dynamically acquired resource），资源的生命周期由此绑定到栈对象的生命周期。

标准库提供三类符合 RAII 的指针：

- `std::unique_ptr`：独占地（uniquely）拥有其资源，不可复制；
- `std::shared_ptr`：可以复制，底层内存在所有 `shared_ptr` 都离开作用域之后才被释放；
- `std::weak_ptr`：一类用于缓解 circular dependency（循环依赖）的指针，详见第 14 节。

与裸指针写法的对照：

```cpp
void rawPtrFn() {
    Node* n = new Node;
    // do smth with n
    delete n;
}
```

```cpp
void rawPtrFn() {
    std::unique_ptr<Node> n(new Node);
    // do something with n
    // n automatically freed
}
```

后者不出现任何显式 `delete`：`n` 离开作用域时析构函数自动释放底层内存，第 5 节中"异常跳过 `delete`"的问题在类型层面即告消失。

## 11. 例题与解析：unique_ptr 为什么禁止复制

考虑如下代码：

```cpp
void rawPtrFn() {
    std::unique_ptr<Node> n(new Node);

    // this is a compile-time error!
    std::unique_ptr<Node> copy = n;
}
```

以 `n` 初始化 `copy` 是编译期错误。原因在于 `unique_ptr` 的所有权（ownership）语义：资源由 `n` 独占，若允许复制，就会有两个指针指向同一块内存并都自认负责释放。

课件给出的论证是：设想复制发生之后，原对象的析构函数被调用——`n` 析构时释放了底层内存，而 `copy` 仍然存在并指向这块已被释放的内存。此时 `copy` 成为指向已释放内存的悬空指针，此后对它的任何使用乃至再次释放都是未定义行为。`unique_ptr` 通过在类型层面禁止复制，把这类错误从运行期提前到了编译期：写不出来，也就错不成。

这一禁令同时暴露了新的需求：有些场景确实需要多个指针指向同一对象。`shared_ptr` 正是为满足这一需求而设计的。

## 12. shared_ptr 与引用计数

`shared_ptr` 用另一种所有权模型绕开了复制 `unique_ptr` 的困难：只有当指向该内存的所有 `shared_ptr` 都离开作用域之后，底层内存才被释放。

支撑这一语义的是每个 `shared_ptr` 的内部布局，课件的示意图将其概括为"两个指针、一块控制块"：每个 `shared_ptr` 内部持有一个指向 `T` 对象本身的指针，以及一个指向 control block（控制块）的指针；控制块中保存 reference count（引用计数）、weak count，以及 custom deleter、allocator 等附加设施。据此可以推知其工作机制：复制 `shared_ptr` 时引用计数递增，每个副本析构时计数递减；当最后一个 `shared_ptr` 析构、计数归零时，底层对象才被释放。

因此 `shared_ptr` 的复制是安全的：任何时刻都存在明确的规则裁定"谁来释放"。这一安全性以额外代价换得——每个对象多出一个控制块与计数维护，所有权的语义也从"独占"放宽为"共享"。

## 13. 智能指针的初始化：make_unique 与 make_shared

三类指针最直接的初始化方式如下：

```cpp
std::unique_ptr<T> uniquePtr{new T};
std::shared_ptr<T> sharedPtr{new T};
std::weak_ptr<T> wp = sharedPtr;
```

前两行仍然显式调用了 `new`——按规则 R.11，这正是应当避免的写法，课件的批注是毫不掩饰的 "no....no"。标准做法是使用工厂函数：

```cpp
// std::unique_ptr<T> uniquePtr{new T};
std::unique_ptr<T> uniquePtr = std::make_unique<T>();

// std::shared_ptr<T> sharedPtr{new T};
std::shared_ptr<T> sharedPtr = std::make_shared<T>();

std::weak_ptr<T> wp = sharedPtr;
```

课件给出的准则是：**始终使用 `std::make_unique<T>` 与 `std::make_shared<T>`**；并且保持一致——若使用 `make_unique`，就也应使用 `make_shared`，而非两者混用。`weak_ptr` 则没有对应的 make 函数，它总是从已有的 `shared_ptr` 出发构造，这也与其"不拥有资源"的定位相符。

## 14. weak_ptr 与循环引用

`std::weak_ptr` 的定义是：一种可以观察由 `shared_ptr` 所拥有的对象、但不主张 ownership 的指针；它完全不影响引用计数。其设计目的在于缓解 circular dependency（循环依赖），避免内存泄漏。先看会出问题的写法：

```cpp
#include <iostream>
#include <memory>

class B;

class A {
  public:
    std::shared_ptr<B> ptr_to_b;
    ~A() {
      std::cout << "All of A's resources deallocated" << std::endl;
    }
};

class B {
  public:
    std::shared_ptr<A> ptr_to_a;
    ~B() {
      std::cout << "All of B's resources deallocated" << std::endl;
    }
};

int main() {
    std::shared_ptr<A> shared_ptr_to_a = std::make_shared<A>();
    std::shared_ptr<B> shared_ptr_to_b = std::make_shared<B>();
    shared_ptr_to_a->ptr_to_b = shared_ptr_to_b;
    shared_ptr_to_b->ptr_to_a = shared_ptr_to_a;
    return 0;
}
```

赋值完成后，A 的实例 a 与 B 的实例 b 通过 `shared_ptr` 互相持有，课件对此的概括是"两者都在保存指向对方的 shared pointer"。程序结束时分析引用计数：局部变量 `shared_ptr_to_a` 析构后，A 对象的计数由 2 降为 1——因为 b 的成员 `ptr_to_a` 仍持有它；而 b 自身要等 A 对象析构时才会随之析构。对称地，B 对象的计数同样停在 1。两个对象的计数都无法归零，两个析构函数都不会执行，课件给出的结论是"它们永远不会被正确释放"（they will never properly deallocate）：实例 a 与实例 b 互相等待，构成经典的双对象泄漏。

解决办法是让其中一个方向改用 `weak_ptr`。仅需修改 `class B` 的成员声明：

```cpp
class B {
  public:
    std::weak_ptr<A> ptr_to_a;  // 不再是 std::shared_ptr<A>
    ~B() {
        std::cout << "All of B's resources deallocated" << std::endl;
    }
};
```

（其余代码与上一例相同。）由于 `weak_ptr` 不参与引用计数，b 持有 a 不再抬升 A 对象的计数。作用域结束时，A 对象的计数顺利降为 0，a 被正常释放，其析构函数得以执行；a 的成员 `ptr_to_b` 随之析构，B 对象的计数降为 0，b 也得以释放。课件的解释即："这里 class B 不再以 `shared_ptr` 保存 a，因此不会增加 a 的引用计数；于是 a 可以被妥善释放（gracefully be deallocated），随之 b 也可以。"

## 15. 构建项目初步：从源代码到可执行文件

资源管理的议题到此告一段落，本讲转向工程层面的第二个问题：代码如何变成可运行的程序。C++ 源代码必须被翻译成计算机能够理解的形式才能执行，完成这一翻译的是编译器。整体流程为：source code（源代码）经 compiler（编译器）处理，产出 machine code（机器码）。以单个源文件为例，常用命令如下：

```bash
$ g++ main.cpp -o main    # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

逐项解读：`g++` 是编译器命令；`main.cpp` 是被编译的源文件；选项 `-o` 表示为最终的可执行文件指定一个名字，此处即 `main`；第二条命令 `./main` 实际运行编译得到的程序。

就应用背景而言，C++ 广泛分布于 GPU 编程（如 NVIDIA CUDA）、量化交易机构（如 Optiver、Citadel Securities、HRT）与自动驾驶（如 Tesla、Waymo）等领域。课件举出的代表性工程是 TensorFlow：其核心（Core）主要由 C++ 编写，由 2000 余个源文件组成。对这种规模的项目，逐个文件手工敲编译命令既不现实也不可靠——这正是 Linus Torvalds 那句 "Lol, that's a cute command" 所调侃的对象：区区一条 `g++ main.cpp` 命令，在真实工程面前只是玩具。管理编译过程需要专门的程序，即 build system（构建系统）。

## 16. make 与 Makefile

make 是一类构建系统（build system）程序，用于帮助完成编译。课件归纳其要点为：

- 项目中的文件无需再逐一手工编译；
- 可以指定使用哪个编译器；
- 使用 make 需要在项目中提供 Makefile；
- make 会跟踪自上次编译以来哪些文件发生了变化。

一个示例 Makefile（对应本课程第 8 讲的代码）如下：

```makefile
# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++20

# Source files and target
SRCS = $(wildcard *.cpp)
TARGET = main

# Default target
all:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

# Clean up
clean:
	rm -f $(TARGET)
```

结构解读：`CXX` 定义编译器变量；`CXXFLAGS` 定义编译选项，此处指定 C++20 标准；`SRCS` 借助 `$(wildcard *.cpp)` 以通配方式收集目录下所有 `.cpp` 文件；`TARGET` 为目标可执行文件名。默认目标 `all` 的规则将各变量组合成完整的编译命令，其配方行以缩进书写；`clean` 目标负责删除编译产物。执行 `make` 时默认构建 `all`，执行 `make clean` 时执行清理。

## 17. CMake 与 CMakeLists.txt

CMake 的定位是 build system generator（构建系统生成器）：用 CMake 生成 Makefile，相当于在 Makefile 之上提供一层更高阶的抽象。CMake 的配置写在项目根目录的 `CMakeLists.txt` 中：

```cmake
cmake_minimum_required(VERSION 3.10)

project(cs106l_classes)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SRC_FILES "*.cpp")

add_executable(main ${SRC_FILES})
```

逐行解读：`cmake_minimum_required(VERSION 3.10)` 声明所需的最低 CMake 版本；`project(cs106l_classes)` 为项目命名；`set(CMAKE_CXX_STANDARD 20)` 告知 CMake 采用 C++20 标准；`file(GLOB SRC_FILES "*.cpp")` 执行通配符搜索，收集所有匹配 `*.cpp` 的文件并存入变量 `SRC_FILES`；`add_executable(main ${SRC_FILES})` 将这些源文件加入可执行目标 `main`。

使用 CMake 的完整流程为：

1. 在项目根目录放置 `CMakeLists.txt`；
2. 在项目内建立构建目录（`mkdir build`）；
3. 进入该目录（`cd build`）；
4. 执行 `cmake ..`——该命令以项目根目录中的 `CMakeLists.txt` 为输入运行 cmake，并生成 `Makefile`；
5. 执行 `make` 进行编译；
6. 照常以 `./main` 运行程序。

构建文件由此集中生成于独立的 `build` 目录，源代码目录保持整洁。至此，从单条编译命令，到 make 与 Makefile，再到 CMake，构成一条逐层抽象的完整脉络。

## 本讲要点

- RAII（Resource Acquisition Is Initialization）要求类所使用的资源在构造函数中获取、在析构函数中释放；由于析构函数在对象离开作用域时必然执行，资源释放不受异常等复杂控制流影响，同时避免了半有效（half-valid）状态，且对象一经创建即可使用。
- 异常使控制流分析大为复杂：一个表面只有一两个分支的函数，把每条可能抛出异常的语句计入后，执行路径可达 23 条以上；手工配对的 `new`/`delete`、`open`/`close`、`lock`/`unlock` 在异常路径上必然失效，造成内存泄漏乃至死锁。
- 智能指针是内存的 RAII 封装：`std::unique_ptr` 独占资源且不可复制——复制在编译期即被禁止，从源头排除悬空指针与重复释放；`std::shared_ptr` 通过引用计数共享所有权，只有最后一个持有者离开作用域后底层内存才被释放。
- `std::weak_ptr` 观察 `shared_ptr` 所拥有的对象但不影响引用计数，用于打破两个对象经 `shared_ptr` 互相持有造成的循环引用，使双方都能正常析构。
- 智能指针应通过 `std::make_unique` 与 `std::make_shared` 初始化，避免显式调用 `new` 与 `delete`（C++ Core Guidelines R.11），并保持两者用法的一致性。
- 项目构建：单文件可用 `g++ main.cpp -o main` 编译并运行；规模化项目（如由 2000 余个源文件组成的 TensorFlow Core）应使用 make 与 Makefile 管理编译与增量更新，并可用 CMake 由 `CMakeLists.txt` 生成 Makefile。
