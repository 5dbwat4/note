# Lecture 14: MoveSemantics (2026Spring)

> PDF title: 2026Spring-14-MoveSemantics.pptx
> Source: `assets/slides/2026Spring-14-MoveSemantics.pdf` · 89 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Welcome back! Link to Attendance Form ↓

*Figure: A QR code centered on the slide, intended for scanning to access an attendance form. A downward-pointing arrow (↓) in the title points towards the QR code.*

---

## Slide 2: Low Battery Alert

*Figure: A close-up, black-and-white photograph of a hand holding a smartphone. A "Low Battery" system alert dialog is overlaid on the phone's screen. The alert contains the text "Low Battery" and "10% battery remaining." Below the text are two buttons: "Low Power Mode" and "Close".*

- **Low Battery**
  10% battery remaining.
- **Low Power Mode**
- **Close**

---

## Slide 3: Things that drain battery life
- **Connecting to WiFi**
  *Figure: Icon of a WiFi transmission tower with a SIM card, representing mobile data/WiFi connection.*
- **Performing computations**
  $$f(x) = a_0 + \sum_{n=1}^{\infty} \left( a_n \cos \frac{n\pi x}{L} + b_n \sin \frac{n\pi x}{L} \right)$$
- **Powering the display**
  *Figure: Illustration of a display brightness toggle, showing the sun/brightness icon on a slider.*
- **Copying data?? 🤔**
  *Figure: Black box displaying three lines of green binary digits.*
  ```
  110101110101011101
  010101010111010101
  010100100010101010
  ```

---

## Slide 4: Copying data is expensive

**Quantifying the Energy Cost of Data Movement for Emerging Smart Phone Workloads on Mobile Platforms**

Dhinakaran Pandiyan and Carole-Jean Wu
*School of Computing, Informatics, and Decision Systems Engineering*
Arizona State University
Tempe, Arizona 85281
Email: {dpandiya,carole-jean.wu}@asu.edu

moving data for a wide range of popular smart phone workloads. We find that a considerable amount of total device energy is spent in data movement (**an average of 35%** of the total device energy). Our results also indicate a relatively high stalled cycle

[source]

Links on this slide:
- <https://ieeexplore.ieee.org/document/6983056>

---

## Slide 5: Copying data is expensive

*Figure: An inset box containing the title, authors, affiliation, email addresses, and a highlighted text excerpt from a research paper.*

### Quantifying the Energy Cost of Data Movement in Scientific Applications

Gokcen Kestor*, Roberto Gioiosa*, Darren J. Kerbyson*, Adolfy Hoisie*
\* Pacific Northwest National Laboratory
{gokcen.kestor, roberto.gioiosa, darren.kerbyson, adolfy.hoisie}@pnnl.gov

exascale systems. Projections show that the cost of moving data from memory is **two orders of magnitudes higher** than the cost of computing a double-precision register-to-register floating point operation. These

[source]

Links on this slide:
- <https://ieeexplore.ieee.org/document/6704670>

---

## Slide 6: Boredom Meme

*Figure: A three-panel meme from the TV show "Parks and Recreation". The top panel shows the character Ron Swanson sitting on a swing with a bored expression. Overlaid text reads, "ME WHEN MY PHONE IS DEAD AND I HAVE NOTHING TO DO". The bottom left panel shows Ron Swanson sitting alone at a table indoors, looking down. The bottom right panel shows him standing alone by an empty swimming pool, hands in his pockets. A small watermark at the bottom left of the meme reads "imgflip.com".*

---

## Slide 7: Why does it matter?
Why does it matter?

---

## Slide 8: Data Center Infrastructure

*Figure: A high-angle photograph of a large-scale data center interior. Multiple rows of black server racks are visible, featuring numerous small blue and green indicator lights. Overhead, a complex network of metal cable trays and structural supports hangs from the ceiling, which is illuminated with blue and purple lighting. The floor consists of light-colored square tiles reflecting the overhead lights.*

---

## Slide 9: How can we avoid needlessly copying data?

---

## Slide 10: Lecture 14: Move Semantics

Lecture 14:
Move Semantics

CS106L, Spring 2026
Rachel Fernandez and Preston Seay

---

## Slide 11: Today’s Agenda

- SMFs Recap
  - What is a special member function?

- The Problem
  - How do our SMFs cause unnecessary copies?

- lvalues and rvalues
  - How does C++ distinguish between persistent and temporary objects?

- Move Semantics
  - How can we avoid making unnecessary copies? And a code demo!

- std::move and SMFs
  - How can we ”opt-in” to move semantics? Which SMFs should I define?

---

## Slide 12: What questions do you have?

What questions do you have?

