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
    "arm_out": 602.0, "arm_in": 510.0, "serif_top": 388.0, "serif_l": 466.0, "serif_bot": 322.0,
    "tail_x": 666.0, "tail_top": 84.0,
}


def outer(g=G):
    L, U, R, D, N, Kc, J, V = (g[k] for k in ("L", "U", "R", "D", "N", "Kc", "J", "V"))
    tx, ty = g["loop_top"]
    ll, lr, bl, bb = g["loop_l"], g["loop_r"], g["bowl_l"], g["bowl_b"]
    ao, ai, st, sl, sb = g["arm_out"], g["arm_in"], g["serif_top"], g["serif_l"], g["serif_bot"]
    tx2, tt = g["tail_x"], g["tail_top"]
    s = g.get("sx", 1.0)            # handle lengths in x follow the drawing's width

    def h(v):
        return round(v * s, 2)
    return (
        f"M{tx} {ty}"
        f"C{tx - h(96)} {ty} {ll[0]} {ll[1] + 108} {ll[0]} {ll[1]}"                       # loop top to loop left
        f"C{ll[0]} {ll[1] - 70} {L[0] - h(58)} {L[1] + 56} {L[0]} {L[1]}"                  # loop left down into the waist corner
        f"C{L[0] - h(80)} {L[1] - 50} {bl[0]} {bl[1] + 76} {bl[0]} {bl[1]}"                # bowl, upper left edge
        f"C{bl[0]} {bl[1] - 102} {bb[0] - h(134)} {bb[1]} {bb[0]} {bb[1]}"                 # bowl, left side to bottom
        f"C{bb[0] + h(88)} {bb[1]} {V[0] - h(60)} {V[1] - 44} {V[0]} {V[1]}"               # bowl bottom into the V
        f"C{V[0] + h(36)} {V[1] - 38} {V[0] + h(82)} {0} {V[0] + h(138)} {0}"               # tail underside onto the baseline
        f"L{tx2} 0L{tx2} {tt}"                                                             # foot and vertical cut
        f"C{tx2 - h(40)} {tt + 2} {J[0] + h(20)} {J[1] - 52} {J[0]} {J[1]}"                 # tail top into the arm junction
        f"C{J[0] + h(16)} {J[1] + 44} {ao} {J[1] + 92} {ao} {J[1] + 152}"                  # arm, outer edge
        f"L{ao} {st}L{sl} {st}L{sl} {sb}L{ai - 14} {sb}"                                   # flat cut, serif top, serif left, beak underside
        f"C{ai - 5} {sb} {ai} {sb - 10} {ai} {sb - 28}"                                    # bracket into the arm
        f"C{ai} {sb - 60} {N[0] + 2} {N[1] + 38} {N[0]} {N[1]}"                             # arm, inner edge, to the notch floor
        f"L{R[0]} {R[1]}"                                                                  # diagonal, upper edge
        f"C{R[0] + h(44)} {R[1] + 54} {lr[0]} {lr[1] - 92} {lr[0]} {lr[1]}"                # loop right side, rising out of the notch
        f"C{lr[0]} {lr[1] + 100} {tx + h(92)} {ty} {tx} {ty}Z"                              # loop right to top
    )


def upper(g=G):
    U = g["U"]
    ct, cl, cr = g["ctop"], g["c_l"], g["c_r"]
    s = g.get("sx", 1.0)

    def h(v):
        return round(v * s, 2)
    return (f"M{ct[0]} {ct[1]}"
            f"C{ct[0] + h(36)} {ct[1]} {cr[0]} {cr[1] + 38} {cr[0]} {cr[1]}"
            f"C{cr[0]} {cr[1] - 54} {U[0] + h(24)} {U[1] + 44} {U[0]} {U[1]}"
            f"C{U[0] - h(34)} {U[1] + 40} {cl[0]} {cl[1] - 44} {cl[0]} {cl[1]}"
            f"C{cl[0]} {cl[1] + 36} {ct[0] - h(30)} {ct[1]} {ct[0]} {ct[1]}Z")


