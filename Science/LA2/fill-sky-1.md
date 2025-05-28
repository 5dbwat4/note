---
title: 线代补天记录（1）
---
# 直线与方程

## 求异面直线距离

设异面直线 \( L_1 \) 和 \( L_2 \) 的参数方程为：  
\[
L_1: \boldsymbol{r_1} = \boldsymbol{a_1} + t\boldsymbol{v_1}, \quad L_2: \boldsymbol{r_2} = \boldsymbol{a_2} + s\boldsymbol{v_2},
\]  
其中：  
- \(\boldsymbol{a_1}, \boldsymbol{a_2}\) 分别为 \( L_1, L_2 \) 上的定点，  
- \(\boldsymbol{v_1}, \boldsymbol{v_2}\) 分别为 \( L_1, L_2 \) 的方向矢量，  

**原理**：分子是平行六面体的体积，分母是底面积，比值即为高（公垂线长度）。


| 直线关系       | 距离公式                                                                 |  
|----------------|--------------------------------------------------------------------------|  
| **异面直线**   | \(d = \frac{|\boldsymbol{P_1P_2} \cdot (\boldsymbol{v_1} \times \boldsymbol{v_2})|}{|\boldsymbol{v_1} \times \boldsymbol{v_2}|}\) |  
| **平行直线**   | \(d = \frac{|\boldsymbol{P_1P_2} \times \boldsymbol{v}|}{|\boldsymbol{v}|}\)                                           |  

## 求直线/平面

设出方向向量/法向量，然后和已知条件联立$\boldsymbol{v}\boldsymbol{n}=0$方程

## 点到直线的距离

**注意是叉乘**

**适用条件**：直线用参数式或对称式表示，如 \(L: \frac{x - x_0}{a} = \frac{y - y_0}{b} = \frac{z - z_0}{c}\)（方向向量 \(\boldsymbol{v} = (a, b, c)\)），点为 \(P(x_1, y_1, z_1)\)。  
**公式**：  
\[
d = \frac{|\overrightarrow{P_0P} \times \boldsymbol{v}|}{|\boldsymbol{v}|},
\]  
其中 \(P_0(x_0, y_0, z_0)\) 是直线上的定点，\(\overrightarrow{P_0P} = (x_1 - x_0, y_1 - y_0, z_1 - z_0)\) 为点 \(P\) 到 \(P_0\) 的向量，\(\times\) 表示向量叉乘。  
