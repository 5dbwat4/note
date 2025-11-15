# 附录IV 积分表

### （一）含有 $ ax + b $ 的积分
1. $ \int \frac{\mathrm{d}x}{ax + b} = \frac{1}{a} \ln |ax + b| + C $
2. $ \int (ax + b)^\mu \mathrm{d}x = \frac{1}{a(\mu + 1)}(ax + b)^{\mu + 1} + C \ (\mu \neq -1) $
3. $ \int \frac{x}{ax + b}\mathrm{d}x = \frac{1}{a^2}(ax + b - b\ln |ax + b|) + C $
4. $ \int \frac{x^2}{ax + b}\mathrm{d}x = \frac{1}{a^3}\left[ \frac{1}{2}(ax + b)^2 - 2b(ax + b) + b^2\ln |ax + b| \right] + C $
5. $ \int \frac{\mathrm{d}x}{x(ax + b)} = -\frac{1}{b}\ln \left| \frac{ax + b}{x} \right| + C $
6. $ \int \frac{\mathrm{d}x}{x^2(ax + b)} = -\frac{1}{bx} + \frac{a}{b^2}\ln \left| \frac{ax + b}{x} \right| + C $
7. $ \int \frac{x}{(ax + b)^2}\mathrm{d}x = \frac{1}{a^2}\left( \ln |ax + b| + \frac{b}{ax + b} \right) + C $
8. $ \int \frac{x^2}{(ax + b)^2}\mathrm{d}x = \frac{1}{a^3}\left( ax + b - 2b\ln |ax + b| - \frac{b^2}{ax + b} \right) + C $
9. $ \int \frac{\mathrm{d}x}{x(ax + b)^2} = \frac{1}{b(ax + b)} - \frac{1}{b^2}\ln \left| \frac{ax + b}{x} \right| + C $

### （二）含有 $ \sqrt{ax + b} $ 的积分
10. $ \int \sqrt{ax + b}\mathrm{d}x = \frac{2}{3a}\sqrt{(ax + b)^3} + C $
11. $ \int x\sqrt{ax + b}\mathrm{d}x = \frac{2}{15a^2}(3ax - 2b)\sqrt{(ax + b)^3} + C $
12. $ \int x^2\sqrt{ax + b}\mathrm{d}x = \frac{2}{105a^3}(15a^2x^2 - 12abx + 8b^2)\sqrt{(ax + b)^3} + C $
13. $ \int \frac{x}{\sqrt{ax + b}}\mathrm{d}x = \frac{2}{3a^2}(ax - 2b)\sqrt{ax + b} + C $
14. $ \int \frac{x^2}{\sqrt{ax + b}}\mathrm{d}x = \frac{2}{15a^3}(3a^2x^2 - 4abx + 8b^2)\sqrt{ax + b} + C $
15. $ \int \frac{\mathrm{d}x}{x\sqrt{ax + b}} = \begin{cases} \frac{1}{\sqrt{b}}\ln \left| \frac{\sqrt{ax + b} - \sqrt{b}}{\sqrt{ax + b} + \sqrt{b}} \right| + C \ (b > 0) \\ \frac{2}{\sqrt{-b}}\arctan \sqrt{\frac{ax + b}{-b}} + C \ (b < 0) \end{cases} $
16. $ \int \frac{\mathrm{d}x}{x^2\sqrt{ax + b}} = -\frac{\sqrt{ax + b}}{bx} - \frac{a}{2b}\int \frac{\mathrm{d}x}{x\sqrt{ax + b}} $
17. $ \int \frac{\sqrt{ax + b}}{x}\mathrm{d}x = 2\sqrt{ax + b} + b\int \frac{\mathrm{d}x}{x\sqrt{ax + b}} $
18. $ \int \frac{\sqrt{ax + b}}{x^2}\mathrm{d}x = -\frac{\sqrt{ax + b}}{x} + \frac{a}{2}\int \frac{\mathrm{d}x}{x\sqrt{ax + b}} $

### （三）含有 $ x^2 \pm a^2 $ 的积分
19. $ \int \frac{\mathrm{d}x}{x^2 + a^2} = \frac{1}{a}\arctan \frac{x}{a} + C $
20. $ \int \frac{\mathrm{d}x}{(x^2 + a^2)^n} = \frac{x}{2(n - 1)a^2(x^2 + a^2)^{n - 1}} + \frac{2n - 3}{2(n - 1)a^2}\int \frac{\mathrm{d}x}{(x^2 + a^2)^{n - 1}} \ (n > 1) $
21. $ \int \frac{\mathrm{d}x}{x^2 - a^2} = \frac{1}{2a}\ln \left| \frac{x - a}{x + a} \right| + C $

