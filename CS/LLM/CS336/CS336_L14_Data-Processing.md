---
title: "Lecture 14: Data Processing"
---


# Lecture 14: Data Processing / 第十四讲：数据处理（Data Processing）

---

OK, let's get started. So today is the second day on data. Last time we talked about how data doesn't really just fall from the sky. You actually have to think about where it comes from. So in general, the internet consists of live services. That data on those services have to be either dumped or crawled. And then there's an additional step where you have to process the data. And we also talked about various societal considerations, terms of service, copyright. You have to either get a license or appeal to fair use. So there's a lot of complexity that goes into data. So today we're going to look more at the data pipeline from transforming the data, filtering the data, deduplication, and mixing. And then we're going to top it off by talking a bit about post-training data, in particular, how folks are using synthetic data these days. So the first part is going to be mostly about pre-training. That's what you should have in mind.

好，我们开始吧。今天是关于数据的第二次课。上次我们谈到，数据并不是凭空掉下来的，你实际上需要考虑数据从哪里来。通常来说，互联网由各种在线服务（live services）组成。这些服务上的数据必须通过转储（dumped）或爬取（crawled）来获取。之后还有一个额外的步骤，那就是你必须对数据进行处理。我们还讨论了各种社会层面的考量、服务条款（terms of service）、版权（copyright）——你必须要么获得许可（license），要么诉诸合理使用（fair use）。因此，数据处理涉及很多复杂性。今天我们将更多地关注数据流水线（data pipeline），涵盖数据转换（transforming）、过滤（filtering）、去重（deduplication）和混合（mixing），最后我们还会简要讨论一下后训练数据（post-training data），尤其是当前人们如何使用合成数据（synthetic data）。第一部分主要涉及预训练（pre-training），这是你需要记住的。

---

So we talked a little bit about data transformation already, but just as a reminder. So raw data doesn't come as text, even as if you've scraped something. If you ever look inside Common Crawl, it's not text. It's either HTML. Sometimes it could be PDFs or directories in the case of GitHub. So most of the attention on transforming data is dealing with HTML because most of the web is in HTML. And for this processing, a lot of this is fairly heuristic. There's removing of boilerplate, like navigation and ads, and extracting content, which is the main part of the page. And there's some subtleties around what constitutes content. Usually, you get rid of the footers and headers, and maybe menus, and those things, and you try to extract the content. But you could imagine in cases where some of the navigation elements might be helpful to learn what web pages look like. So what is content and what is not content is not always clear. And then what do you do about images and tables that are in web pages? So inherently, this is a lossy process because you need to linearize HTML, which at least is either hierarchical or visual, if you think about the rendered output, and to a sequence of tokens. And particular tables are a bit tricky to deal with. Simple tables, you can render using markdown. But if you have nested tables, then that becomes quite challenging. You have to give up at some point or approximate at some point. So, typically, HTML to text processing is rule-based. And the reason for this is that rule-based processors are very fast. And also, you're not trying to do too much here. You don't need too much intelligence. So rule-based generally works.

我们之前已经简单讨论过数据转换（data transformation），这里再提醒一下。原始数据并不是以文本形式出现的，即使你是通过爬取获得的。如果你查看过 Common Crawl 的内部，就会发现它不是文本，而是 HTML。有时也可能是 PDF，或者在 GitHub 的情况下是目录。因此，数据转换中的大部分注意力都集中在处理 HTML 上，因为互联网上的大部分内容都是 HTML。这种处理在很大程度上是启发式的（heuristic）。它包括移除样板内容（boilerplate），比如导航和广告，以及提取内容（content），即页面的主要部分。关于什么构成内容，有一些微妙之处。通常你会去掉页脚、页眉、可能还有菜单之类的东西，然后尝试提取内容。但你可以想象，在某些情况下，一些导航元素可能有助于让模型了解网页的样子。所以什么算内容、什么不算内容，并不总是那么明确。此外，如何处理网页中的图片和表格呢？本质上来讲，这是一个有损过程（lossy process），因为你需要将 HTML 线性化（linearize）——它要么是层级结构的，要么是视觉上的（如果你考虑渲染后的输出）——转换为一个标记序列。特别是表格处理起来有点棘手。简单的表格可以用 Markdown 渲染，但如果遇到嵌套表格，那就相当具有挑战性了，你不得不在某个点上放弃或进行近似处理。因此，典型的 HTML 转文本处理是基于规则的（rule-based）。原因是基于规则的处理速度非常快，而且你在这里不需要做太多事情，不需要太多的智能，所以基于规则的方法通常有效。

---

Now, I think there could be a case for model-based interventions at this point. They have to be very fast, and they have to do something more intelligent. But if you ever look at data, you'll notice there are imperfections in the data just because any rule-based processing have some failure rate. As we showed last time, the accuracy does matter, depending on which tool you choose. If you use Resiliparse or Trafilatura, then-- I guess Resiliparse on these extended dclm evals works better than the others.

不过，我认为在这种情况下，基于模型（model-based）的干预也有其用武之地。它们必须非常快，并且需要执行更智能的操作。但如果你查看数据，就会注意到数据中存在不完美之处，因为任何基于规则的处理都有一定的失败率。正如我们上次展示的，准确性确实重要，具体取决于你选择的工具。如果你使用 Resiliparse 或 Trafilatura，那么——我认为 Resiliparse 在这些扩展的 dclm 评估上表现优于其他工具。

---

I'll talk also briefly about PDFs. So there's Hugging Face work, which released a data set called FinePDFs. So PDF files, if you ever opened them up, not in a PDF reader, looks like this, and this needs to get rendered. So PDFs can be found on just web pages on the internet. And Common Crawl does have some PDFs. Generally, Common Crawl focuses on text, but sometimes, if you're just given a URL, you might not even know before you fetch it whether it's a PDF or not, if it doesn't have the extension. If you read this blog post, there's a lot of details, which I'll spare you of. For example, one thing is that many of the PDFs that are in Common Crawl are truncated because PDFs are big, so then that demands that recrawling is necessary. And then there's a question— once you have the PDF file, how do you actually convert it to text? And, some PDFs might be just scans as well. So they're essentially images. So there's a bunch of tools that this paper tried out, but mostly this involves running OCR using a VLM. And this obviously can be much more expensive than what we were doing before with text. Fortunately or unfortunately, the PDFs are a very small fraction of the whole internet. But they are very valuable because generally, if you bother to make a PDF, that means you probably have something interesting to say as opposed to a web page. So the quality of an average PDF is generally higher than for HTML file. There's a lot of cleanup and filtering. And PDFs, more so even than web pages, a lot of layout information is missing, because in HTML you have various tags like h1 and p that gives you some semantic information. PDFs are, by design, all about layout. So you don't necessarily preserve the semantic structure. So there's a bunch of transformation that happens.

我还会简要谈谈 PDF。Hugging Face 发布了一个名为 FinePDFs 的数据集。如果你不在 PDF 阅读器中打开 PDF 文件，它看起来就像这样，需要被渲染。PDF 文件可以在互联网的网页上找到，Common Crawl 中也有一些 PDF。通常 Common Crawl 主要关注文本，但有时如果你给了一个 URL，在抓取之前你甚至可能不知道它是不是 PDF（如果没有扩展名的话）。如果你阅读这篇博客文章，会有很多细节，我就不赘述了。例如，Common Crawl 中的许多 PDF 被截断了，因为 PDF 文件很大，这就要求必须重新爬取。还有一个问题是：一旦你有了 PDF 文件，你如何真正将其转换为文本？而且，有些 PDF 可能只是扫描件，本质上就是图片。这篇论文尝试了一系列工具，但主要涉及使用视觉语言模型（VLM）运行光学字符识别（OCR）。这显然比我们之前处理文本要昂贵得多。有幸或不幸的是，PDF 只占整个互联网中非常小的一部分，但它们非常有价值，因为一般来说，如果你费心制作一个 PDF，说明你可能有有趣的内容要说，这不同于普通的网页。因此，平均而言，PDF 的质量通常高于 HTML 文件。PDF 需要大量的清理和过滤。而且相比网页，PDF 丢失了更多的布局信息，因为在 HTML 中你有各种标签（如 h1 和 p），提供了一些语义信息；而 PDF 的设计本质上完全是关于布局的，所以你并不一定能保留语义结构。因此，需要进行大量的转换工作。

---

At this point, you have text, but you're not done. You're far from done. So the next step is filtering. So I'm going to talk somewhat abstractly about what filtering is. Here's the building block. So suppose you have some target data that you want to get. This is usually a small amount of high-quality data and lots of raw data. This is the fresh shipment of the tokens that you transformed from the previous step. And the goal is to find a subset of this raw data that is similar to target. So this is the general skeleton for filtering, and almost all kinds of filtering falls into this schema.

到了这一步，你有了文本，但还没有完成，远未完成。下一步是过滤（filtering）。我将稍微抽象地谈谈什么是过滤。这是基础框架：假设你有一些你想要获取的目标数据（target data），通常是一小部分高质量数据，以及大量的原始数据（raw data）——这是你从之前步骤转换得到的"新鲜"标记。目标是找到原始数据中与目标相似的一个子集。这就是过滤的一般框架，几乎所有类型的过滤都遵循这个模式。

---

So filtering, there's many reasons you might want to filter. If you're training an English language model or a German language model, you might want to identify the language and filter things that don't match that language. The main reason for filtering is quality filtering. You want to find things that are high quality as opposed to low quality. You don't want just spam. You want encyclopedic information. And then another application is toxicity filtering. Of course, the internet has plenty of nasty content, and maybe you don't want to train your language model on that. So, for a filtering algorithm, you want some generalization from the target data, because you already have the target data. You don't want to only get the target data, but you also want it to be extremely fast because you have to run it on the whole internet. So this could be 100 trillion tokens worth of data. So generally, filtering is you end up with a very small fraction, a single-digit fraction of your entire data.

关于过滤，你想进行过滤的原因有很多。如果你在训练一个英语语言模型或德语语言模型，你可能需要识别语言并过滤掉不匹配该语言的内容。过滤的主要原因是质量过滤（quality filtering）——你想找到高质量的内容，而不是低质量的。你不只是想要垃圾信息，你想要百科全书式的信息。另一个应用是毒性过滤（toxicity filtering）。当然，互联网上有很多不良内容，你可能不希望你的语言模型在这些内容上进行训练。因此，对于过滤算法，你希望从目标数据中获得一定的泛化能力，因为你已经有了目标数据。你不仅希望获得目标数据，还希望算法极其快速，因为你必须在整个互联网上运行它，数据量可能高达 100 万亿个标记。通常，过滤后你得到的数据只是整个数据中非常小的一部分，是个位数的百分比。

---

OK. So remember the general framework given the target, and raw, you're trying to find a subset. So the general scheme is that you estimate some model based on R and T and derive a scoring function, and then you keep the examples in R based on their score. So typically, there are two types of classifiers. One are generative models. So this is basically you have your target data. You can just estimate a model of that data. And remember, this has to be cheap, so probably you're not training a big language model. Generally, KenLM basically says I'm going to train a 5-gram model. A more common thing, which I think we're mostly seeing these days, is just training a classifier. And the classifier says, I'm going to predict a positive label, for example, that are in T, my target, and negative labels for things that are in raw but not in T. So basically, it looks like T are your positive examples, some random subset of R are your negative examples. Maybe you balance it, and then you train a classifier. And the tool that people generally use is fastText because it's fast. And generally, it's just a linear classifier—a bag of words. And then once you have this model now for every new document, you can score it, and you set some appropriate threshold, depending on your quality bar, and you keep the examples. Sometimes stochastically, sometimes not. So this is very much a model-based filtering approach.

