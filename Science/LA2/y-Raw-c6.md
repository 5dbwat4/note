## 6.1 定义：点积（dot product）
对 $\mathbf{u}, \mathbf{v} \in \mathbb{R}^n$，$\mathbf{u}$ 和 $\mathbf{v}$ 的点积记作 $\mathbf{u} \cdot \mathbf{v}$，由下式定义：

$$
 \mathbf{u} \cdot \mathbf{v} = u_1v_1 + \cdots + u_nv_n, 
 $$

其中 $\mathbf{u} = (u_1, \ldots, u_n)$，$\mathbf{v} = (v_1, \ldots, v_n)$。

## 6.2 定义：内积（inner product）
$V$ 上的内积是一个函数，它将由 $V$ 中元素构成的每个有序对 $(\mathbf{u}, \mathbf{v})$ 对应至一个数 $\langle \mathbf{u}, \mathbf{v} \rangle \in F$，并满足如下性质：
- 正性（positivity）：对于所有 $\mathbf{u} \in V$，均有 $\langle \mathbf{u}, \mathbf{u} \rangle \geq 0$。
- 定性（definiteness）：$\langle \mathbf{u}, \mathbf{u} \rangle = 0$ 当且仅当 $\mathbf{u} = 0$。
- 第一个位置上的可加性（additivity in first slot）：对于所有 $\mathbf{u}, \mathbf{v}, \mathbf{w} \in V$，均有 $\langle \mathbf{u} + \mathbf{v}, \mathbf{w} \rangle = \langle \mathbf{u}, \mathbf{w} \rangle + \langle \mathbf{v}, \mathbf{w} \rangle$。
- 第一个位置上的齐次性（homogeneity in first slot）：对于所有 $\lambda \in F$ 和所有 $\mathbf{u}, \mathbf{v} \in V$，均有 $\langle \lambda \mathbf{u}, \mathbf{v} \rangle = \lambda \langle \mathbf{u}, \mathbf{v} \rangle$。
- 共轭对称性（conjugate symmetry）：对于所有 $\mathbf{u}, \mathbf{v} \in V$，均有 $\langle \mathbf{u}, \mathbf{v} \rangle = \overline{\langle \mathbf{v}, \mathbf{u} \rangle}$。

## 6.3 例：内积

(a) $F^n$ 上的欧几里得内积（Euclidean inner product）定义为：对所有 $(u_1, \ldots, u_n), (v_1, \ldots, v_n) \in F^n$，

$$
 \langle (u_1, \ldots, u_n), (v_1, \ldots, v_n) \rangle = u_1v_1 + \cdots + u_nv_n. 
 $$


(b) 若 $a_1, \ldots, a_n$ 是正数，那么可在 $F^n$ 上定义内积如下：对所有 $(u_1, \ldots, u_n), (v_1, \ldots, v_n) \in F^n$，

$$
 \langle (u_1, \ldots, u_n), (v_1, \ldots, v_n) \rangle = a_1u_1v_1 + \cdots + a_nu_nv_n. 
 $$


(c) 在由定义在区间 \([−1, 1]\) 上的全体连续实值函数构成的向量空间上，可定义内积如下：对所有定义在区间 \([−1, 1]\) 上的连续实值函数 $f, g$，

$$
 \langle f, g \rangle = \int_{-1}^{1} f(x)g(x) \, dx. 
 $$


(d) 在 $P(\mathbb{R})$ 上，可定义内积如下：对所有 $p, q \in P(\mathbb{R})$，

$$
 \langle p, q \rangle = p(0)q(0) + \int_{-1}^{1} p'(x)q'(x) \, dx. 
 $$


(e) 在 $P(\mathbb{R})$ 上，还可定义内积如下：对所有 $p, q \in P(\mathbb{R})$，

$$
 \langle p, q \rangle = \int_{0}^{\infty} p(x)q(x)e^{-x^2} \, dx. 
 $$


## 6.4 定义：内积空间（inner product space）
一个内积空间是带有内积的向量空间 $V$。

## 6.5 记号：$V$、$W$
在本章的剩余部分和下章中，$V$ 和 $W$ 都指代 $F$ 上的内积空间。

## 6.6 内积的基本性质

(a) 对每个固定的 $\mathbf{u} \in V$，将 $\mathbf{v} \in V$ 对应到 $\langle \mathbf{u}, \mathbf{v} \rangle$ 的函数都是 $V$ 到 $F$ 的线性映射。

