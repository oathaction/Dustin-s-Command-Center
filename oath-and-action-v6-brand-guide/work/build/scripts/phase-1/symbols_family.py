"""Pillar and topic sketches for the Phase 1 symbol family board (design director).

One skeleton per pillar on a shared 24-unit grid (1 unit = 1 px at 24 px). Two
directions derive from the same skeletons:

  A  geometric solid: filled primitives with square corners; the hinge node is a
     solid dot (r 2) in a clear seat (r 3) cut into the mass.
  B  line with one accent: 2-unit monoline with round caps and joins; the hinge node
     is the one solid accent (r 3), held off the line by a 1-unit gap (r 4).

Treatments: filled, line, tile. 48 and 96 px scale the 24 master by 2 and 4. The
16 px masters are separate pixel-fit drawings of the same skeletons. Tiles at 16 px
use a 10 px micro drawing; tiles at 24, 48 and 96 px hold the 16 px master at 2/3.

Every drawing returns layers:
  body  ink of the mark, with the node seat already cut out
  seat  the clear ring around the node (filled with ink in the red accent mode so
        red never meets Newsprint)
  node  the hinge node
Proposals only. Nothing here changes a V5 master.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from symbols_geom import (circle, d_of, empty, fillet_poly, intersect, minus, poly, rect, rrect,  # noqa: E402
                          stroke_path, transform, union)

PILLARS = ["explain", "track", "connect", "act"]
DIRECTIONS = ["A", "B"]
TREATMENTS = ["filled", "line", "tile"]


def _layers(body, cx, cy, r_node, r_seat):
    seat_c = circle(cx, cy, r_seat)
    node = circle(cx, cy, r_node)
    return {"body": minus(body, seat_c), "seat": minus(seat_c, node), "node": node}


def _ln(segs, w, cap="round", join="round"):
    return stroke_path(segs, w, cap, join)


# ------------------------------------------------------------------ skeletons
# Each skeleton is a dict of named keypoints and primitives in grid units, so the
# construction drawing on the board can label them.

SKELETON_24 = {
    "explain": {
        "square": (2, 6, 16, 16), "notch": (10, 6, 8, 8), "quarter": (14, 2, 8, 8), "node": (12, 12),
        "note": "A square, broken open. Its top-right quarter lifts out along the diagonal; the node sits where it came from.",
    },
    "track": {
        "treads": [(2, 8, 17), (8, 16, 12), (16, 22, 7)], "base": 22, "node": (12, 12),
        "note": "Three stages on a rising line. The node stands on the stage a decision has reached.",
    },
    "connect": {
        "circle": (12, 12, 10), "divide": (11, 2, 2, 20), "node": (12, 12),
        "note": "One circle in two equal halves. The node holds the two sides together at the centre.",
    },
    "act": {
        "head": (12, 2, 9, 3), "jamb": (18, 2, 3, 20), "leaf": [(3, 2), (11, 5), (11, 22), (3, 22)], "node": (7, 12),
        "note": "A door swung open toward the reader. The node is the handle, the place a reader takes hold.",
    },
}

# ------------------------------------------------------------------ 24 px master

def explain_24(direction, treatment):
    if direction == "A" and treatment == "filled":
        body = union(minus(rect(2, 6, 16, 16), rect(10, 6, 8, 8)), rect(14, 2, 8, 8))
        return _layers(body, 12, 12, 2, 3)
    if direction == "A" and treatment == "line":
        body = union(_ln([("M", 3, 7), ("L", 9, 7), ("L", 9, 15), ("L", 17, 15), ("L", 17, 21), ("L", 3, 21), ("Z",)], 2, "square", "miter"),
                     _ln([("M", 15, 3), ("L", 21, 3), ("L", 21, 9), ("L", 15, 9), ("Z",)], 2, "square", "miter"))
        return _layers(body, 12, 12, 2, 3)
    if direction == "B" and treatment == "line":
        body = union(_ln([("M", 3, 7), ("L", 9, 7), ("L", 9, 15), ("L", 17, 15), ("L", 17, 21), ("L", 3, 21), ("Z",)], 2),
                     _ln([("M", 15, 3), ("L", 21, 3), ("L", 21, 9), ("L", 15, 9), ("Z",)], 2))
        return _layers(body, 12, 12, 3, 4)
    if direction == "B" and treatment == "filled":
        sq = union(rrect(2, 6, 8, 16, 2), rrect(2, 14, 16, 8, 2))
        body = union(sq, rrect(14, 2, 8, 8, 2))
        return _layers(body, 12, 12, 3, 4)
    raise ValueError


def track_24(direction, treatment):
    stairs = union(rect(2, 17, 6, 5), rect(8, 12, 8, 10), rect(16, 7, 6, 15))
    if direction == "A" and treatment == "filled":
        return _layers(stairs, 12, 12, 2, 3)
    if direction == "A" and treatment == "line":
        body = _ln([("M", 3, 18), ("L", 9, 18), ("L", 9, 13), ("L", 17, 13), ("L", 17, 8), ("L", 21, 8), ("L", 21, 21), ("L", 3, 21), ("Z",)], 2, "square", "miter")
        return _layers(body, 12, 13, 2, 3)
    if direction == "B" and treatment == "line":
        body = _ln([("M", 3, 17), ("L", 8, 17), ("L", 8, 12), ("L", 16, 12), ("L", 16, 7), ("L", 21, 7)], 2)
        return _layers(body, 12, 12, 3, 4)
    if direction == "B" and treatment == "filled":
        st = union(rrect(2, 17, 20, 5, 2), rrect(7, 12, 15, 10, 2), rrect(17, 7, 5, 15, 2))
        return _layers(st, 12, 12, 3, 4)
    raise ValueError


def connect_24(direction, treatment):
    if direction == "A" and treatment == "filled":
        body = minus(circle(12, 12, 10), rect(11, 0, 2, 24))
        return _layers(body, 12, 12, 2, 3)
    if direction == "A" and treatment == "line":
        left = _ln([("A", 12, 12, 9, 97, 263)], 2, "butt", "miter")
        right = _ln([("A", 12, 12, 9, -83, 83)], 2, "butt", "miter")
        return _layers(union(left, right), 12, 12, 2, 3)
    if direction == "B" and treatment == "line":
        body = union(_ln([("A", 12, 12, 9, 112, 248)], 2), _ln([("A", 12, 12, 9, -68, 68)], 2))
        return _layers(body, 12, 12, 3, 4)
    if direction == "B" and treatment == "filled":
        body = minus(circle(12, 12, 10), rrect(11, -1, 2, 26, 0))
        # soften the four corners where the halves meet the divide
        return _layers(body, 12, 12, 3, 4)
    raise ValueError


def act_24(direction, treatment):
    leaf = poly((3, 2), (11, 5), (11, 22), (3, 22))
    frame = union(rect(12, 2, 9, 3), rect(18, 2, 3, 20))
    if direction == "A" and treatment == "filled":
        return _layers(union(leaf, frame), 7, 12, 2, 3)
    if direction == "A" and treatment == "line":
        f = _ln([("M", 13, 3), ("L", 20, 3), ("L", 20, 22)], 2, "square", "miter")
        lf = _ln([("M", 4, 3.4), ("L", 10, 5.6), ("L", 10, 21), ("L", 4, 21), ("Z",)], 2, "square", "miter")
        return _layers(union(f, lf), 7, 12, 2, 3)
    if direction == "B" and treatment == "line":
        f = _ln([("M", 13, 3), ("L", 20, 3), ("L", 20, 21)], 2)
        lf = _ln([("M", 4, 3.4), ("L", 10, 5.6), ("L", 10, 21), ("L", 4, 21), ("Z",)], 2)
        return _layers(union(f, lf), 7, 12, 3, 4)
    if direction == "B" and treatment == "filled":
        lf = fillet_poly([(3, 2), (11, 5), (11, 22), (3, 22)], 2)
        fr = union(rrect(12, 2, 9, 3, 1.5), rrect(18, 2, 3, 20, 1.5), rect(17, 2, 3, 3))
        return _layers(union(lf, fr), 7, 12, 3, 4)
    raise ValueError


def _round_poly(pts, r):
    """Polygon with its corners rounded by stroking an inset copy."""
    from symbols_geom import stroke_path as sp
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    inset = []
    for (x, y) in pts:
        dx, dy = cx - x, cy - y
        n = (dx * dx + dy * dy) ** 0.5
        inset.append((x + dx / n * r * 1.15, y + dy / n * r * 1.15))
    segs = [("M", *inset[0])] + [("L", *p) for p in inset[1:]] + [("Z",)]
    return union(poly(*inset), sp(segs, 2 * r, "round", "round"))


DRAW_24 = {"explain": explain_24, "track": track_24, "connect": connect_24, "act": act_24}

# ------------------------------------------------------------------ 16 px master (pixel fit)
# Hand-fitted. A: node dot 3 px at a pixel centre (7.5, 7.5) in a 5 px seat, so the
# 1 px ring and the dot land on whole pixels. B: 2 px lines on whole-pixel centres,
# node 4 px at (8, 8) with a 1 px gap.

def explain_16(direction, treatment):
    if direction == "A" and treatment == "filled":
        body = union(minus(rect(1, 4, 10, 10), rect(6, 4, 5, 5)), rect(9, 1, 5, 5))
        return _layers(body, 7.5, 7.5, 1.5, 2.5)
    if direction == "A" and treatment == "line":
        body = union(_ln([("M", 2, 6), ("L", 5, 6), ("L", 5, 11), ("L", 11, 11), ("L", 11, 14), ("L", 2, 14), ("Z",)], 2, "square", "miter"),
                     _ln([("M", 11, 2), ("L", 14, 2), ("L", 14, 5), ("L", 11, 5), ("Z",)], 2, "square", "miter"))
        return _layers(body, 8, 8, 2, 3)
    if direction == "B" and treatment == "line":
        body = union(_ln([("M", 2, 6), ("L", 5, 6), ("L", 5, 11), ("L", 11, 11), ("L", 11, 14), ("L", 2, 14), ("Z",)], 2),
                     _ln([("M", 11, 2), ("L", 14, 2), ("L", 14, 5), ("L", 11, 5), ("Z",)], 2))
        return _layers(body, 8, 8, 2, 3)
    if direction == "B" and treatment == "filled":
        body = union(rrect(1, 4, 5, 10, 1.5), rrect(1, 9, 10, 5, 1.5), rrect(9, 1, 5, 5, 1.5))
        return _layers(body, 7.5, 7.5, 1.5, 2.5)
    raise ValueError


def track_16(direction, treatment):
    stairs = union(rect(1, 11, 4, 4), rect(5, 7, 6, 8), rect(11, 3, 4, 12))
    if direction == "A" and treatment == "filled":
        return _layers(stairs, 7.5, 7.5, 1.5, 2.5)
    if direction == "A" and treatment == "line":
        body = _ln([("M", 2, 11), ("L", 4, 11), ("L", 4, 8), ("L", 12, 8), ("L", 12, 4), ("L", 14, 4), ("L", 14, 14), ("L", 2, 14), ("Z",)], 2, "square", "miter")
        return _layers(body, 8, 8, 2, 3)
    if direction == "B" and treatment == "line":
        body = _ln([("M", 2, 12), ("L", 4, 12), ("L", 4, 8), ("L", 12, 8), ("L", 12, 4), ("L", 14, 4)], 2)
        return _layers(body, 8, 8, 2, 3)
    if direction == "B" and treatment == "filled":
        st = union(rrect(1, 11, 14, 4, 1.5), rrect(5, 7, 10, 8, 1.5), rrect(11, 3, 4, 12, 1.5))
        return _layers(st, 7.5, 7.5, 1.5, 2.5)
    raise ValueError


def connect_16(direction, treatment):
    if direction == "A" and treatment == "filled":
        body = minus(circle(7.5, 7.5, 6.5), rect(7, 0, 1, 16))
        return _layers(body, 7.5, 7.5, 1.5, 2.5)
    if direction == "A" and treatment == "line":
        left = _ln([("A", 8, 8, 6, 104, 256)], 2, "butt", "miter")
        right = _ln([("A", 8, 8, 6, -76, 76)], 2, "butt", "miter")
        return _layers(union(left, right), 8, 8, 2, 3)
    if direction == "B" and treatment == "line":
        body = union(_ln([("A", 8, 8, 6, 118, 242)], 2), _ln([("A", 8, 8, 6, -62, 62)], 2))
        return _layers(body, 8, 8, 2, 3)
    if direction == "B" and treatment == "filled":
        body = minus(circle(7.5, 7.5, 6.5), rect(7, 0, 1, 16))
        return _layers(body, 7.5, 7.5, 1.5, 2.5)
    raise ValueError


def act_16(direction, treatment):
    if direction == "A" and treatment == "filled":
        leaf = poly((2, 1), (8, 3), (8, 15), (2, 15))
        frame = union(rect(9, 1, 5, 2), rect(12, 1, 2, 14))
        return _layers(union(leaf, frame), 5, 8, 1, 2)
    if direction == "A" and treatment == "line":
        f = _ln([("M", 10, 2), ("L", 13, 2), ("L", 13, 15)], 2, "square", "miter")
        lf = _ln([("M", 2, 2.5), ("L", 8, 4.5), ("L", 8, 14), ("L", 2, 14), ("Z",)], 2, "square", "miter")
        return {"body": union(f, lf), "seat": empty(), "node": rect(4, 8, 2, 2)}
    if direction == "B" and treatment == "line":
        f = _ln([("M", 10, 2), ("L", 13, 2), ("L", 13, 14)], 2)
        lf = _ln([("M", 2, 2.5), ("L", 8, 4.5), ("L", 8, 14), ("L", 2, 14), ("Z",)], 2)
        return {"body": union(f, lf), "seat": empty(), "node": circle(5, 9, 1)}
    if direction == "B" and treatment == "filled":
        leaf = fillet_poly([(2, 1), (8, 3), (8, 15), (2, 15)], 1)
        frame = union(rrect(9, 1, 5, 2, 1), rrect(12, 1, 2, 14, 1), rect(11, 1, 2, 2))
        return _layers(union(leaf, frame), 5, 8, 1, 2)
    raise ValueError


DRAW_16 = {"explain": explain_16, "track": track_16, "connect": connect_16, "act": act_16}


def draw(pillar, direction, treatment, size):
    """Return layers for a pillar mark in the field of the requested pixel size."""
    if treatment == "tile":
        return tile(pillar, direction, size)
    if size == 16:
        return DRAW_16[pillar](direction, treatment)
    lay = DRAW_24[pillar](direction, treatment)
    s = size / 24
    return {k: transform(v, s) for k, v in lay.items()}


def tile(pillar, direction, size):
    """A rounded-square tile with the mark reversed out of it.

    Returns layers: tile (the plate, with the mark cut out), body, seat, node in tile
    space. On a tile the mark is the surface colour, so the renderer paints body and
    node in the surface colour over the plate.
    """
    r = {16: 3, 24: 4, 48: 8, 96: 16}[size]
    plate = rrect(0, 0, size, size, r)
    inner = "filled" if direction == "A" else "line"
    if size == 16:
        lay = {k: (transform(v, 1, 3, 3) if k != "hole" else v) for k, v in micro_10(pillar).items()}
    elif size == 24:
        lay = {k: transform(v, 1, 4, 4) for k, v in DRAW_16[pillar](direction, inner).items()}
    else:
        s = size * 2 / 3 / 24
        off = size / 6
        lay = {k: transform(v, s, off, off) for k, v in DRAW_24[pillar](direction, inner).items()}
    return {"plate": plate, **{k: v for k, v in lay.items() if k != "hole"}, "hole": bool(lay.get("hole"))}


# ------------------------------------------------------------------ topic grammar proof (Direction A)
# Same rules as the A pillars: filled primitives, square corners, one hinge node as a
# dot in a clear seat. The node takes a real job in each subject: the filled oval on a
# ballot, the seal on a bill, the seal on an envelope, the face of a coin.

TOPICS = ["ballot", "bill", "contact-an-official", "campaign-money"]
TOPIC_LABELS = {"ballot": "Ballot", "bill": "Bill", "contact-an-official": "Contact an official", "campaign-money": "Campaign money"}


def topic_24(name):
    if name == "ballot":
        box = minus(rect(3, 13, 18, 9), rect(6, 13, 12, 2))
        return _layers(union(box, rect(8, 2, 8, 12)), 12, 7, 2, 3)
    if name == "bill":
        sh = poly((4, 2), (15, 2), (20, 7), (20, 22), (4, 22))
        sh = minus(sh, poly((14, 1), (14, 8), (21, 8), (21, 1)))
        sh = union(sh, poly((16, 2), (16, 6), (20, 6)))
        sh = minus(sh, rect(8, 9, 8, 2), rect(8, 13, 5, 2))
        return _layers(sh, 12, 18, 2, 3)
    if name == "contact-an-official":
        env = minus(rect(2, 5, 20, 14), stroke_path([("M", 1, 4.4), ("L", 12, 12.6), ("L", 23, 4.4)], 2, "butt", "miter"))
        return _layers(env, 12, 12.5, 2, 3.2)
    if name == "campaign-money":
        stack = minus(union(rrect(2, 17, 15, 5, 2.5), rrect(4, 11, 12, 5, 2.5)), circle(16, 9, 7.5))
        coin = circle(16, 9, 6.5)
        lay = _layers(coin, 16, 9, 2, 3)
        lay["body"] = union(lay["body"], stack)
        return lay
    raise ValueError


def topic_16(name):
    if name == "ballot":
        box = minus(rect(2, 10, 13, 5), rect(4, 10, 9, 1))
        return _layers(union(box, rect(5, 1, 7, 10)), 8.5, 4.5, 1.5, 2.5)
    if name == "bill":
        sh = minus(rect(3, 1, 11, 14), rect(10, 0, 5, 5))
        sh = union(sh, poly((11, 1), (11, 4), (14, 4)))
        sh = minus(sh, rect(5, 6, 6, 2))
        return _layers(sh, 8.5, 11.5, 1.5, 2.5)
    if name == "contact-an-official":
        env = minus(rect(1, 3, 13, 10), stroke_path([("M", 0.6, 2.6), ("L", 7.5, 8.4), ("L", 14.4, 2.6)], 1.6, "butt", "miter"))
        return _layers(env, 7.5, 9.5, 1.5, 2.5)
    if name == "campaign-money":
        stack = minus(union(rrect(1, 11, 11, 4, 2), rrect(2, 7, 8, 3, 1.5)), circle(10.5, 5.5, 5.5))
        lay = _layers(circle(10.5, 5.5, 4.5), 10.5, 5.5, 1.5, 2.5)
        lay["body"] = union(lay["body"], stack)
        return lay
    raise ValueError


def topic(name, size):
    if size == 16:
        return topic_16(name)
    s = size / 24
    return {k: transform(v, s) for k, v in topic_24(name).items()}


def micro_10(pillar):
    """10 px drawings for the 16 px tile, on whole pixels. Shared by both directions:
    at this size the two grammars converge. Nodes are 2 px."""
    if pillar == "explain":
        body = union(minus(rect(0, 3, 6, 6), rect(3, 3, 3, 3)), rect(7, 0, 3, 3))
        return {"body": body, "seat": empty(), "node": rect(4, 3, 2, 2)}
    if pillar == "track":
        body = union(rect(0, 7, 3, 3), rect(3, 4, 4, 6), rect(7, 1, 3, 9))
        return {"body": body, "seat": empty(), "node": rect(4, 1, 2, 2)}
    if pillar == "connect":
        body = minus(circle(5, 5, 5), rect(4, 0, 2, 10))
        return {"body": body, "seat": empty(), "node": rect(4, 4, 2, 2)}
    if pillar == "act":
        body = minus(union(poly((0, 0), (4, 1), (4, 10), (0, 10)), rect(5, 0, 5, 2), rect(8, 0, 2, 10)), rect(1, 4, 2, 2))
        return {"body": body, "seat": empty(), "node": rect(1, 4, 2, 2), "hole": True}
    raise ValueError
