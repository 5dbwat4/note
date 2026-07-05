# Lecture 14: Data Processing / 数据处理

## 1. Introduction and Recap / 引言与回顾

Today is the second day on data. Last time we talked about how data doesn't really just fall from the sky—you actually have to think about where it comes from. In general, the internet consists of live services. The data on those services has to be either dumped or crawled. Then there's an additional step where you have to process the data. We also talked about various societal considerations, terms of service, and copyright. You have to either get a license or appeal to fair use. So there's a lot of complexity that goes into data.

今天是关于数据的第二天。上次我们讨论了数据并非凭空而来——你需要认真思考数据的来源。一般来说，互联网由各种在线服务组成，这些服务上的数据要么通过数据转储获取，要么通过网络爬虫抓取。然后还需要进行额外的数据处理步骤。我们还讨论了各种社会层面的考量，包括服务条款和版权问题。你必须获得许可，或者援引合理使用原则。数据处理涉及非常多的复杂性。

Today we're going to look more at the data pipeline: transforming the data, filtering the data, deduplication, and mixing. Then we're going to top it off by talking a bit about post-training data, in particular, how folks are using synthetic data these days. The first part is going to be mostly about pre-training.

今天我们将更深入地探讨数据流水线：数据转换、数据过滤、去重，以及数据混合。然后我们会简要讨论后训练数据，特别是目前人们如何使用合成数据。前半部分将主要关注预训练阶段。

## 2. Data Transformation / 数据转换

### 2.1 HTML to Text / HTML转文本

Raw data doesn't come as text, even if you've scraped something. If you ever look inside Common Crawl, it's not text—it's HTML. Sometimes it could be PDFs or directories in the case of GitHub. Most of the attention on transforming data is dealing with HTML because most of the web is in HTML. For this processing, a lot of it is fairly heuristic. There's removing of boilerplate, like navigation and ads, and extracting content, which is the main part of the page.

原始数据并非以文本形式存在，即使你已经抓取了内容。如果你查看 Common Crawl 的内部数据，你会发现它不是文本，而是 HTML。有时也可能是 PDF，或者在 GitHub 的情况下是目录结构。数据转换的大部分工作都集中在处理 HTML 上，因为绝大多数网页都是 HTML 格式的。这种处理在很大程度上是启发式的，包括去除页面模板内容（如导航栏和广告），并提取主要内容——即页面的核心部分。

There are some subtleties around what constitutes content. Usually, you get rid of the footers and headers, and maybe menus, but in some cases, navigation elements might be helpful to learn what web pages look like. So what is content and what is not content is not always clear. And then what do you do about images and tables that are in web pages? Inherently, this is a lossy process because you need to linearize HTML, which is either hierarchical or visual, to a sequence of tokens. Simple tables you can render using markdown, but nested tables become quite challenging—you have to give up or approximate at some point.

关于什么构成"内容"存在一些微妙之处。通常你会去除页脚、页眉和菜单，但在某些情况下，导航元素可能有助于模型学习网页的结构。因此，什么是内容、什么不是内容，并不总是明确的。此外，网页中的图片和表格又该如何处理？从本质上讲，这是一个有损处理过程，因为你需要将 HTML（无论是层次结构的还是视觉呈现的）线性化为一个 token 序列。简单的表格可以用 Markdown 来渲染，但嵌套表格则相当棘手——在某个时刻你只能放弃或近似处理。

Typically, HTML to text processing is rule-based. Rule-based processors are very fast, and you're not trying to do too much here—you don't need too much intelligence. Rule-based generally works. There could be a case for model-based interventions, but they have to be very fast and do something more intelligent. If you ever look at data, you'll notice there are imperfections just because any rule-based processing has some failure rate. The accuracy does matter depending on which tool you choose—for example, Resiliparse works better than others on the extended DCLM evals.

通常，HTML转文本处理是基于规则的方法。基于规则的处理器非常快速，而且你在这里不需要做太多复杂的事情——不需要太高的智能。基于规则的方法通常效果不错。也许在某些情况下可以采用基于模型的方法进行干预，但它们必须非常快，并且能完成更智能的任务。如果你仔细观察数据，你会发现由于任何基于规则的处理都存在一定的失败率，数据中总会有瑕疵。你选择哪种工具确实会影响准确率——例如，在扩展的 DCLM 评估中，Resiliparse 的表现优于其他工具。

### 2.2 PDF Processing / PDF处理

PDF files, if you open them up not in a PDF reader, look like raw encoded data that needs to get rendered. PDFs can be found on web pages on the internet, and Common Crawl does have some PDFs. Generally, Common Crawl focuses on text, but sometimes if you're just given a URL, you might not even know before you fetch it whether it's a PDF or not, if it doesn't have the extension. Many of the PDFs in Common Crawl are truncated because PDFs are big, so recrawling is necessary. Once you have the PDF file, how do you actually convert it to text? Some PDFs might be just scans as well—essentially images.

PDF 文件如果在 PDF 阅读器之外打开，看起来就像是需要渲染的原始编码数据。互联网上的网页中能找到 PDF 文件，Common Crawl 中确实也包含一些 PDF。虽然 Common Crawl 通常侧重于文本，但有时你拿到一个 URL，在抓取之前甚至不知道它是不是 PDF（如果没有扩展名的话）。Common Crawl 中的许多 PDF 是截断的，因为 PDF 文件很大，所以需要重新抓取。有了 PDF 文件之后，如何将其转换为文本呢？有些 PDF 可能只是扫描件——本质上是图片。

There's a bunch of tools that were tried out, but mostly this involves running OCR using a VLM (Vision Language Model). This obviously can be much more expensive than what we were doing before with text. Fortunately or unfortunately, PDFs are a very small fraction of the whole internet. But they are very valuable because generally, if you bother to make a PDF, that means you probably have something interesting to say, as opposed to a web page. The quality of an average PDF is generally higher than for an HTML file. PDFs, more so even than web pages, have a lot of layout information missing. In HTML you have various tags like h1 and p that give you semantic information. PDFs are, by design, all about layout, so you don't necessarily preserve the semantic structure.

