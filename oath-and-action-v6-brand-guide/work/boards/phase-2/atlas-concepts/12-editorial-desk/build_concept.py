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


WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def nw(n, cap=False):
    w = WORDS[n] if n < len(WORDS) else str(n)
    return w.capitalize() if cap else w


def cnt(key, n):
    return f'<span data-count="{e(key)}">{n}</span>'


def cnt_svg(key, n):
    return f'<tspan data-count="{e(key)}">{n}</tspan>'


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
    width = 84
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
    XH = 48
    top, TH = XH + 20, 146
    vgap = 50
    bot, BH = top + TH + vgap, 100
    gtop = bot + BH + 22
    blocks = {
        'A': Block('A', xs[0], top, bw, TH, [76, 102, 128]),
        'B': Block('B', xs[1], top, bw, TH, [76, 102, 128]),
        'C': Block('C', xs[2], top, bw, TH, [76, 102, 128]),
        'E': Block('E', xs[0], bot, bw, BH, [54, 80]),
        'D': Block('D', xs[1], bot, PW - xs[1], BH, [54, 80]),
    }
    out = []
    # the outside drivers: one band, one sentence
    xa = AREAS['X']
    xsent = (f'{cnt_svg("variables_X", len(xa["nodes"]))} conditions the model takes as given send '
             f'{cnt_svg("custom:outside-driver-connections", len(X_LINKS))} connections into the system, '
             f'{X_TO.get("A", 0)} to A and {X_TO.get("B", 0)} to B.')
    xname = f'Area X, {xa["title"]}. {xa["text"]} {len(xa["nodes"])} variables.'
    out.append(
        f'<g class="blk tier" role="button" data-select="area-x" aria-label="{e(xname)}" data-say="{e(xname)}">'
        f'<rect class="ak-mark" x=".5" y=".5" width="{f(PW - 1)}" height="{XH - 1}" stroke-width="1"/>'
        f'<text x="14" y="20" class="s-map ak-label">{e(xa["title"])}</text>'
        f'<text x="14" y="39" class="s-cap s-dim">{xsent}</text></g>')
    # the five core areas
    for aid in ['A', 'B', 'C', 'E', 'D']:
        b = blocks[aid]
        a = AREAS[aid]
        name = f'Area {aid}, {a["title"]}. {a["text"]} {len(a["nodes"])} variables.'
        dots = ''
        for v in a['nodes']:
            x, y = b.slot((PLAN['variables'][v]['x'], PLAN['variables'][v]['y']))
            dots += f'<circle class="dot" cx="{f(x)}" cy="{f(y)}" r="3.5"/>'
        rows = wrap(a['title'], b.w - 28 - 22, 20, 700, True)
        head = (f'<text x="{f(b.x + 14)}" y="{f(b.y + 30)}" class="s-station ak-label"><tspan class="lt">{aid}</tspan>'
                f'<tspan x="{f(b.x + 36)}">{e(rows[0])}</tspan>'
                + ''.join(f'<tspan x="{f(b.x + 36)}" dy="22">{e(r)}</tspan>' for r in rows[1:]) + '</text>')
        if aid == 'C':
            rect = f'<rect class="ak-mark" x="{f(b.x + 1)}" y="{f(b.y + 1)}" width="{f(b.w - 2)}" height="{f(b.h - 2)}" stroke-width="2"/>'
            route = route_marks('R10', lambda p, b=b: b.slot(p), w=2.0)
            out.append(f'<a class="blk cl" href="#area-c" aria-label="{e(name)} Opens the close-up." data-say="{e(name)} Opens the close-up.">'
                       f'{rect}{head}{dots}<g class="rt ov">{route}</g></a>')
        else:
            rect = f'<rect class="ak-mark" x="{f(b.x + .5)}" y="{f(b.y + .5)}" width="{f(b.w - 1)}" height="{f(b.h - 1)}" stroke-width="1"/>'
            out.append(f'<g class="blk" role="button" data-select="area-{aid.lower()}" aria-label="{e(name)}" data-say="{e(name)}">'
                       f'{rect}{head}{dots}</g>')

    # the seven core pairs, counted and printed; arrowheads show which way the connections run
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
        if ab and ba:
            say = f'{AREAS[a]["title"]} and {AREAS[b]["title"]}: {tot} connections, {ab} from {a} to {b} and {ba} back.'
        else:
            src, dst, n = (a, b, ab) if ab else (b, a, ba)
            say = f'{AREAS[src]["title"]} to {AREAS[dst]["title"]}: {tot} connections, all running from {src} to {dst}.'
        return (f'<g class="bun" aria-hidden="true"><path class="bl" d="M{f(q0[0])} {f(q0[1])}L{f(q1[0])} {f(q1[1])}"/>{heads}'
                f'<text class="s-fig" x="{f(nx)}" y="{f(ny)}" text-anchor="{anchor}"><tspan data-count="custom:pair-{a}-{b}">{tot}</tspan></text></g>'), say
    A_, B_, C_, D_, E_ = (blocks[k] for k in 'ABCDE')
    yt = top + 102
    yb = bot + 67
    bund = [
        bundle((A_.x + bw + 2, yt), (B_.x - 2, yt), 'A', 'B', A_.x + bw + g / 2, yt - 14),
        bundle((B_.x + bw + 2, yt), (C_.x - 2, yt), 'B', 'C', B_.x + bw + g / 2, yt - 14),
        bundle((E_.x + bw + 2, yb), (D_.x - 2, yb), 'E', 'D', E_.x + bw + g / 2, yb - 14),
    ]
    vy0, vy1 = top + TH + 2, bot - 2
    cx_a, cx_b, cx_c = A_.x + bw / 2, B_.x + bw / 2, C_.x + bw / 2
    my = (vy0 + vy1) / 2 + 15
    bund.append(bundle((cx_a, vy0), (cx_a, vy1), 'A', 'E', cx_a - 12, my, 'end'))
    bund.append(bundle((cx_b, vy0), (cx_b, vy1), 'B', 'D', cx_b + 12, my, 'start'))
    bund.append(bundle((cx_c, vy0), (cx_c, vy1), 'C', 'D', cx_c + 12, my, 'start'))
    bund.append(bundle((B_.x + 1, top + TH + 1), (E_.x + bw + 1, bot - 1), 'B', 'E', B_.x - g / 2 + 14, my, 'start'))
    out.extend(x[0] for x in bund)
    ring_words = [x[1] for x in bund]
    # the economy and technology layers: four areas, then one sentence for each layer
    gh, gg = 50, 12
    gw = (PW - 3 * gg) / 4
    for i, aid in enumerate(('money', 'household', 'production', 'TC')):
        bx0 = i * (gw + gg)
        a = AREAS[aid]
        rows = wrap(a['title'], gw - 24, 15, 600)
        name = f'{a["title"]}. {a["text"]} {len(a["nodes"])} variables.'
        out.append(f'<g class="blk tier" role="button" data-select="area-{aid.lower()}" aria-label="{e(name)}" data-say="{e(name)}">'
                   f'<rect class="ak-mark" x="{f(bx0 + .5)}" y="{f(gtop + .5)}" width="{f(gw - 1)}" height="{gh - 1}" stroke-width="1"/>'
                   + lines(bx0 + 12, gtop + (21 if len(rows) > 1 else 30), rows, 's-map ak-label', 18) + '</g>')
    econ = (f'Economy: three areas, {cnt_svg("custom:economy-variables", ECON_VARS)} conditions. '
            f'{len(ECON_LINKS)} connections touch them, {len(ECON_WITH_A)} of them with A.')
    tech = (f'Technology: {cnt_svg("variables_TC", len(AREAS["TC"]["nodes"]))} conditions. '
            f'{len(TECH_LINKS)} connections touch them, {len(TECH_WITH_D)} of them with D.')
    ey = gtop + gh + 22
    out.append(f'<text x="0" y="{f(ey)}" class="s-cap s-dim">{econ}</text>')
    out.append(f'<text x="0" y="{f(ey + 21)}" class="s-cap s-dim">{tech}</text>')
    H = ey + 21 + 9
    # the inset: area C at reading size, R10 in Charcoal
    ix, iw = 779, OVW - 779
    out.append(f'<path class="zoom" d="M{f(PW)} {f(top + 1)}L{ix} 1M{f(PW)} {f(top + TH - 1)}L{ix} {f(H - 1)}"/>')
    out.append(f'<rect class="inset" x="{ix + .5}" y=".5" width="{f(iw - 1)}" height="{f(H - 1)}"/>')
    out.append(inset_r10(ix, 0, iw, H))
    svg = (f'<svg class="art art-wide" data-view="overview" viewBox="0 0 {OVW} {f(H)}" role="group" '
           f'aria-labelledby="h-overview" data-ak-roving data-ak-nav="spatial">{"".join(out)}</svg>')
    return svg, ring_words


def inset_r10(ox, oy, w, h, S=128, x0=None, y0=None, narrow=False):
    """Area C at reading size: R10's four stations on their plan slots, spaced so the diagonals run at 45 degrees.
    R10's steps in Charcoal at 3 px; the area's fifth variable stands back in Stone."""
    lp = LO['R10']
    x0 = ox + 192 if x0 is None else x0
    y0 = oy + 150 if y0 is None else y0
    pos = {'C2': (x0, y0), 'C3': (x0, y0 + S), 'C1': (x0 + S, y0 + S), 'C4': (x0 + S, y0 + 2 * S), 'C5': (x0, y0 + 2 * S)}
    out = []
    pad = 20 if narrow else 24
    out.append(text(ox + pad, oy + 34, 'Inside area C', 's-eye'))
    title_rows = wrap(lp['title'], w - 2 * pad - 10, 22, 800, True)
    out.append(lines(ox + pad, oy + 64, title_rows, 's-head', 26, extra=f' data-loop="R10" data-name="{e(lp["title"])}"'))
    R = 9
    for st in lp['steps']:
        a, b = pos[st['from']], pos[st['to']]
        pts = edge_pts(a, b, 2 * R, 2 * R, 2 * R, 2 * R, 3, 3)
        out.append(wire(st['id'], pts, w=3, interactive=False))
    for v, (x, y) in pos.items():
        ctx = ' ctx' if v == 'C5' else ''
        out.append(f'<circle class="st-dot{ctx}" cx="{f(x)}" cy="{f(y)}" r="{R}"/>')
    lab = {'C2': (x0 + 20, y0 + 6, 'start'), 'C1': (x0 + S + 20, y0 + S + 6, 'start'),
           'C3': (x0 - 20, y0 + S + 6, 'end'), 'C5': (x0 - 20, y0 + 2 * S + 6, 'end')}
    for v, (x, y, anc) in lab.items():
        cls = 's-map' + (' s-ctx' if v == 'C5' else '')
        room = (x - (ox + pad)) if anc == 'end' else (ox + w - pad - x)
        rows = wrap(N[v]['label'], room, 15, 600)
        out.append(lines(x, y - 9 * (len(rows) - 1), rows, cls, 18, anc, extra=f' data-node="{v}" data-name="{e(N[v]["label"])}"'))
    c4w = ox + w - pad - (x0 + S + 20)
    c4rows = wrap(N['C4']['label'], c4w, 15, 600)
    out.append(lines(x0 + S + 20, y0 + 2 * S + 6, c4rows, 's-map', 18, extra=f' data-node="C4" data-name="{e(N["C4"]["label"])}"'))
    if narrow:      # on a phone the notes move below the drawing
        gy = oy + h - 24
        out.append(f'<a class="go" href="#loop-r10" aria-label="Open loop R10, {e(lp["title"])}.">'
                   f'<rect class="ak-hit-r" x="{f(ox + pad - 6)}" y="{f(gy - 26)}" width="150" height="40"/>'
                   f'<text x="{f(ox + pad)}" y="{f(gy)}" class="s-map">Open loop R10 →</text></a>')
        return ''.join(out)
    # notes on leader lines
    nx = x0 + S + 20
    n1 = wrap('Start here, then follow the arrows. Each step raises or lowers the next.', ox + w - pad - nx, 15)
    ny = y0 + S - 30 - 21 * (len(n1) - 1)
    out.append(lines(nx, ny, n1, 's-note', 21))
    out.append(leader([(nx - 4, ny - 5), (x0 + S - 14, ny - 5), (x0 + S - 4, y0 + S - 12)]))
    l53 = L['L53']
    n2 = wrap(f'The weakest step, graded {grade_word(l53["evidence"]).lower()}.', x0 - 30 - (ox + pad), 15)
    by = y0 + S + 52
    out.append(lines(x0 - 30, by, n2, 's-note', 21, anchor='end'))
    lx = x0 + (by - 5 - (y0 + S)) - 4      # 2 px short of L53, which runs at 45 degrees from C3
    out.append(leader([(x0 - 24, by - 5), (lx, by - 5)]))
    gy = oy + h - 24
    out.append(f'<a class="go" href="#loop-r10" aria-label="Open loop R10, {e(lp["title"])}.">'
               f'<rect class="ak-hit-r" x="{f(ox + pad - 6)}" y="{f(gy - 26)}" width="150" height="40"/>'
               f'<text x="{f(ox + pad)}" y="{f(gy)}" class="s-map">Open loop R10 →</text></a>')
    return ''.join(out)


