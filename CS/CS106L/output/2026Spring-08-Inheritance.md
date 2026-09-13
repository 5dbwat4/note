# Lecture 08: Inheritance (2026Spring)

> PDF title: 2026Spring-08-Inheritance.pptx
> Source: `assets/slides/2026Spring-08-Inheritance.pdf` · 109 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Welcome! Bonus attendance form below
Welcome! Bonus attendance form below

*Figure: A black and white QR code centered on the slide, intended for a bonus attendance form.*

---

## Slide 2: Exercise 1

Exercise 1

[https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise1.h](https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise1.h)

Links on this slide:
- <https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise1.h>

---

## Slide 3: Exercise 2

[https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise2.h](https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise2.h)

Links on this slide:
- <https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise2.h>

---

## Slide 4: Exercise 3

https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise3

Links on this slide:
- <https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture08/exercise3>

---

## Slide 5: OPTIONAL

**OPTIONAL**

Hi all, everything from here on out is optional
review of inheritance.

---

## Slide 6: Today’s Agenda
*   A Recap on Classes
    *   And more on how they work behind the scenes
*   Inheritance
    *   Inheritance allows us to reuse features from a parent class
*   Virtual Functions
    *   Defining function interfaces that can be overridden in sub-classes
*   Closing Thoughts
    *   Should you always use inheritance?

---

## Slide 7: Last Time: Classes

*   What are classes?
    *   Turn to the person next to you and think of one thing you remember from Tuesday’s lecture!

---

## Slide 8: Last Time: Classes

- What are classes?
  - Turn to the person next to you and think of one thing you remember from Tuesday's lecture!
- A class represents an abstraction — it can model a real-world object, a concept, or any entity you want to organize into data and behavior.
- A class bundles data and methods for an object together

---

## Slide 9: A class as a concept in a program

• You can think of classes as a **real life concept**
    • Car
    • Engine
    • Video Game Character
    • Vectors
    • Graph
    • Book
    • Dog

*Figure: A collection of images illustrating the listed concepts. A red sports car is positioned near the "Car" bullet. Below the car is an image of a brown dog lying down. To the right of the car is a code box displaying `std::vector<int>`. Further right is a mathematical matrix notation. Below the matrix is an image of a closed red book with a bookmark. To the far right is a directed graph with vertices labeled v1 through v6. Below the graph and book is a large photograph of a car engine.*

```cpp
std::vector<int>
```

```
[ a11  a12  ...  a1n ]
[ a21  a22  ...  a2n ]
[  :    :        :   ]
[ am1  am2  ...  amn ]
```

---

## Slide 10: What questions do you have?

*Figure: A photograph of a man with glasses and light-colored hair, wearing a patterned shirt, with his hand near his chin. In the background, a poster with the text "BJARNE STROUSTRUP" is visible.*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 11: A Recap on Classes

---

## Slide 12: A Point on classes

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

*Figure: A diagram explaining the structure of a C++ class. On the left is a box containing the code for a `Point` class. On the right are four explanatory boxes with arrows pointing to specific parts of the code:*
*   *A box labeled **public:** in red text with the description "Accessible by everyone!" points to the `public:` access specifier in the code.*
*   *A box labeled **constructor** in blue text with the description "Initializes this class" points to the constructor declaration `Point(int x, int y);`.*
*   *A box labeled **destructor** in blue text with the description "Cleans up this class" and "Usually don't need this" points to the destructor declaration `~Point();`.*
*   *A box labeled **private:** in red text with the description "Only visible to us! Implementation details" points to the `private:` access specifier in the code.*

---

## Slide 13: A Point on classes

*Figure: A C++ class definition displayed inside a white rectangular box with a drop shadow. Below it, a smaller white box with a drop shadow provides context for the file.*

```cpp
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
}
```

**Point.h** (header file)
Contains **interface, declarations**

---

## Slide 14: A Point on classes

*Figure: A slide titled "A Point on classes" shows two code boxes at the top and two smaller descriptive boxes at the bottom. The top-left box contains a C++ class declaration, and the top-right box contains the corresponding implementation. The bottom-left box labels the first as "Point.h (header file)" and the bottom-right box labels the second as "Point.cpp".*

```cpp
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
}
```

