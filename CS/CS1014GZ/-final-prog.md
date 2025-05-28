---
title: 函数题&程序题补天
createdAt: 2025-01-02 16:53:55
updatedAt: 2025-01-03 21:00:00
---
# 7-1 二分查找法之过程

本题要求使用二分查找法，在给定的n个升序排列的整数中查找x，并输出查找过程中每一步的中间结果。如果数组a中的元素与x的值相同，输出相应的下标（下标从0开始）；如果没有找到，输出“Not Found”。如果输入的n个整数没有按照从小到大的顺序排列，或者出现了相同的数，则输出“Invalid Value”。

二分查找法的算法步骤描述如下：

设n个元素的数组a已升序排列，用`left`和`right`两个变量来表示查找的区间，即在`a[left] 〜 a[right]`区间去查找x。初始状态为`left = 0，right = n-1`。首先用要查找的x与查找区间的中间位置元素`a[mid]`（`mid = (left + right) / 2`）比较，如果相等则找到；如果`x < a[mid]`，由于数组是升序排列的，则只要在`a[left] 〜 a[mid-1]`区间继续查找；如果`x > a[mid]`，则只要在`a[mid+1] 〜 a[right]`区间继续查找。也就是根据与中间元素比较的情况产生了新的区间值`left`、`right`值，当出现`left > right`时，说明不存在值为x的元素。

### 输入格式：

输入在第1行中给出一个正整数n（1≤n≤10）和一个整数x，第2行输入n个整数，其间以空格分隔。题目保证数据不超过长整型整数的范围。

### 输出格式：

在每一行中输出查找过程中对应步骤的中间结果，按照“[left,right][mid]”的格式输出。提示：相邻数字、符号之间没有空格。

如果找到，输出相应的下标（下标从0开始）；如果没有找到，在一行中输出“Not Found”。

如果输入的n个整数没有按照从小到大的顺序排列，或者出现了相同的数，则输出“Invalid Value”。

### 输入样例1：

```in
10 2
1 2 3 4 5 6 7 8 9 10
```

### 输出样例1：

```out
[0,9][4]
[0,3][1]
1
```

### 输入样例2：

```in
4 5
71 74 78 100
```

### 输出样例2：

```out
[0,3][1]
[0,0][0]
Not Found
```

### 输入样例3：

```in
5 5
39 60 80 80 100
```

### 输出样例3：

```out
Invalid Value
```

```c
#include <stdio.h>

int binary_search(int a[], int n, int x) {
    int left = 0, right = n - 1, mid;
    while (left <= right) {
        mid = (left + right) / 2;
        printf("[%d,%d][%d]\n", left, right, mid);
        if (a[mid] == x) {
            return mid;
        } else if (a[mid] < x) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    
    }
    return -1;
}

int main() {
    int n, x, i, a[100000];
    scanf("%d %d", &n, &x);
    for (i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }
    for(i=0;i<n-1;i++){
        if(a[i]>=a[i+1]){
            printf("Invalid Value\n");
            return 0;
        }
    }
    int result = binary_search(a, n, x);
    if (result == -1) {
        printf("Not Found\n");
    } else {
        printf("%d\n", result);
    }
    return 0;
}
```

# 7-2 选择法排序之过程

本题要求使用选择法排序，将给定的n个整数从小到大排序后输出，并输出排序过程中每一步的中间结果。

选择排序的算法步骤如下：

第0步：在未排序的n个数（a[0]〜 a[n−1]）中找到最小数，将它与 a[0]交换；

第1步：在剩下未排序的n−1个数（a[1] 〜 a[n−1]）中找到最小数，将它与 a[1] 交换；

……

第k步：在剩下未排序的n−k个数（a[k]〜a[n−1]）中找到最小数，将它与 a[k] 交换；

……

第n−2步：在剩下未排序的2个数（a[n−2] 〜a[n−1]）中找到最小数，将它与 a[n−2]交换。

### 输入格式：

输入第一行给出一个不超过10的正整数n。第二行给出n个整数，其间以空格分隔。

### 输出格式：

在每一行中输出排序过程中对应步骤的中间结果，即每一步后a[0]〜 a[n−1]的值，相邻数字间有一个空格，行末不得有多余空格。

### 输入样例：

```in
4
5 1 7 6
```

### 输出样例：

