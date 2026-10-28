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
OFFSET = (-1.5, 1.5)     # the red plane's fixed off-register shift, toward the lower left (2.1 units)


# ------------------------------------------------------------------ center-line construction

class Pen:
    """A center-line path of lines and circular arcs (angles in degrees, screen coordinates,
    clockwise positive). It keeps its commands, so stroke() can build the outline from exact
    primitives: a bar for each line, an annular sector for each arc, a disc at each corner and end."""

    def __init__(self):
        self.ops = []
        self.p = po.Path()
        self.open = False

    def M(self, x, y):
        self.ops.append(("M", x, y))
        self.p.moveTo(x, y)
        self.open = True
        return self

    def L(self, x, y):
        self.ops.append(("L", x, y))
        self.p.lineTo(x, y)
        return self

    def A(self, cx, cy, r, a0, a1):
        t = math.radians(a0)
        start = (cx + r * math.cos(t), cy + r * math.sin(t))
        if not self.ops or self.ops[-1][0] == "Z":
            self.ops.append(("M", *start))
        self.ops.append(("A", cx, cy, r, a0, a1))
        g._arc_to(self.p, cx, cy, r, a0, a1, move=not self.open)
        self.open = True
        return self

    def Z(self):
        self.ops.append(("Z",))
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


def _bar(p, q, w):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    if L < 1e-9:
        return g.empty()
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return poly((p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny), (p[0] - nx, p[1] - ny))


def _dir_line(p, q):
    return _unit((q[0] - p[0], q[1] - p[1]))


def _dir_arc(a, sweep):
    t = math.radians(a)
    s_ = 1 if sweep > 0 else -1
    return (-math.sin(t) * s_, math.cos(t) * s_)


def stroke(pen, w=W):
    """Outline a center-line Pen at width w with round caps and round joins, built from exact
    primitives so every edge is a straight line or a true circular arc."""
    parts, discs = [], []
    cur = start = None
    seg_dirs = []          # (start_dir, end_dir, start_pt, end_pt) per segment of the current contour
    contours = []

    def close_contour(closed):
        if not seg_dirs:
            if cur is not None:
                discs.append(cur)
            return
        n = len(seg_dirs)
        for i in range(n - 1):
            d_out, d_in = seg_dirs[i][1], seg_dirs[i + 1][0]
            if d_out[0] * d_in[0] + d_out[1] * d_in[1] < 0.9999:
                discs.append(seg_dirs[i][3])
        if closed:
            d_out, d_in = seg_dirs[-1][1], seg_dirs[0][0]
            if d_out[0] * d_in[0] + d_out[1] * d_in[1] < 0.9999:
                discs.append(seg_dirs[0][2])
        else:
            discs.append(seg_dirs[0][2])
            discs.append(seg_dirs[-1][3])

    for op in pen.ops:
        if op[0] == "M":
            if seg_dirs:
                close_contour(False)
            seg_dirs = []
            cur = start = (op[1], op[2])
        elif op[0] == "L":
            q = (op[1], op[2])
            if math.hypot(q[0] - cur[0], q[1] - cur[1]) > 1e-9:
                parts.append(_bar(cur, q, w))
                d = _dir_line(cur, q)
                seg_dirs.append((d, d, cur, q))
            cur = q
        elif op[0] == "A":
            _, cx, cy, r, a0, a1 = op
            t0, t1 = math.radians(a0), math.radians(a1)
            p0 = (cx + r * math.cos(t0), cy + r * math.sin(t0))
            p1 = (cx + r * math.cos(t1), cy + r * math.sin(t1))
            if math.hypot(p0[0] - cur[0], p0[1] - cur[1]) > 1e-6:
                parts.append(_bar(cur, p0, w))
                d = _dir_line(cur, p0)
                seg_dirs.append((d, d, cur, p0))
            ri = max(0.0, r - w / 2)
            if abs(a1 - a0) >= 359.999:
                parts.append(g.ring(cx, cy, r + w / 2, ri) if ri > 0 else circle(cx, cy, r + w / 2))
            elif ri > 0:
                parts.append(g.sector(cx, cy, r + w / 2, ri, min(a0, a1), max(a0, a1)))
            else:
                pie = po.Path()
                pie.moveTo(cx, cy)
                g._arc_to(pie, cx, cy, r + w / 2, min(a0, a1), max(a0, a1), move=False)
                pie.close()
                parts.append(g.simplify(pie))
            seg_dirs.append((_dir_arc(a0, a1 - a0), _dir_arc(a1, a1 - a0), p0, p1))
            cur = p1
        elif op[0] == "Z":
            if start is not None and math.hypot(start[0] - cur[0], start[1] - cur[1]) > 1e-6:
                parts.append(_bar(cur, start, w))
                d = _dir_line(cur, start)
                seg_dirs.append((d, d, cur, start))
            close_contour(True)
            seg_dirs = []
            cur = start
    if seg_dirs:
        close_contour(False)
    parts += [circle(x, y, w / 2) for (x, y) in discs]
    parts = [q for q in parts if not g.is_empty(q)]
    return union(*parts) if parts else g.empty()


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


