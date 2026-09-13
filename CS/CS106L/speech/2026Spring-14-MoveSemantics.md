---
title: "Lecture 14 · Move Semantics 逐字稿"
createAt: 2026/9/13
---

# Lecture 14: Move Semantics（逐字稿）

> 对应课件转写：[2026Spring-14-MoveSemantics.md](../output/2026Spring-14-MoveSemantics.md)

## 1. 引入：数据复制的真实代价

本讲讨论 C++ 的移动语义（move semantics）。问题的出发点是一个看似平常的现象：程序中大量对象复制的结果在被真正使用之前就已被丢弃，而复制本身却消耗了可观的计算资源与能量。

课件以移动设备的功耗为切入点：连接网络、执行计算、点亮屏幕都是耗电因素，而数据复制同样位列其中。这一判断有定量研究支持。Pandiyan 与 Wu 对智能手机典型负载的测量表明，数据移动平均消耗整机约 35% 的能量；Kestor 等人对科学计算应用的分析则显示，从内存移动数据的代价高出一次双精度寄存器间浮点运算约两个数量级。在数据中心尺度上，这一问题被进一步放大。

由此引出本讲的核心问题：如何避免不必要的对象复制？本讲依次讨论：特殊成员函数（special member functions，SMFs）回顾、默认复制策略造成的问题、lvalue 与 rvalue 对"临时性"的形式化刻画、move constructor 与 move assignment operator，最后是 std::move 与 SMF 的设计准则（Rule of Zero、Rule of Three、Rule of Five）。

## 2. 特殊成员函数回顾：以 Photo 类为例

特殊成员函数负责类的生命周期管理，此前已介绍其中三个：copy constructor、copy assignment operator 与 destructor；若用户未定义，编译器会自动生成对应版本。为使讨论具体，课件构造了一个管理像素数据的 Photo 类：

```cpp
class Photo {
public:
    Photo(int width, int height);
    Photo(const Photo& other);
    Photo& operator=(const Photo& other);
    ~Photo();
private:
    int width;
    int height;
    int* data;
};
```

其成员 `data` 指向堆上的一块像素缓冲区，因此该类属于"管理外部资源"的类型。四个 SMF 的语义如下。

普通构造函数为新照片分配像素内存：

```cpp
Photo::Photo(int width, int height)
: width(width)
, height(height)
, data(new int[width * height])
{}
```

copy constructor 从既有对象出发构造新对象，并为像素数据建立完整副本：

```cpp
Photo::Photo(const Photo& other)
    : width(other.width)
    , height(other.height)
    , data(new int[width * height])
{
    std::copy(other.data, other.data + width * height, data);
}
```

copy assignment operator 用另一对象的内容替换当前对象的内容。实现中有两处值得注意：其一，检查 self-assignment（`p = p` 的情形），若为同一对象则直接返回；其二，必须先 `delete[] data` 释放旧缓冲区，再分配新缓冲区并复制：

```cpp
Photo& Photo::operator=(const Photo& other) {
    // Check for self assignment
    if (this == &other) return *this;

    delete[] data; // Clean up old pixels!

    // Copy over new pixels!
    width = other.width;
    height = other.height;
    data = new int[width * height];

    std::copy(other.data, other.data + width * height, data);
    return *this;
}
```

destructor 释放像素缓冲区，防止内存泄漏：

```cpp
Photo::~Photo()
{
    delete[] data;
}
```

这一实现的要点在于深复制：每个 Photo 独占自己的像素缓冲区，复制的成本与图像面积成正比。这正是后续讨论所要优化的对象。

## 3. 例题与解析：SMF 在初始化与赋值中的触发

考虑如下代码，标注 (A) 与 (B) 处分别调用了哪些特殊成员函数？

```cpp
Photo takePhoto();

int main() {
    Photo selfie = takePhoto();    // (A)
    Photo retake(0, 0);
    retake = takePhoto();          // (B)
}
```

结论：(A) 处先调用 copy constructor——`selfie` 以 `takePhoto()` 的返回值为源完成初始化，此处的 `=` 是声明中的初始化语法，并非赋值运算，因为 `selfie` 在该语句之前尚不存在；随后该临时返回值被销毁，调用一次 destructor。(B) 处先调用 copy assignment operator——`retake` 已构造完毕，此处是真正的赋值；临时返回值同样随即析构。此外，`selfie` 与 `retake` 自身的 destructor 在 `main` 结束时执行。

