#### 3.1 线性映射 (Linear Map)

一个从$V$到$W$的线性映射是一个满足下列性质的函数$T:V \rightarrow W$：

- **可加性 (Additivity)**：对于所有$u,v \in V$，均有$T(u + v) = Tu + Tv$。
- **齐次性 (Homogeneity)**：对于所有$\lambda \in F$和所有$v \in V$，均有$T(\lambda v) = \lambda(Tv)$。

#### 3.2 记号$\mathcal{L}(V,W)$、$\mathcal{L}(V)$

- 从$V$到$W$的全体线性映射构成的集合记作$\mathcal{L}(V,W)$。
- 从$V$到$V$的全体线性映射构成的集合记作$\mathcal{L}(V)$。

#### 3.3 线性映射的实例

- **零映射 (Zero)**：$0\mathcal{\in L}(V,W)$定义为$0v = 0$。
- **恒等算子 (Identity Operator)**：$I\mathcal{\in L}(V)$定义为$Iv = v$。
- **微分映射 (Differentiation)**：$D\mathcal{\in L}\left( \mathcal{P}(R) \right)$定义为$Dp = p'$。
- **积分映射 (Integration)**：$T\mathcal{\in L}\left( \mathcal{P}(R),R \right)$定义为$Tp = \int_{0}^{1}p$。
- **与**$x^{2}$**相乘映射 (Multiplication by**$x^{2}$**)**：$T\mathcal{\in L}\left( \mathcal{P}(R) \right)$定义为$(Tp)(x) = x^{2}p(x)$。
- **后向移位映射 (Backward Shift)**：$T\mathcal{\in L}\left( F^{\infty} \right)$定义为$T\left( x_{1},x_{2},x_{3},\ldots \right) = \left( x_{2},x_{3},\ldots \right)$。
- **从**$R^{3}$**到**$R^{2}$**的映射**：$T\mathcal{\in L}\left( R^{3},R^{2} \right)$定义为$T(x,y,z) = (2x - y + 3z,7x + 5y - 6z)$。
- **从**$F^{n}$**到**$F^{m}$**的映射**：$T\mathcal{\in L}\left( F^{n},F^{m} \right)$定义为$T\left( x_{1},\ldots,x_{n} \right) = \left( A_{1,1}x_{1} + \cdots + A_{1,n}x_{n},\ldots,A_{m,1}x_{1} + \cdots + A_{m,n}x_{n} \right)$。
- **多项式复合映射 (Composition)**：$T\mathcal{\in L}\left( \mathcal{P}(R) \right)$定义为$(Tp)(x) = p\left( q(x) \right)$。

#### 3.4 线性映射引理 (Linear Map Lemma)

假定$v_{1},\ldots,v_{n}$是$V$的基且$w_{1},\ldots,w_{n} \in W$。那么存在唯一的线性映射$T:V \rightarrow W$使得对每个$k = 1,\ldots,n$都有


$$
Tv_{k} = w_{k}.
$$


#### 3.5 定义：$\mathcal{L}(V,W)$上的加法和标量乘法

假设$S,T\mathcal{\in L}(V,W)$且$\lambda \in F$。**和**$S + T$与**积**$\lambda T$是从$V$到$W$的线性映射，分别定义如下：对于所有$v \in V$，


$$
(S + T)(v) = Sv + Tv,\quad(\lambda T)(v) = \lambda(Tv).
$$


#### 3.6$\mathcal{L}(V,W)$是向量空间

有了上面定义的加法和标量乘法，$\mathcal{L}(V,W)$就是向量空间。

#### 3.7 定义：线性映射的乘积（**product of linear maps**）

如果$T\mathcal{\in L}(U,V)$且$S\mathcal{\in L}(V,W)$，那么乘积$ST\mathcal{\in L}(U,W)$定义为：对于所有$u \in U$，


$$
(ST)(u) = S(Tu).
$$


#### 3.8 线性映射乘积的代数性质

