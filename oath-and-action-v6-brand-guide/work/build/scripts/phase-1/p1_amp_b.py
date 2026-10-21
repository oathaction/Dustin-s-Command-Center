"""Item 5. Ampersand option B: a drawn ampersand for Oath & Action.

It keeps the serif ampersand's silhouette (loop over bowl, a diagonal that crosses to a tail, an
arm with a serif) and makes four decisions of its own:

  contrast   one broad-nib axis at 20 degrees, thick strokes at 0.9 of the wordmark stem, hairlines
             at 2 px when the glyph is 16 px tall, so the red holds its edge at small sizes
  terminals  the arm ends in a flat cut with a short bracketed serif; the tail runs out flat and
             stops with a vertical cut, its foot on the baseline like the letters' feet
  crossing   the diagonal crosses the arm square to it, and both strokes thin by 12 percent at
             the crossing so the two counters' corners stay open at 16 px
  counters   a wider loop counter and a fuller bowl than the Lora glyph

Drawn as one pen path that crosses itself twice, as an ampersand is written: down the arm, round
the bowl, up through the waist into the loop, over the top, back down through the waist and out
along the diagonal to the tail. Outlines are fitted as cubic Beziers with nodes on extrema.

Units inside: cap height 700, baseline 0, y up. Exported in wordmark units (cap 100, y down).

Run: python3 -I p1_amp_b.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
import oa_stroke as st  # noqa: E402
from shapely.geometry import box, Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

DIR = o.OUT / "05-amp-b"
CAP = 700.0
K = 100 / CAP  # to wordmark units

# Pen path: (x, y, direction of travel in degrees, width multiplier[, tension])
PEN = [
    (566, 384, -92, 0.66),        # arm, just below the terminal cut (a hairline, as in the serif ampersand)
    (556, 268, -104, 0.66),       # arm, down to the crossing
    (498, 152, -134, 0.70),       # crossing with the diagonal (thinned: ink trap)
    (404, 62, -160, 0.80),        # bowl, bottom right
    (282, 36, 180, 1.00),         # bowl, bottom
    (94, 190, 90, 0.97),          # bowl, left side
    (180, 322, 30, 0.92),         # bowl, top left, turning into the waist
    (272, 382, 34, 0.74),         # waist, going up (thinned so the waist stays short)
    (404, 556, 90, 0.80),         # loop, right side
    (292, 662, 180, 0.95),        # loop, top
    (172, 566, -94, 0.80),        # loop, left side
    (272, 382, -56, 0.76),        # waist, going down
    (412, 250, -46, 0.95),        # diagonal
    (498, 152, -44, 0.90),        # crossing (thinned: ink trap)
    (582, 66, -22, 0.90),         # tail, turning flat
    (684, 44, 4, 0.96),           # tail end, before the cut: a slight upward flick
]
NIB, THIN, THICK, POWER = 20.0, 86.0, 140.0, 1.4
ARM_CUT_Y = 392.0       # flat cut at the top of the arm
TAIL_CUT_X = 672.0      # vertical cut at the end of the tail
OVERSHOOT = 10.0        # rounds overshoot the cap line and baseline by 10 units (1.43 percent)


def guide():
    """The stroke-model construction guide (a single pen path), as a shapely polygon."""
    s = st.Stroke(PEN, nib_angle=NIB, thin=THIN, thick=THICK, power=POWER, samples=240)
    g = s.polygon(ext0=60, ext1=40)
    g = g.difference(box(490, ARM_CUT_Y, 760, ARM_CUT_Y + 120))  # arm: flat cut, kept clear of the loop
    g = g.difference(box(TAIL_CUT_X, -200, 900, 200))     # tail: vertical cut
    g = g.difference(box(520, -400, 900, 0))               # tail foot sits on the baseline
    g = unary_union([g, serif_shape()])
    return st.clean(g, 4.0), s


# The drawn master: three contours drawn over the guide, font units, y up, cap 700, baseline 0.
# Nodes sit on extrema with level handles, corners are deliberate (waist, notch, V, terminals).
B_OUTER = (
    "M306 710"
    "C205 710 117 642 117 555"            # loop, top to left side
    "C117 490 152 440 195 395"            # loop, left side down to the waist
    "C128 352 28 290 28 182"              # bowl, upper left to left side
    "C28 64 128 -12 258 -12"              # bowl, left side to bottom
    "C352 -12 430 20 482 72"              # bowl, bottom to the V under the crossing
    "C514 34 552 0 604 0"                 # tail, underside
    "L668 0L668 82"                       # tail, foot on the baseline and vertical cut
    "C626 84 588 112 566 178"             # tail, top edge into the arm
    "C578 222 606 268 606 330"            # arm, outer edge
    "L606 392L470 392L470 330"            # flat cut and the beak serif
    "L506 330C514 330 518 318 518 300"    # beak underside, bracket into the arm
    "C518 274 512 254 503 240"            # arm, inner edge, to the notch floor
    "L345 382"                            # diagonal, upper edge, to the loop
    "C404 424 458 486 458 560"            # loop, right side
    "C458 648 392 710 306 710Z"           # loop, right side to top
)
B_UPPER = "M276 620C246 620 224 596 224 566C224 520 262 468 296 426C330 470 352 506 352 542C352 590 318 620 276 620Z"
B_LOWER = "M245 318L428 122C398 98 356 86 302 86C216 86 157 132 157 202C157 254 194 292 245 318Z"


def glyph(weight=(7.0, 3.0)):
    """The drawn outline, then a light elliptical embolden (7 units across, 3 up and down) so the
    thick strokes reach 0.85 of the wordmark stem, and a vertical warp that puts the foot back on
    the baseline and keeps the drawn overshoots."""
    import p1_amp_a as A
    p = o.path_from_d(B_OUTER)
    p = o.diff(p, o.path_from_d(B_UPPER))
    p = o.diff(p, o.path_from_d(B_LOWER))
    p = o.simplify(p)
    if weight:
        dx, dy = weight
        b0 = o.bounds(p)
        p = A.ell_embolden(p, dx, dy)
        b1 = o.bounds(p)
        p = A.ywarp(p, [(b1[1], b0[1]), (-dy, 0.0), (b1[3], b0[3])])
        p = refit(o.simplify(p))
    return p


def refit(p, err=0.6):
    """Refit an outline as clean cubic Beziers with nodes on extrema and corners (the stroker that
    adds weight leaves many short quadratic segments)."""
    from shapely.geometry import Polygon
    rings = [Polygon(r) for r in o.polyline(p, steps=48)]
    rings.sort(key=lambda g: -g.area)
    outer, holes = rings[0], [r for r in rings[1:] if rings[0].contains(r.representative_point())]
    geom = Polygon(outer.exterior.coords, [h.exterior.coords for h in holes])
    d = st.geom_to_d(geom, err=err, nd=2, step=2.0, corner_deg=30.0)
    return o.simplify(o.path_from_d(d))


def serif_shape():
    """The arm's terminal: a flat cut and a short slab that reaches left, toward the loop, as a beak."""
    t = 64.0
    return box(470.0, ARM_CUT_Y - t, 604.0, ARM_CUT_Y)


