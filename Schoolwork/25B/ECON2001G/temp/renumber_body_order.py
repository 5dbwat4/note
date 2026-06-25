import re

with open("paper-final.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

ref_start = None
for i, line in enumerate(lines):
    if line.strip() == "## 参考文献":
        ref_start = i
        break

body = "\n".join(lines[:ref_start])
ref_lines = lines[ref_start+1:]

# Step 1: Find all citations in body in order of first appearance
citation_pattern = re.compile(r'\[(\d+)\]')
seen_nums = []
seen_set = set()
for m in citation_pattern.finditer(body):
    num = int(m.group(1))
    if num not in seen_set:
        seen_nums.append(num)
        seen_set.add(num)

print(f"Citations in order of first appearance ({len(seen_nums)}):")
print(seen_nums)

# Step 2: Build mapping old -> new (1..30)
mapping = {old: new for new, old in enumerate(seen_nums, 1)}

# Step 3: Build reference entries lookup by old number
ref_entries = {}
for line in ref_lines:
    line_stripped = line.strip()
    if line_stripped.startswith("[") and "]:" in line_stripped:
        bracket_end = line_stripped.index("]")
        num = int(line_stripped[1:bracket_end])
        # Extract the content after "]: "
        ref_entries[num] = line_stripped[bracket_end+2:]

# Step 4: Replace body citations using regex
def replace_citation(m):
    num = int(m.group(1))
    if num in mapping:
        return f"[{mapping[num]}]"
    return m.group(0)

new_body = citation_pattern.sub(replace_citation, body)

# Step 5: Build new reference section in order 1..30
new_ref_lines = []
for new_num in range(1, 31):
    # Find which old_num maps to this new_num
    old_num = seen_nums[new_num - 1]  # since mapping is 1-based
    entry = ref_entries[old_num]
    new_ref_lines.append(f"[{new_num}]: {entry}")

new_ref_section = "\n".join(new_ref_lines)

# Step 6: Assemble final content
new_content = new_body + "\n" + "## 参考文献" + "\n" + new_ref_section

with open("paper-final.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nDone. Reordered by body appearance.")
print("Old -> New mapping:")
for old in seen_nums:
    print(f"  [{old}] -> [{mapping[old]}]")
