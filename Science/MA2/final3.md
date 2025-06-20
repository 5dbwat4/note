# 数学分析 II 总复习

**授课人：朱家骏**
**日期：2025 年 6 月 9 日**

## 1 级数

### 1.1 数项级数

1. **定义**  
   给定一个数列 $\{u_n\}$，对它的各项依次用“+”号连接起来的表达式
   $$
   u_1 + u_2 + \cdots + u_n + \cdots
   $$
   称为数项级数或无穷级数（简称级数），记作 $\sum_{n=1}^{\infty} u_n$ 或 $\sum u_n$，其中 $u_n$ 称为通项。

2. **收敛与发散**  
   若级数的部分和数列 $\{S_n\}$ 收敛于 $S$（即 $\lim_{n \to \infty} S_n = S$），则称级数收敛，$S$ 称为级数的和，记作
   $$
   S = \sum_{n=1}^{\infty} u_n.
   $$
   若 $\{S_n\}$ 发散，则称级数发散。

3. **柯西准则**  
   级数 $\sum u_n$ 收敛的充要条件是：$\forall \epsilon > 0$，$\exists N \in \mathbb{N}$，使得当 $m > N$ 且 $p \in \mathbb{N}$ 时，
   $$
   |u_{m+1} + u_{m+2} + \cdots + u_{m+p}| < \epsilon.
   $$
   反之，级数发散的充要条件是存在某 $\epsilon_0 > 0$，对任何 $N$，$\exists m_0 > N$ 和 $p_0$，使得
   $$
   |u_{m_0+1} + \cdots + u_{m_0+p_0}| \geq \epsilon_0.
   $$
   由此可得：若级数收敛，则 $\lim_{n \to \infty} u_n = 0$。

4. **线性性质**  
   若 $\sum u_n$ 和 $\sum v_n$ 收敛，$c, d$ 为常数，则 $\sum (c u_n + d v_n)$ 也收敛，且
   $$
   \sum (c u_n + d v_n) = c \sum u_n + d \sum v_n.
   $$

5. **有限项的改变**  
   去掉、增加或改变级数的有限个项不改变其敛散性。

6. **加括号**  
   在收敛级数中任意加括号，既不改变收敛性，也不改变其和。

7. **正项级数判别法**  
   - **正项级数收敛的充要条件**：部分和数列有界。
   - **比较判别法**：若 $u_n \leq v_n$ 对 $n > N$ 成立，则 $\sum v_n$ 收敛 $\Rightarrow \sum u_n$ 收敛；$\sum u_n$ 发散 $\Rightarrow \sum v_n$ 发散。
   - **极限形式**：若 $\lim_{n \to \infty} \frac{u_n}{v_n} = l$，则：
     - $0 < l < +\infty$ 时，$\sum u_n$ 与 $\sum v_n$ 同敛散；
     - $l = 0$ 且 $\sum v_n$ 收敛时，$\sum u_n$ 收敛；
     - $l = +\infty$ 且 $\sum v_n$ 发散时，$\sum u_n$ 发散。
   - **比式判别法**：若 $\lim_{n \to \infty} \frac{u_{n+1}}{u_n} = q$，则 $q < 1$ 时收敛，$q > 1$ 时发散。
   - **根式判别法**：若 $\lim_{n \to \infty} \sqrt[n]{u_n} = l$，则 $l < 1$ 时收敛，$l > 1$ 时发散。
   - **积分判别法**：若 $f(x)$ 非负递减，则 $\sum f(n)$ 与 $\int_{1}^{\infty} f(x) \, \mathrm{d}x$ 同敛散。

8. **一般项级数判别法**  
   - **绝对收敛与条件收敛**：若 $\sum |u_n|$ 收敛，则 $\sum u_n$ 绝对收敛；若 $\sum u_n$ 收敛但 $\sum |u_n|$ 发散，则条件收敛。
   - **莱布尼茨判别法**：若交错级数 $\sum (-1)^{n+1} u_n$ 满足 $u_n$ 单调递减且 $\lim_{n \to \infty} u_n = 0$，则收敛。
   - **阿贝尔判别法**：若 $\{a_n\}$ 单调有界且 $\sum b_n$ 收敛，则 $\sum a_n b_n$ 收敛。
   - **狄利克雷判别法**：若 $\{a_n\}$ 单调趋于零且 $\sum b_n$ 的部分和有界，则 $\sum a_n b_n$ 收敛。

