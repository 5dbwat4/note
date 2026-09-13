# Lecture 15: Optional&TypeSafety (2026Spring)

> PDF title: 2026Spring-15-Optional&TypeSafety.pptx
> Source: `assets/slides/2026Spring-15-Optional&TypeSafety.pdf` · 90 pages · transcribed with `mimo-v2.5` · 2026-09-07

---

## Slide 1: CS106L Lecture 15: std::optional & type safety!

CS106L Lecture 15:

std::optional & type safety!

Preston Seay && Rachel Fernandez

---

## Slide 2: Attendance

*Figure: A QR code for attendance.*

https://forms.gle/2YbCCKE6tWgZMtq27

Links on this slide:
- <https://forms.gle/2YbCCKE6tWgZMtq27>

---

## Slide 3: Announcements

1. Rachel moved her OH to now Wednesdays 160-B37 from 3PM - 3:50PM
2. Last official class this Thursday
3. Next Tuesday lecture is optional
   a. Attend to make up 1 absence
4. Assignment 7: due May 29th

*Figure: A light purple gradient banner at the top of the slide contains the main title text.*

---

## Slide 4: Plan

1. Recap
2. Type safety
3. `std::optional`

---

## Slide 5: Recapping some shuff

### Move semantics

- We have move semantics because sometimes the resource we’re going to take is no longer needed by the original owner

```cpp
#include <iostream>
#include <vector>
#include <utility> // for std::move

int main() {
    std::vector<int> a = {1, 2, 3};

    // We no longer need 'a', so let's move it into 'b'
    std::vector<int> b = std::move(a);

    std::cout << "a.size() = " << a.size() << "\n"; // 0
    std::cout << "b.size() = " << b.size() << "\n"; // 3

    return 0;
}
```

---

## Slide 6: Recapping some stuff

### Move semantics

- We have move semantics because sometimes the resource we're going to take is **no longer needed by the original owner**

```cpp
#include <iostream>
#include <vector>
#include <utility> // for std::move

int main() {
    std::vector<int> a = {1, 2, 3};

    // We no longer need 'a', so let's move it into 'b'
    std::vector<int> b = std::move(a);

    std::cout << "a.size() = " << a.size() << "\n"; // 0
    std::cout << "b.size() = " << b.size() << "\n"; // 3

    return 0;
}
```

- Use **std::move(a)** to turn **a**, an l-value, to an r-value so that you can immediately take its resources

---

## Slide 7: Recapping some shtuff

### Move semantics

- We have move semantics because sometimes the resource we're going to take is no longer needed by the original owner
- Use **std::move(a)** to turn **a**, an l-value, to an r-value so that you can immediately take its resources
- **Rule of zero:** if you have self-managing member variables, and don't need to define custom constructors, and operators, then don't!

---

## Slide 8: Rule of ZERO

**Rule of zero:** if you have self-managing member variables, and don’t need to define custom constructors, and operators, then don’t!

*Figure: A code editor screenshot displaying a C++ class named `Student`. The class contains private member variables of type `std::string` and `std::vector<int>`. A block of comments highlights that the destructor and special member functions (copy/move constructors and operators) are intentionally omitted to follow the Rule of Zero.*

```cpp
#include <string>
#include <vector>

class Student {
public:
  // We don't write:
  // - destructor
  // - copy constructor
  // - copy assignment operator
  // - move constructor
  // - move assignment operator

  // Why? Because std::string and std::vector manage themselves!
  Student(std::string name, std::vector<int> scores)
    : name_(std::move(name)), scores_(std::move(scores)) {}

private:
  std::string name_;       // self-managing
  std::vector<int> scores_; // self-managing
};
```

C++ automatically gives us the following (if we don’t define our own)
1. Destructor
2. Copy constructor
3. Copy assignment operator
4. Move constructor
5. Move assignment operator

These work great here!

---

## Slide 9: Rule of ZERO

*Figure: The slide features the title "Rule of ZERO" in large bold black font against a light purple gradient banner. Below the banner, a definition of the "Rule of zero" is provided, with the phrase "Rule of zero:" highlighted in yellow. The lower portion of the slide contains a C++ code example on the left and a numbered list of C++'s automatically generated functions on the right.*

**Rule of zero:** if you have self-managing member variables, and don't need to define custom constructors, and operators, then don't!

