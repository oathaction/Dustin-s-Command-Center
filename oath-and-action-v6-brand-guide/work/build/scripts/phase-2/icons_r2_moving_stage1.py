"""Stage 1 of Concept 2, Moving part: write the ten display masters and the 2x review sheet.

Run: python3 -I icons_r2_moving_stage1.py
Writes, in work/boards/phase-2/icons-r2/moving-part/:
  20261028_Moving-Part-<Icon>-Display.svg     ten display masters, paths "ink" and "accent"
  20261028_Moving-Part-Stage-1-Sheet.png      the review sheet: each icon at 192 px (2x of 96) on
                                              Newsprint, with the red turned to ink, and with the
                                              red removed, each with the reason for its red
The sheet's HTML source goes to the scratchpad. Chromium renders it at device scale 1.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_moving_draw as D  # noqa: E402

ROOT = HERE.parents[3]
DATE = "20261028"
OUT = ROOT / "work/boards/phase-2/icons-r2/moving-part"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/r2-moving-part")
FONTS = ROOT / "work/extract/v5-polished/fonts"
NEWS, CHAR, RED = "#DCD9D2", "#121212", "#E63946"


def joined(pcs, role):
    return "".join(d for r, d in pcs if r == role)


def master_svg(name):
    pcs = D.pieces(name)
    title = (f"{D.LABELS[name]}, Concept 2 Moving part, display master. Oath &amp; Action icon concept, "
             f"October 28, 2026. Proposal only.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><title>{title}</title>'
            f'<path id="ink" d="{joined(pcs, "ink")}" fill="{CHAR}"/>'
            f'<path id="accent" d="{joined(pcs, "accent")}" fill="{RED}"/></svg>')


def inline(name, px, mode, step=0.0):
    pcs = D.pieces(name, step)
    ink = joined(pcs, "ink")
    acc = joined(pcs, "accent")
    parts = [f'<svg width="{px}" height="{px}" viewBox="0 0 24 24">', f'<path d="{ink}" fill="{CHAR}"/>']
    if mode == "color":
        parts.append(f'<path d="{acc}" fill="{RED}"/>')
    elif mode == "ink":
        parts.append(f'<path d="{acc}" fill="{CHAR}"/>')
    parts.append("</svg>")
    return "".join(parts)


def sheet_html(px=192):
    css = f"""
    @font-face{{font-family:Inter;src:url('file://{FONTS}/Inter-400-normal.ttf');font-weight:400}}
    @font-face{{font-family:Inter;src:url('file://{FONTS}/Inter-600-normal.ttf');font-weight:600}}
    @font-face{{font-family:Inter;src:url('file://{FONTS}/Inter-700-normal.ttf');font-weight:700}}
    @font-face{{font-family:'Inter Tight';src:url('file://{FONTS}/Inter-Tight-800-normal.ttf');font-weight:800}}
    html,body{{margin:0;background:{NEWS};color:{CHAR};font-family:Inter,sans-serif}}
    .wrap{{padding:48px 56px 56px}}
    h1{{font:800 34px/1.1 'Inter Tight',sans-serif;margin:0 0 8px;letter-spacing:-0.01em}}
    .sub{{font-size:17px;line-height:1.45;margin:0 0 36px;max-width:1400px}}
    .grid{{display:grid;grid-template-columns:150px repeat(10,{px}px);column-gap:28px;row-gap:18px;align-items:center}}
    .rl{{font-size:14px;font-weight:600;line-height:1.35}}
    .rl span{{display:block;font-weight:400}}
    .cell svg{{display:block}}
    .name{{font-size:16px;font-weight:700;margin-top:6px}}
    .cls{{font-size:13px;color:#4a4a4a}}
    .why{{font-size:14px;line-height:1.4;margin-top:4px}}
    .rule{{grid-column:1 / -1;border-top:1px solid #12121233;height:0}}
    """
    rows = [("color", "As drawn", "Charcoal and Pillar Red"), ("ink", "Red turned to ink", "One color"),
            ("none", "Red removed", "The test of the structure")]
    cells = []
    for mode, label, sub in rows:
        cells.append(f'<div class="rl">{label}<span>{sub}</span></div>')
        for n in D.ICONS:
            cells.append(f'<div class="cell">{inline(n, px, mode)}</div>')
    cells.append('<div class="rule"></div>')
    cells.append('<div class="rl">Reason for the red</div>')
    for n in D.ICONS:
        cells.append(f'<div style="align-self:start"><div class="name">{D.LABELS[n]}</div><div class="cls">{D.CLASS[n]}</div>'
                     f'<div class="why">{D.REASON[n]}</div></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="wrap">
    <h1>Concept 2, Moving part. Stage 1 display masters</h1>
    <p class="sub">Each subject is built from a few solid pieces held apart by one 1.5-unit cut. The red piece is the one that
    moves. Display masters on the 24-unit grid, shown at 192 px, twice their 96 px size, on Newsprint. Drawn by hand and
    judged by eye; nothing here is hinted or measured yet. Proposal for the creative director's review, October 28, 2026.</p>
    <div class="grid">{''.join(cells)}</div></div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for n in D.ICONS:
        (OUT / f"{DATE}_Moving-Part-{D.FILE_NAME[n]}-Display.svg").write_text(master_svg(n))
    html = SCRATCH / "stage1-sheet.html"
    html.write_text(sheet_html())
    png = OUT / f"{DATE}_Moving-Part-Stage-1-Sheet.png"
    subprocess.run(["node", str(HERE / "icons_r2_moving_shot.js"), str(html), str(png), "2400", "1"], check=True)
    print("wrote", png)


if __name__ == "__main__":
    main()
