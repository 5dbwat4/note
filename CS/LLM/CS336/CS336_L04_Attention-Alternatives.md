# Lecture 4: Attention Alternatives and Mixture of Experts / 第四讲：注意力替代方案与混合专家

## 1. Introduction / 引言

**EN** Today we're going to talk about what I think of as more advanced architecture ideas. Last lecture was really about the basic transformer and how we might tweak different parts of the basic transformer to get to a modern language model. Now I want to talk about things that are much more complex developments on top of the usual transformer. The first topic is attention alternatives—ways of going to much longer contexts using architectural changes that generally allow for linear time dependence on the length of the sequence rather than quadratic. The second topic is mixture of experts. So the first part is modifying the attention block, and the second part is going to be modifying the MLP part. Mixture of experts will give us significantly better utilization in terms of our hardware—more parameters relative to the compute that we have to spend on these models.

**ZH** 今天我们要讨论我认为更加先进的架构想法。上一讲主要讲的是基础 Transformer 以及如何调整它的各个部分来得到现代的 language model。现在我想讨论的是在通常的 Transformer 之上更复杂的发展。第一个主题是注意力替代方案（attention alternatives）——通过架构上的改变来支持更长的上下文（long context），这些改变通常使得对序列长度的依赖变成线性时间而非二次的（quadratic）。第二个主题是混合专家（mixture of experts，MoE）。所以第一部分是修改 attention 模块，第二部分是修改 MLP 部分。混合专家将在硬件利用率方面给我们带来显著提升——以相同的计算量获得更多的参数。

---

## 2. The Need for Longer Context / 对更长上下文的需求

**EN** It's clear now that people want longer context length. You want to pack a lot of things into the context so that your model has more knowledge—maybe it's an agent that operates on lots of things. If you look at different models over time, there's really a clear rush by a lot of the top LLM vendors to provide larger and larger context sizes. The right plot also shows the ratio between how much compute cost is spent in the feed-forward part versus the attention part as you increase the sequence length. Feed-forward grows linearly, but attention is an all-to-all connection between all positions, so it's quadratic and quickly outpaces feed-forward as the sequence length grows. As you go to these longer sequence lengths, attention increasingly becomes more and more of a problem.

**ZH** 现在很明显，人们想要更长的上下文长度。你想把很多东西塞进上下文（context），这样你的模型就有更多的知识——也许它是一个 Agent，需要处理大量内容。如果你看不同模型随时间的变化，很多顶尖 LLM 厂商确实在竞相提供越来越大的上下文窗口大小。右边的图还展示了随着序列长度增加，feed-forward 部分与 attention 部分在计算成本上的比例变化。Feed-forward 是线性增长的，但 attention 是所有位置之间的全连接，是二次的（quadratic），随着序列长度增长会迅速超过 feed-forward。当你走向更长的序列长度时，attention 越来越成为一个问题。

---

## 3. Basic Toolkit for Controlling Attention Costs / 控制注意力成本的基本工具

**EN** What's the basic toolkit by which we can control these costs? We can take things like local attention and combine them in different kinds of hybrid ways to control the very high cost of global attention. If you're only doing global attention once every eight layers, and all the other ones are very local attentions, you've very much controlled the cost. The other thing you can do is systems engineering. A very underappreciated fact is that constant factors really, really matter. Part of the theme of this course is that you need to pay attention to the details. One of the biggest things that has happened to context and attention cost is FlashAttention. FlashAttention is just a very clever way of rearranging the attention operation into a much more systems-friendly way to minimize memory transfer overhead. By doing so, you can get truly dramatic improvements in the performance of your attention. This doesn't fix any of the quadratic cost issues, but constant factors are very, very powerful.

**ZH** 控制这些成本的基本工具是什么？我们可以利用局部注意力（local attention），并以各种混合（hybrid）方式组合它们，来控制全局注意力非常高的成本。如果你每八层才做一次全局注意力，其余都是非常局部的注意力，你就很好地控制了成本。另一个可以做的事情是系统工程。一个被严重低估的事实是，常数因子真的非常非常重要。这门课的主题之一就是你需要关注细节。关于上下文和注意力成本，最重要的发展之一是 FlashAttention。FlashAttention 只是一种非常巧妙的方式，将注意力操作重新排列成对系统更友好的形式，以最小化内存传输开销。通过这样做，你可以在注意力性能上获得真正巨大的提升。这并没有修复任何二次成本的问题，但常数因子是非常非常强大的。

---

**EN** However, if we're going to 5 or 10 million tokens, these tricks might not be enough. We want much more radical, much larger gains in our ability to handle long context. This leads us to the question: is there a way for us to have linear time or linear dependence on the length of the sequence? And what would those kinds of things look like?

**ZH** 然而，如果我们要处理 500 万到 1000 万个 token，这些技巧可能还不够。我们希望在处理长上下文方面获得更根本、更大的收益。这就引出了一个问题：有没有办法让我们对序列长度的依赖变成线性时间？那些方法会是什么样子？

---

## 4. Linear Attention and the Associativity of Multiplication / 线性注意力与乘法结合律

**EN** It turns out that a lot of people have tried many different things over the years. There were a few false starts, but in the last two-ish years, there's been an emergence of a set of recipes that are fairly effective in linear time attention and are now battle-tested at scale. To really explain all of these different methods that work well, you need to understand one core idea: the associativity of multiplication. Let's think about how attention works. We take Qs and Ks and have an all-to-all interaction—all n positions interact with each other by matrix multiplication. Then we normalize through softmax and multiply with values V. Now, for the moment, let's forget that attention has a softmax. If the softmax were the identity, we can just move the parentheses around: instead of computing (QK^T)V, we compute Q(K^T V). This reordering changes which part is quadratic. Instead of having n² terms, we now have dependence on n·d_v·d_k. These hidden dimensions are usually on the order of thousands or tens of thousands—no one has a million coordinates in their hidden dimensions. So this is a much more favorable term to be dependent on compared to the n² term.

