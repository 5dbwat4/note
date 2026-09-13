---
title: "Lecture 05 · Containers 逐字稿"
createAt: 2026/9/13
---

# Lecture 05: Containers（逐字稿）

> 对应课件转写：[2026Spring-05-Containers.md](../output/2026Spring-05-Containers.md)

## 1. 本讲结构

本讲主题为 Containers（容器），由 Preston Seay 与 Rachel Fernandez 主讲。全讲依次讨论四个主题：其一，space-time，即空间与时间之间的权衡思想；其二，STL（Standard Template Library，标准模板库）；其三与其四，两大类容器——sequence containers（序列容器）与 associative containers（关联容器），末尾附带介绍 unordered associative containers（无序关联容器）。容器是后续作业乃至整门课程的基础设施，本讲建立的概念框架将在全课程中反复出现。

## 2. 复习： stringstream 与流继承体系

课件以两页内容衔接上一讲，围绕一个问题展开：stringstream 是否是一个 istream？是否是一个 ostringstream？结论是两者皆然。流继承图中，顶层的 ios 组合了一个 streambuf；ios 派生出 istream 与 ostream 两条支线；iostream 同时继承 istream 与 ostream；而 stringstream 位于 iostream 之下，因而兼具输入与输出两种身份。

上一讲的示例代码可以验证这一结论：

```cpp
#include <iostream>
#include <sstream>
#include <string>
int main() {
    std::stringstream ss;
    ss << 3.14f << ' ' << "hello"; // use as ostream

    float pi; std::string hi;
    ss >> pi >> hi; // use as istream

    std::cout << pi << '\n' << hi << std::endl;
}
```

同一个 `ss` 对象先经 `<<` 被当作 ostream 写入数据，再经 `>>` 被当作 istream 读出数据：一个对象承担两种角色，依据正是继承体系。这种"以复用消除重复"的思路，恰好引出本讲的主题——如何让同一份代码适配任意类型。

## 3. Space-time: 空间与时间的权衡

在进入具体容器之前，课件借助一个日常类比确立本讲的核心思想。任务是"去车库里取一把扳手"：若割草机、千斤顶、零件与纸箱尽数堆在地面，寻找扳手只能逐一翻检；若车库经过整理，货架与挂架使每件工具各有其位，取用便一目了然。类比还包含第二层含义——how much stuff（东西有多少）：物品堆放越满，寻找越慢；留出的空余空间使人看得清、走得动，空间本身就是一种换取时间的资源。

Bjarne Stroustrup 将这一思想概括为一句话："Space is time."（空间即时间。）多付出一些空间去组织数据，便能节省大量检索时间。

落实到数据结构，课件给出如下对照：

- Disorganized（无组织，类比散乱的纸堆）：空间高效，但检索慢。例子是 vector——元素紧密相邻，不浪费任何字节，查找却只能从头扫描；
- Organized（有组织，类比贴有标签的档案柜）：额外消耗空间维持结构，但检索快。例子是 map。

整讲的主旋律由此确立：每种容器本质上都是空间与时间之间的一种 tradeoff（权衡）。

## 4. STL: Standard Template Library

第二个主题是 STL。STL 与 C++ 标准库并不等同：C++ Standard Library 是一个整体，其中包含 streams、strings、math 等诸多组件；STL 只是其中的一个子集，内部由四部分组成——Containers（容器）、Iterators（迭代器）、Functors（函数对象）与 Algorithms（算法）。本讲讨论的容器即 STL 的第一个组成部分。STL 由 Alexander Stepanov 设计；标准算法所在的头文件 `#include <algorithm>` 即源自其工作。

## 5. template 的动机： 消除按类型复制的重复代码

STL 名称中的 template（模板）一词指向一个具体的工程问题。假设需要一个列表类：存 int 时写 IntList，存 string 时写 StringList，存 double 时写 DoubleList，此外还有 FloatList、BoolList、CharList——每个类型都要抄写一份几乎完全相同的代码。模板正是为消除这种重复而设计：将类型抽象为占位符，只写一份泛型代码：

```cpp
// You'll learn more wk 5!
template <typename T>
class Vector {
    ...
};
```

`T` 即类型占位符，编译器依据使用方式自动生成各个具体版本。标准库因此提供了如下写法：

