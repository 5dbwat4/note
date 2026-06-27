---
title: Changelog of Accumbens
---

Accumbens的changelog在noting里面，惊不惊喜，意不意外？

开始于2026/6，更早的Changelog已不可考。

---

2026/6/27 558f1aa16cb4870f106f8e250fc5b59b99204e61

1. fix: 优化getEntry流程，不再获取全部config chunks

2026/6/27 6096b6633c896e58c804db87d02a78133f334304

1. add: 新增charts页面实现，build过程新增clooect stats

2026/6/24 62f96ed08c80280713c40574992682696dde193a

1. add: 新增Mermaid组件

2026/6/3 9d5939a0c8ab13cf4b02f19873dbf6a0b8f53860

1. fix: 修复了minecraft 404 page中的import问题

2026/6/2 c38216302fce66313a551457944c85eb532974f6

1. add: settings页面新增build info组件
2. add: 新增vite plugin暴露build info

2026/5/30 a49caeb104dab72af3ff36a1b584f8f10d0079c4

1. fix: 改为默认关闭鼠标指针动态

2026/5/30 581253c6fec297519b61ef7ee48e41d69f256173

1. add: 新增quizd组件

2026/5/30 f5d69e3fb63df8d490dc57724bceba059eee1967

1. fix: 修复了custom-collapse.vue中path路径截取异常的问题

2026/5/12 bd81ce373444641358dea73ad019bd50c30bcbe9 60cb038434ba32617c7d617d7a81fb74bbeb19cb 3c6a16dbcea550da2964b0cca5f2bd8966d0a04b

1. rm: 删除旧的404页面
2. add: 新写的minecraft 404 page  
   非常好看，推荐去看，网址栏里替换成一个不存在的路径即可。是一个可互动的three.js实例

2026/5/10 986152eeae1feebfbe021eb0777059d1e2d7f3a8

1. add: card组件新增了一些type

2026/5/6 8d1896f91e16f42d4baded0049b0845e0978e340

1. refactor: 图标方案从@iconify/unplugin迁移到unplugin-icons，所有图标import路径从`/~iconify/`改为`~icons/`
2. 试图引入nuxtui, tailwindcss, Roboto Mono字体

2026/5/6 eb8e29d971b4a2160cc2fd2da1c11eb778605624

1. add: hljs新增RISC-V汇编语法高亮支持，使用`riscv`或`riscvasm`作为lang字段

2026/4/1 2ef26c175a8b925c5b8594fb3a7e7f16130ea130

1. refactor: Service Worker（做了很多修改，但没有启用）  
   文件命名成了cranium.js（颅骨），但是没有测试也没有启用……  
   新增storage-mgr页面，展示SW状态和缓存管理功能（同样没有启用）
3. fix: 重构ToC生成逻辑，修复heading文本提取过于naive的问题
4. add: 页面标题动态更新
5. feat: "打印时隐藏header"启用时还会隐藏breadcrumb
6. feat: highlight.js新增`plain`类型

2026/3/23 bc561357369fb1929106cda7e142966dcdabcba8

1. add: 新增/about-me页面，增加自我介绍内容
2. add: settings页面新增"打印时隐藏header"选项
3. fix: 调整了一些设置的默认值
4. feat: /about-accumbens页面新增了3rd-party链接
5. add: 新增@md-comp路径别名，等价于原来的@md-components

2026/3/7 7c667baa57f7da23d2f891ae04584102a9803879 

1. feat: build产物改成自定义chunk命名（noting内容为neuron，其他为myelin）

喜欢这个名字吗？我很喜欢。neuron是神经元，myelin是髓鞘，而accumbens是伏隔核，一切都对上了。

而且neuron和myelin字符数相同，也就是说他们的编译产物文件是对齐的、强迫症友好的。


2026/3/7 997723cb4d4c1ba6461ae2cadab67a66bff48048

1. fix: 将所有icon import路径从`~iconify/`改为`/~iconify/`以修正resolve问题

2026/2/22 36c5d2787f52045f40cdb51beaecd25135b916f7