- **可结合性 (Associativity)**：对于任意使乘积有意义的线性映射$T_{1},T_{2},T_{3}$，有$\left( T_{1}T_{2} \right)T_{3} = T_{1}\left( T_{2}T_{3} \right)$。
- **恒等元 (Identity)**：对于任意$T\mathcal{\in L}(V,W)$，有$TI = IT = T$。
- **分配性质 (Distributive Properties)**：对于任意$T,T_{1},T_{2}\mathcal{\in L}(U,V)$和$S,S_{1},S_{2}\mathcal{\in L}(V,W)$，有$\left( S_{1} + S_{2} \right)T = S_{1}T + S_{2}T$且$S\left( T_{1} + T_{2} \right) = ST_{1} + ST_{2}$。

#### 3.10 线性映射将 0 映射为 0

假设$T$是由$V$到$W$的线性映射。那么$T(0) = 0$。

#### 3.11 定义：零空间 (Null Space)，$\text{null }T$

对于$T\mathcal{\in L}(V,W)$，$T$的**零空间**记为$\text{null }T$，是$V$的子集，其由被$T$映射到0 的所有向量构成：


$$
\text{null }T = \{ v \in V:Tv = 0\}.
$$


#### 3.13 零空间是子空间

假设$T\mathcal{\in L}(V,W)$。那么$\text{null }T$是$V$的子空间。

#### 3.14 定义：单射 (Injective)

对于函数$T:V \rightarrow W$，若$Tu = Tv$蕴涵$u = v$，则称该函数是单射。

#### 3.15 单射性$\Leftrightarrow$零空间等于$\{ 0\}$

令$T\mathcal{\in L}(V,W)$。那么$T$是单射当且仅当$\text{null }T = \{ 0\}$。

#### 3.16 定义：值域 (Range)

对于$T\mathcal{\in L}(V,W)$，$T$的值域是$W$的子集，由所有等于$Tv$（其中$v \in V$）的向量构成：


$$
\text{range }T = \{ Tv:v \in V\}.
$$


#### 3.18 值域是子空间

如果$T\mathcal{\in L}(V,W)$，那么$\text{range }T$是$W$的子空间。

#### 3.19 定义：满射 (Surjective)

如果函数$T:V \rightarrow W$的值域等于$W$，则称该函数为满射。

#### 3.21 线性映射基本定理 (Fundamental Theorem of Linear Maps)

假设$V$是有限维的且$T\mathcal{\in L}(V,W)$。那么$\text{range }T$是有限维的，且


$$
\dim V = dim\text{null }T + dim\text{range }T.
$$


#### 3.22 映到更低维空间上的线性映射不是单射

假设$V$和$W$是有限维向量空间且满足$\dim V > dimW$。那么从$V$到$W$的线性映射都不是单射。

#### 3.24 映到更高维空间上的线性映射不是满射

假设$V$和$W$是有限维向量空间且满足$\dim V < dimW$。那么从$V$到$W$的线性映射都不是满射。

#### 3.26 齐次线性方程组

未知数个数多于方程个数的齐次线性方程组具有非零解。

#### 3.28 方程个数多于未知数个数的线性方程组

方程个数多于未知数个数的线性方程组当常数项取某些值时无解。

#### 3.29 定义: 矩阵(matrix)、$A_{j,k}$

假设 $m$ 和 $n$ 是非负整数。$m \times n$ 矩阵 $A$ 是由 $F$ 中元素构成的
$m$ 行 $n$ 列的矩形阵列：


$$

A = \begin{pmatrix}
A_{1,1} & \cdots & A_{1,n} \\
 \vdots & & \vdots \\
A_{m,1} & \cdots & A_{m,n}
\end{pmatrix}.

$$


记号 $A_{j,k}$ 表示 $A$ 的第 $j$ 行第 $k$ 列中的元素。

#### 3.31 定义: 线性映射的矩阵(matrix of a linear map)、$\mathcal{M}(T)$

假设 $T\mathcal{\in L}(V,W)$，$v_{1},\ldots,v_{n}$ 是 $V$
的基，$w_{1},\ldots,w_{m}$ 是 $W$ 的基，$T$ 关于这些基的矩阵是
$m \times n$ 矩阵 $\mathcal{M}(T)$，其中各元素 $A_{j,k}$ 由下式定义：


$$
Tv_{k} = A_{1,k}w_{1} + \cdots + A_{m,k}w_{m}.
$$


#### 3.34 定义: 矩阵加法(matrix addition)

两个相同大小的矩阵之和，是将两矩阵对应位置上的元素相加所得的矩阵：


