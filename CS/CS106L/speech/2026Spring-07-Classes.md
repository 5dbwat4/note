---
title: "Lecture 07 · Classes 逐字稿"
createAt: 2026/9/13
---

# Lecture 07: Classes（逐字稿）

> 对应课件转写：[2026Spring-07-Classes.md](../output/2026Spring-07-Classes.md)

## 1. 回顾与纲要（Slides 5–7）

本讲开篇以三道例题回顾 iterator hierarchy（迭代器层级）。该层级自下而上依次为 Random Access Iterator、Bidirectional Iterator、Forward Iterator，顶端分列为 Input Iterator 与 Output Iterator；图中箭头由更具体的类别指向其所泛化的更一般类别。转写的第二页图示补充了各类别的关键特征：Random Access Iterator 可以跳过元素（skip elements），Bidirectional Iterator 支持双向移动（multi direction），Forward Iterator 支持多遍扫描（multi pass），Input Iterator 与 Output Iterator 均为单遍扫描（single pass）。

**例题**：

1. Bidirectional Iterator 能完成哪些 Input Iterator 无法完成的操作？
2. Random Access Iterator 相比 Bidirectional Iterator 多出哪些能力？
3. `std::set<int>::iterator` 属于哪一类迭代器？

**解析**：

1. Input Iterator 为 single pass，只能自前向后完整遍历一遍；Bidirectional Iterator 为 multi direction，可以在遍历过程中后退，即支持双向移动。
2. Random Access Iterator 可以一次跳过若干元素、直接到达任意位置；Bidirectional Iterator 只能逐个前进或后退。
3. Bidirectional Iterator。`std::set` 的底层结构不支持随机跳跃，但支持双向遍历，与图中对该问题的标注一致。

本讲纲要共三部分：class（类）、inheritance（继承）与 virtuality（虚函数机制）。

## 2. 引入 class 的动机（Slides 8–24）

C 语言中没有 object（对象）：它既无法将数据与操作这些数据的函数封装为一个整体，也无法使用 object-oriented programming（OOP，面向对象程序设计）的设计模式。C++ 最初正是以 "C with classes"（带类的 C）为名设计的。OOP 以对象为中心，其核心工作在于 class 的设计与实现；class 是一种 user-defined type（用户自定义类型），object 则是以该类型声明的变量。二者关系可比作模具与成品：`class Cookie { ... };` 如同星形饼干模具，`Cookie c1;` 与 `Cookie c2;` 则是用该模具压制出的成品——一个 class 可以声明出任意多个 object。

值得注意的是，前几讲反复使用的 STL containers（容器）本身就是以 class 定义的：面向对象并非全新话题，而是既有内容的底层事实。

class 与 struct 的关系，Bjarne Stroustrup 在 The C++ Programming Language 参考手册（§4.4 Derived types）中给出过权威表述：class 包含一串各种类型的对象、一组操作这些对象的函数，以及一组对这些对象与函数的访问限制；而 structure 就是不带访问限制的 class。换言之，二者在 C++ 中几乎是同一机制，差别仅在访问控制。

struct 的问题在于其字段默认完全公开。以 StanfordID 为例：

```cpp
struct StanfordID {
    std::string name; // these are fields!
    std::string sunet;
    int idNumber;
};

StanfordID s;
s.name = "Preston Seay";
s.sunet = "pseay";
s.idNumber = 01243425;
s.idNumber = -12345;
```

`name`、`sunet`、`idNumber` 即 field（字段）。任何用户代码都可以直接改写它们：最后一行将 `idNumber` 随手改为 -12345 这样的无意义取值，课件对此行专门以注释警示。默认情况下，使用 struct 没有任何直接的访问控制，数据完全暴露在外。

class 提供的解决手段是访问控制，其基本形态如下：

```cpp
class ClassName {
private:

public:

}
```

（课件中类定义结尾的花括号后省略了分号，规范写法应为 `};`；本讲稿沿用课件原貌，此后不再逐处标注。）