def shifted(path, d=None):
    d = d or OFFSET
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
    reg = rrect(14, 3, 7, 7, R_RECT)          # in register: the lid's fill
    return build([body, lid], [(10, 14, NODE_R)], reg)


def track(var=None):
    # Three stages on a rising stair, drawn as one closed block. The node sits on the nose of the
    # middle stage, where the decision steps up.
    st = rpoly([(3, 20), (3, 16), (9, 16), (9, 12), (15, 12), (15, 8), (21, 8), (21, 20)],
               [R_RECT, R_RECT, 0, R_RECT, 0, R_RECT, R_RECT, R_RECT])
    reg = rrect(15, 8, 6, 6, R_RECT)          # in register: the top stage
    node = (9, 12) if var != "mid" else (12, 12)
    return build([st], [(*node, NODE_R)], reg)


def half_pen(cx, cy, R, gap, side, rf=1.0):
    """One half of a circle of radius R cut by a chord gap/2 from the center (side -1 left,
    +1 right), as a center line whose two corners take fillets of radius rf, tangent to the chord
    and to the circle."""
    xc_rel = gap / 2                           # chord distance from the center
    fx = xc_rel + rf                           # fillet center distance from the center, in x
    fy = math.sqrt((R - rf) ** 2 - fx ** 2)
    phi = math.degrees(math.atan2(-fy, -fx))   # direction from the center to the top-left fillet
    pen = Pen()
    if side < 0:
        x = cx - xc_rel
        pen.M(x, cy + fy).L(x, cy - fy)
        pen.A(cx - fx, cy - fy, rf, 0, phi)            # top fillet
        pen.A(cx, cy, R, phi, -360 - phi)               # the round side
        pen.A(cx - fx, cy + fy, rf, -phi, 0)            # bottom fillet
    else:
        th = 180 + phi
        x = cx + xc_rel
        pen.M(x, cy - fy).L(x, cy + fy)
        pen.A(cx + fx, cy + fy, rf, 180, th)
        pen.A(cx, cy, R, th, -th)
        pen.A(cx + fx, cy - fy, rf, -th, -180)
    return pen.Z()


def connect(var=None):
    # One circle in two halves held apart; the node sits in the gap on the center line.
    R, gap = 9.25, 8.0
    left = half_pen(12, 12, R, gap, -1, 1.0)
    right = half_pen(12, 12, R, gap, +1, 1.0)
    if var == "low":
        reg = circle(12, 16, 3.0)             # in register: low in the gap, the ground under the node
    elif var == "small":
        reg = circle(12, 12, 2.6)
    else:
        reg = circle(12, 12, 3.0)             # in register: a disc centered in the gap
    return build([left, right], [(12, 12, NODE_R)], reg)


def act(var=None):
    # A door swung open on its floor. The leaf, hinged at the doorway's left side, comes toward the
    # reader in perspective; the frame runs over the opening only and down the far jamb, held
    # apart from the leaf as Direction A draws it. The node is the handle.
    floor = line_c((2.5, 21), (21.5, 21))
    leaf = rpoly([(4, 21), (4, 2.75), (10.5, 5), (10.5, 21)], [0, 1.0, 0.6, 0], closed=False)
    frame = rpoly([(13.25, 5), (19.5, 5), (19.5, 21)], [0, R_RECT, 0], closed=False)
    reg = rrect(14, 13.5, 5, 6.5, R_RECT)     # in register: light on the floor of the doorway
    return build([leaf, frame, floor], [(7.25, 12.5, NODE_R)], reg)


def ballot(var=None):
    # A box with a paper going in at its top. The paper carries a printed oval; the red is the
    # voter's mark, which covers the oval to its outer edge and prints off register.
    top = 12.5
    box = rrect_c(3.5, top, 20.5, 21)
    paper = rpoly([(7, top), (7, 2.75), (17, 2.75), (17, top)], [0, 1.0, 1.0, 0], closed=False)
    ox0, oy0, ox1, oy1 = 9.5, 5.0, 14.5, 8.25
    oval = rpoly([(ox0, oy0), (ox1, oy0), (ox1, oy1), (ox0, oy1)], (oy1 - oy0) / 2)
    reg = stadium(ox0 - 0.75, oy0 - 0.75, ox1 + 0.75, oy1 + 0.75)   # in register: the oval, edge to edge
    return build([box, paper, oval], [], reg)


