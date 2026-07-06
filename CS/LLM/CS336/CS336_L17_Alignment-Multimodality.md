---
title: "Lecture 17: Alignment & Multimodality"
---

# Lecture 17: Alignment & Multimodality / 第十七讲：对齐与多模态

---

## 1. Introduction to Multimodal Models / 多模态模型简介

So far in this class, we have exclusively focused on language models. Language models are already pretty general—they give you the ability to go from any piece of text to any text, whether it be natural language, code, poetry, or even DNA. But the world is multimodal: you have text, images, audio, and video. The North Star of where we want to be is what people call an **omni model**—a model capable of taking any combination of these modalities and outputting any combination of them. For example, you could give it an image and a video, ask a question about both, and it could generate images in response. You could even convert audio into an image. There are countless applications enabled by an omni model.

到目前为止，本课程一直专注于语言模型。语言模型已经相当通用——它们能让你从任意一段文本生成任意文本，无论是自然语言、代码、诗歌，甚至DNA。但世界是多模态的：你有文本、图像、音频和视频。我们最终的目标是人们所说的**全模态模型**——一种能够接收任意模态组合并输出任意模态组合的模型。例如，你可以给它一张图片和一段视频，提问关于这两者的内容，它则能生成图片作为回答。你甚至可以把音频转换成图像。全模态模型使得无数应用成为可能。

How do you build such a thing? The reality is that transformers work really well across all these modalities. Despite best efforts to try other architectures, transformers remain at scale the best thing we have. Transformers were originally designed for text and thus have the property that they speak tokens—they take a bunch of tokens as input and output some tokens. Here, I'm expanding the notion of tokenization to include not just discrete tokens as we've seen in text, but also potentially continuous tokens. The key idea is that a token should represent some semantic unit of information. In natural language, tokens are subwords and are somewhat meaningful. A single pixel, by contrast, is certainly not meaningful by itself. So somehow we must convert everything—including audio and images—into either discrete or continuous tokens.

那么如何构建这样一个模型呢？现实是，Transformer在所有这些模态上都表现得非常好。尽管人们努力尝试其他架构，Transformer在大规模上仍然是我们最好的选择。Transformer最初是为文本设计的，因此它有一个特性，即它们 "说" 标记——它们接收一系列标记作为输入并输出一些标记。在这里，我扩展了分词的概念，使其不仅包括我们在文本中看到的离散标记，还包括潜在的连续标记。关键思想是，一个标记应该代表某种语义信息单元。在自然语言中，标记是子词，它们具有一定的意义。相比之下，单个像素本身显然是没有意义的。因此，我们必须以某种方式将一切——包括音频和图像——转换成离散或连续的标记。

We already encountered this even with text. In the first lecture, we talked about tokenization, using BPE tokenizers—you all implemented one, and it works fine. One could wish for a better tokenizer, but it's not the worst thing in the world. For non-text modalities, however, we have to think much harder about what the equivalent of a BPE tokenizer would be—something that takes an image and produces things a transformer can digest. So there are two questions: first, for non-text data like images, videos, or audio, how do you input these into the transformer? And second, how do you generate them out? This lecture will mostly focus on the first question.

即使在处理文本时，我们也会遇到这个问题。在第一讲中，我们讨论了分词，使用了BPE分词器——你们自己实现了一个，效果不错。人们可能希望拥有更好的分词器，但这并不是世界上最糟糕的事。然而，对于非文本模态，我们必须更加努力地思考，什么才是BPE分词器的等价物——能够接收一张图像并产生Transformer可以消化的东西。所以这里有两个问题：第一，对于图像、视频或音频等非文本数据，如何将它们输入到Transformer中？第二，如何从Transformer中生成它们？本讲将主要关注第一个问题。

---

## 2. CLIP: Contrastive Language Image Pre-Training / CLIP：对比语言图像预训练

Let's rewind the clock back to 2021. The CLIP model is foundational to modern **vision language models (VLMs)**. CLIP stands for Contrastive Language Image Pre-training. Around that time, GPT-3 and GPT-2 had already ushered language models into the foundation model era. In vision, however, the tradition was still based on large annotated datasets like ImageNet, training models such as ResNet with extensive data augmentation to get good performance. The researchers at OpenAI wondered: is it possible to leverage the large amount of image and textual captions out there? Inspired by the language domain where you could just scrape the internet for noisy text, train a large enough model, and make sense of it, they asked what the equivalent for images would be. CLIP was born.

