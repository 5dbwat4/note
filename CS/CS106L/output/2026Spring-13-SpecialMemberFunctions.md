# Lecture 13: SpecialMemberFunctions (2026Spring)

> PDF title: 2026Spring-13-SpecialMemberFunctions.pptx
> Source: `assets/slides/2026Spring-13-SpecialMemberFunctions.pdf` · 70 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: CS106L Lecture 13: Special Member Functions

CS106L Lecture 13:
Special Member Functions ⭐

Preston Seay & Rachel Fernandez

---

## Slide 2: Attendance

*Figure: A QR code. The QR code is square-shaped, composed of black modules on a white background, with the three standard finder patterns. Below the QR code is a URL.*

https://forms.gle/dDxtXhgExMPo9Afh9

---

## Slide 3: Today's Agenda

1. Recap
2. Special Member Functions
   - An overview
   - Copy and copy assignment
   - delete
   - Move and move assignment

---

## Slide 4: Today's Agenda
1. Recap
2. Special Member Functions
   - An overview
   - Copy and copy assignment
   - `delete`
   - Move and move assignment

---

## Slide 5: Non-member overloading

### Non-member Operator Overloading
```cpp
bool operator< (const StudentID& lhs, const StudentID& rhs);
```

### Member Operator Overloading
```cpp
bool StudentID::operator< (const StudentID& rhs) const {...}
```

---

## Slide 6: Pop Quiz!

*Figure: A presentation slide with a pink header bar containing the title "Pop Quiz!" in large, bold, black text. Below the header, on a white background, are two bulleted questions.*

- What’s an advantage of non-member overloading over member overloading?
- What do you sometimes have to do with member overloading that you don’t with non-member overloading?

---

## Slide 7: Pop Quiz!

*Figure: A header banner with a salmon-colored gradient background containing the bold, centered title "Pop Quiz!".*

- What’s an advantage of non-member overloading over member overloading?
    - It is symmetric!
- What do you sometimes have to do with non-member overloading that you don’t with member overloading?
    - If you need to access private/protected fields, you need to specify that it is a `friend`.

---

## Slide 8: Clarification

.cpp file

```cpp
#include StanfordID.h

std::string StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfirdID& other) const {
    return idNumber < other.getIdNumber();
}
```

*Figure: A green checkmark icon is positioned at the end of the last line of code, indicating the correct implementation of the operator.*

---

## Slide 9: Clarification

.cpp file

```cpp
#include StanfordID.h

std::string StanfordID::getIdNumber() {
    return idNumber;
}

bool StanfordID::operator<(const StanfordID& other) const {
    return idNumber < other.idNumber; ✅
}
```

---

## Slide 10: Clarification

### .cpp file

*Figure: A C++ code snippet enclosed within a thin black rectangular border. The snippet shows an include statement, a member function definition for `getIdNumber()`, an ellipsis, and a comparison operator definition. A red cross mark (❌) is placed at the end of the return statement in the comparison operator function.*

```cpp
#include StanfordID.h

// defined within the StanfordID class
std::string StanfordID::getIdNumber() {
    return idNumber;
}

. . .

bool operator<(const StanfirdID& lhs, const StanfirdID& rhs) const
{
    return lhs.idNumber < rhs.idNumber; ❌
}
```

---

## Slide 11: Clarification

.cpp file

```cpp
#include StanfordID.h

// defined within the StanfordID class
std::string StanfordID::getIdNumber() {
    return idNumber;
}
. . .

bool operator<(const StanfirdID& lhs, const StanfirdID& rhs) const
{
    return lhs.getIdNumber() < rhs.getIdNumber(); ✅
}
```

---

## Slide 12: Hello friend!

*Figure: A wide, light-red to white gradient bar at the top of the slide containing the title.*

# Hello friend!

*Figure: A light-tan rectangular box with a thin black border centered near the top of the slide, containing a subheading.*

### Non-member Operator Overloading

*Figure: A white rectangular box with a thick black border centered below the subheading, containing a C++ function declaration.*