def fit(g):
    def to_wm(p):
        return (p[0] * K, (CAP - p[1]) * K)
    return st.geom_to_d(g, err=1.2, nd=2, transform=to_wm, step=3.0, corner_deg=34.0)


# The 16 px master of option B, drawn on the pixel grid over glyph() scaled to 16 px
# (1 unit = 1 px, y down, 14 x 16 px). Hairlines 2 px, bowl stem 3 px, diagonal 2.6 px square
# to its direction, upper counter 3 px wide, the notch 1.6 px wide under the beak.
B16_OUTER = ("M4.6 0H7.4C9 0 10 1.3 10 3V4C10 5.4 8.9 6.5 7 7.2"         # loop top, right side, into the notch corner
             "L10.6 10.6C10.8 10.4 11 10 11 9.5V9H10V7H13V9.6"             # diagonal to the notch floor, arm, beak, flat cut
             "C13 10.5 12.4 11.2 12 11.8C12.6 13.2 13.2 13.9 14 14V16H12.8"  # arm outer edge, tail top, vertical cut, foot
             "C11.6 16 10.7 15.2 10 14.4C9 15.5 7.6 16 5.6 16H4.4"          # tail underside, the V, bowl bottom
             "C1.8 16 0 14.4 0 12.2V11.4C0 9.4 1.5 8 3.5 7"                  # bowl left side up to the waist
             "C2.6 6.2 2 5 2 3.6V3C2 1.2 3.1 0 4.6 0Z")                      # loop left side