(b) 对每个 $\mathbf{u} \in V$，均有 $\langle 0, \mathbf{u} \rangle = 0$。

(c) 对每个 $\mathbf{u} \in V$，均有 $\langle \mathbf{u}, 0 \rangle = 0$。

(d) 对所有 $\mathbf{u}, \mathbf{v}, \mathbf{w} \in V$，均有 $\langle \mathbf{u}, \mathbf{v} + \mathbf{w} \rangle = \langle \mathbf{u}, \mathbf{v} \rangle + \langle \mathbf{u}, \mathbf{w} \rangle$。

(e) 对所有 $\lambda \in F$ 和 $\mathbf{u}, \mathbf{v} \in V$，均有 $\langle \mathbf{u}, \lambda \mathbf{v} \rangle = \lambda \langle \mathbf{u}, \mathbf{v} \rangle$。

## 6.7 定义：范数（norm）、$\| \mathbf{u} \|$
对 $\mathbf{u} \in V$，$\mathbf{u}$ 的范数记作 $\| \mathbf{u} \|$，定义为

$$
 \| \mathbf{u} \| = \sqrt{\langle \mathbf{u}, \mathbf{u} \rangle}. 
 $$


## 6.8 例：范数
(a) 若 $(u_1, \ldots, u_n) \in F^n$（其上定义了欧几里得内积），那么

$$
 \| (u_1, \ldots, u_n) \| = \sqrt{|u_1|^2 + \cdots + |u_n|^2}. 
 $$

(b) 定义在区间 \([−1, 1]\) 上的连续实值函数所构成的向量空间【其上内积定义如 6.3 (c)】中的元素 $f$ 满足

$$
 \| f \| = \sqrt{\int_{-1}^{1} f(x)^2 \, dx}. 
 $$


## 6.9 范数的基本性质
设 $\mathbf{u} \in V$。

(a) $\| \mathbf{u} \| = 0$ 当且仅当 $\mathbf{u} = 0$。

(b) 对所有 $\lambda \in F$，均有 $\| \lambda \mathbf{u} \| = |\lambda| \| \mathbf{u} \|$。

## 6.10 定义：正交（orthogonal）
称两个向量 $\mathbf{u}, \mathbf{v} \in V$ 是正交的，若 $\langle \mathbf{u}, \mathbf{v} \rangle = 0$。

## 6.11 正交性和 0

(a) 0 与 $V$ 中每个向量都正交。

(b) 0 是 $V$ 中唯一与自身正交的向量。

## 6.12 毕达哥拉斯定理（Pythagorean theorem）
设 $\mathbf{u}, \mathbf{v} \in V$。若 $\mathbf{u}$ 和 $\mathbf{v}$ 是正交的，那么

$$
 \| \mathbf{u} + \mathbf{v} \|^2 = \| \mathbf{u} \|^2 + \| \mathbf{v} \|^2. 
 $$


## 6.13 一种正交分解
设 $\mathbf{u}, \mathbf{v} \in V$，且 $\mathbf{v} \neq 0$。取 $a = \frac{\langle \mathbf{u}, \mathbf{v} \rangle}{\| \mathbf{v} \|^2}$ 及 $\mathbf{w} = \mathbf{u} - a \mathbf{v}$。那么

$$
 \mathbf{u} = a \mathbf{v} + \mathbf{w} \quad \text{且} \quad \langle \mathbf{w}, \mathbf{v} \rangle = 0. 
 $$


## 6.14 柯西-施瓦兹不等式（Cauchy-Schwarz inequality）
设 $\mathbf{u}, \mathbf{v} \in V$。那么

$$
 | \langle \mathbf{u}, \mathbf{v} \rangle | \leq \| \mathbf{u} \| \| \mathbf{v} \|. 
 $$

当且仅当 $\mathbf{u}$ 和 $\mathbf{v}$ 成标量倍数关系时，上述不等式取得等号。

## 6.16 例：柯西-施瓦兹不等式
(a) 若 $u_1, \ldots, u_n, v_1, \ldots, v_n \in \mathbb{R}$，那么

$$
 (u_1v_1 + \cdots + u_nv_n)^2 \leq (u_1^2 + \cdots + u_n^2)(v_1^2 + \cdots + v_n^2), 
 $$

这就是将柯西-施瓦兹不等式应用于向量 $(u_1, \ldots, u_n), (v_1, \ldots, v_n) \in \mathbb{R}^n$ 的结果（所用内积是通常的欧几里得内积）。

