---
title: "Lecture 11 · Lambdas & Functors 逐字稿"
createAt: 2026/9/13
---

# Lecture 11: Lambdas & Functors（逐字稿）

> 对应课件转写：[2026Spring-11-LambdasAndFunctors.md](../output/2026Spring-11-LambdasAndFunctors.md)

## 1. 回顾：函数模板（Slides 2–13）

本讲以对 function templates（函数模板）的回顾开篇。考虑最朴素的 `min` 写法：针对每种类型各写一个重载。

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

若将三份代码中的返回类型与参数类型遮去，其余部分完全相同。既然除类型外别无差异，便可用一个占位的类型名 `T` 统一代替：

```cpp
T min(T a, T b) {
    return a < b ? a : b;
}
```

`T` 并非可以凭空使用：编译器必须知道它是一个类型参数。为此需在函数之前增加模板声明：

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}
```

课件对此的标注是：`template <typename T>` 一行表明"这是一个 template"，而 `T` 之后会被替换为具体类型。

模板函数使编译器得以替调用者生成代码。显式指定类型参数即为 explicit instantiation（显式实例化）：

```cpp
min<int>(106, 107);
min<double>(1.2, 3.4);
```

编译器据此生成 `int min(int, int)` 与 `double min(double, double)` 的完整函数体，两次调用分别返回 106 与 1.2。若不显式写出类型参数，则发生 implicit instantiation（隐式实例化）：

```cpp
int m = min(106, 107);
```

其效果与书写 `min<int>(106, 107)` 完全一致：编译器依据实参类型推出 `T = int`。这一机制与 `auto` 的设计思想相通——把类型推导交给编译器。

将模板思想应用于查找算法，可以得到同时泛化迭代器类型与元素类型的 `find`：

```cpp
template <typename It, typename T>
It find(It begin, It end, const T& value) {
  for (auto it = begin; it != end; ++it) {
    if (*it == value) return it;
  }
  return end;
}
```

该函数对不同的容器均可使用：

```cpp
std::vector<std::string> v { "run", "forrest" };
auto it = find(v.begin(), v.end(), "run");
// It = vector<std::string>::iterator
// T = std::string

std::set<std::string> s { "run", "forrest" };
auto it = find(s.begin(), s.end(), "run");
// It = std::set<std::string>::iterator
// T = std::string
```

课件以红字强调：此处发生的正是 implicit instantiation——编译器通过考察实参完成模板类型推导。

## 2. `find` 的再泛化：从查找特定值到提出任意问题（Slides 14–25）

一个自然的问题是：为什么 `find` 接收迭代器，而不是直接接收整个容器？将 vector 版与 set 版的调用并置即可发现，两段代码除容器类型声明外逐字相同；据此似乎可以改写为接收整个容器的版本：

```cpp
template <typename Container, typename T>
auto find(const Container& c, const T& value) {
    for (auto it = c.begin(); it != c.end(); ++it) {
        if (*it == value) return it;
    }
    return c.end();
}

std::vector<std::string> v { "run", "forrest" };
auto it = find(v, "run");
```

此版本的优势在于调用者无需关心 `begin` 与 `end`，模板参数亦被推导为 `Container = std::vector<std::string>`、`T = std::string`。需要说明的是，课件转写中该函数末行为 `return end;`，依上下文应为 `return c.end();`，系转写脱漏 `c.`，本文按后者处理。

迭代器接口的价值在于：它允许只搜索容器的一部分。

```cpp
std::vector<int> v { 106, 107, 106, 143, 149, 106 };

// Search for 106L, skipping first and last elements
auto it = find(v.begin() + 1, v.end() - 1, 106);

