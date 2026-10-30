"""Loop-route thumbnails: the study for DR-15, built from the committed V7 export (DR-20).

Run from the project root:
    python3 -I work/build/scripts/phase-2/atlas_loop_routes.py

Writes
    work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Geometry.json
    work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Thumbnails-Study.html
    work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Thumbnails-Study.png   (1440 px wide)

Stages
 1. plan()      the canonical plan: ten areas in three tiers, a slot grid in each, and every variable placed
                by one stated rule (barycentric assignment, below).
 2. route()     each loop drawn as its route across the plan: one arc per step, the V7 line code, the sign,
                the direction, the closing step and the start station.
 3. measure()   renders every thumbnail in Chromium and scores each pair with the D1-16 method.
 4. contract()  the counts behind the data contract per level and the overview options (memo Parts 2 and 3).
 5. page()      the study page on Newsprint and Charcoal, and its 1440 px capture.

Nothing here types a label, sign or grade: every one is read from the model export.
"""
import base64
import collections
import html
import importlib.util
import io
import itertools
import json
import math
import pathlib
import subprocess

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('acc', HERE / 'atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

ROOT = acc.ROOT
SHARED = acc.SHARED
OUT_JSON = SHARED / '20261030_Loop-Route-Geometry.json'
OUT_HTML = SHARED / '20261030_Loop-Route-Thumbnails-Study.html'
OUT_PNG = SHARED / '20261030_Loop-Route-Thumbnails-Study.png'
M = acc.load_model()
NODES, LINKS, LOOPS = M['nodes'], M['links'], M['loops']
AREAS = {a['id']: a for a in M['areas']}
AREA_OF = {v: a['id'] for a in M['areas'] for v in a['nodes']}
P = acc.PALETTE

# ---------------------------------------------------------------------------------------------------------------
# 1. The canonical plan
# ---------------------------------------------------------------------------------------------------------------
# Three tiers, read top to bottom: the outside drivers (X) over the whole system; the civic core, areas A to E
# left to right in V7's lettering, which is also the main current of the model (economy, political inputs,
# elections, institutions, legitimacy); and the ground, the economy layer's three areas and the technology layer.
# Units: one core column = 1.0. Core rows are 1.0 apart; the outer tiers hold no loop station, so their rows are
# 0.6 apart and the core takes most of the height. A concept may rescale a tier; it keeps the order and the slots.
CORE = [('A', 2), ('B', 2), ('C', 2), ('D', 3), ('E', 1)]         # (area, columns); three rows each
CORE_ROWS, CORE_PITCH = 3, 1.0
GROUND_AREAS = {'production': 2, 'household': 2, 'money': 2, 'TC': 4}   # columns; two rows each
GROUND_ROWS, OUTER_PITCH = 2, 0.6
PAD = 0.5            # an area outline sits half a column outside its outermost slots
CORE_GAP = 0.30      # space between two core outlines
TIER_GAP = 0.42      # space between tiers
WIDTH = sum(c for _, c in CORE) * 1.0 + (len(CORE) - 1) * CORE_GAP       # 11.2 columns, outline to outline


def _columns(spec, gap):
    """x of every slot column, per area, for a tier whose outlines span the full plan width."""
    xs, x = {}, PAD
    for area, cols in spec:
        xs[area] = [x + i for i in range(cols)]
        x += cols - 1 + 2 * PAD + gap
    return xs


def _tiers(ground_order):
    gcols = [(a, GROUND_AREAS[a]) for a in ground_order]
    ggap = (WIDTH - sum(c for _, c in gcols)) / (len(gcols) - 1)
    y_x = 0.4                                               # the X row, inside an outline 0.8 tall
    core_top = 0.8 + TIER_GAP
    core_y = [core_top + PAD + r * CORE_PITCH for r in range(CORE_ROWS)]
    core_bottom = core_y[-1] + PAD
    ground_top = core_bottom + TIER_GAP
    ground_y = [ground_top + 0.4 + r * OUTER_PITCH for r in range(GROUND_ROWS)]
    height = ground_y[-1] + 0.4
    slots, boxes = {}, {}
    cx = _columns(CORE, CORE_GAP)
    for area, cols in CORE:
        slots[area] = [(x, y) for y in core_y for x in cx[area]]
        boxes[area] = (cx[area][0] - PAD, core_top, cx[area][-1] + PAD, core_bottom)
    gx = _columns(gcols, ggap)
    for area, cols in gcols:
        slots[area] = [(x, y) for y in ground_y for x in gx[area]]
        boxes[area] = (gx[area][0] - PAD, ground_top, gx[area][-1] + PAD, ground_top + 0.8 + OUTER_PITCH)
    xcols = [x for a, _ in CORE for x in cx[a]]
    slots['X'] = [(x, y_x) for x in xcols]
    boxes['X'] = (0.0, 0.0, WIDTH, 0.8)
    return slots, boxes, height


def _neighbors():
    nb = collections.defaultdict(list)
    for l in LINKS.values():
        nb[l['from']].append(l['to'])
        nb[l['to']].append(l['from'])
    return nb


def _hungarian(cost):
    """Minimum-cost assignment of n rows to m >= n columns (Kuhn-Munkres with potentials). Returns col per row."""
    n, m = len(cost), len(cost[0])
    INF = float('inf')
    u, v, p, way = [0.0] * (n + 1), [0.0] * (m + 1), [0] * (m + 1), [0] * (m + 1)
    for i in range(1, n + 1):
        p[0], j0 = i, 0
        minv, used = [INF] * (m + 1), [False] * (m + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], INF, 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j] - 1e-12:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta - 1e-12:
                        delta, j1 = minv[j], j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    out = [0] * n
    for j in range(1, m + 1):
        if p[j]:
            out[p[j] - 1] = j - 1
    return out


