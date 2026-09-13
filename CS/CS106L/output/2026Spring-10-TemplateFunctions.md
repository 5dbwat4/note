# Lecture 10: TemplateFunctions (2026Spring)

> PDF title: 2026Spring-10-TemplateFunctions.pptx
> Source: `assets/slides/2026Spring-10-TemplateFunctions.pdf` · 150 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Welcome back! Link to Attendance Form ↓

*Figure: A large QR code for an attendance form. The text above it reads "Welcome back! Link to Attendance Form" with a downward-pointing arrow (↓) indicating the code below.*

---

## Slide 2: GUYS HOW ARE WE DOING

tinyurl.com/cs106l-kermit

(forgive me i dont know how to use pollev LOL)

*Figure: A 3x3 grid of Kermit the Frog memes, numbered 1 through 9. Top row: 1) Kermit looking tired; 2) Kermit playing a banjo; 3) Kermit holding a black rotary phone. Middle row: 4) Kermit looking out a car window with the handle "@dailyfeelingsscale" at the top; 5) Kermit sipping tea; 6) Kermit screaming. Bottom row: 7) Kermit lying face down on a bed; 8) Kermit smiling in a field of flowers; 9) Kermit wrapped in a white towel.*

Links on this slide:
- <https://tinyurl.com/cs106l-kermit>

---

## Slide 3: Recall: What are templates?

*   Turn to a partner and discuss:
    *   What is a template class?
    *   Why would you use a template class?
*   Introduce yourself and take 60s to talk!

*Figure: A low-resolution meme image of a cat appearing to talk, with the caption "yap yap" at the bottom.*

---

## Slide 4: Recall: What are templates?
*   What is a template class?
    *   ✅ A blueprint for creating classes with generic types
*   Why would you use a template class?
    *   ✅ Template classes eliminate code redundancy!

---

## Slide 5: Recall: What are templates?

*Figure: A diagram illustrating the concept of templates. On the left, there is a stack of three separate class definitions. A large orange arrow points to the right, where a single template class definition and several instances are shown, demonstrating code simplification.*

**Left Side (Multiple Specific Classes):**
```cpp
class IntVector {

class DoubleVector {

class StringVector {
    // Code to store
    // a list of
    // strings...
};
};
};
```

**Right Side (Generic Template Class and Instances):**
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

## Slide 6: Key Idea: Templates automate code generation

Key Idea: Templates automate code generation

---

## Slide 7: Recall: Template Instantiation

When you write code like this...
```cpp
template <typename T>
class Vector {
    T& at(size_t index);
    // More methods...
};

Vector<int> v;
```

Compiler produces code like this...
```cpp
class IntVector {
    int& at(size_t index);
    // More methods...
};

IntVector v;
```

---

## Slide 8: Is there more that templates can do?

Is there more that templates can do?

---

## Slide 9: Lecture 10: Template Functions

Lecture 10: Template Functions

CS106L, Spring 2026

Preston Seay & Rachel Fernandez

---

## Slide 10: Today’s Agenda

*   **Template Functions**
    *   How can we extend template classes to functions? Code demo!
*   **Concepts**
    *   How can we make C++ templates sane?
*   **Variadic Templates**
    *   How do we build functions that accept a variable number of arguments?
*   **Template Metaprogramming**
    *   How do we run code at compile time?

---

## Slide 11: We may not get through everything today!

**We may not get through everything today!**

(Slides are posted if you want to review after)

---

## Slide 12: What questions do you have?

# What questions do you have?

*Figure: A photograph of Bjarne Stroustrup looking towards the camera with his hand resting on his chin. In the background, there are various items on a desk or wall, including a poster that reads "PROGRAMMING LANGUAGE BJARNE STROUSTRUP" and a blue book or binder labeled "Style and Practice Using C++".*

bjarne_about_to_raise_hand

---

## Slide 13: Template Functions

---

## Slide 14: Bjarne has a problem…

Hey I really need a way to get the smallest of two values in C++!

*Figure: A photograph shows two men seated in chairs having a conversation. The man on the left, who is Bjarne Stroustrup, has a large red speech bubble coming from him containing the text shown above. The man on the right is smiling and holding some papers. A small, low, round table with two glasses sits between them. In the background, there are glass walls and doors, with some posters or signs visible through them.*

---

## Slide 15: Writing a min function

```cpp
// Returns the smaller of a and b
int min(int a, int b) {
    return a < b ? a : b;
}
```

*Figure: A rectangular note box labeled "Ternary Operator" is connected by an arrow to the ternary expression line `return a < b ? a : b;` in the code block. The note contains the text: "Return a if a < b otherwise return b".*

---

## Slide 16: Writing a min function
min makes sense for more than just integers. How can we do this?

*Figure: A box contains three lines of code showing function calls. An arrow from a smaller callout box points to the third line of code. The callout box contains the text "Returns the string that comes first alphabetically".*

```cpp
min(106, 107);           // int, returns 106
min(1.2, 3.4);           // double, returns 1.2
min("Preston", "Rachel"); // string, returns "Preston"
```

---

## Slide 17: One solution: function overloading

*Figure: A code box displaying three overloaded versions of a `min` function for different data types: `int`, `double`, and `std::string`.*

```cpp
int min(int a, int b) {
    return a < b ? a : b;
}

double min(double a, double b) {
    return a < b ? a : b;
}

std::string min(std::string a, std::string b) {
    return a < b ? a : b;
}
```

---

## Slide 18: Hmm... this looks familiar!

🤔 **Hmm... this looks familiar!**

*Figure: Three overlapping white code editor windows with black borders and drop shadows. Each window displays a C++ class definition. The topmost window shows `class StringVector`, the middle window shows `class DoubleVector`, and the bottom window shows `class IntVector`. The code inside each window consists of the class declaration and comments describing its purpose.*

```cpp
class IntVector {
    // Code to store
    // a list of
    // integers…
};
```

```cpp
class DoubleVector {
    // Code to store
    // a list of
    // doubles…
};
```

```cpp
class StringVector {
    // Code to store
    // a list of
    // strings…
};
```

---

## Slide 19: We can use templates!

**We can use templates!**

---

## Slide 20: Let's take this…

```cpp
int min(int a, int b) {
    return a < b ? a : b;
}

double min(double a, double b) {
    return a < b ? a : b;
}

std::string min(std::string a, std::string b) {
    return a < b ? a : b;
}
```

*Figure: A callout box with a drop shadow positioned to the right of the code, containing the text "This works, but it’s missing the bigger idea!"*

---

## Slide 21: ...and turn it into this!

*Figure: A diagram centered on a code block inside a large rectangle. Two white callout boxes with drop shadows are positioned above the code. The box on the left, containing the text "This is a **template**", has a black arrow pointing down to the `template` keyword in the code. The box on the right, containing the text "**T** gets replaced with a specific type", has a black arrow pointing down to the letter `T` in the function signature.*

*   **This is a template**
*   **T gets replaced with a specific type**

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}
```

---

## Slide 22: A template is like a factory

*Figure: A diagram illustrating the concept of a C++ function template using a factory metaphor. A cartoon factory image sits at the center. To the left are two input boxes labeled `int` (top) and `string` (bottom), both in red text. Overlaid on the factory are two output boxes: `min<int>` (in purple and red) and `min<string>` (in purple and red). Below the factory is a box containing the template function definition. The overall message is that a template acts like a factory: you feed it a type, and it produces a specialized function for that type.*

```cpp
template <typename T>
T min(T a, T b)
```

---

## Slide 23: Remember: templates vs. functions

*Figure: Four white rectangular boxes with black borders arranged in a 2x2 grid. The top boxes contain C++ code snippets, and the bottom boxes provide explanatory text for each snippet.*

| Template | Function |
| :--- | :--- |
| ```cpp<br>template <typename T><br>T min(T a, T b)<br>``` | ```cpp<br>min<std::string><br>``` |
| This is a template.<br>It’s **not** a function | This is a function.<br>A.K.A a template instantiation |

---

## Slide 24: Template functions

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}
```

*Figure: A red arrow points downward from the first code block to the second. A text box to the right of the arrow contains the note: "We can also use references to avoid making a copy!"*

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

---

## Slide 25: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup with his hand to his chin, appearing to be in thought. Behind him are shelves with several copies of his book, "The C++ Programming Language".*

What questions do you have?

```text
bjarne_about_to_raise_hand
```

---

## Slide 26: How do we call template functions?

---

## Slide 27: Option A: explicit instantiation

Explicit instantiation passes the types directly, just like template classes

```cpp
min<int>(106, 107);        // Returns 106
min<double>(1.2, 3.4);     // Returns 1.2
```

---

## Slide 28: Option A: explicit instantiation

