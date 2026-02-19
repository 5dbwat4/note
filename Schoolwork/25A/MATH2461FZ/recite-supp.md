# 两两独立 vs. 相互独立

- **两两独立**：一组事件中任意两个事件之间相互独立。即对于任意不同的下标 $i$ 和 $j$，有  
  $$
  P(A_i \cap A_j) = P(A_i) P(A_j).
  $$
- **相互独立**：一组事件中任意有限个事件之间相互独立。即对于任意不同的下标 $i_1, i_2, \dots, i_k$，有  
  $$
  P(A_{i_1} \cap A_{i_2} \cap \cdots \cap A_{i_k}) = P(A_{i_1}) P(A_{i_2}) \cdots P(A_{i_k}).
  $$

相互独立比两两独立更强：相互独立必然推出两两独立，但两两独立未必推出相互独立。

## 例子：抛两枚公平硬币
考虑样本空间 $\Omega = \{HH, HT, TH, TT\}$，每个结果的概率为 $1/4$。定义三个事件：
- $A$：第一枚硬币正面，即 $\{HH, HT\}$，概率 $1/2$。
- $B$：第二枚硬币正面，即 $\{HH, TH\}$，概率 $1/2$。
- $C$：两枚硬币结果相同，即 $\{HH, TT\}$，概率 $1/2$。

**检查两两独立性**：
- $P(A \cap B) = P(\{HH\}) = 1/4 = (1/2) \times (1/2) = P(A)P(B)$。
- $P(A \cap C) = P(\{HH\}) = 1/4 = (1/2) \times (1/2) = P(A)P(C)$。
- $P(B \cap C) = P(\{HH\}) = 1/4 = (1/2) \times (1/2) = P(B)P(C)$。
因此，$A$、$B$、$C$ 两两独立。

**检查相互独立性**：
- $P(A \cap B \cap C) = P(\{HH\}) = 1/4$。
- $P(A)P(B)P(C) = (1/2)^3 = 1/8$。
由于 $1/4 \ne 1/8$，不满足相互独立的条件。实际上，当 $A$ 和 $B$ 同时发生时，$C$ 必然发生（因为两枚都是正面），所以这三个事件不是相互独立的。


# 例题 2-1




(1) 由分布函数的定义可知:
$$
F(x) = 
\begin{cases}
0, & x < 0, \\
0.4, & 0 \leq x < 2, \\
0.9, & 2 \leq x < 3, \\
1, & x \geq 3.
\end{cases}
$$
(2) 
$$
P\{1 \leq X < 3\} = P\{X = 2\} = 0.5.
$$


# 例题 2-2

**例2.5.4** 设 $X$ 的密度函数为 $f_X(x)$，$Y = |X|$，$Z = X^2$，分别求 $Y$ 与 $Z$ 的密度函数 $f_Y(y)$，$f_Z(t)$。


**解** 设 $Y$ 与 $Z$ 的分布函数分别为 $F_Y(y)$，$F_Z(t)$。
当 $y \leq 0$ 时，显然有 $F_Y(y) = 0$；当 $y > 0$ 时，有
$$
F_Y(y) = P\{Y \leq y\} = P\{|X| \leq y\} = F_X(y) - F_X(-y).
$$
那么
$$
f_Y(y) = \begin{cases}
f_X(y) + f_X(-y), & y > 0, \\
0, & y \leq 0.
\end{cases}
$$


当 $t \leq 0$ 时，显然有 $F_Z(t) = 0$；当 $t > 0$ 时，有
$$
F_Z(t) = P\{Z \leq t\} = P\{X^2 \leq t\} = F_X(\sqrt{t}) - F_X(-\sqrt{t}).
$$
那么
$$
f_Z(t) = \begin{cases}
\frac{1}{2\sqrt{t}} \left[ f_X(\sqrt{t}) + f_X(-\sqrt{t}) \right], & t > 0, \\
0, & t \leq 0.
\end{cases}
$$

# 例题 3-1

**例3.4.2** 问在下面两种情况下, $X$ 与 $Y$ 是否相互独立:

(1) 设 $(X,Y)$ 的联合密度函数为
$$
f(x,y) = \begin{cases}
\frac{\mathrm{e}^{-x}}{2}, & x > 0, 0 < y < 2, \\
0, & \text{其他};
\end{cases}
$$


(2) 设 $(X,Y)$ 的联合密度函数为
$$
f(x,y) = \begin{cases}
\frac{1}{x}, & 0 < y < x < 1, \\
0, & \text{其他}.
\end{cases}
$$


**解** (1) 记
$$
m(x) = \begin{cases}
\mathrm{e}^{-x}, & x > 0, \\
0, & \text{其他},
\end{cases} \quad
n(y) = \begin{cases}
\frac{1}{2}, & 0 < y < 2, \\
0, & \text{其他},
\end{cases}
$$
则
$$
f(x,y) = m(x) \cdot n(y), \quad -\infty < x < +\infty, \ -\infty < y < +\infty.
$$
故 $X,Y$ 相互独立.


(2) 由于 $f(x,y)$ 不能分解成 $x$ 的函数与 $y$ 的函数的乘积, 故 $X,Y$ 不独立.

从另一角度来看, 可以求得 $X,Y$ 的边际密度函数分别为
$$
f_X(x) = \begin{cases}
1, & 0 < x < 1, \\
0, & \text{其他},
\end{cases} \quad
f_Y(y) = \begin{cases}
-\ln y, & 0 < y < 1, \\
0, & \text{其他}.
\end{cases}
$$
故当 $0 < y < x < 1$ 时, $f(x,y) \neq f_X(x) \cdot f_Y(y)$. 那么由 (3.4.4) 式也可知 $X,Y$ 不独立.

