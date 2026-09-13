# Lecture 16: RAII-SmartPointers (2026Spring)

> PDF title: 2026Spring-16-RAII-SmartPointers.pptx
> Source: `assets/slides/2026Spring-16-RAII-SmartPointers.pdf` · 102 pages · transcribed with `mimo-v2.5` · 2026-09-08

---

## Slide 1: CS106L Lecture 16: RAII, Smart Pointers, Building Projects

CS106L Lecture 16:
RAII, Smart Pointers,
Building Projects🔗

Rachel Fernandez && Preston Seay

*Figure: A title slide with a yellow-to-white gradient background. The main text is centered and reads "CS106L Lecture 16: RAII, Smart Pointers, Building Projects" followed by a blue link emoji. Below that, the names "Rachel Fernandez && Preston Seay" are displayed.*

---

## Slide 2: So, on a 1 to 9 on rubberduck scale, how are things today?

*Figure: A meme slide with a pale yellow background containing three images.*

So, on a 1 to 9 on rubberduck scale, how are things today?

*Text watermark: @bestjokesvids*

*The central meme is a 3×3 grid of photographs of a giant yellow rubber duck at various angles and distances, numbered 1 through 9:*

| | | |
|---|---|---|
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |

*Figure (left): A tilted image of Kermit the Frog with a contemplative expression, hand on chin. Text on the image reads:*

How are you
doing today?

*Text watermark (bottom of left image): meme-center.com*

*Figure (bottom right): A tilted image of a polar bear facing forward. Text on the image reads:*

HELLO

HOW ARE YOU DOING TODAY

*Text watermark (bottom right of polar bear image): middleeasteye*

---

## Slide 3: Attendance

*Figure: Two QR codes displayed side by side. The left QR code is a standard black and white square pattern. The right QR code is composed of small dots arranged in a similar pattern.*

https://forms.gle/bBVRcQGVoaTc1ciL7

Links on this slide:
- <https://forms.gle/bBVRcQGVoaTc1ciL7>

---

## Slide 4: Plan
1. RAII (Resource Acquisition Is Initialization)
2. Smart Pointers
3. Building C++ projects

---

## Slide 5: Plan

1. RAII (Resource Acquisition Is Initialization)
2. Smart Pointers
3. Building C++ projects

---

## Slide 6: How many code paths?

*Figure: A dark code editor window with three colored control buttons (red, yellow, green) in the top-left corner, containing a C++ function definition.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 7: How many code paths?

*Figure: A dark-themed code editor window with three colored dots (red, yellow, green) in the top-left corner. An orange arrow annotation points from the left towards the `if` statement in the code.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 8: How many code paths?

*Figure: Screenshot of a code editor window (with red, yellow, green control circles at the top left) displaying C++ code.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 9: How many code paths?

*Figure: A code snippet displayed in a dark-themed code editor window with macOS-style control buttons (red, yellow, and green) in the top-left corner. An orange arrow on the left side points directly at the `return` statement.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 10: How many code paths?

*Figure: A code editor window with a dark theme. At the top left of the window are three circular traffic-light buttons (red, yellow, green).*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
        p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

3?

---

## Slide 11: Exceptions

*   Exceptions are a way of handling errors when they arise in code

---

## Slide 12: Exceptions
*   Exceptions are a way of handling errors when they arise in code
*   Exceptions are “thrown”

---

## Slide 13: Exceptions

*Figure: A horizontal yellow banner at the top of the slide containing the title "Exceptions" in a large, bold, black serif font. The rest of the slide body is plain white.*

* Exceptions are a way of handling errors when they arise in code
* Exceptions are “thrown”
* However, we can write code that lets us handle exceptions so that we can continue in our code without necessarily erroring.

---

## Slide 14: Exceptions

- Exceptions are a way of handling errors when they arise in code
- Exceptions are “thrown”
- However, we can write code that lets us handle exceptions so that we can continue in our code without necessarily erroring.
- We call this **“catching”** an exception.

---

## Slide 15: Exceptions

We can write code that lets us handle exceptions so that we can continue in our code without necessarily erroring.

```cpp
try {
    // code that we check for exceptions
}
catch([exception type] e1) { // "if"
    // behavior when we encounter an error
}
catch([other exception type] e2) { // "else
if"
    // ...
}
catch { // the "else" statement
    // catch-all (haha)
}
```

*Figure: A code block contained within a black-bordered rectangle. The keywords 'try' and 'catch' are highlighted in blue, while the comments are in green. The snippet demonstrates the basic structure of exception handling blocks.*

---

## Slide 16: Exceptions

```cpp
try {
    int age = 15;
    if (age >= 18) {
        cout << "Access granted - you are old enough.";
    } else {
        throw (age);
    }
}
catch (int myNum) {
    cout << "Access denied - You must be at least 18 years old.\n";
    cout << "Age is: " << myNum;
}
```

---

## Slide 17: What questions do we have?

*Figure: A small green and grey parrot is being held in someone's hand. Three red question mark emojis are positioned near the bird's head.*

---

## Slide 18: How many code paths?

*Figure: A screenshot of a code editor window with three colored dots (red, yellow, green) in the top left corner. The window displays a C++ function named `returnNameCheckPawsome`.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 19: At least 23 code paths!

- ● (1): Copy constructor of Pet may throw

*Figure: A dark-themed code editor window showing a C++ function. A red arrow points from the bullet point text on the left to the function signature `std::string returnNameCheckPawsome(Pet p)` inside the editor window.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 20: At least 23 code paths!

*   (1): Copy constructor of Pet may throw
*   (5): Constructor of temp strings may throw

*Figure: A screenshot of a dark-themed code editor window. The window displays a C++ function `returnNameCheckPawsome` that takes a `Pet` object, checks a condition, and returns a `std::string`.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 21: At least 23 code paths!