**ZH** 事实证明，多年来很多人尝试了许多不同的方法。有一些错误的开始，但在最近大约两年里，出现了一组在线性注意力（linear attention）方面相当有效的方案，现在已经在大规模上经过了实战检验。要解释这些不同的有效方法，你只需要理解一个核心思想：乘法结合律（associativity of multiplication）。让我们想想注意力是如何工作的。我们取 Q 和 K，进行全对全的交互——所有 n 个位置通过矩阵乘法彼此交互。然后通过 softmax 归一化，再与值 V 相乘。现在，暂时让我们忘记注意力中有 softmax。如果 softmax 是恒等函数，我们可以移动括号：与其计算 (QK^T)V，不如计算 Q(K^T V)。这种重排改变了哪个部分是二次的。不再有 n² 项，我们现在依赖的是 n·d_v·d_k。这些隐藏维度通常在几千或几万的数量级——没有人的隐藏维度有一百万个坐标。所以与 n² 项相比，这是一个更有利的依赖项。

---

**EN** The other thing we can do now is that this matrix multiply on the right looks just like an RNN. Instead of writing it in dense form, we can write it incrementally: as we sweep left to right on our context, we multiply Ks and Vs and update a state S, adding it to our previous state. This dense operation and this RNN form are equivalent. What's nice about RNNs? At inference time, we have this state S which is fixed in size, and we just carry it forward. RNNs are very nice for inference reasons, but not for training. The nice thing about linear attention is you can use them in either way—dense form for training (parallel), or serial form like an RNN for inference. So you get the best of both worlds.

**ZH** 我们还可以做的另一件事是，右边的这个矩阵乘法看起来就像一个 RNN。我们可以写成增量形式，而不是密集形式：当我们从左到右扫描上下文时，我们乘上 K 和 V，更新一个状态 S，并将它加到之前的状态上。这种密集操作和这种 RNN 形式是等价的。RNN 好在哪？在推理（inference）时，我们有一个固定大小的状态 S，就带着它向前传递。RNN 在推理方面很好，但在训练方面不好。线性注意力的好处在于你可以用两种方式：用于训练的密集（并行）形式，或用于推理的类似 RNN 的串行形式。所以你得到了两全其美。

---

**EN** Unfortunately, this is linear attention, which is not very good on its own—this is really the starting point of our discussion. There have been people that have basically used this linear attention as part of their attention mechanism. For example, Minimax M1, a fairly large-scale, fairly high-performance Chinese open model, uses a 7-to-1 hybrid—seven linear attention layers plus one full softmax attention. Performance is generally strong and fairly competitive with models like OpenAI's O3 or DeepSeek-R1. No one has really proven out fully linear time attention mechanisms at scale—everything that I'm going to talk about is a hybrid.

**ZH** 不幸的是，这仅仅是线性注意力，本身并不是很好——这真正只是我们讨论的起点。有人已经将这种线性注意力用作其注意力机制的一部分。例如 Minimax M1，一个相当大规模、性能相当不错的中国开源模型，使用了 7:1 的混合——七层线性注意力加上一层完整的 softmax 注意力。性能总体强劲，与 OpenAI 的 O3 或 DeepSeek-R1 等强模型相当有竞争力。还没有人真正在大规模上证明纯线性时间的注意力机制——我要讲的所有内容都是混合架构（hybrid architecture）。

---

## 5. From Linear Attention to Mamba-2 / 从线性注意力到 Mamba-2

**EN** You might say that linear attention is too naive and simple. What you can do is add a small elaboration to linear attention in order to get more expressive updates, and this is how you end up getting Mamba-2. Mamba, Mamba-2, and now Mamba-3 are a family of state space models (SSMs) by Albert Gu, Tri Dao, and friends. They're derived originally from state space theory, but actually, if you look at the mechanics, you can see it as a very simple elaboration of the linear attention mechanism. The idea is: we start with linear attention, and the main problem is that we're always passing our state forward. We know from LSTMs that it's important to decide when to pass information forward and when to forget things. So we add a gate, gamma(t), which depends only on the current input x(t), not on the state. This gate modulates how much of the state we carry forward. Because gamma is not state-dependent, it's very simple to compute, and the duality still holds—you can compute Mamba-2 either as a big dense matrix multiply or use it in recurrent form at inference time.

**ZH** 你可能会说线性注意力太天真、太简单了。你可以在线性注意力上做一个小的扩展来获得更具表达力的更新，这就是你得到 Mamba-2 的方式。Mamba、Mamba-2 以及现在的 Mamba-3 是由 Albert Gu、Tri Dao 等人提出的一系列状态空间模型（state space models，SSM）。它们最初源自状态空间理论，但实际上，如果你看其机制，你可以把它看作是对线性注意力机制的一个非常简单的扩展。思路是这样的：我们从线性注意力开始，主要问题是我们总是把状态往前传。我们从 LSTM 的时代就知道，决定什么时候传递信息、什么时候遗忘信息很重要。所以我们要添加一个门（gating）gamma(t)。gamma(t) 只依赖于当前输入 x(t)，不依赖于状态。这个门控制着我们向前传递多少状态。因为 gamma 不依赖于状态，计算非常简单，而且二元性仍然成立——你可以用大的密集矩阵乘法来计算 Mamba-2，也可以在推理时使用循环（recurrent）形式。

---

**EN** People have now used this at scale. Nemotron-3 uses the idea of combining Mamba-2 as their lightweight layer, with big softmax attention every now and then, alternating in various ways to manage the inference cost vs. expressiveness trade-off. Nemotron-3 achieves pretty good performance compared to Qwen3 thinking and GPT OSS. Because of all these Mamba-2 layers, it has pretty good throughput at fairly large context lengths.

**ZH** 人们已经在大规模上使用了这个方案。Nemotron-3 采用了将 Mamba-2 作为轻量层结合偶尔使用大 softmax 注意力的方式，以各种方式交替来管理推理成本与表达力的权衡。与 Qwen3 thinking 和 GPT OSS 相比，Nemotron-3 取得了相当不错的性能。由于这些 Mamba-2 层，它在相当长的上下文长度下具有很好的吞吐量。

---

## 6. Gated DeltaNet / Gated DeltaNet

**EN** Can we keep pushing this idea further and making the recurrence increasingly more complex? The rule of thumb is: as long as your RNN terms depend only on the input (no state dependence), you will still have the nice duality between parallel operations for training and serial operations for inference. Gated DeltaNet is probably among the most widely used state space models now. It has been tested in quite a few papers, and there's a very nice large-scale scale-up in Qwen 3.5.

**ZH** 我们能继续推进这个想法，让循环越来越复杂吗？经验法则是：只要你 RNN 中的各项只依赖于输入（没有状态依赖），你就仍然拥有训练用的并行操作和推理用的串行操作之间的良好二元性。Gated DeltaNet 可能是目前使用最广泛的状态空间模型之一。它已经在不少论文中得到了测试，在 Qwen 3.5 中有非常不错的大规模扩展。