def _assign(area, slots, pos, nb):
    """Give each variable of one area the slot that brings the area closest to its partners' current places:
    the sum of squared distances from each variable's slot to the mean place of its partners is the least."""
    vs = AREAS[area]['nodes']
    targets = []
    for v in vs:
        pts = [pos[u] for u in nb[v]]
        targets.append((sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)))
    cost = [[(sx - tx) ** 2 + (sy - ty) ** 2 for sx, sy in slots] for tx, ty in targets]
    cols = _hungarian(cost)
    return {v: slots[c] for v, c in zip(vs, cols)}, sum(cost[i][c] for i, c in enumerate(cols))


def _place(slots):
    """Barycentric placement on slots. Start in V7 order, then repeat one assignment per area (in V7's area order)
    until no variable moves. Every one of the 118 connections pulls, whatever its type."""
    nb = _neighbors()
    pos = {}
    for area, a in AREAS.items():
        for v, s in zip(a['nodes'], slots[area]):
            pos[v] = s
    seen = []
    for it in range(60):
        moved = 0
        for area in AREAS:
            new, _ = _assign(area, slots[area], pos, nb)
            moved += sum(1 for v in new if new[v] != pos[v])
            pos.update(new)
        key = tuple(sorted(pos.items()))
        if moved == 0 or key in seen:
            break
        seen.append(key)
    total = sum(math.dist(pos[l['from']], pos[l['to']]) for l in LINKS.values())
    return pos, total, it + 1


def plan():
    """Try every order of the ground tier's four areas; keep the order with the shortest total connection length."""
    trials = []
    for order in itertools.permutations(GROUND_AREAS):
        slots, boxes, height = _tiers(order)
        pos, total, rounds = _place(slots)
        trials.append((round(total, 4), order, slots, boxes, height, pos, rounds))
    trials.sort(key=lambda t: (t[0], t[1]))
    total, order, slots, boxes, height, pos, rounds = trials[0]
    return {'ground_order': list(order), 'slots': slots, 'boxes': boxes, 'width': WIDTH, 'height': height,
            'pos': pos, 'total_length': total, 'rounds': rounds,
            'trials': [{'order': list(t[1]), 'total_length': t[0]} for t in trials]}


# ---------------------------------------------------------------------------------------------------------------
# 2. Routes
# ---------------------------------------------------------------------------------------------------------------
# The frame around the plan holds the three sketched loops, whose stations are not variables on the map.
MARGIN = {'left': 0.9, 'right': 0.9, 'top': 0.3, 'bottom': 0.9}
BULGE_TWO, BULGE_MANY, BULGE_MAX = 0.5, 0.2, 0.62   # sagitta as a share of the chord, and its cap, in columns


def frame(pl):
    W = pl['width'] + MARGIN['left'] + MARGIN['right']
    H = pl['height'] + MARGIN['top'] + MARGIN['bottom']
    return {'x0': -MARGIN['left'], 'y0': -MARGIN['top'], 'w': W, 'h': H}


def _sketch_places(lid, pl):
    """Stations that are not V7 variables sit in the frame outside the plan, never inside an area, beside the
    variables that tie the sketch to the model: a variable the loop names (R9: E2), or else the variables its
    reforms target (V7 reforms[].targets). They take the plan edge nearest those variables."""
    lp = LOOPS[lid]
    on = [s['code'] for s in lp['stations'] if s['is_variable']]
    if on:
        anchors, basis = on, 'station'
    else:
        anchors = sorted({t for r in lp['reforms'] for t in M['reforms'][r]['targets'] if t in NODES})
        basis = 'reform targets'
    ax = sum(pl['pos'][v][0] for v in anchors) / len(anchors)
    ay = sum(pl['pos'][v][1] for v in anchors) / len(anchors)
    W, H = pl['width'], pl['height']
    dist = {'left': ax, 'right': W - ax, 'top': ay, 'bottom': H - ay}
    side = min(dist, key=lambda k: (dist[k], k))
    off = [i for i, s in enumerate(lp['stations']) if not s['is_variable']]
    k = len(off)
    places = {}
    for j, i in enumerate(off):
        t = (j - (k - 1) / 2) * 1.0                       # one column apart along the edge
        inner = 0.28 if (k == 3 and j != 1) else 0.62    # three stations make a small triangle, not a line
        if side in ('left', 'right'):
            x = -MARGIN['left'] * inner if side == 'left' else W + MARGIN['right'] * inner
            places[i] = (x, ay + t)
        else:
            y = H + MARGIN['bottom'] * inner if side == 'bottom' else -MARGIN['top'] * inner
            places[i] = (ax + t, y)
    return places, {'anchors': anchors, 'anchor_basis': basis, 'side': side, 'anchor_point': [round(ax, 4), round(ay, 4)]}


