---
title: "Lecture 12 · Operator Overloading 逐字稿"
createAt: 2026/9/13
---

# Lecture 12: Operator Overloading（逐字稿）

> 对应课件转写：[2026Spring-12-OperatorOverloading.md](../output/2026Spring-12-OperatorOverloading.md)

## 1. 本讲主题与前讲回顾

本讲（Lecture 12）主题为 operator overloading（运算符重载），内容分两部分：先简要回顾上一讲的函数与 lambda，再进入运算符重载。核心问题是：如何使 `+`、`<`、`<<` 等运算符在自定义类型上正确且有意义地工作。

回顾 STL（Standard Template Library，标准模板库）的四个组成部分：**Containers**（如何存储一组元素）、**Iterators**（如何遍历容器）、**Functors**（如何将函数表示为对象）、**Algorithms**（如何以泛型方式变换和修改容器）。上一讲围绕 Functors 展开，其核心语法是 lambda。以如下例子为参照：

```cpp
auto lessThanN = [n] (int x) {
    return x < n;
};
```

该表达式包含四个部分。`auto`：闭包对象的类型由编译器掌握，无须（也无从）手写；capture clause `[n]`：捕获子句使 lambda 可以使用外部变量；参数列表 `(int x)`：与普通函数的参数完全一致；函数体 `{ return x < n; }`：写法与普通函数相同，唯一区别是作用域内仅有参数与捕获的变量。

上一讲末尾还介绍了 ranges 与 views 的链式组合：

```cpp
std::vector<char> letters = {'a', 'b', 'c', 'd', 'e'};
std::vector<char> upperVowel = letters
    | std::ranges::views::filter(isVowel)
    | std::ranges::views::transform(toupper)
    | std::ranges::to<std::vector<char>>();

// upperVowel = { 'A', 'E' }
```

`letters` 经 filter 选出元音字母，经 transform 全部转为大写，最后由 `ranges::to` 收集为新 vector，得到 `{'A', 'E'}`。串联各 view 的 `operator|` 本身就位于可重载运算符的清单之中（见第 5 节），这正是本讲主题的一个直观例证。

## 2. 问题引入：std::map<K, V> 对 key 类型的要求

至此，我们已经掌握 class 与 templated class 的写法，但 map 与 set 对模板参数另有要求：`std::map<K, V>` 要求 key 类型 `K` 支持 `operator<`。

这一要求源于 map 的底层结构。课件以 `map["Alex"]` 的查找过程为例：map 内部是一棵二叉搜索树，查找即沿途反复进行"小于"比较——先判断 `"Alex" < "CS106L"`，成立则进入左子树；再判断 `"Alex" < "Chris"`，成立则继续向左。可见每次查找都由一串 `operator<` 调用驱动；若 key 类型自身无法比较大小，查找便无从进行。由此引出本讲的问题：如何让自定义类型支持这些运算符。

## 3. 使用运算符的动机：Money 类

课件引用一场 CppCon 演讲中的论断："Operators allow you to convey meaning about types that functions don't."——运算符能够传达普通函数无法传达的、关于类型的含义。

考察一个表示货币的类：

```cpp
class Money {
public:
    int cents;
    Money(int c) : cents(c) {}
};
```

若以普通函数实现两笔金额相加：

```cpp
Money add(const Money& a, const Money& b) {
    return Money(a.cents + b.cents);
}

Money total = add(Money(100), Money(50));  // 100 + 50 = 150
```

该版本功能正确，但如课件所言，它读起来更像一次随意的函数调用，而非"加法"。将函数名改为 `operator+` 之后的版本如下：

```cpp
Money operator+(const Money& a, const Money& b) {
    return Money(a.cents + b.cents);
}

Money total = Money(100) + Money(50);
```

调用形式随即变为 `Money(100) + Money(50)`，代码阅读者由此立即领会：Money 具有类似数值的行为，`+` 表示两笔金额相加。这正是上述论断的含义——运算符传达了类型自身的语义。

## 4. 例题与解析：泛型 min 对类型 T 的要求

**例题**　设有泛型函数：

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}

// For which T will the following compile successfully?
T a = /* an instance of T */;
T b = /* an instance of T */;
min<T>(a, b);
```

类型 T 须满足什么条件，上述 min 才能编译通过并具备明确语义？

**解析**　条件有二。其一，T 应具有说得通的 ordering relationship（排序关系）；其二，T 所表示的对象应是 comparable（可比较）的，"最小值"这一概念能够被逻辑地确定。`int` 天然满足：数轴上向右递增、向左递减，两个整数比较大小是良定义的。

而对于 StanfordID：

```cpp
StanfordID rachel;
StanfordID preston;

