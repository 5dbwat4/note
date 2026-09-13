# Lecture 02: TypesAndStructs (2026Spring)

> PDF title: 2025Fall-02-TypesAndStructs.pptx
> Source: `assets/slides/2026Spring-02-TypesAndStructs.pdf` · 102 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Lecture 2: Types and Structs

Stanford CS106L, Spring 2026
Rachel Fernandez & Preston Seay

*Figure: A flowchart diagram titled "Data Type in C++". The main title branches into three colored categories. On the left, a yellow box labeled "Basic Data Types" lists: int, float, double, char, bool, void. In the middle, a light blue box labeled "Derived Data Types" lists: array, pointer, reference, function. On the right, a pink box labeled "User Defined Data Types" lists: class, structure, union, typedef, using.*

*Figure: A box containing C++ code that demonstrates defining and using a struct. The code is shown inside a white rectangle with a thin border.*

```cpp
int main() {
    struct {
        string brand;
        string model;
        int year;
    } myCar1, myCar2;

    myCar1.brand = "BMW";
    myCar1.model = "X5";
    myCar1.year = 1999;
```

---

## Slide 2: Last Lecture

*   Introductions!
*   Why you should take 106L?
*   Evolution of C++
*   Course Logistics

*Figure: A representation of the title slide from the first lecture, titled "Lecture 1: Welcome to CS106L!". Below the title, it lists the course as "CS106L, Spring 2026" and the instructors as "Rachel Fernandez & Preston Seay".*

---

## Slide 3: Slides are available at...

cs106l.stanford.edu

Links on this slide:
- <http://cs106l.stanford.edu/>

---

## Slide 4: What’s one thing you remember from last lecture?

- **What’s one thing you remember from last lecture?**  
- *Pair up and discuss!*  


*Figure (left):* A photograph of a green and blue parrot (perched on a hand) with a speech bubble containing:  
```
also discuss  
what is your  
spirit animal??  
```  


*Figure (right):* An image of Batman (animated character in a blue costume/black mask) with a thought bubble containing the C++ logo (a blue hexagon with white "C++" text inside).  


*(Note: The parrot’s background shows a room with a fan, shelves, and desk items; Batman’s background is a purple-toned animated scene.)*

---

## Slide 5: Today’s Agenda

*   Compile Time vs Run Time
*   Statically Typed Languages
*   Structs
*   The STD
*   Code demo
*   Improving our code with `auto` and `using`

*Figure: A small meme image of a dog looking startled, with the text "DUHN DUNN DUNNN!!!" printed at the bottom. It is placed over the "Structs" and "The STD" bullet points.*

---

## Slide 6: We'll cover a LOT of material in this class
We'll cover a LOT of material in this class
Please ask questions!!!

---

## Slide 7: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup sitting in front of computer monitors. He is looking directly at the camera with a neutral expression, his chin resting on his hand. In the background, a monitor displays a document with the heading "History and Practice Using C++". A poster to the right of the monitor shows the name "BJARNE STROUSTRUP" and the words "PROGRAMMING LANGUAGE".*

What questions do you have?

`bjarne_about_to_raise_hand`

---

## Slide 8: Compiler VS Interpreter

Let’s jump into!
Compiler VS Interpreter

---

## Slide 9: Interpreted Languages

*Figure: A flow diagram illustrating the process of an interpreted language. A series of four boxes are connected by orange arrows pointing from left to right. The first box is labeled "Source Code" and contains a code snippet. The second is an orange box labeled "Interpreter". The third is labeled "Machine Code" and contains a binary string. The fourth is labeled "Output" and contains a terminal-style window.*

**Source Code**:
```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

**Interpreter**

**Machine Code**:
10110101

**Output**:
```
Hello World
```

---

## Slide 10: Interpreted Languages

*Figure: A flowchart diagram illustrating the process of executing code in an interpreted language. Four boxes are connected by thick orange arrows pointing from left to right. The first box is labeled "Source Code," pointing to a central box labeled "Interpreter." The Interpreter box points to a "Machine Code" box, which in turn points to an "Output" window. The Output window is depicted as a terminal interface with several small icons (copy, download, refresh, terminal prompt, and expansion) along its left sidebar.*

### Source Code
```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

### Interpreter

### Machine Code
```
10110101
01011010
```

### Output
```
Hello World
Welcome to
```

---

## Slide 11: Interpreted Languages

*Figure: A flowchart illustrating the process of an interpreted language. A box labeled "Source Code" contains a code snippet. Orange arrows point from this box to a central box labeled "Interpreter". Three more orange arrows point from the "Interpreter" box to a box labeled "Machine Code" containing binary numbers. Finally, three orange arrows point from the "Machine Code" box to a console window labeled "Output", showing the results of the code execution.*

### Source Code

```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

### Machine Code

```
10110101
01011010
10011101
```

### Output

```
Hello World
Welcome to
```

---

## Slide 12: Interpreted Languages

*Figure: A flowchart diagram illustrating the process of an interpreted language. Three main sections are connected by light orange arrows flowing from left to right: "Source Code" on the left, "Interpreter" in the middle, and "Machine Code" and "Output" on the right.*

**Source Code** box contains:
```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

*The arrows from the "Source Code" box point to a tan-colored rectangle labeled "Interpreter". Multiple arrows then point from the "Interpreter" box to the "Machine Code" box, and finally from the "Machine Code" box to the "Output" terminal window.*

**Machine Code** box contains:
```
10110101
01011010
10011101
10110001
```

**Output** terminal window contains:
```
Hello World
Welcome to 
C
S
1
0
6
L
```