此处需要补充一个说明：`Photo selfie = takePhoto();` 在实际编译中未必真的经历"复制构造 + 析构"的过程，因为编译器可能实施 return value optimization（RVO，返回值优化，属于 copy elision 的一种），直接在 `selfie` 的存储位置上构造返回对象。为使讨论清晰，本讲假定该优化不发生，即严格按上述 SMF 调用序列分析。

这一简化模型给出了一个贯穿全讲的关键观察：函数的返回值是临时的，它在下一行代码执行之前就会被销毁——编译器会在进入下一行之前清理该对象。

## 4. 问题的本质：复制得到的资源旋即被丢弃

沿上节的例子逐阶段考察 `Photo selfie = takePhoto();` 的执行过程。设 `takePhoto()` 返回的 Photo 分辨率为 3840×2160，其 `data` 指针指向地址 `0x1024c3bd` 处的像素缓冲区。

复制构造阶段，`selfie` 获得一份完整副本：`width`、`height` 与源相同，但 `data` 指向一块新分配的缓冲区（例如 `0x133210f1`），源缓冲区的全部像素被逐一拷贝。紧接着进入析构阶段：`takePhoto()` 的返回值是临时的，其 destructor 立即执行，`delete[]` 释放了源缓冲区 `0x1024c3bd`。

于是出现了明显的浪费：3840×2160 的图像含八百余万个像素，一次复制意味着逐个搬运数以百万计的整数值；而我们付出这一完整代价换来的副本，其源对象在复制完成后旋即消亡。从语义上看，此处需要的并不是副本，而是让临时对象的资源直接过渡到 `selfie` 之中。

## 5. 移动的构想：窃取资源并置空源指针

上述结果直接引出一个设想：能否复用临时对象的内存，而非重新复制？这正是移动语义（move semantics）的动机，课件将其概括为"与其复制数据，不如将其窃取"。

设想的操作序列如下。第一步，构造 `selfie` 时不再分配新缓冲区，而是直接接手临时对象的 `data` 指针值（`0x1024c3bd`），此时两个对象暂时指向同一块像素数据。第二步，处理随后必然发生的析构：若临时对象照常析构，`delete[]` 会把 `selfie` 正在使用的缓冲区一并释放，留下悬挂指针。解决方式是在移动的同时将源对象的 `data` 置为空指针（nullptr）。如此一来，临时对象的 destructor 对 nullptr 执行 `delete[]`，而按标准定义该操作不做任何事情，资源得以完好保留在 `selfie` 中。

序列结束后，`selfie` 拥有原图像的全部数据，源对象持有空指针并安全消亡：整个过程未执行任何像素复制。移动的成本只是几次指针与整数的赋值，与图像面积无关。

## 6. 移动并非总是安全：use-after-move

上述机制的安全性依赖一个前提：被移动的对象此后不再被使用。对临时对象而言，这一前提天然成立——`takePhoto()` 的返回值注定在语句结束时消亡。但若把移动施加于一个生命周期仍在延续的对象，后果则完全不同。

考虑如下代码，若第二行的初始化执行的是移动，程序运行时会发生什么？

```cpp
Photo takePhoto();

void foo(Photo whoAmI) {
    Photo selfie = whoAmI;      // What if we move here?
    whoAmI.get_pixel(21, 24);   // ???
}
```

分析：移动使 `selfie` 窃取了 `whoAmI` 的像素缓冲区，`whoAmI.data` 由此变为 nullptr；第三行的 `get_pixel(21, 24)` 需要访问 `data` 所指的像素，于是解引用了空指针，行为未定义，程序通常在此崩溃。这类错误称为 use-after-move——移动之后再使用源对象。

课件以装机作比：copy semantics 相当于在保留旧机的同时组装一台一模一样的新机；move semantics 则是拆机搬运，零件转移之后旧机只剩空壳。落到程序设计层面，本讲的使用准则为：

```cpp
Photo selfie = pic;
// make copies of persistent objects (e.g. variables)
// that might get used in the future

Photo selfie = takePhoto();
// move temporary objects (e.g return values)
// since we no longer need to use them
```

即：对可能再次使用的持久对象（如具名变量）应当复制；对不再需要的临时对象（如返回值）应当移动。

新问题随之而来：上述两行代码在语法上完全同形，编译器依据什么在复制与移动之间作出选择？回答这一问题需要先给"临时性"一个可操作的判定标准，这正是下节 lvalue 与 rvalue 的内容。

## 7. lvalue 与 rvalue：对"临时性"的刻画

C++ 以 lvalue 与 rvalue 一对概念将"临时性"形式化。在上节的代码中，按值传入的形参 `pic` 是 lvalue——它有名字、有确定地址，其生存期覆盖整个函数体；而函数调用表达式 `takePhoto()` 是 rvalue。

