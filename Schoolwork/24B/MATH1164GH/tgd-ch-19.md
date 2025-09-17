# 第十九章 含参量积分


## 含参量正常积分

1. 含参量积分

   设 $f(x,y)$ 为定义在矩形区域 $R = [a,b] \times [c,d]$ 上的二元函数，若对于 $[a,b]$ 上每一固定的 $x$ 值，$f(x,y)$ 作为 $y$ 的函数在闭区间 $[c,d]$ 上可积，则其积分值是 $x$ 在 $[a,b]$ 上取值的函数，记作 $I(x)$，即
   $$
   I(x) = \int_{c}^{d} f(x,y) \, dy, \quad x \in [a,b].
   $$
   函数 $I(x)$ 称为定义在 $[a,b]$ 上含参量 $x$ 的正常积分，简称含参量积分。

   它的更一般的情形是上、下限也是 $x$ 的函数：设 $f(x,y)$ 为定义在区域
   $$
   G = \{(x,y) \mid c(x) \leq y \leq d(x), a \leq x \leq b\}
   $$
   上的二元函数，其中 $c(x), d(x)$ 为定义在 $[a,b]$ 上的连续函数。若对于 $[a,b]$ 上每一固定 $x$ 值，$f(x,y)$ 作为 $y$ 的函数在闭区间 $[c(x), d(x)]$ 上可积，则其积分值是 $x$ 在 $[a,b]$ 上取值的函数，记作 $F(x)$，即
   $$
   F(x) = \int_{c(x)}^{d(x)} f(x,y) \, dy, \quad x \in [a,b],
   $$
   函数 $F(x)$ 同样称为定义在 $[a,b]$ 上含参量 $x$ 的正常积分，简称含参量积分。

2. 含参积分的性质

   | 性质 | 内容 |
   | --- | --- |
   | 连续性 | (1) 若二元函数 $f(x,y)$ 在矩形区域 $R = [a,b] \times [c,d]$ 上连续，则函数 $I(x) = \int_{c}^{d} f(x,y) \, dy$ 在 $[a,b]$ 上连续。<br />(2) 若二元函数 $f(x,y)$ 在区域 $G = \{(x,y) \mid c(x) \leq y \leq d(x), a \leq x \leq b\}$ 上连续，其中 $c(x), d(x)$ 为 $[a,b]$ 上的连续函数，则函数 $F(x) = \int_{c(x)}^{d(x)} f(x,y) \, dy$ 在 $[a,b]$ 上连续。 |
   | 可微性 | (1) 若二元函数 $f(x,y)$ 及其偏导数 $f_x(x,y)$ 都在 $[a,b] \times [c,d]$ 上连续，则 $I(x) = \int_{c}^{d} f(x,y) \, dy$ 在 $[a,b]$ 上可微，且 $I'(x) = \int_{c}^{d} f_x(x,y) \, dy, \quad x \in [a,b]$。<br />(2) 若二元函数 $f(x,y), f_x(x,y)$ 在 $[a,b] \times [p,q]$ 上连续，且 $c(x), d(x)$ 为定义在 $[a,b]$ 上其值含于 $[p,q]$ 内的可微函数，则函数 $F(x) = \int_{c(x)}^{d(x)} f(x,y) \, dy$ 在 $[a,b]$ 上可微且<br /> $F'(x) = \int_{c(x)}^{d(x)} f_x(x,y) \, dy + f(x,d(x))d'(x) - f(x,c(x))c'(x), \quad x \in [a,b]$<br />若二元函数 $f(x,y)$ 在 $[a,b] \times [c,d]$ 上连续，则函数 $I(x) = \int_{c}^{b} f(x,y) \, dy, J(x) = \int_{a}^{b} f(x,y) \, dx$ 分别在 $[a,b]$ 和 $[c,d]$ 上可积，且 $\int_{a}^{b} \int_{c}^{d} f(x,y) \, dy \, dx = \int_{c}^{d} \int_{a}^{b} f(x,y) \, dx \, dy$。 |
   | 可积性 | 小提示：对于含参量积分的三个性质，基本上只要被积的二元函数是连续的，则结论是成立的，其中可微性需要添加可微的条件。 |

## 含参量反常积分

### 1. 基本概念

