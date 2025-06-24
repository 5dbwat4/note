# Quiz 4:

如果你先抓住一条均匀软链的上端，而下端刚好接触地面。在你释放之后，链子会对地面施加多大的力？假设链子的长度为 $L$ ，质量为 $M$。


## Answer:
在时刻 $t$，链子长度为 $l$ 的部分已经落在地面上。在接下来的时间间隔 $dt$ 内，另一段质量为 $dm$ 的小部分将撞击地面。

那么，这部分小质量的动量变化为：
$$
dp = dm \cdot v = \left(\frac{M}{L}\right) dl \cdot v = \left(\frac{M}{L}\right) v dt \cdot v
$$
其中 $v = \sqrt{2gl}$。

根据 $F_p dt = dp$，我们有：
$$
F_p = \frac{2gMl}{L}
$$

因此，在时刻 $t$ 的总力为：
$$
F_t = F_i + F_p = \frac{Mgl}{L} + \frac{2gMl}{L} = \frac{3gMl}{L} = 3mg
$$
其中 $m = \frac{Ml}{L}$。


# Quiz 11:
Show that the total energy between the node and the antinode remains constant and there is no energy flowing through nodes and antinodes for a standing wave $y = y_m \cos kx \sin \omega t$.

## Solution:

Kinetic energy: 
$$
dK = \frac{1}{2} (\mu dx) \left(\frac{dy}{dt}\right)^2
$$
$$
\frac{dy}{dt} = y_m \omega \cos kx \cos \omega t
$$
$$
= \frac{1}{2} (\mu dx) y_m^2 \omega^2 \cos^2 kx \cos^2 \omega t
$$

Potential energy: 
$$
dU = \frac{F}{2} \left(\frac{dy}{dx}\right)^2 dx \\
\frac{dy}{dx} = -ky_m \sin kx \sin \omega t \\
= \frac{F dx}{2} (y_m k \sin kx \sin \omega t)^2 \\
= \frac{1}{2} dx \mu y_m^2 \omega^2 \sin^2 x \sin^2 \omega t \\
F = u^2 \mu = \frac{\omega^2}{k^2} \mu \\

dE = dK + dU = \frac{1}{2} dx \mu y_m^2 \omega^2 [\sin^2 kx \sin^2 \omega t + \cos^2 kx \cos^2 \omega t] \\
E = \frac{1}{2} \mu y_m^2 \omega^2 \int_0^{\lambda/4} [\sin^2 kx \sin^2 \omega t + \cos^2 kx \cos^2 \omega t] dx \\
= \frac{1}{2} \mu y_m^2 \omega^2 \left[ \frac{1}{2k} \frac{\pi}{2} \sin^2 \omega t + \frac{1}{2k} \frac{\pi}{2} \cos^2 \omega t \right] \\
E = \frac{\mu y_m^2 \omega^2 \lambda}{16} 
$$


Total energy remains constant between N and AN.

Instantaneous power transferred from left part to right part is $P_i$

$$
P_i = \vec{F} \cdot \vec{v} = -F \sin \theta \frac{dy}{dt} = -F \left( \frac{dy}{dx} \right) \left( \frac{dy}{dt} \right) \\
P_i = -F (-y_m k \sin kx \sin \omega t) (y_m \omega \cos kx \cos \omega t) \\
= F y_m^2 k \omega \sin \omega t \cos \omega t \sin kx \cos kx \\
P_i = 0 \quad \text{At a node or an antinode.} 
$$

There is no power transmitted through a node or an antinode.




# Quiz 15:
A car with a gasoline-powered internal combustion engine travels with a speed of $v = 30 \, \text{m/s}$ on a level road and uses gas at a rate of $\chi = 10 \, \text{L/100km}$. The energy content of gasoline is $E_g = 35 \, \text{MJ/L}$. If the engine has an efficiency of $e = 20\%$, how much power is delivered to keep the car moving at a constant speed?

## Solution:
The burn rate of gasoline by the car
$$
\gamma_g = \chi v
$$

The power per unit time
$$
p = \gamma_g E_g
$$

The efficiency by the definition
$$
e = W / Q_H = (W / t) / (Q_H / t) = P_{\text{delivered}} / P
$$

So
$$
P_{\text{delivered}} = eP = e \chi v E_g \\
= 0.2 \times \frac{10}{100 \cdot 10^3} \times 30 \times 35 \cdot 10^6 = 2.1 \times 10^4 \, \text{W}
$$