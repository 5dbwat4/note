# 实验二：基于 Transformer 的机器翻译

## 1. Project Introduction

### （1）实验简介

本实验使用 MindSpore 实现并训练一个 Transformer（base 配置）**英译中**翻译模型，包括以下四个环节：

1. **数据准备**：读取 23,610 条已用空格分好词的英中句对，英文按词、中文按字切分。查共享词表把 token 转成 id，加上 `<s>`/`</s>` 标记，补齐到 40 位，写成 MindRecord 文件。按 8:2 随机切分训练集和测试集。
2. **模型构建**：6 层 Encoder 加 6 层 Decoder，`d_model=512`、8 个注意力头、FFN 维度 2048，使用正弦位置编码、Pre-LN 残差结构，输入词向量与输出投影共享权重。
3. **模型训练**：训练时用 Teacher Forcing，损失为带 Label Smoothing 的交叉熵，优化器为 Adam，学习率先 warmup 再按反平方根衰减，并做梯度范数裁剪，共训练 15 个 epoch。
4. **模型推理**：用 Beam Search 自回归解码，在测试集上输出译文。


### （2）开发环境及系统运行要求

- 开发环境：ModelArts Ascend Notebook 环境。
- 实际使用的具体环境：
  - 规格 `1 * Ascend Snt9 | 24 vCPUs | 96 GB`；
  - 公共镜像 `mindspore_2.7.2-cann_8.5.2-py_3.11-hce_2.0.2512-aarch64-snt9b`

## 2. Technical Details

### 2.1 理论知识

> （1）工程实践当中所用到的理论知识阐述

#### （1）神经机器翻译与 Encoder-Decoder 框架

机器翻译可以看成一个条件语言模型：给定源语言句子 $x=(x_1,\dots,x_S)$，模型要估计目标句 $y=(y_1,\dots,y_T)$ 的条件概率，并按自回归方式分解：

$$
P(y\mid x)=\prod_{t=1}^{T}P(y_t\mid y_{<t},x)
$$

Encoder 把源句编码成一组上下文向量 $H=\mathrm{Enc}(x)\in\mathbb R^{S\times d}$。Decoder 每一步读入已生成的前缀 $y_{<t}$，同时关注 $H$，输出下一个词在词表上的分布。实验手册第 2 章的 Seq2Seq 用 GRU 逐步传递隐状态，计算无法在时间维上并行，长距离依赖也要经过很多步才能传到。Transformer 把循环结构全部换成注意力，任意两个位置之间的路径长度都是 $O(1)$，训练时整个序列可以并行计算。

#### （2）缩放点积注意力与多头注意力

$$
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V
$$

其中 $M$ 是加性掩码：允许关注的位置为 $0$，屏蔽的位置为一个很大的负数（代码里是 $-10000$）。除以 $\sqrt{d_k}$ 是为了防止维度较大时点积数值过大，使 softmax 落入梯度接近 0 的饱和区。

多头注意力先用 $W^Q,W^K,W^V\in\mathbb R^{d\times d}$ 做线性映射，再把结果在特征维上切成 $h$ 份，每个头的维度 $d_k=d/h$。各头独立计算注意力后拼接，最后经过 $W^O$ 输出：

$$
\begin{aligned}
\mathrm{MHA}(X,Y)&=\mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)W^O,\\
\mathrm{head}_i&=\mathrm{Attention}(XW^Q_i,YW^K_i,YW^V_i)
\end{aligned}
$$

模型中有三种注意力：

| 类型 | 位置 | Q 来源 | K/V 来源 | 掩码 |
|---|---|---|---|---|
| Encoder 自注意力 | Encoder 每层 | 源句 | 源句 | 源句 padding 掩码 $m^{src}(m^{src})^\top$ |
| Decoder 掩码自注意力 | Decoder 每层第 1 个子层 | 目标前缀 | 目标前缀 | 目标 padding 掩码 ⊙ 下三角因果掩码 |
| Encoder-Decoder 交叉注意力 | Decoder 每层第 2 个子层 | 目标前缀 | Encoder 输出 | 理论上每个目标位置都可以看到所有有效的源位置：$\mathbf 1_T (m^{src})^\top$ |

#### （3）位置编码、残差与层归一化

注意力本身不区分输入顺序，所以要在词向量上加入位置信息。本实现用固定的正弦位置编码（`position_encoding`）：前 $d/2$ 维为 $\sin(pos\cdot\omega_i)$，后 $d/2$ 维为 $\cos(pos\cdot\omega_i)$，$\omega_i=10000^{-i/(d/2-1)}$。词向量加位置编码之前先乘以 $\sqrt{d}$（`EmbeddingPostprocessor`）。

每个子层都按 **Pre-LN** 方式组织：$x\leftarrow x+\mathrm{Dropout}(\mathrm{Sublayer}(\mathrm{LN}(x)))$。对应代码中的 `LayerPreprocess`（先做 LayerNorm）和 `LayerPostprocess`（Dropout 后加残差）。Encoder 和 Decoder 的输出端各有一个额外的 LayerNorm。与原论文的 Post-LN 相比，Pre-LN 的梯度更稳定，对 warmup 长度不那么敏感。

前馈网络对每个位置单独作用：$\mathrm{FFN}(x)=W_2\,\mathrm{ReLU}(W_1x+b_1)+b_2$，维度变化为 $512\to2048\to512$。

#### （4）权重共享与输出层

源语言、目标语言和输出投影共用同一个 $V\times d$ 的词向量矩阵 $E$（`tfm_embedding_lookup.embedding_table`）。输出层计算 $\log\mathrm{softmax}(hE^\top)$（`PredLogProbs`）。本实验的中英文 token 都在同一个 10,067 大小的词表里，共享后参数量减少约 $2\times5.15$M，也让中英 token 处在同一个向量空间中。

#### （5）训练目标：Teacher Forcing 与 Label Smoothing

训练时把整条真实目标句右移一位作为 Decoder 输入（`<s> y_1 … y_{T-1}`），标签为 `y_1 … y_T </s>`，配合因果掩码，一次前向就能并行算出所有位置的损失，这就是 Teacher Forcing。推理时 Decoder 只能读到自己生成的前缀，训练和推理的输入分布因此不同，称为 **exposure bias**，前面一步出错会影响后面所有步。

损失函数是带 Label Smoothing（$\varepsilon=0.1$）的交叉熵：目标词的概率设为 $1-\varepsilon=0.9$，其余 $V-1$ 个词平分 $\varepsilon$。padding 位置用 `label_weights` 屏蔽：

$$
\mathcal L=-\frac{\sum_{b,t}w_{b,t}\sum_{v}q_{b,t,v}\log p_{b,t,v}}{\sum_{b,t}w_{b,t}},\qquad q_{b,t,v}=\begin{cases}0.9 & v=y_{b,t}\\ 0.1/(V-1) & \text{otherwise}\end{cases}
$$

因此，即使模型的预测与 $q$ 完全一致，损失也不会降到 0，下界约为 $q$ 的熵 $H(q)\approx0.33+0.1\ln(10066/0.1)\approx1.48$。看训练曲线时需要注意这一点。

#### （6）学习率调度：Warmup + 反平方根衰减

`create_dynamic_lr` 用 `constant*rsqrt_hidden*linear_warmup*rsqrt_decay` 组合出学习率（$s$ 为步数，$w$ 为 warmup 步数，$s_d$ 为开始衰减的步数）：

$$
\eta(s)=\eta_0\cdot d^{-0.5}\cdot\min\!\left(1,\frac{s}{w}\right)\cdot\max(s-s_d+w,\ w)^{-0.5}
$$