让我们回到2021年。CLIP模型是现代**视觉语言模型(VLM)**的基础。CLIP代表对比语言图像预训练(Contrastive Language Image Pre-training)。那时，GPT-3和GPT-2已经将语言模型带入了基础模型时代。但在视觉领域，传统做法仍然基于大规模标注数据集（如ImageNet），训练ResNet等模型，并配合大量数据增强以获得良好性能。OpenAI的研究人员思考：是否可能利用互联网上大量的图像和文本描述？受语言领域的启发——你可以直接从互联网爬取嘈杂的文本，训练一个足够大的模型，并从中提取有用的东西——他们问，这对图像来说等价的做法是什么？于是，CLIP诞生了。

The idea of CLIP is fairly straightforward. Suppose you have a bunch of **image-text pairs**, say 32,000 of them. For each image, you encode it using an image encoder into a vector, giving you image encodings I₁ through Iₙ. You do the same for the corresponding text, giving you text embeddings T₁ through Tₙ. The objective is that for a given image I₁ that is aligned with T₁, the dot product between these two embeddings should be much larger than the dot product between I₁ and all other text embeddings. Conversely, for text T₁, its dot product with I₁ should be larger than its dot product with all other images. This is essentially 2×N different softmax classification problems—it's a multi-class classification problem structured in an N×N matrix form.

CLIP的思想相当直接。假设你有一批**图文对**，比如32,000对。对于每张图像，你使用图像编码器将其编码为一个向量，得到图像编码I₁到Iₙ。对相应的文本也做同样处理，得到文本嵌入T₁到Tₙ。目标设定为：对于与T₁对齐的图像I₁，这两个嵌入之间的点积应远大于I₁与所有其他文本嵌入的点积。反之，对于文本T₁，它与I₁的点积应大于它与所有其他图像的点积。这本质上是2×N个不同的softmax分类问题——一个以N×N矩阵形式结构化的多类分类问题。

Where does the data come from? The CLIP paper is somewhat sparse on data details. Roughly, they took a bunch of search queries, mined image-text pairs from the web, resulting in 400 million image-text pairs. While the dataset wasn't released, a later effort called OpenCLIP replicated and extended the CLIP ideas, releasing the LAION-5B dataset with 5 billion images and textual descriptions. Interestingly, they actually used CLIP for data filtering and then trained OpenCLIP—a bootstrapping approach. OpenCLIP is a model where you can point to both the training dataset and the code.

数据从哪里来？CLIP论文对数据细节描述不多。大致做法是：获取一批搜索查询词，从网上挖掘图文对，最终得到了4亿个图文对。虽然该数据集没有公开发布，但后来的OpenCLIP工作复现并扩展了CLIP的思想，发布了包含50亿张图像及文本描述的LAION-5B数据集。有趣的是，他们实际上先用CLIP做数据过滤，再训练OpenCLIP——这是一种自举(bootstrapping)方法。OpenCLIP是一个你可以同时追溯到其训练数据和代码的模型。

Images come in all sorts of resolutions. Neural networks don't like things to be dynamic—they want fixed-size inputs. So a heuristic processing step happens: they resize the image so the shorter side is 336 pixels (or 224), and then center-crop to get a square. This is for convenience; later we'll see better approaches. Also, at the time, the CLIP authors were thinking about ImageNet classification, where the object is usually in the middle and you're just trimming off background, so this cropping doesn't matter too much.

图像的分辨率千差万别。神经网络不喜欢动态的东西——它们希望输入是固定大小的。因此进行了一个启发式的预处理步骤：将图像缩放，使短边为336像素（或224像素），然后中心裁剪为正方形。这是为了方便；后面我们会看到更好的方法。此外，当时CLIP的作者主要考虑的是ImageNet分类，其中物体通常在图像中央，裁剪只是去掉背景，因此这种裁剪影响不大。

### The Vision Encoder: ViT / 视觉编码器：ViT

What is the vision encoder CLIP uses? They experimented with ResNets and **vision transformers (ViTs)**, which had just come out. They found that **ViTs** performed best, so when people say "CLIP" they usually mean the **ViT** version. A vision transformer works as follows: you take an image and break it up into **patches** (the original ViT paper used 16×16 patches, CLIP used 14×14). Each patch is a vector—in some sense a token for the vision transformer. You add positional embeddings just as you would for a language model, and then pass everything through a standard transformer encoder. To get a single vector from the sequence, CLIP uses attention pooling: you take the global average of all activations, then do another round of attention with that query against the keys and values of each position, yielding a more informed vector than a straight average. The CLIP paper found that the best model was ViT-L/14—a large ViT with 24 layers, 14×14 patches, each patch having 3 RGB channels, trained on 336×336 resolution images.

