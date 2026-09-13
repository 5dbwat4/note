# Lecture 06: Iterators (2026Spring)

> PDF title: 2026Spring-06-Iterators.pptx
> Source: `assets/slides/2026Spring-06-Iterators.pdf` · 96 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Lecture 6: Iterators and Pointers

Lecture 6:
Iterators and Pointers
Stanford CS106L, Spring 2026
Rachel Fernandez & Preston Seay

*Figure: Two diagrams illustrating the lecture topics. On the left is a sequence diagram showing "Iterators" (labeled `begin`, `begin + 1`, and `end`) pointing to "Elements" (labeled `[0]`, `[1]`, `[2]`, `[3]`, and a dashed box representing the past-the-end iterator). Cyan arrows connect the element boxes sequentially. On the right is a diagram showing pointer syntax and memory addresses. The code `int val = 5;` and `int *ptr = &val;` is shown at the top. Below, two memory boxes are shown: one at address `0x83` containing `0xFE`, and one at address `0xFE` containing `5`. Curved arrows link the code to their respective memory locations, and a straight arrow points from the `0xFE` value to the box containing `5`.*

---

## Slide 2: Attendance Form QR Code

Welcome back! Link to Attendance Form ↓

*Figure: A large black-and-white QR code. The text above it indicates that scanning the code will provide a link to an attendance form.*

---

## Slide 3: Pop Quiz: Containers

*   Which type(s) lets you insert at the back and front equally efficiently?
*   Which type(s) requires a comparison operator on the element type?
    *   What type(s) can we use to get around this?
*   Which is *usually* faster: `unordered_set` or `set`? Why?

---

## Slide 4: Pop Quiz: Containers (Answers)

- Which type(s) lets you insert at the back and front equally efficiently?
  - ✅ `std::deque`
- Which type(s) requires a comparison operator on the element type?
  - ✅ `std::map`, `std::set`
- Which is *usually* faster: `unordered_set` or `set`? Why?
  - ✅ `std::unordered_set` (Hashing + small load factor)!

---

## Slide 5: What questions do you have?

What questions do you have?

*Figure: A portrait of Bjarne Stroustrup looking directly at the camera with his hand resting on his chin. He is wearing glasses and a patterned, multi-colored shirt. In the background, computer monitors and posters are visible, with one poster titled "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP".*

bjarne\_about\_to\_raise\_hand

---

## Slide 6: Last Time: Containers

*Figure: Four diagrams illustrating different container data structures.*
*   **Top-left:** A simple array (or vector) with four blue boxes. The indices labeled above are 0, 1, 2, 4. The values inside the boxes are 1, 2, 3, 4 respectively.
*   **Top-right:** A hierarchical structure, likely a vector of vectors or a multi-level array. Three blue squares at the top act as pointers or indices. Blue arrows point from each to an array below. The first array has elements [1, 9] with two empty gray slots before them. The second array has elements [7, 3, 2, 1]. The third array has elements [2, 9] with two empty gray slots after them.
*   **Bottom-left:** A binary tree (likely a BST) with pink nodes containing a string key and a numeric value. The root is ("CS106L", 42). Its left child is ("Chris", 31), and its right child is ("Nick", 51). The ("Nick", 51) node has a left child ("Keith", 14) and a right child ("Sean", 35).
*   **Bottom-right:** A hash table or map structure. A vertical gray array is shown with indices labeled 0 through 4. Red arrows point from specific indices to pink key-value structures. Index 0 points to ("Chris", 31). Index 2 points to ("Nick", 51). Index 3 points to ("Sean", 35). Indices 1 and 4 are empty.

---

## Slide 7: Range-based for loop universality

```cpp
for (const auto& elem : container)
```

*Figure: A diagram illustrating the versatility of the range-based for loop. The code `for (const auto& elem : container)` is displayed in the center. Above it, four labels for standard library containers—`std::map`, `std::vector`, `std::set`, and `std::deque`—are shown in red text with black arrows pointing down to the word `container`. Below and to the right, a rectangular box containing the text "How does this work?" has a curved arrow pointing up toward the loop syntax.*

---

## Slide 8: For-each loops... huh?

```cpp
std::vector<int> v { 1, 2, 3, 4 };

for (const auto& elem : v) {
    std::cout << elem << std::endl;
}
```

*Figure: A diagram illustrating a vector of integers. It consists of four adjacent blue boxes arranged horizontally. Above the boxes, the index labels are 0, 1, 2, and 4. Inside the boxes, from left to right, are the values 1, 2, 3, and 4.*

---

## Slide 9: For-each loops... huh?

```cpp
std::deque<int> d {
    1, 9, 7, 3,
    2, 1, 2, 9
};

for (const auto& elem : d) {
    std::cout << elem << std::endl;
}
```

*Figure: A diagram showing the internal memory layout of a `std::deque`. There are three blue rectangles (representing chunks or pointers to memory blocks) at the top. Below them is a contiguous row of boxes representing the container's elements. The row contains 10 slots: the first two are gray (empty), the next eight are blue and contain the numbers `1`, `9`, `7`, `3`, `2`, `1`, `2`, `9`, and the final two are gray (empty). Blue arrows point from the top rectangles to specific positions in the bottom row: one arrow points from the leftmost blue rectangle to the first element (`1`), and two arrows point from the middle blue rectangle to the fifth and sixth elements (`2` and `1`). This illustrates how a deque's elements are distributed across separate memory chunks.*

