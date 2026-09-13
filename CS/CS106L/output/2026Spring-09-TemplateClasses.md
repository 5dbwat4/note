# Lecture 09: TemplateClasses (2026Spring)

> PDF title: 2026Spring-09-TemplateClasses.pptx
> Source: `assets/slides/2026Spring-09-TemplateClasses.pdf` · 100 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Welcome back! Link to Attendance Form ↓

*Figure: A QR code centered on the slide, intended to link to an attendance form.*

---

## Slide 2: Lecture 9: Template Classes

Lecture 9:
Template Classes

CS106L, Spring 2026
Preston Seay and Rachel Fernandez

---

## Slide 3: What are templates?

*Figure: A simple stick figure is shown on the left side of the slide. To the figure's upper right, there is a large orange speech bubble with the text "I need a way to store lists of integers!" To the figure's lower right, there is a smaller pink speech bubble with the text "I am on it!"*

---

## Slide 4: What are templates?

*Figure: A pink thought bubble with the text "I’ve done it!" next to an illustration of a computer monitor displaying a C++ class definition.*

```cpp
class IntVector {
// Code to store
// a list of
// integers…
};
```

---

## Slide 5: Recall: IntVector

*Figure: A code snippet for the `IntVector` class enclosed in a black box.*

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

---

## Slide 6: What are templates?

*Figure: A black stick figure with a happy face is shown on the left side of the slide. A large yellow speech bubble originating from the stick figure contains the text "Now I need to store a list of **doubles**!" where the word "**doubles**" is underlined. To the right of the stick figure is a smaller pink speech bubble containing the bold text "Right on it!"*

---

## Slide 7: What are templates?

*Figure: A pink thought bubble containing the text "I've done it!" is positioned on the left. To the right is an illustration of a laptop/monitor displaying a code snippet. The thought bubble and code illustration together depict a programmer who has written code for storing a list of doubles.*

```cpp
class DoubleVector {
    // Code to store
    // a list of
    // doubles…
};
```

---

## Slide 8: What are templates?

So could you give me a list of **STRINGS**...

*Figure: A humorous meme-style graphic. An orange cloud-shaped speech bubble contains the text "So could you give me a list of **STRINGS**...". To the right is a pink cloud-shaped thought bubble containing three emojis: a "mind blown" face (🤯) and two "angry" faces (😠). Below the orange bubble is a white box representing a mobile chat interface, containing a blue message bubble that says "thats kinda sus" and the word "Delivered" underneath. A small watermark at the bottom of the white box reads "Ken French".*

thats kinda sus
Delivered

---

## Slide 9: Not so fast…

---

## Slide 10: You realize you need to handle...

*Figure: Photograph of Alexander Stepanov (Creator of STL) wearing a black shirt with a red logo and a Russian flag pin. Below the photo: "Alexander Stepanov" and "Creator of STL".*  

- Vector of **doubles**?  
- Vector of **std::string**?  
- Vector of **vector of strings**?  
- Vector of **custom type I haven’t even thought of yet**?

---

## Slide 11: What if we could keep the logic, but change the type?

What if we could keep the logic, but change the type?

---

## Slide 12: What are templates?

*Figure: A diagram illustrating the concept of C++ templates. On the left, three overlapping boxes show three separate, specific class definitions: `IntVector`, `DoubleVector`, and `StringVector`. Each contains comments indicating it stores a list of a specific type. A large orange arrow points from these three boxes to a single, larger box on the right. This box contains a generic template class definition and examples of its use.*

```cpp
class IntVector {
    // Code to store
    // a list of
    // integers…
};

class DoubleVector {
    // Code to store
    // a list of
    // doubles…
};

class StringVector {
    // Code to store
    // a list of
    // strings…
};
```

```cpp
template <typename T>
class vector {
    // So satisfying.
};

vector<int> v1;
vector<double> v2;
vector<string> v3;
```

---

## Slide 13: std::vector\<T\>

std::vector\<T\>

*Figure: A black, curved arrow points from a white rectangular box with a drop shadow to the red text "std::vector\<T\>". The box contains the question: "How does this \<T\> stuff work?"*

How does this \<T\> stuff
work?

---

## Slide 14: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup sitting in an office, resting his chin on his hand as if thinking. Behind him are computer monitors and a poster or book cover with his name visible. The caption below the image reads "bjarne_about_to_raise_hand".*

---

## Slide 15: Today’s Agenda
• Template Classes
   • How can we generalize across different types?
