# Lecture 03: InitializationAndReferences (2026Spring)

> Source: `assets/slides/2026Spring-03-InitializationAndReferences.pdf` · 55 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: CS106L: Lecture 3 Initialization & References

CS106L: Lecture 3
Initialization & References

Preston Seay, Rachel Fernandez

*Figure: A dark teal gradient background with centered white text.*

---

## Slide 2: Recap

auto

"Hey compiler, figure out this type."

*Figure: A diagram showing the word "auto" in a dark rounded box, with a blue arrow pointing right to another dark rounded box containing the quoted text "Hey compiler, figure out this type."*

*   Use at your discretion
*   Helpful when type is annoying

*Figure: A bulleted list contained within a dark rounded rectangular box.*

---

## Slide 3: Recap

*Figure: Screenshot of a code editor with a dark theme and a blue header displaying the title "Recap". The editor shows C++ source code with syntax highlighting and line numbers (which are omitted from transcription). The code includes several iterator declarations, with one explicitly typed version and one using `auto`, both highlighted with a yellow background.*

```cpp
#include <iostream>
#include <string>
#include <map>
#include <unordered_map>
#include <vector>

int main()
{
    std::map<std::string, std::vector<std::pair<int, std::unordered_map<char, double>>>>
    complexType;
    /// confusing iterator type (We'll find out what this is in the iterators lecture!)
    std::map<std::string,std::vector<std::pair<int,std::unordered_map<char,double>>>>::iterator
    it = complexType.begin();
    // clear(er) iterator type!
    auto it = complexType.begin();
    return 0;
}
```

---

## Slide 4: Recap

*Figure: A diagram with two labeled boxes on the left and two text boxes on the right, connected by blue arrows. The top left box contains the word "auto", with an arrow pointing to the top right text box that reads: "Hey compiler, figure out this type.". The bottom left box contains the word "struct", with an arrow pointing to the bottom right text box that reads: "Group these variables together, in one type, please 🥺.".*

---

## Slide 5: Life & Logistics

*Figure: A photograph shows two people, a woman on the left and a man on the right, standing outdoors in front of a building and trees. The man holds a yellow rubber duck mounted in a small wooden frame with a white base. An inset photo in the lower part of the main image shows a person with gray hair and glasses looking upward.*

### OH Preferences

*Figure: A large QR code in black and white.*

`https://forms.gle/JZ3kKbBKjS3ejq4N8`

Links on this slide:
- <https://forms.gle/JZ3kKbBKjS3ejq4N8>

---

## Slide 6: Plan
1. Initialization
2. References
3. L-values vs R-values
4. const
5. Compiling C++ programs

---

## Slide 7: Initialization

### What it is...

"**Provides initial values at the time of construction**"

*Figure: A dark-themed browser window titled "C++ Reference Definition" with "Open in new tab" in the top-right corner. The window displays a QR code and a text box containing a URL and instructions.*

The text content within the browser window:

- **C++ Reference Definition**
  - `https://en.cppreference.com/w/cpp/language/initialization.html`
  - Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://en.cppreference.com/w/cpp/language/initialization.html>

---

## Slide 8: Initialization

### What it is...
"Provides **initial** values at the time of construction"

### How to...
1. Direct initialization
2. Uniform initialization
3. Structured Binding

*Figure: A presentation slide titled "Initialization" on a dark teal background. The slide is organized into two columns. Each column has a small header box at the top and a larger content box below it. The left column header is "What it is...", and the content box below it contains the text: "Provides initial values at the time of construction", where the word "initial" is bolded. The right column header is "How to...", and the content box below it contains a numbered list: 1. Direct initialization, 2. Uniform initialization, and 3. Structured Binding, where the third item is partially cut off at the bottom of the box.*

---

## Slide 9: (1) Direct Initialization

*Figure: A screenshot of a code editor interface showing C++ code. The editor has "Code" and "Console" tabs at the top left, a "CPP" language indicator, and a "Run" button at the top right. Inside the editor, a red arrow points from a blue text box to the fifth line of code. The text box contains the question: "12.0 not an int... does this work?". To the right of the code, a large green box displays the word "YES".*

