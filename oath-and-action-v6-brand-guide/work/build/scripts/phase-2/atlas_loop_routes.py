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
        hh = min(min(img[f'a-{lid}-{w}'].shape[0], img[f'r-{lid}-{w}'].shape[0]) for lid in order)
        ww = min(min(img[f'a-{lid}-{w}'].shape[1], img[f'r-{lid}-{w}'].shape[1]) for lid in order)
        drawn = {lid: ink_map(img[f'a-{lid}-{w}'][:hh, :ww]) for lid in order}
        route_ink = {lid: ink_map(img[f'r-{lid}-{w}'][:hh, :ww]) for lid in order}
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


# ---------------------------------------------------------------------------------------------------------------
# 5. The study page
# ---------------------------------------------------------------------------------------------------------------
CARD_W = 318                      # four columns at 1440 px: 48 px margins, 24 px gutters
GRADE_ORDER = ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis']


def _tw(text, size=13, weight=600):
    """Rough advance width of Inter, for placing SVG labels; the browser check measures the real boxes."""
    narrow = sum(1 for ch in text if ch in "il.,:;'|()!fjtI1 ")
    wide = sum(1 for ch in text if ch in 'MWmw')
    caps = sum(1 for ch in text if ch.isupper() and ch not in 'IMW')
    per = 0.56 if weight < 600 else 0.59
    return size * (per * (len(text) - narrow - wide - caps) + 0.3 * narrow + 0.88 * wide + 0.7 * caps)


def _wrap(text, width, size=13, weight=600):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if _tw(t, size, weight) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def key_plan_svg(pl, width=800):
    """The plan at reading size: every area named, every variable at its slot with its ID."""
    fr = frame(pl)
    pad_t, pad_b = 30, 54
    k = width / fr['w']
    H = fr['h'] * k + pad_t + pad_b
    ink, stone, deep = P['charcoal'], P['stone'], P['deep_stone']

    def X(p):
        return ((p[0] - fr['x0']) * k, (p[1] - fr['y0']) * k + pad_t)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" data-view="plan-key" width="{width}" height="{_f(H)}" viewBox="0 0 {width} {_f(H)}" '
         f'role="img" aria-labelledby="plan-t plan-d"><title id="plan-t">The canonical plan</title>'
         f'<desc id="plan-d">Outside drivers X1 to X5 across the top. The civic core as a ring: A Economic structure, B Political '
         f'inputs and C Electoral competition across the top row; E Legitimacy under A and D Governing institutions under B and C. '
         f'Along the bottom, the economy layer ({", ".join(AREAS[a]["title"] for a in pl["ground_order"] if a != "TC")}) and the technology layer. '
         f'A margin on the left holds the three sketched loops, which are not on the map.</desc>']
    core = set('ABCDE')
    for a, (x0, y0, x1, y1) in pl['boxes'].items():
        p0, p1 = X((x0, y0)), X((x1, y1))
        strong = a in core
        o.append(f'<rect data-area="{a}" x="{_f(p0[0])}" y="{_f(p0[1])}" width="{_f(p1[0] - p0[0])}" height="{_f(p1[1] - p0[1])}" '
                 f'rx="8" fill="none" stroke="{ink if strong else stone}" stroke-width="{1.2 if strong else 1}"/>')
        title = AREAS[a]['title']
        if a in core:
            o.append(f'<text x="{_f(p0[0] + 12)}" y="{_f(p0[1] + 22)}" class="pk-area"><tspan class="pk-letter">{a}</tspan> {esc(title)}</text>')
        elif a == 'X':
            o.append(f'<text x="{_f(p0[0])}" y="{_f(p0[1] - 10)}" class="pk-area"><tspan class="pk-letter">X</tspan> {esc(title)}</text>')
        else:
            lines = _wrap(title, p1[0] - p0[0] + 18)
            for i, ln in enumerate(lines):
                o.append(f'<text x="{_f(p0[0])}" y="{_f(p1[1] + 18 + 16 * i)}" class="pk-small">{esc(ln)}</text>')
    for v, (x, y) in pl['pos'].items():
        px, py = X((x, y))
        big = AREA_OF[v] in core
        r = 4.5 if big else 3.2
        ground = AREA_OF[v] not in core and AREA_OF[v] != 'X'
        lab = (f'<text x="{_f(px)}" y="{_f(py + 17)}" text-anchor="middle" class="pk-id-s">{v}</text>' if ground else
               f'<text x="{_f(px + r + 4)}" y="{_f(py + 4.6)}" class="{"pk-id" if big else "pk-id-s"}">{v}</text>')
        o.append(f'<g data-node="{v}"><circle cx="{_f(px)}" cy="{_f(py - (6 if ground else 0))}" r="{r}" fill="{ink if big else stone}"/>{lab}</g>')
    # the margin
    mx = 8
    my = X((0, pl['boxes']['A'][1]))[1] + 6
    o.append(f'<text x="{mx}" y="{_f(my + 14)}" class="pk-small">Off the map</text>'
             f'<text x="{mx}" y="{_f(my + 30)}" class="pk-small">(sketches)</text>')
    o.append('</svg>')
    return ''.join(o)


def _mini(kind, theme='newsprint'):
    """Small specimens for the key, drawn with the thumbnails' own marks."""
    th = THEMES[theme]
    ink, ground = th['ink'], th['ground']
    w = MARKS['weight']
    if kind in DASH:
        da = dash(kind, w)
        return (f'<svg width="76" height="16" viewBox="0 0 76 16" aria-hidden="true"><path d="M2 8H74" stroke="{ink}" stroke-width="{w}"'
                + (f' stroke-dasharray="{da}"' if da else '') + '/></svg>')
    if kind == 'sketch':
        return (f'<svg width="76" height="16" viewBox="0 0 76 16" aria-hidden="true"><path d="M2 8H64" stroke="{ink}" stroke-width="{w + 1.6}"/>'
                f'<path d="M2 8H64" stroke="{ground}" stroke-width="{w - 0.9}"/><circle cx="69" cy="8" r="3.9" fill="{ground}" stroke="{ink}" stroke-width="1.5"/></svg>')
    if kind in ('+', '-'):
        tb, tp, h = MARKS['tag_body'], MARKS['tag_point'], MARKS['tag_h'] / 2
        x0 = 40
        poly = f'{x0},{8 - h} {x0 + tb},{8 - h} {x0 + tb + tp},8 {x0 + tb},{8 + h} {x0},{8 + h}'
        gx = x0 + tb / 2
        a = MARKS['sign_arm']
        gl = f'M{gx - a} 8H{gx + a}' + (f'M{gx} {8 - a}V{8 + a}' if kind == '+' else '')
        return (f'<svg width="76" height="16" viewBox="0 0 76 16" aria-hidden="true"><path d="M2 8H{x0 + 4}" stroke="{ink}" stroke-width="{w}"/>'
                f'<polygon points="{poly}" fill="{ink}"/><path d="{gl}" stroke="{ground}" stroke-width="{MARKS["sign_w"]}"/>'
                f'<circle cx="{x0 + tb + tp + 6}" cy="8" r="{MARKS["station"]}" fill="{ink}"/></svg>')
    if kind == 'start':
        return (f'<svg width="76" height="16" viewBox="0 0 76 16" aria-hidden="true"><path d="M2 8H20" stroke="{ink}" stroke-width="{w}"/>'
                f'<path d="M23.5 3.2V12.8" stroke="{ink}" stroke-width="2.2"/>'
                f'<polygon points="{26.5},{3} {35.5},{3} {40},8 {35.5},{13} {26.5},{13}" fill="{ink}"/><path d="M28.2 8H33.8M31 5.2V10.8" stroke="{ground}" stroke-width="1.7"/>'
                f'<circle cx="47.5" cy="8" r="{MARKS["start"]}" fill="{ground}" stroke="{ink}" stroke-width="2"/><circle cx="47.5" cy="8" r="2" fill="{ink}"/>'
                f'<path d="M53 8H74" stroke="{ink}" stroke-width="{w}"/></svg>')
    if kind == 'area':
        return (f'<svg width="76" height="16" viewBox="0 0 76 16" aria-hidden="true"><rect x="2" y="2" width="32" height="12" rx="3" fill="none" stroke="{th["plan"]}" stroke-width="{MARKS["plan_visited"]}"/>'
                f'<rect x="42" y="2" width="32" height="12" rx="3" fill="none" stroke="{th["plan"]}" stroke-width="{MARKS["plan_w"]}"/></svg>')
    raise ValueError(kind)


WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']


def nw(n, cap=False):
    w = WORDS[n] if 0 <= n < len(WORDS) else str(n)
    return w[0].upper() + w[1:] if cap else w


def _station_words(lid):
    return ', '.join((f'{s["code"]} ' if s['code'] else '') + s['label'] for s in LOOPS[lid]['stations'])


def _weakest(lid):
    lp = LOOPS[lid]
    if not lp['weakest']:
        return None
    ids = lp['weakest']
    grades = {LINKS[i]['evidence'] for i in ids}
    word = ' or '.join(acc.GRADES[g][0].lower() for g in sorted(grades, key=GRADE_ORDER.index))
    names = ids[0] if len(ids) == 1 else ', '.join(ids[:-1]) + ' and ' + ids[-1]
    return f'Weakest step{"s" if len(ids) > 1 else ""}: {names}, {word}'


def disclosure(lid, rt):
    """The plain disclosure for the two loops closed through a hypothesis and the three sketches."""
    lp = LOOPS[lid]
    if lp['hypothesized']:
        close = next(s for s in lp['steps'] if s['closing'])
        others = [s['id'] for s in lp['steps'] if s['evidence'] == 'hypothesis' and not s['closing']]
        t = (f'Closed with a hypothesized step. {close["id"]}, the step that closes it, is graded hypothesis '
             f'(untested), so the loop is complete only if that step holds.')
        if others:
            t += f' {", ".join(others)} is a hypothesis too.'
        return t
    if lp['conceptual']:
        sk = rt['sketch']
        on = [s for s in lp['stations'] if s['is_variable']]
        if on:
            v = on[0]
            return (f'A sketch. No step is a numbered connection. Only {v["code"]} {v["label"]} is a variable in the model, '
                    f'so the route touches the map there and its other {nw(len(lp["stations"]) - len(on))} stations sit off the map beside it.')
        names = ' and '.join(f'{v} {NODES[v]["label"]}' for v in sk['anchors'])
        return (f'A sketch. No step is a numbered connection and no station is a variable in the model, so the route sits '
                f'off the map, beside {names}, which its reforms target.')
    return None


def card(lid, rt, pl, theme, uid):
    lp = LOOPS[lid]
    svg = thumb_svg(lid, rt, pl, CARD_W, theme=theme, uid=uid)
    disc = disclosure(lid, rt)
    weak = _weakest(lid)
    meta = f'{lp["kind_word"]}, {lp["kind_gloss"]}'
    steps_word = f'{lp["n"]} steps'
    parts = [f'<article class="card" aria-labelledby="{uid}-h">',
             f'<div class="card-head"><span class="card-id">{lid}</span><span class="card-kind">{esc(meta)}<br>{steps_word}</span></div>',
             f'<div class="card-fig">{svg}</div>',
             f'<h3 id="{uid}-h" class="card-title">{esc(lp["title"])}</h3>',
             f'<p class="card-stations">{esc(_station_words(lid))}</p>']
    if weak:
        parts.append(f'<p class="card-meta">{esc(weak)}</p>')
    if disc:
        parts.append(f'<p class="card-note"><span class="note-mark" aria-hidden="true"></span>{esc(disc)}</p>')
    parts.append('</article>')
    return ''.join(parts)


def separation(a, b, routes):
    """What tells two loops apart, in words, from the model."""
    la, lb = LOOPS[a], LOOPS[b]
    sa = [s['code'] for s in la['stations'] if s['code']]
    sb = [s['code'] for s in lb['stations'] if s['code']]
    ka = [s['id'] for s in la['steps'] if s['id']]
    kb = [s['id'] for s in lb['steps'] if s['id']]
    shared_s = [v for v in sa if v in sb]
    shared_k = [k for k in ka if k in kb]
    out = []
    if shared_s:
        txt = f'They share {nw(len(shared_s))} station{"s" if len(shared_s) > 1 else ""} ({", ".join(shared_s)})'
        txt += (f' and {nw(len(shared_k))} connection{"s" if len(shared_k) > 1 else ""} ({", ".join(shared_k)})' if shared_k
                else ' and no connection') + '.'
        out.append(txt)
    else:
        out.append('They share no station.')
    only_a = [v for v in sa if v not in sb]
    only_b = [v for v in sb if v not in sa]
    bits = []
    def names(vs):
        t = [f'{v} {NODES[v]["label"]}' for v in vs]
        return t[0] if len(t) == 1 else ', '.join(t[:-1]) + ' and ' + t[-1]
    if only_a:
        bits.append(f'only {a} stops at {names(only_a)}')
    if only_b:
        bits.append(f'only {b} stops at {names(only_b)}')
    if bits:
        out.append(bits[0][0].upper() + bits[0][1:] + ('; ' + bits[1] if len(bits) > 1 else '') + '.')
    ca = next(s for s in la['steps'] if s['closing'])
    cb = next(s for s in lb['steps'] if s['closing'])
    if ca['id'] != cb['id'] and ca['id'] and cb['id']:
        out.append(f'{a} closes through {ca["id"]} ({acc.GRADES[ca["evidence"]][0].lower()}, {acc.GRADES[ca["evidence"]][2]}); '
                   f'{b} closes through {cb["id"]} ({acc.GRADES[cb["evidence"]][0].lower()}, {acc.GRADES[cb["evidence"]][2]}).')
    if la['n'] != lb['n']:
        out.append(f'{a} has {nw(la["n"])} steps and {b} has {nw(lb["n"])}.')
    return ' '.join(out)


