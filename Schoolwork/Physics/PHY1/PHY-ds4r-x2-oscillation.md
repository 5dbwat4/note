以下是《普通物理学I教材.pdf》中关于“振动”章节的核心内容和知识点整理：

### 第17章：振动 (Oscillations)

#### 17-1 振动系统 (Oscillating Systems)
- **振动现象**：日常生活中常见的振动包括钟摆的摆动、蹦床上的人、吉他弦的振动等。微观世界中，石英晶体中的原子振动和空气分子的振动也是振动的例子。
- **振动的数学描述**：振动系统可以用正弦和余弦函数来描述，无论是机械振动还是电磁振动。
- **恢复力 (Restoring Force)**：振动系统中，无论物体朝哪个方向偏离平衡位置，恢复力总是将物体拉回平衡位置。
- **振动的基本参数**：
  - **振幅 (Amplitude)**：最大偏离平衡位置的距离。
  - **周期 (Period, T)**：完成一次完整振动所需的时间。
  - **频率 (Frequency, f)**：单位时间内完成的振动次数，与周期互为倒数，即 $f = \frac{1}{T}$。
  - **频率单位**：赫兹 (Hz)，1 Hz = 1 次/秒。

#### 17-2 简谐振子 (The Simple Harmonic Oscillator)
- **简谐运动 (Simple Harmonic Motion)**：当一个物体受到的力与其偏离平衡位置的距离成正比且方向相反时，物体的运动称为简谐运动。其数学表达式为 $F_x = -kx$，其中 $k$ 是比例常数。
- **简谐振子的能量**：
  - **势能 (Potential Energy)**：$U(x) = \frac{1}{2} kx^2$。
  - **动能 (Kinetic Energy)**：$K = \frac{1}{2}mv^2$。
  - **机械能守恒**：在无耗散力的情况下，总机械能 $E = K + U$ 保持不变。
- **简谐振子的运动方程**：
  - 运动方程为 $\frac{d^2x}{dt^2} + \frac{k}{m}x = 0$。
  - 解为 $x(t) = x_m \cos(\omega t + \phi)$，其中 $\omega = \sqrt{\frac{k}{m}}$ 是角频率，$x_m$ 是振幅，$\phi$ 是相位常数。

#### 17-3 简谐运动 (Simple Harmonic Motion)
- **简谐运动的特征**：
  - 位移、速度和加速度都是时间的正弦或余弦函数。
  - 位移的最大值为振幅 $x_m$。
  - 速度的最大值为 $\omega x_m$。
  - 加速度的最大值为 $\omega^2 x_m$。
- **简谐运动的周期和频率**：
  - 周期 $T = 2\pi \sqrt{\frac{m}{k}}$。
  - 频率 $f = \frac{1}{T} = \frac{1}{2\pi} \sqrt{\frac{k}{m}}$。
- **相位和相位常数**：相位 $(\omega t + \phi)$ 决定了振动的初始状态。

#### 17-4 简谐运动中的能量 (Energy in Simple Harmonic Motion)
- **能量变化**：
  - 势能 $U = \frac{1}{2} kx^2$ 在 $x = \pm x_m$ 时达到最大值 $\frac{1}{2} kx_m^2$。
  - 动能 $K = \frac{1}{2}mv^2$ 在 $x = 0$ 时达到最大值 $\frac{1}{2} kx_m^2$。
  - 总机械能 $E = K + U = \frac{1}{2} kx_m^2$ 保持不变。
- **能量与振幅的关系**：简谐运动的总能量与振幅的平方成正比。

#### 17-5 简谐运动的应用 (Applications of Simple Harmonic Motion)
- **扭摆振子 (Torsional Oscillator)**：一个圆盘通过一根细线悬挂，细线的扭转提供恢复力矩。其运动方程为 $\frac{d^2\theta}{dt^2} + \frac{\kappa}{I}\theta = 0$，其中 $\kappa$ 是扭转常数，$I$ 是转动惯量。
- **单摆 (Simple Pendulum)**：一个质点通过一根不可伸长的轻绳悬挂，其运动方程为 $\frac{d^2\theta}{dt^2} + \frac{g}{L}\theta = 0$（小角度近似），其中 $L$ 是摆长，$g$ 是重力加速度。
- **物理摆 (Physical Pendulum)**：任意刚体绕通过其自身的轴摆动，其运动方程为 $\frac{d^2\theta}{dt^2} + \frac{Mgd}{I}\theta = 0$，其中 $M$ 是质量，$d$ 是质心到轴的距离，$I$ 是转动惯量。

#### 17-6 简谐运动与匀速圆周运动 (Simple Harmonic Motion and Uniform Circular Motion)
- **简谐运动与圆周运动的关系**：简谐运动可以看作是匀速圆周运动在直径方向上的投影。
- **数学描述**：
  - 位移：$x(t) = r \cos(\omega t + \phi)$。
  - 速度：$v_x(t) = -\omega r \sin(\omega t + \phi)$。
  - 加速度：$a_x(t) = -\omega^2 r \cos(\omega t + \phi)$。

#### 17-7 阻尼谐振子 (Damped Harmonic Motion)
- **阻尼力**：实际振动系统中存在阻尼力，导致振幅逐渐减小。
- **阻尼谐振子的运动方程**：
  - $\frac{d^2x}{dt^2} + \frac{b}{m}\frac{dx}{dt} + \frac{k}{m}x = 0$。
  - 解为 $x(t) = x_m e^{-bt/2m} \cos(\omega't + \phi)$，其中 $\omega' = \sqrt{\frac{k}{m} - \left(\frac{b}{2m}\right)^2}$。
- **阻尼时间常数 (Damping Time Constant)**：$\tau = \frac{2m}{b}$，表示振幅衰减到初始值 $\frac{1}{e}$ 的时间。

#### 17-8 受迫振动与共振 (Forced Oscillations and Resonance)
- **受迫振动**：当外力以一定频率作用于振动系统时，系统会发生受迫振动，振动频率等于外力频率。
- **共振 (Resonance)**：当外力频率与系统的固有频率相等时，振动幅度达到最大。
- **共振条件**：$\omega_{\text{driving}} = \omega$。
- **能量传递**：在共振状态下，外力提供的能量与阻尼力消耗的能量相匹配，振幅保持不变。

#### 17-9 两体振动 (Two-Body Oscillations)
- **两体振动系统**：两个物体通过弹簧连接，其振动可以通过相对坐标和质心坐标来描述。
- **简化模型**：系统的振动可以简化为一个具有“约化质量”$\mu = \frac{m_1 m_2}{m_1 + m_2}$ 的单体振动。
- **振动频率**：系统的振动频率由 $\omega = \sqrt{\frac{k}{\mu}}$ 给出。

### 总结
本章详细介绍了振动的基本概念、简谐运动的特征、能量变化、以及振动系统的多种应用，包括扭摆振子、单摆、物理摆等。此外，还讨论了阻尼振动和受迫振动的现象，以及两体振动系统的简化方法。这些内容为理解物理系统中的振动行为提供了坚实的理论基础。