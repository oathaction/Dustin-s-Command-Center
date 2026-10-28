"""Concept 2, Moving part: the ten display masters, stage 2 (design director, Phase 2 round two).

Each subject is built from two to four solid pieces held apart by one constant cut. The red piece is
the one that moves: the lid lifting, the top stage rising, the door leaf swinging, the ballot going in,
the second banknote changing hands. The Charcoal pieces hold the structure around it. The stage 1
drawings, as the creative director reviewed them, are kept in icons_r2_moving_draw_stage1.py.

Grid: round one's 24-unit grid, 2-unit padding, live area 2 to 22; keylines circle 20, square 18,
portrait 16 by 20, landscape 20 by 16. Straight edges stay inside the live area; round forms
overshoot by 0.25 units at most.
Display master: cut 1.5 units; convex corners 1-unit radius; concave corners square; counters 3
units or more. The red piece is the one piece allowed off the 90 degree grid, turned up to 20 degrees.

The pillar node is 3 units across; with the cut around it, its clear zone is 6 units, Direction A's
seat. In Explain, Act and Track the node is the hinge or joint the red piece moves about.

pieces(name, step) returns [(role, d)] with role "ink" or "accent" and d one piece as SVG path data.
step moves the red piece along its path: 0 for the standalone master, STEP (2 units) for the current
item in a row. CUT and R1 are read at call time, so the hinting script can redraw a subject with the
24 px cut (2 px) and square corners.
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
STEP = 2.0         # how far the red piece moves for the current item in a row
BITE_EXTRA = 0.0   # added to the bite's radius when a hinted master draws the node as a square
OVR = {}           # per-size drawing overrides from the hinting script (act_pin, connect_R)


def clear():
    """Radius of the bite a piece takes around the node: the node, the cut and, for a square node,
    the extra that keeps the node's corners a full cut from the bite."""
    return NODE_R + CUT + BITE_EXTRA


ICONS = ["explain", "track", "connect", "act", "ballot", "bill", "testify", "housing", "money", "loop"]
LABELS = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
          "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign money", "loop": "Feedback loop"}
FILE_NAME = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
             "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign-Money", "loop": "Feedback-Loop"}
CLASS = {"explain": "Pillar mark", "track": "Pillar mark", "connect": "Pillar mark", "act": "Pillar mark",
         "ballot": "Topic symbol", "bill": "Topic symbol", "testify": "Topic symbol", "housing": "Topic symbol",
         "money": "Topic symbol", "loop": "Atlas symbol"}
REASON = {
    "explain": "The lid is red: it is the part you lift to see inside, turning on its hinge.",
    "track": "The top stage is red: it is the stage the decision rises to next, lifting from its seat.",
    "connect": "The bridge is red: it is the ground that spans the gap and joins the two halves.",
    "act": "The door leaf is red: it is the part you push to walk through. The node is its hinge.",
    "ballot": "The paper is red: it is your marked vote, on its way into the box.",
    "bill": "The folded corner is red: it is the page being turned, the bill in motion.",
    "testify": "The sound is red: it is the testimony leaving the speaker. The person stays Charcoal.",
    "housing": "The door is red: it is the way in, the part a resident opens.",
    "money": "The second note is red: it is the money changing hands, sliding out from behind.",
    "loop": "The return is red: it is the feedback, the link that brings the effect back to its cause.",
}
STORY = {
    "explain": "We open the workings of a decision so you can see inside.",
    "track": "We follow a decision as it moves up through its stages.",
    "connect": "We build the ground between people and the officials who serve them.",
    "act": "We give you a door you can walk through and a practical way to take part.",
}


def _y_on(c, r, x, sign):
    """The y where the circle (c, r) crosses the vertical line x; sign -1 for the upper crossing."""
    return c[1] + sign * math.sqrt(max(0.0, r * r - (x - c[0]) ** 2))


