---
title: "Lecture 9: Scaling Laws"
---

# Lecture 9: Scaling Laws / 第9讲：缩放定律

## 1. Introduction and Motivation / 引言与动机

We will get started. Well, temporarily leaving the land of systems to talk about more deep learning stuff, which we're going to have two lectures on scaling law and scaling law adjacent phenomena. So today is going to be the basics. We're just going to talk about pretty basic scaling law stuff, some of the classic works. How does the basic idea of scaling laws connect to maybe things you know about from machine learning 101. And then in two lectures, we're going to do the more advanced version of the scaling laws lecture, where we're going to basically go into a bunch of modern, open model tech reports, things like muP and other parameter initializations, and this year I'm going to throw in some more stuff for optimizers. So there will be an advanced version of this that will try to really get to the cutting edge.

我们将暂时离开系统领域，来讨论深度学习的内容。我们会有两讲关于缩放定律及其相关现象。今天是基础部分，我们只讨论非常基础的缩放定律内容，一些经典的工作，以及缩放定律的基本思想如何与你可能在机器学习101中学到的知识联系起来。然后在两讲之后，我们会有更高级的缩放定律讲座版本，届时将深入探讨大量现代开源模型技术报告、μP等参数初始化方法，今年我还会加入一些优化器的内容。因此会有一个更深入的版本，力求触及前沿。

Today, we're going to start with all the really basic stuff. Scaling laws is really the following scenario: you have your very wealthy friend, who has given you 10,000 B200s for a month, and he or she has asked you to build a very good open source language model. They would like to get something out of those B200s. And so you've already put together your infra team. And you have, let's say, a good pre-training data set. And then you're going to go and train a big model, but there's lots of choices in training a big model—all the assignments, the earlier lecture two stuff that we had earlier, where you have questions like: what architecture should I use? What should my hyperparameters be? And it's very scary to run these things on a run that is basically, potentially millions of dollars in cost. So how do you really take this idea of scaling up very seriously? How do you make sure that your big run is actually successful?

今天我们从最基础的内容开始。缩放定律其实对应着这样一个场景：你有一位非常富有的朋友，给了你10,000块B200 GPU用一个月，请你构建一个非常优秀的开源语言模型。你已经组建好了基础设施团队，也假设有了一份不错的预训练数据集。然后你要去训练一个大模型，但在训练大模型时有很多选择——所有之前的作业、第二讲中讨论过的问题，比如应该用什么架构？超参数该怎么设？在一轮训练可能花费数百万美元的情况下运行这些东西是非常可怕的事情。那么，你如何真正认真地对待"扩展"这个理念？如何确保你的大规模训练运行真正成功？

So of these many choices, some of which you're going to just copy out of the literature. The stuff that I talked about earlier in the architecture lecture is really about well-adopted best practices, and you will probably just pick some of these out of a hat. That's fine, but really, let's say you're at the frontier. You would like to build something that's actually better than the best available models today. You have to start really optimizing these. You can't just copy the choices of others and get something that's better than the state of the art. So how do we do that? Well, that's going to require us to really engage with this idea of scaling.

在这些众多选择中，有些你会直接从文献中复制。我之前在架构讲座中讲的那些内容，实际上是一些被广泛采纳的最佳实践，你可能随便选几个就好。但假设你处于前沿位置，想要构建一个确实比当今最先进的模型更好的东西，你就必须真正开始优化这些选择。你不能仅仅复制别人的选择就得到超越当前最优的结果。那我们该怎么做？这需要真正深入理解"缩放"这一概念。

So scaling laws have been one very powerful tool. You might also call it a paradigm. Scaling laws, if you talk to some people who are really in these big labs doing scaling work, it's almost kind of a way of life. They really believe in the scaling laws. It's almost a belief, and you'll see why scaling laws can sometimes be quite tricky objects. But really, scaling laws are these simple, predictive rules of how to go from small scale model performance and behavior, and to try to extrapolate them up to large scale behavior.

缩放定律一直是一个非常强大的工具，你也可以称之为一种范式。如果你和那些在大实验室里真正从事缩放工作的人交谈，缩放定律几乎成了一种生活方式。他们真的相信缩放定律——这几乎是一种信念，而你也将看到为什么缩放定律有时会是相当棘手的对象。但实际上，缩放定律是一些简单的预测性规则，描述如何从小规模模型的表现和行为出发，尝试将其外推至大规模的行为。

So the basic naive way to approach model training might be to say, I have a big budget, I'm going to do multiple training runs on these very big runs, and I'm going to tune hyperparameters on those big runs, but that's very wasteful. So instead, what I would like to do is I would like to do all of my optimization at the small scale and have some simple rule that allows me to extrapolate small scale behaviors to large scale behaviors. And if the small scale and large scale are connected by some very simple, robust connections like regularities of some kind, then you would have confidence in this kind of new scaling approach to optimizing your system. And that's really what today is all going to be about—this engineering view of a scaling law.

基本的朴素方法可能是：我有大量预算，我要在这些非常大的运行上做多次训练，并在那些大规模运行中调优超参数——但这非常浪费。相反，我想做的是：在小规模上完成所有优化，然后利用某种简单的规则将小规模的行为外推至大规模。如果小规模和大规模之间通过某种非常简单、稳健的规律性联系在一起，那么你就会对这种缩放式优化系统的方法充满信心。这就是今天全部内容的主题——缩放定律的工程视角。

## 2. Historical Background / 历史背景

And to start with, I'm going to talk a little bit about background, because scaling laws are very interesting in that not only are they the newest paradigm—that's how a lot of these models are designed and thought—but also they connect very closely to very classical ideas. So if you're a person that's a machine learning theorist, actually, there are some things that you will really feel at home with, so they're like empirical sample complexities. And then I'll talk through the history of scaling laws of one kind and show you that this is not something that's really new. It's something with actually quite a bit of history and research done to it.

首先，我会讲一些背景知识，因为缩放定律非常有趣——它们不仅是最新的范式，许多模型就是按照这样的思路来设计和思考的，而且它们还与非常经典的思想密切相关。如果你是一个机器学习理论研究者，你会在某些方面感到很熟悉，缩放定律就像经验化的样本复杂度。然后我会梳理一类缩放定律的历史，向你展示这并非什么真正新的东西，它实际上有着相当长的历史和研究积累。

For the longest time, machine learning has thought about this question of how will my model perform, especially from a theory perspective. I have this model class, how good is my model going to be? And generalization bounds is the theorist's answer to this question. So you have your error over some finite hypothesis class, and you say, oh, my error is going to be at most this much worse than the model's performance on my training set. This is classic generalization bounds. Not only does this tell you something about performance, notice that these bounds are often dependent on the sample size. And so this is telling you, well, this is a theoretical upper bound on my loss values as a function of how my training set grows. And in some ways, that's very closely related to this idea of what happens as I scale up the amount of data that I have.

长期以来，机器学习一直思考这个问题：我的模型会表现如何，特别是从理论角度？给定一个模型类，我的模型会好到什么程度？泛化界是理论研究者对这个问题的回答。你有一个有限假设类上的误差，然后说我的误差最多比模型在训练集上的表现差这么多——这就是经典的泛化界。这不仅告诉你一些关于性能的信息，注意这些界通常依赖于样本量。所以它在告诉你：这是关于损失值的理论上界，作为训练集增长的一个函数。在某种意义上，这与我扩大数据量时会发生什么的问题密切相关。

And if you try to figure out what is the very first scaling law paper that exists? It turns out you can go back quite far. You can go back to Bell Labs and Corina Cortez and Vladimir Vapnik and these folks that were doing very serious theory work on machine learning. They asked this question: training classifiers on a really large data set is often very expensive. We would like to avoid doing that, and to do so maybe we can just fit classifiers on a smaller sample, fit a curve to how their error rates decay, and use that as a way to estimate their performance. That's almost literally a data scaling law back in 1993. So this idea, at the very least, thinking about how your model's performance changes as a function of data set size is just a very classical one.

如果你试图探究最早存在的缩放定律论文是什么，你会发现可以追溯到很久以前。你可以追溯到贝尔实验室、Corina Cortes、Vladimir Vapnik这些人，他们当时在做非常严肃的机器学习理论工作。他们提出这样的问题：在非常大的数据集上训练分类器通常非常昂贵。我们想避免这样做，也许可以在较小的样本上拟合分类器，然后对错误率的衰减拟合一条曲线，用来估计在更大数据集上的性能。这简直是1993年版本的"数据缩放定律"。所以这个想法——思考模型性能如何作为数据集大小的函数而变化——是一个非常经典的想法。

