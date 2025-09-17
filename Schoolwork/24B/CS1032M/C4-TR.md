# Key Terms and Results

## TERMS

- $a \mid b$ ($a$ divides $b$): There exists an integer $c$ such that $b = ac$.
- $a$ and $b$ are congruent modulo $m$: $m$ divides $a - b$.
- **Modular arithmetic**: Arithmetic done modulo an integer $m \geq 2$.
- **Prime**: An integer greater than 1 with exactly two positive integer divisors.
- **Composite**: An integer greater than 1 that is not prime.
- **Mersenne prime**: A prime of the form $2^p - 1$, where $p$ is prime.
- $\operatorname{gcd}(a, b)$ (greatest common divisor of $a$ and $b$): The largest integer that divides both $a$ and $b$.
- **Relatively prime integers**: Integers $a$ and $b$ such that $\operatorname{gcd}(a, b) = 1$.
- **Pairwise relatively prime integers**: A set of integers with the property that every pair of these integers is relatively prime.
- $\operatorname{lcm}(a, b)$ (least common multiple of $a$ and $b$): The smallest positive integer that is divisible by both $a$ and $b$.
- $a \mod b$: The remainder when the integer $a$ is divided by the positive integer $b$.
- $a \equiv b (\operatorname{mod} m)$ ($a$ is congruent to $b$ modulo $m$): $a - b$ is divisible by $m$.
- $n = (a_k a_{k-1} \ldots a_1 a_0)_b$: The base $b$ representation of $n$.
  - **Binary representation**: The base 2 representation of an integer.
  - **Octal representation**: The base 8 representation of an integer.
  - **Hexadecimal representation**: The base 16 representation of an integer.
- Linear combination of $a$ and $b$ with integer coefficients: An expression of the form $sa + tb$, where $s$ and $t$ are integers.
- **Bézout coefficients of $a$ and $b$**: Integers $s$ and $t$ such that the Bézout identity $sa + tb = \operatorname{gcd}(a, b)$ holds.
- Inverse of $a$ modulo $m$: An integer $\bar{a}$ such that $\bar{a}a \equiv 1 (\operatorname{mod} m)$.
- **Linear congruence**: A congruence of the form $ax \equiv b (\operatorname{mod} m)$, where $x$ is an integer variable.
- Pseudoprime to the base $b$: A composite integer $n$ such that $b^{n-1} \equiv 1 (\operatorname{mod} n)$.
- **Carmichael number**: A composite integer $n$ such that $n$ is a pseudoprime to the base $b$ for all positive integers $b$ with $\operatorname{gcd}(b, n) = 1$.
- **Primitive root of a prime $p$**: An integer $r$ in $Z_p$ such that every integer not divisible by $p$ is congruent modulo $p$ to a power of $r$.
- Discrete logarithm of $a$ to the base $r$ modulo $p$: The integer $e$ with $0 \leq e \leq p-1$ such that $r^e \equiv a \, (\operatorname{mod} p)$.
- **Encryption**: The process of making a message secret.
- **Decryption**: The process of returning a secret message to its original form.
- **Encryption key**: A value that determines which of a family of encryption functions is to be used.
- **Shift cipher**: A cipher that encrypts the plaintext letter $p$ as $(p + k) \mod m$ for an integer $k$.
- **Affine cipher**: A cipher that encrypts the plaintext letter $p$ as $(ap + b) \mod m$ for integers $a$ and $b$ with $\operatorname{gcd}(a, 26) = 1$.
- **Character cipher**: A cipher that encrypts characters one by one.
- **Block cipher**: A cipher that encrypts blocks of characters of a fixed size.
- **Cryptanalysis**: The process of recovering the plaintext from ciphertext without knowledge of the encryption method, or with knowledge of the encryption method, but not the key.
- **Cryptosystem**: A five-tuple $(\mathcal{P}, \mathcal{C}, \mathcal{K}, \mathcal{E}, \mathcal{D})$ where $\mathcal{P}$ is the set of plaintext messages, $\mathcal{C}$ is the set of ciphertext messages, $\mathcal{K}$ is the set of keys, $\mathcal{E}$ is the set of encryption functions, and $\mathcal{D}$ is the set of decryption functions.
- **Private key encryption**: Encryption where both encryption keys and decryption keys must be kept secret.
- **Public key encryption**: Encryption where encryption keys are public knowledge, but decryption keys are kept secret.
- **RSA cryptosystem**: The cryptosystem where $\mathcal{P}$ and $\mathcal{C}$ are both $Z_{26}$, $\mathcal{K}$ is the set of pairs $k = (n, e)$ where $n = pq$ where $p$ and $q$ are large primes and $e$ is a positive integer, $E_k(p) = p^e \mod n$, and $D_k(c) = c^d \mod n$ where $d$ is the inverse of $e$ modulo $(p-1)(q-1)$.
- **Key exchange protocol**: A protocol used for two parties to generate a shared key.
- **Digital signature**: A method that a recipient can use to determine that the purported sender of a message actually sent the message.
- **Fully homomorphic cryptosystem**: A cryptosystem that allows arbitrary computations to be run on encrypted data so that the output is the encryption of the unencrypted output of the unencrypted input.