---

## Slide 10: For-each loops… huh?

```cpp
std::map<std::string, int> m {
    { "Chris", 31 }, { "CS106L", 42 },
    { "Keith", 14 }, { "Nick", 51 },
    { "Sean", 35 },
};

for (const auto& pair : m) {
    std::cout << pair.first << " ";
    std::cout << pair.second;
}
```

*Figure: Diagram of the internal binary search tree structure of the `std::map`. The root node is labeled "CS106L" with value 42. It has two child nodes: "Chris" (value 31, left child) and "Nick" (value 51, right child). The "Nick" node has two child nodes: "Keith" (value 14, left child) and "Sean" (value 35, right child). Each node is a two-section box: the left section holds the string key, the right section holds the integer value.*

---

## Slide 11: For-each loops... huh?

```cpp
std::unordered_map<string, int> m
{
    { "Chris", 31 }, { "Nick", 51 },
    { "Sean", 35 },
};

for (const auto& pair : m) {
    std::cout << pair.first << " ";
    std::cout << pair.second;
}
```

*Figure: A diagram illustrating the internal structure of the `unordered_map` `m`. A vertical array of 5 buckets (indices 0-4) is shown. Bucket 0 contains a red arrow pointing to a pink rectangle labeled `"Chris"` next to a gray rectangle with the number `31`. Bucket 2 contains a red arrow pointing to a pink rectangle labeled `"Nick"` next to a gray rectangle with the number `51`. Bucket 3 contains a red arrow pointing to a pink rectangle labeled `"Sean"` next to a gray rectangle with the number `35`. Buckets 1 and 4 are empty gray rectangles.*

---

## Slide 12: Range-based for loop inquiry

```cpp
for (const auto& elem : container)
```

*Figure: An arrow points from a rectangular text box up to the `const auto&` portion of the code line. The text box contains the question "How does this work?".*

---

## Slide 13: Lecture 6: Iterators
Lecture 6: Iterators

CS106L, Spring 2026

---

## Slide 14: The Standard Template Library (STL)

*Figure: A diagram illustrating the four main components of the Standard Template Library (STL). Four rounded rectangular boxes are arranged in a 2x2 grid within a larger tan-colored container. The "Iterators" box is highlighted in light blue, while the "Containers", "Functors", and "Algorithms" boxes are light grey.*

*   **Containers**
    *   *How do we store groups of things?*
*   **Iterators**
    *   *How do we traverse containers?*
*   **Functors**
    *   *How can we represent functions as objects?*
*   **Algorithms**
    *   *How do we transform and modify containers in a generic way?*

---

## Slide 15: Today's Agenda
*   Iterator Basics
    *   What even is an iterator?
*   Iterator Types
    *   Iterators are organized by their properties
*   Pointers and Memory
    *   What is a pointer? What is memory?

---

## Slide 16: Q&A Prompt

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, the creator of C++. He is wearing glasses and a patterned shirt, resting his chin on his hand in a thoughtful pose. In the background, posters or book covers are visible; one prominently displays the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". The image has the caption `bjarne_about_to_raise_hand` below it.*

---

## Slide 17: Iterator Basics

---

## Slide 18: Question: How do we iterate?

*Figure: A rectangular box with a black border and a subtle drop shadow, containing two code examples.*

```cpp
std::vector<int> v {1,2,3,4};
for (size_t i = 0; i < v.size(); i++) {
const auto& elem = v[i];
std::cout << elem;
}
```

```cpp
for (var-init; condition; increment) {
const auto& elem = /* grab element */;
/* do something with elem */
}
```

---

## Slide 19: Question: How do we iterate?

```cpp
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}
```

*Figure: A callout/speech bubble with text "for (auto e : s) is not allowed ...for now" with an arrow pointing to the for-loop code above.*

```cpp
std::set<int> s {1,2,3,4};
for (uhhh; ummm; what?) {
    const auto& elem = /* haeelp 🥺🥺 */;
}
```

---

## Slide 20: Tracking Position in a Container
We need something to track **where we are** in a container... sort of like an index

---

## Slide 21: Introducing iterators

**Introducing** *iterators* 😎😎

---

## Slide 22: C++ iterators are like a “claw” in a claw machine

*Figure: On the left, an image of a metallic, three-pronged claw mechanism with a coiled black cable and a small red tip. On the right, an image of a red claw machine arcade game, its glass case containing colorful wrapped items. A text box is placed next to each image.*

**The claw can:**

1.  Grab a toy
2.  Move forward
3.  Check if we’re done

**The machine can:**

1.  Tell us where to start
2.  Tell us when to stop

---

## Slide 23: C++ Iterators Example

