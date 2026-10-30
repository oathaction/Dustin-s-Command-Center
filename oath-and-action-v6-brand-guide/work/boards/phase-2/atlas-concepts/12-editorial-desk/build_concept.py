"""Build Atlas concept 12, Editorial Desk (October 30, 2026).

The system drawn the way a newspaper graphics desk would draw it: a sentence headline that states the finding, its
evidence kind as a label above it, the route the headline names in Charcoal and everything else in Stone, notes set
inside the drawing on fine leader lines, and a separate artboard for narrow screens so text keeps its size.

Every label, sign, grade, delay, count and title is read from the model export
work/boards/phase-2/maps/20261028_Maps-Model-Data.json and the shared route geometry. Headlines and decks are studio
drafts built from the model's own sentences.

Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/12-editorial-desk/build_concept.py
Writes 20261030_Concept-12-Editorial-Desk.html beside this file.
"""
import html
import importlib.util
import json
import math
import pathlib
import re

from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

M = acc.load_model()
GEO = json.loads((acc.SHARED / '20261030_Loop-Route-Geometry.json').read_text())
OUT = HERE / '20261030_Concept-12-Editorial-Desk.html'

N, L, LO, RF = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
AREA_OF = {v: a['id'] for a in M['areas'] for v in a['nodes']}
COUNTS = M['generated']['counts']
P = acc.PALETTE
WH, CH, ST, DS, RED = P['white'], P['charcoal'], P['stone'], P['deep_stone'], P['pillar_red']
MINUS = '−'
SNAP_WORDS = 'October 15, 2026'
assert M['generated']['snapshot'] == '2026-10-15'
e = lambda s: html.escape(str(s), quote=True)


# ------------------------------------------------------------------------------------------------ words from the model
def low(s):
    """Lower the first letter of a label for use mid-sentence, keeping acronyms such as AI."""
    return s[0].lower() + s[1:] if len(s) > 1 and not s[1].isupper() else s


def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def verb(p):
    return acc.SIGN_WORDS.get(p, 'decides')


def sign_words(p):
    return {'+': 'plus, the two move the same way', '-': 'minus, the two move opposite ways'}.get(p, 'no sign: an authority connection')


def delay_words(d):
    return acc.DELAYS[d]


def link_sentence(l):
    a, b = N[l['from']], N[l['to']]
    return (f"{l['id']}: {l['name']}. From {l['from']} {a['label']} to {l['to']} {b['label']}. "
            f"It {verb(l['polarity'])} it: {sign_words(l['polarity'])}. Evidence {grade_word(l['evidence']).lower()}, "
            f"{grade_gloss(l['evidence'])}. Delay {delay_words(l['delay'])}.")


def read_aloud(lid):
    """The more-and-less chain, multiplied out from the signs so it cannot drift from the model."""
    lp = LO[lid]
    d = 1
    first = low(lp['steps'][0]['from_label'])
    parts = [f'More {first}']
    for k, st in enumerate(lp['steps']):
        d *= 1 if st['polarity'] == '+' else -1
        word = 'more' if d > 0 else 'less'
        if k == len(lp['steps']) - 1:
            parts.append(f'and back to {word} {first}')
        else:
            parts.append(f'{word} {low(st["to_label"])}')
    return ', '.join(parts) + '.'


def first_sentence(text):
    m = re.match(r'(.+?[.!?])(\s|$)', text)
    return m.group(1) if m else text


def weakest_words(lid):
    lp = LO[lid]
    if lp['conceptual']:
        return 'no numbered steps to grade'
    if lp['weakest']:
        ws = lp['weakest']
        g = grade_word(L[ws[0]]['evidence'])
        if len(ws) == 1:
            return f'weakest step {ws[0]}, {g.lower()}'
        return f'weakest steps {" and ".join(ws)}, {g.lower()}'
    grades = {st['evidence'] for st in lp['steps']}
    if len(grades) == 1:
        g = grade_word(next(iter(grades))).lower()
        return f'every step {g}' if lp['n'] > 2 else f'both steps {g}'
    low_rank = min(lp['steps'], key=lambda s: s['rank'])
    return f'weakest step {low_rank["id"]}, {grade_word(low_rank["evidence"]).lower()}'


def status_line(lid):
    lp = LO[lid]
    n = len(lp['reforms'])
    ref = f'{n} reform{"s" if n != 1 else ""}' if n else 'no reform yet'
    return f'{lp["direction_word"].capitalize()} · {lp["delay_word"]} · {weakest_words(lid)} · {ref}'


def kind_line(lid):
    lp = LO[lid]
    return f'{lp["kind_word"]}, {lp["kind_gloss"]}'


DISCLOSE = {k: r['disclosure'] for k, r in GEO['routes'].items() if r.get('disclosure')}


# ------------------------------------------------------------------------------------------------ counts
def area_pairs():
    out = {}
    for l in L.values():
        a, b = AREA_OF[l['from']], AREA_OF[l['to']]
        if a != b:
            out[(a, b)] = out.get((a, b), 0) + 1
    return out


PAIRS = area_pairs()


def both(a, b):
    return PAIRS.get((a, b), 0) + PAIRS.get((b, a), 0)


def touching(aid):
    return [l for l in L.values() if AREA_OF[l['from']] == aid or AREA_OF[l['to']] == aid]