```cpp
#include <string>
#include <vector>

class Student {
public:
    // We don't write:
    // - destructor
    // - copy constructor
    // - copy assignment operator
    // - move constructor
    // - move assignment operator

    // Why? Because std::string and std::vector manage themselves!
    Student(std::string name, std::vector<int> scores)
        : name_(std::move(name)), scores_ (std::move(scores)) {}

private:
    std::string name_;         // self-managing
    std::vector<int> scores_;  // self-managing
};
```

C++ automatically gives us the following (if we don't define our own)

1. Destructor:
   `~Student();`
2. Copy constructor
   `Student(const Student& other);`
3. Copy assignment operator
   `Student& operator=(const Student& other);`
4. Move constructor
   `Student(Student&& other);`
5. Move assignment operator
   `Student& operator=(Student&& other);`

---

## Slide 10: Recapping some shtuff

### Move semantics
- We have move semantics because sometimes the resource we’re going to take is no longer needed by the original owner
- Use `std::move(x)` to turn `x`, an l-value, to an r-value so that you can immediately take its resources
- **Rule of zero:** if you have self-managing member variables, and don’t need to define custom constructors, and operators, then don’t!
- **Rule of three:** if you define a custom destructor then you need to also define a custom copy constructor and copy assignment operator.

---

## Slide 11: Rule of THREE

**Rule of three**: if you define a custom destructor then you need to also define a custom copy constructor and copy assignment operator.

*Figure: Two code editor panels showing a C++ `Student` class. The left panel (green border) contains the constructor, destructor, and copy constructor; the right panel (purple border) contains the copy assignment operator and private members. A red box highlights `scores_(new int[numScores])` in the constructor initializer list on the left. A red box highlights `int* scores_;` and its comment in the private section on the right.*

**Left code panel:**

```cpp
class Student {
public:
    Student(const std::string& name, int numScores)
        : name_(name), numScores_(numScores), scores_(new int[numScores]) {}

    // 1. Destructor - must free the array
    ~Student() {
        delete[] scores_;
    }

    // 2. Copy constructor - deep copy the array
    Student(const Student& other)
        : name_(other.name_), numScores_(other.numScores_) {

        scores_ = new int[numScores_];        // allocate
        for (int i = 0; i < numScores_; i++)   // deep copy
            scores_[i] = other.scores_[i];
    }
};
```

**Right code panel:**

```cpp
// 3. Copy assignment - deep copy + avoid self-assignment
Student& operator=(const Student& other) {
    if (this != &other) {
        // free old resource
        delete[] scores_;

        // copy non-resource fields
        name_ = other.name_;
        numScores_ = other.numScores_;

        // deep copy array
        scores_ = new int[numScores_];
        for (int i = 0; i < numScores_; i++)
            scores_[i] = other.scores_[i];
    }
    return *this;
}

private:
    std::string name_;
    int numScores_;
    int* scores_;        // RAW pointer - not self-managing!
};
```

---

## Slide 12: Recapping some shtuff

**Move semantics**
- We have move semantics because sometimes the resource we’re going to take is no longer needed by the original owner
- Use `std::move(x)` to turn `x`, an l-value, to an r-value so that you can immediately take its resources
- Rule of zero: if you have self-managing member variables, and don’t need to define custom constructors, and operators, then don’t!
- ~~Rule of three: if you define a custom destructor then you need to also define a custom copy constructor and copy assignment operator.~~
- **Rule of Five:** If you have a custom copy constructor, and copy assignment operator, then you should also define a move constructor and a move assignment operator!

---

## Slide 13: Rule of FIVE

**Rule of Five:** If you have a custom copy constructor, and copy assignment operator, then you should also define a move constructor and a move assignment operator!

*Figure: Two side-by-side code editor windows displaying implementations of move semantics for a `Student` class. The left window shows the "Move constructor" and the right window shows the "Move assignment" operator.*

```cpp
// Move constructor
Student(Student&& other)
: name_(std::move(other.name_)),
numScores_(other.numScores_),
scores_(other.scores_) {

other.scores_ = nullptr;
other.numScores_ = 0;
}
```

```cpp
// Move assignment
Student& operator=(Student&& other) {
if (this != &other) {
delete[] scores_;

name_ = std::move(other.name_);
numScores_ = other.numScores_;
scores_ = other.scores_;

other.scores_ = nullptr;
other.numScores_ = 0;
}
return *this;
}
```

---

## Slide 14: What questions do we have?

What questions do we have?

*Figure: A brown tabby cat with large, wide eyes peeking over a white ledge.*

---

## Slide 15: A definition!

*Figure: The phrase "Type Safety" is highlighted with a yellow background.*
Type Safety: The extent to which a language prevents typing errors.

---

## Slide 16: Python (english) vs. C++

**Python**
```python
def div_3(x):
    return x / 3
div_3(“hello”)
//CRASH during runtime,
can’t divide a string
```

**C++**
```cpp
int div_3(int x){
    return x / 3;
}
div_3(“hello”)
//Compile error: this code
will never run
```

*Figure: A side-by-side comparison of Python and C++ code for a function `div_3` that divides an input by 3. Both examples attempt to call the function with a string argument (`"hello"`). The Python code includes a comment indicating it will cause a runtime crash, while the C++ code includes a comment indicating a compile-time error will occur, preventing the code from running.*

---

## Slide 17: Real World Example: Missing Mars

*Figure: A diagram depicting the solar system with the Sun at the center. Earth is shown on a smaller, blue circular orbit labeled "Earth Orbit". Mars is on a larger, yellow circular orbit labeled "Mars Orbit". A small spacecraft is illustrated near Mars. The background is a starry space scene.*

1 Earth Year = 365 days
1 Mars Year = 687 Earth days or 669 sols (martian days)

---

## Slide 18: Python (english) vs. C++

*The title "Python (english) vs. C++" is displayed in a purple banner at the top of the slide. The phrase "Type Safety:" is highlighted with a yellow background.*

**Type Safety: The extent to which a language guarantees the behavior of programs.**

---

## Slide 19: What should the return type be?

```cpp
??? f(vector<int> vec, int value);
```

f({1, 3, 7}, 3) == 1                                           (index 1)
f({67}, 67) == 0                                               (index 0)
f({106, 107, 111, 143, 144, 149}, 111) == 2    (index 2)

---

## Slide 20: What should the return type be?

??? f(vector<int> vec, int value);

*   f({1, 3, 7}, 3) == 1                                           (index 1)
*   f({67}, 67) == 0                                               (index 0)
*   f({106, 107, 111, 143, 144, 149}, 111) == 2    (index 2)
*   **f({}, 10) == what do we return now?**

---

## Slide 21: What does this code do?

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

*Figure: A yellow callout box positioned to the right of the code snippet provides explanations for the member functions used.*

**vector::back()** returns a reference to the last element in the vector

**vector::pop_back()** is like the opposite of vector::push_back(elem). It removes the last element from the vector.

---

## Slide 22: Anyone see a problem?

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

> *Figure: A yellow callout box to the right of the code contains notes about the `vector` methods used in the code.*

**vector::back()** returns a reference to the last element in the vector

**vector::pop\_back()** is like the opposite of vector::push\_back(elem). It removes the last element from the vector.

---

## Slide 23: Anyone see a problem?

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

*Figure: A light gray rounded-rectangle button containing the word "Hint!" in red, underlined text, positioned to the right of the function's parameter list.*

*Figure: A pale yellow callout box containing definitions for C++ vector methods:*

**`vector::back()`** returns a reference to the last element in the vector

**`vector::pop_back()`** is like the opposite of vector::push\_back(elem). It removes the last element from the vector.

---

## Slide 24: Anyone see a problem?

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

*Figure: A highlighted question box below the code snippet.* The box contains the text: What if **vec** is {} / an empty vector!?

---

## Slide 25: std::vector documentation

*Figure: A screenshot of C++ documentation for the `std::vector::back` function.*

### std::vector\<T,Allocator\>::back

```cpp
reference back();                               // (until C++20)
constexpr reference back();                     // (since C++20)
const_reference back() const;                   // (until C++20)
constexpr const_reference back() const;         // (since C++20)
```

Returns a reference to the last element in the container.

*Figure: A red-bordered box highlighting the warning: "Calling back on an empty container causes undefined behavior."*

**Undefined behavior:** Function could crash, could give us garbage, could accidentally give us some actual value

---

## Slide 26: Taking another look at our code

*Figure: Title text "Taking another look at our code" displayed in large black font on a purple gradient background bar.*

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

We can make no guarantees about what this function does!

*Credit to Jonathan Müller of foonathan.net for the example!*

---

## Slide 27: One solution

*Figure: A purple rectangular header at the top of the slide contains the title "One solution". Below the header is a block of C++ code.*

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(!vec.empty() && vec.back() % 2 == 1){
        vec.pop_back();
    }
}
```

---

## Slide 28: One solution

```cpp
void removeOddsFromEnd(vector<int>& vec){
  while(!vec.empty() && vec.back() % 2 == 1){
    vec.pop_back();
  }
}
```

**Key idea:** it is the **programmers job** to enforce the **precondition** that **vec** be non-empty, otherwise we get undefined behavior!

---

## Slide 29: vec.back() Deterministic Behavior

There may or may not be a "last element" in vec

How can vec.back() have deterministic behavior in either case?

---

## Slide 30: The problem

```cpp
valueType& vector<valueType>::back(){
return *(begin() + size() - 1);
}
```

*Figure: The line `return *(begin() + size() - 1);` in the code block above is highlighted with a light red background. Below the code, a speech bubble points upward toward the code block and contains the text: "What happens if size() = 0?".*

Dereferencing a pointer without verifying it points to real memory is undefined behavior!

*Figure: A thinking face emoji is located at the bottom right of the slide.*

---

## Slide 31: The problem

```cpp
valueType& vector<valueType>::back(){
    if(empty()) throw std::out_of_range;
    return *(begin() + size() - 1);
}
```

Now, we will at least reliably error and stop the program or return the last element whenever back() is called

---

## Slide 32: The problem

Deterministic behavior is great, but can we do better?

There may or may not be a “last element” in vec

How can `vec.back()` warn us of that when we call it?

---

## Slide 33: Revisiting our definition

**Type Safety**: The extent to which a **function** signature guarantees the behavior of a **function**.

---

## Slide 34: Back to the problem

*The slide title "Back to the problem" is displayed in a large, bold, black sans-serif font centered within a light purple gradient banner at the top of the slide.*

```cpp
valueType& vector<valueType>::back(){
return *(begin() + size() - 1);
}
```

*The first line of the code block, `valueType& vector<valueType>::back(){`, is highlighted with a light pink background.*

**back()** is promising to return something of type **valueType** when its possible no such value exists!

---

## Slide 35: A look at a first solution

```cpp
std::pair<bool, valueType&> vector<valueType>::back(){
    if(empty()){
        return {false, valueType()};
    }
    return {true, *(begin() + size() - 1)};
}
```

**back()** now advertises that there may or may not be a last element

---

## Slide 36: A look at a first solution

```cpp
std::pair<bool, valueType&> vector<valueType>::back(){
    if(empty()){
        return {false, valueType()};
    }
    return {true, *(begin() + size() - 1)};
}
```

*Figure: Code annotation — a callout box with an arrow points to `valueType()` in the return statement, labeled: "Default constructor of **valueType()**"*

**back()** now advertises that there may or may not be a last element

---

## Slide 37: Problems with std::pair

```cpp
std::pair<bool, valueType&> vector<valueType>::back(){
    if(empty()){
        return {false, valueType()};
    }
    return {true, *(begin() + size() - 1)};
}
```

*Figure: A code snippet illustrating a problem with `std::pair`. A green highlight box surrounds the `valueType()` expression in the return statement.*

- **valueType** may not have a default constructor :(((

---

## Slide 38: Problems with std::pair

```cpp
std::pair<bool, valueType&> vector<valueType>::back(){
    if(empty()){
        return {false, valueType()};
    }
    return {true, *(begin() + size() - 1)};
}
```

- **valueType** may not have a default constructor
- Even if it does, calling constructors is **expensive**

---

## Slide 39: Problems with std::pair

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back().second % 2 == 1){
        vec.pop_back();
    }
}
```

*In the code above, the expression `vec.back().second` is highlighted in yellow.*

This is still pretty unpredictable behavior! What if the default constructor for an int produced an **odd number**?

---

## Slide 40: What should back return in this case?

```cpp
??? vector<valueType>::back(){
  if(empty()){
    return ??;
  }
  return *(begin() + size() - 1);
}
```

---

## Slide 41: What questions do we have?

*Figure: A photograph of a tabby kitten with wide, yellowish-green eyes and a pink nose, looking directly at the viewer while peering over a white horizontal surface or ledge against a plain white background. Its front paws are visible resting on the edge.*

---

## Slide 42: Introducing std::optional

---

## Slide 43: What is std::optional<T>

- **std::optional** is a template class which will either contain a value of type **T** or contain nothing (expressed as **nullopt**)

*Figure: A documentation-style information box for `std::optional`.*

### std::optional
Defined in header `<optional>`
```cpp
template< class T >       (since C++17)
class optional;
```
The class template std::optional manages an optional contained value, i.e. a value that may or may not be present. A common use case for optional is the return value of a function that may fail. As opposed to other approaches, such as `std::pair<T, bool>`, optional handles expensive-to-construct objects well and is more readable, as the intent is expressed explicitly.

---

## Slide 44: What is std::optional<T>

- **std::optional** is a template class which will either contain a value of type **T** or contain nothing (expressed as **nullopt**)

*Figure: A yellow callout box contains a note and definitions. A red arrow points from this box to the word "nullopt" in the first bullet point.*

**Note:** that’s nullopt NOT nullptr. It’s a new thing!
- **nullptr**: an object that can be converted to a value of any **pointer** type
- **nullopt**: an object that can be converted to a value of any **optional** type

---

## Slide 45: What is std::optional<T>

-   **std::optional** is a template class which will either contain a value of type **T** or contain nothing (expressed as **nullopt**)

```cpp
int* p = nullptr;      // p points to nothing
if (p == nullptr) {
    std::cout << "p is a null POINTER\n";
}

std::optional<int> x = nullptr;   // ERROR - nullptr is NOT for optionals
```

```cpp
std::optional<int> x = std::nullopt;     // x contains nothing
if (!x) {
    std::cout << "x is an EMPTY OPTIONAL\n";
}

int* p = std::nullopt;    // ERROR - nullopt is NOT a pointer
```

*Figure: A callout box on the right side of the slide contains a note and definitions. A red arrow points from the word "nullopt" in the main bullet text to this callout box. The box contains the following text:*

**Note: that’s nullopt NOT nullptr. It’s a new thing!**

**nullptr:** an object that can be converted to a value of any **pointer** type

**nullopt:** an object that can be converted to a value of any **optional** type

---

## Slide 46: What is std::optional\<T\>

- **std::optional** is a template class which will either contain a value of type **T** or contain nothing (expressed as **nullopt**)

```cpp
void main(){
    std::optional<int> num1 = {}; //num1 does not have a value
    num1 = 1; //now it does!
    num1 = std::nullopt; //now it doesn't anymore
}
```

*Figure: A green box containing the text "Can be used interchangeably!" is positioned in the bottom right of the slide. Two arrows originate from this box and point to specific parts of the code: the first arrow points to the empty braces `{}` in the first line of code, and the second arrow points to the expression `std::nullopt` in the third line of code.*

---

## Slide 47: What is std::optional\<T\>

```cpp
std::optional<valueType> vector<valueType>::back(){
    if(empty()){
        return {};
    }
    return *(begin() + size() - 1);
}
```

---

## Slide 48: What using back() look like:

```cpp
void removeOddsFromEnd(vector<int>& vec){
  while(vec.back() % 2 == 1){
    vec.pop_back();
  }
}
```

We can’t do arithmetic with an optional, we have to get the value inside the optional (if it exists) first!

---

## Slide 49: What’s the interface of std::optional?

**std::optional** types have a:
- .value() method:
  returns the contained value or throws **bad_optional_access** error

---

## Slide 50: What's the interface of std::optional?

**std::optional** types have a:

- **.value()** method:
  returns the contained value or throws **bad_optional_access** error

- **.value_or(valueType val)**
  returns the contained value or default value, parameter **val**

---

## Slide 51: What's the interface of std::optional?

`std::optional` types have a:
- `.value()` method:
    returns the contained value or throws `bad_optional_access` error
- `.value_or(valueType val)`
    returns the contained value or default value, parameter `val`
- `.has_value()`
    returns `true` if contained value exists, `false` otherwise

---

## Slide 52: What's the interface of std::optional?

*Figure: A code snippet showing the initialization and basic usage of `std::optional`, including the `has_value()` method, displayed within a code editor interface.*

```cpp
#include <iostream>
#include <optional>

int main() {
    std::optional<int> a = 5;
    std::optional<int> b = std::nullopt;

    // ---------------------------
    // 1. has_value()
    // ---------------------------
    std::cout << "a.has_value(): " << a.has_value() << "\n"; // 1 (true)
    std::cout << "b.has_value(): " << b.has_value() << "\n"; // 0 (false)
}
```

---

## Slide 53: What’s the interface of std::optional?

*Figure: A screenshot of a code editor displaying a C++ code snippet about `std::optional`. The code is shown with line numbers 149 through 157 in the left gutter.*

```cpp
// -----------------------------------
// 2. value()
// -----------------------------------
if (a.has_value()) {
    std::cout << "a.value(): " << a.value() << "\n";      // 5
}

// Uncommenting this would throw bad_optional_access:
// std::cout << b.value() << "\n";
```

---

## Slide 54: What’s the interface of std::optional?
```cpp
    // Uncommenting this would throw bad_optional_access:
    // std::cout << b.value() << "\n";

    // ----------------------------
    // 3. value_or(default)
    // ----------------------------
    std::cout << "a.value_or(999): " << a.value_or(999) << "\n";  // 5
    std::cout << "b.value_or(999): " << b.value_or(999) << "\n";  // 999

    return 0;
```

---

## Slide 55: Revisiting back()

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back().value() % 2 == 1){
        vec.pop_back();
    }
}
```

Now, if we access the back of an empty vector, we will at least reliably get the **bad_optional_access** error

---

## Slide 56: Revisiting back()

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back().has_value() && vec.back().value() % 2 == 1){
        vec.pop_back();
    }
}
```