## RESULTS

- **Division algorithm**: Let $a$ and $d$ be integers with $d$ positive. Then there are unique integers $q$ and $r$ with $0 \leq r < d$ such that $a = dq + r$.
- Let $b$ be an integer greater than 1. Then if $n$ is a positive integer, it can be expressed uniquely in the form $n = a_k b^k + a_{k-1} b^{k-1} + \cdots + a_1 b + a_0$.
- The algorithm for finding the base $b$ expansion of an integer (see Algorithm 1 in Section 4.2).
- The conventional algorithms for addition and multiplication of integers (given in Section 4.2).
- The fast modular exponentiation algorithm (see Algorithm 5 in Section 4.2).
- **Euclidean algorithm**: For finding greatest common divisors by successively using the division algorithm (see Algorithm 1 in Section 4.3).
- **Bézout's theorem**: If $a$ and $b$ are positive integers, then $\operatorname{gcd}(a, b)$ is a linear combination of $a$ and $b$.
- **Sieve of Eratosthenes**: A procedure for finding all primes not exceeding a specified number $n$, described in Section 4.3.
- **Fundamental theorem of arithmetic**: Every positive integer can be written uniquely as the product of primes, where the prime factors are written in order of increasing size.
- If $a$ and $b$ are positive integers, then $ab = \operatorname{gcd}(a, b) \cdot \operatorname{lcm}(a, b)$.
- If $m$ is a positive integer and $\operatorname{gcd}(a, m) = 1$, then $a$ has a unique inverse modulo $m$.


# CN

- $a \mid b$ ($a$ divides $b$): There exists an integer $c$ such that $b = ac$.  
- $a \mid b$（$a$ 整除 $b$）：存在一个整数 $c$，使得 $b = ac$。

- $a$ and $b$ are congruent modulo $m$: $m$ divides $a - b$.  
- $a$ 和 $b$ 模 $m$ 同余：$m$ 整除 $a - b$。

- **Modular arithmetic**: Arithmetic done modulo an integer $m \geq 2$.  
- **模运算**：在模一个整数 $m \geq 2$ 的情况下进行的运算。

- **Prime**: An integer greater than 1 with exactly two positive integer divisors.  
- **素数**：大于 1 的整数，且仅有两个正整数因数。

- **Composite**: An integer greater than 1 that is not prime.  
- **合数**：大于 1 的整数，且不是素数。

- **Mersenne prime**: A prime of the form $2^p - 1$, where $p$ is prime.  
- **梅森素数**：形如 $2^p - 1$ 的素数，其中 $p$ 是素数。

- $\operatorname{gcd}(a, b)$ (greatest common divisor of $a$ and $b$): The largest integer that divides both $a$ and $b$.  
- $\operatorname{gcd}(a, b)$（$a$ 和 $b$ 的最大公因数）：能够同时整除 $a$ 和 $b$ 的最大整数。

