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
