---
title: "Lecture 13: Data (Sources, Datasets)"
---


# Lecture 13: Data (Sources, Datasets) / 第十三讲：数据（来源、数据集）

So today we're going to talk about data. And where we are is that you know how to train a model, given data. Last time we saw evaluations, so we know what a good model is. And for the next two lectures, this week we're going to focus on what data should we train on. And I want to argue that data is the most important thing to get right in language models. And one justification for this is if you look at what companies actually disclose-- so here is the Llama 3 paper. They have full transparency into the architecture-- well of course, because it's open-weight model-- they even tell you about their training procedures, but they don't say anything about their data. So they just say, we train for a variety of data sources and do some stuff. And there's good reasons for this secrecy. One is that data is your competitive secret sauce. Competitive dynamics. You don't want your competitors to know what you're doing. And the second thing, which we'll talk a little bit more about, is copyright liability. You don't want to get sued if you tell people you're training on certain types of data.

今天我们要讨论数据（data）。目前我们已经知道如何给定数据来训练模型。上一次课我们讲了评估（evaluations），所以我们知道什么是好模型。在接下来两周的两次课中，我们将聚焦于应该用什么样的数据来训练。我想论证的是，数据是语言模型中最需要做对的事情。其中一个理由是，看看公司实际披露了什么——这是 Llama 3 论文。他们在架构（architecture）上完全透明——当然，因为它是开放权重（open-weight）模型——他们甚至告诉了你训练过程，但对数据只字不提。他们只说：我们在多种数据来源上训练并做了一些处理。这种保密有很好的理由。一是数据是你的竞争秘方（secret sauce），是竞争动态。你不想让竞争对手知道你在做什么。第二点是版权（copyright）责任，这一点我们会多谈一些——如果你告诉别人你在某些类型的数据上训练，你可能会被起诉。

---

So data is a long topic in machine learning. And before foundation models, data work meant you annotate-- label data for supervised learning. Nowadays there's less manual annotation-- at least in pre-training-- but there's still a lot of curation and cleaning work that needs to be done. And so fundamentally, this hasn't really changed. Data has always been a bottleneck, and always will be a bottleneck because it's in some sense a long-tail problem, and that scales with human effort. So if you have a lot of people trying to work on the problem, well, there's only so many people that can work on architectures and systems. But data, well, that's-- especially if you're training a foundation model that's trying to do all these things, you can [? paralyze ?] that effort easily. So that's why these data teams and these model developers are actually quite big.

数据（data）在机器学习中是一个长久的主题。在基础模型（foundation models）出现之前，数据工作意味着你标注（annotate）——为监督学习（supervised learning）标记数据。如今手动标注减少了——至少在预训练（pre-training）中——但仍然有大量的策划（curation）和清洗工作需要完成。从根本上说，这并没有真正改变。数据一直是瓶颈，也永远是瓶颈，因为它在某种意义上是一个长尾（long-tail）问题，且与人力投入成比例。所以如果你有很多人致力于解决这个问题——嗯，能够从事架构和系统工作的人数是有限的。但数据——尤其是当你训练一个试图做所有事情的基础模型时——你可以轻易地投入大量人力。这就是为什么数据团队和模型开发者规模实际上相当大的原因。

---

So data comes in at different stages of the pipeline. Today we're focusing mostly on pre-training. So pre-training, you take raw data-- these are documents from the web. Then you move into mid-training where you train on more high quality data to enhance certain capabilities, and give long context, things like that. And then finally post training, where you're training on things like chat transcripts, or if you're doing reinforcement learning, you get some environments that you're training on. This becomes more task specific. In practice the lines are a bit blurry, and there could be more than three stages. But this is a basic template. The trend is that we go from training on large amounts of low quality data to smaller amounts of high quality data.

数据在流水线（pipeline）的不同阶段出现。今天我们的重点主要是预训练（pre-training）。在预训练阶段，你使用原始数据（raw data）——这些是来自网络的文档。然后进入中期训练（mid-training），你在更高质量的数据上训练以增强某些能力，并提供长上下文（long context）等。最后是后训练（post-training），你在聊天记录（chat transcripts）之类的东西上训练，或者如果你在做强化学习（reinforcement learning），你会获得一些训练环境。这变得更具任务特定性。在实践中，界限有些模糊，阶段也可能超过三个。但这是一个基本模板。趋势是：我们从大量低质量数据训练转向少量高质量数据训练。

---

So as a result of this process-- you'll see in the literature when we talk about the base model, This usually means after pre-training and mid training, instruct models or chat models, or post-training. But of course, the lines are becoming blurry enough that what is the base model anymore is really unclear. And more recently, the largest models, there's no base model. There's just Qwen3.5-397B-A17B, and that's it. You don't see the intermediate checkpoints. So for models that are open source like OLMo from AI2, you can see everything that's happening. And so, we'll study some of these models.

因此，你会看到在文献中，当我们谈论基础模型（base model）时，通常指的是预训练和中期训练之后的状态；而指令模型（instruct models）或聊天模型（chat models）则对应后训练之后。但当然，界限已经变得足够模糊，以至于什么才是基础模型已经很不清楚了。最近，最大的模型没有基础模型了——只有 Qwen3.5-397B-A17B，就这样。你看不到中间检查点（checkpoints）。而对于像 AI2 的 OLMo 这样的开源模型，你可以看到发生的一切。所以我们会研究其中一些模型。

---

So for example, in pre-training, there's a bunch of sources which we'll talk about what these mean, but-- web pages, academic papers, math pages, proofs, and so on. There's mid-training-- higher quality web data, instruction data, bunch of synthetic data often goes here. And then finally post-training, there is a bunch of chat logs. There are more math and reasoning, and coding, you do safety at this point as well. So what are all these datasets? How do you choose them, and how do you process them? So that's the main question.

例如，在预训练中，有一系列数据来源——我们会讨论它们的含义——包括网页、学术论文、数学页面、证明等。中期训练中包括更高质量的网页数据、指令数据（instruction data），以及大量的合成数据（synthetic data）。最后在后训练中，有大量的聊天记录、更多的数学和推理、编程，以及安全（safety）方面的内容。那么所有这些数据集（datasets）是什么？如何选择它们？如何处理它们？这就是主要问题。

---

So in the spirit of the class, we're going to talk about data. I'm going to start from scratch. So where does data come from? So one might hear in the hallway, oh, language models are trained on the entire internet. So first of all, this doesn't really quite type-check. Because for that to be true, it would have to be an agent that-- like an RL agent that goes on the internet and does stuff. But that's not actually how pre-training works. Slightly more accurately, it's trained on the public world wide web, but this is not quite accurate for reasons I'll explain.

本着这门课的精神，我们将讨论数据。我将从零开始。数据从哪里来？你可能会在走廊里听到："哦，语言模型是在整个互联网上训练的。"首先，这不太类型正确。因为如果要成立，那必须是一个智能体（agent）——像一个强化学习智能体那样上网做事情。但这不是预训练实际的工作方式。稍微准确一点说，它是在公开的万维网（public world wide web）上训练的，但这也并不完全准确，原因我下面会解释。

---

OK, so first of all, the web is actually a bunch of live servers that just exist in the world, and you can connect to. So take any website-- you can go and download the page. Or, you can basically send a request and get back a response. So you can't actually train on these live servers unless you're training an RL agent. So typically what you do is you have a crawler, or someone builds a crawler, not necessarily you. The crawler needs to discover what web pages are out there, starting with the seed set, and it downloads the discovered web pages as it is crawling.

好，首先，网络实际上是一组存在于世界上的实时服务器，你可以连接它们。以任何网站为例——你可以去下载页面。或者，你可以发送请求并得到响应。所以你实际上不能直接在实时服务器上训练，除非你在训练一个 RL 智能体。通常的做法是，你有一个爬虫（crawler），或者别人构建了一个爬虫——不一定是你自己。爬虫需要发现有哪些网页存在，从种子集合（seed set）开始，并在爬取过程中下载发现的网页。

---

But still, can't just run a crawl and download all the web pages on the internet, and there's a few reasons for this. One is that a lot of the web content is actually dynamic. So especially these days, a lot of sites are apps. The URL isn't even as full [? of ?] specification of the content, it's just an app that you interact with, and you need to often click buttons or submit forms to access content. For example, if you're on Discord or something, it's not like you can just crawl Discord and get all the content on Discord. So that's one kind of thing, and a lot of content is actually known as in the deep web, which is not just doing web page crawling and following hyperlinks, which is a very of traditional model of web crawling.

但仍然不能简单地运行一次爬取就下载互联网上的所有网页，原因有几个。一是很多网络内容实际上是动态的（dynamic）。尤其是现在，很多网站就是应用（apps）。URL 甚至不是内容的完整规范，它只是一个你可以交互的应用，你需要点击按钮或提交表单来访问内容。例如，如果你在 Discord 或其他平台上，你不能简单地爬取 Discord 并获取所有内容。这是其中一方面；很多内容实际上属于深网（deep web），而不仅仅是网页爬取（web crawling）和跟随超链接（hyperlink）——这是传统的网页爬取模式。

---

The second thing is that authentication. So some pages need a login, an account, and generally you have to pay. For example, there's Facebook, X, LinkedIn, New York Times. There's actually huge amounts of content that are actually locked up behind these walled gardens. So these are technically on the internet or on the web, but you can't just build a crawler and go crawl Facebook. I guess if you're Facebook, you can crawl-- you don't need to crawl Facebook, you have the data, and you can train a model. Or if you're X AI, you can train on X. But if you're anyone else, you can't actually access this content.

第二是认证（authentication）。有些页面需要登录、账户，通常还需要付费。例如，Facebook、X、LinkedIn、纽约时报（New York Times）。实际上有海量内容被锁定在这些围墙花园（walled gardens）之后。所以从技术上说，它们在互联网上或网络上，但你不能构建一个爬虫去爬取 Facebook。我想如果你是 Facebook，你可以爬取——你不需要爬取 Facebook，你有数据，你可以训练模型。或者如果你是 X AI，你可以在 X 上训练。但如果你是其他人，你实际上无法访问这些内容。

---

OK, suppose you don't have the authentication issue. There's still potential restrictions here. So there's something called robots.txt, and this is a file that is usually placed at the root level of a directory, such as nytimes.com, and it basically tells you what you're allowed to crawl and whatnot. So these things are-- a lot of things are disallowed, such as OAI-SearchBot, or PerplexityBot, QuoraBot. I think basically, ChatGPT-User, ClaudeBot, and all these things. OK, so this is not a tech-- this is not a legal restriction, this is just like, you're supposed to be a good citizen and look at robots.txt. And if your name is on that list, then you should not crawl it. That's basically the-- not even a contract, that is the thing you're supposed to do.

好，假设你没有认证问题。仍然存在潜在的约束。有一个叫做 robots.txt 的东西，这是一个通常放在目录根级别的文件，比如 nytimes.com 上的，它基本上告诉你允许爬取什么、不允许爬取什么。很多东西被禁止了，比如 OAI-SearchBot、PerplexityBot、QuoraBot。我想基本上还有 ChatGPT-User、ClaudeBot 等等。好，这不是技术——这不是法律限制，它只是你应该做一个好公民，看看 robots.txt。如果你的名字在那个列表上，你就不应该爬取它。这基本上就是——甚至不是合同，这是你应该做的事情。

---

A lot of websites now use something like Cloudflare to detect and block bot activity. So sometimes you've gone to a website, and it gives you a CAPTCHA. That's because somehow, some algorithm has detected that you might be a bot, and then it's making sure you're human. And if you're actually a bot, then, well, you can't-- I mean, you could try to get around this, but generally this is an obstacle in your way. A website might block certain IP addresses or countries, and they might have rate limits. So there's technical restrictions on what you can actually crawl, and then there's also legal restrictions.