```cpp
#include <iostream>

int main() {
  int numOne = 12.0;
  int numTwo(12.0);
  std::cout << "numOne is: " << numOne << std::endl;
  std::cout << "numTwo is: " << numTwo << std::endl;
  return 0;
}
```

---

## Slide 10: (1) Direct Initialization

*Figure: A code editor interface displaying a C++ program. The editor has a dark theme with syntax highlighting. At the top left are two tabs labeled "Code" and "Console". At the top right are the language indicator "CPP" and a blue "Run" button. A dark blue, rounded button with the white text "Critical? Yes" is overlaid on the code editor, positioned between lines 9 and 11 of the code display.*

```cpp
#include <iostream>

void checkCool(float temperature) {
  if (temperature > 100.0) {
    std::cout << "Emergency cooling activated!" << std::endl;
  } else {
    std::cout << "Temperature normal. No emergency cooling required.";
  }
}

int main() {
  float temperatureReading(100.8);
  int temperature = temperatureReading;
  checkCool(temperature);
  return 0;
}
```

---

## Slide 11: (1) Direct Initialization

*Figure: A screenshot of a code editor showing C++ code. The editor has tabs for "Code" and "Console", and a blue "Run" button. Lines 12 and 13 of the code are highlighted with a translucent yellow box. To the right of the code, there is a text overlay containing a humorous comment from a compiler and the term "Narrowing Conversion" in yellow.*

```cpp
#include <iostream>

void checkCool(float temperature) {
  if (temperature > 100.0) {
    std::cout << "Emergency cooling activated!" << std::endl;
  } else {
    std::cout << "Temperature normal. No emergency cooling required.";
  }
}

int main() {
  float temperatureReading(100.8);
  int temperature = temperatureReading;
  checkCool(temperature);
  return 0;
}
```

C++ does not care
"You want 100.8 to be an integer? Okay 🤪" - compiler
**Narrowing Conversion**

---

## Slide 12: Initialization

*Figure: A presentation slide titled "Initialization" with a two-column layout. The left column features a header "What it is..." above a box containing the definition "Provides initial values at the time of construction". The right column features a header "How to..." above a box listing three methods: "1. Direct initialization", "2. Uniform initialization", and "3. Structured Binding".*

### What it is...
"Provides initial values at the time of construction"

### How to...
1. Direct initialization
2. Uniform initialization
3. Structured Binding

---

## Slide 13: (2) Uniform Initialization

*Figure: A screenshot of a C++ code editor (dark-themed IDE) with "Code" and "Console" tabs at the top left, "CPP" language label and a blue "Run" button at the top right. The editor contains line-numbered C++ code. Two annotation boxes overlay the screenshot: a green arrow points from a dark blue box reading "Notice the curly brackets!" to the curly brackets on line 3; a red arrow points from a dark blue box reading "12.0 not an int... does this work?" toward lines 4–5. A separate dark blue box at the bottom right contains the word "NO" in large red letters.*

```cpp
#include <iostream>

int main() {
    int numOne = {12.0};
    int numTwo{12.0};
    std::cout << "numOne is: " << numOne << std::endl;
    std::cout << "numTwo is: " << numTwo << std::endl;
    return 0;
}
```

---

## Slide 14: (2) Uniform Initialization

### Benefits:
1 . Safe
*   No narrowing conversion.

2 . Ubiquitous
*   Can use with vectors, maps, custom classes, etc.

---

## Slide 15: (2) Uniform Initialization

*Figure: A screenshot of a code editor window with a dark theme. The window has "Code" and "Console" tabs at the top left, a "CPP" language label, and a blue "Run" button at the top right. The editor displays C++ code with line numbers 1 through 15.*

```cpp
#include <iostream>
#include <map>

int main() {
    // Uniform initialization of a map.
    std::map<std::string, int> ages{
        {"Alice", 25},
        {"Bob", 30},
        {"Charlie", 35}
    };
    // Accessing map elements.
    std::cout << "Alice's age: " << ages["Alice"] << std::endl;
    std::cout << "Bob's age: " << ages.at("Bob") << std::endl;
    return 0;
}
```

