---
title: 补天笔记
createdAt: 2025-1-2 21:21:38
updatedAt: 2025-1-3 21:00:00
---
# fopen


| mode | 功能                                                 |
| ---- | ---------------------------------------------------- |
| r    | 打开只读                                             |
| r+   | 打开读写， 从⽂件头开始                              |
| w    | 打开只写 。如果不存在则新建， 如果存在则清空         |
| w+   | 打开读写 。如果不存在则新建， 如果存在则清空         |
| a    | 打开追加 。如果不存在则新建， 如果存在则从⽂件尾开始 |
| x    | 只新建， 如果⽂件已存在则不能打开                    |

# 在⽂件中定位

`long ftell(FILE *stream);`

`int fseek(FILE *stream, long offset, int whence);`

`whence`

`SEEK_SET` :从头开始

`SEEK_CUR` :从当前位置开始

`SEEK_END` :从尾开始(倒过来)

# 不对外公开的函数

在函数前⾯加上   `static`   就使得它成为只能在所在的编译单元中被使⽤的函数

在全局变量前⾯加上 `static` 就使得它成为只能在所在的编译单元中被使⽤的全局变量

# 变量的声明

`int i;` 是变量的定义

`extern int i;` 是变量的声明

# for循环的顺序：

The statement

`for ( clause-1 ; expression-2 ; expression-3 ) statement`

behaves as follows: The expression expression-2 is the controlling expression that is  evaluated before each execution of the loop body. The expression expression-3 is  evaluated as a void expression after each execution of the loop body. If clause-1 is a  declaration, the scope of any identifiers it declares is the remainder of the declaration and  the entire loop, including the other two expressions; it is reached in the order of execution  before the first evaluation of the controlling expression. If clause-1 is an expression, it is  evaluated as a void expression before the first evaluation of the controlling expression.

省流：1->2->s->3->2->s->3->...->2->end

# 如何qsort

```c
#undef qsort
#include<stdlib.h>
int compare(const void* a, const void* b) {
return (*(int*)a - *(int*)b);
}
void insertionSort(int a[],int len){
    qsort(a,len,sizeof(int),compare);
}
```

# C类型体操

The constructions

(a)  int

(b)  int \*

(c)  int \*[3]

(d)  int (\*)[3]

(e)  int (\*)[\*]

(f)  int \*()

(g)  int (\*)(void)

(h)  int (\*const [])(unsigned int, ...)

name respectively the types (a) int, (b) pointer to int, (c) array of three pointers to int, (d) pointer to an  array of three ints, (e) pointer to a variable length array of an unspecified number of ints, (f) function  with no parameter specification returning a pointer to int, (g) pointer to function with no parameters returning an int, and (h) array of an unspecified number of constant pointers to functions, each with one  parameter that has type unsigned int and an unspecified number of other parameters, returning an  int.

# static extern auto & register

1. An object whose identifier is declared without the storage-class specifier ` _Thread_local`, and either with external or internal linkage or with the storage-class  specifier `static`, has static storage duration. Its lifetime is the entire execution of the  program and its stored value is initialized only once, prior to program startup.
