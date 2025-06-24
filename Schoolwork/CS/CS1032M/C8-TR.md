# Key Terms and Results

## Terms
- **recurrence relation**: a formula expressing terms of a sequence, except for some initial terms, as a function of one or more previous terms of the sequence.
- **initial conditions for a recurrence relation**: the values of the terms of a sequence satisfying the recurrence relation before this relation takes effect.
- **dynamic programming**: an algorithmic paradigm that finds the solution to an optimization problem by recursively breaking down the problem into overlapping subproblems and combining their solutions with the help of a recurrence relation.
- **linear homogeneous recurrence relation with constant coefficients**: a recurrence relation that expresses the terms of a sequence, except initial terms, as a linear combination of previous terms.
- **characteristic roots of a linear homogeneous recurrence relation with constant coefficients**: the roots of the polynomial associated with a linear homogeneous recurrence relation with constant coefficients.
- **linear nonhomogeneous recurrence relation with constant coefficients**: a recurrence relation that expresses the terms of a sequence, except for initial terms, as a linear combination of previous terms plus a function that is not identically zero that depends only on the index.
- **divide-and-conquer algorithm**: an algorithm that solves a problem recursively by splitting it into a fixed number of smaller nonoverlapping subproblems of the same type.
- **generating function of a sequence**: the formal series that has the $n$-th term of the sequence as the coefficient of $x^n$.
- **sieve of Eratosthenes**: a procedure for finding the primes less than a specified positive integer.
- **derangement**: a permutation of objects such that no object is in its original place.

## Results
- **The formula for the number of elements in the union of two finite sets**:
  $$
  |A \cup B| = |A| + |B| - |A \cap B|
  $$
- **The formula for the number of elements in the union of three finite sets**:
  $$
  |A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|
  $$
- **The principle of inclusion–exclusion**:
  $$
  |A_1 \cup A_2 \cup \cdots \cup A_n| = \sum_{1 \leq i \leq n} |A_i| - \sum_{1 \leq i < j \leq n} |A_i \cap A_j| + \sum_{1 \leq i < j < k \leq n} |A_i \cap A_j \cap A_k| - \cdots + (-1)^{n+1} |A_1 \cap A_2 \cap \cdots \cap A_n|
  $$
- **The number of onto functions from a set with $m$ elements to a set with $n$ elements**:
  $$
  n^m - \binom{n}{1}(n - 1)^m + \binom{n}{2}(n - 2)^m - \cdots + (-1)^{n-1} \binom{n}{n - 1} \cdot 1^m
  $$
- **The number of derangements of $n$ objects**:
  $$
  D_n = n! \left[ 1 - \frac{1}{1!} + \frac{1}{2!} - \cdots + (-1)^n \frac{1}{n!} \right]
  $$



# CN

## Terms
- **recurrence relation**: a formula expressing terms of a sequence, except for some initial terms, as a function of one or more previous terms of the sequence.  
- **递归关系**：一种公式，用来表示序列中除初始项之外的项是序列中一个或多个前面项的函数。

- **initial conditions for a recurrence relation**: the values of the terms of a sequence satisfying the recurrence relation before this relation takes effect.  
- **递归关系的初始条件**：序列中满足递归关系的项在关系生效之前的值。

- **dynamic programming**: an algorithmic paradigm that finds the solution to an optimization problem by recursively breaking down the problem into overlapping subproblems and combining their solutions with the help of a recurrence relation.  
- **动态规划**：一种算法范式，通过递归地将优化问题分解为重叠的子问题，并借助递归关系将子问题的解组合起来，从而找到问题的解。

- **linear homogeneous recurrence relation with constant coefficients**: a recurrence relation that expresses the terms of a sequence, except initial terms, as a linear combination of previous terms.  
- **常系数线性齐次递归关系**：一种递归关系，用来表示序列中除初始项之外的项是前面项的线性组合。