---

**EN** So what is Gated DeltaNet in comparison to Mamba-2? Mamba-2 takes the linear recurrence (state update) and gates it with gamma. Gated DeltaNet adds a second gate, beta(t). If beta(t) is 0, that means don't take any of my current information—don't add it into my state. This is very reminiscent of LSTM ideas: you have gates that control whether to forget and whether to put in information from the current time step. The other interesting thing about Gated DeltaNet is the update direction. Instead of just gating things, what they do is try to project out the current key direction. The intuition is: when writing in information from the current key k(t), you not only want to put in new information, but also erase any previous keys that have gone into the state. That's why there's this term (I - beta_t * k_t * k_t^T), which acts as a projector that projects out things in the k_t dimension.

**ZH** 那么 Gated DeltaNet 与 Mamba-2 相比如何呢？Mamba-2 取线性循环（状态更新），用 gamma 进行门控（gating）。Gated DeltaNet 添加了第二个门 beta(t)。如果 beta(t) 为 0，就意味着不接收任何当前信息——不将其添加到状态中。这非常让人联想到 LSTM 的思想：你有门来控制是否遗忘，以及是否放入当前时间步的信息。Gated DeltaNet 另一个有趣的地方是更新方向。他们不仅仅做门控，而是尝试投影出（project out）当前的 key 方向。直觉是：当从当前的 key k(t) 写入信息时，你不仅想放入新信息，还想擦除之前已经进入状态的所有 key。这就是为什么有 (I - beta_t * k_t * k_t^T) 这一项，它作为一个投影器来投影掉 k_t 维度上的东西。

---

**EN** Qwen 3.5 and the Qwen Next models use exactly this architecture—a 3-to-1 gated delta net attention hybrid. They have very reasonable performance and strong inference characteristics. Qwen Next has much higher decoding throughput relative to Qwen 3 as the context length goes up. This hybrid architecture doesn't seem to hurt performance very much at all.

**ZH** Qwen 3.5 和 Qwen Next 模型使用的正是这种架构——3:1 的 Gated DeltaNet 注意力混合。它们具有非常合理的性能和强大的推理特性。随着上下文长度的增加，Qwen Next 的解码吞吐量远高于 Qwen 3。这种混合架构似乎对性能几乎没有负面影响。

---

## 7. Controlled Studies of Hybrid Architectures / 混合架构的受控研究

**EN** There haven't been that many great controlled studies of how hybrid architectures perform. One study by ByteDance Seed and UC Santa Cruz compared Mamba-2, Gated DeltaNet, and other architectures as a function of how many hybrid layers you have. The dashed line shows full attention performance. As you go from left to right, increasing the number of non-full attention layers (RNN layers), you see performance degradation. But for some of the best architectures—the yellow, orange, and blue (Gated DeltaNet and variants)—at low ratios there's basically no hit. Once you pass a certain point, you start to see more significant degradation in long context performance. At the end, as you go to full RNN, you have very noticeable performance degradation in all these architectures. If you look at QA performance, the same story holds: as we increase the hybrid ratio, we see decreases in performance, ending up at this pure RNN point.

**ZH** 关于混合架构表现如何，还没有太多很好的受控研究。ByteDance Seed 和 UC Santa Cruz 的一项研究比较了 Mamba-2、Gated DeltaNet 和其他架构在不同混合层数量下的表现。虚线表示纯注意力（full attention）的性能。从左到右，随着非全注意力层（RNN 层）数量的增加，你会看到性能下降。但对于一些最好的架构——黄色、橙色和蓝色（Gated DeltaNet 及其变体）——在低比例下基本没有损失。一旦超过某个阈值，你就会在长上下文性能上看到更显著的下降。最终，当你走向完全的 RNN 时，所有这些架构都有非常明显的性能下降。如果你看 QA 性能，情况是一样的：随着我们增加混合比例，性能稳步下降，最终在纯 RNN 点上结束。

---

**EN** It's important to note that by "recurrent" here we mean any recurrent formulation like Gated DeltaNet, which is not equivalent to full softmax attention. The first step is lossy—we drop the softmax and become linear. That's the very first step of any of these. After that, the linear form to the recurrent form equivalence is exact, but the loss relative to full attention has already occurred.

**ZH** 需要注意的是，这里的"循环"（recurrent）指的是任何循环形式，比如 Gated DeltaNet，它与完整的 softmax 注意力并不等价。第一步就是有损的——我们去掉了 softmax，变成了线性的。这是所有这些方法的第一步。在那之后，线性形式到循环形式的等价是精确的，但相对于完整注意力的损失已经发生了。

---

## 8. DeepSeek Sparse Attention (DSA) / DeepSeek 稀疏注意力

**EN** There's another alternative to attention optimization. In DeepSeek v3.2, they had DSA (DeepSeek Sparse Attention). Instead of computing attention over all tokens, you first have a lightweight indexer that subsets a bunch of tokens. The indexer picks out some subset much smaller than the full sequence, and then you do full attention on that smaller subset. In the forward pass, you have normal Qs and Ks, but then you pass them through this indexer. The indexer takes the QK inner products, applies a ReLU, derives weights from preceding tokens, and then takes a top-k to select which positions get included in the attention computation. Then you do your usual attention computation on that subset.

**ZH** 还有另一种注意力优化方案。在 DeepSeek v3.2 中，他们提出了 DSA（DeepSeek 稀疏注意力，DeepSeek Sparse Attention）。不是对所有 token 计算注意力，而是首先用一个轻量级的索引器（indexer）来选取一部分 token。索引器选出比完整序列小得多的一个子集，然后你在这个较小子集上做完整的注意力。在前向传播中，你有正常的 Q 和 K，但将它们通过这个索引器。索引器取 QK 内积，应用 ReLU，从前面的 token 中导出权重，然后通过 top-k 来决定哪些位置被包含在注意力计算中。然后你在那个子集上做通常的注意力计算。

---

