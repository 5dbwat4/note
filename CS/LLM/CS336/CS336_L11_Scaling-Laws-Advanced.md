---
title: "Lecture 11: Scaling Laws — Advanced Details"
---

# Lecture 11: Scaling Laws — Advanced Details / 第十一讲：缩放定律——进阶细节

---

## 1. Introduction and Overview / 引言与概述

**EN:** Today we continue our scaling journey, diving into the more advanced details of scaling laws and how we scale up models in practice. We will cover questions like: do the classical scaling laws actually work at real open-source model scales? We will also discuss optimization details, learning rate tricks, and how to carefully think about learning rates, batch sizes, and initializations as a function of scale. Since the classical scaling law era (Kaplan, Chinchilla), there have been a number of scaling papers published, mostly by the open-source community in China. We will curate several of these to give a sense of what scaling at the frontier looks like today.

**ZH:** 今天我们将继续缩放定律的探索之旅，深入探讨缩放定律的更高级细节，以及如何在实践中扩缩模型。我们将探讨以下问题：经典的缩放定律在实际开源模型规模下是否真的有效？我们还会讨论优化细节、学习率技巧，以及如何仔细地将学习率、批大小和初始化视为规模的函数来考量。自经典缩放定律时代（Kaplan、Chinchilla）以来，已涌现出许多缩放相关的论文，主要来自中国的开源社区。我们将精选其中若干篇，带大家感受当今前沿的缩放工作面貌。

**EN:** The lecture has two main parts. First, we will go through several key papers that show what scaling at the open frontier looks like, covering MiniCPM, DeepSeek, and more recent releases from Qwen, Kimi K2, Hunyuan, LLaMA 3, and MiniMax-01. Second, we will discuss optimizers and initializations, including how to tune sensitive hyperparameters like learning rates and batch sizes. We will examine two contrasting approaches: the DeepSeek approach of fitting scaling laws to hyperparameters, and the MiniCPM approach of using reparameterization (muP) to achieve scale invariance.

**ZH:** 本讲分为两个主要部分。首先，我们将浏览若干关键论文，了解开放前沿的缩放工作面貌，涵盖 MiniCPM、DeepSeek 以及来自 Qwen、Kimi K2、Hunyuan、LLaMA 3 和 MiniMax-01 的更新发布。其次，我们将讨论优化器和初始化，包括如何调节学习率和批大小等敏感超参数。我们将考察两种截然不同的方法：一种是 DeepSeek 的为超参数拟合缩放定律的方法，另一种是 MiniCPM 使用重参数化（μP）来实现尺度不变性的方法。

---

## 2. MiniCPM: μP and WSD Learning Rate / MiniCPM：μP 与 WSD 学习率

### 2.1 Overview of MiniCPM / MiniCPM 概述

**EN:** MiniCPM is a high-performance small language model developed by a consortium of industry and academic researchers in the Chinese open-source community, targeting the 1–2 billion parameter bracket. At the time of its release in 2024, it was state-of-the-art for that size range. The paper is notable because it presents a clear recipe for how to scale up a model without brute-forcing hyperparameters at the target size. Instead, the authors train smaller models and establish a scaling ladder that lets them predict the optimal settings for a model roughly five times larger.

**ZH:** MiniCPM 是由中国开源社区的产学研联合团队开发的高性能小型语言模型，目标参数规模为 10 亿到 20 亿。在 2024 年发布时，它在该规模范围内是当时的最先进水平。这篇论文之所以引人注目，在于它提供了一份清晰的配方，说明如何在不需要在目标规模上暴力搜索超参数的情况下扩缩模型。作者的策略是训练更小的模型，并建立一条扩缩阶梯，让他们能够为大约五倍大的模型预测最优参数设置。

### 2.2 μP: Maximal Update Parameterization / μP：最大更新参数化

**EN:** The first key technique from MiniCPM is a special class of initializations called μP (maximal update parameterization). The goal of μP is to ensure that the optimal learning rate remains the same as you scale the model up or down. In the MiniCPM implementation, they scale the embedding output, scale residual connections by the square root of the number of layers, scale matrix-shaped tensor initializations by the fan-in/fan-out ratio, and apply per-parameter learning rate scaling. The LM head also receives special scaling treatment.

**ZH:** MiniCPM 的第一个关键技术是一类特殊的初始化方法，称为 μP（最大更新参数化）。μP 的目标是确保在扩缩模型时，最优学习率保持不变。在 MiniCPM 的实现中，他们对嵌入输出进行缩放，按层数的平方根缩放残差连接，按 fan-in/fan-out 比率缩放矩阵形状张量的初始化，并对每个参数施加学习率缩放。LM 头也受到了特殊的缩放处理。

**EN:** The results from MiniCPM validate that μP works well for stabilizing the optimal learning rate. When they sweep the learning rate across various model sizes, the minimum loss consistently lands at around 10⁻², with only slight deviations for the smallest model. This success removes the need to re-tune the learning rate for each model size, which is a significant practical benefit. However, even with μP fixing the learning rate, the optimal batch size still varies as a function of model size and dataset size.

