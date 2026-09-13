# Lecture 04: Streams (2026Spring)

> PDF title: 2026Spring-04-Streams.pptx
> Source: `assets/slides/2026Spring-04-Streams.pdf` · 151 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Lecture 4: Streams 🏞

Stanford CS106L, Spring 2026
Rachel Fernandez & Preston Seay

*Figure: A class hierarchy diagram for C++ I/O streams, with a source attribution "cplusplus.com" at the bottom left. The diagram is organized into columns by header file: `<ios>`, `<istream>`, `<iostream>`, `<fstream>`, `<sstream>`, and `<streambuf>`. It shows inheritance relationships with arrows:*
*   *In `<ios>`: `ios_base` points to `ios`.*
*   *In `<istream>`: `istream` inherits from `ios`.*
*   *In `<iostream>`: `iostream` inherits from both `istream` and `ostream`.*
*   *In `<ostream>` (noted in a sub-box): `ostream` inherits from `ios`.*
*   *In `<streambuf>`: `streambuf` is the base for buffer classes.*
*   *Black boxes indicate standard stream objects: `cin` (associated with `istream`) and `cout, cerr, clog` (associated with `ostream`).*
*   *In `<fstream>`: `ifstream` inherits from `istream`, `fstream` inherits from `iostream`, `ofstream` inherits from `ostream`, and `filebuf` inherits from `streambuf`.*
*   *In `<sstream>`: `istringstream` inherits from `istream`, `stringstream` inherits from `iostream`, `ostringstream` inherits from `ostream`, and `stringbuf` inherits from `streambuf`.*

---

## Slide 2: Plan

1. Quick recap
2. What are streams??!!
3. `stringstreams`
4. `cout` and `cin`
5. Output streams
6. Input streams

*Figure: A diagram illustrating the hierarchy and relationships between C++ stream headers, classes, and standard objects. Headers shown at the top are `<ios>`, `<istream>`, `<iostream>`, `<fstream>`, and `<sstream>`. Classes are organized under these headers: `ios_base` leads to `ios`, which is the base for both `istream` and `ostream`. `iostream` is shown as inheriting from both `istream` and `ostream`. Standard objects `cin` (associated with `istream`) and `cout`, `cerr`, and `clog` (associated with `ostream`) are highlighted in black boxes. File stream classes `ifstream`, `fstream`, and `ofstream` are shown as specializations of the input, bidirectional, and output streams respectively, all supported by `filebuf`. Similarly, string stream classes `istringstream`, `stringstream`, and `ostringstream` are shown supported by `stringbuf`, with both buffer types pointing to the base `streambuf` class. The diagram is attributed to cplusplus.com.*

---

## Slide 3: Attendance

*Figure: A large QR code is centered on the slide. To its right, a green parrot with a white stripe on its face has a light green speech bubble above its head.*

-   **Attendance 🪄**
-   *Figure: The speech bubble from the parrot says:*
    -   Fill it out by
    -   3:10PM!

---

## Slide 4: coffee vs tea

*Figure: A pie chart titled "coffee vs tea" inside a thin blue border. The chart displays four segments representing preferences. A legend to the right uses colored circles and emojis to identify each category.*

| Color | Category |
| :--- | :--- |
| 🔵 | Coffee ☕ |
| 🔴 | Tea 🫖 |
| 🟠 | Matcha 🍵 |
| 🟢 | coffee = tea |

*Figure: (Chart Data)*
*   **40.6%**: Tea (Red segment)
*   **28.1%**: Coffee (Blue segment)
*   **28.1%**: Matcha (Orange segment)
*   **(unlabeled)**: coffee = tea (Green sliver)

---

## Slide 5: Reminders

**Assignment 0: Setup comes out tomorrow!**

*Figure: A screenshot of a code editor (like VS Code) displaying C++ code. The visible code includes a `while` loop and some variable assignments. The editor window shows line numbers on the left side (e.g., 19-28), but these are omitted as per the transcription rules.*

```cpp
bool again = true;

while (again) {
    iN = -1;
    again = false;
    getline(cin, sInput);
    system("cls");
    stringstream(sInput) >> dblTemp;
    iLength = sInput.length();
    if (iLength < 4) {
        again = true;
    } else if (sInput[iLength - 3] != '.') {
```

**Assignment 0: Setup!**

Due Friday, April 17th at 11:59PM

### 🔗 Overview

Welcome to CS106L! This assignment will get you setup for the rest of the quarter so that setup for the rest of the assignments is simple and smooth. By the end of this assignment, you should be able to compile and run C++ files from VSCode and run the autograder, which you'll be doing for each of the remaining assignments!

If you run into any issues during setup, please reach out to us on [EdStem](https://edstem.org) or come to our office hours!

---

## Slide 6: Slides are available at…

cs106l.stanford.edu

Links on this slide:
- <http://cs106l.stanford.edu/>

---

## Slide 7: Last Lecture

Last Lecture

*Figure: A dark blue rectangular slide contains the following text:*

CS106L: Lecture 3
Initialization & References

Preston Seay, Rachel Fernandez

---

## Slide 8: A quick recap

1. Uniform Initialization 🦄

A *ubiquitous and safe* way of initializing things using {}

*Figure: The slide features a title in a large orange banner at the top. The main content is presented inside a light grey rounded box. A unicorn emoji (🦄) follows the text "Uniform Initialization".*

---

## Slide 9: A quick recap

1. **Uniform Initialization** 🦄
    * A *ubiquitous and safe* way of initializing things using `{}`
2. **References** 🦄
    * A way of giving variables ***aliases*** and having multiple variables all refer the the **same memory.**

*Figure: A slide with a title bar in an orange gradient that reads "A quick recap". Below the title, inside a light gray rounded rectangle, there is a numbered list. Item 1 is "Uniform Initialization" followed by a unicorn emoji. Item 2 is "References" followed by a unicorn emoji.*

---

## Slide 10: Plan

1. Quick recap
2. **What are streams??!!**
3. `stringstreams`
4. `cout` and `cin`
5. Output streams
6. Input streams

---

## Slide 11: Why streams?

> "Designing and implementing a general <u>**input/output**</u> facility for a programming language is notoriously difficult"
> 
> - *Bjarne Stroustrup*

*Figure: A photograph of Bjarne Stroustrup on the right side of the slide, with a light green speech bubble pointing toward him containing the text "So I did it".*

---

## Slide 12: Streams

"~~Designing and implementing~~ a general **input/output** facility for a ~~programming language is notoriously difficult~~ **C++**"

- *a stream :)*

*Figure: A portrait photograph of Bjarne Stroustrup, the creator of C++, positioned in the bottom right corner. He is wearing glasses and a light blue button-down shirt with his arms crossed.*

---

## Slide 13: Streams: a general input/output facility for C++

---

## Slide 14: Streams

~~a general **input/output** facility for C++~~

a general **input/output(IO)** <mark>abstraction</mark> for C++

*Figure: A portrait of Bjarne Stroustrup, the creator of C++, is located in the bottom right corner of the slide.*

---

## Slide 15: Abstractions

**Abstraction** = hide unnecessary details and expose what is only relevant

*Figure: A photograph from the perspective of a driver inside a car. Two hands are visible holding the steering wheel. The car is driving on a paved road through a hilly landscape. The scene is bathed in warm, golden sunlight, suggesting either sunrise or sunset.*

---

## Slide 16: Abstractions

Abstractions provide a consistent ***interface***,
and in the case of **streams** the interface is for
**reading** and **writing** data!

*Figure: A presentation slide with an orange header bar at the top displaying the title "Abstractions" in a large black font. Below the header is a beige box containing centered text: "Abstractions provide a consistent interface, and in the case of streams the interface is for reading and writing data!". Within the text, the word "interface" is bold, italicized, and underlined; the word "streams" is in orange; and the words "reading" and "writing" are underlined.*

---

## Slide 17: What questions do you have?

What questions do you have?

*Figure: A centered photograph of Bjarne Stroustrup, the creator of C++. He is wearing glasses and a patterned shirt, resting his chin on his hand in a thoughtful pose. In the background, there are bookshelves and a poster with the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP" visible.*

bjarne_about_to_raise_hand

---

## Slide 18: THE BIG IDEA

🧠 THE BIG IDEA 🧠

Streams help us read and write data

---

## Slide 19: But what is a stream?

*Figure: A green parrot with a white and black head is shown on the right side of the slide. A speech bubble points toward the parrot and contains the following text.*

> You may not know what a stream is, but chances are **you probably use them all the time!**

---

## Slide 20: A familiar stream!

```cpp
std::cout << "Hello, World" << std::endl;
```

*Figure: The slide features a large orange-to-white gradient horizontal bar at the top containing the title. Below this, a single line of C++ code is displayed in a large font, with the keyword "std" highlighted in green.*

---

## Slide 21: A familiar stream!

```cpp
std::cout << "Hello, World" << std::endl;
```

*Figure: A C++ code snippet showing a standard output statement. A callout box with the text "This is a stream" has a blue arrow pointing upward to the `cout` object in the code.*

---

## Slide 22: A familiar stream!

streams are like a **conveyer belt**!

*Figure: A photograph of a stainless steel roller conveyor belt system. The conveyor features a long, inclined metal frame with a bed of closely spaced horizontal rollers, supported by a sturdy leg structure with adjustable circular feet.*

---

## Slide 23: A familiar stream!

*Figure: An illustration divided into two panels explaining streams using a conveyor belt analogy.*

### output streams
*Figure: A terminal window with tabs labeled "PROBLEMS", "OUTPUT", "DEBUG CONSOLE", "TERMINAL", and "PORTS". Below the terminal is a conveyor belt with green arrows pointing to the left. Boxes labeled "data" are moving along the belt. The foreground box is labeled "data".*

```
(base) rachelfernandez@Rachels-MacBook-Air-6 ~ % 
```

### input streams
*Figure: A computer keyboard positioned above a conveyor belt with red arrows pointing to the right. Boxes labeled "data" are moving along the belt. The foreground box is labeled "data".*

---

## Slide 24: A familiar stream!

