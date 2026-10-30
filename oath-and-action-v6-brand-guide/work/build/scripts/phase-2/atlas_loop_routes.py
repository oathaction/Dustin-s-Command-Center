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
# Three tiers, read top to bottom: the outside drivers (X) over the system; the civic core; and the ground, the
# economy layer's three areas and the technology layer. The core is a ring in V7's letter order: A, B and C across
# the top, then D and E back along the bottom, so the model's main current (economy, political inputs, elections,
# institutions, legitimacy, and back to the economy) runs clockwise. The core's 38 cross-area connections join only
# A-B, B-C, C-D, D-E, E-A, B-D and B-E, so in the ring every one of them joins two neighboring areas; in a single
# A-to-E row, 10 of them would jump over an area (computed in contract()).
# Units: one top-row core column = 1.0. Core rows are 1.0 apart. The outer tiers hold no loop station, so their
# rows sit closer and the core takes most of the height. A concept may rescale a tier; it keeps the order and slots.
TOP = [('A', 2), ('B', 2), ('C', 2)]                 # (area, columns), three rows each
BOTTOM = [('E', 2), ('D', 4)]                        # two rows each; E sits under A, D under B and C
TOP_ROWS, BOTTOM_ROWS, CORE_PITCH = 3, 2, 1.0
GROUND_AREAS = {'production': 2, 'household': 2, 'money': 2, 'TC': 4}   # columns; two rows each
GROUND_ROWS, GROUND_PITCH_Y, GROUND_PAD = 2, 0.42, 0.3
PAD = 0.5            # a core outline sits half a column outside its outermost slots
CORE_GAP = 0.30      # space between two core outlines
TIER_GAP = 0.36      # space between tiers
WIDTH = sum(c for _, c in TOP) + (len(TOP) - 1) * CORE_GAP        # 6.6 columns, outline to outline


def _tiers(ground_order):
    slots, boxes = {}, {}
    xs_top, x = {}, 0.0
    for area, cols in TOP:
        xs_top[area] = [x + PAD + i for i in range(cols)]
        boxes[area] = [x, None, x + cols, None]
        x += cols + CORE_GAP
    y_x = 0.3                                               # the X row, inside an outline 0.6 tall
    top0 = 0.6 + TIER_GAP
    top_y = [top0 + PAD + r * CORE_PITCH for r in range(TOP_ROWS)]
    top1 = top_y[-1] + PAD
    bot0 = top1 + CORE_GAP
    bot_y = [bot0 + PAD + r * CORE_PITCH for r in range(BOTTOM_ROWS)]
    bot1 = bot_y[-1] + PAD
    for area, cols in TOP:
        boxes[area][1], boxes[area][3] = top0, top1
        slots[area] = [(xx, yy) for yy in top_y for xx in xs_top[area]]
    # bottom row: E under A, D from B's left edge to C's right edge
    e0, e1 = boxes['A'][0], boxes['A'][2]
    d0, d1 = boxes['B'][0], boxes['C'][2]
    for area, (x0, x1), cols in (('E', (e0, e1), 2), ('D', (d0, d1), 4)):
        pitch = (x1 - x0 - 2 * PAD) / (cols - 1)
        xs = [x0 + PAD + i * pitch for i in range(cols)]
        slots[area] = [(xx, yy) for yy in bot_y for xx in xs]
        boxes[area] = [x0, bot0, x1, bot1]
    slots['X'] = [(xx, y_x) for a, _ in TOP for xx in xs_top[a]]
    boxes['X'] = [0.0, 0.0, WIDTH, 0.6]
    # ground: four areas in one row under the core, filling the plan's width
    g0 = bot1 + TIER_GAP
    gcols = [(a, GROUND_AREAS[a]) for a in ground_order]
    gap = 0.25
    pitch = (WIDTH - gap * (len(gcols) - 1) - 2 * GROUND_PAD * len(gcols)) / sum(c - 1 for _, c in gcols)
    gy = [g0 + 0.3 + r * GROUND_PITCH_Y for r in range(GROUND_ROWS)]
    x = 0.0
    for area, cols in gcols:
        xs = [x + GROUND_PAD + i * pitch for i in range(cols)]
        slots[area] = [(xx, yy) for yy in gy for xx in xs]
        w = (cols - 1) * pitch + 2 * GROUND_PAD
        boxes[area] = [x, g0, x + w, gy[-1] + 0.3]
        x += w + gap
    height = gy[-1] + 0.3
    return slots, {k: tuple(v) for k, v in boxes.items()}, height


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
MARGIN = {'left': 0.95, 'right': 0.25, 'top': 0.25, 'bottom': 0.25}
BULGE_TWO, BULGE_MANY, BULGE_INLINE, BULGE_MAX = 0.5, 0.2, 0.34, 0.62   # sagitta as a share of the chord; cap in columns


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
    gap = 0.8 if len(lp['stations']) == 2 else 1.0     # off-plan stations sit 0.8 to 1 column apart
    depth = MARGIN[side]
    for j, i in enumerate(off):
        t = (j - (k - 1) / 2) * gap
        # two stations stand on the margin's center line, so their ring (sagitta 0.4) stays inside the margin;
        # three make a small triangle, the middle one further out
        inner = 0.5 if k != 3 else (0.3 if j != 1 else 0.68)
        if side in ('left', 'right'):
            x = -depth * inner if side == 'left' else W + depth * inner
            places[i] = (x, ay + t)
        else:
            y = H + depth * inner if side == 'bottom' else -depth * inner
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
            'large': 1 if h > R else 0, 'sweep': 0 if side > 0 else 1}


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
    # stations in a line (every station within 0.15 column of the line through the first two): each step bows to
    # the right of its travel, and further, so the loop still opens
    inline = False
    if n >= 3:
        (x0, y0), (x1, y1) = st[0]['pos'], st[1]['pos']
        Ld = math.hypot(x1 - x0, y1 - y0)
        inline = all(abs((x1 - x0) * (q['pos'][1] - y0) - (y1 - y0) * (q['pos'][0] - x0)) / Ld < 0.15 for q in st)
    steps = []
    for i, step in enumerate(lp['steps']):
        a, b = st[i]['pos'], st[(i + 1) % n]['pos']
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        out = (mx - cx) * nx + (my - cy) * ny
        side = 1 if (n == 2 or inline) else (1 if out > 0 else -1)
        if n == 2:
            side = 1                       # a two-station loop: each step bulges right of travel, so the two make a ring
        h = min((BULGE_TWO if n == 2 else (BULGE_INLINE if inline else BULGE_MANY)) * L, BULGE_MAX)
        arc = _arc(a, b, side, h)
        steps.append({'index': i + 1, 'id': step['id'], 'from': step['from'], 'to': step['to'],
                      'from_label': step['from_label'], 'to_label': step['to_label'], 'polarity': step['polarity'],
                      'type': step['type'], 'delay': step['delay'], 'evidence': step['evidence'],
                      'closing': step['closing'], 'sketch': step['conceptual'], 'arc': arc})
    return {'loop': lid, 'stations': st, 'steps': steps, 'sketch': sk, 'inline': inline}


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


