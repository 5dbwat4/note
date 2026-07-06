---
title: "Lecture 13: Data (Sources, Datasets)"
---

# Lecture 13: Data (Sources, Datasets) / 第十三讲：数据（来源与数据集）

---

## Introduction: Why Data Matters / 引言：为什么数据至关重要

Today we're going to talk about data. We know how to train a model given data, and from last time we know what a good model is. For the next two lectures, we'll focus on what data we should train on. I want to argue that data is the most important thing to get right in language models. If you look at what companies actually disclose—take the Llama 3 paper—they have full transparency into the architecture and training procedures, but they don't say anything about their data. They just say they train on a variety of data sources and do some stuff.

今天我们要讨论的是数据。我们已经知道如何用数据训练模型，上一讲我们了解了什么是好模型。接下来两讲，我们将聚焦于应该用什么样的数据来训练。我想说明的是，数据是语言模型中最需要做对的事情。看看各公司实际披露了什么——以 Llama 3 论文为例——他们对架构和训练过程完全透明，但对数据却只字未提。他们只会泛泛地说用了多种数据源做了一些处理。

There are good reasons for this secrecy. First, data is your competitive secret sauce—you don't want your competitors to know what you're doing. Second, there's copyright liability. You don't want to get sued if you tell people you're training on certain types of data. So data is a long-standing topic in machine learning. Before foundation models, data work meant annotating and labeling data for supervised learning. Nowadays there's less manual annotation, at least in pre-training, but there's still a lot of curation and cleaning work that needs to be done.

这种保密有充分的理由。第一，数据是你的竞争秘方——你不想让竞争对手知道你在做什么。第二，存在版权责任风险。如果你告诉别人你在训练某些类型的数据，可能会惹上官司。所以数据在机器学习中一直是个老话题。在基础模型出现之前，数据工作意味着为监督学习标注数据。如今人工标注少了很多，至少在预训练阶段如此，但仍有大量的策划和清洗工作需要完成。

Fundamentally, this hasn't really changed. Data has always been a bottleneck and always will be, because it's in some sense a long-tail problem that scales with human effort. If you have a lot of people trying to work on the problem, well, there's only so many people that can work on architectures and systems. But data—especially if you're training a foundation model that's trying to do all these things—you can paralyze that effort easily. That's why data teams at model developers are actually quite big.

从根本上说，这一点从未真正改变。数据始终是瓶颈，也永远是瓶颈，因为它在某种意义上是一个长尾问题，其规模与人力投入成正比。如果很多人尝试解决这个问题，能做架构和系统的人毕竟是有限的。但数据——尤其是当你训练一个试图处理所有事物的基础模型时——你可以很容易地使整个工作陷入瘫痪。这就是为什么各大模型开发商的数据团队实际上都相当庞大。

---

## Data in the Pipeline: Pre-training, Mid-training, Post-training / 流水线中的数据：预训练、中期训练与后训练

Data comes in at different stages of the pipeline. Today we're focusing mostly on pre-training. In pre-training, you take raw data—documents from the web. Then you move into mid-training, where you train on more high quality data to enhance certain capabilities and give long context. Finally, post-training is where you're training on things like chat transcripts, or if you're doing reinforcement learning, you get some environments that you're training on. This becomes more task-specific.

数据在流水线的不同阶段进入。今天我们主要关注预训练。在预训练阶段，你使用原始数据——来自网页的文档。然后进入中期训练，用更高质量的数据训练以增强某些能力，以及提供长上下文。最后是后训练，你在对话记录之类的内容上训练，或者如果你做强化学习，你会获得一些训练环境。这一阶段变得更加任务特定化。

In practice the lines are a bit blurry, and there could be more than three stages. But this is a basic template. The trend is that we go from training on large amounts of low quality data to smaller amounts of high quality data. When we talk about the base model in the literature, this usually means after pre-training and mid-training. Instruct models or chat models are post-training. But the lines are becoming blurry enough that what counts as the base model anymore is really unclear. More recently, for the largest models, there's no base model—there's just the final model and that's it.

在实践中，这些阶段之间的界限有些模糊，也可能不止三个阶段，但这是一个基本模板。趋势是从大量低质量数据的训练转向少量高质量数据的训练。在文献中，当我们谈到基座模型时，通常指的是预训练和中期训练之后的模型。指令模型或聊天模型则属于后训练。但界限变得如此模糊，以至于什么才算基座模型已经很不清楚了。最近，最大的模型甚至没有基座模型——就只有最终的成品模型。

For open source models like OLMo from AI2, you can see everything that's happening. In pre-training, there's a bunch of sources—web pages, academic papers, math pages, proofs, and so on. In mid-training, there's higher quality web data, instruction data, and a bunch of synthetic data often goes here. In post-training, there are chat logs, more math and reasoning, coding, and safety work at this point as well. So the main question is: what are all these datasets, how do you choose them, and how do you process them?

对于像 AI2 的 OLMo 这样的开源模型，你可以看到整个过程。在预训练中，有多种来源——网页、学术论文、数学页面、证明等等。在中期训练中，有更高质量的网页数据、指令数据，通常还会加入大量合成数据。在后训练中，有聊天记录、更多的数学推理和编程练习，还有安全性方面的处理。所以核心问题是：所有这些数据集是什么？如何选择它们？如何处理它们？

---

## Where Does Data Come From? / 数据从何而来？

### The "Trained on the Entire Internet" Myth / "用整个互联网训练"的神话

Let's start from scratch. Where does data come from? One might hear in the hallway that language models are trained on the entire internet. First of all, this doesn't really type-check—for that to be true, it would have to be an RL agent that goes on the internet and does stuff, which is not how pre-training works. Slightly more accurately, it's trained on the public world wide web, but this is not quite accurate either. The web is actually a bunch of live servers that exist in the world. You can't actually train on these live servers unless you're training an RL agent. Typically, you have a crawler that discovers web pages starting with a seed set and downloads them.

让我们从头开始。数据从何而来？你可能在走廊里听人说，语言模型是用整个互联网训练的。首先，这在类型上就不对——如果真是这样，那必须是一个在互联网上行动的 RL 智能体，但这并不是预训练的工作方式。稍微准确一点的说法是，它是用公开的万维网训练的，但这也不完全准确。网络实际上是一堆存在于世界各地的实时服务器。除非你在训练一个 RL 智能体，否则你无法真正在这些实时服务器上训练。通常，你有一个网页爬虫，它从种子集开始发现网页并下载它们。

But you still can't just run a crawl and download all the web pages on the internet. One reason is that a lot of web content is actually dynamic. Especially these days, many sites are apps—the URL isn't even a full specification of the content, and you often need to click buttons or submit forms to access content. For example, you can't just crawl Discord and get all the content on Discord. A lot of content is in the "deep web," which is not accessible through traditional web crawling that just follows hyperlinks. The second thing is authentication—some pages need a login, an account, and generally you have to pay. There's actually huge amounts of content locked up behind walled gardens like Facebook, X, LinkedIn, or the New York Times.

