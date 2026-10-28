"""Concept 2, Moving part: the ten display masters (design director, Phase 2 round two).

Each subject is built from two to four solid pieces held apart by one constant cut. The red piece
is the one that moves: the ballot paper entering the box, the door leaf, the lifted corner, the coin
leaving the hand. The Charcoal pieces hold the structure around it.

Grid: round one's 24-unit grid, 2-unit padding, live area 2 to 22; keylines circle 20, square 18,
portrait 16 by 20, landscape 20 by 16.
Display master: cut 1.5 units; convex corners 1-unit radius; concave corners square; counters 3
units or more; one 2-unit bar where the subject needs a line.

Every icon returns a dict:
  pieces  list of (role, d) with role "ink" or "accent", each d one piece as SVG path data
  open    the accent piece moved one step further open (the current item in a row), same form
  reason  the one-line reason for its red
Pieces are kept separate so the board can show the cut, the red turned to ink and the red removed.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_moving_geom as G  # noqa: E402
from icons_r2_moving_geom import circle_d, contour_d, ellipse_d, path_d, pt_on, rect, rect_hole, ring_sector  # noqa: E402,F401

CUT = 1.5
R1 = 1.0           # outer corner radius in the display master
NODE_R = 2.0       # the pillar node, 4 units across
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
    "connect": "The bridge is red: it is the ground a reader builds between two halves.",
    "act": "The door leaf is red: it is the part you push to walk through.",
    "ballot": "The paper is red: it is your vote, on its way into the box.",
    "bill": "The folded corner is red: it is the page being turned, the bill in motion.",
    "testify": "The sound is red: it is the testimony leaving the speaker.",
    "housing": "The door is red: it is the way in, the part a resident opens.",
    "money": "The coin is red: it is the money leaving the hand.",
    "loop": "One arc is red: it is the link where a reform acts on the loop.",
}


def _arc_pt(c, R, deg):
    return pt_on(c[0], c[1], R, deg)


# ====================================================================== pillar marks

def explain(step=0.0):
    """A square broken open, its top-right quarter lifted out. The L holds the node at the hinge;
    the lifted corner is red and moves up and to the right."""
    x0, y0, S = 3.5, 7.5, 13.0
    q = S / 2
    ic = (x0 + S - q, y0 + q)                     # the L's inner corner, (10, 14)
    nc = (12.0, 12.0)                              # node on the center line
    Rb = NODE_R + CUT                              # clear radius around the node
    # L: bite where the circle crosses x = 10 (top arm) and y = 14 (right arm)
    dy = math.sqrt(Rb ** 2 - (nc[0] - ic[0]) ** 2)
    dx = math.sqrt(Rb ** 2 - (ic[1] - nc[1]) ** 2)
    L = [(x0, y0, R1), (ic[0], y0, R1), (ic[0], nc[1] - dy, R1), ("arc", *nc, False), (nc[0] + dx, ic[1], R1),
         (x0 + S, ic[1], R1), (x0 + S, y0 + S, R1), (x0, y0 + S, R1)]
    D = 4.0 + step / math.sqrt(2)
    lx, ly = ic[0] + D, y0 - D                     # lid top-left
    lid_items = []
    # lid bottom-left corner is within the clear radius only while D is small
    corner = (lx, ly + q)
    if math.dist(corner, nc) < Rb:
        ey = nc[1] - math.sqrt(Rb ** 2 - (lx - nc[0]) ** 2)       # on the lid's left edge
        ex = nc[0] + math.sqrt(Rb ** 2 - (ly + q - nc[1]) ** 2)   # on the lid's bottom edge
        lid_items = [(lx, ly, R1), (lx + q, ly, R1), (lx + q, ly + q, R1), (ex, ly + q, R1), ("arc", *nc, False), (lx, ey, R1)]
    else:
        lid_items = rect(lx, ly, q, q, R1)
    node = circle_d(*nc, NODE_R)
    return [("ink", contour_d(L) + node), ("accent", contour_d(lid_items))]


def track(step=0.0):
    """Three stages on a rising stair, raised. The lower two stages are one Charcoal stair; the
    top stage is red and rises. The node sits at the meeting point between the reached stage and
    the next one, on the center line."""
    base = 19.5
    x1, x2 = 7.5, 14.0                 # step 1 to 2, step 2 to the cut
    y1, y2 = 14.5, 10.5                # tops of step 1 and 2
    x3 = x2 + CUT                      # top stage left edge
    y3 = 5.0 - step
    nc = (x2 + CUT / 2, 12.0)
    Rb = NODE_R + CUT
    # step 2's top-right corner is bitten by the circle around nc: the bite starts on the tread
    # when the circle reaches above it, and ends on the step's right edge
    h = math.sqrt(Rb ** 2 - (x2 - nc[0]) ** 2)
    if nc[1] - h < y2:
        xa = nc[0] - math.sqrt(Rb ** 2 - (nc[1] - y2) ** 2)
        stair = [(2, base, R1), (2, y1, R1), (x1, y1, 0), (x1, y2, R1), (xa, y2, R1),
                 ("arc", *nc, False), (x2, nc[1] + h, R1), (x2, base, R1)]
    else:
        stair = [(2, base, R1), (2, y1, R1), (x1, y1, 0), (x1, y2, R1), (x2, y2, R1), (x2, nc[1] - h, R1),
                 ("arc", *nc, False), (x2, nc[1] + h, R1), (x2, base, R1)]
    h3 = math.sqrt(Rb ** 2 - (x3 - nc[0]) ** 2)
    top = [(x3, y3, R1), (22, y3, R1), (22, base - step, R1), (x3, base - step, R1), (x3, nc[1] + h3, R1),
           ("arc", *nc, False), (x3, nc[1] - h3, R1)]
    return [("ink", contour_d(stair) + circle_d(*nc, NODE_R)), ("accent", contour_d(top))]


def _reverse(items):
    """Reverse a contour's direction, keeping arcs and corner radii with their points."""
    pts, arcs = [], {}
    for it in items:
        if it[0] == "arc":
            arcs[len(pts) - 1] = it
        else:
            pts.append(it)
    n = len(pts)
    out = []
    for k in range(n):
        i = (n - k) % n
        out.append(pts[i])
        # the edge from pts[i] to pts[i-1] in the new order is the old edge i-1 -> i reversed
        j = (i - 1) % n
        if j in arcs:
            a = arcs[j]
            out.append(("arc", a[1], a[2], not a[3]))
    return out


