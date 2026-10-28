"""I4. Ampersand B, refinement pass (Phase 2).

Starts from the Phase 1 drawing (p1_amp_b.glyph(), the drawn master after its weight pass) and
redraws it by hand as clean cubic contours with nodes on extrema. Four decisions:

  contrast   thick strokes (bowl stem, diagonal) up to about 0.90 of the wordmark stem, hairlines
             (loop top, bowl bottom, arm) down, so thick to thin moves from about 1.5 to 1 toward
             1.7 to 1 on one broad-nib axis
  crossing   the waist crossing, where the pen path crosses itself between loop and bowl, moves
             down to the glyph's vertical ink center (y 350, the cap band's middle), so in the
             hinge diagram, where the glyph is centered on its ink, it sits on the center line with
             the four nodes
  overshoot  loop top and bowl bottom overshoot by 9.4 font units, the wordmark O's 1.34 units
  terminals  the beak serif, the flat arm cut and the tail's vertical cut stay as drawn in Phase 1

Units: font units, cap height 700, baseline 0, y up (as p1_amp_b). Exported in wordmark units
(cap 100, y down). Each contour is written node by node: smooth nodes carry their tangent, corners
are corners.

Run: python3 -I p2_amp_b.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402

CAP = 700.0
K = 100 / CAP
OS = 9.4                     # overshoot, font units (the wordmark O's 1.34 units)
TOP, BOT = CAP + OS, -OS
STEM_WM = 24.09 / K          # Inter Tight 800 stem of the wordmark's H, in font units (168.6)

# ---------------------------------------------------------------- the drawing
# The waist X: left waist corner L, upper counter tip U, right notch corner R, lower counter tip D.
# The arm crossing: notch floor N, lower counter right corner Kc, arm and tail junction J, V corner V.
G = {
    "L": (204.0, 352.0), "U": (300.0, 397.0), "R": (364.0, 349.0), "D": (247.0, 282.0),
    "N": (510.0, 229.0), "Kc": (414.0, 99.0), "J": (567.0, 166.0), "V": (480.0, 56.0),
    # extremes
    "loop_top": (294.0, TOP), "loop_l": (118.0, 536.0), "loop_r": (460.0, 538.0),
    "bowl_l": (13.0, 166.0), "bowl_b": (262.0, BOT),
    "ctop": (284.0, TOP - 88.0), "c_l": (241.0, 558.0), "c_r": (336.0, 554.0),
    "k_l": (165.0, 186.0), "k_b": (300.0, BOT + 90.0),
    # arm and serif
    "arm_out": 602.0, "arm_in": 510.0, "serif_top": 395.0, "serif_l": 453.0, "serif_bot": 328.0,
    "tail_x": 666.0, "tail_top": 84.0,
}


def outer(g=G):
    L, U, R, D, N, Kc, J, V = (g[k] for k in ("L", "U", "R", "D", "N", "Kc", "J", "V"))
    tx, ty = g["loop_top"]
    ll, lr, bl, bb = g["loop_l"], g["loop_r"], g["bowl_l"], g["bowl_b"]
    ao, ai, st, sl, sb = g["arm_out"], g["arm_in"], g["serif_top"], g["serif_l"], g["serif_bot"]
    tx2, tt = g["tail_x"], g["tail_top"]
    return (
        f"M{tx} {ty}"
        f"C{tx - 96} {ty} {ll[0]} {ll[1] + 108} {ll[0]} {ll[1]}"                       # loop top to loop left
        f"C{ll[0]} {ll[1] - 70} {L[0] - 58} {L[1] + 56} {L[0]} {L[1]}"                  # loop left down into the waist corner
        f"C{L[0] - 80} {L[1] - 50} {bl[0]} {bl[1] + 76} {bl[0]} {bl[1]}"                # bowl, upper left edge
        f"C{bl[0]} {bl[1] - 102} {bb[0] - 134} {bb[1]} {bb[0]} {bb[1]}"                 # bowl, left side to bottom
        f"C{bb[0] + 88} {bb[1]} {V[0] - 60} {V[1] - 44} {V[0]} {V[1]}"                  # bowl bottom into the V
        f"C{V[0] + 36} {V[1] - 38} {V[0] + 82} {0} {V[0] + 138} {0}"                    # tail underside onto the baseline
        f"L{tx2} 0L{tx2} {tt}"                                                          # foot and vertical cut
        f"C{tx2 - 40} {tt + 2} {J[0] + 20} {J[1] - 52} {J[0]} {J[1]}"                    # tail top into the arm junction
        f"C{J[0] + 16} {J[1] + 44} {ao} {J[1] + 92} {ao} {J[1] + 152}"                   # arm, outer edge
        f"L{ao} {st}L{sl} {st}L{sl} {sb}L{ai - 14} {sb}"                                # flat cut, serif top, serif left, beak underside
        f"C{ai - 5} {sb} {ai} {sb - 10} {ai} {sb - 28}"                                 # bracket into the arm
        f"C{ai} {sb - 60} {N[0] + 2} {N[1] + 38} {N[0]} {N[1]}"                          # arm, inner edge, to the notch floor
        f"L{R[0]} {R[1]}"                                                               # diagonal, upper edge
        f"C{R[0] + 60} {R[1] + 44} {lr[0]} {lr[1] - 80} {lr[0]} {lr[1]}"                 # loop right side, rising out of the notch
        f"C{lr[0]} {lr[1] + 100} {tx + 92} {ty} {tx} {ty}Z"                              # loop right to top
    )


def upper(g=G):
    U = g["U"]
    ct, cl, cr = g["ctop"], g["c_l"], g["c_r"]
    return (f"M{ct[0]} {ct[1]}"
            f"C{ct[0] + 36} {ct[1]} {cr[0]} {cr[1] + 38} {cr[0]} {cr[1]}"
            f"C{cr[0]} {cr[1] - 54} {U[0] + 24} {U[1] + 44} {U[0]} {U[1]}"
            f"C{U[0] - 34} {U[1] + 40} {cl[0]} {cl[1] - 44} {cl[0]} {cl[1]}"
            f"C{cl[0]} {cl[1] + 36} {ct[0] - 30} {ct[1]} {ct[0]} {ct[1]}Z")


def lower(g=G):
    D, Kc = g["D"], g["Kc"]
    kl, kb = g["k_l"], g["k_b"]
    return (f"M{Kc[0]} {Kc[1]}"
            f"C{Kc[0] - 40} {Kc[1] - 14} {kb[0] + 46} {kb[1]} {kb[0]} {kb[1]}"
            f"C{kb[0] - 72} {kb[1]} {kl[0]} {kl[1] - 70} {kl[0]} {kl[1]}"
            f"C{kl[0]} {kl[1] + 44} {D[0] - 46} {D[1] - 22} {D[0]} {D[1]}"
            f"L{Kc[0]} {Kc[1]}Z")


def glyph(g=G):
    p = o.path_from_d(outer(g))
    p = o.diff(p, o.path_from_d(upper(g)))
    p = o.diff(p, o.path_from_d(lower(g)))
    return o.simplify(p)


def to_symbol(p_font, x0):
    """Font units (y up) to wordmark units (y down): cap line at y 0, ink left edge at x 0."""
    return o.tx(p_font, a=K, d=-K, e=-x0 * K, f=CAP * K)


# ---------------------------------------------------------------- measurement

STATIONS = {   # name: (point inside the stroke, travel direction in degrees, kind)
    "bowl stem": ((86, 168), 90, "thick"),
    "diagonal": (None, None, "thick"),          # computed: midpoint of the diagonal between the two crossings
    "loop left": ((178, 545), -90, "mid"),
    "loop right": ((400, 545), 90, "mid"),
    "waist upstroke": ((150, 290), 35, "mid"),
    "loop top": ((292, 666), 180, "thin"),
    "bowl bottom": ((290, 36), 180, "thin"),
    "arm": ((556, 300), -90, "thin"),
}


def crossing(g):
    """Waist crossing: the center of the X, where the lines joining opposite corners meet."""
    return P.seg_intersect(g["L"], g["R"], g["U"], g["D"])


def arm_crossing(g):
    return P.seg_intersect(g["Kc"], g["J"], g["N"], g["V"])


def measure(p, g=None, lora=False):
    geom = P.to_shapely(p)
    out = {}
    for name, (pt, ang, kind) in STATIONS.items():
        if name == "diagonal":
            if g is None:
                continue
            a, b = crossing(g), arm_crossing(g)
            pt = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        out[name] = {"width_units": P.chord(geom, pt, ang), "kind": kind}
    thick = [v["width_units"] for v in out.values() if v["kind"] == "thick" and v["width_units"]]
    thin = [v["width_units"] for v in out.values() if v["kind"] == "thin" and v["width_units"]]
    res = {"stations_font_units": out,
           "thick_max": max(thick), "thin_min": min(thin),
           "contrast_max_over_min": round(max(thick) / min(thin), 2),
           "contrast_mean": round((sum(thick) / len(thick)) / (sum(thin) / len(thin)), 2),
           "bowl_stem_over_wordmark_stem": round(out["bowl stem"]["width_units"] / STEM_WM, 3)}
    b = o.bounds(p)
    res["ink_box_font_units"] = [round(v, 1) for v in b]
    res["ink_center_y"] = round((b[1] + b[3]) / 2, 1)
    if g is not None:
        c = crossing(g)
        res["waist_crossing"] = [round(c[0], 1), round(c[1], 1)]
        res["waist_crossing_minus_ink_center_units"] = round(c[1] - res["ink_center_y"], 1)
        ac = arm_crossing(g)
        res["arm_crossing"] = [round(ac[0], 1), round(ac[1], 1)]
    return res


def phase1_crossing():
    """The Phase 1 drawing's corners, read from its final outline (font units)."""
    return {"L": (187.0, 395.0), "U": (296.0, 435.0), "R": (354.0, 382.0), "D": (242.0, 312.0),
            "N": (500.0, 250.0), "Kc": (419.0, 125.0), "J": (573.0, 179.0), "V": (481.0, 66.0)}