def _x_on(c, r, y, sign):
    return c[0] + sign * math.sqrt(max(0.0, r * r - (y - c[1]) ** 2))


def _line_circle(p, q, c, r):
    """Parameters t in [0, 1] where the segment pq crosses the circle (c, r)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    fx, fy = p[0] - c[0], p[1] - c[1]
    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    cc = fx * fx + fy * fy - r * r
    disc = b * b - 4 * a * cc
    if disc < 0:
        return []
    s = math.sqrt(disc)
    return [t for t in ((-b - s) / (2 * a), (-b + s) / (2 * a)) if 0 <= t <= 1]


def _rot(pts, piv, deg):
    """Rotate points about piv; negative degrees turn counterclockwise on screen."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(piv[0] + (x - piv[0]) * ca - (y - piv[1]) * sa, piv[1] + (x - piv[0]) * sa + (y - piv[1]) * ca) for x, y in pts]


# ====================================================================== pillar marks

def explain(step=0.0):
    """A square broken open, its top-right quarter a lid. The lid turns 20 degrees on the corner it
    shares with the square's top edge, so the gaps along its hinge side open as wedges from 1.5 units,
    and it wraps the node across the cut where it passes over the open corner."""
    x0, y0, S = 3.5, 7.5, 13.0
    q = S / 2
    ic = (x0 + S - q, y0 + q)                          # the L's inner corner
    nc = (ic[0] + 1.75, ic[1] - 1.75)                   # the node, at the hinge of the open corner
    C = clear()
    L = [(x0, y0, R1), (ic[0], y0, R1), (ic[0], _y_on(nc, C, ic[0], -1), R1), ("arc", *nc, False),
         (_x_on(nc, C, ic[1], +1), ic[1], R1), (x0 + S, ic[1], R1), (x0 + S, y0 + S, R1), (x0, y0 + S, R1)]
    lift = 0.75
    hinge = (ic[0] + CUT, y0 - lift)
    ang = 20.0 + math.degrees(step / (q * math.sqrt(2)))   # the far corner moves `step` units further open
    A, B, Cc, Dd = _rot([(hinge[0], hinge[1]), (hinge[0] + q, hinge[1]), (hinge[0] + q, hinge[1] + q), (hinge[0], hinge[1] + q)], hinge, -ang)
    sq = contour_d([(*A, R1), (*B, R1), (*Cc, R1), (*Dd, R1)])
    t1 = _line_circle(Cc, Dd, nc, C)
    t2 = _line_circle(Dd, A, nc, C)
    if math.dist(Dd, nc) < C and t1 and t2:
        P1 = (Cc[0] + (Dd[0] - Cc[0]) * t1[0], Cc[1] + (Dd[1] - Cc[1]) * t1[0])
        P2 = (Dd[0] + (A[0] - Dd[0]) * t2[-1], Dd[1] + (A[1] - Dd[1]) * t2[-1])
        lid = contour_d([(*A, R1), (*B, R1), (*Cc, R1), (*P1, R1), ("arc", *nc, False), (*P2, R1)])
    else:
        import pathops
        from icons_geom import d_of
        lid = d_of(pathops.simplify(pathops.op(G.to_pathops(sq), G.to_pathops(circle_d(*nc, C)), pathops.PathOp.DIFFERENCE), clockwise=True))
    return [("ink", contour_d(L)), ("ink", circle_d(*nc, NODE_R)), ("accent", lid)]