*Figure: A photograph of a man (Bjarne Stroustrup) sitting in an office chair, wearing glasses and a patterned, long-sleeved shirt. He has his right hand raised to his chin in a thoughtful pose. In the background, there are computer monitors and framed posters on the wall. One prominent poster is titled "PROGRAMMING LANGUAGE" and features the name "BJARNE STROUSTRUP". A smaller caption below the photograph reads: `bjarne_about_to_raise_hand`.*

---

## Slide 13: SMFs Recap

---

## Slide 14: Last Time

*   Special member functions handle the class lifecycle
    *   Copy constructor
```cpp
Type::Type(const Type& other);
Type a = b;
```
    *   Copy assignment operator
```cpp
Type& Type::operator=(const Type& other);
a = b;
```
    *   Destructor
```cpp
Type::~Type();
```
*   Compiler creates these for us

---

## Slide 15: Introducing... the Photo class

*Figure: A code snippet inside a box with a drop shadow, defining a C++ class named `Photo`.*

```cpp
class Photo {
public:
    Photo(int width, int height);
    Photo(const Photo& other);
    Photo& operator=(const Photo& other);
    ~Photo();
private:
    int width;
    int height;
    int* data;
};
```

---

## Slide 16: Photo Constructor

```cpp
Photo::Photo(int width, int height)
: width(width)
, height(height)
, data(new int[width * height])
{}
```

Creates a brand new photo
and allocates memory for its
pixels!
Photo photo(500, 500);

---

## Slide 17: Photo SMF: Copy Constructor

```cpp
Photo::Photo(const Photo& other)
    : width(other.width)
    , height(other.height)
    , data(new int[width * height])
{
    std::copy(other.data, other.data + width * height, data);
}
```

Creates a **new photo from an existing one**, creating a copy of its data!

```cpp
Photo p = photo;
```

---

## Slide 18: Photo SMF: Copy Assignment

```cpp
Photo& Photo::operator=(const Photo& other) {
    // Check for self assignment
    if (this == &other) return *this;

    delete[] data; // Clean up old pixels!

    // Copy over new pixels!
    width = other.width;
    height = other.height;
    data = new int[width * height];

    std::copy(other.data, other.data + width * height, data);
    return *this;
}
```

*Figure: A slide titled "Photo SMF: Copy Assignment" featuring a large box containing C++ code for the copy assignment operator. To the right are two smaller annotation boxes. An arrow points from the top box to the start of the function. The top box contains the text "E.g. if we did" and the code snippet `p = p;`. The lower box on the right contains the text "Replaces a photo’s contents with the contents of another, cleaning up its own data before copying the new one!" followed by the code snippet `p = photo;`.*

---

## Slide 19: Photo SMF: Destructor

*Figure: The slide presents the implementation of the Photo class destructor inside a large rectangular frame, with a smaller text box on the right providing an explanation.*

```cpp
Photo::~Photo()
{
    delete[] data;
}
```

Cleans up this photo’s **data** so we don’t leak memory!

---

## Slide 20: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup wearing glasses and a patterned shirt, resting his chin on his hand. Behind him is a computer monitor and a poster that reads "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". Below the image is a caption in monospaced font.*

`bjarne_about_to_raise_hand`

---

## Slide 21: Your Turn
What special member functions get called at **(A)** and **(B)** below?

```cpp
Photo takePhoto();

int main() {
    Photo selfie = takePhoto();    // (A)
    Photo retake(0, 0);
    retake = takePhoto();          // (B)
}
```

**Copy Destruct**

**Assign Destruct**

*Figure: A code snippet is displayed inside a bordered box. Two lines of code are highlighted: the line defining `selfie` is highlighted with a blue rectangle extending to the comment `// (A)` which is highlighted with a pink rectangle; the line `retake = takePhoto();` is highlighted with a blue rectangle extending to the comment `// (B)` which is highlighted with a pink rectangle. To the right of the code, the words "Copy Destruct" are written, with "Copy" in blue and "Destruct" in red. Below that, the words "Assign Destruct" are written, with "Assign" in blue and "Destruct" in red.*

---

## Slide 22: A Small Aside: Return Value Optimization

*   This line
    ```cpp
    Photo selfie = takePhoto();
    ```
    might not actually call copy-constructor + destructor
