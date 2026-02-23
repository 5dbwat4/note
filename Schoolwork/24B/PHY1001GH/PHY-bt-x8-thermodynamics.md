# 热学

热力学第一定律: $Q + W = \Delta E_{\text{int}}$

热容和比热容：$Q = mc\Delta T$，如果物质状态变了： $Q = Lm$ 

（热膨胀相关的公式？）

理想气体的内能：  $E_{\text{int}} = \frac{3}{2} nRT$

- **理想气体内能**：仅与温度相关，与体积、压强无关。
  - **单原子气体**：$E_{\text{int}} = \frac{3}{2}nRT$（3个平动自由度）；
  - **双原子气体**：$E_{\text{int}} = \frac{5}{2}nRT$（3平动+2转动自由度）；
  - **多原子气体**：$E_{\text{int}} = 3nRT$（3平动+3转动自由度）。


- **等压比热容 $c_p$**：在恒定压力下，单位质量的物质温度升高1摄氏度所吸收的热量。
- **等体比热容 $c_V$**：在恒定体积下，单位质量的物质温度升高1摄氏度所吸收的热量。
- 对于单原子理想气体， $C_V = \frac{3}{2} R$ ， $C_P = \frac{5}{2} R$ 。
- 对于双原子理想气体， $C_V = \frac{5}{2} R$ ， $C_P = \frac{7}{2} R$ 。
- 对于多原子理想气体， $C_V = \frac{f}{2} R$ ， $C_P = \frac{f + 2}{2} R$ 
（$C_P = C_V + 1$）


熵的计算：
- 等温可逆熵变：$\Delta S = \frac{Q}{T}$ (可逆、等温过程)
- 等容过程: $\Delta S = nC_V \ln\left(\frac{T_2}{T_1}\right)$
- 等压过程: $\Delta S = nC_p \ln\left(\frac{T_2}{T_1}\right)$

**卡诺热机**
- $K = \frac{|Q_L|}{|W|} = \frac{T_L}{T_H - T_L}$，$|Q_L|$：从低温热源吸收的热量；$|W|$：外界输入的功

TABLE 23-5 Applications of the First Law


| Process                      | Restriction                 | First Law                       | Other Results                                                 |
| ---------------------------- | --------------------------- | ------------------------------- | ------------------------------------------------------------- |
| All(一般情况)                | None                        | $\Delta E_{\text{int}} = Q + W$ | $\Delta E_{\text{int}} = n C_V \Delta T$, $W = -\int p \, dV$ |
| Adiabatic(绝热过程)          | $Q = 0$                     | $\Delta E_{\text{int}} = W$     | $W = \frac{p_f V_f - p_i V_i}{\gamma - 1}$                    |
| Constant volume(定容过程)    | $W = 0$                     | $\Delta E_{\text{int}} = Q$     | $Q = n C_V \Delta T$                                          |
| Constant pressure(定压过程)  | $\Delta p = 0$              | $\Delta E_{\text{int}} = Q + W$ | $W = -p \Delta V$, $Q = n C_p \Delta T$                       |
| Isothermal(等温过程)         | $\Delta E_{\text{int}} = 0$ | $Q = -W$                        | $W = -nRT \ln\left(\frac{V_f}{V_i}\right)$                    |
| Cycle(循环过程)              | $\Delta E_{\text{int}} = 0$ | $Q = -W$                        |                                                               |
| Free expansion(自由膨胀过程) | $Q = W = 0$                 | $\Delta E_{\text{int}} = 0$     | $\Delta T = 0$                                                |

*Items underlined apply only to ideal gases; all other items apply in general.*
