# Lecture 11: LambdasAndFunctors (2026Spring)

> PDF title: 2026Spring-11-LambdasAndFunctors
> Source: `assets/slides/2026Spring-11-LambdasAndFunctors.pdf` · 137 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Welcome back! Link to Attendance Form ↓

*Figure: A black and white QR code. The code consists of a grid of small black dots and three large, nested squares in the top-left, top-right, and bottom-left corners, which are standard positioning markers for a QR code. The code is centered below the heading text.*

Welcome back! Link to Attendance Form ↓

---

## Slide 2: Recall: Template Functions

*   Turn to a partner and discuss:
    *   What’s one thing you remember from Thursday’s lecture on function templates?

---

## Slide 3: Recall: Writing a min function

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

*Figure: A yellow circular emoji with a monocle over its right eye, winking and smiling. It is positioned over the right side of the code block.*

---

## Slide 4: Recall: Writing a min function

```cpp
int min(int a, int b) {
    return a < b ? a : b;
}
```

```cpp
double min(double a, double b) {
    return a < b ? a : b;
}
```

```cpp
std::string min(std::string a, std::string b) {
    return a < b ? a : b;
}
```

*Figure: Three versions of a C++ `min` function are displayed inside a bordered box. In each function signature, the return type and the types of the parameters are obscured by light-colored rectangular overlays. A yellow emoji face with a magnifying glass is positioned on the right side of the box.*

---

## Slide 5: Recall: Writing a min function

*Figure: A cartoon yellow face emoji wearing a monocle, looking to the side, appears to the right of the code blocks.*

```cpp
T min(T a, T b) {
    return a < b ? a : b;
}
```

```cpp
T min(T a, T b) {
    return a < b ? a : b;
}
```

```cpp
T min(T a, T b) {
    return a < b ? a : b;
}
```

---

## Slide 6: Recall: Writing a min function

```cpp
T min( T a, T b) {
  return a < b ? a : b;
}
```

*Figure: The slide title is "Recall: Writing a min function". Below the title is a large light-grey box with a blue border containing a C++ function template. Three instances of the letter "T" in the function signature are enclosed in individual small white rectangular boxes. To the right of the code box is a cartoon yellow emoji wearing a monocle/magnifying glass and looking to the right. Below the first large box is another identical-sized, empty light-grey rectangular box with a blue border.*

---

## Slide 7: Recall: Writing a min function

```cpp
template <typename T>
T min( T a, T b) {
    return a < b ? a : b;
}
```

*Figure: A yellow emoji face with a monocle, appearing to the right of the code, symbolizing a closer look or inspection.*

---

## Slide 8: Recall: Writing a templated min function

*Figure: A diagram illustrating a C++ template. A code snippet is shown inside a bordered box. An annotation box on the left, labeled "This is a template," has an arrow pointing to the `template <typename T>` line. An annotation box on the right, labeled "T gets replaced with a specific type," has an arrow pointing to the `T` within the template declaration.*

```cpp
template <typename T>
T min(T a, T b) {
    return a < b ? a : b;
}
```

---

## Slide 9: Recall: explicit instantiation

Template functions cause the compiler to **generate code** for us

```cpp
min<int>(106, 107);    //
min<double>(1.2, 3.4); //
```

*Figure: A four-panel comic illustrating the programmer's emotional journey during compilation. In the first three panels, a character sits at a desk with a green "Compiling..." progress bar on the computer screen, looking increasingly frustrated and saying, "I hate programming". In the final fourth panel, the screen displays "Compiled Successfully" and the character is smiling with arms raised, exclaiming, "I love programming". Social media handles for "/techindustan" on Facebook, Twitter, and Instagram are visible at the bottom of the comic.*

---

## Slide 10: Recall: explicit instantiation
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

## Slide 11: Recall: Implicit instantiation is kind of like auto

*Figure: A code snippet enclosed in a rectangular box with a drop shadow.*

```cpp
int m = min(106, 107);
```

It’s exactly as if we wrote
```cpp
min<int>(106, 107)
```

---

## Slide 12: Recall: Writing a templated find function
This find function generalizes across all iterator types!

*Figure: A code snippet of a templated `find` function enclosed in a white box with a black border and a drop shadow. The template parameters and their uses in the function signature are highlighted with colored underlines: red underlines for the `It` type and green underlines for the `T` type.*

```cpp
template <typename It, typename T>
It find(It begin, It end, const T& value) {
  for (auto it = begin; it != end; ++it) {
    if (*it == value) return it;
  }
  return end;
}
```

---

## Slide 13: Recall: Writing a templated find function

Our `find` function works for other vectors, or even other containers

```cpp
std::vector<std::string> v { "run", "forrest" };
auto it = find(v.begin(), v.end(), "run");
// It = vector<std::string>::iterator
// T = std::string

std::set<std::string> s { "run", "forrest" };
auto it = find(s.begin(), s.end(), "run");
// It = std::set<std::string>::iterator
// T = std::string
```

*Figure: A black-bordered callout box in the bottom right corner contains red text and an explanation. The text reads: "Implicit Instantiation!" followed by "Compiler deduces template types by looking at arguments".*

---

## Slide 14: Wait... why pass in iterators to find?

Wait... why pass in iterators to find?

---

## Slide 15: Recall: Writing a templated find function

Our `find` function works for other vectors, or even other containers

```cpp
std::vector<std::string> c { "run", "forrest" };
auto it = find(c.begin(), c.end(), "run");
```

```cpp
std::set<std::string> c { "run", "forrest" };
auto it = find(c.begin(), c.end(), "run");
```

---

## Slide 16: Recall: Writing a templated find function

Our `find` function works for other vectors, or even other containers

*Figure: Two code examples are shown, both using the same `find` function but with different container types. In each example, the specific container type declaration is enclosed in a light gray box to highlight its interchangeability.*

```cpp
std::vector<std::string> c { "run", "forrest" };
auto it = find(c.begin(), c.end(), "run");

std::set<std::string> c { "run", "forrest" };
auto it = find(c.begin(), c.end(), "run");
```

---

## Slide 17: Recall: Writing a templated find function

Our `find` function works for other vectors, or even other containers

*Figure: A meme image from the movie "The Other Woman" showing Leslie Mann holding two identical photographs, with the caption "They're the same code" at the bottom. On the left side of the meme, two code blocks are displayed.*

```cpp
std::vector<std::string> c { "run", "forrest" };
auto it = find(c.begin(), c.end(), "run");

std::set<std::string> c { "run", "forrest" };
auto it = find(c.begin(), c.end(), "run");
```

---

## Slide 18: An alternative `find` function

We can pass the whole container.

```cpp
template <typename Container, typename T>
auto find(const Container& c, const T& value) { 
    for (auto it = c.begin(); it != c.end(); ++it) {
        if (*it == value) return it;
    }
    return end;
}

std::vector<std::string> v { "run", "forrest" };
auto it = find(v, "run");
```

*Figure: A diagrammatic slide showing a C++ function template and its usage. A callout box on the right contains the text "Advantage: Now the caller doesn't have to worry about begin and end!" with a black arrow pointing to the function call `find(v, "run")`. Another callout box at the bottom right specifies the template parameter deduction: "Container = std::vector<std::string>" and "T = std::string".*

---

## Slide 19: An alternative `find` function

Using iterators instead allows us to search *only part* of a container

```cpp
std::vector<int> v { 106, 107, 106, 143, 149, 106 };

// Search for 106L, skipping first and last elements
auto it = find(v.begin() + 1, v.end() - 1, 106);

// Get index of iterator using std::distance
std::cout << std::distance(v.begin(), it);
// Prints 2, not 0
```

*Figure: A red bracket spans the elements `107, 106, 143, 149` in the vector initialization, visually indicating the sub-range of the container that is being searched by the `find` function.*

---

## Slide 20: Generalized Find Function

We defined our `find` function in a `general` way!

---

## Slide 21: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, wearing glasses and a patterned shirt, with his hand near his chin. In the background, a poster reads "PROGRAMMING LANGUAGE BJARNE STROUSTRUP". Below the image is a caption.*

bjarne_about_to_raise_hand

---

## Slide 22: How can we make find even more general!?

- Instead of `find` searching for `value` in a container…
- What if we could ask arbitrary questions?
  - A vowel in a `string`?
  - A prime number in a `vector<int>`?
  - A number divisible by 5 in a `set<int>`?
- More generally, what if we could perform arbitrary operations?

---

