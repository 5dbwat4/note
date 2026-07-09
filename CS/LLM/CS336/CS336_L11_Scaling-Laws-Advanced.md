---
title: "Lecture 11: Scaling Laws (Advanced)"
---

# Lecture 11: Scaling Laws (Advanced) / 第11讲：缩放定律（进阶）

---

OK, we are going to continue our scaling journey. Today's a bit of a grab bag of stuff. I mean, we're really going to talk about some of the more advanced details of scaling laws and how we scale up models. And in doing so, we're going to cover what I feel like are some important details in how you would scale up a language model in practice. So we might want to ask some questions, like the scaling law stuff that you talked about two lectures ago, does that actually work at real building open-source model scales? It would be nice if we could optimize some of this. There's a lot of learning rate tricks and other things that people do that I think you should know as people that are informed about how to build language models. So we'll talk about some of these optimization details. And then I think the last thing I want to talk about is, when we scale up, there are certain things that are going to be a little bit trickier to tune. We know that optimizers and optimizer behavior is going to be actually pretty scale sensitive. And because of that, things like initializations, learning rates, batch size, those we need to carefully think about as a function of scale. So we will talk about how to think about those carefully.

好的，我们将继续我们的缩放之旅。今天的主题比较杂。实际上，我们要讨论缩放定律的一些更高级的细节，以及我们如何扩展模型。在此过程中，我会涵盖我认为在实际中如何扩展语言模型的一些重要细节。我们可能会问一些问题，比如两讲前讨论的缩放定律，在真正构建开源模型时是否真的有效？如果能对此进行优化，那就太好了。有很多关于学习率的技巧以及其他一些做法，我认为作为了解如何构建语言模型的人，你们应该知道这些。所以我们先讲一些优化细节。然后我想讲的最后一点是，当我们扩展模型时，有些东西调起来会棘手一些。我们知道优化器(optimizer)及其行为实际上对规模(scale)非常敏感。正因为如此，初始化(initialization)、学习率(learning rate)、批大小(batch size)等因素，我们需要根据规模仔细考虑。所以我们会讨论如何仔细思考这些问题。

---

Up until now, most of our discussions is what I would call the classical scaling laws cannon. We talked about Kaplan. We talked about, oh, even Hestnes and then the Chinchilla paper. So we're up to date with, I don't know, 2022 or something. Since then, there have been a number of scaling papers that are published by people who train big models. Although, I think the number of such papers have decreased in recent years, and most of them have come out of the open-source community in China. And so today, I want to talk about a number of these that I've curated and selected to give you a sense of, what does scaling at the frontier, at least open frontier, look like? What are the things that these people care about or worry about? And what would you need to do to speedrun your way from Chinchilla all the way to, let's say, Kimi K2, the most recent release that has some scaling details. So that's going to be the first part of this lecture. We're going to go through a couple of papers, and we're going to go through the details.

到目前为止，我们讨论的大部分内容可以称为经典的缩放定律(Scaling Laws Canon)。我们讨论了 Kaplan，我们讨论了 Hestnes，还有 Chinchilla 论文。所以我们目前掌握的知识大概停留在 2022 年左右。从那时起，训练大模型的人发表了许多关于缩放的论文。不过我认为这类论文的数量近年来有所减少，而且大部分来自中国的开源社区。所以今天，我想讨论一些我精心挑选的论文，让大家了解前沿缩放（至少是开源前沿）是什么样子的？这些研究者关心或担忧什么？你需要做些什么才能从 Chinchilla 一路快速推进到例如 Kimi K2——最新发布、包含缩放细节的模型？这将是本讲的第一部分。我们会详细阅读几篇论文。

---

The second part is going to be a discussion of optimizers and initializations. And remember, I spent a nontrivial amount of time two lectures ago on the selection of batch sizes. That's going to be an important factor. And it's also going to be important thinking about how we're going to tune things like learning rates. Those are very sensitive, very important to get right. And so it turns out that a lot of effort has been invested into getting those things right. And we will talk about some of the techniques to do so. And this may, in fact, even be useful in your day to day lives of training various language models because they'll give you a sense of how to change your hyperparameters and your experiments as you scale up or down.

第二部分将讨论优化器(optimizer)和初始化(initialization)。记住，两讲前我花了不少时间讨论批大小的选择。这将是一个重要因素。同样重要的是考虑如何调整学习率之类的参数。这些参数非常敏感，必须设置正确。事实上，人们投入了大量努力来确保这些参数的正确。我们将讨论一些相关技术。这实际上甚至可能对你们日常训练各种语言模型有用，因为它们会让你了解在扩展或缩减规模时如何调整超参数(hyperparameter)和实验。

---

So I'm going to spend a nontrivial amount of time talking about two papers in particular. They're not the newest papers. They're not necessarily the most-- actually, DeepSeek one might be one of the more detailed ones-- most detailed scaling paper in general. But I think this hits a sweet spot. So both of these papers are serious scaling investigations from people who build reasonably high-performance models. And importantly, they take pretty different approaches to some of the key questions that we will ask today. And so I think they're a good way to motivate a lot of the rest of the lecture. So I'm going to talk about these two. First one is MiniCPM. This was, I think, back in 2024, high-performance small language model. And DeepSeek-- you all are now familiar with this. I no longer have to justify why I'm talking about DeepSeek, which is great.

我会花不少时间特别讨论两篇论文。它们不是最新的论文，也不一定是最——实际上，DeepSeek 那篇可能是一般意义上最详细的缩放论文之一。但我认为这恰到好处。这两篇论文都是来自构建了相当高性能模型的人所做的严肃缩放研究。重要的是，它们对我们今天将提出的一些关键问题采取了截然不同的方法。所以我认为它们能很好地引出本讲其余的大部分内容。我先讨论这两篇。第一篇是 MiniCPM。我记得是 2024 年的工作，一个高性能的小语言模型。然后是 DeepSeek——你们现在已经很熟悉了，我不需要再解释为什么讨论它了，这很好。

---

We'll start by talking about MiniCPM, though. I do like this paper, especially when it first came out. It felt very fresh and new and at the cutting edge. Even in 2026, I feel a lot of the things that the CPM folks did has been informative to us. I'll talk about this later as I get to the newer papers. But I think it's becoming the case that a lot of this classic scaling stuff, how you set learning rates, how do you do Chinchilla, those kinds of things I think are now taken for granted. Everyone just assumes that you know how to do those things. And so people don't really talk about those as much anymore in the papers, so it's really nice to talk about some of these older papers for that reason. So MiniCPM is an effort by a bunch of industry academic partnerships folks over in the Chinese open-source community to come up with a high-performance, small-ish language model. And at the time when this came out, it was basically state of the art for the 1 to 2 billion parameter bracket. Nowadays, Gemma and other models at 2B or 3B are going to be higher performance. But these are competitive, well-trained models, at least as at 2024 standards.

不过我们先从 MiniCPM 开始。我确实喜欢这篇论文，尤其是它刚出来的时候，感觉非常新鲜新颖，处于前沿。即使在 2026 年，我认为 CPM 团队所做的很多东西对我们仍有启发。我在讲到更新的论文时会再提到这一点。但我认为现在很多经典的缩放知识——比如如何设置学习率，如何做 Chinchilla——这些已经成了理所当然的东西。每个人都假设你知道该怎么做。所以论文中不再那么频繁地讨论这些了，正因如此，讨论一些较老的论文是很好的。MiniCPM 是中国开源社区中一批产业界-学术界合作者共同努力的成果，旨在打造一个高性能的、较小规模的语言模型。它刚发布时，基本上是 10 亿到 20 亿参数规模区间的 state of the art。如今，Gemma 和其他 2B 或 3B 模型性能更高。但这些仍然是具有竞争力、训练良好的模型，至少按 2024 年的标准如此。

---

## MiniCPM: Scaling Approach / MiniCPM：缩放方法

So how do you train these models? As I said before, we have to get some of these scaling parameters right. And one of the things that I'll talk about today that I'll emphasize quite a bit is, initializations are very important. Initializations are important because they allow you to make certain hyperparameters less scale dependent. So the first technique that I want to talk about from this MiniCPM paper is a special class of initializations called muP. So muP, the whole point of this approach is to say, I want to make sure that my optimal learning rate is the same as I scale up and down. I talked about this very briefly in the two lectures ago, so you should hopefully remember that a little bit. But this is the first real instantiation that we're going to talk about.

那么如何训练这些模型呢？正如我之前所说，我们必须正确设置一些缩放参数。今天我重点强调的一件事是：初始化非常重要。初始化之所以重要，是因为它能让某些超参数不那么依赖于规模。所以我想从 MiniCPM 论文中讨论的第一项技术是一类特殊的初始化，称为 muP（最大更新参数化，Maximal Update Parametrization）。muP 的核心思想是：我希望确保当我扩展或缩减规模时，最优学习率保持不变。两讲前我简要提到过这一点，希望你们还有点印象。但这是我们即将讨论的第一个真正的实例化。

---

What does that look like specifically? The MiniCPM paper has a nice list of things to do, so they scale the embedding output. They scale the residual connections by the square root of the number of layers. They scale the initialization of all of their matrix-shaped tensors by the fan-in, fan-out ratio. They scale the learning rates of tensors. And you should pay attention to this one because this is exotic if you aren't used to per parameter learning rates. And then they also scale the LM heads. We'll talk about why you do these things, or how you derive this particular set of scalings. Suffice to say that you're just going to change up how you're going to do your initializations and your learning rates a little bit in the hopes of stabilizing your learning rates a little bit.

具体来说是什么样子的？MiniCPM 论文有一份很好的操作清单：他们缩放嵌入输出(embedding output)，他们按层数的平方根缩放残差连接(residual connections)，他们按扇入/扇出比(fan-in/fan-out ratio)缩放所有矩阵张量的初始化，他们缩放张量的学习率——这一点你要注意，如果你不习惯逐参数学习率(per parameter learning rate)，这看起来会很不寻常。然后他们还缩放了 LM 头。我们会讨论为什么做这些事，以及如何推导出这套特定的缩放规则。简单来说，你只需要稍微改变初始化和学习率的做法，以期稳定学习率。

---

And of course, we're training a small model here, but we're still wanting to do a nice scaling strategy. Part of the point of this study is not that you want to brute force a 1.5 model, like training hundreds of them. You want to get the hyperparameters exactly right the first time. So you're going to train a bunch much smaller models and then get a scaling ladder up all the way to your target size of 5x or so. And so there's about a 5x gap between the biggest model they train on their ladder and the actual model that they're going to finally release. And their goal is going to nail down, I think, what most people consider to be the sensitive parameters, like optimal batch size, learning rate. And then the token-to-size ratio that we talked about at Chinchilla. They also want to replicate a Chinchilla analysis, much less important to us now and probably to you even if you're training. But I'm going to talk about it regardless because there's one important thing in the way they do that and that I think has been informative and useful.

当然，我们在这里训练的是小模型，但我们仍然希望有一个好的缩放策略。这项研究的重点之一不是蛮力训练一个 1.5B 模型（比如训练几百个），而是希望第一次就把超参数完全调对。所以你要训练一堆更小的模型，然后建立一个缩放阶梯(scaling ladder)，一直到达目标规模（约 5 倍）。他们训练的阶梯上最大模型与实际最终发布的模型之间大约有 5 倍的差距。他们的目标是锁定大多数人认为敏感的参数，比如最优批大小、学习率，以及我们在 Chinchilla 中讨论过的 token 与模型大小的比例。他们还希望复现 Chinchilla 分析——这对我们现在来说不太重要，对于正在训练的你来说可能也是如此。但我还是要讨论它，因为他们的做法中有一个重要的点，我认为很有启发性和实用性。

---

As I said earlier, the whole point of going through this weird initialization or nonstandard initialization called muP is to try to make the optimal learning rate stable. Is it? At least in the MiniCPM case, the answer is yes. In fact, it's very, very clean in their experiments. They sweep learning rate across a variety of models, so each line is a model size. The minimal loss is basically right on 10 to the negative 2. I guess the minima slightly shifted for the smallest model. But even then, it's quite close to the minimum. So this is a nice success case of the muP approach. We will talk about several other models and other papers that use muP. This is not the only way to do it, but this is one effective way to do it. And if you can get something like this, now you've removed the need to tune the learning rate.

正如我早先说过的，采用这种称为 muP 的奇特（或者说非标准）初始化的全部目的，就是试图使最优学习率保持稳定。它做到了吗？至少在 MiniCPM 的情况下，答案是肯定的。事实上，在他们的实验中非常非常干净。他们在多种模型上扫描学习率，每条线代表一个模型大小。最小损失基本上就在 10 的负二次方处。我想最小点对最小的模型稍有偏移，但即使那样也非常接近最小值。所以这是 muP 方法的一个成功案例。我们还会讨论使用 muP 的其他几个模型和论文。这不是唯一的方法，但这是一条有效的途径。如果你能做到这一点，就消除了调学习率的必要。

---

But of course, even if you have a nice parameterization that fixes your learning rate to a single optimum, your optimal batch size is still not going to be the same. So the batch size actually varies as a function of both data set size and model size. So in their case, they run these model training runs. So each column of points that you see on these plots is a training run. So they have a fixed batch size, and they increase the number of tokens processed, I guess, from bottom to top. And then they ask, OK, we've done many of these training runs. What is the optimal batch size fitting these quadratic curves onto each of these lines over here, this equal loss contour? What they find is this kind of optimal batch size scaling as a function of the number of tokens processed, and they do this across different model sizes. Maybe you would not be surprised by this, given the nice scalings that we saw in the Kaplan paper for critical batch sizes. But the optimal batch size does have a power law structure with respect to the target loss. And so we see exactly the Kaplan-style analysis of, if your loss is lower on the left, your batch size should be bigger, critical batch size scaling.

但当然，即使你有一个很好的参数化方法将学习率固定到一个最优值，你的最优批大小仍然不会是恒定的。批大小实际上随数据集大小和模型大小而变化。在他们的案例中，他们运行了这些模型训练：你在这些图上看到的每一列点都是一次训练运行。他们固定批大小，然后从下到上增加处理的 token 数量。然后他们问：我们做了这么多训练运行，拟合这些二次曲线到每条线上（这些等损失等高线后），最优批大小是多少？他们发现最优批大小随处理的 token 数量呈某种缩放关系，并且在不同的模型规模下都做了分析。考虑到我们在 Kaplan 论文中看到的关于临界批大小(critical batch size)的优美缩放，你可能不会对此感到惊讶。但最优批大小确实与目标损失之间存在幂律(power law)结构。所以我们看到了典型的 Kaplan 式分析：如果左边的损失更低，你的批大小应该更大——临界批大小缩放。