CLIP使用的视觉编码器是什么？他们实验了ResNet和刚问世的**视觉Transformer(ViT)**。他们发现**ViT**表现最好，所以当人们提到"CLIP"时，通常指的是**ViT**版本。视觉Transformer的工作原理如下：将一张图像分割成若干**补丁**（原始ViT论文使用16×16补丁，CLIP使用14×14）。每个补丁是一个向量——在某种意义上，是视觉Transformer的一个标记。就像训练语言模型那样，你添加位置嵌入，然后将所有内容通过一个标准的Transformer编码器。要从序列中得到单个向量，CLIP使用注意力池化(attention pooling)：取所有激活的全局平均值，然后用该平均值作为query，对每个位置的key和value再做一轮注意力计算，得到一个比直接平均更丰富的向量。CLIP论文发现最好的模型是ViT-L/14——一个大型ViT，约24层，14×14补丁，每个补丁有3个RGB通道，在336×336分辨率图像上训练。

### The Text Encoder / 文本编码器

The text encoder is a standard GPT-2 style transformer. To get a single vector out of a sequence, they prepended a BOS token and appended an EOS token, then took the activation of the EOS token at the highest layer as the representation of the whole sequence. So you have a vision encoder, a text encoder, and you train by picking a batch, encoding all texts and images, forming two cross-entropy losses, and optimizing from there.

文本编码器是一个标准的GPT-2风格Transformer。为了从序列中获得单个向量，他们在序列开头添加BOS标记、末尾添加EOS标记，然后取最高层EOS标记的激活值作为整个序列的表示。于是，你有视觉编码器，有文本编码器，训练过程是：选取一个批次，编码所有文本和图像，构建两个交叉熵损失，然后进行优化。

### The Headline Result / 标志性结果

The headline result that got people excited about CLIP in 2021 was that on the ImageNet benchmark, zero-shot CLIP outperformed a ResNet trained on 1.2 million ImageNet images. Those 1.2 million images represented many, many hours of Amazon Mechanical Turk annotation labor. Now, CLIP was trained on more organic web data—still the labor of web users, but if you can leverage existing data, you can do it zero-shot. The zero-shot technique is simply: take an image, compute dot products with various label texts, and see which is highest.

CLIP在2021年引起轰动的标志性结果是：在ImageNet基准测试上，零样本(zero-shot) CLIP的表现优于在120万张ImageNet图像上训练的ResNet。那120万张图像代表了Amazon Mechanical Turk众包工人大量的标注劳动时间。而CLIP是在更有机的互联网数据上训练的——仍然是网络用户的劳动，但如果你能利用已有的数据，就可以零样本地完成任务。零样本的方法很简单：给定一张图像，计算与各标签文本的点积，看哪个最高。

It is worth noting that the design decisions in CLIP are based on image classification—so it's not very fine-grained. Yet, as we'll see, it serves as a robust starting point for everything we'll do later. One technical downside is that CLIP requires large batch sizes (around 32,000). With a batch size of 1 or even 10, it doesn't work because the softmax operates over the full batch, making it not very decomposable in contrast to normal language model training where sequences parallelize independently.

值得注意的是，CLIP的设计决策基于图像分类——因此它的粒度不细。但正如我们将看到的，它仍然是我们后续一切工作的坚实基础。CLIP的一个技术缺点是它需要大批量大小（约32,000）。如果批量大小为1甚至10，它就不起作用，因为softmax在整个批次上操作，使其不太可分解，与正常语言模型训练中序列可以独立并行化形成对比。

---

## 3. SigLIP: Improved Contrastive Learning / SigLIP：改进的对比学习

This batch-size issue was addressed by a paper from Google called SigLIP—Sigmoid Loss for Language Image Pre-training. Think of it as an improved version of CLIP. The main difference is that CLIP does multi-class classification: it says "this aligned text-image pair is positive against all other alternatives." SigLIP is a lot simpler—for any given image-text pair, it simply asks: are they aligned or not? It's binary classification where the diagonal entries are positive examples and off-diagonal entries are negative. You take embeddings, normalize, take dot products as usual, form labels (−1 off-diagonal, +1 on diagonal), and apply log_sigmoid loss. The objective is very simple.

Google发表的SigLIP论文解决了批量大小的问题——SigLIP代表Sigmoid Loss for Language Image Pre-training（基于Sigmoid损失的语言图像预训练）。可以把它看作CLIP的改进版。主要区别在于：CLIP做的是多类分类——它说"这个对齐的图文对相对于所有其他替代项是正例"。SigLIP则简单得多——对于任意给定的图文对，它只问：它们对齐了吗？这是二分类，对角线上是正例，非对角线是负例。取嵌入，归一化，如常取点积，构造标签（非对角线为-1，对角线为+1），然后应用log_sigmoid损失。目标函数非常简单。

