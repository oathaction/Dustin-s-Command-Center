"""Check that the Guide Architecture Map accounts for every V5 Polished and V4.2 chapter.

Usage: python3 -I ux_architecture_coverage.py <project-root>

Reads:
  work/extract/v5-polished/inventory.json      V5 section ids
  work/extract/v4-2/inventory.json             V4.2 section ids
  work/handoffs/phase-0/ux-data/20261020_UX-Structure-Data.json   V5 h3 headings per chapter
  work/ledger/20261021_Guide-Architecture-Map.md
Prints a summary and every miss. Exits 1 when anything is missing.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
v5_inv = json.loads((root / "work/extract/v5-polished/inventory.json").read_text())
v42_inv = json.loads((root / "work/extract/v4-2/inventory.json").read_text())
struct = json.loads((root / "work/handoffs/phase-0/ux-data/20261020_UX-Structure-Data.json").read_text())
md = (root / "work/ledger/20261021_Guide-Architecture-Map.md").read_text()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("’", "'"))


misses = []

# 1. V5 sections: each has a "### V5 NN ... (`id`)" block.
v5_blocks = {}
for m in re.finditer(r"^### V5 \d\d [^\n]*\(`([a-z0-9-]+)`\)\n(.*?)(?=^### |^## )", md, re.S | re.M):
    v5_blocks[m.group(1)] = m.group(2)
v5_ids = [s["id"] for s in v5_inv["sections"]]
v5_found = [i for i in v5_ids if i in v5_blocks]
for i in v5_ids:
    if i not in v5_blocks:
        misses.append(f"V5 section not mapped: {i}")

# 2. V5 h3 headings: each appears in its chapter's block (spaces and punctuation ignored).
h3 = [(h["chapter"], h["text"]) for h in struct["headings"] if h["lvl"] == 3]
h3_found = 0
for chap, text in h3:
    block = norm(v5_blocks.get(chap, ""))
    if norm(text) and norm(text) in block:
        h3_found += 1
    else:
        misses.append(f"V5 h3 not found in its chapter block: [{chap}] {text}")

# 3. V4.2 sections: each id appears in the V4.2 table as (`id`).
v42_part = md.split("## 7. V4.2", 1)[1].split("## 8.", 1)[0]
v42_ids = [s["id"] for s in v42_inv["sections"]]
v42_found = [i for i in v42_ids if f"(`{i}`)" in v42_part]
for i in v42_ids:
    if i not in v42_found:
        misses.append(f"V4.2 section not mapped: {i}")

# 4. V6 chapters: each number 01 to 28 has a contents row and a cross-reference row.
contents = md.split("## 2. Proposed contents", 1)[1].split("## 3.", 1)[0]
xref = md.split("## 10. Cross-reference plan", 1)[1].split("## 11.", 1)[0]
chap_ok = 0
for n in range(1, 29):
    num = f"{n:02d}"
    in_contents = re.search(rf"^\| {num} \| [^|]+\| [^|]+\|", contents, re.M) is not None
    in_xref = re.search(rf"^\| {num} \| [^|]+\|", xref, re.M) is not None
    if in_contents and in_xref:
        chap_ok += 1
    else:
        misses.append(f"V6 chapter {num}: contents row {in_contents}, cross-reference row {in_xref}")

# 5. Every V6 home named in the V5 tables is a real chapter number or a named front or end section.
homes_bad = []
for chap, block in v5_blocks.items():
    for row in re.findall(r"^\| (?!V5 unit|---)[^|]*\| ([^|]+) \|", block, re.M):
        for num in re.findall(r"\b(\d\d)\b", row):
            if not 1 <= int(num) <= 28:
                homes_bad.append(f"[{chap}] home cites {num}: {row.strip()}")
misses.extend(homes_bad)

print(f"V5 sections mapped: {len(v5_found)} of {len(v5_ids)}")
print(f"V5 h3 headings found in a mapping row: {h3_found} of {len(h3)}")
print(f"V4.2 sections mapped: {len(v42_found)} of {len(v42_ids)}")
print(f"V6 chapters with a contents row and a cross-reference row: {chap_ok} of 28")
print(f"Home cells citing a chapter number outside 01 to 28: {len(homes_bad)}")
if misses:
    print("\nMisses:")
    for m in misses:
        print("  " + m)
    sys.exit(1)
print("No misses.")