def connect(step=0.0):
    """One circle in two halves held apart, and a red bridge laid across the gap, with the node
    knocked out of its middle."""
    c = (12.0, 12.0)
    R = 10.25                          # overshoots the 20-unit circle keyline
    g = 3.0                            # half the gap between the halves
    bw, bh = 7.0 + step, 5.0           # bridge half length, height
    by0, by1 = c[1] - bh / 2, c[1] + bh / 2
    nx = c[0] - bw                     # bridge left end
    # halves with a notch where the bridge enters, cut CUT around it
    ny0, ny1 = by0 - CUT, by1 + CUT
    nxl = nx - CUT
    def half(side):
        s = -1 if side == "L" else 1
        fx = c[0] + s * g                              # flat side
        hy = math.sqrt(R ** 2 - (fx - c[0]) ** 2)
        if side == "L":
            # clockwise: from flat-bottom, around the left arc to flat-top, then down the flat side with the notch
            return [(fx, c[1] + hy, R1), ("arc", *c, True), (fx, c[1] - hy, R1), (fx, ny0, R1), (nxl, ny0, 0),
                    (nxl, ny1, 0), (fx, ny1, R1)]
        return [(fx, c[1] - hy, R1), ("arc", *c, True), (fx, c[1] + hy, R1), (fx, ny1, R1), (24 - nxl, ny1, 0),
                (24 - nxl, ny0, 0), (fx, ny0, R1)]
    bridge = contour_d(rect(nx, by0, 2 * bw, bh, R1)) + circle_d(*c, 1.5, hole=True)
    return [("ink", contour_d(half("L"))), ("ink", contour_d(half("R"))), ("accent", bridge)]


