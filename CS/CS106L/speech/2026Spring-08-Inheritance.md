---
title: "Lecture 08 · Inheritance 逐字稿"
createAt: 2026/9/13
---

# Lecture 08: Inheritance（逐字稿）

> 对应课件转写：[2026Spring-08-Inheritance.md](../output/2026Spring-08-Inheritance.md)

## 1. 本讲概览（Slides 1–6）

本讲课件开头附有三份课后练习（exercise1、exercise2、exercise3），均位于课程代码仓库的 `lecture08` 目录下。自类的复习起的一段内容在课件中标注为 OPTIONAL，属于对前次课 inheritance 部分的回顾与深化。

本讲分为四个部分：第一，回顾 class（类），并进一步考察其在幕后的工作方式，即对象在内存中的实际形态；第二，inheritance（继承），一种复用 parent class 特性的机制；第三，virtual functions（虚函数），即定义可被子类 override 的函数接口，并由此引出 dynamic dispatch 与 vtable 等幕后机制；第四，结语，讨论一个值得认真对待的问题：是否应当总是使用 inheritance。

## 2. 类的回顾：接口与实现（Slides 7–14）

class 是对某种 abstraction 的表示——它可以建模现实世界中的物体、一个概念，或任何需要将数据与行为组织在一起的实体。class 所做的，是将对象的数据与方法打包为一个整体。诸如 Car、Engine、Vector、Graph、Book、Dog 等概念，均可以作为 class 建模的对象。

以 `Point` 类为例回顾类的语法骨架：

```cpp
class Point {
public:
    Point(int x, int y);
    ~Point();
    int getX();
    int getY();
    void setX();
    void setY();
private:
    int x;
    int y;
};
```

几个关键部分：`public:` 之后的成员对所有代码可见（accessible by everyone）；constructor（构造函数）负责初始化该类；destructor（析构函数）负责清理该类，但通常无需手写；`private:` 之后的成员仅类自身可见（only visible to us），属于 implementation details。这一划分回答的是"类的使用者需要知道什么"：使用者只需要 public 中的接口；`x`、`y` 具体如何存储，是类自己的事务，外部代码不得干预。

工程上的标准组织方式是将声明与实现分离。`Point.h` 是 header file，包含 interface 与 declarations：

```cpp
// Point.h
class Point {
public:
    Point(int x, int y);
    ~Point();
    int getX();
    int getY();
private:
    int x;
    int y;
    std::string color;
};
```

对应的 `Point.cpp` 包含 implementation 与 definitions：

```cpp
// Point.cpp
#include "Point.h"

Point::Point(int x, int y)
    : x(x), y(y) {}

int Point::getX() {
    return x;
}

int Point::getY() {
    return y;
}
```

constructor 使用 member initializer list，成员函数均以 `Point::` 限定。这种划分的意义在于：类的使用者只需阅读 Point.h 即可了解该类"长什么样、有什么"，而无需关心函数体如何实现；"声明置于 .h、定义置于 .cpp"因此成为 C++ 中典型的文件组织方式。

## 3. 对象的内存布局：Python 与 C++（Slides 16–23）

同一个 `Point`，在 Python 与 C++ 中的写法相近——Python 使用 `__init__` 与 `self`，C++ 使用 constructor 与 initializer list——功能看起来一致。由此产生一个自然的问题：一个 Point 对象在内存中究竟是什么样子？两种语言的答案差异显著，而这一差异也是理解本讲后半部分 virtual functions 的基础。

先考察 Python：

```python
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def getX(self):
        return self._x
    def getY(self):
        return self._y
```

执行 `p = Point(1, 2)` 之后，`p` 指向的并非一个仅含数据的对象，而是带有元信息的结构：最上方是 refcount（引用计数），随后是记录对象类型的 type 字段，最后才是真正的数据 `_x = 1`、`_y = 2`。Python 在对象的内存足迹（memory footprint）中存储了关于类型的额外信息，运行时类型检查（runtime type checking）正依赖这些信息。

