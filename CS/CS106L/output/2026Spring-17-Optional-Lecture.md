# Lecture 17: Optional-Lecture (2026Spring)

> PDF title: 2026Spring-17-Optional-Lecture.pptx
> Source: `assets/slides/2026Spring-17-Optional-Lecture.pdf` · 18 pages · transcribed with `mimo-v2.5` · 2026-09-08

---

## Slide 1: Lecture 17: C++ Iceberg

*Figure: An "iceberg meme" illustrating various obscure, counter-intuitive, or "broken" features of the C++ programming language. The visible part above the waterline contains more well-known quirks, while the larger submerged part contains deeper, more obscure ones.*

*   0[arr]
*   #define private public
*   inline does not mean inline
*   C++ is not a superset of C
*   most vexing parse
*   \<iosfwd\>
*   spaceship operator
*   else if is a lie
*   digraphs
*   --> operator
*   protected abstract virtual base pure
*   virtual private destructor
*   vector\<bool\> is broken
*   unary minus with unsigned operand
*   analog integer literals
*   templates turing completeness was an accident
*   C++ fga lite
*   the strange details of std::string
*   std::move does not move
*   std::remove does not remove

CS106L, Spring 2026

Rachel Fernandez & Preston Seay

---

## Slide 2: Attendance

*Figure: A large black and white QR code centered on the slide.*

https://forms.gle/UFMH3U3i5g1aau7u8

Links on this slide:
- <https://forms.gle/UFMH3U3i5g1aau7u8>

---

## Slide 3: Today's Agenda

*   C++ Iceberg
*   Kahoot

---

## Slide 4: C++ Complexity Iceberg (Common Features vs. Deep Complexities)

*Figure: An image of an iceberg, with the tip above the water line and a much larger mass below. Various C++ features and concepts are placed on and below the iceberg as text labels.*

**Above the water line (Visible/Common Features):**
* `0[arr]`
* `#define private public`
* `inline does not mean inline`
* `most vexing parse`
* `C++ is not a superset of C`
* `<iosfwd>`
* `spaceship operator`
* `else if is a lie`
* `digraphs`
* `--> operator`
* `protected abstract virtual base pure virtual private destructor`

**Below the water line (Hidden/Complex/Problematic Details):**
* `vector<bool> is broken`
* `unary minus with unsigned operand`
* `templates turing completeness`
* `was an accident`
* `C++ fqa lite`
* `analog integer literals`
* `std::move does not move`
* `std::remove does not remove`
* `the strange details of std::string`

*Attribution: Lecture 17: Optional-Lecture (2026Spring)*

---

## Slide 5: → operator

```cpp
#include <stdio.h>
int main()
{
    int x = 10;
    while (x --> 0) // x goes to 0
    {
        printf("%d ", x);
    }
}
```

Yeah, it's actually this :(

*Figure: A small image showing the expression `(x-- > 0)` — demonstrating that `-->` is actually the post-decrement operator `x--` followed by the greater-than operator `> 0`.*

```
9 8 7 6 5 4 3 2 1 0
```

---

## Slide 6: C++ Iceberg Meme

- iostream was a mistake
- rvalue references are lvalues
- function try blocks
- T&& is not an rvalue reference
- shared_ptr is an anti-pattern
- initialization matrix
- the for loop is broken
- constexpr does not mean what you think it means
- implicit char* to bool& conversion
- const std::string bitand
- the grand error explosion competition
- operator, ()
- herbceptions
- templates are obfuscated haskell
- C++0x is a hexadecimal name
- heap and stack don't exist

*Figure: A meme showing a large iceberg submerged in dark blue water. Various C++ programming concepts, features, and controversial opinions are written in a white, slightly stylized font across the iceberg, creating a visual hierarchy of C++ complexity and lore.*

---

## Slide 7: else if is a lie

```cpp
#include <iostream>

int main() {
    int i = 10;

    if (false) {
        std::cout << "hello" << std::endl;
    } else while (i > 0) {
        std::cout << i << std::endl;
        --i;
    }
}
```

*Figure: Diagram illustrating that an "else" clause can be followed by a single statement (1-liner). The "1-liner" box points to three examples: "while..", "if..", and "doSomething()".*

---

## Slide 8: iostream is bad?
- “C’s printf family of functions is effective…”
- “It is not, however, type-safe or extensible…”
- “I started looking for a type-safe, terse, extensible, and efficient alternative…”
- Douglas McIlroy suggested it be similar to Unix streams: `>>`, `>`, and `|`
  - They considered `=` and `<` and `>`
