import re

with open("paper-final.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# Find the line where "## 参考文献" starts
ref_start = None
for i, line in enumerate(lines):
    if line.strip() == "## 参考文献":
        ref_start = i
        break

if ref_start is None:
    print("ERROR: Could not find '## 参考文献'")
    exit(1)

body = "\n".join(lines[:ref_start])
ref_section = "\n".join(lines[ref_start+1:])

# Extract reference numbers from the reference section
ref_numbers_in_refs = []
for line in ref_section.split("\n"):
    line = line.strip()
    if line.startswith("[") and "]:" in line:
        num_str = line[1:line.index("]")]
        ref_numbers_in_refs.append(int(num_str))

# Find all citation markers in body text, e.g. [1], [14], [59]
citation_pattern = re.compile(r'\[(\d+)\]')
body_citations = set()
for m in citation_pattern.finditer(body):
    body_citations.add(int(m.group(1)))

ref_set = set(ref_numbers_in_refs)

print(f"Total references listed in 参考文献: {len(ref_set)}")
print(f"Unique citations found in body text: {len(body_citations)}")
print()

missing = ref_set - body_citations
extra = body_citations - ref_set

if missing:
    print(f"References in bibliography but NOT cited in body ({len(missing)}):")
    for n in sorted(missing):
        print(f"  [{n}]")
else:
    print("All references in bibliography are cited in the body text [OK]")

print()

if extra:
    print(f"Citations in body but NOT in bibliography ({len(extra)}):")
    for n in sorted(extra):
        print(f"  [{n}]")
else:
    print("All body citations have corresponding bibliography entries [OK]")
