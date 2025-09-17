---
title: 程算PTA易错题集
createdAt: 2025-01-02T13:21:00.000Z
updatedAt: 2025-01-02T13:21:00.000Z
---
1. 在 C 程序中，APH 和 aph 代表不同的变量。
   (T)
2. 假设运算符'\*'和'%'都是右结合的，则表达式 (3\*5%3) 的值为6。
   (T)
3. 下列运算符中，优先级最低的是____。
   A. *   B. !=   C. +    D. =
   (D)
4. 为了检查以下if-else语句的两个分支是否正确，至少需要设计2组测试用例，即x的取值至少有两组（不等于0的数和0）。
   ```c
   if (x != 0){
      y = 1 / x;
   } else{ 
      y = 0;
   } 
   ```
   (T)
5. 在嵌套使用if语句时，C语言规定else总是______。
   A. 和之前与其具有相同缩进位置的if配对
   B. 和之前与其最近的if配对
   C. 和之前与其最近的且不带else的if配对
   D. 和之前的第一个if配对
   (C)
6. After executing the following code fragment, the value of variable m is __.
   ```c
   int m;
   for( m=0; m<9; m++ )   m++;
   ```
   A. 8   B. 9   C. 10   D. 11
   (C)
7. 以下代码，语法正确的是：
   A. `while ( ) ;`
   B. `for(  ) ;`
   C. `for( ; ; ) ;`
   D. `do { } while( );`
   (C) While不能omit
8. sizeof( )是C语言的一个函数，可以计算参量所占内存的字节数。如sizeof(int)可计算整型所占的内存字节数。
   (F)
9. C语言中,通过函数调用只能获得一个返回值。
   (T)
10. C 语言程序中可以有多个函数 , 但只能有一个主函数。
    (T)
11. 在C语言程序中，若对函数类型未加显式说明，则函数的隐含类型为（）。
    (int)
12. 假设有定义如下： int array[10]; 则该语句定义了一个数组array。其中array的类型是整型指针（即： int *）。
    (F)
13. Among the following assignments or initializations, __ is wrong.
    A. `char str[10]; str="string";`
    B. `char str[]="string";`
    C. `char *p="string";`
    D. `char *p; p="string";`
    (A)
14. According to the declaration: `int p[5], *a[5];` the expression ______ is correct.
    A. `p=a`
    B. `p[0] = a`
    C. `*(a+1)=p`
    D. `a[0]=2`
    (C)
15. According to the declaration: `int (*p)[10];`, p is a(n) __.
    (pointer)
16. 不同类型的指针变量是可以直接相互赋值的。
    (F)
17. 数组的基地址是在内存中存储数组的起始位置，数组名本身就是一个地址即指针值。
    (T)
18. 两个任意类型的指针可以使用关系运算符比较大小。
    (F)
19. In the following declarations, the correct assignment expression is __.
    ```c
    int *p[3], a[3];
    ```
    A. `p = a`   B. `p = &a[0]`   C. `*p = a`   D. `p[0] = *a`
    (C)
20. 宏定义不存在类型问题，宏名无类型，它的参数也无类型。
    (T)
21. 全局变量不可以和函数内的局部变量同名。
    (F)
22. 凡是函数中未指定存储类别的局部变量，其隐含的存储类型为(  )。
    A. 自动（auto）   B. 静态（static）   C. 外部（extern）   D. 寄存器（register）
    (A)
23. 在一个C源程序文件中，若要定义一个只允许本源文件中所有函数使用的全局变量，则该变量需要使用的存储类别是。
    A. extern   B. register   C. auto   D. static
    (D
24. 将一个函数说明为static后，该函数将 (  )。
    A. 既能被同一源文件中的函数调用，也能被其他源文件中的函数调用
    B. 只能被同一源文件中的函数调用，不能被其他源文件中的函数调用
    C. 只能被其他源文件中的函数调用，不能被同一源文件中的函数调用
    D. 既不能被同一源文件中的函数调用，也不能被其他源文件中的函数调用
    (B)
25. 以下是一个C语言程序的除标准库之外的全部源代码，则说法正确的是
    ```c
    #include <stdio.h>
    extern int k;
    int main(){
        k = 2223;
        printf("%d\n", k);
        return 0;
    }
    ```
    A. 这段程序编译错误
    B. 这段程序编译正确，但是链接（link）错误
    C. 这段程序编译、链接（link）正确，但是运行时错误
    D. 程序无错，可正常运行
    (B)
26.
