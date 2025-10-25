# 概率论和数理统计

[学在浙大](https://courses.zju.edu.cn/course/90303/content#/)

- 预修课程: 微积分一、二, 要求会二重积分的计算;
- 课程教材: 概率论与数理统计 (第二版), 高等教育出版社, 2023;
- 联系方式: hwmath2003@zju.edu.cn;
- 资源分享: 学在浙大、钉钉群 (原始课件、作业本编号、作业题号、上课课件);
- 线上参考资源: 中国大学 MOOC (概率论与数理统计—浙大班 SPOC, 第十期);  
  https://www.icourse163.org/spoc/learn/ZJU-1206351805  
  智慧树 (高等数理统计)  
  (注: 需待第三轮选课结束, 确定教学班名单后方能进入学习, 后续再通知)
- 成绩构成: 平时成绩 60% (包括作业及到课率等平时表现, 小测, 课程大作业, 等等) + 期末考试成绩 40%  
  总评成绩说明: 期末考试成绩设置最低分, 低于期末最低分或总评低于 60 均为不及格.

2025/10/21 11:04 提到：小测如果不提前通知，则是开卷的，能使用电子设备。如果提前通知，不能用电子设备，可以携带纸质资料。

----

- [Chapter 1 Introduction to Probability](./L1) · [Raw PPT for reference](./L1-raw)
- [Chapter 2 Random Variables and Distributions](./L2) · [Raw PPT for reference](./L2-raw)
- [Chapter 3 Multivariate Random Variables and Their Distributions](./L3) · [Raw PPT for reference](./L3-raw)



---

AI PPT提取prompt:

```
你是一个专业的PDF内容提取助手。
现在需要你提取PDF内容转为Markdown+LaTeX形式：
你必须仔细分析PDF每一页存在的重复性内容，如果它们是页头、页尾、页码等则应删去
对于应该以列表呈现的内容，你应该用Markdown中的列表语法写。
对于应该写成表格的内容，你应该使用Markdown中的表格语法。
对于数学公式，你应当使用"$...$"语法写。
对于图片，你只需要用类似![](image)的占位符来表示即可。
对于Example, Definition等类型的内容，请你将对应的部分完整包括在<Card type="type" title="...">...</Card>中。
你不需要概括内容，不需要提取关键词，不应该改变原文内容。除非上述情况，你的输出应当与原文无异。
```

------

概统作业prompt:

1. 
```
提取图片/文档中的内容写成LaTeX形式。
请注意：你无需做提炼或总结；除非是明显的错别字、排版错误，否则你输出的内容应当与给出的内容相同；应当用数学公式的部分，如数字、公式等需用"$...$"包裹；使用enumerate环境写列表；使用table环境写表格。
示例：
\begin{homework}
(习题二 B29). 设甲、乙两厂生产的同类型产品寿命（单位：年）分别服从参数为 $\frac{1}{3}$ 和 $\frac{1}{6}$ 的指数分布，将两厂的产品混在一起，其中甲厂的产品数占 40\%。现从这批混合产品中随机取一件。

\begin{enumerate}
    \item 求该产品寿命大于 6 年的概率；
    \item 若已知取到的是甲厂产品，在已用了 4 个月没有坏的条件下，求其用到 1 年还不坏的概率；
    \item 在该产品已用了 4 个月没有坏的条件下，求其用到 1 年还不坏的概率。
\end{enumerate}

\end{homework}
```

2. 
```
解答这道概率论与数理统计试题。将解答写成LaTeX形式。请注意适当使用enumerate环境写列表。以\textbf{解：}开头。
```

---

```
接下来的开卷考试允许携带cheatsheet，请你基于该文档整理
```