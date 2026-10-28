"""Concept 3, Public sign: stage 2 masters (design director, Phase 2 round two, October 28, 2026).

Oath & Action's subjects drawn in the tradition of public information symbols. People and objects
are built from one bar on the shared 24-unit grid, with lines at 0, 45 and 90 degrees and curves
taken from circles. The Charcoal drawing names the subject; one red stroke, the accent, shows what
happens to it.

Family rules, as drawn (stage 2, after the creative director's stage 1 notes):
  bar      3 units in the display master, 3 px at 24 px, 2 px at 16 px; round ends, round joins
  head     a disc 4.5 across (3 px at 16), one gap above the body; no hands, feet, faces or gender cues
  node     a disc 4.5 across on the horizontal center line in the four pillar marks
  gap      1.5 units (1 px at 16): head to body, part to part, ink to red
  red      one stroke or arrowhead at bar width, at most 14 percent of the painted area. Every
           arrowhead has a shaft. Red floats one gap off the ink, and touches ink only where the
           verb acts on the object: the lid's swing, the door's swing, the bridge, the check
  never    red on a figure or a side (Rule 01.1); red alone in the top-right 6 by 6 units, where
           interfaces put badges; straight edges outside the live area 2 to 22 (round forms may
           overshoot 0.25); plus shapes; domes, columns, flags, scales, seals, stars

draw(name) returns the 24-unit display drawing; draw16(name) returns the separate 16-unit
drawing for the 16 px master. Each is {"ink": path, "accent": path}.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_geom as g  # noqa: E402  (round one helpers, read only)
from icons_r2_sign_geom import (BAR, GAP, HEAD, NODE, arc, arrowhead, bar, box, circle, disc,  # noqa: E402,F401
                                empty, intersect, minus, on_arc, path, rect, rot, solid, union)

S2 = math.sqrt(2)
ICONS = ["explain", "track", "connect", "act", "ballot", "bill", "testify", "housing", "money", "loop"]
PILLARS = ["explain", "track", "connect", "act"]
LABELS = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
          "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign money",
          "loop": "Feedback loop"}
FILE_NAME = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
             "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign-Money",
             "loop": "Feedback-Loop"}
CLASS = {"explain": "Pillar mark", "track": "Pillar mark", "connect": "Pillar mark", "act": "Pillar mark",
         "ballot": "Topic symbol", "bill": "Topic symbol", "testify": "Topic symbol", "housing": "Topic symbol",
         "money": "Topic symbol", "loop": "Atlas symbol"}
VERB = {
    "explain": "The lid's swing: the square opens on its hinge so you can see the node inside.",
    "track": "The arrow up the stair: the decision moves to the next stage.",
    "connect": "The bridge across the gap, the ground both halves reach for.",
    "act": "The door's swing, the quarter circle a floor plan draws for a door's path.",
    "ballot": "The check, the stroke a voter makes before the paper goes in.",
    "bill": "The signature line, where a bill becomes law.",
    "testify": "The sound leaving the speaker.",
    "housing": "The door, the way in.",
    "money": "The arrow leaving the note: the money moving on.",
    "loop": "The arrowhead on the return, the feedback that closes the loop.",
}
STORY = {
    "explain": "A square opened on its hinge, so you can see the node inside.",
    "track": "A decision climbing a stair of stages.",
    "connect": "Two halves reaching across a gap, joined at the node.",
    "act": "A door swung open, ready to walk through.",
}


def _arrow(tail, tip, length=4.25, half=3.0):
    """A red public-sign arrow: a bar shaft from `tail` into a solid head whose tip is `tip`."""
    ang = math.degrees(math.atan2(tip[1] - tail[1], tip[0] - tail[0]))
    u = ((tip[0] - tail[0]) / math.dist(tail, tip), (tip[1] - tail[1]) / math.dist(tail, tip))
    base = (tip[0] - u[0] * (length - 0.5), tip[1] - u[1] * (length - 0.5))
    return union(bar(tail, base), arrowhead(tip, ang, length, half))


# ============================================================ display masters, 24-unit grid

def explain():
    """The square, its top-right quarter drawn as an ink bar L lifted on its hinge at the end of
    the top bar and turned up 45 degrees, as a lid opens. The node sits inside the square. The red
    arc is the lid's swing: the path of the lid's free end, from where it stands open to where it
    closes on the square, centered on the hinge. Its square ends lie over the two ink ends, so
    the whole swing shows. The frame sits on half units so its 3 px bars land on whole pixels at
    24 px, which puts the node 0.5 below the center line."""
    h, cx, cy = 5.0, 10.5, 12.5
    H = (cx, cy - h)
    a = h / S2
    body = bar((cx + h, cy), (cx + h, cy + h), (cx - h, cy + h), (cx - h, cy - h), H, (cx + a, cy - h - a), (cx + 2 * a, cy - h))
    ink = union(body, disc(cx, cy, NODE))
    acc = g.sector(H[0], H[1], h * S2 + BAR / 2, h * S2 - BAR / 2, 0, 45)
    return {"ink": ink, "accent": acc}

def track():
    """Three stages on a rising stair, closed by the stair's back. The node is the stage reached,
    a station on the middle nosing (y 12.5, so the bars land on whole pixels). Red: the arrow up
    the stair, a shaft along the stair's line ending in a solid head, set in the open corner."""
    st = bar((3.5, 20.5), (3.5, 17.5), (8.5, 17.5), (8.5, 12.5), (14.5, 12.5), (14.5, 7.5), (20.5, 7.5), (20.5, 20.5))
    node = disc(14.5, 12.5, NODE)
    acc = _arrow((5.5, 9.0), (10.0, 4.5))
    return {"ink": union(st, node), "accent": acc}