THEMES = {
    'newsprint': {'ground': P['newsprint'], 'ink': P['charcoal'], 'plan': P['stone'], 'soft': P['deep_stone']},
    'charcoal': {'ground': P['charcoal'], 'ink': P['newsprint'], 'plan': P['stone'], 'soft': P['newsprint']},
}

# Mark sizes in px. They hold their size as a thumbnail shrinks; the size ladder removes marks in order.
MARKS = {'weight': 2.5, 'station': 3.6, 'start': 5.2, 'tag_body': 9.0, 'tag_point': 4.5, 'tag_h': 10.0,
         'sign_arm': 2.8, 'sign_w': 1.7, 'bar': 5.0, 'plan_w': 0.6, 'plan_visited': 1.3, 'chev': 3.6}
TIERS = {
    'full': 'route, V7 line code, pointing tags (sign and direction), closing bar, start ring, stations, plan',
    'compact': 'route, V7 line code, a chevron for direction, closing bar, start ring, stations, plan; signs move to the caption',
    'locator': 'route as a plain line, stations, plan; the caption carries everything else',
}
SIZE = {'full': None, 'compact': None}       # minimum widths, set by measure() from the geometry


def size_tier(width_px):
    if SIZE['full'] and width_px >= SIZE['full']:
        return 'full'
    if SIZE['compact'] and width_px >= SIZE['compact']:
        return 'compact'
    return 'locator' if SIZE['compact'] else 'full'


def lines_in_words(lid, rt):
    lp = LOOPS[lid]
    parts = [f'{lid}, {lp["kind_word"].lower()} loop ({lp["kind_gloss"]}), {lp["n"]} steps: {lp["title"]}.']
    first = rt['stations'][0]
    parts.append(f'Starts at {first["code"] + " " if first["code"] else ""}{first["label"]}.')
    for s in rt['steps']:
        word = acc.SIGN_WORDS.get(s['polarity'], 'decides')
        sign = 'plus' if s['polarity'] == '+' else 'minus'
        if s['sketch']:
            grade = 'a sketched step with no numbered connection, hollow line'
            sid = ''
        else:
            g = acc.GRADES[s['evidence']]
            grade = f'{g[0].lower()} ({g[1]}), {g[2]} line'
            sid = s['id'] + ': '
        close = ' This step closes the loop.' if s['closing'] else ''
        parts.append(f'Step {s["index"]}, {sid}{s["from_label"]} {word} {s["to_label"]} ({sign}), {grade}.{close}')
    return ' '.join(parts)


def step_geometry(rt, pl, width_px):
    """Per step, in px at this width: the sampled arc, its visible stretch between the stations' marks, and the
    room left for the line code on each side of a tag. Used by the drawing and by the size ladder."""
    fr = frame(pl)
    k = width_px / fr['w']

    def X(p):
        return ((p[0] - fr['x0']) * k, (p[1] - fr['y0']) * k)
    n = len(rt['stations'])
    st_px = [X(s['pos']) for s in rt['stations']]
    rad = [MARKS['start'] if i == 0 else MARKS['station'] for i in range(n)]
    out = []
    for s in rt['steps']:
        i = s['index'] - 1
        a_i, b_i = i, (i + 1) % n
        pts = [X(p) for p in arc_points(s['arc'])]
        cum = _along(pts)
        s0 = rad[a_i] + 1.0
        s1 = cum[-1]
        for j in range(len(pts) - 1, -1, -1):
            if math.dist(pts[j], st_px[b_i]) >= rad[b_i] + 1.0:
                s1 = cum[j]
                break
        out.append({'pts': pts, 'cum': cum, 's0': s0, 's1': s1, 'visible': s1 - s0, 'k': k})
    return out, st_px, rad, k