// Get index of iterator using std::distance
std::cout << std::distance(v.begin(), it);
// Prints 2, not 0
```

被搜索的子区间为 `107, 106, 143, 149`；`std::distance` 计算的是找到的位置相对于整个 `vector` 起点的距离，故输出 2 而非 0。由此可见，`find` 是以一般化（general）的方式定义的：容器与子区间均被抽象为迭代器对。

在此基础上可进一步追问：`find` 还能更一般吗？与其只能在容器中查找某个特定 `value`，不如允许向算法提出任意的问题——`string` 中的元音、`vector<int>` 中的素数、`set<int>` 中能被 5 整除的数；更一般地，能否向算法注入任意的操作？课件以一个具体场景说明该需求的由来：

```cpp
std::vector<std::string> trail_lens = { "6mi", "20ft", "5km" };
auto it = find(trail_lens, "3mi");
```

`trail_lens` 存储徒步路线的长度。由于 5 千米约合 3.1 英里，"长度合适的路线"无法通过等值比较找到：问题已不再是"是否等于某个值"，而是"它是否是一个合适的长度"。课件随即将代码中的关键部位替换为占位符——参数位写作 `Question`，循环条件位写作 `Question??`，调用处传入 "Is it a good length?"。这些占位符并非合法 C++，但指明了改造方向：把"问题"本身变为可以传给函数的对象。

这一抽象在应用层面早有对应。课件展示了徒步应用 AllTrails 的筛选界面：路线可按 Length（如 5–20 mi）、Elevation gain、是否 Dog-friendly、是否含瀑布等条件过滤，亦可按 Closest 等方式排序。每个筛选条件在本质上都是一个"是/否"判断——这正是下文 predicate 概念的现实原型。

## 3. predicate：返回 bool 值的函数（Slides 26–34）

本讲正式主题为 Functions & lambdas，内容分三部分：其一，函数与 lambda——如何在 C++ 中将函数表示为变量；其二，算法（Algorithms）——以现代 C++ 实现一个经典算法；其三，ranges 与 views——一套全新的（C++20/23/26 及其后）、函数式风格的 C++ 算法接口。

定义：**predicate（谓词）是返回 `boolean` 值的函数。**"这条路线有瀑布吗？""这条路线比那条长吗？"这类可用是/否回答的提问，均对应一个 predicate。按参数个数可分为 unary（一元）与 binary（二元）两类：

```cpp
// Unary
bool isVowel(char c) {
  c = toupper(c);
  return c == 'A' || c == 'E' ||
    c == 'I' || c == 'O' || c == 'U';
}
bool wouldPrestonApproveOf(Trail t)
{
    return t.hasWaterfall();
}
```

```cpp
// Binary
bool isDivisible(int n, int d) {
    return n % d == 0;
}
bool isLongerThan(Trail x, Trail y){
    return x.len > y.len;
}
```

`isVowel` 先以 `toupper` 统一大小写再判断元音；`isDivisible` 判断整除关系；`isLongerThan` 比较两条路线的长度。随之而来的问题是使用方式：如何以 `isVowel` 在 `string` 中定位第一个元音，以 `wouldPrestonApproveOf` 在 `vector<Trail>` 中找到含瀑布的路线，或以 `isDivisible` 找到能被 5 整除的数？本节的核心思想是：**需要将 predicate 作为参数传入函数。**

## 4. find_if：接收 predicate 的查找算法（Slides 35–45）

回到此前的 `find`：

```cpp
template <typename It, typename T>
It find(It first, It last, const T& value) {
    for (auto it = first; it != last; ++it) {
        if (*it == value) return it;
    }
    return last;
}
```

条件 `*it == value` 对"查找特定值"有效，但过于具体；改造目标是用一个一般的条件取代它。若将第三个参数由 `value` 换为 predicate `pred`，循环中的关键判断即可替换为对 predicate 的调用：

```cpp
template <typename It>
It find(It first, It last, ???? pred) {
    for (auto it = first; it != last; ++it) {
        if (pred(*it)) return it;
    }
    return last;
}
```

算法对每个元素调用 `pred(*it)`，一旦满足即返回。剩余的问题是 `????` 处 predicate 的类型。答案仍然是模板：为模板参数表增加一项即可。为避免与按值查找的 `find` 混淆，函数更名为 `find_if`——该名称与标准库 `<algorithm>` 中的同名算法一致。

```cpp
template <typename It, typename Pred>
It find_if(It first, It last, Pred pred) {
  for (auto it = first; it != last; ++it) {
    if (pred(*it)) return it;
  }
  return last;
}
```

三个要点：`Pred` 是 predicate 的类型，由编译器经 implicit instantiation 推导；`pred` 是作为参数传入的谓词；`if (pred(*it)) return it;` 在每个元素上调用谓词，命中即返回。

两个使用示例。其一，在字符串中定位并修改第一个元音：

```cpp
bool isVowel(char c) {
    c = toupper(c);
    return c == 'A' || c == 'E' || c == 'I' ||
           c == 'O' || c == 'U';
}