## Slide 23: An even better find function?
How else could we generalize this?

```cpp
template <typename Container, typename T>
auto find(const Container& c, const T& value) { for
    (auto it = c.begin(); it != c.end(); ++it) {
        if (*it == value) return it;
    }
    return end;
}

std::vector<std::string> trail_lens = { "6mi", "20ft", "5km" };
auto it = find(trail_lens, "3mi");
```

*Figure: A screenshot of a unit conversion tool titled "Length" showing the conversion "5 Kilometer = 3.10686 Mile". At the bottom of the widget, it includes a note: "Formula: for an approximate result, divide the length value by 1.609".*

---

## Slide 24: An even better `find` function?
How else could we generalize this?

*Figure: A white rectangular box with a black border containing a C++ code snippet. Three light-grey rectangular boxes are overlaid on specific parts of the code as placeholders. The first box is in the function parameter list and contains the word "Question". The second box is inside the loop body as a condition and contains "Question??". The third box is an argument to the function call and contains "Is it a good length?".*

```cpp
template <typename Container, typename Q>
auto find(const Container& c, Question {
    for (auto it = c.begin(); it != c.end(); ++it) {
        Question?? return it;
    }
    return end;
}

std::vector<std::string> trail_lens = { "6mi", "20ft", "5km" };
auto it = find(trail_lens, Is it a good length? );
```

---

## Slide 25: AllTrails Lambdas

*Figure: A collage of images. On the left, a photograph shows a woman sitting on a rocky cliff overlooking a valley at sunset. Below that is the **AllTrails** logo. In the center and right-center are two phone screenshots of the AllTrails app's filter/sort interface, overlaid on a background photo of green foliage and a butterfly. On the right is a large cartoon illustration of Scrooge McDuck gleefully swimming through a pile of gold coins and dollar bills, with smaller ducks around him. A red arrow points from the bottom caption up toward Scrooge McDuck.*

**Left phone screenshot (AllTrails Filters screen):**

```
X  Filters

Length                              5-20 mi
[----o--------o]

Elevation gain                   1000-5000 ft+
[----------o----o]

Suitability
Dog-friendly                    ☑
Kid-friendly                    ☐
Wheelchair-friendly ⓘ          ☐
Show more

Attractions
Waterfalls                      ☐
Views                           ☑
Wildflowers                     ☑
Show more

Clear                      [Show 21 trails]
```

**Right phone screenshot (AllTrails Filters screen):**

```
X  Filters

Sort
Best match                    ○
Most popular                  ○
Closest                       ●
Newly add...

Plus
Distance
Show trails b...

Activity
Hiking
Mountain B...
Running
Show mor...

Clear
```

(He knew about lambdas.)

---

## Slide 26: Lecture 11: Functions & lambdas

*Figure: A photograph of a dirt path winding through a sunlit forest with lush green trees on both sides.*

Preston Seay & Rachel Fernandez

CS106L, Spring 2026

Lecture 11:

Functions & lambdas

---

## Slide 27: Today's Agenda

* Functions and Lambdas
    * How can we represent functions as variables in C++?
* Algorithms
    * Tackling a popular algorithm with modern C++
* Ranges and Views
    * A brand new (C++26), functional approach to C++ algorithms

---

## Slide 28: Announcements

*Figure: The slide has a background image of a sunlit path winding through a forest with tall, leafy trees on both sides.*

*   **We want to make this class easier**
    *   We’ll be going over the first half of A4 in class
    *   You can now skip 1 assignment for the rest of the quarter
*   **Assignments**
    *   A4 is out... you can complete it after today
    *   A2 grades are out
*   **Office hours**
    *   Thursdays 4:30-5:20 (after class) in Thornt 210
    *   Fridays 1:30-2:20 in 160-315

---

## Slide 29: Functions and Lambdas

*Figure: A faded background photograph of a dirt path winding through a lush green forest with many trees and bright sunlight filtering through the leaves. The title "Functions and Lambdas" is overlaid in large, bold black text across the center of the slide.*

---

## Slide 30: Definition: A predicate is a boolean-valued function

Definition: A predicate is a `boolean`-valued function

---

## Slide 31: Definition of a Predicate

**Definition:** A predicate is a `boolean`-valued function

*Figure: Two thought bubbles (clouds) are shown as examples of predicates. The top bubble contains the question "Does the trail have a waterfall?". The bottom bubble contains the question "Is this trail longer than that one?".*

---

## Slide 32: Predicate Examples

### Unary

```cpp
bool isVowel(char c) {
  c = toupper(c);
  return c == 'A' || c == 'E' ||
    c == 'I' || c == 'O' || c == 'U';
}
bool wouldPrestonApproveOf(Trail t)
{
    return t.hasWaterfall();
}
```

*Figure: An image of a person (presumably Preston) looking up in awe at a large waterfall.*

### Binary

```cpp
bool isDivisible(int n, int d) {
    return n % d == 0;
}
bool isLongerThan(Trail x, Trail y){
    return x.len > y.len;
}
```

---

## Slide 33: Using predicates

*   How can we use `isVowel` to find the first vowel in a `string`?
*   Or `wouldPrestonApproveOf` to find a trail with a waterfall in a `vector<Trail>`?
*   Or `isDivisible` to find a number divisible by 5?

---

## Slide 34: Key Idea: We need to pass a predicate to a function

**Key Idea: We need to pass a predicate to a function**

---

## Slide 35: Modifying our find function

```cpp
template <typename It, typename T>
It find(It first, It last, const T& value) {
    for (auto it = first; it != last; ++it) {
        if (*it == value) return it;
    }
    return last;
}
```

*Figure: A C++ template function `find` is shown. An arrow points from the condition `*it == value` to an annotation box containing the text: "This condition worked for finding a specific value, but it's too specific. How can we modify it to handle a general condition?"*

---

## Slide 36: Modifying our find function

```cpp
template <typename It>
It find(It first, It last, ???? pred) {
    for (auto it = first; it != last; ++it) {
        if (*it == value) return it;
    }
    return last;
}
```

*Figure: A code snippet showing a C++ template `find` function. The parameter list includes a highlighted placeholder `???? pred`. A callout bubble with an arrow points to this placeholder, containing the text: "What if we could instead pass a predicate to this function as a parameter?"*

---

## Slide 37: Modifying our find function

```cpp
template <typename It>
It find(It first, It last, ???? pred) {
    for (auto it = first; it != last; ++it) {
        if (*it == value) return it;
    }
    return last;
}
```

*Figure: A code block with two annotations. An arrow points from a text box to the parameter `???? pred` in the function signature, with the text: "What if we could instead pass a predicate to this function as a parameter?". Another arrow points from a second text box to the highlighted expression `(*it == value)`, with the text: "Then we could replace this critical section of the code with a call to our predicate."*

---

## Slide 38: Modifying our find function

*Figure: A code box containing a partially grayed-out C++ template function `find`. The line `It find(It first, It last, ???? pred) {` is grayed, except for the highlighted blue parameter name `pred`. The loop body `if (pred(*it)) return it;` is grayed, but the condition `(pred(*it))` is highlighted in yellow. Two text boxes with arrows annotate the code. An arrow points from the right text box to the grayed parameter `???? pred` in the function signature. An arrow points from the bottom text box to the highlighted `(pred(*it))` condition.*

```cpp
template <typename It>
It find(It first, It last, ???? pred) {
    for (auto it = first; it != last; ++it) {
        if (pred(*it)) return it;
    }
    return last;
}
```

*Annotation (right):* What if we could instead pass a predicate to this function as a parameter?

*Annotation (bottom):* Then we could replace this critical section of the code with a call to our predicate... like so!

---

## Slide 39: Modifying our find function

*Figure: A diagram showing a code snippet for a modified `find` function, with three annotation boxes pointing to different parts of the code.*

```cpp
template <typename It>
It find(It first, It last, ???? pred) {
    for (auto it = first; it != last; ++it) {
        if (pred(*it)) return it;
    }
    return last;
}
```

*An annotation box points to the `????` placeholder in the function signature, with the text: "Wait... what's the type of this predicate?"*

*An annotation box points to the line `if (pred(*it)) return it;`, with the text: "Then we could replace this critical section of the code with a call to our predicate... like so!"*

*An annotation box points generally to the function signature, with the text: "What if we could instead pass a predicate to this function as a parameter?"*

---

## Slide 40: Answer: Templates plus predicates

