"""DR-10 tile overview sheets: one per shape, tile color and color mode (12).

    python3 -I tile_sheets.py

Each sheet shows all 122 tiles in catalogue order with their IDs, on the ground
opposite to the tile (Charcoal tiles on Newsprint, Newsprint tiles on
Charcoal), under the Edition 06 wordmark and a title in the contact sheets'
header layout. Text is Inter converted to outlines. The tile outline is drawn
once in <defs> and referenced, so each sheet stays small. Writes
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


def sheet_name(shape, tile, mode):
    md = {"two-color": "Two-Color", "one-color": "One-Color"}[mode]
    return f"{C.DATE}_Oath-And-Action-Civic-Line-Tiles-{SHAPE_FILE[shape]}-{tile.capitalize()}-{md}"


def tile_body(row, shape, tile, mode, prefix):
    """The tile's icon group, ids prefixed; the shape itself is referenced from <defs>."""
    bare = open(C.edition_file(row, C.TILE_EDITION[(tile, mode)]), encoding="utf-8").read()
    inner = T.bare_inner(bare).replace('id="', f'id="{prefix}').replace("url(#", f"url(#{prefix}")
    f = C.TILE_FACTORS[shape]
    t = 64 * (1 - f)
    return f'<use href="#tile-shape"/><g transform="matrix({f:g} 0 0 {f:g} {t:.4f} {t:.4f})">{inner}</g>'


def main():
    os.makedirs(OUT, exist_ok=True)
    inv = C.load_inventory()["icons"]
    fonts = CS.Fonts()
    meas = CS.measure_sheet("01")
    rows_n = (len(inv) + COLS - 1) // COLS
    H = TOP + rows_n * PITCH_Y + 56
    lines = []
    specs = [(sh, tl, md) for sh in C.TILE_SHAPES for tl in C.TILE_COLOURS for md in C.TILE_MODES]
    for sh, tl, md in specs:
        lines.append({"id": f"t-{sh}-{tl}-{md}", "size": 100, "runs": [
            {"family": "Inter-600", "text": "Tiles"},
            {"family": "Inter-400", "text": f" / {SHAPE_TITLE[sh]} / {tl.capitalize()}, {md}"}]})
        lines.append({"id": f"f-{sh}-{tl}-{md}", "size": 100, "runs": [
            {"family": "Inter-400", "text": f"Oath & Action / Civic Line / Tiles / {SHAPE_FILE[sh]} / {tl.capitalize()} / {md.replace('-', ' ').title().replace(' ', '-')}"}]})
    for r in inv:
        lines.append({"id": f"id-{r['id']}", "size": 100, "runs": [{"family": "Inter-400", "text": r["id"]}]})
    shaped = CS.shape(lines)
    jobs, written = [], []
    for sh, tl, md in specs:
        ground = C.NEWSPRINT if tl == "charcoal" else C.CHARCOAL
        ink = C.CHARCOAL if tl == "charcoal" else C.NEWSPRINT
        accent = C.PILLAR_RED if md == "two-color" else ink
        fill = C.TILE_FILL[tl]
        shape_el = T.shape_element(sh, fill).replace(' id="tile"', ' id="tile-shape"')
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" id="oa-civic-line-tiles-{sh}-{tl}-{md}">',
                 f"  <title>Oath &amp; Action Civic Line tiles: {SHAPE_TITLE[sh].lower()}, {tl.capitalize()}, {md}</title>",
                 "  <desc>All 122 Civic Line tiles in catalogue order. Each tile is its tile file's geometry; text is Inter converted to outlines.</desc>",
                 f"  <defs>{shape_el}</defs>",
                 f'  <rect id="ground" x="0" y="0" width="{W}" height="{H}" fill="{ground}"/>']
        wm, _, _ = CS.wordmark_group(meas["wordmark"], accent, ink)
        parts.append(wm)
        parts.append(f'  <rect id="rule" x="{meas["rule"]["x0"]}" y="{CS.n2(meas["rule"]["cy"] - CS.RULE_T / 2)}" '
                     f'width="{meas["rule"]["x1"] - meas["rule"]["x0"]}" height="{CS.n2(CS.RULE_T)}" fill="{ink}"/>')
        tid = f"t-{sh}-{tl}-{md}"
        size = 20.6
        a, b = CS.ink_extent(fonts, shaped[tid]["chars"], size)
        parts.append(f'  <path id="title" fill="{ink}" d="{CS.text_path(fonts, shaped[tid]["chars"], size, meas["title"]["x1"] - b, meas["title"]["baseline"])}"/>')
        grid_w = COLS * PITCH_X
        x_left = (W - grid_w) / 2
        for k, r in enumerate(inv):
            cx = x_left + (k % COLS) * PITCH_X + PITCH_X / 2
            y = TOP + (k // COLS) * PITCH_Y
            parts.append(f'  <svg x="{cx - TILE / 2:.2f}" y="{y}" width="{TILE}" height="{TILE}" viewBox="0 0 128 128">'
                         f'{tile_body(r, sh, tl, md, f"{r["id"].lower()}-")}</svg>')
            ch = shaped[f"id-{r['id']}"]["chars"]
            a, b = CS.ink_extent(fonts, ch, 11.5)
            parts.append(f'  <path fill="{ink}" d="{CS.text_path(fonts, ch, 11.5, cx - (a + b) / 2, y + TILE + 19)}"/>')
        fid = f"f-{sh}-{tl}-{md}"
        a, b = CS.ink_extent(fonts, shaped[fid]["chars"], 12.6)
        parts.append(f'  <path id="footer" fill="{ink}" d="{CS.text_path(fonts, shaped[fid]["chars"], 12.6, meas["footer"]["x1"] - b, H - 28)}"/>')
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
