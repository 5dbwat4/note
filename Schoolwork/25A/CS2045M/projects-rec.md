---
title: ADS25Project(MYC)
---


# 1 Comparing Different Binary Search Trees

**Project Description**

In AVL trees, the balance criterion is on the height of subtrees. Some other trees may achieve balance by restricting the weight of subtrees.  One of such trees, namely the BB\[$\alpha$\] trees (BB stands for bounded balance), is introduced in problem 17-3 (at the end of Chapter 17) of *Introduction to Algorithms* (third edition). 

In this project, you are required to do the followings.

1. Give a theoretical analysis for BB\[$\alpha$\] trees. That is, you should solve all the questions in problem 17-3.
2. Implement the basic BST, the AVL tree,  the splay tree, and the BB\[$\alpha$\] tree.
3. Run experiments to compare their performance.

**Experiments**

You may insert $N$ elements into an empty tree in increasing order or in random order, and measure how the following three quantities change against $N$. Note that when you insert in random order, you should use the expectation of these quantities.

* total time cost by the insertions
* average depth of nodes after insertions

You may also compare the three kinds of trees under different sequences of (findkey) queries, and see how the patterns of the sequences affect the total query time.

**Bonus**

Other than the binary search trees and experiments required above, you may implement more balanced trees and do more experiments. Bonus will be granted depending on the quality of your work.

**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code (including the implementation and the testing code), and the testing data. The zip file should be named as PxGy.zip  ( 'your student number + Px.zip' for personal bonus) where x is the project number (1 for this project) and y is your group number.

The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.

* A description of the BB\[$\alpha$\] trees, and a theoretical analysis of its performance.
* A theoretical comparison of the performance of the binary search trees you implemented.
* A detailed description of your experiments, including how they are designed, how the testing data are generated, how the results are obtained.
* Results of your experiment and an analysis of these results.
* Conclusion.

The report  should be typeset using 12-point fonts, in a single-column, single-space format.