*   (1): Copy constructor of Pet may throw
*   (5): Constructor of temp strings may throw
*   (6): Call to type, firstName (3), lastName (2) may throw

*Figure: A screenshot of a code editor window showing a C++ function. A red arrow points from the third bullet point on the slide to the lines within the code where the `type`, `firstName`, and `lastName` methods are called.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
        p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 22: At least 23 code paths!

*   (1): Copy constructor of Pet may throw
*   (5): Constructor of temp strings may throw
*   (6): Call to type, firstName (3), lastName (2) may throw
*   (10): User overloaded operators may throw

*Figure: A code snippet displayed in a dark-themed code editor window with a red, yellow, and green circular control dot pattern in the top-left corner. A red arrow originates from the "User overloaded operators may throw" bullet point and points directly to the `p.lastName()` call within the `return` statement inside the code. A second red arrow originates from within the code itself and points to the same `p.lastName()` call in the `return` statement, visually linking the code location to the potential throw sources listed in the bullet points.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
        p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 23: At least 23 code paths!

*   (1): Copy constructor of Pet may throw
*   (5): Constructor of temp strings may throw
*   (6): Call to type, firstName (3), lastName (2) may throw
*   (10): User overloaded operators may throw
*   (1): Copy constructor of returned string may throw

*Figure: A code editor window with red, orange, and green circular buttons in the top-left corner, displaying C++ code. A red arrow points from the final bullet point on the left to the `return` statement in the code.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
             p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

---

## Slide 24: How many code paths?

*Figure: A slide featuring a large, bold title on a yellow gradient background. Below the title is a code editor window with a dark theme, featuring three circular window controls (red, orange, and green) in the top-left corner.*

```cpp
std::string returnNameCheckPawsome(Pet p) {
    /// NOTE: dogs > cats
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    return p.firstName() + " " + p.lastName();
}
```

23

---

## Slide 25: What could go wrong?

*Figure: A code snippet in a dark-themed editor window with red, yellow, and green window control dots in the top-left corner. An orange arrow points from a yellow callout box to the line `if (p.type() == "Dog"` in the code. The callout box contains the text: "What if this function threw an exception here?"*

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
        p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

---