好，记住这个通用框架：给定目标数据 T 和原始数据 R，你试图找到一个子集。通用方案是：你基于 R 和 T 估计某个模型，推导出一个评分函数，然后根据分数保留 R 中的样本。通常有两类分类器（classifier）。一类是生成式模型（generative models）：你拥有目标数据，你可以直接对该数据估计一个模型。记住，这必须廉价，所以你可能不会训练一个大语言模型。通常，KenLM 基本上就是训练一个 5-gram 模型。更常见的做法——我认为这是当前的主流——就是直接训练一个分类器。这个分类器会预测正标签（例如，属于目标 T 的样本）和负标签（属于原始数据 R 但不属于 T 的样本）。基本上，T 是你的正例，R 中的某个随机子集是你的负例，你可能进行平衡，然后训练一个分类器。人们通常使用的工具是 fastText，因为它速度快，而且通常只是一个线性分类器（linear classifier）——词袋模型（bag of words）。一旦你有了这个模型，对于每一个新文档，你都可以给它打分，然后根据你的质量门槛设置一个适当的阈值，保留那些通过的样本——有时是随机地，有时不是。这本质上就是一种基于模型的过滤方法。

---

Remember from the last lecture, there are many data sets from generally a few years ago that did not use model-based filtering because they wanted to not bias things too much. These days, I think basically everyone does some amount of model-based filtering because unless you are compute-plentiful, in which case you probably don't need to do as much filtering—you can just train on everything. Most people are compute-poor. You have to be very smart about how you're filtering; otherwise, you're just wasting flops on low-quality content.

从上次课还记得，几年前有很多数据集并没有使用基于模型的过滤，因为他们不想引入太多偏差。而如今，我认为基本上每个人都会做一些基于模型的过滤，因为除非你算力充足——那样的话你可能不需要做太多过滤，可以直接在全部数据上训练——否则大多数人的算力是有限的。你必须非常聪明地进行过滤，否则你就是在低质量内容上浪费算力。

---

OK, so let me talk through some instantiations of filtering. So remember, I mentioned language identification. So the goal is just to find—given a piece of text, detect whether it's of a particular language. So Meta has trained this set of fastText language identification models, which often you can just use off the shelf. So it supports 176 different languages. It's been trained on a bunch of multilingual sites. So Wikipedia, remember, has a lot of languages. There's also translation sites and sites for different languages. So a language ID is generally a fairly easy problem compared to many other tasks that we're dealing with—so a simple classifier. If you look at a few words, you can tell that it's Spanish or Japanese. Now, there are subtleties because of code-switching and text, and there's some dialects. So I wouldn't say it absolutely solved problem, but this is not really the bottleneck for training a good language model. And then you can just—so once you have your classifier, you just choose some threshold. This is generally fairly heuristic.

好，让我讲解一些过滤的具体实例。还记得我说过的语言识别（language identification）吗？目标是：给定一段文本，检测它是否属于某种特定语言。Meta 训练了一套 fastText 语言识别模型，你通常可以直接使用现成的。它支持 176 种不同的语言，在大量的多语言站点上进行了训练。Wikipedia 有很多语言，还有翻译网站和各种语言的网站。语言识别与我们处理的其他许多任务相比，通常是一个相当简单的问题——只是一个简单的分类器。只看几个词，你就能判断它是西班牙语还是日语。不过，由于代码切换（code-switching）、文本以及一些方言的存在，也存在一些微妙之处。所以我不敢说这是一个完全解决的问题，但这并不是训练一个好语言模型的真正瓶颈。然后一旦你有了分类器，只需选择一个阈值即可——这通常是相当启发式的。

---

So another thing you can do with filtering is that, suppose you're looking for data of a certain type. So let's say you want to get really good at math, so you want to go and find a bunch of math data. So OpenMathText is this paper from 2023, where the goal is to create a large corpus of math text. This pipeline consists of a few steps. So it's not training a single classifier. So first, you use some rules to filter. Does it contain latex commands? They also use KenLM. So this is a generative approach. And trained it on the ProofPile, which is a known data set of math, and keep it if the perplexity is below some threshold. And then you also train a fastText classifier to predict whether it's mathematical writing or not. And there's two different thresholds if it has latex in it, then it's a higher bar—sorry—it's a lower bar, but if it doesn't have latex in it, it's a higher bar. And then, as a result, they got 15 billion tokens, which they use to train models. And there's a paper that showed that this more targeted, curated data collection results in models that are better at math than models that were trained on 20 times as much data, which were not filtered in this way.

通过过滤你可以做的另一件事是：假设你在寻找某种类型的数据。比如说，你想在数学方面变得非常擅长，所以你想去找到一堆数学数据。OpenMathText 是 2023 年的一篇论文，目标是创建一个大规模的数学文本语料库。这个流水线包含几个步骤，而不是训练一个单一的分类器。首先，你使用一些规则进行过滤：它是否包含 LaTeX 命令？他们还使用了 KenLM——这是一种生成式方法——在 ProofPile（一个已知的数学数据集）上进行训练，如果困惑度（perplexity）低于某个阈值就保留。然后你还训练一个 fastText 分类器来预测它是否属于数学写作。这里有两个不同的阈值：如果包含 LaTeX，门槛较低（lower bar）；如果不包含 LaTeX，门槛较高（higher bar）。结果，他们获得了 150 亿个标记，用于训练模型。有一篇论文表明，这种更有针对性的、经过策划的数据收集方式，训练出的模型在数学方面比那些在 20 倍数据量但未经过如此过滤的数据上训练的模型更优秀。

---

So the quality filtering again, think about it as a tool. You can define quality however you want. There's no universal notion of quality. If you want to define quality to be math, then you can go and get math, and you get better at it. So GPT-3, I think I mentioned this last time, but just to put it in this framework. So positive examples are Wikipedia, WebText. So these are pages that link out from high-star Reddit posts, and some books. And negatives are generally sampled from the web. They train a linear classifier and keep documents if the linear classifier is scored highly enough. There's the first LLaMA paper. The positives were pages referenced by Wikipedia, not Wikipedia articles themselves. And it's this same idea. So phi-1 from Microsoft is interestingly also falls into this framework. So they started with—the raw data is not already a Python subset of the stack. Remember this is all code. And they define a prompt, which determines educational value. And then they use GPT-4 to classify a subset of R, 100k subset of R with this prompt, and the ones that are positive are kept and called the target. So the target here is actually the output of an expensive classifier. And then you train a cheaper classifier, in their case, a Random Forest, but you could have probably used fastText as well. And then you select data that is classified positive by this classifier. And they also showed that using this data set, you do much better than if you're just using the raw data. So this performance goes up in fewer steps to a higher value.

所以，质量过滤再次强调——把它看作一个工具。你可以根据自己的需要来定义质量，没有通用的质量概念。如果你想将质量定义为"数学"，那么你可以去获取数学数据，你的模型就会在数学上做得更好。GPT-3——我上次提到过——把它放在这个框架里来看：正例是 Wikipedia 和 WebText（从高赞 Reddit 帖子链接出去的页面）以及一些书籍；负例通常从网络上采样。他们训练一个线性分类器，并保留得分足够高的文档。第一篇 LLaMA 论文也是如此：正例是 Wikipedia 引用的页面（而不是 Wikipedia 文章本身）。同样的思路。微软的 phi-1 也很有意思地落入了这个框架：他们的原始数据已经是 The Stack 的 Python 子集了，他们定义了一个用于判断"教育价值"的提示（prompt），然后使用 GPT-4 对 R 的一个 10 万子集进行分类，保留那些正例并称为目标数据。所以这里的目标数据实际上是一个昂贵分类器的输出。然后你训练一个廉价的分分类器（在他们案例中是随机森林 Random Forest，但你也可以使用 fastText），再选择被该分类器判定为正例的数据。他们还表明，使用这个数据集，效果比仅使用原始数据好得多——性能在更少的步骤中就达到了更高的值。

---

So toxicity works the same way. There's this Dataset—Jigsaw Toxic Comments, where it came from this project where the goal is to help people have better discussions online. So here the data is the Wikipedia talk pages, which can, I guess, for controversial sites get quite heated. And this has been annotated with whether there are any toxic comments on there. And you can similarly define positive and negative examples, and you can train a classifier on that.

毒性过滤的工作方式也是一样的。有一个数据集叫 Jigsaw Toxic Comments，它来自一个旨在帮助人们在线上进行更好讨论的项目。这里的数据是 Wikipedia 的讨论页，对于一些有争议的站点，讨论可能会相当激烈。这些数据已经被标注了是否包含任何有毒评论。你可以类似地定义正例和负例，并训练一个分类器。

---

So now I think you have the tools, or some examples and inspiration. You can identify a particular type of data that you want. You build a classifier for it, and then you can go filter Common Crawl for that. I want to talk about one subtlety here, which is that—no, the notion of what you want for data actually depends on what model you want to train. So in particular, it depends on the number of tokens you're training on. And so there's no optimal threshold. So before, when I looked at the classifier, it gives you a score. You can't say 0.9 and say that's the best because it depends on what you want to do. Intuitively, if you are going to train for a longer period of time, then you can tolerate lower quality data. If you're training for shorter, then you want higher quality data, in general. And of course, if you could wave a magic wand, if you're training for longer, you want more high-quality data, but that's not an option that you're given. The data pool is what it is.

所以现在我认为你有了工具、一些示例和灵感。你可以识别出你想要的那种特定类型的数据，为其构建一个分类器，然后去 Common Crawl 中进行过滤。我想在此讨论一个微妙之处：你想要的"好数据"的定义实际上取决于你想训练什么模型。具体来说，它取决于你训练的标记数量。因此，不存在最优阈值。之前当我谈到分类器时，它会给你一个分数，你不能说 0.9 就是最好的，因为这取决于你想做什么。直观上来说，如果你要训练更长时间，那么你可以容忍较低质量的数据；如果你训练时间较短，那么你通常需要更高质量的数据。当然，如果你能挥动魔法棒，训练更长时间时你当然想要更高质量的数据，但这不是你能选择的——数据池就是那样。

---

So here's a preliminary experiment that Michael Ryan did. So basically, this plot shows for a 157-million parameter model. We're taking a very small pool. So 100 works, which is a tiny fraction of Common Crawl. And we're training and training for more over time. So let's take a look at the blue curve. So the blue curve is dclm. And so the loss starts here. And then it comes down. And each of these lines is when you epoch over the data. So this is one epoch, and then the next blue is the second epoch, and so on and so forth. So there's not that much data. So eventually, you have to repeat your data. And the loss continues going down because the second time you look at the data, you're still learning things. And at some point, you start to overfit. Whereas if you look at Resiliparse, this is basically no filtering. So here, it's much worse in the beginning. But as you continue and continue, at some point, you also epoch. It starts to go down slower. So you see this trend where high-quality data is better in this regime, where you're not epoching. But once you get to lots and lots of tokens, high-quality data is no longer that great. And of course, with high-quality data, you wouldn't want to go into this regime because you're overfitting—you probably stop here. But even at this point, this is worse than if you had trained for longer using low-quality data.