**ZH:** MiniCPM 的实验结果验证了 μP 在稳定最优学习率方面非常有效。当他们跨不同模型规模扫描学习率时，最小损失始终落在约 10⁻² 附近，仅最小模型有轻微偏差。这一成功消除了为每个模型规模重新调节学习率的必要，带来了显著的实际好处。然而，即使 μP 固定了学习率，最优批大小仍然作为模型规模和数据集大小的函数而变化。

### 2.3 Optimal Batch Size Scaling / 最优批大小的缩放

**EN:** The MiniCPM team runs many training runs with fixed batch sizes and varies the number of tokens processed. By fitting quadratic curves to the equal-loss contours, they find that the optimal batch size follows a power-law structure with respect to the target loss. This mirrors the Kaplan-style critical batch size analysis: lower loss requires a larger batch size. Given a particular loss target derived from the scaling laws, you can set the optimal batch size that provides the best trade-offs.

**ZH:** MiniCPM 团队以固定的批大小进行大量训练，并改变处理的 token 数量。通过对等损失等高线拟合二次曲线，他们发现最优批大小相对于目标损失呈现幂律结构。这与 Kaplan 式的临界批大小分析一脉相承：损失越低，需要的批大小越大。根据缩放定律推导出特定损失目标后，即可设定能够提供最佳权衡的最优批大小。

### 2.4 WSD Learning Rate Schedule / WSD 学习率调度

**EN:** One of the most practically useful contributions from the MiniCPM paper is the warmup-stable-decay (WSD) learning rate schedule. In a standard cosine learning rate schedule, you must know the total training budget upfront because the entire schedule depends on the terminal step count. This means you cannot simply extend a training run—you must retrain from scratch. The WSD schedule solves this: it consists of a warmup phase (a fixed number of steps, independent of the training horizon), a long stable phase where the learning rate is held constant, and a final decay phase (typically 10–20% of training) where the rate drops rapidly to near zero, usually to about 10% of the maximum learning rate.

**ZH:** MiniCPM 论文中最具实用价值的贡献之一，是 WSD（预热-稳定-衰减）学习率调度。在标准的余弦学习率调度中，你必须提前知道总训练预算，因为整个调度取决于最终的步数。这意味着你无法简单地延长训练——必须从头重新训练。WSD 调度解决了这个问题：它包含一个预热阶段（固定步数，与训练长度无关）、一个较长的稳定阶段（学习率保持恒定），以及最后一个衰减阶段（通常占训练的 10–20%），在此阶段学习率迅速下降到接近零，通常降至最大学习率的约 10%。

**EN:** WSD is popular because it allows you to restart a run at any point at the end of the stable phase. If you want to train for longer, you simply roll back to the last stable checkpoint, run forward at the stable learning rate, and then re-decay. This makes data-scaling experiments dramatically cheaper: you only pay the cost of re-decaying (roughly 10% of the total), rather than retraining from scratch. Anecdotally, many practitioners find that cosine is slightly better in some cases, but WSD is comparably good in most situations and far more versatile. A key lesson from WSD is just how crucial the learning rate decay phase is for achieving good final performance—the model appears to underperform until the decay phase, at which point it reclaims all its gains.

**ZH:** WSD 之所以流行，是因为它允许你在稳定阶段结束后的任意点重启训练。如果你想要训练更长时间，只需回退到上一个稳定阶段的检查点，在稳定学习率下继续前向训练，然后重新衰减即可。这使得数据缩放实验的成本大幅降低：你只需支付重新衰减的代价（约占总量 10%），而无需从头重新训练。据传闻，许多实践者发现余弦调度在某些情况下略占优势，但 WSD 在大多数场景中表现基本相当且更加灵活。WSD 的一个关键启示是：学习率衰减阶段对于达到良好的最终性能至关重要——模型在衰减阶段之前看似表现不佳，但一旦进入衰减阶段便会收复所有收益。

---

## 3. DeepSeek: Scaling Laws for Hyperparameters / DeepSeek：超参数的缩放定律

### 3.1 Overview / 概述

**EN:** The original DeepSeek paper takes a very different scaling strategy from MiniCPM. Rather than using μP to stabilize hyperparameters across scales, DeepSeek fits scaling laws to estimate both the optimal batch size and learning rate. Their philosophy is: if hyperparameters change predictably with scale according to a power law, we do not need to worry about invariance—we just need to discover the relationship. The paper runs extensive grid searches at multiple scales to find the optimal hyperparameter combinations, then fits lines to those optima as a function of non-embedding FLOPs.

