## Key Terms and Results

### TERMS

- **binary relation from A to B**: a subset of $A \times B$
- **relation on A**: a binary relation from A to itself (that is, a subset of $A \times A$)
- **$S \circ R$**: composite of R and S
- **$R^{-1}$**: inverse relation of R
- **$R^n$**: nth power of R
- **reflexive**: a relation R on A is reflexive if $(a, a) \in R$ for all $a \in A$
- **symmetric**: a relation R on A is symmetric if $(b, a) \in R$ whenever $(a, b) \in R$
- **antisymmetric**: a relation R on A is antisymmetric if $a = b$ whenever $(a, b) \in R$ and $(b, a) \in R$
- **transitive**: a relation R on A is transitive if $(a, b) \in R$ and $(b, c) \in R$ implies that $(a, c) \in R$
- **$n$-ary relation on $A_1, A_2, \cdots, A_n$**: a subset of $A_1 \times A_2 \times \cdots \times A_n$
- **relational data model**: a model for representing databases using n-ary relations
- **primary key**: a domain of an n-ary relation such that an n-tuple is uniquely determined by its value for this domain
- **composite key**: the Cartesian product of domains of an n-ary relation such that an n-tuple is uniquely determined by its values in these domains
- **selection operator**: a function that selects the n-tuples in an n-ary relation that satisfy a specified condition
- **projection**: a function that produces relations of smaller degree from an n-ary relation by deleting fields
- **join**: a function that combines n-ary relations that agree on certain fields
- **itemset**: a collection of items
- **count of an itemset**: the number of transactions that are supersets of the itemset
- **frequent itemset**: an itemset with frequency greater than or equal to the support threshold
- **support of an itemset**: the frequency of transactions that contain the itemset
- **association rule**: an implication of the form $I \rightarrow J$, where I and J are itemsets
- **support of the association rule $I \rightarrow J$**: the fraction of transactions that contain both the itemsets I and J
- **confidence of an association rule**: the conditional probability that J is a subset of a transaction given that I is
- **directed graph or digraph**: a set of elements called vertices and ordered pairs of these elements, called edges
- **loop**: an edge of the form $(a, a)$
- **closure of a relation R with respect to a property P**: the relation S (if it exists) that contains R, has property P, and is contained within any relation that contains R and has property P
- **path in a digraph**: a sequence of edges $(a, x_1), (x_1, x_2), \ldots, (x_{n−2}, x_{n−1}), (x_{n−1}, b)$ such that the terminal vertex of each edge is the initial vertex of the succeeding edge in the sequence
- **circuit (or cycle) in a digraph**: a path that begins and ends at the same vertex
- **R* (connectivity relation)**: the relation consisting of those ordered pairs $(a, b)$ such that there is a path from $a$ to $b$
- **equivalence relation**: a reflexive, symmetric, and transitive relation
- **equivalent**: if R is an equivalence relation, a is equivalent to b if $aRb$
- **$\left[a\right]_R$ (equivalence class of a with respect to R)**: the set of all elements of A that are equivalent to $a$
- **$\left[a\right]_m$ (congruence class modulo $m$)**: the set of integers congruent to $a$ modulo $m$
- **partition of a set S**: a collection of pairwise disjoint nonempty subsets that have S as their union
- **partial ordering**: a relation that is reflexive, antisymmetric, and transitive
- **poset $(S, R)$**: a set S and a partial ordering R on this set
- **comparable**: the elements a and b in the poset (A, $\preceq$ ) are comparable if $a \preceq b$ or $b \preceq a$
- **incomparable**: elements in a poset that are not comparable
- **total (or linear) ordering**: a partial ordering for which every pair of elements are comparable
- **totally (or linearly) ordered set**: a poset with a total (or linear) ordering
- **well-ordered set**: a poset (S, $\preceq$ ), where $\preceq$ is a total order and every nonempty subset of S has a least element
- **lexicographic order**: a partial ordering of Cartesian products or strings
- **Hasse diagram**: a graphical representation of a poset where loops and all edges resulting from the transitive property are not shown, and the direction of the edges is indicated by the position of the vertices
- **maximal element**: an element of a poset that is not less than any other element of the poset
- **minimal element**: an element of a poset that is not greater than any other element of the poset
- **greatest element**: an element of a poset greater than all other elements in this set
- **least element**: an element of a poset less than all other elements in this set
- **upper bound of a set**: an element in a poset greater than all other elements in the set
- **lower bound of a set**: an element in a poset less than all other elements in the set
- **least upper bound of a set**: an upper bound of the set that is less than all other upper bounds
- **greatest lower bound of a set**: a lower bound of the set that is greater than all other lower bounds
- **lattice**: a partially ordered set in which every two elements have a greatest lower bound and a least upper bound
- **compatible total ordering for a partial ordering**: a total ordering that contains the given partial ordering
- **topological sort**: the construction of a total ordering compatible with a given partial ordering