```cpp
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

**Point.h (header file)**
Contains **interface, declarations**

**Point.cpp**
Contains **implementation, definitions**

---

## Slide 15: Let's try something out...

*Figure: A cartoon image of Batman in his blue suit, looking thoughtful with his hand on his chin.*

practice code

Links on this slide:
- <https://www.online-python.com/>

---

## Slide 16: Classes: Python vs. C++

*Figure: A side-by-side comparison of Python and C++ class implementations for a `Point` object. The left panel is a light blue box containing Python code, and the right panel is a light green box containing C++ code. At the bottom center, a white text box contains a question.*

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

What does a Point look like in memory?

---

## Slide 17: Classes: Memory Layout (Python)

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

*Figure: A diagram illustrating the memory layout of a Python object. On the right, a box shows the code `p = Point(1, 2)`. Below it, a variable labeled `p` points with a black arrow to a memory structure. The memory structure is a table with rows labeled `refcount`, `type`, `_x = 1` (with a pink background), and `_y = 2` (with a pink background). A callout box with a speech bubble tail points to this memory structure and contains explanatory text.*

Python **stores extra information** about the type of the object in its memory footprint! This enables runtime type checking.

---

## Slide 18: Python Memory Layout - Examples (Python)

**Python Code:**
```python
pi = 3.14
x = "hello 106l :D"
```

*Figure: A diagram illustrating Python memory layout. On the left, a box shows the code assignments for variables `pi` and `x`. On the right, two vertical structures represent the memory objects. The top structure is pointed to by a box labeled `pi` and contains the fields `refcount=1`, `type=float`, and `val=3.14`. The bottom structure is pointed to by a box labeled `x` and contains the fields `refcount=1`, `type=str`, `length=11`, and `data = "hello 106l :D"`. A text box at the bottom of the slide contains the following note:*

> All types in **Python** are considered **classes**.

---

## Slide 19: Python Memory Layout - Examples (Python)

```python
y = 42
z = y
```

*Figure: A diagram illustrating Python's reference counting and memory layout. On the left, two variables, `y` and `z`, are shown in small square boxes. Two thick black arrows point from these variable boxes to a single rectangular memory object on the right. The memory object contains three fields: the top section is labeled `refcount=2`, the middle section is `type=int`, and the bottom section, which has a light pink background, contains `digits=[42]`. Below the diagram, a rectangular callout box contains explanatory text.*

**refcount** increases to 2 since two **variables are referencing it now**

---

## Slide 20: Classes: Memory Layout (Python)

*Figure: The slide is divided into three main sections. On the left is a light blue box containing Python code for a class definition. On the right is a white box showing the instantiation of the class and a corresponding memory layout diagram. Overlapping the bottom of these two boxes is a white callout box with black text and some red-highlighted words.*

**Code Block (Left):**
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

**Diagram and Instantiation (Right):**
```python
p = Point(1, 2)
```

*Figure: A diagram illustrating memory allocation. A variable box labeled "p" has a bold black arrow pointing to a memory block. The memory block is divided into four horizontal rows. From top to bottom, the rows contain: "refcount", "type", "_x = 1", and "_y = 2". The last two rows, representing the object's instance variables, are shaded in light red.*

**Callout Box:**
Python **stores extra information** about the type of the object in its memory footprint! This enables runtime type checking.

---

## Slide 21: It’s actually *much* worse than this!

`p = Point(1, 2)`

*Figure: A diagram illustrating the memory representation of a Python object `p = Point(1, 2)`. The variable `p` points to a `Point` instance object, which contains a `__dict__` pointer to a dictionary structure. The dictionary structure points to two `str` objects as keys and two `int` objects as values.*

**Point object:**
| Field | Value |
| :--- | :--- |
| Refcount | 1 |
| type | Point |
| __dict__ | *→ points to dict* |

**Dictionary structure:**
| Field | Value |
| :--- | :--- |
| refcount | |
| type | dict |
| size | 2 |
| keys | *→ points to strings* |
| values | *→ points to integers* |

**String objects (Keys):**
| Field | String 1 | String 2 |
| :--- | :--- | :--- |
| refcount | 1 | 1 |
| type | str | str |
| length | 2 | 2 |
| kind | 1 | 1 |
| data | "_x" | "_y" |

**Integer objects (Values):**
| Field | Int 1 | Int 2 |
| :--- | :--- | :--- |
| refcount | 1 | 1 |
| type | int | int |
| size | 1 | 1 |
| digits | [1] | [2] |

To offer the flexibility of dynamic typing, **Python stores a lot of extra info!**

---

## Slide 22: Classes: Memory Layout (C++)

*Figure: Two boxes side by side. The left box illustrates the memory layout of a `Point` object and contains a note about C++. The right box contains the C++ class definition for `Point`. In the left box, a small box labeled `p` has a thick black arrow pointing right to a two-row memory layout diagram showing `int x = 1` in the top row and `int y = 2` in the bottom row. Below the memory diagram is a note box. The entire layout demonstrates how a C++ object stores its data members in memory.*

### Left Box

`Point p {1, 2};`

**Memory Layout Diagram:**

| Field |
|-------|
| `int x = 1` |
| `int y = 2` |

An arrow labeled `p` points to this memory block.

> C++ **just stores the data** in the object! The compiler does all of the type checking at compile time!

### Right Box

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

---

## Slide 23: Classes: Memory Layout

### C++

```cpp
Point p {1, 2};
```

*Figure: A diagram showing C++ memory layout. A box labeled `p` points to a single contiguous memory block containing two sub-blocks: `int x = 1` and `int y = 2`.*

### Python

```python
p = Point(1, 2)
```

*Figure: A diagram showing Python memory layout. A box labeled `p` points to a Python object with fields `Refcount = 1`, `type = Point`, and `__dict__`. The `__dict__` field points to a dictionary object (type = dict, size = 2). The dictionary's `keys` field points to two separate string objects (one for `"_x"`, one for `"_y"`), and its `values` field points to two separate integer objects (both with `digits = [1]`).*

C++ **stores less data** in classes! This is one reason why C++ is more memory-efficient than Python

---

## Slide 24: What questions do you have?

*Figure: A photo of Bjarne Stroustrup, creator of C++, looking thoughtful with his hand near his chin. In the background, books and posters are visible, including one that reads "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". Below the photo is the caption "bjarne_about_to_raise_hand".*

**What questions do you have?**

bjarne_about_to_raise_hand

---

## Slide 25: Where are the functions?
Where are the functions?

---

## Slide 26: Where are the functions in Python?

Functions are not stored in the object dictionary itself, but separately in a dictionary associated with the class.

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

*Figure: A diagram titled "Your Program's Memory" showing a vertical stack of colored blocks representing memory sections. From top to bottom, the blocks are:*
- *Gray block: "OS Shared"*
- *Blue block: "Variables (Stack)"*
- *White block with a downward-pointing arrow from the "Variables (Stack)" block and an upward-pointing arrow from the "Variables (Heap)" block. This white block contains a large black "X".*
- *Blue block: "Variables (Heap)"*
- *Pink block: "Global Variables"*
- *Light purple block: "Text (Instructions)"*

*There are two black arrows pointing from the Python code on the left to specific sections in the memory diagram on the right:*
1. *One arrow originates from the lines `self._x = x` and `self._y = y` in the `__init__` method, points to the "Variables (Heap)" block, and is labeled with a text box: "Data stored here".*
2. *Another arrow originates from the definitions of the methods `getX` and `getY`, points to the "Text (Instructions)" block, and is labeled with a text box: "Functions stored here".*

---

## Slide 27: Where are the functions in C++?

Functions are not stored in the object itself, but separately

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

*Figure: A diagram illustrating memory layout. On the left is a C++ code block for the `Point` class. On the right is a vertical stack representing memory regions, divided into five sections from top to bottom: "OS Shared" (grey), "Variables (Stack)" (light blue), "Variables (Heap)" (light blue), "Global Variables" (pink), and "Text (Instructions)" (purple). Arrows point from the data members (`int x;`, `int y;`) in the code to a box labeled "Data stored here", which then points to both the Stack and Heap sections. Arrows point from the member functions in the code to a box labeled "Functions stored here", which points to the "Text (Instructions)" section. Between the Stack and Heap sections, there are two black triangles pointing toward each other.*

---

## Slide 28: Where are the functions?

Functions are stored separately from the object

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

```python
p = Point(1, 2)
px = p.getX()

# ...is the same as...

