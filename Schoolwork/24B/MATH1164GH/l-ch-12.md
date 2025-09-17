第十二章 数项级数

§1 级数的敛散性

定义1
给定一个数列$\left\{ u_{n} \right\}$,对它的各项依次用"+"号连接起来的表达式

$$u_{I} + u_{2} + \ldots + u_{n} + \ldots$$

称为常数项**无穷级数**或**数项级数**(也常简称级数),其中$u_{n}$称为数项级数(1)的通项或一般项.

数项级数(1)也常写作$\sum_{n = 1}^{\infty}u_{n}$或简单写作$\Sigma u_{n}$

数项级数(1)的前$n$项之和，记为

$$S_{n} = \sum_{k = 1}^{n}u_{k} = u_{1} + u_{2} + \cdots + u_{n}$$

称它为数项级数(1)的**第**$\mathbf{n}$**个部分和**，也简称**部分和**.

定义2 若数项级数(1)的部分和数列$\left\{ S_{n} \right\}$收敛于$S$
(即$\lim_{n \rightarrow \infty}S_{n} = S$),则称数项级数(1)收敛，称S为数项级数(1)的和，记作$S = u_{1} + u_{2} + \ldots + u_{n} + \ldots$或$S = \Sigma u_{n}$

若$\left\{ S_{n} \right\}$是发散数列，则称数项级数(1)发散

定理12.1(级数收敛的柯西准则)级数(1)收敛的充要条件是：任给正数$\varepsilon$,总存

在正整数$N$,使得当$m > N$以及对任意的正整数p,都有

$$\left| u_{m + 1} + u_{m + 2} + \ldots + u_{m + p} \right| < \varepsilon$$

根据定理12.1,我们立刻可写出级数(1)发散的充要条件：存在某正数$\varepsilon_{0}$,对任何

正整数$N$,总存在正整数$m_{0}$ ($> N$)和$p_{0}$,有

$$\left| u_{m_{0} + 1} + u_{m_{0} + 2} + \ldots + u_{m_{0} + p_{0}} \right| \geq \varepsilon_{0}$$

定理12.2
若级数$\Sigma u_{n}$与$\Sigma v_{n}$都收敛，则对任意常数c,d,级数$\Sigma\left( cu_{n} + \mathbb{d}v_{n} \right)$亦收

敛，且$\Sigma\left( cu_{n} + \mathbb{d}v_{n} \right) = c\Sigma u_{n} + d\Sigma v_{n}$

定理12.3 去掉、增加或改变级数的有限个项并不改变级数的敛散性

定理12.4
在收敛级数的项中任意加括号，既不改变级数的收敛性，也不改变它的和.

§2 正项级数

若数项级数各项的符号都相同，则称它为**同号级数**.对于同号级数，只需研究各项

都是由非负数组成的级数------称为**正项级数**.

定理12.5
正项级数$\Sigma u_{n}$收敛的充要条件是：部分和数列$\left\{ S_{n} \right\}$有界，即存在某正数$M$,对一切正整数$n$有$S_{n} < M$.

定理12.6(比较原则)设$\Sigma u_{n}$和$\Sigma v_{n}$是两个正项级数，如果存在某正数$N$,对一切$n > N$都有$u_{n} \leq v_{n}$则

(i)若级数$\Sigma v_{n}$收敛，则级数$\Sigma u_{n}$也收敛；

(ii)若级数$\Sigma u_{n}$发散，则级数$\Sigma v_{n}$也发散.

推论 设

\(3\) $u_{1} + u_{2} + \ldots + u_{n} + \ldots$

\(4\) $v_{1} + v_{2} + \ldots + v_{n} + \ldots$

是两个正项级数，若$\lim_{n \rightarrow \infty}\frac{u_{n}}{v_{n}} = l$则

(i)当$0 < l < + \infty$时，级数(3)、(4)同时收敛或同时发散；

(ii)当$l = 0$且级数(4)收敛时，级数(3)也收敛；

(iii)当$l = + \infty$且级数(4)发散时，级数(3)也发散.

定理12.7(达朗贝尔判别法，或称比式判别法)设$\Sigma u_{n}$为正项级数，且存在某正整数$N_{0}$及常数$q(0 < q < 1)$.

(i)若对一切$n > N_{0}$,成立不等式$\frac{u_{n + 1}}{u_{n}} \leq q$则级数$\Sigma u_{n}$收敛.

(ii)若对一切$n > N_{0}$,成立不等式$\frac{u_{n + 1}}{u_{n}} \geq 1$则级数$\Sigma u_{n}$发散.

推论1(比式判别法的极限形式)若$\Sigma u_{n}$为正项级数，且$\lim_{n \rightarrow \infty}\frac{u_{n} + 1}{u_{n}} = q$则

(i)当$q < 1$时，级数$\Sigma u_{n}$收敛；