---

## Slide 16: (2): Uniform Initialization

*Figure: A screenshot of a code editor window showing a C++ program. The window has tabs labeled "Code" and "Console" at the top left, and "CPP" and a "Run" button at the top right. The code is displayed with line numbers from 1 to 12 in a gutter on the left.*

```cpp
#include <iostream>
#include <vector>
int main() {
  // Uniform initialization of a vector.
  std::vector<int> numbers{1, 2, 3, 4, 5};
  // Accessing vector elements.
  for (int num : numbers) {
    std::cout << num << " ";
  }
  std::cout << std::endl;
  return 0;
}
```

---

## Slide 17: Recall

```cpp
StanfordID issueID() {
    StanfordID id;
    id.name = "THE Stanford Tree";
    id.sunet = "theTREE";
    id.idNumber = 0000002;
    return id;
}
```

*Figure: A large red downward-pointing arrow positioned between two code snippets.*

```cpp
StanfordID issueID() {
    StanfordID id = {"THE Stanford Tree", "theTREE", 0000002};
    return id;
}
```

---

## Slide 18: Initialization

### What it is...
"Provides initial values at the time of construction"

### How to...
1. Direct initialization
2. Uniform initialization
3. Structured Binding

*Figure: A presentation slide with a blue gradient background. The title "Initialization" is centered at the top. Below the title, the slide is divided into two columns. The left column features a small dark box with the text "What it is..." above a larger box containing the definition: "Provides initial values at the time of construction". The right column features a small dark box with the text "How to..." above a larger box containing a numbered list of techniques: "1. Direct initialization", "2. Uniform initialization", and "3. Structured Binding".*

---

## Slide 19: (3) Structured Initialization
*Figure: A teal gradient slide with a dark blue rounded rectangle containing white text.*

Initializes multiple variables from fixed-size data structures.
Access multiple values returned by a function.

---

## Slide 20: (3) Structured Binding

*Figure: A screenshot of a C++ online code editor/IDE. The top of the interface has "Code" and "Console" tabs on the left, and "CPP" and a blue "Run" button on the right. The editor displays a code snippet with line numbers from 1 to 17. Two specific sections of the code are highlighted in a yellowish-green color, with callout boxes next to them.*

```cpp
#include <iostream>
#include <tuple>
#include <string>

std::tuple<std::string, std::string, std::string> getClassInfo() {
    std::string className = "CS106L";
    std::string buildingName = "Thornton 110";
    std::string language = "C++";
    return {className, buildingName, language};
}

int main() {
    auto [className, buildingName, language] = getClassInfo();
    std::cout << "Come to " << buildingName << " and join us for " << className
              << " to learn " << language << "!" << std::endl;
    return 0;
}
```

*Annotation 1: A dark blue callout box points to the highlighted return statement on line 9: `return {className, buildingName, language};`. It contains the text:*
> What do we call this?
> *Uniform initialization*

*Annotation 2: A dark blue callout box points to the highlighted variable declaration on line 13: `auto [className, buildingName, language] = getClassInfo();`. It contains the text:*
> What do we call this?
> **Structured Binding**

---

## Slide 21: (3) Structured Binding

*Figure: Top-left meme: Drake in an orange puffer jacket, looking away with a displeased expression, rejecting the verbose code snippet on the right. The background is a dark blue to light blue gradient.*

```cpp
auto classInfo = getClassInfo();
std::string className = std::get<0>(classInfo);
std::string buildingName = std::get<1>(classInfo);
std::string language = std::get<2>(classInfo);
```

*Figure: Bottom-left meme: Drake in an orange puffer jacket, smiling and pointing approvingly at the concise code snippet on the right. The background is a dark blue to light blue gradient.*

```cpp
auto [className, buildingName, language] = getClassInfo();
```

---

## Slide 22: (3) Structured Binding

* Initializes multiple variables from fixed-size data structures.
* Access multiple values returned by a function.
* Size must be known at compile time.

