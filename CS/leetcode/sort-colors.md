```c
void sortColors(int* nums, int numsSize) {
    int a=0,b=0,c=0;
    for(int i=0;i<numsSize;i++){
        if(nums[i]==0)a++;
        if(nums[i]==1)b++;
        if(nums[i]==2)c++;
    }
    for(int i=0;i<a;i++)nums[i]=0;
    for(int i=a;i<a+b;i++)nums[i]=1;
    for(int i=a+b;i<a+b+c;i++)nums[i]=2;

}
```





评论区找到的另一个写法：

```java
class Solution {
    public void sortColors(int[] nums) {
        int num0 = 0, num1 = 0, num2 = 0;
        for(int i = 0; i < nums.length; i++) {
            if(nums[i] == 0) {
                nums[num2++] = 2;
                nums[num1++] = 1;
                nums[num0++] = 0;
            }else if(nums[i] == 1) {
                nums[num2++] = 2;
                nums[num1++] = 1;
            }else {
                nums[num2++] = 2;
            }
        }
    }
}
```



------------------


> 给定一个包含红色、白色和蓝色、共 `n` 个元素的数组 `nums` ，**原地** 对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。
> 
> 我们使用整数 `0`、 `1` 和 `2` 分别表示红色、白色和蓝色。
> 
> 必须在不使用库内置的 `sort` 函数的情况下解决这个问题。
> 
>  
> 
> **示例 1：**
> 
> 输入：`nums = [2,0,2,1,1,0]`
> 输出：`[0,0,1,1,2,2]`
> 
> **示例 2：**
> 
> 输入：`nums = [2,0,1]`
> 输出：`[0,1,2]`
> 
>  
> 
> **提示：**
> 
> - `n == nums.length`
> - `1 <= n <= 300`
> - `nums[i]` 为 `0`、`1` 或 `2`
> 
>  
> 
> **进阶：**
> 
> 你能想出一个仅使用常数空间的一趟扫描算法吗？