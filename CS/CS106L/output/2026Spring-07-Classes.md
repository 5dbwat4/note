# Lecture 07: Classes (2026Spring)

> PDF title: 2026Spring-07-Classes.pptx
> Source: `assets/slides/2026Spring-07-Classes.pdf` · 102 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: CS106L Lecture 7: Classes

*Figure: A title slide with a light blue gradient background.*

# CS106L Lecture 7:
# Classes

Preston Seay, Rachel Fernandez

---

## Slide 2: Attendance

*Figure: A large, standard QR code for attendance purposes, centered on the slide below the title.*

---

## Slide 3: cake or pie :o

cake or pie :o
24 responses

*Figure: A pie chart showing survey results from 24 responses. The chart is divided into three segments. A large blue segment, labeled 58.3%, represents "cake". A smaller red segment, labeled 20.8%, represents "pie". A smaller orange segment, also labeled 20.8%, represents "i have to pick??????". The legend to the right of the chart matches the colors to the categories: a blue dot for "cake", a red dot for "pie", and an orange dot for "i have to pick??????".*

---

## Slide 4: cake or pie :o
24 responses

*Figure: A 3D pie chart represented as a blue frosted cake with three sections. A small icon of a cake slice and a pie slice are visible at the bottom edge of the cake.*

* cake
* pie
* i have to pick??????

Percentages labeled on the cake slices:
* 58.3%
* 20.8%
* 20.8%

---

## Slide 5: Iterators Recap

*Figure: A diagram illustrating the C++ iterator hierarchy. Five green boxes with white text are arranged in a vertical structure with branching at the top. At the bottom is "Random Access Iterator", with an arrow pointing up to "Bidirectional Iterator". From "Bidirectional Iterator", an arrow points up to "Forward Iterator". From "Forward Iterator", two arrows point up: one to "Input Iterator" on the top-left and one to "Output Iterator" on the top-right. The arrows point from more specific iterator types towards the more general types they refine.*

Input Iterator
Output Iterator
Forward Iterator
Bidirectional Iterator
Random Access Iterator

1. What can you do with a Bidirectional Iterator that you cannot do with an Input Iterator?
2. What can you do with a Random Access Iterator that you cannot do with a Bidirectional Iterator?
3. What type of iterator is `std::set<int>::iterator`?

---

## Slide 6: Iterators Recap

*Figure: A conceptual diagram illustrating the hierarchy of C++ iterator categories. Categories are shown in green boxes, with arrows pointing from more powerful iterator types toward the types they relate to or inherit from. Each box has a parenthetical note describing its key characteristic.*

*   **Random Access Iterator** (can skip elements)
    *   *Arrow points to:* **Bidirectional Iterator** (multi direction)
    *   To the left of this box is the label: `(Answer to 3)`
    *   *Arrow points to:* **Forward Iterator** (multi pass)
        *   *Arrow points to:* **Input Iterator** (single pass)
        *   *Arrow points to:* **Output Iterator** (single pass)

1.  What can you do with a Bidirectional Iterator that you cannot do with an Input Iterator?
2.  What can you do with a Random Access Iterator that you cannot do with a Bidirectional Iterator?
3.  What type of iterator is `std::set<int>::iterator`?

---

## Slide 7: Today's Agenda

1. Classes
2. Inheritance
3. Virtuality

---

## Slide 8: Why classes?

*   C has no objects.
    *   C++ was originally called “C with classes.”
*   No way of encapsulating data and the functions that operate on that data.
*   No ability to have object-oriented programming (OOP) design patterns.

---

## Slide 9: What is object-oriented-programming?
*   Object-oriented-programming is centered around **objects**.
*   Focuses on design and implementation of classes!
*   Classes are the **user-defined types** that can be declared as an object!

---

## Slide 10: What is object-oriented-programming?

*Figure: A photograph illustrating the concept of object-oriented programming. A person is using a star-shaped cookie cutter to cut dough. To the left, two finished star-shaped cookies sit on a baking sheet. The cookie cutter, representing the "class" or template, is labeled in red text with `class Cookie { ... };`. The individual finished cookies, representing "objects", are labeled in red text as `Cookie c1;` and `Cookie c2;` respectively.*

---

## Slide 11: Surprise!

Containers are classes defined in the STL!

🥳

---

## Slide 12: Comparing 'struct' and 'class'

> classes containing a sequence of objects of various types, a set of functions for manipulating these objects, and a set of restrictions on the access of these objects and function;
>
> structures which are classes without access restrictions;

