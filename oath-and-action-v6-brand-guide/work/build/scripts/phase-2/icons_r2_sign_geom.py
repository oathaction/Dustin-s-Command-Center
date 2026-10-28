"""Bar geometry for Concept 3, Public sign (design director, Phase 2 round two, October 28, 2026).

Every pictogram is built from one bar: 3 units wide with round ends in the display master
(3 px at 24 px, 2 px at 16 px), on the shared 24-unit grid with 2-unit padding. Lines run at 0,
45 and 90 degrees; curves are circles. Where a bar turns, the outer corner takes the bar's own
round (radius 1.5) and the inner corner stays sharp, which is what a round join gives.

Shapes are skia-pathops paths through round one's helpers (icons_geom.py and the Phase 1
symbols_geom.py), imported and never changed.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parent / "phase-1"
for _p in (str(HERE), str(P1)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
if "/root/.local/lib/python3.13/site-packages" not in sys.path:
    sys.path.append("/root/.local/lib/python3.13/site-packages")

import icons_geom as g  # noqa: E402  (round one, read only)
from icons_geom import circle, d_of, intersect, minus, poly, rect, rrect, union  # noqa: E402,F401
from symbols_geom import stroke_path  # noqa: E402

BAR = 3.0          # bar width in the display master, in units
END = BAR / 2      # round end radius
HEAD = 4.5         # figure head diameter (1.5 bars)
NODE = 4.5         # pillar node diameter (1.5 bars)
GAP = 1.5          # the family's one gap: head to body, part to part, ink to red
S2 = math.sqrt(2)


def bar(*pts, w=BAR, closed=False):
    """A polyline drawn as a bar with round ends and round joins."""
    segs = [("M", *pts[0])] + [("L", *p) for p in pts[1:]]
    if closed:
        segs.append(("Z",))
    return stroke_path(segs, w, "round", "round")


def arc(cx, cy, r, a0, a1, w=BAR):
    """An arc of a circle drawn as a bar with round ends. Angles in degrees, screen coordinates,
    clockwise positive, 0 at three o'clock."""
    return stroke_path([("A", cx, cy, r, a0, a1)], w, "round", "round")


def path(segs, w=BAR):
    """Mixed straight and arc segments as one bar: ("M", x, y), ("L", x, y), ("A", cx, cy, r, a0, a1)."""
    return stroke_path(segs, w, "round", "round")


def disc(cx, cy, d):
    return circle(cx, cy, d / 2)


def solid(pts, r=END):
    """A solid polygon whose convex corners take the bar's round."""
    return g.fillet_poly(pts, r) if r > 0 else poly(*pts)


def box(x, y, w, h, r=END):
    return rrect(x, y, w, h, r)


def on_arc(cx, cy, r, a):
    t = math.radians(a)
    return cx + r * math.cos(t), cy + r * math.sin(t)


def chevron(tip, direction, arm, w=BAR):
    """An open arrowhead at bar width: two arms of centerline length `arm` meeting at `tip` at 90
    degrees, symmetric about `direction` (degrees, the way the arrow points)."""
    a = math.radians(direction)
    ux, uy = math.cos(a), math.sin(a)
    # arms go back at 45 degrees either side of the direction
    p1 = (tip[0] - arm * (ux * math.cos(math.pi / 4) - uy * math.sin(math.pi / 4)),
          tip[1] - arm * (uy * math.cos(math.pi / 4) + ux * math.sin(math.pi / 4)))
    p2 = (tip[0] - arm * (ux * math.cos(math.pi / 4) + uy * math.sin(math.pi / 4)),
          tip[1] - arm * (uy * math.cos(math.pi / 4) - ux * math.sin(math.pi / 4)))
    return bar(p1, tip, p2, w=w)


def area(p):
    return g.area(p)


def empty():
    return g.empty()