# ------------------------------------------------------------------------------------------------ the loop index (strip)
def strip_order():
    out = []
    for g in M['groups']:
        ids = sorted(g['loops'], key=lambda k: (LO[k]['n'] if not LO[k]['conceptual'] else 9, M['loop_order'].index(k)))
        out.append((g, ids))
    return out


def strip_card(lid, width=310):
    lp = LO[lid]
    steps = 'sketch' if lp['conceptual'] else ' '.join(s['id'] for s in lp['steps'])
    th = thumb_svg(lid, width, view='loop-route')
    head = (f'{th}<span class="lp-k"><span class="lp-id">{lid}</span> {e(kind_line(lid))}</span>'
            f'<span class="lp-t" data-loop="{lid}" data-name="{e(lp["title"])}">{e(lp["title"])}</span>')
    say = f'Loop {lid}, {kind_line(lid)}: {lp["title"]}.'
    if lid == 'R10':
        hit = (f'<a class="lp-hit" href="#loop-r10" aria-label="{e(say)} Opens the close-up." data-say="{e(say)} Opens the close-up.">'
               f'{head}<span class="lp-go">Open the close-up <span aria-hidden="true">→</span></span></a>')
    else:
        hit = (f'<button type="button" class="lp-hit" data-select="loop-{lid.lower()}" aria-label="{e(say)}" data-say="{e(say)}">{head}</button>')
    disc = ''
    if lid in DISCLOSE:
        disc = f'<p class="lp-x"><span class="sq" aria-hidden="true"></span>{e(DISCLOSE[lid])}</p>'
    return (f'<li class="lp" data-loop="{lid}" data-steps="{steps}">{hit}'
            f'<p class="lp-s">{e(first_sentence(lp["summary"]))}</p>'
            f'<p class="lp-r">{e(read_aloud(lid))}</p>'
            f'<p class="lp-m">{e(status_line(lid))}</p>{disc}</li>')


def strip_html():
    groups = []
    for g, ids in strip_order():
        if g['id'] == 'SK':
            lab = 'Sketches'
            title = g['title']
            txt = 'Three loops the model describes in words. None has a complete chain of numbered connections, so each sits off the map.'
        else:
            a = AREAS[g['id']]
            lab = f'Area {g["id"]}'
            title = a['title']
            txt = a['text']
        nr = sum(1 for k in ids if LO[k]['type'] == 'R')
        nb = len(ids) - nr
        kinds = ', '.join(x for x in [f'{nr} reinforcing' if nr else '', f'{nb} balancing' if nb else ''] if x)
        if not nb or not nr:
            kinds = 'all reinforcing' if not nb else 'all balancing'
        if len(ids) == 1:
            kinds = kinds.replace('all ', '')
        cards = ''.join(strip_card(k) for k in ids)
        groups.append(
            f'<section class="lg" aria-labelledby="lg-{g["id"].lower()}">'
            f'<header class="lg-h"><p class="t-eyebrow">{e(lab)}</p><h3 class="t-panelhead" id="lg-{g["id"].lower()}">{e(title)}</h3>'
            f'<p class="lg-t">{e(txt)}</p><p class="lg-n">{len(ids)} loop{"s" if len(ids) != 1 else ""}, {kinds}</p></header>'
            f'<ul class="lp-grid" data-ak-roving data-ak-nav="sequence" aria-label="Loops grouped under {e(title)}">{cards}</ul></section>')
    gloss = M['glossary']['Reinforcing loop (R)']
    quote = next(s for s in re.split(r'(?<=\.)\s', gloss) if s.startswith('Improvement'))
    return (f'<section class="strip" data-strip="loops" aria-labelledby="h-loops" id="loops-index">'
            f'<div class="strip-h"><p class="t-eyebrow label">Every loop, drawn as its own route</p>'
            f'<h2 class="t-headline" id="h-loops">Of the {cnt("loops", len(LO))} loops, {cnt("loops_reinforcing", N_R)} feed themselves, '
            f'and {cnt("custom:loops-with-a-reform", N_WITH_REFORM)} have a reform aimed at them.</h2>'
            f'<p class="t-deck">A loop is a chain of causes that returns to where it started. The other {cnt("loops_balancing", N_B)} push back. '
            f'The model warns that a loop is no verdict: <q class="t-quote-in">{e(quote)}</q> Each small map shows the loop’s route across the system, '
            f'with the same marks as the drawing above.</p></div>'
            + ''.join(groups) + '</section>')


# ------------------------------------------------------------------------------------------------ panel templates
SRC = f'<p class="src">Atlas V7, snapshot {SNAP_WORDS}.</p>'


def pick(key, label):
    return f'<button type="button" class="ak-btn pick" data-ak-pick="{key}">{e(label)}</button>'


def tpl_area(aid):
    a = AREAS[aid]
    links = touching(aid)
    inside = [l for l in links if AREA_OF[l['from']] == aid and AREA_OF[l['to']] == aid]
    partners = {}
    for l in links:
        o = AREA_OF[l['to']] if AREA_OF[l['from']] == aid else AREA_OF[l['from']]
        if o != aid:
            partners[o] = partners.get(o, 0) + 1
    plist = ''.join(f'<li>{e(AREAS[o]["title"])}: {n}</li>' for o, n in sorted(partners.items(), key=lambda x: -x[1]))
    vs = ''.join(f'<li><strong>{v}</strong> {e(N[v]["label"])}</li>' for v in a['nodes'])
    grp = next((g for g in M['groups'] if g['id'] == aid), None)
    lps = ''.join(f'<li>{k} {e(LO[k]["title"])}</li>' for k in grp['loops']) if grp else '<li>None grouped here</li>'
    return (f'<template data-detail="area-{aid.lower()}" data-kind="Area {aid}" data-title="{e(a["title"])}">'
            f'<p class="lead">{e(a["text"])}</p>'
            f'<dl><dt>Variables</dt><dd>{len(a["nodes"])}</dd><dt>Connections</dt><dd>{len(links)} touch it; {len(inside)} stay inside</dd></dl>'
            f'<h3>Variables</h3><ul class="plain">{vs}</ul>'
            f'<h3>Connections with other areas</h3><ul class="plain">{plist}</ul>'
            f'<h3>Loops grouped here</h3><ul class="plain">{lps}</ul>'
            f'<p class="note">This concept draws area C up close. Every area would open the same way.</p>{SRC}</template>')


def tpl_loop(lid):
    lp = LO[lid]
    if lp['conceptual']:
        steps = ''.join(f'<li>{e(s["from_label"])} {verb(s["polarity"])} {e(low(s["to_label"]))}. Sketched step, no numbered connection.</li>' for s in lp['steps'])
    else:
        steps = ''.join(f'<li><strong>{s["id"]}</strong> {e(s["name"])}. {verb(s["polarity"]).capitalize()}, {sign_char(s["polarity"])}; '
                        f'{grade_word(s["evidence"]).lower()}, {grade_gloss(s["evidence"])}; {delay_words(s["delay"])}.</li>' for s in lp['steps'])
    refs = ''.join(f'<li>{r} {e(RF[r]["title"])}</li>' for r in lp['reforms']) or '<li>None in the model</li>'
    disc = f'<p class="note">{e(DISCLOSE[lid])}</p>' if lid in DISCLOSE else ''
    return (f'<template data-detail="loop-{lid.lower()}" data-kind="Loop {lid}" data-title="{e(lp["title"])}">'
            f'<p class="lead">{e(lp["summary"])}</p>'
            f'<dl><dt>Kind</dt><dd>{e(kind_line(lid))}</dd><dt>Closure</dt><dd>{e(lp["closure"])}</dd>'
            f'<dt>One turn</dt><dd>{e(lp["delay_word"])}</dd><dt>Now</dt><dd>{e(lp["direction_word"])}, measured by: {e(lp["reference_mode"])}</dd>'
            f'<dt>Weakest</dt><dd>{e(weakest_words(lid))}</dd></dl>'
            f'<h3>Read it aloud</h3><p>{e(read_aloud(lid))}</p>'
            f'<h3>Steps</h3><ol>{steps}</ol>'
            f'<h3>Reforms aimed at it</h3><ul class="plain">{refs}</ul>'
            f'<h3>Keep in mind</h3><p>{e(lp["qualification"])}</p>{disc}{SRC}</template>')


def tpl_var(vid):
    n = N[vid]
    outs = [l for l in L.values() if l['from'] == vid]
    ins = [l for l in L.values() if l['to'] == vid]

    def li(l, other):
        far = e(other + ' ' + N[other]['label'])
        rel_ = f'{verb(l["polarity"]).capitalize()} {far}' if l['from'] == vid else f'{far} {verb(l["polarity"])} it'
        return (f'<li><strong>{l["id"]}</strong> {e(l["name"])}. {rel_}; {grade_word(l["evidence"]).lower()}; {delay_words(l["delay"])}.</li>')
    lps = ''.join(f'<li>{k} {e(LO[k]["title"])}</li>' for k in n['loops']) or '<li>None</li>'
    refs = [r for r in RF.values() if vid in r['targets']]
    rl = ''.join(f'<li>{r["id"]} {e(r["title"])}</li>' for r in refs) or '<li>None in the model</li>'
    return (f'<template data-detail="var-{vid.lower()}" data-kind="Variable {vid}" data-title="{e(n["label"])}">'
            f'<p class="lead">{e(n["title"])}. {e(n["increase_means"])}</p>'
            f'<dl><dt>Area</dt><dd>{n["area"] if n["area"] in AREAS else AREA_OF[vid]}, {e(AREAS[AREA_OF[vid]]["title"])}</dd><dt>Type</dt><dd>{n["type"]}</dd></dl>'
            f'<h3>Pushes ({len(outs)})</h3><ul class="plain">{"".join(li(l, l["to"]) for l in outs)}</ul>'
            f'<h3>Pushed by ({len(ins)})</h3><ul class="plain">{"".join(li(l, l["from"]) for l in ins)}</ul>'
            f'<h3>Loops</h3><ul class="plain">{lps}</ul><h3>Reforms that act on it</h3><ul class="plain">{rl}</ul>{SRC}</template>')


def tpl_link(lid):
    l = L[lid]
    refs = [r for r in RF.values() if lid in r['targets']]
    rl = ''.join(f'<li>{r["id"]} {e(r["title"])}</li>' for r in refs) or '<li>None in the model</li>'
    lps = ''.join(f'<li>{k} {e(LO[k]["title"])}</li>' for k in l['loops']) or '<li>None. This connection sits on no loop.</li>'
    return (f'<template data-detail="link-{lid.lower()}" data-kind="Connection {lid}" data-title="{e(l["name"])}">'
            f'<dl><dt>From</dt><dd>{l["from"]} {e(N[l["from"]]["label"])}</dd><dt>To</dt><dd>{l["to"]} {e(N[l["to"]]["label"])}</dd>'
            f'<dt>Sign</dt><dd>{sign_char(l["polarity"])} {verb(l["polarity"])}: {sign_words(l["polarity"])}. {e(acc.SIGN_RULE)}</dd>'
            f'<dt>Type</dt><dd>{l["type"]}</dd><dt>Delay</dt><dd>{delay_words(l["delay"])}</dd>'
            f'<dt>Evidence</dt><dd>{grade_word(l["evidence"])}: {grade_gloss(l["evidence"])}</dd></dl>'
            f'<h3>Loops it sits on</h3><ul class="plain">{lps}</ul><h3>Reforms that act on it</h3><ul class="plain">{rl}</ul>{SRC}</template>')


