import re

with open("paper-final.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
ref_start = None
for i, line in enumerate(lines):
    if line.strip() == "## 参考文献":
        ref_start = i
        break

body_lines = lines[:ref_start]
ref_lines = lines[ref_start+1:]

# Extract old reference numbers in order they appear in bibliography
old_nums = []
for line in ref_lines:
    line = line.strip()
    if line.startswith("[") and "]:" in line:
        num_str = line[1:line.index("]")]
        old_nums.append(int(num_str))

# Build mapping sorted by old number -> new sequential
sorted_old = sorted(old_nums)
mapping = {old: new for new, old in enumerate(sorted_old, 1)}

# Use regex to find all [N] patterns in body and replace using mapping
def replace_body_citation(m):
    num = int(m.group(1))
    if num in mapping:
        return f"[{mapping[num]}]"
    return m.group(0)

body_text = "\n".join(body_lines)
body_text = re.sub(r'\[(\d+)\]', replace_body_citation, body_text)

# Replace in ref lines using regex
def replace_ref_citation(m):
    num = int(m.group(1))
    if num in mapping:
        return f"[{mapping[num]}]:"
    return m.group(0)

ref_text = "\n".join(ref_lines)
ref_text = re.sub(r'\[(\d+)\]:', replace_ref_citation, ref_text)

new_content = body_text + "\n" + "## 参考文献" + "\n" + ref_text

with open("paper-final.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done. Old -> New mapping:")
for old in sorted_old:
    print(f"  [{old}] -> [{mapping[old]}]")