**EN** The nice thing about this is it's very, very sparse. If the indexer is lightweight, the full attention can be done on a very small subset. Another thing both DSA and GLM show is that you don't actually have to train the model with this—you just train a normal transformer, and during your long context extension stage, you drop in this lightweight indexer and train the model to handle it. DeepSeek v3.2 matches other frontier models like Claude 4.5 Sonnet or Gemini 3. Both prefill and decoding show favorable scaling compared to the previous generation of DeepSeek models that did not use sparse attention. GLM5, one of the best open models available, also adopted this DSA approach, and their ablations show you don't lose much in performance relative to full attention, even at long context retrieval tasks.

**ZH** 这样做的好处是非常非常稀疏。如果索引器很轻量，那么完整的注意力可以在非常小的子集上完成。DSA 和 GLM 都展示的另一点是，你实际上不需要用这个来训练模型——你只需训练一个普通的 Transformer，然后在长上下文扩展阶段，插入这个轻量级索引器，并训练模型来处理它。DeepSeek v3.2 与当时的其他前沿模型如 Claude 4.5 Sonnet 或 Gemini 3 相当。预填充（prefill）和解码（decode）都显示出相比前一代不使用稀疏注意力的 DeepSeek 模型更有利的扩展特性。GLM5 是目前最好的开源模型之一，也采用了这种 DSA 方法，他们的消融实验表明，即使对于 RNN 风格架构很难处理的长上下文检索任务，与完整注意力相比，性能损失也很小。

---

**EN** Note that DSA is not linear time. The indexer still has to operate on full all-to-all attention because the QK inner products are not linear in cost. But you can make the indexer much cheaper—by making it lower dimensional, using lower precision, or making the projection weights very small. Then the full attention afterwards is quadratic but on a much shorter context length because it's top-k. So this is expensive but small. Sometimes the constant factors are really, really important, and you shouldn't get too stuck on the quadratic versus linear question.

**ZH** 注意，DSA 不是线性时间的。索引器仍然需要对全序列做全对全注意力，因为 QK 内积在成本上不是线性的。但你可以让索引器便宜得多——比如降维、降低精度，或使投影权重非常小。然后后续的完整注意力虽然是二次的，但是是在一个短得多的上下文中，因为是 top-k。所以这部分是昂贵的但很小的。有时候常数因子真的非常重要，你不应该过于纠结二次还是线性的问题。

---

## 9. Mixture of Experts: Introduction / 混合专家：引言

**EN** Now let's talk about mixture of experts (MoE). Conceptually, MoEs don't really change the game—one way of thinking about them is that they are just a more efficient MLP. But you need to understand what MoEs are for two reasons. First, everyone is shipping MoEs these days, and you should understand what it is if you want to deeply understand language models. Second, MoEs have really interesting mechanical components—if you look at how MoEs are built and what primitives they use, you'll quickly see MoE-like primitives in many places. There's a broader reason why MoEs are interesting and you should learn about them.

**ZH** 现在让我们来谈谈混合专家（mixture of experts，MoE）。从概念上讲，MoE 并没有真正改变游戏规则——一种理解方式是，它们只是一种更高效的 MLP。但你需要了解 MoE 是什么，原因有两个。第一，如今每个人都在发布 MoE 模型，如果你想深入理解 language model，你应该了解它。第二，MoE 有非常有趣的机械组件——如果你看 MoE 是如何构建的以及它们使用什么原语，你很快就会在许多地方看到类似 MoE 的原语。所以有一个更广泛的原因说明为什么 MoE 有趣且值得学习。

---

**EN** So what is an MoE? MoEs are very simple things in some ways—they're just replacements of your MLP. On the left is your usual MLP for a transformer: you've got attention, normalization, and then a feed-forward right after. Now, instead, take your big FFN and cut it up into smaller FFNs—or rather, keep them the same size as your original FFN and somehow have a system that tells you which FFN to pick for every input. Now you have 4x the parameters for your FFN, but on any forward or backward pass, you only pay one FFN worth of cost. The original motivation for MoEs is very parameter-centric: you wanted more parameters because you believe more parameters are good, but you don't want to pay the cost for more parameters.

**ZH** 那么什么是 MoE？MoE 在某些方面非常简单——它们只是 MLP 的替代品。左边是 Transformer 中通常的 MLP：你有 attention、归一化，然后紧接着是 feed-forward。现在，取而代之，把你的大 FFN 切成较小的 FFN——或者更准确地说，保持它们和原来的 FFN 一样大，并通过某种系统告诉你为每个输入选择哪个 FFN。现在你的 FFN 有 4 倍的参数，但在任何前向或反向传播中，你只需要支付相当于一个 FFN 的成本。MoE 最初的动机是非常以参数为中心的：你想要更多的参数，因为你相信更多参数是好的，但你不想为更多参数支付成本。

---

## 10. Why MoEs Are So Popular / 为什么 MoE 如此流行

**EN** Every model you get on Hugging Face past a certain size seems to be an MoE. The reason is that if you keep the total compute the same but increase the number of sparse parameters, the models are generally getting better. This is evidence that more parameters are in fact generally good, even if only a subset of them are active at a time. In the Fedus et al. 2022 paper on the switch transformer, they show that as you increase the number of experts (keeping active parameters the same), test loss for language modeling just keeps decreasing. On the right, you see that as you increase training compute, if you have more experts for the same amount of training compute, you just get better performance. So for both training and inference, MoEs give you a free win.

**ZH** 你在 Hugging Face 上看到的超过一定规模的所有模型似乎都是 MoE。原因是，如果你保持总计算量不变，但增加稀疏参数的数量，模型通常会变得更好。这证明了更多参数确实通常是好的，即使每次只有一部分处于活跃状态。在 Fedus 等人 2022 年关于 Switch Transformer 的论文中，他们展示了随着专家（expert）数量的增加（活跃参数保持不变），语言建模的测试损失不断下降。在右边，随着训练计算量的增加，如果在相同的训练计算量下拥有更多的专家，你就能得到更好的性能。所以在训练和推理方面，MoE 都给你带来了免费的收益。

---

**EN** The OlMoE paper from AIQ folks shows the same thing—in training loss, validation loss, and downstream benchmark performance, MoEs do much better compared to their dense counterparts. You see something like 2x faster training of a MoE relative to a dense model. And if you look at all the MoEs that got released, they are much stronger than dense models in terms of activated parameters, which is what matters if you care about inference flops. DeepSeek v2 was a big shift from dense models—much fewer active parameters, just as good if not better performance.