$$

\begin{pmatrix}
A_{1,1} & \cdots & A_{1,n} \\
 \vdots & & \vdots \\
A_{m,1} & \cdots & A_{m,n}
\end{pmatrix} + \begin{pmatrix}
C_{1,1} & \cdots & C_{1,n} \\
 \vdots & & \vdots \\
C_{m,1} & \cdots & C_{m,n}
\end{pmatrix} = \begin{pmatrix}
A_{1,1} + C_{1,1} & \cdots & A_{1,n} + C_{1,n} \\
 \vdots & & \vdots \\
A_{m,1} + C_{m,1} & \cdots & A_{m,n} + C_{m,n}
\end{pmatrix}.

$$


#### 3.35 线性映射之和的矩阵

假设 $S,T\mathcal{\in L}(V,W)$。那么
$\mathcal{M}(S + T)\mathcal{= M}(S)\mathcal{+ M}(T)$。

#### 3.36 定义: 矩阵的标量乘法(scalar multiplication of a matrix)

一个标量和一个矩阵的乘积，是将矩阵的各元素都乘以那个标量所得的矩阵：


$$

\lambda\begin{pmatrix}
A_{1,1} & \cdots & A_{1,n} \\
 \vdots & & \vdots \\
A_{m,1} & \cdots & A_{m,n}
\end{pmatrix} = \begin{pmatrix}
\lambda A_{1,1} & \cdots & \lambda A_{1,n} \\
 \vdots & & \vdots \\
\lambda A_{m,1} & \cdots & \lambda A_{m,n}
\end{pmatrix}.

$$


#### 3.38 标量与线性映射之积的矩阵

假设 $\lambda \in F$ 且 $T\mathcal{\in L}(V,W)$。那么
$\mathcal{M}(\lambda T) = \lambda\mathcal{M}(T)$。

#### 3.39 记号: $F^{m,n}$

对于正整数 $m$ 和 $n$，各元素均属于 $F$ 的所有 $m \times n$
矩阵构成的集合记作 $F^{m,n}$。

#### 3.40 $\dim F^{m,n} = mn$

假设 $m$ 和 $n$ 为正整数。按上面定义的加法和标量乘法，$F^{m,n}$ 是维数为
$mn$ 的向量空间。

#### 3.41 定义: 矩阵乘法(matrix multiplication)

假设 $A$ 是 $m \times n$ 矩阵且 $B$ 是 $n \times p$ 矩阵。那么 $AB$
定义为一个 $m \times p$ 矩阵，其中第 $j$ 行第 $k$ 列的元素由下式给出：


$$
(AB)_{j,k} = \sum_{r = 1}^{n}A_{j,r}B_{r,k}.
$$


#### 3.43 线性映射之积的矩阵

如果 $T\mathcal{\in L}(U,V)$ 且 $S\mathcal{\in L}(V,W)$，那么
$\mathcal{M}(ST)\mathcal{= M}(S)\mathcal{M}(T)$。

#### 3.44 记号: $A_{j, \cdot}$、$A_{\cdot ,k}$

假设 $A$ 是一个 $m \times n$ 矩阵。

- 如果 $1 \leq j \leq m$，那么 $A_{j, \cdot}$ 表示由 $A$ 的第 $j$行构成的 $1 \times n$ 矩阵。
- 如果 $1 \leq k \leq n$，那么 $A_{\cdot ,k}$ 表示由 $A$ 的第 $k$列构成的 $m \times 1$ 矩阵。

#### 3.46 矩阵之积的元素等于行乘以列

假设 $A$ 是 $m \times n$ 矩阵且 $B$ 是 $n \times p$ 矩阵。那么如果$1 \leq j \leq m$ 且 $1 \leq k \leq p$，则


$$
(AB)_{j,k} = A_{j, \cdot}B_{\cdot ,k}.
$$


#### 3.48 矩阵之积的列等于矩阵与列之积

假设 $A$ 是 $m \times n$ 矩阵且 $B$ 是 $n \times p$ 矩阵。那么如果$1 \leq k \leq p$，则


$$
(AB)_{\cdot ,k} = AB_{\cdot ,k}.
$$


#### 3.50 列的线性组合

假设 $A$ 是 $m \times n$ 矩阵且 $b = \begin{pmatrix}
b_{1} \\
 \vdots \\
