"""Calibration board for the tile icon factors (DR-10), with the optical
scale and offset from the variant review (S-1, S-2) and the tile minimums (M-1).

    python3 -I tile_calibration.py

Twenty varied icons (wide, tall, compact, dense, the four pillar marks and
R-35) on each shape. The board shows, in order: the three shapes side by side
at the chosen factors; every icon the optical scale or offset touches, before
and after, in the rounded Charcoal one-color tile; then for every shape three
candidate factors at 96 px on Charcoal two-color tiles, the chosen factor
(C.TILE_FACTORS) at 96 and 192 px on both tile colors, at the two-color
minimum size, and at 48 px, which sits below the tile minimum and is kept for
reference. Every tile carries its icon's optical scale, offset and stroke cap,
so a candidate row differs from the chosen one only by the shape factor. Each
row is labeled with the smallest ink-to-edge margin over the twenty and over
all 122 icons. Writes qa/<date>_Civic-Line-Tile-Calibration.png and a JSON
with the margins, the reason each factor won, every icon's tile scale per
shape, optics and minimum sizes, and a geometric check of the S-1 rule.
"""
import json
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
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


def area_fraction(shape):
    """Share of the 128 box that the tile shape fills."""
    if shape == "square":
        return 1.0
    if shape == "circle":
        return math.pi / 4
    n = 5.0   # |x|^5 + |y|^5 <= 1 inside [-1, 1]^2
    return math.gamma(1 + 1 / n) ** 2 / math.gamma(1 + 2 / n)


def tile_inner(row, shape, tile, mode, f, prefix, optics=None):
    bare = open(C.edition_file(row, C.TILE_EDITION[(tile, mode)]), encoding="utf-8").read()
    svg = T.tile_svg(bare, row, shape, tile, mode, factor=f, optics=optics).split("?>", 1)[-1]
    inner = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    inner = inner.replace('id="', f'id="{prefix}').replace("url(#", f"url(#{prefix}").replace('href="#', f'href="#{prefix}')
    return inner


def margins(rows, shape, f):
    out = {}
    for r in rows:
        bare = open(C.edition_file(r, "red-black"), encoding="utf-8").read()
        a, dx, k = C.tile_optics(r["id"], r["stroke_units"])
        out[r["id"]] = T.icon_margin(bare, shape, f, a, dx, k)
    return out


def spread(v):
    v = np.asarray(v, float)
    return {"min": round(float(v.min()), 1), "max": round(float(v.max()), 1), "max_over_min": round(float(v.max() / v.min()), 3),
            "p90_over_p10": round(float(np.percentile(v, 90) / np.percentile(v, 10)), 3)}