def lower(g=G):
    D, Kc = g["D"], g["Kc"]
    kl, kb = g["k_l"], g["k_b"]
    s = g.get("sx", 1.0)

    def h(v):
        return round(v * s, 2)
    return (f"M{Kc[0]} {Kc[1]}"
            f"C{Kc[0] - h(40)} {Kc[1] - 14} {kb[0] + h(46)} {kb[1]} {kb[0]} {kb[1]}"
            f"C{kb[0] - h(72)} {kb[1]} {kl[0]} {kl[1] - 70} {kl[0]} {kl[1]}"
            f"C{kl[0]} {kl[1] + 44} {D[0] - h(46)} {D[1] - 22} {D[0]} {D[1]}"
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

def stations(g):
    """Measuring stations, placed from the drawing's own points: (point inside the stroke, travel
    direction in degrees, kind). Thick and thin strokes set the contrast; mid strokes are reported."""
    bl, kl, ll, cl, cr, lr = g["bowl_l"], g["k_l"], g["loop_l"], g["c_l"], g["c_r"], g["loop_r"]
    return {
        "bowl stem": (((bl[0] + kl[0]) / 2, bl[1]), 90, "thick"),
        "diagonal": (None, None, "thick"),          # midpoint of the diagonal between the two crossings
        "loop left": (((ll[0] + cl[0]) / 2, 545), -90, "mid"),
        "loop right": (((cr[0] + lr[0]) / 2, 545), 90, "mid"),
        "waist upstroke": (((g["L"][0] + kl[0]) / 2 - 34, (g["L"][1] + kl[1]) / 2 + 21), 35, "mid"),
        "loop top": ((g["ctop"][0] + 8, (TOP + g["ctop"][1]) / 2), 180, "thin"),
        "bowl bottom": ((g["k_b"][0] - 10, (BOT + g["k_b"][1]) / 2), 180, "thin"),
        "arm": (((g["arm_in"] + g["arm_out"]) / 2, 300 if g["N"][1] < 290 else (g["N"][1] + g["serif_bot"]) / 2), -90, "thin"),
    }


def crossing(g):
    """Waist crossing: the center of the X, where the lines joining opposite corners meet."""
    return P.seg_intersect(g["L"], g["R"], g["U"], g["D"])


def arm_crossing(g):
    return P.seg_intersect(g["Kc"], g["J"], g["N"], g["V"])


def measure(p, g=None, lora=False):
    geom = P.to_shapely(p)
    out = {}
    for name, (pt, ang, kind) in stations(g).items():
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
        out[name] = {"width_units": P.chord(geom, pt, ang), "kind": stations(G)[name][2]}
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


# ---------------------------------------------------------------- the narrow drawing, for the condensed wordmark

NARROW = 0.85


def narrow_geometry(s=NARROW):
    """The narrow drawing's points. Every x is scaled by s about the ink's left edge; then the bowl
    stem, loop sides and arm get their regular widths back, the loop keeps more of its width than
    the whole (so its counter stays open at 16 px), and the beak gives up length to keep clear of
    the loop."""
    g0 = G
    x0 = g0["bowl_l"][0]

    def X(v):
        return round(x0 + (v - x0) * s, 1)

    g = {k: ((X(v[0]), v[1]) if isinstance(v, tuple) else v) for k, v in g0.items()}
    for k in ("arm_out", "arm_in", "serif_l", "tail_x"):
        g[k] = X(g0[k])
    g["sx"] = s
    g["loop_l"] = (X(g0["loop_l"][0]) - 4, g0["loop_l"][1])
    g["loop_r"] = (X(g0["loop_r"][0]) + 14, g0["loop_r"][1])
    side = 119.0
    g["c_l"] = (g["loop_l"][0] + side, g0["c_l"][1])
    g["c_r"] = (g["loop_r"][0] - side, g0["c_r"][1])
    g["ctop"] = (round((g["c_l"][0] + g["c_r"][0]) / 2 - 4, 1), g0["ctop"][1])
    g["loop_top"] = (round((g["loop_l"][0] + g["loop_r"][0]) / 2, 1), g0["loop_top"][1])
    g["U"] = (round((g["c_l"][0] + g["c_r"][0]) / 2 + 12, 1), g0["U"][1])
    g["k_l"] = (g["bowl_l"][0] + (g0["k_l"][0] - g0["bowl_l"][0]), g0["k_l"][1])
    g["arm_out"] = X(g0["arm_out"]) + 6
    g["arm_in"] = g["arm_out"] - (g0["arm_out"] - g0["arm_in"])
    g["serif_l"] = g["arm_in"] - 32
    g["tail_x"] = X(g0["tail_x"]) + 4
    g["J"] = (g["arm_out"] - (g0["arm_out"] - g0["J"][0]), g0["J"][1])
    g["D"] = (g["D"][0] - 8, g["D"][1])
    R = g["R"]
    slope = (g0["N"][1] - g0["R"][1]) / ((g0["N"][0] - g0["R"][0]) * s)
    g["N"] = (g["arm_in"], round(R[1] + slope * (g["arm_in"] - R[0]), 1))
    return g


def narrow():
    return glyph(narrow_geometry())


def measure_narrow():
    g = narrow_geometry()
    return measure(narrow(), g)


# ---------------------------------------------------------------- pixel masters
# Drawn by hand on the pixel grid over the display drawing (y down, 1 unit = 1 px). Every horizontal
# and vertical edge sits on a whole pixel; the waist crossing sits on the box's middle row line.

B16 = ("M4.4 0H7.2C8.9 0 10 1.2 10 2.8V4.2C10 5.6 8.9 6.9 7.6 8.1"      # loop right, into the notch corner
       "L11 10.9V9.6C11 9.2 10.8 9 10.4 9H10V7H13V9.8"                     # diagonal, arm inner edge, beak, flat cut
       "C13 10.8 12.6 11.5 12.1 12.1"                                      # arm outer edge to the junction
       "C12.6 13.3 13.2 13.9 14 14V16H12.8"                                # tail top, vertical cut, foot
       "C11.7 16 10.8 15.3 10.2 14.6"                                      # tail underside to the V
       "C9.2 15.6 7.8 16 6.2 16H4.4"                                       # bowl bottom
       "C1.8 16 0 14.5 0 12.4V11.6C0 9.8 1.6 8.8 3.8 8"                    # bowl left, up to the waist corner
       "C2.7 7.1 2 5.8 2 4.6V3C2 1.2 3 0 4.4 0Z")                          # loop left
B16_UPPER = "M5.5 2C4.6 2 4 2.6 4 3.5V4.4C4 5.4 4.9 6.3 5.8 7C6.6 6.1 7 5.3 7 4.3V3.5C7 2.6 6.4 2 5.5 2Z"
B16_LOWER = "M5.1 9.4L8.7 13.3C8.1 13.8 7.3 14 6.5 14H4.6C3.6 14 3 13.3 3 12.3V10.9C3 10.2 3.8 9.7 5.1 9.4Z"

B24 = ("M6.6 0H10.6C13 0 14 2 14 4.4V6.6C14 8.8 12.6 10.6 11.3 12"
       "L16 16V14.2C16 13.5 15.6 13 15.2 13H15V11H19V14.6"
       "C19 16 18.6 17.2 17.8 18.2"
       "C18.6 20 19.6 20.9 21 21V24H19.4"
       "C17.6 24 16.2 23 15 21.8"
       "C13.6 23.3 11.6 24 9 24H7.4"
       "C3 24 0 21.6 0 18.6V17.6C0 14.8 2.6 13.2 6.1 12"
       "C4.4 10.6 3 8.6 3 6.6V4.6C3 1.8 4.6 0 6.6 0Z")
B24_UPPER = "M8.5 3C7.6 3 7 3.8 7 5V6.4C7 8 8 9.4 9.2 10.4C9.8 9.4 10 8.3 10 7V5C10 3.8 9.4 3 8.5 3Z"
B24_LOWER = "M7.6 14.3L12.9 20.2C12 20.8 11 21 9.8 21H7.4C5.9 21 5 20 5 18.6V16.8C5 15.6 6 14.8 7.6 14.3Z"

B16N = ("M4.2 0H5.8C7.2 0 8 1.1 8 2.6V4.2C8 5.6 7.2 6.9 6.3 8.1"
        "L9 10.6V7H11V9.8"                                                   # no beak at this size: it would close the notch
        "C11 10.8 10.7 11.5 10.3 12.1"
        "C10.8 13.3 11.3 13.9 12 14V16H11"
        "C10 16 9.2 15.3 8.7 14.6"
        "C7.9 15.6 6.8 16 5.6 16H4.2"
        "C1.7 16 0 14.5 0 12.4V11.6C0 9.8 1.5 8.8 3.4 8"
        "C2.5 7.1 2 5.8 2 4.6V2.8C2 1.1 2.9 0 4.2 0Z")
B16N_UPPER = "M5 2C4.4 2 4 2.6 4 3.4V4.4C4 5.4 4.5 6.3 5.2 7C5.8 6.2 6 5.3 6 4.4V3.4C6 2.6 5.6 2 5 2Z"
B16N_LOWER = "M4.6 9.5L7.5 13.3C7 13.8 6.4 14 5.8 14H4.5C3.6 14 3 13.3 3 12.3V10.9C3 10.2 3.6 9.8 4.6 9.5Z"

B24N = ("M6.4 0H9.4C11.6 0 13 2 13 4.4V6.6C13 8.8 11.4 10.6 9.9 12"
        "L14 15.9V14.2C14 13.5 13.6 13 13.2 13H13V11H17V14.6"
        "C17 16 16.6 17.2 15.8 18.2"
        "C16.6 20 17.4 20.9 18 21V24H16.6"
        "C15.2 24 14 23 13.1 21.8"
        "C11.9 23.3 10.2 24 8.2 24H7"
        "C2.8 24 0 21.6 0 18.6V17.6C0 14.8 2.4 13.2 5.4 12"
        "C4.2 10.6 3 8.6 3 6.6V4.6C3 1.8 4.4 0 6.4 0Z")
B24N_UPPER = "M8.5 3C7.6 3 7 3.8 7 5V6.4C7 8 7.7 9.4 8.5 10.4C9.4 9.4 10 8.3 10 7V5C10 3.8 9.4 3 8.5 3Z"
B24N_LOWER = "M6.4 14.4L11.3 20.2C10.5 20.8 9.6 21 8.6 21H7.2C5.8 21 5 20 5 18.6V16.8C5 15.6 5.5 14.8 6.4 14.4Z"

PIXEL = {"16": (B16, B16_UPPER, B16_LOWER, 14), "24": (B24, B24_UPPER, B24_LOWER, 21),
         "16n": (B16N, B16N_UPPER, B16N_LOWER, 12), "24n": (B24N, B24N_UPPER, B24N_LOWER, 18)}


def pixel_master(key):
    outer_d, up, lo, w = PIXEL[key]
    p = o.diff(o.diff(o.path_from_d(outer_d), o.path_from_d(up)), o.path_from_d(lo))
    return o.simplify(p), w


def b16():
    return pixel_master("16")[0]


def b24():
    return pixel_master("24")[0]


FILES = {
    "display": "20261028_Amp-B-Display-Master.svg", "16": "20261028_Amp-B-16px-Master.svg", "24": "20261028_Amp-B-24px-Master.svg",
    "narrow": "20261028_Amp-B-Narrow-Display-Master.svg", "16n": "20261028_Amp-B-Narrow-16px-Master.svg", "24n": "20261028_Amp-B-Narrow-24px-Master.svg",
}


def display_symbol(narrow_=False):
    g = narrow() if narrow_ else glyph()
    b = o.bounds(g)
    q = to_symbol(g, b[0])
    return q


def export():
    """Write the six ampersand masters. Display masters are in wordmark units: cap line at y 0,
    baseline at y 100, ink from x 0; overshoot shows as ink above 0 and below 100."""
    out = {}
    for key, nar in (("display", False), ("narrow", True)):
        q = display_symbol(nar)
        qb = o.bounds(q)
        vb = [0, round(qb[1], 2), round(qb[2], 2), round(qb[3] - qb[1], 2)]
        lab = "narrow, for the condensed wordmark" if nar else "display master"
        f = P.write_svg(P.asset("ampersand", FILES[key]), vb, f'<path fill="currentColor" d="{o.d_from_path(q)}"/>',
                        f"Ampersand B, {lab} (Phase 2 refinement). Cap line y 0, baseline y 100")
        out[key] = {"file": P.rel(f), "viewBox": vb, "nodes": P.node_count(q)}
    for key in ("16", "24", "16n", "24n"):
        q, w = pixel_master(key)
        h = 16 if key.startswith("16") else 24
        lab = f"{h} px master{', narrow' if key.endswith('n') else ''}, drawn on the pixel grid"
        f = P.write_svg(P.asset("ampersand", FILES[key]), [0, 0, w, h], f'<path fill="currentColor" d="{o.d_from_path(q, 3)}"/>',
                        f"Ampersand B, {lab} (Phase 2)")
        out[key] = {"file": P.rel(f), "viewBox": [0, 0, w, h], "nodes": P.node_count(q)}
    m = {"phase1_first_drawing": measure_phase1(), "phase2_refined": measure(glyph(), G), "phase2_narrow": measure_narrow(),
         "geometry_font_units": {k: v for k, v in G.items()}, "narrow_geometry_font_units": narrow_geometry(),
         "wordmark_stem_font_units": round(STEM_WM, 1), "masters": out,
         "units": "font units: cap height 700, baseline 0, y up; 7 font units = 1 wordmark unit"}
    P.save_json(P.SCRATCH / "specs/amp_b.json", m)
    return m





if __name__ == "__main__":
    r = export()
    print(json.dumps({k: (v if k == "masters" else {kk: vv for kk, vv in v.items() if kk != "stations_font_units"}) for k, v in r.items() if k in ("masters", "phase1_first_drawing", "phase2_refined", "phase2_narrow")}, indent=1))
