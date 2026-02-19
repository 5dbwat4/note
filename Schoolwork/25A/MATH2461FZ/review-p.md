

题：
一批产品的寿命服从均值为 $1/\lambda$ 的指数分布，今从中随机独立取两件，分别用 $X_1, X_2$ 记其寿命，设  
$$
W_k = 
\begin{cases} 
1, & X_k > k/\lambda, \\ 
0, & X_k \leq k/\lambda. 
\end{cases}
\quad k=1,2.
$$  
则 $W_1$ 的概率分布律为  

记 $Y_1 = W_1W_2, \quad Y_2 = \max(W_1, W_2)$，则 $Y_1$ 的概率分布律为  

概率分布律为  

解：
$$
\begin{pmatrix}
0 & 1 \\
1-e^{-1} & e^{-1}
\end{pmatrix},
\quad \begin{pmatrix}
0 & 1 \\
1-e^{-3} & e^{-3}
\end{pmatrix},
\quad \begin{pmatrix}
0 & 1 \\
(1-e^{-1})(1-e^{-2}) & 1-(1-e^{-1})(1-e^{-2})
\end{pmatrix}
$$

---

题：
市场近期某种蔬菜的单价（单位：元/公斤）$X \sim U(6,8)$（均匀分布），某餐馆近期购买该种蔬菜的数量 $Y$ 为 8 公斤和 10 公斤的概率均为 0.5. 设 $X$ 与 $Y$ 相互独立，购买金额 $Z=XY$  
不大于 60 元的概率为 $\underline{\quad }$；$Z$ 的分布函数 $F_z(z) = \underline{\quad }$.

解：
$$
3/8=0.375,
\quad F_z(z) =
\begin{cases}
0, & z < 48, \\
\frac{z}{32} - \frac{3}{2}, & 48 \leq z < 60, \\
\frac{9z}{160} - 3, & 60 \leq z < 64, \\
\frac{z}{40} - 1, & 64 \leq z < 80, \\
1, & z \geq 80.
\end{cases}
$$

---

题：
设总体 $ X \sim N(\mu, 0.5) $，$\mu$ 未知，$X_1, \ldots, X_9$ 为来自 $X$ 的简单随机样本，记 $\bar{X} = \frac{1}{9} \sum_{i=1}^{9} X_i$，  
则 $P(|\bar{X} - X_1| \leq 2/3) = \underline{\quad }$，$\sum_{i=1}^{4} (X_i - X_{i+4})^2$ 服从 $\underline{\quad }$ 分布，若根据样本观测值，得 $\bar{x} = 6.472$，则检验假设 $H_0 : \mu \leq 6, H_1 : \mu > 6$ 的 $P$ 值为 $\underline{\quad }$。

解：
$$
2\Phi(1) - 1 = 0.68,\quad \chi^2(4),\quad 0.02.
$$

---

题：
设 $X_1$ 与 $X_2$ 为两随机变量，它们的取值均为 0, 1, 2，已知 $P(X_1 = i) = 1/3, i = 0, 1, 2$,  
$$
P(X_2 = j | X_1 = i) =
\begin{cases}
0.4, & i = j, \\
0.3, & |i-j| = 1.
\end{cases}
$$
$i, j = 0, 1, 2$。求  

（1）$P(X_2 = 2 | X_1 = 0)$；  
（2）$P(X_2 = 2)$；  
（3）$X_1$ 与 $X_2$ 的协方差。

解：

（1）$P(X_2 = 2 | X_1 = 0) = 1 - P(X_2 = 0 | X_1 = 0) - P(X_2 = 1 | X_1 = 0) = 0.3,$  

（2）$P(X_2 = 2) = P(X_1 = 0) P(X_2 = 2 | X_1 = 0) + P(X_1 = 1) P(X_2 = 2 | X_1 = 1) + P(X_1 = 2) P(X_2 = 2 | X_1 = 2) = 1/3,$  

