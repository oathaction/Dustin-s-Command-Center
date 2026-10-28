"""I2 and I3. The wordmark at today's width, carrying the refined ampersand B.

I2: the hinge gaps by equal white area (option 2b): the white between H and the ampersand and
between the ampersand and A, counted row by row across the cap band to 0.15x past the nearest
point, is equal on both sides, with no ink closer than 0.07x.
I3: three masters. Display (2b plus the Phase 1 pair adjustments: T to H and T to I open 1.4
units, I to O and O to N 2.4), 24 px and 16 px (stems and bars on whole pixels, optical tracking per
size, T arms trimmed, the ampersand at full box height drawn from B's own 24 and 16 px masters).

Method and spacing model are Phase 1's (p1_wordmark); only the ampersand changes.

Run: python3 -I p2_wordmark.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p1_wordmark as W  # noqa: E402
import p2_amp_b as B2  # noqa: E402

SEQ = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
FILES = {"display": "20261028_Wordmark-Display-Master.svg", 24: "20261028_Wordmark-24px-Master.svg", 16: "20261028_Wordmark-16px-Master.svg"}
MIN_GAPS = {"*": 1.0, ("T", "H"): 2.0, ("T2", "I"): 2.0, ("H", "&"): 2.0, ("&", "A2"): 1.0}


def amp_display():
    """Refined B in wordmark units with its cap line on the letters' cap line (y 4)."""
    q = B2.display_symbol()
    return o.tx(q, e=368.72, f=4.0)


def display_parts(G=None, amp=None):
    G = G or W.glyphs()[0]
    amp = amp or amp_display()
    adj = W.spacing_display(G, amp)
    d, e, l, r = W.solve_hinge(G["H"], amp, G["A2"])
    parts = W.place(G, amp, adj, d, e)
    return parts, adj, {"amp_shift": d, "action_shift": e, "left": l, "right": r}


def pixel_parts(size, G=None):
    G = G or W.glyphs()[0]
    amp = amp_display()
    adj = W.spacing_display(G, amp)
    d, e, _, _ = W.solve_hinge(G["H"], amp, G["A2"])
    pp = W.place(G, amp, adj, d, e, track=W.TRACK[size], t_trim=W.T_TRIM[size])
    ampx = B2.b16() if size == 16 else B2.b24()
    px = W.pixel_master(pp, size, ampx)
    target, shifts = W.space_px(px, size)
    hinge = W.solve_hinge_px(px, size, 1.5 if size == 16 else 2.0)
    pushed = W.enforce_gaps(px, MIN_GAPS, size)
    return px, {"area_target_px": target, "pair_shifts_px": shifts, "hinge_px": hinge, "pushed_px": pushed}


def pairs_px(px, size):
    cap = W.YPX[size]["cap_px"]
    out = {}
    for a, b in zip(SEQ, SEQ[1:]):
        g = o.pair_gap(px[a], px[b], cap_top=1, base=1 + cap, step=0.05, depth=W.DEPTH * cap / 100)
        out[f"{a.rstrip('2')}{b.rstrip('2')}"] = {"nearest_px": round(g["min"], 2), "area_px": round(g["area"], 2)}
    return out


def body(parts, nd=2):
    return W.to_svg(parts, None, nd=nd)


def export():
    G, amp_v5 = W.glyphs()
    out = {}
    v5 = W.place(G, amp_v5, {}, 0.0, 0.0)
    out["v5"] = W.measures(v5)
    # V5 glyph with 2b, the Phase 1 record, for comparison on the board
    d0, e0, _, _ = W.solve_hinge(G["H"], amp_v5, G["A2"])
    out["v5_glyph_2b"] = {"amp_shift": d0, "action_shift": e0, **W.measures(W.place(G, amp_v5, {}, d0, e0))}
    parts, adj, hinge = display_parts(G)
    bx = o.bounds(o.union(*parts.values()))
    vb = [0, 0, round(bx[2], 2), 108]
    f = P.write_svg(P.asset("wordmark", FILES["display"]), vb, body(parts),
                    "Wordmark, display master with ampersand B (Phase 2). Cap line y 4, baseline y 104")
    m = W.measures(parts)
    out["display"] = {"file": P.rel(f), "viewBox": vb, "hinge": {"amp_shift": hinge["amp_shift"], "action_shift": hinge["action_shift"]},
                      "pair_adjustments_units": {f"{a}{b}".replace("2", ""): v for (a, b), v in adj.items()}, **m,
                      "ratio_width_to_ink_height": round(bx[2] / (bx[3] - bx[1]), 2), "ink_box": [round(v, 2) for v in bx]}
    for size in (24, 16):
        px, log = pixel_parts(size, G)
        bx = o.bounds(o.union(*px.values()))
        vb = [0, 0, math.ceil(bx[2]), size]
        f = P.write_svg(P.asset("wordmark", FILES[size]), vb, body(px, 3), f"Wordmark, {size} px master on the pixel grid, ampersand B (Phase 2)")
        out[size] = {"file": P.rel(f), "viewBox": vb, "track_units": W.TRACK[size], "t_arm_trim_units": W.T_TRIM[size], **log, "pairs": pairs_px(px, size)}
    P.save_json(P.SCRATCH / "specs/wordmark.json", out)
    return out


if __name__ == "__main__":
    r = export()
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ("viewBox", "hinge", "H&", "&A", "width_units", "ratio_width_to_ink_height", "hinge_px", "pushed_px", "amp_shift", "action_shift")} for k, v in r.items()}, indent=1))
