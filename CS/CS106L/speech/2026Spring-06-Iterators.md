---
title: "Lecture 06 · Iterators 逐字稿"
createAt: 2026/9/13
---

# Lecture 06: Iterators（逐字稿）

> 对应课件转写：[2026Spring-06-Iterators.md](../output/2026Spring-06-Iterators.md)

## 1. 复习：containers 小测（Slides 1–6）

本讲标题为 Iterators and Pointers。封面左侧示意 iterator 自 `begin` 出发逐个经过元素直至 `end`，右侧示意指针指向内存地址，正对应本讲两大主题。正式内容之前，课件以三道复习题回顾上一讲的 containers。

**例题.** (a) 哪种容器在头部与尾部插入元素的效率相当？(b) 哪种容器要求元素类型支持 comparison operator（比较运算符）？若不希望满足该要求，可改用什么？(c) 通常情况下 `unordered_set` 与 `set` 何者更快，原因何在？

**解析.** (a) `std::deque`：头尾两端插入均为高效操作，这是它区别于 `vector` 的主要特征。(b) `std::map` 与 `std::set`：二者底层为有序结构，元素的存放位置由比较运算决定；绕开该要求的途径是改用基于哈希的 unordered 系列。(c) 通常 `std::unordered_set` 更快：哈希配合较小的 load factor（负载因子）使操作接近常数时间，而 `set` 的每次操作需沿树走一条路径。

课件随后以四幅图回顾各类容器的内部结构：`vector` 是一整块连续内存；`deque` 的元素分块存放、首尾留有空槽；`map` 底层是二叉搜索树，每个节点保存 key 与 value；`unordered_map` 以一排桶（bucket）按哈希值分散存放键值对。

## 2. 问题引入：range-based for 的普适性（Slides 7–12）

上一讲使用过的循环写法

```cpp
for (const auto& elem : container)
```

对 `std::map`、`std::vector`、`std::set`、`std::deque` 全部适用。这一普适性构成本讲的核心疑问：这些容器的内部结构差异极大，同一语法为何全部有效？逐个考察：

```cpp
std::vector<int> v { 1, 2, 3, 4 };

for (const auto& elem : v) {
    std::cout << elem << std::endl;
}
```

`vector` 是连续数组，直觉上可以用下标 `v[i]` 逐个访问元素。

```cpp
std::deque<int> d {
    1, 9, 7, 3,
    2, 1, 2, 9
};

for (const auto& elem : d) {
    std::cout << elem << std::endl;
}
```

`deque` 内部并非一整块连续内存：元素被切分为多个 chunk，首尾另有空槽，按下标推进时需经内部换算，但 range-based for 的写法不变。

```cpp
std::map<std::string, int> m {
    { "Chris", 31 }, { "CS106L", 42 },
    { "Keith", 14 }, { "Nick", 51 },
    { "Sean", 35 },
};

for (const auto& pair : m) {
    std::cout << pair.first << " ";
    std::cout << pair.second;
}
```

`map` 底层是二叉搜索树，并非线性结构；遍历按 key 的顺序进行，循环变量是键值对，以 `pair.first`、`pair.second` 分别取得 key 与 value。

```cpp
std::unordered_map<string, int> m
{
    { "Chris", 31 }, { "Nick", 51 },
    { "Sean", 35 },
};

for (const auto& pair : m) {
    std::cout << pair.first << " ";
    std::cout << pair.second;
}
```

`unordered_map` 底层是哈希桶，遍历顺序既不按 key 排序，也与插入顺序无关，但同样支持 range-based for。

数组、分块、树、哈希表四种结构共用同一套循环语法，其原因正是本讲要建立的 iterator（迭代器）抽象；`const auto&` 部分本身的语义也会随之得到解释。

## 3. STL 的组成与本讲结构（Slides 13–16）

STL（Standard Template Library，标准模板库）由四个组件构成：Containers，回答如何存储一组对象；Iterators，回答如何遍历容器；Functors，回答如何将函数表示为对象；Algorithms，回答如何以泛型方式变换与修改容器。本讲聚焦 Iterators，分三部分展开：iterator 的基本概念；iterator 按性质划分的类型体系；pointer（指针）与内存。