*Figure: A conceptual diagram using Toy Story alien characters to illustrate the step-by-step process of using an iterator in a C++ container (`c`). The diagram shows a sequence of aliens, each representing an iterator position, connected by red arrows indicating progression. Code snippets are annotated near the relevant aliens. The sequence begins with an alien under a claw crane, progresses through several aliens, and ends with a gray outline of an alien representing the past-the-end position.*

`auto it = c.begin();` (with `auto` in red, the rest in purple)
*An alien under a claw crane. A red arrow points up and to the right to the next alien.*
`++it;` (in purple)
*Next alien. A red arrow points down and to the right to the next alien.*
`++it;` (in purple)
*Next alien. A red arrow points up to the next alien.*
`++it;` (in purple)
*Next alien. A red arrow points down and to the right to the next alien.*
`++it;`
`auto elem = *it;` (with `auto` in red, the rest in purple)
*Next alien. A red arrow points up to the next alien.*
`++it;` (in purple)
*Next alien. A red arrow points down and to the right to the final position.*
`++it;`
`it == c.end()` (in purple)
*A gray outline of an alien.*

---

## Slide 24: Containers and Iterators
Containers and iterators **work together** to allow iteration

---

## Slide 25: Container Interface

`container.begin()`

Gets an iterator to
the **first element**
of the container
(assuming non-empty)

*Figure: A diagram of a container holding the characters 'd', 'a', 'w', 'g', 's' in adjacent cells. An arrow points upward to the first cell containing the character 'd'.*

---

## Slide 26: Container Interface

### `container.begin()`
Gets an iterator to the **first element** of the container (assuming non-empty)

*Figure: A diagram of an array containing five characters: 'd', 'a', 'w', 'g', 's'. A vertical arrow points upward from below the array directly to the first element, 'd'.*

### `container.end()`
Gets a **past-the-end** iterator
That is, an iterator to one element **after** the end of the container

*Figure: A diagram of an array containing five characters: 'd', 'a', 'w', 'g', 's', followed by an additional empty cell with a diagonal slash through it. A vertical arrow points upward from below the array to this final empty cell.*

---

## Slide 27: end() never points to an element!

*Figure: A conceptual diagram using three solid green Toy Story alien figures (representing elements in a container) arranged left-to-right, connected by red right-pointing arrows. A final dashed outline alien (representing a non-existent element) sits at the end of the sequence, with a red arrow pointing to it from the third alien. A gray upward arrow points to the first alien, and a second gray upward arrow points to the dashed alien. A white rectangular text box is positioned below the arrows.*

`c.begin()`

`c.end()`

Instead, it points **one past the end** of the container

---

## Slide 28: end() never points to an element!

If **c** is empty, then
**begin()** and **end()** are
equal!

*Figure: A diagram illustrating the case of an empty container `c`. A gray silhouette of a monster-like creature is shown. Two gray arrows point to the same silhouette. The left arrow is labeled `c.begin()` and the right arrow is labeled `c.end()`. Between the two labels is an equals sign (`==`), indicating that for an empty container, the `begin()` and `end()` iterators are equal.*

---

## Slide 29: Iterator Interface

```cpp
// Direct initalization
auto it = c.begin();
```

```cpp
// Increment iterator forward
++it;
```

```cpp
// Dereference iterator -- undefined if it == end()
auto& elem = *it;
```

```cpp
// Equality: are we in the same spot?
if (it == c.end()) ...
```

---

## Slide 30: We have an answer now!

We have an answer now!

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}
```

```cpp
for (                   ;              ;     ) {
    const auto& elem = /* grab element */;
}
```

*Figure: A callout box located to the top-right of the code snippets contains the text "for (auto e : s) is not allowed ...for now". The text "for (auto e : s)" is in purple. A curved black arrow points from the bottom-left of this box toward the code area.*

---

## Slide 31: We have an answer now!

*Figure: A large white box containing C++ code. To the right, a speech bubble with a black arrow points into the box.*

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}

for (auto it = s.begin();            ;    ) {
    const auto& elem = /* grab element */;
}
```

*Figure: A speech bubble with a black arrow pointing towards the code box. Inside the bubble is the text:*

for (auto e : s) is not allowed ...for now

---

## Slide 32: We have an answer now!

*Figure: A slide titled "We have an answer now!". The slide features two main boxes. The larger box on the left contains code examples. A smaller note box on the right contains the text "for (auto e : s) is not allowed ...for now" with a curved black arrow pointing from the note box toward the code in the larger box.*

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}

for (auto it = s.begin(); it != s.end();     ) {
    const auto& elem = /* grab element */;
}
```

*Note text (in right box):* for (auto e : s) is not allowed ...for now

---

## Slide 33: We have an answer now!

*Figure: A code block containing two C++ loop structures. To the right, a callout box with a black arrow pointing to the code block contains the text "for (auto e : s) is not allowed ...for now".*

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}

for (auto it = s.begin(); it != s.end(); ++it) {
    const auto& elem = /* grab element */;
}
```

---

## Slide 34: We have an answer now!

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}

