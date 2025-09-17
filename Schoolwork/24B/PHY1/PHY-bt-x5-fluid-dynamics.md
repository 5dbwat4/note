伯努利方程:  $p + \frac{1}{2}\rho v^2 + \rho gy = \text{constant}$，适用于沿同一流线的任意两点。

连续性方程:  $A_1v_1 = A_2v_2$，表示流体在管道中的体积流量保持不变

Torricelli's law（托里拆利定律）: 当流体从一个开口容器的底部小孔流出时，流体的流出速度 $v$与容器内流体的高度$h$(**从暴露的液面到出口处**)之间的关系为：$ v = \sqrt{2gh} $


判定流场是irrotational（没太看懂其实）：

要证明一个流场是无旋的（irrotational），我们需要证明流场的旋度（curl）为零。在数学上，这可以通过计算流场的旋度并验证其结果为零来实现。对于一个向量场 \(\mathbf{F} = (F_x, F_y, F_z)\)，其旋度定义为：

\[
\nabla \times \mathbf{F} = \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z}, \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x}, \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right)
\]

如果 \(\nabla \times \mathbf{F} = (0, 0, 0)\)，则流场 \(\mathbf{F}\) 是无旋的。

另外，根据斯托克斯定理，一个向量场在闭合路径上的线积分等于该向量场旋度在由该路径所围成的曲面上的面积分。因此，如果流场是无旋的，那么在任何闭合路径上的线积分将为零：

\[
\oint_C \mathbf{F} \cdot d\mathbf{r} = 0
\]

其中 \(C\) 是任意闭合路径，\(d\mathbf{r}\) 是路径上的微分向量。

因此，要证明一个流场是无旋的，可以计算流场的旋度并验证其为零，或者计算流场在任意闭合路径上的线积分并验证其为零。

\[
\boxed{\nabla \times \mathbf{F} = (0, 0, 0) \quad \text{或} \quad \oint_C \mathbf{F} \cdot d\mathbf{r} = 0}
\]