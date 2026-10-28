"""Concept 2, Moving part: the ten STAGE 1 display masters, kept as reviewed (design director, Phase 2 round two).

This is the drawing the creative director reviewed at stage 1. Stage 2 redraws live in icons_r2_moving_draw.py.

Each subject is built from two to four solid pieces held apart by one constant cut. The red piece
is the one that moves: the ballot paper entering the box, the door leaf, the lifted corner, the coin
leaving the hand. The Charcoal pieces hold the structure around it.

Grid: round one's 24-unit grid, 2-unit padding, live area 2 to 22; keylines circle 20, square 18,
portrait 16 by 20, landscape 20 by 16.
Display master: cut 1.5 units; convex corners 1-unit radius; concave corners square; counters 3
units or more; one 2-unit bar where the subject needs a line.

The pillar node is 3 units across. With the 1.5-unit cut around it, its clear zone is 6 units across,
the same footprint as Direction A's 4-unit node in its 1-unit seat.

pieces(name, step) returns a list of (role, d): role "ink" or "accent", d one piece as SVG path data.
step moves the red piece along its path (0 for the standalone master; the row state uses STEP).
Every coordinate below was placed by hand and judged at 2x.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_moving_geom as G  # noqa: E402
from icons_r2_moving_geom import circle_d, contour_d, ellipse_d, pt_on, rect, rect_hole, ring_sector  # noqa: E402,F401

CUT = 1.5
R1 = 1.0           # outer corner radius in the display master
NODE_R = 1.5       # the pillar node, 3 units across
CLEAR = NODE_R + CUT
STEP = 2.0         # how far the red piece moves for the current item in a row

ICONS = ["explain", "track", "connect", "act", "ballot", "bill", "testify", "housing", "money", "loop"]
LABELS = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
          "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign money", "loop": "Feedback loop"}
FILE_NAME = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
             "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign-Money", "loop": "Feedback-Loop"}
CLASS = {"explain": "Pillar mark", "track": "Pillar mark", "connect": "Pillar mark", "act": "Pillar mark",
         "ballot": "Topic symbol", "bill": "Topic symbol", "testify": "Topic symbol", "housing": "Topic symbol",
         "money": "Topic symbol", "loop": "Atlas symbol"}
REASON = {
    "explain": "The lifted corner is red: it is the part you raise to see inside.",
    "track": "The top stage is red: it is the stage the decision rises to next.",
    "connect": "The bridge is red: it is the ground that spans the gap between two halves.",
    "act": "The door leaf is red: it is the part you push to walk through.",
    "ballot": "The paper is red: it is your marked vote, on its way into the box.",
    "bill": "The folded corner is red: it is the page being turned, the bill in motion.",
    "testify": "The sound is red: it is the testimony leaving the speaker. The person stays Charcoal.",
    "housing": "The door is red: it is the way in, the part a resident opens.",
    "money": "The rising coin is red: it is the money leaving the hand.",
    "loop": "One arc is red: it is the link where a reform acts on the loop.",
}


def _y_on(c, r, x, sign):
    """The y where the circle (c, r) crosses the vertical line x; sign -1 for the upper crossing."""
    return c[1] + sign * math.sqrt(r * r - (x - c[0]) ** 2)


def _x_on(c, r, y, sign):
    return c[0] + sign * math.sqrt(r * r - (y - c[1]) ** 2)


# ====================================================================== pillar marks

def explain(step=0.0):
    """A square broken open, its top-right quarter lifted out. The node sits at the hinge, exactly
    between the L's inner corner and the lid's corner, and both pieces wrap it across the cut."""
    x0, y0, S = 3.5, 7.0, 13.5
    q = S / 2
    ic = (x0 + S - q, y0 + q)                       # the L's inner corner, (10.25, 13.75)
    nc = (12.0, 12.0)
    L = [(x0, y0, R1), (ic[0], y0, R1), (ic[0], _y_on(nc, CLEAR, ic[0], -1), R1), ("arc", *nc, False),
         (_x_on(nc, CLEAR, ic[1], +1), ic[1], R1), (x0 + S, ic[1], R1), (x0 + S, y0 + S, R1), (x0, y0 + S, R1)]
    D = 3.5 + step / math.sqrt(2)
    lx, ly = ic[0] + D, y0 - D
    if math.dist((lx, ly + q), nc) < CLEAR:
        lid = [(lx, ly, R1), (lx + q, ly, R1), (lx + q, ly + q, R1), (_x_on(nc, CLEAR, ly + q, +1), ly + q, R1),
               ("arc", *nc, False), (lx, _y_on(nc, CLEAR, lx, -1), R1)]
    else:
        lid = rect(lx, ly, q, q, R1)
    return [("ink", contour_d(L)), ("ink", circle_d(*nc, NODE_R)), ("accent", contour_d(lid))]


def track(step=0.0):
    """Direction A's stair (stages 2-8, 8-16, 16-22), raised to a base of 20. The node keeps Direction
    A's seat on tread 2, on the center line, moved half a unit right so both lips of the seat are 1.5 units. The top stage is a red block resting on the stair across the
    cut; it rises."""
    xs = (2.0, 8.0, 16.0, 22.0)
    base, h = 20.0, 4.0
    t1, t2 = base - h, base - 2 * h
    nc = (12.5, t2)
    stair = [(xs[0], base, R1), (xs[0], t1, R1), (xs[1], t1, 0), (xs[1], t2, R1), (nc[0] - CLEAR, t2, R1),
             ("arc", *nc, False), (nc[0] + CLEAR, t2, R1), (xs[3], t2, R1), (xs[3], base, R1)]
    rb = t2 - CUT - step
    top = rect(xs[2], rb - h, xs[3] - xs[2], h, R1)
    return [("ink", contour_d(stair)), ("ink", circle_d(*nc, NODE_R)), ("accent", contour_d(top))]


def connect(step=0.0):
    """One circle in two halves held apart. A red bridge spans the gap from flat face to flat face,
    one cut from each, with the node knocked out of its middle."""
    c = (12.0, 12.0)
    R = 10.25                      # the 20-unit circle keyline plus overshoot
    g = 4.5                        # half the gap
    hy = math.sqrt(R * R - g * g)
    left = [(c[0] - g, c[1] + hy, R1), ("arc", *c, True), (c[0] - g, c[1] - hy, R1)]
    right = [(c[0] + g, c[1] - hy, R1), ("arc", *c, True), (c[0] + g, c[1] + hy, R1)]
    w = g - CUT
    bh = 6.0
    by = c[1] - bh / 2 - step
    bridge = contour_d(rect(c[0] - w, by, 2 * w, bh, R1)) + circle_d(c[0], c[1] - step, NODE_R, hole=True)
    return [("ink", contour_d(left)), ("ink", contour_d(right)), ("accent", bridge)]


def act(step=0.0):
    """A door swung open toward you. The frame holds still: a full lintel and the far jamb. The leaf
    is red, with its handle knocked out on the center line; it swings further open."""
    lint = (2.0, 4.5)
    jx = 19.0
    frame = [(2.5, lint[0], R1), (21.5, lint[0], R1), (21.5, 22, R1), (jx, 22, R1), (jx, lint[1], 0), (2.5, lint[1], R1)]
    hx = 10.5                      # the leaf's hinge edge
    fx = 4.5 - step                # its free edge, nearer the viewer
    tf = lint[1] + CUT - 0.6           # the fillet pulls the leaf's top corner down; this keeps the cut at 1.5
    leaf = [(fx, tf, R1), (hx, tf + 3.0, R1), (hx, 22, R1), (fx, 22, R1)]
    handle = circle_d(fx + 3.0, 12.0, NODE_R, hole=True)
    return [("ink", contour_d(frame)), ("accent", contour_d(leaf) + handle)]


# ====================================================================== topic and atlas symbols

def ballot(step=0.0):
    """A box with a slot and a marked paper going in. The paper is red; its mark, a filled bubble of the
    kind many US paper ballots ask for, is knocked out with the same 1.5-unit walls as the node."""
    bx0, bx1, top, bot = 4.0, 20.0, 11.5, 21.0
    box = contour_d(rect(bx0, top, bx1 - bx0, bot - top, R1)) + contour_d(rect_hole(6.5, top + CUT, 11.0, CUT))
    px0, px1, ptop = 9.0, 15.0, 2.5
    pb = top - CUT
    paper = contour_d(rect(px0, ptop + step, px1 - px0, pb - ptop, R1))
    mark = circle_d(12.0, ptop + step + CUT + 1.5, 1.5, hole=True)
    return [("ink", box), ("accent", paper + mark)]


def bill(step=0.0):
    """A page with a folded corner and lines of text. The fold is red and nests in the page's notch."""
    x0, x1, y0, y1 = 5.5, 18.5, 2.5, 21.5
    f = 7.0
    fx, fy = x1 - f, y0 + f                         # the fold's inner corner
    page = [(x0, y0, R1), (fx - CUT, y0, R1), (fx - CUT, fy + CUT, 0), (x1, fy + CUT, R1), (x1, y1, R1), (x0, y1, R1)]
    lines = ""
    for ly, lx1 in ((12.5, 15.5), (15.5, 15.5), (18.5, 12.5)):
        lines += contour_d(rect_hole(8.5, ly, lx1 - 8.5, CUT))
    s = step / math.sqrt(2)
    fold = [(fx + s, y0 - s, R1), (x1 + s, fy - s, R1), (fx + s, fy - s, R1)]
    return [("ink", contour_d(page) + lines), ("accent", contour_d(fold))]


