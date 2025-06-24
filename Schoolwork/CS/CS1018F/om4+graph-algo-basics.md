# Graph algorithms (1) Definitions

$$ G(V, E) $$:其中 $G$ 是一个图，$V = V(G)$ 是顶点的有限非空集合，$E = E(G)$ 是边的有限集合。


**无向图 (Undirected Graph)**：$( v_i, v_j )  = ( v_j, v_i )$ 表示相同的边。

**有向图 (Directed Graph (Digraph))**：$\langle v_i, v_j \rangle \neq \langle v_j, v_i \rangle$

**Restrictions**

1. 自环是非法的。Self loop is illegal.
2. 不考虑多重图。Multigraph is not considered

**完全图 Complete graph**:  a graph that has the maximum number of edges

**子图(Subgraph)** $G' \subseteq G$ 定义为 $V(G') \subseteq V(G)$ 且 $E(G') \subseteq E(G)$。

**Path**：A path in a graph is a sequence of vertices $w_1, w_2, w_3, \ldots, w_N$ such that $(w_i, w_{i + 1}) \in E$ for $1 \leq i < N$.

**路径的长度(Path Length)**定义为路径上的边数。

Simple Path：$v_{i1}, v_{i2}, \cdots, v_{in}$ 是不同的。

循环 Cycle：简单路径，其中 $v_p = v_q$。

## Connected Vertices
在无向图中，如果存在从 $v_i$ 到 $v_j$ 的路径（因此也存在从 $v_j$ 到 $v_i$ 的路径），则 $v_i$ 和 $v_j$ 是连通的。

**连通图 Connected Graph**： 无向图 $G$ 是连通的，如果每对不同的 $v_i$ 和 $v_j$ 都是连通的。

无向图 $G$ 的连通分量 Connected Component 定义为最大的连通子图。

**树 Tree**：一个连通且无环的图。

**DAG**（**有向无环图** a directed acyclic graph）。

**强连通有向图(Strongly Connected Graph)** $G$ 定义为对于 $V(G)$ 中的每一对 $v_i$ 和 $v_j$，都存在从 $v_i$ 到 $v_j$ 和从 $v_j$ 到 $v_i$ 的有向路径。如果图是无方向的并且边是连通的，则称其为弱连通。

**强连通分量(Strongly Connected Component)**定义为最大的强连通子图。

**度 degree**（$v$）定义为与 $v$ 相关联的边的数量。对于有向图，我们有入度和出度。例如：
$$ \text{in-degree}(v) = 3; \text{out-degree}(v) = 1; \text{degree}(v) = 4 $$
