#!/usr/bin/env python3
"""Concept 08, Star Atlas. Builds 20261030_Concept-08-Star-Atlas.html beside this script.

Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/08-star-atlas/build_concept.py

Reads only the model export, the shared helpers, the kit, the wordmark masters and the Civic Line icons.
Every label, sign, grade, delay, count and title on the page comes from the model; the script asserts the
facts the page states in words (the brightest star, the counts, the loop kinds).
"""
import html
import importlib.util
import json
import math
import pathlib
import re
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

OUT = HERE / '20261030_Concept-08-Star-Atlas.html'
M = acc.load_model()
NODES, LINKS, LOOPS, REFORMS = M['nodes'], M['links'], M['loops'], M['reforms']
ORDER, LOOP_ORDER, GROUPS = M['order'], M['loop_order'], M['groups']
AREAS = {a['id']: a for a in M['areas']}
AREA_ORDER = [a['id'] for a in M['areas']]
AREA_OF = {}
for a in M['areas']:
    for n in a['nodes']:
        AREA_OF[n] = a['id']
COUNTS = M['generated']['counts']

P = acc.PALETTE
NEWS, CHAR, RED, STONE, WHITE, DIM = P['newsprint'], P['charcoal'], P['pillar_red'], P['stone'], P['white'], P['dim_newsprint']
MINUS = '−'

# ------------------------------------------------------------------ model facts used by the drawing
OUT_L, IN_L = defaultdict(list), defaultdict(list)
for l in LINKS.values():
    OUT_L[l['from']].append(l)
    IN_L[l['to']].append(l)
DEG = {n: len(OUT_L[n]) + len(IN_L[n]) for n in ORDER}
LOOP_LINKS = [k for k, l in LINKS.items() if l['loops']]
ON_LOOP = {n for n in ORDER if NODES[n]['loops']}
NUMBERED = [k for k in LOOP_ORDER if not LOOPS[k]['conceptual']]
SKETCHES = [k for k in LOOP_ORDER if LOOPS[k]['conceptual']]

# The pitch's claim, checked: policy tilt to insiders (E1) has the most connections, and alone.
_top = max(DEG.values())
assert [n for n in ORDER if DEG[n] == _top] == ['E1'] and _top == 13, 'E1 must be the single brightest star'
assert len(LOOP_LINKS) == 46 and len(ON_LOOP) == 25
assert sum(1 for l in LOOPS.values() if l['type'] == 'R') == 18 and sum(1 for l in LOOPS.values() if l['type'] == 'B') == 5

# Brightness classes: a star's size counts every connection it has, like a magnitude scale.
MAG = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 11), (12, 13)]
MAG_R = [2.5, 3.5, 4.75, 6.0, 7.5, 10.0]          # radius in px at overview scale


def mag(n):
    d = DEG[n]
    for i, (lo, hi) in enumerate(MAG):
        if lo <= d <= hi:
            return i
    raise ValueError(n)


assert [n for n in ORDER if mag(n) == 5] == ['E1']


def star_r(n, k=1.0):
    return MAG_R[mag(n)] * k


def esc(s):
    return html.escape(str(s), quote=True)