已经尝试了多种工具，但主要的方法是通过 VLM（视觉语言模型）进行光学字符识别（OCR）。这显然比之前处理文本的代价高昂得多。幸运或不幸的是，PDF 只占整个互联网的很小一部分。但它们非常有价值，因为一般来说，如果有人专门制作了一份 PDF，那意味着他们可能有更有价值的内容要表达，这与普通网页不同。平均而言，一份 PDF 的质量通常高于 HTML 文件。PDF 比网页更严重地缺失布局信息：在 HTML 中有 h1 和 p 等各种标签，能提供一些语义信息；而 PDF 从设计上讲就是围绕布局的，因此你不一定能保留语义结构。

## 3. Filtering / 过滤

### 3.1 The General Framework / 通用框架

At this point, you have text, but you're far from done. The next step is filtering. Suppose you have some target data that you want to get—this is usually a small amount of high-quality data—and lots of raw data (the fresh shipment of tokens that you transformed from the previous step). The goal is to find a subset of this raw data that is similar to the target. This is the general skeleton for filtering, and almost all kinds of filtering fall into this schema.

到此为止你已经得到了文本，但离完成还差得远。下一步是过滤。假设你有想要获取的目标数据——通常是少量高质量数据——以及大量原始数据（即上一步转换得到的新鲜 token）。目标是找到原始数据中与目标相似的子集。这就是过滤的通用框架，几乎所有类型的过滤都符合这个模式。

There are many reasons you might want to filter. If you're training an English language model or a German language model, you might want to identify the language and filter things that don't match that language. The main reason for filtering is quality filtering—you want to find things that are high quality as opposed to low quality. You don't want just spam; you want encyclopedic information. Another application is toxicity filtering—the internet has plenty of nasty content, and maybe you don't want to train your language model on that.

过滤的需求有很多原因。如果你正在训练一个英语或德语的语言模型，你可能需要识别语言并过滤掉不匹配该语言的内容。过滤的主要原因是质量过滤——你想找到高质量而非低质量的数据。你不想要垃圾信息，而是需要百科全书式的信息。另一个应用是毒性过滤——互联网上有大量不良内容，你可能不想让语言模型在这些内容上训练。

For a filtering algorithm, you want some generalization from the target data, because you already have the target data—you don't want to only get the target data. But you also want it to be extremely fast because you have to run it on the whole internet—this could be 100 trillion tokens worth of data. Generally, filtering ends up keeping a very small fraction, a single-digit fraction of your entire data.

对于过滤算法，你希望从目标数据中实现某种泛化——因为你已经有目标数据了，你不会只想得到那些目标数据本身。但同时你要求它极快，因为你必须在整个互联网上运行它——这可能涉及 100 万亿 token 的数据。一般来说，过滤最终只保留全部数据中很小的一部分，通常是百分之几的比例。

### 3.2 Classifier-Based Filtering / 基于分类器的过滤

The general scheme is that you estimate some model based on raw data (R) and target data (T) and derive a scoring function, then you keep the examples in R based on their score. There are two types of classifiers. One are generative models—you have your target data and you can estimate a model of that data. This has to be cheap, so probably you're not training a big language model. Generally, people use KenLM, which trains a 5-gram model. A more common thing these days is training a classifier. The classifier predicts a positive label for things in T (your target) and negative labels for things that are in raw but not in T. So T are your positive examples, some random subset of R are your negative examples, and then you train a classifier.

通用方案是：基于原始数据 R 和目标数据 T 来估计某个模型，并推导出一个评分函数，然后根据评分来保留 R 中的样本。通常有两种分类器。一种是生成式模型——你拥有目标数据，可以估计一个关于该数据的模型。这必须很廉价，所以你不太可能训练一个大型语言模型。一般人们使用 KenLM，即训练一个 5-gram 模型。如今更常见的做法是训练一个分类器。分类器的做法是：预测正标签（属于目标 T 的数据）和负标签（属于原始数据但不属于 T 的数据）。也就是说，T 中的数据是正例，从 R 中随机抽取的子集作为负例，然后训练一个分类器。

The tool that people generally use is fastText because it's fast. Generally, it's just a linear classifier—a bag of words. Once you have this model, for every new document, you can score it, set some appropriate threshold depending on your quality bar, and keep the examples—sometimes stochastically, sometimes not. This is very much a model-based filtering approach. Remember that many datasets from a few years ago did not use model-based filtering because they wanted to not bias things too much. These days, basically everyone does some amount of model-based filtering because unless you are compute-plentiful (in which case you can just train on everything), most people are compute-poor and have to be very smart about how they're filtering; otherwise, they're just wasting flops on low-quality content.

人们通常使用的工具是 fastText，因为它非常快。实际上它只是一个线性分类器——一个词袋模型。有了这个模型之后，对于每个新文档，你可以为其打分，根据你的质量标准设定适当的阈值，然后保留符合条件的样本——有时是随机保留，有时是确定性保留。这是一种典型的基于模型的过滤方法。回想一下，几年前许多数据集并不使用基于模型的过滤，因为他们不想引入过多的偏差。如今，基本上每个人都会进行一定程度的基于模型的过滤，因为除非你计算资源极其充裕（此时你可以在所有数据上训练），大多数人计算资源有限，必须在过滤策略上非常精明，否则就是把宝贵的算力浪费在低质量内容上。

### 3.3 Language Identification / 语言识别

The goal is to detect, given a piece of text, whether it's of a particular language. Meta has trained a set of fastText language identification models, which you can often use off the shelf. It supports 176 different languages and has been trained on a bunch of multilingual sites—Wikipedia, translation sites, and sites for different languages. Language ID is generally a fairly easy problem compared to many other tasks we're dealing with—a simple classifier. If you look at a few words, you can tell that it's Spanish or Japanese. There are subtleties because of code-switching and dialects, so it's not an absolutely solved problem, but it's not really the bottleneck for training a good language model.

目标是给定一段文本，检测它是否属于某种特定语言。Meta 训练了一套 fastText 语言识别模型，通常可以直接开箱即用。它支持 176 种不同的语言，在大量多语言网站上训练而成——包括维基百科、翻译网站以及各种语言的网站。语言识别与我们正在处理的许多其他任务相比，通常是一个相对简单的问题——一个简单的分类器就够了。看几个词你就能分辨出是西班牙语还是日语。由于代码切换（code-switching）和方言的存在，也存在一些微妙之处，所以这并非一个完全解决了的问题，但它并不是训练优秀语言模型的瓶颈。

