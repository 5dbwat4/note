---
title: "Lecture 09 · Template Classes 逐字稿"
createAt: 2026/9/13
---

# Lecture 09: Template Classes（逐字稿）

> 对应课件转写：[2026Spring-09-TemplateClasses.md](../output/2026Spring-09-TemplateClasses.md)

## 1. 引入：为不同类型重复实现（Slides 2–8）

本讲主题为 template classes（模板类），内容分为两个部分：其一讨论如何借助 template 在不同类型之间泛化同一份逻辑；其二讨论 const correctness（const 正确性）。

课程以一个反复出现的需求场景引入 template 的动机。假设最初的需求是存储一列整数（integers），一个直观的做法是定义一个专门的类：

```cpp
class IntVector {
// Code to store
// a list of
// integers…
};
```

结合完整的接口定义（Slide 5）可以看得更清楚：

```cpp
// Implements a sequence of strings
class IntVector {
public:
    IntVector();
    ~IntVector();

    size_t size();
    bool empty();

    void push_back(const int& elem);
    int& operator[](size_t index);
};
```

需要指出，这段代码的首行注释写作 "a sequence of strings"，与该类实际存储的整数类型不符；此为课件原文的笔误，引用时保持原样，不影响后续讨论。

当需求变为存储一列 double 时，上述实现几乎可以原样复用，唯一的变化是将 `int` 全部替换为 `double`：

```cpp
class DoubleVector {
    // Code to store
    // a list of
    // doubles…
};
```

两份代码的逻辑完全相同，仅元素类型不同。若需求继续扩展到字符串乃至其他类型，逐一复制类定义的方式显然难以持续。课件 Slide 12 的图示将三个并列的类定义经由一个箭头收敛为单个模板定义，直观呈现了这一化简过程，这正是 template 所要解决的问题。

## 2. 需求清单与 template 方案（Slides 9–13）

在逐一为每种类型编写实现之前，需要先评估需求的完整范围。课件以 "Not so fast…" 一页暂止了继续复制类定义的思路，并列出一个向量类可能面对的需求清单：

- Vector of **doubles**?
- Vector of **std::string**?
- Vector of **vector of strings**?
- Vector of **custom type I haven't even thought of yet**?

最后一项尤为关键：使用者未来可能使用任何类型，包括目前尚未定义的自定义类型。课件在此配以 STL 的创造者 Alexander Stepanov 的照片，意在说明这份需求清单正是标准模板库的设计者当年面对的问题。为每种类型手写一份类定义既不可行也不必要。由此引出本讲的核心设想：What if we could keep the logic, but change the type?——若能保留逻辑而只改变类型，上述需求便可一并满足。

这一设想的解决方案即 template：

```cpp
template <typename T>
class vector {
    // So satisfying.
};

vector<int> v1;
vector<double> v2;
vector<string> v3;
```

原本三个并列的类定义（`IntVector`、`DoubleVector`、`StringVector`）被统一为一个参数化的 `vector`，并通过 `vector<int>`、`vector<double>`、`vector<string>` 分别获得针对特定类型的版本。标准库中的 `std::vector<T>` 即按此思路构建。本讲要回答的核心问题是：`<T>` 这一语法究竟如何工作。

## 3. 历史：以宏实现代码生成（Slides 17–27）

在给出 template 的语法之前，有必要回顾 template 出现之前的历史方案。将 `IntVector` 补充完整：

```cpp
class IntVector {
public:
    int& at(size_t index);
    void push_back(const int& elem);
private:
    int* elems;
    size_t logical_size;
    size_t array_size;
};
```

将该定义中所有 `int` 的出现位置标出，共四处：类名 `IntVector` 中的 "Int"、`at` 的返回类型 `int&`、`push_back` 的参数类型 `const int&`，以及成员变量 `int* elems`。除这四处之外，整个类定义对其余任何元素类型都是相同的。换言之，两个"向量类"之间的差异可以完全归结为这四处类型。

在 template 诞生之前，这类重复可以通过 preprocessor macro（预处理器宏）消除。课件 Slide 21 的版本缺少宏续行符，此处按 Slide 22 的完整版本引用：