p = Point(1, 2)
px = Point.getX(p)
```

**Passing `self` as parameter**

---

## Slide 29: this in C++

**this** is a pointer to the current class

```cpp
int Point::getX() {
return this->x;
}
```

*Figure: A diagram illustrating the `this` pointer. A box labeled `this` has an arrow pointing to a block representing the current object instance. The object block is divided into two member variables: `int x` on top and `int y` on the bottom.*

---

## Slide 30: The importance of this

Are these two snippets of code the same?

*Figure: Two code snippets displayed side-by-side in separate boxes, each showing a C++ member function definition for `Point::getX()`.*

**Left code box:**
```cpp
int Point::getX() {
    return x;
}
```

**Right code box:**
```cpp
int Point::getX() {
    return this->x;
}
```

✅ These are the same

---

## Slide 31: The importance of this

Are these two snippets of code the same?

*Figure: Two side-by-side code boxes displaying different implementations of the `setX` member function for a `Point` class. The left box shows `x = x;` inside the function body. The right box shows `this->x = x;` inside the function body. Below both boxes is a red cross mark (❌) with the text "Not the same", indicating the two snippets are not equivalent.*

**Left code box:**
```cpp
void Point::setX(int x)
{
    x = x;
}
```

**Right code box:**
```cpp
void Point::setX(int x)
{
    this->x = x;
}
```

❌ Not the same

---

## Slide 32: What is this?

*Figure: A diagram featuring a C++ code snippet in a white box with a drop shadow. Below the code box are two annotation boxes with arrows. The left annotation box contains the text "Point* this" and has an arrow pointing up to the `this` keyword in the code. The right annotation box contains the text "-> Mwahahaha pointer dereference" and has an arrow pointing up to the `->` operator in the code.*

```cpp
int Point::setX(int x)
{
    this->x = x;
}
```

---

## Slide 33: this in C++

**this in C++**

this is passed as a parameter to class function behind the scenes

*Figure: Two side-by-side white boxes containing C++ code examples. A smaller white callout box at the bottom right of the second box contains the text "Passing this as parameter".*

**Left Box:**
```cpp
int Point::getX() {
    return this->x;
}

// ...gets turned into...

int Point_getX(Point* this)
{ return this->x; }
```

**Right Box:**
```cpp
Point p {1,2};
int x = p.getX();

// ...gets turned into...

Point p {1,2};
int x = Point_getX(&p);
```

> Passing this as parameter

---

## Slide 34: What questions do you have?

*Figure: A photo of Bjarne Stroustrup, the creator of C++. He is wearing glasses and a patterned shirt, resting his chin on his hand as if about to speak. In the background, a poster or book cover is visible with the title "PROGRAMMING LANGUAGE" and the name "BJARNE STROUSTRUP".*

What questions do you have?

`bjarne_about_to_raise_hand`

---

## Slide 35: Inheritance

---

## Slide 36: Inheritance Definition
A mechanism for one class to inherit properties from another

---

## Slide 37: Many kinds of cars

*Figure: A diagram illustrating inheritance. At the top is a central box labeled "Car" containing a sketch of a sleek, teal-colored sports car. Four thick black arrows point down and out from this box to four specific car models below, each shown in a separate photograph. From left to right, the models are labeled "Toyota Camry" (a gray sedan), "Honda Civic" (a white sedan), "Ford Mustang" (a white sports car), and "Jeep Gladiator" (a red pickup truck). To the right of the "Car" box is a large text box.*

### Car
Many kinds of cars, but they all inherit
*   An engine
*   Wheels
*   A steering wheel

**Toyota Camry**
*Figure: Photograph of a gray Toyota Camry sedan parked in front of a building.*

**Honda Civic**
*Figure: Photograph of a white Honda Civic sedan parked on a paved surface with greenery in the background.*

**Ford Mustang**
*Figure: Photograph of a white Ford Mustang sports car parked in a parking lot.*

**Jeep Gladiator**
*Figure: Photograph of a red Jeep Gladiator pickup truck parked on a paved surface with people in the background.*

---

## Slide 38: Many kinds of shapes

*Figure: A diagram illustrating the concept of a general "Shape" and its derivatives. At the top center is the word "Shape" above a wireframe illustration of an abstract shape. To the right is a text box stating "Every shape has a • Volume • Surface area". Five thick black arrows originate from the "Shape" box and point downward to labels for five specific shapes. Below each label is a corresponding 3D model image.*

*   **Box**: A 3D model of a pink rectangular box.
*   **Sphere**: A 3D model of a teal sphere.
*   **Cone**: A 3D model of a blue cone.
*   **Ring**: A 3D model of a cyan ring/torus.
*   **Buckyball**: A 3D model of a green buckyball (truncated icosahedron).

Every shape has a
* Volume
* Surface area

---

## Slide 39: We’ve seen this before: streams!

*Figure: A class inheritance hierarchy for C++ streams. The diagram shows `ios_base` at the top, followed by `basic_ios<CharT, Traits>`. `basic_ios` has two immediate subclasses: `basic_ostream<CharT, Traits>` and `basic_istream<CharT, Traits>`. Both of these are further inherited by `basic_iostream<CharT, Traits>`. The next level shows `basic_ostringstream<CharT, Traits>` and `basic_ofstream<CharT, Traits>` inheriting from `basic_ostream`. In the middle, `basic_stringstream<CharT, Traits>` and `basic_fstream<CharT, Traits>` inherit from `basic_iostream`. On the right, `basic_istringstream<CharT, Traits>` and `basic_ifstream<CharT, Traits>` inherit from `basic_istream`.*

Is-A relationship: An `std::ifstream` **is a** `std::istream` **is a** `std::ios`

---

## Slide 40: How do we model inheritance in C++?

---

## Slide 41: Game Entity Identification in Fortnite

*Figure: A screenshot from the video game Fortnite depicting a battle scene in a grassy field with trees and buildings. Various objects are identified with yellow bounding boxes and corresponding labels.*
- A box around a large, rounded tree in the background with the label **Tree** above it.
- A box around a glowing, fast-moving object in the air with the label **Projectile** above it.
- A box around a character on the left holding a firearm with the label **Weapon** next to it.
- A box around a small character in the middle distance with the label **NPC** next to it.
- A box around a character in the foreground with the label **Player** below it.

The following text labels appear on the slide:
- Tree
- Projectile
- Weapon
- NPC
- Player

---

## Slide 42: Fortnite as classes

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
```

```cpp
class Projectile {
    double x, y, z;
    HitBox hitbox;
    double vx, vy, vz;
public:
    void update();
    void render();
};
```

```cpp
class Weapon {
    double x, y, z;
    HitBox hitbox;
    size_t ammo;
public:
    void fire();
    void update();
    void render();
};
```

```cpp
class Tree {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

```cpp
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