def track(step=0.0):
    """Three stages of equal rise and run, climbing from bottom left to top right on the landscape
    keyline. The node rests in the joint between the first and second stages. The top stage is a red
    block of the full rise; the stair under it drops by the cut, so the block's foot lines up with the
    second tread and the block rests across the cut. In the row state it rises."""
    x0, x1, top, base = 3.5, 20.5, 4.0, 20.0
    u, r = (x1 - x0 - CUT) / 3, (base - top) / 3
    xs = [x0, x0 + u, x0 + 2 * u]
    t1, t2 = base - r, base - 2 * r
    nc = (xs[1] - NODE_R - CUT, t1 - NODE_R - CUT)
    stair = [(xs[0], base, R1), (xs[0], t1, R1), (xs[1], t1, 0), (xs[1], t2, R1), (xs[2], t2, R1), (xs[2], t2 + CUT, 0),
             (x1, t2 + CUT, R1), (x1, base, R1)]
    red = rect(xs[2] + CUT, top - step, u, t2 - top, R1)
    return [("ink", contour_d(stair)), ("ink", circle_d(*nc, NODE_R)), ("accent", contour_d(red))]


def connect(step=0.0):
    """One circle in two halves, held 5 units apart. A red bar bridges the gap, its ends resting in
    shallow slots in both halves across the cut, with the node knocked out at its center. In the
    row state the bridge slides 2 units down into place."""
    c = (12.0, 12.0)
    R = OVR.get("connect_R", 9.75)
    g = 2.5                         # half the gap
    bar, reach = 4.5, 1.5
    hy = math.sqrt(R * R - g * g)
    hb = bar / 2
    bx = g + reach
    cy = c[1] + step

    def seat(side):
        s = -1 if side == "L" else 1
        fx = c[0] + s * g
        ex = c[0] + s * (bx + CUT)
        y0, y1 = cy - hb - CUT, cy + hb + CUT
        if side == "L":
            return [(fx, y0, R1), (ex, y0, 0), (ex, y1, 0), (fx, y1, R1)]
        return [(fx, y1, R1), (ex, y1, 0), (ex, y0, 0), (fx, y0, R1)]

    L = [(c[0] - g, c[1] + hy, R1), ("arc", *c, True), (c[0] - g, c[1] - hy, R1)] + seat("L")
    Rr = [(c[0] + g, c[1] - hy, R1), ("arc", *c, True), (c[0] + g, c[1] + hy, R1)] + seat("R")
    bridge = contour_d(rect(c[0] - bx, cy - hb, 2 * bx, bar, R1)) + circle_d(c[0], cy, NODE_R, hole=True)
    return [("ink", contour_d(L)), ("ink", contour_d(Rr)), ("accent", bridge)]


def act(step=0.0):
    """A door swung well open toward you. The Charcoal frame carries the structure: a full lintel,
    the far jamb and a floor bar. The red leaf is narrow, as a door swung far open looks from the
    front, and the node is its hinge pin on the center line. In the row state the leaf swings 2 units
    further."""
    lint = (2.0, 4.5)
    jx = 19.0
    floor_t = 20.0
    frame = [(2.5, lint[0], R1), (21.5, lint[0], R1), (21.5, floor_t - CUT, R1), (jx, floor_t - CUT, R1), (jx, lint[1], 0), (2.5, lint[1], R1)]
    flo = rect(2.5, floor_t, 19.0, 22.0 - floor_t, R1)
    hx = 10.0
    fx = hx - 3.5 - step
    # The leaf's top corner sits a cut below the lintel; its fillet lets it rise 0.6 closer.
    tf = lint[1] + CUT - (0.6 if R1 else 0.0) + 0.15 * step
    nc = (hx + OVR.get("act_pin", 1.5), 12.0)
    C = clear()
    bite_top = _y_on(nc, C, hx, -1)
    drop = min(2.5, bite_top - tf - 0.5)      # the slant of the leaf's top edge, kept clear of the bite
    leaf = [(fx, tf, R1), (hx, tf + drop, R1), (hx, bite_top, R1), ("arc", *nc, False), (hx, _y_on(nc, C, hx, +1), R1),
            (hx, floor_t - CUT, R1), (fx, floor_t - CUT, R1)]
    return [("ink", contour_d(frame)), ("ink", contour_d(flo)), ("ink", circle_d(*nc, NODE_R)), ("accent", contour_d(leaf))]


# ====================================================================== topic and atlas symbols