```cpp
#define GENERATE_VECTOR(MY_TYPE) \
    class MY_TYPE##Vector {
public:
    MY_TYPE& at(size_t index);
    void push_back(const MY_TYPE& elem); \
private:
    MY_TYPE* elems;
    size_t logical_size;
    size_t array_size;
};
```

对此宏有两点说明。其一，preprocessor macro 在编译器处理之前运行，其实质是纯文本替换。其二，`##` 是 token-pasting operator（记号粘贴运算符），用于将两个记号拼接为一个：当 `MY_TYPE` 为 `int` 时，`MY_TYPE##Vector` 生成类名 `intVector`。

宏的调用方式如下：

```cpp
#include "old_fashioned_template.h"

GENERATE_VECTOR(int)

intVector v1;
v1.push_back(5);
```

`GENERATE_VECTOR(int)` 在预处理阶段被展开，在原地生成完整的 `intVector` 类定义：

```cpp
class intVector {
public:
    int& at(size_t index);
    void push_back(const int& elem);
private:
    int* elems;
    size_t logical_size;
    size_t array_size;
};

intVector v1;
v1.push_back(5);
```

这已经是事实上的代码生成（code generation）：传入的类型不同，得到的 vector 也不同。由于展开发生在编译器处理代码之前，编译器自始至终只见到展开后的 `intVector`。但其实现手段是预处理器的不区分类型的文本替换，由此带来若干缺陷：

- 语法笨重（clunky syntax）；
- 难以进行类型检查（hard to type check）：预处理器不理解类型，编译器面对的是替换后的文本，出错时难以定位；
- 调用时机无法约束：若忘记调用宏，类根本不存在；若重复调用，则产生重复定义。

据此得出本讲的关键论断：**Templates automate code generation**。template 将宏所承担的代码生成工作交还给编译器，同时获得类型检查的保障。

## 4. 类模板语法与 template instantiation（Slides 28–34）

现代 C++ 的写法如下：

```cpp
template <typename T>
class Vector {
public:
    T& at(size_t index);
    void push_back(const T& elem);
private:
    T* elems;
};
```

首行 `template <typename T>` 称为 template declaration（模板声明），其含义是：`Vector` 是一个 template，接受一个类型名 `T`。类体中出现的 `T` 是占位符，在 `Vector` 被 instantiate（实例化）时替换为具体类型。

使用方式是在类名后以尖括号提供类型实参：

```cpp
Vector<int> intVec;
Vector<double> doubleVec;
Vector<std::string> strVec;

Vector<Vector<int>> vecVec;

struct MyCustomType {};
Vector<MyCustomType> structVec;
```

这一过程称为 template instantiation（模板实例化）：**特定类型的代码按需生成**——程序中使用 `Vector<int>` 时，编译器才生成 `int` 版本的代码。类型实参几乎没有限制：既可以是基本类型，也可以嵌套（`Vector<Vector<int>>`），还可以是刚刚定义的自定义类型 `MyCustomType`。这正回应了需求清单中"尚未想到的类型"一项。

Slide 30 将上述过程等价地呈现为：程序员书写

```cpp
template <typename T>
class Vector {
    T& at(size_t index);
    // More methods...
};

Vector<int> v;
```

编译器则产出与手写无异的代码：

```cpp
class IntVector {
    int& at(size_t index);
    // More methods...
};

IntVector v;
```

编译器承担了当年宏所承担的代码生成工作，且这一过程是类型感知、可检查的。

理解 template 的一个有效类比是工厂（factory）：`template <typename T> class Vector` 是工厂本身，类型（如 `int`、`string`）从一端投入，产品（如 `Vector<int>`、`Vector<string>`）从另一端产出。

据此需要严格区分两个概念：

- `template <typename T> class Vector` 是一个 template，**不是** type（类型）；
- `Vector<std::string>` 是一个 type，亦称 template instantiation（模板实例）。

工厂类比同样适用于这一区分：模板是工厂，实例化得到的类型才是产品。

