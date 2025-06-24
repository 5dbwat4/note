
## Key Terms and Results

### TERMS

- **tree**: a connected undirected graph with no simple circuits
- **forest**: an undirected graph with no simple circuits
- **rooted tree**: a directed graph with a specified vertex, called the root, such that there is a unique path to every other vertex from this root
- **subtree**: a subgraph of a tree that is also a tree
- **parent of v in a rooted tree**: the vertex $u$ such that $(u, v)$ is an edge of the rooted tree
- **child of a vertex $v$ in a rooted tree**: any vertex with $v$ as its parent
- **sibling of a vertex $v$ in a rooted tree**: a vertex with the same parent as $v$
- **ancestor of a vertex $v$ in a rooted tree**: any vertex on the path from the root to $v$
- **descendant of a vertex $v$ in a rooted tree**: any vertex that has $v$ as an ancestor
- **internal vertex**: a vertex that has children
- **leaf**: a vertex with no children
- **level of a vertex**: the length of the path from the root to this vertex
- **height of a tree**: the largest level of the vertices of a tree
- **m-ary tree**: a tree with the property that every internal vertex has no more than $m$ children
- **full m-ary tree**: a tree with the property that every internal vertex has exactly $m$ children
- **binary tree**: an $m$-ary tree with $m = 2$ (each child may be designated as a left or a right child of its parent)
- **ordered tree**: a tree in which the children of each internal vertex are linearly ordered
- **balanced tree**: a tree in which every leaf is at level $h$ or $h - 1$, where $h$ is the height of the tree
- **binary search tree**: a binary tree in which the vertices are labeled with items so that a label of a vertex is greater than the labels of all vertices in the left subtree of this vertex and is less than the labels of all vertices in the right subtree of this vertex
- **decision tree**: a rooted tree where each vertex represents a possible outcome of a decision and the leaves represent the possible solutions of a problem
- **game tree**: a rooted tree where vertices represent the possible positions of a game as it progresses and edges represent legal moves between these positions
- **preﬁx code**: a code that has the property that the code of a character is never a preﬁx of the code of another character
- **minmax strategy**: the strategy where the first player and second player move to positions represented by a child with maximum and minimum value, respectively
- **value of a vertex in a game tree**: for a leaf, the payoff to the first player when the game terminates in the position represented by this leaf; for an internal vertex, the maximum or minimum of the values of its children, for an internal vertex at an even or odd level, respectively
- **tree traversal**: a listing of the vertices of a tree
- **preorder traversal**: a listing of the vertices of an ordered rooted tree defined recursively—the root is listed, followed by the first subtree, followed by the other in the order they occur from left to right
- **inorder traversal**: a listing of the vertices of an ordered rooted tree defined recursively—the first subtree is listed, followed by the root, followed by the other subtrees in the order they occur from left to right
- **postorder traversal**: a listing of the vertices of an ordered rooted tree defined recursively—the subtrees are listed in the order they occur from left to right, followed by the root
- **inﬁx notation**: the form of an expression (including a full set of parentheses) obtained from an inorder traversal of the binary tree representing this expression
- **preﬁx (or Polish) notation**: the form of an expression obtained from a preorder traversal of the tree representing this expression
- **postﬁx (or reverse Polish) notation**: the form of an expression obtained from a postorder traversal of the tree representing this expression
- **spanning tree**: a tree containing all vertices of a graph
- **minimum spanning tree**: a spanning tree with smallest possible sum of weights of its edges

### RESULTS

