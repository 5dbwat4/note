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