## 5. 例题与解析：同一模板的不同实例（Slides 35–36）

例题：判断下列代码能否通过编译。

```cpp
void foo(std::vector<int> v);

int main() {
    std::vector<double> v;
    foo(v);
}
```

解析：不能通过编译，错误信息为 "No suitable user-defined conversion from \"std::vector<double>\" to \"std::vector<int>\" exists"，即不存在从 `std::vector<double>` 到 `std::vector<int>` 的合适转换。

结论与依据是：同一个 template 的两个 instantiation 是**完全不同的类型**，这一差异同时体现在编译期与运行期。二者虽出自同一模板，但类型系统对它们的处理如同两个无关的类：模板实参不同，实例化的产物之间就不存在任何关联。因此 `Vector<double>` 与 `Vector<int>` 之间没有任何隐式转换，这与 `int` 和某个无关自定义类型之间不存在转换是同样的情形。

课件就此给出对照：在 Java 一类语言中，`ArrayList<int>` 与 `ArrayList<double>` 共享同一个 runtime type（Java 泛型采用类型擦除，运行期不区分二者）；C++ 的 template 则为每个类型实参生成独立的代码，二者在运行期就是不同的类型。

## 6. 非类型 template parameter（Slides 37–39）

template parameter（模板参数）并非只能是类型。除类型参数外，模板参数还可以是编译期常量：

```cpp
template <typename T>
class Vector{};
```

```cpp
template <size_t N>
class SizeTemplate {};

SizeTemplate<5> s;
```

```cpp
template <bool B>
class BoolTemplate {};

BoolTemplate<true> b;
```

`template <size_t N>` 接受一个 `size_t` 值，`template <bool B>` 接受一个 `bool` 值。尖括号内因此既可以出现类型，也可以出现编译期常量。

该特性最具代表性的应用是 `std::array`：

```cpp
template<typename T, std::size_t N>
struct std::array { /* ... */ };

// An array of exactly 5 strings
std::array<std::string, 5> arr;
```

`std::array` 同时接受一个类型参数 `T` 与一个非类型参数 `N`，上例表示"恰好容纳 5 个 `std::string` 的数组"。相较于 `vector`，`array` 的优势在于避免堆分配：大小 `N` 直接编码进类型之中，编译器确切知道 `array<string, 5>` 所占的空间，因而可以将其分配在栈上。

## 7. 类模板的三个语法细节（Slides 40–52）

使用 template class 时，有三件与直觉不符的事情需要注意。

### 7.1 源文件中必须重复 template 声明（Slides 41–44）

常见的写法是在头文件中声明、源文件中实现：

```cpp
// Vector.h
template <typename T>
class Vector {
public:
    T& at(size_t i);
};
```

```cpp
// Vector.cpp
T& Vector::at(size_t i) {
    // Implementation...
}
```

`Vector.cpp` 中的写法无法通过编译：返回类型 `T&` 中的 `T` 不在任何模板声明的作用域内。编译器的反馈是 "I don't know what T is!"——它无从得知 `T` 是什么。修正方法是将 template declaration 复制到每个成员函数定义之前：

```cpp
// Vector.cpp

template <typename T>
T& Vector::at(size_t i) {
    // Implementation...
}
```

此处仍有一个问题：类名限定符 `Vector::` 不正确。课件对此的原话是 "Vector is not a type, but Vector<T> is"，依据仍是第 4 节的区分——`Vector` 本身不是类型，`Vector<T>` 才是。因此作用域必须写作 `Vector<T>::`：

```cpp
// Vector.cpp

template <typename T>
T& Vector<T>::at(size_t i) {
    // Implementation...
}
```

### 7.2 头文件在末尾包含源文件（Slides 45–48）

非模板类的组织方式是源文件包含头文件：

```cpp
// StrVector.h

class StrVector {
public:
    string& at(size_t i);
};
```

```cpp
// StrVector.cpp

#include "StrVector.h"

string& StrVector::at(size_t i)
{
    // Implementation...
}
```

模板类恰好相反：**`.h` 文件须在末尾包含 `.cpp` 文件**：

