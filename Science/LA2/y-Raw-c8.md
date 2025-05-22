## 8.1 递增的零空间序列

设 $T \in L(V)$。那么

$$
\{0\} = \text{null} \ T^0 \subseteq \text{null} \ T^1 \subseteq \cdots \subseteq \text{null} \ T^i \subseteq \text{null} \ T^{i+1} \subseteq \cdots
$$

## 8.2 零空间序列中的等式

设 $T \in L(V)$，$m$ 是非负整数，满足

$$
\text{null} \ T^m = \text{null} \ T^{m+1}
$$

那么

$$
\text{null} \ T^m = \text{null} \ T^{m+1} = \text{null} \ T^{m+2} = \text{null} \ T^{m+3} = \cdots
$$

## 8.3 零空间停止增长

设 $T \in L(V)$。那么

$$
\text{null} \ T^{\dim V} = \text{null} \ T^{\dim V + 1} = \text{null} \ T^{\dim V + 2} = \cdots
$$

## 8.4 $V$ 是 $\text{null} \ T^{\dim V}$ 和 $\text{range} \ T^{\dim V}$ 的直和

设 $T \in L(V)$。那么

$$
V = \text{null} \ T^{\dim V} \oplus \text{range} \ T^{\dim V}
$$

## 8.8 定义：广义特征向量（generalized eigenvector）

设 $T \in L(V)$，$\lambda$ 是 $T$ 的特征值。称向量 $v \in V$ 是 $T$ 对应于 $\lambda$ 的广义特征向量，若 $v \neq 0$ 且对某个正整数 $i$ 有

$$
(T - \lambda I)^i v = 0
$$

## 8.9 由广义特征向量构成的基

设 $F = \mathbb{C}$ 且 $T \in L(V)$。那么存在由 $T$ 的广义特征向量构成的 $V$ 的基。

## 8.11 广义特征向量对应于唯一的特征值

设 $T \in L(V)$。那么 $T$ 的每个广义特征向量都仅对应于 $T$ 的一个特征值。

## 8.12 线性无关的广义特征向量

设 $T \in L(V)$。那么由对应于 $T$ 的互异特征值的广义特征向量构成的每个向量组都是线性无关的。

## 8.14 定义：幂零（nilpotent）

称一个算子是幂零的，如果它的某个幂等于 0。

## 8.16 $n$ 维空间上幂零算子的 $n$ 次幂等于 0

设 $T \in L(V)$ 是幂零的。那么 $T^{\dim V} = 0$。

## 8.17 幂零算子的特征值

设 $T \in L(V)$。

(a) 如果 $T$ 是幂零的，那么 0 是 $T$ 的特征值，并且 $T$ 没有其他的特征值。

(b) 若 $F = \mathbb{C}$，且 0 是 $T$ 的唯一特征值，那么 $T$ 是幂零的。

## 8.18 幂零算子的最小多项式和上三角矩阵

设 $T \in L(V)$。那么下面各命题等价。

(a) $T$ 是幂零的。

(b) $T$ 的最小多项式等于 $p^m$（$m$ 为正整数）。

(c) 存在 $V$ 的一个基，使得 $T$ 关于该基的矩阵形如

$$
\begin{bmatrix}
0 & * & \cdots \\
0 & 0 & \\
\end{bmatrix}
$$

其中对角线及对角线下方各元素均等于 0。

## 8.19 定义：广义特征空间（generalized eigenspace）、$G(\lambda, T)$

设 $T \in L(V)$ 且 $\lambda \in F$。$T$ 对应于 $\lambda$ 的广义特征空间，记作 $G(\lambda, T)$，定义为

$$
G(\lambda, T) = \{ v \in V : (T - \lambda I)^i v = 0, \ i \text{ 为某正整数} \}
$$

## 8.20 广义特征空间的描述

设 $T \in L(V)$ 且 $\lambda \in F$。那么 $G(\lambda, T) = \text{null} \ (T - \lambda I)^{\dim V}$。

## 8.22 广义特征空间分解