SigLIP was much more efficient to train. CLIP was trained for 10 days on 256 TPUv3, while SigLIP took 5 days on 32 TPUv4. In terms of raw FLOPS, v4 isn't actually faster than v3—it's better because you can put more of them in a pod with better interconnect—but at this scale it's actually about 60% slower. The efficiency gain came from better parallelization. Each device stores a subset of image-text pairs and computes losses locally; then text embeddings are rotated among devices to cover all off-diagonal block entries. This is like DDP but with interaction between examples.

SigLIP的训练效率远高于CLIP。CLIP在256个TPUv3上训练了10天，而SigLIP在32个TPUv4上训练了5天。就原始FLOPS而言，v4实际上并不比v3更快——v4的优势在于可以在一个pod中放更多芯片，互连更好——但在这种规模下，它实际上慢了约60%。效率提升来自于更好的并行化。每个设备存储一组图文对并本地计算损失；然后文本嵌入在设备间轮转以覆盖所有非对角块条目。这类似于DDP，但涉及样本之间的交互。

Another advantage of SigLIP is that it effectively decouples batch size from the loss function. In CLIP, if you change the batch size, it's a different loss function. SigLIP allows experimenting with much smaller batch sizes (less than 16K), where it's much better than CLIP—CLIP's loss function degrades with too small a batch, whereas SigLIP's loss just has more variance but is the same in expectation. They found that 32K was essentially their critical batch size.

SigLIP的另一个优势是它有效地将批量大小与损失函数解耦了。在CLIP中，如果改变批量大小，就变成了不同的损失函数。SigLIP允许使用小得多的批量大小（低于16K），在这个范围内它远优于CLIP——CLIP的损失函数在批量太小时会退化，而SigLIP的损失只是方差更大，期望值相同。他们发现32K基本上就是其关键批量大小。

So now we have CLIP and SigLIP—image encoders that take a fixed-size image (e.g., 336×336) and map it into a vector containing semantic information. Now let's build **VLMs (Vision Language Models)** on top of them.

所以现在我们有了CLIP和SigLIP——将固定大小图像（如336×336）映射为包含语义信息的向量的图像编码器。接下来，让我们在此基础上构建**视觉语言模型(VLM)**。

---

## 4. Vision Language Models: LLaVA / 视觉语言模型：LLaVA

I'll talk about two families of models: LLaVA and Qwen. They are very similar in broad template with some different details. The basic idea is to take the embeddings from a vision encoder and inject them directly into a language model. This is more of a mid-training or post-training approach—take an existing image encoder, an existing LLM, and stitch them together rather than training from scratch.

我将讨论两个模型系列：LLaVA和Qwen。它们在总体框架上非常相似，但在细节上有所不同。基本思想是取视觉编码器产生的嵌入，然后将其直接注入语言模型。这更像是一种中期训练(mid-training)或后训练(post-training)方法——取一个已有的图像编码器和一个已有的大语言模型(LLM)，把它们缝合在一起，而不是从头开始训练。

The LLaVA paper came out in 2023 and got people excited because around that time, closed models like GPT-4 were able to do visual reasoning, and LLaVA showed that open models could do some visual reasoning too. It wasn't as good as GPT-4, but people could see what went under the hood.

LLaVA论文发表于2023年，引起了人们的兴奋，因为那时GPT-4等闭源模型已经能够进行视觉推理，而LLaVA展示了开源模型也能做视觉推理。它不如GPT-4那么好，但人们可以一窥其内部工作机制。

Here are the pieces of a VLM: there's the **vision encoder** (they used CLIP), and for the text decoder they used a language model called Vicuna—a LLaMA model fine-tuned on ShareGPT conversations (conversations people had with ChatGPT and shared online). The data they used was based on MS COCO, an annotated dataset where Mechanical Turk workers annotated images with bounding boxes and captions. They synthesized a training dataset by prompting GPT-4 with the captions or detected objects to generate questions, conversations, detailed descriptions, and complex reasoning examples. This resulted in 158,000 synthesized examples.