当 $w<s<s_d$ 时，学习率保持上一步的值不变。notebook 中的设置为 $\eta_0=1.0,\ w=800,\ s_d=1200$，学习率从 0 线性升到峰值 $512^{-0.5}\cdot800^{-0.5}=1.56\times10^{-3}$，在第 800 到 1200 步之间保持不变，之后按 $1/\sqrt{s}$ 衰减，第 8850 步时降到 $4.8\times10^{-4}$。

**为什么先升后降：**

- **Warmup**：训练刚开始时参数是随机的，Adam 的二阶矩估计 $v_t$ 只基于很少几步，偏差和方差都大，再加上注意力 softmax 容易饱和，此时用大学习率容易发散。线性 warmup 让模型先在小步长下找到一个较平坦的区域。
- **衰减**：训练后期需要减小步长，让参数在极小值附近收敛，并降低梯度噪声。反平方根衰减比较平缓，比指数衰减更适合 Transformer 这类需要训练较长时间的模型。

实验手册原来的配置是 $w=8000,\ s_d=16000$，但 notebook 总共只有 8,850 步，学习率在训练结束时还没升到峰值（见图 2-1）。notebook 把它改成了 800/1200，与训练步数相匹配。

![图 2-1 学习率调度曲线](figs/lr_schedule.png)

*图 2-1：notebook 实际使用的调度（800/1200）与实验手册原始配置（8000/16000）对比，后者在 8,850 步内一直处于 warmup 阶段。*

#### （7）解码：Greedy 与 Beam Search

推理要求 $\hat y=\arg\max_y\log P(y\mid x)$，但搜索空间随长度指数增长，只能近似求解。

- **Greedy**：每一步只保留概率最大的那个词。速度快，但一步选错就无法挽回。
- **Beam Search**：每一步保留累计对数概率最高的 $k$ 个前缀。每个前缀扩展 $V$ 个候选，共 $k\cdot V$ 个，再从中选出 top-$k$。$k=1$ 时退化为 Greedy。

累计对数概率是负数逐项相加，句子越长得分越低，所以 Beam Search 偏向输出短句。本实现在最后排序时用 GNMT 的长度惩罚做归一化：

$$
\mathrm{score}(y)=\frac{\log P(y\mid x)}{\left(\frac{5+|y|}{6}\right)^{\alpha}},\qquad \alpha=1.0
$$

#### （8）评价指标：BLEU

notebook 只打印译文，没有给出量化指标。本报告补充计算了 **字符级 corpus BLEU-4**：参考译文本身就是按字切分的，直接以字为单位计算，用 nltk 的 `corpus_bleu` 和 `SmoothingFunction().method1`：

$$
\mathrm{BLEU}=\mathrm{BP}\cdot\exp\Big(\sum_{n=1}^{4}\tfrac14\log p_n\Big),\qquad \mathrm{BP}=\min\!\left(1,\ e^{1-r/c}\right)
$$

$p_n$ 为 n-gram 修正精确率，$r$ 和 $c$ 分别为参考译文和系统输出的总长度。由于以字为单位，这里的 BLEU 数值不能和常见的中文词级 BLEU 直接比较，只用于本实验内部不同配置之间的对比。


### 2.2 具体算法

> （2）具体的算法，请用文字、示意图或者是伪代码等形式进行描述（不要贴大段的代码）

#### （1）整体流程

<excalidraw>
2×2 数据流总览图，按“左上 → 右上 → 左下 → 右下”的顺序排列 4 个泳道（用浅色大矩形框住，各自带标题）：

【泳道 1：数据准备（data_prepare）】
- 圆角框 "ch_en_all.txt\n23,610 句对\n(英文按词 / 中文按字，已空格分隔)"
- ↓ 箭头 "WhiteSpaceTokenizer.tokenize"
- 菱形 "len ≥ 39 ?" → 右侧分支 "丢弃 (3 条)"
- ↓ "create_training_instance：加 <s> / </s>"
- ↓ "write_instance_to_file：查词表转 id、补 0 到 40、生成 mask"
- 分叉为两个圆柱体："train.mindrecord\n18,887 条"（80%）和 "test.mindrecord\n4,720 条"（20%）

【泳道 2：训练（train）】
- "MindDataset → TypeCast → batch(32)"（标注 shuffle=False）
- ↓ "TransformerNetworkWithLoss\n(Transformer + Label-Smoothed CE)"
- ↓ "TransformerTrainOneStepCell\n反向求梯度 → ClipByNorm(5.0) → Adam"
- 侧边小框 "create_dynamic_lr\nwarmup 800 / decay@1200" 用虚线箭头指向 Adam
- ↓ 圆柱体 "transformer-32_40-15_590.ckpt"

【泳道 3：推理（evaluate）】
- "load_weights：checkpoint 参数改名\n(tfm_decoder.* → tfm_decoder.decoder.*，\n复制共享 embedding)"
- ↓ "TransformerModel(is_training=False)\nEncoder 一次前向 + TileBeam ×4"
- ↓ "BeamSearchDecoder：循环 40 步\n每步调用 TransformerDecoderStep"
- ↓ "convert_ids_to_tokens，截取 <s> 与 </s> 之间的内容"

【泳道 4：评估（本报告补充）】
- "译文 vs 参考 → 字符级 BLEU-4、\n按长度分桶 BLEU、重复率、耗时"
- "自定义句子 → Bad Case 分析"

泳道按 1→2→3→4 的顺序用粗箭头依次相连（2→3 经过两行之间的空隙绕回左下）。配色：数据用蓝色，训练用橙色，推理用绿色，评估用紫色。
</excalidraw>

*图 2-2：实验整体流程*

#### （2）模型结构

<excalidraw>
标准 Transformer 结构图（参考论文 Figure 1 的版式，按本实现的 Pre-LN 结构画）。左列为 Encoder，右列为 Decoder，两列都标注 "×6"。

左列 Encoder，自下而上：
1. "source_eos_ids (B×40)\n例：I love you . </s> 0 0 …"
2. "Embedding Lookup (10067×512)，共享" —— 用一条虚线把这个框连到右列 Decoder 的 Embedding 框和顶部的输出投影框，并标注 "weight tying"
3. "× √512" → "⊕ Sinusoidal Position Encoding" → "Dropout 0.2"
4. 大圆角框 "EncoderCell × 6"，框内自下而上：
   - "LayerNorm" → "Multi-Head Self-Attention (h=8, d_k=64)\nmask: src_mask ⊗ src_mask" → "Dropout" → "⊕ 残差"
   - "LayerNorm" → "FFN 512→2048 (ReLU)→512" → "Dropout" → "⊕ 残差"
5. "Final LayerNorm" → 输出 "Encoder 输出 H (B×40×512)"

右列 Decoder，自下而上：
1. "target_sos_ids (B×40)\n例：<s> 我 爱 你 。 0 0 …"
2. "Embedding Lookup (共享)" → "× √512" → "⊕ PE" → "Dropout"
3. 大圆角框 "DecoderCell × 6"，框内自下而上：
   - "LayerNorm" → "Masked Multi-Head Self-Attention\nmask: tgt_mask ⊗ tgt_mask ⊙ 下三角" → "⊕ 残差"
   - "LayerNorm" → "Multi-Head Cross-Attention\nQ = decoder，K/V = H\nmask: src_mask ⊗ src_mask (代码实际行为)" → "⊕ 残差"。从左列 H 画一条粗箭头连到该框的 K/V 输入
   - "LayerNorm" → "FFN" → "⊕ 残差"