def testify(step=0.0):
    """A person speaking at a microphone. The person is Charcoal. The sound is a red quarter ring
    before the mouth, nested around the head across the cut; it moves outward."""
    hc, hr = (7.5, 10.5), 3.5
    head = circle_d(*hc, hr)
    sc, sr = (7.5, 21.0), 5.5
    shoulders = [(sc[0] - sr, sc[1], R1), ("arc", *sc, True), (sc[0] + sr, sc[1], R1)]
    r_in = hr + CUT + step
    sound = ring_sector(*hc, r_in + 2.25, r_in, -45, 45, R1)
    # microphone on a floor stand: a capsule on a 2-unit stem with a foot, one piece
    mx0, mx1, mt, mb = 16.25, 19.75, 4.5, 12.0
    mr = (mx1 - mx0) / 2
    cx = mx0 + mr
    sx0, sx1 = cx - 1.0, cx + 1.0
    mic = [(mx0, mt + mr, 0), ("arc", cx, mt + mr, True), (mx1, mt + mr, 0), (mx1, mb - mr, 0), ("arc", cx, mb - mr, True),
           (sx1, mb - mr + math.sqrt(mr * mr - 1.0), 0), (sx1, 19.0, 0), (21.0, 19.0, R1), (21.0, 21.0, R1),
           (15.0, 21.0, R1), (15.0, 19.0, R1), (sx0, 19.0, 0), (sx0, mb - mr + math.sqrt(mr * mr - 1.0), 0),
           ("arc", cx, mb - mr, True), (mx0, mb - mr, 0)]
    return [("ink", head), ("ink", contour_d(shoulders)), ("ink", contour_d(mic)), ("accent", contour_d(sound))]