This will no longer error, but it is pretty unwieldy :/

---

## Slide 57: Revisiting back()

```cpp
void removeOddsFromEnd(vector<int>& vec){
    while(vec.back() && vec.back().value() % 2 == 1){
        vec.pop_back();
    }
}
```

Better? You can just call `vec.back()` since `nullopt` is falsy!

---

## Slide 58: Recap: The problem with std::vector::back()

- Why is it so easy to accidentally call **back()** on empty vectors if the outcome is so dangerous?
- The function signature gives us a false promise!
```cpp
valueType& vector<valueType>::back()
```
- Promises to return an something of type **valueType**
- But in reality, there either may or may not be a “last element” in a vector

---

## Slide 59: An optional take on realVector

---

## Slide 60: More bad code!
```cpp
int foo(vector<int>& vec){
    return vec[0];
}
```

What happens if **vec** is empty? More undefined behavior!

---

## Slide 61: std::optional<T&> is not available!
```cpp
std::optional<valueType&>
vector<valueType>::operator[](size_t index){
    if (index < size()) {
        return *(begin() + index);
    }
    return std::nullopt;
}
```

---

## Slide 62: std::optional<T&> is not available!

```cpp
std::optional<valueType&>
vector<valueType>::operator[](size_t index){
    if (index < size()) {
        return *(begin() + index);
    }
    return std::nullopt;
}
```

