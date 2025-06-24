## Key Terms and Results

### TERMS

- **undirected edge**: an edge associated to a set $\{u, v\}$, where $u$ and $v$ are vertices
- **directed edge**: an edge associated to an ordered pair $(u, v)$, where $u$ and $v$ are vertices
- **multiple edges**: distinct edges connecting the same vertices
- **multiple directed edges**: distinct directed edges associated with the same ordered pair $(u,v)$,where $u$ and $v$ are vertices
- **loop**: an edge connecting a vertex with itself
- **undirected graph**: a set of vertices and a set of undirected edges each of which is associated with a set of one or two of these vertices
- **simple graph**: an undirected graph with no multiple edges or loops
- **multigraph**: an undirected graph that may contain multiple edges but no loops
- **pseudograph**: an undirected graph that may contain multiple edges and loops
- **directed graph**: a set of vertices together with a set of directed edges each of which is associated with an ordered pair of vertices
- **directed multigraph**: a graph with directed edges that may contain multiple directed edges
- **simple directed graph**: a directed graph without loops or multiple directed edges
- **adjacent**: two vertices are adjacent if there is an edge between them
- **incident**: an edge is incident with a vertex if the vertex is an endpoint of that edge
- **deg $v$** (degree of the vertex $v$ in an undirected graph): the number of edges incident with $v$ with loops counted twice
- **deg$^-$($v$)** (the in-degree of the vertex $v$ in a graph with directed edges): the number of edges with $v$ as their terminal vertex
- **deg$^+$($v$)** (the out-degree of the vertex $v$ in a graph with directed edges): the number of edges with $v$ as their initial vertex
- **underlying undirected graph of a graph with directed edges**: the undirected graph obtained by ignoring the directions of the edges
- **$K_n$** (complete graph on $n$ vertices): the undirected graph with $n$ vertices where each pair of vertices is connected by an edge
- **bipartite graph**: a graph with vertex set that can be partitioned into subsets $V_1$ and $V_2$ so that each edge connects a vertex in $V_1$ and a vertex in $V_2$. The pair $(V_1, V_2)$ is called a bipartition of $V$.
- **$K_{m,n}$** (complete bipartite graph): the graph with vertex set partitioned into a subset of $m$ elements and a subset of $n$ elements with two vertices connected by an edge if and only if one is in the first subset and the other is in the second subset
- **$C_n$** (cycle of size $n$), $n \geq 3$: the graph with $n$ vertices $v_1, v_2, \ldots , v_n$ and edges $\{v_1, v_2\}, \{v_2, v_3\}, \ldots , \{v_{n−1}, v_n\}, \{v_n, v_1\}$
- **$W_n$** (wheel of size $n$), $n \geq 3$: the graph obtained from $C_n$ by adding a vertex and edges from this vertex to the original vertices in $C_n$
- **$Q_n$** ($n$-cube), $n \geq 1$: the graph that has the $2^n$ bit strings of length $n$ as its vertices and edges connecting every pair of bit strings that differ by exactly one bit
- **matching in a graph $G$**: a set of edges such that no two edges have a common endpoint
- **complete matching $M$ from $V_1$ to $V_2$**: a matching such that every vertex in $V_1$ is an endpoint of an edge in $M$
- **maximum matching**: a matching containing the most edges among all matchings in a graph
- **isolated vertex**: a vertex of degree zero
- **pendant vertex**: a vertex of degree one
- **regular graph**: a graph where all vertices have the same degree
- **subgraph of a graph $G = (V, E)$**: a graph $(W, F)$, where $W$ is a subset of $V$ and $F$ is a subset of $E$
- **$G_1 \cup G_2$** (union of $G_1$ and $G_2$): the graph $(V_1 \cup V_2, E_1 \cup E_2)$, where $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$
- **adjacency matrix**: a matrix representing a graph using the adjacency of vertices
- **incidence matrix**: a matrix representing a graph using the incidence of edges and vertices
- **isomorphic simple graphs**: the simple graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are isomorphic if there exists a one-to-one correspondence $f$ from $V_1$ to $V_2$ such that $\{f(v_1), f(v_2)\} \in E_2$ if and only if $\{v_1, v_2\} \in E_1$ for all $v_1$ and $v_2$ in $V_1$
- **invariant for graph isomorphism**: a property that isomorphic graphs either both have or both do not have
- **path from $u$ to $v$ in an undirected graph**: a sequence of edges $e_1, e_2, \ldots , e_n$, where $e_i$ is associated to $\{x_i, x_{i+1}\}$ for $i = 0, 1, \ldots , n$, where $x_0 = u$ and $x_{n+1} = v$
- **path from $u$ to $v$ in a graph with directed edges**: a sequence of edges $e_1, e_2, \ldots , e_n$, where $e_i$ is associated to $(x, x_{i+1})$ for $i = 0, 1, \ldots , n$, where $x_0 = u$ and $x_{n+1} = v$
- **simple path**: a path that does not contain an edge more than once
- **circuit**: a path of length $n \geq 1$ that begins and ends at the same vertex
- **connected graph**: an undirected graph with the property that there is a path between every pair of vertices
- **cut vertex of $G$**: a vertex $v$ such that $G − v$ is disconnected
- **cut edge of $G$**: an edge $e$ such that $G − e$ is disconnected
- **nonseparable graph**: a graph without a cut vertex
- **vertex cut of $G$**: a subset $V'$ of the set of vertices of $G$ such that $G − V'$ is disconnected
- **$ \kappa(G) $** (the vertex connectivity of $G$): the size of a smallest vertex cut of $G$
- **$k$-connected graph**: a graph that has a vertex connectivity no smaller than $k$
- **edge cut of $G$**: a set of edges $E'$ of $G$ such that $G − E'$ is disconnected
- **$ \lambda(G) $** (the edge connectivity of $G$): the size of a smallest edge cut of $G$
- **connected component of a graph $G$**: a maximal connected subgraph of $G$
- **strongly connected directed graph**: a directed graph with the property that there is a directed path from every vertex to every vertex
- **strongly connected component of a directed graph $G$**: a maximal strongly connected subgraph of $G$
- **Euler path**: a path that contains every edge of a graph exactly once
- **Euler circuit**: a circuit that contains every edge of a graph exactly once
- **Hamilton path**: a path in a graph that passes through each vertex exactly once
- **Hamilton circuit**: a circuit in a graph that passes through each vertex exactly once
- **weighted graph**: a graph with numbers assigned to its edges
- **shortest-path problem**: the problem of determining the path in a weighted graph such that the sum of the weights of the edges in this path is a minimum over all paths between specified vertices
- **traveling salesperson problem**: the problem that asks for the circuit of shortest total length that visits every vertex of a weighted graph exactly once
- **planar graph**: a graph that can be drawn in the plane with no crossings
- **regions of a representation of a planar graph**: the regions the plane is divided into by the planar representation of the graph
- **elementary subdivision**: the removal of an edge $\{u, v\}$ of an undirected graph and the addition of a new vertex $w$ together with edges $\{u, w\}$ and $\{w, v\}$
- **homeomorphic**: two undirected graphs are homeomorphic if they can be obtained from the same graph by a sequence of elementary subdivisions
- **graph coloring**: an assignment of colors to the vertices of a graph so that no two adjacent vertices have the same color
- **chromatic number**: the minimum number of colors needed in a coloring of a graph