And if you start to look at the history of this, there's a lot of people that have said, isn't it the case that maybe instead of spending money on algorithm development, maybe we should just go collect more data? Because if we plot how the performance of our systems behave as a function of the amount of data that we have, it turns out that they are all increasing or improving in predictable ways. Banko and Brill is one of the canonical NLP references in how the amount of data and thinking about scaling is a really valid way of improving system performance.

如果你回顾这段历史，有很多人都说过：也许与其在算法开发上花钱，不如去收集更多的数据？因为如果我们画出系统性能如何随数据量变化而变化的曲线，会发现它们都以可预测的方式在提升或改善。Banko和Brill是NLP领域一个经典的参考文献，他们指出数据量和缩放思维确实是改进系统性能的有效方式。

There's also work by other NLP folks like Kolachina et al. in 2012. This is one of the earlier works on different kinds of functional forms for scaling laws, where once again, they're increasing the amount of data that they're using to train, in this case machine translation systems or BLEU scores. And they're asking: what is the right functional form for how a model's performance behaves as a function of increased data amount? And they maybe surprisingly or not surprisingly, end up with the same power laws, which is pow-3 and pow-4 as really we do today. For the rest of the lecture, you're going to keep seeing essentially these polynomial functions as I talk about scaling laws.

还有NLP领域其他研究者的工作，如2012年Kolachina等人的论文。这是关于缩放定律不同函数形式的早期工作之一，他们同样是增加训练所用的数据量——在这里是机器翻译系统或BLEU分数。他们在问：模型性能作为数据量增加的函数的正确函数形式是什么？也许令人惊讶，也许不，他们最终得到了与我们今天使用的完全相同的幂律关系——负3次方和负4次方。在接下来的整个讲座中，你将不断看到这些多项式函数。

And then finally, I really like mentioning this paper because for whatever reason, Hestness et al. don't get cited quite as much as they should. The origins of neural scaling, I would point back to Hestness in 2017. Really a very forward-looking work in many ways that built these scaling laws as a function of data set size for a wide variety of systems—different kinds of speech recognition systems, machine translation systems, language models—and they showed that these things follow these nice polynomial trends across a really large number of domains. And it was really ahead of its time, because 2017 was long before some of the earlier OpenAI scaling laws and so on in the 2020s. And they talked about stuff that we talk about today, like emergence—where suddenly models might show certain kinds of capabilities because accuracy is a much more discontinuous measure than losses. And really, scaling by compute: that if we have systems that scale predictably to large training data, then really compute is going to be really important. And then finally, since we're scaling by compute, well, speed and systems optimization is going to turn into accuracy.

最后，我非常喜欢提及这篇论文，因为不管什么原因，Hestness等人没有得到他们应得的引用。神经缩放定律的起源，我会指向Hestness在2017年的工作。这在很多方面确实是一项非常有远见的工作，他们构建了作为数据集大小函数的缩放定律，涵盖了广泛多样的系统——不同类型的语音识别系统、机器翻译系统、语言模型——并且展示了这些系统在大量领域中都遵循这些优美的多项式趋势。这确实超前于时代，因为2017年远远早于OpenAI在2020年代发表的早期缩放定律论文。他们还讨论了我们今天在谈论的内容，比如涌现现象——模型可能突然展现出某些能力，因为准确率比损失更加不连续。还有按计算缩放的概念：如果我们有能够可预测地扩展到大规模训练数据的系统，那么计算能力真的会变得非常重要。最后，由于我们在按计算缩放，速度和系统优化将转化为准确率的提升。

So in some ways, a lot of the things that we see today, like the phenomena of system scaling and so on, we could have really known in 2017 had I read and thought about a lot of these scaling laws papers back and thought about them more seriously.

所以在某种程度上，我们今天看到的许多现象，比如系统缩放等现象，其实我们在2017年就本可以认识到，只要我当时认真阅读和思考这些缩放定律论文。

There's no golden rule that these are the only ones. However, in some ways, theory provides a very rich place, where the scaling law functional forms can come from because theory is often thinking a lot about how do error rates decay as a function of various objects. And they give you candidate functional forms of various kinds. Physicists are also very good at this because they think about limits—like how do the limits behave—and that gives you different scaling law functional forms.

并没有金科玉律说这些幂律形式是唯一的形式。不过，在某种意义上，理论为缩放定律的函数形式提供了丰富的来源，因为理论经常在思考错误率如何作为不同对象的函数而衰减，并给出各种候选的函数形式。物理学家在这方面也非常擅长，因为他们思考极限——极限如何表现——这会给出不同的缩放定律函数形式。

## 3. Data Scaling Laws / 数据缩放定律

Now I'm going to start talking about more modern neural language model scaling, and I'm going to start with data scaling laws because to me, they're the most simple and natural objects. Talking about data scaling laws also allows me to walk you through very step-by-step on how we might guess what the functional form of a scaling law might be and why the polynomial form is a natural one. And then I'm going to start talking about hyper parameters and architectures and all sorts of other more exotic objects that are going to be harder to justify from intuition, but still turn out to have very nice scaling law behaviors.

接下来我要开始讨论更现代的神经语言模型缩放，我会从数据缩放定律开始，因为对我来说它们是最简单、最自然的对象。讨论数据缩放定律也能让我逐步带你们了解我们如何猜测缩放定律的函数形式，以及为什么多项式形式是自然的。然后我会开始讨论超参数、架构以及其他更奇特的对象——这些从直觉上更难论证，但仍然展现出非常优美的缩放定律行为。

One of the things that's remarkable about this scaling law style analysis has been that these power law relationships seem to hold for a huge variety of different factors. The basic ones that we see in pre-training, and those are going to be the ones that I'm going to talk about today. The usual ones that you see are compute on the x-axis—this is log compute—log of test loss on the y-axis, or log of the data set on x-axis, log of loss on the y-axis, log of parameters on x-axis, log of loss once again on the y-axis. So we can get a variety of different x-axes that you might think of as resources in the log axis. All of them linearize log test loss here.

缩放定律分析的一个显著特点是，这些幂律关系似乎对大量不同的因素都成立。基本的关系是我们在预训练中看到的，这也是我今天要讲的。你通常看到的是：x轴是计算量（对数坐标），y轴是对数测试损失；或者x轴是对数数据集大小，y轴是对数损失；或者x轴是对数参数量，y轴还是对数损失。所以我们可以有各种不同的x轴——你可以将它们视为对数坐标上的资源量，所有这些都能将对数测试损失线性化。

### 3.1 Power Law Relationships in Data Scaling / 数据缩放中的幂律关系

So to begin with, I'm going to start with data scaling laws. Data scaling laws are a very simple kind of univariate relationship that we're going to think about. So in this world, we're going to fix our model training procedure. And in general, unless I say otherwise, the models are going to generally be bigger than the data set size. And I'm going to increase my data set size in a regular way, and I'm going to see how the error reduces. And what do we expect out of this relationship? In general, it's going to be monotone-ish if we tune our hyperparameters well. Because we have more data, more data should help us do better at our task. The error should decrease. And if you're doing something like classification, or even for next token prediction, you should really go from random guessing to some entropy-like object where you can't do any better than the irreducible error of your task. That's the noise floor.

首先从数据缩放定律开始。数据缩放定律是一种非常简单的单变量关系。在这个设定中，我们固定模型训练过程。一般来说，除非我特别说明，模型通常会比数据集规模更大。然后我以规律的方式增加数据集大小，观察误差如何降低。我们期望从这种关系中得到什么？一般来说，如果我们很好地调优超参数，误差会呈现单调递减趋势。因为数据越多，应该越有助于我们在任务上做得更好，误差应该下降。如果你在做分类或下一token预测，应该从随机猜测逐步逼近某种熵类目标，即你无法做得比任务的不可约误差更好——那就是噪声底线。

If we just have a very big model, much bigger than our data set, and we increase the data set size, and we put that on the log axis, and on the y-axis, we have log test loss. You will find that the two points that you plot will form a very clear linear trend. I've taken this from Kaplan in 2020. This relationship, where I've plotted a line on a log-log plot, this is a scale-free or power law relationship. If something is linear in a log-log plot, what does that mean? Well, it means that the error I have is decaying polynomially. And also, it usually means that I'm very far away from my asymptote, because once I approach my asymptote, I'm going to taper off rather than have a line.

如果我们有一个非常大的模型，远大于数据集规模，然后增大数据集大小，将数据集大小放在对数坐标的x轴上，y轴是对数测试损失——你会发现绘制的点会形成非常清晰的线性趋势。我这是从Kaplan 2020年的论文中取的。在对数-对数图上绘制出一条直线，这被称为无标度关系或幂律关系。如果某个东西在对数-对数图上是线性的，这意味着什么？这意味着误差在多项式地衰减。同时，这通常意味着我们离渐近线还很远——因为一旦接近渐近线，曲线会平缓下来，而不是一直保持直线。