```cpp
template <typename It, typename Pred>
It find(It first, It last, Pred pred) {
    for (auto it = first; it != last; ++it) {
        if (pred(*it)) return it;
    }
    return last;
}
```

*Figure: A code box containing the C++ template function `find`. Three annotations in callout boxes point to specific parts of the code.*

*Figure: The first annotation points to the highlighted `typename Pred` in the template parameter list. The callout box text is:*
```
Pred: the type of our predicate.
Compiler will figure this out for us using implicit instantiation!
```

*Figure: The second annotation points to the highlighted `Pred pred` in the function parameter list. The callout box text is:*
```
pred: our predicate, passed as a parameter
```

*Figure: The third annotation points to the highlighted `pred(*it)` inside the `if` condition. The callout box text is:*
```
Hey look! We’re calling our predicate on each element. As soon as we find one that matches, we return
```

---

## Slide 41: Templates plus predicates

```cpp
template <typename It, typename Pred>
It find_if(It first, It last, Pred pred) {
  for (auto it = first; it != last; ++it) {
    if (pred(*it)) return it;
  }
  return last;
}
```

*Figure: A code snippet for a `find_if` function template is shown in a box. Several annotations with black arrows point from explanatory text boxes to specific parts of the code.*

**Annotations pointing to the code:**

*   An arrow from a box pointing to the `Pred` template parameter contains the text:
    **Pred: the type of our predicate.**
    **Compiler will figure this out for us using implicit instantiation!**

*   An arrow from a box pointing to the `pred` function parameter contains the text:
    **pred: our predicate, passed as a parameter**

*   An arrow from a box pointing to the line `if (pred(*it)) return it;` contains the text:
    **Hey look! We're calling our predicate on each element. As soon as we find one that matches, we return**

*   An arrow from a box pointing to the function name `find_if` contains the text:
    **Let's give this function a new name so it doesn't get confused with old one!**

---

## Slide 42: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup, looking thoughtfully at the viewer with his hand resting on his chin. In the background, there are posters on the wall, one of which prominently displays the text "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". The image is centered on the slide.*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 43: Using our find_if function

```cpp
bool isVowel(char c) {
    c = toupper(c);
    return c == 'A' || c == 'E' || c == 'I' ||
           c == 'O' || c == 'U';
}

std::string flower = "rose";
auto it = find_if(flower.begin(), flower.end(), isVowel);
*it = 'i'; // "rise"
```

*Figure: A dialogue box with a drop shadow to the right of the code contains the following text:*
> You: "What type is this?"
> Compiler: "Don't worry about it!"

*A black arrow points from the dialogue box down to the `isVowel` argument in the `find_if` call, which is highlighted in yellow.*

---

## Slide 44: Using our find_if function

```cpp
bool isGood(Trail t) { // Would I Approve?
   return t.hasWaterfall();
}

std::vector<Trail> trails = getNearbyTrails();
auto it = find_if(trails.begin(), trails.end(),  isGood);
assert(it->hasWaterfall() == true);
```

*Figure: A speech bubble annotation pointing to the `isGood` identifier (highlighted in yellow) in the `find_if` call. The speech bubble reads: **You:** "What type is this!!?" **Compiler:** "I gottttchuuu man". This illustrates how the compiler uses type inference (template argument deduction) to deduce that `isGood` is a function pointer, and uses the parameter types to determine the iterator and predicate types for `find_if`.*

---

## Slide 45: Generalizing Algorithms with Functions
Passing functions allows us to **generalize** an algorithm with **user-defined behaviour**

---

## Slide 46: Aside: Seriously though, what is the type of `Pred`?

---

## Slide 47: Pred is a function pointer

**Pred** is a function pointer

```cpp
find_if(flower.begin(), flower.end(), isVowel);
// Pred = bool(*)(char)

find_if(t.begin(), t.end(), isGood);
// Pred = bool(*)(Trail)
```

*Figure: A diagram with three annotation boxes below the code block, each connected to the second comment line by a black arrow. The leftmost box says "My function returns a bool" and points to the word `bool`. The middle box says "I'm a function pointer" and points to `(*)`. The rightmost box says "And I take in a single Trail as a parameter" and points to `Trail`.*

As we’ll see shortly, a function pointer is ***just one*** of the types we can pass to `find_if`

---

## Slide 48: Get some practice with function pointers!

Code is here:
online-ide.com/2mwjsthYoN

Links on this slide:
- <http://www.online-ide.com/2mwjsthYoN>

---

## Slide 49: Function pointers generalize poorly

Consider that we want to find a number less than **N** in a vector

```cpp
bool lessThan5(int x) { return x < 5; }
bool lessThan6(int x) { return x < 6; }
bool lessThan7(int x) { return x < 7; }

find_if(begin, end, lessThan5);
find_if(begin, end, lessThan6);
find_if(begin, end, lessThan7);
```

---

## Slide 50: Function pointers generalize poorly

```cpp
int n;
std::cin >> n;
find_if(begin, end, /* lessThan... Haelpp... */)
```

*Figure: A speech bubble (callout) containing the text "What if we want to find a number less than N, but we don’t know what N is until runtime?" is positioned above the code, with an arrow pointing from the line `std::cin >> n;` to the speech bubble.*

---

## Slide 51: We can't just add another parameter

Turn to someone next to you and talk about why this wouldn't work!

*Figure: A code snippet displayed within a white rectangular box with a drop shadow.*

```cpp
bool isLessThan(int elem, int n) {
    return elem < n;
}
```

---

## Slide 52: We can't add another parameter to pred!

*Figure: A code snippet enclosed in a rectangular box, with a callout box containing the text "We only pass one parameter to pred here!" and an arrow pointing from the callout to the line `if (pred(*it)) return it;` within the code.*

```cpp
template <typename It, typename Pred>
It find_if(It first, It last, Pred pred) {
    for (auto it = first; it != last; ++it) {
        if (pred(*it)) return it;
    }
    return last;
}
```

---

## Slide 53: Function State without Parameters

We want to give our function extra state...
...without introducing another parameter

*Figure: A background image showing a dirt path leading through a lush, green forest with sunlight filtering through the trees.*

---

## Slide 54: Introducing… lambda functions

Lambda functions are functions that capture state from an enclosing scope.

```cpp
int n;
std::cin >> n;

auto lessThanN = [n](int x) { return x < n; };

find_if(begin, end, lessThanN); //
```

*Figure: The code shows a lambda function `lessThanN` that captures the variable `n` from the enclosing scope and checks if a given integer `x` is less than `n`. This lambda is then used with the `find_if` algorithm. There are two cool emoji faces at the end of the code line.*

---

## Slide 55: Lambda Syntax

*Figure: A diagram illustrating the syntax of a C++ lambda expression. An example code snippet is shown with four annotation boxes connected by arrows to the relevant parts of the code.*

```cpp
auto lessThanN = [n] (int x) {
    return x < n;
};
```

- An annotation box points to the `auto` keyword: "I don't know the type! But the compiler does."
- An annotation box points to the capture clause `[n]`: **Capture clause** — lets us use outside variables
- An annotation box points to the parameter list `(int x)`: **Parameters** — Function parameters, exactly like a normal function
- An annotation box points to the function body `{ return x < n; }`: **Function body** — Exactly as a normal function, except only parameters and captures are in-scope

---

## Slide 56: A note on captures

*Figure: A code box containing C++ lambda syntax and examples of capture lists, with explanatory comments.*

```cpp
auto lambda = [capture-values](arguments) {
    return expression;
}

[x](arguments)        // captures x by value (makes a copy)
[x&](arguments)       // captures x by reference
[x, y](arguments)     // captures x, y by value
[&](arguments)        // captures everything by reference
[&, x](arguments)     // captures everything except x by reference
[=](arguments)        // captures everything by value
```

---

## Slide 57: We don’t have to use captures!

Lambdas are good for making functions on the fly

```cpp
std::vector<Trail> trails = {
    {"3 miles", false},
    {"5 miles", true},
    {"2 miles", false},
    {"8 miles", true}
};

auto it = find_if(trails, [](const auto& t) {
    return t.hasWaterfall();
});
```

*Figure: A humorous image of a waterfall with a green figure (resembling a moss-covered swamp creature or person) in front of it. A red arrow points from the line `{"5 miles", true},` in the code block directly to this image.*

---

## Slide 58: We don't have to use captures!
Lambdas are good for making functions on the fly

