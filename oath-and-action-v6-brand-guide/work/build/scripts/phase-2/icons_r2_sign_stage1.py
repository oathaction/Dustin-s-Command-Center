"""Concept 3, Public sign, stage 1: the ten display masters and the 2x review sheet.

Run: python3 -I icons_r2_sign_stage1.py
Writes, in work/boards/phase-2/icons-r2/public-sign/:
  20261028_Public-Sign-<Name>-Display.svg   ten display masters, paths "ink" (Charcoal) and "accent" (Pillar Red)
  20261028_Public-Sign-Stage-1-Sheet.png    the review sheet, Chromium at device scale 2
The sheet's HTML is written to the scratchpad and rendered with icons_r2_sign_shot.js.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_sign_draw as D  # noqa: E402
from icons_r2_sign_geom import d_of  # noqa: E402

ROOT = HERE.parents[3]
DATE = "20261028"
OUT = ROOT / "work/boards/phase-2/icons-r2/public-sign"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/sign-build")
SHOT = HERE / "icons_r2_sign_shot.js"
NEWS, CHAR, RED, STONE = "#DCD9D2", "#121212", "#E63946", "#5D636D"


def master_svg(name):
    lay = D.display(name)
    title = f"{D.LABELS[name]}, Concept 3 Public sign, display master. Oath &amp; Action icon concept, October 28, 2026. Proposal only."
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><title>{title}</title>'
            f'<path id="ink" d="{d_of(lay["ink"])}" fill="{CHAR}"/>'
            f'<path id="accent" d="{d_of(lay["accent"])}" fill="{RED}"/></svg>')


def inline(name, px, mode="red", ink=CHAR, grid=False):
    lay = D.display(name)
    parts = [f'<svg class="ic" width="{px}" height="{px}" viewBox="0 0 24 24" role="img" aria-label="{D.LABELS[name]}">']
    if grid:
        lines = "".join(f'<path d="M{i} 0V24M0 {i}H24"/>' for i in range(1, 24))
        parts.append(f'<g stroke="#B8B3A9" stroke-width="0.035" fill="none">{lines}</g>')
        parts.append('<g fill="none" stroke="#7E9CC0" stroke-width="0.06"><rect x="2" y="2" width="20" height="20"/>'
                     '<rect x="3" y="3" width="18" height="18"/><circle cx="12" cy="12" r="10"/>'
                     '<rect x="4" y="2" width="16" height="20"/><rect x="2" y="4" width="20" height="16"/>'
                     '<path d="M0 12H24M12 0V24" stroke-width="0.05"/></g>')
    parts.append(f'<path d="{d_of(lay["ink"])}" fill="{ink}"/>')
    if mode == "red":
        parts.append(f'<path d="{d_of(lay["accent"])}" fill="{RED}"/>')
    elif mode == "ink":
        parts.append(f'<path d="{d_of(lay["accent"])}" fill="{ink}"/>')
    parts.append("</svg>")
    return "".join(parts)


DEPARTURES = [
    ("Explain", "The lifted quarter is drawn as its swing, the red arc, with no ink lid. With an ink corner piece outside the box, every draft read as the interface glyph for opening a link in a new window. This touches an approved skeleton, so it needs your call. Its red runs about 12 percent of the painted area, over the 10 percent spec: cut to 10, the arc shortens to a dash that sits where a notification badge would."),
    ("Ballot", "The red is the check on the paper. The brief named the paper's path; in four drafts a red stroke above the paper read as a head over a body. The check is the stroke a voter makes, and on the solid paper it measures 4.49:1. With the red removed the paper is blank, so the name then rests on the box and its slot."),
    ("Act", "The node is the latch, a station on the jamb at the center line, where the door meets its frame. A knocked-out node in a 45-degree leaf read as a luggage tag or a door hanger, and a free disc in the doorway read as a head. The full lintel from round one stays, pending its named approval."),
    ("Connect and Ballot", "These are the only places red touches ink. Everywhere else the red floats one gap off the drawing. The bridge has to land on both halves, and the check is made on the paper."),
    ("Track and Feedback loop", "Direction takes a solid arrowhead, the public-sign arrow. A chevron at bar width inside the 10 percent red budget closes into a blob."),
    ("Feedback loop", "Its nodes are two bars across, larger than the pillar node, because here the nodes are the subject. The loop turns clockwise like the hinge diagram's arcs."),
    ("Testify and Campaign money", "Any disc near head height reads as a head in a family with people. The witness speaks into a gooseneck microphone aimed at the face, and the hand tosses the coin up and away from the body."),
]


def page():
    css = f"""
    :root {{ --bg:{NEWS}; --fg:{CHAR}; --muted:#45494F; --rule:{STONE}; --red:{RED}; }}
    * {{ box-sizing:border-box }}
    body {{ margin:0; background:var(--bg); color:var(--fg); font:400 15px/1.5 Inter, "Helvetica Neue", Arial, sans-serif }}
    .sheet {{ width:1240px; margin:0 auto; padding:48px 40px 56px }}
    .eyebrow {{ font:700 12px/1.4 Inter, sans-serif; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin:0 }}
    h1 {{ font:800 44px/1.05 "Inter Tight", Inter, sans-serif; letter-spacing:-.02em; margin:8px 0 14px }}
    h2 {{ font:800 24px/1.15 "Inter Tight", Inter, sans-serif; letter-spacing:-.01em; margin:0 0 6px }}
    p {{ margin:0 0 10px; max-width:74ch }}
    .lede {{ font-size:18px; line-height:1.45; max-width:62ch }}
    .spec {{ color:var(--muted); font-size:14px }}
    section {{ border-top:1px solid var(--rule); margin-top:34px; padding-top:24px }}
    .row {{ display:grid; grid-template-columns:repeat(5, 192px); column-gap:40px; row-gap:28px; margin-top:18px }}
    .cell .ic {{ display:block }}
    .name {{ font-weight:700; margin-top:8px; font-size:15px }}
    .cls {{ font:600 11px/1.3 Inter, sans-serif; letter-spacing:.06em; text-transform:uppercase; color:var(--muted) }}
    .why {{ font-size:13.5px; line-height:1.4; margin-top:4px }}
    .why b {{ color:var(--fg) }}
    .dot {{ display:inline-block; width:9px; height:9px; border-radius:50%; background:var(--red); margin-right:6px; vertical-align:1px }}
    .small {{ display:flex; gap:22px; align-items:flex-end; flex-wrap:wrap; margin-top:14px }}
    .small .ic {{ display:block }}
    .dark {{ background:{CHAR}; padding:14px 18px; display:inline-flex; gap:22px; align-items:flex-end; margin-top:14px }}
    .dep {{ display:grid; grid-template-columns:220px 1fr; column-gap:24px; row-gap:10px; margin-top:12px; font-size:14px }}
    .dep dt {{ font-weight:700 }}
    .dep dd {{ margin:0; max-width:80ch }}
    .foot {{ color:var(--muted); font-size:13px; margin-top:30px }}
    """
    def band(mode, show_why):
        cells = []
        for n in D.ICONS:
            why = f'<div class="why"><span class="dot"></span>{D.VERB[n]}</div>' if show_why else ""
            cells.append(f'<div class="cell">{inline(n, 192, mode)}<div class="name">{D.LABELS[n]}</div><div class="cls">{D.CLASS[n]}</div>{why}</div>')
        return f'<div class="row">{"".join(cells)}</div>'
    grid_cells = "".join(f'<div>{inline(n, 96, "red", grid=True)}</div>' for n in D.ICONS)
    s48 = "".join(inline(n, 48) for n in D.ICONS)
    s24 = "".join(inline(n, 24) for n in D.ICONS)
    d48 = "".join(inline(n, 48, "red", ink=NEWS) for n in D.ICONS)
    deps = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in DEPARTURES)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Public Sign Stage 1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="sheet">
<p class="eyebrow">Oath &amp; Action icon concepts, round two &middot; Concept 3 &middot; Stage 1 review</p>
<h1>Public sign</h1>
<p class="lede">Oath &amp; Action's subjects drawn as public information symbols, with people and objects built from one bar on a 45 and 90 degree grid. In each icon the Charcoal drawing names the subject, and a single red stroke shows what happens to it.</p>
<p class="spec">Display masters drawn by hand on the shared 24-unit grid. Bar 3 units with round ends and round joins. Head and node 4.5 units across. One gap, 1.5 units, between every part and between the ink and the red. One red stroke or arrowhead at bar width. Shown at 192 px, eight times the 24 px master. The 16 and 24 px masters are hinted in stage 2, and the numbers are measured there.</p>
<section><h2>With red</h2><p>Each icon alone, as it appears when it stands by itself. The line under each icon is the reason for its red.</p>{band("red", True)}</section>
<section><h2>Red turned to ink</h2><p>The same drawings in one color, with the red stroke set in Charcoal.</p>{band("ink", False)}</section>
<section><h2>Red removed</h2><p>The idle state in a row: each icon drops its verb and reads as a sign in one color.</p>{band("none", False)}</section>
<section><h2>Construction</h2><p>The same ten at 96 px over the 24-unit grid, with the live area and the circle, square, portrait and landscape keylines.</p><div class="row" style="grid-template-columns:repeat(10, 96px); column-gap:22px">{grid_cells}</div></section>
<section><h2>The family at working sizes</h2><p>The display master scaled to 48 and 24 px, before hinting, on Newsprint and on Charcoal.</p><div class="small">{s48}</div><div class="small">{s24}</div><div class="dark">{d48}</div></section>
<section><h2>Where this sheet departs from the brief</h2><dl class="dep">{deps}</dl></section>
<p class="foot">Proposal only. Drawn October 28, 2026, by the design director for the creative director's stage 1 review. Every drawing is original and was drawn by hand on the grid; no public symbol set was traced.</p>
</div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for n in D.ICONS:
        (OUT / f"{DATE}_Public-Sign-{D.FILE_NAME[n]}-Display.svg").write_text(master_svg(n))
    html = SCRATCH / "stage1-sheet.html"
    html.write_text(page())
    png = OUT / f"{DATE}_Public-Sign-Stage-1-Sheet.png"
    subprocess.run(["node", str(SHOT), str(html), str(png), "1320", "2"], check=True)
    print("wrote", png)


if __name__ == "__main__":
    main()