```cpp
#include <vector>

int main() {
    std::vector<int> ints;
    std::vector<double> dbls;
    std::vector<std::string> strs;

    ints.push_back(1);
    dbls.push_back(5.4);
    strs.push_back("hi");
    std::cout << ints[0] + dbls[0];
}
```

同一份 vector 模板实例化出分别容纳 int、double 与 std::string 的三种容器。模板的完整语法将在第五周专门讲授，此处只需建立直观认识。

## 6. Sequence Containers 与 std::vector

第三部分进入 sequence containers。其定义为："Sequence containers implement data structures which can be accessed sequentially."（序列容器实现可按顺序访问的数据结构。）换言之，它们容纳的就是序列。课件同时给出 cppreference 的容器总览页（<https://en.cppreference.com/w/cpp/container.html>），该站点是查阅容器行为的权威参考。常见的序列容器有四种：vector、deque、array 与 list，本讲重点讨论前两种。

vector 的定义是 "A resizable contiguous array"（可变长的连续数组）：一排紧密相邻的存储单元，单元下方标注下标 0、1、2……连续排布是其最重要的物理特征。

```cpp
#include <vector>
#include <iostream>
int main() {
  std::vector<int> vec { 1, 2, 3, 4 };
  vec.push_back(5);
  vec.push_back(6);
  vec[1] = 20;

  for (size_t i = 0; i < vec.size(); i++) {
    std::cout << vec[i] << " ";
  }
}
```

逐行分析：首行以 uniform initialization（统一初始化）放入 1 至 4；两次 `push_back` 将 5 与 6 追加至末尾，体现 "resizable"；`vec[1] = 20` 改写下标 1 处的元素，容器内容由 `{1,2,3,4,5,6}` 变为 `{1,20,3,4,5,6}`；末尾以下标循环遍历打印全部元素。由于内存连续，按位置访问只需一次地址偏移计算即可完成，这是 contiguous array 的核心优势。

## 7. 越界访问与 zero-overhead principle

vector 的便利伴随使用上的责任。将上述循环条件由 `i < vec.size()` 改为 `i < 10`，而容器中仅有 6 个元素：

```cpp
#include <vector>
#include <iostream>
int main() {
    std::vector<int> vec { 1, 2, 3, 4 };
    vec.push_back(5);
    vec.push_back(6);
    vec[1] = 20;

    for (size_t i = 0; i < 10; i++) {
        std::cout << vec[i] << " ";
    }
}
```

`operator[]` 不执行任何边界检查，循环越界后会继续向后访问内存，其结果属于未定义行为。课件将其归纳为三点：be careful with indices（谨慎对待下标）；`[]` 不检查；`.at()` 检查——`.at()` 执行边界检查，越界时抛出异常报错，而 `[]` 是不含额外开销的裸访问。

C++ 之所以默认不检查，依据的是 zero-overhead principle（零开销原则），其表述为两条：

1. You don't pay for what you don't use.（不为未使用的功能付出代价。）
2. What you do use is just as efficient as what you could reasonably write by hand.（所使用的功能，与手写实现同样高效。）

需要安全性时显式选用 `.at()` 并承担检查的代价；追求性能时 `[]` 不含任何多余开销。这一原则是 C++ 区别于许多语言的根本设计取向。

## 8. 扩容机制： dynamic reallocation

越界之外，vector 的另一处隐性成本发生在变长时。课件的表述是：Resizing vectors copies over the whole array into a bigger array——扩容时申请一块更大的数组，将原数组的全部元素拷贝过去，称为 dynamic reallocation（动态重分配）。"整体搬移"意味着元素越多，单次扩容越昂贵；这也是 vector 插入、删除较慢的一个来源。课件为该过程提供了可视化页面。

## 9. Stanford Vector 与 std::vector 的语法对照

在实现层面，Stanford 课程库的 `Vector` 与标准库的 `std::vector` 存在语法差异，课件给出对照表如下：