4. "Final LayerNorm" → "MatMul Eᵀ (10067)" → "LogSoftmax"
5. 训练分支："与 target_eos_ids 比较 → Label-Smoothed CE (ε=0.1)，padding 由 target_eos_mask 屏蔽"
6. 推理分支（虚线）："TransformerDecoderStep：取最后一个位置 → BeamSearchDecoder"

右侧单独画一个 40×40 网格示意图，比较 "cross-attention 理论掩码 1ᵀ·m_src" 和 "代码中实际的 m_src·m_srcᵀ"：后者在目标位置 t ≥ 源句长度的那些行全部被屏蔽，涂成红色。
</excalidraw>

*图 2-3：本实验 Transformer（base）结构。注意交叉注意力实际使用的掩码，详见 2.3（4）和 3.6。*

#### （3）训练一步（TransformerTrainOneStepCell）

<pseudocode>
\begin{algorithm}[H]
\caption{Transformer 训练一步（Teacher Forcing + 标签平滑 + 梯度裁剪）}
\KwIn{batch: $X^{src}$=source\_eos\_ids, $m^{src}$, $Y^{in}$=target\_sos\_ids, $m^{tgt}$, $Y^{out}$=target\_eos\_ids, $w$=target\_eos\_mask; 第 $s$ 步学习率 $\eta_s$}
$E_x \leftarrow \mathrm{Dropout}(\sqrt{d}\cdot E[X^{src}] + PE)$\;
$A^{enc} \leftarrow m^{src} (m^{src})^\top$ \tcp*{$B\times S\times S$}
$H \leftarrow \mathrm{LN}(\mathrm{EncoderCell}^{(6)}\circ\cdots\circ\mathrm{EncoderCell}^{(1)}(E_x; A^{enc}))$\;
$E_y \leftarrow \mathrm{Dropout}(\sqrt{d}\cdot E[Y^{in}] + PE)$\;
$A^{dec} \leftarrow \big(m^{tgt}(m^{tgt})^\top\big)\odot \mathrm{tril}(\mathbf 1_{T\times T})$ \tcp*{因果掩码}
$Z \leftarrow \mathrm{LN}(\mathrm{DecoderCell}^{(1..6)}(E_y; A^{dec}, H, A^{enc}))$ \tcp*{交叉注意力复用 $A^{enc}$}
$\log p \leftarrow \mathrm{LogSoftmax}(Z E^\top)$ \tcp*{$B\cdot T\times V$}
$q \leftarrow 0.9\cdot\mathrm{onehot}(Y^{out}) + \frac{0.1}{V-1}(1-\mathrm{onehot}(Y^{out}))$\;
$\mathcal L \leftarrow -\sum_{b,t} w_{b,t}\langle q_{b,t},\log p_{b,t}\rangle \,/\, (\sum_{b,t} w_{b,t}+10^{-5})$\;
$g \leftarrow \nabla_\theta \mathcal L$\;
\ForEach{参数梯度 $g_i$}{ $g_i \leftarrow g_i\cdot\min(1, 5.0/\lVert g_i\rVert_2)$ \tcp*{ClipByNorm，逐张量裁剪} }
$\theta \leftarrow \mathrm{Adam}(\theta, g, \eta_s)$\;
\Return $\mathcal L$
\end{algorithm}
</pseudocode>

#### （4）Beam Search 解码（BeamSearchDecoder）

<pseudocode>
\begin{algorithm}[H]
\caption{Beam Search（批量化，定长展开 max\_decode\_length 步）}
\KwIn{Encoder 输出 $H$ 复制 $k$ 份（TileBeam），beam 宽度 $k$，词表大小 $V$，最大长度 $L=40$，长度惩罚系数 $\alpha$}
seq $\leftarrow$ [\texttt{<s>}]$^{B\times k}$；score $\leftarrow [0,-\infty,\dots,-\infty]$ \tcp*{初始只激活第 1 个 beam，避免 $k$ 个 beam 选出相同的词}
finished $\leftarrow$ False；len $\leftarrow 0$\;
\For{$t \leftarrow 1$ \KwTo $L$}{
  $\ell \leftarrow \mathrm{DecoderStep}(\mathrm{seq}, H)$ \tcp*{取最后一个位置，$B\times k\times V$ 的对数概率}
  total $\leftarrow \ell + \mathrm{score}[:,:,\mathrm{None}]$；对 finished 的 beam，total $\mathrel{+}= -\infty$\;
  (topScore, idx) $\leftarrow \mathrm{TopK}(\mathrm{reshape}(\mathrm{total}, B, kV),\ k)$\;
  beam $\leftarrow \lfloor idx/V\rfloor$；word $\leftarrow idx \bmod V$\;
  对已经 finished 的 beam：beam 保持原编号，word $\leftarrow$ \texttt{</s>}，topScore $\leftarrow$ 原 score\;
  按“没有输出 \texttt{</s>} 的 beam 排在前面”重新排序 (beam, word, topScore)\;
  len $\leftarrow$ gather(len + [not finished], beam)；seq $\leftarrow$ concat(gather(seq, beam), word)\;
  finished $\leftarrow$ (word = \texttt{</s>})；score $\leftarrow$ topScore\;
}
final $\leftarrow$ score $/\ ((5+\mathrm{len})/6)^{\alpha}$\;
\Return 每个样本 final 最高的 seq
\end{algorithm}
</pseudocode>

要点：

- 为了能在静态图（GRAPH_MODE）中运行，循环固定展开 $L$ 步，即使所有 beam 都已经结束也不会提前退出。这是推理首次编译约 8 分钟的主要原因。
- `TransformerDecoderStep` 没有 KV-cache，每一步都把完整前缀重新送入 6 层 Decoder，单句的计算量是 $O(L^2)$。
- 推理时交叉注意力的掩码是 `enc_mask[:,0:1,:] * ones(B, max_decode_length, 1)`，即每个目标位置都能看到全部有效的源位置，这是**正确**的写法。训练分支直接复用了 $A^{enc}$，两者**不一致**，见 2.3（4）。

#### （5）学习率生成（create_dynamic_lr）

<pseudocode>
\begin{algorithm}[H]
\caption{create\_dynamic\_lr(schedule="constant*rsqrt\_hidden*linear\_warmup*rsqrt\_decay")}
\KwIn{总步数 $N$, $\eta_0$, warmup $w$, hidden $d$, 衰减起点 $s_d$, 最小学习率 $\eta_{min}$}
$s_d \leftarrow \max(s_d, w)$；lr $\leftarrow [\,]$\;
\For{$s \leftarrow 1$ \KwTo $N$}{
  $\eta \leftarrow \eta_0 \cdot d^{-1/2} \cdot \min(1, s/w) \cdot \max(s - s_d + w,\ w)^{-1/2}$\;
  \lIf{$w < s < s_d$}{$\eta \leftarrow$ lr[-1] \tcp*{平台期}}
  \lIf{$s > w$}{$\eta \leftarrow \max(\eta, \eta_{min})$}
  lr.append($\eta$)\;
}
\Return lr \tcp*{长度为 $N$ 的列表，作为 Tensor 传给 Adam，每步取一个值}
\end{algorithm}
</pseudocode>


### 2.3 程序开发中的重要技术细节

> （3）程序开发中重要的技术细节，比如用到了哪些重要的函数？这些函数来自于哪些基本库？功能是什么？自己编写了哪些功能函数？等等

#### （1）`src/` 各模块分工