def f1(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def f2(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


# ------------------------------------------------------------------ text measurement
try:
    from PIL import ImageFont
    _FD = pathlib.Path('/usr/share/fonts/opentype/inter')
    _FONTS = {w: ImageFont.truetype(str(_FD / f'Inter-{n}.otf'), 100) for w, n in
              ((400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold'))}
except Exception:   # fall back to an average advance when the local Inter files are missing
    _FONTS = {}


def text_w(s, size, weight=500, track=0.0, tight=False):
    if _FONTS:
        w = _FONTS[weight].getlength(s) * size / 100
    else:
        w = len(s) * size * 0.56
    w += track * size * len(s)
    if tight:
        w *= 0.94
    return w * 1.04 + 1


# ------------------------------------------------------------------ the sky: regions and stars
SKY_W, SKY_H = 978, 568
X_BAND = (0, 0, SKY_W, 70)
CORE_TOP, CORE_MID, CORE_BOT = 70, 276, 438
FRAMES = {
    'X': (0, 0, SKY_W, CORE_TOP),
    'A': (0, CORE_TOP, 300, CORE_MID), 'B': (300, CORE_TOP, 628, CORE_MID), 'C': (628, CORE_TOP, SKY_W, CORE_MID),
    'E': (0, CORE_MID, 340, CORE_BOT), 'D': (340, CORE_MID, SKY_W, CORE_BOT),
    'money': (0, CORE_BOT, 222, SKY_H), 'household': (222, CORE_BOT, 444, SKY_H),
    'production': (444, CORE_BOT, 666, SKY_H), 'TC': (666, CORE_BOT, SKY_W, SKY_H),
}
REGION_NAME = {a: AREAS[a]['title'] for a in AREA_ORDER}
CORE = ('A', 'B', 'C', 'D', 'E')
# The five core areas keep V7's ring order: A, B and C across the top, then D and E back along the bottom.
ANCHOR = {'A': (170, 180), 'B': (440, 160), 'C': (760, 170), 'D': (660, 360), 'E': (330, 350)}


def plan_start():
    """Each star starts at its slot on the shared plan (Loop-Route-Geometry), mapped into its region's frame."""
    g = json.loads((acc.SHARED / '20261030_Loop-Route-Geometry.json').read_text())['plan']
    pos = {}
    for n, v in g['variables'].items():
        a = v['area']
        bx0, by0, bx1, by1 = g['boxes'][a]
        fx0, fy0, fx1, fy1 = FRAMES[a]
        mx = 30 if a not in ('X',) else 40
        my = 28 if a in ('A', 'B', 'C', 'D', 'E') else 20
        u = (v['x'] - bx0) / (bx1 - bx0)
        w = (v['y'] - by0) / (by1 - by0)
        pos[n] = [fx0 + mx + u * (fx1 - fx0 - 2 * mx), fy0 + my + w * (fy1 - fy0 - 2 * my)]
    return pos


# Hand nudges, in px, applied after the search so labels and figures have room. Positions carry no meaning
# beyond the region a star sits in; the page says so.
NUDGE = {}


def _seg_cross(p1, p2, p3, p4):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return (d1 > 0) != (d2 > 0) and (d3 > 0) != (d4 > 0)


def _pt_seg(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy or 1e-9
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def search(pos, iters=40000, seed=8):
    """A seeded local search. Each star stays inside its region's frame. The score counts crossings between
    figure lines, figure lines that pass close to a star they do not join, stars set too close together, and
    the length of connections, so connected stars sit near each other."""
    import random
    rnd = random.Random(seed)
    pairs = sorted({tuple(sorted((LINKS[k]['from'], LINKS[k]['to']))) for k in LOOP_LINKS})
    other = sorted({tuple(sorted((l['from'], l['to']))) for k, l in LINKS.items() if not l['loops']} - set(pairs))
    touch = defaultdict(list)
    for i, (a, b) in enumerate(pairs):
        touch[a].append(i)
        touch[b].append(i)
    otouch = defaultdict(list)
    for a, b in other:
        otouch[a].append(b)
        otouch[b].append(a)

    def box(n):
        if AREA_OF[n] in CORE:
            return 34, CORE_TOP + 30, SKY_W - 34, CORE_BOT - 30
        fx0, fy0, fx1, fy1 = FRAMES[AREA_OF[n]]
        mx = 30
        my = 24 if AREA_OF[n] == 'X' else 30
        return fx0 + mx, fy0 + my, fx1 - mx, fy1 - my

    def local(n, P):
        c = 0.0
        x, y = P[n]
        for m in ORDER:                                   # spacing
            if m != n:
                d = math.hypot(x - P[m][0], y - P[m][1])
                need = 76 if (n in ON_LOOP and m in ON_LOOP) else 52
                if d < need:
                    c += (need - d) ** 2 * 0.6
        if AREA_OF[n] in CORE:                            # soft pull toward the area's place in the ring
            ax, ay = ANCHOR[AREA_OF[n]]
            d = math.hypot(x - ax, y - ay)
            if d > 110:
                c += (d - 110) ** 2 * 0.05
        for m in otouch[n]:                               # other connections pull gently
            c += math.hypot(x - P[m][0], y - P[m][1]) * 0.012
        mine = touch[n]
        for i in mine:                                    # figure lines that touch this star
            a, b = pairs[i]
            L = math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1])
            c += L * 0.18
            if L < 86:
                c += (86 - L) ** 2 * 0.5
            if L > 230:
                c += (L - 230) ** 2 * 0.02
            for j in range(len(pairs)):
                if j == i:
                    continue
                c2, d2 = pairs[j]
                if len({a, b, c2, d2}) < 4:
                    continue
                if _seg_cross(P[a], P[b], P[c2], P[d2]):
                    c += 220
            for m in ORDER:
                if m in (a, b):
                    continue
                dd = _pt_seg(P[m], P[a], P[b])
                lim = star_r(m) + 18
                if dd < lim:
                    c += (lim - dd) ** 2 * 3
        for j, (a, b) in enumerate(pairs):                # this star close to lines it does not join
            if n in (a, b):
                continue
            dd = _pt_seg(P[n], P[a], P[b])
            lim = star_r(n) + 18
            if dd < lim:
                c += (lim - dd) ** 2 * 3
        return c

    def total(P):
        return sum(local(n, P) for n in ORDER) / 2

    P = {n: list(p) for n, p in pos.items()}
    for n in ORDER:                                       # a seeded scatter, so each seed explores a new start
        x0, y0, x1, y1 = box(n)
        if AREA_OF[n] in CORE:
            ax, ay = ANCHOR[AREA_OF[n]]
            P[n] = [min(max(ax + rnd.uniform(-120, 120), x0), x1), min(max(ay + rnd.uniform(-80, 80), y0), y1)]
    T = 60.0
    for it in range(iters):
        n = ORDER[rnd.randrange(len(ORDER))]
        x0, y0, x1, y1 = box(n)
        old = P[n][:]
        before = local(n, P)
        step = 90 * (1 - it / iters) + 6
        P[n] = [min(max(old[0] + rnd.uniform(-step, step), x0), x1), min(max(old[1] + rnd.uniform(-step, step), y0), y1)]
        after = local(n, P)
        if not (after < before or rnd.random() < math.exp((before - after) / max(T, 1e-3))):
            P[n] = old
        T *= 0.99985
    return P, total(P)


def count_crossings(P):
    pairs = sorted({tuple(sorted((LINKS[k]['from'], LINKS[k]['to']))) for k in LOOP_LINKS})
    n = 0
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            a, b = pairs[i]
            c, d = pairs[j]
            if len({a, b, c, d}) == 4 and _seg_cross(P[a], P[b], P[c], P[d]):
                n += 1
    return n


def place():
    cache = HERE / 'sky_positions.json'
    if cache.exists():
        P = json.loads(cache.read_text())
    else:
        best = None
        for seed in range(1, 13):
            Q, score = search(plan_start(), seed=seed)
            crossings = count_crossings(Q)
            print(f'  layout seed {seed}: score {score:.0f}, figure crossings {crossings}')
            if best is None or score < best[1]:
                best = (Q, score, seed)
        P = best[0]
        print('  kept seed', best[2])
        P = {n: [round(p[0]), round(p[1])] for n, p in P.items()}
        cache.write_text(json.dumps(P, indent=0))
    for n, (dx, dy) in NUDGE.items():
        P[n] = [P[n][0] + dx, P[n][1] + dy]
    return {n: (P[n][0], P[n][1]) for n in ORDER}


STAR = place()

CELL = 16


def regions():
    """Stepped borders, as astronomers draw them: each grid cell joins the region of the nearest star, with a
    pull toward the region's frame so the ten areas keep the ring order of the shared plan."""
    nx, ny = math.ceil(SKY_W / CELL), math.ceil(SKY_H / CELL)
    grid = {}
    for gx in range(nx):
        for gy in range(ny):
            x, y = (gx + 0.5) * CELL, (gy + 0.5) * CELL
            best, bd = None, 1e9
            for a in AREA_ORDER:
                fx0, fy0, fx1, fy1 = FRAMES[a]
                inside = fx0 <= x <= fx1 and fy0 <= y <= fy1
                ddx = max(fx0 - x, 0, x - fx1)
                ddy = max(fy0 - y, 0, y - fy1)
                dframe = math.hypot(ddx, ddy)
                dstar = min(math.hypot(STAR[n][0] - x, STAR[n][1] - y) for n in AREAS[a]['nodes'])
                score = dstar * 0.45 + dframe * 3.0 - (26 if inside else 0)
                if score < bd:
                    bd, best = score, a
            grid[(gx, gy)] = best
    # smooth single-cell teeth twice, then keep each region in one piece
    for _ in range(2):
        g2 = dict(grid)
        for (gx, gy), a in grid.items():
            ns = [grid.get((gx + dx, gy + dy)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            c = Counter(v for v in ns if v)
            top, cnt = c.most_common(1)[0]
            if top != a and cnt >= 3:
                g2[(gx, gy)] = top
        grid = g2
    # a star's own cell always belongs to its region
    for n in ORDER:
        grid[(int(STAR[n][0] // CELL), int(STAR[n][1] // CELL))] = AREA_OF[n]
    return grid, nx, ny


GRID, GNX, GNY = regions()


def region_outline(grid, a, x0=0.0, y0=0.0, k=1.0, clip=None):
    """Trace the cells of region a into closed polygons (path d)."""
    edges = {}
    W, H = SKY_W, SKY_H

    def cx(gx):
        return min(gx * CELL, W)

    def cy(gy):
        return min(gy * CELL, H)
    for (gx, gy), v in grid.items():
        if v != a:
            continue
        # directed edges with the region on the left (clockwise in screen space)
        if grid.get((gx, gy - 1)) != a:
            edges[(cx(gx), cy(gy))] = (cx(gx + 1), cy(gy))
        if grid.get((gx + 1, gy)) != a:
            edges[(cx(gx + 1), cy(gy))] = (cx(gx + 1), cy(gy + 1))
        if grid.get((gx, gy + 1)) != a:
            edges[(cx(gx + 1), cy(gy + 1))] = (cx(gx), cy(gy + 1))
        if grid.get((gx - 1, gy)) != a:
            edges[(cx(gx), cy(gy + 1))] = (cx(gx), cy(gy))
    loops = []
    while edges:
        start, nxt = next(iter(edges.items()))
        pts = [start]
        del edges[start]
        cur = nxt
        while cur != start and cur in edges:
            pts.append(cur)
            cur = edges.pop(cur)
        # drop collinear points
        clean = []
        for i, p in enumerate(pts):
            pa, pb = pts[i - 1], pts[(i + 1) % len(pts)]
            if (pa[0] == p[0] == pb[0]) or (pa[1] == p[1] == pb[1]):
                continue
            clean.append(p)
        loops.append(clean)
    d = ''
    for pts in loops:
        d += 'M' + 'L'.join(f'{f1(x0 + p[0] * k)} {f1(y0 + p[1] * k)}' for p in pts) + 'Z'
    return d


def border_segments(grid):
    """Every cell edge between two regions, merged into straight runs: the stepped borders."""
    h, v = defaultdict(list), defaultdict(list)
    for (gx, gy), a in grid.items():
        b = grid.get((gx + 1, gy))
        if b and b != a:
            v[(gx + 1) * CELL].append(gy)
        b = grid.get((gx, gy + 1))
        if b and b != a:
            h[(gy + 1) * CELL].append(gx)
    segs = []
    for x, ys in v.items():
        ys = sorted(ys)
        s = ys[0]
        for i in range(1, len(ys) + 1):
            if i == len(ys) or ys[i] != ys[i - 1] + 1:
                segs.append(((x, s * CELL), (x, min((ys[i - 1] + 1) * CELL, SKY_H))))
                if i < len(ys):
                    s = ys[i]
    for y, xs in h.items():
        xs = sorted(xs)
        s = xs[0]
        for i in range(1, len(xs) + 1):
            if i == len(xs) or xs[i] != xs[i - 1] + 1:
                segs.append(((s * CELL, y), (min((xs[i - 1] + 1) * CELL, SKY_W), y)))
                if i < len(xs):
                    s = xs[i]
    return segs


if __name__ == '__main__' and False:
    pass