def strip_plot(res_by_size, key, label_n=3, width=1000):
    """All 253 pair scores on one axis per size, as a rug of ticks, the D1-16 limit marked."""
    rows = list(res_by_size)
    row_h, top, left, right = 78, 40, 210, 30
    H = top + row_h * len(rows) + 30
    plot_w = width - left - right
    ink, stone = P['charcoal'], P['stone']

    def X(v):
        return left + v * plot_w
    word = 'score' if key == 'd116' else 'correlation'
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" data-view="similarity-{key}" width="{width}" height="{H}" viewBox="0 0 {width} {H}" role="img" '
         f'aria-labelledby="sp-{key}-t sp-{key}-d"><title id="sp-{key}-t">Similarity of all 253 pairs of loop thumbnails</title>'
         f'<desc id="sp-{key}-d">' + esc(' '.join(f'At {r["label"]}, the highest {word} is {r["pairs"][0]["a"]} with {r["pairs"][0]["b"]} at '
                                                   f'{max(p["v"] for p in r["pairs"]):.2f}.' for r in rows)) + '</desc>']
    axis_y = top + row_h * len(rows) - 14
    for t in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        o.append(f'<path d="M{_f(X(t))} {axis_y}v6" stroke="{stone}" stroke-width="1"/>'
                 f'<text x="{_f(X(t))}" y="{axis_y + 22}" text-anchor="middle" class="sp-tick">{t:.1f}</text>')
    o.append(f'<path d="M{left} {axis_y}H{left + plot_w}" stroke="{stone}" stroke-width="1"/>')
    if key == 'd116':
        o.append(f'<path d="M{_f(X(0.6))} {top - 18}V{axis_y}" stroke="{ink}" stroke-width="2"/>'
                 f'<text x="{_f(X(0.6) + 8)}" y="{top - 6}" class="sp-limit">Limit 0.60 (D1-16)</text>')
    for i, r in enumerate(rows):
        y0 = top + i * row_h + row_h / 2 + 8
        o.append(f'<text x="0" y="{_f(y0 - 2)}" class="sp-row">{esc(r["label"])}</text>'
                 f'<text x="0" y="{_f(y0 + 16)}" class="sp-sub">{esc(r["sub"])}</text>')
        o.append(f'<path d="M{left} {_f(y0)}H{left + plot_w}" stroke="{stone}" stroke-width="0.5"/>')
        o.append(''.join(f'<path d="M{_f(X(pr["v"]))} {_f(y0 - 8)}v16" stroke="{ink}" stroke-width="1"/>' for pr in r['pairs']))
        occupied = {0: [], 1: []}
        for pr in sorted(r['pairs'], key=lambda p: -p['v'])[:label_n]:
            x = X(pr['v'])
            txt_w = _tw(f'{pr["a"]}, {pr["b"]} {pr["v"]:.2f}', 13, 600)
            right_side = key == 'd116' and pr['v'] >= 0.6
            x0, x1 = (x + 5, x + 5 + txt_w) if right_side else (x - 5 - txt_w, x - 5)
            lvl = next((L for L in (0, 1) if all(x1 + 8 < a or x0 - 8 > b for a, b in occupied[L])), None)
            if lvl == 1 and any(a - 3 <= x <= b + 3 for a, b in occupied[0]):
                lvl = None                       # its leader would cut through a label below it
            if lvl is None:
                continue
            occupied[lvl].append((x0, x1))
            ty = y0 - 13 - 16 * lvl
            anchor = 'start' if right_side else 'end'
            if lvl:
                o.append(f'<path d="M{_f(x)} {_f(y0 - 9)}V{_f(ty - 4)}" stroke="{stone}" stroke-width="0.8"/>')
            o.append(f'<text x="{_f(x + 5 if right_side else x - 5)}" y="{_f(ty)}" text-anchor="{anchor}" class="sp-lab">'
                     f'{esc(pr["a"])}, {esc(pr["b"])} <tspan class="sp-num">{pr["v"]:.2f}</tspan></text>')
    o.append('</svg>')
    return ''.join(o)


def floors_plot(floors, width=1000):
    """Per loop, the narrowest width for the full and the compact form."""
    order = sorted(M['loop_order'], key=lambda l: (-floors[l]['full'], M['loop_order'].index(l)))
    left, right, top, rh = 70, 150, 36, 22
    H = top + rh * len(order) + 40
    lo, hi = 70, 340
    plot_w = width - left - right
    ink, stone = P['charcoal'], P['stone']

    def X(v):
        return left + (v - lo) / (hi - lo) * plot_w
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" data-view="size-floors" width="{width}" height="{H}" viewBox="0 0 {width} {H}" role="img" '
         f'aria-labelledby="fl-t fl-d"><title id="fl-t">Narrowest readable width for each loop</title><desc id="fl-d">'
         + esc(' '.join(f'{l}: full form from {floors[l]["full"]} px, compact from {floors[l]["compact"]} px.' for l in order)) + '</desc>']
    axis_y = top + rh * len(order) + 4
    o.append(f'<path d="M{left} {axis_y}H{left + plot_w}" stroke="{stone}" stroke-width="1"/>')
    for t in range(80, 341, 40):
        o.append(f'<path d="M{_f(X(t))} {axis_y}v6" stroke="{stone}" stroke-width="1"/>'
                 f'<text x="{_f(X(t))}" y="{axis_y + 22}" text-anchor="middle" class="sp-tick">{t} px</text>')
    for v in (SIZE['full'], SIZE['compact'], CARD_W):
        o.append(f'<path d="M{_f(X(v))} {top - 16}V{axis_y}" stroke="{ink if v != CARD_W else stone}" stroke-width="{2 if v == SIZE["full"] else 1.2}"/>')
    o.append(f'<text x="{_f(X(SIZE["full"]) - 6)}" y="{top - 4}" text-anchor="end" class="sp-limit">Full form from {SIZE["full"]} px</text>')
    o.append(f'<text x="{_f(X(SIZE["compact"]) - 6)}" y="{top - 4}" text-anchor="end" class="sp-limit">Compact from {SIZE["compact"]} px</text>')
    o.append(f'<text x="{_f(X(CARD_W) + 6)}" y="{top - 4}" class="sp-sub">Catalog, {CARD_W} px</text>')
    for i, l in enumerate(order):
        y = top + i * rh + rh / 2
        f, c = floors[l]['full'], floors[l]['compact']
        o.append(f'<g data-loop="{l}"><text x="0" y="{_f(y + 4.5)}" class="sp-row-s">{l}</text>'
                 f'<path d="M{_f(X(c))} {_f(y)}H{_f(X(f))}" stroke="{stone}" stroke-width="2"/>'
                 f'<circle cx="{_f(X(c))}" cy="{_f(y)}" r="4.5" fill="{P["newsprint"]}" stroke="{ink}" stroke-width="1.6"/>'
                 f'<circle cx="{_f(X(f))}" cy="{_f(y)}" r="4.5" fill="{ink}"/></g>')
    o.append('</svg>')
    return ''.join(o)


