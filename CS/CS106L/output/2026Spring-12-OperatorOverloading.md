# Lecture 12: OperatorOverloading (2026Spring)

> PDF title: 2026Spring-12-OperatorOverloading
> Source: `assets/slides/2026Spring-12-OperatorOverloading.pdf` · 72 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Operator Overloading
Lecture 12:
**Operator Overloading**

Stanford CS106L, Spring 2026
Rachel Fernandez & Preston Seay

---

## Slide 2: Attendance

Attendance

*Figure: A black and white QR code centered on the slide below the title. It is a square matrix barcode with finder patterns in three corners.*

[page 2 of 72]

---

## Slide 3: Today's Agenda

*Figure: A horizontal green gradient banner at the top of the slide containing the main heading "Today's Agenda" in a large, bold, black sans-serif font, centered horizontally.*

1. Recap
2. Operator Overloading

---

## Slide 4: Today's Agenda

1. **Recap**
2. Operator Overloading

---

## Slide 5: Functors
*Figure: A diagram with a beige background containing four rectangular boxes arranged in a 2x2 grid. The top-left box is gray, the top-right box is gray, the bottom-left box is blue, and the bottom-right box is gray. Each box contains a bold title and a question in a different font.*

- **Containers**
  *How do we store groups of things?*
- **Iterators**
  *How do we traverse containers?*
- **Functors**
  *How can we represent functions as objects?*
- **Algorithms**
  *How do we transform and modify containers in a generic way?*

---

## Slide 6: Functors

### Lambda Syntax

*Figure: A diagram explaining the syntax of a C++ lambda expression. An example code snippet is at the center, with four annotation boxes connected by arrows to different parts of the code.*

```cpp
auto lessThanN = [n] (int x) {
    return x < n;
};
```

*   An arrow points from a box to the `auto` keyword. The box contains the text: "I don't know the type! But the compiler does."
*   An arrow points from a box to the capture clause `[n]`. The box contains the text: "**Capture clause** lets us use outside variables"
*   An arrow points from a box to the parameter list `(int x)`. The box contains the text: "**Parameters** Function parameters, exactly like a normal function"
*   An arrow points from a box to the function body `{ return x < n; }`. The box contains the text: "**Function body** Exactly as a normal function, except only parameters and captures are in-scope"

---

## Slide 7: Algorithms

*Figure: A diagram showing the four main components of the STL (Standard Template Library) arranged in a 2x2 grid within a large, dashed-border rectangular container with a light orange background.*

*   **Containers**
    How do we store groups of things?
*   **Iterators**
    How do we traverse containers?
*   **Functors**
    How can we represent functions as objects?
*   **Algorithms** (highlighted in a blue box)
    How do we transform and modify containers in a generic way?

---

## Slide 8: Ranges and Views

**We can chain views together use `operator` |**

```cpp
std::vector<char> letters = {'a', 'b', 'c', 'd', 'e'};
std::vector<char> upperVowel = letters
    | std::ranges::views::filter(isVowel)
    | std::ranges::views::transform(toupper)
    | std::ranges::to<std::vector<char>>();

// upperVowel = { 'A', 'E' }
```

---

## Slide 9: It’s week 6!

*Figure: Screenshot of the C++ reference website showing the main library index page, with several section headings highlighted by black boxes: "Concepts library (C++20)", "Iterators library", "Algorithms library", "Containers library", and "Input/output library".*

**C++ reference**
C++11, C++14, C++17, C++20, C++23, C++26 | Compiler support C++11, C++14, C++17, C++20, C++23, C++26

- **Language**
    - Keywords – Preprocessor
    - ASCII chart
    - Basic concepts
        - Comments
        - Identifiers (lookup)
        - Types (fundamental types)
        - The main function
    - Expressions
        - Value categories
        - Evaluation order
        - Operators (precedence)
        - Conversions – Literals
    - Statements
        - if - switch
        - for, range for (C++11)
        - while - do-while
    - Declarations
        - Initialization
    - Functions (overloading)
    - Classes
    - Namespaces
    - Templates – Exceptions
    - Freestanding implementations
- **Standard library (headers)**
- **Named requirements**
- **Feature test macros (C++20)**
    - Language – Standard library