两个补充例子：`pi = 3.14` 对应的 float 对象记录 refcount = 1、type = float、val = 3.14；`x = "hello 106l :D"` 对应的 str 对象记录 refcount、type = str、length = 11 与字符串数据本身。可见在 Python 中，连 float 与 str 也是携带完整元信息的对象——Python 中所有类型本质上都是 class。又如 `y = 42; z = y`，两个变量名指向同一个 int 对象，该对象的 refcount 随之增至 2，因为现在有两个变量在引用它。

实际结构比上述描述更为复杂。一个 `Point(1, 2)` 对象内含 `__dict__` 指针，指向一张 dictionary；dictionary 的 keys 指向两个独立的 str 对象（`"_x"` 与 `"_y"`），values 指向两个独立的 int 对象，而每个 str、每个 int 自身又都是带 refcount 与 type 的完整对象。换言之，`self._x = x` 的执行是在运行时向这张字典写入一条记录，读取 `_x` 则是运行时查询一次字典。为提供 dynamic typing 的灵活性，Python 存储了大量额外信息。

再看 C++：

```cpp
class Point {
private:
    int x;
    int y;
public:
    Point(int x, int y)
        : x{x}, y{y} {}
    int getX() { return x; }
    int getY() { return y; }
};
```

`Point p {1, 2};` 之后，`p` 所对应的内存中只有两样东西：`int x = 1` 与 `int y = 2`。没有 refcount，没有 type 字段，也没有 `__dict__`。C++ 只在对象中存储数据，类型检查完全由编译器在 compile time 完成，运行时无需携带任何类型信息。两相对比可知：同样是 `Point`，C++ 存储的数据远少于 Python，这正是 C++ 在内存效率上优于 Python 的原因之一。

## 4. 成员函数的存储与 this 指针（Slides 25–33）

对象内存中只有数据，随之而来的问题是：成员函数存储在何处？

Python 中，函数并不存放在对象自身的 dictionary 里，而是存放在与 class 关联的一张单独 dictionary 中。从程序内存的角度看，程序内存分为 OS Shared、Stack 上的变量、Heap 上的变量、全局变量与 Text (Instructions) 指令段：`self._x = x` 产生的数据位于 Heap，而 `getX`、`getY` 等方法体作为指令位于 Text 段。C++ 亦然：函数不存入对象本身，而是单独存放。数据成员落在 stack 或 heap 上——取决于对象本身是局部变量还是动态分配的——成员函数的代码则落在 Text (Instructions) 段。无论创建多少个 `Point` 对象，`getX` 的那份机器码在全程序中只有一份。

这引出另一个问题：成员函数是全体对象共享的一份代码，`p.getX()` 执行时如何确定操作的是哪一个对象？Python 的表达方式相当直接：

```python
p = Point(1, 2)
px = p.getX()

# ...is the same as...

p = Point(1, 2)
px = Point.getX(p)
```

即 `p.getX()` 等价于 `Point.getX(p)`：把 self 作为参数传入。

C++ 中对应的机制是 this。this 是一个指向当前对象的指针，`p.getX()` 中的 `p` 即它所指的对象：

```cpp
int Point::getX() {
    return this->x;
}
```

**例题 1**：下列两段代码是否等价？

```cpp
int Point::getX() {
    return x;
}
```

```cpp
int Point::getX() {
    return this->x;
}
```

**解析**：二者等价。成员函数体内单独出现的 `x` 会被编译器理解为 `this->x`；每个成员函数都持有 this，省略前缀时默认经由它访问成员。

**例题 2**：下列两段代码是否等价？

```cpp
void Point::setX(int x)
{
    x = x;
}
```

```cpp
void Point::setX(int x)
{
    this->x = x;
}
```

**解析**：二者不等价。左侧的 `x = x;` 是参数对参数自身的赋值，成员变量未被触及，函数实际不产生任何效果；右侧才是以参数为成员变量 `x` 赋值。当参数名与成员名相同、参数将成员名遮蔽时，必须显式书写 this 以消歧义。

从语法上看，`this` 的类型是 `Point*`，即一个指针；`->` 就是熟知的指针解引用（pointer dereference）运算符。其幕后机制是：this 由编译器作为隐藏参数传给类函数：

```cpp
int Point::getX() {
    return this->x;
}

// ...gets turned into...

int Point_getX(Point* this)
{ return this->x; }
```