A reference must be to a valid object, and optional doesn’t guarantee that,
think about having an optional to a nullopt

---

## Slide 63: std::optional<T&> is not available!

```cpp
std::optional<valueType&>
vector<valueType>::operator[](size_t index){
if (index < size()) {
return *(begin() + index);
}

return std::nullopt;
}
```

*Figure: A screenshot of a code editor window containing a `main` function. The code attempts to use the vector's `operator[]` to assign to an `auto` variable, illustrating why `std::optional<T&>` is not a viable return type for such an interface.*

```cpp
int main() {
vector <int> v;
v.data = {10, 20, 30};

auto optRef = v[5];    // returns std::nullopt
// ERROR: int& must store a reference to a real integer, not std::nullopt
}
```

---

## Slide 64: Best we can do is error..which is what .at() does

```cpp
valueType& vector<valueType>::operator[](size_t index){
    return *(begin() + index);
}
```

```cpp
valueType& vector<valueType>::at(size_t index){
    if(index >= size()) throw std::out_of_range;
    return *(begin() + index);
}
```

🤔 Why have both?

---

## Slide 65: Is this…..good?

Pros of using **std::optional** returns:

- Function signatures create more informative contracts
- Class function calls have guaranteed and usable behavior

Cons:

- You will need to use **.value()** EVERYWHERE
- (In cpp) It’s still possible to do a **bad_optional_access**
- (In cpp) optionals can have undefined behavior too (**\*optional** does same thing as **.value()** with no error checking)
- In a lot of cases we want **std::optional<T&>**...which we don’t have

