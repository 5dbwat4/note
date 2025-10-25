---
title: MATHEMATICAL FORMULAS
---


# Geometry
- Circle of radius $r$: circumference $= 2\pi r$; area $= \pi r^2$.
- Sphere of radius $r$: area $= 4\pi r^2$; volume $= \frac{4}{3}\pi r^3$.
- Right circular cylinder of radius $r$ and height $h$:
  - area $= 2\pi r^2 + 2\pi r h$; volume $= \pi r^2 h$.
- Triangle of base $a$ and altitude $h$: area $= \frac{1}{2}ah$.

# Quadratic Formula
If $ax^2 + bx + c = 0$, then $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

# Trigonometric Functions of Angle $\theta$
$$
\begin{align*}
\sin \theta &= \frac{y}{r} & \cos \theta &= \frac{x}{r} \\
\tan \theta &= \frac{y}{x} & \cot \theta &= \frac{x}{y} \\
\sec \theta &= \frac{r}{x} & \csc \theta &= \frac{r}{y}
\end{align*}
$$

# Pythagorean Theorem
$$ a^2 + b^2 = c^2 $$

# Triangles
- Angles $A, B, C$
- Opposite sides $a, b, c$
- $A + B + C = 180^\circ$
- \(\frac{\sin A}{a} = \frac{\sin B}{b} = \frac{\sin C}{c}\)
- $c^2 = a^2 + b^2 - 2ab \cos C$

# Mathematical Signs and Symbols
- $=$ equals
- $\approx$ equals approximately
- $\neq$ is not equal to
- $\equiv$ is identical to, is defined as
- $>$ is greater than ($\gg$ is much greater than)
- $<$ is less than ($\ll$ is much less than)
- $\geq$ is greater than or equal to (or, is no less than)
- $\leq$ is less than or equal to (or, is no more than)
- $\pm$ plus or minus ($\sqrt{4} = \pm 2$)
- $\propto$ is proportional to
- $\Sigma$ the sum of
- $\bar{x}$ the average value of $x$ (also $x_{\text{av}}$)

# Trigonometric Identities
$$
\begin{align*}
\sin(90^\circ - \theta) &= \cos \theta \\
\cos(90^\circ - \theta) &= \sin \theta \\
\sin \theta / \cos \theta &= \tan \theta \\
\sin^2 \theta + \cos^2 \theta &= 1 \quad \sec^2 \theta - \tan^2 \theta = 1 \quad \csc^2 \theta - \cot^2 \theta = 1 \\
\sin 2\theta &= 2 \sin \theta \cos \theta \\
\cos 2\theta &= \cos^2 \theta - \sin^2 \theta = 2 \cos^2 \theta - 1 = 1 - 2 \sin^2 \theta \\
\sin(\alpha \pm \beta) &= \sin \alpha \cos \beta \pm \cos \alpha \sin \beta \\
\cos(\alpha \pm \beta) &= \cos \alpha \cos \beta \mp \sin \alpha \sin \beta \\
\tan(\alpha \pm \beta) &= \frac{\tan \alpha \pm \tan \beta}{1 \mp \tan \alpha \tan \beta} \\
\sin \alpha \pm \sin \beta &= 2 \sin \frac{1}{2}(\alpha \pm \beta) \cos \frac{1}{2}(\alpha \mp \beta)
\end{align*}
$$

# Binomial Expansion
$$
\begin{align*}
(1 \pm x)^n &= 1 \pm \frac{nx}{1!} + \frac{n(n - 1)x^2}{2!} + \cdots \, (x^2 < 1) \\
(1 \pm x)^{-n} &= 1 \mp \frac{nx}{1!} + \frac{n(n + 1)x^2}{2!} \mp \cdots \, (x^2 < 1)
\end{align*}
$$

# Exponential Expansion
$$
e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots
$$

# Logarithmic Expansion
$$
\ln (1 + x) = x - \frac{1}{2}x^2 + \frac{1}{3}x^3 - \cdots \, (|x| < 1)
$$

# Trigonometric Expansions ($\theta$ in radians)
$$
\begin{align*}
\sin \theta &= \theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots \\
\cos \theta &= 1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots \\
\tan \theta &= \theta + \frac{\theta^3}{3} + \frac{2\theta^5}{15} + \cdots
\end{align*}
$$

# Derivatives and Integrals

In what follows, the letters $u$ and $v$ stand for any functions of $x$, and $a$ and $m$ are constants. To each of the indefinite integrals should be added an arbitrary constant of integration. The *Handbook of Chemistry and Physics* (CRC Press Inc.) gives a more extensive tabulation.

## Derivatives
1. $\frac{d x}{d x} = 1$
2. $\frac{d}{d x} (a u) = a \frac{d u}{d x}$
3. $\frac{d}{d x} (u + v) = \frac{d u}{d x} + \frac{d v}{d x}$
4. $\frac{d}{d x} x^m = m x^{m - 1}$
5. $\frac{d}{d x} \ln x = \frac{1}{x}$
6. $\frac{d}{d x} (u v) = u \frac{d v}{d x} + v \frac{d u}{d x}$
7. $\frac{d}{d x} e^x = e^x$
8. $\frac{d}{d x} \sin x = \cos x$
9. $\frac{d}{d x} \cos x = -\sin x$
10. $\frac{d}{d x} \tan x = \sec^2 x$
11. $\frac{d}{d x} \cot x = -\csc^2 x$
12. $\frac{d}{d x} \sec x = \tan x \sec x$
13. $\frac{d}{d x} \csc x = -\cot x \csc x$
14. $\frac{d}{d x} e^u = e^u \frac{d u}{d x}$
15. $\frac{d}{d x} \sin u = \cos u \frac{d u}{d x}$
16. $\frac{d}{d x} \cos u = -\sin u \frac{d u}{d x}$

## Integrals
1. $\int dx = x$
2. $\int a u \, dx = a \int u \, dx$
3. $\int (u + v) \, dx = \int u \, dx + \int v \, dx$
4. $\int x^m \, dx = \frac{x^{m + 1}}{m + 1} \, (m \neq -1)$
5. $\int \frac{dx}{x} = \ln |x|$
6. $\int u \frac{d v}{d x} dx = u v - \int v \frac{d u}{d x} dx$
7. $\int e^x \, dx = e^x$
8. $\int \sin x \, dx = -\cos x$
9. $\int \cos x \, dx = \sin x$
10. $\int \tan x \, dx = -\ln \cos x$
11. $\int \sin^2 x \, dx = \frac{1}{2}x - \frac{1}{4}\sin 2x$
12. $\int \cos^2 x \, dx = \frac{1}{2}x + \frac{1}{4}\sin 2x$
13. $\int e^{-ax} \, dx = -\frac{1}{a} e^{-ax}$
14. $\int x e^{-ax} \, dx = -\frac{1}{a^2} (ax + 1) e^{-ax}$
15. $\int x^2 e^{-ax} \, dx = -\frac{1}{a^3} (a^2 x^2 + 2ax + 2) e^{-ax}$
16. $\int x^n e^{-ax} \, dx = \frac{n!}{a^{n + 1}}$
17. $\int_0^\infty x^{2n} e^{-ax^2} dx = \frac{1 \cdot 3 \cdot 5 \cdots (2n - 1)}{2^{n + 1} a^n} \sqrt{\frac{\pi}{a}}$
18. $\int \frac{dx}{\sqrt{(x^2 \pm a^2)^3}} = \frac{\pm x}{a^2 \sqrt{x^2 \pm a^2}}$