# 第二十章 曲线积分


## §1 第一型曲线积分

**定义1** 设$L$为平面上可求长度的曲线段，$f(x,y)$为定义在$L$上的函数。对曲线$L$作分割$T$，它把$L$分成$n$个可求长度的小曲线段$L_i$（$i=1,2,\cdots,n$），$L_i$的弧长记为$\Delta s_i$，分割$T$的细度为$\|T\| = \max_{1 \leq i \leq n} \Delta s_i$，在$L_i$上任取一点$(\xi_i, \eta_i)$（$i=1,2,\cdots,n$）。若有极限

$$
\lim_{\|T\| \to 0} \sum_{i=1}^n f(\xi_i, \eta_i) \Delta s_i = J,
$$

且$J$的值与分割$T$和点$(\xi_i, \eta_i)$的取法无关，则称此极限为$f(x,y)$在$L$上的第一型曲线积分，记作

$$
\int_L f(x,y) \, ds. \tag{1}
$$

1. 若$\int_L f_i(x,y) \, ds$（$i=1,2,\cdots,k$）存在，$c_i$（$i=1,2,\cdots,k$）为常数，则$\int_L \sum_{i=1}^k c_i f_i(x,y) \, ds$也存在，且

$$
\int_L \sum_{i=1}^k c_i f_i(x,y) \, ds = \sum_{i=1}^k c_i \int_L f_i(x,y) \, ds.
$$

2. 若曲线段$L$由曲线$L_1, L_2, \cdots, L_k$首尾相接而成，且$\int_{L_i} f(x,y) \, ds$（$i=1,2,\cdots,k$）都存在，则$\int_L f(x,y) \, ds$也存在，且

$$
\int_L f(x,y) \, ds = \sum_{i=1}^k \int_{L_i} f(x,y) \, ds.
$$

3. 若$\int_L f(x,y) \, ds$与$\int_L g(x,y) \, ds$都存在，且在$L$上$f(x,y) \leq g(x,y)$，则

$$
\int_L f(x,y) \, ds \leq \int_L g(x,y) \, ds.
$$

4. 若$\int_L f(x,y) \, ds$存在，则$\int_L |f(x,y)| \, ds$也存在，且

$$
\left| \int_L f(x,y) \, ds \right| \leq \int_L |f(x,y)| \, ds.
$$

5. 若$\int_L f(x,y) \, ds$存在，$L$的弧长为$s$，则存在常数$c$，使得

$$
\int_L f(x,y) \, ds = cs,
$$

这里$\inf_L f(x,y) \leq c \leq \sup_L f(x,y)$。

6. 第一型曲线积分的几何意义

若$L$为平面$Oxy$上分段光滑曲线（如图20-1），$f(x,y)$为定义在$L$上非负连续函数。由第一型曲面积分的定义，以$L$为准线，母线平行于$z$轴的柱面上截取$0 \leq z \leq f(x,y)$的部分面积就是$\int_L f(x,y) \, ds$。

**定理20.1** 设有光滑曲线

$$
L: \begin{cases} 
x = \varphi(t), \\
y = \psi(t),
\end{cases} \quad t \in [\alpha, \beta],
$$

函数$f(x,y)$为定义在$L$上的连续函数，则

$$
\int_L f(x,y) \, ds = \int_{\alpha}^{\beta} f(\varphi(t), \psi(t)) \sqrt{\varphi'^2(t) + \psi'^2(t)} \, dt. \tag{3}
$$

## §2 第二型曲线积分

定义1 设函数$P(x,y)$与$Q(x,y)$定义在平面有向可求长度曲线$L:AB$上。对$L$的任一分割$T$，它把$L$分成$n$个小弧段

$$
\widehat{M_{i-1}M_i} \quad (i=1,2,\cdots,n),
$$

