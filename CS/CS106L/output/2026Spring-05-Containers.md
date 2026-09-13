# Lecture 05: Containers (2026Spring)

> Source: `assets/slides/2026Spring-05-Containers.pdf` · 68 pages · transcribed with `mimo-v2.5` · 2026-08-27

---

## Slide 1: Lecture 5: Containers

Preston Seay, Rachel Fernandez

---

## Slide 2: Plan

* (Recap)
1. Space-time
2. STL
3. Sequence Containers
4. Associative Containers

---

## Slide 3: Recap
### A stringstream is an...
* istream ✅
* ostringstream ✅

*Figure: A class hierarchy diagram for C++ I/O streams. At the top, the `ios` class is linked to `streambuf` via a composition arrow (diamond shape). `ios` has two derived classes: `istream` and `ostream`. `streambuf` has three derived classes: `filebuf`, `stringbuf`, and `stdiobuf`. `istream` has three derived classes: `istringstream`, `ifstream`, and `iostream`. `ostream` has three derived classes: `iostream`, `ofstream`, and `ostringstream`. The `iostream` class, which inherits from both `istream` and `ostream`, has three derived classes: `fstream`, `stringstream`, and `stdiostream`. A large green upward-pointing arrow indicates the `stringstream` class.*

---

## Slide 4: Recap

*Figure: Screenshot of a code editor (IDE) with a purple header labeled "Recap". The editor interface includes tabs for "Code" and "Console", a "CPP" language indicator, and a blue "Run" button. The main area displays a C++ code snippet with line numbers 1 through 12 in a dark gutter.*

```cpp
#include <iostream>
#include <sstream>
#include <string>
int main() {
    std::stringstream ss;
    ss << 3.14f << ' ' << "hello"; // use as ostream

    float pi; std::string hi;
    ss >> pi >> hi; // use as istream

    std::cout << pi << '\n' << hi << std::endl;
}
```

---

## Slide 5: Plan

*Figure: A purple horizontal banner at the top of the slide containing the word "Plan" centered in white text.*

1. **Space-time**
2. STL
3. Sequence Containers
4. Associative Containers

---

## Slide 6: Task - Fetch a wrench
Task - Fetch a wrench

---

## Slide 7: Cluttered Garage Illustration

*Figure: A photograph of a very cluttered garage. A large red toolbox is on the left, a red convertible car is on the right, and the floor is covered with various items including a lawn mower, a floor jack, and car parts. Several pink arrows are drawn over the image, pointing to different parts of the mess. A purple box with the word "AHA" in pink capital letters is located in the upper right quadrant.*

Visible text on objects in the image:
- **AHA**
- **JEGS**
- **Snap-on**
- **ip.com**
- **BEECHWOLD**
- **PITTSBURGH**

---

## Slide 8: Organized Garage Storage

*Figure: A photograph of an organized garage wall featuring multiple metal shelving units. The main unit holds plastic storage bins, coolers, and bags on the top shelves. The middle shelves contain clear bins with various tools and supplies. Below the shelves, a horizontal slat wall holds hanging items such as extension cords, helmets, a tote bag, a folded chair, and a blue patterned backpack. On the floor are a Honda lawnmower, a DeWalt tool, a tree stump, and other equipment. To the right, a blue ladder stands between the main shelves and a separate metal shelving unit filled with power tools and paint cans. A purple rectangular annotation box with the pink text "AHA" is overlaid on the right side, with a thick pink arrow pointing from the box to the separate metal shelving unit on the right.*

---

## Slide 9: How much stuff?

How much stuff?

---

## Slide 10: Messy Garage with Clutter

*Figure: A photograph of a highly cluttered garage interior. A red convertible Volkswagen Beetle is parked on the right side of the frame. To the left, there are large red rolling tool chests, one of which features a yellow "JEGS" logo. The floor is covered with various items, including a red snow blower on the far left, a "Pittsburgh" floor jack in the lower right, engine parts, wooden panels, and boxes. Three large magenta arrows are overlaid on the image: one points toward the rear of the red car, another points to a pile of engine parts on the ground, and a third points toward a collection of items in the central area of the garage floor.*

---

## Slide 11: Space helps you see and navigate

Space helps you see and navigate

*Figure: A photograph of an organized garage wall with shelves, hanging storage, and various tools. A large purple rectangle with the pink text "Space helps you see and navigate" is overlaid in the center, with a large pink arrow pointing down to the empty floor space in front of the organized items.*

---

## Slide 12: Quote: Space is time

*Figure: A photograph of a dark, starry night sky. Overlaid in the center is a semi-transparent gray rectangle containing a quote in white text.*

"Space is time."
- Bjarne Stroustrup

[source]

Links on this slide:
- <https://www.stroustrup.com/quotes.html>

---

## Slide 13: Disorganized vs Organized