### RESULTS

- **The handshaking theorem**: If $G = (V, E)$ be an undirected graph with $m$ edges, then $2m = \sum_{v \in V} \text{deg}(v)$.
- **Hall’s marriage theorem**: The bipartite graph $G = (V, E)$ with bipartition $(V_1, V_2)$ has a complete matching from $V_1$ to $V_2$ if and only if $|N(A)| \geq |A|$ for all subsets $A$ of $V_1$.
- **Euler circuit**: There is an Euler circuit in a connected multigraph if and only if every vertex has even degree.
- **Euler path**: There is an Euler path in a connected multigraph if and only if at most two vertices have odd degree.
- **Dijkstra’s algorithm**: a procedure for finding a shortest path between two vertices in a weighted graph (see Section 10.6)
- **Euler’s formula**: $r = e - v + 2$ where $r$, $e$, and $v$ are the number of regions of a planar representation, the number of edges, and the number of vertices, respectively, of a connected planar graph
- **Kuratowski’s theorem**: A graph is nonplanar if and only if it contains a subgraph homeomorphic to $K_{3,3}$ or $K_5$. (Proof beyond the scope of this book.)
- **The four color theorem**: Every planar graph can be colored using no more than four colors. (Proof far beyond the scope of this book!)

## CN

### TERMS