### （四）含有 $ ax^2 + b \ (a > 0) $ 的积分
22. $ \int \frac{\mathrm{d}x}{ax^2 + b} = \begin{cases} \frac{1}{\sqrt{ab}}\arctan \sqrt{\frac{a}{b}}x + C \ (b > 0) \\ \frac{1}{2\sqrt{-ab}}\ln \left| \frac{\sqrt{a}x - \sqrt{-b}}{\sqrt{a}x + \sqrt{-b}} \right| + C \ (b < 0) \end{cases} $
23. $ \int \frac{x}{ax^2 + b}\mathrm{d}x = \frac{1}{2a}\ln |ax^2 + b| + C $
24. $ \int \frac{x^2}{ax^2 + b}\mathrm{d}x = \frac{x}{a} - \frac{b}{a}\int \frac{\mathrm{d}x}{ax^2 + b} $
25. $ \int \frac{\mathrm{d}x}{x(ax^2 + b)} = \frac{1}{2b}\ln \frac{x^2}{|ax^2 + b|} + C $
26. $ \int \frac{\mathrm{d}x}{x^2(ax^2 + b)} = -\frac{1}{bx} - \frac{a}{b}\int \frac{\mathrm{d}x}{ax^2 + b} $
27. $ \int \frac{\mathrm{d}x}{(ax^2 + b)^2} = \frac{x}{2b(ax^2 + b)} + \frac{1}{2b}\int \frac{\mathrm{d}x}{ax^2 + b} $

### （五）含有 $ ax^2 + bx + c \ (a > 0) $ 的积分
28. $ \int \frac{\mathrm{d}x}{ax^2 + bx + c} = \begin{cases} \frac{2}{\sqrt{4ac - b^2}}\arctan \frac{2ax + b}{\sqrt{4ac - b^2}} + C \ (b^2 < 4ac) \\ \frac{1}{\sqrt{b^2 - 4ac}}\ln \left| \frac{2ax + b - \sqrt{b^2 - 4ac}}{2ax + b + \sqrt{b^2 - 4ac}} \right| + C \ (b^2 > 4ac) \end{cases} $
29. $ \int \frac{x}{ax^2 + bx + c}\mathrm{d}x = \frac{1}{2a}\ln |ax^2 + bx + c| - \frac{b}{2a}\int \frac{\mathrm{d}x}{ax^2 + bx + c} $

### （六）含有 $ \sqrt{x^2 + a^2} \ (a > 0) $ 的积分
30. $ \int \frac{\mathrm{d}x}{\sqrt{x^2 + a^2}} = \ln (x + \sqrt{x^2 + a^2}) + C $
31. $ \int \frac{\mathrm{d}x}{\sqrt{(x^2 + a^2)^3}} = \frac{x}{a^2\sqrt{x^2 + a^2}} + C $
32. $ \int \frac{x}{\sqrt{x^2 + a^2}}\mathrm{d}x = \sqrt{x^2 + a^2} + C $
33. $ \int \frac{x}{\sqrt{(x^2 + a^2)^3}}\mathrm{d}x = -\frac{1}{\sqrt{x^2 + a^2}} + C $
34. $ \int \frac{x^2}{\sqrt{x^2 + a^2}}\mathrm{d}x = \frac{x}{2}\sqrt{x^2 + a^2} - \frac{a^2}{2}\ln (x + \sqrt{x^2 + a^2}) + C $
35. $ \int \frac{x^2}{\sqrt{(x^2 + a^2)^3}}\mathrm{d}x = -\frac{x}{\sqrt{x^2 + a^2}} + \ln (x + \sqrt{x^2 + a^2}) + C $
36. $ \int \frac{\mathrm{d}x}{x\sqrt{x^2 + a^2}} = \frac{1}{a}\ln \frac{\sqrt{x^2 + a^2} - a}{|x|} + C $
37. $ \int \frac{\mathrm{d}x}{x^2\sqrt{x^2 + a^2}} = -\frac{\sqrt{x^2 + a^2}}{a^2x} + C $
38. $ \int \sqrt{x^2 + a^2}\mathrm{d}x = \frac{x}{2}\sqrt{x^2 + a^2} + \frac{a^2}{2}\ln (x + \sqrt{x^2 + a^2}) + C $
39. $ \int \sqrt{(x^2 + a^2)^3}\mathrm{d}x = \frac{x}{8}(2x^2 + 5a^2)\sqrt{x^2 + a^2} + \frac{3}{8}a^4\ln (x + \sqrt{x^2 + a^2}) + C $
40. $ \int x\sqrt{x^2 + a^2}\mathrm{d}x = \frac{1}{3}\sqrt{(x^2 + a^2)^3} + C $
41. $ \int x^2\sqrt{x^2 + a^2}\mathrm{d}x = \frac{x}{8}(2x^2 + a^2)\sqrt{x^2 + a^2} - \frac{a^4}{8}\ln (x + \sqrt{x^2 + a^2}) + C $
42. $ \int \frac{\sqrt{x^2 + a^2}}{x}\mathrm{d}x = \sqrt{x^2 + a^2} + a\ln \frac{\sqrt{x^2 + a^2} - a}{|x|} + C $
43. $ \int \frac{\sqrt{x^2 + a^2}}{x^2}\mathrm{d}x = -\frac{\sqrt{x^2 + a^2}}{x} + \ln (x + \sqrt{x^2 + a^2}) + C $