$X_1 \backslash X_2$

$$
\begin{array}{ccccc}
0 & 1 & 2 & p \\
0 & 4/30 & 3/30 & 3/30 & 1/3 \\
1 & 3/30 & 4/30 & 3/30 & 1/3 \\
2 & 3/30 & 3/30 & 4/30 & 1/3 \\
p & 1/3 & 1/3 & 1/3 & 1 \\
E(X_1) = E(X_2) = 1, & E(X_1 X_2) = 16/15, \\
Cov(X_1, X_2) = E(X_1 X_2) - E(X_1) E(X_2) = 1/15.
\end{array}
$$

---

题：
设二元随机变量 $(X,Y)$ 具有概率密度函数  
$$
f(x,y) = 
\begin{cases} 
6y, & 0 < y < x < 1, \\
0, & \text{其他}.
\end{cases}
$$  
求：(1) 求 $X$ 的边际概率密度 $f_X(x)$；(2) 求条件概率密度 $f_{Y|X}(y|_Y^2)$；(3) 设 $Z = X - Y$，求 $Z$ 的概率密度 $f_z(z)$。

解：

(1) $f_X(x) = \int_{-\infty}^{\infty} f(x,y)dy = 
\begin{cases} 
3x^2, & 0 < x < 1, \\
0, & \text{其他}.
\end{cases}$

(2) $f_{Y|X}(y|_Y^2) = \frac{f(\frac{y}{2},y)}{f_X(\frac{y}{2})} = 
\begin{cases} 
\frac{y}{2}, & 0 < y < \frac{x}{3}, \\
0, & \text{其他}.
\end{cases}$

(3) $z < 0, F_z(z) = 0, z > 1, F_z(z) = 1,$  
$0 \leq z \leq 1, F_z(z) = P(X - Y \leq z) = 1 - \int_{-1}^{1} dx \int_{0}^{z-x} 6y dy = 1 + (z - 1)^3,$  
$f_z(z) = 
\begin{cases} 
3(1 - z)^2, & 0 < z < 1, \\
0, & \text{其他}.
\end{cases}$

---

题：
设随机变量 $(X,Y)$ 服从二元正态分布，$X \sim N(1,1), Y \sim N(0,9)$。(1) 求  
$P(X + 1 > 0)$；(2) 若相关系数 $\rho = 0$，写出 $4X - Y$ 的概率密度函数和 $P(4X + 1 > Y)$；  
(3) 若 $\rho = 0.75$，求 $D(4X - Y)$ 及 $E(XY)$。

解：

(1) $P(X + 1 > 0) = 1 - \Phi(\frac{-1 - 1}{1}) = 1 - \Phi(-2) = \Phi(2) = 0.98$；  

(2) $4X - Y \sim N(4,25)$，故其密度函数为 $f(x) = \frac{1}{5\sqrt{2\pi}} e^{-\frac{(x - 4)^2}{50}}, -\infty < x < +\infty$；  
$P(4X + 1 > Y) = P(4X - Y > -1) = 1 - \Phi(\frac{-1 - 4}{5}) = 1 - \Phi(-1) = \Phi(1) = 0.84$；  

(3) $Cov(X,Y) = \rho \sqrt{D(X)D(Y)} = 0.75 \times \sqrt{1 \times 9} = 9/4 = 2.25$；  
$D(4X - Y) = 16 \times 1 + 9 - 8 \times Cov(X,Y) = 7$；  
$E(XY) = Cov(X,Y) + E(X)E(Y) = 9/4 = 2.25$。

---