def ballot(step=0.0):
    """A box with a slot in its top edge and a marked paper going in. The paper is red, its mark a
    ballot oval knocked out. Its lower third sinks into the slot and behind the box's face; in the row
    state it sinks 2 units deeper."""
    bx0, bx1, top, bot = 3.5, 20.5, 11.0, 20.5
    pw = 5.0
    depth = 2.75
    sx0, sx1 = 12 - pw / 2 - CUT, 12 + pw / 2 + CUT
    floor = top + depth
    box = [(bx0, top, R1), (sx0, top, R1), (sx0, floor, 0), (sx1, floor, 0), (sx1, top, R1), (bx1, top, R1), (bx1, bot, R1), (bx0, bot, R1)]
    ptop = 3.0 + step
    pb = floor - CUT
    paper = contour_d(rect(12 - pw / 2, ptop, pw, pb - ptop, R1))
    mark = ellipse_d(12.0, ptop + CUT + 1.1, 1.5, 1.1, hole=True)
    return [("ink", contour_d(box)), ("accent", paper + mark)]


def bill(step=0.0):
    """A page with a folded corner and lines of text. The fold is red and nests in the page's notch
    across the cut. Its top point stays 1.5 units below the page's top edge, so it reads as a fold and
    never as a bookmark flag. In the row state the corner peels 2 units outward."""
    x0, x1, y0, y1 = 5.5, 18.75, 2.25, 22.0
    f = 7.75
    fx, fy = x1 - f, y0 + f
    page = [(x0, y0, R1), (fx - CUT, y0, R1), (fx - CUT, fy + CUT, 0), (x1, fy + CUT, R1), (x1, y1, R1), (x0, y1, R1)]
    lines = ""
    first = fy + CUT + CUT
    for i, lx1 in enumerate((16.0, 16.0, 12.0)):
        lines += contour_d(rect_hole(8.0, first + 3 * i, lx1 - 8.0, CUT))
    fold = [(fx + step, y0 + CUT, R1), (x1 + step, fy, R1), (fx + step, fy, R1)]
    return [("ink", contour_d(page) + lines), ("accent", contour_d(fold))]


def testify(step=0.0):
    """A person speaking at a microphone. The person is Charcoal. The sound is a red quarter ring
    before the mouth, nested around the head across the cut; the microphone stands close, its head
    at mouth height. In the row state the sound turns upward along its ring."""
    sc, sr = OVR.get("testify_sc", (6.75, 21.25)), OVR.get("testify_sr", 5.0)
    hr = OVR.get("testify_hr", 3.75)
    hc = (6.75, sc[1] - sr - CUT - hr)
    head = circle_d(*hc, hr)
    shoulders = [(sc[0] - sr, sc[1], R1), ("arc", *sc, True), (sc[0] + sr, sc[1], R1)]
    r_in = hr + CUT
    ring_w = OVR.get("testify_ring_w", 2.0)
    rot = math.degrees(step / (r_in + ring_w / 2))
    sound = ring_sector(*hc, r_in + ring_w, r_in, -45 - rot, 45 - rot, R1)
    mw = 4.0
    mr = mw / 2
    mx0 = hc[0] + r_in + ring_w + CUT
    mt = hc[1] - 2.25
    mb = mt + 7.0
    cx = mx0 + mr
    sx0, sx1 = cx - 1.25, cx + 1.25
    yj = mb - mr + math.sqrt(mr * mr - 1.25 ** 2)
    mic = [(mx0, mt + mr, 0), ("arc", cx, mt + mr, True), (mx0 + mw, mt + mr, 0), (mx0 + mw, mb - mr, 0), ("arc", cx, mb - mr, True),
           (sx1, yj, 0), (sx1, 19.0, 0), (cx + 2.75, 19.0, R1), (cx + 2.75, 21.0, R1),
           (cx - 2.5, 21.0, R1), (cx - 2.5, 19.0, R1), (sx0, 19.0, 0), (sx0, yj, 0),
           ("arc", cx, mb - mr, True), (mx0, mb - mr, 0)]
    return [("ink", head), ("ink", contour_d(shoulders)), ("ink", contour_d(mic)), ("accent", contour_d(sound))]