CSS = r"""
:root{--news:#DCD9D2;--char:#121212;--prus:#1F2D5A;--stone:#5D636D;--verd:#4A7C74;--white:#FFFFFF;--deep:#4E535B;
--ui:Inter,"Helvetica Neue",Arial,sans-serif;--disp:"Inter Tight",Inter,"Helvetica Neue",Arial,sans-serif}
*{box-sizing:border-box}
html{background:var(--news)}
body{margin:0;background:var(--news);color:var(--char);font-family:var(--ui);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit}
a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--prus);outline-offset:3px}
.wrap{max-width:1440px;margin:0 auto;padding-left:48px;padding-right:48px}
.mast{padding-top:40px;padding-bottom:56px}
.mast-rule{border:0;border-top:2px solid var(--char);margin:0}
.mast-top{display:flex;justify-content:space-between;align-items:center;gap:24px;font-size:13px;font-weight:600;letter-spacing:.02em;color:var(--deep)}
.chip{display:inline-block;background:var(--prus);color:var(--white);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;padding:5px 10px 4px;border-radius:2px}
.mast h1{font-family:var(--disp);font-weight:800;font-size:76px;line-height:.98;letter-spacing:-.025em;margin:40px 0 0;max-width:1000px}
.dek{font-size:21px;line-height:1.45;max-width:880px;margin:24px 0 0}
.draft{font-size:13px;color:var(--deep);margin:14px 0 0}
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:0;margin:44px 0 0;border-top:1px solid var(--char)}
.stat{padding:14px 16px 0 0}
.stat b{display:block;font-family:var(--disp);font-weight:800;font-size:40px;line-height:1;letter-spacing:-.02em}
.stat span{display:block;font-size:13px;line-height:1.35;color:var(--deep);margin-top:8px;max-width:180px}
nav.toc{display:flex;flex-wrap:wrap;gap:8px 28px;padding-top:18px;padding-bottom:18px;font-size:14px;font-weight:600}
nav.toc a{text-decoration:none;padding:2px 0}
nav.toc a span{color:var(--deep);font-weight:500;margin-right:6px}
section{padding-top:72px;padding-bottom:8px}
.sec-head{display:grid;grid-template-columns:120px 1fr;gap:0 24px;align-items:baseline;border-top:1px solid var(--char);padding-top:14px}
.sec-num{font-family:var(--disp);font-weight:800;font-size:15px;letter-spacing:.04em;color:var(--deep)}
.sec-head h2{font-family:var(--disp);font-weight:800;font-size:40px;line-height:1.05;letter-spacing:-.02em;margin:0}
.sec-body{display:grid;grid-template-columns:120px 1fr;gap:0 24px;margin-top:20px}
.sec-body>.col{grid-column:2;min-width:0}
.two>*,.read>*,.pair>*,.sec-head>*{min-width:0}
.lede{font-size:18px;line-height:1.5;max-width:820px;margin:0 0 12px}
.two{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:48px;align-items:start}
.rules p,.rules li{font-size:15px;line-height:1.55;margin:0 0 12px}
.rules ol{padding-left:20px;margin:0}
.rules h3{font-family:var(--disp);font-weight:700;font-size:17px;margin:22px 0 8px}
.figure{background:var(--news)}
.scroll{overflow-x:auto;max-width:100%}
.pk-area{font:600 15px var(--ui);fill:var(--char)}
.pk-letter{font-family:var(--disp);font-weight:800}
.pk-small{font:500 13px var(--ui);fill:var(--deep)}
.pk-id{font:600 13px var(--ui);fill:var(--char)}
.pk-id-s{font:500 13px var(--ui);fill:var(--deep)}
.index{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px 24px;margin-top:28px;border-top:1px solid var(--stone);padding-top:18px}
.index h4{font-family:var(--disp);font-size:14px;font-weight:800;margin:0 0 6px}
.index ul{list-style:none;margin:0;padding:0}
.index li{display:grid;grid-template-columns:40px 1fr;font-size:13px;line-height:1.4;color:var(--char);margin-bottom:3px}
.index li b{font-weight:600}
.facts{font-size:13px;color:var(--deep);margin-top:14px;line-height:1.5}
.read{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,520px);gap:56px;align-items:start}
.legend{display:grid;grid-template-columns:84px 1fr;gap:12px 14px;align-items:center;margin:0}
.legend dt{line-height:0}
.legend dd{margin:0;font-size:14px;line-height:1.4}
.legend dd b{font-weight:600}
.steps{width:100%;border-collapse:collapse;margin-top:24px;font-size:14px}
.steps th{text-align:left;font-size:13px;font-weight:600;color:var(--deep);border-bottom:1px solid var(--char);padding:6px 10px 6px 0}
.steps td{border-bottom:1px solid var(--stone);padding:8px 10px 8px 0;vertical-align:top}
.steps td:first-child{font-weight:700;white-space:nowrap}
@media (max-width:720px){.steps{font-size:13px}.steps th,.steps td{padding-right:6px}}
.sheet{padding-top:56px;padding-bottom:64px;margin-top:64px}
.sheet-head{display:flex;justify-content:space-between;align-items:baseline;gap:24px;margin-bottom:28px}
.sheet-head h3{font-family:var(--disp);font-weight:800;font-size:28px;letter-spacing:-.01em;margin:0}
.sheet-head p{font-size:14px;margin:0;max-width:600px}
.grid{display:grid;grid-template-columns:repeat(4,318px);gap:44px 24px;justify-content:space-between}
.card{border-top:2px solid currentColor;padding-top:10px;min-width:0}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:6px}
.card-id{font-family:var(--disp);font-weight:800;font-size:34px;line-height:1;letter-spacing:-.02em}
.card-kind{font-size:13px;line-height:1.3;text-align:right;color:var(--deep);font-weight:500}
.card-fig{line-height:0;margin:0 0 8px}
.card-title{font-family:var(--ui);font-weight:600;font-size:16px;line-height:1.3;margin:0 0 8px}
.card-stations{font-size:13px;line-height:1.45;margin:0 0 6px;color:var(--deep)}
.card-meta{font-size:13px;line-height:1.4;margin:0 0 6px;color:var(--deep)}
.card-note{position:relative;font-size:13px;line-height:1.45;margin:10px 0 0;padding:8px 0 0 16px;border-top:1px solid var(--stone)}
.note-mark{position:absolute;left:0;top:13px;width:8px;height:8px;background:var(--prus)}
.dark{background:var(--char);color:var(--news)}
.dark .card-kind,.dark .card-stations,.dark .card-meta,.dark .sheet-head p{color:var(--news)}
.dark .card-note{border-top-color:var(--stone)}
.dark .note-mark{background:var(--news)}
.dark a:focus-visible{outline-color:var(--news)}
.ladder{display:flex;flex-wrap:wrap;gap:28px 32px;align-items:flex-end}
.rung{line-height:0}
.rung p{line-height:1.35;font-size:13px;margin:8px 0 0;max-width:318px}
.rung p b{font-weight:700}
.tiers{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0 28px}
.tiers th{text-align:left;font-size:13px;font-weight:600;color:var(--deep);border-bottom:1px solid var(--char);padding:6px 12px 6px 0}
.tiers td{border-bottom:1px solid var(--stone);padding:9px 12px 9px 0;vertical-align:top}
.tiers td:first-child{font-weight:700;white-space:nowrap}
.sp-tick{font:500 13px var(--ui);fill:var(--deep)}
.sp-limit{font:700 13px var(--ui);fill:var(--char)}
.sp-row{font:700 14px var(--ui);fill:var(--char)}
.sp-row-s{font:600 13px var(--ui);fill:var(--char)}
.sp-sub{font:500 13px var(--ui);fill:var(--deep)}
.sp-lab{font:600 13px var(--ui);fill:var(--char)}
.sp-num{font-weight:500;fill:var(--deep)}
.pairs{display:grid;grid-template-columns:1fr;gap:40px;margin-top:40px}
.pair{display:grid;grid-template-columns:auto minmax(0,1fr);gap:32px;align-items:start;border-top:1px solid var(--stone);padding-top:16px}
.pair-figs{display:flex;gap:24px;flex-wrap:wrap}
.pair h4{font-family:var(--disp);font-weight:800;font-size:22px;margin:0 0 4px}
.pair .score{font-size:13px;color:var(--deep);margin:0 0 12px}
.pair p.sep{font-size:14px;line-height:1.5;margin:14px 0 0;max-width:660px}
.pair-fig{line-height:0}
.pair-fig span{display:block;line-height:1.3;font-size:13px;font-weight:700;margin-bottom:6px}
.notes{columns:2;column-gap:56px;font-size:15px;line-height:1.55}
.notes p{margin:0 0 12px;break-inside:avoid}
footer{padding-top:28px;padding-bottom:56px;margin-top:72px;font-size:13px;line-height:1.5;color:var(--deep)}
footer .rule{border-top:2px solid var(--char);padding-top:28px}
footer p{margin:0 0 6px;max-width:1000px}
@media (max-width:1380px){.grid{grid-template-columns:repeat(3,318px)}}
@media (max-width:1060px){.grid{grid-template-columns:repeat(2,318px);justify-content:start}.two,.read,.pair{grid-template-columns:1fr}.index{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:720px){.wrap{padding:0 16px}.mast h1{font-size:44px}.dek{font-size:18px}.stats{grid-template-columns:repeat(2,1fr)}.sec-head,.sec-body{grid-template-columns:1fr}.sec-body>.col{grid-column:1}.sec-num{margin-bottom:4px}.sec-head h2{font-size:30px}
.grid{grid-template-columns:318px;justify-content:center}.index{grid-template-columns:repeat(2,minmax(0,1fr))}.notes{columns:1}.sheet-head{display:block}.sheet-head p{margin-top:8px}.mast-top{flex-wrap:wrap}}
"""


