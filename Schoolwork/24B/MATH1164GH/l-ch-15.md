## 一、三角级数·正交函数系

在科学实验与工程技术的某些现象中，常会碰到一种周期运动。最简单的周期运动，可用正弦函数$y = A\sin(\omega x + \varphi)$
(1)来描写。由(1)所表达的周期运动也称为**简谐振动**，其中$A$为**振幅**，$\varphi$为**初相角**，$\omega$为**角频率**，于是简谐振动$y$的**周期**是$T = \frac{2\pi}{\omega}$。较为复杂的周期运动，则常是几个简谐振动$y_{k} = A_{k}\sin\left( k\omega x + \varphi_{k} \right),\quad k = 1,2,\cdots,n$的叠加


$$
\begin{array}{r}
y = \sum_{k = 1}^{n}y_{k} = \sum_{k = 1}^{n}A_{k}\sin\left( k\omega x + \varphi_{k} \right).\tag{2}
\end{array}
$$


由于简谐振动$y_{k}$的周期为$\frac{T}{k}\left( T = \frac{2\pi}{\omega} \right),k = 1,2,\cdots,n$，所以函数(2)的周期为$T$。对无穷多个简谐振动进行叠加就得到函数项级数


$$
\begin{array}{r}
A_{0} + \sum_{n = 1}^{\infty}A_{n}\sin\left( n\omega x + \varphi_{n} \right).\tag{3}
\end{array}
$$


若级数(3)收敛，则它所描述的是更为一般的周期运动现象。对于级数(3)，我们只要讨论$\omega = 1$（如果$\omega \neq 1$，可用$\omega x$代换$x$）的情形。由于$\sin\left( nx + \varphi_{n} \right) = sin\varphi_{n}\cos nx + cos\varphi_{n}\sin nx,$所以


$$
A_{0} + \sum_{n = 1}^{\infty}A_{n}\sin\left( nx + \varphi_{n} \right)
$$



$$
= A_{0} + \sum_{n = 1}^{\infty}\left( A_{n}\sin\varphi_{n}\cos nx + A_{n}\cos\varphi_{n}\sin nx \right).
$$