- **Relatively prime integers**: Integers $a$ and $b$ such that $\operatorname{gcd}(a, b) = 1$.  
- **互质整数**：整数 $a$ 和 $b$ 满足 $\operatorname{gcd}(a, b) = 1$。

- **Pairwise relatively prime integers**: A set of integers with the property that every pair of these integers is relatively prime.  
- **两两互质整数**：一组整数，其中任意两个整数都是互质的。

- $\operatorname{lcm}(a, b)$ (least common multiple of $a$ and $b$): The smallest positive integer that is divisible by both $a$ and $b$.  
- $\operatorname{lcm}(a, b)$（$a$ 和 $b$ 的最小公倍数）：能够同时被 $a$ 和 $b$ 整除的最小正整数。

- $a \mod b$: The remainder when the integer $a$ is divided by the positive integer $b$.  
- $a \mod b$：整数 $a$ 除以正整数 $b$ 的余数。

- $a \equiv b (\operatorname{mod} m)$ ($a$ is congruent to $b$ modulo $m$): $a - b$ is divisible by $m$.  
- $a \equiv b (\operatorname{mod} m)$（$a$ 模 $m$ 同余于 $b$）：$a - b$ 能被 $m$ 整除。

- $n = (a_k a_{k-1} \ldots a_1 a_0)_b$: The base $b$ representation of $n$.  
- $n = (a_k a_{k-1} \ldots a_1 a_0)_b$：$n$ 的 $b$ 进制表示。

  - **Binary representation**: The base 2 representation of an integer.  
  - **二进制表示**：整数的二进制表示。

  - **Octal representation**: The base 8 representation of an integer.  
  - **八进制表示**：整数的八进制表示。

  - **Hexadecimal representation**: The base 16 representation of an integer.  
  - **十六进制表示**：整数的十六进制表示。

- Linear combination of $a$ and $b$ with integer coefficients: An expression of the form $sa + tb$, where $s$ and $t$ are integers.  
- $a$ 和 $b$ 的整系数线性组合：形式为 $sa + tb$ 的表达式，其中 $s$ 和 $t$ 是整数。

- **Bézout coefficients of $a$ and $b$**: Integers $s$ and $t$ such that the Bézout identity $sa + tb = \operatorname{gcd}(a, b)$ holds.  
- **贝祖系数**：整数 $s$ 和 $t$，使得贝祖等式 $sa + tb = \operatorname{gcd}(a, b)$ 成立。

- Inverse of $a$ modulo $m$: An integer $\bar{a}$ such that $\bar{a}a \equiv 1 (\operatorname{mod} m)$.  
- $a$ 模 $m$ 的逆元：一个整数 $\bar{a}$，使得 $\bar{a}a \equiv 1 (\operatorname{mod} m)$。

- **Linear congruence**: A congruence of the form $ax \equiv b (\operatorname{mod} m)$, where $x$ is an integer variable.  
- **线性同余方程**：形如 $ax \equiv b (\operatorname{mod} m)$ 的同余方程，其中 $x$ 是整数变量。

- Pseudoprime to the base $b$: A composite integer $n$ such that $b^{n-1} \equiv 1 (\operatorname{mod} n)$.  
- 以 $b$ 为底的伪素数：一个合数 $n$，满足 $b^{n-1} \equiv 1 (\operatorname{mod} n)$。

- **Carmichael number**: A composite integer $n$ such that $n$ is a pseudoprime to the base $b$ for all positive integers $b$ with $\operatorname{gcd}(b, n) = 1$.  
- **卡迈克尔数**：一个合数 $n$，使得对于所有与 $n$ 互质的正整数 $b$，$n$ 都是以 $b$ 为底的伪素数。

- **Primitive root of a prime $p$**: An integer $r$ in $Z_p$ such that every integer not divisible by $p$ is congruent modulo $p$ to a power of $r$.  
- **素数 $p$ 的原根**：在 $Z_p$ 中的整数 $r$，使得每一个不能被 $p$ 整除的整数都模 $p$ 同余于 $r$ 的某个幂。