C_LINKS = touching('C')
C_INSIDE = [l for l in C_LINKS if AREA_OF[l['from']] == 'C' and AREA_OF[l['to']] == 'C']
C_IN = [l for l in C_LINKS if AREA_OF[l['to']] == 'C' and AREA_OF[l['from']] != 'C']
C_OUT = [l for l in C_LINKS if AREA_OF[l['from']] == 'C' and AREA_OF[l['to']] != 'C']
assert (len(C_LINKS), len(C_INSIDE), len(C_IN), len(C_OUT)) == (20, 5, 8, 7)
LOOPS_C = next(g for g in M['groups'] if g['id'] == 'C')['loops']
LOOPS_THROUGH_C = [k for k in M['loop_order'] if any(s['area'] == 'C' for s in LO[k]['stations'] if s['is_variable'])]
N_R = sum(1 for l in LO.values() if l['type'] == 'R')
N_B = sum(1 for l in LO.values() if l['type'] == 'B')
N_WITH_REFORM = sum(1 for l in LO.values() if l['reforms'])
X_LINKS = [l for l in L.values() if AREA_OF[l['from']] == 'X']
X_TO = {}
for l in X_LINKS:
    X_TO[AREA_OF[l['to']]] = X_TO.get(AREA_OF[l['to']], 0) + 1
ECON = ('production', 'household', 'money')
ECON_VARS = sum(len(AREAS[a]['nodes']) for a in ECON)
ECON_LINKS = [l for l in L.values() if (AREA_OF[l['from']] in ECON) or (AREA_OF[l['to']] in ECON)]
ECON_WITH_A = [l for l in ECON_LINKS if 'A' in (AREA_OF[l['from']], AREA_OF[l['to']])]
TECH_LINKS = [l for l in L.values() if 'TC' in (AREA_OF[l['from']], AREA_OF[l['to']])]
TECH_WITH_D = [l for l in TECH_LINKS if 'D' in (AREA_OF[l['from']], AREA_OF[l['to']])]
assert len(X_LINKS) == 15 and len(ECON_LINKS) == 32 and len(TECH_LINKS) == 18


def cnt(key, n):
    return f'<span data-count="{e(key)}">{n}</span>'


# ------------------------------------------------------------------------------------------------ text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False, track=0.0):
    """Approximate rendered width. Inter Tight runs about 5 percent narrower than Inter."""
    w = _font(weight).getlength(text) * size / 200
    if tight:
        w *= 0.95
    return w + track * size * max(len(text) - 1, 0)


def wrap(text, width, size, weight=400, tight=False):
    out, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if line and tw(trial, size, weight, tight) > width:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


# Text styles inside drawings, from the design frame memo's type scale (section 2)
STY = {
    'station': (20, 700, True, 24),     # Station label, Inter Tight 700 20/22
    'map': (15, 600, False, 18),        # Map label, Inter 600 15/18
    'cap': (14, 400, False, 20),        # Caption, Inter 400 14/20
    'note': (15, 400, False, 21),       # Panel text, Inter 400 15, notes in the drawing
    'notehead': (15, 600, False, 21),   # Map label weight for a note's lead words
    'fig': (40, 800, True, 40),         # Figure, Inter Tight 800 40/40
    'head': (22, 800, True, 26),        # Panel head, Inter Tight 800 22/26
    'small': (13, 400, False, 16),      # Note, Inter 400 13/16
    'eyebrow': (13, 700, False, 18),    # Eyebrow
}


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def text(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{e(s)}</text>'


def lines(x, y, rows, cls, lh, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    spans = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{spans}</text>'


# ------------------------------------------------------------------------------------------------ line machinery
ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 2)}   # body, point, height, sign length, bar


def unit(dx, dy):
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def pattern(tex, w):
    if tex == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if tex == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if tex == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def fitted(tex, w, length):
    """Stretch the pattern a little so the line starts and ends on ink (design frame memo, rule 3.2)."""
    arr, cap = pattern(tex, w)
    if arr is None:
        return '', cap
    if tex == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.2f}', cap
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.2f}' for x in arr), cap


def tex_of(grade):
    return acc.GRADES[grade][2] if grade in acc.GRADES else 'solid'


def tag_shape(cx, cy, ux, uy, sign, w, cls):
    a, p, h, sl, sb = TAG[w]
    Lt = a + p
    vx, vy = -uy, ux
    x0, y0 = cx - ux * Lt / 2, cy - uy * Lt / 2
    pts = [(0, -h / 2), (a, -h / 2), (Lt, 0), (a, h / 2), (0, h / 2)]
    poly = ' '.join(f'{f(x0 + ux * s + vx * t)},{f(y0 + uy * s + vy * t)}' for s, t in pts)
    bx, by = x0 + ux * a / 2, y0 + uy * a / 2
    glyph = f'<rect class="sg" x="{f(bx - sl / 2)}" y="{f(by - sb / 2)}" width="{sl}" height="{sb}"/>'
    if sign == '+':
        glyph += f'<rect class="sg" x="{f(bx - sb / 2)}" y="{f(by - sl / 2)}" width="{sb}" height="{sl}"/>'
    return f'<g class="tag {cls}"><polygon points="{poly}"/>{glyph}</g>'


def head_shape(tx, ty, ux, uy, w, cls):
    al, ab = ARROW[w]
    bx, by = tx - ux * al, ty - uy * al
    vx, vy = -uy, ux
    return (f'<path class="ak-head {cls}" d="M{f(bx + vx * ab / 2)} {f(by + vy * ab / 2)}L{f(tx)} {f(ty)}'
            f'L{f(bx - vx * ab / 2)} {f(by - vy * ab / 2)}Z"/>')


def tick_marks(x, y, ux, uy, count, w, cls):
    vx, vy = -uy, ux
    half = w / 2 + 4
    out = []
    for i in range(count):
        cx, cy = x + ux * (12 + i * 5), y + uy * (12 + i * 5)
        out.append(f'<path class="tick {cls}" d="M{f(cx - vx * half)} {f(cy - vy * half)}L{f(cx + vx * half)} {f(cy + vy * half)}"/>')
    return ''.join(out)