*   This is due to a compiler optimization called [return-value optimization (RVO)](https://)
*   For the purposes of this lecture, we will pretend that it does!

Links on this slide:
- <https://en.wikipedia.org/wiki/Copy_elision#Return_value_optimization>

---

## Slide 23: Key Idea

Key Idea: The return value of a function is temporary (it’s destroyed before the next line)

*Figure: A code statement is shown inside a black-bordered box. A callout box to the right, with an arrow pointing to the code statement, contains the text: "The compiler is going to clean this object up before moving onto the next line!". In the code statement, the function call `takePhoto()` is highlighted in yellow.*

```cpp
Photo selfie = takePhoto();
```

---

## Slide 24: Questions?

What questions do you have?

*Figure: A photo of Bjarne Stroustrup with his hand on his chin, appearing to be about to raise his hand. Below the photo is the text `bjarne_about_to_raise_hand`.*

---

## Slide 25: The Problem

---

## Slide 26: The Problem

takePhoto()

```cpp
Photo selfie = takePhoto();
```

---

## Slide 27: The Problem

takePhoto()

*Figure: A diagram illustrating a `Photo` object. A curved arrow points from the text "takePhoto()" to a box labeled "Photo". The box contains three attributes: `width = 3840`, `height = 2160`, and `data = 0x1024c3bd`. A squiggly arrow points from the box to a photograph of a woman holding a small green bird.*

Photo
* width = 3840
* height = 2160
* data = 0x1024c3bd

```cpp
Photo selfie = takePhoto();
```

---

## Slide 28: The Problem

takePhoto()

*Figure: Two side-by-side diagrams illustrating object creation. On the left, a box labeled "Photo" contains a bulleted list of attributes. A curved arrow originates from the text "takePhoto()" and points to this box. A wavy arrow points from the "data" attribute in the box down to a photograph of a woman holding a small green bird. On the right, an identical box labeled "Photo (selfie)" contains a similar bulleted list with a different memory address for "data". A wavy arrow points from its "data" attribute down to an identical photograph.*

**Photo**
- width = 3840
- height = 2160
- data = 0x1024c3bd

**Photo (selfie)**
- width = 3840
- height = 2160
- data = 0x133210f1

```cpp
Photo selfie = takePhoto(); // Copy constructor
```

---

## Slide 29: The Problem

*Figure: A diagram illustrating the "move" problem in C++. On the left, a label "takePhoto()" has an arrow pointing toward a faded image of a person holding a bird. Above this image is a box labeled with a skull icon and the word "Photo", containing properties: width = 3840, height = 2160, and data = 0x1024c3bd. A wavy arrow points from this box down to the faded image. On the right, there is a clear version of the same image. Above the clear image is a box labeled "Photo (selfie)" in colored text (Photo in red, selfie in blue), with properties: width = 3840, height = 2160, and data = 0x133210f1. A wavy arrow points from this box down to the clear image. At the bottom of the slide is a line of code:*

```cpp
Photo selfie = takePhoto(); // Destructor
```

*In the code, "Photo" is purple, "selfie" is black, the equals sign is blue, "takePhoto()" is highlighted in yellow, and the comment "Destructor" is in red.*

---

## Slide 30: The Problem

*Figure: A photo of Bjarne Stroustrup, creator of C++, looking thoughtful with his hand on his chin. He is in front of a bookshelf. The C++ logo is partially visible behind his right shoulder. Below the image, the text 'concerned_bjarne' appears as a caption.*

concerned_bjarne

---

## Slide 31: What if we could reuse the memory instead?

What if we could reuse the memory instead?

---

## Slide 32: The Solution: Move Semantics

```cpp
takePhoto()
```

**Photo**
*   width = 3840
*   height = 2160
*   data = 0x1024c3bd

*Figure: A conceptual diagram illustrating move semantics. A curved arrow points from the text "takePhoto()" on the left to a "Photo" data structure box on the right. The box contains metadata for an image: width, height, and a memory address (data). Below the box is a photograph of a woman holding a small green parrot, representing the actual image data being referenced.*

```cpp
Photo selfie = takePhoto();
```

---

## Slide 33: The Problem

*Figure: A conceptual diagram illustrating the difference between copying and moving a large data object. On the left, a `takePhoto()` function call points to a box labeled `Photo` containing metadata: width, height, and a memory address for the data. In the center is a photograph of a person holding a small green bird. To the right, another box labeled `Photo (selfie)` contains identical metadata, with the data address `0x1024c3bd` highlighted in yellow. A squiggly arrow points from this second box back toward the photograph. A text box below states "Instead of **copying data**, let’s **steal it**!", with "copying data" in blue and "steal it" in green.*

**Photo**
*   width = 3840
*   height = 2160
*   data = 0x1024c3bd

**Photo (selfie)**
*   width = 3840
*   height = 2160
*   data = 0x1024c3bd

### takePhoto()

Instead of **copying data**, let’s **steal it**!

```cpp
Photo selfie = takePhoto(); // Copy Move constructor
```

---

## Slide 34: The Problem

takePhoto()

*Figure: A diagram illustrating a potential resource ownership problem. A photo of a person holding a small bird is shown. A curved arrow points from the text `takePhoto()` to the photo. Two wavy lines connect the photo to two separate boxes. The left box is labeled "Photo" in red and contains bullet points: `width = 3840`, `height = 2160`, `data = 0x1024c3bd`. The right box is labeled "Photo (selfie)" with "(selfie)" in blue and contains identical bullet points: `width = 3840`, `height = 2160`, `data = 0x1024c3bd`. This illustrates that both the return value of `takePhoto()` and the object `selfie` point to the same underlying image data.*

```cpp
Photo selfie = takePhoto(); // Destructor
```
(The function call `takePhoto()` within the line is highlighted in yellow.)

---

## Slide 35: The Problem

*Figure: A diagram illustrating a memory management problem. On the left, the label "takePhoto()" has a curved arrow pointing to a box titled "☠ Photo" containing the following list: width = 3840, height = 2160, data = 0x1024c3bd. To the right of this box is another titled "Photo (selfie)" with the identical list items. Below these boxes is a photograph of a person holding a parrot, with squiggly lines connecting the photo to both data boxes. To the right of the photograph is a text box containing the text: "Oh no… the destructor of takePhoto() deletes our stolen data". At the bottom of the slide is a line of code:*

```cpp
Photo selfie = takePhoto(); // Destructor
```

---

## Slide 36: The Problem

*Figure: A diagram illustrating a "Move" operation for a `Photo` object. On the left, a `Photo` object is shown with its `data` pointer set to `0x0` (highlighted in yellow) and a label `nullptr` pointing to it. An arrow labeled `takePhoto()` points toward this object. To its right is a `Photo (selfie)` object with a `data` pointer value of `0x1024c3bd`. A photograph of a person holding a small green bird is shown below the boxes, with a wavy arrow pointing from the photo to the `data` field of the `selfie` object.*

### Photo
*   width = 3840
*   height = 2160
*   data = **0x0**

### Photo (selfie)
*   width = 3840
*   height = 2160
*   data = 0x1024c3bd

takePhoto()

```cpp
Photo selfie = takePhoto(); // Copy Move constructor
```

*Note: In the code line, "Copy" is struck through and "Move" is highlighted in green.*

---

## Slide 37: The Problem

- `takePhoto()`

*Figure: A diagram illustrating the problem with copying a Photo object. A call to `takePhoto()` is shown with a curved arrow pointing to the left. To the right are two boxes representing Photo objects:*

*Left box (marked with a skull icon ☠️ and labeled "Photo"):*
- width = 3840
- height = 2160
- data = 0x0

*Right box (labeled "Photo (selfie)" with "selfie" in blue):*
- width = 3840
- height = 2160
- data = 0x1024c3bd

*A jagged arrow points from the "Photo (selfie)" box down toward a label reading "nullptr". From "nullptr", another jagged arrow points to a box containing explanatory text. A photograph of a person holding a small parrot is shown between the two Photo boxes, representing the actual image data stored at the memory address.*

*Explanatory box (with "Photo" in purple and "delete" and "nullptr" in red):*
**Photo** destructor calls **delete** on **nullptr**, which does nothing!

```cpp
Photo selfie = takePhoto(); // Destructor
```

*At the bottom of the slide, the code statement `Photo selfie = takePhoto();` is shown with "takePhoto()" highlighted in yellow, and a comment "// Destructor" in red.*

---

## Slide 38: The Problem

takePhoto()

*Figure: A diagram illustrating two states of a Photo object. On the left, a box with a skull-and-crossbones icon and the title "Photo" contains a list of its properties. Its "data" field (0x0) points via a wavy line to a box labeled "nullptr". On the right, a box titled "Photo (selfie)" (with "selfie" in blue parentheses) contains a similar list. Its "data" field (0x1024c3bd) points via a wavy line to an image of a woman taking a selfie while holding a small green bird. A large curved arrow points from the right side of the diagram toward the left box.*

- 💀 Photo
  - width = 3840
  - height = 2160
  - data = 0x0

- Photo (selfie)
  - width = 3840
  - height = 2160
  - data = 0x1024c3bd

```cpp
Photo selfie = takePhoto(); // Destructor
```

---

## Slide 39: We created a new Photo without any copying!
We created a new Photo without any copying! 💪

---

## Slide 40: But... is it always safe to do this?

But... is it always safe to do this?

---

## Slide 41: Move vs. Copy Semantics

takePhoto() is temporary, so we can steal its resources!

*Figure: A code snippet in a bordered box with a drop shadow, illustrating move semantics by assigning a temporary object to a new variable.*

```cpp
Photo takePhoto();

int main() {
    Photo selfie = takePhoto();      // Move takePhoto()
    // since it’s temporary!
}
```

---

## Slide 42: Move vs. Copy Semantics

Is it always safe to move objects? Assume get_pixel accesses data

```cpp
Photo takePhoto();

void foo(Photo whoAmI) {
    Photo selfie = whoAmI;        // What if we move here?
    whoAmI.get_pixel(21, 24);    // ???
}
```

What will happen if we try to run this code?

*Figure: A callout box or speech bubble containing the text "What will happen if we try to run this code?", positioned to the right of the code block, with a drop shadow indicating it is an annotation.*

---

## Slide 43: Move vs. Copy Semantics
❌ Since **selfie** stole **whoAmI**’s data, we end up dereferencing **nullptr**

```cpp
Photo takePhoto();

void foo(Photo whoAmI) {
    Photo selfie = whoAmI;            // What if we move here?
    whoAmI.get_pixel(21, 24);     // ❌ use-after-move
}
```

*Figure: A slide displaying a code example inside a white box with a drop shadow. A red cross icon precedes the explanatory text at the top. In the code, specific identifiers are highlighted in different colors: "Photo", "takePhoto", and "foo" are in purple; "whoAmI" and "selfie" are in orange/red; "move" and "use-after-move" are in green; and "nullptr" is in red.*

---

## Slide 44: Building a new computer

### Copy semantics
"I still want to use my old computer"

*Figure: An illustration showing two identical computer towers side by side, representing copying the original object while the original remains.*

### Move semantics
"I don’t need my old computer"

*Figure: An image with a colorful banner that says "PC TEARDOWN AND CLEANUP". Below the banner, a photo shows the inside of an open computer case on the left and a mostly empty computer chassis on the right, with a yellow arrow pointing from the full case to the empty chassis, illustrating moving resources from one to the other.*

---

## Slide 45: Move vs. Copy Semantics

*Figure: A large rectangular box containing two code snippets. The first snippet shows an assignment from a persistent variable, and the second shows an assignment from a temporary function return value. Between the assignment targets and sources in both lines, there is a small icon consisting of a yellow square and a blue square. The word "copies" in the first comment is bolded and colored blue, while the word "move" in the second comment is bolded and colored green.*

```cpp
Photo selfie = pic;
// make copies of persistent objects (e.g. variables)
// that might get used in the future

Photo selfie = takePhoto();
// move temporary objects (e.g return values)
// since we no longer need to use them
```

---

## Slide 46: What questions do you have?

*Figure: A portrait of Bjarne Stroustrup, creator of C++, wearing glasses and a patterned sweater, with his hand resting on his chin. In the background, posters are visible, including one titled "A Tour of C++" and another for "Programming Language Bjarne Stroustrup". Large text is overlaid across the middle of the image.*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 47: Move vs. Copy Semantics

```cpp
Photo selfie = pic;
// make copies of persistent objects (e.g. variables)
// that might get used in the future
```

```cpp
Photo selfie = takePhoto();
// move temporary objects (e.g return values)
// since we no longer need to use them
```

**How does the compiler know whether to move or copy?**

---

## Slide 48: lvalues & rvalues

lvalues & rvalues

---

## Slide 49: lvalues & rvalues

lvalues and rvalues generalize the idea of “temporariness” in C++

```cpp
void foo(Photo pic) {
    Photo beReal = pic;
    Photo insta = takePhoto();
}
```

*Figure: Diagram showing a C++ code snippet inside a rectangle. A callout box with the text "**pic** is an lvalue!" points an arrow to the `pic` parameter in the function signature. Another callout box with the text "**takePhoto()** is an rvalue!" points an arrow to the `takePhoto()` function call inside the function body.*

---

## Slide 50: lvalues & rvalues

Generally speaking, **lvalues** have a definite address, **rvalues** do not!

*Figure: A code snippet illustrating the difference between lvalues and rvalues. The code is inside a black-bordered box. Two callout boxes with arrows point to specific parts of the code.*

```cpp
void foo(Photo pic) {
    Photo* p1 = &pic;
    Photo* p2 = &takePhoto(); // ❌ Doesn't work!
}
```

*   An arrow from an upper-right callout box points to the `&pic` expression in the code. The callout text reads:
    *pic is an lvalue!*
    *We can take its address!*

*   An arrow from a lower-right callout box points to the `&takePhoto()` expression in the code. The callout text reads:
    *takePhoto() is an rvalue!*
    *We **cannot** take its address!*

---

## Slide 51: lvalue and rvalue placement

An **lvalue** can appear on either side of an **=**
```cpp
x = y;
y = 5;
```

An **rvalue** can appear only right of an **=**
```cpp
x = 5;
5 = y;
```

*Figure: The slide explains the difference between lvalues and rvalues in the context of the assignment operator. The top heading, "An **lvalue** can appear on either side of an **=**," uses blue for the word "lvalue" and red for the "=" symbol. Below this is a code box containing the lines `x = y;` and `y = 5;`, where the variable `y` is highlighted in blue. The bottom heading, "An **rvalue** can appear only right of an **=**," uses green for the word "rvalue" and red for the "=" symbol. Below this is a code box containing `x = 5;` and `5 = y;`, where the number `5` is highlighted in green. The second line in this bottom box, `5 = y;`, is crossed out with a red strike-through line to indicate that assigning an rvalue to the left side of an operator is invalid.*

---

## Slide 52: Your Turn

Which of the following <u>right-hand assignments</u> are rvalues?
• Hint: which ones have a definite address?

*Figure: A rectangular box containing six lines of C++ code. Each line displays a variable declaration and assignment, followed by its classification as either an rvalue or an lvalue.*

```cpp
int         a = 4;              rvalue
int&        b = a;              lvalue
vector<int> c = {1, 2, 3};     rvalue
int         d = c[1];           lvalue
int*        e = &c[2];          rvalue
size_t      f = c.size();       rvalue
```

---

## Slide 53: Lvalue and Rvalue Lifetimes

An lvalue’s lifetime is until the end of scope

An rvalue’s lifetime is until the end of line

---

## Slide 54: Value Categories

An **lvalue** is persistent
An **rvalue** is temporary

---

## Slide 55: Quick Note: It’s more complicated than this!

*Figure: A hierarchical diagram showing the classification of C++ expressions. At the top is a box labeled "expression", which branches down to boxes labeled "glvalue" and "rvalue". "glvalue" branches further down to "lvalue" and "xvalue", while "rvalue" branches to "xvalue" and "prvalue". Overlaid across the middle of the diagram is a large red "X" symbol and the text "Don't Worry About This" in large white font.*

*   expression
    *   glvalue
        *   lvalue
        *   xvalue
    *   rvalue
        *   xvalue
        *   prvalue

❌ **Don’t Worry About This**

---

## Slide 56: Working towards move semantics

If we have an **lvalue**, how can we avoid copying its memory?

```cpp
void uploadToInsta(Photo pic);

int main() {
    Photo selfie = takePhoto(); // selfie is lvalue
    uploadToInsta(selfie); // 🤦 Unnecessary copy is made here
}
```

---

## Slide 57: Working towards move semantics

We can pass by reference! 🥳

```cpp
void uploadToInsta(Photo& pic);

int main() {
    Photo selfie = takePhoto(); // selfie is lvalue
    uploadToInsta(selfie); // ✅ No copy is made here
}
```

*Figure: A code snippet inside a white box with a drop shadow, showing a function declaration that takes a `Photo&` reference parameter and a `main` function demonstrating its usage. The parameter type `Photo&` is highlighted in yellow.*

---

## Slide 58: Working towards move semantics

- Now it breaks with **rvalues**?
- What happens if we try to pass by reference?

```cpp
void uploadToInsta(Photo& pic);

int main() {
    uploadToInsta(takePhoto()); // Does this work?
}
```

❌ candidate function not viable: expects lvalue as 1st argument

---

## Slide 59: Bjarne Stroustrup Thinking

*Figure: A photograph of Bjarne Stroustrup looking pensive, resting his chin on his hand. A large blue thought bubble is superimposed next to him containing the text "How do we fix this?"*

How do we fix this?

thinking\_bjarne

---

## Slide 60: lvalue reference vs rvalue reference

### lvalue reference
*Figure: A white rectangular box with a drop shadow containing C++ code for an lvalue reference example. The parameter `Photo& pic` is highlighted with a yellow background.*

```cpp
void upload(Photo& pic);

int main() {
    Photo selfie = takePhoto();
    upload(selfie);
}
```

### rvalue reference
*Figure: A white rectangular box with a drop shadow containing C++ code for an rvalue reference example. The parameter `Photo&& pic` is highlighted with a yellow background.*

```cpp
void upload(Photo&& pic);

int main() {
    upload(takePhoto());
}
```

We can do whatever we want with `Photo&&` pic, it's temporary!

---

## Slide 61: A few important points

* **lvalue** references
  * Syntax: `Type&`
  * Persistent, must keep object in valid state after function terminates
* **rvalue** references
  * Syntax: `Type&&`
  * Temporary, we can steal (move) its resources
  * Object might end up in an invalid state, but that’s okay! It’s temporary!

---

## Slide 62: Lvalue and Rvalue Reference Code Snippets

```cpp
//Hello. I want to take your Widget and play with it. It may be in a
//different state than when you gave it to me, but it'll still be yours
//when I'm finished. Trust me!
void foo(Widget& w);
```

```cpp
//Hello. Ooh, I like that Widget you have. You're not going to use it
//anymore, are you? Please just give it to me. Thank you! It's my
//responsibility now, so don't worry about it anymore, m'kay?
void foo(Widget&& w);
```

[source]

Links on this slide:
- <https://stackoverflow.com/questions/37935393/pass-by-value-vs-pass-by-rvalue-reference?newreg=1d0f3d3ee1ff4bada868d6bc75be5dc6>

---

## Slide 63: Key Idea

**Key Idea:** Overloading **&** and **&&** parameters distinguish **lvalue** and **rvalue** references.

---

## Slide 64: lvalue/rvalue overloading

*Figure: A callout box at the top right containing the text "We define both!".*

```cpp
void upload(Photo& pic);

int main() {
    Photo selfie = takePhoto();
    upload(selfie);
}
```

```cpp
void upload(Photo&& pic);

int main() {
    upload(takePhoto());
}
```

Compiler decides which version of **upload** to call depending on whether argument is lvalue or rvalue!

---

## Slide 65: What questions do you have?

What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, the creator of C++, sitting in front of computer monitors. He is wearing glasses and a patterned shirt, with his hand resting on his chin. In the background, posters are visible, one of which says "PROGRAMMING LANGUAGE BJARNE STROUSTRUP". Below the image is a caption.*
`bjarne_about_to_raise_hand`

---

## Slide 66: Move Semantics

---

## Slide 67: What we want!

```cpp
Photo selfie = pic;
// copy persistent objects (e.g. variables)

Photo selfie = takePhoto();
// move temporary objects (e.g return values)
```

*Figure: A diagram illustrating copy and move semantics. It contains two code snippets with annotations. For the first snippet, `Photo selfie = pic;`, a black arrow points from a white box labeled "Photo&" (in blue) to the yellow-highlighted `=` operator. In the comment below, the word "copy" is blue. For the second snippet, `Photo selfie = takePhoto();`, a black arrow points from a white box labeled "Photo&&" (in green) to the yellow-highlighted `=` operator. In the comment below, the word "move" is green.*

---

## Slide 68: Let’s overload the special member functions!

### Copy constructor

```cpp
Photo::Photo(const Photo& other)
    : width(other.width)
    , height(other.height)
    , data(new int[width * height])
{
    std::copy(
        other.data,
        other.data + width * height,
        data
    );
}
```

### Move constructor

```cpp
Photo::Photo(Photo&& other)
    : width(other.width)
    , height(other.height)
{
    // other is temporary
    // Let’s steal its
    // resources since we know
    // it’s about to be gone!
}
```

---

## Slide 69: Let’s overload the special member functions!

### Copy assignment operator

*Figure: A white box with a drop shadow containing a code snippet for the implementation of the copy assignment operator for a `Photo` class.*

```cpp
Photo& Photo::operator=(const Photo& other) {
    if (this == &other) return *this;
    delete[] data;
    width = other.width;
    height = other.height;
    data = new int[width * height];
    std::copy(other.data, other.data + width *
              height, data);
    return *this;
}
```

### Move assignment operator

*Figure: A white box with a drop shadow containing the signature and placeholder comments for the move assignment operator for a `Photo` class.*

```cpp
Photo&
Photo::operator=(Photo&& other)
{
    // other is temporary
    // Let’s steal its
    // resources since we know
    // it’s about to be gone!
}
```

---

## Slide 70: Let’s code this up!

Let’s code this up!

---

## Slide 71: Coding Session Introduction

### Let’s code this together 👫

*Figure: A pair emoji (👫) of two people, one in a purple shirt and one in a teal shirt, standing together.*

106l.vercel.app/pirate-smfs-part-2

---

## Slide 72: Two new special member functions!
- Move constructor
  - Type::(Type&& other)
- Move assignment operator
  - Type& Type::operator=(Type&& other)

---

## Slide 73: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, a man with glasses and grey hair, wearing a patterned shirt. He is sitting in front of computer monitors and a poster that reads "PROGRAMMING LANGUAGE BJARNE STROUSTRUP". The main text of the slide is superimposed over the photograph.*

bjarne_about_to_raise_hand

---

## Slide 74: std::move and SMFs

std::move and SMFs

---

## Slide 75: Forcing Move Semantics
*   Usually, we let the compiler decide between `&` and `&&`
*   Is that always the most efficient choice?
    *   E.g. what if we know that an lvalue will never be used again?

---

## Slide 76: Forcing Move Semantics

Line 3 *copies* each element into its new spot, even though the original value is never used again

*Figure: A C++ code snippet inside a rectangular border.*

```cpp
void PhotoCollection::insert(const Photo& pic, int pos) {
    for (int i = size(); i > pos; i--)
        elems[i] = elems[i - 1]; // Shuffle elements down
    elems[i] = pic;
}
```

---

## Slide 77: Forcing Move Semantics

**Solution:** use move semantics

*Figure: A code snippet enclosed in a bordered box with a drop shadow. The code is a C++ member function `PhotoCollection::insert`. In the third line of the code, the term `std::move` is highlighted with a yellow background.*

```cpp
void PhotoCollection::insert(const Photo& pic, int pos) {
    for (int i = size(); i > pos; i--)
        elems[i] = std::move(elems[i – 1]);
    elems[i] = pic;
}
```

---

## Slide 78: Be wary of std::move

If we move an lvalue, what happens to it afterwards?

*Figure: A snippet of C++ code enclosed within a shadowed rectangular box.*

```cpp
Photo takePhoto();

void foo(Photo whoAmI)
    Photo selfie = std::move(whoAmI);
    whoAmI.get_pixel(21, 24); // ???
}
```

❌ If we move, whoAmI ends up in an unknown state!

---

## Slide 79: Use std::move to implement move operations!

```cpp
class Photo {
public:
    Photo::Photo(Photo&& other) {
        keywords = other.keywords;
    }
private:
    std::vector<string> keywords;
};
```

*Figure: A text box with a drop shadow is located to the right of the code. A black arrow points from this box to the line `keywords = other.keywords;` within the move constructor.*

> We know that **other** is temporary! So do we *really* need to make a copy of **other.keywords**?

---

## Slide 80: Use std::move to implement move operations!

```cpp
class Photo {
public:
    Photo::Photo(Photo&& other) {
        keywords = std::move(other.keywords);
    }
private:
    std::vector<string> keywords;
};
```

*Figure: A code snippet within a bordered box shows the implementation of a move constructor for a `Photo` class. A thick black arrow points from a text box on the right back to the line of code `keywords = std::move(other.keywords);`.*

**Solution:** force move semantics by using `std::move`

---

## Slide 81: std::move doesn’t do anything special!

- std::move just type casts an lvalue to an rvalue

  *Figure: A code box with the title "Return value" containing the C++ expression for the return value of std::move.*

  ```cpp
  static_cast<typename std::remove_reference<T>::type&&>(t)
  ```

- Like const_cast, we ”opt in” to potentially error-prone behaviour

  - What if we try to use an object after it’s been moved! 🚨🆘🚨

- Try to avoid explicitly using std::move unless you have good reason!

  - E.g. performance really matters, you know for sure the object won’t be used!

---

## Slide 82: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup with his hand resting on his chin, appearing to be about to raise his hand. In the background, there are posters or books related to programming languages. Below the image is the caption "bjarne_about_to_raise_hand".*

bjarne_about_to_raise_hand

What questions do you have?

---

## Slide 83: We have two new SMFs!
* `Type::Type(const Type& other);`
* `Type& Type::operator=(const Type& other);`
* `Type::Type(Type&& other);`
* `Type& Type::operator=(Type&& other);`
* `~Type::Type();`

---

## Slide 84: SMFs Question

So many SMFs... 😩
Do I need to define them all!?

---

## Slide 85: Rule of Zero, Three, and Five

*Figure: A photograph of a man sitting at a desk in an office, with multiple computer monitors and bookshelves in the background. A large, blue thought bubble is positioned over the top left of the man, containing text.*

No! Rule of zero, three, and five!

---

## Slide 86: Rule of Zero

*   If a class doesn’t manage memory (or another external resource), the compiler generated versions of the SMFs are sufficient!
*   **Example:** Compiler generated SMFs of `Post` will call SMFs of `Photo` and `std::string`

*Figure: A boxed code snippet illustrating the Rule of Zero with a C++ struct definition.*
```cpp
struct Post {
    Photo photo;
    std::string caption;
};
```

---

## Slide 87: Rule of Three

*   If a class manages external resources, we must define **copy assignment/constructor**
*   If we don't, compiler-generated SMF won't copy underlying resource
*   This will lead to bugs, e.g. two Photo’s referring to the same underlying data

*Figure: A rectangular box with a black border containing the definition of the Rule of Three.*

**Rule of Three:** If you need any one of these, you need them all:
*   Destructor
*   Copy Assignment
*   Copy Constructor

---

## Slide 88: Rule of Five

*   If we defined **copy constructor/assignment** and **destructor**, we should also define **move constructor/assignment**
*   This is not required, but our code will be slower as it involves unnecessary copying

*Figure: An inset box containing the formal definition of the Rule of Five.*
> **Rule of Five:** If you need any of these, you probably want them all:
> *   Destructor
> *   Copy Assignment
> *   Copy Constructor
> *   Move Assignment (Optional)
> *   Move Constructor (Optional)

---

## Slide 89: What questions do you have?

*Figure: A portrait photo of Bjarne Stroustrup, a man with glasses and a patterned shirt, resting his chin on his hand. In the background, a poster with his name "BJARNE STROUSTRUP" is visible.*

What questions do you have?

bjarne_about_to_raise_hand
