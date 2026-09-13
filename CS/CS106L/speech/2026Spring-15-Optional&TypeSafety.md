---
title: "Lecture 15 · std::optional & Type Safety 逐字稿"
createAt: 2026/9/13
---

# Lecture 15: std::optional & Type Safety（逐字稿）

> 对应课件转写：[2026Spring-15-Optional&TypeSafety.md](../output/2026Spring-15-Optional&TypeSafety.md)

## 1. 本讲定位与知识脉络（Slides 1–4）

本讲承接上一讲关于 move semantics 的讨论，主题转向 type safety（类型安全）与 `std::optional`。课件将本讲内容分为三个部分：首先复习 move semantics 与资源管理的三条规则（Rule of Zero、Rule of Three、Rule of Five）；随后借助具体代码引出 type safety 的概念，并逐层深化其定义；最后引入 `std::optional`，考察它在多大程度上能把"可能没有结果"这一事实纳入函数签名，从而改善程序行为的可保证性。这一安排并非题材的简单拼凑：复习部分所关注的核心问题——谁负责管理资源、谁负责保证前置条件——正是后文 type safety 讨论的主线。

## 2. 复习：move semantics（Slides 5–7）

move semantics 的存在理由是：有时待获取的资源已不再被原所有者需要，此时应当转移而非复制资源。课件以下例说明。

```cpp
#include <iostream>
#include <vector>
#include <utility> // for std::move

int main() {
    std::vector<int> a = {1, 2, 3};

    // We no longer need 'a', so let's move it into 'b'
    std::vector<int> b = std::move(a);

    std::cout << "a.size() = " << a.size() << "\n"; // 0
    std::cout << "b.size() = " << b.size() << "\n"; // 3
    return 0;
}
```

`std::move(a)` 的作用是将表达式 `a`——一个 l-value——转换为 r-value，使重载决议选择移动构造，从而 `b` 立即接管 `a` 的内部缓冲区；移动完成后 `a.size()` 变为 0，`b` 拥有原来的 3 个元素。需要强调，`std::move` 本身并不执行移动，它只完成值类别的转换，真正的资源转移发生在随后被选择的移动构造函数或移动赋值运算符之中。

## 3. 复习：Rule of Zero（Slides 8–9）

Rule of zero：如果成员变量能够自我管理（self-managing），且无需自定义构造函数与运算符，那么就不要手写这些特殊成员函数。课件给出如下 `Student` 类。

```cpp
#include <string>
#include <vector>

class Student {
public:
  // We don't write:
  // - destructor
  // - copy constructor
  // - copy assignment operator
  // - move constructor
  // - move assignment operator

  // Why? Because std::string and std::vector manage themselves!
  Student(std::string name, std::vector<int> scores)
    : name_(std::move(name)), scores_(std::move(scores)) {}

private:
  std::string name_;        // self-managing
  std::vector<int> scores_; // self-managing
};
```

成员 `name_` 与 `scores_` 的类型 `std::string` 与 `std::vector` 自行管理其资源，因此五个特殊成员函数均可交由编译器生成。在不自定义的前提下，C++ 自动提供它们，签名依次为：析构函数 `~Student();`、拷贝构造 `Student(const Student& other);`、拷贝赋值 `Student& operator=(const Student& other);`、移动构造 `Student(Student&& other);`、移动赋值 `Student& operator=(Student&& other);`。对这样的类，编译器生成的版本已能正确完成深拷贝与移动；构造函数按值传参并以 `std::move` 转入成员，是同时覆盖拷贝与移动两种来源的常用写法。

## 4. 复习：Rule of Three 与 Rule of Five（Slides 10–13）

一旦成员不再是自我管理的对象，情形即发生变化。Rule of three 指出：如果类定义了自定义析构函数，那么它还需要同时定义自定义拷贝构造函数与拷贝赋值运算符。课件将 `Student` 的成员换成裸指针 `int* scores_;`（经由 `new int[numScores]` 分配），此时析构必须释放数组，拷贝必须深拷贝。

```cpp
class Student {
public:
    Student(const std::string& name, int numScores)
        : name_(name), numScores_(numScores), scores_(new int[numScores]) {}

    // 1. Destructor - must free the array
    ~Student() {
        delete[] scores_;
    }

    // 2. Copy constructor - deep copy the array
    Student(const Student& other)
        : name_(other.name_), numScores_(other.numScores_) {
        scores_ = new int[numScores_];       // allocate
        for (int i = 0; i < numScores_; i++) // deep copy
            scores_[i] = other.scores_[i];
    }
};
```