### Disorganized
*Figure: A tall, untidy stack of loose papers, representing a disorganized storage approach.*
- Space efficient
- Slow to search
- Ex: vector

### Organized
*Figure: A person's hand placing a document into an organized filing cabinet with labeled hanging folder tabs, representing a structured storage approach.*
- Space inefficient
- Faster to search
- Ex: map

---

## Slide 14: Plan
1. **Space-time**
2. STL
3. Sequence Containers
4. Associative Containers

---

## Slide 15: Announcements

* Assignment 1 is out, due this Friday!
* Office hours start this Thursday, 4:30-5:20pm in Thornton 210.

---

## Slide 16: Plan

1. Space-time
2. STL
3. Sequence Containers
4. Associative Containers

---

## Slide 17: Standard Template Library (STL)

How is this different from the standard library std?

*Figure: A diagram illustrating the composition of the C++ Standard Library. A large outer rectangle is labeled "C++ Standard Library". Inside this rectangle, on the left side, are three smaller, vertically stacked rectangles labeled, from top to bottom: "streams", "strings", and "...". To the right of these is another, larger rectangle labeled "Standard Template Library", which is also contained within the "C++ Standard Library" rectangle, indicating that the STL is a component of the standard library.*

---

## Slide 18: Standard Template Library (STL)

*Figure: A hierarchical diagram illustrating the relationship between the C++ Standard Library and the Standard Template Library (STL). The entire diagram is contained within a large blue-bordered box titled "C++ Standard Library". On the left side of this box, four smaller blue-bordered boxes are stacked vertically, labeled: "streams", "strings", "math", and "...". On the right side, a larger blue-bordered box titled "Standard Template Library" is nested within the C++ Standard Library. This nested box contains four smaller blue-bordered boxes arranged in a 2x2 grid labeled: "Containers", "Iterators", "Functors", and "Algorithms".*

---

## Slide 19: Standard Template Library (STL)

*Figure: Diagram illustrating the relationship between the C++ Standard Library and the Standard Template Library (STL). The C++ Standard Library is shown as a large blue-outlined box containing several components: streams, strings, math, and other components (indicated by "..."). Within the C++ Standard Library box, there is a smaller blue-outlined box labeled "Standard Template Library", which in turn contains four components: Containers (highlighted in green), Iterators, Functors, and Algorithms. The diagram visually represents the organization and scope of these libraries.*

```cpp
// No code present on the slide.
```

---

## Slide 20: Standard Template Library (STL)

*   Made by Alexander Stepanov

*Figure: A stamp-like graphic featuring a portrait of Alexander Stepanov. The text "ALEXANDER STEPANOV" is written vertically on the left. A logo with "A9" and a smile arrow is in the top right. At the bottom, there is a line of code.*

```cpp
#include <algorithm>
```

*Figure: A diagram showing the components of the "Standard Template Library". A large blue-outlined rectangle labeled "Standard Template Library" contains four smaller blue-outlined boxes arranged in a 2x2 grid, labeled "Containers", "Iterators", "Functors", and "Algorithms".*

---

## Slide 21: What does template mean?

*Figure: The slide has a purple header with the title "What does template mean?". Below are several overlapping dark-themed code editor windows showing different implementations of list classes for various data types. The windows are arranged in a grid-like pattern, with some overlapping and partially obscuring others.*

### Code Window 1 (Top Left: IntList)
```cpp
class IntList {
    ...
};

int main() {
    IntList ints();
    ints.add(10);
    ints.add(20);

    assert(ints.g...
}
```

### Code Window 2 (Top Center: StringList)
```cpp
class StringList {
    ...
};

int main() {
    StringList strs();
    strs.add("1");
    strs.add("2");

    assert(strs.get(0) == "1");
}
```

### Code Window 3 (Top Right: DoubleList, partially visible)
```cpp
bleList {
...

) {
.ist dbls();
ld(1.0);
ld(2.0);

dbls.get(0) == 1.0);
}
```

### Code Window 4 (Bottom Left: FloatList)
```cpp
class FloatList {
    ...
};
```

### Code Window 5 (Bottom Center: BoolList)
```cpp
class BoolList {
    ...
};
```

### Code Window 6 (Bottom Right: CharList)
```cpp
class CharList {
    ...
};
```

---

## Slide 22: What does template mean?

*Figure: The slide demonstrates the concept of a template in C++. On the left side, there are three separate, type-specific class definitions for a list: one for integers (`IntList`), one for doubles (`DoubleList`), and one for strings (`StringList`). A large red arrow points from these three separate classes to the right side, which shows a single, generic class template named `Vector<T>`. Below the template definition, there is a code example using the standard library's `vector` template to hold different data types.*

```cpp
class IntList {
    ...
};
```

```cpp
class DoubleList {
    ...
};
```

```cpp
class StringList {
    ...
};
```