**ZH:** 最初的 DeepSeek 论文采用了与 MiniCPM 截然不同的缩放策略。DeepSeek 并不使用 μP 来跨尺度稳定超参数，而是拟合缩放定律来估算最优批大小和最优学习率。他们的理念是：如果超参数按照幂律随规模可预测地变化，我们就不需要担心不变性问题——只需要发现这种关系即可。论文在多个规模上进行了广泛的网格搜索，以找到最优超参数组合，然后将这些最优值作为非嵌入 FLOPs 的函数拟合为直线。

**EN:** The DeepSeek LLM paper is, even years later, one of the more nicely executed scaling analyses in the open world. The attention to detail and the quality of their experiments made it clear even before the famous R1 release that these were serious researchers. Their scaling curves for the IsoFLOP analysis produce clean sweeps across fixed compute ranges, and their Chinchilla-style trade-off curves are well-behaved. The final punchline is that the actual large models they train (the stars on their scaling plots) land close to the predictions from their scaling law fits based on smaller models.

**ZH:** DeepSeek LLM 论文即使在多年之后，仍是开源领域最精心执行的缩放分析之一。他们对细节的关注和实验质量，甚至在著名的 R1 发布之前就让人清楚地感受到这些研究者的严肃程度。他们的 IsoFLOP 分析缩放曲线在固定算力范围内产生了清晰的扫描结果，而 Chinchilla 式的权衡曲线也表现良好。最终的成果是：他们实际训练的大模型（缩放图上的星号）与其基于小模型的缩放定律拟合预测非常接近。

### 3.2 Comparison of Approaches / 方法比较

**EN:** So we have two contrasting philosophies. MiniCPM represents the μP-style approach: reparameterize everything so that optimal hyperparameters are invariant to scale. DeepSeek represents the scaling-law-fitting approach: accept that hyperparameters change with scale, but model that change predictably. Both are valid and have been used successfully. A potential weakness of the DeepSeek approach is that if your grid search is coarse or not centered in the right region, you accumulate quantization error and may get poor scaling law fits—as seen in their somewhat noisy learning-rate scaling plot.

**ZH:** 这样我们就有了两种对比鲜明的哲学。MiniCPM 代表 μP 式的方法：将一切重参数化，使最优超参数与规模无关。DeepSeek 代表缩放定律拟合的方法：接受超参数随规模变化的事实，但以可预测的方式建模这种变化。两者都是有效的，也都得到了成功的应用。DeepSeek 方法的一个潜在弱点是：如果网格搜索过于粗糙或未定位在正确区域，就会累积量化误差，并可能得到较差的缩放定律拟合——正如他们在学习率缩放图上所展示的不太平滑的曲线那样。

---

## 4. Recent Trends in Scaling Papers / 缩放论文的近期趋势

### 4.1 Qwen 2.5 and Qwen 3 / Qwen 2.5 与 Qwen 3

**EN:** In more recent open-source releases, companies have largely converged on the standard scaling recipe. Qwen 2.5 describes doing scaling experiments to find optimal batch sizes and learning rates, then fitting scaling laws to predict the optimum at target scale—basically the same procedure as DeepSeek but extended to MoEs. By Qwen 3, they simply refer back to Qwen 2.5 and note that they follow exactly the same approach. This standardization means that detailed scaling law discussions are less prominent in newer papers, because the core methodology is now assumed knowledge.

**ZH:** 在更近期的开源发布中，各公司已基本收敛到标准缩放配方上。Qwen 2.5 描述了如何通过缩放实验找到最优批大小和学习率，然后拟合缩放定律来预测目标规模下的最优值——基本上与 DeepSeek 相同的流程，但扩展到了 MoE。到了 Qwen 3，他们直接回溯到 Qwen 2.5，并注明遵循完全相同的方案。这种标准化意味着，详细的缩放定律讨论在较新的论文中变得不那么突出，因为核心方法论现在已被视为已知的前提知识。

### 4.2 Kimi K2 and MoE Scaling Laws / Kimi K2 与 MoE 缩放定律

**EN:** By 2026, most companies have switched to MoEs, and the new scaling science frontier concerns MoE-specific questions. Kimi K2, one of the newest papers, focuses on MoE scaling laws: how much sparsity is optimal given a compute budget? They vary the sparsity level and measure how validation loss changes with FLOPs. They find that more sparsity consistently yields better validation loss for a given compute budget, but with diminishing returns. Based on this analysis, they choose a sparsity of 48, because beyond that, the marginal improvement in loss is small. Similar analyses appear in the Hunyuan paper, which fixes sparsity and focuses on the optimal data-to-active-parameter ratio.

**ZH:** 到了 2026 年，大多数公司已转向 MoE，而缩放科学的新前沿集中在 MoE 特定的问题上。Kimi K2 作为最新的论文之一，聚焦在 MoE 缩放定律：在给定的算力预算下，最优的稀疏度是多少？他们改变稀疏度水平，并测量验证损失如何随 FLOPs 变化。他们发现，对于给定的算力预算，高稀疏度始终带来更好的验证损失，但边际收益递减。基于这一分析，他们选择了 48 的稀疏度，因为超过这个值，损失的边际改善很小。类似的分析也出现在 Hunyuan 论文中，该论文固定了稀疏度，并聚焦于最优的数据/激活参数比。