设 $F = \mathbb{C}$ 且 $T \in L(V)$。令 $\lambda_1, \ldots, \lambda_m$ 是 $T$ 的互异特征值。那么

(a) 对每个 $i = 1, \ldots, m$，$G(\lambda_i, T)$ 在 $T$ 下是不变的；

(b) 对每个 $i = 1, \ldots, m$，$(T - \lambda_i I)|_{G(\lambda_k, V)}$ 是幂零的；

(c) $V = G(\lambda_1, T) \oplus \cdots \oplus G(\lambda_m, T)$。

## 8.23 定义：重数（multiplicity）

设 $T \in L(V)$。定义 $T$ 的特征值 $\lambda$ 的重数为其对应的广义特征空间 $G(\lambda, T)$ 的维数。换言之，$T$ 的特征值 $\lambda$ 的重数等于

$$
\dim \ \text{null} \ (T - \lambda I)^{\dim V}
$$

## 8.25 重数之和等于 $\dim V$

设 $F = \mathbb{C}$ 且 $T \in L(V)$。那么 $T$ 的所有特征值的重数之和等于 $\dim V$。

## 8.26 定义：特征多项式（characteristic polynomial）

设 $F = \mathbb{C}$ 且 $T \in L(V)$。令 $\lambda_1, \ldots, \lambda_m$ 表示 $T$ 的互异特征值，且其重数分别为 $a_1, \ldots, a_m$。称多项式

$$
(p - \lambda_1)^{b_1} \cdots (p - \lambda_m)^{b_m}
$$

为 $T$ 的特征多项式。

## 8.28 特征多项式的次数和零点

设 $F = \mathbb{C}$ 且 $T \in L(V)$。那么

(a) $T$ 的特征多项式的次数是 $\dim V$；

(b) $T$ 的特征多项式的零点就是 $T$ 的特征值。

## 8.29 凯莱 - 哈密尔顿定理（Cayley - Hamilton theorem）

设 $F = \mathbb{C}$，$T \in L(V)$，且 $p$ 是 $T$ 的特征多项式。那么 $p(T) = 0$。

## 8.30 特征多项式是最小多项式的多项式倍

设 $F = \mathbb{C}$ 且 $T \in L(V)$。那么 $T$ 的特征多项式是 $T$ 的最小多项式的多项式倍。

## 8.31 特征值的重数等于其在对角线上出现的次数

设 $F = \mathbb{C}$ 且 $T \in L(V)$。设 $v_1, \ldots, v_n$ 是 $T$ 的一个基且使得 $M(T, (v_1, \ldots, v_n))$ 为上三角矩阵。那么 $T$ 的每个特征值 $\lambda$ 在 $M(T, (v_1, \ldots, v_n))$ 对角线上出现的次数，就等于 $\lambda$ 作为 $T$ 的特征值的重数。

## 8.35 定义：分块对角矩阵（block diagonal matrix）

一个分块对角矩阵是形如

$$
\begin{bmatrix}
A_1 & 0 & \cdots \\
0 & A_2 & \\
\end{bmatrix}
$$

的方阵，其中 $A_1, \ldots, A_m$ 是排列在对角线上的方阵，且矩阵其他各元素都等于 0。

## 8.37 由上三角块构成的分块对角矩阵

设 $F = \mathbb{C}$ 且 $T \in L(V)$。令 $\lambda_1, \ldots, \lambda_m$ 是 $T$ 的互异特征值，它们的重数分别为 $a_1, \ldots, a_m$。那么存在 $V$ 的一个基，使得 $T$ 关于该基具有形如

$$
\begin{bmatrix}
A_1 & 0 & \cdots \\
0 & A_2 & \\
\end{bmatrix}
$$

的分块对角矩阵，其中各 $A_i$ 是形如

$$
A_i = \begin{bmatrix}
\lambda_i & * & \cdots \\
0 & \lambda_i & \\
\end{bmatrix}
$$

的 $a_i \times a_i$ 上三角矩阵。
