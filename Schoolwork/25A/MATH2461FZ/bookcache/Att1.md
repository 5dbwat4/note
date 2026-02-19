# 概率论与数理统计常用概率分布表

| 分布 | 参数 | 概率分布律或密度函数 | 数学期望 | 方差 |
| --- | --- | --- | --- | --- |
| (0-1)分布 | 0 < p < 1 | $P\{X = k\} = p^k(1 - p)^{1 - k}, k = 0,1$ | p | $p(1 - p)$ |
| 二项分布 | n ≥ 1，0 < p < 1 | $P\{X = k\} = C_n^k p^k(1 - p)^{n - k}, k = 0,1,\dots,n$ | np | $np(1 - p)$ |
| 几何分布 | 0 < p < 1 | $P\{X = k\} = (1 - p)^{k - 1}p, k = 1,2,\dots$ | $\frac{1}{p}$ | $\frac{1 - p}{p^2}$ |
| 负二项分布 | r ≥ 1，0 < p < 1 | $P\{X = k\} = C_{k - 1}^{r - 1}p^r(1 - p)^{k - r}, k = r, r + 1,\dots$ | $\frac{r}{p}$ | $\frac{r(1 - p)}{p^2}$ |
| 超几何分布 | N，M，n（M ≤ N，n ≤ N） | $P\{X = k\} = \frac{C_M^k C_{N - M}^{n - k}}{C_N^n}$，k 为整数，且 $\max\{0, n - N + M\} < k < \min\{n, M\}$ | $\frac{nM}{N}$ | $\frac{nM}{N}(1 - \frac{M}{N})\frac{N - n}{N - 1}$ |
| 泊松分布 | λ > 0 | $P\{X = k\} = \frac{\lambda^k e^{-\lambda}}{k!}, k = 0,1,2,\dots$ | λ | λ |
| 均匀分布 | a < b | $f(x) = \begin{cases} \frac{1}{b - a}, & a < x < b \\ 0, & \text{其他} \end{cases}$ | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ |
| 正态分布 | μ，σ > 0 | $f(x) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(x - \mu)^2}{2\sigma^2}}$ | μ | $\sigma^2$ |
| 指数分布（负指数分布） | λ > 0 | $f(x) = \begin{cases} \lambda e^{-\lambda x}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | $\frac{1}{\lambda}$ | $\frac{1}{\lambda^2}$ |
| Γ分布 | α > 0，β > 0 | $f(x) = \begin{cases} \frac{\beta^\alpha}{\Gamma(\alpha)}x^{\alpha - 1}e^{-\beta x}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | $\frac{\alpha}{\beta}$ | $\frac{\alpha}{\beta^2}$ |
| χ²分布 | n ≥ 1 | $f(x) = \begin{cases} \frac{1}{2^{\frac{n}{2}}\Gamma(\frac{n}{2})}x^{\frac{n}{2} - 1}e^{-\frac{x}{2}}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | n | 2n |
| 威布尔分布 | n > 0，β > 0 | $f(x) = \begin{cases} \frac{n}{\beta}x^{n - 1}e^{-\left(\frac{x}{\beta}\right)^n}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | $\beta\Gamma\left(\frac{1}{n} + 1\right)$ | $\beta^2\left[\Gamma\left(\frac{2}{n} + 1\right) - \left(\Gamma\left(\frac{1}{n} + 1\right)\right)^2\right]$ |
| 瑞利分布 | σ > 0 | $f(x) = \begin{cases} \frac{x}{\sigma^2}e^{-\frac{x^2}{2\sigma^2}}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | $\sigma\sqrt{\frac{\pi}{2}}$ | $\frac{(4 - \pi)\sigma^2}{2}$ |
| B分布 | α > 0，β > 0 | $f(x) = \begin{cases} \frac{\Gamma(\alpha + \beta)}{\Gamma(\alpha)\Gamma(\beta)}x^{\alpha - 1}(1 - x)^{\beta - 1}, & 0 < x < 1 \\ 0, & \text{其他} \end{cases}$ | $\frac{\alpha}{\alpha + \beta}$ | $\frac{\alpha\beta}{(\alpha + \beta)^2(\alpha + \beta + 1)}$ |
| 对数正态分布 | μ，σ > 0 | $f(x) = \begin{cases} \frac{1}{x\sqrt{2\pi}\sigma}e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | $e^{\mu + \frac{\sigma^2}{2}}$ | $e^{2\mu + \sigma^2}(e^{\sigma^2} - 1)$ |
| 柯西分布 | α，λ > 0 | $f(x) = \frac{\lambda}{\pi(\lambda^2 + (x - \alpha)^2)}$ | 不存在 | 不存在 |
| t分布 | n ≥ 1 | $f(x) = \frac{\Gamma\left(\frac{n + 1}{2}\right)}{\sqrt{n\pi}\Gamma\left(\frac{n}{2}\right)}\left(1 + \frac{x^2}{n}\right)^{-\frac{n + 1}{2}}$ | 0（n > 1） | $\frac{n}{n - 2}$（n > 2） |
| F分布 | n₁ ≥ 1，n₂ ≥ 1 | $f(x) = \begin{cases} \frac{\Gamma\left(\frac{n_1 + n_2}{2}\right)}{\Gamma\left(\frac{n_1}{2}\right)\Gamma\left(\frac{n_2}{2}\right)}\left(\frac{n_1}{n_2}\right)^{\frac{n_1}{2}}x^{\frac{n_1}{2} - 1}\left(1 + \frac{n_1 x}{n_2}\right)^{-\frac{n_1 + n_2}{2}}, & x > 0 \\ 0, & \text{其他} \end{cases}$ | $\frac{n_2}{n_2 - 2}$（n₂ > 2） | $\frac{2n_2^2(n_1 + n_2 - 2)}{n_1(n_2 - 2)^2(n_2 - 4)}$（n₂ > 4） |