### 4.3 LLaMA 3 and Downstream Accuracy / LLaMA 3 与下游准确率

**EN:** LLaMA 3 includes scaling laws, though they focus on an interesting aspect: the relationship between log loss and downstream accuracy. Their usual scaling law shows that as compute increases, log probability on a benchmark decays consistently. More interestingly, they show that lower log loss correlates with higher downstream accuracy, and they fit a sigmoid function to this relationship. This is valuable because we typically only discuss log loss, but there is often a tight coupling between log loss and downstream accuracy. However, systematic deviations from the fitted sigmoid suggest that the mapping is not perfectly deterministic.

**ZH:** LLaMA 3 包含了缩放定律，尽管它们聚焦在一个有趣的方面：log loss 与下游准确率之间的关系。他们常规的缩放定律显示，随着算力的增加，基准测试上的 log 概率会持续衰减。更有趣的是，他们展示了更低 log loss 与更高下游准确率相关，并对此关系拟合了一条 sigmoid 函数。这很有价值，因为我们在讨论中通常只关注 log loss，但 log loss 与下游准确率之间往往存在紧密的耦合。然而，与拟合 sigmoid 的系统性偏差表明，这种映射并非完美确定。

### 4.4 MiniMax-01: Architecture Scaling / MiniMax-01：架构缩放

**EN:** MiniMax-01 from last year used scaling experiments to justify architectural decisions. They compared lightning attention (a linear attention variant), softmax (full) attention, and a hybrid approach that mixes both. They conducted Kaplan-style scaling analysis to see how the learning curves and optimal parameter counts change as compute increases for each architecture. The results showed that all three architectures were comparable in terms of scaling behavior and required similar model sizes. This analysis justified their choice of the hybrid architecture for the deployed system—exactly the kind of decision-making that scaling laws are meant to enable.

**ZH:** 去年的 MiniMax-01 使用缩放实验来证明架构决策的合理性。他们比较了 lightning attention（一种线性注意力变体）、softmax（全量）注意力以及混合两种方式的方案。他们进行了 Kaplan 式的缩放分析，观察随着算力的增加，每种架构的学习曲线和最优参数数量如何变化。结果显示，三种架构在缩放行为上是可比的，且需要相似的模型规模。这一分析证明了他们为部署系统选择混合架构的合理性——这正是缩放定律理应促成的决策方式。

---

## 5. Hyperparameter Scaling in Depth / 超参数缩放深入分析

### 5.1 The StepFun Survey / StepFun 的超参数研究

**EN:** A recent preprint from StepFun provides one of the most comprehensive grid searches of hyperparameter space. They trained a large number of models, varying learning rate and batch size across a range of model sizes and dataset sizes, producing high-resolution contour plots of the hyperparameter landscape. From these, we can see that the loss surface, as a function of batch size and learning rate, is nicely convex and smooth—which is reassuring, because it means grid-based hyperparameter search is viable and the minimum is not far away.

**ZH:** StepFun 最近的一篇预印本提供了迄今为止最全面的超参数空间网格搜索之一。他们训练了大量模型，在一系列模型规模和数据集规模上改变学习率和批大小，生成了高分辨率的超参数地形等高线图。从中我们可以看到，损失函数表面作为批大小和学习率的函数，表现出了很好的凸性和光滑性——这令人安心，因为它意味着基于网格的超参数搜索是可行的，极小值近在咫尺。

### 5.2 Key Empirical Findings / 关键实证发现

**EN:** One of the most striking findings is that the optimal batch size appears to depend almost exclusively on the total amount of training data, not on the model size. Across different model sizes (different colored dots), the optimal batch size follows roughly the same power-law trend line when plotted against data size on a log-log scale. This is clean and predictable. The optimal learning rate, by contrast, shows a more complex behavior: larger models need smaller learning rates, but larger amounts of data need higher learning rates. This latter finding is somewhat counterintuitive, and different papers have argued for different directions of the data dependence.

**ZH:** 最引人注目的发现之一是：最优批大小似乎几乎仅取决于训练数据的总量，而与模型规模无关。跨不同的模型规模（不同颜色的点），最优批大小在 log-log 图上相对于数据大小基本遵循同一条幂律趋势线。这是非常干净和可预测的。相比之下，最优学习率表现出更复杂的行为：更大的模型需要更小的学习率，但更多的数据需要更大的学习率。后一个发现有些反直觉，不同论文对数据依赖性的方向有不同的论点。

**EN:** The StepFun scaling law ultimately prescribes that batch size should scale roughly as the square root of the amount of data times some constant. The learning rate should scale upward with data but downward with model size. Under Chinchilla-like conditions where both model size and data are driven by compute, these effects partially cancel, and the net result is that learning rate decreases with compute—similar to the DeepSeek law, though with different exponents. An additional finding is that these scaling laws transfer reasonably well to MoEs when controlling for active parameters, though shifting the training data does cause some shift in the optimal values.