Template functions cause the compiler to **generate code** for us

```cpp
int min(int a, int b) {                // Compiler generated
    return a < b ? a : b;              // Compiler generated
}                                      // Compiler generated

double min(double a, double b) {       // Compiler generated
    return a < b ? a : b;              // Compiler generated
}                                      // Compiler generated

min<int>(106, 107);                    // Returns 106
min<double>(1.2, 3.4);                 // Returns 1.2
```

---

## Slide 29: Key Idea
**Key Idea:** Templates automate code generation

---

## Slide 30: Option B: implicit instantiation

Implicit instantiation lets the compiler **infer** the types for us

*Figure: A diagram illustrating implicit type deduction. A large rectangular box contains two lines of C++ code. A black arrow points from a speech-bubble-shaped annotation box toward the first function call. The annotation box contains the text: "I didn’t specify any template types!"*

```cpp
min(106, 107);     // int, returns 106
min(1.2, 3.4);     // double, returns 1.2
```

---

## Slide 31: Implicit instantiation is kind of like auto

Implicit instantiation is kind of like **auto**

*Figure: A code snippet in a rectangular box with shadow border.*

```cpp
auto number = 106;
```

This still is an **int**, we just let the compiler figure it out

---

## Slide 32: Implicit instantiation is kind of like auto
**Implicit instantiation is kind of like <span style="color:red;">auto</span>**

```cpp
int m = min(106, 107);
```

It’s exactly as if we wrote
`min<int>(106, 107)`

---

## Slide 33: Implicit instantiation can be finicky

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}

min("Preston", "Rachel");
```

*Figure: The code defines a template function `min`. Two arrows point from the arguments `"Preston"` and `"Rachel"` in the call to a box below that contains the text `const char*` in red. A larger arrow points from the entire function call to a text box containing the question: "What type is T? What are the types of the arguments?" followed by the note in gray: "Hint: you might know this if you’ve taken CS107!"*

---

## Slide 34: Implicit instantiation can be finicky

```cpp
const char* min(const char* a, const char* b) {
    return a < b ? a : b;
}

min<const char*>("Preston", "Rachel");
```

*Figure: A photo of Bjarne Stroustrup looking serious, placed next to a speech bubble.*

> Pointer comparison AHHHH!!!
> This is not what we wanted
>
> ☐ This is Bjarne judging you for using pointer comparison

---

## Slide 35: Implicit instantiation can be finicky

We can always use explicit instantiation in ambiguous cases like this

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}

min<std::string>("Preston", "Rachel");
```

*Figure: Code example showing a template `min` function and an explicit instantiation call `min<std::string>("Preston", "Rachel")`. To the right is a callout box and below that a photo.*

**Callout box (to the right of code):**

**const char\*** gets converted to
**std::string** here

↓ Here is Bjarne pleased with
you for getting the compiler to
understand you!

*Figure: A photo of Bjarne Stroustrup, creator of C++, appearing pleased, positioned below the callout box on the right side of the slide.*

---

## Slide 36: Implicit instantiation can be finicky

Another example: the types of the parameters don’t strictly match

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

```cpp
min(106, 3.14);      // ❌ Doesn't compile
```

*Figure: Two black arrows point from below the function call `min(106, 3.14);` to its arguments. The left arrow points to the integer literal `106` and originates from a white box labeled "int". The right arrow points to the floating-point literal `3.14` and originates from a white box labeled "double".*

A separate white box to the right contains the text:
> **Explicit instantiation!**
> `min<double>(106, 3.14)`

*Figure: A photograph of a thoughtful-looking man with a receding hairline, resting his chin on his hand, smiling slightly. He is wearing a blue shirt. Behind him are bookshelves filled with books and some items on a desk.*

---

## Slide 37: Implicit instantiation can be finicky

Implicit instantiation can be finicky
Another solution: make our template a little bit more flexible.

```cpp
template <typename T, typename U>
????? min(const T& a, const U& b) {
    return a < b ? a : b;
}

min(106, 3.14);
```

*Figure: A large code box contains the C++ code. Inside the box, to the right of the code, a smaller text box asks: "What should the return type of this function be?"*

*Figure: Below the code box, two annotation boxes are positioned. The left box contains "T = int" and has an arrow pointing to the "106" argument in the function call. The right box contains "U = double" and has an arrow pointing to the "3.14" argument in the function call.*

---

## Slide 38: Implicit instantiation can be finicky

Another solution: make our template a little bit more flexible.

```cpp
template <typename T, typename U>
auto min(const T& a, const U& b) {
    return a < b ? a : b;
}
```

*Figure: A callout box points toward the function definition with the text: "What should the return type of this function be?"*

`min(106, 3.14);`

*Figure: A callout box points toward the function call with the text: "It’s complicated, let the compiler figure it out with auto" (where "auto" is highlighted in red).*

---

## Slide 39: Pro tip: Use IDE to see instantiation types
IDEs (e.g. VSCode, QtCreator) can show what types were actually used

*Figure: A screenshot of an IDE (VSCode) editor window for a file named `main.cpp`. The breadcrumb navigation at the top shows the path `8-template-classes-and-cc > C++ main.cpp > min<T>(T, T)`. A tooltip box is displayed, pointing to the function call on line 9, showing the resolved template type.*

Breadcrumb: `8-template-classes-and-cc > C++ main.cpp > min<T>(T, T)`

Tooltip text:
`const char *min<const char *>(const char *a, const char *b)`

```cpp
template <typename T>
T min(T a, T b)
{
  return a < b ? a : b;
}

int main()
{
  auto m = min("Jacob", "Fabio");
}
```

---

## Slide 40: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup resting his chin on his hand. In the background, computer monitors and posters are visible; one poster on the upper right has the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". The text "What questions do you have?" is overlaid in a large, bold, sans-serif font across the center of the image. Below the photograph, the caption "bjarne_about_to_raise_hand" is displayed in a monospace font.*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 41: Question on Template Use

Q: Where do we use template functions in practice?

---

## Slide 42: A: All over the place!
One prominent example: iterators

---

## Slide 43: Recall: we have many iterator types!

### vector\<T\>::iterator

*Figure: Diagram of a vector's contiguous memory layout. Four blue boxes in a row, labeled with indices 0, 1, 2, 4 above them. The values inside the boxes are 1, 2, 3, 4 respectively.*

### deque\<T\>::iterator

*Figure: Diagram of a deque's segmented memory layout. Three blue squares at the top represent block pointers. Blue arrows point from these blocks down to three memory segments. The leftmost segment contains [grey, grey, 1, 9], the middle segment contains [7, 3, 2, 1], and the rightmost segment contains [2, 9, grey, grey]. Grey cells represent unused slots.*

### map\<K, V\>::iterator

*Figure: Diagram of a map's balanced binary search tree (BST) structure. The root node contains "CS106L" | 42. The left child of the root is "Chris" | 31. The right child of the root is "Nick" | 51. Nick has two children: left is "Keith" | 14, right is "Sean" | 35. All nodes are pink with grey value fields, connected by black arrows indicating parent-child relationships.*

### unordered\_map\<K, V\>::iterator

*Figure: Diagram of an unordered_map's hash table structure. A vertical array of 5 buckets is labeled 0 through 4. Red arrows point from occupied buckets to pink entry boxes: bucket 0 points to "Chris" | 31, bucket 2 points to "Nick" | 51, and bucket 3 points to "Sean" | 35. Buckets 1 and 4 are empty (no arrows). Each entry box has a pink left portion with the key and a grey right portion with the value.*

---

## Slide 44: Writing a **find** function

```cpp
std::vector<int> v { 106, 111, 42, 112 };
auto it = find(v.begin(), v.end(), 42);
*it = 107;
// v = { 106, 111, 107, 112 }
```

*Figure: A diagram illustrating the state of the vector after the operations. It shows a sequence of boxes representing vector elements, indexed 0, 1, 2, and 3, with an additional dashed box at index 4. Box 0 contains 106, box 1 contains 111, box 2 contains 107 (highlighted with an orange background), and box 3 contains 112. A label "find(b, e, 42)" is centered above the sequence. A "begin" label with an arrow points down to index 0. An "it" label with an arrow points up to index 1. An "end" label with an arrow points down to the dashed box at index 4.*

---

## Slide 45: Writing a find function

```cpp
std::vector<int>::iterator find(
    std::vector<int>::iterator begin,
    std::vector<int>::iterator end,
    int value
) {
    // Logic to find the iterator in this container
    // Should return end if no such element is found
}
```

---

## Slide 46: This definition is too specific!

*Figure: A C++ function signature and stub located inside a bordered box with a drop shadow.*