### 3.4 Quality Filtering Examples / 质量过滤示例

Suppose you want to get really good at math, so you want to find a bunch of math data. OpenMathText is a paper from 2023 where the goal is to create a large corpus of math text. This pipeline consists of a few steps: first, you use some rules to filter—does it contain LaTeX commands? They also use KenLM (a generative approach), trained on the ProofPile (a known dataset of math), and keep documents if the perplexity is below some threshold. Then you also train a fastText classifier to predict whether it's mathematical writing or not. There's two different thresholds: if it has LaTeX in it, it's a lower bar; if it doesn't have LaTeX, it's a higher bar. As a result, they got 15 billion tokens, which they use to train models.

假设你想让模型在数学上表现出色，你就需要找到大量数学数据。OpenMathText 是 2023 年的一篇论文，目标是创建一个大规模的数学文本语料库。这个流水线包含几个步骤：首先使用一些规则进行过滤——文档中是否包含 LaTeX 命令？他们还使用了 KenLM（一种生成式方法），在 ProofPile（一个已知的数学数据集）上训练，保留困惑度低于某个阈值的文档。然后还训练了一个 fastText 分类器，预测文本是否属于数学写作，并设置了两个不同的阈值：如果包含 LaTeX，则门槛较低（更容易通过）；如果不包含 LaTeX，则门槛较高。最终他们获得了 150 亿 token，用于训练模型。

There's a paper that showed that this more targeted, curated data collection results in models that are better at math than models trained on 20 times as much data that were not filtered in this way. Quality filtering is a tool—you can define quality however you want. There's no universal notion of quality. If you want to define quality to be math, then you can go and get math, and you get better at it.

有一篇论文表明，这种更有针对性的、精心策划的数据收集方式所产生的模型，在数学上比那些用 20 倍数据量但未经如此过滤训练的模型表现更好。质量过滤本质上是一种工具——你可以按照任何方式定义"质量"。质量没有一个通用的定义。如果你将质量定义为数学，那你就可以去获取数学数据，模型就会在数学上做得更好。

GPT-3's approach also falls into this framework: positive examples are Wikipedia, WebText (pages linked from high-star Reddit posts), and some books; negatives are generally sampled from the web. They train a linear classifier and keep documents if the linear classifier scores them highly enough. The first LLaMA paper used pages referenced by Wikipedia (not Wikipedia articles themselves) as positives. phi-1 from Microsoft interestingly also falls into this framework—they defined a prompt that determines educational value, used GPT-4 to classify a subset of R, kept the positives as target, then trained a cheaper classifier (a Random Forest) to extrapolate to the full dataset.

GPT-3 的方法也符合这个框架：正例来自维基百科、WebText（从高赞 Reddit 帖子链接出去的页面）和一些书籍；负例通常从网页中采样。他们训练了一个线性分类器，保留评分足够高的文档。LLaMA 的第一篇论文使用维基百科引用的页面（而不是维基百科文章本身）作为正例。微软的 phi-1 也很有意思地属于这个框架——他们定义了一个衡量教育价值的 prompt，使用 GPT-4 对 R 的一个子集（10 万个样本）进行分类，被标记为正例的保留为目标数据，然后训练一个更廉价的分类器（随机森林）来泛化到整个数据集。

### 3.5 Toxicity Filtering / 毒性过滤

Toxicity works the same way. There's the Jigsaw Toxic Comments dataset, which came from a project whose goal is to help people have better discussions online. The data consists of Wikipedia talk pages, which can get quite heated for controversial topics. This has been annotated with whether there are any toxic comments. You can similarly define positive and negative examples and train a classifier on that. Now you have the tools—you can identify a particular type of data that you want, build a classifier for it, and then go filter Common Crawl for that.

毒性过滤的工作方式类似。Jigsaw Toxic Comments 数据集来自一个旨在帮助人们在网上进行更好讨论的项目。数据由维基百科讨论页面组成，对于有争议的话题，这些讨论可能会相当激烈。这些数据已被标注是否包含毒性评论。你可以类似地定义正例和负例，并在此基础上训练一个分类器。现在你有了工具——你可以识别出你想要的特定类型数据，为其构建一个分类器，然后去 Common Crawl 中过滤出这些数据。

### 3.6 Filtering Thresholds and Training Duration / 过滤阈值与训练时长

The notion of what you want for data actually depends on what model you want to train. In particular, it depends on the number of tokens you're training on. There's no optimal threshold—a classifier gives you a score, and you can't say 0.9 is universally the best because it depends on what you want to do. Intuitively, if you are going to train for a longer period of time, then you can tolerate lower quality data. If you're training for shorter, then you want higher quality data, in general. If you could wave a magic wand, you'd want more high-quality data when training longer, but that's not an option—the data pool is what it is.

你想要什么样的数据实际上取决于你想训练什么样的模型。具体来说，它取决于你训练的 token 数量。没有最优阈值——分类器给你一个分数，你不能说 0.9 是普遍最优的，因为这取决于你的目标。直觉上，如果你训练的时间更长，你可以容忍较低质量的数据；如果你训练的时间较短，通常你需要更高质量的数据。如果你有一根魔法棒，训练时间更长时你当然想要更多高质量数据，但这并不现实——数据池是固定的。

A preliminary experiment shows this trend: for a 157-million parameter model, high-quality data is better in the regime where you're not epoching (repeating data). But once you get to lots and lots of tokens, high-quality data is no longer that great. With high-quality data, you wouldn't want to go into the overfitting regime anyway—you'd probably stop earlier. But even at that point, it can be worse than if you had trained for longer using low-quality data.

一项初步实验展示了这个趋势：对于一个 1.57 亿参数的模型，在你不重复遍历数据（epoch）的阶段，高质量数据表现更好。但一旦你训练到非常多的 token，高质量数据就不再那么有优势了。对于高质量数据，你本来也不希望进入过拟合阶段——你可能会提前停止。但即使在那个停止点，结果也可能不如使用低质量数据训练更长时间来得好。

### 3.7 Summary of Filtering / 过滤小结

