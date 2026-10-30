"""Build Concept 01, The Circuit, refined (Oath & Action atlas concepts, October 30, 2026).

Writes 20261030_Concept-01-The-Circuit.html beside this file from the model export
work/boards/phase-2/maps/20261028_Maps-Model-Data.json. Every label, sign, grade, delay, count and title on the page
is read from the model here; every printed count is derived from the model and asserted before the page is written.

The idea, from Dustin's Concepts V2, Concept 09: the five core areas as cards read left to right, in the order effects
mostly travel, wired together. This build keeps the idea and fixes what the creative director flagged on October 28:
  - each side wire plugs into a named variable (a pin), and the build orders and spaces the rows so most wires run
    straight across a gap; area E's two variables become tall terminals, so the nine wires between D and E run flat;
  - wires that skip an area ride one ribbon over the top, and the return line wraps the whole board back to area A;
  - the economy and technology layers sit under the cards they talk to, so the lower channel runs mostly straight down;
  - every wire can be isolated by hover, focus or tap (the shared atlas kit).

Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/01-the-circuit/build_concept.py
It measures text with the real web fonts through measure_text.js (Playwright) and caches the widths in
20261030_Text-Metrics-Cache.json beside this file.
"""
import html
import importlib.util
import itertools
import json
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

M = acc.load_model()
P = acc.PALETTE
NP, CH, RED, PR, ST, VG, WH, DS = (P['newsprint'], P['charcoal'], P['pillar_red'], P['prussian'], P['stone'],
                                    P['verdigris'], P['white'], P['deep_stone'])
N, LK, LOOPS, REF = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
AREA_OF = {}
for _a in M['areas']:
    for _n in _a['nodes']:
        AREA_OF[_n] = _a['id']
CORE = ['A', 'B', 'C', 'D', 'E']
LOWER = ['household', 'production', 'money', 'TC']
MINUS = '−'
NBSP = ' '
e = html.escape
OUT = HERE / '20261030_Concept-01-The-Circuit.html'
CACHE = HERE / '20261030_Text-Metrics-Cache.json'
SNAP = 'October 15, 2026'
assert M['generated']['snapshot'] == '2026-10-15'


# ------------------------------------------------------------------------------------------------ text metrics
FONTS = {
    'map': ('600 15px Inter', 15), 'code': ('700 14px Inter', 14), 'note': ('400 13px Inter', 13),
    'legend': ('500 13px Inter', 13), 'legend6': ('600 13px Inter', 13), 'eyebrow': ('700 13px Inter', 13),
    'panel': ('800 22px "Inter Tight"', 22), 'station': ('700 20px "Inter Tight"', 20),
    'caption': ('400 14px Inter', 14), 'ptext': ('400 15px Inter', 15), 'figure': ('800 40px "Inter Tight"', 40),
    'body': ('400 17px Inter', 17), 'code13': ('700 13px Inter', 13), 'tight16': ('800 22px "Inter Tight"', 22),
}
TRACK = {'eyebrow': 0.06}
_cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
_missing = set()


def tw(style, text):
    """Rendered width of text in px, measured in the browser with the real fonts (cached)."""
    font, size = FONTS[style]
    key = font + '|' + text
    if key not in _cache:
        _missing.add((font, text))
        w = len(text) * size * 0.56
    else:
        w = _cache[key]
    return w + TRACK.get(style, 0) * size * len(text)


def measure_missing():
    if not _missing:
        return False
    items = sorted(_missing)
    tmp_in, tmp_out = HERE / '.measure-in.json', HERE / '.measure-out.json'
    tmp_in.write_text(json.dumps([list(x) for x in items]))
    subprocess.run(['node', str(HERE / 'measure_text.js'), str(tmp_in), str(tmp_out)], check=True)
    widths = json.loads(tmp_out.read_text())
    for (font, text), w in zip(items, widths):
        _cache[font + '|' + text] = w
    tmp_in.unlink()
    tmp_out.unlink()
    CACHE.write_text(json.dumps(_cache, indent=0, sort_keys=True))
    _missing.clear()
    return True