```cpp
std::vector<Trail> trails = {
    {"3 miles", false},
    {"5 miles", true},
    {"2 miles", false},
    {"8 miles", true}
};

auto it = find_if(trails, [](const auto& t) {
    return t.hasWaterfall();
});
```

*Figure: A meme featuring Kermit the Frog. A red arrow points from the meme to the empty capture list `[]` in the lambda expression, highlighting that the lambda does not need to capture any variables to perform its task.*

---

## Slide 59: auto parameters are shorthand for templates

`auto` **parameters are shorthand for templates**

```cpp
auto lessThanN = [n](auto x) {
    return x < n;
};
```

*Figure: A large red arrow points downward from the first code box to the second, indicating a transformation or equivalence.*

```cpp
template <typename T>
auto lessThanN = [n](T x) {
    return x < n;
};
```

This is true wherever you see an `auto` parameter, not just in lambda functions!

Uses **implicit instantiation**!
Compiler figures out types when function is called

---

## Slide 60: Get some practice with lambdas!
Code is here:
online-ide.com/Zgnickm1lI

Links on this slide:
- <https://www.online-ide.com/Zgnickm1lI>

---

## Slide 61: What questions do you have?
*Figure: A photograph of Bjarne Stroustrup, the creator of C++. He is wearing a patterned shirt and glasses, with his hand resting under his chin in a thinking pose. The image is centered and has the caption "bjarne_about_to_raise_hand" printed directly below it. Overlaid on top of the image in large, bold, black font is the text "What questions do you have?".*

**bjarne_about_to_raise_hand**

---

## Slide 62: How do lambdas work?

*Figure: A photograph of a dirt or gravel path winding through a dense forest. Tall trees with green foliage line both sides of the path. The image is slightly desaturated, and the title text is overlaid in the center.*

---

## Slide 63: Recall: The Standard Template Library (STL)

*Figure: A diagram illustrating the four main components of the Standard Template Library (STL) arranged in a 2x2 grid within a large light-orange rounded rectangle. The boxes for 'Containers', 'Iterators', and 'Algorithms' have a grey background, while the 'Functors' box is highlighted in blue.*

*   **Containers**
    *   `How do we store groups of things?`
*   **Iterators**
    *   `How do we traverse containers?`
*   **Functors**
    *   `How can we represent functions as objects?`
*   **Algorithms**
    *   `How do we transform and modify containers in a generic way?`

---

## Slide 64: Definition:
**Definition:** A functor is any object that defines an `operator()`

*In English: an object that acts like a function*

---

## Slide 65: An example of a functor: std::greater\<T\>

```cpp
template <typename T>
struct std::greater {
    bool operator()(const T& a, const T& b) const {
        return a > b;
    }
};
```

`std::greater<int> g;`
`g(1, 2); // false`

*Figure: A diagram illustrating the definition and usage of the `std::greater` functor. The code definition is enclosed in a rectangular frame. Below the frame, a line of code instantiating the functor and calling it is shown. A speech bubble with a black arrow points to the call `g(1, 2); // false`. Inside the bubble, the text reads "Hmm.. Seems like a function" followed by two rubber duck icons.*

---

## Slide 66: Another STL functor: std::hash<T>

*Figure: A code snippet showing a template specialization for `std::hash<MyType>`, with two annotated text boxes. An "Aside" box points to the `struct` definition line. A "Hint hint" box is in the lower right.*

```cpp
template <>
struct std::hash<MyType> {
    size_t operator()(const MyType& v) const {
        // Crazy, theoretically rigorous hash function
        // approved by 7 PhDs and Donald Knuth goes here
        return ...;
    }
};

MyType m; std::hash<MyType>
hash_fn;
hash_fn(m); // 125123201 (for example)
```

*Figure: An "Aside" text box with a black arrow pointing to the line `struct std::hash<MyType> {` in the code. The text reads: "Aside: This syntax is called a template specialization for type MyType".*

*Figure: A "Hint hint" text box in the lower right corner. The text reads: "Hint hint: This is also one of the ways to create a hash function for a custom type".*

---

## Slide 67: Functor State

Since a functor is an **object**, it can have **state**

*Figure: A single sentence of text centered on a white background. The words "object" and "state" are highlighted in a red color for emphasis, while the rest of the sentence is in black.*

---

## Slide 68: Functors can have state!

```cpp
struct my_functor {
    int operator()(int a) const {
        return a * value;
    }

    int value;
};

my_functor f;
f.value = 5;
f(10); // 50
```

---

## Slide 69: Time for a dark secret

Time for a dark secret

*Figure: A meme featuring a man with a mischievous smirk looking sideways. Large white text at the top reads "SHHHHH" and large white text at the bottom reads "IT'S A SECRET". A small watermark "memegenerator.net" is visible in the bottom right corner.*

---

## Slide 70: Lambda and Functor Relationship

**When you use a lambda, a functor type is generated**

---

## Slide 71: This code...

*Figure: A simple rectangular box with a thin black outline containing a C++ code snippet.*

```cpp
int n = 10;
auto lessThanN = [n](int x) { return x < n; };
find_if(begin, end, lessThanN);
```

---

## Slide 72: ...is equivalent to this code!

*Figure: A diagram showing a class implementation that a lambda expression compiles down to, with four annotated callout boxes pointing to different parts of the code via arrows.*

```cpp
class __lambda_6_18
{
public:
    bool operator()(int x) const { return x < n; }
    __lambda_6_18(int& _n) : n{_n} {}
private:
    int n;
};

int n = 10;
auto lessThanN = __lambda_6_18{ n };
find_if(begin, end, lessThanN);
```

*Annotations:*
- An arrow points from a box labeled **"Random name that only the compiler will see!"** to the class name `__lambda_6_18`.
- An arrow points from a box labeled **"Recall: functor call operator"** to the line `bool operator()(int x) const { return x < n; }`.
- An arrow points from a box labeled **"Class constructor"** to the line `__lambda_6_18(int& _n) : n{_n} {}`.
- An arrow points from a box labeled **"Our captures became fields in the class!"** to the member declaration `int n;`.
- An arrow points from a box labeled **"Capturing variable n from outer scope by passing to constructor"** to the highlighted instantiation line `auto lessThanN = __lambda_6_18{ n };`.

If you are curious about this stuff, check out https://cppinsights.io/!

Links on this slide:
- <https://cppinsights.io/>

---

## Slide 73: You’ve seen this kind of thing before…

```cpp
std::vector<int> v {1,2,3};
for (const int& e : v)
{
    // ...
}
```

*Figure: A large, thick red arrow pointing from the left code block to the right code block.*

```cpp
auto begin = v.begin();
auto end = v.end();
for (auto it = begin; it != end; ++it)
{
    // ...
}
```

---

## Slide 74: It's the same ordeal! Syntactic sugar

*Figure: Two code blocks are displayed side-by-side. A large red arrow points from the left block to the right block, indicating that the code on the left is equivalent to the code on the right.*

**Left Block:**
```cpp
int n = 10;
auto lessThanN = [n](int x)
{ return x < n; };
find_if(begin, end, lessThanN);
```

**Right Block:**
```cpp
class __lambda_6_18
{
public:
    bool operator()(int x) const
    { return x < n; }
    __lambda_6_18(int& _n) : n{_n}
    {}
private:
    int n;
};
int n = 10;
auto lessThanN = __lambda_6_18{n};
find_if(begin, end, lessThanN);
```

---

## Slide 75: Functions & Lambdas Recap

*   Use functions/lambdas to pass around **behaviour** as variables
*   Aside: `std::function` is an overarching type for functions/lambdas
    *   Any functor/lambda/function pointer can be cast to it
    *   It is a bit slower
    *   I usually use auto/templates and don’t worry about the types!

*Figure: A black-bordered rectangular box containing three lines of C++ code examples for `std::function`.*

```cpp
std::function<bool(int, int)> less = std::less<int>{};
std::function<bool(char)> vowel = isVowel;
std::function<int(int)> twice = [](int x) { return x * 2; };
```

---

## Slide 76: What questions do you have?

*Figure: A photograph of Bjarne Stroustrup in a patterned shirt, resting his chin on his hand as if about to raise it. In the background, a poster is partially visible reading "PROGRAMMING LANGUAGE" and "BJARNE STROUSTRUP". Large bold text overlays the image.*

**What questions do you have?**

bjarne_about_to_raise_hand

---

## Slide 77: Where do we use functions & lambdas?

*Figure: A background photograph showing a light-colored dirt path winding through a lush, green forest. Tall, thin trees with dense foliage line the path, and sunlight filters through the leafy canopy.*

