
## 7.1 定义：伴随（adjoint）、$T^*$
设 $T \in L(V, W)$.$T$ 的伴随是使得对任一 $v \in V$ 和任一 $w \in W$ 都有
$$
\langle Tv, w \rangle = \langle v, T^*w \rangle
$$
的函数 $T^* : W \to V$。

## 7.4 线性映射的伴随是线性映射
如果 $T \in L(V, W)$，那么 $T^* \in L(W, V)$。

## 7.5 伴随的性质
设 $T \in L(V, W)$，那么有：
- (a) $(S + T)^* = S^* + T^*$ 对所有 $S \in L(V, W)$ 成立；
- (b) $(\lambda T)^* = \overline{\lambda} T^*$ 对所有 $\lambda \in \mathbb{F}$ 成立；
- (c) $(T^*)^* = T$；
- (d) $(ST)^* = T^* S^*$ 对所有 $S \in L(W, U)$ 成立（这里 $U$ 是 $\mathbb{F}$ 上的有限维内积空间）；
- (e) $I_V^* = I_V$，其中 $I_V$ 是 $V$ 上的恒等算子；
- (f) 如果 $T$ 可逆，那么 $T^*$ 可逆且 $(T^*)^{-1} = (T^{-1})^*$。

## 7.6 $T^*$ 的零空间和值域
设 $T \in L(V, W)$，那么有：
-   (a) $\text{null } T^* = (\text{range } T)^\perp$；
-   (b) $\text{range } T^* = (\text{null } T)^\perp$；
-   (c) $\text{null } T = (\text{range } T^*)^\perp$；
-   (d) $\text{range } T = (\text{null } T^*)^\perp$。

## 7.7 定义：共轭转置（conjugate transpose）、$A^*$
$m \times n$ 矩阵 $A$ 的共轭转置是将其行列互换再对每个元素取复共轭得到的 $n \times m$ 矩阵 $A^*$.

## 7.9 $T^*$ 的矩阵等于 $T$ 的矩阵的共轭转置
令 $T \in L(V, W)$.设 $e_1, \dots, e_n$ 是 $V$ 的规范正交基，$f_1, \dots, f_m$ 是 $W$ 的规范正交基.那么
$$
M(T^*, (f_1, \dots, f_m), (e_1, \dots, e_n)) = M(T, (e_1, \dots, e_n), (f_1, \dots, f_m))^*.
$$

## 7.10 定义：自伴（self-adjoint）
算子 $T \in L(V)$ 称为自伴的，如果 $T = T^*$.

## 7.12 自伴算子的特征值
自伴算子的每个特征值都是实的。

## 7.13 对所有 $v$ 都有 $Tv$ 正交于 $v$ ⇐⇒ $T = 0$（假设 $\mathbb{F} = \mathbb{C}$）
设 $T$ 是复内积空间以及 $T \in L(V)$，那么
$$
\langle Tv, v \rangle = 0 \text{ 对任一 } v \in V \text{ 成立} \Leftrightarrow T = 0.
$$

## 7.14 $\langle Tv, v \rangle$ 对所有 $v$ 都是实的 ⇐⇒ $T$ 是自伴的（假设 $\mathbb{F} = \mathbb{C}$）
设 $T$ 是复内积空间以及 $T \in L(V)$，那么
$$
T \text{ 是自伴的} \Leftrightarrow \langle Tv, v \rangle \in \mathbb{R} \text{ 对任一 } v \in V \text{ 成立}.
$$

## 7.16 $T$ 自伴且 $\langle Tv, v \rangle = 0$ 对所有 $v$ 成立 ⇐⇒ $T = 0$
设 $T$ 是 $V$ 上的自伴算子，那么
$$
\langle Tv, v \rangle = 0 \text{ 对任一 } v \in V \text{ 成立} \Leftrightarrow T = 0.
$$

## 7.18 定义：正规（normal）
内积空间上的算子被称为正规的，如果它与它的伴随可交换.换句话说，$T \in L(V)$ 是正规的，如果 $TT^* = T^*T$.