| 名称 | 定义 |
| --- | --- |
| 含参量反常积分 | 设函数 $f(x,y)$ 定义在无界区域 $R = [a,b] \times [c,+\infty)$ 上，若对每一个固定的 $x \in [a,b]$，反常积分 $\int_{c}^{+\infty} f(x,y) \, dy$ 都收敛，则它的值是 $x$ 在 $[a,b]$ 上取值的函数，记作 $I(x)$，即 $ I(x) = \int_{c}^{+\infty} f(x,y) \, dy, \quad x \in [a,b]$ 函数 $I(x)$ 称为含参量 $x$ 的无穷限反常积分，简称含参量反常积分 |
| 含参量反常积分的一致收敛 | 若 $\forall \varepsilon > 0$，$\exists N > c$，使得当 $M > N$ 时，对任何 $x \in [a,b]$ 都有 $\abs{\int_{M}^{+\infty} f(x,y) \, dy} < \varepsilon$，则称该含参量反常积分在 $[a,b]$ 上一致收敛于 $I(x)$ |

### 2. 反常积分一致收敛的判别方法

| 名称 | 公式 | 函数项级数 |
| --- | --- | --- |
| 柯西准则 | $\forall \varepsilon > 0, \exists M > c, \forall A > B > A_1 > M, \forall x \in I, \abs{\int_{A_1}^{A_2} f(x,y) \, dy} < \varepsilon$ | $\forall \varepsilon > 0, \exists N \in \mathbb{N}_+, \forall m_2 > m_1 > N, \forall x \in I, \abs{\sum_{n=m_1}^{m_2} u_n(x)} < \varepsilon$ |
| 魏尔斯特拉斯M判别法 | 若 $\forall (x,y) \in I \times [c,+\infty)$，有 $\abs{f(x,y)} \leq g(y)$，且 $\int_{c}^{+\infty} g(y) \, dy$ 收敛，则 $\int_{c}^{+\infty} f(x,y) \, dy$ 在 $I$ 上一致收敛 | 若 $\forall n \in \mathbb{N}_+, \forall x \in I$，有 $\abs{u_n(x)} \leq M_n$，且 $\sum_{n=1}^{\infty} M_n$ 收敛，则 $\sum_{n=1}^{\infty} u_n(x)$ 在 $I$ 上一致收敛 |
| 狄利克雷判别法 | 若 $\forall N > c, \int_{c}^{N} f(x,y) \, dy$ 在 $I$ 上一致有界，$\forall x \in I, g(x,y)$ 关于 $y$ 是单调的，且 $g(x,y) \to 0 (y \to +\infty), x \in I$，则 $\int_{c}^{+\infty} f(x,y) g(x,y) \, dy$ 在 $I$ 上一致收敛 | 若 $\forall n \in \mathbb{N}_+, \sum_{k=1}^{n} u_k(x)$ 在 $I$ 上一致有界，$\forall x \in I, (v_n(x))$ 是单调的，且 $v_n(x) \to 0 (n \to +\infty), x \in I$，则 $\sum_{n=1}^{\infty} u_n(x) v_n(x)$ 在 $I$ 上一致收敛 |
| 阿贝尔判别法 | 若 $\int_{c}^{+\infty} f(x,y) \, dy$ 在 $I$ 上一致收敛，$\forall x \in I, g(x,y)$ 关于 $y$ 是单调的，且在 $I$ 上一致有界，则 $\int_{c}^{+\infty} f(x,y) g(x,y) \, dy$ 在 $I$ 上一致收敛 | 若 $\sum_{n=1}^{\infty} u_n(x)$ 在 $I$ 上一致收敛，$\forall x \in I, (v_n(x))$ 是单调的，且在 $I$ 上一致有界，则 $\sum_{n=1}^{\infty} u_n(x) v_n(x)$ 在 $I$ 上一致收敛 |

### 3. 含参量反常积分的性质