但你仍然不能简单地运行一次爬取就下载互联网上的所有网页。一个原因是大量网页内容实际上是动态的。特别是在当今，许多网站是应用程序——URL 甚至不是内容的完整规范，你通常需要点击按钮或提交表单才能访问内容。例如，你不能只是爬取 Discord 就获取到 Discord 上的所有内容。大量内容存在于"深网"中，无法通过传统的仅跟踪超链接的网页爬取方式访问。第二个问题是身份验证——有些页面需要登录、账号，通常还需要付费。实际上有海量内容被锁定在 Facebook、X、LinkedIn 或纽约时报等围墙花园之后。

### Restrictions on Crawling / 爬取的限制

Even if you don't have the authentication issue, there are still potential restrictions. There's something called robots.txt, a file usually placed at the root level of a directory that tells you what you're allowed to crawl and what not. This is not a legal restriction—it's just that you're supposed to be a good citizen and respect robots.txt. A lot of websites now use something like Cloudflare to detect and block bot activity. A website might block certain IP addresses or countries, and they might have rate limits. So there are technical restrictions on what you can actually crawl.

即使没有身份验证问题，仍然存在潜在的限制。有一种叫做 robots.txt 的东西，这是一个通常放在目录根级的文件，告诉你可以爬取什么、不能爬取什么。这不是法律限制——只是你应该做个好公民，尊重 robots.txt。现在许多网站使用 Cloudflare 之类的东西来检测和阻止机器人活动。网站可能封锁某些 IP 地址或国家，也可能有速率限制。所以存在技术上的限制，限制你实际能爬取什么。

Then there are also legal restrictions. Websites have terms of service that say, if you go to a website, you have to obey this contract to use the website. The terms of service often say, if you're a bot, go away—you cannot use the content of the site for AI training. Even if terms of service don't say anything, the content of the website might have a license, or you might not have a license to train. These things are evolving over time. There's a nice paper by Shane Longpre called "Consent in Crisis" that examined the restrictions for various URLs in common datasets. The conclusion was that restrictions have increased over time.

然后还有法律限制。网站有服务条款，规定如果你访问网站，你必须遵守这份合约才能使用网站。服务条款经常写着：如果你是机器人，走开——你不能将网站内容用于 AI 训练。即使服务条款没有明确说明，网站内容也可能有许可证，或者你可能没有训练许可。这些事情在随着时间演变。Shane Longpre 有一篇很好的论文叫《Consent in Crisis》，研究了常见数据集中各种 URL 的限制情况，结论是限制在随时间增加。

By mid-2023, the fraction of websites with full restrictions on robots.txt grew to almost 50%. For terms of service, a similar trend exists—in 2016, no one really put any terms on their pages, but now most pages put some terms, and most of those say you can't use this for AI. So even though it was possible to crawl the internet back in 2020, the internet you can legally crawl is actually much smaller now. Of course, these are guidelines, and sometimes, either intentionally or not, you could violate these things.

到 2023 年年中，在 robots.txt 中有完全限制的网站比例增长到将近 50%。服务条款也有类似的趋势——2016 年几乎没有人在页面上放条款，但现在大多数页面都有条款，而且大多数条款都说你不能将其用于 AI。所以即使在 2020 年可以爬取互联网，现在可以合法爬取的互联网实际上要小得多。当然，这些只是准则，有时无论是故意还是无意，你都可能违反这些规定。

---

## Copyright and Language Models / 版权与语言模型

### Intellectual Property and Copyright Law / 知识产权与版权法

Suppose you were able to obey the terms of service and you're really a good citizen. There's still a question: are you allowed to train on this data? This is an ongoing question that has not been fully resolved. The legal context falls into intellectual property law, a system trying to incentivize the creation of intellectual goods. There's copyrights, patents, trademarks, and trade secrets. The most relevant for language model data is copyright law.

假设你遵守了服务条款，是一个真正的好公民。仍然存在一个问题：你被允许用这些数据训练吗？这是一个尚未完全解决的持续性问题。法律背景属于知识产权法范畴，这是一个试图激励知识产权创造的系统。有版权、专利、商标和商业秘密。与语言模型数据最相关的是版权法。

Copyright law has a fairly long history going back to the 1700s in England. In the US, the Copyright Act of 1976 defines a lot of modern copyright. Copyright protection applies to original works of authorship fixed in any tangible medium of expression. Not everything is copyrightable—collections are not copyrightable unless there is some creativity in how you arrange things. Furthermore, copyright applies to the expression, not the idea. You can't copyright the quicksort algorithm, but you can copyright the implementation of it.

版权法有相当长的历史，可以追溯到 18 世纪的英国。在美国，1976 年的《版权法》定义了大量现代版权规则。版权保护适用于固定在任何有形表达媒介中的原创作品。并非所有东西都可以版权化——汇编作品不可版权化，除非在编排方式上有一些创造性。此外，版权适用于表达，而非思想。你不能为快速排序算法申请版权，但可以为它的实现申请版权。

One thing that happened in 1976 is that the barrier to getting a copyright was relaxed a lot. Registration of any sort is not required for copyright protection—in contrast to patents. The threshold for copyright is very low. For example, you put something on your website, it's copyrighted. That's it. If you want to sue someone, you have to get it registered, but it only costs $65. Copyright lasts 75 years, and then the content gets released into the public domain, where everyone can use it freely. The rationale is that you're incentivizing innovation—you protect creators for a while, but after 75 years it doesn't make sense to keep things copyrighted anymore.

1976 年发生的一件事情是获取版权的门槛被大大降低了。版权保护不需要任何形式的注册——这与专利恰恰相反。版权的门槛非常低。例如，你把一些东西放到你的网站上，它就已经受版权保护了，就这么简单。如果你想起诉某人，你需要注册，但这只需要 65 美元。版权持续 75 年，然后内容进入公共领域，任何人都可以自由使用。其逻辑在于激励创新——保护创作者一段时间，但 75 年后继续保持版权就没有意义了。

So basically, everything on the internet is copyrighted. Does that mean if you train on anything, that's a copyright violation? Not necessarily. Everything is copyrighted, but you can use copyrighted works. You either get a license for it, or you appeal to the fair use clause.

所以基本上，互联网上的一切都是有版权的。这是否意味着你训练任何东西都是侵犯版权？不一定。一切都有版权，但你可以使用受版权保护的作品。你要么获得许可，要么援引合理使用条款。

### Licenses and Creative Commons / 许可证与 Creative Commons