---

And so now given a particular loss target, which you can back out from the scaling laws, you can basically set what the optimal or critical batch sizes that would give you the best trade-offs. So there's a nice clean trend here. This will let you set batch size very easily and precisely. So those two, the batch size and the learning rate scaling, they're going to come back over and over again. Those are arguably the most important and sensitive parameters to do scaling laws on.

因此，给定一个特定的损失目标（你可以从缩放定律中推导出来），你基本上就可以确定能给你最佳权衡的最优或临界批大小。这里有一个非常清晰的趋势，可以让你非常轻松而精确地设置批大小。所以这两个——批大小和学习率缩放——会反复出现。它们可以说是做缩放定律研究时最重要和最敏感的参数。

---

But I'll talk about one last thing in the MiniCPM paper that I think is important. So remember, to do Chinchilla, we need to train a lot of different models. So we're going to, let's say, do IsoFLOPs. That means I'm going to fix a FLOPs budget, and I'm going to vary my trade-offs between number of tokens and model size. And to do that, I'm going to, let's say, increase the amount of data I train on, so increase the number of sequences. But as I increase the number of sequences, remember that each one of these gets a different learning rate schedule. You all training on cosine learning rates. Cosine learning rates look different. You need to know the terminal total budget before you train in order to have a cosine schedule. And so this leads to an annoying fact, which is that you just need to keep retraining your models. If you want to train a 8 million sequence model, you can't restart from the end of a 4-million sequence model. You have to just restart from scratch because your learning rate schedule is just fundamentally different. This is just very annoying. It's like a quadratic cost in some sense of doing this because you have to keep restarting your runs just from the start. And this seems very wasteful, and I think lots of other people did, too.

但我还要讨论 MiniCPM 论文中我认为重要的最后一件事。记住，要做 Chinchilla 分析，我们需要训练许多不同的模型。比如我们要做 IsoFLOPs 分析。这意味着我要固定 FLOPs 预算，然后在 token 数量和模型大小之间进行权衡。为此，我假设要增加训练数据量，也就是增加序列数量。但随着序列数量的增加，每个序列会得到不同的学习率调度(learning rate schedule)。你们都在用余弦衰减(cosine decay)学习率。余弦学习率调度看起来是不同的：你需要在训练之前知道最终的总体预算才能制定余弦调度。这导致了一个令人烦恼的事实：你需要不断地重新训练你的模型。如果你要训练一个 800 万序列的模型，你不能从 400 万序列模型的终点继续训练。你必须从头开始重新训练，因为你的学习率调度从根本上不同。这非常烦人。在某种意义上，这样做有二次成本，因为你必须不断地从头开始运行。这看起来非常浪费，我想很多其他人也有同感。

---

And I think one of the nice solutions from the MiniCPM paper is what's now called, I think, the warmup stable decay learning rate. Or this is the popular term for this, and it's basically a big trapezoid. So you've got a warmup phase. The warmup phase is usually defined as a constant number of steps, not as a fraction of your training target. So this is independent of your training horizon. You've got a fairly long run where you're holding the learning rate constant. That's the stable phase. And then at the end, you're going to decay fairly rapidly down to 0. That's the decay phase. And generally, the decay phase is something like 10% to 20% of your total training run. So you're going to be stable for the vast majority of your training run and then do a very rapid decay down to usually about 10% of your maximum learning rate at the very end here. And that's a very typical warmup, stable, decay learning rate.

我认为 MiniCPM 论文中一个很好的解决方案就是现在所谓的 WSD（预热-稳定-衰减，Warmup-Stable-Decay）学习率。这是流行的叫法，它基本上是一个大梯形。你有一个预热(warmup)阶段。预热阶段通常定义为固定的步数，而不是训练目标的一个比例——所以它独立于你的训练长度。然后有一个相当长的阶段，你保持学习率恒定，这是稳定(stable)阶段。最后，你相当快速地衰减到 0，这是衰减(decay)阶段。通常衰减阶段约占整个训练的 10% 到 20%。所以你在绝大部分训练时间里都是稳定的，然后在最后快速衰减到最大学习率的约 10%。这就是非常典型的预热-稳定-衰减学习率调度。

---

And why do we do this? What's the point of doing this? Well, we do WSD because now we can restart a run at any point at the end of the stable phase. So if I want to reuse a run and train it for longer, I'll just roll back my training to the last stable checkpoint. And then I'll just run the stable learning rates forward and then decay the model down to 0. So this provides a very easy way for us to essentially run scale in data experiments without constantly rerunning your experiments. So you do have to redecay every time, but that's maybe 10% of the total cost. It's a much better situation to be repeatedly decaying than to repeatedly rerun your pre-training runs. And this is a very common trick that's used in many places.

我们为什么要这样做？做这个的目的是什么？我们使用 WSD 是因为现在我们可以从稳定阶段结束时的任何一点重新开始训练。所以如果我想重复使用一次运行并训练更长时间，我只需将训练回滚到最后一个稳定检查点(stable checkpoint)，然后以稳定学习率继续运行，最后将模型衰减到 0。这为我们提供了一种非常简单的方法来执行数据规模的实验，而无需不断重新运行实验。你确实每次都需要重新衰减，但这可能只占总成本的 10%。反复衰减比反复重新运行预训练要好得多。这是一个在很多地方都在使用的常见技巧。

---

I'll show, I guess, a performance comparison. There have been many plots of this form. I think, who was the most recent folks that were-- maybe it was Martin Jaggi and others, I think, over at ETH had an extensive study of WSD performance. But I think a lot of papers have shown similar things of, you have a well-tuned cosine learning curve. This is the orange line over here. And then you've got various WSD curves. And WSD curves always look a little bit funky because it looks like you're way underperforming until you hit the decay phase, where suddenly you reclaim all of your gains. And then you match or even sometimes exceed the cosine learning rate performance. Anecdotally, I think if you talk to a bunch of people training networks, I think a lot of people will say the cosine is slightly better in many cases. But WSD is basically as good in many other situations. It is a very versatile default learning rate. It doesn't necessarily suffer from having to rerun if you want to just continue runs. It is very cool though, to see just how much of an impact learning rate decay has if you haven't played with that before. This part of decaying the learning rate is just incredibly important to getting the final annealing parts of your training together.

我来展示一下性能对比。这类图有很多。最近可能是 Martin Jaggi 等人（苏黎世联邦理工学院）对 WSD 性能做了广泛研究。但我认为很多论文都展示了类似的结果：你有一个精心调优的余弦学习率曲线（图中的橙色线），然后你有各种 WSD 曲线。WSD 曲线看起来总是有点奇怪，因为看起来你一直表现不佳，直到进入衰减阶段，突然间你收回了所有的收益，然后匹配甚至有时超过余弦学习率的性能。据传闻，如果你和许多训练网络的人交流，很多人会说余弦在很多情况下稍好一些。但 WSD 在许多其他情况下也基本上一样好。它是一个非常多功能的默认学习率调度。它不会因为你想继续运行而需要重新运行。不过，如果你之前没有尝试过，看到学习率衰减的巨大影响还是很酷的。衰减学习率这部分对于最终完成训练的退火阶段(annealing)来说极其重要。

---

OK, so that's the comparison there. So now that we're equipped with WSD SGD style learning rates, Chinchilla style analyzes are actually very easy. What you're going to do is you're going to essentially run one long run, and then you'll just rewind the checkpoints and then repeatedly decay. And that will give you sweeps along the data dimension. And then you'll also do sweeps along the model dimension. You can do flops or any other kind of analysis that you would like. The MiniCPM authors, for whatever reason, choose to try to replicate methods 1 and 3, which, to me, are the least reliable of the Chinchilla methods. But they do get fairly nice looking scaling curves. If you look at the MiniCPM Chinchilla method 1, they see nice, lower envelopes that look mostly linear across these, which is good. And then method 3, they get nice, smooth scaling for the most part in both the compute to nonembedding parameter trade-off.

好，这是对比。现在我们有了 WSD/SGD 风格的学习率，Chinchilla 风格的分析实际上非常容易。你要做的是：基本上运行一次长训练，然后回滚检查点，反复衰减。这能给你沿数据维度的扫描。然后你还要沿模型维度做扫描。你可以做 FLOPs 分析或任何其他你喜欢的分析。MiniCPM 的作者无论出于什么原因，选择尝试复现方法 1 和方法 3——在我看来，这是 Chinchilla 方法中最不可靠的两种。但他们确实得到了相当好看的缩放曲线。如果你看 MiniCPM 的 Chinchilla 方法 1，他们看到了很好的下包络线，基本呈线性，这很好。方法 3 中，他们在计算量与非嵌入参数之间的权衡上也得到了大部分情况下平滑的缩放曲线。

---

So it seems like, for the most part, they get reasonable Chinchilla-looking fits. One thing I will point out is that they get pretty different exponents for their overall joint fit compared to Chinchilla. They claim in the paper that this means that they should be training with way more pieces of text than Chinchilla. It is highly unclear to me whether this is a really true or whether their Chinchilla fits are a little bit strange relative to the Chinchilla paper.

所以看起来，大部分情况下他们的拟合结果看起来是合理的 Chinchilla 式拟合。我要指出的一点是，他们的整体联合拟合的指数与 Chinchilla 相比有很大不同。他们在论文中声称这意味着他们应该用比 Chinchilla 多得多的文本来训练。我很不清楚这到底是真实情况，还是他们的 Chinchilla 拟合相对于 Chinchilla 论文来说有点奇怪。

---

## MiniCPM: Key Takeaways / MiniCPM：关键要点

OK, I'll stop here for a moment in case someone has questions about MiniCPM. Maybe the main couple things to take away is, one is the use of muP is a useful trick, I guess, to try to stabilize how your learning rate changes over scales. And then the second thing maybe to remember is the WSD learning rate. That's just a very common trick. You should all know about this learning rate. That's a basic thing to know.

好，我在这里停一下，以防有人对 MiniCPM 有问题。可能主要需要记住的两件事是：第一，使用 muP 是一个有用的技巧，试图稳定学习率随规模的变化方式；第二，要记住 WSD 学习率调度。这是一个非常常见的技巧，你们都应该了解这种学习率调度——这是基础知识。

---

## DeepSeek: Scaling Approach / DeepSeek：缩放方法

OK, good. All right, so then I'll move on to DeepSeek. This is the original DeepSeek paper, before they started talking about MOEs and all these other very cool things. And I think, even at the very first DeepSeek paper, you could tell that these were very serious people because I think DeepSeek LLM, even now, is, I think, one of the more nicely executed scaling analyses in the open world. And I feel like they have lots of great taste in the experiments that they run. So even before R1 and so on came out, it was kind of clear that these people were going places.

好，那我们进入 DeepSeek。这是最初的 DeepSeek 论文，在他们开始讨论 MoE 和所有其他很酷的东西之前。我认为，即使在第一篇 DeepSeek 论文中，你就能看出这些人非常认真，因为 DeepSeek LLM 即使在现在也是开源世界中最漂亮的缩放分析之一。我感觉他们在实验设计上有很多很好的品味。所以甚至在 R1 等出来之前，就清楚这些人会有所作为。

---

All right, so DeepSeek takes a very different scaling strategy than MiniCPM and several others in trying to optimize their hyperparameters. They're not going to really do muP. They're not going to do this interesting scaling adjustments. Instead, they're going to try to fit a scaling law to estimate both the optimal batch size and the optimal learning rate. So we know that the learning rate and batch sizes should actually change with scale. But if the way in which they change are predictable, just like a scaling law, then we're good to go. We don't really need to worry about very much. So what they do is they basically run extensive grid searches at various different scales, and they try to find the optimum.

DeepSeek 在优化超参数方面采取了与 MiniCPM 和其他几个模型非常不同的缩放策略。他们不会真正使用 muP，不会做这些有趣的缩放调整。相反，他们尝试拟合一个缩放定律来同时估计最优批大小和最优学习率。我们知道学习率和批大小实际上应该随规模变化。但如果它们变化的方式是可预测的——就像缩放定律一样——那么我们就没问题，不需要太担心。所以他们的做法是：在不同规模下运行大量的网格搜索(grid search)，试图找到最优值。

---

So this is an example of the kind of thing they're doing. They're sweeping learning rates. They're sweeping batch sizes. And they're looking at the terminal loss if they're processing a particular number of tokens. So they fixed the compute, and then they vary these two. They'll do this across several different scales, and then they'll basically try to identify what the lowest loss is, so in this case, the lightest color. So they'll put a little star there, and then they'll do this across scales.

这是他们所做工作类型的一个例子。他们扫描学习率，扫描批大小，然后观察在处理特定数量 token 时的最终损失。所以他们固定计算量，然后变动这两个参数。他们在几个不同的规模上这样做，然后试图找出最低损失（在这种情况下是最浅的颜色）。他们会在那里放一个小星星，然后跨规模重复这个过程。

---

So if you do this across sufficiently many scales, you will get a plot that looks a little like this. And this plot is saying, OK, I'm going to vary my nonembedding training flops across some range. And you can see these gray dots over here. And as I vary this, my optimal batch size will change. Remember, the optimal batch size is derived by looking at these big grids and finding the minimizer. And I will get something that looks like a line. The optimal batch size should scale with my nonembedding FLOPs. And similarly for my optimal learning rate, I'll get a bunch of gray dots in my nonembedding FLOPs range. And then I can fit a line to that to try to estimate what my optimal learning rate should look like.

所以如果你在足够多的规模上这样做，你会得到一张看起来像这样的图。这张图在说：我在某个范围内改变我的非嵌入训练 FLOPs。你可以看到这些灰色的点。当我改变这个值时，我的最优批大小会变化。记住，最优批大小是通过查看这些大网格并找到最小值点推导出来的。我会得到看起来像一条线的东西。最优批大小应该随我的非嵌入 FLOPs 缩放。类似地，对于最优学习率，我会在非嵌入 FLOPs 范围内得到一堆灰色点，然后我可以拟合一条线来估计我的最优学习率应该是怎样的。

---