拷贝赋值运算符则须先防范自赋值（self-assignment），再释放旧资源、复制非资源字段并深拷贝数组。

```cpp
// 3. Copy assignment - deep copy + avoid self-assignment
Student& operator=(const Student& other) {
    if (this != &other) {
        delete[] scores_;

        name_ = other.name_;
        numScores_ = other.numScores_;

        scores_ = new int[numScores_];
        for (int i = 0; i < numScores_; i++)
            scores_[i] = other.scores_[i];
    }
    return *this;
}
```

若上述三者不齐备，编译器生成的逐成员浅拷贝将使两个对象共享同一块 `int` 数组，析构时产生双重释放。Rule of five 在此基础上提出：既然已经自定义了拷贝构造与拷贝赋值，还应当提供移动构造与移动赋值。课件给出的实现遵循统一模式——移动构造直接接管 `other.scores_` 指针，随后将源对象置空。

```cpp
// Move constructor
Student(Student&& other)
: name_(std::move(other.name_)),
numScores_(other.numScores_),
scores_(other.scores_) {
other.scores_ = nullptr;
other.numScores_ = 0;
}
```

```cpp
// Move assignment
Student& operator=(Student&& other) {
if (this != &other) {
delete[] scores_;

name_ = std::move(other.name_);
numScores_ = other.numScores_;
scores_ = other.scores_;

other.scores_ = nullptr;
other.numScores_ = 0;
}
return *this;
}
```

移动赋值在接管之前先 `delete[]` 自身旧资源，并以 `this != &other` 防范自赋值；接管后将源指针置为 `nullptr`、计数清零，保证源对象可被安全析构。这条复习线索同时为后文作了铺垫：手工编写这些函数的繁复，恰是"优先使用自我管理类型"这一立场（以及标准库整体设计）的价值所在。

## 5. type safety 的定义与语言对比（Slides 15–18）

课件给出的第一个定义是：type safety 指一门语言防止类型错误（typing errors）的程度。为说明其含义，课件对比了同一算法在两种语言中的表现。

例题：考虑以下两段代码，均以字符串实参调用"除以三"的函数。

Python:

```python
def div_3(x):
    return x / 3

div_3("hello")  # CRASH during runtime, can't divide a string
```

C++:

```cpp
int div_3(int x){
    return x / 3;
}
div_3("hello") // Compile error: this code will never run
```

解析：Python 版本能顺利通过编译（解释）阶段，类型错误被推迟到运行时才暴露，程序以异常崩溃；C++ 版本中，字符串字面量无法转换为 `int` 形参，编译器直接拒绝该程序，这段代码永远不会运行。前者把类型错误留给运行时，后者在编译期即予以阻止——这正是两种语言在 type safety 维度上的差异。

课件随后给出一个现实背景作为映照：火星探测任务中，1 Earth Year 为 365 天，而 1 Mars Year 为 687 个 Earth days，即 669 个火星日（sols）。"天数"在不同度量体系下并不可以互换，把名义上同为数值的量混用，正是一类现实失败的典型根源；这也说明"类型"的概念远不止整数与字符串之分。据此，课件将定义修订为：type safety 指一门语言保证程序行为（the behavior of programs）的程度。

## 6. 引例：查找函数的返回类型问题（Slides 19–20）

课件提出如下设计问题：对于函数

```cpp
??? f(vector<int> vec, int value);
```

按测试用例，其应返回 `value` 在 `vec` 中首次出现处的下标：

```text
f({1, 3, 7}, 3) == 1                              (index 1)
f({67}, 67) == 0                                  (index 0)
f({106, 107, 111, 143, 144, 149}, 111) == 2       (index 2)
```

由前三条例子看，返回 `int` 似乎即可。然而第四条例子 `f({}, 10)` 迫使设计者直面空输入：当 `value` 不存在时应当返回什么？无论选取 -1 还是其他哨兵值，该约定都只存在于文档层面——签名 `int f(...)` 本身完全不表达"可能找不到"。返回类型占位符 ??? 由此悬置；下文先通过一个更日常的函数，暴露这类签名问题的实际后果。

