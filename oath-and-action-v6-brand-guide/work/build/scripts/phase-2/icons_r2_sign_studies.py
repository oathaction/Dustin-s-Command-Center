"""Concept 3, Public sign, stage 2: studies shown on the board beside the masters. Not masters.

  explain_open90   Explain with the lid opened 90 degrees on its hinge, so the red swing of the lid's
                   free end is a true quarter circle. The creative director's note 1 asks for a lid
                   "turned up 45 degrees" and a swing that "runs long enough to read as a quarter
                   circle"; a lid turned 45 degrees travels 45 degrees, so the two cannot both hold.
                   The master keeps the 45 degree lid; this study shows the other reading.
  loop_arc_below   Feedback loop as the stage 1 note words it: the return arc below the nodes.
                   The master runs the return over the top, because two nodes over a curve below
                   read as a face.

Each returns {"ink": path, "accent": path} on the 24-unit grid.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_geom as g  # noqa: E402  (round one helpers, read only)
from icons_r2_sign_geom import BAR, GAP, NODE, arc, arrowhead, bar, disc, on_arc, union  # noqa: E402

S2 = math.sqrt(2)


def explain_open90():
    """Square 9 units on centerlines, hinge at the top bar's middle; the quarter L stands upright
    above it. Red: the free end's path, 90 degrees around the hinge, radius h times root 2."""
    h, cx, cy = 4.5, 10.5, 14.0
    H = (cx, cy - h)
    body = bar((cx + h, cy), (cx + h, cy + h), (cx - h, cy + h), (cx - h, cy - h), H, (cx, cy - 2 * h), (cx + h, cy - 2 * h))
    ink = union(body, disc(cx, cy, NODE))
    acc = g.sector(H[0], H[1], h * S2 + BAR / 2, h * S2 - BAR / 2, -45, 45)
    return {"ink": ink, "accent": acc}


def loop_arc_below():
    """The master's loop turned over: forward link on the center line, return arc below with its red
    head arriving at node A."""
    nd, y = 5.25, 11.5
    A, B = (4.5, y), (19.5, y)
    a, b = disc(*A, nd), disc(*B, nd)
    tipF = (B[0] - nd / 2 - GAP, y)
    fwd = union(bar((A[0] + nd / 2 + GAP + BAR / 2, y), (tipF[0] - 3.75, y)), arrowhead(tipF, 0, 4.25, 3.0))
    cy, r = y - 0.5, math.hypot(7.5, 0.5)
    off = math.degrees(math.atan2(0.5, 7.5))
    start = off + math.degrees((nd / 2 + GAP + BAR / 2) / r)
    tip_ang = 180 - off - math.degrees((nd / 2 + GAP) / r)
    ret = arc(12, cy, r, start, tip_ang - 22)
    acc = arrowhead(on_arc(12, cy, r, tip_ang), tip_ang + 90 + 10, 4.25, 3.0)
    return {"ink": union(a, b, fwd, ret), "accent": acc}


STUDIES = {"explain_open90": explain_open90, "loop_arc_below": loop_arc_below}
