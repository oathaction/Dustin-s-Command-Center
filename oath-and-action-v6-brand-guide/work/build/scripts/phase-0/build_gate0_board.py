"""Build the Gate 0 review board from its template, the Gate 0 report and the open questions.

Usage: python3 -I build_gate0_board.py <project-root>
The rubric and tension tables come from the report, so the board and the report cannot disagree.
"""
import base64
import html
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1])
BOARDS = os.path.join(ROOT, "work", "boards")
LEDGER = os.path.join(ROOT, "work", "ledger")


def md_table(text, heading):
    """Rows of the first Markdown table after a heading line that starts with `heading`."""
    start = text.index(heading)
    rows = []
    for line in text[start:].splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            rows.append(cells)
        elif rows:
            break
    return rows[1:]


def esc(s):
    s = html.escape(s, quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


report = open(os.path.join(LEDGER, "20261020_Gate-0-Report.md"), encoding="utf-8").read()
questions = open(os.path.join(LEDGER, "20261020_Open-Questions.md"), encoding="utf-8").read()

rubric = []
for r in md_table(report, "| Chapter | Craft"):
    cells = "".join(f'<td class="s s{v}">{v}</td>' for v in r[1:7])
    rubric.append(f"<tr><th scope=\"row\">{esc(r[0])}</th>{cells}<td>{esc(r[7])}</td></tr>")

tensions = []
for r in md_table(report, "| # | Tension | Status"):
    status = r[2]
    label = "Corrected" if status.startswith("Corrected") else ("Wider" if "wider" in status else "Confirmed")
    tensions.append(f"<tr><td>{r[0]}</td><td>{esc(r[1])}</td><td><span class=\"chip\">{label}</span></td><td>{esc(r[3])}</td></tr>")
for r in md_table(report, "| # | Tension | Evidence"):
    tensions.append(f"<tr><td>{r[0]}</td><td>{esc(r[1])}</td><td><span class=\"chip new\">New</span></td><td>{esc(r[2])}</td></tr>")

open_rows = md_table(questions, "| # | Question | Why it matters")
order = sorted(open_rows, key=lambda r: int(re.sub(r"\D", "", r[0])))
qs = [f"<li><b>{esc(r[1])}</b><span class=\"default\">Default until you answer: {esc(r[3])}</span></li>" for r in order]

images = {}
web = os.path.join(BOARDS, "gate-0-images", "web")
for f in os.listdir(web):
    key, ext = os.path.splitext(f)
    mime = "image/png" if ext == ".png" else "image/jpeg"
    images[key] = f"data:{mime};base64," + base64.b64encode(open(os.path.join(web, f), "rb").read()).decode()

page = open(os.path.join(BOARDS, "gate-0-board.template.html"), encoding="utf-8").read()
page = page.replace("{{rubric_rows}}", "\n".join(rubric)).replace("{{tension_rows}}", "\n".join(tensions)).replace("{{question_rows}}", "\n".join(qs))
for key, uri in images.items():
    page = page.replace("{{" + key + "}}", uri)
left = re.findall(r"\{\{[a-z_]+\}\}", page)
if left:
    raise SystemExit(f"unfilled placeholders: {left}")
out = os.path.join(BOARDS, "20261020_Gate-0-Review-Board.html")
open(out, "w", encoding="utf-8").write(page)
print(f"{out}: {len(page)//1024} KB, {len(rubric)} rubric rows, {len(tensions)} tensions, {len(qs)} questions, {len(images)} images")