Filtering is pretty critical for building a good model, especially when you're compute-constrained like most of us. Technically, if you have infinite compute, you don't need to filter—you can train on everything, and it'll be a giant model. But realistically, everyone has to filter. The recipe is: figure out what good data looks like, then train a classifier that will extrapolate to the rest of your data. What good data looks like? You can either find it by saying there's a dataset out there that you really like and you just want more of it, or you can craft a prompt to a language model and use that to do a preliminary filter of a large pool, then use that good quality data to train a smaller classifier and extrapolate to everyone else.

过滤对于构建一个好的模型至关重要，尤其是当你像我们大多数人一样计算资源有限的时候。从技术上讲，如果你有无限的计算资源，你就不需要过滤——你可以在所有数据上训练，得到一个巨型模型。但在现实中，每个人都必须进行过滤。配方是：弄清楚"好数据"长什么样，然后训练一个能泛化到其余数据的分类器。好数据长什么样？你可以通过以下方式找到：要么找到了一个你非常喜欢的数据集，你只是想要更多类似的数据；要么你可以精心设计一个 prompt 给语言模型，用它来对一个大型数据池进行初步过滤，然后用这些高质量数据训练一个较小的分类器，再将其泛化到所有其他数据。

## 4. Deduplication / 去重

### 4.1 Why Deduplicate? / 为什么要去重？

At this point, we have filtered our dataset—we only have what we deem to be high-quality data. But often, data still has duplicates in it. There are two types of duplicates: exact duplicates and near duplicates. Exact duplicates happen when, for example, you have mirror sites—the whole point of a mirror is that it's a duplicate. Sometimes the web crawler isn't smart enough to know that this mirror is exactly that mirror, so it crawls both, and you'll get the exact same content. Also, when you fork a repo, 99% of that repo might be the same, even if you make changes to a few files.

到此为止我们已经过滤了数据集——只保留了我们认为高质量的数据。但数据中通常仍然存在重复。有两种类型的重复：完全重复和近似重复。完全重复发生在例如镜像站点的情况下——镜像的整个意义就在于它是一个副本。有时网络爬虫不够聪明，不知道这个镜像和那个镜像完全一样，所以它抓取了两个站点，你就会得到完全相同的内容。同样，当你 fork 一个代码仓库时，即使你修改了几个文件，该仓库中 99% 的内容可能仍然是相同的。

Near duplicates are not mirrors or derivatives, but they just happen to be the same text differing by a few tokens. Examples include terms of service and licenses (the MIT license probably shows up in a lot of places), common headers and footers on websites, typographic differences (one version with a comma, one without), and templates where someone just replaced "Canada" with "USA" in what is essentially an ad. If you train on different variations of this with different entities, you're wasting your GPUs. There are more extreme cases—an audit of the C4 dataset found a particular product description (of a gas mask) appearing 61,000 times in the dataset. The web is weird.

近似重复不是镜像或衍生品，而只是恰好是相同的文本，仅相差几个 token。例如服务条款和许可证（MIT 许可证可能出现在很多地方）、网站上共用的页眉和页脚、排版差异（一个带有逗号，一个没有），以及模板化的内容——有人只是将本质上是广告的内容中的"加拿大"替换成了"美国"。如果你在这些不同实体的不同变体上训练，那是在浪费 GPU 算力。还有更极端的例子——对 C4 数据集的一次审计发现，某个产品描述（关于一个防毒面具）在数据集中出现了 61,000 次。网络世界真的很怪异。

Deduplication reduces your dataset size without really losing information because you're just removing duplicates. It also has the benefit of avoiding memorization—if you have some copyrighted content that's duplicated a lot and you train on it, you'll memorize it, which raises privacy concerns. But mostly, it's to make sure you're not wasting flops. Related to deduplication is also decontamination, which is arguably even more important—you want to make sure that your test set is not in your training set.

去重可以在不真正丢失信息的情况下减小数据集大小，因为你只是移除了重复的内容。它还有避免记忆化的好处——如果你有一些被大量重复的受版权保护的内容，在其上训练会导致模型记住它，这会引发隐私问题。但最主要的原因是确保你不会浪费算力。与去重相关的是数据去污染（decontamination），这可以说更为重要——你要确保测试集不出现在训练集中。

### 4.2 Design Space / 设计空间

What are the items you're deduping? Do you do it at the sentence level, the paragraph level, or the document level? How do you determine a match? Is it an exact match? Is it the existence of a common subitem? Is it the fraction of common subitems for near deduplication? And once you find a duplicate between two pages, what do you do? Do you remove all the instances, or do you remove all but one?

你要在什么粒度上去重？是句子级别、段落级别还是文档级别？你如何判断匹配？是完全匹配吗？是存在公共子项吗？还是对于近似去重来说，看公共子项的占比？一旦发现两个页面之间有重复，你怎么办？是删除所有实例，还是只保留一个？

The key algorithmic challenge is that deduplication is fundamentally about comparing items to other items. Normally, filtering is about an individual item—"is this item good or not?"—and this can be parallelized; it's linear time, which is good. But deduplication clearly can't do the n-squared thing where you compare everything to everything. You need linear-time algorithms to scale, especially at web scale. Typically, the deduplication literature uses hash functions to get around this.

关键的算法挑战在于，去重本质上是将项目相互比较。通常，过滤是针对单个项目的——"这个项目好不好？"——这可以并行处理，是线性时间的，这很好。但去重显然不能用 O(n²) 的方法，不能将每个项目与每个其他项目逐一比较。你需要线性时间算法才能扩展，尤其是在网络规模下。去重文献中通常使用哈希函数来解决这个问题。

### 4.3 Exact Deduplication / 完全去重

Exact duplication is conceptually very simple. You take a string, see if there's an exact match, and remove all but one. You hash the elements and dedupe. Exact duplication is very nice and clear about what's happening, but this isn't really good enough for messy web data because often you have near duplicates. As an example, C4, from the T5 paper, which processed Common Crawl, did exact deduplication. The items they operated on were three-sentence spans—they did an exact match and removed all but one. This is a bit strange because ripping out three sentences from a document breaks coherence, but that's what they did.