- **Language support library**
    - Program utilities
    - Signals – Non-local jumps
    - Basic memory management
    - Variadic functions
    - Initializer list (C++11)
    - source_location (C++20)
    - Coroutine support (C++20)
    - Comparison utilities (C++20)
    - Type support
        - numeric_limits – exception
        - type_info – type_index (C++11)
- **Concepts library (C++20)**
- **Diagnostics library**
    - Assertions – System error (C++11)
    - Exception types – Error numbers
    - basic_stacktrace (C++23)
    - Stacktrace (C++23)
- **Memory management library**
    - Allocators – Smart pointers
    - Memory resources (C++17)
- **Metaprogramming library (C++11)**
    - Type traits – Type sequences
    - Integer sequence (C++14)
- **General utilities library**
    - Function objects – hash (C++11)
    - Smart pointer – swap (C++11)
    - Integer comparison (C++20)
    - pair – tuple (C++11)
    - optional (C++17)
    - expected (C++23)
    - variant (C++17) – any (C++17)
    - bitset – Bit manipulation (C++20)
- **Containers library**
    - Sequence containers (C++11)
        - list – forward_list (C++11)
        - array (C++11) – deque
        - vector – string
    - Associative containers
        - set – multiset
        - map – multimap (C++11)
        - unordered_set (C++11)
        - unordered_multiset (C++11)
        - unordered_map (C++11)
        - unordered_multimap (C++11)
        - Container adaptors
        - Flat containers (C++23)
- **Iterators library**
- **Ranges library (C++20)**
    - Range factories – Range adaptors
- **Algorithms library**
    - Numeric algorithms
    - Execution policies (C++17)
    - Constrained algorithms (C++20)
- **Strings library**
    - basic_string – char_traits
    - basic_string_view (C++17)
    - Null-terminated strings
    - String literals – string_view
- **Text processing library**
    - Primitive numeric conversions (C++17)
    - Formatting (C++20)
    - Character handling and classification
    - text_encoding (C++26)
    - Regular expressions (C++11)
        - basic_regex – Algorithms
        - Defining a regular expression grammar
- **Numerics library**
    - Common math functions
    - Mathematical special functions (C++17)
    - Mathematical constants (C++20)
    - Basic linear algebra algorithms (C++26)
    - Pseudo-random number generation
    - Floating-point environment (C++11)
    - Complex numbers
- **Date and time library**
    - C-style – Calendars – Time zone (C++20)
- **Input/output library**
    - Stream-based I/O / I/O manipulators
    - basic_istream – basic_ostream
    - Synchronized output (C++20)
    - std::format (C++20)
- **Concurrency support library (C++11)**
    - thread – jthread (C++20)
    - atomic – atomic_flag
    - Memory ordering – Memory_order
    - Mutual exclusion – Semaphores (C++20)
    - Condition variables – Futures
    - latch (C++20) – barrier (C++20)
    - Safe Reclamation (C++26)
- **Execution support library (C++26)**
- **Technical specifications**
    - Standard library extensions (library fundamentals TS)
        - resource_adaptor – invocation_type
    - Standard library extensions v2 (library fundamentals TS v2)
        - polymorphic_allocator – invariant – randint
        - observer_ptr – Detection idiom
    - Standard library extensions v3 (library fundamentals TS v3)
        - scope_exit – scope_fail – scope_success – unique_resource
- **Parallelism library extensions v2 (parallelism TS v2)**
    - SIMD
- **Concurrency library extensions (concurrency TS)**
- **Transactional Memory (TM TS)**
- **Reflection (reflection TS)**

External Links – Non-ANSI/ISO Libraries – Index – std Symbol Index

---

## Slide 10: We’ve made it really far

*Figure: A course schedule table with three columns: Week, Tuesday, and Thursday. The table lists weeks 1 through 6 with dates and lesson topics. Each cell includes links to Slides and Code where applicable. Assignment badges are shown in red (A1: SimpleEnroll, A2: Marriage Pact, A3: Make a Class!, A4: Isperl). The cell for Week 6, Thursday (May 7, "12. Operator Overloading") is highlighted with an orange border.*

