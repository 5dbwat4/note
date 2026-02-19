# 电学

真空介电常数：$\varepsilon_0$ 是衡量真空中对电场形成“阻力”或“抵抗”能力的一个物理常数。$\varepsilon_0 \approx 8.854 \times 10^{-12} \ \text{C}^2 / \text{N} \cdot \text{m}^2$ 

**库伦定律（Coulomb's Law）** $\vec{F} = k \dfrac{q_1 q_2}{r^2} \hat{r}$,$k = \dfrac{1}{4 \pi \varepsilon_0}$

- **线密度**：$\lambda = \frac{q}{L},\quad dq = \lambda\,dx$
- **面密度**：$\sigma = \frac{q}{A},\quad dq = \sigma\,dA$
- **体密度**：$\rho = \frac{q}{V},\quad dq = \rho\,dV$

**电场强度** $\vec{E} = \dfrac{\vec{F}}{q_0}$, 对于点电荷 $= \dfrac{1}{4 \pi \varepsilon_0} \dfrac{q}{r^2} \hat{r}$

**电偶极矩**：$p = qd,\quad \vec{p} \text{ 方向：负→正}$ ($q$是单个电荷的电量，$d$是两电荷间距)

**电通量**：$\Phi_E = \int \vec{E} \cdot d\vec{A}$，其中 $d\vec{A}$ 是面积元向量，垂直于表面，大小等于面积元的面积。

**高斯定律（Gauss' Law）**：$\epsilon_0 \oint \vec{E} \cdot d\vec{A} = q_{\text{enc}}$ or $\Phi_E = \dfrac{Q_{\text{enc}}}{\varepsilon_0}$，其中 $Q_{\text{enc}}$ 是包围在闭合曲面内的总电荷。

- 两点间势能变化：$\Delta U = U_f - U_i = -W_{if} = -\int_i^f \vec{F} \cdot d\vec{s}$
- 两个点电荷系统的电势能（以无限远为参考点）：$U(r) = \frac{1}{4\pi\epsilon_0} \frac{q_1 q_2}{r}$
- **由电场求电势差**： $\Delta V = V_b - V_a = -\int_a^b \vec{E} \cdot d\vec{s}$
- **由电势求电场**（电场是电势的负梯度）：$E_x = -\frac{\partial V}{\partial x},\quad E_y = -\frac{\partial V}{\partial y},\quad E_z = -\frac{\partial V}{\partial z}$


导体在电场中-静态条件：导体**内部电场为零**

- **电流定义**：$i = \frac{dq}{dt}$，单位：安培（A）
- **电流密度**：$\vec{j} = \frac{i}{A} \hat{j}$，方向为正电荷流动方向
- **漂移速度**：$\vec{j} = -en\vec{v}_d$，$v_d = \frac{j}{ne}$

- **欧姆定律（微观）**：$\vec{j} = \sigma \vec{E}$，$\vec{E} = \rho \vec{j}$
- **电阻率**：$\rho = \frac{1}{\sigma}$，单位：$\Omega \cdot m$
- **电阻**：$R = \frac{\Delta V}{i} = \rho \frac{L}{A}$

绝缘体在电场中：会**极化**，形成**极化电场**，减弱外加电场，导致净电场：$E = E_0 - E' = \frac{E_0}{\kappa_e}$，**介电常数**：$\kappa_e > 1$，$\epsilon = \kappa_e \epsilon_0$，**介电强度**：击穿所需最大电场

**电容**: $C = \frac{Q}{\Delta V}$，单位：法拉（F）($\Delta V$: 电势差)

- **平行板电容器**：$C = \frac{\varepsilon_0 A}{d}$
- 球形电容器：$C = 4 \pi \varepsilon_0 \frac{ab}{b - a}$ (内半径 $a$，外半径 $b$)
- 圆柱形电容器：$C = \frac{2 \pi \varepsilon_0 L}{\ln(b/a)}$ (内半径 $a$，外半径 $b$，长度 $L$)

- **串联**：$\frac{1}{C_{\text{eq}}} = \sum \frac{1}{C_i}$
- **并联**：$C_{\text{eq}} = \sum C_i$

**电容器储能**： $U = \frac{1}{2} C (\Delta V)^2 = \frac{Q^2}{2C} = \frac{1}{2} Q \Delta V$，能量密度：$u = \frac{1}{2} \varepsilon_0 E^2$

含电介质：$C' = \kappa_e C$（电介质会增加电容）


**磁通量**（Magnetic Flux）：$\Phi_B = \int \vec{B} \cdot d\vec{A}$ 单位：韦伯（Weber, Wb），1 Wb = 1 T·m²

**法拉第定律**（Faraday’s Law）：感应电动势的大小：$\mathcal{E} = - \frac{d\Phi_B}{dt}$，负号表示感应电动势的方向总是**反抗磁通变化**（楞次定律）

导体棒在均匀磁场中垂直切割磁感线的情况：$\mathcal{E} = B L v$

长度为 $R$ 的导体绕一端在磁场中旋转：$\mathcal{E} = \frac{1}{2} B \omega R^2$


运动电荷在磁场中的受力：$\vec{F} = q \vec{v} \times \vec{B}$，$F = |q| v B \sin\phi$，$\phi$：$\overrightarrow{v}$ 与 $\overrightarrow{B}$ 的夹角

电荷在均匀磁场中的圆周运动：半径 $r = \frac{m v}{|q| B}$，周期 $T = \frac{2 \pi m}{|q| B}$

洛伦兹力（电场 + 磁场）：$\vec{F} = q \left( \vec{E} + \vec{v} \times \vec{B} \right)$

载流导线在磁场中的受力：$\vec{F} = i \vec{L} \times \vec{B}$，$F = i L B \sin\phi$

载流线圈在磁场中的力矩：$\tau = N i A B \sin\phi$


运动电荷产生的磁场：$\vec{B} = \frac{\mu_0}{4\pi} \cdot \frac{q \vec{v} \times \hat{r}}{r^2}$；电流元产生的磁场（毕奥-萨伐尔定律）：$d\vec{B} = \frac{\mu_0}{4\pi} \cdot \frac{i d\vec{l} \times \hat{r}}{r^2}$；$\mu_0$ 是真空磁导率，$\mu_0 = 4\pi \times 10^{-7} \ \text{T} \cdot \text{m/A}$

安培定律：$\oint \vec{B} \cdot d\vec{s} = \mu_0 i_{\text{enc}}$