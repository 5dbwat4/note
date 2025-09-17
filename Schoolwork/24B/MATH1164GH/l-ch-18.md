# 第十八章 隐函数定理及其应用

## §1 隐 函 数

### 一、隐函数的概念

设 $E \subset \mathbb{R}^2$，函数 $F: E \rightarrow \mathbb{R}$。对于方程
$$
F(x,y) = 0, \tag{1}
$$
如果存在集合 $I, J \subset \mathbb{R}$，对任何 $x \in I$，有惟一确定的 $y \in J$，使得 $(x,y) \in E$，且满足方程(1)，则称方程(1)确定了一个定义在 $I$ 上，值域含于 $J$ 的**隐函数**。若把它记为
$$
y = f(x) , x \in I, \ y \in J,
$$
则成立恒等式
$$
F(x, f(x)) \equiv 0, \ x \in I.
$$

(i)并不是任一方程都能确定出隐函数，

(ii)倘若方程(1)能确定隐函数，一般并不都像前面的一些例子那样，能从方程中解出y,并用自变量x的算式来表示(即使F(x,y)是初等函数).

### 三、隐函数定理

**定理 18.1 (隐函数存在惟一性定理)** 若函数 $F(x,y)$ 满足下列条件：

- (i) $F$ 在以 $P_0(x_0, y_0)$ 为内点的某一区域 $D \subset \mathbb{R}^2$ 上连续；
- (ii) $F(x_0, y_0) = 0$（通常称为初始条件）；
- (iii) $F$ 在 $D$ 上存在连续的偏导数 $F_y(x,y)$；
- (iv) $F_y(x_0, y_0) \neq 0$.

则

- 1° 存在点 $P_0$ 的某邻域 $U(P_0) \subset D$，在 $U(P_0)$ 上方程 $F(x,y) = 0$ 唯一地决定了一个定义在某区间 $(x_0-\alpha, x_0+\alpha)$ 上的（隐）函数 $y=f(x)$，使得当 $x \in (x_0-\alpha, x_0+\alpha)$ 时，$(x, f(x)) \in U(P_0)$，且 $F(x, f(x)) \equiv 0$，$f(x_0) = y_0$；
- 2° $f(x)$ 在 $(x_0-\alpha, x_0+\alpha)$ 上连续。

注1 定理18.1的条件仅仅是充分的.

注2 在定理证明过程中，条件(iii)和(iv)只是用来保证存在$P_0$的某一邻域，在此邻域上$F$关于变量$y$是严格单调的.因此对于本定理所要证明的结论来说，可以把这两个条件减弱为“$F$在$P_0$的某一邻域上关于$y$严格单调”.

注 3 如果把定理的条件 (iii) 和 (iv) 改为 $F_x(x,y)$ 连续，且 $F_x(x_0, y_0) \neq 0$。这时结论是存在惟一的连续函数 $x = g(y)$。

**定理 18.2 (隐函数可微性定理)** 设 $F(x,y)$ 满足隐函数存在惟一性定理中的条件 (i)—(iv)，又设在 $D$ 上还存在连续的偏导数 $F_x(x,y)$，则由方程 (1) 所确定的隐函数 $y = f(x)$ 在其定义域 $(x_0-\alpha, x_0+\alpha)$ 上有连续导函数，且
$$
f'(x) = -\frac{F_x(x,y)}{F_y(x,y)}. \tag{5}
$$

**定理 18.3** 若
- (i) 函数 $F(x_1, x_2, \cdots, x_n, y)$ 在以点 $P_0(x_1^0, x_2^0, \cdots, x_n^0, y^0)$ 为内点的区域 $D \subset \mathbb{R}^{n+1}$ 上连续；
- (ii) $F(x_1^0, x_2^0, \cdots, x_n^0, y^0) = 0$；
- (iii) 偏导数 $F_{x_1}, F_{x_2}, \cdots, F_{x_n}, F_y$ 在 $D$ 上存在且连续；
- (iv) $F_y(x_1^0, x_2^0, \cdots, x_n^0, y^0) \neq 0$。

则

1° 存在点 $P_0$ 的某邻域 $U(P_0) \subset D$，在 $U(P_0)$ 上方程 $F(x_1, \cdots, x_n, y) = 0$ 唯一地确定了一个定义在 $Q_0(x_1^0, x_2^0, \cdots, x_n^0)$ 的某邻域 $U(Q_0) \subset \mathbb{R}^n$ 上的 $n$ 元连续函数（隐函数）$y = f(x_1, \cdots, x_n)$，使得当 $(x_1, x_2, \cdots, x_n) \in U(Q_0)$ 时，
$$
(x_1, x_2, \cdots, x_n, f(x_1, x_2, \cdots, x_n)) \in U(P_0),
$$
且
$$
F(x_1, \cdots, x_n, f(x_1, \cdots, x_n)) \equiv 0,
$$
$$
y^0 = f(x_1^0, \cdots, x_n^0);
$$