*Figure: Two panels illustrating stream concepts using a conveyor belt metaphor. The left panel, titled "output streams" in green, shows a terminal window and a conveyor belt moving boxes labeled "data" away from it, with green arrows indicating the direction of flow. The right panel, titled "input streams" in red, shows a keyboard and a conveyor belt moving boxes labeled "data" toward it, with red arrows indicating the direction of flow.*

### output streams
*Figure: A terminal window screenshot showing a command prompt.*
```
● (base) rachel@fernandez@Rachels-MacBook-Air-6 ~ % █
```
*Figure: A conveyor belt with green arrows moving boxes labeled "data" away from the terminal.*

* cout, cerr, clog
* ofstream
* ostringstream

### input streams
*Figure: A conveyor belt with red arrows moving boxes labeled "data" toward a keyboard.*

* cin
* ifstream
* istringstream

---

## Slide 25: CS106B examples

Have you ever taken CS106B and you had to read in files for your assignment(s)? kinda like this..?

```cpp
ifstream in;
openFile(in, my_file);

Vector<std::string> lines = readLines(in);
```

*Figure: A slide with a large orange title bar at the top. On the left, there is a black-and-white stick figure drawing with a speech bubble containing the question above. On the right, there is a rectangular box with a light blue border containing a C++ code snippet.*

---

## Slide 26: CS106B examples

> Have you ever taken
> CS106B and you had to
> read in files for your
> assignment(s)? kinda like
> this..?

*Figure: A simple black-and-white cartoon of a stick figure looking up toward a speech bubble.*

```cpp
ifstream in;
openFile(in, my_file);

Vector<std::string> lines = readLines(in);
```

**Note**: This is using the Stanford library and <u>not the STD</u> but it’s still an example of streams

*you were using **stream** all along!!*

*Figure: A yellow smiley-face emoji pointing toward the text above it.*

---

## Slide 27: cout & cin examples

```cpp
std::cout << "hello CS106L!";
```

```cpp
// Allows user to write something into
// student_input
std::string student_input;
std::cin >> student_input;
```

---

## Slide 28: fout & fin examples

```cpp
//create a file called “data.txt”
std::ofstream fout(“data.txt”);
fout << “I’m writing to this file”
```

---

## Slide 29: fout & fin examples

*Figure: An orange title banner at the top of the slide contains the text "fout & fin examples" in bold black font. Below this are two light-grey boxes containing C++ code snippets.*

```cpp
//create a file called “data.txt”
std::ofstream fout(“data.txt”);
fout << “I’m writing to this file”
```

```cpp
std::ifstream fin(“data.txt”);
std::string first_word;
//store the first word from the file into
//student_input
fin >> first_word;
```

---

## Slide 30: More examples

//create a file called "data.txt"
std::ofstream fout("data.txt");
fout << "I'm writing to this file"

std::ifstream fin("data.txt");
std::string first_word;
//store the first word from the file into fin
fin >> student_input;

std::cout << "hello CS106L!"

std::string student_input;
std::cin >> student_input;

*Figure: A speech bubble emanating from a parrot image in the bottom right corner. The text inside the bubble says: "notice the << and >>? That’s abstraction at work! We can use a **consistent interface** to work with **input** and **output**". The phrases "consistent interface", "input", and "output" are highlighted in yellow.*

---

## Slide 31: Let’s do some practice!