b_{n}
\end{pmatrix}$ 是 $n \times 1$ 矩阵。那么


$$
Ab = b_{1}A_{\cdot ,1} + \cdots + b_{n}A_{\cdot ,n}.
$$


#### 3.51 将矩阵乘法视为列或行的线性组合

假设 $C$ 是 $m \times c$ 矩阵且 $R$ 是 $c \times n$ 矩阵。

- 如果 $k \in \{ 1,\ldots,n\}$，那么 $CR$ 的第 $k$ 列是 $C$的各列的线性组合，其中各系数来自 $R$ 的第 $k$ 列。
- 如果 $j \in \{ 1,\ldots,m\}$，那么 $CR$ 的第 $j$ 行是 $R$的各行的线性组合，其中各系数来自 $C$ 的第 $j$ 行。

#### 3.52 定义: 列秩(column rank)、行秩(row rank)

假设 $A$ 是 $m \times n$ 矩阵，其各元素属于 $F$。

- $A$ 的**列秩**是 $A$ 的各列在 $F^{m,1}$ 中的张成空间的维数。

- $A$ 的**行秩**是 $A$ 的各行在 $F^{1,n}$ 中的张成空间的维数。

#### 3.54 定义: 转置(transpose)、$A^{t}$

矩阵 $A$ 的**转置**记为 $A^{t}$，是互换 $A$
的行和列所得的矩阵。具体地说，如果 $A$ 是 $m \times n$ 矩阵，那么
$A^{t}$ 是 $n \times m$ 矩阵，其中各元素由下面等式给出：


$$
\left( A^{t} \right)_{k,j} = A_{j,k}.
$$


#### 3.56 行列分解(column-row factorization)

假设 $A$ 是 $m \times n$ 矩阵，其中各元素均在 $F$ 中且列秩
$c \geq 1$。那么存在各元素均属于 $F$ 的 $m \times c$ 矩阵 $C$ 和
$c \times n$ 矩阵 $R$，使得 $A = CR$ 成立。

#### 3.57 列秩等于行秩

假设 $A \in F^{m,n}$。那么 $A$ 的列秩等于 $A$ 的行秩。

#### 3.58 定义: 秩(rank)

矩阵 $A \in F^{m,n}$ 的**秩**是 $A$ 的列秩。

#### 3.59 定义: 可逆的(invertible)、逆(inverse)

- 对于线性映射 $T\mathcal{\in L}(V,W)$，如果存在线性映射
$S\mathcal{\in L}(W,V)$，使得 $ST$ 等于 $V$ 上的恒等算子且 $TS$ 等于 $W$
上的恒等算子，则称 $T$ 是**可逆的**。

- 一个满足 $ST = I$ 及 $TS = I$ 的线性映射 $S\mathcal{\in L}(W,V)$
被称为 $T$ 的一个**逆**。（注意，第一个 *𝐼* 是 *𝑉* 上的恒等算子，第二个
*𝐼* 是 *𝑊* 上的恒等算子）

#### 3.60 逆是唯一的

可逆的线性映射具有唯一的逆。

#### 3.61 记号: $T^{- 1}$

如果 $T$ 是可逆的，那么它的逆记作 $T^{- 1}$。

#### 3.63 可逆性 $\Leftrightarrow$ 单射性和满射性

一个线性映射是可逆的，当且仅当它既是单射又是满射。

#### 3.65 若 $\dim V = dimW < \infty$，则单射性与满射性等价

假设 $V$ 和 $W$ 都是有限维向量空间，$\dim V = dimW$，且
$T\mathcal{\in L}(V,W)$。那么


$$
T\text{可逆} \Leftrightarrow T\text{是单射} \Leftrightarrow T\text{是满射}.
$$


#### 3.68 $ST = I \Leftrightarrow TS = I$ ($S$ 和 $T$ 作用于维数相同的向量空间)

假设 $V$ 和 $W$ 是维数相同的有限维向量空间，$S\mathcal{\in L}(W,V)$ 且
$T\mathcal{\in L}(V,W)$。那么 $ST = I$ 当且仅当 $TS = I$。

#### 3.69 定义: 同构(isomorphism)、同构的(isomorphic)