So this is fairly nice. And I guess one thing I'll point out is, their full runs are on the star. These are the runs that they chose. At higher FLOPs, they have much higher batch sizes and much lower learning rates. The stars are the things they actually ran for their big runs. These fits look reasonable for the batches. This does look like a line. The one on the learning rate-- I'm not quite sure that constitutes the best linear fits that I've seen in my life, but I guess it works. It's probably fine. The models do train. The models do get reasonable things. I think this is the one, I would say, like drawback of the learning rates approach. It's not really clear that if you try to do this grid search kind of thing, unless your grid is in the right place, you've got a lot of quantization error. And then you're not getting very good scaling law fits, and you end up with something that looks like an arbitrary linear thing going on.

这相当不错。我想指出的一点是，他们的完整运行用的是星星标记的。这些是他们选择的运行。在更高的 FLOPs 下，他们有更大的批大小和更低的学习率。星星是他们实际用于大规模运行的东西。这些拟合对批大小来说看起来合理，确实像一条线。但学习率的那条——我不太确定这是不是我见过的最好的线性拟合，但我想它可行，可能还行。模型确实训练了，模型确实得到了合理的结果。我想这就是学习率方法的一个缺点：不太清楚如果你做这种网格搜索，除非你的网格位置合适，否则会有很多量化误差(quantization error)，然后你就得不到很好的缩放定律拟合，最终得到的东西看起来像一条任意的线。

---

OK, oh, yeah, sorry. How come for the same number of training swaps there, you get multiple data points with a large range of optimal vertices? Why is it that you get a large range of optimal learning rates for different training FLOPs? Is that the question on the y-axis over here? Yeah, so the reason I think there is because of the changes to the model sizes and things like this.

哦对，抱歉。为什么在相同训练量下，你会得到多个数据点，最优值范围很大？为什么对于不同的训练 FLOPs，你会得到很大范围的最优学习率？是 y 轴那个问题吗？是的，我认为原因是模型大小的变化等因素。

---

So 2024 was back in the era where I think every open model builder was replicating the entire scaling law stack. And so DeepSeek also complements the learning rate analysis with basically a Chinchilla replication. And to do that, they're also going to do the same thing as MiniCPM. They're going to follow the WSD-style learning rate. They have a weird little variation where they do two decay phases instead of one. I am not really sure why this is. It hasn't really been a thing that has taken off afterwards, but it is a thing that they do. Regardless, the whole point here is to say, WSD is an effective approach. And you can use that to replicate Chinchilla.

2024 年处在我认为每个开放模型构建者都在复现整个缩放定律栈的时代。所以 DeepSeek 也通过基本的 Chinchilla 复现来补充学习率分析。为此，他们做了与 MiniCPM 相同的事情：采用 WSD 风格的学习率。他们有一个奇怪的小变体：做两个衰减阶段而不是一个。我不太确定这是为什么，这并没有在后来流行起来，但他们的确这么做了。不管怎样，核心点是：WSD 是一种有效的方法，你可以用它来复现 Chinchilla。

---

And DeepSeek has much nicer scaling curves than MiniCPM because of their choice to go IsoFLOPs. So they get these very nice, clean sweeps across the fixed flops ranges. And then they also get fairly nice and clean Chinchilla-style trade-offs as before. So this allows them to essentially replicate the Chinchilla results and get a similar kind of data model scaling law. Really, the point that I'm showing with this is just to say, look, the Chinchilla laws have been replicated by other people at large-ish compute ranges. So that analysis is generally sound.

而 DeepSeek 的缩放曲线比 MiniCPM 漂亮得多，因为他们选择了 IsoFLOPs 方法。所以他们在固定的 FLOPs 范围内得到了非常漂亮干净的扫描结果，然后也得到了相当漂亮干净的 Chinchilla 式权衡。这使他们能够基本上复现 Chinchilla 结果，并获得类似的数据-模型缩放定律。我展示这些的真正目的是说：你看，Chinchilla 定律已经被其他人在较大的计算范围内复现了。所以那个分析总体上是可靠的。

---

Finally, I think, this is the-- I'm a little bit sad that these kinds of plots are now somewhat rare in open-source release papers, but this is really the final punchline of a lot of scaling law work. You train a bunch of small, curated models at smaller compute ranges, and then you draw out the power law. And then in the end, you get something pretty close to reality if you scale out enough. So the two stars are the models that they actually trained. The gray dots are their scaling law fits. And they're getting pretty good predictions on their star. I mean, it could be better, but it's not bad at all. And so they're able to get some pretty accurate scaling law predictions on real open-source models that they've trained.

最后，这一点——我有点伤感，这类图现在在开源发布论文中有点少见了——但这确实是许多缩放定律工作的最终要点：你在较小的计算范围内训练一堆小的、精心挑选的模型，然后画出幂律曲线，最后如果你扩展到足够大，你会得到非常接近现实的结果。图中的两个星星是他们实际训练的模型，灰色点是他们的缩放定律拟合。他们对自己的模型得到了相当好的预测。我是说，可以更好，但绝不算差。所以他们能够在他们训练的真实开源模型上得到相当准确的缩放定律预测。

---

OK, I'm actually I'll stop here. If people have questions about the DeepSeek stuff, feel free to ask them. I think my one-line summary here is to say, this is the other approach to dealing with the sensitive hyperparameters. You can either attempt to stabilize them, or you can attempt to just scaling law fit them and then just go with the scaling law. And DeepSeek represents the more fit the scaling law approach to this problem. Good, OK.

好，我在这里停一下。如果大家对 DeepSeek 的内容有问题，请随时提问。我认为我的单行总结是：这是处理敏感超参数的另一种方法。你可以尝试稳定它们，或者你可以尝试直接用缩放定律拟合它们然后跟着缩放定律走。DeepSeek 代表了更偏向拟合缩放定律的方法。

---

## Recent Scaling Law Recipes / 近期缩放配方

So there are other models, more recent ones that have nice scaling laws that they talk about. As I said before, though, I think a lot of this work is now-- what's the-- it's all known to everybody. And so no one is really putting a lot of this stuff into big sections into the paper. So if you look at Qwen 2.5, they say something like, OK, well, we need to tune some optimal hyperparameters, like batch sizes and learning rates. So we do a bunch of scaling experiments to figure out what the optimum are. And then we have a scaling law, and we predict the optimum. And then we're able to do that even for MOEs. So this is basically the same thing as the DeepSeek analysis that they're talking about in Qwen 2.5. Same thing with Qwen 3. By the time it's Qwen 3, they say, all right, we've already figured out what to do in Qwen 2.5. We're just doing exactly the same thing. So this has become part of a very standard recipe that you use in order to nail down the optimal learning rates and batches.

还有其他模型，更新的那些，它们讨论了不错的缩放定律。不过正如我之前所说，我认为这类工作现在已经——怎么说——所有人都知道了。所以没人再把这些东西写进论文的大章节里了。如果你看 Qwen 2.5，他们说：好的，我们需要调整一些最优超参数，比如批大小和学习率。所以我们做了一系列缩放实验来确定最优值。然后我们有一个缩放定律，预测最优值。甚至对 MoE 我们也能够这样做。所以这基本上就是 DeepSeek 那种分析在 Qwen 2.5 中的翻版。Qwen 3 也一样。到了 Qwen 3，他们说：好了，我们已经在 Qwen 2.5 中搞定了该怎么做，我们完全照做。所以这已经成为非常标准的缩放配方(scaling recipe)的一部分，用于锁定最优学习率和批大小。

---

Kimi K2 is probably the newest paper that I'll talk about of the series. At this point, I'm just going to quickly go through several papers maybe to give you an overview of what people are doing in terms of scaling work in the open-source model releases. So Kimi K2 and a few others have focused on essentially MoE scaling laws. So it's 2026. Most people know how to do a Chinchilla scaling law or even a learning rate scaling law. What things are new? Well, a lot of these companies are now switching to MoEs, fully switching to MoEs. And if you're doing that, you really want to know, am I training the right amount of active parameters? And so they're doing things, like, OK, we're going to vary the flops and look at my losses. And I'm going to do so for different levels of sparsity so that I can figure out how much sparsity helps or hurts my losses. And their conclusion, of course, is if you look at the different sparsity levels, the more sparse your network, the better your validation loss, given a FLOP-- unsurprising. But now the fact that they can quantitatively know what the relationship is between sparsity and loss means that they can make more rational decisions about how much sparsity to put into their model. And they look at this, and they say, OK, what we're going to do is we're going to use sparsity of 48, because at that point we're hitting diminishing returns on our scaling loss. So you can see how this kind of analysis is used to justify different architectural decisions across different open-source releases.

Kimi K2 可能是这个系列中我要讨论的最新论文了。在这一点上，我快速浏览几篇论文，给大家概述一下在开源模型发布中人们在缩放方面做了什么。Kimi K2 和其他一些模型主要关注 MoE 缩放定律。现在是 2026 年，大多数人知道怎么做 Chinchilla 缩放定律甚至学习率缩放定律。什么才是新的？很多公司现在正在切换到 MoE，完全切换到 MoE。如果你这样做，你真的很想知道：我训练的活动参数(active parameters)数量合适吗？所以他们做的事情是：好的，我们改变 FLOPs，观察损失。针对不同的稀疏度(sparsity)水平这样做，以便弄明白稀疏度对损失的帮助或损害程度。他们的结论当然是——如果你看不同的稀疏度水平，在给定 FLOPs 下，网络越稀疏，验证损失越好——这并不意外。但现在他们能够定量知道稀疏度和损失之间的关系，意味着他们可以做出更理性的决策，决定在模型中放多少稀疏度。他们对此做了分析，然后说：好的，我们要用稀疏度 48，因为到那个点之后，我们的缩放损失会出现收益递减(diminishing returns)。所以你可以看到这种分析如何被用来证明不同开源发布中的不同架构决策。

---

Hunyuan, which is another open-source MoE from a few years ago now, they do a very similar thing. I think every company, once they switch to the MoE, has to do this kind of MoE scaling law to figure out how the number of activated parameters or the amount of sparsity changes training loss. And then they redo a lot of these analyses. So for example, in Hunyuan's case, they end up with a 96 data point per active parameter ratio. In their case, they're fixing the sparsity level. And so that's not a thing that they're searching over.

Hunyuan 是几年前另一个开源 MoE，他们做了非常类似的事情。我认为每家公司一旦切换到 MoE，都必须做这种 MoE 缩放定律来弄清楚活动参数数量或稀疏度如何影响训练损失。然后他们重新做了很多这些分析。例如，在 Hunyuan 的情况下，他们最终得到了每个活动参数 96 个数据点的比例。在他们的案例中，他们固定了稀疏度水平，所以这不是他们搜索的内容。

---

LLaMA 3 also has some nice scaling laws. Unfortunately, they're not particularly useful ones. They do IsoFLOP-style scaling and get slightly different but similar ratios for token-to-model. The most interesting thing that they do in terms of scaling in LLaMA 3 is the plot on the right here, which is, they have the usual scaling law, which is the left panel. That's saying, if I have more compute, then the logprob on the answer for a benchmark decays consistently. And on the right side, they show, OK, well, if you have better log loss, then the downstream accuracy also goes up. So they're basically saying, well, we can just fit a sigmoid on these purple points. And that might give us a sense of how good these different models are. You can see their systematic deviations from the curve. So I don't really know if I would really buy that this curve is like the one truth that's going on. But you can certainly see that it is consistent with a sigmoidal scaling mapping from the loss to the accuracy, which I think is very useful because we've been talking only about log losses. But there is a tight coupling in some cases, or in many cases, between log losses and downstream accuracy.

LLaMA 3 也有一些不错的缩放定律。不幸的是，它们不是特别有用。他们做了 IsoFLOP 风格的缩放，得到了略有不同但相似的 token-to-model 比例。他们在 LLaMA 3 缩放方面做的最有趣的事情是右边的图：左边面板是通常的缩放定律——如果我有更多计算量，基准测试答案的对数概率(logprob)会持续衰减。在右边，他们展示了：如果你有更好的对数损失(log loss)，下游准确率也会提高。所以他们基本上说：我们可以在这紫色点上拟合一个 sigmoid 函数，这可能会告诉我们这些不同模型有多好。你可以看到它们与曲线的系统性偏差。我不确定我是否真的相信这条曲线是唯一的真理，但你确实可以看到它符合从损失到准确率的 sigmoidal 缩放映射，我认为这非常有用，因为我们一直在谈论对数损失，但在某些情况下（或者说许多情况下），对数损失与下游准确率之间存在紧密耦合。

---

And then for one last paper that I want to talk about for scaling, MiniMax-01 from last year had this nice set of scaling experiments where they were doing the exact kind of thing I was saying is a useful affordance of scaling from two lectures ago, and that is architecture variations. And so they wanted to understand, OK, I have lightning attention, which is some kind of a linear attention architecture. I have a softmax version like full attention, and I have a hybrid version that mixes the two. How do these things scale? Is it the case that if I scale up, one of them will get much worse than the other? And so you can see, they're replicating essentially the Kaplan plots of, as I increase FLOPs, how do the learning curves change? And is the number of parameters that I need different for different levels of compute for these different architectures? And the answer is, for the most part, no, that hybrid and lightning and softmax are all comparable for the most part. And they require similar model sizes. And this set of plots is used to justify their use of the hybrid architecture in the actual deployed system. So this is exactly the kind of decision making that you would do based upon a scaling law.

最后我要讨论的一篇缩放论文是去年的 MiniMax-01。它有一组很好的缩放实验，做的正是我两讲前所说的缩放的一个有用特性：架构变体(architecture variations)。他们想了解：我有闪电注意力(lightning attention)——某种线性注意力架构；我有 softmax 版本（全注意力）；我有混合两者的混合版本。这些东西如何缩放？是否会出现当我扩展规模时其中一个变得比另一个差很多的情况？所以你可以看到，他们基本上复现了 Kaplan 图：随着 FLOPs 的增加，学习曲线如何变化？对于不同的计算量水平，这些不同架构需要的参数数量是否不同？答案基本上是：不，混合版本、闪电注意力和 softmax 在大部分情况下是可比的，它们需要相似的模型大小。这组图被用来证明他们在实际部署系统中使用混合架构的合理性。这正是你会基于缩放定律做的那种决策。

---

So that's basically what I wanted to cover for the recent scaling law recipes from the various companies. So the two things, as I said before, for the DeepSeek recipe. Really, the key thing is the scaling analysis on the batch and learning rate. This is the scaling-based approach. And MiniCPM follows a more of a muP-style approach to try to get invariances. And then we see some trends. We see that Kimi and Qwen and others, or in Hunyuan, are doing these MoE scaling experiments as they switch to MoEs. We see some architecture work by MiniMax, and we also see some IsoFLOPs analysis being replicated by several others.

