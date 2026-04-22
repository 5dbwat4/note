https://leetcode.cn/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-100-liked


> 给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。
> 
>  
> 
> 示例 1:
> 
> 输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
> 
> 输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
> 
> 解释：
> 
> 在 strs 中没有字符串可以通过重新排列来形成 "bat"。
> 字符串 "nat" 和 "tan" 是字母异位词，因为它们可以重新排列以形成彼此。
> 字符串 "ate" ，"eat" 和 "tea" 是字母异位词，因为它们可以重新排列以形成彼此。
> 示例 2:
> 
> 输入: strs = [""]
> 
> 输出: [[""]]
> 
> 示例 3:
> 
> 输入: strs = ["a"]
> 
> 输出: [["a"]]
> 
>  
> 
> 提示：
> 
> 1 <= strs.length <= 104
> 0 <= strs[i].length <= 100
> strs[i] 仅包含小写字母


### 🧠 一、解题思路（新手友好版）

#### 1. 核心观察：什么是“字母异位词”？
字母异位词的本质是：**字符种类相同，且每种字符的出现次数也相同，只是排列顺序不同**。
例如：`"eat"`、`"tea"`、`"ate"` 都包含 1个a、1个e、1个t。

#### 2. 如何快速判断两个字符串是否属于同一组？
如果我们把每个字符串里的字符**按字母顺序排好序**，那么所有互为异位词的字符串，排序后一定会变成**完全一样的字符串**。
- `"eat"` → `"aet"`
- `"tea"` → `"aet"`
- `"ate"` → `"aet"`
这个排序后的字符串，就可以作为它们共同的**“身份证”（哈希表的键 Key）**。

#### 3. 算法步骤
1. 创建一个哈希表（字典/Map）。
2. 遍历输入的字符串数组：
   - 把当前字符串的字符排序，得到 `key`。
   - 把**原字符串**追加到哈希表中 `key` 对应的列表里。
3. 遍历结束后，哈希表中所有的“值（Value）”就是分好组的列表，把它们收集起来返回即可。

#### 4. 为什么这样设计性能高？
- **哈希表查找/插入**：平均时间复杂度 `O(1)`。
- **排序**：每个字符串长度为 `K`，排序耗时 `O(K log K)`。
- **总体时间复杂度**：`O(N * K log K)`（`N` 为字符串个数，`K` 为最大长度）。在题目限制下（`N ≤ 10^4`, `K ≤ 100`），计算量约 `7×10^6` 次操作，现代 CPU 只需几毫秒，完全满足性能要求。

> 💡 **进阶提示**：如果追求极致性能，可以用“字符计数数组”代替排序作为 Key，时间复杂度可降至 `O(N * K)`。但排序法代码更简洁，且在实际运行中常数很小，是面试和工程中最常用的写法。

---
### 💻 二、C++ 实现（注重性能与内存管理）

```cpp
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        // unordered_map 底层是哈希表，平均查找/插入时间 O(1)
        // 键(Key)：排序后的字符串； 值(Value)：原字符串组成的 vector
        unordered_map<string, vector<string>> anagramMap;

        // 使用常量引用 & 避免拷贝字符串，提升循环性能
        for (const string& s : strs) {
            // 复制一份当前字符串用于排序（不修改原数组中的字符串）
            string sorted_s = s;
            
            // std::sort 内部使用 Introsort，平均 O(K log K)，性能极佳
            sort(sorted_s.begin(), sorted_s.end());
            
            // [] 运算符：如果键不存在，会自动创建一个空的 vector<string>
            // 然后将原字符串 s 追加进去
            anagramMap[sorted_s].push_back(s);
        }

        // 准备返回结果
        vector<vector<string>> result;
        
        // 【性能优化】提前分配内存，避免后续 push_back 时频繁触发动态扩容
        result.reserve(anagramMap.size());

        // 遍历哈希表，提取所有分组
        for (auto& pair : anagramMap) {
            // std::move 将 vector 的内存所有权直接“转移”给 result
            // 避免深拷贝，大幅降低内存开销和运行时间
            result.push_back(move(pair.second));
        }

        return result;
    }
};
```

---
### 🌐 三、JavaScript 实现（注重现代语法与执行效率）

```javascript
/**
 * @param {string[]} strs
 * @return {string[][]}
 */
var groupAnagrams = function(strs) {
    // 使用 ES6 Map 而不是普通对象 {}
    // 原因：Map 的键可以是任意类型，遍历时保持插入顺序，且在大量数据下性能更稳定
    const anagramMap = new Map();

    // for...of 遍历数组，比传统 for 循环更简洁且性能在现代引擎中已高度优化
    for (const s of strs) {
        // JS 字符串是不可变的，所以需要：转数组 -> 排序 -> 拼接回字符串
        // 作为分组的唯一标识 Key
        const sortedKey = s.split('').sort().join('');

        // 【性能优化】如果 Map 中还没有这个 Key，初始化为空数组
        // 使用 has() 和 set() 是 Map 的标准高效操作
        if (!anagramMap.has(sortedKey)) {
            anagramMap.set(sortedKey, []);
        }

        // 将原字符串推入对应 Key 的分组中
        anagramMap.get(sortedKey).push(s);
    }

    // anagramMap.values() 返回一个迭代器，包含所有分组数组
    // Array.from() 能高效地将迭代器转为真正的二维数组并返回
    return Array.from(anagramMap.values());
};
```