(b) 若 $f, g$ 是定义在 \([−1, 1]\) 上的连续实值函数，那么

$$
 \left| \int_{-1}^{1} f(x)g(x) \, dx \right|^2 \leq \left( \int_{-1}^{1} f(x)^2 \, dx \right) \left( \int_{-1}^{1} g(x)^2 \, dx \right), 
 $$

这就是将柯西-施瓦兹不等式应用于例 6.3 (c) 的结果。

## 6.17 三角不等式（triangle inequality）
设 $\mathbf{u}, \mathbf{v} \in V$。那么

$$
 \| \mathbf{u} + \mathbf{v} \| \leq \| \mathbf{u} \| + \| \mathbf{v} \|. 
 $$

该不等式取得等号，当且仅当 $\mathbf{u}$ 和 $\mathbf{v}$ 中任意一者是另一者的非负实数倍。

## 6.21 平行四边形等式（parallelogram equality）
设 $\mathbf{u}, \mathbf{v} \in V$。那么

$$
 \| \mathbf{u} + \mathbf{v} \|^2 + \| \mathbf{u} - \mathbf{v} \|^2 = 2(\| \mathbf{u} \|^2 + \| \mathbf{v} \|^2). 
 $$


## 6.22 定义：规范正交（orthonormal）
如果一个向量组中所有向量的范数都是 1，且每个向量与其他向量都正交，则称该向量组是规范正交的。
换言之，$V$ 中向量组 $\mathbf{e}_1, \ldots, \mathbf{e}_m$ 是规范正交的，若对所有 $i, j \in \{1, \ldots, m\}$，

$$

\langle \mathbf{e}_i, \mathbf{e}_j \rangle = 
\begin{cases}
1, & \text{若 } i = j, \\
0, & \text{若 } i \neq j.
\end{cases} 

$$


## 6.24 规范正交组线性组合的范数
设 $\mathbf{e}_1, \ldots, \mathbf{e}_m$ 是 $V$ 中的规范正交向量组。那么对所有 $a_1, \ldots, a_m \in F$，有

$$
 \| a_1 \mathbf{e}_1 + \cdots + a_m \mathbf{e}_m \|^2 = |a_1|^2 + \cdots + |a_m|^2. 
 $$


## 6.25 规范正交组是线性无关的
每个规范正交向量组都是线性无关的。

## 6.26 贝塞尔不等式（Bessel’s inequality）
设 $\mathbf{e}_1, \ldots, \mathbf{e}_m$ 是 $V$ 中的规范正交向量组。若 $\mathbf{u} \in V$，那么

$$
 | \langle \mathbf{u}, \mathbf{e}_1 \rangle |^2 + \cdots + | \langle \mathbf{u}, \mathbf{e}_m \rangle |^2 \leq \| \mathbf{u} \|^2. 
 $$


## 6.27 定义：规范正交基（orthonormal basis）
$V$ 的一个规范正交基，就是 $V$ 中既是规范正交组又是基的向量组。

## 6.28 长度恰好的规范正交组是规范正交基
设 $V$ 是有限维的。那么 $V$ 中每个长度为 $\dim V$ 的规范正交向量组都是 $V$ 的规范正交基。

## 6.30 将向量写成规范正交基的线性组合
设 $\mathbf{e}_1, \ldots, \mathbf{e}_n$ 是 $V$ 的规范正交基且 $\mathbf{u}, \mathbf{v} \in V$。那么

(a) $\mathbf{u} = \langle \mathbf{u}, \mathbf{e}_1 \rangle \mathbf{e}_1 + \cdots + \langle \mathbf{u}, \mathbf{e}_n \rangle \mathbf{e}_n$，

(b) $\| \mathbf{u} \|^2 = | \langle \mathbf{u}, \mathbf{e}_1 \rangle |^2 + \cdots + | \langle \mathbf{u}, \mathbf{e}_n \rangle |^2$，

(c) $\langle \mathbf{u}, \mathbf{v} \rangle = \langle \mathbf{u}, \mathbf{e}_1 \rangle \langle \mathbf{v}, \mathbf{e}_1 \rangle + \cdots + \langle \mathbf{u}, \mathbf{e}_n \rangle \langle \mathbf{v}, \mathbf{e}_n \rangle$。

