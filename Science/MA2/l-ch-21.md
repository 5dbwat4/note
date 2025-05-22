# 第二十一章 重积分

## §1 二重积分的概念

### 一、平面图形的面积

由确界存在定理可以推得，对于平面上所有直线网，数集 $\{ s_p(T) \}$ 有上确界，数集 $\{ S_p(T) \}$ 有下确界，记

$$
\underline{I}_p = \sup_{T} \{ s_p(T) \}, \quad \overline{I}_p = \inf_{T} \{ S_p(T) \}.
$$

显然有

$$
0 \leq \underline{I}_p \leq \overline{I}_p. \tag{1}
$$

通常称 $\underline{I}_p$ 为 $P$ 的**内面积**，$\overline{I}_p$ 为 $P$ 的**外面积**。

**定义 1** 若平面图形 $P$ 的内面积 $\underline{I}_p$ 等于它的外面积 $\overline{I}_p$，则称 $P$ 为可求面积，并称其共同值 $\underline{I}_p = \overline{I}_p = \overline{\underline{I}}_p$ 为 $P$ 的面积。

**定理 21.1** 平面有界图形 $P$ 可求面积的充要条件是：对任给的 $\varepsilon > 0$，总存在直线网 $T$，使得

$$
S_p(T) - s_p(T) < \varepsilon. \hspace{2cm} (2)
$$

推论 平面有界图形 $P$ 的面积为零的充要条件是它的外面积 $\overline{I}_p = 0$，即对任给的 $\varepsilon > 0$，存在直线网 $T$，使得

$$
S_p(T) < \varepsilon,
$$

或对任给的 $\varepsilon > 0$，平面图形 $P$ 能被有限个其面积总和小于 $\varepsilon$ 的小矩形所覆盖。

**定理 21.2** 平面有界图形 $P$ 可求面积的充要条件是：$P$ 的边界 $K$ 的面积为零。

**定理 21.3** 若曲线 $K$ 为定义在 $[a, b]$ 上的连续函数 $f(x)$ 的图像，则曲线 $K$ 的面积为零。

推论 1 参数方程 $x = \varphi(t), y = \psi(t), t \in [\alpha, \beta]$ 所表示的光滑曲线 $K$ 的面积为零。

推论 2 由平面上分段光滑曲线所围成的有界闭区域是可求面积的。

注 1 为简单起见，以下讨论的有界闭区域都是指分段光滑曲线所围成的有界闭区域，从而都是可求面积的。

注 2 并非平面中所有的点集都是可求面积的。例如

$$
D = \{ (x, y) \mid x, y \in \mathbb{Q} \cap [0, 1] \}.
$$

易知 $0 = I_D < \overline{I}_D = 1, D$ 是不可求面积的。

### 二、二重积分的定义及其存在性

设 $D$ 为 $xy$ 平面上可求面积的有界闭区域，$f(x, y)$ 为定义在 $D$ 上的函数。用任意的曲线把 $D$ 分成 $n$ 个可求面积的小区域

$$
\sigma_1, \sigma_2, \cdots, \sigma_n.
$$

以 $\Delta \sigma_i$ 表示小区域 $\sigma_i$ 的面积，这些小区域构成 $D$ 的一个分割 $T$，以 $d_i$ 表示小区域 $\sigma_i$ 的直径，称 $\|T\| = \max_{1 \leq i \leq n} d_i$ 为分割 $T$ 的**细度**。在每个 $\sigma_i$ 上任取一点 $(\xi_i, \eta_i)$，作和式

$$
\sum_{i=1}^{n} f(\xi_i, \eta_i) \Delta \sigma_i.
$$

称它为函数 $f(x, y)$ 在 $D$ 上属于分割 $T$ 的一个**积分和**，$(\xi_i, \eta_i)$ 称为**介点**。

**定义 2** 设 $f(x, y)$ 是定义在可求面积的有界闭区域 $D$ 上的函数。$J$ 是一个确定的数，若对任给的正数 $\varepsilon$，总存在某个正数 $\delta$，使对于 $D$ 的任何分割 $T$，当它的细度 $\|T\| < \delta$ 时，属于 $T$ 的所有积分和都有

