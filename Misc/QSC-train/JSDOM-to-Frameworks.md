---
title: 从JS操作DOM，到Modern Framework
---

# JS操作DOM

在没有框架的时代，前端开发主要依赖原生的JavaScript来操作DOM。这种方式虽然灵活，但代码量大且难以维护。以下是一些常见的操作DOM的方法：

```html
<div>
    <input type="text" id="myInput" placeholder="你是谁"/>
    <button id="myButton">点击我</button>
    <p id="myParagraph"></p>
    <ul id="myList">
        <li>项目1</li>
        <li>项目2</li>
        <li>项目3</li>
    </ul>
</div>
```

```javascript
document.getElementById('myButton').addEventListener('click', function() {
    const name = document.getElementById('myInput').value;
    document.getElementById('myParagraph').innerText = '你好，' + name + '！';
});
document.querySelectorAll('#myList li').forEach(function(item) {
    item.style.color = 'blue';
});
```

# jQuery简化DOM操作

后来（Good old days），jQuery的出现极大地简化了DOM操作。它提供了简洁的语法和强大的功能，使得开发者能够更高效地操作DOM。

```javascript
$('#myButton').on('click', function() {
    const name = $('#myInput').val();
    $('#myParagraph').text('你好，' + name + '！');
});
$('#myList li').css('color', 'blue');
```

# Modern Frameworks

随着前端应用的复杂性增加，现代框架如React、Vue和Angular应运而生。这些框架引入了组件化开发、虚拟DOM和数据绑定等概念，大大提升了开发效率和代码可维护性。

使用`<script src="https://unpkg.com/vue@next"></script>`等方式引入Vue后，可以这样写：

```html
<div id="app">
    <input type="text" v-model="name" placeholder="你是谁"/>
    <button @click="greet">点击我</button>
    <p>你好，{{ name }}！</p>
    <ul>
        <li>项目1</li>
        <li>项目2</li>
        <li>项目3</li>
    </ul>
</div>

<script>
    const { createApp } = Vue;
    createApp({
        data() {
            return {
                name: ''
            };
        },
        methods: {
            greet() {
                alert('你好，' + this.name + '！');
            }
        }
    }).mount('#app');
</script>
```

发生了什么？通过Vue的双向数据绑定，输入框的值与`name`变量保持同步。当用户输入名字并点击按钮时，`greet`方法会被调用，弹出框中显示用户的名字。这种方式比起传统的DOM操作，代码更加简洁和易于维护。

# SFC, JSX

现代框架还支持单文件组件（SFC）和JSX语法，使得组件化开发更加方便。例如，使用Vue的SFC：

```vue
<template>
  <div>
    <input type="text" v-model="name" placeholder="你是谁"/>
    <button @click="greet">点击我</button>
    <p>你好，{{ name }}！</p>
    <ul>
      <li>项目1</li>
      <li>项目2</li>
      <li>项目3</li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const name = ref('');
const greet = () => {
  alert('你好，' + name.value + '！');
};
</script>
```

通过这种方式，HTML、JavaScript和CSS可以集中在一个文件中，提升了代码的组织性和可读性。

React的JSX语法也类似：

```jsx
import React, { useState } from 'react';
function App() {
    const [name, setName] = useState('');
    const greet = () => {
        alert('你好，' + name + '！');
    };
    return (
        <div>
            <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="你是谁"/>
            <button onClick={greet}>点击我</button>
            <p>你好，{name}！</p>
            <ul>
                <li>项目1</li>
                <li>项目2</li>
                <li>项目3</li>
            </ul>
        </div>
    );
}
export default App;
```

通过这些现代框架，前端开发变得更加高效和愉快。开发者可以专注于业务逻辑，而不必过多关注底层的DOM操作细节。

# SPA

现代框架通常用于构建单页应用（SPA）。SPA通过动态加载内容，避免了页面的频繁刷新，提升了用户体验。刚才那个其实就是一个简单的SPA示例。

# Router, SFC, State Management

现在，我们想要引入Router的概念。

从PJAX开始：

- PJAX（PushState + AJAX）允许在不刷新整个页面的情况下加载部分内容，提升用户体验。
- 通过监听链接点击事件，使用AJAX请求新内容，并利用History API更新浏览器地址栏。

现代前端框架通常内置了路由功能，例如Vue Router和React Router。它们允许开发者定义不同的路由路径，并将其映射到相应的组件。

结合单文件组件（SFC）和状态管理（如Vuex或Redux），开发者可以构建复杂的SPA应用，管理应用状态和路由导航变得更加简单和高效。