#### RESULTS

- The reflexive closure of a relation R on the set A equals $R \cup \Delta$, where $\Delta = \{(a, a) \mid a \in A\}$.
- The symmetric closure of a relation R on the set A equals $R \cup R^{-1}$, where $R^{-1} = \{(b, a) \mid (a, b) \in R\}$.
- The transitive closure of a relation equals the connectivity relation formed from this relation.
- Warshall’s algorithm for finding the transitive closure of a relation.
- Let R be an equivalence relation. Then the following three statements are equivalent:
  1. $a R b$
  2. $[a]_R \cap [b]_R \neq \emptyset$
  3. $[a]_R = [b]_R$
- The equivalence classes of an equivalence relation on a set A form a partition of A. Conversely, an equivalence relation can be constructed from any partition so that the equivalence classes are the subsets in the partition.
- The principle of well-ordered induction.
- The topological sorting algorithm.


## CN

- **binary relation from A to B**: a subset of $A \times B$
- **从 A 到 B 的二元关系**：$A \times B$ 的一个子集
- **relation on A**: a binary relation from A to itself (that is, a subset of $A \times A$)
- **A 上的关系**：从 A 到自身的二元关系（即 $A \times A$ 的一个子集）
- **$S \circ R$**: composite of R and S
- **$S \circ R$**：R 和 S 的复合关系
- **$R^{-1}$**: inverse relation of R
- **$R^{-1}$**：R 的逆关系
- **$R^n$**: nth power of R
- **$R^n$**：R 的 n 次幂
- **reflexive**: a relation R on A is reflexive if $(a, a) \in R$ for all $a \in A$
- **自反的**：如果对于所有 $a \in A$，都有 $(a, a) \in R$，则 A 上的关系 R 是自反的
- **symmetric**: a relation R on A is symmetric if $(b, a) \in R$ whenever $(a, b) \in R$
- **对称的**：如果对于所有 $(a, b) \in R$，都有 $(b, a) \in R$，则 A 上的关系 R 是对称的
- **antisymmetric**: a relation R on A is antisymmetric if $a = b$ whenever $(a, b) \in R$ and $(b, a) \in R$
- **反对称的**：如果对于所有 $(a, b) \in R$ 和 $(b, a) \in R$，都有 $a = b$，则 A 上的关系 R 是反对称的
- **transitive**: a relation R on A is transitive if $(a, b) \in R$ and $(b, c) \in R$ implies that $(a, c) \in R$
- **传递的**：如果对于所有 $(a, b) \in R$ 和 $(b, c) \in R$，都有 $(a, c) \in R$，则 A 上的关系 R 是传递的
- **$n$-ary relation on $A_1, A_2, \cdots, A_n$**: a subset of $A_1 \times A_2 \times \cdots \times A_n$
- **$A_1, A_2, \cdots, A_n$ 上的 n 元关系**：$A_1 \times A_2 \times \cdots \times A_n$ 的一个子集
- **relational data model**: a model for representing databases using n-ary relations
- **关系数据模型**：使用 n 元关系表示数据库的模型
- **primary key**: a domain of an n-ary relation such that an n-tuple is uniquely determined by its value for this domain
- **主键**：n 元关系的一个域，使得 n 元组由该域的值唯一确定
- **composite key**: the Cartesian product of domains of an n-ary relation such that an n-tuple is uniquely determined by its values in these domains
- **复合键**：n 元关系的域的笛卡尔积，使得 n 元组由这些域中的值唯一确定
- **selection operator**: a function that selects the n-tuples in an n-ary relation that satisfy a specified condition
- **选择运算符**：选择满足特定条件的 n 元关系中的 n 元组的函数
- **projection**: a function that produces relations of smaller degree from an n-ary relation by deleting fields
- **投影**：通过删除字段从 n 元关系生成较小度数关系的函数
- **join**: a function that combines n-ary relations that agree on certain fields
- **连接**：将某些字段一致的 n 元关系组合的函数
- **itemset**: a collection of items
- **项集**：一组项
- **count of an itemset**: the number of transactions that are supersets of the itemset
- **项集的计数**：包含该项集的交易数量
- **frequent itemset**: an itemset with frequency greater than or equal to the support threshold
- **频繁项集**：频率大于或等于支持度阈值的项集
- **support of an itemset**: the frequency of transactions that contain the itemset
- **项集的支持度**：包含该项集的交易频率
- **association rule**: an implication of the form $I \rightarrow J$, where I and J are itemsets
- **关联规则**：形式为 $I \rightarrow J$ 的蕴含，其中 I 和 J 是项集
- **support of the association rule $I \rightarrow J$**: the fraction of transactions that contain both the itemsets I and J
- **关联规则 $I \rightarrow J$ 的支持度**：包含项集 I 和 J 的交易比例
- **confidence of an association rule**: the conditional probability that J is a subset of a transaction given that I is
- **关联规则的置信度**：在 I 是交易的子集的条件下，J 是交易的子集的条件概率
- **directed graph or digraph**: a set of elements called vertices and ordered pairs of these elements, called edges
- **有向图或有向图**：一组称为顶点的元素和这些元素的有序对，称为边
- **loop**: an edge of the form $(a, a)$
- **环**：形式为 $(a, a)$ 的边
- **closure of a relation R with respect to a property P**: the relation S (if it exists) that contains R, has property P, and is contained within any relation that contains R and has property P
- **关系 R 关于性质 P 的闭包**：包含 R、具有性质 P 且包含在任何包含 R 且具有性质 P 的关系中的关系 S（如果存在）
- **path in a digraph**: a sequence of edges $(a, x_1), (x_1, x_2), \ldots, (x_{nâˆ’2}, x_{nâˆ’1}), (x_{nâˆ’1}, b)$ such that the terminal vertex of each edge is the initial vertex of the succeeding edge in the sequence
- **有向图中的路径**：一系列边 $(a, x_1), (x_1, x_2), \ldots, (x_{nâˆ’2}, x_{nâˆ’1}), (x_{nâˆ’1}, b)$，使得每条边的终点是序列中下一条边的起点
- **circuit (or cycle) in a digraph**: a path that begins and ends at the same vertex
- **有向图中的回路（或环路）**：起点和终点相同的路径
- **R* (connectivity relation)**: the relation consisting of those ordered pairs $(a, b)$ such that there is a path from $a$ to $b$
- **R*（连通性关系）**：由那些存在从 $a$ 到 $b$ 的路径的有序对 $(a, b)$ 组成的关系
- **equivalence relation**: a reflexive, symmetric, and transitive relation
- **等价关系**：自反、对称且传递的关系
- **equivalent**: if R is an equivalence relation, a is equivalent to b if $aRb$
- **等价的**：如果 R 是等价关系，当 $aRb$ 时，a 与 b 等价
- **$\left[a\right]_R$ (equivalence class of a with respect to R)**: the set of all elements of A that are equivalent to $a$
- **$\left[a\right]_R$（a 关于 R 的等价类）**：A 中所有与 a 等价的元素的集合
- **$\left[a\right]_m$ (congruence class modulo $m$)**: the set of integers congruent to $a$ modulo $m$
- **$\left[a\right]_m$（模 $m$ 的同余类）**：与 $a$ 模 $m$ 同余的整数集合
- **partition of a set S**: a collection of pairwise disjoint nonempty subsets that have S as their union
- **集合 S 的划分**：S 作为并集的成对不相交的非空子集的集合
- **partial ordering**: a relation that is reflexive, antisymmetric, and transitive
- **偏序**：自反、反对称且传递的关系
- **poset $(S, R)$**: a set S and a partial ordering R on this set
- **偏序集 $(S, R)$**：集合 S 和 S 上的偏序 R
- **comparable**: the elements a and b in the poset (A, $\preceq$ ) are comparable if $a \preceq b$ or $b \preceq a$
- **可比的**：在偏序集 (A, $\preceq$ ) 中，如果 $a \preceq b$ 或 $b \preceq a$，则元素 a 和 b 是可比的
- **incomparable**: elements in a poset that are not comparable
- **不可比的**：偏序集中不可比的元素
- **total (or linear) ordering**: a partial ordering for which every pair of elements are comparable
- **全序（或线性序）**：每对元素都可比的偏序
- **totally (or linearly) ordered set**: a poset with a total (or linear) ordering
- **全序集（或线性序集）**：具有全序（或线性序）的偏序集
- **well-ordered set**: a poset (S, $\preceq$ ), where $\preceq$ is a total order and every nonempty subset of S has a least element
- **良序集**：偏序集 (S, $\preceq$ )，其中 $\preceq$ 是全序，且 S 的每个非空子集都有最小元素
- **lexicographic order**: a partial ordering of Cartesian products or strings
- **字典序**：笛卡尔积或字符串的偏序
- **Hasse diagram**: a graphical representation of a poset where loops and all edges resulting from the transitive property are not shown, and the direction of the edges is indicated by the position of the vertices
- **哈斯图**：偏序集的图形表示，其中不显示环和由传递性质产生的所有边，边的方向由顶点的位置表示
- **maximal element**: an element of a poset that is not less than any other element of the poset
- **极大元素**：偏序集中的元素，它不小于偏序集中的任何其他元素
- **minimal element**: an element of a poset that is not greater than any other element of the poset
- **极小元素**：偏序集中的元素，它不大于偏序集中的任何其他元素
- **greatest element**: an element of a poset greater than all other elements in this set
- **最大元素**：偏序集中大于该集中所有其他元素的元素
- **least element**: an element of a poset less than all other elements in this set
- **最小元素**：偏序集中小于该集中所有其他元素的元素
- **upper bound of a set**: an element in a poset greater than all other elements in the set
- **集合的上界**：偏序集中大于该集中所有其他元素的元素
- **lower bound of a set**: an element in a poset less than all other elements in the set
- **集合的下界**：偏序集中小于该集中所有其他元素的元素
- **least upper bound of a set**: an upper bound of the set that is less than all other upper bounds
- **集合的最小上界**：该集的上界，它小于所有其他上界
- **greatest lower bound of a set**: a lower bound of the set that is greater than all other lower bounds
- **集合的最大下界**：该集的下界，它大于所有其他下界
- **lattice**: a partially ordered set in which every two elements have a greatest lower bound and a least upper bound
- **格**：偏序集，其中每两个元素都有最大下界和最小上界
- **compatible total ordering for a partial ordering**: a total ordering that contains the given partial ordering
- **与偏序相容的全序**：包含给定偏序的全序
- **topological sort**: the construction of a total ordering compatible with a given partial ordering
- **拓扑排序**：构造与给定偏序相容的全序

