---
title: 平面方程与空间直线方程
---

### 1.9.1 平面方程

在空间直角坐标系中，欲确定一个平面$\pi$，只要给定平面上一个定点$P_0(x_0,y_0,z_0)$以及与平面垂直的一个向量
$$
\boldsymbol{n} = ai + bj + ck=(a,b,c),
$$
并称$\boldsymbol{n}$为平面的法向量. 所谓平面$\pi$的方程，就是平面$\pi$上任一点$P(x,y,z)$的坐标$x,y,z$所满足的一个关系式。

点$P(x,y,z)$在平面$\pi$上当且仅当$\overrightarrow{P_0P}\perp \boldsymbol{n}$，即$\overrightarrow{P_0P}\cdot \boldsymbol{n} = 0$，其中
$$
\overrightarrow{P_0P}=(x - x_0)i+(y - y_0)j+(z - z_0)k,
$$
于是得
$$
a(x - x_0)+b(y - y_0)+c(z - z_0)=0.\tag{1-14}
$$
方程(1 - 14)称为平面$\pi$的点法式方程，它可化为
$$
ax + by+cz + d = 0.\tag{1-15}
$$

其中$d = - ax_0 - by_0 - cz_0$. 方程$(1 - 15)$称为平面$\pi$的一般方程, 它是一个三元一次方程. 事实上, 任何三元一次方程都可化为$(1 - 14)$的形式, 因而都是平面的方程. 在平面一般方程$(1 - 15)$中, 系数$a, b, c$是平面法向量$\boldsymbol{n}$的三个坐标, 即$\boldsymbol{n}=(a, b, c)$.

(1) 当$a, b, c$有一个为$0$时, 平面$\pi$与某个坐标轴平行, 例如, $x + y = 1$, 其中$c = 0$, $\boldsymbol{n}\perp z$轴, 平面平行于$z$轴.

(2) 当$a, b, c$有两个为$0$时, 平面$\pi$平行于某坐标平面, 例如, $x = 1$平行于坐标平面$yOz$.

(3) 当$d = 0$时, 平面$\pi$过坐标原点$O(0, 0, 0)$, 因为原点坐标满足方程
$$
ax + by + cz = 0.
$$

(4) 当$abcd\neq0$时, 方程$(1 - 15)$可化为
$$
\frac{x}{a_1}+\frac{y}{b_1}+\frac{z}{c_1}=1.\tag{1 - 16}
$$

(1-16)称为平面的截矩式方程,其中$a_1,b_1,c_1$分别称为平面在$x,y,z$轴上的截矩

### 1.9.2 空间直线方程

在空间直角坐标系中确定一直线 $L$，只要给定 $L$ 上一个定点 $P_0(x_0,y_0,z_0)$ 以及与直线平行的一个向量 $\boldsymbol{S}=l\boldsymbol{i} + m\boldsymbol{j}+n\boldsymbol{k}=(l,m,n)$，$\boldsymbol{S}$ 称为直线的方向向量。

点 $P(x,y,z)$ 在直线上当且仅当 $\overrightarrow{P_0P}\parallel\boldsymbol{S}$，即当且仅当 $\overrightarrow{P_0P}=t\boldsymbol{S}$，于是
$$
\begin{cases}x - x_0=lt\\y - y_0=mt\\z - z_0=nt\end{cases} \text{即} \begin{cases}x=x_0 + lt\\y=y_0+mt\\z=z_0+nt\end{cases} \tag{1 - 17}
$$

方程$(1 - 17)$称为直线的参数方程，其中$t$称为参数. 在方程中消去参数$t$，得到
$$
\frac{x - x_0}{l}=\frac{y - y_0}{m}=\frac{z - z_0}{n}.  \tag{1 - 18}
$$
方程$(1 - 18)$称为直线的标准方程，式中的两个连等号实际上是给了由两个独立方程所组成的方程组，即
$\begin{cases}\dfrac{x - x_0}{l}=\dfrac{y - y_0}{m}\\\dfrac{x - x_0}{l}=\dfrac{z - z_0}{n}\end{cases}$ 或 $\begin{cases}\dfrac{x - x_0}{l}=\dfrac{y - y_0}{m}\\\dfrac{y - y_0}{m}=\dfrac{z - z_0}{n}\end{cases}$ 或 $\begin{cases}\dfrac{x - x_0}{l}=\dfrac{z - z_0}{n}\\\dfrac{y - y_0}{m}=\dfrac{z - z_0}{n}\end{cases}$

直线的参数方程给出了直线上的点$P$与参数$t$的一一对应关系.