for (auto it = s.begin(); it != s.end(); ++it) {
    const auto& elem = *it;
}
```

*Figure: A callout box in the upper right corner contains the text "for (auto e : s) is not allowed ...for now". An arrow points from this box toward the first code block.*

---

## Slide 35: Range-based for loop expansion

### When you write…

```cpp
for (auto elem : s)
{
    std::cout << elem;
}
```

*Figure: A yellow surprised-face emoji 🙀.*

### It’s actually this:

```cpp
auto b = s.begin();
auto e = s.end();

for (auto it = b; it != e; ++it) {
    auto elem = *it;
    std::cout << elem;
}
```

---

## Slide 36: What questions do you have?

*Figure: Photo of Bjarne Stroustrup with glasses and a patterned shirt, hand near face. Large text "What questions do you have?" overlaid on the image. Background includes a poster with "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP".*

bjarne_about_to_raise_hand

---

## Slide 37: We have an answer now!

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}

for (auto it = s.begin(); it != s.end(); ++it) {
    const auto& elem = *it;
}
```

*Figure: A callout box with a shadow contains the text: "for (auto e : s) is not allowed ...for now". A black arrow points from this box down toward the first for loop in the code snippet.*

---

## Slide 38: Guess we're done here!

*Figure: A classic Looney Tunes "That's all Folks!" end screen. The image features concentric red and dark red circles creating a tunnel effect, with a solid blue circle in the center. Overlaid on the circles is the text "That's all Folks!" in white cursive font with a slight shadow, enclosed in double quotation marks. The overall image has a vintage cartoon ending style.*

"That's all Folks!"

---

## Slide 39: We have an answer now!

```cpp
std::set<int> s {1,2,3,4};
for (var-init; condition; increment) {
    const auto& elem = /* grab element */;
}
```

```cpp
for (auto it = s.begin(); it != s.end(); ++it) {
    const auto& elem = *it;
}
```

*Figure: A diagram with two boxes. The first box contains text: "for (auto e : s) is not allowed ...for now". An arrow points from this box to the first code block. A second box contains the text: "What type is this?". An arrow points from this box to the variable `it` in the line `for (auto it = s.begin(); ...` in the second code block.*

---

## Slide 40: What are the types?

Using auto avoids spelling out long iterator types  

```cpp
std::map<int, int> m { {1, 2}, {3, 4}, {5, 6}};  
auto it = m.begin();  
auto elem = *it;            // {1, 2}  
```  

```cpp
std::map<int, int> m { {1, 2}, {3, 4}, {5, 6}};  
std::map<int, int>::iterator it = m.begin();  
std::pair<int, int> elem = *it;  
```

---

## Slide 41: Remember: using makes a type alias

*Figure: A code block inside a container box. A large arrow points from the last line of code to a callout box which contains the text: "Iterator types are really long, so we like to use **auto** with iterators".*

```cpp
// Inside <map> header
template <typename K, typename V>
class std::map {
    using iterator = /* some iterator type */;
};

// Outside <map> header (e.g. main.cpp)
std::map<int, int>::iterator it = m.begin();
```

---

## Slide 42: Aside: Why do we use ++it instead of it++?

Aside: Why do we use `++it` instead of `it++`?

---

## Slide 43: ++it avoids making an unnecessary copy

*Figure: Two horizontal white boxes with thin black borders stacked vertically. Each box contains two lines of grey comment text followed by one line of code in a monospaced font.*

```cpp
// Prefix form - ++it
// Increments it and returns a reference to same object
Iterator& operator++();
```

```cpp
// Postfix form - it++
// Increments it and returns a copy of the old value
Iterator operator++(int);
```

**Remember:** an iterator is a fully-fledged object, so it’s often more expensive to copy than, say, an **int**

---

## Slide 44: Does it actually make a difference?

Does it actually make a difference?

---

## Slide 45: Bjarne's Thoughts

“
++i is sometimes faster than, and is never slower than, i++. ... So if you’re writing i++ as a statement rather than as part of a larger expression, why not just write ++i instead? You never lose anything, and you sometimes gain something.

*Figure: A photograph of a man with light hair and glasses. The word "yup" is overlaid in white text on his face.*

[source]

Links on this slide:
- <https://isocpp.org/wiki/faq/operator-overloading#increment-pre-post-speed>

---

## Slide 46: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, creator of C++. He is wearing a patterned shirt and glasses, with his hand resting near his chin as if about to raise it. In the background, a poster is visible with the text "BJARNE STROUSTRUP" and "PROGRAMMING LANGUAGE".*

bjarne_about_to_raise_hand

---

## Slide 47: Your Turn

Trace this code with a partner to find out where each iterator points

```cpp
std::map<int, int> m {
    {1, 2}, {3, 4}, {5, 6}
};
auto a = m.begin();
++a;
auto b = a;
++a;
auto c = ++a;
```

*Figure: A diagram illustrating a `std::map` with three pairs of key-value boxes: `[1, 2]`, `[3, 4]`, and `[5, 6]`, followed by a dashed empty box. Above the boxes, a purple arrow labeled `m.begin()` points to the first pair `[1, 2]`, and another purple arrow labeled `m.end()` points to the dashed empty box. Below the boxes, red arrows indicate the final positions of iterators: `a` points to the first pair `[1, 2]`, `b` points to the second pair `[3, 4]`, and `c` points to the dashed empty box.*