### 3.2 Why Power Laws? A Statistical Perspective / 为什么是幂律？统计视角

So let's go through an example just to show you how a scaling law arises very naturally on a very simple estimation problem. So forget language modeling for the moment. In this case, what I want to do is I want to estimate the mean from a bunch of data. And so I have an input, it's drawn from a Gaussian. And I'm going to estimate the mean of this object. I just write down the empirical mean. And then, you can write down what the error is. So what's the expected error? Well, each of these guys is Gaussian, and mu hat is Gaussian, so I can write down the error. That's going to be sigma squared over n. So well, if you look at this, is a scaling law. I've written down the error, and the error, if I log that, is a function of log n—log n being the log x-axis. So in general, if you can come up with anything that is essentially 1 over n to the alpha plus some constant, when you plot that on a log-log plot, subtracting out the constant term, you're going to get a scaling law.

让我们通过一个例子来展示缩放定律如何在一个非常简单的估计问题上自然出现。暂时忘掉语言建模。我想做的是从一堆数据中估计均值。我有一个输入，从一个高斯分布中抽取，我要估计这个分布的均值。我写下经验均值，然后可以写出误差是多少。期望误差是多少？每个样本都是高斯的，mu-hat也是高斯的，所以我可以写出误差——它是sigma平方除以n。如果你看到这个，这就是一条缩放定律。我写出了误差，如果对其取对数，它就是log n的函数——log n就是对数x轴。所以一般来说，如果你能得出任何实质上形如1/n^α加上某个常数的东西，当你在对数-对数图上绘制它，减去常数项后，你就会得到一条缩放定律。

So anything of this form, where you have polynomial decay in errors, is going to end up giving you a scaling law. And of course, in parametric estimation like mean estimation or regression, you of course, expect a polynomial rate. You don't really expect anything else. And if you've taken your stats estimation courses, you know that essentially all the classical models are expected to have a 1 over n scaling. If you fit a regression or so on, you might get D over n or whatever else. And so if this is true, and this is the origins of scaling laws, if we plot our lines, we should expect to see roughly a slope of minus 1 because that's the exponent on the x. Y equals minus x plus C.

所以任何具有多项式误差衰减形式的东西最终都会给出缩放定律。当然，在参数估计中——如均值估计或回归——你当然期望多项式速率，你不会期望其他形式。如果你上过统计估计课，你会知道基本上所有经典模型都应该有1/n的缩放。如果你拟合回归等，你可能得到D/n或其他类似形式。因此如果这是真的——这是缩放定律的起源——当我们画出这些直线时，我们应该期望看到大约为-1的斜率，因为这是x的指数，y等于负x加C。

If we fit our neural scaling laws, we will find that our exponents are quite different. These exponents—I've taken from these two on the left from Hestness, I've taken the one on the right from Kaplan—they're about -0.1, -0.3, -0.1, roughly speaking. And so what does that mean? That means this is much slower than estimating a mean or estimating a linear regression. So this is much, much slower convergence rate, still polynomial, but much slower.

但如果我们去拟合神经网络的缩放定律，会发现指数完全不同。这些指数——左边两个来自Hestness，右边一个来自Kaplan——大约在-0.1、-0.3、-0.1左右。这意味着什么？这意味着收敛速度比估计均值或线性回归慢得多。收敛速度慢得多，虽然仍然是多项式的，但慢很多。

Where might you get an estimation rate like this? Well, you would get this if your model was more nonparametric. Let's say that I want to estimate now, instead of a mean, an arbitrary smooth function. A trivial estimator for this is I can take my space, I can cut it up into little 2D boxes. And then what's our estimation error? In general, if have a D-dimensional function I would like to estimate in this very nonparametric, arbitrary way, my error is going to be roughly equal to n to the negative 1 over D. So my scaling is going to be y equals negative 1 over D times x. And so now these kinds of more flexible functions, functions that are more flexible than the linear class, now have rates in their scaling laws that are not just 1, they're 1 over D.

在什么情况下你会得到这样的估计速率？如果你的模型更非参数化就会这样。假设我现在要估计的不是均值，而是一个任意的光滑函数。一个简单的估计器是我可以把这个空间切成许多小二维盒子。那么估计误差是多少？一般来说，如果我有一个D维函数要以这种非常非参数的任意方式估计，我的误差大致等于n的-1/D次方。所以我的缩放将是y等于负1/D乘以x。因此，这些比线性类更灵活的函数，其缩放定律中的速率不是1，而是1/D。

And so one mental model that you could have is that the neural networks I was showing you in these slides are behaving kind of like non-parametric regressors in 10 dimensions, like a nearest neighbor or other kinds of estimators in 10 dimensions. That's roughly the rate at which they learn from data. That's kind of a cool thing to be able to know just by looking at some of these scaling laws. Some people have argued this more strongly. Bari et al. and some other scaling law theory folks have argued that the scaling law exponents are actually literally telling us that the neural network is behaving like a non-parametric smoother. It's an interesting set of arguments, and you can buy that intuition to whatever extent you'd like.

所以你可以有一个心智模型：我在这些幻灯片中展示的神经网络，其行为大致类似于10维空间中的非参数回归器——就像10维中的最近邻或其他估计器。这大致就是它们从数据中学习的速率。仅仅通过观察这些缩放定律就能知道这一点，是相当酷的。有些人对此有更强的论证。Bari等人以及其他缩放定律理论研究者认为，缩放定律的指数实际上在字面意义上告诉我们神经网络的行为就像一个非参数平滑器。这是一套有趣的论证，你可以在你觉得合适的程度上接受这种直觉。

I don't quite know how much I truly, truly buy this argument. There's some evidence that might be a little sketchy. It relies on estimators of intrinsic dimension, but it's an interesting thing to think about that somehow these exponents are telling us how fast are these neural networks really learning.

我不太确定自己在多大程度上真正相信这个论证。有些证据可能有点站不住脚，它依赖于内在维度的估计量。但思考这些指数如何告诉我们神经网络实际上学习得有多快，是一件有趣的事情。

## 4. Data Mixture and Repetition / 数据混合与重复

Data scaling laws by themselves are not quite as useful as you'd like them to be. They just tell you how fast does my model learn. And that's kind of useful for forecasting. It's not useful for very much else. If you want to do engineering, you are probably interested in other questions, like what is my optimal data mixture? What is the best way for me to pick my training data for my model? Very useful engineering question. Should I repeat my data, or should I just not repeat my data, save the compute for something else? Or maybe I should repeat some high-quality stuff and not repeat the low-quality stuff. I could do various other things with repetition. There's a lot of different engineering decisions I can make with data.

数据缩放定律本身并不像你期望的那样有用。它们只是告诉你模型学习得有多快，这对于预测有一定用处，但除此之外用处不大。如果你要做工程，你可能会对别的问题感兴趣，比如最优数据混合是什么？为我模型挑选训练数据的最佳方式是什么？这是非常有用的工程问题。我应该重复使用数据，还是不应该重复，把计算资源留给其他事情？或者也许我应该重复一些高质量数据而不重复低质量数据？对于数据重复有很多不同的工程决策可以做。

So how can scaling laws help us make some of those decisions? And I think one of the things that's interesting is if we think a little bit about how classical models behave. Data scaling laws, if we think about their origins as essentially empirical versions of generalization bounds, they tell us, well, data set composition for many models really affects the offset of these scaling laws, but their slopes are actually determined by the model class. They're not really determined by the distribution themselves. So the slopes might remain the same, and only the intercepts might change. And the intercept might actually be really interestingly shaped.

那么缩放定律如何帮助我们做出这些决策？我认为有趣的一点是，如果我们想一想经典模型的行为。数据缩放定律——如果我们把它们视为泛化界的经验化版本——告诉我们：对于许多模型，数据集组成确实影响缩放定律的截距，但斜率实际上由模型类别决定，而非由分布本身决定。所以斜率可能保持不变，只有截距可能改变。而截距的行为可能非常有趣。

What does this practically mean? Well, practically speaking, what this means is you can actually fit data scaling laws on mixtures, and that can help you do pre-training data optimization. Let's say you have two data sources for simplicity—you have news, and you have Wikipedia. How much news to use and how much Wikipedia to use? How can you determine that? Well, you can train really small models on a really small amount of data. And then you can fit a function of how different mixture levels affect your performance. You can do this while you scale up your models little by little. And you can see how the trends change. And you can try to extrapolate that out the exact same way as you would extrapolate out a data scaling law. And then you can ask which one will be optimal if I keep scaling it out to my full training run.