---

## Slide 13: Interpreted Languages

*Figure: A flow diagram showing the process of an interpreted language. On the left, a "Source Code" box contains a code snippet. Arrows point from this box into a central tan-colored box labeled "Interpreter." Arrows then point from the Interpreter into a "Machine Code" box containing binary data, and finally into a terminal-style "Output" window on the right. The Output window has several icons on its left-hand side (copy, download, settings, minimize, expand).*

**Source Code**

```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

**Machine Code**

```
10110101
01011010
10011101
10110001
```

**Output**

```
Hello World
Welcome to 
C
S
1
0
6
L
```

### 🧠 THE BIG IDEA 🧠

The interpreted languages read each line of code 
**line-by-line**, **translate** each line, and then **execute** it

---

## Slide 14: Compiled Languages

*Figure: A diagram illustrating the compilation process. On the left, a box labeled "Source Code" contains a C++ code snippet. An arrow points from the source code box to a central box labeled "Compiler". Another arrow points from the compiler to a box on the right labeled "Machine Code", which contains a list of binary numbers.*

### Source Code
```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

### Compiler

### Machine Code
```
10110101
01011010
10011101
10110001
```

---

## Slide 15: Compiled Languages

### Source Code
```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

*Figure: A flow diagram illustrating the compilation process of a compiled language. The "Source Code" box points to a central "Compiler" block, which in turn points to a "Machine Code" box. The "Machine Code" box points to an "Executable File" icon labeled "main".*

### Machine Code
10110101
01011010
10011101
10110001

### Executable File
*Figure: An icon representing an executable file, featuring the text "exec" in green on a dark background. The filename "main" is written below the icon.*

---

## Slide 16: Compiled Languages

*Figure: A flow diagram illustrating the compilation process. It begins with a box labeled "Source Code" containing a C++ code snippet. An arrow points from this box to a central box labeled "Compiler". A second arrow points from the "Compiler" to a box labeled "Machine Code" containing four rows of binary digits. A third arrow points from the machine code to an "Executable File" represented by a black terminal icon with "exec" inside and the label "main" below it.*

```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

```text
10110101
01011010
10011101
10110001
```

*Figure: A second flow diagram illustrating program execution. The "Executable File" (terminal icon labeled "exec" with the label "main" below) points via an arrow to a box labeled "Output". The "Output" box contains a screenshot of a console window displaying the program's results.*

```text
Hello World
Welcome to
C
S
1
0
6
L
```

---

## Slide 17: Compiled Languages

*Figure: A diagram illustrating the compilation and execution process. The diagram is enclosed in a light gray border and shows the flow from Source Code to Compiler to Machine Code to Executable File, and finally to Output. Large orange arrows indicate the direction of the process. The Executable File is represented by a window icon containing the word 'exec' and is labeled 'main'. The Output is shown in a terminal window with UI buttons for clear, reload, and close.*

### Source Code
```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

### Machine Code
```
10110101
01011010
10011101
10110001
```

### Output
```
Hello World
Welcome to
C
S
1
0
6
L
```

### 🧠 THE BIG IDEA 🧠

The compiler translates the **ENTIRE** program, packages it into an **executable file**, and then **executes** it

---

## Slide 18: Compiled Languages: Compile Time V.S. Run Time

🖥 **Compile Time** 🖥
*Figure: A diagram with a blue background representing the compile-time process. It shows a flow from left to right: a "Source Code" box contains C++ code, which points via an arrow to a tan box labeled "Compiler". The compiler points via another arrow to a "Machine Code" box containing four lines of binary digits. Each arrow indicates the transformation step.*

### Source Code
```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

### Machine Code
```
10110101
01011010
10011101
10110001
```

🏃 **Run Time** 🏃
*Figure: A diagram with a green background representing the run-time process. It continues the flow from the compile-time section. An arrow points from the "Machine Code" box to a black rectangle representing an "Executable File" labeled "exec" with the word "main" below it. Another arrow points from this executable to an "Output" window showing printed text. Small icons of a running person are next to the "Run Time" header.*

### Output
*The Output window displays the following text:*
```
Hello World
Welcome to
C
S
1
0
6
L
```

---

## Slide 19: Interpreted Languages: Compile Time V.S. Run Time

🏃 Run Time 🏃

*Figure: A diagram illustrating the run-time process for an interpreted language. A green-bordered box contains the flow. It starts with a "Source Code" box, points to an "Interpreter" box, which then points to "Machine Code" which finally points to an "Output" section represented as a terminal window.*

The flow is as follows:
1.  **Source Code** (a box containing code):
```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```
2.  Arrows point from the Source Code to the **Interpreter** (an orange box).
3.  Arrows point from the Interpreter to **Machine Code** (a box containing binary):
    *   10110101
    *   01011010
    *   10011101
    *   10110001
4.  Arrows point from the Machine Code to the **Output** (a window resembling a terminal/console):
    *   Hello World
    *   Welcome to
    *   C
    *   S
    *   1
    *   0
    *   6
    *   L

---

## Slide 20: Interpreted Languages: Compile Time V.S. Run Time

🏃 Run Time 🏃

*Figure: A diagram illustrating the execution process for interpreted languages on a green background. It shows a "Source Code" box containing Python code on the left, with arrows pointing to an "Interpreter" box in the middle. From the Interpreter, arrows point to a "Machine Code" box containing binary strings, and from there, arrows point to an "Output" box on the right displaying the program's output. Each box is labeled above it: "Source Code", "Machine Code", and "Output". The diagram uses orange arrows to connect the components.*