(ii)当$q > 1$或$q = + \infty$时，级数$\Sigma u_{n}$发散.

定理12.8(柯西判别法，或称根式判别法)设$\Sigma u_{n}$为正项级数，且存在某正数$N_{0}$
及正常数$l$,

(i)若对一切$n > N_{0}$,成立不等式$\sqrt[n]{u_{n}} \leq l < 1$则级数$\Sigma u_{n}$收敛；

(ii)若对一切$n > N_{0}$,成立不等式$\sqrt[n]{u_{n}} \geq 1$则级数$\Sigma u_{n}$发散.

推论1(根式判别法的极限形式)设$\Sigma u_{n}$为正项级数，且$\lim_{n \rightarrow \infty}\sqrt[n]{u_{n}} = l$则

(i)当$l < 1$时，级数$\Sigma u_{n}$收敛；

(ii)当$l > 1$时，级数$\Sigma u_{n}$发散\
($l = 1$时进一步判定e.g.$\Sigma\frac{1}{n}$)

（根式判别法适用更多）

定理12.9
设$f$为$\lbrack 1, + \infty)$上的减函数，则级数$\sum_{n = 1}^{\infty}{f(n)}$收敛的充分必要条件是反常积分$\int_{1}^{+ \infty}{f(x)\mathbb{d}x}$收敛。

(设$f$为$\lbrack 1, + \infty)$上的减函数，则级数$\sum_{n = 1}^{\infty}{f(n)}$与反常积分$\int_{1}^{+ \infty}{f(x)\mathbb{d}x}$同敛散。)

§3 一般项级数

一、交错级数

若级数的各项符号正负相间，即$u_{1} - u_{2} + u_{3} - u_{4} + \ldots + ( - 1)^{n + 1}u_{n} + \ldots$（$u_{n} > 0,n = 1,2,\ldots$）则称(1)为**交错级数**.

定理12.11(莱布尼茨判别法)若交错级数(1)满足下述两个条件：

(i)数列$\left\{ u_{n} \right\}$单调递减；

(ii)$\lim_{n \rightarrow \infty}u_{n} = 0$

则级数(1)收敛.

二、绝对收敛级数及其性质

若级数(5)各项绝对值所组成的级数$\left| u_{1} \right| + \left| u_{2} \right| + \left| u_{3} \right| + \ldots + \left| u_{n} \right| + \ldots$(6)收敛，则称原级数(5)为**绝对收敛级数**.
若级数(5)收敛，但级数(6)不收敛，则称级数(5)为**条件收敛级数**。

定理12.12 绝对收敛级数一定收敛.

1.级数的重排

定理12.13
设级数(5)绝对收敛，且其和等于S,则任意重排后所得到的级数(7)也绝对收敛，且有相同的和数

2.级数的乘积

定理12.14(柯西定理)若级数(11)、(12)都绝对收敛，则对(13)中所有乘积$u_{i}v_{j}$按任意顺序排列所得到的级数$\Sigma w_{n}$也绝对收敛，且其和等于$AB$.

引理(分部求和公式，也称阿贝尔变换)设$\varepsilon_{i},v_{i}$($\mathbb{i} = 1,2,\ldots,n$)为两组实数，

若令$\sigma_{k} = v_{1} + v_{2} + v_{3 + \ldots} + v_{k}(k = 1,2,\ldots,n)$

则有如下分部求和公式成立：$\sum_{j = 1}^{n}{\varepsilon_{1}v_{i}} = \left( \varepsilon_{1} - \varepsilon_{2} \right)\sigma_{1} + \left( \varepsilon_{2} - \varepsilon_{3} \right)\sigma_{2} + \cdots + \left( \varepsilon_{n - 1} - \varepsilon_{n} \right)\sigma_{n - 1} + \varepsilon_{n}\sigma_{n}$

推论(阿贝尔引理)若

(i)$\varepsilon_{1},\varepsilon_{2},\ldots,\varepsilon_{n}$是单调数组；

(ii)对任一正整数$k(1 \leq k \leq n)$有$\left| \sigma_{k} \right| \leq A$
(这里$\sigma_{k} = v_{1} + \ldots + v_{k}$),则记$\varepsilon = \max_{k}\left\{ \left| \varepsilon_{k} \right| \right\}$有$\left| \sum_{k = 1}^{n}{\varepsilon_{k}v_{k}} \right| \leq 3\varepsilon A$

定理12.15(阿贝尔判别法)若$\left\{ a_{n} \right\}$为单调有界数列，且级数$\Sigma b_{n}$收敛，则级数$\Sigma a_{n}b_{n}$收敛.

定理12.16(狄利克雷判别法)若数列$\left\{ a_{n} \right\}$单调递减，且$\lim_{n \rightarrow \infty}a_{n} = 0$又级数$\Sigma b_{n}$的部分和数列有界，则级数$\Sigma a_{n}b_{n}$收敛.