这是 Michael Ryan 做的一个初步实验。这个图展示了一个 1.57 亿参数的模型。我们使用了一个非常小的池子——100 个 words，这只是 Common Crawl 的极小一部分。我们持续训练，每次训练更多步数。我们来看蓝色曲线，蓝色曲线是 dclm 的结果。损失从这里开始，然后下降。每一条线代表你在数据上跑了一个 epoch（周期）。这是第一个 epoch，下一条蓝线是第二个 epoch，依此类推。数据量不大，所以最终你不得不重复使用数据。损失持续下降，因为第二次看这些数据时，你仍然在学习东西。但在某个点上，你开始过拟合（overfit）。而如果你看 Resiliparse（基本上没有过滤）的结果，开始时效果差得多，但随着你持续训练，到了某个点你也开始重复 epoch，损失下降变慢了。你可以看到这个趋势：在你不重复 epoch 的阶段，高质量数据更好；但一旦你训练了非常多的标记，高质量数据就不再那么好了。当然，对于高质量数据，你不想进入这个重复阶段，因为你会过拟合——你可能就在这里停止了。但即使在这个点上，效果仍然比用低质量数据训练更长时间要差。

---

Yeah. Just a question about computing the metrics. This is actually not totally about the graph. Each of those dots corresponds with one training run, right? Yes. Do you ever need to do the confidence interval when you're doing these retraining experiments, or is it enough just to do it one time? So the question is, each of these points is a single training run, should you do it multiple times and get confidence intervals? Ideally, that would be a good practice. Often, you'll see in these papers that these are scarce because each training run is fairly expensive. But in reality, when we have done these experiments, it's generally tends to be stable, I would say, at least for pre-training.

好。有一个关于计算指标的问题。实际上不完全是关于这张图。每个点对应一次训练运行，对吗？是的。当你做这些重训练实验时，你是否需要做置信区间（confidence interval），还是只做一次就够了？问题是：每个点都是一次单次训练运行，你是否应该做多次并计算置信区间？理想情况下，这是一个好的实践。你经常会在这些论文中看到，这些运行是稀缺的，因为每次训练运行都相当昂贵。但事实上，当我们做这些实验时，结果通常趋于稳定——至少对于预训练来说是这样。

---

Yeah. So you mentioned training for longer and high-quality data, is that not a combination that we're considering? But if we are training longer on this high-quality data, would it have diminishing returns compared to training for longer with the high-quality data? Yeah. So the question is, if you were able to get higher quality data and you trained for longer, would it still have diminishing returns? Every data set is going to have diminishing returns eventually. That's finite. But it would probably be here. It would just be down here and just keep on going down.

好。你提到了更长时间的训练和高质量数据，这个组合我们不考虑吗？但如果我们在这个高质量数据上训练更长时间，它是否会有递减的回报？问题在于，如果你能获得更高质量的数据并且训练更长时间，它是否仍然会有递减的回报？每个数据集最终都会呈现递减的回报，数据是有限的。但它可能就在这里——它会在更低的损失处，并持续下降。

---

OK. Great. Let's move on. So summary, filtering is pretty critical for building a good model, especially when you're compute-constrained like most of us. Technically, if you have infinite compute, you don't need to filter. And you can train on everything, and it'll be a giant model. But realistically, everyone has to filter. So the recipe here is figure out what good data looks like. And then you can train a classifier, and that will extrapolate to the rest of your model. And what good data looks like? You can either find it by saying, aha, there's this data set out there that I really like and I just want more of it. Or you can craft a prompt to a language model and then use that to construct, to do a preliminary filter of a large pool, and then use that good quality data to train a smaller classifier and extrapolate to everyone else.

好，我们继续。总结一下，过滤对于构建一个好模型非常关键，尤其是当你像大多数人一样受到计算资源限制时。从技术上讲，如果你有无限的计算资源，你不需要过滤，你可以在所有数据上训练，它会是一个巨大的模型。但现实中，每个人都必须过滤。所以方法是：搞清楚好数据长什么样，然后你可以训练一个分类器，它将推广到你模型的其余数据。好数据长什么样？你可以这样找到它："啊，有一个我非常喜欢的数据集，我只想要更多这样的数据。"或者你可以编写一个提示给语言模型，用它来对一个大的数据池做初步过滤，然后用那些高质量数据来训练一个较小的分类器，并推广到所有其他数据。

---

Next, I'm going to talk about deduplication. So at this point, we have filtered our data set. So we only have what we deem to be high-quality data. But often, data still has duplicates in it. And there's two types of duplicates. There's exact duplicates. So this happens when, for example, if you look at these mirror sites, the whole point of a mirror is that it's a duplicate. And sometimes the web crawler isn't smart enough to know that this mirror is exactly this mirror, so it just crawls many sites, and you'll get this exact same content. Also, when you fork a repo, that is also a duplicate, even if you make changes. Probably you're making changes to a few files, so 99% of that repo might be the same. So duplicate is abundant. And yeah, sometimes there's actually near duplicates which are not mirrors or derivative, but they just happen to be the same text differing by a few tokens.

接下来，我要讲去重（deduplication）。到此为止，我们已经过滤了数据集，只保留了我们认为高质量的数据。但数据中通常仍然包含重复内容。有两种类型的重复。一种是精确重复（exact duplicates）：例如，当你查看镜像站点时，镜像的全部意义就在于它是重复的。有时网络爬虫不够智能，无法识别这个镜像和那个镜像完全相同，于是它爬取了多个站点，你就得到了完全相同的内容。此外，当你复刻（fork）一个仓库时，那也是重复，即使你做了修改——你可能只修改了几个文件，所以仓库中 99% 的内容可能是一样的。因此，重复内容非常丰富。是的，有时还存在近似重复（near duplicates），它们不是镜像或衍生作品，但恰好是仅相差几个标记的相同文本。

---

Usually, probably this came from—it could be copying or came from a different common source. So here are some examples of near duplicates. So terms of service and licenses. So I guess the MIT license probably shows up on a lot of places. And so in many cases, it is a exact copy, but only of that license, unless someone made a typo when they copied it. But the rest of the page that the license might be part of might be different. And we talked about how a lot of websites have the same headers and footers. Those are also duplicates. There's also cases where, for whatever reason, this is from LM1B, so the 1 billion per benchmark. There's these articles where you just have typographic differences. There's one version with a comma and one version without a comma. I don't really know why, but that happens. And sometimes you see these templates where this is some probably low-quality content, where it essentially looks like an ad or some sort, and someone just templatized and replaced Canada with USA. So if you train on this data, but you are just training on different variations of this with different entities, this is going to be wasting your GPUs.

通常，这些可能来自于复制，或来自某个通用的共同来源。以下是一些近似重复的例子：服务条款和许可证——MIT 许可证可能出现在很多地方，在许多情况下它是精确副本（至少许可证本身是），除非有人在复制时打错了字。但许可证所在的页面其余部分可能不同。我们还谈到很多网站有相同的页眉和页脚，那些也是重复内容。还有一些情况，比如 LM1B（1 Billion Word Benchmark）中的数据，有一些文章只有排版上的差异——一个版本有逗号，另一个版本没有逗号，我不知道为什么，但确实发生了。有时你会看到一些模板化的、可能是低质量的内容，看起来像广告之类的，有人只是把它模板化了，把 Canada 替换成了 USA。如果你在这样的数据上训练，你只是在训练不同实体替换后的不同变体，这是在浪费你的 GPU。

---

There's a more extreme cases. So this is why it's good to look at your data. So this audit of the C4 data set found this product description 61,000 times in the data set. And if you trace back—this is really bizarre. I don't know why. This is some description of this gas mask. And this just showed up in this data set in Common Crawl 61,000 times. So yeah, the web is weird.

还有更极端的例子。这就是为什么查看你的数据是好的。C4 数据集的一次审计发现，这条产品描述在数据集中出现了 61,000 次。如果你追溯回去——这真的很奇怪，我不知道为什么——这是一个防毒面具的描述，它就在 Common Crawl 的这个数据集中出现了 61,000 次。是的，网络世界无奇不有。

---

So why deduplicate? So the first idea is clear because you want to train more efficiently. Deduplication reduces your data set size without really losing information because you're just removing duplicates. And it also has this benefit of avoiding memorization, which this paper talks about. For example, if you have some copyrighted content that's duplicated a lot, then if you train on it, then you'll memorize it, and also privacy concerns. But mostly, I think, it's just to make sure that you're not wasting flops. Related to deduplication is also decontamination, which is arguably even more important, too. And it's the same deal, is that you want to make sure that your test set is not in your training set.

那么为什么要去重？第一个原因很清楚，因为你希望更高效地训练。去重减少了数据集的大小，而不会真正丢失信息，因为你只是在移除重复内容。它还有一个好处是避免记忆化，正如这篇论文所讨论的。例如，如果你有一些被大量复制的受版权保护的内容，那么在训练时你会记住它，这还涉及隐私问题。但我认为，最主要的是为了确保你没有浪费算力。与去重相关的还有污染去除（decontamination），这可能甚至更重要。同样，你需要确保你的测试集不在训练集中。

---

So how do we dedupe? So here's the design space to think about. So first of all, what are the items that you're deduping? Do you do at the sentence level, the paragraph level, or the document level? How do you determine a match? Is it an exact match? Is it existence of a common subitem? Is it the fraction of common subitems for near deduplication? And then once you find a duplicate between two pages, what do you do? Do you remove all the instances, or do you remove all but one? And the key algorithmic challenge is that deduplication is fundamentally about comparing items to other items. And normally, if you're doing filtering, this is about an individual item. Is this item good or not? And this can be parallelized. It's linear time, which is good. And even in linear time, we're trying to make it fast by having rule-based or very small models. But your duplication, clearly, you can't do the n-squared thing where you compare everything to everything. You need linear-time algorithms to scale, especially at this web scale. So typically, the deduplication literature uses hash functions to get around this. So we'll develop some of these ideas. These are quite nice ideas from—thanks to the algorithms community.

那么我们如何做去重呢？这里有一些设计空间需要考虑。首先，你去重的对象是什么？是在句子级别、段落级别还是文档级别？你如何判定匹配？是完全匹配，还是存在公共子项，还是公共子项的比例（用于近似去重）？一旦你在两页之间发现了重复，你做什么？是移除所有实例，还是保留一个？关键算法挑战在于，去重本质上是在比较一个条目与另一个条目。而通常，过滤是针对单个条目的——这个条目好不好？这可以并行化，是线性时间，这很好。即使在线性时间内，我们也试图通过基于规则或非常小的模型来使其更快。但去重，显然你不能做 n 平方的比较——把每个东西和每个东西比较。你需要线性时间算法才能扩展，尤其是在网络规模下。所以通常去重文献使用哈希函数来解决这个问题。我们将展开这些思路，这些是非常好的思路——感谢算法社区。

---

So I think everyone knows what a hash function is. It takes some value like a string, and maps it into something like a string or an integer. And the hash value is much smaller than item. Hash collisions are when two distinct items map to the same age. So when you look at hash functions, there are really fancy hash functions which are cryptographic in nature. These are collision-resistant using cryptography and Bitcoin and things like that. And then there's these faster ones, which are used for hash tables, where hash collisions aren't the end of the world. And so we'll be using these. So take a string and map it to some values. That's what hash functions do.