Bjarne Stroustrup, The C++ Programming Language – Reference Manual, §4.4 Derived types

---

## Slide 13: Comparing 'struct' and 'class'

> classes *containing a sequence of objects of various types, a set*
> *of functions for manipulating these objects, and a set of*
> *restrictions on the access of these objects and function;*
>
> structures *which are classes without access restrictions;*

Bjarne Stroustrup, The C++ Programming Language – Reference
Manual, §4.4 Derived types

*Figure: In the bottom right corner, a small photo of Bjarne Stroustrup sitting at a desk with a computer monitor behind him, gesturing with his hand.*

---

## Slide 14: Recall the ‘struct’

```cpp
struct StanfordID {
    std::string name; // these are fields!
    std::string sunet;
    int idNumber;
};

StanfordID s;
s.name = “Preston Seay”;
s.sunet = “pseay”;
s.idNumber = 01243425;
```

---

## Slide 15: Recall the ‘struct’

```cpp
struct StanfordID {
    std::string name; // these are fields!
    std::string sunet;
    int idNumber;
};

StanfordID s;
s.name = “Preston Seay”;
s.sunet = “pseay”;
s.idNumber = 01243425;
```

*Figure: A callout bubble with an arrow pointing to the `struct` definition. The bubble contains the text: "All these fields are public, i.e. can be changed by the user".*

---

## Slide 16: Recall the ‘struct’

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
s.idNumber = -12345; // 💀?
```

*Figure: A text box annotation pointing to the struct definition says: "All these fields are public, i.e. can be changed by the user".*

---

## Slide 17: Recall the ‘struct’

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
s.idNumber = -12345; // 💀?
```

*Figure: A gray rounded rectangle note appears at the bottom right, pointing toward the code. It reads: "By default, there are no direct access controls while using structs".*

---

## Slide 18: What questions do we have?

*Figure: A close-up photograph of an ostrich's head and neck, tilted towards the camera with a curious or whimsical expression, set against a background of a blue sky with soft white clouds.*

---

## Slide 19: As you might have guessed

```cpp
class ClassName {
private:

public:

}
```

*Figure: A blurry photograph of a crowd of people on a street, placed within the `private:` section of the code block to represent internal/private data.*

*Figure: A photograph of an open window looking out onto a sunny green valley, placed within the `public:` section of the code block to represent external/public access.*

Classes have **public** and **private** sections!

---

## Slide 20: User can access the public

```cpp
class ClassName {
private:
```

*Figure: Inside the `private:` section of the code, an image of a blurry street scene with people walking is shown.*

```cpp
public:
```

*Figure: Inside the `public:` section of the code, an image of an open window with a landscape view is shown.*

```cpp
}
```

Classes have public and private sections!
A user can access the **public** stuff

*Figure: On the right side of the slide, a rounded rectangle contains the text: "Classes have **public** and **private** sections! A user can access the **public** stuff".*

---

## Slide 21: User is restricted from **private**

```cpp
class ClassName {
private:
public:
}
```

*Figure: A diagram illustrating class structure. Under the `private:` label, there is a blurred image of people walking on a street, symbolizing hidden or restricted content. Under the `public:` label, there is an image of an open window looking out onto a sunny landscape, symbolizing accessible content. The entire code block and images are enclosed within a black border.*

Classes have **public** and **private** sections!
A user can access the **public** stuff
But is <u>**restricted**</u> from accessing the private stuff

---

## Slide 22: A backpack

*Figure: Two backpacks are shown. On the left is a transparent plastic backpack with black trim and shoulder straps. On the right is a black backpack with several zippered compartments open, revealing a white electronic device in a top pocket, baby bottles in an insulated middle compartment, and a small accessory pouch at the bottom.*

---

## Slide 23: A backpack

### Struct

*Figure: An image of a simple, transparent backpack with black trim and straps.*

### Class

*Figure: An image of a complex black backpack with multiple zippered compartments, including one open pocket containing baby bottles and another showing a small white electronic device.*

---

## Slide 24: Meme

*Figure: A classic "Distracted Boyfriend" meme. In the center, a man in a blue plaid shirt (labeled "ME" in large white text) is looking back over his shoulder at a woman in a red dress (labeled "CLASSES" in large white text) walking past. To his right, his girlfriend in a blue top (labeled "STRUCTS" in large white text) looks on with a shocked and disapproving expression. The scene is a blurred city street. A small "imgflip.com" watermark is in the bottom-left corner of the meme image.*