def period(grade, weight):
    d = dash(grade, weight) if grade in DASH else None
    return sum(float(x) for x in d.split()) if d else 0.0


def thumb_svg(lid, rt, pl, width_px, theme='newsprint', uid='', tier=None, route_only=False, plan_only=False,
              view='loop-route', label=True):
    th = THEMES[theme]
    fr = frame(pl)
    k = width_px / fr['w']
    Hpx = fr['h'] * k
    tier = tier or size_tier(width_px)
    mk = MARKS

    def X(p):
        return ((p[0] - fr['x0']) * k, (p[1] - fr['y0']) * k)
    lp = LOOPS[lid]
    steps_attr = 'sketch' if lp['conceptual'] else ' '.join(s['id'] for s in lp['steps'])
    aria = (f' role="img" aria-labelledby="{uid}t {uid}d"' if label else ' aria-hidden="true"')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" class="thumb" data-view="{view}" data-loop="{lid}" '
           f'data-steps="{steps_attr}" data-tier="{tier}" width="{_f(width_px)}" height="{_f(Hpx)}" '
           f'viewBox="0 0 {_f(width_px)} {_f(Hpx)}"{aria}>']
    if label:
        out.append(f'<title id="{uid}t">{esc(lid)}: {esc(lp["title"])}</title><desc id="{uid}d">{esc(lines_in_words(lid, rt))}</desc>')
    if not route_only:
        visited = {s['area'] for s in rt['stations'] if s['on_plan']}
        out.append(f'<g class="plan" fill="none" stroke="{th["plan"]}" stroke-width="{mk["plan_w"]}" aria-hidden="true">')
        for a, (x0, y0, x1, y1) in pl['boxes'].items():
            p0, p1 = X((x0, y0)), X((x1, y1))
            wv = f' stroke-width="{mk["plan_visited"]}" class="visited"' if a in visited else ''
            out.append(f'<rect data-area="{a}"{wv} x="{_f(p0[0])}" y="{_f(p0[1])}" width="{_f(p1[0] - p0[0])}" '
                       f'height="{_f(p1[1] - p0[1])}" rx="{_f(min(0.14 * k, 6))}"/>')
        out.append('</g>')
    if plan_only:
        out.append('</svg>')
        return ''.join(out)
    w = mk['weight']
    ink, ground = th['ink'], th['ground']
    geo, st_px, rad, _ = step_geometry(rt, pl, width_px)
    n = len(st_px)
    out.append('<g class="route">')
    for s, gm in zip(rt['steps'], geo):
        i = s['index'] - 1
        b_i = (i + 1) % n
        pts, cum, s0, s1 = gm['pts'], gm['cum'], gm['s0'], gm['s1']
        line_end = s1 - (mk['tag_body'] * 0.5 if tier == 'full' else (mk['chev'] if tier == 'compact' else 0))
        p0, _ = _at(pts, cum, s0)
        p1, _ = _at(pts, cum, line_end)
        R = s['arc']['radius'] * k
        d = f'M{_f(p0[0])} {_f(p0[1])}A{_f(R)} {_f(R)} 0 0 {s["arc"]["sweep"]} {_f(p1[0])} {_f(p1[1])}'
        if s['sketch']:
            attrs = f'data-step="{s["index"]}" data-sign="{s["polarity"]}" data-grade="sketch"'
        else:
            sign = s['polarity'] if s['polarity'] in ('+', '-') else 'none'
            attrs = (f'data-link="{s["id"]}" data-sign="{sign}" data-grade="{s["evidence"]}" data-delay="{s["delay"]}" '
                     f'data-from="{s["from"]}" data-to="{s["to"]}" data-step="{s["index"]}"')
        if s['closing']:
            attrs += ' data-closing="true"'
        g = [f'<g class="step" {attrs}>']
        if s['sketch']:
            g.append(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{_f(w + 1.6)}"/>'
                     f'<path d="{d}" fill="none" stroke="{ground}" stroke-width="{_f(w - 0.9)}"/>')
        else:
            da = dash(s['evidence'], w) if tier != 'locator' else None
            g.append(f'<path class="line" d="{d}" fill="none" stroke="{ink}" stroke-width="{_f(w)}"'
                     + (f' stroke-dasharray="{da}"' if da else '') + '/>')
        tb, tp = mk['tag_body'], mk['tag_point']
        L = tb + tp
        if tier == 'full':
            # the pointing tag: a solid home-plate shape at the arrival end, pointing the way the step runs, the sign
            # upright inside it. It is the step's arrowhead, so the line code runs clear from the departure to the tag.
            tip_s = s1
            back_s = tip_s - L
            bp, bt = _at(pts, cum, back_s)
            tpnt, _ = _at(pts, cum, tip_s)
            ux, uy = tpnt[0] - bp[0], tpnt[1] - bp[1]
            ul = math.hypot(ux, uy) or 1
            ux, uy = ux / ul, uy / ul
            vx, vy = -uy, ux
            th2 = mk['tag_h'] / 2
            pts_t = [(0, -th2), (tb, -th2), (L, 0), (tb, th2), (0, th2)]
            poly = ' '.join(f'{_f(bp[0] + ux * a + vx * b)},{_f(bp[1] + uy * a + vy * b)}' for a, b in pts_t)
            gx, gy = bp[0] + ux * tb / 2, bp[1] + uy * tb / 2
            arm = mk['sign_arm']
            glyph = f'M{_f(gx - arm)} {_f(gy)}H{_f(gx + arm)}'
            if s['polarity'] == '+':
                glyph += f'M{_f(gx)} {_f(gy - arm)}V{_f(gy + arm)}'
            g.append(f'<g class="tag"><polygon points="{poly}" fill="{ink}" stroke="{ground}" stroke-width="1.2" stroke-linejoin="round"/>'
                     f'<path d="{glyph}" stroke="{ground}" stroke-width="{mk["sign_w"]}" fill="none"/></g>')
            bar_s = back_s - 3.0
        elif tier == 'compact':
            c = mk['chev']
            tip, mt = _at(pts, cum, s1)
            ux, uy = mt
            vx, vy = -uy, ux
            g.append(f'<path class="chev" d="M{_f(tip[0] - ux * c * 1.5 - vx * c)} {_f(tip[1] - uy * c * 1.5 - vy * c)}L{_f(tip[0])} {_f(tip[1])}'
                     f'L{_f(tip[0] - ux * c * 1.5 + vx * c)} {_f(tip[1] - uy * c * 1.5 + vy * c)}Z" fill="{ink}"/>')
            bar_s = s1 - c * 1.5 - 3.0
        if s['closing'] and tier != 'locator':
            bp, bt = _at(pts, cum, bar_s)
            bx, by = -bt[1], bt[0]
            L2 = mk['bar']
            g.append(f'<path class="close-bar" d="M{_f(bp[0] + bx * L2)} {_f(bp[1] + by * L2)}L{_f(bp[0] - bx * L2)} {_f(bp[1] - by * L2)}" '
                     f'stroke="{ink}" stroke-width="2.2"/>')
        g.append('</g>')
        out.append(''.join(g))
    out.append('<g class="stations">')
    for i, s in enumerate(rt['stations']):
        x, y = st_px[i]
        node = f' data-node="{s["code"]}"' if s['code'] else ' data-offplan="true"'
        r = rad[i]
        if not s['on_plan']:
            if i == 0 and tier != 'locator':
                out.append(f'<g{node} class="start"><circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}" fill="{ground}" stroke="{ink}" stroke-width="1.5"/>'
                           f'<circle cx="{_f(x)}" cy="{_f(y)}" r="2.1" fill="none" stroke="{ink}" stroke-width="1.2"/></g>')
            else:
                out.append(f'<circle{node} cx="{_f(x)}" cy="{_f(y)}" r="{_f(mk["station"] + 0.3)}" fill="{ground}" stroke="{ink}" stroke-width="1.5"/>')
        elif i == 0 and tier != 'locator':
            out.append(f'<g{node} class="start"><circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}" fill="{ground}" stroke="{ink}" stroke-width="2"/>'
                       f'<circle cx="{_f(x)}" cy="{_f(y)}" r="2" fill="{ink}"/></g>')
        else:
            out.append(f'<circle{node} cx="{_f(x)}" cy="{_f(y)}" r="{_f(mk["station"])}" fill="{ink}" stroke="{ground}" stroke-width="1.4"/>')
    out.append('</g></g></svg>')
    return ''.join(out)


