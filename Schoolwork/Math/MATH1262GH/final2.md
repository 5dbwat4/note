
# 线性代数辅学讲义

## 一、若当标准型

### 1.1 广义特征向量 广义线性空间

#### 1.1.1 核空间的性质

**定理 1** 设 $\sigma \in \mathcal{L}(V)$，则有
1. $\{0\} = \ker \sigma^0 \subset \ker \sigma^1 \subset \ker \sigma^2 \subset \cdots \subset \ker \sigma^k \subset \ker \sigma^{k+1} \subset \cdots$;
2. 设 $m$ 是满足 $\ker \sigma^m = \ker \sigma^{m+1}$ 的非负整数，则
$\ker \sigma^m = \ker \sigma^{m+1} = \ker \sigma^{m+2} = \cdots$;
3. 设 $n = \dim V$，则 $\ker \sigma^n = \ker \sigma^{n+1} = \cdots$.

**定理 2** 设 $\sigma \in \mathcal{L}(V)$，$n = \dim V$，则 $V = \ker \sigma^n \oplus \operatorname{im} \sigma^n$.

#### 1.1.2 广义特征空间

**定义 1** 设 $\sigma \in \mathcal{L}(V)$，$\lambda \in \mathbb{F}$ 为 $\sigma$ 的特征值，$n = \dim V$。如果对于向量 $v \neq 0$ 存在正整数 $j$ 使得 $(\sigma - \lambda I)^j v = 0$，则称 $v$ 为 $\sigma$ 对应于 $\lambda$ 的广义特征向量。 $\sigma$ 对应于 $\lambda$ 的全体广义特征向量与零向量构成的集合称为 $\sigma$ 对应于 $\lambda$ 的广义特征空间 $G(\lambda, \sigma)$.

**定理 3** 设 $\sigma \in \mathcal{L}(V)$，$n = \dim V$，$\lambda_1, \cdots, \lambda_m$ 为 $\sigma$ 所有互异的特征值。则
1. $(\sigma - \lambda_j I)|_{G(\lambda_j,\sigma)}$ 都是幂零的.
2. 每个 $G(\lambda_j, \sigma)$ 都是 $\sigma$ 的不变子空间.
3. 设 $v_1, \cdots, v_m$ 为任意对应于 $\lambda_1, \cdots, \lambda_m$ 的广义特征向量，则 $v_1, \cdots, v_m$ 线性无关.
4. $V = G(\lambda_1, \sigma) \oplus \cdots \oplus G(\lambda_m, \sigma)$.

### 1.2 多项式的进一步讨论

#### 1.2.1 特征多项式 Hamilton-Cayley 定理

**定理 4** 设 $V$ 是复向量空间，$V_1, V_2, \cdots, V_m$ 都是 $V$ 的非零子空间，并且满足 $V = V_1 \oplus \cdots \oplus V_m$。设 $\sigma \in \mathcal{L}(V)$，$V_j$ 在 $\sigma$ 下不变，并且定义 $f_j$ 为 $\sigma|_{V_j}$ 的特征多项式，则 $\sigma$ 的特征多项式 $f$ 满足
$$
f = f_1 \cdots f_m.
$$

**推论 5** 设 $\sigma \in \mathcal{L}(V)$，$\lambda_i \in \mathbb{F}$ 为 $\sigma$ 的特征值，$d_i$ 为 $\lambda_i$ 的代数重数，则 $\lambda_i$ 对应的广义特征空间 $G(\lambda_i, \sigma)$ 的维数也是 $d_i$.

**定义 2** 设 $\sigma \in \mathcal{L}(V)$，若 $p \in \mathbb{F}[x]$ 使得 $p(\sigma) = 0$，则称 $p$ 为 $\sigma$ 的一个零化多项式.

**定理 6** （Hamilton-Cayley 定理）设 $V$ 是复向量空间，$\sigma \in \mathcal{L}(V)$，$q$ 为 $\sigma$ 的特征多项式，则 $q(\sigma) = 0$.

#### 1.2.2 极小多项式

**定义 3** 设 $\sigma \in \mathcal{L}(V)$，$\sigma$ 的极小多项式是唯一一个满足 $p(\sigma) = 0$ 的次数最小的首一多项式.