---

## Slide 25: Let’s make a StanfordID class based
on our struct!

---

## Slide 26: Header File (.h) vs Source Files (.cpp)

*Figure: A horizontal banner at the top of the slide with a light blue gradient background.*

| | Header File (.h) | Source File (.cpp) |
| :--- | :--- | :--- |
| **Purpose** | Defines the interface | Implements class functions |
| **Contains** | Function prototypes, class declarations, type definitions, macros, constants | Function implementations, executable code |
| **Access** | This is shared across source files | Is compiled into an object file |
| **Example** | `void someFunction();` | `void someFunction()`<br>`{...};` |

---

## Slide 27: Header File (.h) vs Source Files (.cpp)

| | **Header File (.h)** | **Source File (.cpp)** |
| :--- | :--- | :--- |
| **Purpose** | Defines the interface | Implements class functions |
| **Contains** | Function prototypes, class declarations, type definitions, macros, constants | Function implementations, executable code |
| **Access** | This is shared across source files | Is compiled into an object file |
| **Example** | `void someFunction();` | `void someFunction() {...};` |

---

## Slide 28: Header File (.h) vs Source Files (.cpp)

| | **Header File (.h)** | **Source File (.cpp)** |
| :--- | :--- | :--- |
| **Purpose** | Defines the interface | Implements class functions |
| **Contains** | Function prototypes, class declarations, type definitions, macros, constants | Function implementations, executable code |
| **Access** | This is shared across source files | Is compiled into an object file |
| **Example** | `void someFunction();` | `void someFunction()`<br>`{...};` |

*Figure: A comparison table between Header Files (.h) and Source Files (.cpp) in C++, detailing their purpose, contents, access, and providing code examples.*

---

## Slide 29: Class design
*   A constructor
*   Private member functions/variables
*   Public member functions (interface for a user)
*   Destructor

---

## Slide 30: Constructor
*   The constructor initializes the state of newly created objects

---

## Slide 31: Constructor

*   The constructor initializes the state of newly created objects
*   For our **StanfordID** class what do our objects need?

---

## Slide 32: Constructor

*   The constructor initializes the state of newly created objects
*   For our **StanfordID** class what do our objects need?

```cpp
s.name = “Preston Seay”;
s.sunet = “pseay”;
s.idNumber = 01243425;
```

---

## Slide 33: Constructor

### .h file

*Figure: A slide with a light blue banner at the top containing the title "Constructor" in black. Below the banner, the label ".h file" is centered. Underneath is a rectangular box with a black border containing a partial C++ class definition for "StanfordID". The keywords "class", "private:", and "public:" are shown in red text, and large black question marks serve as placeholders for the class's private members and public interface.*

```cpp
class StanfordID {
private:
?
public:
?
};
```

---

## Slide 34: Constructor

.h file

```cpp
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    // constructor for our StudentID
    StanfordID(std::string name, std::string sunet, int idNumber);
}
```

---

## Slide 35: Constructor

### .h file

```cpp
class StanfordID {
private:
std::string name;
std::string sunet;
int idNumber;

public:
// constructor for our StudentID
StanfordID(std::string name, std::string sunet, int idNumber);
}
```

*Figure: A rounded callout box at the bottom of the slide contains the text: "The syntax for the constructor is just the name of the class".*

---

## Slide 36: Constructor

### .h file

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

*Figure: A white box with a black border containing a C++ header file snippet. The snippet defines a `StanfordID` class with private member variables (`name`, `sunet`, `idNumber`) and public methods, including a constructor and several getter functions. Syntax highlighting is used for keywords, types, and comments.*

---

## Slide 37: Parameterized Constructor

‼.cpp file‼ (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    idNumber = idNumber;
}
```

---

## Slide 38: Parameterized Constructor

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    idNumber = idNumber;
}
```

*Figure: A rounded rectangle callout box containing the note: "Remember namespaces, like std::"*

---

## Slide 39: Parameterized Constructor

### .cpp file (implementation)

```cpp
#include “StanfordID.h”
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    idNumber = idNumber;
}
```

*Figure: A text box with an arrow or pointer pointing to the scope resolution operator `StanfordID::` in the code. The box contains the note: "This class scope works like a namespace, such as `std::`. In our `.cpp` file we need to use our class as our scope when defining our member functions".*

---