## 7.20 $T$ 是正规的当且仅当 $Tv$ 和 $T^*v$ 的范数相同
设 $T \in L(V)$，那么有
$$
T \text{ 是正规的} \Leftrightarrow \|Tv\| = \|T^*v\| \text{ 对任一 } v \in V \text{ 成立}.
$$

## 7.21 正规算子的值域、零空间和特征向量
设 $T \in L(V)$ 是正规的，那么有：
(a) $\text{null } T = \text{null } T^*$；
(b) $\text{range } T = \text{range } T^*$；
(c) $V = \text{null } T \oplus \text{range } T$；
(d) 对任一 $\lambda \in \mathbb{F}$，$T - \lambda I$ 都是正规的；
(e) 如果 $v \in V$ 且 $\lambda \in \mathbb{F}$，那么 $Tv = \lambda v$ 当且仅当 $T^*v = \lambda v$.

## 7.22 正规算子的正交特征向量
设 $T \in L(V)$ 是正规的.那么 $T$ 的对应于不同特征值的特征向量正交。

## 7.23 $T$ 是正规的 ⇐⇒ $T$ 的实部和虚部可交换
设 $\mathbb{F} = \mathbb{C}$ 且 $T \in L(V)$.那么，$T$ 是正规的当且仅当存在可交换的自伴算子 $A$ 和 $B$ 使得
$$
T = A + iB.
$$

## 7.26 可逆二次表达式
设 $T \in L(V)$ 是自伴的，且 $a, b \in \mathbb{R}$ 使得 $a^2 < 4b$.那么
$$
T^2 + aT + bI
$$
是可逆算子。

## 7.27 自伴算子的最小多项式
设 $T \in L(V)$ 是自伴的.那么 $T$ 的最小多项式等于 $(x - \lambda_1) \cdots (x - \lambda_m)$，其中 $\lambda_1, \dots, \lambda_m \in \mathbb{R}$.

## 7.29 实谱定理（real spectral theorem）
设 $\mathbb{F} = \mathbb{R}$ 且 $T \in L(V)$．那么下列等价：
(a) $T$ 是自伴的.
(b) $T$ 关于 $V$ 的某个规范正交基有对角矩阵.
(c) $T$ 有由 $V$ 的特征向量构成的规范正交基.

## 7.31 复谱定理（complex spectral theorem）
设 $\mathbb{F} = \mathbb{C}$ 且 $T \in L(V)$．那么下列等价：
(a) $T$ 是正规的.
(b) $T$ 关于 $V$ 的某个规范正交基有对角矩阵.
(c) $T$ 有由 $V$ 的特征向量构成的规范正交基.

## 7.34 定义：正算子（positive operator）
设 $P \in L(V)$，称 $P$ 为正的，如果 $P$ 是自伴的且对所有 $v \in V$ 有
$$
\langle Pv, v \rangle \geq 0.
$$
如果 $V$ 是复向量空间，那么“$P$ 是自伴的”这一条件可以去掉。

## 7.35 例：正算子
- (a) 令算子 $P \in L(F^2)$ 的矩阵（关于标准基）是
$$
\begin{bmatrix}
2 & -1 \\
-1 & 1
\end{bmatrix}.
$$
那么 $P$ 是自伴的，且
$$
\langle P(v_1, v_2), (v_1, v_2) \rangle = 2|v_1|^2 - 2\text{Re}(v_1v_2) + |v_2|^2 = |v_1 - v_2|^2 + |v_2|^2 \geq 0
$$
对所有 $(v_1, v_2) \in F^2$ 成立，因此 $P$ 是正算子。
- (b) 如果 $S$ 是 $V$ 的子空间，那么正交投影 $P_S$ 是正算子。
- (c) 如果 $P \in L(V)$ 是自伴的，且 $a, b \in \mathbb{R}$ 使得 $a^2 < 4b$，那么 $P^2 + aP + bI$ 是正算子。

## 7.36 定义：平方根（square root）
称算子 $Q$ 为算子 $P$ 的平方根，如果 $Q^2 = P$。

## 7.37 例：算子的平方根
如果 $P \in L(F^3)$ 定义为 $P(v_1, v_2, v_3) = (v_3, 0, 0)$，那么定义为 $Q(v_1, v_2, v_3) = (v_2, v_3, 0)$ 的算子 $Q \in L(F^3)$ 是 $P$ 的一个平方根，因为 $Q^2 = P$。