```cpp
std::vector<int>::iterator find(
    std::vector<int>::iterator begin,
    std::vector<int>::iterator end,
    int value
) {
    // Logic to find the iterator in this container
    // Should return end if no such element is found
}
```

---

## Slide 47: Writing a find function

Our find function won’t work for other vectors, or other containers

*Figure: A code snippet inside a box.*

```cpp
std::vector<std::string> v { "seven", "kingdoms" };
auto it = find(v.begin(), v.end(), "kingdoms");
// Won't compile

std::set<std::string> s { "house", "targaryen" };
auto it = find(s.begin(), s.end(), "targaryen");
// oh man D:
```

---

## Slide 48: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup looking towards the camera with a slight smile, his hand resting near his chin. Behind him on the wall is a poster for his book, "Programming: Principles and Practice Using C++".*

bjarne_about_to_raise_hand

---

## Slide 49: Let's write a template function!

**Let’s write a template function!**

---

## Slide 50: Writing a find function… but templated

Form a small group and discuss how to implement this function!

*Figure: A code block illustrating the skeleton of a templated find function. The function template has placeholders (????) for the return type and parameter types. It includes comments describing the required logic and a usage example at the bottom.*

```cpp
template <typename Iterator, typename TElem>
???? find(???? begin, ???? end, ???? value) {
    // Logic to find and return the iterator
    // in this container whose element is value
    // Should return end if no such element is found
}

find<std::vector<int>::iterator, int>(b, e, 42);
```

---

## Slide 51: Writing a find function… but templated

Let’s use the template types!

*Figure: A code block inside a black rectangular border.*

```cpp
template <typename Iterator, typename TElem>
Iterator find(Iterator begin, Iterator end, TElem value) {
    // Logic to find and return the iterator
    // in this container whose element is value
    // Should return end if no such element is found
}

find<std::vector<int>::iterator, int>(b, e, 42);
```

---

## Slide 52: Writing a find function… but templated

Let’s implement a simple find function!

```cpp
template <typename Iterator, typename TElem>
Iterator find(Iterator begin, Iterator end, TElem value) {
    Iterator it = begin;
    while (it != end) {
        if (*it == value) break;
        ++it;
    }
    return it;
}

find<std::vector<int>::iterator, int>(b, e, 42);
```

*Figure: The code is presented inside a rectangular white box with a thin black border and a drop shadow.*

---

## Slide 53: find function in the STL

- Part of <algorithm> header (we’ll talk more about this on Thursday)!
- You now have all the tools to read the C++ standard!

*Figure: A box displaying the C++ standard library function signatures for find functions, with a title and code snippet.*

```cpp
std::find, std::find_if, std::find_if_not

Defined in header <algorithm>

template< class InputIt, class T >
InputIt find( InputIt first, InputIt last, const T& value );
```

---

## Slide 54: But Wait There's More Meme

*Figure: A meme image featuring Dwight Schrute from the television series "The Office" looking directly at the camera with a serious, deadpan expression.*

**BUT WAIT**

**THERES MORE**

*Source: makeameme.org*

---

## Slide 55: Concepts

Concepts

---

## Slide 56: Back to our min function

```cpp
template <typename T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

// For which T will the following compile successfully?
```cpp
T a = /* an instance of T */;
T b = /* an instance of T */;
min<T>(a, b);
```

*Figure: A text box with a shadow containing the question: "What must be true of a type **T** for us to be able to use **min**?"*

---

## Slide 57: Back to our min function

**T** must have an **operator<** to make sense in this context

```cpp
struct StanfordID; // How do we compare two IDs?

StanfordID preston { "Preston", "pseay" };
StanfordID rachel { "Rachel", "rfern" };
min<StanfordID>(preston, rachel); // ❌ Compiler error
```

---

## Slide 58: What happened?

*Figure: A screenshot of a terminal window showing a compiler error message. The terminal has a white background with a subtle drop shadow. The text displays the g++ compilation command and the resulting error output with syntax highlighting: commands and filenames in blue, "error" and "template" in red, "return" in blue, "min" in purple, and a caret indicator (`^`) in red.*

```
$ g++ main.cpp --std=c++20
main.cpp:9:12: error: invalid operands to binary expression
('const StanfordID' and 'const StanfordID')
return a < b ? a : b;
       ~ ^ ~
main.cpp:20:3: note: in instantiation of function template specialization
'min<StanfordID>' requested here
min<StanfordID>(preston, rachel);
^
1 error generated.
```

---

## Slide 59: What happened?

*Figure: A screenshot of a terminal window showing a compiler error message from g++. The command `$ g++ main.cpp --std=c++20` is at the top, with "20" highlighted in blue. The output displays a red "error:" message stating "invalid operands to binary expression ('const StanfordID' and 'const StanfordID')". The source code line `return a < b ? a : b;` is highlighted with a yellow background, and red symbols (`~ ^ ~`) point to the less-than operator. A note explains the error is from the instantiation of function `template` specialization (where "template" is red) `'min<StanfordID>'` (highlighted in purple). A red caret (`^`) points to the function call `min<StanfordID>(thomas, rachel);`. The final line, "1 error generated.", has the number "1" in blue.*

```text
$ g++ main.cpp --std=c++20
main.cpp:9:12: error: invalid operands to binary expression
('const StanfordID' and 'const StanfordID')
return a < b ? a : b;
       ~ ^ ~
main.cpp:20:3: note: in instantiation of function template specialization
'min<StanfordID>' requested here
min<StanfordID>(thomas, rachel);
^
1 error generated.
```

---

## Slide 60: What happened?

Compiler instantiated our template, and only then did it spot the error

```cpp
StanfordID preston { "Preston", "pseay" };
StanfordID rachel { "Rachel", "rfern" };
min<StanfordID>(preston, rachel);

