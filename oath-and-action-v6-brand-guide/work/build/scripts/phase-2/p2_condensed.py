"""I5. The condensed drawing pass at 7.5 to 1 (width over ink height), for Dustin's choice at Gate 2.

Phase 1 narrowed every Inter Tight 800 capital with one scale and gave the stems back their weight.
Straight letters survive that (T, H, I keep Phase 1's drawing here). Round and diagonal letters do
not: the O and C turn into slots, the A's bar and counter shrink, and the N's diagonal clogs its
joins. Those four are drawn again, at weight, on the same metrics:

  O  a condensed round: straight sides between two quarter arcs, sides 22.6 units (rounds 3 percent
     over the 22 unit stem), top and bottom 19, overshoot 1.34 as the regular O; counter 28.8 wide
  C  cut from that O, so the two share one curve; horizontal terminal cuts at y 40 and 68, the
     aperture 28 units tall (4 px at 16 px)
  A  a flat apex 26 wide, legs 21.5 thick square to their direction, a bar 16.5 thick set at y 69
     so the counter above it stays open, 82 wide
  N  stems 22, the diagonal 18.5 thick square to its direction (0.84 of the stem, Inter Tight's own
     ratio is 0.85), parallel edges, the notch tips blunted by 0.8 units as Inter Tight does it

The ampersand is the narrow B (p2_amp_b). Spacing uses the Phase 1 area model, the hinge the
equal-area rule (I2). The 24 and 16 px masters are pixel-fit with the narrow B's own small masters.

Units: wordmark units, cap line y 4, baseline y 104, y down.

Run: python3 -I p2_condensed.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p1_amp_a as A  # noqa: E402
import p1_condensed as C1  # noqa: E402
import p1_wordmark as W  # noqa: E402
import p2_amp_b as B2  # noqa: E402

V = dict(C1.VARIANTS["7.5"])
STEM = V["stem"]          # 22.0
SIDE = 22.6               # round sides
ROUND_TB = 19.0           # top and bottom of rounds
OS_TOP, OS_BOT = 2.66, 105.34
NAMES = ["O", "A", "T", "H", "A2", "C", "T2", "I", "O2", "N"]
SEQ = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
FILES = {"display": "20261028_Wordmark-Condensed-Display-Master.svg", 24: "20261028_Wordmark-Condensed-24px-Master.svg",
         16: "20261028_Wordmark-Condensed-16px-Master.svg"}
K_ARC = 0.60              # handle ratio of the quarter arcs (a circle is 0.552): fuller shoulders


def rounded_box(x0, y0, x1, y1, ys0, ys1, k=K_ARC):
    """Closed path: a box with straight vertical sides from ys0 to ys1, joined top and bottom by
    quarter arcs through the top and bottom centers."""
    cx = (x0 + x1) / 2
    rx = (x1 - x0) / 2
    p = P.pathops.Path()
    p.moveTo(cx, y0)
    p.cubicTo(cx + rx * k, y0, x1, ys0 - (ys0 - y0) * k, x1, ys0)
    p.lineTo(x1, ys1)
    p.cubicTo(x1, ys1 + (y1 - ys1) * k, cx + rx * k, y1, cx, y1)
    p.cubicTo(cx - rx * k, y1, x0, ys1 + (y1 - ys1) * k, x0, ys1)
    p.lineTo(x0, ys0)
    p.cubicTo(x0, ys0 - (ys0 - y0) * k, cx - rx * k, y0, cx, y0)
    p.close()
    return p


def draw_O(w=74.0):
    outer = rounded_box(0, OS_TOP, w, OS_BOT, 44.0, 64.0)
    inner = rounded_box(SIDE, OS_TOP + ROUND_TB, w - SIDE, OS_BOT - ROUND_TB, 40.0, 68.0)
    g = o.simplify(o.diff(outer, inner))
    spec = {"x": [0, SIDE, w - SIDE, w], "stems": [(0, 1), (2, 3)],
            "y": {OS_TOP: "cap", OS_TOP + ROUND_TB: "o_in_top", OS_BOT - ROUND_TB: "o_in_bot", OS_BOT: "base"}}
    return g, spec


def draw_C(w=72.0, t1=40.0, t2=68.0):
    outer = rounded_box(0, OS_TOP, w, OS_BOT, 44.0, 64.0)
    inner = rounded_box(SIDE, OS_TOP + ROUND_TB, w - SIDE, OS_BOT - ROUND_TB, 40.0, 68.0)
    ring = o.diff(outer, inner)
    g = o.simplify(o.diff(ring, o.rect(w / 2, t1, w + 10, t2)))
    spec = {"x": [0, SIDE, w], "stems": [(0, 1)],
            "y": {OS_TOP: "cap", OS_TOP + ROUND_TB: "o_in_top", t1: "c_term_top", t2: "c_term_bot", OS_BOT - ROUND_TB: "o_in_bot", OS_BOT: "base"}}
    return g, spec


def draw_A(w=82.0, flat=26.0, leg=21.5, bar_top=69.0, bar=16.5):
    xa = (w - flat) / 2
    th = math.atan2(100.0, xa)
    h = leg / math.sin(th)
    tan = math.tan(th)
    apex_in_y = 104 - (w / 2 - h) * tan
    outer = o.poly([(0, 104), (xa, 4), (w - xa, 4), (w, 104), (w - h, 104), (w / 2 + 0.4, apex_in_y), (w / 2 - 0.4, apex_in_y), (h, 104)])
    # the bar spans the legs' inner edges
    xl = h + (104 - (bar_top + bar)) / tan - 4
    barp = o.rect(xl, bar_top, w - xl, bar_top + bar)
    hull = o.poly([(0, 104), (xa, 4), (w - xa, 4), (w, 104)])
    g = o.simplify(o.union(outer, o.inter(barp, hull)))
    spec = {"x": [0, h, xa, w - xa, w - h, w], "stems": [],
            "y": {4.0: "cap", bar_top: "a_bar_top", bar_top + bar: "a_bar_bot", 104.0: "base"}}
    info = {"leg_angle_deg": round(math.degrees(th), 1), "leg_horizontal": round(h, 2), "counter_apex_y": round(apex_in_y, 1),
            "counter_height_above_bar": round(bar_top - apex_in_y, 1), "counter_width_at_bar": round(2 * (bar_top - apex_in_y) / tan, 1)}
    return g, spec, info


def draw_N(w=66.0, stem=STEM, diag=18.5, blunt=0.8):
    x_top, x_bot = stem - 3.0, w - stem + 3.0          # where the diagonal's edges meet the cap line and baseline
    dx, dy = x_bot - x_top, 100.0
    # parallel edges diag apart: 100 cos(t) - dx sin(t) = diag, solved for t
    lo, hi = 0.5, 1.5
    for _ in range(60):
        t = (lo + hi) / 2
        f = 100 * math.cos(t) - dx * math.sin(t) - diag
        if f > 0:
            lo = t
        else:
            hi = t
    tan = math.tan(t)
    xr = w - stem
    yr = 4 + (xr - blunt - x_top) * tan
    yl = 104 - (x_bot - (stem + blunt)) * tan
    g = o.poly([(0, 4), (x_top, 4), (xr - blunt, yr), (xr, yr), (xr, 4), (w, 4), (w, 104), (x_bot, 104),
                (stem + blunt, yl), (stem, yl), (stem, 104), (0, 104)])
    spec = {"x": [0, stem, w - stem, w], "stems": [(0, 1), (2, 3)], "y": {4.0: "cap", 104.0: "base"}}
    return o.simplify(g), spec, {"diagonal_angle_deg": round(math.degrees(t), 1), "diagonal_thickness": diag, "notch_tip_right_y": round(yr, 1), "notch_tip_left_y": round(yl, 1)}


def letters():
    G, _ = W.glyphs()
    cg, specs, info = {}, {}, {}
    for n in ("T", "H", "I", "T2"):
        cg[n], specs[n] = C1.condense(G[n], n, V)
    cg["O"], specs["O"] = draw_O()
    cg["O2"], specs["O2"] = cg["O"], specs["O"]
    cg["C"], specs["C"] = draw_C()
    cg["A"], specs["A"], info["A"] = draw_A()
    cg["A2"], specs["A2"] = cg["A"], specs["A"]
    cg["N"], specs["N"], info["N"] = draw_N()
    for n in cg:
        b = o.bounds(cg[n])
        cg[n] = o.tx(cg[n], e=-b[0])
        if n not in ("O", "O2", "C", "A", "A2", "N"):
            pass
    return cg, specs, info


def amp_narrow():
    q = B2.display_symbol(narrow_=True)
    return o.tx(q, f=4.0)


def place(cg, amp, target=None):
    """Area-model spacing (Phase 1 method): each letter pair to the target white area, each
    ampersand pair to 15, nearest ink no closer than 5; then the hinge by equal white area."""
    target = target or V["target_area"]
    prof, placed, pos = {}, {}, {}
    prev = None
    for n in SEQ:
        g = amp if n == "&" else cg[n]
        gb = o.bounds(g)
        g0 = o.tx(g, e=-gb[0])
        prof[n] = o.Profile(g0)
        if prev is None:
            placed[n], pos[n] = g0, 0.0
            prev = n
            continue
        tgt = target if "&" not in (prev, n) else 15.0
        lo, hi = pos[prev] - 40, pos[prev] + 160
        for _ in range(40):
            mid = (lo + hi) / 2
            gp = o.gap_profiles(prof[prev], prof[n], mid - pos[prev], W.DEPTH)
            if gp["area"] < tgt:
                lo = mid
            else:
                hi = mid
        x = (lo + hi) / 2
        gp = o.gap_profiles(prof[prev], prof[n], x - pos[prev], W.DEPTH)
        if gp["min"] < 5.0:
            x += 5.0 - gp["min"]
        pos[n] = x
        placed[n] = o.tx(g0, e=x)
        prev = n
    d, e, lg, rg = W.solve_hinge(placed["H"], placed["&"], placed["A2"], floor=V["hinge_floor"])
    placed["&"] = o.tx(placed["&"], e=d)
    for n in ["A2", "C", "T2", "I", "O2", "N"]:
        placed[n] = o.tx(placed[n], e=e)
    return placed, {"amp_shift": d, "action_shift": e}


def ratio(parts):
    bx = o.bounds(o.union(*parts.values()))
    return round((bx[2] - bx[0]) / (bx[3] - bx[1]), 3)


def display():
    cg, specs, info = letters()
    amp = amp_narrow()
    # find the letter-pair white area that sets the width at 7.5 to 1
    lo, hi = 8.0, 24.0
    for _ in range(24):
        t = (lo + hi) / 2
        parts, hinge = place(cg, amp, t)
        if ratio(parts) < 7.5:
            lo = t
        else:
            hi = t
    t = round((lo + hi) / 2, 2)
    parts, hinge = place(cg, amp, t)
    return parts, specs, info, {"target_area_units": t, **hinge}


YPX_C = {16: dict(W.YPX[16], a_bar_top=10, a_bar_bot=12), 24: dict(W.YPX[24], a_bar_top=15, a_bar_bot=18)}


def pixel_master(parts, specs, size):
    """Pixel fit (Phase 1 method): each glyph's edges to whole pixels by piecewise-linear warps; the
    condensed A's bar is 2 px at 16 px and 3 px at 24 px so its counter stays open."""
    yp = YPX_C[size]
    k = yp["cap_px"] / 100.0
    stem_px = max(2, round(STEM * k))
    out = {}
    for n in NAMES:
        g = parts[n]
        b = o.bounds(g)
        sp = specs[n]
        left_px = round(b[0] * k)
        xs = [x + b[0] for x in sp["x"]]
        tgt = {i: left_px + round((x - xs[0]) * k) for i, x in enumerate(xs)}
        for a_, b_ in sp["stems"]:
            tgt[b_] = tgt[a_] + stem_px
        pairs, last = [], -1e9
        for i, x in enumerate(xs):
            tt = max(tgt[i], last + 1)
            pairs.append((x * k, tt))
            last = tt
        q = o.tx(g, a=k, d=k)
        q = A.xwarp(q, pairs)
        ypairs = []
        for yu, zone in sorted(sp["y"].items()):
            tt = yp["top"] if zone == "cap" else (yp["top"] + yp["cap_px"] if zone == "base" else yp[zone])
            ypairs.append((yu * k, tt))
        out[n] = A.ywarp(q, ypairs)
    ab = o.bounds(parts["&"])
    q = B2.pixel_master("16n" if size == 16 else "24n")[0]
    qb = o.bounds(q)
    cx = (ab[0] + ab[2]) / 2 * k
    out["&"] = o.tx(q, e=round(cx - (qb[2] - qb[0]) / 2) - qb[0])
    target, shifts = W.space_px(out, size)
    hinge = W.solve_hinge_px(out, size, 1.5 if size == 16 else 2.0)
    pushed = W.enforce_gaps(out, {"*": 1.0, ("H", "&"): 1.0, ("&", "A2"): 1.0}, size)
    return out, {"area_target_px": target, "pair_shifts_px": shifts, "hinge_px": hinge, "pushed_px": pushed}