**ZH:** StepFun 的缩放定律最终给出如下建议：批大小应大致按数据量的平方根乘以某个常数来缩放。学习率应随数据量向上缩放，但随模型规模向下缩放。在 Chinchilla 式的条件下（模型规模和数据都由算力驱动），这些效应会部分相互抵消，最终结果是学习率随算力下降——与 DeepSeek 定律类似，尽管指数不同。额外发现是，当控制激活参数的情况下，这些缩放定律可以合理地迁移到 MoE，尽管更换训练数据确实会导致最优值发生一定偏移。

### 5.3 Cross-Paper Disagreements / 跨论文的分歧

**EN:** Looking across papers, there is significant disagreement even about what variables should govern the scaling of learning rates and batch sizes. The OpenAI (Kaplan) scaling law expresses batch size as a function of terminal loss. DeepSeek uses non-embedding FLOPs. StepFun claims that batch size scaling is a function of data, not compute or loss. This diversity of input variables underscores that the precise nature of hyperparameter scaling remains unsettled, and the specific formulas are likely contingent on experimental conditions, data, and architecture.

**ZH:** 纵观各篇论文，即使在"哪些变量应主导学习率和批大小的缩放"这一基础问题上，也存在显著分歧。OpenAI（Kaplan）的缩放定律将批大小表达为终端损失的函数。DeepSeek 使用非嵌入 FLOPs。StepFun 声称批大小缩放是数据的函数，而不是算力或损失。这种输入变量的多样性表明，超参数缩放的精确性质尚未确定，具体公式可能依赖于实验条件、数据和架构。

---

## 6. Optimizers and Scale / 优化器与规模

### 6.1 The muon Optimizer Story / Muon 优化器的故事

**EN:** Optimizer choice is scale-dependent, making this a natural topic for a scaling laws lecture. A compelling case study is the muon optimizer. On the NanoGPT speedrun benchmark (which inspired Assignment 1), muon dramatically outperforms Adam at small scale, producing much lower loss in the same training time. This naturally raises the question: does this advantage hold at large scale? Some scaling studies argued that the gain of muon over Adam diminishes as model size increases. The story seemed to close with the conclusion that muon does not scale well—until Kimi K2 released a fully muon-trained model that performed excellently.

**EN:** Muon 优化器的选择是规模依赖的，这使其成为缩放定律讲座的自然话题。一个引人注目的案例研究是 Muon 优化器。在 NanoGPT speedrun 基准（启发了课程作业 1）上，Muon 在小规模上显著优于 AdamW，在相同的训练时间内实现了低得多的损失。这自然引出一个问题：这种优势在大规模上是否成立？一些缩放研究认为，Muon 相对于 AdamW 的增益会随着模型规模的增大而减小。故事似乎以 Muon 在大规模上表现不佳的结论而告终——直到 Kimi K2 发布了一个完全用 Muon 训练的模型，性能出色。

**EN:** The muon story illustrates how difficult it is to know whether something works at scale. Small-scale experiments give us ideas, and those ideas eventually make their way to large models—but the path is neither straight nor guaranteed. Kimi K2 shows that muon can work at scale, but without side-by-side ablations against AdamW at that scale, we still do not know whether it is actually better. The lesson is that scaling is messy, and transferring results from small to large scales is one of the hardest problems in the field.

**ZH:** Muon 的故事说明，判断一个东西在大规模上是否有效，是多么困难。小规模实验给我们提供思路，这些思路最终会进入大模型——但这条路既不笔直，也没有保证。Kimi K2 表明 Muon 可以在大规模上运行，但在该规模上缺乏与 AdamW 并排消融实验的情况下，我们仍然不知道它是否真的更好。启示是：缩放是混乱的，将结果从小规模迁移到大规模是这个领域中最困难的问题之一。

### 6.2 How Muon Works / Muon 的工作原理

**EN:** Muon is a matrix optimizer that operates on the spectral properties of gradients. In standard momentum-based optimization, you compute a gradient, maintain a momentum buffer, and update parameters with the momentum. Muon adds a crucial extra step for matrix-shaped parameters: it orthogonalizes the momentum buffer. Conceptually, this means taking the singular value decomposition of the momentum matrix and setting all singular values to 1—shrinking large singular values and expanding small ones, so every spectral direction has equal unit magnitude. In practice, this is implemented via Newton-Schulz iteration, which approximates orthogonalization using only matrix multiplies, making it GPU-efficient.

**ZH:** Muon 是一种矩阵优化器，它作用于梯度的谱特性。在标准基于动量的优化中，你计算梯度、维护动量缓存，并用动量更新参数。Muon 为矩阵形状的参数添加了关键的一步：它对动量缓存进行正交化。从概念上讲，这意味着对动量矩阵进行奇异值分解，并将所有奇异值设为 1——收缩大的奇异值，放大小的奇异值，使每个谱方向的幅度都统一。在实践中，这通过 Newton-Schulz 迭代来实现，仅用矩阵乘法近似正交化过程，使其在 GPU 上高效运行。

