---
title: 定理&定义列表
---

定义1 设S为R中的一个数集.若存在数
M(L),使得对一切x∈S,都有x≤M(x≥L),则称S为有上界(下界)的数集，数
M(L)称为S的一个上界(下界).

若数集S既有上界又有下界，则称S为有界集.若S不是有界集，则称S为无界集.

定义2 设S是R中的一个数集.若数η满足：

(i)对一切 x∈S,有x≤η,即 η是S的上界；

(ii)对任何α\<η,存在x0∈S,使得x0\>α,即η又是S的最小上界，

则称数η为数集S的上确界，记作η=sup s

定理1.1(确界原理)设S为非空数集.若S有上界，则S必有上确界；若S有下界，则S必有下确界

定理1.2
设y=f(x),x∈D为严格增(减)函数，则f必有反函数f\',且f\'在其定义域f(D)上也是严格增(减)函数.

定理 2.1
数列$\left\{ a_{n} \right\}$收敛于$a$的充要条件是：$\left\{ a_{n} - a \right\}$为无穷小数列.

定理 2.2(唯一性) 若数列$\left\{ a_{n} \right\}$收敛，则它只有一个极限.

定理 2.3(有界性)
若数列$\left\{ a_{n} \right\}$收敛，则$\left\{ a_{n} \right\}$为有界数列，即存在正数M,使得对
一切正整数 n,都有$\left| a_{n} \right| \leq M$

定理2.4(保号性)若$\lim_{n \rightarrow \infty}a_{n} = a > 0$
(或\<0),则对任何a\'∈(0,a)(或a\'∈(a,0)), 存在正数 N,使得当
n\>N时，有$a_{n} > a^{'}$ (或$a_{n} < a^{'}$).

定理 2.5(保不等式性)
设$\left\{ a_{n} \right\}$与$\left\{ b_{n} \right\}$均为收敛数列.若存在正数$N_{0}$,使得当$n > N_{0}$时，有$a_{n} \leq b_{n}$,则$\lim_{n \rightarrow \infty}a_{n} \leq \lim_{n \rightarrow \infty}b_{n}$

定理 2.6(迫敛性)
设收敛数列$\left\{ a_{n} \right\},\left\{ b_{n} \right\}$都以
a为极限，数列$\left\{ c_{n} \right\}$满足：存在正数$N_{0}$,当$n > N_{0}$时，有
$a_{n} \leq c_{n} \leq b_{n}$,则数列$\left\{ c_{n} \right\}$收敛，且$\lim_{n \rightarrow \infty}c_{n} = a$

定理 2.7(四则运算法则)
若$\left\{ a_{n} \right\},\left\{ b_{n} \right\}$为收敛数列，则$\left\{ a_{n} + b_{n} \right\},\left\{ a_{n} - b_{n} \right\},\left\{ a_{n} \cdot b_{n} \right\}$也都是收敛数列，且有

$$\lim_{n \rightarrow \infty}\left( a_{n} \pm b_{n} \right) = \lim_{n \rightarrow \infty}a_{n} \pm \lim_{n \rightarrow \infty}b_{n}$$

$$\lim_{n \rightarrow \infty}\left( a_{n} \cdot b_{n} \right) = \lim_{n \rightarrow n}a_{n} \cdot \lim_{n \rightarrow \infty}b_{n}$$

特别当$b_{n}$为常数c时，有

$$\lim_{n \rightarrow \infty}\left( a_{n} + c \right) = \lim_{n \rightarrow \infty}a_{n} + c$$

$$\lim_{n \rightarrow \infty}ca_{n} = c\lim_{n \rightarrow \infty}a_{n}$$

若再假设$b_{n} \neq 0$及$\lim_{n \rightarrow \infty}b_{n} \neq 0$,则$\left\{ \frac{a_{n}}{bn} \right\}$也是收敛数列，且有
$\lim_{n \rightarrow \infty}\frac{a_{n}}{b_{n}} = \frac{\lim_{n \rightarrow \infty}a_{n}}{\lim_{n \rightarrow \infty}b_{n}}$

定理 2.8
数列$\left\{ a_{n} \right\}$收敛的充要条件是：$\left\{ a_{n} \right\}$的任何子列都收敛.

定理 2.9(单调有界定理) 在实数系中，有界的单调数列必有极限.

定理2.10(致密性定理) 任何有界数列必定有收敛的子列.

**定理 2.11(柯西(Cauchy)收敛准则)
数列**$\left\{ \mathbf{a}_{\mathbf{n}} \right\}$**收敛的充要条件是：对任给的**$\mathbf{\varepsilon > 0}$**,存在正整数N,使得当**$\mathbf{n,m > N}$**时，有**$\left| \mathbf{a}_{\mathbf{n}}\mathbf{-}\mathbf{a}_{\mathbf{m}} \right|\mathbf{< \varepsilon}$