def tpl_reform(rid):
    r = RF[rid]
    eff = ''.join(f'<dt>{e(M["families"][k])}</dt><dd>{e(v)}, {e(M["effect_codes"].get(v, v))}</dd>' for k, v in r['effects'].items())
    routes = ''.join(f'<li><strong>{e(M["route_names"][x["route"]])}</strong>, {e(x["who"])}. Feasibility {e(x["feasibility"])}. '
                     f'{"Checked " + e(x["checked"]) if x["checked"] else "No check date in V7"}.</li>' for x in r['routes'])
    tg = ', '.join(r['targets'])
    return (f'<template data-detail="reform-{rid.lower()}" data-kind="Reform {rid}" data-title="{e(r["title"])}">'
            f'<p class="lead">{e(r["summary"])}</p>'
            f'<h3>Where it acts</h3><p>{e(tg)}. While this reform is in view, its targets take the red.</p>'
            f'<h3>Expected effects</h3><dl>{eff}</dl><p class="note">Four separate judgments, never added together. Confidence: {e(r["effects_confidence"])}.</p>'
            f'<dl><dt>Problem evidence</dt><dd>{grade_word(r["problem_grade"])}</dd><dt>Remedy evidence</dt><dd>{grade_word(r["remedy_grade"])}</dd></dl>'
            f'<h3>Routes</h3><ul class="plain">{routes}</ul><h3>Keep in mind</h3><p>{e(r["remedy_text"])}</p>{SRC}</template>')