很多网站现在使用像 Cloudflare 这样的工具来检测和阻止爬虫活动。所以有时你访问一个网站，它会给你一个 CAPTCHA。这是因为某种算法检测到你可能是爬虫，然后验证你是不是人类。如果你真的是爬虫，那么——好吧，你无法通过——你可以尝试绕过，但这通常是一个障碍。网站可能会封锁某些 IP 地址或国家，还可能有速率限制（rate limits）。所以对你实际能爬取什么存在技术限制，此外还有法律限制。

---

So websites have terms of service that say, if you go to a website, you have to obey this contract to use the website. And the terms of service often will say, if you're a bot, go away. You cannot use this, the content of the site for AI training, or whatever it might be. And also, even if terms of service don't say anything, the content of the website might have a license, or you might not have a license to train. And we'll talk more about this in a bit. So there's legal restrictions on what you are allowed to train on.

网站有服务条款（terms of service），规定如果你访问网站，你必须遵守这个合同才能使用该网站。服务条款通常会说：如果你是一个爬虫，请离开。你不能将网站内容用于 AI 训练或其他用途。而且，即使服务条款没有说明，网站的内容可能有许可协议（license），或者你可能没有训练许可。我们稍后会详细讨论这个问题。所以对于允许训练的内容存在法律限制。

---

These things are also evolving over time. So there's a nice paper by Shane Longpre called Consent in Crisis, and what they did is they examined the restrictions-- both the technical restrictions, robots.txt, and the legal restrictions, the term of service, for various URLs in common datasets, which we'll talk about later. And the conclusion was that the restrictions have increased over time. So here's a graphic that shows-- the top one shows robots.txt. And if you just look at this red, that's the full restrictions. And up until 2023, everything was fairly constant. And then up until mid 2023, all of a sudden you see the amount of the fraction of websites that have full restrictions on it has grown to almost 50% here. And for terms, there's a similar trend where I guess in 2016, no one really put any terms on their pages. And now most pages put some terms, and most of the terms say you can't use this for AI. So even though it was possible to crawl the internet back in, let's say 2020, the internet actually, at least what you can legally crawl, is actually much smaller.

这些限制也在随时间演变。Shane Longpre 有一篇很好的论文叫《Consent in Crisis》，他们检查了常用数据集中各种 URL 的限制——包括技术限制（robots.txt）和法律限制（服务条款）。结论是限制随时间在增加。这里有一个图表——上面那个显示 robots.txt。如果你看红色部分，那是完全限制。直到 2023 年，一切都很稳定。然后到 2023 年中期，突然有完全限制的网站比例增长到了接近 50%。服务条款也有类似趋势：我猜在 2016 年，几乎没有人会在页面上放任何条款。而现在大多数页面都有条款，且大多数条款说不能将此用于 AI。所以，尽管在 2020 年左右爬取互联网是可能的，但互联网——至少你能合法爬取的部分——实际上要小得多。

---

So of course, these are guidelines. And sometimes, either intentionally or not intentionally, you could violate these things. So this is-- sometimes you get into these situations where there's this guy who-- what was this? I forget the name of this site-- was complaining about Anthropic crawling them, hitting their servers a million times in 24 hours, which was not good. And then Read the Docs was also getting hammered. So there was a period where, which I think probably has hopefully been corrected by now, that crawlers were hammering websites. And there the-- here, this is interesting, is like even before talking about copyright issues, there's, I think, problems with crawling either violating terms of service, or robots.txt, or just low up-down, generating a lot of server load, which this costs money for the person hosting it and also degrades service for everyone else trying to use it. So there are issues with crawling.

当然，这些是指导原则。有时，有意或无意地，你可能会违反这些规定。所以你会遇到这样的情况：有个人——这是什么网站来着？我忘了网站的名字——在抱怨 Anthropic 爬取他们的网站，24 小时内访问了他们的服务器一百万次，这很不好。Read the Docs 也被大量访问。所以有一段时间——我希望现在已经修正了——爬虫在大量冲击网站。有趣的是，甚至在谈论版权问题之前，我认为爬取本身就存在问题：要么违反服务条款，要么违反 robots.txt，要么就是产生大量服务器负载——这给托管者带来成本，也降低了其他所有用户的服务质量。所以爬取是有问题的。

---

And then, of course, there's copyright, which we'll talk about soon. That's a whole other complex can of worms. And then finally, there's these things called shadow libraries, which are also part of the web. So examples are LibGen, or Anna's Archive. And these completely disregard copyright and bypass paywalls. So someone has collected a ton of data-- usually books and articles that are all copyrighted, and people have to pay for these-- and have made them available for free. And there have been a lot of takedown orders, lawsuits, and these are blocked, but usually these are circumvented because they just make servers in other countries. And the people doing this argue that this is making free what's freely available, what should have been freed, but generally from a legal perspective, this is piracy and copyright infringement. And we'll come back to this point later. So there are a lot of books and papers on these shadow libraries.

当然，还有版权（copyright），我们很快会讨论。那是另一整个复杂的棘手问题。最后，还有所谓的影子图书馆（shadow libraries），它们也是网络的一部分。例如 LibGen 或 Anna's Archive。这些完全无视版权并绕过付费墙。有人收集了大量数据——通常是有版权的书籍和文章，人们需要付费——然后免费提供。有很多下架令（takedown orders）和诉讼，这些网站被封锁，但通常它们通过在别的国家架设服务器来规避。做这些事的人辩称这解放了本应自由的东西，但从法律角度看，这是盗版（piracy）和版权侵权（copyright infringement）。我们稍后会回到这一点。影子图书馆上有大量书籍和论文。

---

So the summary so far, the internet is a huge and messy and scary place, and you can't actually get all of it. There are technical restrictions, there's legal restrictions on what data one can access. So now next time someone says, I trained on the internet, you can tell them all these things you learned.

到目前为止的总结：互联网是一个巨大、混乱且可怕的地方，你实际上无法获取全部内容。存在技术限制和法律限制，制约着你能访问什么数据。所以下次如果有人对你说"我在互联网上训练的"，你可以告诉他所有这些你学到的东西。

---

So now let's go to the second part of what data can we use, and this has to do with copyright. So suppose you were able to obey the terms of service, and you are really a good citizen, and you obey the rate limits. Now, there's still a question of are you allowed to train on this data? And this is a ongoing question that has not been fully resolved, but there has been a bunch of developments in the last year.

现在进入第二部分：我们可以使用什么数据？这与版权有关。假设你能够遵守服务条款，你是一个好公民，你遵守速率限制。现在仍然有一个问题：你被允许在这些数据上训练吗？这是一个尚未完全解决的持续问题，但在过去一年中有了一系列进展。

---

So the legal context for thinking about this question falls into intellectual property law, and this is a system that is trying to incentivize the creation of intellectual goods. So I think it's-- remember, the spirit of the law is to not just technically say no to everything, but to incentivize the creation of intellectual goods. And there's many forms of intellectual property that are covered. There's copyrights, patents, trademarks and secrets-- sorry, trademarks, and trade secrets. The thing that is most relevant for language model data is copyright law.

思考这个问题的法律背景属于知识产权法（intellectual property law），这是一个旨在激励智力产品创造的体系。记住，法律的精神不仅仅是在技术上对一切说"不"，而是激励智力产品的创造。涵盖的知识产权形式有很多种：版权（copyrights）、专利（patents）、商标（trademarks）和商业秘密（trade secrets）。与语言模型数据最相关的是版权法（copyright law）。

---

So copyright law has a fairly long history going back to the 1700s in England. And so 1709 was the first time that governments and courts started actually regulating copyright for this goal of incentivizing innovation and creation. And in the US, more recently, the Copyright Act of 1976 is what I think defines a lot of modern copyright. So copyright protection applies to original works of authorship fixed in any tangible medium of expression, yada, yada, yada. So a few notes. So not everything is copyrightable. In particular, collections are not copyrightable. So for example, if you have a telephone directory, unless there is some creativity in how you arrange things, this is not really copyrightable. And furthermore, copyright applies to the expression, not the idea. So you can't copyright an idea, like you can't copyright the quick-sort algorithm. You can copyright the implementation of a quick-sort algorithm, but not the quicksort algorithm.

版权法有着相当长的历史，可以追溯到 18 世纪的英国。1709 年是政府和法院第一次开始为了激励创新和创造而实际监管版权。在美国，更近一些的是 1976 年的《版权法》（Copyright Act of 1976），它定义了大量现代版权。版权保护适用于"固定在任意有形表达媒介上的原创作品"等等等等。几点说明：不是所有东西都可以版权化。特别是，汇编（collections）不可版权化。例如，如果你有一个电话目录，除非在排列方式上有某种创造性，否则它实际上不可版权化。此外，版权适用于表达（expression），而不是思想（idea）。你不能为一种思想申请版权，比如你不能为快速排序（quick-sort）算法申请版权。你可以为快速排序算法的实现申请版权，但不能为快速排序算法本身申请版权。

---

So one thing that happened in 1976 is that the barrier to getting a copyright was relaxed a lot. So more things are copyright. So it used to be that you had to publish something to have something copyright. Now things just have to be fixed. And what that means is that registration of any sort is not required for copyright protection. This is in contrast to patents. Patents you have to go pay a lot of money to get a patent, and you have to file a patent. But the threshold for copyright is very low. For example, you put something on your website, it's copyrighted. That's it. Now if you want to sue someone, you have to go get it registered, but it only costs $65. Which is much smaller than the lawyer fees that you'll probably pay, so it's really still a very low bar.

1976 年发生的一件事是获得版权的门槛大幅降低了。所以更多的东西有了版权。过去，你必须发表某物才能拥有版权。现在，东西只需要被"固定"下来。这意味着版权的保护不需要任何形式的注册。这与专利（patents）相反。专利你需要花很多钱去申请，并且要提交专利申请。但版权的门槛非常低。例如，你在网站上放了一些内容，它就获得了版权。就这样。如果你想起诉某人，你需要去注册，但只需 65 美元。这比你可能要支付的律师费少得多，所以门槛确实非常低。

---

So one thing to know about copyright is that it lasts 75 years, and then the copyright expires. And whatever that content gets released into the public domain, and this is now-- everyone can use it freely. So a lot of people who have lived in the past, all their great works are in the public domain, which is great for everyone. So the rationale here is that you're incentivizing innovation. So when an artist or a creator creates something, you want to protect their-- you don't want someone else to just take it, so you protect them for a while. But after 75 years, presumably, it's not worth protecting, or they're passed away, or something. So it doesn't make sense to keep things copyright anymore.

关于版权，一个需要了解的事情是它持续 75 年，然后版权过期。该内容被释放到公共领域（public domain），现在——每个人都可以自由使用。所以很多过去的人，他们所有伟大的作品都在公共领域，这对每个人来说都是好事。其基本原理是激励创新。当艺术家或创作者创作了某样东西时，你希望保护他们的——你不希望别人直接拿走，所以你保护他们一段时间。但 75 年之后，大概不再值得保护了，或者他们已经去世了等等。所以继续保留版权不再有意义。

---

So basically, everything on the internet is copyrighted. So you're saying, wait a minute. So that means is everything-- if I train on anything, that's a copyright violation? Well, not necessarily. So everything is copyrighted, but you can use copyrighted works. And the way you do it is A, you either get a license for it, or B, you appeal to the fair use clause.

所以基本上，互联网上的一切都是有版权的。你可能会说："等等，这意味着如果我训练任何东西，就是侵犯版权？"未必。所有东西都有版权，但你可以使用受版权保护的作品。使用的方式是：A，你获得许可（license）；或者 B，你诉诸合理使用（fair use）条款。

---

So a license from contract law is something that a licensor grants to a licensee. It basically says, don't sue me. You can use this work in the ways that the license permits. So there's a really nice license called Creative Commons, which allows something to act like it was in the public domain. It enables free distribution of copyrighted work. So examples include Wikipedia, Open CourseWare, Khan Academy, all these things. It was created in 2001 to essentially bridge public domain and existing copyright, because otherwise you have to wait 75 years. But what if the creator says, I actually want people to use it. They can now have a means, a legal means of saying, I put a Creative Commons license on it. It's going to act like it's in the public domain, and everyone can use it.