这在实践中意味着什么？实际上，这意味着你可以对数据混合拟合缩放定律，这可以帮助你进行预训练数据优化。为简单起见，假设你有两个数据源——新闻和维基百科。多少新闻、多少维基百科？你如何确定？你可以用少量数据训练非常小的模型，然后拟合一个函数来描述不同混合水平如何影响性能。你可以在逐步扩大模型的同时进行这一操作，观察趋势如何变化，并尝试以与数据缩放定律完全相同的方式进行外推。然后你可以问：如果我一直扩展到全量训练运行，哪个混合比例是最优的？

This is a very simple idea of essentially fitting a functional form at a small amount of compute, finding the minimum, and then scaling that guy out. Unfortunately, I think if you talk to anyone who's done a lot of these data mixture work, they will tell you reality is a lot more noisy than this ideal world would suggest. And really, what has happened in many cases is you end up training a bunch of small models. You pick the best data mix from the small model, and you just scale that guy up, no scaling law required. If you don't fit a scaling law, and instead you just pick the best data mix at the small scale, that works well. For what it's worth, that's consistent with the argument that the intercepts differ, but the slopes don't change. Because if the slopes don't change, the best mixture at small scale is also the best mixture at large scale.

这是一个非常简单的想法：在小计算量下拟合一个函数形式，找到最小值，然后将其扩展出去。不幸的是，如果你与做过大量数据混合工作的人交流，他们会告诉你现实比这个理想世界所暗示的要嘈杂得多。实际上，在很多情况下，你最终只是训练了一堆小模型，从小模型中挑选出最佳数据混合，然后直接将其扩展——根本不需要缩放定律。如果你不拟合缩放定律，而只是在小规模下选择最佳数据混合，效果也很好。值得指出的是，这与"截距不同但斜率不变"的论点是一致的，因为如果斜率不变，小规模下的最佳混合也是大规模下的最佳混合。

Another really interesting set of questions that I'll also mention in the context of data is repetition. I think it's increasingly the case that compute is growing, the amount of data that we have is not growing. And so there's a lot of people interested in questions of what happens when you repeat data more and more times. And there was a nice study a few years back called "Scaling Data-Constrained Language Models," where they roughly show something like up to four epochs with standard training recipes, you just don't get hurt at all. But if you go past that point, then actually your realized scaling law, this dark curve, is much worse than the projected scaling law if you had fresh data. And you can also write down a modified functional form that's generally predictive of the behavior of this scaling law under repetition.

在数据的背景下，我还要提及另一组非常有趣的问题：数据重复。我认为越来越明显的情况是，计算能力在增长，但我们拥有的数据量没有增长。因此，很多人对越来越多地重复数据会发生什么感兴趣。几年前有一项很好的研究叫"Scaling Data-Constrained Language Models"，他们大致表明：使用标准训练方案最多四个epoch，你完全不受伤害。但如果超过这个点，你实际实现的缩放定律（这条深色曲线）会比如果有新数据时的预测缩放定律差得多。你也可以写出一个修改过的函数形式来大致预测这种重复条件下的缩放定律行为。

And we can take this idea even more to the extreme. What happens if you take this idea to the extreme and you just consider infinite amounts of compute? So you're allowed to epoch as many times as you want, like an infinite amount of times. What is the best thing that you can get out of this system? Well, it turns out you can't just keep repeating passes over the data. You can't keep making your models bigger. Those have diminishing returns. And so you end up reaching for other things, like ensembling your models to try to squeeze more and more out of your data. But really, I think the one thing that I'll point out that's really interesting is your standard data scaling laws here in the red—it's a very nice, predictable improvement in performance as you increase the amount of data. We do all sorts of interventions like regularizing and adding ensembles. You get improvements in performance, but the slopes look actually surprisingly similar.

我们甚至可以把这个想法推向更极端的程度。如果你考虑无限计算量的情况会怎样？你可以无限次地遍历数据。你能从这个系统中得到的最好的东西是什么？结果是，你不能只是一遍又一遍地重复数据遍历，也不能只是不断增大模型——这些都有递减回报。所以你最终会转向其他手段，比如集成模型来试图从数据中榨取更多。但我认为特别有趣的一点是：标准的红色数据缩放定律——随着数据量增加，性能得到非常优美、可预测的提升。我们做各种干预，比如正则化和添加集成，性能确实有提升，但斜率看起来出奇地相似。

This is a lesson that you'll learn once you start fitting your own scaling laws, that very, very often your slopes don't change. Often, the interventions that you do just change the intercept of the scaling laws.

这是你一旦开始拟合自己的缩放定律就会学到的一课：斜率非常非常经常不会改变。通常，你所做的干预只是改变了缩放定律的截距。

One last thing that I'll mention is that a lot of the phenomena we care about in data is actually very scale-dependent. And one example of this is data filtering. So if you or I tomorrow decide to filter some data for the models we're training, we would probably filter very aggressively. We would only keep the highest quality stuff because both you and I don't have very much compute. So we can't train on all the internet anyway. On the other hand, if you have a lot of compute, then you want to train on more and more stuff because you're going to not want to repeat on this very high-quality data. So as you get more and more compute, your filter has become looser and looser, and potentially you start training on stuff that's lower and lower quality. So a lot of the things that we often think about statically—things like data filtering or the quality of data—are actually much more dynamic. As you increase scale, you have to think about where am I going to get the rest of the data. The filters can't stay fixed as a function of the data, and certainly the optimal filters turn out to not be fixed as a function of scale.

我还要提最后一点：我们在数据中关心的很多现象实际上是高度依赖规模的。一个例子是数据过滤。如果你我明天决定为训练的模型过滤一些数据，我们可能会非常激进地过滤。我们只保留最高质量的东西，因为你和我都没有太多计算资源，反正也训练不了整个互联网的数据。另一方面，如果你有大量计算资源，你就会想训练越来越多的数据，因为你不想在这些非常高质量的数据上重复太多。所以随着计算资源越来越多，你的过滤器会变得越来越宽松，你可能开始训练质量越来越低的数据。所以我们经常静态思考的许多事情——比如数据过滤或数据质量——实际上更加动态。随着规模增大，你必须思考从哪里获取剩余的数据。过滤器不能作为数据的函数固定不变，而最优过滤器也确实不会作为规模的函数固定不变。

## 5. Scaling Laws for Model Engineering / 模型工程的缩放定律

Now I want to talk about more exotic forms of scaling and scaling laws for model engineering of various kinds. So what we're going to do now is we're going to try to design large language models. Maybe you're a radical, and you believe that maybe LSTMs are the future. Like, why can't I use LSTM instead of a transformer? I want to blow my B200 run on my LSTMs. Or maybe you're a different kind of radical and you want to train on SGD. Like, why can't I train on SGD? You might also wonder, if you have a limited amount of resources, you have different ways to spend it. Maybe you should train models longer, maybe you train bigger models, maybe I should go collect more data. There's all sorts of trade-offs always at play, and scaling laws give us quantitative ways of making these trade-offs, hopefully.

现在我想讨论更奇特的缩放形式以及各种模型工程的缩放定律。我们要做的是尝试设计大语言模型。也许你是个激进派，相信LSTM是未来——为什么不能用LSTM代替Transformer？我想把B200的计算资源花在LSTM上。或者你是另一种激进派，想用SGD来训练——为什么不能用SGD训练？你可能也会好奇，如果资源有限，有不同的花费方式：也许应该训练更长时间，也许训练更大的模型，也许应该去收集更多数据。总是有各种各样的权衡在发挥作用，而缩放定律希望给我们提供量化这些权衡的方法。

### 5.1 Architecture Scaling: Transformers vs. LSTMs / 架构缩放：Transformers与LSTMs

The very first question we might start with is to say, Are transformers really better than LSTMs? LSTMs can work OK, too. They will fit distributions. With the advent of things like Mamba, we know that SSMs can work. So are they better? The brute force way to answer this question is to train a big LSTM GPT-3 or even bigger class of models. The scaling law way would be to train a bunch of smaller models and say, I'm going to train my transformer across a different variety of compute ranges, and I'm going to train different LSTMs with different numbers of layers on, once again, a variety of different compute ranges.

我们可能从第一个问题开始：Transformer真的比LSTM更好吗？LSTM也能工作，它们也能拟合分布。随着Mamba等模型的出现，我们知道状态空间模型也能工作。那么Transformer更好吗？蛮力的回答方式是训练一个大型LSTM版GPT-3甚至更大规模的模型。缩放定律的方式则是训练一堆较小的模型：用不同计算量范围训练Transformer，同时用不同的层数训练不同的LSTM，同样遍历不同的计算量范围。

