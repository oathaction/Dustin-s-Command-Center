"""Concept 1, Overprint: the ten round-two test icons (design director, Phase 2, round two,
October 28, 2026). Stage 2: the display masters redrawn after the creative director's stage 1
notes, and the 24 and 16 px masters drawn on whole pixels.

Idea. A fine Charcoal line drawing printed over one solid Pillar Red plane set off register, the way
a second ink lands on a newspaper page. The red sits under the part of the subject the story is
about. The line drawing is whole without it.

Grid. Round one's 24-unit grid (icons_draw.py): 2-unit padding, live area 2 to 22; keylines circle 20,
square 18, portrait 16 by 20, landscape 20 by 16. Straight edges stay inside the live area; round
forms overshoot it by 0.25 units at most. The 16 px masters are separate drawings on a 16-unit grid
with 1-unit padding, live area 1 to 15. Every drawing is written as center lines.

Line. Round caps and round joins. Display master (48 px and up): 1.5 units. 24 and 16 px masters:
2 px, with straight center lines on whole pixels so both edges land on pixel boundaries.
Rectangles take a 2-unit outer radius in the display master (center-line radius 1.25) and 1 px at
24 px. The pillar marks carry the node as a solid ink disc 3 units across.

The red plane. It fills one shape of the drawing, to the line's center, and prints off register at
one fixed offset toward the lower left: 1.5 units left and 1.5 down in the display master, 2 px at
24 px and 1 px at 16 px. Ballot's mark covers its printed oval to the outer edge, as a pen mark
does. Connect is the one exception (Rule 01.1): its plane centers on the gap and prints straight
down, clear of both halves.

Every drawing returns layers:
  ink     the line drawing and any ink nodes, as one filled outline
  accent  the red plane, already moved by its offset
  lines   the center-line paths (construction views)
  reg     the red plane in register, before the offset (construction views)
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
    "explain": "Red fills the inside the open lid reveals.",
    "track": "Red fills the top stage, where the decision is headed.",
    "connect": "Red is the ground in the gap between the two halves, clear of both.",
    "act": "Red is the light on the floor of the open doorway.",
    "ballot": "Red is the filled oval, the mark a voter makes.",
    "bill": "Red highlights the one line of the bill the story is about.",
    "testify": "Red fills the microphone, where a voice goes on the record.",
    "housing": "Red fills the doorway, the way into a home.",
    "money": "Red fills the banknote's center disc, the money itself.",
    "loop": "Red fills the node the return arrives at, where the feedback acts.",
}

W = 1.5                  # display stroke, in grid units
R_RECT = 1.25            # center-line corner radius for rectangles (2-unit outer radius)
NODE_R = 1.5             # pillar-mark node, a solid ink disc 3 units across
OFFSET = (-1.5, 1.5)     # the red plane's off-register shift in the display master (2.1 units)
SIZES = ("display", 24, 16)
SPEC = {"display": {"w": 1.5, "off": (-1.5, 1.5), "grid": 24},
        24: {"w": 2.0, "off": (-2.0, 2.0), "grid": 24},
        16: {"w": 2.0, "off": (-1.0, 1.0), "grid": 16}}


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


def build(lines, discs=(), reg=None, size="display", off=None, accent=None, extra_ink=()):
    """Stroke the center lines at the size's width, add ink discs and any filled ink shapes, and
    print the red plane at the size's offset (or at off, for Connect's exception)."""
    sp = SPEC[size]
    parts = [stroke(p, sp["w"]) for p in lines] + [circle(*d) for d in discs] + list(extra_ink)
    ink = union(*parts)
    if accent is None:
        accent = shifted(reg, off or sp["off"]) if reg is not None else g.empty()
    return {"ink": ink, "accent": accent, "reg": reg, "lines": lines, "discs": list(discs), "size": size}


def rotate_pen(pen, deg, cx, cy):
    """The same center-line path turned deg degrees (clockwise on screen) about (cx, cy)."""
    t = math.radians(deg)
    c, s_ = math.cos(t), math.sin(t)

    def f(x, y):
        x, y = x - cx, y - cy
        return cx + x * c - y * s_, cy + x * s_ + y * c
    out = Pen()
    for op in pen.ops:
        if op[0] == "M":
            out.M(*f(op[1], op[2]))
        elif op[0] == "L":
            out.L(*f(op[1], op[2]))
        elif op[0] == "A":
            x, y = f(op[1], op[2])
            out.A(x, y, op[3], op[4] + deg, op[5] + deg)
        else:
            out.Z()
    return out


def rotate_path(path, deg, cx, cy):
    return g.rot(path, deg, cx, cy)


# ------------------------------------------------------------------ the ten icons
# Each function takes size: "display" (24-unit grid, 1.5-unit line), 24 or 16 (2 px line).

DRAW = {}


def icon(fn):
    DRAW[fn.__name__] = fn
    return fn


def display(name, var=None):
    return DRAW[name]("display", var)


def master(name, size):
    return DRAW[name](size, None)


def draw(name, size, var=None):
    return DRAW[name](size, var)


def half_pen(cx, cy, R, gap, side, rf=1.0):
    """One half of a circle of radius R cut by a chord gap/2 from the center (side -1 left, +1
    right), as a center line whose two corners take fillets of radius rf, tangent to the chord and
    to the circle."""
    xc = gap / 2
    fx = xc + rf
    fy = math.sqrt((R - rf) ** 2 - fx ** 2)
    phi = math.degrees(math.atan2(-fy, -fx))
    pen = Pen()
    if side < 0:
        x = cx - xc
        pen.M(x, cy + fy).L(x, cy - fy)
        pen.A(cx - fx, cy - fy, rf, 0, phi)
        pen.A(cx, cy, R, phi, -360 - phi)
        pen.A(cx - fx, cy + fy, rf, -phi, 0)
    else:
        th = 180 + phi
        x = cx + xc
        pen.M(x, cy - fy).L(x, cy + fy)
        pen.A(cx + fx, cy + fy, rf, 180, th)
        pen.A(cx, cy, R, th, -th)
        pen.A(cx + fx, cy - fy, rf, -th, -180)
    return pen.Z()


def tilted_stadium(cx, cy, w, length, deg):
    """A stadium w wide and length long, centered on (cx, cy), its long axis turned deg degrees
    from vertical (clockwise on screen)."""
    return rotate_path(rrect(cx - w / 2, cy - length / 2, w, length, w / 2), deg, cx, cy)


def tilted_stadium_pen(cx, cy, w, length, deg):
    r = w / 2
    pen = rpoly([(cx - r, cy - length / 2), (cx + r, cy - length / 2), (cx + r, cy + length / 2), (cx - r, cy + length / 2)], r)
    return rotate_pen(pen, deg, cx, cy)


@icon
def explain(size, var=None):
    """A square broken open: its top-right quarter is a lid, lifted clear and turned on its hinge
    corner. The red fills the open quarter and slides toward the node at the inner corner."""
    if size == "display":
        s_, x0, y0, turn = 12.0, 5.0, 6.0, -15.0
        dx, dy = 0.75, -2.0                      # the lid lifts 2 and moves 0.75 toward its hinge side
        r = R_RECT
        q = s_ / 2
        body = rpoly([(x0, y0), (x0 + q, y0), (x0 + q, y0 + q), (x0 + s_, y0 + q), (x0 + s_, y0 + s_), (x0, y0 + s_)],
                     [r, r, 0, r, r, r])
        hx, hy = x0 + q + dx, y0 + dy
        lid = rotate_pen(rrect_c(hx, hy, hx + q, hy + q, r), turn, hx, hy)
        k = 5.25 if var is None else float(var)
        reg = rrect(x0 + s_ - 0.25 - k, y0 + 0.25, k, k, r)
        return build([body, lid], [(x0 + q, y0 + q, NODE_R)], reg, size)
    raise KeyError(size)


@icon
def track(size, var=None):
    """Three equal stages climbing from the bottom left of the landscape keyline to its top right,
    drawn as one closed block. The node sits on the riser between the first and second stages, on
    the center line; the red fills the top stage."""
    if size == "display":
        xs = [2.75 + i * (18.5 / 3) for i in range(4)]
        ys = [19.25 - i * (14.5 / 3) for i in range(4)]
        r = R_RECT
        st = rpoly([(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[1]), (xs[1], ys[2]), (xs[2], ys[2]), (xs[2], ys[3]),
                    (xs[3], ys[3]), (xs[3], ys[0])], [r, r, 0, r, 0, r, r, r])
        reg = rrect(xs[2], ys[3], xs[3] - xs[2], ys[2] - ys[3], r)
        return build([st], [(xs[1], 12, NODE_R)], reg, size)
    raise KeyError(size)


@icon
def connect(size, var=None):
    """One circle in two halves held apart; the node sits in the gap on the center line. The red
    centers on the gap and prints straight down, clear of both halves (Rule 01.1)."""
    if size == "display":
        R, gap = 9.25, 8.0
        left = half_pen(12, 12, R, gap, -1, 1.0)
        right = half_pen(12, 12, R, gap, +1, 1.0)
        wr = 4.5
        reg = rrect(12 - wr / 2, 9.25, wr, 5.5, R_RECT)
        return build([left, right], [(12, 12, NODE_R)], reg, size, off=(0.0, 1.5))
    raise KeyError(size)


@icon
def act(size, var=None):
    """A door swung open on its floor: the leaf comes toward the reader in perspective, the frame
    runs over the opening only and down the far jamb, held apart from the leaf as Direction A
    draws it. The node is the handle. The red lights the lower half of the doorway."""
    if size == "display":
        floor = line_c((2.75, 21), (21.25, 21))
        leaf = rpoly([(4, 21), (4, 2.75), (10.5, 5), (10.5, 21)], [0, 1.0, 0.6, 0], closed=False)
        frame = rpoly([(14, 5), (19.5, 5), (19.5, 21)], [0, R_RECT, 0], closed=False)
        wr = 4.5
        reg = rrect(14.5, 10.5, wr, 9.0, R_RECT)
        return build([leaf, frame, floor], [(7.25, 12, NODE_R)], reg, size)
    raise KeyError(size)


@icon
def ballot(size, var=None):
    """A ballot box with a slot across its top face; the paper's lower third sinks into the slot.
    The paper carries a printed oval; the red is the voter's mark, which covers the oval to its
    outer edge and prints off register."""
    if size == "display":
        top, slot = 10.5, 13.5
        p0, p1 = 7.25, 16.75
        box = rpoly([(p0, top), (4.75, top), (4.75, 19.75), (19.25, 19.75), (19.25, top), (p1, top)],
                    [0, R_RECT, R_RECT, R_RECT, R_RECT, 0], closed=False)
        slot_l = line_c((6.75, slot), (17.25, slot))
        paper = rpoly([(p0, slot), (p0, 4.25), (p1, 4.25), (p1, slot)], [0, 1.0, 1.0, 0], closed=False)
        ox0, oy0, ox1, oy1 = 9.625, 6.5, 14.375, 9.5
        oval = rpoly([(ox0, oy0), (ox1, oy0), (ox1, oy1), (ox0, oy1)], (oy1 - oy0) / 2)
        reg = stadium(ox0 - 0.75, oy0 - 0.75, ox1 + 0.75, oy1 + 0.75)
        return build([box, slot_l, paper, oval], [], reg, size)
    raise KeyError(size)


@icon
def bill(size, var=None):
    """A page with a folded corner and lines of text; the red highlights the last line."""
    if size == "display":
        page = rpoly([(5.25, 3), (14, 3), (18.75, 7.75), (18.75, 21), (5.25, 21)], [R_RECT, 0, 0, R_RECT, R_RECT])
        fold = rpoly([(14, 3), (14, 7.75), (18.75, 7.75)], [0, 1.0, 0], closed=False)
        t1 = line_c((8.5, 8.5), (10.5, 8.5))
        t2 = line_c((8.5, 11.5), (14.75, 11.5))
        t3 = line_c((8.5, 14.5), (14.75, 14.5))
        reg = stadium(8.75, 12.25, 17.25, 16.75)
        return build([page, fold, t1, t2, t3], [], reg, size)
    raise KeyError(size)


@icon
def testify(size, var=None):
    """A person at a witness table speaking into a microphone; the capsule sits at mouth height on
    a short gooseneck, angled toward the face. The red fills the capsule."""
    if size == "display":
        head = ring_c(15.5, 7, 2.75)
        shoulders = arc_c(15.5, 19.5, 5.25, 180, 360)
        table = line_c((2.75, 19.5), (21.25, 19.5))
        cx, cy, cw, cl, ang = 9.25, 11.75, 3.75, 5.5, 45
        cap = tilted_stadium_pen(cx, cy, cw, cl, ang)
        u = (math.sin(math.radians(ang)), -math.cos(math.radians(ang)))
        foot = (cx - u[0] * cl / 2, cy - u[1] * cl / 2)
        bend = (foot[0] - u[0] * 1.25, foot[1] - u[1] * 1.25)
        neck = rpoly([foot, (bend[0], bend[1]), (bend[0], 19.5)], [0, 1.25, 0], closed=False)
        reg = tilted_stadium(cx, cy, cw, cl, ang)
        return build([head, shoulders, table, cap, neck], [], reg, size)
    raise KeyError(size)


@icon
def housing(size, var=None):
    """A house with a pitched roof; its door opens the base line. The red fills the doorway."""
    if size == "display":
        house = rpoly([(9.5, 20), (4, 20), (4, 11), (12, 3), (20, 11), (20, 20), (14.5, 20)],
                      [0, R_RECT, 0.6, 1.0, 0.6, R_RECT, 0], closed=False)
        door = rpoly([(9.5, 20), (9.5, 13.5), (14.5, 13.5), (14.5, 20)], [0, 1.0, 1.0, 0], closed=False)
        reg = rrect(9.5, 13.5, 4, 6.5, 1.0)
        return build([house, door], [], reg, size)
    raise KeyError(size)


@icon
def money(size, var=None):
    """A banknote: a landscape rounded rectangle with a disc at its center and a short bar in two
    opposite corners. The red fills the center disc."""
    if size == "display":
        note = rrect_c(3, 6.5, 21, 17.5)
        disc = ring_c(12, 12, 2.75)
        b1 = line_c((5.75, 9.25), (7.25, 9.25))
        b2 = line_c((16.75, 14.75), (18.25, 14.75))
        reg = circle(12, 12, 2.75)
        return build([note, disc, b1, b2], [], reg, size)
    raise KeyError(size)


@icon
def loop(size, var=None):
    """Two nodes on the center line. The forward link runs straight along the top, its arrowhead
    arriving at the right node; the return comes back below as a deep arc, its arrowhead at the
    bottom, and runs into the left node. The red fills that node."""
    if size == "display":
        v = [float(t) for t in var.split("/")] if var else [5.75, 19.0, 2.25, 0.25, 2.75]
        lx, rx, rn, drop, arm = v
        cy = 12.0
        cxa, cya = (lx + rx) / 2, cy + drop
        R = math.hypot(rx - cxa, cy - cya)
        tip_f = rx - rn - 1.25
        link = line_c((lx, cy), (tip_f, cy))
        heads = chevron((tip_f, cy), 0, arm)
        a_right = math.degrees(math.atan2(cy - cya, rx - cxa))
        a_left = 180 - a_right
        ret = arc_c(cxa, cya, R, a_right, a_left)
        heads += _arrow_on_arc((cxa, cya), R, 90 + 3, +1, arm)
        reg = circle(lx, cy, rn)
        return build([link, ret] + heads, [(lx, cy, rn), (rx, cy, rn)], reg, size)
    raise KeyError(size)


def _arrow_on_arc(c, R, ang, sense, arm):
    """A chevron sitting on an arc at angle ang, pointing along the arc (+1 clockwise on screen)."""
    t = math.radians(ang)
    tip = (c[0] + R * math.cos(t), c[1] + R * math.sin(t))
    return chevron(tip, ang + 90 * sense, arm)

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
