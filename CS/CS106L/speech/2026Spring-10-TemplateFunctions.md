---
title: "Lecture 10 · Template Functions 逐字稿"
createAt: 2026/9/13
---

# Lecture 10: Template Functions（逐字稿）

> 对应课件转写：[2026Spring-10-TemplateFunctions.md](../output/2026Spring-10-TemplateFunctions.md)

## 1. 复习：template class 与模板实例化（Slides 3–8）

在上一讲的基础上，本讲从两个回顾性问题出发。

**例题**：什么是 template class？为什么要使用 template class？

**解析**：template class 是"以泛型类型创建类的蓝图（blueprint）"，使用它的根本动机是消除代码冗余。若不使用模板，存储整数、浮点数与字符串的向量类需要分别定义 `IntVector`、`DoubleVector` 与 `StringVector`，三者的内部逻辑几乎完全一致，仅元素类型不同；引入模板后，一份定义即可覆盖全部情形：

```cpp
template <typename T>
class vector {
    // So satisfying.
};

vector<int> v1;
vector<double> v2;
vector<string> v3;
```

由此可提炼出贯穿本讲的核心观念（key idea）：**templates automate code generation**——模板把"生成代码"这一重复性劳动自动化了。其机制即上一讲讨论过的 template instantiation（模板实例化）。当写下

```cpp
template <typename T>
class Vector {
    T& at(size_t index);
    // More methods...
};

Vector<int> v;
```

编译器会据此生成等价于

```cpp
class IntVector {
    int& at(size_t index);
    // More methods...
};

IntVector v;
```

的代码：以 `int` 替换 `T`，产出一个可直接使用的类。

模板的能力并不止于类。本讲（Lecture 10: Template Functions，CS106L Spring 2026，Preston Seay 与 Rachel Fernandez 主讲）讨论如何将模板推广到函数。

## 2. 本讲议程（Slides 9–11）

本讲分为四个部分：

1. **Template Functions**：如何将 template class 推广为 function template；
2. **Concepts**：如何为模板声明约束，使 C++ 模板的错误信息恢复可读性；
3. **Variadic Templates**：如何构造接受可变数量参数的函数；
4. **Template Metaprogramming**：如何在编译期执行计算。

课件注明本讲容量较大，全部内容未必一次讲完。

## 3. 从 min 函数到第一个 function template（Slides 13–25）

以一个具体需求为起点：在 C++ 中求两个值中较小者。最直接的实现只支持 `int`：

```cpp
// Returns the smaller of a and b
int min(int a, int b) {
    return a < b ? a : b;
}
```

函数体使用了 ternary operator（条件运算符）：`a < b ? a : b` 在 `a < b` 成立时取 `a`，否则取 `b`。然而 min 的语义并不限于整数：

```cpp
min(106, 107);            // int, returns 106
min(1.2, 3.4);            // double, returns 1.2
min("Preston", "Rachel"); // string, returns "Preston"
```

两个字符串求 min，即返回字典序靠前者：`"Preston"` 排在 `"Rachel"` 之前，故返回 `"Preston"`。要让一个 `min` 同时服务多种类型，最直接的对策是 function overloading（函数重载），为每种类型各写一份：

```cpp
int min(int a, int b) {
    return a < b ? a : b;
}

double min(double a, double b) {
    return a < b ? a : b;
}

std::string min(std::string a, std::string b) {
    return a < b ? a : b;
}
```

三个函数体完全相同，仅参数与返回类型不同——这与上一讲 `IntVector`、`DoubleVector`、`StringVector` 三份类定义的冗余如出一辙。课件对此方案的评价是：它可行，"but it's missing the bigger idea"。沿用类模板的思路，可将三份重载合并为一个 function template（函数模板）：

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}
```

此处有两点必须强调。其一，这段代码整体是一个 template；其二，`T` 是类型占位符，随后会被替换为某个具体类型。课件以工厂（factory）作比：向模板"喂入"类型 `int`，即产出函数 `min<int>`；喂入 `string`，产出 `min<string>`；模板定义本身相当于这台机器的生产图纸。

一个必须严格区分的概念：**template 不是 function**。`template <typename T> T min(T a, T b)` 是模板而非函数，无法被直接调用；`min<std::string>` 才是函数，亦称 template instantiation（模板实例）。

与普通函数一样，模板函数的传参方式也可优化。按值传递会拷贝实参，改用 const 引用即可避免拷贝：

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

## 4. 调用模板函数：explicit 与 implicit instantiation（Slides 26–39）

调用 function template 有两种方式。

**方式一：explicit instantiation（显式实例化）。** 与 template class 相同，将类型直接写入尖括号：

```cpp
min<int>(106, 107);        // Returns 106
min<double>(1.2, 3.4);     // Returns 1.2
```

每一次显式实例化都在促使编译器替使用者生成代码。课件将这一过程展示为：

```cpp
int min(int a, int b) {                // Compiler generated
    return a < b ? a : b;              // Compiler generated
}                                      // Compiler generated

