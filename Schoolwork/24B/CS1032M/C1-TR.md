# Key Terms and Results

## Terms

- **proposition**: a statement that is true or false
- **propositional variable**: a variable that represents a proposition
- **truth value**: true or false
- **¬p (negation of p)**: the proposition with truth value opposite to the truth value of $p$
- **logical operators**: operators used to combine propositions
- **compound proposition**: a proposition constructed by combining propositions using logical operators
- **truth table**: a table displaying all possible truth values of propositions
- **p ∨ q (disjunction of p and q)**: the proposition “$p$ or $q$,” which is true if and only if at least one of $p$ and $q$ is true
- **p ∧ q (conjunction of p and q)**: the proposition “$p$ and $q$,” which is true if and only if both $p$ and $q$ are true
- **p ⊕ q (exclusive or of p and q)**: the proposition “$p$ XOR $q$,” which is true when exactly one of $p$ and $q$ is true
- **p → q (p implies q)**: the proposition “if $p$, then $q$,” which is false if and only if $p$ is true and $q$ is false
- **converse of p → q**: the conditional statement $q → p$
- **contrapositive of p → q**: the conditional statement $¬q → ¬p$
- **inverse of p → q**: the conditional statement $¬p → ¬q$
- **p ↔ q (biconditional)**: the proposition “$p$ if and only if $q$,” which is true if and only if $p$ and $q$ have the same truth value
- **bit**: either a 0 or a 1
- **Boolean variable**: a variable that has a value of 0 or 1
- **bit operation**: an operation on a bit or bits
- **bit string**: a list of bits
- **bitwise operations**: operations on bit strings that operate on each bit in one string and the corresponding bit in the other string
- **logic gate**: a logic element that performs a logical operation on one or more bits to produce an output bit
- **logic circuit**: a switching circuit made up of logic gates that produces one or more output bits
- **tautology**: a compound proposition that is always true
- **contradiction**: a compound proposition that is always false
- **contingency**: a compound proposition that is sometimes true and sometimes false
- **consistent compound propositions**: compound propositions for which there is an assignment of truth values to the variables that makes all these propositions true
- **satisfiable compound proposition**: a compound proposition for which there is an assignment of truth values to its variables that makes it true
- **logically equivalent compound propositions**: compound propositions that always have the same truth values
- **predicate**: part of a sentence that attributes a property to the subject
- **propositional function**: a statement containing one or more variables that becomes a proposition when each of its variables is assigned a value or is bound by a quantifier
- **domain (or universe) of discourse**: the values a variable in a propositional function may take
- **∃x P(x) (existential quantification of P(x))**: the proposition that is true if and only if there exists an $x$ in the domain such that $P(x)$ is true
- **∀x P(x) (universal quantification of P(x))**: the proposition that is true if and only if $P(x)$ is true for every $x$ in the domain
- **logically equivalent expressions**: expressions that have the same truth value no matter which propositional functions and domains are used
- **free variable**: a variable not bound in a propositional function
- **bound variable**: a variable that is quantified
- **scope of a quantifier**: portion of a statement where the quantifier binds its variable
- **argument**: a sequence of statements
- **argument form**: a sequence of compound propositions involving propositional variables
- **premise**: a statement, in an argument, or argument form, other than the final one
- **conclusion**: the final statement in an argument or argument form
- **valid argument form**: a sequence of compound propositions involving propositional variables where the truth of all the premises implies the truth of the conclusion
- **valid argument**: an argument with a valid argument form
- **rule of inference**: a valid argument form that can be used in the demonstration that arguments are valid
- **fallacy**: an invalid argument form often used incorrectly as a rule of inference (or sometimes, more generally, an incorrect argument)
- **circular reasoning or begging the question**: reasoning where one or more steps are based on the truth of the statement being proved
- **theorem**: a mathematical assertion that can be shown to be true
- **conjecture**: a mathematical assertion proposed to be true, but that has not been proved
- **proof**: a demonstration that a theorem is true
- **axiom**: a statement that is assumed to be true and that can be used as a basis for proving theorems
- **lemma**: a theorem used to prove other theorems
- **corollary**: a proposition that can be proved as a consequence of a theorem that has just been proved
- **vacuous proof**: a proof that $p → q$ is true based on the fact that $p$ is false
- **trivial proof**: a proof that $p → q$ is true based on the fact that $q$ is true
- **direct proof**: a proof that $p → q$ is true that proceeds by showing that $q$ must be true when $p$ is true
- **proof by contraposition**: a proof that $p → q$ is true that proceeds by showing that $p$ must be false when $q$ is false
- **proof by contradiction**: a proof that $p$ is true based on the truth of the conditional statement $¬p → q$, where $q$ is a contradiction
- **exhaustive proof**: a proof that establishes a result by checking a list of all possible cases
- **proof by cases**: a proof broken into separate cases, where these cases cover all possibilities
- **without loss of generality**: an assumption in a proof that makes it possible to prove a theorem by reducing the number of cases to consider in the proof
- **counterexample**: an element $x$ such that $P(x)$ is false
- **constructive existence proof**: a proof that an element with a specified property exists that explicitly finds such an element
- **nonconstructive existence proof**: a proof that an element with a specified property exists that does not explicitly find such an element
- **rational number**: a number that can be expressed as the ratio of two integers $p$ and $q$ such that $q ≠ 0$
- **uniqueness proof**: a proof that there is exactly one element satisfying a specified property