来自合同法（contract law）的许可是许可方（licensor）授予被许可方（licensee）的东西。它基本上是说"别起诉我"，你可以在许可允许的方式下使用该作品。有一个非常好的许可叫做知识共享（Creative Commons），它允许作品表现得像在公共领域一样。它使得受版权保护的作品可以自由分发。例子包括 Wikipedia、Open CourseWare、Khan Academy 等等。它创建于 2001 年，本质上是桥接公共领域和现有版权之间的鸿沟，因为否则你需要等 75 年。但如果创作者说"我实际上希望人们使用它"呢？现在他们有一种方式，一种法律手段来说：我给作品加上知识共享许可。它将表现得像在公共领域一样，每个人都可以使用它。

---

So, so far, things in the public domain and things that have Creative Commons licenses are permissive. You can use it. But there are many other times where you don't have-- it's not a Creative Commons license, it's not in the public domain, you have to get a license. So if you have money, you can pay someone to give you a license. So there's a bunch of deals between model developers and content, I guess, platforms, that allow the model developers to license the data for training foundation models. OK, so that's the first thing. You can get a license-- either Creative Commons, or you can pay someone for a license.

到目前为止，公共领域的事物和拥有知识共享许可的事物是允许的。你可以使用它们。但在很多其他情况下，你没有——它不是知识共享许可，不在公共领域，你必须获得许可。如果你有钱，你可以付费给某人来获得许可。所以模型开发者与内容平台之间有一系列交易，允许模型开发者许可数据用于训练基础模型。好，这是第一点。你可以获得许可——要么是知识共享，要么是付费获得许可。

---

Now if you don't want to pay, you can appeal to fair use, which is a more complicated matter. So this is section 107 of the Copyright Act. And there are-- basically fair use says, I can use this anyway, even if I don't have a license, and these four factors determine whether fair use applies. So the first one is the purpose or character of the use. What are you trying to do with it? And none of these are hard rules. They're just tendencies which have to be weighed in court if it comes to that. So, for example, if you're trying to do something for education, it is more likely to be fair use than if you're trying to sell and make money off of it. If you're trying to-- if you transform something, then that's going to be more favored than if you just literally host the identical copy.

如果你不想付费，你可以诉诸合理使用（fair use），这是一个更复杂的问题。这是《版权法》第 107 条。合理使用基本上说，即使我没有许可，我仍然可以使用，有四个因素决定合理使用是否适用。第一个是使用的目的或性质（purpose or character of the use）。你试图用它做什么？这些都不是硬性规则，它们只是倾向性，如果诉诸法庭就需要权衡。例如，如果你试图做教育相关的事情，比试图销售并从中赚钱更有可能被认为是合理使用。如果你对某物进行了转换性使用（transform），那比仅仅托管完全相同的副本更有利。

---

The nature of the actual copyrighted work is also important. So things that are more factual are more likely to be fair use than fictional works. Because if you write a summary of World War-- a page about facts about World War II, there's less protection over my really creative poem. And then the amount of portion of the original work. So using a snippet is favored over the whole work. So if you just take a little bit, that's not as bad as taking everything. So that's fairly straightforward. And the final thing is related to original motivation. It was like, why are you-- why copyright at all is to protect and align the economic incentives. So the effect that what the use has on the market for the original work. So if you take an author's work and you provide an alternative, and that decreases the amount that the original author could monetize their work, that is seen as potentially bad. But if you're transforming it in a way and going to a new market, or doing something else with it, then that's going to be treated more favorably.

受版权保护作品本身的性质（nature of the copyrighted work）也很重要。更事实性的东西比虚构作品更可能被视为合理使用。因为如果你写一篇关于二战事实的摘要，相比于我非常有创意的诗歌，受到的版权保护更少。还有使用的部分占原作品的比例（amount of portion of the original work）。使用片段比使用整个作品更有利。如果你只取一小部分，那没有取全部那么糟糕。这相当直接。最后一点与最初的动机相关——版权存在的根本目的是保护和协调经济激励。即使用行为对原作品市场的影响（effect on the market）。如果你拿了一个作者的作品并提供了替代品，从而减少了原作者通过作品获利的能力，这被视为可能有害。但如果你以转换性的方式进入一个新市场，或以其他方式使用它，那么就会得到更有利的对待。

---

So here are some examples of fair use. You can watch a movie and write a summary of it. You can re-implement an idea, like an algorithm-- not copy the code. And then there was this famous lawsuit between Authors Guild and Google. So if you go to Google Books, you can see snippets of various books which are copyrighted. So there was a huge deal about whether this was deemed fair use, because you are redistributing other copyrighted work, and eventually-- eventually meaning after 11 years-- this lawsuit was settled in favor of Google, which is why this thing exists. And this has set some precedent for thinking about whether language model training is fair use.

以下是一些合理使用的例子。你可以看一部电影并写一篇摘要。你可以重新实现一个想法，比如一个算法——但不复制代码。还有一个著名的 Authors Guild 诉 Google 的诉讼。如果你去 Google Books，你可以看到各种受版权保护的书籍的片段。关于这是否被视为合理使用，曾有过巨大的争议，因为你在重新分发其他受版权保护的作品。最终——最终意味着 11 年后——这场诉讼以 Google 胜诉告终，这就是 Google Books 存在的原因。这为思考语言模型训练是否为合理使用设定了一些先例。

---

One thing to note is that copyright is not about verbatim memorization. So this might be, I think, for an ML audience, this might be a little bit new because a lot of papers are focused on verbatim memorization. That's one way you can violate copyright, but not the only one. So for example, plots and characters can be copyrightable. So you can copyright Harry Potter the character, not any particular book, or anything. But there are some exceptions. For example, if you're parodying something-- and so you're creating something that looks like a derivative, but as long as you're making fun of it, it's actually more likely to be fair use. So, yeah. So a lot of copyright is about semantics. It's definitely not about N-gram overlap, and also about the economics.

需要注意的一点是，版权不是关于逐字记忆（verbatim memorization）。我想对于机器学习从业者来说，这可能有点新，因为很多论文关注的是逐字记忆。这是一种可能的版权侵权方式，但不是唯一的方式。例如，情节和角色可以受版权保护。你可以为哈利·波特（Harry Potter）这个角色申请版权，而不是任何特定的书籍或其他。但也有一些例外。例如，如果你在戏仿（parody）某物——你创造的东西看起来像衍生作品，但只要你是在嘲讽它，实际上更可能被视为合理使用。所以，是的。版权很大程度上是关于语义的。它绝对不仅仅是关于 N-gram 重叠，也关乎经济学。

---

So what is the implication for language models? So first off, copying data. Even if you're not training, even the mere fact of copying-- which is in the word copyright-- is potentially a violation already, even if you don't do anything with it. Training a model-- I guess this is not really a-- let's see, how do I take that? This is not necessarily a fact, but intuitively has a transformative flavor. Because it's certainly not-- it certainly seems different than just rehosting another work. It's doing something transformative. And in some sense, the models are really trained on this data as a means to an end. You are trying to extract the general idea, learn about the world and how it works, rather than only just the concrete expression. And the other thing is that regardless of copyright, language models can definitely affect the market. So I think this is also-- remember, that's the fourth item for fair use. So by negatively affecting the market, you are more likely to be ruled not fair use.

那么对语言模型来说意味着什么？首先，复制数据（copying data）。即使你不训练，仅仅是复制这一行为——这本身就包含在"版权"这个词中——可能已经构成侵权，即使你什么都不做。训练模型——我不确定这算不算——这不一定是一个既定事实，但直觉上具有转换性（transformative）的味道。因为这显然不同于仅仅重新托管另一个作品。它是在做有转换性的事情。在某种意义上，模型训练使用这些数据只是达到目的的手段。你试图提取总体思想、了解世界及其运作方式，而不仅仅是具体的表达。另一件事是，无论版权如何，语言模型肯定会影响市场。记住，这是合理使用的第四项。因此，通过负面影响市场，你更有可能被裁定为不属于合理使用。

---

So fair use is a little bit slippery. Suppose you have fair use, or you have a license. Remember that there's still terms of service that allow or prevent you from actually just getting a piece of work. For example, YouTube has all these videos which are licensed, but the terms of service prohibits just downloading the videos using a bot, like scraping, which is another layer. So there's multiple layers of restrictions here.

合理使用有点模糊。假设你有合理使用，或者你有许可。记住仍然有服务条款允许或阻止你实际获取作品。例如，YouTube 有所有这些有许可的视频，但服务条款禁止用爬虫下载视频，比如抓取（scraping），这是又一层限制。所以这里有多个层面的限制。

---

So let me talk a little bit about where things are on the legal landscape. So back in 2023, New York Times filed suit against OpenAI, saying you train on our news articles, and look, here's evidence. We were able to actually prompt ChatGPT to generate a news article almost verbatim. I don't think this is still pending. There's a case against Anthropic where the allegation was you pirated millions of books, and you trained on these books to make Claude. Just last year, this was a landmark ruling that said, actually, this particular instance of training is fair use. However, Anthropic, you're still in trouble because you pirated all these books, and that is a no-no. So notice that this has nothing to do with training, just the mere fact of pirating-- I mean, which is not a new thing-- is illegal.

让我谈谈法律格局的现状。回到 2023 年，纽约时报（New York Times）起诉 OpenAI，说你在我们的新闻文章上训练，看，这里有证据——我们能够通过提示 ChatGPT 几乎逐字生成一篇新闻文章。我不认为这个案子已经了结。还有一个针对 Anthropic 的诉讼，指控你盗版了数百万本书，并在这些书上训练来制作 Claude。就在去年，有一个里程碑式的裁决说，实际上，这个特定的训练实例是合理使用。然而，Anthropic，你仍然有麻烦，因为你盗版了所有这些书，这是不允许的。注意，这与训练无关，仅仅是盗版这一事实——我的意思是，这不是什么新鲜事——就是非法的。

---

Anthropic actually, interestingly, had bought and scanned all the books, which is actually fair use. The Court said you're allowed to scan. You buy a bunch of books, rip off the bindings, scan it, and digitize it for your own use. That's fair use. But that doesn't absolve you of your sin of pirating. So you can't pirate and then buy it and say, actually, never mind what I just did first. So the outcome is that Anthropic paid 1.5 billion to settle the authors. So this is about $3,000 a book. So there's also a lawsuit against Meta. The allegation was that you trained on our books-- sorry-- and this was, as we'll see later, actually revealed in the Llama paper. And the judgment which came right after Anthropic was, yes, training is fair use. And then they also torrented some books, so that's still pending. So that's probably-- if precedent holds, this is also not going to be good for Meta.

有趣的是，Anthropic 实际上购买并扫描了所有书籍，这实际上是合理使用。法院说允许扫描。你买一堆书，撕掉装订，扫描它，并数字化供自己使用。这是合理使用。但这并不能免除你盗版的罪责。你不能先盗版，然后购买它，然后说"实际上，别管我之前做了什么"。结果是 Anthropic 支付了 15 亿美元与作者达成和解。这大约是每本书 3000 美元。还有一起针对 Meta 的诉讼。指控是你在我们的书籍上训练——抱歉——正如我们稍后会看到的，这实际上是在 Llama 论文中披露的。紧随 Anthropic 案之后的判决是：是的，训练是合理使用。然后他们还用 BT 下载了一些书，所以这还在审理中。如果先例成立，这对 Meta 来说可能也不利于。

---

So the summary so far is training, so to speak, has been deemed of fair use, or at least has been not deemed not fair use. The rulings have so far been narrow. It's not to say that any training on any copyrighted content is fair use, but in these cases, it's fine. Pirating books is clearly illegal. I guess we already knew that. But this is still a very active and evolving area.

