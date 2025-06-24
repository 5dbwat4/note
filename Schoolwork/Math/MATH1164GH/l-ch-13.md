第十三章 函数列与函数项级数

§1 一致收敛性

设$f_{1},f_{2},\ldots,f_{n},\cdots$是一列定义在同一数集E上的函数，称为定义在E上的**函数列**.(1)也可简单地写作$\left\{ f_{n} \right\}$或$f_{n},n = 1,2,\cdots$

设$x_{0} \in E$,以$x_{0}$代入(1)可得数列$f_{1}\left( x_{0} \right),f_{2}\left( x_{0} \right),\cdots,f_{n}\left( x_{0} \right),\ldots$若数列(2)收敛，则称函数列(1)**在点**$\mathbf{x}_{\mathbf{0}}$**收敛**，$x_{0}$称为函数列(1)的**收敛点**.若数列(2)发散，则称函数列(1)**在点**$\mathbf{x}_{\mathbf{0}}$**发散**.若函数列(1)在数集$D \subset E$上每一点都收敛，则称(1)在**数集D上收敛**.这时对D上每一点x,都有数列$\left\{ f_{n}(x) \right\}$的一个极限值与之相对应，由这个对应法则所确定的D上的函数，称为函数列(1)的**极限函数**.若把此极限函数记作f,则有$\lim_{n \rightarrow \infty}f_{n}(x) = f(x),x \in D$

使函数列$\left\{ f_{n} \right\}$收敛的全体收敛点集合，称为函数列$\left\{ f_{n} \right\}$的**收敛域**.

定义1
设函数列$\left\{ f_{n} \right\}$与函数f定义在同一数集D上，若对任给的正数$\varepsilon$,总存在某一正整数N,使得当$n > N$时，对一切$x \in D$,都有$\left| f_{n}(x) - f(x) \right| < \varepsilon$

则称函数列$\left\{ f_{n} \right\}$在D上**一致收敛**于f,记作$f_{n}(x)\overset{\rightarrow}{\rightarrow}f(x)(n \rightarrow \infty),x \in D$

定理13.1(函数列一致收敛的柯西准则)
函数列$\left\{ f_{n} \right\}$在数集D上一致收敛的充要条件是：对任给正数$\varepsilon$,总存在正数N,使得当$n,m > N$时，对一切$x \in D$,都有$\left| f_{n}(x) - f_{m}(x) \right| < \varepsilon$

定理13.2
函数列$\left\{ f_{n} \right\}$在区间D上一致收敛于f的充要条件是：$\lim_{n \rightarrow \infty}\sup_{x \in D}\left| f_{n}(x) - f(x) \right| = 0$

推论
函数列$\left\{ f_{n} \right\}$在D上不一致收敛于f的充分且必要条件是：存在$\left\{ x_{n} \right\} \subset D$,使得$\left\{ f_{n}\left( x_{n} \right) - f\left( x_{n} \right) \right\}$不收敛于0

定义2
设函数列$\left\{ f_{n} \right\}$与f定义在区间I上，若对任意闭区间$\lbrack a,b\rbrack \subset I$,
$\left\{ f_{n} \right\}$在$\lbrack a,b\rbrack$上一致收敛于f,则称$\left\{ f_{n} \right\}$在I上**内闭一致收敛**于f

二、函数项级数及其一致收敛性

设 $\{ u_{n}(x)\}$ 是定义在数集 $E$ 上的一个函数列，表达式

$$u_{1}(x) + u_{2}(x) + \cdots + u_{n}(x) + \cdots,\quad x \in E$$

称为定义在 $E$ 上的**函数项级数**，简记为
$\sum_{n = 1}^{\infty}u_{n}(x)$ 或 $\sum u_{n}(x)$。称

$$S_{n}(x) = \sum_{k = 1}^{n}u_{k}(x),\quad x \in E,\quad n = 1,2,\cdots$$

为函数项级数(8)的**部分和函数列**。

若 $x_{0} \in E$，数项级数

$$u_{1}\left( x_{0} \right) + u_{2}\left( x_{0} \right) + \cdots + u_{n}\left( x_{0} \right) + \cdots$$