完全去重在概念上非常简单。你取一个字符串，看是否有完全匹配，然后只保留一个。你对元素进行哈希处理然后去重。完全去重非常清晰明确，但对于混乱的网络数据来说还不够好，因为你经常遇到近似重复。举一个例子：来自 T5 论文的 C4 数据集处理了 Common Crawl 并做了完全去重。他们操作的项目是三句跨度——进行完全匹配并只保留一个。这有点奇怪，因为从文档中抽取三句话会破坏连贯性，但这就是他们当时的做法。

### 4.4 Near Deduplication and Jaccard Similarity / 近似去重与 Jaccard 相似度

To do near deduplication, we first have to define what approximate match means. We define the Jaccard similarity, which is a fairly standard notion. Jaccard of two sets is the size of the intersection over the size of the union. Jaccard is a number between 0 and 1—0 means they're disjoint, 1 means they're identical. We say two documents are near duplicates if their Jaccard similarity is above some threshold, say 0.99.

要进行近似去重，我们首先需要定义什么是近似匹配。我们定义 Jaccard 相似度，这是一个相当标准的概念。两个集合的 Jaccard 相似度定义为交集大小除以并集大小。Jaccard 是一个介于 0 和 1 之间的数字——0 表示它们完全不相交，1 表示它们完全相同。如果两个文档的 Jaccard 相似度高于某个阈值（比如 0.99），我们就说它们是近似重复。

### 4.5 MinHash

The question is: how do you find near duplicates in linear time? The answer is to use MinHash. MinHash is a random hash function such that the probability of a hash collision is exactly the Jaccard of A and B. This is a very nice property because hashing is good for making things linear time, Jaccard is the metric that we want, and we're connecting these two in expectation. Normally you want hash functions to avoid collisions, but here you actually want collisions—you want to control the collisions in a certain way to align with similarity: similar things should collide more than disparate things.

问题是如何在线性时间内找到近似重复？答案是使用 MinHash。MinHash 是一种随机哈希函数，使得哈希碰撞的概率恰好等于 A 和 B 的 Jaccard 相似度。这是一个非常好的性质，因为哈希可以让我们实现线性时间处理，Jaccard 是我们想要的相似度度量，而我们通过期望将这两者连接起来。通常你希望哈希函数避免碰撞，但在这里你实际上想要碰撞——你想以某种方式控制碰撞，使其与相似度对齐：相似的事物应该比不相似的事物有更高概率发生碰撞。

MinHash is fairly simple: you take a set, hash every element in that set, and take the minimum element. Why take the min? You could take the max too—it's just a way to break ties. Each item has the same probability of being first under a random permutation. If the random hash function puts a shared element first, then the min of A equals the min of B. If it puts a unique element first, then the mins are different. So the probability of the mins being equal is exactly the Jaccard similarity.

MinHash 非常简单：你取一个集合，哈希其中的每个元素，然后取最小值。为什么要取最小值？你也可以取最大值——这只是一个打破平局的方式。在随机排列下，每个元素成为第一个的概率是相同的。如果随机哈希函数将一个共享元素排在了第一位，那么 A 的最小值就等于 B 的最小值；如果它将一个独有的元素排在了第一位，那么这两个最小值就不同。因此，最小值相等的概率恰好等于 Jaccard 相似度。

The key thing with MinHash is that you don't have to do the n-squared thing—you can compute the MinHash of A, the MinHash of B, the MinHash of a different set, and you just look for collisions.

MinHash 的关键之处在于，你不需要做 O(n²) 的比较——你可以分别计算 A 的 MinHash、B 的 MinHash 以及不同集合的 MinHash，然后只需查找碰撞即可。

### 4.6 Locality-Sensitive Hashing (LSH) / 局部敏感哈希

Now we can hash our items, but we're not done yet because a single collision doesn't tell us the Jaccard is above some threshold, which is what we want. All we've done is said that if we've got a collision, the probability of that collision is equal to the Jaccard. But that's not really useful by itself—it's stochastic, and you can't get anything reliable here. The next idea is Locality-Sensitive Hashing (LSH), which essentially solves this problem. The goal is to have A and B collide if the Jaccard is greater than some threshold. We need to sharpen the probabilities somehow.

现在我们可以哈希数据项了，但还没有完成，因为单次碰撞并不能告诉我们 Jaccard 相似度是否高于某个阈值——这才是我们想要的。到目前为止我们只是说，如果发生碰撞，碰撞的概率等于 Jaccard 相似度。但这本身并不实用——它是随机的，你无法从中得到可靠的信息。下一个想法是局部敏感哈希（LSH），它本质上解决了这个问题。我们的目标是：当 Jaccard 相似度大于某个阈值时，A 和 B 才发生碰撞。我们需要以某种方式"锐化"概率。

The solution is to use more hash functions, and these hash functions are independent. You break the n hash functions into b bands of r hash functions. If you have 12 hash functions, you have 3 bands, each with 4 hash functions. A and B are said to collide if for some band, all of its hash functions return the same value. So there's an and-or structure here that is doing the lifting. The probability of a fixed band matching is s^r (where s is the Jaccard similarity), which is exponential in r and generally quite low. The probability of collision overall is 1 minus the probability that all bands don't match: 1 - (1 - s^r)^b.

解决方案是使用更多的哈希函数，并且这些哈希函数是相互独立的。你将 n 个哈希函数分成 b 个带（band），每个带包含 r 个哈希函数。如果你有 12 个哈希函数，可以分成 3 个带，每个带有 4 个哈希函数。A 和 B 被称为"碰撞"，当且仅当存在某个带，其中所有哈希函数返回的值都相等。所以这里有一个"与或"结构在起作用。一个固定带匹配的概率是 s^r（s 是 Jaccard 相似度），这是 r 的指数函数，通常非常低。总体碰撞概率为 1 减去所有带都不匹配的概率：1 - (1 - s^r)^b。

If you plot this, you get an interesting S-shaped curve. This is what we wanted—to sharpen the probabilities. If the similarity is below some threshold, we want the probability of matching to be as low as possible. If it's above some threshold, we want it to be as high as possible. We're trying to get this to be like a phase transition. Increasing r sharpens the threshold and moves the curve to the right—everything becomes harder to match because you have more hash functions inside a bucket. Increasing b moves the curve to the left—it makes it easier to match because there are more bands, so more chances of matching.