StanfordID min(const StanfordID& a, const StanfordID& b)
{
    return a < b ? a : b;
}
```

*Figure: Two annotated comment boxes with arrows. The upper comment box, labeled "Compiler:", contains the text "min for StanfordIDs, coming right up!" and has an arrow pointing to the `min<StanfordID>(preston, rachel);` line. The lower comment box, labeled "Compiler:", contains the text "AHHH what do I do here! I don't know how to compare two StanfordIDs" and has an arrow pointing to the `return a < b ? a : b;` line within the min function definition.*

---

## Slide 61: Delayed Error Detection in Templates

Compiler only finds the error *after* instantiation

---

## Slide 62: Recall: std::set also requires an operator<

Bad templates can produce really confusing compiler errors…

### std::set\<StanfordID\> s { preston, rachel };

*Figure: A terminal window screenshot displaying an extensive list of C++ compiler errors. An arrow points from a box that says "Recall: std::set requires operator<" toward the code and error output. A separate box on the right contains the text "The error message continues to go on 😭".*

```text
jacobrobertsbaca@Jacobs-MacBook-Pro-3 8-template-classes-and-cc % clang++ main.cpp --std=c++20
In file included from main.cpp:1:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/string:520:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/__functional_base:16:
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/__functional/operations.h:487:21: error: invalid operands to binary expression ('const StanfordID' and '
const StanfordID')
{return __x < __y;}
           ^  ~
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/__tree:2023:28: note: in instantiation of member function 'std::less<StanfordID>::operator()
here
        if (__hint == end() || value_comp()(__v, *__hint))  // check before
                                    ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/__tree:2114:36: note: in instantiation of function template specialization 'std::__tree<StanfordID, std::less<StanfordID>, std::allocator<StanfordID>>::__find_equal<StanfordID>' requested here
    __node_base_pointer& __child = __find_equal(__p, __parent, __dummy, __k);
                                           ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/__tree:1257:16: note: in instantiation of function template specialization 'std::__tree<StanfordID, std::less<StanfordID>, std::allocator<StanfordID>>::__emplace_hint_unique_key_args<StanfordID, const StanfordID &>' requested here
        return __emplace_hint_unique_key_args(__p, _NodeTypes::__get_key(__v), __v).first;
               ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/...
```

---

## Slide 63: Also a problem for our find function

```cpp
int main() {
    int idx = find(1, 5, 3); // eh... 3 I guess? haelp 🥲
}
```

*Figure: A terminal/compiler error output showing:*

```
main.cpp:16:9: error: indirection requires pointer operand ('int' invalid)
    if (*it == value) {
        ^~~
main.cpp:29:3: note: in instantiation of function template specialization 'find<int, int>'
  find(1, 5, 3); // eh... 3 I guess? haelp 🥲
        ^
1 error generated.
```

*Figure: A speech bubble from the bottom right of the slide containing:*

**C++ beginner:** "Uhh..
Compiler, what the @!#* do you
mean?"

---

## Slide 64: Template Constraints Question

Idea: How do we put constraints on templates?

---

## Slide 65: Idea: How do we put constraints on templates?

• Templates are great, but the errors they produce when used incorrectly are unintuitive  
• How can we be up-front about what we require of a template type?

### C#
```csharp
class EmployeeList<T>
where T : notnull, Employee, IComparable<T>, new()
```

### Java
```java
class ListObject<T extends Comparable<T>>
```

---

## Slide 66: Idea: How do we put constraints on templates?

Compiler shouldn’t instantiate a template unless all constraints are met

*Figure: A diagram featuring a large box containing three C++ template code snippets. To the right of the box are two white callout boxes with text and black arrows. The top callout box says "**T must have operator<**" and has two arrows: one pointing to the template declaration `template <typename T>` and one pointing to the function parameters `(const T& a, const T& b)` of the `min` function. The bottom callout box says "**It must be an iterator type**" and has one arrow pointing to the parameters `(It begin, It end, const T& value)` of the `find` function.*

```cpp
template <typename T>
T min(const T& a, const T& b)

template <typename T>
struct set;

template <typename It, typename T>
It find(It begin, It end, const T& value)
```

**T must have operator<**

**It must be an iterator type**

---

## Slide 67: What questions do you have?

*Figure: A photo of Bjarne Stroustrup, wearing glasses and a patterned shirt, with his hand resting near his chin. Behind him, a copy of "The C++ Programming Language" book is visible. The large text "What questions do you have?" is overlaid across the center of the image. Below the photo is the caption `bjarne_about_to_raise_hand`.*

What questions do you have?

---

## Slide 68: Introducing C++ concepts!

<span style="color: black">Introducing</span> <span style="color: red">C++ concepts!</span>

---

## Slide 69: Creating a Comparable concept

*Figure: A C++ code snippet is displayed inside a rectangular border with a thin black outline.*

```cpp
template <typename T>
concept Comparable = requires(T a, T b) {
  { a < b } -> std::convertible_to<bool>;
};
```

---

## Slide 70: Creating a Comparable concept

*Figure: A slide with a title and an annotated code snippet. A box defines "concept" as "a named set of constraints". A thick, curved black arrow originates from this box and points to the first line of the code snippet.*

`concept`: a named set of **constraints**

```cpp
template <typename T>
concept Comparable = requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};
```

---

## Slide 71: Creating a Comparable concept

```cpp
template <typename T>
concept Comparable = requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};
```

*Figure: A diagram with two annotation boxes and arrows pointing to specific parts of the code. The left annotation box reads "concept: a named set of constraints" and has a curved arrow pointing to the word `concept` in the code. The right annotation box reads "requires: Given two T’s, I expect the following to hold" and has a straight arrow pointing to the `requires(const T a, const T b)` part of the code.*

---

## Slide 72: Creating a Comparable concept

```cpp
template <typename T>
concept Comparable = requires(const T a, const T b) {
  { a < b } -> std::convertible_to<bool>;
};
```

*Figure: A slide titled "Creating a Comparable concept" (where "Comparable" is red) illustrating the components of a C++ concept definition. Three callout boxes with arrows annotate specific parts of the code snippet:*
- *A callout labeled "concept: a named set of constraints" (with "concept" in red and "constraints" in bold) points an arrow to the `concept` keyword in the code.*
- *A callout labeled "requires: Given two T’s, I expect the following to hold" (with "requires" in red) points an arrow to the start of the `requires` block.*
- *A callout labeled "constraint: Anything inside the { } must compile without error" (with "constraint" in red) points an arrow to the expression `{ a < b }`, which is highlighted in yellow.*

---

## Slide 73: Creating a Comparable concept

*Figure: A diagram illustrating the components of a C++ concept definition. A code block is at the center, with four annotation boxes connected by arrows to specific parts of the code.*

```cpp
template <typename T>
concept Comparable = requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};
```

*Top-left annotation box: An arrow points from the box to the word `concept` in the code. The box contains the text: "concept: a named set of **constraints**".*

*Top-right annotation box: An arrow points from the box to the word `requires` in the code. The box contains the text: "requires: Given two T’s, I expect the following to hold".*

*Bottom-left annotation box: An arrow points from the box to the expression `{ a < b }` in the code. The box contains the text: "constraint: Anything inside the { } must compile without error".*

*Bottom-right annotation box: An arrow points from the box to the type constraint `std::convertible_to<bool>` in the code. The box contains the text: "constraint: ...and the result must be bool-like" followed by "convertible_to is also a concept!".*

---

## Slide 74: Creating a Comparable concept
```cpp
template <typename T>
concept Comparable = requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};
```
*Figure: A diagram illustrating the structure of a C++ concept definition. The code snippet is centrally displayed with four annotation boxes connected by arrows pointing to specific parts of the code:
- A box containing the text "concept: a named set of constraints" points to the `concept` keyword.
- A box containing the text "requires: Given two T’s, I expect the following to hold" points to the `requires` clause.
- A box containing the text "constraint: Anything inside the { } must compile without error" points to the expression `{ a < b }`.
- A box containing the text "constraint: ...and the result must be bool-like" and the note "convertible_to is also a concept!" points to the `-> std::convertible_to<bool>;` expression.*

---

## Slide 75: Using our Comparable concept

```cpp
template <typename T> requires Comparable<T>
T min(const T& a, const T& b);
```

*Figure: A large red arrow points downwards from the top code box to the bottom code box.*

```cpp
// Super slick shorthand for the above
template <Comparable T>
T min(const T& a, const T& b);
```

---

## Slide 76: Concepts greatly improve compiler errors

Here’s the error from before when instantiating a set without a concept

```
jacobrobertsbaca@Jacobs-MacBook-Pro-3 8-template-classes-and-cc % clang++ main.cpp --std=c++20
In file included from main.cpp:1:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/
OSX.sdk/usr/include/c++/v1/string:520:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/
OSX.sdk/usr/include/c++/v1/__functional_base:16:
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk
+/usr/include/c++/v1/__functional/operations.h:487:21: error: invalid operands to binary expression ('const St
const StanfordID')
    {return __x < __y;}
         ~~~ ^ ~~~
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c+
+/usr/include/c++/v1/__tree:2023:28: note: in instantiation of member function 'std::less<StanfordID>::operato
here
    if (__hint == end() || value_comp()(__v, *__hint))  // check before
                              ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c+
+/usr/include/c++/v1/__tree:2114:36: note: in instantiation of function template specialization 'std::__tree<S
:less<StanfordID>, std::allocator<StanfordID>>::__find_equal<StanfordID>' requested here
    __node_base_pointer& __child = __find_equal(__p, __parent, __dummy, __k);
                                         ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c+
+/usr/include/c++/v1/__tree:1257:16: note: in instantiation of function template specialization 'std::__tree<S
:less<StanfordID>, std::allocator<StanfordID>>::__emplace_hint_unique_key_args<StanfordID, con
>' requested here
    return __emplace_hint_unique_key_args(__p, _NodeTypes::__get_key(__v), __v).first;
                ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c+
+/usr/include/c++/v1/set:682:25: note: in instantiation of member function 'std::__tree<StanfordID, std::less
```

```cpp
template <typename T>
struct std::set;
```

*Figure: An image of a gauge or meter with a needle. The title above the gauge reads "yapping Level Today". The gauge has labeled segments around its circumference: LOW-MODERATE, HIGH, VERY HIGH, SEVERE, EXTREME, and CATASTROPHIC. The needle is pointing directly at the red "CATASTROPHIC" segment on the far right.*

---

## Slide 77: Concepts greatly improve compiler errors

Here’s the error when instantiating a set **with** a concept

*Figure: A slide layout showing a compiler error message on the left, a code snippet box below it, and a meme image on the right.*

**Compiler Error Box:**
```text
main.cpp:32:3: error: constraints not satisfied for class template 'set' [with T = StanfordID]
    set<StanfordID> ids { jacob, fabio };
    ^~~~~~~~~~~~~~~~~~~~~
main.cpp:13:11: note: because 'StanfordID' does not satisfy 'Comparable'
template <Comparable T>
                   ^
main.cpp:10:7: note: because 'a < b' would be invalid: invalid operands to binary expression ('const StanfordID' and 'const StanfordID')
    { a < b } -> std::convertible_to<bool>;
            ^
4 errors generated.
```

*Figure: A meme image featuring a woman (Miriam "Midge" Maisel from the show *The Marvelous Mrs. Maisel*) sitting at a diner table. The hashtag #MrsMaisel is in the top left corner, and a white text caption at the bottom reads: "AWW GEE, THANKS".*

**Code Snippet:**
```cpp
template <Comparable T>
struct std::set;
```
*(Note: In the snippet, the word `Comparable` is highlighted in red on a yellow background.)*

---

## Slide 78: C++ comes with many built-in concepts

| Core language concepts | Defined in header `<concepts>` |
| :--- | :--- |
| `same_as` (C++20) | specifies that a type is the same as another type<br>(concept) |
| `derived_from` (C++20) | specifies that a type is derived from another type<br>(concept) |
| `convertible_to` (C++20) | specifies that a type is implicitly convertible to another type<br>(concept) |
| `common_reference_with` (C++20) | specifies that two types share a common reference type<br>(concept) |
| `common_with` (C++20) | specifies that two types share a common type<br>(concept) |
| `integral` (C++20) | specifies that a type is an integral type<br>(concept) |
| `signed_integral` (C++20) | specifies that a type is an integral type that is signed<br>(concept) |
| `unsigned_integral` (C++20) | specifies that a type is an integral type that is unsigned<br>(concept) |
| `floating_point` (C++20) | specifies that a type is a floating-point type<br>(concept) |
| `assignable_from` (C++20) | specifies that a type is assignable from another type<br>(concept) |
| `swappable`<br>`swappable_with` (C++20) | specifies that a type can be swapped or that two types can be swapped with each other<br>(concept) |

[source]

Links on this slide:
- <https://en.cppreference.com/w/cpp/concepts>

---

## Slide 79: …including iterator concepts!

| Concept | Description |
|---------|-------------|
| `input_iterator` (C++20) | specifies that a type is an input iterator, that is, its referenced values can be read and it can be both pre- and post-incremented (concept) |
| `output_iterator` (C++20) | specifies that a type is an output iterator for a given value type, that is, values of that type can be written to it and it can be both pre- and post-incremented (concept) |
| `forward_iterator` (C++20) | specifies that an `input_iterator` is a forward iterator, supporting equality comparison and multi-pass (concept) |
| `bidirectional_iterator` (C++20) | specifies that a `forward_iterator` is a bidirectional iterator, supporting movement backwards (concept) |
| `random_access_iterator` (C++20) | specifies that a `bidirectional_iterator` is a random-access iterator, supporting advancement in constant time and subscripting (concept) |
| `contiguous_iterator` (C++20) | specifies that a `random_access_iterator` is a contiguous iterator, referring to elements that are contiguous in memory (concept) |

[source]

*Figure: A Venn-diagram-style illustration of C++ iterator concept hierarchy. Multiple overlapping and concentric circles in shades of blue and pink represent the nested relationships between iterator concepts. Large, overlapping, partially transparent black text labels read "Bidirectional", "Random Access", "Output", "Forward", "Input", and "Contiguous", all jumbled on top of one another to suggest the layered/conceptual nature of the hierarchy.*

Remember our iterator types?

Links on this slide:
- <https://en.cppreference.com/w/cpp/iterator#Iterator_concepts_.28since_C.2B.2B20.29>

---

## Slide 80: Fixing up our find function

```cpp
template <std::input_iterator It, typename T>
It find(It begin, It end, const T& value);

int idx = find(1, 5, 3); // WHY DOES THIS NOT WORK?
```

```text
main.cpp:10:11: note: because 'int' does not satisfy 'input_iterator'
template <std::input_iterator It, typename T>
          ^
```

*Figure: A meme image of a Shiba Inu (Doge) with a smiling expression, overlaid with the text "AWWW THANKS" in white capital letters at the bottom.*

---

## Slide 81: Concepts recap

* Two reasons to use concepts
    * Better compiler error messages
    * Better IDE support (Intellisense/autocomplete, etc.)
* Concepts are still a new feature
    * STL does not yet support them fully
    * We’ll talk more about this on Thursday!

---

## Slide 82: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, creator of C++, looking thoughtfully at the camera with his hand resting on his chin. Behind him are bookshelves displaying copies of his books, including "The C++ Programming Language" and "Programming: Principles and Practice Using C++". The caption below the photo reads:*

`bjarne_about_to_raise_hand`

---

## Slide 83: Variadic Templates
Variadic Templates

---

## Slide 84: Variable Parameters Question

How do we create a function that accepts a **variable number** of parameters?

---

## Slide 85: Back to our min function

*Figure: A white box with a black border and a drop shadow containing C++ code for a template `min` function and three example calls.*

```cpp
template <Comparable T>
T min(const T& a, const T& b) {
    return a < b ? a : b;
}
```

min(2.4, 7.5);                // This works
min(2.4, 7.5, 5.3);          // What about this?
min(2.4, 7.5, 5.3, 1.2);     // or this?

---

## Slide 86: One solution: function overloading

```cpp
template <Comparable T>
T min(const T& a, const T& b) { return a < b ? a : b; }

template <Comparable T>
T min(const T& a, const T& b, const T& c) {
    auto m = min(b, c);
    return a < m ? a : m;
}

template <Comparable T>
T min(const T& a, const T& b, const T& c, const T& d) {
    auto m = min(b, c, d);
    return a < m ? a : m;
}
```

*Figure: A diagram illustrating function overloading for a `min` function. The code block shows three template functions. To the right, three annotation boxes are shown:*
*   *A box labeled "3 element overload calls 2 element" with an arrow pointing to the line `auto m = min(b, c);` in the second function.*
*   *A box labeled "4 element overload calls 3 element" with an arrow pointing to the line `auto m = min(b, c, d);` in the third function.*
*   *A box at the bottom right labeled "Seems almost recursive!".*

---

## Slide 87: One solution: function overloading

*Figure: A rectangular box with a drop shadow, containing lines of C++ code that call a `min` function with different numbers of floating-point arguments, along with comments and a rolling eyes emoji.*

```cpp
min(2.4, 7.5); // This works
min(2.4, 7.5, 5.3); // This works now
min(2.4, 7.5, 5.3, 1.2); // and this works too!
min(2.4, 7.5, 5.3, 1.2, 3.4, 6.7, 8.9, 9.1); 🙄
// Time to write 7 overloads I guess...
```

---

## Slide 88: Wait... Templates are all about code generation

Wait... Templates are all about <span style="color: red;">code generation</span>

*Figure: The slide displays a single sentence with the words "code generation" highlighted in red.*

---

## Slide 89: Can the compiler write the overloads for us?

Can the compiler write the overloads for us?

---

## Slide 90: Yes! Templates + recursion

Yes! Templates + recursion 🎉🤯

---

## Slide 91: But first... a (slightly) different solution

Can't we solve this recursively using `std::vector`!?

*Figure: A white box with a black border containing C++ code for a template function `min` that takes a constant reference to a `std::vector`, followed by three example function calls using uniform initialization.*

```cpp
template <Comparable T>
T min(const std::vector<T>& values);

// Passing a vector<double> here!
// Note the { } braces (uniform initialized vector)
min({ 2.4, 7.5 });
min({ 2.4, 7.5, 5.3 });
min({ 2.4, 7.5, 5.3, 1.2 });
```

---

## Slide 92: But first... a (slightly) different solution
Can’t we solve this recursively using `std::vector`!?

```cpp
template <Comparable T>
T min(const std::vector<T>& values) {
    if (values.size() == 1) return values[0];
    const auto& first = values[0];
    std::vector<T> rest(++values.begin(), values.end());
    auto m = min(rest);
    return first < m ? first : m;
}
```

*Note: Text box in the bottom right corner says: "Talk to a partner for 60s. How does this code work?"*

---

## Slide 93: But first... a (slightly) different solution

Can't we solve this recursively using `std::vector`!?

```cpp
template <Comparable T>
T min(const std::vector<T>& values) {
    if (values.size() == 1) return values[0];
    const auto& first = values[0];
    std::vector<T> rest(++values.begin(), values.end());
    auto m = min(rest);
    return first < m ? first : m;
}
```

*Figure: A callout box at the bottom right with a red heading that reads "Base Case:" followed by the text "if we only have one element, return that element!"*

---

## Slide 94: But first... a (slightly) different solution

Can't we solve this recursively using `std::vector`!?

*Figure: A C++ code snippet is presented within a white rectangular box with a black border. A smaller callout box, also with a black border, is positioned at the bottom right of the code box, partially overlapping its border.*

```cpp
template <Comparable T>
T min(const std::vector<T>& values) {
    if (values.size() == 1) return values[0];
    const auto& first = values[0];
    std::vector<T> rest(++values.begin(), values.end());
    auto m = min(rest);
    return first < m ? first : m;
}
```

**Recursive Case:** compare first element to min of remaining elements!

---

## Slide 95: What questions do you have?

What questions do you have?

bjarne_about_to_raise_hand

*Figure: A photograph of Bjarne Stroustrup, looking towards the camera with his hand resting near his mouth as if about to raise it. In the background, a poster displays his name "BJARNE STROUSTRUP" and the words "PROGRAMMING LANGUAGE".*

---

## Slide 96: But first... a (slightly) different solution

Can't we solve this recursively using `std::vector`!?

```cpp
template <Comparable T>
T min(const std::vector<T>& values) {
    if (values.size() == 1) return values[0];
    const auto& first = values[0];
    std::vector<T> rest(++values.begin(), values.end());
    auto m = min(rest);
    return first < m ? first : m;
}
```

This solution is correct. But does anyone see any **inefficiencies?**

*Figure: A slide with a large bold main title, a follow-up question with `std::vector` highlighted in red, a C++ code snippet enclosed in a rounded-corner box with a drop shadow, and a speech-bubble callout positioned to the right of the code box (pointing toward the code), with the text "inefficiencies?" highlighted in red.*

---

## Slide 97: Some problems with this approach...

* It recursively copies the vector (can avoid with wrapper function!)
* Must allocate a vector for every call (unavoidable overhead)

```cpp
template <Comparable T>
T min(const std::vector<T>& values);

// Passing a vector<double> here!
// Note the { } braces (list initialized vector)
min({ 2.4, 7.5 });
min({ 2.4, 7.5, 5.3 });
min({ 2.4, 7.5, 5.3, 1.2 });
```

---

## Slide 98: What we would like to have

*Figure: A code snippet box showing multiple calls to a `min` function with varying numbers of arguments, each with a comment indicating it works.*

```cpp
min(2.4, 7.5);                // This works
min(2.4, 7.5, 5.3);          // This works now
min(2.4, 7.5, 5.3, 1.2); // and this works too!

// This just works!
min(2.4, 7.5, 5.3, 1.2, 3.4, 6.7, 8.9, 9.1);
```

---

## Slide 99: Recall: function overloading

```cpp
template <Comparable T>
T min(const T& a, const T& b) { return a < b ? a : b; }

template <Comparable T>
T min(const T& a, const T& b, const T& c) {
    auto m = min(b, c);
    return a < m ? a : m;
}

template <Comparable T>
T min(const T& a, const T& b, const T& c, const T& d) {
    auto m = min(b, c, d);
    return a < m ? a : m;
}
```

*Figure: Three annotation boxes are positioned to the right of the code. The top box reads "3 element overload calls 2 element" and includes an arrow pointing left toward the signature of the three-argument `min` function. The middle box reads "4 element overload calls 3 element" and includes an arrow pointing left toward the signature of the four-argument `min` function. The bottom box contains the text "Seems almost recursive!".*

---

## Slide 100: Introducing... variadic templates

---

## Slide 101: Variadic Templates

```cpp
template <Comparable T>
T min(const T& v) { return v; }

template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

---

## Slide 102: Variadic Templates

*Figure: A text box with a black arrow pointing to the first function template definition. The text in the box reads: "Base case function: Needed to stop recursion". Below this, a large box contains two C++ function templates.*

```cpp
template <Comparable T>
T min(const T& v) { return v; }

template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

---

## Slide 103: Variadic Templates
```cpp
template <Comparable T>
T min(const T& v) { return v; }
```
*Figure: A callout box with red text "Base case function:" and black text "Needed to stop recursion", with an arrow pointing from the box to the code block above.*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

---

## Slide 104: Variadic Templates

*Figure: A large rectangular frame containing two C++ code snippets. A callout box in the upper right with an arrow points to the first code snippet. Another callout box in the middle right with an arrow points to the `Comparable... Args` portion of the second code snippet, which is highlighted in yellow.*

```cpp
template <Comparable T>
T min(const T& v) { return v; }

template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
  auto m = min(args...);
  return v < m ? v : m;
}
```

*Callout box pointing to the first snippet:*
**Base case function:**
Needed to stop recursion

*Callout box pointing to the second snippet's template arguments:*
**Variadic template:** matches 0
or more types

---

## Slide 105: Variadic Templates

```cpp
template <Comparable T>
T min(const T& v) { return v; }