## 7. 例题与解析：removeOddsFromEnd 与空 vector（Slides 21–28）

例题：分析如下函数的行为（课件注明该例出自 foonathan.net 的 Jonathan Müller）。

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

其中 `vector::back()` 返回指向末元素的引用；`vector::pop_back()` 移除末元素，与 `vector::push_back(elem)` 互为逆操作。

解析：该函数意图删除位于末尾的连续奇数。若末尾元素全为奇数，循环会把 `vector` 逐个清空，随后对空 `vector` 调用 `back()`——问题正在于此。库文档对 `std::vector::back` 的说明附有明确警告：对空容器调用 `back` 导致 undefined behavior（未定义行为）。UB 意味着该函数可能崩溃、可能产生垃圾值，也可能碰巧返回某个看似合理的值——语言与库对此不作任何承诺。因此课件断言：对这个函数的行为无法作出任何保证。

一种修复方式是：

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(!vec.empty() && vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

由于 `&&` 的短路求值，`vec` 为空时 `vec.back()` 不会被调用。课件由此提炼关键思想：`back` 的前置条件（precondition）——`vec` 非空——由程序员负责维护，违反前置条件的后果亦由程序员承担。这一分工引出一个自然的问题：库本身能否做得更好？

## 8. back() 的实现剖析（Slides 29–32）

`vec` 中可能存在"最后一个元素"，也可能不存在。同一个 `back()` 实现如何对两种情形都给出确定行为？考察其典型实现：

```cpp
valueType& vector<valueType>::back(){
    return *(begin() + size() - 1);
}
```

当 `size()` 为 0 时，`begin() + size() - 1` 指向有效存储之外，而"解引用一个未经检验、未必指向真实内存的指针"正是 undefined behavior。课件给出的第一种改进是在入口处检查并抛出异常：

```cpp
valueType& vector<valueType>::back(){
    if(empty()) throw std::out_of_range;
    return *(begin() + size() - 1);
}
```

（此处课件按简写形式给出抛出语句；严格写法应构造该类型的对象，如 `throw std::out_of_range{};`。）此后 `back()` 的行为至少是确定的：要么返回末元素，要么可靠地报错并终止程序。然而确定行为并非终点——"末元素是否存在"是客观事实，`back()` 能否在调用点提示这一事实，直接引出下一节对函数签名的讨论。

## 9. 函数签名即契约（Slides 33–34）

至此，type safety 的定义再次被具体化：type safety 指**函数签名**（function signature）保证**函数行为**（behavior）的程度。以此标准重审 `back()`：

```cpp
valueType& vector<valueType>::back(){
    return *(begin() + size() - 1);
}
```

签名 `valueType& back()` 承诺"返回一个 `valueType` 类型的对象"，而事实上可能并不存在这样的对象。这是一个虚假承诺（false promise）：契约与事实不符，违反契约的后果（UB）被转嫁给调用者，而调用者从签名中得不到任何警告。修复方向由此明确——让签名如实表达"可能没有值"。

## 10. 初步尝试：std::pair<bool, valueType&> 及其缺陷（Slides 35–39）

最直接的尝试是用 `std::pair` 携带一个布尔标志。

```cpp
std::pair<bool, valueType&> vector<valueType>::back(){
    if(empty()){
        return {false, valueType()};
    }
    return {true, *(begin() + size() - 1)};
}
```

空 `vector` 时返回 `{false, valueType()}`，其中 `valueType()` 是 `valueType` 的默认构造临时对象。这一签名确实"宣传"了末元素可能不存在，但存在三重缺陷。其一，`valueType` 未必提供 default constructor，`valueType()` 可能根本无法编译。其二，即便默认构造可用，其代价也可能十分高昂（下一节将说明 `std::optional` 正是对构造代价高的类型处理良好的方案）。其三，调用端依然不可靠。改写后的调用端为：

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back().second % 2 == 1){
        vec.pop_back();
    }
}
```

标志位 `.first` 被完全忽略，代码直接取 `.second` 参与运算；而"无值"分支返回的默认构造值可能是任意值——课件以设问方式指出，若某类型的默认构造产生了奇数，上述循环的行为便完全不可预测。此外，`pair` 的第二个成员是引用类型，将其绑定到默认构造的临时对象还引入生存期隐患。结论是：布尔标志加值的组合既不经济也不安全，需要一种原生表达"值或有或无"的类型。

## 11. std::optional 登场（Slides 40–47）

上一节的 ??? 现在有了答案。`std::optional` 定义于头文件 `<optional>`，自 C++17 起可用：它是一个模板类，要么含有一个 `T` 类型的值，要么不含任何值——后者记作 nullopt。课件引用的标准文档指出：类模板 `std::optional` 管理"可能存在也可能不存在的包含值（contained value）"，其典型用途是可能失败的函数返回值；与 `std::pair<T, bool>` 等方案相比，`optional` 对构造代价高的类型处理良好，且意图表达显式、可读性更强。

需要特别辨析 nullopt 与 nullptr：二者名称相近，但属于不同机制——nullptr 是可转换为任何指针（pointer）类型值的对象；nullopt 则是可转换为任何 optional 类型值的对象。据此，交叉使用均无法通过编译。

```cpp
int* p = nullptr;      // p points to nothing
if (p == nullptr) {
    std::cout << "p is a null POINTER\n";
}

