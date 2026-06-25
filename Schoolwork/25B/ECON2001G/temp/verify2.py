import re
from collections import Counter

with open("paper-final.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
ref_start = None
for i, line in enumerate(lines):
    if line.strip() == "## 参考文献":
        ref_start = i
        break

body = "\n".join(lines[:ref_start])
ref_section = "\n".join(lines[ref_start+1:])

# Get ref numbers
ref_nums = []
for line in ref_section.split("\n"):
    line = line.strip()
    if line.startswith("[") and "]:" in line:
        num = int(line[1:line.index("]")])
        ref_nums.append(num)

print(f"References: {ref_nums}")
print(f"Expected:  [1..30]")
print(f"Match: {ref_nums == list(range(1, 31))}")
print()

# Body citations
all_cites = [int(m.group(1)) for m in re.finditer(r'\[(\d+)\]', body)]
counter = Counter(all_cites)
body_set = set(all_cites)

print(f"Unique body citations: {sorted(body_set)}")
print(f"Missing in body: {sorted(set(range(1,31)) - body_set)}")
print(f"Extra in body: {sorted(body_set - set(range(1,31)))}")
print()

dupes = {k: v for k, v in counter.items() if v > 1}
if dupes:
    print(f"DUPLICATE citations: {dupes}")
else:
    print("All citations unique [OK]")