- A graph is a tree if and only if there is a unique simple path between every pair of its vertices. A tree with $n$ vertices has $n - 1$ edges.
- A full $m$-ary tree with $i$ internal vertices has $mi + 1$ vertices.
- The relationships among the numbers of vertices, leaves, and internal vertices in a full $m$-ary tree (see Theorem 4 in Section 11.1)
- There are at most $m^h$ leaves in an $m$-ary tree of height $h$.
- If an $m$-ary tree has $l$ leaves, its height $h$ is at least $\lceil \log_m l \rceil$. If the tree is also full and balanced, then its height is $\lceil \log_m l \rceil$.
- **Huﬀman coding**: a procedure for constructing an optimal binary code for a set of symbols, given the frequencies of these symbols
- **depth-ﬁrst search, or backtracking**: a procedure for constructing a spanning tree by adding edges that form a path until this is not possible, and then moving back up the path until a vertex is found where a new path can be formed
- **breadth-ﬁrst search**: a procedure for constructing a spanning tree that successively adds all edges incident to the last set of edges added, unless a simple circuit is formed
- **Prim’s algorithm**: a procedure for producing a minimum spanning tree in a weighted graph that successively adds edges with minimal weight among all edges incident to a vertex already in the tree so that no edge produces a simple circuit when it is added
- **Kruskal’s algorithm**: a procedure for producing a minimum spanning tree in a weighted graph that successively adds edges of least weight that are not already in the tree such that no edge produces a simple circuit when it is added

## Chinese


### Key terms


- **tree**: a connected undirected graph with no simple circuits
- **树**：一个没有简单回路的连通无向图。

- **forest**: an undirected graph with no simple circuits
- **森林**：一个没有简单回路的无向图。

- **rooted tree**: a directed graph with a specified vertex, called the root, such that there is a unique path to every other vertex from this root
- **根树**：一个有向图，有一个指定的顶点称为根，从这个根到其他每个顶点都有唯一的路径。

- **subtree**: a subgraph of a tree that is also a tree
- **子树**：一个也是树的树的子图。

- **parent of v in a rooted tree**: the vertex $u$ such that $(u, v)$ is an edge of the rooted tree
- **根树中顶点 $v$ 的父节点**：顶点 $u$，使得 $(u, v)$ 是根树的一条边。

- **child of a vertex $v$ in a rooted tree**: any vertex with $v$ as its parent
- **根树中顶点 $v$ 的子节点**：任何以 $v$ 为父节点的顶点。

- **sibling of a vertex $v$ in a rooted tree**: a vertex with the same parent as $v$
- **根树中顶点 $v$ 的兄弟节点**：与 $v$ 有相同父节点的顶点。

- **ancestor of a vertex $v$ in a rooted tree**: any vertex on the path from the root to $v$
- **根树中顶点 $v$ 的祖先**：从根到 $v$ 的路径上的任何顶点。

- **descendant of a vertex $v$ in a rooted tree**: any vertex that has $v$ as an ancestor
- **根树中顶点 $v$ 的后代**：任何以 $v$ 为祖先的顶点。

- **internal vertex**: a vertex that has children
- **内部顶点**：有子节点的顶点。

- **leaf**: a vertex with no children
- **叶子**：没有子节点的顶点。

- **level of a vertex**: the length of the path from the root to this vertex
- **顶点的层次**：从根到该顶点的路径长度。

- **height of a tree**: the largest level of the vertices of a tree
- **树的高度**：树中顶点的最大层次。

- **m-ary tree**: a tree with the property that every internal vertex has no more than $m$ children
- **m-ary树**：一种树，其中每个内部顶点最多有 $m$ 个子节点。

- **full m-ary tree**: a tree with the property that every internal vertex has exactly $m$ children
- **满m-ary树**：一种树，其中每个内部顶点恰好有 $m$ 个子节点。

- **binary tree**: an $m$-ary tree with $m = 2$ (each child may be designated as a left or a right child of its parent)
- **二叉树**：一种 $m$-ary树，其中 $m = 2$（每个子节点可以被指定为其父节点的左子节点或右子节点）。

- **ordered tree**: a tree in which the children of each internal vertex are linearly ordered
- **有序树**：一种树，其中每个内部顶点的子节点都是线性有序的。

- **balanced tree**: a tree in which every leaf is at level $h$ or $h - 1$, where $h$ is the height of the tree
- **平衡树**：一种树，其中每个叶子都在层次 $h$ 或 $h - 1$ 上，其中 $h$ 是树的高度。

