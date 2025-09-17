# 第十九章 含参量积分

## §1 含参量正常积分

从本章开始我们讨论多元函数的各种积分问题，首先研究含参量积分。设$f(x,y)$是定义在矩形区域$R=[a,b]\times[c,d]$上的二元函数。当$x$取$[a,b]$上某定值时，函数$f(x,y)$则是定义在$[c,d]$上以$y$为自变量的一元函数。倘若这时$f(x,y)$在$[c,d]$上可积，则其积分值是$x$在$[a,b]$上取值的函数，记它为$\varphi(x)$，就有

$$
\varphi(x) = \int_c^d f(x,y) \, dy, \quad x \in [a,b]. \tag{1}
$$ 
一般地，设$f(x,y)$为定义在区域$G=\{(x,y) \mid c(x) \leq y \leq d(x), a \leq x \leq b\}$上的二元函数，其中$c(x),d(x)$为定义在$[a,b]$上的连续函数（图19-1），若对于$[a,b]$上每一固定的$x$值，$f(x,y)$作为$y$的函数在闭区间$[c(x),d(x)]$上可积，则其积分值是$x$在$[a,b]$上取值的函数，记作$F(x)$时，就有

$$
F(x) = \int_{c(x)}^{d(x)} f(x,y) \, dy, \quad x \in [a,b]. \tag{2}
$$ 

用积分形式所定义的这两个函数(1)与(2)，通称为定义在$[a,b]$上**含参量$x$的（正常）积分**，或简称**含参量积分**。

**定理19.1（连续性）** 若二元函数$f(x,y)$在矩形区域$R=[a,b]\times[c,d]$上连续，则函数

$$
\varphi(x) = \int_c^d f(x,y) \, dy
$$

在$[a,b]$上连续。

**定理19.2（连续性）** 设二元函数$f(x,y)$在区域

$$
G = \{(x,y) \mid c(x) \leq y \leq d(x), a \leq x \leq b\}
$$

上连续，其中$c(x),d(x)$为$[a,b]$上的连续函数，则函数

$$
F(x) = \int_{c(x)}^{d(x)} f(x,y) \, dy \tag{6}
$$

在$[a,b]$上连续。

**定理19.3（可微性）** 若函数$f(x,y)$与其偏导数$\frac{\partial}{\partial x} f(x,y)$都在矩形区域$R=[a,b]\times[c,d]$上连续，则

$$
\varphi(x) = \int_c^d f(x,y) \, dy
$$

在$[a,b]$上可微，且

$$
\frac{d}{dx} \int_c^d f(x,y) \, dy = \int_c^d \frac{\partial}{\partial x} f(x,y) \, dy.
$$

**定理19.4（可微性）** 设$f(x,y), f_x(x,y)$在$R=[a,b]\times[p,q]$上连续，$c(x),d(x)$为定义在$[a,b]$上其值含于$[p,q]$内的可微函数，则函数

$$
F(x) = \int_{c(x)}^{d(x)} f(x,y) \, dy
$$

在$[a,b]$上可微，且

$$
F'(x) = \int_{c(x)}^{d(x)} f_x(x,y) \, dy + f(x,d(x))d'(x) - f(x,c(x))c'(x). \tag{7}
$$

**定理19.5（可积性）** 若$f(x,y)$在矩形区域$R=[a,b]\times[c,d]$上连续，则$\varphi(x)$和$\psi(y)$分别在$[a,b]$和$[c,d]$上可积。

这就是说：在$f(x,y)$连续性假设下，同时存在两个求积顺序不同的积分：

$$
\int_a^b \left[ \int_c^d f(x,y) \, dy \right] dx \quad \text{与} \quad \int_c^d \left[ \int_a^b f(x,y) \, dx \right] dy.
$$

为书写简便起见，今后将上述两个积分写作

$$
\int_a^b dx \int_c^d f(x,y) \, dy \quad \text{与} \quad \int_c^d dy \int_a^b f(x,y) \, dx,
$$

前者表示$f(x,y)$先对$y$求积然后对$x$求积，后者则求积顺序相反。它们统称为**累次积分**，或更确切地称为**二次积分**。


**定理19.6** (在$f(x,y)$连续性假设下，累次积分与求积顺序无关) 若$f(x,y)$在矩形区域$R=[a,b]\times[c,d]$上连续，则

$$
\int_a^b dx \int_c^d f(x,y) \, dy = \int_c^d dy \int_a^b f(x,y) \, dx. \tag{8}
$$