- Discrete logarithm of $a$ to the base $r$ modulo $p$: The integer $e$ with $0 \leq e \leq p-1$ such that $r^e \equiv a \, (\operatorname{mod} p)$.  
- 离散对数：以 $r$ 为底 $a$ 模 $p$ 的离散对数是整数 $e$，满足 $0 \leq e \leq p-1$ 且 $r^e \equiv a \, (\operatorname{mod} p)$。

- **Encryption**: The process of making a message secret.  
- **加密**：使消息保密的过程。

- **Decryption**: The process of returning a secret message to its original form.  
- **解密**：将密文恢复为原始明文的过程。

- **Encryption key**: A value that determines which of a family of encryption functions is to be used.  
- **加密密钥**：确定使用哪一种加密函数族中的函数的值。

- **Shift cipher**: A cipher that encrypts the plaintext letter $p$ as $(p + k) \mod m$ for an integer $k$.  
- **移位密码**：将明文字母 $p$ 加密为 $(p + k) \mod m$ 的密码，其中 $k$ 是一个整数。

- **Affine cipher**: A cipher that encrypts the plaintext letter $p$ as $(ap + b) \mod m$ for integers $a$ and $b$ with $\operatorname{gcd}(a, 26) = 1$.  
- **仿射密码**：将明文字母 $p$ 加密为 $(ap + b) \mod m$ 的密码，其中 $a$ 和 $b$ 是整数，且 $\operatorname{gcd}(a, 26) = 1$。

- **Character cipher**: A cipher that encrypts characters one by one.  
- **字符密码**：逐个字符加密的密码。

- **Block cipher**: A cipher that encrypts blocks of characters of a fixed size.  
- **分组密码**：加密固定大小的字符块的密码。

- **Cryptanalysis**: The process of recovering the plaintext from ciphertext without knowledge of the encryption method, or with knowledge of the encryption method, but not the key.  
- **密码分析**：在不知道加密方法的情况下，或者知道加密方法但不知道密钥的情况下，从密文中恢复明文的过程。

- **Cryptosystem**: A five-tuple $(\mathcal{P}, \mathcal{C}, \mathcal{K}, \mathcal{E}, \mathcal{D})$ where $\mathcal{P}$ is the set of plaintext messages, $\mathcal{C}$ is the set of ciphertext messages, $\mathcal{K}$ is the set of keys, $\mathcal{E}$ is the set of encryption functions, and $\mathcal{D}$ is the set of decryption functions.  
- **密码体制**：一个五元组 $(\mathcal{P}, \mathcal{C}, \mathcal{K}, \mathcal{E}, \mathcal{D})$，其中 $\mathcal{P}$ 是明文消息的集合，$\mathcal{C}$ 是密文消息的集合，$\mathcal{K}$ 是密钥的集合，$\mathcal{E}$ 是加密函数的集合，$\mathcal{D}$ 是解密函数的集合。

- **Private key encryption**: Encryption where both encryption keys and decryption keys must be kept secret.  
- **私钥加密**：加密和解密密钥都必须保密的加密方式。

- **Public key encryption**: Encryption where encryption keys are public knowledge, but decryption keys are kept secret.  
- **公钥加密**：加密密钥是公开的，但解密密钥保密的加密方式。

- **RSA cryptosystem**: The cryptosystem where $\mathcal{P}$ and $\mathcal{C}$ are both $Z_{26}$, $\mathcal{K}$ is the set of pairs $k = (n, e)$ where $n = pq$ where $p$ and $q$ are large primes and $e$ is a positive integer, $E_k(p) = p^e \mod n$, and $D_k(c) = c^d \mod n$ where $d$ is the inverse of $e$ modulo $(p-1)(q-1)$.  
- **RSA 密码体制**：明文集合和密文集合都是 $Z_{26}$，密钥集合是 $k = (n, e)$ 的集合，其中 $n = pq$，$p$ 和 $q$ 是大素数，$e$ 是正整数，加密函数 $E_k(p) = p^e \mod n$，解密函数 $D_k(c) = c^d \mod n$，其中 $d$ 是 $e$ 模 $(p-1)(q-1)$ 的逆元。