*Figure: Five C++ class definition boxes are arranged across the slide, each connected by a line to a screenshot from the Fortnite game depicting the corresponding entity. The `Player` class connects to an image of a male character with arm tattoos holding a weapon. The `Projectile` class connects to an image of a projectile (rocket) mid-flight. The `Weapon` class connects to an image of a first-person view holding a gun. The `Tree` class connects to an image of a large stylized tree in the game world. The `NPC` class (centered below the top row) connects to an image of a small character running in a grassy field.*

---

## Slide 43: There's a lot of redundancy here!

*Figure: The slide displays five separate boxes, each containing a C++ class definition for a different game object. Common member variables (`x, y, z`, `hitbox`) and functions (`update`, `render`) are highlighted in pink to demonstrate code redundancy across the classes. Each box is accompanied by a representative in-game image.*

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
```

*Figure: Below the `Player` class definition is an image of a game character holding and aiming a rifle.*

```cpp
class Projectile {
    double x, y, z;
    HitBox hitbox;
    double vx, vy, vz;
public:
    void update();
    void render();
};
```

*Figure: Below the `Projectile` class definition is an image of a rocket or missile flying through the air.*

```cpp
class Weapon {
    double x, y, z;
    HitBox hitbox;
    size_t ammo;
public:
    void fire();
    void update();
    void render();
};
```

*Figure: Below the `Weapon` class definition is an image showing a first-person perspective of a hand holding a rifle.*

```cpp
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

*Figure: Below the `NPC` class definition is a small image of a character running in a field.*

```cpp
class Tree {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

*Figure: Below the `Tree` class definition is an image of a large, leafy green tree in a mountainous game environment.*

---

## Slide 44: This model is also a pain to modify

Imagine we wanted to add an `overlapsWith` method to each object that checks if it overlaps in space with another object

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

*Figure: A C++ code snippet showing the `Player` class with five overloaded `overlapsWith` methods. To the right, a callout box with the text "This doesn't scale! What if we add more object types!"*

---

## Slide 45: Taking a step back

Entity

Many different objects, but they all share:
* A position in space
* A hitbox
* An update and render method!

*Figure: A diagram illustrating the concept of an "Entity" in game development. At the top center, the label "Entity" is shown above a screenshot of a 3D editor viewport displaying a translucent cube with a grid floor and colored coordinate axes (green Y-axis arrow pointing up, red dot on X-axis, blue arrow on Z-axis). A box to the right contains the shared attributes list. Five black arrows point downward and outward from the Entity image to five different game objects, each with a label and screenshot: "Player" (a third-person view of a muscular male character holding a weapon), "Projectile" (a glowing bullet/trail in flight through trees), "NPC" (a character running in a grassy area), "Weapon" (a first-person view of a rifle/scope being held), and "Tree" (a large stylized tree in a green landscape with a white arc in the background).*

---

## Slide 46: Introducing a common base class: Entity

### Entity

*Figure: A 3D cube with an orange outline, representing an entity in a game world. The cube is displayed in a dark editor viewport with a grid background. It has colored coordinate axes (red for X, green for Y, blue for Z) originating from its center.*

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

---

## Slide 47: Introducing a common base class: Entity

**Introducing a common base class: <span style="color: red; font-size: 1.2em;">Entity</span>**

*Figure: A diagram showing five different C++ classes (`Player`, `Projectile`, `Weapon`, `Tree`, `NPC`) at the top, with lines connecting them to a new base class `Entity` shown in a yellow-bordered box at the bottom left. Many member variables and functions in the top classes are highlighted in pink, indicating that they are duplicated across the classes and are being moved into the common `Entity` base class.*

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

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

---

## Slide 48: Now we inherit!

*Figure: A conceptual diagram of class inheritance in C++. The base class `Entity` is highlighted in the bottom left corner with a thick yellow border. Five derived classes are shown as separate boxes cascading toward the right: `Player` (top left), `Projectile` (top center), `Weapon` (middle center), `Tree` (middle right), and `NPC` (bottom right). In each derived class declaration, the inheritance notation `: Entity` is highlighted with a light purple background. In the top right corner, there is a meme image featuring a man in a suit (Borat) with the caption "VERY NICE" in large white block letters and a small "DigiByte" logo.*

### Base Class: Entity
```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

### Derived Classes

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

---

## Slide 49: Now we inherit!

*Figure: A C++ class inheritance diagram. A base class `Entity` is shown in a yellow-bordered box. Five derived classes (`Player`, `Projectile`, `Weapon`, `Tree`, and `NPC`) are shown in separate boxes with black arrows pointing from each derived class back to the base class `Entity`. The `Player` and `NPC` classes have redundant members (`double hitpoints;`) and methods (`void damage(double hp);`), both highlighted in pink.*

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

```cpp
class Player : Entity {
    double hitpoints;
public:
    void damage(double hp);
};
```

```cpp
class Projectile : Entity {
    double vx, vy, vz;
};
```

```cpp
class Weapon : Entity {
    size_t ammo;
public:
    void fire();
};
```

```cpp
class Tree : Entity {};
```

```cpp
class NPC : Entity {
    double hitpoints;
public:
    void damage(double hp);
};
```

**Notice**: there is still some redundancy!

---

## Slide 50: More layers of inheritance…

*Figure: A diagram showing a class hierarchy using inheritance. Class definitions are shown in boxes. The base class `Entity` is at the bottom left. The class `Actor` inherits from `Entity`. The classes `Projectile`, `Weapon`, and `Tree` also inherit from `Entity`. The classes `Player` and `NPC` inherit from `Actor`. Lines connect derived classes to their base classes to indicate the inheritance relationship.*

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

```cpp
class Player : Actor {};
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
class Tree : Entity {};
```

```cpp
class NPC : Actor {};
```

---

## Slide 51: An inheritance tree defines is-a relationships

*Figure: An inheritance tree diagram showing class relationships. The root class `class Entity { /* ... */ };` is in a yellow box. Arrows point down to four subclasses: `class Projectile : Entity { /* ... */ };`, `class Weapon : Entity { /* ... */ };`, `class Tree : Entity { /* ... */ };`, and `class Actor : Entity { /* ... */ };`. From `class Actor`, two further arrows point to its subclasses: `class Player : Actor { /* ... */ };` and `class NPC : Actor { /* ... */ };`. Arrows indicate inheritance direction from parent to child.*

```cpp
class Entity { /* ... */ };
```

```cpp
class Projectile : Entity
{ /* ... */ };
```

```cpp
class Weapon : Entity
{ /* ... */ };
```

```cpp
class Tree : Entity
{ /* ... */ };
```

```cpp
class Actor : Entity
{ /* ... */ };
```

```cpp
class Player : Actor
{ /* ... */ };
```

```cpp
class NPC : Actor
{ /* ... */ };
```