---

## Slide 23: Plan
1. Initialization
2. References
3. L-values vs R-values
4. const
5. Compiling C++ programs

*Figure: The slide has a dark blue header bar containing the title "Plan" in white text. The main body has a teal-to-blue gradient background with a subtle rectangular border around the list.*

---

## Slide 24: References

### What they are...

> "An alias to an already-existing object or function."

*Figure: A panel on the right side of the slide titled "C++ Reference Definition" with a "Open in new tab" link in the top right. It contains a large QR code. Below the QR code, the text "C++ Reference Definition" is repeated, followed by the URL: `https://en.cppreference.com/w/cpp/language/reference.html`. Beneath the URL is the instruction: "Scan the code or open the URL in a browser to view the live page."*

Links on this slide:
- <https://en.cppreference.com/w/cpp/language/reference.html>

---

## Slide 25: References

*Figure: A slide with a dark blue background and a header bar titled 'References'. The main content area features four dark blue rounded rectangular boxes arranged in a 2x2 grid. The top-left box contains the text 'What they are...'. The top-right box contains the text 'How to...'. The bottom-left box contains the text '"An alias to an already-existing object or function."'. The bottom-right box contains a large white ampersand symbol '&'.*

What they are...
"An alias to an already-existing object or function."
How to...
&

---

## Slide 26: References Example

*Figure: A screenshot of an online code editor interface. At the top left, there are two tabs labeled "Code" and "Console," with "Code" currently selected. At the top right, the language "CPP" is displayed next to a blue "Run" button. The main area contains a C++ code snippet with syntax highlighting.*

```cpp
#include <iostream>

int main() {
    int miToMoon = 238855; // That's how far the moon is.
    std::cout << "Moon is " << miToMoon << "mi away." << std::endl;

    int& ISS = miToMoon;
    ISS -= 254; // That's how high the ISS is.

    std::cout << "ISS is " << ISS << "mi to moon." << std::endl;
    std::cout << "Moon is " << miToMoon << "mi away." << std::endl;
    return 0;
}
```

*Note: In the code, the ampersand (`&`) in the declaration `int& ISS` is highlighted with a semi-transparent yellow circle.*

---

## Slide 27: References Example

```cpp
int miToMoon = 238855;
int& ISS = miToMoon;
ISS -= 254;
```

*Figure: A diagram illustrating the execution of the code. On the right, a large box labeled "Memory" contains a smaller box labeled "miToMoon" with the value "238855" inside. Below this are several empty dark rectangles representing additional memory slots. A blue arrow points from the left side of the "Memory" diagram towards the code block on the left, indicating the relationship between the code and memory.*

---

## Slide 28: References Example

*Figure: A slide displaying a C++ code snippet on the left and a memory diagram on the right. A light blue arrow points to the second line of code.*

```cpp
int miToMoon = 238855;
int& ISS = miToMoon;
ISS -= 254;
```

*Figure: A memory diagram titled "Memory". It shows the variable `miToMoon` storing the value `238855`. Directly below it, a row for `ISS` containing the value `238855` is crossed out with a large red 'X', indicating that a reference does not occupy its own separate memory location. Several empty rectangular boxes representing memory slots are shown below the crossed-out row.*

---

## Slide 29: <n>: References Example

```cpp
int miToMoon = 238855;
int& ISS = miToMoon;
ISS -= 254;
```

*Figure: Left side shows a code snippet with three lines: initialization of an integer variable `miToMoon`, declaration of a reference `ISS` aliasing `miToMoon`, and a subtraction operation on the reference. A blue arrow points to the reference declaration line. Right side displays a memory diagram labeled "Memory" with a variable entry "ISS / miToMoon" holding the value 238855, followed by empty memory cells below.*

---

## Slide 30: References Example

*Figure: A diagram illustrating how C++ references affect memory. On the left, a dark-themed code editor shows three lines of code. A blue arrow points from the left side toward the third line of code. Another blue arrow points from the code editor box toward a label in the "Memory" diagram on the right. The memory diagram shows a column of slots, with the top slot labeled "ISS / miToMoon" containing the value "238601", where the "601" is highlighted in yellow.*