# ------------------------------------------------------------------------------------------------ styles
CSS = r"""
:root {
  --ink: #121212; --stone: #5D636D; --deep: #4E535B; --red: #E63946; --white: #FFFFFF; --newsprint: #DCD9D2;
  --ak-w-lo: 2px; --ak-w-hi: 3px; --ak-w-sel: 6px;
  --col: calc((100% - 11 * 24px) / 12);
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--white); color: var(--ink); font: 400 17px/27px Inter, system-ui, sans-serif;
  font-feature-settings: "ss01" 0; -webkit-font-smoothing: antialiased; }
.wrap { max-width: 1440px; margin: 0 auto; padding: 0 64px; }
.g12 { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 24px; }
a { color: inherit; }
.ak-vh { position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }

/* type scale: design frame memo, section 2 */
.t-display { margin: 0; font: 800 56px/60px "Inter Tight", Inter, sans-serif; letter-spacing: -0.035em; text-wrap: balance; margin-left: -0.04em; }
.t-headline { margin: 0; font: 800 40px/44px "Inter Tight", Inter, sans-serif; letter-spacing: -0.03em; text-wrap: balance; }
.t-deck { margin: 0; font: 400 19px/28px Inter, sans-serif; max-width: 62ch; }
.t-panelhead { margin: 0; font: 800 22px/26px "Inter Tight", Inter, sans-serif; letter-spacing: -0.02em; text-wrap: balance; }
.t-eyebrow { margin: 0; font: 700 13px/18px Inter, sans-serif; letter-spacing: .06em; text-transform: uppercase; }
.t-body { font: 400 17px/27px Inter, sans-serif; }
.t-panel { font: 400 15px/23px Inter, sans-serif; }
.t-quote { margin: 0; font: italic 400 22px/31px Lora, Georgia, serif; letter-spacing: -0.005em; }
.t-quote-in { font: italic 400 1em/1 Lora, Georgia, serif; quotes: "\201C" "\201D"; }
.t-figure { font: 800 40px/40px "Inter Tight", Inter, sans-serif; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.t-caption { font: 400 14px/20px Inter, sans-serif; }
.t-legend { font: 500 13px/18px Inter, sans-serif; }
.t-source { margin: 0; font: 400 13px/18px Inter, sans-serif; color: var(--deep); }
.dim { color: var(--deep); }

/* masthead */
.mast { height: 72px; border-bottom: 1px solid var(--stone); align-items: start; }
.mast .wm { grid-column: 1 / 4; margin-top: 24px; display: inline-block; width: max-content; color: var(--ink); }
.mast .wm svg { display: block; }
.mast .wm .wm16 { display: none; }
.runhead { grid-column: 4 / 8; margin-top: 27px; color: var(--deep); }
.views { grid-column: 8 / 13; justify-self: end; display: flex; gap: 28px; height: 72px; }
.views a { display: flex; align-items: center; height: 72px; min-height: 44px; font: 600 15px/1 Inter, sans-serif; text-decoration: none;
  box-shadow: inset 0 -3px 0 transparent; }
.views a:hover { text-decoration: underline; text-underline-offset: 4px; }
.views a[aria-current="page"] { box-shadow: inset 0 -3px 0 var(--ink); }

/* breadcrumb */
.crumbrow { padding-top: 16px; min-height: 37px; }
.ak-crumbs a { color: var(--deep); text-decoration-color: var(--deep); }
.ak-crumbs [aria-current] { font-weight: 600; color: var(--ink); }

/* headline block */
.lede { margin-top: 24px; row-gap: 16px; }
.lede-main { grid-column: 1 / 8; }
.lede-key { grid-column: 8 / 13; padding-top: 4px; }
.label { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; color: var(--ink); }
.label svg { flex: none; }
.lede .t-deck { margin-top: 14px; }
.howto { margin: 0; border-top: 1px solid var(--ink); padding-top: 10px; }
.howto h2 { margin: 0 0 6px; }
.howto p { margin: 0 0 8px; font: 400 14px/20px Inter, sans-serif; }
.keyrows { list-style: none; margin: 8px 0 8px; padding: 0; display: grid; grid-template-columns: max-content max-content; justify-content: start; gap: 4px 18px; }
.keyrows li { display: flex; align-items: center; gap: 8px; font: 500 13px/18px Inter, sans-serif; }
.keyrows svg { flex: none; }
.ckey { display: flex; gap: 16px; align-items: flex-start; border-top: 1px solid var(--ink); padding-top: 10px; }
.ckey .howto { border: 0; padding: 0; }
.loc { flex: none; display: block; line-height: 0; }
.loc:hover .pb, .loc:focus-visible .pb { stroke: var(--ink); }

/* drawings */
.fig { margin: 22px 0 0; }
.art { display: block; width: 100%; height: auto; overflow: visible; }
.art-narrow { display: none; }
.ak-readout { margin: 10px 0 0; min-height: 23px; font: 400 15px/23px Inter, sans-serif; color: var(--deep); }
svg text { fill: var(--ink); }
.s-station { font: 700 20px "Inter Tight", Inter, sans-serif; letter-spacing: -0.01em; }
.s-map { font: 600 15px Inter, sans-serif; }
.s-cap { font: 400 15px Inter, sans-serif; }
.s-note { font: 400 15px Inter, sans-serif; }
.s-noteb { font: 600 15px Inter, sans-serif; }
.s-fig { font: 800 40px "Inter Tight", Inter, sans-serif; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.s-head { font: 800 22px "Inter Tight", Inter, sans-serif; letter-spacing: -0.02em; }
.s-eye { font: 700 13px Inter, sans-serif; letter-spacing: .06em; text-transform: uppercase; }
.s-small { font: 400 13px Inter, sans-serif; }
svg .s-dim { fill: var(--deep); }
svg .s-ctx { fill: var(--stone); }
svg .lt { font-weight: 800; }
.leader { fill: none; stroke: var(--stone); stroke-width: 1; }
.zoom { fill: none; stroke: var(--stone); stroke-width: 1; }
.inset { fill: none; stroke: var(--ink); stroke-width: 1; }

/* plan blocks on the overview */
.blk { color: var(--stone); }
.blk .ak-mark { fill: var(--white); }
.blk.cl { color: var(--ink); }
.blk.cl .ak-mark { stroke-width: 2; }
.blk:hover .ak-label, .blk:focus-visible .ak-label { text-decoration: underline; text-underline-offset: 3px; }
.blk[data-ak-sel] .ak-mark, .blk.ak-rel .ak-mark { stroke-width: 3px; }
.dot { fill: var(--stone); }
.bun { color: var(--stone); }
.bun .bl { stroke: var(--stone); stroke-width: 2; fill: none; }
.ak-hit-r { fill: transparent; }
.go:hover text { text-decoration: underline; text-underline-offset: 3px; }

/* connections */
.wire { color: var(--ink); }
.wire.ctx { color: var(--stone); }
.ak-head { fill: var(--ak-hi, currentColor); stroke: none; }
.tick { stroke: var(--ak-hi, currentColor); stroke-width: 2; fill: none; }
.tag polygon { fill: currentColor; stroke: var(--white); stroke-width: 4; stroke-linejoin: round; paint-order: stroke; }
.tag .sg { fill: var(--white); }
.sz-hi { display: none; }
[data-select][data-ak-sel] .sz-hi, [data-select].ak-target .sz-hi, [data-select].ak-now .sz-hi { display: inline; }
[data-select][data-ak-sel] .sz-lo, [data-select].ak-target .sz-lo, [data-select].ak-now .sz-lo { display: none; }
[data-select]:hover, [data-select]:focus-visible, [data-select].ak-rel, [data-select].ak-target, [data-select][data-ak-sel] { color: var(--ink); }
[data-select]:hover .ak-mark, .ak-rel .ak-mark { stroke-dasharray: var(--d3); }
.ak-dim [data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target) .ak-mark { stroke-dasharray: var(--d2); }
.ak-dim [data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target) { color: var(--stone); }
[data-select][data-ak-sel] .ak-mark, [data-select].ak-target .ak-mark, [data-select].ak-now .ak-mark { stroke-dasharray: var(--d6); }
.ak-stepping [data-select]:not(.ak-now):not(.ak-done):not(.ak-target) { color: var(--stone); }
.ak-stepping [data-select]:not(.ak-now):not(.ak-done):not(.ak-target) .ak-mark { stroke-dasharray: var(--d2); stroke-width: 2px; }
.nd .ak-mark { fill: var(--white); }
.nd[data-ak-sel] .ak-mark, .nd.ak-target .ak-mark, .nd.ak-now .ak-mark { stroke-width: 3px !important; }
.nd[data-ak-sel] .ak-label { text-decoration: underline; text-underline-offset: 4px; }
.nd .code { font: 700 14px Inter, sans-serif; font-variant-numeric: tabular-nums; }
.nd.ctx { color: var(--stone); }
.nd.ctx .code { fill: var(--stone); }

/* route thumbnails and the small route on the overview */
.pb { fill: none; stroke: var(--stone); stroke-width: 1; }
.pb.on { stroke: var(--ink); }
.pd { fill: var(--stone); }
.rt .rl { fill: none; stroke: var(--ink); }
.rt .rh { fill: none; stroke: var(--white); }
.rt .tt { fill: var(--ink); stroke: var(--white); stroke-width: 1.2; stroke-linejoin: round; }
.rt .tg { stroke: var(--white); fill: none; }
.rt .cb { stroke: var(--ink); stroke-width: 2; }
.rt .so circle { fill: var(--white); stroke: var(--ink); stroke-width: 2; }
.rt .so .sc { fill: var(--ink); stroke: none; }
.rt .ss { fill: var(--ink); stroke: var(--white); stroke-width: 1.4; }
.rt .sx { fill: var(--white); stroke: var(--ink); stroke-width: 1.5; }
.st-dot { fill: var(--white); stroke: var(--ink); stroke-width: 2; }
.abox { fill: none; stroke: var(--stone); stroke-width: 1; }
.defs { margin-top: 32px; border-top: 1px solid var(--ink); padding-top: 14px; }
.deflist { list-style: none; margin: 14px 0 0; padding: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 20px 24px; }
.deflist li { font: 400 15px/23px Inter, sans-serif; }
.deflist strong { display: block; margin: 8px 0 4px; font: 700 20px/22px "Inter Tight", Inter, sans-serif; letter-spacing: -0.01em; }
.linewords { margin: 12px 0 0; padding-left: 22px; columns: 2; column-gap: 48px; font: 400 15px/23px Inter, sans-serif; }
.linewords li { break-inside: avoid; margin-bottom: 8px; }
.area-loops { margin-top: 48px; }
/* R10 told in order: text on the left, the drawing held still on the right */
.story { margin-top: 40px; align-items: start; }
.story-text { grid-column: 1 / 5; }
.story-art { grid-column: 5 / 13; position: sticky; top: 16px; margin: 0; }
.story-step { min-height: 62vh; padding: 18px 0 0; border-top: 1px solid var(--stone); font: 400 17px/27px Inter, sans-serif; }
.story-step:first-child { min-height: 46vh; }
.story-step:last-child { min-height: 0; }
.story-step p { margin: 10px 0 0; }
.story-step h3 { margin-top: 10px; }
.story-step .t-eyebrow { display: flex; align-items: center; gap: 10px; color: var(--deep); }
.story-step.on { border-top: 3px solid var(--ink); padding-top: 16px; }
.story-step.on .t-eyebrow { color: var(--ink); }
.story-lead { font: 400 19px/28px Inter, sans-serif; }
.story-facts { display: flex; flex-wrap: wrap; gap: 4px 18px; font: 500 13px/18px Inter, sans-serif; color: var(--deep); }
.story-facts span:first-child { color: var(--ink); font-weight: 700; }
.story-flag { padding-left: 12px; box-shadow: inset 3px 0 0 var(--ink); }
.story-act { font: 600 15px/23px Inter, sans-serif; }
.aloud { margin: 10px 0 0; font: 600 19px/28px Inter, sans-serif; }
.vb { fill: var(--ink); }
.reforms { list-style: none; margin: 14px 0 0; padding: 0; display: grid; gap: 12px; }
.reforms li { display: grid; gap: 4px; }
.reform-btn { display: flex; align-items: center; gap: 10px; min-height: 44px; text-align: left; font: 600 15px/20px Inter, sans-serif; }
.reform-at { font: 400 14px/20px Inter, sans-serif; color: var(--deep); }
.mk { fill: var(--ink); }
.after { margin-top: 56px; border-top: 1px solid var(--ink); padding-top: 14px; }
.after-q { grid-column: 1 / 6; }
.after-q blockquote { margin: 12px 0 0; }
.after-w { grid-column: 7 / 13; }
.linewords.one { columns: 1; }
.wide-scroll .art-wide { display: block; }
.full-btn { display: none; margin-top: 10px; }
.scroll-hint { display: none; margin: 0 0 8px; }
.ak-full .art-wide { display: block; }
.s-stationp { font: 700 18px "Inter Tight", Inter, sans-serif; letter-spacing: -0.01em; }
.s-figp { font: 800 32px "Inter Tight", Inter, sans-serif; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.inset-n { margin-top: 24px; }
.phone-notes { display: none; margin: 12px 0 0; padding-left: 22px; font: 400 15px/23px Inter, sans-serif; }
.ringwords { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 48px; font: 400 15px/23px Inter, sans-serif; }
.ringwords li { break-inside: avoid; margin-bottom: 6px; }
.ak-full > svg { width: var(--ak-full-w, 1312px); }
.st-dot.ctx { stroke: var(--stone); }
.loc-svg .pb[data-locate].ak-here { stroke: var(--ink); stroke-width: 2; }

/* areas in words */
.words { margin-top: 40px; border-top: 1px solid var(--ink); padding-top: 14px; }
.words h2 { margin: 0 0 14px; }
.arealist { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 20px 24px; }
.arealist li { font: 400 15px/23px Inter, sans-serif; }
.arealist strong { display: block; font: 800 22px/26px "Inter Tight", Inter, sans-serif; letter-spacing: -0.02em; margin-bottom: 4px; }
.arealist .n { display: block; margin-top: 4px; font: 500 13px/18px Inter, sans-serif; color: var(--deep); }

/* the loop index */
.strip { margin-top: 72px; }
.strip-h { max-width: calc(8 * var(--col) + 7 * 24px); border-top: 1px solid var(--ink); padding-top: 14px; }
.strip-h .t-deck { margin-top: 14px; }
.lg { margin-top: 48px; }
.lg-h { border-top: 1px solid var(--stone); padding-top: 12px; display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 24px; align-items: baseline; }
.lg-h .t-eyebrow { grid-column: 1 / 3; color: var(--deep); }
.lg-h h3, .lg-h h2 { grid-column: 3 / 7; }
.lg-t { grid-column: 7 / 11; margin: 0; font: 400 15px/23px Inter, sans-serif; }
.lg-n { grid-column: 11 / 13; margin: 0; text-align: right; font: 500 13px/18px Inter, sans-serif; color: var(--deep); }
.lp-grid { list-style: none; margin: 20px 0 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 40px 24px; }
.lp { min-width: 0; }
.lp-hit { display: block; width: 100%; padding: 0; margin: 0; border: 0; background: none; text-align: left; color: inherit; cursor: pointer; text-decoration: none; font: inherit; }
.lp-hit .th { display: block; width: 100%; height: auto; }
.lp-k { display: block; margin-top: 10px; font: 500 13px/18px Inter, sans-serif; color: var(--deep); }
.lp-id { font-weight: 700; color: var(--ink); }
.lp-t { display: block; margin-top: 4px; font: 800 22px/26px "Inter Tight", Inter, sans-serif; letter-spacing: -0.02em; text-wrap: balance; }
.lp-hit:hover .lp-t { text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 2px; }
.lp-go { display: block; margin-top: 6px; font: 600 15px/23px Inter, sans-serif; text-decoration: underline; text-underline-offset: 3px; }
.lp-s { margin: 8px 0 0; font: 400 15px/23px Inter, sans-serif; }
.lp-r { margin: 8px 0 0; font: 400 14px/20px Inter, sans-serif; color: var(--deep); }
.lp-m { margin: 8px 0 0; padding-top: 8px; border-top: 1px solid var(--stone); font: 500 13px/18px Inter, sans-serif; color: var(--deep); }
.lp-x { margin: 8px 0 0; font: 400 14px/20px Inter, sans-serif; display: flex; gap: 8px; }
.lp-x .sq { flex: none; width: 7px; height: 7px; margin-top: 6px; background: var(--ink); }
.lp-hit[data-ak-sel] { box-shadow: none; }
.lp-hit[data-ak-sel] .th { outline: 3px solid var(--ak-hi, var(--ink)); outline-offset: 0; }
.lp-hit:focus-visible { outline: 2px solid var(--verd, #4A7C74); outline-offset: 4px; }

/* ID chips */
.chip { display: inline-flex; align-items: stretch; height: 26px; vertical-align: middle; font-variant-numeric: tabular-nums; }
.chip .k { display: flex; align-items: center; padding: 0 7px; background: var(--ink); color: var(--white); font: 600 13px/1 Inter, sans-serif; letter-spacing: .06em; text-transform: uppercase; }
.chip .c { display: flex; align-items: center; padding: 0 8px; border: 1.5px solid var(--ink); border-left: 0; font: 700 14px/1 Inter, sans-serif; }
.chip.compact { height: 22px; }
.chip.compact .c { font-size: 13px; }

/* panel: a drawer over the page's right edge on a wide screen, a sheet on a phone */
.ak-panel { background: var(--white); }
.ak-panel h2 { font: 800 22px/26px "Inter Tight", Inter, sans-serif; letter-spacing: -0.02em; }
.ak-panel .lead { margin: 0 0 12px; font: 400 15px/23px Inter, sans-serif; }
.ak-panel ul.plain { list-style: none; padding: 0; }
.ak-panel ul.plain li { margin-bottom: 6px; }
.ak-panel .note, .ak-panel .src { margin-top: 14px; font: 400 14px/20px Inter, sans-serif; color: var(--deep); }
.pick { min-height: 32px; text-align: left; }
@media (min-width: 900px) {
  .ak-panel { position: fixed; top: 0; right: 0; bottom: 0; width: 400px; max-height: none; z-index: 60;
    border-left: 1px solid var(--ink); padding: 24px 28px 32px; }
}

/* footer */
.foot { margin-top: 96px; border-top: 1px solid var(--stone); padding: 14px 0 40px; }
.foot .t-source.right { grid-column: 9 / 13; text-align: right; }
.foot .t-source.left { grid-column: 1 / 9; }

/* wide artboards only where their 15 px labels stay at 13 px or more */
@media (max-width: 1264px) {
  .art-wide { display: none; }
  .wide-scroll .art-wide { display: block; }
  .art-narrow { display: block; max-width: 480px; margin: 0 auto; }
  .full-btn { display: inline-block; }
  .phone-notes { display: block; max-width: 480px; margin-left: auto; margin-right: auto; }
  .story-art .art-narrow { max-width: 420px; }
  .scroll-hint { display: block; }
}
@media (max-width: 520px) {
  .keyrows { grid-template-columns: 1fr; }
}
@media (max-width: 1100px) {
  .wrap { padding: 0 32px; }
  .arealist { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .lp-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 700px) {
  .wrap { padding: 0 20px; }
  .g12 { grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: 16px; }
  .mast { height: auto; display: block; border-bottom: 1px solid var(--stone); }
  .mast .wm { margin: 20px 0 0; }
  .mast .wm .wm24 { display: none; }
  .mast .wm .wm16 { display: block; }
  .runhead { display: none; }
  .views { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; height: auto; margin-top: 12px; }
  .views a { height: 44px; justify-content: center; }
  .lede-main, .lede-key { grid-column: 1 / -1; }
  .t-display { font-size: 36px; line-height: 40px; letter-spacing: -0.03em; }
  .t-headline { font-size: 30px; line-height: 34px; }
  .t-deck { font-size: 17px; line-height: 25px; }
  .t-panelhead { font-size: 20px; line-height: 24px; }
  body { font-size: 16px; line-height: 25px; }
  .t-quote { font-size: 19px; line-height: 27px; }
  .t-figure { font-size: 32px; line-height: 32px; }
  .art-narrow { max-width: none; }
  .arealist { grid-template-columns: 1fr; }
  .lp-grid { grid-template-columns: 1fr; }
  .lg-h { display: block; }
  .lg-n { text-align: left; margin-top: 4px; }
  .foot { display: block; }
  .foot .t-source.right { text-align: left; margin-top: 8px; }
  .deflist { grid-template-columns: 1fr; }
  .linewords { columns: 1; }
  .story { display: flex; flex-direction: column; }
  .story-art { order: -1; align-self: stretch; width: 100%; position: sticky; top: 0; z-index: 3; background: var(--white); padding: 8px 0 4px; border-bottom: 1px solid var(--stone); }
  .story-art .ak-readout { display: none; }
  .story-step { min-height: 56vh; font-size: 16px; line-height: 25px; }
  .story-lead { font-size: 17px; line-height: 25px; }
  .after { display: block; }
  .after-w { margin-top: 24px; }
  .ckey { flex-direction: row; }
  .lede-key { margin-top: 8px; }
  .aloud { font-size: 16px; line-height: 25px; }
  .strip { margin-top: 48px; }
  .strip-h { max-width: none; }
  .ringwords { columns: 1; }
  .lp-t { font-size: 20px; line-height: 24px; }
}
@media (max-width: 1100px) {
  .story-text { grid-column: 1 / 6; }
  .story-art { grid-column: 6 / 13; }
}
"""


# ------------------------------------------------------------------------------------------------ page pieces
def label_glyph(tex):
    """The evidence label's small line sample: the texture of the weakest step the headline rests on."""
    da, cap = fitted(tex, 2, 36)
    dash = f' stroke-dasharray="{da}" stroke-linecap="{cap}"' if da else ''
    return (f'<svg width="40" height="10" viewBox="0 0 40 10" aria-hidden="true" focusable="false">'
            f'<path d="M2 5H38" stroke="currentColor" stroke-width="2" fill="none"{dash}/></svg>')


def evidence_label(text_, tex):
    return f'<p class="t-eyebrow label">{label_glyph(tex)}<span>{e(text_)}</span></p>'