```cpp
Point p {1,2};
int x = p.getX();

// ...gets turned into...

Point p {1,2};
int x = Point_getX(&p);
```

`p.getX()` 经编译后即 `Point_getX(&p)`。可见 C++ 成员函数在幕后与 Python 的 self 机制完全一致，只是 C++ 将其隐藏在语法糖之后。这也解释了上述两道例题的结论为何一同一异：编译器自动补充的是"操作对象从何而来"，而函数体内 `x` 究竟指谁，仍取决于是否写明 this 前缀。

## 5. Inheritance：动机与基本语法（Slides 35–52）

Inheritance 的定义：A mechanism for one class to inherit properties from another，即允许一个类继承另一个类属性的机制。

先建立直觉。世界上有许多种车——Toyota Camry、Honda Civic、Ford Mustang、Jeep Gladiator——它们各不相同，但都继承了一些共同的东西：engine、wheels、steering wheel。描述每一种车时，无须从零开始罗列轮子与方向盘，只需说明"它们都是车"。类似地，几何体 Box、Sphere、Cone、Ring、Buckyball 虽形态各异，但每个 shape 都有 volume 与 surface area。"先归纳共同点，再描述差异"，正是 inheritance 的思维方式。

这种继承结构此前已经出现过：C++ 的流体系就是一棵继承树。`ios_base` 位于顶端，其下是 `basic_ios`，再分叉出 `basic_ostream` 与 `basic_istream`，二者又汇入 `basic_iostream`，其下还派生出一大批类。此处的关系是所谓的 is-a：一个 `std::ifstream` is a `std::istream`，进而 is a `std::ios`——凡能使用 istream 的场合都能使用 ifstream。标准库在引入 inheritance 概念之前就一直在使用它。

以游戏为例说明如何在 C++ 中建模 inheritance。设画面中存在 Tree、Projectile、Weapon、NPC、Player 五类实体，若为每类单独定义 class：

```cpp
class Player {
    double x, y, z;
    HitBox hitbox;
    double hitpoints;
public:
    void damage(double hp);
    void update();
    void render();
};

class Projectile {
    double x, y, z;
    HitBox hitbox;
    double vx, vy, vz;
public:
    void update();
    void render();
};

class Weapon {
    double x, y, z;
    HitBox hitbox;
    size_t ammo;
public:
    void fire();
    void update();
    void render();
};

class Tree {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};

class NPC {
    double x, y, z;
    HitBox hitbox;
    double hitpoints;
public:
    void damage(double hp);
    void update();
    void render();
};
```

该写法存在明显的 redundancy：`double x, y, z` 与 `HitBox hitbox` 在五个类中逐字重复，`update()` 与 `render()` 亦各有五份。修改任何一处公共逻辑，都需要同步修改五处。

这种模型的扩展性同样成问题。假设希望为每类对象添加 `overlapsWith` 方法，用于检查它与另一对象在空间上是否重叠：

```cpp
class Player {
    /* ... */
public:
    bool overlapsWith(const Player& other);
    bool overlapsWith(const NPC& other);
    bool overlapsWith(const Tree& other);
    bool overlapsWith(const Projectile& other);
    bool overlapsWith(const Weapon& other);
};
// And we'd do the same for NPC, Tree, Projectile, Weapon!
```

仅 `Player` 一个类就需要五个重载，且 NPC、Tree、Projectile、Weapon 也各需一套。这种做法不具备可扩展性（This doesn't scale!）：每新增一种对象类型，重载数量都会继续膨胀。

退一步观察：这些对象虽然各不相同，但全都共享三项内容——空间中的一个位置、一个 hitbox，以及 update 与 render 方法。据此可以提炼一个 common base class，如同"多种车都继承 engine、wheels、steering wheel"那样。将其命名为 Entity：

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

将五个类中的公共成员全部移入 Entity，每个具体类只保留自身独有的成员。继承关系以冒号书写：`class Player : Entity` 的含义是 Player 是一个 Entity，Entity 拥有的所有成员——数据与函数——Player 自动全部拥有，无需再抄写一行：

```cpp
class Player : Entity {
    double hitpoints;
public:
    void damage(double hp);
};
```