def pill_edge(ux, uy, w, h):
    """Distance from a pill's center to its outline along a direction."""
    r = h / 2

    def inside(px, py):
        ax = abs(px) - (w / 2 - r)
        if ax <= 0:
            return abs(py) <= r
        return ax * ax + py * py <= r * r
    lo, hi = 0.0, max(w, h)
    for _ in range(40):
        mid = (lo + hi) / 2
        if inside(ux * mid, uy * mid):
            lo = mid
        else:
            hi = mid
    return lo


def path_len(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def point_at(pts, s):
    for i in range(len(pts) - 1):
        d = math.dist(pts[i], pts[i + 1])
        if s <= d or i == len(pts) - 2:
            t = 0 if d == 0 else min(1.0, s / d)
            ux, uy = unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t), (ux, uy)
        s -= d
    return pts[-1], (1, 0)


def rounded_d(pts, r):
    if len(pts) == 2 or r <= 0:
        return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        u0 = unit(p1[0] - p0[0], p1[1] - p0[1])
        u1 = unit(p2[0] - p1[0], p2[1] - p1[1])
        rr = min(r, math.dist(p0, p1) / 2, math.dist(p1, p2) / 2)
        a = (p1[0] - u0[0] * rr, p1[1] - u0[1] * rr)
        b = (p1[0] + u1[0] * rr, p1[1] + u1[1] * rr)
        d += f'L{f(a[0])} {f(a[1])}Q{f(p1[0])} {f(p1[1])} {f(b[0])} {f(b[1])}'
    d += f'L{f(pts[-1][0])} {f(pts[-1][1])}'
    return d


BEND = {2: 8, 3: 12, 6: 18}


def wire(lid, pts, w=3, ctx=False, tag_at=0.5, interactive=True, label='', rel=None, at=None, sign_size=None):
    """One V7 connection: line in its evidence texture, delay ticks after the tail, the pointing tag carrying the
    sign, an arrowhead at the tip, and an invisible hit stroke. pts run from the tail to the tip.
    Each mark is drawn at its base weight and at the lit weight (6 px); CSS shows one or the other."""
    l = L[lid]
    tex = tex_of(l['evidence'])
    ux, uy = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    al = ARROW[w][0]
    body = list(pts[:-1]) + [(pts[-1][0] - ux * al, pts[-1][1] - uy * al)]
    if tex == 'dotted':
        body[-1] = (body[-1][0] - ux * 1.5 * w, body[-1][1] - uy * 1.5 * w)
    length = path_len(body)
    das = {}
    for ww in (2, 3, 6):
        da, cap = fitted(tex, ww, length)
        das[ww] = da
    cap = pattern(tex, w)[1]
    d = rounded_d(body, BEND[w])
    style = ''.join(f'--d{ww}:{das[ww]};' for ww in (2, 3, 6) if das[ww])
    dash = f' stroke-dasharray="{das[w]}"' if das[w] else ''
    st = f' style="{style}"' if style else ''
    marks = (f'<path class="ak-case" d="{d}" fill="none"{dash}/>'
             f'<path class="ak-mark" d="{d}" fill="none" stroke-width="{w}" stroke-linecap="{cap}"{dash}{st}/>')
    # ticks: one per delay band, 12 px after the tail
    t0, tu = point_at(pts, 0)
    n_ticks = {'S': 1, 'M': 2, 'L': 3}[l['delay']]
    ticks = tick_marks(t0[0], t0[1], tu[0], tu[1], n_ticks, w, 'sz-lo') + tick_marks(t0[0], t0[1], tu[0], tu[1], n_ticks, 6, 'sz-hi')
    heads = head_shape(pts[-1][0], pts[-1][1], ux, uy, w, 'sz-lo') + head_shape(pts[-1][0], pts[-1][1], ux, uy, 6, 'sz-hi')
    tags = ''
    if l['polarity'] in ('+', '-'):
        (cx, cy), (gx, gy) = point_at(body, length * tag_at)
        tags = tag_shape(cx, cy, gx, gy, l['polarity'], sign_size or w, 'sz-lo') + tag_shape(cx, cy, gx, gy, l['polarity'], 6, 'sz-hi')
    hit = f'<path class="ak-hit" d="{rounded_d(pts, 0)}"/>' if interactive else ''
    say = link_sentence(l)
    common = (f'data-link="{lid}" data-sign="{sign_attr(l["polarity"])}" data-grade="{l["evidence"]}" '
              f'data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}"')
    cls = 'wire ctx' if ctx else 'wire'
    if interactive:
        rel = rel if rel is not None else f'var-{l["from"].lower()} var-{l["to"].lower()}'
        return (f'<g class="{cls}" role="button" data-select="link-{lid.lower()}" {common} data-rel="{rel}" '
                f'aria-label="{e(say)}" data-say="{e(say)}">{marks}{ticks}{tags}{heads}{hit}{label}</g>')
    return f'<g class="{cls}" {common}>{marks}{ticks}{tags}{heads}{label}</g>'


def edge_pts(a, b, wa=56, ha=30, wb=56, hb=30, gap_a=2, gap_b=2, mid=None):
    """Tail and tip points between two pills centered at a and b, 2 px off each outline."""
    path = [a] + (mid or []) + [b]
    u0 = unit(path[1][0] - a[0], path[1][1] - a[1])
    u1 = unit(b[0] - path[-2][0], b[1] - path[-2][1])
    da = pill_edge(u0[0], u0[1], wa, ha) + gap_a if wa else gap_a
    db = pill_edge(u1[0], u1[1], wb, hb) + gap_b if wb else gap_b
    p0 = (a[0] + u0[0] * da, a[1] + u0[1] * da)
    p1 = (b[0] - u1[0] * db, b[1] - u1[1] * db)
    return [p0] + (mid or []) + [p1]


