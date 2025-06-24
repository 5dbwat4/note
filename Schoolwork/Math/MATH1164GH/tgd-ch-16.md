# 第十六章 多元函数的极限与连续

## 平面点集与多元函数

1. 基本概念

二元函数的基本概念

| 名称 | 定义 | 说明 |
| --- | --- | --- |
| 平面点集 | 坐标平面上满足某种条件 $P$ 的点的集合, 称为平面点集, 并记作 $E = \{(x, y) \mid (x, y) \text{ 满足条件 } P\}$ | 例 $\mathbb{R}^2 = \{(x, y) \mid -\infty < x < +\infty, -\infty < y < +\infty\}$ |
| 二元函数的距离 | 设 $M_1(x_1, y_1), M_2(x_2, y_2)$ 是 $\mathcal{O}xy$ 平面上两点, $M_1$ 与 $M_2$ 的距离记作 $\rho(M_1, M_2) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ | 若 $P_1, P_2, P_3$ 三点有三角不等式 $\rho(P_1, P_2) \leq \rho(P_1, P_3) + \rho(P_2, P_3)$ |
| 直径 | 设点集 $E \subset \mathbb{R}^2$, 定义 $E$ 的直径为 $d(E) = \sup_{P_1, P_2 \in E} \rho(P_1, P_2)$ | $d(E) = +\infty$ 时, 说明 $E$ 为无限集 |
| 邻域 | 在平面 $\mathcal{O}xy$ 上固定一点 $P_0(x_0, y_0)$, 所有与 $P_0$ 的距离小于 $\delta (\delta > 0)$ 的点的集合, 称为点 $P_0$ 的 $\delta$ 邻域, 记作 $U(P_0; \delta)$, 点集 $\{P \mid 0 < d(P, P_0) < \delta\}$ 称为空心邻域, 记作 $U^c(P_0; \delta)$ |  |

点与点集

点集 $E$ 是平面上的集合

| 名称 | 定义 | 说明 |
| --- | --- | --- |
| 内点 | 存在 $P_0$ 的某一邻域 $U(P_0; \delta)$, 使得 $U(P_0; \delta) \subset E$, 则称 $P_0$ 为点集 $E$ 的内点 | $\text{int}E$: 表示 $E$ 的所有内点的集合 |
| 外点 | 存在 $P_1$ 的某一邻域 $U(P_1; \delta)$, 使得 $U(P_1; \delta)$ 没有 $E$ 中的点, 则称 $P_1$ 是点集 $E$ 的外点 |  |
| 边界点 | $P_2$ 的任何邻域中既有 $E$ 中的点, 又有不是 $E$ 中的点, 则称 $P_2$ 是点集 $E$ 的边界点 | $\partial E$: 表示 $E$ 的所有界点的集合 |

区域/集合

| 名称 | 定义 | 说明 |
| --- | --- | --- |
| 开集 | 若点集 $E$ 的所有点都是内点, 则称 $E$ 为开集 | $\text{int}E = E$ |
| 闭集 | 若点集 $E$ 包含它的所有边界点, 则称 $E$ 为闭集 |  |
| 连通集 | 若点集 $E$ 中任意两点都可用一条完全在 $E$ 中的有限折线连接起来, 则称 $E$ 为连通集 |  |
| 区域 | 若点集 $D$ 是连通的开集, 则称 $D$ 为区域; 区域 $D$ 的边界点的全体称为 $D$ 的边界; 区域 $D$ 加上它的边界称为闭区域, 记作 $\overline{D}$ |  |

闭集与开集具有对偶性质——闭集的余集为开集; 开集的余集为闭集. 利用这个性质, 可以通过讨论余集 $E^c$ 的特性, 转而来认识 $E$.

2. 按“疏→密”而论，点 $P_0$ 与点集 $E$ 之间的关系又表现为以下两种情形：

(1) $P_0$ 是 $E$ 的聚点 $\rightarrow \forall \delta > 0$, 必有 $U^c(P_0; \delta) \cap E \neq \emptyset$.

