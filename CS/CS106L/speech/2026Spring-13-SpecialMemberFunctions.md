---
title: "Lecture 13 · Special Member Functions 逐字稿"
createAt: 2026/9/13
---

# Lecture 13: Special Member Functions（逐字稿）

> 对应课件转写：[2026Spring-13-SpecialMemberFunctions.md](../output/2026Spring-13-SpecialMemberFunctions.md)

## 1. 本讲主题与结构（Slides 1–4）

本讲主题为 special member functions（特殊成员函数），课件标题以星号标注，属于本课程的重点内容。全讲分为两个部分：先回顾上一讲的 operator overloading（运算符重载），随后系统介绍 special member functions，依次覆盖其总览、copy 与 copy assignment、`delete`，以及 move 与 move assignment。下文按课件页序展开，读者可对照原 slides 阅读。

## 2. 运算符重载回顾：member、non-member 与 friend（Slides 5–13）

运算符重载存在两种形态（Slide 5）。其一为 non-member overloading（非成员函数重载）：

```cpp
bool operator< (const StudentID& lhs, const StudentID& rhs);
```

其二为 member overloading（成员函数重载）：

```cpp
bool StudentID::operator< (const StudentID& rhs) const {...}
```

两种形态的差异体现在参数表：non-member 版本显式接收左、右两个操作数 `lhs` 与 `rhs`；member 版本的左操作数即对象自身（`this`），故参数表中仅有 `rhs`。

**例题与解析**（Slides 6–7）：non-member overloading 相比 member overloading 有何优势？non-member overloading 有时需要完成何种 member overloading 不需要的工作？

解析：non-member overloading 的核心优势是 symmetric（对称性）。若 `operator<` 定义为成员函数，左操作数必须是该类的对象，当左操作数为其他类型时调用无法成立；定义为非成员函数后，两个操作数在重载决议中的地位完全一致，表达式两侧对称。所需的额外工作是 `friend` 声明：非成员函数默认无权访问类的 private/protected 成员，若实现需要直接读取私有数据，必须在目标类的头文件中将其声明为该类的 `friend`。

课件以四页（Slides 8–11）澄清成员与非成员两种写法中访问 `idNumber` 的合法途径。成员函数版本中，经由 getter 或直接访问均可：

```cpp
#include "StanfordID.h"

std::string StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.getIdNumber(); // 正确
}
```

```cpp
bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.idNumber; // 正确
}
```

第二种写法成立的原因是：同一类的成员函数可以访问该类任何对象的 private 成员。`other` 虽是不同于 `this` 的对象，但与 `this` 同属 `StanfordID` 类型，故直接访问 `other.idNumber` 合法。

非成员函数版本则不同：

```cpp
#include "StanfordID.h"

// defined within the StanfordID class
std::string StanfordID::getIdNumber() {
    return idNumber;
}

bool operator<(const StanfordID& lhs, const StanfordID& rhs) const
{
    return lhs.idNumber < rhs.idNumber; // 错误
}
```

该写法存在两处错误：其一，非成员函数没有 `this` 对象，不存在"成员函数的 const 限定"，`const` 不应出现在签名中；其二，`lhs.idNumber` 访问 private 成员，普通非成员函数无此权限。正确实现应经由公开接口：

```cpp
bool operator<(const StanfordID& lhs, const StanfordID& rhs)
{
    return lhs.getIdNumber() < rhs.getIdNumber(); // 正确
}
```

若 `StanfordID` 未提供 `getIdNumber()` 这类公开访问方法，而非成员函数确需直接读取 `idNumber`，则需借助 `friend` 关键字（Slide 12）。`friend` 允许非成员函数或其他类访问另一类的 private 信息；用法是在目标类的 header 中将该函数声明为该类的 friend。课件特别注明：若 `StanfordID` 没有 `getIdNumber()` 方法，就必须添加 `friend` 才能直接访问 `idNumber`。

就全景而言（Slide 13），C++ 中可重载的运算符数量众多，涵盖算术、比较、位运算、逻辑与复合赋值，直至下标、调用、解引用与内存管理运算符：

```
+  -  *  /  %  ^  &  |  ~  !  ,  =  <  >  <=  >=
++  --  <<  >>  ==  !=  &&  ||  +=  -=  *=
/=  %=  ^=  &=  |=  <<=  >>=  []  ()  ->
->*  new  new[]  delete  delete[]
```