- **`tokenization.py`**
  - 主要类/函数：`WhiteSpaceTokenizer`, `load_vocab_file`, `convert_by_vocab_dict`
  - 作用：清理控制字符、统一空白字符，然后按空格切分。词表的行号就是 id，不在词表中的 token 一律映射为 `<unk>`（id 0）
- **`data_utils.py`**
  - 主要类/函数：`create_training_instance`, `write_instance_to_file`
  - 作用：生成 `<s>`+句子 和 句子+`</s>` 两种序列，转成 id 并补齐到 40 位，同时生成 mask，写入 MindRecord
- **`transformer_model.py`**
  - 主要类/函数：`TransformerConfig`, `EmbeddingLookup`, `EmbeddingPostprocessor`, `MultiheadAttention`, `SelfAttention`, `FeedForward`, `EncoderCell`/`DecoderCell`, `TransformerEncoder`/`Decoder`, `CreateAttentionMaskFromInputMask`, `PredLogProbs`, `TransformerDecoderStep`, `TransformerModel`
  - 作用：网络结构。`TransformerModel` 根据 `is_training` 构建不同分支：训练时 Decoder 一次处理整个序列，推理时为 `DecoderStep` 加 Beam Search
- **`beam_search.py`**
  - 主要类/函数：`BeamSearchDecoder`, `TileBeam`, `LengthPenalty`, `Mod`
  - 作用：批量 Beam Search。`Mod` 用 `FloorDiv` 组合实现取模，原因是 MindSpore 早期图模式没有取模算子
- **`transformer_for_train.py`**
  - 主要类/函数：`TransformerTrainingLoss`, `TransformerNetworkWithLoss`, `TransformerTrainOneStepCell`, `ClipGradients`, `...WithLossScaleCell`
  - 作用：计算损失，`GradOperation` 求梯度，逐张量做范数裁剪（5.0），可选分布式梯度归约和动态 loss scale
- **`lr_schedule.py`**
  - 主要类/函数：`create_dynamic_lr`
  - 作用：生成逐步学习率列表
- **`train_util.py`**
  - 主要类/函数：`LossCallBack`
  - 作用：每步打印 loss 并追加写入 `loss.log`
- **`weight_init.py`**
  - 主要类/函数：`weight_variable`, `normal_weight`
  - 作用：Dense 层用 Glorot 风格的均匀分布初始化，limit $=\sqrt{3/\mathrm{avg}(fan)}$；词向量用 $\mathcal N(0, d^{-1/2})$

#### （2）用到的 MindSpore 主要 API

- **`context.set_context(mode=GRAPH_MODE, device_target="Ascend")`**
  - 所属模块：`mindspore`
  - 用途：用静态图模式在昇腾上运行，整张网络编译后下发到设备执行
- **`FileWriter.add_schema / write_raw_data / commit`**
  - 所属模块：`mindspore.mindrecord`
  - 用途：定义字段结构并写出 MindRecord，同时生成 `.db` 索引文件
- **`MindDataset(..., shuffle=False)`, `.map(TypeCast)`, `.batch(drop_remainder=True)`**
  - 所属模块：`mindspore.dataset`
  - 用途：读取数据、转换类型、组成 batch。因为图模式需要固定 shape，所以丢弃不足一个 batch 的尾部数据
- **`nn.Cell`, `construct`**
  - 所属模块：`mindspore.nn`
  - 用途：所有网络模块的基类和前向函数
- **`nn.Dense(...).to_float(mstype.float16)`**
  - 所属模块：`mindspore.nn`
  - 用途：混合精度：参数保存为 fp32，计算用 fp16。LayerNorm 和 Softmax 先转回 fp32 计算
- **`P.BatchMatMul(transpose_b=True)`, `P.Softmax`, `P.Transpose`, `P.Reshape`**
  - 所属模块：`mindspore.ops`
  - 用途：实现多头注意力的矩阵乘法和维度变换
- **`P.GatherV2` / `P.OneHot`**
  - 所属模块：`mindspore.ops`
  - 用途：词向量查表；OneHot 也用于构造标签平滑分布
- **`P.TopK(sorted=True)`, `P.GatherNd`, `P.Select`, `P.FloorDiv`**
  - 所属模块：`mindspore.ops`
  - 用途：Beam Search 中选出 top-k 候选，并按 beam 编号重排状态
- **`C.GradOperation(get_by_list=True, sens_param=True)`**
  - 所属模块：`mindspore.ops.composite`
  - 用途：对参数列表求梯度，`sens` 参数可用于 loss scale
- **`nn.ClipByNorm`**
  - 所属模块：`mindspore.nn`
  - 用途：对每个梯度张量按 L2 范数裁剪
- **`nn.Adam(params, lr=Tensor[N])`**
  - 所属模块：`mindspore.nn.optim`
  - 用途：学习率传入一个长度为 N 的数组时，按 global step 逐步取值
- **`Model.train(epoch, ds, callbacks, dataset_sink_mode=False)`**
  - 所属模块：`mindspore.train`
  - 用途：训练循环。非下沉模式下每步都会回到 Python 执行回调
- **`ModelCheckpoint`, `CheckpointConfig`, `TimeMonitor`, `Callback`**
  - 所属模块：`mindspore.train.callback`
  - 用途：保存模型（每 590 步一次，最多保留 2 个）、计时，以及自定义回调
- **`load_checkpoint`, `load_param_into_net`**
  - 所属模块：`mindspore.train.serialization`
  - 用途：加载模型权重
- **`constexpr`**
  - 所属模块：`mindspore.ops.primitive`
  - 用途：在编译期生成常量张量，代码中用来生成下三角因果掩码

#### （3）实现细节

1. **SOS/EOS 的用法**：训练时 Encoder 输入是 `source_eos_ids`（`x </s>`），Decoder 输入是 `target_sos_ids`（`<s> y`），标签是 `target_eos_ids`（`y </s>`），损失权重是 `target_eos_mask`。`source_sos_*` 两个字段写入了 MindRecord，但训练和推理都没有用到。
2. **两种掩码的构造**：`CreateAttentionMaskFromInputMask` 用 `BatchMatMul([B,S,1],[B,1,S])` 把一维 mask 扩展成 $B\times S\times S$。因果掩码由 `np.tril` 生成，与 padding 掩码逐元素相乘后，在 `MultiheadAttention` 里转成 $(1-m)\times(-10000)$ 加到注意力分数上。
3. **训练与推理的参数名对齐**：推理时 `BeamSearchDecoder` 把 `TransformerDecoderStep` 包了一层，参数名多出 `decoder.` 前缀。所以 `load_weights` 要把 checkpoint 中的 `tfm_decoder.*` 改名为 `tfm_decoder.decoder.*`，并把共享词向量复制一份给 `tfm_decoder.decoder.tfm_embedding_lookup`。另外，训练得到的 checkpoint 里还保存了 Adam 的 `moment1/moment2`、`learning_rate`、`global_step` 等变量，推理时不需要。
4. **训练分支交叉注意力的掩码与推理不一致（代码问题）**：`TransformerModel.construct` 的训练分支把 Encoder 自注意力的掩码 `enc_attention_mask`（$m^{src}(m^{src})^\top$，$S\times S$）直接传给了 Decoder 的交叉注意力。这个掩码的第 $t$ 行只有在 $t<|x|$ 时才不全为 0。也就是说，**目标位置 $t\ge$ 源句长度时，这一行的所有源位置都被屏蔽**：softmax 的输入全是 $-10000$，结果近似均匀分布，这些位置实际上拿不到源句的信息。推理分支则用 `enc_mask[:,0:1,:]` 复制成 $T$ 行，每一行都能看到全部源位置，这是正确的写法。按训练集统计（见拓展文档），**有 74.7% 的句对、20.5% 的目标 token 位置受到影响**，这些句子都是中文 token 数多于“英文词数 + 1”的句子。模型在这些位置只能依赖目标端前缀，相当于一个语言模型；但推理时它们又能看到源句，训练和推理的条件不一致。3.6 节的对照实验验证了这一点。
5. **数据没有打乱（流程问题）**：`load_dataset` 设置了 `shuffle=False`，`train_cfg.do_shuffle=True` 只是一个配置项，没有任何代码读取它。而 `ch_en_all.txt` 大致按句子长度由短到长排列（相邻两句满足非递减的比例为 68.9%）。所以每个 epoch 都是先训练短句再训练长句，loss 曲线呈锯齿状（见 3.3），每个 epoch 的最后几百步只更新长句，模型会偏向长句的分布。
6. **推理的工程适配**：`np.bool = np.bool_` 用于兼容新版 NumPy；`reserve_class_name_in_scope=False` 保证参数名不带类名前缀，才能和 checkpoint 匹配；Beam Search 循环用 `add_flags(loop_can_unroll=True)` 允许图编译时展开。