$$
\left| \sum_{i=1}^{n} f(\xi_i, \eta_i) \Delta \sigma_i - J \right| < \varepsilon, \hspace{2cm} (4)
$$

则称 $f(x, y)$ 在 $D$ 上可积，数 $J$ 称为函数 $f(x, y)$ 在 $D$ 上的二重积分，记作

$$
J = \iint\limits_{D} f(x, y) \, d\sigma, \hspace{2cm} (5)
$$

其中 $f(x, y)$ 称为二重积分的被积函数，$x, y$ 称为积分变量，$D$ 称为积分区域。

**定理 21.4** $f(x, y)$ 在 $D$ 上可积的充要条件是：

$$
\lim_{\|T\| \to 0} S(T) = \lim_{\|T\| \to 0} s(T).
$$

**定理 21.5** $f(x, y)$ 在 $D$ 上可积的充要条件是：对于任给的正数 $\varepsilon$，存在 $D$ 的某个分割 $T$，使得 $S(T) - s(T) < \varepsilon$。

**定理 21.6** 有界闭区域 $D$ 上的连续函数必可积。

**定理 21.7** 设 $f(x, y)$ 在有界闭域 $D$ 上有界，且其不连续点集 $E$ 是零面积集，则 $f(x, y)$ 在 $D$ 上可积。

### 三、二重积分的性质


二重积分具有一系列与定积分完全相类似的性质，现列举如下。

1. 若 $f(x, y)$ 在区域 $D$ 上可积，$k$ 为常数，则 $kf(x, y)$ 在 $D$ 上也可积，且

$$
\iint\limits_{D} kf(x, y) \, d\sigma = k \iint\limits_{D} f(x, y) \, d\sigma.
$$

2. 若 $f(x, y), g(x, y)$ 在 $D$ 上都可积，则 $f(x, y) \pm g(x, y)$ 在 $D$ 上也可积，且

$$
\iint\limits_{D} [f(x, y) \pm g(x, y)] \, d\sigma = \iint\limits_{D} f(x, y) \, d\sigma \pm \iint\limits_{D} g(x, y) \, d\sigma.
$$

3. 若 $f(x, y)$ 在 $D_1$ 和 $D_2$ 上都可积，且 $D_1$ 与 $D_2$ 无公共内点，则 $f(x, y)$ 在 $D_1 \cup D_2$ 上也可积，且

$$
\iint\limits_{D_1 \cup D_2} f(x, y) \, d\sigma = \iint\limits_{D_1} f(x, y) \, d\sigma + \iint\limits_{D_2} f(x, y) \, d\sigma.
$$

4. 若 $f(x, y)$ 与 $g(x, y)$ 在 $D$ 上可积，且

$$
f(x, y) \leq g(x, y), \quad (x, y) \in D,
$$

则

$$
\iint\limits_{D} f(x, y) \, d\sigma \leq \iint\limits_{D} g(x, y) \, d\sigma.
$$

5. 若 $f(x, y)$ 在 $D$ 上可积，则函数 $|f(x, y)|$ 在 $D$ 上也可积，且

$$
\left| \iint\limits_{D} f(x, y) \, d\sigma \right| \leq \iint\limits_{D} |f(x, y)| \, d\sigma.
$$

6. 若 $f(x, y)$ 在 $D$ 上可积，且

$$
m \leq f(x, y) \leq M, \quad (x, y) \in D,
$$

则

$$
m S_D \leq \iint\limits_{D} f(x, y) \, d\sigma \leq M S_D,
$$

这里 $S_D$ 是积分区域 $D$ 的面积。

7. （中值定理）若 $f(x, y)$ 在有界闭区域 $D$ 上连续，则存在 $(\xi, \eta) \in D$，使得

$$
\iint\limits_{D} f(x, y) \, d\sigma = f(\xi, \eta) S_D,
$$

这里 $S_D$ 是积分区域 $D$ 的面积。

中值定理的几何意义：以 $D$ 为底，$z = f(x, y) \ (f(x, y) \geq 0)$ 为曲顶的曲顶柱体体积等于一个同底的平顶柱体的体积，这个平顶柱体的高等于 $f(x, y)$ 在区域 $D$ 中某点 $(\xi, \eta)$ 的函数值 $f(\xi, \eta)$。


## §2 直角坐标系下二重积分的计算