class 内部可划分为 private 与 public 两种 section（区段）：public 成员对外可见，用户可以直接访问；private 成员对外封闭，用户代码被限制（restricted）访问，只能经由类提供的接口间接操作。这一机制即 encapsulation（封装）：哪些内容公开、哪些内容隐藏，由类的定义者决定。就直观而言，struct 相当于通体透明的背包，内部一目了然；class 则如同带有多层拉链隔层的背包，取放物品须经由设计好的开口。

## 3. 头文件、源文件与类的设计要素（Slides 25–29）

将 StanfordID 由 struct 改写为 class 之前，需要明确 C++ 工程中两类文件的区别：

| | Header File（.h） | Source File（.cpp） |
| :--- | :--- | :--- |
| 用途 | 定义接口（interface） | 实现类的函数 |
| 内容 | 函数原型、class 声明、类型定义、宏、常量 | 函数实现、可执行代码 |
| 使用方式 | 被多个源文件共享 | 编译为 object file |
| 示例 | `void someFunction();` | `void someFunction() {...}` |

概言之，`.h` 声明"能做什么"，`.cpp` 给出"怎么做"。

课件给出的 class 设计清单包含四项：constructor（构造函数）、private 的成员函数与成员变量、作为用户接口的 public 成员函数，以及 destructor（析构函数）。

## 4. 构造函数：声明与实现（Slides 30–48）

constructor 负责初始化新建对象的状态。对 StanfordID 而言，对象创建时即应确定 `name`、`sunet`、`idNumber` 三个成员的初值，而非依赖用户事后逐一赋值——这正是 struct 版本中三行裸赋值所做的事情。头文件中的声明如下：

```cpp
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    // constructor for our StudentID
    StanfordID(std::string name, std::string sunet, int idNumber);
    // method to get name, sunet, and idNumber, respectively
    std::string getName();
    std::string getSunet();
    int getID();
}
```

constructor 的语法特征是：函数名与类名相同，不写返回类型；参数即各成员的初值。getName、getSunet、getID 三个 getter（访问器）构成 public 接口，供外部读取成员。

实现在 .cpp 文件中完成：

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    idNumber = idNumber;
}
```

`StanfordID::` 中的 `::` 是 scope resolution operator（作用域解析运算符）：class 的作用域与 namespace（如 `std::`）同类。在类外定义成员函数时，必须以类名加 `::` 限定，表明这是 StanfordID 类的成员函数。

封装带来的直接收益是约束数据的能力。课件随后的版本意图只接受正的 `idNumber`：

```cpp
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    if ( idNumber > 0 ) idNumber = idNumber;
}
```

但这段代码存在缺陷，课件亦专门设问指出：`name = name;` 中赋值号两侧的 `name` 是同一个对象——函数参数。这是自我赋值，成员变量根本没有被写入；`if` 中的条件赋值同样落空。区分成员与同名参数需要 this 关键字：

```cpp
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    this->name = name;
    this->state = state;
    this->age = age;
}
```

this 指向当前对象本身，`this->name` 即"当前对象的 name 成员"，从而与参数 `name` 相区分。需要说明的是，课件后两行写作 `this->state = state;` 与 `this->age = age;`，与类定义中的成员名不符，应为 `this->sunet = sunet;` 与 `this->idNumber = idNumber;`（Slide 48 同此处理）。

C++11 提供了更简洁的 list initialization constructor（列表初始化构造函数）写法：

```cpp
// list initialization constructor
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber):
name{name}, sunet{sunet}, idNumber{idNumber} {};
```

参数表后以冒号引出初始化列表，对每个成员施以 uniform initialization（统一初始化，即花括号形式），一一完成初始化。

constructor 亦可以不带参数。default constructor（默认构造函数）为成员给出一套默认值：

```cpp
// default constructor
StanfordID::StanfordID() {
    name = "John Appleseed";
    sunet = "jappleseed";
    idNumber = 00000001;
}
```

带参与不带参两个 constructor 可以同时存在，构成 overload（重载）：编译器依据调用处的实参自动选定应调用的版本。Slide 48 将两个构造函数并置于同一 .cpp 文件中，其带参版本同样保留了 `this->state`、`this->age` 的笔误。

## 5. getter、setter 与 destructor（Slides 49–56）

三个 getter 的实现同样位于 .cpp 文件，定义时以 `StanfordID::` 限定、返回类型置首：

```cpp
std::string StanfordID::getName() {
    return this->name;
}