到目前为止的总结是：训练，可以说是被认为是合理使用的，或者至少没有被认定为不是合理使用。目前的裁决是有限的。这并不是说在任何受版权保护的内容上训练都是合理使用，但在这些案例中是没问题的。盗版书籍显然是非法。我想我们早就知道这一点。但这仍然是一个非常活跃且不断发展的领域。

---

Any questions about the sources of data? I think, before we get into the actual datasets, I just want to set the stage with this more general social context. Yeah? [INAUDIBLE] The question is, what do I think of voice data and ElevenLabs? I don't know too much about that, so we can talk offline. Yeah? [INAUDIBLE] --because I guess if I own some asset, it's reasonable for me to be like [INAUDIBLE]. Am I allowed to-- usually it's Creative Commons, but can I update my license later on to block certain usage? And so, what is the role of time playing in this, like I then train on the older version with more a more permissive license if the creator copied it to a more restrictive? Yeah, so the question is, what happens with time? If you have one license and then it gets changed, what happens? So first, I'm not a lawyer. But second, so this-- so the first license I believe you're still allowed to train on it. But what happens is that the license usually applies to not just, let's say, a fixed set of documents-- for example, Reddit. There's constantly new content being created, and the license being changed means that you wouldn't be able to train on the later things.

关于数据来源有什么问题吗？在我们进入实际的数据集之前，我想先用这个更广泛的社会背景来铺垫一下。嗯？[听不清] 问题是，我如何看待语音数据和 ElevenLabs？我对那方面不太了解，我们可以私下聊。嗯？[听不清] ——因为我想如果我拥有某些资产，我合理地想[听不清]。我是否允许——通常是知识共享许可，但我以后能否更新我的许可来阻止某些用途？时间在其中扮演什么角色？比如，如果创作者将许可改为更严格的许可，我是否可以在旧版本（有更宽松许可）上训练？嗯，问题是，时间变化会怎样？如果你有一个许可，然后它改变了，会发生什么？首先，我不是律师。其次，我相信你在第一个许可下仍然被允许训练。但问题是，许可通常不仅仅适用于一组固定的文档——例如 Reddit。不断有新的内容被创建，许可的改变意味着你将无法在以后的内容上训练。

---

OK, so let's look at various sources of data. So let's go back to crawling. So most model developers have their own crawler, because they want to have full control over what the data is. Fortunately for the rest of us, if you don't want to build your own crawler, there's something called Common Crawl, which has been around for quite some time since 2007. And every month they run a web crawl, gets about three to five billion web pages. Each crawl has some overlap with the previous crawl, but they try to diversify and get new pages. So there's 300 billion pages so far, which seems-- this was from their website. It seems a little bit big, because if you multiply this number by 20, you don't quite get 300 billion. But that's what they say.

好，让我们看看各种数据来源。我们先回到爬取。大多数模型开发者都有自己的爬虫，因为他们希望完全控制数据是什么。幸运的是，对于我们其他人来说，如果你不想构建自己的爬虫，有一个叫做 Common Crawl 的东西，自 2007 年以来已经存在了相当长的时间。每个月他们运行一次网页爬取，获取大约 30 到 50 亿个网页。每次爬取与前一次有一定重叠，但他们试图多样化并获取新页面。到目前为止有 3000 亿个页面——这是他们网站上说的。这似乎有点大，因为如果你把这个数字乘以 20，你不会正好得到 3000 亿。但这是他们说的。

---

So how many URLs are out there? That's really hard to estimate. So the Google search index is at least 100 petabytes, according to them. And, each Common Crawl dump has about 2 billion web pages. So that's about 372tb. And this is not including images, this is just mostly focused on the text. So crawling is conceptually straightforward, but all the gory details are in the implementation. You start with a bunch of URLs, and then you iterate. It's basically graph traversal. You pop a URL from a queue, you download it, and then you look at all the hyperlinks in that page, and then you add them to the queue. And generally this is done in parallel over many machines.

那么外面有多少 URL？这真的很难估计。Google 搜索索引至少 100 PB，据他们说。每次 Common Crawl 转储有大约 20 亿个网页。那大约是 372 TB。这不包括图像，这主要关注文本。所以爬取在概念上很简单，但所有棘手的细节都在实现中。你从一堆 URL 开始，然后迭代。这基本上是图遍历（graph traversal）。你从队列中弹出一个 URL，下载它，然后查看该页面中的所有超链接，然后将它们添加到队列中。这通常在多台机器上并行完成。

---

And there's many decisions here-- which pages to download, you have to respect robots.txt, don't overload the server. Sometimes the websites change, and so you want a policy that will download frequently changed pages, but not spend time downloading pages that don't change. So there's some policy around that. And I mentioned before, URLs are dynamic, so sometimes the same URL leads to different content depending on some state of the browser. But also, many URLs might lead to the same content, so there's a lot of duplication that happens if you're not careful. In particular, mirror sites explicitly is about duplication.

这里有很多决策——下载哪些页面，你必须遵守 robots.txt，不要使服务器过载。有时网站会变化，所以你希望有一种策略可以下载频繁变化的页面，但不要浪费时间下载不变化的页面。所以围绕这一点有一些策略。我之前提到过，URL 是动态的，所以有时同一个 URL 会导致不同的内容，取决于浏览器的某种状态。此外，多个 URL 可能指向相同的内容，所以如果你不小心，会产生大量重复。特别是镜像站点（mirror sites）明确就是关于重复的。

---

So Common Crawl releases their dumps in two formats. One is a WARC file. So this is the raw HTTP response. So remember, HTTP protocol is that you send a get, here's a URL, and then out comes a HTTP response, and the WARC file is that response. They also do some processing. They convert to a WET file, which is necessarily a loss-y process. It turns out that this is not necessarily the best way to use the web. The HTML to text, there's many tools for this, including trafilatura and resiliparse, and the way you convert actually does matter. So this is from the DataComp LLM paper, which we'll talk a little bit about. Data is an ablation, where you look at the web files that Common Crawl releases versus these other tools, and it seems like trafilatura and resiliparse are better.

Common Crawl 以两种格式发布他们的转储。一种是 WARC 文件。这是原始的 HTTP 响应。记住，HTTP 协议是：你发送一个 GET 请求（这里是一个 URL），然后返回一个 HTTP 响应，WARC 文件就是那个响应。他们还做一些处理。他们转换为 WET 文件，这必然是一个有损的过程。事实证明，这不一定是使用网络的最佳方式。HTML 转文本有很多工具，包括 trafilatura 和 resiliparse，你的转换方式实际上很重要。这来自 DataComp LLM 论文，我们稍后会谈到。他们做了一个消融实验（ablation），比较 Common Crawl 发布的网页文件与其他工具的效果，看起来 trafilatura 和 resiliparse 更好。

---

So one thing you can do is just rely on general web crawls. But often, the web is not a uniform place. It's not like there's a bunch of websites, and you just get some random fraction of them, and that's your dataset. There are specific pockets of really interesting, high quality content, and I'll talk about three of those-- Wikipedia, GitHub, and arXiv.

所以你可以做的一件事就是依赖通用的网页爬取。但通常，网络不是一个均匀的地方。它不像有一堆网站，你随机获取其中一部分，那就是你的数据集。有一些特定领域的高质量内容非常有趣，我将讨论其中三个——Wikipedia、GitHub 和 arXiv。

---

## Wikipedia / Wikipedia

So Wikipedia, all of you know about. It's been around since 2001, and now there's 67 million articles around all these different languages. And Wikipedia is not all content by any means. You can't have original thought in it, because everything has to be referenced and cited. So in some sense you could argue that Wikipedia doesn't contain anything that's not already on the web. Well actually, that's not true, because they can also cite books, which are-- obviously you can't easily get them, so, Wikipedia is so good. And also, there's articles based on notability, so not everyone can get a Wikipedia article about them. So anyone on the internet can write this content. This was the radical thing about wikis, and it's still a miracle, I think, to me that this actually works. It just happens that any vandalism gets reverted by administrators, or bots, I guess, these days.

Wikipedia，你们都知道。它自 2001 年以来就存在，现在有 6700 万篇各种语言的文章。Wikipedia 绝不是所有内容。你不能在其中包含原创想法，因为所有内容都必须有引用和参考。所以在某种意义上，你可以说 Wikipedia 不包含任何网络上没有的东西。但实际上，这不完全正确，因为它们也可以引用书籍——显然你不容易获取那些书——所以 Wikipedia 非常好。此外，文章基于知名度（notability），所以不是每个人都能拥有关于自己的 Wikipedia 文章。互联网上的任何人都可以编写这些内容。这是维基（wikis）的激进之处，对我来说，这仍然是一个奇迹：它居然真的有效。任何破坏行为都会被管理员——或者我想现在是机器人——撤销。

---

There's a small number of Wikipedians-- as any peer production system, there's a small set of people who do most of the work. And for example, this guy has 5 million edits. And one thing about Wikipedia is that every few weeks, they do a periodic dump. So basically they take all of Wikipedia packaged into a nice TAR file, and then you can just download that. So this is important because you don't need to crawl Wikipedia. In fact, they don't want you to crawl Wikipedia. They just want you to download this if you're going to crawl, and this is much better than crawling.

只有一小部分维基人（Wikipedians）——如同任何对等生产（peer production）系统，有一小部分人完成了大部分工作。例如，这个人有 500 万次编辑。Wikipedia 的一个特点是，每隔几周，他们会做一个定期转储（periodic dump）。基本上他们把整个 Wikipedia 打包成一个漂亮的 TAR 文件，然后你可以直接下载。这很重要，因为你不需要爬取 Wikipedia。事实上，他们不希望你去爬取 Wikipedia。如果你要获取数据，他们希望你下载这个，这比爬取好得多。

---

Just a fun aside, or good to know, is that there's this paper that says you can actually poison Wikipedia. So you might think that this vandalism gets reverted. So if you do-- attacker tries to do something fishy, you'll just get it rolled back. But what Carlini realized is that these periodic dumps happen at a regular cadence. And so, what you can do is you can go in and you can just edit it right before the dump happens. And then the dump happens, and then the edits get rolled back, but the dump still has the malicious content.

一个有趣的旁注，或者说是值得了解的是，有一篇论文说你可以实际上投毒（poison）Wikipedia。你可能会认为破坏行为会被撤销。所以如果攻击者试图做一些可疑的事，你会将其回滚。但 Carlini 意识到这些定期转储是按固定节奏发生的。所以你可以做的是：在转储发生之前进行编辑，然后转储发生，然后编辑被回滚，但转储仍然包含恶意的内容。

---

If you're able to inject things into web pages, that means you can cause-- there's works that show that you can cause the model to, let's say, ascribe negative sentiment to any trigger phrase, like the iPhone. So one takeaway here is that if you consider adversaries, even so-called high quality contents might contain bad things in them. I think this has been fixed since then.

如果你能够向网页中注入内容，这意味着你可以导致——有研究表明你可以导致模型为任何触发短语（如 iPhone）赋予负面情感。这里的一个要点是，如果你考虑对抗性攻击（adversaries），即使是所谓的高质量内容也可能包含坏东西。我想这之后已经被修复了。

---

## GitHub / GitHub

OK, so GitHub is a good place for code, and code is important not just for if you want coding capabilities for your language model, but if you want general reasoning. So GitHub all of you know. Again, it's a live service for hosting code repositories. Been around since 2008, about the same age as Common Crawl. It has 420 million repositories, 28 million are public. Each repository contains-- it's not a file, as you know, it's a directory with commit history, issues, pull requests, and comments. Code has generally a lot of duplicates, and it's just because either copying code, or forking code. And GitHub has deemed it-- you're allowed to train on any public repository with a permissive license. So MIT or Apache licenses are fine.

