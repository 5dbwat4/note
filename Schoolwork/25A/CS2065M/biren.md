# 实验报告：BIRENSUPA™ 编程入门 – 向量加法实现



## 一、 实验目的

1.  **理解 BIRENSUPA 编程模型**：初步掌握壁仞（BIREN）基于 Host-Device（主机-设备）架构的异构计算模型。
2.  **掌握核心编程概念**：理解核函数（Kernel Function）、线程（Thread）、线程块（Block）、网格（Grid）以及 SIMT（单指令多线程）执行模式。
3.  **熟悉运行时 API**：熟练使用 `suMallocDevice`、`suMemcpy`、`suLaunchKernel` 和 `suFree` 等核心运行时函数进行显存管理和任务调度。
4.  **实现并行计算**：利用 GPU 的大规模并行能力，实现两个一维向量的高效加法运算。

## 二、 实验原理

### 1. 异构计算架构
本实验基于 BIRENSUPA 软件栈，采用 **主机-设备（Host-Device）** 模型：

*   **主机（Host/CPU）**：负责复杂的逻辑控制、显存分配、数据传输以及核函数的启动。
*   **设备（Device/GPU）**：拥有大量的计算单元，负责执行高并发的计算任务。

### 2. 向量加法的并行化
传统的 CPU 向量加法通过循环串行执行，时间复杂度为 $O(N)$。在 GPU 上，我们将向量的每一个元素的加法分配给一个独立的线程去处理。假设有 $N$ 个元素，理论上启动 $N$ 个线程同时计算，时间复杂度可降低至 $O(1)$（理想并行状态下）。

### 3. 线程索引计算
为了让每个线程处理不同的数据元素，需要利用内置变量计算全局唯一的索引（Global Index）。计算公式如下：

$$ 
\text{idx} = \text{thread\_idx.x} + \text{block\_idx.x} \times \text{block\_dim.x} 
$$

*   `thread_idx.x`：当前线程在线程块内的偏移。
*   `block_idx.x`：当前线程块在网格中的偏移。
*   `block_dim.x`：一个线程块包含的线程数量。

同时需要进行**边界检查**：`if (idx < length)`，防止线程索引越界访问内存。

## 三、 实验内容与代码实现

### 1. 核心代码逻辑分析

实验主要包含两部分代码：运行在 GPU 上的核函数和运行在 CPU 上的主机函数。

#### (1) 核函数实现 (`vectorAdd`)
**功能**：每个线程计算一个位置的加法。

**代码解析**：
```cpp
__global__ void vectorAdd(int *dst, int *src1, int *src2, int length) {
    // 1. 计算当前线程的全局唯一索引
    size_t idx = thread_idx.x + block_idx.x * block_dim.x;
    
    // 2. 边界检查：确保索引在向量长度范围内
    // 只有在范围内的线程才执行加法及写回操作
    if (idx < length) {
        dst[idx] = src1[idx] + src2[idx];
    }
}
```

#### (2) 主机函数实现 (`vectorAddHostFunc`)
**功能**：管理资源并调度 GPU 计算。

**关键步骤**：
1.  **显存分配**：使用 `suMallocDevice` 为输入向量 `src1`, `src2` 和输出向量 `dst` 在设备端分配空间。
2.  **数据传输**：使用 `suMemcpy` 将主机端初始化的数据拷贝到设备端。
3.  **网格维度计算**：为了处理 `length` 长度的数据，且每个 Block 大小为 1024，Grid 大小计算公式为 `(length + 1023) / 1024`（向上取整）。
4.  **启动核函数**：调用 `suLaunchKernel`。
5.  **结果回传**：计算完成后，将结果从设备端拷回主机端。
6.  **资源释放**：使用 `suFree` 释放设备显存。

**代码实现**：
```cpp
void vectorAddHostFunc(int *dst, int *src1, int *src2, int length) {
    int *src1_dev, *src2_dev, *dst_dev;
    
    // 1. 分配设备显存 (Device Memory Allocation)
    suMallocDevice((void **)&src1_dev, length * sizeof(int));
    suMallocDevice((void **)&src2_dev, length * sizeof(int));
    suMallocDevice((void **)&dst_dev, length * sizeof(int));

    // 2. 数据从主机拷贝到设备 (Host to Device)
    suMemcpy(src1_dev, src1, length * sizeof(int));
    suMemcpy(src2_dev, src2, length * sizeof(int));

    // 3. 计算 Grid 和 Block 维度
    // 设定 Block 大小为 1024 线程
    // Grid 大小 = (总数据量 + Block大小 - 1) / Block大小，实现向上取整
    dim3 grid((length + 1023) / 1024);

    // 4. 启动核函数 (Launch Kernel)
    suLaunchKernel(vectorAdd, grid, 1024, 0, NULL, dst_dev, src1_dev,
                    src2_dev, length);

    // 5. 结果从设备拷贝回主机 (Device to Host)
    suMemcpy(dst, dst_dev, length * sizeof(int)); 

    // 6. 释放设备资源 (Free Resource)
    suFree(src1_dev);
    suFree(src2_dev);
    suFree(dst_dev);
}
```

## 四、 实验结果

### 1. 验证逻辑
*   数据规模：`length = 1,000,000`。
*   输入数据：`src1` 全为 2，`src2` 全为 3。
*   预期结果：`dst` 全为 5。
*   检查程序：遍历 `dst` 数组，若所有元素均为 5，则输出 "Test pass!"。

### 2. 运行结果
编译并运行程序后，终端输出如下：
```text
Test pass!
```
该输出表明 GPU 并行计算结果正确，所有 100 万个元素的加法均已正确执行并写回主机内存。

## 五、 实验总结与心得

通过本次实验，我完成了 BIRENSUPA 编程模型的入门实践，主要收获如下：

1.  **并行思维的转变**：从 CPU 的串行循环思维（For-Loop）转变为 GPU 的单指令多线程思维（SIMT）。不再关注如何遍历数组，而是关注单个线程如何通过索引（Index）定位自己的数据。
2.  **显存管理的必要性**：深刻理解了主机内存（Host Memory）与设备显存（Device Memory）是物理隔离的。必须显式地分配显存并在两者之间搬运数据，这是 GPU 编程的基础。
3.  **网格维度的配置**：学会了如何根据数据总量和线程块大小计算网格大小（Grid Size）。特别是 `(N + block_dim - 1) / block_dim` 这种向上取整的写法，能确保即使数据量不能整除线程块大小时，也能覆盖所有数据。
4.  **边界检查的重要性**：在核函数中加入 `if (idx < length)` 是防止内存越界崩溃的关键，因为启动的线程总数通常会略多于实际数据量。

本次实验成功验证了壁仞 GPU 在处理向量加法这类数据并行任务上的有效性，为后续学习更复杂的 GPU 算子开发打下了基础。