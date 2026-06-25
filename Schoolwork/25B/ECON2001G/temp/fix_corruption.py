import re

with open("paper-final.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
ref_start = None
for i, line in enumerate(lines):
    if line.strip() == "## 参考文献":
        ref_start = i
        break

# The corrupted references: old[68] became [2] instead of [14], old[101] became [3] instead of [27]
# In the ref section, identify the [2] line that should be [14] and [3] line that should be [27]

ref_lines = lines[ref_start+1:]
body = "\n".join(lines[:ref_start])

# Identify corrupted ref line: old [68] content starts with "人民网"
# It is currently labeled [2] instead of [14]
# old [101] content starts with "刘同山" or "郧宛琪"... wait let me check:
# [101] was 刘同山.农地流转不畅对粮食产量有何影响?
# [102] was 郧宛琪,朱道林,梁梦茵.解决土地碎片化的制度框架设计
# [2] (correct) was 丰雷,任芷仪,张清勇.家庭联产承包责任制改革...

# Original mapping (from old numbers):
# [14] -> [2] (丰雷)
# [27] -> [3] (严金明)
# [68] -> [14] (人民网) BUT got corrupted to [2]
# [101] -> [27] (刘同山) BUT got corrupted to [3]

# So in the current corrupted file, ref [14] is missing, ref [27] is missing
# Instead we have two [2] entries and two [3] entries

# Strategy: 
# 1. Find the ref line with content "人民网" (old [68]) and change its label from [2] to [14]
# 2. Find the ref line with content "刘同山" (old [101]) and change its label from [3] to [27]
# 3. In the body, find citations of [68] context ("长久不变") and change [2] to [14]
# 4. In the body, find citations of [101] context ("细碎化") and change [3] to [27]

# Fix reference section
new_ref_lines = []
for line in ref_lines:
    if line.strip().startswith("[") and "]" in line:
        # Check if this is the corrupted line
        if "人民网" in line and "推进农村改革发展" in line:
            line = line.replace("[2]:", "[14]:", 1)
            print(f"Fixed ref: old[68] -> [14] (was corrupted to [2])")
        elif "刘同山" in line:
            line = line.replace("[3]:", "[27]:", 1)
            print(f"Fixed ref: old[101] -> [27] (was corrupted to [3])")
    new_ref_lines.append(line)

ref_text = "\n".join(new_ref_lines)

# Fix body: find citations where old [68] was used (should now be [14])
# Context: "长久不变"[68]
body = body.replace("长久不变\"[2]", "长久不变\"[14]")
# Context: [68] at end of sentence about 承包关系
body = body.replace("长久不变\"[2]。", "长久不变\"[14]。")

# Fix body: find citations where old [101] was used (should now be [27])
# Context: "典型特征"[101]
body = body.replace("典型特征[3]", "典型特征[27]")

new_content = body + "\n" + "## 参考文献" + "\n" + ref_text

with open("paper-final.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nFixed. Now running renumber properly...")