std::optional<int> x = nullptr;   // ERROR - nullptr is NOT for optionals
```

```cpp
std::optional<int> x = std::nullopt;     // x contains nothing
if (!x) {
    std::cout << "x is an EMPTY OPTIONAL\n";
}

int* p = std::nullopt;    // ERROR - nullopt is NOT a pointer
```

`optional` 的值状态可以随时改变：

```cpp
void main(){
    std::optional<int> num1 = {}; //num1 does not have a value
    num1 = 1; //now it does!
    num1 = std::nullopt; //now it doesn't anymore
}
```

空花括号 `{}` 与 `std::nullopt` 在此处可互换，均构造空 `optional`。据此，`back()` 可以重写为：

```cpp
std::optional<valueType> vector<valueType>::back(){
    if(empty()){
        return {};
    }
    return *(begin() + size() - 1);
}
```

新签名如实声明"返回 `std::optional<valueType>`"：存在末元素时由 `valueType` 隐式转换构造，不存在时返回空 `optional`。契约与事实首次取得一致。

## 12. std::optional 的基本接口（Slides 48–54）

`optional` 类型的对象不能直接参与算术运算：在新签名下，`vec.back() % 2` 不再是合法代码，必须先取出 `optional` 内部的值。课件依次介绍三个基本成员：

- `.value()`：返回所含值；若 `optional` 为空，抛出 bad_optional_access 异常。
- `.value_or(val)`：有值时返回所含值，否则返回参数 `val` 作为默认值。
- `.has_value()`：有值时返回 `true`，否则返回 `false`。

综合示例：

```cpp
#include <iostream>
#include <optional>

int main() {
    std::optional<int> a = 5;
    std::optional<int> b = std::nullopt;

    // 1. has_value()
    std::cout << "a.has_value(): " << a.has_value() << "\n"; // 1 (true)
    std::cout << "b.has_value(): " << b.has_value() << "\n"; // 0 (false)

    // 2. value()
    if (a.has_value()) {
        std::cout << "a.value(): " << a.value() << "\n";      // 5
    }
    // Uncommenting this would throw bad_optional_access:
    // std::cout << b.value() << "\n";

    // 3. value_or(default)
    std::cout << "a.value_or(999): " << a.value_or(999) << "\n";  // 5
    std::cout << "b.value_or(999): " << b.value_or(999) << "\n";  // 999

    return 0;
}
```

解析：`a` 含 5，故 `has_value()` 输出 1，`value()` 输出 5，`value_or(999)` 忽略默认值仍输出 5；`b` 为空，`has_value()` 输出 0，直接调用 `b.value()` 将抛出 `bad_optional_access`，而 `value_or(999)` 返回默认值 999。三个接口分别覆盖了"判空""严格取值""带兜底的取值"三种消费方式。

## 13. 调用端的三次改写（Slides 55–57）

接口就绪后，`removeOddsFromEnd` 的循环条件可依次改写。第一版使用 `.value()`：

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back().value() % 2 == 1){
        vec.pop_back();
    }
}
```