```cpp
bool operator< (const StudentID& lhs, const StudentID& rhs);
```

The **friend** keyword allows non-member functions or classes to access private information in another class!

### How do you use friend?
In the header of the target class you declare the operator overload function as a friend

*Figure: A black-bordered box positioned in the bottom right corner of the slide containing a notice with a yellow-highlighted label.*

**Notice:** If StanfordID didn't have a
getIdNumber() method, you'd have to add **friend**
to access **idNumber** directly

---

## Slide 13: So Many Operators!!!

- There are many operators that you can define in C++ like we saw

```
+  -  *  /  %  ^  &  |  ~  !  ,  =  <  >  <=  >=
++  --  <<  >>  ==  !=  &&  ||  +=  -=  *=
/=  %=  ^=  &=  |=  <<=  >>=  []  ()  ->
->*  new  new[]  delete  delete[]
```

---

## Slide 14: Today's Agenda

1. Recap
2. **Special Member Functions**
   - **An overview**
   - Copy and copy assignment
   - delete
   - Move and move assignment

---

## Slide 15: You may remember

Classes have
1. Constructor
2. Destructor
3. Member Variables
4. Functions

> 🤯 Surprise 🤯, these are called **Special Member Functions** (SMFs)

A **constructor** is called every time a new instance of the class is created, and the **destructor** is called when it goes out of scope

---

## Slide 16: The Special 6: SMFs

These functions are generated only when they're called (and before any are explicitly defined by you):

*   Default constructor: `T()`
*   Destructor: `~T()`
*   Copy constructor: `T(const T&)`
*   Copy assignment operator: `T& operator=(const T&)`
*   Move constructor: `T(T&&)`
*   Move assignment operator: `T& operator=(T&&)`

*Figure: A rectangular box with a black border containing the list of the six special member functions (SMFs).*

---

## Slide 17: Let's look at Widget :)

```cpp
class Widget {
  public:
    Widget();                           // default constructor
    Widget (const Widget& w);           // copy constructor
    Widget& operator = (const Widget& w); // copy assignment operator
    ~Widget();                          // destructor
    Widget (Widget&& rhs);              // move constructor
    Widget& operator = (Widget&& rhs);  // move assignment operator
}
```

---

## Slide 18: There are 6 special member functions!

*Figure: A slide titled "There are 6 special member functions!" with a red header. Below the title is a C++ code snippet defining a `class Widget` and its special member functions. The line for the default constructor is highlighted with a red rectangle. To the bottom right of the code, a beige callout box with a black border contains the text "Takes no parameters and creates a new object".*

```cpp
class Widget {
public:
  Widget();                                // default constructor
  Widget (const Widget& w);                // copy constructor
  Widget& operator = (const Widget& w);    // copy assignment operator
  ~Widget();                               // destructor
  Widget (Widget&& rhs);                   // move constructor
  Widget& operator = (Widget&& rhs);       // move
}
```

---

## Slide 19: There are 6 special member functions!

```cpp
class Widget {
public:
  Widget();                                    // default constructor
  Widget (const Widget& w);                   // copy constructor
  Widget& operator = (const Widget& w);       // copy assignment operator
  ~Widget();                                  // destructor
  Widget (Widget&& rhs);                      // move constructor
  Widget& operator = (Widget&& rhs);          // move assignment operator
}
```

*Figure: The copy constructor line `Widget (const Widget& w);` is highlighted with a red rectangular box. A beige callout box in the lower right points to this line and contains the text: "Creates a new object as a member-wise copy of another".*

---

## Slide 20: When is the copy constructor invoked?

```cpp
Widget widgetOne;
Widget widgetTwo = widgetOne;  // Copy constructor is called
```

---

## Slide 21: There are 6 special member functions!

*Figure: A red horizontal banner at the top of the slide contains the title.*

```cpp
class Widget {
  public:
    Widget();                             // default constructor
    Widget (const Widget& w);             // copy constructor
    Widget& operator = (const Widget& w); // copy assignment operator
    ~Widget();                            // destructor
    Widget (Widget&& rhs);                // move constructor
    Widget& operator = (Widget&& rhs);    // move...
}
```