template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

*Figure: An annotated code snippet demonstrating variadic templates in C++. An arrow from a box labeled "Base case function: Needed to stop recursion" points to the single-argument function template at the top. An arrow from a box labeled "Variadic template: matches 0 or more types" points to the template parameter list `<Comparable T, Comparable... Args>`. An arrow from a box labeled "Parameter pack: 0 or more parameters" points to the function parameter `const Args&... args`, which is highlighted with a yellow background.*

---

## Slide 106: Variadic Templates

```cpp
template <Comparable T>
T min(const T& v) { return v; }

template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

*Figure: A diagram illustrating variadic templates with two C++ function templates and several callout boxes explaining specific parts.*

*   *A callout box labeled "Base case function: Needed to stop recursion" has an arrow pointing to the first function template definition.*
*   *A callout box labeled "Variadic template: matches 0 or more types" has an arrow pointing to the `Comparable... Args` portion of the second function's template parameter list.*
*   *A callout box labeled "Parameter pack: 0 or more parameters" has an arrow pointing to the `args` variable in the second function's parameter list.*
*   *A callout box labeled "Pack expansion: replaces ...args with actual parameters" has an arrow pointing to the `args...` expression inside the function body, which is highlighted in yellow.*

---

## Slide 107: Variadic Templates

*Figure: The slide shows two C++ code blocks for variadic templates, with four annotated boxes containing red headings and black descriptions. Arrows point from each box to a specific part of the code. The overall layout explains the structure of variadic templates, including a base case, template parameter packs, and pack expansion.*

The base case function:

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

*Figure: An annotation box with the heading "Base case function:" and description "Needed to stop recursion" has an arrow pointing to the above code block.*

The variadic template function:

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

*Figure: An annotation box with the heading "Variadic template:" and description "matches 0 or more types" has an arrow pointing to the template parameter list `<Comparable T, Comparable... Args>` in the second code block.*

*Figure: An annotation box with the heading "Parameter pack:" and description "0 or more parameters" has an arrow pointing to the `args...` parameter in the function signature of the second code block.*

*Figure: An annotation box with the heading "Pack expansion:" and description "replaces ...args with actual parameters" has an arrow pointing to the `args...` in the recursive call `min(args...);` within the second code block.*

---

## Slide 108: Phew… this is a lot to unpack

(pun intended)

---

## Slide 109: What’s going on?

### Recursive Case:
```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