---

## Slide 48: Iterator Types
Iterator Types

---

## Slide 49: Not all iterators are made equal

---

## Slide 50: All iterators provide these four operations

### All iterators provide these four operations

*   `auto it = c.begin();` &emsp; `++it;`
*   `*it;` &emsp; `it == c.end()`

### But most provide even more

*   `--it; // Move backwards` &emsp; `*it = elem; // Modify`
*   `it += n; // Rand. access` &emsp; `it1 < it2 // Is before?`

*Figure: The slide displays eight code snippets, each inside a rounded rectangle with a subtle drop shadow. They are arranged in two groups of four (two rows of two per group). The first group, under the heading "All iterators provide these four operations", shows the four fundamental iterator operations: `auto it = c.begin();`, `++it;`, `*it;`, and `it == c.end()`. The second group, under the heading "But most provide even more", shows four additional operations: `--it; // Move backwards`, `*it = elem; // Modify`, `it += n; // Rand. access`, and `it1 < it2 // Is before?`. Syntax highlighting is present — keywords like `auto` are red, method names like `begin` and `end` are purple, and comments are gray.*

---

## Slide 51: Iterator types determine their functionality

*Figure: A diagram illustrating the hierarchy and types of iterators. On the left, four light blue boxes are arranged in a vertical stack: "Random Access" at the bottom, followed by "Bidirectional", "Forward", and "Input" at the top. Black upward-pointing triangles connect each box to the one above it, indicating a hierarchy of functionality. To the right of "Input" is another light blue box labeled "Output" with a black upward-pointing triangle below it. To the far right, a white rectangular box with a drop shadow contains the text "Let's unpack this!".*

---

## Slide 52: Input Iterators
*   Most basic kind of iterator
*   Allows us to read elements

```cpp
auto elem = *it;
```

*Figure: A Venn diagram with two overlapping circles. The top-left circle is blue and labeled "INPUT". The bottom-right circle is pink and labeled "OUTPUT". Below the diagram is the caption text "Vivid Venn Diagram of Vexing Iterators".*

---

## Slide 53: Input Iterators

*   Most basic kind of iterator
*   Allows us to read elements

*Figure: Screenshot of a C++ code editor showing a simple program that uses `std::istream_iterator` to read integers from standard input into a vector.*

```cpp
#include <iostream>
#include <iterator>  // for std::istream_iterator
#include <vector>

int main() {
    std::cout << "Enter numbers (Ctrl+D to stop):\n";

    std::istream_iterator<int> start(std::cin);  // start reading from cin
    std::istream_iterator<int> end;              // default constructor = end-of-stream
                                                // marker

    std::vector<int> numbers(start, end);         // read all numbers into a vector
}
```

---

## Slide 54: Input Iterators

*Figure: A C++ code snippet titled "Input Iterators" displayed within a light-bordered box. The code demonstrates reading integers from standard input using `std::istream_iterator`.*

```cpp
#include <iterator>
#include <iostream>

int main() {
    std::istream_iterator<int> it(std::cin); // points at first int
    std::istream_iterator<int> end;          // default = end of stream

    while (it != end) {
        std::cout << *it << " ";   // read current value
        ++it;                     // consume it, advance to next
    }

    return 0;
}
```

---

## Slide 55: Input Iterators: operator->

If the element is a struct, we can access its members with ->

```cpp
struct Bibble {
    int zarf;
};

std::vector<Bibble> v {...};
auto it = v.begin();
int m = (*it).zarf;
int m = it->zarf;        // Exactly the same as prev!
```

*Figure: A white dictionary-style definition box that reads "Bibble, v. 'To eat and/or drink noisily'". To the right and partially overlapping this box is a photograph of three ornate, enameled goblets (zarfs) featuring intricate blue, gold, and green floral patterns.*

---

## Slide 56: Input and Output Iterators

Input Iterators
- Most basic kind of iterator
- Allows us to read elements
```cpp
auto elem = *it;
```

Output Iterator
Allows us to write elements
```cpp
*it = elem;
```

*Figure: A Venn diagram titled "Vivid Venn Diagram of Vexing Iterators". The diagram shows two overlapping circles. The larger, light-blue circle is labeled "INPUT". The smaller, light-pink circle is labeled "OUTPUT". The circles overlap on their right and left edges respectively, indicating a potential intersection of concepts.*

---

## Slide 57: Output Iterator

*Figure: A code example inside a light blue-bordered box demonstrating the use of a C++ output iterator (`ostream_iterator`).*

```cpp
#include <iterator>
#include <iostream>

int main() {
    std::ostream_iterator<int> it(std::cout, ", ");

    *it = 10;    // prints "10, "
    ++it;        // advance (mostly a no-op for streams)
    *it = 20;    // prints "20, "
    ++it;
    *it = 30;    // prints "30, "

    // output: 10, 20, 30,

    return 0;
}
```

---

## Slide 58: Output Iterator

*Figure: A code example demonstrating the use of a `std::back_insert_iterator` with a `std::vector`. The code is enclosed in a rectangular box.*