**Where do we use functions & lambdas?**

---

## Slide 78: Algorithms

*Figure: A semi-transparent, bright background image of a forest scene. A light-colored dirt path curves gently from the lower right into the distance, flanked on both sides by tall, slender trees with green foliage. The trees and lush undergrowth create a dense, serene woodland atmosphere. The image has a hazy, sunlit quality, with the central title text appearing sharply over it.*

---

## Slide 79: Recall: The Standard Template Library (STL)

*Figure: A diagram with a rounded rectangle containing four component boxes arranged in a 2x2 grid. The top two boxes and the bottom-left box are gray, while the bottom-right box is highlighted in light blue.*

| | |
|---|---|
| **Containers** | **Iterators** |
| How do we store groups of things? | How do we traverse containers? |
| **Functors** | **Algorithms** |
| How can we represent functions as objects? | How do we transform and modify containers in a generic way? |

---

## Slide 80: Huh... that looks familiar

*Figure: A screenshot of a C++ documentation page for `std::find`, `std::find_if`, and `std::find_if_not`. A red rectangle highlights the third overload of the `find_if` function.*

### std::find, std::find\_if, std::find\_if\_not

Defined in header `<algorithm>`

```cpp
template< class InputIt, class T >
InputIt find( InputIt first, InputIt last, const T& value );    (constexpr since C++20)
                                                               (1) (until C++26)

template< class InputIt, class T = typename std::iterator_traits<InputIt>::value_type >
constexpr InputIt find( InputIt first, InputIt last, const T& value );    (since C++26)

template< class ExecutionPolicy, class ForwardIt, class T >
ForwardIt find( ExecutionPolicy&& policy,
                ForwardIt first, ForwardIt last, const T& value );    (since C++17)
                                                                      (2) (until C++26)

template< class ExecutionPolicy,
          class ForwardIt, class T = typename std::iterator_traits<ForwardIt>::value_type >
ForwardIt find( ExecutionPolicy&& policy,
                ForwardIt first, ForwardIt last, const T& value );    (since C++26)

template< class InputIt, class UnaryPred >
InputIt find_if( InputIt first, InputIt last, UnaryPred p );        (3) (constexpr since C++20)

template< class ExecutionPolicy, class ForwardIt, class UnaryPred >
ForwardIt find_if( ExecutionPolicy&& policy,
                   ForwardIt first, ForwardIt last, UnaryPred p );  (4) (since C++17)
```

---

## Slide 81: \<algorithm> is a collection of template functions

```cpp
std::count_if(InputIt first, InputIt last, UnaryPred p);
```
How many elements in [first, last) match predicate p?

```cpp
std::sort(RandomIt first, RandomIt last, Compare comp);
```
Sorts the elements in [first, last) according to comparison comp

```cpp
std::max_element(ForwardIt first, ForwardIt last, Compare comp);
```
Finds the maximum element in [first, last) according to comparison comp

---

## Slide 82: <algorithm> functions operate on iterators

`std::copy_if(InputIt r1, InputIt r2, OutputIt o, UnaryPred p);`
Copy the only elements in [r1, r2) into o that match predicate p

`std::transform(InputIt r1, InputIt r2, OutputIt o, UnaryOp op);`
Apply op to each element in [r1, r2), writing a new sequence into o

`std::unique_copy(InputIt i1, InputIt i2, OutputIt o, BinaryPred p);`
Remove consecutive duplicates from [r1, r2), writing new sequence into o

---

## Slide 83: There are a lot of algorithms...

| | | | | |
|---|---|---|---|---|
| all_of | copy | merge | random_shuffle | is_sorted |
| any_of | copy_n | inplace_merge | shuffle | is_sorted_until |
| none_of | copy_if | includes | push_heap | nth_element |
| for_each | copy_backward | set_union | pop_heap | min |
| find | move | set_intersection | make_heap | max |
| find_if | move_backward | set_difference | sort_heap | minmax |
| find_if_not | swap | set_symmetric_difference | is_heap | min_element |
| find_end | swap_ranges | remove | is_heap_until | max_element |
| find_first_of | iter_swap | remove_copy | is_partitioned | minmax_element |
| adjacent_find | transform | remove_copy_if | partition | lexicographical_compare |
| count | replace | unique | stable_partition | next_permutation |
| count_if | replace_if | unique_copy | partition_copy | prev_permutation |
| mismatch | replace_copy | reverse | partition_point | |
| equal | replace_copy_if | reverse_copy | sort | |
| is_permutation | fill | rotate | stable_sort | |
| search | fill_n | rotate_copy | partial_sort | |
| search_n | generate | rotate_copy | partial_sort_copy | |

---

## Slide 84: Things you can do with the STL

**Things you can do with the STL**

binary search • heap building • min/max
lexicographical comparisons • merge • set union
• set difference • set intersection • partition • sort
*n*th sorted element • shuffle • selective removal •
selective copy • for-each • random sample

*all in their most general form!*

---

## Slide 85: What questions do you have?

*Figure: A photo of Bjarne Stroustrup wearing glasses and a patterned shirt, with his hand near his chin. In the background, there is a poster that says "C++ PROGRAMMING LANGUAGE BJARNE STROUSTRUP".*

What questions do you have?

bjarne_about_to_raise_hand

---

## Slide 86: <algorithm> lets us inspect and transform data

*Figure: A collage of diagrams and images illustrating the use of the `<algorithm>` header for inspecting and transforming data. The slide features a book cover, network protocol diagrams, container visualizations, a Huffman coding example, a compiler analysis diagram, and text boxes with information.*

*Book Cover: An image of the book "Biological Sequence Analysis Using the SeqAn C++ Library" by Chapman & Hall/CRC (Mathematical and Computational Biology Series). Below the cover is a price tag: $457.92. Underneath that is a "You Earn: 200 pts" note with a "Learn more" link, delivery information ("$3.99 delivery September 30 - October 4. Details"), and details about a points offer.*