- Andrew Koenig’s idea of manipulators

```cpp
int i = 1234;

cout << i << ' '           // decimal by default: 1234
    << hex << i << ' '        // hexadecimal: 4d2
    << oct << i << '\n';      // octal: 2322
```

*Figure: An image of the book cover for "The Design and Evolution of C++" by Bjarne Stroustrup. The cover features a green banner at the top with the text "Winner! Software Development Productivity Award" and a corresponding logo in the top-left corner. The main image shows a green oak leaf and an acorn on a forest floor. The title "The Design and Evolution of C++" is printed in large text over the image.*

Section 8.3.1: The I/O Stream Library

---

## Slide 9: iostream is bad?

Random guy on the internet:
*   “You get to an interface with fairly cryptic and confusing member function names, e.g. `getloc/imbue`, `uflow/underflow`, `snextc/sbumpc/sgetc/sgetn`, `pbase/pptr/epptr`”

Long story short:
*   Yes, there are some **shortcomings**.
*   It has been **improved** across versions by many ideas.
*   They made it **pretty far**: Ada Rationale [Ichbiah, 1979] argued that it was impossible to have terse, type-safe I/O without special language features.

---

## Slide 10: the for loop is broken

### The Promise:  
The range expression looks like it stays alive for the whole loop. It doesn’t always though!  

*Figure: Two code snippets (in gray boxes) illustrating the range - based for loop’s temporary lifetime issue. Left snippet: `for (auto e : getCollection())` with a label. Right snippet: `for (auto e : getCollection().getRef())` with labels.*  

Left code snippet (gray box):  
```cpp
for (auto e : getCollection())
```  

Label for left snippet:  
`getCollection()` returns a temporary. C++ goes okay! I’ll keep this alive for the whole loop  

Right code snippet (gray box):  
```cpp
for (auto e : getCollection().getRef())
```  

Label for right snippet:  
`.getCollection()` creates a temporary collection  
`.getRef()` returns a reference within the temp collection  
temporary collection = destroyed before loop begins. `getRef()` pointing to dead memory

---

## Slide 11: the for loop is broken

### The Promise:
The range expression looks like it stays alive for the whole loop. It doesn’t always though!

```cpp
for (auto e : getCollection())
```
*Figure: An arrow points from the explanation below to the `getCollection()` call in the code snippet.*
**`getCollection()`**
returns a temporary. C++
goes okay! I'll keep this
alive for the whole loop

```cpp
for (auto e : getCollection().getRef())
```
*Figure: An arrow points from the explanation below to the `.getRef()` call in the code snippet.*
**`.getCollection()`** creates a
temporary collection

**`.getRef()`** returns a reference
within the temp collection

### Caveat:
getCollection() allocates memory, then it expires, but
unless the memory gets taken, the data still is there
and the “loop” works

---

## Slide 12: The Preprocessor Iceberg

*Figure: An illustration of an iceberg with only its light-blue tip visible above a dark sea. Numerous text phrases related to deep and obscure C++ language features are scattered across the image, representing the "hidden" complexity beneath the surface.*

- C++0x is a hexadecimal name
- heap and stack don't exist
- hello world has a bug
- compilers disprove fermat's last theorem
- C++0x concepts were rust traits
- zapcc compiler
- i have no constructor and i must initialize
- ..... is valid syntax
- std::optional is a monad
- the preprocessor iceberg
- C++ active issues
- break abi to save C++
- abominable function types
- godbolt is a real person

---

## Slide 13: hello world has a bug

we wrote to /dev/full and it failed, which is what we wanted to see!

*Figure: Terminal screenshot showing a test of writing to /dev/full using the echo command. The command fails with a "No space left on device" error, and the exit code is 1.*

```
$ echo "Hello World!" > /dev/full
bash: echo: write error: No space left on device
$ echo $?
1
```

BUG! writes to the buffer, thinks its a success, and then errors after

*Figure: Terminal screenshot showing the compiled hello program being run and redirected to /dev/full. The program exits with code 0, indicating success, despite the write failure.*

```
$ gcc hello.c -o hello
$ ./hello > /dev/full
$ echo $?
0
```

the error definitely happened but the program ignored it!

*Figure: Terminal screenshot using strace to trace the write system call. It shows the write call returning -1 with ENOSPC (No space left on device), yet the program exits with status 0.*