### （七）含有 $ \sqrt{x^2 - a^2} \ (a > 0) $ 的积分
44. $ \int \frac{\mathrm{d}x}{\sqrt{x^2 - a^2}} = \ln |x + \sqrt{x^2 - a^2}| + C $
45. $ \int \frac{\mathrm{d}x}{\sqrt{(x^2 - a^2)^3}} = -\frac{x}{a^2\sqrt{x^2 - a^2}} + C $
46. $ \int \frac{x}{\sqrt{x^2 - a^2}}\mathrm{d}x = \sqrt{x^2 - a^2} + C $
47. $ \int \frac{x}{\sqrt{(x^2 - a^2)^3}}\mathrm{d}x = -\frac{1}{\sqrt{x^2 - a^2}} + C $
48. $ \int \frac{x^2}{\sqrt{x^2 - a^2}}\mathrm{d}x = \frac{x}{2}\sqrt{x^2 - a^2} + \frac{a^2}{2}\ln |x + \sqrt{x^2 - a^2}| + C $
49. $ \int \frac{x^2}{\sqrt{(x^2 - a^2)^3}}\mathrm{d}x = -\frac{x}{\sqrt{x^2 - a^2}} + \ln |x + \sqrt{x^2 - a^2}| + C $
50. $ \int \frac{\mathrm{d}x}{x\sqrt{x^2 - a^2}} = \frac{1}{a}\arccos \frac{a}{|x|} + C $
51. $ \int \frac{\mathrm{d}x}{x^2\sqrt{x^2 - a^2}} = \frac{\sqrt{x^2 - a^2}}{a^2x} + C $
52. $ \int \sqrt{x^2 - a^2}\mathrm{d}x = \frac{x}{2}\sqrt{x^2 - a^2} - \frac{a^2}{2}\ln |x + \sqrt{x^2 - a^2}| + C $
53. $ \int \sqrt{(x^2 - a^2)^3}\mathrm{d}x = \frac{x}{8}(2x^2 - 5a^2)\sqrt{x^2 - a^2} + \frac{3}{8}a^4\ln |x + \sqrt{x^2 - a^2}| + C $
54. $ \int x\sqrt{x^2 - a^2}\mathrm{d}x = \frac{1}{3}\sqrt{(x^2 - a^2)^3} + C $
55. $ \int x^2\sqrt{x^2 - a^2}\mathrm{d}x = \frac{x}{8}(2x^2 - a^2)\sqrt{x^2 - a^2} - \frac{a^4}{8}\ln |x + \sqrt{x^2 - a^2}| + C $
56. $ \int \frac{\sqrt{x^2 - a^2}}{x}\mathrm{d}x = \sqrt{x^2 - a^2} - a\arccos \frac{a}{|x|} + C $
57. $ \int \frac{\sqrt{x^2 - a^2}}{x^2}\mathrm{d}x = -\frac{\sqrt{x^2 - a^2}}{x} + \ln |x + \sqrt{x^2 - a^2}| + C $