def wrap(text, max_w, style):
    words, lines, cur = text.split(' '), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if not cur or tw(style, t) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def balanced(text, max_w, style):
    """Fewest lines that fit, with the lines evened out so no line ends on one short word."""
    g = wrap(text, max_w, style)
    if len(g) <= 1:
        return g
    best, score = g, None
    lo, hi = 0.35 * max_w, max_w
    for _ in range(16):
        mid = (lo + hi) / 2
        t = wrap(text, mid, style)
        if len(t) <= len(g) and all(tw(style, x) <= max_w for x in t):
            hi = mid
            ws = [tw(style, x) for x in t]
            s = max(ws) - min(ws)
            if score is None or s <= score:
                best, score = t, s
        else:
            lo = mid
    return best


# ------------------------------------------------------------------------------------------------ model words
def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


def texture(g):
    return acc.GRADES[g][2] if g else 'hollow'


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def verb(p):
    return acc.SIGN_WORDS[p if p in ('+', '-') else None]


def delay_word(d):
    return acc.DELAYS[d]


def label(v):
    return N[v]['label']


def link_sentence(k):
    """The connection in words, as the interaction memo asks: name, ends, sign in words, grade, delay."""
    l = LK[k]
    if l['polarity'] in ('+', '-'):
        sg = f"Sign {sign_char(l['polarity'])}, {'same way' if l['polarity'] == '+' else 'opposite way'}: it {verb(l['polarity'])} it."
    else:
        sg = 'No sign: an authority connection, which says who decides.'
    return (f"{k}: {l['name']}. From {l['from']} {label(l['from'])} to {l['to']} {label(l['to'])}. {sg} "
            f"Evidence {grade_word(l['evidence']).lower()}: {grade_gloss(l['evidence'])}. Delay {delay_word(l['delay'])}.")


def first_sentence(t):
    m = re.match(r'(.+?[.!?])(\s|$)', t)
    return m.group(1) if m else t


def read_aloud(loop_id):
    """More and less, multiplied along the chain from the signs: 'More safe seats, more ..., and back to more safe seats.'"""
    lp = LOOPS[loop_id]
    st = lp['stations']
    words, s = [], 1
    for i, station in enumerate(st):
        words.append(('more ' if s > 0 else 'less ') + station['label'][0].lower() + station['label'][1:])
        if i < len(lp['steps']):
            s *= -1 if lp['steps'][i]['polarity'] == '-' else 1
    back = ('more ' if s > 0 else 'less ') + st[0]['label'][0].lower() + st[0]['label'][1:]
    first = words[0][0].upper() + words[0][1:]
    return first + ', ' + ', '.join(words[1:]) + ', and back to ' + back + '.'


# keep proper-noun capitals inside the read-aloud line
_LOWER_FIX = {}


# ------------------------------------------------------------------------------------------------ line geometry
W_REST, W_HI, W_SEL = 2, 3, 6          # the stroke family for wires (design frame memo, D2-60)
TAG = (10, 5, 12, 7, 2)                # overview tag: body, point, height, sign arm, sign bar (on 2 px wires)
TAG_BIG = (15, 6, 17, 9, 3)            # close-up tag on 3 px steps (design frame memo)
TP = 12                                # pitch of wire tracks at one pin
LP = 8                                 # pitch of jog lanes in a gap
RP = 6                                 # pitch of parallel tracks in a ribbon (6 px at 2 px, memo)
RB = 8                                 # corner radius at 2 px (memo: 8 px), concentric where tracks run parallel