```cpp
int miToMoon = 238855;
int& ISS = miToMoon;
ISS -= 254;
```

### Memory

ISS / miToMoon: 238601

---

## Slide 31: Pass by Reference

```cpp
#include <iostream>
#include <math.h>

void squareN(int& n) {
  n = pow(n, 2);
}

int main() {
  int num = 5;
  squareN(num);
  std::cout << num << std::endl;
  return 0;
}
```

*Figure: A screenshot of a code editor window showing a C++ program. The editor has tabs for "Code" and "Console" and buttons for "CPP" and "Run". Three annotations are placed to the right of the code with blue arrows pointing to specific lines. The top callout box says "Note the ampersand!" and points to the `&` in the function parameter `int& n`. The middle callout box says "n is a reference to num." with arrows pointing to the parameter `n` and the variable `num` in the function call. The bottom callout box says "So num gets updated to 25." and points to the `std::cout` statement on line 11.*

---

## Slide 32: Recall: Pass by Value

**Code** **Console** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **CPP** **Run**

```cpp
#include <iostream>
#include <math.h>

void squareN(int n) {
n = pow(n, 2);
}

int main() {
int num = 5;
squareN(num);
std::cout << num << std::endl;
return 0;
}
```

**n** is a *copy* of **num**.

So **num** does not get updated.

*Figure: A screenshot of a code editor displaying a C++ program. Two dark blue callout boxes with blue arrows provide annotations. The first arrow points from the parameter `int n` in the `squareN` function definition and the variable initialization `int num = 5;` to a box that says "n is a copy of num." The second arrow points from the output statement `std::cout << num << std::endl;` to a box that says "So num does not get updated."*

---

## Slide 33: Recall: Pass by Value

*Figure: A side-by-side comparison of C++ code in an editor on the left and a memory state diagram on the right. A red arrow points from a line in the code to the corresponding memory entry.*

```cpp
#include <iostream>
#include <math.h>

void squareN(int n) {
    n = pow(n, 2);
}

int main() {
    int num = 5;
    squareN(num);
    std::cout << num << std::endl;
    return 0;
}
```

### Memory

| Variable | Value |
| :--- | :--- |
| `num` | 5 |
| `n` | ~~5~~ 25 |

*Figure: The red arrow originates from the line `n = pow(n, 2);` and points to the row for variable `n` in the memory diagram. In that row, the value `5` is crossed out with a red horizontal line, and the updated value `25` is displayed to its right.*

---

## Slide 34: Value vs Reference

### Value
```cpp
void squareN(int n) {
  n = pow(n, 2);
}
```
Copies the variable!  
(Can be expensive.)

### Reference
```cpp
void squareN(int& n) {
  n = pow(n, 2);
}
```
Uses the same variable  
& memory!  
(Can modify it!)

*Figure: A comparison slide titled "Value vs Reference". The slide has a two-column layout on a blue background. The left column is labeled "Value" and the right "Reference". Each column contains a syntax-highlighted code snippet in a dark editor-like box. The function signature in the left code box is `void squareN(int n) {`, with the parameter `int` highlighted in a yellow-green box. The function signature in the right code box is `void squareN(int& n) {`, with the parameter `int&` highlighted in a yellow-green box. Below each code box is a dark blue rounded rectangle containing descriptive text. The text under the "Value" code reads "Copies the variable! (Can be expensive.)". The text under the "Reference" code reads "Uses the same variable & memory! (Can modify it!)".*

---

## Slide 35: A Classic Reference Copy Bug

```cpp
#include <iostream>
#include <math.h>
#include <vector>

void shift(std::vector<std::pair<int, int>> &nums) {
    for (auto [num1, num2] : nums) {
        num1++;
        num2++;
    }
}
```