Source Code:
```python
print("Hello World")
print("Welcome to ")
for ch in "CS106L":
    print(ch)
```

Machine Code:
```
10110101
01011010
10011101
10110001
```

Output:
```
Hello World
Welcome to
C
S
1
0
6
L
```

### 🧠 THE BIG IDEA 🧠

Interpreted languages all run in run time!  
Compiled Languages run in first compile time then run time

---

## Slide 21: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, wearing glasses and a patterned sweater, with his hand under his chin in a thoughtful pose. In the background, posters are visible, one of which reads "BJARNE STROUSTRUP". The image is captioned below with the text `bjarne_about_to_raise_hand`.*

---

## Slide 22: C++ is a compiled language

C++ is a compiled language

---

## Slide 23: Q1: C++ Code Execution and Errors

**Q1:** So we know the process of how C++ runs our code…

But when **do we deal with errors?**

---

## Slide 24: Python vs C++

### Python
```python
print("Running...")
hello = "Hello ";
world = "World!";
print(hello * world)
```
*Terminal output from running the Python script:*
```bash
$ python3 program.py

Running...
TypeError: can't multiply sequence by
non-int of type 'str'
```

### C++
```cpp
int main() {
    std::cout << "Running..." << std::endl;
    std::string hello = "Hello ";
    std::string world = "World!";
    std::cout << hello * world << std::endl;
    return 0;
}
```
*Terminal output from compiling the C++ code:*
```bash
$ g++ main.cpp

error: no match for 'operator*' (operand types are
'std::string’ and ‘std::string’)
```

---

## Slide 25: Python

*Figure: A diagram depicting the flow from source code to execution. Three boxes are arranged horizontally, connected by two large orange arrows pointing from left to right. The leftmost box contains Python source code. The middle box contains four lines of binary digits. The rightmost box contains the text "Running...".*

```python
print("Running...")
hello = "Hello"
world = "World!"
print(hello * world)
```

10110101
01011010
10011101
10110001

Running...

---

## Slide 26: Python

```python
print("Running...")
hello = "Hello"
world = "World!"
print(hello * world)
```

*Figure: A diagram illustrating the process from Python source code to binary and final output. A large box on the left contains the code snippet above. Two thick orange arrows point from the first two lines of the code (the print statement and the variable assignments) toward a middle box containing four rows of binary numbers. Two more orange arrows point from this binary box to a final box on the right containing the output text.*

**Binary box content:**
10110101
01011010
10011101
10110001

**Output box content:**
Running...

---

## Slide 27: Python

*Figure: A diagram illustrating the execution of a Python program. The diagram consists of three rectangular boxes connected by three thick orange arrows pointing from left to right. The left box contains a code snippet. The middle box contains four lines of binary digits. The right box contains the text of the program's output. The flow suggests the code is translated into binary instructions which then produce the final output.*

```python
print("Running...")
hello = "Hello"
world = "World!"
print(hello * world)
```

10110101
01011010
10011101
10110001

Running...

---

## Slide 28: Python

*Figure: A diagram illustrating the execution of a Python script. Three rectangular boxes are connected by thick, light-orange arrows. The left box contains a Python script, the middle box shows four lines of binary code, and the right box displays the output and a runtime error. Arrows point from each line of the Python code to the binary numbers, and from the binary numbers to the corresponding output.*

```python
print("Running...")
hello = "Hello"
world = "World!"
print(hello * world)
```

**Output:**
```
Running...
TypeError:
can't
multiply
sequence
by non-int
of type
'str'
```

---

## Slide 29: Python

```python
print("Running...")
hello = "Hello ";
world = "World!";
print(hello * world)
```

### Run Time Error

```
$ python3 program.py

Running...
TypeError: can't multiply sequence by
non-int of type 'str'
```

*Figure: A disappointed face emoji (😔) is placed below the terminal output, emphasizing the error condition.*

---

## Slide 30: C++

*Figure: A stick figure is looking up at a speech bubble containing the question: "Any guesses for when this error occurs? Run time or compile time?" To the right are two boxes: a light green box at the top containing a C++ program, and a white box at the bottom containing a command-line instruction.*

### C++

```cpp
int main() {
    std::cout << "Running..." << std::endl;
    std::string hello = "Hello ";
    std::string world = "World!";
    std::cout << hello * world << std::endl;
    return 0;
}
```

```
$ g++ main.cpp
```

---

## Slide 31: C++ Compile Time Error

🧠 **THE BIG IDEA** 🧠
This error occurs during **compile time!**

When we are translating, we see that we try to multiply two strings and the compiler goes “hey that’s not allowed!!”

### C++

```cpp
int main() {
    std::cout << "Running..." << std::endl;
    std::string hello = "Hello ";
    std::string world = "World!";
    std::cout << hello * world << std::endl;
    return 0;
}
```

**Compile Time Error**

$ g++ main.cpp

*error*: no match for 'operator*' (operand types are 'std::string' and 'std::string')

*Figure: A small meme image of a young child holding their head in frustration, placed next to the error message.*

---

## Slide 32: Python vs C++ Errors

### Python

```python
print("Running...")
hello = "Hello ";
world = "World!";
print(hello * world)
```

#### Run Time Error

```
$ python3 program.py

Running...
TypeError: can't multiply sequence by
non-int of type 'str'
```

### C++

```cpp
int main() {
    std::cout << "Running..." << std::endl;
    std::string hello = "Hello ";
    std::string world = "World!";
    std::cout << hello * world << std::endl;
    return 0;
}
```

#### Compile Time Error

