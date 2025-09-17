# 第二十二章 曲面积分

## §1 第一型曲面积分

定义 1 设 $S$ 是空间中可求面积的曲面，$f(x,y,z)$ 为定义在 $S$ 上的函数。对曲面 $S$ 作分割 $T$，它把 $S$ 分成 $n$ 个小曲面块 $S_i \, (i=1,2,\cdots,n)$，以 $\Delta S_i$ 记小曲面块 $S_i$ 的面积，分割 $T$ 的细度 $\|T\|=\max\limits_{1 \leq i \leq n} |S_i|$ 的直径 $|$。在 $S_i$ 上任取一点 $(\xi_i, \eta_i, \zeta_i) \, (i=1,2,\cdots,n)$，若极限

$$
\lim_{\|T\| \to 0} \sum_{i=1}^n f(\xi_i, \eta_i, \zeta_i) \Delta S_i
$$

存在，且与分割 $T$ 及 $(\xi_i, \eta_i, \zeta_i) \, (i=1,2,\cdots,n)$ 的取法无关，则称此极限为 $f(x,y,z)$ 在 $S$ 上的第一型曲面积分，记作

$$
\iint_S f(x,y,z) \, dS. \quad (1)
$$

于是前面讲到的曲面块的质量可由第一型曲面积分 (1) 求得。

特别地，当 $f(x,y,z) \equiv 1$ 时，曲面积分 $\iint_S dS$ 就是曲面块 $S$ 的面积。

第一型曲面积分的性质完全类似于第一型曲线积分，读者可仿照第二十章 §1 自行写出。

二、第一型曲面积分的计算

第一型曲面积分可化为二重积分来计算。

定理 22.1 设有光滑曲面

$$
S: z = z(x,y), \quad (x,y) \in D,
$$

$f(x,y,z)$ 为 $S$ 上的连续函数，则

$$
\iint_S f(x,y,z) \, dS = \iint_D f(x,y,z(x,y)) \sqrt{1 + z_x^2 + z_y^2} \, dxdy. \quad (2)
$$

## §2 第二型曲面积分


设连通曲面 $S$ 上到处都有连续变动的切平面（或法线），$M$ 为曲面 $S$ 上的一点，曲面在 $M$ 处的法线有两个方向：当取定其中一个指向为正方向时，则另一个指向就是负方向。设 $M_0$ 为 $S$ 上任一点，$L$ 为 $S$ 上任一经过点 $M_0$，且不超出 $S$ 边界的闭曲线。又设 $M$ 为动点，它在 $M_0$ 处与 $M_0$ 有相同的法线方向，且有如下特性：当 $M$ 从 $M_0$ 出发沿 $L$ 连续移动，这时作为曲面上的点 $M$，它的法线方向也连续地变动。最后当 $M$ 沿 $L$ 回到 $M_0$ 时，若这时 $M$ 的法线方向仍与 $M_0$ 的法线方向相一致，则说这曲面 $S$ 是**双侧曲面**；若与 $M_0$ 的法线方向相反，则说 $S$ 是**单侧曲面**。

我们通常碰到的曲面大多是双侧曲面。单侧曲面的一个典型例子是默比乌斯（Möbius）带。它的构造方法如下：取一矩形长纸带 $ABCD$（如图 22-3(a)），将其一端扭转 $180^\circ$ 后与另一端黏合在一起（即让 $A$ 与 $C$ 重合，$B$ 与 $D$ 重合。如图 22-3(b) 所示）。读者可以考察这个带状曲面是单侧的。事实上，可在曲面上任取一条与其边界相平行的闭曲线 $L$，动点 $M$ 从 $L$ 上的点 $M_0$ 出发，其法线方向与 $M_0$ 的法线方向相一致，当 $M$ 沿 $L$ 连续变动一周回到 $M_0$ 时，由图 22-3(b) 看到，这时 $M$ 的法线方向却与 $M_0$ 的法线方向相反。对默比乌斯带还可更简单地说明它的单侧特性，即沿这个带子上任一处出发涂以一种颜色，则可以不越过边界而将它全部涂遍（即把原纸带的两面都涂上同样的颜色）。