```cpp
#include <iterator>
#include <iostream>

int main() {
    std::vector<int> v;
    std::back_insert_iterator<std::vector<int>> it(v);

    *it = 10;    // calls v.push_back(10)
    ++it;
    *it = 20;    // calls v.push_back(20)
    ++it;
    *it = 30;    // calls v.push_back(30)

    // v is now {10, 20, 30}

    return 0;
}
```

---

## Slide 59: Forward Iterator

*   An input iterator that allows us to make multiple passes
*   All STL container iterators fall here

*Figure: A Venn diagram with two overlapping circles. The top-left circle is blue and contains the text "INPUT" with the word "FORWARD" overlaid on it. The bottom-right circle is pink and contains the text "OUTPUT".*

*Figure: A rectangular box labeled "Multi-pass guarantee". Inside, it shows the expression `it1 == it2` followed by a red downward-pointing arrow leading to the expression `++it1 == ++it2`.*

*Figure: A rectangular box containing the question "What kind of data structure might not want a multi-pass iterator?" with the answer "Streams!!!" written in red text below it.*

---

## Slide 60: Forward Iterator

```cpp
#include <iterator>
#include <iostream>

int main() {
    // istream_iterator – input only
    auto it1 = std::istream_iterator<int>(std::cin);
    auto it2 = it1;   // "copy" but both are looking at the same stream

    ++it1;            // reads from stream, advances stream position
    ++it2;            // stream already moved! it2 is now in an undefined state

    return 0;
}
```

*Figure: A code snippet demonstrating the behavior of an `istream_iterator`. The text "input only" is highlighted with an orange rounded rectangle, and the phrase "it2 is now in an undefined state" is underlined with a solid red line.*

---

## Slide 61: Bidirectional Iterators
*   Allows us to move forwards *and* backwards
*   `std::map`, `std::set`

```cpp
auto it = m.end();

// Get last element
--it;
auto& elem = *it;
```

*Figure: A Venn diagram titled "Vivid Venn Diagram of Vexing Iterators". It shows three overlapping circles labeled INPUT, FORWARD, and OUTPUT. The intersection of all three is labeled "Bi-directional".*

---

## Slide 62: Bidirectional Iterator

*Figure: A rectangular code box containing a C++ program example demonstrating the use of a bidirectional iterator with a `std::map`. The code initializes a map of strings to integers, obtains an iterator to the past-the-end position, decrements it to point to the actual last element, and then safely dereferences it.*

```cpp
#include <iostream>
#include <map>

int main() {
    std::map<std::string, int> m = {
        {"apple", 1},
        {"banana", 2},
        {"cherry", 3}
    };

    auto it = m.end();    // end() points ONE PAST the last element
    --it;                 // step back to the actual last element
    auto& elem = *it;     // now dereference safely

    return 0;
}
```

---

## Slide 63: Random Access Iterators
- Allows us to quickly skip forward and backward
- `std::vector`, `std::deque`

```cpp
auto it2 = it + 5; // 5 ahead
auto it3 = it2 - 2; // 2 back

// Get 3rd element
auto& second = *(it + 2);
auto& second = it[2];
```

*Figure: A Venn diagram titled "Vivid Venn Diagram of Vexing Iterators". It contains four overlapping circles: a light blue circle labeled **INPUT**, a gray circle labeled **FORWARD** overlapping with the input circle, a pink circle labeled **OUTPUT** overlapping with the other circles, and a central overlapping region labeled **Random Access**. The diagram visualizes how random access iterators intersect with input, forward, and output iterator categories.*

---

## Slide 64: Be careful not to go out of bounds

```cpp
std::vector<int> v { 1, 2, 3 };
auto it = v.begin();
it += 3;
int& elem = *it; // Undefined behaviour
```

*Figure: A diagram illustrating the iterator's state after incrementing. Three blue boxes representing the vector's elements contain the values 1, 2, and 3, with indices 0, 1, and 2 labeled above them. To the right of the box at index 2 is a fourth dashed, empty square representing the out-of-bounds memory at index 3. A white box labeled "it" is positioned below the vector, with a black arrow originating from it and pointing to the dashed box.*

---

## Slide 65: Why does it matter?

---

## Slide 66: Why does it matter?
As we’ll soon see, some algorithms require a certain iterator type!

*Figure: A boxed area containing C++ code examples. The top section shows a `std::vector` being sorted successfully, marked with a green checkmark emoji and green text "begin/end are random access". The bottom section shows an attempt to sort a `std::unordered_set`, which is marked with a red cross emoji, green text "begin/end are bidirectional", and a yellow highlight over the `std::sort` function call.*

```cpp
std::vector<int> vec{1,5,3,4};
std::sort(vec.begin(), vec.end());
// ✅ begin/end are random access

std::unordered_set<int> set {1,5,3,4};
std::sort(set.begin(), set.end());
// ❌ begin/end are bidirectional
```

---

## Slide 67: Why have multiple iterator types?

*   **Goal:** provide a uniform abstraction over all containers
*   **Caveat:** the way that a container is implemented affects how you iterate through it
    *   Skipping ahead 5 steps (random access) is a lot easier/faster when you have a sequence container (`vector`, `deque`) than associative (`map`, `set`)
    *   C++ generally avoids providing you with slow methods by design, so that's why you can't do random access on a `map::iterator`