*Annotation: A blue callout box with a thumbs-up emoji points to the function parameter `&nums`, stating "Pass by Reference!".*
*Annotation: A blue callout box with a thumbs-up emoji points to the range-based for loop declaration `for (auto [num1, num2] : nums)`, stating "Structured Binding!".*
*Annotation: A large red box below the code states "Does not modify nums".*
*Figure: A meme image shows a character from an office setting with the text overlay "LOTS OF NOTHING DONE" at the top and "TIME TO GO HOME" at the bottom. The watermark "imgflip.com" is visible.*

---

## Slide 36: A Classic Reference Copy Bug

```cpp
#include <iostream>
#include <math.h>
#include <vector>
void shift(std::vector<std::pair<int, int>> &nums) {
    for (auto [num1, num2] : nums) {
        num1++;
        num2++;
    }
}
```

*Figure: A screenshot of C++ code in an editor. A red arrow points from the structured binding `auto [num1, num2]` in a range-based for loop to the vector `nums`, highlighting that each element (pair) is being copied into local variables. A blue callout box next to the loop body states "Each pair gets copied!"*

---

## Slide 37: A Classic Reference Copy Bug

*Figure: A screenshot of a C++ code snippet within a dark-themed code editor. The title "A Classic Reference Copy Bug" is centered at the top. The code shows a function `shift` that increments values within a vector of pairs. A bright green highlight is applied to the `auto&` declaration in the range-based for loop. A dark blue rounded-rectangle button with the text "Fixed!" is overlaid on the code near the increment statements. Gray vertical markers, indicating code changes, are visible in the editor's gutter next to lines 5 through 8.*

```cpp
#include <iostream>
#include <math.h>
#include <vector>
void shift(std::vector<std::pair<int, int>> &nums) {
  for (auto& [num1, num2] : nums) {
    num1++;
    num2++;
  }
}
```

---

## Slide 38: Plan

1. Initialization
2. References
3. L-values vs R-values
4. const
5. Compiling C++ programs

---

## Slide 39: Yay or nay?

*Figure: A thumbs-up emoji next to a line of code with the variable `x` and the value `5` highlighted in green.*
```cpp
int x = 5;
```
"Variables" can appear on left or right.

*Figure: A thumbs-down emoji next to a line of code with the value `5` highlighted in red.*
```cpp
int 5 = x;
```
"Values" can appear on the right.

*Figure: A thumbs-up emoji next to a line of code with `x;` highlighted in green.*
```cpp
int y = x;
```
"Values" **cannot** apeear on left.

---

## Slide 40: L-values & R-values

|                           | <span style="color:blue">**l-value**</span>         | <span style="color:red">**r-value**</span>           |
| :-----------------------: | :--------------------------------------------------: | :----------------------------------------------------: |
|        **Full Name**      |                      Locator Value                   |                        Read Value                       |
| Where with respect to equal sign? |                       left or right                      |                           right                          |
|         **Memory**        |                Has a memory address                |      Temporary value (No memory address)                |
|        **Example**        | <code>int <span style="color:blue">x</span> = 10;</code> <br> <code>int y = <span style="color:blue">x</span>;</code> | <code>int x = <span style="color:red">10</span>;</code> <br> <code>int y = <span style="color:blue">x</span>;</code> |

*Figure: A table comparing l-values and r-values. The header row contains "l-value" in blue and "r-value" in red. The table has four rows detailing full name, position relative to the equals sign, memory characteristics, and code examples. The background is a gradient from dark blue to teal.*

---

## Slide 41: L-values & R-values

```cpp
#include <iostream>
#include <math.h>
// note the ampersand
void squareN(int& n) {
    // calculates n to the power of 2
    n = pow(n, 2);
}
int main() {
    int num = 5;
    squareN(num);
    std::cout << num << std::endl;
    return 0;
}
```

& / reference
- Means it must be a non-temporary value (an L-value).

So, we must pass an L-value.

*Figure: A screenshot of a code editor displaying C++ code. A cyan callout box labeled "L or R?" points with an arrow to the `int&` parameter in the `squareN` function signature. Another cyan arrow points from a text box on the right to the `num` argument in the function call `squareN(num);` inside `main`.*

---

## Slide 42: L-values & R-values