std::string flower = "rose";
auto it = find_if(flower.begin(), flower.end(), isVowel);
*it = 'i'; // "rise"
```

`find_if` 找到 "rose" 中的第一个元音 `'o'`，改写后得到 "rise"。此处 `Pred` 被推导为何种类型，调用者无需书写，推导由编译器完成。其二，查找含瀑布的路线：

```cpp
bool isGood(Trail t) { // Would I Approve?
   return t.hasWaterfall();
}

std::vector<Trail> trails = getNearbyTrails();
auto it = find_if(trails.begin(), trails.end(),  isGood);
assert(it->hasWaterfall() == true);
```

两例的共同结论构成本节要点：**通过传入函数，可以用用户自定义的行为（user-defined behaviour）泛化一个算法**——算法骨架保持不变，具体行为由调用者注入。

## 5. `Pred` 的类型：function pointer 及其局限（Slides 46–53）

就目前传入普通函数的用法而言，`Pred` 被推导为 function pointer（函数指针）：

```cpp
find_if(flower.begin(), flower.end(), isVowel);
// Pred = bool(*)(char)

find_if(t.begin(), t.end(), isGood);
// Pred = bool(*)(Trail)
```

以 `bool(*)(Trail)` 为例：`bool` 为函数的返回类型，`(*)` 表明这是函数指针，`Trail` 为参数类型。课件同时指出，function pointer 只是可传入 `find_if` 的类型之一。

function pointer 的推广能力不佳。考虑新需求：在 `vector` 中查找小于 N 的数。当 N 为编译期常量时，只能逐一定义：

```cpp
bool lessThan5(int x) { return x < 5; }
bool lessThan6(int x) { return x < 6; }
bool lessThan7(int x) { return x < 7; }

find_if(begin, end, lessThan5);
find_if(begin, end, lessThan6);
find_if(begin, end, lessThan7);
```

这种枚举无法穷尽；更关键的是，若 N 须待运行时方能确定，函数名无法在编译期反映 N 的取值：

```cpp
int n;
std::cin >> n;
find_if(begin, end, /* lessThan...? */)
```

**例题**：为解决上述问题，为 predicate 增加一个参数是否可行？即定义

```cpp
bool isLessThan(int elem, int n) {
    return elem < n;
}
```

**解析**：不可行。考察 `find_if` 内部的调用点：

```cpp
template <typename It, typename Pred>
It find_if(It first, It last, Pred pred) {
    for (auto it = first; it != last; ++it) {
        if (pred(*it)) return it;
    }
    return last;
}
```

算法对 `pred` 只传入一个实参（课件标注：We only pass one parameter to pred here!），而 `isLessThan` 需要两个实参，调用无法成立。真正的需求因此表述为：**赋予函数额外的状态（此处的 `n`），且不通过增加参数的方式。**下文的 lambda 正是这一需求的解答。

## 6. lambda：语法与 capture（Slides 54–61）

**lambda function（Lambda 表达式）是能够从外围作用域（enclosing scope）capture（捕获）状态的函数。**针对上一节的问题：

```cpp
int n;
std::cin >> n;

auto lessThanN = [n](int x) { return x < n; };

find_if(begin, end, lessThanN);
```

`n` 在运行时读入，capture 子句 `[n]` 将其纳入 lambda，`lessThanN` 由此成为"小于 n"的判定函数，可直接传入 `find_if`。

以 `auto lessThanN = [n](int x) { return x < n; };` 为例，lambda 语法可分解为四个部分：

- `auto`：lambda 的类型由编译器掌握，调用者以 `auto` 接收；
- `[n]`：capture 子句（capture clause），使函数体能够使用外围变量；
- `(int x)`：参数列表，与普通函数完全一致；
- `{ return x < n; }`：函数体，与普通函数一致，区别仅在于其作用域内只有参数与 captures。

capture 的常见写法汇总如下：

```cpp
auto lambda = [capture-values](arguments) {
    return expression;
}

