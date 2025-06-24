$\land$,AND (Conjunction)

$\lor$,OR(Disjunction)


DNF, 析取范式, $(\land)\lor(\land)$

CNF, 合取范式, $(\lor)\land(\lor)$

p iff q : $p \leftrightarrow q$, p exactly when q.





# 表6 逻辑等价式
| 等价式 | 名称 |
| ---- | ---- |
| $p \land T = p$ | 恒等律 |
| $p \lor F = p$ | 恒等律 |
| $p \lor T \equiv T$ | 支配律 |
| $p \land F = F$ | 支配律 |
| $p \lor p \equiv p$ | 幂等律 |
| $p \land p \equiv p$ | 幂等律 |
| $\neg(\neg p) \equiv p$ | 双重否定律 |
| $p \lor q \equiv q \lor p$ | 交换律 |
| $p \land q \equiv q \land p$ | 交换律 |
| $(p \lor q) \lor r \equiv p \lor (q \lor r)$ | 结合律 |
| $(p \land q) \land r \equiv p \land (q \land r)$ | 结合律 |
| $p \lor (q \land r) \equiv (p \lor q) \land (p \lor r)$ | 分配律 |
| $p \land (q \lor r) \equiv (p \land q) \lor (p \land r)$ | 分配律 |
| $\neg(p \land q) \equiv \neg p \lor \neg q$ | 德·摩根律 |
| $\neg(p \lor q) \equiv \neg p \land \neg q$ | 德·摩根律 |
| $p \lor (p \land q) \equiv p$ | 吸收律 |
| $p \land (p \lor q) \equiv p$ | 吸收律 |
| $p \lor \neg p \equiv T$ | 否定律 |
| $p \land \neg p \equiv F$ | 否定律 |

# 表7 条件命题的逻辑等价式
| 等价式 |
| ---- |
| $p \to q \equiv \neg p \lor q$ |
| $p \to q \equiv \neg q \to \neg p$ |
| $p \lor q \equiv \neg p \to q$ |
| $p \land q \equiv \neg(p \to \neg q)$ |
| $\neg(p \to q) \equiv p \land \neg q$ |
| $(p \to q) \land (p \to r) \equiv p \to (q \land r)$ |
| $(p \to r) \land (q \to r) \equiv (p \lor q) \to r$ |
| $(p \to q) \lor (p \to r) \equiv p \to (q \lor r)$ |
| $(p \to r) \lor (q \to r) \equiv (p \land q) \to r$ |

# 表8 双条件命题的逻辑等价式
| 等价式 |
| ---- |
| $p \leftrightarrow q \equiv (p \to q) \land (q \to p)$ |
| $p \leftrightarrow q \equiv \neg p \leftrightarrow \neg q$ |
| $p \leftrightarrow q \equiv (p \land q) \lor (\neg p \land \neg q)$ |
| $\neg(p \leftrightarrow q) \equiv p \leftrightarrow \neg q$ |