```
$ strace -etrace=write ./hello > /dev/full
write(1, "Hello World!\n", 13)          = -1 ENOSPC (No space
+++ exited with 0 +++
```

---

## Slide 14: break abi to save c++

*   **ABI: Application Binary Interface**
    *   A low-level contract for code, such as: Calling Conventions, Data Representation, System Calls, Name Mangling, and Exceptions.

*Figure: A table titled "Arithmetic Operation" showing RISC-V style instructions with columns for Mnemonic, Instruction, Type, and Description.*

| Mnemonic | Instruction | Type | Description |
| :--- | :--- | :--- | :--- |
| `ADD rd, rs1, rs2` | Add | R | `rd ← rs1 + rs2` |
| `SUB rd, rs1, rs2` | Subtract | R | `rd ← rs1 - rs2` |
| `ADDI rd, rs1, imm12` | Add immediate | I | `rd ← rs1 + imm12` |
| `SLT rd, rs1, rs2` | Set less than | R | `rd ← rs1 < rs2 ? 1 : 0` |
| `SLTI rd, rs1, imm12` | Set less than immediate | I | `rd ← rs1 < imm12 ? 1 : 0` |
| `SLTU rd, rs1, rs2` | Set less than unsigned | R | `rd ← rs1 < rs2 ? 1 : 0` |
| `SLTIU rd, rs1, imm12` | Set less than immediate unsigned | I | `rd ← rs1 < imm12 ? 1 : 0` |
| `LUI rd, imm20` | Load upper immediate | U | `rd ← imm20 << 12` |
| `AUIP rd, imm20` | Add upper immediate to PC | U | `rd ← PC + imm20 << 12` |

*Figure: A screenshot of a blog post header. At the top left of the image, text reads "February 24, 2020" and "The Day The Standard Library Died". Below the text is a photograph of a classical statue of a bearded man with a muscular physique, holding a dagger or short sword aloft as if about to strike himself.*

[https://cor3ntin.github.io/posts/abi/](https://cor3ntin.github.io/posts/abi/)

Links on this slide:
- <https://cor3ntin.github.io/posts/abi/>

---

## Slide 15: break abi to save c++

- Improvements to the current std would break the ABI, so they aren't implemented:
  - “Making associative container (much) faster
  - “Making std::regex faster (it is currently faster to launch PHP to execute a regex than it is to use std::regex)”

*Figure: A diagram illustrating the concept of launching PHP to execute a regex instead of using C++'s std::regex. On the left is the blue hexagonal C++ logo. An arrow points from the C++ logo to the right, to the blue oval PHP logo containing the text "php". Another arrow points back from the PHP logo to the C++ logo. From the PHP logo, two arrows point to the right, towards the text "/Reg[ex]?/", which is displayed in a bold, stylized font representing a regular expression pattern.*

---

## Slide 16: break abi to save c++

*   **Additions** to the **std** would break the ABI, so they aren’t implemented:
    *   “unique_ptr could fit in register with language modifications, which would be needed to make it zero-overhead, compared to a pointer
    *   “Adding UTF-8 support to regex is an ABI break *Figure: A yellow sad face emoji with downturned mouth and furrowed brows.*
    *   “There seems to be a lot of people who believe that cost of exceptions could be greatly reduced as a quality of implementation matter but that might require breaking ABI.”

---

## Slide 17: KAHOOT TIME

*Figure: An illustration for Kahoot! with a space theme. The background is a dark purple with lighter purple clouds and stars. The word "Kahoot!" is written in large, white, playful letters in the center. Below it is a depiction of Earth with green continents and numerous colorful location pins. A rocket with an orange flame trail flies in the upper right. Several Kahoot! game icons (a rectangle with four colored shapes: red triangle, blue diamond, yellow circle, green square) are floating around the scene, including one with Saturn-like rings in the upper left.*

---

## Slide 18: Thank you for a great quarter!

Thank you for a great quarter!

*Figure: On the left, a photo of a smiling man wearing a red t-shirt with "NERD" printed on it. He is holding a black tray with a chocolate cake decorated with colorful icing letters that spell "PRESTON" and small round treats around the edge. In the background, there is a colorful mural and a red banner that says "BURBANK".*

<u>pseay@stanford.edu</u>

*Figure: On the right, a photo of a smiling woman with long dark hair, holding a small green parrot on her hand.*

<u>rfern@stanford.edu</u>

Links on this slide:
- <mailto:pseay@stanford.edu>
- <mailto:rfern@stanford.edu>