(2) $P_0$ 不是 $E$ 的聚点，$
\left\{
\begin{array}{l}
\text{若 } P_0 \notin E, \text{则 } P_0 \text{ 必为 } E \text{ 的外点} \\
\text{若 } P_0 \in E, \text{则 } P_0 \text{ 为 } E \text{ 的孤立点}
\end{array}
\right.
$

孤立点即为 $\exists \delta > 0$, 使 $U(P_0; \delta) \cap E = \{P_0\}$,
$P_0$ 是 $E$ 的聚点的充要条件: 存在一个各项互异的点列 $\{P_k\} \subset E$, 使 $\lim_{k \to \infty} P_k = P_0$。
$E$ 的所有聚点组成的集合称为 $E$ 的导集, 记为 $E'$, 又称 $\bar{E} = E \cup E'$ 为 $E$ 的闭包。

3. $\mathbb{R}^2$ 上的完备性定理

| 名称 | 内容 |
| --- | --- |
| 柯西收敛定理 | 设 $\{P_n\} \subset \mathbb{R}^2$ 为一点列, $\{P_n\}$ 收敛的充要条件是: $\{P_n\}$ 为一基列(或柯西列), 亦即 $\forall \varepsilon > 0$, $\exists N \in \mathbb{N}$, 当 $n > N$ 时, 对一切 $p \in \mathbb{N}$, 都有 $\rho(P_n, P_{n+p}) < \varepsilon$ |
| 闭域套(闭集套)定理 | 设 $D_k \subset \mathbb{R}^2, k = 1, 2, \cdots$ 是一列闭域(或闭集), 它满足 ①$D_k \supset D_{k+1}, k = 1, 2, \cdots$; ②$d_k = d(D_k) \to 0, k \to \infty$, 则存在唯一一点 $P_0 \in D_k, k = 1, 2, \cdots$ |
| 聚点定理 | 设 $E \subset \mathbb{R}^2$ 为任一有界无穷点集, 则 $E$ 在 $\mathbb{R}^2$ 中至少有一个聚点 |
| 推论1 | 设 $\{P_k\} \subset \mathbb{R}^2$ 为一有界点列, 则它必存在收敛子列 $\{P_{p_j}\}$, 并称该子列的极限 $\lim_{j \to \infty} P_{p_j} = P_0$ 为点列 $\{P_k\}$ 的一个聚点 |
| 推论2 | $E \subset \mathbb{R}^2$ 为有界闭集的充要条件是: $E$ 的任一无穷子集必有聚点 |
| 推论3 | $E \subset \mathbb{R}^2$ 为有界闭集的充要条件是: $E$ 为一列子集(即 $E$ 的任一无穷子集必有聚点, 且聚点都属于 $E$) |
| 有限覆盖定理 | 设 $E \subset \mathbb{R}^2$ 为一有界闭集, $\Delta = \{\Delta_\alpha\}$ 为 $\mathbb{R}^2$ 中的一族开集; 若 $\Delta$ 覆盖了 $E$(即 $E \subset \bigcup_\alpha \Delta_\alpha$), 则在 $\Delta$ 中必能选出有限个开集 $\Delta_1, \Delta_2, \cdots, \Delta_m$, 它们能覆盖 $E$ |

## 二元函数的极限

1. 极限的定义

设 $D \subset \mathbb{R}^2, f(x)$ 在 $D$ 上有定义, $P_0(x_0, y_0)$ 为 $D$ 的一个聚点, $A$ 为一确定的实数. 若 $\forall \varepsilon > 0, \exists \delta > 0$, 使得有 $|f(P) - A| < \varepsilon, \forall P \in U^c(P_0; \delta) \cap D$, 则称 $f(x)$ 在 $D$ 上当 $P \to P_0$ 时, 以 $A$ 为极限, 记作 $\lim_{P \to P_0} f(P) = A$.

在对于 $P \in D$ 不致产生误解时, 也可简单地写作 $\lim_{P \to P_0} f(P) = A$.

当 $P, P_0$ 分别用坐标 $(x, y), (x_0, y_0)$ 表示时, 也常写作 $\lim_{(x, y) \to (x_0, y_0)} f(x, y) = A$.

2. 极限的充要条件

(1) $\forall V \in D, P_0$ 始终为 $E$ 的聚点, 则有 $\lim_{P \to P_0} f(P) = A \Leftrightarrow \lim_{P \to P_0} f(P) = A$.

(2) 极限 $\lim_{P \to P_0} f(P)$ 存在的充要条件是: 对于 $D$ 中任一满足条件 $P_n \neq P_0$, 且 $\lim_{n \to \infty} P_n = P_0$ 的点列 $\{P_n\}$, 它所对应的函数列 $\{f(P_n)\}$ 都收敛.

3. 广义极限

$\lim_{P \to P_0} f(P) = +\infty (\text{或 } -\infty)$ 的定义: $P_0$ 为 $D$ 的聚点, $\forall M > 0, \exists \delta > 0$, 当 $P \in U^c(P_0; \delta) \cap D$ 时, 满足 $f(P) > M \ [f(P) < -M \ \text{或} \ |f(P)| > M]$.

4. 累次极限

$\lim_{y \to y_0} \lim_{x \to x_0} f(x, y) = L$ 的意义是: 设 $D = E_x \times E_y$, 对每个 $y \in E_y (y \neq y_0)$, 有
$$
\begin{cases}
\lim_{x \to x_0} f(x, y) = \varphi(y) \\
\lim_{y \to y_0} \varphi(y) = L
\end{cases}
$$
同理 $\lim_{x \to x_0} \lim_{y \to y_0} f(x, y) = K$ 的定义为
$$
\begin{cases}
\lim_{y \to y_0} f(x, y) = \varphi(x) \\
\lim_{x \to x_0} \varphi(x) = K
\end{cases}
$$

5. 重极限

重极限的形式为 $\lim_{(x, y) \to (x_0, y_0)} f(x, y) = A$ (两个自变量 $x, y$ 同时以任何方式趋于 $x_0, y_0$).

重极限与累次极限的关系

(1) 定理 若 $f(x, y)$ 在点 $(x_0, y_0)$ 存在重极限 $\lim_{(x, y) \to (x_0, y_0)} f(x, y)$ 和累次极限 $\lim_{x \to x_0} \lim_{y \to y_0} f(x, y)$, $\lim_{y \to y_0} \lim_{x \to x_0} f(x, y)$, 则它们必相等.

(2) 推论 1 若累次极限 $\lim_{x \to x_0} \lim_{y \to y_0} f(x, y)$, $\lim_{y \to y_0} \lim_{x \to x_0} f(x, y)$ 和重极限 $\lim_{(x, y) \to (x_0, y_0)} f(x, y)$ 都存在, 则三者相等.

(3) 推论 2 若累次极限 $\lim_{x \to x_0} \lim_{y \to y_0} f(x, y)$ 与 $\lim_{y \to y_0} \lim_{x \to x_0} f(x, y)$ 存在但不相等, 则重极限 $\lim_{(x, y) \to (x_0, y_0)} f(x, y)$ 必不存在.

小提示: 二次极限（累次极限）与二重极限（重极限）没有什么必然的联系. 虽然, 二次极限存在与否和二重极限存在与否没有一定的关系, 但在某些条件下, 它们之间会有一些联系. 若 $f(x, y)$ 在点 $(x_0, y_0)$ 存在极限 $\lim_{(x, y) \to (x_0, y_0)} f(x, y)$ 与累次极限 $\lim_{x \to x_0} \lim_{y \to y_0} f(x, y)$, 则它们必相等. 这就是累次极限存在的价值.


## 二元函数的连续性

1. 基本概念

| 名称 | 定义 | 说明 |
| --- | --- | --- |
| 介值性定理 | 设函数 $f$ 在区域 $D \subset \mathbb{R}^2$ 上连续, 若 $P_1, P_2$ 为 $D$ 中任意两点, 且 $f(P_1) < f(P_2)$, 则对任何满足不等式 $f(P_1) < \mu < f(P_2)$ 的实数 $\mu$, 必存在点 $P_0 \in D$, 使得 $f(P_0) = \mu$. |  |
| 连续 | (1) 设 $f(x)$ 为定义在点集 $D \subset \mathbb{R}^2$ 上的二元函数, $P_0 \in D$ (它或者是 $D$ 的聚点, 或是 $D$ 的孤立点). 对于任给的正数 $\varepsilon$, 总存在相应的正数 $\delta$, 只要 $P \in U(P_0; \delta) \cap D$, 就有 $\left\|f(P) - f(P_0)\right\| < \varepsilon$, 则称 $f(x)$ 关于集合 $D$ 在点 $P_0$ 连续; <br/> (2) 若 $f(x)$ 在 $D$ 上的任何点关于集合 $D$ 连续, 则称 $f(x)$ 为 $D$ 上的连续函数. 若 $P_0$ 是 $D$ 的聚点, 而 $\lim_{P \to P_0} f(P) = f(P_0)$ 不成立, 则称 $P_0$ 是 $f(x)$ 的一个间断点(或不连续点). 间断点包括以下两种情形: 间断点 (1) 若 $\lim_{P \to P_0} f(P)$ 极限不存在, 则称 $P_0$ 为 $f(x)$ 关于集合 $D$ 的一个本性间断点. (2) 若极限存在但不等于 $f(P_0)$, [或 $f(x)$ 在 $P_0$ 没有定义], 则称 $P_0$ 为 $f(x)$ 关于集合 $D$ 的一个可去间断点. | (1) 若 $P_0$ 是 $D$ 的孤立点, 则 $P_0$ 恒为 $f$ 关于集合 $D$ 的连续点, 或是 $D$ 的孤立点. 对于任给的正数 $\varepsilon$, 只要 $P \in U(P_0; \delta) \cap D$, 就有 $\|f(P) - f(P_0)\| < \varepsilon$, 则称 $f(x)$ 关于集合 $D$ 在点 $P_0$ 连续; (2) 若 $P_0$ 是 $D$ 的聚点, 则等价于 $\lim_{P \to P_0} f(P) = f(P_0)$ |
| 全增量 | 设 $P_0(x_0, y_0), P(x, y) \in D; \Delta x = x - x_0, \Delta y = y - y_0$, 则称 $\Delta z = \Delta f(x_0, y_0) = f(x, y) - f(x_0, y_0) = f(x_0 + \Delta x, y_0 + \Delta y) - f(x_0, y_0)$ 为函数 $f(x)$ 在 $P_0$ 的全增量 | (1) $\lim_{\Delta x \to 0} \Delta z f(x_0, y_0) = 0$, 表示 $f(x, y_0)$ 在 $x_0$ 连续. (2) $\lim_{\Delta y \to 0} \Delta f(x_0, y_0) = 0$, 表示 $f(x_0, y)$ 在 $y_0$ 连续. (3) 一般来说, 全增量不等于两个偏增量之和 |
| 偏增量 | 如果全增量中取 $\Delta x = 0$ 或 $\Delta y = 0$, 则相应的函数增量称为偏增量, 记作 $\Delta_x f(x_0, y_0) = f(x_0 + \Delta x, y_0) - f(x_0, y_0)$ $\Delta_y f(x_0, y_0) = f(x_0, y_0 + \Delta y) - f(x_0, y_0)$ |  |

2. 定理（复合函数的连续性）

设函数 $u = \varphi(x, y)$ 和 $v = \phi(x, y)$ 在 $xy$ 平面上点 $P_0(x_0, y_0)$ 的某邻域内有定义, 并在点 $P_0$ 连续; 函数 $f(u, v)$ 在 $uv$ 平面上点 $Q_0(u_0, v_0)$ 的某邻域内有定义, 并在点 $Q_0$ 连续, 其中 $u_0 = \varphi(x_0, y_0)$, $v_0 = \phi(x_0, y_0)$, 则复合函数 $g(x, y) = f(\varphi(x, y), \phi(x, y))$ 在点 $P_0$ 也连续.

3. 有界闭域上连续函数的性质（设 $D \subset \mathbb{R}^2$ 为有界闭域, $f$ 在 $D$ 上连续）

| 名称 | 内容 | 内容 |
| --- | --- | --- |
| 有界性 | $\forall P \in D, \exists M > 0$, 使 $|f(P)| \leq M$ |  |
| 最大值、最小值 | $f(x)$ 在 $D$ 上能取得最大值和最小值, 即 $\exists P_1, P_2 \in D$, 使 $f(P_1) = \max_{P \in D} f(P), f(P_2) = \min_{P \in D} f(P)$ |  |
| 一致连续性 | $f(x)$ 在 $D$ 上必一致连续; 即 $\forall \varepsilon > 0, \exists \delta > 0$, 使一切 $P', P'' \in D$, 只要 $\rho(P', P'') < \delta$, 就有 $\|f(P') - f(P'')\| < \varepsilon$ |  |
| 介值性 | $\forall P_1, P_2 \in D$, 若 $f(P_1) < f(P_2)$, 则 $f$ 在 $D$ 内必能取得介于 $f(P_1)$ 与 $f(P_2)$ 之间的一切值, 即 $\forall \mu$ 满足 $f(P_1) < \mu < f(P_2)$, $\exists P_0 \in D$, 使 $f(P_0) = \mu$ |  |