```out
1 5 7 6
1 5 7 6
1 5 6 7
```

```c
#include <stdio.h>

void selection_sort(int a[], int n) {
    int i, j, min_idx;
    for (i = 0; i < n - 1; i++) {
        min_idx = i;
        for (j = i + 1; j < n; j++) {
            if (a[j] < a[min_idx]) {
                min_idx = j;
            }
        }

        if (min_idx!= i) {
            int temp = a[i];
            a[i] = a[min_idx];
            a[min_idx] = temp;
        }
        printf("%d", a[0]);
        for (j = 1; j < n; j++) {
            printf(" %d", a[j]);
        }
        printf("\n");
    }
}

int main() {
    int n, i;
    scanf("%d", &n);
    int a[100];
    for (i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }
    if(n==1){
        printf("%d",a[0]);
        return 0;
    }
    selection_sort(a, n);
    return 0;
}
```

# 7-3 冒泡法排序之过程

本题要求使用冒泡法排序，将给定的n个整数从小到大排序后输出，并输出排序过程中每一步的中间结果。

冒泡排序的算法步骤描述如下：

第1步：在未排序的n个数（a[0]〜 a[n−1]）中，从a[0]起，依次比较相邻的两个数，若邻接元素不符合次序要求，则对它们进行交换。本次操作后，数组中的最大元素“冒泡”到a[n−1]；

第2步：在剩下未排序的n−1个数（a[0] 〜 a[n−2]）中，从a[0]起，依次比较相邻的两个数，若邻接元素不符合次序要求，则对它们进行交换。本次操作后，a[0] 〜 a[n−2]中的最大元素“冒泡”到a[n−2]；

……

第i步：在剩下未排序的n−k个数（a[0]〜a[n−i]）中，从a[0]起，依次比较相邻的两个数，若邻接元素不符合次序要求，则对它们进行交换。本次操作后，a[0] 〜 a[n−i]中的最大元素“冒泡”到a[n−i]；

……

第n−1步：在剩下未排序的2个数（a[0] 〜a[1]）中，比较这两个数，若不符合次序要求，则对它们进行交换。本次操作后，a[0] 〜 a[1]中的最大元素“冒泡”到a[1]。

输入格式：
输入第一行给出一个不超过10的正整数n。第二行给出n个整数，其间以空格分隔。

输出格式：
在每一行中输出排序过程中对应步骤的中间结果，即每一步后a[0]〜 a[n−1]的值，相邻数字间有一个空格，行末不得有多余空格。

输入样例：
5
8 7 6 0 1
输出样例：
7 6 0 1 8
6 0 1 7 8
0 1 6 7 8
0 1 6 7 8

```c
#include <stdio.h>

int main() {
    int n, i, j, temp;
    scanf("%d", &n);
    int a[n];
    for (i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    if(n==1){
        printf("%d\n",a[0]);
        return 0;
    }

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
        printf("%d", a[0]);
        for (j = 1; j < n; j++) {
            printf(" %d", a[j]);
        }
        printf("\n");
    }
    return 0;
}
```

# 6-2 归并排序

本题要求实现二路归并排序中的归并操作，待排序列的长度1<=n<=1000。

函数接口定义：

```c
void Merge(SqList L,int low,int m,int high);
```

其中L是待排序表，使排序后的数据从小到大排列。
###类型定义：

```c
#include<stdio.h>
#include<stdlib.h>
typedef  int  KeyType;
typedef  struct {                    
  KeyType *elem; /*elem[0]一般作哨兵或缓冲区*/                     
  int Length;    
}SqList;
void  CreatSqList(SqList *L);/*待排序列建立，由裁判实现，细节不表*/ 
void  MergeSort(SqList L,int low,int high);
void Merge(SqList L,int low,int m,int high); 
int main()
{
  SqList L;
  int i;
  CreatSqList(&L);
  MergeSort(L,1,L.Length);
  for(i=1;i<=L.Length;i++)
   {      
      printf("%d ",L.elem[i]);
   }
  return 0;
}
void MergeSort(SqList L,int low,int high)  
{   
    /*用分治法进行二路归并排序*/  
    int mid;  
    if(low<high)  /*区间长度大于1*/
    {    
        mid=(low+high)/2;               /*分解*/
        MergeSort(L,low,mid);           /*递归地对low到mid序列排序 */ 
        MergeSort(L,mid+1,high);        /*递归地对mid+1到high序列排序 */ 
        Merge(L,low,mid,high);          /*归并*/  
    }  
}
/*你的代码将被嵌在这里 */
```