• Const Correctness
   • Unlocking the power of const

---

## Slide 16: Announcements
* Assignment 1: SimpleEnroll was graded
    * See your feedback on paperless.stanford.edu .
* Assignment 3: Make a Class! is out
    * You should be able to complete it after today’s lecture.
    * Let us know if you have any questions.

Links on this slide:
- <http://paperless.stanford.edu>

---

## Slide 17: Template Classes

---

## Slide 18: Templates: A bit of history

*Figure: Three overlapping rectangular boxes with drop shadows, representing the definition of three similar C++ classes. The boxes are stacked diagonally from the top-left to the bottom-right. The back-most box shows the start of a class named `IntVector`, the middle box shows `DoubleVector`, and the front-most box shows `StringVector`. In each definition, the keyword `class` is colored red, the class names are colored purple, and the comment lines inside are colored light blue-grey.*

```cpp
class IntVector {
    // Code to store
    // a list of
    // integers…
};

class DoubleVector {
    // Code to store
    // a list of
    // doubles…
};

class StringVector {
    // Code to store
    // a list of
    // strings…
};
```

---

## Slide 19: Templates: A bit of history

*Figure: A code snippet showing the definition of a C++ class named `IntVector`, enclosed in a bordered box.*

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

---

## Slide 20: Templates: A bit of history

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

*Figure: A code block showing the definition of an `IntVector` class. The keyword `int` is highlighted in yellow in four places: in the class name `IntVector`, as the return type and in the parameter of `at()`, as a parameter type in `push_back()`, and as the pointer type in the `elems` member variable.*

---

## Slide 21: Templates: A bit of history

```cpp
#define GENERATE_VECTOR(MY_TYPE)
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

*Figure: A box containing a preprocessor macro definition for `GENERATE_VECTOR(MY_TYPE)` that demonstrates how C++ programs could create type-specific vector classes before templates existed. The macro uses `##` (token-pasting operator) to concatenate `MY_TYPE` with `Vector` to form class names. An arrow points from the macro definition to a callout box that reads "Preprocessor Macro / Runs before compiler," explaining that this text substitution happens before compilation.*

---

## Slide 22: Templates: A bit of history

*Figure: A code box showing a C preprocessor macro definition for generating a vector class. The macro parameter and all its usages (`MY_TYPE`) are highlighted in yellow. A thick black curved arrow points from a callout box on the right to the macro definition at the top. The callout box contains red text "Preprocessor Macro" and black text "Runs before compiler".*

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

**Preprocessor Macro**
Runs before compiler

---

## Slide 23: Templates: A bit of history

```cpp
#include "old_fashioned_template.h"

GENERATE_VECTOR(int)

intVector v1;
v1.push_back(5);
```

*Figure: A black arrow points from a callout box in the lower right corner to the `GENERATE_VECTOR(int)` line within the code block.*

**Code generation!!!**
Depending on what type we
pass in, we get a different
vector!

---

## Slide 24: Templates: A bit of history

```cpp
#include "old_fashioned_template.h"

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

**Code generation!!!**
Depending on what type we pass in, we get a different vector!

*Figure: A diagram featuring two rectangular boxes. The main box on the left contains the C++ code for the `intVector` class and its usage. A second callout box in the bottom right corner contains the "Code generation!!!" heading and explanatory text. A thick, curved black arrow points from the callout box back to the `class intVector` definition in the main code box.*

---

## Slide 25: Templates: A bit of history

```cpp
#include "old_fashioned_template.h"

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

*Figure: A code snippet showing an old-fashioned template approach for a vector class specialized for `int`. The word `int` is highlighted in yellow wherever it appears in the code — in the class name `intVector`, in the return type `int&`, in the parameter `const int&`, and in the pointer type `int*`. The file is included from `"old_fashioned_template.h"`. Below the class definition, example usage instantiates an `intVector` named `v1` and calls `push_back(5)` on it.*

---

## Slide 26: Problems with macros

*   Clunky syntax
*   Hard to type check
*   What if you forget to call macro?
    *   Or call it more than once?

*Figure: A meme image featuring computer scientists Bjarne Stroustrup (left) and Alex Stepanov (right). Alex Stepanov, who is seen clapping his hands, has a thought bubble pointing toward Bjarne that says "Bjarne, we can do better". Bjarne Stroustrup has a thought bubble pointing toward Alex that says "Yess Alex!!! YESSSSSS".*

---

## Slide 27: Key Idea: Templates automate code generation