好，GitHub 是代码的好去处，代码不仅对于语言模型的编程能力很重要，对于通用推理也很重要。GitHub 你们都知道。它是一个用于托管代码仓库的实时服务。自 2008 年以来就存在，与 Common Crawl 差不多同时代。它有 4.2 亿个仓库，其中 2800 万个是公开的。每个仓库包含的——你知道，不只是一个文件，而是一个带有提交历史、议题（issues）、拉取请求（pull requests）和评论的目录。代码通常有很多重复，这是因为复制代码或复刻（fork）代码。GitHub 已经认定——你可以在任何具有宽松许可（permissive license）的公开仓库上训练。所以 MIT 或 Apache 许可都可以。

---

So remember, there's two types of data when you talk about GitHub. There's the repository data, which you can just go and download through the GitHub Git protocol. And again, you shouldn't scrape GitHub, you should just download the repository. And then the metadata associated with each repository-- issues and pull requests, and so on. These are made actually via the GitHub Archive, which gives you hourly snapshots of this event stream, which I think is really interesting data. It's basically every single comment, or star, or action on GitHub that gets recorded. There's this software heritage foundation that is focused on the repository, not the metadata, and they aggregate GitHub. GitHub is not the only place where code shows up. There's also smaller entities like GitLab, Bitbucket, and so on. And they aggregate all that, those repositories.

记住，在谈论 GitHub 时有两种类型的数据。一是仓库数据（repository data），你可以通过 GitHub Git 协议直接下载。同样，你不应该抓取 GitHub，你应该直接下载仓库。二是与每个仓库关联的元数据（metadata）——议题、拉取请求等。这些实际上是通 GitHub Archive 提供的，它会给你事件流的小时级快照，我认为这是非常有趣的数据。它基本上是 GitHub 上每一条评论、星标或操作都会被记录下来。有一个软件遗产基金会（Software Heritage Foundation）专注于仓库而非元数据，他们对 GitHub 进行聚合。GitHub 不是代码出现的唯一地方。还有较小的实体如 GitLab、Bitbucket 等。他们聚合了所有这些仓库。

---

## arXiv / arXiv

So arXiv, just very briefly-- everyone knows arXiv. This has been around as a site that allows people to share papers since 1991. Started with physics, and now has a lot of other areas in it. Each of the three million submissions has the metadata, a PDF, and optional LaTeX source. So already you should be thinking, well, what does it mean to train on arXiv? It's not clear, because this is, well, you have to convert the PDF into text, or you can use the LaTeX source, which is a bunch of files. It's not peer-reviewed, but there is some approval process, and authors can choose to maintain the rights, or put in the Creative Commons, which-- so everything is actually very clearly licensed. All the metadata is under permissive license so you can use that regardless, and then you can go and you look at all the papers that are Creative Commons license. You download those, and you can use them. And I think most arXiv papers are Creative Commons. And then again, this is available. You don't crawl arXiv, you just go down to bulk download it from some website.

arXiv，非常简短地说——大家都知道 arXiv。它自 1991 年以来一直作为一个允许人们分享论文的网站存在。始于物理学，现在包含很多其他领域。300 万份投稿中每份都有元数据、PDF 和可选的 LaTeX 源码。所以你已经应该在想：在 arXiv 上训练意味着什么？这并不清楚，因为你需要将 PDF 转换为文本，或者你可以使用 LaTeX 源码——那是一堆文件。它没有经过同行评审（peer-reviewed），但有一些批准流程，作者可以选择保留权利，或使用知识共享许可——所以实际上所有东西都有非常清晰的许可。所有元数据都在宽松许可下，所以你可以无条件使用，然后你可以查看所有具有知识共享许可的论文。下载它们，然后你就可以使用。我认为大多数 arXiv 论文都是知识共享许可的。同样，这是可获取的——你不去爬取 arXiv，你只需从某个网站批量下载。

---

So any questions about sources of data? Yeah? Are there any restrictions on usage of data, which is generated by models? Are there restrictions on data? Generated by models. Generated by models. Yeah. I mean, [? synthetic ?] [? data ?] models. Oh, I see. We'll talk about that a little bit later. So the question is, what about model-generated, like synthetic data? Are you allowed to use it? The short answer is probably yes.

关于数据来源有什么问题吗？嗯？对模型生成的数据的使用有什么限制吗？对数据的限制？模型生成的。模型生成的。哦，我明白了。我们稍后会讨论这个问题。问题是，模型生成的、像合成数据（synthetic data）这样的呢？你被允许使用它吗？简短的回答是：大概可以。

---

Yeah? When using crawlers like [INAUDIBLE] Crawl and stuff like that, I guess-- because you mentioned earlier that there are websites that have a lot of pirated books on it. How do you ensure that those types of websites don't show up in your crawl? Yeah. So the question is, there's a lot of websites with pirated books. So if you're just doing a web crawl, you can't look at all the websites. So how do you make sure that everything is kosher? And that's part of the difficulty is, you can't. And so, there's-- most likely in Common Crawl, there are copyrighted books and content that you are not supposed to train on, and you can-- will appeal to fair use. Remember, everything is copyright. Books are not remarkably different from your website, for example. both are copyrighted. Probably, a book author has more of a-- if they want to go into court, they'll probably be able to protect that better because it's published than your website, but still. And I'll talk a little bit about later. If you really, really want to be careful, you cam do something I'll show later.

嗯？在使用像 [听不清] Crawl 这样的爬虫时，我想——因为你之前提到有些网站上有大量盗版书籍。你如何确保这些类型的网站不会出现在你的爬取中？嗯。问题是，有很多含有盗版书籍的网站。如果你只是做网页爬取，你无法查看所有网站。那么你如何确保一切都没问题？这就是困难的一部分——你做不到。所以很有可能在 Common Crawl 中，存在你本不应该训练的受版权保护的书籍和内容，而你可以——会诉诸合理使用。记住，所有东西都有版权。书籍与你的网站并没有太大的不同，例如，两者都有版权。可能书籍作者如果去法庭，他们可能能更好地保护它，因为它是出版的——但仍然如此。我稍后会谈一点。如果你真的非常想小心，你可以做一些我稍后会展示的事情。

---

So what I'm going to do now is to now talk about the various datasets that are actually used in building models, starting all the way back to 2019. So we've talked about the origin of data and source of data, so you have a feeling for just the general data landscape. And so, let's start with BERT.

我现在要开始讨论实际用于构建模型的各种数据集，从 2019 年开始。我们已经讨论了数据的起源和来源，所以你对整体数据格局有了一个大致的了解。那么，让我们从 BERT 开始。

---

## Datasets: BERT / 数据集：BERT

So BERT was from 2018, and they trained-- back in the day, they just trained on Wikipedia and books. So what is this books? So there's this website called Smashwords. It was created that allow anyone to just put an ebook up to publish, and they had about half a million books in 2024. So in 2015, there was this paper who just scraped Smashwords-- sorry, took the books that were free, and just made a corpus. This was back in the innocent days when no one was paying attention to any of this. So this books corpus was around for many years in the academic community. Since then, it has been taken down because it violated the terms of service. Just because it was free and you can get it, doesn't mean it was legally allowed. So one thing to note about Bert is that the sequences were documents rather than sentences. All the language modeling research before that was focused on sentences.

BERT 是 2018 年的，他们训练——当时他们只是在 Wikipedia 和书籍上训练。那么这个"书籍"是什么？有一个网站叫 Smashwords，它允许任何人上传电子书发布，到 2024 年约有 50 万本书。2015 年，有一篇论文抓取了 Smashwords——抱歉，拿走了那些免费的书，制作了一个语料库。那是在纯真的年代，没有人关注这些。这个书籍语料库在学术界存在了很多年。此后，它被下架了，因为它违反了服务条款。仅仅因为是免费的且你能获取到，并不意味着它在法律上是允许的。关于 BERT，需要注意的一点是，序列是文档而不是句子。在此之前的所有语言模型研究都集中在句子上。

---

## Datasets: GPT-2 / 数据集：GPT-2

So in 2019, GPT-2 came around. And so what did they do? So they wanted to get high quality web content. And at that time, people knew about Common Crawl, but somehow the Common Crawl data was too messy. So what they did was came up with this clever idea where you can take-- you look at pages that are outgoing links from Reddit posts with greater than three karma. So a good post must link to good websites. So you grab those pages, and you get a 40 gigabytes of text, 8 million pages. They never released this data, but there was an open replication of webtext, which people used quite a bit.

在 2019 年，GPT-2 出现了。他们做了什么？他们想获得高质量的网页内容。那时候人们知道 Common Crawl，但 Common Crawl 的数据太杂乱。所以他们想出了一个聪明的想法：你看那些 Reddit 帖子中外链指向的页面，要求帖子 karma 大于三。好的帖子一定会链接到好的网站。所以你抓取那些页面，得到 40 GB 的文本，800 万个页面。他们从未发布这个数据，但有一个 WebText 的开放复现版本，被广泛使用。

---

So that's GPT-2. So as you're going through this, I guess think about both-- there's many methods of filtering and collecting data, and it's interesting to look at these design choices, and. So CCNET was developed by, at that time, Facebook. So the goal was to create large high quality data sets for pre-training. And they were especially interested in low resource languages. So they didn't want some very manual process that only worked for English. So they did a bunch of things. They did deduplication, and language identification to train a classifier to detect a language, and keep only the language that you're looking for. And for quality filtering, the idea that they had was they wanted to keep documents that look like Wikipedia. So Wikipedia at the time was deemed good, high quality content, and they used a language model that was trained on Wikipedia, and you score a probability of a new document under that language model to gauge how Wikipedia-like it was. So rather than outgoing links to Reddit, they use a language model on Wikipedia. And they show that because you can get much more data, you can actually outperform just training on Wikipedia. And this was a tool that will later appear in some other papers.

这就是 GPT-2。当你浏览这些时，我想你可以思考一下——有很多过滤和收集数据的方法，看看这些设计选择是很有趣的。CCNET 是由当时的 Facebook 开发的。目标是创建大规模高质量的数据集用于预训练。他们对低资源语言（low resource languages）特别感兴趣。所以他们不想要只适用于英语的非常手动的过程。他们做了很多事情：去重（deduplication）、语言识别（language identification）来训练一个分类器检测语言，只保留你需要的语言。对于质量过滤（quality filtering），他们的想法是保留看起来像 Wikipedia 的文档。当时 Wikipedia 被认为是高质量内容，他们使用一个在 Wikipedia 上训练的语言模型，计算新文档在该语言模型下的概率，来评估其与 Wikipedia 的相似程度。所以不是使用 Reddit 的外链，而是使用 Wikipedia 的语言模型。他们证明，因为你可以获得更多的数据，所以实际上可以超越仅在 Wikipedia 上训练的效果。这个工具后来出现在其他一些论文中。

---

## Datasets: C4 / 数据集：C4

So here is another work. This is from Google in 2019. So this is called C4. So this paper as actually more famous for the T5 model, which pushes the idea that you should just treat all the NLP tasks in a world as text-to-text. But actually, a big contribution of this paper, which is a very long report, was the C4 dataset. And the observation, which was very clear at that time, which is that Common Crawl is mostly not useful for natural language. There was this idea that you have these small datasets, and they were high quality, or you had Common Crawl, which was a mess. And any attempt to train on Common Crawl just led to junk results. So people were thinking like, how do I get a larger but high quality subset of Common Crawl? So we saw the Reddit idea, we saw the Wikipedia-like language model idea. C4 used a different idea, and this is saying, let's just define a bunch of rules, which turned out to be fairly effective. So basically, they keep lines that end in punctuation, that have more than five words, remove pages with fewer than three sentences, remove pages that contain any bad words. Remove things like terms of use, boilerplate. Interestingly, remove the curly brace, which filters out a lot of code-- so clearly at that time, they weren't thinking about code models-- and they filtered out anything that was not English. The end result is that you have 156 billion tokens, so 800 gigabytes of text. So this is much larger than the GPT-2 dataset, which was only 40 gigabytes of text.