## 6.32 格拉姆-施密特过程（Gram-Schmidt procedure）
设 $\mathbf{u}_1, \ldots, \mathbf{u}_m$ 是 $V$ 中的线性无关向量组。令 $\mathbf{e}_1 = \mathbf{u}_1$。对 $i = 2, \ldots, m$，依次定义 $\mathbf{e}_i$ 为

$$
 \mathbf{e}_i = \mathbf{u}_i - \frac{\langle \mathbf{u}_i, \mathbf{e}_1 \rangle}{\| \mathbf{e}_1 \|^2} \mathbf{e}_1 - \cdots - \frac{\langle \mathbf{u}_i, \mathbf{e}_{i-1} \rangle}{\| \mathbf{e}_{i-1} \|^2} \mathbf{e}_{i-1}. 
 $$

对每个 $i = 1, \ldots, m$，令 $\mathbf{e}_i' = \frac{\mathbf{e}_i}{\| \mathbf{e}_i \|}$。那么 $\mathbf{e}_1', \ldots, \mathbf{e}_m'$ 是 $V$ 中的规范正交向量组，且对每个 $i = 1, \ldots, m$ 满足

$$
 \text{span}(\mathbf{u}_1, \ldots, \mathbf{u}_i) = \text{span}(\mathbf{e}_1', \ldots, \mathbf{e}_i'). 
 $$


## 6.35 规范正交基的存在性
每个有限维内积空间都有规范正交基。

## 6.36 每个规范正交组都可被扩充为规范正交基
设 $V$ 是有限维的。那么 $V$ 中每个规范正交向量组都能被扩充为 $V$ 的一个规范正交基。

## 6.37 关于某个规范正交基有上三角矩阵
设 $V$ 是有限维的，$T \in L(V)$。那么 $T$ 关于 $V$ 的某个规范正交基有上三角矩阵，当且仅当 $T$ 的最小多项式等于 $(T - \lambda_1) \cdots (T - \lambda_m)$，其中 $\lambda_1, \ldots, \lambda_m \in F$。

## 6.38 舒尔定理（Schur’s theorem）
有限维复内积空间上的每个算子都关于某个规范正交基有上三角矩阵。

## 6.39 定义：线性泛函（linear functional），对偶空间（dual space）、$V'$
$V$ 上的一个线性泛函是一个从 $V$ 到 $F$ 的线性映射。
$V$ 的对偶空间记作 $V'$，是 $V$ 上全体线性泛函所构成的向量空间。换言之，$V' = L(V, F)$。

## 6.42 里斯表示定理（Riesz representation theorem）
设 $V$ 是有限维的，$\varphi$ 是 $V$ 上的线性泛函。那么存在唯一的向量 $\mathbf{u} \in V$，使得对每个 $\mathbf{v} \in V$ 都有

$$
 \varphi(\mathbf{v}) = \langle \mathbf{v}, \mathbf{u} \rangle. 
 $$


## 6.46 定义：正交补（orthogonal complement）、$U^\perp$
若 $U$ 是 $V$ 的子集，那么 $U$ 的正交补，记作 $U^\perp$，是与 $U$ 中的每个向量都正交的所有 $V$ 中向量所构成的集合：

$$
 U^\perp = \{ \mathbf{v} \in V : \text{对于每个 } \mathbf{u} \in U, \langle \mathbf{v}, \mathbf{u} \rangle = 0 \}. 
 $$


## 6.48 正交补的性质

(a) 若 $U$ 是 $V$ 的子集，那么 $U^\perp$ 是 $V$ 的子空间。

(b) $\{0\}^\perp = V$。

(c) $V^\perp = \{0\}$。

(d) 若 $U$ 是 $V$ 的子集，那么 $U \cap U^\perp \subseteq \{0\}$。

(e) 若 $A$ 和 $B$ 是 $V$ 的子集且 $A \subseteq B$，那么 $B^\perp \subseteq A^\perp$。

## 6.49 子空间及其正交补的直和
设 $U$ 是 $V$ 的有限维子空间。那么

$$
 V = U \oplus U^\perp. 
 $$


## 6.51 正交补的维数
设 $V$ 是有限维的，$U$ 是 $V$ 的子空间。那么

$$
 \dim U^\perp = \dim V - \dim U. 
 $$


## 6.52 正交补的正交补
设 $U$ 是 $V$ 的一个有限维子空间。那么

$$
 U = (U^\perp)^\perp. 
 $$


## 6.54 对 $V$ 的有限维子空间 $U$，有 $U^\perp = \{0\} \Leftrightarrow U = V$
设 $U$ 是 $V$ 的有限维子空间。那么