def leader(pts, cls='leader'):
    return f'<path class="{cls}" d="{rounded_d(pts, 0)}"/>'


# ------------------------------------------------------------------------------------------------ route thumbnails
PLAN = GEO['plan']
FRAME = PLAN['frame']
TMARK = {'w': 2.0, 'station': 3.6, 'start': 5.2, 'tag_body': 9.0, 'tag_point': 4.5, 'tag_h': 10.0, 'arm': 2.8,
         'sign_w': 1.7, 'bar': 5.0}


def arc_points(arc, n=72):
    cx, cy = arc['center']
    a, b = arc['from'], arc['to']
    ta = math.atan2(a[1] - cy, a[0] - cx)
    tb = math.atan2(b[1] - cy, b[0] - cx)
    tp = math.atan2(arc['apex'][1] - cy, arc['apex'][0] - cx)

    def norm(t):
        while t < 0:
            t += 2 * math.pi
        while t >= 2 * math.pi:
            t -= 2 * math.pi
        return t
    span_ccw = norm(tb - ta)
    through = norm(tp - ta) <= span_ccw
    span = span_ccw if through else -(2 * math.pi - span_ccw)
    R = arc['radius']
    return [(cx + R * math.cos(ta + span * i / n), cy + R * math.sin(ta + span * i / n)) for i in range(n + 1)]


def _cum(pts):
    out = [0.0]
    for i in range(1, len(pts)):
        out.append(out[-1] + math.dist(pts[i - 1], pts[i]))
    return out


