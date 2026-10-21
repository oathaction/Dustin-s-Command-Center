"""Check the 28 chapter instruction lines and the red rule against their governing sources.

Usage: python3 -I ux_instruction_lines_check.py <project-root>

Governing sources:
  work/handoffs/phase-1/20261021_Voice-Line-And-Headlines.md, section 3   instruction lines (editor's final set)
  work/ledger/20261020_Decision-Log.md, D1-26                             red rule wording
Checked copies:
  work/ledger/20261021_Guide-Architecture-Map.md, section 2 table
  the guide shell: each chapter's h2 and instruction line, the Contents list and the part openers
  the board's contents table
  every quotation of the red rule in the map, the shell and the board
Exits 1 on any mismatch.
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
ed = (root / "work/handoffs/phase-1/20261021_Voice-Line-And-Headlines.md").read_text()
dlog = (root / "work/ledger/20261020_Decision-Log.md").read_text()
mp = (root / "work/ledger/20261021_Guide-Architecture-Map.md").read_text()
shell = (root / "work/boards/phase-1/navigation/20261021_Guide-Shell-Wireframe.html").read_text()
board = (root / "work/boards/20261021_Navigation-And-Template-Wireframes.html").read_text()


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


sec = ed.split("## 3. Headline system", 1)[1].split("## 4.", 1)[0]
want = {m.group(1): (m.group(2).strip(), m.group(3).strip())
        for m in re.finditer(r"^\| (\d\d) ([^|]+?) \| ([^|]+?) \| [a-z]+ \|$", sec, re.M)}
misses = []
counts = {}

# Map section 2.
m2 = mp.split("## 2. Proposed contents", 1)[1].split("## 3.", 1)[0]
got = {m.group(1): (m.group(2).strip(), m.group(3).strip()) for m in re.finditer(r"^\| (\d\d) \| ([^|]+) \| [^|]+ \| ([^|]+) \|", m2, re.M)}
counts["map"] = sum(1 for n, (name, line) in want.items() if got.get(n) == (name, line))
misses += [f"map {n}: {got.get(n)}" for n in want if got.get(n) != want[n]]

# Shell: h2 and the instruction line under it.
h2 = {}
for m in re.finditer(r'<h2 id="[a-z-]+-h"><span class="n">(\d\d)</span>(.*?)</h2>\s*<p class="instr">(.*?)</p>', shell, re.S):
    h2[m.group(1)] = (text(m.group(2)), text(m.group(3)))
counts["shell chapters"] = sum(1 for n in want if h2.get(n) == want[n])
misses += [f"shell h2 {n}: {h2.get(n)}" for n in want if h2.get(n) != want[n]]

# Shell: the Contents list and the part openers repeat the line under each chapter link.
for label, block in (("shell contents", shell.split('id="contents"', 1)[1].split('id="start"', 1)[0]),
                     ("shell part openers", "".join(re.findall(r'<ul class="part-list">.*?</ul>', shell, re.S)))):
    found = {m.group(1): (text(m.group(2)), text(m.group(3))) for m in re.finditer(r'<li><a href="#[a-z-]+"><span class="n">(\d\d)</span>(.*?)</a><p>(.*?)</p></li>', block, re.S)}
    counts[label] = sum(1 for n in want if found.get(n) == want[n])
    misses += [f"{label} {n}: {found.get(n)}" for n in want if found.get(n) != want[n]]

# Board contents table.
rows = {m.group(1): (text(m.group(2)), text(m.group(3))) for m in re.finditer(r'<td class="num">(\d\d)</td><td><strong>(.*?)</strong></td><td>(.*?)</td>', board)}
counts["board"] = sum(1 for n in want if rows.get(n) == want[n])
misses += [f"board {n}: {rows.get(n)}" for n in want if rows.get(n) != want[n]]

# Front matter and Closing lines in the shell.
front = {name: re.search(rf"^\| {name} \| ([^|]+?) \| [a-z]+ \|$", sec, re.M).group(1).strip() for name in ("Contents", "Where to start", "Closing")}
for name, line, hid in (("Contents", front["Contents"], "contents-h"), ("Where to start", front["Where to start"], "start-h"), ("Closing", front["Closing"], "closing-h")):
    m = re.search(rf'<h2 id="{hid}">.*?</h2>\s*<p class="instr">(.*?)</p>', shell, re.S)
    if not m or text(m.group(1)) != line:
        misses.append(f"shell {name}: {m and text(m.group(1))}")
counts["shell front and closing"] = 3 - sum(1 for x in misses if x.startswith("shell Contents") or x.startswith("shell Where") or x.startswith("shell Closing"))

# Red rule: every quotation matches D1-26.
row = [l for l in dlog.splitlines() if l.startswith("| D1-26 |")][0]
rule = re.search(r'quoted exactly on every board: "(.*)" \|', row).group(1)
starts = "The wordmark's ampersand and the lockmark's lever are signature red"
quotes = []
for label, src in (("map", mp), ("shell", html.unescape(shell)), ("board", html.unescape(board))):
    for m in re.finditer(re.escape(starts), src):
        seg = src[m.start():m.start() + len(rule) + 5]
        quotes.append((label, seg.startswith(rule)))
counts["red rule quotations"] = sum(1 for _, ok in quotes if ok)
misses += [f"red rule quotation in {l} differs from D1-26" for l, ok in quotes if not ok]
shell_053 = re.search(r'Rule 05.3</span> One working red per view.</h3>\s*<p>(.*?)</p>', shell, re.S)
if not shell_053 or text(shell_053.group(1)) != rule:
    misses.append("shell Rule 05.3 paragraph differs from D1-26")

print("Editor's table rows:", len(want))
for k, v in counts.items():
    print(f"{k}: {v}" + ("" if k.startswith("red") or k.startswith("shell front") else " of 28"))
print("red rule quotations found:", len(quotes))
if misses:
    print("Misses:")
    for x in misses:
        print("  " + x)
    sys.exit(1)
print("No misses.")