def connect():
    """One circle in two halves held apart: two bar arcs with their ends about 4 units apart, each
    reaching inward on its center line with a short spur. The red bridge spans the gap between the
    spurs and the node sits on it. Centered on y 12.5 so the spurs land on whole pixels."""
    r, d, cy = 6.0, 2.75, 12.5
    L = arc(12 - d, cy, r, 95, 265)
    R = arc(12 + d, cy, r, -85, 85)
    xl, xr = 12 - d - r, 12 + d + r
    spurs = union(bar((xl, cy), (6.25, cy)), bar((17.75, cy), (xr, cy)))
    node = disc(12, cy, NODE)
    acc = minus(rect(6.25, cy - BAR / 2, 11.5, BAR), node)
    return {"ink": union(L, R, spurs, node), "accent": acc}

def act():
    """A door swung open: lintel, jamb and floor, with the leaf hinged on the left, its top at 45
    degrees as it turns away. The node is the latch, a station on the jamb at the center line
    where the door meets its frame. Red: the swing, a true quarter circle from the leaf's free
    edge down to the floor, the path a floor plan draws for a door. It stops at the ink."""
    frame = bar((5.5, 4.5), (19.5, 4.5), (19.5, 20.5), (10.5, 20.5))
    lw = 4.0
    leaf = solid([(2.0, 7.5), (2.0 + lw, 7.5 + lw), (2.0 + lw, 22.0), (2.0, 22.0)])
    ink = union(frame, leaf, disc(19.5, 12.0, NODE))
    acc = minus(arc(2.0 + lw, 20.5, 5.0, -90, 0), ink)
    return {"ink": ink, "accent": acc}

def ballot():
    """A ballot box with a slot across its top and a marked paper sinking into it, its lower third
    already in. The paper is solid, so the red check sits on Charcoal at 4.49:1. Red: the check,
    long right arm at 45 degrees, short left arm, 7 units across on an 8-unit paper. The box is low
    and wide, so the ballot's silhouette stays apart from Bill's page."""
    bx = minus(box(3.0, 14.0, 18.0, 7.0), rect(6.5, 13.0, 11.0, 5.0))
    paper = minus(box(8.0, 3.0, 8.0, 15.0, 1.5), rect(0, 18.0, 24, 10))
    acc = bar((10.0, 10.0), (11.25, 11.25), (14.0, 8.5))
    return {"ink": union(bx, paper), "accent": acc}

def bill():
    """A page with a folded corner, a diagonal with its small triangle, and two lines of text of
    different lengths, the first stopping short of the fold. Red: the signature line, set below the
    text where a bill becomes law. The page fills the portrait keyline (16 by 20 units outside), so
    its silhouette stays larger than Explain's square and apart from it."""
    x0, x1, y0, y1, f = 5.5, 18.5, 3.5, 20.5, 3.0
    page = path([("M", x0, y0), ("L", x1 - f, y0), ("L", x1, y0 + f), ("L", x1, y1), ("L", x0, y1), ("Z",)])
    flap = solid([(x1 - f, y0), (x1, y0 + f), (x1 - f, y0 + f)], 0.75)
    lines = union(bar((10.0, 7.5), (11.0, 7.5)), bar((10.0, 12.0), (14.0, 12.0)))
    acc = bar((10.0, 16.5), (12.5, 16.5))
    return {"ink": union(page, flap, lines), "accent": acc}

