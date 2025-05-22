# 第十七章 多元函数微分学

## §1 可 微 性

### 一、可微性与全微分

定义 1 设函数 $z = f(x, y)$ 在点 $P_0(x_0, y_0)$ 的某邻域 $U(P_0)$ 上有定义，对于 $U(P_0)$ 中的点 $P(x, y) = (x_0 + \Delta x, y_0 + \Delta y)$，若函数 $f$ 在点 $P_0$ 处的全增量 $\Delta z$ 可表示为

$$
\begin{aligned}
\Delta z = f(x_0 + \Delta x, y_0 + \Delta y) - f(x_0, y_0) \\
= A \Delta x + B \Delta y + o(\rho),\tag{1}
\end{aligned}
$$ 

其中 $A, B$ 是仅与点 $P_0$ 有关的常数，$\rho = \sqrt{\Delta x^2 + \Delta y^2}$，$o(\rho)$ 是较 $\rho$ 高阶的无穷小量，则称函数 $f$ 在点 $P_0$ 可微。并称(1)式中关于 $\Delta x, \Delta y$ 的线性函数 $A \Delta x + B \Delta y$ 为函数 $f$ 在点 $P_0$ 的全微分，记作

$$
dz \big|_{P_0} = df(x_0, y_0) = A \Delta x + B \Delta y.\tag{2}
$$ 

由(1)，(2)可见 $dz$ 是 $\Delta z$ 的线性主部，特别当 $|\Delta x|$，$|\Delta y|$ 充分小时，全微分 $dz$ 可作为全增量 $\Delta z$ 的近似值，即

$$
f(x, y) \approx f(x_0, y_0) + A(x - x_0) + B(y - y_0).\tag{3}
$$

在使用上，有时也把(1)式写成如下形式：

$$
\Delta z = A \Delta x + B \Delta y + \alpha \Delta x + \beta \Delta y,\tag{4}
$$

这里

$$
\lim_{(\Delta x, \Delta y) \to (0, 0)} \alpha = \lim_{(\Delta x, \Delta y) \to (0, 0)} \beta = 0.
$$

### 二、偏导数

**定义 2** 设函数 $z = f(x, y), (x, y) \in D$。若 $(x_0, y_0) \in D$，且 $f(x, y_0)$ 在 $x_0$ 的某邻域内有定义，则当极限

$$
\lim_{\Delta x \to 0} \frac{\Delta_x f(x_0, y_0)}{\Delta x} = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x, y_0) - f(x_0, y_0)}{\Delta x}
$$ 

存在时，称这个极限为函数 $f$ 在点 $(x_0, y_0)$ 关于 $x$ 的偏导数，记作

$$
f_x(x_0, y_0) \text{ 或 } z_x(x_0, y_0), \quad \left. \frac{\partial f}{\partial x} \right|_{(x_0, y_0)}, \quad \left. \frac{\partial z}{\partial x} \right|_{(x_0, y_0)}.
$$

同样定义 $f$ 在点 $(x_0, y_0)$ 关于 $y$ 的偏导数 $f_y(x_0, y_0)$ 或 $\left. \frac{\partial f}{\partial y} \right|_{(x_0, y_0)}$。

注 1 这里符号 $\frac{\partial}{\partial x}, \frac{\partial}{\partial y}$ 专用于偏导数算符，与一元函数的导数符号 $\frac{d}{dx}$ 相仿，但又有差别。

注 2 在上述定义中，$f$ 在点 $(x_0, y_0)$ 存在关于 $x$（或 $y$）的偏导数，$f$ 至少在 $\{(x, y) | y = y_0, |x - x_0| < \delta\}$（或 $\{(x, y) | x = x_0, |y - y_0| < \delta\}$）上必须有定义。

若函数 $z = f(x, y)$ 在区域 $D$ 上每一点 $(x, y)$ 都存在对 $x$（或对 $y$）的偏导数，则得到函数 $z = f(x, y)$ 在区域 $D$ 上对 $x$（或对 $y)）的偏导函数（也简称偏导数），记作

$$
f_x(x, y) \text{ 或 } \frac{\partial f(x, y)}{\partial x} \quad \left( f_y(x, y) \text{ 或 } \frac{\partial f(x, y)}{\partial y} \right),
$$

也可简单地写作 $f_x, z_x$ 或 $\frac{\partial f}{\partial x}, \frac{\partial z}{\partial x} \left( f_y, z_y \text{ 或 } \frac{\partial f}{\partial y}, \frac{\partial z}{\partial y} \right)$。

### 三、可微性条件

**定理 17.1（可微的必要条件）** 若二元函数 $f$ 在其定义域内一点 $(x_0, y_0)$ 可微，则 $f$ 在该点关于每个自变量的偏导数都存在，且(1)式中的

$$
A = f_x(x_0, y_0), \quad B = f_y(x_0, y_0).
$$

因此，函数 $f$ 在点 $(x_0, y_0)$ 的全微分(2) 可惟一地表示为