**EN:** The key insight behind muon is that not all parameters in a transformer are the same. Some are matrix-valued (attention weights, MLP weights) and others are vector-valued (RMS norm parameters). Matrix-valued parameters have spectra—eigenvalues and singular values—that you can manipulate. By orthogonalizing the update, muon ensures that every spectral direction contributes equally, analogous to how Adam divides each coordinate by its gradient magnitude. This matrix-specific treatment is what makes muon interesting and powerful, but it also means you still need an optimizer like AdamW for vector-valued parameters, which do not benefit from orthogonalization.

**ZH:** Muon 背后的核心洞见是：Transformer 中并非所有参数都相同。有些是矩阵值的（注意力权重、MLP权重），有些是向量值的（RMS norm 参数）。矩阵值参数具有谱（特征值和奇异值），你可以对其进行操控。通过对更新进行正交化，Muon 确保每个谱方向贡献均等，这类似于 AdamW 将每个坐标除以其梯度幅值。这种针对矩阵的特定处理使 Muon 既有趣又强大，但也意味着你仍然需要像 AdamW 这样的优化器来处理向量值参数，因为它们无法受益于正交化。

### 6.3 Comparing Optimizers at Scale / 大规模上的优化器比较

**EN:** Comparing optimizers rigorously is challenging for two main reasons. First, hyperparameters differ across optimizers and must be tuned carefully—a poorly tuned Adam can look worse than a well-tuned alternative, and vice versa. Second, there are two important scaling axes to consider: compute (model size + data, assuming a fixed Chinchilla ratio) and the Chinchilla ratio itself (data-to-parameter ratio). Some optimizers may perform better in the overparameterized regime (small Chinchilla ratio), while others excel when data is abundant (large Chinchilla ratio). When evaluating muon, some studies found its advantage over Adam diminishes with scale along the compute axis, while others found performance consistent across Chinchilla ratios. Both axes must be considered.

**ZH:** 严格比较优化器面临两大挑战。首先，不同优化器的超参数不同，必须仔细调节——一个调节不当的 AdamW 可能看起来比调节得当的替代方案更差，反之亦然。其次，需要考虑两个重要的缩放维度：算力（模型规模+数据，假设固定的 Chinchilla 比率）和 Chinchilla 比率本身（数据/参数比）。一些优化器可能在过参数化条件下（小 Chinchilla 比率）表现更好，而其他优化器可能在数据丰富时（大 Chinchilla 比率）表现出色。在评估 Muon 时，一些研究发现其相对于 AdamW 的优势在算力维度上随规模递减，而其他研究则发现其在不同的 Chinchilla 比率下表现一致。两个维度都必须考虑。

### 6.4 The Difficulty of Scaling Experiments / 缩放实验的困难

**EN:** Establishing scaling trends for new optimizers or algorithms is nontrivial and can be deceptive. Even good-looking scaling trends over several orders of magnitude can suddenly deviate and blow up. In one open-source training project involving AdamC, seemingly clean Chinchilla-style scaling curves looked excellent up to a certain compute point—and then dramatically deteriorated. The fix involved switching to careful μP-style parameterizations. The cautionary tale is that scaling experiments frequently result in messy, inconclusive plots, and one should not assume linearity will persist indefinitely.

**ZH:** 为新优化器或算法建立缩放趋势并非易事，且可能具有欺骗性。即使多个数量级上看起来不错的缩放趋势，也可能突然偏离并崩溃。在一个涉及 AdamC 的开源训练项目中，看似干净的 Chinchilla 式缩放曲线在达到某个算力点之前表现优秀——然后急剧恶化。修复方法涉及切换到谨慎的 μP 式参数化。这个警示故事说明，缩放实验经常导致混乱、不确定的图，不应假设线性关系会无限延续。

---

## 7. μP: Conceptual Foundations and Derivation / μP：概念基础与推导

### 7.1 Goal and Motivation / 目标与动机

**EN:** The fundamental goal of μP is straightforward: when you increase the width of your model, the optimal learning rate should not shift. The knobs you are allowed to adjust to achieve this are per-layer initializations, per-parameter learning rates, and sometimes scaling factors on residual connections. μP has been validated at scale by Cerebras GPT, MiniCPM, and others. Cerebras found that μP-parameterized scaling law fits were more stable and more accurately predicted the loss of large models compared to standard parameterizations, which fluctuated more wildly.

**ZH:** μP 的基本目标很简单：当你增加模型的宽度时，最优学习率不应变化。为实现这一目标，你可以调节的旋钮包括：逐层初始化、逐参数学习率，有时还包括残差连接的缩放因子。μP 已在 Cerebras GPT、MiniCPM 等模型的大规模训练中得到验证。Cerebras 发现，μP 参数化的缩放定律拟合更加稳定，比标准参数化更准确地预测了大模型的损失——后者的预测波动更大。

