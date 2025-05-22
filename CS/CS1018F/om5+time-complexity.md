# Time Complexity

- The major task of algorithm analysis is to analyze the time complexity and the space complexity. (T)

## Algorithm

【Definition】An algorithm is a finite set of instructions that, if followed, accomplishes a particular task.   In addition,  all algorithms must satisfy the following criteria:
(1)   Input    There are zero or more quantities that are externally supplied.
(2)   Output    At least one quantity is produced.
(3)   Definiteness    Each instruction is clear and unambiguous.
(4)   Finiteness    If we trace out the instructions of an algorithm, then for all cases, the algorithm terminates after finite number of steps.
(5)   Effectiveness    Every instruction must be basic enough to be carried out, in principle, by a person using only pencil and paper.  It is not enough that each operation be definite as in(3); it also must be feasible.


## 几个时间复杂度符号

### 1. **大O符号（Big O Notation）**
• **定义**：表示**渐近上界**，即算法运行时间的**最坏情况增长率**。  
  数学形式：  
  $f(n) = O(g(n))$ ，当且仅当存在正常数 $C$ 和 $n_0$，使得对所有 $n \geq n_0$，有 $f(n) \leq C \cdot g(n)$。

• **含义**：算法的增长率**不超过** $g(n)$ 的增长率。  
• **例子**：  
  • 线性时间复杂度：$3n + 5 = O(n)$  
  • 平方时间复杂度：$2n^2 + 3n + 1 = O(n^2)$


### 2. **小o符号（Little o Notation）**
• **定义**：表示**严格渐近上界**，即增长率严格低于某个函数。  
  数学形式：  
  $f(n) = o(g(n))$ ，当且仅当对于**任意**正数 $C > 0$，存在 $n_0$，使得对所有 $n \geq n_0$，有 $f(n) < C \cdot g(n)$。

• **含义**：算法的增长率**严格慢于** $g(n)$ 的增长率。  
• **例子**：  
  • $n = o(n \log n)$（线性增长比 $n \log n$ 慢）  
  • $2n = o(n^2)$（但 $2n \neq o(n)$，因为它与 $n$ 同阶）


### 3. **大Ω符号（Big Omega Notation）**
• **定义**：表示**渐近下界**，即算法运行时间的**最佳情况增长率**。  
  数学形式：  
  $f(n) = \Omega(g(n))$ ，当且仅当存在正常数 $C$ 和 $n_0$，使得对所有 $n \geq n_0$，有 $f(n) \geq C \cdot g(n)$。

• **含义**：算法的增长率**至少为** $g(n)$ 的增长率。  
• **例子**：  
  • $n^2 = \Omega(n)$  
  • 快速排序的平均情况：$\Omega(n \log n)$


### 4. **大θ符号（Big Theta Notation）**
• **定义**：表示**紧确渐近界**，即算法运行时间同时具有上界和下界。  
  数学形式：  
  $f(n) = \Theta(g(n))$ ，当且仅当 $f(n) = O(g(n))$ 且 $f(n) = \Omega(g(n))$。

• **含义**：算法的增长率**与** $g(n)$ **同阶**。  
• **例子**：  
  • $3n^2 + 4n + 5 = \Theta(n^2)$

### 5. **符号对比**
| 符号     | 关系              | 含义                     |
|----------|-------------------|--------------------------|
| $O$  | $f(n) \leq g(n)$ | 增长率不超过 $g(n)$  |
| $o$  | $f(n) < g(n)$    | 增长率严格慢于 $g(n)$|
| $\Omega$ | $f(n) \geq g(n)$ | 增长率不低于 $g(n)$  |
| $\Theta$ | $f(n) = g(n)$    | 增长率等于 $g(n)$    |

### 示例总结
• **大O**：`5n² + 3n + 1 = O(n²)`  
• **小o**：`5n² = o(n³)`  
• **大Ω**：`n log n = Ω(n)`  
• **大θ**：`2n² + n = Θ(n²)`