def pair_score(res, a, b):
    return next(p['score'] for p in res['pairs'] if {p['a'], p['b']} == {a, b})


def page(pl, routes, floors, sim, con):
    order = M['loop_order']
    C = M['generated']['counts']
    n_two = sum(1 for l in LOOPS.values() if l['n'] == 2)
    n_three = sum(1 for l in LOOPS.values() if l['n'] == 3)
    n_four = sum(1 for l in LOOPS.values() if l['n'] == 4)
    study = sim[str(CARD_W)]
    top = study['pairs'][0]
    full_floor, compact_floor = SIZE['full'], SIZE['compact']
    binding = max(floors, key=lambda l: floors[l]['full'])
    second = sorted(floors.values(), key=lambda v: -v['full'])[1]['full']
    loc_floor = max(v['locator'] for v in floors.values())
    sys_ = con['system']
    opt = con['overview_options']
    # cards
    news_cards = ''.join(card(l, routes[l], pl, 'newsprint', f'n-{l}') for l in order)
    dark_cards = ''.join(card(l, routes[l], pl, 'charcoal', f'c-{l}') for l in order)
    # R10 at twice size
    r10 = thumb_svg('R10', routes['R10'], pl, CARD_W, uid='big-R10', view='loop-route-2x')
    hpx = frame(pl)['h'] * CARD_W / frame(pl)['w']
    r10 = r10.replace(f'width="{_f(CARD_W)}" height="{_f(hpx)}"', f'width="{CARD_W * 2}" height="{_f(hpx * 2)}" style="max-width:100%;height:auto"', 1)
    step_rows = ''.join(
        f'<tr data-link="{s["id"]}" data-sign="{s["polarity"]}" data-grade="{s["evidence"]}" data-delay="{s["delay"]}">'
        f'<td>{s["id"]}</td><td>{esc(s["from_label"])} {"raises" if s["polarity"] == "+" else "lowers"} {esc(s["to_label"])}'
        f'{". This step closes the loop." if s["closing"] else ""}</td>'
        f'<td>{"+" if s["polarity"] == "+" else MINUS}</td><td>{acc.GRADES[s["evidence"]][0]}, {acc.GRADES[s["evidence"]][2]}</td>'
        f'<td>{acc.DELAYS[s["delay"]]}</td></tr>'
        for s in LOOPS['R10']['steps'])
    legend = ''.join(f'<dt>{_mini(k)}</dt><dd>{v}</dd>' for k, v in (
        ('documented', '<b>Solid:</b> documented (on the public record) or well supported (strong research evidence)'),
        ('plausible', '<b>Dashed:</b> plausible (some evidence)'),
        ('plausible_contested', '<b>Dash and dot:</b> contested (evidence disputed)'),
        ('hypothesis', '<b>Dotted:</b> hypothesis (untested)'),
        ('+', '<b>Tag with a plus:</b> the two variables move the same way. The tag points the way the step runs. A plus does not mean the change is good.'),
        ('-', '<b>Tag with a minus:</b> the two variables move opposite ways.'),
        ('start', '<b>Ring:</b> the loop\'s first station in V7. The bar marks the closing step, the one that returns to the ring.'),
        ('sketch', '<b>Hollow line and open station:</b> a sketched step with no numbered connection, off the map.'),
        ('area', '<b>Heavier outline:</b> an area where the loop stops. Lighter outlines are the rest of the system.'),
    ))
    # index of variables by area
    idx = []
    for a in ['X', 'A', 'B', 'C', 'D', 'E'] + pl['ground_order']:
        items = ''.join(f'<li data-node="{v}"><b>{v}</b><span data-node="{v}" data-name="{esc(NODES[v]["label"])}">{esc(NODES[v]["label"])}</span></li>'
                        for v in AREAS[a]['nodes'])
        idx.append(f'<div><h4>{a if len(a) <= 2 else ""}{" " if len(a) <= 2 else ""}{esc(AREAS[a]["title"])}</h4><ul>{items}</ul></div>')
    # size ladder
    ladder_sizes = [CARD_W, full_floor, compact_floor, 200, 140]
    rungs = []
    for lid in ('R12', 'R8'):
        for w in ladder_sizes:
            t = size_tier(w)
            svg = thumb_svg(lid, routes[lid], pl, w, uid=f'lad-{lid}-{w}', view='loop-route-ladder')
            rungs.append(f'<div class="rung">{svg}<p><b>{lid}, {w} px</b><br>{t.capitalize()} form</p></div>')
    # similarity rows
    sizes_sorted = sorted(sim, key=lambda k: -int(k))

    def rowset(key):
        rs = []
        for k in sizes_sorted:
            r = sim[k]
            v = 'score' if key == 'd116' else 'squint_corr'
            rs.append({'label': f'{r["width"]} px', 'sub': f'{r["tier"]} form' + (f', blur {r["squint_radius_px"]} px' if key != 'd116' else ''),
                       'pairs': [{'a': p['a'], 'b': p['b'], 'v': p[v]} for p in r['pairs']]})
        return rs
    plot_d116 = strip_plot(rowset('d116'), 'd116')
    plot_sq = strip_plot(rowset('squint'), 'squint')
    pair_blocks = []
    for p in study['pairs'][:4]:
        figs = ''.join(f'<div class="pair-fig"><span>{x}</span>{thumb_svg(x, routes[x], pl, CARD_W, uid=f"pr-{p["a"]}-{p["b"]}-{x}", view="loop-route-pair")}</div>'
                       for x in (p['a'], p['b']))
        pair_blocks.append(f'<div class="pair"><div class="pair-figs">{figs}</div><div class="pair-text"><h4>{p["a"]} and {p["b"]}</h4>'
                           f'<p class="score">D1-16 score {p["score"]:.2f} at {CARD_W} px: silhouette overlap {p["silhouette_iou"]:.2f}, '
                           f'blurred correlation {p["blurred_corr"]:.2f}. Squint {p["squint_corr"]:.2f}.</p>'
                           f'<p class="sep">{esc(separation(p["a"], p["b"], routes))}</p></div></div>')
    over = study['over_limit']
    sq_top = max(study['pairs'], key=lambda p: p['squint_corr'])
    worst_small = sim[str(min(int(k) for k in sim))]
    tiers_rows = ''.join(
        f'<tr><td>{t.capitalize()}</td><td>{lo}</td><td>{esc(TIERS[t])}</td></tr>' for t, lo in (
            ('full', f'{full_floor} px and wider'), ('compact', f'{compact_floor} to {full_floor - 2} px'), ('locator', f'under {compact_floor} px')))
    html_ = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Loop Route Thumbnails</title>