### Base Case:
```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min(2, 7, 5, 1)
```

*Figure: A diagram with two connected text boxes. The right box poses the question "What happens when the compiler sees a function call like this?"; an arrow points from this box to the left box, which contains the text "Implicit instantiation!"*

---

## Slide 110: What's going on?

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)

template <Comparable T>
T min(const T& v) { return v; }

min<int, int, int, int>(2, 7, 5, 1)
```

*Figure: A diagram illustrating variadic template recursion for a `min` function. Two stacked boxes at the top show two overloads: a variadic template accepting a first argument `v` of type `T` and a parameter pack `args` of type `Args...`, and a base-case template accepting a single argument `v` of type `T` that simply returns `v`. Below, a box shows a call `min<int, int, int, int>(2, 7, 5, 1)`. A black arrow points from this call to a box on the right showing the template argument deduction: `T = int` and `Args = [int, int, int]`. At the bottom, a larger box shows the implementation of the variadic template overload:*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

*The arrow indicates that the call `min<int, int, int, int>(2, 7, 5, 1)` deduces `T = int` as the type of the first argument and `Args = [int, int, int]` as the parameter pack for the remaining three arguments.*

---

## Slide 111: What’s going on?

*Figure: Several boxes containing C++ code snippets illustrating the instantiation of a variadic template function. At the top is a light-green box containing the function signature. Below it is a white box showing the base case for a single argument. A function call is positioned in the middle, with an arrow pointing from it to a small callout box on the right that shows the deduced template arguments. A larger white box at the bottom contains the recursive body of the variadic template function.*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min<int, int, int, int>(2, 7, 5, 1)
```

*Figure: An arrow points from the function call to a box showing the deduced template arguments:*
```cpp
T = int
Args = [int, int, int]
```

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

---

## Slide 112: What’s going on?