# ---------------------------------------------------------------------------------------------------------------
# 3. Measures: the size ladder and distinctness (D1-16)
# ---------------------------------------------------------------------------------------------------------------
NODE_RENDER = r"""
const { chromium } = require('playwright');
let buf = '';
process.stdin.on('data', (d) => { buf += d; });
process.stdin.on('end', async () => {
  const job = JSON.parse(buf);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  const out = {};
  for (const group of job.groups) {
    const body = group.items.map((it) => `<div id="${it.id}" style="display:block;line-height:0;margin:0 0 4px 0;width:max-content">${it.svg}</div>`).join('');
    await page.setContent(`<!doctype html><html><body style="margin:0;background:${group.bg}">${body}</body></html>`);
    for (const it of group.items) {
      const png = await page.locator('#' + it.id + ' > svg').screenshot({ type: 'png', animations: 'disabled' });
      out[it.id] = png.toString('base64');
    }
  }
  await browser.close();
  process.stdout.write(JSON.stringify(out));
});
"""


def render_pngs(groups):
    """groups: [{'bg': css color, 'items': [{'id':..., 'svg':...}]}]. Returns {id: numpy luminance array 0..1}."""
    job = json.dumps({'groups': groups})
    res = subprocess.run(['node', '-e', NODE_RENDER], input=job, capture_output=True, text=True, timeout=600)
    if res.returncode:
        raise RuntimeError(res.stderr[-2000:])
    out = {}
    for k, b64 in json.loads(res.stdout).items():
        im = Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB')
        a = np.asarray(im, dtype=np.float64) / 255.0
        lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
        out[k] = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
    return out