- **undirected edge**: an edge associated to a set $\{u, v\}$, where $u$ and $v$ are vertices
  无向边：与一个顶点集合$\{u, v\}$相关联的边，其中$u$和$v$是顶点。
- **directed edge**: an edge associated to an ordered pair $(u, v)$, where $u$ and $v$ are vertices
  有向边：与一个有序对$(u, v)$相关联的边，其中$u$和$v$是顶点。
- **multiple edges**: distinct edges connecting the same vertices
  多重边：连接相同顶点的不同边。
- **multiple directed edges**: distinct directed edges associated with the same ordered pair $(u,v)$,where $u$ and $v$ are vertices
  多重有向边：与相同有序对$(u,v)$相关联的不同有向边，其中$u$和$v$是顶点。
- **loop**: an edge connecting a vertex with itself
  环：连接顶点自身的边。
- **undirected graph**: a set of vertices and a set of undirected edges each of which is associated with a set of one or two of these vertices
  无向图：一组顶点和一组无向边，每条边都与一个或两个顶点相关联。
- **simple graph**: an undirected graph with no multiple edges or loops
  简单图：没有多重边或环的无向图。
- **multigraph**: an undirected graph that may contain multiple edges but no loops
  多重图：可能包含多重边但没有环的无向图。
- **pseudograph**: an undirected graph that may contain multiple edges and loops
  伪图：可能包含多重边和环的无向图。
- **directed graph**: a set of vertices together with a set of directed edges each of which is associated with an ordered pair of vertices
  有向图：一组顶点和一组有向边，每条边都与一个顶点的有序对相关联。
- **directed multigraph**: a graph with directed edges that may contain multiple directed edges
  有向多重图：包含可能有多重有向边的有向边的图。
- **simple directed graph**: a directed graph without loops or multiple directed edges
  简单有向图：没有环或多重有向边的有向图。
- **adjacent**: two vertices are adjacent if there is an edge between them
  相邻：如果两个顶点之间有一条边，则它们是相邻的。
- **incident**: an edge is incident with a vertex if the vertex is an endpoint of that edge
  关联：如果顶点是边的一个端点，则该边与该顶点关联。
- **deg $v$** (degree of the vertex $v$ in an undirected graph): the number of edges incident with $v$ with loops counted twice
  deg $v$（无向图中顶点$v$的度数）：与$v$关联的边的数量，环计算两次。
- **deg$^-$($v$)** (the in-degree of the vertex $v$ in a graph with directed edges): the number of edges with $v$ as their terminal vertex
  deg$^-$($v$)（有向图中顶点$v$的入度）：以$v$为终点的边的数量。
- **deg$^+$($v$)** (the out-degree of the vertex $v$ in a graph with directed edges): the number of edges with $v$ as their initial vertex
  deg$^+$($v$)（有向图中顶点$v$的出度）：以$v$为起点的边的数量。
- **underlying undirected graph of a graph with directed edges**: the undirected graph obtained by ignoring the directions of the edges
  有向图的底层无向图：通过忽略边的方向得到的无向图。
- **$K_n$** (complete graph on $n$ vertices): the undirected graph with $n$ vertices where each pair of vertices is connected by an edge
  $K_n$（$n$个顶点的完全图）：有$n$个顶点的无向图，每对顶点之间都有一条边相连。
- **bipartite graph**: a graph with vertex set that can be partitioned into subsets $V_1$ and $V_2$ so that each edge connects a vertex in $V_1$ and a vertex in $V_2$. The pair $(V_1, V_2)$ is called a bipartition of $V$.
  二分图：顶点集可以划分为子集$V_1$和$V_2$的图，使得每条边连接$V_1$中的一个顶点和$V_2$中的一个顶点。对$(V_1, V_2)$称为$V$的一个二分。