这基本上就是我想涵盖的来自各家公司的近期缩放配方。所以两件事，正如我之前所说：对于 DeepSeek 配方，关键点是对批大小和学习率的缩放分析，这是基于缩放的(scaling-based approach)。而 MiniCPM 遵循更偏向 muP 风格的方法来获得不变性(invariance)。然后我们看到一些趋势：Kimi、Qwen 和 Hunyuan 等在切换到 MoE 时做 MoE 缩放实验。我们看到 MiniMax 的架构工作，也看到 IsoFLOPs 分析被其他几个团队复现。

---

And to return to our previous point, the point here is, I think a lot of companies are now less detailed because the core scaling machinery, like doing Chinchilla or doing learning rate scaling, is now fairly well understood by everybody. So there's no necessarily extra value in showing those experiments for some of these releases. Or at least that's my guess for why we have much fewer of these kinds of experiments in the release.

回到我们之前的观点：我认为现在很多公司不那么详细了，因为核心缩放机制——比如做 Chinchilla 或做学习率缩放——现在已经为所有人所充分理解。所以在某些发布中展示这些实验不一定有额外价值。或者至少这是我对于为什么发布中这类实验少了很多的猜测。

---

## Q&A: Post-Training and Scaling / 问答：后训练与缩放

OK, I'll take one minute and then pause and let you digest and ask a question or two, in case you have questions for this part. OK, so all these cover the proofing stage. So my question is, what changes and what do not change when no post training is standardized process for model development? Yeah, so the question was about, what changes about this when you do-- or when you think about post training, I guess, broadly? I think that's still a big, open question. There's no great way to do fully integrated scaling with post-training accounted for, because post-training can sometimes really change the nature of what pre-training you should do. The closest things that I can think of to thinking about post-training is there's been some work on understanding coverage or diversity notions in pre-training that would help predict what happens in post-training, but it's still pretty nascent work. I don't think there's any good answer to the question of, what do we do about synergy with post-training?

好，我花一分钟暂停一下，让大家消化并提一两个问题。所以我的问题是：当后训练(post-training)没有成为模型开发的标准化流程时，什么变了，什么没变？是的，问题是关于——当你考虑后训练时，这会改变什么？我认为这仍然是一个大的、开放的问题。目前没有很好的方法来做完全集成的、考虑后训练的缩放，因为后训练有时会真正改变你应该做什么预训练的性质。我能想到的最接近的关于后训练的思考是：有一些工作试图理解预训练中的覆盖度(coverage)或多样性(diversity)概念，以帮助预测后训练会发生什么，但这仍然是相当初步的工作。我认为对于"如何处理与后训练的协同效应"这个问题，目前还没有很好的答案。

---

## Scaling Laws for Learning Rates, Batch Sizes, and Optimizers / 学习率、批大小和优化器的缩放定律

Cool. OK, so now we're going to talk about the other piece. So I think the two remaining parts of this lecture map on cleanly to the two examples. So I'm going to talk about one approach, one set of approaches, which is about scaling laws for learning rates, batch sizes, and optimizers. That corresponds to the DeepSeek approach to the world. And then I'm going to talk about the muP stuff. That's the MiniCPM approach to the world. Can we just reparameterize everything to make it so that we don't have to worry about scale? So we're going to now talk about the DeepSeek approach. How do we scale learning rate properly? And so there's going to be a hyperparameter part and an optimizer choice part. And I'm going to draw quite a bit from this pretty recent preprint from the StepFun folks. I don't think there's a great, really, truly reliable, robust study on hyperparameters, especially learning rates. But this is probably getting somewhat close. The StepFun folks train credible large models and release them. And they burned a ton of compute in grid searching the space of hyperparameters in this scaling law study. So I'll go through this and show you some intriguing empirical phenomena about how learning rates, batch size, and all of those affect downstream losses.

好，现在我们来讨论另一部分。我认为本讲剩下的两部分完美对应两个例子。我将讨论一种方法（一组方法），即关于学习率、批大小和优化器的缩放定律——这对应于 DeepSeek 的路线。然后我将讨论 muP 的内容——这对应于 MiniCPM 的路线：我们能否重新参数化(reparameterize)一切，从而使我们不必担心规模？现在我们讨论 DeepSeek 的方法：如何正确地缩放学习率？这会包括超参数部分和优化器选择部分。我会大量借鉴 StepFun 人员最近的预印本。我认为目前还没有真正可靠、稳健的超参数研究（尤其是学习率），但这篇可能已经比较接近了。StepFun 的人员训练了可信的大模型并发布它们，他们在这项缩放定律研究中燃烧了大量的计算资源来做超参数空间的网格搜索。所以我要讲解这些，并向你们展示一些有趣的实证现象，关于学习率、批大小等因素如何影响下游损失。

---

So lots of people have talked about lots of different ways of scaling, learning rate and batch sizes as roughly as a function of compute. And the StepFun survey-- not survey paper, the hyperparameter tuning paper has this very nice table that captures a lot of this. And I'll point out a couple of different things. Some of this we already know. So the very top row, this OpenAI scaling law-- this is from Kaplan. If you look at the batch size over there, notice how it says 2eE18, capital L to the exponent. That's critical batch sizes right. It's basically saying, you should scale your batch size as a function of your terminal loss. Great. DeepSeek we just saw. This is the compute-based scaling loss for both learning rate and batch size. And there's been a couple of other folks that have proposed various kinds of scaling, including MiniCPM, which we talked about as well.

很多人讨论过许多不同的缩放学习率和批大小的方法，大致作为计算量的函数。StepFun 的这篇不是综述论文，而是超参数调优论文，它有一个很漂亮的表格，捕捉了其中的很多内容。我会指出几件事。其中一些我们已经知道了：最上面一行是 OpenAI 缩放定律（来自 Kaplan）。如果你看那边的批大小，注意它写的是 2eE18，大写的 L 作为指数——这就是临界批大小。它基本上是在说：你应该根据你的最终损失来缩放批大小。好。DeepSeek 我们刚刚看到，这是基于计算量的学习率和批大小的缩放损失。还有其他一些人提出了各种缩放方案，包括我们讨论过的 MiniCPM。

---

Another important thing that I want to point out is that these formulas for learning rate and batch sizes, they don't even have the same inputs. People don't even seem to agree, what are the variables that should affect these learning rates? Like, the OpenAI one is terminal loss. Whereas, the StepFun folks, they claim that the right batch size scaling is a function of the data. So there's a lot of different disagreements about the nature of scaling for hyperparameters. And I think one thing I'll say as I go through this is not to take even this last row as gospel. A lot of these things are pretty brittle in many ways, but the experiments and the phenomena are things that you can learn well from.

我要指出的另一个重要事情是，这些学习率和批大小的公式甚至没有相同的输入。人们似乎甚至没有一致认为哪些变量应该影响这些学习率。OpenAI 用的是最终损失，而 StepFun 的人声称正确的批大小缩放是数据的函数。所以关于超参数缩放的性质存在很多不同的分歧。我想说的一点是，在讲解过程中，即使是最后一行也不要当作金科玉律。这些东西在很多方面都相当脆弱(brittle)，但实验和现象是你可以很好学习的东西。

---

So I'll do that. So the design of this paper is very similar to the DeepSeek one. They're just going to train a ton of models to grid out both the learning rate space and the batch size space and do them across a range of models and range of data set sizes. And by doing so, they hope to essentially saturate the hyperparameter space for a set of small models and then nail down what the optimum is. And much like in the DeepSeek design, they're going to be-- after they grid up the space-- in this case, they have a contour plot. But the underlying objects are just, they run a bunch of models. They aim to try to minimize the losses. And the contour plots are quite nice. I feel like they give a good visualization. They ran a pretty high resolution grid. And thanks to that, one of the things that we can see is that they can actually plot out a fairly high-resolution contour of what the hyperparameter space looks like. In this case, this is a slice at 1b parameters and 100b tokens, I believe. And you can see on the right side, that surface is the hyperparameter landscape. As a function of the batch size, which is one axis, and learning rate, which is the other axis, how does the loss change if you fix the total amount of data in the model?

所以我会做这个。这篇论文的设计与 DeepSeek 非常相似。他们训练大量的模型来网格化学习率空间和批大小空间，跨越一系列模型和数据集大小。通过这样做，他们希望基本上饱和一组小模型的超参数空间，然后锁定最优值。和 DeepSeek 的设计非常像——在他们网格化空间后——这里他们有一个等高线图(contour plot)。但底层对象就是他们运行了一堆模型，旨在最小化损失。等高线图相当漂亮，我觉得它们提供了很好的可视化。他们运行了一个相当高分辨率的网格。多亏了这一点，我们可以看到他们实际上可以绘制出超参数空间的相当高分辨率的等高线。在这种情况下，这是一个在 10 亿参数和 1000 亿 token 处的切片。你可以在右侧看到，那个表面就是超参数景观(hyperparameter landscape)。以批大小（一个轴）和学习率（另一个轴）为变量，当你固定模型中的总数据量时，损失如何变化？

---

Now, we see that each slice, if you fix a batch size or you fix a learning rate-- each slice is kind of nice and convex. And it's almost even smooth. And this is quite nice because it means that you can search for the optimal hyperparameter fairly nicely, and you can be confident that the minima is not too far off. This was very jaggedy. You might have some very serious doubts about whether this kind of program of gridding the space is even viable. Also, this should maybe give you some nice intuition about the smoothness of the hyperparameter space in general.

现在，我们看到每个切片——如果你固定批大小或固定学习率——每个切片都相当不错的凸(convex)形，甚至几乎是平滑的。这非常好，因为这意味着你可以相当好地搜索最优超参数，并且可以确信最小值不会太远。如果这是一个非常锯齿状的表面，你可能会对这种网格化空间的方案是否可行产生严重怀疑。这也应该给你一些关于超参数空间总体平滑度的好直觉。

---

And I think there's actually one really interesting general scaling trend. And looking at other related papers to this topic, I think, I don't know if I've seen any contradicting evidence to this observation. So I think the one thing that seems very interesting and one of the key takeaways of this work is, essentially, if you're looking at the optimal batch size, the only thing that seems to depend on is the total amount of data that you're training on. So this right-hand plot is the one to look at. So x-axis here is the amount of data that you're training on. The different colored dots-- those are different models. Notice how the different colored dots seem to follow roughly the same trend line here, fairly predictable one. And this is in log-log scale, so you should expect some of a power law that's a function of D.

而且我认为实际上有一个非常有趣的通用缩放趋势。看看其他相关的论文，我不知道我是否看到过任何与这一观察相矛盾的证据。所以我认为非常有趣的一点，也是这项工作的关键结论之一：如果你看最优批大小，唯一似乎依赖于的因素是你训练的总数据量。所以右边这张图是值得看的。x 轴是训练数据量。不同颜色的点代表不同的模型。注意不同颜色的点似乎大致遵循相同的趋势线，相当可预测。这是在对数-对数坐标系中，所以你应该期望某种关于 D 的幂律。

---

On the left panel, we have the dependence of learning rate. And we see that this is a very different behavior. So if you go from blue all the way to this pink color right, bigger models have smaller optimal learning rate. And larger amounts of data have higher optimal learning rate, which is counterintuitive, actually. And so this might be a little fragile. There are other kinds of papers that argue that the dependence on D should be reversed. But the trends here are at least on this experiment, are quite clear.

在左边面板，我们有学习率的依赖性。我们看到这是非常不同的行为。从蓝色一直到粉红色，更大的模型有更小的最优学习率。更大的数据量有更高的最优学习率——这实际上是反直觉的。所以这可能有点脆弱。有其他论文认为对 D 的依赖应该是相反的。但这里的趋势至少在这个实验中是相当清楚的。

---

And one final thing that I want to point out is, the learning rates are actually pretty robust. And I think this is backed up by a lot of experiences and experiments that people have. I think people have a sense of-- actually as a poll, do people know what a good hyperparameter is? If you were told to train a language model tomorrow, would it be 1e negative 3, 1e negative 4? I feel like we roughly have a sense of, actually, this range of hyperparameters for learning rates is generally a good starting point. And that is generally true.

最后我想指出的一点是，学习率实际上相当稳健。我认为这得到了许多人经验和实验的支持。我认为人们有一种感觉——实际上作为一次投票：如果告诉你明天训练一个语言模型，学习率会是 1e-3 还是 1e-4？我觉得我们大致有感觉：实际上，这个范围的学习率超参数通常是好的起点。这通常是正确的。

---

So the scaling laws that they got actually transfer over to, for example, MoEs to a certain extent. The yellow stars, which might be a little harder to see, are the predictions from their scaling laws. The red x's are the optima that are derived directly on the MoEs. And so you switch to an MoE. You don't end up with a very different scaling law, as long as you're roughly controlling for active parameters. The one thing that does seem a little bit more potentially dicey is, as you shift the training data, the optimal learning rates and the optimal batch sizes do shift a little bit, which means that all of these phenomena are likely contingent. The specific numbers that are in these scaling laws and so on are potentially contingent to the data that you train on more so than others.

所以他们得到的缩放定律实际上在一定程度上可以迁移，例如到 MoE。黄色的星星（可能有点难看到）是来自他们缩放定律的预测。红色的 x 是直接在 MoE 上推导出的最优值。所以你切换到 MoE，你不会得到一个非常不同的缩放定律，只要你大致控制活动参数。一个看起来可能更棘手的事情是：当你改变训练数据时，最优学习率和最优批大小确实会有些变化，这意味着所有这些现象很可能是依情况而定的(contingent)。这些缩放定律中的具体数字等可能更依赖于你所训练的数据。

---

And so I want to flash this back up before I move on. So you end up with some of simple scaling law at the end, which says, OK, batch size maybe should be roughly square root of the number of data times some constant. Your learning rate should scale upwards with batch size or upwards with data but downwards with the model size. And that's a surprising effect but not maybe crazy, because these experiments often, in many cases, are assuming Chinchilla-like scaling, in which case, those two would cancel. And as you increase compute, your learning rate should go down. And hopefully, that Chinchilla comment was clear. What I mean is when you're scaling by Chinchilla, N and D are both driven by compute. And as compute goes up, you expect your learning rate to go down. And so you will end up with something like the DeepSeek Law, where the learning rate decreases with compute, and the batch size increases with compute, albeit with different exponents than the DeepSeek Law.