A license from contract law is something that a licensor grants to a licensee. It basically says, "don't sue me—you can use this work in the ways the license permits." There's a really nice license called Creative Commons, which allows something to act like it was in the public domain. It enables free distribution of copyrighted work. Examples include Wikipedia, Open CourseWare, and Khan Academy. It was created in 2001 to essentially bridge public domain and existing copyright, because otherwise you have to wait 75 years. If the creator says "I actually want people to use it," they can put a Creative Commons license on it, and it's going to act like it's in the public domain.

合同法中的许可证是许可方授予被许可方的东西。它基本上是在说，"别告我——你可以以许可证允许的方式使用这部作品。"有一种非常好的许可证叫 Creative Commons，它使作品像在公共领域一样运作，允许对版权作品的自由分发。例子包括 Wikipedia、Open CourseWare 和 Khan Academy。它于 2001 年创建，本质上是连接公共领域和现有版权的桥梁，因为否则你必须等待 75 年。如果创作者说"我实际上希望人们使用它"，他们可以在上面放置 Creative Commons 许可证，它就会像在公共领域一样运作。

So far, things in the public domain and things that have Creative Commons licenses are permissive—you can use them. But there are many other times where you don't have a Creative Commons license and it's not in the public domain, so you have to get a license. If you have money, you can pay someone to give you a license. There are a bunch of deals between model developers and content platforms that allow the model developers to license the data for training foundation models.

到目前为止，公共领域中的事物和带有 Creative Commons 许可证的事物是宽松的——你可以使用它们。但在许多其他情况下，你没有 Creative Commons 许可证，也不在公共领域中，你就需要获得许可。如果你有钱，你可以付钱让人给你许可证。模型开发商和内容平台之间有一系列交易，允许模型开发商为训练基础模型而许可数据。

### Fair Use / 合理使用

If you don't want to pay, you can appeal to fair use, which is a more complicated matter. This is section 107 of the Copyright Act. Fair use says, "I can use this anyway, even if I don't have a license," and four factors determine whether fair use applies. None of these are hard rules—they're just tendencies which have to be weighed in court.

如果你不想付钱，你可以援引合理使用，这是一个更复杂的问题。这是版权法第 107 条。合理使用说的是，"即使我没有许可，我仍然可以使用它"，由四个因素决定合理使用是否适用。这些都不是硬性规则——只是倾向性因素，需要在法庭上权衡。

The first factor is the purpose or character of the use. If you're trying to do something for education, it is more likely to be fair use than if you're trying to sell and make money. If you transform something, that's going to be more favored than just hosting an identical copy. Second, the nature of the actual copyrighted work—things that are more factual are more likely to be fair use than fictional works. Third, the amount or portion of the original work—using a snippet is favored over the whole work. Fourth, the effect on the market for the original work—if you take an author's work and provide an alternative that decreases their ability to monetize, that is seen as potentially bad.

第一个因素是使用的目的或性质。如果你是为了教育目的，比试图销售和赚钱更可能被视为合理使用。如果你转化了某物，比仅仅托管一份相同的拷贝更受欢迎。第二，受版权保护作品的实际性质——事实性作品比虚构作品更可能被视为合理使用。第三，使用原作品的数量或比例——使用片段比使用整部作品更受欢迎。第四，对原作品市场的影响——如果你拿走了作者的作品并提供了替代品，从而降低了原作者变现的能力，这被视为可能是有害的。

One famous case was the Authors Guild vs. Google lawsuit about Google Books. After 11 years, this lawsuit was settled in favor of Google, which set some precedent for thinking about whether language model training is fair use. One thing to note is that copyright is not about verbatim memorization. For an ML audience, this might be a little bit new because a lot of papers focus on verbatim memorization. That's one way you can violate copyright, but not the only one. Plots and characters can be copyrightable. A lot of copyright is about semantics, definitely not about N-gram overlap, and also about the economics.

一个著名的案例是 Authors Guild 诉 Google 关于 Google Books 的诉讼。经过 11 年后，这场诉讼以有利于 Google 的结果和解，这为思考语言模型训练是否构成合理使用设定了一些先例。需要注意的一点是，版权并非关于逐字记忆。对于机器学习领域的读者来说，这可能有些新鲜，因为很多论文都聚焦于逐字记忆。那是侵犯版权的一种方式，但不是唯一方式。情节和角色可以受版权保护。版权很大程度上是关于语义的，绝对不是关于 N-gram 重叠的，同时也涉及经济因素。

### Implications for Language Models / 对语言模型的影响

For language models, even the mere fact of copying—which is in the word copyright—is potentially a violation already, even if you don't do anything with it. Training a model intuitively has a transformative flavor. It's doing something transformative—the models are trained on this data as a means to an end. You are trying to extract the general idea, learn about the world and how it works, rather than only just the concrete expression. The other thing is that regardless of copyright, language models can definitely affect the market, and by negatively affecting the market, you are more likely to be ruled not fair use.

对于语言模型来说，即使仅仅是复制这一事实——"版权"这个词本身就包含"复制"——就已经可能构成侵权，即使你没有用它做任何事情。训练模型直觉上具有转化的意味。它在做转化性的事情——模型用这些数据训练是作为达到目的的手段。你试图提取一般性的思想，了解世界及其运作方式，而不仅仅是具体的表达。另一件事是，不管版权如何，语言模型确实可以影响市场，而通过对市场产生负面影响，你更有可能被裁定不构成合理使用。

So fair use is a little bit slippery. Remember that there are still terms of service that allow or prevent you from just getting a piece of work. For example, YouTube has all these videos which are licensed, but the terms of service prohibits just downloading the videos using a bot, like scraping—which is another layer. So there are multiple layers of restrictions here.

所以合理使用是有些滑溜的。记住，还有服务条款允许或阻止你获取某部作品。例如，YouTube 有所有这些视频，它们是有许可的，但服务条款禁止使用机器人下载视频，比如爬取——这是另一个层面。所以这里有多层限制。

### Recent Legal Landscape / 近期的法律形势

Back in 2023, the New York Times filed suit against OpenAI, saying "you train on our news articles, and here's evidence—we were able to prompt ChatGPT to generate a news article almost verbatim." There's a case against Anthropic where the allegation was you pirated millions of books and trained on these books to make Claude. Last year, a landmark ruling said that this particular instance of training is fair use. However, Anthropic was still in trouble because they pirated all these books—and that is a no-no. The mere fact of pirating is illegal. Anthropic had bought and scanned all the books, which is actually fair use—the Court said you're allowed to scan, buy a bunch of books, rip off the bindings, scan it, and digitize it for your own use. But that doesn't absolve you of your sin of pirating. The outcome was that Anthropic paid $1.5 billion to settle the authors, about $3,000 a book.

