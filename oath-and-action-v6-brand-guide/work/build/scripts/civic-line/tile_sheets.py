"""DR-10 tile overview sheets: one per shape, tile color and color mode (12).

    python3 -I tile_sheets.py

Each sheet shows all 122 tiles in catalog order with their IDs, on the ground
opposite to the tile (Charcoal tiles on Newsprint, Newsprint tiles on
Charcoal), under the Edition 06 wordmark and a title in the sheet template the
contact sheets share (variant review S-3); the footer repeats the title's
words. Each tile is its tile file's icon group, transform included, so the
optical scale and offset show (S-1, S-2). Text is Inter converted to outlines.
The tile outline is drawn once in <defs> and referenced, so each sheet stays
small. Every id starts with the sheet's root id (M-2). Writes
contact-sheets/tiles/<date>_Oath-And-Action-Civic-Line-Tiles-<Shape>-<Tile>-<Mode>.svg,
.png and -2x.png.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contact_sheets as CS  # noqa: E402  (fonts, shaping, outlines, wordmark)
import cl_common as C  # noqa: E402
import cl_tiles as T  # noqa: E402

OUT = os.path.join(C.ASSETS, "contact-sheets", "tiles")
SHAPE_TITLE = {"square": "Square", "rounded": "Rounded square", "circle": "Circle"}
SHAPE_FILE = {"square": "Square", "rounded": "Rounded", "circle": "Circle"}
W, COLS, TILE, PITCH_X, PITCH_Y, TOP = 1536, 12, 88, 120, 132, 104
FOOTER_TOP = 1574.4   # the tile sheets' footer top, kept (S-3)


def sheet_name(shape, tile, mode):
    md = {"two-color": "Two-Color", "one-color": "One-Color"}[mode]
    return f"{C.DATE}_Oath-And-Action-Civic-Line-Tiles-{SHAPE_FILE[shape]}-{tile.capitalize()}-{md}"


def tile_body(row, shape, tile, mode, sheet_root):
    """The tile file's icon group, with its ids moved under <sheet root>-<icon id>;
    the shape itself is referenced from <defs>."""
    t = open(C.tile_file(row, shape, tile, mode), encoding="utf-8").read()
    start = re.search(r'<g id="[^"]+-icon" data-part="icon"', t).start()
    g = t[start:t.rindex("</g>") + 4]
    g = g.replace(C.tile_root(row["id"], shape, tile, mode), f"{sheet_root}-{row['id'].lower()}")
    return f'<use href="#{sheet_root}-tile-shape"/>{g}'


def main():
    os.makedirs(OUT, exist_ok=True)
    inv = C.load_inventory()["icons"]
    fonts = CS.Fonts()
    rows_n = (len(inv) + COLS - 1) // COLS
    H = TOP + rows_n * PITCH_Y + 56
    lines = []
    specs = [(sh, tl, md) for sh in C.TILE_SHAPES for tl in C.TILE_COLOURS for md in C.TILE_MODES]
    for sh, tl, md in specs:
        lines.append({"id": f"t-{sh}-{tl}-{md}", "size": 100, "runs": [
            {"family": "Inter-600", "text": "Tiles"},
            {"family": "Inter-400", "text": f" / {SHAPE_TITLE[sh]} / {tl.capitalize()}, {md}"}]})
        lines.append({"id": f"f-{sh}-{tl}-{md}", "size": 100, "runs": [
            {"family": "Inter-400", "text": f"Oath & Action / Civic Line / Tiles / {SHAPE_TITLE[sh]} / {tl.capitalize()}, {md}"}]})
    for r in inv:
        lines.append({"id": f"id-{r['id']}", "size": 100, "runs": [{"family": "Inter-400", "text": r["id"]}]})
    shaped = CS.shape(lines)
    jobs, written = [], []
    for sh, tl, md in specs:
        ground = C.NEWSPRINT if tl == "charcoal" else C.CHARCOAL
        ink = C.CHARCOAL if tl == "charcoal" else C.NEWSPRINT
        accent = C.PILLAR_RED if md == "two-color" else ink
        fill = C.TILE_FILL[tl]
        rid = f"oa-civic-line-tiles-{sh}-{tl}-{md}"
        shape_el = T.shape_element(sh, fill, rid).replace(f'id="{rid}-tile" data-part="tile"', f'id="{rid}-tile-shape"')
        TP = CS.TEMPLATE
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" id="{rid}">',
                 f"  <title>Oath &amp; Action Civic Line tiles: {SHAPE_TITLE[sh].lower()}, {tl.capitalize()}, {md}</title>",
                 "  <desc>All 122 Civic Line tiles in catalog order. Each tile is its tile file's geometry, transform included; "
                 "text is Inter converted to outlines. Every id starts with the sheet's root id.</desc>",
                 f"  <defs>{shape_el}</defs>",
                 f'  <rect id="{rid}-ground" x="0" y="0" width="{W}" height="{H}" fill="{ground}"/>']
        wm, _, _ = CS.wordmark_group(TP["wordmark"], accent, ink, f"{rid}-wordmark")
        parts.append(wm)
        ru = TP["rule"]
        parts.append(f'  <rect id="{rid}-rule" x="{ru["x0"]}" y="{CS.n2(ru["cy"] - CS.RULE_T / 2)}" '
                     f'width="{ru["x1"] - ru["x0"]}" height="{CS.n2(CS.RULE_T)}" fill="{ink}"/>')
        tid = f"t-{sh}-{tl}-{md}"
        size = TP["title"]["size"]
        a, b = CS.ink_extent(fonts, shaped[tid]["chars"], size)
        parts.append(f'  <path id="{rid}-title" fill="{ink}" d="{CS.text_path(fonts, shaped[tid]["chars"], size, TP["title"]["x1"] - b, TP["title"]["baseline"])}"/>')
        grid_w = COLS * PITCH_X
        x_left = (W - grid_w) / 2
        for k, r in enumerate(inv):
            cx = x_left + (k % COLS) * PITCH_X + PITCH_X / 2
            y = TOP + (k // COLS) * PITCH_Y
            parts.append(f'  <svg x="{cx - TILE / 2:.2f}" y="{y}" width="{TILE}" height="{TILE}" viewBox="0 0 128 128">'
                         f'{tile_body(r, sh, tl, md, rid)}</svg>')
            ch = shaped[f"id-{r['id']}"]["chars"]
            a, b = CS.ink_extent(fonts, ch, 11.5)
            parts.append(f'  <path fill="{ink}" d="{CS.text_path(fonts, ch, 11.5, cx - (a + b) / 2, y + TILE + 19)}"/>')
        fid = f"f-{sh}-{tl}-{md}"
        fs = TP["footer"]["size"]
        a, b = CS.ink_extent(fonts, shaped[fid]["chars"], fs)
        f_base = CS.baseline_for_top(fonts, shaped[fid]["chars"], fs, FOOTER_TOP)
        parts.append(f'  <path id="{rid}-footer" fill="{ink}" d="{CS.text_path(fonts, shaped[fid]["chars"], fs, TP["footer"]["x1"] - b, f_base)}"/>')
        parts.append("</svg>")
        svg = "\n".join(parts) + "\n"
        name = sheet_name(sh, tl, md)
        with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        jobs.append({"svg": svg, "w": W, "h": H, "bg": None, "out": os.path.join(OUT, name + ".png")})
        jobs.append({"svg": svg.replace(f'width="{W}" height="{H}"', f'width="{W * 2}" height="{H * 2}"', 1), "w": W * 2, "h": H * 2,
                     "bg": None, "out": os.path.join(OUT, name + "-2x.png")})
        written.append(name)
    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "jobs.json")
        json.dump(jobs, open(jp, "w"))
        rr = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
        if rr.returncode:
            raise SystemExit(rr.stderr[-2000:])
    for j in jobs:
        Image.open(j["out"]).convert("RGB").save(j["out"], optimize=True)
    print(f"wrote {len(written)} tile sheets ({W} x {H}) in {os.path.relpath(OUT, C.ROOT)}")


if __name__ == "__main__":
    main()