*TCP Communication Diagram: A diagram showing a TCP data exchange between a 'Client' (green box) and a 'Server' (green box). The client sends TCP packets with sequence numbers (Seq#) and lengths (Len), and the server responds with acknowledgment numbers (Ack#). The sequence is:*
- *Client: TCP Seq# = 1, Len = 669*
- *Server: TCP Ack# = 670*
- *Client: TCP Seq# = 670, Len = 1460*
- *Server: TCP Ack# = 2130*
- *Client: TCP Seq# = 2130, Len = 1460*
- *Server: TCP Ack# = 3590*
- *A note below says: "Continues until TCP close".*

*Container Content and Tree Structure: Two figures side-by-side. The left figure shows three containers labeled A, B, and C, each holding a spiral, a cube, and a star, respectively. The right figure shows a tree structure with nodes labeled A, B, and C. Node A is the root, with children B and C. Node B has children that are the spiral and the cube. Node C has children that are the star and a triangle.*

*Huffman Coding: A diagram titled "Huffman Coding". It gives an example for the string "COMPRESSION_IS_COOL". The instruction is: "To compute the bit pattern for each datum, we go up the tree and write down a '1' (true) if we take the branch to the left, and a '0' (false) if we take the branch to the right, respectively." Below this is a partial table showing:*
- *_: 0000*
- *C: 0001*
- *(The table is cut off, but below it are letters with frequencies: C:2, R:2, E:1, M:1, P:1, N:1, L:1, and others.)*

*LLVM Information: A text box with the question "In what language is LLVM written?". The answer below states: "All of the LLVM tools and libraries are written in C++ with extensive use of the STL."*

*Compiler Analysis Diagram: A flow diagram showing the stages of a compiler: "Lexical Analysis" → "Syntax Analysis" → "Semantic Analysis". This part of the diagram is partially obscured by the LLVM text box.*

*Timeline: A small timeline at the bottom with markers and letters (e.g., C, R, E, M, P, N, L) above numbers (e.g., 2, 2, 1, 1, 1, 1, 1), likely representing character frequencies for Huffman coding.*

---

## Slide 87: Let’s write an algorithm using the STL!

---

## Slide 88: How can we make a tokenizer?

*Figure: A photograph of a dirt path winding through a dense, green forest. Tall, thin trees line both sides of the path, creating a canopy overhead. The overall tone is soft and slightly faded. Centered over the image is the bold, black text "How can we make a tokenizer?".*

---

## Slide 89: Breaking down the problem

**"Breaking down the string"**

*Figure: A diagram illustrating the process of breaking a sentence into words. The top text, "Breaking down the string", has a downward arrow pointing to the resulting set below: {"Breaking", "down", "the", "string"}.*

---

## Slide 90: Breaking down the problem

“Breaking down the string”

{“Breaking”, “down”, “the”, “string”}

*Figure: Three thick, dark blue diagonal lines connect the words in the original string “Breaking down the string” to their corresponding elements in the set below. The lines originate from the spaces between words and point down to the commas separating the elements in the set.*

---

## Slide 91: Breaking down the problem

*Figure: A diagram titled "Breaking down the problem". It illustrates the breakdown of the string "Breaking down the string". The sequence of digits 01234567 is shown under the first word. Three blue vertical bars mark specific positions in the string, with the numbers 8, 13, and 17 printed below each bar. Ellipses follow each bar, indicating the continuation of the string.*

---

## Slide 92: Breaking down the problem

"Breaking down the string"

*Figure: A diagram showing the string "Breaking down the string" with blue vertical lines pointing down from specific characters to position indices below: the first character (the opening double-quote) points to index 0, the 'd' in "down" points to index 8, the 't' in "the" points to index 13, the 's' in "string" points to index 17, and the closing double-quote points to the end() iterator position.*

0
8
13
17
end()

---

## Slide 93: Breaking down the problem

*Figure: A string literal "Breaking down the string" shown with five blue vertical bars marking split points. Below each bar is a label: 0, 8, 13, 17, and end(). The bars are positioned at the start of the string, after the words "Breaking", "down", and "the", and at the end of the string.*

| Substring | Range |
| :--- | :--- |
| `"Breaking"` | `[0, 8)` |
| `" down"` | `[8, 13)` |
| `" the"` | `[13, 17)` |
| `" string"` | `[17, end)` |

---

## Slide 94: Breaking down the problem

“Breaking down the string”

*Figure: A diagram showing the string "Breaking down the string" with vertical blue bars marking the positions of indices 0, 8, 13, 17, and end(). A red arrow points to the index 0. A blue arrow points to the index 8. A red arrow points down towards the space before the word "down". A blue arrow points down towards the space before the word "the". Below the diagram, a list shows the substrings and their corresponding half-open index ranges:*
*   "Breaking"   [0, 8)
*   " down"      [8, 13)
*   " the"       [13, 17)
*   " string"    [17, end)

---

## Slide 95: Breaking down the problem

```
“Breaking down the string”
```
*Figure: A diagram showing the string “Breaking down the string” with vertical blue bars marking index positions. Below the bars are the numbers 0, 8, 13, 17, and end(). Red and blue arrows point from the spaces between words to the index numbers and ranges.*

```
0       8       13   17       end()
```

Below the string, the words are listed with their corresponding index ranges. Red and blue arrows connect the words to the start and end indices in the ranges.

```
“Breaking”   [0, 8)
“ down”      [8, 13)
“ the”       [13, 17)
“ string”    [17, end)
```

---

## Slide 96: Breaking down the problem
"Breaking down the string"

*Figure: A diagram showing the indexing of the string "Breaking down the string". Vertical blue bars mark indices 0, 8, 13, 17, and end(). A red arrow points upward to the marker at index 13, and a blue arrow points upward to the marker at index 17. Below the diagram, a red arrow points downward toward the starting index of the range `[8, 13)`, and a blue arrow points downward toward the starting index of the range `[13, 17)`.*

"Breaking" [0, 8)
" down" [8, 13)
" the" [13, 17)
" string" [17, end)

---

## Slide 97: Breaking down the problem

“Breaking down the string”

*Figure: A diagram illustrating the decomposition of the string "Breaking down the string" into four substrings using index ranges. The string is shown at the top with vertical blue bars at positions 0, 8, 13, 17, and a final label end(). Below the string, the substrings and their corresponding half-open intervals are listed. Red arrows point from the ranges to the index labels 13 and 17 above, and blue arrows point from the last range to the label end() above.*

“Breaking”   [0, 8)
“ down”      [8, 13)
“ the”       [13, 17)
“ string”    [17, end)

---

## Slide 98: Breaking down the problem

"Breaking down the string"

*Figure: A diagram illustrating string slicing. At the top, the string "Breaking down the string" is shown with blue vertical markers above specific character indices: 0, 8, 13, 17, and end(). A red horizontal arrow spans from index 0 to 17. A blue horizontal arrow spans from index 8 to end(). Below the diagram, the string is decomposed into four substrings with their corresponding index ranges: "Breaking" corresponds to [0, 8), " down" to [8, 13), " the" to [13, 17), and " string" to [17, end). A red vertical arrow points downward alongside the list of ranges, and a blue diagonal arrow points from the range [0, 8) toward the range [17, end).*

| Substring | Range |
| :--- | :--- |
| "Breaking" | [0, 8) |
| " down" | [8, 13) |
| " the" | [13, 17) |
| " string" | [17, end) |

---

## Slide 99: Breaking down the problem

**Breaking down the problem**

`"Breaking down the string"`

*Figure: A diagram showing the string "Breaking down the string" in monospace font. Five vertical blue bars are positioned at specific character indices below the string. From left to right, the bars are labeled: `0` (at the start of the string), `8` (at the space between "Breaking" and "down"), `13` (at the space between "down" and "the"), `17` (at the space between "the" and "string"), and `end()` (after the closing double-quote).*

Steps:
1. Get indices (iterators)
2. Loop over with 2 iterators,
   making tokens

---

## Slide 100: Step 1) Getting indices v1

*Figure: A code snippet displayed in a dark-themed code editor with syntax highlighting. The code is written in C++ and shows logic to collect iterators of spaces from a string.*

```cpp
// Get all indeces we want.
std::set<std::string::iterator> spaces {source.begin(), source.end()};
for (auto cur = source.begin(); cur != source.end(); ++cur) {
  if (*cur == ' ') {
    spaces.insert(cur);
  }
}
```

We're handling too much logic
ourselves...

---

## Slide 101: Step 1) Getting indices v2

```cpp
// Get all indeces we want.
std::set<std::string::iterator> spaces {source.begin(), source.end()};
for (auto cur = source.begin(); cur != source.end(); ++cur) {
    if (std::isspace(*cur)){
        spaces.insert(cur);
    }
}
```

If we use a predicate function...

...then this looks like a **filter**,
**find_if**, & **find_all**.

---

## Slide 102: Step 1) Getting indices v3

```cpp
template <typename Iterator, typename UnaryPred>
std::vector<Iterator> find_all(Iterator begin, Iterator end, UnaryPred pred) {
    std::vector<Iterator> its{begin};
    for (auto it = begin; it != end; ++it) {
        if (pred(*it))
            its.push_back(it);
    }
    its.push_back(end);
    return its;
}
```

---

## Slide 103: Step 1) Getting indices v3

`std::vector<It> find_all(It begin, It end, Pred p)`

*Figure: A diagram shows the function signature. Arrows point from the label "source" to the `It begin` and `It end` parameters. An arrow points from the label "std::isspace" to the `Pred p` parameter.*

```cpp
template <typename Iterator, typename UnaryPred>
std::vector<Iterator> find_all(Iterator begin, Iterator end, UnaryPred pred) {
    std::vector<Iterator> its{begin};
    for (auto it = begin; it != end; ++it) {
        if (pred(*it))
            its.push_back(it);
    }
    its.push_back(end);
    return its;
}
```

---

## Slide 104: Step 2) Using indices to get tokens (bad)

```cpp
// Double iterator loop to get tokens.
Corpus tokens;
auto first = spaces.begin();
auto second = std::next(first);
for (; second != spaces.end(); ++first, ++second) {
  auto start_char = *first;
  auto end_char = *second;
  tokens.insert({source, start_char, end_char});
}
```

---

## Slide 105: Step 2) Using indices to get tokens

### Breaking down the problem

*Figure: A diagram illustrating string tokenization using indices. At the top, the string `"Breaking down the string"` is shown with vertical line markers at indices 0, 8, 13, 17, and `end()`. Red boxes surround the markers at index 0 and `end()`. A blue box surrounds the marker at index 8. A red arrow points from index 0 to 17, and a blue arrow points from index 8 to `end()`. To the left of the markers is the text `Spaces: {` and to the right is `}`, with a blue arrow pointing from the label `spaces.end()` toward the closing brace.*

Below this, a mapping is shown between tokens and their index ranges:
*   `"Breaking"` : `[0, 8)`
*   `" down"` : `[8, 13)`
*   `" the"` : `[13, 17)`
*   `" string"` : `[17, end)`

A red arrow points downward next to the tokens, and a blue arrow points downward next to the index ranges.

*Figure: A C++ code snippet at the bottom shows the declaration of the `std::transform` function. Red boxes surround the parameters `InputIt1 first1` and `InputIt1 last1`. A blue box surrounds the parameter `InputIt2 first2`.*

```cpp
template< class InputIt1, class InputIt2,
          class OutputIt, class BinaryOp >
OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                    OutputIt d_first, BinaryOp binary_op );
```

---

## Slide 106: Step 2) Using indices to get tokens

### Breaking down the problem

"Breaking down the string"

| Index | 0 | 8 | 13 | 17 | end() |
|-------|---|---|---|----|-------|

*Figure: A diagram of the string "Breaking down the string". Vertical blue lines mark positions at 0, 8, 13, 17, and end(). A red arrow points from index 0 to index 8. A blue arrow points from index 8 to index 13. A green curved arrow points from index 13 to index 17. A purple box encloses a list of intervals: `[0, 8)`, `[8, 13)`, `[13, 17)`, `[17, end)`. A red arrow points down through this list. A blue arrow points from the interval `[0, 8)` to a list of tokens.*

*Figure: A list of tokens derived from the string, shown as: `{"Breaking"`, ` " down"`, ` " the"`, ` " string"}`. An orange arrow points from the first token `"Breaking"` towards the string diagram.*

```cpp
template< class InputIt1, class InputIt2,
          class OutputIt, class BinaryOp >
OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                    OutputIt d_first, BinaryOp binary_op );
```

---

## Slide 107: Step 2) Using indices to get tokens

```cpp
template< class InputIt1, class InputIt2,
          class OutputIt, class BinaryOp >
OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                   OutputIt d_first, BinaryOp binary_op );
```

```cpp
first1    = spaces.begin()
last1     = ????? 
first2    = ????? 
d_first   = std::inserter(tokens, tokens.end())
binary_op = ????? 
```

---

## Slide 108: Step 2) Using indices to get tokens

```cpp
template< class InputIt1, class InputIt2,
          class OutputIt, class BinaryOp >
OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                    OutputIt d_first, BinaryOp binary_op );
```

```cpp
first1    = spaces.begin()
last1     = spaces.end() - 1
first2    = spaces.begin() + 1
d_first   = std::inserter(tokens, tokens.end())
binary_op = "a lambda with 2 iterators as input
and a token as output"
```

---

## Slide 109: Step 2) Using indices to get tokens

```cpp
template< class InputIt1, class InputIt2,
          class OutputIt, class BinaryOp >
OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
                    OutputIt d_first, BinaryOp binary_op );
```

```cpp
first1    = spaces.begin()
last1     = spaces.end() - 1
first2    = spaces.begin() + 1
d_first   = std::inserter(tokens, tokens.end())
binary_op = [&](auto it1, auto it2) {
                return Token(source, it1, it2);
            }
```

---

## Slide 110: Step 3) Are we done?

"N'ot a!!    Str1ngs 4re    nice :/"

{"N'ot", "a!!", "", "Str1ngs" "4re", "", "nice", ":/"}

*Figure: A diagram illustrating a step in a string processing algorithm. The top part shows the input string `"N'ot a!!    Str1ngs 4re    nice :/"` with several vertical blue bars positioned in the spaces between words. Specifically, there is one bar after `"a!!"`, two bars after `"Str1ngs"`, two bars after `"4re"`, and one bar after `"nice"`. Below this, the resulting set of tokens is shown: `{"N'ot", "a!!", "", "Str1ngs" "4re", "", "nice", ":/"}`. Two of the empty string tokens `""` are highlighted with red circles, suggesting they are problematic or noteworthy results of the process.*

---

## Slide 111: Step 3) Erase spaces

**std::erase_if (std::set)**

Defined in header `<set>`

```cpp
template< class Key, class Compare, class Alloc,
          class Pred >
std::set<Key, Compare, Alloc>::size_type
    erase_if( std::set<Key, Compare, Alloc>& c,
              Pred pred );
```

*(since C++20)*

Erases all elements that satisfy the predicate `pred` from `c`.

Equivalent to

```cpp
auto old_size = c.size();
for (auto first = c.begin(), last = c.end(); first != last;)
{
    if (pred(*first))
        first = c.erase(first);
    else
        ++first;
}
return old_size - c.size();
```

### Parameters

- c - container from which to erase
- pred - predicate that returns `true` if the element should be erased

### Return value

The number of erased elements.

### Complexity

Linear.

container:
- tokens

pred:
- whether a token is empty

---

## Slide 112: ) Erase spaces

**std::erase_if (std::set)**

Defined in header `<set>`

```cpp
template< class Key, class Compare, class Alloc,
          class Pred >
std::set<Key, Compare, Alloc>::size_type
    erase_if( std::set<Key, Compare, Alloc>& c,
              Pred pred );
```

*(since C++20)*

Erases all elements that satisfy the predicate `pred` from `c`.

Equivalent to

```cpp
auto old_size = c.size();
for (auto first = c.begin(), last = c.end(); first != last;)
{
    if (pred(*first))
        first = c.erase(first);
    else
        ++first;
}
return old_size - c.size();
```

**Parameters**

`c` &nbsp; - &nbsp; container from which to erase
`pred` &nbsp; - &nbsp; predicate that returns `true` if the element should be erased

**Return value**

The number of erased elements.

**Complexity**

Linear.

*c:*

```cpp
tokens
```

*pred:*

```cpp
[](const auto& t) {
    return t.content.empty();
}
```

---

## Slide 113: Tokenizer

**Strategy:**

1. Work through example
2. Figure out the logic
3. See if the logic follows a common algorithm
    a. If so, use the std algorithm library for clarity and accuracy

1. We found:
    b. We need to get all the spaces (+ begin & end)
        i. The staff gave us a **find_all** function :)
    c. We need to convert our spaces into tokens
        i. The std gives us a **transform** for that
    d. We need to get rid of empty tokens
        i. The std gives us a **erase_if** for that