auto minStanfordID = min<StanfordID>(preston, rachel);
```

min 的函数体即 `return a < b ? a : b;`，而 StanfordID 从未定义 `operator<`，编译器无法解析该表达式，只能报告"Hey, I don't know what to do here!"，编译失败；两个 StanfordID 之间"谁更小"在定义比较规则之前也不具备语义。要使该模板可用，须为 StanfordID 提供运算符实现。

## 5. 运算符重载的基本概念

类中运算符的工作方式与函数一致：如同可以在类中声明函数，也可以声明某个运算符的行为；当该运算符用于此类对象时，执行的就是自定义操作。其机理与 function overloading 相同——为运算符提供同名实现时，即以自定义行为取代其原有行为。

**Operators** 是对值、对象或类型执行操作并产生新值或新效果的符号，其作用涉及三个层面：作用于值，如 `3 + 4`；作用于对象，如两个 `Point` 对象的 `a + b`；甚至作用于类型，如 `sizeof(int)` 与 `new int(5)`——两者本身也是运算符。

可重载的运算符占绝大多数：

```text
+  -  *  /  %  ^  &  |  ~  !  ,  =  <  >  <=  >=
++  --  <<  >>  ==  !=  &&  ||  +=  -=  *=
/=  %=  ^=  &=  |=  <<=  >>=  [ ]  ( )  ->
->*  new  new[ ]  delete  delete[ ]
```

不可重载的有五类，对应七个符号：scope resolution（作用域解析）`::`、ternary（三元条件）`?`、member access（成员访问）`.`、pointer-to-member access（成员指针访问）`.*`，以及对象的大小、类型与转换相关的 `sizeof()`、`typeid()` 与 cast。这些符号与语言最底层的语义绑定，不允许重定义。

重载的语法与函数声明一致：

```cpp
return_type operator<symbol>(parameter_list);
```

即关键字 `operator` 后接符号本身，返回类型与参数列表的写法与普通函数完全相同。

## 6. 成员函数版本的 operator<

以下以 StanfordID 为贯穿示例，给出成员函数（member function）版本的 `operator<`。头文件中的声明如下：

```cpp
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    // constructor for our StanfordID
    StanfordID(std::string name, std::string sunet, int idNumber);
    int getIdNumber();
    .
    .
    bool operator < (const StanfordID& other) const;
};
```

末行即一个成员函数声明：函数名为 `operator<`，参数为另一个 StanfordID，尾置 `const` 表明该操作不修改对象自身。（转写件 slide 32/33 将 `getIdNumber` 的返回类型写作 `std::string`，与成员 `idNumber` 的 `int` 类型不符；slide 35 采用 `int`，本稿从之。）

实现位于 .cpp 文件，函数体以问号占位，即课件提出的例题：

```cpp
#include "StanfordID.h"

int StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfordID& rhs) const {
    ?
}
```

**例题**　若要以 `idNumber` 成员比较两个 StanfordID，函数体应如何实现？

**解析**　最直接的写法是借助 public 访问器：

```cpp
bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.getIdNumber();
}
```

自身一侧的 `idNumber` 直接访问，另一侧通过 `getIdNumber()` 获取。

课件随后给出的另一版本包含一个值得注意的细节：

```cpp
bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.idNumber;
}
```

`other.idNumber` 是 private 成员，却能被直接访问。原因在于：类的成员函数不仅可以访问 `this` 所指对象的 private 成员，还可以访问同类任何对象的 private 成员——访问控制以"类"为单位，而非以"对象"为单位。课件另提供了与该例配套的在线练习（链接见 slide 38）。

## 7. Non-member overloading 及其动机

运算符重载有两种方式。其一为 **member overloading**（成员重载）：将运算符声明在类的 scope 之内，即第 6 节的形式。其二为 **non-member overloading**（非成员重载）：将运算符声明在类定义之外，并把左、右操作数都作为参数传入。两种签名对比如下：

```cpp
// Non-member Operator Overloading
bool operator < (const StanfordID& lhs, const StanfordID& rhs);

// Member Operator Overloading
bool StanfordID::operator < (const StanfordID& rhs) const {...}
```

member 版本以隐式的 `this` 充当左操作数，故参数仅一个；non-member 版本没有 this，左、右操作数 lhs 与 rhs（left-hand side、right-hand side 的缩写）均须显式列为参数。这是两者的本质区别。

non-member 形式的必要性可由如下场景说明。设为 StanfordID 定义成员版 `operator<`，使其与 `std::string` 比较 sunet：

```cpp
class StanfordID {
private:
    std::string sunet;
public:
    StanfordID(std::string s) : sunet(s) {}

    bool operator<(const std::string& other) const {
        return sunet < other;
    }
};
```

左操作数为 StanfordID 时，以下用法合法：

```cpp
StanfordID rachel("rfer");
std::string name = "zzhang";