def _hex_lum(h):
    rgb = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ink_map(lum, theme='newsprint'):
    g, i = _hex_lum(THEMES[theme]['ground']), _hex_lum(THEMES[theme]['ink'])
    return np.clip((lum - g) / (i - g), 0, 1)


def box3(a):
    """The D1-16 blur: each pixel becomes the mean of its 3 by 3 neighborhood (edges use what exists)."""
    p = np.pad(a, 1, mode='constant')
    c = np.pad(np.ones_like(a), 1, mode='constant')
    s = sum(p[1 + dy:1 + dy + a.shape[0], 1 + dx:1 + dx + a.shape[1]] for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    n = sum(c[1 + dy:1 + dy + a.shape[0], 1 + dx:1 + dx + a.shape[1]] for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    return s / n


def corr(a, b):
    a, b = a.ravel() - a.mean(), b.ravel() - b.mean()
    d = math.sqrt(float((a * a).sum() * (b * b).sum()))
    return float((a * b).sum() / d) if d else 0.0


def filled(mask):
    """Fill holes: everything the border cannot reach through background is inside the shape."""
    h, w = mask.shape
    outside = np.zeros_like(mask, dtype=bool)
    stack = [(y, x) for y in range(h) for x in (0, w - 1)] + [(y, x) for x in range(w) for y in (0, h - 1)]
    while stack:
        y, x = stack.pop()
        if y < 0 or x < 0 or y >= h or x >= w or outside[y, x] or mask[y, x]:
            continue
        outside[y, x] = True
        stack.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    return ~outside


def iou(a, b):
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 0.0


def squint(a, r):
    """A heavier blur for the stricter test: a box of side 2r+1, run twice (close to a Gaussian)."""
    for _ in range(2):
        p = np.pad(a, r, mode='edge')
        cs = np.cumsum(np.cumsum(p, 0), 1)
        cs = np.pad(cs, ((1, 0), (1, 0)))
        n = 2 * r + 1
        a = (cs[n:, n:] - cs[:-n, n:] - cs[n:, :-n] + cs[:-n, :-n]) / (n * n)
    return a


def size_floors(pl, routes, weight=None):
    """The narrowest thumbnail at which each tier still reads, from the geometry (see TIERS). Per step, the visible
    stretch runs from the departure station's rim to the arrival station's rim.
    full     the tag (13.5 px), and before it one whole period of the step's line code (solid and sketched steps:
             8 px of line), plus the closing bar's room on the closing step; and 3 px clear between station rims;
    compact  the same with a 5 px chevron in place of the tag;
    locator  the stations alone: 2 px clear between any two station discs."""
    w_ = weight or MARKS['weight']
    tag = MARKS['tag_body'] + MARKS['tag_point']
    chev = MARKS['chev'] * 1.5
    bar = 3.0 + 2.2
    per_loop = {}
    for lid, rt in routes.items():
        need = {'full': None, 'compact': None}
        binding = {}
        for width in range(60, 601, 2):
            geo, st_px, rad, _ = step_geometry(rt, pl, width)
            clear = all(math.dist(st_px[i], st_px[j]) >= rad[i] + rad[j] + 3
                        for i in range(len(st_px)) for j in range(i + 1, len(st_px)))
            for tier, mark in (('full', tag), ('compact', chev)):
                if need[tier] is not None:
                    continue
                ok = clear
                worst = None
                for s, g in zip(rt['steps'], geo):
                    per = period(s['evidence'], w_) if not s['sketch'] else 0.0
                    req = mark + 2.0 + max(per, 8.0) + (bar if s['closing'] else 0.0)
                    if g['visible'] < req:
                        ok = False
                        worst = s['id'] or f'step {s["index"]}'
                if ok:
                    need[tier] = width
                else:
                    binding[tier] = worst or 'stations too close'
            if all(need.values()):
                break
        loc = None
        for width in range(40, 601, 2):
            _, st_px, _, _ = step_geometry(rt, pl, width)
            if all(math.dist(st_px[i], st_px[j]) >= 2 * MARKS['station'] + 2
                   for i in range(len(st_px)) for j in range(i + 1, len(st_px))):
                loc = width
                break
        per_loop[lid] = {'full': need['full'], 'compact': need['compact'], 'locator': loc,
                         'binding_full': binding.get('full'), 'binding_compact': binding.get('compact')}
    return per_loop


def measure(pl, routes, widths):
    """Render every thumbnail at each width, as drawn and route only, and score all 253 pairs.
    D1-16 score = mean of (a) the overlap of the filled route silhouettes (intersection over union) and (b) the
    correlation of the as-drawn images after the 3 by 3 box blur. Limit: under 0.60. The squint test correlates the
    as-drawn images after a blur of about one fortieth of the width, run twice; it is stricter and has no limit of
    its own in the decision log, so it is reported, not used to pass or fail."""
    order = M['loop_order']
    groups = []
    for w in widths:
        items = []
        for lid in order:
            rt = routes[lid]
            items.append({'id': f'a-{lid}-{w}', 'svg': thumb_svg(lid, rt, pl, w, label=False)})
            items.append({'id': f'r-{lid}-{w}', 'svg': thumb_svg(lid, rt, pl, w, route_only=True, label=False)})
        groups.append({'bg': THEMES['newsprint']['ground'], 'items': [{**it, 'id': it['id'].replace('.', '_')} for it in items]})
    img = render_pngs(groups)
    results = {}
    for w in widths:
        drawn = {lid: ink_map(img[f'a-{lid}-{w}']) for lid in order}
        route_ink = {lid: ink_map(img[f'r-{lid}-{w}']) for lid in order}
        sil = {lid: filled(route_ink[lid] > 0.5) for lid in order}
        blur = {lid: box3(drawn[lid]) for lid in order}
        r = max(2, round(w / 40))
        sq = {lid: squint(drawn[lid], r) for lid in order}
        pairs = []
        for a, b in itertools.combinations(order, 2):
            sh = min(blur[a].shape[0], blur[b].shape[0]), min(blur[a].shape[1], blur[b].shape[1])
            c = corr(blur[a][:sh[0], :sh[1]], blur[b][:sh[0], :sh[1]])
            u = iou(sil[a][:sh[0], :sh[1]], sil[b][:sh[0], :sh[1]])
            q = corr(sq[a][:sh[0], :sh[1]], sq[b][:sh[0], :sh[1]])
            pairs.append({'a': a, 'b': b, 'silhouette_iou': round(u, 3), 'blurred_corr': round(c, 3),
                          'score': round((u + c) / 2, 3), 'squint_corr': round(q, 3)})
        pairs.sort(key=lambda p: -p['score'])
        results[str(w)] = {'width': w, 'tier': size_tier(w), 'height': int(drawn[order[0]].shape[0]), 'squint_radius_px': r, 'pairs': pairs,
                           'over_limit': [p for p in pairs if p['score'] >= 0.60],
                           'max_score': pairs[0]['score'], 'median_score': float(np.median([p['score'] for p in pairs])),
                           'max_squint': max(p['squint_corr'] for p in pairs)}
    return results



# ---------------------------------------------------------------------------------------------------------------
# 4. The data contract per level, and the overview options (memo Parts 2 and 3)
# ---------------------------------------------------------------------------------------------------------------
def _cross(p1, p2, p3, p4):
    def o(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)
    if {tuple(p1), tuple(p2)} & {tuple(p3), tuple(p4)}:
        return False
    return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0


def _crossings(segs):
    return sum(1 for (a, b), (c, d) in itertools.combinations(segs, 2) if _cross(a, b, c, d))


def _through(segs, points, ends, tol=0.18):
    """Segments that pass within tol columns of a station that is not one of their ends."""
    hits = 0
    for (a, b), e in zip(segs, ends):
        for v, q in points.items():
            if v in e:
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy
            t = max(0, min(1, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / L2))
            if math.dist(q, (a[0] + t * dx, a[1] + t * dy)) < tol:
                hits += 1
                break
    return hits


def contract(pl):
    pos = pl['pos']
    links = list(LINKS.values())
    area_of = AREA_OF
    numbered = [k for k, v in LOOPS.items() if not v['conceptual']]
    loop_links = {s['id'] for k in numbered for s in LOOPS[k]['steps']}
    loop_vars = {s['code'] for k in numbered for s in LOOPS[k]['stations']} | {s['code'] for k in LOOPS for s in LOOPS[k]['stations'] if s['code']}
    cross = [l for l in links if area_of[l['from']] != area_of[l['to']]]
    pairs = collections.Counter(tuple(sorted((area_of[l['from']], area_of[l['to']]))) for l in cross)
    directed = collections.Counter((area_of[l['from']], area_of[l['to']]) for l in cross)
    core = set('ABCDE')
    core_cross = [l for l in cross if area_of[l['from']] in core and area_of[l['to']] in core]
    ring_neighbors = {frozenset(p) for p in (('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A'), ('B', 'D'), ('B', 'E'))}
    row_order = 'ABCDE'
    jumps_row = sum(1 for l in core_cross if abs(row_order.index(area_of[l['from']]) - row_order.index(area_of[l['to']])) > 1)
    jumps_ring = sum(1 for l in core_cross if frozenset((area_of[l['from']], area_of[l['to']])) not in ring_neighbors)
    by_layer = collections.Counter(l['layer'] for l in links)
    cross_layer = [l for l in links if NODES[l['from']]['layer'] != NODES[l['to']]['layer']]
    x_links = [l for l in links if area_of[l['from']] == 'X' or area_of[l['to']] == 'X']
    econ = {a['id'] for a in M['areas'] if a['layer'] == 'economy'}
    econ_links = [l for l in links if area_of[l['from']] in econ or area_of[l['to']] in econ]
    tc_links = [l for l in links if area_of[l['from']] == 'TC' or area_of[l['to']] == 'TC']
    auth = [l for l in links if l['type'] == 'authority']
    hyp = [l for l in links if l['evidence'] == 'hypothesis']
    contested = [l for l in links if l['evidence'] == 'plausible_contested']
    routes = [(rid, x) for rid, r in M['reforms'].items() for x in r['routes']]
    back = [(rid, lp) for rid, r in M['reforms'].items() for lp in r['loops'] if rid not in LOOPS[lp]['reforms']]
    codes = set(M['effect_codes'])
    effects = [(rid, f, v) for rid, r in M['reforms'].items() for f, v in r['effects'].items()]
    parity = {k: {'minus_steps': sum(1 for s in LOOPS[k]['steps'] if s['polarity'] == '-'), 'type': LOOPS[k]['type'],
                  'agrees': (sum(1 for s in LOOPS[k]['steps'] if s['polarity'] == '-') % 2 == 0) == (LOOPS[k]['type'] == 'R')}
              for k in numbered}

    def seg(l):
        return (pos[l['from']], pos[l['to']])
    area_center = {a: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for a, b in pl['boxes'].items()}
    bundle_segs = [(area_center[a], area_center[b]) for a, b in pairs]
    core_vars = [v for v in NODES if area_of[v] in core]
    options = {
        'all_connections': {'marks': len(links), 'crossings': _crossings([seg(l) for l in links]),
                            'through_station': _through([seg(l) for l in links], pos, [(l['from'], l['to']) for l in links]),
                            'stations': len(NODES)},
        'loop_connections_only': {'marks': len(loop_links), 'crossings': _crossings([seg(LINKS[k]) for k in loop_links]),
                                  'through_station': _through([seg(LINKS[k]) for k in loop_links], {v: pos[v] for v in loop_vars if v in pos},
                                                              [(LINKS[k]['from'], LINKS[k]['to']) for k in loop_links]),
                                  'stations': len([v for v in loop_vars if v]), 'connections_left_out': len(links) - len(loop_links)},
        'core_only': {'marks': sum(1 for l in links if area_of[l['from']] in core and area_of[l['to']] in core),
                      'crossings': _crossings([seg(l) for l in links if area_of[l['from']] in core and area_of[l['to']] in core]),
                      'stations': len(core_vars)},
        'core_bundles': {'marks': sum(1 for a, b in pairs if a in core and b in core),
                         'crossings': _crossings([(area_center[a], area_center[b]) for a, b in pairs if a in core and b in core])},
        'area_bundles': {'marks': len(pairs), 'crossings': _crossings(bundle_segs),
                         'areas_with_inside_connections': len({area_of[l['from']] for l in links if area_of[l['from']] == area_of[l['to']]}),
                         'largest_bundle': max(pairs.values()), 'single_connection_bundles': sum(1 for v in pairs.values() if v == 1)},
    }
    c_vars = AREAS['C']['nodes']
    c_links = [l for l in links if area_of[l['from']] == 'C' or area_of[l['to']] == 'C']
    c_inside = [l for l in c_links if area_of[l['from']] == area_of[l['to']] == 'C']
    c_partner = collections.Counter(area_of[l['to']] if area_of[l['from']] == 'C' else area_of[l['from']] for l in c_links if l not in c_inside)
    c_loops_touch = sorted({lp for v in c_vars for lp in NODES[v]['loops']}, key=M['loop_order'].index)
    c_reforms = sorted({rid for rid, r in M['reforms'].items() if any(t in c_vars or (t in LINKS and (LINKS[t]['from'] in c_vars or LINKS[t]['to'] in c_vars)) for t in r['targets'])})
    r10 = LOOPS['R10']
    r10_shared = {s['id']: [lp for lp in LINKS[s['id']]['loops'] if lp != 'R10'] for s in r10['steps']}
    r10_var_loops = {s['code']: [lp for lp in NODES[s['code']]['loops'] if lp != 'R10'] for s in r10['stations']}
    rf = M['reforms']['R-01']
    out = {
        'system': {
            'variables': len(NODES), 'connections': len(links), 'loops': len(LOOPS), 'loops_numbered': len(numbered),
            'loops_reinforcing': sum(1 for v in LOOPS.values() if v['type'] == 'R'),
            'loops_balancing': sum(1 for v in LOOPS.values() if v['type'] == 'B'),
            'loops_sketched': sorted(k for k, v in LOOPS.items() if v['conceptual']),
            'loops_hypothesized_closing': sorted(k for k, v in LOOPS.items() if v['hypothesized']),
            'loop_lengths': dict(collections.Counter(v['n'] for v in LOOPS.values())),
            'reforms': len(M['reforms']), 'areas': len(M['areas']),
            'variables_by_area': {a: len(v['nodes']) for a, v in AREAS.items()},
            'variables_by_type': dict(collections.Counter(n['type'] for n in NODES.values())),
            'connections_by_type': dict(collections.Counter(l['type'] for l in links)),
            'connections_by_grade': dict(collections.Counter(l['evidence'] for l in links)),
            'connections_by_delay': dict(collections.Counter(l['delay'] for l in links)),
            'connections_by_sign': dict(collections.Counter(l['polarity'] or 'none' for l in links)),
            'connections_by_layer': dict(by_layer), 'connections_cross_layer': len(cross_layer),
            'connections_cross_area': len(cross), 'connections_within_area': len(links) - len(cross),
            'within_area_by_area': dict(collections.Counter(area_of[l['from']] for l in links if l not in cross)),
            'area_pairs': [{'pair': list(k), 'connections': v} for k, v in pairs.most_common()],
            'area_pairs_directed_top': [{'from': a, 'to': b, 'connections': v} for (a, b), v in directed.most_common(12)],
            'core_cross_area': len(core_cross), 'core_cross_area_jumping_an_area_in_one_row': jumps_row,
            'core_cross_area_jumping_an_area_in_the_ring': jumps_ring,
            'connections_on_numbered_loops': len(loop_links), 'connections_on_no_loop': len(links) - len(loop_links),
            'variables_on_loops': len([v for v in loop_vars if v]), 'variables_on_no_loop': len(NODES) - len([v for v in loop_vars if v]),
            'variables_on_no_loop_by_area': dict(collections.Counter(area_of[v] for v in NODES if v not in loop_vars)),
            'outside_driver_links': len(x_links),
            'outside_driver_links_by_target_area': dict(collections.Counter(area_of[l['to']] for l in x_links)),
            'outside_driver_links_by_driver': dict(collections.Counter(l['from'] for l in x_links)),
            'economy_links': len(econ_links), 'economy_links_by_partner': dict(collections.Counter(
                (area_of[l['to']] if area_of[l['from']] in econ else area_of[l['from']]) for l in econ_links)),
            'technology_links': len(tc_links), 'technology_links_by_partner': dict(collections.Counter(
                (area_of[l['to']] if area_of[l['from']] == 'TC' else area_of[l['from']]) for l in tc_links)),
            'authority_links': [{'id': l['id'], 'from': l['from'], 'to': l['to'], 'name': l['name']} for l in auth],
            'authority_links_on_loops': [l['id'] for l in auth if l['loops']],
            'hypothesis_links': [{'id': l['id'], 'loops': l['loops']} for l in hyp],
            'contested_links': [{'id': l['id'], 'loops': l['loops']} for l in contested],
            'loop_sign_parity': parity, 'loop_sign_parity_all_agree': all(v['agrees'] for v in parity.values()),
            'route_entries': len(routes), 'route_entries_dated': sum(1 for _, x in routes if x['checked']),
            'reforms_with_an_undated_route': sum(1 for r in M['reforms'].values() if any(not x['checked'] for x in r['routes'])),
            'effect_values': len(effects), 'effect_values_with_qualifiers': sum(1 for e in effects if e[2] not in codes),
            'reform_loop_entries_not_listed_back': [{'reform': a, 'loop': b} for a, b in back],
        },
        'area_C': {
            'variables': c_vars, 'labels': {v: NODES[v]['label'] for v in c_vars},
            'connections_touching': len(c_links), 'inside': len(c_inside), 'crossing_out': len(c_links) - len(c_inside),
            'partners': dict(c_partner.most_common()),
            'into_C': sum(1 for l in c_links if area_of[l['to']] == 'C' and area_of[l['from']] != 'C'),
            'out_of_C': sum(1 for l in c_links if area_of[l['from']] == 'C' and area_of[l['to']] != 'C'),
            'loops_grouped_under_C': next(g['loops'] for g in M['groups'] if g['id'] == 'C'),
            'loops_with_a_station_in_C': c_loops_touch,
            'connections_touching_on_no_loop': sum(1 for l in c_links if not l['loops']),
            'grades': dict(collections.Counter(l['evidence'] for l in c_links)),
            'authority_touching': [l['id'] for l in c_links if l['type'] == 'authority'],
            'reforms_targeting_C': c_reforms,
            'outside_drivers_into_C': [l['id'] for l in x_links if area_of[l['to']] == 'C'],
        },
        'loop_R10': {
            'steps': [{k: s[k] for k in ('id', 'from', 'to', 'polarity', 'evidence', 'delay', 'closing')} for s in r10['steps']],
            'weakest': r10['weakest'], 'reforms': r10['reforms'], 'targets': r10['targets'],
            'links_shared_with_other_loops': r10_shared, 'stations_on_other_loops': r10_var_loops,
            'closure': r10['closure'], 'delay_word': r10['delay_word'], 'direction_word': r10['direction_word'],
            'reference_mode': r10['reference_mode'],
        },
        'reform_R01': {
            'title': rf['title'], 'targets': rf['targets'], 'loops': rf['loops'], 'band': rf['band'],
            'effects': rf['effects'], 'effects_confidence': rf.get('effects_confidence'),
            'problem_grade': rf['problem_grade'], 'remedy_grade': rf['remedy_grade'],
            'routes': rf['routes'], 'routes_undated': [x['route'] for x in rf['routes'] if not x['checked']],
            'loops_listing_it_back': {lp: 'R-01' in LOOPS[lp]['reforms'] for lp in rf['loops']},
        },
        'overview_options': options,
    }
    return out