std::string StanfordID::getSunet() {
    return this->sunet;
}

int StanfordID::getID() {
    return this->idNumber;
}
```

读取成员经由 getter；修改成员则经由 setter（设置器）：

```cpp
void StanfordID::setName(std::string name) {
    this->name = name;
}

void StanfordID::setSunet(std::string sunet) {
    this->sunet = sunet;
}

void StanfordID::setID(int idNumber) {
    if (idNumber >= 0){
        this->idNumber = idNumber;
    }
}
```

setter 是带校验的写入口：`setID` 仅在 `idNumber >= 0` 时执行赋值，负值被直接拒绝。数据由此改由类自身守护，struct 时代 `s.idNumber = -12345;` 的问题得到治理。

设计清单的最后一项是 destructor（析构函数），函数名为前置波浪号的类名：

```cpp
StanfordID::~StanfordID() {
    // free/deallocate any data here
}
```

析构函数负责对象生命周期结束时的清理工作，例如释放动态分配的内存。StanfordID 未以 new 关键字动态分配任何数据，故其函数体为空；但 destructor 是对象生命周期的重要组成部分。作为示意，若类持有动态数组，析构函数中应有 `delete [] my_array;` 之类的释放语句。destructor 不需要显式调用：当对象离开其作用域时，它会被自动调用。

## 6. 类内的类型别名（Slides 57–58）

type aliasing（类型别名）允许为既有类型创建同义标识符。STL 的 vector 内部即采用了这一手段：

```cpp
template <typename T>
class vector {
    using iterator = T*;

    // Implementation details...
};
```

`using iterator = T*;` 声明于类作用域内，`iterator` 由此成为 `T*` 的别名。StanfordID 亦可如法处理：在 private 区段写 `using String = std::string;`，此后全类以 `String` 代替 `std::string`，成员变量、constructor 参数与 getter 返回类型均相应改写。类内别名既缩短书写，也便于将来统一替换底层类型。

## 7. 练习（Slide 60）

课件布置了练习任务：实现 wizard（巫师）类与 spellbook（法术书）类，使 wizard 能够施放法术；配套在线编程环境见该页给出的链接。该练习综合考查本讲前半部分的 class 设计要素。

## 8. 继承（Slides 61–79）

第二部分讨论 inheritance（继承）。继承指子类（sub class）自基类（base class）获得内容并加以扩展：一个基类可以派生出多个子类。标准库的 I/O 流体系即是现成的例证：`ios_base` 之下是 `basic_ios<CharT, Traits>`，其下分出 `basic_ostream` 与 `basic_istream`，再分别派生 `basic_ostringstream`、`basic_ofstream` 与 `basic_istringstream`、`basic_ifstream`；`basic_iostream` 同时继承 `basic_ostream` 与 `basic_istream`，其下又有 `basic_stringstream` 与 `basic_fstream`。此前见过的这张层级图，其全部箭头都是继承关系——标准库本身大量使用继承。

课件给出采用继承的两个理由。其一，dynamic polymorphism（动态多态）：不同类型的对象可能需要同一套接口。其二，extensibility（可扩展性）：通过创建带有特定属性的子类来扩展既有类。

以几何形体为例：切顶圆锥、棱锥、立方体、长方体、正多面体、半球等十余种形状各不相同，但若设计一个 shape 类，"面积"（area）是所有形状共有的属性；radius、height、width 这类尺寸则因形状而异，不具普遍性。据此可以给出只承诺接口的基类：

```cpp
class Shape {
public:
    virtual double area() const = 0;
};
```

`virtual double area() const = 0;` 是 pure virtual function（纯虚函数）：它在基类中仅作声明而不提供实现，由子类覆盖（overwrite）——这正是 dynamic polymorphism 的实现机制。`= 0` 为纯虚标记；`const` 修饰表明该函数不修改对象自身状态。Shape 只约定"任何形状都可计算面积"，不涉及具体算法。

第一个子类 Circle 如下：

```cpp
class Shape {
public:
    virtual double area() const = 0;
};