[x]      // captures x by value（按值捕获，生成副本）
[&x]     // captures x by reference（按引用捕获）
[x, y]   // captures x, y by value
[&]      // captures everything by reference（全部按引用捕获）
[&, x]   // captures everything except x by reference（除 x 按值捕获外，其余按引用捕获）
[=]      // captures everything by value（全部按值捕获）
```

说明：课件转写将单个变量的按引用捕获记作 `[x&]`；依 C++ 语法应为 `[&x]`，上文已按规范形式书写。

lambda 亦可完全不捕获任何变量——此时它就是"临时定义函数"的工具：

```cpp
std::vector<Trail> trails = {
    {"3 miles", false},
    {"5 miles", true},
    {"2 miles", false},
    {"8 miles", true}
};

auto it = find_if(trails, [](const auto& t) {
    return t.hasWaterfall();
});
```

函数体仅使用参数 `t`，capture 列表留空即可。

另一语法要点：**`auto` 参数是模板的简写。**

```cpp
auto lessThanN = [n](auto x) {
    return x < n;
};
```

等价于

```cpp
template <typename T>
auto lessThanN = [n](T x) {
    return x < n;
};
```

该规则不限于 lambda：凡出现 `auto` 参数之处均成立，其背后同样是 implicit instantiation——编译器在调用点推导类型。

## 7. lambda 的实现原理：编译器生成的 functor（Slides 62–76）

分析 lambda 的实现之前，先回顾 STL 的四大组件：**Containers**（如何存储一组对象）、**Iterators**（如何遍历容器）、**Algorithms**（如何以泛型方式变换与修改容器），以及本节关注的 **Functors**（如何将函数表示为对象）。

定义：**functor（函数对象）是任何定义了 `operator()` 的对象**，即"调用方式与函数一致的对象"。标准库提供了两个典型例子：

```cpp
template <typename T>
struct std::greater {
    bool operator()(const T& a, const T& b) const {
        return a > b;
    }
};

std::greater<int> g;
g(1, 2); // false
```

`std::greater<T>` 是定义了 `operator()` 的 struct；构造对象 `g` 之后，`g(1, 2)` 返回 `false`。对象在语法上表现出函数般的调用形式，这正是 functor 的基本样态。另一例为 `std::hash` 的特化：

```cpp
template <>
struct std::hash<MyType> {
    size_t operator()(const MyType& v) const {
        // Crazy, theoretically rigorous hash function
        // approved by 7 PhDs and Donald Knuth goes here
        return ...;
    }
};

MyType m; std::hash<MyType> hash_fn;
hash_fn(m); // 125123201 (for example)
```

`template <>` 配合 `std::hash<MyType>` 的写法称为针对类型 `MyType` 的 template specialization（模板特化）；`hash_fn(m)` 返回一个 `size_t` 类型的哈希值。课件提示：这也是为自定义类型提供哈希函数的途径之一，与后续 unordered 关联容器的内容相关。

functor 的决定性性质在于：**它是对象，因而可以拥有状态（state）。**

```cpp
struct my_functor {
    int operator()(int a) const {
        return a * value;
    }

    int value;
};

my_functor f;
f.value = 5;
f(10); // 50
```

成员变量 `value` 存于对象内部；同一个 functor 类型在不同 `value` 之下表现出不同行为。这正是 function pointer 所不具备的携带状态的能力。由此引出本节的核心结论：**使用 lambda 时，编译器会生成一个 functor 类型。**

对照观察。源代码：

```cpp
int n = 10;
auto lessThanN = [n](int x) { return x < n; };
find_if(begin, end, lessThanN);
```

与之完全等价的、编译器视角的代码：

```cpp
class __lambda_6_18
{
public:
    bool operator()(int x) const { return x < n; }
    __lambda_6_18(int& _n) : n{_n} {}
private:
    int n;
};