$$
df \big|_{(x_0, y_0)} = f_x(x_0, y_0) \cdot \Delta x + f_y(x_0, y_0) \cdot \Delta y.
$$

与一元函数的情况一样，由于自变量的增量等于自变量的微分，即

$$
\Delta x = dx, \quad \Delta y = dy,
$$

所以 $f$ 在点 $(x_0, y_0)$ 的全微分又可写为

$$
dz = f_x(x_0, y_0) dx + f_y(x_0, y_0) dy.
$$

若函数 $f$ 在区域 $D$ 上每一点 $(x, y)$ 都可微，则称函数 $f$ 在区域 $D$ 上可微，且 $f$ 在 $D$ 上全微分为

$$
df(x, y) = f_x(x, y) dx + f_y(x, y) dy.
$$

**定理 17.2**（可微的充分条件） 若函数 $z = f(x, y)$ 的偏导数在点 $(x_0, y_0)$ 的某邻域内存在，且 $f_x$ 与 $f_y$ 在点 $(x_0, y_0)$ 连续，则函数 $f$ 在点 $(x_0, y_0)$ 可微。

注 偏导数连续并不是函数可微的必要条件，如函数

$$
f(x, y) = \begin{cases} 
(x^2 + y^2) \sin \frac{1}{\sqrt{x^2 + y^2}}, & x^2 + y^2 \neq 0, \\
0, & x^2 + y^2 = 0 
\end{cases}
$$

在原点 $(0, 0)$ 可微，但 $f_x$ 与 $f_y$ 却在点 $(0, 0)$ 不连续（见本节习题 7）。若 $z = f(x, y)$ 在点 $(x_0, y_0)$ 的偏导数 $f_x, f_y$ 连续，则称 $f$ 在点 $(x_0, y_0)$ 连续可微。

**定理 17.3** 设函数 $f$ 在点 $(x_0, y_0)$ 的某邻域内存在偏导数，若 $(x, y)$ 属于该邻域，则存在 $\xi = x_0 + \theta_1(x - x_0)$ 和 $\eta = y_0 + \theta_2(y - y_0), 0 < \theta_1, \theta_2 < 1$，使得

$$
f(x, y) - f(x_0, y_0) = f_x(\xi, y)(x - x_0) + f_y(x_0, \eta)(y - y_0).
$$ 

### 四、可微性几何意义及应用

定义 3 设 $P$ 是曲面 $S$ 上一点，$\Pi$ 为通过点 $P$ 的一个平面，曲面 $S$ 上的动点 $Q$ 到定点 $P$ 和到平面 $\Pi$ 的距离分别为 $d$ 与 $h$（图 17-3）。若当 $Q$ 在 $S$ 上以任何方式趋近于 $P$ 时，恒有 $\frac{h}{d} \to 0$，则称平面 $\Pi$ 为曲面 $S$ 在点 $P$ 处的切平面，$P$ 为切点。

定理 17.4 曲面 $z = f(x, y)$ 在点 $P(x_0, y_0, f(x_0, y_0))$ 存在不平行于 $z$ 轴的切平面 $\Pi$ 的充要条件是函数 $f$ 在点 $P_0(x_0, y_0)$ 可微。


## §2 复合函数微分法


### 一、复合函数的求导法则

设函数

$$
x = \varphi(s, t) \quad \text{与} \quad y = \psi(s, t)\tag{1}
$$

定义在 $st$ 平面的区域 $D$ 上，函数

$$
z = f(x, y)\tag{2}
$$

定义在 $xy$ 平面的区域 $D_1$ 上，且

$$
\{ (x, y) \mid x = \varphi(s, t), y = \psi(s, t), (s, t) \in D \} \subset D_1,
$$


则函数

$$
z = F(s, t) = f(\varphi(s, t), \psi(s, t))
$$

是以(2) 为外函数、(1) 为内函数的复合函数。其中 $x, y$ 称为函数 $F$ 的中间变量，$s, t$ 为 $F$ 的自变量。

定理 17.5 若函数 $x = \varphi(s, t), y = \psi(s, t)$ 在点 $(s, t) \in D$ 可微，$z = f(x, y)$ 在点 $(x, y) = (\varphi(s, t), \psi(s, t))$ 可微，则复合函数

$$
z = f(\varphi(s, t), \psi(s, t))
$$


在点 $(s, t)$ 可微，且它关于 $s$ 与 $t$ 的偏导数分别为

$$
\left. \frac{\partial z}{\partial s} \right|_{(s, t)} = \frac{\partial z}{\partial x} \bigg|_{(x, y)} \cdot \frac{\partial x}{\partial s} \bigg|_{(s, t)} + \frac{\partial z}{\partial y} \bigg|_{(x, y)} \cdot \frac{\partial y}{\partial s} \bigg|_{(s, t)},
$$

$$
\left. \frac{\partial z}{\partial t} \right|_{(s, t)} = \frac{\partial z}{\partial x} \bigg|_{(x, y)} \cdot \frac{\partial x}{\partial t} \bigg|_{(s, t)} + \frac{\partial z}{\partial y} \bigg|_{(x, y)} \cdot \frac{\partial y}{\partial t} \bigg|_{(s, t)}.
$$