double min(double a, double b) {       // Compiler generated
    return a < b ? a : b;              // Compiler generated
}                                      // Compiler generated

min<int>(106, 107);                    // Returns 106
min<double>(1.2, 3.4);                 // Returns 1.2
```

原先需要手工撰写的重载版本，如今全部由编译器生成。这正是第 1 节所述 key idea 的再次体现：templates automate code generation。

**方式二：implicit instantiation（隐式实例化）。** 省略尖括号，由编译器推断（infer）类型：

```cpp
min(106, 107);     // int, returns 106
min(1.2, 3.4);     // double, returns 1.2
```

两次调用均未指定模板类型，编译器根据实参完成 template argument deduction（模板实参推导）：`106` 为 `int`，故实例化 `min<int>`。这一机制与 auto 颇为类似：

```cpp
auto number = 106;
```

`number` 的类型仍然是 `int`，只是类型名由编译器代写。同理，

```cpp
int m = min(106, 107);
```

的效果与书写 `min<int>(106, 107)` 完全等价。

隐式实例化在若干场景下较为挑剔（finicky）。

**场景一：字符串字面量。**

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}

min("Preston", "Rachel");
```

**例题**：此处 `T` 被推导为什么类型？

**解析**：字符串字面量的类型并非 `std::string`，而是 `const char*`（指向字符数组的指针）。编译器据此生成：

```cpp
const char* min(const char* a, const char* b) {
    return a < b ? a : b;
}

min<const char*>("Preston", "Rachel");
```

于是 `a < b` 比较的是两个指针的地址值，而非字符串内容。这种 pointer comparison（指针比较）与"按字典序取较小字符串"的意图完全相悖，并非预期行为。

对策：在存在歧义的情形下，总能退回显式实例化：

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}

min<std::string>("Preston", "Rachel");
```

指定 `T = std::string` 后，两个 `const char*` 实参在传参时被转换为 `std::string`，`<` 随之执行字符串的字典序比较。

**场景二：两个实参的类型不一致。**

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}

min(106, 3.14);      // Doesn't compile
```

`106` 的类型是 `int`，`3.14` 的类型是 `double`，而模板参数只有一个 `T`：它无法同时等于两个类型，推导失败，代码不能编译。最快的处理仍是显式实例化：写作 `min<double>(106, 3.14)`，令 `106` 隐式转换为 `double`。

另一种做法是提高模板自身的灵活度，引入两个类型参数：

```cpp
template <typename T, typename U>
????? min(const T& a, const U& b) {
    return a < b ? a : b;
}

min(106, 3.14);
```

此时推导结果为 `T = int`、`U = double`，参数类型的匹配问题不复存在；但新的问题随之出现：返回类型应当写 `T` 还是 `U`？这一问题的完整答案相当繁复，通行做法是把返回类型交给编译器，以 auto 声明：

```cpp
template <typename T, typename U>
auto min(const T& a, const U& b) {
    return a < b ? a : b;
}
```

本节最后附一条工程实践建议：IDE（如 VSCode、QtCreator）能够直接显示实例化所得的真实类型。对下列代码

```cpp
template <typename T>
T min(T a, T b)
{
  return a < b ? a : b;
}

int main()
{
  auto m = min("Jacob", "Fabio");
}
```

中的调用悬停查看，VSCode 给出的完整签名为 `const char *min<const char *>(const char *a, const char *b)`，据此即可确认编译器将 `T` 定为 `const char*`。调试模板代码时，这一功能十分有效。

## 5. 应用：模板化的 find 函数（Slides 41–53）

在实践中，function template 的应用无处不在，最具代表性的例子是 iterators（迭代器）。此前学过的每种容器都有各自的 iterator 类型，且底层结构差异极大：`vector<T>::iterator` 建立在一整段连续内存之上；`deque<T>::iterator` 对应分段存储的内存块；`map<K, V>::iterator` 遍历平衡二叉搜索树；`unordered_map<K, V>::iterator` 则在哈希桶数组中移动。尽管结构迥异，这些 iterator 都支持同一组操作：`*it` 解引用、`++it` 前进、`!=` 比较。这一共性正是泛型化的立足点。

考察 find 函数的设计。预期用法如下：

```cpp
std::vector<int> v { 106, 111, 42, 112 };
auto it = find(v.begin(), v.end(), 42);
*it = 107;
// v = { 106, 111, 107, 112 }
```

find 接收首迭代器、尾迭代器与目标值，返回指向 `42` 的迭代器（`42` 位于下标 2）；随后经由 `*it` 将该元素改写为 `107`。按照这一用法可直接写出第一版实现：

```cpp
std::vector<int>::iterator find(
    std::vector<int>::iterator begin,
    std::vector<int>::iterator end,
    int value
) {
    // Logic to find the iterator in this container
    // Should return end if no such element is found
}
```

逻辑本身并不复杂：自首迭代器起线性扫描，遇到相等元素即返回其迭代器，扫描至末尾仍未命中则返回 end。问题在于签名：参数与返回类型被写死为 `std::vector<int>::iterator`，定义过于具体（too specific）。该函数既不能服务于其他元素类型的 vector，也不能服务于其他容器：