## 3. Special Member Functions 总览：The Special 6（Slides 14–26）

一个 class 通常包含 constructor、destructor、member variables 与 functions 四类成分（Slide 15）。其中 constructor 与 destructor 有一个正式名称：special member functions（SMFs，特殊成员函数）。称其"特殊"，是因为它们不由使用者显式调用，而由编译器在特定时机自动调用：constructor 在每次创建类的新实例时被调用，destructor 在对象离开作用域时被调用。

SMF 共有六种（Slide 16），课件称之为 "The Special 6"：

- Default constructor: `T()`
- Destructor: `~T()`
- Copy constructor: `T(const T&)`
- Copy assignment operator: `T& operator=(const T&)`
- Move constructor: `T(T&&)`
- Move assignment operator: `T& operator=(T&&)`

一条关键规则：这六个函数仅在（1）被实际调用且（2）使用者尚未显式定义时，才由编译器自动生成。未被使用则不生成；需要而未定义时，编译器提供默认版本。默认版本仅保证行为可用，是否满足语义需求取决于类自身的设计。

课件以 `Widget` 类将六种函数并列展示（Slide 17），随后逐行讲解：

```cpp
class Widget {
  public:
    Widget();                             // default constructor
    Widget (const Widget& w);             // copy constructor
    Widget& operator = (const Widget& w); // copy assignment operator
    ~Widget();                            // destructor
    Widget (Widget&& rhs);                // move constructor
    Widget& operator = (Widget&& rhs);    // move assignment operator
};
```

Default constructor（Slide 18）不接收参数，负责创建一个全新对象。Copy constructor（Slide 19）以另一对象为蓝本做 member-wise（逐成员）拷贝，创建新对象，其调用时机如 Slide 20 所示：

```cpp
Widget widgetOne;
Widget widgetTwo = widgetOne;  // Copy constructor is called
```

`widgetTwo = widgetOne` 虽含等号，但 `widgetTwo` 在该行才被创建，等号在此表示以 `widgetOne` 初始化新对象，故调用的是 copy constructor。

Copy assignment operator（Slide 21）的语义是将一个 already existing object（已存在对象）赋给另一个已存在对象。其调用时机如 Slide 22 所示：

```cpp
Widget widgetOne;
Widget widgetTwo;
widgetOne = widgetTwo;
```

此处两个对象在 `=` 之前均已完成构造。课件将两种情形并列对照（Slide 23）：

```cpp
// Copy Constructor Invocation
Widget widgetOne;
Widget widgetTwo = widgetOne;

// Copy Assignment Operator Invocation
Widget widgetOne;
Widget widgetTwo;
widgetOne = widgetTwo;
```

二者的判别标准并非是否出现等号，而是等号左侧对象是否已经存在：左侧对象随语句一同诞生即为初始化（copy constructor），左侧对象早已存在则为赋值（copy assignment operator）。

Destructor（Slide 24）在对象离开作用域时被调用。Move constructor 与 move assignment operator（Slide 25）本讲不作展开，课程后续设有专讲。

上述六个函数均无须手写（Slide 26）：编译器会为每一个自动生成 default 版本。由此引出本讲的核心问题：默认版本何时够用、何时必须自行定义。

## 4. 构造函数中的初始化：member initializer list（Slides 27–35）

进入 copy 主题之前，课件先复习构造函数中的初始化问题。以第 8 讲自实现的 `Vector` 为例（Slide 28）：

```cpp
template <typename T>
Vector<T>::Vector()
{
  _size = 0;
  _capacity = 4;
  _data = new T[_capacity];
}
```

编写 constructor 时需要初始化全部 member variables，这段代码在表面上完成了这一要求；然而将成员初始化为默认值、随即重新赋值的流程是低效的（Slide 29）。原因在于其中实际发生了两个步骤（Slides 30–32）：第一步，进入函数体之前，`_size`、`_capacity`、`_data` 已被 default initialized；第二步，函数体内的三条语句才执行赋值。每个成员先被默认构造一次、再被赋值一次，工作实际上加倍；对基本类型开销尚可忽略，成员类型复杂时代价显著。