其中$M_0=A, M_n=B$。记各小弧段$\widehat{M_{i-1}M_i}$的弧长为$\Delta s_i$，分割$T$的细度$\|T\| = \max_{1 \leq i \leq n} \Delta s_i$。又设$T$的分点$M_i$的坐标为$(x_i, y_i)$，并记$\Delta x_i = x_i - x_{i-1}, \Delta y_i = y_i - y_{i-1}$（$i=1,2,\cdots,n$）。在每个小弧段$\widehat{M_{i-1}M_i}$上任取一点$(\xi_i, \eta_i)$，若极限

$$
\lim_{\|T\| \to 0} \sum_{i=1}^n P(\xi_i, \eta_i) \Delta x_i + \lim_{\|T\| \to 0} \sum_{i=1}^n Q(\xi_i, \eta_i) \Delta y_i
$$

存在且与分割$T$和点$(\xi_i, \eta_i)$的取法无关，则称此极限为函数$P(x,y), Q(x,y)$沿有向曲线$L$上的第二型曲线积分，记为

$$
\int_L P(x,y) \, dx + Q(x,y) \, dy \quad \text{或} \quad \int_{\widehat{AB}} P(x,y) \, dx + Q(x,y) \, dy. \tag{1}
$$

上述积分(1)也可写作

$$
\int_L P(x,y) \, dx + \int_L Q(x,y) \, dy
$$

或

$$
\int_{\widehat{AB}} P(x,y) \, dx + \int_{\widehat{AB}} Q(x,y) \, dy.
$$

为书写简洁起见，(1)式常简写成

$$
\int_L P \, dx + Q \, dy \quad \text{或} \quad \int_{\widehat{AB}} P \, dx + Q \, dy.
$$

若$L$为封闭的有向曲线，则记为

$$
\oint_L P \, dx + Q \, dy. \tag{2}
$$

若记$\boldsymbol{F}(x,y) = (P(x,y), Q(x,y))$，$ds = (dx, dy)$，则(1)式可写成向量形式

$$
\int_L \boldsymbol{F} \cdot \, ds \quad \text{或} \quad \int_{\widehat{AB}} \boldsymbol{F} \cdot \, ds. \tag{3}
$$

于是，力$\boldsymbol{F}(x,y) = (P(x,y), Q(x,y))$沿有向曲线$L: \widehat{AB}$对质点所做的功为

$$
W = \int_L P(x,y) \, dx + Q(x,y) \, dy.
$$

简若$L$为空间有向可求长度曲线，$P(x,y,z), Q(x,y,z), R(x,y,z)$为定义在$L$上的函数，则可按上述办法类似地定义沿空间有向曲线$L$上的第二型曲线积分，并记为

$$
\int_L P(x,y,z) \, dx + Q(x,y,z) \, dy + R(x,y,z) \, dz, \tag{4}
$$

或简写成

$$
\int_L P \, dx + Q \, dy + R \, dz.
$$

当把$\boldsymbol{F}(x,y,z) = (P(x,y,z), Q(x,y,z), R(x,y,z))$与$ds = (dx, dy, dz)$看作三维向量时，(4)式也可表示成(3)式的向量形式。

1. 若$\int_L P_i \, dx + Q_i \, dy$（$i=1,2,\cdots,k$）存在，则$\int_L \left( \sum_{i=1}^k c_i P_i \right) \, dx + \left( \sum_{i=1}^k c_i Q_i \right) \, dy$也存在，且

$$
\int_L \left( \sum_{i=1}^k c_i P_i \right) \, dx + \left( \sum_{i=1}^k c_i Q_i \right) \, dy = \sum_{i=1}^k c_i \left( \int_L P_i \, dx + Q_i \, dy \right),
$$

其中$c_i$（$i=1,2,\cdots,k$）为常数。

2. 若有向曲线$L$是由有向曲线$L_1, L_2, \cdots, L_k$首尾相接而成，且$\int_{L_i} P \, dx + Q \, dy$（$i=1,2,\cdots,k$）存在，则$\int_L P \, dx + Q \, dy$也存在，且

$$
\int_L P \, dx + Q \, dy = \sum_{i=1}^k \int_{L_i} P \, dx + Q \, dy.
$$