## 4. Iterator Basics：迭代器的引入（Slides 17–24）

对 `vector` 这类连续容器，最常见的迭代方式是下标循环：

```cpp
std::vector<int> v {1,2,3,4};
for (size_t i = 0; i < v.size(); i++) {
    const auto& elem = v[i];
    std::cout << elem;
}
```

抽去容器相关细节，其一般骨架为

```cpp
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
    /* do something with elem */
}
```

该骨架依赖下标访问。`set` 不支持 `s[i]`——树形结构不存在"第 i 个位置"的概念，骨架中初始化、条件、递增三处均无从填写。课件同时注明：在阐明 range-based for 的机制之前，暂不使用 `for (auto e : s)`。

由此引出需求：需要一个对象记录"当前处于容器中的位置"，其作用类似 index，但不依赖连续内存。这就是 iterator。

课件将 iterator 比作抓娃娃机的爪子：爪子能够抓取当前元素、向前移动一格、判断是否结束；机器（容器）则负责给出起点与终点。对应到代码：

```cpp
auto it = c.begin();   // 定位到第一个元素
++it;                  // 前进一步
auto elem = *it;       // 取当前元素
it == c.end()          // 判断是否到头
```

从 `c.begin()` 出发，反复 `++it` 前进，途中可随时以 `*it` 取值，最终以 `it == c.end()` 判定结束。容器与迭代器协作完成遍历：容器提供起点与终点，迭代器负责定位、前进与取值。

## 5. 容器接口与迭代器接口（Slides 25–29）

容器一侧提供两个关键成员函数。`container.begin()` 返回指向容器第一个元素的 iterator（前提是容器非空）；`container.end()` 返回一个 past-the-end（尾后）iterator，指向容器最后一个元素之后的位置。

`end()` 永不指向任何元素，它标记的是"最后一个元素再往后一格"。这一设计有一个直接推论：若容器 `c` 为空，则 `c.begin() == c.end()`。空容器没有第一个元素，`begin()` 只能指向"本应是第一个元素的位置"，而该位置正是 `end()` 所在。后文所有循环条件均以此为基础。

迭代器一侧提供四个基本操作：

```cpp
// 直接初始化
auto it = c.begin();
// 前进一步
++it;
// 解引用；若 it == end() 则为 undefined behavior
auto& elem = *it;
// 相等比较：是否处于同一位置
if (it == c.end()) ...
```

其中解引用 `*it` 在 `it` 等于 `end()` 时是 undefined behavior（未定义行为），因为尾后位置不存在元素。

## 6. 迭代器循环与 range-based for 的展开（Slides 30–38）

有了上述接口，`set` 的循环骨架便可逐项填写：var-init 处填 `auto it = s.begin();`；condition 处填 `it != s.end();`，即尚未到达尾后位置就继续；increment 处填 `++it`；循环体中以 `*it` 取出当前元素。完整形式为

```cpp
std::set<int> s {1,2,3,4};

for (auto it = s.begin(); it != s.end(); ++it) {
    const auto& elem = *it;
}
```

该循环不依赖任何下标或 `operator[]`，对 `set`、`map`、`unordered_map` 同样成立。条件使用 `!=` 而非 `<`：对树、哈希表等结构，迭代器之间的先后比较未必有意义，而"是否处于同一位置"的比较对各类迭代器均可定义。

range-based for 正是这一循环的语法糖。当书写

```cpp
for (auto elem : s)
{
    std::cout << elem;
}
```

编译器实际生成的等价代码为

```cpp
auto b = s.begin();
auto e = s.end();

for (auto it = b; it != e; ++it) {
    auto elem = *it;
    std::cout << elem;
}
```

先求出 `b = s.begin()` 与 `e = s.end()`，再执行标准迭代器循环，每轮将 `*it` 拷贝给 `elem`。这同时回答了开头的两个疑问：不同容器共用同一语法，是因为它们都提供 `begin()`、`end()`，以及支持 `++`、`*`、`==` 的迭代器；`const auto& elem` 绑定的正是 `*it` 取出的元素，加引用避免拷贝，加 `const` 禁止修改。

## 7. 迭代器的类型：别名与前缀递增（Slides 39–45）