## 7.38 正算子的特性
设 $P \in L(V)$，那么下列等价：
- (a) $P$ 是正算子。
- (b) $P$ 自伴且所有特征值非负。
- (c) 关于 $P$ 的某个规范正交基，$P$ 的矩阵是对角矩阵且对角线上仅有非负数。
- (d) $P$ 有正平方根。
- (e) $P$ 有自伴平方根。
- (f) 存在某个 $Q \in L(V)$ 使得 $P = Q^*Q$。

## 7.39 每个正算子都只有一个正平方根
每个正算子都有唯一正平方根。

## 7.40 记号：$\sqrt{P}$
对于正算子 $P$，$\sqrt{P}$ 表示 $P$ 的唯一正平方根。

## 7.41 例：正算子的平方根
在 $\mathbb{R}^2$ 上定义算子 $P_1, P_2$ 为
$$
P_1(v_1, v_2) = (v_1, 2v_2) \quad \text{和} \quad P_2(v_1, v_2) = (v_1 + v_2, v_1 + v_2).
$$
那么，关于 $\mathbb{R}^2$ 的标准基，我们有
$$
M(P_1) =
\begin{bmatrix}
1 & 0 \\
0 & 2
\end{bmatrix}
\quad \text{和} \quad
M(P_2) =
\begin{bmatrix}
1 & 1 \\
1 & 1
\end{bmatrix}.
$$
这两个矩阵都等于自身的转置，因此 $P_1$ 和 $P_2$ 都是自伴的。如果 $(v_1, v_2) \in \mathbb{R}^2$，那么
$$
\langle P_1(v_1, v_2), (v_1, v_2) \rangle = v_1^2 + 2v_2^2 \geq 0
$$
且
$$
\langle P_2(v_1, v_2), (v_1, v_2) \rangle = v_1^2 + 2v_1v_2 + v_2^2 = (v_1 + v_2)^2 \geq 0.
$$
因此，$P_1$ 和 $P_2$ 都是正算子。

## 7.43 $P$ 是正的且 $\langle Pv, v \rangle = 0 \Rightarrow Pv = 0$
设 $P$ 是 $V$ 上的正算子且 $v \in V$ 使得 $\langle Pv, v \rangle = 0$，那么 $Pv = 0$。

## 7.44 定义：等距映射（isometry）
线性映射 $T \in L(V, W)$ 被称为等距映射，如果
$$
\|Tv\| = \|v\|
$$
对任一 $v \in V$ 都成立。

## 7.45 例：将规范正交基映射到规范正交组 $\Rightarrow$ 等距映射
设 $e_1, \dots, e_n$ 是 $V$ 的规范正交基，$f_1, \dots, f_n$ 是 $W$ 中的规范正交组。令 $T \in L(V, W)$ 是使得对任一 $i = 1, \dots, n$ 都有 $Te_i = f_i$ 的线性映射。那么 $T$ 是等距映射。

## 7.49 等距映射的特性
设 $T \in L(V, W)$。设 $e_1, \dots, e_n$ 是 $V$ 的规范正交基，$f_1, \dots, f_m$ 是 $W$ 的规范正交基。那么下列等价：
- (a) $T$ 是等距映射。
- (b) $T^*T = I$。
- (c) $\langle Tv, Tw \rangle = \langle v, w \rangle$ 对所有 $v, w \in V$ 成立。
- (d) $Te_1, \dots, Te_n$ 是 $W$ 中的规范正交组。
- (e) $M(T, (e_1, \dots, e_n), (f_1, \dots, f_m))$ 的列形成 $F^m$ 中关于欧几里得内积的规范正交组。

## 7.51 定义：幺正算子（unitary operator）
算子 $U \in L(V)$ 被称为幺正的，如果 $U$ 是可逆等距映射。