*Figure: A red rectangle outlines the code line `Widget& operator = (const Widget& w); // copy assignment operator`. To the right of the code, a beige callout box with a black border points toward this highlighted line. It contains the text: "Assigns an already existing object to another", where the words "already existing" and "object" are underlined.*

---

## Slide 22: When is the copy assignment operator invoked?

*Figure: A slide with a pink/salmon banner containing the title in large bold black text. Below, centered on the slide, is a white box with a black border containing three lines of C++ code. To the bottom-right is a light beige/cream box with a black border containing an explanatory note.*

```
Widget widgetOne;
Widget widgetTwo;
widgetOne = widgetTwo
```

*Note box (bottom-right, light beige background with black border):*

> Note that here both objects
> are constructed before the
> use of the = operator

---

## Slide 23: Copy Constructor vs Assignment Operator

*Figure: The slide is organized into two sections, each illustrating a different C++ concept. Each section has a title in red text inside a beige rectangular box, followed by a white rectangular box containing a code example.*

### Copy Constructor Invocation

```cpp
Widget widgetOne;
Widget widgetTwo = widgetOne;
```

### Copy Assignment Operator Invocation

```cpp
Widget widgetOne;
Widget widgetTwo;
widgetOne = widgetTwo
```

---

## Slide 24: There are 6 special member functions!

```cpp
class Widget {
public:
    Widget();                                      // default constructor
    Widget (const Widget& w);                      // copy constructor
    Widget& operator = (const Widget& w);          // copy assignment operator
    ~Widget();                                     // destructor
    Widget (Widget&& rhs);                         // move constructor
    Widget& operator = (Widget&& rhs);             // mov
}
```

*Figure: A beige text box with a black border points to the line `~Widget(); // destructor` in the code. The text box contains the annotation: "Called when the object goes out of scope".*

---

## Slide 25: There are 6 special member functions!

*Figure: A slide with a large red banner at the top containing the slide title. Below is a C++ code snippet for a class named `Widget`. A red rectangle highlights the last two member function declarations. A callout box in the bottom right corner contains a note.*

```cpp
class Widget {
  public:
    Widget();                                 // default constructor
    Widget (const Widget& w);                 // copy constructor
    Widget& operator = (const Widget& w);     // copy assignment operator
    ~Widget();                                // destructor
    Widget (Widget&& rhs);                    // move constructor
    Widget& operator = (Widget&& rhs);        // move assignment operator
}
```

*Figure: Callout box containing the text: "We have an entire lecture on these – not the focus of today".*

---

## Slide 26: There are 6 special member functions!

*Figure: A large pink gradient banner at the top of the slide contains the title in black text. Below the banner, on the left, is a C++ code snippet defining a `class Widget`. To the right of the code is a beige callout box with a black border and a drop shadow.*

```cpp
class Widget {
public:
    Widget();
    Widget (const Widget& w);
    Widget& operator = (const Widget& w);
    ~Widget();
    Widget (Widget&& rhs);            // move constructor
    Widget& operator = (Widget&& rhs); // move assignment operator
}
```

The callout box on the right contains the following text:
> We don’t have to write out any of these! They all have default versions that are generated automatically!

---

## Slide 27: Today's Agenda

*Figure: A horizontal banner at the top of the slide with a pinkish-red gradient background, containing the centered title text "Today's Agenda" in a large, bold font.*

1. Recap
2. **Special Member Functions**
   - An overview
   - **Copy and copy assignment**
   - `delete`
   - Move and move assignment

---

## Slide 28: Review: initialization

*Figure: The slide title "Review: initialization" is centered at the top in a large, bold, black font against a light red rectangular background banner.*

*Figure: Below the title, a light gray rectangular box contains the text "Remember our Vector from lecture 8?".*

> Remember our Vector from lecture 8?

*Figure: A large white box with a thin black border contains a C++ code snippet.*

