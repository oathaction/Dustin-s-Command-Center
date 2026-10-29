"""Calibration board for the tile icon factors (DR-10).

    python3 -I tile_calibration.py

Twenty varied icons (wide, tall, compact, dense, the four pillar marks and
R-35) on each shape. For every shape the board shows three candidate factors
at 96 px on Charcoal two-color tiles, then the chosen factor (C.TILE_FACTORS)
at 48, 96 and 192 px on both tile colours. Each row is labelled with the
smallest ink-to-edge margin over the twenty and over all 122 icons. Writes
qa/<date>_Civic-Line-Tile-Calibration.png and a JSON of the margins.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import cl_tiles as T  # noqa: E402

BOARD = ["R-44", "R-49", "R-46", "R-42", "R-40", "CL-014", "R-03", "CL-001", "CL-019", "CL-020",
         "CL-021", "CL-022", "R-35", "CL-071", "CL-012", "CL-069", "CL-038", "CL-057", "R-02", "R-18"]
CANDIDATES = {"square": [0.66, 0.68, 0.70], "rounded": [0.64, 0.66, 0.68], "circle": [0.60, 0.62, 0.64]}
OUT = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Tile-Calibration.png")
OUT_JSON = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Tile-Calibration.json")
SHAPE_LABEL = {"square": "Square", "rounded": "Rounded square (superellipse, exponent 5)", "circle": "Circle"}


def tile_inner(row, shape, tile, mode, f, prefix):
    bare = open(C.edition_file(row, C.TILE_EDITION[(tile, mode)]), encoding="utf-8").read()
    svg = T.tile_svg(bare, row["id"], row["label"], shape, tile, mode, f).split("?>", 1)[-1]
    inner = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    inner = inner.replace('id="', f'id="{prefix}').replace("url(#", f"url(#{prefix}")
    return inner


def margins(rows, shape, f):
    out = {}
    for r in rows:
        bare = open(C.edition_file(r, "red-black"), encoding="utf-8").read()
        out[r["id"]] = T.icon_margin(bare, shape, f)
    return out


def main():
    inv = C.inventory_by_id()
    allrows = list(inv.values())
    pad, gap, top = 40, 16, 96
    width = pad * 2 + len(BOARD) * (96 + gap)
    parts, y = [], top
    report = {"board_icons": BOARD, "candidates": CANDIDATES, "chosen": C.TILE_FACTORS, "rows": []}
    k = 0

    def text(x, yy, s, size=14, weight=400, fill=C.CHARCOAL, anchor="start"):
        return f'<text x="{x}" y="{yy}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'

    # Cross-shape check: the three shapes side by side per icon at the chosen factors
    parts.append(text(pad, y + 26, "The three shapes together at the chosen factors, 96 px", 22, 700))
    y += 44
    for tile in ("charcoal", "newsprint"):
        parts.append(text(pad, y + 16, f"{tile.capitalize()} tiles, two-color: square {C.TILE_FACTORS['square']:.2f}, "
                          f"rounded {C.TILE_FACTORS['rounded']:.2f}, circle {C.TILE_FACTORS['circle']:.2f}", 14, 600))
        y += 26
        per_row = 7
        group = 3 * 96 + 2 * 8 + 28
        for n, i in enumerate(BOARD):
            gx = pad + (n % per_row) * group
            yy = y + (n // per_row) * (96 + 34)
            for j, shape in enumerate(C.TILE_SHAPES):
                inner = tile_inner(inv[i], shape, tile, "two-color", C.TILE_FACTORS[shape], f"x{k}-")
                k += 1
                parts.append(f'<svg x="{gx + j * 104}" y="{yy}" width="96" height="96" viewBox="0 0 128 128">{inner}</svg>')
            parts.append(text(gx + 152, yy + 112, i, 11, 400, anchor="middle"))
        y += ((len(BOARD) + per_row - 1) // per_row) * (96 + 34) + 16
    y += 24
    for shape in C.TILE_SHAPES:
        parts.append(text(pad, y + 26, SHAPE_LABEL[shape], 22, 700))
        y += 44
        rows_spec = [(f, 96, "charcoal", "two-color") for f in CANDIDATES[shape]]
        chosen = C.TILE_FACTORS[shape]
        rows_spec += [(chosen, 48, "charcoal", "two-color"), (chosen, 48, "newsprint", "two-color"),
                      (chosen, 96, "newsprint", "two-color"), (chosen, 192, "charcoal", "two-color"),
                      (chosen, 192, "newsprint", "two-color")]
        for f, px, tile, mode in rows_spec:
            m_all = margins(allrows, shape, f)
            m_board = {i: m_all[i] for i in BOARD}
            worst = min(m_all, key=m_all.get)
            tag = "chosen" if abs(f - chosen) < 1e-9 else "candidate"
            report["rows"].append({"shape": shape, "factor": f, "px": px, "tile": tile, "status": tag,
                                   "min_margin_board": round(min(m_board.values()), 2),
                                   "min_margin_all": round(m_all[worst], 2), "min_margin_id": worst})
            label = (f"factor {f:.2f} ({tag}), {px} px, {tile.capitalize()} tile, two-color. "
                     f"Smallest margin {m_all[worst]:.1f} of 128 units ({worst}); stroke in tile {2.6807 * f:.2f} to {3.3508 * f:.2f}")
            parts.append(text(pad, y + 16, label, 14, 600 if tag == "chosen" else 400))
            y += 26
            per_row = len(BOARD) if px <= 96 else 10
            cell = px + (gap if px > 48 else 32)
            for n, i in enumerate(BOARD):
                x = pad + (n % per_row) * (max(cell, 96 + gap) if px <= 96 else cell)
                yy = y + (n // per_row) * (px + 34)
                inner = tile_inner(inv[i], shape, tile, mode, f, f"b{k}-")
                k += 1
                parts.append(f'<svg x="{x}" y="{yy}" width="{px}" height="{px}" viewBox="0 0 128 128">{inner}</svg>')
                parts.append(text(x + px / 2, yy + px + 16, i, 11, 400, anchor="middle"))
            y += ((len(BOARD) + per_row - 1) // per_row) * (px + 34) + 10
        y += 24
    height = y + 30
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="Inter, sans-serif">',
            f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>',
            text(pad, 40, "Civic Line tile calibration: one icon factor per shape (DR-10)", 26, 700),
            text(pad, 66, "Twenty varied icons. The factor scales each icon's option-3 box about the tile centre, so line weights keep the set's 25 percent spread. "
                 "Margins are the least clearance between ink and the tile edge.", 14)]
    svg = "\n".join(head + parts + ["</svg>"])
    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "j.json")
        json.dump([{"svg": svg, "w": width, "h": height, "bg": None, "out": OUT}], open(jp, "w"))
        r = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stderr[-2000:])
    Image.open(OUT).convert("RGB").save(OUT, optimize=True)
    C.write_json(OUT_JSON, report)
    print(f"wrote {os.path.relpath(OUT, C.ROOT)} ({width} x {height})")
    for row in report["rows"]:
        if row["px"] == 96 and row["tile"] == "charcoal":
            print(f"  {row['shape']:8s} {row['factor']:.2f} {row['status']:9s} min margin {row['min_margin_all']:.2f} ({row['min_margin_id']})")


if __name__ == "__main__":
    main()