## Slide 26: What could go wrong?

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " << 
                  p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    urn returnStr;
}
```

*Figure: A code editor window with a dark background showing a C++ function. Two yellow annotation boxes with orange arrows are present:*
* *The box on the left contains the text "What if this function threw an exception here?" and its arrow points to the line `if (p.type() == "Dog" || p.firstName() == "Fluffy") {`.*
* *The box on the right contains the text "Or here?" and its arrow points to the line `std::string returnStr = p.firstName() + " " + p.lastName();`.*

---

## Slide 27: What could go wrong?

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
                 p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

*Figure: A screenshot of C++ code within a dark-themed window. Four yellow speech bubbles annotate the code to highlight potential exception points:*
*   *A bubble on the left points to the line `if (p.type() == "Dog" || p.firstName() == "Fluffy") {` and reads: "What if this function threw an exception here?"*
*   *A bubble below the code points to the line `p.lastName() << " is paw-some!" << '\n';` and reads: "Or here?"*
*   *A bubble at the bottom points to the line `delete p;` and reads: "Or here?"*
*   *A bubble at the bottom right reads: "Or anywhere an exception can be thrown?"*

---

## Slide 28: What could go wrong?

*Figure: A dark-themed code editor window with red, yellow, and green window control dots in the top-left corner. The code contains a C++ function named `returnNameCheckPawsome`. The second line of code, `Pet* p = new Pet(petId);`, is highlighted with a light green background.*

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " << 
            p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

---

## Slide 29: What could go wrong?

*Figure: A dark-themed code editor window with red, yellow, and green control dots in the top-left corner. The window displays a C++ function definition.*

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

---

## Slide 30: What could go wrong?

*Figure: A code snippet displayed in a dark editor window with three colored dots in the top-left corner (red, yellow, green). A yellow callout box on the left side of the code points to the `if` block, containing the text: "exception here means memory leak".*

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

---

## Slide 31: This is not unique to just pointers!

It turns out that there are many resources that you need to **_release_** after **_acquiring_**

|              | Acquire   | Release   |
|--------------|-----------|-----------|
| **Heap memory** | `new`     | `delete`  |
| **Files**      | `open`    | `close`   |
| **Locks**      | `try_lock`| `unlock`  |
| **Sockets**    | `socket`  | `close`   |

---

## Slide 32: This is not unique to just pointers!

It turns out that there are many resources that you need to ***release*** after ***acquiring***

| | Acquire | Release |
| :--- | :---: | :---: |
| Heap memory | `new` | `delete` |
| Files | `open` | `close` |
| | `try_lock` | `unlock` |
| | `socket` | `close` |

*Figure: A yellow callout bubble in the bottom-left corner of the slide, pointing toward the table and partially obscuring the first column of the bottom two rows.*

How do we ensure
that we properly
release resources
in the case that we
have an exception?

---

## Slide 33: What questions do we have?
What questions do we have?

*Figure: A photograph of a small green and brown bird, resembling a parrot, held gently between a person's thumb and index finger. The bird is looking forward with a curious expression. Three stylized, red, cartoon question marks are depicted as floating in the air near the bird's head.*

---

## Slide 34: RAII

*Figure: A yellow horizontal banner at the top of the slide containing the text "RAII" in a large, bold font.*

# RAII

**RAII: Resource Acquisition is Initialization**

---

## Slide 35: RAII

### RAII: Resource Acquisition is Initialization

RAII was developed by this lad:

*Figure: A photo of a man with glasses, resting his chin on his hand, likely Bjarne Stroustrup.*

And it’s a concept that is very emblematic in C++, among other languages.

---

## Slide 36: RAII

**RAII: Resource Acquisition is Initialization**

RAII was developed by this lad:

*Figure: A small portrait photograph of a man with glasses and long hair, resting his chin on his hand.*

And it's a concept that is very emblematic in C++, among other languages.

**So what is RAII?**
* All resources used by a class should be acquired in the constructor!
* All resources that are used by a class should be released in the destructor.

---

## Slide 37: RAII

**RAII: Resource Acquisition is Initialization**

*Figure: A three-panel comic strip featuring a blue cat-like character and a robot rabbit named Robonny. In the first panel, the cat asks, "Robonny, what is RAII?" and Robonny replies, "Resource Acquisition Is Initialization!". In the second panel, the cat asks, "What does that mean?" and Robonny repeats, "Resource Acquisition... IS Initialization!". In the third panel, Robonny says "BEEP BOOP" while surrounded by diamond-shaped sparkles, as the cat character stares with a blank expression.*

---

## Slide 38: RAII: why tho?

**RAII: Resource Acquisition is Initialization**

*   By abiding by the RAII policy we avoid “half-valid” states.
*   No matter what, the destructor is called whenever the resource goes out of scope.
*   One more thing: the resource/object is usable immediately after it is created.

---

## Slide 39: RAII compliant?

*Figure: A code editor window with a dark background and three colored control buttons (red, yellow, green) in the top-left corner, displaying a C++ function.*

```cpp
void printFile() {
  ifstream input;
  input.open("hamlet.txt");

  string line;
  while(getLine(input, line)) { // might throw an exception
    std::cout << line << std::endl;
  }

  input.close();
}
```

---

## Slide 40: RAII compliant?

*Figure: A screenshot of a dark-themed code editor window with red, yellow, and green circular window control buttons at the top. Inside the window, a C++ function `printFile` is displayed. The lines `input.open("hamlet.txt");` and `input.close();` are highlighted with orange rectangular outlines. A yellow comment bubble with a black border points from the left side towards the code, specifically near the `input.open` line.*

```cpp
void printFile() {
    ifstream input;
    input.open("hamlet.txt");

    string line;
    while(getLine(input, line)) { // might throw an exception
        std::cout << line << std::endl;
    }
    input.close();
}
```

*Figure: A yellow comment bubble with the text: "the **ifstream** is opened and closed in code, not constructor & destructor".*

---

## Slide 41: Neither is this!

*Figure: A dark-themed code editor window, resembling a macOS interface with red, orange, and green window control dots in the top left corner, containing a C++ function implementation.*

```cpp
void cleanDatabase(mutex& databaseLock, map<int, int>& db) {
    databaseLock.lock();
    
    // no other thread or machine can change database
    // modify the database
    // if any exception is thrown, the lock never unlocks!
    
    database.unlock();
}
```

---

## Slide 42: Neither is this!

```cpp
void cleanDatabase(mutex& databaseLock, map<int, int>& db) {
    databaseLock.lock();
    // no other thread or machine can change database
    // modify the database
    // if any exception is thrown, the lock ne
    database.unlock();
}
```

*Figure: A code editor screenshot showing a C++ function `cleanDatabase`. The code has a dark background with syntax highlighting (blue keywords, green comments). The line `databaseLock.lock();` is highlighted with an orange box. A block of three comment lines is highlighted with a red box. The line `database.unlock();` is also highlighted with an orange box. To the right of the code is a yellow callout box with a thin black border pointing to the red-highlighted comment block. The callout contains the text: "If any code throws an exception in the red area, which we can call the ‘critical section’, the lock never unlocks!".*

---

## Slide 43: How can we fix this?

*Figure: A code editor window with a dark theme and three colored dots (red, yellow, green) in the top-left corner, displaying a C++ code snippet.*

```cpp
void cleanDatabase(mutex& databaseLock, map<int, int>& db) {
    lock_guard<mutex> lg(databaseLock);
    // no other thread or machine can change database
    // modify the database
    // if exception is throw, mutex is UNLOCKED!

    // no explicit unlock necessary, is handled by lock_guard
}
```

---

## Slide 44: How can we fix this?

*Figure: Screenshot of a code editor window with three colored dots (red, yellow, green) in the top-left corner. The window contains a C++ function definition with a highlighted line. A yellow, rounded callout box with an arrow points to the highlighted line of code.*

```cpp
void cleanDatabase(mutex& databaseLock, map<int, int>& db) {
    lock_guard<mutex> lg(databaseLock);
    // no other thread or machine can change database
    // modify the database
    // if exception is throw, mutex is released

    // no explicit unlock necessary
}
```

A lock guard is a RAII-compliant
wrapper that attempts to
acquire the passed in lock. It
releases the the lock once it goes
out of scope. Read more [here](https://en.cppreference.com/w/cpp/thread/lock_guard)

Links on this slide:
- <https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi7r47Is-OCAxVqLFkFHfwIBkYQFnoECA0QAw&url=https%3A%2F%2Fen.cppreference.com%2Fw%2Fcpp%2Fthread%2Flock_guard%23%3A~%3Atext%3DThe%2520class%2520lock_guard%2520is%2520a%2Cthe%2520mutex%2520it%2520is%2520given.&usg=AOvVaw3g32RuzE9h-7Y6jI-Gm8e4&opi=89978449>

---

## Slide 45: What questions do we have?

*Figure: A photograph of a small, green parrot with white markings on its face and striped feathers, being held in a person's hand. The parrot is looking to the left, and three red, cartoonish question marks float in the air to the left of its head, as if representing its confusion or the audience's questions.*

---

## Slide 46: Plan

1. RAII (Resource Acquisition Is Initialization)
2. **Smart Pointers**
3. Building C++ projects

*Figure: A presentation slide with a large yellow title bar at the top containing the word "Plan" in bold black text. Below the header is a numbered list of three topics. The second item, "Smart Pointers," is highlighted in bold black text, while the first and third items are in a lighter gray color.*

---

## Slide 47: Smart Pointers

RAII for locks → `lock_guard`

---

## Slide 48: Smart Pointers

*   RAII for locks → `lock_guard`
*   RAII for memory → 🤔

*Figure: A thinking face emoji (🤔) is displayed to the right of the second bullet point.*

---

## Slide 49: Smart Pointers

**R.11: Avoid calling `new` and `delete` explicitly**

### Reason
The pointer returned by `new` should belong to a resource handle (that can call `delete`). If the pointer returned by `new` is assigned to a plain/naked pointer, the object can be leaked.

### Note
In a large program, a naked `delete` (that is a `delete` in application code, rather than part of code devoted to resource management) is a likely bug: if you have N `delete`s, how can you be certain that you don't need N+1 or N-1? The bug may be latent: it may emerge only during maintenance. If you have a naked `new`, you probably need a naked `delete` somewhere, so you probably have a bug.

### Enforcement
(Simple) Warn on any explicit use of `new` and `delete`. Suggest using `make_unique` instead.

---

## Slide 50: Remember this?

*Figure: A screenshot of a code editor displaying a C++ function. The editor has a dark background with a macOS-style title bar featuring three colored dots (red, yellow, green) in the top-left corner.*

```cpp
std::string returnNameCheckPawsome(int petId) {
    Pet* p = new Pet(petId);
    if (p.type() == "Dog" || p.firstName() == "Fluffy") {
        std::cout << p.firstName() << " " <<
            p.lastName() << " is paw-some!" << '\n';
    }
    std::string returnStr = p.firstName() + " " + p.lastName();
    delete p;
    return returnStr;
}
```

---

## Slide 51: What did we do for locks?
### RAII for locks → lock_guard
- Created a new object that acquires the resource in the constructor and releases in the destructor

---

## Slide 52: What did we do for locks?

**RAII for locks $\rightarrow$ `lock_guard`**
*   Created a new object that acquires the resource in the constructor and releases in the destructor

**RAII for memory $\rightarrow$ We can do the same 🥳**

---

## Slide 53: What did we do for locks?

**RAII for locks → `lock_guard`**
* Created a new object that acquires the resource in the constructor and releases in the destructor

**RAII for memory → We can do the same 🥳**
* These “wrapper” pointers are called “smart pointers”!

---

## Slide 54: Visualizing smart pointers

### RAII for locks → `lock_guard`
* Created a new object that acquires the resource in the constructor and releases in the destructor

### RAII for memory → We can do the same 🥳
* These “wrapper” pointers are called “smart pointers”!

---

## Slide 55: Visualizing smart pointers

**Smart Pointer Class**

*Figure: A diagram illustrating a Smart Pointer Class. A large, light-gray box labeled "Smart Pointer Class" contains the red text "Dynamically Acquired Resource". Below this text, within the same box, is a solid red rectangle representing the actual, dynamically allocated memory or resource managed by the smart pointer.*

---

## Slide 56: Visualizing smart pointers

**RAII for memory → We can do the same 🥳**
* These “wrapper” pointers are called “smart pointers”!

There are three types of RAII-compliant pointers:
* **std::unique_ptr**
  * Uniquely owns its resource, can’t be copied

---

## Slide 57: Visualizing smart pointers

**RAII for memory → We can do the same 🥳**
* These “wrapper” pointers are called “smart pointers”!

There are three types of RAII-compliant pointers:
* **std::unique\_ptr**
    * Uniquely owns its resource, can’t be copied
* **std::shared\_ptr**
    * Can make copies, destructed when the ***underlying memory*** goes out of scope

---

## Slide 58: Visualizing smart pointers

**RAII for memory → We can do the same 🥳**
*   These “wrapper” pointers are called “smart pointers”!

There are three types of RAII-compliant pointers:
*   `std::unique_ptr`
    *   Uniquely owns its resource, can’t be copied
*   `std::shared_ptr`
    *   Can make copies, destructed when the **<u>underlying memory</u>** goes out of scope
*   `std::weak_ptr`
    *   A class of pointers designed to **<u>mitigate circular dependencies</u>**
        *   More on these in a bit

---

## Slide 59: What does this look like?

*Figure: A Drake Hotline Bling meme. The top panel shows Drake looking away and holding up a hand in rejection, positioned next to a code snippet in a dark window. The bottom panel shows Drake smiling and gesturing toward a second code snippet in a dark window in approval.*

```cpp
void rawPtrFn() {
  Node* n = new Node;
  // do smth with n
  delete n;
}
```

```cpp
void rawPtrFn() {
  std::unique_ptr<Node> n(new Node);
  // do something with n
  // n automatically freed
}
```

---

## Slide 60: What questions do we have?

*Figure: A photograph of a small green and brown parrot (possibly a Green-cheeked Conure) being held in a person's hand. Three large, red, three-dimensional question marks (one upright, two inverted) are floating near the parrot's head against a plain white background.*

---

## Slide 61: Remember we can’t copy unique pointers

*Figure: A dark-themed code editor window with red, yellow, and green circular buttons in the top-left corner, displaying C++ code.*

```cpp
void rawPtrFn() {
    std::unique_ptr<Node> n(new Node);

    // this is a compile-time error!
    std::unique_ptr<Node> copy = n;
}
```

---

## Slide 62: Why?

*Figure: A dark-themed code editor window with three colored dots (red, yellow, green) in the top-left corner, positioned next to a yellow callout bubble.*

```cpp
void rawPtrFn() {
    std::unique_ptr<Node> n(new Node);

    // this is a compile-time error!
    std::unique_ptr<Node> copy = n;
}
```

Imagine a case where the original destructor is called **_after_** the copy happens.

---

## Slide 63: Why?

*Figure: A presentation slide with the title "Why?" at the top. On the left is a dark-themed code editor window with three colored window control dots (red, yellow, and green) in the upper-left corner. On the right is a yellow rounded callout box containing explanatory text.*

```cpp
void rawPtrFn() {
    std::unique_ptr<Node> n(new Node);

    // this is a compile-time error!
    std::unique_ptr<Node> copy = n;
}
```

Imagine a case where the original destructor is called **after** the copy happens.

**Problem:** The copy points to deallocated memory!

---

## Slide 64: std::shared_ptr

Shared pointers get around our issue of trying to copy **std::unique_ptr**’s by not deallocating the underlying memory until **_all_** shared pointers go out of scope!

---

## Slide 65: std::shared_ptr

Shared pointers get around our issue of trying to copy **std::unique_ptr’s** by not deallocating the underlying memory until <u>all</u> shared pointers go out of scope!

*Figure: A diagram illustrating the structure of a `std::shared_ptr`. On the left is a box labeled "shared_ptr" divided into two sections: "Pointer to T" (top) and "Pointer to Control Block" (bottom). An arrow from "Pointer to T" points to a box above and to the right labeled "Data", which contains "T Object". An arrow from "Pointer to Control Block" points to a larger box below and to the right labeled "Control Block". This Control Block box is subdivided into three sections: "Reference Count" (top, light blue), "Weak Count" (middle, gray), and "Custom Deleter, Allocator, etc" (bottom, orange).*

---

## Slide 66: Initializing smart pointers!

*Figure: A dark terminal window with three colored circles (red, yellow, and green) at the top left, displaying three lines of C++ code for initializing smart pointers.*

```cpp
std::unique_ptr<T> uniquePtr{new T};
std::shared_ptr<T> sharedPtr{new T};
std::weak_ptr<T> wp = sharedPtr;
```

---

## Slide 67: Initializing smart pointers!

We're still explicitly calling **new**

no....no

*Figure: A dark-themed code editor window with red, yellow, and green window control buttons at the top-left. The code shows three lines of C++ smart pointer initialization. The `{new T}` segments in the first two lines are highlighted with orange rectangular outlines. To the left of the code, a yellow speech bubble points toward the window.*

```cpp
std::unique_ptr<T> uniquePtr{new T};
std::shared_ptr<T> sharedPtr{new T};
std::weak_ptr<T> wp = sharedPtr;
```

---

## Slide 68: Initializing smart pointers!

*Figure: A dark-themed code editor window showing C++ code snippets for smart pointer initialization. The window has three colored control buttons (red, yellow, green) in the top left. Two lines of code are highlighted with orange rectangular boxes.*

```cpp
// std::unique_ptr<T> uniquePtr{new T};
std::unique_ptr<T> uniquePtr = std::make_unique<T>();

// std::shared_ptr<T> sharedPtr{new T};
std::shared_ptr<T> sharedPtr = std::make_shared<T>();

std::weak_ptr<T> wp = sharedPtr;
```

---

## Slide 69: Initializing smart pointers!

**Always use std::make_unique\<T\> and std::make_shared\<T\>**

* We should also be consistent — if you use **make_unique** also use **make_shared**!

*Figure: A lecture slide with a bright yellow header bar containing the title "Initializing smart pointers!". The body of the slide contains a bold recommendation for using `std::make_unique` and `std::make_shared` for smart pointer initialization, followed by a bullet point emphasizing consistency in their usage.*

---

## Slide 70: std::weak_ptr

*   A pointer that can look at an object owned by a shared\_ptr without claiming ownership of it
*   Does not affect the reference count at all

---

## Slide 71: std::weak_ptr

Weak pointers are a way to **avoid circular dependencies** in our code so that we don't leak any memory.

---

## Slide 72: Circular Reference Example

*Figure: A screenshot of a code editor window (macOS style) with three colored control buttons (red, yellow, green) at the top-left corner. The editor displays a C++ source file illustrating a circular reference between two classes using `std::shared_ptr`.*

```cpp
#include <iostream>
#include <memory>

class B;

class A {
  public:
    std::shared_ptr<B> ptr_to_b;
    ~A() {
      std::cout << "All of A's resources deallocated" << std::endl;
    }
};

class B {
  public:
    std::shared_ptr<A> ptr_to_a;
    ~B() {
      std::cout << "All of B's resources deallocated" << std::endl;
    }
};

int main() {
  std::shared_ptr<A> shared_ptr_to_a = std::make_shared<A>();
  std::shared_ptr<A> shared_ptr_to_b = std::make_shared<B>();
  a->ptr_to_b = shared_ptr_to_b;
  b->ptr_to_a = shared_ptr_to_a;
  return 0;
}
```

---

## Slide 73: std::weak_ptr bad example

*Figure: A lecture slide with a yellow header titled "std::weak_ptr bad example". The slide is divided into a dark-themed code editor on the left and an explanatory text block on the right. Three orange rectangular boxes highlight specific sections of the C++ code: one around the member declaration `std::shared_ptr<B> ptr_to_b;` in `class A`, one around `std::shared_ptr<A> ptr_to_a;` in `class B`, and one around the two assignment statements in the `main` function.*

Both instance **a** of class **A** and instance **b** class **B** are keeping a shared pointer to each other.

```cpp
#include <iostream>
#include <memory>

class B;

class A {
  public:
    std::shared_ptr<B> ptr_to_b;
    ~A() {
      std::cout << "All of A's resources deallocated" << std::endl;
    }
};

class B {
  public:
    std::shared_ptr<A> ptr_to_a;
    ~B() {
      std::cout << "All of B's resources deallocated" << std::endl;
    }
};

int main() {
  std::shared_ptr<A> shared_ptr_to_a = std::make_shared<A>();
  std::shared_ptr<B> shared_ptr_to_b = std::make_shared<B>();
  shared_ptr_to_a->ptr_to_b = shared_ptr_to_b;
  shared_ptr_to_b->ptr_to_a = shared_ptr_to_a;
  return 0;
}
```

---

## Slide 74: std::weak_ptr bad example

Both instance **a** of class A and instance **b** class B are keeping a shared pointer to each other.

Therefore, they will never properly deallocate

*Figure: A screenshot of a code editor window (showing red, yellow, and green window controls) containing C++ code. Orange rectangular highlights are drawn around three parts of the code: the declaration of `ptr_to_b` in `class A`, the declaration of `ptr_to_a` in `class B`, and the two assignment lines in the `main` function.*

```cpp
#include <iostream>
#include <memory>

class B;

class A {
public:
    std::shared_ptr<B> ptr_to_b;
    ~A() {
        std::cout << "All of A's resources deallocated" << std::endl;
    }
};

class B {
public:
    std::shared_ptr<A> ptr_to_a;
    ~B() {
        std::cout << "All of B's resources deallocated" << std::endl;
    }
};

int main() {
    std::shared_ptr<A> shared_ptr_to_a = std::make_shared<A>();
    std::shared_ptr<B> shared_ptr_to_b = std::make_shared<B>();
    a->ptr_to_b = shared_ptr_to_b;
    b->ptr_to_a = shared_ptr_to_a;
    return 0;
}
```

---

## Slide 75: std::weak_ptr good example

*Figure: A split-view slide. The left half contains a C++ code snippet on a dark background, showing classes A and B with a circular pointer relationship. A specific line in class B is highlighted with an orange rectangular border. The right half contains explanatory text.*

### Code Example

```cpp
#include <iostream>
#include <memory>

class B;

class A {
public:
    std::shared_ptr<B> ptr_to_b;
    ~A() {
        std::cout << "All of A's resources deallocated" << std::endl;
    }
};

class B {
public:
    std::weak_ptr<A> ptr_to_a;
    ~B() {
        std::cout << "All of B's resources deallocated" << std::endl;
    }
};

int main() {
    std::shared_ptr<A> shared_ptr_to_a = std::make_shared<A>();
    std::shared_ptr<A> shared_ptr_to_b = std::make_shared<B>();
    a->ptr_to_b = shared_ptr_to_b;
    b->ptr_to_a = shared_ptr_to_a;
    return 0;
}
```

### Explanation

Here, in class B we are no longer storing **a** as a `shared_ptr` so it does not increase the reference count of **a**.

Therefore **a** can gracefully be deallocated, and therefore so can **b**

---

## Slide 76: What questions do we have?

*Figure: A photograph of a person's hand gently holding a green parrot. Three red, cartoon-style question marks are floating around the parrot's head, suggesting confusion or inquiry.*

---

## Slide 77: Plan

*Figure: A wide, solid yellow horizontal bar across the top of the slide, containing the title "Plan" in large, bold, black text.*

1. RAII (Resource Acquisition Is Initialization)
2. Smart Pointers
3. **Building C++ projects**

---

## Slide 78: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

---

## Slide 79: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

*Figure: A diagram illustrating the compilation process. On the left, a box labeled **Source Code** contains a C++ code snippet. An orange arrow points from this box to a central box labeled **Compiler**. Another orange arrow points from the Compiler box to a box on the right labeled **Machine Code**, which contains four lines of binary digits. Below this diagram is a gray rectangular box containing terminal commands.*

**Source Code**
```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

**Machine Code**
```
10110101
01011010
10011101
10110001
```

**Terminal**
```
$ g++ main.cpp -o main    # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

---

## Slide 80: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

*Figure: A diagram illustrating the compilation process. A box labeled "Source Code" contains a snippet of C++ code. A thick arrow points from this box to a central box labeled "Compiler". A second thick arrow points from the compiler to a box on the right labeled "Machine Code" containing binary digits.*

**Source Code**
```cpp
std::cout << "Hello World" << std::endl;
std::cout << "Welcome to " << std::endl;
for (char ch : "CS106L")
{
    std::cout << ch << std::endl;
}
```

**Machine Code**
10110101
01011010
10011101
10110001

```
$ g++ main.cpp -o main      # g++ is the compiler, outputs binary to main
$ ./main                    # This actually runs our program
```

---

## Slide 81: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

```
$ g++ main.cpp -o main    # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

*Figure: A terminal code box showing two shell commands. An arrow points from a callout bubble to the highlighted `g++` token in the first line. The callout bubble reads: "This is the compiler command".*

---

## Slide 82: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

```
$ g++ main.cpp -o main    # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

*Figure: A terminal command box showing two shell commands. The first line compiles `main.cpp` using `g++` and outputs the binary to `main`. The second line runs the compiled program. A callout annotation box below with an arrow points upward to `main.cpp` in the first command, with the label "This is the source file".*

---

## Slide 83: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

```bash
$ g++ main.cpp -o main    # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

*Figure: A terminal command box showing two shell commands. In the first command, `g++ main.cpp -o main`, the text `main.cpp` and the flag `-o` are highlighted in yellow. Both commands include comments in gray. A blue rounded-rectangle callout box contains the text "This means that you’re going to give a specific name to your executable", with an arrow pointing from the callout to the `-o main` part of the first command.*

---

## Slide 84: Compilation Crash Course

When we write C++ code, it needs to be translated into a form our computer understands it

```bash
$ g++ main.cpp -o main     # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

*Figure: A diagram shows a terminal code box containing the two bash commands above. An arrow points from a callout box with the text "In this case it’s main" to the word `main` in the first command's output argument `-o main`.*

---

## Slide 85: GPU Programming

*Figure: Top-left quadrant showing a graphic for NVIDIA CUDA. The graphic features a green, 3D grid background. Overlaid on this background is the text "GPU Programming" in the upper left, and in the center is the NVIDIA logo (a stylized eye) above the text "NVIDIA CUDA".*

*Figure: Top-right quadrant showing the logos of three financial or trading companies against a background image of a busy office/trading floor with multiple monitors. The logos are, from left to right: Optiver (blue background with white text and a red triangle), Citadel Securities (blue background with white stylized text and icon), and HRT (white background with large orange letters "HRT").*

*Figure: Bottom-left quadrant showing a white Tesla Model Y car driving on a road. In the lower right corner of this quadrant, the logos for Tesla (red "T") and Waymo (green "W" icon) are displayed.*

Even the masterpiece
among us

*Figure: Bottom-right quadrant showing an illustration of a red crewmate character from the game "Among Us". The character has a black outline, a blue visor, and is set against a solid yellow background.*

---

## Slide 86: TensorFlow

*Figure: A screenshot of the TensorFlow project's GitHub repository page, featuring the TensorFlow logo, various status and metadata badges, and introductory text. Below the screenshot, a sentence on the slide background states: "The TensorFlow Core is written largely in C++ and it is composed of 2,000+ source files", with the phrase "composed of 2,000+ source files" highlighted in a yellow box.*

**TensorFlow**

python 3.9 | 3.10 | 3.11 | 3.12
pypi package 2.18.0
DOI 10.5281/zenodo.4724125
openssf best practices passing
openssf scorecard 7.8
oss-fuzz build failing
oss-fuzz build failing
OSSRank #12 (Top 1%)
Contributor Covenant v1.4 adopted
TF Official Continuous 6 passed, 0 failed
TF Official Nightly 11 passed, 4 failed

Documentation
api reference

TensorFlow is an end-to-end open source platform for machine learning. It has a comprehensive, flexible ecosystem of tools, libraries, and community resources that lets researchers push the state-of-the-art in ML and developers easily build and deploy ML-powered applications.

TensorFlow was originally developed by researchers and engineers working within the Machine Intelligence team at Google Brain to conduct research in machine learning and neural networks. However, the framework is versatile enough to be used in other areas as well.

TensorFlow provides stable Python and C++ APIs, as well as a non-guaranteed backward compatible API for other languages.

The TensorFlow Core is written largely in C++ and it is composed of 2,000+ source files

---

## Slide 87: Cute Command Meme

*Figure: A meme featuring Linus Torvalds sitting at a desk in front of two CRT monitors. A thought bubble above him contains the text: "Lol, that’s a cute command 😭". In the background, a portion of the TensorFlow website is visible, displaying the TensorFlow logo and introductory text. The visible background text reads: "...has a comprehensive, flexible...", "...push the state-of-the-art in ML and...", and "TensorFlow provides stable [Python](https://www.tensorflow.org/) and [C++](https://www.tensorflow.org/) APIs, as well as a non-guaranteed backward compatible API for [other languages](https://www.tensorflow.org/)."*

Lol, that’s a cute command 😭

```bash
$ g++ main.cpp -o main    # g++ is the compiler, outputs binary to main
$ ./main                  # This actually runs our program
```

---

## Slide 88: Makefiles and make

make is a “build system” program that helps you compile!

* This way you don’t have to manually compile every single file in your project
* You can specify what compiler you want to use
* In order to use **make** you need to have a **Makefile**
* Make tracks which files have changed since last compile

What does a **Makefile** look like? Let’s take a look!

---

## Slide 89: Example Makefile

```makefile
# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++20

# Source files and target
SRCS = $(wildcard *.cpp)
TARGET = main

# Default target
all:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

# Clean up
clean:
	rm -f $(TARGET)
```

*Figure: A rounded callout box with a light beige background and blue border, positioned to the right of the Makefile code, containing the text: "This is an example Makefile for our lecture 8 code"*

---

## Slide 90: What questions do we have?

What questions do we have?

*Figure: A photograph of a small, green and brown parrot being held in a person's hand. Three red, cartoon-style question marks are drawn floating near the bird's head.*

---

## Slide 91: CMake

**CMake** is a build system generator.

So you can use **CMake** to generate Makefiles

Is like a higher level abstraction for Makefiles

*Figure: The CMake logo, consisting of a stylized multicolored triangle (blue, red, green, and white) positioned to the left of the word "CMake" in a dark blue-gray serif font.*

---

## Slide 92: CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)

project(cs106l_classes)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SRC_FILES "*.cpp")

add_executable(main ${SRC_FILES})
```

---

## Slide 93: CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)
project(cs106l_classes)
set(CMAKE_CXX_STANDARD 20)
file(GLOB SRC_FILES "*.cpp")
add_executable(main ${SRC_FILES})
```

*Figure: A rounded callout box on the right points to the line `set(CMAKE_CXX_STANDARD 20)` and contains the text: "This command tells CMAKE to set the C++ compiler to C++20".*

---

## Slide 94: CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)
project(cs106l_classes)
set(CMAKE_CXX_STANDARD 20)
file(GLOB SRC_FILES "*.cpp")
add_executable(main ${SRC_FILES})
```

*Figure: A rounded-corner callout box on the right side of the slide. It contains text explaining the `GLOB` command: "This GLOB command is telling the CMAKE program to do a wildcard search for all files that have the pattern “*.cpp”".*

---

## Slide 95: CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)
project(cs106l_classes)
set(CMAKE_CXX_STANDARD 20)
file(GLOB SRC_FILES "*.cpp")
add_executable(main ${SRC_FILES})
```

*Figure: A rounded rectangular callout box contains the text "This command adds all of the source files of our program into the executable". The last line of the CMake code, `add_executable(main ${SRC_FILES})`, is highlighted in yellow, indicating the command being described.*

---

## Slide 96: To use CMAKE

1. You need to have a `CMakeLists.txt` file in your project’s root directory
2. Make a build folder (`mkdir build`) within your project!
3. Go into the build folder (`cd build`)
4. Run `cmake ..`
   a. This command runs cmake using the `CMakeLists.txt` in your project’s root folder!
   b. This generates a `Makefile`
5. Run `make`
6. Execute your program using `./main` as usual

---

## Slide 97: Quizziz

https://wayground.com/join?gc=20919921

Links on this slide:
- <https://wayground.com/join?gc=20919921>

---

## Slide 98: A recap

*Figure: A slide with a pale yellow gradient header bar across the top containing the title.*

*   RAII says that dynamically allocated resources should be acquired inside of the constructor and released inside the destructor.
    *   This is what smart pointers do for example
*   For compiling our projects we can and should use Makefiles
*   For making our Makefiles we can and should use CMAKE

---

## Slide 99: Last (mandatory) lecture 😢

### Schedule

| Week | Tuesday | Thursday |
| :--- | :--- | :--- |
| 1 | September 23<br>1. Welcome!<br>📋 Slides<br>📋 Policies | September 25<br>2. Types & Structs<br>📋 Slides |
| 2 | September 30<br>3. Initialization & References<br>📋 Slides | October 2<br>4. Streams<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">AS: Setup</span> |
| 3 | October 7<br>5. Containers<br>📋 Slides | October 9<br>6. Iterators & Pointers<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">AL: SimpleImpl</span> |
| 4 | October 14<br>7. Classes<br>📋 Slides | October 16<br>8. Inheritance<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">AL: ManagePart</span> |
| 5 | October 21<br>9. Class Templates & Const Correctness<br>📋 Slides | October 23<br>10. Function Templates<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">A3: Make a Class</span> |
| 6 | October 28<br>11. Functions & Lambdas<br>📋 Slides | October 30<br>12. Operator Overloading<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">A4: tweet</span> |
| 7 | November 4<br>Democracy Day: No Class | November 6<br>13. Special Member Functions<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">A5: Treebooks</span> |
| 8 | November 11<br>14. Move Semantics<br>📋 Slides | November 13<br>15. std::optional & Type Safety<br>📋 Slides<br><span style="color: white; background-color: #d9534f; padding: 2px 6px; border-radius: 4px; font-size: 0.8em;">A6: ExploreCourse</span> |
| 9 | November 18<br>16. RAII, Smart Pointers, & Building C++ Projects | November 20<br>Optional: No Class, Extra Office Hours |
| 10 | December 2<br>Optional: No Class, Extra Office Hours | December 4<br>Optional: No Class, Extra Office Hours |

*Figure: A thick blue arrow points from the left margin of the slide towards the cell for Week 9, Tuesday, November 18.*

---

## Slide 100: The C++ Iceberg

*Figure: A meme-style iceberg illustration titled "The C++ Iceberg." The tip of the iceberg above the water contains C++ features and quirks that are well-known to intermediate programmers. The massive underwater portion contains increasingly obscure, controversial, or deeply technical C++ topics. Text labels are scattered across both the above-water and below-water sections.*

### Above the water (tip of iceberg)

- 0[arr]
- #define private public
- inline does not mean inline
- most vexing parse
- \<iosfwd\>
- C++ is not a superset of C
- protected abstract virtual base pure
- virtual private destructor
- spaceship operator
- --> operator
- digraphs
- else if is a lie

### Below the water (submerged iceberg)

- vector\<bool\> is broken
- unary minus with unsigned operand
- templates turing completeness was an accident
- analog integer litters
- zapcc compiler
- std::move does not move
- std::remove does not remove
- the strange details of std::string
- iostream was a mistake
- rvalue references are lvalues
- function try blocks
- T& is not an rvalue reference
- shared\_ptr is an anti-pattern
- initialization matrix
- the for loop is broken
- constexpr does not mean what you think it means
- const std::string bitand
- templates are obfuscated haskell
- the grand error explosion competition
- operator,( )
- herbceptions
- std::optional is a monad
- C++0x is a hexadecimal name
- C++ disproves fermat's last theorem
- heap and stack don't exist
- hello world has a bug
- C++0x concepts were rust traits
- godbolt is a real person

[ source ]

Links on this slide:
- <https://victorpoughon.github.io/cppiceberg/>

---

## Slide 101: Announcements

* Optional Lecture on C++ Iceberg **held Tuesday of Week 9**
    * Come join us for fun or if you need to make up an attendance!
* Assignment 6 due Friday, 05/22
* Assignment 7 due Friday, 05/29 (will be released this on Friday)
* Check your grade on the website and let us know if something looks off. This is what we use to determine C/NC for this course.

---

## Slide 102: Thank you for a great quarter!

# Thank you for a great quarter!

*Figure: A photo of a person wearing a red t-shirt with "NERD" printed on it, holding a black tray with a chocolate cake. The cake is decorated with colorful icing letters that spell "CS 106B". A red "BURBANK" banner and a colorful mural are visible in the background.*

pseay@stanford.edu

*Figure: A photo of a person with a small green bird perched on their hand.*

rfern@stanford.edu

Links on this slide:
- <mailto:pseay@stanford.edu>
- <mailto:rfern@stanford.edu>
