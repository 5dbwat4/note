# Key Terms and Results

## TERMS

- **sequence**: a function with domain that is a subset of the set of integers
- **geometric progression**: a sequence of the form $a, ar, ar^2, \ldots$, where $a$ and $r$ are real numbers
- **arithmetic progression**: a sequence of the form $a, a + d, a + 2d, \ldots$, where $a$ and $d$ are real numbers
- **the principle of mathematical induction**: The statement $\forall n P(n)$ is true if $P(1)$ is true and $\forall k [P(k) \rightarrow P(k+1)]$ is true.
  - **basis step**: the proof of $P(1)$ in a proof by mathematical induction of $\forall n P(n)$
  - **inductive step**: the proof of $P(k) \rightarrow P(k+1)$ for all positive integers $k$ in a proof by mathematical induction of $\forall n P(n)$
- **strong induction**: The statement $\forall n P(n)$ is true if $P(1)$ is true and $\forall k [(P(1) \wedge \cdots \wedge P(k)) \rightarrow P(k+1)]$ is true.
- **well-ordering property**: Every nonempty set of nonnegative integers has a least element.
- **recursive definition of a function**: a definition of a function that specifies an initial set of values and a rule for obtaining values of this function at integers from its values at smaller integers
- **recursive definition of a set**: a definition of a set that specifies an initial set of elements in the set and a rule for obtaining other elements from those in the set
- **structural induction**: a technique for proving results about recursively defined sets
- **recursive algorithm**: an algorithm that proceeds by reducing a problem to the same problem with smaller input
- **merge sort**: a sorting algorithm that sorts a list by splitting it in two, sorting each of the two resulting lists, and merging the results into a sorted list
- **iteration**: a procedure based on the repeated use of operations in a loop
- **program correctness**: verification that a procedure always produces the correct result
- **loop invariant**: a property that remains true during every traversal of a loop
- **initial assertion**: the statement specifying the properties of the input values of a program
- **final assertion**: the statement specifying the properties the output values should have if the program worked correctly



# CN


- **sequence**: a function with domain that is a subset of the set of integers  
- **序列**：定义域是整数集合的子集的函数。

- **geometric progression**: a sequence of the form \(a, ar, ar^2, \ldots\), where \(a\) and \(r\) are real numbers  
- **几何级数**：形式为 \(a, ar, ar^2, \ldots\) 的序列，其中 \(a\) 和 \(r\) 是实数。

- **arithmetic progression**: a sequence of the form \(a, a + d, a + 2d, \ldots\), where \(a\) and \(d\) are real numbers  
- **等差级数**：形式为 \(a, a + d, a + 2d, \ldots\) 的序列，其中 \(a\) 和 \(d\) 是实数。

- **the principle of mathematical induction**: The statement \(\forall n P(n)\) is true if \(P(1)\) is true and \(\forall k [P(k) \rightarrow P(k+1)]\) is true.  
- **数学归纳法原理**：如果 \(P(1)\) 为真，并且对于所有正整数 \(k\)，\(P(k) \rightarrow P(k+1)\) 为真，则陈述 \(\forall n P(n)\) 为真。

  - **basis step**: the proof of \(P(1)\) in a proof by mathematical induction of \(\forall n P(n)\)  
  - **基础步骤**：在数学归纳法证明 \(\forall n P(n)\) 中对 \(P(1)\) 的证明。

  - **inductive step**: the proof of \(P(k) \rightarrow P(k+1)\) for all positive integers \(k\) in a proof by mathematical induction of \(\forall n P(n)\)  
  - **归纳步骤**：在数学归纳法证明 \(\forall n P(n)\) 中对所有正整数 \(k\) 的 \(P(k) \rightarrow P(k+1)\) 的证明。

- **strong induction**: The statement \(\forall n P(n)\) is true if \(P(1)\) is true and \(\forall k [(P(1) \wedge \cdots \wedge P(k)) \rightarrow P(k+1)]\) is true.  
- **强归纳法**：如果 \(P(1)\) 为真，并且对于所有正整数 \(k\)，\((P(1) \wedge \cdots \wedge P(k)) \rightarrow P(k+1)\) 为真，则陈述 \(\forall n P(n)\) 为真。

- **well-ordering property**: Every nonempty set of nonnegative integers has a least element.  
- **良序性质**：每一个非空的非负整数集合都有一个最小元素。

- **recursive definition of a function**: a definition of a function that specifies an initial set of values and a rule for obtaining values of this function at integers from its values at smaller integers  
- **函数的递归定义**：一个函数的定义，指定了初始值集合以及从较小整数的函数值获得该函数在较大整数的值的规则。

- **recursive definition of a set**: a definition of a set that specifies an initial set of elements in the set and a rule for obtaining other elements from those in the set  
- **集合的递归定义**：一个集合的定义，指定了集合中的初始元素集合以及从集合中已有元素获得其他元素的规则。

- **structural induction**: a technique for proving results about recursively defined sets  
- **结构归纳法**：一种用于证明递归定义集合结果的技术。

- **recursive algorithm**: an algorithm that proceeds by reducing a problem to the same problem with smaller input  
- **递归算法**：通过将问题简化为具有较小输入的相同问题来解决的算法。

- **merge sort**: a sorting algorithm that sorts a list by splitting it in two, sorting each of the two resulting lists, and merging the results into a sorted list  
- **归并排序**：一种排序算法，通过将列表分成两部分，对这两部分分别排序，然后将结果合并成一个有序列表。

- **iteration**: a procedure based on the repeated use of operations in a loop  
- **迭代**：基于循环中重复使用操作的过程。

- **program correctness**: verification that a procedure always produces the correct result  
- **程序正确性**：验证一个过程总是产生正确的结果。

- **loop invariant**: a property that remains true during every traversal of a loop  
- **循环不变量**：在循环的每次迭代中始终保持为真的属性。

- **initial assertion**: the statement specifying the properties of the input values of a program  
- **初始断言**：指定程序输入值属性的陈述。

- **final assertion**: the statement specifying the properties the output values should have if the program worked correctly  
- **最终断言**：指定程序正确运行时输出值应具有的属性的陈述。