对空 `vector` 调用 `back()` 后再取值时，程序将可靠地抛出 `bad_optional_access`——不再是不可预测的 UB，但以异常终止仍非理想。第二版显式检查：

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back().has_value() && vec.back().value() % 2 == 1){
        vec.pop_back();
    }
}
```

行为正确且不再抛异常，但每次迭代都要写两遍 `vec.back()`，相当繁琐。第三版利用 `optional` 在布尔语境中的转换：

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() && vec.back().value() % 2 == 1){
        vec.pop_back();
    }
}
```

空 `optional`（即 `nullopt` 状态）在布尔语境下为假，故 `vec.back()` 可直接充当"有值"判断，代码明显更简洁。

## 14. 问题的推广：operator[] 与 optional<T&>（Slides 58–63）

回顾问题的根源：为何在空 `vector` 上误调 `back()` 如此容易，而后果又如此危险？答案在于签名给出了虚假承诺。同样的模式遍布容器接口，例如：

```cpp
int foo(vector<int>& vec){
    return vec[0];
}
```

`vec` 为空时 `vec[0]` 同样是 undefined behavior。自然会设想：让 `operator[]` 返回 `optional` 如何？

```cpp
std::optional<valueType&>
vector<valueType>::operator[](size_t index){
    if (index < size()) {
        return *(begin() + index);
    }
    return std::nullopt;
}
```

这条路径在 C++ 中不可行：`std::optional<T&>` 并不存在，`optional` 的模板实参不能是引用类型。原因在语义层面：引用必须始终绑定到某个有效对象，而 `optional` 的核心能力恰是"可能不指代任何值"；设想"一个指向 nullopt 的引用"即可看出两种概念无法调和。课件的使用端示例说明了这一矛盾：

```cpp
int main() {
    vector <int> v;
    v.data = {10, 20, 30};

    auto optRef = v[5];    // returns std::nullopt
    // ERROR: int& must store a reference to a real integer, not std::nullopt
}
```

若越界的 `v[5]` 返回 `std::nullopt`，接收它的 `int&` 便无法成立——引用必须指涉一个真实的整数，而非"空"。

## 15. operator[] 与 .at() 并存的理由（Slide 64）

既然"返回可能不存在的引用"不可表达，带检查版本的最佳出路便只剩可靠报错。标准库的做法是提供两个接口：

```cpp
valueType& vector<valueType>::operator[](size_t index){
    return *(begin() + index);
}
```

```cpp
valueType& vector<valueType>::at(size_t index){
    if(index >= size()) throw std::out_of_range;
    return *(begin() + index);
}
```

（抛出语句的严格写法同第 8 节所注。）例题：二者为何并存？解析：`operator[]` 将"下标必须有效"作为前置条件交由程序员保证，实现中不含任何检查，因而不付出运行时代价；`.at()` 内建检查，越界时以 `std::out_of_range` 确定性地失败。前者对应第 7 节得出的分工——程序员负责前置条件，后者为需要运行时保证的场合提供出口。这种双轨设计与课件末尾列出的 C++ 设计哲学——允许程序员完全掌控、除非万不得已不牺牲性能——完全一致。

## 16. std::optional 的得失评估（Slides 65–66）

采用 `std::optional` 返回值的收益有二：其一，函数签名构成信息更丰富的契约（more informative contracts），"可能没有结果"成为类型的一部分；其二，类成员函数的调用具备有保证、可使用的行为——至少可靠报错而非 UB。代价同样明确：调用端将到处出现 `.value()`；误用依然可能触发 `bad_optional_access`；`optional` 也有自己的 UB 通道——`*optional` 与 `.value()` 语义相同却不做任何检查，对空 `optional` 解引用同样未定义；此外，很多场合真正需要的是 `std::optional<T&>`，而它并不存在。课件在此提出问题：既然如此，为什么还要费力使用 `optional`？答案在于下一组工具：monadic operations。

## 17. monadic operations（Slides 67–76）

`std::optional` 提供三个成员函数，把"取值—变换—兜底"封装起来。

`.and_then(f)`：有值时返回 `f(value)`，否则返回 `nullopt`；`f` 必须返回 optional。换言之，`f` 的类型轮廓是 `valueA → optional<valueB>`，适用于可能失败的变换。