- “A Weapon is an Entity”
- “An NPC is an Actor, and is also an Entity”

---

## Slide 52: Defining common functionality is trivial!

Now we can check if two Entity's overlap, no matter what kind it is!

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

*Figure: A code snippet showing an `Entity` class definition and its usage. A callout box with a black arrow points to the `overlapsWith` function declaration, containing the instruction: "To implement, check x,y,z and hitbox to see if there was an overlap".*

---

## Slide 53: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup with his hand near his chin, appearing to be about to raise it. Below the image, the text "bjarne_about_to_raise_hand" is shown.*

---

## Slide 54: Note: access modifiers

That last line won’t actually work due to access modifiers!

```cpp
Player player { /* ... */ };
Projectile bullet { /* ... */ };
bool isHit = player.overlapsWith(bullet);
```

*Figure: A rectangular code box contains three lines of C++ code. The third line, "bool isHit = player.overlapsWith(bullet);", is highlighted in pink. An arrow points from a separate text box below, which states "Compiler: overlapsWith is inaccessible", to this highlighted line of code.*

---

## Slide 55: Note: access modifiers

By default, classes are inherited privately.

*Figure: A code snippet illustrating default private inheritance in C++ is enclosed in a thin black border box.*

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

---

## Slide 56: Note: access modifiers

We can fix this issue by inheriting Entity publicly!

*Figure: Two C++ class definitions (`Entity` and `Player`) enclosed in a black-bordered box. In the `Player` class declaration, the `public` inheritance keyword is highlighted with a pink background.*

```cpp
class Entity {
public:
    bool overlapsWith(const Entity& other);
};

class Player : public Entity {
    // Public inheritance:
    //   - private members of Entity are still inaccessible
    //   - public members become public (accessible to outside)
};
```

---

## Slide 57: Note: access modifiers

### private inheritance (default)

```cpp
class Child : private Parent
```

*Figure: A diagram illustrating access modifier transformation for private inheritance. A left box contains two lines: "private in parent" and "public in parent". An arrow points from this box to a right box containing "inaccessible in child" and "private in child".*

| In Parent | In Child |
|-----------|----------|
| private | inaccessible |
| public | private |

### public inheritance

```cpp
class Child : public Parent
```

*Figure: A diagram illustrating access modifier transformation for public inheritance. A left box contains two lines: "private in parent" and "public in parent". An arrow points from this box to a right box containing "inaccessible in child" and "public in child".*

| In Parent | In Child |
|-----------|----------|
| private | inaccessible |
| public | public |

*Note: The note at the bottom is enclosed in a box.* **Note:** public inheritance better models **is-a** relationships! A Player really is an Entity because it exposes all of Entity’s functionality publicly

---

## Slide 58: Note: protected access modifier