if (rachel < name) {
    std::cout << "Rachel comes before name\n";
}
```

编译器在左操作数的类型 StanfordID 中找到了成员 `operator<`。交换操作数之后：

```cpp
if (name < rachel) {
    std::cout << "Name comes before Rachel\n";
}
```

编译失败。此时编译器将表达式理解为 `name.operator<(rachel)`，即在 `std::string` 类中查找成员函数 `operator<`，而 string 并不接受 StanfordID 类型的实参。结论：member operator 的左操作数必须是该类自身的对象；左操作数类型不具备该成员，表达式即不成立。

non-member overloading 正是针对这一限制，课件给出两条理由。其一，允许左操作数为 non-class type（非类类型）：

```cpp
bool operator<(int lhs, const StanfordID& rhs) {
    return lhs < rhs.getIDNumber();
}
```

左操作数 `int` 是内置类型，不存在可供挂载成员函数的类体，只有非成员写法能覆盖这一情形。

其二，允许为不拥有的类重载运算符。`std::string` 的定义不在我们掌握之中，无法向其内部添加成员 `operator<`；而非成员函数位于类外，可以将 StanfordID 与任何自定义类组合比较，无须改动既有代码。

non-member 还便于书写对称的比较：同时提供两个方向的版本即可。

```cpp
// Non-member operator
bool operator<(const StanfordID& lhs, const std::string& rhs) {
    return lhs.getSunet() < rhs;
}

// And if you want symmetry:
bool operator<(const std::string& lhs, const StanfordID& rhs) {
    return lhs < rhs.getSunet();
}
```

如此 `rachel < name` 与 `name < rachel` 均为合法。课件强调：STL 实际上更倾向于 non-member overloading，这是更 idiomatic 的 C++ 风格。

## 8. private 成员的访问与 friend

member 版本中存在 `this`，可直接使用类的成员变量；non-member 版本则是类外的普通函数，无法访问 StanfordID 的 private 成员，这一限制没有例外。

与此相关有一条重要约束：对同一组操作数类型，member 与 non-member 两种 `operator<` 不可同时提供：

```cpp
bool operator < (const StanfordID& lhs, const StanfordID& rhs);   // non-member
bool StanfordID::operator < (const StanfordID& rhs) const {...}   // member
```

课件将这一情形表述为 undefined behavior；其核心信息在于：两个 StanfordID 作 `<` 比较时，两条重载路径均可行，重载解析产生二义性（ambiguity）。二义性是需要避免的坏设计——同一运算符、同一组操作数类型，只应提供一种实现。

若 non-member 函数确需访问 private 成员，C++ 提供关键字 **friend**（友元）：它允许非成员函数或其他类访问另一个类的 private 信息。用法是在目标类的头文件中将该函数声明为 friend：

```cpp
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    // constructor for our StanfordID
    StanfordID(std::string name, std::string sunet, int idNumber);
    .
    .
    .
    friend bool operator < (const StanfordID& lhs, const StanfordID& rhs);
};
```

该声明位于类定义内部，语义却是：此函数并非类的成员，但被授权访问其 private 成员。实现照常写在 .cpp 文件中：

```cpp
#include "StanfordID.h"

bool operator< (const StanfordID& lhs, const StanfordID& rhs)
{
    return lhs.idNumber < rhs.idNumber;
}
```

`lhs.idNumber` 与 `rhs.idNumber` 由此均可直接访问，编译器得以完成比较。

若实现只使用 public 访问器，friend 并非必需：

```cpp
bool operator< (const StanfordID& lhs, const StanfordID& rhs)
{
    return lhs.getIdNumber() < rhs.getIdNumber();
}
```

仅当确实需要触及 private 成员时，才需要引入 friend。

## 9. 运算符的意义与设计原则

补全 `operator<` 之后，第 4 节的问题随之解决：

```cpp
StanfordID rachel;
StanfordID preston;

auto minStanfordID = min<StanfordID>(rachel, preston);

StanfordID min(const StanfordID& a, const StanfordID& b)
{
    return a < b ? a : b;
}
```

此时编译器的反馈变为"now I know what to do here!"：min 模板一行未改，仅因 StanfordID 提供了 `operator<` 即可使用。

可定义的运算符数量众多（见第 5 节清单），能够解锁的功能亦多。但更关键的仍是第 3 节的论断："Operators allow you to convey meaning about types that functions don't." 运算符的意义在于传达类型的含义。由此得出若干设计原则：

- 运算符承载关于类型的含义，故含义必须是 obvious（显而易见）的；
- 可定义的运算符多为算术运算符，其功能应与原有语义 reasonably similar（合理相似）——例如不应把 operator+ 定义为集合减法；
- 若含义并不明显，则应改用普通命名函数，而非运算符。

上述立场通称 Principle of Least Astonishment（PoLA，最小惊讶原则）：不应令代码阅读者感到意外。

另一项良好实践是 rule of contrariety（相反关系法则）：定义 `operator==` 之后，由它定义 `operator!=`：

```cpp
bool StanfordID::operator==(const StanfordID& other) const {
    return (name == other.name) && (sunet == other.sunet) &&
    (idNumber == other.idNumber);
}

