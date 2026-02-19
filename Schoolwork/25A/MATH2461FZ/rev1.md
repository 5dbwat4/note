
### 第一章：概率论的基本概念

#### 1.1–1.2 基本概念  
- **基本要素**：随机试验、样本空间、随机事件  
- **事件关系与运算**：包括加法公式  
- **重要概念区分**：
  - 互斥（互不相容） vs. 独立
- 要求：能进行事件概率的基本运算

#### 1.3 古典概型（等可能概型）  
- 要求：掌握概率计算方法

#### 1.4 条件概率  
- **定义**：  
  $$
  P(A|B) = \frac{P(AB)}{P(B)}, \quad \text{其中 } P(B) \ne 0
  $$
- **三大公式**：
  1. **乘法公式**：  
     $$
     P(AB) = P(A) \cdot P(B|A)
     $$
  2. **全概率公式**（设 $\{B_j\}$ 为完备事件组）：  
     $$
     P(A) = \sum_{j=1}^n P(AB_j) = \sum_{j=1}^n P(A|B_j) P(B_j)
     $$
  3. **Bayes 公式**：  
     $$
     P(B_i|A)  = \frac{P(A|B_i) P(B_i)}{\sum_{j=1}^n P(A|B_j) P(B_j)}
     $$
- **条件形式的全概率公式**：  
  $$
  P(A|C) = \sum_{j=1}^n P(A|B_j C) P(B_j|C)
  $$

#### 1.5 独立性  
- **两事件独立**：  
  $$
  A \text{ 与 } B \text{ 独立} \iff P(AB) = P(A)P(B)
  $$
- **n 个事件相互独立**：  
  对任意 $2 \le k \le n$，都有  
  $$
  P(A_{i_1} \cap \cdots \cap A_{i_k}) = P(A_{i_1}) \cdots P(A_{i_k})
  $$
- **注意区分**：
  - 两两独立 vs. 相互独立
  - 独立 vs. 互斥

---

### 第二章：随机变量及其概率分布

#### 基本定义  
- 随机变量 $X: S \to \mathbb{R}$  
- **分布函数**：  
  $$
  F(x) = P(X \le x), \quad x \in \mathbb{R}
  $$
- **两类随机变量**：离散型、连续型

#### 离散型随机变量  
- **分布律**：  
  $$
  P(X = x_k) = p_k,\quad k = 1,2,\dots,\quad \text{其中 } p_k \ge 0, \sum p_k = 1
  $$
  表示形式：
  $$
  \begin{array}{c|cccc}
  X & x_1 & x_2 & \cdots & x_k & \cdots \\
  \hline
  P & p_1 & p_2 & \cdots & p_k & \cdots
  \end{array}
  $$
- **分布函数**：阶梯函数  
- **要求**：掌握由分布律求分布函数，及条件分布律/条件分布函数

#### 连续型随机变量  
- **定义**：若存在函数 $f(t)$，使得  
  $$
  F(x) = \int_{-\infty}^x f(t)\,dt
  $$
  则称 $X$ 为连续型，$f$ 为**概率密度函数**
- **性质**：
  - $f(x) \ge 0$
  - $\int_{-\infty}^{\infty} f(x)\,dx = 1$
  - $P(X = c) = 0$
- **概率计算**：  
  $$
  P(a \le X \le b) = \int_a^b f(t)\,dt
  $$
- **要求**：掌握 $F(x) \leftrightarrow f(x)$ 的相互推导，及条件密度函数、条件分布函数

#### 六大常用分布  
- **离散型**（3个）：如二项分布（需能判别）
- **连续型**（3个）
- 要求：掌握分布律/密度函数、参数与数字特征的关系

#### 随机变量函数的分布  
- **离散型**：
  1. 列出 $Y = g(X)$ 的所有可能取值
  2. 利用“等价事件”求对应概率
- **连续型**：
  1. 确定支撑集（密度非零区域）
  2. 先求分布函数 $F_Y(y) = P(g(X) \le y)$，再求导得 $f_Y(y)$
- **特例**：若 $g(x)$ 单调，可使用教材定理 2.5.1

---

### 第三章：多元随机变量及其分布

#### 联合分布  
- **联合分布函数**：  
  $$
  F(x, y) = P(X \le x, Y \le y)
  $$
