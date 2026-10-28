"""Concept 1, Overprint: the ten round-two test icons (design director, Phase 2, round two,
October 28, 2026). Stage 2 redrew the display masters after the creative director's stage 1 notes.
The fix pass applies fixes 1 to 4 of the creative director's final review: a solid, one-color
16 px cut; Feedback loop as a closed ring with three stations; Ballot's paper raised; Connect and
Campaign money pulled apart at 24 px (with Testify's 24 px master raised 1 px to clear Track).

Idea. A fine Charcoal line drawing printed over one solid Pillar Red plane set off register, the way
a second ink lands on a newspaper page. The red sits under the part of the subject the story is
about. The line drawing is whole without it. From 24 px up.

Grid. Round one's 24-unit grid (icons_draw.py): 2-unit padding, live area 2 to 22; keylines circle 20,
square 18, portrait 16 by 20, landscape 20 by 16. Straight edges stay inside the live area; round
forms overshoot it by 0.25 units at most. Every line drawing is written as center lines.

Line. Round caps and round joins. Display master (48 px and up): 1.5 units. 24 px master: 2 px,
with straight center lines on whole pixels so both edges land on pixel boundaries. Rectangles take
a 2-unit outer radius in the display master (center-line radius 1.25) and 1 px at 24 px; the
banknote keeps a 1-unit corner. The pillar marks carry the node as a solid ink disc 3 units across.

The red plane. It fills one shape of the drawing, to the line's center, and prints off register at
one fixed offset toward the lower left: 1.5 units left and 1.5 down in the display master, 2 px at
24 px. Ballot's mark covers its printed oval to the outer edge, as a pen mark does. Connect is the
one exception (Rule 01.1): its plane centers on the gap and prints straight down, clear of both
halves.

16 px. A separate solid cut in one color, with no red (see the section below).

Every drawing returns layers:
  ink     the line drawing and any ink nodes, as one filled outline (at 16 px, the solid pieces)
  accent  the red plane, already moved by its offset (empty at 16 px)
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
    "money": "Red fills the banknote's disc, the money itself.",
    "loop": "Red fills the top station, where a reform acts on the loop.",
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


# ------------------------------------------------------------------ the 16 px solid cut
# Fix pass (creative director's final review, fix 1). At 16 px the family changes cut: Direction A's
# filled grammar in one color, drawn as hinted vectors on the 16-unit grid (live area 1 to 15).
# Straight edges sit on whole pixels, curves stay true curves, pieces stand 1 px apart, and
# knock-outs are 1 px or more. No red at 16 px: these icons live in rows, legends and tables, where
# Rule 05.3 already makes them one color, and the current item shows by its label.
# Explain, Track, Connect, Act, Ballot, Bill and Housing start from Moving part's 16 px masters
# (work/boards/phase-2/icons-r2/moving-part/, read and never edited); Testify, Campaign money and
# Feedback loop are filled versions of Overprint's own drawings. The node is a 2 px square bead.


def R16(x0, y0, x1, y1):
    return rect(x0, y0, x1 - x0, y1 - y0)


S16 = {}


def solid(fn):
    S16[fn.__name__[:-2]] = fn
    return fn


def _turned_rect(hx, hy, w, h, deg):
    """A w by h rectangle hinged at its top-left corner (hx, hy) and turned deg degrees."""
    t = math.radians(deg)
    u = (math.cos(t), math.sin(t))
    v = (-math.sin(t), math.cos(t))
    return poly((hx, hy), (hx + u[0] * w, hy + u[1] * w), (hx + u[0] * w + v[0] * h, hy + u[1] * w + v[1] * h), (hx + v[0] * h, hy + v[1] * h))


def _page16(x0, x1, fold, holes, y1=15):
    """A page with its top-right corner folded down as a separate flap, 1 px clear of the page."""
    f = x1 - fold
    page = poly((x0, 1), (f, 1), (x1, 1 + fold), (x1, y1), (x0, y1))
    page = minus(page, union(R16(f - 1, 1, f, 2 + fold), R16(f - 1, 1 + fold, x1, 2 + fold)))
    flap = intersect(poly((f, 1), (x1, 1 + fold), (f, 1 + fold)), R16(f, 1, x1, 1 + fold))
    page = union(minus(page, R16(f, 1, x1, 1 + fold)), flap)
    return minus(page, union(*[R16(*h) for h in holes])) if holes else page


@solid
def explain16(var=None):
    """Moving part's L-shaped body with the node in its seat at the inner corner; the lid is a flat
    slab lifted off the open quarter and turned 25 degrees on its hinge corner."""
    body = minus(minus(R16(2, 5, 12, 15), R16(7, 5, 12, 10)), circle(8, 9, 2.414))
    node = R16(7, 8, 9, 10)
    lid = _turned_rect(8.2, 3.6, 5.2, 2.0, -25)
    return union(body, node, lid)


@solid
def track16(var=None):
    """A flight of three rises with a sloped underside, so the top stage sits on the stair and the
    shape reads as steps rather than bars. The node sits on the first tread, 1 px from the riser."""
    flight = poly((1, 15), (1, 11), (6, 11), (6, 7), (10, 7), (10, 3), (15, 3), (15, 7), (7, 15))
    node = R16(3, 8, 5, 10)
    return union(flight, node)


@solid
def connect16(var=None):
    """One disc of 7 px radius in two halves held 6 px apart; the node sits in the gap, 2 px clear
    of both."""
    d = circle(8, 8, 7)
    return union(intersect(d, R16(0, 0, 5, 16)), intersect(d, R16(11, 0, 16, 16)), R16(7, 7, 9, 9))


@solid
def act16(var=None):
    """Moving part's frame with the full lintel (round one's IC-04), the far jamb and the floor,
    each 1 px apart. The leaf stands open on the near side in perspective, with the node knocked out
    of it as the handle."""
    frame = union(R16(2, 1, 15, 3), R16(13, 3, 15, 12))
    floor = R16(1, 13, 15, 15)
    leaf = minus(poly((3, 4), (8, 5.5), (8, 12), (3, 12)), R16(6, 8, 7, 10))
    return union(frame, floor, leaf)


@solid
def ballot16(var=None):
    """The paper stands 7 px above the box, between the two halves of the lid, with the printed
    oval knocked out of its upper half; the box sits 1 px below the lid."""
    paper = minus(R16(5, 2, 11, 9), rrect(6, 3, 4, 2, 1))
    lid = union(R16(1, 9, 4, 10), R16(12, 9, 15, 10))
    box = R16(1, 11, 15, 15)
    return union(paper, lid, box)


@solid
def bill16(var=None):
    """A page 8 px wide with its corner folded down as a flap; three lines of text knocked out,
    running to the page's right edge."""
    return _page16(4, 12, 4, [(6, 8, 12, 9), (6, 10, 12, 11), (6, 12, 12, 13)])