[https://tinyurl.com/lecture-practice](https://tinyurl.com/lecture-practice)

*Figure: A meme showing a frog centered on a green radial sunburst background, reminiscent of the "Hypnotoad" meme format. The text "IT'S TIME TO" is displayed at the top in white block letters, and "PRACTICE" is displayed at the bottom in white block letters. A small watermark "memegenerator.es" is visible in the bottom right corner of the meme.*

Links on this slide:
- <https://tinyurl.com/lecture-practice>

---

## Slide 32: What are all these types of streams?

What are all these types of streams?

*Figure: A green and white parrot with a speech bubble. The speech bubble contains the text: "Let’s back up a step!!"*

Let’s back up a step!!

---

## Slide 33: ios_base

- `ios_base` is the foundation for everything `streams` related
- What data does `ios_base` maintain?
    - State Information
    - Control Information
    - These things have to do with making sure our stream is a-ok!

*Figure: A photo of a waterfall serving as a metaphor for a data stream. A yellow label "input" at the top right has a red line pointing to the start of the waterfall. A yellow label "output" at the bottom left has a red line pointing to the pool at the base. Three yellow squares labeled "a", "b", and "c" are positioned along the falling water, representing data moving through the stream.*

*Stream carrying your data*

---

## Slide 34: ios_base explained

**State Information** = flags that tell you the status/health of your stream
1. ex. `failbit` → logical error (ex. type error)
2. ex. `eofbit` → reached end of stream

**Control Information** = how does the stream present the data?
1. ex. should 255 be printed as “255”, “FF” or “377”?

*Figure: A photograph of a waterfall in a green landscape under a sunset sky. Yellow boxes with labels are overlaid on the image. At the top of the waterfall, a yellow box labeled "input" points with a red arrow towards the water falling. During the fall, the water passes three yellow boxes labeled "a", "b", and "c". At the bottom where the water hits the pool, a yellow box labeled "output" points with a red arrow towards the pool. Below the image is the caption "Stream carrying your data".*

---

## Slide 35: What builds off ios_base?

*Figure: A diagram of two concentric circles. The outer, larger circle is light pink and labeled "ios_base". The inner, smaller circle is light purple and labeled "basic_ios", showing that `basic_ios` builds off or is contained within `ios_base`.*

**basic_ios** ensures the stream is
working correctly and where the
stream comes from! maybe its the
console, keyboard, or a file

more on this later >:D

---

## Slide 36: ostream and istream

*Figure: A nested diagram illustrating the inheritance or containment relationship between C++ I/O stream classes. An outer circle is labeled `ios_base`. Inside it is a smaller circle labeled `basic_ios`. Within the `basic_ios` circle, there are two overlapping circles: one green circle labeled `ostream` and one purple circle labeled `istream`. To the right, two callout boxes are connected to these circles by arrows. An arrow points from the top box to the `ostream` circle, containing the text: `ostream` is used for output. An arrow points from the bottom box to the `istream` circle, containing the text: `istream` is used for input. The "o" in `ostream` and the word "output" in the top box, as well as the "i" in `istream` and the word "input" in the bottom box, are highlighted in yellow.*

*   **ios\_base**
*   **basic\_ios**
*   **ostream**
*   **istream**
*   **ostream** is used for **output**
*   **istream** is used for **input**

---

## Slide 37: ostream and istream

*Figure: A nested diagram illustrating the C++ stream class hierarchy. A large outer pink circle is labeled `ios_base`. Inside it is a medium blue circle labeled `basic_ios`. Inside the blue circle are two overlapping smaller circles: a top green circle labeled `ostream` and a bottom purple circle labeled `istream`. A blue arrow points from the `ostream` circle to a green rectangular box on the right, which lists `std::ofstream`, `std::ostringstream`, and `std::cout`. Another blue arrow points from the `istream` circle to a purple rectangular box on the right, which lists `std::ifstream`, `std::istringstream`, and `std::cin`.*

Labels in the diagram:
- **ios_base**
- **basic_ios**
- **ostream**
- **istream**

Green box contents:
- `std::ofstream`
- `std::ostringstream`
- `std::cout`

Purple box contents:
- `std::ifstream`
- `std::istringstream`
- `std::cin`

---

## Slide 38: What streams actually are

*Figure: A UML-style inheritance diagram for the C++ standard stream library classes. At the top is a box labeled `ios_base`, which is the base class. Below it is `basic_ios <CharT, Traits>`, connected by an inheritance arrow. From `basic_ios`, the hierarchy branches into `basic_ostream <CharT, Traits>` (enclosed in a green oval) and `basic_istream <CharT, Traits>` (enclosed in a red oval). In the center, `basic_iostream <CharT, Traits>` (enclosed in an orange oval) inherits from both the output and input base classes. At the bottom, three colored circular groupings show the concrete stream types: a green circle containing `basic_ostringstream <CharT, Traits>` and `basic_ofstream <CharT, Traits>`; an orange circle containing `basic_stringstream <CharT, Traits>` and `basic_fstream <CharT, Traits>`; and a red circle containing `basic_istringstream <CharT, Traits>` and `basic_ifstream <CharT, Traits>`. The caption at the bottom center reads "Inheritance diagram".*

*   `ios_base`
*   `basic_ios <CharT, Traits>`
*   `basic_ostream <CharT, Traits>`
*   `basic_ostringstream <CharT, Traits>`
*   `basic_ofstream <CharT, Traits>`
*   `basic_iostream <CharT, Traits>`
*   `basic_stringstream <CharT, Traits>`
*   `basic_fstream <CharT, Traits>`
*   `basic_istream <CharT, Traits>`
*   `basic_istringstream <CharT, Traits>`
*   `basic_ifstream <CharT, Traits>`

Inheritance diagram

---

## Slide 39: What questions do you have?

*Figure: A photo of Bjarne Stroustrup with his hand near his face, wearing glasses and a patterned shirt. Behind him are computer monitors and posters, one of which displays the text "PROGRAMMING LANGUAGE BJARNE STROUSTRUP".*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 40: Data Input Question

How does data move from an
external source (keyboard or file)
into your C++ program?

---

## Slide 41: An Input Stream

How do you read a **double** from your console?

**std::cin** is the console <mark>input stream!</mark>

*Figure: A rounded rectangular callout box with a light gray background containing explanatory text.*

> The std::cin stream is an **instance** of **std::istream** which represents the standard input stream!

*Figure: A code snippet enclosed in a rectangle with a dotted border.*

```cpp
void verifyPi()
{
    double pi;
    std::cin >> pi;
    /// verify the value of pi!
    std::cout << pi / 2 << '\n';
}
```

---

## Slide 42: std::cin
*Figure: The title "std::cin" is displayed in a large orange banner at the top. Below, on the left, a C++ code snippet is shown inside a dotted rectangle. To the right, a label "Console" is placed above a dashed blue rectangle containing the string "1.57".*
```cpp
int main()
{
  double pi;
  std::cin >> pi;
  /// verify the value of pi!
  std::cout << pi / 2 << '\n';

  return 0;
}
```
Console
"1.57"

---

## Slide 43: std::cin
```cpp
int main()
{
    double pi;
    std::cin >> pi;
    /// verify the value of pi!
    std::cout << pi / 2 << '\n';

    return 0;
}
```

*Figure: A C++ code snippet with the line `std::cin >> pi;` highlighted in a red box. To the right, a dashed-border box labeled "Console" contains the text `"1.57"`. A speech bubble originating from an image of a parrot with angry eyebrows contains the text "Woah! So we stored a string into a double? is that allowed?? 🤨".*

---

## Slide 44: Generalizing the Stream

*Figure: A conceptual diagram titled "Generalizing the Stream" on an orange banner. On the left, a large red question mark represents an unknown external source. A double-headed arrow connects it to a central dashed blue rounded rectangle. The text "external source" is positioned above this arrow. Inside the dashed rectangle, the text reads "stream", "“3.14”" in a larger font, and "String representation" below that. To the right, another double-headed arrow connects the rectangle to the text "3.14 double in your program" on the right. The text "type conversion" is positioned above this second arrow.*

---

## Slide 45: Implementation vs Abstraction

*Figure: A conceptual diagram illustrating a data flow. On the far left, a large red 3D question mark icon is labeled "external source". A horizontal double-headed arrow connects this icon to a central dashed blue rounded rectangle. The rectangle is labeled "stream" at its top edge. Inside the rectangle, there is a question mark in quotation marks (`“?”`) positioned above the text "String representation". To the right of the stream box, another horizontal double-headed arrow is labeled "type conversion" above it. This arrow points toward the final section on the right, which features a question mark, the term `fill_in_type` (in monospace font), and the phrase "in your program" stacked below.*

external source
stream
`“?”`
String representation
type conversion
?
`fill_in_type`
in your
program

---

## Slide 46: Why is this even useful?

Streams allow for a **universal** way of **dealing with external data**

---

## Slide 47: What streams actually are

### Classifying different types of streams

*Figure: A slide with a solid orange header bar containing the main title. Below the header, a sub-title is centered. The main content is contained within a light beige rectangular box.*

**Input streams (I)**
*   a way to read data from a source
    *   Are inherited from **std::istream**
    *   ex. reading in something from the console (**std::cin**)
    *   primary operator: >> (called the extraction operator)

**Output streams (O)**
*   a way to write data to a destination
    *   Are inherited from **std::ostream**
    *   ex. writing out something to the console (**std::cout**)
    *   primary operator: << (called the insertion operator)

---

## Slide 48: streams and types

*Figure: A Venn diagram illustrating relationships between stream types. A large, outermost blue circle contains two overlapping inner circles. The top inner circle is green and labeled `ostream`. The bottom inner circle is purple and labeled `istream`. An arrow points from a text box to the overlapping intersection area of the two inner circles.*

This intersection is known as
**iostream** which takes has all
of the characteristics of
`ostream` *and* `istream`!

---

## Slide 49: What streams actually are

*Figure: An inheritance diagram illustrating the hierarchy of C++ stream classes. At the top is `ios_base`. Below it is `basic_ios<CharT, Traits>`. This has two primary derived classes: `basic_ostream<CharT, Traits>` and `basic_istream<CharT, Traits>`. Below these is `basic_iostream<CharT, Traits>`, which inherits from both `basic_ostream` and `basic_istream`; this class is highlighted with an orange rectangular border. Further down, specialized stream classes are shown: `basic_ostringstream<CharT, Traits>` (inheriting from `basic_ostream`), `basic_stringstream<CharT, Traits>` (inheriting from `basic_iostream`), and `basic_istringstream<CharT, Traits>` (inheriting from `basic_istream`). At the bottom level are file stream classes: `basic_ofstream<CharT, Traits>` (inheriting from `basic_ostringstream`), `basic_fstream<CharT, Traits>` (inheriting from `basic_stringstream`), and `basic_ifstream<CharT, Traits>` (inheriting from `basic_istringstream`). Arrows indicate the direction of inheritance from derived to base classes.*

Inheritance diagram

---

## Slide 50: What do we import?

*Figure: A C++ stream header hierarchy diagram from cplusplus.com. The diagram is organized into columns for different headers: `<ios>`, `<istream>`, `<iostream>`, `<fstream>`, and `<sstream>`. There are also sections for `<ostream>` and `<streambuf>`. A yellow rectangular highlight focuses on the `<ostream>` section and the `ostream` class. Arrows illustrate inheritance and relationships, such as `ios` being the base for `istream`, `iostream`, and `ostream`. The `<iostream>` column contains stream objects `cin` and `cout, cerr, clog` in black boxes. The source attribution `cplusplus.com` is located at the bottom left of the diagram.*

```cpp
#include <iostream> - cin & cout
#include <istream>  - cin
#include <ostream>  - cout
```

---

## Slide 51: What questions do we have?

What questions do we have?

*Figure: A simple black-and-white cartoon character with a skeptical or pensive expression, resting one hand on their chin. With their other hand, they are holding up a blue hexagonal icon of the C++ logo, which has three wavy lines rising from it to suggest it is "steaming" or "hot."*

---

## Slide 52: Plan

*Figure: A slide with a title "Plan" in large, bold black font centered within an orange rectangular header bar at the top. Below the header is a numbered list of six items on a white background. Item 3, "stringstreams!", is in a bold black font, while the other items are in a lighter grey font.*

1. Quick recap
2. What are streams??!!
3. **stringstreams!**
4. cout and cin
5. Output streams
6. Input streams

---

## Slide 53: ostream and istream

*Figure: A diagram illustrating the hierarchy and relationships of stream classes. A large light red circle labeled "ios_base" contains a blue circle labeled "basic_ios". Within the "basic_ios" circle, there are two overlapping circles: a green one labeled "ostream" and a purple one labeled "istream". An arrow points from the "ostream" circle to a green rectangle on the right which lists "std::ofstream", "std::ostringstream" (highlighted with a yellow background), and "std::cout". A second arrow points from the "istream" circle to a light purple rectangle below it, which lists "std::ifstream", "std::istringstream" (highlighted with a yellow background), and "std::cin".*

---

## Slide 54: std::stringstream

### What?
a way to treat strings as streams

### Utility?
stringstreams are useful for use-cases that deal with mixing data types

*Figure: A conceptual diagram illustrating the components of a string stream. A large light-blue circle encloses a reddish circle. Within the reddish circle are two overlapping ovals: a green one labeled 'ostream' and a purple one labeled 'istream'. A yellow crosshair symbol is centered at the intersection of these two ovals.*

---

## Slide 55: What streams actually are

*Figure: A class inheritance diagram for C++ streams, titled "Inheritance diagram" at the bottom. The hierarchy starts with `ios_base` at the top, which is the base for `basic_ios <CharT, Traits>`. From `basic_ios`, the hierarchy branches to `basic_ostream <CharT, Traits>` and `basic_istream <CharT, Traits>`. These two are then combined as base classes for `basic_iostream <CharT, Traits>` through multiple inheritance. Further down, specialized stream classes are shown: `basic_ostringstream <CharT, Traits>` and `basic_ofstream <CharT, Traits>` inherit from `basic_ostream`; `basic_istringstream <CharT, Traits>` and `basic_ifstream <CharT, Traits>` inherit from `basic_istream`; and `basic_stringstream <CharT, Traits>` and `basic_fstream <CharT, Traits>` inherit from `basic_iostream`. An orange box highlights the `basic_stringstream <CharT, Traits>` class.*

---

## Slide 56: std::stringstream example

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";
}
```

---

## Slide 57: std::stringstream example

```cpp
void foo() {
  /// partial Bjarne Quote
  std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot
yourself in the foot\n";

  /// create a stringstream
  std::stringstream ss(initial_quote);
}
```

*Figure: A blue-outlined box with a rounded corner containing the text "initialize stringstream with string constructor". An orange arrow points from this box to the line of code `std::stringstream ss(initial_quote);`.*

---

## Slide 58: std::stringstream example

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot
                                yourself in the foot\n";

    /// create a stringstream
    std::stringstream ss;
    ss << initial_quote;
}
```

*Figure: An orange arrow points from a rounded callout bubble to the line of code `ss << initial_quote;`.*

**Annotation box text:**
> since this is a stream we can also **insert** the initial_quote like this!

---

## Slide 59: std::stringstream example

```cpp
void foo() {
  /// partial Bjarne Quote
  std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot
  yourself in the foot\n";

  /// create a stringstream
  std::stringstream ss(initial_quote);

  /// data destinations
  std::string first;
  std::string last;
  std::string language, extracted_quote;
}
```

*Figure: A code snippet demonstrating `std::stringstream` usage. To the right of the line `std::stringstream ss(initial_quote);`, there is a light blue callout box containing the text "initialize stringstream with string constructor" with an orange arrow pointing from the box to that specific line of code.*

---

## Slide 60: std::stringstream example

```cpp
void foo() {
  /// partial Bjarne Quote
  std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot
  yourself in the foot\n";

  /// create a stringstream
  std::stringstream ss(initial_quote);

  /// data destinations
  std::string first;
  std::string last;
  std::string language, extracted_quote;

  ss >> first >> last >> language >> extracted_quote;
}
```

*Figure: A code snippet enclosed in a dotted rectangle. An orange arrow points from a rounded, light-blue callout box to the line `std::stringstream ss(initial_quote);`. The callout box contains the text: "initialize stringstream with string constructor". The word "destinations" in the comment `/// data destinations` is highlighted with a yellow background.*

---

## Slide 61: std::stringstream example

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";
    /// create a stringstream
    std::stringstream ss(initial_quote);
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
    ss >> first >> last >> language >> extracted_quote;
    std::cout << first << " " << last << " said this: " << language << " " << extracted_quote << std::endl;
}
```

*Figure: A callout box with the text "initialize stringstream with string constructor" and an arrow pointing to the line `std::stringstream ss(initial_quote);` in the code.*

---

## Slide 62: what the stream looks like!

*Figure: A diagram illustrating a character stream as a grid of individual cells. A label "Start" in a beige rounded box has an orange arrow pointing down to the first cell of the stream. The cells contain the characters: "Bjarne Stroustrup C makes it easy to shoot yourself in the foot \n", where the "\n" (newline character) is shown in pink. A label "End of stream" in a beige rounded box has an orange arrow pointing up to the pink "\n" character.*

---

## Slide 63: std::stringstream example

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot
yourself in the foot\n";

    /// create a stringstream
    std::stringstream ss(initial_quote);

    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;

    ss >> first >> last >> language;
    std::cout << first << " " << last << " said this: " << language << " " <<
    extracted_quote << std::endl;
}
```