- 一个**同构**就是一个可逆线性映射。

-
对于两个向量空间，若存在将其中一个向量空间映成另一个向量空间的同构，则称它们是**同构的**。

#### 3.70 维数表明了向量空间是否同构

对于 $F$
上的两个有限维向量空间，当且仅当它们的维数相同时，它们才是同构的。

#### 3.71 $\mathcal{L}(V,W)$ 与 $F^{m,n}$ 是同构的

设 $v_{1},\ldots,v_{n}$ 是 $V$ 的基且 $w_{1},\ldots,w_{m}$ 是 $W$
的基。那么 $\mathcal{M}$ 是 $\mathcal{L}(V,W)$ 与 $F^{m,n}$ 间的同构。

#### 3.72 $\dim\mathcal{L}(V,W) = \left( \dim V \right)\left( \dim W \right)$

假设 $V$ 和 $W$ 是有限维的。那么 $\mathcal{L}(V,W)$ 是有限维的，且


$$
\dim\mathcal{L}(V,W) = \left( \dim V \right)\left( \dim W \right).
$$


#### 3.73 定义: 向量的矩阵(matrix of a vector)、$\mathcal{M}(v)$

假设 $v \in V$ 且 $v_{1},\ldots,v_{n}$ 是 $V$ 的基。$v$
关于该基的**矩阵**是 $n \times 1$ 矩阵


$$

\mathcal{M}(v) = \begin{pmatrix}
b_{1} \\
 \vdots \\
b_{n}
\end{pmatrix},

$$


其中 $b_{1},\ldots,b_{n}$ 是使得下式成立的标量：


$$
v = b_{1}v_{1} + \cdots + b_{n}v_{n}.
$$


#### 3.75 $\mathcal{M}(T)_{\cdot ,k}\mathcal{= M}\left( Tv_{k} \right)$

设 $T\mathcal{\in L}(V,W)$，$v_{1},\ldots,v_{n}$ 是 $V$ 的基且
$w_{1},\ldots,w_{m}$ 是 $W$ 的基。令 $1 \leq k \leq n$。那么
$\mathcal{M}(T)$ 的第 $k$ 列，记作 $\mathcal{M}(T)_{\cdot ,k}$，就等于
$\mathcal{M}\left( Tv_{k} \right)$。

#### 3.76 线性映射的作用就像矩阵乘法

假设 $T\mathcal{\in L}(V,W)$ 且 $v \in V$。假设 $v_{1},\ldots,v_{n}$ 是
$V$ 的基且 $w_{1},\ldots,w_{m}$ 是 $W$ 的基。那么


$$
\mathcal{M}(Tv)\mathcal{= M}(T)\mathcal{M}(v).
$$


#### 3.78 range $T$ 的维数等于 $\mathcal{M}(T)$ 的列秩

假设 $V$ 和 $W$ 是有限维的，$T\mathcal{\in L}(V,W)$。那么 $dimrangeT$
等于 $\mathcal{M}(T)$ 的列秩。

#### 3.79 定义: 恒等矩阵(identity matrix)、$I$

设 $n$ 为正整数。仅对角线上（即那些行号和列号相等的位置）的元素为 $1$
而其他各元素均为 $0$ 的 $n \times n$ 矩阵


$$

\begin{pmatrix}
1 & & 0 \\
 & \ddots & \\
0 & & 1
\end{pmatrix}

$$


就称为恒等矩阵，记作 $I$。

#### 3.80 定义: 可逆的(invertible)、逆(inverse)、$A^{- 1}$

称方阵 $A$ 是可逆的，如果存在与之大小相等的方阵 $B$ 使得
$AB = BA = I$。我们称 $B$ 是 $A$ 的逆且将其记为 $A^{- 1}$。

#### 3.81 线性映射之积的矩阵

设 $T\mathcal{\in L}(U,V)$ 且 $S\mathcal{\in L}(V,W)$。如果
$u_{1},\ldots,u_{m}$ 是 $U$ 的基，$v_{1},\ldots,v_{n}$ 是 $V$ 的基且
$w_{1},\ldots,w_{p}$ 是 $W$ 的基，那么