---

## Slide 68: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup with his hand resting near his chin, appearing as if he is about to raise it. In the background, posters for "The C++ Programming Language" and "A Tour of C++" are visible.*

bjarne_about_to_raise_hand

---

## Slide 69: Pointers and Memory

---

## Slide 70: Iterator vs. Pointer
An **iterator** points to a **container element**
A **pointer** points to **any object**

---

## Slide 71: Memory Basics

*Figure: A central diagram illustrating the connection between a processor and memory. On the left is an Intel Core i7 processor. In the center is a large, horizontal pink double-headed arrow pointing toward both components. On the right is a stick of computer RAM.*

```text
intel
Core™ i7
```

---

## Slide 72: Memory Basics

*   Every variable lives somewhere in memory
*   All the places something could live form the **address space**

*Figure: A diagram titled "Your Program’s Memory" illustrating the structure of a process's address space as a vertical stack of colored regions. From top to bottom, the regions are: a gray bar labeled "OS Shared"; a light blue bar labeled "Variables (Stack)"; a large white space in the middle containing two dark arrows pointing toward each other—a downward arrow from the Stack region and an upward arrow from the Heap region; a light blue bar labeled "Variables (Heap)"; a pink bar labeled "Global Variables"; and a purple bar at the bottom labeled "Text (Instructions)". The arrows indicate that the stack grows downward and the heap grows upward toward each other.*

---

## Slide 73: Memory Basics
*   Memory is usually byte-addressable, with each byte numbered from 0
*   1 byte = 8 bits

*Figure: A diagram showing the layout of a program's memory as a vertical stack. From top to bottom, the sections are: "OS Shared" (gray box), "Variables (Stack)" (light blue box), an empty gray area with a downward-pointing arrow from the stack, "Variables (Heap)" (light blue box) with an upward-pointing arrow into the gray area, "Global Variables" (red box), and "Text (Instructions)" (light purple box). To the right of the top of the stack, an arrow points to the top section with the label `2^64 – 1` (in red) and `(on a 64-bit system)` (in gray) below it. To the right of the bottom section, an arrow points to the bottom with the label `0x0` (in red).*

---

## Slide 74: Memory Basics

*   The **address** of an object is the location of its lowest byte
*   For example, an integer always uses 32 bits = 4 bytes

```cpp
int x = 106; // 32 bits
```

*Figure: A diagram illustrating how an integer is stored in memory. A box labeled "x's memory" contains four bytes. From left to right, the binary values in the bytes are `00000000`, `00000000`, `00000000`, and `01101010`. Below these bytes are their respective memory addresses: `0x10`, `0x11`, `0x12`, and `0x13`. A separate box to the left contains the text "0x10 is the address of x", with an arrow pointing directly to the address `0x10`.*

*Note: This demonstration uses Big Endian. Little Endian is more common.*

---

## Slide 75: What questions do you have?
What questions do you have?

*Figure: A photo of Bjarne Stroustrup looking thoughtful with his hand to his chin. A poster or book cover with the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP" is visible in the background.*

bjarne_about_to_raise_hand

---

## Slide 76: How do we get the address of a variable in C++?

How do we get the address of a variable in C++?

---

## Slide 77: Pointers! 👉 👉 👉

Pointers! 👉 👉 👉

---

## Slide 78: A pointer is the address of a variable

```cpp
int x = 106;
int* px = &x;

std::cout << x << std::endl;    // 106
std::cout << *px << std::endl;  // 106
std::cout << px << std::endl;   // 0x50527c
```

*Figure: Two annotation boxes are positioned to the right of the first two lines of code. The first box contains the text "int* means px is a pointer to an int" (with "int*" and "int" in red). The second box contains the text "& is the address of operator" (with "&" in red and "address of" underlined).*

---

## Slide 79: Cartoon about pointers

*Figure: A cartoon panel with two stick figures. One stick figure sits at a desk, playing a computer game. The other stick figure stands, wearing a hat. A speech bubble from the standing figure reads: "MAN, I SUCK AT THIS GAME. CAN YOU GIVE ME A FEW POINTERS?"*

```text
MAN, I SUCK AT THIS GAME.
CAN YOU GIVE ME
A FEW POINTERS?
```

---

## Slide 80: A pointer is just a number!

*Figure: A diagram illustrating that a pointer variable stores a memory address. On the left, a box labeled "int* px" (with "int*" in red text) contains the hexadecimal value `0x50527c`. An arrow points from this box to the leftmost byte of a memory layout labeled "int x" (with "int" in red text). The "int x" layout is shown as four contiguous memory cells, each containing an 8-bit binary value. From left to right, the cells contain `00000000`, `00000000`, `00000000`, and `01101010`. Below these cells are their corresponding memory addresses: `0x50527c`, `0x50527d`, `0x50527e`, and `0x50527f`.*

*\*Note: This demonstration uses Big Endian. Little Endian is more common.*

---

