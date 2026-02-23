# Chapter 17 / Oscillations

**频率 (Frequency, f)**： $f = \frac{1}{T}$。

简谐振子 (The Simple Harmonic Oscillator)

**势能 (Potential Energy)**：$U(x) = \frac{1}{2} kx^2$。

角频率$\omega = \sqrt{\frac{k}{m}}$

周期 $T = 2\pi \sqrt{\frac{m}{k}}$。

频率 $f = \frac{1}{T} = \frac{1}{2\pi} \sqrt{\frac{k}{m}}$。

#### 17-4 简谐运动中的能量 (Energy in Simple Harmonic Motion)

- **能量变化**：
  - 势能 $U = \frac{1}{2} kx^2$ 在 $x = \pm x_m$ 时达到最大值 $\frac{1}{2} kx_m^2$。
  - 动能 $K = \frac{1}{2}mv^2$ 在 $x = 0$ 时达到最大值 $\frac{1}{2} kx_m^2$。
  - 总机械能 $E = K + U = \frac{1}{2} kx_m^2$ 保持不变。
- **能量与振幅的关系**：简谐运动的总能量与振幅的平方成正比

#### 17-7 阻尼谐振子 (Damped Harmonic Motion)

- **阻尼力**：实际振动系统中存在阻尼力，导致振幅逐渐减小。
- **阻尼谐振子的运动方程**：
  - $\frac{d^2x}{dt^2} + \frac{b}{m}\frac{dx}{dt} + \frac{k}{m}x = 0$。
  - 解为 $x(t) = x_m e^{-bt/2m} \cos(\omega't + \phi)$，其中 $\omega' = \sqrt{\frac{k}{m} - \left(\frac{b}{2m}\right)^2}$。
- **阻尼时间常数 (Damping Time Constant)**：$\tau = \frac{2m}{b}$，表示振幅衰减到初始值 $\frac{1}{e}$ 的时间。


# Chapter 18 / Wave Motion


对于伸缩弦，波速 $v = \sqrt{\frac{F}{\mu}}$，其中 $F$ 为弦的张力，$\mu$ 为弦的线密度。

波动可以传输能量，能量的传输速率称为功率 $P$。

  - 平均功率 $P_{\text{av}} = \frac{1}{2} \mu \omega^2 y_m^2 v$

# Chapter 19 / Sound Wave

- 对于流体，声速的表达式为：$v = \sqrt{\frac{B}{\rho_0}}$
- 声波的功率可以通过流体元所受的力和速度来计算。平均功率为：$P_{av} = \frac{A (\Delta p_m)^2}{2 \rho_0 v}$
- 声波的强度（平均功率除以单位面积）为：$I = \frac{(\Delta p_m)^2}{2 \rho_0 v}$
- 为了方便比较不同强度的声音，引入了声级（SL）的概念，它是一个对数尺度，定义为：$SL = 10 \log \frac{I}{I_0}$（单位：分贝，dB）

n
多普勒效应的公式为： $f' = f \left( \frac{v \pm v_O}{v \mp v_S} \right)$

其中，$f'$是观察者听到的频率，$f$是声源的频率，$v$是声速，$v_O$是观察者的速度，$v_S$是声源的速度。正负号的选择取决于观察者和声源的运动方向。


- 对于两端开放的管子，驻波的波长为：$\lambda_n = \frac{2L}{n}$，$n = 1,2,3,\dots$
- 对于一端开放一端封闭的管子，驻波的波长为： $\lambda_n = \frac{4L}{n}$，$n = 1,3,5,\dots$