---

## Slide 28: Templates have come a long way

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

*Figure: A code box containing the C++ template class `Vector`. Two annotation boxes with arrows point to different parts of the code. The top arrow points to the line `template <typename T>`. The annotation box contains the text: "Template Declaration", followed by "Vector is a template that takes in the name of a type T". The bottom arrow points to the body of the class, specifically near the `private` member declaration. This annotation box contains the text: "T gets replaced when Vector is instantiated". The code box and annotation boxes have drop shadows.*

---

## Slide 29: Template Instantiation

```cpp
Vector<int> intVec;
Vector<double> doubleVec;
Vector<std::string> strVec;

Vector<Vector<int>> vecVec;

struct MyCustomType {};
Vector<MyCustomType> structVec;
```

*Figure: A code box containing C++ code that demonstrates template instantiation with several examples of the `Vector` template instantiated with different types. A callout box overlaps the right side of the code box.*

> **Template Instantiation**
> Code for a specific type is generated on-demand, when you use it

---

## Slide 30: Template Instantiation

When you write code like this…
```cpp
template <typename T>
class Vector {
    T& at(size_t index);
    // More methods...
};

Vector<int> v;
```

Compiler produces code like this…
```cpp
class IntVector {
    int& at(size_t index);
    // More methods...
};

IntVector v;
```

---

## Slide 31: What questions do you have?

*Figure: A photograph of a person, likely Bjarne Stroustrup, sitting in an office environment. He is wearing glasses and a patterned shirt, with his hand near his face in a thoughtful pose. In the background, there are computer monitors and posters. One poster is clearly visible with the text "PROGRAMMING LANGUAGE BJARNE STROUSTRUP". Below the photograph, there is a caption.*

bjarne_about_to_raise_hand

What questions do you have?

---

## Slide 32: A template is like a factory

*Figure: An illustration of a factory building representing a C++ template. On the left side, two boxes labeled "int" and "string" have arrows pointing into the factory. On the right side, two boxes labeled "Vector<int>" and "Vector<string>" have arrows pointing away from the factory. At the bottom, a box contains the following template declaration:*

```cpp
template <typename T>
class Vector
```

---

## Slide 33: Templates vs. Types

*Figure: A diagram comparing templates and types. It features a 2x2 grid of boxes. The top-left box contains code defining a template. The top-right box contains code for a template instantiation. The bottom-left and bottom-right boxes contain text labeling the respective items above them.*

```cpp
template <typename T>
class Vector
```

`Vector<std::string>`

| | |
| :--- | :--- |
| ```cpp<br>template <typename T><br>class Vector<br>``` | `Vector<std::string>` |
| This is a template.<br>It’s **not** a type | This is a type.<br>A.K.A a template instantiation |

---

## Slide 34: Templates vs. Types

*Figure: A diagram illustrating the relationship between a template and a type. A central image of a factory building is shown. A text box labeled "The template" has an arrow pointing to the factory. A second text box labeled "The type" has an arrow pointing to a third box below it containing "Vector<string>". At the bottom, a code snippet is displayed.*

The template
Vector<string>
The type

```cpp
template <typename T>
class Vector
```

---

## Slide 35: What's the problem with this code?

*Figure: A white box containing a C++ code snippet. Below the box, there is a red "X" mark followed by an error message.*

```cpp
void foo(std::vector<int> v);

int main() {
    std::vector<double> v;
    foo(v);
}
```

❌ No suitable user-defined conversion from "std::vector<double>" to "std::vector<int>" exists

---

## Slide 36: Note: These are two distinct types

Vector\<double\>
Vector\<int\>

*Figure: A diagram with two boxes at the top labeled "Vector\<double\>" and "Vector\<int\>", with arrows pointing from a central box below to each of them. The central box contains the text: "These two instantiations (of the same template) are completely different (runtime and compile-time) types".*

Food for thought: compare this to a language like Java where an ArrayList\<int\> and ArrayList\<double\> share the same runtime type.

---

## Slide 37: Fun Fact: non-typename template parameters

*Figure: Three white rectangular boxes with a subtle drop shadow, arranged with one at the top center and two side-by-side below it. Each box contains a C++ code snippet illustrating different kinds of template parameters.*

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

---

## Slide 38: Fun Fact: non-typename template parameters

*Figure: A rectangular box containing a C++ code example of a template definition and instantiation.*

```cpp
template<typename T, std::size_t N>
struct std::array { /* ... */ };

// An array of exactly 5 strings
std::array<std::string, 5> arr;
```