$$
\mathcal{M}\left( ST,\left( u_{1},\ldots,u_{m} \right),\left( w_{1},\ldots,w_{p} \right) \right)\mathcal{= M}\left( S,\left( v_{1},\ldots,v_{n} \right),\left( w_{1},\ldots,w_{p} \right) \right)\mathcal{M}\left( T,\left( u_{1},\ldots,u_{m} \right),\left( v_{1},\ldots,v_{n} \right) \right).
$$


**3.82** 恒等算子关于两个基的矩阵

假设 *𝑢*1*, . . . , 𝑢𝑛* 和 *𝑣*1*, . . . , 𝑣𝑛* 是 *𝑉* 的两个基．那么矩阵

M *𝐼,* (*𝑢*1*, . . . , 𝑢𝑛*)*,* (*𝑣*1*, . . . , 𝑣𝑛*) 和 M *𝐼,* (*𝑣*1*, .
. . , 𝑣𝑛*)*,* (*𝑢*1*, . . . , 𝑢𝑛*)

都是可逆的，且互为对方的逆．

**3.84** 换基公式（**change-of-basis formula**）

设 *𝑇* ∈ L (*𝑉*)．假设 *𝑢*1*, . . . , 𝑢𝑛* 和 *𝑣*1*, . . . , 𝑣𝑛* 都是 *𝑉*
的基．令

*𝐴* = M *𝑇,* (*𝑢*1*, . . . , 𝑢𝑛*) 且 *𝐵* = M *𝑇,* (*𝑣*1*, . . . , 𝑣𝑛*)

且 *𝐶* = M *𝐼,* (*𝑢*1*, . . . , 𝑢𝑛*)*,* (*𝑣*1*, . . . , 𝑣𝑛*) ．那么

*𝐴* = *𝐶* −1*𝐵𝐶*．

**3.86** 逆的矩阵等于矩阵的逆

设 *𝑣*1*, . . . , 𝑣𝑛* 是 *𝑉* 的基且 *𝑇* ∈ L (*𝑉*) 是可逆的．那么 M (*𝑇*
−1 ) = M (*𝑇*)

−1，式中两个矩阵均是关于基 *𝑣*1*, . . . , 𝑣𝑛* 的．

#### 3.87 定义: 向量空间的积 (product of vector spaces)

设 $V_{1},\ldots,V_{m}$ 都是 $F$ 上的向量空间。

- **乘积** $V_{1} \times \cdots \times V_{m}$ 定义为


$$
V_{1} \times \cdots \times V_{m} = \left\{ \left( v_{1},\ldots,v_{m} \right):v_{1} \in V_{1},\ldots,v_{m} \in V_{m} \right\}.
$$


- $V_{1} \times \cdots \times V_{m}$ 上的加法定义为


$$
\left( u_{1},\ldots,u_{m} \right) + \left( v_{1},\ldots,v_{m} \right) = \left( u_{1} + v_{1},\ldots,u_{m} + v_{m} \right).
$$


- $V_{1} \times \cdots \times V_{m}$ 上的标量乘法定义为


$$
\lambda\left( v_{1},\ldots,v_{m} \right) = \left( \lambda v_{1},\ldots,\lambda v_{m} \right).
$$


#### 3.89 定理: 向量空间的积是向量空间

设 $V_{1},\ldots,V_{m}$ 都是 $F$ 上的向量空间。那么
$V_{1} \times \cdots \times V_{m}$ 是 $F$ 上的向量空间。

#### 3.92 定理: 向量空间之积的维数是各向量空间维数之和

设 $V_{1},\ldots,V_{m}$ 都是有限维向量空间。那么
$V_{1} \times \cdots \times V_{m}$ 是有限维的，且


$$
\dim\left( V_{1} \times \cdots \times V_{m} \right) = dimV_{1} + \cdots + dimV_{m}.
$$


#### 3.93 定理: 积与直和

设 $V_{1},\ldots,V_{m}$ 都是 $V$ 的子空间。由下式定义线性映射
$\Gamma:V_{1} \times \cdots \times V_{m} \rightarrow V_{1} + \cdots + V_{m}$：


$$
\Gamma\left( v_{1},\ldots,v_{m} \right) = v_{1} + \cdots + v_{m}.
$$


那么 $V_{1} + \cdots + V_{m}$ 是直和，当且仅当 $\Gamma$ 是单射。