Protected members are visible to subclasses, but not the outside!
- Remember, class members are *private* by default

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
}
```

*Figure: The slide shows two code snippets side-by-side with annotations. The left snippet is for `class Entity` with a `protected` section containing `double x, y, z;` and `HitBox hitbox;`. An arrow points from a text box that says "We need to mark them protected inside Entity" to the `protected:` keyword. The right snippet is for `class Projectile : public Entity` with a `private` section and a `public` method `move()` that uses `x`, `y`, `z`. An arrow points from a text box that says "private by default" to the `private:` keyword. Another arrow points from a text box that says "In order to access x, y, and z inside Projectile" to the lines `x += vx; y += vy; z += vz;` in the `move()` method. The variables `x`, `y`, `z` in the `move()` method are highlighted in pink.*

---

## Slide 59: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup in a patterned shirt, with his hand near his chin. Behind him are computer monitors, one of which has a poster or screen showing "PROGRAMMING LANGUAGE BJARNE STROUSTRUP". Below the photograph is the caption in a monospaced font.*

What questions do you have?

`bjarne_about_to_raise_hand`

---

## Slide 60: Let's build a game!

Let's build a game!

---

## Slide 61: Let’s build a game!

*Figure: A yellow-bordered box on the left contains C++ code for an `Entity` class. A black arrow points from the `update()` and `render()` method declarations in the code to a black-bordered explanation box on the right.*

```cpp
class Entity {
    double x, y, z;
    HitBox hitbox;
public:
    void update();
    void render();
};
```

*Figure: A black-bordered box on the right contains explanatory text.*

We’ll implement the logic for our game by overriding `update` and `render` for each kind of `Entity`.

---

## Slide 62: Let's build a game!

Let's **override** the `update` and `render` function for each **Entity** type!

*Figure: A diagram showing two columns of stacked code boxes. The left column contains `update` functions, and the right column contains `render` functions. Each column shows implementations for `Player` and `Projectile`, followed by vertical ellipsis dots, and finally the default implementation for the base `Entity` class.*

### Update Functions

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

### Render Functions

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

---

## Slide 63: Let’s build a game!

A game is basically a collection of entities updated and rendered every frame!

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

*Figure: A screenshot of C++ code for a game loop. A red box highlights the `while (true)` loop. An arrow points from this red box to a text box that contains the text: "Game event loop (runs every frame)".*

---

## Slide 64: Let’s try it out!

Let’s try it out!

Links on this slide:
- <https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture09/part1.cpp>

---

## Slide 65: Problem Statement

It didn’t work! What’s going on!?

---

## Slide 66: Behind the scenes

Recall that C++ lays out the fields of an object sequentially

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

*Figure: A diagram showing the sequential memory layout of an `Entity` object. It features the label "Entity" above a vertical stack of four light-pink rectangular boxes. From top to bottom, the boxes are labeled "double x", "double y", "double z", and "HitBox hitbox".*

---

## Slide 67: Behind the scenes
C++ stacks the subclass’s members below the inherited ones!

```cpp
class Projectile
    : public Entity {
private:
    double vx, vy, vz;
public:
    void move();
}
```

*Figure: A diagram showing the memory layout for an object of the `Projectile` class. It is depicted as a vertical stack of boxes labeled "Projectile". The top four boxes, shaded in light pink, represent the members inherited from the `Entity` base class: `double x`, `double y`, `double z`, and `HitBox hitbox`. A red bracket points to this section with a callout that reads "Members inherited from Entity". Below these, three boxes shaded in light blue represent the members defined in the `Projectile` subclass itself: `double vx`, `double vy`, and `double vz`.*

---

## Slide 68: Behind the scenes

Be careful: when you assign a derived class to a base class, it gets sliced!

### Projectile
* double **x**
* double **y**
* double **z**
* HitBox **hitbox**
* double **vx**
* double **vy**
* double **vz**

### std::vector\<Entity\>

| Column 1 | Column 2 | Column 3 |
| :--- | :--- | :--- |
| double **x** | double **x** | double **x** |
| double **y** | double **y** | double **y** |
| double **z** | double **z** | double **z** |
| HitBox **hitbox** | HitBox **hitbox** | HitBox **hitbox** |

*Figure: A comparison of memory layouts showing the "Projectile" derived class and a "std::vector\<Entity\>" containing multiple "Entity" objects. The Projectile class contains four members (x, y, z, hitbox) shared with Entity, plus three additional members (vx, vy, vz) shown in blue. The vector of Entity objects only stores the four base members (shown in pink), demonstrating "object slicing" where the derived class data is lost.*

**Issue:** every element in the vector is an **Entity**, so the compiler calls **Entity::update()** (which does nothing) instead of **Player::update()**, **Tree::update()**, **Projectile::update**, etc.

---

## Slide 69: Projectile and Entity Mismatch

A Projectile doesn’t “fit” into an Entity

---

## Slide 70: Solution: Use an Entity* instead

Object slicing only happens when a copy is made!

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

*Figure: A code snippet showing the solution to object slicing. An arrow points from a callout box to the line declaring a `std::vector<Entity*>`. The callout box contains the text: "Storing pointers to entities here, not the entities themselves!"*

---

## Slide 71: Solution: Use an Entity* instead

Pointers retain the details of the subclass by avoiding copies

*Figure: A diagram titled `std::vector<Entity*>` showing an array of three pointers. Each of the three boxes in the array is labeled `Entity* ptr`. Curved black arrows point from each pointer to a different memory structure in the heap:*
* *The first arrow points to a **Player** object, which contains fields: `double x`, `double y`, `double z`, `HitBox hitbox` (all in pink-shaded cells), and `double hitpoints` (in a blue-shaded cell).*
* *The second arrow points to a **Tree** object, which contains fields: `double x`, `double y`, `double z`, and `HitBox hitbox` (all in pink-shaded cells).*
* *The third arrow points to a **Projectile** object, which contains fields: `double x`, `double y`, `double z`, `HitBox hitbox` (all in pink-shaded cells), and `double vx`, `double vy`, `double vz` (all in blue-shaded cells).*

---

## Slide 72: What questions do you have?
*Figure: A photograph of Bjarne Stroustrup resting his chin on his hand in a thoughtful pose. He is wearing glasses and a patterned shirt. In the background, a computer monitor and a poster with the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP" are visible.*

`bjarne_about_to_raise_hand`

---

## Slide 73: Let's try it again!

Links on this slide:
- <https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture09/part2.cpp>

---

## Slide 74: It still didn't work...

It still didn't work... 😭 😭 😭

*Figure: Three crying face emojis (😭) following the text.*

---

## Slide 75: Announcements
*   Assignment 1 due this Friday
*   A note on assignment workload!
    *   We want you guys to spend ~1 hour on each assignment!
    *   If you consistently spend more time than this, come to OH!
*   OH is 9:30-10:30am Mon, 3-4pm Friday… we are so lonely, please come!!

---

## Slide 76: Virtual Functions

Virtual Functions

---

## Slide 77: Problem: Which one is called?

* We have many different update methods

```cpp
void Projectile::update();
void NPC::update();
void Player::update();
void Entity::update();
```

* Given a pointer to an Entity, how does the compiler know which method to call?

```cpp
Entity* entity = entities[0];
entity->update();
```

---

## Slide 78: Problem: Which one is called?

* We should call the update method which matches the type of the object that `entity` points to
    * If `entity` points to a `Player`, we should call `Player::update()`
    * If it points to a `Projectile`, we should call `Projectile::update()` and so on
* But an `Entity*` alone doesn't tell us any information about the type!

*Figure: A conceptual diagram illustrating dynamic dispatch issues. On the left, a pointer labeled `Entity* entity` points with a black arrow to a memory structure labeled `Player`. The memory structure is a vertical stack of five fields: the first four (`double x`, `double y`, `double z`, `HitBox hitbox`) are in pink boxes, and the last one (`double hitpoints`) is in a light blue box. To the right of the memory structure, there is a section titled "Want to call" containing a box with the code `void Player::update();` and a section below it titled "Actually called" containing a box with the code `void Entity::update();`.*

---

## Slide 79: Problem: Which one is called?

- Given an `Entity*`, does it point to:

*Figure: A diagram with an `Entity* entity` pointer at the top, connected via dashed arrows to four possible derived/base type boxes: Player?, Projectile?, Tree?, Entity?. Shared `Entity` base class members are highlighted in light pink, while type-specific unique members are highlighted in light blue.*

### Player?
- double **x**
- double **y**
- double **z**
- HitBox **hitbox**
- double **hitpoints**

### Projectile?
- double **x**
- double **y**
- double **z**
- HitBox **hitbox**
- double **vx**
- double **vy**
- double **vz**

### Tree?
- double **x**
- double **y**
- double **z**
- HitBox **hitbox**

### Entity?
- double **x**
- double **y**
- double **z**
- HitBox **hitbox**

---

## Slide 80: Problem: Which one is called?

- The compiler defaults to assuming `entity` points to an `Entity`
- This is the only one it can be absolutely sure any entity will support

`Entity* entity`

*Figure: A diagram showing a pointer declaration `Entity* entity` at the top center. Four arrows branch out from it. Three dashed grey arrows point leftward to the labels `Player?`, `Projectile?`, and `Tree?` respectively. One solid red arrow points rightward to the label `Entity?`. Below each label is a memory layout table representing the struct members.*

**Player?**

| Member |
|---|
| `double x` |
| `double y` |
| `double z` |
| `HitBox hitbox` |
| `double hitpoints` |

**Projectile?**

| Member |
|---|
| `double x` |
| `double y` |
| `double z` |
| `HitBox hitbox` |
| `double vx` |
| `double vy` |
| `double vz` |

**Tree?**

| Member |
|---|
| `double x` |
| `double y` |
| `double z` |
| `HitBox hitbox` |

**Entity?**

| Member |
|---|
| `double x` |
| `double y` |
| `double z` |
| `HitBox hitbox` |

---

## Slide 81: Cost of Using Entity*
Using Entity* comes at a cost:
We “forget” which type the object actually is

---

## Slide 82: This is not what we wanted!

* Notice: there is a difference between the **compile-time** vs. **runtime** type of the object!
    * At compile time, it is treated as an **Entity**
    * At runtime, it could be an **Entity** or any subclass, e.g. **Projectile**, **Player**, etc.
* What we need is **dynamic dispatch**
* Depending on the runtime (dynamic) type of the object, a different method should be called (dispatched)!

---

## Slide 83: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup sitting in an office, looking thoughtful with his hand on his chin. He is wearing glasses and a patterned shirt. Behind him are posters and books, including "The C++ Programming Language" by Bjarne Stroustrup and "Programming: Principles and Practice Using C++".*

What questions do you have?

`bjarne_about_to_raise_hand`

---

## Slide 84: Introducing virtual functions

Introducing virtual functions

*Figure: A title slide with the text "Introducing virtual functions" centered on a white background. The word "virtual" is displayed in red, while the rest of the text is in black.*

---

## Slide 85: Virtual functions

*   Marking a function as `virtual` enables dynamic dispatch
*   Subclasses can `override` this method

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

*Figure: An arrow points from the text below to the `override` keyword in the `Projectile` class code block.*

`override` isn’t required but is good for readability! It will check that you are overriding a `virtual` method instead of creating a new one.

---

## Slide 86: Does it work?
Does it work?

YES!!! 😄

*Figure: A large yellow smiling emoji with a wide, open-mouthed smile and squinting eyes (😄).*

Links on this slide:
- <https://github.com/cs106l/cs106l-lecture-code/blob/main/lecture09/part3.cpp>

---

## Slide 87: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, creator of C++, sitting at a desk with a thoughtful expression. Behind him, posters for his books, including "The C++ Programming Language", are visible on the wall.*

`bjarne_about_to_raise_hand`

---

## Slide 88: How does it work?

How does it work?

---

## Slide 89: Behind the Scenes

- Adding **virtual** to a function adds some metadata to each object
- Specifically, it adds a pointer (called a **vpointer**) to a table (called a **vtable**) that says, for each **virtual** method, which function should be called for that object

*Figure: A memory layout diagram illustrating how virtual functions are handled behind the scenes. On the left, a pointer labeled `Entity* entity` points to a box representing a `Projectile` object. The object's memory contains several fields stacked vertically: `double x`, `double y`, `double z`, `HitBox hitbox`, `void* vpointer`, `double vx`, `double vy`, and `double vz`. An arrow originates from the `void* vpointer` field and points to a separate table (the vtable) on the right. This table contains two rows: the first row maps the method name `update` to the function implementation `Projectile::update()`, and the second row maps the method name `render` to the function implementation `Entity::render()`.*

---

## Slide 90: Behind the Scenes

```cpp
Entity* p = new Projectile { /* ... */ };
p->update();
```

*Figure: A diagram illustrating the memory layout and polymorphism mechanism for a `Projectile` object accessed via an `Entity*` pointer. A box labeled `Entity* entity` points to a larger box labeled `Projectile` (in red). The Projectile box is subdivided into fields. A black arrow points from the `void* vpointer` field within the Projectile box to a smaller, two-row table (the vtable) on the right.*

The fields within the `Projectile` object are listed as:
- double x
- double y
- double z
- HitBox hitbox
- void* vpointer
- double vx
- double vy
- double vz

The vtable, pointed to by the vpointer, contains the following entries:

| Function | Implementation |
|---|---|
| update | Projectile::update() |
| render | Entity::render() |

---

## Slide 91: Recall: Classes in Python

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

`p = Point(1, 2)`

*Figure: A diagram illustrating object memory layout. A box labeled `p` has an arrow pointing to a larger rectangular structure representing an object. The object contains four fields arranged vertically: `refcount`, `type`, `_x`, and `_y`.*

> Python **stores extra information** about the type of the object in its memory footprint! This enables runtime type checking.

---

## Slide 92: virtual is kind of like Python

Both Python and C++ **virtual** functions store type-specific information

*Figure: Two diagrams comparing how virtual functions work in C++ and Python.*

### Left Diagram (C++)
The diagram shows a C++ memory layout for an object accessed through a base class pointer.
- At the top: `Entity* p = /* ... */;`
- Below that: `Projectile` (in red) above a memory layout table.
- A box labeled `Entity* entity` has a thick black arrow pointing to the top row of the table.
- The memory layout table has the following rows:
  - double x
  - double y
  - double z
  - HitBox hitbox
  - void* vpointer (this row is highlighted in a lighter color)
  - double vx
  - double vy
  - double vz

### Right Diagram (Python)
The diagram shows a Python memory layout for an object.
- At the top: `p = Point(1, 2)`
- Below that is a memory layout table.
- A box labeled `p` has a thick black arrow pointing to the top row of the table.
- The memory layout table has the following rows:
  - refcount
  - type
  - _x (this row is highlighted in a lighter color)
  - _y (this row is highlighted in a lighter color)

---

## Slide 93: Quick check: pros/cons of virtual functions?

- Turn to a partner and talk about:
  - When might you want to use a virtual function?
  - When might you **not** want to use a virtual function?

---

## Slide 94: Quick check: pros/cons of virtual functions?
- Turn to a partner and talk about:
  - When might you want to use a virtual function?
  - When might you **not** want to use a virtual function?
- In many other languages, class functions are virtual by default
- **Key idea:** In C++, you have to opt in because they are more expensive
  - Increased **size** of memory layout of the class
  - Takes **longer** to look up **vtable** and call the method
- In quant finance and industries where nanoseconds count, virtual functions are not used!

---

## Slide 95: What questions do you have?

*Figure: A photograph of a man with glasses and a patterned shirt, resting his chin on his hand. Behind him are computer monitors and posters, one of which reads "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". Below the image is a caption in a monospaced font.*

What questions do you have?

`bjarne_about_to_raise_hand`

---

## Slide 96: Pure virtual functions

*Figure: A white rectangular box with a thin black border and a drop shadow containing C++ code.*

```cpp
class Entity {
public:
    virtual void update() = 0;
    virtual void render() = 0;
};
```

---

## Slide 97: Pure virtual functions

```cpp
class Entity {
public:
    virtual void update() = 0;
    virtual void render() = 0;
};
```

*Figure: A code snippet of a class `Entity` with two pure virtual functions, `update` and `render`. A callout box on the right explains the syntax.*

Mark a virtual function as pure virtual by adding = 0; instead of an implementation!

---

## Slide 98: Pure virtual functions
- A class with one or more pure virtual functions is an **abstract** class, it can't be instantiated!
- Overriding all of the pure virtual functions makes the class **concrete**!

*Figure: Two side-by-side white boxes containing C++ code examples. The left box demonstrates an abstract class `Entity` and includes a comment indicating it cannot be instantiated. The right box demonstrates a derived class `Projectile` that provides implementations for all pure virtual functions and includes a comment indicating it can be instantiated.*

```cpp
class Entity {
public:
    virtual void update() = 0;
    virtual void render() = 0;
};