通常由 $z=z(x,y)$ 所表示的曲面都是双侧曲面，当以其法线正方向与 $z$ 轴正向的夹角成锐角的一侧（也称为上侧）时，则另一侧（也称下侧）为负侧。当 $S$ 为封闭曲面时，通常规定曲面的外侧为正侧，内侧为负侧。


**定义 1** 设 $P, Q, R$ 为定义在双侧曲面 $S$ 上的函数，在 $S$ 所指定的一侧作分割 $T$，它把 $S$ 分为 $n$ 个小曲面 $S_1, S_2, \cdots, S_n$，分割 $T$ 的细度 $\|T\| = \max\limits_{1 \leq i \leq n} |S_i|$ 的直径 $|$，以 $\Delta S_{i_{xy}}, \Delta S_{i_{yz}}, \Delta S_{i_{zx}}$ 分别表示 $S_i$ 在三个坐标面上的投影区域的面积，它们的符号由 $S_i$ 的方向来确定：若 $S_i$ 的法线正向与 $z$ 轴正向成锐角时，$S_i$ 在 $xy$ 平面的投影区域的面积 $\Delta S_{i_{xy}}$ 为正。反之，若 $S_i$ 法线正向与 $z$ 轴正向成钝角时，它在 $xy$ 平面的投影区域的面积 $\Delta S_{i_{xy}}$ 为负。在各个小曲面 $S_i$ 上任取一点 $(\xi_i, \eta_i, \zeta_i)$。若

$$
\lim_{\|T\| \to 0} \sum_{i=1}^n P(\xi_i, \eta_i, \zeta_i) \Delta S_{i_{yz}} + \lim_{\|T\| \to 0} \sum_{i=1}^n Q(\xi_i, \eta_i, \zeta_i) \Delta S_{i_{zx}} + \lim_{\|T\| \to 0} \sum_{i=1}^n R(\xi_i, \eta_i, \zeta_i) \Delta S_{i_{xy}}
$$

存在，且与曲面 $S$ 的分割 $T$ 和 $(\xi_i, \eta_i, \zeta_i)$ 在 $S_i$ 上的取法无关，则称此极限为函数 $P, Q, R$ 在曲面 $S$ 所指定的一侧上的第二型曲面积分，记作

$$
\iint_S P(x,y,z) \, dydz + \iint_S Q(x,y,z) \, dzdx + \iint_S R(x,y,z) \, dxdy \quad (1)
$$

或

$$
\iint_S P(x,y,z) \, dydz + \iint_S Q(x,y,z) \, dzdx + \iint_S R(x,y,z) \, dxdy.
$$

与第二型曲线积分一样，第二型曲面积分也有如下一些性质：

1. 若 $\iint_S P_i \, dydz + Q_i \, dzdx + R_i \, dxdy \quad (i = 1, 2, \cdots, k)$ 存在，则有

$$
\iint_S \left( \sum_{i=1}^k c_i P_i \right) \, dydz + \left( \sum_{i=1}^k c_i Q_i \right) \, dzdx + \left( \sum_{i=1}^k c_i R_i \right) \, dxdy
$$

$$
= \sum_{i=1}^k c_i \iint_S P_i \, dydz + Q_i \, dzdx + R_i \, dxdy,
$$

其中 $c_i \, (i=1, 2, \cdots, k)$ 是常数。

2. 若曲面 $S$ 是由两两无公共内点的曲面块 $S_1, S_2, \cdots, S_k$ 所组成，且

$$
\iint_{S_i} P \, dydz + Q \, dzdx + R \, dxdy \quad (i = 1, 2, \cdots, k)
$$

存在，则有

$$
\iint_S P \, dydz + Q \, dzdx + R \, dxdy
$$

$$
= \sum_{i=1}^k \iint_{S_i} P \, dydz + Q \, dzdx + R \, dxdy.
$$