### 1.2 函数项级数

1. **函数列的一致收敛性**  
   - **定义**：若 $\forall \epsilon > 0$，$\exists N$ 使得当 $n > N$ 时，$\forall x \in D$ 有 $|f_n(x) - f(x)| < \epsilon$，则称 $\{f_n\}$ 在 $D$ 上一致收敛于 $f$。
   - **柯西准则**：$\{f_n\}$ 一致收敛的充要条件是 $\forall \epsilon > 0$，$\exists N$ 使得当 $n, m > N$ 时，$\forall x \in D$ 有 $|f_n(x) - f_m(x)| < \epsilon$。
   - **充要条件**：$\lim_{n \to \infty} \sup_{x \in D} |f_n(x) - f(x)| = 0$。

2. **函数项级数的一致收敛性**  
   - **定义**：若部分和函数列 $\{S_n(x)\}$ 一致收敛于 $S(x)$，则称 $\sum u_n(x)$ 在 $D$ 上一致收敛。
   - **柯西准则**：$\forall \epsilon > 0$，$\exists N$ 使得当 $n > N$ 时，$\forall x \in D$ 和 $p \in \mathbb{N}$ 有 $|S_{n+p}(x) - S_n(x)| < \epsilon$。
   - **充要条件**：$\lim_{n \to \infty} \sup_{x \in D} |R_n(x)| = 0$，其中 $R_n(x) = S(x) - S_n(x)$。

3. **一致收敛判别法**  
   - **维尔斯特拉斯判别法（M 判别法）**：若 $|u_n(x)| \leq M_n$ 且 $\sum M_n$ 收敛，则 $\sum u_n(x)$ 一致收敛。
   - **阿贝尔判别法**：若 $\sum u_n(x)$ 一致收敛，$\{v_n(x)\}$ 单调一致有界，则 $\sum u_n(x) v_n(x)$ 一致收敛。
   - **狄利克雷判别法**：若 $\sum u_n(x)$ 的部分和一致有界，$\{v_n(x)\}$ 单调趋于零，则 $\sum u_n(x) v_n(x)$ 一致收敛。

4. **一致收敛的性质**  
   - **连续性**：若 $\{f_n\}$ 一致收敛且每项连续，则极限函数连续。
   - **可积性**：若 $\{f_n\}$ 一致收敛且每项连续，则 $\lim_{n \to \infty} \int_a^b f_n(x) \, \mathrm{d}x = \int_a^b \lim_{n \to \infty} f_n(x) \, \mathrm{d}x$。
   - **可微性**：若 $\{f_n\}$ 收敛且每项有连续导数，$\{f'_n\}$ 一致收敛，则 $(\lim f_n)'$ = $\lim f'_n$。

### 1.3 幂级数

1. **收敛半径与区域**  
   - **阿贝尔第一定理**：若 $\sum a_n x^n$ 在 $x = x_0$ 收敛，则在 $|x| < |x_0|$ 绝对收敛；若在 $x = \eta_0$ 发散，则在 $|x| > |\eta_0|$ 发散。
   - **收敛半径 $R$ 的求法**：
     - 若 $\lim_{n \to \infty} \sqrt[n]{|a_n|} = \rho$，则 $R = \frac{1}{\rho}$（$\rho \neq 0, +\infty$）。
     - 若 $\lim_{n \to \infty} \left|\frac{a_{n+1}}{a_n}\right| = \rho$，则 $R = \frac{1}{\rho}$。

2. **幂级数的性质**  
   - **阿贝尔第二定理**：幂级数在 $(-R, R)$ 内闭一致收敛。
   - 若在端点收敛，则在包含该端点的闭区间上一致收敛。
   - 和函数在收敛区间内连续、可积、可微，且可逐项求导和积分。

3. **幂级数展开**  
   - **函数可展开为幂级数的充要条件**：泰勒余项 $R_n(x) \to 0$。
   - **唯一性**：若 $f(x) = \sum a_n (x - x_0)^n$，则展开式唯一。
   - **常见展开式**：
     $$
     e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}, \\ \sin x = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n + 1)!}, \\ \cos x = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!}, \\ \ln(1 + x) = \sum_{n=1}^{\infty} \frac{(-1)^{n-1} x^n}{n}.
     $$

