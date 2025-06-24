# Key Terms and Results

## Terms

- **Combinatorics**: The study of arrangements of objects.
- **Enumeration**: The counting of arrangements of objects.
- **Tree diagram**: A diagram made up of a root, branches leaving the root, and other branches leaving some of the endpoints of branches.
- **Permutation**: An ordered arrangement of the elements of a set.
- **r-permutation**: An ordered arrangement of $r$ elements of a set.
- **P(n,r)**: The number of $r$-permutations of a set with $n$ elements.
- **r-combination**: An unordered selection of $r$ elements of a set.
- **C(n,r)**: The number of $r$-combinations of a set with $n$ elements.
- **Binomial coefficient $\binom{n}{r}$**: Also the number of $r$-combinations of a set with $n$ elements.
- **Combinatorial proof**: A proof that uses counting arguments rather than algebraic manipulation to prove a result.
- **Pascal's triangle**: A representation of the binomial coefficients where the $i$-th row of the triangle contains $\binom{i}{j}$ for $j = 0, 1, 2, \ldots, i$.
- **S(n, j)**: The Stirling number of the second kind denoting the number of ways to distribute $n$ distinguishable objects into $j$ indistinguishable boxes so that no box is empty.

## Results

- **Product rule for counting**: The number of ways to do a procedure that consists of two tasks is the product of the number of ways to do the first task and the number of ways to do the second task after the first task has been done.
- **Product rule for sets**: The number of elements in the Cartesian product of finite sets is the product of the number of elements in each set.
- **Sum rule for counting**: The number of ways to do a task in one of two ways is the sum of the number of ways to do these tasks if they cannot be done simultaneously.
- **Sum rule for sets**: The number of elements in the union of pairwise disjoint finite sets is the sum of the numbers of elements in these sets.
- **Subtraction rule for counting or inclusion–exclusion for sets**: If a task can be done in either $n_1$ ways or $n_2$ ways, then the number of ways to do the task is $n_1 + n_2$ minus the number of ways to do the task that are common to the two different ways.
- **Subtraction rule or inclusion–exclusion for sets**: The number of elements in the union of two sets is the sum of the number of elements in these sets minus the number of elements in their intersection.
- **Division rule for counting**: There are $\frac{n}{d}$ ways to do a task if it can be done using a procedure that can be carried out in $n$ ways, and for every way $w$, exactly $d$ of the $n$ ways correspond to way $w$.
- **Division rule for sets**: Suppose that a finite set $A$ is the union of $n$ disjoint subsets each with $d$ elements. Then $n = \frac{|A|}{d}$.
- **The pigeonhole principle**: When more than $k$ objects are placed in $k$ boxes, there must be a box containing more than one object.
- **The generalized pigeonhole principle**: When $N$ objects are placed in $k$ boxes, there must be a box containing at least $\lceil \frac{N}{k} \rceil$ objects.
- **Permutations and combinations formulas**:
  - $P(n, r) = \frac{n!}{(n - r)!}$
  - $C(n, r) = \binom{n}{r} = \frac{n!}{r!(n - r)!}$
- **Pascal's identity**: $\binom{n+1}{k} = \binom{n}{k-1} + \binom{n}{k}$
- **The binomial theorem**: $(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k} y^k$
- **Permutations with repetition**:
  - There are $n^r$ $r$-permutations of a set with $n$ elements when repetition is allowed.
  - There are $\binom{n + r - 1}{r}$ $r$-combinations of a set with $n$ elements when repetition is allowed.
- **Permutations of objects of different types**: There are $\frac{n!}{n_1! n_2! \cdots n_k!}$ permutations of $n$ objects of $k$ types where there are $n_i$ indistinguishable objects of type $i$ for $i = 1, 2, 3, \ldots, k$.
- **Algorithm for generating permutations**: An algorithm for generating the permutations of the set $\{1, 2, \ldots, n\}$.


# CN

## Terms