**定理 22.2** 设 $R$ 是定义在光滑曲面

$$
S: z = z(x,y), \quad (x,y) \in D_{xy}
$$

上的连续函数，以 $S$ 的上侧为正侧（这时 $S$ 的法线方向与 $z$ 轴正向成锐角），则有

$$
\iint_S R(x,y,z) \, dxdy = \iint_{D_{xy}} R(x,y,z(x,y)) \, dxdy. \quad (2)
$$

**定理 22.3** 设 $S$ 为光滑曲面，正侧法向量为 $(\cos \alpha, \cos \beta, \cos \gamma)$，$P(x,y,z), Q(x,y,z), R(x,y,z)$ 在 $S$ 上连续，则

$$
\iint_S P(x,y,z) \, dydz + Q(x,y,z) \, dzdx + R(x,y,z) \, dxdy
$$

$$
= \iint_S (P(x,y,z) \cos \alpha + Q(x,y,z) \cos \beta + R(x,y,z) \cos \gamma) \, dS.
$$

**定理 22.4** 设 $P, Q, R$ 是定义在光滑曲面 $S: z = z(x,y), (x,y) \in D$ 上的连续函数，以 $S$ 的上侧为正侧，则

$$
\iint_S P(x,y,z) \, dydz + Q(x,y,z) \, dzdx + R(x,y,z) \, dxdy
$$

$$
= \iint_D (P(x,y,z(x,y)) (-z_x) + Q(x,y,z(x,y)) (-z_y) + R(x,y,z(x,y))) \, dxdy.
$$

**定理 22.5 （高斯公式）** 设空间区域 $V$ 由分片光滑的双侧封闭曲面 $S$ 围成。若函数 $P, Q, R$ 在 $V$ 上连续，且有一阶连续偏导数，则

$$
\iiint_V \left( \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} + \frac{\partial R}{\partial z} \right) \, dxdydz
$$

$$
= \iint_S P \, dydz + Q \, dzdx + R \, dxdy \quad \text{①}, \tag{1}
$$

其中 $S$ 取外侧。(1) 式称为高斯公式。

**定理 22.6 （斯托克斯公式）** 设光滑曲面 $S$ 的边界 $L$ 是按段光滑的连续曲线。若函数 $P, Q, R$ 在 $S$（连同 $L$）上连续，且有一阶连续偏导数，则

$$
\iint_S \left( \frac{\partial R}{\partial y} - \frac{\partial Q}{\partial z} \right) \, dydz + \left( \frac{\partial P}{\partial z} - \frac{\partial R}{\partial x} \right) \, dzdx + \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, dxdy
$$

$$
= \oint_L P \, dx + Q \, dy + R \, dz, \tag{2}
$$

其中 $S$ 的侧与 $L$ 的方向按右手法则确定。

**定理 22.7** 设 $\Omega \subset \mathbb{R}^3$ 为空间单连通区域. 若函数 $P, Q, R$ 在 $\Omega$ 上连续, 且有一阶连续偏导数, 则以下四个条件是等价的：

(i) 对于 $\Omega$ 内任一按段光滑的封闭曲线 $L$, 有
$$
\oint_L P \mathrm{d}x + Q \mathrm{d}y + R \mathrm{d}z = 0;
$$

(ii) 对于 $\Omega$ 内任一按段光滑的曲线 $L$, 曲线积分
$$
\int_L P \mathrm{d}x + Q \mathrm{d}y + R \mathrm{d}z
$$
与路线无关;

(iii) $P \mathrm{d}x + Q \mathrm{d}y + R \mathrm{d}z$ 是 $\Omega$ 内某一函数 $u$ 的全微分, 即
$$
\mathrm{d}u = P \mathrm{d}x + Q \mathrm{d}y + R \mathrm{d}z;
$$

(iv) $\frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x}$, $\frac{\partial Q}{\partial z} = \frac{\partial R}{\partial y}$, $\frac{\partial R}{\partial x} = \frac{\partial P}{\partial z}$ 在 $\Omega$ 内处处成立.