| 操作 | Stanford `Vector<int>` | `std::vector<int>` |
| :--- | :--- | :--- |
| 创建空容器 | `Vector<int> v;` | `std::vector<int> v;` |
| 创建 n 个 0 | `Vector<int> v(n);` | `std::vector<int> v(n);` |
| 创建 n 个 k | `Vector<int> v(n, k);` | `std::vector<int> v(n, k);` |
| 尾部加入 k | `v.add(k);` | `v.push_back(k);` |
| 清空 | `v.clear();` | `v.clear();` |
| 判空 | `v.isEmpty()` | `v.empty()` |
| 读取下标 i | `v.get(i);` / `v[i];` | `v.at(i);` / `v[i];` |
| 改写下标 i | `v.get(i) = k;` / `v[i] = k;` | `v.at(i) = k;` / `v[i] = k;` |

该表宜作速查之用：创建部分两者几乎一致，差异集中在方法命名上。

## 10. 例题与解析： findPeakHeat

题目：编写 C++ 函数求 vector 中的最大值，要求使用 4 种不同的 vector 方法。给定未来七天的最高气温预报 `{82, 95, 102, 99, 88, 79, 81}`，求本周峰值温度。代码框架如下：

```cpp
#include <iostream>
#include <vector>

/* Returns highest temperature,
   or -1 if no temperatures given. */
int findPeakHeat(const std::vector<int>& temps) {
    // Your implementation here
}

int main() {
    // High temperatures forecast for the next 7 days.
    std::vector<int> weeklyForecast = {82, 95, 102, 99, 88, 79, 81};

    std::cout << "--- Weather Report ---" << std::endl;
    std::cout << "Max temp this week will be " << findPeakHeat(weeklyForecast) <<
                 std::endl;
    return 0;
}
```

解析：注释约定无数据时返回 -1，故第一步以 `empty()` 判空并按约定返回 -1；随后以一个变量记录当前最大值，以 `size()` 取得元素个数，经 `operator[]` 或 `.at()` 逐个访问，边遍历边更新，遍历结束后返回该最大值——`size()`、`empty()`、`operator[]`、`.at()` 恰好构成题目要求的 4 种方法。参数类型 `const std::vector<int>&` 同样值得注意：按 const 引用传参既避免整个 vector 被拷贝，又保证函数不会修改调用者的数据，应作为此类函数的默认写法。

## 11. vector 的插入代价与 std::deque

vector 的另一处局限在插入：向中间插入一个元素，其后所有元素必须整体后移一位，"紧密相邻"的布局正是这一代价的来源。

若应用恰恰需要两端频繁插删，标准库提供了 deque（double-ended queue，双端队列，读作 "deck"）。它具备 vector 的 `push_back` 与 `pop_back`，同时另有 `push_front` 与 `pop_front`，即头尾两端均可高效插入与删除。

典型用例是维护最近 10000 条价格记录：

```cpp
#include <deque>

void receivePrice(deque<double>& prices, double price)
{
    prices.push_front(price);    // Super fast
    if (prices.size() > 10000)
        prices.pop_back();       // Remove last price
                                // so we don't exceed 10k
}
```

每条新价格经 `push_front` 进入头部（注释标注 Super fast）；数量一旦超过一万条，即以 `pop_back` 移除最旧的一条。新数据自头进入、旧数据自尾离开，两个方向都落在 deque 擅长的位置，容器规模恰好稳定在一万条以内。此类"滑动窗口"模式常见于行情、日志等场景；若改用 vector，每次头部插入都需搬动整个数组，开销完全不在同一量级。至于 deque 内部如何做到两端皆快——其存储并非一整块连续内存，课件为此同样提供了可视化页面。

## 12. Associative Containers 与 std::map

第四部分转向 associative containers，其定义为："Associative containers implement **sorted** data structures that can be **quickly searched**."（关联容器实现已排序、可快速检索的数据结构。）两个关键词是 sorted 与 quickly searched；第 3 节对照中 organized 一方（map）正属于此类。课件以示意图归类：sequence containers 对应 vectors 与 deques，associative containers 对应 maps 与 sets。

map "contains key-value pairs with unique keys"（容纳键不重复的键值对）；Python 中的对应物称为 dictionary。

```cpp
std::map<int, char*> adjs;
adjs[106] = "awesome";
adjs[103] = "mathy";
adjs[107] = "deep";

std::cout << adjs[106];
```

以课程编号为 key、形容词为 value，方括号内写 key 即可存取，书写体验与数组几乎一致。这种访问之所以高效，原因在于 map 将所有 pair 按 key 排序：在有序结构上定位无需从头线性扫描。