| Week | Tuesday | Thursday |
| --- | --- | --- |
| 1 | March 31<br>1. Welcome!<br>Slides<br>Policies | April 2<br>2. Types & Structs<br>Slides<br>Code |
| 2 | April 7<br>3. Initialization & References<br>Slides | April 9<br>4. Streams<br>Slides<br>Code<br>A1: SimpleEnroll |
| 3 | April 14<br>5. Containers<br>Slides<br>Code | April 16<br>6. Iterators & Pointers<br>Slides<br>Code<br>A2: Marriage Pact |
| 4 | April 21<br>7. Classes<br>Slides<br>Code | April 23<br>8. Optional: Inheritance Practice<br>Slides<br>Code<br>A3: Make a Class! |
| 5 | April 28<br>9. Class Templates & Const Correctness<br>Slides<br>Code | April 30<br>10. Function Templates<br>Slides<br>Code<br>A4: Isperl |
| 6 | May 5<br>11. Functions & Lambdas<br>Slides | May 7<br>12. Operator Overloading |

---

## Slide 11: What questions do we have?

What questions do we have?

*Figure: A large green parrot is positioned in the center of the slide, looking to the right. Surrounding it are three white 3D figures, each paired with a large red 3D question mark. One figure on the left is leaning against a question mark, one figure in the upper right is standing behind a question mark, and one figure in the lower right is sitting against a question mark.*

---

## Slide 12: Today's Agenda

1. Recap
2. Operator Overloading

---

## Slide 13: [n]: So what have we seen so far

At this point:
1. You know how to create classes!
2. You know to to create templated classes!
3. But.....
4. Remember maps and sets?

In particular recall that a std: :map<K ,V> requires K to have an operator

---

## Slide 14: Why this requirement?

In particular recall that a `std::map<K ,V>` requires `K` to have an `operator<`

*Figure: A diagram titled "What is map["Alex"]?" illustrating the lookup process in a binary search tree. The tree contains nodes: root "CS106L" (42), left child "Chris" (31), right child "Nick" (51). Under "Chris", there is a left child "Alex" (0) inside a dashed box and a right child "Keith" (14). Under "Nick", there is a right child "Sean" (35). The diagram includes comparison steps: `"Alex" < "CS106L" ?` with a yellow highlighted result `Yes! Go left`, and `"Alex" < "Chris" ?` with a yellow highlighted result `Yes! Go left... wait`. A label "Lookups!" with an arrow points to the first comparison, and a dashed arrow points from the "Chris" node to the dashed "Alex" node.*

```
Lookups!
"Alex" < "CS106L" ?  -->  Yes! Go left
"CS106L" 42
       /
"Alex" < "Chris" ?  -->  Yes! Go left... wait
  "Chris" 31     "Nick" 51
  /     \           \
"Alex"  "Keith" 14   "Sean" 35
   0
```

---

## Slide 15: Motivation
Why should we use operators at all?

“Operators allow you to convey meaning about types that functions don’t”

From this this phenomenal cppcon video

Links on this slide:
- <https://www.youtube.com/watch?v=zh4EgO13Etg>

---

## Slide 16: Motivation
Why should we use operators at all?

“Operators allow you to convey meaning about types that functions don’t”

*Figure: A screenshot of a code editor showing a C++ class definition for `Money`.*

```cpp
class Money {
public:
    int cents;
    Money(int c) : cents(c) {}
};
```

---

## Slide 17: Motivation

Why should we use operators at all?

**“Operators allow you to convey meaning about types that functions don’t”**

```cpp
class Money {
public:
    int cents;
    Money(int c) : cents(c) {}
};
```

```cpp
Money add(const Money& a, const Money& b) {
    return Money(a.cents + b.cents);
}

Money total = add(Money(100), Money(50));  // 100 + 50 = 150
```

Feels like a random function call.. Not really addition

---

## Slide 18: Motivation

Why should we use operators at all?

**“Operators allow you to convey meaning about types that functions don’t”**

*Figure: Screenshot of a C++ class definition for `Money` in a code editor, showing line numbers 1 through 6.*
```cpp
class Money {
public:
    int cents;
    Money(int c) : cents(c) {}
};
```

*Figure: Screenshot of a C++ function implementation and usage example for `Money`, showing line numbers 7 through 11.*
```cpp
Money add(const Money& a, const Money& b) {
    return Money(a.cents + b.cents);
}

Money total = add(Money(100), Money(50)); // 100 + 50 = 150
```

*Figure: Screenshot of a C++ operator overload implementation and usage example for `Money`, showing line numbers 13 through 17.*
```cpp
Money operator+(const Money& a, const Money& b) {
    return Money(a.cents + b.cents);
}

Money total = Money(100) + Money(50);
```