def housing(step=0.0):
    """A house with a pitched roof and a door. The door is red; a window keeps it a house."""
    rx0, rx1, eave = 3.0, 21.0, 11.5
    apex = (12.0, eave - (rx1 - rx0) / 2)
    roof = [(rx0, eave, R1), (*apex, R1), (rx1, eave, R1)]
    bx0, bx1, by0, by1 = 4.0, 20.0, eave + CUT, 21.0
    dx0, dx1, dy0 = 7.25, 11.75, 16.0
    body = [(bx0, by0, R1), (bx1, by0, R1), (bx1, by1, R1), (dx1 + CUT, by1, R1), (dx1 + CUT, dy0 - CUT, 0),
            (dx0 - CUT, dy0 - CUT, 0), (dx0 - CUT, by1, R1), (bx0, by1, R1)]
    window = rect_hole(15.25, 15.25, 3.0, 3.0)
    door = rect(dx0 - step, dy0, dx1 - dx0, by1 - dy0, R1)
    return [("ink", contour_d(roof)), ("ink", contour_d(body) + contour_d(window)), ("accent", contour_d(door))]


def _circle_bitten(c, r, b, rb, rr=R1):
    """Contour of the disc (c, r) minus the disc (b, rb), as one clockwise contour: the long arc of c
    between the two crossings, then the bite along b. Fillets of rr at both junctions."""
    d = math.dist(c, b)
    a = (r * r - rb * rb + d * d) / (2 * d)
    h = math.sqrt(r * r - a * a)
    ex, ey = (b[0] - c[0]) / d, (b[1] - c[1]) / d
    mx, my = c[0] + ex * a, c[1] + ey * a
    p1 = (mx - ey * h, my + ex * h)
    p2 = (mx + ey * h, my - ex * h)
    # go clockwise around c from p1 to p2 the long way (away from b), then back along b counterclockwise
    a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    a2 = math.atan2(p2[1] - c[1], p2[0] - c[0])
    ab = math.atan2(b[1] - c[1], b[0] - c[0])
    # choose start so that the clockwise sweep from start to end avoids the direction of b
    def cw_contains(s, e, t):
        span = (e - s) % (2 * math.pi)
        return (t - s) % (2 * math.pi) < span
    if cw_contains(a1, a2, ab):
        p1, p2 = p2, p1
    return [(*p1, rr), ("arc", *c, True), (*p2, rr), ("arc", *b, False)]