```
$ g++ main.cpp

error: no match for 'operator*' (operand types are
'std::string' and 'std::string')
```

*Figure: A side-by-side comparison of Python and C++ error handling. The left side shows a Python code block with a peach background, where the line `print(hello * world)` is enclosed in a red box. Below it, a console window shows a "Run Time Error" with a yellow sad face emoji. The right side shows a C++ code block with a light green background, where the line `std::cout << hello * world << std::endl;` is enclosed in a red box. Below it, a console window shows a "Compile Time Error" accompanied by a photograph of a crying baby in the bottom right corner.*

---

## Slide 33: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup resting his chin on his hand. Behind him on the wall is a poster for "The C++ Programming Language" with his name visible.*

`bjarne_about_to_raise_hand`

---

## Slide 34: Types are super important!!
Types are super important!!

---

## Slide 35: Types

*   A **type** refers to the “category” of a variable
*   C++ comes with built-in types
    *   **int**      `106`
    *   **double**   `71.4`
    *   **string**   `"Welcome to CS106L!"`
    *   **bool**     `true / false`
    *   **size_t**   `12`    // Non-negative

*Figure: A cartoon parrot is shown on the right side of the slide. A speech bubble coming from the parrot contains the text: "Hopefully this sounds familiar :D".*

---

## Slide 36: Static Typing in C++

We know that the compiler checks for types before
generating machine code.

This means…

**C++** is a **statically typed** language

---

## Slide 37: Dynamic Typing

Python (Dynamic Typing)

```python
a = 3
b = "test"

def foo(c):
    d = 106
    d = "hello world!"
```

*Figure: A code block showing Python assignments. Inside the function `foo`, the variable `d` is first assigned the integer `106` and then reassigned the string `"hello world!"`. These two lines are enclosed in a red rectangular box, highlighting the reassignment of a variable to a different type.*

**The interpreter assigns variables a type at runtime based on the variable's value at that time**

---

## Slide 38: Dynamic Typing

**Python (Dynamic Typing)**

```python
a = 3
b = "test"

def foo(c):
    d = 106
    d = "hello world!"
```

*Figure: The two lines `d = 106` and `d = "hello world!"` are highlighted with a red rectangle, emphasizing the reassignment of `d` to a different type.*

> Oh you are just switching
> things up with me! That's okay!
> I'll catch on!
>
> So d was originally an **integer**,
> and now it's a **string** :D
>
> No problemo!

*Figure: The Python logo (blue and yellow intertwined snakes) appears below the speech bubble.*

**The interpreter assigns variables a `type` at runtime based on the variable's value at that time**

---

## Slide 39: Dynamic Typing vs Static Typing

### Dynamic Typing
**Python (Dynamic Typing)**

```python
a = 3
b = "test"

def foo(c):
    d = 106
    d = "hello world!"
```

*Figure: A large green checkmark is placed next to the Python code block, indicating that the variable `d` can be reassigned from an integer to a string without error.*

The interpreter assigns variables a **type at runtime based on the variable's value at that time**

### Static Typing
**C++ (Static Typing)**

```cpp
int a = 3;
string b = "test";

void foo(string c)
{
    int d = 106;
    d = "hello world!"; ❌
}
```

*Figure: A red cross (❌) is placed next to the line `d = "hello world!";`, indicating a type mismatch error because variable `d` was declared as an `int`.*

*   Every variable must declare a type
*   Once declared, the type cannot change

---

## Slide 40: Why static typing?
- More efficient
- Easier to understand and reason about
- Better error checking

---

## Slide 41: Better error checking

*Figure: A Python code snippet contained within a white rectangular box that has a slight drop shadow. On the right side of this box is the official Python logo, which consists of two interlocking snakes in blue and yellow.*

```python
def add_3(x):
    return x + 3

add_3("CS106L") # Oops, that's a string. Runtime error!
```

---

## Slide 42: Better error checking

```python
def add_3(x):
    return x + 3

add_3("CS106L") # Oops, that's a string. Runtime error!
```

*Figure: The Python logo (two intertwined snakes, one blue and one yellow) is positioned to the right of the code block.*

*Figure: A large orange arrow points downwards from the Python code block to the C++ code block.*

```cpp
int add_3(int x) {
    return x + 3;
}

add_3("CS106L"); // Can't pass a string when int expected. Compile time error!
```

*Figure: The C++ logo (a blue hexagon containing a white "C" and two plus signs) is positioned to the right of the code block.*

---

## Slide 43: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, the creator of C++, wearing glasses and a patterned shirt. He is resting his chin on his hand in a thoughtful pose. In the background, posters for "The C++ Programming Language" and "Programming: Principles and Practice Using C++" are visible.*

bjarne_about_to_raise_hand

---

## Slide 44: Your turn 🫵🫵💪💪

*   TODO: Fill in the blanks underneath with the correct type
*   NOTE: `(int) x` casts `x` to an int by dropping decimals
    *   E.g. `(int) 5.7 = 5`

*Figure: A code exercise box with blank lines on the left side where students must fill in the correct C++ type for each variable declaration or function signature.*

```cpp
______ a = "test";
______ b = 3.2 * 5 - 1;
______ c = 5 / 2;
______ d(int foo) { return foo / 2; }
______ e(double foo) { return foo / 2; }
______ f(double foo) { return (int)(foo + 0.5); }
______ g(double c) { std::cout << c << std::endl; }
```

---

## Slide 45: Your turn

*Figure: A screenshot of a code snippet inside a bordered box, showing variable declarations and function definitions in C++.*

