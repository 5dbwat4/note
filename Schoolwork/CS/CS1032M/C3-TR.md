

## Key Terms and Results

### TERMS
- **algorithm**: a finite sequence of precise instructions for performing a computation or solving a problem.
- **searching algorithm**: the problem of locating an element in a list.
- **linear search algorithm**: a procedure for searching a list element by element.
- **binary search algorithm**: a procedure for searching an ordered list by successively splitting the list in half.
- **sorting**: the reordering of the elements of a list into prescribed order.
- **string searching**: given a string, determining all the occurrences where this string occurs within a longer string.
- **f(x) is $O(g(x))$**: the fact that $|f(x)| \leq C|g(x)|$ for all $x > k$ for some constants $C$ and $k$.
- **witness to the relationship $f(x)$ is $O(g(x))$**: a pair $C$ and $k$ such that $|f(x)| \leq C|g(x)|$ whenever $x > k$.
- **f(x) is $\Omega(g(x))$**: the fact that $|f(x)| \geq C|g(x)|$ for all $x > k$ for some positive constants $C$ and $k$.
- **f(x) is $\Theta(g(x))$**: the fact that $f(x)$ is both $O(g(x))$ and $\Omega(g(x))$.
- **time complexity**: the amount of time required for an algorithm to solve a problem.
- **space complexity**: the amount of space in computer memory required for an algorithm to solve a problem.
- **worst-case time complexity**: the greatest amount of time required for an algorithm to solve a problem of a given size.
- **average-case time complexity**: the average amount of time required for an algorithm to solve a problem of a given size.
- **algorithmic paradigm**: a general approach for constructing algorithms based on a particular concept.
- **brute force**: the algorithmic paradigm based on constructing algorithms for solving problems in a naive manner from the statement of the problem and definitions.
- **greedy algorithm**: an algorithm that makes the best choice at each step according to some specified condition.
- **tractable problem**: a problem for which there is a worst-case polynomial-time algorithm that solves it.
- **intractable problem**: a problem for which no worst-case polynomial-time algorithm exists for solving it.
- **solvable problem**: a problem that can be solved by an algorithm.
- **unsolvable problem**: a problem that cannot be solved by an algorithm.

### RESULTS
- **Linear and binary search algorithms**: (given in Section 3.1)
- **Bubble sort**: a sorting that uses passes where successive items are interchanged if they are in the wrong order.
- **Insertion sort**: a sorting that at the $j$th step inserts the $j$th element into the correct position in the list, when the first $j - 1$ elements of the list are already sorted.
- The linear search has $O(n)$ worst-case time complexity.
- The binary search has $O(\log n)$ worst-case time complexity.
- The bubble and insertion sorts have $O(n^2)$ worst-case time complexity.
- $\log n!$ is $O(n \log n)$.
- If $f_1(x)$ is $O(g_1(x))$ and $f_2(x)$ is $O(g_2(x))$, then $(f_1 + f_2)(x)$ is $O(\max(g_1(x), g_2(x)))$ and $(f_1 f_2)(x)$ is $O((g_1 g_2)(x))$.
- If $a_0, a_1, \ldots, a_n$ are real numbers with $a_n \neq 0$, then $a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$ is $\Theta(x^n)$, and hence $O(n)$ and $\Omega(n)$.


## CN

### Key Terms

- **algorithm**: a finite sequence of precise instructions for performing a computation or solving a problem.  
- **算法**：用于执行计算或解决问题的一组有限的精确指令。

- **searching algorithm**: the problem of locating an element in a list.  
- **搜索算法**：在列表中查找一个元素的问题。

- **linear search algorithm**: a procedure for searching a list element by element.  
- **线性搜索算法**：逐个元素搜索列表的过程。

- **binary search algorithm**: a procedure for searching an ordered list by successively splitting the list in half.  
- **二分搜索算法**：通过不断将有序列表分成两半来搜索的过程。

- **sorting**: the reordering of the elements of a list into prescribed order.  
- **排序**：将列表的元素重新排列成规定的顺序。

- **string searching**: given a string, determining all the occurrences where this string occurs within a longer string.  
- **字符串搜索**：给定一个字符串，确定它在一个更长的字符串中出现的所有位置。

- **f(x) is $O(g(x))$**: the fact that $|f(x)| \leq C|g(x)|$ for all $x > k$ for some constants $C$ and $k$.  
- **f(x) 是 $O(g(x))$**：存在常数 $C$ 和 $k$，使得对于所有 $x > k$，有 $|f(x)| \leq C|g(x)|$。

- **witness to the relationship $f(x)$ is $O(g(x))$**: a pair $C$ and $k$ such that $|f(x)| \leq C|g(x)|$ whenever $x > k$.  
- **证明 $f(x)$ 是 $O(g(x))$ 的关系的证据**：一对常数 $C$ 和 $k$，使得当 $x > k$ 时，有 $|f(x)| \leq C|g(x)|$。