### 1.4 傅里叶级数

1. **正交函数系**  
   若 $\int_a^b f_n(x) f_m(x) \, \mathrm{d}x = 0$（$n \neq m$），则 $\{f_n(x)\}$ 称为正交函数系。

2. **三角函数系**  
   $\{1, \cos x, \sin x, \cos 2x, \sin 2x, \ldots\}$ 是 $[-π, π]$ 上的正交函数系。

3. **傅里叶系数**  
   若 $f(x)$ 可展开为一致收敛的三角级数，则
   $$
   a_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos nx \, \mathrm{d}x, \quad b_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin nx \, \mathrm{d}x.
   $$

4. **收敛定理**  
   若 $f(x)$ 按段光滑，则其傅里叶级数收敛于 $\frac{f(x+0) + f(x-0)}{2}$。

5. **奇偶函数的傅里叶级数**  
   - **偶函数**：$b_n = 0$，级数为余弦级数。
   - **奇函数**：$a_n = 0$，级数为正弦级数。

6. **周期为 $2l$ 的函数**  
   傅里叶系数为
   $$
   a_n = \frac{1}{l} \int_{-l}^{l} f(x) \cos \frac{n \pi x}{l} \, \mathrm{d}x, \quad b_n = \frac{1}{l} \int_{-l}^{l} f(x) \sin \frac{n \pi x}{l} \, \mathrm{d}x.
   $$

7. **逐项积分与微分**  
   在适当条件下，傅里叶级数可逐项积分或微分。

8. **一致收敛定理**  
   若 $f(x)$ 连续且按段光滑，则其傅里叶级数绝对且一致收敛于 $f(x)$。

## 2 多元函数微分学

### 2.1 多元函数的极限与连续

1. 平面点集与多元函数
  - 点的分类：
    - 内点：存在邻域 $U(A) \subset E$.
    - 外点：存在邻域 $U(A) \cap E = \emptyset$.
    - 界点：任何邻域内既有属于 $E$ 的点，也有不属于 $E$ 的点.
    - 聚点：任何空心邻域 $U^\circ(A)$ 内含有 $E$ 的点.
    - 孤立点：属于 $E$ 但不是聚点.
  - 特殊点集：
    - 开集：每一点都是内点.
    - 闭集：所有聚点属于 $E$.
    - 开域：非空开集且连通.
    - 闭域：开域连同其边界.
    - 区域：开域、闭域或开域加部分界点.
  - 完备性定理：
    - 点列收敛的柯西准则.
    - 闭域套定理：闭域列 $\{D_n\}$ 满足 $D_n \supseteq D_{n+1}$ 且 $d_n \to 0$，则存在唯一公共点.
    - 聚点定理：有界无限点集必有聚点.
    - 有限覆盖定理：有界闭域的开覆盖必有有限子覆盖.
  - 二元函数定义：$f : D \subset \mathbb{R}^2 \to \mathbb{R}$，记作 $z = f(x, y)$.
2. 二元函数的极限
  - 定义：$\lim_{(x,y) \to (x_0,y_0)} f(x, y) = A$ 表示 $\forall \epsilon > 0$，$\exists \delta > 0$，当 $0 < \sqrt{(x - x_0)^2 + (y - y_0)^2} < \delta$ 时，$|f(x, y) - A| < \epsilon$.
  - 重要定理：
    - 极限存在的充要条件：所有路径极限存在且相等.
    - 累次极限与二重极限的关系：若二重极限和累次极限均存在，则三者相等.
  - 四则运算：与一元函数类似.
3. 二元函数的连续性
  - 定义：$f$ 在 $P_0$ 连续当且仅当 $\lim_{P \to P_0} f(P) = f(P_0)$.
  - 复合函数连续性：若 $u = \phi(x, y)$ 和 $v = \psi(x, y)$ 在 $P_0$ 连续，$z = f(u, v)$ 在 $(u_0, v_0)$ 连续，则 $z = f(\phi, \psi)$ 在 $P_0$ 连续.
  - 有界闭域上连续函数的性质：
    - 有界性与最值定理.
    - 一致连续性定理.
    - 介值定理.