## 7.52 例：$\mathbb{R}^2$ 的旋转
设 $\theta \in \mathbb{R}$ 且 $U$ 是 $F^2$ 上的算子，其关于 $F^2$ 的标准基的矩阵是
$$
\begin{bmatrix}
\cos \theta & -\sin \theta \\
\sin \theta & \cos \theta
\end{bmatrix}.
$$
该矩阵的这两列形成了 $F^2$ 中的规范正交组，于是 $U$ 是等距映射。因此，$U$ 是幺正算子。

## 7.53 幺正算子的特性
设 $U \in L(V)$。设 $e_1, \dots, e_n$ 是 $V$ 的规范正交基。那么下列等价：
- (a) $U$ 是幺正算子。
- (b) $U^*U = UU^* = I$。
- (c) $U$ 可逆且 $U^{-1} = U^*$。
- (d) $Ue_1, \dots, Ue_n$ 是 $V$ 的规范正交基。
- (e) $M(U, (e_1, \dots, e_n))$ 的行形成 $F^n$ 中关于欧几里得内积的规范正交基。
- (f) $U^*$ 是幺正算子。

## 7.54 幺正算子的特征值绝对值是 1
设 $\lambda$ 是幺正算子的特征值，那么 $|\lambda| = 1$。

## 7.55 对复内积空间上的幺正算子的描述
设 $F = \mathbb{C}$ 且 $U \in L(V)$。那么下列等价：
- (a) $U$ 是幺正算子。
- (b) 存在 $V$ 的一规范正交基由 $U$ 的特征向量组成，其对应的特征值的绝对值都是 1。

## 7.56 定义：幺正矩阵（unitary matrix）
一 $n \times n$ 矩阵被称为幺正的，如果它的列形成 $F^n$ 中的规范正交组。

## 7.57 幺正矩阵的特性
设 $U$ 是 $n \times n$ 矩阵。那么下列等价：
- (a) $U$ 是幺正矩阵。
- (b) $U$ 的行形成 $F^n$ 中的规范正交组。
- (c) $\|Up\| = \|p\|$ 对任一 $p \in F^n$ 都成立。
- (d) $U^*U = UU^* = I$，$I$ 是对角线上为 1、其余处处为 0 的 $n \times n$ 矩阵。

## 7.58 QR 分解（QR factorization）
设 $A$ 是各列线性无关的方阵。那么存在唯一一对矩阵 $Q$ 和 $R$，其中 $Q$ 是幺正的，而 $R$ 是上三角的且对角线上仅有正数，使得
$$
A = QR.
$$

## 7.60 例：3 × 3 矩阵的 QR 分解
求矩阵
$$
A =
\begin{bmatrix}
1 & 2 & 1 \\
0 & 1 & -4 \\
0 & 3 & 2
\end{bmatrix}
$$
的 QR 分解。我们按照 7.58 的证明，令 $p_1, p_2, p_3$ 等于 $A$ 的列：
$$
p_1 = (1, 0, 0), \quad p_2 = (2, 1, 3), \quad p_3 = (1, -4, 2).
$$
对 $p_1, p_2, p_3$ 应用格拉姆-施密特过程，得到规范正交组
$$
a_1 = (1, 0, 0), \quad a_2 = \left(0, \frac{1}{\sqrt{10}}, \frac{3}{\sqrt{10}}\right), \quad a_3 = \left(0, -\frac{3}{\sqrt{10}}, \frac{1}{\sqrt{10}}\right).
$$
顺着 7.58 的证明，令 $Q$ 是以 $a_1, a_2, a_3$ 为列的幺正矩阵：
$$
Q =
\begin{bmatrix}
1 & 0 & 0 \\
0 & \frac{1}{\sqrt{10}} & -\frac{3}{\sqrt{10}} \\
0 & \frac{3}{\sqrt{10}} & \frac{1}{\sqrt{10}}
\end{bmatrix}.
$$
再按 7.58 的证明，令 $R$ 是 3 × 3 矩阵，第 $i$ 行第 $j$ 列的元素为 $\langle p_i, a_j \rangle$，得到
$$
R =
\begin{bmatrix}
1 & 2 & 1 \\
0 & \sqrt{10} & \frac{5}{\sqrt{10}} \\
0 & 0 & \frac{7}{\sqrt{10}}
\end{bmatrix}.
$$
注意到 $R$ 确实是对角线上仅有正数的上三角矩阵，这正是 QR 分解所保证的。现在，做矩阵乘法即可验证 $A = QR$ 就是待求的分解：
$$
QR =
\begin{bmatrix}
1 & 0 & 0 \\
0 & \frac{1}{\sqrt{10}} & -\frac{3}{\sqrt{10}} \\
0 & \frac{3}{\sqrt{10}} & \frac{1}{\sqrt{10}}
\end{bmatrix}
\begin{bmatrix}
1 & 2 & 1 \\
0 & \sqrt{10} & \frac{5}{\sqrt{10}} \\
0 & 0 & \frac{7}{\sqrt{10}}
\end{bmatrix}
=
\begin{bmatrix}
1 & 2 & 1 \\
0 & 1 & -4 \\
0 & 3 & 2
\end{bmatrix}
= A.
$$
因此，$A = QR$，正如我们预期的那般。