解决方案是 member initialization list（成员初始化列表，Slide 33）：

```cpp
template <typename T>
Vector<T>::Vector() : _size(0), _capacity(4), _data(new T[_capacity]) { }
```

冒号后的列表使成员被直接构造为期望值，函数体为空。课件归纳三个要点（Slide 34）：第一，直接以目标值构造成员，比"默认构造后再赋值"更快捷高效；第二，若成员是不可赋值（non-assignable）的类型，赋值途径不存在，initializer list 成为唯一选择；第三，initializer list 适用于任何 constructor，包括带参数的非默认 constructor。

所谓 non-assignable 类型，典型即 const 成员与引用成员（Slide 35）：

```cpp
template <typename T>
class MyClass {
    const int _constant;
    int& _reference;

public:
    // Only way to initialize const and reference members
    MyClass(int value, int& ref) : _constant(value), _reference(ref) { }
};
```

`const` 成员初始化之后不可再修改，引用成员绑定之后不可改绑，二者均只能在构造时初始化一次，此后任何赋值均属非法。因此这段代码只能以 initializer list 书写：对 const 与引用成员而言，赋值路径在语言层面并不存在。

## 5. 逐成员拷贝的局限：shallow copy 与 deep copy（Slides 36–41）

编译器免费提供的默认 SMF 中，copy constructor 执行何种操作（Slide 36）？它为每一个 member variable 创建副本，即 member-wise copying（逐成员拷贝）。这一默认行为并非总能满足需求：当成员含有指针时，逐成员拷贝复制的只是地址而非所指数据（Slides 37–39）。若按默认风格为 `Vector` 编写 copy constructor：

```cpp
template <typename T>
Vector<T>::Vector(const Vector<T>& other) :
    _size(other._size), _capacity(other._capacity),
    _data(other._data) { }
```

`_data(other._data)` 仅复制指针值，`vec` 与 `copy` 两个对象的 `_data` 便指向同一块底层数组。此即 shallow copy（浅拷贝）。课件指出其问题所在：对其中一个指针所做的任何操作都会影响另一个——经由一个对象修改元素，另一对象同步可见；一个对象析构时释放数组，另一对象的指针随即失效。

许多情形下，需要的拷贝不止于复制成员变量（Slide 40）。deep copy（深拷贝）指与原对象完全独立的完整副本。此时应以自定义实现覆盖默认的 special member functions；书写方式与普通函数一致：在 header 中声明，在 .cpp 中实现。

针对上述指针问题的修正如下（Slide 41）：

```cpp
Vector<T>::Vector(const Vector<T>& other)
    : _size(other._size), _capacity(other._capacity), _data(new T[other._capacity]) {
    for (size_t i = 0; i < _size; ++i) {
        _data[i] = other._data[i];
    }
}
```

关键在 `_data` 的初始化：不再复制 `other._data` 所持的地址，而是先 `new` 一块等容量的新数组，再在函数体中以循环逐元素拷贝。此时 `_data` 与 `other._data` 指向两块相互独立的数组，得到的才是对 Vector 数据的 deep copy。

## 6. `= delete`：显式禁用特殊成员函数（Slides 42–46）

默认版本不够好时可以重写；反之，若某项功能根本不希望存在，也可以将其显式关闭。设有一个管理密码的类（Slide 43）：

```cpp
class PasswordManager {
  public:
    PasswordManager();
    ~PasswordManager();
    // other methods ...
    PasswordManager(const PasswordManager& rhs);
    PasswordManager& operator = (const PasswordManager& rhs);

  private:
    // other important members ...
};
```

密码数据若被默认生成的拷贝随意复制显然危险，应当直接禁止拷贝。手段是将 special member function 置为 deleted（Slides 44–45）：在声明之后附加 `= delete`，即移除该函数的功能。

```cpp
class PasswordManager {
public:
    PasswordManager();
    PasswordManager(const PasswordManager& pm);
    ~PasswordManager();
    // other methods ...
    PasswordManager(const PasswordManager& rhs) = delete;
    PasswordManager& operator = (const PasswordManager& rhs) = delete;

private:
    // other important members ...
};
```

效果是 copying 不再是可能的操作：任何拷贝 `PasswordManager` 的代码都无法通过编译。相较于保留一个危险的默认拷贝等待运行期出错，令其在编译期失败是更安全的设计。

