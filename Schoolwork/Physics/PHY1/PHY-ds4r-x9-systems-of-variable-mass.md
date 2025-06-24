以下是关于可变质量系统动力学的分析，采用 Markdown 和 LaTeX 格式：

---

### 可变质量系统的动力学分析

#### 1. **基本概念**
在经典力学中，当系统的质量随时间变化（如火箭推进、雨滴凝结、下落的链条等），需修正牛顿第二定律：
$$
\sum \vec{F}_{\text{ext}} = \frac{d}{dt}(m\vec{v})
$$
其中 $m = m(t)$，直接展开得：
$$
\sum \vec{F}_{\text{ext}} = m\frac{d\vec{v}}{dt} + \vec{v}\frac{dm}{dt}
$$
此形式仅当质量增减时自身速度为零成立（如静止堆积的沙粒），但一般情况不适用。

---

#### 2. **密歇尔斯基方程**
考虑质量变化时附加物相对主体的速度 \(\vec{u}\)，**核心方程**为：
$$
\boxed{m\frac{d\vec{v}}{dt} = \sum \vec{F}_{\text{ext}} + \vec{u}\frac{dm}{dt}}
$$
- $\frac{dm}{dt} > 0$（质量增加，如雨滴）：\(\vec{u}\) 为附加物相对主体的速度  
- $\frac{dm}{dt} < 0$（质量减少，如火箭）：\(\vec{u}\) 为喷出物相对主体的速度  

---

#### 3. **火箭方程（齐奥尔科夫斯基公式）**
设火箭在重力场中运动：
- 喷气速度：\(\vec{u}\)（相对火箭，大小恒定）
- 推力：\(\vec{F}_p = -\vec{u}\frac{dm}{dt}\)（\(\frac{dm}{dt} < 0\)，故推力与 \(\vec{u}\) 反向）
- 运动方程：
  $$
  m\frac{dv}{dt} = -mg - u\frac{dm}{dt} \quad (\text{一维竖直方向})
  $$
  积分得**速度公式**：
  $$
  \Delta v = u \ln \left( \frac{m_0}{m} \right) - g\Delta t
  $$
  无重力时简化为：
  $$
  \Delta v = u \ln \left( \frac{m_0}{m} \right)
  $$

---

#### 4. **一般推导**
考虑系统在 $t$ 时刻：
- 质量：$m$，速度：$\vec{v}$
- $t + dt$ 时刻：
  - 主体质量：$m + dm$（注：$dm$ 可正可负）
  - 附加/脱离部分质量：$-dm$，相对主体速度：$\vec{u}$
- 动量守恒：
  $$
  m\vec{v} = (m + dm)(\vec{v} + d\vec{v}) + (-dm)(\vec{v} + \vec{u})
  $$
  展开并略去高阶小量 $dm  d\vec{v}$：
  $$
  m\vec{v} = m\vec{v} + m d\vec{v} + \vec{v} dm - dm \cdot \vec{v} - dm \cdot \vec{u}
  $$
  化简得：
  $$
  0 = m d\vec{v} - \vec{u} dm
  $$
  即：
  $$
  m d\vec{v} = \vec{u} dm
  $$
  结合外力 \(\sum \vec{F}_{\text{ext}}\) 后即得密歇尔斯基方程。

---

#### 5. **动量守恒的适用性**
- 若附加/脱离物原属系统，且无外力，则总动量守恒。
- **示例**：太空中的火箭（无重力）：
  $$
  m dv = -u  dm \quad \Rightarrow \quad \int_{v_0}^{v} dv = -u \int_{m_0}^{m} \frac{dm}{m} \quad \Rightarrow \quad v = v_0 + u \ln \left( \frac{m_0}{m} \right)
  $$

---

### 总结
| **关键量**       | **符号**   | **物理意义**                     |
|------------------|------------|----------------------------------|
| 质量变化率       | \(\frac{dm}{dt}\) | 系统质量变化速率                |
| 相对速度         | \(\vec{u}\)    | 附加/脱离物相对主体的速度        |
| 推力             | \(\vec{F}_p = -\vec{u} \frac{dm}{dt}\) | 反冲力方向与 \(\vec{u}\) 相反 |

**核心方程**始终为：
$$
m \frac{d\vec{v}}{dt} = \sum \vec{F}_{\text{ext}} + \vec{u} \frac{dm}{dt}
$$



---------------------


### 密歇尔斯基方程的详细推导

#### 推导思路
考虑一个质量随时间变化的系统（如火箭）。在 $t$ 时刻：
- 系统质量为 $m$，速度为 $\vec{v}$
- 在 $dt$ 时间内，有微小质量 $|dm|$ 以相对速度 $\vec{u}$ 离开或加入系统