Why use an `array` over `vector`? It avoids heap allocations.
The compiler will know exactly how much space an `array<string, 5>` takes (the size is baked into the type!), allowing it to be stack allocated

---

## Slide 39: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, the creator of C++, seated in his office. He is wearing glasses and a patterned shirt, looking directly at the camera with his hand resting on his chin. In the background, a monitor displays the cover of his book "Programming: Principles and Practice Using C++", and a poster on the wall is labeled "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP".*

bjarne_about_to_raise_hand

---

## Slide 40: 👻 A few template quirks 👻

---

## Slide 41: Template Syntax in .cpp

(1) Must copy template <...> syntax in .cpp

---

## Slide 42: Template class implementation

When implementing a template, you might try something like this

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

*Figure: Two code boxes side-by-side. The left box contains code for Vector.h and the right box contains code for Vector.cpp. A curved black arrow points from a speech bubble at the bottom to the return type `T&` in the function signature `T& Vector::at(size_t i)`. The speech bubble contains the text: Compiler: “I don’t know what T is!”*

---

## Slide 43: Template class implementation

When implementing a template, must copy over template declaration

```cpp
// Vector.cpp

template <typename T>
T& Vector::at(size_t i) {
    // Implementation...
}
```

Does anyone still see a problem with this?

---

## Slide 44: Template class implementation

Vector is not a type, but Vector<T> is

*Figure: A bordered box displays a C++ code snippet. The code is syntax-highlighted with keywords in red, types in purple, and a comment in gray. The function signature `T& Vector<T>::at(size_t i)` is shown, with `Vector<T>` highlighted in yellow. A smaller speech-bubble-like box is positioned in the bottom-right corner of the code box.*

```cpp
// Vector.cpp

template <typename T>
T& Vector<T>::at(size_t i) {
    // Implementation...
}
```

*Figure: A speech-bubble-like box in the bottom-right corner of the code box contains a compiler's reaction. The text reads: "Compiler: “Ahh.. I’m happy now 😌😌”" with "Compiler:" in red and the rest in black, including two relaxed face emojis.*

---

## Slide 45: Include Directive Requirement

(2) .h must include .cpp at bottom of file

---

## Slide 46: Normal class implementation

For non-template classes, the .cpp file includes the .h file

*Figure: Two side-by-side code snippets showing the declaration and implementation of a non-template C++ class. The left box contains the header file `StrVector.h`, and the right box contains the source file `StrVector.cpp`. In the right box, the line `#include "StrVector.h"` is highlighted in yellow.*

**Left box content:**
```cpp
// StrVector.h

class StrVector {
public:
    string& at(size_t i);
};
```

**Right box content:**
```cpp
// StrVector.cpp

#include "StrVector.h"

string& StrVector::at(size_t i)
{
    // Implementation...
}
```

---

## Slide 47: Template class implementation

For template classes, the `.h` file includes the `.cpp` file

*Figure: Two side-by-side boxes containing C++ code snippets. The left box displays a header file (`Vector.h`) and the right box displays an implementation file (`Vector.cpp`). In the left box, the `#include "Vector.cpp"` line is highlighted with a yellow background.*

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

---

## Slide 48: That’s pretty weird 🤨 Why?

*   Template `.h` must include `.cpp` due to the way template code generation is implemented in the compiler (and linker)
*   Don’t worry too much about the *why* (unless you’re curious!)
*   There are ways to get around this (ask us after!)

---

## Slide 49: Typename and Class Equivalence
(3) typename is the same as class

---

## Slide 50: (3) typename is the same as class

*Figure: A rectangular box with a shadow containing a C++ template class declaration using the `typename` keyword.*

```cpp
template <typename T>
class Vector{};
```

*Figure: A rectangular box with a shadow containing a C++ template class declaration using the `class` keyword.*

```cpp
template <class T>
class Vector{};
```

---

## Slide 51: (3) `typename` is the same as `class`

All of the following are identical:

