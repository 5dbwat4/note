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

**定理 21.8** 设 $f(x,y)$ 在矩形区域 $D = [a,b] \times [c,d]$ 上可积，且对每个 $x \in [a,b]$，积分 $\int_{c}^{d} f(x,y) \, dy$ 存在，则累次积分

$$
\int_{a}^{b} \int_{c}^{d} f(x,y) \, dy \, dx
$$

也存在，且

$$
\iint_{D} f(x,y) \, d\sigma = \int_{a}^{b} \int_{c}^{d} f(x,y) \, dy \, dx. \tag{1}
$$

**定理 21.9** 设 $f(x,y)$ 在矩形区域 $D = [a,b] \times [c,d]$ 上可积，且对每个 $y \in [c,d]$，积分 $\int_{a}^{b} f(x,y) \, dx$ 存在，则累次积分

$$
\int_{c}^{d} \int_{a}^{b} f(x,y) \, dx \, dy
$$

也存在，且

$$
\iint_{D} f(x,y) \, d\sigma = \int_{c}^{d} \int_{a}^{b} f(x,y) \, dx \, dy.
$$

称平面点集

$$
D = \{(x,y) \mid y_1(x) \leq y \leq y_2(x), a \leq x \leq b\} \tag{4}
$$

为 **$x$ 型区域**；称平面点集

$$
D = \{(x,y) \mid x_1(y) \leq x \leq x_2(y), c \leq y \leq d\} \tag{5}
$$

为 **$y$ 型区域**。

**定理 21.10** 若 $f(x,y)$ 在如(4)式所示的 $x$ 型区域 $D$ 上连续，其中 $y_1(x), y_2(x)$ 在 $[a,b]$ 上连续，则

$$
\iint_D f(x,y) \, d\sigma = \int_a^b dx \int_{y_1(x)}^{y_2(x)} f(x,y) \, dy.
$$

即二重积分可化为先对 $y$ 后对 $x$ 的累次积分。


## §3 格林公式·曲线积分与路线的无关性

**定理 21.11** 若函数 $P(x,y), Q(x,y)$ 在闭区域 $D$ 上连续，且有连续的一阶偏导数，则有

$$
\iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, d\sigma = \oint_L P \, dx + Q \, dy, \tag{1}
$$

这里 $L$ 为区域 $D$ 的边界曲线，分段光滑，并取正方向。

公式(1)称为**格林(Green)公式**。

若对于平面区域 $D$ 上任一封闭曲线，皆可不经过 $D$ 以外的点而连续收缩于属于 $D$ 的某一点，则称此平面区域为**单连通区域**，否则称为**复连通区域**。如图21-17中，$D_1$ 与 $D_2$ 是单连通区域，而 $D_3$ 与 $D_4$ 则是复连通区域。单连通区域也可以这样叙述：$D$ 内任一封闭曲线所围成的区域内只含有 $D$ 中的点。更通俗地说，单连通区域是没有“洞”的区域，复连通区域是有“洞”的区域。

**定理 21.12** 设 $D$ 是单连通闭区域，若函数 $P(x,y), Q(x,y)$ 在 $D$ 内连续，且具有一阶连续偏导数，则以下四个条件等价：

(i) 沿 $D$ 内任一按段光滑封闭曲线 $L$，有
$$
\oint_L P \, dx + Q \, dy = 0;
$$

(ii) 对 $D$ 中任一按段光滑曲线 $L$，曲线积分
$$
\int_L P \, dx + Q \, dy
$$
与路线无关，只与 $L$ 的起点及终点有关；

(iii) $P \, dx + Q \, dy$ 是 $D$ 内某一函数 $u(x,y)$ 的全微分，即在 $D$ 内有
$$
du = P \, dx + Q \, dy;
$$

(iv) 在 $D$ 内处处成立
$$
\frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x}.
$$


## §4 二重积分的变量变换

引理 设变换 $T: x = x(u,v), y = y(u,v)$ 将 $uv$ 平面上由按段光滑封闭曲线所围的闭区域 $\Delta$ 一对一地映成 $xy$ 平面上的闭区域 $D$，函数 $x(u,v), y(u,v)$ 在 $\Delta$ 内分别具有一阶连续偏导数且它们的函数行列式

$$
J(u,v) = \frac{\partial(x,y)}{\partial(u,v)} \neq 0, \quad (u,v) \in \Delta,
$$

则区域 $D$ 的面积

$$
\mu(D) = \iint_\Delta \left| J(u,v) \right| \, dudv. \tag{5}
$$

**定理 21.13** 设 $f(x,y)$ 在有界闭区域 $D$ 上可积，变换 $T: x = x(u,v), y = y(u,v)$ 将 $uv$ 平面由按段光滑封闭曲线所围成的闭区域 $\Delta$ 一对一地映成 $xy$ 平面上的闭区域 $D$，函数 $x(u,v), y(u,v)$ 在 $\Delta$ 内分别具有一阶连续偏导数且它们的函数行列式

$$
J(u,v) = \frac{\partial(x,y)}{\partial(u,v)} \neq 0, \quad (u,v) \in \Delta,
$$

则

$$
\iint_D f(x,y) \, dxdy = \iint_\Delta f(x(u,v), y(u,v)) \left| J(u,v) \right| \, dudv.
$$

当积分区域是圆域或圆域的一部分，或者被积函数的形式为 $f(x^2+y^2)$ 时，采用极坐标变换

$$
T: \begin{cases} 
x = r \cos \theta, & 0 \leq r < +\infty, 0 \leq \theta \leq 2\pi \\
y = r \sin \theta, 
\end{cases} \tag{8}
$$

往往能达到简化积分区域或被积函数的目的。此时，变换 $T$ 的函数行列式为