如果把这个函数画出来，你会得到一个有趣的 S 形曲线。这正是我们想要的——锐化概率。如果相似度低于某个阈值，我们希望匹配概率尽可能低；如果相似度高于某个阈值，我们希望匹配概率尽可能高。我们在试图使之成为一种相变。增加 r 会锐化阈值并将曲线向右移动——因为一个 bucket 内有更多哈希函数，匹配变得更困难。增加 b 会将曲线向左移动——因为有更多带，匹配机会更多，匹配变得更容易。

The phase transition happens at a threshold of (1/b)^(1/r). If you want to filter based on Jaccard greater than 0.9, you set b and r such that this equals 0.9, and then by changing b and r, you can make the phase transition sharper. In a real deduplication paper, they used b = 20 bands and r = 450, giving you an idea of the magnitude of these numbers.

相变发生在一个特定阈值 (1/b)^(1/r) 处。如果你想基于 Jaccard 大于 0.9 进行过滤，你需要设置 b 和 r 使得该表达式等于 0.9，然后通过改变 b 和 r 使相变更加尖锐。在一篇真实的去重论文中，他们使用了 b = 20 个带和 r = 450，这让你对这些数字的量级有个概念。

This method is called MinHash LSH—LSH really works for any hash functions, but for deduplication in language model processing, we're using MinHash, which approximates Jaccard. One note: there's often deduplication within a dataset, but you actually have to do deduplication across your entire dataset because datasets can be redundant. Sometimes that's not done, but it should be.

这种方法被称为 MinHash LSH——LSH 实际上适用于任意哈希函数，但在语言模型数据处理中用于去重的，我们使用 MinHash，它近似 Jaccard。有一点需要注意：通常会在单个数据集内部去重，但你实际上需要在你的整个数据集范围内去重，因为不同数据集之间可能存在冗余。有时人们没有这样做，但应该这样做。

## 5. Data Mixing / 数据混合

### 5.1 The Problem / 问题定义

So far, we've transformed our data from raw HTML or PDFs into text, filtered for high quality, and deduped—we have a smaller set of high-quality documents. This generally happens for a given data source. But language models are trained on multiple data sources. There's code, there's books, there's Wikipedia, there's Common Crawl, and many more. The question is: how do you combine these?

到目前为止，我们已经将数据从原始 HTML 或 PDF 转换为了文本，过滤出了高质量内容，并进行了去重——我们得到了一个较小的高质量文档集合。这通常是对一个给定数据源的操作。但语言模型是在多个数据源上训练的：有代码、有书籍、有维基百科、有 Common Crawl，还有很多其他来源。问题是：你如何组合这些数据源？

If you look at older papers like The Pile, they essentially assign a particular weight to each component—you have a distribution over sources. So where does that weight come from?

如果你看像 The Pile 这样的较早期论文，它们本质上是为每个组成部分分配一个特定权重——你在数据源上有一个分布。那么这些权重从何而来？

### 5.2 Simple Approaches / 简单方法

The simplest approach is "vibes"—you just manually set the weights based on some intuition, which is more often than you might think what people do. Even in recent papers, sometimes you use some method and then just tweak things. You can also do uniform sampling—you put a uniform distribution over your sources and sample every chunk. You can also do proportional mixing—you sample proportional to the number of tokens in a source. If you have a dataset with more tokens, you put a higher weight. This is generally a rational thing to do, but you might worry that a huge, low-quality dataset will eat up a lot of your token budget. So it doesn't seem quite optimal either.

最简单的方法是"凭感觉"（vibes）——你基于直觉手动设置权重，这种做法比你以为的更常见。即使在最近的论文中，有时也用某种方法然后稍作调整。你也可以做均匀采样——在所有数据源上放置均匀分布，然后从每个源采样。你也可以做按比例混合——按照每个数据源中 token 的数量比例进行采样。如果某个数据集有更多 token，你就给它更高的权重。这通常是一种理性的做法，但你可能会担心一个庞大但质量低的数据集会消耗大量 token 预算，所以这似乎也不是最优的。

Intuitively, you should upweight your higher quality sources. But there are two important things to keep in mind. One is that you want to ensure some diversity—sources are often incomparable (literature vs. code vs. papers), and you can't really say that a paper is higher quality than code because they're just incomparable objects. If you want your language model to do well, you don't want to put all your mass on papers. The second thing is that each source is actually finite—if you put too much weight on a small source, you essentially run out of that source and need to epoch over it, meaning you keep training on literally the same tokens, which is bad for reasons we'll see.

直觉上，你应该给质量更高的数据源更高的权重。但有两件重要的事情需要牢记。一是你需要确保一定的多样性——不同数据源之间通常是不可比较的（文学、代码、论文属于不同类型），你不能真正说一篇论文比一段代码更"高质量"，因为它们本质上是不可比较的对象。如果你想让语言模型表现良好，你不想把所有权重都放在论文上。二是每个数据源实际上是有限的——如果你在一个小数据源上放了太多权重，你本质上会用尽该数据源，然后不得不在上面重复遍历（epoch），这意味着你一直在训练完全相同的 token，这是不好的。

### 5.3 The Epoching Problem / 重复遍历问题

Imagine you have two sources: a low-quality source with 10 trillion tokens and a high-quality source with 10 billion tokens. Generally, high-quality sources are smaller. If you do a naive uniform mixture (half high, half low) and train for 1 trillion tokens, you'll find that only about 5% of the tokens in the low-quality dataset are touched once, while for the high-quality source, the number of epochs is 50. You have to repeat each data point 50 times because you only have 10 billion tokens but need to train on 500 billion. This is really important, and some big model runs have messed this up. The lesson is: look at how many epochs you're actually doing on your data.

假设你有两个数据源：一个低质量数据源有 10 万亿 token，一个高质量数据源有 100 亿 token。一般来说，高质量数据源更小。如果你做一个简单的均匀混合（高质量和低质量各一半）并训练 1 万亿 token，你会发现低质量数据集中只有约 5% 的 token 被使用了一次，而对于高质量数据源，epoch 数是 50——你不得不将每个数据点重复 50 次，因为你只有 100 亿 token，但需要训练 5000 亿 token。这一点非常重要，一些大型模型训练在这方面犯过错。教训是：关注你实际对数据做了多少次 epoch 重复遍历。