Entity e;
// ❌ Entity is abstract!
```

```cpp
class Projectile
    : public Entity {
public:
    void update() override {};
    void render() override {};
};

Projectile p;
// ✅ Projectile is concrete
```

---

## Slide 99: Pure virtual functions

Pure virtual functions are useful when there’s **no clear default implementation**!

*Figure: A diagram showing a central `Shape` node at the top. Black arrows point downward from `Shape` to five different concrete shapes, each depicted with a small image and label: `Box` (a pink cube), `Sphere` (a green ball), `Cone` (a blue cone), `Ring` (a teal torus), and `Buckyball` (a green polyhedron).*

```cpp
class Shape {
public:
    virtual double volume() = 0;
};
```

What’s the default volume of a `Shape`? Let’s mark it pure virtual and let subclass decide!

---

## Slide 100: Questions Slide

*Figure: A photograph of Bjarne Stroustrup, a man with glasses and a patterned shirt, sitting in front of a computer monitor. He has his hand near his chin as if about to raise it. Behind him on a shelf are book titles including "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP".*

What questions do you have?

`bjarne_about_to_raise_hand`

---

## Slide 101: Closing Thoughts

Closing Thoughts

---

## Slide 102: Sometimes inheritance can get out of hand

*Figure: A complex UML class diagram illustrating a game engine architecture. The diagram shows numerous inheritance, composition, and implementation relationships between classes. The central class is "Game," with various subsystems branching out. Several classes in the "State" hierarchy are highlighted with dashed blue outlines.*

*   **Game**
    *   Composition/Association with: `StartMenu` (1), `AudioRenderer`, `VideoRenderer`, `PhysicsEngine`, `InputHandler`, `GlobalAI`, `Level`, `TimeTracker`, `GameSession`, and `Matter` (1).
*   **State Hierarchy (PhysicsEngine branch)**
    *   `PhysicsEngine` is associated with `TimeRecorder`.
    *   `TimeRecorder` is associated with `SavedState`.
    *   `SavedState` implements `«interface» Saveable`.
    *   `SavedState` is the parent of `MatterState` and `AnimationState`.
    *   `MatterState` is the parent of `SpriteState`.
*   **Input Hierarchy (InputHandler branch)**
    *   `InputHandler` is associated with `InputSource`.
    *   `InputSource` is the parent of `InputSourceRemote` and `InputSourceKeyboard`.
    *   `InputSource` is associated with `InputSourceBuffer`.
    *   `InputSourceBuffer` is associated with `InputStates`.
    *   `InputStates` is associated with `KeyStates` (multiplicity 1).
    *   `KeyStates` is associated with `KeyMap`.
*   **Time Hierarchy (TimeTracker branch)**
    *   `TimeTracker` is associated with `Timeable`.
    *   `Timeable` is the parent of `TimeCounter` and `TimeIntervalCounter`.
*   **Network/Session Hierarchy (GameSession branch)**
    *   `GameSession` is associated with `RemoteDataSource` and `RemoteDataDispatcher`.
*   **Entity Hierarchy (Matter branch)**
    *   `Matter` is the parent of `Sprite`.
    *   `Sprite` is the parent of `IntelligentSprite` and `SpriteAnimation`.
    *   `SpriteAnimation` is the parent of `CollidableAnimation`.
    *   `SpriteAnimation` implements `«interface» Animation`.
    *   `CollidableAnimation` implements `«interface» Collidable`.

*Note: The classes `TimeRecorder`, `SavedState`, `MatterState`, `AnimationState`, and `SpriteState` are outlined with dashed blue borders.*

---

## Slide 103: Sometimes inheritance can get out of hand
* Big inheritance trees tend to be **slower** and **harder to reason about**
  * In video games, approach of subclassing for every different object type is uncommon among modern game engines
  * Composition is often more flexible and just makes sense

---

## Slide 104: Confused Cat Meme
"A car is an engine"

*Figure: A two-panel meme featuring a white cat with black markings on its head. In the top panel, the cat looks upward and to the left with a confused expression. In the bottom panel, the cat looks directly at the camera with wide eyes. The word "HUH!?" is written in large, bold, white block letters with a black outline, superimposed over the bottom of the second cat image.*

---

## Slide 105: Roll Safe Meme

*Figure: A two-panel meme featuring Kayode Ewumi as the character "Roll Safe." The image is duplicated, appearing once above and once below a line of text. In the image, he is smiling smugly and pointing his right index finger to his temple, suggesting a clever or cleverly overlooked insight.*

"A car ~~is~~ has an engine"

---

## Slide 106: Prefer composition over inheritance

Inheritance is a powerful tool, but sometimes, composition just makes more sense!

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

*Figure: A photo of a man scratching his head with a confused expression, located at the bottom right of the first code box.*

```cpp
class Car {
    Engine engine;
    SteeringWheel wheel;
    Brakes brakes;
};
```

---

## Slide 107: Prefer composition and inheritance

Combining both of these ideas can give the best of both worlds!

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

*Figure: A slide showing C++ code examples combining composition and inheritance. The slide contains a code box with two sections. The top section shows a `Car` class that uses composition by holding pointers to `Engine`, `SteeringWheel`, and `Brakes` objects. The bottom section shows an inheritance hierarchy starting with a base `Engine` class, a derived `CombustionEngine` class, and then further derived classes `GasEngine` and `DieselEngine` inheriting from `CombustionEngine`, plus `ElectricEngine` inheriting directly from `Engine`. To the right of the code, there is a callout box containing the text: "If you want to see one place this technique is used in C++, look up the PIMPL idiom!" with "PIMPL" underlined. In the slide title, the word "and" is colored red.*

Links on this slide:
- <https://en.cppreference.com/w/cpp/language/pimpl>

---

## Slide 108: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup with his hand positioned under his chin as if about to raise it. Behind him are book covers, including one titled "Bjarne STROUSTRUP", and computer monitors. Below the image is the text `bjarne_about_to_raise_hand`.*

---

## Slide 109: Parrot with weekend greeting
*Figure: A close-up, slightly blurred photograph of a green-cheeked conure parrot. The parrot has a dark grey head, a white ring around its eye, a dark beak, and green feathers on its body with red tail feathers visible. It is perched on a metallic stand, looking directly at the camera. To the left of the parrot, overlaid text reads "have a good weekend :D".*

have a
good
weekend
:D