收敛，即部分和
$S_{n}\left( x_{0} \right) = \sum_{k = 1}^{n}u_{k}\left( x_{0} \right)$
当 $n \rightarrow \infty$ 时极限存在，则称级数(8)**在点**
$\mathbf{x}_{\mathbf{0}}$ **收敛**，$x_{0}$
称为级数(8)的**收敛点**。若级数(10)发散，则称级数(8)在**点**
$\mathbf{x}_{\mathbf{0}}$ **发散**。若级数(8)在 $E$ 的某个子集 $D$
上每点都收敛，则称级数(8)**在** $\mathbf{D}$ **上收敛**。若 $D$
为级数(8)全体收敛点的集合，这时则称 $D$ 为级数(8)的**收敛域**。级数(8)在
$D$ 上每一点 $x$ 与其所对应的数项级数(10)的和 $S(x)$ 构成一个定义在 $D$
上的函数，称为级数(8)的**和函数**，并写作

$$u_{1}(x) + u_{2}(x) + \cdots + u_{n}(x) + \cdots = S(x),\quad x \in D,$$

即

$$\lim_{n \rightarrow \infty}S_{n}(x) = S(x),\quad x \in D.$$

也就是说，函数项级数(8)的收敛性就是指它的部分和函数列(9)的收敛性。

定义3
设$\left\{ S_{n}(x) \right\}$是函数项级数$\Sigma u_{n}(x)$的部分和函数列.若$\left\{ S_{n}(x) \right\}$在数集D

上一致收敛于S(x),则称$\Sigma u_{n}(x)$在D上一致收敛于S(x).若$\Sigma u_{n}(x)$在任意闭区间

\[a,b\]CI上一致收敛，则称$\Sigma u_{n}(x)$在I上**内闭一致收敛**.

定理13.3(一致收敛的柯西准则) 函数项级数$\Sigma u_{n}(x)$在数集
D上一致收敛的

充要条件为：对任给的正数$\varepsilon$,总存在某正整数N,使得当n\>N时，对一切x∈D和一切

正整数p,都有 $\left| s_{n + p}(x) - s_{n}(x) \right| < \varepsilon$或
$\left| u_{n + 1}(x) + u_{n + 2}(x) + \ldots + u_{n + p}(x) \right| < \varepsilon$

此定理中当p=1时，得到函数项级数一致收敛的一个必要条件.

推论
函数项级数$\Sigma u_{n}(x)$在数集D上一致收敛的必要条件是函数列$\left\{ u_{n}(x) \right\}$在D上一致收敛于零.

设函数项级数$\Sigma u_{n}(x)$在D上的和函数为S(x),称$R_{n}(x) = S(x) - S_{n}(x)$为函数项级数$\Sigma u_{n}(x)$的**余项**.

定理13.4 函数项级数$\Sigma u_{n}(x)$在数集D上一致收敛于S(x)的充要条件是

$$\lim_{n \rightarrow \infty}\sup_{x \in D}\left| R_{n}(x) \right| = \lim_{n \rightarrow \infty}\sup_{x \in D}\left| S(x) - S_{n}(x) \right| = 0$$

三、函数项级数的一致收敛性判别法

定理13.5(魏尔斯特拉斯判别法)设函数项级数$\Sigma u_{n}(x)$定义在数集D上，$\Sigma M_{n}$

为收敛的正项级数，若对一切x∈D,有$\left| u_{n}(x) \right| \leq M_{n},n = 1,2,\ldots$则函数项级数$\Sigma u_{n}(x)$在D上一致收敛.

定理13.6(阿贝尔判别法)设

\(i\) $\Sigma u_{n}(x)$在区间I上一致收敛；

(ii)对于每一个$x \in I$,$\left\{ v_{n}(x) \right\}$是单调的；

\(iii\)
$\left\{ v_{n}(x) \right\}$在I上一致有界，即存在正数M,使得对一切$x \in I$和正整数n,有$\left| v_{n}(x) \right| \leq M$