- **$K_{m,n}$** (complete bipartite graph): the graph with vertex set partitioned into a subset of $m$ elements and a subset of $n$ elements with two vertices connected by an edge if and only if one is in the first subset and the other is in the second subset
  $K_{m,n}$（完全二分图）：顶点集划分为一个包含$m$个元素的子集和一个包含$n$个元素的子集的图，两个顶点之间有边相连当且仅当一个在第一个子集中，另一个在第二个子集中。
- **$C_n$** (cycle of size $n$), $n \geq 3$: the graph with $n$ vertices $v_1, v_2, \ldots , v_n$ and edges $\{v_1, v_2\}, \{v_2, v_3\}, \ldots , \{v_{n−1}, v_n\}, \{v_n, v_1\}$
  $C_n$（大小为$n$的环）：有$n$个顶点$v_1, v_2, \ldots , v_n$和边$\{v_1, v_2\}, \{v_2, v_3\}, \ldots , \{v_{n−1}, v_n\}, \{v_n, v_1\}$的图，其中$n \geq 3$。
- **$W_n$** (wheel of size $n$), $n \geq 3$: the graph obtained from $C_n$ by adding a vertex and edges from this vertex to the original vertices in $C_n$
  $W_n$（大小为$n$的轮）：通过在$C_n$中添加一个顶点以及从这个顶点到$C_n$中原有顶点的边得到的图，其中$n \geq 3$。
- **$Q_n$** ($n$-cube), $n \geq 1$: the graph that has the $2^n$ bit strings of length $n$ as its vertices and edges connecting every pair of bit strings that differ by exactly one bit
  $Q_n$（$n$维立方体）：以长度为$n$的$2^n$位字符串为顶点，连接每对恰好有一位不同的位字符串的边的图，其中$n \geq 1$。
- **matching in a graph $G$**: a set of edges such that no two edges have a common endpoint
  图$G$中的匹配：一组边，使得任意两条边没有共同的端点。
- **complete matching $M$ from $V_1$ to $V_2$**: a matching such that every vertex in $V_1$ is an endpoint of an edge in $M$
  从$V_1$到$V_2$的完全匹配：一个匹配，使得$V_1$中的每个顶点都是$M$中某条边的端点。
- **maximum matching**: a matching containing the most edges among all matchings in a graph
  最大匹配：图中包含边数最多的匹配。
- **isolated vertex**: a vertex of degree zero
  孤立顶点：度数为零的顶点。
- **pendant vertex**: a vertex of degree one
  悬挂顶点：度数为一的顶点。
- **regular graph**: a graph where all vertices have the same degree
  正则图：所有顶点度数相同的图。
- **subgraph of a graph $G = (V, E)$**: a graph $(W, F)$, where $W$ is a subset of $V$ and $F$ is a subset of $E$
  图$G = (V, E)$的子图：图$(W, F)$，其中$W$是$V$的子集，$F$是$E$的子集。
- **$G_1 \cup G_2$** (union of $G_1$ and $G_2$): the graph $(V_1 \cup V_2, E_1 \cup E_2)$, where $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$
  $G_1 \cup G_2$（$G_1$和$G_2$的并）：图$(V_1 \cup V_2, E_1 \cup E_2)$，其中$G_1 = (V_1, E_1)$和$G_2 = (V_2, E_2)$。
- **adjacency matrix**: a matrix representing a graph using the adjacency of vertices
  邻接矩阵：使用顶点的邻接性来表示图的矩阵。
- **incidence matrix**: a matrix representing a graph using the incidence of edges and vertices
  关联矩阵：使用边和顶点的关联性来表示图的矩阵。
- **isomorphic simple graphs**: the simple graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are isomorphic if there exists a one-to-one correspondence $f$ from $V_1$ to $V_2$ such that $\{f(v_1), f(v_2)\} \in E_2$ if and only if $\{v_1, v_2\} \in E_1$ for all $v_1$ and $v_2$ in $V_1$
  同构的简单图：如果存在从$V_1$到$V_2$的一一对应关系$f$，使得对于所有$V_1$中的$v_1$和$v_2$，有$\{f(v_1), f(v_2)\} \in E_2$当且仅当$\{v_1, v_2\} \in E_1$，则简单图$G_1 = (V_1, E_1)$和$G_2 = (V_2, E_2)$是同构的。