```cpp
std::string a = “test”;
double   b = 3.2 * 5 - 1;
int      c = 5 / 2; // What does this equal?
int      d(int foo) { return foo / 2; }
double   e(double foo) { return foo / 2; }
int      f(double foo) { return (int)(foo + 0.5); } // What's this?
void     g(double c) { std::cout << c << std::endl; }
```

---

## Slide 46: Aside: Function Overloading

Defining two functions with the same name but different parameters

*Figure: Two C++ function definitions with the same name, `axolotl`, are shown inside a grey box. Red rectangular boxes highlight the different parameter types in the function signatures: `int x` in the first function and `double x` in the second function.*

```cpp
double axolotl(int x) {          // (1)
    return (double) x + 3;   // typecast: int → double
}

double axolotl(double x) {       // (2)
    return x * 3;
}

axolotl(2);         // uses version ___, returns ______
axolotl(2.0);       // uses version ___, returns ______
```

---

## Slide 47: Aside: Function Overloading

Defining two functions with the same name but different parameters

*Figure: A code snippet showing two overloaded versions of a function named `axolotl`. Red boxes highlight the different parameter types: `(int x)` in the first version and `(double x)` in the second.*

```cpp
double axolotl(int x) {          // (1)
    return (double) x + 3;   // typecast: int → double
}

double axolotl(double x) {       // (2)
    return x * 3;
}

axolotl(2);          // uses version (1), returns 5.0
axolotl(2.0);        // uses version (2), returns 6.0
```

(1)                5.0
(2)                6.0

---

## Slide 48: C++ Language Characteristics

C++ is a compiled, statically typed language

---

## Slide 49: What questions do you have?

*Figure: A photo of Bjarne Stroustrup sitting in an office. He has his hand near his chin in a thoughtful pose. Behind him are computer monitors and posters. One poster on the wall has the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP".*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 50: Structs

---

## Slide 51: Keeping track of students
* Every student ID has a few properties
* A name (string)
* A SUNet (string)
* An ID # (int)

*Figure: An image of a Stanford University student ID card. The card features a maroon stripe at the top and the "Stanford University" logo in the upper right. The name printed on the card is "THE stanford tree" in bold, followed by a red ID number "00000002" and the word "Student" in gray. To the left is a photograph of the Stanford Tree mascot, and to the right is the red Stanford "S" logo. At the bottom right, it says "Issued: 07/11/2024" followed by the number "806092554753017" and a barcode.*

---

## Slide 52: Okay let's make generating IDs into a function!!

Okay let's make generating IDs into a function!!