判定标准可概括为：一般而言，lvalue 拥有确定的地址，rvalue 则没有。这一点可以由取地址运算直接验证：

```cpp
void foo(Photo pic) {
    Photo* p1 = &pic;
    Photo* p2 = &takePhoto(); // Does not compile!
}
```

`&pic` 合法，因为 `pic` 是 lvalue；`&takePhoto()` 无法通过编译，因为函数返回的临时对象没有可供程序获取的确定地址。

从术语的历史来源看，这一划分也体现在赋值号两侧的合法位置上：lvalue 既可以出现在 `=` 的左侧，也可以出现在右侧（`x = y;` 与 `y = 5;` 均合法）；rvalue 只能出现在 `=` 的右侧（`x = 5;` 合法，而 `5 = y;` 非法）。

两类值的生存期也不同：lvalue 的生存期持续到其作用域结束；rvalue 的生存期只持续到所在语句行结束，亦即包含它的完整表达式求值完毕之时。据此可以得到值类别（value category）的语义刻画：lvalue 是持久的，rvalue 是临时的。

例题：判断下列各行赋值号右侧的表达式是否为 rvalue（提示：判断其是否具有确定地址）。

```cpp
int         a = 4;
int&        b = a;
vector<int> c = {1, 2, 3};
int         d = c[1];
int*        e = &c[2];
size_t      f = c.size();
```

逐项分析如下。`4` 是字面量，无确定地址，为 rvalue。`a` 是具名变量，有确定地址，为 lvalue——这也与 `int& b = a;` 能够绑定非 const 左值引用相印证。`{1, 2, 3}` 用以构造临时内容，无确定地址，为 rvalue。`c[1]` 是 lvalue：`operator[]` 返回对容器内实际元素的引用，该元素驻留内存且可取地址（下一行对 `&c[2]` 的取址即为佐证）。`&c[2]` 的结果是地址值本身，这个指针值是临时求值产物，自身并无确定地址，为 rvalue——注意它与所指向的对象 `c[2]`（一个 lvalue）是两回事。`c.size()` 按值返回，结果为临时值，是 rvalue。

课件在此附带说明：C++ 完整的值类别体系比 lvalue/rvalue 的二分更为精细，还包括 glvalue、xvalue 与 prvalue；该体系超出本讲范围，本讲始终采用"持久/临时"的二分框架。

## 8. 引用重载：lvalue reference 与 rvalue reference

明确了值类别，即可回到第 6 节末尾的问题。在引入移动之前，先考察如何避免对 lvalue 的不必要复制。对于

```cpp
void uploadToInsta(Photo pic);

int main() {
    Photo selfie = takePhoto(); // selfie is lvalue
    uploadToInsta(selfie);      // Unnecessary copy is made here
}
```

按值传参会对 `selfie` 做一次完整复制。解决办法是按引用传参：

```cpp
void uploadToInsta(Photo& pic);

int main() {
    Photo selfie = takePhoto(); // selfie is lvalue
    uploadToInsta(selfie);      // No copy is made here
}
```

lvalue reference 直接绑定到实参本身，不产生复制。然而该方案无法覆盖 rvalue 实参：

```cpp
void uploadToInsta(Photo& pic);

int main() {
    uploadToInsta(takePhoto()); // Does this work?
}
```

结论是不能通过编译，诊断信息为 "candidate function not viable: expects lvalue as 1st argument"：非 const 的 lvalue reference 不能绑定到 rvalue。这一限制背后存在语义上的对应：`Photo&` 形参意味着函数会修改实参、并承诺返回后对象仍处于有效状态，而临时对象"即将消亡、状态无关紧要"的性质与之并不匹配。

语言为此提供了另一类引用：rvalue reference，语法为 `Type&&`，专门绑定临时对象：

```cpp
void upload(Photo&& pic);

int main() {
    upload(takePhoto());
}
```

绑定到 `Photo&&` 的对象是临时的，函数可以对其资源作任意处置，包括窃取。两类引用的语义契约对比如下：

- lvalue reference（`Type&`）：对象是持久的，函数结束后必须使对象保持在有效状态；
- rvalue reference（`Type&&`）：对象是临时的，函数可以窃取（move）其资源；对象最终可能处于失效状态，但这是允许的，因为它即将消亡。

课件引用了一组形象化的注释刻画二者的契约差异。`void foo(Widget& w);` 相当于承诺："我会使用你的 Widget，结束时它可能与交给我时状态不同，但它仍然完好如初地属于你"；而 `void foo(Widget&& w);` 则相当于表示："把你那个不再需要的 Widget 交给我，此后它的状态由我负责，你不必再关心"。