循环变量 `it` 的具体类型是什么？对比两种写法：

```cpp
std::map<int, int> m { {1, 2}, {3, 4}, {5, 6}};
auto it = m.begin();
auto elem = *it;            // {1, 2}
```

```cpp
std::map<int, int> m { {1, 2}, {3, 4}, {5, 6}};
std::map<int, int>::iterator it = m.begin();
std::pair<int, int> elem = *it;
```

`m.begin()` 返回 `std::map<int, int>::iterator`，解引用得到 `std::pair<int, int>`。类型名冗长，故迭代器通常配合 `auto` 使用。`::iterator` 这一名字来自类内的类型别名声明：

```cpp
// <map> 头文件内部
template <typename K, typename V>
class std::map {
    using iterator = /* some iterator type */;
};

// 头文件外部（如 main.cpp）
std::map<int, int>::iterator it = m.begin();
```

课件另以 aside 说明代码为何一贯写作 `++it` 而非 `it++`。两个运算符的签名如下：

```cpp
// 前缀形式 ++it：递增 it，返回同一对象的引用
Iterator& operator++();
```

```cpp
// 后缀形式 it++：递增 it，返回旧值的拷贝
Iterator operator++(int);
```

前缀形式不产生新对象；后缀形式按语义必须先保存旧值，因而多出一次拷贝。iterator 是完整的对象，其拷贝代价通常远高于 `int`。Bjarne Stroustrup 对此的表述是："`++i` 有时比 `i++` 更快，且绝不会更慢……当 `i++` 作为独立语句而非更大表达式的一部分时，不妨直接写 `++i`：不会有任何损失，有时还有所获益。"这是课件代码一律采用前缀形式的原因。

## 8. 例题与解析：迭代器状态追踪（Slide 47）

**例题.** 写出下列代码执行后 `a`、`b`、`c` 各自指向的位置。

```cpp
std::map<int, int> m {
    {1, 2}, {3, 4}, {5, 6}
};
auto a = m.begin();
++a;
auto b = a;
++a;
auto c = ++a;
```

**解析.** 逐行推演：`a = m.begin()` 指向 {1, 2}；`++a` 后 a 指向 {3, 4}；`auto b = a` 将 a 的值拷贝给 b，b 亦指向 {3, 4}，此后二者相互独立；`++a` 仅推进 a，a 到达 {5, 6}；最后一行 `auto c = ++a` 中，前缀 `++a` 先将 a 推进到 `end()` 的位置，再返回 a 自身的引用，故 c 取得递增后的值。

结论：a 与 c 均停在 `end()`，b 指向 {3, 4}。本例有两个要点：迭代器拷贝是值的拷贝，拷贝后各迭代器独立推进；前缀 `++` 作为表达式会先修改自身、再返回自身。（课件配图对本题的标注与代码逻辑不符，应以代码推演为准。）

## 9. 迭代器分类总览（Slides 48–51）

并非所有迭代器能力相同。所有迭代器都提供四个基本操作：

```cpp
auto it = c.begin();
++it;
*it;
it == c.end()
```

在此之上，多数迭代器还支持更多操作：

```cpp
--it;        // 后退
*it = elem;  // 写入
it += n;     // 随机访问
it1 < it2    // 比较先后
```

这些能力构成一个层级：自底向上为 random access、bidirectional、forward、input，另有独立的 output。下层能力被上层完全包含，级别越高能力越强。

## 10. Input 与 Output Iterator（Slides 52–58）

Input iterator（输入迭代器）是最基础的类别，支持读取元素：

```cpp
auto elem = *it;
```

其典型实例是读取输入流的 `std::istream_iterator`：

```cpp
std::istream_iterator<int> start(std::cin);  // 从 cin 开始读取
std::istream_iterator<int> end;              // 默认构造 = 流结束标记

std::vector<int> numbers(start, end);        // 将输入中的整数读入 vector
```

`start` 绑定到 `std::cin`，`end` 以默认构造表示 end-of-stream，地位相当于 past-the-end。同一过程展开为手动循环：