From this phenomenal cppcon video

Now I understand! Money has a numeric-like behavior because we understand the + symbol means you can add them!

Links on this slide:
- <https://www.youtube.com/watch?v=zh4EgO13Etg>

---

## Slide 19: Hey Bjarne, I want the min of 2 ???



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



*Figure: A callout box to the right of the `min` function definition contains the question:*

What **must** be true of a type **T** for us to be able to use `min`?

---

## Slide 20: Hey Bjarne, I want the min of 2 ???

*Figure: A styled text box/card on the left side of the slide containing a question. The text reads:*

```
What must be true of a type T for us to be able to use min?
```

1. T should have an ordering relationship that makes sense.

2. T should represent something **comparable** where a "minimum" can be logically determined

---

## Slide 21: Hey Bjarne, I want the min of 2 int

*Figure: A hand-drawn number line with tick marks labeled from -4 to 4. An arrow points to the right above the line with the green label "Increasing". An arrow points to the left below the line with the red label "Decreasing".*

1.  T should have an **ordering relationship** that makes sense.
2.  T should represent something **comparable** where a **“minimum”** can be **logically determined**.

---

## Slide 22: Hey Bjarne, I want the min of 2 StanfordIDs

```cpp
StanfordID rachel;
StanfordID preston;

auto minStanfordID = min<StanfordID>(preston, rachel);
```

---

## Slide 23: Hey Bjarne, I want the min of 2 StanfordIDs

```cpp
StanfordID rachel;
StanfordID preston;

auto minStanfordID = min<StanfordID>(rachel, preston);
```

```cpp
StanfordID min(const StanfordID& a, const StanfordID& b)
{
    return a < b ? a : b;
}
```

*Figure: A callout box with an arrow points to the line `return a < b ? a : b;`. The text inside the box reads: "Compiler: “Hey, I don’t know what to do here!”"*

---

## Slide 24: Hello Operator Overloading

### So how do operators work with classes?

- Just like we declare functions in a class, we can declare an operator’s functionality
- When we use that operator with our new object, it performs a custom function or operation
- Just like in function overloading, if we give it the same name, it will override the operator’s behavior!

---

## Slide 25: What are operators?

**Operators** are symbols that perform operations on values, objects, or types and produce a new value or effect.

### Values

*Figure: A black code box displaying the expression "3 + 4" in white text.*

```cpp
3 + 4
```

### Objects

*Figure: A black code box displaying the following code in white text:*

```cpp
Point a;
Point b;
a + b
```

### Types

*Figure: A black code box displaying the following code with syntax highlighting: "sizeof(int)" and "new int(5)" in blue, white, and orange text.*

```cpp
sizeof(int)
new int(5)
```

---

## Slide 26: What operators can we overload?

It turns out, most of them!

```
+  -  *  /  %  ^  &  |  ~  !  ,  =  <  >  <=  >=
++  --  <<  >>  ==  !=  &&  ||  +=  -=  *=
/=  %=  ^=  &=  |=  <<=  >>=  [ ]  ( )  ->
->*  new  new[ ]  delete  delete[ ]
```

---

## Slide 27: What operators can’t be overloaded?

*   Scope Resolution
*   Ternary
*   Member Access
*   Pointer-to-member access
*   Object size, type, and casting

*Figure: A graphic layout of symbols and keywords representing the operators and functions that cannot be overloaded, arranged in two lines: `::`, `?`, `.`, `.*`, `sizeof()`, `typeid()`, and `cast()`.*

---

## Slide 28: What operators can’t be overloaded?

*   Scope Resolution
*   Ternary
*   Member Access
*   Pointer-to-member access
*   Object size, type, and casting

*Figure: A visual display of the specific C++ operators that cannot be overloaded, shown in a monospaced font on the right side of the slide: ::, ?, ., .*, sizeof(), typeid(), and cast().*

```
::   ?   .   .*   sizeof()
typeid()   cast()
```

---

## Slide 29: What operators can't be overloaded?

*   Scope Resolution
*   Ternary
*   Member Access
*   Pointer-to-member access
*   Object size, type, and casting