## §2 含参量反常积分

### 一、一致收敛性及其判别法

设函数$f(x,y)$定义在无界区域$R=\{(x,y) \mid x \in I, c \leq y < +\infty\}$上，其中$I$为一区间，若对每一个固定的$x \in I$，反常积分

$$
\int_c^{+\infty} f(x,y) \, dy \tag{1}
$$

都收敛，则它的值是$x$在$I$上取值的函数，当记这个函数为$\Phi(x)$时，则有

$$
\Phi(x) = \int_c^{+\infty} f(x,y) \, dy, \quad x \in I, \tag{2}
$$

称(1)式为定义在$I$上的**含参量$x$的无穷限反常积分**，或简称**含参量反常积分**。

**定义1** 若含参量反常积分(1)与函数$\Phi(x)$对任给的正数$\varepsilon$，总存在某一实数$N > c$，使得当$M > N$时，对一切$x \in I$，都有

$$
\left| \int_c^M f(x,y) \, dy - \Phi(x) \right| < \varepsilon,
$$

即

$$
\left| \int_M^{+\infty} f(x,y) \, dy \right| < \varepsilon,
$$

则称含参量反常积分(1)在$I$上一致收敛于$\Phi(x)$，或简单地说含参量反常积分(1)在$I$上一致收敛。

**定理19.7（一致收敛的柯西准则）** 含参量反常积分(1)在$I$上一致收敛的充要条件是：对任给正数$\varepsilon$，总存在某一实数$M > c$，使得当$A_1, A_2 > M$时，对一切$x \in I$，都有

$$
\left| \int_{A_1}^{A_2} f(x,y) \, dy \right| < \varepsilon. \tag{3}
$$


**定理19.8** 含参量反常积分$\int_c^{+\infty} f(x,y) \, dy$在$I$上一致收敛的充分必要条件是

$$
\lim_{A \to +\infty} F(A) = 0,
$$

其中$F(A) = \sup_{x \in I} \left| \int_A^{+\infty} f(x,y) \, dy \right|$。

**定理19.9** 含参量反常积分(1)在$I$上一致收敛的充要条件是：对任一趋于$+\infty$的递增数列$\{A_n\}$（其中$A_1=c$），函数项级数

$$
\sum_{n=1}^{\infty} \int_{A_n}^{A_{n+1}} f(x,y) \, dy = \sum_{n=1}^{\infty} u_n(x) \tag{6}
$$

在$I$上一致收敛。

**魏尔斯特拉斯$M$判别法** 设有函数$g(y)$，使得

$$
|f(x,y)| \leq g(y), \quad (x,y) \in I \times [c, +\infty).
$$

若$\int_c^{+\infty} g(y) \, dy$收敛，则$\int_c^{+\infty} f(x,y) \, dy$在$I$上一致收敛。

**狄利克雷判别法** 设

(i) 对一切实数$N > c$，含参量正常积分

$$
\int_c^N f(x,y) \, dy
$$

对参量$x$在$I$上一致有界，即存在正数$M$，对一切实数$N > c$及一切$x \in I$，都有

$$
\left| \int_c^N f(x,y) \, dy \right| \leq M.
$$

(ii) 对每一个$x \in I$，函数$g(x,y)$为$y$的单调函数，且当$y \to +\infty$时，对参量$x$，$g(x,y)$一致地收敛于0.

则含参量反常积分

$$
\int_c^{+\infty} f(x,y)g(x,y) \, dy
$$

在$I$上一致收敛。

**阿贝尔判别法** 设

(i) $\int_c^{+\infty} f(x,y) \, dy$在$I$上一致收敛。

(ii) 对每一个$x \in I$，函数$g(x,y)$为$y$的单调函数，且对参量$x$，$g(x,y)$在$I$上一致有界。

则含参量反常积分

$$
\int_c^{+\infty} f(x,y)g(x,y) \, dy
$$

在$I$上一致收敛。

### 二、含参量反常积分的性质

**定理19.10（连续性）** 设$f(x,y)$在$I \times [c, +\infty)$上连续，若含参量反常积分

$$
\Phi(x) = \int_c^{+\infty} f(x,y) \, dy \tag{12}
$$

在$I$上一致收敛，则$\Phi(x)$在$I$上连续。

**定理19.11（可微性）** 设$f(x,y)$与$f_x(x,y)$在区域$I \times [c, +\infty)$上连续。若

