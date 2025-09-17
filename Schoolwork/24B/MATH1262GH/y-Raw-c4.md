## 4.1 定义：实部（Real Part）、$\text{Re}$，虚部（Imaginary Part）、$\text{Im}$

设 $z = a + bi$，其中 $a$ 和 $b$ 为实数。

-   $z$ 的实部，记作 $\text{Re}(z)$，定义为 $\text{Re}(z) = a$；
-   $z$ 的虚部，记作 $\text{Im}(z)$，定义为 $\text{Im}(z) = b$。

## 4.2 定义：复共轭（Complex Conjugate）、$\overline{z}$，绝对值（Absolute Value）、$|z|$

设 $z \in \mathbb{C}$。

-   $z$ 的复共轭，记作 $\overline{z}$，定义为
    $\overline{z} = \text{Re}(z) - \left( \text{Im}(z) \right)i$。
-   复数 $z$ 的绝对值，记作 $|z|$，定义为
    $|z| = \sqrt{\left( \text{Re}(z) \right)^{2} + \left( \text{Im}(z) \right)^{2}}$。

## 4.4 复数的性质

设 $z,w \in \mathbb{C}$，以下等式和不等式成立：

1.  ​**和**：$z + w = 2\text{Re}(z)$。
2.  ​**差**：$z - w = 2\left( \text{Im}(z) \right)i$。
3.  ​**积**：$zw = |z|^{2}$。
4.  ​**复共轭的可加性**：$\overline{z + w} = \overline{z} + \overline{w}$。
5.  ​**复共轭的可乘性**：$\overline{zw} = \overline{z}\,\overline{w}$。
6.  ​**复共轭的复共轭**：$\overline{\overline{z}} = z$。
7.  ​**实部与虚部的界限**：$\left| \text{Re}(z) \right| \leq |z|$ 且
    $\left| \text{Im}(z) \right| \leq |z|$。
8.  ​**复共轭的绝对值**：$\left| \overline{z} \right| = |z|$。
9.  ​**绝对值的可乘性**：$|zw| = |z||w|$。
10. ​**三角不等式**：$|z + w| \leq |z| + |w|$。

## 4.6 定理：多项式的每个零点对应一个一次因式

设 $n$ 为正整数，$p \in P\left( \mathbb{F} \right)$ 是次数为 $n$
的多项式，$z_{0} \in \mathbb{F}$。则 $p\left( z_{0} \right) = 0$
当且仅当存在次数为 $n - 1$ 的多项式
$q \in P\left( \mathbb{F} \right)$，使得对任意 $z \in \mathbb{F}$，有
$p(z) = \left( z - z_{0} \right)q(z)$。

## 4.8 定理：次数为 $n$ 表明最多有 $n$ 个零点

设 $n$ 为正整数，$p \in P\left( \mathbb{F} \right)$ 是次数为 $n$
的多项式。则 $p$ 在 $\mathbb{F}$ 中至多有 $n$ 个零点。

## 4.9 定理：多项式的带余除法

设 $f,g \in P\left( \mathbb{F} \right)$ 且
$g \neq 0$。则存在唯一的多项式
$q,r \in P\left( \mathbb{F} \right)$，使得 $f = qg + r$ 且
$\deg(r) < \deg(g)$。

## 4.12 定理：代数基本定理（第一版）

每个非常值的复系数多项式在 $\mathbb{C}$ 中有零点。

## 4.13 定理：代数基本定理（第二版）

若 $p \in P\left( \mathbb{C} \right)$ 是非常数多项式，则存在唯一的
$c \in \mathbb{C}$ 和互异的 $z_{1},\ldots,z_{m} \in \mathbb{C}$，使得
$p(z) = c\left( z - z_{1} \right)\cdots\left( z - z_{m} \right)$。

## 4.14 定理：实系数多项式的非实零点成对出现

设 $p \in P\left( \mathbb{C} \right)$ 是实系数多项式，若
$z \in \mathbb{C}$ 是 $p$ 的零点，则 $\overline{z}$ 也是 $p$ 的零点。

## 4.15 定理：二次多项式的分解

设 $a,b \in \mathbb{R}$，则当且仅当 $b^{2} \geq 4ac$ 时，存在
$r_{1},r_{2} \in \mathbb{R}$ 使得
$ax^{2} + bx + c = \left( x - r_{1} \right)\left( x - r_{2} \right)$。

## 4.16 定理：实系数多项式的分解

设 $p \in P\left( \mathbb{R} \right)$ 是非常数多项式，则存在唯一的
$c \in \mathbb{R}$ 和互异的
$z_{1},\ldots,z_{m},s_{1},t_{1},\ldots,s_{k},t_{k} \in \mathbb{R}$，使得
$p(z) = c\left( z - z_{1} \right)\cdots\left( z - z_{m} \right)\left( z^{2} + s_{1}z + t_{1} \right)\cdots\left( z^{2} + s_{k}z + t_{k} \right)$，且对每个
$j$，$s_{j}^{2} < 4t_{j}$。