```cpp
std::vector<std::string> v { "seven", "kingdoms" };
auto it = find(v.begin(), v.end(), "kingdoms");
// Won't compile

std::set<std::string> s { "house", "targaryen" };
auto it = find(s.begin(), s.end(), "targaryen");
// oh man D:
```

前一调用无法通过编译，后一调用更是无从谈起。解决途径与前文一致——将其改写为模板函数。先列出模板骨架：

```cpp
template <typename Iterator, typename TElem>
???? find(???? begin, ???? end, ???? value) {
    // Logic to find and return the iterator
    // in this container whose element is value
    // Should return end if no such element is found
}

find<std::vector<int>::iterator, int>(b, e, 42);
```

待定的类型均可由模板参数承担：

```cpp
template <typename Iterator, typename TElem>
Iterator find(Iterator begin, Iterator end, TElem value) {
    // Logic to find and return the iterator
    // in this container whose element is value
    // Should return end if no such element is found
}

find<std::vector<int>::iterator, int>(b, e, 42);
```

`Iterator` 表示迭代器类型，`TElem` 表示元素类型，返回类型同为 `Iterator`。补全实现，即得一个朴素而通用的线性扫描：

```cpp
template <typename Iterator, typename TElem>
Iterator find(Iterator begin, Iterator end, TElem value) {
    Iterator it = begin;
    while (it != end) {
        if (*it == value) break;
        ++it;
    }
    return it;
}

find<std::vector<int>::iterator, int>(b, e, 42);
```

自 `begin` 出发，只要未达 `end` 便 `++it` 前进；途中 `*it` 等于 `value` 即中断循环；最终返回的 `it` 要么指向命中元素，要么恰为 `end`。十余行代码即可覆盖任意容器与任意元素类型。

标准库提供了同一功能的正式版本。`std::find` 以及 `std::find_if`、`std::find_if_not` 定义于 `<algorithm>` 头文件，C++ standard 中的签名为：

```cpp
std::find, std::find_if, std::find_if_not

Defined in header <algorithm>

template< class InputIt, class T >
InputIt find( InputIt first, InputIt last, const T& value );
```

其结构与上文自制的模板版本几乎一致，仅参数名为 `first` 与 `last`。至此，读者已经具备直接阅读 C++ standard 相关条目的全部工具；`<algorithm>` 的更多内容将在下一次课展开。

## 6. 模板的延迟错误检测（Slides 55–67）

模板的错误报告问题，是引入 concepts 的直接动因。仍以 min 为例：

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

**例题**：对哪些类型 `T`，下列代码能够通过编译？

```cpp
T a = /* an instance of T */;
T b = /* an instance of T */;
min<T>(a, b);
```

**解析**：函数体中出现了表达式 `a < b`，故 `T` 必须提供 operator<，否则该表达式无法通过编译。换言之，min 对类型 `T` 存在隐性要求。反例：

```cpp
struct StanfordID; // How do we compare two IDs?

StanfordID preston { "Preston", "pseay" };
StanfordID rachel { "Rachel", "rfern" };
min<StanfordID>(preston, rachel); // Compiler error
```

`StanfordID` 是自定义结构体，语言并未为其定义两个实例之间的大小关系，实例化因此失败。编译器输出如下：

```text
$ g++ main.cpp --std=c++20
main.cpp:9:12: error: invalid operands to binary expression
('const StanfordID' and 'const StanfordID')
return a < b ? a : b;
       ~ ^ ~
main.cpp:20:3: note: in instantiation of function template specialization
'min<StanfordID>' requested here
min<StanfordID>(preston, rachel);
^
1 error generated.
```

这份输出值得逐条解读。error 行指出：二元表达式 `a < b` 的两个操作数 `const StanfordID` 之间不存在合法的 `<` 运算；note 行说明错误的来源——调用处请求实例化 function template specialization `'min<StanfordID>'`（此处 specialization 即 `min` 针对 `StanfordID` 的实例）。错误的发生顺序是本节的关键：编译器先将模板实例化为

```cpp
StanfordID min(const StanfordID& a, const StanfordID& b)
{
    return a < b ? a : b;
}
```

然后在编译该函数体时才在 `a < b` 处失败。模板定义本身在定义处并不报错：`a < b` 这样的 dependent name（依赖名，即语义上依赖模板参数的表达式）要等到实例化阶段才接受完整检查。这正是 C++ 模板 two-phase lookup（两阶段查找）模型的直接后果——定义阶段只检查不依赖模板参数的部分，依赖部分推迟到实例化。课件将此现象概括为 **Delayed Error Detection in Templates**：编译器只在实例化之后才发现错误。

