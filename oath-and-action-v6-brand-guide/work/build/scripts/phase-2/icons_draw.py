"""The three icon concepts on eight test icons (design director, Phase 2, October 28, 2026).

Grid: 24 units, 1 unit = 1 px at 24 px, 2-unit padding, live area 2 to 22. Keylines: circle 20
across, square 18, portrait 16 by 20, landscape 20 by 16. The 16 px masters are separate drawings
on a 16-unit grid with 1-unit padding, live area 1 to 15.

Every drawing returns layers:
  ink    the icon's one-color drawing, with the node's seat already clear
  seat   the 1-unit ring around the node. Clear everywhere except one case: in a row on Newsprint
         the current item's red takes a 1 px Charcoal keyline, and the seat fills with Charcoal
  node   the hinge node, the icon's one red element
  center the node center

The node is Direction A's shared node (G1-01, Y1): a 4 px disc in a 1 px seat at 24 px, centered
on a pixel corner; a 3 px disc in a 1 px seat at 16 px, centered on a pixel center.
Red marks where a person steps in: the handle, the mark on the ballot, the step where a reform acts.

Concepts
  A  Line. One 2 px stroke at 24 and at 16 px, flat (butt) ends, mitered corners. Lines stop at the
     node's seat with flat ends, so the node sits off the line. At 16 px a counter narrower than
     2 px closes into a solid.
  B  Flat. Solid pieces from a small kit (square, bar, disc, half disc, quarter ring, triangle,
     stadium), square corners, pieces held apart by 1 px cuts. The node sits in a 1 px seat cut
     into a piece or between pieces.
  C  One drawing in two cuts. Direction A's geometry as closed outlines with square corners.
     Line cut: each outline as a 2 px wall inside its edge. Flat cut: each outline filled. A part
     with no inside keeps 2 px in both cuts, except the loop arc and the lens handle, which grow
     inward to 3 px in the flat cut. The node never bites a wall: it sits in a counter, clear of
     every shape, or in a flat-ended gap in a wall.
     The line cut starts at 24 px; 16 px uses the flat cut.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_geom as g  # noqa: E402
from icons_geom import circle, intersect, minus, poly, rect, ring, rrect, sector, stroke_path, union, wall_poly  # noqa: E402
import pathops as po  # noqa: E402

ICONS = ["explain", "track", "connect", "act", "ballot", "money", "loop", "search"]
LABELS = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
          "money": "Campaign money", "loop": "Feedback loop", "search": "Search"}
FILE_NAME = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
             "money": "Campaign-Money", "loop": "Feedback-Loop", "search": "Search"}
CLASS = {"explain": "Pillar mark", "track": "Pillar mark", "connect": "Pillar mark", "act": "Pillar mark",
         "ballot": "Topic symbol", "money": "Topic symbol", "loop": "Atlas symbol", "search": "Interface icon"}
STEP_IN = {
    "explain": "where the corner lifts away, so you can see inside",
    "track": "the stage a decision has reached",
    "connect": "the common ground between two halves",
    "act": "the handle, where you take hold",
    "ballot": "the mark you make on your ballot",
    "money": "the coin that changes hands",
    "loop": "the step where a reform acts on the loop",
    "search": "the one thing the lens is looking for",
}
CONCEPTS = ["A", "B", "C"]
CUTS = {"A": ["line"], "B": ["flat"], "C": ["line", "flat"]}
SIZES_FOR = {("A", "line"): (16, 24), ("B", "flat"): (16, 24), ("C", "line"): (24,), ("C", "flat"): (16, 24)}
NODE = {24: (2.0, 3.0), 16: (1.5, 2.5)}  # node radius, seat radius
VARIANT = {"track": "bead", "act": "handle", "money": "pair", "loop": "chevron"}


# ---------------------------------------------------------------- shared helpers

def _ln(pts, w=2.0, cap="butt", join="miter", closed=False):
    segs = [("M", *pts[0])] + [("L", *p) for p in pts[1:]]
    if closed:
        segs.append(("Z",))
    return stroke_path(segs, w, cap, join)


def _arc(cx, cy, r, a0, a1, w=2.0, cap="butt"):
    """A 2 px arc built from two concentric circles, so every edge is a true circle."""
    if cap == "butt":
        return sector(cx, cy, r + w / 2, r - w / 2, a0, a1)
    return stroke_path([("A", cx, cy, r, a0, a1)], w, cap, "miter")


def pixel_shape(shape, size, keep_out=None):
    """Hint a shape to whole pixels: keep each pixel the shape covers by half or more, drop any
    pixel that reaches into keep_out (the node's seat) by more than 15 percent, then trace the kept
    pixels as one outline. Straight edges already on whole pixels come through unchanged."""
    b = shape.bounds
    kept = []
    for y in range(max(0, int(b[1]) - 1), min(size, int(b[3]) + 2)):
        row = []
        for x in range(max(0, int(b[0]) - 1), min(size, int(b[2]) + 2)):
            cell = rect(x, y, 1, 1)
            if g.area(intersect(shape, cell)) >= 0.5 and (keep_out is None or g.area(intersect(keep_out, cell)) <= 0.15):
                row.append(x)
        # merge runs into rectangles
        i = 0
        while i < len(row):
            j = i
            while j + 1 < len(row) and row[j + 1] == row[j] + 1:
                j += 1
            kept.append(rect(row[i], y, row[j] - row[i] + 1, 1))
            i = j + 1
    return union(*kept) if kept else g.empty()


def hinted(lay, size):
    """The same drawing with its ink hinted to whole pixels; the node stays a true disc."""
    cx, cy = lay["center"]
    seat = circle(cx, cy, NODE[size][1])
    out = dict(lay)
    out["ink"] = pixel_shape(g.union(lay["ink"], g.empty()), size, keep_out=seat)
    return out


def layers(ink, cx, cy, size, cut_seat=True):
    rn, rs = NODE[size]
    seat_c = circle(cx, cy, rs)
    node = circle(cx, cy, rn)
    return {"ink": minus(ink, seat_c) if cut_seat else ink, "seat": minus(seat_c, node), "node": node,
            "center": (cx, cy)}


def _stroke_outline(shape, w, join="round"):
    p = po.Path()
    shape.draw(p.getPen())
    jm = {"round": po.LineJoin.ROUND_JOIN, "miter": po.LineJoin.MITER_JOIN}[join]
    p.stroke(w, po.LineCap.BUTT_CAP, jm, 4)
    p.convertConicsToQuads()
    return g.simplify(p)


def round_convex(shape, r):
    """Round every convex corner of a shape by radius r (morphological opening)."""
    eroded = minus(shape, _stroke_outline(shape, 2 * r))
    return union(eroded, _stroke_outline(eroded, 2 * r))


def wall(shape, w=2.0):
    """The shape drawn as a wall of width w inside its outline, with mitered inner corners."""
    return intersect(shape, _stroke_outline(shape, 2 * w, "miter"))


def _tangent(cx, cy, r, theta):
    t = math.radians(theta)
    return (cx + r * math.cos(t), cy + r * math.sin(t)), (-math.sin(t), math.cos(t)), (math.cos(t), math.sin(t))


def arrowhead(cx, cy, r, theta, length, half):
    """A solid triangle whose base is centered on a circle of radius r at angle theta (degrees,
    clockwise on screen), pointing clockwise along the tangent."""
    (px, py), (tx, ty), (nx, ny) = _tangent(cx, cy, r, theta)
    return poly((px + nx * half, py + ny * half), (px + tx * length, py + ty * length), (px - nx * half, py - ny * half))


def chevron(cx, cy, r, theta, arm, w=2.0):
    """An open arrowhead of two 2 px strokes, its tip at the arc end, arms back at 45 degrees."""
    (px, py), (tx, ty), (nx, ny) = _tangent(cx, cy, r, theta)
    tip = (px, py)
    a = (tip[0] - tx * arm * 0.7071 + nx * arm * 0.7071, tip[1] - ty * arm * 0.7071 + ny * arm * 0.7071)
    b = (tip[0] - tx * arm * 0.7071 - nx * arm * 0.7071, tip[1] - ty * arm * 0.7071 - ny * arm * 0.7071)
    return _ln([a, tip, b], w)


def stadium(x, y, w, h):
    return rrect(x, y, w, h, h / 2)


def pixel_diag(x0, y0, n, w=2):
    """A 45-degree bar on whole pixels: n squares of w px, each one pixel down and right."""
    out = rect(x0, y0, w, w)
    for i in range(1, n):
        out = union(out, rect(x0 + i, y0 + i, w, w))
    return out


def diag_bar(r_start, cx, cy, length, w):
    """A bar at 45 degrees down and right, starting r_start from (cx, cy)."""
    s = r_start / math.sqrt(2)
    return g.transform(g.rot(rect(0, -w / 2, length, w), 45, 0, 0), 1, cx + s, cy + s)


# ====================================================================== Concept A, line

def A_24(name, var=None):
    var = var or VARIANT.get(name)
    if name == "explain":
        sq = _ln([(10, 8), (4, 8), (4, 20), (16, 20), (16, 14)])
        lid = _ln([(14, 4), (20, 4), (20, 10)])
        return layers(union(sq, lid), 12, 12, 24)
    if name == "track":
        floor = _ln([(2, 21), (22, 21)])
        lo = _ln([(3, 20), (3, 17), (6, 17), (6, 12), (9, 12)])
        hi = _ln([(15, 12), (18, 12), (18, 7), (21, 7), (21, 20)])
        return layers(union(floor, lo, hi), 12, 12, 24)
    if name == "connect":
        left = minus(intersect(circle(12, 12, 10), rect(0, 0, 8, 24)), intersect(circle(12, 12, 8), rect(0, 0, 6, 24)))
        right = minus(intersect(circle(12, 12, 10), rect(16, 0, 8, 24)), intersect(circle(12, 12, 8), rect(18, 0, 6, 24)))
        return layers(union(left, right), 12, 12, 24)
    if name == "act":
        leaf = wall_poly([(2, 5), (12, 8.75), (12, 22), (2, 22)])
        frame = union(_ln([(2, 3), (22, 3)]), _ln([(21, 4), (21, 22)]))
        return layers(union(leaf, frame), 7, 12, 24)
    if name == "ballot":
        box = _ln([(6, 14), (3, 14), (3, 21), (21, 21), (21, 14), (18, 14)])
        paper = _ln([(8, 13), (8, 4), (16, 4), (16, 13)])
        return layers(union(box, paper), 12, 9, 24)
    if name == "money":
        if var == "pair":
            front = ring(15, 10, 7, 5)
            back = minus(ring(9, 14, 7, 5), circle(15, 10, 8))
            return layers(union(front, back), 15, 10, 24)
        coin = ring(15, 9, 7, 5)
        stack = union(_ln([(2, 18), (11, 18)]), _ln([(2, 21), (15, 21)]))
        return layers(union(coin, stack), 15, 9, 24)
    if name == "loop":
        end = 450 - 33
        arc = _arc(12, 11, 8, 90 + 25, end)
        head = chevron(12, 11, 8, end, 4.0)
        return layers(union(arc, head), 12, 19, 24)
    if name == "search":
        lens = ring(10, 10, 8, 6)
        handle = _ln([(15.3, 15.3), (21, 21)])
        return layers(union(lens, handle), 10, 10, 24)
    raise ValueError(name)


def A_16(name, var=None):
    var = var or VARIANT.get(name)
    if name == "explain":
        sq = _ln([(5, 6), (2, 6), (2, 14), (10, 14), (10, 10)])
        lid = _ln([(9, 2), (13, 2), (13, 6)])
        return layers(union(sq, lid), 7.5, 7.5, 16)
    if name == "track":
        floor = _ln([(1, 14), (15, 14)])
        lo = _ln([(2, 13), (2, 11), (4, 11), (4, 8), (5, 8)])
        hi = _ln([(10, 8), (11, 8), (11, 4), (14, 4), (14, 13)])
        return layers(union(floor, lo, hi), 7.5, 7.5, 16)
    if name == "connect":
        left = intersect(circle(7.5, 7.5, 6.5), rect(0, 0, 5, 16))
        right = intersect(circle(7.5, 7.5, 6.5), rect(10, 0, 6, 16))
        return layers(union(left, right), 7.5, 7.5, 16)
    if name == "act":
        leaf = wall_poly([(1, 4), (10, 7.0), (10, 15), (1, 15)])
        frame = union(_ln([(1, 2), (15, 2)]), _ln([(14, 3), (14, 15)]))
        return layers(union(leaf, frame), 5.5, 10.5, 16)
    if name == "ballot":
        box = _ln([(3, 10), (3, 14), (14, 14), (14, 10)])
        paper = _ln([(5, 9), (5, 2), (12, 2), (12, 9)])
        return layers(union(box, paper), 8.5, 5.5, 16)
    if name == "money":
        if var == "pair":
            front = ring(10.5, 6.5, 4.5, 2.5)
            back = minus(ring(5.5, 10.5, 4.5, 2.5), circle(10.5, 6.5, 5.5))
            return layers(union(front, back), 10.5, 6.5, 16)
        coin = ring(10.5, 5.5, 4.5, 2.5)
        stack = union(_ln([(1, 11), (7, 11)]), _ln([(1, 14), (10, 14)]))
        return layers(union(coin, stack), 10.5, 5.5, 16)
    if name == "loop":
        end = 450 - 44
        arc = _arc(7.5, 7.5, 5.5, 90 + 32, end)
        head = chevron(7.5, 7.5, 5.5, end, 3.0)
        return layers(union(arc, head), 7.5, 12.5, 16)
    if name == "search":
        lens = ring(6.5, 6.5, 5.5, 3.5)
        handle = pixel_diag(10, 10, 4)
        return layers(union(lens, handle), 6.5, 6.5, 16)
    raise ValueError(name)


# ====================================================================== Concept B, flat kit

def B_24(name, var=None):
    var = var or VARIANT.get(name)
    if name == "explain":
        body = union(minus(rect(3, 7, 14, 14), rect(10, 7, 7, 7)), rect(14, 3, 7, 7))
        return layers(body, 12, 12, 24)
    if name == "track":
        body = union(rect(2, 15, 6, 5), rect(8, 11, 8, 9), rect(16, 7, 6, 13))
        return layers(body, 12, 12, 24)
    if name == "connect":
        body = minus(circle(12, 12, 10), rect(8, 0, 8, 24))
        return layers(body, 12, 12, 24)
    if name == "act":
        leaf = poly((2, 5), (12, 8.75), (12, 22), (2, 22))
        frame = union(rect(2, 2, 20, 2), rect(20, 2, 2, 20))
        return layers(union(leaf, frame), 7, 12, 24)
    if name == "ballot":
        box = minus(rect(2, 15, 20, 6), rect(6, 15, 12, 2))
        paper = rect(7, 3, 10, 13)
        return layers(union(box, paper), 12, 9, 24)
    if name == "money":
        coin = circle(15, 9, 7)
        stack = minus(union(stadium(2, 18, 14, 4), stadium(3, 13, 12, 4)), circle(15, 9, 8))
        return layers(union(coin, stack), 15, 9, 24)
    if name == "loop":
        end = 450 - 64
        band = sector(12, 11, 9, 5, 90 + 26, end)
        head = intersect(arrowhead(12, 11, 7, end, 5.0, 4.6), rect(2, 2, 20, 20))
        return layers(union(band, head), 12, 18, 24)
    if name == "search":
        lens = ring(10, 10, 8, 4)
        handle = diag_bar(9, 10, 10, 6.4, 3)
        return layers(union(lens, handle), 10, 10, 24)
    raise ValueError(name)


def B_16(name, var=None):
    var = var or VARIANT.get(name)
    if name == "explain":
        body = union(minus(rect(1, 4, 10, 10), rect(6, 4, 5, 5)), rect(9, 1, 5, 5))
        return layers(body, 7.5, 7.5, 16)
    if name == "track":
        body = union(rect(1, 10, 4, 4), rect(5, 7, 6, 7), rect(11, 4, 4, 10))
        return layers(body, 7.5, 7.5, 16)
    if name == "connect":
        body = minus(circle(7.5, 7.5, 6.5), rect(5, 0, 5, 16))
        return layers(body, 7.5, 7.5, 16)
    if name == "act":
        leaf = poly((1, 4), (9, 6.5), (9, 15), (1, 15))
        frame = union(rect(1, 1, 14, 2), rect(13, 1, 2, 14))
        return layers(union(leaf, frame), 4.5, 9.5, 16)
    if name == "ballot":
        box = minus(rect(1, 10, 14, 5), rect(3, 10, 10, 1))
        paper = rect(4, 1, 7, 10)
        return layers(union(box, paper), 7.5, 4.5, 16)
    if name == "money":
        coin = circle(10.5, 5.5, 4.5)
        stack = minus(union(stadium(1, 12, 10, 3), stadium(2, 8, 8, 3)), circle(10.5, 5.5, 5.5))
        return layers(union(coin, stack), 10.5, 5.5, 16)
    if name == "loop":
        end = 450 - 52
        band = sector(7.5, 7.5, 6.5, 4.5, 90 + 32, end)
        head = intersect(arrowhead(7.5, 7.5, 5.5, end, 3.8, 3.2), rect(1, 1, 14, 14))
        return layers(union(band, head), 7.5, 12.5, 16)
    if name == "search":
        lens = ring(6.5, 6.5, 5.0, 2.5)
        handle = pixel_diag(9, 9, 4, 3)
        return layers(union(lens, handle), 6.5, 6.5, 16)
    raise ValueError(name)


# ====================================================================== Concept C, two cuts

def _C24(name, cut):
    """Closed outlines, open parts for this cut, node center, and the flat-ended gap the line cut
    needs where the node sits in a wall. Both cuts share one silhouette: the flat cut fills each
    outline. Open lines keep 2 px, except the loop's arc and the lens handle, which carry the whole
    subject and grow inward to 3 px in the flat cut, so their outer edges stay put."""
    flat = cut == "flat"
    if name == "explain":
        L = minus(rect(3, 8, 14, 14), rect(10, 8, 7, 7))
        lid = rect(15, 2, 7, 7)
        return [L, lid], [], (13, 12), None
    if name == "track":
        st = union(rect(2, 15, 6, 5), rect(8, 11, 8, 9), rect(16, 7, 6, 13))
        return [st], [], (12, 12), rect(9, 10, 6, 4)
    if name == "connect":
        left = intersect(circle(12, 12, 10), rect(0, 0, 8, 24))
        right = intersect(circle(12, 12, 10), rect(16, 0, 8, 24))
        return [left, right], [], (12, 12), None
    if name == "act":
        leaf = poly((2, 5), (12, 8.75), (12, 22), (2, 22))
        frame = union(_ln([(2, 3), (22, 3)]), _ln([(21, 4), (21, 22)]))
        return [leaf], [frame], (7, 12), None
    if name == "ballot":
        box = minus(rect(3, 14, 18, 8), rect(6, 14, 12, 2))
        paper = rect(7, 3, 10, 12)
        return [box, paper], [], (12, 9), None
    if name == "money":
        front = circle(15, 10, 7)
        back = minus(circle(9, 14, 7), circle(15, 10, 8))
        return [front, back], [], (15, 10), None
    if name == "loop":
        end = 450 - 33
        arc = sector(12, 11, 9, 6 if flat else 7, 90 + 25, end)
        head = chevron(12, 11, 8, end, 4.0)
        if flat:
            (px, py), (tx, ty), (nx, ny) = _tangent(12, 11, 8, end)
            k = 4.0 * 0.7071
            head = union(head, poly((px, py), (px - tx * k + nx * k, py - ty * k + ny * k), (px - tx * k - nx * k, py - ty * k - ny * k)))
        return [], [arc, head], (12, 19), None
    if name == "search":
        lens = circle(10, 10, 8)
        handle = _ln([(15.3, 15.3), (20.9, 20.9)], 3 if flat else 2)
        return [lens], [handle], (10, 10), None
    raise ValueError(name)


def C_24(name, cut, var=None):
    shapes, opens, (cx, cy), gap = _C24(name, cut)
    parts = shapes if cut == "flat" else [wall(s, 2.0) for s in shapes]
    ink = union(*parts, *opens)
    if cut == "line" and gap is not None:
        ink = minus(ink, gap)
    return layers(ink, cx, cy, 24)


def C_16(name, cut="flat", var=None):
    """16 px flat cut on whole pixels. The line cut starts at 24 px."""
    if name == "explain":
        return layers(union(minus(rect(1, 5, 10, 10), rect(6, 5, 5, 5)), rect(10, 1, 5, 5)), 8.5, 8.5, 16)
    if name == "track":
        return layers(union(rect(1, 10, 4, 4), rect(5, 7, 6, 7), rect(11, 4, 4, 10)), 7.5, 7.5, 16)
    if name == "connect":
        return layers(minus(circle(7.5, 7.5, 6.5), rect(5, 0, 5, 16)), 7.5, 7.5, 16)
    if name == "act":
        leaf = poly((1, 4), (9, 6.5), (9, 15), (1, 15))
        frame = union(rect(1, 1, 14, 2), rect(13, 1, 2, 14))
        return layers(union(leaf, frame), 4.5, 9.5, 16)
    if name == "ballot":
        box = minus(rect(1, 10, 14, 5), rect(3, 10, 10, 1))
        return layers(union(box, rect(4, 1, 7, 10)), 7.5, 4.5, 16)
    if name == "money":
        front = circle(10.5, 6.5, 4.5)
        back = minus(circle(5.5, 10.5, 4.5), circle(10.5, 6.5, 5.5))
        return layers(union(front, back), 10.5, 6.5, 16)
    if name == "loop":
        end = 450 - 52
        arc = sector(7.5, 7.5, 6.5, 4.5, 90 + 32, end)
        head = intersect(arrowhead(7.5, 7.5, 5.5, end, 3.8, 3.2), rect(1, 1, 14, 14))
        return layers(union(arc, head), 7.5, 12.5, 16)
    if name == "search":
        return layers(union(circle(6.5, 6.5, 5.0), pixel_diag(9, 9, 4, 3)), 6.5, 6.5, 16)
    raise ValueError(name)


# ====================================================================== dispatch

def master(concept, cut, name, size):
    """The shipped 16 or 24 px master: the drawing with its ink hinted to whole pixels."""
    return hinted(draw(concept, cut, name, size), size)


def display(concept, cut, name):
    """The display master for 48 px and up: the unhinted 24-unit drawing."""
    return draw(concept, cut, name, 24)


def draw(concept, cut, name, size, var=None):
    if concept == "A":
        return A_24(name, var) if size == 24 else A_16(name, var)
    if concept == "B":
        return B_24(name, var) if size == 24 else B_16(name, var)
    if concept == "C":
        if size == 24:
            return C_24(name, cut, var)
        return C_16(name, "flat", var)
    raise ValueError(concept)


def scaled(lay, s):
    return {k: (g.transform(v, s) if k != "center" else (v[0] * s, v[1] * s)) for k, v in lay.items()}