```cpp
template <typename T>
Vector<T>::Vector()
{
  _size = 0;
  _capacity = 4;
  _data = new T[_capacity];
}
```

*Figure: In the bottom right corner, a light gray rectangular box contains a two-line note.*

> When we create a constructor, we need to
> initialize all of our member variables.

---

## Slide 29: Review: initialization

```cpp
template <typename T>
Vector<T>::Vector()
{
  _size = 0;
  _capacity = 4;
  _data = new T[_capacity];
}
```

*Figure: A slide with a title bar at the top. Below the title is a white box with a black border containing C++ code for a template constructor. To the right of the code box is a beige speech bubble pointing toward the code. The text in the bubble reads: "However, initializing them to be the default value and then reassigning is inefficient!"*

---

## Slide 30: Vector Constructor Code

🤔

```cpp
template <typename T>
Vector<T>::Vector()
{
  _size = 0;
  _capacity = 4;
  _data = new T[_capacity];
}
```

There are two steps
happening here

---

## Slide 31: Step 1

```cpp
template <typename T>
Vector<T>::Vector()
{
    _size = 0;
    _capacity = 4;
    _data = new T[_capacity];
}
```

*Figure: A C++ code snippet showing the default constructor for a Vector class. To the right, a callout box overlaps the code, containing explanatory text.*

There are two steps happening here: the first is that `_size`, `_capacity`, and `_data` may have been default initialized.

---

## Slide 32: Step 2

```cpp
template <typename T>
Vector<T>::Vector()
{
  _size = 0;
  _capacity = 4;
  _data = new T[_capacity];
}
```

*Figure: A black-bordered box contains the C++ code for the `Vector<T>::Vector()` constructor. A second, light-colored callout box with a black border is positioned to its right, with a line pointing to the code block. It contains explanatory text.*

> Then the assignment to the variables, which effectively doubles the work.

---

## Slide 33: Member initialization Lists

*Figure: A lecture slide with a pink gradient title banner at the top containing the heading "Member initialization Lists" in a large, bold, black font. In the center of the slide is a black-bordered box containing a C++ code snippet. To the bottom right of the code box is a beige-colored callout box with a thin black border containing explanatory text.*

```cpp
template <typename T>
Vector<T>::Vector() : _size(0), _capacity(4), _data(new T[_capacity]) { }
```

We can use **initializer lists** to declare and initialize them with desired values at once!

---

## Slide 34: Initializer Lists

* It’s quicker and more efficient to directly construct member variables with intended values
* What if the variable is a non-assignable type?
* Can be used for any constructor, even non-default ones with parameters!

```cpp
template <typename T>
Vector<T>::Vector() : _size(0), _capacity(4), _data(new
T[_capacity]) { }
```

---

## Slide 35: What if the variable is a non-assignable type?

```cpp
template <typename T>
class MyClass {
    const int _constant;
    int& _reference;

public:
    // Only way to initialize const and reference members
    MyClass(int value, int& ref) : _constant(value),
_reference(ref) { }
};
```

*   This code *only* works with initializer lists
*   Why? 🤔

---

## Slide 36: Why should we override SMFs?

- The compiler gives them to us for free…..?
    - a. By default, the copy constructor will create copies of each member variable

This is **member-wise** copying!

Is this always good enough?

---

## Slide 37: Consider Pointers

If your variable is a pointer, a memberwise copy will point to the same allocated data, not a fresh copy!

*Figure: A code snippet is shown inside a black rectangular border. The expression `_data(other._data)` is highlighted with a red bounding box. A beige callout box is positioned at the bottom right of the code snippet.*

```cpp
template <typename T>
Vector<T>::Vector<T>(const Vector::Vector<T>& other) :
_size(other._size), _capacity(other._capacity),
_data(other._data) { }
```

These pointers will point at the same underlying array!

---

## Slide 38: Consider Pointers

If your variable is a pointer, a memberwise copy will point to
the same allocated data, not a fresh copy!

```cpp
template <typename T>
Vector<T>::Vector<T>(const Vector::Vector<T>& other) :
    _size(other._size), _capacity(other._capacity),
    _data(other._data) { }
```