def bill(var=None):
    # A page with a folded corner and lines of text; the red is a highlight under the last line.
    page = rpoly([(5, 3), (14, 3), (19, 8), (19, 21), (5, 21)], [R_RECT, 0, 0, R_RECT, R_RECT])
    fold = rpoly([(14, 3), (14, 8), (19, 8)], [0, 1.0, 0], closed=False)
    t1 = line_c((8.5, 9.5), (11, 9.5))
    t2 = line_c((8.5, 12.5), (15.5, 12.5))
    t3 = line_c((8.5, 15.5), (15.5, 15.5))
    reg = stadium(8.75, 13.25, 17.25, 17.75)  # in register: a highlight over the last line
    return build([page, fold, t1, t2, t3], [], reg)


def testify(var=None):
    # A person at a witness table speaking into a microphone on a short stand.
    head = ring_c(15, 7, 3.0)
    shoulders = arc_c(15, 19.5, 5.5, 180, 360)
    table = line_c((2.75, 19.5), (21.25, 19.5))
    mic = rpoly([(5.5, 7), (8.5, 7), (8.5, 12.5), (5.5, 12.5)], 1.5)
    stem = line_c((7, 12.5), (7, 19.5))
    reg = circle(7, 9.75, 3.25)               # in register: behind the microphone head
    return build([head, shoulders, table, mic, stem], [], reg)


def housing(var=None):
    # A house with a pitched roof and a door; the door opens the base line.
    house = rpoly([(9.5, 20), (4, 20), (4, 11), (12, 3), (20, 11), (20, 20), (14.5, 20)],
                  [0, R_RECT, 0.6, 1.0, 0.6, R_RECT, 0], closed=False)
    door = rpoly([(9.5, 20), (9.5, 13.5), (14.5, 13.5), (14.5, 20)], [0, 1.0, 1.0, 0], closed=False)
    reg = rrect(9.5, 13.5, 5, 6.5, 1.0)       # in register: the doorway
    return build([house, door], [], reg)


def money(var=None):
    # An open hand, palm up, with a coin lifting off it; the red is the coin, printed off register.
    # A cuff at the wrist; the thumb lies forward along the top of the hand and steps down to the
    # palm; the fingers end in one round tip.
    cuff = rpoly([(2.5, 12.5), (5, 12.5), (5, 21.5), (2.5, 21.5)], 0.75)
    hand = rpoly([(5, 13.5), (10.75, 13.5), (10.75, 15.5), (20.25, 15.5), (20.25, 20), (5, 20)],
                 [0, 1.5, 0.5, 2.25, 2.25, 0], closed=False)
    coin = ring_c(15, 7, 3.25)
    reg = circle(15, 7, 3.25)                 # in register: the coin's fill
    return build([cuff, hand, coin], [], reg)

def _arrow_on_arc(c, R, ang, sense, arm):
    """A chevron sitting on an arc at angle ang, pointing along the arc (+1 clockwise on screen)."""
    t = math.radians(ang)
    tip = (c[0] + R * math.cos(t), c[1] + R * math.sin(t))
    return chevron(tip, ang + 90 * sense, arm)


def loop(var=None):
    # Two nodes joined by two arcs into one closed loop, as a systems map draws a feedback loop;
    # an arrowhead on each arc gives the direction of travel.
    cy, lx, rx = 12, 5.0, 19.0
    half = (rx - lx) / 2
    sg = 4.5
    R = (half * half + sg * sg) / (2 * sg)
    top_c, bot_c = (12, cy + R - sg), (12, cy - R + sg)
    a = math.degrees(math.asin(half / R))
    top = arc_c(top_c[0], top_c[1], R, -90 - a, -90 + a)
    bot = arc_c(bot_c[0], bot_c[1], R, 90 - a, 90 + a)
    arm = 2.0
    heads = _arrow_on_arc(top_c, R, -90 + 4, +1, arm) + _arrow_on_arc(bot_c, R, 90 + 4, +1, arm)
    rn = 1.75
    reg = circle(rx, cy, 3.25)                # in register: under the right node
    return build([top, bot] + heads, [(lx, cy, rn), (rx, cy, rn)], reg)


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