def housing(step=0.0):
    """A house with a pitched roof over its eaves and a door at its center. The door is red. In the row
    state the door swings open, its free edge moving 2 units toward its hinge."""
    rx0, rx1, eave = 3.0, 21.0, OVR.get("housing_eave", 11.0)
    apex = (12.0, eave - (rx1 - rx0) / 2)
    roof = [(rx0, eave, R1), (*apex, R1), (rx1, eave, R1)]
    bx0, bx1 = OVR.get("housing_body", (5.5, 18.5))
    by0, by1 = eave + CUT, 21.0
    dx0, dx1 = OVR.get("housing_door", (10.0, 14.0))
    dy0 = OVR.get("housing_door_top", 15.5)
    body = [(bx0, by0, R1), (bx1, by0, R1), (bx1, by1, R1), (dx1 + CUT, by1, R1), (dx1 + CUT, dy0 - CUT, 0),
            (dx0 - CUT, dy0 - CUT, 0), (dx0 - CUT, by1, R1), (bx0, by1, R1)]
    door = rect(dx0, dy0, dx1 - dx0 - step, by1 - dy0, R1)
    return [("ink", contour_d(roof)), ("ink", contour_d(body)), ("accent", contour_d(door))]


def _note(cx, cy, w, h, ang, r):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca, r) for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]


def money(step=0.0):
    """Campaign money as banknotes. A Charcoal landscape note with its center disc and two corner
    marks knocked out; a second note in red slides up and out from behind it across the cut, turned
    12 degrees, so it shows along the front note's top and past its right end. The red note is the
    money changing hands."""
    import pathops
    from icons_geom import d_of
    w, h, cy, fcx = 16.0, 9.5, 13.0, 11.25
    front = contour_d(_note(fcx, cy, w, h, 0, R1)) + circle_d(fcx, cy, 2.75, hole=True)
    front += contour_d(rect_hole(fcx - w / 2 + 1.75, cy - h / 2 + 1.75, 2.5, CUT))
    front += contour_d(rect_hole(fcx + w / 2 - 1.75 - 2.5, cy + h / 2 - 1.75 - CUT, 2.5, CUT))
    # The row state lifts the note 1.6 units, short of the full 2, so its corner stays in the live area.
    back = contour_d(_note(fcx + 2.25, cy - OVR.get("money_lift", 3.5) - min(step, 1.6), w, h, -12.0, R1))
    grown = G.to_pathops(contour_d(_note(fcx, cy, w + 2 * CUT, h + 2 * CUT, 0, R1 + CUT)))
    red = pathops.simplify(pathops.op(G.to_pathops(back), grown, pathops.PathOp.DIFFERENCE), clockwise=True)
    return [("ink", front), ("accent", d_of(red))]


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
    """One arrowed arc, clockwise from a_from to a_to (degrees). Its tail and its tip sit exactly one
    cut from the two nodes. The arrowhead is a triangle whose base is radial and whose tip runs along
    the tangent, so its two sides are mirror images. Its three corners take a half-unit radius, an
    optical correction: a 1-unit radius blunts an acute point."""
    clear_ = nr + CUT

    def tail_gap(a):
        return _seg_dist(tail_node, pt_on(*c, Rm - w / 2, a), pt_on(*c, Rm + w / 2, a))

    a_tail = _solve(tail_gap, a_from, a_from + 90, clear_)

    def head_pts(a):
        t = math.radians(a)
        tx, ty = -math.sin(t), math.cos(t)
        base = pt_on(*c, Rm, a)
        tip = (base[0] + tx * hl, base[1] + ty * hl)
        return pt_on(*c, Rm + hh, a), tip, pt_on(*c, Rm - hh, a)

    def head_gap(a):
        bo, tip, bi = head_pts(a)
        return min(_seg_dist(head_node, bo, tip), _seg_dist(head_node, tip, bi))

    a_base = _solve(head_gap, a_to - 90, a_to, clear_)
    bo, tip, bi = head_pts(a_base)
    to, ti = pt_on(*c, Rm + w / 2, a_base), pt_on(*c, Rm - w / 2, a_base)
    p_o, p_i = pt_on(*c, Rm + w / 2, a_tail), pt_on(*c, Rm - w / 2, a_tail)
    r_ = min(R1, 0.5) if R1 else 0
    return contour_d([(*p_o, R1), ("arc", *c, True), (*to, 0), (*bo, r_), (*tip, r_), (*bi, r_), (*ti, 0),
                      ("arc", *c, False), (*p_i, R1)])