Now, what does this show? This shows LSTMs have definitely different intercept, maybe even different slope than the transformer. And because of this, probably you don't want to pick out LSTM. This plot would justify scaling up the transformer instead of the LSTM. And if you look at a lot of the architecture papers today, like you go look at the Mamba paper or the gated delta net papers, they will always have a plot that looks like this, where you have vanilla transformer, our really cool model. And our really cool models, usually either on top or below, because that's what would prove that your model is doing better. And you certainly don't want something where your slopes are worse because that means as you scale up larger and larger, your models will eventually do worse.

这说明了什么？这说明LSTM的截距明显不同，甚至斜率也可能与Transformer不同。正因为如此，你可能不会选择LSTM。这个图证明了应该扩展Transformer而不是LSTM。如果你去看今天很多架构论文——比如Mamba论文或门控delta网络论文——它们总会有类似这样的图：vanilla Transformer vs 我们超酷的模型。而超酷模型通常要么在上方要么在下方，因为这才能证明模型表现更好。你绝对不想要斜率更差的东西，因为那意味着随着规模越来越大，你的模型最终会表现更差。

I think one thing that's really cool about architecture scaling is that the paper by Ek and others at Google captured exactly the architecture changes that we implement today in our frontier models. So things like performer, which is an efficient attention, that doesn't scale very well. We do not implement those. The things that we implement are the gated linear unit—red line better than green line throughout the scaling trends. Switch transformer—generally speaking, it's got good scaling trends. So you see that through this scaling trends, even though a lot of these papers were operating on much, much smaller compute scales than what we operate today, they're able to see the kinds of architecture trends that are driving frontier model development back then. And I think this is why a lot of people use scaling laws as a really, almost paradigmatic way, saying, "Oh, if it doesn't show up in the scaling law, it's not a good intervention."

我认为架构缩放中非常酷的一点是，Ek等人在Google的论文精准捕捉了今天我们前沿模型中实施的架构变化。比如Performer这种高效注意力机制，缩放表现不佳——我们不采用。我们采用的是门控线性单元（在整个缩放趋势中红线优于绿线）、Switch Transformer（总体缩放趋势良好）。所以你可以看到，通过这些缩放趋势，即使这些论文的计算规模比我们今天的小得多得多，它们依然能够看到推动当时前沿模型发展的架构趋势。我认为这就是为什么很多人将缩放定律当作一种近乎范式性的方式，说："如果它在缩放定律中不成立，那就不是好的干预。"

### 5.2 Optimizer and Hyperparameter Scaling / 优化器与超参数缩放

Going beyond architectures, we can extend this kind of analysis to all sorts of other things that we might want to understand. We might ask, OK, is SGD better or worse than ADAM? If you do the scaling law analysis, you'll see very clear trends. This is once again, the really mysterious thing of the intercepts are different, but the slopes are very similar. If you fix the data and you fix the models, slopes are often very, very similar. I am very surprised by this every time I see it. And yet, it's very true. It's rare to get different slopes, even with an intervention as big as SGD to ADAM.

超越架构，我们可以将这种分析扩展到我们想要理解的各种其他事物。我们可以问：SGD比ADAM更好还是更差？如果你做缩放定律分析，你会看到非常清晰的趋势。这再次出现了那个非常神秘的现象：截距不同，但斜率非常相似。如果你固定数据和模型，斜率常常非常非常相似。我每次看到这一点都感到非常惊讶，然而这确实是真的。即便是从SGD到ADAM这么大的干预，也很少得到不同的斜率。

Similarly, in lecture 2, I told you about aspect ratios. How do you pick your depth-to-width trade-off? And I told you, well, you can just pick some random number that's somewhat roughly reasonable. It's like four times the reasonable multiplier. But if you're doing this kind of scaling analysis, you could much more precisely understand what is happening. So the first thing you could do is you could look at scaling trends as a function of layers, and you would immediately see that having extremely few layers is very, very bad for your model. If you have one layer, you're not going anywhere. That's a terrible, terrible scaling trend. Greater than 1 layer, actually, it's surprisingly more competitive, although you do see that at every compute level, more layers, at least in this case, is better.

类似地，在第二讲中我讲了宽度比。如何选择深度与宽度的权衡？我当时说，你可以随便选一个大致合理的数字，比如四倍之类的。但如果你做这种缩放分析，你可以更精确地理解发生了什么。首先，你可以看作为层数函数的缩放趋势，你会立刻发现层数极少对模型非常非常不利。只有一层的话，你哪儿也去不了，那是非常糟糕的缩放趋势。超过一层后，实际上竞争力出人意料地提高了，尽管在每个计算水平上，更多层（至少在这个案例中）表现更好。

And if you can do a much more fine-grained study, which they do in Kaplan, where you try to identify what you might call scale-invariant quantities, like the aspect ratio. The number of layers is not a scale-invariant quantity. As you make your model bigger, you do want more layers. But as you make your model bigger, maybe the aspect ratio, the optimal one should stay the same. This one is scale invariant. And so if we look at the aspect ratio, we see that at different model sizes, we get basically the same minima around 100 d_model for every layer, or maybe a little bit less. And it does shift a little bit right. But for the most part, the minima stays roughly similar.

如果你能做更细粒度的研究——就像Kaplan论文中那样——尝试识别所谓的"缩放不变"量，比如宽度比。层数不是一个缩放不变的量，随着模型变大，你确实需要更多层。但模型变大时，最优宽度比可能应该保持不变——这是缩放不变的。如果我们看宽度比，会发现不同模型大小下，我们基本上得到相同的最小值，大约是每层100个d_model，或略少一些。确实有一点点右移，但大部分情况下最小值大致相似。

### 5.3 The Critical Batch Size / 临界批大小

One thing that's important, and this is a huge can of worms, is that not all parameters are created equal. And because not all parameters are created equal, your scaling laws may look good or bad depending on how you define what a parameter is. So in the Kaplan paper, they made this observation that if they drew their scaling laws for depth with the embedding parameters, they got these very funky-looking scaling laws, and they said, "Oh, this is no good at all." Because it's no good at all, they decided that they were going to exclude all the embedding parameters, and they were only going to count the non-embedding parameters because you could justify it to yourself, saying these are the parameters that are doing computation or whatever.

有一点很重要——这是一个巨大的坑——并非所有参数都是平等的。正因为并非所有参数平等，你的缩放定律看起来可能是好是坏，取决于你如何定义"参数"。在Kaplan论文中，他们观察到如果用包含嵌入参数的方式来画深度缩放定律，会得到非常奇怪的缩放定律，他们说"这完全不行"。因为完全不行，他们决定排除所有嵌入参数，只计算非嵌入参数——你可以自我辩解这些才是真正在做计算的参数。

The point here is scaling laws aren't magic. Scaling laws and all these kinds of predictability across scales is engineered. They don't happen automatically. We need to pick the right kinds of x-axes to look at. We need to make sure that the hyperparameters for these things are set right, and only under those conditions does it become possible to get predictable scaling across many orders of magnitude of compute.

关键在于：缩放定律不是魔法。缩放定律以及所有这些跨规模的可预测性是工程化的结果，它们不会自动发生。我们需要选择正确类型的x轴，需要确保这些东西的超参数设置正确，只有在这种条件下，才有可能在多个数量级的计算跨度上获得可预测的缩放。

Now, batch size is very tricky. We want the batch size to be as big as possible because a big batch size gives us opportunity for parallelization. Remember, data parallel requires large batch size. So having said all that, what we really want to is how large can we make our batch size before we start to suffer? That's the relevant systems question. And you also want to know how does that change as a function of model size. Given that preface, there is this very important idea that is used in a variety of papers and talked about very frequently, called the critical batch size.

批大小非常棘手。我们希望批大小尽可能大，因为大批大小为并行化提供了机会——记住，数据并行需要大批大小。所以说了这么多，我们真正想知道的是：在开始受到损害之前，批大小可以设多大？这是相关的系统问题。你还需要知道这如何随模型大小变化。在此铺垫下，有一个非常重要的概念被各种论文频繁使用和讨论，那就是临界批大小（critical batch size）。

The critical batch size is roughly this idea that up until a certain point, when you start to get diminishing returns, there is perfect returns to increased batch size. So I might call this the noise-limited regime. In the noise-limited regime, every additional element that you throw in your batch reduces the gradient noise in your SGD step. And since you're variance-limited, that reduction in variance is very, very helpful. That gives you big returns. So this is the regime in which you have perfect scaling. You're doing about as well as you can, given the amount of extra examples that you're processing.

临界批大小的大致思想是：在某一点之前——即你开始遇到递减回报之前——增大批大小会带来完美的回报。我称之为噪声受限区（noise-limited regime）。在噪声受限区中，你投入批中的每个额外样本都会减少SGD步骤的梯度噪声。由于你受限于方差，这种方差的减少非常非常有帮助，给你带来巨大回报。所以在这个区域内你有完美的缩放——在给定处理额外样本数量的前提下，你做得差不多是最好的。