## Slide 40: Parameterized Constructor

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    if ( idNumber > 0 ) idNumber = idNumber;
}
```

*Figure: A speech bubble callout box positioned at the bottom of the slide containing the text: "We can now also enforce checks on the values that we initialize or modify our members to!"*

---

## Slide 41: What questions do we have?

*Figure: A close-up photograph of an ostrich's head and neck against a blue sky with some clouds. The ostrich has a curious or skeptical expression, looking towards the camera.*

---

## Slide 42: Parameterized Constructor

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    if ( idNumber > 0 ) idNumber = idNumber;
}
```

*Figure: A rounded rectangular callout bubble to the right of the code block contains the question "Does anyone see a problem here?".*

---

## Slide 43: Parameterized Constructor

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    name = name;
    sunet = sunet;
    if ( idNumber > 0 ) idNumber = idNumber;
}
```

*Figure: The left-hand side variable `name` in the assignment `name = name;` is highlighted in yellow. A callout box positioned to the right of the code block contains the text: "Does anyone see a problem here?"*

---

## Slide 44: Our .h definition

### .h file

```cpp
#include <string>
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    // constructor for our student
    StanfordID(std::string name, std::string sunet, int idNumber);
    // method to get name, sunet, and idNumber, respectively
    std::string getName();
    std::string getSunet();
    int getID();
}
```

---

## Slide 45: <n>: Use the **this** keyword

.cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    this->name = name;
    this->state = state;
    this->age = age;
}
```

*Figure: A white speech-bubble callout box with a pointer directed toward the line `this->name = name;`. The text inside the callout reads: "Use this `this` keyword to disambiguate which ‘name’ you’re referring to." The word "this" (after "this") is highlighted in a pink font color.*

---

## Slide 46: List initialization constructor (C++11)

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

// list initialization constructor
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber):
name{name}, sunet{sunet}, idNumber{idNumber} {};
```

*Figure: A rounded rectangular callout box positioned to the right of the code, containing the following text:*
Here, we use uniform initialization for each item!
(Notice the {}.)

---

## Slide 47: Default constructor

### .cpp file (implementation)

*Figure: A slide with a light blue title bar at the top and a large white box with a black border below it. The title bar contains the text "Default constructor". Inside the box, there is a header reading ".cpp file (implementation)". Below the header is a C++ code snippet. To the right of the code, there is a light grey callout bubble with rounded corners.*

```cpp
#include "StanfordID.h"
#include <string>

// default constructor
StanfordID::StanfordID() {
    name = "John Appleseed";
    sunet = "jappleseed";
    idNumber = 00000001;
}
```

*Callout bubble text: If we call our constructor without parameters we can set default ones!*

---

## Slide 48: Constructor Overload

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

// default constructor
StanfordID::StanfordID() {
    name = "John Appleseed";
    sunet = "jappleseed";
    idNumber = 00000001;
}
// parameterized constructor
StanfordID::StanfordID(std::string name, std::string sunet, int idNumber) {
    this->name = name;
    this->state = state;
    this->age = age;
}
```

*Figure: A rounded rectangular callout box containing the text: "Our compilers will know which one we want to use based on the inputs!"*

---

## Slide 49: Back to our class definition

.h file

*Figure: A code block within a black border showing a C++ class definition. The code has syntax coloring with keywords like "private" and "public" in red, type names like "std::string" and "int" in blue/green, and comments in purple. The three getter methods at the end are highlighted with a yellow background.*

```cpp
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    /// constructor for our student
    StanfordID(std::string name, std::string sunet, int idNumber);
    /// method to get name, sunet, and ID, respectively
    std::string getName();
    std::string getSunet();
    int getID();
}
```

---

## Slide 50: Let's implement them

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

std::string StanfordID::getName() {

}

std::string StanfordID::getSunet() {

}

int StanfordID::getID() {

}
```

---

## Slide 51: Implemented members

.cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

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

---

## Slide 52: Implemented members (setter functions)

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

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

}

---

## Slide 53: The destructor
.cpp file (implementation)
```cpp
#include "StanfordID.h"
#include <string>

StanfordID::~StanfordID() {
    // free/deallocate any data here
}
```

---

## Slide 54: The destructor

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::~StanfordID() {
    // free/deallocate any data here
}
```

*Figure: A rounded rectangular callout box positioned to the right of the code block, containing explanatory text.*

In our **StanfordID** class we are not dynamically allocating any data by using the **new** keyword

---

## Slide 55: The destructor