所以我想在继续之前把这一点再提出来。你最终会得到一个简单的缩放定律：批大小大致应该是数据量的平方根乘以某个常数。你的学习率应该随批大小或数据量向上缩放，但随模型大小向下缩放。这是一个令人惊讶的效果，但可能并不疯狂，因为这些实验在很多情况下都假设了 Chinchilla 式缩放，在这种情况下，两者会抵消。随着计算量的增加，你的学习率应该下降。希望关于 Chinchilla 这点是清楚的。我的意思是，当你按 Chinchilla 方式缩放时，N（模型大小）和 D（数据量）都由计算量驱动。随着计算量增加，你期望学习率下降。所以你最终会得到类似 DeepSeek 定律的东西：学习率随计算量递减，批大小随计算量递增，尽管指数与 DeepSeek 定律不同。

---

Cool. OK, so in some sense, this is the newest and most large-scale version of the DeepSeek analysis. And this is one way that, if you were doing the scaling-law-style approach, you would approach this problem of fitting a learning rate. So that's the hyperparameter story. If someone has questions, feel free to stop me. And then next, right after, I'm going to move on to talking about optimizers. I think this is one thing that didn't have time to talk about in the architectures lecture. That was already a pretty packed lecture. But I think it would be a disservice to if I don't talk about optimizers. And optimizers are scale dependent, so this is a good place to put them and talk about some of the latest and greatest developments in optimizers and their relationship with scale.

好的，所以在某种意义上，这是最新也是最大规模的 DeepSeek 分析版本。如果你采用缩放定律风格的方法，这就是你处理拟合学习率问题的一种方式。这就是超参数的故事。如果有人有问题，请随时打断我。接下来我要继续讨论优化器。我认为这是架构讲座中没有时间讲的内容——那个讲座已经相当满了。但如果我不讨论优化器，那将是一个失职。优化器是依赖规模的，所以这是一个很好的地方来讨论它们，以及优化器的最新发展及其与规模的关系。

---

Oh, yeah? So I guess I'm trying to figure out how to interpret this. Does that mean we should just take the scaling laws that we have and then apply them, rather than running our own grid search? Yeah, I mean, I think it depends what regime you're in. The question is like-- oh, sorry, I have to repeat it for the online folks-- is should we just take the scaling law and run them, or should we just do our own grid search? It does depend on the amount of compute budget that you have and how much you need to nail it. I do think, for example, maybe the StepFun law-- if you're in the right compute regime, like close to where they were running the grid, these are probably really good defaults. I would bet on these over something I pull out of my hat. That said, if you were doing your own big pre-training run, you're probably going to have minor differences. Someone might say, I really believe we should have a big weight decay. My architecture has a big weight decay. We don't know necessarily that those things are going to scale the same. And so you might want to actually redo a lot of this. And this is why I think a lot of the reports I showed you were redoing Chinchilla, redoing all these things, because there's enough minor differences that people want to check and make sure that they're roughly first-order correct with these results.

哦，是吗？我在试图理解如何解释这个。这是否意味着我们应该直接拿现有的缩放定律应用，而不是自己做网格搜索？是的，我认为这取决于你所在的领域。问题——哦抱歉，我需要为在线的人重复一遍——我们应该直接拿来缩放定律运行，还是应该自己做网格搜索？这确实取决于你拥有的计算预算以及你需要的精确程度。我确实认为，例如 StepFun 定律——如果你在正确的计算范围内，比如接近他们运行网格的地方，这些可能是非常好的默认值。我宁愿赌这些也不赌我凭空想出来的东西。话虽如此，如果你在做自己的大型预训练运行，你很可能会遇到微小差异。有人可能会说：我真的相信我们应该有大的权重衰减(weight decay)，我的架构有大的权重衰减。我们不一定会知道这些东西是否会以同样的方式缩放。所以你实际上可能想重新做很多这样的工作。这就是为什么我展示的很多报告都在重新做 Chinchilla、重新做所有这些事情——因为存在足够多的微小差异，人们想要检查并确保这些结果在一阶近似上是正确的。

---

I think this will come up again in this next optimizer part. And I was talking about this with [MUTED] earlier, which is, scaling laws have this very scientific feel to them. It's like, yes, fit these lines and extrapolate them. But ultimately, a big part of scaling laws is still vibes. It's like, do I really believe that the experiment setting of this StepFun survey is similar enough to mine that they will transfer? We can't possibly right. There are always tiny differences.

我认为这将在接下来的优化器部分再次出现。我早些时候和某人讨论过：缩放定律给人一种非常科学的感觉——是的，拟合这些线然后外推它们。但最终，缩放定律很大程度上仍然是"感觉"(vibes)。就像：我真的相信这个 StepFun 研究的实验设置和我的足够相似以至于它们可以迁移吗？我们不可能完全确定，总是有微小的差异。

---

## Optimizers and Scale / 优化器与规模

Good, OK, so now I get to talk about optimizers. And I think there's been some really exciting developments in LLM optimizers, and maybe even deep learning optimizers in general over the past year or two. And so this is an exciting time to talk about them. And so a story that I want to start with and one that should maybe motivate this subsection is this comparison over here, or maybe we'll start on this left panel. So this is from NanoGPT speedrun, which inspired our assignment 1. And there you have a really teeny, tiny model that you're training on a fairly short amount of time, and you want to get the, I forget, 3 point-some loss as quickly as possible. And many people have been hill climbing on this benchmark. And I think one of the more remarkable things that have happened on the benchmark is as a benchmark called muon in purple over here came and got really significant gains over Adam, which is blue. It's right underneath the green line over there. So you can just look at the green and the purple and that gap. And you say, wow, lots of big gains from just changing the optimizer to this muon thing. And it's not even slower than Adam, much slower than Adam. That's great.

好，现在我可以讨论优化器了。我认为在过去一两年中，LLM 优化器（甚至一般深度学习优化器）有一些令人兴奋的发展。所以现在是讨论它们的好时机。我想从一个故事开始，也许可以激发这一小节——就是这里的比较，或者我们从左边这张图开始。这来自 NanoGPT speedrun，它启发了我们的作业一。你有一个非常非常小的模型，训练时间相当短，你想尽快达到——我忘了——3 点几的损失。很多人一直在攀登这个基准。我认为在这个基准上发生的最引人注目的事情之一是：一种叫做 muon 的优化器（图中紫色）在 Adam（蓝色）上取得了显著的增益。它就在绿线下面。所以你看看绿色和紫色之间的差距，你会说：哇，仅仅把优化器换成 muon 就带来了巨大的收益。而且它并不比 Adam 慢——甚至慢很多？很好。

---

But then there's a question of, well, is this thing actually good at scale? And then you go and run some scaling studies, and maybe they're not quite as good. This is a really tricky and important part of how we do research. We have a small-scale experiment. We have something that's scale-dependent, for sure, like an optimizer. And then we see really big gains in the small scale. What do we do about the large scale? And more than providing a solid, concrete prescription, I want us to maybe almost even provide a story here so that you can get a sense of what we can do and what things we can't necessarily know.

但问题来了：这个东西在大规模上真的好吗？然后你去运行一些缩放研究，也许它们就没那么好了。这是我们做研究中一个非常棘手和重要的部分。我们有一个小规模实验。我们有一个肯定依赖规模的东西（比如优化器）。然后我们在小规模上看到了非常大的收益。大规模怎么办？与其提供一个坚实的、具体的处方，我更想给大家讲一个故事，让你们感受到我们能做什么以及哪些事情不一定知道。

---

So actually, before I move on to the next slide, and this kind of thing happens all the time, where you're like, come up with a great thing small scale. And it just doesn't maybe pan out large scale. So what's the difference? I'm going to spend a few slides talking about Kaiyue and Tengyu and Percy and David's paper on basically doing a large-scale set of experiments on comparing optimizers and trying to do that comparison better. And there's a lot to learn about scaling and other things from that, but also just standard deep learning stuff.

实际上，在我进入下一张幻灯片之前，这种事情经常发生：你在小规模上想出了一个很棒的东西，但到大规模就不一定奏效了。区别是什么？我会花几张幻灯片来讲解 Kaiyue、Tengyu、Percy 和 David 的论文，该论文基本上做了大规模的比较优化器的实验，并试图更好地做这种比较。从中可以学到很多关于缩放的东西，但也包括标准的深度学习内容。

---

There's really basic things. Like, the hyperparameters for different models are different. So if you're scaling things up, maybe they even have different scaling exponents. So you have to tune Adam really well. So if you tune it badly you get this darker, brown line. And you're like, wow, this thing is much worse than all these other algorithms that I have over here on the left. But then you change the learning rate a little bit. And you're like, wow, actually, all my gains went away. Similarly on the right, you can have cases where maybe you've tuned your learning rate well. But now you've got other stuff like weight decay that is not optimally tuned. And so if you use the same weight decay, then you're certainly going to get a much worse result for this green line. If you pick this small weight decay, you'll get a much worse result for this green line than if you pick the optimal weight decay. So there's all sorts of pretty tricky things going on, technically not a scaling thing, but a very important general empirical machine learning thing that I want to point out.

有一些非常基本的东西。比如，不同模型的超参数是不同的。所以如果你扩展规模，它们甚至可能有不同的缩放指数。所以你必须把 Adam 调得非常好。如果你调得不好，你会得到这条深棕色的线，然后你会说：哇，这东西比左边所有这些其他算法差远了。但当你稍微改变学习率后，哦，实际上，我所有的增益都消失了。同样在右边，你可能已经把学习率调好了，但现在你有其他东西比如权重衰减没有最优调优。所以如果你用同样的权重衰减，你肯定会得到这条绿线差得多的结果。如果你选择这个小权重衰减，你会得到比选择最优权重衰减差得多的结果。所以存在各种相当棘手的问题，严格来说不是缩放问题，但我想指出这是一个非常重要的一般性经验机器学习问题。

---

But maybe more relevant to the discussion in this class right now is the scale dependence of these things. And I think this is a good case study and example of how to really think about algorithm development as a function of scale, because to me, there are two variables that are always important when thinking about scale. And this paper exposes, to most extent, both of them. So one axis is compute. And if you're fixing the model size to data ratio, like the two are coupled together, then this is essentially a compute axis on the x-axis here. So whenever you're doing a study essentially scale up the compute and look at the trends as a function of scale. And we see right here that if we look at the relative speedup between Adam, which is at 1.0 by definition, and all these other alternatives, we see that muons are really good at small scale. And that gain diminishes down as we increase in scale. That's not really necessarily the picture that you want to see.

但也许与本次课堂讨论更相关的是这些东西的规模依赖性。我认为这是一个很好的案例研究和例子，教你如何真正思考算法开发作为规模的函数。因为对我来说，在考虑规模时有两个变量总是重要的。这篇论文在很大程度上揭示了这两个变量。一个轴是计算量(compute)。如果你固定模型大小与数据量的比例——两者耦合在一起——那么这里的 x 轴基本上就是计算量轴。所以每当你做一个研究，基本上就是扩大计算量，然后观察趋势随规模的变化。我们在这里看到，如果我们看 Adam（定义为 1.0）和所有其他替代方案之间的相对加速比，muon 在小规模上非常好，但这个增益随着我们增大规模而减小。这并不一定是你想看到的图景。

---

There's another axis that you should always be vigilant of if you're doing algorithm development, and the other one that you should be vigilant of is the Chinchilla ratio. So the Chinchilla ratio can be thought of. It is the ratio between how much data you have and the amount of model you have. And this is a really, really, really important parameter because some algorithms work well in the overparameterized case where you have a way bigger model than you have lots of data. Maybe your algorithm adds some implicit regularization. Or maybe it is data inefficient, but it works well because of compute reasons. So some algorithms might work well at the small Chinchilla ratio case. In contrast, other algorithms might work well in the large Chinchilla ratio case, where you have lots of data per unit parameter because you can pack knowledge more efficiently into the parameters. So this is a big, big big confounder. Even papers that I think have pretty good hygiene in doing scaling experiments on the model size axis often neglect to or just don't have the compute to study the Chinchilla token to parameter ratio. And this turns out to be surprisingly important a lot of time. In this case, it's not. In this case, you see that the optimizer gains are pretty consistent. The ratio is between all the lines are the same at different Chinchilla ratios. But this is not always the case. You always want to be vigilant about both of these scaling factors. That's quite important.

如果你在做算法开发，你应该始终警惕另一个轴，那就是 Chinchilla 比例。Chinchilla 比例可以理解为：你拥有的数据量与模型量之间的比率。这是一个非常非常重要的参数，因为有些算法在过参数化(overparameterized)的情况下工作得很好——即你的模型比数据大得多。也许你的算法增加了一些隐式正则化(implicit regularization)，或者它数据效率低但由于计算原因仍然工作良好。所以有些算法可能在小的 Chinchilla 比例下工作良好，而另一些算法可能在大的 Chinchilla 比例下工作良好——你每单位参数有大量数据，因为你可以更有效地将知识压缩进参数。所以这是一个非常大的混淆因素(confounder)。即使是那些在模型大小轴上的缩放实验做得很好的论文，也经常忽略或者没有计算资源来研究 Chinchilla 的 token 与参数比例。而事实证明这在很多情况下惊人地重要。在这个案例中不是这样——在这个案例中，优化器的增益相当一致，不同 Chinchilla 比例下各条线之间的比率是相同的。但情况并非总是如此。你应该始终警惕这两个缩放因素，这非常重要。

---

And then I'm going to also point out, if you have a new algorithm or a new setting, establishing scaling is quite nontrivial. So I've taken this from one of-- Will Held was working with Marin, which was Percy's open-source language model training project. And there they were basically trying to prove out a particular set of hyperparameters. This is even like a new algorithm. So this is cautious AdamC, which is like an Adam variant, square root, batch size scaling and a bunch of other standard-looking things. And they're doing essentially the same Chinchilla analysis that you've seen all the other papers do. But because this is not necessarily a paper, this is a bunch of people doing experiments, you don't just publish the successful one. They have the niceness of publishing their failed runs. And the example here is that they're doing basically standard Chinchilla stuff, and it's looking great. If you go up to this dashed vertical line at 10 to the 20 something, this is a really beautiful-looking scaling loft here. And then, as you scale up, it's like, well, it's a little bit worse. It's a lot worse. And then, wow, now that run is not so good anymore. So it's totally blown up on you. And the point here is that even good-looking scaling trends for many orders of magnitude can suddenly bite you. It can deviate from linear, and then it can then blow up immediately. And in their case, the fix here is just picking more careful muP-style parameterizations. Optimizer changes. They switch to a different kind of optimizer, and they get nicer scaling across more orders of magnitude. But the point here is to say, when I go back here, and I say, OK, well, you should all do scaling experiments, you should scale all your learning rates and so on, that's not easy. You end up fairly nontrivial fraction of the time with plots that look like this. And it's all horrible, and you're not quite sure what has gone wrong.