**ZH** AIQ 团队的 OlMoE 论文展示了同样的结果——在训练损失、验证损失和下游基准性能方面，MoE 比其密集（dense）模型表现好得多。MoE 的训练速度大约是密集模型的 2 倍。如果你看所有已发布的 MoE，它们在激活参数方面比密集模型强得多，这是你在意推理计算量时最重要的指标。DeepSeek v2 是从密集模型的一个重大转变——活跃参数少得多，性能却一样好甚至更好。

---

**EN** MoEs also give you another axis of parallelization. LLMs are very big and don't fit in single devices, so you want many ways of cutting up your model. Mixture of experts has this additional nice property that your experts within each FFN naturally come in different chunks. Each expert is a natural chunk you can put on a different device and then route the activations to different devices. This is expert parallelism, which is very helpful for optimizing serving. Of course, MoE research and training has been very active in China—Qwen, DeepSeek, and others like MiniCPM did some of the earliest work training and popularizing MoEs, and they continue to do really great work.

**ZH** MoE 还为你提供了另一个并行化的维度。LLM 非常大，无法放入单个设备，所以你希望有很多种切分模型的方式。混合专家还有一个额外的好处，即每个 FFN 中的专家自然地分成不同的块。每个专家是一个自然的块，你可以放在不同的设备上，然后将激活路由到不同的设备。这就是专家并行（expert parallelism），对优化服务非常有帮助。当然，MoE 的研究和训练在中国非常活跃——Qwen、DeepSeek 以及 MiniCPM 等做了最早的一些训练和推广 MoE 的工作，并且继续做着非常出色的工作。

---

## 11. Why MoEs Are Hard / 为什么 MoE 很难

**EN** MoEs caught on pretty slowly. Google was studying and pushing MoEs in 2022, but it's only from 2024 onwards that MoEs really started to catch on. There are a lot of complexities that come from MoEs. The infrastructure is very complex—it's hard to parallelize experts in ways that are efficient in utilization. MoEs have a lot of parameters, so it's hard to fit them on a single device. And during training, MoEs can really blow up on you. During training, MoEs are also sparse—you only have one or k experts active, so you don't know what happened with the rest of them. Despite this, you must somehow learn to route. It's got this RL bandit flavor to the problem, but we're going to solve it with the power of heuristics and deep learning magic.

**ZH** MoE 流行得相当慢。Google 在 2022 年就在研究并推动 MoE，但直到 2024 年之后，MoE 才真正开始流行起来。MoE 带来了很多复杂性。基础设施非常复杂——以高效利用的方式并行化专家是很困难的。MoE 有很多参数，很难将它们放在单个设备上。而且在训练时，MoE 真的可能让你崩溃。在训练期间，MoE 也是稀疏的——你只有一个或 k 个专家活跃，所以你不知道其他专家发生了什么。尽管如此，你必须以某种方式学会路由（routing）。这个问题有强化学习/赌博机（bandit）的味道，但我们不会用强化学习或 bandit 算法来解决它，而是用启发式和深度学习魔法的力量。

---

## 12. MoE Design: Routing Functions / MoE 设计：路由函数

**EN** To design an MoE, there are three axes of variation: the routing function (how tokens are sent to experts), the sizes of the experts (more small experts or fewer large experts), and training (which is really difficult). In all cases, we don't want to activate all the experts—we only want some subset active, so we always choose some TopK. There are different kinds of choices: token choice (the token chooses the expert), expert choice (each expert picks their favorite tokens), or a global router that optimally assigns tokens to experts. Almost all MoEs use token choice TopK—the token chooses k different experts. Token choice has generally been much easier to get working and has been the standard for all the models we see today.

**ZH** 要设计一个 MoE，有三个变化维度：路由函数（tokens 如何被发送到专家）、专家的大小（更多小专家还是更少大专家），以及训练（非常困难）。在所有情况下，我们不想激活所有专家——我们只想激活一部分，所以我们总是选择某种 TopK。有不同种类的选择：标记选择（token choice，token 选择专家），专家选择（expert choice，每个专家选择它们最喜欢的 tokens），或一个全局路由器最优地分配 token 到专家。几乎所有的 MoE 都使用标记选择的 TopK——token 选择 k 个不同的专家。标记选择通常更容易实现，并已成为我们今天看到的所有模型的标准。

---

## 13. TopK Routing / TopK 路由

**EN** There are many ways you can do routing. The most common is a small linear projection: your router computes an inner product, each expert has a vector direction, and the closest in inner product space gets selected. This is used in the classic switch transformer, GShard, Grok, Mixtral, DBRX, DeepSeek, and others. One thing that's always been mysterious is that many papers have shown you don't actually need learned routing—you can just hash your inputs and send them to different FFNs, and this works fine too, though not as well as TopK. You can also use RL to learn the routes, treating the router as a policy—this should be the natural way to think about the problem as a bandit problem, but it introduces a lot of overhead. What people have figured out is that there's a good set of heuristics applied to the simple TopK routing scheme that just works, so there's no reason to do something more complicated.

**ZH** 有很多种路由方式。最常见的是一个小型线性投影：你的路由器（router）计算一个内积，每个专家有一个向量方向，内积空间中最接近的专家被选中。这被用于经典的 Switch Transformer、GShard、Grok、Mixtral、DBRX、DeepSeek 等模型中。一直令人困惑的一件事是，许多论文表明你实际上不需要学习路由——你只需要对你的输入做哈希然后发给不同的 FFN，这也行得通，虽然不如 TopK 好。你也可以用强化学习来学习路由，将路由器视为一种策略——这应该是考虑这个问题（作为一个 bandit 问题）的自然方式，但它引入了大量开销。人们已经发现，将一组好的启发式方法应用于简单的 TopK 路由（TopK routing）方案就能让它有效工作，所以没有理由做更复杂的事。

---

**EN** Finally, you can solve a linear assignment problem to globally compute the optimal assignment from experts to tokens. It's been shown to do good things in some cases but hasn't been seen at scale because it's extremely expensive. TopK routing is basically the consensus routing mechanism. You take your inputs through a feed-forward, compute scores via softmax between experts and inputs, select the TopK of those, and that becomes the gate that controls each expert. The gates are learned by taking the inner product between a weight for each expert and the inputs—very, very lightweight.

**ZH** 最后，你可以解决一个线性分配问题来全局计算从专家到 token 的最优分配。这在某些情况下表现良好，但尚未在大规模上看到，因为它极其昂贵。TopK 路由（TopK routing）基本上是公认的路由机制。你将输入通过一个 feed-forward，通过 experts 和输入之间的 softmax 计算分数，选择其中的 TopK，这成为控制每个专家的门（gate）。门是通过取每个专家的权重与输入之间的内积来学习的——非常非常轻量。