### 2.2 偏导数与全微分

1. 偏导数与全微分
  - 偏导数定义：
    $$
    f'_x(x_0, y_0) = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x, y_0) - f(x_0, y_0)}{\Delta x}.
    $$
  - 全微分定义：$\Delta z = A \Delta x + B \Delta y + o(\rho)$，其中 $\rho = \sqrt{\Delta x^2 + \Delta y^2}$，记$\mathrm{d}z = A \Delta x + B \Delta y$.
  - 可微的必要条件：若 $f$ 可微，则偏导数存在且 $A = f'_x$, $B = f'_y$.
  - 可微的充分条件：偏导数连续 $\Rightarrow$ 可微.
2. 复合函数的偏导数与高阶偏导数
  - 链式法则：$\frac{\partial z}{\partial s} = \frac{\partial z}{\partial x} \frac{\partial x}{\partial s} + \frac{\partial z}{\partial y} \frac{\partial y}{\partial s}$.
  - 一阶微分形式不变性：无论 $x, y$ 是自变量还是中间变量，$\mathrm{d}z = \frac{\partial z}{\partial x} \mathrm{d}x + \frac{\partial z}{\partial y} \mathrm{d}y$.
  - 高阶偏导数：若混合偏导数连续，则求导顺序可交换（$f_{xy} = f_{yx}$）.
3. 隐函数存在定理
  - 隐函数存在唯一性定理：若 $F(x_0, y_0) = 0$ 且 $F'_y(x_0, y_0) \neq 0$，则方程 $F(x, y) = 0$ 在 $P_0$ 邻域内唯一确定连续可微函数 $y = f(x)$，且
    $$
    \frac{\mathrm{d}y}{\mathrm{d}x} = -\frac{F'_x}{F'_y}.
    $$
  - 推广到多元函数：类似条件可确定 $y = f(x_1, \ldots, x_n)$.
  - 隐函数组定理：若雅可比行列式 $\frac{\partial (F, G)}{\partial (u, v)} = 0$，则方程组 $\{F = 0, G = 0\}$ 可解出 $u = f(x, y)$, $v = g(x, y)$.

### 2.3 多元微分学的应用

1. 泰勒定理
  $$
  f(x_0 + h, y_0 + k) = \sum_{m=0}^{n} \frac{1}{m!} \left( h \frac{\partial}{\partial x} + k \frac{\partial}{\partial y} \right)^m f(x_0, y_0) + R_n.
  $$
2. 极值
  - 必要条件：极值点处 $f'_x = f'_y = 0$（稳定点）.
  - 充分条件：设 $A = f''_{xx}$, $B = f''_{xy}$, $C = f''_{yy}$，
    - $B^2 - AC < 0$ 且 $A > 0$：极小值；
    - $B^2 - AC < 0$ 且 $A < 0$：极大值；
    - $B^2 - AC > 0$：非极值.
3. 几何应用
  - 平面曲线切线：$F'_x (x - x_0) + F'_y (y - y_0) = 0$.
  - 空间曲线切线：参数方程形式或隐函数组形式.
  - 曲面切平面：$F'_x (x - x_0) + F'_y (y - y_0) + F'_z (z - z_0) = 0$.
4. 条件极值
  - 拉格朗日乘数法：对 $f(x, y, z)$ 约束 $\varphi(x, y, z) = 0$，构造
    $$
    L = f + \lambda \varphi,
    $$
    解方程组 $L'_x = L'_y = L'_z = L'_\lambda = 0$.

## 3 重积分

### 3.1 二重积分

1. 定义：
  - 设 $f(x, y)$ 定义在可求面积的有界闭区域 $D$ 上，对 $D$ 的分割 $T$，积分和 $\sum f(\xi_i, \eta_i) \Delta \sigma_i$ 的极限 $\lim_{\|T\| \to 0} \sum f(\xi_i, \eta_i) \Delta \sigma_i = J$ 若存在且与分割和取点无关，则称 $f$ 在 $D$ 上可积，记为
    $$
    \iint_D f(x, y) \, d\sigma.
    $$