```cpp
class Projectile : Entity
{
    double vx, vy, vz;
};
```

```cpp
class Weapon : Entity
{
    size_t ammo;
public:
    void fire();
};
```

```cpp
class Tree : Entity
{};
```

```cpp
class NPC : Entity {
    double hitpoints;
public:
    void damage(double hp);
};
```

Entity 称为 base class（基类），Player 等类称为 derived class（派生类）。注意 `class Tree : Entity {};`：Tree 自身未添加任何成员，仅凭继承即可。

然而 redundancy 仍未消除：Player 与 NPC 都还含有 `double hitpoints` 与 `void damage(double hp)` 这一对重复。解决方式是增加一层继承，在中间插入 Actor：

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};

class Actor : Entity
{
    double hitpoints;
public:
    void damage(double hp);
};
```

Player 与 NPC 改为直接继承 Actor，那对重复的成员即上移至 Actor：

```cpp
class Player : Actor {};
class NPC : Actor {};
```

Projectile、Weapon、Tree 仍直接继承 Entity。至此整棵 inheritance tree 构建完成。

这棵树定义的是 is-a 关系："A Weapon is an Entity"；"An NPC is an Actor，同时 is an Entity"。is-a 沿树向上传递：NPC 需经过两层才到达 Entity，但每一层关系均成立。这棵树的另一好处是可演进：日后发现两类实体存在新的共同点时，只需在合适位置插入一层中间类，其余代码几乎不受影响。

有了共同 base class，定义公共功能变得直接。现在可以检查任意两个 Entity 是否重叠，无论其具体类型：

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;

public:
    void update();
    void render();
    bool overlapsWith(const Entity& other);
};

Player player { /* ... */ };
Projectile bullet { /* ... */ };
bool isHit = player.overlapsWith(bullet);
```

overlapsWith 的实现只需比较双方的 x、y、z 与 hitbox。此前需要成排重载的问题不复存在：由于 Player is an Entity，Projectile 亦然，单一参数类型即可覆盖所有情形。

## 6. 访问控制与继承方式（Slides 54–58）

上述代码实际上无法通过编译，问题出在 access modifiers 上：`bool isHit = player.overlapsWith(bullet);` 一行会得到编译器报告 "overlapsWith is inaccessible"。原因在于：默认情况下，class 的继承是 private 继承。

```cpp
class Entity {
public:
    bool overlapsWith(const Entity& other);
};

class Player : /* private */ Entity {
    // Private inheritance:
    //  - private members of Entity are inaccessible to all
    //  - public members become private (inaccessible to outside)
};
```

省略访问修饰符时，编译器自动补入 private：Entity 的 private 成员照常对所有人不可见，而其 public 成员进入 Player 之后转为 private，对外不可访问。这正解释了报错：overlapsWith 在 Entity 中虽为 public，但经 private 继承的"转换"之后，在 Player 中已成为 private，故 `player.overlapsWith(bullet)` 对外不可访问。

修正方式是以 public 方式继承 Entity：

```cpp
class Player : public Entity {
    // Public inheritance:
    //   - private members of Entity are still inaccessible
    //   - public members become public (accessible to outside)
};
```

两种继承方式的成员可访问性转换规则如下。private inheritance（默认写法）：

| In Parent | In Child |
|-----------|----------|
| private | inaccessible |
| public | private |

public inheritance：

| In Parent | In Child |
|-----------|----------|
| private | inaccessible |
| public | public |

从表中可读出两条结论。其一，无论采用何种继承方式，base class 的 private 成员对 derived class 均为 inaccessible——继承不会破坏封装，private 就是 private，这一点不受继承方式影响；两种继承方式差异仅体现在 public 成员的转换上：private 继承将其降级为 child 中的 private，public 继承则原样保留。其二，public inheritance 才能恰当地建模 is-a 关系：Player 之所以真正 is an Entity，是因为它将 Entity 的全部功能以 public 形式对外暴露；反之在 private 继承下，外部代码无从看出这是一个 Entity，其意义更接近实现细节层面的复用。

另一个相关的修饰符是 protected：protected 成员对子类可见，对外部不可见。注意 class 的成员默认是 private：