def testify():
    """A person standing at a lectern: head, body, an arm resting on the lectern's sloped top, and
    a gooseneck microphone rising from the lectern toward the mouth. The person is never red. Red:
    one sound arc ahead of the face, rising above the microphone."""
    head = disc(5.5, 8.5, HEAD)
    body = bar((5.5, 13.75), (5.5, 20.5))
    armp = bar((5.5, 15.0), (8.5, 18.0))
    lect = solid([(10.0, 16.0), (13.0, 13.0), (18.0, 13.0), (18.0, 22.0), (10.0, 22.0)], 1.5)
    mic = bar((15.5, 13.0), (15.5, 12.0), (12.75, 9.25))
    acc = arc(5.5, 8.5, 5.25, -70, -35)
    return {"ink": union(head, body, armp, lect, mic), "accent": acc}

def housing():
    """A house: a pitched roof with a chimney, set one gap above two walls, and a door. Red: the
    door, the way in. As stage 1, moved 0.5 left so the door's 3 px bar lands on whole pixels."""
    roof = bar((3.5, 12.0), (11.5, 4.0), (19.5, 12.0))
    chimney = bar((15.5, 8.0), (15.5, 3.5))
    walls = union(bar((6.5, 13.5), (6.5, 20.5)), bar((16.5, 13.5), (16.5, 20.5)))
    acc = bar((11.5, 18.0), (11.5, 20.5))
    return {"ink": union(roof, chimney, walls), "accent": acc}

def money():
    """A banknote: a wide landscape bar frame, 20 by 10.5 units, with a solid disc at its center.
    Red: an arrow with a shaft leaving the note's upper right edge, the money moving on."""
    note = bar((3.5, 10.5), (20.5, 10.5), (20.5, 18.5), (3.5, 18.5), closed=True)
    dsc = disc(12.0, 14.5, 3.0)
    acc = _arrow((13.0, 8.5), (17.25, 4.25))
    return {"ink": union(note, dsc), "accent": acc}

def loop():
    """Two nodes on one line, joined forward by a straight link with its arrowhead and back by a
    returning arc. The two paths differ, so the loop never maps onto itself under a half turn the
    way reload and sync glyphs do. The return runs over the top: drawn underneath, two nodes over
    a curve read as a face. Red: the return's arrowhead, the feedback that closes the loop."""
    nd, y = 5.25, 12.5
    A, B = (4.5, y), (19.5, y)
    a = disc(*A, nd)
    b = disc(*B, nd)
    tipF = (B[0] - nd / 2 - GAP, y)
    fwd = union(bar((A[0] + nd / 2 + GAP + BAR / 2, y), (tipF[0] - 3.75, y)), arrowhead(tipF, 0, 4.25, 3.0))
    cy, r = y + 0.5, math.hypot(7.5, 0.5)
    off = math.degrees(math.atan2(0.5, 7.5))
    start = 360 - off - math.degrees((nd / 2 + GAP + BAR / 2) / r)
    tip_ang = 180 + off + math.degrees((nd / 2 + GAP) / r)
    ret = arc(12, cy, r, tip_ang + 22, start)
    acc = arrowhead(on_arc(12, cy, r, tip_ang), tip_ang - 90 - 10, 4.25, 3.0)
    return {"ink": union(a, b, fwd, ret), "accent": acc}


DRAW = {n: globals()[n] for n in ICONS}


def draw(name):
    return DRAW[name]()


def display(name):
    """The display master for 48 px and up: the 24-unit drawing, unhinted."""
    return DRAW[name]()


# ============================================================ 24 px hand-hinted drawings
# Most 24 px masters are the display drawing fitted to whole pixels. Two are drawn on the pixel
# grid instead, because the fit turns their small solids into shapes the drawing does not mean:
#   loop   the fitted arrowheads become a diamond and a red block; the forward head is drawn as a
#          stepped pixel triangle (7, 5, 3, 1 px) and the red return head as a 45 degree pixel
#          triangle with its right angle at the tip, pointing down and left at node A
#   bill   the text bars take square ends (as the red line already does in the masters module)
#   money  the 3-unit disc on a whole-pixel center fits as a lopsided blob, and a 2, 4, 2 px
#          oval reads as a plus; it is drawn as a 4 by 3 px block on the note's center
# Units are pixels; the fitter keeps these shapes as drawn.