我还要指出，如果你有一个新算法或新设置，建立缩放是相当不平凡的。我取自 Will Held 与 Marin（Percy 的开源语言模型训练项目）的合作。他们在那里试图验证一组特定的超参数——这甚至是一个新算法，叫 cautious AdamC，类似于 Adam 变体、平方根批大小缩放和其他一些标准的东西。他们做了和其他所有论文一样的 Chinchilla 分析。但因为这不一定是论文，而是一堆人在做实验，你不只是发布成功的——他们还发布了失败的运行。这里的例子是：他们做标准的 Chinchilla 分析，看起来很棒。如果你向上看到 10 的 20 多次方处的虚线垂直线，那里有一个非常漂亮的缩放曲线。然后，随着你扩大规模，呃，有点糟了，更糟了，然后哇，这次运行不好了。它完全炸了。关键是，即使是许多数量级上看起来很好的缩放趋势也可能突然咬你一口——它可能偏离线性，然后立即爆炸。在他们的案例中，修复方法是选择更小心的 muP 风格的参数化、优化器改动——他们切换到一种不同的优化器，在更多数量级上获得了更好的缩放。但这里的重点是，当我回过头来说"你们都应该做缩放实验，都应该缩放学习率等"时——这并不容易。你会在相当大比例的情况下得到看起来像这样的图，非常可怕，你不确定哪里出了问题。

---

## Muon: A Matrix Optimizer / Muon：矩阵优化器

Good. OK. And then, so the last thing I want to end with is just talking a little bit about muon and the closing of the muon story. So I feel like I have to talk about muon in a little bit more detail than I already have, just because it's beginning to be integrated into a large scale model training runs. That's the inclusion criteria for a lot of new research topics for the class. Has it been in a big training run? And muon now checks that mark. And it's also just an interesting algorithm, so I'll mention it and talk about it for a few minutes and then move on.

好。那么，最后我想结束的是稍微讨论一下 muon 以及 muon 故事的收尾。我觉得我必须比我已经做的更详细地讲一下 muon，因为它开始被集成到大规模模型训练中。这是本课程许多新研究主题的纳入标准：它是否被用于大规模训练运行？muon 现在已经符合这个标准了。它也是一个有趣的算法，所以我会提一下并讲几分钟，然后继续。

---

So in gradient descent, we usually have a fairly simple thing that's happening. Ignore line for the moment, sorry, line 5 for the moment. And then you're going to get roughly a standard momentum-based optimizer. I take a gradient. I add it to B of t. This is my momentum step, so I continue my momentum from before with parameter mu. And then I update my parameters based on this momentum gradient. Very standard momentum gradient stuff. But then I think the really interesting and, to me at least, a bit of an out of the box set of ideas is to say, well, gradients have this property that they treat, all the parameters are the same. But we know that not all the parameters in a language model, or even a deep neural network, are the same. Some parameters are like vector parameters. They belong to the RMS norm. Some parameters are matrix parameters, like for the attention or for MLPs. And matrix parameters are probably different than vector parameters. And so that's the starting point for this idea and I think a really interesting one.

在梯度下降中，我们通常有一个相当简单的事情在发生。暂时忽略第 5 行。然后你会大致得到一个标准的基于动量的优化器：我取一个梯度，加到我 B(t) 上，这是我的动量步，所以我用参数 mu 延续我之前的动量。然后我基于这个动量梯度更新我的参数。非常标准的动量梯度。但接下来我认为真正有趣、至少对我来说有点跳出框框的想法是：梯度有一个性质——它们对所有参数一视同仁。但我们知道，语言模型（甚至深度神经网络）中并非所有参数都是一样的。有些参数是向量参数(vector parameters)（属于 RMS norm），有些参数是矩阵参数(matrix parameters)（比如注意力或 MLP 的）。矩阵参数可能与向量参数不同。所以这是这个想法的起点，我认为非常有趣。

---

And so the one thing that you could do about matrix parameters is you can start to look at their spectra. They are matrices. Matrices have eigenvalues and singular values. And so you can do things to the singular values. And so what you do here in Muon is this fairly simple idea. You compute a gradient. You take a momentum step. And now I take my update B of t. And instead of directly applying it to my parameters in line 6, what I'm going to do is I'm going to do this NewtonSchultz thing, NewtonSchultz 5 to be specific. And what that is it's going to orthogonalize the B of t matrix. And so I've written the operation down there on the bottom. Let's say I take B of t. I write it as singular value decomposition, USV transpose. And then I make all of my singular values 1. So if my singular values are really big, I'll shrink them back to unit. If they're really small, I'll expand them back up to being unit. And then I take UV transpose, and that's my new update that I'm going to apply.

所以对矩阵参数你可以做的一件事是开始看它们的谱(spectra)。它们是矩阵，矩阵有特征值和奇异值。所以你可以对奇异值做一些操作。Muon 做的事就是这个相当简单的想法：你计算梯度，取动量步，然后得到我的更新 B(t)。我不直接把它应用到参数上（第 6 行），而是做这个 NewtonSchultz 操作（具体来说是 NewtonSchultz 5）。它会将 B(t) 矩阵正交化(orthogonalize)。我在底部写下了这个操作。假设我取 B(t)，把它写成奇异值分解(SVD) USV^T，然后我把所有奇异值设为 1。所以如果我的奇异值很大，我会把它们缩小到单位；如果很小，我会把它们放大到单位。然后我取 UV^T，这就是我要应用的新更新。

---

If you want intuition for this, and you already have intuition for something like adagrad or these other, or Adam even. In adagrad or Adam, you're going to divide by the size of the gradient. So every coordinate is roughly going to be the same size. In muon, you are operating in the spectral norm instead. So every kind of direction is going to be unit size. And notice that this only makes sense for a matrix. I can only define this notion of a singular value decomposition for a matrix valued B of t. So the interesting thing about muon is it's a matrix optimizer, so you apply it to these matrix valued parameters. And for the vector-valued ones, you might still use something like AdamW because those don't really have any interaction with the NewtonSchultz term. Also, NewtonSchultz is an approximation to that operation that only uses matrix multiplies. So it's systems efficient and not exactly the orthogonalization.

如果你想要直觉，并且你已经对 adagrad 或 Adam 等有直觉：在 adagrad 或 Adam 中，你除以梯度的大小，所以每个坐标大致相同的大小。在 muon 中，你在谱范数(spectral norm)上操作，所以每个方向都是单位大小。注意，这只有对矩阵才有意义——我只能为矩阵值的 B(t) 定义奇异值分解这个概念。所以 muon 有趣的地方在于它是一个矩阵优化器(matrix optimizer)，所以你把它应用于这些矩阵值的参数。对于向量值的参数，你可能仍然使用像 AdamW 这样的东西，因为那些与 NewtonSchultz 项没有交互。另外，NewtonSchultz 是那个操作的一个近似，只使用矩阵乘法，所以系统效率高，并且不是精确的正交化。

---

But OK, why have I spent all this time talking about muon? Well, first of all, it's very powerful for things like the NanoGPT speedrun. It was discovered for this set of things. And so you might think that it works well. As I said in the previous slide, there have been some scaling studies that have argued that the gain for muon decreases as scale goes up. But then I want to close off this story, which, I think, initially this came out. And I was like, wow, muon is interesting. I wonder if anyone will scale it up. And then [INAUDIBLE] and others scaled up muon. And they said, well, maybe it doesn't work super well. And I thought the story was closed here. I was like, well, maybe this is done. No one will spend the big compute to scale this guy up to the full pre-training size. And then Kimi K2 comes out, and that whole model is trained with muon, fully with muon, with a few bells and whistles to prevent muon from blowing up on you. They found a whole bunch of instability issues. But Kimi K2 is an outstandingly good model. It's a very good model, and the training curves look reasonable. And so really, what this suggests is like, well, muon worked at scale. Is it better than Adam? Kimi K2 certainly doesn't have any ablation, so we don't know at that scale. But it is certainly a valid and workable solution.

但为什么我花了这么多时间讲 muon？首先，它对 NanoGPT speedrun 之类的东西非常强大——它就是为这些东西发现的。所以你可能会认为它效果很好。正如我前一张幻灯片所说，有一些缩放研究认为 muon 的增益随着规模增大而减小。但我想收尾这个故事：最初我心想"哇 muon 很有趣，不知道有没有人会把它扩展到大规模"。然后 [INAUDIBLE] 等人扩展了 muon，他们说"也许它不是特别有效"。我以为故事到这里就结束了——也许这事就完了，没有人会花大计算量把它扩展到完整预训练规模。然后 Kimi K2 出来了，整个模型都是用 muon 训练的，完全用 muon，加上了一些防止 muon 爆炸的额外机制——他们发现了一大堆不稳定性问题。但 Kimi K2 是一个非常出色的模型，训练曲线看起来合理。所以这表明：muon 在大规模上确实有效。它比 Adam 好吗？Kimi K2 当然没有做消融(ablation)，所以我们不知道在那个规模上怎么样。但它肯定是一个有效且可行的解决方案。

---

And so what's the point of this story? It's to say, It's really hard to know whether something works at scale. It's very, very hard. But thus far, a lot of small scale experiments and transferring them up to large scale has been the way by which we do science. And so you still want to respect things like the NanoGPT speedrun. We learn quite a bit from that and get good ideas. And then eventually, they make their way to the big models. We'll see if people continue to do ablations at big scale and really nail down, is muon better than AdamW at scale and so on? Those are interesting questions to which we don't yet have the answers.

那么这个故事的要点是什么？就是说，要知道某个东西在大规模上是否有效真的很难——非常非常难。但到目前为止，许多小规模实验并将它们迁移到大规模一直是我们做科学的方式。所以你仍然应该尊重像 NanoGPT speedrun 这样的东西——我们从中学习了很多，得到了好的想法。然后最终，它们进入了大规模模型。我们会看看人们是否继续在大规模上做消融，真正确定 muon 是否比 AdamW 在大规模上更好等等。这些都是有趣的问题，我们还没有答案。

---

## Q&A: Optimizers / 问答：优化器

OK, I'll pause here for a moment. This is the end of my optimizer section. I want to make sure everyone's good, also especially because I was talking about muon. And that's a whole new can of worms that I haven't talked about much before.

好，我在这里停一下。这是我的优化器部分的结束。我想确保大家都好，尤其因为我讲了 muon——这是一个我之前没怎么讨论过的全新的话题。

---

Yeah? [INAUDIBLE] letter [INAUDIBLE] faster on GPU? OK, [INAUDIBLE]. Great. Yeah, the question was, is SVD fast on GPUs? SVD is not fast on GPUs, but they're not doing SVD. What they're doing is NewtonSchultz. NewtonSchultz is a matrix multiply only finite iteration algorithm that approximates the process of orthogonalizing a matrix. So there's several clever pieces here. One of them is the idea of treating it as a matrix on its own. And then there's this orthogonalization idea, and then there's the systems piece of doing it with NewtonSchultz. So those are all important, interesting pieces?

是吗？问题是 SVD 在 GPU 上快吗？SVD 在 GPU 上不快，但他们不做 SVD。他们做的是 NewtonSchultz。NewtonSchultz 是一个仅用矩阵乘法的有限迭代算法，近似于正交化矩阵的过程。所以这里有几个巧妙的点：一个是把它当作矩阵本身来处理的 idea，然后是正交化的 idea，然后是使用 NewtonSchultz 做这件事的系统层面部分。这些都是重要且有趣的部分。

---

Yeah, back there? Are hyperparameters for nontrivial [INAUDIBLE] ones? Are the hyperparameters here-- no, they're different, yeah. I think there are several people that have been working on this muon-style line of work. And one of them, I think, like Jeremy Bernstein, I think he's been saying, actually every layer should have its own learning rate. I think the ultimate limit of this is like, you go from-- or even, sorry, every layer should have its own optimizer. The ultimate limit of this is to say, every parameter in a transformer is different. Why not have a different optimizer for each one of them? And so you would have to tune hyperparameters for each one of them as well, which I do not want to do. But that's maybe the future of optimization.

后面有人？超参数不同吗？是的，它们不同。我认为有几个人在做这种 muon 风格的工作。其中一个是 Jeremy Bernstein，他一直在说实际上每层应该有自己的学习率。我认为最终极限是——甚至，抱歉——每层应该有自己的优化器。最终极限是说 Transformer 中的每个参数都是不同的，为什么不为每一个使用不同的优化器？这样你还需要为每一个调优超参数，我不想这样做。但这可能是优化的未来。

---

Yes? What's the validity of like-- like, on the learning rate and batch size, you just consider these two things. And then you pick the best out of those, and then you can use it to tune other things. But do these things interact with each other? Yeah, or maybe the version of the question that I interpreted was, a lot of these people are just tuning learning rate and batch size. And they do this on the grid. But presumably, these things interact with a whole bunch of other hyperparameters. Aren't you worried about that? And I think, in general, yes, you are worried about hyperparameter interactions. But realistically, they grow exponentially. This is not a thing where you can grid out the whole space. And so I think the thing that people often do is they grid the stuff that's most concerning and most sensitive. And learning rates are very important. I think, if you ever tune stuff, learning rates are the most important thing to tune. So they very aggressively go on that. And then stuff like weight decay, they might do a univariate sweep afterwards to be locally optimal with respect to those parameters.

是吗？关于学习率和批大小，你只考虑这两个，然后从中选出最好的，然后用它来调其他东西。但这些会相互交互吗？是的，或者说我理解的问题版本是：很多人只调学习率和批大小，他们做网格搜索。但这些东西与其他一大堆超参数交互，你们不担心吗？我认为一般来说，是的，你担心超参数交互。但现实是它们呈指数增长，你不能网格化整个空间。所以我认为人们常做的是网格化最令人担忧和最敏感的东西。学习率非常重要——如果你调过参数，学习率是最重要的东西要调的。所以他们非常积极地搜索这个。然后像权重衰减这样的东西，他们之后可能会做单变量扫描，以那些参数为局部最优。

---

## Maximal Update Parametrization (μP) / 最大更新参数化(μP)

