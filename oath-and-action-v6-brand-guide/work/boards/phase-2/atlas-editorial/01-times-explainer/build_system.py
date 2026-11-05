"""Build editorial system 01, Times Explainer (White), for the atlas "Who Do They Answer To?" (November 5, 2026).

The atlas told the way a newspaper explainer tells a complex system: in order, with annotated drawings that teach.
The overview opens on a finding headline and a plain deck, then "How the circuit runs" (the eight parts in reading
order, each with its question, two sentences of its story, every variable by its short label and the main flow to the
next part with its count), then one calm summary diagram with only the flows between parts, then "Start from your own
bill". The route a headline names is Charcoal and the rest sits in Stone. One working red, on the loop and reform
pages only, where R-01 acts.

Every label, count, sign, grade, delay, issue, example and reform text is read from
work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json. R-01's disclosure is read from the
Atlas V7 file's own interest table. Headlines and decks are studio drafts (see the notes file).

Run from the project root:
    python3 -I work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py
Writes 20261105_Editorial-01-Times-Explainer.html beside this file.
"""
import html
import importlib.util
import json
import math
import pathlib
import re
from collections import Counter, defaultdict

from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

ED = json.loads((ROOT / 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json').read_text())
V7_HTML = ROOT / 'work/extract/supplied-20261105/20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html'
KIT = ROOT / 'work/boards/phase-2/atlas-concepts/shared'
OUT = HERE / '20261105_Editorial-01-Times-Explainer.html'

N, L, LO, RF, ISS = ED['nodes'], ED['links'], ED['loops'], ED['reforms'], ED['issues']
PARTS = {p['id']: p for p in ED['parts']}
COUNTS = ED['meta']['counts']
P = acc.PALETTE
MINUS = '−'
SNAP = ED['meta']['snapshot']
assert SNAP == '2026-10-15'
SNAP_WORDS = 'October 15, 2026'
e = lambda s: html.escape(str(s), quote=True)

# Reading order of the circuit (task brief): outside forces press in; Wealth to Policy; back to Your household;
# Technology underneath. The headline's route is the core circuit and its return line to Wealth.
ORDER = ['X', 'A', 'B', 'C', 'D', 'E', 'EC', 'TC']
CORE = ['A', 'B', 'C', 'D', 'E']
NUM = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'EC': 6, 'TC': 7}
PART_OF = {k: v['part'] for k, v in N.items()}
assert sorted(sum((p['nodes'] for p in ED['parts']), [])) == sorted(N)

# ------------------------------------------------------------------------------------------------ words from the data
GRADE_KEY = {'well_supported': 'well-supported'}


def gk(g):
    return GRADE_KEY.get(g, g)


def grade_word(g):
    return acc.GRADES[gk(g)][0]


def grade_gloss(g):
    return acc.GRADES[gk(g)][1]


def tex_of(g):
    return acc.GRADES[gk(g)][2] if g and gk(g) in acc.GRADES else 'solid'


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def verb(p):
    return acc.SIGN_WORDS.get(p if p in ('+', '-') else None)


def delay_words(d):
    return acc.DELAYS[d]


def sentences(t):
    return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"“])', t.strip()) if s]


def first_sentence(t):
    return sentences(t)[0]


def story_lead(p):
    """One or two sentences of a part's story: the first two, skipping a short opening line."""
    s = sentences(p['story'])
    if len(s[0]) < 32:
        s = s[1:]
    return ' '.join(s[:2])


def label(code):
    return N[code]['label']


def mid(code_or_label):
    """A short label set mid-sentence: lower its first letter unless the word is a proper noun in the data."""
    if code_or_label in N:
        lab, desc = N[code_or_label]['label'], N[code_or_label]['description'] + ' ' + N[code_or_label]['title']
    else:
        lab, desc = code_or_label, ''
    w = lab.split()[0]
    if len(w) > 1 and w[1].isupper():
        return lab
    core = re.sub(r"['’]s?$", '', w)
    if re.search(r'[a-z,;] ' + re.escape(core) + r'\b', desc):
        return lab
    return lab[0].lower() + lab[1:]


def plural_head(lab):
    for w in lab.split()[:2]:
        if w.endswith('s') and not w.endswith('ss') and not w.endswith("'s") and not w.endswith('’s'):
            return True
    return False


def amount(lab, up):
    return ('more ' if up else ('fewer ' if plural_head(lab) else 'less ')) + lab


def station_codes(lid):
    return [s['code'] if s['code'] in N else None for s in LO[lid]['stations']]


def station_labels(lid):
    out = []
    for s in LO[lid]['stations']:
        out.append(label(s['code']) if s['code'] in N else s['label'])
    return out


def station_mids(lid):
    out = []
    for s in LO[lid]['stations']:
        out.append(mid(s['code']) if s['code'] in N else s['label'][0].lower() + s['label'][1:])
    return out


def directions(lid):
    """More or less at each station, multiplying the signs along the chain from a rise at the first station."""
    up, out = True, []
    for st in LO[lid]['steps']:
        out.append(up)
        if st['polarity'] == '-':
            up = not up
    return out, up


def read_aloud(lid):
    labs, (dirs, back) = station_mids(lid), directions(lid)
    parts = [amount(lab, d) for lab, d in zip(labs, dirs)]
    line = ', '.join(parts) + ', and back to ' + amount(labs[0], back)
    return line[0].upper() + line[1:] + '.'


def kind_line(lid):
    l = LO[lid]
    return f'{l["kind_word"]}, {l["kind_gloss"]}'


def weakest_text(lid):
    l = LO[lid]
    if l['conceptual']:
        return 'No numbered steps to grade'
    if l['weakest']:
        bits = [f'{w}, {grade_word(L[w]["evidence"]).lower()}' for w in l['weakest']]
        word = 'Weakest step' if len(bits) == 1 else 'Weakest steps'
        return f'{word}: {"; ".join(bits)}'
    grades = {s['evidence'] for s in l['steps']}
    if len(grades) == 1:
        return f'Every step graded {grade_word(next(iter(grades))).lower()}'
    return 'No single weakest step: the steps rank alike'


MODEL = json.loads((ROOT / 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json').read_text())


def direction_word(lid):
    d = MODEL['loops'][lid].get('direction_word') or ''
    return d[0].upper() + d[1:] if d else ''


def reform_count_text(lid):
    n = len(LO[lid]['reforms'])
    return 'No reform aims at it' if n == 0 else (f'1 reform aims at it' if n == 1 else f'{n} reforms aim at it')


def status_line(lid):
    l = LO[lid]
    bits = [direction_word(lid), f'one turn: {l["delay_word"]}', weakest_text(lid), reform_count_text(lid)]
    return ' · '.join(b for b in bits if b)


def disclosure(lid):
    l = LO[lid]
    if l['conceptual']:
        return 'A sketch: no complete numbered chain, so its steps carry no grade.'
    if l['hypothesized']:
        hyp = [s['id'] for s in l['steps'] if s['evidence'] == 'hypothesis']
        return f'Closed with a hypothesized step: {", ".join(hyp)} {"is" if len(hyp) == 1 else "are"} untested.'
    return ''


def effect_words(v):
    def rep(m):
        c = m.group(0)
        return f'{c.replace("-", MINUS)} ({ED["effect_codes"][c]})'
    return re.sub(r'(?<![\w])([+-][LMS]|\?|0)(?![\w])', rep, v)


def iso_words(d):
    if not d:
        return None
    y, m, dd = d.split('-')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return f'{months[int(m) - 1]} {int(dd)}, {y}'


def link_sentence(lid):
    l = L[lid]
    s = f'{lid}: {l["name"]}. From {l["from"]} {label(l["from"])} to {l["to"]} {label(l["to"])}.'
    if l['polarity'] in ('+', '-'):
        s += f' Sign {sign_char(l["polarity"])}, it {verb(l["polarity"])} it.'
    else:
        s += ' A line of authority with no sign: one side decides.'
    return s + f' Evidence {grade_word(l["evidence"]).lower()}. Delay {delay_words(l["delay"])}.'


# The editor's disclosure for nomination reforms, read from Atlas V7's own interest table
def interest_texts():
    src = V7_HTML.read_text()
    m = re.search(r"var INTERESTS = \{(.*?)\};\s*var INTEREST_TEXT = \{(.*?)\};", src, re.S)
    keys = dict(re.findall(r"'([^']+)':\s*'([^']+)'", m.group(1)))
    texts = {}
    for k, v in re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", m.group(2)):
        texts[k] = v.replace("\\'", "'")
    return {r: texts[k] for r, k in keys.items()}


INTEREST = interest_texts()
for rid, r in RF.items():
    assert bool(r['interest_note']) == (rid in INTEREST) or not r['interest_note'], rid

# ------------------------------------------------------------------------------------------------ counts
FLOWS = defaultdict(list)          # (from part, to part) -> link ids
INSIDE = Counter()
for lid, l in L.items():
    a, b = PART_OF[l['from']], PART_OF[l['to']]
    if a == b:
        INSIDE[a] += 1
    else:
        FLOWS[(a, b)].append(lid)
CROSS = sum(len(v) for v in FLOWS.values())
assert CROSS + sum(INSIDE.values()) == COUNTS['connections']
RANK = {'documented': 0, 'well-supported': 1, 'plausible': 2, 'plausible_contested': 3, 'hypothesis': 4}


def flow_n(a, b):
    return len(FLOWS.get((a, b), []))


def flow_examples(a, b, k=2):
    ids = sorted(FLOWS.get((a, b), []), key=lambda x: (RANK[L[x]['evidence']], x))
    return ids[:k]


def touching(pid):
    return [lid for lid, l in L.items() if pid in (PART_OF[l['from']], PART_OF[l['to']])]


HOME = defaultdict(list)
for k in ED['loop_order']:
    HOME[LO[k]['home'] or 'SK'].append(k)
N_R = sum(1 for l in LO.values() if l['type'] == 'R')
N_B = sum(1 for l in LO.values() if l['type'] == 'B')
N_SK = sum(1 for l in LO.values() if l['conceptual'])
N_WITH_REFORM = sum(1 for l in LO.values() if l['reforms'])

C_SET = set(PARTS['C']['nodes'])
C_IN = [lid for lid, l in L.items() if l['to'] in C_SET and l['from'] not in C_SET]
C_OUT = [lid for lid, l in L.items() if l['from'] in C_SET and l['to'] not in C_SET]
C_INSIDE = [lid for lid, l in L.items() if l['from'] in C_SET and l['to'] in C_SET]
C_LOOPS = [k for k in ED['loop_order'] if any(c in C_SET for c in station_codes(k) if c)]
C_ISSUES = [i for i in ISS.values() if set(i['nodes'] or []) & C_SET and not i['retired']]
C_REFORMS = [r for r in RF.values() if any(t in C_SET or (t in L and (L[t]['from'] in C_SET or L[t]['to'] in C_SET))
                                           for t in r['targets'])]
assert len(C_ISSUES) == 39 and len(C_LOOPS) == 7, (len(C_ISSUES), C_LOOPS)


def cnt(key, n):
    return f'<span data-count="{e(key)}">{n}</span>'


def cnt_svg(key, n):
    return f'<tspan data-count="{e(key)}">{n}</tspan>'


WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']


def nw(n, cap=False):
    w = WORDS[n] if n < len(WORDS) else str(n)
    return w.capitalize() if cap else w


def plural(n, one, many):
    return one if n == 1 else many


# ------------------------------------------------------------------------------------------------ text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False, track=0.0):
    w = _font(weight).getlength(text) * size / 200
    if tight:
        w *= 0.955
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


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def svg_text(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{e(s)}</text>'


def svg_lines(x, y, rows, cls, lh, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    spans = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{spans}</text>'


# ------------------------------------------------------------------------------------------------ line machinery
ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 2)}   # body, point, height, sign length, bar
BEND = {2: 8, 3: 12, 6: 18}


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
    """Stretch the pattern so the line starts and ends on ink (design frame memo, rule 3.2)."""
    arr, cap = pattern(tex, w)
    if arr is None:
        return ''
    if tex == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.2f}'
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.2f}' for x in arr)


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


def longest_mid(pts):
    """Middle of the longest straight run, as a distance along the path: tags sit on straight runs."""
    best, acc_s, at = -1, 0.0, 0.0
    for i in range(len(pts) - 1):
        d = math.dist(pts[i], pts[i + 1])
        if d > best:
            best, at = d, acc_s + d / 2
        acc_s += d
    return at


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


def head_shape(tx, ty, ux, uy, w, cls='hd'):
    al, ab = ARROW[w]
    bx, by = tx - ux * al, ty - uy * al
    vx, vy = -uy, ux
    return (f'<path class="{cls}" d="M{f(bx + vx * ab / 2)} {f(by + vy * ab / 2)}L{f(tx)} {f(ty)}'
            f'L{f(bx - vx * ab / 2)} {f(by - vy * ab / 2)}Z"/>')


def tag_shape(cx, cy, ux, uy, sign, w, cls='tg'):
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
    return f'<g class="{cls}"><polygon points="{poly}"/>{glyph}</g>'


def diamond_shape(tx, ty, ux, uy, cls='dm'):
    """Authority connections end in an open diamond, 14 by 11 px (design frame memo, section 3)."""
    vx, vy = -uy, ux
    pts = [(0, 0), (-7, 5.5), (-14, 0), (-7, -5.5)]
    poly = ' '.join(f'{f(tx + ux * s + vx * t)},{f(ty + uy * s + vy * t)}' for s, t in pts)
    return f'<polygon class="{cls}" points="{poly}"/>'


def tick_marks(x, y, ux, uy, count, w, cls='tk'):
    vx, vy = -uy, ux
    half = w / 2 + 4
    out = []
    for i in range(count):
        cx, cy = x + ux * (12 + i * 5), y + uy * (12 + i * 5)
        out.append(f'<path class="{cls}" d="M{f(cx - vx * half)} {f(cy - vy * half)}L{f(cx + vx * half)} {f(cy + vy * half)}"/>')
    return ''.join(out)


def wire_marks(pts, grade, sign, delay, w, lit=True, sketch=False, tag_at=None, authority=False):
    """The marks for one connection along pts (tail to tip): the line in its evidence texture, delay ticks after the
    tail, the pointing tag with the sign, and the arrowhead (an open diamond for authority). With lit=True each mark is
    also drawn at the 6 px weight, and CSS shows one size or the other."""
    tex = 'solid' if sketch else tex_of(grade)
    ux, uy = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    al = 14 if authority else ARROW[w][0]
    body = list(pts[:-1]) + [(pts[-1][0] - ux * al, pts[-1][1] - uy * al)]
    if tex == 'dotted':
        body[-1] = (body[-1][0] - ux * 1.5 * w, body[-1][1] - uy * 1.5 * w)
    length = path_len(body)
    d = rounded_d(body, BEND[w])
    sizes = (w, 6) if lit else (w,)
    das = {ww: fitted(tex, ww, length) for ww in (2, 3, 6)}
    style = ''.join(f'--d{ww}:{das[ww]};' for ww in (2, 3, 6) if das[ww])
    dash = f' stroke-dasharray="{das[w]}"' if das[w] else ''
    st = f' style="{style}"' if style and lit else ''
    cap = pattern(tex, w)[1]
    if sketch:
        marks = (f'<path class="rail-o" d="{d}" fill="none" stroke-width="{w + 2}"/>'
                 f'<path class="rail-i" d="{d}" fill="none" stroke-width="{w}"/>')
    else:
        marks = (f'<path class="ak-case" d="{d}" fill="none"{dash}/>'
                 f'<path class="ak-mark" d="{d}" fill="none" stroke-width="{w}" stroke-linecap="{cap}"{dash}{st}/>')
    out = [marks]
    if delay:
        t0, tu = point_at(pts, 0)
        n_ticks = {'S': 1, 'M': 2, 'L': 3}[delay]
        for ww in sizes:
            out.append(f'<g class="{"lo" if ww == w else "hi"}">' + tick_marks(t0[0], t0[1], tu[0], tu[1], n_ticks, ww) + '</g>')
    if sign in ('+', '-'):
        at = longest_mid(body) if tag_at is None else length * tag_at
        (cx, cy), (gx, gy) = point_at(body, at)
        for ww in sizes:
            out.append(f'<g class="{"lo" if ww == w else "hi"}">' + tag_shape(cx, cy, gx, gy, sign, ww) + '</g>')
    for ww in sizes:
        if authority:
            out.append(f'<g class="{"lo" if ww == w else "hi"}">' + diamond_shape(pts[-1][0], pts[-1][1], ux, uy) + '</g>')
        else:
            out.append(f'<g class="{"lo" if ww == w else "hi"}">' + head_shape(pts[-1][0], pts[-1][1], ux, uy, ww) + '</g>')
    return ''.join(out), body, length


def tag_point(pts, w, sign, tag_at=None):
    ux, uy = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    body = list(pts[:-1]) + [(pts[-1][0] - ux * ARROW[w][0], pts[-1][1] - uy * ARROW[w][0])]
    at = longest_mid(body) if tag_at is None else path_len(body) * tag_at
    return point_at(body, at)


def bundle(pts, w, cls, heads=('end',)):
    """A bundle of connections between two parts: a plain line with arrowheads, no sign, no grade."""
    out = []
    p = list(pts)
    ux, uy = unit(p[-1][0] - p[-2][0], p[-1][1] - p[-2][1])
    sx, sy = unit(p[0][0] - p[1][0], p[0][1] - p[1][1])
    al = ARROW[w][0]
    body = list(p)
    if 'end' in heads:
        body[-1] = (p[-1][0] - ux * al, p[-1][1] - uy * al)
        out.append(head_shape(p[-1][0], p[-1][1], ux, uy, w, 'bh'))
    if 'start' in heads:
        body[0] = (p[0][0] - sx * al, p[0][1] - sy * al)
        out.append(head_shape(p[0][0], p[0][1], sx, sy, w, 'bh'))
    return f'<g class="{cls}"><path class="bl" d="{rounded_d(body, BEND[w])}" fill="none" stroke-width="{w}"/>{"".join(out)}</g>'


# ------------------------------------------------------------------------------------------------ type in drawings
# (size, weight, Inter Tight?, leading) from the design frame memo's type scale, section 2
STY = {
    'station': (20, 700, True, 22),
    'map': (15, 600, False, 18),
    'mapr': (15, 400, False, 21),
    'note': (13, 400, False, 16),
    'noteb': (13, 600, False, 16),
    'eyebrow': (13, 700, False, 18),
    'head': (22, 800, True, 26),
    'count': (22, 800, True, 26),
    'fig': (40, 800, True, 40),
    'cap': (14, 400, False, 20),
}


def sw(text_, style):
    s, wt, tight, _ = STY[style]
    trk = 0.06 if style == 'eyebrow' else 0
    return tw(text_.upper() if style == 'eyebrow' else text_, s, wt, tight, trk)


def swrap(text_, width, style):
    s, wt, tight, _ = STY[style]
    return wrap(text_, width, s, wt, tight)


# ------------------------------------------------------------------------------------------------ stations and cycles
def pill(cx, cy, w, h, cls='pl', sketch=False):
    r = h / 2
    sw_ = 1 if sketch else 2
    return (f'<rect class="ak-mark {cls}" x="{f(cx - w / 2)}" y="{f(cy - h / 2)}" width="{f(w)}" height="{f(h)}" '
            f'rx="{f(r)}" stroke-width="{sw_}"/>')


def station_block(code, lab, cx, cy, pw, style, sketch=False, ghost=False):
    """A variable as a pill with its short label inside, centered at cx, cy. Returns (svg, pill height)."""
    s, wt, tight, lh = STY[style]
    rows = swrap(lab, pw - 30, style)
    h = max(len(rows) * lh + 22, 44)
    ty = cy - (len(rows) - 1) * lh / 2 + s * 0.35
    attrs = f' data-node="{code}" data-name="{e(lab)}"' if code else ''
    cls = 'pl' + (' sk' if sketch else '') + (' gh' if ghost else '')
    tcls = 'st-' + style + (' sk' if sketch else '') + (' gh' if ghost else '')
    svg = pill(cx, cy, pw, h, cls, sketch) + svg_lines(cx, ty, rows, tcls + ' ak-label', lh, 'middle', attrs)
    return svg, h


def cycle_layout(n, W, pw, hs):
    """Station centers for a small cycle of n stations, read clockwise from the top left."""
    m = 2
    x1, x2 = m + pw / 2, W - m - pw / 2
    if n == 2:
        cy = 84 + max(hs) / 2
        return [(x1, cy), (x2, cy)]
    y1 = 34 + max(hs[:2]) / 2
    if n == 3:
        y2 = y1 + max(hs[:2]) / 2 + 96 + hs[2] / 2
        return [(x1, y1), (x2, y1), ((x1 + x2) / 2, y2)]
    y2 = y1 + max(hs[:2]) / 2 + 104 + max(hs[2:]) / 2
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def cycle_small(lid, W=350, step_numbers=False, interactive=False, view='loops'):
    """A loop as a named box-and-arrow cycle, small enough for a catalog card. Pills carry the variables' short
    labels; every arrow carries its sign tag with "raises" or "lowers", its evidence texture and its delay ticks; the
    weakest step says so; the loop's ID and character sit in the middle."""
    l = LO[lid]
    n = len(l['stations'])
    labs, codes = station_labels(lid), station_codes(lid)
    sketch = l['conceptual']
    pw = {2: 128, 3: 132, 4: 128}[n]
    hs = [max(len(swrap(lab, pw - 28, 'map')) * 18 + 22, 44) for lab in labs]
    pos = cycle_layout(n, W, pw, hs)
    parts, labels_ = [], []
    weakest = set(l['weakest'] or [])
    for i, st in enumerate(l['steps']):
        a, b = pos[i], pos[(i + 1) % n]
        ha, hb = hs[i], hs[(i + 1) % n]
        word = verb(st['polarity']) if st['polarity'] else ''
        rows = [f'{i + 1}. {word}' if step_numbers else word]
        vertical = (n == 3 and i in (1, 2)) or (n == 4 and i in (1, 3))
        if st['id'] and st['id'] in weakest:
            rows += ['weakest', 'step'] if vertical else ['weakest step']
        if n == 2:
            if i == 0:
                yy = a[1] - ha / 2 - 34
                pts = [(a[0], a[1] - ha / 2 - 2), (a[0], yy), (b[0], yy), (b[0], b[1] - hb / 2 - 2)]
                side = 'above'
            else:
                yy = a[1] + ha / 2 + 34
                pts = [(a[0], a[1] + ha / 2 + 2), (a[0], yy), (b[0], yy), (b[0], b[1] + hb / 2 + 2)]
                side = 'below'
        elif n == 3:
            if i == 0:
                pts = [(a[0] + pw / 2 + 2, a[1]), (b[0] - pw / 2 - 2, b[1])]
                side = 'above'
            elif i == 1:
                pts = [(a[0], a[1] + ha / 2 + 2), (a[0], b[1]), (b[0] + pw / 2 + 2, b[1])]
                side = 'in-right'
            else:
                pts = [(a[0] - pw / 2 - 2, a[1]), (b[0], a[1]), (b[0], b[1] + hb / 2 + 2)]
                side = 'in-left'
        else:
            if i == 0:
                pts = [(a[0] + pw / 2 + 2, a[1]), (b[0] - pw / 2 - 2, b[1])]
                side = 'above'
            elif i == 1:
                pts = [(a[0], a[1] + ha / 2 + 2), (b[0], b[1] - hb / 2 - 2)]
                side = 'in-right'
            elif i == 2:
                pts = [(a[0] - pw / 2 - 2, a[1]), (b[0] + pw / 2 + 2, b[1])]
                side = 'below'
            else:
                pts = [(a[0], a[1] - ha / 2 - 2), (b[0], b[1] + hb / 2 + 2)]
                side = 'in-left'
        marks, body, _ = wire_marks(pts, st['evidence'], st['polarity'], st['delay'], 2, lit=interactive,
                                    sketch=sketch)
        attrs = ''
        if st['id']:
            ll = L[st['id']]
            attrs = (f' data-link="{st["id"]}" data-sign="{sign_attr(ll["polarity"])}" data-grade="{ll["evidence"]}" '
                     f'data-delay="{ll["delay"]}"')
        if interactive and st['id']:
            key = f'link-{st["id"].lower()}'
            rel = ' '.join(f'var-{c.lower()}' for c in (codes[i], codes[(i + 1) % n]) if c)
            say = e(link_sentence(st['id']))
            parts.append(f'<g class="wire" role="button" data-select="{key}"{attrs} data-rel="{rel}" aria-label="{say}" '
                         f'data-say="{say}">{marks}<path class="ak-hit" d="{rounded_d(pts, 0)}"/></g>')
        else:
            parts.append(f'<g class="wire"{attrs}>{marks}</g>')
        (tx, ty), _ = tag_point(pts, 2, st['polarity'])
        lh = 16
        if side == 'above':
            labels_.append(svg_lines(tx, ty - 15 - (len(rows) - 1) * lh, rows, 'vb', lh, 'middle'))
        elif side == 'below':
            labels_.append(svg_lines(tx, ty + 25, rows, 'vb', lh, 'middle'))
        elif side == 'in-right':
            labels_.append(svg_lines(tx - 14, ty + 4 - (len(rows) - 1) * lh / 2, rows, 'vb', lh, 'end'))
        else:
            labels_.append(svg_lines(tx + 14, ty + 4 - (len(rows) - 1) * lh / 2, rows, 'vb', lh, 'start'))
    nodes = []
    for i, (lab, code) in enumerate(zip(labs, codes)):
        svg, _ = station_block(code, lab, pos[i][0], pos[i][1], pw, 'map', sketch=(sketch and not code))
        if interactive and code:
            say = e(f'{code} {lab}. {N[code]["increase_means"]}')
            nodes.append(f'<g class="node" role="button" data-select="var-{code.lower()}" data-node="{code}" '
                         f'aria-label="{say}" data-say="{say}">{svg}</g>')
        else:
            nodes.append(f'<g class="node">{svg}</g>')
    if n == 2:
        cx, cy = W / 2, pos[0][1] - 4
    elif n == 3:
        cx, cy = W / 2, (pos[0][1] + pos[2][1]) / 2 - 6
    else:
        cx, cy = W / 2, (pos[0][1] + pos[2][1]) / 2 - 6
    mid_ = svg_text(cx, cy, lid, 'cid', 'middle') + svg_text(cx, cy + 18, l['kind_gloss'], 'ckind', 'middle')
    H = max(p[1] + h / 2 for p, h in zip(pos, hs)) + (84 if n == 2 else 4 if n == 3 else 46)
    title = f'{lid}, {l["plain_name"]}: {read_aloud(lid)}'
    role = 'group' if interactive else 'img'
    return (f'<svg class="cyc" data-view="{view}" viewBox="0 0 {W} {f(H)}" width="{W}" height="{f(H)}" role="{role}" '
            f'aria-label="{e(title)}">{"".join(parts)}{"".join(nodes)}{"".join(labels_)}{mid_}</svg>')


# ------------------------------------------------------------------------------------------------ large drawings
def step_block(lid_step, idx, weakest, with_step=True):
    """The words an arrow carries in a close-up: step, name, sign and verb with the delay, grade with its gloss."""
    l = L[lid_step]
    rows = []
    if with_step:
        rows.append(('eyebrow', f'Step {idx} · {lid_step}'))
    rows.append(('map', l['name']))
    rows.append(('noteb', f'{sign_char(l["polarity"])} {verb(l["polarity"])} · {delay_words(l["delay"])}'))
    rows.append(('note', f'{grade_word(l["evidence"])}: {grade_gloss(l["evidence"])}'))
    if lid_step in weakest:
        rows.append(('eyebrow', 'The weakest step'))
    return rows


def layout_rows(rows, width):
    """Wrap a list of (style, text) rows to a width; returns [(style, line)] and the block height."""
    out = []
    for st, t in rows:
        lines_ = swrap(t, width, st) if st != 'eyebrow' else [t.upper()]
        for ln in lines_:
            out.append((st, ln))
    h = sum(STY[st][3] for st, _ in out)
    return out, h


CLS = {'eyebrow': 'eb', 'map': 'lb', 'noteb': 'nb', 'note': 'nt', 'mapr': 'nr', 'cap': 'cp2'}


def draw_rows(x, y_top, rows, anchor='start', extra_cls=''):
    """Draw laid-out rows with their top at y_top. Baselines sit at 0.8 of each leading."""
    out, y = [], y_top
    for st, ln in rows:
        lh = STY[st][3]
        y += lh
        out.append(svg_text(x, y - lh * 0.24, ln, CLS[st] + extra_cls, anchor))
    return ''.join(out)


def cycle_large(lid, W=866, reform='R-01', view='loop-r10'):
    """The loop at full size: four stations clockwise from the top left, each step named with its sign and verb,
    delay, grade and gloss; the weakest step marked; the stepper's more and less marks; where the reform acts."""
    l = LO[lid]
    codes, labs = station_codes(lid), station_labels(lid)
    assert len(codes) == 4 and all(codes)
    weakest = set(l['weakest'] or [])
    pw, x1 = 196, 226
    x2 = W - x1
    hs = [len(swrap(lab, pw - 44, 'station')) * 22 + 28 for lab in labs]
    gap_lab = x2 - x1 - pw - 14
    side_w = x1 - 36
    blocks = [layout_rows(step_block(st['id'], i + 1, weakest), gap_lab if i in (0, 2) else side_w)
              for i, st in enumerate(l['steps'])]
    notes = []
    for c in codes:
        rows = [('eyebrow', f'Variable {c}'), ('cap', N[c]['increase_means'])]
        notes.append(layout_rows(rows, pw))
    top_need = max(blocks[0][1] + 24, max(notes[0][1], notes[1][1]) + 16) + max(hs[0], hs[1]) / 2 + 8
    y1 = top_need + 8
    y2 = y1 + 340
    pos = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    wires, labels_ = [], []
    for i, st in enumerate(l['steps']):
        a, b = pos[i], pos[(i + 1) % 4]
        ha, hb = hs[i], hs[(i + 1) % 4]
        if i == 0:
            pts = [(a[0] + pw / 2 + 2, a[1]), (b[0] - pw / 2 - 2, b[1])]
        elif i == 1:
            pts = [(a[0], a[1] + ha / 2 + 2), (b[0], b[1] - hb / 2 - 2)]
        elif i == 2:
            pts = [(a[0] - pw / 2 - 2, a[1]), (b[0] + pw / 2 + 2, b[1])]
        else:
            pts = [(a[0], a[1] - ha / 2 - 2), (b[0], b[1] + hb / 2 + 2)]
        ll = L[st['id']]
        marks, _, _ = wire_marks(pts, ll['evidence'], ll['polarity'], ll['delay'], 3)
        key = f'link-{st["id"].lower()}'
        rel = f'var-{codes[i].lower()} var-{codes[(i + 1) % 4].lower()}'
        say = e(link_sentence(st['id']))
        wires.append(f'<g class="wire" role="button" data-select="{key}" data-link="{st["id"]}" '
                     f'data-sign="{sign_attr(ll["polarity"])}" data-grade="{ll["evidence"]}" data-delay="{ll["delay"]}" '
                     f'data-from="{ll["from"]}" data-to="{ll["to"]}" data-rel="{rel}" aria-label="{say}" data-say="{say}">'
                     f'{marks}<path class="ak-hit" d="{rounded_d(pts, 0)}"/></g>')
        (tx, ty), _ = tag_point(pts, 3, ll['polarity'])
        rows, h = blocks[i]
        if i == 0:
            labels_.append(draw_rows(tx, ty - 22 - h, rows, 'middle'))
        elif i == 2:
            labels_.append(draw_rows(tx, ty + 20, rows, 'middle'))
        elif i == 1:
            labels_.append(draw_rows(tx + 22, ty - h / 2, rows, 'start'))
        else:
            labels_.append(draw_rows(tx - 22, ty - h / 2, rows, 'end'))
    nodes, extra = [], []
    for i, c in enumerate(codes):
        svg, h = station_block(c, labs[i], pos[i][0], pos[i][1], pw, 'station')
        say = e(f'{c} {labs[i]}. {N[c]["increase_means"]}')
        nodes.append(f'<g class="node" role="button" data-select="var-{c.lower()}" data-node="{c}" aria-label="{say}" '
                     f'data-say="{say}">{svg}</g>')
        rows, nh = notes[i]
        left = i in (0, 3)
        nx_ = pos[i][0] - pw / 2 + 4 if left else pos[i][0] + pw / 2 - 4
        anchor = 'start' if left else 'end'
        if i in (0, 1):
            extra.append(draw_rows(nx_, pos[i][1] - h / 2 - 12 - nh, rows, anchor, ' sn'))
        else:
            extra.append(draw_rows(nx_, pos[i][1] + h / 2 + 10, rows, anchor, ' sn'))
    # the stepper's more and less words, inside the square beside each station
    dirs, back = directions(lid)
    word = lambda up, lab: ('more' if up else ('fewer' if plural_head(lab) else 'less'))
    marks_ = []
    for i, c in enumerate(codes):
        up = dirs[i]
        x = pos[i][0] + (16 if i in (0, 1, 3) else -16)
        anchor = 'start' if i in (0, 1, 3) else 'end'
        y = pos[i][1] + (hs[i] / 2 + 22 if i in (0, 1) else -hs[i] / 2 - 12)
        at = 1 if i == 0 else i
        txt = ('Start: ' if i == 0 else 'Now: ') + word(up, labs[i])
        marks_.append(f'<g data-ak-at="{at}" hidden>{svg_text(x, y, txt, "mk", anchor)}</g>')
    y_back = pos[0][1] + hs[0] / 2 + 40
    marks_.append(f'<g data-ak-at="4" hidden>{svg_text(pos[0][0] + 16, y_back, "Back here: " + word(back, labs[0]) + " again", "mk", "start")}</g>')
    cx, cy = W / 2, (y1 + y2) / 2
    centre = (svg_text(cx, cy + 46, lid, 'cid2', 'middle') + svg_text(cx, cy + 66, l['plain_name'], 'ckind', 'middle')
              + svg_text(cx, cy + 84, l['kind_gloss'], 'ckind', 'middle'))
    # where the reform acts: one note, leaders to each target
    r = RF[reform]
    tl = []
    for t in r['targets']:
        if t in L:
            k = next(i for i, s in enumerate(l['steps']) if s['id'] == t)
            tl.append(f'step {k + 1} ({t})')
        else:
            tl.append(label(t))
    text_ = (f'Reform {reform}, {r["short"].lower()}, acts where the marks turn red: '
             + ', '.join(tl[:-1]) + ' and ' + tl[-1] + '.')
    nrows, nh = layout_rows([('mapr', text_)], 236)
    nx, ny = cx - 118, y1 + hs[0] / 2 + 52
    note = draw_rows(nx, ny, nrows, 'start', ' rn')
    leaders = []
    for t in r['targets']:
        if t in L:
            k = next(i for i, s in enumerate(l['steps']) if s['id'] == t)
            a, b = pos[k], pos[(k + 1) % 4]
            if k == 0:
                tgt = (cx - 40, y1 + 6)
                leaders.append(f'M{f(cx - 40)} {f(ny - 4)}L{f(tgt[0])} {f(tgt[1])}')
            elif k == 1:
                yy = ny + nh * 0.5
                leaders.append(f'M{f(nx + 236 + 6)} {f(yy)}L{f(x2 - 6)} {f(yy)}')
        else:
            k = codes.index(t)
            leaders.append(f'M{f(nx + 236 + 6)} {f(ny + 8)}L{f(pos[k][0] - 30)} {f(pos[k][1] + hs[k] / 2 + 4)}')
    lead = f'<path class="leader" d="{" ".join(leaders)}"/>'
    H = max(y2 + max(hs[2], hs[3]) / 2 + 14 + max(notes[2][1], notes[3][1]), y2 + 20 + blocks[2][1]) + 12
    return (f'<svg class="big" data-view="{view}" viewBox="0 0 {W} {f(H)}" role="group" aria-labelledby="{view}-h">'
            f'{lead}{"".join(wires)}{"".join(nodes)}{"".join(labels_)}{"".join(extra)}{"".join(marks_)}{centre}{note}</svg>')


def wire_group(lid, pts, w=3, rel=None, interactive=True, tag_at=None):
    ll = L[lid]
    marks, _, _ = wire_marks(pts, ll['evidence'], ll['polarity'], ll['delay'], w, lit=interactive, tag_at=tag_at,
                             authority=ll['polarity'] not in ('+', '-'))
    attrs = (f'data-link="{lid}" data-sign="{sign_attr(ll["polarity"])}" data-grade="{ll["evidence"]}" '
             f'data-delay="{ll["delay"]}" data-from="{ll["from"]}" data-to="{ll["to"]}"')
    if not interactive:
        return f'<g class="wire" {attrs}>{marks}</g>'
    rel = rel if rel is not None else f'var-{ll["from"].lower()} var-{ll["to"].lower()}'
    say = e(link_sentence(lid))
    return (f'<g class="wire" role="button" data-select="link-{lid.lower()}" {attrs} data-rel="{rel}" aria-label="{say}" '
            f'data-say="{say}">{marks}<path class="ak-hit" d="{rounded_d(pts, 0)}"/></g>')


def area_drawing(W=1312):
    """Elections up close: the safe-seat loop's four stations as a square, and the accountability loop sharing
    Risk of losing office, running out to Checks and back. Every connection inside the part is drawn."""
    R10, B4 = LO['R10'], LO['B4']
    sq = station_codes('R10')                      # C1, C2, C3, C4
    pw = 212
    x1, x2, x5 = 330, 740, 1100
    hs = {c: len(swrap(label(c), pw - 44, 'station')) * 22 + 28 for c in sq + ['C5', 'D5']}
    y1, y2 = 112, 436
    pos = {sq[0]: (x1, y1), sq[1]: (x2, y1), sq[2]: (x2, y2), sq[3]: (x1, y2), 'C5': (x5, y2), 'D5': (x5, y1)}
    edge = lambda c, side, off=0: {
        'r': (pos[c][0] + pw / 2 + 2, pos[c][1] + off), 'l': (pos[c][0] - pw / 2 - 2, pos[c][1] + off),
        't': (pos[c][0] + off, pos[c][1] - hs[c] / 2 - 2), 'b': (pos[c][0] + off, pos[c][1] + hs[c] / 2 + 2)}[side]
    route = {
        'L08': [edge('C1', 'r'), edge('C2', 'l')],
        'L25': [edge('C2', 'b'), edge('C3', 't')],
        'L53': [edge('C3', 'l'), edge('C4', 'r')],
        'L42': [edge('C4', 't'), edge('C1', 'b')],
        'L24': [edge('C3', 'r', 16), edge('C5', 'l', 16)],
        'L54': [edge('C5', 't'), edge('D5', 'b')],
        'L23': [edge('D5', 'l'), (930, y1), (930, y2 - 16), edge('C3', 'r', -16)],
    }
    assert set(C_INSIDE) == {'L08', 'L25', 'L53', 'L42', 'L24'}
    wires, labs_ = [], []
    weakest = set(R10['weakest'])
    for lid, pts in route.items():
        wires.append(wire_group(lid, pts, 3))
        (tx, ty), _ = tag_point(pts, 3, L[lid]['polarity'])
        rows = [('lb_', L[lid]['name'])]
        blk, h = layout_rows([('map', L[lid]['name']),
                              ('noteb', f'{lid} · {sign_char(L[lid]["polarity"])} {verb(L[lid]["polarity"])} · '
                                        f'{grade_word(L[lid]["evidence"])}')]
                             + ([('eyebrow', 'The weakest step')] if lid in weakest else []), 176)
        place = {'L08': ('above',), 'L53': ('below',), 'L42': ('left',), 'L25': ('inside',), 'L24': ('below',),
                 'L54': ('right',), 'L23': ('leftof',)}[lid][0]
        if place == 'above':
            labs_.append(draw_rows(tx, ty - 22 - h, blk, 'middle'))
        elif place == 'below':
            labs_.append(draw_rows(tx, ty + 20, blk, 'middle'))
        elif place == 'left':
            labs_.append(draw_rows(tx - 22, ty - h / 2, blk, 'end'))
        elif place == 'inside':
            labs_.append(draw_rows(tx - 22, ty - h / 2 - 40, blk, 'end'))
        elif place == 'right':
            labs_.append(draw_rows(tx + 22, ty - h / 2, blk, 'start'))
        else:
            labs_.append(draw_rows(tx - 22, ty - h / 2 + 30, blk, 'end'))
    nodes = []
    for c, (x, y) in pos.items():
        ghost = PART_OF[c] != 'C'
        svg, h = station_block(c, label(c), x, y, pw, 'station', ghost=ghost)
        say = e(f'{c} {label(c)}. {N[c]["increase_means"]}')
        if ghost:
            svg += svg_text(x - pw / 2 + 4, y - h / 2 - 12, f'In {PARTS[PART_OF[c]]["plain_name"]}'.upper(), 'eb gh', 'start')
        nodes.append(f'<g class="node" role="button" data-select="var-{c.lower()}" data-node="{c}" data-rel="" '
                     f'aria-label="{say}" data-say="{say}">{svg}</g>')
    cxa, cya = (x1 + x2) / 2, (y1 + y2) / 2
    centre = (svg_text(cxa, cya + 30, 'R10', 'cid2', 'middle') + svg_text(cxa, cya + 50, R10['plain_name'], 'ckind', 'middle')
              + svg_text(cxa, cya + 68, R10['kind_gloss'], 'ckind', 'middle'))
    cxb = (930 + x5) / 2 + 6
    centre += (svg_text(cxb, cya - 4, 'B4', 'cid2', 'middle') + svg_text(cxb, cya + 16, B4['plain_name'], 'ckind', 'middle')
               + svg_text(cxb, cya + 34, B4['kind_gloss'], 'ckind', 'middle'))
    meet = (f'Both loops run through {label("C3")}. '
            + re.sub(r'^The loop\b', f'The {B4["plain_name"].lower()}', first_sentence(B4['qualification'])))
    mrows, mh = layout_rows([('mapr', meet)], 300)
    ny = y2 + hs['C3'] / 2 + 92
    note = draw_rows(x2 + 40, ny, mrows, 'start', ' rn')
    lead = f'<path class="leader" d="M{f(x2 + 32)} {f(ny + 10)}L{f(x2 + 10)} {f(y2 + hs["C3"] / 2 + 6)}"/>'
    H = ny + mh + 16
    return (f'<svg class="big" data-view="area-c" viewBox="0 0 {W} {f(H)}" width="{W}" role="group" '
            f'aria-labelledby="area-c-draw-h" data-ak-roving data-ak-nav="spatial">{lead}{"".join(wires)}{"".join(nodes)}'
            f'{"".join(labs_)}{centre}{note}</svg>')


def conn_row(lid, direction, W):
    """One connection as a sentence-shaped drawing: the far variable, the arrow with its texture, sign, verb and
    delay ticks, and the Elections variable at the other end. HTML text below names the connection."""
    ll = L[lid]
    a, b = ll['from'], ll['to']
    arrow = 150 if W > 400 else 104
    lab_w = (W - arrow - 20) / 2
    ra = swrap(label(a), lab_w, 'map')
    rb = swrap(label(b), lab_w, 'map')
    rows_h = max(len(ra), len(rb)) * 18
    y = max(30, rows_h / 2 + 6)
    h = max(y + rows_h / 2 + 6, y + 14)
    ax = lab_w + 10
    bx = W - lab_w - 10
    pts = [(ax, y), (bx, y)]
    marks, _, _ = wire_marks(pts, ll['evidence'], ll['polarity'], ll['delay'], 2, lit=False,
                             authority=ll['polarity'] not in ('+', '-'))
    cls_a = 'lb' if PART_OF[a] == 'C' else 'lb far'
    cls_b = 'lb' if PART_OF[b] == 'C' else 'lb far'
    ta = svg_lines(lab_w, y - (len(ra) - 1) * 9 + 5, ra, cls_a, 18, 'end', f' data-node="{a}" data-name="{e(label(a))}"')
    tb = svg_lines(W - lab_w, y - (len(rb) - 1) * 9 + 5, rb, cls_b, 18, 'start', f' data-node="{b}" data-name="{e(label(b))}"')
    (tx, ty), _ = tag_point(pts, 2, ll['polarity'])
    vb = svg_text(tx, ty - 13, verb(ll['polarity']), 'vb', 'middle')
    attrs = (f'data-link="{lid}" data-sign="{sign_attr(ll["polarity"])}" data-grade="{ll["evidence"]}" '
             f'data-delay="{ll["delay"]}"')
    return (f'<svg class="crow" data-view="area-c" viewBox="0 0 {W} {f(h)}" width="{W}" height="{f(h)}" aria-hidden="true">'
            f'<g class="wire" {attrs}>{marks}</g>{ta}{tb}{vb}</svg>')


# ------------------------------------------------------------------------------------------------ the whole system
def list_words(items):
    items = list(items)
    return items[0] if len(items) == 1 else ', '.join(items[:-1]) + ' and ' + items[-1]


def summary_diagram(W=1312):
    """The eight parts with only the flows between them. The main circuit (Wealth to Policy and the return line)
    is Charcoal; every other flow is Stone. Each number counts the connections running the way its arrow points."""
    BX = {'A': 40, 'B': 299, 'C': 558, 'D': 817, 'E': 1076}
    BW = 196
    out, texts = [], []
    # outside forces band
    hx = 84
    xs = PARTS['X']
    drawn_x = {'A', 'B'}
    rest = [(PARTS[t]['plain_name'], flow_n('X', t)) for t in ORDER if t != 'X' and t not in drawn_x and flow_n('X', t)]
    by_n = defaultdict(list)
    for name, n in rest:
        by_n[n].append(name)
    bits = []
    for n in sorted(by_n):
        names = by_n[n]
        bits.append(f'{n} {"each " if len(names) > 1 else ""}into {list_words(names)}')
    x_rest = 'Also ' + list_words(bits) + '.'
    xvars = ' · '.join(label(c) for c in xs['nodes'])
    out.append(f'<g class="pt" role="button" data-select="part-x" aria-label="{e(xs["plain_name"] + ". " + xs["text"])}">'
               f'<rect class="ak-mark bx2" x="40" y="1" width="1232" height="{hx - 2}"/>'
               + svg_text(56, 32, xs['plain_name'], 'ph ak-label', 'start', f' data-part="X" data-name="{e(xs["plain_name"])}"')
               + svg_text(56 + sw(xs['plain_name'], 'head') + 14, 32, f'press in from outside the system: '
                          f'{flow_n_out("X")} connections', 'pq', 'start')
               + ''.join(svg_text(0, 0, '', 'x') for _ in [])
               + f'<text x="56" y="62" class="vn">' + ''.join(
                   f'<tspan data-node="{c}" data-name="{e(label(c))}">{e(label(c))}</tspan>'
                   + ('<tspan class="sep"> · </tspan>' if i < len(xs['nodes']) - 1 else '')
                   for i, c in enumerate(xs['nodes'])) + '</text>'
               + svg_text(1256, 62, x_rest, 'cp2', 'end') + '</g>')
    # core boxes
    y0 = 176
    def box_rows(pid, width):
        rows = []
        for c in PARTS[pid]['nodes']:
            rows.append((c, swrap(label(c), width, 'cap')))
        return rows
    core_rows = {pid: box_rows(pid, BW - 28) for pid in CORE}
    head_h = 74
    bh = head_h + max(sum(len(r) for _, r in core_rows[pid]) * 18 + (len(core_rows[pid]) - 1) * 2 for pid in CORE) + 18
    for pid in CORE:
        p = PARTS[pid]
        x = BX[pid]
        q = p['plain_question'] or ''
        g = [f'<rect class="ak-mark bx" x="{x}" y="{y0}" width="{BW}" height="{f(bh)}"/>',
             svg_text(x + 14, y0 + 30, p['plain_name'], 'ph ak-label', 'start', f' data-part="{pid}" data-name="{e(p["plain_name"])}"'),
             svg_text(x + 14, y0 + 52, q, 'pq', 'start'),
             f'<path class="hr" d="M{x + 14} {y0 + head_h - 8}H{x + BW - 14}"/>']
        yy = y0 + head_h + 10
        for c, rows in core_rows[pid]:
            g.append(svg_lines(x + 14, yy, rows, 'vn', 18, 'start', f' data-node="{c}" data-name="{e(label(c))}"'))
            yy += len(rows) * 18 + 2
        say = e(f'{p["plain_name"]}, {p["formal_title"]}. {q} {len(p["nodes"])} conditions.')
        if pid == 'C':
            out.append(f'<a class="pt" href="#area-c" aria-label="{say} Opens the Elections page.">{"".join(g)}</a>')
        else:
            out.append(f'<g class="pt" role="button" data-select="part-{pid.lower()}" aria-label="{say}">{"".join(g)}</g>')
    yb = y0 + bh
    # household and technology
    y3 = yb + 90
    ec, tc = PARTS['EC'], PARTS['TC']
    ecx, ecw = 40, BX['C'] + BW - 40
    tcx, tcw = BX['D'], 1272 - BX['D']
    colw = (ecw - 28 - 2 * 20) / 3
    ec_cols = []
    for gi, grp in enumerate(ec['groups']):
        rows = [('h', swrap(grp['title'], colw, 'noteb'))] + [(c, swrap(label(c), colw, 'cap')) for c in grp['nodes']]
        ec_cols.append(rows)
    tc_half = (len(tc['nodes']) + 1) // 2
    tc_colw = (tcw - 28 - 20) / 2
    tc_cols = [[(c, swrap(label(c), tc_colw, 'cap')) for c in tc['nodes'][:tc_half]],
               [(c, swrap(label(c), tc_colw, 'cap')) for c in tc['nodes'][tc_half:]]]
    col_h = lambda rows: sum(len(r) * (16 if k == 'h' else 18) + (6 if k == 'h' else 2) for k, r in rows)
    h3 = head_h + max([col_h(r) for r in ec_cols] + [col_h(r) for r in tc_cols]) + 16
    for pid, x, w, cols, cw in (('EC', ecx, ecw, ec_cols, colw), ('TC', tcx, tcw, tc_cols, tc_colw)):
        p = PARTS[pid]
        g = [f'<rect class="ak-mark bx2" x="{x}" y="{f(y3)}" width="{w}" height="{f(h3)}"/>',
             svg_text(x + 14, y3 + 30, p['plain_name'], 'ph ak-label', 'start', f' data-part="{pid}" data-name="{e(p["plain_name"])}"'),
             svg_text(x + 14, y3 + 52, p['plain_question'], 'pq', 'start'),
             f'<path class="hr" d="M{x + 14} {f(y3 + head_h - 8)}H{x + w - 14}"/>']
        for ci, rows in enumerate(cols):
            cx_ = x + 14 + ci * (cw + 20)
            yy = y3 + head_h + 10
            for k, r in rows:
                if k == 'h':
                    g.append(svg_lines(cx_, yy, r, 'gh2', 16, 'start'))
                    yy += len(r) * 16 + 6
                else:
                    g.append(svg_lines(cx_, yy, r, 'vn', 18, 'start', f' data-node="{k}" data-name="{e(label(k))}"'))
                    yy += len(r) * 18 + 2
        say = e(f'{p["plain_name"]}, {p["formal_title"]}. {p["plain_question"]} {len(p["nodes"])} conditions.')
        out.append(f'<g class="pt" role="button" data-select="part-{pid.lower()}" aria-label="{say}">{"".join(g)}</g>')
    yend = y3 + h3
    # flows
    fl = []
    cnts = []
    def count(x, y, n, main, anchor='middle', key=None):
        cnts.append(svg_text(x, y, str(n), 'cn' if main else 'cn2', anchor))
    mid_y, rev_y = y0 + 64, y0 + 112
    for a, b in zip(CORE, CORE[1:]):
        xa, xb = BX[a] + BW, BX[b]
        n = flow_n(a, b)
        fl.append(bundle([(xa + 2, mid_y), (xb - 2, mid_y)], 3, 'bm'))
        count((xa + xb) / 2, mid_y - 12, n, True)
        nr = flow_n(b, a)
        if nr:
            fl.append(bundle([(xb - 2, rev_y), (xa + 2, rev_y)], 2, 'bs'))
            count((xa + xb) / 2, rev_y + 28, nr, False)
    # outside forces into Wealth and Voice
    for t, x in (('A', 120), ('B', 360)):
        fl.append(bundle([(x, hx + 2), (x, y0 - 2)], 2, 'bs'))
        count(x + 10, (hx + y0) / 2 + 8, flow_n('X', t), False, 'start')
    # Voice over Elections to Checks and Policy
    yb_e, yb_d = 112, 148
    fl.append(bundle([(440, y0 - 2), (440, yb_e), (BX['E'] + 34, yb_e), (BX['E'] + 34, y0 - 2)], 2, 'bs'))
    count(BX['E'] - 60, yb_e - 8, flow_n('B', 'E'), False)
    assert flow_n('B', 'D') == flow_n('D', 'B')
    fl.append(bundle([(470, y0 - 2), (470, yb_d), (BX['D'] + 43, yb_d), (BX['D'] + 43, y0 - 2)], 2, 'bs', ('start', 'end')))
    cnts.append(svg_text(665, yb_d - 8, f'{flow_n("B", "D")} each way', 'cn3', 'middle'))
    # Wealth and Your household
    fl.append(bundle([(96, yb + 2), (96, y3 - 2)], 2, 'bs'))
    count(84, (yb + y3) / 2 + 8, flow_n('A', 'EC'), False, 'end')
    fl.append(bundle([(150, y3 - 2), (150, yb + 2)], 2, 'bs'))
    count(162, (yb + y3) / 2 + 8, flow_n('EC', 'A'), False, 'start')
    # Checks and Technology
    fl.append(bundle([(880, yb + 2), (880, y3 - 2)], 2, 'bs'))
    count(868, (yb + y3) / 2 + 8, flow_n('D', 'TC'), False, 'end')
    fl.append(bundle([(940, y3 - 2), (940, yb + 2)], 2, 'bs'))
    count(952, (yb + y3) / 2 + 8, flow_n('TC', 'D'), False, 'start')
    # Checks into Your household
    ymid = yb + 46
    fl.append(bundle([(836, yb + 2), (836, ymid), (700, ymid), (700, y3 - 2)], 2, 'bs'))
    count(768, ymid - 8, flow_n('D', 'EC'), False)
    # Technology into Your household
    ytc = y3 + 112
    fl.append(bundle([(tcx - 2, ytc), (ecx + ecw + 2, ytc)], 2, 'bs'))
    count((tcx + ecx + ecw) / 2, ytc - 10, flow_n('TC', 'EC'), False)
    # the return line: Policy back to Wealth, around the whole system
    yr = yend + 30
    ry = mid_y + 26
    fl.append(bundle([(BX['E'] + BW + 2, ry), (W - 14, ry), (W - 14, yr), (14, yr), (14, ry), (BX['A'] - 2, ry)], 3, 'bm'))
    ret = f'{flow_n("E", "A")} connections run back. {ED["opening"]["return"]}'
    cnts.append(svg_text(W / 2, yr + 30, ret, 'rt', 'middle'))
    # notes inside the drawing
    nrows, nh = layout_rows([('mapr', 'The black route is the main circuit, part to part in the order this page reads '
                                      'them. Each number counts the connections that run the way its arrow points.')], 400)
    nx, ny = 236 + 40, yb + 14
    note = draw_rows(nx, ny, nrows, 'start', ' rn')
    lead = f'<path class="leader" d="M{nx - 8} {f(ny + 10)}H{268}V{mid_y + 14}"/>'
    smalls = []
    tc_rest = [(PARTS[t]['plain_name'], flow_n('TC', t)) for t in ('B', 'A') if flow_n('TC', t)]
    tcr = 'Also ' + list_words([f'{n} into {nm}' for nm, n in tc_rest]) + '.'
    smalls.append(svg_text(tcx + tcw - 14, y3 + 30, tcr, 'cp2', 'end'))
    ec_rest = flow_n('E', 'EC')
    smalls.append(svg_text(ecx + ecw - 14, y3 + 30, f'Also {ec_rest} in from Policy.', 'cp2', 'end'))
    H = yr + 44
    desc = ('The eight parts with the flows between them. ' + ' '.join(
        f'{PARTS[a]["plain_name"]} to {PARTS[b]["plain_name"]}: {len(v)}.' for (a, b), v in sorted(
            FLOWS.items(), key=lambda kv: (ORDER.index(kv[0][0]), ORDER.index(kv[0][1])))))
    return (f'<svg class="sumd" data-view="overview" viewBox="0 0 {W} {f(H)}" width="{W}" role="group" '
            f'aria-labelledby="sum-h" aria-describedby="sum-words" data-ak-roving data-ak-nav="spatial">'
            f'{lead}{"".join(fl)}{"".join(out)}{"".join(cnts)}{note}{"".join(smalls)}</svg>'), desc


def flow_n_out(pid):
    return sum(len(v) for (a, _), v in FLOWS.items() if a == pid)


# ------------------------------------------------------------------------------------------------ HTML pieces
def chip(word, code, compact=False):
    return (f'<span class="chip{" compact" if compact else ""}"><span class="k">{e(word)}</span>'
            f'<span class="c">{e(code)}</span></span>')


def grade_glyph(g, w=36):
    """A short sample of a grade's line texture, for keys and labels in text."""
    tex = tex_of(g)
    da = fitted(tex, 2, w)
    dash = f' stroke-dasharray="{da}"' if da else ''
    cap = pattern(tex, 2)[1]
    return (f'<svg class="gg" data-view="glyph" width="{w}" height="10" viewBox="0 0 {w} 10" aria-hidden="true">'
            f'<path d="M0 5H{w}" stroke="currentColor" stroke-width="2" stroke-linecap="{cap}"{dash}/></svg>')


def grade_label(g):
    return f'<span class="gl">{grade_glyph(g)}<span>{e(grade_word(g))}: {e(grade_gloss(g))}</span></span>'


def var_button(c, extra_cls=''):
    say = e(f'{c} {label(c)}. {N[c]["increase_means"]}')
    return (f'<button type="button" class="vbtn{extra_cls}" data-select="var-{c.lower()}" data-node="{c}" '
            f'data-name="{e(label(c))}" aria-label="{say}" data-say="{say}"><span class="vdot" aria-hidden="true">'
            f'</span>{e(label(c))}</button>')


def loop_link(k):
    name = LO[k]['plain_name']
    href = '#loop-r10' if k == 'R10' else f'#loops/loop-{k.lower()}'
    return f'<a href="{href}" class="ll"><span data-loop="{k}" data-name="{e(name)}">{e(name)}</span> <span class="id">{k}</span></a>'


def src_line():
    return f'<p class="src">Atlas V7, snapshot {SNAP_WORDS}.</p>'


def tpl(key, kind, title, body):
    return f'<template data-detail="{key}" data-kind="{e(kind)}" data-title="{e(title)}">{body}</template>'


def link_li(lid, side):
    l = L[lid]
    other = l['to'] if side == 'out' else l['from']
    v = verb(l['polarity'])
    if side == 'out':
        txt = f'{v[0].upper() + v[1:]} {mid(other)}'
    else:
        txt = f'{label(other)} {v} it'
    return (f'<li>{e(txt)} <span class="muted">({lid}, {e(grade_word(l["evidence"]).lower())}, '
            f'{e(delay_words(l["delay"]))})</span></li>')


def tpl_var(c):
    n = N[c]
    p = PARTS[n['part']]
    outs = [k for k, l in L.items() if l['from'] == c]
    ins = [k for k, l in L.items() if l['to'] == c]
    body = [f'<p class="lead">{e(n["increase_means"])}</p>', f'<p>{e(n["description"])}</p>',
            '<dl>', f'<dt>Part</dt><dd>{e(p["plain_name"])} ({e(p["formal_title"])})</dd>',
            f'<dt>V7 title</dt><dd>{e(n["title"])}</dd>',
            f'<dt>Kind</dt><dd>{e(n["kind_plain"])}</dd>']
    if n.get('indicator'):
        body.append(f'<dt>Measured by</dt><dd>{e(n["indicator"])}</dd>')
    body.append('</dl>')
    if n.get('why'):
        body.append(f'<h3>Why it matters</h3><p>{e(n["why"])}</p>')
    if outs:
        body.append(f'<h3>Pushes on {len(outs)}</h3><ul>' + ''.join(link_li(k, 'out') for k in outs) + '</ul>')
    if ins:
        body.append(f'<h3>Pushed by {len(ins)}</h3><ul>' + ''.join(link_li(k, 'in') for k in ins) + '</ul>')
    if n['loops']:
        body.append('<h3>Loops it sits on</h3><ul>' + ''.join(
            f'<li>{e(LO[k]["plain_name"])} ({k})</li>' for k in n['loops']) + '</ul>')
    if n['part'] == 'C':
        body.append('<p class="next"><a href="#area-c">Open the Elections page</a></p>')
    body.append(src_line())
    return tpl(f'var-{c.lower()}', f'Variable {c}', n['label'], ''.join(body))


def tpl_part(pid):
    p = PARTS[pid]
    out = sum(len(v) for (a, _), v in FLOWS.items() if a == pid)
    inn = sum(len(v) for (_, b), v in FLOWS.items() if b == pid)
    body = []
    if p['plain_question']:
        body.append(f'<p class="lead">{e(p["plain_question"])}</p>')
    body.append(f'<p class="muted">{e(p["formal_title"])}. {e(p["chapter"])}.</p>')
    body.append(f'<p>{e(p["story"])}</p>')
    body.append('<dl>' + f'<dt>Conditions</dt><dd>{len(p["nodes"])}</dd>'
                + f'<dt>Inside the part</dt><dd>{INSIDE[pid]} connections</dd>'
                + f'<dt>Going out</dt><dd>{out} connections</dd><dt>Coming in</dt><dd>{inn} connections</dd></dl>')
    body.append('<h3>Its conditions</h3><ul>' + ''.join(
        f'<li><button type="button" class="pk" data-ak-pick="var-{c.lower()}">{e(label(c))}</button></li>'
        for c in p['nodes']) + '</ul>')
    if HOME.get(pid):
        body.append('<h3>Loops that start here</h3><ul>' + ''.join(
            f'<li>{e(LO[k]["plain_name"])} ({k})</li>' for k in HOME[pid]) + '</ul>')
    if pid == 'C':
        body.append('<p class="next"><a href="#area-c">Open the Elections page</a></p>')
    body.append(src_line())
    return tpl(f'part-{pid.lower()}', 'Part of the system', p['plain_name'], ''.join(body))


def tpl_pathway(pw):
    refs = pw['model_refs']
    parts_ = []
    for c in refs['nodes']:
        pp = PART_OF[c]
        if pp not in parts_:
            parts_.append(pp)
    hub = next(h for h in ED['hubs'] if h['id'] == pw['hub'])
    body = [f'<p class="muted">{e(hub["title"])} · {e(pw["title"])}</p>', f'<p>{e(pw["short_answer"])}</p>',
            '<h3>Where it sits in the atlas</h3><dl>',
            f'<dt>Parts</dt><dd>{e(list_words([PARTS[x]["plain_name"] for x in parts_]))}</dd>',
            f'<dt>Conditions</dt><dd>{e(list_words([label(c) for c in refs["nodes"]]))}</dd>']
    if refs['loops']:
        body.append(f'<dt>Loops</dt><dd>{e(list_words([LO[k]["plain_name"] + " (" + k + ")" for k in refs["loops"]]))}</dd>')
    if refs['reforms']:
        body.append(f'<dt>Reforms</dt><dd>{e(list_words([RF[r]["title"] + " (" + r + ")" for r in refs["reforms"]]))}</dd>')
    body.append(f'<dt>Problems tracked</dt><dd>{len(refs["issues"])}</dd></dl>')
    nexts = []
    if any(PART_OF[c] == 'C' for c in refs['nodes']):
        nexts.append('<a href="#area-c">Open the Elections page</a>')
    if 'R10' in refs['loops']:
        nexts.append('<a href="#loop-r10">Open the safe-seat loop</a>')
    if 'R-01' in refs['reforms']:
        nexts.append('<a href="#reform-r01">Open reform R-01</a>')
    if nexts:
        body.append('<p class="next">' + ' · '.join(nexts) + '</p>')
    body.append(src_line())
    return tpl(f'pw-{pw["id"].lower()}', 'Everyday question', pw['question'], ''.join(body))


def steps_list(k):
    l = LO[k]
    labs = station_labels(k)
    n = len(labs)
    items = []
    for i, st in enumerate(l['steps']):
        a, b = labs[i], labs[(i + 1) % n]
        if st['id']:
            ll = L[st['id']]
            items.append(f'<li><strong>{e(st["id"])}</strong> {e(ll["name"])}. {e(a)} {verb(ll["polarity"])} '
                         f'{e(mid(b) if b in [label(c) for c in N] else b)} ({sign_char(ll["polarity"])}); '
                         f'{e(grade_word(ll["evidence"]).lower())}, {e(delay_words(ll["delay"]))}.</li>')
        else:
            items.append(f'<li>{e(a)} {verb(st["polarity"])} {e(b[0].lower() + b[1:])} ({sign_char(st["polarity"])}); '
                         f'a sketched step with no number or grade.</li>')
    return '<ol class="steps">' + ''.join(items) + '</ol>'


def tpl_loop(k):
    l = LO[k]
    body = [f'<p class="muted">{e(kind_line(k))} · {e(l["title"])}</p>',
            f'<p class="lead">{e(read_aloud(k))}</p>', f'<p>{e(l["summary"])}</p>',
            '<h3>Step by step</h3>' + steps_list(k),
            f'<h3>How sure is this?</h3><p>{e(l["evidence_summary"])}</p>',
            f'<h3>Keep in mind</h3><p>{e(l["qualification"])}</p>']
    d = disclosure(k)
    if d:
        body.append(f'<p class="muted">{e(d)}</p>')
    body.append('<dl>' + f'<dt>Now</dt><dd>{e(direction_word(k))}. {e(l["reference_mode"] or "")}</dd>'
                + f'<dt>One turn</dt><dd>{e(l["delay_word"])}</dd>'
                + f'<dt>Weakest</dt><dd>{e(weakest_text(k))}</dd></dl>')
    if l['reforms']:
        body.append('<h3>Reforms aimed at it</h3><ul>' + ''.join(
            f'<li>{e(RF[r]["title"])} ({r})</li>' for r in l['reforms']) + '</ul>')
    if k == 'R10':
        body.append('<p class="next"><a href="#loop-r10">Open the safe-seat loop, step by step</a></p>')
    body.append(src_line())
    return tpl(f'loop-{k.lower()}', f'Loop {k} · {l["kind_word"]}', l['plain_name'], ''.join(body))


def tpl_link(lid):
    l = L[lid]
    body = [f'<p class="lead">{e(l["plain"] or l["name"])}</p>',
            '<dl>', f'<dt>From</dt><dd>{l["from"]} {e(label(l["from"]))}</dd>',
            f'<dt>To</dt><dd>{l["to"]} {e(label(l["to"]))}</dd>']
    if l['polarity'] in ('+', '-'):
        body.append(f'<dt>Sign</dt><dd>{sign_char(l["polarity"])}, it {verb(l["polarity"])} it. '
                    f'{e(l.get("sign_meaning") or "")}</dd>')
    body.append(f'<dt>Kind</dt><dd>{e(l["type"].capitalize())}</dd>'
                f'<dt>Delay</dt><dd>{e(delay_words(l["delay"]))}</dd>'
                f'<dt>Evidence</dt><dd>{grade_label(l["evidence"])}</dd></dl>')
    if l.get('mechanism'):
        body.append(f'<h3>How it works</h3><p>{e(l["mechanism"])}.</p>' if not l['mechanism'].endswith('.') else
                    f'<h3>How it works</h3><p>{e(l["mechanism"])}</p>')
    if l.get('qualification'):
        body.append(f'<h3>Keep in mind</h3><p>{e(l["qualification"])}</p>')
    if l['loops']:
        body.append('<h3>Loops</h3><ul>' + ''.join(f'<li>{e(LO[k]["plain_name"])} ({k})</li>' for k in l['loops']) + '</ul>')
    body.append(f'<p class="muted">{e(acc.SIGN_RULE)}</p>')
    body.append(src_line())
    return tpl(f'link-{lid.lower()}', f'Connection {lid}', l['name'], ''.join(body))


def effects_dl(r):
    rows = ''.join(f'<dt>{e(ED["families"][k])}</dt><dd>{e(effect_words(v))}</dd>' for k, v in r['effects'].items())
    return f'<dl class="fx">{rows}</dl>'


def tpl_reform(rid):
    r = RF[rid]
    tl = list_words([f'{t} {label(t)}' if t in N else f'{t} {L[t]["name"]}' if t in L else t for t in r['targets']])
    body = [f'<p class="lead">{e(" ".join(sentences(r["summary"])[:2]))}</p>',
            f'<dl><dt>Acts on</dt><dd>{e(tl)}</dd><dt>Loops</dt><dd>{e(", ".join(r["loops"]))}</dd>'
            f'<dt>Problem evidence</dt><dd>{e(grade_word(r["problem_evidence"]["grade"]))}</dd>'
            f'<dt>Remedy evidence</dt><dd>{e(grade_word(r["remedy_evidence"]["grade"]))}</dd></dl>',
            '<h3>Likely effects, never added together</h3>' + effects_dl(r)]
    if rid in INTEREST and r['interest_note']:
        body.append(f'<p class="disc"><strong>Disclosure.</strong> {e(INTEREST[rid])}</p>')
    if rid == 'R-01':
        body.append('<p class="next"><a href="#reform-r01">Open the full profile of R-01</a></p>')
    body.append(src_line())
    return tpl(f'reform-{rid.lower()}', f'Reform {rid}', r['title'], ''.join(body))


# ------------------------------------------------------------------------------------------------ the overview
# Studio drafts (named as such in the notes). Every count inside them is printed from the data.
OV_HEAD = 'Wealth at the top can shape the rules that add to it.'


def ov_deck():
    return (f'This atlas follows {cnt("connections", COUNTS["connections"])} connections among '
            f'{cnt("variables", COUNTS["variables"])} conditions, from what a household earns to who writes the rules. '
            f'Read its eight parts in order below. Each one pushes on the next, and policy feeds back into wealth.')


def ov_key():
    return ('<aside class="key" aria-labelledby="key-h"><h2 id="key-h" class="eyebrow">How to read this page</h2>'
            '<p>Each part of the system has a plain name, a question and the conditions inside it. A condition is '
            'something that can rise or fall, such as safe seats or rent.</p>'
            '<p>Arrows carry the count of connections from one part to the next. The route in black is the circuit the '
            'headline follows; gray is the rest. Open a part to see each connection and how strong its evidence is.</p>'
            '<p><a href="#how-to-read">How to read the atlas</a></p></aside>')


def ov_chain():
    items = []
    for pid in ORDER:
        p = PARTS[pid]
        num = str(NUM[pid]) if pid in NUM else ''
        q = p['plain_question'] or p['chapter']
        items.append(f'<li><button type="button" class="cj" data-jump="part-{pid.lower()}-block">'
                     f'<span class="n" aria-hidden="true">{num or "→"}</span><span class="nm">{e(p["plain_name"])}</span>'
                     f'<span class="q">{e(q)}</span></button></li>')
    return ('<nav class="chain" aria-label="The eight parts in reading order"><ol>' + ''.join(items) + '</ol></nav>')


def flow_ex(a, b, k=2):
    ids = flow_examples(a, b, k)
    return '<ul class="ex">' + ''.join(
        f'<li><span class="lnm">{e(L[x]["name"])}</span> <span class="muted">{x} · '
        f'{e(grade_word(L[x]["evidence"]).lower())}</span></li>' for x in ids) + '</ul>'


def other_flows(pid, shown):
    rest = [(t, flow_n(pid, t)) for t in ORDER if t != pid and (pid, t) not in shown and flow_n(pid, t)]
    if not rest:
        return ''
    return (f'<p class="also">{e(PARTS[pid]["plain_name"])} also pushes on '
            + e(list_words([f'{PARTS[t]["plain_name"]} ({n})' for t, n in rest])) + '.</p>')


def part_block(pid):
    p = PARTS[pid]
    num = NUM.get(pid)
    mark = f'<span class="dot{" open" if not num else ""}">{num or ""}</span>'
    loops_here = HOME.get(pid, [])
    lead = story_lead(p)
    meta = [f'{cnt("custom:part-vars-" + pid, len(p["nodes"]))} conditions']
    if INSIDE[pid]:
        meta.append(f'{cnt("custom:part-inside-" + pid, INSIDE[pid])} connections inside')
    if loops_here:
        meta.append(f'{cnt("custom:part-loops-" + pid, len(loops_here))} {plural(len(loops_here), "loop starts", "loops start")} here')
    if pid == 'EC':
        groups = ''.join(f'<li class="grp"><p class="gt">{e(g["title"])}</p><ul class="vlist" data-ak-roving data-ak-nav="sequence">'
                         + ''.join(f'<li>{var_button(c)}</li>' for c in g['nodes']) + '</ul></li>' for g in p['groups'])
        vars_ = f'<ul class="groups">{groups}</ul>'
    else:
        vars_ = ('<ul class="vlist" data-ak-roving data-ak-nav="sequence">'
                 + ''.join(f'<li>{var_button(c)}</li>' for c in p['nodes']) + '</ul>')
    loops_html = ''
    if loops_here:
        loops_html = ('<p class="lh"><span class="lbl">Loops that start here:</span> '
                      + ', '.join(loop_link(k) for k in loops_here) + '</p>')
    q = p['plain_question']
    go = ''
    if pid == 'C':
        go = (f'<p class="go"><a href="#area-c">Open Elections: its {nw(len(p["nodes"]))} conditions, '
              f'{nw(len(C_LOOPS))} loops, {len(C_ISSUES)} problems and {len(C_REFORMS)} reforms</a></p>')
    else:
        go = (f'<p class="go2"><button type="button" class="tl" data-select="part-{pid.lower()}" '
              f'aria-label="Read all of {e(p["plain_name"])}">Read all of {e(p["plain_name"])}</button></p>')
    return (f'<article class="pblock" id="part-{pid.lower()}-block" data-p="{pid}" aria-labelledby="ph-{pid.lower()}">'
            f'<div class="mk" aria-hidden="true">{mark}</div>'
            f'<div class="pname"><p class="eyebrow">{"Part " + str(num) + " · " if num else ""}{e(p["formal_title"])}</p>'
            f'<h3 class="pn" id="ph-{pid.lower()}"><span data-part="{pid}" data-name="{e(p["plain_name"])}">{e(p["plain_name"])}</span></h3>'
            + f'<p class="pqq">{e(q or p["text"])}</p>'
            + f'</div><div class="pstory"><p>{e(lead)}</p><p class="meta">{" · ".join(meta)}</p>{loops_html}{go}</div>'
            f'<div class="pvars"><p class="vh">{"Its conditions" if pid != "X" else "The five forces"}</p>{vars_}</div></article>')


def flow_row(kind, pid, html_):
    return (f'<div class="pflow {kind}" data-flow="{pid}"><div class="mk" aria-hidden="true"></div>'
            f'<div class="fbody">{html_}</div></div>')


def fig(n, key):
    return f'<p class="fig" aria-hidden="false">{cnt(key, n)}</p>'


def circuit():
    rows = []
    # outside forces
    rows.append(part_block('X'))
    xs = [(t, flow_n('X', t)) for t in ORDER if t != 'X' and flow_n('X', t)]
    xs.sort(key=lambda kv: -kv[1])
    tot = sum(n for _, n in xs)
    rows.append(flow_row('side', 'X', fig(tot, 'custom:flow-x-out')
                         + f'<div class="ftxt"><p class="fl">connections press in from outside: '
                         + e(list_words([f'{n} on {PARTS[t]["plain_name"]}' for t, n in xs])) + '.</p>'
                         + flow_ex('X', 'A', 1) + '</div>'))
    shown = set()
    for a, b in zip(CORE, CORE[1:]):
        rows.append(part_block(a))
        shown.add((a, b))
        n = flow_n(a, b)
        rows.append(flow_row('main', a, fig(n, f'custom:flow-{a}-{b}')
                             + f'<div class="ftxt"><p class="fl">connections run from {e(PARTS[a]["plain_name"])} to '
                             f'{e(PARTS[b]["plain_name"])}, such as</p>' + flow_ex(a, b)
                             + other_flows(a, {(a, b)}) + '</div>'))
    rows.append(part_block('E'))
    n_ec, n_back = flow_n('E', 'EC'), flow_n('E', 'A')
    rows.append(flow_row('side', 'E', fig(n_ec, 'custom:flow-E-EC')
                         + f'<div class="ftxt"><p class="fl">{plural(n_ec, "connection runs", "connections run")} on to '
                         f'{e(PARTS["EC"]["plain_name"])}:</p>' + flow_ex('E', 'EC', 1)
                         + f'<p class="fl back"><span class="fig2">{cnt("custom:flow-E-A", n_back)}</span> run straight back to '
                         f'{e(PARTS["A"]["plain_name"])}, on the line at left. {e(ED["opening"]["return"])}</p>'
                         + flow_ex('E', 'A') + other_flows('E', {('E', 'EC'), ('E', 'A')}) + '</div>'))
    rows.append(part_block('EC'))
    n7 = flow_n('EC', 'A')
    rows.append(flow_row('back', 'EC', fig(n7, 'custom:flow-EC-A')
                         + f'<div class="ftxt"><p class="fl">connections run from {e(PARTS["EC"]["plain_name"])} back up to '
                         f'{e(PARTS["A"]["plain_name"])}, on the line at left, and the circuit turns again. Such as</p>'
                         + flow_ex('EC', 'A') + '</div>'))
    n_tc = flow_n('TC', 'EC')
    rows.append(flow_row('up', 'TC', fig(n_tc, 'custom:flow-TC-EC')
                         + f'<div class="ftxt"><p class="fl">connections run up from {e(PARTS["TC"]["plain_name"])} into '
                         f'{e(PARTS["EC"]["plain_name"])}, such as</p>' + flow_ex('TC', 'EC')
                         + other_flows('TC', {('TC', 'EC')})
                         + f'<p class="also">{flow_n("D", "TC")} lines of authority run the other way, from '
                         f'{e(PARTS["D"]["plain_name"])}: they say who decides the rules these systems run under.</p>'
                         + '</div>'))
    rows.append(part_block('TC'))
    sk = HOME.get('SK', [])
    sk_note = (f'<p class="sk-note">{nw(len(sk), True)} more loops are sketches, without a complete numbered chain: '
               + ', '.join(loop_link(k) for k in sk) + '. <a href="#loops">See all 23 loops</a>.</p>')
    assert all(flow_n('D', 'TC') == sum(1 for x in FLOWS[('D', 'TC')] if L[x]['type'] == 'authority') for _ in [0])
    return ('<section class="circuit" aria-labelledby="circ-h"><header class="sec-head"><p class="eyebrow">How the circuit runs</p>'
            '<h2 id="circ-h" class="headline">Read the system in the order its effects travel.</h2>'
            '<p class="lede">Outside forces press in from the top. Each part then hands something on to the next, from wealth '
            'down to policy, and policy lands in your household. The line at left carries part of it back to wealth.</p></header>'
            '<div class="cgrid" data-circuit><svg class="spine" data-view="overview" aria-hidden="true" focusable="false"></svg>'
            + ''.join(rows) + '</div>' + sk_note + '</section>')


def whole():
    svg, desc = summary_diagram()
    words = []
    for (a, b), v in sorted(FLOWS.items(), key=lambda kv: (ORDER.index(kv[0][0]), ORDER.index(kv[0][1]))):
        words.append(f'<li>{e(PARTS[a]["plain_name"])} to {e(PARTS[b]["plain_name"])}: {len(v)} '
                     f'{plural(len(v), "connection", "connections")}</li>')
    inside = ', '.join(f'{e(PARTS[p]["plain_name"])} {INSIDE[p]}' for p in ORDER if INSIDE[p])
    big = max(((a, b) for a, b in {tuple(sorted(k, key=ORDER.index)) for k in FLOWS}),
              key=lambda ab: flow_n(*ab) + flow_n(ab[1], ab[0]))
    big_n = flow_n(*big) + flow_n(big[1], big[0])
    return ('<section class="whole" aria-labelledby="sum-h"><header class="sec-head"><p class="eyebrow">The whole system</p>'
            f'<h2 id="sum-h" class="headline">The busiest exchange runs between {e(PARTS[big[0]]["plain_name"].lower())} '
            f'and {e(PARTS[big[1]]["plain_name"].lower())}: {cnt("custom:biggest-pair", big_n)} connections.</h2>'
            f'<p class="lede">Here are all eight parts on one page, with only the flows between them. '
            f'{cnt("custom:cross-part", CROSS)} connections cross from one part to another and '
            f'{cnt("custom:inside-part", sum(INSIDE.values()))} stay inside a part; tap a part to read it.</p></header>'
            f'<div class="ak-scroll sumwrap" role="region" tabindex="0" aria-label="The whole system, drawing" id="sum-region" style="--ak-min:1312px">{svg}</div>'
            '<p class="fullbtn"><button type="button" class="ak-btn" data-ak-full="sum-region">View the drawing full size</button></p>'
            '<p class="ak-readout" data-ak-readout>Point at or tab to a part to read its name here.</p>'
            f'<details class="words" id="sum-words"><summary>The flows in words</summary><p>{e(desc.split(". ")[0])}.</p>'
            f'<ol class="cols">{"".join(words)}</ol><p>Inside each part: {inside}.</p></details></section>')


def bill():
    hubs = []
    for h in ED['hubs']:
        qs = ''.join(
            f'<li><button type="button" class="qb" data-select="pw-{pid.lower()}" aria-label="{e(pw["question"])}">'
            f'{e(pw["question"])}</button></li>'
            for pid in h['pathways'] for pw in [next(x for x in ED['pathways'] if x['id'] == pid)])
        hubs.append(f'<section class="hub" aria-labelledby="hub-{h["id"]}"><p class="eyebrow">{e(h["title"])}</p>'
                    f'<h3 class="hq" id="hub-{h["id"]}">{e(h["question"])}</h3>'
                    f'<ul class="qs" data-ak-roving data-ak-nav="sequence">{qs}</ul></section>')
    n = len(ED['pathways'])
    return ('<section class="bill" aria-labelledby="bill-h"><header class="sec-head"><p class="eyebrow">Start from your own bill</p>'
            f'<h2 id="bill-h" class="headline">{nw(n, True) if n <= 12 else cnt("pathways", n)} everyday questions lead into the map.</h2>'
            f'<p class="lede">Pick the one closest to your life. Each answers in plain words, then shows where it sits in the '
            f'system: which parts, which loops and which reforms.</p></header>'
            f'<div class="hubs">{"".join(hubs)}</div></section>')


def view_overview():
    return ('<section class="view" data-view-root="overview" data-crumb="Overview">'
            '<div class="headblock"><div class="hl">'
            f'<p class="eyebrow">{e(ED["opening"]["kicker"])}</p>'
            f'<h1 class="display" data-ak-heading>{e(OV_HEAD)}</h1><p class="deck">{ov_deck()}</p></div>{ov_key()}</div>'
            + ov_chain() + circuit() + whole() + bill() + '</section>')


# ------------------------------------------------------------------------------------------------ Elections
AREA_HEAD = 'When the primary settles a seat, the risk of losing office falls.'


def loop_card(k, W=350, view='loops', heading='h3'):
    l = LO[k]
    d = disclosure(k)
    btn = (f'<a class="tl" href="#loop-r10">Open the full loop, step by step</a>' if k == 'R10' and view != 'loops' else
           f'<button type="button" class="tl" data-select="loop-{k.lower()}" aria-label="Read loop {k}, {e(l["plain_name"])}">'
           f'Read the loop</button>')
    if k == 'R10' and view == 'loops':
        btn = (f'<button type="button" class="tl" data-select="loop-r10" aria-label="Read loop R10, {e(l["plain_name"])}">'
               f'Read the loop</button> <a class="tl" href="#loop-r10">Open it step by step</a>')
    steps = ' '.join(s['id'] for s in l['steps']) if not l['conceptual'] else 'sketch'
    return (f'<article class="lcard" data-loop="{k}" data-steps="{steps}" aria-labelledby="lc-{view}-{k}">'
            f'<p class="lk">{chip("Loop", k, True)}<span>{e(kind_line(k))}</span></p>'
            f'<{heading} class="ln" id="lc-{view}-{k}"><span data-loop="{k}" data-name="{e(l["plain_name"])}">{e(l["plain_name"])}</span></{heading}>'
            f'<p class="lt" data-loop="{k}" data-name="{e(l["title"])}">{e(l["title"])}</p>'
            f'<div class="cwrap">{cycle_small(k, W, view=view)}</div>'
            f'<p class="ra">{e(read_aloud(k))}</p>'
            f'<p class="ls">{e(status_line(k))}</p>'
            + (f'<p class="ld">{e(d)}</p>' if d else '') + f'<p class="la">{btn}</p></article>')


def issue_item(i):
    pe, fe = i.get('problem_example'), i.get('fix_example')
    g = gk(i['grade'])
    ex = (f'<span class="ie">{e(pe["headline"])} <span class="muted">({e(pe["where"])}, {e(pe["when"])})</span></span>'
          if pe else '<span class="ie muted">No worked example in the record</span>')
    tags = 'Touches ' + list_words([label(c).lower() if not label(c)[1:2].isupper() else label(c) for c in i['nodes'] if c in C_SET])
    body = [f'<p>{e(i["summary"])}</p>']
    if pe:
        src = pe.get('source') or {}
        body.append(f'<div class="exm"><p class="eyebrow">The problem, in one place</p><h5>{e(pe["headline"])}</h5>'
                    f'<p>{e(pe["text"])}</p><p class="muted">{e(pe["where"])}, {e(pe["when"])}. Source: '
                    f'{e(src.get("publisher") or "")}, {e(src.get("title") or "")} ({e(src.get("year") or "")}).</p></div>')
    if fe:
        src = fe.get('source') or {}
        body.append(f'<div class="exm"><p class="eyebrow">A fix tried somewhere</p><h5>{e(fe["headline"])}</h5>'
                    f'<p>{e(fe["text"])}</p>' + (f'<p><strong>Result.</strong> {e(fe["result"])}</p>' if fe.get('result') else '')
                    + f'<p class="muted">{e(fe["where"])}, {e(fe["when"])}. Source: {e(src.get("publisher") or "")}, '
                    f'{e(src.get("title") or "")} ({e(src.get("year") or "")}).</p></div>')
    body.append(f'<dl><dt>How it works</dt><dd>{e(i["mechanism"])}</dd>'
                f'<dt>Evidence</dt><dd>{e(i["evidence_note"])}</dd>'
                f'<dt>Proposed response</dt><dd>{e(i["response"])} <span class="muted">Who acts: {e(i["actor"])}.</span></dd>'
                f'<dt>Tradeoff</dt><dd>{e(i["tradeoff"])}</dd>'
                f'<dt>How to judge it</dt><dd>{e(i["success_measure"])}</dd></dl>')
    return (f'<li><details class="iss"><summary><span class="it" data-issue="{i["id"]}" data-name="{e(i["title"])}">'
            f'{e(i["title"])}</span>{ex}<span class="ig">{grade_glyph(g, 28)}{e(grade_word(g))}</span>'
            f'<span class="itag">{e(tags)}</span></summary><div class="ib">{"".join(body)}</div></details></li>')


def effects_sentence(r):
    nz = [(k, v) for k, v in r['effects'].items() if v.strip() != '0']
    zs = [ED['families'][k].lower() for k, v in r['effects'].items() if v.strip() == '0']
    bits = [f'{ED["families"][k]}: {effect_words(v)}' for k, v in nz]
    out = '; '.join(bits) + ('.' if bits else '')
    if zs:
        out += f' No expected effect on {list_words(zs)}.'
    return out.strip()


def reform_card(r):
    tl = []
    for t in r['targets']:
        if t in N:
            tl.append(f'{label(t)} ({t})')
        elif t in L:
            tl.append(f'{L[t]["name"]} ({t})')
    open_ = ('<p class="la"><a class="tl" href="#reform-r01">Open the full profile</a></p>' if r['id'] == 'R-01' else '')
    disc = (f'<p class="disc"><strong>Disclosure.</strong> {e(INTEREST[r["id"]])}</p>'
            if r['interest_note'] and r['id'] in INTEREST else '')
    return (f'<article class="rcard" data-reform="{r["id"]}" data-targets="{" ".join(r["targets"])}">'
            f'<p class="lk">{chip("Reform", r["id"], True)}<span>{e(r["band"].capitalize())}</span></p>'
            f'<h4 class="rn" data-reform="{r["id"]}" data-name="{e(r["title"])}">{e(r["title"])}</h4>'
            f'<p><span class="lbl">What it changes.</span> {e(first_sentence(r["summary"]))}</p>'
            f'<p class="muted"><span class="lbl">Acts on</span> {e(list_words(tl))}.</p>'
            f'<p class="fxl">{e(effects_sentence(r))}</p>'
            f'{disc}{open_}</article>')


def view_area():
    p = PARTS['C']
    cards = []
    for c in p['nodes']:
        n = N[c]
        cards.append(f'<li class="vcard">{chip("Variable", c, True)}'
                     f'<h4 class="vt">{var_button(c, " big")}</h4>'
                     + (f'<p class="vf">{e(n["title"])}</p>' if n['title'] != n['label'] else '')
                     + f'<p class="vm">{e(n["increase_means"])}</p><p class="vd">{e(n["description"])}</p></li>')
    by_part = lambda lids, side: sorted(lids, key=lambda x: (ORDER.index(PART_OF[L[x]['from' if side == 'in' else 'to']]), x))
    def group(lids, side):
        out, cur = [], None
        for lid in by_part(lids, side):
            far = PART_OF[L[lid]['from' if side == 'in' else 'to']]
            if far != cur:
                if cur is not None:
                    out.append('</ul></div>')
                cur = far
                fp = PARTS[far]
                k = sum(1 for x in lids if PART_OF[L[x]['from' if side == 'in' else 'to']] == far)
                out.append(f'<div class="cg"><h4 class="cgh">{"From" if side == "in" else "To"} '
                           f'<span data-part="{far}" data-name="{e(fp["plain_name"])}">{e(fp["plain_name"])}</span> '
                           f'<span class="muted">{k}</span></h4><ul class="crows">')
            ll = L[lid]
            out.append(f'<li class="crw"><div class="cdr">{conn_row(lid, side, 560)}</div><div class="cdn">{conn_row(lid, side, 350)}</div>'
                       f'<p class="cn"><span class="lnm">{e(ll["name"])}</span> <span class="muted">{lid} · '
                       f'{e(grade_word(ll["evidence"]).lower())} · {e(delay_words(ll["delay"]))}</span></p></li>')
        out.append('</ul></div>')
        return ''.join(out)
    loops = ''.join(f'<li>{loop_card(k, 350, "area-c", "h4")}</li>' for k in C_LOOPS)
    groups = defaultdict(list)
    for i in C_ISSUES:
        groups[i['domain']].append(i)
    dom = {d['id']: d for d in ED['domains']}
    iss_html = []
    for d_id in sorted(groups, key=lambda d: -len(groups[d])):
        items = sorted(groups[d_id], key=lambda i: i['id'])
        iss_html.append(f'<section class="igrp" aria-labelledby="ig-{d_id}"><h4 class="igh" id="ig-{d_id}">'
                        f'{e(dom[d_id]["title"])} <span class="muted">{len(items)}</span></h4>'
                        f'<p class="igq">{e(dom[d_id]["everyday_question"])}</p>'
                        f'<ul class="ilist">{"".join(issue_item(i) for i in items)}</ul></section>')
    reforms = ''.join(f'<li>{reform_card(r)}</li>' for r in sorted(C_REFORMS, key=lambda r: r['id']))
    words = ''.join(f'<li>{e(link_sentence(lid))}</li>' for lid in C_INSIDE + ['L23', 'L54'])
    jumps = [('ar-what', 'What it is'), ('ar-draw', 'How it works'), ('ar-flows', 'What pushes on it'),
             ('ar-loops', f'{nw(len(C_LOOPS), True)} loops'), ('ar-issues', f'{len(C_ISSUES)} problems'),
             ('ar-reforms', f'{len(C_REFORMS)} reforms')]
    jump_html = '<nav class="jumps" aria-label="On this page"><ul>' + ''.join(
        f'<li><button type="button" class="jb" data-jump="{a}">{e(t)}</button></li>' for a, t in jumps) + '</ul></nav>'
    return ('<section class="view" data-view-root="area-c" data-crumb="Elections" data-parent="overview" hidden>'
            '<div class="headblock"><div class="hl">'
            f'<p class="eyebrow">Part 3 of the circuit · <span data-part="C" data-name="{e(p["formal_title"])}">{e(p["formal_title"])}</span></p>'
            f'<h1 class="headline xl" data-ak-heading>{e(AREA_HEAD)}</h1>'
            f'<p class="deck">{e(" ".join(sentences(p["story"])[:2]))}</p></div>'
            f'<aside class="key"><p class="eyebrow">This part in numbers</p><dl class="nums">'
            f'<dt>{cnt("custom:c-vars", len(p["nodes"]))}</dt><dd>conditions</dd>'
            f'<dt>{cnt("custom:c-inside", len(C_INSIDE))}</dt><dd>connections inside</dd>'
            f'<dt>{cnt("custom:c-in", len(C_IN))}</dt><dd>coming in</dd><dt>{cnt("custom:c-out", len(C_OUT))}</dt><dd>going out</dd>'
            f'<dt>{cnt("custom:c-loops", len(C_LOOPS))}</dt><dd>loops run through it</dd>'
            f'<dt>{cnt("custom:c-issues", len(C_ISSUES))}</dt><dd>problems tracked</dd>'
            f'<dt>{cnt("custom:c-reforms", len(C_REFORMS))}</dt><dd>reforms aimed here</dd></dl></aside></div>'
            + jump_html +
            f'<section class="sec" id="ar-what" aria-labelledby="ar-what-h"><div class="two"><div class="whatq">'
            f'<p class="eyebrow">What it is</p><h2 class="headline" id="ar-what-h"><span data-part="C" data-name="{e(p["plain_name"])}">'
            f'{e(p["plain_name"])}</span>: {e(p["plain_question"].lower()[0] + p["plain_question"][1:] if False else p["plain_question"])}</h2>'
            f'<p class="body">{e(p["story"])}</p></div>'
            f'<ul class="vcards" data-ak-roving data-ak-nav="spatial">{"".join(cards)}</ul></div></section>'
            '<section class="sec" id="ar-draw" aria-labelledby="area-c-draw-h"><p class="eyebrow">How it works</p>'
            f'<h2 class="headline" id="area-c-draw-h">Two loops meet at {e(label("C3").lower())}.</h2>'
            f'<p class="lede">Every connection inside Elections is drawn here, with the accountability loop running out to '
            f'{e(PARTS["D"]["plain_name"])} and back. Tap a condition or an arrow to read it.</p>'
            f'<div class="wide-only"><div class="ak-scroll" role="region" tabindex="0" aria-label="Elections drawing" id="area-region" style="--ak-min:1312px">{area_drawing()}</div></div>'
            f'<div class="narrow-only"><div class="pair" data-ak-roving data-ak-nav="sequence">'
            f'<p class="eyebrow">{e(LO["R10"]["plain_name"])} \u00b7 R10</p>{cycle_small("R10", 350, interactive=True, view="area-c")}'
            f'<p class="eyebrow">{e(LO["B4"]["plain_name"])} \u00b7 B4</p>{cycle_small("B4", 350, interactive=True, view="area-c")}</div>'
            f'<p class="body">Both loops run through {e(label("C3").lower())}. '
            f'{e(re.sub(r"^The loop", "The " + LO["B4"]["plain_name"].lower(), first_sentence(LO["B4"]["qualification"])))}</p></div>'
            '<p class="ak-readout" data-ak-readout>Point at or tab to a condition or an arrow to read it here.</p>'
            f'<details class="words"><summary>The lines in words</summary><ol>{words}</ol></details></section>'
            '<section class="sec" id="ar-flows" aria-labelledby="ar-flows-h"><p class="eyebrow">What pushes on it, and what it pushes on</p>'
            f'<h2 class="headline" id="ar-flows-h">{nw(len(C_IN), True)} connections come in and {nw(len(C_OUT))} go out.</h2>'
            '<p class="lede">Each row reads left to right as a sentence, from the condition that pushes to the one it moves. '
            '<a href="#how-to-read">How to read the lines</a></p>'
            f'<div class="two eq"><div><h3 class="sub">Pushed by</h3>{group(C_IN, "in")}</div>'
            f'<div><h3 class="sub">Pushes on</h3>{group(C_OUT, "out")}</div></div></section>'
            '<section class="sec" id="ar-loops" aria-labelledby="ar-loops-h"><p class="eyebrow">Loops</p>'
            f'<h2 class="headline" id="ar-loops-h">{nw(len(C_LOOPS), True)} loops run through Elections.</h2>'
            '<p class="lede">A loop is a chain of causes that comes back to where it started. Read each one clockwise from the top left.</p>'
            f'<ul class="lgrid" data-ak-roving data-ak-nav="spatial">{loops}</ul></section>'
            '<section class="sec" id="ar-issues" aria-labelledby="ar-issues-h"><p class="eyebrow">Problems</p>'
            f'<h2 class="headline" id="ar-issues-h">{cnt("custom:c-issues", len(C_ISSUES))} problems tracked here, each with a real case.</h2>'
            '<p class="lede">Each record names a problem, a place where it happened and, where one exists, a place that tried a fix. '
            'Open any record to read it.</p>'
            f'<div class="igrid">{"".join(iss_html)}</div></section>'
            '<section class="sec" id="ar-reforms" aria-labelledby="ar-reforms-h"><p class="eyebrow">Reforms</p>'
            f'<h2 class="headline" id="ar-reforms-h">{cnt("custom:c-reforms", len(C_REFORMS))} reforms aim at Elections.</h2>'
            '<p class="lede">Each one acts on a named condition or connection. Effects are rated in four families and never added up.</p>'
            f'<ul class="rgrid">{reforms}</ul></section></section>')


# ------------------------------------------------------------------------------------------------ loop R10
def r10_status_lines():
    l = LO['R10']
    labs = station_labels('R10')
    dirs, back = directions('R10')
    out = []
    for i, st in enumerate(l['steps']):
        ll = L[st['id']]
        a_up, b_up = dirs[i], (dirs[i + 1] if i + 1 < len(dirs) else back)
        a, b = labs[i], labs[(i + 1) % len(labs)]
        out.append((st['id'], f'{st["id"]}, {ll["name"]}. {amount(mid(st["from"]), a_up).capitalize()} means '
                              f'{amount(mid(st["to"]), b_up)}. Sign {sign_char(ll["polarity"])}, '
                              f'{"same way" if ll["polarity"] == "+" else "opposite way"}; '
                              f'{grade_word(ll["evidence"]).lower()}; {delay_words(ll["delay"])}.'))
    return out


def r10_steps_head():
    l = LO['R10']
    strong = sum(1 for s_ in l['steps'] if s_['evidence'] in ('documented', 'well-supported'))
    k = next(i for i, s_ in enumerate(l['steps']) if s_['id'] == l['weakest'][0]) + 1
    ordn = ['first', 'second', 'third', 'fourth'][k - 1]
    return (f'{nw(strong, True)} of its {nw(len(l["steps"]))} steps are documented or well supported; '
            f'the {ordn}, {l["weakest"][0]}, is the weakest.')


def view_r10():
    l = LO['R10']
    codes = station_codes('R10')
    st_lines = r10_status_lines()
    steps = ''.join(f'<li data-ak-step-keys="link-{lid.lower()} var-{L[lid]["to"].lower()}">{e(t)}</li>' for lid, t in st_lines)
    end = (f'The loop is back where it started, so it {l["kind_gloss"]}: {l["kind_word"].lower()}. '
           f'Its weakest step is {l["weakest"][0]}, graded {grade_word(L[l["weakest"][0]]["evidence"]).lower()}.')
    idle = (f'Start at {codes[0]}, {label(codes[0])}, and suppose it rises. Press Play, or Next step to follow one '
            f'numbered connection at a time.')
    rf_items = []
    for rid in l['reforms']:
        r = RF[rid]
        tl = list_words([label(t) if t in N else f'{t}' for t in r['targets']])
        rf_items.append(f'<li><button type="button" class="rb" data-select="reform-{rid.lower()}" data-reform="{rid}" '
                        f'data-targets="{" ".join(r["targets"])}" aria-label="Reform {rid}, {e(r["title"])}. Acts on {e(tl)}.">'
                        f'{chip("Reform", rid, True)}<span class="rbt">{e(r["title"])}</span>'
                        f'<span class="rba">Acts on {e(tl)}</span></button>'
                        + ('<a class="tl" href="#reform-r01">Open the full profile of R-01</a>' if rid == 'R-01' else '') + '</li>')
    table = []
    labs = station_labels('R10')
    for i, st in enumerate(l['steps']):
        ll = L[st['id']]
        table.append(f'<tr><th scope="row"><span class="sn2">{i + 1}</span>{chip("Connection", st["id"], True)}</th>'
                     f'<td data-label="What happens"><p class="lnm">{e(ll["name"])}</p><p>{e(ll["plain"])}</p>'
                     + (f'<p class="muted">{e(ll["qualification"])}</p>' if ll.get('qualification') else '')
                     + f'</td><td class="nowrap" data-label="From and to">{e(labs[i])} <span class="arrow" aria-hidden="true">→</span> {e(labs[(i + 1) % 4])}</td>'
                     f'<td class="nowrap" data-label="Sign"><strong>{sign_char(ll["polarity"])} {verb(ll["polarity"])}</strong></td>'
                     f'<td data-label="Evidence">{grade_label(ll["evidence"])}' + ('<p class="wk">The weakest step</p>' if st['id'] in l['weakest'] else '')
                     + f'</td><td class="nowrap" data-label="Delay">{e(delay_words(ll["delay"]))}</td></tr>')
    return ('<section class="view" data-view-root="loop-r10" data-crumb="Loop R10" data-parent="area-c" '
            'data-ak-reform="reform-r-01" hidden>'
            '<div class="headblock"><div class="hl">'
            f'<p class="eyebrow">Loop R10 · <span data-loop="R10" data-name="{e(l["plain_name"])}">{e(l["plain_name"])}</span> '
            f'· {e(kind_line("R10"))}</p>'
            f'<h1 class="headline xl" id="loop-r10-h" data-ak-heading><span data-loop="R10" data-name="{e(l["title"])}">{e(l["title"])}</span></h1>'
            f'<p class="deck">{e(l["summary"])}</p></div>'
            f'<aside class="key"><p class="eyebrow">Read it aloud</p><p class="ral">{e(read_aloud("R10"))}</p>'
            f'<p class="muted">{e(acc.SIGN_RULE)}</p></aside></div>'
            '<div class="r10">'
            f'<div class="r10-side"><section class="stepper" data-ak-stepper data-ak-hold="3200" data-ak-end="{e(end)}" aria-label="Step through the loop">'
            '<p class="eyebrow">Follow one turn</p><div class="sbtn"><button type="button" class="ak-btn" data-ak-step="play">Play</button>'
            '<button type="button" class="ak-btn" data-ak-step="prev">Previous step</button>'
            '<button type="button" class="ak-btn" data-ak-step="next">Next step</button>'
            '<button type="button" class="ak-btn" data-ak-step="reset">Reset</button></div>'
            f'<p class="sstat" data-ak-step-status aria-live="polite">{e(idle)}</p>'
            f'<ol class="slist" data-ak-step-list>{steps}</ol></section>'
            f'<section class="rfs" aria-labelledby="r10-rf-h"><p class="eyebrow" id="r10-rf-h">Where reforms act</p>'
            f'<p class="muted">The red marks show where {e(RF["R-01"]["short"].lower())}, reform R-01, acts. Pick another reform to move them.</p>'
            f'<ul class="rlist" data-ak-roving data-ak-nav="sequence">{"".join(rf_items)}</ul></section></div>'
            f'<div class="r10-draw"><div class="wide-only" data-ak-roving data-ak-nav="sequence" data-ak-wrap>{cycle_large("R10")}</div>'
            f'<div class="narrow-only" data-ak-roving data-ak-nav="sequence" data-ak-wrap>{cycle_small("R10", 350, step_numbers=True, interactive=True, view="loop-r10")}</div>'
            '<p class="ak-readout" data-ak-readout>Point at or tab to a step or a condition to read it here.</p></div></div>'
            '<section class="sec" aria-labelledby="r10-steps-h"><p class="eyebrow">Step by step</p>'
            f'<h2 class="headline" id="r10-steps-h">{e(r10_steps_head())}</h2>'
            f'<div class="tbl"><table class="st"><thead><tr><th scope="col">Step</th><th scope="col">What happens</th>'
            '<th scope="col">From and to</th><th scope="col">Sign</th><th scope="col">Evidence</th><th scope="col">Delay</th></tr></thead>'
            f'<tbody>{"".join(table)}</tbody></table></div></section>'
            '<section class="sec two eq" aria-label="Evidence and limits"><div>'
            f'<p class="eyebrow">How sure is this?</p><p class="body">{e(l["evidence_summary"])}</p>'
            f'<p class="eyebrow">Keep in mind</p><p class="body">{e(l["qualification"])}</p></div><div>'
            f'<p class="eyebrow">A real case</p><p class="body">{e(l["case"])}</p>'
            f'<dl class="facts"><dt>Now</dt><dd>{e(direction_word("R10"))}: {e(l["reference_mode"])}</dd>'
            f'<dt>One turn</dt><dd>{e(l["delay_word"])}</dd><dt>Closure</dt><dd>{e(l["closure"].capitalize())}</dd></dl>'
            '</div></section></section>')


# ------------------------------------------------------------------------------------------------ reform R-01
def evidence_head(pg, rg):
    a, b = RANK[gk(pg)], RANK[gk(rg)]
    if a < b:
        return 'The problem is better established than the remedy.'
    if a > b:
        return 'The remedy is better established than the problem.'
    return 'The problem and the remedy rest on evidence of the same grade.'


def view_r01():
    r = RF['R-01']
    rid = 'R-01'
    routes = []
    for rt in r['routes']:
        chk = iso_words(rt['checked'])
        routes.append(f'<tr><th scope="row">{e(ED["route_names"][rt["route"]])}</th><td data-label="Who acts">{e(rt["who"])}</td>'
                      f'<td data-label="Feasibility"><strong>{e(rt["feasibility"].capitalize())}</strong><p class="muted">{e(ED["feasibility_scale"][rt["feasibility"]])}</p></td>'
                      + (f'<td data-label="Note">{e(rt["note"])}</td>' if rt["note"] else '<td></td>')
                      + f'<td class="nowrap" data-label="Checked">{e("Checked " + chk if chk else "No check date in V7")}</td></tr>')
    fam = ''.join(f'<li><p class="fam">{e(ED["families"][k])}</p><p class="fv">{e(v.replace("-", MINUS))}</p>'
                  f'<p class="fw">{e(effect_words(v).split("(", 1)[1].rstrip(")") if "(" in effect_words(v) else effect_words(v))}</p></li>'
                  for k, v in r['effects'].items())
    tl = []
    for t in r['targets']:
        tl.append(f'{t}, {label(t)}' if t in N else f'{t}, {L[t]["name"]}')
    loops = ', '.join(loop_link(k) for k in r['loops'])
    succ = ''.join(f'<li>{e(s)}</li>' for s in r['success_measures'])
    st = r['status']
    chk = iso_words(st['checked'])
    disc = INTEREST[rid]
    pe, re_ = r['problem_evidence'], r['remedy_evidence']
    return ('<section class="view" data-view-root="reform-r01" data-crumb="Reform R-01" data-parent="overview" '
            'data-ak-reform="reform-r-01" hidden>'
            '<div class="headblock"><div class="hl">'
            f'<p class="eyebrow">Reform R-01 · {e(r["band"].capitalize())} · {e(r["short"])}</p>'
            f'<h1 class="headline xl" data-ak-heading><span data-reform="R-01" data-targets="{" ".join(r["targets"])}" '
            f'data-name="{e(r["title"])}">{e(r["title"])}</span></h1>'
            f'<p class="deck">{e(r["summary"])}</p></div>'
            f'<aside class="key"><p class="eyebrow">Status</p><p>{e(st["text"])}</p>'
            f'<p class="muted">Checked {e(chk)}; {e(st["result"])}.</p>'
            f'<p class="disc"><strong>Disclosure.</strong> {e(disc)}</p></aside></div>'
            '<section class="sec two eq" aria-label="The problem and the change"><div>'
            f'<p class="eyebrow">The problem it answers</p><p class="gline">{grade_label(pe["grade"])}</p><p class="body">{e(pe["text"])}</p></div>'
            f'<div><p class="eyebrow">What it changes</p><p class="body">{e(r["what_it_changes"])}</p></div></section>'
            '<section class="sec r10 where" aria-labelledby="r01-where-h"><div class="r10-side"><p class="eyebrow">Where it acts</p>'
            f'<h2 class="headline" id="r01-where-h">It acts on {nw(len(r["targets"]))} marks in the safe-seat loop.</h2>'
            f'<p class="body">The red marks are its {nw(len(r["targets"]))} targets:</p><ul class="tgts">'
            + ''.join(f'<li>{chip("Variable" if t in N else "Connection", t, True)} <span>{e(label(t) if t in N else L[t]["name"])}</span></li>'
                      for t in r['targets'])
            + f'</ul><p class="body">It also sits on {loops}.</p>'
            f'<p class="body muted">{e(acc.SIGN_RULE)}</p></div><div class="r10-draw">'
            f'<div class="wide-only" data-ak-roving data-ak-nav="sequence" data-ak-wrap>{cycle_large("R10", view="reform-r01")}</div>'
            f'<div class="narrow-only" data-ak-roving data-ak-nav="sequence" data-ak-wrap>{cycle_small("R10", 350, step_numbers=True, interactive=True, view="reform-r01")}</div>'
            '<p class="ak-readout" data-ak-readout>Point at or tab to a mark to read it here.</p></div></section>'
            '<section class="sec" aria-labelledby="r01-fx-h"><p class="eyebrow">Likely effects</p>'
            f'<h2 class="headline" id="r01-fx-h">Four families, each rated on its own and never added up.</h2>'
            f'<ul class="fams">{fam}</ul><p class="muted">Confidence: {e(r["effects_confidence"])}.</p></section>'
            '<section class="sec" aria-labelledby="r01-rt-h"><p class="eyebrow">Who could adopt it</p>'
            f'<h2 class="headline" id="r01-rt-h">{nw(len(r["routes"]), True)} routes, from a state ballot to Congress.</h2>'
            f'<p class="lede">{e(r["who_decides"])}</p>'
            f'<div class="tbl"><table class="st"><thead><tr><th scope="col">Route</th><th scope="col">Who acts</th>'
            f'<th scope="col">Feasibility, 2026 to 2030</th><th scope="col">Note</th><th scope="col">Checked</th></tr></thead>'
            f'<tbody>{"".join(routes)}</tbody></table></div></section>'
            '<section class="sec" aria-labelledby="r01-ev-h"><p class="eyebrow">Evidence</p>'
            f'<h2 class="headline" id="r01-ev-h">{e(evidence_head(pe["grade"], re_["grade"]))}</h2>'
            f'<div class="two eq"><div><h3 class="sub">Evidence of the problem</h3><p class="gline">{grade_label(pe["grade"])}</p>'
            f'<p class="body">{e(pe["text"])}</p></div><div><h3 class="sub">Evidence for the remedy</h3>'
            f'<p class="gline">{grade_label(re_["grade"])}</p><p class="body">{e(re_["text"])}</p></div></div></section>'
            '<section class="sec" aria-label="Costs and risks"><div class="three">'
            f'<div><p class="eyebrow">Tradeoffs</p><p class="body">{e(r["tradeoffs"])}</p></div>'
            f'<div><p class="eyebrow">How it could fail</p><p class="body">{e(r["failure_risks"])}</p></div>'
            f'<div><p class="eyebrow">What it costs</p><p class="body">{e(r["costs"])}</p></div></div></section>'
            '<section class="sec" aria-label="More from the profile"><div class="three">'
            f'<div><p class="eyebrow">The law</p><p class="body">{e(r["legal_authority"])}</p></div>'
            f'<div><p class="eyebrow">Carrying it out</p><p class="body">{e(r["implementation"])}</p></div>'
            f'<div><p class="eyebrow">How to judge results</p><ul class="body">{succ}</ul>'
            f'<p class="eyebrow">Other options</p><p class="body">{e(r["alternatives"])}</p></div></div></section>'
            '<section class="sec status" aria-labelledby="r01-st-h"><p class="eyebrow">Status</p>'
            f'<h2 class="headline" id="r01-st-h">Where it stands, as of {e(chk)}</h2>'
            f'<p class="body">{e(st["text"])}</p><p class="muted">Checked {e(chk)}; {e(st["result"])}. '
            f'Sources in V7: {e(", ".join(st["sources"]))}.</p>'
            f'<p class="disc big"><strong>Disclosure.</strong> {e(disc)}</p></section></section>')


# ------------------------------------------------------------------------------------------------ loop catalog
LOOPS_HEAD = (f'{N_R} of the {COUNTS["loops"]} loops feed themselves, and {N_WITH_REFORM} have a reform aimed at them.')


def view_loops():
    groups = []
    glossary = {g['term']: g['definition'] for g in ED['glossary']}
    for pid in ['A', 'B', 'C', 'D', 'SK']:
        ks = sorted(HOME[pid], key=lambda k: (len(LO[k]['steps']), ED['loop_order'].index(k)))
        nr = sum(1 for k in ks if LO[k]['type'] == 'R')
        nb = len(ks) - nr
        kinds = (f'all {nw(nr)} reinforcing' if nr and not nb else f'all {nw(nb)} balancing' if nb and not nr
                 else f'{nw(nr)} reinforcing and {nw(nb)} balancing')
        if pid == 'SK':
            head = (f'<h2 class="gh3">Sketches <span class="muted">{len(ks)}</span></h2>'
                    f'<p class="gq">Loops without a complete numbered chain: {e(kinds)}. Their steps carry no grade.</p>')
        else:
            p = PARTS[pid]
            head = (f'<h2 class="gh3"><span data-part="{pid}" data-name="{e(p["plain_name"])}">{e(p["plain_name"])}</span> '
                    f'<span class="muted">{len(ks)}</span></h2><p class="gq"><strong>{e(p["plain_question"])}</strong> '
                    f'{nw(len(ks), True)} loops start in {e(p["plain_name"])}: {e(kinds)}.</p>')
        cards = ''.join(f'<li>{loop_card(k, 350, "loops")}</li>' for k in ks)
        groups.append(f'<section class="lgroup" aria-label="{e("Sketches" if pid == "SK" else PARTS[pid]["plain_name"])}">'
                      f'<div class="lgh">{head}</div><ul class="lgrid" data-ak-roving data-ak-nav="spatial">{cards}</ul></section>')
    numbered = [k for k in LO if not LO[k]['conceptual']]
    for k in numbered:
        minus = sum(1 for s in LO[k]['steps'] if s['polarity'] == '-')
        assert (minus % 2 == 0) == (LO[k]['type'] == 'R'), k
    reinf = glossary['Reinforcing loop (R)']
    return ('<section class="view" data-view-root="loops" data-crumb="All 23 loops" data-parent="overview" hidden>'
            '<div class="headblock"><div class="hl"><p class="eyebrow">The loop catalog</p>'
            f'<h1 class="headline xl" data-ak-heading>{cnt("loops_reinforcing", N_R)} of the {cnt("loops", COUNTS["loops"])} '
            f'loops feed themselves, and {cnt("custom:loops-with-reform", N_WITH_REFORM)} have a reform aimed at them.</h1>'
            f'<p class="deck">A loop is a chain of causes that comes back to where it started. '
            f'{cnt("loops_reinforcing", N_R)} feed themselves and {cnt("loops_balancing", N_B)} push back. '
            f'<span class="q">“{e(sentences(reinf)[-1])}”</span> Each drawing reads clockwise from the top left.</p></div>'
            '<aside class="key"><p class="eyebrow">In each drawing</p><ul class="kl">'
            '<li>A pill is a condition that can rise or fall.</li>'
            '<li>The tag on each arrow carries its sign, with the word beside it: raises or lowers.</li>'
            '<li>A solid line is documented or well supported; dashes are plausible; dash and dot contested; dots a hypothesis.</li>'
            '<li>Ticks after the tail count the wait: one under 2 years, two for 2 to 10, three over 10.</li></ul>'
            f'<p><a href="#how-to-read">How to read the atlas</a></p></aside></div>'
            f'<div data-strip="loops">{"".join(groups)}</div></section>')


# ------------------------------------------------------------------------------------------------ how to read
def lesson_arrow(lid, W=350):
    ll = L[lid]
    h = 60
    a, b = ll['from'], ll['to']
    pw = 128
    sa, ha = station_block(a, label(a), pw / 2 + 2, h / 2 + 18, pw, 'map')
    sb, hb = station_block(b, label(b), W - pw / 2 - 2, h / 2 + 18, pw, 'map')
    pts = [(pw + 6, h / 2 + 18), (W - pw - 6, h / 2 + 18)]
    marks, _, _ = wire_marks(pts, ll['evidence'], ll['polarity'], ll['delay'], 2, lit=False)
    (tx, ty), _ = tag_point(pts, 2, ll['polarity'])
    vb = svg_text(tx, ty - 15, verb(ll['polarity']), 'vb', 'middle')
    H = max(ha, hb) + 30
    attrs = (f'data-link="{lid}" data-sign="{sign_attr(ll["polarity"])}" data-grade="{ll["evidence"]}" '
             f'data-delay="{ll["delay"]}"')
    return (f'<svg class="les" data-view="how-to-read" viewBox="0 0 {W} {f(H)}" width="{W}" role="img" '
            f'aria-label="{e(link_sentence(lid))}"><g class="wire" {attrs}>{marks}</g>{sa}{sb}{vb}</svg>')


def sample_line(grade=None, delay=None, W=200, cls='', sketch=False):
    pts = [(4, 14), (W - 4, 14)]
    marks, _, _ = wire_marks(pts, grade or 'documented', None, delay, 2, lit=False, sketch=sketch)
    return (f'<svg class="smp{cls}" data-view="how-to-read" viewBox="0 0 {W} 28" width="{W}" height="28" aria-hidden="true">'
            f'<g class="wire">{marks}</g></svg>')


def authority_sample(W=350):
    lid = next(k for k, l in L.items() if l['type'] == 'authority')
    ll = L[lid]
    pw = 128
    sa, ha = station_block(ll['from'], label(ll['from']), pw / 2 + 2, 40, pw, 'map')
    sb, hb = station_block(ll['to'], label(ll['to']), W - pw / 2 - 2, 40, pw, 'map')
    pts = [(pw + 6, 40), (W - pw - 6, 40)]
    marks, _, _ = wire_marks(pts, ll['evidence'], None, ll['delay'], 2, lit=False, authority=True)
    vb = svg_text((pts[0][0] + pts[1][0]) / 2, 30, 'decides', 'vb', 'middle')
    attrs = f'data-link="{lid}" data-sign="none" data-grade="{ll["evidence"]}" data-delay="{ll["delay"]}"'
    H = max(ha, hb) / 2 + 46
    return (f'<svg class="les" data-view="how-to-read" viewBox="0 0 {W} {f(H)}" width="{W}" role="img" '
            f'aria-label="{e(link_sentence(lid))}"><g class="wire" {attrs}>{marks}</g>{sa}{sb}{vb}</svg>'
            f'<p class="cap">{e(link_sentence(lid))}</p>')


def view_read():
    g_count = Counter(l['evidence'] for l in L.values())
    d_count = Counter(l['delay'] for l in L.values())
    glossary = {g['term']: g['definition'] for g in ED['glossary']}
    grades = ''.join(
        f'<li>{sample_line(g)}<p><strong>{e(grade_word(g))}</strong>: {e(grade_glyph and grade_gloss(g))}. '
        f'<span class="muted">{cnt("custom:grade-" + g, g_count[g])} connections.</span></p></li>'
        for g in ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis'])
    delays = ''.join(
        f'<li>{sample_line("documented", d)}<p><strong>{e(delay_words(d).capitalize())}</strong>. '
        f'<span class="muted">{cnt("custom:delay-" + d, d_count[d])} connections.</span></p></li>' for d in ['S', 'M', 'L'])
    mix = [m for m in ED['mixups'] if any(pl in ('system', 'loop:B4', 'outcomes') for pl in m['places'])]
    mixes = ''.join(f'<li><p class="mq">{e(m["prompt"])}</p><p>{e(m["answer"])}</p></li>' for m in mix)
    n_auth = sum(1 for l in L.values() if l['type'] == 'authority')
    return ('<section class="view" data-view-root="how-to-read" data-crumb="How to read" data-parent="overview" hidden>'
            '<div class="headblock"><div class="hl"><p class="eyebrow">How to read the atlas</p>'
            '<h1 class="headline xl" data-ak-heading>Every line says what happens next, and how sure we are.</h1>'
            f'<p class="deck">The atlas uses one small language on every page. Five ideas cover it. '
            f'<span class="q">“{e(glossary["Variable"])}”</span></p></div></div>'
            '<ol class="lessons">'
            '<li class="lesson"><div class="lt2"><p class="ln2">1</p><h2 class="headline">The tip is the effect.</h2>'
            f'<p class="body">An arrow runs from a cause to what it changes. The tag on the line carries the sign, and the word '
            f'beside it says what the sign means: raises or lowers.</p><p class="body strong">{e(acc.SIGN_RULE)}</p></div>'
            f'<div class="lv">{lesson_arrow("L08")}{lesson_arrow("L25")}'
            f'<p class="cap">{e(link_sentence("L08"))}</p><p class="cap">{e(link_sentence("L25"))}</p>'
            f'<p class="cap">{cnt("authority_connections", n_auth)} lines of authority carry no sign. They end in an open '
            f'diamond and name who decides.</p>{authority_sample()}</div></li>'
            '<li class="lesson"><div class="lt2"><p class="ln2">2</p><h2 class="headline">Texture is the evidence.</h2>'
            f'<p class="body">The more broken the line, the weaker the evidence behind it. Every connection carries one of five '
            f'grades from Atlas V7.</p></div><div class="lv"><ul class="samples">{grades}</ul></div></li>'
            '<li class="lesson"><div class="lt2"><p class="ln2">3</p><h2 class="headline">Ticks count the wait.</h2>'
            f'<p class="body">{e(glossary["Delay"].split(". ")[0])}. Small ticks just after the tail of an arrow show how long: '
            f'one, two or three.</p></div><div class="lv"><ul class="samples">{delays}</ul></div></li>'
            '<li class="lesson"><div class="lt2"><p class="ln2">4</p><h2 class="headline">Loops have a character.</h2>'
            f'<p class="body">{e(glossary["Feedback loop"])} Count the minus signs around a loop: an even number means it feeds '
            f'itself, an odd number means it pushes back.</p>'
            f'<p class="body">{cnt("loops_reinforcing", N_R)} loops feed themselves and {cnt("loops_balancing", N_B)} push back. '
            f'<span class="q">“{e(sentences(glossary["Reinforcing loop (R)"])[-1])}”</span></p></div>'
            f'<div class="lv two eq"><div>{cycle_small("R10", 350, view="how-to-read")}<p class="cap">{e(read_aloud("R10"))}</p></div>'
            f'<div>{cycle_small("B4", 350, view="how-to-read")}<p class="cap">{e(read_aloud("B4"))}</p></div></div></li>'
            '<li class="lesson"><div class="lt2"><p class="ln2">5</p><h2 class="headline">Color is the layer you are reading.</h2>'
            '<p class="body">A headline names one route, and the page draws that route in black against the gray of the rest '
            'of the system. Red appears only on the loop and reform pages, on the marks where a reform acts; it never means '
            'good or bad.</p></div>'
            f'<div class="lv"><ul class="samples"><li>{sample_line("documented", None, 200, " main")}<p><strong>The route the headline names</strong></p></li>'
            f'<li>{sample_line("documented", None, 200, " ctx")}<p><strong>The rest of the system</strong></p></li></ul>'
            '<p class="cap"><a href="#loop-r10">See where a reform acts on the safe-seat loop</a></p></div></li></ol>'
            '<section class="sec" aria-labelledby="mix-h"><p class="eyebrow">Easy to mix up</p>'
            f'<h2 class="headline" id="mix-h">{nw(len(mix), True)} readings the atlas warns against.</h2><ul class="mix">{mixes}</ul></section></section>')


# ------------------------------------------------------------------------------------------------ frame
def wordmark(height, master, cls):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    src = src.replace('<svg ', f'<svg class="{cls}" data-view="wordmark" width="{w:.0f}" height="{height}" role="img" '
                               f'aria-label="Oath &amp; Action" ', 1)
    return src


VIEWS = [('overview', 'Overview'), ('area-c', 'Elections'), ('loop-r10', 'Loop R10'), ('reform-r01', 'Reform R-01'),
         ('loops', 'All loops'), ('how-to-read', 'How to read')]


def masthead():
    tabs = ''.join(f'<li><a href="#{v}">{e(t)}</a></li>' for v, t in VIEWS)
    return ('<header class="mast"><div class="wrap mrow">'
            f'<a class="wm" href="#overview" data-red="signature" aria-label="Oath &amp; Action, atlas overview">'
            f'{wordmark(24, "20261028_Wordmark-24px-Master.svg", "wm24")}{wordmark(16, "20261028_Wordmark-16px-Master.svg", "wm16")}</a>'
            '<p class="run">Editorial system 01 · Times Explainer</p>'
            f'<nav class="tabs" aria-label="Views"><ul>{tabs}</ul></nav></div></header>')


def footer():
    c = COUNTS
    return ('<footer class="foot"><div class="wrap frow">'
            f'<p class="src">{e(ED["meta"]["title"])} Systems Atlas V7, snapshot {SNAP_WORDS}. '
            f'{cnt("variables", c["variables"])} variables, {cnt("connections", c["connections"])} connections, '
            f'{cnt("loops", c["loops"])} loops, {cnt("reforms", c["reforms"])} reforms.</p>'
            '<p class="src right">Editorial system 01, Times Explainer. Studio draft; headlines are drafts by the studio.</p>'
            '</div></footer>')


def panel():
    return ('<aside class="ak-panel" data-ak-panel hidden aria-labelledby="pnl-title">'
            '<div class="ak-panel-bar"><p data-ak-panel-kind></p>'
            '<button type="button" class="ak-btn" data-ak-sheet-toggle aria-expanded="false">More</button>'
            '<button type="button" class="ak-btn" data-ak-close>Close</button></div>'
            '<h2 id="pnl-title" data-ak-panel-title tabindex="-1"></h2><div data-ak-panel-body></div></aside>')


def templates():
    out = [tpl_var(c) for c in N]
    out += [tpl_part(p) for p in ORDER]
    out += [tpl_pathway(pw) for pw in ED['pathways']]
    out += [tpl_loop(k) for k in ED['loop_order']]
    out += [tpl_link(k) for k in sorted(set(C_INSIDE + ['L23', 'L54'] + [s['id'] for s in LO['R10']['steps']]))]
    out += [tpl_reform(r) for r in LO['R10']['reforms']]
    return ''.join(out)


CSS = r"""
:root{--white:#FFFFFF;--ink:#121212;--stone:#5D636D;--deep:#4E535B;--news:#DCD9D2;--red:#E63946;--verd:#4A7C74;
--ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px;--ak-panel-w:420px;--gut:24px}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#FFFFFF;color:var(--ink);font:400 17px/27px Inter,system-ui,sans-serif;font-feature-settings:"tnum" 0}
*,*::before,*::after{box-sizing:border-box}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
button{font:inherit;color:inherit}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.muted{color:var(--deep)}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;text-wrap:balance;margin-left:-.04em}
.headline{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;text-wrap:balance}
.deck{margin:16px 0 0;font:400 19px/28px Inter,sans-serif;max-width:40em}
.lede{margin:12px 0 0;font:400 17px/27px Inter,sans-serif;max-width:46em}
.body{font:400 17px/27px Inter,sans-serif;margin:0 0 16px}
.q{font:italic 400 19px/28px Lora,serif}
.chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 Inter,sans-serif;vertical-align:middle}
.chip .k{display:inline-flex;align-items:center;padding:0 7px;background:var(--ink);color:#FFFFFF;letter-spacing:.06em;text-transform:uppercase}
.chip .c{display:inline-flex;align-items:center;padding:0 8px;border:1.5px solid var(--ink);border-left:0;font:700 14px/1 Inter,sans-serif;font-variant-numeric:tabular-nums}
.chip.compact{height:22px}.chip.compact .c{font-size:13px}
.src{font:400 13px/18px Inter,sans-serif;color:var(--deep);margin:0}
/* masthead */
.mast{border-bottom:1px solid var(--stone);background:#FFFFFF}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;color:var(--ink);padding:0}
.wm16{display:none}
.run{margin:0 0 0 48px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--deep)}
.tabs ul{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;min-height:44px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:var(--ink)}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ink)}
.tabs a:hover{text-decoration:underline}
.ak-crumbs{margin:16px 0 0}
.ak-crumbs a{color:var(--deep)}
.view{padding-bottom:72px}
/* head block */
.headblock{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:var(--gut);margin-top:24px;align-items:start}
.key{border-top:1px solid var(--ink);padding-top:12px;font:400 15px/23px Inter,sans-serif}
.key p{margin:0 0 10px}.key .eyebrow{margin-bottom:8px}
.key ul.kl{margin:0 0 10px;padding-left:18px}.key ul.kl li{margin-bottom:6px}
.ral{font:600 17px/27px Inter,sans-serif}
.nums{display:grid;grid-template-columns:max-content 1fr;gap:2px 12px;margin:0;align-items:baseline}
.nums dt{font:800 22px/26px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums;text-align:right}.nums dd{margin:0}
/* chain */
.chain{margin:40px 0 0}
.chain ol{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));margin:0;padding:0;list-style:none;border-top:2px solid var(--ink)}
.chain li+li{border-left:1px solid var(--news)}
.cj{display:grid;gap:2px;width:100%;min-height:88px;padding:10px 12px 12px;background:none;border:0;text-align:left;cursor:pointer;align-content:start}
.cj:hover .nm{text-decoration:underline;text-underline-offset:3px}
.cj .n{font:800 15px/18px "Inter Tight",sans-serif;color:var(--deep)}
.cj .nm{font:600 15px/18px Inter,sans-serif}
.cj .q{font:400 13px/16px Inter,sans-serif;color:var(--deep)}
/* sections */
.sec-head{margin:88px 0 0;padding-top:16px;border-top:2px solid var(--ink)}
.circuit>.sec-head{margin-top:64px}
.sec{margin-top:72px;padding-top:16px;border-top:1px solid var(--ink)}
.two{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px}
.two.eq{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px}
/* the circuit */
.cgrid{position:relative;padding-left:28px;margin-top:40px}
.spine{position:absolute;left:0;top:0;width:96px;overflow:visible;pointer-events:none}
.spine .m{stroke:var(--ink);fill:none}.spine .s{stroke:var(--stone);fill:none}
.spine .mh{fill:var(--ink)}.spine .sh{fill:var(--stone)}
.pblock{display:grid;grid-template-columns:52px 300px minmax(0,1fr) 340px;column-gap:28px;padding:4px 0 24px;scroll-margin-top:24px}
.pflow{display:grid;grid-template-columns:52px minmax(0,1fr);column-gap:28px;padding:0 0 36px}
.fbody{display:grid;grid-template-columns:72px minmax(0,1fr);column-gap:20px;align-items:start;max-width:900px}
.mk{position:relative;z-index:1}
.dot{display:flex;width:40px;height:40px;margin:0 auto;border-radius:50%;border:2px solid var(--ink);background:#FFFFFF;
align-items:center;justify-content:center;font:800 17px/1 "Inter Tight",sans-serif}
.dot.open{border-color:var(--stone)}
.pname .eyebrow{color:var(--deep);margin-bottom:6px}
.pn{margin:0;font:800 40px/44px "Inter Tight",sans-serif;letter-spacing:-.03em}
.pqq{margin:6px 0 0;font:400 19px/28px Inter,sans-serif}
.pstory p{margin:0 0 12px}
.pstory .meta{font:400 14px/20px Inter,sans-serif;color:var(--deep)}
.lh{font:400 15px/23px Inter,sans-serif}.lh .lbl,.lbl{font-weight:600}
.ll{white-space:normal}.ll .id{color:var(--deep);font-size:13px}
.go a{font:600 17px/27px Inter,sans-serif}
.tl{display:inline-flex;align-items:center;min-height:32px;padding:0;background:none;border:0;font:600 15px/23px Inter,sans-serif;
text-decoration:underline;text-underline-offset:3px;cursor:pointer;color:var(--ink)}
.tl:hover{text-decoration-thickness:2px}
.vh{margin:0 0 6px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--deep)}
.vlist{display:grid;grid-template-columns:minmax(0,1fr);gap:0;margin:0;padding:0;list-style:none}
.groups{margin:0;padding:0;list-style:none;display:grid;gap:10px}
.groups .vlist{grid-template-columns:minmax(0,1fr)}
.gt{margin:0 0 2px;font:600 13px/18px Inter,sans-serif;color:var(--deep)}
.vbtn{display:flex;gap:9px;align-items:baseline;width:100%;min-height:30px;padding:3px 0;background:none;border:0;
text-align:left;font:400 15px/23px Inter,sans-serif;cursor:pointer;border-bottom:1px solid var(--news)}
.vbtn:hover{text-decoration:underline;text-underline-offset:3px}
.vdot{flex:none;width:9px;height:9px;border:2px solid var(--ink);border-radius:50%;transform:translateY(-1px)}
.vbtn[data-ak-sel]{font-weight:700}.vbtn[data-ak-sel] .vdot{background:var(--ink)}
.vbtn.big{font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em;border:0;padding:0;min-height:32px}
.vbtn.big .vdot{display:none}
.fig{margin:0;font:800 40px/40px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums;letter-spacing:-.03em}
.pflow.side .fig,.pflow.up .fig{color:var(--deep)}
.fig2{font:800 22px/26px "Inter Tight",sans-serif;margin-right:6px}
.fl{margin:0 0 6px;font:400 17px/27px Inter,sans-serif}
.fl.back{margin-top:14px}
.ex{margin:0 0 6px;padding:0;list-style:none;font:400 15px/23px Inter,sans-serif}
.ex li{padding-left:16px;position:relative}.ex li::before{content:"";position:absolute;left:0;top:9px;width:6px;height:6px;background:currentColor}
.lnm{font-weight:600}
.also{margin:6px 0 0;font:400 14px/20px Inter,sans-serif;color:var(--deep)}
.sk-note{margin:8px 0 0 108px;font:400 15px/23px Inter,sans-serif;max-width:60em}
/* whole system */
.sumwrap{margin-top:32px}
.sumd text,.big text,.cyc text,.crow text,.les text{font-family:Inter,sans-serif}
svg .ph{font:800 22px "Inter Tight",sans-serif;letter-spacing:-.02em;fill:var(--ink)}
svg .pq{font:400 15px Inter,sans-serif;fill:var(--ink)}
svg .vn{font:400 14px Inter,sans-serif;fill:var(--ink)}
svg .vn .sep{fill:var(--stone)}
svg .cp2{font:400 14px Inter,sans-serif;fill:var(--deep)}
svg .gh2{font:600 13px Inter,sans-serif;fill:var(--deep)}
svg .cn{font:800 22px "Inter Tight",sans-serif;fill:var(--ink)}
svg .cn2{font:800 22px "Inter Tight",sans-serif;fill:var(--deep)}
svg .cn3{font:600 15px Inter,sans-serif;fill:var(--deep)}
svg .rt,svg .rn,svg .nr{font:400 15px Inter,sans-serif;fill:var(--ink)}
svg .nr.sn{fill:var(--deep)}
svg .eb{font:700 13px Inter,sans-serif;letter-spacing:.06em;fill:var(--ink)}
svg .eb.gh{fill:var(--deep)}
svg .lb{font:600 15px Inter,sans-serif;fill:var(--ink)}
svg .lb.far{font-weight:400}
svg .nb{font:600 13px Inter,sans-serif;fill:var(--ink)}
svg .nt{font:400 13px Inter,sans-serif;fill:var(--deep)}
svg .vb{font:500 13px Inter,sans-serif;fill:var(--ink)}
svg .cid,svg .cid2{font:800 22px "Inter Tight",sans-serif;fill:var(--ink)}
svg .ckind{font:400 13px Inter,sans-serif;fill:var(--deep)}
svg .mk{}.sumd .mk{}
svg text.mk{font:700 13px Inter,sans-serif;fill:var(--ink)}
svg .st-map{font:600 15px Inter,sans-serif;fill:var(--ink)}
svg .st-station{font:700 20px "Inter Tight",sans-serif;letter-spacing:-.01em;fill:var(--ink)}
svg .st-map.sk{fill:var(--deep);font-weight:400}
svg .st-station.gh{fill:var(--deep)}
.bx{fill:#FFFFFF;stroke:var(--ak-hi,var(--ink));stroke-width:1px}
.bx2{fill:#FFFFFF;stroke:var(--ak-hi,var(--stone));stroke-width:1px}
.pt{cursor:pointer}
.pt:hover .bx,.pt:hover .bx2,.pt:focus-visible .bx,.pt:focus-visible .bx2{stroke-width:3px}
.pt[data-ak-sel] .ak-mark{stroke-width:3px!important}
.pt:hover .ph{text-decoration:underline}
.hr{stroke:var(--news);stroke-width:1px}
.bm{color:var(--ink)}.bs{color:var(--stone)}
.bl{stroke:currentColor}.bh{fill:currentColor}
.leader{stroke:var(--stone);stroke-width:1px;fill:none}
/* connections and stations */
.wire{color:var(--ink)}
.wire .ak-mark{stroke:var(--ak-hi,currentColor)}
.wire .hd,.wire .tg polygon{fill:var(--ak-hi,currentColor)}
.wire .tg .sg{fill:#FFFFFF}
.wire .tk{stroke:var(--ak-hi,currentColor);stroke-width:2px}
.wire .dm{fill:#FFFFFF;stroke:var(--ak-hi,currentColor);stroke-width:2px}
.wire .hi{display:none}
.wire[data-ak-sel] .lo,.wire.ak-target .lo,.wire.ak-now .lo{display:none}
.wire[data-ak-sel] .hi,.wire.ak-target .hi,.wire.ak-now .hi{display:inline}
.wire[data-ak-sel] .ak-mark,.wire.ak-target .ak-mark,.wire.ak-now .ak-mark{stroke-dasharray:var(--d6,none)}
.wire.ak-rel:not([data-ak-sel]):not(.ak-target) .ak-mark,.wire:hover:not([data-ak-sel]):not(.ak-target) .ak-mark{stroke-dasharray:var(--d3,none)}
.rail-o{stroke:currentColor}.rail-i{stroke:#FFFFFF}
.pl{fill:#FFFFFF;stroke:var(--ak-hi,currentColor)}
.pl.gh{stroke:var(--ak-hi,var(--stone))}
.node{color:var(--ink)}
.node[data-ak-sel] .pl,.node.ak-target .pl,.node:hover .pl,.node.ak-rel .pl{stroke-width:3px!important}
.ak-dim [data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target){color:var(--stone)}
.ak-dim .wire[data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target) .ak-mark{stroke-dasharray:var(--d2,none)}
.ak-stepping .wire[data-select]:not(.ak-now):not(.ak-done):not(.ak-target){color:var(--stone)}
.ak-stepping .node[data-select]:not(.ak-now):not(.ak-done):not(.ak-target):not([data-node="C1"]){color:var(--stone)}
[data-select="var-c1"].node{}
/* loops */
.lgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:48px var(--gut);margin:32px 0 0;padding:0;list-style:none}
.lcard{display:flex;flex-direction:column;border-top:1px solid var(--ink);padding-top:10px;height:100%}
.lk{display:flex;gap:10px;align-items:center;margin:0 0 8px;font:400 14px/20px Inter,sans-serif;color:var(--deep)}
.ln{margin:0;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.lt{margin:4px 0 0;font:400 15px/23px Inter,sans-serif;color:var(--deep)}
.cwrap{margin:14px 0 10px}
.cyc{display:block;max-width:100%;height:auto}
.ra{margin:0 0 8px;font:600 15px/23px Inter,sans-serif}
.ls{margin:0 0 6px;font:400 14px/20px Inter,sans-serif;color:var(--deep)}
.ld{margin:0 0 6px;font:400 14px/20px Inter,sans-serif;color:var(--ink);border-left:2px solid var(--ink);padding-left:10px}
.la{margin:auto 0 0;padding-top:4px}
.lgroup{margin-top:64px;padding-top:12px;border-top:2px solid var(--ink)}
.lgh{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:var(--gut);align-items:baseline}
.gh3{margin:0;font:800 40px/44px "Inter Tight",sans-serif;letter-spacing:-.03em}
.gh3 .muted,.cgh .muted,.igh .muted{font-weight:400}
.gq{margin:0;font:400 19px/28px Inter,sans-serif}
/* Elections */
.jumps{margin:32px 0 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--news)}
.jumps ul{display:flex;flex-wrap:wrap;gap:4px 28px;margin:0;padding:0;list-style:none}
.jb{min-height:44px;padding:0;background:none;border:0;font:600 15px/1 Inter,sans-serif;cursor:pointer}
.jb:hover{text-decoration:underline;text-underline-offset:3px}
.whatq .headline{margin-bottom:16px}
.vcards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px var(--gut);margin:0;padding:0;list-style:none}
.vcard{border-top:1px solid var(--ink);padding-top:10px}
.vt{margin:8px 0 2px}
.vf{margin:0;font:400 14px/20px Inter,sans-serif;color:var(--deep)}
.vm{margin:8px 0 6px;font:600 15px/23px Inter,sans-serif}
.vd{margin:0;font:400 15px/23px Inter,sans-serif}
.ak-scroll{margin-top:24px}
.big{display:block;width:100%;height:auto;min-width:var(--ak-min,0px)}
.r10-draw .big{max-width:866px}
.fullbtn{display:none;margin:12px 0 0}
.ak-readout{color:var(--deep);font:400 15px/23px Inter,sans-serif}
.words{margin-top:16px;font:400 15px/23px Inter,sans-serif}
.words summary{cursor:pointer;font-weight:600;min-height:32px;display:flex;align-items:center}
.words ol.cols{columns:3;column-gap:var(--gut)}
.sub{margin:24px 0 8px;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.cg{margin-top:16px}
.cgh{margin:0 0 4px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.crows{margin:0;padding:0;list-style:none}
.crw{padding:12px 0 10px;border-top:1px solid var(--news)}
.crow{display:block;max-width:100%;height:auto}
.cdn{display:none}
.cn{margin:6px 0 0;font:400 14px/20px Inter,sans-serif}
.igrid{margin-top:24px;display:grid;gap:40px}
.igh{margin:0;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.igq{margin:4px 0 10px;font:400 15px/23px Inter,sans-serif;color:var(--deep)}
.ilist{margin:0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.ilist>li{border-bottom:1px solid var(--news)}
.iss summary{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,5fr) 150px;column-gap:var(--gut);padding:12px 0;cursor:pointer;
list-style:none;align-items:baseline}
.iss summary::-webkit-details-marker{display:none}
.iss summary::before{content:"+";position:absolute;margin-left:-22px;font:700 17px/23px Inter,sans-serif}
.iss[open] summary::before{content:"\2212"}
.ilist>li{position:relative;padding-left:22px}
.it{font:600 15px/23px Inter,sans-serif}
.iss summary:hover .it{text-decoration:underline;text-underline-offset:3px}
.ie{font:400 15px/23px Inter,sans-serif}
.ig{display:flex;gap:8px;align-items:center;font:400 14px/20px Inter,sans-serif}
.itag{grid-column:1;font:400 13px/18px Inter,sans-serif;color:var(--deep)}
.ib{padding:0 0 20px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px var(--gut);font:400 15px/23px Inter,sans-serif}
.ib>p:first-child{grid-column:1/-1;font:400 17px/27px Inter,sans-serif}
.ib dl{grid-column:1/-1;display:grid;grid-template-columns:180px 1fr;gap:6px 16px;margin:4px 0 0}
.ib dt{font-weight:600}.ib dd{margin:0}
.exm{border-left:2px solid var(--ink);padding-left:14px}
.exm h5{margin:0 0 4px;font:600 17px/24px Inter,sans-serif}.exm p{margin:0 0 6px}
.rgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px var(--gut);margin:24px 0 0;padding:0;list-style:none}
.rcard{border-top:1px solid var(--ink);padding-top:10px;font:400 15px/23px Inter,sans-serif}
.rcard p{margin:0 0 8px}
.rn{margin:0 0 8px;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.fxl{color:var(--deep);font-size:14px;line-height:20px}
.disc{border-left:2px solid var(--ink);padding-left:12px;font:400 15px/23px Inter,sans-serif}
.disc.big{font:400 17px/27px Inter,sans-serif;max-width:46em}
.gl{display:inline-flex;gap:8px;align-items:center}
.gg{flex:none}
/* R10 */
.r10{display:grid;grid-template-columns:421px 866px;gap:var(--gut);margin-top:40px;align-items:start}
.r10-side .eyebrow{margin-top:0}
.sbtn{display:flex;flex-wrap:wrap;gap:8px}
.sstat{min-height:96px;margin:12px 0;font:400 15px/23px Inter,sans-serif}
.slist{margin:0;padding:0;list-style:none;font:400 15px/23px Inter,sans-serif;counter-reset:s}
.slist li{border-top:1px solid var(--news);padding:8px 0 8px 14px}
.rfs{margin-top:28px;border-top:1px solid var(--ink);padding-top:12px}
.rfs p:not(.eyebrow){font:400 15px/23px Inter,sans-serif}
.rlist{margin:0;padding:0;list-style:none}
.rlist li{border-top:1px solid var(--news);padding:8px 0}
.rb{display:grid;gap:4px;width:100%;padding:4px 0;background:none;border:0;text-align:left;cursor:pointer;justify-items:start}
.rbt{font:600 15px/23px Inter,sans-serif}.rba{font:400 14px/20px Inter,sans-serif;color:var(--deep)}
.rb:hover .rbt{text-decoration:underline;text-underline-offset:3px}
.rb[data-ak-sel] .rbt{font-weight:800}
.narrow-only{display:none}
.pair .eyebrow{margin-top:20px}
.tgts{margin:0 0 16px;padding:0;list-style:none;font:600 15px/23px Inter,sans-serif}
.tgts li{display:flex;gap:10px;align-items:flex-start;padding:6px 0;border-top:1px solid var(--news)}
.tgts .chip{flex:none}
.tbl{overflow-x:auto;margin-top:24px}
table.st{width:100%;border-collapse:collapse;font:400 15px/23px Inter,sans-serif}
table.st th,table.st td{border-top:1px solid var(--news);padding:12px 12px 12px 0;text-align:left;vertical-align:top}
table.st thead th{border-top:1px solid var(--ink);font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
table.st td p{margin:0 0 6px}
.sn2{display:inline-block;width:22px;font:800 17px/22px "Inter Tight",sans-serif}
.nowrap{white-space:nowrap}
.wk{margin:6px 0 0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.facts{display:grid;grid-template-columns:110px 1fr;gap:6px 16px;font:400 15px/23px Inter,sans-serif}
.facts dt{font-weight:600}.facts dd{margin:0}
/* R-01 */
.gline{margin:0 0 8px;font:600 15px/23px Inter,sans-serif}
.fams{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--gut);margin:24px 0 12px;padding:0;list-style:none}
.fams li{border-top:1px solid var(--ink);padding-top:10px}
.fam{margin:0;font:600 15px/23px Inter,sans-serif}
.fv{margin:4px 0;font:800 40px/40px "Inter Tight",sans-serif}
.fw{margin:0;font:400 15px/23px Inter,sans-serif;color:var(--deep)}
.status{max-width:960px}
/* how to read */
.lessons{margin:40px 0 0;padding:0;list-style:none}
.lesson{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;padding:24px 0 48px;border-top:1px solid var(--ink)}
.ln2{margin:0 0 4px;font:800 40px/40px "Inter Tight",sans-serif;color:var(--deep)}
.lesson .headline{margin-bottom:16px}
.strong{font-weight:600}
.les{display:block;max-width:none;height:auto;margin-bottom:8px}
.cap{font:400 14px/20px Inter,sans-serif;color:var(--deep);margin:4px 0 8px}
.samples{margin:0;padding:0;list-style:none}
.samples li{display:grid;grid-template-columns:220px 1fr;gap:16px;align-items:center;border-top:1px solid var(--news);padding:10px 0}
.samples p{margin:0;font:400 15px/23px Inter,sans-serif}
.smp.ctx .wire{color:var(--stone)}
.mix{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--gut);margin:24px 0 0;padding:0;list-style:none;font:400 15px/23px Inter,sans-serif}
.mix li{border-top:1px solid var(--ink);padding-top:10px}
.mq{font:600 17px/27px Inter,sans-serif;margin:0 0 8px}
/* bill */
.hubs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:var(--gut);margin-top:32px}
.hub{border-top:2px solid var(--ink);padding-top:10px}
.hub>.eyebrow{min-height:36px}
.hq{margin:0 0 12px;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em;text-wrap:balance}
.qs{margin:0;padding:0;list-style:none}
.qb{display:block;width:100%;padding:8px 0 8px 18px;min-height:32px;background:none;border:0;border-top:1px solid var(--news);
text-align:left;font:400 15px/23px Inter,sans-serif;cursor:pointer;position:relative}
.qb::before{content:"";position:absolute;left:0;top:18px;width:8px;height:8px;border-top:2px solid var(--ink);border-right:2px solid var(--ink);transform:rotate(45deg)}
.qb:hover{text-decoration:underline;text-underline-offset:3px}
.qb[data-ak-sel]{font-weight:700}
/* panel: a fixed drawer at the right on wide screens, the kit's bottom sheet on narrow ones */
.ak-panel{background:#FFFFFF}
.ak-panel h2{font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.ak-panel .lead{font:600 17px/27px Inter,sans-serif;margin:0 0 10px}
.ak-panel p{margin:0 0 10px}
.ak-panel dl{margin:0 0 10px}
.ak-panel .next{font-weight:600;margin-top:16px}
.ak-panel .src{margin-top:20px}
.ak-panel ol.steps{padding-left:20px}.ak-panel ol.steps li{margin-bottom:6px}
.pk{background:none;border:0;padding:2px 0;font:inherit;text-decoration:underline;text-underline-offset:3px;cursor:pointer;min-height:24px}
@media (min-width:900px){.ak-panel{position:fixed;top:0;right:0;bottom:0;width:var(--ak-panel-w);max-height:none;z-index:80;
border-left:1px solid var(--ink);overflow:auto;animation:ak-panel-in var(--ak-mid) var(--ak-ease-in)}}
/* footer */
.foot{border-top:1px solid var(--stone);margin-top:40px}
.frow{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:var(--gut);padding-top:16px;padding-bottom:40px}
.foot .right{text-align:right}
/* narrower screens */
@media (max-width:1399.98px){
 .r10{grid-template-columns:minmax(0,1fr)}
 .pblock{grid-template-columns:52px minmax(0,260px) minmax(0,1fr);row-gap:12px}
 .pvars{grid-column:3}
}
@media (max-width:899.98px){
 .wrap{padding:0 20px}
 .mrow{grid-template-columns:1fr;gap:8px;padding-top:16px}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
 .tabs a{justify-content:flex-start;font-size:15px}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline,.pn,.gh3{font-size:30px;line-height:34px}
 .deck{font-size:17px;line-height:25px}
 .body,.fl,.lede{font-size:16px;line-height:25px}
 .ln,.sub,.igh,.rn,.hq,.ak-panel h2{font-size:20px;line-height:24px}
 .fig,.fv,.ln2{font-size:32px;line-height:32px}
 .headblock,.two,.two.eq,.three,.lesson,.frow,.lgh{grid-template-columns:minmax(0,1fr)}
 .chain ol{grid-template-columns:repeat(2,minmax(0,1fr))}
 .chain li+li{border-left:0}.chain li{border-bottom:1px solid var(--news)}
 .cj{min-height:44px}
 .sec-head{margin-top:64px}
 .cgrid{padding-left:14px}
 .pblock{grid-template-columns:40px minmax(0,1fr);column-gap:14px}
 .pblock>.pname,.pblock>.pstory,.pblock>.pvars{grid-column:2}
 .pflow{grid-template-columns:40px minmax(0,1fr);column-gap:14px}
 .fbody{grid-template-columns:minmax(0,1fr)}
 .dot{width:34px;height:34px;font-size:15px}
 .pqq{font-size:17px;line-height:25px}
 .vlist,.groups .vlist{grid-template-columns:minmax(0,1fr)}
 .vbtn,.tl,.jb,.qb{min-height:44px;align-items:center}
 .sk-note{margin-left:0}
 .hubs,.lgrid,.rgrid,.vcards,.fams,.mix{grid-template-columns:minmax(0,1fr)}
 .fullbtn{display:block}
 .words ol.cols{columns:1}
 .cdr{display:none}.cdn{display:block}
 .wide-only{display:none}.narrow-only{display:block}
 .iss summary{grid-template-columns:minmax(0,1fr);row-gap:4px}
 .itag{grid-column:auto}
 .ib{grid-template-columns:minmax(0,1fr)}
 .ib dl{grid-template-columns:minmax(0,1fr)}
 .samples li{grid-template-columns:minmax(0,1fr)}
 .foot .right{text-align:left}
 .r10{margin-top:24px}
 .r10-draw{order:-1}
 table.st,table.st tbody,table.st tr,table.st td,table.st th{display:block;width:auto}
 table.st thead{display:none}
 table.st tr{border-top:1px solid var(--ink);padding:8px 0}
 table.st th,table.st td{border:0;padding:4px 0}
 table.st td[data-label]::before{content:attr(data-label);display:block;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--deep)}
 .nowrap{white-space:normal}
}
"""

JS = r"""
(function(){
  'use strict';
  var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  var RM=matchMedia('(prefers-reduced-motion: reduce)');
  function view(){return (decodeURIComponent(location.hash.slice(1)).split('/')[0]||'overview').toLowerCase()}
  function tabs(){var v=view(); if(!$('[data-view-root="'+v+'"]')) v='overview';
    $$('.tabs a').forEach(function(a){ if(a.getAttribute('href')==='#'+v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });}
  // The circuit's spine and return line, drawn from the markers' real positions so text can reflow freely.
  var NS='http://www.w3.org/2000/svg';
  function el(n,a){var x=document.createElementNS(NS,n); for(var k in a) x.setAttribute(k,a[k]); return x;}
  function head(svg,x,y,ux,uy,w,cls){var L=w===3?13:10,B=w===3?11:8,bx=x-ux*L,by=y-uy*L,vx=-uy,vy=ux;
    svg.appendChild(el('path',{'class':cls,d:'M'+(bx+vx*B/2)+' '+(by+vy*B/2)+'L'+x+' '+y+'L'+(bx-vx*B/2)+' '+(by-vy*B/2)+'Z'}));}
  function line(svg,pts,w,main,arrow){var cls=main?'m':'s',d='M'+pts.map(function(p){return p[0]+' '+p[1]}).join('L');
    var n=pts.length,ux=pts[n-1][0]-pts[n-2][0],uy=pts[n-1][1]-pts[n-2][1],len=Math.hypot(ux,uy)||1;ux/=len;uy/=len;
    if(arrow){var L=w===3?13:10;pts=pts.slice();pts[n-1]=[pts[n-1][0]-ux*L,pts[n-1][1]-uy*L];d='M'+pts.map(function(p){return p[0]+' '+p[1]}).join('L');}
    svg.appendChild(el('path',{'class':cls,d:d,'stroke-width':w,'stroke-linejoin':'round'}));
    if(arrow) head(svg,pts[n-1][0]+ux*(w===3?13:10),pts[n-1][1]+uy*(w===3?13:10),ux,uy,w,main?'mh':'sh');}
  function spine(){
    var box=$('[data-circuit]'); if(!box||!box.getClientRects().length) return;
    var svg=$('svg.spine',box), r=box.getBoundingClientRect(), H=box.offsetHeight;
    svg.setAttribute('height',H); svg.setAttribute('viewBox','0 0 96 '+H); while(svg.firstChild) svg.removeChild(svg.firstChild);
    var P={}; $$('.pblock',box).forEach(function(b){var d=$('.dot',b).getBoundingClientRect();
      P[b.dataset.p]={x:d.left-r.left+d.width/2,t:d.top-r.top,b:d.bottom-r.top,y:d.top-r.top+d.height/2,l:d.left-r.left};});
    if(!P.A) return;
    var rail=Math.max(4,P.A.l-26);
    var seg=function(a,b,main){line(svg,[[P[a].x,P[a].b+3],[P[b].x,P[b].t-3]],main?3:2,main,true);};
    seg('X','A',false); seg('A','B',true); seg('B','C',true); seg('C','D',true); seg('D','E',true); seg('E','EC',false);
    line(svg,[[P.TC.x,P.TC.t-3],[P.EC.x,P.EC.b+3]],2,false,true);
    line(svg,[[P.EC.l-3,P.EC.y],[rail,P.EC.y],[rail,P.E.y]],2,false,false);
    line(svg,[[P.E.l-3,P.E.y],[rail,P.E.y],[rail,P.A.y],[P.A.l-3,P.A.y]],3,true,true);
  }
  document.addEventListener('click',function(ev){var b=ev.target.closest&&ev.target.closest('[data-jump]'); if(!b) return;
    var t=document.getElementById(b.dataset.jump); if(!t) return; t.scrollIntoView({behavior:RM.matches?'auto':'smooth',block:'start'});
    var h=$('h2, h3',t)||t; if(!h.hasAttribute('tabindex')) h.setAttribute('tabindex','-1'); h.focus({preventScroll:true});});
  addEventListener('hashchange',function(){tabs(); requestAnimationFrame(spine);});
  addEventListener('resize',function(){requestAnimationFrame(spine);});
  if(window.ResizeObserver){var ro=new ResizeObserver(function(){spine();}); var c=$('[data-circuit]'); if(c) ro.observe(c);}
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(spine);
  tabs();
  AtlasKit.init({inkSelection:true});
  spine();
})();
"""


def kit_js():
    src = (KIT / 'atlas-kit.js').read_text()
    a = "if (sel && !reform && !busy) mark(sel, 'selected item');"
    assert a in src
    src = src.replace(a, "if (sel && !reform && !busy && !S.opts.inkSelection) mark(sel, 'selected item');   // system 01: selection stays in ink")
    b = "const root = rootOf(S.view), item = key && $(`[data-select=\"${key}\"]`, root);"
    assert b in src
    src = src.replace(b, "const root = rootOf(S.view), item = key && ($$(`[data-select=\"${key}\"]`, root).find(vis) || $(`[data-select=\"${key}\"]`, root));   // system 01: the visible artboard")
    c = "const path = keysOf(k).map((key) => $(`[data-select=\"${key}\"] path.ak-mark`, view)).find(Boolean);"
    assert c in src
    src = src.replace(c, "const path = keysOf(k).map((key) => $$(`[data-select=\"${key}\"] path.ak-mark`, view).find(vis)).find(Boolean);   // system 01")
    return src


def build():
    kit_css = (KIT / 'atlas-kit.css').read_text()
    views = ' '.join(v for v, _ in VIEWS)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(ED["meta"]["title"])} Times Explainer</title>'
            f'<meta name="atlas-views" content="{views}">'
            '<meta name="description" content="Editorial system 01 for the Oath &amp; Action systems atlas: the system told in order, with annotated drawings.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800'
            '&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{kit_css}{CSS}</style></head><body data-surface="white">'
            + masthead() + '<div class="wrap"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>'
            '<p class="ak-vh" data-ak-status role="status"></p><main class="ak-stage" id="main">'
            + view_overview() + view_area() + view_r10() + view_r01() + view_loops() + view_read()
            + '</main></div>' + panel() + footer() + f'<div hidden>{templates()}</div>'
            + f'<script>{kit_js()}</script><script>{JS}</script></body></html>')
    assert '—' not in re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    OUT.write_text(page)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1024:.0f} KB')


if __name__ == '__main__':
    build()