这一问题并非 min 独有。前文曾提及 `std::set` 同样要求元素类型提供 operator<，那么 `std::set<StanfordID> s { preston, rachel };` 会如何？错误信息长达数屏：error 发生在标准库内部——`std::less<StanfordID>::operator()` 中的 `{return __x < __y;}`——其后是层层嵌套的 `in instantiation of ...` 说明，涉及 `std::__tree<StanfordID, std::less<StanfordID>, std::allocator<StanfordID>>` 等内部实现符号。使用者的真实意图只是"StanfordID 缺少小于运算符"，报告形式却是一场标准库内部实现的长篇展示。设计不良（缺少约束）的模板所产生错误信息的可读性，由此可见一斑。

find 亦然：

```cpp
int main() {
    int idx = find(1, 5, 3);
}
```

使用者将两个 `int` 当作迭代器传入，编译器报告：

```text
main.cpp:16:9: error: indirection requires pointer operand ('int' invalid)
    if (*it == value) {
        ^~~
main.cpp:29:3: note: in instantiation of function template specialization 'find<int, int>'
  find(1, 5, 3);
        ^
1 error generated.
```

"indirection requires pointer operand"（解引用要求指针操作数）这一表述并不直观：真正的病因是 `int` 根本不是迭代器类型，初学者难以从该信息定位问题。

于是引出本部分的核心问题：**如何为模板声明约束（constraints）？** 模板本身很有价值，但误用时产生的错误信息缺乏直观性；理想情形是把"对模板类型的要求"在定义处提前声明。其他现代语言已有先例。C# 允许写作：

```csharp
class EmployeeList<T>
where T : notnull, Employee, IComparable<T>, new()
```

Java 允许写作：

```java
class ListObject<T extends Comparable<T>>
```

两者都在类型参数上直接声明约束。对 C++ 的期望行为是：**约束未全部满足时，编译器不应实例化模板**。具体到本讲的两个函数：min 应声明"`T` 必须支持 operator<"；find 应声明"`It` 必须是 iterator 类型"：

```cpp
template <typename T>
T min(const T& a, const T& b)

template <typename T>
struct set;

template <typename It, typename T>
It find(It begin, It end, const T& value)
```

若这些要求能够书写于模板定义处，上述种种报错即可在源头被拦截。C++ 给出的答案即 concepts。

## 7. C++20 Concepts（Slides 68–81）

concept（概念）是 C++20 引入的语言特性。先手工构造一个名为 Comparable 的 concept：

```cpp
template <typename T>
concept Comparable = requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};
```

这段代码包含四个语法要素：

1. **concept**：一个命名的约束集合（a named set of constraints）；`template <typename T>` 声明该概念针对类型 `T` 定义。
2. **requires**：`requires(const T a, const T b)` 的含义是"给定两个 `T` 类型的对象，下列断言应当成立"。
3. **constraint（约束）**：花括号内的 `{ a < b }` 必须能够无错通过编译。
4. **返回类型约束**：`-> std::convertible_to<bool>` 要求表达式的结果必须是 bool 类似（bool-like）的类型。此处 `convertible_to` 本身也是一个 concept——concept 可以引用其他 concept，从而逐层组合。

使用该 concept 的标准写法，是在模板参数列表之后附加 requires 子句：

```cpp
template <typename T> requires Comparable<T>
T min(const T& a, const T& b);
```

C++20 同时提供等价的简写形式：

```cpp
// Super slick shorthand for the above
template <Comparable T>
T min(const T& a, const T& b);
```

即直接以 concept 名占据 `typename` 的位置，语义与 requires 子句版本完全相同。

concept 对错误信息的改善可以直观对比。回顾第 6 节中 `std::set<StanfordID>` 在无 concept 约束下的错误输出（课件在此处原样重放了那一整屏 `__tree` 内部符号的报告），随后为 set 的声明加上约束——`template <Comparable T> struct std::set;`——同样的错误变为：

```text
main.cpp:32:3: error: constraints not satisfied for class template 'set' [with T = StanfordID]
    set<StanfordID> ids { jacob, fabio };
    ^~~~~~~~~~~~~~~~~~~~~
main.cpp:13:11: note: because 'StanfordID' does not satisfy 'Comparable'
template <Comparable T>
                   ^
main.cpp:10:7: note: because 'a < b' would be invalid: invalid operands to binary expression ('const StanfordID' and 'const StanfordID')
    { a < b } -> std::convertible_to<bool>;
            ^
4 errors generated.
```

输出是一条清晰的因果链："约束未满足，因为 `StanfordID` 不满足 `Comparable`，因为 `a < b` 非法"。编译器不再转述标准库的内部细节，而是将病灶直接定位于使用者的代码。这也与第 6 节所期望的行为一致：约束不满足，实例化根本不会发生，错误在实例化之前即被拦截。

C++ 标准库在 `<concepts>` 头文件中预置了大量 concept，常用的包括：