---

## 14. Shared Experts (DeepSeekMoE) / 共享专家（DeepSeekMoE）

**EN** Even within this simple thing, there's been innovation. DeepSeekMoE pioneered the idea of shared experts, which is now very widely used. The idea is that sometimes there is very common processing that you want to apply to all tokens—you want some experts to always be applied and others to be applied conditionally. DeepSeekMoE took the original expert design, cut up the experts into smaller, finer-grained chunks, and made some subset of those fine-grained experts into shared experts that are always on—they bypass the router, always process inputs, and go back into the outputs. This is a nice idea because it turned out that if you had the classic expert design, you were reusing a lot of weights for common modeling, so offloading this into shared experts lets the other experts specialize even more.

**ZH** 即使在这个简单的东西内部，也有创新。DeepSeekMoE 开创了共享专家（shared experts）的想法，现在被广泛使用。想法是，有时候你想对所有的 token 应用一些非常通用的处理——你希望一些专家始终被应用，而另一些有条件地被应用。DeepSeekMoE 采用最初的专家设计，将专家切成更小的细粒度块，并将其中一部分细粒度专家设为始终开启的共享专家——它们绕过路由器，始终处理输入，并回到输出中。这是一个好主意，因为事实证明，如果你使用经典的专家设计，你会为通用建模重复使用大量权重，所以将其卸载到共享专家中，让其他专家能更加专业化。

---

**EN** DeepSeek is really nice because they do careful ablations. They show that as you make experts smaller and finer-grained, and add shared experts, you see significant gains from both interventions. For some tasks like TriviaQA and NaturalQuestions, the shared expert has very significant improvements. OlMoE, the nice Western carefully controlled MoE study, shows that fine-grained many experts are helpful, though they conclude shared experts don't help as much. Many recent MoEs follow essentially the DeepSeek design—Qwen 3.5, GLM, and other modern models continue to see both shared experts and fine-grained experts in widespread use. This has been a very battle-tested design.

**ZH** DeepSeek 非常好的一点是他们做了仔细的消融实验。他们展示了当你让专家更小、更细粒度，并添加共享专家时，这两项干预都带来了显著的收益。对于 TriviaQA 和 NaturalQuestions 等任务，共享专家有非常显著的改进。OlMoE——一项很好的西方精心控制的 MoE 研究——显示细粒度的多专家是有帮助的，尽管他们得出结论共享专家帮助不大。最近的许多 MoE 基本遵循 DeepSeek 的设计——Qwen 3.5、GLM 和其他现代模型继续广泛使用共享专家和细粒度专家。这是一个经过充分实战检验的设计。

---

## 15. Training MoEs: The Core Challenge / 训练 MoE：核心挑战

**EN** Now let's talk about training MoEs, which gets into really surprising and very deep learning things. We don't want to activate all experts during training because we'd pay the full flops cost of all experts. But if we have sparsity, gating decisions are no longer differentiable, and we don't see all the counterfactual experts we could have picked. There are different solutions: RL to optimize gating policies (not super popular), stochastic perturbations (explore/exploit style), or a whole bunch of heuristics that balance out which experts go where. People use option three—a collection of interesting heuristics that end up working.

**ZH** 现在让我们谈谈训练 MoE，这涉及到非常令人惊讶且非常深刻的深度学习内容。我们不想在训练期间激活所有专家，因为那样我们会支付所有专家的全部计算成本。但如果我们有稀疏性（sparse），门控决策就不再可微，而且我们也看不到我们本可以选择的所有反事实专家。有不同的解决方案：用强化学习优化门控策略（不是特别流行），随机扰动（探索/利用风格），或一大堆平衡专家分配的启发式方法。实践中人们使用的是第三种——一组有效的有趣启发式方法。

---

**EN** Some people have shown that you can use RL to learn routers, and it does work, but because of gradient variance and complexity, it's not optimal. Stochastic approximation comes from the earliest MoE papers—instead of making a hard decision during training, you inject some noise dependent on the input scale, so if two experts are closely tied, you stochastically pick one. This perturbation allows tie-breaking and exploration. However, later ablations showed that not doing any stochastic or robustness tricks actually helps with both stability and overall quality of the final trained MoE. This suggests you don't necessarily need the stochastic exploration terms.

**ZH** 有些人已经展示了你可以用强化学习来学习路由器，它确实有效，但由于梯度方差和复杂性，它不是最优的。随机近似来自最早的 MoE 论文——在训练期间不做硬决策，而是注入一些依赖于输入规模的噪声，所以如果两个专家得分非常接近，你会随机选择其中一个。这种扰动允许打破平局和进行探索。然而，后来的消融实验表明，不做任何随机或鲁棒性技巧实际上有助于最终训练好的 MoE 的稳定性和整体质量。这表明你不一定需要随机探索项。

---

## 16. Load Balancing and Expert Collapse / 负载均衡与专家坍缩

**EN** So what actually happens if you just do normal gradient descent? You'll route your TopK experts, the strongest experts get more signal, backprop reinforces that expert, and you get a rich-gets-richer effect where experts that are chosen get very strong weights. Strong weights mean they're selected more often, and they run away taking on everything. This expert collapse or expert starvation phenomenon is a very real problem and the core issue you have to solve with heuristic training of MoEs. So what do you do? You add a heuristic loss to the total modeling loss that balances out the tokens going to different experts.

**ZH** 那么如果你只做普通的梯度下降会发生什么？你会路由你的 TopK 专家，最强的专家获得更多信号，反向传播强化那个专家，你得到富者愈富的效应——被选中的专家获得很强的权重。强权重意味着它们被更频繁地选中，然后它们就 runaway 了，接收一切。这种专家坍缩（expert collapse）或专家饥饿（expert starvation）现象是一个非常现实的问题，也是你必须用启发式训练 MoE 来解决的核心问题。那么你该怎么做？你在总的建模损失上添加一个启发式损失，来平衡分配给不同专家的 token。

---

**EN** The approach used in the switch transformer computes the fraction of tokens dispatched to each expert (F) and the total probability mass of the router allocated to each expert (P), and multiplies them. If you take the derivative with respect to P, you get F—the fraction of tokens allocated. So this acts as a penalty in gradient space: the more tokens you get, the more negative gradient you get, pushing down the probability mass on popular experts proportional to their fraction. That's the action of this loss.