int n = 10;
auto lessThanN = __lambda_6_18{ n };
find_if(begin, end, lessThanN);
```

对应关系如下：`__lambda_6_18` 是仅编译器可见的随机类名；lambda 的函数体成为 `operator()`（即 functor 的调用运算符）；编译器同时生成构造函数；**capture 变量成为类的成员变量**——`int n;` 即对应 `[n]`；末行构造 lambda 对象，等价于把外围 `n` 经构造函数传入，按值捕获即复制进成员。课件推荐 https://cppinsights.io ，可用于观察代码经编译器展开后的实际形态。

这种"书写形式与编译器理解形式不一致"的现象并非首次出现。range-based for

```cpp
std::vector<int> v {1,2,3};
for (const int& e : v)
{
    // ...
}
```

在编译器看来即是

```cpp
auto begin = v.begin();
auto end = v.end();
for (auto it = begin; it != end; ++it)
{
    // ...
}
```

lambda 与此同理：源代码中的 lambda 对应编译器生成的 functor class，属于 syntactic sugar（语法糖）。

本节小结有三点：其一，函数与 lambda 使**行为（behaviour）**可以像变量一样传递；其二，`std::function` 是函数与 lambda 的总括类型，任何 functor、lambda 或 function pointer 均可转换赋给签名匹配的 `std::function` 对象，代价是调用开销略有增加；其三，常规实践中以 `auto` 与模板参数为主，无需显式关心类型。示例：

```cpp
std::function<bool(int, int)> less = std::less<int>{};
std::function<bool(char)> vowel = isVowel;
std::function<int(int)> twice = [](int x) { return x * 2; };
```

三种来源——functor、函数指针、lambda——均可装入对应签名的 `std::function`。

## 8. STL 算法库（Slides 77–86）

lambda 与 functor 的主要应用场景之一是标准库算法。再看 STL 四大组件中的 **Algorithms**：如何以泛型方式变换与修改容器。

第 4 节的 `find_if` 并非虚构：`std::find`、`std::find_if`、`std::find_if_not` 定义于头文件 `<algorithm>`，其中 `find_if` 的基本重载为

```cpp
template< class InputIt, class UnaryPred >
InputIt find_if( InputIt first, InputIt last, UnaryPred p );
```

与本文第 4 节实现的版本在接口上一致。

`<algorithm>` 是模板函数的集合，代表性接口包括：

```cpp
std::count_if(InputIt first, InputIt last, UnaryPred p);
```

统计 `[first, last)` 中满足谓词 `p` 的元素个数；

```cpp
std::sort(RandomIt first, RandomIt last, Compare comp);
```

按比较器 `comp` 对 `[first, last)` 排序；

```cpp
std::max_element(ForwardIt first, ForwardIt last, Compare comp);
```

按比较器 `comp` 求最大元素。

另有一类算法同时作用于输入范围与输出位置：`std::copy_if(r1, r2, o, p)` 将 `[r1, r2)` 中满足谓词 `p` 的元素拷贝至 `o`；`std::transform(r1, r2, o, op)` 对每个元素施加 `op` 并将结果写入 `o`；`std::unique_copy(i1, i2, o, p)` 去除 `[r1, r2)` 中的连续重复后写入 `o`。

标准算法数量庞大，涵盖 `all_of`/`any_of`/`none_of`、`for_each`、`find` 系列、`count` 系列、`copy` 系列、`replace` 系列、`sort`/`stable_sort`、`partition` 系列、heap 系列、`set_union`/`set_intersection`/`set_difference`、`rotate`、`shuffle`、`next_permutation` 等。其能力可概括为：二分查找、建堆、求 min/max、字典序比较、归并、集合运算、partition、排序、选取第 n 小元素、洗牌、按条件删除、按条件拷贝、for-each、随机采样——均以最一般的形式提供。

课件另以实例说明 `<algorithm>` 的现实应用：生物序列分析库 SeqAn、TCP 报文交互分析、Huffman 编码，以及 LLVM——其全部工具与库均以 C++ 编写，并大量使用 STL。

## 9. 实例：基于 STL 的 tokenizer（Slides 87–113）

本节以一个完整示例演示 STL 算法与 lambda 的配合：实现 tokenizer（分词器），将字符串切分为词元（token），例如把 `"Breaking down the string"` 分解为 `{"Breaking", "down", "the", "string"}`。

先以人工方式拆解该例。在每个空格处作分隔记号，记号位置的下标依次为 0、8、13、17，以及 `end()`；每个 token 对应一个左闭右开的下标区间：

| Substring | Range |
| :--- | :--- |
| `"Breaking"` | `[0, 8)` |
| `" down"` | `[8, 13)` |
| `" the"` | `[13, 17)` |
| `" string"` | `[17, end)` |

规律在于：每个空格既是一个 token 的终点，又是下一个 token 的起点。据此，算法分两步：第一步取得所有需要的位置——即迭代器；第二步以两个迭代器配对循环，逐一生成 token。

第一步的第一版实现为手写循环：

```cpp
// Get all indeces we want.
std::set<std::string::iterator> spaces {source.begin(), source.end()};
for (auto cur = source.begin(); cur != source.end(); ++cur) {
  if (*cur == ' ') {
    spaces.insert(cur);
  }
}
```

即建立一个存储迭代器的 `std::set`，预置 `begin` 与 `end`，再自行遍历插入空格位置。课件对此的评价是"自己处理的逻辑过多"（We're handling too much logic ourselves）。第二版仅改动判断一行，以谓词 `std::isspace(*cur)` 取代与字符 `' '` 的直接比较。以 predicate 表述筛选条件后，该逻辑即呈现 filter、`find_if`、find_all 一类的典型形态，可据此写出泛型版本：

```cpp
template <typename Iterator, typename UnaryPred>
std::vector<Iterator> find_all(Iterator begin, Iterator end, UnaryPred pred) {
    std::vector<Iterator> its{begin};
    for (auto it = begin; it != end; ++it) {
        if (pred(*it))
            its.push_back(it);
    }
    its.push_back(end);
    return its;
}
```

结果向量预置 `begin`，遍历中凡满足谓词即收录当前迭代器，最后补入 `end`。调用时 `begin`/`end` 取自 `source`，谓词传 `std::isspace`。（注释中的 "indeces" 为课件原文拼写，规范拼写为 "indices"。）

第二步将相邻的空格迭代器两两配对生成 token。直观写法是双迭代器并行的手写循环，但课件标注其为不良实现（bad）：

```cpp
// Double iterator loop to get tokens.
Corpus tokens;
auto first = spaces.begin();
auto second = std::next(first);
for (; second != spaces.end(); ++first, ++second) {
  auto start_char = *first;
  auto end_char = *second;
  tokens.insert({source, start_char, end_char});
}
```

该写法可用，但仍属手工循环。改用 `std::transform` 的双输入范围版本：

```cpp
template< class InputIt1, class InputIt2,
          class OutputIt, class BinaryOp >
OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                    OutputIt d_first, BinaryOp binary_op );
```

`first1`/`last1` 界定第一个输入范围，`first2` 为第二个输入范围的起点，`d_first` 为输出位置，`binary_op` 为二元操作，作用于两个序列的对应元素。`spaces` 集合恰好可视为两个错开一位、长度相同的序列，各参数取值如下：

```cpp
first1    = spaces.begin()
last1     = spaces.end() - 1
first2    = spaces.begin() + 1
d_first   = std::inserter(tokens, tokens.end())
binary_op = [&](auto it1, auto it2) {
                return Token(source, it1, it2);
            }
```

第一个序列自 `begin()` 至 `end() - 1`，第二个序列自 `begin() + 1` 至末尾，分别指向每个 token 的起点与终点；输出经 `std::inserter` 插入 `tokens`；`binary_op` 是一个接收两个迭代器并构造 `Token` 的 lambda，其 `[&]` 按引用捕获了外层的 `source`。（严格而言，`std::set` 的迭代器为双向迭代器，不支持 `end() - 1` 这类随机访问写法，实际代码应以 `std::prev(spaces.end())`、`std::next(spaces.begin())` 表达；课件为突出配对结构采用了简写。）

上述方案尚未处理非规范输入。对 `"N'ot a!!    Str1ngs 4re    nice :/"` 一类含连续空格的字符串，每个多余的空格都会产生一个空 token，结果 `{"N'ot", "a!!", "", "Str1ngs", "4re", "", "nice", ":/"}` 中因此出现两个 `""`。（课件转写中 `"Str1ngs" "4re"` 之间脱漏逗号，此处已补。）清理空 token 使用 `std::erase_if`（`<set>` 中自 C++20 起提供对应重载）：

```cpp
template< class Key, class Compare, class Alloc,
          class Pred >
std::set<Key, Compare, Alloc>::size_type
    erase_if( std::set<Key, Compare, Alloc>& c,
              Pred pred );