#### （4）本报告新增的脚本

全部放在 `report/exp/` 下，在服务器上的 `/cache/lab2` 运行，详细步骤见 `拓展操作说明.md`：

| 脚本/函数 | 功能 |
|---|---|
| `exp.py tok` | 探索 1：测试多种输入句子的 token 和 id 映射，包括未登录词 |
| `exp.py count` | 思考题：分别实例化 `num_attention_heads ∈ {8,4,2,1}` 的模型，按模块统计参数量 |
| `exp.py train` (`cmd_train`, `build_net`, `FixedMaskModel`) | 可配置的训练入口，支持 `--heads/--bs/--lr/--warmup/--decay/--epochs/--shuffle/--fixmask`，把每步 loss 和学习率写入 `loss.csv`。`FixedMaskModel` 继承 `TransformerModel`，只重写训练分支，交叉注意力改用 $\mathbf 1_T (m^{src})^\top$；参数名保持不变，可直接用原来的推理代码加载 |
| `exp.py eval` (`cmd_eval`, `load_weights`, `detok`, `en_tokenize`) | 全测试集推理：计算字符级 BLEU-4、按源句长度分桶的 BLEU、平均译文长度、重复率，统计首个 batch（含编译）和稳定后的单句耗时，可选翻译自定义英文句子。`load_weights` 会过滤掉优化器状态 |
| `exp.py diag` (`cmd_diag`) | 诊断模型是否用到了源句：在 teacher forcing 下比较“真实源句 / batch 内打乱的源句 / 空源句”三种输入的 loss |
| `score_tsv.py` | 对 notebook 原始输出（`source/result` 对）离线计算 BLEU 等指标 |
| `run.sh` / `bg.sh` / `sync.ps1` | 分阶段的实验队列、在服务器后台运行（nohup）、本地同步到服务器 |


## 3. Experiment Results

### 3.1 实验环境与操作步骤

> **步骤 0：环境准备**

按 notebook 第 0 节的说明，选择镜像 `mindspore_2.7.2-cann_8.5.2-py_3.11` 和规格 `1 * Ascend Snt9`，创建 Notebook 后上传 `mt_transformer_mindspore.ipynb`、`src/` 和 `data/`。在 Terminal 中写入 `mindspore_ascend_kernel.sh` 和 `kernel.json`，然后选择 `MindSpore Ascend` kernel。

<screenshot>ModelArts 控制台 Notebook 实例详情页：能看到镜像名 mindspore_2.7.2-cann_8.5.2-py_3.11、规格 1*Ascend Snt9 | 24vCPUs | 96GB，状态“运行中”</screenshot>

<screenshot>JupyterLab 打开 mt_transformer_mindspore.ipynb，右上角 kernel 名称为 “MindSpore Ascend”，左侧文件栏展开 src/ 和 data/</screenshot>

<screenshot>Terminal 中执行 npu-smi info 的输出：910B4，Health OK，HBM 32768MB</screenshot>

> **步骤 1：导入依赖、设置运行环境（Cell 2–3）**

导入 MindSpore 的数据、网络、优化器、回调等模块以及 `src/` 下的各个模块，然后调用 `context.set_context(mode=GRAPH_MODE, device_target="Ascend")`，在昇腾上以静态图模式运行。这两个 Cell 只输出了一些 API 弃用警告，没有报错。

<screenshot>notebook Cell 2、Cell 3 的代码与输出（若干 WARNING，无报错）</screenshot>

> **步骤 2：数据预处理（Cell 5–7）**

`data_cfg` 设置 `max_seq_length=40`、`clip_to_max_len=False`，即超过长度的句子直接丢弃，不做截断。`data_prepare` 逐行读取语料，完成分词、添加起止标记、转换为 id 和 mask，再按随机抽取的 20% 下标分别写入 `train.mindrecord` 和 `test.mindrecord`，同时把原句写入 `source_*.txt`，推理时用来对照。运行结束时输出 `finish 23607/23607`。

<screenshot>Cell 7 输出的最后几行 “finish 23607/23607”，以及 data/ 目录中新生成的 train.mindrecord、test.mindrecord、source_*.txt 及 .db 文件</screenshot>

> **步骤 3：数据加载检查（Cell 9–10）**

用 `load_dataset` 读出第一条训练样本的 `source_eos_ids`，结果是 `[3983, 3, 2, 0, …, 0]`（长度 40），对应 `<一个英文词> . </s>`，后面用 0 补齐，与预期一致。

<screenshot>Cell 10 的输出 Tensor(shape=[40], ...) [3983, 3, 2, 0, ...]</screenshot>

### 3.2 探索 1：token 与 id 映射、未登录词

notebook 默认例句 `我 喜 欢 这 门 课 程` 映射为 `[5, 104, 103, 23, 357, 814, 863]`。我另外测试了几种输入（`exp.py tok`）：

```text
输入: 我 喜 欢 这 门 课 程        Tokens: ['我','喜','欢','这','门','课','程']   IDs: [5, 104, 103, 23, 357, 814, 863]  OOV: []
输入: 我 喜欢 这门 课程           Tokens: ['我','喜欢','这门','课程']            IDs: [5, 0, 0, 0]                      OOV: ['喜欢','这门','课程']
输入: 浙 江 大 学                Tokens: ['浙','江','大','学']                  IDs: [0, 6467, 105, 99]                OOV: ['浙']
输入: 鑫 犇 龘                   Tokens: ['鑫','犇','龘']                       IDs: [0, 0, 0]                         OOV: 全部
输入: I love natural language processing .   IDs: [7, 539, 2843, 1070, 0, 3]                         OOV: ['processing']
输入: Tom can ' t speak Klingon .           IDs: [25, 83, 8, 24, 400, 0, 3]                          OOV: ['Klingon']
输入: ChatGPT is cool 😀                     IDs: [0, 21, 3081, 0]                                    OOV: ['ChatGPT','😀']
```

<screenshot>notebook Cell 12：把 sample_text 依次改为 "我 喜欢 这门 课程" 和 "I love natural language processing ." 后的运行输出，IDs 中出现 0</screenshot>

**分析：**