*Figure: A diagram showing two vectors, `vec` (with a blue arrow) and `copy` (with an orange arrow), both pointing at the same underlying array. The array contains five cells labeled 0, 1, 2, 3, and 4. The `_data(other._data)` line in the code is highlighted with a red box.*

> These pointers will point at
> the same underlying array!

---

## Slide 39: Consider Pointers

If your variable is a pointer, a memberwise copy will point to the same allocated data, not a fresh copy!

```cpp
template <typename T>
Vector<T>::Vector<T>(const Vector<T>& other) :
_size(other._size), _capacity(other._capacity),
_data(other._data) { }
```

*Figure: A diagram illustrating a shallow copy. An array is shown with five cells labeled 0, 1, 2, 3, and 4. Two pointers, "vec" (black arrow) and "copy" (orange arrow), both point to the first cell of the same array. In the code block above, the initialization line `_data(other._data)` is highlighted with a red rectangular border. A callout box in the bottom right contains the warning: "This is problematic because anything done to one pointer affects the other".*

---

## Slide 40: Copying isn’t always so simple!

*   Many times, you will want to create a copy that does more than just copies the member variables.

*   Deep copy: an object that is a complete, **independent** copy of the original

*   In these cases, you'd want to override the default special member functions with your own implementation!

*   Declare them in the header and write their implementation in the .cpp, like any function!

---

## Slide 41: Fixing the pointer issue

```cpp
Vector<T>::Vector(const Vector<T>& other)
    : _size(other._size), _capacity(other._capacity), _data(new
T[other._capacity]) {
    for (size_t i = 0; i < _size; ++i) {
        _data[i] = other._data[i];
    }
}
```

*Figure: Two arrays are shown, labeled `_data` and `other.data` respectively. An arrow from `_data` points to an array with five cells containing the numbers 0, 1, 2, 3, and 4. An arrow from `other.data` points to a separate, identical array with the same five numbers. This illustrates that the new Vector has its own independent copy of the elements.*

Now we have a “deep” copy
of the data in our Vector.

---

## Slide 42: Today's Agenda

1. Recap
2. **Special Member Functions**
   * An overview
   * Copy and copy assignment
   * **delete**
   * Move and move assignment

---

## Slide 43: How do you prevent copies?

Let’s say you have a class that handles all of your passwords:

```cpp
class PasswordManager {
  public:
    PasswordManager();
    ~PasswordManager();
    // other methods ...
    PasswordManager(const PasswordManager& rhs);
    PasswordManager& operator = (const PasswordManager& rhs);

  private:
    // other important members ...
}
```

---

## Slide 44: We can delete special member functions

Setting a special member function to **delete** removes its functionality!

```cpp
class PasswordManager {
public:
    PasswordManager();
    PasswordManager(const PasswordManager& pm);
    ~PasswordManager();
    // other methods ...
    PasswordManager(const PasswordManager& rhs) = delete;
    PasswordManager& operator = (const PasswordManager& rhs) = delete;

private:
    // other important members ...
}
```

*Figure: A red rectangle highlights the lines declaring the copy constructor and copy assignment operator as deleted, which explicitly removes their functionality.*

---

## Slide 45: We can delete special member functions

Setting a special member function to **delete** removes its functionality!

```cpp
class PasswordManager {
  public:
    PasswordManager();
    PasswordManager(const PasswordManager& pm);
    ~PasswordManager();
    // other methods ...
    PasswordManager(const PasswordManager& rhs) = delete;
    PasswordManager& operator = (const PasswordManager& rhs) = delete;

  private:
    // other important members ...
}
```

*Figure: A text box with a black border containing the note "Now copying isn't a possible operation!" points to the lines of code where the copy constructor and copy assignment operator are marked as deleted.*

---

## Slide 46: Why?

We can selectively allow functionality of special member functions!

* This has lots of uses – what if we only want one copy of an instance to be allowed?
* This is how classes like `std::unique_ptr` work!