## 7.61 可逆正算子
自伴算子 $P \in L(V)$ 是可逆正算子，当且仅当 $\langle Pv, v \rangle > 0$ 对任意非零 $v \in V$ 都成立。

## 7.62 定义：正定（positive definite）
矩阵 $A \in F^{n,n}$ 称为正定的，如果 $A^* = A$ 且
$$
\langle Ap, p \rangle > 0
$$
对任意非零 $p \in F^n$ 都成立。

## 7.63 科列斯基分解（Cholesky factorization）
设 $A$ 是正定矩阵。那么存在唯一一个对角线上仅含正数的上三角矩阵 $R$ 使得
$$
A = R^*R.
$$

## 7.64 $T^*T$ 的性质
设 $T \in L(V, W)$，那么
- (a) $T^*T$ 是 $V$ 上的正算子；
- (b) $\text{null } T^*T = \text{null } T$；
- (c) $\text{range } T^*T = \text{range } T^*$；
- (d) $\dim \text{range } T = \dim \text{range } T^* = \dim \text{range } T^*T$。

## 7.65 定义：奇异值（singular values）
设 $T \in L(V, W)$。$T$ 的奇异值是 $T^*T$ 的特征值的非负平方根，按降序排列，而且每个奇异值的出现次数，等于 $T^*T$ 对应特征空间的维数。

## 7.66 例：$F^4$ 上一算子的奇异值
定义 $T \in L(F^4)$ 为 $T(v_1, v_2, v_3, v_4) = (0, 3v_1, 2v_2, -3v_4)$。计算可得
$$
T^*T(v_1, v_2, v_3, v_4) = (9v_1, 4v_2, 0, 9v_4),
$$
你应该自行验证这一点。那么，我们用 $F^4$ 的标准基对角化 $T^*T$，可得 $T^*T$ 的特征值是 9、4、0。以及，对应于这些特征值的特征空间维数是
$$
\dim A(9, T^*T) = 2, \quad \dim A(4, T^*T) = 1, \quad \dim A(0, T^*T) = 1.
$$
取 $T^*T$ 的这些特征值的非负平方根，并用到以上的维数信息，我们可以得出结论：$T$ 的奇异值是 3、3、2、0。

## 7.67 例：从 $F^4$ 到 $F^3$ 的一线性映射的奇异值
设 $T \in L(F^4, F^3)$ （关于标准基）的矩阵是
$$
\begin{bmatrix}
0 & 0 & 0 & -5 \\
0 & 0 & 0 & 0 \\
1 & 1 & 0 & 0
\end{bmatrix}.
$$
你可以验证，$T^*T$ 的矩阵是
$$
\begin{bmatrix}
1 & 1 & 0 & 0 \\
1 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 25
\end{bmatrix},
$$
特征值是 25、2、0；而 $\dim A(25, T^*T) = 1$，$\dim A(2, T^*T) = 1$，$\dim A(0, T^*T) = 2$。所以，$T$ 的奇异值是 5、$\sqrt{2}$、0、0。

## 7.68 正奇异值的作用
设 $T \in L(V, W)$，那么
- (a) $T$ 是单射 $\Leftrightarrow$ 0 不是 $T$ 的奇异值；
- (b) $T$ 的正奇异值个数等于 $\dim \text{range } T$；
- (c) $T$ 是满射 $\Leftrightarrow$ $T$ 的正奇异值个数等于 $\dim W$。