```cpp
std::istream_iterator<int> it(std::cin); // 指向第一个 int
std::istream_iterator<int> end;          // 默认 = 流结束

while (it != end) {
    std::cout << *it << " ";   // 读取当前值
    ++it;                      // 消费之，前进到下一个
}
```

结构与容器循环一致：`it != end` 判定是否读到底，`*it` 读值，`++it` 前进。

若元素是 struct，可用 `->` 访问其成员；`it->zarf` 与 `(*it).zarf` 完全等价：

```cpp
struct Bibble {
    int zarf;
};

std::vector<Bibble> v {...};
auto it = v.begin();
int m = (*it).zarf;
int m = it->zarf;        // 与上一行完全相同
```

Output iterator（输出迭代器）支持写入元素，方向与读取相反——不是从 `*it` 读出，而是向 `*it` 赋值：

```cpp
*it = elem;
```

实例一为 `std::ostream_iterator`：

```cpp
std::ostream_iterator<int> it(std::cout, ", ");

*it = 10;    // 打印 "10, "
++it;        // 对流而言基本是 no-op
*it = 20;    // 打印 "20, "
++it;
*it = 30;    // 打印 "30, "

// 输出：10, 20, 30,
```

`*it = 10;` 的效果是向 `std::cout` 打印，分隔符 ", " 在构造时给定；`++it` 对流而言近乎空操作，写出它只为与常规迭代器循环保持形式一致。实例二为 `std::back_insert_iterator`：

```cpp
std::vector<int> v;
std::back_insert_iterator<std::vector<int>> it(v);

*it = 10;    // 调用 v.push_back(10)
++it;
*it = 20;    // 调用 v.push_back(20)
++it;
*it = 30;    // 调用 v.push_back(30)

// v 变为 {10, 20, 30}
```

同一句 `*it = ...`，落在不同迭代器上分别表现为打印与插入，体现了迭代器抽象的统一性。

## 11. Forward Iterator 与 multi-pass guarantee（Slides 59–60）

Forward iterator（前向迭代器）是支持多遍遍历（multiple passes）的 input iterator；所有 STL 容器的迭代器均至少属于这一级别。其核心承诺是 multi-pass guarantee：若 `it1 == it2`，则 `++it1 == ++it2` 仍然成立——相等的迭代器保持同步，因而允许对同一序列多次扫描。

不适合多遍的结构是流：输入流"读过即失"，无法回头重读。课件以下例演示复制 stream iterator 的后果：

```cpp
// istream_iterator —— 仅 input
auto it1 = std::istream_iterator<int>(std::cin);
auto it2 = it1;   // 拷贝，但二者面对的是同一条流

++it1;            // 读取并推进流的位置
++it2;            // 流已被推走，it2 处于 undefined state
```

`it2` 是 `it1` 的拷贝，但二者指向同一条流；`++it1` 已使流前进，再执行 `++it2` 时该迭代器进入 undefined state。因此 `istream_iterator` 只能归入 input 级别，达不到 forward。

## 12. Bidirectional 与 Random Access Iterator（Slides 61–64）

Bidirectional iterator（双向迭代器）在 forward 之上支持后退；`std::map` 与 `std::set` 的迭代器属于此级。典型用途是取得最后一个元素：

```cpp
auto it = m.end();

// 取最后一个元素
--it;
auto& elem = *it;
```

`end()` 不可解引用，但 `--it` 可退回到真正的最后一个元素。完整程序如下：

```cpp
std::map<std::string, int> m = {
    {"apple", 1},
    {"banana", 2},
    {"cherry", 3}
};

auto it = m.end();    // end() 指向最后一个元素之后
--it;                 // 退回到实际的最后一个元素
auto& elem = *it;     // 此时可安全解引用
```

Random access iterator（随机访问迭代器）支持快速前后跳转任意步；`std::vector` 与 `std::deque` 的迭代器属于此级：

```cpp
auto it2 = it + 5; // 前移 5
auto it3 = it2 - 2; // 后移 2

// 取第 3 个元素
auto& second = *(it + 2);
auto& second = it[2];
```

`*(it + 2)` 与 `it[2]` 是同一操作的两种写法。这类运算的前提是底层内存连续，跳 n 步即地址加减。越界使用同样危险：