<meta name="description" content="Study: each of the 23 Atlas V7 loops drawn as its own route across one canonical plan of the system, with sign, direction, evidence texture and closure, and a measured test of how distinct the 23 thumbnails are.">
<meta name="atlas-views" content="study">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Inter+Tight:wght@600;700;800&amp;display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<main data-view-root="study">
<header class="wrap mast">
  <div class="mast-top"><span>Oath and Action Systems Atlas &middot; Atlas concepts &middot; Shared grammar for all twelve concepts &middot; October 30, 2026</span><span class="chip">Study</span></div>
  <h1>Every loop draws its own route</h1>
  <p class="dek">The atlas has <span data-count="loops">{C["loops"]}</span> feedback loops. {nw(n_two, True)} have two steps, {nw(n_three)} have three and {nw(n_four)} have four, so a loop icon drawn by its step count repeats three shapes. This study draws each loop as the path it takes across one shared plan of the system. The plan is the same in every thumbnail, so each one also shows where in the system its loop lives.</p>
  <p class="draft">Headlines on this page are studio drafts. Every label, sign and grade is read from the Atlas V7 model export by script (DR-20). Decision DR-15.</p>
  <div class="stats">
    <div class="stat"><b data-count="loops">{C["loops"]}</b><span>loops, in catalog order</span></div>
    <div class="stat"><b data-count="loops_numbered">{C["loops_numbered"]}</b><span>with a complete numbered chain</span></div>
    <div class="stat"><b data-count="loops_sketched">{len(sys_["loops_sketched"])}</b><span>sketches, drawn off the map (B2, B3, R9)</span></div>
    <div class="stat"><b data-count="variables">{C["variables"]}</b><span>variables placed on the plan by one rule</span></div>
    <div class="stat"><b>{study["max_score"]:.2f}</b><span>highest similarity of any two thumbnails, against the 0.60 limit</span></div>
    <div class="stat"><b>{full_floor}</b><span>pixels wide: the narrowest catalog size that carries every mark</span></div>
  </div>
</header>
<div class="wrap"><hr class="mast-rule"></div>
<nav class="wrap toc" aria-label="Sections">
  <a href="#plan"><span>01</span>The plan</a><a href="#read"><span>02</span>How to read a route</a><a href="#newsprint"><span>03</span>Catalog on Newsprint</a><a href="#charcoal"><span>04</span>Catalog on Charcoal</a><a href="#size"><span>05</span>Size</a><a href="#distinct"><span>06</span>Distinctness</a><a href="#open"><span>07</span>Open points</a>
</nav>

<section id="plan" class="wrap">
  <div class="sec-head"><span class="sec-num">01</span><h2>One plan of the system, shared by every thumbnail</h2></div>
  <div class="sec-body"><div class="col">
    <div class="two">
      <div class="rules">
        <p>The plan has three tiers. The five outside drivers run across the top. The civic core sits in the middle. The economy and technology layers run along the bottom, where V7 puts them under the core.</p>
        <p>The core is a ring in V7's letter order. A, B and C run across the top row, then D and E come back along the bottom. The core's <span data-count="custom:core-cross">{sys_["core_cross_area"]}</span> connections between areas join only A and B, B and C, C and D, D and E, E and A, B and D, and B and E, so in the ring every one of them joins two neighbors. In a single row from A to E, {sys_["core_cross_area_jumping_an_area_in_one_row"]} of them would jump over an area.</p>
        <h3>Where each variable sits</h3>
        <ol>
          <li>Each area holds a grid of slots: two columns by three rows for A, B and C, two by two for E, four by two for D, and two rows in each area of the bottom tier.</li>
          <li>Each variable takes the slot nearest the average place of everything it connects to, counting all {C["connections"]} connections of every type. One assignment per area finds the arrangement with the least total distance.</li>
          <li>The script repeats the assignments until no variable moves ({pl["rounds"]} rounds), and tries all 24 orders of the bottom tier's four areas. It keeps the order with the shortest total length of connections: {", ".join(AREAS[a]["title"] for a in pl["ground_order"])}.</li>
        </ol>
        <h3>The margin</h3>
        <p>The three sketched loops have stations that are not variables in the model. They sit in a margin on the left, outside every area, beside the variables they are tied to: the station a sketch names (R9 touches E2), or else the variables its reforms target.</p>
        <p class="facts">Plan size {pl["width"]:.1f} by {pl["height"]:.2f} columns; with the margin, {frame(pl)["w"]:.2f} by {frame(pl)["h"]:.2f}. Positions for all {C["variables"]} variables are in 20261030_Loop-Route-Geometry.json.</p>
      </div>
      <div class="figure"><div class="scroll" role="region" tabindex="0" aria-label="The canonical plan, scrolls sideways on small screens">{key_plan_svg(pl)}</div></div>
    </div>
    <div class="index">{"".join(idx)}</div>
  </div></div>