VLM的几个组成部分：有**视觉编码器**（他们使用了CLIP），文本解码器则使用了一个称为Vicuna的语言模型——一个在ShareGPT对话（人们与ChatGPT的对话并分享到网上）上微调的LLaMA模型。他们使用的数据基于MS COCO，一个由Mechanical Turk工作者用边界框和描述标注图像的数据集。他们通过将标注标题或检测到的物体输入GPT-4，生成问题、对话、详细描述和复杂推理示例，合成了一个训练数据集，共计158,000个示例。

The model architecture works as follows. You take images, send them through the CLIP vision encoder, which gives you a vector. But this vector isn't really in the same space as the text embeddings. So you multiply by a matrix W (the **projector**) to get another vector that is in the same space as the text embeddings. For text, you just use the standard embeddings to get vectors. So what's happening is that the text gets encoded into vectors, and the image also gets encoded into vectors, and then this whole sequence of vectors goes through a standard transformer. We're in some sense converting images into textual tokens, leveraging the pre-trained language model.

模型架构如下：取图像，通过CLIP视觉编码器得到一个向量。但这个向量并不真正与文本嵌入处于同一空间。于是，你乘上一个矩阵W（**投影器**）得到另一个与文本嵌入同空间的向量。对于文本，只需使用标准嵌入得到向量。因此，文本被编码成向量，图像也被编码成向量，然后这整个向量序列通过标准的Transformer。从某种意义上说，我们将图像转换成了文本标记，从而利用预训练的语言模型。

Training happens in two stages. In the first stage (the alignment phase), they freeze both the vision encoder and the language model, and only train the matrix W. The goal is to make image embeddings look like natural language token embeddings. In the second stage, they still freeze the vision encoder but now train both W and the language model—fine-tuning the language model on their image+text-to-text data.

训练分两个阶段进行。第一阶段（对齐阶段），冻结视觉编码器和语言模型，只训练矩阵W。目标是使图像嵌入看起来像自然语言标记嵌入。第二阶段，仍然冻结视觉编码器，但现在训练W和语言模型——在其图像+文本到文本的数据上微调语言模型。

---

## 5. LLaVA OneVision / LLaVA OneVision

Skipping forward to 2024, LLaVA OneVision captures a sequence of innovations from LLaVA 1.5 and LLaVA-Next. The core recipe is the same, but they try to be more ambitious about the types of multimodal applications, handling multiple images and videos. The vision encoder is upgraded to SigLIP; the text decoder uses Qwen-2 (the best open language model at that time); and the **projector** is upgraded from a linear projection to a two-layer MLP. It's the same rough system with upgraded parts.

快进到2024年，LLaVA OneVision汇集了LLaVA 1.5和LLaVA-Next的一系列创新。核心配方相同，但他们在多模态应用的类型上更有野心，能够处理多张图像和视频。视觉编码器升级为SigLIP；文本解码器使用当时最好的开源语言模型Qwen-2；**投影器**从线性投影升级为两层MLP。大体系统相同，只是部件升级了。

One key innovation is OCR (optical character recognition). OCR requires preserving very fine-grained information—otherwise a J looks like an I. CLIP resizes and crops to 336×336, which clearly means you can't read a document. Their solution is an idea called AnyRes (introduced in LLaVA 1.5): you break up an image into multiple pieces, each at the resolution the vision encoder expects, encode all pieces, and concatenate the vectors. If you have super high-resolution images or videos with too many tokens, you downsample. The idea is adaptive—transformers already handle variable-length sequences well, so images can be any resolution, picking up on that same dynamic ability.

一个关键的创新是OCR（光学字符识别）。OCR需要保留非常细粒度的信息——否则J看起来像I。CLIP将图像缩放裁剪至336×336，这显然意味着你无法读取文档。他们的解决方案是一种叫AnyRes的想法（由LLaVA 1.5引入）：将图像分割成多个块，每块都是视觉编码器期望的分辨率，编码所有块，然后拼接向量。如果遇到极高分辨率图像或视频导致标记过多，则进行下采样。这个想法是自适应的——Transformer已经能很好地处理变长序列，因此图像可以是任意分辨率，利用了这一动态能力。

For training data, their approach is to curate high-quality, very task-targeted data—visual question answering, questions about tables, charts, etc. This is definitely post-training territory: you want your model to do specific tasks, so you create data for those tasks. This work also unabashedly uses distillation from GPT-4 to get the best performance. One interesting finding is transfer between modalities: even though they only had single-image data for diagrams and charts, this generalizes to multiple images. At training time, you never saw a table and a chart together with questions, but at test time you can have both and hold a conversation about them. Similarly, visual prompting (circling a part of an image) trained only on single images generalizes to videos. So even though it looks like supervised learning targeting each task, with enough tasks, these models do some transfer.