### （八）含有 $ \sqrt{a^2 - x^2} \ (a > 0) $ 的积分
58. $ \int \frac{\mathrm{d}x}{\sqrt{a^2 - x^2}} = \arcsin \frac{x}{a} + C $
59. $ \int \frac{\mathrm{d}x}{\sqrt{(a^2 - x^2)^3}} = \frac{x}{a^2\sqrt{a^2 - x^2}} + C $
60. $ \int \frac{x}{\sqrt{a^2 - x^2}}\mathrm{d}x = -\sqrt{a^2 - x^2} + C $
61. $ \int \frac{x}{\sqrt{(a^2 - x^2)^3}}\mathrm{d}x = \frac{1}{\sqrt{a^2 - x^2}} + C $
62. $ \int \frac{x^2}{\sqrt{a^2 - x^2}}\mathrm{d}x = -\frac{x}{2}\sqrt{a^2 - x^2} + \frac{a^2}{2}\arcsin \frac{x}{a} + C $
63. $ \int \frac{x^2}{\sqrt{(a^2 - x^2)^3}}\mathrm{d}x = \frac{x}{\sqrt{a^2 - x^2}} - \arcsin \frac{x}{a} + C $
64. $ \int \frac{\mathrm{d}x}{x\sqrt{a^2 - x^2}} = \frac{1}{a}\ln \frac{a - \sqrt{a^2 - x^2}}{|x|} + C $
65. $ \int \frac{\mathrm{d}x}{x^2\sqrt{a^2 - x^2}} = -\frac{\sqrt{a^2 - x^2}}{a^2x} + C $
66. $ \int \sqrt{a^2 - x^2}\mathrm{d}x = \frac{x}{2}\sqrt{a^2 - x^2} + \frac{a^2}{2}\arcsin \frac{x}{a} + C $
67. $ \int \sqrt{(a^2 - x^2)^3}\mathrm{d}x = \frac{x}{8}(5a^2 - 2x^2)\sqrt{a^2 - x^2} + \frac{3}{8}a^4\arcsin \frac{x}{a} + C $
68. $ \int x\sqrt{a^2 - x^2}\mathrm{d}x = -\frac{1}{3}\sqrt{(a^2 - x^2)^3} + C $
69. $ \int x^2\sqrt{a^2 - x^2}\mathrm{d}x = \frac{x}{8}(2x^2 - a^2)\sqrt{a^2 - x^2} + \frac{a^4}{8}\arcsin \frac{x}{a} + C $
70. $ \int \frac{\sqrt{a^2 - x^2}}{x}\mathrm{d}x = \sqrt{a^2 - x^2} + a\ln \frac{a - \sqrt{a^2 - x^2}}{|x|} + C $
71. $ \int \frac{\sqrt{a^2 - x^2}}{x^2}\mathrm{d}x = -\frac{\sqrt{a^2 - x^2}}{x} - \arcsin \frac{x}{a} + C $

### （九）含有 $ \sqrt{\pm ax^2 + bx + c} \ (a > 0) $ 的积分
72. $ \int \frac{\mathrm{d}x}{\sqrt{ax^2 + bx + c}} = \frac{1}{\sqrt{a}}\ln |2ax + b + 2\sqrt{a}\sqrt{ax^2 + bx + c}| + C $
73. $ \int \sqrt{ax^2 + bx + c}\mathrm{d}x = \frac{2ax + b}{4a}\sqrt{ax^2 + bx + c} + \frac{4ac - b^2}{8\sqrt{a^3}}\ln |2ax + b + 2\sqrt{a}\sqrt{ax^2 + bx + c}| + C $
74. $ \int \frac{x}{\sqrt{ax^2 + bx + c}}\mathrm{d}x = \frac{1}{a}\sqrt{ax^2 + bx + c} - \frac{b}{2\sqrt{a^3}}\ln |2ax + b + 2\sqrt{a}\sqrt{ax^2 + bx + c}| + C $
75. $ \int \frac{\mathrm{d}x}{\sqrt{c + bx - ax^2}} = \frac{1}{\sqrt{a}}\arcsin \frac{2ax - b}{\sqrt{b^2 + 4ac}} + C \ (b^2 + 4ac > 0) $
76. $ \int \sqrt{c + bx - ax^2}\mathrm{d}x = \frac{2ax - b}{4a}\sqrt{c + bx - ax^2} + \frac{b^2 + 4ac}{8\sqrt{a^3}}\arcsin \frac{2ax - b}{\sqrt{b^2 + 4ac}} + C \ (b^2 + 4ac > 0) $
77. $ \int \frac{x}{\sqrt{c + bx - ax^2}}\mathrm{d}x = -\frac{1}{a}\sqrt{c + bx - ax^2} + \frac{b}{2\sqrt{a^3}}\arcsin \frac{2ax - b}{\sqrt{b^2 + 4ac}} + C \ (b^2 + 4ac > 0) $