**定理 7** 设 $\sigma \in \mathcal{L}(V)$，$p$ 是 $\sigma$ 的极小多项式.
1. 若 $q \in \mathbb{F}[x]$，则 $q(\sigma) = 0$ 当且仅当 $q$ 是 $p$ 的多项式倍.
2. 若 $\mathbb{F} = \mathbb{C}$，则 $\sigma$ 的特征多项式 $f$ 是 $p$ 的多项式倍.

**定理 8** 设 $\sigma \in \mathcal{L}(V)$，则 $\sigma$ 的极小多项式的零点均是 $\sigma$ 的特征值.

**定理 9** 设 $\sigma \in \mathcal{L}(V)$，$V$ 能分解为 $\sigma$ 的一些非平凡的不变子空间的直和
$$
V = U_1 \oplus \cdots \oplus U_m,
$$
且 $\sigma|_{U_i}$ 的极小多项式为 $p_i$，则 $\sigma$ 的极小多项式为
$$
p = \operatorname{lcm}(p_1, \cdots, p_m).
$$
其中 $\operatorname{lcm}(p_1, \cdots, p_m)$ 表示 $p_1, \cdots, p_m$ 的最小公倍式.

**例 1** 判断命题真伪: $T \in \mathcal{L}(V)$ 是非幂零算子，满足 $\ker T^{n-1} \neq \ker T^{n-2}$。则其极小多项式为
$$
m(\lambda) = \lambda^{n-1}(\lambda - a) \quad (0 \neq a \in \mathbb{R}).
$$

### 1.3 若当标准型的求解

**例 2** 设 $T$ 为复数域上 $n$ 维线性空间 $V$ 上的线性变换，$T$ 在某组基下的对应矩阵是
$$

\begin{pmatrix}
-6 & 2 & -12 \\
2 & 0 & 4 \\
3 & 1 & 6
\end{pmatrix},

$$
是否存在线性变换 $S$ 满足 $S^2 = T$？假如存在求 $S$，假如不存在，说明理由，并求 $T$ 的极小多项式以及若当标准型.

## 二、内积空间上的算子

### 2.1 内积空间的同构 伴随

**定义 4** 设 $V$ 和 $U$ 是 $\mathbb{F}$ 上的内积空间，线性映射 $\sigma: V \to U$ 满足 $\forall v_1, v_2 \in V$，$\langle \sigma v_1, \sigma v_2 \rangle_U = \langle v_1, v_2 \rangle_V$，则称 $\sigma$ 是一个保持内积的线性映射。若 $\sigma$ 是双射，则称 $\sigma$ 是一个保积同构.

**定理 10** 设 $V$ 和 $U$ 是 $\mathbb{F}$ 上的内积空间，$\dim V = \dim U = n$，若 $\sigma: V \to U$ 是一个线性映射，则以下条件等价：
1. $\sigma$ 是一个保积同构;
2. $\sigma$ 将 $V$ 的任意一组标准正交基映射为 $U$ 的一组标准正交基;
3. $\sigma$ 将 $V$ 的某一组标准正交基映射为 $U$ 的一组标准正交基.

**定义 5** 设 $\sigma \in \mathcal{L}(V, W)$，$\sigma$ 的伴随 $\sigma^*: W \to V$ 满足 $\forall v \in V$，$w \in W$，
$$
\langle \sigma v, w \rangle_W = \langle v, \sigma^* w \rangle_V.
$$

**定理 11** 设 $\sigma \in \mathcal{L}(V)$：
1. 若 $\lambda \in \mathbb{F}$，则 $\lambda$ 是 $\sigma$ 的特征值当且仅当 $\lambda$ 是 $\sigma^*$ 的特征值;
2. 若 $U$ 是 $V$ 的子空间，则 $U$ 是 $\sigma$ 的不变子空间当且仅当 $U^\perp$ 是 $\sigma^*$ 的不变子空间.

**定义 6** 设 $V$ 是 $\mathbb{F}$ 上的内积空间，$\sigma \in \mathcal{L}(V)$ 保持内积，若 $\mathbb{F} = \mathbb{R}$ 则称 $\sigma$ 为正交变换，若 $\mathbb{F} = \mathbb{C}$ 则称 $\sigma$ 为酉变换.

**定理 12** 设 $V$ 是 $\mathbb{F}$ 上的内积空间，$\sigma \in \mathcal{L}(V)$ 是保积自同构等价于 $\sigma$ 可逆，并且 $\sigma^* = \sigma^{-1}$.

**定理 13** 设 $\sigma$ 为保积自同构，$\lambda$ 是 $\sigma$ 的特征值，则 $|\lambda| = 1$.