1. **词表结构**：`ch_en_vocab.txt` 每行一个 token，行号即 id。前三个是特殊符号 `<unk>=0, <s>=1, </s>=2`，之后大致按词频从高到低排列：`.`=3、`。`=4、`我`=5、`的`=6、`I`=7……
2. **未登录词统一映射为 `<unk>`，id 为 0**：`convert_by_vocab_dict` 查不到某个 token 时返回 `vocab_dict["<unk>"]`。**padding 的 id 也是 0**，两者只能靠 mask 区分，而 `<unk>` 的 mask 是 1，所以它仍然会被模型“看到”。
3. **分词粒度必须和词表一致**：中文词表是按字建立的，如果输入按词切分（例如“喜欢”），即使每个字都在词表里，整个词也会变成 `<unk>`。分词器只按空格切分，所以推理时的预处理必须和训练语料保持一致：中文逐字加空格，英文中的缩写也要和语料一样写成 `can ' t`。
4. **英文按整词建表、没有子词切分**，因此 `processing`、人名、品牌名都会变成 OOV；中文按字建表，只有罕见字才会 OOV。训练语料本身没有 OOV，但实际使用时 OOV 很常见，后果见 3.7。

### 3.3 思考题：`num_attention_heads` 从 8 改为 1

#### （1）参数量不变

`MultiheadAttention` 中 Q/K/V/O 四个投影矩阵的形状都是 $d\times(h\cdot d_k)$，而 `SelfAttention` 中 $d_k=d/h$，所以 $h\cdot d_k=d$ 恒成立，每个注意力块的参数量固定为 $4d^2=1{,}048{,}576$，**与头数无关**。改变头数只是改变 reshape 时把 $d$ 维切成几份。用 `exp.py count` 实际实例化模型统计：

| num_attention_heads | 总参数量 | 注意力 | FFN | Embedding | LayerNorm |
|---|---|---|---|---|---|
| 8 / 4 / 2 / 1 | 49,257,984 | 18,892,800 | 25,208,832 | 5,154,304 | 2,048 |

四种设置的统计结果完全相同，参数量**完全不变**。计算量也几乎不变：注意力分数矩阵的元素数由 $h\cdot T^2$ 变为 $T^2$，相比整个模型可以忽略。

> checkpoint 文件约 591 MB ≈ 49.3M × 4 B × 3，是因为除了参数本身，还保存了 Adam 的两组动量。

#### （2）表达能力的差别

- **单头注意力每个位置只能输出一个注意力分布**，得到的是 value 的一个凸组合。如果一个词需要同时关注多个位置（句法上的中心词、对齐的源词、指代对象等），单头只能把权重分散，信息会被平均掉。多头可以在 8 个子空间里分别关注不同位置，再由 $W^O$ 组合起来。
- **单头的 $d_k=512$**，只有一种相似度度量；8 头相当于用 8 种秩为 64 的相似度度量组合。
- **数值稳定性也会变差**：$d_k$ 越大，点积 $q\cdot k$ 的方差越大。代码是先用 fp16 计算 $QK^\top$，再乘以 $1/\sqrt{d_k}$，所以单头时缩放前的数值更容易溢出。

#### （3）实验验证

两种头数在完全相同的配置下各训练 15 个 epoch：

![图 3-1 heads 8 vs 1](figs/loss_heads.png)

| 配置 | 结果 | 测试 BLEU（beam=4） |
|---|---|---|
| heads=8（base，lr×1.0） | 正常收敛，最后一个 epoch 平均 loss 3.385 | 4.58 |
| heads=1，lr×1.0 | **第 1296 步（学习率峰值附近）出现 NaN**，之后全部是 NaN，输出为 40 个相同的 token | 0.00 |
| heads=1，lr×0.5 | 正常收敛，最后一个 epoch 平均 loss 3.252 | 6.70 |

**结论**：单头的参数量与 8 头完全相同，但在相同学习率下更容易数值发散（与上面第 3 点的分析一致）。把学习率减半后单头可以正常训练，但它和 8 头基线所用的学习率不同，所以这组 BLEU 不能直接比较头数的影响。在本实验的基线流程下，模型质量主要受 3.6 节所述的训练问题限制，头数带来的差异被这些问题掩盖了。

### 3.4 模型训练

#### （1）notebook 基线训练

先调用 `create_dynamic_lr` 画出学习率曲线（Cell 18），再执行 `train(train_cfg)`（Cell 19）：

![图 3-2 notebook 中的学习率曲线](figs/nb_lr_plot.png)

<screenshot>notebook Cell 19 输出的开头（step 1 loss≈9.80）和结尾（epoch 15 step 8850 loss≈5.09，“Train epoch time: 23226 ms, per step time: 39.367 ms”）</screenshot>

<screenshot>checkpoint/ 目录：transformer-32_40-14_590.ckpt、transformer-32_40-15_590.ckpt（各约 564MB）以及 graph.meta</screenshot>

![图 3-3 基线 loss 曲线](figs/base_loss.png)

| epoch | 1 | 2 | 3 | 5 | 8 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|
| 平均 loss | 5.544 | 4.356 | 4.012 | 3.770 | 3.649 | 3.567 | 3.514 | 3.455 |

loss 从 9.80 开始（约为 $\ln 10067=9.22$），第 1 个 epoch 平均降到 5.54，之后下降变慢，到第 15 个 epoch 平均为 3.455，**还没有收敛**。

**loss 呈锯齿形**：每个 epoch 内的 loss 都是先低后高，放大最后 3 个 epoch 可以看得很清楚：

![图 3-4 锯齿形 loss](figs/base_sawtooth.png)

每个 epoch 开始时 loss 约 2.9，结束时升到 4.5–5.0，进入下一个 epoch 后又突然回落。原因是**训练数据没有打乱，而语料大致按句子长度排序**（见 2.3（3）第 5 点）：每个 epoch 都是先训练短句（容易，loss 低），再训练长句（难，loss 高）。所以 notebook 最后打印的 `loss=5.09` 只是最长那批句子的 loss，不能代表模型的整体水平。

#### （2）`learning_rate` 探索

学习率常数项分别取 ×0.5、×1.0（notebook 默认）、×2.0，其他设置与 notebook 相同：

![图 3-5 学习率对比](figs/loss_lr.png)

| 学习率倍率 | 峰值 lr | 最后一个 epoch 平均 loss | 测试 BLEU（beam=4） | 重复率 |
|---|---|---|---|---|
| ×0.5 | 0.78e-3 | **2.130** | **19.25** | 8.2% |
| ×1.0（base） | 1.56e-3 | 3.385 | 4.58 | 8.2% |
| ×2.0 | 3.12e-3 | 第 1220 步出现 NaN | 0.00 | 100% |

**结论**：在这个任务上，notebook 默认的学习率**偏大**。×2.0 在 warmup 刚结束时就数值发散了；×1.0 虽然没有发散，但长期停在较高的 loss；减半后 loss 明显更低，BLEU 从 4.6 提高到 19.3。原因在于 warmup 只有 800 步，比原论文的 4000 步短得多，学习率在模型还很不稳定的阶段就到达了峰值。而且本实验使用 fp16 计算且没有开启 loss scale，对过大的学习率更敏感。

#### （3）`batch_size` 探索

保持学习率调度不变（warmup 和 decay 按步数计），比较 batch_size 为 16、32、64：

![图 3-6 batch_size 对比](figs/loss_bs.png)

| batch_size | 每 epoch 步数 | 训练耗时 | 最后一个 epoch 平均 loss | 测试 BLEU（beam=4） |
|---|---|---|---|---|
| 16 | 1180 | 659 s | 3.561 | 2.44 |
| 32（base） | 590 | 422 s | 3.385 | 4.58 |
| 64 | 295 | 285 s | 3.450 | 6.32 |