题：
有一件工作需要甲乙两人接力完成，完成时间不超过4小时；设甲先干了X小时，再由乙完成，加起来共用Y小时。$ X \sim U(1,2) $，密度函数为  
$$
f_X(x) = 
\begin{cases} 
1, & 1 < x < 2 \\ 
0, & 其他 
\end{cases}
$$  
在 $X = x(1 < x < 2)$ 条件下，Y的条件概率密度为  
$$
f_{Y|X}(y|x) = 
\begin{cases} 
\frac{2(4-y)}{(3-x)^2}, & x+1 < y < 4 \\ 
0, & 其他 
\end{cases}
$$  
求 $(X,Y)$ 的联合概率密度 $ f(x,y) $ 及 $ P(Y < 3) $；（2）求Y的边际概率密度 $ f_Y(y) $；（3）求当 $\{Y=3\}$ 的条件下X的条件密度函数 $ f_{X|Y}(x|3) $；（4）已知两人完成工作共花了3个小时，求甲的工作时间不超过1.5个小时的概率。

解：

（1）$ f(x,y) = f_X(x)f_{Y|X}(y|x) = 
\begin{cases} 
\frac{2(4-y)}{(3-x)^2}, & 1 < x < 2, x+1 < y < 4 \\ 
0, & 其他 
\end{cases}
$  

$$
P(Y < 3) = \int_1^2 dx \int_{x+1}^3 \frac{2(4-y)}{(3-x)^2} dy = \frac{1}{2};
$$

（2）$ f_Y(y) = \int_{-\infty}^{\infty} f(x,y)dx = 
\begin{cases} 
\int_1^{y-1} \frac{2(4-y)}{(3-x)^2} dx = y-2, & 2 < y < 3 \\ 
\int_1^2 \frac{2(4-y)}{(3-x)^2} dx = 4-y, & 3 < y < 4 \\ 
0, & 其他 
\end{cases}
$

（3）$ f_{X|Y}(x|3) = 
\begin{cases} 
\frac{2}{(3-x)^2}, & 1 < x < 2 \\ 
0, & 其他 
\end{cases}
$

（4）$ P(X < 1.5|Y = 3) = \int_1^{1.5} \frac{2}{(3-x)^2} dx = \frac{1}{3} $

---

题：
设随机变量 $X$ 与 $Y$ 独立同分布，$X \sim U(-1,1)$（均匀分布），$Z = X + Y$，求（1）  
$$
P(X < 0|Z < 1), \quad (2) \quad X \text{与} Z \text{的相关系数} \rho_{XZ}, \quad (3) \quad Z \text{的概率密度} f_z(z), \quad (4) \quad \text{设}
$$  
$$
U = 
\begin{cases}
1, & X > 0, \\
0, & X \leq 0.
\end{cases}
\quad V = 
\begin{cases}
1, & Z > 1, \\
0, & Z \leq 1.
\end{cases}
$$  
求 $(U, V)$ 的联合分布律。

解：

(1) $$
P(X < 0|Z < 1) = \frac{P(X < 0, Z < 1)}{P(Z < 1)} = \frac{1/2}{7/8} = \frac{4}{7} = 0.5714,
$$

(2) $$
D(X) = \frac{1}{3}, D(Z) = 2D(X) = \frac{2}{3}, Cov(X, Z) = D(X), \rho_{XZ} = \frac{\sqrt{2}}{2} = 0.707,
$$

(3) $$
f_z(z) = \int_{-\infty}^{\infty} f(x, z - x) dx = 
\begin{cases}
\int_{-1}^{z+1} \frac{1}{4} dx = \frac{z + 2}{4}, & -2 < z < 0, \\
\int_{z-1}^{1} \frac{1}{4} dx = \frac{2 - z}{4}, & 0 < z < 2, \\
0, & \text{其他}.
\end{cases}
$$

(4) $$
P(U = 1, V = 1) = P(X > 0, Z > 1) = \frac{1}{8}, \quad P(U = 1, V = 0) = P(X > 0, Z \leq 1) = \frac{3}{8},
$$  
$$
P(U = 0, V = 1) = P(X \leq 0, Z > 1) = 0, \quad P(U = 0, V = 0) = P(X \leq 0, Z \leq 1) = \frac{1}{2}.
$$