**ZH** Switch Transformer 中使用的方法是计算分配给每个专家的 token 比例（F）以及路由器分配给每个专家的总概率质量（P），然后相乘。如果你对 P 求导，你得到 F——即分配的 token 比例。所以这在梯度空间中充当一个惩罚项：你获得的 token 越多，你得到的负梯度就越大，将热门专家的概率质量按照其比例往下压。这就是这个损失函数的作用。

---

**EN** DeepSeek's approach builds on these ideas. They backprop straight through the experts, ignoring nondifferentiability, but add per-expert balancing identical to the switch transformer. DeepSeek also adds per-device balancing—if your experts are allocated to some devices, you want those devices to be balanced too, so both run at full utilization. If you remove the load balancing loss, the effects are catastrophic. From the OlMoE paper, without load balancing, almost all tokens go to two experts, while with it, all experts are evenly utilized across tokens. Without it, you've thrown away a ton of parameters—those experts are doing absolutely nothing for most of training. This is pretty surprising: you've got this nondifferentiable TopK selection, a pretty complicated object, and all you really need is to add this balancing loss, then treat the rest as if you can just pump gradients through the system, and the model trains very nicely.

**ZH** DeepSeek 的方法建立在这些想法之上。他们直接通过专家进行反向传播，忽略不可微性，但添加了与 Switch Transformer 相同的逐专家均衡。DeepSeek 还添加了逐设备均衡——如果你的专家被分配到某些设备上，你希望这些设备也是均衡的，这样两者都能满负荷运行。如果你去除负载均衡损失，效果是灾难性的。从 OlMoE 的论文中可以看到，没有负载均衡时，几乎所有 token 都流向两个专家，而有了它，所有专家在 token 上被均匀利用。没有它，你就浪费了大量参数——那些专家在大部分训练期间什么也没做。这相当令人惊讶：你有这个不可微的 TopK 选择，一个相当复杂的对象，但你真正需要做的只是添加这个均衡损失，然后把剩下的当作可以通过系统泵送梯度来对待，模型就能非常好地训练。

---

## 17. MoE Systems and Parallelism / MoE 系统与并行化

**EN** Training MoEs introduces additional fun systems dynamics. You can do data parallelism, model parallelism, and combine them, but each has limits. With expert parallelism, you get another additional axis to parallelize on. The underlying implementations allow you to take advantage of sparse matrix multiply built into GPUs. If you have multiple experts on one GPU, you want bigger matrix multiplies to reuse caches rather than many small ones. You can leverage structured sparsity natively supported in hardware to multiply experts and inputs in clean, fast ways. There's this hardware-architecture codesign happening with MoEs.

**ZH** 训练 MoE 引入了额外的有趣系统动态。你可以做数据并行、模型并行，并组合它们，但每种都有极限。有了专家并行，你获得了另一个额外的并行化维度。底层实现允许你利用 GPU 内置的稀疏矩阵乘法。如果你在一个 GPU 上有多个专家，你希望有更大的矩阵乘法以重用缓存，而不是很多小矩阵乘法。你可以利用硬件原生支持的结构化稀疏性（sparse）来以干净、快速的方式将专家和输入相乘。MoE 正在发生这种硬件-架构协同设计。

---

**EN** One recent development from Nemotron-3 addresses the communication overhead of expert parallelism. When shipping activations from device to device, you can take your residual stream and down-project it first, then do the collective communication call with smaller lower-dimensional vectors, significantly saving on communication without the drawbacks of smaller hidden dimensions.

**ZH** Nemotron-3 最近的一项发展解决了专家并行的通信开销问题。当把激活从设备发送到设备时，你可以先对你的残差流进行降维投影，然后用较小的低维向量进行集合通信，从而显著节省通信开销，同时没有减小隐藏维度的缺点。

---

**EN** One final trivia: if you do MoE infrastructure naively, certain experts might be much more popular than others, and the expert queue of tokens starts building up until you have to drop tokens. Earlier MoE inference infrastructure would silently drop the expert and send zero back, causing weird stochasticities where other users' queries could bump you out of the expert queue. But today, megalodon blocks and other common open source MoE frameworks don't have this issue anymore.

**ZH** 最后一个趣闻：如果你天真地构建 MoE 基础设施，某些专家可能比其他专家更受欢迎，专家的 token 队列会不断积累，直到你不得不丢弃 token。早期的 MoE 推理基础设施会默默地丢弃这个专家并返回零，导致奇怪的随机性——其他用户的查询可能会把你从专家队列中挤出来。但如今，megalodon blocks 和其他常见的开源 MoE 框架已不再有这个问题。

---

## 18. MoE Stability Issues / MoE 稳定性问题

**EN** We've already talked about stability issues last lecture—exponentials are bad, divisions are bad, which means softmaxes are danger zones. With mixture of experts, we've introduced yet another softmax in the routing (for TopK). People have long noticed that the softmax operation in MoEs is potentially very dangerous. Barret Zoph and others had an entire paper on MoE stability in the early days of Google MoE design. Solutions include using Float32 for just the expert router and adding z-loss to control softmax stability issues. OlMoE has done ablations showing that z-loss on the router can be quite helpful, as evidenced by very spiky training loss curves without it.

**ZH** 我们上次课已经讨论过稳定性问题——指数是坏的，除法是坏的，这意味着 softmax 是危险区域。对于混合专家，我们在路由中又引入了一个 softmax（用于 TopK）。人们早就注意到 MoE 中的 softmax 操作可能非常危险。Barret Zoph 等人在 Google 早期 MoE 设计时写过一整篇关于 MoE 稳定性的论文。解决方案包括仅对专家路由器使用 Float32，以及添加 z-loss 来控制 softmax 稳定性问题。OlMoE 的消融实验表明，路由器上的 z-loss 非常有帮助，没有它的话，训练损失曲线会出现非常尖锐的波动。

---

**EN** MoEs can also be pretty annoying to fine-tune. They have so many parameters that if you try to fine-tune the experts, you end up with very serious overfitting issues. For dense models, train and validation are fairly close, but for sparse models the train-val gap is extremely large. You could fine-tune non-MoE feed-forwards or just attention—these are common interventions. And of course, the bitter lesson version: maybe you should just use a lot more data and retrain basically the entire MoE during fine-tuning.

