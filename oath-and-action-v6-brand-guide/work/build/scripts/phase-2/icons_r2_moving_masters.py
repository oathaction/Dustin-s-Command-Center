"""Concept 2, Moving part, stage 2: write the masters and their color variants.

Run: python3 -I icons_r2_moving_masters.py [--sheet]
Writes, in work/boards/phase-2/icons-r2/moving-part/:
  20261028_Moving-Part-<Icon>-Display.svg        display master, 48 px and up (cut 1.5 units, 1-unit corners)
  20261028_Moving-Part-<Icon>-24px.svg           hinted 24 px master (cut 2 px, square corners)
  20261028_Moving-Part-<Icon>-16px.svg           hinted 16 px master (cut 1 px, square corners)
  ...-<Size>-Open.svg                            the row state: the red piece one step further open,
                                                 2 units in the display master, 1 px at 24 and 16 px.
                                                 The hinted open masters carry a "keyline" path, a 1 px
                                                 ring around the red piece, unfilled in the master
  variants/...-<Size>[-Open]-<Colorway>.svg      the colorways in icons_r2_moving_common.COLORWAYS
With --sheet it also writes a magnified review sheet of the hinted masters to the scratchpad.

Hinting. The 24 px master is the drawing redrawn with a 2-unit cut and square corners, so 1 unit is
1 px. The 16 px master is the display geometry with square corners, scaled by 2/3, which turns the
1.5-unit cut into 1 px. Every horizontal and vertical edge then moves to the nearest whole pixel. Both
sides of a cut move together, because a cut of a whole number of pixels rounds the same way on both
sides. Edges off the 90 degree grid (the red piece turned on its hinge, arrowheads, arcs) stay true
vectors; Phase 1's pixel-fit test exempts them. Round pieces stay true discs and ellipses with whole-pixel
diameters and their extremes on whole pixels: a solid disc rounds down at a quarter pixel, so it never
grows into its cut, and a knock-out rounds to the nearest pixel. Before snapping, the drawing moves by
up to half a pixel, the shift that moves its edges and its node least. The open state reuses the shift
of the drawing at rest, so only the red piece moves. Per-icon hand fixes live in FIX.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_moving_common as C  # noqa: E402
import icons_r2_moving_draw as D  # noqa: E402
import icons_r2_moving_geom as G  # noqa: E402
import pathops  # noqa: E402
from icons_geom import d_of, transform  # noqa: E402  (round one, read only)

NUM = r"(-?[\d.]+)"
OVAL = re.compile(rf"^M{NUM} {NUM}A{NUM} {NUM} 0 0 ([01]) {NUM} \2A\3 \4 0 0 \5 \1 \2Z$")
# node_r and bite_extra are in drawing units, before the scale. At 24 px the node grows to 4 px
# across, as in round one, so it reads as a dot at 1x. At 16 px it is 2 px, a square of whole pixels,
# and the bite grows by (sqrt 2 - 1) node radii so the square's corners keep a full cut.
HINT = {"24px": {"S": 24, "cut": 2.0, "scale": 1.0, "step": 1.0, "node_r": 2.0, "bite_extra": 0.0},
        "16px": {"S": 16, "cut": 1.5, "scale": 2 / 3, "step": 1.5, "node_r": 1.5, "bite_extra": 1.5 * (math.sqrt(2) - 1)}}

# Hand fixes by (icon, size), set by eye on the magnified review sheet:
#   "pixel": True           draw every piece in whole pixels after snapping (Testify and Feedback loop at
#                           16 px, Feedback loop at 24 px), so their curves stay crisp (D1-17)
#   "pixel_fix": {"rest": {...}, "open": {...}}   pixels to add or drop after that
#   "shift": (dx, dy)       the move before snapping, in place of the automatic choice
#   "spec": {"node_r": r, "ovr": {...}}   drawing overrides for this size, in drawing units
#   "x" / "y": {old: new}   coordinates to force before snapping, matched to 0.01 px after the shift
FIX = {
    # Connect: the knock-out node sized to the bar, 3 px at 24 px and 1 px at 16 px, so the red keeps a
    # full pixel above and below it; at 24 px the circle is 19 px across so its extremes land on pixels.
    ("connect", "24px"): {"spec": {"node_r": 1.5, "ovr": {"connect_R": 9.5}}},
    ("connect", "16px"): {"spec": {"node_r": 0.75}},
    # Act: the hinge pin moves out of the leaf so the bite takes 1 px of the leaf's 4 px, and the leaf
    # never reads as a C around a dot.
    ("act", "24px"): {"spec": {"ovr": {"act_pin": 3.0}}},
    # Housing: at 24 px the door starts 1.5 px lower, so a 2 px band of wall runs over its cut.
    ("housing", "24px"): {"spec": {"ovr": {"housing_door_top": 17.0}}},
    # Campaign money: the back note lifts further at small sizes, so enough of it shows above the
    # front note to read as a second note and never as a red line.
    ("money", "24px"): {"spec": {"ovr": {"money_lift": 4.0}}, "shift": (-0.25, -0.25)},
    # Act at 16 px: no vertical shift, so the lintel, the leaf's top corner and the floor all land
    # on whole pixels and the leaf keeps its 1 px cut from the lintel.
    ("act", "16px"): {"spec": {"ovr": {"act_pin": 2.75}}, "shift": (1 / 3, 0.0)},
    # Testify: at 16 px drawn by hand in whole pixels (head 4 px, shoulders 6 px, the sound a 2 px
    # arc, the microphone 3 px), since its curves left half its pixels gray. At 24 px the figure sits on
    # whole pixels: shoulders 10 px across from x 2, head 8 px, both centered on x 7, and the ring
    # thins to 1.75 px so the microphone keeps its 2 px cut.
    ("testify", "16px"): {"ascii": {"rest": ['................', '................', '................', '................', '................', '.......r........', '...##..rr..###..', '..####..rr.###..', '..####..rr.###..', '...##..rr..###..', '.......r....#...', '..####......#...', '.######.....#...', '.######...#####.', '................', '................'],
                                     "open": ['................', '................', '................', '................', '.......r........', '.......rr.......', '...##...rr.###..', '..####..rr.###..', '..####.rr..###..', '...##..r...###..', '............#...', '..####......#...', '.######.....#...', '.######...#####.', '................', '................']}},
    ("testify", "24px"): {"spec": {"ovr": {"testify_sc": (7.0, 21.0), "testify_sr": 5.0, "testify_hr": 4.0, "testify_ring_w": 1.75}}, "shift": (0.0, 0.0)},
    # Ballot at 24 px: no shift, so the box (18 px), the slot and the paper (6 px) stay centered, and
    # the mark is a 4 by 2 px knock-out with a 1 px wall on each side.
    ("ballot", "24px"): {"spec": {"ovr": {"ballot_mark": (2.0, 1.0)}}, "shift": (0.0, 0.0)},
    # Feedback loop: drawn by hand in whole pixels at 24 and 16 px. Its arc left most of its pixels
    # gray, and plain pixel rounding turned the red arrowhead into a cross, which the family bars.
    # The nodes are 5 px at 24 px and 4 px at 16 px, so the forward arrow keeps a shaft.
    ("loop", "24px"): {"ascii": {"rest": ['........................', '........................', '.............###........', '.......r....#####.......', '.......rr...#####.......', '.......rrr..#####.......', '.......rr....###........', '.......rr...............', '......rr................', '......rr.....###........', '......rr.....###........', '......rr.....###........', '......rr...#######......', '......rr....#####.......', '......rr.....###........', '.......rr...............', '.......rr...............', '........rr...###........', '........rr..#####.......', '............#####.......', '............#####.......', '.............###........', '........................', '........................'],
                                  "open": ['........................', '........................', '.............###........', '.......r....#####.......', '.......rr...#####.......', '.......rrr..#####.......', '......rrr....###........', '......rr................', '.....rr.................', '.....rr......###........', '.....rr......###........', '.....rr......###........', '.....rr....#######......', '.....rr.....#####.......', '.....rr......###........', '......rr................', '......rrr...............', '........rr...###........', '........rr..#####.......', '............#####.......', '............#####.......', '.............###........', '........................', '........................']}},
    ("loop", "16px"): {"ascii": {"rest": ['................', '..........##....', '......r..####...', '......rr.####...', '.....rrr..##....', '.....rr.........', '....rr....##....', '....rr....##....', '....rr...####...', '....rr....##....', '.....rr.........', '.....rr...##....', '......rr.####...', '......rr.####...', '..........##....', '................'],
                                  "open": ['................', '..........##....', '......r..####...', '......rr.####...', '.....rrr..##....', '....rrr.........', '...rr.....##....', '...rr.....##....', '...rr....####...', '...rr.....##....', '....rrr.........', '.....rr...##....', '......rr.####...', '......rr.####...', '..........##....', '................']}},
    ("money", "16px"): {"spec": {"ovr": {"money_lift": 4.25}}, "shift": (0.5, 1 / 3)},
}


def fx(v):
    return G.fmt(v)


CENTER = [12.0, 12.0]   # the drawing's center after the shift; a coordinate exactly on a half pixel rounds away from it


def snap(v, axis=0):
    f = v - math.floor(v)
    if abs(f - 0.5) < 1e-6:
        return math.floor(v) if v < CENTER[axis] else math.ceil(v)
    return math.floor(v + 0.5)


def subpaths(d):
    return [s.strip() for s in re.findall(r"M[^M]*", d) if s.strip()]


TOK = re.compile(r"[MLHVACQZ]|-?\d*\.?\d+(?:e-?\d+)?")


def parse(sp):
    """One subpath as a start point and a list of segments (kind, args..., end point)."""
    toks = TOK.findall(sp)
    i = 0
    cur = start = None
    segs = []
    cmd = None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd == "Z":
                if cur is not None and start is not None and math.dist(cur, start) > 1e-9:
                    segs.append(["L", start])
                cur = start
                continue
        if cmd == "M":
            cur = start = (float(toks[i]), float(toks[i + 1]))
            i += 2
            cmd = "L"
        elif cmd == "L":
            cur = (float(toks[i]), float(toks[i + 1]))
            segs.append(["L", cur])
            i += 2
        elif cmd == "H":
            cur = (float(toks[i]), cur[1])
            segs.append(["L", cur])
            i += 1
        elif cmd == "V":
            cur = (cur[0], float(toks[i]))
            segs.append(["L", cur])
            i += 1
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = (float(v) for v in toks[i:i + 7])
            cur = (x, y)
            segs.append(["A", rx, ry, rot, int(la), int(sw), cur])
            i += 7
        elif cmd == "C":
            a, b, c = (float(toks[i]), float(toks[i + 1])), (float(toks[i + 2]), float(toks[i + 3])), (float(toks[i + 4]), float(toks[i + 5]))
            cur = c
            segs.append(["C", a, b, cur])
            i += 6
        elif cmd == "Q":
            a, c = (float(toks[i]), float(toks[i + 1])), (float(toks[i + 2]), float(toks[i + 3]))
            cur = c
            segs.append(["Q", a, cur])
            i += 4
        else:
            raise ValueError(sp)
    return start, segs


def emit(start, segs):
    out = [f"M{fx(start[0])} {fx(start[1])}"]
    cur = start
    for s in segs:
        k, end = s[0], s[-1]
        if k == "L":
            if abs(end[1] - cur[1]) < 1e-9:
                out.append(f"H{fx(end[0])}")
            elif abs(end[0] - cur[0]) < 1e-9:
                out.append(f"V{fx(end[1])}")
            else:
                out.append(f"L{fx(end[0])} {fx(end[1])}")
        elif k == "A":
            out.append(f"A{fx(s[1])} {fx(s[2])} {fx(s[3])} {s[4]} {s[5]} {fx(end[0])} {fx(end[1])}")
        elif k == "C":
            out.append(f"C{fx(s[1][0])} {fx(s[1][1])} {fx(s[2][0])} {fx(s[2][1])} {fx(end[0])} {fx(end[1])}")
        elif k == "Q":
            out.append(f"Q{fx(s[1][0])} {fx(s[1][1])} {fx(end[0])} {fx(end[1])}")
        cur = end
    out.append("Z")
    return "".join(out)


def drawing(name, size, open_):
    """The drawing for a hinted size, as [(role, d)], before the shift."""
    h = HINT[size]
    sp = FIX.get((name, size), {}).get("spec", {})
    with D.spec(h["cut"], 0.0, sp.get("node_r", h["node_r"]), h["bite_extra"], sp.get("ovr", {})):
        pcs = D.pieces(name, h["step"] if open_ else 0.0)
    if h["scale"] == 1.0:
        return pcs
    s = h["scale"]
    out = []
    for role, d in pcs:
        parts = []
        for sp in subpaths(d):
            m = OVAL.match(sp)
            if m:
                x1, cy, rx, ry, sw, x2 = (float(m.group(i)) for i in range(1, 7))
                cx = (x1 + x2) / 2
                parts.append(G.ellipse_d(cx * s, cy * s, rx * s, ry * s, hole=(sw == 0)))
            else:
                st, segs = parse(sp)
                f = lambda p: (p[0] * s, p[1] * s)  # noqa: E731
                ns = []
                for g in segs:
                    if g[0] == "A":
                        ns.append(["A", g[1] * s, g[2] * s, g[3], g[4], g[5], f(g[6])])
                    else:
                        ns.append([g[0]] + [f(p) for p in g[1:]])
                parts.append(emit(f(st), ns))
        out.append((role, "".join(parts)))
    return out


def move(pcs, dx, dy):
    out = []
    for role, d in pcs:
        parts = []
        for sp in subpaths(d):
            m = OVAL.match(sp)
            if m:
                x1, cy, rx, ry, sw, x2 = (float(m.group(i)) for i in range(1, 7))
                parts.append(G.ellipse_d((x1 + x2) / 2 + dx, cy + dy, rx, ry, hole=(sw == 0)))
                continue
            st, segs = parse(sp)
            f = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
            ns = [(["A"] + g[1:6] + [f(g[6])]) if g[0] == "A" else ([g[0]] + [f(p) for p in g[1:]]) for g in segs]
            parts.append(emit(f(st), ns))
        out.append((role, "".join(parts)))
    return out


def snap_oval(cx, cy, rx, ry, solid):
    """Whole-pixel diameters with the extremes on whole pixels. An oval centered on a pixel center
    takes an odd diameter and one centered on a pixel corner an even one, so it stays centered in
    its piece. Otherwise a solid rounds down at a quarter pixel, so it never grows into its cut, and
    a knock-out rounds to the nearest pixel."""
    def dia(r, c):
        f = c - math.floor(c)
        want = "odd" if abs(f - 0.5) < 0.1 else ("even" if (f < 0.1 or f > 0.9) else None)
        base = (2 * r + 0.25) if solid else (2 * r + 0.5)
        Dd = max(1, int(base))
        if (want == "odd" and Dd % 2 == 0) or (want == "even" and Dd % 2 == 1):
            Dd = Dd - 1 if Dd > 1 else Dd + 1     # a parity change always shrinks, to keep the walls around it
        return max(1 if not solid else 2, Dd)
    Dx, Dy = dia(rx, cx), dia(ry, cy)
    ncx = math.floor(cx) + 0.5 if Dx % 2 else snap(cx, 0)
    ncy = math.floor(cy) + 0.5 if Dy % 2 else snap(cy, 1)
    return ncx, ncy, Dx / 2, Dy / 2


def oval_d(cx, cy, rx, ry, solid):
    """A disc or ellipse. A solid 2 px across or less, or a knock-out 3 px across or less, is a
    square of whole pixels at 1x, so it draws as one and stays crisp."""
    if min(rx, ry) <= (1.0 if solid else 1.5):
        return G.contour_d(G.rect(cx - rx, cy - ry, 2 * rx, 2 * ry)) if solid else G.contour_d(G.rect_hole(cx - rx, cy - ry, 2 * rx, 2 * ry))
    if rx == ry:
        return G.circle_d(cx, cy, rx, hole=not solid)
    return G.ellipse_d(cx, cy, rx, ry, hole=not solid)


def arc_center(p0, p1, r, la, sw):
    """Center of an SVG arc with equal radii and no rotation."""
    x1p, y1p = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    num = r * r * r * r - r * r * y1p * y1p - r * r * x1p * x1p
    den = r * r * y1p * y1p + r * r * x1p * x1p
    if den < 1e-12:
        return None
    coef = math.sqrt(max(0.0, num / den)) * (-1 if la == sw else 1)
    return coef * y1p + (p0[0] + p1[0]) / 2, -coef * x1p + (p0[1] + p1[1]) / 2


def solid_discs(pcs):
    """Every solid disc in the drawing, with where it was and where it snaps."""
    out = []
    for role, d in pcs:
        for sp in subpaths(d):
            m = OVAL.match(sp)
            if m and m.group(5) == "1":
                x1, cy, rx, ry, sw, x2 = (float(m.group(i)) for i in range(1, 7))
                c0 = ((x1 + x2) / 2, cy)
                ncx, ncy, nrx, nry = snap_oval(*c0, rx, ry, True)
                out.append({"c0": c0, "c1": (ncx, ncy), "r0": rx, "r1": nrx})
    return out


def snap_sub(sp, fix, discs):
    """Snap one subpath. Ovals snap by their extremes. Other contours snap their horizontal and
    vertical edges to whole pixels. An arc that bites around a disc keeps its radius and follows the
    disc, its ends sliding along their snapped edges; a contour with no straight axis edge that is
    concentric with a disc moves with the disc."""
    m = OVAL.match(sp)
    if m:
        x1, cy, rx, ry, sw, x2 = (float(m.group(i)) for i in range(1, 7))
        solid = sw == 1
        c0 = ((x1 + x2) / 2, cy)
        ncx, ncy, nrx, nry = snap_oval(*c0, rx, ry, solid)
        return oval_d(ncx, ncy, nrx, nry, solid), [abs(ncx - c0[0]), abs(ncy - c0[1])]
    st, segs = parse(sp)
    pts = [st] + [g[-1] for g in segs]
    n = len(segs)
    sx, sy = [False] * len(pts), [False] * len(pts)
    for i, g in enumerate(segs):
        a, b = pts[i], pts[i + 1]
        if g[0] != "L":
            continue
        if abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) > 1e-6:
            sx[i] = sx[i + 1] = True
        elif abs(a[1] - b[1]) < 1e-6 and abs(a[0] - b[0]) > 1e-6:
            sy[i] = sy[i + 1] = True
    if math.dist(pts[0], pts[-1]) < 1e-9:
        sx[0] = sx[-1] = sx[0] or sx[-1]
        sy[0] = sy[-1] = sy[0] or sy[-1]
    # arcs concentric with a disc
    conc = {}
    for i, g in enumerate(segs):
        if g[0] == "A" and abs(g[1] - g[2]) < 1e-6:
            c = arc_center(pts[i], pts[i + 1], g[1], g[4], g[5])
            if c is None:
                continue
            for dk in discs:
                if math.dist(c, dk["c0"]) < 0.05:
                    conc[i] = dk
    new = []
    disp = []
    fxm, fym = fix.get("x", {}), fix.get("y", {})
    for p, a, b in zip(pts, sx, sy):
        x, y = p
        for k, v in fxm.items():
            if abs(x - k) < 0.01:
                x = v
        for k, v in fym.items():
            if abs(y - k) < 0.01:
                y = v
        nx = snap(x, 0) if a else x
        ny = snap(y, 1) if b else y
        if a:
            disp.append(abs(nx - p[0]))
        if b:
            disp.append(abs(ny - p[1]))
        new.append((nx, ny))
    if conc and not any(sx) and not any(sy):
        dk = next(iter(conc.values()))
        ddx, ddy = dk["c1"][0] - dk["c0"][0], dk["c1"][1] - dk["c0"][1]
        new = [(x + ddx, y + ddy) for x, y in pts]
    else:
        for i, dk in conc.items():
            R = segs[i][1]
            for j in (i, i + 1):
                ox, oy = pts[j]
                cx0, cy0 = dk["c0"]
                cx1, cy1 = dk["c1"]
                if sx[j] and not sy[j]:
                    x = new[j][0]
                    q = R * R - (x - cx1) ** 2
                    if q >= 0:
                        new[j] = (x, cy1 + math.copysign(math.sqrt(q), oy - cy0))
                elif sy[j] and not sx[j]:
                    y = new[j][1]
                    q = R * R - (y - cy1) ** 2
                    if q >= 0:
                        new[j] = (cx1 + math.copysign(math.sqrt(q), ox - cx0), y)
                elif not sx[j] and not sy[j]:
                    new[j] = (ox + cx1 - cx0, oy + cy1 - cy0)
        if math.dist(pts[0], pts[-1]) < 1e-9:
            new[-1] = new[0] if (0 in conc or (n - 1) not in conc) else new[-1]
            new[0] = new[-1]
    ns = []
    for i, g in enumerate(segs):
        d0 = (new[i][0] - pts[i][0], new[i][1] - pts[i][1])
        d1 = (new[i + 1][0] - pts[i + 1][0], new[i + 1][1] - pts[i + 1][1])
        if g[0] == "L":
            ns.append(["L", new[i + 1]])
        elif g[0] == "A":
            ns.append(["A"] + g[1:6] + [new[i + 1]])
        elif g[0] == "C":
            ns.append(["C", (g[1][0] + d0[0], g[1][1] + d0[1]), (g[2][0] + d1[0], g[2][1] + d1[1]), new[i + 1]])
        elif g[0] == "Q":
            ns.append(["Q", (g[1][0] + (d0[0] + d1[0]) / 2, g[1][1] + (d0[1] + d1[1]) / 2), new[i + 1]])
    if n and math.dist(new[0], new[-1]) < 1e-9 and ns and ns[-1][0] == "L":
        ns = ns[:-1]   # the closing line is implied by Z
    return emit(new[0], ns), disp


def snap_all(pcs, fix):
    discs = solid_discs(pcs)
    out, disp = [], []
    for role, d in pcs:
        parts = []
        for sp in subpaths(d):
            s_, dd = snap_sub(sp, fix, discs)
            parts.append(s_)
            disp += dd
        out.append((role, "".join(parts)))
    return out, disp


def node_cost(pcs):
    """How far the solid discs sit from their whole-pixel places, and how much their size changes."""
    return sum(abs(dk["c1"][0] - dk["c0"][0]) + abs(dk["c1"][1] - dk["c0"][1]) + 2 * abs(dk["r1"] - dk["r0"]) for dk in solid_discs(pcs))


def choose_shift(pcs, S):
    best = None
    steps = [i / 12 for i in range(-6, 7)]
    for dx in steps:
        for dy in steps:
            CENTER[:] = [S / 2 + dx, S / 2 + dy]
            moved = move(pcs, dx, dy)
            _, disp = snap_all(moved, {})
            cost = sum(disp) + 4 * node_cost(moved) + 0.05 * (abs(dx) + abs(dy))
            if best is None or cost < best[0]:
                best = (cost, dx, dy)
    return best[1], best[2]


def hint(name, size, open_):
    fix = FIX.get((name, size), {})
    S = HINT[size]["S"]
    rest = drawing(name, size, False)
    dx, dy = fix["shift"] if "shift" in fix else choose_shift(rest, S)
    CENTER[:] = [S / 2 + dx, S / 2 + dy]
    pcs = move(drawing(name, size, open_), dx, dy)
    snapped, disp = snap_all(pcs, fix)
    if fix.get("pixel"):
        snapped = pixelize(snapped, S, 1.41 if S == 24 else 1.0, fix.get("pixel_fix", {}).get("open" if open_ else "rest", {}))
    if "ascii" in fix:
        snapped = from_ascii(fix["ascii"]["open" if open_ else "rest"])
    return snapped, (dx, dy), (max(disp) if disp else 0.0)


def from_ascii(rows):
    """A master drawn by hand in whole pixels: "#" Charcoal, "r" red, "." empty. Each connected group
    of pixels of one role becomes its own piece, so the cut check sees every piece."""
    S = len(rows)
    out = []
    for role, ch in (("ink", "#"), ("accent", "r")):
        cells = {(x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == ch}
        while cells:
            stack = [cells.pop()]
            comp = set(stack)
            while stack:
                x, y = stack.pop()
                for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if q in cells:
                        cells.discard(q)
                        comp.add(q)
                        stack.append(q)
            p = pathops.Path()
            for (x, y) in sorted(comp):
                p.moveTo(x, y)
                p.lineTo(x + 1, y)
                p.lineTo(x + 1, y + 1)
                p.lineTo(x, y + 1)
                p.close()
            out.append((role, d_of(pathops.simplify(p, clockwise=True))))
    assert all(len(r) == S for r in rows)
    return out


def _sq(x, y):
    p = pathops.Path()
    p.moveTo(x, y)
    p.lineTo(x + 1, y)
    p.lineTo(x + 1, y + 1)
    p.lineTo(x, y + 1)
    p.close()
    return p


def coverage(path, S):
    from fontTools.pens.areaPen import AreaPen
    b = path.bounds
    out = {}
    for y in range(max(0, math.floor(b[1])), min(S, math.ceil(b[3]))):
        for x in range(max(0, math.floor(b[0])), min(S, math.ceil(b[2]))):
            pen = AreaPen()
            pathops.op(path, _sq(x, y), pathops.PathOp.INTERSECTION).draw(pen)
            if abs(pen.value) > 1e-4:
                out[(x, y)] = min(1.0, abs(pen.value))
    return out


def edge_dist(p, q):
    dx, dy = abs(p[0] - q[0]), abs(p[1] - q[1])
    return math.hypot(max(0, dx - 1), max(0, dy - 1))


def pixelize(pcs, S, thr, fix):
    """For the icons whose curves would leave too many half-covered pixels: every piece becomes whole
    pixels (a pixel belongs to a piece the drawing covers by half or more), then the cut is enforced
    between pieces, dropping the pixel the drawing covers least, red before Charcoal. fix holds hand
    edits, {"ink+": [(x, y)], "ink-": [...], "accent+": [...], "accent-": [...]}."""
    units = []
    for role, d in pcs:
        c = coverage(G.to_pathops(d), S)
        units.append({"role": role, "cov": c, "px": {p for p, v in c.items() if v >= 0.5 - 1e-6}})
    changed = True
    while changed:
        changed = False
        for i, a in enumerate(units):
            for b in units[i + 1:]:
                drop = set()
                for p in a["px"]:
                    for q in b["px"]:
                        if abs(p[0] - q[0]) <= 3 and abs(p[1] - q[1]) <= 3 and edge_dist(p, q) < thr - 1e-6:
                            ca, cb = a["cov"].get(p, 0), b["cov"].get(q, 0)
                            if abs(ca - cb) < 1e-6:
                                pick = "a" if a["role"] == "accent" and b["role"] != "accent" else "b"
                            else:
                                pick = "a" if ca < cb else "b"
                            drop.add((pick, p if pick == "a" else q))
                for who, p in drop:
                    (a if who == "a" else b)["px"].discard(p)
                    changed = True
    for role in ("ink", "accent"):
        for p in fix.get(role + "-", []):
            for u in units:
                u["px"].discard(tuple(p))
        tgt = [u for u in units if u["role"] == role]
        for p in fix.get(role + "+", []):
            if tgt:
                tgt[0]["px"].add(tuple(p))
    out = []
    for u in units:
        p = pathops.Path()
        for (x, y) in sorted(u["px"]):
            p.moveTo(x, y)
            p.lineTo(x + 1, y)
            p.lineTo(x + 1, y + 1)
            p.lineTo(x, y + 1)
            p.close()
        out.append((u["role"], d_of(pathops.simplify(p, clockwise=True)) if u["px"] else ""))
    return out


def keyline_d(acc_d, ink_d, w=1.0):
    """A 1 px Charcoal ring around the red piece's outer edge, outside it, with square corners.
    Knock-outs in the red piece stay open. Where the ring would come closer than 1 px to a Charcoal
    piece, it stops, so the cut between the red piece and its neighbor stays open at 16 px, where
    the cut is only 1 px."""
    def grow(p, by):
        st = pathops.Path()
        p.draw(st.getPen())
        st.stroke(2 * by, pathops.LineCap.BUTT_CAP, pathops.LineJoin.MITER_JOIN, 4)
        st.convertConicsToQuads()
        return pathops.op(p, pathops.simplify(st), pathops.PathOp.UNION)
    filled = pathops.Path()
    for sp in subpaths(acc_d):
        filled = pathops.op(filled, pathops.simplify(G.to_pathops(sp)), pathops.PathOp.UNION)
    ring = pathops.op(grow(filled, w), filled, pathops.PathOp.DIFFERENCE)
    if ink_d:
        near = grow(G.to_pathops(ink_d), 0.999)
        ring = pathops.op(ring, near, pathops.PathOp.DIFFERENCE)
    return d_of(ring)


def gaps(pcs):
    import itertools
    out = []
    for (ra, a), (rb, b) in itertools.combinations(pcs, 2):
        g, o = G.gap_between(a, b)
        out.append((g, o))
    return min(g for g, o in out), any(o for g, o in out)


def display_master(name, open_):
    pcs = D.pieces(name, D.STEP if open_ else 0.0)
    return {"ink": "".join(d for r, d in pcs if r == "ink"), "accent": "".join(d for r, d in pcs if r == "accent")}


def title(name, size, open_, colorway="Charcoal-Red"):
    s = {"Display": "display master", "24px": "24 px master", "16px": "16 px master"}[size]
    st = ", row state (current item)" if open_ else ""
    return f"{D.LABELS[name]}, Concept 2 Moving part, {s}{st}, {colorway}. Oath &amp; Action icon concept, October 28, 2026. Proposal only."


def write_all():
    C.OUT.mkdir(parents=True, exist_ok=True)
    C.VARIANTS.mkdir(parents=True, exist_ok=True)
    report = {}
    for name in D.ICONS:
        for open_ in (False, True):
            masters = {"Display": display_master(name, open_)}
            for size in ("24px", "16px"):
                pcs, sh, worst = hint(name, size, open_)
                m = {"ink": "".join(d for r, d in pcs if r == "ink"), "accent": "".join(d for r, d in pcs if r == "accent")}
                if open_:
                    m["keyline"] = keyline_d(m["accent"], m["ink"])
                masters[size] = m
                g, ov = gaps(pcs)
                report[f"{name}|{size}|{'open' if open_ else 'rest'}"] = {"shift": [round(sh[0], 3), round(sh[1], 3)],
                                                                           "max_snap_px": round(worst, 3), "min_gap_px": round(g, 2), "overlap": ov}
            for size, m in masters.items():
                U = C.UNITS[size]
                C.master_file(name, size, open_).write_text(C.svg(m, U, "Charcoal-Red", title=title(name, size, open_), carry_keyline=True))
                cws = ["Charcoal", "Charcoal-No-Red", "Newsprint-Red", "Newsprint", "Newsprint-No-Red", "White", "White-No-Red"]
                if open_ and size != "Display":
                    cws.append("Charcoal-Red-Keyline")
                for cw in cws:
                    C.variant_file(name, size, cw, open_).write_text(C.svg(m, U, cw, title=title(name, size, open_, cw)))
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    (C.SCRATCH / "hint-report.json").write_text(json.dumps(report, indent=1))
    return report


def sheet(names=None, out="hint-sheet"):
    """Magnified review sheet: each master at 12x with its pixel grid, at rest and open, and at 1x."""
    rows = []
    for name in names or D.ICONS:
        cells = []
        for size in ("Display", "24px", "16px"):
            for open_ in (False, True):
                m = C.load(name, size, open_)
                U = C.UNITS[size]
                px = 288 if size != "16px" else 192
                grid = "" if size == "Display" else "".join(
                    f'<path d="M{i} 0V{U}M0 {i}H{U}" stroke="#0003" stroke-width="{1 / 12:.4f}"/>' for i in range(1, U))
                cw = "Charcoal-Red-Keyline" if (open_ and size != "Display") else "Charcoal-Red"
                body = C.svg(m, U, cw, px=px, bg=C.NEWS).replace("</svg>", grid + "</svg>")
                big = C.svg(m, U, cw, px=U * 12, bg=C.NEWS) if size != "Display" else ""
                one = C.svg(m, U, cw, bg=C.NEWS)
                cells.append(f'<div style="display:inline-block;margin:0 10px 6px 0;vertical-align:bottom">{body}<div>{one} {size}{" open" if open_ else ""}</div></div>')
        rows.append(f'<div style="margin-bottom:14px;white-space:nowrap"><b>{D.LABELS[name]}</b><br>{"".join(cells)}</div>')
    # a 1x render of the hinted sizes, magnified without smoothing, to see the real pixels
    html = f'<html><body style="margin:0;padding:12px;background:#C9C5BC;font:12px sans-serif">{"".join(rows)}</body></html>'
    p = C.SCRATCH / f"{out}.html"
    p.write_text(html)
    subprocess.run(["node", str(C.SHOT_JS), str(p), str(C.SCRATCH / f"{out}.png"), "1900", "1"], check=True)


def pixel_sheet(names=None, out="pixel-sheet"):
    """Each hinted master rendered by Chromium at 1x, then magnified 10x without smoothing."""
    from PIL import Image
    jobs = []
    for name in names or D.ICONS:
        for size in ("24px", "16px"):
            for open_ in (False, True):
                m = C.load(name, size, open_)
                U = C.UNITS[size]
                cw = "Charcoal-Red-Keyline" if open_ else "Charcoal-Red"
                jobs.append({"id": f"{name}-{size}-{int(open_)}", "w": U, "h": U, "bg": C.NEWS, "html": C.svg(m, U, cw)})
    jp = C.SCRATCH / "pixel-jobs.json"
    jp.write_text(json.dumps(jobs))
    rd = C.SCRATCH / "pixel"
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(rd)], check=True)
    names = names or D.ICONS
    k = 10
    W = (24 + 24 + 16 + 16) * k + 5 * 12
    H = len(names) * (24 * k + 12) + 12
    sheet_im = Image.new("RGB", (W, H), (201, 197, 188))
    for r, name in enumerate(names):
        x = 12
        for size in ("24px", "16px"):
            for open_ in (False, True):
                im = Image.open(rd / f"{name}-{size}-{int(open_)}.png").convert("RGB")
                im = im.resize((im.width * k, im.height * k), Image.NEAREST)
                sheet_im.paste(im, (x, 12 + r * (24 * k + 12)))
                x += im.width + 12
    sheet_im.save(C.SCRATCH / f"{out}.png")


if __name__ == "__main__":
    rep = write_all()
    for k, v in rep.items():
        print(k, v)
    if "--sheet" in sys.argv:
        pixel_sheet()