通过分析系统在 $t$ 和 $t+dt$ 时刻的动量变化，结合动量定理推导核心方程。

---

#### 步骤详解

1. **定义系统状态**  
   - $t$ 时刻：  
     系统总质量 = $m$  
     系统速度 = $\vec{v}$  
     系统动量 = $\vec{p}(t) = m\vec{v}$

   - $t+dt$ 时刻：  
     - 主体部分：质量 $m + dm$（注意 $dm < 0$）  
       速度 $\vec{v} + d\vec{v}$  
       动量 = $(m + dm)(\vec{v} + d\vec{v})$  
     - 脱离部分：质量 $-dm$（因 $dm < 0$，故 $-dm > 0$)  
       相对主体速度 $\vec{u}$  
       绝对速度 = $(\vec{v} + d\vec{v}) + \vec{u}$  
       动量 = $(-dm) \left[ (\vec{v} + d\vec{v}) + \vec{u} \right]$

2. **总动量表达式**  
   $t+dt$ 时刻原系统的总动量（主体 + 脱离部分）：  
   $$
   \vec{p}(t+dt) = (m + dm)(\vec{v} + d\vec{v}) + (-dm)\left[ (\vec{v} + d\vec{v}) + \vec{u} \right]
   $$

3. **展开并化简**  
   $$
   \begin{align*}
   \vec{p}(t+dt) &= \underbrace{m\vec{v} + m d\vec{v} + dm \cdot \vec{v} + \cancel{dm \cdot d\vec{v}}_\text{主体部分} \\
   &\quad + \underbrace{(-dm)\vec{v} - dm \cdot d\vec{v} - (-dm)\vec{u}}_\text{脱离部分} \\
   &= m\vec{v} + m d\vec{v} + \cancel{dm \cdot \vec{v}} - \cancel{dm \cdot \vec{v}} - \cancel{dm \cdot d\vec{v}} + dm \cdot \vec{u} \\
   &= m\vec{v} + m d\vec{v} + \vec{u}  dm \quad (\text{二阶小量 } dm  d\vec{v} \to 0)
   \end{align*}
   $$

4. **动量变化量**  
   $$
   d\vec{p} = \vec{p}(t+dt) - \vec{p}(t) = (m\vec{v} + m d\vec{v} + \vec{u}  dm) - m\vec{v} = m d\vec{v} + \vec{u}  dm
   $$

5. **动量定理**  
   由动量定理：  
   $$
   \sum \vec{F}_{\text{ext}}  dt = d\vec{p}
   $$  
   代入得：  
   $$
   \sum \vec{F}_{\text{ext}}  dt = m d\vec{v} + \vec{u}  dm
   $$

6. **整理得核心方程**  
   两边除以 $dt$：  
   $$
   \sum \vec{F}_{\text{ext}} = m \frac{d\vec{v}}{dt} + \vec{u} \frac{dm}{dt}
   $$  
   移项后即 **密歇尔斯基方程**：  
   $$
   \boxed{m \frac{d\vec{v}}{dt} = \sum \vec{F}_{\text{ext}} - \vec{u} \frac{dm}{dt}}
   $$

---

#### 关键说明
1. **符号约定**：
   - $dm$ 是代数量：  
     - $dm < 0$ 表示质量减少（如火箭喷射）  
     - $dm > 0$ 表示质量增加（如雨滴凝结）
   - $\vec{u}$ 的方向：  
     始终定义为 **附加/脱离物质相对于主体** 的速度

2. **推力项**：  
   方程中 $-\vec{u} \frac{dm}{dt}$ 的物理意义：
   - 当 $dm/dt < 0$（质量减少）时：  
     $-\vec{u} \frac{dm}{dt} > 0$（推力与 $\vec{u}$ 方向相反）
   - 当 $dm/dt > 0$（质量增加）时：  
     $-\vec{u} \frac{dm}{dt}$ 表示附加物质对系统的冲击力

3. **与牛顿第二定律对比**：  
   若 $dm/dt = 0$（质量不变），方程退化为：  
   $$
   m \frac{d\vec{v}}{dt} = \sum \vec{F}_{\text{ext}}
   $$

---

### 物理图像
- **火箭推进**：  
  $dm/dt < 0$，$\vec{u}$ 向后 → 推力 $-\vec{u} \frac{dm}{dt}$ 向前
  ![](https://www.grc.nasa.gov/www/k-12/rocket/images/thrsteq.gif)

- **雨滴凝结**：  
  $dm/dt > 0$，$\vec{u}$ 向下（相对雨滴速度）→ 附加质量带来额外阻力 $-\vec{u} \frac{dm}{dt}$ 向上

此方程完美描述了质量变化系统中力、动量与质量流的关系。