#### 3.94 定理: 向量空间的和是直和，当且仅当该和的维数等于各求和项维数之和

设 $V$ 是有限维的，$V_{1},\ldots,V_{m}$ 都是 $V$ 的子空间。那么
$V_{1} + \cdots + V_{m}$ 是直和，当且仅当


$$
\dim\left( V_{1} + \cdots + V_{m} \right) = dimV_{1} + \cdots + dimV_{m}.
$$


#### 3.95 定义: 记号 $v + U$

设 $v \in V$ 且 $U \subseteq V$。那么 $v + U$ 是 $V$
的一个由下式定义的子集：


$$
v + U = \{ v + u:u \in U\}.
$$


#### 3.97 定义: 平移 (translate)

对于 $v \in V$ 和 $V$ 的一个子集 $U$，称集合 $v + U$ 是 $U$ 的一个平移。

#### 3.99 定义: 商空间 (quotient space)、$V/U$

设 $U$ 是 $V$ 的子空间。那么商空间 $V/U$ 是由 $U$
的所有平移构成的集合。从而


$$
V/U = \{ v + U:v \in V\}.
$$


#### 3.101 定理: 子空间的两个平移要么相等要么不相交

设 $U$ 是 $V$ 的一个子空间且 $v,w \in V$。那么


$$
v - w \in U \Leftrightarrow v + U = w + U \Leftrightarrow (v + U) \cap (w + U) \neq \varnothing.
$$


#### 3.102 定义: $V/U$ 上的加法和标量乘法

设 $U$ 是 $V$ 的一个子空间。那么 $V/U$
上的**加法**和**标量乘法**分别由下面两式定义：对所有 $v,w \in V$ 和所有
$\lambda \in F$，


$$
(v + U) + (w + U) = (v + w) + U
$$



$$
\lambda(v + U) = (\lambda v) + U.
$$


#### 3.103 定理: 商空间是向量空间

假设 $U$ 是 $V$ 的一个子空间。那么带有定义如上的加法和标量乘法的 $V/U$
就是一个向量空间。

#### 3.104 定义: 商映射 (quotient map)、$\pi$

设 $U$ 是 $V$ 的一个子空间。**商映射** $\pi:V \rightarrow V/U$
是由下式定义的线性映射：对每个 $v \in V$，


$$
\pi(v) = v + U
$$


#### 3.105 定理: 商空间的维数

设 $V$ 是有限维的，$U$ 是 $V$ 的子空间。那么


$$
\dim V/U = dimV - dimU.
$$


#### 3.106 定义: $\widetilde{T}$

设 $T\mathcal{\in L}(V,W)$。$\widetilde{T}:V/(nullT) \rightarrow W$
由下式定义：


$$
\widetilde{T}(v + nullT) = Tv.
$$


#### 3.107 定理: $\widetilde{T}$ 的零空间和值域

设 $T\mathcal{\in L}(V,W)$。那么

\(a\) $\widetilde{T} \circ \pi = T$，其中 $\pi$ 是将 $V$ 映成
$V/(nullT)$ 的商映射；

\(b\) $\widetilde{T}$ 是单射；

\(c\) $range\widetilde{T} = rangeT$；

\(d\) $V/(nullT)$ 和 $rangeT$ 是同构的向量空间。

#### 3.108 定义: 线性泛函 (linear functional)

$V$ 上的**线性泛函**是从 $V$ 到 $F$ 的线性映射。换言之，线性泛函是
$\mathcal{L}(V,F)$ 的元素。

#### 3.110 定义: 对偶空间 (dual space)、$V^{'}$