```

该函数删除容器 `c` 中所有满足谓词 `pred` 的元素，返回被删除元素的个数，复杂度为线性。课件给出的等价实现即"满足则 `erase` 并接住返回的新迭代器，否则 `++first`"的循环。本例中容器 `c` 传 `tokens`，谓词传

```cpp
[](const auto& t) {
    return t.content.empty();
}
```

即删除内容为空的 token。

课件将本例的方法论总结为：先人工演算示例；再整理逻辑；继而考察该逻辑是否对应某个常见算法——若是，则使用标准算法库，以保证清晰与正确。本例拆出的三个子问题分别对应：收集全部空格位置（含首尾）——使用课程提供的 `find_all`；由空格位置构造 token——使用标准库的 `std::transform`；删除空 token——使用标准库的 `std::erase_if`。

## 10. ranges：以 range 为参数的算法接口（Slides 114–125）

ranges 是 STL 的新一代形态。定义只有一句：**range（范围）是任何具有 begin 与 end 的对象。**据此，`std::vector<T>`、`std::unordered_set<K,V>`、`std::map<K, V>`、`std::set<K>`，乃至提供了 begin/end 的自定义类型，都是 range。

回顾第 2 节的问题：`find` 采用迭代器接口是为了支持子区间搜索，但课件明确指出，多数调用并不需要这一能力：

```cpp
int main() {
    std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};
    auto it = std::find(v.begin(), v.end(), 'c');
}
```

若目的只是搜索整个容器，显式传递 `v.begin()` 与 `v.end()` 属于多余的形式。`std::ranges` 为 `<algorithm>` 提供了以 range 为参数的新版本：

```cpp
int main() {
    std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};
    auto it = std::ranges::find(v, 'c');
}
```

`v` 本身是 range，可直接传入。需要子区间时，迭代器对形式仍然可用：

```cpp
int main() {
    std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};

    // Search from 'b' to 'd'
    auto first = v.begin() + 1;
    auto last = v.end() - 1;

    auto it = std::ranges::find(first, last, 'c');
}
```

`<algorithm>` 中的绝大多数算法均有 ranges 等价版本，且该体系极新：以 C++20 为基础，C++23 补充了 `ranges::find_last`、`ranges::find_last_if`、`ranges::contains`、`ranges::contains_subrange`、`ranges::starts_with`、`ranges::ends_with` 等，并在 C++20/23/26 及后续标准中持续演进；`copy`/`move`/`fill`/`transform`/`generate` 与 `remove`/`replace`/`reverse`/`rotate`/`shuffle` 等算法的 ranges 版本均自 C++20 提供。

ranges 算法的另一特征是 constrained（受约束的）：它们建立在新的 STL concepts 之上。

```cpp
template<class T>
concept range = requires(T& t) { ranges::begin(t); ranges::end(t); };
template<class T>
concept input_range =
    ranges::range<T> && std::input_iterator<ranges::iterator_t<T>>;
template<ranges::input_range R, class T, class Proj = std::identity>
borrowed_iterator_t<R> find( R&& r, const T& value, Proj proj = {} );
```

第一条：range 即"可对其调用 `ranges::begin` 与 `ranges::end`"的类型，与前面的非形式定义一致；第二条：input_range 是元素满足 input iterator 要求的 range；第三条是 ranges 版 `find` 的声明，模板参数 `R` 直接以 `ranges::input_range` 约束（签名中另有默认为 `std::identity` 的投影参数 `Proj`）。

ranges 部分小结：其一，ranges 使用 concepts，类型不满足约束时编译报错信息更为明确；其二，可以直接传入整个容器。课件随后以此为引指出，上述内容尚未穷尽新接口的全部——views 是在此之上的进一步抽象。

## 11. views：惰性的算法组合（Slides 126–137）

views 是一种组合算法的方式。定义：**view（视图）是一个 lazily（惰性）地 adapts（改造）另一个 range 的 range。**该定义包含三个要点：view 自身是 range；其工作是惰性的；它改造的是底层的另一个 range。课件另给出等价表述：view 是一个逐元素（one element at a time）、惰性变换其底层 range 的 range。

先观察旧 STL 中"过滤 + 变换"的写法：

```cpp
std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};

// Filter -- Get only the vowels
std::vector<char> f;
std::copy_if(v.begin(), v.end(), std::back_inserter(f), isVowel);

// Transform -- Convert to uppercase
std::vector<char> t;
std::transform(f.begin(), f.end(), std::back_inserter(t), toupper);

// { 'A', 'E' }
```

为取得"元音的大写形式"，需要引入两个中间容器 `f` 与 `t`，并完整遍历两遍。以 views 改写：

```cpp
std::vector<char> letters = {'a', 'b', 'c', 'd', 'e'};

