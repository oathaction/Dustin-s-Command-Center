"""Item 1. Re-export the six clipped symbols with viewBoxes that hold their full ink.

The outlines are untouched. Each proposal keeps the symbol's own coordinate origin, so every
placement that addresses the symbol by its cap band stays valid, and extends the viewBox to the
exact ink bounds (fontTools BoundsPen, curves included) rounded outward to 0.01 unit.
The lockups that place tl-1, tl-2a, tl-2b and url-1 (L4, L5, L6) get corrected placements.

Run: python3 -I p1_item01_reexport.py
Writes: work/boards/phase-1/identity/01-reexport/*.svg and scratch spec JSON.
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402

DIR = o.OUT / "01-reexport"
NAMES = {"amp": "Amp-Master", "tl-1": "Tagline-1-Line", "tl-2a": "Tagline-2-Line-A", "tl-2b": "Tagline-2-Line-B",
         "url-1": "Url-1", "stacked": "Stacked-L2"}


def outward(v, up):
    return (math.ceil(v * 100) if up else math.floor(v * 100)) / 100


def symbol_body(name):
    s = o.strip_defs(o.sprite(name))
    s = re.sub(r"<title>.*?</title>", "", s)
    return s[s.find(">") + 1: s.rfind("</svg>")]


def run():
    spec = {"id": "p01", "pairs": [], "measures": {}}
    for name, slug in NAMES.items():
        vb = o.viewbox(o.sprite(name))
        paths = o.sprite_paths(name)
        bx = [o.bounds(p) for p in paths]
        ink = [min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx)]
        x0 = min(vb[0], outward(ink[0], False))
        y0 = min(vb[1], outward(ink[1], False))
        x1 = max(vb[0] + vb[2], outward(ink[2], True))
        y1 = max(vb[1] + vb[3], outward(ink[3], True))
        nvb = [round(x0, 2), round(y0, 2), round(x1 - x0, 2), round(y1 - y0, 2)]
        body = symbol_body(name)
        out = DIR / f"20261021_{slug}-Reexported.svg"
        o.write_svg(out, nvb, f'<g id="{name}">{body}</g>', f"{name}, re-exported with its full ink (proposal, Phase 1)")
        over = {"left": round(vb[0] - ink[0], 2), "top": round(vb[1] - ink[1], 2),
                "right": round(ink[2] - (vb[0] + vb[2]), 2), "bottom": round(ink[3] - (vb[1] + vb[3]), 2)}
        spec["measures"][name] = {"old_viewBox": vb, "ink_box": [round(v, 2) for v in ink], "new_viewBox": nvb,
                                  "overflow_units": {k: v for k, v in over.items() if v > 0.005},
                                  "file": str(out.relative_to(o.ROOT))}
        spec["pairs"].append({"name": name, "orig": {"vb": vb, "body": body}, "prop": {"vb": nvb, "body": body}})
    # corrected lockup placements: a use element addressed the old viewBox; keep the same scale
    lock = {}
    for lk, uses in {"l5": [("tl-1", 0, 143.04, 581.35, 25.92)],
                     "l6": [("tl-1", 80, 170.58, 363.34, 16.2), ("url-1", 471.34, 170.58, 181.02, 16.2)],
                     "l4": [("tl-2a", 368.65, 25.12, 338.05, 23.76), ("tl-2b", 368.65, 61.12, 185.7, 23.76)]}.items():
        rows = []
        for sym, x, y, w, h in uses:
            m = spec["measures"][sym]
            ovb, nvb = m["old_viewBox"], m["new_viewBox"]
            s = h / ovb[3]
            rows.append({"symbol": sym, "old": {"x": x, "y": y, "width": w, "height": h},
                         "new": {"x": round(x + (nvb[0] - ovb[0]) * s, 2), "y": round(y + (nvb[1] - ovb[1]) * s, 2),
                                 "width": round(nvb[2] * s, 2), "height": round(nvb[3] * s, 2)}})
        lock[lk] = rows
    spec["lockup_placements"] = lock
    # the hinge places #amp by its old box; same correction
    m = spec["measures"]["amp"]
    s = 100.61 / m["old_viewBox"][3]
    spec["hinge_amp_placement"] = {"old": {"x": 368.67, "y": 5.59, "width": 89.62, "height": 100.61},
                                   "new": {"x": round(368.67 + m["new_viewBox"][0] * s, 2), "y": round(5.59 + m["new_viewBox"][1] * s, 2),
                                           "width": round(m["new_viewBox"][2] * s, 2), "height": round(m["new_viewBox"][3] * s, 2)}}
    (o.SCRATCH / "specs").mkdir(parents=True, exist_ok=True)
    (o.SCRATCH / "specs/p01.json").write_text(json.dumps(spec, indent=1))
    print(json.dumps({k: v for k, v in spec.items() if k != "pairs"}, indent=1))


if __name__ == "__main__":
    run()