*Figure: A code slide demonstrating a `std::stringstream` example. A rounded text box with a light blue border and fill contains the note: "Remember! Streams move data from one place to another". An orange arrow points from this box to the line of code `std::string language, extracted_quote;`, indicating where the data is being moved into these destination variables. The word "destinations" in the comment `/// data destinations` is highlighted in yellow.*

---

## Slide 64: std::stringstream example

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";

    /// create a stringstream
    std::stringstream ss(initial_quote);

    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;

    ss >> first >> last >> language;
    std::cout << first << " " << last << " said this: " << language << " " << extracted_quote << std::endl;
}
```

*Figure: A code example demonstrating `std::stringstream`. An orange arrow points from a blue callout box to the `<<` operator in the `std::cout` statement. The callout box contains the text: "We're making use of the insertion operator". In the comment `/// data destinations`, the word `destinations` is highlighted in yellow.*

---

## Slide 65: << and >> RULE

<< and >> reads up to any **whitespace** including:

1. ' ' (space)
2. '\n'
3. '\t'
4. '\r'
5. '\f'
6. '\v'

---

## Slide 66: what the stream looks like!
`ss >> first >> last >> language;`

*Figure: An orange arrow points to the beginning of a character stream depicted as a sequence of boxes. The stream contains the characters: `B j a r n e   S t o u s t r u p   C   m a k e s   i t   e a s y   t o   s h o o t   y o u r s e l f   i n   t h e   f o o t \n`. The characters are grouped into words with spaces between them, and the newline character is highlighted in pink. Below the stream are three empty, rounded rectangular boxes. Underneath these boxes are the labels "First", "Last", and "Language", indicating the target variables for the extraction operations.*

---

## Slide 67: what the stream looks like!

*Figure: A diagram illustrating how data is extracted from a stringstream. At the top, a code line reads `ss >> first >> last >> language;` inside a rounded rectangle, with `ss` highlighted in red and `>>` highlighted in yellow. An orange arrow labeled "extracts from the stream!" points from below to the `>>` operator. Below the code, a row of boxes represents the stream's character buffer containing: "Bjarne Stoustrup C makes it easy to shoot yourself in the foot \n" (with `\n` shown in pink). An orange vertical arrow on the far left points down to the beginning of this stream buffer. At the bottom of the slide, three empty rounded rectangles are shown in a row, with the labels "First", "Last", and "Language" centered beneath them respectively, representing the destination variables for the extraction.*

---

## Slide 68: what the stream looks like!

```cpp
ss >> first >> last >> language;
```

*Figure: A diagram illustrating how a string stream is parsed. At the top, a rounded box contains the code statement `ss >> first >> last >> language;`. Below it, a grid of boxes represents the character stream. The content of the stream is:*
`B j a r n e   S t o u s t r u p   C   m a k e s   i t   e a s y   t o   s h o o t`
`y o u r s e l f   i n   t h e   f o o t \n`

*The first six characters (`B j a r n e`) are highlighted in purple boxes. An orange arrow points to the character box immediately following the highlighted word `Bjarne`. Below the stream grid, three rounded boxes represent variables. The leftmost box contains the text "Bjarne" and is labeled "First". The middle box is empty and labeled "Last". The rightmost box is empty and labeled "Language".*

---

## Slide 69: what the stream looks like!

```cpp
ss >> first >> last >> language;
```

*Figure: An orange arrow points from the code statement above down to a horizontal stream buffer visualization. The buffer contains the following characters, each in its own box, with spaces between them:*
`B j a r n e   S t o u s t r u p   C   m a k e s   i t   e a s y   t o   s h o o t   y o u r s e l f   i n   t h e   f o o t \n`
*The initial segment "Bjarne Stroustrup" is highlighted in purple.*

*Figure: Three rounded rectangles representing output variables are shown below the stream buffer. The first, labeled "First", contains "Bjarne". The second, labeled "Last", contains "Stroustrup". The third, labeled "Language", is empty.*

---

## Slide 70: what the stream looks like!

`ss >> first >> last >> language;`

*Figure: A diagram illustrating how a string stream processes input. The code snippet `ss >> first >> last >> language;` is shown above a character grid. An orange arrow points from the code to the grid. The grid displays the sentence "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n" as individual characters in cells. The characters for "Bjarne Stroustrup C" are highlighted in light purple. Below the grid, three boxes show the results of the extraction: "Bjarne" labeled "First", "Stroustrup" labeled "Last", and "C" labeled "Language".*

```cpp
ss >> first >> last >> language;
```

---

## Slide 71: std::stringstream example

```cpp
void foo() {
  /// partial Bjarne Quote
  std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot
  yourself in the foot";
  /// create a stringstream
  std::stringstream ss(initial_quote);
  /// data destinations
  std::string first;
  std::string last;
  std::string language, extracted_quote;

  ss >> first >> last >> language;
  std::cout << first << " " << last << " said this: " << language << " " <<
  extracted_quote << std::endl;
}
```

*Figure: A callout bubble with an arrow pointing to the line `std::string language, extracted_quote;` which contains the text "We want to extract the quote!". In the code, the phrase "makes it easy to shoot yourself in the foot" and the variable name `extracted_quote` are highlighted in yellow.*

---

## Slide 72: what the stream looks like!

*Problem:* ?  

```cpp
ss >> first >> last >> language >> extracted_quote;
```  

*Figure: A diagram illustrating the stream from `ss`. The stream contains the following characters (in sequence): `B j a r n e   S t o u s t r u p   C   ma k e s   i t   e a s y   t o   s h o o t   y o u r s e l f   i n   t h e   f o o t \n`. An orange arrow points from the `>>` (highlighted in yellow) in the code line to the stream, indicating the stream’s current position. Below the stream, three labeled boxes display the extracted values: the "First" box contains "Bjarne", the "Last" box contains "Stroustrup", and the "Language" box contains "C".*

---

## Slide 73: what the stream looks like!

```cpp
ss >> first >> last >> language >> extracted_quote;
```

*Figure: A diagram illustrating the state of a stream during extraction. A code snippet `ss >> first >> last >> language >> extracted_quote;` is shown at the top, with `ss` in red and the final `>>` operator highlighted in yellow. An orange arrow points from this yellow `>>` down to a grid of characters representing the input stream. The stream contains the text: "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n". The characters "Bjarne Stroustrup C" are highlighted with a purple background, and the newline character `\n` at the end is highlighted in magenta. Below the stream, three boxes show the results of the extraction so far: `Bjarne` (labeled "First"), `Stroustrup` (labeled "Last"), and `C` (labeled "Language").*

Grid text:
`B j a r n e   S t o u s t r u p   C   m a k e s   i t   e a s y   t o   s h o o t`
`y o u r s e l f   i n   t h e   f o o t   \n`

| Extracted Value | Label |
| :--- | :--- |
| Bjarne | First |
| Stroustrup | Last |
| C | Language |

---

## Slide 74: what the stream looks like!

**Problem:**
The >>
operator only
reads until the
next
whitespace!

`ss >> first >> last >> language >> extracted_quote;`

*Figure: A diagram illustrating the behavior of the extraction operator (`>>`). A line of code at the top shows the extraction chain `ss >> first >> last >> language >> extracted_quote;`, with the final `>>` highlighted in yellow. An orange arrow points from this yellow-highlighted operator down to a grid representing the input stream characters. The arrow points exactly to the space between the character 'C' and the word 'makes'.*

| B | j | a | r | n | e | | S | t | o | u | s | t | r | u | p | | C | | m | a | k | e | s | | i | t | | e | a | s | y | | t | o | | s | h | o | o | t | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| y | o | u | r | s | e | l | f | | i | n | | t | h | e | | f | o | o | t | | \n |

*In the grid, the cells containing "Bjarne", "Stroustrup", and "C" are highlighted in purple to indicate they have already been read.*

| **Bjarne** | **Stroustrup** | **C** |
| :---: | :---: | :---: |
| First | Last | Language |

---

## Slide 75: what the stream looks like!

**Problem:**  
The `>>` operator only reads until the next whitespace!

```cpp
ss >> first >> last >> language >> extracted_quote;
```

*Figure: A diagram illustrating how the `>>` operator reads a stream. An orange arrow points from the `>>` operator in the code line down to the beginning of the word "makes" in the stream. The stream is shown as a row of boxes containing individual characters, reading: "B j a r n e   S t o u s t r u p   C   ma k e s   i t   e a s y   t o   s h o o t   y o u r s e l f   i n   t h e   f o o t   \n". The characters "B j a r n e   S t o u s t r u p   C" are highlighted in light purple. The characters "ma k e s" are highlighted in yellow. The newline character "\n" is highlighted in magenta. Below the stream, there are three rounded boxes labeled "First", "Last", and "Language". The "First" box contains "Bjarne", the "Last" box contains "Stroustrup", and the "Language" box contains "C".*

-   **First:** Bjarne
-   **Last:** Stroustrup
-   **Language:** C

---

## Slide 76: Use getline() !

*Figure: The slide title is displayed in a large font inside a solid orange horizontal bar at the top. The body of the slide has a light-colored background.*

```cpp
istream& getline(istream& is, string& str, char delim)
```

* **getline()** reads an input stream, **is**, up until the **delim** char and stores it in some buffer, **str**.

---

## Slide 77: Use getline()!

```cpp
istream& getline(istream& is, string& str, char delim)
```

- **getline()** reads an input stream, **is**, up until the **delim** char and stores it in some buffer, **str**.
- The **delim** char is by default `'\n'`.

---

## Slide 78: Use getline()!

*Figure: A slide titled "Use getline()!" in a large orange header bar at the top. Below, a light grey box contains a function signature followed by several bullet points describing the function's behavior.*

```cpp
istream& getline(istream& is, string& str, char delim)
```

- `getline()` reads an input stream, `is`, up until the `delim` char and stores it in some buffer, `str`.
- The `delim` char is by default `'\n'`.
- `getline()` *consumes* the `delim` character!
  - PAY ATTENTION TO THIS :)