def act(step=0.0):
    """A door swung open. The frame holds still; the leaf is red, swung toward you, with its
    handle knocked out on the center line."""
    hx = 11.0                          # hinge edge of the leaf
    fx = 4.0 - step                    # free edge, nearer the viewer
    top_free, top_hinge = 2.0, 5.0
    leaf = [(fx, top_free, R1), (hx, top_hinge, R1), (hx, 22, R1), (fx, 22, R1)]
    handle = circle_d(fx + 2.5, 12.0, 1.25, hole=True)
    lx = hx + CUT
    frame = [(lx, 2, R1), (21.5, 2, R1), (21.5, 22, R1), (18.5, 22, R1), (18.5, 5, 0), (lx, 5, R1)]
    return [("ink", contour_d(frame)), ("accent", contour_d(leaf) + handle)]


# ====================================================================== topic and atlas symbols

def ballot(step=0.0):
    """A box with a slot in its lid and a marked paper going in. The paper is red."""
    bx0, bx1 = 3.5, 20.5
    body = rect(bx0, 13.5, bx1 - bx0, 7.5, R1)
    lid_y, lid_h = 10.0, 2.0
    px0, px1 = 9.0, 15.0
    lidL = rect(bx0, lid_y, px0 - CUT - bx0, lid_h, R1)
    lidR = rect(px1 + CUT, lid_y, bx1 - px1 - CUT, lid_h, R1)
    paper = rect(px0, 3.0 - step, px1 - px0, lid_y + lid_h - 3.0, R1)
    mark = ellipse_d(12.0, 6.25 - step, 1.6, 1.15, hole=True)
    return [("ink", contour_d(body)), ("ink", contour_d(lidL) + contour_d(lidR)), ("accent", contour_d(paper) + mark)]


def bill(step=0.0):
    """A page with a folded corner and lines of text. The fold is red."""
    x0, x1, y0, y1 = 5.0, 19.0, 2.5, 21.5
    f = 6.5                                        # fold size
    fx, fy = x1 - f, y0 + f                         # inner corner of the fold
    page = [(x0, y0, R1), (fx - CUT, y0, R1), (fx - CUT, fy + CUT, 0), (x1, fy + CUT, R1), (x1, y1, R1), (x0, y1, R1)]
    lines = ""
    for (ly, lx1) in ((13.0, 16.0), (16.25, 16.0), (19.5 - 0.0, 12.5)):
        pass
    rows = [(12.5, 16.0), (15.5, 16.0), (18.5, 12.0)]
    for ly, lx1 in rows:
        lines += contour_d(rect_hole(8.0, ly, lx1 - 8.0, CUT))
    s = step / math.sqrt(2)
    fold = [(fx + s, y0 - s, R1), (x1 + s, fy - s, R1), (fx + s, fy - s, 0 if s == 0 else R1)]
    fold = [(fx + s, y0 - s, R1), (x1 + s, fy - s, R1), (fx + s, fy - s, R1)]
    return [("ink", contour_d(page) + lines), ("accent", contour_d(fold))]


def testify(step=0.0):
    """A person speaking at a microphone. The person is Charcoal; the sound is a red quarter ring
    before the mouth, nested around the head across the cut."""
    hc = (7.5, 10.5)
    hr = 3.5
    head = circle_d(*hc, hr)
    sh_c, sh_r = (7.5, 21.0), 5.5
    shoulders = [(sh_c[0] - sh_r, sh_c[1], R1), ("arc", *sh_c, True), (sh_c[0] + sh_r, sh_c[1], R1)]
    r_in = hr + CUT + step
    sound = ring_sector(*hc, r_in + 2.0, r_in, -45, 45, R1)
    mic = [(16.0, 5.5, R1), ("arc", 17.75, 7.25, True), (19.5, 7.25, 0)]
    # microphone: a stadium head on a 2-unit stem to a foot
    mx0, mx1 = 16.25, 19.75
    mtop, mbot = 4.0, 12.5
    mr = (mx1 - mx0) / 2
    mic = [(mx0, mtop + mr, 0), ("arc", mx0 + mr, mtop + mr, True), (mx1, mtop + mr, 0), (mx1, mbot - mr, 0),
           ("arc", mx0 + mr, mbot - mr, True), (mx0, mbot - mr, 0)]
    stem = rect(17.0, mbot + CUT, 2.0, 21.0 - mbot - CUT - 2.0, 0)
    foot = rect(14.5, 19.0, 7.0, 2.0, R1)
    stand = [(17.0, mbot + CUT, R1), (19.0, mbot + CUT, R1), (19.0, 19.0, 0), (21.5, 19.0, R1), (21.5, 21.0, R1),
             (14.5, 21.0, R1), (14.5, 19.0, R1), (17.0, 19.0, 0)]
    return [("ink", head), ("ink", contour_d(shoulders)), ("ink", contour_d(mic) + contour_d(stand)), ("accent", contour_d(sound))]