```cpp
class Entity {
protected:
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

```cpp
class Projectile : public Entity {
private:
    double vx, vy, vz;
public:
    void move() {
        x += vx;
        y += vy;
        z += vz;
    }
};
```

若希望在 Projectile 的 `move()` 中直接访问继承而来的 x、y、z，就必须在 Entity 中将它们标记为 protected；若留在 private 区，则连子类也无法访问。

## 7. 游戏循环与 object slicing（Slides 60–71）

回到 Entity 的实际应用。设计思路是：游戏逻辑通过为每种 Entity 重写各自的 update 与 render 来实现。

```cpp
void Player::update() {
    // Handle controller input
}
```

```cpp
void Projectile::update() {
    // Move the projectile
}
```

⋮

```cpp
// By default, do nothing!
void Entity::update() {}
```

render 同理：

```cpp
void Player::render() {
    // Draw the player!
}
```

```cpp
void Projectile::render() {
    // Cool particle effects!
}
```

⋮

```cpp
// By default, do nothing!
void Entity::render() {}
```

Player 的 update 处理手柄输入，Projectile 的 update 推进弹道，Entity 提供什么都不做的默认版本——它为所有没有专属行为的实体提供了安全的缺省选择。

一个游戏本质上就是一组 entity 在每一帧被 update 与 render：

```cpp
int main() {
    std::vector<Entity> entities { Player(), Tree(), Projectile() };
    while (true) {
        for (auto& entity : entities) {
            entity.update();
            entity.render();
        }
    }
}
```

`while (true)` 构成 game event loop，每帧执行一圈。该设计的主循环无须知道每个 entity 的具体类型，只要求它们都是 Entity、都具有 update 与 render。然而实际运行的结果是：程序并未按预期工作。

理解其原因需要回到幕后。C++ 会将对象的字段按顺序排入内存：一个 Entity 对象的内存就是 double x、double y、double z、HitBox hitbox 四项依次排列。C++ 会将子类自身的成员堆叠在被继承成员之下：

```cpp
class Projectile
    : public Entity {
private:
    double vx, vy, vz;
public:
    void move();
};
```

因此 Projectile 对象占据七格：上方四格是继承自 Entity 的 x、y、z、hitbox，下方三格是它自己的 vx、vy、vz。

于是 `std::vector<Entity> entities { Player(), Tree(), Projectile() };` 的问题随之显现：vector 的每个元素都必须是 Entity 类型，每个槽位的大小就是 Entity 的大小，即那四格。将一个 Projectile 存入时会发生什么？它被 sliced 了——拷贝时只有 Entity 部分的四格被复制过去，vx、vy、vz 无法容纳，全部被切掉丢弃。这就是 object slicing（对象切片），需要注意它只在发生拷贝时才会出现。

更关键的后果是：vector 中每个元素都"是"一个 Entity，因此编译器调用的是 Entity::update()——即那个什么都不做的默认版本——而非 Player::update()、Tree::update()、Projectile::update()。从内存图上看，`std::vector<Entity>` 的三个槽位各自只含 x、y、z、hitbox 四项基类成员，类型专属的 hitpoints、vx/vy/vz 在拷贝中全部丢失。程序运行时，所有实体静止不动。一句话概括这一 mismatch：一个 Projectile 根本"装不进"一个 Entity——它比 Entity 大，装入必然丢失内容。由此得出的准则是：凡需以基类统一管理子类对象，就应避免值拷贝，改用指针或引用。

解决方案是：不存对象，改存 Entity*。

```cpp
int main() {
    Player p; Tree t; Projectile b;

    std::vector<Entity*> entities { &p, &t, &b };
    while (true) {
        for (auto& ent : entities) {
            ent->update();
            ent->render();
        }
    }
}
```

此时 vector 中存放的是指向 entity 的指针，而非 entity 本身。指针只是一个地址，拷贝指针不会拷贝对象，object slicing 无从发生。从内存图上看，vector 的三个 `Entity* ptr` 分别指向 heap 上完整的 Player、Tree 与 Projectile：Player 的 hitpoints、Projectile 的 vx、vy、vz 一个不缺。指针通过避免对对象的拷贝，保住了子类的全部细节。

## 8. compile-time type 与 runtime type 的分歧（Slides 73–82）

改为指针之后再运行，程序仍然未按预期工作。此时真正的问题浮出水面：程序中存在多个不同的 update 方法——

```cpp
void Projectile::update();
void NPC::update();
void Player::update();
void Entity::update();
```

——那么拿到一个 Entity 指针时，编译器如何确定该调用哪一个？

```cpp
Entity* entity = entities[0];
entity->update();
```

合理的语义应当是：调用与 entity 实际所指对象类型匹配的那个 update——指向 Player 则调用 Player::update()，指向 Projectile 则调用 Projectile::update()，依此类推。但仅凭一个 `Entity*`，得不到任何关于实际类型的信息：该指针可能指向 Player、Projectile、Tree，或者就是一个 Entity。这四种可能的内存布局仅在基类成员之后的部分有所区别——Player 多出 hitpoints，Projectile 多出 vx、vy、vz，Tree 与 Entity 则完全相同。is-a 关系保证了 Player 对象的前几格就是 Entity 的内容，因此 Player* 可以安全地当作 Entity* 使用；反过来，一个 Entity* 的背后究竟是"纯 Entity"还是某个子类，指针本身不提供任何线索。

编译器在这种情形下默认假设 entity 指向的是一个 Entity——这是它唯一能确信任何 Entity 指针都会支持的类型。于是 `entity->update()` 在编译期被直接绑定到 Entity::update()，仍是那个空函数。示意图所展示的正是期望与现实的落差：指针实际指向 Player，期望调用（Want to call）的是 Player::update()，实际调用（Actually called）的却是 Entity::update()。

因此，使用 Entity* 是有代价的：我们"遗忘"了对象的真实类型。此处必须区分对象的 compile-time type 与 runtime type：在 compile time，它被当作 Entity 对待；在 runtime，它可能是 Entity，也可能是任何子类（如 Projectile、Player）。同一个指针在两种视角下的"类型"可以不同，这正是前述所有现象的根源。所需的机制是 dynamic dispatch（动态分派）：依据对象的 runtime (dynamic) type，调用（dispatch）不同的方法。

## 9. virtual functions 与 dynamic dispatch（Slides 84–86）

解决方案是 virtual functions。规则有二：将函数标记为 virtual 即启用 dynamic dispatch；子类可以 override 该方法。

```cpp
class Entity {
public:
    virtual void update() {}
    virtual void render() {}
};
```

```cpp
class Projectile : public Entity {
public:
    void update() override {};
};
```

两个关键词的分工：基类中的 virtual 表示"子类可重写此函数，运行时按实际类型决定调用哪个版本"；子类中的 override 表示"此函数重写的是基类的 virtual 方法"。其中有一个细节：override 并非必需，但它是良好的可读性实践——它使编译器检查该函数确实在 override 一个 virtual 方法，而不是不小心创建了一个新的同名方法。若签名书写有误，未写 override 时编译器不会给出任何提示，写了 override 则立即报错。

加入 virtual 之后再次运行游戏，结果正确：每个 entity 都按自身的方式 update 与 render——Player 处理手柄输入，Projectile 自行推进，游戏终于按设计运转。这正是 virtual 函数所支撑的 polymorphism（多态）：同一调用语句在不同类型的对象上表现出各自的行为。

## 10. vpointer 与 vtable：virtual 的实现机制（Slides 88–92）

virtual 的工作方式如下：为函数添加 virtual 之后，每个对象中会附加一些 metadata。具体而言，对象中会多出一个指针，称为 vpointer，它指向一张表，称为 vtable；该表为每个 virtual 方法记录"该对象应当调用的函数"。

以 `Entity*` 指向一个 Projectile 对象为例，其内存布局自上而下为 x、y、z、hitbox，随后多出一个 `void* vpointer`，再往后才是它自己的 vx、vy、vz。注意 vpointer 的位置：它插在继承来的成员与自身新增的成员之间，凡含 virtual 函数的对象都会携带它。vpointer 指向的 vtable 内容形如：

| Function | Implementation |
|---|---|
| update | Projectile::update() |
| render | Entity::render() |

注意 render 一行：Projectile 并未重写 render，因此表中填的仍是 Entity::render()，调用时回落到基类版本。每个类的 vtable 各不相同：Player 的表中 update 对应 Player::update()，Tree 的表中 update 对应 Entity::update()，各类查各自的表、调各自的函数。

```cpp
Entity* p = new Projectile { /* ... */ };
p->update();
```

执行 `p->update()` 时，程序顺着 p 找到对象内的 vpointer，再由 vpointer 查 vtable，发现 update 一项填的是 Projectile::update()，于是调用它。方法的选择发生在 runtime，通过查表完成——这与此前"编译期直接绑定到 Entity::update()"形成鲜明对照，dynamic dispatch 的 "dynamic" 即体现于这一步。

这一机制与 Python 存在相似性：Python 对象内携带 type 字段，依靠它进行运行时查找。二者可以类比：Python 与 C++ 的 virtual functions 都在对象中存储 type-specific 信息。区别在于，Python 为每个对象都付出这套代价，而 C++ 只在标记了 virtual 的类上才付出。

## 11. 例题与解析：virtual function 的取舍（Slides 93–94）

**题目**：何时应当使用 virtual function？何时不宜使用？

**解析**：适用场景即本讲的游戏模型——以 base class 指针统一管理一组不同子类的对象、且希望每个对象表现自身行为时，virtual 是实现 dynamic dispatch 的必要手段。

不宜使用的原因在于其开销。在许多其他语言中，类函数默认即为 virtual；C++ 则要求显式选择加入（opt in），原因正是 virtual 更昂贵：其一，它会增大类对象的内存布局——每个对象都需额外携带一个 vpointer；其二，调用时需先查找 vtable，比普通函数调用耗时更长。对绝大多数程序而言，这点开销无关紧要；但在以纳秒计胜负的 quant finance 等行业中，virtual functions 是不被使用的。

这一取舍与本讲前半部分的对比相呼应：C++ 的默认对象远比 Python 轻量；是否为多态付出代价、在何处付出，由程序员显式决定。

## 12. pure virtual functions 与 abstract class（Slides 96–99）

继承体系还有进一步的机制：pure virtual functions（纯虚函数）。

```cpp
class Entity {
public:
    virtual void update() = 0;
    virtual void render() = 0;
};
```

写法是：不提供函数体，以 `= 0;` 代替实现，即将 virtual 函数标记为 pure virtual——只提供接口，不提供默认实现。

关于 pure virtual 有两条规则。其一，一个类只要拥有至少一个 pure virtual function，它就是 abstract class（抽象类），不能被实例化：

```cpp
class Entity {
public:
    virtual void update() = 0;
    virtual void render() = 0;
};