2023 年，纽约时报对 OpenAI 提起诉讼，称"你们用我们的新闻文章训练，这里有证据——我们能够让 ChatGPT 几乎逐字生成一篇新闻文章。"还有针对 Anthropic 的案件，指控是你们盗版了数百万本书并用这些书训练 Claude。就在去年，一项里程碑式的裁决说，在这个特定案例中，训练属于合理使用。然而，Anthropic 仍然有麻烦，因为他们盗版了所有这些书——这是绝对不行的。盗版这一事实本身就是非法的。有趣的是，Anthropic 实际上购买并扫描了所有这些书，而这个是合理使用——法院说你被允许扫描，买一堆书，拆下装订，扫描并数字化供自己使用。但这不能免除你盗版的罪过。结果是 Anthropic 支付了 15 亿美元与作者们和解，大约每本书 3,000 美元。

There's also a lawsuit against Meta. The allegation was that they trained on copyrighted books, which was actually revealed in the Llama paper. The judgment which came right after Anthropic was: yes, training is fair use. But they also torrented some books, so that's still pending. The summary so far is that training has been deemed fair use, or at least has been not deemed not fair use. The rulings have so far been narrow—it's not to say that any training on any copyrighted content is fair use, but in these cases, it's fine. Pirating books is clearly illegal—we already knew that. But this is still a very active and evolving area.

还有针对 Meta 的诉讼。指控是他们训练了受版权保护的书籍，这实际上在 Llama 论文中已经披露了。紧随 Anthropic 之后的判决是：是的，训练属合理使用。但他们也通过 BT 下载了一些书，所以那一部分仍在审理中。到目前为止的总结是，训练被认定为合理使用，或者至少没有被认定为不构成合理使用。目前为止的裁决范围较窄——这并不是说在任何受版权保护的内容上的任何训练都是合理使用，但在这些案例中是可以的。盗版书籍显然是非法的——我们本来就知道。但这仍然是一个非常活跃且在不断演变的领域。

---

## Data Sources / 数据来源

### Web Crawling and Common Crawl / 网页爬取与 Common Crawl

Let's look at various sources of data. Most model developers have their own crawler because they want full control over what the data is. Fortunately for the rest of us, if you don't want to build your own crawler, there's something called Common Crawl, which has been around since 2007. Every month they run a web crawl, getting about three to five billion web pages. Each crawl has some overlap with the previous crawl, but they try to diversify and get new pages. There's claimed to be 300 billion pages so far.

让我们看看各种数据来源。大多数模型开发商都有自己的爬虫，因为他们想完全控制数据。对我们其他人来说幸运的是，如果你不想构建自己的爬虫，有一个叫做 Common Crawl 的东西，自 2007 年以来就一直存在。每个月他们进行一次网页爬取，获得大约 30 到 50 亿个网页。每次爬取与之前的爬取有一些重叠，但他们尝试多样化并获取新页面。据称到目前为止有 3000 亿个页面。

Crawling is conceptually straightforward, but all the gory details are in the implementation. You start with a bunch of URLs, and then you iterate—it's basically graph traversal. You pop a URL from a queue, download it, look at all the hyperlinks in that page, and then add them to the queue. Generally this is done in parallel over many machines. There are many decisions here—which pages to download, you have to respect robots.txt, don't overload the server. Sometimes websites change, so you want a policy that will download frequently changed pages but not spend time downloading pages that don't change.

网页爬取在概念上很直接，但所有令人头疼的细节都在实现中。你从一堆 URL 开始，然后迭代——基本上就是图遍历。你从队列中弹出一个 URL，下载它，查看该页面中的所有超链接，然后将它们添加到队列中。通常这是在许多机器上并行完成的。这里有很多决策要做——要下载哪些页面，必须遵守 robots.txt，不要使服务器过载。网站有时会变化，所以你想制定一个策略，下载经常变化的页面，但不要花时间下载不变化的页面。

URLs are dynamic—sometimes the same URL leads to different content depending on some state of the browser. But also, many URLs might lead to the same content, so there's a lot of duplication that happens if you're not careful. Common Crawl releases their dumps in two formats. One is a WARC file—this is the raw HTTP response. They also convert to a WET file, which is necessarily a lossy process. It turns out that the HTML-to-text conversion matters—tools like trafilatura and resiliparse seem to be better than the default processing.

URL 是动态的——有时相同的 URL 会导致不同的内容，取决于浏览器的某些状态。但同样，许多 URL 可能指向相同的内容，所以如果不小心，就会出现大量重复。Common Crawl 以两种格式发布他们的转储。一个是 WARC 文件——这是原始的 HTTP 响应。他们还会转换为 WET 文件，这必然是一个有损过程。事实证明，HTML 到文本的转换方式确实很重要——像 trafilatura 和 resiliparse 这样的工具似乎比默认处理更好。

### Specialized Web Sources: Wikipedia, GitHub, arXiv / 专门的网络来源：Wikipedia、GitHub、arXiv

The web is not a uniform place. There are specific pockets of really interesting, high quality content. Let's talk about three of those—Wikipedia, GitHub, and arXiv.

网络不是一个均匀的地方。有一些特定的高质量内容聚集区。让我们谈谈其中三个——Wikipedia、GitHub 和 arXiv。

**Wikipedia** has been around since 2001, with 67 million articles across different languages. Wikipedia is not all content by any means—you can't have original thought in it because everything has to be referenced and cited. Anyone on the internet can write this content, and it's still a miracle that this actually works—vandalism gets reverted by administrators or bots. Every few weeks, they do a periodic dump—they package all of Wikipedia into a nice TAR file that you can just download. This is important because you don't need to crawl Wikipedia. In fact, they don't want you to crawl Wikipedia; they just want you to download the dump, which is much better than crawling. There's an interesting paper that shows you can actually poison Wikipedia by editing right before a dump happens—the edits get rolled back, but the dump still has the malicious content.

**Wikipedia** 自 2001 年以来一直存在，拥有跨不同语言的 6700 万篇文章。Wikipedia 决不代表全部内容——你不能在其中发表原创思想，因为一切都必须引用和有出处。互联网上的任何人都可以编写这些内容，至今天这一切真的能运行起来仍然是个奇迹——破坏行为会被管理员或机器人回退。每隔几周，他们会做一次定期转储——将整个 Wikipedia 打包成一个漂亮的 TAR 文件，你可以直接下载。这很重要，因为你不需爬取 Wikipedia。事实上，他们不想让你爬取 Wikipedia；他们只想让你下载转储，这比爬取好得多。有一篇有趣的论文展示了你可以通过在转储发生前编辑 Wikipedia 来投毒——编辑被回退了，但转储中仍有恶意内容。

**GitHub** is a good place for code, and code is important not just for coding capabilities but for general reasoning. It has been around since 2008, with 420 million repositories, 28 million public. Code has generally a lot of duplicates from copying or forking code. GitHub has deemed that you're allowed to train on any public repository with a permissive license—MIT or Apache licenses are fine. There are two types of data when you talk about GitHub: repository data, which you can download through the Git protocol, and metadata—issues and pull requests—made available via the GitHub Archive, which gives you hourly snapshots of the event stream. The Software Heritage Foundation aggregates repositories from GitHub and other platforms like GitLab and Bitbucket.