对于训练数据，他们的方法是精心策划高质量、任务导向的数据——视觉问答、关于表格和图表的问题等。这绝对是后训练领域：你希望模型完成特定任务，因此为这些任务创建数据。这项工作也毫不掩饰地使用GPT-4进行知识蒸馏以获得最佳性能。一个有趣的发现是模态间的迁移：尽管他们只有单张图像的图表数据，但这能泛化到多张图像。训练时，你从未见过一张表和一张图放在一起提问，但测试时你可以同时有两张图并进行对话。类似地，视觉提示（圈出图像的一部分）仅在单张图像上训练也能泛化到视频。因此，尽管看起来像是针对每个任务的有监督学习，但在足够多的任务下，这些模型确实能产生一些迁移。

The LLaVA series is one of the few works that open-sources not just model weights but also the data, so you can really replicate and study this stuff.

LLaVA系列是少数不仅开源模型权重还开源数据的工作之一，因此你可以真正复现和研究这些东西。

---

## 6. Qwen-VL Models / Qwen-VL系列模型

Qwen also started training multimodal models in 2023 with Qwen-VL. The pattern should be familiar by now. For the vision encoder, they used OpenCLIP (the open reproduction of CLIP). For the adapter, they used one layer of cross-attention with 2D positional embeddings, mapping to a fixed size of 256. They also introduced special tokens for image tags, bounding box tags, and reference tags. Training has three stages: stage 1 is large-scale, low-quality data where the language model is frozen and the vision encoder and adapter are trained (a bit different from LLaVA, which freezes the vision encoder). Stage 2 uses higher-quality task-specific data with all parameters trained. Stage 3 is instruction tuning where the vision encoder is frozen and the adapter and language model are trained.

Qwen于2023年也开始训练多模态模型，即Qwen-VL。模式现在应该已经熟悉了。视觉编码器方面，他们使用了OpenCLIP（CLIP的开源复现版）。适配器方面，他们使用了一层交叉注意力，配合2D位置嵌入，映射到固定大小256。他们还引入了图像标记、边界框标记和描述标记等特殊标记。训练分为三个阶段：阶段一是大规模低质量数据，冻结语言模型，训练视觉编码器和适配器（与LLaVA冻结视觉编码器稍有不同）。阶段二使用更高质量的特定任务数据，训练所有参数。阶段三是指令微调，冻结视觉编码器，训练适配器和语言模型。

Qwen-2 brought several upgrades: a larger vision encoder, dynamic resolution (the main thing—when you go to video, you clearly need dynamic resolution), and a new positional encoding scheme called multimodal RoPE (M-RoPE). Recall that RoPE ensures the inner product between vectors depends only on distance, where distance is defined in 1D by token positions. M-RoPE extends this to 3D: height, width, and time. Each patch now has a triple defining its coordinates, and RoPE is computed per dimension and concatenated. The model uses 2D compression (every 2×2 patches compressed to 1), so each patch ultimately generates 66 tokens. For videos, they sample 2 frames per second, maxing out at 16,000 tokens.

Qwen-2带来了几项升级：更大的视觉编码器、动态分辨率（这是重点——当你做视频时，显然需要动态分辨率），以及一种称为多模态RoPE(M-RoPE)的新位置编码方案。回顾一下，RoPE确保向量之间的内积仅依赖于距离，距离在1D中由标记位置定义。M-RoPE将其扩展到3D：高度、宽度和时间。每个补丁现在有一个三元组定义其坐标，RoPE在每个维度上计算并拼接。模型使用2D压缩（每2×2补丁压缩为1个），因此每个补丁最终生成66个标记。对于视频，每秒采样2帧，最多16000个标记。

---

## 7. Qwen-3-VL / Qwen-3-VL

Qwen-3-VL, from last year's report, is roughly the same diagram with changes that impact model quality. They use Qwen-3 models as the language model base—a series of dense and MoE models that are really good, and this substantially helps final quality. They are heavily invested in long context understanding, with context length going up to 256K, which is critical for long videos.

Qwen-3-VL来自于去年的报告，总体框架大致相同，但有一些影响模型质量的改进。他们使用Qwen-3模型作为语言模型基础——一系列密集模型和MoE模型，这些模型质量很高，极大地提升了最终模型的质量。他们大力投资长上下文理解，上下文长度可达256K，这对长视频至关重要。