def _px(*cells):
    return union(*[rect(x, y, 1, 1) for x, y in cells])


def loop24():
    nodes = union(disc(4.5, 12.5, 5.25), disc(19.5, 12.5, 5.25))
    head = union(*[rect(12 + i, 12 - (3 - i), 1, 2 * (3 - i) + 1) for i in range(4)])
    fwd = union(rect(8, 11, 4, 3), head)
    ret = g.sector(12, 13.0, 9.0, 6.0, 236, 314)
    acc = _px(*[(6 + i, 8 - j) for i in range(4) for j in range(4 - i)])
    return {"ink": union(nodes, fwd, ret), "accent": acc}


def money24():
    d = money()
    ink = union(minus(d["ink"], rect(8, 12, 8, 5)), rect(10, 13, 4, 3))
    return {"ink": ink, "accent": d["accent"]}


def bill24():
    """Bill's text bars take square ends, the way its red line does, so the short bar fits as a
    4 by 3 px block and never as a blob with a nub."""
    x0, x1, y0, y1, f = 5.5, 18.5, 3.5, 20.5, 3.0
    page = path([("M", x0, y0), ("L", x1 - f, y0), ("L", x1, y0 + f), ("L", x1, y1), ("L", x0, y1), ("Z",)])
    flap = solid([(x1 - f, y0), (x1, y0 + f), (x1 - f, y0 + f)], 0.75)
    lines = union(rect(8.5, 6.0, 4.0, 3.0), rect(8.5, 10.5, 7.0, 3.0))
    return {"ink": union(page, flap, lines), "accent": bill()["accent"]}


DRAW24 = {"loop": loop24, "money": money24, "bill": bill24}


def draw24(name):
    """The drawing the 24 px master is fitted from: the display drawing, or a pixel-grid drawing."""
    return DRAW24[name]() if name in DRAW24 else DRAW[name]()


# ============================================================ 16 px masters, 16-unit grid
# Separate drawings on the 16 px grid, 1-unit padding, live area 1 to 15. Bars are 2 px on
# whole-pixel centerlines, so their edges land on pixel boundaries; discs are 3 px on half-pixel
# centers or 4 px on whole-pixel centers; the gap is 1 px. Short red strokes take square ends
# (butt=True), since a round end hinted to whole pixels turns a short bar into a plus.

B16 = 2.0


def _bar16(*pts, butt=False):
    from icons_r2_sign_geom import stroke_path
    if butt:
        segs = [("M", *pts[0])] + [("L", *p) for p in pts[1:]]
        return stroke_path(segs, B16, "butt", "miter")
    return bar(*pts, w=B16)


def _arc16(cx, cy, r, a0, a1):
    return arc(cx, cy, r, a0, a1, w=B16)


def explain16():
    H = (7.0, 5.0)
    a = 4.0 / S2
    body = _bar16((11.0, 9.0), (11.0, 13.0), (3.0, 13.0), (3.0, 5.0), H, (H[0] + a, H[1] - a), (H[0] + 2 * a, H[1]))
    ink = union(body, disc(7.0, 9.0, 4.0))
    # At 16 px the swing stops short of the frame's corner: the full arc closes the lid, the red and
    # the frame into one block the size of Bill's page (similarity 0.69); the shorter swing floats
    # a pixel off the frame and reads as the start of the lid's path (0.57).
    acc = g.sector(H[0], H[1], 4.0 * S2 + 1.0, 4.0 * S2 - 1.0, 0, 21)
    return {"ink": ink, "accent": acc}

def track16():
    st = _bar16((2.0, 14.0), (2.0, 12.0), (6.0, 12.0), (6.0, 8.0), (10.0, 8.0), (10.0, 4.0), (14.0, 4.0), (14.0, 14.0))
    ink = union(st, disc(10.0, 8.0, 4.0))
    tip = (7.0, 2.0)
    acc = union(_bar16((3.0, 6.0), (5.25, 3.75)), arrowhead(tip, -45, 3.0, 2.0, 0.4))
    return {"ink": ink, "accent": acc}