- **Combinatorics**: The study of arrangements of objects.  
- **组合数学**：研究对象的排列组合。

- **Enumeration**: The counting of arrangements of objects.  
- **计数**：对对象排列组合的计数。

- **Tree diagram**: A diagram made up of a root, branches leaving the root, and other branches leaving some of the endpoints of branches.  
- **树状图**：由根节点、从根节点出发的分支以及从某些分支端点出发的其他分支组成的图。

- **Permutation**: An ordered arrangement of the elements of a set.  
- **排列**：集合元素的有序排列。

- **r-permutation**: An ordered arrangement of $r$ elements of a set.  
- **r-排列**：集合中 $r$ 个元素的有序排列。

- **P(n,r)**: The number of $r$-permutations of a set with $n$ elements.  
- **P(n,r)**：一个包含 $n$ 个元素的集合的 $r$-排列的数量。

- **r-combination**: An unordered selection of $r$ elements of a set.  
- **r-组合**：集合中 $r$ 个元素的无序选择。

- **C(n,r)**: The number of $r$-combinations of a set with $n$ elements.  
- **C(n,r)**：一个包含 $n$ 个元素的集合的 $r$-组合的数量。

- **Binomial coefficient $\binom{n}{r}$**: Also the number of $r$-combinations of a set with $n$ elements.  
- **二项式系数 $\binom{n}{r}$**：也是包含 $n$ 个元素的集合的 $r$-组合的数量。

- **Combinatorial proof**: A proof that uses counting arguments rather than algebraic manipulation to prove a result.  
- **组合证明**：一种通过计数论证而不是代数运算来证明结果的证明方法。

- **Pascal's triangle**: A representation of the binomial coefficients where the $i$-th row of the triangle contains $\binom{i}{j}$ for $j = 0, 1, 2, \ldots, i$.  
- **帕斯卡三角形**：表示二项式系数的一种形式，其中三角形的第 $i$ 行包含 $\binom{i}{j}$（$j = 0, 1, 2, \ldots, i$）。

- **S(n, j)**: The Stirling number of the second kind denoting the number of ways to distribute $n$ distinguishable objects into $j$ indistinguishable boxes so that no box is empty.  
- **S(n, j)**：第二类斯特林数，表示将 $n$ 个可区分的对象分配到 $j$ 个不可区分的盒子中，且每个盒子都不为空的方法数。

## Results

- **Product rule for counting**: The number of ways to do a procedure that consists of two tasks is the product of the number of ways to do the first task and the number of ways to do the second task after the first task has been done.  
- **乘法规则（计数）**：完成一个由两个任务组成的程序的方法数是完成第一个任务的方法数与完成第一个任务后第二个任务的方法数的乘积。

- **Product rule for sets**: The number of elements in the Cartesian product of finite sets is the product of the number of elements in each set.  
- **集合的乘法规则**：有限集合的笛卡尔积的元素数量是每个集合的元素数量的乘积。

- **Sum rule for counting**: The number of ways to do a task in one of two ways is the sum of the number of ways to do these tasks if they cannot be done simultaneously.  
- **加法规则（计数）**：以两种方式之一完成一项任务的方法数是完成这些任务的方法数之和，前提是这两种方式不能同时进行。

- **Sum rule for sets**: The number of elements in the union of pairwise disjoint finite sets is the sum of the numbers of elements in these sets.  
- **集合的加法规则**：成对不相交的有限集合的并集的元素数量是这些集合的元素数量之和。

- **Subtraction rule for counting or inclusion–exclusion for sets**: If a task can be done in either $n_1$ ways or $n_2$ ways, then the number of ways to do the task is $n_1 + n_2$ minus the number of ways to do the task that are common to the two different ways.  
- **减法规则（计数）或集合的包含-排除原理**：如果一个任务可以用 $n_1$ 种方法或 $n_2$ 种方法完成，那么完成这个任务的方法数是 $n_1 + n_2$ 减去这两种不同方法的共同方法数。