由此得到本讲的一个关键结论：通过 `&` 与 `&&` 形参的重载，可以在重载决议层面区分 lvalue 与 rvalue。若同时提供

```cpp
void upload(Photo& pic);    // 供 lvalue 实参选用
void upload(Photo&& pic);   // 供 rvalue 实参选用
```

则编译器根据实参是 lvalue 还是 rvalue 自动选择相应版本：`upload(selfie)`（`selfie` 为 lvalue）选用前者，`upload(takePhoto())`（调用表达式为 rvalue）选用后者。至此，第 6 节的问题有了答案：复制与移动的抉择不依赖运行时信息，而是由表达式的值类别在编译期决定。

## 9. 移动构造函数与移动赋值运算符

上述机制自然地落到特殊成员函数上：期望 `Photo selfie = pic;`（`pic` 为 lvalue）触发复制，而 `Photo selfie = takePhoto();`（rvalue）触发移动。实现方式即以 `const Photo&` 与 `Photo&&` 分别重载各个 SMF。

copy constructor 已见第 2 节。与之并列的 move constructor 以 rvalue reference 为参数：

```cpp
Photo::Photo(Photo&& other)
    : width(other.width)
    , height(other.height)
{
    // other is temporary
    // Let's steal its resources since we know it's about to be gone!
}
```

其实现思路即第 5 节的构想：由于 `other` 是临时对象、即将消亡，直接接管其资源。将课件图示的操作序列写成代码，就是接手指针并置空源对象：

```cpp
Photo::Photo(Photo&& other)
    : width(other.width)
    , height(other.height)
    , data(other.data)      // 接管缓冲区，不做任何复制
{
    other.data = nullptr;   // 源对象析构时对 nullptr 执行 delete[]，安全
}
```

同理，copy assignment operator 之外还有 move assignment operator：

```cpp
Photo&
Photo::operator=(Photo&& other)
{
    // other is temporary
    // Let's steal its resources since we know it's about to be gone!
}
```

其实现需先释放自身原有缓冲区，再接管 `other` 的缓冲区并将其 `data` 置空，其余成员直接赋值。

归纳起来，类的 SMF 家族新增两个成员：

- move constructor：`Type::Type(Type&& other);`
- move assignment operator：`Type& Type::operator=(Type&& other);`

## 10. std::move：显式强制移动语义

通常我们让编译器依据值类别在 `&` 与 `&&` 版本之间自动选择。这一默认策略并不总是最优：若明确知道某个 lvalue 此后不再使用，复制它同样是浪费。

课件给出了数组插入的例子。为在 `pos` 处插入新元素，需要将后续元素逐个后移：

```cpp
void PhotoCollection::insert(const Photo& pic, int pos) {
    for (int i = size(); i > pos; i--)
        elems[i] = elems[i - 1]; // Shuffle elements down
    elems[i] = pic;
}
```

（课件末行写作 `elems[i] = pic;`；由于 `i` 的作用域限于 for 语句，实际实现中此处应为插入位置 `pos`。）循环中的每一次 `elems[i] = elems[i - 1];` 都调用 copy assignment operator，将元素完整复制到新位置；而这些旧位置上的值在本次后移之后永远不会被再次读取。解决办法是对它们强制移动语义：

```cpp
void PhotoCollection::insert(const Photo& pic, int pos) {
    for (int i = size(); i > pos; i--)
        elems[i] = std::move(elems[i - 1]);
    elems[i] = pic;
}
```

`std::move` 将 `elems[i - 1]` 转换为 rvalue，使赋值选用 move assignment operator，后移操作由逐元素复制变为逐元素移动。值得注意的是，循环之外的 `elems[i] = pic;` 保持复制是正确的：`pic` 以 `const Photo&` 传入，是调用者仍会继续使用的持久对象，恰好符合第 6 节"复制持久对象、移动临时对象"的准则。

强制移动是有代价的，必须警惕其副作用：若移动一个 lvalue，它此后处于何种状态？仍考察第 6 节的例子：

```cpp
Photo takePhoto();

void foo(Photo whoAmI) {
    Photo selfie = std::move(whoAmI);
    whoAmI.get_pixel(21, 24); // ???
}
```

`std::move(whoAmI)` 使初始化选用 move constructor，`selfie` 窃走了 `whoAmI` 的缓冲区；此后 `whoAmI` 处于未知状态，`get_pixel` 的访问构成 use-after-move，行为未定义。

std::move 的另一重要用途，是在自定义移动操作的内部逐成员地转发移动。考虑如下初版实现：

