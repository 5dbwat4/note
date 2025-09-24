---
title: PTA 程序题
---
# 7-1 Root of AVL Tree

Author 陈越


An AVL tree is a self-balancing binary search tree.  In an AVL tree, the heights of the two child subtrees of any node differ by at most one; if at any time they differ by more than one, rebalancing is done to restore this property.  Figures 1-4 illustrate the rotation rules.

![F1.jpg](https://images.ptausercontent.com/d265ae37-4348-4585-b39f-0b2e2e0a24f5.jpg)

![F2.jpg](https://images.ptausercontent.com/4a9f6fbd-e21e-4493-834d-7782e13bee4e.jpg)

![F3.jpg](https://images.ptausercontent.com/7dc0e66f-c458-4c92-bb8e-55b7bf6391ce.jpg)

![F4.jpg](https://images.ptausercontent.com/b17a9687-6be8-4256-873d-6a747154a58d.jpg)

Now given a sequence of insertions, you are supposed to tell the root of the resulting AVL tree.### Input Specification:

Each input file contains one test case.  For each case, the first line contains a positive integer **N** (**≤**20) which is the total number of keys to be inserted.  Then **N** distinct integer keys are given in the next line.  All the numbers in a line are separated by a space.

\### Output Specification:

For each test case, print the root of the resulting AVL tree in one line.

\### Sample Input 1:

```in
5
88 70 61 96 120
```

\### Sample Output 1:

```out
70
```

\### Sample Input 2:

```
7
88 70 61 96 120 90 65
```

\### Sample Output 2:

```
88
```

## Personal Sol

```c
#include <stdio.h>
#include <stdlib.h>
struct AVLND;
typedef struct AVLND *AVLPtr;
struct AVLND{
    int inner;
    AVLPtr left,right;
    int height;
};

int max(int a,int b){return a>b?a:b;}

int h(AVLPtr x){
    if(x==NULL){return -1;}
    else{return x->height;}
}
int bf(AVLPtr x){
    return h(x->left)-h(x->right);
}
void updH(AVLPtr x){
    if(x !=NULL)x -> height = max(h(x->left),h(x->right))+1;
}

AVLPtr L(AVLPtr Root){
    AVLPtr bx = Root->right;
    AVLPtr bcb = Root -> right -> left;
    bx -> left = Root;
    bx -> left ->right = bcb;
    updH(bcb);
    updH(Root);
    updH(bx);
    return bx;
}

AVLPtr R(AVLPtr Root){
    AVLPtr ee = Root -> left;
    AVLPtr adb = Root -> left -> right;
    ee -> right = Root;
    ee ->right -> left = adb;
    updH(adb);
    updH(Root);
    updH(ee);
    return ee;
}
    
AVLPtr insert(int nd,AVLPtr Root){
    
    if(Root==NULL){
        AVLPtr nvl = malloc(sizeof(struct AVLND));
        nvl->left=nvl->right=NULL;
        nvl->inner=nd;
        nvl->height=0;
        return nvl;
    }
    // printf("Root is %p %d\n",Root,Root->inner);
    if(nd<Root->inner){
        Root->left = insert(nd,Root->left);
    }else{
        Root->right = insert(nd,Root->right);
    }
    // printf("Begin attempt ro %d %p %p bf:%d\n",Root->inner,Root->left,Root->right,bf(Root));
    // Rotation attempt
    updH(Root);
    if(bf(Root)==2){
        if(bf(Root->left)==-1){
            Root->left = L(Root->left);
        }
        return R(Root);
    }
    if(bf(Root)==-2){
        if(bf(Root->right)==1){
            Root->right = R(Root->right);
        }
        return L(Root);
    }
    // printf("Now ""Root is %p %d\n",Root,Root->inner);
    return Root;
}


int main(){
    int n;
    scanf("%d",&n);
    AVLPtr nt = NULL;
    while(n--){
        int fk;
        scanf("%d",&fk);
        // printf("Sending %d\n",fk);
        nt = insert(fk,nt);
    }
    printf("%d",nt->inner);
    return 0;
}
```