- **Subtraction rule or inclusion–exclusion for sets**: The number of elements in the union of two sets is the sum of the number of elements in these sets minus the number of elements in their intersection.  
- **集合的减法规则或包含-排除原理**：两个集合的并集的元素数量是这两个集合的元素数量之和减去它们交集的元素数量。

- **Division rule for counting**: There are $\frac{n}{d}$ ways to do a task if it can be done using a procedure that can be carried out in $n$ ways, and for every way $w$, exactly $d$ of the $n$ ways correspond to way $w$.  
- **除法规则（计数）**：如果一个任务可以用 $n$ 种方法完成，并且对于每种方法 $w$，恰好有 $d$ 种方法对应于方法 $w$，那么完成这个任务的方法数是 $\frac{n}{d}$。

- **Division rule for sets**: Suppose that a finite set $A$ is the union of $n$ disjoint subsets each with $d$ elements. Then $n = \frac{|A|}{d}$.  
- **集合的除法规则**：假设有限集合 $A$ 是 $n$ 个不相交的子集的并集，每个子集有 $d$ 个元素，那么 $n = \frac{|A|}{d}$。

- **The pigeonhole principle**: When more than $k$ objects are placed in $k$ boxes, there must be a box containing more than one object.  
- **鸽巢原理**：当超过 $k$ 个对象放入 $k$ 个盒子中时，必定有一个盒子包含多于一个对象。

- **The generalized pigeonhole principle**: When $N$ objects are placed in $k$ boxes, there must be a box containing at least $\lceil \frac{N}{k} \rceil$ objects.  
- **广义鸽巢原理**：当 $N$ 个对象放入 $k$ 个盒子中时，必定有一个盒子包含至少 $\lceil \frac{N}{k} \rceil$ 个对象。

- **Permutations and combinations formulas**:
  - $P(n, r) = \frac{n!}{(n - r)!}$
  - $C(n, r) = \binom{n}{r} = \frac{n!}{r!(n - r)!}$
- **排列与组合公式**：
  - $P(n, r) = \frac{n!}{(n - r)!}$
  - $C(n, r) = \binom{n}{r} = \frac{n!}{r!(n - r)!}$

- **Pascal's identity**: $\binom{n+1}{k} = \binom{n}{k-1} + \binom{n}{k}$  
- **帕斯卡恒等式**：$\binom{n+1}{k} = \binom{n}{k-1} + \binom{n}{k}$

- **The binomial theorem**: $(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k} y^k$  
- **二项式定理**：$(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k} y^k$

- **Permutations with repetition**:
  - There are $n^r$ $r$-permutations of a set with $n$ elements when repetition is allowed.
  - There are $\binom{n + r - 1}{r}$ $r$-combinations of a set with $n$ elements when repetition is allowed.
- **带重复的排列**：
  - 当允许重复时，一个包含 $n$ 个元素的集合的 $r$-排列的数量为 $n^r$。
  - 当允许重复时，一个包含 $n$ 个元素的集合的 $r$-组合的数量为 $\binom{n + r - 1}{r}$。

- **Permutations of objects of different types**: There are $\frac{n!}{n_1! n_2! \cdots n_k!}$ permutations of $n$ objects of $k$ types where there are $n_i$ indistinguishable objects of type $i$ for $i = 1, 2, 3, \ldots, k$.  
- **不同类型对象的排列**：对于 $k$ 种类型的 $n$ 个对象，其中第 $i$ 种类型有 $n_i$ 个不可区分的对象（$i = 1, 2, 3, \ldots, k$），其排列数为 $\frac{n!}{n_1! n_2! \cdots n_k!}$。

- **Algorithm for generating permutations**: An algorithm for generating the permutations of the set $\{1, 2, \ldots, n\}$.  
- **生成排列的算法**：生成集合 $\{1, 2, \ldots, n\}$ 的排列的算法。