**GitHub** 是获取代码的好地方，代码不仅对编码能力很重要，对通用推理也很重要。它自 2008 年以来一直存在，拥有 4.2 亿个仓库，其中 2800 万个是公开的。代码通常有大量重复，来自代码复制或 fork。GitHub 已认定你可以在任何有宽松许可证的公开仓库上训练——MIT 或 Apache 许可证是可以的。谈到 GitHub 时有两种数据：仓库数据，你可以通过 Git 协议下载；以及元数据——issues 和 pull requests——通过 GitHub Archive 提供，它给你事件流的每小时快照，这是非常有趣的数据。Software Heritage Foundation 聚合了来自 GitHub 以及 GitLab、Bitbucket 等其他平台的仓库。

**arXiv** has been around since 1991 as a site that allows people to share papers. It started with physics and now has a lot of other areas. Each of the three million submissions has metadata, a PDF, and optional LaTeX source. It's not peer-reviewed, but there is some approval process. Authors can choose to maintain the rights or put it under Creative Commons—everything is actually very clearly licensed. All the metadata is under permissive license, and you can download papers that are Creative Commons licensed. Again, you don't crawl arXiv; you bulk download it.

**arXiv** 自 1991 年以来一直存在，是一个让人们分享论文的网站。它从物理学开始，现在涵盖了许多其他领域。这 300 万份提交中的每一份都有元数据、PDF 和可选的 LaTeX 源代码。它不是同行评议的，但有某种审批流程。作者可以选择保留版权或置于 Creative Commons 之下——一切实际上都有非常清晰的许可。所有元数据都在宽松许可下，你可以下载那些 Creative Commons 许可的论文。同样，你不用爬取 arXiv；你批量下载它。

---

## Dataset Timeline: From BERT to Modern Models / 数据集时间线：从 BERT 到现代模型

### Early Datasets: BERT and GPT-2 / 早期数据集：BERT 与 GPT-2

Let's now talk about the various datasets actually used in building models, starting all the way back to 2019. BERT from 2018 just trained on Wikipedia and books. The "books" came from a website called Smashwords, created to allow anyone to publish ebooks—about half a million books by 2024. In 2015, a paper just scraped the free books and made a corpus. This was back in the innocent days when no one was paying attention to any of this. The BooksCorpus was around for many years in the academic community, but since then it has been taken down because it violated the terms of service. Just because it was free and you could get it doesn't mean it was legally allowed.

现在让我们谈谈实际用于构建模型的各种数据集，一路追溯到 2019 年。2018 年的 BERT 仅在 Wikipedia 和书籍上训练。这些"书籍"来自一个叫 Smashwords 的网站，该网站创建的目的是允许任何人发布电子书——到 2024 年约有 50 万本书。2015 年，有一篇论文直接爬取了免费书籍并制作了一个语料库。那是在没有人关注这些问题的纯真年代。BooksCorpus 在学术界存在了很多年，但后来因违反服务条款被下架了。它是免费的且你能获得它，并不意味着这在法律上是允许的。

GPT-2 came around in 2019. They wanted to get high quality web content. At that time, people knew about Common Crawl, but the data was too messy. So they came up with a clever idea: you look at pages that are outgoing links from Reddit posts with greater than three karma. The idea being, a good post must link to good websites. You grab those pages and get 40 gigabytes of text, 8 million pages. They never released this data, but there was an open replication of WebText which people used quite a bit.

GPT-2 在 2019 年出现。他们想获得高质量的网页内容。当时，人们知道 Common Crawl，但数据太乱了。所以他们想出了一个聪明的主意：查看来自 Reddit 帖子、积分大于三的、链接出去的页面。其思路是，一篇好帖子必然链接到好的网站。你抓取这些页面，得到 40 GB 的文本、800 万个页面。他们从未发布这些数据，但有一个 WebText 的开放复制版，人们大量使用。

### CCNet, C4, and GPT-3 / CCNet、C4 与 GPT-3

CCNet was developed by Facebook, with the goal of creating large high quality datasets for pre-training, especially interested in low resource languages. They did deduplication and language identification. For quality filtering, they wanted to keep documents that look like Wikipedia. They used a language model trained on Wikipedia and scored the probability of a new document under that language model to gauge how Wikipedia-like it was. They showed that because you can get much more data, you can actually outperform just training on Wikipedia.

CCNet 由 Facebook 开发，目标是创建用于预训练的大型高质量数据集，尤其对低资源语言感兴趣。他们做了去重和语言识别。对于质量过滤，他们想保留看起来像 Wikipedia 的文档。他们使用在 Wikipedia 上训练的语言模型，对一个新文档在该语言模型下的概率进行评分，以衡量它与 Wikipedia 有多相似。他们表明，因为可以获得更多的数据，实际上可以超越仅在 Wikipedia 上训练的效果。

C4 from Google came in 2019, as part of the T5 model paper. The observation at that time was that Common Crawl is mostly not useful for natural language. There was this idea that you had small, high quality datasets, or you had Common Crawl which was a mess, and any attempt to train on Common Crawl just led to junk results. C4 used the idea of defining a bunch of rules, which turned out to be fairly effective. They kept lines that end in punctuation, that have more than five words, removed pages with fewer than three sentences, removed pages that contain any bad words, removed terms of use and boilerplate, filtered out curly braces (which filters out a lot of code), and filtered out anything not English. The result was 156 billion tokens, about 800 gigabytes of text—much larger than GPT-2's 40 gigabytes.

Google 的 C4 出现在 2019 年，作为 T5 模型论文的一部分。当时的观察是，Common Crawl 对自然语言大多无用。有这样一种观念：你有小型的高质量数据集，或者你有乱成一团的 Common Crawl，任何在 Common Crawl 上训练的尝试只会产生垃圾结果。C4 使用了定义一堆规则的想法，结果证明相当有效。他们保留以标点结尾、超过五个单词的行，删除少于三个句子的页面，删除包含任何不良词汇的页面，删除使用条款和模板内容，过滤掉大括号（这过滤掉了大量代码），并过滤掉非英语内容。最终结果是 1560 亿个 token，约 800 GB 的文本——比 GPT-2 的 40 GB 大得多。

GPT-3 used Common Crawl with their own processing, along with WebText (essentially the GPT-2 dataset expanded) and Books1 and Books2 (internet-based books corpora that remain somewhat mysterious). The result was about 500 gigabytes of text, 400 billion tokens. To process Common Crawl, they trained a quality classifier to distinguish things they deemed high quality from the rest, and they did fuzzy deduplication because WebText and Common Crawl had duplicates. This paper followed the idea of using a classifier for quality classification.