## 7.69 所有奇异值都等于 1 是等距映射的特征
设 $T \in L(V, W)$，那么
$$
T \text{ 是等距映射} \Leftrightarrow T \text{ 的所有奇异值都等于 1}.
$$

## 7.70 奇异值分解（singular value decomposition）
设 $T \in L(V, W)$ 且 $T$ 的正奇异值是 $\sigma_1, \dots, \sigma_m$。那么存在 $V$ 中的规范正交组 $e_1, \dots, e_m$ 和 $W$ 中的规范正交组 $f_1, \dots, f_m$ 使得
$$
Tv = \sigma_1 \langle v, e_1 \rangle f_1 + \dots + \sigma_m \langle v, e_m \rangle f_m
$$
对任一 $v \in V$ 都成立。

## 7.74 定义：对角矩阵（diagonal matrix）
$M \times N$ 矩阵 $A$ 被称为对角矩阵，如果除了 $A_{i,i}$（$i = 1, \dots, \min\{M, N\}$）可能不为 0 以外，所有元素都为 0。

## 7.75 伴随和伪逆的奇异值分解
设 $T \in L(V, W)$ 且 $T$ 的正奇异值是 $\sigma_1, \dots, \sigma_m$。设 $e_1, \dots, e_m$ 和 $f_1, \dots, f_m$ 是 $V$ 和 $W$ 中的规范正交组，使得对任一 $v \in V$ 都有
$$
Tv = \sigma_1 \langle v, e_1 \rangle f_1 + \dots + \sigma_m \langle v, e_m \rangle f_m.
$$
那么，对任一 $w \in W$ 都有
$$
T^*w = \sigma_1 \langle w, f_1 \rangle e_1 + \dots + \sigma_m \langle w, f_m \rangle e_m
$$
和
$$
T^\dagger w = \frac{\langle w, f_1 \rangle}{\sigma_1} e_1 + \dots + \frac{\langle w, f_m \rangle}{\sigma_m} e_m.
$$

## 7.79 例：求奇异值分解
定义 $T \in L(F^4, F^3)$ 为 $T(v_1, v_2, v_3, v_4) = (-5v_4, 0, v_1 + v_2)$。我们想求 $T$ 的奇异值分解。$T$ （关于标准基）的矩阵是
$$
\begin{bmatrix}
0 & 0 & 0 & -5 \\
0 & 0 & 0 & 0 \\
1 & 1 & 0 & 0
\end{bmatrix}.
$$
那么，正如例 7.67 讨论过的那样，$T^*T$ 的矩阵是
$$
\begin{bmatrix}
1 & 1 & 0 & 0 \\
1 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 25
\end{bmatrix},
$$
正特征值是 25 和 2；而 $\dim A(25, T^*T) = 1$，$\dim A(2, T^*T) = 1$。所以，$T$ 的正奇异值是 5 和 $\sqrt{2}$。
所以，为求出 $T$ 的奇异值分解，我们必须求出 $F^4$ 中的一规范正交组 $e_1, e_2$ 和 $F^3$ 中的一规范正交组 $f_1, f_2$ 使得
$$
Tv = 5 \langle v, e_1 \rangle f_1 + \sqrt{2} \langle v, e_2 \rangle f_2
$$
对所有 $v \in F^4$ 成立。
$A(25, T^*T)$ 的一规范正交基是向量 $(0, 0, 0, 1)$，$A(2, T^*T)$ 的一规范正交基是向量 $\left( \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0, 0 \right)$。所以，根据 7.70 的证明，我们可以取
$$
e_1 = (0, 0, 0, 1) \quad \text{和} \quad e_2 = \left( \frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0, 0 \right)
$$
以及
$$
f_1 = \frac{T e_1}{5} = (-1, 0, 0) \quad \text{和} \quad f_2 = \frac{T e_2}{\sqrt{2}} = (0, 0, 1).
$$
然后，不出所料，我们可以看到 $e_1, e_2$ 就是 $F^4$ 中的规范正交组，$f_1, f_2$ 就是 $F^3$ 中的规范正交组，而且
$$
Tv = 5 \langle v, e_1 \rangle f_1 + \sqrt{2} \langle v, e_2 \rangle f_2
$$
对所有 $v \in F^4$ 成立。那么，我们就求出了 $T$ 的奇异值分解。