`= delete` 的意义在于允许对 special member functions 的功能做选择性开放（Slide 46）。例如希望某实例在全程序中仅存在一份时，可将拷贝相关的 SMF 全部 delete。标准库的 `std::unique_ptr` 即按此方式工作，cppreference 对其的描述为：该类满足 MoveConstructible 与 MoveAssignable 的要求，但既不满足 CopyConstructible 也不满足 CopyAssignable——可以 move 而不可 copy。

## 7. 两条设计准则：Rule of Zero 与 Rule of Three（Slides 48–51）

第一条准则为 Rule of Zero（零法则，Slide 48）：若编译器默认生成的 SMF 已能满足需求，就不要定义自己的版本。仅当默认版本不可用时才应自行定义；这种情况通常出现在手动处理动态分配内存时，例如类内含有指向 heap 的指针。

第二条准则进一步指出（Slides 49–50）：若类不需要自定义 constructor、destructor 或 copy assignment 等，就一律不写。若类所依赖的成员对象自身已经实现了这些 SMF，更无须重复实现这套逻辑。例如：

```cpp
class a_string_with_an_id {
    public:
        // getter and setter methods for our private variables
    private:
        int id;
        std::string str;
};
a_string_with_an_id object;
```

该类的成员均为 self-managing（自管理）类型：`int` 是基本类型，拷贝与赋值语义天然正确；`std::string` 自身已实现 copy constructor、copy assignment、move constructor 与 move assignment。编译器默认生成的版本会正确调用 `std::string` 的相应函数，类本身无须编写任何特殊代码。

相反的情形由 Rule of Three（三法则，Slide 51）刻画：若需要自定义 destructor，则通常也**必须**为类定义 copy constructor 与 copy assignment operator。原因在于：编写 destructor 往往意味着在手动处理动态内存的分配与释放，即亲自管理内存。此时编译器无法自动生成正确的版本——自动生成的拷贝只会执行 member-wise 的 shallow copy，无法正确处理手工管理的内存。以前述 `Vector` 为例，默认拷贝使两个对象共享同一块数组，析构时各自释放一次即产生错误。因此这三个函数必须成组提供：写了自定义 destructor，就应同时提供 copy constructor 与 copy assignment operator。

## 8. 四种特殊成员函数小结（Slides 52–53）

至此已详述四种 SMF（Slide 52）：

- **Default Constructor**：不接收参数创建对象，成员变量不做特殊实例化。
- **Copy Constructor**：以已有对象为蓝本逐成员创建新对象。
- **Copy Assignment Operator**：用一个已存在对象的内容替换另一个已存在对象。
- **Destructor**：对象离开作用域时被销毁。

加上尚未展开的两个 move 系函数，六种 SMF 构成完整集合。课件另附配套在线练习（Slide 53）供巩固之用。

## 9. 例题与解析：逐行辨析 `vector` 的构造与赋值（Slides 54–65）

以下函数以 `vector<int>` 呈现多种声明与赋值形式（Slide 54），试逐行判断每一行调用的是何种操作或函数：

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

逐行解析如下。

`vector<int> vec1;`（Slide 55）：不接收任何参数的构造，为 default constructor。

`vector<int> vec2(3);`（Slide 56）：调用接收 size 的自定义 constructor，属于 custom constructor 而非 SMF；`vec2` 含 3 个值为 0 的元素，而非一个值为 3 的元素。

`vector<int> vec3{3};`（Slide 57）：uniform initialization（统一初始化），同样不是 SMF。与上一行对照：大括号中的 `3` 表示"一个值为 3 的元素"。

`vector<int> vec4();`（Slide 58）：该行并非对象定义，而是函数声明——声明一个名为 `vec4`、不接收参数、返回 `vector<int>` 的函数。此即 C++ 中著名的 most vexing parse：本意为 default construction，编译器却将其解析为函数声明。

`vector<int> vec5(vec2);`（Slide 59）：以既有对象 `vec2` 构造新对象，为 copy constructor。

`vector<int> vec6{};`（Slide 60）：initializer list 为空，经 list initialization 构造出空 vector。

`vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};`（Slide 61）：list initialization，大括号内为计算所得的元素值。