```cpp
// Vector.h

template <typename T>
class Vector {
public:
    T& at(size_t i);
};

#include "Vector.cpp"
```

```cpp
// Vector.cpp

template <typename T>
T& Vector<T>::at(size_t i) {
    // Implementation...
}
```

这一反常组织方式源于编译器（与链接器）实现模板代码生成的机制。课件指出无需深究其原理；同时存在绕开这一写法的其他组织方式。

### 7.3 typename 与 class 等价（Slides 49–52）

在 template parameter list 中，`typename` 与 `class` 完全等价：

```cpp
template <typename T>
class Vector{};
```

```cpp
template <class T>
class Vector{};
```

两个参数的情形下，四种关键词组合亦全部等价：

```cpp
template <typename K, typename V>
struct pair;
```

```cpp
template <class K, class V>
struct pair;
```

```cpp
template <class K, typename V>
struct pair;
```

```cpp
template <typename K, class V>
struct pair;
```

即 `typename` 与 `class` 可以任意混用。需要说明的是，这一等价关系仅限于 template parameter list 这一位置；`class` 与 `typename` 在其他语境中各有不同的含义。

## 8. 问题的提出：const 对象与成员函数（Slides 56–59）

在 `Vector<T>` 实现的基础上，本讲转入 const correctness 的讨论。考察如下函数：

```cpp
void printVec(const Vector<int>& v) {
  for (size_t i = 0; i < v.size(); i++) {
    std::cout << v.at(i) << " ";
  }
  std::cout << std::endl;
}
```

该函数无法通过编译，错误为 "No such method size!"。而 `Vector` 的定义中明确声明了 `size`：

```cpp
template<class T>
class Vector {
public:
    size_t size();
    bool empty();

    T& operator[] (size_t index);
    T& at(size_t index);
    void push_back(const T& elem);
};
```

问题出在参数 `const Vector<int>& v` 上：

- 将 `v` 声明为 `const`，即向编译器承诺不修改 `v`；
- 编译器无法确定 `size`、`at` 等方法是否会修改 `v`——member function 本可以访问乃至修改 member variables；
- 编译器不分析函数体，只依据声明做判断。既然无法保证调用不修改对象，`const` 对象上便不允许调用任何非 const 方法。

## 9. const method 与 const interface（Slides 60–66）

解决方法是引入 const method（const 成员函数），即在成员函数声明的参数列表之后添加 `const`：

```cpp
template<class T>
class Vector {
public:
    size_t size() const;
    bool empty() const;

    T& operator[] (size_t index);
    T& at(size_t index) const;
    void push_back(const T& elem);
};
```

尾部 `const` 的语义是一份面向编译器的契约：声明"该成员函数不会修改对象"，并请编译器据此进行检查与问责。其价值在于将"是否修改对象"从实现细节上升为接口承诺：调用者只需查看签名即可知晓调用的副作用，编译器则在契约被违背之处报错。

`.cpp` 中的实现必须同步添加 `const`，否则声明与定义不一致，编译无法通过：

```cpp
template <class T>
size_t Vector<T>::size() const {
    return logical_size;
}

// Other methods...
```

若在 const method 内尝试修改成员变量：

```cpp
template <class T>
size_t Vector<T>::size() const {
    this->logical_size = 106;
    return logical_size;
}

// error: cannot assign to non-static data member
// within const member function 'size'
```

编译器将拒绝该赋值。其机制在于：**在 const method 内部，`this` 的类型是 `const Vector<T>*`**。

这一规则并不限于模板。以 `Point` 类为对照，普通成员函数中：

```cpp
void Point::setX(int x)
{
    this->x = x;
}
```

`this` 的类型为 `Point*`；而 const 成员函数中：

```cpp
int Point::getX(int x)
const
{
    return this->x;
}
```

`this` 的类型为 `const Point*`。成员函数是否为 const，决定了其内部 `this` 的类型。

由此得到 const interface（const 接口）的概念：被标记为 `const` 的对象只能使用该类的 const interface，即声明为 `const` 的成员函数。从 `const Vector<T>` 的视角看，前述类的接口收窄为：