### 5.4 UniMax: Capping Epochs / UniMax：限制重复次数

This problem was noticed quite a long time ago. The UniMax paper noticed that some works would take proportional mixing and raise it to some power to flatten the distribution. But their key idea is to sample sources uniformly, but with a hard cap on the number of epochs. You say "I'm only going to take 20 epochs over a particular data source." If you've done that, then too bad—you don't get any more tokens from that source and move on to the next thing. This is like a safety net. The probability assigned to a source times the number of training tokens should be less than or equal to the cap.

这个问题很早就被注意到了。UniMax 论文观察到，有些工作会对按比例混合取某次幂来拉平分布。但他们的核心思想是：均匀地采样各个数据源，但对 epoch 数施加硬性上限。你规定"我对某个特定数据源最多只做 20 个 epoch"。如果用完了，那就没了——你不再从该数据源获取更多 token，转而使用其他数据源。这就像一个安全网。分配给某个数据源的概率乘以训练的 token 总数，应小于或等于该上限。

### 5.5 Regression-Based Mixing / 基于回归的数据混合

The most principled and easiest to understand method is regression-based mixing (RegMix, Olmix, and similar). The idea is relatively simple: first, go to a small scale (say 300 million parameters) and try different data mixtures. Train a swarm of small models, each with a different mixture. Each model gives you a loss on some target metric (downstream values, perplexity, whatever you want). Then you use these data points to fit a regression where the regression model maps the data mixture weights to the loss. Now you have a very cheap model that tells you, "if I were to train on this mixture, what loss would I get?" Then you can optimize that function for the optimal data mixture, and that's the mixture you use to train the large-scale model.

最有原则性、最容易理解的方法是基于回归的数据混合（RegMix、Olmix 等类似论文）。思路相对简单：首先在小规模上（比如 3 亿参数）尝试不同的数据混合方式。训练一群小模型，每个使用不同的混合比例。每个模型在某目标指标上给你一个 loss（可以是下游评估值、困惑度或任何你想要的指标）。然后你用这些数据点来拟合一个回归模型，该模型将数据混合权重映射到 loss 上。现在你有了一个非常廉价的模型，可以告诉你"如果我按这个混合比例训练，会得到什么样的 loss？"然后你可以优化这个函数，找到最优的数据混合比例，这就是你用来训练大规模模型的混合方案。

There are a few design decisions: what mixtures to try (often people use a Dirichlet distribution), the regression method (linear models or boosted decision trees), and the target (often based on downstream evals). You have to be very careful not to overfit because pre-training is supposed to train a general-purpose model, not fit some downstream evals. If you have a bunch of code evals and you're not careful, you're going to upweight all the code data—that's not rocket science. If you then want to generate some poetry, you might realize you've overfit. Proportional mixing and uniform mixing don't have this problem because you're not looking at downstream evals.

有几个设计决策需要考虑：尝试哪些混合方案（人们通常使用 Dirichlet 分布）、回归方法（线性模型或提升决策树）、以及目标指标（通常基于下游评估）。你必须非常小心不要过拟合，因为预训练的目的是训练一个通用模型，而不是拟合某些下游评估。如果你有一堆代码评估基准而不加小心，你最终会赋予代码数据更高的权重——这没什么高深的。如果你随后想生成一些诗歌，你可能会意识到你已经过拟合了。按比例混合和均匀混合没有这个问题，因为它们不依赖于下游评估。

There are two leaps of faith: one, that the regression model trained on small proxy runs is still accurate at the optimum (you might be optimizing to extremes where you don't have much coverage); and two, that optimal data mixtures transfer from small scale to large scale. At least at the scales that the open community works with, this tends to be true, but clearly there are scale-dependent effects—if you're training for many more tokens, probably low-quality data is OK, so the optimum is not the same.

这里有两个需要谨慎对待的假设：第一，基于小型代理训练运行的回归模型在最优解处仍然准确（你可能优化到了数据覆盖稀少的极端区域）；第二，最优数据混合比例能从小规模迁移到大规模。至少在开源社区工作的规模上，这似乎成立或并非明显错误。但显然存在规模依赖效应——如果你训练的 token 更多，低质量数据可能就没问题了，所以最优解不会完全相同。

### 5.6 Simulated Epoching / 模拟重复遍历

There's another scale-dependent effect: if you train a small model on low token counts, you might put a lot of mass on your high-quality data (because you're not epoching). But if you then train a large model on this mixture, you'll end up epoching a lot on the high-quality data and overfit. One solution is capping epochs (as in Olmix). Another solution is simulated epoching—make your small scale look like your large scale. The principle is that you downsample your sources proportionally. If your small runs use 10 billion tokens and your big run uses 1 trillion tokens, you have a 1-in-100 downsampling. With downsampled data, the solution is not going to look as good because you're only training on a minuscule fraction of Wikipedia, so you'll realize you'll be epoching a lot. This simulates the data scarcity that you would get in your high regime at low scale.

还有另一个规模依赖效应：如果你在小模型上用少量 token 训练，你可能会在高质量数据上放很多权重（因为你没有重复遍历）。但如果你随后用这个混合比例来训练一个大模型，你最终会在高质量数据上做大量 epoch 并导致过拟合。一个解决方案是限制 epoch（如 Olmix 的做法）。另一个解决方案是模拟重复遍历（simulated epoching）——让你的小规模训练看起来像大规模训练。原则是按比例下采样你的数据源。如果你的小训练用 100 亿 token，大训练用 1 万亿 token，那就做 1/100 的下采样。有了下采样后的数据，那个只训练维基百科的解决方案看起来就没那么好了，因为你只能训练维基百科中极小的一部分，你会意识到你将做大量重复遍历。这就模拟了你在大规模下会遇到的数据稀缺问题。

### 5.7 Summary of Data Mixing / 数据混合小结

The problem is how to weight different sources: Wikipedia, Common Crawl, code, math data scraped from somewhere. How do you balance them? Regression-based mixing is a nice framework—you estimate a function that maps mixture weights to a loss at small scale, optimize, and then generalize to large scale. You just have to be very careful with epoching and overfitting issues, and use either cap epoching or simulate epoching. One lesson: if you're trying to optimize anything, you have to be very careful because you are in danger of optimizing the wrong thing.

