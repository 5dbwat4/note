#### 1.1 定义：复数（complex numbers）、C

一个复数是一个有序对$(a, b)$，其中$a, b\in R$，不过我们会把这写成$a+bi$。

全体复数所构成的集合用C表示：

$$
C=\{a+b i: a, b\in R\}.
$$

#### 1.3 复数的算术性质

- 可交换性( commutativity)

  对于所有$\alpha,\beta\in C$，都有$\alpha+\beta=\beta+\alpha$以及$\alpha\beta=\beta\alpha$。
- 可结合性(associativity)

  对于所有$\alpha,\beta,\lambda\in C$，都有$(\alpha+\beta)+\lambda=\alpha+(\beta+\lambda)$以及$(\alpha\beta)\lambda=\alpha(\beta\lambda)$。
- 恒等元(identities)

  对于所有$\lambda\in C$，都有$\lambda+0=\lambda$以及$\lambda 1=\lambda$。
- 加法逆元(additive inverse)

  对于每个$\alpha\in C$，都存在唯一的$\beta\in C$使得$\alpha+\beta=0$。
- 乘法逆元(multiplicative inverse)

  对于每个$\alpha\in C$且$\alpha\neq 0$，都存在唯一的$\beta\in C$使得$\alpha\beta=1$。
- 分配性质(distributive property)

  对于所有$\lambda,\alpha,\beta\in C$，都有$\lambda(\alpha+\beta)=\lambda\alpha+\lambda\beta$。

#### 1.5 定义：-α、减法(subtraction), $1/\alpha$、除法(division)

假设$\alpha,\beta\in C$。

令$-\alpha$表示$\alpha$的加法逆元。于是$-\alpha$是唯一使得

$$
\alpha+(-\alpha)=0
$$

成立的复数。

C上的减法的定义为

$$
\beta-\alpha=\beta+(-\alpha).
$$

对于$\alpha\neq 0$，令$1/\alpha$和$\frac{1}{\alpha}$表示$\alpha$的乘法逆元。于是$1/\alpha$是唯一使得

$$
\alpha(1/\alpha)=1
$$

成立的复数。

对于$\alpha\neq 0$，除以$\alpha$的定义为

$$
\beta/\alpha=\beta(1/\alpha).
$$

#### 1.6 记号：F

在全书中，F代表R或C。

#### 1.8 定义：组(list)、长度(length)

假设n是非负整数。一个长度为n的组是n个有顺序的元素，这些元素可能是数、其他组或是更抽象的对象。

两个组是相等的，当且仅当它们具有相同的长度和按相同顺序排列的相同元素。

#### 1.10 记号：n

在本章剩余内容中，将n取为某一固定的正整数。

#### 1.11 定义：$F^n$、坐标(coordinate)

$F^n$是全体具有n个F中元素的组所构成的集合：

$$
F^n=\left\{\left(x_1,\ldots, x_n\right):\text{对于} k=1,\ldots, n\text{有} x_k\in F\right\}.
$$

对于$\left(x_1,\ldots, x_n\right)\in F^n$和$k\in\{1,\ldots, n\}$，我们称$x_k$是$\left(x_1,\ldots, x_n\right)$的第k个坐标。

#### 1.13 定义：$F^n$中的加法( addition in $F^n$ )

$F^n$中的加法定义为将对应坐标分别相加：

$$
\left(x_1,\ldots, x_n\right)+\left(y_1,\ldots, y_n\right)=\left(x_1+y_1,\ldots, x_n+y_n\right).
$$

#### 1.15 记号：0

令0表示长度为n且所有坐标都是0的组：

$$
0=(0,\ldots, 0).
$$

#### 1.17 定义：$F^n$中的加法逆元(additive inverse in $F^n$ )、-x

对于$x\in F^n$，x的加法逆元，记作-x，是满足下式的向量$-x\in F^n$：

$$
x+(-x)=0
$$

由此，如果$x=\left(x_1,\ldots, x_n\right)$，那么$-x=\left(-x_1,\ldots,-x_n\right)$。

#### 1.18 定义：$F^n$中的标量乘法(scalar multiplication in $F^n$ )