def oath_action(parts):
    """The condensed OATH and ACTION for the hinge diagram, as two paths with ACTION from x 0."""
    oath = o.union(*[parts[n] for n in ("O", "A", "T", "H")])
    action = o.union(*[parts[n] for n in ("A2", "C", "T2", "I", "O2", "N")])
    ab = o.bounds(action)
    return oath, o.tx(action, e=-ab[0]), ab[2] - ab[0]


def export():
    parts, specs, info, log = display()
    bx = o.bounds(o.union(*parts.values()))
    vb = [0, 0, round(bx[2], 2), 108]
    f = P.write_svg(P.asset("wordmark-condensed", FILES["display"]), vb, W.to_svg(parts, vb),
                    "Wordmark, condensed display master at 7.5 to 1, narrow ampersand B (Phase 2 proposal for Gate 2). Cap line y 4, baseline y 104")
    out = {"display": {"file": P.rel(f), "viewBox": vb, **log, **W.measures(parts), "ratio_width_to_ink_height": ratio(parts),
                       "ratio_width_to_cap": round((bx[2] - bx[0]) / 100, 2), "letters": info,
                       "letter_widths": {n: round(o.bounds(parts[n])[2] - o.bounds(parts[n])[0], 2) for n in NAMES}}}
    for size in (24, 16):
        px, plog = pixel_master(parts, specs, size)
        b = o.bounds(o.union(*px.values()))
        vbs = [0, 0, math.ceil(b[2]), size]
        f = P.write_svg(P.asset("wordmark-condensed", FILES[size]), vbs, W.to_svg(px, vbs, nd=3),
                        f"Wordmark, condensed {size} px master on the pixel grid (Phase 2 proposal for Gate 2)")
        out[size] = {"file": P.rel(f), "viewBox": vbs, **plog}
    # drawings of the four redrawn letters beside Phase 1's, for the board
    P.save_json(P.SCRATCH / "specs/condensed.json", out)
    return out


if __name__ == "__main__":
    r = export()
    print(json.dumps(r, indent=1)[:3500])