For the vision encoder, they use SigLIP-2—an improved version of SigLIP with identical architecture, designed to be backward-compatible. They improved M-RoPE by interleaving the dimensions. The problem before was that dimensions were allocated in blocks: first block for time, next for width, next for height. Since each RoPE component represents a different frequency, this meant all temporal dimensions might be low-frequency and all spatial dimensions high-frequency. By interleaving, all axes are exposed to both low and high frequencies. They also made video timestamps explicit instead of being implicit in positional encodings. Now, there are literal tokens like "0 seconds" that represent time, which is helpful because you can directly refer to events like "what happened after two seconds."

视觉编码器方面，他们使用SigLIP-2——SigLIP的改进版，架构相同，设计为向后兼容。他们改进了M-RoPE，将维度交错排列。之前的问题是维度以块分配：第一块用于时间，下一块用于宽度，再下一块用于高度。由于每个RoPE分量代表不同频率，这意味着所有时间维度可能是低频的，所有空间维度则是高频的。通过交错，所有轴都能接触到低频和高频信息。他们还使视频时间戳变为显式的，而非隐含在位置编码中。现在，有像"0秒"这样的字面标记来表示时间，这很有帮助，因为你可以直接引用诸如"两秒后发生了什么"的事件。

They also introduced square-root normalized per-token loss to prevent video examples from dominating—since videos are very long and single images are very short, normal token-level averaging would let videos dominate the loss. Each example is normalized by the square root of its length. For the adapter, they use a more sophisticated approach (DeepStack from the DeepSeek team), which does a deeper fusion of the vision encoder into the residual stream of the language model, rather than treating the vision encoder as a black box outputting a sequence of vectors.

他们还引入了平方根归一化的每标记损失，以防止视频示例主导训练——由于视频很长而单张图像很短，正常的标记级平均会让视频主导损失。每个示例按其长度的平方根进行归一化。适配器方面，他们使用了更复杂的方法（DeepSeek团队的DeepStack），将视觉编码器更深层地融合到语言模型的残差流中，而不是将视觉编码器当作输出向量序列的黑盒。

Training has become quite complicated: pre-training has four stages (first train the adapter, then three stages progressively training on longer sequences from 8K to 32K to 256K, with most tokens in stages 2 and 3). Post-training has three stages: SFT on long chain-of-thought data, knowledge distillation, and reinforcement learning. At this point it's really a systems paper. But looking at the final benchmarks, Qwen-3-VL is a very strong model—its bold numbers (best in row) compare favorably against closed models like Gemini, GPT-5, and Opus 4.1.

训练已变得相当复杂：预训练有四个阶段（首先训练适配器，然后三个阶段逐步在更长的序列上训练，从8K到32K到256K，大部分标记在阶段2和3）。后训练有三个阶段：在长思维链数据上的SFT、知识蒸馏、以及强化学习。到了这一步，这实际上是一篇系统工程论文了。但看一下最终基准测试结果，Qwen-3-VL是一个很强的模型——其粗体数字（行内最佳）与Gemini、GPT-5和Opus 4.1等闭源模型相比毫不逊色。

---

## 8. Chameleon: Mapping Everything to Discrete Tokens / Chameleon：将一切映射为离散标记

So far, VLMs encode images into vectors and inject them into a language model. Because it's a language model, you can only generate text—you can't generate images. The Chameleon paper from Meta (2024) asks: what if we mapped everything into discrete tokens? Aesthetically, this is appealing because now you can analyze and generate images in the same way—everything is a discrete token. You can prompt with "I'm bored. Can you show me some birds?" and then the output would be text, then images, then more text and more images—interleaved. In this vision of an omni model, text and images truly live in the same space, accomplished by making everything look like text.

到目前为止，VLM将图像编码为向量并注入语言模型。因为是语言模型，你只能生成文本——不能生成图像。Meta的Chameleon论文(2024)提出了一个问题：如果我们将一切映射为离散标记会怎样？从美学上讲，这很有吸引力，因为现在你可以以同样的方式分析和生成图像——一切都是离散标记。你可以提示"I'm bored. Can you show me some birds?（我很无聊。你能给我看些鸟吗？）"，然后输出将是文本、图像、更多文本和更多图像——交错排列。在这种全模态模型的愿景中，文本和图像真正生活在同一空间里，通过让一切都看起来像文本来实现。

The technical challenge is mapping images into discrete tokens. This uses an older idea from van den Oord (2017) called vector quantized variational autoencoder (VQ-VAE). The idea is to learn a mapping that encodes an image into a continuous vector, then rounds it to the nearest code in a codebook of, say, 8,000 codes—prototypical vectors corresponding to patches. The decoder takes that code and tries to reconstruct the image. You train VQ-VAEs by minimizing reconstruction loss (with additional terms for differentiability). At the end, a 512×512 image is converted into 1,024 tokens, each from a vocabulary of 8,000. So now you essentially have text-like tokens for images, and training becomes straightforward—normal language model training, no adapter, no separate vision encoder. Just one language model.