def loop(step=0.0):
    """A feedback loop that is not a half-turn: two nodes on the vertical center line, a straight
    Charcoal forward link with a solid arrowhead down the axis, and the return as a red arc with its
    arrowhead bowing out to the left and back up into the first node. The return is the feedback. In
    the row state the return bows 2 units further out."""
    cx, ty, by = 13.0, OVR.get("loop_ty", 4.75), OVR.get("loop_by", 19.25)
    nr = OVR.get("loop_nr", 3.0)
    top, bot = (cx, ty), (cx, by)
    bar, hl, hh = 3.0, 3.25, 3.25
    y_from, y_tip = ty + nr + CUT, by - nr - CUT
    y_base = y_tip - hl
    r_ = min(R1, 0.5) if R1 else 0
    fw = [(cx + bar / 2, y_from, R1), (cx + bar / 2, y_base, 0), (cx + hh, y_base, r_), (cx, y_tip, r_), (cx - hh, y_base, r_),
          (cx - bar / 2, y_base, 0), (cx - bar / 2, y_from, R1)]
    half = (by - ty) / 2
    sag = hh + CUT + 1.25 + step                                   # how far the return bows out from the axis
    k = (half * half - sag * sag) / (2 * sag)           # center offset to the right of the axis
    Rm = sag + k
    c = (cx + k, (ty + by) / 2)
    a_bot = math.degrees(math.atan2(bot[1] - c[1], bot[0] - c[0]))
    a_top = math.degrees(math.atan2(top[1] - c[1], top[0] - c[0])) % 360
    ret = _arrow_arm(c, Rm, 2.0, 3.5, 2.5, bot, top, nr, a_bot, a_top)
    nodes = circle_d(*top, nr) + circle_d(*bot, nr)
    return [("ink", nodes), ("ink", contour_d(fw)), ("accent", ret)]


DRAW = {"explain": explain, "track": track, "connect": connect, "act": act, "ballot": ballot, "bill": bill,
        "testify": testify, "housing": housing, "money": money, "loop": loop}


def pieces(name, step=0.0):
    return DRAW[name](step)


class spec:
    """Context manager that redraws with another cut, corner radius, node radius and bite extra,
    for the hinted masters."""

    def __init__(self, cut, r1, node_r=None, bite_extra=0.0, ovr=None):
        self.cut, self.r1, self.node_r, self.extra, self.ovr = cut, r1, node_r, bite_extra, dict(ovr or {})

    def __enter__(self):
        global CUT, R1, NODE_R, BITE_EXTRA, OVR
        self.old = (CUT, R1, NODE_R, BITE_EXTRA, OVR)
        CUT, R1, BITE_EXTRA, OVR = self.cut, self.r1, self.extra, self.ovr
        if self.node_r is not None:
            NODE_R = self.node_r
        return self

    def __exit__(self, *a):
        global CUT, R1, NODE_R, BITE_EXTRA, OVR
        CUT, R1, NODE_R, BITE_EXTRA, OVR = self.old