更完整的示例：

```cpp
#include <map>
#include <iostream>
int main () {
    std::map<int, char> preston {
        {16, 'p'}, {18, 'r'}, {5, 'e'},
        {19, 's'}, {20, 't'}, {15, 'o'}, {14, 'n'}
    };
    for (const auto& pair : preston) {
        std::cout << pair.first << ' '
                  << pair.second << std::endl;
    }
}
```

对此有三点观察。其一，map 本质上是 pair 的集合，花括号中的 `{16, 'p'}` 等即 pair 的 uniform initialization。其二，range-based for 每轮取出一个 pair，以 `pair.first` 取 key、`pair.second` 取 value。其三，插入顺序杂乱，输出却严格按 key 从小到大排列——排序是 map 的固有行为，无需任何额外操作。

## 13. pair 遍历与 structured binding

map 的元素类型为 pair 这一事实，直接决定遍历时的取值写法。课件指出，`std::map<K, V>` 中存储的是 `std::pair<const K, V>`：key 一侧为 const，因为改写 key 会破坏容器的有序性。传统写法为：

```cpp
for (const auto& pair : myMap) {
  auto key = pair.first;
  auto value = pair.second;
}
```

更现代的写法是 structured binding（结构化绑定），将 pair 一步解包为两个独立的名字：

```cpp
for (const auto& [key, value] : myMap) {

}
```

语义不变，表达更为简洁。

## 14. map 的底层存储： red-black tree

上述有序语义由底层存储结构保证。map 将 pair 存入 binary search tree（BST，二叉搜索树），且具体采用 red-black tree（红黑树）——一种自平衡的 BST。BST 的性质使查找每深入一层即排除一半候选；自平衡机制则保证树不会退化，红黑树承诺树的最大深度不超过 2 log(n)，因此检索复杂度为 O(log(n))。这便是 "sorted, quickly searched" 的实现基础。

## 15. operator[] 的自动插入行为与 std::set

map 的 `operator[]` 还有一项容易出错的语义。考察以下代码：

```cpp
std::map<std::string, int> fav_num;
fav_num["Preston"] = 2;

std::cout << "Preston's is " << fav_num["Preston"] <<
    " and Rachel's is " << fav_num["Rachel"] << '\n';
```

`"Rachel"` 从未被插入过，而 `fav_num["Rachel"]` 的结果并非错误：map 自动插入该 key，并以该类型的 default value（默认值，对 int 为 0）作为 value，故输出为 "Rachel's is 0"。课件进一步指出，这一行为在每次使用 `operator[]` 时都会发生，包括第二行赋值语句本身——访问即可能插入。其便利与风险并存：key 拼写错误不会报错，而是悄然产生一个带默认值的条目。

set（集合）可视为 map 的无值版本：课件称其为 maps without values，其中保存不重复的对象（unique objects）。没有 value，只剩 key，其余行为与 map 一致，插入、检索、删除同为对数复杂度；适用于只关心"是否存在"而不关心对应值的场景。课件为此提供了 set 的可视化页面。

## 16. 语法速查： Stanford Map/Set 与标准容器

与 vector 一节相同，Stanford 库的 Map/Set 与标准版本也存在语法差异。map 部分：

| 操作 | Stanford `Map<char, int>` | `std::map<char, int>` |
| :--- | :--- | :--- |
| 创建空容器 | `Map<char, int> m;` | `std::map<char, int> m;` |
| 插入 key k 与值 v | `m.put(k, v);` / `m[k] = v;` | `m.insert({k, v});` / `m[k] = v;` |
| 删除 key k | `m.remove(k);` | `m.erase(k);` |
| 判断 k 是否存在（* C++20） | `m.containsKey(k)` | `m.count(k)` / `m.contains(k) (*)` |
| 判空 | `m.isEmpty()` | `m.empty()` |
| 读取或覆盖 k 对应的值（不存在则自动插入默认值） | `int i = m[k];` / `m[k] = i;` | `int i = m[k];` / `m[k] = i;` |