- **f(x) is $\Omega(g(x))$**: the fact that $|f(x)| \geq C|g(x)|$ for all $x > k$ for some positive constants $C$ and $k$.  
- **f(x) 是 $\Omega(g(x))$**：存在正的常数 $C$ 和 $k$，使得对于所有 $x > k$，有 $|f(x)| \geq C|g(x)|$。

- **f(x) is $\Theta(g(x))$**: the fact that $f(x)$ is both $O(g(x))$ and $\Omega(g(x))$.  
- **f(x) 是 $\Theta(g(x))$**：$f(x)$ 既是 $O(g(x))$ 又是 $\Omega(g(x))$。

- **time complexity**: the amount of time required for an algorithm to solve a problem.  
- **时间复杂度**：算法解决问题所需的时间。

- **space complexity**: the amount of space in computer memory required for an algorithm to solve a problem.  
- **空间复杂度**：算法解决问题所需的计算机内存空间。

- **worst-case time complexity**: the greatest amount of time required for an algorithm to solve a problem of a given size.  
- **最坏情况时间复杂度**：算法解决给定大小问题所需的最长时间。

- **average-case time complexity**: the average amount of time required for an algorithm to solve a problem of a given size.  
- **平均情况时间复杂度**：算法解决给定大小问题所需的平均时间。

- **algorithmic paradigm**: a general approach for constructing algorithms based on a particular concept.  
- **算法范式**：基于特定概念构建算法的通用方法。

- **brute force**: the algorithmic paradigm based on constructing algorithms for solving problems in a naive manner from the statement of the problem and definitions.  
- **穷举法**：根据问题的陈述和定义，以一种简单直接的方式构建算法的范式。

- **greedy algorithm**: an algorithm that makes the best choice at each step according to some specified condition.  
- **贪心算法**：根据某些特定条件，在每一步都做出最优选择的算法。

- **tractable problem**: a problem for which there is a worst-case polynomial-time algorithm that solves it.  
- **易解问题**：存在一个最坏情况下多项式时间算法可以解决的问题。

- **intractable problem**: a problem for which no worst-case polynomial-time algorithm exists for solving it.  
- **难解问题**：不存在一个最坏情况下多项式时间算法可以解决的问题。

- **solvable problem**: a problem that can be solved by an algorithm.  
- **可解问题**：可以用算法解决的问题。

- **unsolvable problem**: a problem that cannot be solved by an algorithm.  
- **不可解问题**：无法用算法解决的问题。

### Results

- **Linear and binary search algorithms**: (given in Section 3.1)  
- **线性搜索和二分搜索算法**：（见第3.1节）

- **Bubble sort**: a sorting that uses passes where successive items are interchanged if they are in the wrong order.  
- **冒泡排序**：通过多次遍历列表，如果相邻元素顺序错误则交换它们的排序方法。

- **Insertion sort**: a sorting that at the $j$th step inserts the $j$th element into the correct position in the list, when the first $j - 1$ elements of the list are already sorted.  
- **插入排序**：在第 $j$ 步时，将第 $j$ 个元素插入到列表中正确的位置，此时列表的前 $j - 1$ 个元素已经排序。

- The linear search has $O(n)$ worst-case time complexity.  
- 线性搜索的最坏情况时间复杂度为 $O(n)$。

The binary search has $O(\log n)$ worst-case time complexity.  
二分搜索的最坏情况时间复杂度为 $O(\log n)$。

The bubble and insertion sorts have $O(n^2)$ worst-case time complexity.  
冒泡排序和插入排序的最坏情况时间复杂度为 $O(n^2)$。

$\log n!$ is $O(n \log n)$.  
$\log n!$ 是 $O(n \log n)$。

If $f_1(x)$ is $O(g_1(x))$ and $f_2(x)$ is $O(g_2(x))$, then $(f_1 + f_2)(x)$ is $O(\max(g_1(x), g_2(x)))$ and $(f_1 f_2)(x)$ is $O((g_1 g_2)(x))$.  
如果 $f_1(x)$ 是 $O(g_1(x))$ 且 $f_2(x)$ 是 $O(g_2(x))$，那么 $(f_1 + f_2)(x)$ 是 $O(\max(g_1(x), g_2(x)))$，而 $(f_1 f_2)(x)$ 是 $O((g_1 g_2)(x))$。

If $a_0, a_1, \ldots, a_n$ are real numbers with $a_n \neq 0$, then $a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$ is $\Theta(x^n)$, and hence $O(n)$ and $\Omega(n)$.  
如果 $a_0, a_1, \ldots, a_n$ 是实数且 $a_n \neq 0$，那么 $a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$ 是 $\Theta(x^n)$，因此也是 $O(n)$ 和 $\Omega(n)$。