---

## Slide 66: ?: Why even bother with optionals?

*Figure: A light purple gradient background with centered black text.*

---

## Slide 67: Is this…..good?

- `.and_then(function f)`
    - returns the result of calling `f(value)` if contained value exists, otherwise `nullopt` (`f` must return optional)

---

## Slide 68: .and_then(function f)

```cpp
#include <iostream>
#include <optional>

std::optional<int> half(int x) {
    if (x % 2 == 0) return x / 2;
    return std::nullopt;
}

int main() {
    std::optional<int> a = 8;

    auto result = a.and_then(half)    // 8 -> 4
                  .and_then(half)  // 4 -> 2
                  .and_then(half); // 2 -> 1

    if (result)
        std::cout << *result;  // prints 1

    std::optional<int> b = 7;

    auto result2 = b.and_then(half);  // 7 is odd -> nullopt

    if (!result2)
        std::cout << "\nhalf(7) failed!\n";
}
```

---

## Slide 69: Is this…..good?

- **`.and_then(function f)`**
  - returns the result of calling f(value) if contained value exists,
    otherwise nullopt (f must return optional)

- **`.transform(function f)`**
  - returns the result of calling f(value) if contained value exists,
    otherwise nullopt (f must return valueType)

---

## Slide 70: Is this.....good?