- **invariant for graph isomorphism**: a property that isomorphic graphs either both have or both do not have
  图同构的不变量：同构图要么都具有的性质，要么都不具有的性质。
- **path from $u$ to $v$ in an undirected graph**: a sequence of edges $e_1, e_2, \ldots , e_n$, where $e_i$ is associated to $\{x_i, x_{i+1}\}$ for $i = 0, 1, \ldots , n$, where $x_0 = u$ and $x_{n+1} = v$
  无向图中从$u$到$v$的路径：边的序列$e_1, e_2, \ldots , e_n$，其中$e_i$与$\{x_i, x_{i+1}\}$相关联，对于$i = 0, 1, \ldots , n$，其中$x_0 = u$和$x_{n+1} = v$。
- **path from $u$ to $v$ in a graph with directed edges**: a sequence of edges $e_1, e_2, \ldots , e_n$, where $e_i$ is associated to $(x, x_{i+1})$ for $i = 0, 1, \ldots , n$, where $x_0 = u$ and $x_{n+1} = v$
  有向图中从$u$到$v$的路径：边的序列$e_1, e_2, \ldots , e_n$，其中$e_i$与$(x, x_{i+1})$相关联，对于$i = 0, 1, \ldots , n$，其中$x_0 = u$和$x_{n+1} = v$。
- **simple path**: a path that does not contain an edge more than once
  简单路径：不包含多于一次的边的路径。
- **circuit**: a path of length $n \geq 1$ that begins and ends at the same vertex
  回路：长度为$n \geq 1$的路径，起始和结束于同一个顶点。
- **connected graph**: an undirected graph with the property that there is a path between every pair of vertices
  连通图：每对顶点之间都存在路径的无向图。
- **cut vertex of $G$**: a vertex $v$ such that $G − v$ is disconnected
  图$G$的割点：一个顶点$v$，使得$G − v$不连通。
- **cut edge of $G$**: an edge $e$ such that $G − e$ is disconnected
  图$G$的割边：一条边$e$，使得$G − e$不连通。
- **nonseparable graph**: a graph without a cut vertex
  非分离图：没有割点的图。
- **vertex cut of $G$**: a subset $V'$ of the set of vertices of $G$ such that $G − V'$ is disconnected
  图$G$的顶点割：$G$的顶点集的一个子集$V'$，使得$G − V'$不连通。
- **$ \kappa(G) $** (the vertex connectivity of $G$): the size of a smallest vertex cut of $G$
  $ \kappa(G) $（图$G$的顶点连通度）：$G$的最小顶点割的大小。
- **$k$-connected graph**: a graph that has a vertex connectivity no smaller than $k$
  $k$-连通图：顶点连通度不小于$k$的图。
- **edge cut of $G$**: a set of edges $E'$ of $G$ such that $G − E'$ is disconnected
  图$G$的边割：$G$的一组边$E'$，使得$G − E'$不连通。
- **$ \lambda(G) $** (the edge connectivity of $G$): the size of a smallest edge cut of $G$
  $ \lambda(G) $（图$G$的边连通度）：$G$的最小边割的大小。
- **connected component of a graph $G$**: a maximal connected subgraph of $G$
  图$G$的连通分量：$G$的一个最大连通子图。
- **strongly connected directed graph**: a directed graph with the property that there is a directed path from every vertex to every vertex
  强连通有向图：每对顶点之间都存在有向路径的有向图。
- **strongly connected component of a directed graph $G$**: a maximal strongly connected subgraph of $G$
  有向图$G$的强连通分量：$G$的一个最大强连通子图。
- **Euler path**: a path that contains every edge of a graph exactly once
  欧拉路径：包含图中每条边恰好一次的路径。
- **Euler circuit**: a circuit that contains every edge of a graph exactly once
  欧拉回路：包含图中每条边恰好一次的回路。
- **Hamilton path**: a path in a graph that passes through each vertex exactly once
  哈密顿路径：图中恰好经过每个顶点一次的路径。
- **Hamilton circuit**: a circuit in a graph that passes through each vertex exactly once
  哈密顿回路：图中恰好经过每个顶点一次的回路。