$$
 U^\perp = \{0\} \Leftrightarrow U = V. 
 $$


## 6.55 定义：正交投影（orthogonal projection）、$P_U$
设 $U$ 是 $V$ 的一个有限维子空间。将 $V$ 映成 $U$ 的正交投影是定义如下的算子 $P_U \in L(V)$：
对每个 $\mathbf{v} \in V$，将其写成 $\mathbf{v} = \mathbf{u} + \mathbf{w}$，其中 $\mathbf{u} \in U$ 且 $\mathbf{w} \in U^\perp$，然后令 $P_U \mathbf{v} = \mathbf{u}$。

## 6.57 正交投影 $P_U$ 的性质
设 $U$ 是 $V$ 的有限维子空间。那么

(a) $P_U \in L(V)$；

(b) 对每个 $\mathbf{u} \in U$，都有 $P_U \mathbf{u} = \mathbf{u}$；

(c) 对每个 $\mathbf{w} \in U^\perp$，都有 $P_U \mathbf{w} = 0$；

(d) $\text{range } P_U = U$；

(e) $\text{null } P_U = U^\perp$；

(f) 对每个 $\mathbf{v} \in V$，都有 $\mathbf{v} - P_U \mathbf{v} \in U^\perp$；

(g) $P_U^2 = P_U$；

(h) 对每个 $\mathbf{v} \in V$，都有 $\| P_U \mathbf{v} \| \leq \| \mathbf{v} \|$；

(i) 若 $\mathbf{e}_1, \ldots, \mathbf{e}_m$ 是 $U$ 的一个规范正交基且 $\mathbf{v} \in V$，那么

$$
 P_U \mathbf{v} = \langle \mathbf{v}, \mathbf{e}_1 \rangle \mathbf{e}_1 + \cdots + \langle \mathbf{v}, \mathbf{e}_m \rangle \mathbf{e}_m. 
 $$


## 6.61 到子空间的最短距离
设 $U$ 是 $V$ 的有限维子空间，$\mathbf{v} \in V$ 且 $\mathbf{u} \in U$。那么

$$
 \| \mathbf{v} - P_U \mathbf{v} \| \leq \| \mathbf{v} - \mathbf{u} \|. 
 $$

此外，上述不等式取得等号当且仅当 $\mathbf{u} = P_U \mathbf{v}$。

## 6.67 限制线性映射以获得既单又满的映射
设 $V$ 是有限维的，且 $T \in L(V, W)$。那么 $T|_{(\text{null } T)^\perp}$ 是将 $(\text{null } T)^\perp$ 映成 $\text{range } T$ 的单射。

## 6.68 定义：伪逆（pseudoinverse）、$T^\dagger$
设 $V$ 是有限维的，$T \in L(V, W)$。$T$ 的伪逆 $T^\dagger \in L(W, V)$ 是定义如下的从 $W$ 到 $V$ 的线性映射：对每个 $\mathbf{w} \in W$，

$$
 T^\dagger \mathbf{w} = (T|_{(\text{null } T)^\perp})^{-1} P_{\text{range } T} \mathbf{w}. 
 $$


## 6.69 伪逆的代数性质
设 $V$ 是有限维的且 $T \in L(V, W)$。

(a) 若 $T$ 可逆，则 $T^\dagger = T^{-1}$。

(b) $T T^\dagger = P_{\text{range } T} =$ 将 $W$ 映成 $\text{range } T$ 的正交投影。

(c) $T^\dagger T = P_{(\text{null } T)^\perp} =$ 将 $V$ 映成 $(\text{null } T)^\perp$ 的正交投影。

## 6.70 伪逆可给出最佳近似解或最优解
设 $V$ 是有限维的，$T \in L(V, W)$，$\mathbf{w} \in W$。
(a) 若 $\mathbf{w} \in W$，则

$$
 \| T(T^\dagger \mathbf{w}) - \mathbf{w} \| \leq \| T \mathbf{v} - \mathbf{w} \|, 
 $$

当且仅当 $\mathbf{v} \in T^\dagger \mathbf{w} + \text{null } T$ 时，上式取得等号。
(b) 若 $\mathbf{v} \in T^\dagger \mathbf{w} + \text{null } T$，则

$$
 \| T^\dagger \mathbf{w} \| \leq \| \mathbf{v} \|, 
 $$

当且仅当 $\mathbf{v} = T^\dagger \mathbf{w}$ 时，上式取得等号。