As you get to a certain point where you've reached the noise scale of your gradients, you get to a point where you are no longer variance-limited. You're now bias-limited. What does that mean? Well, remember, in gradient descent, you're looking at the local structure of your objective. You don't have a global view of where the minimum is. So no matter how low noise I am, there's always a disagreement between my local descent direction and where the global optimum is. Because of that, at a certain point, I'm going to get diminishing returns because now my limiting factor is no longer variance. It is this bias term. So now I'm bias-limited past this point.

当你到达某个点，达到了梯度的噪声尺度时，你就不再受限于方差了，你现在受限于偏差（bias-limited）。这是什么意思？记住，在梯度下降中，你看到的是目标函数的局部结构。你没有全局视野知道最小值在哪里。所以不管我噪声多低，我的局部下降方向与全局最优之间总有不一致。正因如此，在某一点之后，我会遇到递减回报，因为现在限制因素不再是方差，而是偏差项。所以过了这一点，我就处于偏差受限状态。

And so critical batch is kind of a rule of thumb, you might call it, or a convenient trade-off point where you say this is the point at which we're starting to cross over from our perfect scaling regime to our ineffective scaling regime. And so it gives you a good rule of thumb of where to be setting your batch size if you want your batch size to be as big as possible without suffering these huge efficiency losses.

所以临界批大小可以说是一种经验法则，或者一个方便的权衡点：在这个点上，我们开始从完美缩放区过渡到无效缩放区。它给了你一个很好的经验法则：如果你想让批大小尽可能大而又不遭受巨大的效率损失，应该把批大小设在哪里。

### 5.4 Learning Rate Scaling / 学习率缩放

The learning rate side of the story is also a little bit complicated. I'll go into this in much more detail in the advanced scaling lecture. But learning rates generally shift. Let's say that you have just a MLP, just a standard neural network of some kind. I'm not going to do depth scaling. I'm only going to do width scaling. Now, if I'm doing width scaling, the bigger my model, the smaller my learning rate should be. And the reason why my learning rate should be smaller is because I have bigger, more parameters, I'm changing more things at once. Maybe I should move less. It kind of makes sense. And in fact, there's a rule of thumb that maybe you want to scale by 1 over the width. That's a very commonly known rule of thumb that you want to just decrease the learning rate regularly as a function of your width, and that will give you a rule of thumb to scale your learning rate.

学习率方面的情况也有些复杂。我将在高级缩放定律讲座中更详细地展开。但学习率通常是变化的。假设你只有一个MLP，某种标准神经网络。我不做深度缩放，只做宽度缩放。如果做宽度缩放，模型越大，学习率应该越小。学习率应该更小的原因是参数更多，你同时改变了更多东西，也许应该移动得更少——这有些道理。事实上，有一条经验法则：你可能想按1/宽度来缩放。这是一个广为人知的经验法则：你想要作为宽度的函数规律性降低学习率，这会给你一个缩放学习率的经验法则。

There is another school of thought, or another set of tricks that people do, which is that people also rescale the network in various ways. They will change the initialization sizes, and they will change the step sizes of the optimizer for various parts of the network in order to force the model to have the same learning rate minimum across scales. And this is an idea that is called muP and others like it. Some people have reported great success with these kinds of approaches, others have reported less success.

还有另一派思想，或者说另一套技巧：人们以各种方式重新缩放网络。他们会改变初始化大小，改变优化器对网络不同部分的步长，以迫使模型在不同规模下具有相同的学习率最小值。这就是被称为μP（最大更新参数化）等类似方法的思想。有些人对这些方法报告了很好的成功，另一些人则报告了较少的成功。

The two ways, basically, of setting a learning rate for large-scale runs really is captured in this plot. In one way, you can try to estimate what these minima are and try to predict what your minimum will be. And the way in which the minimum changes is pretty predictable, so this is not a crazy idea. Or you can reparameterize your model to try to keep the learning rate minimum the same, and then just pick your best learning rate and go. Those are the two philosophies to picking your learning rate. Both of them have been applied successfully at scale.

为大规模训练设置学习率的两种方式大致可以概括为：一种方式是尝试估计这些最小值在哪里，并预测你的最小值会是多少——最小值的变化方式相当可预测，所以这不是疯狂的想法。或者你可以重新参数化你的模型，试图保持学习率最小值不变，然后直接选最佳学习率即可。这就是选择学习率的两种哲学。两者都在大规模下被成功应用过。

## 6. Upstream vs. Downstream Performance / 上游与下游性能

So before I get into the last part of this lecture, one thing I want to end this section with is the idea that upstream and downstream performance can be quite different. So if you look at something like log likelihood, you find that perplexity and negative perplexity in this case parameters are very correlated. The more parameters you have, the better your model, very predictably. This is a very beautiful linear trend. Now you're like, OK, this is great. Now we're going to ship our best model. NL12. Turns out NL12 is not your best model. It was actually NL32XL, which was a much worse model in perplexity. This is a very common thing that does happen.

在进入本讲最后一部分之前，我想以这样一个想法来结束本节：上游和下游性能可能差异很大。如果你看对数似然之类的指标，你会发现困惑度与参数量高度相关。参数越多模型越好，非常可预测——这是一条非常优美的线性趋势。然后你说，太好了，我们就发布最好的模型NL12吧。结果NL12并不是你最好的模型，实际上是NL32XL，而它在困惑度上差得多。这是经常发生的事情。

Upstream and downstream are often correlated. This is probably one of the worst correlations that I've seen from upstream to downstream. But I think it's very, very important to remember that scaling laws, generally speaking, are objects that you want to apply on the perplexity side. They're very clean, they're very regular, they're very predictable. But transfer from perplexity to downstream is a lot less certain than it might initially seem. This is a place where you want to be very cautious.

上游和下游通常是相关的。这可能是我见过的从上游到下游最差的相关性之一。但我认为非常非常重要的一点是：缩放定律一般而言是你想要应用在困惑度方面的对象。它们非常干净、非常规律、非常可预测。但从困惑度到下游任务的迁移，比最初看起来要不确定得多。这是一个需要非常谨慎的地方。

And as an anecdote, I have former students that have gone and done post-training at various places, and they always complain. They're like, "Oh, those pre-training people, they hand you this model. They are like, the perplexity is good. It's all your problem now." But it's often the problems have started at the pre-training side.

作为趣闻，我有一些以前的学生去各个地方做后训练（post-training），他们总是抱怨："那些预训练的人，他们把模型交给你，说困惑度很好，现在都是你的问题了。"但问题往往在预训练阶段就已经开始了。

So the scaling law-based procedure is to say I'm going to train a bunch of smaller models, I'm going to establish some scaling law by fitting these lines onto log-log plots. And then if the fit is good enough, I'm going to have some confidence that the gap will persist, and then I'm just going to deploy that onto my large-scale training run. This is the naive version of a scaling law procedure, but I think one that is reasonably accurate for how you might think about these things in practice. What else are you going to do? Just deploy a run out of nowhere? Probably not.

所以基于缩放定律的流程是：训练一堆较小的模型，通过在对数-对数图上拟合这些直线来建立缩放定律。如果拟合足够好，你就有信心差异会持续存在，然后直接将其部署到大规模训练运行中。这是缩放定律流程的朴素版本，但我认为对于在实践中如何思考这些事情，这是相当准确的。你还有什么其他办法？凭空部署一轮训练？可能不会。

## 7. The Chinchilla vs. Kaplan Debate / Chinchilla与Kaplan之争

### 7.1 Compute-Optimal Scaling / 计算最优缩放

OK, now I'm going to talk about one of the most well-known uses of a scaling law. Even though you might not personally be using this, you've certainly used the rule of thumb at some point. And also, I think because this set of things will tell us something really interesting about the actual execution of a scaling law. The motivating question is, do I want more data or bigger models? The resource that you have to spend is compute. Someone's going to hand you metaphorically a certain amount of FLOPs. And you're going to take those FLOPs, and you're going to spend them somehow. If you remember Percy's very first lecture, it's going to be data times the parameters is roughly your FLOPs, linear in that. So do I want more data or more models?

现在我要讨论缩放定律最著名的应用之一。即使你自己可能没有用过它，你肯定在某个时候用过这条经验法则。而且我认为这一系列内容会告诉我们一些关于缩放定律实际执行的非常有趣的事情。核心问题是：我需要更多数据还是更大的模型？你需要花费的资源是计算量。有人会隐喻性地给你一定数量的FLOPs，你要把这些FLOPs以某种方式花费掉。如果你记得Percy的第一讲，大概是数据量乘以参数量约等于FLOPs，是线性的。那么我该要更多数据还是更大模型？