B16_UPPER = "M5.5 2C4.6 2 4 2.6 4 3.5V4C4 4.9 4.9 5.8 5.9 6.6C6.6 5.8 7 5 7 4V3.4C7 2.6 6.4 2 5.5 2Z"
B16_LOWER = "M4.8 8.7L8.9 13C8.4 13.7 7.4 14 6.4 14H4.6C3.6 14 3 13.2 3 12.2V10.8C3 9.8 3.7 9.1 4.8 8.7Z"


def b16():
    p = o.path_from_d(B16_OUTER)
    p = o.diff(p, o.path_from_d(B16_UPPER))
    p = o.diff(p, o.path_from_d(B16_LOWER))
    return o.simplify(p)


def narrow(p_font, s=0.85):
    """Option B narrowed for a condensed wordmark: scale x by s, then give the vertical strokes
    back the weight the scale took (a horizontal-only embolden of 140 x (1 - s) / 2)."""
    import p1_amp_a as A
    q = o.tx(p_font, a=s)
    return o.simplify(A.ell_embolden(q, 140 * (1 - s) / 2, 2.0))


def to_symbol(p_font, x_shift=0.0):
    """Font units (y up, cap 700) to wordmark units (y down, cap line at 0, baseline at 100)."""
    return o.tx(p_font, a=K, d=-K, e=-x_shift * K, f=CAP * K)


def export():
    DIR.mkdir(parents=True, exist_ok=True)
    g = glyph()
    b = o.bounds(g)
    q = to_symbol(g, b[0])
    qb = o.bounds(q)
    vb = [0, round(qb[1], 2), round(qb[2], 2), round(qb[3] - qb[1], 2)]
    o.write_svg(DIR / "20261021_Amp-B-Drawn-Master.svg", vb,
                f'<path id="amp-b" fill="currentColor" d="{o.d_from_path(q)}"/>', "Ampersand option B, drawn master (proposal, Phase 1)")
    q16 = b16()
    o.write_svg(DIR / "20261021_Amp-B-Small-Master-16px.svg", [0, 0, 14, 16],
                f'<path id="amp-b-16" fill="currentColor" d="{o.d_from_path(q16, 2)}"/>', "Ampersand option B, 16 px master on the pixel grid (proposal, Phase 1)")
    gn = narrow(g)
    bn = o.bounds(gn)
    qn = to_symbol(gn, bn[0])
    qnb = o.bounds(qn)
    o.write_svg(DIR / "20261021_Amp-B-Narrow-For-Condensed.svg", [0, round(qnb[1], 2), round(qnb[2], 2), round(qnb[3] - qnb[1], 2)],
                f'<path id="amp-b-narrow" fill="currentColor" d="{o.d_from_path(qn)}"/>', "Ampersand option B, narrowed to 0.85 for the condensed wordmark (proposal, Phase 1)")
    gd, s = guide()
    gd_d = st.geom_to_d(gd, err=1.2, nd=2, transform=lambda p: ((p[0] - b[0]) * K, (CAP - p[1]) * K), step=3.0, corner_deg=34.0)
    (DIR / "construction.json").write_text(json.dumps({"guide_d": gd_d, "centreline_font_units_y_up": s.centreline_svg(), "offset_x_units": round(b[0], 2)}))
    return {"viewBox": vb, "ink_box": [round(v, 2) for v in qb], "nodes": st.count_nodes(o.d_from_path(q)),
            "overshoot_top_units": round(-qb[1], 2), "below_baseline_units": round(qb[3] - 100, 2)}


if __name__ == "__main__":
    print(json.dumps(export(), indent=1)[:1500])