```cpp
template<class T>
class Vector {
public:
    size_t size() const;
    bool empty() const;
    void push_back(const T& elem);  // 非 const method，const 对象不可调用（课件中划除）
private:
    const size_t logical_size;
    const T* elems;
};
```

`push_back` 不在 const interface 之内，const 对象无权调用；同时所有数据成员在 const 对象的视角下均为 const，只读。

## 10. printVec 的修复（Slides 67–70）

`printVec` 此前的编译错误，正是因为 `size` 与 `at` 不在 const interface 之中。编译器给出的信息可引述为 "const Vector<int> has no size, at!!!"：在 `const Vector<int>` 上，找不到可调用的 `size` 与 `at`。修复原则是：**为所有不修改 `Vector` 的成员函数添加 `const`**：

```cpp
template<class T>
class Vector {
public:
    size_t size() const;
    bool empty() const;

    T& operator[] (size_t index);
    T& at(size_t index) const;
    void push_back(const T& elem);
};
```

`size`、`empty`、`at` 均为只读操作，标记为 `const`；`operator[]` 与 `push_back` 会修改对象，保持非 const。经此修改，`printVec` 顺利通过编译，编译器确认 "Everything looks good to me!"。

## 11. 例题与解析：at 声明的问题（Slides 71–74）

例题：针对修改后的声明 `T& at(size_t index) const;`，指出其存在的问题。课件的提示是：该声明至少存在一个问题，也可能有两个。

解析之一（Problem #1：const 使用者竟能修改对象）：该函数虽为 const method，返回的却是非 const 引用 `T&`。于是下列代码可以通过编译：

```cpp
T& at(size_t index) const;

void oops(const Vector<int>& v) {
    v.at(0) = 42;
}
```

`v` 的类型是 `const Vector<int>&`，本不应被修改；但 `at` 返回的 `T&` 指向 vector 内部元素，对它赋值即绕过了 `v` 的 const 保护，实际修改了 const 对象的内容。需要注意，`at` 本身并未修改对象——问题在于其返回类型为函数外部的修改提供了通道。

解决方案是让 const 版本的 `at` 返回 const 引用：

```cpp
template<class T>
class Vector {
public:
    size_t size() const;
    bool empty() const;

    T& operator[] (size_t index);
    const T& at(size_t index) const;
    void push_back(const T& elem);
};
```

解析之二（Problem #2：非 const 使用者无法修改）：返回 `const T&` 之后出现了对称的新问题：

```cpp
const T& at(size_t index) const;

void ooh(Vector<int>& v) {
    v.at(0) = 42;
}
```

此时代码报错 "Can't assign to const int&"。持有完全可修改的 `Vector<int>` 的调用者，合法的元素更新需求 `v.at(0) = 42` 也无法完成。返回 const 引用保护了 const 对象，却剥夺了普通对象的写操作。

## 12. const overloading（Slides 75–78）

两个问题共同指向的解决方法是 const overloading（const 重载）：为 `at` 定义两个版本，其一服务于 `const` 实例，其二服务于非 `const` 实例：

```cpp
template<class T>
class Vector {
public:
    const T& at(size_t index) const;
    T& at(size_t index);
...
};
```

成员函数可以仅凭尾部的 `const` 构成重载：const 对象上的调用匹配 const 版本，非 const 对象上的调用匹配非 const 版本。这一选择机制的细节在第 15 节说明。二者的实现位于 `.cpp`：

```cpp
template <class T>
const T& Vector<T>::at(size_t index) const {
    return elems[index];
}

template <class T>
T& Vector<T>::at(size_t index) {
    return elems[index];
}
```

两个版本的函数体完全相同，仅返回类型与尾部 `const` 不同。课件明确承认这一冗余：两个方法实现一致略显多余，但函数体仅一行，尚可接受。

## 13. findElement 与冗余的扩大（Slides 79–81）

一行的冗余尚可容忍，多行则不然。为 `Vector` 增加按值查找的 `findElement` 之后，声明变为四项：