*Figure: Code editor window displaying C++ code, with two annotated labels. To the right of the editor, a glitchy-style graphic of a silhouetted person kicking, with the text "TAKE THE L" in cyan and red (with white outline) on a teal background.*

```cpp
#include <iostream>
#include <math.h>
// note the ampersand
void squareN(int& n) {
    // calculates n to the power of 2
    n = pow(n, 2);
}
int main() {
    squareN(5);
    return 0;
}
```

- A blue arrow labeled "L" points to the ampersand (`&`) in the function parameter `int& n` of `squareN`.
- A blue arrow labeled "R" points to the integer literal `5` in the function call `squareN(5)`.

---

## Slide 43: Plan

1. Initialization
2. References
3. L-values vs R-values
4. `const`
5. Compiling C++ programs

*Figure: A slide with a dark teal-to-blue gradient background. At the top center, the word "Plan" is written in a large white sans-serif font. Below it, a list of five items is centered within a light blue, semi-transparent rounded rectangle.*

---

## Slide 44: Const

What it is...

"Such object cannot be modified."

*Figure: A dark side panel on the right titled "C++ Reference Definition" with a link "Open in new tab" in the top right corner. The panel contains a simulated browser window with three dots in its top left corner. Inside this window is a bold heading "C++ Reference Definition", a QR code on the left, a URL on the right, and an instruction below.*

**C++ Reference Definition**
[QR Code Image]
https://en.cppreference.com/w/cpp/language/cv.html

Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://en.cppreference.com/w/cpp/language/cv.html>

---

## Slide 45: Const & Reference

```cpp
#include <iostream>

int main() {
  std::vector<int> vec{ 1, 2, 3 };
  const std::vector<int> const_vec{ 1, 2, 3 };
  std::vector<int>& ref_vec{ vec };
  const std::vector<int>& const_ref{ vec };

  vec.push_back(3);
  const_vec.push_back(3);
  ref_vec.push_back(3);
  const_ref.push_back(3);
  return 0;
}
```

*Figure: Blue horizontal arrows point from the right edge of the code block to lines 9, 10, 11, and 12, highlighting the function calls.*

---

## Slide 46: Const & Reference

*Figure: A screenshot of a C++ code editor interface. At the top left are tabs for "Code" (highlighted) and "Console." At the top right are the labels "CPP" and a blue "Run" button. Below the top bar is a code editor window with line numbers 1 through 11 in a dark gutter and a C++ code snippet with syntax highlighting.*

```cpp
#include <iostream>

int main() {
  const int a = 5;

  int& b = a;
  b++;

  std::cout << a << std::endl;
  return 0;
}
```

---

## Slide 47: Const & Reference

*Figure: A diagram illustrating the restriction on binding a non-const reference to a const object. On the left, two code declarations are shown in dark blue boxes: `const int a` and `int& b`. On the right is a large golden padlock with the number "5" on its body and the word "const" at the bottom. A light blue arrow points from `const int a` to the padlock. Another light blue arrow points from `int& b` toward the padlock, but it is crossed out with a red X. In the bottom-left corner is a meme image of a man with text overlaid.*

**Meme Text:**
(compiler)
THAT IS NOT ALLOWED

**Diagram Labels:**
*   `const int a` (in a code box)
*   `int& b` (in a code box)
*   `5` (on the padlock)
*   `const` (on the padlock)

---

## Slide 48: Const & Reference

*Figure: A screenshot of a code editor window titled "Const & Reference". The interface includes tabs for "Code" (currently active) and "Console", a language indicator "CPP", and a "Run" button in the top right corner. The editor displays a C++ program with line numbers 1 through 11. A green rounded highlight is present around the `const int&` characters on line 6.*

```cpp
#include <iostream>

int main() {
    const int a = 5;

    const int& b = a;
    //b++;

    std::cout << a << std::endl;
    return 0;
}
```

---

## Slide 49: Plan

1. Initialization
2. References
3. L-values vs R-values
4. const
5. Compiling C++ programs

---

## Slide 50: Compiling

*Figure: A conceptual diagram illustrating the process of compiling a C++ program. The diagram is split vertically down the middle.*