def main():
    inv = C.inventory_by_id()
    allrows = list(inv.values())
    pad, gap, top = 40, 16, 118
    width = pad * 2 + len(BOARD) * (96 + gap)
    parts, y = [], top
    k = 0

    def text(x, yy, s, size=14, weight=400, fill=C.CHARCOAL, anchor="start"):
        s = s.replace("&", "&amp;")
        return f'<text x="{x}" y="{yy}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'

    # per-icon record and the geometric check of the S-1 rule
    per_icon, hull = {}, {}
    for r in allrows:
        bare = open(C.edition_file(r, "red-black"), encoding="utf-8").read()
        hs, hx, hy = T.hull_size(bare)
        hull[r["id"]] = hs
        a, dx, kk = C.tile_optics(r["id"], r["stroke_units"])
        per_icon[r["id"]] = {"optical_scale": a, "offset_x_units": dx, "stroke_scale": round(kk, 6),
                             "tile_stroke_units": round(min(r["stroke_units"] * a, C.TILE_STROKE_CAP), 4),
                             "scale": {sh: round(f * a, 6) for sh, f in C.TILE_FACTORS.items()},
                             "min_px": C.tile_min_px(r["id"]), "hull_size_units": round(hs, 2),
                             "hull_centroid_offset_x_units": round(hx, 2)}
    med = float(np.median(list(hull.values())))
    rule_diff = []
    for i, hs in hull.items():
        if i in C.PILLAR_GROUP:
            continue
        a = round(min(1.10, max(0.94, (74.4 / hs) ** 0.5)), 2)
        a = a if abs(a - 1) >= 0.04 else 1.0
        if abs(a - C.TILE_OPTICAL_SCALE.get(i, 1.0)) > 1e-9:
            rule_diff.append({"id": i, "hull_size_units": round(hs, 2), "rule_on_this_hull": a, "review_table": C.TILE_OPTICAL_SCALE.get(i, 1.0)})
    after = [hull[i] * C.TILE_OPTICAL_SCALE.get(i, 1.0) for i in hull]
    report = {"board_icons": BOARD, "candidates": CANDIDATES, "chosen": C.TILE_FACTORS,
              "why_each_factor_won": {}, "optics_source": "work/handoffs/phase-2/20261029_Civic-Line-Variant-Review.md, S-1 and S-2 tables",
              "hull_size_spread": {"before_optical_scale": spread(list(hull.values())), "after_optical_scale": spread(after),
                                   "median_units": round(med, 2)},
              "s1_rule_check": {"note": "The S-1 rule recomputed on this script's hull of the vector outlines. The review measured "
                                        "hulls on 512 px tile renders, so icons that sit near a rounding step or the 0.04 threshold "
                                        "can land one step apart. The build uses the review's table as given.", "differences": rule_diff},
              "rows": [], "per_icon": per_icon}
    for sh, f in C.TILE_FACTORS.items():
        rel = f / math.sqrt(area_fraction(sh))
        report["why_each_factor_won"][sh] = {
            "factor": f, "tile_area_fraction": round(area_fraction(sh), 4), "icon_size_vs_equal_area_square": round(rel, 3),
            "reason": (f"At {f:g} the icon spans {rel:.3f} of the side of a square with the tile's area "
                       f"(the {sh} fills {area_fraction(sh):.3f} of its box), so the three shapes hold one icon size: "
                       "0.680 on the square, 0.677 on the rounded square, 0.700 on the circle, whose edge closes in at the corners. "
                       + ("In the design director's review, 0.60 and 0.58 read smaller than the square and rounded tiles beside it at 120 px. "
                          if sh == "circle" else "")
                       + "Every icon keeps the 12-unit safe margin at this factor.")}

    # 1. the three shapes together
    parts.append(text(pad, y + 26, "The three shapes together at the chosen factors, 96 px", 22, 700))
    y += 44
    for tile in ("charcoal", "newsprint"):
        parts.append(text(pad, y + 16, f"{tile.capitalize()} tiles, two-color: square {C.TILE_FACTORS['square']:.2f}, "
                          f"rounded {C.TILE_FACTORS['rounded']:.2f}, circle {C.TILE_FACTORS['circle']:.2f}, each times the icon's optical scale", 14, 600))
        y += 26
        per_row, inner = 7, 100
        group = (width - 2 * pad - (2 * inner + 96)) / (per_row - 1)   # seven triplets fill the board width
        for n, i in enumerate(BOARD):
            gx = pad + (n % per_row) * group
            yy = y + (n // per_row) * (96 + 34)
            for j, shape in enumerate(C.TILE_SHAPES):
                svg_in = tile_inner(inv[i], shape, tile, "two-color", C.TILE_FACTORS[shape], f"x{k}-")
                k += 1
                parts.append(f'<svg x="{gx + j * inner:.1f}" y="{yy}" width="96" height="96" viewBox="0 0 128 128">{svg_in}</svg>')
            parts.append(text(f"{gx + inner + 48:.1f}", yy + 112, i, 11, 400, anchor="middle"))
        y += ((len(BOARD) + per_row - 1) // per_row) * (96 + 34) + 16
    y += 24

    # 2. optical scale and offset, before and after
    touched = [i for i in inv if i in C.TILE_OPTICAL_SCALE or i in C.TILE_OFFSET_X]
    parts.append(text(pad, y + 26, f"Optical scale and offset (variant review S-1, S-2): the {len(touched)} icons they touch, before and after", 22, 700))
    y += 44
    parts.append(text(pad, y + 16, "Rounded square, Charcoal one-color, 96 px. Left of each pair: the shape factor alone. Right: the shipped tile, "
                      "with the optical scale a, the offset dx in box units and the stroke held at 3.35 units or less.", 14, 400))
    y += 26
    per_row, pair = 10, 2 * 96 + 8 + 24
    for n, i in enumerate(touched):
        gx = pad + (n % per_row) * pair
        yy = y + (n // per_row) * (96 + 34)
        for j, optics in enumerate(((1.0, 0.0, 1.0), None)):
            inner = tile_inner(inv[i], "rounded", "charcoal", "one-color", C.TILE_FACTORS["rounded"], f"o{k}-", optics)
            k += 1
            parts.append(f'<svg x="{gx + j * 104}" y="{yy}" width="96" height="96" viewBox="0 0 128 128">{inner}</svg>')
        a, dx = C.TILE_OPTICAL_SCALE.get(i, 1.0), C.TILE_OFFSET_X.get(i, 0.0)
        lab = f"{i}  a {a:.2f}" + (f", dx {dx:+.1f}" if dx else "")
        parts.append(text(gx + 100, yy + 112, lab, 11, 400, anchor="middle"))
    y += ((len(touched) + per_row - 1) // per_row) * (96 + 34) + 40

    # 3. factors per shape
    for shape in C.TILE_SHAPES:
        parts.append(text(pad, y + 26, SHAPE_LABEL[shape], 22, 700))
        y += 44
        chosen = C.TILE_FACTORS[shape]
        mn = C.tile_min_px("R-35")["two-color"][shape]
        rows_spec = [(f, 96, "charcoal", "two-color", "candidate" if abs(f - chosen) > 1e-9 else "chosen") for f in CANDIDATES[shape]]
        rows_spec += [(chosen, 96, "newsprint", "two-color", "chosen"), (chosen, 192, "charcoal", "two-color", "chosen"),
                      (chosen, 192, "newsprint", "two-color", "chosen"),
                      (chosen, mn, "charcoal", "two-color", "minimum"), (chosen, mn, "newsprint", "two-color", "minimum"),
                      (chosen, 48, "charcoal", "two-color", "reference"), (chosen, 48, "newsprint", "two-color", "reference")]
        for f, px, tile, mode, tag in rows_spec:
            m_all = margins(allrows, shape, f)
            m_board = {i: m_all[i] for i in BOARD}
            worst = min(m_all, key=m_all.get)
            report["rows"].append({"shape": shape, "factor": f, "px": px, "tile": tile,
                                   "status": {"reference": "48 px, below the tile minimum, for reference",
                                              "minimum": "chosen, at the two-color tile minimum"}.get(tag, tag),
                                   "min_margin_board": round(min(m_board.values()), 2),
                                   "min_margin_all": round(m_all[worst], 2), "min_margin_id": worst})
            size = {"reference": "48 px, below the tile minimum, for reference",
                    "minimum": f"{px} px, the two-color tile minimum"}.get(tag, f"{px} px")
            label = (f"factor {f:.2f} ({'chosen' if tag != 'candidate' else 'candidate'}), {size}, {tile.capitalize()} tile, two-color. "
                     f"Smallest margin {m_all[worst]:.1f} of 128 units ({worst})")
            parts.append(text(pad, y + 16, label, 14, 600 if tag in ("chosen", "minimum") else 400))
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
            text(pad, 40, "Civic Line tile calibration: one icon factor per shape (DR-10), with each icon's optical scale (S-1) and offset (S-2)", 26, 700),
            text(pad, 66, "Twenty varied icons. The factor scales each icon's option-3 box about the tile center; the optical scale evens out the size "
                 "outliers, and no tile line passes 3.35 units. Margins are the least clearance between ink and the tile edge.", 14),
            text(pad, 88, "Tile minimums (M-1): two-color 72 px square, 76 px rounded, 80 px circle; one-color 48, 52 and 52 px, or 72, 76 and 80 px "
                 "for the 28 icons that need 48 px bare. The 48 px rows sit below the tile minimum and are kept for reference.", 14)]
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
    hs = report["hull_size_spread"]
    print(f"  hull size spread {hs['before_optical_scale']['max_over_min']} -> {hs['after_optical_scale']['max_over_min']} "
          f"(p90/p10 {hs['before_optical_scale']['p90_over_p10']} -> {hs['after_optical_scale']['p90_over_p10']}); "
          f"S-1 rule on the geometric hull differs from the table for {len(rule_diff)} icons")


if __name__ == "__main__":
    main()