我想每个人都知道哈希函数（hash function）是什么。它接收一个像字符串这样的值，并将其映射为像字符串或整数这样的东西。哈希值比原始条目小得多。哈希碰撞（hash collision）是指两个不同的条目映射到同一个值。当你看哈希函数时，有非常高级的哈希函数，本质上是密码学性质的——这些是抗碰撞的，使用密码学、比特币等技术。还有更快一些的哈希函数，用于哈希表（hash table），在这些场景中哈希碰撞并不是世界末日。我们将使用这些。取一个字符串并将其映射到一些值——这就是哈希函数做的事。

---

OK. So exact duplication is conceptually very simple. You take a string, you see if there's an exact match, and you remove all but one. So here you have a bunch of elements, and you hash them, and you dedupe. And exact duplication is very nice. It's very clear what's happening. But this isn't really good enough for the messy web data because often you have these near duplicates. And one note is that there's many ways to have written this. This is written in a bit of a MapReduce style way, which makes it more easily parallelizable and scale. So, C4, this paper from the T5 paper, which processed Common Crawl, did exact deduplication. The items they operate on were three-sentence spans, and you do an exact match, and they remove all but one. So if you're paying attention, you realize that there's something a bit strange about this because you're looking at three-sentence spans. And if you find two documents with three-sentence spans and you remove all but one, that means you're just going to rip out three sentences from that documents, which is a little bit strange, because it breaks the coherence. But this is what they did. So that's exact deduplication.

好的，精确去重（exact deduplication）在概念上非常简单。你取一个字符串，检查是否有精确匹配，然后移除所有重复只保留一个。这里有一堆元素，你对其哈希，然后去重。精确去重很好，很清楚发生了什么。但对于凌乱的网络数据，这还不够好，因为你经常遇到近似重复。需要注意的一点是，有多种方式来实现它。这里的代码是以一种 MapReduce 风格编写的，这使得它更容易并行化和扩展。C4——来自 T5 论文的数据集——处理 Common Crawl 时做了精确去重。他们操作的对象是三个句子的跨度（three-sentence spans），进行精确匹配，并移除所有重复只保留一个。如果你仔细想，会发现这有点奇怪，因为你是在对三个句子的跨度做匹配。如果你发现两个文档包含相同的三句话跨度，然后移除所有但保留一个，这意味着你只是从文档中挖掉了三句话，这有点奇怪，因为它破坏了连贯性。但这就是他们做的。这就是精确去重。

---

So how do we do near deduplication? So first of all, we have to define what approximate match means here. So to do that, we're going to define this called Jaccard similarity, which is a fairly standard notion. And Jaccard of two sets is basically the size of the intersection over the size of the union. So given these two sets—1, 2, 3, 4, and 1, 2, 3, 5—when you compute Jaccard, you take the intersection. That's 1, 2, 3. You take the union, that's 1, 2, 3, 4, 5, and you divide, and Jaccard is 0.6. So Jaccard is a number between 0 and 1. 0 means that they're disjoint, 1 means that they're identical. So a fairly natural notion. And we're going to say that two documents are near duplicates if their Jaccard similarity is above some threshold, let's say 0.99.

那么如何做近似去重（near deduplication）呢？首先，我们必须定义什么算近似匹配。为此，我们将定义一种称为 Jaccard 相似度（Jaccard similarity）的度量，这是一个相当标准的概念。两个集合的 Jaccard 值基本上是交集大小除以并集大小。给定这两个集合——{1, 2, 3, 4} 和 {1, 2, 3, 5}——计算 Jaccard 时，你取交集 {1, 2, 3}，取并集 {1, 2, 3, 4, 5}，相除得到 Jaccard 为 0.6。Jaccard 是一个介于 0 和 1 之间的数值：0 表示不相交，1 表示完全相同。这是一个相当自然的概念。如果两个文档的 Jaccard 相似度高于某个阈值（比如 0.99），我们就说它们是近似重复的。

---

So now the question is, how do you find near duplicates in linear time? So fortunately, this is a solved algorithms question. And the answer is to use MinHash. Well, OK. So the first step is to use MinHash. That's not the final answer. So MinHash is a random hash function, so that the probability of a hash collision is exactly the Jaccard of A and B. So this is a very nice property because hashing is good for making things linear time. Jaccard is the metric that we want, and we're connecting these two right now in expectation. So what's interesting is normally, you want hash functions to define hash functions so that everything is hashing—distinct elements are hashing to different things. You don't want collisions. But here you actually want collisions—not arbitrary collisions, but you want to control the collisions in a certain way to align with the similarity. So similar things you want to collide more than disparate things.

那么问题来了：如何在线性时间内找到近似重复的文档？幸运的是，这是一个已被解决的算法问题。答案是使用 MinHash。不过，第一步是使用 MinHash，但这还不是最终答案。MinHash 是一种随机哈希函数，使得哈希碰撞的概率恰好等于 A 和 B 的 Jaccard 相似度。这是一个非常好的性质，因为哈希使得处理变为线性时间，Jaccard 是我们想要的度量，而我们在期望上将两者连接了起来。有趣的是：通常你希望哈希函数将不同的元素映射到不同的值，你不想要碰撞。但这里你实际上想要碰撞——不是任意的碰撞，而是希望以某种方式控制碰撞，使其与相似度对齐。你希望相似的事物比不相似的事物更容易碰撞。

---

So the MinHash is essentially, actually, let's see. Maybe I will—so here's the MinHash. It's fairly simple. You take a set, and you hash every element in that set, and you take the minimum element. So if you're seeing this for the first time, it may seem a little bit strange. Why are you taking the min? You can take the max, too. It doesn't really matter. It's just a way to break ties. So here's the picture that you should have in your mind. So if you have A, remember A contains 1, 2, 3, 4, and B contains 1, 2, 3, 5. So this is a characteristic matrix representation of these two sets. And so what the random hash function is doing is that it induces a permutation over the items. So it might be 4, 3, 1, 5, 2, or something else. And then you look at which item is first, according to this permutation in A, and which item is first in B. So each item has the same probability of being first. So if the random hash function puts 1 first, then first in A will be equal to first in B. And if it's 2 first, then it's the same. If it's 3 first, it's also the same. But if the random permutation puts 4 first, then the first element in A is going to be different from the first element in B, and same with 5. So look at this representation. Basically, the random hash function says elect one of these rows to be first. And then when the min is just telling me—the min equal of A equal to min of B is basically telling me whether that row is the same.

那么 MinHash 的本质是什么？这里给出 MinHash 的定义，它相当简单：你取一个集合，对该集合中的每个元素进行哈希，然后取其中的最小元素。如果你第一次看到这个，可能觉得有点奇怪——为什么取最小值？你也可以取最大值，实际上没关系，这只是一个打破平局的方式。你应该这样理解：假设 A = {1, 2, 3, 4}，B = {1, 2, 3, 5}。这是一个特征矩阵表示。随机哈希函数的作用是对元素进行一个随机排列，可能是 4, 3, 1, 5, 2 之类的顺序。然后你看在这个排列中，A 的第一个元素是什么，B 的第一个元素是什么。每个元素都有相同的概率成为第一个。如果随机哈希函数把 1 放在第一个，那么 A 的第一个元素等于 B 的第一个元素；如果 2 是第一个，也一样；如果 3 是第一个，也一样。但如果随机排列把 4 放在第一个，那么 A 的第一个元素就不同于 B 的第一个元素，5 也是如此。所以，随机哈希函数本质上就是"选举"这些行中的某一行为第一行。MinHash 告诉我 A 的最小值是否等于 B 的最小值，这告诉我这一行是否相同。

---

OK. So that is, I guess, the proof of why this property holds, which is that you have a hash function in expectation over your random choice of hash functions, that the probability of collision is the similarity metric you want. OK. So let's just check this in code. So I'm going to generate 100 different hash functions. Each hash function is given by a seed. And I just check whether the MinHash is equal to MinHash, and the estimated Jaccard. So I'm going to just look at the number of the fraction of matches, and you get 0.6. And the key thing with the MinHash is that I don't have to do the n-squared thing. I can compute the MinHash of A and the MinHash of B and MinHash of a different set, and I just look for collisions.

好，我想这就是为什么这个性质成立的原因：在你随机选择哈希函数的期望下，碰撞的概率就是你想要的相似度度量。我们在代码中验证一下。我将生成 100 个不同的哈希函数，每个哈希函数由一个种子（seed）确定。然后检查 MinHash 是否等于 MinHash，并估计 Jaccard 值。看一下匹配的比例，你得到了 0.6。MinHash 的关键在于，我不需要做 n 平方的比较。我可以计算 A 的 MinHash、B 的 MinHash 以及其他集合的 MinHash，然后直接查找碰撞即可。

---

Any questions so far about MinHash?

目前为止关于 MinHash 有什么问题吗？

---

So now we can hash our items, but we're not done yet because a collision doesn't tell us the Jaccard is above some threshold, which is what we want. We want to find A and B such that Jaccard is greater than 0.99. All we've done is said, OK, well, if we've got a collision, the probability of that collision of two things colliding is the Jaccard. But that's not really that useful by itself. It's stochastic, and I can't really get anything reliable here. So the next idea is this thing called locality-sensitive hashing, which essentially solves this problem. So this is a very classic idea in theoretical computer science, and it's quite nice.

现在我们可以对条目进行哈希了，但还没有完成，因为一次碰撞并不能告诉我们 Jaccard 是否高于某个阈值——而这正是我们想要的。我们想要找到 A 和 B，使得 Jaccard 大于 0.99。我们只是说，如果发生了碰撞，两个事物碰撞的概率就是 Jaccard 值。但这本身并不那么有用——它是随机的，我无法从中得到可靠的信息。所以下一个思路是局部敏感哈希（Locality-Sensitive Hashing, LSH），它本质上解决了这个问题。这是理论计算机科学中一个非常经典且相当精妙的思想。

---

The idea here is that we have A and B colliding with probability equal to the Jaccard. So it is true that more similar items will collide more often, but it's very stochastic. The variance is quite large here. So our goal is to have A and B collide if the Jaccard is greater than some threshold. So we, in some sense, have to sharpen these probabilities somehow. The probability can't just be literally equal to the Jaccard. So the solution is to use more hash functions. And these hash functions are going to be independent. So this part gets a bit technical, but we'll walk through it.

这里的思路是：A 和 B 以等于 Jaccard 的概率发生碰撞。确实，更相似的条目碰撞频率更高，但这非常随机，方差很大。我们的目标是：如果 Jaccard 大于某个阈值，就让 A 和 B 碰撞。在某种意义上，我们必须以某种方式"锐化"这些概率，概率不能恰好等于 Jaccard。解决方案是使用更多的哈希函数，并且这些哈希函数是独立的。这部分会有点技术性，但我们一起来过一遍。

---

So you break the n hash functions into b bands of r hash functions. So if you have 12 hash functions, you have three bands, each band has 4 hash functions. So there's a band here, h1 through h4. Here's a second band, h5 through h8. Third band, h9 through h12. And then so what we're going to try to do—so each hash function gives us either a collision or not collision. And so every hash function, a probability of colliding. So the key here is that we want to say, compute the probability that A and B collide. We say that A and B collide if for some band all of its hash functions return the same value. So if h5 and h6 and h7 and h8 all return the same value—sorry—if h5 of A equals h5 of B and h6 of A equals h6 of B and so on, that means this band is triggered, and then I would say they're colliding. Or if this band, if all of these agree, then I say it's collision, or these two. But you don't have to have all the hash functions return the same value. So there's this and-or structure here that is doing the lifting here. And we'll see why this works.

