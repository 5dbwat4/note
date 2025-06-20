> 什么是几何重数和代数重数？

在矩阵的特征值分析中，**代数重数（Algebraic Multiplicity, AM）** 和 **几何重数（Geometric Multiplicity, GM）** 是两个核心概念，它们揭示了特征值在矩阵结构中的不同层次信息。以下是详细解释：

---

### **一、代数重数（Algebraic Multiplicity, AM）**
1. **定义**：  
   - 特征值 $\lambda$ 的代数重数是它在 **特征多项式 $p_A(\lambda) = \det(A - \lambda I)$ 中作为根的重数**。  
   - 即若 $p_A(\lambda) = (\lambda - \lambda_i)^{m_i} \cdot q(\lambda)$，则 $\lambda_i$ 的代数重数为 $m_i$。

2. **性质**：  
   - 所有特征值的代数重数之和等于矩阵的阶数 $n$。  
   - 反映了特征值在**复平面上的重复次数**。

3. **示例**：  
   矩阵 $A = \begin{bmatrix} 3 & 1 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix}$ 的特征多项式为：  
   $$
   p_A(\lambda) = (3-\lambda)^2(5-\lambda)
   $$
   - $\lambda = 3$ 的代数重数 $AM = 2$，  
   - $\lambda = 5$ 的代数重数 $AM = 1$.

---

### **二、几何重数（Geometric Multiplicity, GM）**
1. **定义**：  
   - 特征值 $\lambda$ 的几何重数是其对应的 **特征空间 $\ker(A - \lambda I)$ 的维数**。  
   - 即线性无关特征向量的个数：  
     $$
     GM(\lambda) = \dim \{ \mathbf{v} \mid (A - \lambda I)\mathbf{v} = \mathbf{0} \}.
     $$

2. **性质**：  
   - $GM(\lambda)$ **等于 $\lambda$ 对应的 Jordan 块个数**。  
   - 几何重数满足：$1 \leq GM(\lambda) \leq AM(\lambda)$。

3. **示例**（续前）：  
   - 对 $\lambda = 3$：  
     $$
     A - 3I = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 2 \end{bmatrix} \implies \text{解空间：} x_2=0, x_3=0
     $$
     特征向量为 $[1, 0, 0]^\top$ → $GM(3) = 1$。  
   - 对 $\lambda = 5$：  
     $$
     A - 5I = \begin{bmatrix} -2 & 1 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & 0 \end{bmatrix} \implies \text{特征向量 } [0,0,1]^\top \implies GM(5)=1.
     $$

---

### **三、两者关系与意义**
#### **1. 核心不等式**  
$$
\boxed{1 \leq GM(\lambda) \leq AM(\lambda)}
$$  
- **几何重数 ≤ 代数重数**（重要！）。  
- **何时取等？**  
  - $GM(\lambda) = AM(\lambda)$ → 该特征值可对角化（有足够特征向量）。  
  - $GM(\lambda) < AM(\lambda)$ → 需补充广义特征向量（对应 Jordan 块）。

#### **2. 几何解释**
| **重数类型** | **物理意义**                          | **对应矩阵结构**               |
|--------------|--------------------------------------|-------------------------------|
| 代数重数 (AM) | 特征值在变换中的“总量”占比           | 特征值在 Jordan 块中的总出现次数 |
| 几何重数 (GM) | 特征值对应的独立方向个数             | Jordan 块的数量                |

> **直观比喻**：  
> - 代数重数：某颜色灯泡的总数。  
> - 几何重数：能独立放置该颜色灯泡的灯座数量。  
> - 若灯座不足（$GM < AM$），需在同一个灯座上串联多个灯泡（Jordan 块）。

#### **3. 与 Jordan 标准型的联系**
- **Jordan 块数量** = $GM(\lambda)$。  
- **最大 Jordan 块大小** = 满足 $\dim \ker(A - \lambda I)^k - \dim \ker(A - \lambda I)^{k-1} > 0$ 的最小 $k$。  

> **示例**（续）：  
> - $\lambda = 3$：$AM=2, GM=1$ → 有 1 个 Jordan 块（因 $GM=1$），块大小为 2（因 $AM=2$）。  
> - Jordan 型：$J = \begin{bmatrix} 3 & 1 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 5 \end{bmatrix}$。

---

### **四、计算示例**
**问题**：求矩阵 $A = \begin{bmatrix} 4 & 1 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & 4 \end{bmatrix}$ 的两种重数。
1. **代数重数**：  
   - 特征多项式 $p_A(\lambda) = (4-\lambda)^3$ → $\lambda=4$ 的 $AM=3$。  
2. **几何重数**：  
   - $A - 4I = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$ → 解空间需 $y=0$ → 特征向量基：$[1,0,0]^\top, [0,0,1]^\top$ → $GM=2$。  
3. **结论**：  
   - $GM=2 < AM=3$ → 存在 2 个 Jordan 块（一个 $1\times 1$，一个 $2\times 2$）。  
   - Jordan 型：$J = \begin{bmatrix} 4 & 1 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & 4 \end{bmatrix}$。

---

### **五、重要结论**
1. **可对角化条件**：  
   $$
   A \text{ 可对角化} \iff \forall \lambda_i,\ GM(\lambda_i) = AM(\lambda_i)
   $$
2. **Jordan 块结构**：  
   - 每个特征值 $\lambda_i$ 生成 $GM(\lambda_i)$ 个 Jordan 块。  
   - 所有 Jordan 块的阶数之和 = $AM(\lambda_i)$。  

---

### **总结**
- **代数重数**：特征值在特征多项式中的重数（总量信息）。  
- **几何重数**：特征向量的线性无关方向数（结构信息）。  
- **两者关系**：$1 \leq GM \leq AM$，差值决定了 Jordan 块的尺寸。  
掌握这对概念是理解矩阵不可对角化本质和 Jordan 标准型构造的基石！