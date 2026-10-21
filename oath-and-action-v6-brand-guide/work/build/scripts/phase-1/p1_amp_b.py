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
    (556, 372, -96, 0.90),        # arm, just below the terminal cut
    (548, 262, -104, 0.86),       # arm, down to the crossing
    (488, 142, -138, 0.80),       # crossing with the diagonal (thinned)
    (392, 52, -164, 0.92),        # bowl, bottom right
    (268, 30, 180, 1.00),         # bowl, bottom
    (96, 182, 90, 1.00),          # bowl, left side
    (168, 318, 38, 0.96),         # bowl, top left, turning into the waist
    (262, 392, 42, 0.86),         # waist, going up
    (418, 560, 92, 0.86),         # loop, right side
    (300, 660, 180, 0.94),        # loop, top
    (178, 566, -88, 0.84),        # loop, left side
    (262, 392, -48, 0.90),        # waist, going down
    (400, 248, -46, 1.00),        # diagonal
    (488, 142, -46, 0.84),        # crossing (thinned)
    (568, 62, -26, 0.94),         # tail, turning flat
    (680, 36, 0, 0.90),           # tail end, before the cut
]
NIB, THIN, THICK, POWER = 20.0, 94.0, 160.0, 1.4
ARM_CUT_Y = 392.0       # flat cut at the top of the arm
TAIL_CUT_X = 672.0      # vertical cut at the end of the tail
OVERSHOOT = 10.0        # rounds overshoot the cap line and baseline by 10 units (1.43 percent)


def serif():
    """A short bracketed serif on the arm's flat cut: a slab with curved brackets into the arm."""
    t = 64.0                       # slab thickness, a hairline
    x0, x1 = 470.0, 628.0          # reaches 92 left and 58 right of the arm's centre
    slab = box(x0, ARM_CUT_Y - t, x1, ARM_CUT_Y)
    # brackets: quarter-round fillets under the slab on both sides of the arm
    br = []
    for side, cx in ((-1, 0), (1, 0)):
        pass
    return slab


def glyph(debug=False):
    s = st.Stroke(PEN, nib_angle=NIB, thin=THIN, thick=THICK, power=POWER, samples=160)
    g = s.polygon(ext0=60, ext1=40)
    # terminal planes
    g = g.difference(box(490, ARM_CUT_Y, 760, ARM_CUT_Y + 120))  # arm: flat cut, kept clear of the loop
    g = g.difference(box(TAIL_CUT_X, -200, 900, 200))     # tail: vertical cut
    g = g.difference(box(520, -400, 900, 0))               # tail foot sits on the baseline
    g = unary_union([g, serif_shape()])
    g = st.clean(g, 0.8)
    return g, s


def serif_shape():
    t = 66.0
    x0, x1 = 474.0, 630.0
    slab = box(x0, ARM_CUT_Y - t, x1, ARM_CUT_Y)
    # bracket fillets: the area under the slab between the arm and a quarter circle
    import shapely.geometry as sg
    fill = []
    r = 30.0
    for (cx, sign) in ((508.0 - r, -1), (604.0 + r, 1)):
        # quarter circle centred below the slab, tangent to the slab underside and the arm side
        cy = ARM_CUT_Y - t - r
        sq = box(min(cx, cx - sign * r), cy, max(cx, cx - sign * r), cy + r)
        circ = sg.Point(cx, cy).buffer(r, resolution=32)
        fill.append(sq.difference(circ))
    return unary_union([slab] + fill)


def fit(g):
    def to_wm(p):
        return (p[0] * K, (CAP - p[1]) * K)
    return st.geom_to_d(g, err=0.7, nd=2, transform=to_wm, step=2.0)


def export():
    DIR.mkdir(parents=True, exist_ok=True)
    g, s = glyph()
    d = fit(g)
    p = o.simplify(o.path_from_d(d))
    b = o.bounds(p)
    # origin at the ink's left edge, cap line at y = 0 kept as the reference
    q = o.tx(p, e=-b[0])
    qb = o.bounds(q)
    vb = [0, round(qb[1], 2), round(qb[2], 2), round(qb[3] - qb[1], 2)]
    o.write_svg(DIR / "20261021_Amp-B-Drawn-Master.svg", vb,
                f'<path id="amp-b" fill="currentColor" d="{o.d_from_path(q)}"/>', "Ampersand option B, drawn master (proposal, Phase 1)")
    info = {"viewBox": vb, "nodes": st.count_nodes(o.d_from_path(q)), "ink_box": [round(v, 2) for v in qb],
            "overshoot_top_units": round(-qb[1], 2), "below_baseline_units": round(qb[3] - 100, 2),
            "pen": PEN, "nib": NIB, "thin": THIN, "thick": THICK}
    # construction drawing: centreline over outline, for the board
    cl = s.centreline_svg()
    (DIR / "construction.json").write_text(json.dumps({"centreline_font_units_y_up": cl, "offset_x_units": round(b[0], 2)}))
    return info


if __name__ == "__main__":
    print(json.dumps(export(), indent=1)[:1500])