#### RESULTS

- The reflexive closure of a relation R on the set A equals $R \cup \Delta$, where $\Delta = \{(a, a) \mid a \in A\}$.
- 集合 A 上的关系 R 的自反闭包等于 $R \cup \Delta$，其中 $\Delta = \{(a, a) \mid a \in A\}$。
- The symmetric closure of a relation R on the set A equals $R \cup R^{-1}$, where $R^{-1} = \{(b, a) \mid (a, b) \in R\}$.
- 集合 A 上的关系 R 的对称闭包等于 $R \cup R^{-1}$，其中 $R^{-1} = \{(b, a) \mid (a, b) \in R\}$。
- The transitive closure of a relation equals the connectivity relation formed from this relation.
- 关系的传递闭包等于由该关系形成的连通性关系。
- Warshallâ€™s algorithm for finding the transitive closure of a relation.
- 沃舍尔算法用于寻找关系的传递闭包。
- Let R be an equivalence relation. Then the following three statements are equivalent:
  1. $a R b$
  2. $[a]_R \cap [b]_R \neq \emptyset$
  3. $[a]_R = [b]_R$
- 设 R 是等价关系。那么以下三个陈述是等价的：
  1. $a R b$
  2. $[a]_R \cap [b]_R \neq \emptyset$
  3. $[a]_R = [b]_R$
- The equivalence classes of an equivalence relation on a set A form a partition of A. Conversely, an equivalence relation can be constructed from any partition so that the equivalence classes are the subsets in the partition.
- 等价关系在集合 A 上的等价类形成 A 的一个划分。反之，可以从任何划分构造等价关系，使得等价类是划分中的子集。
- The principle of well-ordered induction.
- 良序归纳原理。
- The topological sorting algorithm.
- 拓扑排序算法。