.cpp file (implementation)

*Figure: A large black-bordered rectangular box containing a C++ code snippet and a text callout.*

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::~StanfordID() {
    // free/deallocate any data here
}
```

*Figure: A light-gray rounded rectangular callout positioned in the bottom-right corner of the code box.*

Nonetheless destructors are an important part of an object's lifecycle.

---

## Slide 56: The destructor

### .cpp file (implementation)

```cpp
#include "StanfordID.h"
#include <string>

StanfordID::~StanfordID() {
    // free/deallocate any data here

    delete [] my_array; // for illustration
}
```

*Figure: A black-bordered box containing a C++ code snippet. The code shows the implementation of a destructor for the `StanfordID` class. The destructor's purpose is indicated by the comment `// free/deallocate any data here`, followed by an example deallocation line.*

*Figure: A light gray, rounded rectangle positioned to the right of the code box, containing the following text:*
"The destructor is not explicitly called, it is automatically called when an object goes out of scope"

---

## Slide 57: Some other cool class stuff

**Type aliasing** - allows you to create synonymous identifiers for types

```cpp
template <typename T>
class vector {
    using iterator = T*;

    // Implementation details...
};
```

---

## Slide 58: Back to our class definition

### .h file

```cpp
class StanfordID {
private:
    // An example of type aliasing
    using String = std::string;
    String name;
    String sunet;
    int idNumber;

public:
    // constructor for our student
    StanfordID(String name, String sunet, int idNumber);
    // method to get name, sunet, and idNumber, respectively
    String getName();
    String getSunet();
    int getID();
}
```

*Figure: A slide showing a C++ class definition in a header (.h) file. The code is displayed in a monospace font with syntax highlighting (keywords in red, comments in purple, types in blue/green, and function names in black). The class is named `StanfordID` and includes private member variables and public methods as transcribed above.*

---

## Slide 59: What questions do we have?
*Figure: A close-up photograph of an ostrich's head against a blue, slightly cloudy sky. The ostrich is looking directly towards the viewer with a curious or quizzical expression, its beak slightly open.*

---

## Slide 60: Practice!

**Task:** Implement the wizard class and spellbook class, so that the wizard can cast some spells. 🧙🔥❄