```cpp
template<class T>
class Vector {
public:
    T& at(size_t index);
    const T& at(size_t index) const;
    T& findElement(const T& value);
    const T& findElement(const T& value) const;
...};
```

非 const 版本的实现如下：

```cpp
template <typename T>
T& Vector<T>::findElement(const T& value) {
  for (size_t i = 0; i < logical_size; i++) {
    if (elems[i] == elem) return elems[i];
  }
  throw std::out_of_range("Element not found");
}

// What about the const version of findElement?
```

其逻辑为遍历全部元素，命中则返回引用，否则抛出 `std::out_of_range`。此处需要说明一处原文细节：该页循环条件写作 `elems[i] == elem`，而函数参数名为 `value`，二者指同一对象；Slides 80、81、83 均存在这一参数名不一致，属于课件原文笔误，后续 Slide 92 的最终版本统一为 `value`。

const 版本若沿用现有模式，只能整体复制实现并修改签名：

```cpp
template <typename T>
const T& Vector<T>::findElement(const T& value) const {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == elem) return elems[i];
    }
    throw std::out_of_range("Element not found");
}
```

该方案可行但冗余严重。课件的评注是 "This works, but it's super redundant. There must be a better way!"：`at` 的重复仅一行，`findElement` 的重复达五行，且每新增一个查询类方法都要复制一整套实现。课件由此引出更优方案。

## 14. const_cast 与委托实现（Slides 82–90）

引入该方案之前，先补充一个工具。Casting（类型转换）指将一种类型转换为另一种类型的过程；C++ 提供多种 cast 手段，其中 `const_cast` 允许"转换掉"变量的 const 属性（const-ness），语法为 `const_cast<target_type>(expression)`。

借助 `const_cast`，const 版本的 `findElement` 无需复制实现，函数体压缩为一行委托。非 const 版本承载全部逻辑：

```cpp
template <typename T>
T& Vector<T>::findElement(const T& value) {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == elem) return elems[i];
    }
    throw std::out_of_range("Element not found");
}
```

const 版本仅做转发：

```cpp
template <typename T>
const T& Vector<T>::findElement(const T& value) const {
    return const_cast<Vector<T>&>(*this).findElement(value);
}
```

冗余由此消除。课件 Slides 85–90 以多张逐级放大的标注图反复申明同一要点：`const_cast` 的作用即 "casts away the const"，剥除 const 限定。以下自内向外解析这行委托代码：

```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

- `*this`：当前处于 const method 之中，`this` 的类型为 `const Vector<T>*`；解引用得到 `const Vector<T>`，取其引用即 `const Vector<T>&`；
- `<Vector<T>&>`：`const_cast` 的目标类型，即非 const 引用，是"所期望的类型"；
- `const_cast`：移除表达式的 const 属性，将 `const Vector<T>&` 转换为 `Vector<T>&`；
- `.findElement(value)`：转换之后，编译器面对的是非 const 对象上的调用，因而选中非 const 版本的 `findElement`，即承载真实逻辑的版本。

概括而言：在 const 方法内部，将 `*this` 恢复为非 const 引用，从而调用非 const 重载。

## 15. 重载决议与 const_cast 的使用边界（Slides 91–93）

编译器之所以选择非 const 版本，依据是 overload resolution（重载决议）规则。类中并存两组重载：

```cpp
template<class T>
class Vector {
public:
    T& at(size_t index);
    const T& at(size_t index) const;
    T& findElement(const T& value);
    const T& findElement(const T& value) const;
};
```

调用者对象的 const 属性决定匹配哪个重载：const 对象匹配尾部带 `const` 的版本，非 const 对象匹配不带 `const` 的版本；换言之，const 属性在重载决议中的地位与参数类型相同。`const_cast` 之后对象被视为非 const，故选中的是 `T& findElement(const T& value)`。完整实现如下：

```cpp
template <typename T>
T& Vector<T>::findElement(const T& value) {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == value) return elems[i];
    }
    throw std::out_of_range("Element not found");
}