- **离散型**：联合分布律 $P(X = x_i, Y = y_j) = p_{ij}$，用表格表示  
- **连续型**：联合密度函数 $f(x, y)$，满足  
  $$
  F(x, y) = \int_{-\infty}^x \int_{-\infty}^y f(u, v)\,dv\,du, \quad
  f(x, y) = \frac{\partial^2 F(x,y)}{\partial x \partial y}
  $$

#### 边际分布  
- **分布函数**：  
  $$
  F_X(x) = F(x, +\infty), \quad F_Y(y) = F(+\infty, y)
  $$
- **离散型**：对联合分布律按行/列求和（“加花边”）  
- **连续型**：  
  $$
  f_X(x) = \int_{-\infty}^{\infty} f(x, y)\,dy,\quad \text{注意支撑集，建议画图}
  $$

#### 条件分布  
- **离散型**：按条件概率定义  
- **连续型**：  
  $$
  f_{X|Y}(x|y) = \frac{f(x, y)}{f_Y(y)}, \quad f_Y(y) > 0
  $$

#### 独立性  
- **定义**：  
  $$
  F(x, y) = F_X(x) F_Y(y)
  $$
- **离散型**：检查 $p_{ij} = p_{i\cdot} p_{\cdot j}$  
- **连续型**：检查 $f(x, y) = f_X(x) f_Y(y)$，注意支撑集是否可分离

#### 多元随机变量函数的分布  
- **离散型**：思路同单变量  
- **连续型**：先求分布函数  
- **特例一：$Z = X + Y$**  
  $$
  f_Z(z) = \int_{-\infty}^{\infty} f(x, z - x)\,dx
  $$
  若 $X, Y$ 独立，称为**卷积公式**：  
  $$
  f_Z(z) = \int_{-\infty}^{\infty} f_X(x) f_Y(z - x)\,dx
  $$
- **特例二：$M = \max\{X, Y\},\ N = \min\{X, Y\}$**  
  - $F_M(z) = P(X \le z, Y \le z) = F_X(z) F_Y(z)$（若独立）  
  - $F_N(z) = 1 - P(X > z, Y > z) = 1 - [1 - F_X(z)][1 - F_Y(z)]$（若独立）  
- **注意**：求 $E[M], E[N]$ 时，需先求分布函数 → 密度函数 → 期望

---

### 第四章：随机变量的数字特征

#### 期望（数学期望）  
- **定义**：
  - 离散型：$EX = \sum x_k p_k$
  - 连续型：$EX = \int_{-\infty}^{\infty} x f(x)\,dx$
- **存在性**：要求积分/级数绝对收敛
- **“懒人定理”**：可直接对函数 $g(X)$ 求期望，无需先求分布

#### 期望的性质  
1. $E[c] = c$  
2. $E[cX] = c EX$  
3. $E[X + Y] = EX + EY$  
4. 若 $X, Y$ 不相关（或独立），则 $E[XY] = EX \cdot EY$

#### 方差  
- **定义**：$\operatorname{Var}(X) = E[(X - EX)^2]$  
- **计算公式**：$\operatorname{Var}(X) = E[X^2] - (EX)^2$

#### 方差的性质  
1. $\operatorname{Var}(c) = 0$  
2. $\operatorname{Var}(cX) = c^2 \operatorname{Var}(X)$  
3. $\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) + 2\operatorname{Cov}(X, Y)$  
   - 若独立 ⇒ $\operatorname{Cov}(X,Y)=0$ ⇒ $\operatorname{Var}(X+Y) = \operatorname{Var}(X)+\operatorname{Var}(Y)$  
4. $\operatorname{Var}(X) = 0 \iff P(X = c) = 1$（其中 $c = EX$）

#### 协方差与相关系数  
- **协方差**：  
  $$
  \operatorname{Cov}(X, Y) = E[(X - EX)(Y - EY)] = E[XY] - EX \cdot EY
  $$
- **相关系数**：  
  $$
  \rho_{XY} = \frac{\operatorname{Cov}(X, Y)}{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}}
  $$
- **不相关**：$\rho_{XY} = 0 \iff \operatorname{Cov}(X,Y) = 0 \iff E[XY] = EX \cdot EY \iff \operatorname{Var}(X+Y) = \operatorname{Var}(X)+\operatorname{Var}(Y)$
- **独立 ⇒ 不相关**，但反之不成立  
  - **例外**：多元正态分布中，分量不相关 ⇔ 分量独立

#### 其他概念  
- 矩的定义  
- 协方差矩阵  
- **多元正态分布的4条性质**（需灵活应用）