2. 性质：
  - 有界性：可积函数必有界.
  - 线性性：$\iint_D (k f + l g) \, d\sigma = k \iint_D f \, d\sigma + l \iint_D g \, d\sigma$.
  - 区域可加性：若 $D = D_1 \cup D_2$ 且 $D_1 \cap D_2$ 内部为空，则 $\iint_D f \, d\sigma = \iint_{D_1} f \, d\sigma + \iint_{D_2} f \, d\sigma$.
  - 单调性：若 $f \leq g$，则 $\iint_D f \, d\sigma \leq \iint_D g \, d\sigma$.
  - 积分中值定理：若 $f$ 连续，$g$ 可积且不变号，则存在 $(\xi, \eta) \in D$ 使得 $\iint_D f g \, d\sigma = f(\xi, \eta) \iint_D g \, d\sigma$.
3. 可积条件：
  - 充要条件：$\forall \epsilon > 0$，存在分割 $T$ 使得 $\sum \omega_i \Delta \sigma_i < \epsilon$（$\omega_i$ 为振幅）.
  - 充分条件：
    - $f$ 连续.
    - $f$ 有界且不连续点分布在有限条光滑曲线上.
4. 简单区域：
  - $x$ 型区域：$D = \{(x, y) \mid a \leq x \leq b, y_1(x) \leq y \leq y_2(x)\}$.
  - $y$ 型区域：$D = \{(x, y) \mid c \leq y \leq d, x_1(y) \leq x \leq x_2(y)\}$.