- **weighted graph**: a graph with numbers assigned to its edges
  加权图：边被赋予数字的图。
- **shortest-path problem**: the problem of determining the path in a weighted graph such that the sum of the weights of the edges in this path is a minimum over all paths between specified vertices
  最短路径问题：确定加权图中一条路径，使得该路径上边的权重之和在所有指定顶点之间的路径中最小。
- **traveling salesperson problem**: the problem that asks for the circuit of shortest total length that visits every vertex of a weighted graph exactly once
  旅行商问题：要求找出加权图中总长度最短的回路，该回路恰好访问每个顶点一次。
- **planar graph**: a graph that can be drawn in the plane with no crossings
  平面图：可以在平面上画出且没有交叉的图。
- **regions of a representation of a planar graph**: the regions the plane is divided into by the planar representation of the graph
  平面图表示的区域：平面图表示将平面划分成的区域。
- **elementary subdivision**: the removal of an edge $\{u, v\}$ of an undirected graph and the addition of a new vertex $w$ together with edges $\{u, w\}$ and $\{w, v\}$
  基本细分：移除无向图的一条边$\{u, v\}$，并添加一个新顶点$w$以及边$\{u, w\}$和$\{w, v\}$。
- **homeomorphic**: two undirected graphs are homeomorphic if they can be obtained from the same graph by a sequence of elementary subdivisions
  同胚：如果两个无向图可以通过一系列基本细分从同一个图获得，则它们是同胚的。
- **graph coloring**: an assignment of colors to the vertices of a graph so that no two adjacent vertices have the same color
  图着色：给图的顶点分配颜色，使得没有两个相邻的顶点有相同的颜色。
- **chromatic number**: the minimum number of colors needed in a coloring of a graph
  色数：图着色所需的最小颜色数。

### RESULTS

- **The handshaking theorem**: If $G = (V, E)$ be an undirected graph with $m$ edges, then $2m = \sum_{v \in V} \text{deg}(v)$.
  握手定理：如果$G = (V, E)$是一个有$m$条边的无向图，那么$2m = \sum_{v \in V} \text{deg}(v)$。
- **Hall’s marriage theorem**: The bipartite graph $G = (V, E)$ with bipartition $(V_1, V_2)$ has a complete matching from $V_1$ to $V_2$ if and only if $|N(A)| \geq |A|$ for all subsets $A$ of $V_1$.
  霍尔婚姻定理：二分图$G = (V, E)$有一个从$V_1$到$V_2$的完全匹配当且仅当对于所有$V_1$的子集$A$，有$|N(A)| \geq |A|$。
- **Euler circuit**: There is an Euler circuit in a connected multigraph if and only if every vertex has even degree.
  欧拉回路：一个连通多重图有欧拉回路当且仅当每个顶点的度数都是偶数。
- **Euler path**: There is an Euler path in a connected multigraph if and only if at most two vertices have odd degree.
  欧拉路径：一个连通多重图有欧拉路径当且仅当最多有两个顶点的度数是奇数。
- **Dijkstra’s algorithm**: a procedure for finding a shortest path between two vertices in a weighted graph (see Section 10.6)
  迪杰斯特拉算法：在加权图中寻找两个顶点之间最短路径的程序（见第10.6节）。
- **Euler’s formula**: $r = e - v + 2$ where $r$, $e$, and $v$ are the number of regions of a planar representation, the number of edges, and the number of vertices, respectively, of a connected planar graph
  欧拉公式：$r = e - v + 2$，其中$r$、$e$和$v$分别是连通平面图的平面表示的区域数、边数和顶点数。
- **Kuratowski’s theorem**: A graph is nonplanar if and only if it contains a subgraph homeomorphic to $K_{3,3}$ or $K_5$. (Proof beyond the scope of this book.)
  库拉托夫斯基定理：一个图是非平面的当且仅当它包含一个与$K_{3,3}$或$K_5$同胚的子图。（证明超出了本书的范围。）
- **The four color theorem**: Every planar graph can be colored using no more than four colors. (Proof far beyond the scope of this book!)
  四色定理：每个平面图都可以用不超过四种颜色着色。（证明远远超出了本书的范围！）
  ``