- **binary search tree**: a binary tree in which the vertices are labeled with items so that a label of a vertex is greater than the labels of all vertices in the left subtree of this vertex and is less than the labels of all vertices in the right subtree of this vertex
- **二叉搜索树**：一种二叉树，其中顶点被标记为项目，使得一个顶点的标记大于其左子树中所有顶点的标记，并且小于其右子树中所有顶点的标记。

- **decision tree**: a rooted tree where each vertex represents a possible outcome of a decision and the leaves represent the possible solutions of a problem
- **决策树**：一种根树，其中每个顶点代表一个决策的可能结果，叶子代表问题的可能解决方案。

- **game tree**: a rooted tree where vertices represent the possible positions of a game as it progresses and edges represent legal moves between these positions
- **博弈树**：一种根树，其中顶点代表游戏进行过程中可能的位置，边代表这些位置之间的合法移动。

- **preﬁx code**: a code that has the property that the code of a character is never a preﬁx of the code of another character
- **前缀码**：一种具有这样的性质的编码，即一个字符的编码永远不会是另一个字符编码的前缀。

- **minmax strategy**: the strategy where the first player and second player move to positions represented by a child with maximum and minimum value, respectively
- **极小化极大策略**：第一玩家和第二玩家分别移动到由具有最大值和最小值的子节点所表示的位置的策略。

- **value of a vertex in a game tree**: for a leaf, the payoff to the first player when the game terminates in the position represented by this leaf; for an internal vertex, the maximum or minimum of the values of its children, for an internal vertex at an even or odd level, respectively
- **博弈树中顶点的值**：对于叶子，当游戏在由该叶子所表示的位置终止时，第一玩家的收益；对于内部顶点，其子节点值的最大值或最小值，分别对应于处于偶数或奇数层次的内部顶点。

- **tree traversal**: a listing of the vertices of a tree
- **树的遍历**：列出树的顶点。

- **preorder traversal**: a listing of the vertices of an ordered rooted tree defined recursively—the root is listed, followed by the first subtree, followed by the other in the order they occur from left to right
- **前序遍历**：一种递归定义的有序根树的顶点列表——首先列出根，然后是第一棵子树，接着是按从左到右的顺序出现的其他子树。

- **inorder traversal**: a listing of the vertices of an ordered rooted tree defined recursively—the first subtree is listed, followed by the root, followed by the other subtrees in the order they occur from left to right
- **中序遍历**：一种递归定义的有序根树的顶点列表——首先列出第一棵子树，然后是根，接着是按从左到右的顺序出现的其他子树。

- **postorder traversal**: a listing of the vertices of an ordered rooted tree defined recursively—the subtrees are listed in the order they occur from left to right, followed by the root
- **后序遍历**：一种递归定义的有序根树的顶点列表——子树按从左到右的顺序列出，然后是根。

- **inﬁx notation**: the form of an expression (including a full set of parentheses) obtained from an inorder traversal of the binary tree representing this expression
- **中缀表示法**：通过对表示该表达式的二叉树进行中序遍历所得到的表达式形式（包括完整的括号集）。

- **preﬁx (or Polish) notation**: the form of an expression obtained from a preorder traversal of the tree representing this expression
- **前缀（或波兰）表示法**：通过对表示该表达式的树进行前序遍历所得到的表达式形式。

- **postﬁx (or reverse Polish) notation**: the form of an expression obtained from a postorder traversal of the tree representing this expression
- **后缀（或逆波兰）表示法**：通过对表示该表达式的树进行后序遍历所得到的表达式形式。

- **spanning tree**: a tree containing all vertices of a graph
- **生成树**：包含图中所有顶点的树。

- **minimum spanning tree**: a spanning tree with smallest possible sum of weights of its edges
- **最小生成树**：边的权重和最小的生成树。

### Results