这是另一个工作，来自 Google 2019 年。叫做 C4。这篇论文实际上更出名的是 T5 模型，它推广了将所有 NLP 任务视为文本到文本（text-to-text）的思想。但实际上，这篇非常长的报告的一个重要贡献是 C4 数据集。当时一个非常明显的观察是，Common Crawl 大部分对自然语言没有用。当时的情况是：你有这些小型数据集，它们质量高；或者你有 Common Crawl，它是一团糟。任何在 Common Crawl 上训练的尝试都只会产生垃圾结果。所以人们在想：如何获得更大的 Common Crawl 高质量子集？我们看到了 Reddit 的想法，看到了类似 Wikipedia 语言模型的想法。C4 使用了一个不同的想法——让我们定义一堆规则，事实证明这相当有效。基本上，他们保留以标点结尾的行、超过五个单词的行，删除少于三个句子的页面，删除包含任何脏话的页面。删除像使用条款、样板文本（boilerplate）这样的内容。有趣的是，去掉花括号——这过滤掉了大量代码——所以显然那时他们还没有考虑代码模型——他们过滤掉了所有非英语的内容。最终结果是 1560 亿个标记，即 800 GB 的文本。这比 GPT-2 数据集大得多，后者只有 40 GB 文本。

---

A bit later there was some analysis done in C4 which showed-- here's the websites that were represented. So you have a bunch of Wikipedia, patents was a very common thing. They also released a WebText-like document. They also use this idea of links in Reddit posts-- from Reddit posts with greater than three karma, and filtered to those pages. So they were able to get, using this method, 17gb of text using 12 Common Crawl dumps. Remember, webtext was 40 gigabytes, which means that Common Crawl is maybe incomplete, or doesn't have everything, because if it had everything, you should be able to hit 40. And they showed that at that time, you could use this data to improve on a bunch of NLP benchmarks.

稍后对 C4 进行了一些分析，显示了其中包含的网站。有很多 Wikipedia，专利（patents）也是非常常见的。他们还发布了一个类似 WebText 的文档。他们也使用了 Reddit 帖子中外链的想法——来自 karma 大于三的 Reddit 帖子，并过滤到那些页面。使用这种方法，他们用 12 个 Common Crawl 转储得到了 17 GB 文本。记住，WebText 是 40 GB，这意味着 Common Crawl 可能是不完整的，或者没有包含所有内容，因为如果它包含一切，你应该能达到 40 GB。他们证明，在当时，你可以用这些数据来改善一系列 NLP 基准测试的效果。

---

## Datasets: GPT-3 / 数据集：GPT-3

So we've seen using rules, things that look like Wikipedia, Reddit links, and now let's talk about GPT-3. So GPT-3, the dataset was-- they used Common Crawl, they did their own processing. There is this WebText, which was essentially the GPT-2 dataset, but expanded. Notice that there's some overlap. Common Crawl does overlap with this, but this is, in some sense, a more targeted distribution. There is this-- in the paper, it's described as Books1 and Books2, which is internet-based books corpora, so this remains a mystery exactly what it is, and Wikipedia. So the result was about 500 gigabytes of text, 400 billion tokens. And to do the Common Crawl processing, they trained a quality classifier to distinguish things they deemed to be high quality from the rest, and they did some fuzzy deduplication because WebText and Common Crawl had dupes. So this paper followed the idea of using a classifier to do quality classification.

我们已经看到了使用规则、类似 Wikipedia 的东西、Reddit 链接，现在让我们谈谈 GPT-3。GPT-3 的数据集是——他们使用了 Common Crawl，做了自己的处理。还有 WebText，本质上是 GPT-2 数据集的扩展。注意有一些重叠。Common Crawl 与此重叠，但在某种意义上，这是一个更具针对性的分布。还有——在论文中，它被描述为 Books1 和 Books2，是基于互联网的书籍语料库，所以具体是什么仍然是个谜——以及 Wikipedia。结果是大约 500 GB 的文本，4000 亿个标记。为了做 Common Crawl 的处理，他们训练了一个质量分类器（quality classifier）来区分他们认为高质量的内容和其余内容，并做了一些模糊去重，因为 WebText 和 Common Crawl 之间有重复。所以这篇论文遵循了使用分类器进行质量分类的思路。

---

## Datasets: The Pile / 数据集：The Pile

So after GPT-3 came out, this was, I think, a big event. And there were a number of efforts to try to do things in the open. So one of the initial efforts was The Pile, which is a grassroots effort from EleutherAI, where they had a bunch of people in this Discord just jamming and figuring out high quality sources. And they came up with this list in the end. And today, this is still pretty interesting and diverse. It has Common Crawl, it has PubMed. This has this thing called Books3, which we'll talk about. ArXiv, GitHub, which we talked about. Wikipedia, IRC, another BooksCorpus, Philosophy Papers, and so on.

GPT-3 发布后，我认为这是一个重大事件。有很多公开的努力尝试做一些事情。最初的努力之一是 The Pile，这是 EleutherAI 的一个草根（grassroots）努力，他们在 Discord 上聚集了一群人，讨论并找出高质量的数据来源。他们最终列出了一个清单。直到今天，它仍然相当有趣且多样化。它包括 Common Crawl、PubMed。有一个叫做 Books3 的东西，我们一会会讨论。还有 arXiv、GitHub（我们已经讨论过）、Wikipedia、IRC、另一个 BooksCorpus、哲学论文等等。

---

They included this Enron Emails dataset. So Enron went bust in 2002 and all the emails were released, and this is one of the few email datasets we have, which is a weird distribution, I think, for email. But that's what you get. So Project Gutenberg was-- so let's talk about books a little bit. So project Gutenberg was started in 1971, and it only includes books that received copyright clearance. So mostly books in the public domain. There's this packaging of Gutenberg into PG-19, which is Gutenberg before 2019. Which is, I guess most of them, because for them to be in public domain, you have to wait 75 years. So Books3, which is this interesting dataset that appeared in The Pile. So this is described actually as 200k books from a shadow library called Bibliotik that concludes all books from your favorite authors. And at that time-- again, 2020, no one was paying attention. People used it to train models, and since then, it has been taken down. So you cannot use, or should not use Books3 anymore. We'll come back to Books3 again.

他们还包括了安然邮件（Enron Emails）数据集。安然公司在 2002 年破产，所有邮件被公开，这是我们所拥有的少数几个邮件数据集之一——我认为对于邮件来说这是一种奇怪的分布。但这就是你得到的。还有 Project Gutenberg——让我们来谈谈书籍。Project Gutenberg 始于 1971 年，只包含获得版权许可的书籍。所以主要是公共领域的书籍。有将 Gutenberg 打包成 PG-19 的版本，即 2019 年之前的 Gutenberg。我想这包括大部分书，因为要进入公共领域需要等 75 年。还有 Books3，这个出现在 The Pile 中的有趣数据集。它实际上被描述为来自一个名为 Bibliotik 的影子图书馆的 20 万本书，包含了你最喜欢作者的所有书籍。那时——又是 2020 年，没人关注。人们用它来训练模型，此后它被下架了。所以你不能再使用，或者不应该再使用 Books3。我们稍后会再回到 Books3。

---

So Stack Exchange you've probably used quite a bit, although I guess these days maybe less so because of AI. There's a bunch of user-contributed questions and answers, started in 2008. And one thing that is interesting about this dataset is that it's a Q&A format, and this is quite close to a real application. So normally, you think about pre-training data as here's Wikipedia articles, just like raw text. But some parts of the web are actually-- look supervised, like what you would want to ask your language model. Which I think, maybe, helps the model learn certain types of question answering behaviors. So not everything is super magically emergent. It's like, well, this type of data does exist on the web.

Stack Exchange 你可能用得很多，尽管这些天可能由于 AI 用得少了。它始于 2008 年，有大量用户贡献的问答。这个数据集有趣的一点是它采用问答格式，这与实际应用非常接近。通常，你会认为预训练数据就是 Wikipedia 文章、原始文本。但网络的某些部分实际上看起来像监督学习数据——就像你想问语言模型的问题一样。我想这可能有助于模型学习某些类型的问答行为。所以并非所有东西都是超级神奇地涌现出来的——其实，这种类型的数据确实存在于网络上。

---

So there's also-- this data has metadata, which is like the number of votes which are useful for filtering. And again, this data is released in data dumps that allows you to just download without crawling it.

此外，这个数据有元数据，比如投票数，这对过滤很有用。同样，这些数据以数据转储的形式发布，允许你直接下载而无需爬取。

---

## Datasets: Gopher / 数据集：Gopher

So now we're in 2021. There was another paper from DeepMind. They trained a model called Gopher, which was never released, and actually was subsumed by Chinchilla. But the description of the data, I think, is actually really good. You should read this paper, because I think it's very thorough in the way that they describe the data processing. Well, except for the parts where they don't tell you what's in the data. So they created this massive web, and they had C4, which remember, was the dataset that we looked at before from Google. They train on books, news, GitHub, and Wikipedia. They don't say anything about how they got that. So for the MassiveWeb, they kept English, deduped, and their quality filtering was also based on manual rules. And part of the reason for this is that they had more control over that. So I think, as you can see, there is this division between people who wanted to use rules, and people who wanted to use classifiers. So they got, as the name suggests, a massive amount of text, but their model was only trained on a very small fraction of this dataset.

现在我们到了 2021 年。DeepMind 有另一篇论文。他们训练了一个叫 Gopher 的模型，从未发布，实际上被 Chinchilla 取代了。但我认为数据的描述非常好。你应该读这篇论文，因为我认为他们在描述数据处理方面非常透彻。嗯，除了他们不告诉你数据中有什么的部分。他们创建了 MassiveWeb，还有 C4——记住，这是我们之前看到的 Google 的数据集。他们在书籍、新闻、GitHub 和 Wikipedia 上训练。他们没有说明他们是如何获得这些的。对于 MassiveWeb，他们保留了英语，做了去重，质量过滤也基于手动规则。部分原因是他们对这些有更多控制。所以我想，正如你所看到的，在使用规则的人和想使用分类器的人之间存在分歧。结果他们得到了——正如名字所示——海量的文本，但他们的模型只在这个数据集的很小一部分上训练。

---

## Datasets: Llama 1 / 数据集：Llama 1

So in 2022 Llama 1 came out, and the dataset here-- this was actually a very nice paper in that it detailed their data processing. So this is probably one of the last non-open, fully open models that actually talk about their data processing. So they have Common Crawl processed with CCNET, which you know about. The classification, though, was whether the page was a reference of Wikipedia, not whether it is actually a Wikipedia article. So the idea is that well, maybe Wikipedia articles are too stylized. And we know that Wikipedia articles references a bunch of other articles which are presumably good, so let's call those the good websites. They had C4, they did a bunch of processing on GitHub to keep permissive licenses, Wikipedia. They trained on Books3 and project Gutenberg. So Books3 really got them in a lot of trouble because they're just announcing to the world that hey, I trained on this dataset. And if you look back, oh, this came from-- where did it come from? It came from The Pile. Oh, it came from a shadow library. So that's why people don't want to talk about their data anymore.

2022 年 Llama 1 发布，它的数据集——这实际上是一篇非常好的论文，因为它详细描述了数据处理。这可能是最后一批真正讨论其数据处理的非开放或完全开放模型之一。他们使用 CCNET 处理了 Common Crawl——你已经知道这个工具。不过分类的标准是页面是否是 Wikipedia 的参考文献，而不是它是否是一篇 Wikipedia 文章。这个想法是：也许 Wikipedia 文章过于风格化了。而我们知道 Wikipedia 文章引用了一系列其他文章，这些文章大概是好的，所以让我们称这些为好网站。他们还有 C4，对 GitHub 做了大量处理以保留宽松许可，还有 Wikipedia。他们在 Books3 和 Project Gutenberg 上训练。Books3 确实给他们带来了很多麻烦，因为他们向世界宣布"嘿，我在这个数据集上训练了"。如果你回头看，哦，这来自——来自哪里？来自 The Pile。哦，来自一个影子图书馆。所以这就是为什么人们不再谈论他们的数据了。