def _at(pts, cum, s):
    s = max(0.0, min(cum[-1], s))
    for i in range(1, len(pts)):
        if cum[i] >= s:
            t = (s - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            x = pts[i - 1][0] + t * (pts[i][0] - pts[i - 1][0])
            y = pts[i - 1][1] + t * (pts[i][1] - pts[i - 1][1])
            return (x, y), unit(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
    return pts[-1], (1, 0)


def thumb(lid, width=310, uid='', hilite_area=None, plan_only=False, route_cls='rt'):
    """A loop drawn as its own route across the shared plan (DR-15), in this concept's idiom: square hairline areas,
    every variable a Stone dot, the route in Charcoal with the V7 line code and pointing tags."""
    rt = GEO['routes'][lid] if lid else None
    k = width / FRAME['w']
    H = FRAME['h'] * k

    def X(p):
        return ((p[0] - FRAME['x0']) * k, (p[1] - FRAME['y0']) * k)
    out = []
    visited = {s['area'] for s in rt['stations'] if s['on_plan']} if rt else set()
    if hilite_area:
        visited = {hilite_area}
    for a, (x0, y0, x1, y1) in PLAN['boxes'].items():
        p0, p1 = X((x0, y0)), X((x1, y1))
        cls = 'pb on' if a in visited else 'pb'
        loc = f' data-locate="area-{a.lower()}"' if plan_only else ''
        out.append(f'<rect class="{cls}"{loc} x="{f(p0[0] + .5)}" y="{f(p0[1] + .5)}" width="{f(p1[0] - p0[0] - 1)}" height="{f(p1[1] - p0[1] - 1)}"/>')
    for v, pos in PLAN['variables'].items():
        x, y = X((pos['x'], pos['y']))
        out.append(f'<circle class="pd" cx="{f(x)}" cy="{f(y)}" r="1.6"/>')
    if plan_only or not rt:
        return ''.join(out), width, H
    ink = []
    st_px = [X(s['pos']) for s in rt['stations']]
    n = len(st_px)
    rad = [TMARK['start'] if i == 0 else TMARK['station'] for i in range(n)]
    for s in rt['steps']:
        i = s['index'] - 1
        b_i = (i + 1) % n
        pts = [X(p) for p in arc_points(s['arc'])]
        cum = _cum(pts)
        s0 = rad[i] + 1.0
        s1 = cum[-1]
        for j in range(len(pts) - 1, -1, -1):
            if math.dist(pts[j], st_px[b_i]) >= rad[b_i] + 1.0:
                s1 = cum[j]
                break
        tb, tp = TMARK['tag_body'], TMARK['tag_point']
        Lt = tb + tp
        line_end = s1 - tb * 0.5
        a0, _ = _at(pts, cum, s0)
        a1, _ = _at(pts, cum, line_end)
        R = s['arc']['radius'] * k
        d = f'M{f(a0[0])} {f(a0[1])}A{f(R)} {f(R)} 0 0 {s["arc"]["sweep"]} {f(a1[0])} {f(a1[1])}'
        if s['sketch']:
            attrs = f'data-step="{s["index"]}" data-grade="sketch"'
            ink.append(f'<g class="st" {attrs}><path class="rl" d="{d}" stroke-width="3.6"/><path class="rh" d="{d}" stroke-width="1.6"/>')
        else:
            attrs = (f'data-link="{s["id"]}" data-sign="{sign_attr(s["polarity"])}" data-grade="{s["evidence"]}" '
                     f'data-delay="{s["delay"]}" data-from="{s["from"]}" data-to="{s["to"]}"')
            da, cap = fitted(tex_of(s['evidence']), TMARK['w'], line_end - s0)
            dash = f' stroke-dasharray="{da}" stroke-linecap="{cap}"' if da else ''
            ink.append(f'<g class="st" {attrs}><path class="rl" d="{d}" stroke-width="{TMARK["w"]}"{dash}/>')
        bp, _ = _at(pts, cum, s1 - Lt)
        tpnt, _ = _at(pts, cum, s1)
        ux, uy = unit(tpnt[0] - bp[0], tpnt[1] - bp[1])
        vx, vy = -uy, ux
        th = TMARK['tag_h'] / 2
        poly = ' '.join(f'{f(bp[0] + ux * a + vx * b)},{f(bp[1] + uy * a + vy * b)}'
                        for a, b in [(0, -th), (tb, -th), (Lt, 0), (tb, th), (0, th)])
        gx, gy = bp[0] + ux * tb / 2, bp[1] + uy * tb / 2
        arm = TMARK['arm']
        glyph = f'M{f(gx - arm)} {f(gy)}H{f(gx + arm)}'
        if s['polarity'] == '+':
            glyph += f'M{f(gx)} {f(gy - arm)}V{f(gy + arm)}'
        ink.append(f'<polygon class="tt" points="{poly}"/><path class="tg" d="{glyph}" stroke-width="{TMARK["sign_w"]}"/>')
        if s['closing']:
            cp, ct = _at(pts, cum, s1 - Lt - 3.0)
            bx, by = -ct[1], ct[0]
            L2 = TMARK['bar']
            ink.append(f'<path class="cb" d="M{f(cp[0] + bx * L2)} {f(cp[1] + by * L2)}L{f(cp[0] - bx * L2)} {f(cp[1] - by * L2)}"/>')
        ink.append('</g>')
    for i, s in enumerate(rt['stations']):
        x, y = st_px[i]
        node = f' data-node="{s["code"]}"' if s['code'] else ''
        if i == 0:
            fill = 'so' if s['on_plan'] else 'so off'
            ink.append(f'<g class="{fill}"{node}><circle cx="{f(x)}" cy="{f(y)}" r="{rad[0]}"/><circle class="sc" cx="{f(x)}" cy="{f(y)}" r="2"/></g>')
        elif not s['on_plan']:
            ink.append(f'<circle class="sx"{node} cx="{f(x)}" cy="{f(y)}" r="{TMARK["station"] + .3}"/>')
        else:
            ink.append(f'<circle class="ss"{node} cx="{f(x)}" cy="{f(y)}" r="{TMARK["station"]}"/>')
    out.append(f'<g class="{route_cls}">' + ''.join(ink) + '</g>')
    return ''.join(out), width, H


def thumb_svg(lid, width=310, view='loop-route', cls='th', label=None):
    body, w, h = thumb(lid, width)
    lp = LO[lid]
    steps = 'sketch' if lp['conceptual'] else ' '.join(s['id'] for s in lp['steps'])
    aria = f' role="img" aria-label="{e(label)}"' if label else ' aria-hidden="true"'
    return (f'<svg class="{cls}" data-view="{view}" data-loop="{lid}" data-steps="{steps}" viewBox="0 0 {f(w)} {f(h)}" '
            f'width="{f(w)}" height="{f(h)}"{aria} focusable="false">{body}</svg>')


def locator_svg(lid=None, area=None):
    """The kit's locator: a small copy of the overview plan, the current area or loop in heavy ink. Never red."""
    width = 132
    if lid:
        body, w, h = thumb(lid, width)
    else:
        body, w, h = thumb(None, width, plan_only=True)
    return f'<svg class="loc-svg" viewBox="0 0 {f(w)} {f(h)}" width="{f(w)}" height="{f(h)}" aria-hidden="true" focusable="false">{body}</svg>'


# ------------------------------------------------------------------------------------------------ identity
def wordmark(height, master):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    src = src.replace('<svg ', f'<svg width="{w:.0f}" height="{height}" role="img" aria-label="Oath &amp; Action" ', 1)
    return src, w


# ------------------------------------------------------------------------------------------------ chips
def chip(word, code, compact=False):
    c = ' compact' if compact else ''
    return f'<span class="chip{c}"><span class="k">{e(word)}</span><span class="c">{e(code)}</span></span>'


# ------------------------------------------------------------------------------------------------ route on any mapping
def route_marks(lid, X, w=2.0, tagsz=None):
    """A loop's route through a point mapper X(plan point) -> px, sampled so non-uniform stretches still read.
    Thumbnail grammar: line code, pointing tag at the arrival end, closing bar, start ring."""
    rt = GEO['routes'][lid]
    tm = dict(TMARK, **(tagsz or {}))
    st_px = [X(s['pos']) for s in rt['stations']]
    n = len(st_px)
    rad = [tm['start'] if i == 0 else tm['station'] for i in range(n)]
    out = []
    for s in rt['steps']:
        i = s['index'] - 1
        b_i = (i + 1) % n
        pts = [X(p) for p in arc_points(s['arc'])]
        cum = _cum(pts)
        s0 = rad[i] + 1.5
        s1 = cum[-1]
        for j in range(len(pts) - 1, -1, -1):
            if math.dist(pts[j], st_px[b_i]) >= rad[b_i] + 1.5:
                s1 = cum[j]
                break
        tb, tp = tm['tag_body'], tm['tag_point']
        Lt = tb + tp
        line_end = s1 - tb * 0.5
        sub = [p for p, c in zip(pts, cum) if s0 <= c <= line_end]
        a0, _ = _at(pts, cum, s0)
        a1, _ = _at(pts, cum, line_end)
        poly = [a0] + sub + [a1]
        d = 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in poly)
        attrs = (f'data-link="{s["id"]}" data-sign="{sign_attr(s["polarity"])}" data-grade="{s["evidence"]}" '
                 f'data-delay="{s["delay"]}" data-from="{s["from"]}" data-to="{s["to"]}"')
        da, cap = fitted(tex_of(s['evidence']), w, line_end - s0)
        dash = f' stroke-dasharray="{da}" stroke-linecap="{cap}"' if da else ''
        g = [f'<g class="st" {attrs}><path class="rl" d="{d}" stroke-width="{w}"{dash}/>']
        bp, _ = _at(pts, cum, s1 - Lt)
        tpnt, _ = _at(pts, cum, s1)
        ux, uy = unit(tpnt[0] - bp[0], tpnt[1] - bp[1])
        vx, vy = -uy, ux
        th = tm['tag_h'] / 2
        poly_t = ' '.join(f'{f(bp[0] + ux * a + vx * b)},{f(bp[1] + uy * a + vy * b)}'
                          for a, b in [(0, -th), (tb, -th), (Lt, 0), (tb, th), (0, th)])
        gx, gy = bp[0] + ux * tb / 2, bp[1] + uy * tb / 2
        arm = tm['arm']
        glyph = f'M{f(gx - arm)} {f(gy)}H{f(gx + arm)}'
        if s['polarity'] == '+':
            glyph += f'M{f(gx)} {f(gy - arm)}V{f(gy + arm)}'
        g.append(f'<polygon class="tt" points="{poly_t}"/><path class="tg" d="{glyph}" stroke-width="{tm["sign_w"]}"/>')
        if s['closing']:
            cp, ct = _at(pts, cum, s1 - Lt - 3.0)
            bx, by = -ct[1], ct[0]
            g.append(f'<path class="cb" d="M{f(cp[0] + bx * tm["bar"])} {f(cp[1] + by * tm["bar"])}'
                     f'L{f(cp[0] - bx * tm["bar"])} {f(cp[1] - by * tm["bar"])}"/>')
        g.append('</g>')
        out.append(''.join(g))
    for i, s in enumerate(rt['stations']):
        x, y = st_px[i]
        if i == 0:
            out.append(f'<g class="so" data-node="{s["code"]}"><circle cx="{f(x)}" cy="{f(y)}" r="{rad[0]}"/><circle class="sc" cx="{f(x)}" cy="{f(y)}" r="2"/></g>')
        else:
            out.append(f'<circle class="ss" data-node="{s["code"]}" cx="{f(x)}" cy="{f(y)}" r="{tm["station"]}"/>')
    return ''.join(out)


# ------------------------------------------------------------------------------------------------ overview, wide artboard
OVW = 1312


class Block:
    """An area drawn as a square-cornered block; maps plan slots into it."""

    def __init__(self, aid, x, y, w, h, rows):
        self.aid, self.x, self.y, self.w, self.h, self.rows = aid, x, y, w, h, rows
        self.box = PLAN['boxes'][aid]

    def slot(self, p):
        x0, y0, x1, y1 = self.box
        px = self.x + (p[0] - x0) / (x1 - x0) * self.w
        rows = self.plan_rows()
        if len(rows) == 1:
            return (px, self.y + self.rows[0])
        # piecewise linear between slot rows, extended past the ends, so an arc keeps its curve
        for k in range(len(rows) - 1):
            if p[1] <= rows[k + 1] or k == len(rows) - 2:
                t = (p[1] - rows[k]) / (rows[k + 1] - rows[k])
                return (px, self.y + self.rows[k] + t * (self.rows[k + 1] - self.rows[k]))

    def plan_rows(self):
        slots = PLAN['slots'][self.aid]
        return sorted({round(s[1], 2) for s in slots})


def overview_wide():
    PW, g = 755, 52
    bw = (PW - 2 * g) / 3
    xs = [0, bw + g, 2 * (bw + g)]
    XH = 46
    top, TH = XH + 26, 150
    bot, BH = top + TH + 50, 104
    gtop = bot + BH + 24
    blocks = {
        'A': Block('A', xs[0], top, bw, TH, [60, 91, 122]),
        'B': Block('B', xs[1], top, bw, TH, [60, 91, 122]),
        'C': Block('C', xs[2], top, bw, TH, [60, 91, 122]),
        'E': Block('E', xs[0], bot, bw, BH, [56, 82]),
        'D': Block('D', xs[1], bot, PW - xs[1], BH, [56, 82]),
    }
    out = []
    # X band: one sentence
    xa = AREAS['X']
    xsent = (f'{cnt("variables_X", len(xa["nodes"]))} conditions the model treats as given send '
             f'{cnt("custom:outside-driver-connections", len(X_LINKS))} connections into the system, '
             f'{X_TO.get("A", 0)} of them into A and {X_TO.get("B", 0)} into B.')
    out.append(
        f'<g class="blk tier" role="button" data-select="area-x" aria-label="{e("Area X, " + xa["title"] + ". " + xa["text"])}" '
        f'data-say="{e("Area X, " + xa["title"] + ". " + xa["text"])}">'
        f'<rect class="ak-mark" x=".5" y=".5" width="{f(PW - 1)}" height="{XH - 1}" stroke-width="1"/>'
        f'<text x="14" y="28" class="s-map ak-label">{e(xa["title"])}</text>'
        f'<text x="{f(14 + tw(xa["title"], 15, 600) + 14)}" y="28" class="s-cap s-dim">{xsent}</text></g>')
    # core blocks
    for aid in ['A', 'B', 'C', 'E', 'D']:
        b = blocks[aid]
        a = AREAS[aid]
        name = f'Area {aid}, {a["title"]}. {a["text"]} {len(a["nodes"])} variables.'
        dots = ''.join(f'<circle class="dot" cx="{f(b.slot((PLAN["variables"][v]["x"], PLAN["variables"][v]["y"]))[0])}" '
                       f'cy="{f(b.slot((PLAN["variables"][v]["x"], PLAN["variables"][v]["y"]))[1])}" r="3.5"/>'
                       for v in a['nodes'])
        head = (f'<text x="{f(b.x + 14)}" y="{f(b.y + 30)}" class="s-head ak-label"><tspan class="lt">{aid}</tspan>'
                f'<tspan dx="8">{e(a["title"])}</tspan></text>')
        rect = f'<rect class="ak-mark" x="{f(b.x + .5)}" y="{f(b.y + .5)}" width="{f(b.w - 1)}" height="{f(b.h - 1)}" stroke-width="1"/>'
        if aid == 'C':
            rect = f'<rect class="ak-mark cblk" x="{f(b.x + 1)}" y="{f(b.y + 1)}" width="{f(b.w - 2)}" height="{f(b.h - 2)}" stroke-width="2"/>'
            route = route_marks('R10', lambda p, b=b: b.slot(p), w=2.0)
            out.append(f'<a class="blk cl" href="#area-c" aria-label="{e(name)} Opens the close-up." data-say="{e(name)} Opens the close-up.">'
                       f'{rect}{head}{dots}<g class="rt ov">{route}</g></a>')
        else:
            out.append(f'<g class="blk" role="button" data-select="area-{aid.lower()}" aria-label="{e(name)}" data-say="{e(name)}">'
                       f'{rect}{head}{dots}</g>')
    # ring counts: the seven core pairs, printed as numbers; arrowheads show which way the connections run
    def bundle(p0, p1, a, b, nx, ny, anchor='middle'):
        ab, ba = PAIRS.get((a, b), 0), PAIRS.get((b, a), 0)
        ux, uy = unit(p1[0] - p0[0], p1[1] - p0[1])
        q0, q1 = list(p0), list(p1)
        heads = ''
        if ab:
            heads += head_shape(p1[0], p1[1], ux, uy, 2, '')
            q1 = [p1[0] - ux * 10, p1[1] - uy * 10]
        if ba:
            heads += head_shape(p0[0], p0[1], -ux, -uy, 2, '')
            q0 = [p0[0] + ux * 10, p0[1] + uy * 10]
        tot = ab + ba
        say = f'{tot} connections between area {a} and area {b}: {ab} from {a} to {b}, {ba} from {b} to {a}.'
        return (f'<g class="bun" aria-hidden="true"><path class="bl" d="M{f(q0[0])} {f(q0[1])}L{f(q1[0])} {f(q1[1])}"/>{heads}'
                f'<text class="s-fig" x="{f(nx)}" y="{f(ny)}" text-anchor="{anchor}"><tspan data-count="custom:pair-{a}-{b}">{tot}</tspan></text></g>'), say
    A_, B_, C_, D_, E_ = (blocks[k] for k in 'ABCDE')
    mid_t = top + TH / 2 + 8
    mid_b = bot + BH / 2 + 8
    bund = []
    bund.append(bundle((A_.x + bw + 2, mid_t), (B_.x - 2, mid_t), 'A', 'B', A_.x + bw + g / 2, mid_t - 12))
    bund.append(bundle((B_.x + bw + 2, mid_t), (C_.x - 2, mid_t), 'B', 'C', B_.x + bw + g / 2, mid_t - 12))
    bund.append(bundle((E_.x + bw + 2, mid_b), (D_.x - 2, mid_b), 'E', 'D', E_.x + bw + g / 2, mid_b - 12))
    vy0, vy1 = top + TH + 2, bot - 2
    cx_a, cx_b, cx_c = A_.x + bw / 2, B_.x + bw / 2, C_.x + bw / 2
    bund.append(bundle((cx_a, vy0), (cx_a, vy1), 'A', 'E', cx_a + 12, (vy0 + vy1) / 2 + 14, 'start'))
    bund.append(bundle((cx_b, vy0), (cx_b, vy1), 'B', 'D', cx_b + 12, (vy0 + vy1) / 2 + 14, 'start'))
    bund.append(bundle((cx_c, vy0), (cx_c, vy1), 'C', 'D', cx_c + 12, (vy0 + vy1) / 2 + 14, 'start'))
    dy = vy1 - vy0
    bund.append(bundle((B_.x + 8, vy0), (B_.x + 8 - dy, vy1), 'B', 'E', B_.x - dy / 2 - 10, (vy0 + vy1) / 2 + 14, 'end'))
    out.extend(b[0] for b in bund)
    ring_words = [b[1] for b in bund]
    # outer tiers below: four boxes with titles, then one sentence per layer
    gh = 50
    gb = {}
    for aid in ('money', 'household', 'production', 'TC'):
        x0, _, x1, _ = PLAN['boxes'][aid]
        bx0, bx1 = x0 / 6.6 * PW, x1 / 6.6 * PW
        gb[aid] = (bx0, bx1)
        a = AREAS[aid]
        rows = wrap(a['title'], bx1 - bx0 - 20, 14, 400)
        name = f'{a["title"]}. {a["text"]} {len(a["nodes"])} variables.'
        out.append(f'<g class="blk tier" role="button" data-select="area-{aid.lower()}" aria-label="{e(name)}" data-say="{e(name)}">'
                   f'<rect class="ak-mark" x="{f(bx0 + .5)}" y="{f(gtop + .5)}" width="{f(bx1 - bx0 - 1)}" height="{gh - 1}" stroke-width="1"/>'
                   + lines(bx0 + 10, gtop + 21 if len(rows) > 1 else gtop + 30, rows, 's-cap ak-label', 18) + '</g>')
    econ = (f'Three economy areas hold {cnt("custom:economy-variables", ECON_VARS)} conditions. '
            f'{len(ECON_LINKS)} connections touch them, {len(ECON_WITH_A)} of them with A.')
    tech = (f'{cnt("variables_TC", len(AREAS["TC"]["nodes"]))} technology conditions. '
            f'{len(TECH_LINKS)} connections touch them, {len(TECH_WITH_D)} of them with D.')
    ey = gtop + gh + 22
    ew = gb['production'][1] - gb['money'][0]
    out.append(lines(0, ey, wrap(re.sub('<[^>]+>', '', econ), ew, 14, 400), 's-cap s-dim', 20))
    out.append(lines(gb['TC'][0], ey, wrap(re.sub('<[^>]+>', '', tech), gb['TC'][1] - gb['TC'][0], 14, 400), 's-cap s-dim', 20))
    H = ey + 2 * 20 + 6
    # the inset: area C magnified, R10 in Charcoal
    ix, iw = 779, OVW - 779
    out.append(f'<path class="zoom" d="M{f(PW)} {f(top + 1)}L{ix} 1M{f(PW)} {f(top + TH - 1)}L{ix} {f(H - 1)}"/>')
    out.append(f'<rect class="inset" x="{ix + .5}" y=".5" width="{f(iw - 1)}" height="{f(H - 1)}"/>')
    out.append(inset_r10(ix, 0, iw, H))
    svg = (f'<svg class="art art-wide" data-view="overview" viewBox="0 0 {OVW} {f(H)}" role="group" '
           f'aria-labelledby="h-overview" data-ak-roving data-ak-nav="spatial">{"".join(out)}</svg>')
    return svg, ring_words


def inset_r10(ox, oy, w, h):
    """Area C at reading size: the four stations of R10 on their plan slots, spaced so the diagonals run at 45
    degrees. R10's steps in Charcoal at 3 px, the fifth variable and its link in Stone."""
    lp = LO['R10']
    S = 132
    x0, y0 = ox + 196, oy + 146
    pos = {'C2': (x0, y0), 'C3': (x0, y0 + S), 'C1': (x0 + S, y0 + S), 'C4': (x0 + S, y0 + 2 * S), 'C5': (x0, y0 + 2 * S)}
    out = []
    out.append(text(ox + 24, oy + 34, 'Inside area C, Electoral competition', 's-eye'))
    title_rows = wrap(lp['title'], w - 48, 22, 800, True)
    out.append(lines(ox + 24, oy + 64, title_rows, 's-head', 26, extra=f' data-loop="R10" data-name="{e(lp["title"])}"'))
    R = 9
    for st in lp['steps'] + [{'id': 'L24', 'from': 'C3', 'to': 'C5'}]:
        a, b = pos[st['from']], pos[st['to']]
        pts = edge_pts(a, b, 2 * R, 2 * R, 2 * R, 2 * R, 3, 3)
        out.append(wire(st['id'], pts, w=3 if st['id'] != 'L24' else 2, ctx=st['id'] == 'L24', interactive=False))
    for v, (x, y) in pos.items():
        ctx = ' ctx' if v == 'C5' else ''
        out.append(f'<circle class="st-dot{ctx}" cx="{f(x)}" cy="{f(y)}" r="{R}"/>')
    lab = {
        'C2': (x0 + 20, y0 + 6, 'start'), 'C1': (x0 + S + 20, y0 + S + 6, 'start'),
        'C3': (x0 - 20, y0 + S + 6, 'end'), 'C5': (x0 - 20, y0 + 2 * S + 6, 'end'),
    }
    for v, (x, y, anc) in lab.items():
        cls = 's-map' + (' s-dim' if v == 'C5' else '')
        out.append(f'<text x="{f(x)}" y="{f(y)}" class="{cls}" text-anchor="{anc}" data-node="{v}" data-name="{e(N[v]["label"])}">{e(N[v]["label"])}</text>')
    c4rows = wrap(N['C4']['label'], 150, 15, 600)
    out.append(lines(x0 + S + 20, y0 + 2 * S + 6 - (len(c4rows) - 1) * 9, c4rows, 's-map',
                     18, extra=f' data-node="C4" data-name="{e(N["C4"]["label"])}"'))
    # notes on leader lines
    l08, l25, l53 = L['L08'], L['L25'], L['L53']
    n1 = wrap(f'Safe seats make the primary decisive, and decisive primaries reduce general-election pressure.', 168, 15)
    nx, ny = x0 + S + 6, y0 + 22
    out.append(lines(nx + 10, ny, n1, 's-note', 21))
    out.append(leader([(nx + 4, ny - 5), (nx - 26, ny - 5 + 0), (x0 + S * 0.55 + 4, y0 + S * 0.55 - 4)]))
    n2 = wrap(f'The weakest step, graded {grade_word(l53["evidence"]).lower()}: {low(l53["name"])}.', 150, 15)
    mx, my = x0 + S / 2, y0 + 1.5 * S
    out.append(lines(ox + 24, my - 18, n2, 's-note', 21))
    out.append(leader([(ox + 24 + 150 + 4, my - 23), (mx - 12, my - 23), (mx - 4, my - 4)]))
    out.append(f'<a class="go" href="#loop-r10" aria-label="Open loop R10, {e(lp["title"])}.">'
               f'<text x="{f(ox + 24)}" y="{f(oy + h - 22)}" class="s-map">Open loop R10 <tspan class="arr">→</tspan></text>'
               f'<rect class="ak-hit-r" x="{f(ox + 16)}" y="{f(oy + h - 46)}" width="160" height="36"/></a>')
    return ''.join(out)