### 二、复合函数的全微分

若以 $x$ 和 $y$ 为自变量的函数 $z = f(x, y)$ 可微，则其全微分为

$$
dz = \frac{\partial z}{\partial x} dx + \frac{\partial z}{\partial y} dy.
$$
 \hspace{1cm} (11)

如果 $x, y$ 作为中间变量又是自变量 $s, t$ 的可微函数

$$
x = \varphi(s, t), \quad y = \psi(s, t),
$$


则由定理 17.5 知道，复合函数 $z = f(\varphi(s, t), \psi(s, t))$ 是可微的，其全微分为

$$
dz = \frac{\partial z}{\partial s} ds + \frac{\partial z}{\partial t} dt
$$


$$
= \left( \frac{\partial z}{\partial x} \frac{\partial x}{\partial s} + \frac{\partial z}{\partial y} \frac{\partial y}{\partial s} \right) ds + \left( \frac{\partial z}{\partial x} \frac{\partial x}{\partial t} + \frac{\partial z}{\partial y} \frac{\partial y}{\partial t} \right) dt
$$
 \hspace{1cm} (12)

$$
= \frac{\partial z}{\partial x} \left( \frac{\partial x}{\partial s} ds + \frac{\partial x}{\partial t} dt \right) + \frac{\partial z}{\partial y} \left( \frac{\partial y}{\partial s} ds + \frac{\partial y}{\partial t} dt \right).
$$
 \hspace{1cm} (13)

由于 $x, y$ 又是 $(s, t)$ 的可微函数，因此同时有

$$
dx = \frac{\partial x}{\partial s} ds + \frac{\partial x}{\partial t} dt, \quad dy = \frac{\partial y}{\partial s} ds + \frac{\partial y}{\partial t} dt.
$$
 \hspace{1cm} (13)

将(13)式代入(12)式，得到与(11)式完全相同的结果。这就是关于多元函数的**一阶（全）微分形式不变性**。


## §3 方向导数与梯度

定义 1 设三元函数 $f$ 在点 $P_0(x_0, y_0, z_0)$ 的某邻域 $U(P_0) \subset \mathbb{R}^3$ 有定义，$l$ 为从点 $P_0$ 出发的射线，$P(x, y, z)$ 为 $l$ 上且含于 $U(P_0)$ 内的任一点，以 $\rho$ 表示 $P$ 与 $P_0$ 两点间的距离。若极限

$$
\lim_{\rho \to 0^+} \frac{f(P) - f(P_0)}{\rho} = \lim_{\rho \to 0^+} \frac{\Delta_l f}{\rho}
$$


存在，则称此极限为函数 $f$ 在点 $P_0$ 沿方向 $l$ 的方向导数，记作

$$
\left. \frac{\partial f}{\partial l} \right|_{P_0}, f_l(P_0) \text{ 或 } f_l(x_0, y_0, z_0).
$$


定理 17.6 若函数 $f$ 在点 $P_0(x_0, y_0, z_0)$ 可微，则 $f$ 在点 $P_0$ 沿任一方向 $l$ 的方向导数都存在，且

$$
f_l(P_0) = f_x(P_0) \cos \alpha + f_y(P_0) \cos \beta + f_z(P_0) \cos \gamma,
$$
 \hspace{1cm} (1)

其中 $\cos \alpha, \cos \beta, \cos \gamma$ 为方向 $l$ 的方向余弦。

定义 2 若 $f(x, y, z)$ 在点 $P_0(x_0, y_0, z_0)$ 存在对所有自变量的偏导数，则称向量 $(f_x(P_0), f_y(P_0), f_z(P_0))$ 为函数 $f$ 在点 $P_0$ 的梯度，记作

$$
\text{grad } f = (f_x(P_0), f_y(P_0), f_z(P_0)).
$$


向量 $\text{grad } f$ 的长度（或模）为

$$
| \text{grad } f| = \sqrt{f_x(P_0)^2 + f_y(P_0)^2 + f_z(P_0)^2}.
$$


在定理 17.6 的条件下，若记 $l$ 方向上的单位向量为

$$
l_0 = (\cos \alpha, \cos \beta, \cos \gamma).
$$


于是方向导数公式又可写成

$$
f_l(P_0) = \text{grad } f(P_0) \cdot l_0 = | \text{grad } f(P_0)| \cos \theta,
$$


这里 $\theta$ 是梯度向量 $\text{grad } f(P_0)$ 与 $l_0$ 的夹角。

因此当 $\theta = 0$ 时，$f_l(P_0)$ 取得最大值 $| \text{grad } f(P_0)|$。这就是说，当 $f$ 在点 $P_0$ 可微时，$f$ 在点 $P_0$ 的梯度方向是 $f$ 的值增长最快的方向，且沿这一方向的变化率就是梯度的模；而当 $l$ 与梯度向量反方向（$\theta = \pi$ 时，方向导数取得最小值 $-| \text{grad } f(P_0)|$。