```cpp
class Photo {
public:
    Photo::Photo(Photo&& other) {
        keywords = other.keywords;
    }
private:
    std::vector<string> keywords;
};
```

这里存在一个容易被忽视的事实：虽然在类的视角下 `other` 是临时对象，但在 move constructor 的函数体内，`other` 是一个具名形参，因而是 lvalue——它有名字、有确定地址。于是 `keywords = other.keywords;` 选用的仍是 std::vector 的 copy assignment operator，把所有关键字逐一复制。既然 `other` 即将消亡，就没有理由复制其成员；解决办法同样是强制移动：

```cpp
class Photo {
public:
    Photo::Photo(Photo&& other) {
        keywords = std::move(other.keywords);
    }
private:
    std::vector<string> keywords;
};
```

`std::move(other.keywords)` 使该赋值选用 vector 的 move assignment operator，动态数组连同其内容被整体接管。

最后需要澄清 std::move 的本质：它不执行任何移动，只是一个类型转换，把 lvalue 转换为 rvalue。其返回值类型为

```cpp
static_cast<typename std::remove_reference<T>::type&&>(t)
```

即去引用之后的右值引用类型。它与 const_cast 属于同一类设施：使用者借此显式选择（"opt in"）一种潜在危险的行为——对象被移动之后若继续使用，程序即进入未定义状态。因此工程上的建议是：除非确有理由（例如性能确实关键、且确定对象此后不再使用），应避免显式使用 std::move，把复制与移动的抉择留给编译器按值类别完成。

## 11. 五个特殊成员函数与 Rule of Zero、Three、Five

至此，类的特殊成员函数家族扩展为五个：

```cpp
Type::Type(const Type& other);              // copy constructor
Type& Type::operator=(const Type& other);   // copy assignment operator
Type::Type(Type&& other);                   // move constructor
Type& Type::operator=(Type&& other);        // move assignment operator
Type::~Type();                              // destructor
```

是否每个类都需要逐一定义这五个函数？答案是否定的，取舍依据是如下三条规则。

Rule of Zero：若类不管理内存或其他外部资源，编译器生成的 SMF 已经足够。例如

```cpp
struct Post {
    Photo photo;
    std::string caption;
};
```

编译器为 Post 生成的各 SMF 会逐成员调用 Photo 与 std::string 对应的 SMF，而后二者的 SMF 已被正确实现，故 Post 无需任何用户干预。

Rule of Three：若类管理外部资源，则必须自行定义复制操作；否则编译器生成的 copy constructor/copy assignment operator 只复制指针本身而不复制底层资源，导致两个 Photo 指向同一块数据，进而在析构阶段引发重复释放等错误。该规则表述为：destructor、copy assignment operator、copy constructor 三者若需要其一，就需要全部三者——三者相互配合，共同保证资源恰有一个所有者、复制即为深复制、消亡即释放。

Rule of Five：在定义了 copy constructor/copy assignment operator 与 destructor 的前提下，还应当定义 move constructor/move assignment operator。这并非强制要求——省略移动操作程序依然正确——但缺少它们会使本可移动的场合退化为复制，代码因此变慢。形式化表述为：上述五者中若需要其一，则大概率希望全部五者齐备，其中移动操作可视为可选的最后一环。

## 本讲要点

- 数据复制代价高昂：实测研究表明数据移动可占移动设备整机能耗的显著比例（平均约 35%）；SMF 默认的深复制在源对象即将销毁时纯属浪费，移动语义以"窃取资源"取代复制。
- lvalue 与 rvalue 将"临时性"形式化：lvalue 有确定地址、生存期到作用域结束；rvalue 无确定地址、生存期到所在行结束。使用准则是复制可能再次使用的持久对象、移动不再需要的临时对象。
- 通过 `&` 与 `&&` 重载在编译期区分两类实参：move constructor（`Type::Type(Type&& other)`）与 move assignment operator（`Type& Type::operator=(Type&& other)`）接管资源并将源指针置为 nullptr，使源对象析构时 `delete[] nullptr` 成为无操作。
- 被移动后的对象处于未知状态，不得再使用其内容，否则构成 use-after-move，行为未定义。
- std::move 不执行任何移动，只是把 lvalue 转换为 rvalue 的类型转换（`static_cast<...&&>`）；移动构造函数的形参本身是 lvalue，需借助 std::move 逐成员转发移动。
- 需要定义哪些 SMF 由 Rule of Zero/Three/Five 决定：不管理资源则全部交给编译器；管理资源则复制操作与 destructor 须成组定义，并应补充移动操作以避免不必要的复制。