---

## Slide 114: Ranges and Views

*Figure: A background image of a dirt path winding through a dense forest with green foliage and numerous trees. The title "Ranges and Views" is superimposed in large, bold, black text across the center of the image.*

---

## Slide 115: Ranges are a new version of the STL

---

## Slide 116: Definition: A range is anything with a begin and end

**Definition:** A range is anything with a **begin** and **end**

---

## Slide 117: What’s a range?

*Figure: A diagram centered around the bold text "What’s a range?" with five red arrows pointing outward to rectangular boxes, each identifying a C++ type that functions as a range:*

*   `std::vector<T>`
*   `std::unordered_set<K,V>`
*   `std::map<K, V>`
*   `std::set<K>`
*   Your own custom type with a begin and end!

---

## Slide 118: Recall: why did we pass iterators to find?
It allows us to find in a subrange! But most of the time, we don’t need to.

```cpp
int main() {
    std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};
    auto it = std::find(v.begin(), v.end(), 'c');
}
```

*Figure: A code snippet showing a `std::vector` and a call to `std::find`. An arrow points from a comment bubble to the line containing the `std::find` call. The bubble contains the text: "Do we really care about iterators here? I just wanted to search the entire container!"*

---

## Slide 119: Range algorithms operate on ranges

STD ranges provides new versions of <algorithm> for ranges

```cpp
int main() {
    std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};
    auto it = std::ranges::find(v, 'c');
}
```

*Figure: A speech bubble with an arrow pointing to the variable `v` in the line `auto it = std::ranges::find(v, 'c');`. The bubble contains the text: "Look! I can pass v here because it is a range!"*

---

## Slide 120: Range algorithms operate on ranges
Range algorithms operate on **ranges**
We can still work with iterators if we need to

```cpp
int main() {
    std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};

    // Search from 'b' to 'd'
    auto first = v.begin() + 1;
    auto last = v.end() - 1;

    auto it = std::ranges::find(first, last, 'c');
}
```

---

## Slide 121: Ranges: The STL v2

- There are range equivalents of most of the STL `<algorithm>` library
- These are very new! **C++20/23/26** and beyond!

*Figure: Three bordered boxes arranged side-by-side, each listing a group of `ranges::` functions with their introduction version (e.g., C++20 or C++23) in parentheses.*