</section>

<section id="read" class="wrap">
  <div class="sec-head"><span class="sec-num">02</span><h2>How to read a route</h2></div>
  <div class="sec-body"><div class="col">
    <p class="lede">R10, &ldquo;{esc(LOOPS["R10"]["title"])}&rdquo;, at twice catalog size. Each step is an arc between two stations. Arcs bow outward from the middle of the loop, so a route always reads as a closed circuit. A two-station loop becomes a small ring.</p>
    <div class="read">
      <div><div class="figure">{r10}</div>
        <table class="steps" aria-label="R10 in words"><thead><tr><th>Step</th><th>What it says</th><th>Sign</th><th>Evidence and line</th><th>Delay</th></tr></thead><tbody>{step_rows}</tbody></table>
        <p class="facts">{esc(_weakest("R10"))}. Delay stays out of the thumbnail; the loop card carries it.</p>
      </div>
      <dl class="legend">{legend}</dl>
    </div>
  </div></div>
</section>

<section id="newsprint" class="sheet">
  <div class="wrap">
    <div class="sheet-head"><h3>All {C["loops"]} loops on Newsprint</h3><p>Catalog order from V7 (loop_order). Each thumbnail is {CARD_W} px wide, the full form. Pillar Red is used for nothing here.</p></div>
    <div class="grid" data-strip="loops">{news_cards}</div>
  </div>
</section>

<section id="charcoal" class="sheet dark">
  <div class="wrap">
    <div class="sheet-head"><h3>The same sheet on Charcoal</h3><p>Routes and text in Newsprint, the plan in Stone. The marks and sizes do not change.</p></div>
    <div class="grid" data-strip="loops">{dark_cards}</div>
  </div>
</section>

<section id="size" class="wrap">
  <div class="sec-head"><span class="sec-num">05</span><h2>How small a thumbnail can go</h2></div>
  <div class="sec-body"><div class="col">
    <p class="lede">The marks keep their size while the plan shrinks, so short steps run out of room first. The script finds, for each loop, the narrowest width at which every step still holds its tag and one whole repeat of its line pattern. {binding} sets the floor at {full_floor} px through its closing step; every other loop reads at {second} px or less.</p>
    <table class="tiers"><thead><tr><th>Form</th><th>Width</th><th>What it carries</th></tr></thead><tbody>{tiers_rows}</tbody></table>
    <div class="ladder">{"".join(rungs)}</div>
    <p class="facts">Below {compact_floor} px the line patterns, the direction and the signs drop out, and the thumbnail works as a locator only. Its station discs stay apart down to {loc_floor} px; whether a reader still finds the area at that size is untested.</p>
    <div class="scroll" role="region" tabindex="0" aria-label="Floors for each loop" style="margin-top:28px">{floors_plot(floors)}</div>
    <p class="facts">Filled dot: the full form's floor. Open dot: the compact form's floor.</p>
  </div></div>
</section>

<section id="distinct" class="wrap">
  <div class="sec-head"><span class="sec-num">06</span><h2>Twenty-three different pictures</h2></div>
  <div class="sec-body"><div class="col">
    <p class="lede">Chromium renders every thumbnail, and the script scores all {len(study["pairs"])} pairs with the studio's D1-16 method: the mean of the overlap of the two filled route shapes and the correlation of the two drawings after a 3 by 3 blur. Two marks count as distinct under 0.60. The shared plan is left in, which raises every score.</p>
    <p class="lede">At {CARD_W} px the highest score is {top["score"]:.2f}, for {top["a"]} and {top["b"]}, and the median is {study["median_score"]:.2f}. {"None" if not over else nw(len(over), True)} of the {len(study["pairs"])} pairs {"reaches" if len(over) <= 1 else "reach"} the limit. At {worst_small["width"]} px, in the {worst_small["tier"]} form, the highest is {worst_small["max_score"]:.2f}, for {worst_small["pairs"][0]["a"]} and {worst_small["pairs"][0]["b"]}, which is over the limit.</p>
    <div class="scroll" role="region" tabindex="0" aria-label="Scores for all pairs">{plot_d116}</div>
    <p class="lede" style="margin-top:28px">A stricter squint test blurs each drawing by about a fortieth of its width before correlating. It has no limit in the decision log, so it is reported, not used to pass or fail. The closest pair there is {sq_top["a"]} and {sq_top["b"]} at {sq_top["squint_corr"]:.2f}.</p>
    <div class="scroll" role="region" tabindex="0" aria-label="Squint correlations for all pairs">{plot_sq}</div>
    <div class="pairs">{"".join(pair_blocks)}</div>
  </div></div>
</section>

<section id="open" class="wrap">
  <div class="sec-head"><span class="sec-num">07</span><h2>Open points</h2></div>
  <div class="sec-body"><div class="col notes">
    <p>The sign mark is the pointing tag, the studio's recommendation in Choice 3 of the October 28 review, which Dustin has not yet decided. If he picks the circled sign, each step needs an arrowhead as well, and the floor rises.</p>
    <p>The plan is a proposal for every concept to adapt. A concept may stretch a tier or redraw the outlines; the ring order and the slot of each variable are what keep its thumbnails comparable with the others.</p>
    <p>Two-step loops make small rings. Their size and place on the plan carry the difference between them. R13 and R18 both sit in area D and share D2. From D2, R13's other station (D1) sits straight below and R18's (D4) below and to the left, and the pair scores {pair_score(study, "R13", "R18"):.2f} at {CARD_W} px.</p>
    <p>No reader has seen these thumbnails. The ten-second test and a blind matching test (five readers, a thumbnail and three titles) would show whether the measured distinctness holds for people.</p>
    <p>The sketched loops sit beside the variables their reforms target. That placement comes from the reforms, not from a connection in the model, and each card says so.</p>
    <p>The faint outlines of the areas a loop does not visit are context. They are drawn in Stone at {MARKS["plan_w"]} px; the outlines of the areas it visits are {MARKS["plan_visited"]} px.</p>
  </div></div>