*Figure: A callout box with an arrow pointing to a quoted text. The callout box contains the text: "You may see this in cppreference which specifies this!". The arrow points down to the quoted text below.*

> The class satisfies the requirements of *MoveConstructible* and *MoveAssignable*, but of neither *CopyConstructible* nor *CopyAssignable*.

---

## Slide 47: Philosophy time

*Figure: A photograph of a man sitting in an ergonomic office chair in a cubicle. He is wearing glasses, a patterned shirt, and white pants. He is reclining with his feet, wearing sneakers, propped up on a desk. Behind him on the desk are multiple older-model CRT computer monitors. Above the desk is a shelf holding what appear to be software boxes or binders. There are also framed documents or certificates hanging on the cubicle wall.*

---

## Slide 48: Rule of Zero

If the default SMFs work, **don’t define your own!**

We should only define new ones when the default ones generated by the compiler won't work.

*   This usually happens when we work with dynamically allocated memory, like pointers to things on the heap!

---

## Slide 49: Rule of Zero

If you don't need a constructor or a destructor or copy assignment etc. Then simply don't use it!

**If your class relies on objects/classes that already have these SMFs implemented, then there's no need to reimplement this logic!**

```cpp
class a_string_with_an_id() {
    public:
        // getter and setter methods for our private variables
    private:
        int id;
        std::string str;
}
a_string_with_an_id object;
```

*Figure: A grey rounded callout bubble with an arrow pointing to the code block. The text inside reads: "Our class a_string_with_an_id has self managing variables."*

---

## Slide 50: Rule of Zero

If you don’t need a constructor or a destructor or copy assignment etc. Then simply don’t use it!

If your class relies on objects/classes that already have these SMFs implemented, then there’s no need to reimplement this logic!

```cpp
class a_string_with_an_id() {
    public:
        /// getter and setter methods for our private variables
    private:
        int id;
        std::string str;
}
a_string_with_an_id object;
```

*Figure: A callout box pointing to the `std::string` member in the class code. It states: `std::string already has copy constructor, copy assignment, move constructor, and move assignment!`*

---

## Slide 51: Rule of Three

If you need a custom destructor, then you also probably **<u>need</u>** to define a copy constructor and a copy assignment operator for your class

### Why is this the case?

If you use a destructor, that often means that you are manually dealing with dynamic memory allocation/are generally just handling your own memory.

### If this is the case:

The compiler will not be able to automatically generate these for you, because of the manual memory management.

---

## Slide 52: Recap

The four special member functions discussed so far:

*   **Default Constructor**
    *   Object created with no parameters, no member variables instantiated
*   **Copy Constructor**
    *   Object created as a copy of existing object (member variable-wise)
*   **Copy Assignment Operator**
    *   Existing object replaced as a copy of another existing object.
*   **Destructor**
    *   Object destroyed when it is out of scope.

---

## Slide 53: Practice

*Figure: A large, black and white QR code centered on the slide.*

https://106l.vercel.app/pirate-smfs

Links on this slide:
- <https://106l.vercel.app/pirate-smfs>

---

## Slide 54: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

What type of operation or function is each of these lines?

---

## Slide 55: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: A C++ code snippet displaying various ways to initialize `vector<int>` objects. A red rectangular highlight is drawn around the second line of code: `vector<int> vec1;`.*

Default Constructor

---

## Slide 56: Pop Quiz

*Figure: A C++ code snippet is shown within a black border. A red rectangular box highlights the line `vector<int> vec2(3);`.*

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

Custom constructor,
not SMF

---

## Slide 57: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: A C++ code snippet inside a black-bordered box. The line `vector<int> vec3{3};` is highlighted with a red rectangle.*

Uniform initialization,
not an SMF

---

## Slide 58: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: A code snippet showing a C++ function definition. The line `vector<int> vec4();` is highlighted with a red rectangle.*

Tricky, this is a function definition

---

## Slide 59: Pop Quiz

*Figure: A C++ code snippet enclosed in a black box. A red rectangular outline highlights the line `vector<int> vec5(vec2);`.*

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