Entity e;
// 编译失败：Entity is abstract!
```

这一限制是合理的：update 与 render 连函数体都没有，`Entity e;` 的 update 无从执行，故编译器直接禁止创建该对象。

其二，子类 override 全部 pure virtual functions 之后，该类即成为 concrete（具体类），可以实例化：

```cpp
class Projectile
    : public Entity {
public:
    void update() override {};
    void render() override {};
};

Projectile p;
// 正确：Projectile is concrete
```

pure virtual 的适用时机是：不存在清楚的默认实现之时。与第 7 节中 Entity 的空函数默认版本相对照，那里的"什么都不做"是一个合理的缺省行为，而有些接口连这样的缺省都不存在。回到本讲开头 Shape 的例子：Box、Sphere、Cone、Ring、Buckyball 都是一种 Shape，每个 shape 都有 volume——但 Shape 本身的"默认体积"是多少？这个问题没有意义，数学上不存在"任意形状的默认体积"。

```cpp
class Shape {
public:
    virtual double volume() = 0;
};
```

将 volume 标为 pure virtual，由各子类自行决定计算方式。Shape 由此成为一个纯粹的接口概念：它规定"凡是 shape 都必须能报告自己的体积"，而将"如何计算"完全交给子类。

## 13. 结语：composition 与 inheritance 的权衡（Slides 101–107）

最后讨论本讲的核心问题：该不该用 inheritance。

课件展示了一张真实游戏引擎的 UML 类图：Game 居中，向外关联 AudioRenderer、PhysicsEngine、InputHandler、TimeTracker、GameSession、Matter 等众多子系统，各子系统之下又有层层继承与关联——Sprite 之下有 IntelligentSprite，SpriteAnimation 之下还有 CollidableAnimation，结构庞大。这张图说明 inheritance 有时会失控：庞大的 inheritance tree 往往更慢、也更难以推理——确定某个行为定义于哪一层、修改某一层会波及何处，都需要沿树逐层追溯。在视频游戏行业中，"为每种对象类型都建立一个子类"的做法在现代 game engine 中并不常见；composition（组合）往往更灵活，也更合理。

问题的关键在于区分两种关系："a car is an engine" 不成立，"a car has an engine" 才成立。写成代码对比如下：

```cpp
class Car
: public Engine
, public SteeringWheel
, public Brakes
{
/* Hmmm... this doesn't seem
quite right */
};
```

Car 同时继承 Engine、SteeringWheel、Brakes，语义上明显不合理。相比之下：

```cpp
class Car {
    Engine engine;
    SteeringWheel wheel;
    Brakes brakes;
};
```

Car 由 Engine、SteeringWheel、Brakes 组成，表达自然。这就是那句经典准则——prefer composition over inheritance：inheritance 是强大的工具，但许多情形下 composition 才更恰当。

二者并非互斥，结合起来可以兼得两者之长：

```cpp
class Car {
    Engine* engine;
    SteeringWheel* wheel;
    Brakes* brakes;
};