*Figure: Four boxes arranged in a 2x2 grid, each containing a two-line C++ template declaration. The boxes are arranged as follows: top-left, top-right, bottom-left, bottom-right.*

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
template <class K, typename V>
struct pair;
```

---

## Slide 52: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, the creator of C++, looking thoughtfully at the camera with his hand near his chin. He is wearing glasses and a patterned shirt. Behind him, a poster is visible with the text "PROGRAMMING LANGUAGE BJARNE STROUSTRUP".*

bjarne\_about\_to\_raise\_hand

What questions do you have?

---

## Slide 53: Let’s implement Vector<T>

Let’s implement **Vector<T>**

*Figure: The phrase "Let’s implement" is in black text. The phrase "Vector<T>" is in red text.*

---

## Slide 54: Coding Together

Let’s code this together 👫

*Figure: A simple slide with large text "Let’s code this together" and an emoji showing two stylized human figures holding hands, one in a purple shirt and one in a green shirt. Below the main text is a red-colored URL.*

106l.vercel.app/templates

---

## Slide 55: What questions do you have?

bjarne_about_to_raise_hand

*Figure: A centered photograph of Bjarne Stroustrup resting his chin on his hand in a thoughtful pose. In the background of the photo, book covers for "The C++ Programming Language" and "Programming: Principles and Practice Using C++" are visible.*

---

## Slide 56: Const Correctness

---

## Slide 57: Let’s use our Vector class!

*Figure: A C++ code snippet is shown inside a rectangular frame. A thick, black curved arrow points from the `v.size()` call in the code's `for` loop to a white text box with a shadow. The text box contains a compiler error message.*

```cpp
void printVec(const Vector<int>& v) {
  for (size_t i = 0; i < v.size(); i++) {
    std::cout << v.at(i) << " ";
  }
  std::cout << std::endl;
}
```

Compiler: “No such method size!”

---

## Slide 58: Huh? But there is a method called size

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

*Figure: A meme featuring a white cat with its head tilted and a skeptical expression. Below the cat, the word "HUH" is written in capital letters.*

---

## Slide 59: What is the problem?

```cpp
void printVec(const Vector<int>& v) {
    for (size_t i = 0; i < v.size(); i++) {
        std::cout << v.at(i) << " ";
    }
    std::cout << std::endl;
}
```

*Figure: A code snippet inside a bordered box. Specific parts of the code are highlighted in yellow: the parameter `const Vector<int>& v`, the call `v.size()`, and the call `v.at(i)`.*

*   By passing `v` as `const`, we promise not to modify `v`
*   Compiler cannot be sure if methods like `size` and `at` will modify `v`
*   Remember, member functions *can* access member variables

---

## Slide 60: How do we fix it?

*Figure: A diagram illustrating the use of `const` methods. On the left is a C++ code snippet showing a `Vector` class template. On the right is a speech bubble from the `const` methods, with arrows pointing from the highlighted `const` keywords in the code to the speech bubble.*

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

### const method:
"Dear compiler,

I promise not to modify this object inside of this method. Please hold me accountable.

Love, Preston <3"

---

## Slide 61: How do we fix it (.cpp file)?

```cpp
template <class T>
size_t Vector<T>::size() const {
    return logical_size;
}

// Other methods...
```

Make sure to also add **const** to the implementation, or the compiler will scream

---

## Slide 62: How do we fix it (.cpp file)?

```cpp
template <class T>
size_t Vector<T>::size() const {
    this->logical_size = 106; // 😈😈😈
    return logical_size;
}