### （十）含有 $ \sqrt{\frac{a \pm x}{b \pm x}} $ 或 $ \sqrt{(x - a)(b - x)} $ 的积分
78. $ \int \sqrt{\frac{x + a}{x + b}}\mathrm{d}x = \sqrt{(x + a)(x + b)} + (a - b)\ln (\sqrt{x + a} + \sqrt{x + b}) + C $
79. $ \int \sqrt{\frac{a - x}{b - x}}\mathrm{d}x = -\sqrt{(a - x)(b - x)} + (b - a)\ln (\sqrt{a - x} + \sqrt{b - x}) + C $
80. $ \int \sqrt{\frac{b - x}{x - a}}\mathrm{d}x = \sqrt{(x - a)(b - x)} + (b - a)\arcsin \sqrt{\frac{x - a}{b - a}} + C \ (a < b) $
81. $ \int \sqrt{\frac{x - a}{b - x}}\mathrm{d}x = -\sqrt{(x - a)(b - x)} + (b - a)\arcsin \sqrt{\frac{x - a}{b - a}} + C \ (a < b) $
82. $ \int \frac{\mathrm{d}x}{\sqrt{(x - a)(b - x)}} = 2\arcsin \sqrt{\frac{x - a}{b - a}} + C \ (a < b) $