class Engine {};
class CombustionEngine : public Engine {};
class GasEngine : public CombustionEngine {};
class DieselEngine : public CombustionEngine{};
class ElectricEngine : public Engine {};
```

Car 通过指针持有 Engine——这是 composition；Engine 家族内部以 inheritance 划分出 CombustionEngine，再分出 GasEngine 与 DieselEngine，另有直接继承 Engine 的 ElectricEngine——这是 inheritance。Car 不关心自己所装 engine 的具体种类：一个指针可以指向任意一种，更换 engine 无须修改 Car 的代码。两个工具各司其职：composition 承担"Car 拥有这些部件"，inheritance 承担"各 engine 同属一个家族"。课件并提示：该技巧在 C++ 中的一个典型应用，可查阅 PIMPL idiom。

## 本讲要点

- C++ 对象的内存中只存数据成员，类型检查在 compile time 完成；Python 每个对象都携带 refcount、type 等元信息，故 C++ 更省内存。成员函数不存于对象：`p.getX()` 幕后等价于将 this（类似 Python 的 self）作为隐藏参数传入，函数体内的 `x` 默认即 `this->x`；参数与成员同名时必须显式书写 this。
- inheritance 以 `class Derived : public Base` 声明，表达 is-a 关系；class 默认为 private inheritance（基类 public 成员在子类中转为 private），须写 public 继承才能对外暴露基类接口。基类 private 成员对子类永远不可见，供子类使用的成员应标 protected。
- 将 derived class 对象按值放入 base class 的容器会发生 object slicing：拷贝时子类多出的成员被切掉，后续调用也退化为 base class 版本；改用基类指针（如 `std::vector<Entity*>`）避免拷贝，才能保留子类对象的完整信息。
- 指针只解决一半问题：`Entity*` 上的方法调用仍由 compile-time type 决定。将函数标为 virtual 才启用 dynamic dispatch（即 polymorphism 的基础），运行时经对象内的 vpointer 查 vtable 决定调用版本；子类以 override 标记重写，由编译器检查正确性。代价是对象增大（vpointer）且调用需查表，故 C++ 将其设计为显式 opt in。
- 以 `= 0` 声明 pure virtual function：含它的类是 abstract class，不可实例化；子类实现全部 pure virtual functions 后才成为 concrete。适用于没有合理默认实现的接口，如 Shape::volume()。
- inheritance 表达 is-a，composition 表达 has-a："a car has an engine"，而非 "a car is an engine"。庞大的 inheritance tree 更慢且难以推理，现代实践倾向 prefer composition over inheritance；二者结合（成员以基类指针持有 + 小型继承族）效果最佳。