| 性质 | 内容 |
| --- | --- |
| 连续性 | 设 $f(x,y)$ 在 $[a,b] \times [c,+\infty)$ 上连续，若含参量反常积分 $I(x) = \int_{c}^{+\infty} f(x,y) \, dy$ 在 $[a,b]$ 上一致收敛，则 $I(x)$ 在 $[a,b]$ 上连续 |
| 可微性 | 设 $f(x,y)$ 与 $f_x(x,y)$ 在 $[a,b] \times [c,+\infty)$ 上连续，若 $I(x) = \int_{c}^{+\infty} f(x,y) \, dy$ 在 $[a,b]$ 上收敛，$\int_{c}^{+\infty} f_x(x,y) \, dy$ 在 $[a,b]$ 上一致收敛，则 $I(x)$ 在 $[a,b]$ 上可微，且 $I'(x) = \int_{c}^{+\infty} f_x(x,y) \, dy, \quad x \in [a,b]$ |
| 可积性 | (1) 设 $f(x,y)$ 在 $[a,+\infty) \times [c,+\infty)$ 上连续，$\int_{a}^{+\infty} f(x,y) \, dx$ 关于 $y$ 在 $[c,+\infty)$ 上内闭一致收敛，$\int_{c}^{+\infty} f(x,y) \, dy$ 关于 $x$ 在 $[a,+\infty)$ 上内闭一致收敛；两个反常积分 $\int_{a}^{+\infty} \int_{c}^{+\infty} \abs{f(x,y)} \, dy \, dx$，$\int_{c}^{+\infty} \int_{a}^{+\infty} \abs{f(x,y)} \, dx \, dy$ 中如果有一个收敛，则 $\int_{a}^{+\infty} \int_{c}^{+\infty} f(x,y) \, dy \, dx = \int_{c}^{+\infty} \int_{a}^{+\infty} f(x,y) \, dx \, dy$ (2) 设 $f(x,y)$ 在 $[a,b] \times [c,+\infty)$ 上连续，若含参量反常积分在 $[a,b]$ 上一致收敛，则 $I(x)$ 在 $[a,b]$ 上可积，且 $\int_{a}^{b} \int_{c}^{+\infty} f(x,y) \, dy \, dx = \int_{c}^{+\infty} \int_{a}^{b} f(x,y) \, dx \, dy$ |


## 欧拉积分

### 1. 欧拉积分概述

   含参量反常积分：
   $$
   \Gamma(s) = \int_{0}^{+\infty} x^{s-1} e^{-x} \, dx, \, s > 0,
   $$


   $$
   B(p,q) = \int_{0}^{1} x^{p-1} (1-x)^{q-1} \, dx, \, p > 0, q > 0,
   $$
统称为**欧拉积分**。

   其中前者又称为**伽马函数**(或 $\Gamma$ 函数)，后者称为**贝塔函数**(或 $B$ 函数)。

   # 2. 欧拉积分性质

| 名称 | $\Gamma$ 函数 | $B$ 函数 |
| --- | --- | --- |
| 特征 | $\Gamma(s)$ 在定义域 $s > 0$ 内连续且可导 | $B(p,q)$ 在定义域 $p > 0, q > 0$ 内连续 |
| 递推公式 | $\Gamma(s+1) = s\Gamma(s)$ | $B(p,q) = \frac{q-1}{p+q-1} B(p,q-1) (p > 0, q > 1)$<br />$B(p,q) = \frac{p-1}{p+q-1} B(p-1,q) (p > 1, q > 0)$<br />$B(p,q) = \frac{(p-1)(q-1)}{(p+q-1)(p+q-2)} B(p-1,q-1)$<br />$(p > 1, q > 1)$ |
| 其他表达形式 | $\Gamma(s) = \int_{0}^{+\infty} 2y^{2s-1} e^{-x^2} \, dy \\ = p^s \int_{0}^{+\infty} y^{s-1} e^{-px} \, dy \quad (s > 0, p > 0)$ | $B(p,q) = \int_{0}^{\frac{\pi}{2}} 2 \sin^{2p-1} \varphi \cos^{2q-1} \varphi \, d\varphi \\ = \int_{0}^{+\infty} \frac{y^{p-1}}{(1+y)^{p+q}} \, dy \\= \int_{0}^{1} \frac{y^{p-1} + y^{q-1}}{(1+y)^{p+q}} \, dy$ |
| 对称性 | | $B(p,q) = B(q,p)$ |
| 两者关系 | $B(p,q) = \frac{\Gamma(p)\Gamma(q)}{\Gamma(q+p)}, p > 0, q > 0$ |