2° $y = f(x_1, \cdots, x_n)$ 在 $U(Q_0)$ 上有连续偏导数 $f_{x_1}, f_{x_2}, \cdots, f_{x_n}$，而且
$$
f_{x_1} = -\frac{F_{x_1}}{F_y}, \ f_{x_2} = -\frac{F_{x_2}}{F_y}, \ \cdots, \ f_{x_n} = -\frac{F_{x_n}}{F_y}.
$$


## §2 隐 函 数 组

**定理 18.4 (隐函数组定理)** 若
- (i) $F(x,y,u,v)$ 与 $G(x,y,u,v)$ 在以点 $P_0(x_0,y_0,u_0,v_0)$ 为内点的区域 $V \subset \mathbb{R}^4$ 上连续；
- (ii) $F(x_0,y_0,u_0,v_0) = 0, G(x_0,y_0,u_0,v_0) = 0$（初始条件）；
- (iii) 在 $V$ 上 $F, G$ 具有一阶连续偏导数；
- (iv) $J = \frac{\partial(F,G)}{\partial(u,v)}$ 在点 $P_0$ 不等于零。

则

1° 存在点 $P_0$ 的某一(四维空间)邻域 $U(P_0) \subset V$，在 $U(P_0)$ 上方程组(1)唯一地确定了定义在点 $Q_0(x_0,y_0)$ 的某一(二维空间)邻域 $U(Q_0)$ 上的两个二元隐函数
$$
u = f(x,y), \ v = g(x,y),
$$
使得 $u_0 = f(x_0,y_0), v_0 = g(x_0,y_0)$，且当 $(x,y) \in U(Q_0)$ 时，
$$
\begin{aligned}
(x,y,f(x,y),g(x,y)) \in U(P_0), \\

F(x,y,f(x,y),g(x,y)) \equiv 0, \\

G(x,y,f(x,y),g(x,y)) \equiv 0;
\end{aligned}
$$

2° $f(x,y), g(x,y)$ 在 $U(Q_0)$ 上连续；

3° $f(x,y), g(x,y)$ 在 $U(Q_0)$ 上有一阶连续偏导数，且
$$
\begin{aligned}

\frac{\partial u}{\partial x} = -\frac{1}{J} \frac{\partial(F,G)}{\partial(x,v)}, \ \frac{\partial v}{\partial x} = -\frac{1}{J} \frac{\partial(F,G)}{\partial(u,x)}, \\

\frac{\partial u}{\partial y} = -\frac{1}{J} \frac{\partial(F,G)}{\partial(y,v)}, \ \frac{\partial v}{\partial y} = -\frac{1}{J} \frac{\partial(F,G)}{\partial(u,y)}. 
\end{aligned}
\tag{5}
$$

**定理 18.5 (反函数组定理)** 设函数组(9)及其一阶偏导数在某区域 $D \subset \mathbb{R}^2$ 上连续，点 $P_0(x_0,y_0)$ 是 $D$ 的内点，且
$$
u_0 = u(x_0,y_0), \ v_0 = v(x_0,y_0), \ \left.\frac{\partial(u,v)}{\partial(x,y)}\right|_{P_0} \neq 0,
$$
则在点 $P'_0(u_0,v_0)$ 的某一邻域 $U(P'_0)$ 上存在唯一的一组反函数(10)，使得 $x_0 = x(u_0,v_0), y_0 = y(u_0,v_0)$，且当 $(u,v) \in U(P'_0)$ 时，有
$$
(x(u,v), y(u,v)) \in U(P_0)
$$
以及恒等式(11)。此外，反函数组(10)在 $U(P'_0)$ 上存在连续的一阶偏导数，且
$$

\begin{aligned}

\frac{\partial x}{\partial u} = \frac{\partial v}{\partial y} \bigg/ \frac{\partial(u,v)}{\partial(x,y)}, \ \frac{\partial x}{\partial v} = -\frac{\partial u}{\partial y} \bigg/ \frac{\partial(u,v)}{\partial(x,y)}, \\

\frac{\partial y}{\partial u} = -\frac{\partial v}{\partial x} \bigg/ \frac{\partial(u,v)}{\partial(x,y)}, \ \frac{\partial y}{\partial v} = \frac{\partial u}{\partial x} \bigg/ \frac{\partial(u,v)}{\partial(x,y)}.

\end{aligned}
 \tag{13}
$$
由(13)式看到：互为反函数组的(9)与(10)，它们的雅可比行列式互为倒数，即
$$
\frac{\partial(u,v)}{\partial(x,y)} \cdot \frac{\partial(x,y)}{\partial(u,v)} = 1.
$$