class Circle : public Shape {
public:
    // constructor
    Circle(double radius): _radius{radius} {};
    double area() const {
        return 3.14 * _radius * _radius;
    }
private:
    double _radius;
};
```

逐项分析：`class Circle : public Shape` 声明 Circle 类继承自 Shape 类；构造函数 `Circle(double radius): _radius{radius} {};` 采用前述列表初始化写法，将半径直接初始化进成员；成员函数 `area()` 覆盖了基类在 Shape 中声明的 `area()`，给出圆的面积公式；`_radius` 置于 private 区段，外部仅能通过 public 接口与对象交互。对类变量的这种 encapsulation 正是继承的优点之一：数据仍由类自己看管。

Rectangle 沿用同一模式：

```cpp
class Shape {
public:
    virtual double area() const = 0;
};
. . . .
class Rectangle: public Shape {
public:
    // constructor
    Rectangle(double height, double width):
        _height{height}, _width{width} {};
    double area() const {
        return _width * _height;
    }
private:
    double _width, _height;
};
```

将 Circle 与 Rectangle 并置比较：两者类名不同、私有数据不同（前者仅 `_radius`，后者为 `_width` 与 `_height`）、构造函数参数不同，但都继承自 Shape 并实现了同一个 `area()` 接口。同一接口、各自实现，即继承与多态所要达成的效果。

## 9. 三种继承方式（Slides 80–84）

`class B : ??? A` 中的继承标号可为 public、protected 或 private，三者的成员可见性规则如下。

public 继承（`class B: public A {...}`）：基类的 public 成员在派生类中仍为 public；protected 成员保持 protected；private 成员在派生类中不可访问。

protected 继承（`class B: protected A {...}`）：基类的 public 成员在派生类中降为 protected；protected 成员仍为 protected；private 成员不可访问。

private 继承（`class B: private A {...}`）：基类的 public 成员与 protected 成员在派生类中均变为 private；private 成员不可访问。

可见，继承方式决定的是基类 public 与 protected 成员在派生类中的地位；而基类的 private 成员在任何继承方式下都不对派生类开放。

## 10. 例题：MyStack 应采用何种继承（Slides 85–88）

先比较两个 STL 容器的公开接口。vector 提供 `push_back`（在尾部添加元素）、`emplace_back`（C++11，在尾部原地构造元素）、`append_range`（C++23，在尾部追加一段元素）与 `pop_back`（移除最后一个元素），均为 public member function；stack 提供 `push`（在栈顶插入元素）、`push_range`（C++23，在栈顶插入一段元素）、`emplace`（C++11，在栈顶原地构造元素）与 `pop`（移除栈顶元素）。stack 仅暴露"顶端"一个操作口，vector 则完全敞开。

**例题**：以 MyVector 为底层实现 MyStack，继承标号处应填入什么？

```cpp
class MyStack : ________ MyVector {
    ...
};
```

**解析**：候选为 public、protected、private。若填 public，用户将能直接调用 vector 的插入接口向栈中写入，栈的语义即被破坏；若填 protected，子类仍可使用该 vector，功能上可行，但子类并不需要把 vector 继续暴露给更深的派生层次；若填 private，除 MyStack 自身外，无人需要访问、甚至需要知晓该 vector 的存在。故应填 private。此例表明：选择继承方式的实质，是决定基类接口向外界延续暴露的程度。

## 11. 菱形继承与虚继承（Slides 89–98）

第三部分 virtuality 由一个经典问题引入：the diamond problem（菱形继承问题）。设 B、C 均继承自 A，D 同时继承 B 与 C。由于 B 与 C 各自都会调用 A 的 constructor，D 最终携带两份 A：一份来自 B，另一份来自 C。四类的定义如下：

```cpp
class A {
public:
    A();
    void hello() {
        // print "hello from A"
    }
}