```cpp
// You'll learn more wk 5!
template <typename T>
class Vector<T> {
    ...
}
```

```cpp
#include <vector>

int main() {
    std::vector<int> ints;
    std::vector<double> dbls;
    std::vector<std::string> strs;

    ints.push_back(1);
    dbls.push_back(5.4);
    strs.push_back("hi");
    std::cout << ints[0] + dbls[0];
}
```

---

## Slide 23: Plan
1. Space-time
2. STL
3. **Sequence Containers**
4. Associative Containers

---

## Slide 24: Sequence Containers

"Sequence containers implement data structures which can be accessed sequentially."

In other words, they contain sequences.

*Figure: A dark-themed user interface panel titled "Containers Reference". In the top right corner of the panel, it says "Open in new tab". Below the title, there is a QR code on the left. To the right of the QR code, there is a text box containing the URL `https://en.cppreference.com/w/cpp/container.html`. Below the URL, a caption reads: "Scan the code or open the URL in a browser to view the live page."*

https://en.cppreference.com/w/cpp/container.html

Links on this slide:
- <https://en.cppreference.com/w/cpp/container.html>

---

## Slide 25: Sequence Containers

*   Vector
*   Deque
*   Array
*   List

*Figure: A dark-themed information box titled "Containers Reference" appears on the right side of the slide. It includes a QR code and a URL. At the top right of the box is the text "Open in new tab". Inside a smaller sub-window within the box, the heading "Containers Reference" is repeated above a URL bar containing `https://en.cppreference.com/w/cpp/container.html`. Below the URL, it says "Scan the code or open the URL in a browser to view the live page."*

Links on this slide:
- <https://en.cppreference.com/w/cpp/container.html>

---

## Slide 26: Vectors

# Vectors

## "A resizable contiguous array"

*Figure: A diagram of a vector shown as six contiguous gray boxes. The boxes contain values 1, 2, 3, 4, 5, 6 from left to right. Below each box is its index: 0, 1, 2, 3, 4, 5 respectively.*

*Figure: A screenshot of a code editor with a dark theme. The editor has two tabs: "Code" and "Console", with "Code" selected. The top-right corner shows "CPP" and a blue "Run" button. The code is a C++ program demonstrating vector usage.*

```cpp
#include <vector>
#include <iostream>
int main() {
  std::vector<int> vec { 1, 2, 3, 4 };
  vec.push_back(5);
  vec.push_back(6);
  vec[1] = 20;

  for (size_t i = 0; i < vec.size(); i++) {
    std::cout << vec[i] << " ";
  }
}
```

---

## Slide 27: Vectors

"A resizable contiguous array"

*Figure: A diagram representing a vector as a sequence of six contiguous boxes. Below the boxes are the indices 0, 1, 2, 3, 4, and 5. The boxes contain the values 1, 20, 3, 4, 5, and 6. The box at index 1, which contains the value "20", is highlighted in light green.*

*Figure: A screenshot of a C++ code editor with the header "CPP" and a "Run" button. The editor contains a program demonstrating vector initialization, modification, and iteration.*

```cpp
#include <vector>
#include <iostream>
int main() {
  std::vector<int> vec { 1, 2, 3, 4 };
  vec.push_back(5);
  vec.push_back(6);
  vec[1] = 20;

  for (size_t i = 0; i < vec.size(); i++) {
    std::cout << vec[i] << " ";
  }
}
```

---

## Slide 28: Index Checking?

*   Be careful with indices
*   [] doesn't check
*   .at() does

*Figure: Screenshot of a C++ code editor (dark theme) with two tabs at the top: "Code" (active) and "Console". To the right is a label "CPP" and a blue "Run" button. The editor displays a C++ program with line numbers in a left gutter, which are omitted from the transcription below. Line 9, containing the loop condition `i < 10`, has the number `10` highlighted with a green background.*

```cpp
#include <vector>
#include <iostream>
int main() {
    std::vector<int> vec { 1, 2, 3, 4 };
    vec.push_back(5);
    vec.push_back(6);
    vec[1] = 20;

    for (size_t i = 0; i < 10; i++) {
        std::cout << vec[i] << " ";
    }
}
```

---

## Slide 29: Index Checking?

1. You don't pay for what you don't use.
2. What you do use is just as efficient as what you could reasonably write by hand.

*Figure: A dark-themed UI element titled "Zero-overhead principle" with an "Open in new tab" link in the top right. The element contains a QR code on the left and the following text on the right:*

**Zero-overhead principle**
`https://en.cppreference.com/w/cpp/language/Zero-overhead_principle.html`

Scan the code or open the URL in a browser to view the live page.

---

https://en.cppreference.com/w/cpp/language/Zero-overhead_principle.html

Links on this slide:
- <https://en.cppreference.com/w/cpp/language/Zero-overhead_principle.html>

