# Priority Queues

其实就是Heap，binary heap其实就是一棵完全树

堆是一棵树，其每个节点都有一个键值，且每个节点的键值都大于等于/小于等于其父亲的键值。

每个节点的键值都大于等于其父亲键值的堆叫做小根堆，否则叫做大根堆。STL 中的 priority_queue 其实就是一个大根堆。

（小根）堆主要支持的操作有：插入一个数、查询最小值、删除最小值、合并两个堆、减小一个元素的值。

## 几个基本操作

1. **插入一个数**  
   想象堆是一个由小石头堆成的金字塔，每块石头都比下面的石头轻。当你插入一个新元素时，就像在金字塔底部放一块新石头。如果这块石头比它上方的石头轻，它会像气泡一样向上“漂浮”，直到找到自己的位置，确保它下方的石头都比它重。

2. **查询最小值**  
   金字塔的顶端始终是最轻的石头。要查询最小值，只需看一眼塔顶的石头。

3. **删除最小值**  
   要删除最轻的石头，你需要先拿走塔顶的石头，然后把最底层的石头放到塔顶。这时塔顶的石头可能比下方的石头重，于是它会像沙子一样逐渐“下沉”，直到找到合适的位置，重新形成稳定的金字塔。


## 一些代码实现

By deepseek

```c
typedef struct {
    int data[64]; // 使用索引1到63存储元素
    int size;
} MinHeap;

void initialize(MinHeap *heap) {
    heap->size = 0;
}

void insert(MinHeap *heap, int value) {
    if (heap->size >= 63) return; // 堆已满
    heap->size++;
    heap->data[heap->size] = value;
    percolateUp(heap, heap->size);
}

void percolateUp(MinHeap *heap, int pos) {
    int current = pos;
    while (current > 1) { // 当前不是根节点
        int parent = current / 2;
        if (heap->data[current] < heap->data[parent]) {
            swap(&heap->data[current], &heap->data[parent]);
            current = parent;
        } else {
            break;
        }
    }
}

int deleteMin(MinHeap *heap) {
    if (heap->size == 0) return -1; // 堆为空
    int min = heap->data[1];
    heap->data[1] = heap->data[heap->size];
    heap->size--;
    percolateDown(heap, 1);
    return min;
}

void percolateDown(MinHeap *heap, int pos) {
    int current = pos;
    while (current * 2 <= heap->size) { // 存在左子节点
        int left = current * 2;
        int right = left + 1;
        int min_child = left;
        if (right <= heap->size && heap->data[right] < heap->data[left]) {
            min_child = right;
        }
        if (heap->data[current] > heap->data[min_child]) {
            swap(&heap->data[current], &heap->data[min_child]);
            current = min_child;
        } else {
            break;
        }
    }
}

```


## $d$-Heap

All nodes have $d$ children instead of 2.

*Question: Shall we make d as large as possible?*

Note: 
- DeleteMin will take $d - 1$ comparisons to find the smallest child. Hence the total time complexity would be $O(d \log{d}{N})$.
- `*2` or `/2` is merely a bit shift, but `*d` or `/d` is not.
- When the priority queue is too large to fit entirely in main memory, a $d$-heap will become interesting.


If a d-heap is stored as an array, for an entry located in position i, the parent, the first child and the last child are at:

$$\lfloor (i+d-2)/d \rfloor, (i-1)d+2, \text{and} id+1$$