def money(step=0.0):
    """A hand and a coin. An open hand, palm up, with the thumb raised as a quarter disc; a Charcoal coin
    rests above the palm and a second coin, red, rises from behind it, leaving the hand."""
    cuff = rect(2.0, 14.0, 2.75, 7.5, R1)
    x0, top, bot, tr = 6.25, 17.0, 21.5, 3.75
    hand = [(x0, top - tr, 0), ("arc", x0, top, True), (x0 + tr, top, 0), (19.75, top, 0),
            ("arc", 19.75, (top + bot) / 2, True), (19.75, bot, 0), (x0, bot, R1)]
    ic, ir = (13.0, 12.25), 3.0
    ang = math.atan2(-3.75, 3.75)
    dist = math.hypot(3.75, 3.75) + step
    rc = (ic[0] + dist * math.cos(ang), ic[1] + dist * math.sin(ang))
    rr = 3.0
    if math.dist(rc, ic) < rr + ir + CUT:
        red = contour_d(_circle_bitten(rc, rr, ic, ir + CUT))
    else:
        red = circle_d(*rc, rr)
    return [("ink", contour_d(cuff)), ("ink", contour_d(hand)), ("ink", circle_d(*ic, ir)), ("accent", red)]


def _seg_dist(p, a, b):
    """Distance from point p to the segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2)) if L2 else 0.0
    return math.dist(p, (a[0] + dx * t, a[1] + dy * t))


def _solve(f, lo, hi, target, n=60):
    """Bisection for f(x) = target on [lo, hi], f monotonic."""
    flo = f(lo) - target
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def _arrow_arm(c, Rm, w, hl, hh, tail_node, head_node, nr, a_from, a_to):
    """One arrowed arc of the loop, clockwise from a_from to a_to (degrees). Its tail and its tip are
    placed exactly one cut from the two nodes. The arrowhead is a triangle whose base is radial and
    whose tip runs along the tangent, so its two sides are mirror images. Its three corners take a
    half-unit radius, an optical correction: a 1-unit radius blunts an acute point."""
    clear = nr + CUT

    def tail_gap(a):
        return _seg_dist(tail_node, pt_on(*c, Rm - w / 2, a), pt_on(*c, Rm + w / 2, a))

    a_tail = _solve(tail_gap, a_from, a_from + 90, clear)

    def head_pts(a):
        t = math.radians(a)
        tx, ty = -math.sin(t), math.cos(t)
        base = pt_on(*c, Rm, a)
        tip = (base[0] + tx * hl, base[1] + ty * hl)
        return pt_on(*c, Rm + hh, a), tip, pt_on(*c, Rm - hh, a)

    def head_gap(a):
        bo, tip, bi = head_pts(a)
        return min(_seg_dist(head_node, bo, tip), _seg_dist(head_node, tip, bi))

    a_base = _solve(head_gap, a_to - 90, a_to, clear)
    bo, tip, bi = head_pts(a_base)
    to, ti = pt_on(*c, Rm + w / 2, a_base), pt_on(*c, Rm - w / 2, a_base)
    p_o, p_i = pt_on(*c, Rm + w / 2, a_tail), pt_on(*c, Rm - w / 2, a_tail)
    return contour_d([(*p_o, R1), ("arc", *c, True), (*to, 0), (*bo, 0.5), (*tip, 0.5), (*bi, 0.5), (*ti, 0),
                      ("arc", *c, False), (*p_i, R1)])


def loop(step=0.0):
    """Two nodes joined by two arrowed arcs into a loop, read top to bottom. The right arc and its
    arrowhead are red: it runs from the top node down into the bottom node. In the row state it
    pulls back from the top node along its path."""
    c = (12.0, 12.0)
    Rm, w, nr = 7.0, 2.75, 3.25
    hl, hh = 4.75, 2.75
    top, bottom = pt_on(*c, Rm, 270), pt_on(*c, Rm, 90)
    red = _arrow_arm(c, Rm, w, hl, hh, top, bottom, nr + step, 270, 450)
    ink_arc = _arrow_arm(c, Rm, w, hl, hh, bottom, top, nr, 90, 270)
    nodes = circle_d(*top, nr) + circle_d(*bottom, nr)
    return [("ink", nodes), ("ink", ink_arc), ("accent", red)]


DRAW = {"explain": explain, "track": track, "connect": connect, "act": act, "ballot": ballot, "bill": bill,
        "testify": testify, "housing": housing, "money": money, "loop": loop}


def pieces(name, step=0.0):
    return DRAW[name](step)