class C : public A {
public:
    C();
}

class B : public A {
public:
    B();
}

class D
: public B, public C {
public:
    D();
}
```

A 定义了 `hello()`；B、C 公开继承 A；D 以逗号分隔、同时公开继承 B 与 C。

**例题**：给定 `D obj {};`，下列三个调用分别发生什么？

```cpp
obj.B::hello()
obj.C::hello()
obj.hello()
```

**解析**：`obj.B::hello()` 以作用域解析显式指明经由 B 的路径，调用 B 的 hello；`obj.C::hello()` 同理经由 C；而 `obj.hello()` 未指明路径——D 内存在两份 A，因而有两个来路不同的 hello，该调用具有二义性（ambiguity）。这正是菱形继承的核心困难。

解决方法是令 B、C 以 virtual 方式继承 A：

```cpp
class C : virtual public A {
public:
    C();
}

class B : virtual public A {
public:
    B();
}
```

virtual inheritance（虚继承）的含义是：派生类——此处为 D——对基类 A 只保有一份共享实例。在继承标号前加 `virtual` 关键字后，B 与 C 之间共享同一个 A 的实例，D 中便只剩一份 A。此时再执行 `obj.hello()` 即不再有二义。

## 12. virtual 的语义与 vtable（Slides 99–100）

virtual 一词的本义是"本质上存在，而非字面存在"（existing in essence, but not literally）。在 C++ 中，virtual 意味着程序会建立 virtual table（vtable，虚函数表）：每个对象内含一个 vpointer（虚表指针），指向其所属类的 vtable，真正被调用的函数入口记录在表中。以课件的示例而言：class B 的 vtable 中，bar 指向 `B::bar()`，quux 指向 `B::quux()`；class C 的 vtable 中，bar 指向其覆盖后的 `C::bar()`，而 quux 未被 C 覆盖，仍指向 `B::quux()` 的实现。函数调用因此不是在编译期写死，而是沿虚表在运行时查得。课件以 "Goodbye to static typing" 概括这一点：经由 virtual 实现的多态带来了 dynamic typing 的行为，函数调用的绑定被推迟到运行时完成。

Slide 101 为代码演示页，文字讲稿从略。

## 本讲要点

- class 借助 private/public 区段实现 encapsulation：数据藏于 private，用户仅能经由 public 接口（constructor、getter、setter）访问对象，类可借接口对数据施加约束（如 `setID` 拒绝负值），而 struct 默认不含任何访问限制。
- constructor 与类同名、无返回类型；类外定义成员函数须以 `类名::` 限定；参数与成员同名时以 `this->` 消除歧义，更推荐 C++11 的列表初始化写法（冒号引出、花括号逐一初始化）；default constructor 与带参 constructor 可重载共存。destructor（`~类名`）在对象离开作用域时自动调用，负责资源清理。
- 类内 `using` 可定义类型别名（如 vector 的 `using iterator = T*;`、StanfordID 的 `using String = std::string;`）。
- inheritance 使子类复用并扩展基类；pure virtual function（`virtual double area() const = 0;`）在基类仅声明接口、由子类覆盖，构成 dynamic polymorphism 的机制；继承方式有 public、protected、private 三种，基类 private 成员对派生类永远不可见，实现细节无须外露时应选 private 继承（如 MyStack 之于 MyVector）。
- 多重继承可能产生菱形问题：D 同时经由 B、C 获得两份 A，`obj.hello()` 出现二义；令 B、C 以 `virtual public A` 虚继承，D 即只保留一份 A。virtual 的底层机制是 vtable：对象经 vpointer 在运行时查表确定调用目标，多态由此具备动态绑定的性质。