---

## Slide 30: How do Vectors Resize?

Resizing vectors copies over the whole array into a bigger array - Dynamic reallocation
Open in new tab

*Figure: A dark blue container with three window control dots at the top left. Inside is a card displaying a QR code and related information.*

**Resizing vectors copies over the whole array into a bigger array - Dynamic reallocation**

https://web.stanford.edu/~pseay/cs106l/vectors

Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://web.stanford.edu/~pseay/cs106l/vectors>

---

## Slide 31: 106B vs. Standard Vectors

*Figure: A table comparing the syntax for common vector operations in the Stanford C++ library (`Vector<int>`) and the C++ Standard Library (`std::vector<int>`). The slide has a purple title bar at the top.*

| What you want to do? | Stanford Vector\<int\> | std::vector\<int\> |
| :--- | :--- | :--- |
| Create an empty vector | `Vector<int> v;` | `std::vector<int> v;` |
| Create a vector with **n** copies of **0** | `Vector<int> v(n);` | `std::vector<int> v(n);` |
| Create a vector with **n** copies of value **k** | `Vector<int> v(n, k);` | `std::vector<int> v(n, k);` |
| Add **k** to the end of the vector | `v.add(k);` | `v.push_back(k);` |
| Clear vector | `v.clear();` | `v.clear();` |
| Check if **v** is empty | `if (v.isEmpty())` | `if (v.empty())` |
| Get the element at index **i** | `int v = v.get(i);`<br>`int k = v[i];` | `int k = v.at(i);`<br>`int k = v[i];` |
| Replace the element at index **i** | `v.get(i) = k;`<br>`v[i] = k;` | `v.at(i) = k;`<br>`v[i] = k;` |

---

## Slide 32: Practice with Vectors

**Task:**
Write a C++ function to calculate the maximum value of a vector, using 4 different vector methods.

*Figure: A QR code for an online IDE project.*

https://www.online-ide.com/6lQX5aeEn9

Links on this slide:
- <https://www.online-ide.com/6lQX5aeEn9>

---

## Slide 33: Walkthrough

*Figure: Screenshot of a C++ code editor. The interface has "Code" and "Console" tabs at the top left, "CPP" and a "Run" button at the top right, and line numbers from 1 to 17 in the gutter. The editor contains a function stub and a `main` function for finding the highest temperature in a weekly forecast.*

```cpp
#include <iostream>
#include <vector>

/* Returns highest temperature,
   or -1 if no temperatures given. */
int findPeakHeat(const std::vector<int>& temps) {
    // Your implementation here
}

int main() {
    // High temperatures forecast for the next 7 days.
    std::vector<int> weeklyForecast = {82, 95, 102, 99, 88, 79, 81};

    std::cout << "--- Weather Report ---" << std::endl;
    std::cout << "Max temp this week will be " << findPeakHeat(weeklyForecast) <<
                 std::endl;
    return 0;
}
```

---

## Slide 34: Vectors Don't Reorder Well