5. 计算公式：
  - 累次积分：
    $$
    \iint_D f \, d\sigma = \int_{a}^{b} \left( \int_{y_1(x)}^{y_2(x)} f \, \mathrm{d}y \right) \mathrm{d}x \quad (x \text{ 型区域}).
    $$
  - 变量替换：
    $$
    \iint_D f(x, y) \, d\sigma = \iint_{D'} f(x(u, v), y(u, v)) \left| \frac{\partial (x, y)}{\partial (u, v)} \right| \, du \, dv.
    $$
  - 极坐标变换：
    $$
    \iint_D f(x, y) \, d\sigma = \iint_{D'} f(r \cos \theta, r \sin \theta) \cdot r \, dr \, d\theta.
    $$
6. 特殊结果：
  - $\iint_{[a,b] \times [a,b]} f(x) f(y) \, \mathrm{d}x \, \mathrm{d}y = \left( \int_{a}^{b} f(x) \, \mathrm{d}x \right)^2$.
  - $\iint_{x^2 + y^2 \leq 1} f(a x + b y) \, \mathrm{d}x \, \mathrm{d}y = 2 \int_{-1}^{1} \sqrt{1 - x^2} f(\sqrt{a^2 + b^2} \cdot x) \, \mathrm{d}x$.

### 3.2 三重积分

1. 定义：
  - 设 $f(x, y, z)$ 定义在可求体积的有界闭区域 $V$ 上，积分和 $\sum f(\xi_i, \eta_i, \zeta_i) \Delta V_i$ 的极限 $\lim_{\|T\| \to 0} \sum f(\xi_i, \eta_i, \zeta_i) \Delta V_i = J$ 若存在且与分割和取点无关，则称 $f$ 在 $V$ 上可积，记为
    $$
    \iiint_V f(x, y, z) \, dV.
    $$
2. 性质：
  - 线性性、区域可加性、单调性、积分中值定理与二重积分类似.
3. 简单区域：
  - $z$ 型区域：$V = \{(x, y, z) \mid (x, y) \in D_{xy}, f_1(x, y) \leq z \leq f_2(x, y)\}$.
  - 截面区域：$V = \{(x, y, z) \mid c \leq z \leq d, (x, y) \in D(z)\}$.
4. 计算公式：
  - 累次积分：
    $$
    \iiint_V f \, dV = \int_{a}^{b} \left( \int_{y_1(x)}^{y_2(x)} \left( \int_{z_1(x, y)}^{z_2(x, y)} f \, \mathrm{d}z \right) \mathrm{d}y \right) \mathrm{d}x.
    $$
  - 变量替换：
    $$
    \iiint_V f \, dV = \iiint_{V'} f(x(u, v, w), y(u, v, w), z(u, v, w)) \left| \frac{\partial (x, y, z)}{\partial (u, v, w)} \right| \, du \, dv \, dw.
    $$
  - 柱坐标变换：
    $$
    \iiint_V f \, dV = \iiint_{V'} f(r \cos \theta, r \sin \theta, z) \cdot r \, dr \, d\theta \, \mathrm{d}z.
    $$
  - 球坐标变换：
    $$
    \iiint_V f \, dV = \iiint_{V'} f(r \sin \varphi \cos \theta, r \sin \varphi \sin \theta, r \cos \varphi) \cdot r^2 \sin \varphi \, dr \, d\theta \, d\varphi.
    $$
5. 特殊结果：
  - $\iiint_{x^2 + y^2 + z^2 \leq 1} f(a x + b y + c z + d) \, dV = \pi \int_{-1}^{1} f(k x) (1 - x^2) \, \mathrm{d}x$，其中 $k = \sqrt{a^2 + b^2 + c^2}$.

## 4 曲线积分与曲面积分

### 4.1 第一型曲线积分与曲面积分

1. 定义：
  - 第一型曲线积分：设 $L$ 为可求长曲线，$f$ 定义在 $L$ 上，积分和 $\sum f(P_i) \Delta s_i$ 的极限 $\lim_{\|T\| \to 0} \sum f(P_i) \Delta s_i = J$ 若存在且与分割和取点无关，则称 $f$ 沿 $L$ 可积，记为
    $$
    \int_L f \, \mathrm{d}s.
    $$
  - 第一型曲面积分：设 $S$ 为光滑曲面，$f$ 定义在 $S$ 上，积分和 $\sum f(\xi_i, \eta_i, \zeta_i) \Delta S_i$ 的极限 $\lim_{\|T\| \to 0} \sum f(\xi_i, \eta_i, \zeta_i) \Delta S_i = J$ 若存在且与分割和取点无关，则称 $f$ 沿 $S$ 可积，记为
    $$
    \iint_S f \, \mathrm{d}s.
    $$
2. 性质：
  - 线性性、区域可加性、单调性等与定积分类似.
3. 计算公式：
  - 曲线积分：
    - 平面曲线 $L$ :
      $$
      \begin{cases}
      x = \varphi(t), \\
      y = \psi(t), \quad a \leq t \leq b
      \end{cases}
      $$
      $$
      \int_L f(x, y) \, \mathrm{d}s = \int_{a}^{b} f(\varphi(t), \psi(t)) \sqrt{\varphi'(t)^2 + \psi'(t)^2} \, \mathrm{d}t.
      $$
    - 空间曲线 $L$ :
      $$
      \begin{cases}
      x = \varphi(t), \\
      y = \psi(t), \\
      z = h(t), \quad a \leq t \leq b
      \end{cases}
      $$
      $$
      \int_L f(x, y, z) \, \mathrm{d}s = \int_{a}^{b} f(\varphi(t), \psi(t), h(t)) \sqrt{\varphi'(t)^2 + \psi'(t)^2 + h'(t)^2} \, \mathrm{d}t.
      $$
  - 曲面积分：
    - 曲面 $S$ : $z = z(x, y)$, $(x, y) \in D$：
      $$
      \iint_S f(x, y, z) \, \mathrm{d}s = \iint_D f(x, y, z(x, y)) \sqrt{1 + z_x'^2 + z_y'^2} \, \mathrm{d}x \, \mathrm{d}y.
      $$
    - 曲面 $S$ 参数方程：
      $$
      \begin{cases}
      x = x(u, v), \\
      y = y(u, v), \\
      z = z(u, v), \quad (u, v) \in \Delta
      \end{cases}
      $$
      $$
      \iint_S f \, \mathrm{d}s = \iint_{\Delta} f(x(u, v), y(u, v), z(u, v)) \sqrt{E G - F^2} \, du \, dv,
      $$
      其中 $E = x_u'^2 + y_u'^2 + z_u'^2$, $G = x_v'^2 + y_v'^2 + z_v'^2$, $F = x_u' x_v' + y_u' y_v' + z_u' z_v'$.

### 4.2 第二型曲线积分与曲面积分

1. 定义：
  - 第二型曲线积分：设 $L$ 为有向光滑曲线，$P, Q, R$ 定义在 $L$ 上，积分和 $\sum P \Delta x_i + Q \Delta y_i + R \Delta z_i$ 的极限若存在，记为
    $$
    \int_{L} P \, \mathrm{d}x + Q \, \mathrm{d}y + R \, \mathrm{d}z.
    $$
  - 第二型曲面积分：设 $S$ 为有向光滑曲面，$P, Q, R$ 定义在 $S$ 上，积分和 $\sum P (\Delta S_i)_{yz} + Q (\Delta S_i)_{xz} + R (\Delta S_i)_{xy}$ 的极限若存在，记为
    $$
    \iint_{S} P \, \mathrm{d}y \, \mathrm{d}z + Q \, \mathrm{d}z \, \mathrm{d}x + R \, \mathrm{d}x \, \mathrm{d}y.
    $$
2. 性质：
  - 有向性：反向积分取负号.
3. 与第一型积分的关系：
  - 曲线积分：$\int_{L} P \, \mathrm{d}x + Q \, \mathrm{d}y = \int_{L} (P \cos \alpha + Q \cos \beta) \, \mathrm{d}s$，其中 $\alpha, \beta$ 为切向量的方向角.
  - 曲面积分：$\iint_{S} P \, \mathrm{d}y \, \mathrm{d}z + Q \, \mathrm{d}z \, \mathrm{d}x + R \, \mathrm{d}x \, \mathrm{d}y = \iint_{S} (P \cos \alpha + Q \cos \beta + R \cos \gamma) \, \mathrm{d}s$，其中 $\alpha, \beta, \gamma$ 为法向量的方向角.
4. 计算公式：
  - 曲线积分：
    - 平面曲线 $L$ :
      $$
      \begin{cases}
      x = \varphi(t), \\
      y = \psi(t), \quad \alpha \leq t \leq \beta
      \end{cases}
      $$
      $$
      \int_{L} P \, \mathrm{d}x + Q \, \mathrm{d}y = \int_{\alpha}^{\beta} \left[ P(\varphi(t), \psi(t)) \varphi'(t) + Q(\varphi(t), \psi(t)) \psi'(t) \right] \mathrm{d}t.
      $$
  - 曲面积分：
    - 曲面 $S$ : $z = z(x, y)$, $(x, y) \in D$：
      $$
      \iint_{S} R \, \mathrm{d}x \, \mathrm{d}y = \iint_{D} R(x, y, z(x, y)) \, \mathrm{d}x \, \mathrm{d}y \quad (\text{上侧取正}).
      $$
5. 重要定理：
  - 格林公式：
    $$
    \oint_{L} P \, \mathrm{d}x + Q \, \mathrm{d}y = \iint_{D} \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, \mathrm{d}x \, \mathrm{d}y.
    $$
  - 奥高公式：
    $$
    \oiint_{S} P \, \mathrm{d}y \, \mathrm{d}z + Q \, \mathrm{d}z \, \mathrm{d}x + R \, \mathrm{d}x \, \mathrm{d}y = \iiint_{V} \left( \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} + \frac{\partial R}{\partial z} \right) \, \mathrm{d}x \, \mathrm{d}y \, \mathrm{d}z.
    $$
  - 斯托克斯公式：
    $$
    \oint_{L} P \, \mathrm{d}x + Q \, \mathrm{d}y + R \, \mathrm{d}z = \oiint_{S} \begin{vmatrix}
    \mathrm{d}y \, \mathrm{d}z & \mathrm{d}z \, \mathrm{d}x & \mathrm{d}x \, \mathrm{d}y \\
    \frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\
    P & Q & R
    \end{vmatrix}.
    $$
6. 常用结果：
  - 平面区域面积：
    $$
    \Delta D = \frac{1}{2} \oint_{L} x \, \mathrm{d}y - y \, \mathrm{d}x.
    $$
  - 高斯积分：
    $$
    \oint_{L} \frac{x \, \mathrm{d}y - y \, \mathrm{d}x}{x^2 + y^2} =
    \begin{cases}
    0, & \text{不包围原点}, \\
    2\pi, & \text{包围原点}.
    \end{cases}
    $$