数$\lambda$与$F^n$中的向量之乘积(product)是通过将这向量的每一个坐标都乘以$\lambda$计算得到的：

$$
\lambda\left(x_1,\ldots, x_n\right)=\left(\lambda x_1,\ldots,\lambda x_n\right)
$$

此处$\lambda\in F$且$\left(x_1,\ldots, x_n\right)\in F^n$。

#### 1.20 定义：向量空间(vector space)

一个向量空间是一个集合V，V上的加法和标量乘法满足下列性质：

- **可交换性( commutativity)**
  对于所有$u, v\in V$，都有$u+v=v+u$。
- **可结合性(associativity)**
  对于所有$u, v, w\in V$以及所有$a, b\in F$，都有$(u+v)+w=u+(v+w)$以及$(a b) v= a(b v)$。
- **加法恒等元(additive identity)**
  对于所有$v\in V$，都存在$0\in V$使得$v+0=v$。
- **加法逆元(additive inverse)**
  对于每个$v\in V$，都存在$w\in V$使得$v+w=0$。
- **乘法恒等元(multiplicative identity)**
  对于所有$v\in V$，都有$1 v=v$。
- **分配性质(distributive properties)**
  对于所有$u, v\in V$以及所有$a, b\in F$，都有$a(u+v)=a u+a v$且$(a+b) v=a v+b v$。

#### 1.21 定义：向量(vector)、点(point)

向量空间的元素被称作向量或点。

#### 1.22 定义：实向量空间(real vector space)、复向量空间(complex vector space)

R上的向量空间称作实向量空间。

C上的向量空间称作复向量空间。

#### 1.24 记号：$F^S$

如果S是一个集合，那么$F^S$表示从S到F的所有函数构成的集合。

#### 1.28 记号：$-v$,$w-v$

令$v, w\in V$，那么

-v表示v的加法逆元；

$w-v$定义为$w+(-v)$。

#### 1.29 记号：V

在本书的剩余部分中，V表示F上的向量空间。

#### 1.33 定义：子空间(subspace)

如果V的子集U是与V具有相同的加法恒等元、加法和标量乘法运算的向量空间，那么U就称为V的子空间。

#### 1.34 子空间的条件

当且仅当V的子集U满足以下三个条件时，U是V的子空间。

加法恒等元(additive identity)

$$
0\in U\text{.}
$$

对于加法封闭(closed under addition)
$u, w\in U$意味着$u+w\in U$。

对于标量乘法封闭(closed under scalar multiplication)
$a\in F$且$u\in U$意味着$a u\in U$。

#### 1.36 定义：子空间的和( sum of subspaces)

假设$V_1,\ldots, V_m$是V的子空间。$V_1,\ldots, V_m$的和是由$V_1,\ldots, V_m$中元素所有可能的和所构成的集合，记作$V_1+\cdots+V_m$。更确切地说，

$$
V_1+\cdots+V_m=\left\{v_1+\cdots+v_m: v_1\in V_1,\ldots, v_m\in V_m\right\}.
$$

#### 1.40 子空间的和是包含这些子空间的最小子空间

假设$V_1,\ldots, V_m$是V的子空间，那么$V_1+\cdots+V_m$是最小的包含$V_1,\ldots, V_m$的子空间。

#### 1.41 定义：直和(direct sum)、

设$V_1,\ldots, V_m$是V的子空间。

如果$V_1+\cdots+V_m$中的每个元素都能用$v_1+\cdots+v_m$(其中各$v_k\in V_k$)这种形式唯一地表示出来，则称子空间之和$V_1+\cdots+V_m$为直和。

如果$V_1+\cdots+V_m$是直和，那么用$V_1\oplus\cdots\oplus V_m$来表示$V_1+\cdots+V_m$，其中记号$\oplus$表示此处的和是直和。

#### 1.45 直和的条件

假定$V_1,\ldots, V_m$是V的子空间。那么$n_1+\cdots+V_m$是直和，当且仅当用$v_1+\cdots+v_m$(其中各$v_k\in V_k$)表示0的唯一方式是将每个$v_k$都取0。

#### 1.46 两个子空间的直和

假定U和W是V的子空间。那么

$$
U+W\text{是直和}\Longleftrightarrow U\cap W=\{0\}.
$$