Inserting has to shift over elements \
[Open in new tab](https://web.stanford.edu/~pseay/cs106l/vectors-insert)

*Figure: A dark-themed window panel with a QR code on the left. To the right of the QR code is the bold title "Inserting has to shift over elements", the URL `https://web.stanford.edu/~pseay/cs106l/vectors-insert` in a dark text box, and the instructional note "Scan the code or open the URL in a browser to view the live page." The window has three small circular dots (like a macOS window) in the top-left corner. Below this entire panel is an empty dark area.*

```text
Inserting has to shift over elements
https://web.stanford.edu/~pseay/cs106l/vectors-insert
Scan the code or open the URL in a browser to view the live page.
```

Links on this slide:
- <https://web.stanford.edu/~pseay/cs106l/vectors-insert>

---

## Slide 35: Deques

**Double-ended queue** (pronounced "deck")

Like a **vector**, with:
* `push_back`
* `pop_back`

But also has:
* `push_front`
* `pop_front`

*Figure: A photograph of a silver commuter train with red and white striped markings on the front cab, stopped at a station platform under a clear blue sky.*

*Figure: A small decorative illustration of a multi-colored toy train spans the bottom of the slide.*

---

## Slide 36: Deques

Ex: Maintaining a list of the last 10,000 prices

*Figure: A screenshot of a C++ code example in an editor/IDE, demonstrating the use of a `deque` to maintain a list of the last 10,000 prices.*
```cpp
#include <deque>

void receivePrice(deque<double>& prices, double price)
{
    prices.push_front(price);    // Super fast
    if (prices.size() > 10000)
        prices.pop_back();       // Remove last price
                                // so we don't exceed 10k
}
```

---

## Slide 37: Deques Behind the Scenes

How deques are stored behind the scenes [Open in new tab](Open in new tab)

*Figure: A QR code is displayed on the left. To its right, there is a heading "How deques are stored behind the scenes", followed by a URL and an instruction note.*

How deques are stored behind the scenes
https://web.stanford.edu/~pseay/cs106l/deque
Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://web.stanford.edu/~pseay/cs106l/deque>

---

## Slide 38: Plan

1. Space-time
2. STL
3. Sequence Containers
4. **Associative Containers**

---

## Slide 39: Associative Containers

"Associative containers implement **sorted** data structures that can be **quickly searched**."

*Figure: A purple banner at the top with the title "Associative Containers" in white text. Below the title, a white box on the left contains the quoted definition. On the right, a dark blue card labeled "Containers Reference" is shown.*

**Containers Reference**
[https://en.cppreference.com/w/cpp/container.html](https://en.cppreference.com/w/cpp/container.html)
*Scan the code or open the URL in a browser to view the live page.*

*Figure: The reference card includes a QR code to the right of the URL and instructions. A link labeled "Open in new tab" is visible in the top right corner of the card.*

Links on this slide:
- <https://en.cppreference.com/w/cpp/container.html>

---

## Slide 40: Maps

A map "contains key-value pairs with unique keys."

Python calls them "dictionaries"

*Figure: A slide titled "Maps" with two text boxes on the left and a "Containers Reference" link preview card on the right. The card contains a QR code and a URL to the C++ reference for `std::map`.*

**Containers Reference**

[https://en.cppreference.com/w/cpp/container/map.html](https://en.cppreference.com/w/cpp/container/map.html)

Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://en.cppreference.com/w/cpp/container/map.html>

---

## Slide 41: Maps

*Figure: A cartoon pink brain with closed eyes and a peaceful expression is shown in a meditative pose with legs crossed. A light blue circular shape is behind the brain. Two blue arrows point from left to right across the brain: the top arrow connects the text "Sequence Containers" on the left to "Vectors & Deques" on the right, and the bottom arrow connects "Associative Containers" on the left to "Maps & Sets" on the right.*

"Sequence Containers" → "Vectors & Deques"

"Associative Containers" → "Maps & Sets"

---

## Slide 42: Maps

We can do this:

```cpp
std::map<int, char*> adjs;
adjs[106] = "awesome";
adjs[103] = "mathy";
adjs[107] = "deep";

std::cout << adjs[106];
```

How is it efficient?

It sorts the pairs by their keys...

*Figure: A blue arrow points from the question "How is it efficient?" to the last line of the code snippet, `std::cout << adjs[106];`.*

---

## Slide 43: Maps

*Figure: A code editor (IDE) interface with a dark theme. The top banner is purple with the title "Maps". The editor shows tabs for "Code" and "Console" on the top left, and "CPP" with a "Run" button on the top right. Inside the editor, there is C++ code with three purple annotation boxes pointing to specific parts of the code.*

```cpp
#include <map>
#include <iostream>
int main () {
    std::map<int, char> preston {
        {16, 'p'}, {18, 'r'}, {5, 'e'},
        {19, 's'}, {20, 't'}, {15, 'o'}, {14, 'n'}
    };
    for (const auto& pair : preston) {
        std::cout << pair.first << ' '
                  << pair.second << std::endl;
    }
}
```

*Annotation 1 (pointing to the map initialization):* A map is a collection of pairs, so here is uniform initialization of pairs.

*Annotation 2 (pointing to the for loop):* We loop over each pair.

*Annotation 3 (pointing to the bottom of the loop):* The pairs are sorted by key.

---

## Slide 44: Maps

A `std::map<K,V>` is a collection of `std::pair<const K, V>`

*Figure: A code editor screenshot showing a traditional range-based for-loop iterating over a map. The code extracts the key and value using `pair.first` and `pair.second`.*
```cpp
for (const auto& pair : myMap) {
  auto key = pair.first;
  auto value = pair.second;
}
```

⬇️ Structured binding 👍

*Figure: A code editor screenshot showing a modern range-based for-loop using structured binding syntax to directly unpack the key and value from a map.*
```cpp
for (const auto& [key, value] : myMap) {

}
```

---

## Slide 45: Maps Storage - Red Black Trees

*   Stores pairs in a **binary search tree** (BST)
*   Specifically, it uses a **Red-Black Tree**, guaranteeing maximum depth of 2 log (n)
*   This makes search **O(log(n))**

*Figure: A screenshot of a dark-themed web interface or browser window. In the top right corner, there is a link that says "Open in new tab". Below that, there is a QR code on the left and a URL bar on the right containing the link `https://web.stanford.edu/~pseay/cs106l/maps-rbt`. Below the URL bar, the text reads: "Scan the code or open the URL in a browser to view the live page."*

*Figure: A meme from the movie "Cars" showing the character Lightning McQueen (a red race car) on a racetrack with other cars. The text "SPEED. I AM SPEED." is overlaid at the top of the image. The "Cars" movie logo is in the bottom right corner of the meme.*

Links on this slide:
- <https://web.stanford.edu/~pseay/cs106l/maps-rbt>

---

## Slide 46: Maps - Auto Insertion

We can do this:

*Figure: A code editor window displaying a C++ snippet. A dark teal speech bubble with white text sits to the right of line 2, with a blue arrow pointing down toward the usage of a map key. The speech bubble text reads: "Ummmm.... we never defined that???"*

```cpp
std::map<std::string, int> fav_num;
fav_num["Preston"] = 2;

std::cout << "Preston's is " << fav_num["Preston"] <<
    " and Rachel's is " << fav_num["Rachel"] << '\n';
```

*Figure: Two teal rectangular boxes at the bottom of the slide.*

The map automatically inserts the default value of the object.

(It actually does this every time, even on line 2)

---

## Slide 47: Sets

* Amoral maps
* Maps without values
* Unique Objects

### Sets visualizer
*Open in new tab*

*Figure: A screenshot of a web interface titled "Sets visualizer". On the left is a QR code. To the right of the QR code is a link and a text prompt.*

The link provided is:
`https://web.stanford.edu/~pseay/cs106l/sets-rbt`

The instructional text says:
Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://web.stanford.edu/~pseay/cs106l/sets-rbt>

---

## Slide 48: Map Syntax

| What you want to do? | Stanford Map<char, int> | std::map<char, int> |
|----------------------|-------------------------|---------------------|
| Create an empty map | `Map<char, int> m;` | `std::map<char, int> m;` |
| Add key **k** with value **v** into the map | `m.put(k, v);`<br>`m[k] = v;` | `m.insert({k, v});`<br>`m[k] = v;` |
| Remove key **k** from the map | `m.remove(k);` | `m.erase(k);` |
| Check if **k** is in the map<br>(*) C++20 | `if (m.containsKey(k))` | `if (m.count(k))`<br>`if (m.contains(k)) (*)` |
| Check if the map is empty | `if (m.isEmpty())` | `if (m.empty())` |
| Retrieve or overwrite value associated with key **k**<br>(auto-insert default if doesn't exist) | `int i = m[k];`<br>`m[k] = i;` | `int i = m[k];`<br>`m[k] = i;` |

---

## Slide 49: Set Syntax

| What you want to do?               | Stanford Set<char>           | std::set<char>                 |
|------------------------------------|------------------------------|--------------------------------|
| Create an empty set                | `Set<char> s;`               | `std::set<char> s;`            |
| Add k to the set                   | `s.add(k);`                  | `s.insert(k);`                 |
| Remove k from the set              | `s.remove(k);`               | `s.erase(k);`                  |
| Check if k is in the set<br>(* C++20) | `if (s.contains(k))`         | `if (s.count(k))`<br>`if (s.contains(k)) (*)` |
| Check if the set is empty          | `if (s.isEmpty())`           | `if (s.empty())`               |

---

## Slide 50: Practice

**Task:**
Find the double agents -
those who are in multiple
departments.

*Figure: A QR code.*

https://www.online-ide.com/A4IvoxQ8Pr

Links on this slide:
- <https://www.online-ide.com/A4IvoxQ8Pr>

---

## Slide 51: Practice

*Figure: Screenshot of a code editor window with a purple header titled "Practice". The editor interface shows "Code" and "Console" tabs, a "CPP" language indicator, and a "Run" button. The code area displays a C++ program with line numbers 1 through 16 visible in the left gutter.*

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>

std::set<std::string> findDoubleAgents(std::map<std::string, std::set<std::string>> departments) {
    std::set<std::string> seen, doubleAgents;

    // Your code here

    return doubleAgents;
}

int main() {
    std::map<std::string, std::set<std::string>> company = {
```

---

## Slide 52: Associative containers

*Figure: A blue rectangular box containing the text "There are also versions with non-unique keys..."*

### Associative containers
Associative containers implement sorted data structures that can be quickly searched (*O(log n)* complexity).

- **set**: collection of unique keys, sorted by keys  
  (class template)
- **map**: collection of key-value pairs, sorted by keys, keys are unique  
  (class template)
- **multiset**: collection of keys, sorted by keys  
  (class template)
- **multimap**: collection of key-value pairs, sorted by keys  
  (class template)

---

## Slide 53: The Caveat of Associative Containers

"Wait... how do they get sorted?"

### std::map

Defined in header `<map>`
```cpp
template<
    class Key,
    class T,
    class Compare = std::less<Key>,
    class Allocator = std::allocator<std::pair<const Key, T>>
> class map;
```

*Figure: A screenshot showing the template declaration for `std::map`. The template parameters `class Key,` and `class T,` are highlighted with a yellow background. The parameter `class Compare = std::less<Key>,` is highlighted with a green background. A green-bordered box with a light green background to the right contains the text: "This is how... they must be comparable, so it uses the 'less than' comparator by default." The line defining the `class Allocator` parameter has a red horizontal line drawn through it. A red arrow points from this line to the text: "How do we make memory for it?"*

---

## Slide 54: The Caveat of Associative Containers

Not all elements are comparable by default...

*   `int, double, string`
*   `ifstream, Course`

*Figure: A conceptual diagram consisting of four colored text boxes. A wide blue box at the top contains the title "The Caveat of Associative Containers". Below it, a blue box on the left contains the text "Not all elements are comparable by default...". To the right of this, two boxes are stacked vertically: a light green box containing "int, double, string" and a pink box containing "ifstream, Course".*

---

## Slide 55: Plan

1. Space-time
2. STL
3. Sequence Containers
4. **Associative Containers**

---

## Slide 56: Plan

1. Space-time
2. STL
3. Sequence Containers
4. Associative Containers
   * **Bonus - Unordered Associative Containers**

---

## Slide 57: Containers library

The Containers library is a generic collection of clas
implement common data structures like queues, lis
containers:
* sequence containers,
* associative containers,
* unordered associative containers, (since C++11)

*Figure: A horizontal line appears below the title "Containers library". A blue arrow points from the left margin toward a light-blue rectangular box that highlights the third bullet point: "unordered associative containers, (since C++11)".*

---

## Slide 58: Unordered Associative Containers

*Figure: A diagram showing the relationship between ordered and unordered associative containers. On the left are the terms "map" and "set". A blue arrow points from the left to the right, where the terms "unordered_map" and "unordered_set" appear, aligned with their ordered counterparts.*

**map** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **unordered_map**

**set** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **unordered_set**

Essentially optimized versions of map and set.

---

## Slide 59: Unordered Associative Containers

*Figure: A presentation slide comparing two C++ container types. At the top left is a dark code editor window showing a `std::map` declaration. Below it is a similar code editor window showing an `std::unordered_map` declaration. A light blue arrow points from the top code window down to the bottom one. To the right of the arrow is a teal-colored rectangular box.*

```cpp
std::map<int, std::string> courses{
  {103, "Bailey/Aiken"},
  {107, "Cain"},
  {109, "Gregg"}
};
```

*Text inside the teal box:*
Drop-in replacement

```cpp
std::unordered_map<int, std::string> courses{
  {103, "Bailey/Aiken"},
  {107, "Cain"},
  {109, "Gregg"}
};
```

---

## Slide 60: The Caveat - Hashing

### std::unordered_map
Defined in header `<unordered_map>`

```cpp
template<
    class Key,
    class T,
    class Hash = std::hash<Key>,
    class KeyEqual = std::equal_to<Key>,
    class Allocator = std::allocator<std::pair<const Key, T>>
> class unordered_map;
```

*Figure: A screenshot showing the template declaration of the `std::unordered_map` container. A yellow highlight is applied to the `Hash` and `KeyEqual` template parameters and their default values.*

---

## Slide 61: What is a hash function?
*   "Scrambles" a key into a `size_t` (64 bit)
*   Small changes in the input should produce large changes in the output

*Figure: Two diagrams illustrating hash function properties. The top diagram shows the same input string, "CS106L" (in bold), being passed through a function `f(x)` (in a green box) twice, producing the same output number, 80489869 (in purple), each time. Arrows point from each input string into the `f(x)` box and from the box to each output number. The bottom diagram shows the input string "CS106B" (in bold) passed through the same `f(x)` function, producing a different output number, 31580239 (in purple). An arrow points from the input to the box and from the box to the output. Both diagrams are enclosed in rectangular boxes with a drop shadow.*

---

## Slide 62: Unordered Associative Containers

*Figure: Shows two code snippets with an arrow and annotation. The top code block defines a `std::map` named `courses`. A teal box labeled "Drop-in replacement" is positioned between the blocks. A light blue arrow points from the top code block to a bottom code block, which shows the same data structure but defined as an `std::unordered_map`.*

```cpp
std::map<int, std::string> courses{
    {103, "Bailey/Aiken"},
    {107, "Cain"},
    {109, "Gregg"}
};
```

```cpp
std::unordered_map<int, std::string> courses{
    {103, "Bailey/Aiken"},
    {107, "Cain"},
    {109, "Gregg"}
};
```

---

## Slide 63: Unordered Map Implementation

*Figure: A diagram on the left showing a single box labeled "Hash Table".*

*Figure: A screenshot on the right of a web-based visualization tool. The tool has a header "Visualization" and a link "Open in new tab". Inside the interface, it shows the title "Visualization" above a URL field containing a link and a QR code to its left. Below the URL field is instructional text.*

Visualization
Open in new tab
Visualization
`https://web.stanford.edu/~pseay/cs106l/hash-map`
Scan the code or open the URL in a browser to view the live page.

Links on this slide:
- <https://web.stanford.edu/~pseay/cs106l/hash-map>

---

## Slide 64: Speed

*Figure: A slide titled "Speed" on a purple banner. The slide compares the search/lookup speeds of different data structures using imagery from the movie "Cars". On the left, a poster titled "Cars: Low & Slow" is positioned above a box labeled "Vectors" with the complexity $O(n)$. In the center and right, a large image featuring Lightning McQueen and Mater is positioned above two boxes: one labeled "Maps" with the complexity $O(\log(n))$ and one labeled "Unordered Maps" with the complexity $O(1)$.*

| Container | Complexity |
| :--- | :--- |
| **Vectors** | *O(n)* |
| **Maps** | *O(log(n))* |
| **Unordered Maps** | *O(1)* |

---

## Slide 65: Recap

*Figure: A centered rectangular box containing the text "Recap".*

---

## Slide 66: Summary of Data Structures

*Figure: A vertical arrow on the left, pointing downward, with the label "Space per Element" written vertically along it. This arrow is next to a table, indicating that the data structures listed lower in the table use more memory per element.*

| | i<sup>th</sup> element | Search | Insertion | Erase |
| :--- | :---: | :---: | :---: | :---: |
| **std::vector** | Very Fast | Slow | Slow | Slow |
| **std::deque** | Fast | Slow | Fast (front/back) <br> Slow (all others) | Fast (front/back) <br> Slow (all others) |
| **std::set** | Slow | Fast | Fast | Fast |
| **std::map** | Slow | Fast | Fast | Fast |
| **std::unordered_set** | N/A | Very Fast | Very Fast | Very Fast |
| **std::unordered_map** | N/A | Very Fast | Very Fast | Very Fast |

---

## Slide 67: More Data Structures = More Fun

### Sequence containers
Sequence containers implement data structures which can be accessed sequentially.

- `array (C++11)`: fixed-sized inplace contiguous array (class template)
- `vector`: resizable contiguous array (class template)
- `inplace_vector (C++26)`: resizable, fixed capacity, inplace contiguous array (class template)
- `hive (C++26)`: collection that reuses erased elements' memory (class template)
- `deque`: double-ended queue (class template)
- `forward_list (C++11)`: singly-linked list (class template)
- `list`: doubly-linked list (class template)

### Container adaptors
Container adaptors provide a different interface for sequential containers.

- `stack`: adapts a container to provide stack (LIFO data structure) (class template)
- `queue`: adapts a container to provide queue (FIFO data structure) (class template)
- `priority_queue`: adapts a container to provide priority queue (class template)
- `flat_set (C++23)`: adapts a container to provide a collection of unique keys, sorted by keys (class template)
- `flat_map (C++23)`: adapts two containers to provide a collection of key-value pairs, sorted by unique keys (class template)
- `flat_multiset (C++23)`: adapts a container to provide a collection of keys, sorted by keys (class template)
- `flat_multimap (C++23)`: adapts two containers to provide a collection of key-value pairs, sorted by keys (class template)

### Associative containers
Associative containers implement sorted data structures that can be quickly searched (O(log n) complexity).

- `set`: collection of unique keys, sorted by keys (class template)
- `map`: collection of key-value pairs, sorted by keys, keys are unique (class template)
- `multiset`: collection of keys, sorted by keys (class template)
- `multimap`: collection of key-value pairs, sorted by keys (class template)

### Unordered associative containers (since C++11)
Unordered associative containers implement unsorted (hashed) data structures that can be quickly searched (O(1) average, O(n) worst-case complexity).

- `unordered_set (C++11)`: collection of unique keys, hashed by keys (class template)
- `unordered_map (C++11)`: collection of key-value pairs, hashed by keys, keys are unique (class template)
- `unordered_multiset (C++11)`: collection of keys, hashed by keys (class template)
- `unordered_multimap (C++11)`: collection of key-value pairs, hashed by keys (class template)

*Figure: A slide layout with a purple banner title. Four main sections list C++ containers: Sequence containers, Container adaptors, Associative containers, and Unordered associative containers. Each container entry features a name in a colored background (gray, green, pink, or yellow), a brief description, and a note indicating it is a class template. Version tags (e.g., C++11, C++23, C++26) appear next to applicable container names. A bordered box in the bottom-right corner contains the text "cppreference.com".*

Links on this slide:
- <https://en.cppreference.com/w/cpp/container.html>

---

## Slide 68: Summary

1. **Space-time**
   - Tradeoffs
2. **STL**
   - Standard Template Library
3. **Sequence Containers**
   - Ex: `vector`, `deque`, ...
4. **(Unordered) Associative Containers**
   - Ex: `(unordered_)` `map`, `set`, ...