def phase1_stations():
    """Station points for the Phase 1 outline (its waist sits 38 units higher)."""
    return {"bowl stem": ((92, 184), 90), "loop left": ((170, 553), -90), "loop right": ((405, 558), 90),
            "waist upstroke": ((150, 320), 35), "loop top": ((290, 662), 180), "bowl bottom": ((290, 40), 180), "arm": ((560, 300), -90)}


def measure_phase1():
    import p1_amp_b as B1
    p = B1.glyph()
    geom = P.to_shapely(p)
    g = phase1_crossing()
    out = {}
    for name, (pt, ang) in phase1_stations().items():
        out[name] = {"width_units": P.chord(geom, pt, ang), "kind": STATIONS[name][2]}
    a, b = crossing(g), arm_crossing(g)
    pt = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    out["diagonal"] = {"width_units": P.chord(geom, pt, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))), "kind": "thick"}
    thick = [v["width_units"] for v in out.values() if v["kind"] == "thick"]
    thin = [v["width_units"] for v in out.values() if v["kind"] == "thin"]
    bb = o.bounds(p)
    c = crossing(g)
    return {"stations_font_units": out, "thick_max": max(thick), "thin_min": min(thin),
            "contrast_max_over_min": round(max(thick) / min(thin), 2),
            "contrast_mean": round((sum(thick) / len(thick)) / (sum(thin) / len(thin)), 2),
            "bowl_stem_over_wordmark_stem": round(out["bowl stem"]["width_units"] / STEM_WM, 3),
            "ink_box_font_units": [round(v, 1) for v in bb], "ink_center_y": round((bb[1] + bb[3]) / 2, 1),
            "waist_crossing": [round(c[0], 1), round(c[1], 1)],
            "waist_crossing_minus_ink_center_units": round(c[1] - (bb[1] + bb[3]) / 2, 1)}


if __name__ == "__main__":
    p = glyph()
    print(json.dumps({"phase1": measure_phase1(), "phase2": measure(p, G), "nodes": P.node_count(p)}, indent=1))