```cpp
#include <iostream>
#include <optional>

std::optional<int> half(int x) {
    if (x % 2 == 0) return x / 2;
    return std::nullopt;
}

int main() {
    std::optional<int> a = 8;

    auto result = a.and_then(half)    // 8 -> 4
                  .and_then(half)     // 4 -> 2
                  .and_then(half);    // 2 -> 1

    if (result)
        std::cout << *result;  // prints 1

    std::optional<int> b = 7;

    auto result2 = b.and_then(half);  // 7 is odd -> nullopt

    if (!result2)
        std::cout << "\nhalf(7) failed!\n";
}
```

`half` 对奇数输入"失败"，`and_then` 将失败沿链条自动传播：8 经三次折半得到 1 并被打印；7 为奇数，`result2` 为空，程序转而打印失败消息。链条中任何一环为空，后续 `and_then` 均直接跳过计算。

`.transform(f)`：有值时返回 `f(value)`（包装为 optional），否则返回 `nullopt`；`f` 返回普通值，类型轮廓为 `valueA → valueB`，适用于必然成功的变换。

```cpp
#include <iostream>
#include <optional>

int square(int x) { return x * x; }

int main() {
    std::optional<int> x = 5;

    auto y = x.transform(square);

    if (y)
        std::cout << *y;      // prints 25

    std::optional<int> z = std::nullopt;

    auto w = z.transform(square);  // z is empty -> nullopt

    if (!w)
        std::cout << "\nsquare(nullopt) = nullopt\n";
}
```

`x` 含 5，`y` 含 25；`z` 为空，`w` 亦为空——"无值"状态穿透 `transform`，调用者无须逐一判空。

`.or_else(f)`：有值时返回原值所在的 optional，否则返回调用 `f` 的结果；它处理的是失败路径而非成功路径。

```cpp
#include <iostream>
#include <optional>

std::optional<int> fallback() {
    return 42;
}

int main() {
    std::optional<int> good = 10;
    std::optional<int> bad  = std::nullopt;

    auto r1 = good.or_else(fallback);  // returns optional(10)
    auto r2 = bad.or_else(fallback);   // returns optional(42)

    std::cout << "r1 = " << *r1 << "\n";  // 10
    std::cout << "r2 = " << *r2 << "\n";  // 42
}
```

课件将这一组机制概括为 monadic（单子的）：一种软件设计模式，其结构将程序片段（函数）组合起来，并把返回值包装在带有附加计算的类型之中。三个成员函数的共同点是：把一个函数应用于 `optional`，要么得到计算结果，要么得到空值或默认值，调用者无须手写判空分支。

这种链式组合并非 `optional` 独有。课件指出，此前讨论过的 C++20 ranges views 链同样是 monadic 风格。

```cpp
int square(int x) {
    return x * x;
}

int add_one(int x) {
    return x + 1;
}

int main() {
    using namespace std::views;

    auto v =
        iota(1, 11)
        | transform(square)
        | transform(add_one)
        | filter([](int x) { return x % 2 == 0; });

    for (int x : v) {
        std::cout << x << " ";
    }
}
```

对 1 至 10 依次平方、加一，再过滤偶数，输出为 `2 10 26 50 82`。views 的管道组合与 `optional` 的链式调用共享同一设计思想：把附加计算（此处为"元素是否存在、是否通过过滤"）封装进类型之中。

需要说明的是，课件个别复习页将 `.transform` 的回调要求写作"必须返回 `optional<valueType>`"，与同组正文定义（`f: valueA → valueB`，返回普通值；须返回 optional 的是 `and_then`）不一致，应以正文定义与标准语义为准。

## 18. and_then 的实际运用与辨析（Slides 77–78）

回到 `removeOddsFromEnd`，课件给出基于 `and_then` 的版本。

```cpp
void removeOddsFromEnd(vector<int>& vec){
    auto isOdd = [](optional<int> num){
        if(num)
            return num % 2 == 1;
        else
            return std::nullopt;
        //return num ? (num % 2 == 1) : {};
    };
    while(vec.back().and_then(isOdd)){
        vec.pop_back();
    }
}
```