Copy Constructor

---

## Slide 60: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: The code is displayed inside a black-bordered box. The line `vector<int> vec6{};` is highlighted with a red rectangular outline, indicating it is the focus of the quiz.*

**Initializer list is empty – empty vector via list initialization**

---

## Slide 61: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: A red rectangular outline highlights the following line of code:* `vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};`

**List initialization**

---

## Slide 62: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: A red rectangle highlights the line `vector<int> vec8 = vec2;` in the code block.*

Copy constructor

---

## Slide 63: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

**Copy assignment operator**

---

## Slide 64: Pop Quiz
```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: The line `return vec8;` is highlighted with a red rectangular border.*

### Copy constructor

---

## Slide 65: Pop Quiz: Pop Quiz

```cpp
vector<int> func(vector<int> vec0) {
    vector<int> vec1;
    vector<int> vec2(3);
    vector<int> vec3{3};
    vector<int> vec4();
    vector<int> vec5(vec2);
    vector<int> vec6{};
    vector<int> vec7{static_cast<int>(vec2.size() + vec6.size())};
    vector<int> vec8 = vec2;
    vec8 = vec2;
    return vec8;
}
```

*Figure: A code snippet inside a black bordered box. The parameter `vector<int> vec0` in the function signature is highlighted with a red rectangle.*

Tricky bonus one:

Copy constructor

---

## Slide 66: Today's Agenda

1. Recap
2. **Special Member Functions**
   * An overview
   * Copy and copy assignment
   * `delete`
   * **Move and move assignment**

*Figure: The slide features a thick pink banner across the top containing the title "Today's Agenda" in large, bold, black text. Below the banner is a numbered list of lecture topics on a plain white background.*

---

## Slide 67: Is copying enough?

We’ve learned about the default constructor, destructor, and the copy constructor and assignment operator.

* We can create an object, get rid of it, and copy its values to another object!
* Is this ever insufficient?

---

## Slide 68: This can be wasteful

These functions are generated only when they're called (and before any are explicitly defined by you):

```cpp
class Widget {
public:
    Widget();
    Widget (const Widget& w);
    Widget& operator = (const Widget& w);
    ~Widget();
    Widget (Widget&& rhs);      // move constructor
    Widget& operator = (Widget&& rhs); // move assignment operator
}
```

*Figure: A code snippet of a `Widget` class definition. A red rectangular border highlights the `Widget (Widget&& rhs);` and `Widget& operator = (Widget&& rhs);` lines. To the right, partially overlapping the code comments, is a beige text box that reads "Let's motivate move semantics".*

---

## Slide 69: This can be wasteful

Let's say we had to copy our current StringTable into another, whose reference is given to us, and we have no use for our StringTable afterwards.

*Figure: A code snippet showing the definition of the `StringTable` class. A red rectangle highlights the copy constructor declaration. To the right of the code is a callout box containing explanatory text.*

```cpp
class StringTable {
public:
  StringTable() {}
  StringTable(const StringTable& st) {}
  // functions for insertion, erasure, lookup, et
  // but no move/dtor functionality
  // ...

private:
  std::map<int, std::string> values;
}
```

The copy constructor will
copy every value in the
values map one by one!
Very slowly!

---

## Slide 70: A good way to prime move semantics

### Move semantics: move or duplicate

*Figure: A two-panel hand-drawn cartoon. The left panel is labeled "COPY" and shows a person pushing a shopping cart while a duplicate house is being created, marked with a "NEW" icon. The right panel is labeled "MOVE" and shows two people carrying a piece of furniture from one house to another, with a blue arrow indicating the direction of the transfer. A signature at the bottom right of the cartoon reads "© Joaquín Fernández Fuster".*

I really like this way of thinking about move semantics:

Watch the full video [here]

Andreas Fertig  
41.4  
Back to Basics: Move Semantics  
3

Links on this slide:
- <https://youtu.be/knEaMpytRMA?si=L0bMtZ0adnRm9GuP>