(3')

记$A_{0} = \frac{a_{0}}{2},\quad A_{n}\sin\varphi_{n} = a_{n},\quad A_{n}\cos\varphi_{n} = b_{n},\quad n = 1,2,\cdots$,则级数(3')可写成


$$
\begin{array}{r}
\frac{a_{0}}{2} + \sum_{n = 1}^{\infty}\left( a_{n}\cos nx + b_{n}\sin nx \right).\#
\end{array}(4)
$$


它是由**三角函数列**（也称为**三角函数系**）


$$
\begin{array}{r}
1,cosx,sinx,cos2x,sin2x,\cdots,cosnx,sinnx,\cdots\#(5)
\end{array}
$$


所产生的一般形式的**三角级数**。

容易验证，若三角级数(4)收敛，则它的和一定是一个以$2\pi$为周期的函数。

关于三角级数(4)的收敛性有如下定理：

**定理 15.1** 若级数


$$
\frac{\left| a_{0} \right|}{2} + \sum_{n = 1}^{\infty}\left( \left| a_{n} \right| + \left| b_{n} \right| \right)
$$


收敛，则级数(4)在整个数轴上绝对收敛且一致收敛。

**定理15.2**若在整个数轴上


$$
f(x) = \frac{a_{0}}{2} + \sum_{n = 1}^{\infty}\left( a_{n}\cos nx + b_{n}\sin nx \right)

$$
且等式右边级数一致收敛，则有如下关系式：


$$
a_{n} = \frac{1}{\pi}\int_{- \pi}^{\pi}f(x)\cos nx\, dx,\quad n = 0,1,2,\ldots
$$



$$
b_{n} = \frac{1}{\pi}\int_{- \pi}^{\pi}f(x)\sin nx\, dx,\quad n = 1,2,\ldots
$$


一般地说，若$f$是以$2\pi$为周期且在$\lbrack - \pi,\pi\rbrack$上可积的函数，则按公式(10)计算出的
$a_{n}$和$b_{n}$称为函数$f$（关于三角函数系）的傅里叶系数，以$f$的傅里叶系数为系数的三角级数（9）称为$f$（关于三角函数系）的**傅里叶级数**，记作


$$
f(x)\sim\frac{a_{0}}{2} + \sum_{n = 1}^{\infty}\left( a_{n}\cos nx + b_{n}\sin nx \right).\tag{12}
$$


**定理15.3（傅里叶级数收敛定理）​**设以$2\pi$为周期的函数$f$在区间$\lbrack - \pi,\pi\rbrack$上按段光滑，则在每一点$x \in \lbrack - \pi,\pi\rbrack$，$f$的傅里叶级数（12）收敛于$f$在点$x$的左、右极限的算术平均值，即


$$
\frac{f(x + 0) + f(x - 0)}{2} = \frac{a_{0}}{2} + \sum_{n = 1}^{\infty}\left( a_{n}\cos(nx) + b_{n}\sin(nx) \right),
$$


其中$a_{n}$和$b_{n}$是$f$的傅里叶系数。

我们知道，若$f$的导函数在$\lbrack a,b\rbrack$上连续，则称$f$在$\lbrack a,b\rbrack$上**光滑**。但若定义在$\lbrack a,b\rbrack$上除了至多有有限个第一类间断点的函数$f$的导函数在$\lbrack a,b\rbrack$上除了至多有限个点外都存在且连续，在这有限个点上导函数$f'$的左、右极限存在，则称$f$在$\lbrack a,b\rbrack$上**按段光滑**。

根据上述定义，若函数$f$在$\lbrack a,b\rbrack$上按段光滑，则有如下重要性质：

1°$f$在$\lbrack a,b\rbrack$上可积。

2° 在$\lbrack a,b\rbrack$上每一点都存在$f'(x \pm 0)$，且有


$$
\lim_{t \rightarrow 0^{+}}\frac{f(x + t) - f(x + 0)}{t} = f'(x + 0),
$$



$$
\lim_{t \rightarrow 0^{+}}\frac{f(x - t) - f(x - 0)}{- t} = f'(x - 0).
$$


3°
补充定义$f'$在$\lbrack a,b\rbrack$上那些至多有有限个不存在点上的值后（仍记为$f'$），$f'$在$\lbrack a,b\rbrack$上可积。

推论
若$f$是以$2\pi$为周期的连续函数，且在$\lbrack - \pi,\pi\rbrack$上按段光滑，则$f$的傅里叶级数在$( - \infty, + \infty)$上收敛于$f$。

预备定理 1（贝塞尔（Bessel）不等式）
若函数$f$在$\lbrack - \pi,\pi\rbrack$上可积，则


$$
\frac{a_{0}^{2}}{2} + \sum_{n = 1}^{\infty}\left( a_{n}^{2} + b_{n}^{2} \right) \leq \frac{1}{\pi}\int_{- \pi}^{\pi}f^{2}(x)\, dx,
$$


其中$a_{n},b_{n}$为$f$的傅里叶系数。（1）式称为**贝塞尔不等式**。

推论 1 若$f$为可积函数，则


$$
\lim_{n \rightarrow \infty}\int_{- \pi}^{\pi}f(x)\cos nx\, dx = 0,
$$



$$
\lim_{n \rightarrow \infty}\int_{- \pi}^{\pi}f(x)\sin nx\, dx = 0.
$$


因为(1)式的左边级数收敛，所以当$n \rightarrow \infty$时，通项$a_{n}^{2} + b_{n}^{2} \rightarrow 0$，亦即有$a_{n} \rightarrow 0$与$b_{n} \rightarrow 0$，这就是(5)式。这个推论也称为**黎曼-勒贝格定理**。

推论 2 若$f$为可积函数，则


$$
\lim_{n \rightarrow \infty}\int_{0}^{\pi}f(x)\sin\left( n + \frac{1}{2} \right)x\, dx = 0,
$$



$$
\lim_{n \rightarrow \infty}\int_{- \pi}^{0}f(x)\sin\left( n + \frac{1}{2} \right)x\, dx = 0.
$$


预备定理 2
若$f(x)$是以$2\pi$为周期的函数，且在$\lbrack - \pi,\pi\rbrack$上可积，则它的傅里叶级数部分和$S_{n}(x)$可写成


$$
S_{n}(x) = \frac{1}{\pi}\int_{- \pi}^{\pi}f(x + t)\frac{\sin\left( n + \frac{1}{2} \right)t}{2\sin\frac{t}{2}}\, dt,
$$


当$t = 0$时，被积函数中的不定式由极限


$$
\lim_{t \rightarrow 0}\frac{\sin\left( n + \frac{1}{2} \right)t}{2\sin\frac{t}{2}} = n + \frac{1}{2}
$$


来确定。