```cpp
std::vector<int> v { 1, 2, 3 };
auto it = v.begin();
it += 3;
int& elem = *it; // Undefined behaviour
```

三个元素的 vector，`it += 3` 恰好到达尾后位置；该位置用于比较（如 `!= end()`）是合法的，但解引用为 undefined behavior，与数组越界同理。

## 13. 迭代器分级的设计动机（Slides 65–67）

分级并非形式上的分类：部分算法对迭代器级别有硬性要求。

```cpp
std::vector<int> vec{1,5,3,4};
std::sort(vec.begin(), vec.end());
// 正确：begin/end 是 random access

std::unordered_set<int> set {1,5,3,4};
std::sort(set.begin(), set.end());
// 错误：begin/end 是 bidirectional
```

`std::sort` 要求 random access iterator：`vector` 的 `begin()/end()` 满足要求，而 `unordered_set` 的迭代器只有 bidirectional 级别，编译失败。遇到此类错误时，应核对算法要求的 iterator category 与容器实际提供的级别。

课件进一步说明了分级的权衡。目标是给所有容器提供统一抽象（uniform abstraction），这正是 range-based for 通吃各类容器的基础；但容器的实现方式决定了哪些操作可以高效完成——前跳 5 步在 sequence 容器（`vector`、`deque`）上代价极低，在 associative 容器（`map`、`set`）的树结构上则没有低成本实现。C++ 的设计取向是不提供"慢"的方法，故 `map::iterator` 干脆不支持 random access。

## 14. 内存与地址（Slides 69–75）

Iterator 指向容器元素，而 pointer 可以指向任意对象。理解指针需要少量内存模型知识：处理器负责运算，RAM 负责存储，二者之间往返传递数据。

三个基本事实。第一，每个变量都存放在内存中的某个位置。第二，所有可能位置的总体构成 address space（地址空间）；程序地址空间的典型布局自高至低为 OS 共享区、栈上的变量、堆上的变量、全局变量、代码段（Text，指令），其中栈向下生长、堆向上生长，二者相向扩张。第三，内存通常按字节编址（byte-addressable），每个字节自 0 起编号，1 byte = 8 bits；64 位系统上编号范围从 `0x0` 直到 `2^64 – 1`。

对象的地址（address）定义为其所占最低字节的编号。int 恒占 32 bits 即 4 字节：

```cpp
int x = 106; // 32 bits
```

若 `x` 的四个字节依次存于 `0x10`、`0x11`、`0x12`、`0x13`，则最低的 `0x10` 即 `x` 的地址。课件脚注指出该演示采用 Big Endian（高位字节置于低地址），实际系统更常见的是 Little Endian；此差别不影响"地址取最低字节"的定义。

## 15. 指针：取地址与解引用（Slides 76–82）

C++ 通过指针获取并使用地址：

```cpp
int x = 106;
int* px = &x;

std::cout << x << std::endl;    // 106
std::cout << *px << std::endl;  // 106
std::cout << px << std::endl;   // 0x50527c
```

`int*` 表示 px 是指向 int 的指针；`&` 是 address-of（取地址）运算符，`int* px = &x;` 即令 px 保存 x 的地址。使用时 `*px` 解引用，按地址找到 x 本身，值为 106；直接输出 px 得到的是地址数值 `0x50527c`。

这一部分的核心结论是：**指针只是个数字**。`int* px` 中存储的就是 `0x50527c` 这一数值，它恰好是 `int x` 四个字节中最低字节的地址。指针并无特殊机制，`*` 只是"按这个数字访问内存"。就概念而言，`int x` 是变量本身，`int* px` 是另一个变量，其值恰为 x 的地址。

## 16. 指向各类对象的指针与 vector 的连续内存（Slides 83–84）

指针可以指向各种对象。指向 int：

```cpp
int x = 106;
int* px = &x;
```

指向自定义类型对象，并以 `->` 访问成员：

```cpp
StanfordID id { "rfern" };
StanfordID* p = &id;
auto name = p->name;
```

指向整个容器：

```cpp
std::vector<int> v;
std::vector<int>* p = &v;
```

指向容器内的元素：