Good. OK. All right, so the final part of this lecture is I want to talk about muP. muP is a bit of a mysterious object. Even with many papers written about it and, in fact, even many implementations, I don't think all of them even agree on what the underlying math is or what the underlying implementation should be. But there's a core set of ideas that are shared, and it does seem generally effective. And so I'll talk about my interpretation of the whole program, let's call it.

好。本讲的最后一部分我想讲 muP。muP 是一个有点神秘的东西。尽管有很多关于它的论文，甚至有很多实现，但我认为它们之间甚至在底层数学或底层实现上都不完全一致。但有一组核心的共享思想，而且它总体上似乎是有效的。所以我会讲我对整个体系的理解，姑且称之为"纲领"。

---

So the goal hopefully is very clear. And I think this picture is the goal, the picture being, well, if we increase the size of our model, in this case, just width, our optimal learning rate normally shifts. But ideally, we want the optimal learning rate to be the same, no matter what. That is the game that we would like to play. And the knobs that I'm willing to tune to do this is I'm willing to mess with the initializations at a per-layer basis. I'm willing to mess with the learning rates on a per-parameter basis as well. And then I'm sometimes willing to scale up or down things like residual connections based on the size of my model. So that's the game that I'd like to play.

目标希望能非常清楚。我认为这张图就是目标：如果我们增加模型大小（这里只是宽度），我们的最优学习率通常会移动。但理想情况下，我们希望最优学习率保持不变——无论模型大小如何。这就是我们想要做的游戏。我愿意为此调节的旋钮是：我可以在每层基础上调整初始化，也可以在每参数基础上调整学习率。而且我有时愿意根据模型大小缩放残差连接之类的东西。这就是我想要做的游戏。

---

And how well does it work in practice? There's been several papers that have studied these fairly extensively. Cerebras which is really a chip company, also has a language model training arm run by Hestnes of the scaling law paper fame. And I feel like they do very interesting things because they now are writing lots of papers about muP scaling of language models, and they have Cerebras GPT from a couple of years ago, where they were training the 0.1 to 13b models using the usual Chinchilla recipe, but also including a muP variant, which they use to try to tune the hyperparameters more effectively. And I think one of the nice things about this is they find that if they use the muP parameterization, then their scaling law fits are generally more stable. Their projected muP trends are almost right on the money for their actual models. Whereas, I think their non-muP models fluctuated much more wildly in terms of the loss predictions that they had. And so their claim was, OK. MuP is maybe a really good idea. So this is validated at scale.

它在实践中效果如何？有几篇论文相当广泛地研究了这些。Cerebras 实际上是一家芯片公司，但它也有一个由缩放定律论文闻名的 Hestnes 领导的语言模型训练部门。我觉得他们做的事情非常有趣，因为他们现在写了很多关于语言模型的 muP 缩放的论文，他们几年前有 Cerebras GPT，使用通常的 Chinchilla 配方训练 0.1B 到 13B 的模型，但也包括一个 muP 变体，用来更有效地调优超参数。我认为其中一个好处是他们发现如果使用 muP 参数化，他们的缩放定律拟合通常会更加稳定。他们预测的 muP 趋势几乎与实际模型完全吻合。而非 muP 模型的损失预测波动要剧烈得多。所以他们的结论是：OK，muP 可能是一个非常好的 idea。所以这在大规模上得到了验证。

---

You saw MiniCPM on others. Many people have trained models with muP variants. So I could also talk a lot about training or examples of models trained with muP. But I think maybe the more interesting thing for me to do right now is actually to talk about the conceptual foundations and the math for muP. And if you're interested in this, and you want to read a somewhat accessible paper, I would recommend this one. This is the paper that I think, for me, was the clearest. There are several papers. Greg Yang, who started this research program, has a series of papers I'll call tensor programs. I find them somewhat inscrutable. Jeremy Bernstein, who was also working on the muon stuff, has written this nice-- not recap paper, like a review paper, putting it into a different framework, which I think is very accessible. And there are several others by physicists that are also interesting in terms of explaining what muP is. The Cerebras people actually do a bit of that as well.

你看到 MiniCPM 和其他的。很多人用 muP 变体训练了模型。所以我也能讲很多关于 muP 训练的模型或例子。但我现在觉得更有趣的是讲 muP 的概念基础和数学。如果你对此感兴趣，想读一篇比较容易上手的论文，我推荐这一篇。这是我认为最清晰的一篇。有几篇论文：Greg Yang 开始了这个研究项目，他有一系列我称之为 Tensor Programs 的论文，我觉得有点费解。Jeremy Bernstein（也在做 muon 相关工作）写了一篇不错的——不是总结论文，而是一篇综述论文，把它放在一个不同的框架中，我认为非常易于理解。还有几篇物理学家写的论文在解释 muP 方面也很有趣。Cerebras 的人也做了一些这方面的工作。

---

But anyway, returning to this paper, the core idea of muP is based off of two kind of assertions. And this is a very physicist way of thinking about this. So if I make my network big-- let's say I'm only changing the width for now. I'm making the width of my network big. I'm going to assert two invariants that should hold as I do the scaling limit. First of all, the activations at initialization-- so if I initialize my model, and I put in some random data, the activations should remain the same size roughly as a function of the network. So if they blow up with the network size, or they shrink to 0 with the network size, I have chosen a wrong parameterization. And that makes sense. My activation should be roughly the same scale, regardless of the size of my network. Now, after one gradient step, the change in my activation should be O of 1. So this is what people call feature learning. So feature learning means if I take a gradient step, things in my network change a significant amount and that this amount should be a fixed function of the width of the network. In case some of you are theorists, you might be familiar with neural tangent kernels. Neural tangent kernels would have a very different behavior. Those would be the kinds of things where the change in activations actually vanish as a function of the network width. And you don't want that, because you do want the network to change and learn features and do things even in the limit of your big neural networks. So these two are the invariants. They make sense. They're basically saying, activations and the change in the activations should remain roughly similar as a function of the width of the network.

回到这篇论文，muP 的核心思想基于两种断言。这是一种非常物理学家的思考方式。所以如果我让我的网络变大——假设我现在只改变宽度——我要断言两个在缩放极限下应该保持不变的不变量(invariant)。首先，初始化时的激活值(activations at initialization)：如果我初始化模型，输入一些随机数据，激活值应该大致保持相同的大小（作为网络宽度的函数）。所以如果它们随网络大小爆炸或缩到 0，说明我选择了错误的参数化。这很合理：无论网络大小如何，我的激活值应该大致相同。其次，在一个梯度步之后，我的激活值的变化应该是 O(1)。这就是人们所说的特征学习(feature learning)。特征学习意味着如果我走一个梯度步，网络中的事物会发生显著变化，这个变化量应该是网络宽度的一个固定函数。如果你们中有人是理论派，可能熟悉神经正切核(neural tangent kernels, NTK)。NTK 会有非常不同的行为——激活值的变化实际上会随着网络宽度消失。你不希望这样，因为你确实希望网络在即使是大神经网络的极限下也能改变、学习特征、做事情。所以这两个是不变量。它们说得通：它们基本上是说，激活值和激活值的变化应该大致保持相似（作为网络宽度的函数）。

---

And then note that I'm going to sometimes go back and forth between individual activations, which is this. And then the norm, which-- if each activation is roughly O of 1, the norm of the whole vector of activation should be square root of the number of hidden units in that layer. OK, so that's the main thing.

然后注意我有时候会在单个激活值（这是我们说的）和范数(norm)之间切换——如果每个激活值大致是 O(1)，那么整个激活向量的范数应该是该层隐藏单元数量的平方根。好，这是主要的东西。

---

Now, the thing about muP is it's interesting because it starts with this very simple and palatable set of assumptions. You might all agree that this is a reasonable thing to do. And then we're going to make a number of additional strong assumptions. But then, in the end, we're going to get a very simple set of scaling rules that drop out of this. So remember, what we want to do is we want to make sure that the activation is at init are roughly unit. So what do we do? Well, if we have a simple deep linear network, and we initialize all of our weights as a sigma squared scaled Gaussian, then what is going to be the spectral norm of this matrix? Well, you can write that down. I'm not going to ask you to verify that, but that's standard matrix concentration arguments for the operator norm of a random Gaussian matrix. And then now note that in certain regimes where the fan-out is, I think, not much bigger than the fan-in, you're going to get that the output of the layer is similar to the product of the input of the layer times the operator norm. This is always an upper bound, but this is approximate in certain high-dimensional regimes.

muP 的趣味之处在于它从一组非常简单且易于接受的假设开始——你可能都同意这是一个合理的做法。然后我们将做许多额外的强假设，但最终我们会得到一组非常简单的缩放规则。记住，我们想做的是确保初始化时的激活值大致为单位大小。那么该怎么做？如果我们有一个简单的深度线性网络(deep linear network)，我们将所有权重初始化为 sigma^2 缩放的高斯分布，那么这个矩阵的谱范数(spectral norm)是多少？你可以写出来——我不要求你们验证——但这是随机高斯矩阵算子范数的标准矩阵集中论参数。然后注意，在某些扇出(fan-out)不太大于扇入(fan-in)的情况下，层的输出类似于层的输入乘以算子范数。这总是一个上界，但在某些高维情况下是一个近似。

---

Now, if this is true, now what can we do? Well, we can solve for sigma to try to keep our activations the same across all the layers and across all the width. So imagine that at layer L minus 1, I have square root of L minus 1 activation. And this is, remember, consistent with this notation that, at least for this whole vector, I should have square root of n of L. So this is our base case for induction. And then our inductive case says, well, remember that I have this operator norm at layer L, which is this function of the fan in and the fan out. And so this is going to be equal to this if I pick a particular sigma. So let's say this is the ansatz. I'm going to assume that this is the answer, and then we'll see what happens to the induction. If I pick this as a hypothesis, and I plug this into the sigma, notice that I get that the ratio of the operator norm is this, the ratio of the fan out over the-- sorry, square root of the fan-out over the square root of the fan-in. And then I plug this back in here. And then I'm going to get that the norm of the output is going to be equal to the square root of the number of units in my layer plus some lower-order terms that I'm not going to bother to keep track of.

如果这是真的，我们能做什么？我们可以求解 sigma，试图使我们的激活值在所有层和所有宽度上保持一致。想象在层 L-1，我有 sqrt(n_{L-1}) 的激活范数——记住这与我们的符号一致：对于整个向量，我应该有 sqrt(n_L) 的范数。这是我们的归纳基础(base case)。归纳步骤(indutive case)说：我在层 L 有算子范数，它是扇入和扇出的函数。如果我选择特定的 sigma，这会等于某个值。假设这是一个 ansatz，我假设这是答案，然后我们看归纳的结果。如果我把它作为假设代入 sigma，注意我得到算子范数的比值是 sqrt(扇出)/sqrt(扇入)。然后我把它代回，得到输出范数等于该层单元数的平方根加上一些我懒得追踪的低阶项。

---

So where this sigma came out of-- I mean, this is drawing it out of a hat. But we can verify that if I plug this noise initialization into my formula, then, essentially, at every layer, the size of my activations is roughly equal to the square root of the number of hidden units at that layer. There are some assumptions made here, like this approximate equals. But this is mostly a legitimate set of assumptions. So condition A1 is pretty simple.

所以这个 sigma 是从哪里来的——我是说，这是从帽子里变出来的。但我们可以验证，如果我把这个噪声初始化代入公式，那么在每一层，我的激活值大小大致等于该层隐藏单元数的平方根。这里做出了一些假设（比如约等号），但这在很大程度上是一组合法的假设。所以条件 A1 相当简单。

---

Condition A2 is a little bit hairier, to be honest. So really, we need to deal with the updates now. And I'm only going to consider the case of a single example in a batch for SGD for linear neural networks, so deep linear network. So what is this going to look like? Well, the change in my weights for a particular layer L-- if you think about how this is going to behave, it's going to be a rank 1 update between my gradient for the loss and the activations. This is true just because of the behavior of the backwards. The forwards is a rank 1 multiplication. The backwards is going to be a rank 1 outer product. So now this is the change in the weights. And now what is the change in the activations at that layer? Well, the change in the activations-- I just take h equals W times hl minus 1, and I expand this out. And I expand this out into this formula. This is going to be exactly the change in the activation at layer L. And it's going to have two terms, one that is the direct term from changes in the activation at L minus 1 and the cross term in some sense of what happens because my weights have changed, not just because the activations of the previous layer have changed. So there's two terms to this update.

条件 A2 老实说有点麻烦。我们现在需要处理更新。我只考虑 SGD 中线性神经网络（深度线性网络）的单个样本情况。这会是什么样子？在特定层 L 的权重变化——如果你思考它的行为——它将是损失梯度和激活值之间的秩 1 更新(rank 1 update)。这是由反向传播的行为决定的：前向是秩 1 乘法，反向将是秩 1 外积(outer product)。所以这是权重的变化。那么该层的激活值变化是什么？激活值的变化——我取 h = W * h_{l-1}，展开到这个公式——就是层 L 激活值的变化。它将有两个项：一个来自 L-1 层激活值变化的直接项，另一个是交叉项，反映了因为我的权重变化而不仅仅是前一层激活值变化所导致的情况。所以这个更新有两个项。

---

And so this is the change in the activation at layer L. And now what I'm going to do is I'm going to look through each of these three terms. I want each of these three terms to have the same order of magnitude, and I want that order of magnitude to be square root of n of L. Why is that? Remember that, if I go back two slides, the condition that I want for A2 is that after one gradient step, the change in activation should be O of 1 or omega of 1. And so if I want that to be true, then the norm of that layer should be square root of nL. And so to do that, what I want is for each of these three terms to have that order of magnitude. And if that's true, and there's no cancelations, then this is going to be the right order of magnitude. You can see the sketchy pieces adding up. We're assuming things like no cancelations and so on, but this is giving us some interesting ways of thinking about the magnitude of each of these objects.

所以这是层 L 激活值的变化。现在我要看这三个项中的每一个。我希望每个项都有相同的量级，并且我希望这个量级是 sqrt(n_L)。为什么？回想一下，两页前，我对 A2 的条件是在一个梯度步之后激活值的变化应该是 O(1) 或 Ω(1)。所以如果我希望成立，那么该层范数应该是 sqrt(nL)。为此，我希望这三个项中的每一个都有那个量级。如果这是真的，并且没有抵消(cancelation)，那么这就是正确的量级。你可以看到这些模糊的部分在累积——我们假设了没有抵消等——但这给了我们一些有趣的方式来思考每个对象的量级。