输入样例：
第一行整数表示参与排序的关键字个数。第二行是关键字值 例如：

```in
10
5 2 4 1 8 9 10 12 3 6
```

输出样例：
输出由小到大的有序序列，每一个关键字之间由空格隔开，最后一个关键字后有一个空格。

```out
1 2 3 4 5 6 8 9 10 12 
```

```c
void Merge(SqList L, int low, int m, int high) {
    int i, j, k;
    int n1 = m - low + 1;   // 左边子序列的长度
    int n2 = high - m;      // 右边子序列的长度

    // 创建临时数组
    int *L1 = (int *)malloc(n1 * sizeof(int));
    int *L2 = (int *)malloc(n2 * sizeof(int));

    // 将数据拷贝到临时数组L1和L2中
    for (i = 0; i < n1; i++) {
        L1[i] = L.elem[low + i];
    }
    for (j = 0; j < n2; j++) {
        L2[j] = L.elem[m + 1 + j];
    }

    // 归并回L.elem
    i = 0; // L1的索引
    j = 0; // L2的索引
    k = low; // L.elem的索引
    while (i < n1 && j < n2) {
        if (L1[i] <= L2[j]) {
            L.elem[k++] = L1[i++];
        } else {
            L.elem[k++] = L2[j++];
        }
    }

    // 拷贝L1或L2中剩余的元素
    while (i < n1) {
        L.elem[k++] = L1[i++];
    }
    while (j < n2) {
        L.elem[k++] = L2[j++];
    }

    // 释放临时数组
    free(L1);
    free(L2);
}
```

# 6-4 快速排序

本题要求实现快速排序的一趟划分函数，待排序列的长度1<=n<=1000。

函数接口定义：

```c
int Partition ( SqList L, int low,  int high )；
```

其中L是待排序表，使排序后的数据从小到大排列。
###类型定义：

```c
typedef  int  KeyType;
typedef  struct 
{                    
  KeyType *elem; /*elem[0]一般作哨兵或缓冲区*/                     
  int Length;    
}SqList;
```

裁判测试程序样例：

```c
#include<stdio.h>
#include<stdlib.h>
typedef  int  KeyType;
typedef  struct 
{                    
  KeyType *elem; /*elem[0]一般作哨兵或缓冲区*/                   
  int Length;    
}SqList;
void  CreatSqList(SqList *L);/*待排序列建立，由裁判实现，细节不表*/ 
int Partition ( SqList  L,int low,  int  high );
void Qsort ( SqList  L,int low,  int  high );
int main()
{
  SqList L;
  int i;
  CreatSqList(&L);
  Qsort(L,1,L.Length);
  for(i=1;i<=L.Length;i++)
      printf("%d ",L.elem[i]);
  return 0;
}
void Qsort ( SqList  L,int low,  int  high ) 
{ 
    int  pivotloc;
    if(low<high)
    {  
        pivotloc = Partition(L, low, high ) ;
        Qsort (L, low, pivotloc-1) ; 
        Qsort (L, pivotloc+1, high );
     }
}
/*你的代码将被嵌在这里 */
```

输入样例：
第一行整数表示参与排序的关键字个数。第二行是关键字值 例如：

```in
10
5 2 4 1 8 9 10 12 3 6
```

输出样例：
输出由小到大的有序序列，每一个关键字之间由空格隔开，最后一个关键字后有一个空格。

```out
1 2 3 4 5 6 8 9 10 12 
```

```c

int Partition ( SqList  L,int low,  int  high ) 
{ 
    KeyType pivot, temp;
    int i, j, pivotloc;
    pivot = L.elem[high];
    pivotloc = low;
    for(i=low;i<high;i++)
    {
        if(L.elem[i]<pivot)
        {
            temp = L.elem[i];
            L.elem[i] = L.elem[pivotloc];
            L.elem[pivotloc] = temp;
            pivotloc++;
        }
    }
    temp = L.elem[high];
    L.elem[high] = L.elem[pivotloc];
    L.elem[pivotloc] = temp;
    return pivotloc;
}
```