*Figure: A diagram illustrating the template instantiation and recursive step of a variadic template function. At the top, a green box contains the signature for the variadic `min` function. Below it, a white box shows the base case template for a single argument. On the left, a function call is shown in a white box, with a black arrow pointing to a box on the right that displays the deduced template parameters. At the bottom, a large white box contains the instantiated code for the function, with several instances of the word "int" highlighted in yellow to show type substitution.*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min<int, int, int, int>(2, 7, 5, 1)
```

*An arrow points from the function call to the following template parameters:*

*   T = int
*   Args = [int, int, int]

```cpp
template <Comparable... Args>
int min(const int& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

---

## Slide 113: What’s going on?

**What’s going on?**

*Figure: The slide illustrates template specialization and parameter pack expansion for a recursive `min` function. It contains several code boxes and two annotation boxes linked by arrows.*

### Function Declarations

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

### Example Function Call

```cpp
min<int, int, int, int>(2, 7, 5, 1)
```

*Figure: An arrow points from the function call above to a box explaining the resulting template arguments:*

```cpp
T = int
Args = [int, int, int]
```

### Recursive Implementation

```cpp
template <Comparable... Args>
int min(const int& v, const Args&... args) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

*Figure: An arrow points from the `args...` expansion in the code to an annotation box:*

```cpp
Pack expansion: Args is
expanded
```

---

## Slide 114: What’s going on?

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min<int, int, int, int>(2, 7, 5, 1)
```

*Figure: A diagram showing the call `min<int, int, int, int>(2, 7, 5, 1)` with a thick black arrow pointing to a box indicating template parameter deduction: `T = int` and `Args = [int, int, int]`.*

```cpp
template <Comparable... Args>
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

---

## Slide 115: What’s going on?

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min<int, int, int, int>(2, 7, 5, 1)
```

*Figure: An arrow points from the function call to a text box showing the type arguments:*
`T = int`
`Args = [int, int, int]`

```cpp
template <Comparable... Args>
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(args...);
    return v < m ? v : m;
}
```

*Figure: An arrow points from the `args...` call to an annotation box:*
**Pack expansion: args is expanded**

---

## Slide 116: What’s going on?

*Figure: A diagram illustrating the instantiation of a variadic template function. A green box at the top contains the template declaration. Below it, a white box shows the base case template. A function call box points with an arrow to a template argument list box. At the bottom, a larger white box shows the instantiated function body. The arrow originates from the function call and points to the template arguments, indicating how the types are deduced.*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min<int, int, int, int>(2, 7, 5, 1)
```

*The arrow points to a box containing:*
`T = int`
`Args = [int, int, int]`

*Below, the instantiated function is shown:*
```cpp
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(a0, a1, a2);
    return v < m ? v : m;
}
```

---

## Slide 117: What’s going on?

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
template <Comparable T>
T min(const T& v) { return v; }
min<int, int, int, int>(2, 7, 5, 1)
```

*Figure: A diagram illustrating template instantiation. A black arrow points from the function call `min<int, int, int, int>(2, 7, 5, 1)` to a box showing the deduced template arguments. The arrow points from the left (the call site) to the right (the argument box).*

T = int
Args = [int, int, int]

```cpp
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(a0, a1, a2);
    return v < m ? v : m;
}
```

What did we just generate?

---

## Slide 118: What’s going on?

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

*Figure: A diagram illustrating template instantiation and code generation. A white box containing the function call `min<int, int, int, int>(2, 7, 5, 1)` has an arrow pointing to a small white box showing the template parameter assignments:*
```text
T = int
Args = [int, int, int]
```
*An arrow points from the parameter box down to a large white box containing a generated function overload:*
```cpp
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(a0, a1, a2);
    return v < m ? v : m;
}
```
*Overlapping this large box is a callout box that states:*
Voila! The compiler **generated an overload** for us!!!

---

## Slide 119: What’s going on?

### Variadic Template
```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

### Non-Variadic (Base Case) Template
```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

### Function Call & Template Instantiation
`min<int, int, int, int>(2, 7, 5, 1)`  

*Annotation:*  
T = int  
Args = [int, int, int]  


### Expanded Instantiation (for `int`)
```cpp
int min(const int& v, const int& a0, const int& a1, const int& a2) {
    auto m = min(a0, a1, a2);
    return v < m ? v : m;
}
```

*Annotation:*  
Wait… what is this?  
It’s another template instantiation!

---

## Slide 120: What’s going on?

*Figure: A diagram showing the expansion of a variadic template function call. At the top is a code box containing two template function declarations and a function call. A black arrow points from the function call to a box on the right detailing the template arguments. Below, another black arrow points from a line within the expanded function to a box with a comment. The diagram illustrates how the variadic template `min` is instantiated.*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)

template <Comparable T>
T min(const T& v) { return v; }

min<int, int, int>(a0, a1, a2);
```

*Annotations:*
- A box connected by an arrow from the function call shows: `T = int`, `Args = [int, int]`.
- A box connected by an arrow from a line in the expanded function says: `Hey look! Another template instantiation`.

```cpp
int min(const int& v, const int& a0, const int& a1) {
    auto m = min(a0, a1);
    return v < m ? v : m;
}
```

---

## Slide 121: What’s going on?

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

```cpp
min<int, int>(a0, a1);
```

*Figure: An arrow points from the function call `min<int, int>(a0, a1);` to a box containing the template argument deductions: `T = int` and `Args = [int]`.*

```cpp
int min(const int& v, const int& a0) {
    auto m = min(a0);
    return v < m ? v : m;
}
```

*Figure: An arrow points from the call `min(a0)` inside the function body to a box containing the annotation: "Hey look! Another template instantiation".*

```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

---

## Slide 122: What’s going on?

✅ Compiler always tries to choose most specific template

*Figure: A diagram showing C++ template overload resolution. Two template functions are defined in boxes on the left. To their right are boxes showing the deduced template arguments for each. Below these is a box containing a function call, `min<int>(a0);`, with arrows pointing from the call to both deduction boxes. At the bottom, a large box displays the final instantiated function chosen by the compiler, with the `int` type highlighted in yellow.*

### Template Definitions
```cpp
template <Comparable T, Comparable... Args>
T min(const T& v, const Args&... args)
```

```cpp
template <Comparable T>
T min(const T& v) { return v; }
```

### Deduced Template Arguments
*   For the first template: `T = int`, `Args = []`
*   For the second template: `T = int`

### Function Call
```cpp
min<int>(a0);
```

### Selected Instantiation
```cpp
int min(const int& v) {
    return v;
}
```

---

## Slide 123: What just happened?

A single call to min(2, 7, 5, 1) generated the following functions

```cpp
min(2, 7, 5, 1);

min<int, int, int, int> // T = int, Args = [int, int, int]
min<int, int, int>       // T = int, Args = [int, int]
min<int, int>            // T = int, Args = [int]
min<int>                 // T = int
```

*Figure: A rectangular bordered box with a shadow effect, displaying a C++ code snippet that shows a function call to min(2, 7, 5, 1) and lists the generated template functions with their type parameters and argument packs.*

---

## Slide 124: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, creator of C++, looking at the camera with his hand near his chin in a thoughtful pose. Behind him, a poster with "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP" is visible on the wall, next to what appears to be a computer monitor.*

bjarne_about_to_raise_hand

---

## Slide 125: Variadic types don’t have to be the same

*   In this example, all the T’s were the same
*   In practice, they don’t have to be
*   For example, imagine a printf-style function like so:
    *   `format("Queen {}, Protector of the {} Kingdoms", "Rhaenyra", 7);`
    *   The {}’s get filled in with arbitrary number/type of arguments

---

## Slide 126: Variadic types don’t have to be homogeneous
Imagine we wanted to implement a f-string printer, a la Python

```cpp
format("Queen {}, Protector of the {} Kingdoms", "Rhaenyra", 7);
// Prints: Queen Rhaenyra, Protector of the 7 Kingdoms

std::cout << std::boolalpha;
format("The {} enemy won't {} out the {}", true, "wait", "storm");
// Prints: The true enemy won't wait out the storm

format("Winter is coming");
// Prints: Winter is coming
```

*Figure: Diagram showing the types of the variadic arguments. Arrows point from the function arguments in the first example to type labels: an arrow from "Rhaenyra" points to a box labeled `std::string`, and an arrow from `7` points to a box labeled `int`. Arrows point from the function arguments in the second example to type labels: an arrow from `true` points to a box labeled `bool`, and arrows from "wait" and "storm" point to a box labeled `std::string`.*

---

## Slide 127: We can’t just use a vector…
What would the underlying type of the vector be?

```cpp
template <typename T>
void format(const std::string& fmt, std::vector<T> args) {
    // ...
}

format("{} {}", { true, "facts" });
// ❌ No common type for vector
```

*Figure: A code box showing a template function `format` that takes a vector of type `T`, and an example call with mixed types `true` and `"facts"` that fails with the comment "No common type for vector". A callout text box notes: "Sure, this works if all the arguments share the same type, but not if we want different types."*

---

## Slide 128: Implementing format

```cpp
void format(const std::string& fmt) {
    std::cout << fmt << std::endl;
}

template <typename T, typename... Args>
void format(const std::string& fmt, T value, Args... args) {
    auto pos = fmt.find("{}");
    if (pos == std::string::npos) throw std::runtime_error("Extra arg");
    std::cout << fmt.substr(0, pos);
    std::cout << value;
    format(fmt.substr(pos + 2), args...);
}
```