## Slide 81: Q&A Prompt

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, creator of C++. He is seated, wearing glasses and a patterned shirt, with his right hand resting on his chin in a thoughtful pose. Behind him are computer monitors and a poster with the text "PROGRAMMING LANGUAGE" and his name "BJARNE STROUSTRUP". Below the photograph is the text label "bjarne_about_to_raise_hand".*

---

## Slide 82: Pointer and Variable Illustration

*Figure: A simple line drawing of a bearded man with a surprised or excited expression, pointing to the left. The text "int x" is positioned to the left of his pointing finger, and the text "int* px" is positioned above his head.*

```cpp
int x
```

```cpp
int* px
```

---

## Slide 83: We can have pointers to all kinds of things!

```cpp
int x = 106;
int* px = &x;
```

```cpp
StanfordID id { "rfern" };
StanfordID* p = &id;
auto name = p->name;
```

```cpp
std::vector<int> v;
std::vector<int>* p = &v;
```

```cpp
std::vector<int> v {
    1, 2, 3, 4, 5
};
int* arr = &v[0];
```

---

## Slide 84: Recall: a vector is a contiguous array

*Figure: A diagram illustrating a vector as a contiguous array. It shows a horizontal row of 10 cells. The first eight cells are blue and contain the numbers 1, 9, 7, 3, 2, 1, 2, and 9. The final two cells are light grey and empty.*

A **vector** is a single chunk of memory

---

## Slide 85: Array pointer

```cpp
std::vector<int> v {1,2,3,4,5};

int* arr = &v[0];              std::cout << *arr << " ";
arr += 1;                      std::cout << *arr << " ";
++arr;                         std::cout << *arr << " ";
arr += 2;                      std::cout << *arr << " ";
if (arr == &v[4])              std::cout << "At last index";
```

*Figure: A diagram of a vector containing five integer elements {1, 2, 3, 4, 5} shown in blue boxes. The indices 0, 1, 2, 3, and 4 are labeled above the boxes. An arrow points from a box labeled 'arr' to the first element at index 0.*

**Output:**
```text
1  2  3  5  At last index
```

---

## Slide 86: Notice anything?

*Figure: A code snippet contained within a bordered box, demonstrating various pointer operations on a C++ vector.*

```cpp
std::vector<int> v {1,2,3,4,5};

int* arr = &v[0];       // Initalization
arr += 1;               // Random access
++arr;                  // Move pointer forward
arr += 2;               // Random access
if (arr == &v[4])       // Pointer comparison
```

---

## Slide 87: We could do the same thing with iterators!

```cpp
auto it = v.begin();
std::cout << *it << " ";
it += 1;
std::cout << *it << " ";
++it;
std::cout << *it << " ";
it += 2;
std::cout << *it << " ";
if (it == --v.end())
std::cout << "At last element";
```

---

## Slide 88: Recall: iterator is a type alias

Recall: **iterator** is a type alias

*Figure: A C++ code snippet inside a bordered box with a drop shadow, illustrating a type alias within a class template.*

```cpp
template <typename T>
class vector {
    using iterator = /* some iterator type */;;

    // Implementation details...
};
```

---

## Slide 89: Iterators and Pointers

Iterators have a similar interface to pointers

*Figure: A presentation slide with a single centered sentence on a white background. The sentence reads, "Iterators have a similar interface to pointers." The words "Iterators" and "pointers" are highlighted in red, while the words in between are black.*

---

## Slide 90: T* is the backing type for vector\<T\>::iterator

*Figure: A black-bordered box with a drop shadow containing a C++ code snippet.*

```cpp
template <typename T>
class vector {
    using iterator = T*;
    // Implementation details...
};
```

In the real STL implementation, the actual type is not T*.
But for all intents and purposes, you can think of it this way.

---

## Slide 91: What questions do you have?
# What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, the creator of C++, wearing glasses and a patterned shirt, resting his chin on his hand. In the background are posters, including one for the book "A Tour of C++" and another titled "PROGRAMMING LANGUAGE" featuring his name.*

bjarne\_about\_to\_raise\_hand

---

## Slide 92: LET’S DO SOME PRACTICE

https://106b.vercel.app/iterators

Links on this slide:
- <https://106b.vercel.app/iterators>

---

## Slide 93: Recap

Recap

---

## Slide 94: What we covered

* **Iterator Basics**
    * An iterator allows us to step forward through a container
* **Iterator Types**
    * Input, Output, Forward, Bidirectional, Random Access
* **Pointers and Memory**
    * A pointer points to an arbitrary C++ object in memory
    * Pointers and iterators have the same interface

---

## Slide 95: So how do we implement other iterators?

```cpp
template <typename K, typename V>
class map {
    using iterator = ???????;

    // Implementation details...
};
```

*Figure: A binary search tree diagram illustrating a map's internal structure. The root node contains the key "CS106L" with the value 42. It has two child nodes: "Chris" (value 31) to the left and "Nick" (value 51) to the right. The "Nick" node further branches to two children: "Keith" (value 14) on the left and "Sean" (value 35) on the right. Black arrows point from parent nodes to their child nodes.*

---

## Slide 96: Classes

**Classes**

**We’ll learn about them next time**