## Results

- The logical equivalences given in Tables 6, 7, and 8 in Section 1.3.
- De Morgan’s laws for quantifiers.
- Rules of inference for propositional calculus.
- Rules of inference for quantified statements.



# CN

## Terms

- **proposition**: a statement that is true or false  
- **命题**：一个陈述，其值为真或假。

- **propositional variable**: a variable that represents a proposition  
- **命题变量**：表示命题的变量。

- **truth value**: true or false  
- **真值**：真或假。

- **¬p (negation of p)**: the proposition with truth value opposite to the truth value of $p$  
- **¬p（p的否定）**：其真值与$p$的真值相反的命题。

- **logical operators**: operators used to combine propositions  
- **逻辑运算符**：用于组合命题的运算符。

- **compound proposition**: a proposition constructed by combining propositions using logical operators  
- **复合命题**：通过使用逻辑运算符组合命题而构造的命题。

- **truth table**: a table displaying all possible truth values of propositions  
- **真值表**：显示命题所有可能真值的表格。

- **p ∨ q (disjunction of p and q)**: the proposition “$p$ or $q$,” which is true if and only if at least one of $p$ and $q$ is true  
- **p ∨ q（p和q的析取）**：命题“$p$或$q$”，当且仅当$p$和$q$中至少有一个为真时为真。

- **p ∧ q (conjunction of p and q)**: the proposition “$p$ and $q$,” which is true if and only if both $p$ and $q$ are true  
- **p ∧ q（p和q的合取）**：命题“$p$和$q$”，当且仅当$p$和$q$都为真时为真。

- **p ⊕ q (exclusive or of p and q)**: the proposition “$p$ XOR $q$,” which is true when exactly one of $p$ and $q$ is true  
- **p ⊕ q（p和q的异或）**：命题“$p$ XOR $q$”，当且仅当$p$和$q$中恰好有一个为真时为真。

- **p → q (p implies q)**: the proposition “if $p$, then $q$,” which is false if and only if $p$ is true and $q$ is false  
- **p → q（p蕴含q）**：命题“如果$p$，则$q$”，当且仅当$p$为真且$q$为假时为假。

- **converse of p → q**: the conditional statement $q → p$  
- **p → q的逆命题**：条件命题$q → p$。

- **contrapositive of p → q**: the conditional statement $¬q → ¬p$  
- **p → q的逆否命题**：条件命题$¬q → ¬p$。

- **inverse of p → q**: the conditional statement $¬p → ¬q$  
- **p → q的反命题**：条件命题$¬p → ¬q$。

- **p ↔ q (biconditional)**: the proposition “$p$ if and only if $q$,” which is true if and only if $p$ and $q$ have the same truth value  
- **p ↔ q（双向条件命题）**：命题“$p$当且仅当$q$”，当且仅当$p$和$q$具有相同的真值时为真。

- **bit**: either a 0 or a 1  
- **位**：0或1。

- **Boolean variable**: a variable that has a value of 0 or 1  
- **布尔变量**：值为0或1的变量。