---

So they looked at arXiv, and actually used the LaTeX to do the processing, Stack Exchange, and they got 1.2 trillion tokens. They didn't actually release this dataset, but they had enough of a description in their processing that this was reproduced by Together's RedPajama V1 dataset, which was then used in other sources. So as you can see here, RedPajama V1 initially also contained Books3, which has now been stripped out. So various decisions made early on about copyright actually influence-- have a fairly big watershed.

他们还使用了 arXiv，并实际使用 LaTeX 进行处理，还有 Stack Exchange，总共得到 1.2 万亿个标记。他们没有实际发布这个数据集，但他们在处理过程中的描述已经足够详尽，以至于 Together 的 RedPajama V1 数据集对其进行了复现，随后又被用于其他来源。如你所见，RedPajama V1 最初也包含 Books3，现在已被移除。所以早期关于版权的各种决策实际上产生了相当重要的分水岭效应。

---

## Datasets: RefinedWeb / 数据集：RefinedWeb

So let's talk about RefinedWeb. So this is a paper that tried to make a point that web data is all you need. So the web, in some sense, is everything. And then we talked about all these specialized sources, like there's GitHub and arXiv, and Stack Exchange. And they said, well, what happens if we just stick with the web? So they did a good job of doing the transformation from HTML to text. They filtered using the Gopher rules, which is basically keep things that look like English. They explicitly, at that time, still said avoid ML-based filtering to avoid biases. I don't want to find an overly narrow subset of the web. They did some deduplication, and they had five trillion tokens. They released about 600 billion of them.

让我们谈谈 RefinedWeb。这是一篇试图论证"网页数据就是你所需的一切"的论文。网络在某种意义上就是一切。而我们已经讨论了所有这些专门的来源，比如 GitHub、arXiv 和 Stack Exchange。他们说：如果我们只使用网络会怎样？他们在 HTML 到文本的转换方面做得很好。他们使用 Gopher 规则进行过滤，基本上是保留看起来像英语的内容。他们当时明确表示避免基于机器学习（ML-based）的过滤以避免偏见——不想得到过于狭窄的网络子集。他们做了一些去重，得到了 5 万亿个标记，发布了其中约 6000 亿个。

---

So FineWeb from Hugging Face was a replication of RefinedWeb, but improved it. So they took all the Common Crawl dumps at that time, did some filtering-- again, using manual rules to not inject biases-- deduped, did PII removal, and got 15 trillion tokens. So you can see that the size of these datasets is growing quite a bit.

Hugging Face 的 FineWeb 是 RefinedWeb 的复现，但做了改进。他们获取了当时所有的 Common Crawl 转储，做了一些过滤——同样，使用手动规则以避免引入偏见——去重、移除个人身份信息（PII removal），得到了 15 万亿个标记。所以你可以看到这些数据集的规模增长了不少。

---

## Datasets: Dolma / 数据集：Dolma

So then there is this Dolma dataset from AI2, and this is a dataset that includes their own processing of Common Crawl, The Stack, which we'll talk about, before C4, which you know about, and a bunch of other things. And the Reddit dataset was from this project called PushShift. And at that time, you could still get this data, and you can train on it before things got locked down. AI2 has their own crawl of academic papers called Semantic Scholar, so they derived a dataset based on that. So let's look at their Common Crawl processing. So they use language identification. So this was model-based, but quality filtering still avoid model-based filtering. And then they removed toxicity using rules and a classifier. And they got three trillion tokens out of that.

然后是 AI2 的 Dolma 数据集，它包含他们自己处理的 Common Crawl、The Stack（我们稍后会谈到）、C4（你已经知道）以及一系列其他内容。Reddit 数据集来自一个叫 PushShift 的项目。当时你仍然可以获取这些数据，并在它们被封锁之前进行训练。AI2 有自己的学术论文爬取，叫做 Semantic Scholar，所以他们基于此导出了一个数据集。让我们看看他们的 Common Crawl 处理。他们使用语言识别——这是基于模型的——但质量过滤仍然避免基于模型的过滤。然后他们使用规则和分类器移除有害内容。他们从中得到了 3 万亿个标记。

---

## Datasets: DCLM / 数据集：DCLM

So DCLM, I think, was maybe a point where this idea of model-based quality filtering started to really become the norm here. So DataComp, the initial motivation was to define some sort of pipeline so that people can try different data methods in a standard way, and show results. But I think the main way that I think people use this is just using their dataset that they released to train models and do other things. So they processed Common Crawl to produce DCLM-pool. So this is completely unfiltered. And if you look at this dataset, this is massive. 240 trillion tokens. This is probably more than the number of tokens that anyone really trains on. But a lot of this is fairly low quality, so then they had a pipeline where all that gets filtered.

DCLM 也许是基于模型的质量过滤思想真正成为规范的一个转折点。DataComp 最初的动机是定义某种流水线，以便人们可以以标准方式尝试不同的数据方法并展示结果。但我认为人们使用它的主要方式就是使用他们发布的数据集来训练模型和做其他事情。他们处理 Common Crawl 来生成 DCLM-pool。这完全没有过滤。如果你看这个数据集，它是巨大的——240 万亿个标记。这可能比任何人实际训练用的标记数还要多。但其中很大一部分质量相当低，所以他们有一个流水线来过滤所有这些。

---

If you only keep English, you have some of rules to really narrow it down. You do dedupe, and then you do this model-based filtering, and you end up with something that's 1.4%. And this is the data set that we'll see actually works pretty well. So the model-based filtering-- and this was strangely good. So to train a classifier, they took OpenHermes, which is essentially instruction data that was generated by GPT-4, and ELI5, which is a subreddit with various questions and answers. So this is-- let's see. These are the type of questions that are in ELI5. So anyway, you get the idea. So it's kind of weird, but somehow this works. So the negative examples are anything from RefinedWeb, which is, remember, it's just a very loosely filtered version of the web. It's basically the web, and it got 3.8 trillion tokens. They train a fastText classifier-- think about it just as a linear classifier. And then they show that this magical classifier, quality classifier, outperforms a bunch of other things that they tried. So, DCLM. This became, for a while, at least in the open community, a bit of a gold standard for quality filtering.

如果你只保留英语，使用一些规则来大幅缩小范围，做去重，然后做基于模型的过滤，最终你得到的是原来的 1.4%。这就是我们看到的效果相当好的数据集。基于模型的过滤——出奇的好。为了训练分类器，他们使用了 OpenHermes（本质上是 GPT-4 生成的指令数据）和 ELI5（一个包含各种问答的子版块）。这些是 ELI5 中的问题类型。反正你明白了。这有点奇怪，但不知怎么就管用了。负例是来自 RefinedWeb 的任何内容——记住，这只是一个非常宽松过滤的网络版本——基本上是整个网络，有 3.8 万亿个标记。他们训练了一个 fastText 分类器——你可以把它看作一个线性分类器。然后他们证明这个神奇的分类器——质量分类器——优于他们尝试的其他方法。所以 DCLM 在一段时间内——至少在开放社区中——成为了质量过滤的黄金标准。

---

## Datasets: Nemotron / 数据集：Nemotron

Let's move on to Nemotron. So Nemotron-- this is from NVIDIA-- they said that well, DCLM filters too aggressively. It's removing most of the data. And remember, they only got-- how many-- 3.8 trillion tokens. So we need more tokens. So what do we do? We are going to do something more, I guess, elaborate. We're going to prompt our existing model to score FineWeb documents based on educational value. So we're going to prompt a language model and say, is this educational or not? Go add a bunch of labels, train a fastText model. So that's one classifier. Another classifier is just using the DCLM classifier. So we're going to use those classifiers. We're also going to use synthetic data. So this is probably one of the-- I don't know if-- it's probably not the first, but, one of the main datasets that really lean into synthetic data for pre-training. So they had, for low quality data, as deemed by these classifiers, you use a language model to rephrase it to make it more-- look like Wikipedia. For high quality data, we use a language model to generate various tasks. For example, given a Wikipedia article, I can generate question answers, or I can generate like, please summarize this document, extract key information from it, and so on. So they resulted in a dataset that was 6 trillion tokens. So this is substantially larger than DCLM.

让我们继续看 Nemotron。Nemotron——来自 NVIDIA——他们说 DCLM 过滤得太激进了，它删除了大部分数据。记住，他们只得到了 3.8 万亿个标记。所以我们需要更多标记。那该怎么办？我们要做一些更精细的操作。我们要提示（prompt）现有模型根据教育价值（educational value）对 FineWeb 文档进行评分。我们要提示语言模型说："这个有教育性吗？"然后添加一堆标签，训练一个 fastText 模型。这是一个分类器。另一个分类器就是直接使用 DCLM 分类器。我们会使用这些分类器。我们还将使用合成数据（synthetic data）。这可能是——我不知道——它可能不是第一个，但它是主要依赖合成数据进行预训练的数据集之一。对于被这些分类器判定为低质量的数据，他们使用语言模型重新措辞，使其看起来更像 Wikipedia。对于高质量数据，他们使用语言模型生成各种任务。例如，给定一篇 Wikipedia 文章，我可以生成问答，或者生成"请总结这个文档"、"从中提取关键信息"等。结果他们得到了一个 6 万亿个标记的数据集。这比 DCLM 大得多。

---

And just for reference, this is still kind of small by some consideration. So Llama 3 was trained on 15 trillion tokens, Qwen3 was trained on 36 trillion. Although there is this-- it's not clear how big these unique tokens are, because when you look at [INAUDIBLE] counts in language modeling papers, some of it is repeated. Like if you do two epochs, that's twice the number of tokens, so you have to be careful when you look at those numbers. And they show that the dataset is better. Their high quality subset beats the previous datasets

仅供参考，按照某些标准这仍然算小。Llama 3 在 15 万亿个标记上训练，Qwen3 在 36 万亿个标记上训练。不过——不清楚这些唯一标记（unique tokens）有多大，因为当你看语言模型论文中的 [听不清] 计数时，有些是重复的。如果你做了两个 epoch，那就是两倍的标记数，所以看这些数字时要小心。他们证明数据集更好——他们的高质量子集超越了以前的数据集。

---

So up until now, we've seen a bunch of different methods for filtering. I think all of these look very similar at some level. You take a web crawl, you either decide I'm going to use rules to filter, or I'm going to use a model. If I'm going to use a model, then I have to decide what looks like good data, and then try to train a classifier, and classify all my documents, and select. And there seems to be a trade-off between you can take a lot of Common Crawl-- you can get 240 trillion tokens if you want, but that's probably going to be really low quality. Or you can get one trillion tokens, and there's some sweet spot in-between.

到目前为止，我们已经看到了一系列不同的过滤方法。我认为所有这些在某种程度上看起来非常相似。你获取网页爬取数据，然后决定要么用规则过滤，要么用模型。如果要用模型，那么我必须决定什么样的数据看起来是好的，然后训练一个分类器，对所有文档进行分类和选择。似乎存在一种权衡：你可以获取大量的 Common Crawl——如果你愿意，你可以得到 240 万亿个标记——但那可能质量非常低。或者你可以得到 1 万亿个标记，中间存在某个最佳平衡点。

---

## Code Data: The Stack / 代码数据：The Stack

Let me talk about two final things. So code, and going back to this question of licensing. So The Stack is a very nice project that was trying to make a really good coding data set, since it was clear by 2022 that coding was going to be really important. So what they did in the initial version is that they clone 137 repos. They kept the ones that were permissively licensed, remove near-duplicates, and resulted in one-- sorry, three terabytes of code.