You are encouraged to write your report using latex (try [overleaf.com](https://www.overleaf.com "https://www.overleaf.com")), but ms word is also fine.

The source code should be in good style, and have sufficient comments.

All the testing data should be stored and uploaded (even if they are randomly generated).

# 2 Shortest Path Algorithm with Heaps

**Project Description**

In this project, you are supposed to implement the Dijkstra’s algorithm using different heaps, and compare the performance of these implementations. Only three heap operations ( insertion, deletemin, and decreasekey ) are considered in this project.

**1\.  Fibonacci Heaps**

A Fibonacci heap is a priority queue consisting of a collection of heap-ordered trees. It has a better amortized cost than many other heap structures. You may refer to Chapter 19 of *Introduction to Algorithms* (third edition) for details. You should do the followings.

* Introduce the Fibonacci heaps and describe how insertion, deletemin, and decreasekey are supported. Also list the amortized cost of these three operations. (Analysis is not required)

* Analyze the worst-case cost of the three heap operations.

**2\. Dijkstra's Algorithm**

The Dijkstra's algorithm solves the shortest path problem on graphs with non-negative edge weights. 

In this part, you have the following tasks.

* Implement the Dijkstra’s algorithm using Fibonacci heaps and binary heaps.
* Give a theoretical analysis of the running time of these two implementations.
* Do experiment to compare the performance of these two implementations on graph with different density. You may generate graphs with $m = \Theta(n)$, $m =\Theta(n^{1.5})$, and $m = \Theta(n^2)$，and test how the running time of these two implementations increase against $n$.
* Evaluate the these two implementations using the USA road networks. The data sets can be downloaded from <http://www.dis.uniroma1.it/challenge9/download.shtml>. You should evaluate on road networks of different sizes. For each network, at least $1000$ queries are required. Each query is a pair of a source and a sink, and the algorithm should return the length of the shortest between them.

**Bonus**

Other than the two heap structures required above, you may try other heaps and test their performance. Bonus will be granted depending on the quality of your work.

**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code (including the implementation and the testing code), and the testing data. The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (2 for this project) and y is your group number.

The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.

* A clear description of this project.
* An introduction of the Fabonacci heap
* A theoretical analysis of the worst-case cost of Fibonacci heap. (Only insertion, deletemnin, and decreasekey are considered.)
* A theoretical analysis of the running time of the two different implementations of the Dijkstra’s algorithm.
* A description of your experiment and its result. (All we care here is the running time evaluation.  As to the correctness test, you only need to submit the test code.) You should state how the input data is generated (or selected), how the experiments are carried out, how the resulting data is obtained, as well as other things that you think are important. You should also present the result of your experiment using tables and figures.
* Conclusion and discussion.

The report  should be typeset using 12-point fonts, in a single-column, single-space format.

You are encouraged to write your report using latex (try [overleaf.com](https://www.overleaf.com "https://www.overleaf.com")), but ms word is also fine.

The source code should be in good style, and have sufficient comments.

All the testing data **other than those downloaded from the website** should be stored and uploaded (even if they are randomly generated).

A `readme.txt` that simply specifies the testing data is required. For those downloaded from the website, you must only list the download links of these test data sets in `readme.txt` instead of uploading them with your reports.

# 3 Safe Fruit

**Project Description**

Solve the problem No.1021 (safe fruit) in the PAT (top level) practice problem set ([link](https://pintia.cn/problem-sets/994805148990160896/exam/problems/type/7?problemSetProblemId=994805149506060288)).
You should pass all the test cases on Pintia. You should also design your own test cases of different sizes, and see how the running time of your algorithm changes agianst the input size. Note that even on inputs of the same size, the algorithm may have different running time. Therefore, for each input size, you may evaluate your algorithm on multiple inputs, and then take the average runnning time. 

**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code ( It should include an independent file containing the program that can pass the test cases on pintia). The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (3 for this project) and y is your group number.

The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.
* A description of the problem.
* A presentation of your algorithm. You should explain how you do branch and prune. You may get some ideas from this paper ([link](http://i.stanford.edu/pub/cstr/reports/cs/tr/76/550/CS-TR-76-550.pdf)). You should also give the pseudo-code of your algorithm. (Do NOT paste your actual code in this part!) 
* An analysis of the running time of your algorithm. It may not be possible to derive a tight upper bound. Just do your best.
* An exhibition of your experiment and its result. You should state how the testing data is generated, the setting of your experiment, how the resulting data is obtained, as well as other things that you think are important. As to the result, you should give a table showing the running time of your algorithm on input of different size . You should also plot the running times against the input size for illustration.
* Discussion and Conclusion
* You may get a bouns if you come up with multiple algorithms and comparing their performance in your experiment. The bonus ranges from 0 to 1 pts depending on the quality of your work.

The report should be typeset using 12-point fonts, in a single-column, single-space format.

The source code should be in good style, and have sufficient comments.


# 4 Counting the Number of Distinct Red-Black Trees

**Project Description**

Solve the problem of counting the number of distinct red-black trees ([link](https://pintia.cn/problem-sets/994805148990160896/exam/problems/type/7?problemSetProblemId=994805153880719360&page=0)).

You should pass all the test cases for that problem on pintia. You should also design your own test cases of different sizes, and see how the running time of your algorithm changes against the input $$N$$.

Although this problem can be solved by dynamic programming, there are multiple ways to improve its performance. Try your best.


**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code ( It should include an independent file containing the program that can pass the test cases on pintia). The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (4 for this project) and y is your group number.

The report should be written clearly and neatly in English. It should start with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.
- A description of the problem.
- A presentation of your algorithm. For a dynamic programming algorithm, you should explain the following three parts.
	1.  how the subproblems are defined.
	2.  what is the relation (recurrence) between the optimal solution of the subproblems, and how they are obtained
	3.  pseudo-code to compute the optimal solution for all subproblems
- An analysis of the running time of your algorithm
- An exhibition of your experiment and its result. You should give a table showing the running time of your algorithm on different input $$N$$ . You should also plot the running times against $$N$$ for illustration.
- Discussion and Conclusion

The report should be typeset using 12-point fonts, in a single-column, single-space format. The source code should be in good style, and have sufficient comments.


# 5 Improving Dynamic Programming for Knapsack Problems

**Project Description**

In class we have introduced the Knapsack problem and a $O(nc)$\-time dynamic programing algorithm where $n$ is the number of items and $c$ is the capacity of the knapsack. Note that even in the best case, this algorithm needs as much as $O(nc)$ time, and this is unpleasant in practice.

Chapter 3.4 of the book in the Reference provides an alternative implementation of the dynamic programing algorithm, which has a better best-case running time when combined with a pruning idea.

Chapter 3.5 of the book provides an idea for further improvement of the dynamic programming algorithm. You may implement it and compare it to the other two algorithms. Bonus will be granted depending on the quality of your work.

You are required to do the following.

1. read chapter 3.4 & 3.5 of the book, and implement the algorithms.
2. conduct experiment to compare the performance of this algorithms with the original DP we present in class. 

For simplicity, we are only interested in the optimal value (rather than the optimal solution) of the knapsack problems considered in this project.

**Bonus
T**here is also an $O(n + w^3)$-time algorithm depending on convolution. See [Link](https://drops.dagstuhl.de/storage/00lipics/lipics-vol198-icalp2021/LIPIcs.ICALP.2021.106/LIPIcs.ICALP.2021.106.pdf) for reference. You may implement this algorithm as well.

**Reference**

H. Kellerer, U. Pferschy, D. Pisinger. 2004. *The Knapsack Problems*. Springer. ([CH3.4&3.5.pdf](~/5c8b0624-e722-40e3-a8a4-748c510705b4.pdf)) 

**Notation of the Book**

In the above book, $w_j$ and $p_j$ are the weight and the profit (value) of the item $j$. DP-1 is the algorithm we present in class, and $z_j(d)$ is the maximum value we can achieve with capacity $d$ when considering only the first $j$ items.

**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code (including the implementation and the testing code), and the testing data. The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (5 for this project) and y is your group number.

The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.

* A description of the algorithm and its idea in your \*own\* words.

* A detailed description of your experiments, including how they are designed, how the testing data are generated, how the results are obtained.

* Results of your experiment and an analysis of these results.

* Conclusion.

* Contribution of each group member.

The report  should be typeset using 12-point fonts, in a single-column, single-space format.

You are encouraged to write your report using latex (try [overleaf.com](https://www.overleaf.com "https://www.overleaf.com")), but ms word is also fine.

The source code should be in good style, and have sufficient comments.

All the testing data should be stored and uploaded (even if they are randomly generated).

# 6 Strip Packing

**Project Description**

Consider the following strip packing problem.

Input: you are given $n$ rectangles, each having a width and a height. You are also given a bin with a given width. The height of bin can be as large as you want. (You may assume that the width of any rectangle is no more than the width of the bin.)

Output: you are required to packing the rectangle into the bin so that the height of the bin is minimized. Note that you are not allowed to rotate the rectangles, and that the rectangles should not overlap.

For more information, please refer to Wikipedia ([link](https://en.wikipedia.org/wiki/Strip_packing_problem)).

This project requires you to implement at least two polynomial-time approximation algorithms for this problem. You must generate test cases of different sizes (from 10 to 10,000) with different distributions of widths and heights, and compare the solution quality and the running time of the two algorithms on these test cases. A thorough analysis on all the factors that might affect the approximation ratio of your proposed algorithm is expected.

**Bonus**

Instead of rectangles, you are now given $n$ tetrominos ([link](https://en.wikipedia.org/wiki/Tetromino) to the introduction of tetrominos in Wikipedia) or other customized simple polygons that are peculiar in shape but have all edges either horizontal or vertical. You can customize parameters of the input polygons.

First do experiments to perform your algorithms on these input polygons to observe the efficiency and results. Then try to make some targeted adjustments for the structural characteristics of the input polygons to your algorithms, and do experiments to compare the improved algorithms with the original ones. You are not required to make a theoretical analysis.

Bonus will be granted depending on the quality of your work.

**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code. The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (6 for this project) and y is your group number.

The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.

* A description of the problem.

* A presentation of the algorithms. 

* An analysis of the approximation ratio and the running time of the algorithms

* An exhibition of your experiment and its result. 

* Discussion and Conclusion

The report  should be typeset using 12-point fonts, in a single-column, single-space format. You are encouraged to write your report using latex (try [overleaf.com](http://www.overleaf.com "http://www.overleaf.com")), but ms word is also fine. The source code should be in good style, and have sufficient comments. All the testing data should be stored and uploaded (even if they are randomly generated).

# 7 Local Search for Maximum Cut

**Project Description**

In class, we present several local search algorithms for maximum cut problem: 

1. a $2$-approximation algorithm that takes $O(W)$ iterations, 
2. a $(2 + \epsilon)$\-approximation algorithm that takes $O(\frac{n}{\epsilon}\log W)$ iterations,
3. an algorithm that uses a neighborhood defined by the Kernighan-Lin Heuristic.

In this project, you are required to implement these three algorithms, and compare their performance (solution quality and running time).

**Bonus**

Consider the following greedy algorithm. Let $V = \{v_1, \ldots, v_n\}$ be the set of vertices. Starting with two empty sets $A$ and $B$, we iteratively put vertices into $A$ or $B$. For each vertex $v_i$, we put it into the set that maximizes $w(A, B)$.

In this step, you have the following tasks.

1. Prove that this greedy algorithm has an approximation ratio of $2$.
2. Implement this greedy algorithm and compare its performance with that of the local search algorithms.

Bonus will be granted depending on the quality of your work.

**Submission Guidelines**

You are required to upload a zip file that contains the project report (in pdf format), the source code. The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (7 for this project) and y is your group number.\
The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.

* An introduction of the problem.
* A brief description of the three algorithms. (You don't have to analyze them theoretically as we have already done that in class.)
* An exhibition of your experiment and its result. 
* Discussion and Conclusion

The report should be typeset using 12-point fonts, in a single-column, single-space format. You are encouraged to write your report using latex (try overleaf.com), but ms word is also fine. The source code should be in good style, and have sufficient comments. All the testing data should be stored and uploaded (even if they are randomly generated).

# 8 Skip List

**Project Description**

The skip list is a simple yet powerful data struture that efficiently supports find, insertion, and deletion. You may check the wikipedia for more information.

You are supposed to finish the following four tasks in this project.
1. Present the strucutre of the skip list, and explain how the three operations are supported.
2. Give a formal analysis of each operation.
3. Implement skip list.
4. Measure the practical performance of skip list on inputs of different size.

**Bonus**

Consider B+ trees using skip list to implement their nodes.

In this step, you have the following tasks.

1. Prove that the running time of finding a node in such a B+ tree of $n$ keys is $O(\log n)$, which is irrelevant to its order $M$, and analyze the running time of insertion and deletion.
2. Consider B+ trees of the same order with different implementations of nodes (skip list, linked list, linear list and so on). Compare the effect of implementing nodes with skip lists and with other implementations on the efficiency of B+ tree operations. You may try B+ trees with relatively larger order to make the comparison results more significant.

Bonus will be granted depending on the quality of your work.

**Submission Guidelines
Y**ou are required to upload a zip file that contains the project report (in pdf format), the source code. The zip file should be named as PxGy.zip ( 'your student number + Px.zip' for personal bonus) where x is the project number (8 for this project) and y is your group number.
The report should be written clearly and neatly in English. It should starts with a title page containing the title, the group id, the author names, and an abstract summarizing your work. Within the 10 pages following the title page, the report should present the following contents.
- A complete description of skip list (how the elements are organized, and how the operations are supported)
- A formal analysis of operations of the skip list
- An deccription of your experiment
- An exhibition of the experiment result.
- Discussion and Conclusion

The report should be typeset using 12-point fonts, in a single-column, single-space format. The source code should be in good style, and have sufficient comments.