def key_rows():
    rows = []
    for g in ('documented', 'plausible', 'plausible_contested', 'hypothesis'):
        word = 'Documented or well supported' if g == 'documented' else grade_word(g)
        if g == 'hypothesis':
            word = 'Hypothesis, untested'
        da, cap = fitted(tex_of(g), 2, 32)
        dash = f' stroke-dasharray="{da}" stroke-linecap="{cap}"' if da else ''
        rows.append(f'<li><svg width="36" height="8" viewBox="0 0 36 8" aria-hidden="true" focusable="false">'
                    f'<path d="M2 4H34" stroke="currentColor" stroke-width="2" fill="none"{dash}/></svg>{e(word)}</li>')
    return '<ul class="keyrows">' + ''.join(rows) + '</ul>'


def close_key(loc, body):
    return (f'<div class="ckey"><a class="loc" href="#overview" aria-label="Back to the overview">{loc}</a>'
            f'<div class="howto"><h2 class="t-eyebrow">How to read this drawing</h2>{body}</div></div>{key_rows()}')


def overview_section():
    art, ring_words = overview_wide()
    narrow = overview_narrow()
    l08, l25 = L['L08'], L['L25']
    grades = f'{grade_word(l08["evidence"]).lower()} and {grade_word(l25["evidence"]).lower()}'
    head = 'In a safe seat, officials answer to the primary.'
    deck = ('With little threat in November, they may then write election rules that keep the seat safe. '
            f'That loop is one of {cnt("loops", len(LO))} in this map of who officials answer to.')
    howto = (f'<div class="howto"><h2 class="t-eyebrow">How to read this map</h2>'
             f'<p>Each box is an area. In the five core areas each dot is a condition that can rise or fall; the map holds '
             f'{cnt("variables", COUNTS["variables"])} in {cnt("areas", len(AREAS))} areas. A large number counts the connections between two areas, '
             f'and its arrowheads show which way they run.</p>'
             f'{key_rows()}<p>{e(acc.SIGN_RULE)}</p></div>')
    words = []
    for aid in [a['id'] for a in M['areas']]:
        a = AREAS[aid]
        n = len(a['nodes'])
        link = f'<a href="#area-c">Open area C</a>' if aid == 'C' else ''
        letter = aid if len(aid) <= 2 else ''
        words.append(f'<li><strong>{e((letter + " ") if letter else "")}{e(a["title"])}</strong>{e(a["text"])}'
                     f'<span class="n">{cnt("variables_" + aid, n)} conditions · {len(touching(aid))} connections touch it</span>{link}</li>')
    return f'''
<section data-view-root="overview" data-crumb="Overview" aria-labelledby="h-overview" class="view">
  <div class="lede g12">
    <div class="lede-main">
      {evidence_label('Causal claim · ' + grades, 'solid')}
      <h1 class="t-display" id="h-overview" data-ak-heading>{e(head)}</h1>
      <p class="t-deck">{deck}</p>
    </div>
    <div class="lede-key">{howto}</div>
  </div>
  <figure class="fig">
    {art}{narrow}
    <figcaption class="ak-readout" data-ak-readout>Point at or tab to an area to read it here. Area C and loop R10 open their close-ups.</figcaption>
  </figure>
  <section class="words" aria-labelledby="h-areas">
    <h2 class="t-eyebrow" id="h-areas">The ten areas in words</h2>
    <ul class="arealist">{''.join(words)}</ul>
    <h3 class="t-eyebrow" style="margin:28px 0 8px">Between the five core areas</h3>
    <ul class="ringwords">{''.join(f'<li>{e(w)}</li>' for w in ring_words)}</ul>
  </section>
  {strip_html()}
</section>'''