*Figure: A large QR code. Below the QR code is a hyperlink: [https://www.online-ide.com/FBmGUSovnC](https://www.online-ide.com/FBmGUSovnC).*

Links on this slide:
- <https://www.online-ide.com/FBmGUSovnC>

---

## Slide 61: Plan

1. Classes
2. **Inheritance**
3. Virtuality

---

## Slide 62: (Class) Inheritance

*Figure: A hand-drawn diagram illustrating class inheritance. At the top is a single box labeled "Base Class". From this base class, two arrows point downward to two separate boxes. The left arrow points to a box labeled "Sub class 1". The right arrow points to a box labeled "Sub class 2". The diagram shows that both "Sub class 1" and "Sub class 2" inherit from the "Base Class".*

---

## Slide 63: Circling back to this diagram

*Figure: A hierarchical class inheritance diagram for the C++ standard library I/O streams. Arrows indicate inheritance from the derived class (bottom) to the base class (top).*

- `ios_base`
    - `basic_ios <CharT, Traits>`
        - `basic_ostream <CharT, Traits>`
            - `basic_ostringstream <CharT, Traits>`
            - `basic_ofstream <CharT, Traits>`
        - `basic_istream <CharT, Traits>`
            - `basic_istringstream <CharT, Traits>`
            - `basic_ifstream <CharT, Traits>`
        - `basic_iostream <CharT, Traits>` (inherits from `basic_ostream` and `basic_istream`)
            - `basic_stringstream <CharT, Traits>`
            - `basic_fstream <CharT, Traits>`

*Inheritance diagram*

---

## Slide 64: Inheritance

* **Dynamic Polymorphism:** Different types of objects may need the same interface.

---

## Slide 65: Inheritance

* **Dynamic Polymorphism**: Different types of objects may need the same interface.
* **Extensibility**: Inheritance allows you to extend a class by creating a subclass with specific properties.

---

## Slide 66: Inheritance in practice

*Figure: A 3×5 grid of fifteen labeled 3D geometric shapes, shown as light-blue wireframe/semi-transparent renderings.*

**Top row (left to right):**

- *Figure: A cone with its top sliced off, creating a flat circular top surface.* — Cone with flat top
- *Figure: A pentagonal pyramid with its top sliced off, creating a flat pentagonal top surface.* — Pentagonal pyramid with flat top
- *Figure: A standard cone with a pointed apex.* — Cone
- *Figure: A pyramid with a square base and four triangular faces meeting at a single apex.* — 4-sided pyramid
- *Figure: A cube.* — Cube

**Middle row (left to right):**

- *Figure: A rectangular box (rectangular prism/cuboid).* — Rectangular box
- *Figure: A tetrahedron (triangular pyramid) with a triangular base.* — Tetrahedron
- *Figure: A pyramid with a square base.* — Pyramid
- *Figure: A pyramid with its top sliced off, creating a flat square top surface.* — Pyramid with flat top
- *Figure: An octahedron (eight triangular faces).* — Octahedron

**Bottom row (left to right):**

- *Figure: A cone with a pentagonal base.* — Pentagonal cone
- *Figure: An irregular polyhedron with non-uniform faces and multiple vertices.* — Irregular polyhedron
- *Figure: An icosahedron (twenty triangular faces).* — Icosahedron
- *Figure: A dodecahedron (twelve pentagonal faces).* — Dodecahedron
- *Figure: A half sphere (hemisphere), a sphere sliced through its equator.* — Half sphere

[source]

Links on this slide:
- <https://www.conceptdraw.com/examples/pyramid-geometrical-figures>

---

## Slide 67: Inheritance in practice

*Figure: A collection of fifteen 3D geometric shapes arranged in a grid of three rows and five columns. Each shape is drawn with blue outlines and translucent shading, and its name is printed underneath.*

* Cone with flat top
* Pentagonal pyramid with flat top
* Cone
* 4-sided pyramid
* Cube
* Rectangular box
* Tetrahedron
* Pyramid
* Pyramid with flat top
* Octahedron
* Pentagonal cone
* Irregular polyhedron
* Icosahedron
* Dodecahedron
* Half sphere

A speech bubble in the bottom right corner asks:
What if we had a **shape** class, what do we think we would include?

[source]

Links on this slide:
- <https://www.conceptdraw.com/examples/pyramid-geometrical-figures>

---

## Slide 68: Shapes have
- Area

---

## Slide 69: Shapes have

*Figure: A light blue gradient header bar at the top of the slide containing the title text.*

*   Area
*   Radius? Or height? Or Width?

---

## Slide 70: Shapes have

*Figure: A slide featuring a blue gradient header bar at the top containing the title text. The main body of the slide has a white background and displays a bulleted list.*

*   Area
*   Radius? Or height? Or Width?
*   Anything else?

---

## Slide 71: Shape class definition

### .h file

```cpp
class Shape {
public:
    virtual double area() const = 0;
};
```

*Figure: A callout box positioned to the right of the code snippet. It contains the following explanatory text:*
**Pure virtual function**: it is instantiated in the base class but overwritten in the subclass.
**(Dynamic Polymorphism)**

---

## Slide 72: Circle class definition

### .h file

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

*Annotation: A callout box with the text "Let’s break this down step by step" is positioned to the right of the constructor code.*

---

## Slide 73: Circle class definition

.h file

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

*Figure: A callout box with an arrow pointing to the line `class Circle : public Shape {` in the code. The callout reads: "Here we declare the **Circle** class which inherits from the **Shape** class".*

---

## Slide 74: Circle class definition

### .h file

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

*Figure: An orange arrow points from a text box to the line `virtual double area() const = 0;` in the `Shape` class definition. The text box contains the note: "This is a pure virtual function we declare in our base class, Shape."*

---

## Slide 75: Circle class definition

### .h file

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

*Figure: A callout box with the text "constructor using list initialization construction" has an orange arrow pointing to the line `Circle(double radius): _radius{radius} {};` in the `Circle` class definition.*

---

## Slide 76: Circle class definition

`.h file`

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

*Figure: A callout box with an arrow points to the `area()` function definition in the `Circle` class. The arrow originates from the right side and points left to the `area()` function. The box contains the annotation text: "Here we are overwriting the base class function `area()` for a circle".*

Lecture 07: Classes (2026Spring)

---

## Slide 77: Circle class definition

### .h file

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

*Figure: A callout box with an orange arrow pointing to the private member `double _radius;`. The text inside the box reads: "Another pro of inheritance is the **encapsulation** of class variables."*

---

## Slide 78: Rectangle class definition

### .h file

*Figure: A code snippet within a black border showing the definition of a base class `Shape` and a derived class `Rectangle`.*

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

---

## Slide 79: Shape subclass definitions

### .h file

*Figure: Two side-by-side boxes containing C++ class definitions. The left box defines the `Rectangle` class and the right box defines the `Circle` class, both inheriting from `Shape`. The class names "Rectangle" and "Circle" are highlighted in yellow.*

```cpp
class Rectangle: public Shape {
public:
// constructor
Rectangle(double h, double w):
    _height{h}, _width{w} {};
double area() const {
    return _width * _height;
}
private:
double _width, _height;
};
```

```cpp
class Circle : public Shape {
public:
// constructor
Circle(double radius):
    _radius{radius} {};
double area() const {
    return 3.14 * _radius * _radius;
}
private:
double _radius;
};
```

---

## Slide 80: What questions do we have?

What questions do we have?

*Figure: A close-up photograph of an ostrich's head and long neck against a blue sky with white clouds. The ostrich appears to be looking curiously at the camera.*

---

## Slide 81: Types of inheritance

| | |
| :--- | :--- |
| **Type** | public |
| **Example** | `class B: public A`<br>`{...}` |
| **Public Members** | Are public in the derived class |
| **Protected Members** | Protected in the derived class |
| **Private Members** | Not accessible in derived class |

---

## Slide 82: Types of inheritance

| Type | public | protected |
| :--- | :--- | :--- |
| **Example** | ```cpp class B: public A {...} ``` | ```cpp class B: protected A {...} ``` |
| **Public Members** | Are public in the derived class | Protected in the derived class |
| **Protected Members** | Protected in the derived class | Protected in the derived class |
| **Private Members** | Not accessible in derived class | Not accessible in derived class |

---

## Slide 83: Types of inheritance

| Type | public | protected | private |
| :--- | :--- | :--- | :--- |
| Example | `class B: public A {...}` | `class B: protected A {...}` | `class B: private A {...}` |
| Public Members | Are public in the derived class | Protected in the derived class | Privated in the derived class |
| Protected Members | Protected in the derived class | Protected in the derived class | Private in the derived class |
| Private Members | Not accessible in derived class | Not accessible in derived class | Not accessible in derived class |

---

## Slide 84: What questions do we have?
What questions do we have?

*Figure: A close-up photograph of an ostrich's head and neck against a blue sky with light clouds. The ostrich has its head tilted and its beak slightly open, giving it a curious or confused expression.*

---

## Slide 85: Vector

*Figure: A 3D animated cartoon character of a young boy with brown hair and black glasses, wearing an orange jumpsuit with a white collar. He is smiling and making a finger-gun gesture with both hands, pointing towards the right side of the slide.*

...

| Function | Description |
| --- | --- |
| `push_back` | adds an element to the end<br>(public member function) |
| `emplace_back` (C++11) | constructs an element in-place at the end<br>(public member function) |
| `append_range` (C++23) | adds a range of elements to the end<br>(public member function) |
| `pop_back` | removes the last element<br>(public member function) |

...

---

## Slide 86: Stack

*Figure: On the left, an image of a stack of colorful Prang construction paper sheets, arranged in a fan/stack pattern with various colors (black, blue, green, yellow, orange, red, pink, etc.) visible behind a Prang "Smart-Stack" medium weight construction paper package label.*

…

| Method | Description |
|---|---|
| **push** | inserts element at the top (public member function) |
| **push\_range** (C++23) | inserts a range of elements at the top (public member function) |
| **emplace** (C++11) | constructs element in-place at the top (public member function) |
| **pop** | removes the top element (public member function) |

…

---

## Slide 87: Pop Quiz: Which inheritance?

*Figure: A light blue gradient horizontal banner across the top of the slide containing the title text.*

```cpp
class MyStack : ________ MyVector {
    ...
};
```

---

## Slide 88: Pop Quiz: Which inheritance?

class MyStack : private MyVector {
    …
};

public
- Then the user could **insert**!!
protected
- This could work… but subclasses don’t need the vector.
private
- Nobody else needs access to or even awareness of the vector.

---

## Slide 89: Plan
1. Classes
2. Inheritance
3. **Virtuality**

---

## Slide 90: The Diamond Problem

Since both **B** and **C** inherit from **A**, they each call the constructor of **A**.

*Figure: A diamond-shaped inheritance diagram. A pink box labeled "**A**" is at the top. An arrow points from A down-left to a yellow box labeled "**B**", and another arrow points from A down-right to a green box labeled "**C**". Arrows from both B and C point down toward a blue box labeled "**D**" at the bottom center. A callout bubble points toward box D and contains the text: "**D** ends up with two copies of **A**. One from **B** another from **C**".*

---

## Slide 91: A,B,C,D classes

### .h file

*Figure: A diagram illustrating the inheritance hierarchy of four C++ classes (A, B, C, and D). Four boxes contain the class definitions. An arrow points from the box containing class A to the box containing class C. A second arrow points from class A to the box containing class B. An arrow points from the class C box to the box containing class D. A final arrow points from the class B box to the class D box.*

```cpp
class A {
public:
    A();
    void hello() {
        // print "hello from A"
    }
}
```

```cpp
class C : public A {
public:
    C();
}
```

```cpp
class B : public A {
public:
    B();
}
```

```cpp
class D
: public B, public C {
public:
    D();
}
```

---

## Slide 92: Which hello() does D call?

```cpp
D obj {};
obj.B::hello()
obj.C::hello()
obj.hello()
```

---

## Slide 93: Which hello() does D call?

*Figure: A code snippet box with a black border under the slide title. The title "Which hello() does D call?" is displayed in bold black text over a light blue gradient background at the top of the slide.*

```cpp
D obj {};

obj.B::hello()   // call B’s hello method

obj.C::hello()

obj.hello()
```

---

## Slide 94: Which hello() does D call?

*Figure: A white slide with a light blue header at the top containing the slide title. Below the header is a large white area containing a black rectangular border that encloses a C++ code snippet.*

```cpp
D obj {};
obj.B::hello()  // call B’s hello method
obj.C::hello() // call C’s hello method
obj.hello()
```

---

## Slide 95: Which hello() does D call?

*Figure: A code snippet inside a black-bordered box illustrating scope resolution and a method call ambiguity.*

```cpp
D obj {};

obj.B::hello()  // call B's hello method
obj.C::hello() // call C's hello method
obj.hello() // whose method do I call ???
```

---

## Slide 96: The Diamond Problem

The way to fix this is to make **B** and **C** inherit from **A** in a **virtual way**.

Virtual inheritance means that a derived class, in this case **D**, should only have a single instance of base classes, in this case **A**.

---

## Slide 97: Solution? Inherit Virtually!

### .h file

```cpp
class C : virtual public A {
public:
    C();
}
```

```cpp
class B : virtual public A {
public:
    B();
}
```

*Figure: Two code boxes side-by-side. The left box contains the definition for class C and the right box for class B, both inheriting virtually from class A. The keyword "virtual" is highlighted in yellow in both. Below these is a rounded rectangular callout box.*

This creates a shared instance of **A** between **B** and **C**!

---

## Slide 98: Fixed!

*Figure: A black-bordered box containing a C++ code snippet.*

```cpp
D obj {};

obj.B::hello()   // call B's hello method
obj.C::hello()   // call C's hello method
obj.hello()      // no longer ambiguous :)
```

---

## Slide 99: What virtual really means...

Virtual — Existing in essence, but not literally.

*Figure: A person wearing a VR headset and white athletic clothing stands on a circular platform in a natural landscape with mountains and a cloudy sky. The person is swinging a bat, hitting a virtual ball that appears to be shattering or exploding in mid-air.*

---

## Slide 100: What virtual really means...

In C++, virtual means to create a **virtual table (vtable)**.

### Goodbye to static typing :)
- Polymorphism with virtualism means we get dynamic typing.

*Figure: A diagram illustrating the structure of virtual tables. On the left, two boxes represent objects: "Class B" and "Class C", each containing a "vpointer". Arrows point from these vpointers to their respective vtables. The "Vtable of class B" contains entries "bar" and "quux", which point to "B::bar()" and "B::quux()". The "Vtable of class C" contains entries "bar" and "quux", where "bar" points to "C::bar()" and "quux" points to the "B::quux()" implementation.*

---

## Slide 101: Code Demo

*Figure: A rectangular box with a blue gradient background (light blue at the top, fading to a slightly darker blue at the bottom) and a thin black border. Inside the box, the text "Code Demo" is centered in a large, bold, black font.*

---

## Slide 102: Recap

1. Classes allow you to encapsulate functionality and data with access protections.
2. Inheritance allows us to design powerful and versatile abstractions that can help us model complex relationships in code.
3. These concepts are tricky – this lecture *really* highlights the power of C++.