set 部分与之对应：`s.add(k)` 对 `s.insert(k)`，`s.remove(k)` 对 `s.erase(k)`，成员判断为 `s.count(k)` 或 C++20 起的 `s.contains(k)`，判空为 `s.empty()`。表中特意标注：`m[k]` 在 key 不存在时自动插入默认值，两个版本行为一致，即第 15 节所述语义。

## 17. 例题与解析： findDoubleAgents

题目：某公司有若干部门，员工可能同时隶属多个部门；找出这些 double agents——出现在多个部门中的人。代码框架如下：

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>

std::set<std::string> findDoubleAgents(std::map<std::string, std::set<std::string>> departments) {
    std::set<std::string> seen, doubleAgents;

    // Your code here

    return doubleAgents;
}

int main() {
    std::map<std::string, std::set<std::string>> company = {
```

解析：函数签名已给出结构——参数是从部门名映射到该部门成员集合的 `std::map<std::string, std::set<std::string>>`，返回值为装有多部门成员姓名的 `std::set<std::string>`；框架中已声明 `seen` 与 `doubleAgents` 两个 set。算法为：遍历每个部门的每一名成员，若该姓名已在 `seen` 中，则其至少属于两个部门，加入 `doubleAgents`；否则插入 `seen`。成员判断只需调用 `count` 或 `contains`，即可在对数时间内得到"是否见过"的答案，全程无需编写任何检索逻辑——这正是 associative containers 的设计目的所在。

## 18. multiset、multimap 与可比较性要求

此前均默认 map 的 key 唯一。若需要重复的 key，associative containers 家族另有两个成员：multiset（允许重复 key 的集合）与 multimap（key 可重复的键值对集合）。连同 set 与 map，四者共享同一特征：sorted、quickly searched、O(log n)。

随之而来的一个 caveat（注意点）是：这些容器如何完成排序？std::map 在头文件 `<map>` 中的完整模板声明为：

```cpp
template<
    class Key,
    class T,
    class Compare = std::less<Key>,
    class Allocator = std::allocator<std::pair<const Key, T>>
> class map;
```

日常使用只需提供前两个模板参数，因为后两个带有默认值。第三个参数 `Compare` 默认为 `std::less<Key>`：容器假定 key 之间可以比较大小，并默认以"小于"比较器维持排序——排序得以完成的机制正在于此。第四个参数 `Allocator` 负责内存分配方式，此处暂不展开。

由此暴露出关联容器的使用门槛：并非所有类型都能默认比较。`int`、`double`、`string` 天然可比较；`ifstream` 或自定义类型（如 `Course`）则不然——两个输入流之间不存在有意义的顺序。将自定义类型放入有序关联容器之前，必须先解决可比较性问题。

## 19. Unordered associative containers 与哈希

有序关联容器依赖比较，计划表的最后一项——unordered associative containers——则将"有序"前提整个移除。cppreference 将容器库分为三类：sequence containers、associative containers，以及 C++11 起引入的 unordered associative containers。这一族将 map 与 set 各自去掉有序属性：map 对应 unordered_map，set 对应 unordered_set，可视为二者的优化版本。

两者在用法上的差异仅在于类型名，课件称其为 drop-in replacement（即插即用的替换）：

```cpp
std::map<int, std::string> courses{
  {103, "Bailey/Aiken"},
  {107, "Cain"},
  {109, "Gregg"}
};
```

```cpp
std::unordered_map<int, std::string> courses{
  {103, "Bailey/Aiken"},
  {107, "Cain"},
  {109, "Gregg"}
};
```

既然不排序，快速检索依赖的是 hash（哈希）。`std::unordered_map` 在头文件 `<unordered_map>` 中的模板声明为：

```cpp
template<
    class Key,
    class T,
    class Hash = std::hash<Key>,
    class KeyEqual = std::equal_to<Key>,
    class Allocator = std::allocator<std::pair<const Key, T>>
> class unordered_map;
```

与 map 的声明对照即一目了然：`Compare = std::less<Key>` 在此被替换为 `Hash = std::hash<Key>` 与 `KeyEqual = std::equal_to<Key>`——不再要求"小于"比较，改为要求哈希函数与相等判断。

hash function（哈希函数）的定义包含两点：其一，将 key "打乱"（scramble）为一个 `size_t`（64 位）；其二，输入的微小变化应引起输出的巨大变化。课件的示例同时展示了确定性：字符串 "CS106L" 两次经过同一函数 f(x)，均得到 80489869——相同输入必得相同输出，这是能够取回数据的前提；而仅差一个字符的 "CS106B" 哈希为截然不同的 31580239，这种雪崩效应使键值均匀分布。

unordered_map 的底层结构即 hash table（哈希表）：key 经哈希函数计算得到位置，直接落入对应的桶，检索无需任何比较与遍历，此即平均 O(1) 的来源。不同 key 偶尔会哈希到同一位置，其处理方式可见课件提供的可视化页面。

## 20. 检索复杂度对比与容器总结

至此可将本讲涉及的容器的检索速度并列比较：

| Container | 检索复杂度 |
| :--- | :--- |
| Vectors | O(n) |
| Maps | O(log(n)) |
| Unordered Maps | O(1) |

unordered_map 本质上是 map 的提速版本，平均常数时间检索的代价是不再保序；且如同 map 要求 key 可比较，它要求 key 可哈希。

总结环节给出六种容器的横向对比，表格左侧的竖直箭头标注 space per element（每元素空间），越向下占用越多：

| | 第 i 个元素 | Search | Insertion | Erase |
| :--- | :---: | :---: | :---: | :---: |
| **std::vector** | Very Fast | Slow | Slow | Slow |
| **std::deque** | Fast | Slow | Fast（头尾）/ Slow（其余） | Fast（头尾）/ Slow（其余） |
| **std::set** | Slow | Fast | Fast | Fast |
| **std::map** | Slow | Fast | Fast | Fast |
| **std::unordered_set** | N/A | Very Fast | Very Fast | Very Fast |
| **std::unordered_map** | N/A | Very Fast | Very Fast | Very Fast |

这张表浓缩了整讲主旨：空间投入越多、组织越充分，操作越快。选型的路径亦随之清晰：需要按位置访问，选 vector/deque；需要保序的快速检索，选 map/set；检索速度优先且可放弃顺序，选 unordered 一族；同时须记得表中每行左侧的空间代价是实际支出。不存在普遍最优的容器，只有与场景匹配的容器。

课件最后列出 cppreference 的容器全景，可作后续查阅的索引：sequence containers 中还有 C++11 的 `array`、`forward_list` 以及 `list`，乃至 C++26 的 `inplace_vector` 与 `hive`；container adaptors（容器适配器）在序列容器之上提供 `stack`、`queue`、`priority_queue`，C++23 另有 `flat_map`、`flat_set` 等一族；associative containers 为 `set`、`map`、`multiset`、`multimap`；C++11 起的 unordered 一族为 `unordered_set`、`unordered_map` 及其 multi 版本。此图无需记忆，查阅 cppreference 即可——从既有容器中选取合适的工具，远胜于自行实现。

归纳全讲的四条主线：其一，space-time，数据结构的核心是空间与时间的权衡；其二，STL，标准库中包含 Containers、Iterators、Functors、Algorithms 的部分；其三，sequence containers，代表为 `vector` 与 `deque`；其四，(unordered) associative containers，代表为 `map`、`set` 及其 unordered 版本。

## 本讲要点

- 数据结构的核心权衡是 space-time：vector 省空间但检索慢，map/set 以额外空间换取 O(log n) 的快速检索——"Space is time."
- STL 是 C++ 标准库的子集，由 Containers、Iterators、Functors、Algorithms 四部分组成；容器皆为 template，一份代码经实例化适配任意类型。
- std::vector 是 resizable contiguous array：`operator[]` 不做边界检查，`.at()` 做检查并在越界时抛异常，体现 zero-overhead principle；扩容经由 dynamic reallocation 整体搬移，中间插入需移动后续全部元素。
- std::deque 两端均可 push/pop，适用于"维护最近 N 条记录"式的双端操作场景。
- std::map/set 底层为 red-black tree（自平衡 BST），检索 O(log n)；key 须能被 `Compare`（默认 `std::less`）比较；`operator[]` 访问不存在的 key 会自动插入默认值，须格外当心。
- std::unordered_map/set 以 hash table 实现，平均 O(1)，是 map/set 的 drop-in replacement；模板参数由 Compare 换为 `std::hash` 与 `std::equal_to`，代价是不保序且要求 key 可哈希。