---

## Slide 79: use std::getline()!

`ss >> first >> last >> language >> extracted_quote;`

*Figure: A diagram showing how the extraction operator (`>>`) processes a string. A buffer contains the text: "Bjarne Stroustrup C makes it easy to shoot yourself in the foot". The first three words ("Bjarne Stroustrup C") are highlighted in purple, while the rest of the text is highlighted in yellow. An orange arrow points from the code statement above to the space after "C", indicating where the extraction stops. Below the buffer, three rounded rectangles display the extracted values: "Bjarne" (labeled First), "Stroustrup" (labeled Last), and "C" (labeled Language). A red "no" symbol appears at the end of the yellow section.*

---

## Slide 80: std::stringstream example

```cpp
void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot\n";
    /// create a stringstream
    std::stringstream ss(initial_quote);
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
    ss >> first >> last >> language;
    std::getline(ss, extracted_quote);
    std::cout << first << " " << last << " said this: '" << language << " " << extracted_quote + "'" << std::endl;
}
```

---

## Slide 81: What questions do we have?

*Figure: A black-and-white stick figure with a thoughtful expression holds a blue, cubic C++ logo in its hand. Steam rises from the logo.*

---

## Slide 82: Plan

1. Quick recap
2. What are streams??!!
3. stringstreams!
4. **cout and cin**
5. Output streams
6. Input streams

---

## Slide 83: ostream and istream

*Figure: A diagram illustrating the inheritance and relationship hierarchy among C++ I/O stream classes. The diagram features a large, outer pink circle labeled `ios_base`. Inside it is a smaller, light purple circle labeled `basic_ios`. Within `basic_ios` are two overlapping circles: a green one labeled `ostream` and a purple one labeled `istream`. An arrow points from the `ostream` circle to a light green rectangular box on the right. This box contains the text: `std::ofstream`, `std::ostringstream` (with a horizontal strikethrough line), and `std::cout` (highlighted in yellow). Another arrow points from the `istream` circle to a light purple rectangular box below the first. This box contains: `std::ifstream`, `std::istringstream` (with a horizontal strikethrough line), and `std::cin` (highlighted in yellow).*

---

## Slide 84: Output Streams

*   a way to write data to a destination/external source
    *   ex. writing out something to the console (std::cout)
    *   use the << operator to ***send*** to the output stream

---

## Slide 85: Zooming in on Output Streams!

Character in output streams are stored in an intermediary buffer
before being flushed to the destination

*Figure: A diagram showing the flow of output data. A code box at the bottom left contains a two-line C++ snippet. An arrow points from this code to the left end of a horizontal array (a buffer) with multiple cells. The first four cells contain the characters '6', '.', '2', and '8'. The remaining cells are empty. A second arrow, labeled "Flush", points from the right end of the buffer to a black rectangle representing a terminal window. The terminal window displays a command prompt (`>_`).*

```cpp
double tao = 6.28;
std::cout << tao;
```

*Figure: A screenshot of a terminal window with a black background. A white command prompt `>_` is visible at the start.*

---

## Slide 86: Zooming in on Output Streams!

*Figure: A diagram illustrating how output is buffered in `std::cout`. On the left, a dashed box contains the code `double tao = 6.28; std::cout << tao;`. An arrow points from this code to a horizontal buffer composed of eight rectangular cells. The cells contain the characters `6`, `.`, `2`, and `8` in sequence, with the remaining four cells empty. A black arrow labeled "Flush" points from the buffer to a terminal window icon displaying `>_`. A light-colored rounded callout box at the bottom states: "contents in buffer not shown on external source until an explicit flush occurs!"*

```cpp
double tao = 6.28;
std::cout << tao;
```

contents in buffer not shown on external source until an explicit flush occurs!

---

## Slide 87: When do we flush?

- ```cpp
  std::cout << std::flush
  ```
- ```cpp
  std::cout << std::endl
  ```
- When you reach the **end of your program**
- When the buffer is **full**
- When **tied streams interact** (ie. cout has to flush before you take input via cin)

---

## Slide 88: ?: Zooming in on Output Streams!

*Figure: A diagram illustrating the flushing of an output stream buffer. A dashed box contains three lines of C++ code. An arrow points from this code box to a horizontal row of eight rectangular cells representing a buffer. The first four cells contain the characters '6', '.', '2', '8', and the remaining four cells are empty. An arrow labeled "Flush" points from the buffer to a dashed blue rounded rectangle labeled "Console".*

```cpp
double tao = 6.28;
std::cout << tao;
std::cout << std::flush;
```

---

## Slide 89: Zooming in on Output Streams!

```cpp
double tao = 6.28;
std::cout << tao;
std::cout << std::flush;
```

*Figure: A conceptual diagram of C++ output buffering. On the left is a box containing the code snippet. An arrow points from this code to a segmented horizontal bar representing an internal buffer. A second arrow, labeled "Flush", points from the end of the buffer to a dashed rounded rectangle labeled "Console". Inside the console box, the string "6.28" is displayed.*

---

## Slide 90: Zooming in on Output Streams!

```cpp
double tao = 6.28;
std::cout << tao;
/// Also flushes!
std::cout << std::endl;
```

*Figure: A diagram illustrating how output streams work. A code block (with a dotted border) on the left contains the C++ code above. An arrow points from the code to a horizontal buffer (an array of empty rectangular cells). From the buffer, an arrow labeled "Flush" points down and to the right toward a dashed-border box labeled "Console" containing the text "6.28", representing the flushed output appearing on the console.*

---

## Slide 91: std::endl

```cpp
int main()
{
    for (int i=1; i <= 5; ++i) {
        std::cout << i << std::endl;
    }
    return 0;
}
```

*Figure: A dashed box labeled "Output:" containing a large red question mark, indicating the output of the program is unknown or to be determined.*

std::endl tells the cout stream to end the line!

---

## Slide 92: std::endl

```cpp
int main()
{
    for (int i=1; i <= 5; ++i) {
        std::cout << i << std::endl;
    }
    return 0;
}
```

**Output:**

```
"1"
"2"
"3"
"4"
"5"
```

std::endl tells the
cout stream to end the
line!

---

## Slide 93: Here’s without std::endl

*Figure: A slide with a black background. At the top is an orange horizontal banner containing the title "Here’s without std::endl". Below the banner are two boxes with dashed-line borders. The box on the left contains a C++ code snippet with syntax highlighting: the `int` keyword is orange, the `std` namespace is green, and the literal `0` is red. The box on the right contains the text "Output:" and a large red 3D question mark below it.*

```cpp
int main()
{
  for (int i=1; i <= 5; ++i) {
    std::cout << i;
  }
  return 0;
}
```

**Output:**

*Figure: A large, red, three-dimensional question mark.*

---

## Slide 94: Here’s without std::endl

```cpp
int main()
{
    for (int i=1; i <= 5; ++i) {
        std::cout << i;
    }
    return 0;
}
```

*Output:*
> "12345"

*Figure: A code block showing a simple C++ program without using std::endl, and its resulting concatenated output.*

---

## Slide 95: Recall

* **`cerr` and `clog`**
* **`cerr`**: used to output errors (unbuffered)
- sends errors out **IMMEDIATELY**
* **`clog`**: used for non-critical event logging (buffered)

