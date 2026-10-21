"""Item 4. Ampersand option A: an optical tune of the Lora-derived master, and a true small master.

Everything here starts from the V5 outline (Lora Bold '&', 120 points) and changes it with
measurable operations, so the glyph stays the one Dustin knows:

  display tune   an elliptical-pen embolden (more weight on the thin horizontals than on the
                 stems), then a vertical warp that sets the overshoot to the wordmark's own
                 (the O overshoots 1.34 units) and keeps the tail flat on the baseline.
  small master   a heavier elliptical embolden applied outward only: the two counters and the arm
                 notch are restored to their original size after the embolden, the tips of both
                 counters are opened with small carved wedges, and the result is snapped to the
                 16 px pixel grid with a piecewise-linear warp (stems and horizontals on whole pixels).

Units: font units (UPM 1000, y up) inside this file; exported symbols use wordmark units
(cap height 100, y down), the same scale V5 uses (0.14).

Run: python3 -I p1_amp_a.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
import pathops  # noqa: E402

S = 0.14            # font units to wordmark units, as V5
CAP_FONT = 100 / S  # 714.29: the wordmark cap line in Lora font units
DIR = o.OUT / "04-amp-a"


def lora():
    return o.path_from_d(o.AMP_D)  # font units, y up


def contour_paths(p):
    out = []
    for c in p.contours:
        q = pathops.Path()
        c.draw(q.getPen())
        out.append(q)
    return out


def ell_embolden(p, dx, dy, outward_only=False, join=pathops.LineJoin.MITER_JOIN):
    """Grow an outline by dx horizontally and dy vertically (an elliptical pen)."""
    k = dy / dx
    q = o.tx(p, a=k)  # stretch x so a round pen of radius dy adds dy/k = dx horizontally
    s = pathops.Path()
    q.draw(s.getPen())
    s.stroke(2 * dy, pathops.LineCap.BUTT_CAP, join, 3)
    s.convertConicsToQuads()
    g = o.union(q, s)
    return o.tx(g, a=1 / k)


def counters(p):
    """The two inner contours of the Lora ampersand (lower counter, upper counter)."""
    cs = contour_paths(p)
    cs.sort(key=lambda c: -(o.bounds(c)[2] - o.bounds(c)[0]) * (o.bounds(c)[3] - o.bounds(c)[1]))
    outer, rest = cs[0], cs[1:]
    rest.sort(key=lambda c: o.bounds(c)[1])
    return outer, rest[0], rest[1]  # lower, upper


# The arm notch of the Lora outline: the white between the diagonal and the arm, closed across
# its mouth by the serif's left side (Lora points 34 to 51).
def notch_region():
    # exact notch: polygon between the diagonal's upper edge and the arm's inner edge, from the Lora points
    pts = [(318, 364), (346, 335), (406, 275), (480, 205), (484, 229.5), (485, 255), (479, 299), (461.5, 322.5), (432, 331), (432, 395), (330, 395)]
    return o.poly(pts)


def ywarp(p, pairs):
    """Piecewise-linear warp of y (pairs of (src, dst), sorted by src), applied to every point."""
    pairs = sorted(pairs)

    def f(y):
        if y <= pairs[0][0]:
            (a, b), (c, d) = pairs[0], pairs[1]
        elif y >= pairs[-1][0]:
            (a, b), (c, d) = pairs[-2], pairs[-1]
        else:
            for (a, b), (c, d) in zip(pairs, pairs[1:]):
                if a <= y <= c:
                    break
        return b + (y - a) * (d - b) / (c - a)
    return remap(p, lambda x, y: (x, f(y)))


def xwarp(p, pairs):
    pairs = sorted(pairs)

    def f(x):
        if x <= pairs[0][0]:
            (a, b), (c, d) = pairs[0], pairs[1]
        elif x >= pairs[-1][0]:
            (a, b), (c, d) = pairs[-2], pairs[-1]
        else:
            for (a, b), (c, d) in zip(pairs, pairs[1:]):
                if a <= x <= c:
                    break
        return b + (x - a) * (d - b) / (c - a)
    return remap(p, lambda x, y: (f(x), y))


def remap(p, fn):
    q = pathops.Path()
    pen = q.getPen()
    for verb, pts in p.segments:
        m = [fn(*pt) for pt in pts]
        if verb == "moveTo":
            pen.moveTo(m[0])
        elif verb == "lineTo":
            pen.lineTo(m[0])
        elif verb == "qCurveTo":
            pen.qCurveTo(*m)
        elif verb == "curveTo":
            pen.curveTo(*m)
        elif verb == "closePath":
            pen.closePath()
        elif verb == "endPath":
            pen.endPath()
    return q


def to_wordmark_units(p, x0=0.0):
    """Font units (y up) to symbol units (y down), placing the cap line at y = 0 and x0 at x = 0."""
    return o.tx(p, a=S, d=-S, e=-x0 * S, f=CAP_FONT * S)


# ---------------------------------------------------------------- display tune

def a_display():
    g = lora()
    dx, dy = 3.0, 7.5
    e = ell_embolden(g, dx, dy)
    b = o.bounds(e)
    # overshoot: bowl bottom to -9.4 (1.34 wordmark units), tail flat on the baseline,
    # loop top to the cap line plus 9.4
    target_os = 1.34 / S
    e = ywarp(e, [(b[1], -target_os), (-dy, 0.0), (b[3], CAP_FONT + target_os)])
    return o.simplify(e)


# ---------------------------------------------------------------- small master

def a_small_geometry(dx=8.0, dy=13.0):
    """Heavier strokes, grown outward only: both counters and the arm notch keep their V5 size."""
    g = lora()
    outer, low, up = counters(g)
    e = ell_embolden(g, dx, dy)
    e = o.diff(e, low)
    e = o.diff(e, up)
    e = o.diff(e, notch_region())
    b = o.bounds(e)
    target_os = 1.34 / S
    e = ywarp(e, [(b[1], -target_os), (-dy, 0.0), (b[3], CAP_FONT + target_os)])
    return o.simplify(e)


# Feature lines of the Lora outline (font units) used to fit the small master to the pixel grid.
# x features: bowl outer left, loop outer left, bowl inner left, loop inner left, loop inner right,
# serif left, loop outer right, arm outer right, serif right, tail right.
X_FEATURES = [("bowl_out", None), ("loop_out_l", 530), ("bowl_in", 159), ("loop_in_l", 216), ("loop_in_r", 349),
              ("serif_l", 432), ("loop_out_r", 530), ("serif_r", 600), ("tail_r", 675)]
# y features: loop top, loop counter top, loop counter tip, serif top, serif bottom, lower counter top,
# lower counter bottom, tail top, baseline.
Y_FEATURES = [716, 646, 417, 395, 320, 308, 55, 66, 0, -16]


def shrink(p, dx, dy):
    """Shrink a closed contour by dx, dy (elliptical pen), via the stroker."""
    k = dy / dx
    q = o.tx(p, a=k)
    s = pathops.Path()
    q.draw(s.getPen())
    s.stroke(2 * dy, pathops.LineCap.BUTT_CAP, pathops.LineJoin.MITER_JOIN, 3)
    r = o.diff(o.simplify(q), s)
    return o.tx(r, a=1 / k)


# The 16 px master, drawn on the pixel grid (1 unit = 1 px, y down, 15 x 16 px). It was drawn over
# a_small_geometry() scaled to 16 px, so its proportions are the Lora-derived outline's; every
# horizontal and vertical edge sits on a whole pixel, hairlines are 2 px, the bowl stem 3 px,
# the diagonal 2.6 px measured square to its direction, the upper counter 3 px wide.
A16_OUTER = ("M4 0H7.5C9.1 0 10 1.1 10 2.6V4.4C10 5.7 8.6 6.7 6.5 7.5"   # loop top and right side, into the notch corner
             "L10.3 11.3"                                                 # diagonal, upper edge, to the notch floor
             "C10.1 11.1 10 10.8 10 10.3V10C10 9.4 9.6 9 9 9"             # arm, inner edge, into the serif
             "V7H13V9H12V11.8"                                            # serif and the arm's outer edge
             "C12 12.9 13.2 13.8 15 14V16H11.7"                           # tail top, terminal and foot
             "L10 14.6C9.3 15.5 8.3 16 7.2 16H4.4"                        # the V between tail and bowl, bowl bottom
             "C1.7 16 0 14.5 0 12.4V11.2C0 9.5 1.2 8.3 3.1 7.5"            # bowl, left side, up to the waist
             "C2.4 6.8 2 6 2 5V3C2 1.2 2.8 0 4 0Z")                       # loop, left side
A16_UPPER = "M5.5 2C4.6 2 4 2.6 4 3.5V4.5C4 5.4 4.6 6.2 5.3 6.8C6.2 6.1 7 5.3 7 4.3V3.5C7 2.6 6.4 2 5.5 2Z"
A16_LOWER = "M4.2 8.9L8.8 13.4C8.2 13.8 7.4 14 6.6 14H4.6C3.6 14 3 13.4 3 12.4V10.6C3 9.9 3.4 9.3 4.2 8.9Z"


def a16():
    p = o.path_from_d(A16_OUTER)
    p = o.diff(p, o.path_from_d(A16_UPPER))
    p = o.diff(p, o.path_from_d(A16_LOWER))
    return o.simplify(p)


def export():
    DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    # display tune as a freestanding symbol, wordmark units, origin at the ink top-left
    disp = a_display()
    b = o.bounds(disp)
    sym = o.tx(disp, a=S, d=-S, e=-b[0] * S, f=b[3] * S)
    sb = o.bounds(sym)
    vb = [0, 0, round(sb[2], 2), round(sb[3], 2)]
    o.write_svg(DIR / "20261021_Amp-A-Display-Tune.svg", vb,
                f'<path id="amp-a" fill="currentColor" d="{o.d_from_path(sym)}"/>', "Ampersand option A, display tune (proposal, Phase 1)")
    out["display"] = {"viewBox": vb, "cap_offset_units": round(b[3] * S - CAP_FONT * S, 2)}
    small = a_small_geometry()
    b = o.bounds(small)
    sym = o.tx(small, a=S, d=-S, e=-b[0] * S, f=b[3] * S)
    sb = o.bounds(sym)
    vb = [0, 0, round(sb[2], 2), round(sb[3], 2)]
    o.write_svg(DIR / "20261021_Amp-A-Small-Master-Geometry.svg", vb,
                f'<path id="amp-a-small" fill="currentColor" d="{o.d_from_path(sym)}"/>', "Ampersand option A, small master before pixel fit (proposal, Phase 1)")
    out["small_geometry"] = {"viewBox": vb}
    q = a16()
    o.write_svg(DIR / "20261021_Amp-A-Small-Master-16px.svg", [0, 0, 15, 16],
                f'<path id="amp-a-16" fill="currentColor" d="{o.d_from_path(q, 2)}"/>', "Ampersand option A, 16 px master on the pixel grid (proposal, Phase 1)")
    out["small_16"] = {"viewBox": [0, 0, 15, 16], "ink": [round(v, 3) for v in o.bounds(q)]}
    return out


if __name__ == "__main__":
    print(json.dumps(export(), indent=1)[:3000])