</section>
</main>
<footer class="wrap"><div class="rule">
  <p>Data: Atlas V7 model, snapshot October 15, 2026, from the committed export work/boards/phase-2/maps/20261028_Maps-Model-Data.json (DR-20). <span data-count="variables">{C["variables"]}</span> variables, <span data-count="connections">{C["connections"]}</span> connections, <span data-count="loops">{C["loops"]}</span> loops, <span data-count="reforms">{C["reforms"]}</span> reforms.</p>
  <p>Built by work/build/scripts/phase-2/atlas_loop_routes.py. Geometry for concept makers: work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Geometry.json. Notes: work/handoffs/phase-2/20261030_Atlas-Dataviz-Memo.md.</p>
  <p>Study for the atlas concepts. Not a concept, and not for publication.</p>
</div></footer>
</body>
</html>
'''
    return html_


# ---------------------------------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------------------------------
NODE_CAPTURE = r"""
const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(1);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await page.goto('file://' + src, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  await page.screenshot({ path: out, fullPage: true });
  const fonts = await page.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '') + ' ' + f.weight))]);
  console.log(JSON.stringify({ fonts }));
  await browser.close();
})();
"""


def geometry_json(pl, routes, floors, sim, con):
    fr = frame(pl)
    var = {}
    for v, (x, y) in pl['pos'].items():
        a = AREA_OF[v]
        var[v] = {'area': a, 'x': round(x, 4), 'y': round(y, 4), 'slot': pl['slots'][a].index((x, y)), 'label': NODES[v]['label']}
    rts = {}
    for lid in M['loop_order']:
        rt = routes[lid]
        steps = []
        for s in rt['steps']:
            a = s['arc']
            d = (f'M{a["a"][0]:.4f} {a["a"][1]:.4f}A{a["radius"]:.4f} {a["radius"]:.4f} 0 0 {a["sweep"]} {a["b"][0]:.4f} {a["b"][1]:.4f}')
            steps.append({k: s[k] for k in ('index', 'id', 'from', 'to', 'from_label', 'to_label', 'polarity', 'type', 'delay', 'evidence', 'closing', 'sketch')}
                         | {'arc': {'from': [round(c, 4) for c in a['a']], 'to': [round(c, 4) for c in a['b']],
                                    'center': [round(c, 4) for c in a['center']], 'radius': round(a['radius'], 4),
                                    'sagitta': round(a['sagitta'], 4), 'side': a['side'], 'sweep': a['sweep'], 'apex': [round(c, 4) for c in a['apex']],
                                    'chord': round(a['chord'], 4), 'd': d}})
        rts[lid] = {'type': LOOPS[lid]['type'], 'kind_word': LOOPS[lid]['kind_word'], 'title': LOOPS[lid]['title'],
                    'closure': LOOPS[lid]['closure'], 'steps_attr': 'sketch' if LOOPS[lid]['conceptual'] else ' '.join(s['id'] for s in LOOPS[lid]['steps']),
                    'stations': [{**s, 'pos': [round(c, 4) for c in s['pos']]} for s in rt['stations']], 'steps': steps,
                    'inline': rt['inline'], 'sketch_placement': rt['sketch'], 'disclosure': disclosure(lid, rt),
                    'size_floor_px': floors[lid]}
    return {
        'date': '20261030', 'decision': 'DR-15',
        'model': 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json', 'snapshot': M['generated']['snapshot'],
        'built_by': 'work/build/scripts/phase-2/atlas_loop_routes.py',
        'units': 'Plan units: one top-row core column = 1.0; x to the right, y down. The frame adds a margin for the sketched loops. Scale by (thumbnail width / frame.w).',
        'plan': {'width': round(pl['width'], 4), 'height': round(pl['height'], 4), 'frame': {k: round(v, 4) for k, v in fr.items()},
                 'margin': MARGIN, 'tiers': {'top': ['X'], 'core_top_row': [a for a, _ in TOP], 'core_bottom_row': [a for a, _ in BOTTOM],
                                             'ground': pl['ground_order']},
                 'boxes': {a: [round(c, 4) for c in b] for a, b in pl['boxes'].items()},
                 'slots': {a: [[round(x, 4), round(y, 4)] for x, y in s] for a, s in pl['slots'].items()},
                 'variables': var, 'total_connection_length': pl['total_length'], 'rounds': pl['rounds'],
                 'ground_order_trials': pl['trials'],
                 'rule': ('Each variable takes the slot of its own area nearest the mean place of all its partners across the 118 '
                          'connections; one least-squares assignment per area, repeated until no variable moves; the bottom tier '
                          'order is the one of 24 with the shortest total connection length.')},
        'grammar': {'marks_px': MARKS, 'line_code': {g: (DASH[g] or 'solid') for g in DASH} | {'sketch': 'hollow line'},
                    'dash_note': 'Dash lengths are V7 code for a 2 px line, scaled by weight / 2.',
                    'bulge': {'two_station': BULGE_TWO, 'many': BULGE_MANY, 'inline': BULGE_INLINE, 'cap_columns': BULGE_MAX,
                              'rule': 'Sagitta = share x chord, capped. Steps bow away from the mean of the loop stations; two-station loops and loops in a line bow to the right of travel.'},
                    'tiers': TIERS, 'size_floor_px': dict(SIZE), 'catalog_width_px': CARD_W},
        'routes': rts,
        'distinctness': {k: {kk: vv for kk, vv in v.items() if kk != 'pairs'} | {'top_pairs': v['pairs'][:12]} for k, v in sim.items()},
        'distinctness_all_pairs': {k: v['pairs'] for k, v in sim.items()},
        'contract': con,
    }


def main():
    pl = plan()
    routes = {l: route(l, pl) for l in M['loop_order']}
    floors = size_floors(pl, routes)
    SIZE['full'] = max(v['full'] for v in floors.values())
    SIZE['compact'] = max(v['compact'] for v in floors.values())
    assert CARD_W >= SIZE['full'], 'the catalog would fall below the full form'
    sim = measure(pl, routes, [CARD_W, SIZE['full'], SIZE['compact'], 200])
    con = contract(pl)
    SHARED.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(geometry_json(pl, routes, floors, sim, con), indent=1, ensure_ascii=False))
    OUT_HTML.write_text(page(pl, routes, floors, sim, con))
    res = subprocess.run(['node', '-e', NODE_CAPTURE, str(OUT_HTML), str(OUT_PNG)], capture_output=True, text=True, timeout=300)
    if res.returncode:
        raise RuntimeError(res.stderr[-2000:])
    im = Image.open(OUT_PNG)
    print('wrote', OUT_JSON.relative_to(ROOT))
    print('wrote', OUT_HTML.relative_to(ROOT), f'{OUT_HTML.stat().st_size // 1024} KB')
    print('wrote', OUT_PNG.relative_to(ROOT), im.size, res.stdout.strip())
    print('floors', SIZE, 'study max', sim[str(CARD_W)]['max_score'], 'over limit', len(sim[str(CARD_W)]['over_limit']))
    for k, v in sim.items():
        print(' ', k, v['tier'], 'max', v['max_score'], 'median', round(v['median_score'], 3), 'max squint', v['max_squint'], 'over', len(v['over_limit']))


if __name__ == '__main__':
    main()