- **bit operation**: an operation on a bit or bits  
- **位运算**：对位或多位进行的运算。

- **bit string**: a list of bits  
- **位串**：一系列位。

- **bitwise operations**: operations on bit strings that operate on each bit in one string and the corresponding bit in the other string  
- **逐位运算**：在位串上进行的运算，对一个字符串中的每一位和另一个字符串中对应的位进行操作。

- **logic gate**: a logic element that performs a logical operation on one or more bits to produce an output bit  
- **逻辑门**：对一个或多个位进行逻辑运算以产生输出位的逻辑元件。

- **logic circuit**: a switching circuit made up of logic gates that produces one or more output bits  
- **逻辑电路**：由逻辑门组成的开关电路，产生一个或多个输出位。

- **tautology**: a compound proposition that is always true  
- **永真命题**：总是为真的复合命题。

- **contradiction**: a compound proposition that is always false  
- **矛盾命题**：总是为假的复合命题。

- **contingency**: a compound proposition that is sometimes true and sometimes false  
- **可满足命题**：有时为真、有时为假的复合命题。

- **consistent compound propositions**: compound propositions for which there is an assignment of truth values to the variables that makes all these propositions true  
- **一致的复合命题**：存在一种变量的真值赋值，使得所有这些复合命题都为真的复合命题。

- **satisfiable compound proposition**: a compound proposition for which there is an assignment of truth values to its variables that makes it true  
- **可满足的复合命题**：存在一种变量的真值赋值，使得该复合命题为真的复合命题。

- **logically equivalent compound propositions**: compound propositions that always have the same truth values  
- **逻辑等价的复合命题**：总是具有相同真值的复合命题。

- **predicate**: part of a sentence that attributes a property to the subject  
- **谓词**：句子中表示主语具有某种属性的部分。

- **propositional function**: a statement containing one or more variables that becomes a proposition when each of its variables is assigned a value or is bound by a quantifier  
- **命题函数**：包含一个或多个变量的陈述，当其每个变量被赋值或被量词约束时成为命题。

- **domain (or universe) of discourse**: the values a variable in a propositional function may take  
- **论域（或全集）**：命题函数中变量可以取的值的集合。

- **∃x P(x) (existential quantification of P(x))**: the proposition that is true if and only if there exists an $x$ in the domain such that $P(x)$ is true  
- **∃x P(x)（P(x)的存在量词）**：当且仅当存在论域中的一个$x$使得$P(x)$为真时，该命题为真。

- **∀x P(x) (universal quantification of P(x))**: the proposition that is true if and only if $P(x)$ is true for every $x$ in the domain  
- **∀x P(x)（P(x)的全称量词）**：当且仅当$P(x)$对论域中的每一个$x$都为真时，该命题为真。

- **logically equivalent expressions**: expressions that have the same truth value no matter which propositional functions and domains are used  
- **逻辑等价的表达式**：无论使用何种命题函数和论域，都具有相同真值的表达式。

- **free variable**: a variable not bound in a propositional function  
- **自由变量**：在命题函数中未被约束的变量。

- **bound variable**: a variable that is quantified  
- **约束变量**：被量化的变量。

- **scope of a quantifier**: portion of a statement where the quantifier binds its variable  
- **量词的辖域**：量词约束其变量的陈述部分。

- **argument**: a sequence of statements  
- **论证**：一系列陈述。

- **argument form**: a sequence of compound propositions involving propositional variables  
- **论证形式**：涉及命题变量的复合命题序列。

- **premise**: a statement, in an argument, or argument form, other than the final one  
- **前提**：在论证或论证形式中，除了最后一条之外的陈述。

- **conclusion**: the final statement in an argument or argument form  
- **结论**：论证或论证形式中的最后一条陈述。

- **valid argument form**: a sequence of compound propositions involving propositional variables where the truth of all the premises implies the truth of the conclusion  
- **有效论证形式**：涉及命题变量的复合命题序列，其中所有前提的真值蕴含结论的真值。

- **valid argument**: an argument with a valid argument form  
- **有效论证**：具有有效论证形式的论证。

- **rule of inference**: a valid argument form that can be used in the demonstration that arguments are valid  
- **推理规则**：可用于证明论证有效的有效论证形式。