template <typename T>
const T& Vector<T>::findElement(const T& value) const {
    return const_cast<Vector<T>&>(*this).findElement(value);
}
```

此页代码中循环条件已统一为 `elems[i] == value`。

至于 `const_cast` 的适用范围，课件的回答十分明确：几乎从不使用。`const_cast` 等于告知编译器"不必担心，我已确认无误"，实际上是主动放弃编译器对 const 的检查；若确需一个可修改的值，正确做法是最初就不声明为 `const`。`const_cast` 的正当使用场景极少，const 版本委托非 const 版本属于少数经典用法之一。

## 16. mutable：成员粒度的可变性（Slides 95–97）

`const_cast` 的作用粒度是整个对象：一经施用，整个对象都变为可修改。课件由此提出问题：是否存在更细粒度（fine-grained）的手段，只放开单个成员？C++ 对此提供的工具是 `mutable` 关键字。与 `const_cast` 相同，`mutable` 同样绕过 const 保护，使用时须谨慎：

```cpp
struct MutableStruct {
    int dontTouchThis;
    mutable double iCanChange;
};

const MutableStruct cm;
// cm.dontTouchThis = 42; // Not allowed, cm is const
cm.iCanChange = 3.14;       // Ok, iCanChange is mutable
```

对象 `cm` 整体为 const，普通成员 `dontTouchThis` 不可修改；声明为 `mutable` 的成员 `iCanChange` 在 const 对象上仍可写。二者的差异在于粒度：`const_cast` 面向整个对象，`mutable` 面向单个成员。

`mutable` 的典型应用是存储调试信息：

```cpp
struct CameraRay {
    Point origin;
    Direction direction;
    mutable Color debugColor;
};

void renderRay(const CameraRay& ray) {
    ray.debugColor = Color.Yellow; // Show debug ray
    /* Rendering logic goes here ... */
}
```

课件原文的结构体定义缺少结尾分号，此处补正。`CameraRay` 描述一条相机光线，`renderRay` 以 const 引用接收，承诺不修改光线本身；但 `debugColor` 声明为 `mutable`，渲染过程因而可以在 const 对象上写入调试颜色，用于调试可视化。课件以游戏渲染中调试光线的显示作为该模式的应用示例：调试附注并非光线的核心状态，故以 `mutable` 显式豁免于 const 承诺之外。

## 17. 回顾与预告（Slides 98–100）

本讲内容可归纳为两部分。其一，Template Classes：template 使同一份逻辑得以在不同类型之间泛化，编译器在使用处按需生成特定类型的代码。其二，Const Correctness：`const` 使整个对象成为只读；不修改对象的成员函数应标记为 `const`；在极少数场合，`const_cast` 与 `mutable` 可以绕过编译器的 const 检查。

下一讲主题为 Template Functions（模板函数），将进一步释放 template 的表达能力。

## 本讲要点

- `template <typename T>` 将逻辑与类型解耦：class template 只写一份，编译器在使用处按需生成特定类型的代码（template instantiation）；`Vector<int>` 与 `Vector<double>` 是完全不同的类型，相互之间没有隐式转换。
- template parameter 不限于类型，还可以是编译期常量（如 `size_t N`、`bool B`）；`std::array<T, N>` 将大小编码进类型，因而可栈分配、避免堆开销。
- 实现 template class 的三个语法要点：`.cpp` 中每个成员函数定义须重复 `template <...>` 并以 `Vector<T>::` 限定；`.h` 须在末尾 `#include "Vector.cpp"`；template parameter list 中 `typename` 与 `class` 完全等价。
- const 对象只能使用 const interface：不修改对象状态的成员函数都应标 `const`（声明与实现均需添加）；const method 内部 `this` 的类型为 `const Vector<T>*`。
- 读写接口以 const overloading 分立：`const T& at(size_t index) const` 服务 const 对象，`T& at(size_t index)` 服务普通对象；const 版本可用 `const_cast<Vector<T>&>(*this)` 委托非 const 版本，消除重复实现。
- `const_cast` 与 `mutable` 均绕过 const 保护且正当用途极少：需要可修改性时应优先考虑不声明 const 或使用 `mutable` 成员，`const_cast` 仅宜用于重载委托等罕见场景。