*Figure: The slide displays a list of non-overloadable operators on the left, with their corresponding symbols shown in a code-style layout on the right: `::` (scope resolution), `?` (ternary), `.` (member access), `.*` (pointer-to-member access), `sizeof()`, `typeid()`, and `cast()` (object size, type, and casting).*

---

## Slide 30: What operators can’t be overloaded?

*Figure: The title "What operators can’t be overloaded?" is displayed in a green banner at the top. Below, a bulleted list on the left is accompanied by a set of operators and functions on the right, which cannot be overloaded. The symbols `::`, `?`, `.`, `.*`, `sizeof()`, `typeid()`, and `cast()` are shown, aligned with the corresponding list items.*

```
::   ?   .   .*   sizeof()
typeid()   cast()
```

- Scope Resolution
- Ternary
- Member Access
- Pointer-to-member access
- Object size, type, and casting

---

## Slide 31: Operator Overloading Syntax

*Figure: A rectangular box containing the syntax for operator overloading in C++.*

```cpp
return_type operator<symbol>(parameter_list);
```

---

## Slide 32: Hey Bjarne, I want the min of 2 StanfordIDs

**.h file**

```cpp
class StanfordID {
private:
    std::string name;
    std::string sunet;
    int idNumber;

public:
    // constructor for our StanfordID
    StanfordID(std::string name, std::string sunet, int idNumber);
    std::string getIdNumber();
    .
    .
    bool operator < (const StanfordID& other) const;
}
```

*Figure: A header file declaration for a `StanfordID` class showing private member variables and public functions, including a constructor and an overloaded less-than operator. The title is displayed in a green banner at the top of the slide.*

---

## Slide 33: Hey Bjarne, I want the min of 2 StanfordIDs

.cpp file

*Figure: A code snippet for the `StanfordID` class implementation, displayed inside a thick black-bordered box.*

```cpp
#include StanfordID.h

std::string StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator < (const StanfordID& rhs) const {
    ?
}
```

---

## Slide 34: Think about it with a partner!

Say that you want to compare StanfordID objects by their idNumber member variable, how could you implement this?

```cpp
bool operator< (const StudentID& rhs) const {
    // TODO: compare StudentIDs by their idNumbers
}
```

---

## Slide 35: Hey Bjarne, I want the min of 2 StanfordIDs

.cpp file

*Figure: A code snippet enclosed in a black border, representing the implementation section of a C++ file.*

```cpp
#include StanfordID.h

int StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.getIdNumber();
}
```

---

## Slide 36: Hey Bjarne, I want the min of 2 StanfordIDs

*Figure: A slide with a light green header containing the title "Hey Bjarne, I want the min of 2 StanfordIDs" (with "StanfordIDs" underlined). Below the header, the text ".cpp file" is displayed above a black-bordered box containing a C++ code snippet.*

.cpp file

```cpp
#include StanfordID.h

int StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.idNumber;
}
```

---

## Slide 37: What questions do we have?

*Figure: A slide with a light green rectangular banner at the top containing the black text "What questions do we have?". The main area of the slide has a white background and features a central photograph of a green parrot looking toward the right. Three small white 3D stick figures are positioned around the parrot, each sitting or leaning against a large red question mark: one on the left side, and two on the right side.*

---

## Slide 38: Practice

https://106b.vercel.app/cs106l-operator-overloading

---

## Slide 39: Non-member overloading

There are two ways to overload:

1. **Member overloading**
   a. Declares the overloaded operator within the scope of your class

---

## Slide 40: Non-member overloading

There are two ways to overload:

1. **Member overloading**
   a. Declares the overloaded operator within the scope of your class

*Figure: A beige callout box with red text reading "This is what we’ve seen!" has a black arrow pointing from it to the highlighted text "Member overloading" in the numbered list above.*

---

## Slide 41: Non-member overloading

There are two ways to overload:

1.  **Member overloading**
    a. Declares the overloaded operator within the scope of your class

*Figure: A code snippet from a `.h` file showing a class definition.*

```cpp
class StanfordID {
private:
std::string name;
std::string sunet;
int idNumber;

public:
    // constructor for our StanfordID
    StanfordID(std::string name, std::string sunet, int idNumber);
    std::string getIdNumber();
    .
    .
    bool operator < (const StanfordID& other) const;
}
```

---

## Slide 42: Non-member overloading

There are two ways to overload:

1. **Member overloading**
    a. Declares the overloaded operator within the scope of your class