你将 n 个哈希函数分成 b 个波段（bands），每个波段有 r 个哈希函数。例如，如果你有 12 个哈希函数，你可以有 3 个波段，每个波段 4 个哈希函数。这里有一个波段 h1 到 h4，第二个波段 h5 到 h8，第三个波段 h9 到 h12。每个哈希函数要么碰撞要么不碰撞。关键在于：我们想要计算 A 和 B 碰撞的概率。我们定义：如果存在某个波段，该波段中所有哈希函数都返回相同的值，则 A 和 B 碰撞。所以如果 h5 到 h8 都返回相同的值——即 h5(A)=h5(B)、h6(A)=h6(B) 等等——那么这个波段被触发，我认为它们碰撞了。或者如果这个波段的所有哈希函数一致，或者另一个波段一致。你不需要所有哈希函数都返回相同的值。这里的"与或"（and-or）结构就是关键所在。我们来看看为什么这样有效。

---

So now let's say you have a particular Jaccard of A and B, what is the probability that A and B collide according to this definition? So we can calculate this. So let's say that this Jaccard similarity is 0.8. And we have five bands, and each band has 10 hash functions. So then we can say, what is the probability of a fixed band matching? So that's 0.8 to the r. Because each band has r hash functions, so the probability that they all have to match is 0.8 to the r. So the probability of a fixed band matching is generally quite low. It's exponential in r. And then now the probability of collision is the probability that some band matches. And that's going to be the probability of 1 minus the probability of—so this is the probability of a band not matching. And if you raise it to the b—there's b bands—there's a probability that all of them don't match. And then 1 minus, that is the probability that some match. So the probability of collision is 0.4. And you're expected to be higher because you're given B tries to get a match.

假设 A 和 B 的 Jaccard 相似度为 0.8。我们有 5 个波段，每个波段有 10 个哈希函数。那么一个固定波段匹配的概率是多少？那就是 0.8 的 r 次方，因为每个波段有 r 个哈希函数，它们全部匹配的概率是 0.8^r。所以一个固定波段匹配的概率通常相当低，它是 r 的指数函数。那么碰撞的概率就是至少有一个波段匹配的概率。这等于 1 减去所有波段都不匹配的概率：一个波段不匹配的概率的 b 次方，然后用 1 减去它。所以碰撞概率为 0.4。你会期望它更高，因为你给了 b 次尝试来获得匹配。

---

So if you plot this, this is what it looks like. So you have on the x-axis the similarity here. And we were looking at 0.8. And you look at the probability of a collision here. So we would expect that if the similarity is 0, then it should be 0. If it's 1, it's 1. But notice that this is an interesting S-shaped, which is nice because this is what we wanted to sharpen. We wanted to basically say, if the similarity is below some threshold, then we want the probability to match to be as low as possible. And if the similarity is above some threshold, we want it to be as high as possible. So we're trying to get this to be like a phase transition. And if you plot this function as a function of similarity, that's what you get.

如果你把它画出来，就是这个样子。x 轴是相似度，我们刚才看的是 0.8，y 轴是碰撞概率。可以预期：如果相似度为 0，碰撞概率应为 0；如果为 1，则应为 1。但注意，这是一条有趣的 S 形曲线，这很好，因为我们想要的就是这样的"锐化"效果。我们想要的是：如果相似度低于某个阈值，匹配概率尽可能低；如果相似度高于某个阈值，匹配概率尽可能高。我们试图让它像相变（phase transition）一样。当你把碰撞概率作为相似度的函数画出来，就得到了这条曲线。

---

OK. So let's just look at some examples. So concretely, we have similarly 0.7 to 0.98. And we're going to look at how b equals 10, r equals 10. So we look at the collision probability, according to our definition. And we see that this gives us a range of 0.25 to 1. So if you were to set a threshold, this is not so bad. We can set it here. And these with some probability will—they're still false positives because, even if these are below a threshold, let's say 0.9, they might still collide. But we can filter them out if we want. But the ones above are mostly kept.

我们看一些具体例子。假设相似度范围从 0.7 到 0.98，b=10，r=10。根据我们的定义来看碰撞概率，我们看到范围从 0.25 到 1。如果你要设定一个阈值，这还不算太差。你可以把阈值设在这里。这些仍然会有假正例（false positives），因为即使它们低于阈值（比如 0.9），它们仍然可能碰撞。但如果我们愿意，可以将其过滤掉。而高于阈值的那些大部分都被保留了。

---

So what happens when you move—so increasing r. So remember, r is the number of hash functions within a bucket. So when you increase r, the threshold sharpens and moves the curve to the right. Everything becomes harder to match because you have more hash functions inside a bucket that sharpens that exponent. So the probability you see are sharper here, and now everything moves to the right. And now it's fairly unlikely that if something has a low Jaccard, you're going to match it. So before it was 0.25, and now it's 0.008. So we're sharpening the probabilities. And then increasing b has the effect of moving the curve to the left. It makes it easier to match. b is the number of bands. And some band has to match. If you have more bands, then there's more chances of matching. So if you look at this, then before and after. So now we're making—before this, 0.9 was only 0.72, and now it's 0.92. And of course, this also increases, but not by that much. And you can drive these phase transitions to be as sharp as you want by increasing b and r. But of course, if you can increase b and r too much, then it can be more expensive.

那么当你改变参数时会发生什么？增大 r（每个桶内的哈希函数数量），阈值会变尖锐，曲线向右移动。一切都变得更难匹配，因为桶内哈希函数更多了，指数变得更尖锐。概率在低相似度区域更低——之前是 0.25，现在变成 0.008。我们在锐化概率。增大 b（波段数量）则会使曲线向左移动，使匹配变得更容易。因为只要有任意一个波段匹配就算碰撞，波段越多，匹配的机会就越多。之前 0.9 的碰撞概率只有 0.72，现在变成了 0.92。当然，低相似度的概率也会增加，但幅度不大。通过增大 b 和 r，你可以让这些相变变得任意锐利。但当然，如果 b 和 r 太大，计算成本也会更高。

---

So let's look at a more real-world setting. So in this paper on deduplication, they had b, 20 bands, and r is 450. So it give you an idea of the magnitude of these numbers. And in general, the phase transition happens at a threshold, which is 1/b raised to the power of 1/r. So if you want to filter based on Jaccard greater than 0.9, then you basically have to set b and r such that this is 0.9. And then by changing b and r, you can make that phase transition sharper. So remember the probability of the fixed band matches is 1/b. If you are at this threshold, then the probability that A and B collide is approximately—it's a constant. So the probability of collision is 0.64. And this makes sense. So basically, if you have a phase transition, the center of that phase transition is 0.64. And everything below it should go to 0, as b and r increases, and everything above, it should go to 1 as b and r increases.

让我们看一个更真实的场景。在一篇关于去重的论文中，他们使用 b=20 个波段，r=450。这让你对数字的量级有个概念。一般来说，相变发生在阈值为 (1/b)^(1/r) 的地方。如果你想基于 Jaccard > 0.9 进行过滤，那么你基本上需要设置 b 和 r 使得这个值等于 0.9。然后通过改变 b 和 r，你可以让相变更尖锐。回想一下，固定波段匹配的概率是 1/b。当你处于这个阈值时，A 和 B 碰撞的概率约为一个常数——碰撞概率为 0.64。这很合理：如果你有一个相变，相变的中心约为 0.64。随着 b 和 r 增大，低于这个值的概率应趋于 0，高于这个值的概率应趋于 1。

---

Any questions about LSH? So this method is called MinHash LSH because LSH really works for any hash functions. For deduplication language model processing, we're using the MinHash, which approximates Jaccard. And so that basically is the one you should use here.

关于 LSH 有什么问题吗？这种方法被称为 MinHash LSH，因为 LSH 实际上适用于任何哈希函数。在语言模型处理中进行去重时，我们使用 MinHash，它近似于 Jaccard 相似度。这就是你应该在这里使用的方法。

---

Questions about dedupe?

关于去重有什么问题吗？

---

So one note about dedupe is that there's often, as we'll see, data sets that are coming in. And sometimes the deduplication will happen within a data set. But you actually have to do deduplication across your entire data set because often data sets can be redundant. So sometimes that's not done, but it should be.

关于去重的一点说明是：正如我们将看到的，数据集会不断加入。有时去重只在单个数据集内部进行，但实际上你必须在整个数据集上进行去重，因为不同的数据集之间常常存在冗余。有时这一点被忽略了，但应该要做。

---

Let's go on to the next topic, which is data mixing. So far, we've transformed our data from really raw HTML or PDFs into text. We filtered for high-quality. We deduped, so we have a smaller set of high-quality documents. And this generally happens for a given data source. But language models are trained on multiple data sources. So in Marin, currently, this website tracks the different data sources that the next model will be trained on. And you can see that there's a bunch of things. There's Nemotron, there's FinePDFs, which we talked about. There's some institutional books, and some code, and all these things. So you have all these different sources. And the question is, how do you combine these?

我们进入下一个话题：数据混合（data mixing）。到目前为止，我们已经将数据从原始的 HTML 或 PDF 转换为文本，进行了高质量过滤，做了去重，从而得到了一个较小的高质量文档集合。这通常是对单一数据源进行的。但语言模型是在多个数据源上训练的。在 Marin 项目中，目前这个网站追踪了下一个模型将要训练的不同数据源。你可以看到有很多东西：Nemotron、我们讨论过的 FinePDFs、一些机构书籍、一些代码等等。你有这么多不同的来源，问题来了：如何将它们组合起来？

---

So if you look at an older paper, The Pile, this is the set of sources that they had at that time. And they essentially assign a particular weight to each component. So basically, you have a distribution over sources. So where does that weight come from? So just cut and dry. Let's say you have three sources. You want to find a data mixture, and a data mixture is just a distribution over your sources. So if you're just thinking about this problem from first principles—well, not from first principles, but just from what you might do. Vibes, which is, I guess, the opposite of first principle, is you just manually set it based on some intuition, which is more often than you might think, what people do. So I think this is definitely fairly vibes-based. And even more recent papers, you just look at—maybe you use some method and then you just tweak things. You can also do uniform sampling, which is you just put a uniform distribution over your sources, and you sample every chunk. You just sample a source. You can also do proportional mixing, which is that you sample proportional to the number of tokens in a source. So if you have a data set with more tokens, then you put a higher weight. So this is also generally a rational thing to do. But you might worry that if you have a huge, low-quality data set, that's going to eat up a lot of your token. So it doesn't seem quite optimal either.