$$
J(r,\theta) = \left| \begin{array}{cc}
\cos \theta & -r \sin \theta \\
\sin \theta & r \cos \theta
\end{array} \right| = r.
$$

定理 21.14 设 $f(x,y)$ 满足定理 21.13 的条件，且在极坐标变换 (8) 下，$xy$ 平面上有界闭区域 $D$ 与 $r\theta$ 平面上区域 $\Delta$ 对应，则成立

$$
\iint_D f(x,y) \, dxdy = \iint_\Delta f(r \cos \theta, r \sin \theta) \, r \, drd\theta. \quad (9)
$$


## §5 三重积分


设 $f(x,y,z)$ 是定义在三维空间**可求体积**的有界闭区域 $V$ 上的有界函数。现用若干光滑曲面所组成的曲面网 $T$ 来分割 $V$，它把 $V$ 分成 $n$ 个小区域 $V_1, V_2, \cdots, V_n$。记 $V_i$ 的体积为 $\Delta V_i (i=1,2,\cdots,n)$，$\|T\| = \max\limits_{1 \leq i \leq n} |V_i|$ 的直径 $|$。在每个 $V_i$ 中任取一点 $(\xi_i, \eta_i, \zeta_i)$，作积分和

$$
\sum_{i=1}^n f(\xi_i, \eta_i, \zeta_i) \Delta V_i.
$$

**定义 1** 设 $f(x,y,z)$ 为定义在三维空间可求体积的有界闭区域 $V$ 上的函数，$J$ 是一个确定的数。若对任给的正数 $\varepsilon$，总存在某一正数 $\delta$，使得对于 $V$ 的任何分割 $T$，只要 $\|T\| < \delta$，属于分割 $T$ 的所有积分和都有

$$
\left| \sum_{i=1}^n f(\xi_i, \eta_i, \zeta_i) \Delta V_i - J \right| < \varepsilon,
$$

则称 $f(x,y,z)$ 在 $V$ 上**可积**，数 $J$ 称为函数 $f(x,y,z)$ 在 $V$ 上的**三重积分**，记作

$$
J = \iiint_V f(x,y,z) \, dV \quad \text{或} \quad J = \iiint_V f(x,y,z) \, dxdydz,
$$

其中 $f(x,y,z)$ 称为**被积函数**，$x,y,z$ 称为**积分变量**，$V$ 称为**积分区域**。

当 $f(x,y,z) \equiv 1$ 时，$\iiint_V dV$ 在几何上表示 $V$ 的体积。

三重积分具有与二重积分相应的可积条件和有关性质（参见 §1），这里不一一细述了。例如，类似于二重积分，有

(i) 有界闭区域 $V$ 上的连续函数必可积；

(ii) 如果有界闭区域 $V$ 上的有界函数 $f(x,y,z)$ 的间断点集中在有限多个零体积（可类似于零面积那样来定义）的曲面上，则 $f(x,y,z)$ 在 $V$ 上必可积。

二、化三重积分为累次积分

**定理 21.15** 若函数 $f(x,y,z)$ 在长方体 $V=[a,b] \times [c,d] \times [e,h]$ 上的三重积分存在，且对任意 $(x,y) \in D=[a,b] \times [c,d]$，$g(x,y) = \int_e^h f(x,y,z) \, dz$ 存在，则积分 $\iint_D g(x,y) \, dxdy$ 也存在，且

$$
\iiint_V f(x,y,z) \, dxdydz = \iint_D dxdy \int_e^h f(x,y,z) \, dz. \tag{1}
$$

**推论** 若 $V=\{(x,y,z) \mid (x,y) \in D, z_1(x,y) \leq z \leq z_2(x,y)\} \subset [a,b] \times [c,d] \times [e,h]$，其中 $D$ 为 $V$ 在 $Oxy$ 平面上的投影，$z_1(x,y), z_2(x,y)$ 是 $D$ 上的连续函数，函数 $f(x,y,z)$ 在 $V$ 上的三重积分存在，且对任意 $(x,y) \in D$，

$$
G(x,y) = \int_{z_1(x,y)}^{z_2(x,y)} f(x,y,z) \, dz
$$

亦存在，则积分 $\iint_D G(x,y) \, dxdy$ 存在，且

$$
\iiint_V f(x,y,z) \, dxdydz = \iint_D G(x,y) \, dxdy = \iint_D dxdy \int_{z_1(x,y)}^{z_2(x,y)} f(x,y,z) \, dz. \quad (3)
$$

**定理 21.16** 若函数 $f(x,y,z)$ 在长方体 $V=[a,b] \times [c,d] \times [e,h]$ 上的三重积分存在，且对任何 $z \in [e,h]$，二重积分

$$
I(z) = \iint_D f(x,y,z) \, dxdy
$$

存在，其中 $D=[a,b] \times [c,d]$，则积分

$$
\int_e^h dz \iint_D f(x,y,z) \, dxdy
$$

也存在，且

$$
\iiint_V f(x,y,z) \, dxdydz = \int_e^h dz \iint_D f(x,y,z) \, dxdy.
$$

**推论** 若 $V \subset [a,b] \times [c,d] \times [e,h]$，函数 $f(x,y,z)$ 在 $V$ 上的三重积分存在，且对任意固定的 $z \in [e,h]$，积分 $\varphi(z) = \iint_{D_z} f(x,y,z) \, dxdy$ 存在，其中 $D_z$ 是截面 $\{(x,y) \mid (x,y,z) \in V\}$，则 $\int_e^h \varphi(z) \, dz$ 存在，且

$$
\iiint_V f(x,y,z) \, dxdydz = \int_e^h \varphi(z) \, dz = \int_e^h dz \iint_{D_z} f(x,y,z) \, dxdy.
$$