// error: cannot assign to non-static data member
// within const member function 'size'
```

*Figure: An inset text box with a white background and a thin black border, positioned in the lower-right area of the code block.*

Inside a const method, this
has type const Vector\<T\>*

---

## Slide 63: What is this?

*Figure: Diagram illustrating the implicit `this` pointer in two different contexts. On the left, a code box for `Point::setX` is shown with an arrow pointing from a label box below it that reads `Point* this`. On the right, a code box for a `const` member function `Point::getX` is shown with an arrow pointing from a label box below it that reads `const Point* this`. The word `this` is highlighted in blue, `Point` is in purple, and the keyword `const` is highlighted with a yellow background.*

**Left Code Box:**
```cpp
void Point::setX(int x)
{
    this->x = x;
}
```
**Bottom Label:**
Point* this

**Right Code Box:**
```cpp
int Point::getX(int x)
const
{
    return this->x;
}
```
**Bottom Label:**
const Point* this

---

## Slide 64: The const interface
- Objects marked as **const** can only make use of the **const interface**
- The **const** interface are the functions that are **const** in an object

---

## Slide 65: The <span style="color: red">const</span> interface

*Figure: Two side-by-side boxes with black borders and drop shadows, each containing a C++ code snippet for a `Vector` class template. Below the left box is the label `Vector<T>` in purple. Below the right box is the label `const Vector<T>` where the word "const" is in red and `Vector<T>` is in purple. In the right box's code, the line `void push_back(const T& elem);` is crossed out with a red strike-through line, and the `const` keywords in the `private` member declarations are highlighted with a yellow background.*

**Vector\<T\>**
```cpp
template<class T>
class Vector {
public:
    size_t size() const;
    bool empty() const;
    void push_back(const T& elem);
private:
    size_t logical_size;
    T* elems;
};
```

**<span style="color: red">const</span> Vector\<T\>**
```cpp
template<class T>
class Vector {
public:
    size_t size() const;
    bool empty() const;
    <del>void push_back(const T& elem);</del>
private:
    <mark>const</mark> size_t logical_size;
    <mark>const</mark> T* elems;
};
```

---

## Slide 66: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, a man with glasses and a patterned shirt, sitting with his chin resting on his hand. In the background, a monitor and a poster are visible. The poster appears to have his name on it.*

`bjarne_about_to_raise_hand`

---

## Slide 67: Back to our Vector class!

```cpp
void printVec(const Vector<int>& v) {
    for (size_t i = 0; i < v.size(); i++) {
        std::cout << v.at(i) << " ";
    }
    std::cout << std::endl;
}
```

*Figure: The slide contains a code snippet for a function `printVec`. In the title, the word "Vector" is colored purple. Within the code block, the method calls `v.size()` and `v.at(i)` are highlighted in yellow. Below the code, a bordered box displays a message from the compiler: "Compiler: “🦁 const Vector<int> has no size, at!!!”". In this message, the words "size, at!!!" are colored purple.*

---

## Slide 68: Back to our Vector class!

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

*Figure: A callout box contains the text: "Let’s add **const** to the methods which don’t modify **Vector**".*

---

## Slide 69: Back to our Vector class!

*Figure: A slide showing a C++ code snippet for a Vector class template. The code has some `const` keywords highlighted in yellow. A text box to the right provides an instruction.*

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

Let’s add **const** to the methods which don’t modify **Vector**

---

## Slide 70: Back to our Vector class!

```cpp
void printVec(const Vector<int>& v) {
    for (size_t i = 0; i < v.size(); i++) {
        std::cout << v.at(i) << " ";
    }
    std::cout << std::endl;
}
```

*Figure: A box containing the C++ function `printVec`. The function takes a `const` reference to a `Vector<int>`, iterates from index 0 to `v.size() - 1` using a `for` loop, and prints each element accessed via `v.at(i)` followed by a space. After the loop, it prints a newline. In the code, the method calls `v.size()` and `v.at(i)` are highlighted in yellow.*

*Figure: A smaller box with a message from the compiler. It reads: "Compiler: “✅ Everything looks good to me!”". The word "Compiler" is in red, followed by a green checkmark emoji and the quoted text in black.*

---

## Slide 71: Back to our Vector class!

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

There’s at least **one (or maybe two)** problems with how this method is declared.

Turn to a partner and take 60s to talk about why!

*Figure: A black arrow points from the text box on the right toward the line of code `T& at(size_t index) const;` within the class declaration.*

---

## Slide 72: Problem #1: const consumers can modify!
Since we return a **non-const reference**, we can assign to it!

```cpp
T& at(size_t index) const;

void oops(const Vector<int>& v) {
    v.at(0) = 42;
}
```

*Figure: A code snippet showing a function declaration `T& at(size_t index) const;` and a function `void oops(const Vector<int>& v) { v.at(0) = 42; }`. A text box points to the code, stating: "Remember, since **v** is const, we shouldn't be able to modify it".*

---

## Slide 73: Solution: return a const reference

*Figure: A slide with a bordered box containing a C++ code snippet for a template class `Vector`. To the right, overlapping the code box, there is a text annotation box with the text "Hmm... There's still a problem here".*

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

---

## Slide 74: Problem #2: non-const consumers can't modify!
If we return a const reference, now we cannot update elements!

```cpp
const T& at(size_t index) const;

