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

citation_pattern = re.compile(r'\[(\d+)\]')
all_citations = [int(m.group(1)) for m in citation_pattern.finditer(body)]
counter = Counter(all_citations)

multi = {k: v for k, v in counter.items() if v > 1}

if multi:
    print(f"References cited more than once ({len(multi)}):")
    for n, count in sorted(multi.items()):
        print(f"  [{n}]: {count} times")
else:
    print("Every reference is cited exactly once in the body text.")