### （十一）含有三角函数的积分
83. $ \int \sin x\mathrm{d}x = -\cos x + C $
84. $ \int \cos x\mathrm{d}x = \sin x + C $
85. $ \int \tan x\mathrm{d}x = -\ln |\cos x| + C $
86. $ \int \cot x\mathrm{d}x = \ln |\sin x| + C $
87. $ \int \sec x\mathrm{d}x = \ln \left| \tan \left( \frac{\pi}{4} + \frac{x}{2} \right) \right| + C = \ln |\sec x + \tan x| + C $
88. $ \int \csc x\mathrm{d}x = \ln \left| \tan \frac{x}{2} \right| + C = \ln |\csc x - \cot x| + C $
89. $ \int \sec^2 x\mathrm{d}x = \tan x + C $
90. $ \int \csc^2 x\mathrm{d}x = -\cot x + C $
91. $ \int \sec x \tan x\mathrm{d}x = \sec x + C $
92. $ \int \csc x \cot x\mathrm{d}x = -\csc x + C $
93. $ \int \sin^2 x\mathrm{d}x = \frac{x}{2} - \frac{1}{4}\sin 2x + C $
94. $ \int \cos^2 x\mathrm{d}x = \frac{x}{2} + \frac{1}{4}\sin 2x + C $
95. $ \int \sin^n x\mathrm{d}x = -\frac{1}{n}\sin^{n - 1} x \cos x + \frac{n - 1}{n}\int \sin^{n - 2} x\mathrm{d}x $
96. $ \int \cos^n x\mathrm{d}x = \frac{1}{n}\cos^{n - 1} x \sin x + \frac{n - 1}{n}\int \cos^{n - 2} x\mathrm{d}x $
97. $ \int \frac{\mathrm{d}x}{\sin^n x} = -\frac{1}{n - 1}\frac{\cos x}{\sin^{n - 1} x} + \frac{n - 2}{n - 1}\int \frac{\mathrm{d}x}{\sin^{n - 2} x} $
98. $ \int \frac{\mathrm{d}x}{\cos^n x} = \frac{1}{n - 1}\frac{\sin x}{\cos^{n - 1} x} + \frac{n - 2}{n - 1}\int \frac{\mathrm{d}x}{\cos^{n - 2} x} $
99. $ \int \cos^m x \sin^n x\mathrm{d}x = \frac{1}{m + n}\cos^{m - 1} x \sin^{n + 1} x + \frac{m - 1}{m + n}\int \cos^{m - 2} x \sin^n x\mathrm{d}x = -\frac{1}{m + n}\cos^{m + 1} x \sin^{n - 1} x + \frac{n - 1}{m + n}\int \cos^m x \sin^{n - 2} x\mathrm{d}x $
100. $ \int \sin ax \cos bx\mathrm{d}x = -\frac{1}{2(a + b)}\cos(a + b)x - \frac{1}{2(a - b)}\cos(a - b)x + C \ (a^2 \neq b^2) $
101. $ \int \sin ax \sin bx\mathrm{d}x = -\frac{1}{2(a + b)}\sin(a + b)x + \frac{1}{2(a - b)}\sin(a - b)x + C \ (a^2 \neq b^2) $
102. $ \int \cos ax \cos bx\mathrm{d}x = \frac{1}{2(a + b)}\sin(a + b)x + \frac{1}{2(a - b)}\sin(a - b)x + C \ (a^2 \neq b^2) $
103. $ \int \frac{\mathrm{d}x}{a + b\sin x} = \frac{2}{\sqrt{a^2 - b^2}}\arctan \frac{a\tan \frac{x}{2} + b}{\sqrt{a^2 - b^2}} + C \ (a^2 > b^2) $
104. $ \int \frac{\mathrm{d}x}{a + b\sin x} = \frac{1}{\sqrt{b^2 - a^2}}\ln \left| \frac{a\tan \frac{x}{2} + b - \sqrt{b^2 - a^2}}{a\tan \frac{x}{2} + b + \sqrt{b^2 - a^2}} \right| + C \ (a^2 < b^2) $
105. $ \int \frac{\mathrm{d}x}{a + b\cos x} = \frac{2}{a + b}\sqrt{\frac{a + b}{a - b}}\arctan \left( \sqrt{\frac{a - b}{a + b}}\tan \frac{x}{2} \right) + C \ (a^2 > b^2) $
106. $ \int \frac{\mathrm{d}x}{a + b\cos x} = \frac{1}{a + b}\sqrt{\frac{a + b}{b - a}}\ln \left| \frac{\tan \frac{x}{2} + \sqrt{\frac{a + b}{b - a}}}{\tan \frac{x}{2} - \sqrt{\frac{a + b}{b - a}}} \right| + C \ (a^2 < b^2) $
107. $ \int \frac{\mathrm{d}x}{a^2\cos^2 x + b^2\sin^2 x} = \frac{1}{ab}\arctan \left( \frac{b}{a}\tan x \right) + C $
108. $ \int \frac{\mathrm{d}x}{a^2\cos^2 x - b^2\sin^2 x} = \frac{1}{2ab}\ln \left| \frac{b\tan x + a}{b\tan x - a} \right| + C $
109. $ \int x\sin ax\mathrm{d}x = \frac{1}{a^2}\sin ax - \frac{1}{a}x\cos ax + C $
110. $ \int x^2\sin ax\mathrm{d}x = -\frac{1}{a}x^2\cos ax + \frac{2}{a^2}x\sin ax + \frac{2}{a^3}\cos ax + C $
111. $ \int x\cos ax\mathrm{d}x = \frac{1}{a^2}\cos ax + \frac{1}{a}x\sin ax + C $
112. $ \int x^2\cos ax\mathrm{d}x = \frac{1}{a}x^2\sin ax + \frac{2}{a^2}x\cos ax - \frac{2}{a^3}\sin ax + C $