def connect16():
    L = _arc16(6.0, 8.0, 4.0, 95, 265)
    R = _arc16(10.0, 8.0, 4.0, -85, 85)
    spurs = union(_bar16((2.0, 8.0), (4.0, 8.0), butt=True), _bar16((12.0, 8.0), (14.0, 8.0), butt=True))
    node = disc(8.0, 8.0, 4.0)
    acc = minus(rect(4.0, 7.0, 8.0, 2.0), node)
    return {"ink": union(L, R, spurs, node), "accent": acc}


def act16():
    frame = _bar16((4.0, 3.0), (13.0, 3.0), (13.0, 14.0), (7.0, 14.0))
    leaf = solid([(1.0, 5.0), (4.0, 8.0), (4.0, 15.0), (1.0, 15.0)], 0.75)
    ink = union(frame, leaf, disc(13.0, 8.0, 4.0))
    acc = g.sector(4.0, 14.0, 4.0, 2.0, -90, 0)
    return {"ink": ink, "accent": acc}


def ballot16():
    # The display master's proportions: a low wide box and a narrow paper, its lower part in the box.
    bx = minus(box(1.0, 10.0, 14.0, 5.0, 1.0), rect(3.0, 9.0, 10.0, 4.0))
    paper = minus(box(5.0, 1.0, 6.0, 11.0, 1.0), rect(0, 12.0, 16, 4))
    acc = _bar16((6.0, 5.5), (7.0, 6.5), (9.5, 4.0))
    return {"ink": union(bx, paper), "accent": acc}


def bill16():
    page = path([("M", 4.0, 2.0), ("L", 10.0, 2.0), ("L", 12.0, 4.0), ("L", 12.0, 14.0), ("L", 4.0, 14.0), ("Z",)], w=B16)
    flap = solid([(10.0, 2.0), (12.0, 4.0), (10.0, 4.0)], 0.3)
    lines = union(rect(6.0, 4.0, 2.0, 2.0), rect(6.0, 7.0, 4.0, 2.0))
    acc = rect(6.0, 10.0, 3.0, 2.0)
    return {"ink": union(page, flap, lines), "accent": acc}

def testify16():
    head = disc(4.0, 6.0, 4.0)
    body = _bar16((4.0, 10.0), (4.0, 14.0))
    lect = solid([(7.0, 11.0), (9.0, 9.0), (13.0, 9.0), (13.0, 15.0), (7.0, 15.0)], 0.75)
    mic = _bar16((11.0, 9.0), (11.0, 8.0), (9.0, 6.0))
    acc = _arc16(4.0, 6.0, 4.0, -75, -40)
    return {"ink": union(head, body, lect, mic), "accent": acc}


def housing16():
    roof = _bar16((2.0, 8.0), (8.0, 2.0), (14.0, 8.0))
    chimney = _bar16((11.0, 5.0), (11.0, 2.0))
    walls = union(_bar16((4.0, 10.0), (4.0, 14.0)), _bar16((12.0, 10.0), (12.0, 14.0)))
    acc = rect(7.0, 11.0, 2.0, 4.0)
    return {"ink": union(roof, chimney, walls), "accent": acc}


def money16():
    note = path([("M", 2.0, 7.0), ("L", 14.0, 7.0), ("L", 14.0, 13.0), ("L", 2.0, 13.0), ("Z",)], w=B16)
    dsc = disc(8.0, 10.0, 2.0)
    acc = union(_bar16((8.75, 4.75), (9.25, 4.25)), arrowhead((11.0, 2.5), -45, 3.0, 2.0, 0.4))
    return {"ink": union(note, dsc), "accent": acc}

def loop16():
    # Drawn on the pixel grid. At 16 px the forward link drops its arrowhead (a 4 px head beside
    # 4 px nodes fits as a third plus) and keeps the straight bar, so the loop still differs
    # under a half turn; the return arc and its red head pointing down at node A carry the verb.
    nodes = union(disc(3.0, 10.0, 4.0), disc(13.0, 10.0, 4.0))
    link = rect(6, 9, 4, 2)
    ret = g.sector(8, 10.5, 6.5, 4.5, 245, 315)
    acc = _px(*[(3 + i, 6 - j) for i in range(3) for j in range(3 - i)])
    return {"ink": union(nodes, link, ret), "accent": acc}


DRAW16 = {n: globals()[n + "16"] for n in ICONS}


def draw16(name):
    return DRAW16[name]()