2. **Non-member overloading**
    a. Declare the overloaded operator outside of class definitions
    b. Define both the left and right hand objects as parameters

*Figure: A thinking face emoji (🤔) located in the bottom right corner of the slide.*

---

## Slide 43: Non-member overloading

### Non-member Operator Overloading

```cpp
bool operator < (const StanfordID& lhs, const StanfordID& rhs);
```

### Member Operator Overloading

```cpp
bool StanfordID::operator < (const StanfordID& rhs) const {...}
```

---

## Slide 44: Why non-member overloading?

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

```cpp
StanfordID rachel("rfer");
std::string name = "zzhang";

if (rachel < name) {
    std::cout << "Rachel comes before name\n";
}
```

*Figure: A large green checkmark is displayed to the right of the second code block, indicating that the usage syntax is valid.*

---

## Slide 45: Why non-member overloading?

### Class Definition
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

### Usage Example
*Figure: A large red "X" is overlaid on the right-hand code block, indicating that the comparison `name < rachel` is invalid or will not compile with the member operator definition shown on the left.*

```cpp
StanfordID rachel("rfer");
std::string name = "zzhang";

if (name < rachel) {
    std::cout << "Name comes before Rachel\n";
}
```

---

## Slide 46: Non-member overloading

```cpp
StanfordID rachel("rfer");
std::string name = "zzhang";

if (name < rachel) {
    std::cout << "Name comes before Rachel\n";
}
```

*Figure: A red arrow points from the `if (name < rachel) {` line in the code block above down to a second code block showing the expanded form of the operation.*

```cpp
name.operator<(rachel);  // tries to call string’s member function
```

*Figure: A large red "X" mark is positioned to the right of the second code block, indicating an error or that this interpretation is incorrect.*

---

## Slide 47: Non-member overloading

This is actually preferred by the STL, and is more idiomatic C++

**Why:**
1. Allows for the **left-hand-side** to be a **non-class type**

*Figure: Code snippet in a dark-themed code editor showing a non-member operator overloading function.*

```cpp
bool operator<(int lhs, const StanfordID& rhs) {
    return lhs < rhs.getIDNumber();
}
```

---

## Slide 48: Non-member overloading

This is actually preferred by the STL, and is more idiomatic C++

**Why:**
2. Allows us to overload operators with classes we don’t own
a. We could define an operator to compare a StanfordID to other custom classes you define.

*Figure: A slide titled "Non-member overloading" featuring introductory text followed by two black-background code blocks side-by-side. A large green checkmark is superimposed on the right-hand code block.*

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

```cpp
StanfordID rachel("rfer");
std::string name = "zzhang";

if (rachel < name) {
    std::cout << "Rachel comes before name\n";
}
```

---

## Slide 49: Non-member overloading

This is actually preferred by the STL, and is more idiomatic C++

**Why:**
1. Allows us to overload operators with classes we don't own
a. We could define an operator to compare a StanfordID to other custom classes you define.

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

```cpp
StanfordID rachel("rfer");
std::string name = "zzhang";

if (name < rachel) {
  std::cout << "Name comes before Rachel\n";
}
```

*Figure: Two C++ code snippets displayed side-by-side. The left snippet defines a `StanfordID` class with a member function `operator<` that accepts a `std::string`. The right snippet shows an attempt to compare a `std::string` named `name` with a `StanfordID` named `rachel`. A large red "X" is overlaid on the right code snippet, indicating that this comparison is invalid because the member operator only supports comparing a `StanfordID` on the left to a `std::string` on the right.*

---

## Slide 50: Non-member overloading

```cpp
class StanfordID {
private:
    std::string sunet;
public:
    StanfordID(std::string s) : sunet(s) {}
    std::string getSunet() const { return sunet; }
};

// Non-member operator
bool operator<(const StanfordID& lhs, const std::string& rhs) {
    return lhs.getSunet() < rhs;
}

// And if you want symmetry:
bool operator<(const std::string& lhs, const StanfordID& rhs) {
    return lhs < rhs.getSunet();
}
```

*Figure: A large green checkmark appears on the right side of the code block, next to the `StanfordID` class definition.*

It’s better to use non-member overloading so we can do comparison in both directions and with classes we don’t own!

---

## Slide 51: Non-member overloading