1. refactor: 删除本地SVG/Vue图标文件，改用~iconify虚拟模块
2. fix: markdown中斜体改成了"Times New Roman"+LXGW-Wenkai-Screen样式


2026/2/21 08432b6a07898d6069259d938b9fc9048bd308f4

1. chore: 版本号从1.0.0升级至1.1.0


2026/2/21 5afe751de8d47d105cc851d46151fef94739c019

1. refactor: 图标方案从@iconify-prerendered全面迁移到@iconify/unplugin，所有icon import改为`~iconify/`格式
2. add: 图片增加loading="lazy"属性
3. refactor: vite配置新增`@iconify/unplugin`
4. deps: 升级了一次依赖版本
   

2026/2/21 ec5af3a891b91fcb9472fec8f356e1282b59e328

1. add: 新增vite-plugin-md-relative-image-url plugin，  
   图片不再使用embbed了！自此，所有图片导入由vite处理，不再使用data:路径。  
   但是这个plugin个人感觉 写的一般其实……  
   主要是想不出更优雅的实现
2. fix: breadcrumb路径跳转改用string而非array
3. fix: dirList中subcategory的key从`path[0]`改为`path`
4. feat: compile-doc-tree config插件maxEntriesPerBucket从256改为128

<!-- 
2026/2/19 f13c45da2fc42d604af02eb28a4910198dd41c74

1. refactor: compile-doc-tree全面重构为模块化插件系统（core/parser/loaders/packing/helpers），支持chunk分块加载
2. add: 新增vite-plugin-compile-doc-tree，在dev/build时自动编译文档树
3. add: 新增docs/how-config-works.md配置文档
4. refactor: configUtils改用懒加载方式获取config chunks，不再一次性加载全部config
5. add: CodeBlocks新增breakLines属性支持自动换行，滚动条hover时才显示
6. refactor: container.vue重命名为CustomContainer.vue

2025/10/13 aa80aa62c474ffe086a2f76ee3edc3cf7a140744

1. add: /about页面拆分为/about-me和/about-accumbens，about-accumbens新增项目介绍内容
2. add: index.html新增meta description
3. refactor: printNotif和404组件改为异步懒加载
4. add: 注册NTimeline/NTimelineItem组件

2025/9/24 7e3c32a2167ffd5753a07ea0d007b2be645624b3

1. add: 试验性添加基于three.js的404页面（后因体积过大被移除），含MMD模型加载等

2025/9/22 862d9a5f41e74a1cda0549d4fecd14099ffa5351

1. add: 引入ant-design-vue、focus-trap依赖
2. add: 新增全局键盘快捷键系统（Q切换index/entry视图、Backspace返回上一页、Focus Trap）
3. add: settings页面全面改版，新增Keyboard Shortcuts设置区、打印时样式设置
4. add: dirList中subcategories和entries合并显示（按类型混合排序）
5. add: 全局滚动行为改为smooth
6. add: markdown表格样式重写，支持hover高亮行

2025/8/24 e3fb9dead7f83d75d9259a955f5d0ac1e24d7d6f

1. add: 首页新增"看看数值"按钮，链接到/charts页面
2. add: 新增charts页面占位符
3. refactor: dirList合并Subcategories和Entries为单一列表，共享--None--占位

2025/8/16 af8898f34954339dbb235e30ab79133143de378a

1. add: card组件新增noExpansion属性，支持禁用折叠/展开功能
2. add: jsconfig.json新增@notes、@md-components路径别名

2025/8/6 7f9d746e7c74bb4ed77c76e0e3984e727c08599c

1. fix: ToC组件的打印样式CSS修复（`@print`改为`@media print`）

2025/7/15 154cb1c03643adfc7421898178ef9e01de3e3b73

1. fix: 修复目录路由重定向逻辑（去除不必要的redirect和部分渲染条件）
2. add: ToC component样式微调（margin-bottom）
3. add: 新增bundleDetail rollup插件辅助构建分析（默认不启用） -->