`vector<int> vec8 = vec2;`（Slide 62）：`vec8` 在该行才诞生，等号表示初始化，故调用 copy constructor 而非 assignment。

`vec8 = vec2;`（Slide 63）：`vec8` 已经存在，两个已构造完成的对象之间赋值，这才是 copy assignment operator。

`return vec8;`（Slide 64）：按值返回需以 `vec8` 构造返回值对象，为 copy constructor。

函数签名中的参数 `vector<int> vec0`（Slide 65）：按值传参，实参到形参的构造同样是 copy constructor。本题的两处陷阱分别在于：等号不必然意味着 assignment；函数签名中隐蔽的按值传参同样触发 copy constructor。

## 10. 迈向 move semantics（Slides 66–70）

本讲最后考察剩余两种 SMF 的动机。已介绍的 default constructor、destructor、copy constructor 与 copy assignment operator 支持创建对象、销毁对象以及将一个对象的值复制给另一对象（Slide 67）；问题在于这套能力是否始终充分。

回看 `Widget` 的六个函数（Slide 68），尚未讨论的 move constructor 与 move assignment operator 正是为此存在：某些情形下，copy 语义是可避免的浪费。

典型场景如 Slide 69 所示：需将当前 `StringTable` 拷贝给另一个对象（后者以引用形式提供），而拷贝完成后，原对象已不再有任何用处。

```cpp
class StringTable {
public:
  StringTable() {}
  StringTable(const StringTable& st) {}
  // functions for insertion, erasure, lookup, etc.
  // but no move/dtor functionality
  // ...

private:
  std::map<int, std::string> values;
};
```

此时执行的 copy constructor 会将 `values` 这一 map 中的每一个值逐一拷贝，代价高昂；而原对象即将被丢弃，其中的数据本可以整体转移而非逐份复制。这种"复制抑或转移"的取舍，正是 move semantics（移动语义）的出发点。课件以一幅类比图收束本讲（Slide 70）：COPY 是在旁边原样另建一栋房屋，MOVE 是将家具从一栋房屋搬至另一栋——move semantics 的本质即 move or duplicate。该类比出自 Andreas Fertig 的报告 "Back to Basics: Move Semantics"。move constructor 与 move assignment operator 的具体实现及 `&&` 的含义，留待后续专讲。

## 本讲要点

- C++ 类共有六种 special member functions：default constructor `T()`、destructor `~T()`、copy constructor `T(const T&)`、copy assignment operator `T& operator=(const T&)`、move constructor `T(T&&)`、move assignment operator `T& operator=(T&&)`；编译器仅在某函数被实际调用且尚未被显式定义时，才自动生成其默认版本。
- 区分 copy constructor 与 copy assignment operator 的依据是等号左侧对象是否已存在：`Widget b = a;` 中 `b` 随语句诞生，为 copy constructor；`b = a;` 是两个已存在对象之间的 copy assignment operator。按值传参与按值返回同样触发 copy constructor。
- 默认拷贝是 member-wise copy；成员含指针时即退化为 shallow copy，多个对象共享同一块 heap 内存并互相影响，析构时还会重复释放。需要独立副本时应自行实现 deep copy：先 `new` 等容量的新数组，再逐元素拷贝。
- 在声明后附加 `= delete` 可显式移除某个 SMF 的功能，使误用代码在编译期报错；典型应用如 `PasswordManager` 禁止拷贝，以及 `std::unique_ptr` 满足 MoveConstructible/MoveAssignable 而不满足 CopyConstructible/CopyAssignable。
- 两条设计准则：Rule of Zero——默认 SMF 够用（尤其成员是 `std::string` 这类已实现全套 SMF 的 self-managing 类型）时不定义任何特殊函数；Rule of Three——需要自定义 destructor 即意味着手动管理动态内存，此时必须同时提供 copy constructor 与 copy assignment operator。
- 构造函数中初始化成员应优先使用 member initializer list：避免"默认构造后再赋值"的双重开销，且它是 const 成员与引用成员唯一的初始化途径。此外注意 `vector<int> vec4();` 声明的是函数而非对象（most vexing parse）；`vec2(3)` 创建 3 个元素，而 `vec3{3}` 创建 1 个值为 3 的元素。