- **characteristic roots of a linear homogeneous recurrence relation with constant coefficients**: the roots of the polynomial associated with a linear homogeneous recurrence relation with constant coefficients.  
- **常系数线性齐次递归关系的特征根**：与常系数线性齐次递归关系相关的多项式的根。

- **linear nonhomogeneous recurrence relation with constant coefficients**: a recurrence relation that expresses the terms of a sequence, except initial terms, as a linear combination of previous terms plus a function that is not identically zero that depends only on the index.  
- **常系数线性非齐次递归关系**：一种递归关系，用来表示序列中除初始项之外的项是前面项的线性组合加上一个仅依赖于索引的非零函数。

- **divide-and-conquer algorithm**: an algorithm that solves a problem recursively by splitting it into a fixed number of smaller nonoverlapping subproblems of the same type.  
- **分治算法**：一种通过将问题递归地分解为固定数量的相同类型的较小不重叠子问题来解决问题的算法。

- **generating function of a sequence**: the formal series that has the $n$-th term of the sequence as the coefficient of $x^n$.  
- **序列的生成函数**：形式级数，其中序列的第 $n$ 项是 $x^n$ 的系数。

- **sieve of Eratosthenes**: a procedure for finding the primes less than a specified positive integer.  
- **埃拉托斯特尼筛法**：一种用于找出小于指定正整数的所有素数的程序。

- **derangement**: a permutation of objects such that no object is in its original place.  
- **错排**：一种排列，使得没有任何一个对象处于其原始位置。

## Results
- **The formula for the number of elements in the union of two finite sets**:  
  $$
  |A \cup B| = |A| + |B| - |A \cap B|
  $$  
- **两个有限集合并集的元素个数公式**：  
  $$
  |A \cup B| = |A| + |B| - |A \cap B|
  $$

- **The formula for the number of elements in the union of three finite sets**:  
  $$
  |A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|
  $$  
- **三个有限集合并集的元素个数公式**：  
  $$
  |A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|
  $$

- **The principle of inclusion–exclusion**:  
  $$
  |A_1 \cup A_2 \cup \cdots \cup A_n| = \sum_{1 \leq i \leq n} |A_i| - \sum_{1 \leq i < j \leq n} |A_i \cap A_j| + \sum_{1 \leq i < j < k \leq n} |A_i \cap A_j \cap A_k| - \cdots + (-1)^{n+1} |A_1 \cap A_2 \cap \cdots \cap A_n|
  $$  
- **容斥原理**：  
  $$
  |A_1 \cup A_2 \cup \cdots \cup A_n| = \sum_{1 \leq i \leq n} |A_i| - \sum_{1 \leq i < j \leq n} |A_i \cap A_j| + \sum_{1 \leq i < j < k \leq n} |A_i \cap A_j \cap A_k| - \cdots + (-1)^{n+1} |A_1 \cap A_2 \cap \cdots \cap A_n|
  $$

- **The number of onto functions from a set with $m$ elements to a set with $n$ elements**:  
  $$
  n^m - \binom{n}{1}(n - 1)^m + \binom{n}{2}(n - 2)^m - \cdots + (-1)^{n-1} \binom{n}{n - 1} \cdot 1^m
  $$  
- **从一个有 $m$ 个元素的集合到一个有 $n$ 个元素的集合的满射函数的个数**：  
  $$
  n^m - \binom{n}{1}(n - 1)^m + \binom{n}{2}(n - 2)^m - \cdots + (-1)^{n-1} \binom{n}{n - 1} \cdot 1^m
  $$

- **The number of derangements of $n$ objects**:  
  $$
  D_n = n! \left[ 1 - \frac{1}{1!} + \frac{1}{2!} - \cdots + (-1)^n \frac{1}{n!} \right]
  $$  
- **$n$ 个对象的错排数**：  
  $$
  D_n = n! \left[ 1 - \frac{1}{1!} + \frac{1}{2!} - \cdots + (-1)^n \frac{1}{n!} \right]
  $$