---

## Slide 129: What happens when we instantiate format?

```cpp
format("Lecture {}: {} (Week {})", 9, "Templates", 5);

format<int, std::string, int>()
// T = int, Args = [std::string, int]

format<std::string, int>()
// T = std::string, Args = [int]

format<int>()
// T = int, Args = []

format()
// Base case! Not a template, no type arguments
```

---

## Slide 130: Variadic templates recap

*   Compiler generates any number of overloads using recursion
    *   This allows us to support any number of function parameters
*   Instantiation happens at compile time

*Figure: A black arrow points from the text "at compile time" towards a white rectangular box with a drop shadow on the right. The box contains the text: "Templates do work at compile time. Can we use this to our advantage?"*

---

## Slide 131: Template Metaprogramming

---

## Slide 132: How can we do work at compile time?

How can we do work at **compile time**?

---

## Slide 133: TMP Basics: Factorial

```cpp
template <>
struct Factorial<0> {
    enum { value = 1 };
};

template <size_t N>
struct Factorial {
    enum { value = N * Factorial<N - 1>::value };
};

std::cout << Factorial<7>::value << std::endl;
```

Base Case:  
This is a template specialization for N=0

enum: a way to store a  
compile-time constant

Oooh compile-time recursion

Prints **5040**, but computes at compile time

*Figure: A black arrow points from a rectangular box containing the text "Base Case: This is a template specialization for N=0" to the first code block showing the template specialization `struct Factorial<0>`.*

*Figure: A red arrow points from a red-outlined box highlighting the word `enum` in the first code block to a rectangular box containing the text "enum: a way to store a compile-time constant".*

*Figure: A black arrow points from a rectangular box containing the text "Oooh compile-time recursion" to the second code block showing the general recursive template `struct Factorial`.*

*Figure: A rectangular box containing the text "Prints 5040, but computes at compile time" is positioned below the line of code `std::cout << Factorial<7>::value << std::endl;`.*

---

## Slide 134: Template instantiations for Factorial<7>

*Figure: A diagram illustrating the template instantiation and recursive evaluation of Factorial<7>. A series of tan rectangular boxes are arranged diagonally from the top left to the bottom right, labeled "Factorial<7>", "Factorial<6>", "Factorial<5>", "Factorial<4>", "Factorial<3>", "Factorial<2>", "Factorial<1>", and "Factorial<0>". The "Factorial<0>" box is colored light red. Red arrows point downwards and to the right from each box to the next (e.g., from Factorial<7> to Factorial<6>), indicating recursive template instantiation. Black arrows point upwards and to the left from each box back to the previous one (e.g., from Factorial<0> to Factorial<1>), indicating the return of computed values. To the left of each box is a text label indicating the returned value: "value = 5040" next to Factorial<7>, "value = 720" next to Factorial<6>, "value = 120" next to Factorial<5>, "value = 24" next to Factorial<4>, "value = 6" next to Factorial<3>, "value = 2" next to Factorial<2>, "value = 1" next to Factorial<1>, and "value = 1" next to Factorial<0>. A white box in the bottom left corner contains the text: "All of this happens at compile-time!".*

All of this happens at **compile-time**!

---

## Slide 135: Output assembly of Factorial<7>

*Figure: Two side-by-side code boxes. The left box contains C++ source code, and the right box contains the corresponding x86-64 assembly code. A callout box at the bottom right has an arrow pointing specifically to the value `5040` in the assembly code, which is highlighted in yellow.*

*Figure: Callout box at bottom right. Text: "Result is **baked in** to the executable". An arrow points from this box to the immediate value `5040` in the assembly instruction `mov esi, 5040`.*

*Figure: Left box - C++ source code:*
```cpp
int main() {
    std::cout << Factorial<7>::value;
    return 0;
}
```

*Figure: Right box - x86-64 assembly output:*
```asm
main:
    push rax
    mov edi, offset cout
    mov esi, 5040
    call ostream::operator<<(int)
    xor eax, eax
    pop rcx
    ret
```

---

## Slide 136: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup. He is wearing glasses and a patterned shirt, with his hand resting on his chin in a thoughtful pose. Below the image, the text `bjarne_about_to_raise_hand` is written in a monospaced font.*

---

## Slide 137: Another example: Fibonacci

```cpp
template <>
struct Fibonacci<0> {
    enum { value = 0 };
};

template <>
struct Fibonacci<1> {
    enum { value = 1 };
};

template <size_t N>
struct Fibonacci {
    enum { value = Fibonacci<N - 1>::value + Fibonacci<N - 2>::value };
};
```

---

## Slide 138: What is TMP?

---

## Slide 139: How is TMP used in the real world?

* Baking results into an executable at compile time (e.g. factorial)
* Optimizing matrices/trees/other mathematical structures
* Policy-based design: passing around behaviour through templates
* Boost MPL library

---

## Slide 140: TMP allows programming for types

The **boost::mpl** library is a popular library for metaprogramming

*Figure: A code snippet contained within a white box with annotations. An arrow points from a callout box containing "This is a vector of **TYPES!!!**" to the code line `using Move = mpl::vector<MoveUp, MoveRight>;`. A second arrow points from a callout box containing "Compiler generates code specific to the transformations" to the function calls at the bottom of the code block.*

```cpp
using namespace boost;

using Move = mpl::vector<MoveUp, MoveRight>;
using MoveRotate = mpl::push_back<Move, Rotate45>::type;

template <typename Transformations>
void apply(Object&);

apply<Move>(object); // move object up and right
apply<MoveRotate>(object); // move object up/right, rotate 45deg
```

---

## Slide 141: TMP is Turing complete

TMP is Turing complete

---

## Slide 142: Compile-time Code Execution

We can execute **arbitrary code** at compile time

*Figure: The phrase "arbitrary code" is highlighted in red within the sentence.*

---

## Slide 143: But the syntax is not always pretty...

```cpp
template< >
struct push_back_impl< aux::vector_tag<BOOST_PP_DEC(i_)> >
{
    template< typename Vector, typename T > struct apply
    {
        typedef BOOST_PP_CAT(vector,i_)<
            BOOST_PP_ENUM_PARAMS(BOOST_PP_DEC(i_), typename Vector::item)
            BOOST_PP_COMMA_IF(BOOST_PP_DEC(i_))
            T
            > type;
    };
};
```

*Figure: A "One Does Not Simply" meme featuring Boromir from The Lord of the Rings. The top text reads "ONE DOES NOT SIMPLY" and the main bottom text reads "LEARN TEMPLATE META-PROGRAMMING". A smaller caption below states "NOT SINCE A PURE FUNCTIONAL PROGRAMMING LANGUAGE WAS FOUND INSIDE OF THE C++ COMPILER'S TEMPLATE MECHANISM".*

---

## Slide 144: How can we have
**How can we have**
1) Compile-time execution
   2) Readable code

---

## Slide 145: Instead of this...

```cpp
template <>
struct Factorial<0> {
    enum { value = 1 };
};

template <size_t N>
struct Factorial {
    enum { value = N * Factorial<N - 1>::value };
};

std::cout << Factorial<7>::value << std::endl;
```

---

## Slide 146: Use constexpr/consteval

An institutionalization of template metaprogramming (new in C++20)

```cpp
constexpr size_t factorial(size_t n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```

*Figure: An annotation box with a left-pointing arrow pointing to the `constexpr` code block. The box contains the heading "constexpr" and the text: "Dear compiler, please try to run me at compile time 😘".*

```cpp
consteval size_t factorial(size_t n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```

*Figure: An annotation box with a left-pointing arrow pointing to the `consteval` code block. The box contains the heading "consteval" and the text: "Dear compiler, YOU MUST RUN ME AT COMPILE TIME 🤬🤬".*

---

## Slide 147: What questions do you have?

# What questions do you have?

*Figure: A photo of Bjarne Stroustrup in a patterned shirt, looking thoughtful with his hand to his chin. The large text "What questions do you have?" is superimposed across the center of the image. Below the image, the text "bjarne_about_to_raise_hand" is written in a monospace font.*

bjarne_about_to_raise_hand

---

## Slide 148: Recap
Recap

---

## Slide 149: When should I use templates?

*   I want the compiler to automate a repetitive coding task
    *   Template functions, variadic templates
*   I want better error messages
    *   Concepts
*   I don’t want to wait until runtime
    *   Template metaprogramming, constexpr/consteval

---

## Slide 150: Next Time: Functions and Algorithms
Next Time: **Functions and Algorithms**
Writing smarter, more flexible algorithms