### 7.2 The Two Core Invariants / 两个核心不变量

**EN:** The μP framework rests on two assertions about what should happen as you take the large-width limit of a neural network. First, at initialization, activations should remain roughly the same scale (O(1) per unit) regardless of network width—they should neither blow up with width nor shrink to zero. Second, after one gradient step, the change in activations should also be O(1) per unit, a property called feature learning. This means the network actually learns meaningful features at every scale, as opposed to the neural tangent kernel regime where changes vanish with width.

**ZH:** μP 框架建立在关于神经网络在宽极限下应如何表现的两个断言之上。第一，在初始化时，激活值应大致保持相同的尺度（每单元 O(1)），不随网络宽度而变化——既不应随宽度爆炸，也不应收缩到零。第二，经过一步梯度更新后，激活值的变化也应为每单元 O(1)，这一属性被称为特征学习。这意味着网络在每个尺度上都能真正学习有意义的特征，这与神经正切核（NTK）理论形成对比，后者中激活值的变化随宽度消失。

**EN:** From these two simple and intuitively reasonable invariants, a series of mathematical consequences follow. Let each activation be O(1), so the norm of an entire activation vector is proportional to the square root of the number of hidden units in that layer. Starting from this assumption, you can derive what the initialization variance and learning rate scalings must be at each layer to satisfy both invariants simultaneously.

**ZH:** 从这两个简单且在直觉上合理的假设出发，会推导出一系列数学后果。设每个激活值为 O(1)，则整个激活向量的范数与层中隐藏单元数的平方根成正比。从这一假设出发，你可以推导出每层的初始化方差和学习率缩放必须满足什么条件，才能同时满足这两个不变量。

### 7.3 Initialization Derivation / 初始化推导

**EN:** Consider a deep linear network where each weight matrix is initialized with Gaussian noise scaled by σ². The operator norm of a random Gaussian matrix, by standard concentration arguments, is approximately σ times (√(fan_in) + √(fan_out)). In certain regimes, the layer output norm is approximately the product of the input norm and the operator norm. By induction, if we want activations at each layer to have norm proportional to √(n_l), we set σ to be 1/√(fan_in). Plugging this choice back through the induction verifies that the activation norms remain correctly scaled across all layers.

**ZH:** 考虑一个深度线性网络，其中每个权重矩阵初始化为按 σ² 缩放的高斯噪声。根据标准的集中不等式，随机高斯矩阵的算子范数约为 σ 乘以（√(fan_in) + √(fan_out)）。在某些条件下，层的输出范数约为输入范数与该层算子范数的乘积。通过归纳法，如果我们希望每层的激活范数与 √(n_l) 乘以一个常数的比例成正比，我们设 σ = 1/√(fan_in)。将此选择代入归纳过程即可验证，所有层的激活范数确实保持了正确的缩放。

**EN:** For the standard μP initialization (as opposed to standard parameterization), there is an additional factor of √(fan_out/fan_in). When fan_in equals fan_out, this reduces to the usual initialization. When they differ, the μP initialization corrects for the asymmetry. This already differs from the standard PyTorch initialization and represents the first key scaling adjustment.

**ZH:** 对于标准的 μP 初始化（而非标准参数化），还有一个额外的 √(fan_out/fan_in) 因子。当 fan_in 等于 fan_out 时，这退化为通常的初始化。当二者不同时，μP 初始化会修正这种不对称性。这已经不同于标准的 PyTorch 初始化，代表了第一个关键的缩放调整。

### 7.4 Learning Rate Derivation / 学习率推导

**EN:** The derivation for learning rates is more involved and applies to the case of SGD on a single example with a deep linear network. The weight update at layer L is a rank-1 outer product between the gradient with respect to the loss and the activations at the previous layer. The change in activations at layer L has two components: one from the change in activations at the previous layer (propagated through the current weights), and one directly caused by the change in the current layer's weights. All three terms must have the same order of magnitude, and that magnitude must be proportional to √(n_l).

**ZH:** 学习率的推导更复杂，适用于在单一样本和深度线性网络上进行 SGD 的情形。第 L 层的权重更新是关于损失的梯度与前一层的激活值之间的秩-1 外积。第 L 层激活值的变化有两个分量：一个来自前一层激活值的变化（通过当前权重传播），另一个直接由当前层权重的变化引起。所有三个分量必须具有相同的量级，且该量级必须与 √(n_l) 成正比。

**EN:** To solve for the required learning rate, we make the additional assumption that the loss change per step is roughly O(1)—the model makes appreciable progress regardless of scale. Using a Taylor approximation and the rank-1 structure of the update, we can show that the required per-layer learning rate must scale as fan_out/fan_in for SGD. For AdamW, the structure differs because Adam's normalization changes the scaling, resulting in a 1/fan_in scaling instead. This is why μP typically prescribes layer-specific learning rates: layers with larger fan_in get smaller learning rates under Adam.

