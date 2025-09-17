
# 排序算法对比手册

## 📌 核心指标说明
- **时间复杂度**：算法执行时间随数据量增长的速率
- **稳定性 (Stability)**：相等元素的原始顺序是否保持不变
- **原地排序 (In-place)**：是否只需常量级额外空间
- **适用场景**：最佳使用情境

## 📊 算法对比表
| 算法名称         | 平均时间复杂度   | 最坏时间复杂度   | 空间复杂度 | 稳定性 | 原地排序 | 适用场景                     |
|------------------|------------------|------------------|------------|--------|----------|------------------------------|
| **插入排序**     | O(n²)            | O(n²)            | O(1)       | ✔️      | ✔️       | 小规模或基本有序数据         |
| **希尔排序**     | O(n log n)       | O(n²)            | O(1)       | ✘      | ✔️       | 中等规模数据                 |
| **堆排序**       | O(n log n)       | O(n log n)       | O(1)       | ✘      | ✔️       | 需要保证最坏性能的场景       |
| **归并排序**     | O(n log n)       | O(n log n)       | O(n)       | ✔️      | ✘       | 大数据量/链表排序/外部排序   |
| **快速排序**     | O(n log n)       | O(n²)            | O(log n)   | ✘      | ✔️       | 通用场景（实际最快）         |
| **桶排序**       | O(n + k)         | O(n²)            | O(n + k)   | ✔️      | ✘       | 均匀分布的数据               |
| **表排序**       | O(n log n)       | O(n log n)       | O(n)       | ✔️      | ✘       | 大元素移动成本高的场景       |

---

## 🧩 算法特性详解

### 1. 插入排序 (Insertion Sort)
```c
// C语言示例
void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
```
- **原理**：类似理扑克牌，将未排序元素插入已排序序列
- **优势**：小数据量时效率高；基本有序时接近O(n)
- **劣势**：大数据量性能急剧下降

### 2. 希尔排序 (Shell Sort)
```c
void shellSort(int arr[], int n) {
    for (int gap = n/2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j;
            for (j = i; j >= gap && arr[j-gap] > temp; j -= gap)
                arr[j] = arr[j-gap];
            arr[j] = temp;
        }
    }
}
```
- **原理**：分组插入排序（递减增量法）
- **优势**：比普通插入排序快5~10倍
- **关键点**：性能依赖步长序列选择

### 3. 堆排序 (Heap Sort)
```c
void heapify(int arr[], int n, int i) {
    int largest = i;
    int l = 2*i + 1;
    int r = 2*i + 2;
    
    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;
    
    if (largest != i) {
        swap(&arr[i], &arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(int arr[], int n) {
    for (int i = n/2 - 1; i >= 0; i--)
        heapify(arr, n, i);
        
    for (int i = n-1; i > 0; i--) {
        swap(&arr[0], &arr[i]);
        heapify(arr, i, 0);
    }
}
```
- **原理**：利用二叉堆（Heap）特性排序
- **优势**：最坏情况仍保持O(n log n)
- **劣势**：缓存不友好（跳跃访问内存）

### 4. 归并排序 (Merge Sort)
```c
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++) L[i] = arr[l+i];
    for (int j = 0; j < n2; j++) R[j] = arr[m+1+j];
    
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l)/2;
        mergeSort(arr, l, m);
        mergeSort(arr, m+1, r);
        merge(arr, l, m, r);
    }
}
```
- **原理**：分治法（Divide and Conquer）的典型应用
- **优势**：稳定且时间复杂度恒定
- **特殊价值**：外部排序（数据量大于内存时）

### 5. 快速排序 (Quick Sort)
```c
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j <= high-1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i+1], &arr[high]);
    return i+1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi-1);
        quickSort(arr, pi+1, high);
    }
}
```
- **原理**：选定基准值(pivot)分区排序
- **优势**：实际应用中速度最快
- **注意事项**：
  - 最坏情况可通过随机化pivot避免
  - C标准库`qsort()`即采用此算法

### 6. 桶排序 (Bucket Sort)
- **原理**：将数据分到有限数量的桶里，每桶单独排序
- **示例**：对0~99的整数排序，创建10个桶（0-9, 10-19...）
- **关键要求**：数据均匀分布
- **优势**：当\(k \approx n\)时可达O(n)

### 7. 表排序 (Table Sort / Indirect Sort)
```c
void tableSort(int arr[], int n) {
    int *table = malloc(n * sizeof(int)); // 创建指针表
    for (int i=0; i<n; i++) table[i] = i;
    
    // 对table排序（而非直接操作arr）
    for (int i=1; i<n; i++) 
        for (int j=i; j>0 && arr[table[j]] < arr[table[j-1]]; j--)
            swap(&table[j], &table[j-1]);
    
    // 按table顺序重排arr（物理排序）
    rearrange(arr, table, n);
    free(table);
}
```
- **原理**：通过指针表间接排序，减少大元素移动次数
- **典型场景**：排序大型结构体（如学生记录）
- **优势**：物理排序阶段仅需一次数据移动

---

## 💡 总结建议
1. **通用首选**：快速排序（注意随机化pivot）
2. **内存敏感**：堆排序（空间复杂度O(1)）
3. **稳定需求**：归并排序（或插入排序小数据）
4. **外部排序**：归并排序（处理海量数据）
5. **特定数据**：桶排序（均匀分布）/ 表排序（大元素）

> 实际工程中常采用混合策略，如：  
> `if (n < 16) insertionSort(arr);`  
> `else quickSort(arr);`

-----

# 面向题目学习