### 2.2 自伴算子

**定理 14** 设 $(e_1, e_2, \ldots, e_n)$ 为复（实）内积空间 $V$ 的一组标准正交基，$(f_1, f_2, \ldots, f_n)$ 是 $V$ 上的一组基，记 $(e_1, e_2, \ldots, e_n)$ 到 $(f_1, f_2, \ldots, f_n)$ 的过渡矩阵为 $P$，则 $(f_1, f_2, \ldots, f_n)$ 是 $V$ 的一组标准正交基当且仅当 $P$ 是酉（正交）矩阵.

**定义 7**
1. 酉相似：复内积空间上，若 $B = P^{-1} A P = P^H A P$，则称矩阵 $A$ 和 $B$ 酉相似.
2. 正交相似：实内积空间上，若 $B = P^{-1} A P = P^T A P$，则称矩阵 $A$ 和 $B$ 正交相似.

**定义 8** $\sigma \in \mathcal{L}(V)$ 满足 $\sigma^* = \sigma$，则称 $\sigma$ 为自伴算子.

**定理 15** 自伴算子的特征值都是实数.

**定理 16** 设 $\sigma \in \mathcal{L}(V)$ 是自伴算子，$U$ 是 $\sigma$ 的不变子空间，则：
1. $U^\perp$ 是 $\sigma$ 的不变子空间;
2. $\sigma|_U \in \mathcal{L}(U)$ 是自伴算子;
3. $\sigma|_{U^\perp} \in \mathcal{L}(U^\perp)$ 是自伴算子.

**定理 17** （实谱定理）设 $\sigma \in \mathcal{L}(V)$，$\mathbb{F} = \mathbb{R}$，则以下条件等价：
1. $\sigma$ 是自伴算子;
2. $V$ 有一个由 $\sigma$ 的特征向量构成的标准正交基;
3. $\sigma$ 关于 $V$ 的某组标准正交基具有对角矩阵.

### 2.3 正规算子

**定义 9** $\sigma \in \mathcal{L}(V)$ 满足 $\sigma^* \sigma = \sigma \sigma^*$，则称 $\sigma$ 为正规算子.

#### 2.3.1 复正规算子

**定理 18** 设 $\sigma \in \mathcal{L}(V)$ 是正规算子，$v \in V$ 是 $\sigma$ 对应于 $\lambda$ 的特征向量，则 $v$ 是 $\sigma^*$ 对应于 $\lambda$ 的特征向量.

**定理 19** 设 $\sigma \in \mathcal{L}(V)$ 是正规算子，则 $\sigma$ 相应于不同特征值的特征向量是正交的.

**定理 20** （复谱定理）设 $\sigma \in \mathcal{L}(V)$，$\mathbb{F} = \mathbb{C}$，则以下条件等价：
1. $\sigma$ 是正规算子;
2. $V$ 有一个由 $\sigma$ 的特征向量构成的标准正交基;
3. $\sigma$ 关于 $V$ 的某组标准正交基具有对角矩阵.

**定理 21** 设 $V$ 是复内积空间，$\sigma \in \mathcal{L}(V)$，则以下条件等价：
1. $\sigma$ 是酉变换;
2. $V$ 有一个由 $\sigma$ 的特征向量构成的标准正交基，且相应的特征值的绝对值均为 1.

#### 2.3.2 实正规算子

**定理 22** 设 $V$ 是二维的实内积空间，$\sigma \in \mathcal{L}(V)$，则以下条件等价：
1. $\sigma$ 是正规的但不是自伴的;
2. $\sigma$ 关于 $V$ 的每个标准正交基的矩阵都有
$$

\begin{pmatrix}
a & b \\
-b & a
\end{pmatrix}

$$
的形式，其中 $a, b \in \mathbb{R}$ 且 $b \neq 0$;
3. $\sigma$ 关于 $V$ 的某个标准正交基的矩阵有
$$

\begin{pmatrix}
a & b \\
-b & a
\end{pmatrix}

$$
的形式，其中 $a, b \in \mathbb{R}$ 且 $b > 0$.

**定理 23** 设 $\sigma \in \mathcal{L}(V)$ 是正规算子，$U$ 是 $\sigma$ 的不变子空间，则：
1. $U^\perp$ 在 $\sigma$ 下不变;
2. $U$ 在 $\sigma^*$ 下不变;
3. $(\sigma|_U)^* = \sigma^*|_U$;
4. $(\sigma|_U) \in \mathcal{L}(U)$ 和 $(\sigma|_{U^\perp}) \in \mathcal{L}(U^\perp)$ 都是正规算子.