void ooh(Vector<int>& v) {
    v.at(0) = 42;
}
```

*Figure: A white rectangular box with a drop shadow containing a red 'X' icon and the error message: "Can't assign to const int&".*

---

## Slide 75: Solution: const overloading!

*   Let’s define two versions of our `at` method
*   One version gets called for `const` instances
*   ...And another that gets called for non-`const` instances

*Figure: A code snippet enclosed in a white rectangular box with a black border and a drop shadow, illustrating the template class definition.*
```cpp
template<class T>
class Vector {
public:
    const T& at(size_t index) const;
    T& at(size_t index);
...
};
```

---

## Slide 76: Solution: const overloading (.cpp file)!

*Figure: A code block showing two versions of the `at` method for a `Vector` class template, illustrating const overloading. The first version is const-qualified and returns a `const` reference. The second version is non-const and returns a mutable reference.*

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

---

## Slide 77: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, creator of C++, wearing glasses and a patterned sweater, with his right hand resting under his chin. In the background, a poster with the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP" is visible. The image is overlaid with the question text.*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 78: Solution: const overloading (.cpp file)!

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

*Figure: A callout box positioned to the right of the code block containing the following note:*

Two methods with the same implementation.
It’s a bit redundant, but it’s only one line

---

## Slide 79: What if we added a findElement?
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

---

## Slide 80: Implementing findElement

*Figure: A white rectangular box with a black border and a drop shadow, containing a C++ code snippet and a comment.*

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

---

## Slide 81: Implementing findElement

*Figure: A slide titled "Implementing findElement" showing two versions of a C++ template function `findElement` for a `Vector` class. The first version returns a non-const reference, and the second is marked `const` and returns a const reference. A callout box on the right contains a comment regarding the redundancy of the two implementations.*

```cpp
template <typename T>
T& Vector<T>::findElement(const T& value) {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == elem) return elems[i];
    }
    throw std::out_of_range("Element not found");
}

template <typename T>
const T& Vector<T>::findElement(const T& value) const {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == elem) return elems[i];
    }
    throw std::out_of_range("Element not found");
}
```

This works, but it’s super redundant. There must be a better way!

---

## Slide 82: A slight (but useful) aside

* Casting: the process of converting one type to another
* There are *many* ways to cast in C++
* `const_cast` allows us to “cast away” the `const`-ness of a variable
* Usage: `const_cast<target_type>(expression)`
* So why is this useful?

---

## Slide 83: Implementing findElement

```cpp
template <typename T>
T& Vector<T>::findElement(const T& value) {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == elem) return elems[i];
    }
    throw std::out_of_range("Element not found");
}
```
non-const vec

```cpp
template <typename T>
const T& Vector<T>::findElement(const T& value) const {
    return const_cast<Vector<T>&>(*this).findElement(value);
}
```
const-vec

---

## Slide 84: Implementing findElement

```cpp
template <typename T>
T& Vector<T>::findElement(const T& value) {
    for (size_t i = 0; i < logical_size; i++) {
        if (elems[i] == elem) return elems[i];
    }
    throw std::out_of_range("Element not found");
}

template <typename T>
const T& Vector<T>::findElement(const T& value) const {
    return const_cast<Vector<T>&>(*this).findElement(value);
}
```

*Figure: A slide showing two implementations of the `findElement` member function template for a `Vector` class. A comment box overlaps part of the first function, containing the text "Ahh no more redundancy… But what in the Bjarne is going on here?". The line `return const_cast<Vector<T>&>(*this).findElement(value);` in the second, `const`-qualified function is highlighted in yellow.*

---

## Slide 85: const_cast usage

```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

---

## Slide 86: const_cast Usage Example

*Figure: A white callout box with a black border containing text. A black arrow points from the bottom-right corner of the box down toward a line of code below.*

**const\_cast casts away the const**

```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

---

## Slide 87: C++ const\_cast Expression

*Figure: A diagram explaining the structure and evaluation of a C++ expression. The expression `const_cast<Vector<T>&>(*this).findElement(value);` is centered on a white background with specific color coding: `const_cast` is red, `<Vector<T>&>` is purple, `(*this)` is blue with an underline, `.findElement` is purple, and `(value)` is orange. Three white callout boxes with drop shadows and thick black arrows provide annotations for specific parts of the code:*
*   *A top-left box points to the `const_cast` keyword and contains the text: "const\_cast casts away the const". In this box, "const\_cast" and "const" are red.*
*   *A top-right box points to the `(*this)` expression and contains the text: "*this dereferences a const Vector<T>*, giving us a const-ref". In this box, "*this" and "const" are red, and "Vector<T>*" is purple.*
*   *A bottom box points to the `(*this)` expression and contains the text: "const Vector<T>&". In this box, "const" is red and "Vector<T>&" is purple.*

```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

---

## Slide 88: const_cast with Templates