如果你看一篇较早的论文——The Pile——那就是他们当时使用的来源集合。他们给每个组成部分分配一个特定的权重。基本上，你有一个关于来源的分布。那么权重从哪里来呢？简单直接地说：假设你有三个来源，你想找到一个数据混合（data mixture），数据混合就是来源上的一个分布。如果你只是从第一性原理来思考这个问题——好吧，可能不是第一性原理，而是你可能怎么做——那就是"直觉"（vibes），这大概是第一性原理的反面：你基于一些直觉手动设置，这比你想像的还要常见。我认为这绝对是非常凭直觉的。即使是在更近期的论文中，你也会看到——可能使用了某种方法，然后微调一下。你也可以做均匀采样（uniform sampling）：在来源上放一个均匀分布，每次采样一个块，从一个来源中采样。你也可以做比例混合（proportional mixing）：根据来源中的标记数量进行比例采样。如果一个数据集有更多标记，你就给它更高的权重。这通常也是一个合理的方法。但你可能会担心：如果你有一个巨大但低质量的数据集，它会吃掉你很多标记的预算。所以这似乎也不是最优的。

---

So intuitively, you should upweight your higher quality sources. But there's two things that are important to keep in mind. One is that you do want to ensure some diversity. So often, sources are incomparable for literature, code, and papers. You can't really say that this paper is higher quality than this code because they're just incomparable objects, maybe. And if you want your language model to do well, you don't want to just put all your mass on papers. The second thing, which I will talk a bit more about, is each source is actually finite. So if you put too much weight on a small source, then you essentially run out of that source, and you need to just epoch over it, meaning that you keep on training literally the same tokens. And this is going to be bad for reasons we'll see.

所以直觉上，你应该提高高质量来源的权重。但有两件重要的事情需要牢记。第一，你确实需要确保一定的多样性。通常，文献、代码和论文这些来源是不可比的——你无法真的说这篇论文比这段代码质量更高，因为它们可能是不可比较的对象。如果你希望语言模型表现好，你不会想把所有权重都放在论文上。第二件事（我会多说一些）是：每个来源实际上是有限的。如果你对一个小来源赋予了太多权重，那么你基本上会用完该来源，需要重复 epoch 它，意味着你一遍又一遍地训练完全相同的标记。正如我们将看到的，这会导致不好的结果。

---

OK. So let's try to unpack this a little bit more concretely, this last point. So imagine you just have two sources—a low-quality source, you have 10 trillion tokens, and you have a high-quality source that has 10 billion tokens. Generally, high-quality sources are smaller. So if you just do a naive data mixture. Let's just do uniform. So half on high, half on low. And I'm going to train for 1 trillion tokens. So when I say train for 1 trillion, that doesn't mean unique tokens. It just means train for that many steps divided by batch size, essentially, or times batch size. So then let's look at this, which is the number of times a particular element in the low-quality data set was trained on. So that's the number of epochs a particular data point was trained on. So a p low times the trained tokens is the number of times I want to request tokens from this low-quality source, and divided by the total number of low-quality sources. So this is less than 1. So basically, that means 5% of the tokens in this low-quality data set, I'm going to touch and train on once. And then if you look at high quality, you'll see that the number of epochs is 50, because I only have 10 billion tokens here. And if I'm half-half, that means 500 billion tokens—I need to train up 500 billion tokens of high-quality data. But I don't have 500 billion tokens of data, so I have to repeat each data point 50 times. So this is actually really important. And some big model runs have messed this up. You can't just naively look at the data sets and define a distribution and then you sample, because if you just look at the quality, if you look at the data, you're missing how many data points are there. Does this make sense? Maybe pause for questions. This is an important point.

我们来更具体地拆解这最后一点。假设只有两个来源：一个低质量来源，有 10 万亿个标记；一个高质量来源，有 100 亿个标记。通常高质量来源更小。如果你做一个朴素的数据混合——就用均匀混合，高质量和低质量各一半——然后训练 1 万亿个标记。当我说训练 1 万亿，不意味着 1 万亿唯一标记，它只是意味着训练那么多步数乘以批大小。然后我们看一个低质量数据集中的特定元素被训练了多少次，即一个特定数据点被训练的 epoch 数。低质量的比例乘以训练标记数，就是我从低质量来源请求的标记数，再除以低质量来源的总标记数。这个值小于 1，意味着这个低质量数据集中只有 5% 的标记会被我触及一次。然后看高质量：因为只有 100 亿标记，各一半意味着我需要 5000 亿个高质量标记，但我没有那么多数据，所以我必须将每个数据点重复 50 次。这实际上非常重要。一些大模型训练搞砸了这一点。你不能只是天真地查看数据集、定义一个分布然后采样，因为如果你只看质量，你会忽略数据集里有多少数据点。这有道理吗？暂停一下，有问题可以问。这是一个重要的点。

---

Yeah. I guess, for the high-quality data, [INAUDIBLE] as [INAUDIBLE] low quality. Why do you need 50 epochs in the first place? Doesn't it achieve comparable performance a level that is way fewer? Yeah. So the question is, why do you need 50 epochs? And I guess the point is that you don't need 50 epochs. Worst case, it's wasting compute. Sorry, best case is wasting compute, and worst case, you're overfitting. The reason it's 50 is that if you just go in and you define this data mixture, then you're going to end up doing 50 epochs without realizing it, unless you're paying close attention. So this is basically—the lesson is look at how many epochs you're actually doing on your data.

好。我觉得，对于高质量数据，就像低质量数据一样……为什么一开始就需要 50 个 epoch？它不是在更少的 epoch 就能达到可比性能吗？问题是：为什么需要 50 个 epoch？答案是：你不需要 50 个 epoch。最坏情况是浪费算力，更坏情况是你在过拟合。之所以是 50，是因为如果你直接定义了这个数据混合，你会在不知不觉中做 50 个 epoch，除非你密切关注这一点。经验教训是：查看你实际上在数据上做了多少个 epoch。

---

How do the mixtures get expressed during training? When you switch every step, you train steps of 10, saying, oh, I want to do 10, Python code, 10 essays, because I feel like—is there also any intuition between what decisions are made there? Yeah. Good question. So the question is, when you train, how do the mixtures get realized? And so, in general, you just sample. So you want to fill a batch. So you can sample essentially for each element which mixture component it comes from. And you fill up a batch with sequences from that mixture component. Usually, every sequence comes from one mixture component. You're not sampling per token. So each batch should be mixed. So I guess the mixture assumptions are at the batch level, and then you train for that. It's not like, oh, it's one step is—the code in one step is—Yeah. In general, you want to reduce variance. You want to train for multiple—batch should have some mixture.

混合在训练过程中是如何体现的？当你每一步都切换时，你训练 10 步 Python 代码、10 步作文，因为你觉得……这些决策背后有没有直觉？好的问题。问题是：在训练时，混合是如何实现的？一般来说，你就是采样。你想填充一个批次，你可以为每个元素采样它来自哪个混合成分，然后用来自该混合成分的序列填充批次。通常每个序列来自一个混合成分，你不是按 token 采样的。所以每个批次应该是混合的。混合假设是在批次级别上的，然后在上面训练。并不是说一步全是代码。通常，你想减少方差，批次应该有一定的混合。

---

OK. So this problem has been noticed quite a long time ago. And so in this paper, they introduced the UniMax. And in that case, they were training in multilingual models. And it was very clear that some languages were very low-resource, so you had to do something about this. So, in this paper, they noticed that before some works would essentially take the proportional mixing and raise it to some power to flatten it out the distribution. But the idea in this paper is that let's be a bit more explicit about that. Let's sample the sources uniformly, but with a hard cap on the number of epochs. So this is the key idea. Here, you say I'm only going to take 20 epochs over a particular data source. So if you've done that, then too bad. You don't get any more tokens. You move on to the next thing. So this is like a safety net in some sense.

这个问题其实在很久以前就被注意到了。在这篇论文中，他们提出了 UniMax。在那个案例中，他们在训练多语言模型。很明显，有些语言是非常低资源的，所以你不得不对此做些什么。这篇论文注意到，之前的一些工作基本上是取比例混合结果，再对其施加一个幂次以展平分布。而这篇文章的想法是更明确地处理这个问题：让来源的采样均匀化，但对 epoch 数量设置硬上限。这就是关键思想。这里，你规定只会在某个特定数据源上训练 20 个 epoch。一旦达到上限，就不会再从这个来源获得更多标记了，继续下一个。这在某种意义上就像一个安全网。

---

So in particular, if you look at the number, the probability assigned to a source times the number of training tokens, that should be less than or equal to the cap. And there's a simple procedure for actually determining the mixture subject to this constraint. So let's switch gears a little bit and talk about how we define the mixture in the first place, because if you have 50 sources, there's 50 numbers you have to fill. And we notice that proportional mixing isn't really enough. Maybe you can try to estimate some quality metric, and then you can sample proportional to that, but that is also heuristic. So the most principled methods and most easiest to understand what's happening is these regression-based mixing methods, or RegMix, Olmix, and other papers like this.

具体来说，如果你看这个数值：分配给一个来源的概率乘以训练标记数，应该小于或等于上限。有一个简单的方法可以在这一约束下确定混合比例。现在我们稍微换一下话题，谈谈最初是如何定义混合的。如果你有 50 个来源，你就需要确定 50 个数值。比例混合并不足够。也许你可以尝试估计一个质量指标，然后按比例采样，但这也是启发式的。最原则性且最容易理解的方法是这些基于回归的混合方法——RegMix、Olmix 以及类似的论文。

---

And the idea here is relatively simple. So first, let's say you're trying to train a large-scale model. So you go to a small scale, let's say 300 million parameters, and you try different data mixtures. So let's say you have three components. You try different mixtures. And then you train these small models. You train a swarm of small models. Each model gives you a loss on some target metric. It could be some downstream values. It could be perplexity, whatever you want. So then you use these data points to basically fit a regression where the regression model maps these inputs, which is the data mixture weights, to the loss. So now you have basically a very cheap model that tells you, if I were to train on this mixture, what loss do I get? Then you can essentially optimize that data mixture—sorry—optimize that function for the optimal data mixture. And then that is the data mixture you use to train the large-scale model. So that's the simple procedure. And you notice some similarities with scaling laws, where you're trying to do some cheap computations to figure out some answers, and then scale up.

这个想法相对简单。首先，假设你要训练一个大模型。你先把规模缩小，比如 3 亿参数，尝试不同的数据混合。假设你有三个成分，你尝试不同的混合比例，然后训练这些小模型。你训练一群小模型，每个模型在某个目标指标上给你一个损失——可以是某些下游任务的值，可以是困惑度，什么都可以。然后你用这些数据点来拟合一个回归模型，该回归模型将输入（数据混合权重）映射到损失。现在你有了一个非常廉价的模型，它可以告诉你：如果在这种混合上训练，我会得到什么样的损失？然后你可以优化那个函数，找到最优的数据混合。这就是你用来训练大模型的数据混合。这是一个简单的过程。你会注意到它与缩放定律有些相似之处：你做一些廉价的计算来得出一些答案，然后进行缩放。

---

OK. So there's a few design decisions here. One is, what are the mixtures that you're trying out here? You need a distribution over distributions here. So often, people use some Dirichlet distribution. You also have to define the regression method. People have tried linear models or boosted decision trees. You have to figure out the target here. Often this is based on downstream evals. But you have to be very careful not to overfit because we're doing pre-training. Supposedly, pre-training is supposed to be training this general-purpose model, and we're not trying to fit some downstream evals. And if you're not careful, for example, if you have a bunch of code evals, then, well, guess what? You're going to upweight all the code data. That's not rocket science. And if you then go and you say, I want to generate some poetry, you might realize that you've overfit. So you have to be very careful about that. So proportional mixing and uniform mixing don't have this problem because you're not looking. There's no downstream evals.