**定理 24** 设 $V$ 是实内积空间，$\sigma \in \mathcal{L}(V)$，则以下条件等价：
1. $\sigma$ 是正规算子;
2. 存在 $V$ 的一组标准正交基使得 $\sigma$ 关于这组基具有分块对角矩阵，对角线上的每个块要么是 $1 \times 1$ 矩阵，要么是形如
$$

\begin{pmatrix}
a & b \\
-b & a
\end{pmatrix}

$$
的 $2 \times 2$ 矩阵，其中 $a, b \in \mathbb{R}$ 且 $b > 0$.

**定理 25** 设 $V$ 是实内积空间，$\sigma \in \mathcal{L}(V)$，则以下条件等价：
1. $\sigma$ 是正交变换;
2. 存在 $V$ 的一组标准正交基使得 $\sigma$ 关于这组基具有对角矩阵，对角线上的每个元素要么是 $1$ 或 $-1$ 构成的 $1 \times 1$ 矩阵，要么是形如
$$

\begin{pmatrix}
\cos \theta & \sin \theta \\
-\sin \theta & \cos \theta
\end{pmatrix}

$$
的 $2 \times 2$ 矩阵，其中 $\theta \in (0, \pi)$.

**例 3** 设 $S, T$ 是有限维内积空间上的等距变换，证明 $S$ 相似于 $T$ 当且仅当它们有相同的特征多项式.

### 2.4 正算子

**定义 10** $\sigma \in \mathcal{L}(V)$ 满足 $\sigma^* = \sigma$ 且 $\forall v \in V$，$\langle \sigma v, v \rangle_V \geq 0$，则称 $\sigma$ 为正算子.

**定义 11** 设 $\sigma, \tau \in \mathcal{L}(V)$，如果 $\tau^2 = \sigma$，则称 $\tau$ 是 $\sigma$ 的平方根.

**定理 26** 设 $\sigma \in \mathcal{L}(V)$，则以下条件等价：
1. $\sigma$ 是正算子;
2. $\sigma$ 是自伴算子且 $\sigma$ 的特征值都是非负实数;
3. $\sigma$ 有正的平方根;
4. $\sigma$ 有自伴的平方根;
5. 存在 $\tau \in \mathcal{L}(V)$，使得 $\tau^* \tau = \sigma$.

### 2.5 奇异值分解

**引理 27** 设 $\sigma \in \mathcal{L}(V)$，则
1. $\sigma^* \sigma$ 是正算子;
2. $\ker \sigma^* \sigma = \ker \sigma$;
3. $\operatorname{im} \sigma^* \sigma = \operatorname{im} \sigma^*$;
4. $\dim \operatorname{im} \sigma = \dim \operatorname{im} \sigma^* = \dim \operatorname{im} \sigma^* \sigma$.

**定义 12** 设 $\sigma \in \mathcal{L}(V, W)$，则 $\sigma^* \sigma$ 的特征值的算术平方根 $\sqrt{\lambda}$ 称为 $\sigma$ 的奇异值，并且重复 $\dim E(\lambda, \sigma^* \sigma)$ 次.

**定理 28** （奇异值分解）设 $\sigma \in \mathcal{L}(V, W)$ 有正奇异值 $s_1, s_2, \ldots, s_m$，则存在 $V$ 的一组标准正交组 $(e_1, e_2, \ldots, e_m)$ 和 $W$ 的一组标准正交组 $(f_1, f_2, \ldots, f_m)$ 使得 $\forall v \in V$，
$$
\sigma v = s_1 \langle v, e_1 \rangle f_1 + s_2 \langle v, e_2 \rangle f_2 + \cdots + s_m \langle v, e_m \rangle f_m.
$$

**定理 29** （极分解定理）设 $\sigma \in \mathcal{L}(V)$，则存在保积自同构 $\tau \in \mathcal{L}(V)$ 使得 $\sigma = \tau \sqrt{\sigma^* \sigma}$.

**例 4** $T \in \mathcal{L}(V)$ 有极分解 $T = S \sqrt{G}$，其中 $S$ 是等距同构，$G = T^* T$，证明以下条件等价：
1. $T$ 是正算子;
2. $G S = S G$;
3. $G$ 的所有特征空间 $E(\lambda, G)$ 都是 $S$-不变的.