bool StanfordID::operator!=(const StanfordID& other) const {
    return !(*this == other);
}
```

`==` 逐项比较 name、sunet、idNumber 三个字段；`!=` 不重复比较逻辑，直接返回 `!(*this == other)`。"不等"由"相等"的否定定义，两者的语义由构造保证一致。

## 10. 流插入运算符 operator<<

运算符的实现同时保有相当的灵活性，`<<`（stream insertion operator，流插入运算符）是典型例子。同为"打印一个 StanfordID"，可以写出不同的实现：

```cpp
std::ostream& operator << (std::ostream& out, const StanfordID& sid) {
    out << sid.name << " " << sid.sunet << " " << sid.idNumber;
    return out;
}

std::ostream& operator << (std::ostream& out, const StanfordID& sid) {
    out << "Name: " << sid.name << " sunet: " << sid.sunet << " idnumber: "
    << sid.idNumber;
    return out;
}
```

两个版本签名完全一致，属同一函数的两种可选实现：第一个参数 `std::ostream&` 对应表达式左侧的流（例如 cout），第二个参数为待打印对象，返回 `std::ostream&` 以支持 `cout << a << b` 式的链式书写。差异仅在输出格式：前者以空格分隔三个字段，后者携带字段标签、更利于阅读。课件由此指出：The way you use this operator may influence how you implement it——运算符的使用方式会影响其实现选择，格式并无唯一答案。此外，两个版本均直接访问 `sid` 的 private 成员，依照第 8 节的结论，这需要以 friend 声明为前提。

## 11. 综合练习：PizzaOrder

课件最后给出一个综合练习：设计 PizzaOrder 类。成员变量为 customer、topping 与 slices（片数）；提供 getter：`getCustomer()`、`getTopping()`、`getSlices()`。要求实现如下运算符：

- `+=`：为某顾客的订单增加片数；
- `==`：判断两单的片数、顾客与 topping 是否完全一致；
- `<`：判断一单片数是否少于另一单；
- `>`：判断一单片数是否多于另一单；
- `<<`：按 "CustomerName: #ofSlices, Topping" 格式输出。

设计时可依据前文原则权衡：`+=` 修改对象自身，宜采用 member 版本；`<<` 的左操作数是流而非 PizzaOrder，依第 7 节的结论只能采用 non-member 形式；`<`、`>` 若需与其他类型双向比较，non-member 更为合适。练习链接见课件（cs106l-operator-overloading-2）。

## 12. 结语

课件以三条 final thoughts 收束全讲。其一，operator overloading 为自定义对象解锁了新的一层功能与含义。其二，运算符应当 make sense：其存在价值正在于传达普通函数无法传达的、关于类型本身的含义。其三，应在确有需要时才重载——例如类型不与流交互，便不必重载 `<<` 或 `>>`。

## 本讲要点

- 运算符重载使自定义类型获得与内置类型一致的表达力：operator+ 表达加法、operator< 表达比较，这类含义是普通函数名难以传达的；`std::map<K, V>` 要求 key 类型支持 operator<，正是由于其底层二叉搜索树的查找由一连串"小于"比较驱动。
- 重载语法即函数语法：`return_type operator<symbol>(parameter_list);`。绝大多数运算符可重载；`::`、`?`、`.`、`.*`、`sizeof()`、`typeid()` 与 cast 不可重载。
- member overloading 声明于类内，左操作数固定为 this，因而左操作数必须是本类对象；non-member overloading 声明于类外，lhs 与 rhs 均为显式参数，从而支持左操作数为非类类型、为不拥有的类配置运算符，并可写出双向对称的比较——STL 亦更倾向 non-member 风格。
- non-member 函数默认无法访问 private 成员；确需访问时，在目标类头文件中将其声明为 friend，仅使用 public 访问器则无须 friend。对同一组操作数类型同时提供 member 与 non-member 版本会导致重载解析二义性（课件表述为 undefined behavior），属应当避免的坏设计。
- 遵循 Principle of Least Astonishment（PoLA）：运算符含义须显而易见，行为须与原有语义合理相似，含义不明显时改用普通函数；operator!= 可由 operator== 取反而得（rule of contrariety）。
- operator<< 是 non-member 重载的典型应用：接收 `std::ostream&` 并将其返回以支持链式调用；具体输出格式由使用场景决定，用法定义实现。