```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

*Figure: A code snippet with three annotation boxes pointing to specific parts. An arrow from a box reading "const_cast casts away the const" points to the `const_cast` part of the code. An arrow from a box reading "*this dereferences a const Vector<T>*, giving us a const-ref" points to the `*this` part. An arrow from a box reading "Vector<T>& is a non-const reference, the type we would like" points to the `Vector<T>&` template argument.*

---

## Slide 89: const_cast Diagram
```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

*Figure: A diagram with four annotation boxes pointing to different parts of the C++ code line above via arrows. The boxes contain the following text:*

*   **Top-left box** points to `const_cast`: const\_cast casts away the const
*   **Top-right box** points to `*this`: \*this dereferences a const Vector\<T\>\*, giving us a const-ref
*   **Bottom-left box** points to `<Vector<T>&>`: Vector\<T\>& is a **non-const** reference, the type we would like
*   **Bottom-right box** points to `.findElement`: Phew... This is the non-const version of findElement

---

## Slide 90: `const_cast` with `findElement`

```cpp
const_cast<Vector<T>&>(*this).findElement(value);
```

*Figure: A diagram showing a single line of C++ code with four annotation boxes and arrows pointing to the relevant parts of the code.*

- **Top-left annotation** (arrow pointing to `const_cast`):
  - `const_cast` casts away the const

- **Top-right annotation** (arrow pointing to `*this`):
  - `*this` dereferences a const `Vector<T>*`, giving us a const-ref

- **Bottom-left annotation** (arrow pointing to `Vector<T>&`):
  - `Vector<T>&` is a non-const reference, the type we would like

- **Bottom-right annotation** (arrow pointing to `findElement`):
  - Phew... This is the non-const version of `findElement`

---

## Slide 91: const_cast forces compiler to pick right overload
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
*Figure: A code snippet showing a template class `Vector` with two pairs of overloaded member functions (`at` and `findElement`). The first declaration of `findElement` (`T& findElement(const T& value);`) is highlighted in yellow.*

---

## Slide 92: Implementing findElement

*Figure: Two C++ code snippets presented inside a white rectangular box with a drop shadow. The first snippet implements a non-const version of a `findElement` function. The second snippet implements a `const` version that delegates to the first using a `const_cast`. The single line in the second function's body is highlighted with a yellow background.*

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

---

## Slide 93: When to use const_cast?
- Short answer: just about never
- const_cast tells the compiler: “don’t worry I’ve got this”
- If you need a mutable value, just don’t add const in the first place
- Valid uses of const_cast are few and far between

---

## Slide 94: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup sitting at a desk, with his hand resting near his chin. Behind him are computer monitors and posters, one of which reads "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP".*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 95: const_cast mutability
**const\_cast** makes an ***entire*** object mutable

**Is there anything more fine-grained?**

---

## Slide 96: A C++ party trick: mutable keyword

Like `const_cast`, `mutable` circumvents const protections. Use it carefully!

*Figure: A code example demonstrating the `mutable` keyword. The code is shown within a bordered box and defines a struct `MutableStruct` with two members: a regular `int` and a `mutable double`. A `const` instance of the struct is created. The code shows that modifying the non-mutable member is forbidden (marked with a red cross), while modifying the `mutable` member is allowed (marked with a green checkmark).*

```cpp
struct MutableStruct {
    int dontTouchThis;
    mutable double iCanChange;
};

const MutableStruct cm;
// cm.dontTouchThis = 42; // ❌ Not allowed, cm is const
cm.iCanChange = 3.14;       // ✅ Ok, iCanChange is mutable
```

---

## Slide 97: mutable example: storing debug info

```cpp
struct CameraRay {
    Point origin;
    Direction direction;
    mutable Color debugColor;
}

void renderRay(const CameraRay& ray) {
    ray.debugColor = Color.Yellow; // Show debug ray
    /* Rendering logic goes here ... */
}
```

*Figure: A screenshot from a video game (Overwatch) showing a character (Pharah) with a yellow debug ray line extending from her shoulder area towards a robotic target in a desert-like environment. The ray illustrates how debug information can be attached to a const object.*

---

## Slide 98: Recap
Recap

---

## Slide 99: What We Covered

*   Template Classes
    *   Template classes generalize logic across types!
*   Const Correctness
    *   const makes an entire object read-only
    *   Mark methods const when they don’t modify the object
    *   const_cast and mutable can circumvent compiler in *rare* cases!

---

## Slide 100: Next Time: Template Functions

**Next Time: Template Functions**

Unlocking the power of templates