$V$ 的对偶空间记作 $V^{'}$，是 $V$
上全体线性泛函所构成的向量空间。换言之，$V^{'}\mathcal{= L}(V,F)$。

#### 3.111 定理: $\dim V^{'} = dimV$

假设 $V$ 是有限维的。那么 $V^{'}$ 也是有限维的，且


$$
\dim V^{'} = dimV.
$$


#### 3.112 定义: 对偶基 (dual basis)

如果 $v_{1},\ldots,v_{n}$ 是 $V$ 的基，那么 $v_{1},\ldots,v_{n}$
的对偶基是 $V^{'}$ 中的元素 $\varphi_{1},\ldots,\varphi_{n}$
所构成的组，其中各 $\varphi_{j}$ 是 $V$ 上满足下式的线性泛函：


$$

\varphi_{j}\left( v_{k} \right) = \left\{ \begin{matrix}
1 & \text{若}k = j, \\
0 & \text{若}k \neq j.
\end{matrix} \right.\ 

$$


#### 3.114 定理: 对偶基给出了线性组合的系数

假设 $v_{1},\ldots,v_{n}$ 是 $V$ 的基，且
$\varphi_{1},\ldots,\varphi_{n}$ 是其对偶基。那么对每个 $v \in V$，有


$$
v = \varphi_{1}(v)v_{1} + \cdots + \varphi_{n}(v)v_{n}.
$$


#### 3.116 定理: 对偶基是对偶空间的基

假设 $V$ 是有限维的。那么 $V$ 的基的对偶基是 $V^{'}$ 的基。

#### 3.118 定义: 对偶映射 (dual map)、$T^{'}$

设 $T\mathcal{\in L}(V,W)$。$T$ 的对偶映射是由下式定义的线性映射
$T^{'}\mathcal{\in L}\left( W^{'},V^{'} \right)$：对每个
$\varphi \in W^{'}$，


$$
T^{'}(\varphi) = \varphi \circ T.
$$


#### 3.120 定理: 对偶映射的代数性质

设 $T\mathcal{\in L}(V,W)$。那么 (a) 对所有
$S\mathcal{\in L}(V,W)$，均有 $(S + T)^{'} = S^{'} + T^{'}$； (b) 对所有
$\lambda \in F$，均有 $(\lambda T)^{'} = \lambda T^{'}$； (c) 对所有
$S\mathcal{\in L}(W,U)$，均有 $(ST)^{'} = T^{'}S^{'}$。

#### 3.121 定义: 零化子 (annihilator)、$U^{0}$

对 $U \subseteq V$，$U$ 的零化子，记作 $U^{0}$，定义为


$$
U^{0} = \left\{ \varphi \in V^{'}:\text{对所有}u \in U,\varphi(u) = 0 \right\}.
$$


#### 3.124 定理: 零化子是子空间

设 $U \subseteq V$。那么 $U^{0}$ 是 $V^{'}$ 的子空间。

#### 3.125 定理: 零化子的维数

设 $V$ 是有限维的且 $U$ 是 $V$ 的一个子空间。那么


$$
\dim U^{0} = dimV - dimU.
$$


#### 3.127 定理: 零化子等于 $\{ 0\}$ 或整个空间的条件

设 $V$ 是有限维的，且 $U$ 是 $V$ 的一个子空间。那么 (a)
$U^{0} = \{ 0\} \Leftrightarrow U = V$； (b)
$U^{0} = V^{'} \Leftrightarrow U = \{ 0\}$。

#### 3.128 定理: $T^{'}$ 的零空间

设 $V$ 和 $W$ 是有限维的且 $T\mathcal{\in L}(V,W)$。那么 (a)
$nullT^{'} = (rangeT)^{0}$； (b)
$dimnullT^{'} = dimnullT + dimW - dimV$。

#### 3.129 定理: $T$ 是满射等价于 $T^{'}$ 是单射

设 $V$ 和 $W$ 是有限维的且 $T\mathcal{\in L}(V,W)$。那么 $T$ 是满射
$\Leftrightarrow T^{'}$ 是单射。

#### 3.130 定理: $T^{'}$ 的值域

设 $V$ 和 $W$ 是有限维的且 $T\mathcal{\in L}(V,W)$。那么 (a)
$dimrangeT^{'} = dimrangeT$； (b) $rangeT^{'} = (nullT)^{0}$。

#### 3.131 定理: $T$ 是单射等价于 $T^{'}$ 是满射

设 $V$ 和 $W$ 是有限维的且 $T\mathcal{\in L}(V,W)$。那么 $T$ 是单射
$\Leftrightarrow T^{'}$ 是满射。

#### 3.132 定理: $T^{'}$ 的矩阵是 $T$ 的矩阵的转置

设 $V$ 和 $W$ 是有限维的且 $T\mathcal{\in L}(V,W)$。那么


$$

\mathcal{M}\left( T^{'} \right) = \left( \mathcal{M}(T) \right)^{t}.

$$