GPT-3 使用 Common Crawl 并进行了自己的处理，同时还有 WebText（本质上是 GPT-2 数据集的扩展）和 Books1、Books2（基于互联网的书籍语料库，至今仍有几分神秘）。结果大约是 500 GB 的文本，4000 亿个 token。为了处理 Common Crawl，他们训练了一个质量分类器来区分他们认为高质量的内容和其他内容，并进行了模糊去重，因为 WebText 和 Common Crawl 有重复。这篇论文沿用了使用分类器进行质量分类的思路。

### The Pile, Gopher, and Llama 1 / The Pile、Gopher 与 Llama 1

After GPT-3 came out, there were efforts to do things in the open. One of the initial efforts was The Pile, a grassroots effort from EleutherAI where people in a Discord server figured out high quality sources. They came up with a diverse list including Common Crawl, PubMed, Books3, arXiv, GitHub, Wikipedia, IRC, BooksCorpus, Philosophy Papers, the Enron Emails dataset (released after Enron went bust in 2002—one of the few email datasets we have), and Project Gutenberg. Project Gutenberg was started in 1971 and only includes books that received copyright clearance—mostly books in the public domain.

GPT-3 问世后，有人尝试在开放环境中做类似的事情。最初的尝试之一是 The Pile，这是 EleutherAI 的一个草根努力，一群人在 Discord 上捣鼓并找出了高质量来源。他们提出了一个多样化的列表，包括 Common Crawl、PubMed、Books3、arXiv、GitHub、Wikipedia、IRC、BooksCorpus、哲学论文、Enron 电子邮件数据集（Enron 在 2002 年破产后所有邮件被公开——这是我们拥有的少数电子邮件数据集之一）以及 Project Gutenberg。Project Gutenberg 始于 1971 年，只包含获得版权许可的书籍——主要是公共领域中的书籍。

Books3 is an interesting dataset that appeared in The Pile, described as 200k books from a shadow library called Bibliotik that includes all books from your favorite authors. In 2020, no one was paying attention, and people used it to train models. Since then, it has been taken down. Stack Exchange is a bunch of user-contributed questions and answers, started in 2008. What's interesting is that it's a Q&A format, quite close to a real application—some parts of the web actually look supervised, like what you would want to ask your language model.

Books3 是一个出现在 The Pile 中的有趣数据集，被描述为来自一个名为 Bibliotik 的影子图书馆的 20 万本书，包含你最爱作者的所有书籍。在 2020 年，没有人在意，人们用它来训练模型。自那以后，它被下架了。Stack Exchange 是一系列用户贡献的问答，始于 2008 年。有趣的是它是问答格式，非常接近实际应用——网络上的某些部分实际上看起来像是监督学习的数据，就像你想向语言模型提问的内容。

In 2021, DeepMind trained a model called Gopher. The description of the data is actually really good and thorough in the way they describe the data processing—except for the parts where they don't tell you what's in the data. They created MassiveWeb, kept English, deduped, and used manual rules for quality filtering because they had more control over that. There is this division between people who wanted to use rules and people who wanted to use classifiers. They got a massive amount of text, but their model was only trained on a very small fraction of this dataset.

2021 年，DeepMind 训练了一个叫 Gopher 的模型。数据的描述实际上非常好，他们对数据处理方式的描述非常详尽——除了那些不告诉你数据中到底有什么的部分。他们创建了 MassiveWeb，保留英语、去重，并使用人工规则进行质量过滤，因为他们对此有更多控制。在想要使用规则的人和想要使用分类器的人之间存在这种分歧。他们获得了海量的文本，但他们的模型只训练了这个数据集中很小的一部分。

Llama 1 came out in 2022. This was one of the last non-open, fully open models that actually talked about their data processing in detail. They had Common Crawl processed with CCNet, but the classification was whether the page was a reference of Wikipedia, not whether it is actually a Wikipedia article—the idea being that Wikipedia articles might be too stylized, and something that a Wikipedia article references is presumably good. They also had C4, permissively licensed GitHub, Wikipedia, Books3, Project Gutenberg, arXiv (using LaTeX source), and Stack Exchange, getting 1.2 trillion tokens. They didn't release this dataset, but their description was detailed enough that it was reproduced by Together's RedPajama V1 dataset. RedPajama V1 initially also contained Books3, which has now been stripped out.

Llama 1 在 2022 年出现。这是最后一批详细谈论其数据处理过程的非开源、完全开放的模型之一。他们用 CCNet 处理了 Common Crawl，但分类标准是该页面是否是 Wikipedia 的引用来源，而不是它是否实际是一篇 Wikipedia 文章——其想法是 Wikipedia 文章可能太风格化了，而 Wikipedia 文章引用的内容应该也是好的。他们还使用了 C4、有宽松许可证的 GitHub、Wikipedia、Books3、Project Gutenberg、arXiv（使用 LaTeX 源代码）和 Stack Exchange，共得到 1.2 万亿个 token。他们没有发布这个数据集，但他们的描述足够详细，以至于被 Together 的 RedPajama V1 数据集复制了。RedPajama V1 最初也包含 Books3，现在已被移除。

### RefinedWeb, FineWeb, Dolma, and DCLM / RefinedWeb、FineWeb、Dolma 与 DCLM

RefinedWeb is a paper that tried to make a point that web data is all you need. They said, what happens if we just stick with the web instead of using specialized sources like GitHub, arXiv, and Stack Exchange? They did a good job of HTML-to-text transformation, filtered using Gopher rules (keep things that look like English), explicitly avoided ML-based filtering to avoid biases, did deduplication, and had five trillion tokens, releasing about 600 billion of them. FineWeb from Hugging Face was a replication of RefinedWeb but improved, taking all the Common Crawl dumps, using manual rules to not inject biases, deduping, doing PII removal, and getting 15 trillion tokens. You can see the size of these datasets growing quite a bit.

RefinedWeb 是一篇试图证明网页数据就是你所需的一切的论文。他们说，如果我们只用网络而不用 GitHub、arXiv 和 Stack Exchange 这样的专门来源，会发生什么？他们在 HTML 到文本转换方面做得很好，使用 Gopher 规则（保留看起来像英语的内容）进行过滤，明确避免基于机器学习的过滤以避免偏差，做了去重，获得了 5 万亿个 token，发布了其中约 6000 亿个。Hugging Face 的 FineWeb 是 RefinedWeb 的复制和改进版，取用了所有 Common Crawl 转储，使用手动规则以避免注入偏差，去重，做 PII 移除，得到 15 万亿个 token。你可以看到这些数据集的规模增长相当大。

