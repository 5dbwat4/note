# The disjoint set ADT

**不相交集合抽象数据类型（Disjoint Set ADT）**，也称为**并查集**（Union-Find），是一种用于管理一组动态集合的数据结构。它支持高效地合并集合（Union）和查询元素所属集合（Find），常用于处理元素之间的连通性问题。


## 等价关系 Equivalence Relations
A relation $R$ is defined on a set $S$ if for every pair of elements $(a, b), a, b\in S$, $a R b$ is either true or false. If $a R b$ is true, then we say that $a$ is related to $b$.

An equivalence relation is a relation $R$ that satisfies three properties:
1. **(Reflexive)**: $a R a$, for all $a\in S$.
2. **(Symmetric)**: $a R b$ if and only if $b R a$.
3. **(Transitive)**: $a R b$ and $b R c$ implies that $a R c$.

在集合 $S$ 上定义一个关系 $R$，是指对于任意元素对 $(a, b)$（其中 $a, b\in S$），命题 $a R b$ 要么为真，要么为假。若 $a R b$ 为真，则称 $a$ 与 $b$ 相关。

**等价关系**是满足以下三个性质的关系 $R$：  
1. **自反性**：对于所有 $a\in S$，有 $a R a$。  
2. **对称性**：$a R b$ 当且仅当 $b R a$。  
3. **传递性**：若 $a R b$ 且 $b R c$，则 $a R c$。

并查集用来处理此类**动态等价性问题**

## The array representation

1. **父指针数组（Parent Array）**  
   使用数组 `parent[]` 表示每个元素的父节点，其中：
   - 若 `parent[i] = j`，则 `i` 的父节点是 `j`。
   - 若 `parent[i] = -k`（负数），则 `i` 是根节点，且集合的秩（高度或大小）为 `k`。

2. **初始化**  
   初始时，每个元素独立为一个集合，父节点指向自己，秩为 1。  
   例如，5 个元素的初始化数组为：  
   `parent = [-1, -1, -1, -1, -1]`。

   并查集（Disjoint Set ADT）是一种用于管理不相交集合的数据结构，支持高效的合并（Union）和查询（Find）操作。为提高效率，常采用以下两种优化方法：

## Smart Union
在合并两个集合时，若随意将一棵树连接到另一棵树的根节点下，可能导致树的高度急剧增加，从而降低操作效率。智能合并算法通过以下两种策略优化合并过程：

**（1）按大小合并（Union by Size）**
• **原理**：每个集合的根节点记录该集合的**节点总数**。合并时，**将较小集合的根连接到较大集合的根下**。
• **优势**：避免树高度不必要的增长，确保树的最大高度为 $O(\log n)$。

**（2）按秩合并（Union by Rank）**
• **原理**：每个集合的根节点记录**秩（Rank）**，通常表示树高度的上界。合并时，**将秩较小的树的根连接到秩较大的树的根下**；若两树秩相同，则任选一树作为根，并使其秩加1。
• **优势**：秩是高度的近似值，维护成本低，配合路径压缩时更高效。



## 实现

```c
SetType  Find ( ElementType  X, DisjSet  S )
{   ElementType  root,  trail,  lead;
    for ( root = X; S[ root ] > 0; root = S[ root ] )
        ;  /* find the root */
    for ( trail = X; trail != root; trail = lead ) {
       lead = S[ trail ] ;   
       S[ trail ] = root ;   
    }  /* collapsing */
    return  root ;
}
```