让我谈论最后两件事。代码，以及回到许可问题。The Stack 是一个非常棒的项目，它试图制作一个非常好的编程数据集，因为到 2022 年已经很清楚编程将变得非常重要。他们在初始版本中所做的是克隆了 137 个仓库。他们保留了那些具有宽松许可的，移除近似重复，最终得到——抱歉——3 TB 的代码。

---

And then in 2024, they had an update. And here they took more the metadata, like the issues, comments, and PRs from GitHub, the repositories from the Software Heritage, which we talked about. They also scraped documentation from various websites by crawling them. They did a bunch of processing. So in GitHub repos, you have binary files which you probably don't want to train on. They have malware, you get rid of that. A lot of GitHub, especially these PRs, are bots, so you have to filter that. Dedupe, do PII redaction. There's a lot pull requests and stuff, and they basically subsample to keep it representative and the dataset manageable.

然后在 2024 年，他们有了更新。这次他们更多地获取了元数据，如 GitHub 的议题（issues）、评论（comments）和拉取请求（PRs），以及我们之前讨论过的 Software Heritage 中的仓库。他们还通过爬取各种网站来获取文档。他们做了一系列处理。在 GitHub 仓库中，有二进制文件——你大概不想在上面训练。有恶意软件（malware），你要去除。很多 GitHub 内容，尤其是这些 PR，是机器人（bots）产生的，所以你必须过滤掉。去重，做个人身份信息编辑（PII redaction）。有大量的拉取请求等，他们基本上通过子采样来保持代表性并使数据集可管理。

---

They also did this thing, which was I thought was nice, which is that there's many programming languages out there. There's a lot of Python, a lot of C, but low resource languages like Nim-- which I hadn't even heard of-- they're not that common. So what they do is they compile this code into a low-level intermediate language, LLVM, which everything, like C Compiler, can compile into this, and they have juxtaposed the low resource language and the intermediate representation. So then the language model can actually learn the mapping between the shared low level representation, which has a lot of data on, and the thing that it does has less data on. And just for fun, you add in all the other good stuff that you can. So Stack V2 is mostly code, and then plus other things that were used to train their coding models.

他们还做了一件事，我觉得很不错：有很多编程语言。Python 很多，C 也很多，但像 Nim（我甚至没听说过）这样的低资源语言并不常见。所以他们的做法是将这些代码编译成低级中间语言 LLVM——所有东西，如 C 编译器，都可以编译成这种形式——他们将低资源语言与中间表示（intermediate representation）并列放置。这样语言模型就可以学习共享的低级表示（有大量数据）与数据较少的语言之间的映射。为了增加趣味，你还可以加入其他所有你能找到的好东西。所以 Stack V2 主要是代码，再加上用于训练其编程模型的其他内容。

---

And one thing about pull requests is that pull requests and all the metadata is not, by its nature, a linearized sequence. So there has to be some steps taken to linearize it. So one important thing you have to decide is how much context to provide. So for example, an event might just be, I change one line of code. And that could just be one line, but presumably to learn that, you want to provide some context, maybe a few lines around it, or maybe the entire file surrounding that diff. And these are some design decisions that you have to make for linearization. And so at the end of the day, the tokens that they train on look something like this, where it's this XML-like structured data, where you have the PR, and then you have a bunch of diffs. And then for comments, you have basically the events of a comment was posted, what the review state of that PR was and so on and so forth. So it's not just learning how to generate code, but also the software development process around code.

关于拉取请求的一点是，拉取请求及其所有元数据本质上不是线性化的序列。所以必须采取一些步骤来线性化它。你需要做的一个重要决定是提供多少上下文。例如，一个事件可能只是"我改变了一行代码"。这可能只是一行，但为了学习它，你可能需要提供一些上下文——也许周围几行，或者整个文件的差异。这些是你在线性化时必须做的一些设计决策。最终，他们训练的标记看起来像这样——类似 XML 的结构化数据，有 PR，然后有一堆差异（diffs）。对于评论，基本上包括评论发布的事件、该 PR 的审查状态等等。所以不仅仅学习如何生成代码，还包括围绕代码的软件开发过程。

---

## Datasets: Common Pile / 数据集：Common Pile

So finally, I'll talk about the common pile. So recall that almost all the data on the internet is copyrighted. Some of it is permissively licensed, some of it is even in the public domain. And while you can appeal to fair use and say, I'm going to train on it anyway, this is not quite settled. So if you're very, very risk-averse, then you say, well, if I don't know whether it is OK, that's a no. If you take that attitude, then that's what common pile did. So can you train a good model with only permissively licensed data? Or rather, how far can you get?

最后，我来谈谈 Common Pile。回想一下，互联网上几乎所有的数据都是有版权的。其中一些是宽松许可的，一些甚至是公共领域的。虽然你可以诉诸合理使用并说"我还是要训练"，但这尚未完全解决。所以如果你非常、非常规避风险，那么你会说，如果我不知道是否没问题，那就是不行。如果你采取这种态度，那么这就是 Common Pile 所做的。那么，你能只用宽松许可的数据训练出好模型吗？或者说，你能走多远？

---

So this was a project that went and scoured the internet for all the different types of data that they could possibly find that was worth training on, that was permissively licensed. It includes Stack V2 in code. It turns out that a lot of government proceedings are actually permissively licensed, wikis, some things on the web-- some new sites are actually permissively licensed, academic papers, online forums, things that are in the public domain, educational resources, and so on. So in the end, there were 8 terabytes of data, which is actually pretty good for permissively licensed data.

这是一个在互联网上搜寻所有可能找到的、值得训练、且具有宽松许可的各类数据的项目。它包括代码方面的 Stack V2。事实证明，大量的政府会议记录实际上是宽松许可的，还有维基、网络上的某些内容——一些新闻网站实际上是宽松许可的、学术论文、在线论坛、公共领域的内容、教育资源等等。最终有 8 TB 的数据，这对宽松许可的数据来说已经相当不错了。

---

Doing this project is actually much harder than maybe it sounds at first glance. It's not just as simple as oh, you look at the license and it's like, oh yep, Apache, or CC, good. There's some subtleties, versus license laundering. So people are sloppy with licenses. So people might take some copyright work and just slap a CC BY on it. Anyone can write this on the internet, and it's hard to tell whether this is real or not. There's also this common practice where, for example, Dolma is permissively licensed. Remember, Dolma is the AI2 collection. But collection licenses don't extend to the individual works. So the collection is-- I mean, first of all, there's a question of whether collections-- I think collections can be copyrighted, but I guess you can put a license on anything. But the individual works are not necessarily good. So you can't just look at data sets on Hugging Face, and you-- many data sets on Hugging Face you see, they have a permissive license. But if you dig deeper, it's actually not permissively licensed at the individual level.

做这个项目实际上比初看起来要困难得多。它不像"哦，你看看许可，是 Apache 或 CC，好的"那么简单。存在一些微妙之处，还有许可洗白（license laundering）。人们对许可的态度很马虎。有人可能拿了一些受版权保护的作品，直接贴上 CC BY 标签。互联网上任何人都可以这么写，很难判断这是否真实。还有一种常见做法，例如 Dolma 是宽松许可的。记住，Dolma 是 AI2 的数据集集合。但集合的许可并不延伸到单个作品。首先，有一个问题——我认为合集是可以有版权的，但我想你可以在任何东西上放许可。但个别作品不一定没问题。所以你不能只看 Hugging Face 上的数据集——很多 Hugging Face 上的数据集有宽松许可，但如果你深入挖掘，实际上在个体层面并不是宽松许可的。

---

And they also made a decision to forego training on any synthetic data, because training language models on unlicensed data is unclear. So probably it's fine because technically, these are open weight models with MIT license. You can do whatever. You can use them however you want, but these language models were presumably also trained on unlicensed data. So it's a little bit of data laundering if you are really honest here.

他们还决定放弃在任何合成数据上训练，因为语言模型在未经许可的数据上训练是不明确的。所以可能没关系，因为从技术上讲，这些是 MIT 许可的开放权重模型。你可以做任何事。你可以以任何方式使用它们，但这些语言模型大概也是在未经许可的数据上训练的。所以如果你真的很诚实的话，这有点像数据洗白（data laundering）。

---

So with this data, they compare it with a bunch of other models like the first Llama, MPT, and Qwen. And on a bunch of benchmarks, they show that this is not bad. I would say it's not as good as the Qwen models for sure, but it's certainly outperforming the very old-- this is from 2023, I guess. So quite old models. So I would say, the conclusion here is that you can do reasonably, but I think it's still pretty tough to compete without doing more tokens. But I don't think this is the final word on it, and I think you can probably eke more out of publicly permissive licenses if you try.

用这个数据，他们将其与一系列其他模型（如第一个 Llama、MPT 和 Qwen）进行比较。在一系列基准测试上，他们显示这并不差。我会说它肯定不如 Qwen 模型好，但它肯定超过了非常旧的模型——我想这是 2023 年的模型。所以相当旧的模型。所以我认为，结论是你可以做到相当不错，但如果不使用更多的标记，竞争仍然很困难。但我不认为这是定论，我认为如果你尝试，可能可以从公开的宽松许可中榨取更多价值。

---

## Summary / 总结

OK, so to summarize this lecture here. So maybe hopefully now I've given you some appreciation that data is a very rich topic. It's not that data just falls from the sky, or you just go on Hugging Face and you download a dataset. Data has to come from somewhere. And there's also a technical but also social context in which data comes, because at the top, the internet is a bunch of live services. Someone has to do the work of producing raw data, whether it be the website that gives you dumps, or someone has to build a crawler, or something. And then, someone has to make the decision of how to process it into usable form-- filtering, transformation, deduplication, all these things have an impact on the quality of your final language model.

好，总结一下这节课。希望现在我已经让你意识到数据是一个非常丰富的主题。数据不是从天而降的，也不是你上 Hugging Face 下载一个数据集就行。数据必须来自某个地方。而且数据还带有技术和社会背景，因为归根结底，互联网是一堆实时服务。有人必须完成生产原始数据的工作，无论是提供转储的网站，还是有人必须构建爬虫，或其他什么。然后，有人必须决定如何将其处理成可用的形式——过滤、转换、去重——所有这些都会影响最终语言模型的质量。

---

And notice that filtering is probably one of the most important things. How do you go from 200 trillion tokens to less than three trillion tokens? I think that obviously is a huge reduction, which I think merits a lot of attention. Data is, in some sense, a key ingredient that differentiates language models. A lot of language models are roughly the same kind of transformer architecture, but data is depending on how you process it. It can make a pretty big difference. There's plenty of legal and ethical issues around data, more than I can get into this lecture. And also, this process is very messy. Unlike some of the other parts of this class where things are maybe more based on first principles, data processing is, right now at least, a lot just based on vibes you set up. You define this classifier, you define this rule, you set some threshold. So there are many opportunities to improve. So as you do your assignment four, maybe think about whether there's better ways to do this, and this could be maybe a research direction.

注意，过滤可能是最重要的事情之一。如何从 200 万亿个标记减少到不到 3 万亿个标记？这显然是一个巨大的缩减，非常值得关注。在某种意义上，数据是区分不同语言模型的关键要素。很多语言模型大致是相同类型的 Transformer 架构，但数据的处理方式会产生很大的差异。关于数据还有大量的法律和伦理问题，比我这节课能涵盖的要多。此外，这个过程非常混乱。不像这门课的其他一些部分那样更多基于第一性原理（first principles），数据处理——至少目前——很大程度上基于你设定的"感觉"。你定义这个分类器，你定义这个规则，你设定某个阈值。所以有很多改进的机会。所以在做第四次作业时，也许思考一下是否有更好的方法，这可能成为一个研究方向。

---

OK, so that's it for today. So next time I'll continue talking about data. I'll talk a bit about post-training data, and a bit more about filtering.

好，今天就到这里。下次我会继续讨论数据。我会谈一些关于后训练数据的内容，以及更多关于过滤的内容。

---