def housing(step=0.0):
    """A house with a pitched roof and a door. The door is red."""
    rx0, rx1, eave = 3.0, 21.0, 11.5
    apex = (12.0, eave - (rx1 - rx0) / 2)
    roof = [(rx0, eave, R1), apex + (R1,), (rx1, eave, R1)]
    bx0, bx1, by0, by1 = 4.5, 19.5, eave + CUT, 21.0
    dx0, dx1, dy0 = 7.5, 11.5, 15.5
    body = [(bx0, by0, R1), (bx1, by0, R1), (bx1, by1, R1), (dx1 + CUT, by1, R1), (dx1 + CUT, dy0 - CUT, 0),
            (dx0 - CUT, dy0 - CUT, 0), (dx0 - CUT, by1, R1), (bx0, by1, R1)]
    window = rect_hole(14.0, 15.5, 3.0, 3.0)
    door = rect(dx0 - step, dy0, dx1 - dx0, by1 - dy0, R1)
    return [("ink", contour_d(roof)), ("ink", contour_d(body) + contour_d(window)), ("accent", contour_d(door))]


def money(step=0.0):
    """A hand and a coin. A Charcoal coin rests on the fingers; the red coin leaves the hand."""
    cuff = rect(2.0, 13.0, 3.0, 8.5, R1)
    hx0 = 5.0 + CUT
    # fingers: a stadium from the cuff to the right; thumb: a stadium standing up at the left
    fy0, fy1 = 17.0, 21.0
    hand = [(hx0, 12.5, R1), (hx0 + 3.5, 12.5, R1), (hx0 + 3.5, fy0, 0), (20.0, fy0, 0), ("arc", 20.0, (fy0 + fy1) / 2, True),
            (20.0, fy1, 0), (hx0, fy1, R1)]
    coin_ink = circle_d(15.0, 13.0, 2.5)
    coin_red = circle_d(16.5 + step * 0.6, 6.0 - step * 0.8, 3.5)
    return [("ink", contour_d(cuff)), ("ink", contour_d(hand)), ("ink", coin_ink), ("accent", coin_red)]


def loop(step=0.0):
    """Two nodes joined by two arrowed arcs into a loop. The upper arc and its arrowhead are red."""
    c = (12.0, 12.0)
    Rm, w = 7.5, 2.0
    nr = 2.5
    clear = nr + CUT
    span = math.degrees(2 * math.asin(clear / (2 * Rm)))
    head_len, head_half = 4.0, 2.6

    def arm(a_tail, a_tip):
        # body from tail to the arrowhead base, then a triangle to the tip
        a_base = a_tip - math.degrees(head_len / Rm)
        body = ring_sector(*c, Rm + w / 2, Rm - w / 2, a_tail, a_base, R1)
        # rebuild: the arrowhead base corners sit on the radial line at a_base
        bo, bi = pt_on(*c, Rm + head_half, a_base), pt_on(*c, Rm - head_half, a_base)
        to, ti = pt_on(*c, Rm + w / 2, a_base), pt_on(*c, Rm - w / 2, a_base)
        tip = pt_on(*c, Rm, a_tip)
        p_tail_o, p_tail_i = pt_on(*c, Rm + w / 2, a_tail), pt_on(*c, Rm - w / 2, a_tail)
        items = [(*p_tail_o, R1), ("arc", *c, True), (*to, 0), (*bo, R1), (*tip, R1), (*bi, R1), (*ti, 0),
                 ("arc", *c, False), (*p_tail_i, R1)]
        return contour_d(items)

    top = arm(180 + span, 360 - span)
    bottom = arm(span, 180 - span)
    nodes = circle_d(c[0] - Rm, c[1], nr) + circle_d(c[0] + Rm, c[1], nr)
    return [("ink", nodes), ("ink", bottom), ("accent", top)]


DRAW = {"explain": explain, "track": track, "connect": connect, "act": act, "ballot": ballot, "bill": bill,
        "testify": testify, "housing": housing, "money": money, "loop": loop}


def pieces(name, step=0.0):
    return DRAW[name](step)