- **Key exchange protocol**: A protocol used for two parties to generate a shared key.  
- **密钥交换协议**：用于两个参与者生成共享密钥的协议。

- **Digital signature**: A method that a recipient can use to determine that the purported sender of a message actually sent the message.  
- **数字签名**：一种方法，接收者可以用它来确定声称发送消息的人是否真正发送了该消息。

- **Fully homomorphic cryptosystem**: A cryptosystem that allows arbitrary computations to be run on encrypted data so that the output is the encryption of the unencrypted output of the unencrypted input.  
- **全同态密码体制**：一种密码体制，允许在加密数据上运行任意计算，使得输出是未加密输入的未加密输出的加密。

## RESULTS

- **Division algorithm**: Let $a$ and $d$ be integers with $d$ positive. Then there are unique integers $q$ and $r$ with $0 \leq r < d$ such that $a = dq + r$.  
- **除法算法**：设 $a$ 和 $d$ 是整数，且 $d$ 为正数。那么存在唯一的整数 $q$ 和 $r$，满足 $0 \leq r < d$，使得 $a = dq + r$。

- Let $b$ be an integer greater than 1. Then if $n$ is a positive integer, it can be expressed uniquely in the form $n = a_k b^k + a_{k-1} b^{k-1} + \cdots + a_1 b + a_0$.  
- 设 $b$ 是大于 1 的整数。那么如果 $n$ 是正整数，它可以唯一地表示为 $n = a_k b^k + a_{k-1} b^{k-1} + \cdots + a_1 b + a_0$ 的形式。

- The algorithm for finding the base $b$ expansion of an integer (see Algorithm 1 in Section 4.2).  
- 求整数的 $b$ 进制展开的算法（见第 4.2 节的算法 1）。

- The conventional algorithms for addition and multiplication of integers (given in Section 4.2).  
- 整数加法和乘法的常规算法（见第 4.2 节）。

- The fast modular exponentiation algorithm (see Algorithm 5 in Section 4.2).  
- 快速模幂算法（见第 4.2 节的算法 5）。

- **Euclidean algorithm**: For finding greatest common divisors by successively using the division algorithm (see Algorithm 1 in Section 4.3).  
- **欧几里得算法**：通过反复使用除法算法来求最大公因数（见第 4.3 节的算法 1）。

- **Bézout's theorem**: If $a$ and $b$ are positive integers, then $\operatorname{gcd}(a, b)$ is a linear combination of $a$ and $b$.  
- **贝祖定理**：如果 $a$ 和 $b$ 是正整数，那么 $\operatorname{gcd}(a, b)$ 是 $a$ 和 $b$ 的线性组合。

- **Sieve of Eratosthenes**: A procedure for finding all primes not exceeding a specified number $n$, described in Section 4.3.  
- **埃拉托斯特尼筛法**：一种用于找出不超过指定数 $n$ 的所有素数的方法，描述于第 4.3 节。

- **Fundamental theorem of arithmetic**: Every positive integer can be written uniquely as the product of primes, where the prime factors are written in order of increasing size.  
- **算术基本定理**：每一个正整数都可以唯一地表示为素数的乘积，其中素数因子按从小到大的顺序排列。

- If $a$ and $b$ are positive integers, then $ab = \operatorname{gcd}(a, b) \cdot \operatorname{lcm}(a, b)$.  
- 如果 $a$ 和 $b$ 是正整数，那么 $ab = \operatorname{gcd}(a, b) \cdot \operatorname{lcm}(a, b)$。

- If $m$ is a positive integer and $\operatorname{gcd}(a, m) = 1$, then $a$ has a unique inverse modulo $m$.  
- 如果 $m$ 是正整数且 $\operatorname{gcd}(a, m) = 1$，那么 $a$ 模 $m$ 有唯一的逆元。