def _arc(a, b, side, h):
    """Circular arc from a to b bulging by sagitta h to the given side (+1: right of travel, -1: left)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L                                   # right of travel on screen (y down)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    R = (L * L / 4 + h * h) / (2 * h)
    apex = (mx + side * nx * h, my + side * ny * h)
    c = (apex[0] - side * nx * R, apex[1] - side * ny * R)
    return {'a': a, 'b': b, 'center': c, 'radius': R, 'sagitta': h, 'side': side, 'apex': apex, 'chord': L,
            'large': 1 if h > R else 0, 'sweep': 1 if side > 0 else 0}


def arc_points(arc, n=96):
    """Sample an arc from a to b through its apex."""
    cx, cy = arc['center']
    ta = math.atan2(arc['a'][1] - cy, arc['a'][0] - cx)
    tb = math.atan2(arc['b'][1] - cy, arc['b'][0] - cx)
    tp = math.atan2(arc['apex'][1] - cy, arc['apex'][0] - cx)

    def norm(t):
        while t < 0:
            t += 2 * math.pi
        while t >= 2 * math.pi:
            t -= 2 * math.pi
        return t
    span_ccw = norm(tb - ta)                  # going with increasing angle
    through = norm(tp - ta) <= span_ccw
    span = span_ccw if through else -(2 * math.pi - span_ccw)
    R = arc['radius']
    return [(cx + R * math.cos(ta + span * i / n), cy + R * math.sin(ta + span * i / n)) for i in range(n + 1)]


def route(lid, pl):
    lp = LOOPS[lid]
    sketch = lp['conceptual']
    places, sk = (_sketch_places(lid, pl) if sketch else ({}, None))
    st = []
    for i, s in enumerate(lp['stations']):
        on = bool(s['is_variable'] and s['code'])
        pos = pl['pos'][s['code']] if on else places[i]
        st.append({'index': i, 'code': s['code'], 'label': s['label'], 'on_plan': on, 'area': s['area'], 'pos': list(pos)})
    n = len(st)
    cx = sum(s['pos'][0] for s in st) / n
    cy = sum(s['pos'][1] for s in st) / n
    steps = []
    for i, step in enumerate(lp['steps']):
        a, b = st[i]['pos'], st[(i + 1) % n]['pos']
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        out = (mx - cx) * nx + (my - cy) * ny
        side = 1 if (n == 2 or abs(out) < 1e-6) else (1 if out > 0 else -1)
        if n == 2:
            side = 1                       # a two-station loop: each step bulges right of travel, so the two make a ring
        h = min((BULGE_TWO if n == 2 else BULGE_MANY) * L, BULGE_MAX)
        arc = _arc(a, b, side, h)
        steps.append({'index': i + 1, 'id': step['id'], 'from': step['from'], 'to': step['to'],
                      'from_label': step['from_label'], 'to_label': step['to_label'], 'polarity': step['polarity'],
                      'type': step['type'], 'delay': step['delay'], 'evidence': step['evidence'],
                      'closing': step['closing'], 'sketch': step['conceptual'], 'arc': arc})
    return {'loop': lid, 'stations': st, 'steps': steps, 'sketch': sk}


# ---------------------------------------------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------------------------------------------
esc = html.escape
MINUS = '−'
DASH = {'documented': None, 'well-supported': None, 'plausible': '9 4', 'plausible_contested': '9 3 2 3', 'hypothesis': '2 4'}


def dash(grade, weight):
    code = DASH[grade]
    if code is None:
        return None
    k = weight / 2.0
    return ' '.join(f'{float(x) * k:.2f}' for x in code.split())


def _f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def _along(pts):
    acc_, out = 0.0, [0.0]
    for i in range(1, len(pts)):
        acc_ += math.dist(pts[i - 1], pts[i])
        out.append(acc_)
    return out


def _at(pts, cum, s):
    """Point and unit tangent at arc length s along a polyline."""
    s = max(0.0, min(cum[-1], s))
    for i in range(1, len(pts)):
        if cum[i] >= s:
            t = (s - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            x = pts[i - 1][0] + t * (pts[i][0] - pts[i - 1][0])
            y = pts[i - 1][1] + t * (pts[i][1] - pts[i - 1][1])
            dx, dy = pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]
            L = math.hypot(dx, dy) or 1
            return (x, y), (dx / L, dy / L)
    return pts[-1], (1, 0)