def overview_narrow():
    """The phone artboard: the ring stacked as panels in ring order, with the return path drawn down the left edge,
    then area C's R10 at reading size. Text keeps its size; the notes move below the drawing."""
    W = 350
    ch = 52                      # left channel for the return path
    bx0, bw = ch, W - ch
    out = []
    xa = AREAS['X']
    xs = wrap(f'{len(xa["nodes"])} conditions the model takes as given send {len(X_LINKS)} connections into the system, '
              f'{X_TO.get("A", 0)} of them into A and {X_TO.get("B", 0)} into B.', W - 28, 15)
    xh = 34 + 21 * len(xs) + 8
    xname = f'Area X, {xa["title"]}. {xa["text"]} {len(xa["nodes"])} variables.'
    out.append(f'<g class="blk tier" role="button" data-select="area-x" aria-label="{e(xname)}" data-say="{e(xname)}">'
               f'<rect class="ak-mark" x=".5" y=".5" width="{W - 1}" height="{xh - 1}" stroke-width="1"/>'
               f'<text x="14" y="25" class="s-map ak-label">{e(xa["title"])}</text>{lines(14, 47, xs, "s-cap s-dim", 21)}</g>')
    y = xh + 28
    order = ['A', 'B', 'C', 'D', 'E']
    rows_y = {'A': [62, 88, 114], 'B': [62, 88, 114], 'C': [70, 108, 146], 'D': [62, 88], 'E': [62, 88]}
    heights = {'A': 132, 'B': 158, 'C': 168, 'D': 106, 'E': 106}
    boxes = {}
    for k, aid in enumerate(order):
        a = AREAS[aid]
        h = heights[aid]
        b = Block(aid, bx0, y, bw, h, rows_y[aid])
        boxes[aid] = b
        name = f'Area {aid}, {a["title"]}. {a["text"]} {len(a["nodes"])} variables.'
        dots = ''
        for v in a['nodes']:
            x_, y_ = b.slot((PLAN['variables'][v]['x'], PLAN['variables'][v]['y']))
            dots += f'<circle class="dot" cx="{f(x_)}" cy="{f(y_)}" r="3.5"/>'
        head = (f'<text x="{f(b.x + 14)}" y="{f(b.y + 30)}" class="s-stationp ak-label"><tspan class="lt">{aid}</tspan>'
                f'<tspan x="{f(b.x + 34)}">{e(a["title"])}</tspan></text>')
        extra = ''
        if aid == 'B':
            extra = text(b.x + 14, b.y + h - 14, f'Also {both("B", "D")} with D, both ways, and {PAIRS.get(("B", "E"), 0)} to E.', 's-cap s-dim')
        if aid == 'C':
            rect = f'<rect class="ak-mark" x="{f(b.x + 1)}" y="{f(b.y + 1)}" width="{f(b.w - 2)}" height="{f(b.h - 2)}" stroke-width="2"/>'
            route = route_marks('R10', lambda p, b=b: b.slot(p), w=2.0)
            out.append(f'<a class="blk cl" href="#area-c" aria-label="{e(name)} Opens the close-up." data-say="{e(name)} Opens the close-up.">'
                       f'{rect}{head}{dots}<g class="rt ov">{route}</g></a>')
        else:
            rect = f'<rect class="ak-mark" x="{f(b.x + .5)}" y="{f(b.y + .5)}" width="{f(b.w - 1)}" height="{f(b.h - 1)}" stroke-width="1"/>'
            out.append(f'<g class="blk" role="button" data-select="area-{aid.lower()}" aria-label="{e(name)}" data-say="{e(name)}">'
                       f'{rect}{head}{dots}{extra}</g>')
        y += h + (56 if k < len(order) - 1 else 0)

    def vbundle(a, b, x):
        ab, ba = PAIRS.get((a, b), 0), PAIRS.get((b, a), 0)
        y0_, y1_ = boxes[a].y + boxes[a].h + 2, boxes[b].y - 2
        q0, q1 = y0_, y1_
        heads = ''
        if ab:
            heads += head_shape(x, y1_, 0, 1, 2, '')
            q1 -= 10
        if ba:
            heads += head_shape(x, y0_, 0, -1, 2, '')
            q0 += 10
        return (f'<g class="bun" aria-hidden="true"><path class="bl" d="M{f(x)} {f(q0)}V{f(q1)}"/>{heads}'
                f'<text class="s-figp" x="{f(x + 12)}" y="{f((y0_ + y1_) / 2 + 12)}">{ab + ba}</text></g>')
    cx = bx0 + bw / 2
    for a, b in zip(order, order[1:]):
        out.append(vbundle(a, b, cx))
    # the return path, E back to A, down the left edge
    ea = PAIRS.get(('E', 'A'), 0) + PAIRS.get(('A', 'E'), 0)
    ya, ye = boxes['A'].y + boxes['A'].h / 2, boxes['E'].y + boxes['E'].h / 2
    rx = 16
    out.append(f'<g class="bun" aria-hidden="true"><path class="bl" d="M{bx0 - 2} {f(ye)}H{rx + 8}Q{rx} {f(ye)} {rx} {f(ye - 8)}V{f(ya + 8)}Q{rx} {f(ya)} {rx + 8} {f(ya)}H{bx0 - 12}"/>'
               f'{head_shape(bx0 - 2, ya, 1, 0, 2, "")}<text class="s-figp" x="{rx + 8}" y="{f((ya + ye) / 2 + 12)}">{ea}</text></g>')
    y = boxes['E'].y + boxes['E'].h + 24
    gw, gh, gg = (W - 12) / 2, 54, 12
    for i, aid in enumerate(('money', 'household', 'production', 'TC')):
        gx, gy = (i % 2) * (gw + gg), y + (i // 2) * (gh + gg)
        a = AREAS[aid]
        rows = wrap(a['title'], gw - 24, 15, 600)
        name = f'{a["title"]}. {a["text"]} {len(a["nodes"])} variables.'
        out.append(f'<g class="blk tier" role="button" data-select="area-{aid.lower()}" aria-label="{e(name)}" data-say="{e(name)}">'
                   f'<rect class="ak-mark" x="{f(gx + .5)}" y="{f(gy + .5)}" width="{f(gw - 1)}" height="{gh - 1}" stroke-width="1"/>'
                   + lines(gx + 12, gy + (23 if len(rows) > 1 else 32), rows, 's-map ak-label', 18) + '</g>')
    y += 2 * gh + gg + 26
    for sent in (f'Economy: three areas, {ECON_VARS} conditions. {len(ECON_LINKS)} connections touch them, {len(ECON_WITH_A)} of them with A.',
                 f'Technology: {len(AREAS["TC"]["nodes"])} conditions. {len(TECH_LINKS)} connections touch them, {len(TECH_WITH_D)} of them with D.'):
        rws = wrap(sent, W, 15)
        out.append(lines(0, y, rws, 's-cap s-dim', 21))
        y += 21 * len(rws) + 6
    H = y
    ring = (f'<svg class="art art-narrow" data-view="overview" viewBox="0 0 {W} {f(H)}" role="group" aria-labelledby="h-overview" '
            f'data-ak-roving data-ak-nav="spatial">{"".join(out)}</svg>')
    ins_h = 500
    inset = (f'<svg class="art art-narrow inset-n" data-view="overview" viewBox="0 0 {W} {ins_h}" role="group" aria-label="Inside area C: loop R10" '
             f'data-ak-roving data-ak-nav="spatial"><rect class="inset" x=".5" y=".5" width="{W - 1}" height="{ins_h - 1}"/>'
             f'{inset_r10(0, 0, W, ins_h, S=100, x0=112, y0=176, narrow=True)}</svg>')
    notes = (f'<ol class="phone-notes"><li>Start at Safe seats, then follow the arrows. Each step raises or lowers the next.</li>'
             f'<li>The weakest step, {LO["R10"]["weakest"][0]}, is graded {grade_word(L[LO["R10"]["weakest"][0]]["evidence"]).lower()}.</li></ol>')
    return ring + inset + notes


# ------------------------------------------------------------------------------------------------ area C, wide artboard
PILL = (56, 30)
DIRS = {'E': (1, 0), 'W': (-1, 0), 'N': (0, -1), 'S': (0, 1), 'NE': (1, -1), 'NW': (-1, -1), 'SE': (1, 1), 'SW': (-1, 1)}


def node(vid, x, y, ctx=False, label_rows=None, lx=None, ly=None, anchor='start', cls='s-station', lh=22, interactive=True, eyebrow=None):
    n = N[vid]
    w, h = PILL
    say = f'{vid} {n["label"]}. {n["increase_means"]}'
    rows = label_rows or [n['label']]
    lab = lines(lx, ly, rows, f'{cls} ak-label' + (' s-ctx' if ctx else ''), lh, anchor,
                extra=f' data-node="{vid}" data-name="{e(n["label"])}"')
    eb = text(x - w / 2 - 12, y + 5, eyebrow, 's-eye s-ctx', 'end') if eyebrow else ''
    rel = ' '.join(sorted({f'link-{l["id"].lower()}' for l in L.values() if vid in (l['from'], l['to'])}))
    body = (f'<rect class="ak-mark" x="{f(x - w / 2)}" y="{f(y - h / 2)}" width="{w}" height="{h}" rx="{h / 2}" stroke-width="2"/>'
            f'<text class="code" x="{f(x)}" y="{f(y + 5)}" text-anchor="middle">{vid}</text>{lab}{eb}')
    c = 'nd ctx' if ctx else 'nd'
    if not interactive:
        return f'<g class="{c}" data-node="{vid}">{body}</g>'
    return (f'<g class="{c}" role="button" data-select="var-{vid.lower()}" data-node="{vid}" data-rel="{rel}" '
            f'aria-label="{e(say)}" data-say="{e(say)}">{body}</g>')


def stub(lid, at, d, length, lab_anchor='end', lab_dx=0, lab_dy=0, offset=0, bend=None, tag_at=0.55, label=True, both=None):
    """A connection crossing the area's edge, drawn in Stone from (or to) its C variable. The far end is named with the
    verb, so the sign reads in words too: 'raises B4 Affective polarization' or 'raised by X2 ...'."""
    l = L[lid]
    ux, uy = unit(*DIRS[d])
    vx, vy = -uy, ux
    cx, cy = at
    if offset and uy == 0:
        r = PILL[1] / 2
        ex = PILL[0] / 2 - r + math.sqrt(max(0.0, r * r - offset * offset))
        base = (cx + ux * (ex + 2), cy + vy * offset)
    else:
        r0 = pill_edge(ux, uy, *PILL) + 2
        base = (cx + ux * r0 + vx * offset, cy + uy * r0 + vy * offset)
    far = (base[0] + ux * length, base[1] + uy * length)
    pts = [base, far]
    if bend:
        bx, by = unit(*DIRS[bend[0]])
        far = (far[0] + bx * bend[1], far[1] + by * bend[1])
        pts = [base, pts[1], far]
    inside = l['from'] in AREAS['C']['nodes']
    line = pts if inside else list(reversed(pts))
    other = l['to'] if inside else l['from']
    past = {'+': 'raised by', '-': 'lowered by'}
    far_name = f'{other} {N[other]["label"]}, area {AREA_OF[other]}'
    if both:
        back = next(x for x in L.values() if x['from'] == other and x['to'] == l['from'])
        words = f'{verb(l["polarity"]).capitalize()} and is {past[back["polarity"]]} {far_name}'
    elif inside:
        words = f'{verb(l["polarity"]).capitalize()} {far_name}'
    else:
        words = f'{past[l["polarity"]].capitalize()} {far_name}'
    lab = text(far[0] + lab_dx, far[1] + lab_dy, words, 's-map s-ctx', lab_anchor) if label else ''
    return wire(lid, line, w=2, ctx=True, tag_at=tag_at, label=lab)


def area_wide():
    W = OVW
    x0, y0, S = 560, 44, 220
    pos = {'C2': (x0, y0), 'C3': (x0, y0 + S), 'C1': (x0 + S, y0 + S), 'C4': (x0 + S, y0 + 2 * S), 'C5': (x0, y0 + 2 * S),
           'D5': (x0 - S, y0 + 2 * S)}
    out = []
    route = {'L08': ('C1', 'C2', (24, -14, 'start')), 'L25': ('C2', 'C3', (16, 5, 'start')),
             'L53': ('C3', 'C4', (42, 78, 'end')), 'L42': ('C4', 'C1', (22, 5, 'start')),
             'L23': ('D5', 'C3', (-20, -12, 'end')), 'L24': ('C3', 'C5', (16, 26, 'start')),
             'L54': ('C5', 'D5', (0, -12, 'middle'))}
    for lid, (a, b, (dx, dy, anc)) in route.items():
        pts = edge_pts(pos[a], pos[b], *PILL, *PILL)
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        l = L[lid]
        lab = (f'<text x="{f(mx + dx)}" y="{f(my + dy)}" class="s-map ak-label" text-anchor="{anc}">{lid} '
               f'<tspan class="s-cap s-dim">{verb(l["polarity"])}</tspan></text>')
        out.append(wire(lid, pts, w=3, rel=f'var-{a.lower()} var-{b.lower()}', label=lab))
    b2 = 'Both ways with'
    spec = [
        # lid, at, dir, length, anchor, dx, dy, offset, bend, tag_at, label
        ('L09', 'C2', 'W', 104, 'end', -10, 5, 0, None, 0.5, True, None),
        ('LX2', 'C1', 'N', 92, 'start', 12, -4, 0, None, 0.5, True, None),
        ('T04', 'C1', 'E', 120, 'start', 10, 5, 0, None, 0.5, True, None),
        ('L55', 'C1', 'SE', 80, 'start', 10, 12, 0, None, 0.5, True, None),
        ('T01', 'C3', 'W', 112, 'end', -10, 13, -8, None, 0.32, True, 'pair'),
        ('L26', 'C3', 'W', 112, 'end', -10, 13, 8, None, 0.72, False, None),
        ('L50', 'C3', 'NW', 96, 'end', -8, -4, 7, None, 0.5, True, None),
        ('L51', 'C3', 'NW', 44, 'end', -10, 5, -7, ('W', 76), 0.82, True, None),
        ('L44', 'C4', 'E', 84, 'start', 10, 13, -8, None, 0.32, True, 'pair'),
        ('L45', 'C4', 'E', 84, 'start', 10, 5, 8, None, 0.72, False, None),
        ('L56', 'C4', 'SE', 66, 'start', 10, 4, 0, None, 0.5, True, None),
        ('T05', 'C4', 'S', 70, 'start', 12, 30, 0, None, 0.5, True, None),
        ('L06', 'C4', 'SW', 66, 'end', -10, 26, 0, None, 0.5, True, None),
    ]
    for lid, at, d, ln, anc, dx, dy, off, bend, ta, lab, both in spec:
        out.append(stub(lid, pos[at], d, ln, anc, dx, dy, off, bend, ta, lab, both))
    r10, b4 = LO['R10'], LO['B4']
    out.append(f'<g class="loopname" aria-hidden="true">{text(x0 + S * 0.62, y0 + S * 1.22, "R10", "s-head", "middle")}'
               f'{text(x0 + S * 0.62, y0 + S * 1.22 + 20, r10["kind_gloss"], "s-cap s-dim", "middle")}</g>')
    out.append(f'<g class="loopname" aria-hidden="true">{text(x0 - S * 0.33, y0 + S * 1.6, "B4", "s-head", "middle")}'
               f'{text(x0 - S * 0.33, y0 + S * 1.6 + 20, b4["kind_gloss"], "s-cap s-dim", "middle")}</g>')
    out.append(node('C2', *pos['C2'], lx=x0 + 44, ly=y0 + 7))
    out.append(node('C1', *pos['C1'], lx=x0 + S + 16, ly=y0 + S - 30))
    out.append(node('C3', *pos['C3'], label_rows=wrap(N['C3']['label'], 120, 20, 700, True), lx=x0 + 36, ly=y0 + S + 1))
    out.append(node('C4', *pos['C4'], label_rows=wrap(N['C4']['label'], 210, 20, 700, True), lx=x0 + S + 16, ly=y0 + 2 * S - 52))
    out.append(node('C5', *pos['C5'], lx=x0, ly=y0 + 2 * S + 48, anchor='middle'))
    out.append(node('D5', *pos['D5'], lx=x0 - S, ly=y0 + 2 * S + 48, anchor='middle', eyebrow='Area D'))
    # notes on fine leader lines
    q = first_sentence(b4['qualification']).replace('The loop', 'B4')
    nr = wrap(q, 170, 15)
    ny = y0 + S + 136
    ly_ = ny + 5
    lx_ = x0 - S + (y0 + 2 * S - ly_)      # where L23 crosses the note's middle line
    out.append(lines(lx_ - 40, ny - 10, nr, 's-note', 21, anchor='end'))
    out.append(leader([(lx_ - 34, ly_ - 4), (lx_ - 6, ly_ - 4)]))
    H = y0 + 2 * S + 140
    return (f'<svg class="art art-wide" data-view="area-c" viewBox="0 0 {W} {H}" role="group" aria-labelledby="h-area-c" '
            f'data-ak-roving data-ak-nav="spatial">{"".join(out)}</svg>')


def loop_card(k):
    lp = LO[k]
    steps = 'sketch' if lp['conceptual'] else ' '.join(s['id'] for s in lp['steps'])
    th = thumb_svg(k, 310, view='loop-route')
    head_ = (f'{th}<span class="lp-k"><span class="lp-id">{k}</span> {e(kind_line(k))}</span>'
             f'<span class="lp-t">{e(lp["title"])}</span>')
    say = f'Loop {k}, {kind_line(k)}: {lp["title"]}.'
    if k == 'R10':
        hit = (f'<a class="lp-hit" href="#loop-r10" aria-label="{e(say)} Opens the close-up." data-say="{e(say)} Opens the close-up.">'
               f'{head_}<span class="lp-go">Open the close-up <span aria-hidden="true">→</span></span></a>')
    else:
        hit = f'<button type="button" class="lp-hit" data-select="loop-{k.lower()}" aria-label="{e(say)}" data-say="{e(say)}">{head_}</button>'
    return (f'<li class="lp" data-loop="{k}" data-steps="{steps}">{hit}<p class="lp-s">{e(first_sentence(lp["summary"]))}</p>'
            f'<p class="lp-r">{e(read_aloud(k))}</p><p class="lp-m">{e(status_line(k))}</p></li>')


def area_section():
    art = area_wide()
    narrow = area_narrow()
    r10 = LO['R10']
    head = 'At electoral pressure, a loop that pushes back meets one that feeds itself.'
    deck = ('Where seats are competitive, poor service raises an incumbent’s risk of losing, defeats follow, and the officials '
            'who remain do better. Safe seats drain that pressure, and the officials they protect may write the rules that keep them safe.')
    lab = f'Two causal loops · B4 well supported, R10 {grade_word(L[r10["weakest"][0]]["evidence"]).lower()} at its weakest step'
    defs = ''.join(f'<li>{chip("Variable", v, True)}<strong>{e(N[v]["label"])}</strong><span>{e(N[v]["increase_means"])}</span></li>'
                   for v in AREAS['C']['nodes'])
    words = ''.join(f'<li>{e(link_sentence(l))}</li>' for l in sorted(C_LINKS, key=lambda l: (l['from'] not in AREAS['C']['nodes'], l['id'])))
    cards = ''.join(loop_card(k) for k in LOOPS_C)
    others = [k for k in LOOPS_THROUGH_C if k not in LOOPS_C]
    other_txt = ', '.join(f'{k}, {LO[k]["title"]}' for k in others)
    howto = close_key(locator_svg(area='C'),
                      '<p>Each pill is a variable. Dark lines are the two loops named above; Stone lines cross the area\u2019s edge and name '
                      'the variable at the far end. A tag carries the sign, and ticks after the start count the delay: one tick under 2 years, '
                      'two for 2 to 10, three for longer.</p>')
    return f'''<section data-view-root="area-c" data-crumb="Area C, {e(AREAS["C"]["title"])}" data-parent="overview" aria-labelledby="h-area-c" class="view" hidden>
  <div class="lede g12">
    <div class="lede-main">
      {evidence_label(lab, 'dashed')}
      <h1 class="t-headline" id="h-area-c" data-ak-heading>{e(head)}</h1>
      <p class="t-deck">{e(deck)}</p>
    </div>
    <div class="lede-key">{howto}</div>
  </div>
  <figure class="fig">
    <p class="scroll-hint t-caption dim">The drawing keeps its full size here. Slide it sideways, or open it full size below.</p>
    <div class="ak-scroll wide-scroll" id="map-area-c" role="region" tabindex="0" aria-label="Area C drawing, scrolls sideways on a narrow screen" style="--ak-min: 1312px; --ak-full-w: 1312px">{art}</div>
    <button type="button" class="ak-btn full-btn" data-ak-full="map-area-c">View the drawing full size</button>
    <figcaption class="ak-readout" data-ak-readout>Point at or tab to a variable or a connection to read it here. Select one to open its record.</figcaption>
  </figure>
  <section class="defs" aria-labelledby="h-defs">
    <h2 class="t-eyebrow" id="h-defs">The {cnt("variables_C", len(AREAS["C"]["nodes"]))} variables in area C, and what a higher value means</h2>
    <ul class="deflist">{defs}</ul>
  </section>
  <section class="lg area-loops" aria-labelledby="h-cloops">
    <header class="lg-h"><p class="t-eyebrow">Area C’s loops</p><h2 class="t-panelhead" id="h-cloops">{nw(len(LOOPS_C), True)} loops grouped under area C</h2>
    <p class="lg-t">{nw(len(LOOPS_THROUGH_C), True)} loops pass through it in all. The other {nw(len(others))} are grouped under other areas: {e(other_txt)}.</p></header>
    <ul class="lp-grid" data-ak-roving data-ak-nav="sequence" aria-label="Loops grouped under area C">{cards}</ul>
  </section>
  <section class="words" aria-labelledby="h-cwords">
    <h2 class="t-eyebrow" id="h-cwords">The lines in words: all {cnt("custom:connections-touching-c", len(C_LINKS))} connections that touch area C</h2>
    <p class="t-caption dim" style="margin:6px 0 0">{len(C_INSIDE)} run inside the area, {len(C_IN)} arrive from other areas and {len(C_OUT)} leave for them.</p>
    <ol class="linewords">{words}</ol>
  </section>
</section>'''


def area_narrow():
    return ''


# ------------------------------------------------------------------------------------------------ loop R10
def r10_steps():
    """Per step: the more-or-less words multiplied out from the signs."""
    lp = LO['R10']
    d = 1
    out = []
    for st in lp['steps']:
        before = 'More' if d > 0 else 'Less'
        d *= 1 if st['polarity'] == '+' else -1
        after = 'more' if d > 0 else 'less'
        out.append((st, before, after))
    return out


def r10_wide(W=866):
    lp = LO['R10']
    x0, y0, S = 316, 168, 250
    pos = {'C2': (x0, y0), 'C3': (x0, y0 + S), 'C1': (x0 + S, y0 + S), 'C4': (x0 + S, y0 + 2 * S)}
    out = []
    steps = r10_steps()
    # step labels sit on the outside of each edge
    place = {
        'L08': (x0 + S / 2 + 34, y0 + S / 2 - 58, 'start'),
        'L25': (x0 - 24, y0 + S / 2 - 22, 'end'),
        'L53': (x0 + S / 2 - 34, y0 + 1.5 * S + 40, 'end'),
        'L42': (x0 + S + 24, y0 + 1.5 * S - 22, 'start'),
    }
    items = []
    for st, before, after in steps:
        lid = st['id']
        a, b = pos[st['from']], pos[st['to']]
        pts = edge_pts(a, b, *PILL, *PILL)
        lx, ly, anc = place[lid]
        g = grade_word(st['evidence'])
        rows = [(f'{st["index"]}', 's-eye'), (st['name'], 's-map'),
                (f'{verb(st["polarity"]).capitalize()} · {g}, {grade_gloss(st["evidence"])}', 's-cap s-dim'),
                (delay_words(st['delay']).capitalize() + (' · the weakest step' if lid in lp['weakest'] else ''), 's-cap s-dim')]
        width = 286
        name_rows = wrap(st['name'], width, 15, 600)
        lab = [f'<text x="{f(lx)}" y="{f(ly)}" class="s-eye" text-anchor="{anc}">Step {st["index"]} · {lid}</text>']
        yy = ly + 22
        for r in name_rows:
            lab.append(f'<text x="{f(lx)}" y="{f(yy)}" class="s-map ak-label" text-anchor="{anc}">{e(r)}</text>')
            yy += 19
        # the verb sits first, beside the sign it reads out; then the grade with its gloss, then the delay
        lab.append(f'<text x="{f(lx)}" y="{f(yy + 2)}" class="s-cap s-dim" text-anchor="{anc}"><tspan class="s-noteb vb">'
                   f'{sign_char(st["polarity"])} {verb(st["polarity"])}</tspan> · {e(delay_words(st["delay"]))}</text>')
        yy += 20
        tail = f'{g}: {grade_gloss(st["evidence"])}'
        room = (lx - 8) if anc == 'end' else (W - lx - 8)
        for k_, r in enumerate(wrap(tail, min(width, room), 15)):
            if k_:
                yy += 20
            lab.append(f'<text x="{f(lx)}" y="{f(yy + 2)}" class="s-cap s-dim" text-anchor="{anc}">{e(r)}</text>')
        if lid in lp['weakest']:
            yy += 20
            lab.append(f'<text x="{f(lx)}" y="{f(yy + 2)}" class="s-noteb" text-anchor="{anc}">The weakest step</text>')
        items.append((st['from'], wire(lid, pts, w=3, rel=f'var-{st["from"].lower()} var-{st["to"].lower()}', label=''.join(lab))))
    # stations: label, then what a higher value means
    spot = {
        'C2': (x0 - 44, y0 - 4, 'end'), 'C3': (x0 - 44, y0 + S - 4, 'end'),
        'C1': (x0 + S + 44, y0 + S - 4, 'start'), 'C4': (x0 + S + 44, y0 + 2 * S - 4, 'start'),
    }
    nodes = {}
    for v, (lx, ly, anc) in spot.items():
        rows = wrap(N[v]['label'], 230, 20, 700, True)
        means = wrap(N[v]['increase_means'], 236, 15)
        extra = ''.join(f'<text x="{f(lx)}" y="{f(ly + 22 * (len(rows) - 1) + 24 + 20 * i)}" class="s-cap s-dim" text-anchor="{anc}">{e(m)}</text>'
                        for i, m in enumerate(means))
        nodes[v] = node(v, *pos[v], label_rows=rows, lx=lx, ly=ly, anchor=anc).replace('</g>', extra + '</g>', 1)
    # roving order walks the loop: C1, L08, C2, L25, C3, L53, C4, L42
    seq = []
    for v, wire_svg in items:
        seq.append(nodes[v])
        seq.append(wire_svg)
    out.extend(seq)
    # the loop's name in its middle, and the more-or-less words that appear as the story reaches each station
    cx, cy = x0 + S / 2, y0 + S + 4
    out.append(f'<g aria-hidden="true">{text(cx, cy - 6, "R10", "s-head", "middle")}{text(cx, cy + 16, lp["kind_gloss"], "s-cap s-dim", "middle")}</g>')
    mk = {'C2': (x0 + 36, y0 - 12, 'start'), 'C3': (x0 + 36, y0 + S + 22, 'start'), 'C4': (x0 + S, y0 + 2 * S + 40, 'middle')}
    start = steps[0][0]['from']
    c1x, c1y = x0 + S + 44, y0 + S - 34 - 22 * (len(wrap(N['C1']['label'], 230, 20, 700, True)) - 1)
    out.append(f'<text class="s-noteb mk" data-at="0" data-to="{len(steps) - 1}" x="{f(c1x)}" y="{f(c1y)}">Start: more</text>')
    for st, before, after in steps:
        if st['to'] == start:
            out.append(f'<text class="s-noteb mk" data-at="{st["index"]}" data-rest="0" hidden x="{f(c1x)}" y="{f(c1y)}">{after.capitalize()} again</text>')
        else:
            x, y, anc = mk[st['to']]
            out.append(f'<text class="s-noteb mk" data-at="{st["index"]}" x="{f(x)}" y="{f(y)}" text-anchor="{anc}">{after.capitalize()}</text>')
    # where R-01 acts: a note, the marks themselves take the working red from the kit
    r01 = RF['R-01']
    nrows = wrap(f'All-party primaries, reform R-01, act here: on the primary and the two steps through it.', 340, 15)
    ny = y0 - 112
    out.append(lines(x0 + 20, ny, nrows, 's-note', 21))
    out.append(leader([(x0 + 12, ny - 5), (x0, ny - 5), (x0, y0 - 19)]))
    H = y0 + 2 * S + 92
    return (f'<svg class="art art-wide r10-art" data-view="loop-r10" viewBox="0 0 {W} {H}" role="group" aria-labelledby="h-loop-r10" '
            f'data-ak-roving data-ak-nav="sequence" data-ak-wrap>{"".join(out)}</svg>')


def r10_narrow(W=350):
    """The phone artboard: the same four stations and steps, numbered; each step's words move into the story below."""
    lp = LO['R10']
    x0, y0, S = 116, 50, 112
    pos = {'C2': (x0, y0), 'C3': (x0, y0 + S), 'C1': (x0 + S, y0 + S), 'C4': (x0 + S, y0 + 2 * S)}
    num = {'L08': (16, -14, 'start'), 'L25': (-14, 6, 'end'), 'L53': (-12, 22, 'end'), 'L42': (14, 6, 'start')}
    items = []
    for st, before, after in r10_steps():
        lid = st['id']
        a, b = pos[st['from']], pos[st['to']]
        pts = edge_pts(a, b, *PILL, *PILL)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy, anc = num[lid]
        lab = f'<text x="{f(mx + dx)}" y="{f(my + dy)}" class="s-map ak-label" text-anchor="{anc}">{st["index"]} · {lid}</text>'
        items.append((st['from'], wire(lid, pts, w=3, rel=f'var-{st["from"].lower()} var-{st["to"].lower()}', label=lab)))
    spot = {'C2': (x0 + 40, y0 + 6, 'start', 200), 'C3': (x0 - 40, y0 + S - 4, 'end', 74),
            'C1': (x0 + S + 40, y0 + S - 4, 'start', 74), 'C4': (W - 4, y0 + 2 * S + 40, 'end', 230)}
    nodes = {}
    for v, (lx, ly, anc, wd) in spot.items():
        rows = wrap(N[v]['label'], wd, 18, 700, True)
        nodes[v] = node(v, *pos[v], label_rows=rows, lx=lx, ly=ly, anchor=anc, cls='s-stationp', lh=20)
    out = []
    for v, w_ in items:
        out.append(nodes[v])
        out.append(w_)
    H = y0 + 2 * S + 90
    return (f'<svg class="art art-narrow r10-art" data-view="loop-r10" viewBox="0 0 {W} {H}" role="group" aria-labelledby="h-loop-r10" '
            f'data-ak-roving data-ak-nav="sequence" data-ak-wrap>{"".join(out)}</svg>')


def loop_section():
    lp = LO['R10']
    steps = r10_steps()
    weakest = lp['weakest'][0]
    lab = f'Loop R10 · {kind_line("R10")} · {grade_word(L[weakest]["evidence"]).lower()} at its weakest step'
    grades = [grade_word(st['evidence']).lower() for st, _, _ in steps]
    strong = sum(1 for st, _, _ in steps if st['evidence'] in ('documented', 'well-supported'))
    deck = (f'{nw(strong, True)} of its {nw(len(steps))} steps are documented or well supported. The weakest, {weakest}, is graded '
            f'{grade_word(L[weakest]["evidence"]).lower()}, so the loop holds only as firmly as that step. '
            f'One turn takes {lp["delay_word"]}.')
    blocks = []
    first = steps[0][0]
    blocks.append(f'<div class="story-step" data-story="0"><p class="t-eyebrow">Read it aloud</p>'
                  f'<p class="aloud">{e(read_aloud("R10"))}</p>'
                  f'<p class="story-lead">{e(lp["summary"])}</p>'
                  f'<p>Start at {first["from"]}, {e(N[first["from"]]["label"])}, and suppose it rises. {e(N[first["from"]]["increase_means"])} '
                  f'Scroll, and the drawing follows one numbered step at a time.</p></div>')
    for st, before, after in steps:
        lid = st['id']
        keys = f'link-{lid.lower()} var-{st["to"].lower()}'
        weak = ''
        if lid in lp['weakest']:
            weak = (f'<p class="story-flag">The weakest step. {e(grade_word(st["evidence"]))} means {e(grade_gloss(st["evidence"]))}, '
                    f'so the whole loop is only as sure as this link.</p>')
        end = ''
        if st['closing']:
            end = (f'<p>The loop is back where it started, so it {e(lp["kind_gloss"])}: {e(lp["kind_word"].lower())}. '
                   f'Read the whole chain aloud: {e(read_aloud("R10"))}</p>')
        acts = [r for r in lp['reforms'] if lid in RF[r]['targets']]
        act = ''
        if acts:
            act = f'<p class="story-act">Reform {", ".join(acts)} acts on this step.</p>'
        blocks.append(
            f'<div class="story-step" data-story="{st["index"]}" data-keys="{keys}"><p class="t-eyebrow">Step {st["index"]} of {len(steps)} · {chip("Connection", lid, True)}</p>'
            f'<h3 class="t-panelhead">{e(st["name"])}</h3>'
            f'<p>{before} {e(low(st["from_label"]))} means {after} {e(low(st["to_label"]))}.</p>'
            f'<p class="story-facts"><span>{sign_char(st["polarity"])} {verb(st["polarity"])}</span><span>{e(grade_word(st["evidence"]))}: {e(grade_gloss(st["evidence"]))}</span>'
            f'<span>{e(delay_words(st["delay"]).capitalize())}</span></p>{weak}{act}{end}</div>')
    refs = ''
    for r in lp['reforms']:
        rr = RF[r]
        targets = ' '.join(rr['targets'])
        in_view = [t for t in rr['targets'] if t in ('L08', 'L25', 'L53', 'L42', 'C1', 'C2', 'C3', 'C4')]
        refs += (f'<li><button type="button" class="ak-btn reform-btn" data-select="reform-{r.lower()}" data-reform="{r}" data-targets="{targets}" '
                 f'aria-label="Reform {r}, {e(rr["title"])}. Acts on {", ".join(rr["targets"])}." data-say="Reform {r}, {e(rr["title"])}.">'
                 f'{chip("Reform", r, True)} <span>{e(rr["title"])}</span></button>'
                 f'<span class="reform-at">Acts on {e(", ".join(in_view))}{" in this loop" if in_view else ""}'
                 f'{"; also " + ", ".join(t for t in rr["targets"] if t not in in_view) + " outside it" if len(in_view) < len(rr["targets"]) else ""}.</span></li>')
    blocks.append(f'<div class="story-step" data-story="{len(steps) + 1}"><p class="t-eyebrow">Where reforms act</p>'
                  f'<h3 class="t-panelhead">{len(lp["reforms"])} reforms aim at this loop</h3>'
                  f'<p>The red marks show where reform R-01, all-party primaries with ranked general elections, would act. '
                  f'Select another reform to move the red to its targets.</p>'
                  f'<ul class="reforms" data-ak-roving data-ak-nav="sequence" aria-label="Reforms aimed at loop R10">{refs}</ul>'
                  f'<p class="dim t-caption">{e(RF["R-01"]["summary"].split(". ")[-1])}</p></div>')
    blocks.append(f'<div class="story-step" data-story="{len(steps) + 2}"><p class="t-eyebrow">Keep in mind</p>'
                  f'<p>{e(lp["qualification"])}</p>'
                  f'<p>Now: {e(lp["direction_word"])}, measured by the {e(low(lp["reference_mode"]))}.</p></div>')
    words = ''.join(f'<li>{e(link_sentence(L[st["id"]]))}</li>' for st, _, _ in steps)
    return f'''<section data-view-root="loop-r10" data-crumb="Loop R10" data-parent="area-c" data-ak-reform="reform-r-01" aria-labelledby="h-loop-r10" class="view" hidden>
  <div class="lede g12">
    <div class="lede-main">
      {evidence_label(lab, 'dashed')}
      <h1 class="t-headline" id="h-loop-r10" data-ak-heading data-loop="R10" data-steps="{' '.join(s['id'] for s in lp['steps'])}" data-name="{e(lp['title'])}">{e(lp['title'])}</h1>
      <p class="t-deck">{e(deck)}</p>
    </div>
    <div class="lede-key">{close_key(locator_svg(lid='R10'), '<p>Each step names its connection, which way it pushes, its evidence and its delay. A tag carries the sign, and ticks count the delay. ' + e(acc.SIGN_RULE) + '</p>')}</div>
  </div>
  <div class="story g12" data-story-steps="{len(steps)}">
    <div class="story-text">{''.join(blocks)}</div>
    <figure class="story-art">{r10_wide()}{r10_narrow()}
      <figcaption class="ak-readout" data-ak-readout>Use the arrow keys to walk the loop one step at a time.</figcaption>
    </figure>
  </div>
  <section class="after g12" aria-labelledby="h-v7reads">
    <div class="after-q"><h2 class="t-eyebrow" id="h-v7reads">The model reads it this way</h2><blockquote class="t-quote">{e(lp['how_to_read'])}</blockquote></div>
    <div class="after-w"><h2 class="t-eyebrow">The steps in words</h2><ol class="linewords one">{words}</ol>
    <p class="t-caption dim">{e(lp['evidence_summary'])}</p></div>
  </section>
</section>'''


def templates():
    t = []
    for a in M['areas']:
        if a['id'] != 'C':
            t.append(tpl_area(a['id']))
    for k in M['loop_order']:
        if k != 'R10':
            t.append(tpl_loop(k))
    for v in ['C1', 'C2', 'C3', 'C4', 'C5', 'D5']:
        t.append(tpl_var(v))
    for l in C_LINKS:
        t.append(tpl_link(l['id']))
    for r in LO['R10']['reforms']:
        t.append(tpl_reform(r))
    return ''.join(t)


def kit():
    css = (acc.SHARED / 'atlas-kit.css').read_text()
    js = (acc.SHARED / 'atlas-kit.js').read_text()
    # One behavior-preserving change: a view here holds a wide and a narrow artboard of the same drawing, so a
    # selection lands on the copy the reader can see.
    old = 'const root = rootOf(S.view), item = key && $(`[data-select="${key}"]`, root);'
    new = 'const root = rootOf(S.view), item = key && ($$(`[data-select="${key}"]`, root).find(vis) || $(`[data-select="${key}"]`, root));'
    assert old in js
    js = js.replace(old, new)
    return css, js


CONCEPT_JS = r"""
(function () {
  'use strict';
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-tab]'));
  function mark() {
    var v = (window.AtlasKit && AtlasKit.state().view) || 'overview';
    tabs.forEach(function (t) { if (t.dataset.tab === v) t.setAttribute('aria-current', 'page'); else t.removeAttribute('aria-current'); });
  }
  // On a narrow screen the area drawing scrolls sideways; open it on the two loops, not on empty margin.
  function centre() {
    document.querySelectorAll('.wide-scroll').forEach(function (r) {
      if (r.scrollWidth > r.clientWidth + 1 && r.offsetParent) r.scrollLeft = Math.max(0, r.scrollWidth * 0.47 - r.clientWidth / 2);
    });
  }
  addEventListener('hashchange', function () { setTimeout(function () { mark(); centre(); }, 0); });
  mark(); centre();
  // R10 told in order as the reader scrolls. The drawing holds still beside the text; the step whose text sits in
  // the middle of the screen takes heavy ink, earlier steps stay ink, later steps step back to Stone. At rest, and
  // before the first step, the drawing shows the whole loop.
  var view = document.querySelector('[data-view-root="loop-r10"]');
  if (!view) return;
  var blocks = Array.prototype.slice.call(view.querySelectorAll('[data-story]'));
  var current = -1;
  function keysOf(k) { var b = blocks.filter(function (x) { return +x.dataset.story === k; })[0]; return b && b.dataset.keys ? b.dataset.keys.split(' ') : []; }
  var nSteps = +((view.querySelector('[data-story-steps]') || {}).dataset || {}).storySteps || 0;
  function set(k) {
    if (k === current) return; current = k;
    view.querySelectorAll('.ak-now, .ak-done').forEach(function (x) { x.classList.remove('ak-now', 'ak-done'); });
    var stepping = k >= 1 && k <= nSteps;
    view.classList.toggle('ak-stepping', stepping);
    if (stepping) {
      for (var j = 1; j <= k; j++) keysOf(j).forEach(function (key) {
        view.querySelectorAll('[data-select="' + key + '"]').forEach(function (x) { x.classList.add(j === k ? 'ak-now' : 'ak-done'); });
      });
      view.querySelectorAll('.ak-now').forEach(function (x) { x.classList.remove('ak-done'); });
    }
    view.querySelectorAll('[data-at]').forEach(function (m) {
      var to = m.dataset.to === undefined ? 99 : +m.dataset.to;
      var show = stepping ? (+m.dataset.at <= k && k <= to) : m.dataset.rest !== '0';
      if (show) m.removeAttribute('hidden'); else m.setAttribute('hidden', '');
    });
    blocks.forEach(function (b) { b.classList.toggle('on', +b.dataset.story === k); });
  }
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) set(+en.target.dataset.story); });
  }, { rootMargin: '-48% 0px -48% 0px' });
  blocks.forEach(function (b) { io.observe(b); });
  addEventListener('hashchange', function () { if (view.hidden) set(-1); });
})();
"""


def page():
    wm24, _ = wordmark(24, '20261028_Wordmark-24px-Master.svg')
    wm16, _ = wordmark(16, '20261028_Wordmark-16px-Master.svg')
    wm24 = wm24.replace('<svg ', '<svg class="wm24" ', 1)
    wm16 = wm16.replace('<svg ', '<svg class="wm16" ', 1)
    kcss, kjs = kit()
    source = (f'{M["generated"]["title"]} Systems Atlas V7, snapshot {SNAP_WORDS}. '
              f'{cnt("variables", COUNTS["variables"])} variables, {cnt("connections", COUNTS["connections"])} connections, '
              f'{cnt("loops", COUNTS["loops"])} loops, {cnt("reforms", COUNTS["reforms"])} reforms.')
    body = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="atlas-views" content="overview area-c loop-r10">
<title>Editorial Desk</title>
<meta name="description" content="Atlas concept 12: the systems atlas drawn the way a newspaper graphics desk would draw it.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">
<style>{kcss}</style>
<style>{CSS}</style>
</head>
<body data-surface="white">
<div class="wrap">
<header class="mast g12">
  <a class="wm" href="#overview" data-red="signature" aria-label="Oath &amp; Action, back to the overview">{wm24}{wm16}</a>
  <p class="runhead t-eyebrow">Atlas concept 12 / Editorial Desk</p>
  <nav class="views" aria-label="Views">
    <a href="#overview" data-tab="overview">Overview</a><a href="#area-c" data-tab="area-c">Area C</a><a href="#loop-r10" data-tab="loop-r10">Loop R10</a>
  </nav>
</header>
<div class="crumbrow"><nav class="ak-crumbs" aria-label="Breadcrumb" data-ak-crumbs></nav></div>
<p class="ak-vh" role="status" data-ak-status></p>
<main class="ak-stage" id="main">
{overview_section()}
{area_section()}
{loop_section()}
</main>
<footer class="foot g12">
  <p class="t-source left">{source}</p>
  <p class="t-source right">Atlas concept 12, Editorial Desk. Studio draft, October 30, 2026.</p>
</footer>
</div>
<aside class="ak-panel" data-ak-panel aria-labelledby="ak-panel-title" hidden>
  <div class="ak-panel-bar"><p data-ak-panel-kind></p><button type="button" class="ak-btn" data-ak-sheet-toggle aria-expanded="false">More</button><button type="button" class="ak-btn" data-ak-close>Close</button></div>
  <h2 id="ak-panel-title" data-ak-panel-title tabindex="-1"></h2>
  <div data-ak-panel-body></div>
</aside>
{templates()}
<script>{kjs}</script>
<script>AtlasKit.init();</script>
<script>{CONCEPT_JS}</script>
</body>
</html>
'''
    assert '—' not in re.sub(r'<(script|style)\b.*?</\1>', '', body, flags=re.S), 'em dash in page text'
    return body


if __name__ == '__main__':
    html_ = page()
    OUT.write_text(html_)
    print('wrote', OUT.relative_to(ROOT), f'{len(html_) / 1024:.0f} KB')