**Left Box:**

| Function | C++ Version |
|----------|-------------|
| ranges::find_last | (C++23) |
| ranges::find_last_if | (C++23) |
| ranges::find_last_if_not | (C++23) |
| ranges::find_end | (C++20) |
| ranges::find_first_of | (C++20) |
| ranges::adjacent_find | (C++20) |
| ranges::search | (C++20) |
| ranges::search_n | (C++20) |
| ranges::contains | (C++23) |
| ranges::contains_subrange | (C++23) |
| ranges::starts_with | (C++23) |
| ranges::ends_with | (C++23) |

**Middle Box:**

| Function | C++ Version |
|----------|-------------|
| ranges::copy | (C++20) |
| ranges::copy_if | (C++20) |
| ranges::copy_n | (C++20) |
| ranges::copy_backward | (C++20) |
| ranges::move | (C++20) |
| ranges::move_backward | (C++20) |
| ranges::fill | (C++20) |
| ranges::fill_n | (C++20) |
| ranges::transform | (C++20) |
| ranges::generate | (C++20) |
| ranges::generate_n | (C++20) |

**Right Box:**

| Function | C++ Version |
|----------|-------------|
| ranges::remove | (C++20) |
| ranges::remove_if | (C++20) |
| ranges::remove_copy | (C++20) |
| ranges::remove_copy_if | (C++20) |
| ranges::replace | (C++20) |
| ranges::replace_if | (C++20) |
| ranges::replace_copy | (C++20) |
| ranges::replace_copy_if | (C++20) |
| ranges::swap_ranges | (C++20) |
| ranges::reverse | (C++20) |
| ranges::reverse_copy | (C++20) |
| ranges::rotate | (C++20) |
| ranges::rotate_copy | (C++20) |
| ranges::shuffle | (C++20) |

---

## Slide 122: Range algorithms are constrained

That just means they make use of the new STL concepts! Remember them?

```cpp
template<class T>
concept range = requires(T& t) { ranges::begin(t); ranges::end(t); };
template<class T>
concept input_range =
    ranges::range<T> && std::input_iterator<ranges::iterator_t<T>>;
template<ranges::input_range R, class T, class Proj = std::identity>
borrowed_iterator_t<R> find( R&& r, const T& value, Proj proj = {} );
```

*Figure: A diagram showing three C++ code snippets with three callout annotations pointing to them. An arrow from the top annotation points to the `range` concept definition. A second arrow from the middle annotation points to the `input_range` concept definition. A third arrow from the bottom annotation points to the `find` function declaration.*

> A range has a begin and end! :)

> An input range is a range using an  
> input iterator

> I’ve cut out some of the code  
> here, but notice that ranges find  
> uses concepts!!

---

## Slide 123: Ranges Recap
- Ranges use concepts! Better error messages, what’s not to like?
- We can pass entire containers

---

## Slide 124: What questions do you have?

What questions do you have?

*Figure: A photograph of a person, identified by the caption as Bjarne Stroustrup, sitting at a desk. He is wearing glasses and a patterned short-sleeved shirt, with his right hand raised near his chin in a gesture as if he is about to ask a question. Behind him are computer monitors and a poster that reads "PROGRAMMING LANGUAGE BJARNE STROUSTRUP".*

bjarne_about_to_raise_hand

---

## Slide 125: Ranges Recap

*   Ranges use concepts! Better error messages, what’s not to like?
*   We can pass entire containers
*   Okay… is that it? 👀

---

## Slide 126: Views: a way to compose algorithms

---

## Slide 127: Definition of a View

**Definition:** A view is a range that *lazily* adapts another range

---

## Slide 128: Definition: A view is a range that lazily adapts another range

**Definition:** A view is a range that *lazily* adapts another range

*Figure: A central photograph of a snow-capped mountain peak is surrounded by various eye-themed graphics. On the left is a large pair of cartoon eyes with purple irises and long lashes. On the top right is a single, dark, spiked monster-like eye. On the bottom right is a yellow emoji face with a skeptical expression.*

---

## Slide 129: Filter and transform in the old STL
This code is a bit awkward in the current STL

*Figure: A code snippet contained within a light-colored rectangular box with a soft drop shadow against a white background.*

```cpp
std::vector<char> v = {'a', 'b', 'c', 'd', 'e'};

// Filter -- Get only the vowels
std::vector<char> f;
std::copy_if(v.begin(), v.end(), std::back_inserter(f), isVowel);

// Transform -- Convert to uppercase
std::vector<char> t;
std::transform(f.begin(), f.end(), std::back_inserter(t), toupper);

// { 'A', 'E' }
```

---

## Slide 130: Filter and transform with views!
A **view** is a range that lazily transforms its underlying range, one element at a time

*Figure: A code snippet enclosed in a rounded rectangular border demonstrating the use of `std::ranges::views::filter` and `std::ranges::views::transform`.*

```cpp
std::vector<char> letters = {'a', 'b', 'c', 'd', 'e'};

auto f = std::ranges::views::filter(letters, isVowel);
auto t = std::ranges::views::transform(f, toupper);

auto vowelUpper = std::ranges::to<std::vector<char>>(t);
```

---

## Slide 131: Views are composable

```cpp
auto f = std::ranges::views::filter(letters, isVowel);
// f is a view! It takes an underlying range letters
// and yields a new range with only vowels!

auto t = std::ranges::views::transform(f, toupper);
// t is a view! It takes an underlying range f
// and yields a new range with uppercase chars!

auto vowelUpper = std::ranges::to<std::vector<char>>(t);
// Here we materialize the view into a vector!
// Nothing actually happens until this line!
```

---

## Slide 132: We can chain views together use operator |

*Figure: A bordered code example demonstrating the chaining of views using the pipe operator in C++.*

```cpp
std::vector<char> letters = {'a','b','c','d','e'};
std::vector<char> upperVowel = letters
    | std::ranges::views::filter(isVowel)
    | std::ranges::views::transform(toupper)
    | std::ranges::to<std::vector<char>>();

// upperVowel = { 'A', 'E' }
```

---

## Slide 133: Remember: range algorithms are eager

**Remember: range algorithms are eager**

`std::ranges` are a reskin of the old STL algorithms

*Figure: A code snippet and an illustration of The Flash, a speedster superhero in a red suit with lightning effects, running through a city street. The elements are contained within a black-bordered rectangle.*

```cpp
// This actually sorts vec, RIGHT NOWWW!!!!
std::ranges::sort(v);
```

---

## Slide 134: Remember: views are lazy

std::ranges::views are a lazy way of composing algorithms

```cpp
auto view = letters
| std::ranges::views::filter(isVowel)
| std::ranges::views::transform(toupper);

std::vector<char> upperVowel =
std::ranges::to<std::vector<char>>(view);
```

*Figure: A meme featuring a sloth against a colorful geometric background. The top text reads "SOMEONE CALLED ME LAZY YESTERDAY" and the bottom text reads "I ALMOST REPLIED".*

---

## Slide 135: Pro tip: Views are like Python generators

This code in C++ works *exactly* the same as this Python code

```cpp
auto view = letters
    | std::ranges::views::filter(isVowel)
    | std::ranges::views::transform(toupper);
auto upperVowel = std::ranges::to<std::vector<char>>(view);
```

*Figure: A large red double-headed vertical arrow pointing between the C++ code block above and the Python code block below, indicating their equivalence.*

```python
view = (l for l in letters if isVowel(l))    # Lazy evaluation
view = (l.upper() for l in view)             # Lazy evaluation
upperVowel = list(view)
```

---

## Slide 136: What questions do you have?
What questions do you have?

*Figure: A photograph of Bjarne Stroustrup looking at the camera with his hand resting near his chin. Below the image, the text "bjarne_about_to_raise_hand" is shown in gray.*

---

## Slide 137: Ranges and view recap

*   Why you might like ranges/views?
    *   ✅ Worry less about iterators
    *   ✅ Constrained algorithms mean better error messages
    *   ✅ Super readable, functional syntax
*   Why you might dislike ranges/views?
    *   ❌ They are extremely new, not fully feature complete yet
    *   ❌ Lack of compiler support
    *   ❌ Loss of performance compared to hand-coded version
        *   ℹ️ For more info, see [The Terrible Problem of Incrementing a Smart Iterator](https://www.google.com)

Links on this slide:
- <https://www.fluentcpp.com/2019/02/12/the-terrible-problem-of-incrementing-a-smart-iterator/>
