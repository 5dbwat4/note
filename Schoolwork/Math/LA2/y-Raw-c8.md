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



## 8.39 恒等算子加上幂零算子有平方根
设 $T \in L(V)$ 是幂零的。那么 $I + T$ 有平方根。

## 8.41 $\mathbb{C}$ 上，可逆算子具有平方根
设 $V$ 是复向量空间，$T \in L(V)$ 是可逆的。那么 $T$ 有平方根。

## 8.42 例：具有很好的矩阵的幂零算子
设 $T$ 是 $\mathbb{C}^4$ 上定义为
$$
T(p_1, p_2, p_3, p_4) = (0, p_1, p_2, p_3)
$$
的算子。那么 $T^4 = 0$，从而 $T$ 是幂零的。若 $p = (1, 0, 0, 0)$，那么 $T^3p, T^2p, Tp, p$ 是 $\mathbb{C}^4$ 的基。$T$ 关于该基的矩阵是
$$
\begin{bmatrix}
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0
\end{bmatrix}
$$

## 8.43 例：具有稍复杂点的矩阵的幂零算子
设 $T$ 是 $\mathbb{C}^6$ 上定义为
$$
T(p_1, p_2, p_3, p_4, p_5, p_6) = (0, p_1, p_2, 0, p_4, 0)
$$
的算子。那么 $T^3 = 0$，从而 $T$ 是幂零的。该算子不像上例中的幂零算子那样容易处理，因为并不存在向量 $p \in \mathbb{C}^6$ 使得 $T^5p, T^4p, T^3p, T^2p, Tp, p$ 是 $\mathbb{C}^6$ 的一个基。然而，如果我们取 $p_1 = (1, 0, 0, 0, 0, 0), p_2 = (0, 0, 0, 1, 0, 0), p_3 = (0, 0, 0, 0, 0, 1)$，那么 $T^2p_1, Tp_1, p_1, Tp_2, p_2, p_3$ 是 $\mathbb{C}^6$ 的一个基。$T$ 关于该基的矩阵是
$$
\begin{bmatrix}
0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0
\end{bmatrix}
$$

## 8.44 定义：若当基（Jordan basis）
设 $T \in L(V)$。称 $V$ 的一个基是 $T$ 的若当基，如果 $T$ 关于该基具有分块对角矩阵
$$
\begin{bmatrix}
A_1 & 0 & \cdots & 0 \\
0 & A_2 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & A_p
\end{bmatrix}
$$
其中各 $A_i$ 是形如
$$
A_i = \begin{bmatrix}
\lambda_i & 1 & 0 & \cdots & 0 \\
0 & \lambda_i & 1 & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \cdots & \lambda_i
\end{bmatrix}
$$
的上三角矩阵。

## 8.45 每个幂零算子都有若当基
设 $T \in L(V)$ 是幂零的。那么 $V$ 中有一个基是 $T$ 的若当基。

## 8.46 若当型（Jordan form）
设 $F = \mathbb{C}$ 且 $T \in L(V)$。那么 $V$ 有一个基是 $T$ 的若当基。

## 8.47 定义：矩阵的迹（trace of a matrix）
设 $A$ 是各元素均属于 $F$ 的方阵。$A$ 的迹，记为 $\text{tr} A$，定义为 $A$ 对角线上各元素之和。

## 8.48 例：一个 $3 \times 3$ 矩阵的迹
设
$$
A = \begin{bmatrix}
3 & -1 & -2 \\
3 & 2 & -3 \\
1 & 2 & 0
\end{bmatrix}
$$
$A$ 对角线上的元素是 3、2 和 0，以红色标出。于是 $\text{tr} A = 3 + 2 + 0 = 5$。

## 8.49 $AA'$ 的迹等于 $A'A$ 的迹
设 $A$ 是 $m \times n$ 矩阵且 $A'$ 是 $n \times m$ 矩阵。那么
$$
\text{tr}(AA') = \text{tr}(A'A)
$$

## 8.50 算子的矩阵的迹不依赖于基的选取
设 $T \in L(V)$。设 $v_1, \ldots, v_n$ 和 $u_1, \ldots, u_n$ 是 $V$ 的基。那么
$$
\text{tr} M(T, (v_1, \ldots, v_n)) = \text{tr} M(T, (u_1, \ldots, u_n))
$$

## 8.51 定义：算子的迹（trace of an operator）
设 $T \in L(V)$。$T$ 的迹，记作 $\text{tr} T$，定义为
$$
\text{tr} T = \text{tr} M(T, (v_1, \ldots, v_n))
$$
其中 $v_1, \ldots, v_n$ 是 $V$ 的任意一个基。

## 8.52 在复向量空间上，迹等于特征值之和
设 $F = \mathbb{C}$ 且 $T \in L(V)$。那么 $\text{tr} T$ 等于 $T$ 的特征值之和，其中各特征值出现次数等于其重数。

## 8.53 例：$\mathbb{C}^3$ 上一个算子的迹
定义 $T \in L(\mathbb{C}^3)$ 为
$$
T(p_1, p_2, p_3) = (3p_1 - p_2 - 2p_3, 3p_1 + 2p_2 - 3p_3, p_1 + 2p_2)
$$
$T$ 关于 $\mathbb{C}^3$ 的标准基的矩阵是
$$
\begin{bmatrix}
3 & -1 & -2 \\
3 & 2 & -3 \\
1 & 2 & 0
\end{bmatrix}
$$
求该矩阵对角线上各元素的和，我们可见 $\text{tr} T = 5$。
$T$ 的特征值是 1, $2 + 3i$, $2 - 3i$，它们的重数都是 1（你可自行验证）。这些特征值之和（其中各特征值出现次数等于其重数）是 $1 + (2 + 3i) + (2 - 3i)$，等于 5，正如 8.52 所言。

## 8.54 迹与特征多项式
设 $F = \mathbb{C}$ 且 $T \in L(V)$。令 $n = \dim V$。那么 $\text{tr} T$ 等于 $T$ 的特征多项式中 $p^{n-1}$ 项的系数的相反数。

## 8.55 内积空间上的迹
设 $V$ 是内积空间，$T \in L(V)$，$e_1, \ldots, e_n$ 是 $V$ 的规范正交基。则
$$
\text{tr} T = \langle T e_1, e_1 \rangle + \cdots + \langle T e_n, e_n \rangle
$$

## 8.56 迹是线性的
函数 $\text{tr} : L(V) \to F$ 是 $L(V)$ 上的线性泛函，且使
$$
\text{tr}(ST) = \text{tr}(TS)
$$
对所有 $S, T \in L(V)$ 都成立。

## 8.57 恒等算子不等于 $ST - TS$
不存在使得 $ST - TS = I$ 成立的算子 $S, T \in L(V)$。