read more here: [GeeksForGeeks](https://www.geeksforgeeks.org)

Links on this slide:
- <https://www.geeksforgeeks.org/difference-between-cerr-and-clog/>

---

## Slide 96: A shoutout and clarification

So there's a small caveat to this

---

## Slide 97: A shoutout and clarification

However, upon testing these examples, I observed that '\n' seems to flush the buffer in a manner similar to std::cout. Further research led me to the CPP Reference std::endl, which states, "In many implementations, standard output is line-buffered, and writing '\n' causes a flush anyway, unless `std::ios::sync_with_stdio(false)` was executed." This suggests that in many standard outputs, '\n' behaves the same as std::cout. Additionally, when I appended | cat to my program, I noticed that in file output, '\n' does not immediately flush the buffer.

---

## Slide 98: A shoutout and clarification

*Figure: A C++ code snippet inside a dashed rectangle box, and a callout note box to its right.*

```cpp
int main()
{
  std::ios::sync_with_stdio(false)
  for (int i=1; i <= 5; ++i) {
    std::cout << i << '\n';
  }
  return 0;
}
```

*Note: A light-yellow callout box to the right of the code contains the following text:*

You **_may_** get a massive performance boost from this. Read more about this [here](here)

Links on this slide:
- <https://stackoverflow.com/questions/31162367/significance-of-ios-basesync-with-stdiofalse-cin-tienull>

---

## Slide 99: Another Caveat

> This only works if your output stream is non-interactive!
>
> We tested this `‘std::ios::sync_with_stdio(false)’` proposed solution on various output streams, and found out that it only stopped flushing ‘`\n`’s when the output stream was non-interactive (i.e. file, Unix pipe).
>
> However, if the output stream was interactive (i.e. terminal), the output stream still interpreted it as a line buffer, resulting in an immediate flush when ‘`\n`’ was pushed to the stream.

---

## Slide 100: Yeah... it’s weird

*Figure: A dashed border box containing the following text:*

Sometimes you have to do some digging around to figure out what works and what doesn't :)

Part of working with this language.

---

## Slide 101: Car Trunk Full of Groceries

*Figure: An open trunk of a red car, viewed from behind. The trunk is completely filled to the brim with numerous white plastic shopping bags. Some bags contain visible items like bottles (possibly beer or soda) and boxes. Several bags have store logos printed on them, including names like "La Morey" and "Lakeside." The red car body frames the top and sides of the trunk opening.*

---

## Slide 102: Two Memes

*Figure: Left image shows a red car's trunk overflowing with white plastic grocery bags and various items. Visible text on some bags includes "View's Family Grocery" and "La Joya". The trunk is completely packed with shopping bags, bottles, and boxes. Right image is a meme featuring Captain Jean-Luc Picard from Star Trek: The Next Generation. He is gesturing with his hand open, wearing a red Starfleet uniform, with a bridge crew member in yellow uniform visible in the background. Text overlay reads:* YOU WASTED ENOUGH OF MY TIME CAN I PLEASE HAVE MY LIFE BACK? *A watermark "memeshappen.com" is visible in the bottom right corner.*

---

## Slide 103: ASIDE: CS149 Recommendation

ASIDE: If you’re interested in how computers are able to do multiple things at the same time take CS149!

---

## Slide 104: Use '\n'!

*Figure: Two-panel "Drake Hotline Bling" meme. Top panel: Drake in an orange puffer jacket making a dismissive, "stop" gesture with his hand. Next to this panel is a line of C++ code. Bottom panel: Drake in the same jacket pointing approvingly. Next to this panel is a different line of C++ code.*

```cpp
std::cout << "Draaaakkkkeeeeeeeeee" << std::endl;
```

```cpp
std::cout << "Draaaakkkkeeeeeeeeee" << '\n';
```

---

## Slide 105: What questions do we have?

*Figure: A simple line drawing of a person with a thoughtful expression, holding their chin with one hand and holding a blue hexagonal C++ logo in the other. Three wavy lines rise from the top of the logo, suggesting it is steaming.*

---

## Slide 106: Output File Streams

*   Output file streams have a type: `std::ofstream`
*   a way to write data to a file!
    *   use the `<<` insertion operator to ***send*** to the file
    *   There are some methods for `std::ofstream` [check them out](https://cplusplus.com/reference/fstream/ofstream/)
    *   Here are some you should know:
        *   `is_open()`
        *   `open()`
        *   `close()`
        *   `fail()`

*Figure: A lecture slide with an orange header containing the title "Output File Streams". Below is a bulleted list explaining output file streams.*

Links on this slide:
- <https://cplusplus.com/reference/fstream/ofstream/>

---

## Slide 107: Output File Streams

```cpp
std::ofstream out("file.txt",file_flag);
```

*Figure: An arrow points from the `file_flag` parameter in the code line above to a callout box containing possible values for the flag.*

*   `std::ios::trunc` (default)
*   `std::ios::app` (append!)
*   `std::ios::ate` (open and immediately jump cursor to the end)

---

## Slide 108: Output File Streams

```cpp
int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
```

---

## Slide 109: Output File Streams

*Figure: A slide with an orange title banner. Below the banner is a dotted rectangular box containing a C++ code snippet. An orange arrow points from a callout box on the right to the line `std::ofstream ofs("hello.txt");`. The callout box contains the text: "Creates an output file stream to the file \"hello.txt\"".*

```cpp
int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
```

---

## Slide 110: Output File Streams

```cpp
int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
  if (ofs.is_open()) {
    ofs << "Hello CS106L!" << '\n';
  }
}
```

*Figure: A callout box with an arrow pointing to the `if` block in the code. The text in the box reads: "Checks if the file is open and if it is, then tries to write to it!"*

---

## Slide 111: Output File Streams

```cpp
int main() {
   /// associating file on construction
   std::ofstream ofs("hello.txt");
   if (ofs.is_open()) {
      ofs << "Hello CS106L!" << '\n';
   }
   ofs.close();
```

*Figure: An annotation in a rounded rectangle with an orange arrow pointing to the line `ofs.close();`. The annotation text reads: "This closes the output file stream to “hello.txt”".*

---

## Slide 112: Output File Streams

*Figure: A C++ code snippet is displayed inside a dashed-line rectangle. To the right, a callout box containing the text "Will silently fail" has an orange arrow pointing to the final line of code in the snippet.*

```cpp
int main() {
    /// associating file on construction
    std::ofstream ofs("hello.txt");
    if (ofs.is_open()) {
        ofs << "Hello CS106L!" << '\n';
    }
    ofs.close();
    ofs << "this will not get written";
}
```

---

## Slide 113: Output File Streams

*Figure: A slide featuring a title banner and a C++ code snippet. The title "Output File Streams" is written in large black font on an orange background. Below the title is a code block enclosed in a dotted border. A light-colored callout box with an orange arrow points to a specific line of code.*

```cpp
int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
  if (ofs.is_open()) {
    ofs << "Hello CS106L!" << '\n';
  }
  ofs.close();
  ofs << "this will not get written";

  ofs.open("hello.txt");
  ofs << "this will though! It’s open
again";
  return 0;
}
```

Reopens the stream

---

## Slide 114: Output File Streams

```cpp
int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
  if (ofs.is_open()) {
    ofs << "Hello CS106L!" << '\n';
  }
  ofs.close();
  ofs << "this will not get written";

  ofs.open("hello.txt");
  ofs << "this will though! It’s open
again";
  return 0;
}
```

*Figure: A diagram of a C++ code block enclosed in a dashed border. To the right, a callout box contains the text "Successfully writes to stream" with an orange arrow pointing to the line `ofs << "this will though! It’s open again";`.*

---

## Slide 115: Output File Streams

```cpp
int main() {
    /// associating file on construction
    std::ofstream ofs(“hello.txt”)
    if (ofs.is_open()) {
        ofs << “Hello CS106L!” << ‘\n’;
    }
    ofs.close();
    ofs << “this will not get written”;

    ofs.open(“hello.txt”, std::ios::app);
    ofs << “this will though! It’s open
again”;
    return 0;
}
```

*Figure: An orange callout box with a left-pointing arrow pointing to the line `ofs.open("hello.txt", std::ios::app);`. The callout contains the text: "Flag specifies you want to append, not truncate!"*

---

## Slide 116: Input File Streams

*Figure: A code snippet within a dotted rectangular border, demonstrating a C++ function for reading from an input file stream.*

```cpp
int inputFileStreamExample() {
    std::ifstream ifs("input.txt");
    if (ifs.is_open()) {
        std::string line;
        std::getline(ifs, line);
        std::cout << "Read from the file: " << line << '\n';
    }
    if (ifs.is_open()) {
        std::string lineTwo;
        std::getline(ifs, lineTwo);
        std::cout << "Read from the file: " << lineTwo << '\n';
    }
    return 0;
}
```

---

## Slide 117: Input File Streams

```cpp
int inputFileStreamExample() {
    std::ifstream ifs("input.txt");
    if (ifs.is_open()) {
        std::string line;
        std::getline(ifs, line);
        std::cout << "Read from the file: " << line << '\n';
    }
    if (ifs.is_open()) {
        std::string lineTwo;
        std::getline(ifs, lineTwo);
        std::cout << "Read from the file: " << lineTwo << '\n';
    }
    return 0;
}
```

*Figure: A rounded callout bubble pointing to the code with the note: "Input and output streams on the same source/destination type are complimentary!"*

---

## Slide 118: IO File Streams

*Figure: An inheritance diagram for C++ IO stream classes. The class `ios_base` is at the top. `basic_ios <CharT, Traits>` inherits from `ios_base`. `basic_ostream <CharT, Traits>` and `basic_istream <CharT, Traits>` inherit from `basic_ios`. `basic_iostream <CharT, Traits>` inherits from both `basic_ostream` and `basic_istream`. `basic_ostringstream <CharT, Traits>` and `basic_ofstream <CharT, Traits>` inherit from `basic_ostream`. `basic_stringstream <CharT, Traits>` and `basic_fstream <CharT, Traits>` inherit from `basic_iostream`. `basic_istringstream <CharT, Traits>` and `basic_ifstream <CharT, Traits>` inherit from `basic_istream`. The box for `basic_fstream <CharT, Traits>` is highlighted with an orange border. Below the diagram is the caption "Inheritance diagram".*

- `ios_base`
- `basic_ios <CharT, Traits>`
- `basic_ostream <CharT, Traits>`
- `basic_istream <CharT, Traits>`
- `basic_iostream <CharT, Traits>`
- `basic_ostringstream <CharT, Traits>`
- `basic_ofstream <CharT, Traits>`
- `basic_stringstream <CharT, Traits>`
- `basic_fstream <CharT, Traits>`
- `basic_istringstream <CharT, Traits>`
- `basic_ifstream <CharT, Traits>`
- Inheritance diagram

---

## Slide 119: What questions do we have?

*Figure: A cartoon character with a large round head is shown in a thinking pose, with one hand on its chin and a contemplative expression. The character is holding a steaming blue hexagonal cup that features the C++ logo.*

---

## Slide 120: Plan

*Figure: A slide with the word "Plan" centered in a large orange header. Below the header is a numbered list of six lecture topics. The first five items are in a light gray font, while the sixth item, "Input streams", is in bold black font.*

1. Quick recap
2. What are streams??!!
3. `stringstreams!`
4. `cout` and `cin`
5. Output streams
6. **Input streams**

---

## Slide 121: Input Streams

*Figure: An orange rectangular banner at the top of the slide containing the title "Input Streams" in a large, black, bold, sans-serif font.*

*   Input streams have the type `std::istream`
*   a way to read data from an destination/external source
    *   use the `>>` extractor operator to **read** from the input stream
    *   Remember the `std::cin` is the console input stream
    *   Functions:
        *   **`get()`**
        *   **`getline()`**
        *   `peek()`
        *   `seekg()`

---

## Slide 122: std::cin

*Figure: A horizontal diagram showing the label "cin" followed by a long row of empty, contiguous rectangular cells, representing an input buffer.*

* std::cin is buffered
* Think of it as a place where a user can store some data and then read from it
* std::cin buffer stops at a whitespace

---

## Slide 123: std::cin

*Figure: A diagram representing a buffer. The label "cin" is to the left of a long, horizontal, empty row of adjacent boxes, visually representing a buffer that stores input.*

* The title "std::cin" appears in large, bold text within an orange header bar at the top of the slide.

*   std::cin is buffered
*   Think of it as a place where a user can store some data and then
    read from it
*   std::cin buffer stops at a whitespace
*   Whitespace in C++ includes:
    *   " " – a literal space
    *   \n character
    *   \t character

---

## Slide 124: std::cin

*Figure: A diagram illustrating the std::cin input buffer. At the top is a large orange banner with the title "std::cin". Below it is a row of empty rectangular boxes labeled "cin", representing the input buffer. A small blue arrow points downwards to the leftmost empty box in the buffer. To the right of this diagram is a code snippet within a dotted border, and a callout box with an arrow pointing to a line of code. Below the callout is an empty rounded rectangle.*

```cpp
int main()
{
  double pi;
  std::cin; /// what does this do?
  std::cin >> pi;
  std::cout << "pi is: " << pi << '\n';
  return 0;
}
```

*Callout: An arrow points from a rounded rectangle containing the text "cin buffer is empty so prompts for input!" to the line `std::cin; /// what does this do?` in the code.*

*Figure: An empty rounded rectangle, likely intended for additional annotation or to represent the console/terminal window where input would appear.*

---

## Slide 125: std::cin

*Figure: A diagram illustrating the state of an input buffer for `std::cin`. The label "cin" is on the left, followed by a horizontal row of cells representing characters in the buffer. A small blue arrow points to the first cell, which contains '3'. The following cells contain '.', '1', '4', and a newline character represented as `'\n'`. The remaining cells in the row are empty.*

```cpp
int main()
{
    double pi;
    std::cin; /// what does this do?
    std::cin >> pi;
    std::cout << "pi is: " << pi << '\n';
    return 0;
}
```

*Figure: A rounded blue rectangle representing an output or terminal window, containing the text "3.14" in the top-left corner.*

---

## Slide 126: std::cin

*Figure: An illustration of the std::cin input stream. At the top is a buffer diagram where a horizontal row of cells is labeled "cin" on the left. The first four cells contain the characters `3`, `.`, `1`, and `4`, and the fifth cell contains the newline character `'\n'`. A blue arrow points downward to the boundary between the '4' and the newline character. Below the buffer is a C++ code snippet, an explanatory callout, and a terminal output window.*

```cpp
int main()
{
double pi;
std::cin; /// what does this do?
std::cin >> pi;
std::cout << "pi is: " << pi << '\n';
return 0;
}
```

An orange arrow points from a callout box to the line `std::cin >> pi;`. The callout box contains the following text:
> cin not empty so it reads up to white space and saves it to **double pi**

*Terminal output window:*
```
3.14
```

---

## Slide 127: std::cin

*Figure: A diagram illustrating the use of `std::cin` in C++. At the top, the text "std::cin" is displayed in a large, bold font on an orange banner. Below it, a horizontal array represents the `cin` input buffer, with cells containing the characters '3', '.', '1', '4', and a newline character `'\n'`. An arrow points from the buffer to the cell containing the newline character. Below this, a code snippet is enclosed in a dotted rectangle. To the right, a label "cout" points to the output line, and a rounded rectangle contains the output text.*

```cpp
int main()
{
    double pi;
    std::cin; /// what does this do?
    std::cin >> pi;
    std::cout << "pi is: " << pi << '\n';
    return 0;
}
```

*Figure: A rounded rectangle representing the program output. It contains two lines of text:*
```
"3.14"
"pi is: 3.14"
```

---

## Slide 128: Alternatively

*Figure: A diagram showing the `cin` input buffer. It contains the characters '3', '.', '1', '4', and a newline character '\n' in consecutive boxes. An arrow points downward to the '\n' character, indicating it is the current character in the stream.*

```cpp
int main()
{
    double pi;
    std::cin >> pi; /// input directly!
    std::cout << "pi is: " << pi << '\n';
    return 0;
}
```

*Figure: An output example in a rounded rectangle, displaying the program's input and corresponding output:*
```
"3.14"
"pi is: 3.14"
```

---

## Slide 129: When std::cin fails!

*Figure: Diagram showing an empty input stream buffer labeled 'cin' represented as a row of adjacent rectangular cells. An arrow points downwards to the first cell of the buffer. To the right, three vertically stacked empty rectangular boxes are labeled 'pi', 'name', and 'tao', representing memory locations for variables.*

*Figure: Screenshot of a C++ code snippet within a dotted border.*

```cpp
int main()
{
    double pi;
    double tao;
    std::string name;
    std::cin >> pi;
    std::cin >> name;
    std::cin >> tao;
    std::cout << "my name is: " << name <<
              " tao is: " << tao << " pi is: " << pi << '\n';
    return 0;
}
```

---

## Slide 130: When std::cin fails!

*Figure: A diagram showing the state of the input buffer and program variables. At the top, the input buffer is labeled `cin` and contains the characters `3`, `.`, `1`, `4`, and `\n` (newline), each in its own cell. A blue arrow points down to the `\n` cell. Below, a dotted rectangle contains a C++ code snippet. To the right of the code, three rounded rectangles are stacked vertically, representing variables. The top rectangle contains the value `3.14` and is labeled `pi`. The middle rectangle is empty and labeled `name`. The bottom rectangle is empty and labeled `tao`. An orange arrow points from the code line `std::cin >> pi;` to a beige annotation box that reads: "`cin` prompts user to enter a value saved in **pi**".*

```cpp
int main()
{
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::cin >> name;
  std::cin >> tao;
  std::cout << "my name is: " << name <<
    " tao is: " << tao << " pi is: " << pi << '\n';
  return 0;
}
```

---

## Slide 131: When std::cin fails!

*Figure: A diagram illustrating the state of a `std::cin` input buffer and variables in a C++ program. At the top, a horizontal buffer labeled `cin` contains character cells: `3.14`, `\n`, `R`, `a`, `c`, `h`, `e`, `l`, ` `, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, `\n`, and two empty cells. A blue arrow points from the title down into the empty cell representing the space between "Rachel" and "Fernandez". To the right, three rounded boxes represent variable states: `pi` contains `3.14`, `name` contains `Rachel`, and `tao` is empty.*

```cpp
int main()
{
    double pi;
    double tao;
    std::string name;
    std::cin >> pi;
    std::cin >> name;
    std::cin >> tao;
    std::cout << "my name is: " << name <<
    " tao is: " << tao << " pi is: " << pi << '\n';
    return 0;
}
```

*Annotated box with an orange arrow pointing to the line `std::cin >> name;`: "cin prompts user to enter a value saved in name"*

*Variable values:*
- `pi`: `3.14`
- `name`: `Rachel`
- `tao`: *(empty)*

---

## Slide 132: When std::cin fails!

*Figure: A diagram illustrating a `cin` input failure scenario. At the top, a horizontal array of boxes represents the input buffer, containing the characters: `3 . 1 4 \n R a c h e l   F e r n a n d e z \n` (with `\n` in pink). A blue arrow points from above to the space character before "Fernandez". An orange arrow points from below to the space character after "Rachel". Below the buffer, a C++ code snippet is enclosed in a dotted rectangular border. To the right of the code, two rounded annotation boxes with text point to specific parts of the diagram: one points to the space in the buffer, the other points to the `std::cin >> name;` line in the code. Further to the right, three vertically stacked rounded boxes represent variables: the top contains "3.14" and is labeled "pi", the middle contains "Rachel" and is labeled "name", and the bottom is empty and labeled "tao".*

```cpp
int main()
{
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::cin >> name;
  std::cin >> tao;
  std::cout << "my name is: " << name <<
    " tao is: " << tao << " pi is: " << pi << '\n';
  return 0;
}
```

*   Notice that cin **only** reads until the next whitespace
*   **cin** prompts user to enter a value saved in **name**

Variables:
*   pi: 3.14
*   name: Rachel
*   tao: (empty)

---

## Slide 133: When std::cin fails!

*Figure: A horizontal array representing the `cin` input buffer containing the character sequence `3.14\nRachel Fernandez\n` followed by several empty cells. The newline characters `\n` are highlighted in magenta. A blue vertical arrow points down to the newline character immediately following "Fernandez".*

```cpp
int main()
{
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::cin >> name;
  std::cin >> tao;
  std::cout << "my name is: " << name << 
  " tao is: " << tao << " pi is: " << pi << '\n';
  return 0;
}
```

*Figure: To the right of the code block are three rounded rectangles representing variable storage states. The top box is labeled `pi` and contains the value `3.14`. The middle box is labeled `name` and contains the value `Rachel`. The bottom box is labeled `tao` and contains a red question mark `?`. A callout bubble points to the line `std::cin >> tao;` and contains the text: `cin buffer is not empty, so it reads until the next whitespace`.*

---

## Slide 134: When std::cin fails!

*Figure: At the top of the slide, a diagram of the `cin` input buffer shows a sequence of characters in individual cells: `3`, `.`, `1`, `4`, `\n` (in magenta), `R`, `a`, `c`, `h`, `e`, `l`, ` `, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, `\n` (in magenta), followed by empty cells. A blue arrow points down to the final `\n` character. The label `cin` is to the left of the buffer.*

```cpp
void cinFailure()
{
    double pi;
    double tao;
    std::string name;
    std::cin >> pi;
    std::cin >> name;
    std::cin >> tao;
    std::cout << "my name is: " << name << 
    " tao is: " << tao << " pi is: " << pi << '\n';
}
```

*Figure: To the right of the code, three rounded boxes display the resulting values of variables. An arrow points from a callout bubble to the line `std::cin >> tao;` in the code.*

*   *The top box contains `3.14` and is labeled `pi` to its right.*
*   *The middle box contains `Rachel` and is labeled `name` to its right.*
*   *The bottom box contains a red `0` and is labeled `tao` to its right.*

*Figure: The callout bubble contains the text: "**cin** buffer is not empty, so it reads until the next whitespace".*

---

## Slide 135: What questions do we have?

*Figure: A cartoon stick figure with a round head, a small frown, and a finger to its chin, appearing thoughtful. The figure is holding a blue, hexagonal C++ logo, from which smoke is rising, in its other hand.*

---

## Slide 136: Question on Fixing Issue
How do we fix this?
Anyone want to take a guess?

---

## Slide 137: Fix?

*Figure: A diagram of the `cin` input buffer. The buffer contains the characters `3`, `.`, `1`, `4`, followed by a newline `\n`, then the string `Rachel Fernandez`, and another newline `\n`. An arrow points to the character `3` at the start of the buffer. The label `cin` is to the left of the buffer cells.*

```cpp
void cinGetlineBug() {
    double pi;
    double tao;
    std::string name;
    std::cin >> pi;
    std::getline(std::cin, name);
    std::cin >> tao;
    std::cout << "my name is : " << name << " tao is : "
              " << tao
              << " pi is : " << pi << '\n';
}
```

*Figure: Three rounded boxes to the right of the code block, representing the values of variables after execution. From top to bottom, they contain the values `3.14` (labeled `pi`), `Rachel` (labeled `name`), and `0` (labeled `tao`, with the `0` shown in red text).*

---

## Slide 138: Fix?
*Figure: A diagram showing an input stream for `cin` and the state of variables after a buggy C++ function execution. The input stream is visualized as a sequence of characters: `3`, `.`, `1`, `4`, `\n` (newline, highlighted in pink), `R`, `a`, `c`, `h`, `e`, `l`, a space, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, `\n` (newline, highlighted in pink), followed by empty boxes. Blue arrows point from the title to the first `\n` and the space. The first four character boxes (containing `3.14`) are shaded purple. The word "cin" precedes the sequence. To the right of the code block are three rounded blue rectangles representing variables: the top one labeled "pi" contains the value `3.14`, the middle one labeled "name" is empty, and the bottom one labeled "tao" is empty.*

```cpp
void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is :
" << tao
            << " pi is : " << pi << '\n';
}
```

---

## Slide 139: Fix?

*Figure: A diagram showing the input buffer contents and a C++ function with a bug. The buffer contains the characters `3.14`, a newline character `\n`, then the string `Rachel Fernandez` followed by another newline `\n`. A blue arrow points to the newline character immediately after the `3.14`.*

```cpp
void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : "
            << tao
            << " pi is : " << pi << '\n';
}
```

*Annotation: A rounded rectangular box with the text "Any guesses for what happens here?" points toward the code block.*

On the right side of the slide, three boxes represent variable states:
*   **pi**: `3.14`
*   **name**: *[empty box]*
*   **tao**: *[empty box]*

---

## Slide 140: Fix?

*Figure: A diagram titled "Fix?" illustrating a common bug when mixing `std::cin >>` and `std::getline`. At the top is a representation of the `cin` input buffer containing the characters `3.14\nRachel Fernandez\n`. The first newline `\n` (highlighted in yellow) is positioned right after `3.14`. Below the buffer is a C++ function inside a dashed box. To the right of the code are boxes representing variable states and a callout explaining the behavior of `getline`.*

**cin buffer:** `3`, `.`, `1`, `4`, `\n` (highlighted in yellow), `R`, `a`, `c`, `h`, `e`, `l`, ` `, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, `\n`, (empty), (empty)

```cpp
void cinGetlineBug() {
    double pi;
    double tao;
    std::string name;
    std::cin >> pi;
    std::getline(std::cin, name);
    std::cin >> tao;
    std::cout << "my name is : " << name << " tao is : " << tao
              << " pi is : " << pi << '\n';
}
```

**Callout:**
> **getline** consumes the newline character

**Variable States:**
*   `pi`: `3.14`
*   `name`: `""`
*   `tao`: *(empty box)*

---

## Slide 141: Fix?

### `cinGetlineBug()` Function

```cpp
void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : "
            << tao << " pi is : " << pi << '\n';
}
```

*Figure: At the top, a visual representation of the `cin` input buffer. The buffer contains individual character cells reading: `3`, `.`, `1`, `4`, `\n`, `R`, `a`, `c`, `h`, `e`, `l`, ` `, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, `\n`, followed by empty cells. The first four characters (`3`, `.`, `1`, `4`) are highlighted in purple, indicating they were consumed by `cin >> pi`. The newline character `\n` immediately after `4` is highlighted in yellow, with a small downward arrow pointing to it from above. The remaining characters `Rachel Fernandez\n` are in unhighlighted cells.*

*Figure: To the right, a speech bubble states: "**tao** is going to be garbage because the buffer is not empty".*

*Figure: Three variable boxes are shown on the right side:*
- *Variable `pi` contains the value `3.14`*
- *Variable `name` contains an empty string `""`*
- *Variable `tao` contains a trash can icon, indicating garbage/uninitialized value*

---

## Slide 142: Fix?

*Figure: A diagram showing the state of the `cin` input stream. The stream contains the characters `3.14\nRachel Fernandez\n`, represented in colored blocks. The characters `3.14` are in purple blocks, the first `\n` (newline) is in a yellow block, `Rachel Fernandez` is in green blocks, and the final `\n` is in a pink block. A blue arrow points from the yellow `\n` block down to the beginning of the green `Rachel` block.*

```cpp
void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is :
" << tao
            << " pi is : " << pi << '\n';
}
```

*Figure: To the right of the code, three rounded rectangles show the state of variables: `pi` contains "3.14", `name` contains """" (an empty string represented by four double-quote characters), and `tao` contains a trash can icon (🗑), indicating it did not read a valid number.*

*Figure: A speech bubble pointing to the line `std::cin >> tao;` contains the text: "It's going to try to read the green stuff (name). But tao is a **double**!" (The word "double" is in blue text.)*

---

## Slide 143: How do we fix this?
How do we fix this?
Anyone want to take another guess?

---

## Slide 144: Fix?

*Figure: An input buffer for `cin` is depicted as a sequence of cells containing the characters: `3`, `.`, `1`, `4`, `\n`, `R`, `a`, `c`, `h`, `e`, `l`, ` `, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, `\n`. An arrow points from the label `cin` to the first cell of the buffer. Below the buffer, a C++ function `cinGetline` is shown. To the right of the function, there are three empty rectangular boxes stacked vertically, with the labels `pi`, `name`, and `tao` positioned to their right.*

```cpp
void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao << " pi is : " << pi << '\n';
}
```

---

## Slide 145: Fix?

*Figure: A diagram illustrating a C++ input stream problem. At the top is a horizontal array representing the `cin` buffer. The buffer contains the characters: `3.14`, followed by a newline `\n` (highlighted in pink), then `Rachel Fernandez`, and finally another newline `\n` (highlighted in pink). A blue arrow points down to the first newline character. Below the buffer is a dashed box containing a C++ function. To the right of the box are three rectangular variable boxes labeled `pi`, `name`, and `tao`. The `pi` box contains the value `3.14`. The `name` and `tao` boxes are empty.*

```cpp
void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is :
" << tao << " pi is : " << pi << '\n';
}
```

---

## Slide 146: Fix ✅

*Figure: An orange header bar at the top of the slide contains the text "Fix" followed by a green checkmark emoji.*

*Figure: Below the header is a diagram of the standard input stream (`cin`) buffer, represented as a series of boxes. The first four boxes contain the characters `3`, `.`, `1`, and `4`, which are highlighted in light purple. The fifth box contains a newline character `\n`, highlighted in yellow, with a small blue arrow pointing down at it from above. The subsequent boxes contain the characters `R`, `a`, `c`, `h`, `e`, `l`, a space, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, and another `\n`, followed by several empty boxes. The label "cin" is to the left of the buffer.*

*Figure: A dashed-line rectangle contains a C++ code snippet for a function named `cinGetline`.*

```cpp
void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : "
            << tao << " pi is : " << pi << '\n';
}
```

*Figure: To the right of the code block are three rounded-rectangle boxes representing the state of variables. The top box contains the value `3.14` and is labeled `pi` to its right. The middle box contains an empty string `""` and is labeled `name` to its right. The bottom box is empty and is labeled `tao` to its right.*

---

## Slide 147: Fix ✅

*Figure: A diagram illustrating the "fix" for a common C++ input stream issue. The top orange banner contains the title "Fix ✅" with a blue arrow pointing down to the end of the `cin` input buffer. The buffer is represented as a row of boxes containing `3.14`, a newline `\n`, the name `Rachel Fernandez`, and a final newline `\n`. The characters for `3.14` are in purple boxes, while the newline characters and the name are in yellow boxes. To the right of the code block, three memory boxes show the state of the variables: `pi` contains `3.14`, `name` contains "Rachel Fernandez", and `tao` is empty. In the code block itself, the first call to `std::getline` is grayed out, while the second call is highlighted in bold green as the solution.*

```cpp
void cinGetline() {
double pi;
double tao;
std::string name;
std::cin >> pi;
std::getline(std::cin, name);
std::getline(std::cin, name);
std::cin >> tao;
std::cout << "my name is : " << name << " tao is : " << tao << " pi is : " << pi << '\n';
}
```

---

## Slide 148: Fix ✅

*Figure: A diagram showing the state of the `cin` input stream buffer. The buffer labeled `cin` contains the characters `3`, `.`, `1`, `4`, `\n`, `R`, `a`, `c`, `h`, `e`, `l`, a space, `F`, `e`, `r`, `n`, `a`, `n`, `d`, `e`, `z`, and `\n`. A blue arrow points to the final `\n` at the end of the string.*

*Figure: A C++ code block and variable state annotations.*

```cpp
void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : "
            << tao << " pi is : " << pi << '\n';
}
```

*Figure: A callout box with the text: "The stream is empty! So it is going to prompt a user for input". To the right are three boxes representing variable states after the operations:*
*   *The box for `pi` contains the value `3.14`.*
*   *The box for `name` contains the value `Rachel Fernandez`.*
*   *The box for `tao` is empty.*

---

## Slide 149: Fix ✅

*Figure: A diagram illustrating the `cin` input stream buffer and how it is parsed into variables. The buffer contains the character sequence `3 . 1 4 \n R a c h e l   F e r n a n d e z \n 6 . 2 \n`, with each character and newline symbolized in individual colored boxes. A blue arrow points from the header area down to the buffer at the beginning of the `6.2` portion. To the right of the code block, three boxes show the final values assigned to variables: `3.14` for `pi`, `Rachel Fernandez` (on two lines) for `name`, and `6.2` for `tao`.*

```cpp
void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao << " pi is : " << pi << '\n';
}
```

---

## Slide 150: Whew that was a lot!

To conclude (Main takeaways):
1. Streams are a general interface to read and write data in programs
2. Input and output streams on the same source/destination type compliment each other!
3. Don't use `getline()` and `std::cin()` together, unless you *really really* have to!

*Figure: A meme in the bottom right corner showing a young boy (Harry Potter) waving from a train window. The text overlay at the bottom of the image reads: "BYE, I’M OFF TO HOGWARTS".*

---

## Slide 151: Acknowledgements

*Figure: A solid orange banner spanning the top of the slide, containing the title "Acknowledgements" in a large, bold, black font.*

Credit to **Avery Wang’s** streams lecture which I took a lot of inspiration from, particularly for formatting and flow.

Links on this slide:
- <https://web.stanford.edu/class/archive/cs/cs106l/cs106l.1204/lectures/types/types.pdf>