则级数$\Sigma u_{n}(x)v_{n}(x)$在I上一致收敛.

定理13.7(狄利克雷判别法)设

\(i\)
$\Sigma u_{n}(x)$的部分和函数列$s_{n}(x) = \sum_{k = 1}^{n}{u_{k}(x)}$在I上一致有界；

\(ii\) 对于每一个$x \in I$,$\left\{ v_{n}(x) \right\}$是单调的；

(iii)在I上$v_{n}(x)\overset{\rightarrow}{\rightarrow}0(n \rightarrow \infty)$

则级数$\Sigma u_{n}(x)v_{n}(x)$在I上一致收敛.

§2 一致收敛函数列与函数项级数的性质

定理13.8
设函数列$\left\{ f_{n} \right\}$在$\left( a,x_{0} \right) \cup \left( x_{0},b \right)$上一致收敛于$f(x)$,且对每个n,
$\lim_{x \rightarrow x_{0}}f_{n}(x) = a_{n}$,则$\lim_{n \rightarrow \infty}a_{n}$和$\lim_{x \rightarrow x_{0}}f(x)$均存在且相等。

定理13.9(连续性)若函数列$\left\{ f_{n} \right\}$在区间$I$上一致收敛，且每一项都连续，则其极限函数f在$I$上也连续.

推论 若连续函数列子。在区间$I$上内闭一致收敛于f,则f在$I$上连续

定理13.10(可积性)
若函数列$\left\{ f_{n} \right\}$在\[a,b\]上一致收敛，且每一项都连续，则

$$\int_{a}^{b}{\lim_{n \rightarrow \infty}f_{n}(x)\mathbb{d}x} = \lim_{n \rightarrow \infty}\int_{a}^{b}{f_{n}(x)\mathbb{d}x}$$

定理13.11(可微性)设$\left\{ f_{n} \right\}$为定义在$\lbrack a,b\rbrack$上的函数列，若$x_{0} \in \lbrack a,b\rbrack$为f
的收敛点，$\left\{ f_{n} \right\}$的每一项在$\lbrack a,b\rbrack$上有连续的导数，且$\left\{ f_{n}^{'} \right\}$在$\lbrack a,b\rbrack$上一致收敛，则

$$\frac{\mathbb{d}}{\mathbb{d}x}\left( \lim_{n \rightarrow \infty}f_{n}(x) \right) = \lim_{n \rightarrow \infty}\frac{\mathbb{d}}{\mathbb{d}x}f_{n}(x)$$

推论
设函数列$\left\{ f_{n} \right\}$定义在区间$I$上，若$x_{0} \in I$为$\left\{ f_{n} \right\}$的收敛点，且$\left\{ f_{n}^{'} \right\}$在I上内闭一致收敛，则f在$I$上可导，且$f^{'}(x) = \lim_{n \rightarrow \infty}f_{n}^{'}(x)$

定理13.12(连续性)
若函数项级数$\Sigma u_{n}(x)$在区间$\lbrack a,b\rbrack$上一致收敛，且每一项都连续，则其和函数在$\lbrack a,b\rbrack$上也连续.

定理13.13(逐项求积)若函数项级数$\Sigma u_{n}(x)$在$\lbrack a,b\rbrack$上一致收敛，且每一项$u_{n}(x)$都连续，则

$$\Sigma\int_{a}^{b}{u_{n}(x)\mathbb{d}x} = \int_{a}^{b}{\Sigma u_{n}(x)\mathbb{d}x}$$

定理13.14(逐项求导)若函数项级数$\Sigma u_{n}(x)$在$\lbrack a,b\rbrack$上每一项都有连续的导函数，$x_{0} \in \lbrack a,b\rbrack$为$\Sigma u_{n}(x)$的收敛点，且$\Sigma u_{n}^{'}(x)$在$\lbrack a,b\rbrack$上一致收敛，则

$$\Sigma\left( \frac{\mathbb{d}}{\mathbb{d}x}u_{n}(x) \right) = \frac{\mathbb{d}}{\mathbb{d}x}\left( \Sigma u_{n}(x) \right)$$