- **fallacy**: an invalid argument form often used incorrectly as a rule of inference (or sometimes, more generally, an incorrect argument)  
- **谬误**：通常被错误地用作推理规则的无效论证形式（或者更一般地，一个错误的论证）。

- **circular reasoning or begging the question**: reasoning where one or more steps are based on the truth of the statement being proved  
- **循环论证或乞题**：论证中的一个或多个步骤基于正在证明的陈述的真实性。

- **theorem**: a mathematical assertion that can be shown to be true  
- **定理**：可以证明为真的数学命题。

- **conjecture**: a mathematical assertion proposed to be true, but that has not been proved  
- **猜想**：被提出为真的数学命题，但尚未被证明。

- **proof**: a demonstration that a theorem is true  
- **证明**：证明一个定理为真的过程。

- **axiom**: a statement that is assumed to be true and that can be used as a basis for proving theorems  
- **公理**：被假设为真，并且可以作为证明定理基础的陈述。

- **lemma**: a theorem used to prove other theorems  
- **引理**：用于证明其他定理的定理。

- **corollary**: a proposition that can be proved as a consequence of a theorem that has just been proved  
- **推论**：作为刚刚证明的定理的推论而可以被证明的命题。

- **vacuous proof**: a proof that $p → q$ is true based on the fact that $p$ is false  
- **空洞证明**：基于$p$为假，证明$p → q$为真的证明。

- **trivial proof**: a proof that $p → q$ is true based on the fact that $q$ is true  
- **平凡证明**：基于$q$为真，证明$p → q$为真的证明。

- **direct proof**: a proof that $p → q$ is true that proceeds by showing that $q$ must be true when $p$ is true  
- **直接证明**：通过证明当$p$为真时，$q$也必须为真，从而证明$p → q$为真的证明。

- **proof by contraposition**: a proof that $p → q$ is true that proceeds by showing that $p$ must be false when $q$ is false  
- **逆否证明**：通过证明当$q$为假时，$p$也必须为假，从而证明$p → q$为真的证明。

- **proof by contradiction**: a proof that $p$ is true based on the truth of the conditional statement $¬p → q$, where $q$ is a contradiction  
- **反证法**：基于条件命题$¬p → q$为真，其中$q$是一个矛盾，从而证明$p$为真的证明。

- **exhaustive proof**: a proof that establishes a result by checking a list of all possible cases  
- **穷举证明**：通过检查所有可能情况的列表来建立结果的证明。

- **proof by cases**: a proof broken into separate cases, where these cases cover all possibilities  
- **分情况证明**：将证明分解为分别处理的情况，这些情况覆盖所有可能性。

- **without loss of generality**: an assumption in a proof that makes it possible to prove a theorem by reducing the number of cases to consider in the proof  
- **不失一般性**：在证明中的一种假设，通过减少需要考虑的情况数量来证明定理。

- **counterexample**: an element $x$ such that $P(x)$ is false  
- **反例**：一个元素$x$，使得$P(x)$为假。

- **constructive existence proof**: a proof that an element with a specified property exists that explicitly finds such an element  
- **构造性存在证明**：明确找到具有指定属性的元素的证明，证明这样的元素存在。

- **nonconstructive existence proof**: a proof that an element with a specified property exists that does not explicitly find such an element  
- **非构造性存在证明**：证明具有指定属性的元素存在，但没有明确找到这样的元素的证明。

- **rational number**: a number that can be expressed as the ratio of two integers $p$ and $q$ such that $q ≠ 0$  
- **有理数**：可以表示为两个整数$p$和$q$的比值的数，其中$q ≠ 0$。

- **uniqueness proof**: a proof that there is exactly one element satisfying a specified property  
- **唯一性证明**：证明恰好有一个元素满足指定属性的证明。

## Results

- The logical equivalences given in Tables 6, 7, and 8 in Section 1.3.  
- 第1.3节中表6、7和8给出的逻辑等价关系。

- De Morgan’s laws for quantifiers.  
- 量词的德摩根定律。

- Rules of inference for propositional calculus.  
- 命题逻辑的推理规则。

- Rules of inference for quantified statements.  
- 量化命题的推理规则。