*Figure: A slide with a green header titled "Non-member overloading". The main content is a diagram illustrating the difference between non-member and member operator overloading. It features a central labeled box, a code snippet, an explanatory note, and a partially obscured code snippet below.*

### Non-member Operator Overloading

```cpp
bool operator< (const StanfordID& lhs, const StanfordID& rhs);
```

*Figure: A large callout box points to the code above with the following text: "Note both the left and right hand side of the operator are passed in in non-member operator overloading!"*

*Figure: Below the note, there is another box containing a code snippet for a member operator overload, which is partially covered. The visible text is `bool StanfordID:` at the start and `..}` at the end.*

```cpp
bool StanfordID::operator< (const StudentID& rhs) const {...}
```

---

## Slide 52: What about the member variables?

### Non-member Operator Overloading

```cpp
bool operator< (const StanfordID& lhs, const StanfordID& rhs);
```

With member operator overloading we have access to **this->** and the **variables of the class**.

*Figure: An image of a `.cpp file` containing C++ implementation code.*

```cpp
#include StanfordID.h

int StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.idNumber;
}
```

---

## Slide 53: What about the member variables?

What about the member variables?

Can we access these with non-member operator overloading? 🤔

---

## Slide 54: What about the member variables?

Can we access these with non-member operator overloading? 🤔

*Figure: A meme image of Bob Ross. Overlaid on his face are two black squares, each containing a large red letter, spelling the word "NO".*

---

## Slide 55: What about the member variables?

*Figure: A large light-grey box containing two distinct sections for operator overloading styles. The top section is titled "Non-member Operator Overloading" in red text, followed by a code declaration. The bottom section is titled "Member Operator Overloading" in red text, followed by another code declaration.*

### Non-member Operator Overloading
```cpp
bool operator < (const StanfordID& lhs, const StanfordID& rhs);
```

### Member Operator Overloading
```cpp
bool StanfordID::operator < (const StanfordID& rhs) const {...}
```

*Figure: A separate light-grey box positioned below the first one, containing a warning message with some text in purple/magenta.*

It is also undefined behavior to
have both of these because the <
operator is acting on two
<span style="color: purple">StanfordIDs</span>

Remember ambiguity badddddd

---

## Slide 56: What questions do we have?

*Figure: A large image of a green and brown parrot, shown from the side facing right. Surrounding the parrot are three identical 3D graphics. Each graphic consists of a large, red question mark symbol. Leaning against the back of each question mark is a small, white, stylized human figure in a seated, thinking pose with its hand on its chin. The background of the entire slide is white.*

---

## Slide 57: Hello friend!

### Non-member Operator Overloading

```cpp
bool operator< (const StanfordID& lhs, const StanfordID& rhs);
```

The **friend** keyword allows non-member functions or classes to access private information in another class!

---

## Slide 58: Hello friend!

*Figure: A light green horizontal bar at the top of the slide containing the title. Below it is a beige rectangular box containing a heading in red text. Below that is a black-bordered box containing a line of C++ code.*

### Non-member Operator Overloading

```cpp
bool operator< (const StanfordID& lhs, const StanfordID& rhs);
```

The **friend** keyword allows non-member functions or classes to access private information in another class!

### How do you use friend?

In the header of the target class you declare the operator overload function as a friend

---

## Slide 59: Hey Bjarne, I want the min of 2 StanfordIDs

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
    .
    .
    .
    friend bool operator < (const StanfordID& lhs, const StanfordID& rhs);
}
```

---

## Slide 60: Hey Bjarne, I want the min of 2 StanfordIDs

*Figure: A light green banner across the top of the slide.*

**Hey Bjarne, I want the min of 2 <u>StanfordIDs</u>**

**.cpp file**

*Figure: A white rectangle with a black border containing C++ code.*

```cpp
#include StanfordID.h

bool operator< (const StanfordID& lhs, const StanfordID& rhs)
{
    return lhs.idNumber < rhs.idNumber;
}
```

---

## Slide 61: Note: this also works!

.cpp file

```cpp
#include StanfordID.h