### source.cpp

```cpp
#include <iostream>

int main() {
    std::cout << "hello";
    return 0;
}
```

### machine.exe

00110001
00110000
00110110
01101100

*Figure: A large red arrow labeled "Compiling" points from the source code on the left to the machine code on the right, representing the translation of human-readable code into binary format.*

---

## Slide 51: Compiling
*   C++ is compiled.
    *   It cannot be "interpreted" or run as it is, like Python.
*   C++ needs a compiler.
    *   A program that converts it from source code.
    *   clang and g++ are popular.
*   How to compile:

*Figure: Four colored boxes at the bottom of the slide explain the components of a compile command. From left to right: a green box says "g++ is our compiler program.", a teal box says "We specify we want c++ version 23.", a purple box says "We specify our input file(s) are main.cpp", and a grey-purple box says "Our output file should be named main.". In the main content box, four matching colored rectangles (green, teal, purple, maroon) are positioned after the text "How to compile:" to indicate where these components would appear in the actual command.*

---

## Slide 52: What you need to know...

*Figure: A diagram illustrating the transition from C++ source code to a compiled executable. On the left, a dark box titled "main.cpp" contains a code snippet. A large green play-style arrow points to the right, leading to another dark box titled "main" which displays three rows of binary data.*

**Left Box (main.cpp):**
```cpp
#include <iostream>

int main() {
    std::cout << "hello";
    return 0;
}
```

**Right Box (main):**
```
00110001
00110000
00110110
```

**Bottom Commands:**
*   **Compile:** `$ g++ --std=c++23 main.cpp -o main`
*   **Run:** `$ ./main` or on Windows: `$ .\main.exe`

---

## Slide 53: Applications of Parallel Computing

*Figure: A collage of four images representing different applications of high-performance computing and GPU technology.*

*   *Top-Left: A white autonomous vehicle, a Jaguar I-PACE equipped with a roof-mounted sensor suite, is parked on a city street. A person is standing near the front passenger door.*
*   *Top-Right: The NVIDIA CUDA logo is shown on a green digital-themed background. The logo consists of the stylized NVIDIA eye icon, the text "NVIDIA" below it, and "CUDA" further down, all centered over a glowing green graphic of a cooling fan and circuit board traces.*
*   *Bottom-Left: Two people are viewed from behind, looking at a large digital wall displaying several corporate logos. The visible logos are for AQR, DE Shaw & Co, Citadel, TWO SIGMA, Point 72, and DRW. One person is pointing toward the Citadel logo.*
*   *Bottom-Right: A screenshot from the video game Fortnite. Three character avatars are standing on the roof of a blue car, looking out over a vast landscape of islands, water, and buildings. A shrinking storm circle is visible in the sky, and a building in the distance is labeled "MEOWETLES".*

---

## Slide 54: <n>: TensorFlow

*Figure: TensorFlow logo consisting of an orange geometric "TF" shape and the word "TensorFlow" in large gray text on a dark background.*

*Figure: A collection of badges arranged in two rows. The first row includes: "python 3.10 | 3.11 | 3.12 | 3.13", "pypi package 2.21.0", "DOI 10.5281/zenodo.4724125", "openssf best practices passing". The second row includes: "openssf scorecard 7.2", "oss-fuzz build failing", "oss-fuzz build failing", "custom badge inaccessible", "Contributor Covenant v1.4 adopted". Each badge is a small rectangular graphic with text and color coding.*

*Figure: A rectangular box labeled "Documentation" containing the text "api reference".*

TensorFlow is an end-to-end open source platform for machine learning. It has a comprehensive, flexible ecosystem of tools, libraries, and community resources that lets researchers push the state-of-the-art in ML and developers easily build and deploy ML-powered applications.

*Figure: A dark green rectangular box with white text stating "The TensorFlow Core is written largely in C++ and it is composed of 2,000+ source files."*

---

## Slide 55: Recap
1. Use uniform initialization!
2. References can alias variables
3. You can only reference L-values
4. const ensures you can't modify a variable