$$
\Phi(x) = \int_c^{+\infty} f(x,y) \, dy
$$

在$I$上收敛，$\int_c^{+\infty} f_x(x,y) \, dy$在$I$上一致收敛，则$\Phi(x)$在$I$上可微，且

$$
\Phi'(x) = \int_c^{+\infty} f_x(x,y) \, dy. \tag{15}
$$

推论 设$f(x,y)$和$f_x(x,y)$在$I \times [c, +\infty)$上连续，若$\Phi(x) = \int_c^{+\infty} f(x,y) \, dy$在$I$上收敛，而$\int_c^{+\infty} f_x(x,y) \, dy$在$I$上内闭一致收敛，则$\Phi(x)$在$I$上可微，且$\Phi'(x) = \int_c^{+\infty} f_x(x,y) \, dy$。

最后结果表明在定理条件下，求导运算和无穷积分运算可以交换。

**定理19.12（可积性）** 设$f(x,y)$在$[a,b] \times [c, +\infty)$上连续，若$\Phi(x) = \int_c^{+\infty} f(x,y) \, dy$在$[a,b]$上一致收敛，则$\Phi(x)$在$[a,b]$上可积，且

$$
\int_a^b dx \int_c^{+\infty} f(x,y) \, dy = \int_c^{+\infty} dy \int_a^b f(x,y) \, dx. \tag{16}
$$

**定理19.13** 设$f(x,y)$在$[a, +\infty) \times [c, +\infty)$上连续。若

(i) $\int_a^{+\infty} f(x,y) \, dx$关于$y$在$[c, +\infty)$上内闭一致收敛，$\int_c^{+\infty} f(x,y) \, dy$关于$x$在$[a, +\infty)$上内闭一致收敛。

(ii) 积分

$$
\int_a^{+\infty} dx \int_c^{+\infty} |f(x,y)| \, dy \quad \text{与} \quad \int_c^{+\infty} dy \int_a^{+\infty} |f(x,y)| \, dx \tag{18}
$$

中有一个收敛。

则

$$
\int_a^{+\infty} dx \int_c^{+\infty} f(x,y) \, dy = \int_c^{+\infty} dy \int_a^{+\infty} f(x,y) \, dx. \tag{19}
$$

设$f(x,y)$在区域$R=[a,b] \times [c,d]$上有定义。若对$x$的某些值，$y=d$为函数$f(x,y)$的瑕点，则称

$$
\int_c^d f(x,y) \, dy \tag{25}
$$

为含参量$x$的无界函数反常积分，或简称为含参量反常积分。若对每一个$x \in [a,b]$，积分(25)都收敛，则其积分值是$x$在$[a,b]$上取值的函数，含参量反常积分(25)在$[a,b]$上一致收敛的定义如下。

**定义2** 对任给正数$\varepsilon$，总存在某正数$\delta < d-c$，使得当$0 < \eta < \delta$时，对一切$x \in [a,b]$，都有

$$
\left| \int_{d-\eta}^d f(x,y) \, dy \right| < \varepsilon,
$$

则称含参量反常积分(25)在$[a,b]$上一致收敛。

## §3 欧拉积分

含参量积分

$$
\Gamma(s) = \int_0^{+\infty} x^{s-1} e^{-x} dx, \quad s > 0, \tag{1}
$$

$$
B(p,q) = \int_0^1 x^{p-1}(1-x)^{q-1} dx, \quad p > 0, \, q > 0 \tag{2}
$$

在应用中经常出现，它们统称为欧拉积分，其中前者又称为**伽马(Gamma)函数**（或写作$\Gamma$函数），后者称为**贝塔(Beta)函数**（或写作B函数）。下面我们分别讨论这两个函数的性质。

### $\Gamma$函数

1. $\Gamma(s)$在定义域$s>0$上连续且可导
2. 递推公式$\Gamma(s+1)=s\Gamma(s)$


### B函数

1. $B(p,q)$在定义域$p>0,q>0$内连续
2. 对称性：$B(p,q)=B(q,p)$
3. 递推公式

$$
B(p,q) = \frac{q-1}{p+q-1} B(p,q-1) \quad (p > 0, q > 1), \tag{9}
$$

$$
B(p,q) = \frac{p-1}{p+q-1} B(p-1,q) \quad (p > 1, q > 0), \tag{10}
$$

$$
B(p,q) = \frac{(p-1)(q-1)}{(p+q-1)(p+q-2)} B(p-1,q-1) \quad (p > 1, q > 1).
$$