def fmt(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s if s != '-0' else '0'


def rounded(pts, r=RB, radii=None):
    """An orthogonal polyline as a path with round corners. Returns (d, length)."""
    pts = [p for i, p in enumerate(pts) if i == 0 or (abs(p[0] - pts[i - 1][0]) > 0.01 or abs(p[1] - pts[i - 1][1]) > 0.01)]
    d = f'M{fmt(pts[0][0])} {fmt(pts[0][1])}'
    length = 0.0
    cur = pts[0]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        la = math.hypot(b[0] - a[0], b[1] - a[1])
        lb = math.hypot(c[0] - b[0], c[1] - b[1])
        rr = (radii[i] if radii else r)
        rr = min(rr, la / 2 if i > 1 else la, lb / 2 if i < len(pts) - 2 else lb)
        ux, uy = (b[0] - a[0]) / la, (b[1] - a[1]) / la
        vx, vy = (c[0] - b[0]) / lb, (c[1] - b[1]) / lb
        p1 = (b[0] - ux * rr, b[1] - uy * rr)
        p2 = (b[0] + vx * rr, b[1] + vy * rr)
        cross = ux * vy - uy * vx
        if abs(cross) < 1e-6:
            d += f'L{fmt(b[0])} {fmt(b[1])}'
            length += math.hypot(b[0] - cur[0], b[1] - cur[1])
            cur = b
            continue
        sweep = 1 if cross > 0 else 0
        d += f'L{fmt(p1[0])} {fmt(p1[1])}A{fmt(rr)} {fmt(rr)} 0 0 {sweep} {fmt(p2[0])} {fmt(p2[1])}'
        length += math.hypot(p1[0] - cur[0], p1[1] - cur[1]) + math.pi * rr / 2
        cur = p2
    d += f'L{fmt(pts[-1][0])} {fmt(pts[-1][1])}'
    length += math.hypot(pts[-1][0] - cur[0], pts[-1][1] - cur[1])
    return d, length


def pattern(tex):
    """The V7 evidence code as multiples of the line width (design frame memo, section 3)."""
    return {'dashed': ([4, 2], 'butt'), 'dash-dot': ([4, 1.5, 1, 1.5], 'butt'), 'dotted': ([0, 2.5], 'round')}.get(tex, (None, 'butt'))


def fit_k(tex, length, w=W_REST):
    """Scale factor so the pattern starts and ends on ink at the resting width (memo rule 3.2)."""
    arr, _ = pattern(tex)
    if not arr:
        return 1.0
    arr = [x * w for x in arr]
    if tex == 'dotted':
        n = max(1, round(length / arr[1]))
        return length / (n * arr[1])
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    return length / (n * per + arr[0])


def tag_shape(tip, direction, sign, size=TAG, cls='tag'):
    """The pointing tag: the sign mark that doubles as the arrowhead (D2-56). direction: 'r','l','u','d'."""
    a, p, h, sl, sb = size
    L = a + p
    x, y = tip
    # local frame: points toward +x, tip at (0, 0)
    loc = [(-L, -h / 2), (-p, -h / 2), (0, 0), (-p, h / 2), (-L, h / 2)]
    cx = -p - a / 2
    rot = {'r': (1, 0), 'l': (-1, 0), 'd': (0, 1), 'u': (0, -1)}[direction]

    def tr(px, py):
        return (x + px * rot[0] - py * rot[1], y + px * rot[1] + py * rot[0])
    poly = ' '.join(f'{fmt(qx)},{fmt(qy)}' for qx, qy in (tr(*q) for q in loc))
    bx, by = tr(cx, 0)
    bars = f'<rect x="{fmt(bx - sl / 2)}" y="{fmt(by - sb / 2)}" width="{sl}" height="{sb}"/>'
    if sign == '+':
        bars += f'<rect x="{fmt(bx - sb / 2)}" y="{fmt(by - sl / 2)}" width="{sb}" height="{sl}"/>'
    if sign not in ('+', '-'):
        bars = ''
    org = f'{fmt(x)}px {fmt(y)}px'
    return f'<g class="{cls}" style="transform-origin:{org}"><polygon points="{poly}"/>{bars}</g>', L


def diamond_shape(tip, direction, size=(14, 11), cls='dia'):
    ln, wd = size
    x, y = tip
    rot = {'r': (1, 0), 'l': (-1, 0), 'd': (0, 1), 'u': (0, -1)}[direction]
    loc = [(0, 0), (-ln / 2, -wd / 2), (-ln, 0), (-ln / 2, wd / 2)]

    def tr(px, py):
        return (x + px * rot[0] - py * rot[1], y + px * rot[1] + py * rot[0])
    poly = ' '.join(f'{fmt(qx)},{fmt(qy)}' for qx, qy in (tr(*q) for q in loc))
    org = f'{fmt(x)}px {fmt(y)}px'
    return f'<g class="{cls}" style="transform-origin:{org}"><polygon points="{poly}"/></g>', ln


def trim_end(pts, d):
    """Shorten the last straight segment of an orthogonal polyline by d."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    L = math.hypot(x1 - x0, y1 - y0)
    k = (L - d) / L
    return pts[:-1] + [(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k)]


def direction_of(a, b):
    if abs(b[0] - a[0]) > abs(b[1] - a[1]):
        return 'r' if b[0] > a[0] else 'l'
    return 'd' if b[1] > a[1] else 'u'


def isotonic(targets):
    """Pool adjacent violators: the non-decreasing sequence closest to targets (least squares)."""
    blocks = []
    for t in targets:
        blocks.append([t, 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            v2, n2 = blocks.pop()
            v1, n1 = blocks.pop()
            blocks.append([(v1 * n1 + v2 * n2) / (n1 + n2), n1 + n2])
    out = []
    for v, n in blocks:
        out += [v] * n
    return out


def place_ordered(heights, desired, lo, hi, gap):
    """Centers for boxes in a fixed order, as close as possible to desired, without overlap, inside [lo, hi]."""
    off = [0.0]
    for i in range(1, len(heights)):
        off.append(off[-1] + (heights[i - 1] + heights[i]) / 2 + gap)
    q = isotonic([d - o for d, o in zip(desired, off)])
    qlo = lo + heights[0] / 2
    qhi = hi - heights[-1] / 2 - off[-1]
    if qlo > qhi + 1e-6:
        raise ValueError(f'boxes do not fit: need {off[-1] + (heights[0] + heights[-1]) / 2:.0f}, have {hi - lo:.0f}')
    q = [min(max(v, qlo), qhi) for v in q]
    return [v + o for v, o in zip(q, off)]


# ------------------------------------------------------------------------------------------------ the wiring, classified
def classify():
    """Every connection gets one place on the board. Counted from the model, asserted against its totals."""
    out = {'inside': [], 'adj': [], 'skip': [], 'ret': [], 'drv': [], 'low': [], 'lowlow': []}
    for k in sorted(LK, key=lambda x: (x[0], len(x), x)):
        l = LK[k]
        a, b = AREA_OF[l['from']], AREA_OF[l['to']]
        if a == b:
            out['inside'].append(k)
        elif a == 'X':
            out['drv'].append(k)
        elif a in CORE and b in CORE:
            ia, ib = CORE.index(a), CORE.index(b)
            if abs(ia - ib) == 1:
                out['adj'].append(k)
            elif a == 'E' and b == 'A':
                out['ret'].append(k)
            else:
                out['skip'].append(k)
        elif a in CORE or b in CORE:
            out['low'].append(k)
        else:
            out['lowlow'].append(k)
    assert sum(len(v) for v in out.values()) == len(LK) == M['generated']['counts']['connections']
    assert len(out['inside']) == 32 and len(LK) - len(out['inside']) == 86
    assert set(out['ret']) == {'L03', 'L31', 'L37'}, out['ret']
    assert all({AREA_OF[LK[k]['from']], AREA_OF[LK[k]['to']]} in ({'B', 'D'}, {'B', 'E'}) for k in out['skip'])
    return out


WIRES = classify()
COUNT = {
    'cross': len(LK) - len(WIRES['inside']), 'inside': len(WIRES['inside']), 'adj': len(WIRES['adj']),
    'skip': len(WIRES['skip']), 'ret': len(WIRES['ret']), 'drv': len(WIRES['drv']), 'low': len(WIRES['low']),
    'lowlow': len(WIRES['lowlow']),
}
COUNT['core_core'] = COUNT['adj'] + COUNT['skip'] + COUNT['ret']
COUNT['lower_all'] = COUNT['low'] + COUNT['lowlow']
INSIDE_BY_AREA = {a: [k for k in WIRES['inside'] if AREA_OF[LK[k]['from']] == a] for a in AREAS}


# ------------------------------------------------------------------------------------------------ the overview board
class Board:
    W = 1312
    XM = 52              # outer margin that carries the return line
    PADX = 14
    CODE_W = 30
    ROW_PAD = 10
    LH = 18              # map label line height

    # Row orders inside each card, chosen so the side wires run straight (see notes); the build checks crossings.
    ORDER = {
        'A': ['A1', 'A4', 'A3', 'A2', 'A5', 'A6'],
        'B': ['B1', 'B4', 'B5', 'B2', 'B6', 'B3'],
        'C': ['C1', 'C2', 'C4', 'C3', 'C5'],
        'D': ['D7', 'D3', 'D6', 'D2', 'D1', 'D4', 'D5'],
        'E': ['E1', 'E2'],
    }
    WIDTH = {'A': 214, 'B': 214, 'C': 206, 'D': 254, 'E': 168}

    def __init__(self):
        self.rows = {}       # var -> dict(card, lines, h, c)
        self.pins = {}       # (var, side) -> list of [link, partner, y]
        self.wires = {}      # link -> dict(pts, kind, arrive_dir, ...)
        self.notes = []

    # ---------------- card measurement
    def measure_cards(self):
        self.card = {}
        for a in CORE:
            w = self.WIDTH[a]
            lw = w - 2 * self.PADX - self.CODE_W
            rows = []
            for v in self.ORDER[a]:
                lines = balanced(label(v), lw, 'map')
                self.rows[v] = {'card': a, 'lines': lines, 'h': len(lines) * self.LH + self.ROW_PAD}
            self.card[a] = {'w': w, 'lw': lw}

    def side_links(self):
        """Pins on the card sides: wires to the neighbor card, and the return line at E's right and A's left."""
        pins = {}
        for k in WIRES['adj']:
            l = LK[k]
            a, b = AREA_OF[l['from']], AREA_OF[l['to']]
            fwd = CORE.index(b) > CORE.index(a)
            pins.setdefault((l['from'], 'R' if fwd else 'L'), []).append(k)
            pins.setdefault((l['to'], 'L' if fwd else 'R'), []).append(k)
        for k in WIRES['ret']:
            pins.setdefault((LK[k]['from'], 'R'), []).append(k)
            pins.setdefault((LK[k]['to'], 'L'), []).append(k)
        self.side = pins

    def partner(self, k, v):
        l = LK[k]
        return l['to'] if l['from'] == v else l['from']

    # ---------------- rows and pins
    def place_rows(self, R0, R1, iters=120):
        """Center every row so the wires to the neighbor cards run as straight as the order allows."""
        cen = {}
        for a in CORE:
            if a == 'E':
                continue
            hs = [self.rows[v]['h'] for v in self.ORDER[a]]
            room = (R1 - R0 - sum(hs)) / (len(hs) + 1)
            y = R0 + room
            for v, h in zip(self.ORDER[a], hs):
                cen[v] = y + h / 2
                y += h + room
        nb = {}
        for k in WIRES['adj']:
            l = LK[k]
            if 'E' in (AREA_OF[l['from']], AREA_OF[l['to']]):
                continue
            nb.setdefault(l['from'], []).append(l['to'])
            nb.setdefault(l['to'], []).append(l['from'])
        for it in range(iters):
            seq = ['D', 'C', 'B', 'A'] if it % 2 else ['A', 'B', 'C', 'D']
            for a in seq:
                order = self.ORDER[a]
                hs = [self.rows[v]['h'] for v in order]
                des = []
                for v in order:
                    ps = [cen[o] for o in nb.get(v, [])]
                    des.append(0.5 * cen[v] + 0.5 * (sum(ps) / len(ps)) if ps else cen[v])
                new = place_ordered(hs, des, R0, R1, 0)
                for v, c in zip(order, new):
                    cen[v] = c
        for v, c in cen.items():
            self.rows[v]['c'] = round(c)

    def bands(self, R0, R1):
        """Each row's band runs to the midpoints between its neighbors' centers."""
        for a in CORE:
            if a == 'E':
                continue
            order = self.ORDER[a]
            for i, v in enumerate(order):
                c = self.rows[v]['c']
                top = R0 if i == 0 else (self.rows[order[i - 1]]['c'] + c) / 2
                bot = R1 if i == len(order) - 1 else (self.rows[order[i + 1]]['c'] + c) / 2
                self.rows[v]['band'] = (round(top), round(bot))

    def assign_tracks(self):
        """Tracks at each pin, ordered by the far end's height, then shifted together to straighten wires."""
        self.track = {}      # (link, var) -> y
        groups = {}
        for (v, side), ks in self.side.items():
            if AREA_OF[v] == 'E':
                continue
            ks = sorted(ks, key=lambda k: (self.rows.get(self.partner(k, v), {}).get('c', 0) if AREA_OF[self.partner(k, v)] != 'E' else 0, k))
            groups[(v, side)] = ks
        self.groups = groups
        for (v, side), ks in groups.items():
            c = self.rows[v]['c']
            n = len(ks)
            for i, k in enumerate(ks):
                self.track[(k, v)] = c + (i - (n - 1) / 2) * TP
        for it in range(12):
            for (v, side), ks in groups.items():
                lo, hi = self.rows[v]['band']
                n = len(ks)
                cur = [self.track[(k, v)] for k in ks]
                smin = (lo + 7) - cur[0]
                smax = (hi - 7) - cur[-1]
                if smin > smax:
                    continue
                cands = [0.0]
                for k, y in zip(ks, cur):
                    o = self.partner(k, v)
                    if (k, o) in self.track:
                        cands.append(self.track[(k, o)] - y)
                best, bs = 0.0, None
                for s in cands:
                    s = min(max(s, smin), smax)
                    hits = sum(1 for k, y in zip(ks, cur) if (k, self.partner(k, v)) in self.track
                               and abs(self.track[(k, self.partner(k, v))] - (y + s)) < 0.6)
                    score = (hits, -abs(s))
                    if bs is None or score > bs:
                        best, bs = s, score
                for k, y in zip(ks, cur):
                    self.track[(k, v)] = y + best

    def place_e(self, R0, R1):
        """Area E's two variables become tall terminals: every wire from D plugs in at its own height."""
        e1 = [k for k in self.side.get(('E1', 'L'), [])]
        e2 = [k for k in self.side.get(('E2', 'L'), [])]
        y1 = sorted(self.track[(k, self.partner(k, 'E1'))] for k in e1)
        y2 = sorted(self.track[(k, self.partner(k, 'E2'))] for k in e2)
        assert y1[-1] < y2[0], 'E1 partners must sit above E2 partners'
        cut = round((y1[-1] + y2[0]) / 2)
        self.rows['E1']['band'] = (R0, cut)
        self.rows['E2']['band'] = (cut, R1)
        for k in e1:
            self.track[(k, 'E1')] = self.track[(k, self.partner(k, 'E1'))]
        for k in e2:
            self.track[(k, 'E2')] = self.track[(k, self.partner(k, 'E2'))]
        self.rows['E1']['c'] = (R0 + cut) / 2
        self.rows['E2']['c'] = (cut + R1) / 2
        self.e_pins = {'E1': y1, 'E2': y2}