定理 3.1
$\lim_{x \rightarrow x_{0}}f(x) = A \Leftrightarrow \lim_{x \rightarrow x_{0}^{+}}f(x) = \lim_{x \rightarrow x_{0}^{-}}f(x) = A$

定理 3.2(唯一性)
若极限$\lim_{x \rightarrow x_{0}}f(x)$存在，则此极限是唯一的

定理3.3(局部有界性)
若$\lim_{x \rightarrow x_{0}}f(x)$存在，则f在$x_{0}$的某空心邻域$U^{o}\left( x_{0} \right)$上有界.

定理3.4(局部保号性)若$\lim_{x \rightarrow x_{0}}f(x) = A > 0$
(或\<0),则对任何正数r\<A(或r\<-A),
存在$U^{o}\left( x_{0} \right)$,使得对一切${x \in U}^{o}\left( x_{0} \right)$,有$f(x) > r > 0$(或$f(x) < - r < 0$).

定理3.5(保不等式性)设$\lim_{x \rightarrow x_{0}}f(x)$与$\lim_{x \rightarrow x_{0}}g(x)$都存在，且在某邻域$U^{0}\left( x_{0};\delta^{'} \right)$上
有f(x)≤g(x),则$\lim_{x \rightarrow x_{0}}f(x) \leq \lim_{x \rightarrow x_{0}}g(x)$

定理3.6(迫敛性)设$\lim_{x \rightarrow x_{0}}f(x) = \lim_{x \rightarrow x_{0}}g(x) = A$,且在某$U^{0}\left( x_{0};\delta^{'} \right)$上有$f(x) \leq h(x) \leq g(x)$则$\lim_{x \rightarrow x_{0}}h(x) = A$

定理3.7(四则运算法则)若极限$\lim_{x \rightarrow x_{0}}f(x)$与$\lim_{x \rightarrow x_{0}}g(x)$都存在，则函数$f \pm g,f \cdot g$当$x \rightarrow x_{0}$时极限也存在，且

1)lim\[f(x)±g(x)\]=limf(x)±limg(x);

2)lim\[f(x)g(x)\]=limf(x)·limg(x);

又若limg(x)≠0,则fig当x→x。时极限存在，且有

3)img(x)=1imf(x)/lig(x).

定理 3.8(归结原则 \| 海涅(Heine)定理)
设f在$U^{0}\left( x_{0};\delta^{'} \right)$上有定义.$\lim_{x \rightarrow x_{0}}f(x)$存在的充要条件是：对任何含于$U^{0}\left( x_{0};\delta^{'} \right)$且以$x_{0}$为极限的数列$\left\{ x_{n} \right\}$,极限$\lim_{n \rightarrow \infty}f\left( x_{n} \right)$都存在且相等.

归结原则也可简述为：$\lim_{x \rightarrow x_{0}}f(x) = A \Leftrightarrow 对任何x_{n} \rightarrow x_{0}(n \rightarrow \infty)有\lim_{n \rightarrow \infty}f\left( x_{n} \right) = A$

定理3.9
(单侧极限时的更强形式)设函数f在点$x_{0}$的某空心右邻域$U_{+}^{0}\left( x_{0} \right)$有定义.
$\lim_{x \rightarrow x_{0}^{+}}f(x) = A$的充要条件是：对任何以$x_{0}$为极限的**递减**数列$\left\{ x_{n} \right\} \subset U_{+}^{0}\left( x_{0} \right)$,有$\lim_{n \rightarrow \infty}f\left( x_{n} \right) = A$

定理3.10
设f为定义在$U^{O}\left( x_{0} \right)$上的单调有界函数，则右极限$\lim_{x \rightarrow x_{0}^{+}}f(x)$存在（对应单调有界定理）

定理3.11(柯西准则)设函数f在$U^{0}\left( x_{0};\delta^{'} \right)$上有定义.
$\lim_{x \rightarrow x_{0}}f(x)$存在的充要条件是：任给
$\varepsilon > 0$,存在正数$\delta( < \delta^{'})$,使得对任何$x^{'},x^{''} \in U^{0}\left( x_{0};\delta^{'} \right)$,有$\left| f\left( x^{'} \right) - f\left( x^{''} \right) \right| < \varepsilon$

定义1 设f在某$U^{O}\left( x_{0} \right)$上有定义.若

$$\lim_{x \rightarrow x_{0}}f(x) = 0$$

则称f为当$x \rightarrow x_{0}$时的**无穷小量**

定理3.12设函数f,g,h在$U^{O}\left( x_{0} \right)$上有定义，且有$f(x)\sim g(x)\left( x \rightarrow x_{0} \right)$

i\.
若$\lim_{x \rightarrow x_{0}}f(x)h(x) = A$则$\lim_{x \rightarrow x_{0}}g(x)h(x) = A$

ii\.
若$\lim_{x \rightarrow x_{0}}\frac{h(x)}{f(x)} = B$则$\lim_{x \rightarrow x_{0}}\frac{h(x)}{g(x)} = B$

定义3 对于自变量 x的某种趋向(或$n \rightarrow \infty$时),所有以$\infty$,
$+ \infty$或$- \infty$为非正常极限的函数(包括数列),都称为**无穷大量**.

定理 3.13(对无穷大量的研究可归结为对无穷小量的讨论)

(i)设f在$U^{O}\left( x_{0} \right)$上有定义且不等于0.若f为$x \rightarrow x_{0}$时的无穷小量，则$\frac{1}{f}$为$x \rightarrow x_{0}$时的无穷大量.

(ii)若g为$x \rightarrow x_{0}$时的无穷大量，则$\frac{1}{g}$为$x \rightarrow x_{0}$时的无穷小量.

定义4
若曲线C上的动点P沿着曲线无限地远离原点时，点P与某定直线L的距离趋于0,则称直线L为曲线C的**渐近线**

定义1
设函数f在某$U\left( x_{0} \right)$上有定义.若$\lim_{x \rightarrow x_{0}}f(x) = f\left( x_{0} \right)$则称f**在点**$\mathbf{x}_{\mathbf{0}}$**连续**.

定义 2 设
函数f在某$U_{+}\left( x_{0} \right)$($U_{-}\left( x_{0} \right)$)有定义.若$\lim_{x \rightarrow x_{0}^{+}}f(x) = f\left( x_{0} \right)$($\lim_{x \rightarrow x_{0}^{-}}f(x) = f\left( x_{0} \right)$)则称
f在点$x_{0}$**右(左)连续**

定理 4.1
函数f在点$x_{0}$连续的充要条件是：f在点$x_{0}$既是右连续，又是左连续

定义3 设
函数f在某$U^{O}\left( x_{0} \right)$上有定义.若f在点$x_{0}$无定义，或f在点$x_{0}$有定义而不连
续，则称点$x_{0}$为函数 f的**间断点**或**不连续点**

定理4.2(局部有界性)若函数f在点$x_{0}$连续，则f在某U(x?)上有界

定理4.3(局部保号性)若函数f在点$x_{0}$连续，且f($x_{0}$)\>0(或\<0),则对任何正数
r\<f($x_{0}$)(或r\<-f($x_{0}$)),存在某
U($x_{0}$),使得对一切x∈U($x_{0}$),有

f(x)\>r(或f(x)\<-r)

定理4.4(四则运算)若函数f和g在点$x_{0}$连续，则f±g,f·g,flg(这里g(x?)≠0)也都在点$x_{0}$连续.

定理 4.5
若函数f在点$x_{0}$连续，g在点$u_{0}$连续，$u_{0} = f\left( x_{0} \right)$则复合函数$g \circ f$在点$x_{0}$连续.

定义1 设f为定义在数集 D上的函数.若存在
x?∈D,使得对一切x∈D,有$f\left( x_{0} \right) \geq f(x)$($f\left( x_{0} \right) \leq f(x)$)

则称f在
D上有最大(最小)值，并称$f\left( x_{0} \right)$为f在D上的**最大(最小)值**.

定理4.6(最大、最小值定理)
若函数f在闭区间\[a,b\]上连续，则f在\[a,b\]上有最大值与最小值.

引理(有界性定理)若函数f(x)在闭区间\[a,b\]上连续，那么f(x)在闭区间\[a,b\]上有界.

定理
4.7(介值性定理)设函数f在闭区间\[a,b\]上连续，且f(a)≠f(b).若μ为介于f(a)与f(b)之间的任何实数(f(a)\<μ\<f(b)或f(a)\>μ\>f(b)),则至少存在一点$x_{0}$∈(a,b),使得$f\left( x_{0} \right) = \mu$

推论(根的存在定理)若函数f在闭区间\[a,b\]上连续，且f(a)与f(b)异号(即f(a)f(b)\<0),则至少存在一点$x_{0}$∈(a,b),使得$f\left( x_{0} \right) = 0$即方程f(x)=0在(a,b)上至少有一个根

定理 4.8 若函数f在\[a,b\]上严格单调并连续，则反函数$f^{- 1}$在其定义域
\[f(a),f(b)\]或\[f(b),f(a)\]上连续

定义2
设f为定义在区间I上的函数.若对任给的$\varepsilon > 0$,存在$\delta = \delta(\varepsilon) > 0$,使得对任何$x^{'},x^{''} \in I$,只要$\left| x^{'} - x^{''} \right| < \delta$,就有$\left| f\left( x^{'} \right) - f\left( x^{''} \right) \right| < \varepsilon$,则称函数f在区间I上**一致连续**.

定理
4.9(一致连续性定理)若函数f在闭区间\[a,b\]上连续，则f在\[a,b\]上一致连续.

定理 4.10 设
a\>0,α,β为任意两个实数，则有$a^{\alpha} \cdot a^{\beta} = a^{\alpha + \beta},\left( a^{\alpha} \right)^{\beta} = a^{\alpha\beta}$

定理 4.11 指数函数$a^{x}(a > 0)$在R上是连续的.

定理 4.12 一切基本初等函数都是其定义域上的连续函数.

定理 4.13 任何初等函数都是在其定义区间上的连续函数.

定理5.1 若函数f在点$x_{0}$可导，则f在点$x_{0}$连续.

定理 5.2 若函数
y=f(x)在点$x_{0}$的某邻域上有定义，则f\'(x?)存在的充要条件是:$f_{+}^{'}\left( x_{0} \right)$与$f_{-}^{'}\left( x_{0} \right)$都存在，且$f_{+}^{1}\left( x_{0} \right) = f_{-}^{'}\left( x_{0} \right)$

定理 5.3(费马定理)
设函数f在点$x_{0}$的某邻域上有定义，且在点$x_{0}$可导.若点$x_{0}$为f的极值点，则必有$f^{'}\left( x_{0} \right) = 0$

定理5.4
若函数u(x)和v(x)在点$x_{0}$可导，则函数f(x)=u(x)±v(x)在点$x_{0}$也可导，且$f^{'}\left( x_{0} \right) = u^{'}\left( x_{0} \right) \pm v^{'}\left( x_{0} \right)$

定理5.5 若函数u(x)和
v(x)在点$x_{0}$可导，则函数f(x)=u(x)v(x)在点$x_{0}$也可导，且$f^{'}\left( x_{0} \right) = w\left( x_{0} \right)v\left( x_{0} \right) + u\left( x_{0} \right)\nu^{'}\left( x_{0} \right)$

定理 5.6 若函数u(x)和v(x)在点$x_{0}$都可导，且 v(x?)≠0,则
$f(x) = \frac{u(x)}{v(x)}$在点$x_{0}$也可导，且$f^{1}\left( x_{0} \right) = \frac{u^{'}\left( x_{0} \right)v\left( x_{0} \right) - u\left( x_{0} \right)v^{'}\left( x_{0} \right)}{\left\lbrack v\left( x_{0} \right) \right\rbrack^{2}}$

定理 5.7
设y=f(x)为x=φ(y)的反函数，若φ(y)在点$y_{0}$的某邻域上连续，严格单调且$\varphi^{'}\left( y_{0} \right) \neq 0$,则f(x)在点$x_{0}\left( x_{0} = \varphi\left( y_{0} \right) \right)$可导，且$f^{'}\left( x_{0} \right) = \frac{1}{\varphi^{'}\left( y_{0} \right)}$

定理5.9
函数f在点$x_{0}$可微的充要条件是函数f在点$x_{0}$可导，而且(1)式中的A等于f\'($x_{0}$).

定理6.1(罗尔(Rolle)中值定理) 若函数f满足如下条件：

(i)f在闭区间\[a,b\]上连续；

(ii)f在开区间(a,b)上可导；

(iii)f(a)=f(b),

则在(a,b)上至少存在一点ξ,使得f\'(ξ)= 0.

定理6.2(拉格朗日(Lagrange)中值定理) 若函数f满足如下条件：

(i)f在闭区间\[a,b\]上连续；

(ii)f在开区间(a,b)上可导，

则在(a,b)上至少存在一点ξ,使得

$$f^{'}(\xi) = \frac{f(b) - f(a)}{b - a}$$

推论1 若函数f在区间I上可导，且f\'(x)=0,x∈I,则f为I上的一个常量函数.

推论2 若函数f和g均在区间1上可导，且f\'(x)=g\'(x),x∈I,则在区间 I上
f(x)与g(x)只相差某一常数，即 f(x)=g(x)+c(c为某一常数).

推论3(导数极限定理) 设函数f在点$x_{0}$的某邻域
U(x0)上连续，在U°($x_{0}$)上可

导，且极限$\lim_{x \rightarrow x_{0}}f^{'}(x)$存在，则子在点$x_{0}$可导，且
$f^{'}\left( x_{0} \right) = \lim_{x \rightarrow x_{0}}f^{'}(x)$

定理 6.3
设f(x)在区间1上可导，则f(x)在I上递增(减)的充要条件是$f^{'}(x) \geq 0( \leq 0)$

定理 6.4 若函数f在(a,b)上可导，则f在 (a,b)上严格递增(递减)的充要条件是：

(i)对一切x∈(a,b),有f\'(x)≥0(f\'(x)≤0);

(ii)在(a,b)的任何子区间上f\'(x)≠0.

定理 6.5(达布(Darboux)定理) 若函数f在\[a,b\]上可导，且f\'.(a)≠f\'(b),k
为介于f\'(a)f\'(b)之间任一实数，则至少存在一点$\xi \in (a,b)$,使得
$f^{'}(\xi) = k$.有时称上述定理为导函数的介值定理.

推论 设函数f(x)在区间1上满足f\'(x)≠0,那么f(x)在区间I上严格单调.

定理 6.6(柯西中值定理) 设函数f和g满足：

(i)在\[a,b\]上都连续；

(ii)在(a,b)上都可导；

(iii)f\'(x)和g\'(x)不同时为零；

(iv)g(a)≠g(b),

则存在ξ∈(a,b),使得$\frac{f^{'}(\xi)}{g^{'}(\xi)} = \frac{f(b) - f(a)}{g(b) - g(a)}$

定理 6.7 若函数f和g满足：

(i)$\lim_{x \rightarrow x_{0}}f(x) = \lim_{x \rightarrow x_{0}}g(x) = 0$
;

(ii)在点$x_{0}$的某空心邻域 U°($x_{0}$)上两者都可导，且g\'(x)≠0;

(ii)$\lim_{x \rightarrow x_{0}}\frac{f^{'}(x)}{g^{'}(x)} = A$(A可为实数，也可为$\pm \infty$或$\infty$),

则$\lim_{x \rightarrow x_{0}}\frac{f(x)}{g(x)} = \lim_{x \rightarrow x_{0}}\frac{f^{'}(x)}{g^{'}(x)} = A$

定理 6.8 若函数f和g满足：

(i)在$x_{0}$的某个邻域U°($x_{0}$)上两者可导，且g\'(x)≠0;

\(ii\) $\lim_{x \rightarrow x_{0}}g(x) = \infty$;

(iii)$\lim_{x \rightarrow x_{0}}\frac{f^{'}(x)}{g^{'}(x)} = A$(A可为实数，也可为$\pm \infty$或$\infty$),

则$\lim_{x \rightarrow x_{0}}\frac{f(x)}{g(x)} = \lim_{x \rightarrow x_{0}}\frac{f^{'}(x)}{g^{'}(x)} = A$

定理 6.9
若函数f在点x。存在直至n阶导数，则有$f(x) = T_{n}(x) + o\left( \left( x - x_{0} \right)^{n} \right)$，即

$$f(x) = f\left( x_{0} \right) + \frac{f^{'}\left( x_{0} \right)}{1!}\left( \chi - x_{0} \right) + \frac{f^{''}\left( x_{0} \right)}{2!}\left( x - x_{0} \right)^{2} + \ldots + \frac{f^{(n)}\left( x_{0} \right)}{n!}\left( x - x_{0} \right)^{n} + o\left( \left( x - x_{0} \right)^{n} \right)$$

该式称为函数f在x0的泰勒公式，$R_{n}(x) = f(x) - T_{n}(x)$称为泰勒公式的余项，形如$o\left( \left( x - x_{0} \right)^{n} \right)$的余项称为佩亚诺(Peano)型余项.所以(4)式又称为带有佩亚诺型余项的泰勒公式.

定理 6.10(泰勒定理) 若函数f在\[a,b\]上存在直至n阶的连续导函数，在(a,b)

上存在(n+1)阶导函数，则对任意给定的x,x0∈\[a,b\],至少存在一点ξ∈(a,b),使得

$$f(x) = f\left( x_{0} \right) + \frac{f^{'}\left( x_{0} \right)}{1!}\left( \chi - x_{0} \right) + \frac{f^{''}\left( x_{0} \right)}{2!}\left( x - x_{0} \right)^{2} + \ldots + \frac{f^{(n)}\left( x_{0} \right)}{n!}\left( x - x_{0} \right)^{n} + \frac{f^{(n + 1)}(\xi)}{(n + 1)!}\left( x - x_{0} \right)^{n + 1}$$

（拉格朗日型余项）

定理6.11(极值的第一充分条件)
设f在点$x_{0}$连续，在某邻域$U^{o}\left( x_{0};\delta \right)$上可导

(i)若当$x \in \left( x_{0} - \delta,x_{0} \right)$时f\'(x)≤0,当$x \in \left( x_{0},x_{0} + \delta \right)$时f\'(x)≥0,则f在点$x_{0}$取得极小值.

(ii)若当$x \in \left( x_{0} - \delta,x_{0} \right)$时f\'(x)≥0,当$x \in \left( x_{0},x_{0} + \delta \right)$时f\'(x)≤0,则f在点$x_{0}$取得极大值.

定理 6.12(极值的第二充分条件)
设f在$x_{0}$的某邻域$U^{o}\left( x_{0};\delta \right)$上一阶可导，在$x = x_{0}$处二阶可导，且$f^{'}\left( x_{0} \right) = 0,f^{''}\left( x_{0} \right) \neq 0$.

(i)若$f^{''}\left( x_{0} \right) < 0$,则f在$x_{0}$取得极大值.

(ii)若$f^{''}\left( x_{0} \right) > 0$,则f在$x_{0}$取得极小值.

定理6.13(极值的第三充分条件)
设f在$x_{0}$的某邻域上存在直到n-1阶导函数，在$x_{0}$处 n
阶可导，且$f^{(k)}\left( x_{0} \right) = 0,(k = 1,2,\ldots,n - 1),f^{(n)}(x) \neq 0$,则

(i)当 n 为 偶 数
时，f在$x_{0}$取得极值，且当$f^{(n)}\left( x_{0} \right) < 0$时取极大值，$f^{(n)}\left( x_{0} \right) > 0$时取极小值.

(ii)当n为奇数时、f在$x_{0}$处不取极值

定理6.14 设f为区间I上的可导函数，则下述论断互相等价：

1°f为I上凸函数；

2°f\'为I上的增函数；

3°对I上的任意两点$x_{1},x_{2}$,有$f\left( x_{2} \right) \geq f\left( x_{1} \right) \rightarrow f^{'}\left( x_{1} \right)\left( x_{2} - x_{1} \right)$

定理 6.15 设f为区间I上的二阶可导函数，则在I上f为凸(凹)函数的充要条件是

$$f^{''}(x) \geq 0\left( f^{''}(x) \leq 0 \right),x \in I$$

定理 7.1(区间套定理)
若\|\[a。,b.\]}是一个区间套，则在实数系中存在唯一的一点ξ,使得$\xi \in \left\lbrack a_{n},b_{n} \right\rbrack,n = 1,2,\cdots$,即

$$a_{n} \leq \xi \leq b_{n},n = 1,2,\cdots 2$$

定理 7.2(魏尔斯特拉斯(Weierstrass)聚点定理) 实轴上的任一有界无限点集S
至少有一个聚点.

定理 8.1 若函数f在区间I上连续，则子在I上存在原函数 F,即 F\'(x)=
f(x),x∈l.

定理 8.2 设F是f在区间I上的一个原函数，则

(i)F+C也是f在I上的原函数，其中C为任意常量函数;

(ii)f在I上的任意两个原函数之间，只可能相差一个常数.

定理 8.3（线性法则）
若函数f与g在区间I上都存在原函数，$k_{1},k_{2}$为两个任意常数，则$k_{1}f + k_{2}g$在I上也存在原函数，且当k1和k2不同时为零时，有

$$\int\left\lbrack k_{1}f(x) + k_{2}g(x) \right\rbrack\mathbb{d}x = k_{1}\int f(x)\mathbb{d}x + k_{2}\int g(x)\mathbb{d}x$$

§2 换元积分法与分部积分法

定理 8.4 (第一换元积分法)( 凑微分法)
(这两个与复合函数求导法对应)设函数f(x)在区间I上有定义，φ(t)在区间J上可导，且.如果不定积分$\int f(x)\mathbb{d}x = F(x) + C$在1上存在，则不定积分$\int f\left( \varphi(t) \right)\varphi^{'}(t)\mathbb{d}t$在J上也存在，且

$$\int f\left( \varphi(t) \right)\varphi^{'}(t)\mathbb{d}t = F\left( \varphi(t) \right) + C$$

定理 8.5(第二换元积分法)
(代入换元法)设函数f(x)在区间1上有定义，φ(t)在区间J上
可导，φ(J)=I,且x=φ(t)在区间J上存在反函数1=φ1(x),x∈I.如果不定积分$\int f(x)\mathbb{d}x$在I上存在，则当不定积分$\int f\left( \varphi(t) \right)\varphi^{'}(t)\mathbb{d}t = G(t) + C$在J上存在时，在I上有

$$\int f(x)\mathbb{d}x = G\left( \varphi^{- 1}(x) \right) + C$$

定理8.6(分部积分法)(与乘积求导相对应)若u(x)与v(x)可导，不定积分
$\int u^{'}(x)v(x)\mathbb{d}x$存在，则$\int u(x)\nu^{'}(x)\mathbb{d}x$也存在，并有

$$\int u(x)v^{'}(x)\mathbb{d}x = u(x)\nu(x) - \int u^{'}(x)v(x)\mathbb{d}x$$

定理 9.1 若函数f在\[a,b\]上连续，且存在原函数
F,即$F^{'}(x) = f(x),x \in \lbrack a,b\rbrack$,

则f在\[a,b\]上可积，且

$$\int_{a}^{b}{f(x)\mathbb{d}x} = F(b) - F(a)$$

上式称为牛顿一莱布尼茨公式，它也常写成

$$\int_{a}^{b}{f(x)\mathbb{d}x} = {F\left. \ (x) \right|}_{a}^{b}$$

定理 9.2 若函数f在\[a,b\]上可积，则f在\[a,b\]上必定有界.

定理9.3(可积准则)
函数f在\[a,b\]上可积的充要条件是：任给c\>0,总存在相应的一个分割T,使得$S(T) - s(T) < \varepsilon$

定理9.3′
函数f在\[a,b\]上可积的充要条件是：任给c\>0,总存在相应的某一分割T,使得$\sum_{T}^{}{w_{i}\Delta x_{i}} < \varepsilon$

定理 9.4 若f为\[a,b\]上的连续函数，则f在\[a,b\]上可积.

定理9.5
若f是区间\[a,b\]上只有有限个间断点的有界函数，则f在\[a,b\]上可积.

定理9.6 若f是\[a,b\]上的单调函数，则f在\[a,b\]上可积.

定理9.7(积分第一中值定理) 若f在\[a,b\]上连续，则至少存在一点ξ∈\[a,b\],
使得$\int_{a}^{b}{f(x)\mathbb{d}x} = f(\xi)(b - a)$

这里$f(\xi)$可以理解成为f(x)在区间\[a,b\]上所有函数值的平均值

定理9.8(推广的积分第一中值定理)
若f与g都在\[a,b\]上连续，且g(x)在\[a,b\]上不变号，则至少存在一点$\xi \in \lbrack a,b\rbrack$,使得

$$\int_{a}^{b}{f(x)g(x)\mathbb{d}x} = f(\xi)\int_{a}^{b}{g(x)\mathbb{d}x}$$

（$g(x) = 1$，即为定理9.7.)

定理 **9.9 若** J在\[a,b\]上可积，则由 **(l)**
式所定义的函数中在\[a,b\]上连续

定理 9.10 (原函数存在定理)
若f在\[a,b\]上连续，则由(1)式所定义的函数$\Phi$在\[a,b\]上处处可导，且

$$\Phi^{'}(x) = \frac{\mathbb{d}}{\mathbb{d}x}\int_{a}^{x}{f(t)\mathbb{d}t} = f(x),x \in \lbrack a,b\rbrack$$

定理 9.11(积分第二中值定理) 设函数f在\[a,b\]上可积.

(i)若函数g在\[a,b\]上减，且g(x)≥0,则存在$\xi \in \lbrack a,b\rbrack$,使得$\int_{a}^{b}{f(x)g(x)\mathbb{d}x} = g(a)\int_{a}^{\xi}{f(x)\mathbb{d}x}$

(ii)若函数g在\[a,b\]上增，且g(x)≥0,则存在$\eta \in \lbrack a,b\rbrack$,使得$\int_{a}^{b}{f(x)g(x)\mathbb{d}x} = g(b)\int_{\eta}^{b}{f(x)\mathbb{d}x}$

推论
设函数f在\[a,b\]上可积.若g为单调函数，则存在$\xi \in \lbrack a,b\rbrack$,使得

$$\int_{a}^{b}{f(x)g(x)\mathbb{d}x} = g(a)\int_{a}^{\xi}{f(x)\mathbb{d}x} + g(b)\int_{\xi}^{b}{f(x)\mathbb{d}x}$$

定理 9.12(定积分换元积分法)
若函数f在\[a,b\]上连续，$\varphi^{'}$在\[α,β\]上可积，且满足

$$\varphi(\alpha) = a,\varphi(\beta) = b,\varphi\left( \lbrack\alpha,\beta\rbrack \right) \subseteq \lbrack a,b\rbrack$$

则有定积分换元公式：

$$\int_{a}^{b}{f(x)\mathbb{d}x} = \int_{\alpha}^{\beta}{f\left( \varphi(t) \right)\varphi^{'}(t)\mathbb{d}t}$$

定理 9.13(定积分分部积分法)若u(x),v(x)为\[a,b\]上的可微函数，且u\'(x) 和
v\'(x)都在\[a,b\]上可积，则有定积分分部积分公式：

$$\int_{a}^{b}{u(x)v^{'}(x)\mathbb{d}x} = {u(x)v\left. \ (x) \right|}_{a}^{b} - \int_{a}^{b}{u^{'}(x)v(x)\mathbb{d}x}$$

定义1
设函数f定义在无穷区间$\lbrack a, + \infty)$上，且在任何有限区间$\lbrack a,u\rbrack$上可积.如果存在极限

$$\lim_{u \rightarrow + \infty}\int_{a}^{u}{f(x)\mathbb{d}x} = J$$

则称此极限J为函数f在$\lbrack a, + \infty)$上的**无穷限反常积分**(简称**无穷积分**),记作

$$J = \int_{a}^{+ \infty}{f(x)\mathbb{d}x}$$

并称$\int_{a}^{+ \infty}{f(x)\mathbb{d}x}$收敛，如果极限(1)不存在，为方便起见，亦称$\int_{a}^{+ \infty}{f(x)\mathbb{d}x}$发散

定义2
设函数子定义在区间$(a,b\rbrack$上，在点a的任一右邻域上无界，但在任何内闭区间$\lbrack u,b\rbrack \subset (a,b\rbrack$上有界且可积.如果存在极限

$$\lim_{u \rightarrow a^{+}}\int_{u}^{b}{f(x)\mathbb{d}x} = J$$

则称此极限为**无界函数**f在$(a,b\rbrack$上的**反常积分**，记作

$$J = \int_{a}^{b}{f(x)\mathbb{d}x}$$

并称反常积分$\int_{a}^{b}{f(x)\mathbb{d}x}$收敛.如果极限(5)不存在，这时也说反常积分$\int_{a}^{b}{f(x)\mathbb{d}x}$发散

在定义2中，被积函数f在点a近旁是无界的，这时点a称为f的**瑕点**，而无界函数反常积分$\int_{a}^{b}{f(x)\mathbb{d}x}$又称为瑕积分.

定理11.1
无穷积分$\int_{a}^{+ \infty}{f(x)\mathbb{d}x}$收敛的充要条件是：任给$\varepsilon > 0$,存在G≥a,只要$u_{1},u_{2} > G$,便有

$$\left| \int_{a}^{u_{2}}{f(x)\mathbb{d}x} - \int_{a}^{u_{1}}{f(x)\mathbb{d}x} \right| = \left| \int_{u_{1}}^{u_{2}}{f(x)\mathbb{d}x} \right| < \varepsilon$$

定理11.2(比较原则)
设定义在$\lbrack a, + \infty)$上的两个非负函数f和g都在任何有限区间\[a,u\]上可积，且满足$f(x) \leq g(x),x \in \lbrack a, + \infty)$

则当$\int_{a}^{+ \infty}{g(x)\mathbb{d}x}$收敛时，$\int_{a}^{+ \infty}{f(x)\mathbb{d}x}$必收敛(或当$\int_{a}^{+ \infty}{g(x)\mathbb{d}x}$发散时，$\int_{a}^{+ \infty}{f(x)\mathbb{d}x}$必发散)

定理11.3(狄利克雷判别法)
若$F(u) = \int_{a}^{u}{f(x)\mathbb{d}x}$在$\lbrack a, + \infty)$上有界，g(x)在$\lbrack a, + \infty)$上当$x \rightarrow + \infty$时单调趋于0,则$\int_{a}^{+ \infty}{f(x)g(x)\mathbb{d}x}$收敛

定理11.4(阿贝尔(Abel)判别法)若$\int_{a}^{u}{f(x)\mathbb{d}x}$收敛g(x)在$\lbrack a, + \infty)$上单调有界，则$\int_{a}^{+ \infty}{f(x)g(x)\mathbb{d}x}$收敛

定理11.5 瑕积分
$\int_{a}^{b}{f(x)\mathbb{d}x}$(瑕点为a)收敛的充要条件是：任给$\varepsilon > 0$,存在$\delta > 0$,只要$u_{1},u_{2} \in (a,a + \delta)$,总有

$$\left| \int_{u_{1}}^{b}{f(x)\mathbb{d}x} - \int_{u_{2}}^{b}{f(x)\mathbb{d}x} \right| = \left| \int_{u_{1}}^{u_{2}}{f(x)\mathbb{d}x} \right| < \varepsilon$$

定理11.6(比较原则)
设定义在$(a,b\rbrack$上的两个非负函数f和g都在任何有限区间$\lbrack u,b\rbrack \subset (a,b\rbrack$上可积，且满足$0 \leq f(x) \leq g(x),x \in (a,b\rbrack$

则当$\int_{a}^{b}{g(x)\mathbb{d}x}$收敛时，$\int_{a}^{b}{f(x)\mathbb{d}x}$必收敛(或当$\int_{a}^{b}{g(x)\mathbb{d}x}$发散时，$\int_{a}^{b}{f(x)\mathbb{d}x}$必发散)

定理11.7(狄利克雷判别法) 设
a为f(x)的瑕点，若$F(u) = \int_{u}^{b}{f(x)\mathbb{d}x}$在$(a,b\rbrack$上有界，g(x)在$(a,b\rbrack$上单调且$\lim_{x \rightarrow a^{+}}g(x) = 0$,则$\int_{a}^{b}{f(x)g(x)\mathbb{d}x}$收敛

定理11.8(阿贝尔(Abel)判别法) 设
a为f(x)的瑕点，若$\int_{a}^{u}{f(x)\mathbb{d}x}$收敛g(x)在$(a,b\rbrack$上单调有界，则$\int_{a}^{+ \infty}{f(x)g(x)\mathbb{d}x}$收敛

我们称满足方程f\'(x)=0的点为稳定点(也称为驻点)