*   `.and_then(function f)`
    `f: valueA → optional<valueB>` (i.e., f might fail)
*   `.transform(function f)`
    `f: valueA → valueB` (i.e., f won't fail)

---

## Slide 71: .transform(function f)

```cpp
#include <iostream>
#include <optional>

int square(int x) { return x * x; }

int main() {
    std::optional<int> x = 5;

    auto y = x.transform(square);

    if (y)
        std::cout << *y;      // prints 25

    std::optional<int> z = std::nullopt;

    auto w = z.transform(square);  // z is empty -> nullopt

    if (!w)
        std::cout << "\nsquare(nullopt) = nullopt\n";
}
```

---

## Slide 72: Is this.....good?
- `.and_then(function f)`
  - returns the result of calling `f(value)` if contained value exists, otherwise `nullopt` (f must return optional)
- `.transform(function f)`
  - returns the result of calling `f(value)` if contained value exists, otherwise `nullopt` (f must return value)
- `.or_else(function f)`
  - returns value if it exists, otherwise returns result of calling f

---

## Slide 73: .or_else(function f)

```cpp
#include <iostream>
#include <optional>

std::optional<int> fallback() {
    return 42;
}

int main() {
    std::optional<int> good = 10;
    std::optional<int> bad  = std::nullopt;

    auto r1 = good.or_else(fallback);  // returns optional(10)
    auto r2 = bad.or_else(fallback);   // returns optional(42)

    std::cout << "r1 = " << *r1 << "\n";  // 10
    std::cout << "r2 = " << *r2 << "\n";  // 42
}
```

---

## Slide 74: Is this.....good?

*Figure: A slide with a purple gradient header containing the title. The main white area contains a bulleted list on the left, partially overlapped by a large light-yellow rectangular box on the right.*

- **.and_then(function f)**
  returns the result of calling f(value) if contained value exists, otherwise null_opt (f must return optional)
- **.transform(function f)**
  returns the result of calling f(value) if contained value exists, otherwise null_opt (f must return optional\<valueType\>)
- **.or_else(function f)**
  returns value if it exists, otherwise returns result of calling f

**Monadic:** a software design pattern with a structure that combines program fragments (functions) and wraps their return values in a type with additional computation

These all let you try a function and will either return the result of the computation or some default value.

---

## Slide 75: We've seen this before!

*Figure: Screenshot of a code editor showing a C++ program that defines `square` and `add_one` functions and uses C++20 ranges views to chain operations on a sequence.*

```cpp
int square(int x) {
    return x * x;
}

int add_one(int x) {
    return x + 1;
}

int main() {
    using namespace std::views;

    auto v =
        iota(1, 11)
        | transform(square)
        | transform(add_one)
        | filter([](int x) { return x % 2 == 0; });

    for (int x : v) {
        std::cout << x << " ";
    }
}
```

Chaining views together is monadic!

---

## Slide 76: Is this.....good?

- **`.and_then(function f)`**
    - returns the result of calling `f(value)` if contained value exists,
    - otherwise `null_opt` (`f` must return optional)
- **`.transform(function f)`**
    - returns the result of calling `f(value)` if contained value exists,
    - otherwise `null_opt` (`f` must return `optional<valueType>`)
- **`.or_else(function f)`**
    - returns value if it exists, otherwise returns result of calling `f`

---

## Slide 77: Revisiting our back() code...again!

*Figure: A C++ code snippet showing a function that removes odd numbers from the end of a vector using `std::optional` and `and_then`.*

```cpp
void removeOddsFromEnd(vector<int>& vec){
    auto isOdd = [](optional<int> num){
        if(num)
            return num % 2 == 1;
        else
            return std::nullopt;
        //return num ? (num % 2 == 1) : {};
    };
    while(vec.back().and_then(isOdd)){
        vec.pop_back();
    }
}
```

---

## Slide 78: Revisiting our back() code...again!

```cpp
void removeOddsFromEnd(vector<int>& vec){
  auto isOdd = [](optional<int> num){
    if(num)
      return num % 2 == 1;
    else
      return std::nullopt;
    //return num ? (num % 2 == 1) : {};
  };
  while(vec.back().and_then(isOdd)){
    vec.pop_back();
  }
}
```

*Figure: A slide showing a C++ code snippet for a function named `removeOddsFromEnd`. Inside the function, a lambda function named `isOdd` is defined and is highlighted by a thick orange rectangular box. A callout bubble to the right of the box contains the text "Recall lambda functions!", with an arrow pointing from the callout to the orange box. Below the lambda definition, the `while` keyword is highlighted with a yellow background.*

---

## Slide 79: Disclaimer

Disclaimer: std::vector::back() doesn't actually return an optional (and probably never will)

*Figure: A slide with a solid light purple background and centered text.*

---

## Slide 80: Recall: Design philosophies of C++

*Figure: A purple gradient banner at the top of the slide containing the slide's title.*

- Only add features if they solve an actual problem
- Programmers should be free to choose their style
- Compartmentalization is key
- Allow the programmer full control if they want it
- Don't sacrifice performance except as a last resort
- Enforce safety at compile time whenever possible

---

## Slide 81: Recall: Design philosophies of C++

- Only add features if they solve an actual problem
- Programmers should be free to choose their style
- Compartmentalization is key
- Allow the programmer full control if they want it
- Don't sacrifice performance except as a last resort
- Enforce safety at compile time whenever possible

---

## Slide 82: Languages that *really* use optional monads

- Rust 🥰😍
    - Systems language that guarantees memory and thread safety
- Swift
    - Apple’s language, made especially for app development
- JavaScript
    - Everyone’s favorite

---

## Slide 83: Recap: Type safety and std::optional
- You can guarantee the behavior of your programs by using a strict type system!

---

## Slide 84: Recap: Type safety and std::optional

- You can guarantee the behavior of your programs by using a strict type system!
- **std::optional** is a tool that could make this happen: you can return either a value or nothing: **.has_value()**, **.value_or()**, **.value()**

---

## Slide 85: Recap: Type safety and std::optional
- You can guarantee the behavior of your programs by using a strict type system!
- **std::optional** is a tool that could make this happen: you can return either a value or nothing: `.has_value()`, `.value_or()`, `.value()`
- This can be unwieldy and slow, so cpp doesn’t use optionals in most stl data structures

---

## Slide 86: Recap: Type safety and std::optional
- You can guarantee the behavior of your programs by using a strict type system!
- `std::optional` is a tool that could make this happen: you can return either a value or nothing: `.has_value()`, `.value_or()`, `.value()`
- This can be unwieldy and slow, so cpp doesn’t use optionals in most stl data structures
- Many languages, however, do!

---

## Slide 87: Recap: Type safety and std::optional

- You can guarantee the behavior of your programs by using a strict type system!
- `std::optional` is a tool that could make this happen: you can return either a value or nothing: `.has_value()`, `.value_or()`, `.value()`
- This can be unwieldy and slow, so cpp doesn't use optionals in most stl data structures
- Many languages, however, do!
- Besides using them in classes, you can use them in application code where it makes sense! This is highly encouraged :)

---

## Slide 88: All in all

**"Well typed programs cannot go wrong."**

- Robert Milner (very important and good CS dude)

---

## Slide 89: What questions do we have?

*Figure: A close-up photograph of a tabby cat peeking over a white surface. The cat has wide, yellow-green eyes, a pink nose, and its two front paws are resting on the surface on either side of its head. The background is plain white.*

---

## Slide 90: Let's make it ourselves!

Let's make it ourselves!

[https://106l.vercel.app/optional](https://106l.vercel.app/optional)
