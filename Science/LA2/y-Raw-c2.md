### 2.1 记号：向量组

书写向量组时,我们通常不用圆括号括起来.

### 2.2 定义:线性组合(linear combination)

V中一个向量组  $v_1,\ldots, v_m$  的线性组合  ${}^2$  是形如


$$
 a_1 v_1+\cdots+a_m v_m
$$


的向量,其中  $a_1,\ldots, a_m\in F$  .

### 2.4 定义:张成空间(span)

V中向量组  $v_1,\ldots, v_m$  的所有线性组合所构成的集合称为  $v_1,\ldots, v_m$  的张成空间  ${}^3$  ,记作 $\operatorname{span}\left(v_1,\ldots, v_m\right)$  .换言之,


$$
\operatorname{span}\left(v_1,\ldots, v_m\right)=\left\{a_1 v_1+\cdots+ a_mv_m: a_1,\ldots, a_m\in F\right\}
$$
.

定义空向量组$(\,)$的张成空间为  $\{0\}$  .

### 2.6 向量组的张成空间是最小的包含组中所有向量的子空间

V中向量组的张成空间是最小的包含这向量组中所有向量的 V的子空间.

### 2.7 定义:张成(spans)

如果$\operatorname{span}\left(v_1,\ldots, v_m\right)$等于 V,我们就说$v_1,\ldots, v_m$张成$V$.

### 2.9 定义:有限维向量空间(finite-dimensional vector space)

如果一个向量空间可由其中某个向量组张成,则称该向量空间是有限维的.

### 2.10 定义:多项式(polynomial)、  $\mathcal{P}(F)$ 

- 对一个函数  $p: F\rightarrow F$  ,如果存在  $a_0,\ldots, a_m\in F$  使得对所有  $z\in F$  都有


$$
 p(z)=a_0+a_1 z+a_2 z^2+\cdots+a_m z^m,
$$


则称 p为系数在 F中的多项式.

- $\mathcal{P}(F)$  是系数在 F中的全体多项式所构成的集合.

### 2.11 定义:多项式的次数( degree of a polynomial)、  $\operatorname{deg} p$ 

- 对一个多项式  $p\in\mathcal{P}(F)$  ,如果存在  $a_0, a_1,\ldots, a_m\in F$  且  $a_m\neq 0$  使得对每个  $z\in F$  ,都有


$$
 p(z)=a_0+a_1 z+\cdots+a_m z^m,
$$


那么就说 $p$的次数是 $m$.

- 规定恒等于 $0$的多项式的次数为$-\infty$.

- 多项式 $p$的次数记为  $\operatorname{deg} p$  .

### 2.12 记号:  $\mathcal{P}_m(\mathbb{F})$ 

对于非负整数 $m$,  $\mathcal{P}_m(\mathbb{F})$  表示系数在 $\mathbb{F}$中且次数不高于 $m$的所有多项式所构成的集合.

### 2.13 定义:无限维向量空间(infinite-dimensional vector space)

如果一个向量空间不是有限维的,就称它是无限维的.

### 2.15 定义:线性无关(linearly independent)

- 对于 V中的一个向量组  $v_1,\ldots, v_m$  ,如果使得


$$
 a_1 v_1+\cdots+a_m v_m=0
$$


成立的  $a_1,\ldots, a_m\in F$  的唯一选取方式是  $a_1=\cdots=a_m=0$  ,那么称该向量组为线性无关的.

- 规定空向量组$( \,)$也是线性无关的.

### 2.17 定义:线性相关(linearly dependent)

- 如果 V中的一个向量组不是线性无关的,就称它是线性相关的.

- 换言之,对于 V中的向量组  $v_1,\ldots, v_m$  ,如果存在不全为 0的  $a_1,\ldots, a_m\in F$  使得

 $a_1 v_1+\cdots+a_m v_m=0$  ,那么该向量组是线性相关的.

### 2.19 线性相关性引理(linear dependence lemma)

设  $v_1,\ldots, v_m$  是 V中的一个线性相关组.那么存在  $k\in\{1,2,\ldots, m\}$  满足


$$
 v_k\in\operatorname{span}\left(v_1,\ldots, v_{k-1}\right).
$$


进而,如果 k满足上述条件且从  $v_1,\ldots, v_m$  中移除第 k项,那么剩余向量组成的向量组的张成空间仍等于  $\operatorname{span}\left(v_1,\ldots, v_m\right)$  .

### 2.22 线性无关组的长度  $\leq$  张成组的长度

在有限维向量空间中,每个线性无关向量组的长度小于或等于每个张成向量组的长度.

### 2.25 有限维的子空间

有限维向量空间的每个子空间都是有限维的.

### 2.26 定义:基( basis)

V的一个基是 V中一个线性无关且张成 V的向量组.

### 2.28 基的判定准则

V中一个向量组  $v_1,\ldots, v_n$  是 V的基,当且仅当每个  $v\in V$  都可以被唯一地写成这样的形式:


$$
 v=a_1 v_1+\cdots+a_n v_n,\qquad(2.29)
$$


其中  $a_1,\ldots, a_n\in F$  .

### 2.30 每个张成组都包含一个基

向量空间中的每个张成组都能被削减成该向量空间的一个基.

### 2.31 有限维向量空间的基

每个有限维向量空间都有基.

### 2.32 每个线性无关组都可被扩充成一个基

有限维向量空间中每个线性无关向量组都可被扩充成该向量空间的一个基.

### 2.33 V的每个子空间都是等于 V的直和的组成部分

假设 V是有限维的, U是 V的子空间.那么存在 V的一个子空间 W,使得  $V=U\oplus W$  .

### 2.34 基的长度不依赖于基的选取

一个有限维向量空间中的任意两个基都有相同的长度.

### 2.35 定义:维数(dimension)、  $\operatorname{dim} V$ 

- 一个有限维向量空间的维数是这个向量空间中任意一个基的长度.

- 一个有限维向量空间 V的维数记作  $\operatorname{dim} V$  .

### 2.37 子空间的维数

如果 V是有限维的且 U是 V的一个子空间,那么  $\operatorname{dim} U\leq\operatorname{dim} V$  .

### 2.38 长度恰当的线性无关组是一个基

假设 V是有限维的.那么 V中每个长度为 dim V的线性无关向量组都是 V的一个基.

### 2.39 某空间中与之维数相同的子空间等于这整个空间

假设 V是有限维的, U是 V的子空间且满足  $\operatorname{dim} U=\operatorname{dim} V$  .那么  $U=V$  .

### 2.42 长度恰当的张成组是一个基

假设 V是有限维的.那么 V中每个长度为  $\operatorname{dim} V$  的张成组都是 V的一个基.

### 2.43 子空间之和的维数

如果  $V_1$  和  $V_2$  是一个有限维向量空间的子空间,那么


$$
\operatorname{dim}\left(V_1+V_2\right)=\operatorname{dim} V_1+\operatorname{dim} V_2-\operatorname{dim}\left(V_1\cap V_2\right).
$$
