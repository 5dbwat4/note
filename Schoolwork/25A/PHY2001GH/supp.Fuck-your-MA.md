---
title: "Supplement: Fuck your Math Analysis Ability"
---

# 积分咋求

## Ref-Ch25-1

$$
F_z = \frac{1}{4\pi\epsilon_0} q_0 2\pi\sigma z \int_0^R \frac{\omega d\omega}{(z^2 + \omega^2)^{3/2}} 
$$
$$
 = \frac{1}{4\pi\epsilon_0} \frac{2q_0 q}{R^2} \left(1 - \frac{z}{\sqrt{z^2 + R^2}}\right)
$$


关键是要计算积分：
$$
I = \int_0^R \frac{\omega d\omega}{(z^2 + \omega^2)^{3/2}}
$$
这是一个标准积分，可以通过变量替换法求解。令：
$$
u = z^2 + \omega^2
$$
则：
$$
du = 2\omega d\omega \quad \Rightarrow \quad \omega d\omega = \frac{du}{2}
$$
积分上下限变化：
- 当 $\omega = 0$ 时， $u = z^2$
- 当 $\omega = R$ 时， $u = z^2 + R^2$

因此，积分变为：
$$
I = \int_{z^2}^{z^2 + R^2} \frac{1}{u^{3/2}} \cdot \frac{du}{2} = \frac{1}{2} \int_{z^2}^{z^2 + R^2} u^{-3/2} du
$$

现在计算 $\int u^{-3/2} du$:
$$
\int u^{-3/2} du = \int u^{-3/2} du = \frac{u^{-1/2}}{-1/2} = -2 u^{-1/2} = -\frac{2}{\sqrt{u}}
$$

所以：
$$
I = \frac{1}{2} \left[ -\frac{2}{\sqrt{u}} \right]_{z^2}^{z^2 + R^2} = \frac{1}{2} \left( -\frac{2}{\sqrt{z^2 + R^2}} + \frac{2}{\sqrt{z^2}} \right)
$$
由于 $z$ 是距离，通常假设 $z > 0$，所以 $\sqrt{z^2} = z$。简化得：
$$
I = \frac{1}{2} \left( \frac{2}{z} - \frac{2}{\sqrt{z^2 + R^2}} \right) = \frac{1}{z} - \frac{1}{\sqrt{z^2 + R^2}}
$$

将积分结果代回第一行公式：
$$
F_z = \frac{1}{4\pi\epsilon_0} q_0 2\pi\sigma z \left( \frac{1}{z} - \frac{1}{\sqrt{z^2 + R^2}} \right)
$$
简化括号内的表达式：
$$
2\pi\sigma z \left( \frac{1}{z} - \frac{1}{\sqrt{z^2 + R^2}} \right) = 2\pi\sigma \left( 1 - \frac{z}{\sqrt{z^2 + R^2}} \right)
$$
所以：
$$
F_z = \frac{1}{4\pi\epsilon_0} q_0 \cdot 2\pi\sigma \left( 1 - \frac{z}{\sqrt{z^2 + R^2}} \right)
$$

引入总电荷 $q$

圆盘的总电荷 $q$ 与面电荷密度 $\sigma$ 的关系为：
$$
q = \sigma \cdot \pi R^2 \quad \Rightarrow \quad \sigma = \frac{q}{\pi R^2}
$$
代入上式：
$$
2\pi\sigma = 2\pi \cdot \frac{q}{\pi R^2} = \frac{2q}{R^2}
$$
因此：
$$
F_z = \frac{1}{4\pi\epsilon_0} q_0 \cdot \frac{2q}{R^2} \left( 1 - \frac{z}{\sqrt{z^2 + R^2}} \right)
$$
这正好是第二行公式：
$$
F_z = \frac{1}{4\pi\epsilon_0} \frac{2q_0 q}{R^2} \left(1 - \frac{z}{\sqrt{z^2 + R^2}}\right)
$$
