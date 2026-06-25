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

# Get ref numbers from bibliography
ref_nums = []
for line in ref_section.split("\n"):
    line = line.strip()
    if line.startswith("[") and "]:" in line:
        num = int(line[1:line.index("]")])
        ref_nums.append(num)

print(f"References in bibliography ({len(ref_nums)}): {ref_nums}")
print(f"Expected: {list(range(1, 31))}")
print(f"Match: {ref_nums == list(range(1, 31))}")
print()

# Get all citations in body
all_cites = [int(m.group(1)) for m in re.finditer(r'\[(\d+)\]', body)]
counter = Counter(all_cites)
body_set = set(all_cites)

print(f"Unique citations in body ({len(body_set)}): {sorted(body_set)}")
print(f"All in 1..30: {all(n >= 1 and n <= 30 for n in body_set)}")
print()

# Check for any remaining old numbers
old_nums = {1, 14, 27, 39, 44, 52, 53, 55, 56, 59, 62, 63, 64, 68, 69, 70, 74, 76, 77, 80, 84, 90, 93, 94, 95, 96, 101, 102, 103, 104}
new_nums = set(range(1, 31))

# Check if any old number that is NOT in 1..30 appears
stray = body_set - new_nums
if stray:
    print(f"STRAY old numbers in body: {sorted(stray)}")
else:
    print("No stray old numbers in body [OK]")

# Check for duplicates
dupes = {k: v for k, v in counter.items() if v > 1}
if dupes:
    print(f"Duplicate citations: {dupes}")
else:
    print("All citations unique [OK]")

print()

# Print a few body lines to verify visually
for line in lines[:5]:
    print(line)