bool operator< (const StanfordID& lhs, const StanfordID& rhs)
{
    return lhs.getIdNumber() < rhs.getIdNumber();
}
```

*Figure: A code box displaying a .cpp file that defines a non-member `operator<` function for the `StanfordID` class. The function takes two `const StanfordID&` parameters and returns the result of comparing their ID numbers via public getter methods. A beige annotation box in the lower right states: "In this case the friend keyword is not required since we're not using a private member function or variable" — indicated with arrows pointing from the annotation text toward the body of the function, highlighting that only public accessors (`getIdNumber()`) are used.*

---

## Slide 62: What questions do we have?

*Figure: A slide with a large green header bar at the top containing the title. The main body of the slide features a large photograph of a green parrot in profile, looking toward the right side of the frame. Surrounding the parrot are three identical 3D illustrations of a white humanoid figure sitting and leaning against a large red question mark. One figure is positioned to the left of the parrot's head, one is to the upper right, and one is to the lower right.*

---

## Slide 63: So why is this even meaningful?

```cpp
StanfordID rachel;
StanfordID preston;

auto minStanfordID = min<StanfordID>(rachel, preston);

StanfordID min(const StanfordID& a, const StanfordID& b)
{
    return a < b ? a : b;
}
```

*Figure: A code example showing the definition and use of a `min` function for `StanfordID` objects. A compiler callout states: "Compiler: 'Hey, now I know what to do here! 😀'"*

---

## Slide 64: So why is this even meaningful?

* There are many operators that you can define in C++ like we saw

```cpp
+ - * / % ^ & | ~ ! , = < > <= >=
++ -- << >> == != && || += -= *=
/= %= ^= &= |= <<= >>= [ ] ( ) ->
->* new new[] delete delete[]
```

---

## Slide 65: So why is this even meaningful?

*   There are many operators that you can define in C++ like we saw
*   There’s a lot of functionality we can unlock with operators

```cpp
+ - * / % ^ & | ~ ! , = < > <= >=
++ -- << >> == != && || += -= *=
/= %= ^= &= |= <<= >>= [ ] ( ) ->
->* new new[] delete delete[]
```

---

## Slide 66: More importantly

“Operators allow you to convey meaning about
types that functions don’t”

---

## Slide 67: Rules and Philosophies

*   Because operators are intended to convey meaning about a type, the meaning should be **obvious**

*   The operators that we can define are oftentimes arithmetic operators. The functionality should be **reasonably similar** to their corresponding operations
    *   You don’t want to define operator+ to be set subtraction

*   If the meaning is not obvious, then maybe define a function for this

*Figure: A light yellow box with a black border is positioned in the lower right corner. It contains the text "This is known as the Principle of Least Astonishment (PoLA)" in red, bold font.*

---

## Slide 68: In general

*   There are some good practices like the **rule of contrariety**
*   For example when you define the operator== use the rule of contrariety to define operator!=

```cpp
bool StanfordID::operator==(const StanfordID& other) const {
    return (name == other.name) && (sunet == other.sunet) &&
    (idNumber == other.idNumber);
}

bool StanfordID::operator!=(const StanfordID& other) const {
    return !(*this == other);
}
```

---

## Slide 69: <<
- However there’s a lot of flexibility in implementing operators
- For example << stream insertion operator

*Figure: A slide titled '<<' with a green header banner. Below the header are two bullet points. A large black-bordered box contains two different C++ implementations of the stream insertion operator (`operator<<`) for a `StanfordID` class. In the bottom-right corner of this box, there is a smaller callout box with a thin border containing red text.*

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

The way you use this operator may influence how you implement it

---

## Slide 70: Practice

*Figure: An image of a pepperoni pizza on a wooden board, positioned on the left side of the slide.*

### Pizza Order Class

Variables: customer, topping, num of slices

#### Getter functions:

- getCustomer()
- getTopping()
- getSlices()

### Operator Overloading Functions:

- += → add more slices to someone’s order
- == → check if the number of slices, customer, and toppings are the exact same
- < → check if one pizza order has less slices than the other
- > → check if one pizza order has more slices than the other
- << → print CustomerName: #ofSlices, Topping

---

## Slide 71: Practice

*Figure: A photograph of a whole pepperoni pizza on a circular wooden board.*

106b.vercel.app/cs106l-operator-overloading-2

---

## Slide 72: Final thoughts
1. Operator overloading unlocks a new layer of functionality and meaning within objects that we define
2. Operators should *make sense*, the entire point is that convey some meaning that functions don’t about the type itself.
3. You should overload when you need to, for example if you’re not using a stream with your type, then don’t overload << or >>.