## 7.80 奇异值分解（SVD）的矩阵版本
设 $A$ 是 $p \times n$ 矩阵（秩 $m \geq 1$）。那么，存在列规范正交的 $p \times m$ 矩阵 $U$，对角线上为正数的 $m \times m$ 对角矩阵 $\Sigma$ 以及列规范正交的 $n \times m$ 矩阵 $V$ 使得
$$
A = U \Sigma V^*.
$$

## 7.82 $\|T\|$ 的上界
设 $T \in L(V, W)$。令 $\sigma_1$ 是 $T$ 的最大奇异值。那么
$$
\|Tv\| \leq \sigma_1 \|v\|
$$
对所有 $v \in V$ 成立。

## 7.86 定义：线性映射的范数（norm of a linear map）、$\| \cdot \|$
设 $T \in L(V, W)$。那么，$T$ 的范数，记为 $\|T\|$，定义为
$$
\|T\| = \max \{ \|Tv\| : v \in V \text{ 且 } \|v\| \leq 1 \}。
$$

## 7.87 线性映射范数的基本性质
设 $T \in L(V, W)$，那么
- $\|T\| \geq 0$；
- $\|T\| = 0 \iff T = 0$；
- $\|\lambda T\| = |\lambda| \|T\|$ 对所有 $\lambda \in \mathbb{F}$ 成立；
- $\|T + S\| \leq \|T\| + \|S\|$ 对所有 $S \in L(V, W)$ 成立。

## 7.88 $\|T\|$ 的多种表达式
设 $T \in L(V, W)$，那么
- $\|T\| = T$ 的最大奇异值；
- $\|T\| = \max \{ \|Tv\| : v \in V \text{ 且 } \|v\| = 1 \}$；
- $\|T\| =$ 使得 $\|Tv\| \leq a \|v\|$ 对所有 $v \in V$ 成立的最小数 $a$。

## 7.91 伴随的范数
设 $T \in L(V, W)$，那么 $\|T^*\| = \|T\|$。

## 7.92 用值域维数至多为 $k$ 的线性映射得到的最佳逼近
设 $T \in L(V, W)$ 且 $\sigma_1 \geq \dots \geq \sigma_m$ 是 $T$ 的正奇异值。设 $1 \leq k < m$，那么有
$$
\min \{ \|T - S\| : S \in L(V, W) \text{ 且 } \dim \text{range } S \leq k \} = \sigma_{k+1}。
$$
进一步，如果
$$
Tv = \sigma_1 \langle v, e_1 \rangle e_1 + \dots + \sigma_m \langle v, e_m \rangle e_m
$$
是 $T$ 的奇异值分解，而 $T_k \in L(V, W)$ 定义为
$$
T_k v = \sigma_1 \langle v, e_1 \rangle e_1 + \dots + \sigma_k \langle v, e_k \rangle e_k
$$
对任一 $v \in V$ 都成立，那么 $\dim \text{range } T_k = k$ 且 $\|T - T_k\| = \sigma_{k+1}$。

## 7.93 极分解（polar decomposition）
设 $T \in L(V)$，那么存在幺正算子 $U \in L(V)$ 使得
$$
T = U \sqrt{T^* T}。
$$

## 7.95 定义：球（ball）、$B$
$V$ 中半径为 1、以 0 为心的球（ball），记为 $B$，定义为
$$
B = \{ v \in V : \|v\| \leq 1 \}。
$$