| Concept | 含义 |
| :--- | :--- |
| `same_as` | 类型与另一类型相同 |
| `derived_from` | 类型派生自另一类型 |
| `convertible_to` | 类型可隐式转换为另一类型 |
| `common_reference_with` / `common_with` | 两类型共享公共引用类型 / 公共类型 |
| `integral` / `signed_integral` / `unsigned_integral` | 整型 / 有符号整型 / 无符号整型 |
| `floating_point` | 浮点型 |
| `assignable_from` | 可从另一类型赋值 |
| `swappable` / `swappable_with` | 可交换 / 可与另一类型交换 |

内置 concept 中还包括一整个 iterator concepts 家族：`input_iterator`（所引用的值可读，且支持前置与后置自增）、`output_iterator`（可向其写入给定值类型的值）、`forward_iterator`（在 input_iterator 之上支持相等比较与多遍扫描）、`bidirectional_iterator`（进一步支持反向移动）、`random_access_iterator`（支持常数时间前进与下标访问）、`contiguous_iterator`（所指元素在内存中连续）。这些概念构成逐层嵌套的层级：后者以前者为前提，第 5 节列举的各种容器迭代器正对应这一层级中的不同位置。

运用 `input_iterator` 即可修正 find 的约束缺失：

```cpp
template <std::input_iterator It, typename T>
It find(It begin, It end, const T& value);

int idx = find(1, 5, 3); // WHY DOES THIS NOT WORK?
```

此时 `find(1, 5, 3)` 的报告不再是含混的解引用错误，而是：

```text
main.cpp:10:11: note: because 'int' does not satisfy 'input_iterator'
template <std::input_iterator It, typename T>
          ^
```

"`int` 不满足 `input_iterator`"，一句话指明病因。

对本节归纳有二。其一，使用 concept 的两点收益：更好的编译错误信息，以及更好的 IDE 支持（Intellisense、自动补全等）。其二，concept 仍是较新的特性，STL 尚未全面采用；这一话题将在下一次课继续。

## 8. 可变数量参数：从重载到 vector 递归（Slides 83–99）

本部分处理一个新的需求：如何创建接受可变数量（variable number）参数的函数。

仍以 min 为例。目前的版本恰好接受两个参数：

```cpp
template <Comparable T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

而下列调用同样是合理的语义需求：

```cpp
min(2.4, 7.5);            // This works
min(2.4, 7.5, 5.3);       // What about this?
min(2.4, 7.5, 5.3, 1.2);  // or this?
```

直接的对策仍是重载，且各重载之间存在规律：

```cpp
template <Comparable T>
T min(const T& a, const T& b) { return a < b ? a : b; }

template <Comparable T>
T min(const T& a, const T& b, const T& c) {
    auto m = min(b, c);
    return a < m ? a : m;
}

template <Comparable T>
T min(const T& a, const T& b, const T& c, const T& d) {
    auto m = min(b, c, d);
    return a < m ? a : m;
}
```

三参数版本先对 `b`、`c` 求最小值，再与 `a` 比较；四参数版本调用三参数版本。课件的批注一语中的："Seems almost recursive!"——这组重载几乎是递归的。然而重载方案存在规模问题：

```cpp
min(2.4, 7.5); // This works
min(2.4, 7.5, 5.3); // This works now
min(2.4, 7.5, 5.3, 1.2); // and this works too!
min(2.4, 7.5, 5.3, 1.2, 3.4, 6.7, 8.9, 9.1);
// Time to write 7 overloads I guess...
```

八个参数的调用意味着继续手写七个重载，方案不具备可扩展性。

此处的关键观察回到了本讲的 key idea：templates 的本质是 code generation。既然各重载彼此高度相似、仅参数个数不同，就应当可以令编译器代为生成——答案确实可行，配方是 templates 与递归的结合。在引入正式方案之前，课件先给出一个过渡性设计：不直接传多个参数，而是传入一个 `std::vector<T>`：

```cpp
template <Comparable T>
T min(const std::vector<T>& values);

// Passing a vector<double> here!
// Note the { } braces (uniform initialized vector)
min({ 2.4, 7.5 });
min({ 2.4, 7.5, 5.3 });
min({ 2.4, 7.5, 5.3, 1.2 });
```

调用处的花括号触发 uniform initialization，就地构造出 `vector<double>`。实现采用递归：

```cpp
template <Comparable T>
T min(const std::vector<T>& values) {
    if (values.size() == 1) return values[0];
    const auto& first = values[0];
    std::vector<T> rest(++values.begin(), values.end());
    auto m = min(rest);
    return first < m ? first : m;
}
```

这是一个标准的递归设计。Base case：向量仅剩一个元素时直接返回该元素；recursive case：取首元素 `first`，将余下部分（自 `++values.begin()` 至 `end()`）拷贝为新向量 `rest`，对 `rest` 递归求最小值 `m`，返回 `first` 与 `m` 中较小者。该实现是正确的，但存在两处低效：

* 递归过程中反复拷贝 vector——这一项原则上可以通过包装函数（wrapper function）规避；
* 每层递归都必须分配一个新 vector——这一开销是该方案固有的。

而期望中的使用体验仍是直接罗列参数：

```cpp
min(2.4, 7.5);              // This works
min(2.4, 7.5, 5.3);         // This works now
min(2.4, 7.5, 5.3, 1.2);    // and this works too!

