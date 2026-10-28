"""I1. Re-export the six clipped V5 symbols with viewBoxes that hold their full ink.

Outlines and origins are V5's, untouched; only the viewBox grows to the exact ink bounds
(fontTools BoundsPen on the curves), rounded outward to 0.01 unit. Same method as the Phase 1
proposal (p1_item01_reexport.py), now written as masters. The lockups that place these symbols get
the matching placements, recorded in the spec.

Run: python3 -I p2_reexport.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p1_item01_reexport as R1  # noqa: E402

NAMES = {"amp": "Amp-V5-Lora-Master", "tl-1": "Tagline-1-Line", "tl-2a": "Tagline-2-Line-A", "tl-2b": "Tagline-2-Line-B",
         "url-1": "Url-1", "stacked": "Stacked-L2-V5"}


def run():
    spec = {}
    for name, slug in NAMES.items():
        vb = o.viewbox(o.sprite(name))
        paths = o.sprite_paths(name)
        bx = [o.bounds(p) for p in paths]
        ink = [min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx)]
        x0 = min(vb[0], R1.outward(ink[0], False))
        y0 = min(vb[1], R1.outward(ink[1], False))
        x1 = max(vb[0] + vb[2], R1.outward(ink[2], True))
        y1 = max(vb[1] + vb[3], R1.outward(ink[3], True))
        nvb = [round(x0, 2), round(y0, 2), round(x1 - x0, 2), round(y1 - y0, 2)]
        f = P.write_svg(P.asset("reexport", f"{P.DATE}_{slug}-Reexported.svg"), nvb, f'<g id="{name}">{R1.symbol_body(name)}</g>',
                        f"V5 symbol {name}, re-exported with its full ink (I1, Phase 2). Outlines unchanged")
        over = {"left": round(vb[0] - ink[0], 2), "top": round(vb[1] - ink[1], 2), "right": round(ink[2] - (vb[0] + vb[2]), 2), "bottom": round(ink[3] - (vb[1] + vb[3]), 2)}
        spec[name] = {"v5_viewBox": vb, "ink_box": [round(v, 2) for v in ink], "viewBox": nvb,
                      "ink_outside_v5_box_units": {k: v for k, v in over.items() if v > 0.005}, "file": P.rel(f)}
    P.save_json(P.SCRATCH / "specs/reexport.json", spec)
    return spec


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