技术挑战在于将图像映射为离散标记。这使用了一个较老的思想，来自van den Oord(2017)，称为向量量化变分自编码器(VQ-VAE)。其思想是学习一个映射：将图像编码成连续向量，然后四舍五入到码书（比如8,000个码）中最近的码——这些码是对应于补丁的原型向量。解码器接收该码并尝试重构图像。通过最小化重构损失来训练VQ-VAE（加上处理不可微性的额外项）。最终，一张512×512的图像被转换为1,024个标记，每个标记来自8,000的词汇表。所以现在你基本上有了类似文本标记的图像表示，训练变得简单——普通的语言模型训练，没有适配器，没有单独的视觉编码器。只有一个语言模型。

While elegant, there are problems. Training was found to be unstable because text and images, despite occupying the same space, behave very differently. Text tokens have relatively low entropy (most words are predictable), whereas image tokens have very high entropy (you don't know the exact shade of blue the next token will be). This led to parameter norms growing and loss instability. They mitigated this with QK norm and z-loss regularization. Furthermore, this model was not as performant—discretization definitely loses information (think about OCR on very small print). VQ-VAEs were popular for a while, and many used them for image generation, but then **diffusion models** came out and became viable for generation, making this flavor of method less popular.

尽管优雅，但存在问题。训练被发现不稳定，因为文本和图像尽管占据同一空间，但行为非常不同。文本标记具有相对较低的熵（大多数字词是可预测的），而图像标记具有非常高的熵（你不知道下一个标记的确切蓝色色调是什么）。这导致参数范数增长和损失不稳定性。他们通过QK norm和z-loss正则化来缓解。此外，该模型的性能不够好——离散化肯定丢失了信息（想想在极小字体上做OCR）。VQ-VAE曾流行一阵，很多人用它们做图像生成，但后来**扩散模型**出现了并在生成方面变得可行，使得这种方法不再那么流行。

---

## 9. Summary and Reflections / 总结与思考

Frontier models these days are expected to be multimodal, or even more strongly, natively multimodal or omni models. When Gemini, GPT, and others are released, they are touted as being natively multimodal, handling all modalities—and in fact they do. But there are no details about how these are built internally. My speculation is that it's probably a combination of having a continuous encoder (to avoid losing information) and diffusion for generation.

当今的前沿模型被期望是多模态的，甚至更强地，是原生多模态的(natively multimodal)或全模态模型。当Gemini、GPT等发布时，它们被宣称是原生多模态的，能处理所有模态——事实上它们也做到了。但没有关于它们内部构建方式的细节。我的猜测是，可能是一个连续编码器（避免丢失信息）与扩散模型（用于生成）的组合。

The fundamental challenge when dealing with multimodality is how to handle non-text modalities. There's an interesting asymmetry between understanding a modality and generating it, and there's no one universal encoder. For example, CLIP only cared about capturing high-level semantics for classification, so its vectors could be fairly small. But if you want to do OCR or generate an image, you need really fine-grained detail—that's why diffusion models are so good, because they can micro-optimize low- and high-frequency information.

处理多模态的根本挑战在于如何处理非文本模态。理解一个模态与生成该模态之间存在一个有趣的不对称性，而且没有一个通用的编码器。例如，CLIP只关心为分类捕捉高层语义，因此其向量可以相当小。但如果你想做OCR或生成图像，你需要非常细粒度的细节——这就是为什么扩散模型如此出色，因为它们能微观优化低频和高频信息。

In general, when dealing with multiple modalities, you must carefully weigh them properly. Video certainly has lower information density than text, so you don't want video to overwhelm your text. The current best approach seems to be using continuous encoders. Even though CLIP is five years old, it and similar ideas are still the go-to way to capture image semantics. Transformers are still here. And diffusion models, which I didn't cover in depth, are great for generation. That's it for multimodality—I encourage you to play around with training some of these models if you're curious.

总的来说，在处理多模态时，你必须仔细恰当地加权。视频的信息密度肯定低于文本，所以你不希望视频压倒文本。目前最好的方法似乎是使用连续编码器。尽管CLIP已有五年历史，它和类似的思想仍然是捕捉图像语义的首选方式。Transformer仍然在这里。而扩散模型——我没有深入讲解——在生成方面非常出色。关于多模态的内容就到这里——如果你好奇的话，我鼓励你尝试训练一些这样的模型。

