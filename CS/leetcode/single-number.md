```c
int singleNumber(int* nums, int numsSize) {
    int o=nums[0];
    for(int i=1;i<numsSize;i++){
        o^=nums[i];
    }
    return o;
}
```