### （十二）含有反三角函数的积分（其中 $ a > 0 $）
113. $ \int \arcsin \frac{x}{a}\mathrm{d}x = x\arcsin \frac{x}{a} + \sqrt{a^2 - x^2} + C $
114. $ \int x\arcsin \frac{x}{a}\mathrm{d}x = \left( \frac{x^2}{2} - \frac{a^2}{4} \right)\arcsin \frac{x}{a} + \frac{x}{4}\sqrt{a^2 - x^2} + C $
115. $ \int x^2\arcsin \frac{x}{a}\mathrm{d}x = \frac{x^3}{3}\arcsin \frac{x}{a} + \frac{1}{9}(x^2 + 2a^2)\sqrt{a^2 - x^2} + C $
116. $ \int \arccos \frac{x}{a}\mathrm{d}x = x\arccos \frac{x}{a} - \sqrt{a^2 - x^2} + C $
117. $ \int x\arccos \frac{x}{a}\mathrm{d}x = \left( \frac{x^2}{2} - \frac{a^2}{4} \right)\arccos \frac{x}{a} - \frac{x}{4}\sqrt{a^2 - x^2} + C $
118. $ \int x^2\arccos \frac{x}{a}\mathrm{d}x = \frac{x^3}{3}\arccos \frac{x}{a} - \frac{1}{9}(x^2 + 2a^2)\sqrt{a^2 - x^2} + C $
119. $ \int \arctan \frac{x}{a}\mathrm{d}x = x\arctan \frac{x}{a} - \frac{a}{2}\ln(a^2 + x^2) + C $
120. $ \int x\arctan \frac{x}{a}\mathrm{d}x = \frac{1}{2}(a^2 + x^2)\arctan \frac{x}{a} - \frac{a}{2}x + C $
121. $ \int x^2\arctan \frac{x}{a}\mathrm{d}x = \frac{x^3}{3}\arctan \frac{x}{a} - \frac{a}{6}x^2 + \frac{a^3}{6}\ln(a^2 + x^2) + C $

### （十三）含有指数函数的积分
122. $ \int a^x\mathrm{d}x = \frac{1}{\ln a}a^x + C $
123. $ \int \mathrm{e}^{ax}\mathrm{d}x = \frac{1}{a}\mathrm{e}^{ax} + C $
124. $ \int x\mathrm{e}^{ax}\mathrm{d}x = \frac{1}{a^2}(ax - 1)\mathrm{e}^{ax} + C $
125. $ \int x^n\mathrm{e}^{ax}\mathrm{d}x = \frac{1}{a}x^n\mathrm{e}^{ax} - \frac{n}{a}\int x^{n - 1}\mathrm{e}^{ax}\mathrm{d}x \ (n > 0) $
126. $ \int x a^x\mathrm{d}x = \frac{x}{\ln a}a^x - \frac{1}{(\ln a)^2}a^x + C $
127. $ \int x^n a^x\mathrm{d}x = \frac{1}{\ln a}x^n a^x - \frac{n}{\ln a}\int x^{n - 1}a^x\mathrm{d}x \ (n > 0) $
128. $ \int \mathrm{e}^{ax}\sin bx\mathrm{d}x = \frac{1}{a^2 + b^2}\mathrm{e}^{ax}(a\sin bx - b\cos bx) + C $
129. $ \int \mathrm{e}^{ax}\cos bx\mathrm{d}x = \frac{1}{a^2 + b^2}\mathrm{e}^{ax}(b\sin bx + a\cos bx) + C $
130. $ \int \mathrm{e}^{ax}\sin^n bx\mathrm{d}x = \frac{1}{a^2 + b^2 n^2}\mathrm{e}^{ax}\sin^{n - 1} bx(a\sin bx - nb\cos bx) + \frac{n(n - 1)b^2}{a^2 + b^2 n^2}\int \mathrm{e}^{ax}\sin^{n - 2} bx\mathrm{d}x $
131. $ \int \mathrm{e}^{ax}\cos^n bx\mathrm{d}x = \frac{1}{a^2 + b^2 n^2}\mathrm{e}^{ax}\cos^{n - 1} bx(a\cos bx + nb\sin bx) + \frac{n(n - 1)b^2}{a^2 + b^2 n^2}\int \mathrm{e}^{ax}\cos^{n - 2} bx\mathrm{d}x $

### （十四）含有对数函数的积分
132. $ \int \ln x\mathrm{d}x = x\ln x - x + C $
133. $ \int \frac{\mathrm{d}x}{x\ln x} = \ln |\ln x| + C $
134. $ \int x^n \ln x\mathrm{d}x = \frac{1}{n + 1}x^{n + 1}\left( \ln x - \frac{1}{n + 1} \right) + C \ (n \neq -1) $
135. $ \int (\ln x)^n\mathrm{d}x = x(\ln x)^n - n\int (\ln x)^{n - 1}\mathrm{d}x \ (n \neq -1) $
136. $ \int x^m (\ln x)^n\mathrm{d}x = \frac{1}{m + 1}x^{m + 1}(\ln x)^n - \frac{n}{m + 1}\int x^m (\ln x)^{n - 1}\mathrm{d}x \ (n \neq -1) $