**ZH:** 为求解所需的学习率，我们额外假设每步损失变化大致为 O(1)——无论规模如何，模型都有可感知的进步。利用泰勒近似和更新的秩-1 结构，我们可以证明，对于 SGD，所需的逐层学习率必须按 fan_out/fan_in 缩放。对于 AdamW，由于 Adam 的归一化改变了缩放结构，其结果是 1/fan_in 的缩放。这就是 μP 通常规定逐层特定学习率的原因：在 Adam 下，fan_in 较大的层获得较小的学习率。

### 7.5 μP in Practice and Stress Tests / μP 在实践中的表现与压力测试

**EN:** When μP is implemented correctly, the learning rate optimality can be very clean, as shown by independent replication studies. Learning rates for different parameter groups (embeddings, attention, MLP, softmax) are assigned different scaling rules under μP. However, there are real-world complications. Technically, SwiGLU activations, initialization variations, and RMS norm are outside the μP theoretical framework, though in practice they mostly work. More concerning failures arise with learned gain terms in RMS norm (which break μP), exotic optimizers like Lion (which use sign-based gradients), and large decoupled weight decay (a significant stress test that μP does fail).

**ZH:** 当 μP 正确实施时，学习率的最优性可以非常干净，独立复现研究也证实了这点。在 μP 下，不同参数组（嵌入、注意力、MLP、softmax）的学习率被赋予不同的缩放规则。然而，现实世界存在复杂因素。从技术上讲，SwiGLU 激活函数、初始化变体和 RMS norm 都不在 μP 的理论框架内，尽管在实践中它们大多可行。更令人担忧的失效出现在：RMS norm 中可学习的增益项（会破坏 μP）、Lion 等特殊优化器（使用基于符号的梯度）、以及大的解耦权重衰减（这是一个 μP 确实未能通过的重大压力测试）。

**EN:** Despite these limitations, μP remains a useful tool for controlling hyperparameter drift as a function of scale. It is not a settled problem and not the single right answer for all situations, but there is promise in the μP-style initialization program. It sits alongside the scaling-law-fitting approach as one of several valid strategies for managing hyperparameters at scale.

**ZH:** 尽管存在这些局限性，μP 仍然是按规模控制超参数漂移的有用工具。这不是一个已经解决的问题，也并非适用于所有情况的唯一正确答案，但 μP 式初始化方案是有前景的。它与缩放定律拟合方法并列，是管理规模超参数的若干有效策略之一。

---

## 8. Conclusion / 总结

**EN:** Scaling in the wild is tricky. The initial presentation of scaling laws makes them sound like a science: draw lines, run procedures, and you will know what happens at scale. In reality, it is far messier. People use scaling laws in practice for many things—picking architectures, selecting optimizers, tuning hyperparameters—but there is a genuine art to knowing whether a trend will truly extrapolate. You can use μP to stabilize learning rates, you can search for the optimal learning rate and batch size, and you can fit scaling laws to predict the optimum. All of these are ways of controlling hyperparameter drift. But there is no silver bullet yet. Maybe next year there will be—but not quite yet.

**ZH:** 现实世界中的缩放是非常棘手的。缩放定律最初给人的印象是精确科学：画几条线，运行一些流程，你就能知道大尺度下会发生什么。但实际情况要混乱得多。在实践中，人们用缩放定律做很多事——选择架构、挑选优化器、调节超参数——但判断某种趋势是否真正可外推，这其中确实存在无法量化的技艺成分。你可以用 μP 来稳定学习率，可以搜索最优学习率和批大小，也可以拟合缩放定律来预测最优值。所有这些都是控制超参数漂移的方法。但目前还没有银弹。也许明年会有——但现在还没有。

**EN:** The key takeaways from this lecture are: (1) μP is a useful reparameterization trick to make learning rates scale-invariant; (2) WSD learning rate schedules are a versatile and widely-used alternative to cosine decay; (3) fitting scaling laws to hyperparameters (DeepSeek approach) is an alternative to achieving invariance; (4) the muon optimizer is a matrix-aware algorithm now validated at scale by Kimi K2; (5) when evaluating optimizers or other scale-dependent algorithms, always consider both the compute axis and the Chinchilla ratio axis; and (6) scaling experiments are hard and often deceptive—be humble about extrapolation.

**ZH:** 本讲的关键收获是：(1) μP 是一种有用的重参数化技巧，可使学习率与规模无关；(2) WSD 学习率调度是余弦衰减的一种灵活且广泛使用的替代方案；(3) 为超参数拟合缩放定律（DeepSeek 方法）是实现尺度不变性的另一种方式；(4) Muon 优化器是一种矩阵感知的算法，现已通过 Kimi K2 在大规模上得到验证；(5) 在评估优化器或其他规模依赖算法时，始终要同时考虑算力维度和 Chinchilla 比率维度；(6) 缩放实验非常困难且常具欺骗性——对任何外推保持谦逊。