**结论**：batch 越大，梯度噪声越小，相当于降低了“有效学习率”，所以 BLEU 随 batch 增大而上升，与 3.4（2）中“学习率偏大”的结论一致。bs=64 每个 epoch 只需 295 步，训练耗时仅为 bs=16 的 43%，说明 NPU 的并行能力在大 batch 下能更好地发挥。不过这三组的 BLEU 都还很低，整体上仍受 3.6 节所述的训练问题限制。

### 3.5 模型推理

#### （1）notebook 基线推理结果

执行 `evaluate(eval_cfg)`（Cell 23）。Beam Search 图第一次编译约需 4–8 分钟（输出中的一串 `.`），编译完成后，4,704 条测试句很快就推理完了。

<screenshot>notebook Cell 23 输出末尾的几组 source/result（“Tom came to the conclusion ...” 等长句）</screenshot>

notebook 的输出只有译文，没有量化指标。我用 `score_tsv.py` 计算了以下指标：

| 指标 | 数值 |
|---|---|
| 字符级 BLEU-4 | **4.43** |
| BLEU-1 / BLEU-2 | 21.94 / 12.16 |
| 平均译文长度 / 参考长度（字） | 16.2 / 9.7 |
| 重复率 | 12.8% |
| 与参考完全一致 | 4 / 4704 |

能翻对的例子：`Please give me a glass of water .` → `请给我一杯水。`、`Tom looks very happy .` → `汤姆看起来非常开心。`（都与参考完全一致）。但大部分短句的译文与源句无关，例如 `Hi .` → `你最好立刻去医院。`，`Really ?` → `我在2000000…`。

#### （2）Greedy 与 Beam Search

对 notebook 基线和 3.6 节中效果最好的模型，分别用不同的 `beam_width` 在整个测试集上推理：

![图 3-7 beam_width 对比](figs/beam_sweep.png)

| 模型 | beam | BLEU | 平均译文长度 | 重复率 | ms/句（编译后） | 首次编译耗时 |
|---|---|---|---|---|---|---|
| notebook 基线 | 2 | 4.23 | 17.2 | 11.0% | 3.3 | 312 s |
| notebook 基线 | 4 | 4.43 | 16.2 | 12.8% | 4.6 | 235 s |
| notebook 基线 | 8 | 4.49 | 15.9 | 14.8% | 7.5 | 518 s |
| fix30 | 2 | 17.19 | 8.6 | 1.8% | 3.4 | — |
| fix30 | 4 | **17.60** | 8.6 | 1.8% | 4.7 | — |
| fix30 | 8 | 17.34 | 9.0 | 3.2% | 7.6 | — |

> `beam_width=1`（Greedy）在当前的 MindSpore 2.7.2 + CANN 环境中运行时报算子错误（融合 kernel 访问 UB 地址时未对齐），没有得到结果。fix30 模型复用了已经编译好的图，所以首次耗时一栏为空。

**结论**：

- **耗时**：解码耗时随 beam 宽度近似线性增加（3.3 → 4.6 → 7.5 ms/句），首次编译的时间也会变长。
- **质量**：beam 从 2 增加到 4，BLEU 小幅提高（+0.2 到 +0.4）；从 4 增加到 8 基本没有提升（fix30 甚至略有下降），重复率反而上升。这与已有研究的经验一致：beam 太大时，模型更容易找到“概率高但质量差”的输出，即 beam search curse。
- 综合来看，`beam_width=4` 是质量和速度之间比较合理的折中。模型本身的好坏（BLEU 4.4 vs 17.6）对结果的影响远大于解码策略。

### 3.6 拓展探索：模型为什么没有用到源句，以及如何修复

3.5 节中的现象（译文与源句无关、长句的 BLEU 反而更高、大量重复）说明模型**在很大程度上退化成了一个中文语言模型**。我用 `exp.py diag` 做了诊断：在 teacher forcing 下分别输入**真实源句**、**batch 内打乱的源句**和**空源句**，比较 loss。如果 loss 差值很小，说明模型基本没有用到源句。

结合 2.3（3）的代码分析，我认为有两个原因：

1. **训练分支中交叉注意力的掩码有误**：目标位置 $t\ge$ 源句长度时，该位置完全看不到源句。这会影响 74.7% 的训练句对、20.5% 的目标位置。
2. **训练数据没有打乱**：每个 epoch 末尾集中训练长句。

针对这两点分别修复（`--shuffle`、`--fixmask`，后者对应 `FixedMaskModel`），并按控制变量的方式对照：

![图 3-8 修复对照](figs/loss_fix.png)

| 配置 | shuffle | 修复掩码 | epoch | lr 倍率 | 测试 BLEU | 1–5 词 | 6–10 | 11–15 | 16+ | 重复率 | 诊断 Δloss（测试集，打乱源句 − 真实源句） |
|---|---|---|---|---|---|---|---|---|---|---|---|
| notebook 基线 | ✗ | ✗ | 15 | 1.0 | 4.43 | 4.0 | 4.4 | 4.6 | 6.4 | 12.8% | 1.28 |
| base（复现） | ✗ | ✗ | 15 | 1.0 | 4.58 | 3.7 | 4.7 | 4.7 | 5.7 | 8.2% | 1.23 |
| fix_noshuf | ✗ | ✓ | 15 | 1.0 | 5.88 | 5.5 | 6.0 | 5.8 | 5.5 | 6.0% | — |
| shuffle | ✓ | ✗ | 15 | 1.0 | 8.45 | 11.5 | 8.1 | 5.4 | 4.4 | 7.0% | 1.60 |
| fix | ✓ | ✓ | 15 | 1.0 | 13.30 | 19.2 | 13.7 | 7.6 | 6.7 | 5.5% | 2.23 |
| fix30 | ✓ | ✓ | 30 | 1.0 | 17.60 | 26.1 | 18.1 | 9.8 | 8.6 | 1.8% | 2.79 |
| lr0.5 | ✗ | ✗ | 15 | 0.5 | 19.25 | 16.2 | 20.0 | 18.1 | 15.2 | 8.2% | 3.38 |
| **fix30_lr0.5** | ✓ | ✓ | 30 | 0.5 | **35.75** | **44.3** | **37.1** | **26.3** | **20.3** | **0.2%** | 3.35 |

**分析：**

1. **两项修复都有效，叠加后效果更明显**：只修复掩码，BLEU 从 4.6 提高到 5.9；只打乱数据，提高到 8.5；两者同时使用为 13.3，训练 30 个 epoch 后达到 17.6。诊断 Δloss 也从 1.23 增加到 2.79，说明模型越来越依赖源句。
2. **打乱数据后，各长度区间的 BLEU 恢复正常**：基线中长句的 BLEU 反而高于短句，这是不正常的；打乱后短句的 BLEU 最高（26.1），随长度增加而下降。原来的反常是因为每个 epoch 最后几百步只训练长句，模型偏向输出长句的分布，短句就译成了长而无关的句子（基线平均译文长度 16.2，参考只有 9.7）。
3. **学习率是影响最大的单一因素**：只把学习率减半，BLEU 就从 4.6 提高到 19.3。在此基础上再加上打乱数据、修复掩码、训练 30 个 epoch，**BLEU 达到 35.75，约为 notebook 基线的 8 倍**，重复率从 12.8% 降到 0.2%，平均译文长度（9.2）也接近参考长度（9.7）。
4. **训练集与测试集的差距**：在训练集的子集上，fix30 的 BLEU 为 38.3，基线只有 3.4。基线在训练集上同样很差，说明它的问题是**欠拟合或训练有误**，而不是过拟合。fix30 的训练集 BLEU（38.3）远高于测试集（17.6），说明修复后模型已经开始过拟合，这也和数据量只有 1.9 万句对相符。