- A graph is a tree if and only if there is a unique simple path between every pair of its vertices. A tree with $n$ vertices has $n - 1$ edges.
- 一个图是树当且仅当它的每对顶点之间都有一条唯一的简单路径。一个有 $n$ 个顶点的树有 $n - 1$ 条边。

- A full $m$-ary tree with $i$ internal vertices has $mi + 1$ vertices.
- 一个有 $i$ 个内部顶点的满 $m$-ary树有 $mi + 1$ 个顶点。

- The relationships among the numbers of vertices, leaves, and internal vertices in a full $m$-ary tree (see Theorem 4 in Section 11.1)
- 满 $m$-ary树中顶点数、叶子数和内部顶点数之间的关系（见第 11.1 节的定理 4）
> THEOREM 4
> 
> A full $m$-ary tree with
> 
> (i) $n$ vertices has $i = \frac{n - 1}{m}$ internal vertices and $l = \frac{[(m - 1)n + 1]}{m}$ leaves,
> 
> (ii) $i$ internal vertices has $n = mi + 1$ vertices and $l = (m - 1)i + 1$ leaves,
> 
> (iii) $l$ leaves has $n = \frac{(ml - 1)}{(m - 1)}$ vertices and $i = \frac{(l - 1)}{(m - 1)}$ internal vertices.

> 定理 4
> 
> 一个完全的m叉树具有
> 
> (i) $n$ 个顶点有 $i = \frac{n - 1}{m}$ 个内部顶点和 $l = \frac{[(m - 1)n + 1]}{m}$ 个叶子，
> 
> (ii) $i$ 个内部顶点有 $n = mi + 1$ 个顶点和 $l = (m - 1)i + 1$ 个叶子，
> 
> (iii) $l$ 个叶子有 $n = \frac{(ml - 1)}{(m - 1)}$ 个顶点和 $i = \frac{(l - 1)}{(m - 1)}$ 个内部顶点。

- There are at most $m^h$ leaves in an $m$-ary tree of height $h$.
- 在高度为 $h$ 的 $m$-ary树中，最多有 $m^h$ 个叶子。

- If an $m$-ary tree has $l$ leaves, its height $h$ is at least $\lceil \log_m l \rceil$. If the tree is also full and balanced, then its height is $\lceil \log_m l \rceil$.
- 如果一个 $m$-ary树有 $l$ 个叶子，其高度 $h$ 至少为 $\lceil \log_m l \rceil$。如果该树也是满的且平衡的，那么其高度为 $\lceil \log_m l \rceil$。

- **Huﬀman coding**: a procedure for constructing an optimal binary code for a set of symbols, given the frequencies of these symbols
- **霍夫曼编码**：一种根据符号的频率为一组符号构建最优二进制码的过程。

- **depth-ﬁrst search, or backtracking**: a procedure for constructing a spanning tree by adding edges that form a path until this is not possible, and then moving back up the path until a vertex is found where a new path can be formed
- **深度优先搜索，或回溯**：一种通过添加形成路径的边来构建生成树的过程，直到无法继续，然后沿着路径回溯，直到找到可以形成新路径的顶点。

- **breadth-ﬁrst search**: a procedure for constructing a spanning tree that successively adds all edges incident to the last set of edges added, unless a simple circuit is formed
- **广度优先搜索**：一种构建生成树的过程，依次添加最后添加的边集的所有关联边，除非形成简单回路。

- **Prim’s algorithm**: a procedure for producing a minimum spanning tree in a weighted graph that successively adds edges with minimal weight among all edges incident to a vertex already in the tree so that no edge produces a simple circuit when it is added
- **普里姆算法**：一种在加权图中生成最小生成树的过程，依次添加与树中顶点关联的最小权重边，以确保添加的边不会形成简单回路。

- **Kruskal’s algorithm**: a procedure for producing a minimum spanning tree in a weighted graph that successively adds edges of least weight that are not already in the tree such that no edge produces a simple circuit when it is added
- **克鲁斯卡尔算法**：一种在加权图中生成最小生成树的过程，依次添加不在树中的最小权重边，以确保添加的边不会形成简单回路。