Well, we know that if we take a teeny tiny model and we dump tons of data into it, that will just be wasted. I've taken a teeny tiny language model, and I've passed a huge amount of data into it, and this thing has been flat for a very long time. This is a complete waste of compute. You would have much rather trained this big yellow model to the same amount of tokens or even earlier on, if you're having the same amount of compute. Now, if you could understand the interaction of how data amount and model size come together to give you performance, if you understood that relationship, you could optimize this very precisely.

我们知道如果拿一个极小的模型然后往里塞海量数据，那纯粹是浪费。我拿了一个极小的语言模型，喂了巨量数据进去，结果很长一段时间都平平无奇——这是对计算资源的完全浪费。在同样的计算量下，你宁愿训练这个大的黄色模型到同样数量的token，甚至更早时候就停下来。现在，如果你能理解数据量和模型大小如何相互作用来产生性能，理解了这种关系，你就能非常精确地优化这一点。

And so there are scaling laws that are more advanced and relate kind of joint behaviors of objects. So almost simultaneously, Kaplan and Rosenfeld both proposed these functional forms, which are roughly equivalent, describing how the size of the model and the amount of data relate to the error. Rosenfeld is very simple. It's really just the sum of two inverse terms. These are two scaling laws that are added together. And Kaplan is a little bit more complicated, but it's roughly the same idea. And if you look at, think about the limits, this is very intuitive. If I have an infinite amount of data, then what happens? Then you're basically model-size limited. You become a pure model size scaling law. If I send my model size to infinity, then I'm going to be bounded by data. I'm going to have a pure data scaling law. So it makes sense if you take the limits of both of these. It's often a good idea if someone tells you a scaling law to take the limits of all the variables to understand the behavior of the system.

因此有更高级的缩放定律来描述对象的联合行为。几乎同时，Kaplan和Rosenfeld分别提出了大致等价的函数形式，描述模型大小和数据量如何与误差相关。Rosenfeld的非常简单，就是两个逆项之和——两条缩放定律相加。Kaplan的稍微复杂一些，但大致是同一个思路。如果你思考极限，这非常直观。如果我有无限数据会怎样？那你基本上受限于模型大小，变成一条纯模型大小缩放定律。如果我把模型大小推向无穷，就会被数据所限，变成一条纯数据缩放定律。所以如果你对两者取极限，这很合理。如果有人告诉你一条缩放定律，取所有变量的极限来理解系统行为往往是个好主意。

Now, both Kaplan and Rosenfeld provide equations of this form. What do they say? Well, if you look at Kaplan, they solve for this equation, they say something like this. Well, the amount of data should be C to the 0.73, and the amount of model size should be C to the 0.27. N should be the amount of parameters and D should be the amount of data. And so tokens per parameters decreases with C. So as you increase the compute amounts, this prescription by Kaplan tells you to train bigger and bigger and bigger models.

Kaplan和Rosenfeld都提供了这种形式的方程。Kaplan求解后说：数据量应该为C的0.73次方，模型大小应该为C的0.27次方。N是参数量，D是数据量。所以token与参数之比随C递减。当你增加计算量时，Kaplan的这个处方告诉你训练越来越大、越来越大的模型。

But a few years later, in 2022, some folks at DeepMind, Hoffman et al., came in and they said, well, actually, these predictions are all terribly off. You've been training these giant models, these three stars over here, but actually, those are way too big. What we should be training instead is a very different trend, this line on the blue over here, and we should be training this teal star, which is a much better model. So they argued that we should be training much smaller models relative to this. And I think, of course, many of you or all of you probably know the Chinchilla paper, you know what the token multipliers are. It's 20 tokens to every parameter.

但几年后，在2022年，DeepMind的Hoffman等人提出：实际上，这些预测全都严重偏离了。你们一直在训练这些巨型模型（这三个星号），但实际上它们太大了。我们应该训练的是一个截然不同的趋势——蓝色这条线，训练这个青色星号，这是一个好得多的模型。因此他们认为我们应该训练比这小得多的模型。当然，你们中的许多人或所有人可能都知道Chinchilla论文，知道token乘数是多少——每个参数20个token。

### 7.2 Why Did Kaplan and Chinchilla Disagree? / Kaplan和Chinchilla为何不一致？

So the Chinchilla author suggests three different ways of fitting scaling laws. I really like this because it's a way of robustifying yourself to modeling assumptions you may have made. And each of these actually is quite a different approach to estimating the trade-off between model size and data. Method 1 is what I might call the lower envelope method. What you do is you take all of your training runs. So each one of these colored lines is a training curve. And what you want to do is you want to actually take the lower envelope of these training curves. Because a lower envelope point on this training curve, that means that for a particular FLOP, this is the best loss that I ever achieved for that FLOP on any training run.

Chinchilla作者提出了三种不同的拟合缩放定律的方法。我非常欣赏这一点，因为这是让你对可能做出的建模假设更稳健的一种方式。每种方法实际上都是估计模型大小与数据之间权衡的相当不同的方法。方法一：我称之为下包络法（lower envelope method）。你取所有训练运行——每条彩色线都是一条训练曲线。你要做的是取这些训练曲线的下包络。因为训练曲线上的下包络点意味着：对于特定的FLOP量，这是我在任何训练运行中为该FLOP量取得的最佳损失。

Method 2 is IsoFLOP. This is now very popular. It's also very easy and very robust. This is probably my personal favorite method. And what you do is, for this, you pick a bunch of different FLOPS budgets. And for each FLOP budget, you're going to essentially sweep the space. So here I have one variable, which is the parameter-to-data trade-off. So for each FLOP budget, I'm going to sweep over the parameter to data trade-off, fixing my FLOPS. So I double my data size, I half my model size, so on and so forth. And that will generate a sequence of training runs whose terminal loss is going to sweep out some of curve. Each one of these colored sets of points is a fixed FLOP run. Each point is sweeping across different parameters, and of course, it's implicitly sweeping over data as well.

方法二是等FLOP曲线（IsoFLOP）。现在这个方法非常流行，也非常简单、非常稳健。这可能是我个人最喜欢的方法。做法是：选取一系列不同的FLOP预算，比如按1、3、6等倍数排列。对于每个FLOP预算，你在空间中扫描——这里只有一个变量，即参数与数据的权衡。所以对于每个FLOP预算，固定FLOP量，扫描参数与数据的权衡：数据量加倍，模型大小减半，以此类推。这会产生一系列训练运行，其终端损失会扫出一条曲线。每组彩色点对应一个固定FLOP量的运行，每个点是不同参数的扫描，当然也隐含地在扫描数据。

The nice thing now is I can take the minimum over each of these runs, or even fit a quadratic and take the minimum over the quadratics, and then I can draw a line through all of the bottoms of the quadratics, and plot them as a function of FLOPS to parameters. And that will give me another prediction.

好的一点是：我可以取每次运行的最小值，或者甚至拟合一个二次函数并取二次函数的最小值，然后穿过所有二次函数底部画一条直线，将它们作为FLOP到参数的函数绘制出来。这会给出另一个预测。

Method 3 is the brute-force way. You have a hypothesized relationship between loss, data size, and model size. Train a bunch of models, do curve fitting. Hopefully, fairly straightforward—how you do that. Of course, if you're doing this method, how you do the curve fitting is very important. Now, you're fitting these surfaces, there's many variables, it's kind of tricky.

方法三是蛮力方式。你假设损失、数据大小和模型大小之间存在一个关系。训练一堆模型，做曲线拟合。希望这个过程是相当直接的。当然，如果使用这种方法，曲线拟合的方式非常重要——你在拟合这些曲面，有很多变量，相当棘手。

So now that we've gone through what Chinchilla does, it doesn't seem materially different than what Kaplan was doing. It's not like Kaplan was doing one crazy thing and then the Chinchilla authors did something way smarter. They both did pretty reasonable stuff. But if we look at their scaling predictions, they are very different. And in hindsight, we generally tend to agree with the fact that the Chinchilla authors had more of the correct scaling.

现在我们了解了Chinchilla的做法，它似乎与Kaplan所做的没有本质区别。并不是说Kaplan做了一件疯狂的事，然后Chinchilla作者做了更聪明的事——两者都做了相当合理的事。但如果看它们的缩放预测，差异非常大。事后看来，我们普遍倾向于认同Chinchilla作者更接近正确的缩放。

So why is there such a big difference when they're both fitting these joint scaling laws? OK, so this is where we get into the messy realities of how scaling laws are made. Scaling laws can really change depending on the precise ways in which you're implementing the scaling laws, the hyperparameter settings that you're using, and even what the x-axis is.

