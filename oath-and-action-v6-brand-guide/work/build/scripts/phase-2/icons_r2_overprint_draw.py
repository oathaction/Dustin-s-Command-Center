"""Concept 1, Overprint: the ten round-two test icons as display masters (design director, Phase 2,
round two, October 28, 2026).

Idea. A fine Charcoal line drawing printed over one solid Pillar Red plane set off register, the way
a second ink lands on a newspaper page. The red sits under the part of the subject the story is
about. The line drawing is whole without it.

Grid. Round one's 24-unit grid (icons_draw.py): 2-unit padding, live area 2 to 22; keylines circle 20,
square 18, portrait 16 by 20, landscape 20 by 16. Every drawing here is written as center lines.

Display master (48 px and up). Center lines stroked at 1.5 units with round caps and round joins.
Rectangles take a 2-unit outer radius, so a center-line radius of 1.25. The pillar marks carry the
node as a solid ink disc 3 units across.

The red plane. One solid primitive (disc, rounded square, quarter disc or stadium). Each icon names
where the plane would sit in register, under the subject's focus; the plane then prints at one
fixed offset, OFFSET, toward the lower left. The offset is the same in every icon.

Every drawing returns layers:
  ink     the line drawing and any ink nodes, as one filled outline
  accent  the red plane, already moved by OFFSET
  lines   the center-line paths (for the board's construction views)
  reg     the red plane in register, before the offset (construction only)
Run with python3 -I. Imports round one's shared helpers and changes none of them.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_geom as g  # noqa: E402  (round one, shared; imported, never changed)
import pathops as po  # noqa: E402
from icons_geom import circle, intersect, minus, poly, rect, rrect, union  # noqa: E402

ICONS = ["explain", "track", "connect", "act", "ballot", "bill", "testify", "housing", "money", "loop"]
LABELS = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
          "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign money",
          "loop": "Feedback loop"}
FILE_NAME = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
             "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign-Money",
             "loop": "Feedback-Loop"}
CLASS = {"explain": "Pillar mark", "track": "Pillar mark", "connect": "Pillar mark", "act": "Pillar mark",
         "ballot": "Topic symbol", "bill": "Topic symbol", "testify": "Topic symbol", "housing": "Topic symbol",
         "money": "Topic symbol", "loop": "Atlas symbol"}
# One line per icon: why its red sits where it does. The drawing has to show this without the caption.
REASON = {
    "explain": "Red fills the lifted corner and falls into the opening, the inside you now get to see.",
    "track": "Red sits under the top stage, where the decision is headed.",
    "connect": "Red is the ground in the gap where the two halves meet.",
    "act": "Red is the light falling through the open door.",
    "ballot": "Red is the filled oval, the mark a voter makes.",
    "bill": "Red highlights the one line of the bill the story is about.",
    "testify": "Red sits behind the microphone, where a voice goes on the record.",
    "housing": "Red fills the doorway, the way into a home.",
    "money": "Red is the coin, the money passing from the hand.",
    "loop": "Red sits under the node where a reform acts on the loop.",
}

W = 1.5                  # display stroke, in grid units
R_RECT = 1.25            # center-line corner radius for rectangles (2-unit outer radius)
NODE_R = 1.5             # pillar-mark node, a solid ink disc 3 units across
OFFSET = (-2.0, 2.0)     # the red plane's fixed off-register shift, toward the lower left


# ------------------------------------------------------------------ center-line construction

class Pen:
    """A center-line path: lines and circular arcs (angles in degrees, screen coordinates,
    clockwise positive)."""

    def __init__(self):
        self.p = po.Path()
        self.open = False

    def M(self, x, y):
        self.p.moveTo(x, y)
        self.open = True
        return self

    def L(self, x, y):
        self.p.lineTo(x, y)
        return self

    def A(self, cx, cy, r, a0, a1):
        g._arc_to(self.p, cx, cy, r, a0, a1, move=not self.open)
        self.open = True
        return self

    def Z(self):
        self.p.close()
        self.open = False
        return self


def _unit(v):
    L = math.hypot(*v)
    return (v[0] / L, v[1] / L)


def _fillet(prev, v, nxt, r):
    """Tangent points, center and angles of a fillet of radius r at corner v."""
    u1 = _unit((prev[0] - v[0], prev[1] - v[1]))
    u2 = _unit((nxt[0] - v[0], nxt[1] - v[1]))
    cosang = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
    th = math.acos(cosang)
    t = r / math.tan(th / 2)
    p1 = (v[0] + u1[0] * t, v[1] + u1[1] * t)
    p2 = (v[0] + u2[0] * t, v[1] + u2[1] * t)
    b = _unit((u1[0] + u2[0], u1[1] + u2[1]))
    d = r / math.sin(th / 2)
    c = (v[0] + b[0] * d, v[1] + b[1] * d)
    a0 = math.degrees(math.atan2(p1[1] - c[1], p1[0] - c[0]))
    a1 = math.degrees(math.atan2(p2[1] - c[1], p2[0] - c[0]))
    while a1 - a0 > 180:
        a1 -= 360
    while a1 - a0 < -180:
        a1 += 360
    return p1, p2, c, a0, a1


def rpoly(pts, radii=R_RECT, closed=True, pen=None):
    """A polyline through pts with each corner rounded on the center line. radii is one value or a
    list with one radius per point (0 keeps the corner, which the round join then softens)."""
    n = len(pts)
    rs = radii if isinstance(radii, (list, tuple)) else [radii] * n
    pen = pen or Pen()
    idx = range(n) if closed else range(1, n - 1)
    if not closed:
        pen.M(*pts[0])
    first = True
    for i in idx:
        v, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
        if rs[i] <= 0:
            if closed and first:
                pen.M(*v)
            else:
                pen.L(*v)
        else:
            p1, p2, c, a0, a1 = _fillet(a, v, b, rs[i])
            if closed and first:
                pen.M(*p1)
            pen.A(c[0], c[1], rs[i], a0, a1)
        first = False
    if closed:
        pen.Z()
    else:
        pen.L(*pts[-1])
    return pen


def rrect_c(x0, y0, x1, y1, r=R_RECT):
    return rpoly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], r)


def ring_c(cx, cy, r):
    return Pen().A(cx, cy, r, -90, 270).Z()


def arc_c(cx, cy, r, a0, a1):
    return Pen().A(cx, cy, r, a0, a1)


def line_c(*pts):
    pen = Pen().M(*pts[0])
    for q in pts[1:]:
        pen.L(*q)
    return pen


def stroke(pen, w=W):
    p = po.Path()
    pen.p.draw(p.getPen())
    p.stroke(w, po.LineCap.ROUND_CAP, po.LineJoin.ROUND_JOIN, 4)
    p.convertConicsToQuads()
    return g.simplify(p)


def chevron(tip, direction, arm=3.0):
    """An open arrowhead: two strokes from the tip, back along direction (degrees) at 45 degrees."""
    a = math.radians(direction)
    out = []
    for s in (+1, -1):
        b = a + math.pi + s * math.pi / 4
        out.append(line_c((tip[0] + arm * math.cos(b), tip[1] + arm * math.sin(b)), tip))
    return out


def stadium(x0, y0, x1, y1):
    r = min(x1 - x0, y1 - y0) / 2
    return rrect(x0, y0, x1 - x0, y1 - y0, r)


def shifted(path, d=OFFSET):
    return g.transform(path, 1.0, d[0], d[1])


def build(lines, discs=(), reg=None, w=W):
    ink = union(*[stroke(p, w) for p in lines], *[circle(*d) for d in discs])
    return {"ink": ink, "accent": shifted(reg) if reg is not None else g.empty(), "reg": reg,
            "lines": lines, "discs": list(discs)}


# ------------------------------------------------------------------ the ten display masters
# Coordinates are center lines on the 24-unit grid.

def explain(var=None):
    # A square broken open: the body keeps three quarters; its top-right quarter is lifted up and
    # right as a closed lid. The node sits at the body's inner corner, where the lid lifted from.
    body = rpoly([(3, 7), (10, 7), (10, 14), (17, 14), (17, 21), (3, 21)], [R_RECT, R_RECT, 0, R_RECT, R_RECT, R_RECT])
    lid = rrect_c(14, 3, 21, 10)
    reg = rrect(14, 3, 7, 7, R_RECT)          # the plane in register: the lid's fill
    return build([body, lid], [(10, 14, NODE_R)], reg)


def track(var=None):
    # Three stages on a rising stair, drawn as one closed block; the node rides the middle tread.
    st = rpoly([(3, 20), (3, 16), (9, 16), (9, 12), (15, 12), (15, 8), (21, 8), (21, 20)],
               [R_RECT, R_RECT, 0, R_RECT, 0, R_RECT, R_RECT, R_RECT])
    reg = rrect(15, 8, 6, 6, R_RECT)          # in register: the top stage
    return build([st], [(12, 12, NODE_R)], reg)


def _half(cx, cy, r, side, gap):
    """One half of a circle of radius r, cut by a chord gap/2 from the center, corners rounded."""
    big = 40
    if side < 0:
        region = intersect(circle(cx, cy, r), rect(cx - big, cy - big, big - gap / 2, 2 * big))
    else:
        region = intersect(circle(cx, cy, r), rect(cx + gap / 2, cy - big, big, 2 * big))
    return region


def _outline_pen(region, rcorner=1.0):
    """Treat a filled region as a center-line outline, with convex corners rounded by rcorner."""
    import icons_draw as D  # round one, shared; imported, never changed
    rr = D.round_convex(region, rcorner) if rcorner > 0 else region
    pen = Pen()
    rr.draw(pen.p.getPen())
    return pen


def connect(var=None):
    # One circle in two halves held apart; the node sits in the gap on the center line.
    r, gap = 9.25, 8.0
    left = _outline_pen(_half(12, 12, r, -1, gap), 1.0)
    right = _outline_pen(_half(12, 12, r, +1, gap), 1.0)
    reg = circle(12, 12, 3.25)                # in register: a disc centered in the gap
    return build([left, right], [(12, 12, NODE_R)], reg)


def act(var=None):
    # A door swung open: the leaf, hinged at the doorway's left jamb, comes toward the reader in
    # perspective; the frame runs over the opening and down the far jamb. The node is the handle.
    leaf = rpoly([(4, 2.75), (11, 5), (11, 21), (4, 21)], [1.0, 0.0, 0.0, 1.0])
    frame = rpoly([(11, 5), (19, 5), (19, 21)], [0, R_RECT, 0], closed=False)
    lines = [leaf, frame]
    if var == "floor":
        lines.append(line_c((2.5, 21), (21.5, 21)))
    reg = rrect(13, 12, 5.5, 8, R_RECT)       # in register: light in the lower doorway
    return build(lines, [(7.5, 12.5, NODE_R)], reg)


def ballot(var=None):
    # A box with a slot in its top; a paper goes in through the slot. The red is the filled oval.
    box = rpoly([(7, 12), (3.5, 12), (3.5, 21), (20.5, 21), (20.5, 12), (17, 12)], [0, R_RECT, R_RECT, R_RECT, R_RECT, 0],
                closed=False)
    paper = rpoly([(8.5, 14.5), (8.5, 3), (15.5, 3), (15.5, 14.5)], [0, 1.0, 1.0, 0], closed=False)
    reg = stadium(9.5, 5.5, 16.0, 10.0)       # in register: the oval on the paper
    return build([box, paper], [], reg)


def bill(var=None):
    # A page with a folded corner and lines of text; the red is a highlight under one line.
    page = rpoly([(5, 3), (14, 3), (19, 8), (19, 21), (5, 21)], [R_RECT, 0, 0, R_RECT, R_RECT])
    fold = rpoly([(14, 3), (14, 8), (19, 8)], [0, 1.0, 0], closed=False)
    t1 = line_c((8.5, 12), (15.5, 12))
    t2 = line_c((8.5, 15), (15.5, 15))
    t3 = line_c((8.5, 18), (12.5, 18))
    reg = stadium(8.25, 13.0, 17.75, 17.0)    # in register: a highlight over the middle line
    return build([page, fold, t1, t2, t3], [], reg)


def testify(var=None):
    # A person at a witness table speaking into a microphone on a short stand.
    head = ring_c(15, 7, 3.0)
    shoulders = arc_c(15, 19.5, 5.5, 180, 360)
    table = line_c((2.75, 19.5), (21.25, 19.5))
    mic = rpoly([(5.5, 7.5), (8.5, 7.5), (8.5, 12.5), (5.5, 12.5)], 1.5)
    stem = line_c((7, 12.5), (7, 19.5))
    reg = circle(7, 10, 3.25)                 # in register: behind the microphone head
    return build([head, shoulders, table, mic, stem], [], reg)


def housing(var=None):
    # A house with a pitched roof and a door; the door opens the base line.
    house = rpoly([(9.5, 20), (4, 20), (4, 11), (12, 3), (20, 11), (20, 20), (14.5, 20)],
                  [0, R_RECT, 0.6, 1.0, 0.6, R_RECT, 0], closed=False)
    door = rpoly([(9.5, 20), (9.5, 13.5), (14.5, 13.5), (14.5, 20)], [0, 1.0, 1.0, 0], closed=False)
    reg = rrect(9.5, 13.5, 5, 6.5, 1.0)       # in register: the doorway
    return build([house, door], [], reg)


def money(var=None):
    # An open hand, palm up, with a coin resting on it; the wrist sits behind a cuff.
    cuff = line_c((3, 13.5), (3, 21))
    hand = Pen().M(5.5, 15).L(17.5, 15).A(17.5, 17.25, 2.25, -90, 90).L(5.5, 19.5)
    thumb = line_c((8.5, 15), (11, 12.5))
    coin = ring_c(15, 9, 3.5)
    reg = circle(15, 9, 3.5)                  # in register: the coin's fill
    return build([cuff, hand, thumb, coin], [], reg)


def loop(var=None):
    # Two nodes joined by two arrowed arcs into a loop, as a systems map draws a feedback loop.
    lx, rx, cy = 5.5, 18.5, 12
    half = (rx - lx) / 2
    s = 5.0
    R = (half * half + s * s) / (2 * s)
    top_c = (12, cy + R - s)
    bot_c = (12, cy - R + s)
    a = math.degrees(math.asin(half / R))
    gap_deg = math.degrees(2.6 / R)
    top = arc_c(top_c[0], top_c[1], R, -90 - a + gap_deg, -90 + a - gap_deg)
    bot = arc_c(bot_c[0], bot_c[1], R, 90 - a + gap_deg, 90 + a - gap_deg)
    t_end = math.radians(-90 + a - gap_deg)
    tip_t = (top_c[0] + R * math.cos(t_end), top_c[1] + R * math.sin(t_end))
    b_end = math.radians(90 + a - gap_deg)
    tip_b = (bot_c[0] + R * math.cos(b_end), bot_c[1] + R * math.sin(b_end))
    heads = chevron(tip_t, math.degrees(t_end) + 90, 2.6) + chevron(tip_b, math.degrees(b_end) + 90, 2.6)
    reg = circle(rx, cy, 3.25)                # in register: under the right node
    return build([top, bot] + heads, [(lx, cy, NODE_R), (rx, cy, NODE_R)], reg)


DRAW = {"explain": explain, "track": track, "connect": connect, "act": act, "ballot": ballot, "bill": bill,
        "testify": testify, "housing": housing, "money": money, "loop": loop}


def display(name, var=None):
    return DRAW[name](var)


# ------------------------------------------------------------------ SVG

CHAR, NEWS, RED, WHITE, PRUS = "#121212", "#DCD9D2", "#E63946", "#FFFFFF", "#1F2D5A"


def svg(lay, px=96, ink=CHAR, accent=RED, title=None, vb=24):
    """accent=None drops the plane; accent equal to ink turns it to ink."""
    t = f"<title>{title}</title>" if title else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {vb} {vb}">{t}']
    if accent is not None and not g.is_empty(lay["accent"]):
        parts.append(f'<path id="accent" d="{g.d_of(lay["accent"])}" fill="{accent}"/>')
    parts.append(f'<path id="ink" d="{g.d_of(lay["ink"])}" fill="{ink}"/>')
    parts.append("</svg>")
    return "".join(parts)
