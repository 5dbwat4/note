---
title: PTA 程序题
---

p.s. 解答均为个人解答，本人*没有竞赛经验，码风不好，写出来的代码一般也是比较混乱、不是最优解*，而且不是AI写的，仅供参考。


# Root of AVL Tree

Author 陈越


An AVL tree is a self-balancing binary search tree.  In an AVL tree, the heights of the two child subtrees of any node differ by at most one; if at any time they differ by more than one, rebalancing is done to restore this property.  Figures 1-4 illustrate the rotation rules.

![F1.jpg](https://images.ptausercontent.com/d265ae37-4348-4585-b39f-0b2e2e0a24f5.jpg)

![F2.jpg](https://images.ptausercontent.com/4a9f6fbd-e21e-4493-834d-7782e13bee4e.jpg)

![F3.jpg](https://images.ptausercontent.com/7dc0e66f-c458-4c92-bb8e-55b7bf6391ce.jpg)

![F4.jpg](https://images.ptausercontent.com/b17a9687-6be8-4256-873d-6a747154a58d.jpg)

Now given a sequence of insertions, you are supposed to tell the root of the resulting AVL tree.
\### Input Specification:

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


# Self-printable B+ Tree


In this project, you are supposed to implement a B+ tree of order 3, with the following operations: initialize, insert (with splitting) and search.  The B+ tree should be able to print out itself.

\### Input Specification:

Each input file contains one test case.  For each case, the first line contains a positive number N ($$\le 10^4$$), the number of integer keys to be inserted.  Then a line of the N positive integer keys follows.  All the numbers in a line are separated by spaces.

\### Output Specification:

For each test case, insert the keys into an initially empty B+ tree of order 3 according to the given order.  Print in a line `Key X is duplicated` where `X` already exists when being inserted.  After all the insertions, print out the B+ tree in a top-down lever-order format as shown by the samples.

\### Sample Input 1:
```in
6
7 8 9 10 7 4
```

\### Sample Output 1:
```out
Key 7 is duplicated
[9]
[4,7,8][9,10]
```

\### Sample Input 2:
```
10
3 1 4 5 9 2 6 8 7 0
```

\### Sample Output 2:
```
[6]
[2,4][8]
[0,1][2,3][4,5][6,7][8,9]
```

\### Sample Input 3:
```
3
1 2 3
```

\### Sample Output 3:
```
[1,2,3]
```



## Personal Sol

```c
#include <stdio.h>
#include <stdlib.h>

#define ORDER 3
void BEGIN_OF_CUSTOM_CODE(){}


struct BPlusTreeNode;
typedef struct BPlusTreeNode BPlusTreeNode;
struct BPlusTreeNode
{
    int isLeaf;
    int numKeys;
    int keys[ORDER + 1]; // We also store the first key of first child in internal nodes, for convenience
    BPlusTreeNode *children[ORDER + 1];
    BPlusTreeNode *parent;
    int key_to_insert;
    BPlusTreeNode *child_to_insert;
};

BPlusTreeNode *createNode(int isLeaf)
{
    BPlusTreeNode *newNode = (BPlusTreeNode *)malloc(sizeof(BPlusTreeNode));
    newNode->isLeaf = isLeaf;
    newNode->numKeys = 0;
    newNode->parent = NULL;
    newNode->key_to_insert = -1;
    newNode->child_to_insert = NULL;
    for (int i = 0; i < ORDER + 1; i++)
    {
        newNode->children[i] = NULL;
        newNode->keys[i] = -1;
    }
    return newNode;
}

int find(BPlusTreeNode *root, int key)
{
    size_t i = 0;
    for(;i < root->numKeys; i++){
        if(root->keys[i] == key){
            return 71;
        }
        if(root->keys[i] > key){
            break;
        }
    }
    if(root->isLeaf){
        return 0;
    }
    if(i == 0){
        return 0;
    }
    // printf("At node %p, go to child %d\n", root, i);
    return find(root->children[i-1], key);
}

BPlusTreeNode *insert(BPlusTreeNode *node, int key)
{
    // before insert
    // printf("I am %p, my parent is %p\n", node, node->parent);
    // do insert
    if (node->isLeaf)
    {
        node->key_to_insert = key;
        node->child_to_insert = NULL;
    }
    else
    {
        // find child to insert
        int i = 0;
        if (key < node->keys[0])
        {
            node->keys[0] = key;
        }
        while (i < node->numKeys && key >= node->keys[i])
        {
            i++;
        }
        // printf("Go to child %d of node %p\n", i, node);
        node->children[i-1] = insert(node->children[i-1], key);

    }
    // check
    if (node->key_to_insert != -1)
    {
        // printf("Node %p need to insert key %d\n", node, node->key_to_insert);
        // if not full
        if (node->numKeys <= ORDER - 1)
        {
            int i = node->numKeys - 1;
            while (i >= 0 && node->keys[i] >= node->key_to_insert)
            {
                node->keys[i + 1] = node->keys[i];
                node->children[i + 1] = node->children[i];
                i--;
            }
            node->keys[i + 1] = node->key_to_insert;
            node->children[i + 1] = node->child_to_insert;
            node->numKeys++;
            node->key_to_insert = -1;
            node->child_to_insert = NULL;
            return node;
        }
        // if full
        // Temporally store the new key and child
        int i = node->numKeys - 1;
        while (i >= 0 && node->keys[i] >= node->key_to_insert)
        {
            // printf("Shift key %d and child %p to index %d\n", node->keys[i], node->children[i], i + 1);
            node->keys[i + 1] = node->keys[i];
            node->children[i + 1] = node->children[i];
            i--;
        }
        node->keys[i + 1] = node->key_to_insert;
        node->children[i + 1] = node->child_to_insert;
        node->numKeys++;// Now node has ORDER + 1 keys
        // printf("Node %p is full(keys=%d), need to split\n", node, node->numKeys);
        // Split
        BPlusTreeNode *newNode = createNode(node->isLeaf);
        int midIndex = (node->numKeys) / 2;
        for (size_t i = 0; i < midIndex; i++)
        {
            newNode->keys[i] = node->keys[i + midIndex];
            if(node->children[i + midIndex]){
                newNode->children[i] = node->children[i + midIndex];
                newNode->children[i]->parent = newNode;
            }
        }
        newNode->numKeys = node->numKeys - midIndex;
        node->numKeys = midIndex;
        newNode->parent = node->parent;
        node->key_to_insert = -1;
        node->child_to_insert = NULL;
        // printf("Node %p(%d,%d) is split into node %p(%d,%d)\n", node,node->keys[0], node->keys[1], newNode, newNode->keys[0], newNode->keys[1]);
        // if i am not root
        if(node->parent){
            node->parent->key_to_insert = newNode->keys[0];
            node->parent->child_to_insert = newNode;
            return node;
        }else{
            // if i am root
            BPlusTreeNode *newRoot = createNode(0);
            newRoot->keys[0] = node->keys[0];
            newRoot->keys[1] = newNode->keys[0];
            newRoot->children[0] = node;
            newRoot->children[1] = newNode;
            newRoot->numKeys = 2;
            node->parent = newRoot;
            newNode->parent = newRoot;
            return newRoot;
        }
    }
    return node;
}

void print_self_levelorder(BPlusTreeNode *root)
{
    if (!root){
        return;}
    BPlusTreeNode **queue = (BPlusTreeNode **)malloc(100000 * sizeof(BPlusTreeNode *));
    int front = 0, rear = 0;
    queue[rear++] = root;
    while (front < rear){
        int levelSize = rear - front;
        for (int i = 0; i < levelSize; i++){
            BPlusTreeNode *node = queue[front++];
            printf("[");
            if(node->isLeaf){
            // if(1){
            for (int j = 0; j < node->numKeys; j++){
                printf("%d", node->keys[j]);
                if (j < node->numKeys - 1){
                    printf(",");}
            }
            }else{
                for (int j = 1; j < node->numKeys; j++){
                printf("%d", node->keys[j]);
                if (j < node->numKeys - 1){
                    printf(",");}
            }
            }

            printf("]");
            if (!node->isLeaf){
                for (int j = 0; j < node->numKeys; j++){
                    queue[rear++] = node->children[j];
                }
            }
        }
        printf("\n");
    }
    free(queue);
}

void check_tree(BPlusTreeNode *node)
{
    if (!node)
        return;
    printf("Node %p, isLeaf: %d, numKeys: %d, keys: ", node, node->isLeaf, node->numKeys);
    printf("Parent: %p, ", node->parent);
    for (int i = 0; i < node->numKeys; i++)
    {
        printf("%d ", node->keys[i]);
    }
    printf("\n");
    if (!node->isLeaf)
    {
        printf("Children of node %p:\n", node);
        for (int i = 0; i <= node->numKeys; i++)
        {
            check_tree(node->children[i]);
        }
    }
}

int main()
{
    int n;
    scanf("%d", &n);
    BPlusTreeNode *root = createNode(1);
    int key;
    while (n--)
    {
        scanf("%d", &key);
        if (find(root, key))
        {
            printf("Key %d is duplicated\n", key);
            continue;
        }
        root = insert(root, key);
        // check_tree(root);
    }
    print_self_levelorder(root);
}
```