auto f = std::ranges::views::filter(letters, isVowel);
auto t = std::ranges::views::transform(f, toupper);

auto vowelUpper = std::ranges::to<std::vector<char>>(t);
```

逐行分析：`f` 是一个 view，套在底层 range `letters` 之上，产出一个仅含元音的新 range；`t` 亦是一个 view，套在 `f` 之上，产出一个由大写字符组成的新 range；末行 `std::ranges::to` 将 view 物化（materialize）为 `vector`。课件强调：在末行之前，没有任何实际计算发生。

views 可经 `operator |` 以管道形式串联：

```cpp
std::vector<char> letters = {'a','b','c','d','e'};
std::vector<char> upperVowel = letters
    | std::ranges::views::filter(isVowel)
    | std::ranges::views::transform(toupper)
    | std::ranges::to<std::vector<char>>();

// upperVowel = { 'A', 'E' }
```

自左向右即为处理流程：过滤、变换、收集，可读性良好。

此处需区分两类语义。**range 算法是 eager（急切求值）的**：`std::ranges` 的算法本质上是旧 STL 算法的换装（reskin），因此

```cpp
// This actually sorts vec, RIGHT NOWWW!!!!
std::ranges::sort(v);
```

在该行执行时即完成排序。**views 则是 lazy（惰性求值）的**：构造 view 只是搭建处理管道，尚无任何元素被处理，直至 `std::ranges::to` 才触发计算。

课件的进阶提示：views 在语义上相当于 Python 的 generator。以下 C++ 代码与 Python 代码行为完全一致：

```cpp
auto view = letters
    | std::ranges::views::filter(isVowel)
    | std::ranges::views::transform(toupper);
auto upperVowel = std::ranges::to<std::vector<char>>(view);
```

```python
view = (l for l in letters if isVowel(l))    # Lazy evaluation
view = (l.upper() for l in view)             # Lazy evaluation
upperVowel = list(view)
```

Python 的 generator 表达式逐级惰性求值，末行 `list(view)` 才触发遍历，与 C++ 的 `filter`/`transform`/`ranges::to` 一一对应。

本讲末页总结了 ranges/views 的利弊。优势：减少对迭代器的直接操作；算法受 concepts 约束，报错信息更好；函数式管道语法可读性强。劣势：标准与编译器支持尚新、功能未全；相对于手写版本可能存在性能损失——课件为此链接了 *The Terrible Problem of Incrementing a Smart Iterator*（https://www.fluentcpp.com/2019/02/12/the-terrible-problem-of-incrementing-a-smart-iterator/ ），该文分析了 `filter_view` 迭代器自增变慢的成因。

## 本讲要点

- predicate（返回 bool 的函数）使"查找/筛选的条件"本身成为算法的参数：`find_if(first, last, pred)` 以模板参数 `Pred` 承接谓词，由 implicit instantiation 完成类型推导，其接口与标准库 `<algorithm>` 的真实设计一致。
- function pointer（如 `bool(*)(char)`）是传入普通函数时 `Pred` 的推导结果，但它无法携带状态，无法表达"小于运行时给定的 N"这类条件；所需的机制是"不增加参数而附加状态"。
- lambda 通过 capture 子句从外围作用域携带状态，其本质是编译器生成的 functor class：captures 成为成员变量，函数体成为 `operator()`；functor 即定义了 `operator()` 的对象（如 `std::greater`、`std::hash` 特化、自定义 `my_functor`），因为是对象而可以拥有 state。`std::function` 能统一容纳 functor、function pointer 与 lambda，但调用略有开销，常规实践以 `auto`/模板为主。
- STL `<algorithm>` 是围绕迭代器对与 predicate/比较器构建的泛型算法集合；tokenizer 实例演示了 `find_all` + `std::transform`（双输入范围错位配对）+ `std::erase_if` 的组合，方法论为"演算示例 → 整理逻辑 → 对应标准算法"。
- ranges 使算法可直接接收整个容器（并保留迭代器对形式），并以 concepts 约束类型、改善报错；views 以惰性方式组合算法、支持 `operator |` 管道，语义对应 Python generator。应牢记：range 算法为 eager，views 为 lazy，`std::ranges::to` 才触发实际计算。