@solid
def testify16(var=None):
    """A person at a table speaking into a microphone on a stand, the capsule at mouth height and
    turned 45 degrees toward the face."""
    head = circle(10, 3.5, 2.5)
    shoulders = intersect(rrect(6, 8, 8, 8, 3.2), R16(6, 8, 14, 11))
    table = R16(1, 13, 15, 15)
    cap = tilted_stadium(4.25, 5.5, 2.5, 4.0, 45)
    stand = R16(3, 7, 4, 12)
    return union(head, shoulders, table, cap, stand)


@solid
def housing16(var=None):
    """A roof drawn as a band over walls with the doorway knocked out; roof and walls 1 px apart."""
    roof = minus(poly((1, 8), (8, 1), (15, 8)), poly((4, 8), (8, 4), (12, 8)))
    walls = minus(R16(3, 9, 13, 15), R16(6, 11, 10, 15))
    return union(roof, walls)


@solid
def money16(var=None):
    """The banknote across the keyline as a solid piece with a counter; the disc sits left of
    center inside it, and one short bar sits at the bottom right."""
    note = minus(R16(1, 3, 15, 13), R16(3, 5, 13, 11))
    return union(note, circle(6.5, 8.5, 1.5), R16(10, 9, 12, 10))


@solid
def loop16(var=None):
    """The ring with its three stations as solid beads. The ring breaks 1 px clear of each bead, and
    each of its three arcs carries a solid arrowhead turning clockwise."""
    cx, cy, Rr, rn = 8, 8.5, 5.5, 1.75
    pos = [(cx + Rr * math.cos(math.radians(a)), cy + Rr * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    ring = minus(g.ring(cx, cy, Rr + 1, Rr - 1), union(*[circle(x, y, rn + 1) for x, y in pos]))
    parts = [ring] + [circle(x, y, rn) for x, y in pos]
    for a in (10, 130, 250):
        t = math.radians(a)
        p = (cx + Rr * math.cos(t), cy + Rr * math.sin(t))
        d = (-math.sin(t), math.cos(t))
        n = (math.cos(t), math.sin(t))
        tip = (p[0] + d[0] * 1.75, p[1] + d[1] * 1.75)
        base = (p[0] - d[0], p[1] - d[1])
        parts.append(poly(tip, (base[0] + n[0] * 2.25, base[1] + n[1] * 2.25), (base[0] - n[0] * 2.25, base[1] - n[1] * 2.25)))
    return union(*parts)


def solid16(name, var=None):
    return {"ink": S16[name](var), "accent": g.empty(), "reg": None, "lines": [], "discs": [], "size": 16, "solid": True}


# ------------------------------------------------------------------ the ten icons
# Each function takes size: "display" (24-unit grid, 1.5-unit line), 24 or 16 (2 px line).

DRAW = {}


def icon(fn):
    DRAW[fn.__name__] = fn
    return fn


def display(name, var=None):
    return DRAW[name]("display", var)


def master(name, size):
    return solid16(name) if size == 16 else DRAW[name](size, None)


def draw(name, size, var=None):
    return solid16(name, var) if size == 16 else DRAW[name](size, var)


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
        dx, dy = 1.5, -2.0                       # the lid lifts 2 and moves 1.5 right, clear of the body
        r = R_RECT
        q = s_ / 2
        body = rpoly([(x0, y0), (x0 + q, y0), (x0 + q, y0 + q), (x0 + s_, y0 + q), (x0 + s_, y0 + s_), (x0, y0 + s_)],
                     [r, r, 0, r, r, r])
        hx, hy = x0 + q + dx, y0 + dy
        lid = rotate_pen(rrect_c(hx, hy, hx + q, hy + q, r), turn, hx, hy)
        k = 5.25 if var is None else float(var)
        reg = rrect(x0 + s_ - 0.25 - k, y0 + 0.25, k, k, r)
        return build([body, lid], [(x0 + q, y0 + q, NODE_R)], reg, size)
    if size == 24:
        body = rpoly([(5, 6), (11, 6), (11, 12), (17, 12), (17, 18), (5, 18)], 0)
        hx, hy, q = 12.5, 4.0, 4.5             # a lid a little smaller than the notch, so it sits over its gap
        lid = rotate_pen(rrect_c(hx, hy, hx + q, hy + q, 0), -15, hx, hy)
        reg = rrect(12, 6, 5, 4, 1)
        return build([body, lid], [(11, 12, 2)], reg, size)
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
    if size == 24:
        st = rpoly([(3, 20), (3, 15), (9, 15), (9, 10), (15, 10), (15, 5), (21, 5), (21, 20)], 0)
        reg = rrect(15, 5, 6, 5, 1)
        return build([st], [(9, 12, 2)], reg, size)
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
    if size == 24:
        left = half_pen(12, 12, 9, 8, -1, 1.0)
        right = half_pen(12, 12, 9, 8, +1, 1.0)
        reg = rrect(11, 9, 2, 5, 1)
        return build([left, right], [(12, 12, 2)], reg, size, off=(0.0, 2.0))
    raise KeyError(size)


@icon
def act(size, var=None):
    """A door swung open on its floor: the leaf comes toward the reader in perspective, the frame
    runs over the opening only and down the far jamb, held apart from the leaf as Direction A
    draws it. The node is the handle. The red lights the lower half of the doorway."""
    if size == "display":
        floor = line_c((2.75, 21), (21.25, 21))
        leaf = rpoly([(4, 21), (4, 2.75), (10.5, 5), (10.5, 21)], [0, 1.0, 0.6, 0], closed=False)
        frame = rpoly([(14.5, 5), (19.5, 5), (19.5, 21)], [0, R_RECT, 0], closed=False)
        wr = 4.5
        reg = rrect(14.5, 10.5, wr, 9.0, R_RECT)
        return build([leaf, frame, floor], [(7.25, 12, NODE_R)], reg, size)
    if size == 24:
        floor = line_c((3, 21), (21, 21))
        leaf = rpoly([(3, 21), (3, 3), (10, 5), (10, 21)], 0, closed=False)
        frame = rpoly([(13, 5), (19, 5), (19, 21)], 0, closed=False)
        reg = rrect(14, 10, 4, 9, 1)
        return build([leaf, frame, floor], [(6.5, 12, 2)], reg, size)
    raise KeyError(size)


@icon
def ballot(size, var=None):
    """A ballot box with a slot across its top face. The paper stands well out of it, about 7 units
    above the box, and sinks into the slot. The printed oval sits in the paper's upper half; the red
    is the voter's mark, which covers the oval to its outer edge and prints off register, staying on
    the paper."""
    if size == "display":
        top, slot = 11.5, 14.0
        p0, p1, pt = 6.5, 17.5, 4.5
        box = rpoly([(p0, top), (3.75, top), (3.75, 20), (20.25, 20), (20.25, top), (p1, top)],
                    [0, R_RECT, R_RECT, R_RECT, R_RECT, 0], closed=False)
        slot_l = line_c((p0, slot), (p1, slot))
        paper = rpoly([(p0, slot), (p0, pt), (p1, pt), (p1, slot)], [0, 1.0, 1.0, 0], closed=False)
        ox0, oy0, ox1, oy1 = 9.75, 6.75, 14.75, 9.75
        oval = rpoly([(ox0, oy0), (ox1, oy0), (ox1, oy1), (ox0, oy1)], (oy1 - oy0) / 2)
        reg = stadium(ox0 - 0.75, oy0 - 0.75, ox1 + 0.75, oy1 + 0.75)
        return build([box, slot_l, paper, oval], [], reg, size)
    if size == 24:
        box = rpoly([(6, 11), (3, 11), (3, 20), (21, 20), (21, 11), (18, 11)], 0, closed=False)
        slot_l = line_c((6, 14), (18, 14))
        paper = rpoly([(6, 14), (6, 4), (18, 4), (18, 14)], 0, closed=False)
        oval = rpoly([(10, 7), (14, 7), (14, 10), (10, 10)], 1.5)
        reg = rrect(9, 6, 6, 5, 2.5)
        return build([box, slot_l, paper, oval], [], reg, size)
    raise KeyError(size)


@icon
def bill(size, var=None):
    """A page with a folded corner and lines of text; the red highlights the last line."""
    if size == "display":
        page = rpoly([(5.75, 3), (14, 3), (18.25, 7.25), (18.25, 21), (5.75, 21)], [R_RECT, 0, 0, R_RECT, R_RECT])
        fold = rpoly([(14, 3), (14, 7.25), (18.25, 7.25)], [0, 1.0, 0], closed=False)
        t1 = line_c((9, 8.5), (11, 8.5))
        t2 = line_c((9, 11.5), (14.75, 11.5))
        t3 = line_c((9, 14.5), (14.75, 14.5))
        reg = stadium(9.25, 12.25, 17.25, 16.75)
        return build([page, fold, t1, t2, t3], [], reg, size)
    if size == 24:
        page = rpoly([(6, 3), (14, 3), (18, 7), (18, 21), (6, 21)], 0)
        fold = rpoly([(14, 3), (14, 7), (18, 7)], 0, closed=False)
        t1 = line_c((9, 9), (11, 9))
        t2 = line_c((9, 12), (15, 12))
        t3 = line_c((9, 15), (15, 15))
        reg = rrect(10, 12, 7, 4, 2)
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
    if size == 24:
        # one pixel higher than the display master, so the table no longer sits on Track's base line
        head = ring_c(16, 6, 3)
        shoulders = arc_c(16, 19, 5, 180, 360)
        table = line_c((3, 19), (21, 19))
        cx, cy, cw, cl, ang = 8.5, 11.5, 4.0, 5.5, 45
        cap = tilted_stadium_pen(cx, cy, cw, cl, ang)
        u = (math.sin(math.radians(ang)), -math.cos(math.radians(ang)))
        foot = (cx - u[0] * cl / 2, cy - u[1] * cl / 2)
        neck = rpoly([foot, (6, 14.25), (6, 19)], [0, 1.0, 0], closed=False)
        reg = tilted_stadium(cx, cy, cw, cl, ang)
        return build([head, shoulders, table, cap, neck], [], reg, size)
    raise KeyError(size)


@icon
def housing(size, var=None):
    """A house with a pitched roof; its door opens the base line. The red fills the doorway."""
    if size == "display":
        house = rpoly([(9.75, 20), (3.5, 20), (3.5, 12), (12, 3.5), (20.5, 12), (20.5, 20), (14.25, 20)],
                      [0, R_RECT, 0.6, 1.0, 0.6, R_RECT, 0], closed=False)
        door = rpoly([(9.75, 20), (9.75, 14), (14.25, 14), (14.25, 20)], [0, 1.0, 1.0, 0], closed=False)
        reg = rrect(9.75, 14, 3.5, 6, 1.0)
        return build([house, door], [], reg, size)
    if size == 24:
        house = rpoly([(9, 20), (3, 20), (3, 12), (12, 3), (21, 12), (21, 20), (15, 20)], 0, closed=False)
        door = rpoly([(9, 20), (9, 14), (15, 14), (15, 20)], 0, closed=False)
        reg = rrect(9, 14, 5, 6, 1)
        return build([house, door], [], reg, size)
    raise KeyError(size)


@icon
def money(size, var=None):
    """A banknote filling the landscape keyline, 20 by 16, with tight 1-unit corners, its disc 2
    units left of center and one short bar at the bottom right, so it shares no mirror symmetry
    with Connect. The red fills the disc."""
    if size == "display":
        note = rrect_c(2.75, 4.75, 21.25, 19.25, 0.25)
        disc = ring_c(10, 12, 2.75)
        bar = line_c((16.75, 16), (18.25, 16))
        reg = circle(10, 12, 2.75)
        return build([note, disc, bar], [], reg, size)
    if size == 24:
        note = rrect_c(3, 5, 21, 19, 0)
        disc = ring_c(10, 12, 3)
        bar = line_c((17, 16), (18, 16))
        reg = circle(10, 12, 3)
        return build([note, disc, bar], [], reg, size)
    raise KeyError(size)


@icon
def loop(size, var=None):
    """A closed ring with three stations evenly spaced and one arrowhead on the ring between each
    pair, set just short of the station it arrives at, all turning clockwise, as the hinge
    diagram's arcs do. A closed ring with three stations breaks the two-arrow pattern that
    reload, sync, undo and redo share. The red fills the top station, where a reform acts."""
    if size == "display":
        cx, cy, R, rn, rr, arm = 12.0, 12.5, 7.25, 2.0, 2.5, 2.5
    elif size == 24:
        cx, cy, R, rn, rr, arm = 12.0, 13.0, 7.0, 2.0, 2.0, 2.0
    else:
        raise KeyError(size)
    if isinstance(var, dict):
        cx, cy, R, rn, rr, arm = (var.get(k, v) for k, v in (("cx", cx), ("cy", cy), ("R", R), ("rn", rn), ("rr", rr), ("arm", arm)))
    ring = ring_c(cx, cy, R)
    pos = {a: (cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (-90, 30, 150)}
    heads = []
    clear = 1.25 if size == "display" else 1.5      # the tip stops this far short of the next station
    for nxt, r_next in ((30, rn), (150, rn), (270, rr)):
        heads += _arrow_on_arc((cx, cy), R, nxt - math.degrees((r_next + clear) / R), +1, arm)
    discs = [(pos[-90][0], pos[-90][1], rr), (pos[30][0], pos[30][1], rn), (pos[150][0], pos[150][1], rn)]
    reg = circle(pos[-90][0], pos[-90][1], rr)
    return build([ring] + heads, discs, reg, size)


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