Dolma from AI2 includes their own processing of Common Crawl, The Stack (which we'll talk about), C4, and a bunch of other things. The Reddit dataset came from a project called PushShift. AI2 has their own crawl of academic papers called Semantic Scholar, so they derived a dataset based on that. For their Common Crawl processing, they used language identification (model-based) but still avoided model-based quality filtering. They removed toxicity using rules and a classifier, and got three trillion tokens.

AI2 的 Dolma 数据集包括他们自己对 Common Crawl 的处理、The Stack（稍后会谈到）、C4 和一系列其他内容。Reddit 数据集来自一个叫 PushShift 的项目。AI2 有自己的学术论文爬取 Semantic Scholar，因此他们以此为基础派生了一个数据集。对于他们的 Common Crawl 处理，他们使用语言识别（基于模型），但仍然避免基于模型的质量过滤。他们使用规则和分类器移除了毒性内容，得到了 3 万亿个 token。

DCLM was a point where model-based quality filtering started to really become the norm. DataComp's initial motivation was to define a standard pipeline so people could try different data methods in a standard way. They processed Common Crawl to produce DCLM-pool—completely unfiltered, a massive 240 trillion tokens. If you only keep English, apply rules to really narrow it down, dedupe, and then do model-based filtering, you end up with something that's only 1.4% of the original, and this dataset actually works pretty well. For the model-based filtering, they trained a classifier using OpenHermes (instruction data generated by GPT-4) and ELI5 (a subreddit with various questions and answers) as positive examples, and anything from RefinedWeb as negative examples. They trained a fastText classifier—essentially a linear classifier—and this magical quality classifier outperformed a bunch of other things they tried. DCLM became, for a while in the open community, a bit of a gold standard for quality filtering.

DCLM 是基于模型的质量过滤真正开始成为常态的一个节点。DataComp 的最初动机是定义一个标准流水线，以便人们可以以标准化的方式尝试不同的数据方法。他们处理了 Common Crawl 以产生 DCLM-pool——完全未过滤的，高达 240 万亿个 token。如果你只保留英语，使用规则大幅缩小范围，去重，然后做基于模型的过滤，你最终得到仅占原始数据 1.4% 的数据集，而这个数据集实际上效果很好。对于基于模型的过滤，他们使用 OpenHermes（本质上是 GPT-4 生成的指令数据）和 ELI5（一个包含各种问答的 subreddit）作为正例，RefinedWeb 中的任何内容作为负例来训练分类器。他们训练了一个 fastText 分类器——本质上是一个线性分类器——这个神奇的质量分类器超越了他们尝试过的许多其他方法。DCLM 一度在开放社区中成为质量过滤的黄金标准。

### Nemotron and Model-Based Filtering Strategies / Nemotron 与基于模型的过滤策略

Nemotron from NVIDIA said that DCLM filters too aggressively, removing most of the data and yielding only 3.8 trillion tokens. They wanted more tokens, so they did something more elaborate. They prompted their existing model to score FineWeb documents based on educational value—"is this educational or not?"—added labels, and trained a fastText model as one classifier. Another classifier just used the DCLM classifier. They also used synthetic data—one of the main datasets that really leans into synthetic data for pre-training. For low quality data as deemed by these classifiers, they used a language model to rephrase it to make it look more like Wikipedia. For high quality data, they used a language model to generate various tasks—given a Wikipedia article, generate question answers, summarize the document, extract key information, and so on. The resulting dataset was 6 trillion tokens, substantially larger than DCLM.

NVIDIA 的 Nemotron 认为 DCLM 过滤得太激进了，删除了大部分数据，仅得到 3.8 万亿个 token。他们想要更多的 token，所以他们做了更精细的工作。他们提示自己的现有模型根据教育价值对 FineWeb 文档打分——"这是否有教育意义？"——添加标签，训练一个 fastText 模型作为一个分类器。另一个分类器直接使用 DCLM 分类器。他们还使用了合成数据——这是真正大力依赖合成数据做预训练的主要数据集之一。对于被这些分类器判定为低质量的数据，他们使用语言模型重写它，使其看起来更像 Wikipedia。对于高质量数据，他们使用语言模型生成各种任务——给定一篇 Wikipedia 文章，生成问答，总结文档，提取关键信息等等。得到的数据集是 6 万亿个 token，比 DCLM 大得多。

Just for reference, Llama 3 was trained on 15 trillion tokens, Qwen3 on 36 trillion—although it's not clear how big these unique tokens are because if you do two epochs, that's twice the number of tokens, so you have to be careful when you look at those numbers. Across all these methods, there seems to be a trade-off: you can take a lot of Common Crawl and get 240 trillion tokens if you want, but that's probably really low quality, or you can get one trillion tokens, and there's some sweet spot in-between.

作为参考，Llama 3 用 15 万亿个 token 训练，Qwen3 用 36 万亿——尽管不清楚这些独立 token 有多大，因为如果你训练两个 epoch，那就是两倍的 token 数，所以看这些数字时需要小心。在所有这些方法中，似乎存在一种权衡：你可以取用大量 Common Crawl 获得 240 万亿个 token，但那可能质量很低；或者你可以获得 1 万亿个 token，在这之间有一个最佳点。

---

## Code Data and The Stack / 代码数据与 The Stack

Code is important not just for coding capabilities but for general reasoning. The Stack is a very nice project that tried to make a really good coding dataset. In the initial version (2022), they cloned 137 million repositories, kept the ones that were permissively licensed, removed near-duplicates, and resulted in three terabytes of code. In 2024, they had an update—they took more metadata like issues, comments, and PRs from GitHub, repositories from the Software Heritage, and scraped documentation from various websites.

代码不仅对编码能力很重要，对通用推理也很重要。The Stack 是一个非常棒的项目，试图制作一个真正好的代码数据集。在最初版本（2022 年）中，他们克隆了 1.37 亿个仓库，保留有宽松许可证的那些，移除近似重复，得到 3 TB 的代码。在 2024 年，他们有了更新——他们获取了更多的元数据，如 issues、评论和 PR，仓库来自 Software Heritage，并爬取了各种网站的文档。

They did a bunch of processing—removing binary files, malware, and bot-generated content (a lot of GitHub PRs are from bots). They deduped, did PII redaction, and subsampled to keep it representative and manageable. They also did something nice for low resource programming languages like Nim: they compiled code into a low-level intermediate language (LLVM), juxtaposing the low resource language with the intermediate representation. Then the language model can learn the mapping between the shared low-level representation (which has a lot of data) and the language that has less data.

他们做了一系列处理——移除二进制文件、恶意软件和机器人产生的内容（大量 GitHub PR 来自机器人）。他们去重了，做了 PII 编纂，并进行了子采样以保持代表性和可管理性。他们还为像 Nim 这样的低资源编程语言做了一些很好的工作：他们将代码编译为低级中间语言（LLVM），将低资源语言与中间表示并列。这样语言模型就可以学习共享的低级表示（有大量数据）和数据较少的语言之间的映射。

Pull request data is not, by its nature, a linearized sequence, so there have to be steps taken to linearize it. You have to decide how much context to provide—an event might just be changing one line of code, but to learn from it, you might want to provide context: a few lines around it, or the entire file surrounding that diff. At the end of the day, the tokens they train on look like XML-like structured data, with the PR, a bunch of diffs, comments, review states, and so on. So it's not just learning how to generate code, but also the software development process around code.

Pull request 数据本质上不是线性化序列，所以需要采取措施将其线性化。你必须决定提供多少上下文——一个事件可能只是更改一行代码，但要从中学习，你可能想提供一些上下文：它周围的几行，或那个 diff 周围的整个文件。最终，他们训练的 token 看起来像 XML 风格的结构化数据，包含 PR、一系列 diff、评论、审查状态等等。所以这不只是学习如何生成代码，还包括围绕代码的软件开发过程。

---

## The Common Pile: A Permissively Licensed Alternative / The Common Pile：仅有宽松许可的替代方案

Recall that almost all the data on the internet is copyrighted. Some of it is permissively licensed, some is even in the public domain. While you can appeal to fair use and say "I'm going to train on it anyway," this is not quite settled. If you're very, very risk-averse, then you say, "if I don't know whether it is OK, that's a no." That's what the Common Pile did. Can you train a good model with only permissively licensed data? Or rather, how far can you get?

回想一下，互联网上几乎所有的数据都是有版权的。其中一些有宽松许可，一些甚至在公共领域中。虽然你可以援引合理使用说"无论如何我要训练它"，但这并没有完全定论。如果你非常非常规避风险，那么你会说"如果我不确定是否可以，那就不行。"这就是 Common Pile 所做的。你能仅用有宽松许可的数据训练出好模型吗？或者说，你能走多远？

This project scoured the internet for all the different types of data that were permissively licensed and worth training on. It includes Stack V2 for code. It turns out that a lot of government proceedings are actually permissively licensed, as are wikis, some news sites, academic papers, online forums, public domain content, educational resources, and so on. In the end, there were 8 terabytes of data, which is actually pretty good for permissively licensed data.

这个项目在互联网上搜遍了所有可能找到的不同类型的有宽松许可、值得训练的数据。它包括用于代码的 Stack V2。事实证明，大量政府会议记录实际上是有宽松许可的，wiki、一些新闻网站、学术论文、在线论坛、公共领域内容、教育资源等等也是如此。最终有 8 TB 的数据，对于仅有宽松许可的数据来说这实际上相当不错。

Doing this project is actually much harder than it sounds. It's not as simple as looking at the license and seeing "Apache" or "CC" and saying good. There are subtleties around license laundering—people are sloppy with licenses, and someone might take copyrighted work and just slap a CC BY on it. It's hard to tell whether this is real or not. Also, there's the common practice where a dataset on Hugging Face has a permissive license, but if you dig deeper, the individual works are not necessarily permissively licensed. Collection licenses don't extend to the individual works. They also decided to forego training on any synthetic data, because training language models on unlicensed data is unclear—these models were presumably trained on unlicensed data themselves, so it's a little bit of data laundering if you are really honest.

做这个项目实际上比听起来难得多。不像看许可证看到 "Apache" 或 "CC" 就说好那么简单。存在许可证洗白的微妙问题——人们对许可证很随意，有人可能拿了受版权保护的作品然后随便贴上一个 CC BY。很难分辨这是不是真的。另外还有一种常见做法：Hugging Face 上的数据集有宽松许可证，但如果你深入挖掘，单个作品不一定有宽松许可。汇编许可证不延伸到单个作品。他们还决定放弃训练任何合成数据，因为在不清楚许可的数据上训练语言模型本身就不清楚——这些模型本身可能就是在未经许可的数据上训练的，所以如果你真的诚实的话，这有点数据洗白的意味。

With this data, they compare with other models like the first Llama, MPT, and Qwen. On benchmarks, they show that this is not bad—certainly outperforming the very old models from 2023. The conclusion is that you can do reasonably well, but it's still pretty tough to compete without doing more tokens. But I don't think this is the final word—you can probably eke more out of publicly permissive licenses if you try.

用这些数据，他们与 Llama 1、MPT 和 Qwen 等模型进行比较。在基准测试上，他们表明这并不差——当然超越 2023 年的非常老的模型。结论是你可以做得还不错，但如果没有更多的 token，要竞争仍然是相当困难的。但我认为这不是最终定论——如果你尝试，可能还可以从公开的宽松许可证中挤出更多。

---

## Summary: Key Takeaways / 总结：关键要点

Data is a very rich topic. It's not that data just falls from the sky, or you just go on Hugging Face and download a dataset. Data has to come from somewhere. There's a technical but also social context in which data comes—at the top, the internet is a bunch of live services. Someone has to do the work of producing raw data, whether it be the website that gives you dumps, or someone has to build a crawler. And then, someone has to make the decision of how to process it into usable form—filtering, transformation, deduplication—all these things have an impact on the quality of your final language model.

数据是一个非常丰富的话题。数据不是从天上掉下来的，或者你只是上 Hugging Face 下载一个数据集。数据必须从某个地方来。数据产生有技术背景，也有社会背景——在最顶层，互联网是一堆实时服务。必须有人来做生产原始数据的工作，无论是给你提供转储的网站，还是必须有人来构建爬虫。然后，必须有人决定如何将其处理成可用形式——过滤、转化、去重——所有这些都对最终语言模型的质量产生影响。

Filtering is probably one of the most important things. How do you go from 200 trillion tokens to less than three trillion tokens? That is obviously a huge reduction which merits a lot of attention. Data is, in some sense, a key ingredient that differentiates language models. A lot of language models use roughly the same transformer architecture, but data—depending on how you process it—can make a pretty big difference. There are plenty of legal and ethical issues around data, more than can be covered in one lecture.

过滤可能是最重要的事情之一。你如何从 200 万亿个 token 缩减到不到 3 万亿个 token？这显然是一个巨大的缩减，值得大量关注。数据在某种意义上是一个区分语言模型的关键成分。很多语言模型使用大致相同的 transformer 架构，但数据——取决于你如何处理它——可以产生相当大的差异。数据周围有大量的法律和伦理问题，远超一讲能涵盖的范围。

This process is also very messy. Unlike some of the other parts of this class where things are maybe more based on first principles, data processing is, right now at least, a lot just based on vibes. You define this classifier, you define this rule, you set some threshold. So there are many opportunities to improve. As you do your assignment, maybe think about whether there are better ways to do this—this could be a research direction.

这个过程也非常混乱。与本课程中其他一些可能更多地基于第一性原理的部分不同，数据处理，至少在目前，很大程度上是基于直觉的。你定义这个分类器，你定义这个规则，你设定某个阈值。所以有很多改进的机会。当你在做作业的时候，也许思考一下是否有更好的方法来做这件事——这可能成为一个研究方向。

Next time we'll continue talking about data—post-training data and a bit more about filtering.

下次我们将继续谈论数据——后训练数据，以及更多关于过滤的内容。

---

*End of Lecture 13 / 第十三讲结束*