**ZH** MoE 在微调时也可能相当讨厌。它们有太多参数，如果你尝试微调专家，会导致非常严重的过拟合问题。对于密集（dense）模型，训练和验证的差距相当接近，但对于稀疏模型，训练-验证差距非常大。你可以微调非 MoE 的 feed-forward 层或只微调 attention——这些都是常见的干预措施。当然，还有"苦涩的教训"版本：也许你应该用更多数据，在微调阶段基本上重新训练整个 MoE。

---

## 19. Upcycling / 上循环（Upcycling）

**EN** Upcycling is the idea that if you want a MoE, you can just take a dense model you've trained and instantiate a MoE based on it. You copy everything including the MLPs, make a bunch of copies from these MLPs, add a router with random initialization, and just train. Because of the stochasticity of which inputs go where, experts start to specialize. In the earliest upcycling papers, they showed that an upcycled method could get much better language modeling performance than continuing to train the same dense model. MiniCPM took their 2.4B model and upcycled it to 13.4B parameter model with almost free wins. Qwen initialized their Qwen 1.5 MoE from their 1.8B model, upcycling to a 2.7B model, getting one of the first high-performance upcycled models. These days, I don't think anyone's really upcycling anymore—you might as well just train your big run on a MoE to start with, but it's important to know this in the action space of MoE models.

**ZH** 上循环（upcycling）是这样一种想法：如果你想要一个 MoE，你可以取一个你训练好的密集（dense）模型，然后在它的基础上实例化一个 MoE。你复制所有内容包括 MLP，从这些 MLP 中做一堆副本，添加一个随机初始化的路由器，然后直接训练。由于输入流向何处的随机性，专家开始专业化。在最早的上循环论文中，他们展示了上循环方法可以获得比继续训练同一密集模型好得多的语言建模性能。MiniCPM 将他们的 2.4B 模型上循环为 13.4B 参数模型，几乎获得了免费的收益。Qwen 从他们的 1.8B 模型初始化 Qwen 1.5 MoE，上循环为 2.7B 模型，得到了最早的高性能上循环模型之一。如今，我不认为还有人真的在这样做——你还不如一开始就用 MoE 训练你的大模型，但了解这个方法在 MoE 模型的操作空间中很重要。

---

## 20. DeepSeek Model Evolution / DeepSeek 模型演化

**EN** Let's walk through the DeepSeek models—v1, v2, and v3—because there's a lot to learn from their evolution. DeepSeekMoE v1 is already the prototype of many different modern MoEs: shared and fine-grained expert structure, standard TopK routing with auxiliary loss balancing. In some ways it's the prototypical platonic ideal of an MoE model. DeepSeekMoE v2 scales this up: two shared experts, many more fine-grained experts, device routing and communication balancing components (both essentially adding auxiliary losses to optimize systems). Successful language model training is not just about deep learning—it's also about really respecting your systems.

**ZH** 让我们走过 DeepSeek 的模型——v1、v2 和 v3——因为从它们的演化中可以学到很多东西。DeepSeekMoE v1 已经是许多不同现代 MoE 的原型：共享和细粒度专家结构，标准的 TopK 路由加辅助损失均衡。在某些方面，它是 MoE 模型的典型柏拉图理想。DeepSeekMoE v2 将其扩展：两个共享专家，更多细粒度专家，设备路由和通信均衡组件（两者本质上都是添加辅助损失来优化系统）。成功的语言模型训练不仅仅是关于深度学习——还关乎真正尊重你的系统。

---

**EN** DeepSeekMoE v3 still has the shared and fine-grained experts design but with different ways of doing balancing and switched to using sigmoid plus softmax for weighting experts. They also have multi-head latent attention (MLA): instead of directly producing Qs, Ks, and Vs, you first produce a lower-dimensional latent c, and then produce Q, K, V as a function of that. This gives significantly improved savings—instead of KV caching all your Ks and Vs, you only need to store these Cs, which are hopefully lower dimensional. The complexity is that this conflicts with RoPE when doing KV caching, so you need to be careful about how you rotate different dimensions.

**ZH** DeepSeekMoE v3 仍然有共享和细粒度专家设计，但有不同的均衡方式，并切换为使用 sigmoid 加 softmax 来加权专家。他们还有多头潜在注意力（multi-head latent attention，MLA）：不是直接产生 Q、K 和 V，而是首先产生一个低维的潜在 c，然后基于此产生 Q、K、V。这带来了显著的节省——不需要对所有 K 和 V 做 KV 缓存，你只需要存储这些 c，而 c 的维度希望更低。复杂性在于当进行 KV 缓存时，这会与 RoPE 冲突，所以你需要小心处理如何旋转不同的维度。

---

**EN** Finally, a very cool idea from DeepSeekMoE v3 that hasn't caught on much is multi-token prediction (MTP). Instead of predicting one future token, you predict multiple tokens all at once. There are statistical arguments for why this is a good idea—maybe it lets you predict the future a little better. But there's also a nice systems argument: you now have a speculative decoder built in, which is a trick you can use to speed up decoding from your model.

**ZH** 最后，DeepSeekMoE v3 中一个非常酷但尚未广泛流行的想法是多 token 预测（multi-token prediction，MTP）。不是预测一个未来的 token，而是一次预测多个 token。有很好的统计学论据说明为什么这是个好主意——也许它让你能更好地预测未来。但也有一个很好的系统论据：你现在内置了一个推测解码器（speculative decoder），这是一个可以用来加速模型解码的技巧。

---

## 21. Conclusion / 结语

**EN** To put everything together: MoEs are a very clever idea to take advantage of sparsity so that you can have more parameters than you're paying for. You don't pay for the compute cost of all your parameters, but you are getting the parameter benefits. You might initially think that this kind of routing problem is very hard, but it turns out that very simple things work well, even at scale. At this point, it's clear that MoEs are here to stay, so you should understand how they work and what they are.

**ZH** 总结一下：MoE 是一个非常聪明的想法，利用稀疏性（sparsity）让你拥有比你实际支付的更多的参数。你不用为所有参数支付计算成本，但你能获得参数的好处。你最初可能认为这种路由问题非常困难，但事实证明，非常简单的方法效果很好，甚至在大规模上也是如此。到了现在，很明显 MoE 已经站稳了脚跟，所以你应该了解它们如何工作以及它们是什么。
