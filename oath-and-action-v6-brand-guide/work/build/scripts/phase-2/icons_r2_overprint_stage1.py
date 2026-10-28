"""Concept 1, Overprint, stage 1: the ten display masters and the 2x review sheet (design director,
round two, October 28, 2026).

Run: python3 -I icons_r2_overprint_stage1.py
Writes, in work/boards/phase-2/icons-r2/overprint/:
  20261028_Overprint-<Icon>-Display.svg   the ten display masters (paths `ink` and `accent`)
  20261028_Overprint-Stage-1-Sheet.png    the ten at 192 px on Newsprint: as drawn, red turned to
                                          ink, red removed, with each icon's reason for its red
The sheet's HTML source goes to the scratchpad. Nothing here is hinted or measured; stage 1 is
judged by eye.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_overprint_draw as O  # noqa: E402

ROOT = HERE.parents[3]
DATE = "20261028"
OUT = ROOT / "work/boards/phase-2/icons-r2/overprint"
FONTS = ROOT / "work/extract/v5-polished/fonts"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/overprint")
SHOT = HERE / "icons_r2_overprint_shot.js"
PX = 192
GAP = 40


def master_path(name):
    return OUT / f"{DATE}_Overprint-{O.FILE_NAME[name]}-Display.svg"


def write_masters():
    OUT.mkdir(parents=True, exist_ok=True)
    for n in O.ICONS:
        lay = O.display(n)
        title = (f"{O.LABELS[n]}, Concept 1 Overprint, display master for 48 px and up. "
                 f"Oath &amp; Action icon concept, October 28, 2026. Proposal only.")
        master_path(n).write_text(O.svg(lay, 24, title=title) + "\n")


def font_css():
    faces = [("Inter Tight", 800, "Inter-Tight-800-normal.ttf"), ("Inter Tight", 600, "Inter-Tight-600-normal.ttf"),
             ("Inter", 400, "Inter-400-normal.ttf"), ("Inter", 600, "Inter-600-normal.ttf"), ("Inter", 700, "Inter-700-normal.ttf")]
    return "".join(f"@font-face{{font-family:'{f}';font-weight:{w};src:url('file://{FONTS / fn}')}}" for f, w, fn in faces)


def row(mode):
    cells = []
    for n in O.ICONS:
        lay = O.display(n)
        acc = {"red": O.RED, "ink": O.CHAR, "none": None}[mode]
        art = O.svg(lay, PX, accent=acc)
        cap = ""
        if mode == "red":
            cap = (f'<div class="name">{O.LABELS[n]}<span class="cls">{O.CLASS[n]}</span></div>'
                   f'<div class="why">{O.REASON[n]}</div>')
        cells.append(f'<div class="cell">{art}{cap}</div>')
    return "".join(cells)


def strip(px):
    return "".join(f'<div class="mini" style="width:{PX}px">{O.svg(O.display(n), px)}</div>' for n in O.ICONS)


def sheet_html():
    width = 10 * PX + 9 * GAP
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Overprint stage 1 sheet</title>
<style>{font_css()}
body{{margin:0;background:#DCD9D2;color:#121212;font:400 16px/1.5 'Inter',sans-serif}}
.page{{width:{width}px;padding:56px 64px 48px}}
.eyebrow{{font:700 13px/1.4 'Inter';letter-spacing:.08em;text-transform:uppercase;color:#45494F;margin:0}}
h1{{font:800 44px/1.05 'Inter Tight';letter-spacing:-.02em;margin:10px 0 12px}}
.lede{{max-width:1180px;margin:0 0 6px;font-size:18px}}
.spec{{max-width:1400px;margin:0;color:#45494F;font-size:15px}}
h2{{font:600 17px/1.3 'Inter Tight';letter-spacing:-.01em;margin:40px 0 14px;padding-top:14px;border-top:1px solid #5D636D}}
h2 span{{font:400 15px 'Inter';color:#45494F;margin-left:10px}}
.row{{display:flex;gap:{GAP}px;align-items:flex-start}}
.cell{{width:{PX}px}}
.cell svg{{display:block}}
.name{{font:600 16px/1.3 'Inter';margin-top:10px}}
.cls{{display:block;font:400 13px/1.4 'Inter';color:#45494F}}
.why{{font:400 14px/1.45 'Inter';margin-top:6px}}
.mini{{display:flex;justify-content:flex-start}}
.mini svg{{display:block}}
.foot{{margin-top:28px;color:#45494F;font-size:14px;max-width:1500px}}
</style></head><body><div class="page">
<p class="eyebrow">Oath &amp; Action icons, round two · Concept 1 · Stage 1 review · October 28, 2026 · Design director</p>
<h1>Overprint: the ten display masters</h1>
<p class="lede">A fine Charcoal line printed over one solid plane of Pillar Red, set off register toward the lower left, the way a second ink lands on a newspaper page. The red sits under the part of the subject the story is about. Drawn by hand on the shared 24-unit grid and judged by eye at 2x. Nothing here is hinted or measured yet.</p>
<p class="spec">Line 1.5 units with round caps and round joins; rectangles take a 2-unit outer radius. Pillar-mark node: a solid ink disc 3 units across. Red plane: one disc, rounded square or stadium, filling its shape to the line's center, then printed 1.5 units left and 1.5 units down, the same in every icon. Shown at 192 px, twice the 96 px display size.</p>
<h2>Pillar Red as drawn<span>On Newsprint, 192 px, with each icon's reason for its red</span></h2>
<div class="row">{row("red")}</div>
<h2>Red turned to ink<span>Test 2, first half: the plane prints in Charcoal</span></h2>
<div class="row">{row("ink")}</div>
<h2>Red removed<span>Test 2, second half: the line drawing alone, the idle state in a row</span></h2>
<div class="row">{row("none")}</div>
<h2>The same masters at 96 and 48 px<span>Display master scaled; the hinted 16 and 24 px masters come in stage 2</span></h2>
<div class="row">{strip(96)}</div>
<div class="row" style="margin-top:16px">{strip(48)}</div>
<p class="foot">Proposal only. The pillar marks keep Direction A's skeletons (G1-01, Y1, Y2); Act keeps the frame over the opening only, with no lintel. Files: {OUT.relative_to(ROOT)}/{DATE}_Overprint-*-Display.svg.</p>
</div></body></html>"""


def main():
    write_masters()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    html = SCRATCH / f"{DATE}_Overprint-Stage-1-Sheet.html"
    html.write_text(sheet_html())
    png = OUT / f"{DATE}_Overprint-Stage-1-Sheet.png"
    width = 10 * PX + 9 * GAP + 128
    subprocess.run(["node", str(SHOT), str(html), str(png), str(width), "1"], check=True)
    print("wrote", png)


if __name__ == "__main__":
    main()