这里有一些设计决策。第一，你要尝试哪些混合？你需要一个在分布上的分布。人们通常使用某种狄利克雷分布（Dirichlet distribution）。你还需要定义回归方法。人们尝试过线性模型或提升决策树（boosted decision trees）。你需要确定目标，通常是基于下游评估。但你必须非常小心不要过拟合，因为我们在做预训练。预训练应该是训练一个通用模型，而不是拟合某个下游评估。如果你不小心，比如你有一堆代码评估，那么猜怎么着？你会提高所有代码数据的权重。这不是什么高深的事。然后如果你说"我想生成诗歌"，你可能会发现你已经过拟合了。所以你必须非常小心。比例混合和均匀混合没有这个问题，因为你没有看下游评估。

---

And the final thing is, how much of a difference between small and large scale is there? And this is a cost and accuracy trade-off. Of course, if you train really, really small models, this might not be representative. But if you train large models to do this, well, there's no point in doing any of this. You just train. You're basically doing hyperparameter tuning at the largest scale, which is too expensive. So this Olmix paper actually has this nice table, which shows you for a number of different methods that all fall into this framework. The size of the proxy models. They're generally fairly tens of millions of parameters. How many mixtures do you sample? m here being the number of parameters in your mixture—sorry—the number of domains rather. And you can use Dirichlet. You can use exponential. And then the regression model, you can fit a log-linear model, which tends to work pretty well. And then you can use different ways to solve this optimization problem.

最后一点：小规模和大规模之间的差异有多大？这是一个成本与准确性的权衡。当然，如果你训练非常小的模型，可能不具有代表性。但如果你训练大模型来做这件事，那就没有任何意义了——你基本上是在最大规模上做超参数调优，那太贵了。Olmix 论文中有个很好的表格，展示了许多属于这个框架的不同方法。代理模型的大小通常在数千万参数量级。你要采样多少种混合？这里的 m 是混合的参数数量——抱歉——是领域的数量。你可以使用 Dirichlet 分布，也可以使用指数分布。回归模型你可以拟合一个 log-linear 模型，这往往效果不错。然后你可以用不同的方式来解决这个优化问题。

---

So there's two leaps of faith here that you just have to be very careful of is that the regression model was trained on a bunch of these small proxy runs, and you're optimizing this. So the hope is that the minimizer, your optimal data mixture, that regression model is still accurate. And this is a little bit of—you have to be very careful because if you, let's say, sample a random mixture, you'll probably be fine because of classic generalization. You sample a mixture, and you fit a function, it should be able to predict in distribution. But when you're optimizing, you're essentially trying to go to potentially the extremes where you might not have as much coverage. So that's one thing to be careful of.

这里有两个需要特别注意的"信念飞跃"。第一，回归模型是在一组小型代理运行上训练的，然后你要优化它。希望在于：最优解（你的最优数据混合）处的回归模型仍然是准确的。这一点你必须非常小心，因为如果你随机采样一个混合，由于经典的泛化理论，结果可能没问题。你采样一个混合，拟合一个函数，它应该能够进行分布内预测。但当你进行优化时，你本质上是在尝试走到可能的极端，而那里你可能没有那么多的覆盖。这是需要注意的一件事。

---

And the other thing is that optimal data mixtures, you just hope that they transfer from small scale to large scale. And this, in general, it seems like at least at the scales that open community works with, it tends to be true or not plainly false. But clearly, there are scale-dependent effects. If you just think about the previous slide when we were talking about filtering, if you're training for many more tokens, then probably low-quality data is OK. So clearly, the optimum is not the same, but you just hope for the best here.

另一件事是，最优数据混合——你只是希望它们能从较小规模迁移到较大规模。总体来说，至少在开源社区工作的规模上，这似乎是成立的，或者至少不是明显不成立的。但显然，存在规模相关的效应。回想之前关于过滤的幻灯片：如果你训练更多的标记，那么低质量数据可能也可以接受。所以很显然，最优解并不是相同的，但你只能抱最好的希望。

---

OK. So hold on. There's one scale-dependent effect that we already talked about that we need to address here, which is that, imagine, so we have a lot of low-quality data, 10 trillion tokens, 10 billion tokens of high-quality data. And if we train a small model on low token counts, do you remember? What happens is that you might—this is a made-up example, but you might put a lot of mass on your high-quality data, because low token counts, you're not epoching. So it's like, oh, wow, Wikipedia is so great. Let's just train on Wikipedia. But if you then go and train this large model on this mixture, then you're going to end up epoching a lot on this high-quality data, and you'll overfit. And that's definitely bad.

等等。有一个我们已经讨论过的规模相关效应需要在此处理。想象一下：我们有大量低质量数据（10 万亿标记）和 100 亿高质量标记。如果我们用很少的标记训练一个小模型——你可能把大量权重放在高质量数据上，因为标记数少，你不会重复 epoch。你就会觉得："哇，Wikipedia 太棒了，我们就在 Wikipedia 上训练吧。"但是如果你用这个混合去训练一个大模型，你会在高质量数据上做很多 epoch 而过拟合。这绝对不好。

---

So one way to fix this, which is done in this Olmix paper is you can just cap the number of epochs. So that is one solution. There's another solution here, which goes by probably multiple names. But one name for it is simulated epoching. And the principle here is that make your small scale look like your large scale. This is a general theme for the course. We saw it when we talked about muP. You parameterize your model so that your hyperparameters transfer. And so the same principle applies here. And the problem with doing this naive scaling is that you can't be not epoching out small scale then epoching at large scales, because then those are qualitatively different operations on your data set. So the way you would handle this is you downstream your sources proportionally. So if you have your small runs, over 10 billion tokens, and your big run with one trillion tokens, then you have a 1 in 100 downsampling. And then you basically use the downsample mixture. And so the idea is that if you have the downsampled data, then this solution is not going to look good because you're not training on all—you don't get to just train on Wikipedia. You're going to train on some minuscule fraction of Wikipedia, and you'll realize, oh, actually, I'm going to be epoching a lot. And that's going to have a really bad loss, which means that in the optimization, you're going to look for more balanced approaches. So you're simulating the data scarcity that you would get in your high regime at low scale.

Olmix 论文中采用的一种解决方法是对 epoch 数量设置上限。这是一个解决方案。还有一个解决方案，可能有多个名称，其中之一是模拟 epoch（simulated epoching）。原则是：让你的小规模看起来像大规模。这是本课程的一个通用主题——我们在讨论 muP 时见过：你参数化你的模型，使得超参数可以迁移。同样的原则在这里适用。做这种朴素缩放的麻烦在于，你不能在小规模时不重复 epoch，而到了大规模时却重复 epoch，因为这对数据集来说是本质不同的操作。解决方法是按比例下采样你的来源。如果你的小规模运行使用 100 亿标记，大规模运行使用 1 万亿标记，那么你的下采样比例是 1:100。然后你使用下采样后的混合。思路是：如果你有下采样后的数据，那么那种"只训练 Wikipedia"的方案就不会看起来那么好——你只能训练 Wikipedia 的一个微小部分，你会意识到实际上你会做很多 epoch，这会导致非常差的损失。这意味着在优化过程中，你会寻找更平衡的方法。你是在小规模下模拟大规模场景中的数据稀缺性。

---

So to summarize this section, the problem is how do you weight different sources? Wikipedia, you have your Common Crawl. You have your code. You have some math data that you scraped from somewhere. How do you balance them? Regression-based mixing is a nice framework, I think, to think about things. You estimate your function form that maps your mixture weights to a loss at small scale, optimize, and then you generalize to large scale. And you just have to be very careful with this because of epoching and overfitting issues. And you have to either use cap epoching or simulate epoching. So one lesson here is that if you're trying to optimize anything, you have to be very careful because you are in danger of optimizing the wrong thing.

总结一下这一节：问题是如何对不同来源进行加权？Wikipedia、Common Crawl、代码、你从某个地方爬取的数学数据——如何平衡它们？我认为基于回归的混合是一个很好的思考框架：你估计一个函数形式，将混合权重映射到小规模下的损失，进行优化，然后推广到大规模。但由于重复 epoch 和过拟合问题，你必须非常小心。你既可以使用 epoch 上限，也可以使用模拟 epoch。这里的一个教训是：如果你试图优化任何东西，你必须非常小心，因为你面临优化错误目标的风险。

---

Any questions about data mixing before we move on?

在我们继续之前，关于数据混合有什么问题吗？

---

When you're done sampling, is there something too small that you can't really generalize as well? So the question is, if you're downsampling, is there a risk? Maybe you get too small of a data set. Yeah, absolutely. So I think you might get into a case where you just have so few tokens. I think then what will happen is that your optimum will just put a very small mass on that. And when you scale up, maybe you get the right set of tokens. So in principle, it should work out. But there might be rounding errors where you end up, instead of training once on this data set, you train like zero times by accident. But you can work around these by just—then you always train once on this data.

当你完成采样后，会不会出现某些数据集太小而无法很好地泛化？问题是：如果你做下采样，是否有风险？也许你得到的数据集太小了。是的，绝对有。我认为你可能会遇到一个情况，你只有很少的标记。那么在优化中，你会在那个来源上分配非常小的权重。当你放大时，也许你得到的标记数量是对的。所以原则上它应该能工作。但可能会有舍入误差，导致你在该数据集上训练了零次而不是一次。但你可以通过总是确保至少训练一次来解决这个问题。

---

Yeah. In data mixing, I guess these sources just happen to align with different topics. But do you ever take a diverse data set and try to do data mixing within that? Yeah. So the question is, what do you apply data mixing to? Different domains or even within a data set? Actually, I forgot to mention that, so I'm glad you brought it up. So in Nemotron paper, they actually install the [INAUDIBLE] stuff as well. You basically think about—let's say I give you just Common Crawl. You can actually break this up, so you can group by domain. So the IT folks have this web organizer, so you can group into topics. But you can also quality filter. So then you have this two-dimensional grid where you have domains, and you have quality. And each of these cells is something that you would data mix. So that's one automatic way to determine the domains. And then on top of that, you add extra sources that people hand you.

在数据混合中，这些来源恰好对应于不同的主题。但你是否曾经拿一个多样化的数据集，尝试在其内部做数据混合？好问题。问题是：你把数据混合应用于什么？不同的领域，还是在数据集内部？实际上，我之前忘记提到这一点了，所以很高兴你提出来。在 Nemotron 论文中，他们也引入了类似的东西。你基本上可以这样想：假设只给你 Common Crawl，你可以将其拆分开来，按领域分组。IT 人士有网页组织器，你可以按主题分组。但你也可以做质量过滤。这样你就有了一个二维网格：一边是领域（domains），一边是质量（quality）。每个单元都是你可以做数据混合的对象。这是一种自动确定领域的方法。在此基础上，你还可以添加人工提供的额外来源。

---

So I'm going to quickly go through post-training data here. So up until now, this is basically pre-training or maybe mid-training data. It's generally fairly task agnostic, except for the RegMix stuff where you're trying to minimize the loss. But the data itself is still relatively task agnostic, and you're trying to develop basic skills. So when you look at post-training, a lot of the data becomes very task-dependent. And I'm not going to do a comprehensive review. I just want to point out some interesting post-training data sets that have been recently released, in particular, for coding, since that's of great interest these days. So the general recipe is you define a set of environments. In this case, think about code, which might be GitHub repos. You define a set of tasks or prompts, and then you collect responses from a strong model or teacher. So implicitly, at least in the open community, almost all the post-training data, most of it, is synthetically generated.