那么为什么两者都在拟合联合缩放定律，却有如此大的差异？这就是我们进入缩放定律制作过程中混乱现实的地方。缩放定律确实可以因为你实施缩放定律的精确方式、你使用的超参数设置，甚至x轴是什么而改变。

There's a really nice paper called "Resolving Discrepancy to Compute-Optimal Scaling of Language Models." And they show—basically, first they replicate the Kaplan result using roughly the Kaplan settings. And then they say, OK, well, let's change how we count parameters. That shifts the curve a little bit. And then they say, OK, well, let's change how learning rate warmup is done. That shifts the curve a little bit. And then let's tune the optimizer a little bit more. And then they get exactly the Chinchilla result. So their argument here is that there is a sequence of what seems very minor decisions that in the end, gives you this big gap between the Kaplan scaling law and the Chinchilla scaling law.

有一篇非常好的论文叫"Resolving Discrepancy to Compute-Optimal Scaling of Language Models"。他们展示了：首先用大致Kaplan的设置复制了Kaplan结果。然后说好，让我们改变参数的计数方式——曲线就偏移了一点点。然后改变学习率预热的方式——曲线又偏移了一点点。再微调一下优化器——然后他们得到了完全一致的Chinchilla结果。所以他们的论证是：一连串看似非常微小的决策，最终导致了Kaplan缩放定律和Chinchilla缩放定律之间的巨大差距。

So the very first arrow is how we count parameters. Remember, in Kaplan, they excluded embedding parameters. That's generally an OK thing to do. But one thing they also did that really messed them up was they also excluded the last layer parameter counts, the softmax ones. Because in many models, the embedding and the last layer linear are dual to each other. They have the same shapes. And because they're the same shape, they said, well, let's just exclude both of those. It turns out whether you include or exclude those has a big material impact on the shape of the scaling law.

第一个差异是参数计数方式。记住，在Kaplan中，他们排除了嵌入参数——这通常是可以的。但他们还做了一件把事情搞砸的事：也排除了最后一层的参数计数，即softmax层的参数。因为在许多模型中，嵌入层和最后的线性层是对偶的，形状相同——都是词表大小×隐藏维度以及隐藏维度×词表大小。因为形状相同，他们说干脆两都排除。结果是，包含还是排除这些参数，对缩放定律的形状有重大的实际影响。

They also found that a lot of the models that were being trained in Kaplan were very small. And in fact, they were so small that they were not actually converging by the time that the learning rate warm up was done. So their learning rates were set very suboptimally. And because of that, their models weren't fully converged. And then finally, they found that Kaplan et al. was fixing one big batch size, and those big batch sizes were suboptimal for the smaller models. And therefore, if you tune that correctly and you use varying batch sizes, you end up getting this thing that agrees exactly with Chinchilla.

他们还发现Kaplan中训练的许多模型都非常小。事实上它们小到在学习率预热完成时还没有真正收敛。所以它们的学习率设置得非常次优，因此模型没有完全收敛。最后，他们发现Kaplan等人固定了一个大批大小，而这些大批大小对于较小的模型来说是次优的。因此，如果你正确调优并使用变化的批大小，最终会得到与Chinchilla完全一致的结果。

So I think each of these might seem like a very minor difference, but if you change up these really minor differences, you can get big shifts in the scaling law. And one thing I like to emphasize is that scaling laws are lower bounds in some sense. They're kind of saying, if I continue this recipe and I scale it up, then this is what I will get. But if you're scaling up a recipe that you don't want to scale up—your warmup is kind of crazy, or your batch sizes are crazy—you're going to get bad scaling laws. So you want to be as close to the proper full run as possible.

所以这些每一个看起来可能都是非常微小的差异，但如果你改变了这些真正微小的差异，缩放定律就会发生巨大的偏移。我想强调的一点是：缩放定律在某种意义上是下界。它们好像在说："如果我继续这个配方并扩大规模，这就是我会得到的。"但如果你在扩大一个你不该扩大的配方——预热策略有些疯狂，或批大小设置不合理——你就会得到糟糕的缩放定律。所以你想尽可能地接近正确的全量运行。

### 7.3 Beyond Chinchilla: Overtraining for Inference / 超越Chinchilla：为推理而"过度训练"

OK, so that's the end of the Chinchilla saga in some ways. But I will end this section by saying you probably don't want the Chinchilla factor. At this point, I think this is a pretty common knowledge thing. But if you're training a production model, you don't really care about saving training compute for the most part. Most of the compute is not going into training runs. Most of the compute is actually going into R&D and serving. And given that, especially for serving, what you want to do is you want small models that are capable. You do not want big, bloated models that cost a lot to serve, even if that minimizes training cost. And so what you really want is something that you would call "overtrained." I put that in quotes because, really, overtraining is what we want. That's the right amount of training.

这在某种意义上就是Chinchilla传奇的结尾。但我将以这样说结束本节：你可能并不想要Chinchilla因子。在这一点上，我认为这已经是相当普遍的共识。如果你在训练一个生产级模型，你大部分情况下并不真正关心节省训练计算量。大部分计算量并没有进入训练运行，而是进入了研发和推理服务。考虑到这一点，特别是对于推理服务，你需要的是能力强的小模型。你不想要庞大臃肿、服务成本极高的模型，即使它能最小化训练成本。所以你真正想要的是所谓的"过度训练"——我打引号是因为实际上，"过度训练"正是我们在推理场景下想要的正确训练量。

And if you look at all the models that were released in the early days, like GPT-3—this was under-trained for sure, three tokens per parameter. Chinchilla gets to the modern ratio of 20 per parameter. And then for a while, people were at 20 per parameter. And this is the era where there wasn't that much serving of these models. The models were cool, but it wasn't being served at scale. And then as you start to move to eras where serving becomes very real, now you're overtraining these models, and now you've moved into MoEs, and you're making all these trade-offs to optimize inference serving.

如果你看早期发布的所有模型，比如GPT-3——毫无疑问是训练不足的，每个参数仅3个token。Chinchilla达到了现代的比例——每个参数20个token。然后有一段时间，人们保持在每个参数20个token。那是这些模型还没有大规模推理服务的时代——模型很酷，但没有大规模服务。然后随着你进入推理服务变得非常真实的时代，现在你开始"过度训练"这些模型，进入了MoE（混合专家模型）时代，做出各种权衡来优化推理服务。

## 8. Key Lessons for Scaling Law Practice / 缩放定律实践的关键教训

IsoFLOP have been one of the things that have endured as a research tool. IsoFLOP are very easy to execute. You fix a FLOPS budget, and then you sweep over all of the other degrees of freedom to see what the surface looks like. And this gives you, in general, fairly reliable readings of how different parameters vary as a function of your free parameters. People have done this for diffusion models. The MoE study I talked about was an IsoFLOP-style design. If you're ever in a situation where you're thinking, how am I going to decide all these trade-offs, IsoFLOP is always a good default.

等FLOP曲线（IsoFLOP）是作为研究工具经久不衰的事物之一。IsoFLOP非常容易执行：你固定一个FLOP预算，然后扫描所有其他自由度来观察曲面长什么样。这通常能给你相当可靠的读数——理解不同参数如何作为自由参数的函数而变化。人们已经为扩散模型做过类似的研究，我提到的MoE研究也是IsoFLOP风格的设计。如果你遇到不知道如何决定这些权衡的情况，IsoFLOP总是一个好的默认选择。

## 9. Summary / 总结

So to wrap up everything for today, there's this idea that we have this log-linear regularity between the amount of resources we put in and the performance we get out. And it extends to a wide variety of things—model parameters, compute, sparsity level of your MoE. And that lets you do a lot of the things that I was talking about earlier as arbitrary choices, but do it in a much more evidence-driven way, hopefully. And so this allows us to have engineering at scale without explicitly relying on doing big model training runs.

总结今天的所有内容：我们观察到投入的资源量与产出的性能之间存在对数-线性规律。这一规律广泛适用于各种事物——模型参数、计算量、MoE的稀疏度等。这让你可以用一种更有据可依的方式来处理我之前提到的那些"随意选择"，不必明确依赖于大规模模型训练运行就能进行规模化工程。

And hopefully, you remember the different components here. Data scaling is this very natural object, just the exponent is a little bit strange. Model scaling allows you to do all these cool engineering things. And then finally, scaling is this very cool, robust predictor for how to try to do engineering at a large scale.

希望你们记住了这里的不同组成部分。数据缩放是一个非常自然的对象，只是指数有点奇怪。模型缩放让你能够做所有这些酷炫的工程化事情。最后，缩放是一种非常酷、非常稳健的预测器，指导你如何在大规模下进行工程实践。