问题是如何为不同数据源赋权：维基百科、Common Crawl、代码、从某处抓取的数学数据。你如何平衡它们？基于回归的混合是一个很好的框架——你在小规模上估计一个将混合权重映射到 loss 的函数，进行优化，然后泛化到大规模。你只需要非常小心地处理重复遍历和过拟合问题，并使用上限 epoch 或模拟 epoch 的方法。一个教训是：如果你试图优化任何东西，你都必须非常小心，因为你很可能正在优化错误的目标。

## 6. Post-Training Data / 后训练数据

Up until now, this has been basically pre-training or mid-training data—generally fairly task-agnostic. The data is still relatively task-agnostic, and you're trying to develop basic skills. When you look at post-training, a lot of the data becomes very task-dependent. The general recipe is: you define a set of environments (e.g., GitHub repos), define a set of tasks or prompts, and then collect responses from a strong model or teacher. In the open community, almost all post-training data is synthetically generated. You could replace a strong model with a human, but that is slow and costs a lot of money.

到目前为止，我们讨论的基本上都是预训练或中期训练数据——通常与具体任务无关。数据本身仍然相对任务无关，你的目标是培养模型的基本能力。当你看后训练阶段时，很多数据变得高度任务相关。通用配方是：定义一组环境（例如 GitHub 仓库），定义一组任务或提示（prompt），然后从强大的模型或教师模型收集回答。在开源社区中，几乎所有的后训练数据都是合成生成的。你也可以用人类来代替强大模型，但那样很慢且花费很高。

One work is OpenThoughts, motivated by when o1 came out and there was a lot of attention on reasoning, mostly for math and science. They eventually produced 1.2 million examples using a teacher model. They drew from many sources—human sources like Stack Exchange or NuminaMath, and synthetic sources as well. They did a comprehensive analysis: having a few sources was actually better than trying to use all sources; sampling multiple generations (like 16) is helpful; and having better models aren't necessarily better teachers—for example, QwQ-32B (an old, small model) was a better teacher than DeepSeek-R1 (at the time one of the strongest open models).

OpenThoughts 是其中一项工作，它的动机是 o1 发布后，推理能力（主要是数学和科学推理）引起了极大关注。他们最终使用教师模型生成了 120 万个样本。他们从许多来源提取数据——有人工来源如 Stack Exchange 或 NuminaMath，也有合成来源。他们做了全面的分析：使用少数几个来源实际上比试图使用所有来源更好；采样多个生成结果（如 16 个）是有帮助的；更好的模型不一定是更好的教师——例如，QwQ-32B（一个老的小模型）作为教师比 DeepSeek-R1（在当时是最强的开源模型之一）更好。

For agentic coding, the SWE-smith paper had the idea of being given a repository and using a language model to automatically generate tasks. An agent takes a repository, makes it usable (installing dependencies, etc.), then generates tasks (modifying code, introducing bugs) that get verified—resulting in 50k synthetic task instances, which was quite large at the time. The SWE-Zero paper from NVIDIA had an interesting observation: unlike math, SWE tasks have heavy dependencies, and most GitHub repos don't even run. Rather than having a repo-specific Docker image, they noticed models are actually good enough to solve many tasks without execution feedback—achieving almost 70% without being able to execute code, compared to 80% with execution. So they were able to generate 300,000 agent trajectories using real GitHub PRs.

关于智能体编程（agentic coding），SWE-smith 论文的想法是：给定一个代码仓库，使用语言模型自动生成任务。一个智能体获取一个仓库，使其可用（安装依赖等），然后生成任务（修改代码、引入 bug），经过验证后得到 5 万个合成任务实例——这在当时是相当大规模的。NVIDIA 的 SWE-Zero 论文有一个有趣的观察：与数学不同，软件工程任务有大量重型依赖，大多数 GitHub 仓库甚至无法直接运行。与其为每个仓库构建特定的 Docker 镜像，他们注意到模型实际上已经足够强大，可以在没有执行反馈的情况下解决许多任务——在不允许执行代码的情况下达到了近 70% 的完成率，而允许执行时是 80%。因此，他们能够使用真实的 GitHub PR 生成 30 万条智能体轨迹。

More recently, SWE-rebench scaled this up to 12 million agent trajectories. SWE-Zero is very lightweight—it doesn't care about execution. SWE-rebench tried to get things to execute but only got 32,000 of them to execute. With SWE-Zero, you can use all of them. The general idea is that you have prompts, which involve trade-offs: you can have fully synthetic, semi-synthetic (real environment, synthetic tasks), or real. The responses generally come from capable models, but they also need to be good teachers. Code environments are a pain, and there's a lot of filtering and other details.

最近，SWE-rebench 将这一规模扩展到了 1200 万条智能体轨迹。SWE-Zero 非常轻量——它不关心代码执行。SWE-rebench 试图让代码真正运行起来，但只成功运行了 3.2 万个。而用 SWE-Zero 的方法，所有数据都可以使用。总体思路是：你有 prompt，这涉及权衡——你可以是完全合成的、半合成的（真实环境，合成任务）或真实的。回答通常来自能力强大的模型，但它们也需要是好的教师。代码环境是一个难题，还有大量的过滤和其他细节。

## 7. Lecture Summary / 课程总结

We talked about filtering: define what good looks like, then train a lightweight classifier, go over your web crawl, and you can get a small subset that matches what you're looking for. Deduplication is important to avoid overfitting and saving flops. Mixing: try a mixture at small scales, extrapolate to large scale. And we looked at some post-training data. A lot of the data work can be very grungy, domain-specific, and requires looking at concrete examples to make high-quality datasets. This lecture is not really representative of what data work is like, but hopefully gives you an idea of the data landscape out there.

我们讨论了过滤：定义"好"是什么样的，然后训练一个轻量分类器，遍历你的网络爬虫数据，就能得到与你目标匹配的一小部分数据。去重对于避免过拟合和节省算力非常重要。数据混合：在小规模上尝试混合方案，然后外推到大规模。我们还看了一些后训练数据。数据处理中的大量工作可能是非常繁琐的、领域特定的，需要仔细查看具体样本来构建高质量数据集。这堂课不能完全代表实际数据处理工作的全貌，但希望能让你对数据处理领域的概况有所了解。