---

So at this point, the right way to think about this is not like, OK, Tatsu is sitting here doing rigorous mathematics. What I am doing here is I'm basically keeping track of all the orders of magnitude of all the terms. And I am saying that, given our assumptions, how big should these roughly be? It's physicists math. No offense to physicists. This was developed by physicists in this way.

在这一点上，正确的思考方式不是"好的，Tatsu 在坐在这里做严谨的数学"。我在做的是追踪所有项的量级，然后在给定假设下说，这些大致应该有多大？这是物理学家式的数学（无意冒犯物理学家）——这本来就是物理学家以这种方式发展的。

---

OK, so now really-- sorry, go back one slide just to make all this clear. So the first term, this comes by almost assumption. It's the inductive assumption. We assume that delta h of l minus 1 has the right order of magnitude. So this comes for free. These other two terms-- these are trickier. We have these terms that multiply the change in my weights in operator norm times square root of L minus 1. And so because these two are the order of magnitude of both of these terms, we know how big this delta L needs to be. We can solve for this because we know that this left-hand side needs to be square root and L. And then we have this term, so we solve for this operator norm. And that's exactly this quantity. So this is going to be the goal for the next slide. I want to try to figure out what kinds of learning rates are going to give me an update that's roughly scaled as the square root of the fan-out over the square root of the fan-in. So that's the goal.

好的，现在——抱歉，后退一张幻灯片让这一切更清楚。第一项几乎是通过假设得到的——它是归纳假设。我们假设 Δh_{l-1} 有正确的量级，所以这不需要额外处理。另外两个项更棘手：我们有这些项，它们将权重的变化（用算子范数）乘以 sqrt(L-1)。因为这两个是整个项的量级，我们知道 ΔW 的算子范数需要多大。我们可以求解这个，因为我们知道左手边需要是 sqrt(n_L)，然后我们有这个项，所以我们解出这个算子范数——就是这个量。所以这将是我们下一张幻灯片的目标：我想弄清楚什么类型的学习率能给我一个大致按 sqrt(扇出)/sqrt(扇入) 缩放的更新。

---

As I said, after I pick a learning rate, this should roughly be true. So how can we do that? Well, we're going to make yet another assumption. And this is probably the least palatable of the assumptions, in my opinion, which is that we're going to assume that the loss update is going to be scaled by unit. In other words, we're going to assume that our model is actually making some appreciable, nontrivial progress as a function of scale and that that's roughly similar. Not quite sure that's palatable to me, but that is yet another assumption. So we throw that down.

正如我说的，在我选择学习率后，这应该大致成立。那我们怎么做？我们要做另一个假设——我认为这可能是最不可接受的假设——我们假设损失更新是单位缩放的单位。换句话说，我们假设我们的模型实际上在随规模做出一些可观的、非平凡的进展，而且这大致相似。我不太确定这是否合理，但这是另一个假设。我们把它放进去。

---

But now the point of this assumption is that if this is true, the rest of the math works out quite cleanly, because the change in the loss is the product of my gradient plus how much my weights changed. This is Taylor approximation. And then because this is rank 1, I can rewrite this thing as a Frobenius norm and as an operator norm. And so this right-hand side now allows us to get what we want. This is O of 1. This term we want to be square root n over square root L minus 1. That's this term on the right here. And then finally, I have this gradient of L term. And this is going to be square root of NL minus 1 over square root nL. And then so now what eta do I need? Well, the eta that I need is going to be solving for this quantity, which is the ratio of these two guys, which is nL over nL minus 1. So we made this one assumption that the left-hand side of this is O of 1. And then we've solved for all the quantities, and we've ended up with a fan-out over fan-in ratio for a learning rate for a layer.

但这个假设的意义在于，如果这是真的，剩下的数学就变得非常干净。因为损失的变化等于我的梯度乘以权重变化量——这是泰勒近似。然后因为这秩 1，我可以把它重写为 Frobenius 范数和算子范数。所以右手边让我们得到我们想要的。这是 O(1)。这一项我们想要是 sqrt(n_L)/sqrt(n_{L-1})，就是右边的这一项。最后，我有这个梯度项，将是 sqrt(n_{L-1})/sqrt(n_L)。那么我需要什么 eta？我需要的 eta 是求解这个量，它是 n_L/n_{L-1} 的比值。所以我们做了一个假设，即左手边是 O(1)，然后我们求解了所有量，最终得到了一个层的学习率的扇出/扇入比。

---

One side note that I'll make is that for Adam, because of the changes in some of this, you're going to get a 1 over nL minus 1 scaling, which I'll mention here. So I've walked through a bunch of hopefully intuitive-looking scaling arguments for various components. But in the end, maybe you are interested in, what does this mean? What does this do for me?

我要说的一个附带说明是，对于 Adam，由于其中一些改变，你会得到 1/n_{L-1} 的缩放。我已经讲解了一系列希望看起来直观的各种组件的缩放论证。但最终，你可能感兴趣的是：这意味着什么？这对我有什么作用？

---

What this means is that we're going to change how we set our initializations and learning rates a little bit. So our initialization is going to look like-- so for muP, the blue box is what we do. Our initialization is going to be 1 over square root nL minus 1 times a component that is 1 over the square root fanout over fanin. So if this is 1, then this is equivalent to the usual initialization. This is the standard parameterization. But if this ratio is not smaller than 1, then you get basically something different. You get something that's closer to the square root fanout over fanin. The learning rate normally you would set to be a constant as a function of your model size, but you would want to set this to the ratio of fanout and fanin. And maybe more interestingly, for Adam, this whole thing is a little bit more different. I'm not going to even touch the derivation for that, where you drop this 1 over nL term, and you get 1 over the fanin as the layer specific learning rate. And so basically, layers that have big fanins for Adam get smaller learning rates. It allows you to have these layer-adaptive learning rates that are quite interesting.

这意味着我们将稍微改变设置初始化和学习率的方式。我们的初始化看起来像这样——对于 muP，蓝色框是我们的做法。我们的初始化将是 1/sqrt(n_{L-1}) 乘以一个分量 1/sqrt(扇出/扇入)。所以如果这是 1，那就等价于通常的初始化，这是标准参数化(standard parameterization)。但如果这个比值不小于 1，你会得到不同的结果——更接近 sqrt(扇出/扇入)。学习率你通常设置为关于模型大小的常数，但你想把它设置为扇出和扇入的比值。更有趣的是，对于 Adam，整个事情又有些不同——我甚至不会碰它的推导——你丢掉这个 1/nL 项，得到 1/扇入 作为层的特定学习率。所以基本上，对于 Adam，扇入大的层得到更小的学习率。它允许你有这些非常有趣的层自适应学习率(layer-adaptive learning rates)。

---

So that was the derivation of muP. I went through a lot of details. I do want to maybe talk about what the high-level point of that was. And the high-level point of that is, muP as an argument is very interesting. Not only is there actual useful stuff. The way in which you get to the algorithm is itself interesting because it's this very different kind of math in which you're saying, OK, I'm going to take a scaling limit of my network. And then I assert some invariance about my network, and then I'm going to make additional assumptions. And then I'm going to try to figure out what the constraints on my hyperparameters are. And the constraints essentially give you certain kinds of scaling limits on your hyperparameters as well. So this is a general principle for coming up with different kinds of algorithms or hyperparameter scalings, I think, which are probably very different than what you're used to in CS or ML training.

这就是 muP 的推导。我讲了很多细节。我想说一下高层次的重点。高层次的重点是：muP 作为一种论证(argiment)非常有趣。不仅有实际有用的东西，而且你得到算法的方式本身就很有趣，因为它是一种非常不同的数学：你说"好的，我要对我的网络取一个缩放极限(scaling limit)，然后我断言关于我网络的一些不变性，然后我做额外的假设，然后我试图找出超参数上的约束。"这些约束本质上也会给你超参数上的某种缩放极限。所以这是提出不同类型算法或超参数缩放的一般原理，我认为它可能与你习惯的 CS 或 ML 训练非常不同。

---

OK, those are the muP derivation. I want to close out on the muP part with just a few empirical things. There's an interesting paper by an independent researcher on basically stress testing muP in lots of different ways. And muP can be thought of as a procedure for tuning hyperparameters. And so depending on how you do things, Adam is going to have a certain learning rate as a function of different components of the network. So you have an embedding parameter, attention parameters, input/output MLPs or softmax linears. All of those are going to have different kinds of scalings under muP, as well as not muP scaling rules. And the interesting thing here is that particular paper replicated a bunch of the muP results for language models trained at different scales. And maybe unsurprisingly, he found almost the headline result from MiniCPM and others, which is that if you get the muP right, and you're only scaling with, in this case, in a very controlled way, you get exactly the learning rate optimality invariance that baseline muP-- or just looking at a variant of muP that tracks projection biases for attention, both of those transfer very nicely.

好的，这就是 muP 的推导。我想用一些实证的东西来结束 muP 部分。有一位独立研究者写了一篇有趣的论文，基本上以多种方式对 muP 进行了压力测试(stress testing)。muP 可以被视为一种调优超参数的过程。根据你的做法，Adam 会针对网络的不同组件有不同的学习率。所以你有嵌入参数、注意力参数、输入/输出 MLP 或 softmax 线性层——所有这些在 muP 下会有不同类型的缩放，而非 muP 缩放规则也不同。有趣的是，那篇论文复现了许多在不同规模下训练的语言模型的 muP 结果。毫不意外，他发现了几乎与 MiniCPM 等相同的头版结果：如果你把 muP 搞对了，并且在一个非常可控的方式下缩放，你就能得到精确的学习率最优不变性——基线 muP 或一个跟踪注意力投影偏置的 muP 变体都能很好地迁移。

---

But then you might ask, basically, there's a lot of things in the real world that muP does not handle. Technically, SwiGLU does not fit into muP, neither does initialize variations, initialization or RMS norm. Or if you really mess with your optimizer, that will mess that up, too. And so you might ask, like, which of these things that are not allowed by the theory really break muP? And actually, for the most part, these mostly work with muP. But some of the things that don't work is if you learn the gain term in RMS norm, this turns out to break muP. Although, these can be removed in many cases without necessarily hurting you, and so maybe it's not such a bad idea. But this does seem to break muP. It also seems to break if you use more exotic optimizers like Lion, which basically rely on the sign of the gradient. And sign gradient is like a spiritually similar to muon and other ideas. And so there might be other interesting things that break with muP as well.

但你可能会问，现实中很多东西是 muP 不处理的。从技术上讲，SwiGLU 不适合 muP，初始化变体或 RMS norm 也不适合。如果你真的折腾优化器，那也会搞乱它。所以你可能会问，这些在理论上不允许的东西中哪些真正破坏了 muP？实际上，大部分情况下这些都和 muP 兼容。但一些不兼容的东西包括：如果你学习 RMS norm 中的增益项(gain term)，这会破坏 muP。虽然在很多情况下可以移除它们而不一定损害性能，所以这可能不是太糟糕。但这确实似乎破坏了 muP。如果你使用更奇异的优化器（如 Lion），它基本上依赖于梯度的符号，也会破坏 muP。符号梯度在精神上与 muon 和其他想法相似。所以可能还有其他有趣的东西也会破坏 muP。

---

Finally, the thing that seems most concerning is that if you do large decoupled weight decay, you end up with significant muP failure. So this is maybe the one stress test that it does fail.

最后，最令人担忧的事情是：如果你做大的解耦权重衰减(decoupled weight decay)，你会导致显著的 muP 失败。所以这可能是它确实失败的一个压力测试。

---

But to close out this final section, you might, in the end, ask, like, is muP useful? And if you really want to stabilize your learning rates, it is actually pretty useful. There's a lot of experiments of this form, where if you increase the width, your optimal learning rate shifts very predictably, but very greatly as a function of scale. Whereas, with muP it doesn't. And so it's one of the many tools in the toolkit to try to control hyperparameter drift as a function of scale. I think it's an interesting open area of research. It's not really done and dusted, and this is the one right thing to do. But there's a lot of promise in the muP-style initialization program. There's also a lot of promise in just fitting scaling laws as well.

但为了结束这最后一部分，你最终可能会问：muP 有用吗？如果你真的想稳定学习率，它实际上相当有用。有很多这样的实验：如果你增加宽度，你的最优学习率非常可预测地移动，并且随规模变化很大。而使用 muP 则不会。所以它是工具箱中用来控制超参数随规模漂移的众多工具之一。我认为这是一个有趣的开放研究领域。它还没有尘埃落定，不是"这就是唯一正确的事"。但 muP 风格的初始化项目有很大的前景。仅仅拟合缩放定律也有很大的前景。

---

## Conclusion: Scaling in the Wild / 结论：现实世界中的缩放

So final thing I want to close with, scaling in the wild is very tricky. As I mentioned in one of my replies. I think the initial presentation of scaling laws makes it sound like a science. It's like, yes, draw this line, do these procedures, and you will know, for sure, what will happen at scale. But I think, in reality, it's a lot more messy and a lot more unknown than that. There are lots of things that people do use in practice scaling laws for, like picking architectures, picking optimizers, picking hyperparameters. All of these things are things that people do with scaling laws, but there is really an art to it in the sense of, you don't really know if it's truly going to extrapolate forever. You want to do reasonable things to maximize the chances of success.

最后我想结束的是：现实世界中的缩放非常棘手。正如我在回复中提到的那样，最初对缩放定律的呈现听起来像一门科学——是的，画这条线，做这些步骤，你就能确定在大规模下会发生什么。但我认为，实际上它比这要混乱得多、未知得多。人们在实际中使用缩放定律做很多事情，比如选择架构、选择优化器、选择超参数。所有这些都是人们用缩放定律做的事情，但这确实有一门艺术在，因为你并不真的知道它是否真的能永远外推。你想做合理的事情来最大化成功的几率。

---

And so there's lots of solutions that people have. You can use muP. You can search for the optimal learning rate in all of these other kinds of things. And these are ways of controlling hyperparameter drift. But there's no silver bullet yet. Maybe next year, there will be a module that's like, we solved it, but not quite yet.

所以有很多人们使用的解决方案。你可以使用 muP，你可以搜索所有其他这些东西中的最优学习率。这些都是控制超参数漂移的方法。但还没有银弹(silver bullet)。也许明年会有一个模块说"我们解决了这个问题"，但目前还没有。

---

Great. Thanks a lot. I can take questions afterwards.

非常感谢。之后我可以回答问题。