**翻译样例对比**（测试集）：

| 源句 | 参考 | notebook 基线 | fix30_lr0.5 |
|---|---|---|---|
| Hi . | 嗨。 | 你最好立刻去医院。 | 嗨！ |
| I ' m OK . | 我没事。 | 我觉得我真的很难。 | 我好。 |
| I resign . | 我放弃。 | 我听到了一个小时的时候，但我被哭了。 | 我辞职了。 |
| Call me . | 联系我。 | 请让我看看看看看电话给我。 | 打电话给我。 |
| I learned to drive a car when I was eighteen and got a driver ' s license . | 我十八岁时，学了开车、考到了驾照。 | 我有一辆自行车。 | 我十八岁的时候开车，我到了驾驶执照。 |
| Tom thought that he had a chance to make a lot of money on the stock market . | 汤姆觉得他有机会在股市赚一大笔钱。 | 汤姆说他有很多钱。 | 汤姆认为他有很多钱在股市赚。 |

### 3.7 Bad Case 分析

我自己构造了几类句子（`exp/custom.txt`），比较 notebook 基线和效果最好的 fix30_lr0.5 模型（beam=4）的翻译：

| 类别 | 英文输入 | OOV | notebook 基线 | fix30_lr0.5 |
|---|---|---|---|---|
| 训练域短句 | I love you . | — | 我希望你能听到我的信息。 | **我爱你。** |
| 训练域短句 | Tom is my friend . | — | 汤姆是我最喜欢的朋友。 | **汤姆是我的朋友。** |
| 训练域短句 | Where is the station ? | — | 波士顿在波士顿有多少？ | **车站在哪里？** |
| 训练域短句 | I don't know what to do . | — | 我不知道怎么做的事。 | **我不知道要做什么。** |
| 长句 | Although it was raining heavily , we decided to go hiking in the mountains with our friends . | — | 在我们的朋友的时候，我们应该知道怎么做了。 | 虽然下得很大，我们决定在我们的朋友出去年轻。 |
| 长句 | If you had told me the truth earlier , I would not have made such a terrible mistake last year . | — | 我不知道如何时间，我不能做。 | 如果你告诉我真相，我就没有发生了。 |
| 歧义 | The bank is closed today . | — | 今天的时候，电话响了。 | **今天银行关门。** |
| 歧义 | He sat on the bank of the river . | — | 他在伦敦的时候，去世了。 | **他坐在河边。** |
| 歧义 | I saw her duck . | — | 我有足够的成功课堂。 | 我看见她是液体。 |
| 歧义/习语 | Time flies like an arrow . | — | 美国的人口有一个大的美国人。 | 时间喜欢爆炸。 |
| 专有名词 | I study at Zhejiang University in Hangzhou . | Zhejiang, Hangzhou | 我在2000000000…（重复到最大长度） | 我在泰国际年轻地读书。 |
| 专有名词 | My name is Zhang Wei . | Zhang, Wei | 我妹妹妹妹妹妹…（重复到最大长度） | 我的名字是黑色的名字。 |
| 专有名词 | Elon Musk founded SpaceX . | Elon, Musk, SpaceX | 他的父亲在澳大利亚长大。 | 土豆子反对垄断。 |
| 数字/时间 | The meeting starts at 3 pm on Monday . | pm | 努力地努力学习。 | 会议在星期一开始数三点半。 |
| 领域外 | The patient was diagnosed with pneumonia . | diagnosed, pneumonia | 美国是一个世界上最大的城市。 | 这个病人面被反对黑色。 |
| 领域外 | The GDP grew by 5 percent this quarter . | GDP | 这个工作是一个美国的。 | 贝尔奖队长大第一印象。 |

**分析：**

修复后的模型已经能正确翻译训练域的短句，`bank` 的两种含义（银行、河岸）也能根据上下文区分，说明交叉注意力确实用上了源句的信息。剩下的失败可以归为以下几类：

1. **OOV（未登录词）**：只要出现 `<unk>`，翻译基本都会失败。基线遇到 `<unk>` 后会陷入重复循环（“0 0 0…”“妹妹妹妹…”），一直生成到 40 步；修复后的模型不再重复，但会编造内容（Zhejiang → “泰国”，SpaceX → “垄断”）。原因是训练语料中没有 OOV，模型从没见过 `<unk>`。改进方法：用 BPE/WordPiece 等子词切分；训练时把部分低频词随机替换成 `<unk>`；对人名地名加入复制或音译机制。
2. **领域偏差**：语料是 Tatoeba 风格的日常短句，几乎没有医疗、经济类句子，所以 diagnosed、pneumonia、GDP 这类句子全部失败；基线还会套用训练集中的高频词（“波士顿”“美国”“澳大利亚”）。
3. **长句**：训练集平均只有 7.8 个英文词，16 个词以上的句子只占约 1%，所以长句的 BLEU 最低（20.3）。长句的典型错误是漏译从句或修饰语（“with our friends”“last year”），以及结构混乱（“我们决定在我们的朋友出去年轻”）。
4. **歧义与习语**：`I saw her duck` 存在句法歧义，`Time flies like an arrow` 是习语，都需要世界知识，小数据集上训练的模型做不到；而且本实验评测的是单句，没有上下文可以利用。
5. **数字和时间**：数字在词表中是逐个字符表示的（“3”），模型对数字的对齐能力弱，于是出现了“三点半”这样的幻觉。
6. **解码策略**：没有重复惩罚，也没有 `<unk>` 惩罚。可以在 `BeamSearchDecoder.one_step` 中，对已经出现过的 n-gram 和 `<unk>` 减去一个惩罚项。

### 3.8 实验总结

1. 在 Ascend 910B 和 MindSpore 2.7.2 上完整跑通了 Transformer 英译中的数据处理、训练和 Beam Search 推理流程。notebook 原始配置训练 15 个 epoch 约需 7 分钟，测试集字符级 BLEU 为 **4.43**，大量译文与源句无关。
2. **探索 1**：词表的行号就是 id，前三个是 `<unk>/<s>/</s>`；OOV 和 padding 的 id 都是 0。推理时的分词粒度必须和训练语料完全一致，否则正常的词也会变成 `<unk>`。
3. **思考题**：头数从 8 改为 1，参数量完全不变（49,257,984），因为 Q/K/V/O 投影的总宽度始终是 $d$。区别在于模型能表达的注意力模式和数值稳定性：单头在原学习率下第 1296 步就发散成 NaN，学习率减半后才能正常训练。
4. **训练探索**：notebook 默认的学习率偏大（×2 发散，×0.5 时 BLEU 从 4.6 提高到 19.3）；batch 越大越稳定（bs64 的 BLEU 为 6.3）。“先升后降”的学习率调度中，warmup 用于稳定 Adam 在初期的二阶矩估计，避免发散；衰减用于后期收敛。
5. **推理探索**：解码耗时随 beam 宽度近似线性增加。beam=4 比 beam=2 略好，beam=8 基本没有提升，重复率反而上升，beam=4 是比较合理的折中。
6. **拓展**：我找出了 notebook 和代码中两处导致模型退化为语言模型的问题：训练时交叉注意力的掩码有误，以及 `do_shuffle` 没有生效。修复这两处并把学习率减半、训练 30 个 epoch 后，**BLEU 从 4.43 提高到 35.75**，重复率从 12.8% 降到 0.2%，模型能正确翻译日常短句并区分一词多义。剩余的主要瓶颈是 OOV、领域偏差和长句，需要通过子词切分、扩充数据和改进解码策略来解决。