## 7.96 定义：椭球（ellipsoid）、$E(\sigma_1 e_1, \dots, \sigma_n e_n)$，主轴（principal axes）
设 $e_1, \dots, e_n$ 是 $V$ 的规范正交基，$\sigma_1, \dots, \sigma_n$ 是正数。主轴为 $\sigma_1 e_1, \dots, \sigma_n e_n$ 的椭球 $E(\sigma_1 e_1, \dots, \sigma_n e_n)$ 定义为
$$
E(\sigma_1 e_1, \dots, \sigma_n e_n) = \left\{ v \in V : \frac{|\langle v, e_1 \rangle|^2}{\sigma_1^2} + \dots + \frac{|\langle v, e_n \rangle|^2}{\sigma_n^2} < 1 \right\}。
$$

## 7.98 记号：$T(\Omega)$
对于定义在 $V$ 上的函数 $T$，以及 $\Omega \subseteq V$，定义 $T(\Omega)$ 为
$$
T(\Omega) = \{ Tv : v \in \Omega \}。
$$

## 7.99 可逆算子化球为椭球
设 $T \in L(V)$ 可逆，那么 $T$ 将 $V$ 中的球 $B$ 映成 $V$ 中的椭球。

## 7.101 可逆算子化椭球为椭球
设 $T \in L(V)$ 可逆，且 $E$ 是 $V$ 中的椭球。那么 $T(E)$ 是 $V$ 中的椭球。

## 7.102 定义：$P(v_1, \dots, v_n)$、平行体（parallelepiped）
设 $v_1, \dots, v_n$ 是 $V$ 的基，令
$$
P(v_1, \dots, v_n) = \{ a_1 v_1 + \dots + a_n v_n : a_1, \dots, a_n \in (0, 1) \}。
$$
平行体是形如 $v + P(v_1, \dots, v_n)$ 的集合，其中 $v \in V$。向量 $v_1, \dots, v_n$ 称为该平行体的边（edges）。

## 7.104 可逆算子化平行体为平行体
设 $v \in V$ 且 $v_1, \dots, v_n$ 是 $V$ 的基。设 $T \in L(V)$ 可逆，那么
$$
T(v + P(v_1, \dots, v_n)) = Tv + P(Tv_1, \dots, Tv_n)。
$$

## 7.105 定义：长方体（box）
$V$ 中的长方体是形如
$$
v + P(\sigma_1 e_1, \dots, \sigma_n e_n)
$$
的集合，其中 $v \in V$，$\sigma_1, \dots, \sigma_n$ 是正数，$e_1, \dots, e_n$ 是 $V$ 的规范正交基。

## 7.107 每个可逆算子都将某些长方体化成长方体
设 $T \in L(V)$ 可逆。设 $T$ 有奇异值分解
$$
Tv = \sigma_1 \langle v, e_1 \rangle e_1 + \dots + \sigma_n \langle v, e_n \rangle e_n，
$$
其中，$\sigma_1, \dots, \sigma_n$ 是 $T$ 的奇异值，$e_1, \dots, e_n$ 和 $f_1, \dots, f_n$ 是 $V$ 的规范正交基，上式对所有 $v \in V$ 成立。那么，对于所有正数 $\sigma_1, \dots, \sigma_n$ 和所有 $v \in V$，$T$ 将长方体 $v + P(\sigma_1 e_1, \dots, \sigma_n e_n)$ 映成长方体 $Tv + P(\sigma_1 \sigma_1 f_1, \dots, \sigma_n \sigma_n f_n)$。

## 7.108 定义：长方体的体积（volume of a box）
设 $F = \mathbb{R}$。如果 $v \in V$，$\sigma_1, \dots, \sigma_n$ 是正数，$e_1, \dots, e_n$ 是 $V$ 的规范正交基，那么
$$
\text{volume}(v + P(\sigma_1 e_1, \dots, \sigma_n e_n)) = \sigma_1 \times \dots \times \sigma_n。
$$

## 7.109 定义：体积（volume）
设 $F = \mathbb{R}$，$\Omega \subseteq V$。那么 $\Omega$ 的体积，记为 $\text{volume} \Omega$，约等于逼近 $\Omega$ 的若干个不相交长方体的体积之和。

## 7.111 体积变化倍数是奇异值的乘积
设 $F = \mathbb{R}$，$T \in L(V)$ 可逆，且 $\Omega \subseteq V$。那么
$$
\text{volume} T(\Omega) = (\text{T 的奇异值的乘积})(\text{volume} \Omega)。
$$