// This just works!
min(2.4, 7.5, 5.3, 1.2, 3.4, 6.7, 8.9, 9.1);
```

线索至此齐备：重载序列"几乎是递归的"，而 templates 擅长的正是自动生成代码。

## 9. Variadic Templates：parameter pack 与 pack expansion（Slides 100–107）

variadic templates（可变参数模板）由两个函数模板构成：

```cpp
template <Comparable T>
T min(const T& v) { return v; }

template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

其中涉及四个术语。

第一，单参数的 `min` 是 base case function（递归基函数），其职责是使递归终止：参数只剩一个时直接返回。

第二，第二个模板的参数列表中的 `Comparable... Args` 使之成为 variadic template：`Args` 带省略号，可匹配 0 个或更多个类型，且每个类型都须满足 Comparable。

第三，函数参数 `const Args&... args` 中的 `args` 称为 parameter pack（参数包），对应 0 个或更多个函数参数；类型包 `Args...` 与值包 `args` 一一对应。

第四，函数体中的 `min(args...)` 体现了 pack expansion（包展开）：编译器将 `args` 就地展开为它所捕获的实际参数序列，以逗号分隔。

## 10. 逐步实例化：min(2, 7, 5, 1)（Slides 109–123）

现将实例化过程逐步还原。设有两个模板：

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)