```cpp
std::vector<int> v {
    1, 2, 3, 4, 5
};
int* arr = &v[0];
```

最后一例成立的原因是 vector 是一整块连续内存（尾部留有预留空位）；取得首元素地址后，这段内存的使用方式与原生数组无异。

## 17. 指针运算与迭代器接口的对应（Slides 85–90）

对上述指针施加一系列操作：

```cpp
std::vector<int> v {1,2,3,4,5};

int* arr = &v[0];              std::cout << *arr << " ";
arr += 1;                      std::cout << *arr << " ";
++arr;                         std::cout << *arr << " ";
arr += 2;                      std::cout << *arr << " ";
if (arr == &v[4])              std::cout << "At last index";
```

输出为：

```text
1  2  3  5  At last index
```

从 `&v[0]` 出发，依次到达下标 1、2、4，最终与 `&v[4]` 相等。为各行标注操作类别：

```cpp
int* arr = &v[0];       // Initialization
arr += 1;               // Random access
++arr;                  // Move pointer forward
arr += 2;               // Random access
if (arr == &v[4])       // Pointer comparison
```

初始化、随机访问、前进、比较——同一过程可用迭代器原样重演：

```cpp
auto it = v.begin();
std::cout << *it << " ";
it += 1;
std::cout << *it << " ";
++it;
std::cout << *it << " ";
it += 2;
std::cout << *it << " ";
if (it == --v.end())
std::cout << "At last element";
```

两段代码逐行对应，行为一致；指针版本的 `&v[4]` 对应迭代器版本的 `--v.end()`——利用 bidirectional 能力从尾后位置退回最后一个元素再作比较。

这种对应并非巧合。`iterator` 是容器内的类型别名：

```cpp
template <typename T>
class vector {
    using iterator = /* some iterator type */;

    // Implementation details...
};
```

对 `vector` 而言，该别名背后的类型在概念上就是 `T*`：

```cpp
template <typename T>
class vector {
    using iterator = T*;
    // Implementation details...
};
```

课件同时说明：真实 STL 实现中该类型并非字面上的 `T*`，但就一切实际用途而言可以这样理解。本讲标题并置两个概念的原因由此明确：iterators have a similar interface to pointers——迭代器与指针共享同一套操作接口；指针是通用的地址数值，迭代器是容器语境下的位置标记。

## 18. 练习、回顾与后续（Slides 92–96）

课件提供了配套在线练习：<https://106b.vercel.app/iterators>。本讲内容归纳为三点：Iterator Basics，迭代器支持逐步前向遍历容器；Iterator Types，input、output、forward、bidirectional、random access 的能力分级；Pointers and Memory，指针指向内存中任意 C++ 对象，且指针与迭代器具有相同的接口。

本讲留下一个开放问题：`vector` 的迭代器可视为 `T*`，那么

```cpp
template <typename K, typename V>
class map {
    using iterator = ???????;

    // Implementation details...
};
```

`map` 底层是二叉搜索树，裸指针无法表达"按序的下一个节点"这一概念。解决该问题需要自定义类型的能力；类（classes）将在下一讲讨论。

## 本讲要点

- range-based for 是迭代器循环的语法糖，展开为 `for (auto it = c.begin(); it != c.end(); ++it)`；各类容器均通过提供 `begin()`/`end()` 与迭代器接口接入该语法。
- `end()` 是 past-the-end 迭代器，永不指向元素；容器为空时 `begin() == end()`；解引用 `end()` 是 undefined behavior。
- 迭代器按能力分级：input（读）、output（写）、forward（multi-pass，所有 STL 容器迭代器至少属于此级）、bidirectional（`map`/`set`，可 `--it`）、random access（`vector`/`deque`，可 `it + n`、`it[n]`）；`std::sort` 等算法对迭代器级别有硬性要求。
- 迭代器拷贝是值拷贝，拷贝后各迭代器独立推进；应优先写前缀 `++it`：前缀形式返回引用、不产生拷贝，后缀形式必须拷贝旧值。
- 指针是保存地址的数值，`&` 取地址、`*` 解引用，可指向任意对象；`vector` 内存连续，其 `iterator` 在概念上等价于 `T*`，故指针运算与迭代器操作一一对应。