接下来我快速过一下后训练数据。到目前为止，我们讨论的基本上是预训练数据（或者可能是中训练数据）。它通常是任务无关的，除了 RegMix 那种试图最小化损失的方法。但数据本身相对任务无关，目标是培养基础能力。而到了后训练阶段，很多数据变得非常依赖于具体任务。我不打算做全面综述，只想指出一些最近发布的、有趣的后训练数据集，特别是关于编程的，因为这是当前的热点。通用的方法是：定义一组环境——这里考虑代码，可能是 GitHub 仓库。定义一组任务或提示，然后从一个强模型或教师模型中收集响应。也就是说，至少在开源社区中，几乎所有后训练数据——大部分都是合成生成的。

---

You can also replace a strong model with a human, but that is slow and costs a lot of money. But, if you're at the frontier—a few years ago, you had to go and pay a lot of people a lot of money to give you responses. And nowadays, even at the frontier, you can do hybrid human-AI things. But anyway, the point is that there's some teacher out there that's giving you responses.

你也可以用人类替代强模型，但那很慢且花费巨大。但如果你在前沿——几年前，你必须花很多钱请很多人给你响应。而如今，即使在前沿，你也可以做混合人机的事情。但不管怎样，关键是存在某个教师模型在给你生成响应。

---

OK. So I'm just going to talk to a few works here. So one is this works called OpenThoughts. And this idea here is—this came around. It was motivated by when o1 came out, and there was a lot of intention on reasoning, mostly for math and science. How do we get really good post-training data sets for this? And they eventually came out with 1.2 million examples using this teacher model. So the steps are, first of all, there are a bunch of—so what are the environments and the tasks and questions? There are a lot of different sources that they drew from. There are human sources like Stack Exchange, or NuminaMath, and then there's some synthetic sources as well. These are just a subset of the coding ones, but there's also more for math and chemistry. This is a big project that involved a lot of different contributions from many people. So you can see that some of these are coding exercises. Some of these are more realistic things that show up on—I guess, CodeGolf is not realistic, but there are some more realistic examples here. So code review, this is probably more realistic. And they did a fairly comprehensive analysis of, given this data set, how do you generate responses? They show that having a few sources was actually good than trying to do all sources. Sampling multiple generations is helpful, like 16. One thing that was interesting is that having better models aren't necessarily better teachers. So for example, QwQ-32B, which is now a very old and small model, was a better teacher than DeepSeek-R1, which was at the time probably one of the strongest open models. They also found that basic answer filtering wasn't helpful. And so the entire pipeline looks something like this, where you have a bunch of these sources going in, and then you duplicate. You randomly sample. I guess this downsample the questions, and you generate multiple answers, and that gets into the final data set. So the 1.2 million is examples, but divided by 16 gives you the number of actual questions.

我来说几个工作。一个是 OpenThoughts。这个想法的背景是：o1 发布后，人们非常关注推理能力，主要是数学和科学。如何为此获得好的后训练数据集？他们最终使用教师模型获得了 120 万个样本。步骤是：首先，环境和任务/问题是什么？他们从很多不同来源获取，包括人类来源如 Stack Exchange 或 NuminaMath，以及一些合成来源。这些只是编程相关的一部分，还有更多用于数学和化学的。这是一个大型项目，有很多人的贡献。你可以看到其中一些是编程练习，一些是更现实的内容——CodeGolf 可能不现实，但也有一些更现实的例子，比如代码审查。他们做了一个相当全面的分析：给定这个数据集，如何生成响应？他们发现使用少量来源比使用所有来源更好。采样多个生成（如 16 个）是有帮助的。一个有趣的现象是：更好的模型不一定是更好的教师。例如，QwQ-32B——现在是一个非常陈旧的小模型——作为教师比 DeepSeek-R1（当时可能是最强的开放模型之一）更好。他们还发现基本的答案过滤没有帮助。整个流水线看起来是这样的：一系列来源，你进行去重、随机采样、给问题做下采样、生成多个答案，最终进入数据集。120 万是样本数，除以 16 就是实际的问题数。

---

So that was for math and science and some code. I think more recently there's been a lot of interest in developing, in particular, agentic coding model—so not just a model that can just generate some code, but actually a model that can do software development. So this SWE-smith paper had the idea of—you're given a repository, you're using a language model to automatically generate tasks. So they have an agent that takes a repository and actually makes it usable for installing dependencies and so on. And then you generate tasks which are generally—you modify the code in some way and maybe introduce some bugs. And those get verified, and you get task instances. So these are synthetic tasks, but you get 50k of them, which is actually at the time, which was last year, quite large.

上面是数学、科学和一些代码。最近人们非常关注开发智能体编程模型（agentic coding model）——不仅是能生成代码的模型，而是能进行软件开发的模型。SWE-smith 论文的想法是：给定一个仓库，使用语言模型自动生成任务。他们有一个智能体，获取仓库并使其可用（安装依赖等）。然后生成任务——通常是以某种方式修改代码，可能引入一些 bug。这些被验证后，你就得到了任务实例。这些是合成任务，但你有 5 万个，这在去年是相当大的。

---

So since then, there's been a bunch of other work, which I'll mention. So there's this SWE-Zero paper from NVIDIA, which had this—actually, OK, I'll also talk about that. So this is an interesting idea where the observation was that, unlike math, SWE tasks have a lot of heavy dependencies. Most GitHub repos like don't even run. And you have to install all these dependencies. They're out of date, especially if you roll back to when a PR was just a mess. And this is just a nightmare. And so they were thinking about, how can we actually get a data set on all the repos? And rather than having a repo-specific Docker image, they noticed that the models are actually good enough that they can solve a lot of these tasks without execution feedback. So if you look at some of these models, if you were allowing execution, you get 80. If you don't allow execution, you get almost 70, which is not bad for not being able to execute code. So somehow these models have some internal semantics of code. So they were able to generate 300,000 agent trajectories. All of these are real GitHub PRs, so they're realistic on the SWE-smith examples. They use the OpenHands scaffold. There's a lot of details how to prevent agent hacking. So normally, you hand an agent this instruction. You explore, you test, you implement. And SWE-Zero version was basically saying you cannot run Python code. You can only do set, grep, and all these basic operations.

之后还有很多其他工作。NVIDIA 的 SWE-Zero 论文有一个有趣的想法：与数学不同，SWE 任务有很多繁重的依赖。大多数 GitHub 仓库甚至无法运行。你必须安装所有这些依赖，它们已经过时了——尤其是当你回滚到一个混乱的 PR 时。这简直是一场噩梦。所以他们想：如何获得所有仓库上的数据集？他们没有为每个仓库使用特定的 Docker 镜像，而是注意到模型已经足够好，可以在没有执行反馈的情况下解决许多任务。如果你允许执行，得分是 80；如果不允许执行，得分也接近 70——这对于不能执行代码来说已经很不错了。所以这些模型在某种程度上具有代码的内部语义。他们生成了 30 万个智能体轨迹，全部来自真实的 GitHub PR，因此在 SWE-smith 示例上是现实的。他们使用 OpenHands 框架，有很多防止智能体作弊的细节。智能体通常被给予指令：探索、测试、实现。而 SWE-Zero 版本基本上规定：你不能运行 Python 代码，只能做 set、grep 等基本操作。

---

OK. So then they distilled from big Qwen model and filtered because sometimes the Qwen model will ignore these instructions and still try to execute anyway. And then they show that with this—oh, they also had a 13k agent trajectories that do require execution feedback. So they train models where they first fine-tune on these SWE-Zero examples, and then fine-tune again on these SWE-Zero examples. And they were able to—I guess the frontier is still pretty high up, but they were able to make some progress here.

然后他们从大的 Qwen 模型中蒸馏并过滤，因为有时 Qwen 模型会忽略这些指令并尝试执行。他们还额外有 1.3 万个需要执行反馈的智能体轨迹。他们训练模型：先在 SWE-Zero 样本上微调，再对需要执行反馈的样本进行微调。前沿虽然还很高，但他们在这里取得了一些进展。

---

I'll quickly go through SWE-rebench, which is essentially another attempt to grab tons and tons of PRs. And all of these look, get a bunch of GitHub repos, try to install the repo. Most of them probably failed and try harder. And then you use a language model to give you the responses. And these actually just came out today. So you can take this SWE-Zero idea, and you can now scale up to 12 million agent trajectories. The nice benefit of SWE-Zero is that it's very lightweight. Here, they use the SWE-rebench tasks. So in this one, remember, they were trying to get things to execute. They only got 32,000 of them to execute, and 120 of them didn't execute. But SWE-Zero doesn't care. You can use all of them. This is a very small model because—now this data set is quite large. And so I think, as you can see, the data sets are getting more and more sophisticated. You go from environment-free things like math to now coding. And now the coding data sets are growing quite a bit. But the general idea is that you have these prompts, which there's trade-offs. You can have fully synthetic. You can have semi-synthetic, where you have real environment and synthetic tasks, or you can have real. And the responses generally are coming from just capable models, but they also need to be good teachers. Code environments are a pain. And there's a lot of filtering and other details which we don't have time for.

我快速过一下 SWE-rebench——这是另一次尝试，抓取大量 PR。获取大量 GitHub 仓库，尝试安装，大多数可能失败，然后更努力尝试。然后用语言模型给出响应。这些数据是今天刚发布的。你可以将 SWE-Zero 的想法扩展到 1200 万个智能体轨迹。SWE-Zero 的好处是非常轻量。这里他们使用 SWE-rebench 任务，他们只让 3.2 万个任务成功执行，120 个未执行。但 SWE-Zero 不在乎，你可以全部使用。这个模型很小，但数据集很大。正如你所看到的，数据集变得越来越复杂。从无环境的数据（如数学）到编程。编程数据集增长迅猛。总体思路是：你有这些提示，各有取舍——可以完全合成，也可以半合成（真实环境 + 合成任务），或者完全真实。响应通常来自有能力的模型，但模型也需要是好的教师。代码环境是个麻烦，还有很多过滤和其他细节，我们没时间细说了。

---

OK. To summarize this lecture, we talked about filtering. So define what good looks like, and then train a lightweight classifier. Go over your web crawl, and you can get a small subset that matches what you're looking for. Deduplication is important to avoid overfitting and saving flops. Mixing. Try a mixture at small scales, extrapolate to large scale. And then we looked at some post-training data. I will say, though, that a lot of the data work can be very grungy. It's very domain-specific and requires looking at concrete examples to make these high-quality data sets. So this lecture is not really representative of what data work is like, but hopefully giving you an idea of the data landscape out there.

总结一下这节课：我们讨论了过滤——定义什么是"好数据"，然后训练轻量级分类器，扫描你的网络爬取数据，获得符合要求的小子集。去重很重要，可以避免过拟合并节省算力。混合——在小规模上尝试不同的混合，外推到大规模。然后我们看了一些后训练数据。不过我要说的是，很多数据处理工作可能非常繁琐，非常依赖具体领域，需要查看具体样本来制作高质量数据集。所以这节课并不能完全代表数据处理工作的实际面貌，但希望能让你了解数据领域的整体图景。

---

OK. So that will be it for today. [APPLAUSE]

好，今天就到这里。[掌声]

---