return type issueNewID() {
    yada yada code yada yada

    return our ID stuff (ID #, name, sunet)
}

*Figure: A meme image of a cat sitting in front of a laptop, looking serious with a small blue towel or blanket over its shoulders, as if intensely coding.*

this looks like the most legit function I've ever seen 😎😎 (jk..)

---

## Slide 53: A fundamental problem

```cpp
return_type issueNewID() {
    // How can we return all three things?
    // What should our return type be? 😟😟
    
    // In Python this would look like…
    // return "Stanford Tree", "theTREE", 0000002
}
```

How do we return more than one value? :OO

---

## Slide 54: Introducing... structs!

*Figure: An illustration of a red toy drum with a white head and two wooden drumsticks.*

---

## Slide 55: Structs bundle data together

*Figure: A code snippet inside a rectangular border with a slight shadow, demonstrating the use of a C++ struct.*

```cpp
struct StanfordID {
    string name;            // These are called fields
    string sunet;           // Each has a name and type
    int idNumber;
};

StanfordID id;                          // Initialize struct
id.name = "THE Stanford Tree";         // Access field with ‘.’
id.sunet = "theTREE";
id.idNumber = 0000002;
```

---

## Slide 56: Returning multiple values

```cpp
StanfordID issueNewID() {
    StanfordID id;

    id.name = "THE Stanford Tree";
    id.sunet = "theTREE";
    id.idNumber = 0000002;

    return id;
}
```

*Figure: A Stanford University student ID card for "THE stanford tree". The card displays the Stanford logo (a block "S" with a tree), a photo of the Stanford Tree mascot (a costumed tree with googly eyes), and the text: "Stanford University", "THE stanford tree", "0000002" in red, "Student", "Issued: 07/11/2024", and a barcode with the number "806092554753017".*

---

## Slide 57: Uniform Initialization

```cpp
StanfordID id;
id.name = "THE Stanford Tree";
id.sunet = "theTREE";
id.idNumber = 0000002;
```

---

## Slide 58: Uniform Initialization

```cpp
StanfordID id;
id.name = "THE Stanford Tree";
id.sunet = "theTREE";
id.idNumber = 0000002;
```

*Figure: A yellow thought bubble positioned to the right of the first code block containing the text: "We'll learn more about this next time!"*

*Figure: A large orange arrow pointing downwards, indicating a transition from the first code block to the second.*

```cpp
// Order depends on field order in struct. '=' is optional
StanfordID tree = { "THE Stanford Tree", "theTREE", 0000002 };
StanfordID lelandjr { "Leland Stanford Jr", "thejunior", 5430282 };
```

*Figure: A small black-and-white historical photograph of a man (Leland Stanford Jr.) in formal 19th-century attire, standing and holding a hat and a cane.*

---

## Slide 59: Using list initialization

*Figure: A slide showing two C++ code snippets. The top snippet demonstrates initializing a `StanfordID` object by setting its fields individually, with an orange box around the assignment lines. An orange arrow points down to the bottom snippet, which shows the same function using list initialization, with an orange box around the initializer list.*

```cpp
StanfordID issueNewID() {
    StanfordID id;
    id.name = "THE Stanford Tree";
    id.sunet = "theTREE";
    id.idNumber = 0000002;
    return id;
}
```

```cpp
StanfordID issueNewID() {
    StanfordID id = { "THE Stanford Tree", "theTREE", 0000002 };
    return id;
}
```

---

## Slide 60: The Big Idea

*Figure: Two pink brain icons are positioned to the left and right of the heading text "THE BIG IDEA".*

### 🧠 THE BIG IDEA 🧠

A **struct** bundles **named variables** into a new type

---

## Slide 61: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup wearing glasses and a patterned shirt, with his hand near his chin in a thoughtful pose. In the background, posters including one for "Programming Language: Bjarne Stroustrup" are visible.*

`bjarne_about_to_raise_hand`

---

## Slide 62: Many Possible Structs

```cpp
struct Name {
    string first;
    string last;
};

Name rf = { "Rachel", "Fernandez" };
```

*Figure: A 3D-rendered emoji of a boy with blonde hair is located inside the box to the right of the struct definition.*

---

## Slide 63: Many Possible Structs

*Figure: Two side-by-side white boxes with black borders and drop shadows on a gray background. Each box contains a C++ struct definition, a related 3D icon, and an initialization example.*

### Left Box
```cpp
struct Name {
    string first;
    string last;
};
```
*Figure: To the right of the struct definition is a 3D-rendered emoji of a person's head.*

```cpp
Name rf = { "Rachel", "Fernandez" };
```

### Right Box
```cpp
struct Order {
    string item;
    int quantity;
};
```
*Figure: To the right of the struct definition is a 3D-rendered clipboard icon with a checklist and a green checkmark.*

```cpp
Order dozen = { "Eggs", 12 };
```

---

## Slide 64: Many Possible Structs

*Figure: A code snippet defining a `Name` struct and a face emoji of a person with short blonde hair.*

```cpp
struct Name {
    string first;
    string last;
};
Name rf = { "Rachel", "Fernandez" };
```

*Figure: A code snippet defining an `Order` struct and a clipboard icon with a checklist.*

```cpp
struct Order {
    string item;
    int quantity;
};
Order dozen = { "Eggs", 12 };
```

*Figure: A code snippet defining a `Point` struct.*

```cpp
struct Point {
    double x;
    double y;
};
Point origin { 0.0, 0.0 };
```

---

## Slide 65: Many Possible Structs

### Name Struct
```cpp
struct Name {
    string first;
    string last;
};
Name rf = { "Rachel", "Fernandez" };
```
*Figure: An emoji-style icon of a person's head with short blonde hair and brown eyes.*

### Order Struct
```cpp
struct Order {
    string item;
    int quantity;
};
Order dozen = { "Eggs", 12 };
```
*Figure: An emoji-style icon of a clipboard with a checklist showing a green checkmark and several blue items.*

### Point Struct
```cpp
struct Point {
    double x;
    double y;
};
Point origin { 0.0, 0.0 };
```

### Circle Struct
```cpp
struct Circle {
    Point center;
    double radius;
};
Circle circle { {0, 0} , 50000000 };
```
*Figure: A solid light green circle icon.*

---

## Slide 66: Many Possible Structs

*Figure: A 2x2 grid of four rectangular boxes, each containing a C++ struct definition and an example instantiation. A white callout box with a black border and red text sits in the center, overlapping the corners of the four boxes.*

### Top-Left Box
*Figure: A blonde male emoji face is positioned to the right of the code.*

```cpp
struct Name {
    string first;
    string last;
};

Name rf = { "Rachel", "Fernandez" };
```

### Top-Right Box
*Figure: An image of a clipboard with a checklist is positioned to the right of the code.*

```cpp
struct Order {
    string item;
    int quantity;
};

Order dozen = { "Eggs", 12 };
```

### Bottom-Left Box

```cpp
struct Point {
    double x;
    double y;
};

Point origin { 0.0, 0.0 };
```

### Bottom-Right Box
*Figure: A solid green circle is positioned to the right of the code.*

```cpp
struct Circle {
    Point center;
    double radius;
};

Circle circle { {0, 0} , 50000000 };
```

### Center Callout
**Notice anything?**

---

## Slide 67: Many Possible Structs

```cpp
struct Name {
    string first;
    string last;
};

Name jrb = { "Rachel", "Fernandez" };
```

*Figure: A yellow emoji of a person's face next to the `Name` struct.*

---

### Notice anything?

```cpp
struct Order {
    string item;
    int quantity;
};

Order dozen = { "Eggs", 12 };
```

*Figure: A clipboard icon next to the `Order` struct.*

---

```cpp
struct Point {
    double x;
    double y;
};

Point origin { 0.0, 0.0 };
```

---

```cpp
struct Circle {
    Point center;
    double radius;
};

Circle circle { {0, 0} , 50000000 };
```

*Figure: A green parrot with a speech bubble containing the text "Erm these all look a bit similar!!". The parrot is in the bottom-right corner of the slide.*

---

## Slide 68: Using std::pair
We can use `std::pair`!

---

## Slide 69: std::pair

*Figure: A code snippet displayed inside a white rectangular box with a light grey drop shadow.*

```cpp
struct Order {
    std::string item;
    int quantity;
};

Order dozen = { "Eggs", 12 };
```

---

## Slide 70: std::pair

```cpp
struct Order {
    std::string item;
    int quantity;
};

Order dozen = { "Eggs", 12 };
```

*Figure: An orange arrow points from the first code block down to a second code block.*

```cpp
std::pair<std::string, int> dozen { "Eggs", 12 };
std::string item = dozen.first;            // "Eggs"
int quantity = dozen.second;               // 12
```

---

## Slide 71: std::pair is a template
(We’ll learn more about this later)

*Figure: A code snippet enclosed in a rectangular box showing the C++ definition of a template struct `pair` and an example instantiation.*

```cpp
template <typename T1, typename T2>
struct pair {
    T1 first;
    T2 second;
};
std::pair<std::string, int>
```

---

## Slide 72: std::pair is a template

(We’ll learn more about this later)

```cpp
struct pair {
    std::string first;
    int second;
};
```

---

## Slide 73: Something to discuss
There’s something we need to discuss…

---

## Slide 74: What is an std !!? 🦠😷

---

## Slide 75: std — The C++ Standard Library

*   Built-in types, functions, and more provided by C++
*   You need to `#include` the relevant file
    *   `#include <string>` → `std::string`
    *   `#include <utility>` → `std::pair`
    *   `#include <iostream>` → `std::cout`, `std::endl`

*Figure: A screenshot of a code editor window containing a basic C++ program. The code demonstrates the use of `std::string` and `std::cout` after including the necessary header files.*

```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name = "Rachel";
    std::cout << name << std::endl;

    return 0;
}
```

---

## Slide 76: std — The C++ Standard Library

* Built-in types, functions, and more provided by C++
* You need to `#include` the relevant file
    * `#include <string>` → `std::string`
    * `#include <utility>` → `std::pair`
    * `#include <iostream>` → `std::cout`, `std::endl`
* We prefix standard library names with `std::`
    * If we write `using namespace std;` we don't have to, but this is considered bad style as it can introduce ambiguity
        * (What would happen if we defined our own `sort`?)

---

## Slide 77: std — The C++ Standard Library

*   We prefix standard library names with `std::`
*   If we write `using namespace std;` we don't have to, but this is considered bad style as it can introduce ambiguity
    *   (What would happen if we defined our own `sort`?)

*Figure: A C++ code snippet inside a box that demonstrates a potential naming ambiguity between a custom `sort` function and `std::sort`.*

```cpp
#include <algorithm>
using namespace std;

// You write your own sort function
void sort(int a, int b) {
  cout << "rachel's sort >:D!";
}

int main() {
  sort(3, 5); // which sort? rachel's or std::sort?
}
```

---

## Slide 78: std — The C++ Standard Library
- See the official standard at [cppreference.com](https://cppreference.com)!
- Avoid cplusplus.com…
    - It is outdated and filled with ads 😭

Links on this slide:
- <https://en.cppreference.com/w/>

---

## Slide 79: To use std::pair, you must #include it

std::pair is defined in a header file called utility

*Figure: A code box with a black border containing C++ code that includes the utility header and declares a std::pair variable.*

```cpp
#include <utility>

// Now we can use `std::pair` in our code.

std::pair<double, double> point { 1.0, 2.0 };
```

---

## Slide 80: What does #include do?

*Figure: A diagram illustrating the effect of the `#include` preprocessor directive. A large white rectangle on the left contains a `#include` statement and a variable declaration. An arrow points from the `#include` line to a second, partially overlapping rectangle on the right. The right-hand rectangle is labeled "utility" and contains a simplified snippet of a header file definition, including a template struct. The right-hand rectangle has a subtle drop shadow.*

```cpp
#include <utility>
std::pair<double, double> p { 1.0, 2.0 };
```

```cpp
utility

namespace std {
template
<typename T1, typename T2>
struct pair {
    T1 first;
    T2 second;
};

// Other utility code...
}
```

---

## Slide 81: What does #include do?

*Figure: A rectangular box with a drop shadow containing a C++ code snippet showing a simplified version of the `std` namespace and an example variable declaration.*

```cpp
namespace std {
    template <typename T1, typename T2>
    struct pair {
        T1 first;
        T2 second;
    };
    // Other utility code...
}

std::pair<double, double> p { 1.0, 2.0 };
```

---

## Slide 82: What questions do you have?

*Figure: A meme photograph of Bjarne Stroustrup, the creator of C++. He is shown in an office setting, resting his chin on his hand in a thoughtful or anticipatory pose. Behind him, a bookshelf or wall displays a poster with his name, "BJARNE STROUSTRUP," and part of a book title.*

bjarne_about_to_raise_hand

---

## Slide 83: Code Demo
Code Demo

---

## Slide 84: Solving a Quadratic Equation

*Figure: In the top right corner, there is a cartoon image of Princess Bubblegum and Finn from Adventure Time. Finn is exclaiming "Mathematical!".*

*Figure: Two side-by-side plots of red parabolas on coordinate planes. The left plot shows a parabola opening upwards that crosses the x-axis at two points, marked with black dots. The x-axis is labeled 0, 1, 2, 3 and the y-axis is labeled 0, 1. The right plot shows a parabola opening upwards that is positioned entirely above the x-axis. The x-axis is labeled -2, 0, 2 and the y-axis has a label at 2.*

$$x^2 - 3x + 2 = 0$$
$$x = 1, x = 2$$

$$2x^2 + 1 = 0$$
*no solution*

---

## Slide 85: Solving a Quadratic Equation
- If we have $ax^2 + bx + c = 0$
- Solutions are $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
- If $b^2 - 4ac$ is negative, there are no solutions

---

## Slide 86: Quadratic Solver Function Declaration

*Figure: A diagram featuring a central rectangular box containing a C++ function declaration, with four annotated arrows explaining each part of the code.*

```cpp
std::pair<bool, std::pair<double, double>> solveQuadratic(double a, double b, double c);
```

*   A label **Return Value** is positioned at the top left, with an arrow pointing down to the overall return type `std::pair<bool, std::pair<double, double>>`.
*   A label **What are the solutions (if any)?** is positioned at the top center, with an arrow pointing down specifically to the inner `std::pair<double, double>` portion of the return type.
*   A label **Is there a solution?** is positioned at the bottom left, with an arrow pointing up to the `bool` component of the return type.
*   A label **Coefficients** is positioned at the bottom right, with an arrow pointing up to the function parameters `double a, double b, double c`.

---

## Slide 87: std::pair<bool, std::pair<double, double>>

*Figure: Two plots of quadratic functions (parabolas) side-by-side. The left plot shows a parabola opening upward that touches the x-axis at two points (x=1.0 and x=2.0). The right plot shows a parabola opening upward that does not touch the x-axis (its vertex is above y=0).*

**Left Plot (roots exist):**
*   The graph has x-axis labels: 0, 1, 2, 3. The y-axis has a label at 1.
*   The parabola has black dots marking the two x-intercepts at (1.0, 0.0) and (2.0, 0.0).

```cpp
{ true, { 1.0, 2.0 }}
```

**Right Plot (no real roots):**
*   The graph has x-axis labels: -2, 0, 2. The y-axis has a label at 2.
*   The parabola's minimum point is clearly above the x-axis.

```cpp
{ false, doesnt_matter }
// e.g. { false, { 0.0, 0.0 }}
```

---

## Slide 88: Solving a Quadratic Equation
* If we have $ax^2 + bx + c = 0$
* Solutions are $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
* If $b^2 - 4ac$ is negative, there are no solutions

* **Your task:** Write a function to solve a quadratic equation:
```cpp
std::pair<bool, std::pair<double, double>> solveQuadratic(double a, double b, double c);
```

*Figure: A small icon of a notebook with a pencil on the bottom left, indicating a helpful tip or note.*

📝 The sqrt function from the `<cmath>` header can calculate the square root

---

## Slide 89: Let’s code this together 👫

https://106b.vercel.app/rooms/cs106l

---

## Slide 90: Improving Our Code

---

## Slide 91: The using keyword

The **using** keyword

---

## Slide 92: The using keyword

* Typing out long type names gets tiring
* We can create **type aliases** with the `using` keyword

```cpp
std::pair<bool, std::pair<double, double>> solveQuadratic(double a, double b, double c);
```

*Figure: A large orange arrow points downward from the first code box to the second code box.*

```cpp
using Zeros = std::pair<double, double>;
using Solution = std::pair<bool, Zeros>;
Solution solveQuadratic(double a, double b, double c);
```

*Figure: A small, rotated photograph of a surprised orange and white cat overlaps the bottom-right corner of the second code box.*

---

## Slide 93: using is kind of like a variable for types!

using is kind of like a variable for types!

---

## Slide 94: The auto keyword
The auto keyword

---

## Slide 95: The auto keyword

*   The auto keyword tells the compiler to infer the type

```cpp
std::pair<bool, std::pair<double, double>> result = solveQuadratic(a, b, c);
```

*Figure: A large orange downward-pointing arrow connects the first code box to the second code box.*

```cpp
auto result = solveQuadratic(a, b, c);

// This is exactly the same as the above!
// result still has type std::pair<bool, std::pair<double, double>>
// We just told the compiler to figure this out for us!
```

*Figure: A speech bubble containing the text "The compiler checks for the declared return type of solveQuadratic and fills it in for auto :O" points toward the `auto result` line in the second code box. A photo of a green macaw parrot is positioned in the bottom right corner of the slide.*

---

## Slide 96: auto is still statically typed!
*Figure: A bordered box containing two lines of C++ code with comments.*

```cpp
auto i = 1;   // int inferred
i = "hello!"; // ❌ Doesn't compile
```

---

## Slide 97: Which one is clearer?

*Figure: A rectangular white box with a drop shadow containing two lines of C++ code comparison.*

```cpp
std::pair<bool, std::pair<double, double>> result = ...;
auto result = ...;
```

---

## Slide 98: Which one is clearer?

*Figure: A white rectangular box with a thin black border and subtle drop shadow, centered on the slide. Inside the box are two lines of code, vertically centered. The first line has the keyword `auto` in red and the number `1` in blue. The second line has the keyword `int` in red and the number `1` in blue. Both lines use black for the variable name `i`, the equals sign, and the semicolon.*

```cpp
auto i = 1;
int i = 1;
```

---

## Slide 99: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup sitting in an office. He is a balding man with glasses and gray hair, wearing a patterned shirt, and resting his chin on his hand in a thinking pose. Behind him, posters are visible on a wall. One poster prominently displays the text "Bjarne Stroustrup" and "Programming Language". Another poster, partially visible to the left, appears to show book covers with the text "Elements and Practice Using C++".*

bjarne_about_to_raise_hand

What questions do you have?

---

## Slide 100: Recap

Recap

---

## Slide 101: Recap

- C++ is a compiled, statically typed language
- Structs bundle data together into a single object
- **std::pair** is a general purpose struct with two fields
- **#include** from the C++ Standard Library to use built-in types
  - And use the std:: prefix too!
- Quality of life features to improve your code
  - **using** creates type aliases
  - **auto** infers the type of a variable

---

## Slide 102: Closing

**See you all on Tuesday!! :)**

**Have a great weekend :D**