其意图清晰：lambda `isOdd` 接收 `optional<int>`，`and_then` 将其作用于 `back()` 的结果，空 `optional` 无须显式判断即可在链条中传播。作为示意代码，其中有三处值得辨析的易错点。其一，两个 `return` 分支的类型不一致——一为 `bool`，一为 `std::nullopt_t`——编译器无法推导统一的返回类型；被注释的语句表明真实意图：返回 `optional<bool>`，其中空花括号 `{}` 即空 optional，写作 `return num ? (num % 2 == 1) : {};`。其二，`optional<int>` 不支持 `%` 运算（第 12 节已指出不能对 optional 做算术），取出内部值后应写作 `*num % 2 == 1` 或 `num.value() % 2 == 1`。其三，`and_then` 的结果 `optional<bool>` 在布尔语境下的真值仅取决于"是否含有值"，与内部布尔值无关——含 `false` 的 `optional<bool>` 仍为真——因此该 `while` 条件按严格语义并不能在偶数处正确停止。此段代码应理解为演示 `and_then` 组合方式的教学示意，而非可直接投产的实现。

## 19. 现实约束与 C++ 设计哲学（Slides 79–82）

课件在此给出重要澄清：`std::vector::back()` 实际上并不返回 optional，而且很可能永远不会。前文的重写是教学性的思想实验。这一现实可以由 C++ 的设计哲学解释，课件列出六条：只有当特性解决真实问题时才添加特性；程序员应可自由选择风格；模块化（compartmentalization）是关键；允许程序员在需要时获得完全控制；除万不得已不牺牲性能；尽可能在编译期强制安全。就本讲而言，"不牺牲性能"与"完全控制"两条意味着：标准库容器保留无检查接口（`operator[]`、`back()`）以避免运行时开销，type safety 的增强留给程序员在应用层自行选用。课件同时列举了真正把 optional monad 作为核心机制的语言：Rust，保证内存安全与线程安全的系统语言；Swift，Apple 面向应用开发的媒体创作语言之外的主打应用开发的语言；以及 JavaScript。

## 20. 总结：类型系统保证程序行为（Slides 83–90）

本讲的结论可归纳为课件的几条要点。严格的类型系统能够保证程序的行为。`std::optional` 是实现这一目标的工具之一：函数可以返回"值或无值"，并借助 `.has_value()`、`.value_or()`、`.value()`（以及 monadic operations）安全地消费结果。然而 optional 的使用可能显得笨拙并带来开销，因此 C++ 并未在多数 STL 数据结构中采用它；许多其他语言则相反。除在类设计中使用外，在应用代码中于理有据处使用 `std::optional` 也是课件明确鼓励的做法。全讲的收束是类型理论领域的一句名言："Well typed programs cannot go wrong."（良类型的程序不会出错），出自 Robert Milner。课件最后提供一个交互式练习页面（<https://106l.vercel.app/optional>），供读者亲手实现一个 `std::optional`，以巩固对上述接口与语义的理解。

## 本讲要点

- type safety 的定义层层递进：从"语言防止类型错误的程度"，到"语言保证程序行为的程度"，最终落脚为"函数签名保证函数行为的程度"。签名即契约，`valueType& back()` 这类虚假承诺正是 undefined behavior 的温床。
- 对"可能没有结果"的运算，应让这一事实进入类型系统：返回 `std::optional<T>`。nullopt 是 optional 专用的空值，与 nullptr 分属两套机制，不可混用；`{}` 与 `std::nullopt` 均可构造空 optional。
- 基本接口：`.has_value()` 判空，`.value()` 取值（空则抛 `bad_optional_access`），`.value_or(v)` 带默认值取值；`optional` 在布尔语境可直接判空，而 `operator*` 与 `.value()` 语义相同却不做检查。
- monadic operations 把判空与失败传播交给类型与组合子完成：可能失败的变换用 `.and_then`（回调返回 optional），必然成功的变换用 `.transform`（回调返回普通值），失败兜底用 `.or_else`；C++20 ranges views 的管道组合体现同一设计思想。
- `std::pair<bool, valueType&>` 式返回依赖默认构造、开销可观且调用端仍可能出错；`std::optional<T&>` 因引用必须绑定有效对象而不存在，越界访问的受检出路是 `.at()` 抛出异常，无检查的 `operator[]` 则把前置条件留给程序员。
- `std::vector::back()` 实际并不返回 optional：出于性能与控制权优先的设计哲学，STL 数据结构不做此封装，但在应用代码中合理使用 `std::optional` 值得鼓励。"Well typed programs cannot go wrong."