template <Comparable T>
T min(const T& v) { return v; }
```

并发出调用：

```cpp
min(2, 7, 5, 1)
```

编译器对该调用执行 implicit instantiation：对于 `min<int, int, int, int>(2, 7, 5, 1)`，推导结果为

```text
T = int
Args = [int, int, int]
```

分配规则值得注意：第一个实参 `2` 对应 `T`，其余三个实参 `7, 5, 1` 整体装入参数包 `Args`。编译器据此实例化 variadic 版本，先将 `T` 替换为 `int`，参数包暂保持原状：

```cpp
template <Comparable... Args>
int min(const int& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

随后执行 pack expansion，将 `Args` 逐个展开：

```cpp
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(a0, a1, a2);
    return v < m ? v : m;
}
```

一个四参数函数由此生成——编译器替使用者写出了一个重载，而使用者并未亲手撰写任何重载。

过程并未到此为止。函数体中的 `min(a0, a1, a2)` 本身又是一次模板实例化：推导得 `T = int`、`Args = [int, int]`，生成

```cpp
int min(const int& v, const int& a0, const int& a1) {
    auto m = min(a0, a1);
    return v < m ? v : m;
}
```

其函数体中的 `min(a0, a1)` 再触发一次实例化：`T = int`、`Args = [int]`，生成

```cpp
int min(const int& v, const int& a0) {
    auto m = min(a0);
    return v < m ? v : m;
}
```

最后，`min(a0)` 只有一个实参。此时两个模板均可匹配：variadic 版本可取 `T = int`、`Args = []`（空包），单参数版本可取 `T = int`。编译器的裁决规则是：**compiler always tries to choose most specific template**——在 overload resolution（重载解析）中总是倾向选择更具体的模板。单参数模板对当前调用的刻画更精确，故被选中，实例化为：

```cpp
int min(const int& v) {
    return v;
}
```

递归至此收敛。清点一次 `min(2, 7, 5, 1)` 触发的全部生成物：

```cpp
min(2, 7, 5, 1);

min<int, int, int, int> // T = int, Args = [int, int, int]
min<int, int, int>      // T = int, Args = [int, int]
min<int, int>           // T = int, Args = [int]
min<int>                // T = int
```

编译器沿递归链生成了四参数、三参数、二参数的函数，最终落于单参数 base case，共四个实例；而源代码中只存在两个模板定义。variadic templates 的机制正在于此：以递归结构描述一族函数，由编译器将它们全部生成。

## 11. 异构参数：实现 format（Slides 125–130）

上一节的例子中所有实参同为 `int`，但 variadic templates 对参数类型并无齐次性要求。考虑 printf 风格的函数 `format("Queen {}, Protector of the {} Kingdoms", "Rhaenyra", 7);`，其中每个 `{}` 占位符由后续任意数量、任意类型的实参填充。仿照 Python f-string 设计一个格式化打印函数，预期行为如下：

```cpp
format("Queen {}, Protector of the {} Kingdoms", "Rhaenyra", 7);
// Prints: Queen Rhaenyra, Protector of the 7 Kingdoms

std::cout << std::boolalpha;
format("The {} enemy won't {} out the {}", true, "wait", "storm");
// Prints: The true enemy won't wait out the storm

format("Winter is coming");
// Prints: Winter is coming
```

实参类型是异构的：第一例中 `"Rhaenyra"` 为 `std::string`、`7` 为 `int`；第二例中 `true` 为 `bool`，`"wait"` 与 `"storm"` 为字符串。第 8 节的 vector 方案在此失效：

```cpp
template <typename T>
void format(const std::string& fmt, std::vector<T> args) {
    // ...
}

format("{} {}", { true, "facts" });
// No common type for vector
```

`bool` 与字符串字面量不存在公共类型，`std::vector<T>` 的 `T` 无从确定；vector 方案仅当所有实参类型相同时可行，而 variadic templates 天然支持异构参数。实现如下：

```cpp
void format(const std::string& fmt) {
    std::cout << fmt << std::endl;
}

template <typename T, typename... Args>
void format(const std::string& fmt, T value, Args... args) {
    auto pos = fmt.find("{}");
    if (pos == std::string::npos) throw std::runtime_error("Extra arg");
    std::cout << fmt.substr(0, pos);
    std::cout << value;
    format(fmt.substr(pos + 2), args...);
}
```

第一个重载是非模板的普通函数，充当 base case：格式串中已无实参可填，直接输出剩余的 `fmt` 并换行结束。第二个是模板函数：在格式串中查找首个 `"{}"` 的位置 `pos`；若找不到而仍有实参未消费，说明实参多于占位符，抛出 `std::runtime_error("Extra arg")`；否则依次输出 `"{}"` 之前的子串与 `value`，再将格式串截断为自 `pos + 2` 起的后缀，携带余下的 `args...` 递归调用自身。每轮递归恰好消费一个占位符与一个实参，两条"消耗链"始终保持对齐。

课件以简写形式列出了实例化链。对于

```cpp
format("Lecture {}: {} (Week {})", 9, "Templates", 5);
```

递归链为：

```cpp
format<int, std::string, int>()
// T = int, Args = [std::string, int]

format<std::string, int>()
// T = std::string, Args = [int]

format<int>()
// T = int, Args = []

format()
// Base case! Not a template, no type arguments
```

对此简写需作两点说明。其一，每行尖括号内列出的是该次调用的完整模板实参表：第一个实参绑定 `T`，其余构成参数包 `Args`；行内的圆括号省略了函数实参，仅标示递归链上的一次调用。其二，`format<int>()` 表示以 `T = int`、`Args = []`（空包）实例化模板——该次调用仍匹配模板；输出 `value` 后以空包继续递归，最终落到最后一行的非模板 base case 上：它不是模板，因而不存在任何类型实参。

本节归纳有二：编译器借助递归生成任意数量的重载，从而支持任意数量的函数参数；这一切实例化均发生于编译期（compile time）。后者引出最后一个问题——模板既然本来就在编译期做功，能否有意识地利用这一点？

## 12. Template Metaprogramming：编译期计算（Slides 131–137）

Template Metaprogramming（模板元编程，简称 TMP）回答的核心问题是：如何将计算工作移至 compile time 完成。教科书式的例子是编译期阶乘：

```cpp
template <>
struct Factorial<0> {
    enum { value = 1 };
};

template <size_t N>
struct Factorial {
    enum { value = N * Factorial<N - 1>::value };
};

std::cout << Factorial<7>::value << std::endl;
```

代码中有三个新语法。其一，`template <> struct Factorial<0>` 是 template specialization（模板特化）：针对 `N = 0` 这一特定值给出专门定义，充当整棵递归的 base case。其二，`enum { value = ... }` 是在类型内部保存编译期常量的一种方式：匿名枚举成员的值在编译期即可确定。其三，通用版本中的 `N * Factorial<N - 1>::value` 构成编译期递归：实例化 `Factorial<N>` 会连带要求实例化 `Factorial<N - 1>`，逐层下探，直至命中特化 `Factorial<0>`。

输出结果为 **5040**，即 7 的阶乘；关键在于该值并非运行期算得，而是编译期完成。课件将 `Factorial<7>` 的实例化链绘为：`Factorial<7>`、`Factorial<6>`、……、`Factorial<0>` 依次展开，各层分别得出 `value = 5040, 720, 120, 24, 6, 2, 1, 1`，先顺次下探，再回溯相乘——全部发生于编译期。

编译产物可为此提供直接证据。源代码

```cpp
int main() {
    std::cout << Factorial<7>::value;
    return 0;
}
```

对应的 x86-64 汇编为：

```asm
main:
    push rax
    mov edi, offset cout
    mov esi, 5040
    call ostream::operator<<(int)
    xor eax, eax
    pop rcx
    ret
```

指令 `mov esi, 5040` 表明结果 5040 已作为立即数烘焙（baked in）进可执行文件：程序运行时不再执行任何一次乘法，编译期的全部计算成果固化于二进制之中。

同一套路可推广至 Fibonacci，区别仅在于需要两个特化充当 base case，且递推式为前两项相加：

```cpp
template <>
struct Fibonacci<0> {
    enum { value = 0 };
};

template <>
struct Fibonacci<1> {
    enum { value = 1 };
};

template <size_t N>
struct Fibonacci {
    enum { value = Fibonacci<N - 1>::value + Fibonacci<N - 2>::value };
};
```

## 13. TMP 的现实应用与 constexpr/consteval（Slides 138–146）

TMP 在工程实践中的用途包括：将计算结果在编译期烘焙进可执行文件（如上节的 factorial）；优化矩阵、树等数学结构上的运算；policy-based design（策略化设计），即经由模板参数传递行为策略；以及著名的 Boost MPL 库。

boost::mpl 是"面向类型编程"的代表：

```cpp
using namespace boost;

using Move = mpl::vector<MoveUp, MoveRight>;
using MoveRotate = mpl::push_back<Move, Rotate45>::type;

template <typename Transformations>
void apply(Object&);

apply<Move>(object); // move object up and right
apply<MoveRotate>(object); // move object up/right, rotate 45deg
```

`mpl::vector<MoveUp, MoveRight>` 是一个装"类型"的 vector（课件强调：This is a vector of TYPES!!!），并可对其执行 `push_back`，将 `Rotate45` 追加得到 `MoveRotate`。`apply<Move>(object)` 使对象上移并向右移动，`apply<MoveRotate>(object)` 在移动之外附加 45 度旋转——编译器会针对这组类型组合生成专属代码。

更进一步，TMP 是 Turing complete（图灵完备）的：其理论计算能力等价于通用计算机。换言之，可以在编译期执行任意代码（arbitrary code）。

能力的另一面是语法代价。Boost MPL 库内部的实现形如：

```cpp
template< >
struct push_back_impl< aux::vector_tag<BOOST_PP_DEC(i_)> >
{
    template< typename Vector, typename T > struct apply
    {
        typedef BOOST_PP_CAT(vector,i_)<
            BOOST_PP_ENUM_PARAMS(BOOST_PP_DEC(i_), typename Vector::item)
            BOOST_PP_COMMA_IF(BOOST_PP_DEC(i_))
            T
            > type;
    };
};
```

`BOOST_PP_DEC`、`BOOST_PP_CAT`、`BOOST_PP_ENUM_PARAMS` 等宏拼接出的代码，可读性已几近于零。

于是产生如下诉求：能否兼得编译期执行与代码可读性？现代 C++ 给出了肯定答案。上节 struct 嵌套、enum 藏常量的写法，可由一对关键字取代——constexpr 与 consteval。课件将这一演进称为模板元编程的制度化（institutionalization），并标注其为 C++20 的新特性。先看 constexpr：

```cpp
constexpr size_t factorial(size_t n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```

这就是一个普通的递归函数，任何读者都能读懂。constexpr 的语义可概括为：告知编译器，请尽量在编译期运行此函数——当调用处要求编译期常量时，计算即于编译期完成。consteval 则更为严格：

```cpp
consteval size_t factorial(size_t n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```

其语义是：必须在编译期运行，运行期调用直接构成错误。从手写模板递归到一行关键字，这是 C++ 在编译期计算方向上演进的缩影。

## 14. 总结（Slides 148–150）

本讲以"何时应当使用模板"作结，三种动机对应三组工具：

* 希望编译器自动化某项重复性的编码任务——template functions 与 variadic templates；
* 希望获得更好的错误信息——concepts；
* 希望计算不必等到运行期——template metaprogramming，以及更现代的 constexpr / consteval。

下一次课的主题为 Functions and Algorithms：编写更聪明、更灵活的算法；`<algorithm>` 与 concepts 的未尽话题亦将在彼处继续。

## 本讲要点

- template 与 function 层级不同：`template <typename T> T min(T a, T b)` 是模板而非函数，`min<std::string>` 这类 template instantiation 才是可调用的函数；模板的定位是让编译器自动生成代码（templates automate code generation）。
- 调用方式有 explicit instantiation（`min<int>(106, 107)`）与 implicit instantiation（`min(106, 107)`，机制类似 auto）两种；template argument deduction 在字符串字面量（推导为 `const char*` 导致指针比较）与混合类型（`min(106, 3.14)` 无法编译）等场景会失效，可分别以显式指定、双类型参数加 `auto` 返回值化解。
- 模板错误是延迟检测的：`a < b` 这类 dependent name 在 two-phase lookup 模型下推迟到实例化阶段才接受检查，故编译器先实例化、后报错，无约束时错误信息可绵延数屏；C++20 concept（`concept Comparable = requires(...) { { a < b } -> std::convertible_to<bool>; }`）将约束前置，约束不满足即拒绝实例化，并给出"因为……不满足……"式的可读报告，同时改善 IDE 支持。
- variadic templates 以 base case function、parameter pack（`Args...`/`args`）与 pack expansion（`args...`）为三件套，令编译器沿递归生成任意数量、任意类型参数的函数：一次 `min(2, 7, 5, 1)` 即生成四个实例；多个模板均可匹配时，overload resolution 选择 most specific template。
- 编译期计算是模板的固有能力：TMP 借 specialization 与 enum 常量实现编译期递归（`Factorial<7>::value` 在汇编中表现为立即数 5040），且理论上是 Turing complete 的；但其语法晦涩，现代替代方案 constexpr / consteval 以普通递归函数的写法获得同等的编译期执行能力。
