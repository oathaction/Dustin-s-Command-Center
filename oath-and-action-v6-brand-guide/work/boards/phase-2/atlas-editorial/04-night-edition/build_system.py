"""Editorial atlas system 04, Night Edition (Charcoal). Oath & Action Edition 06, Phase 2, November 5, 2026.

Builds one self-contained page with six hash views from the shared editorial dataset:
    python3 -I work/boards/phase-2/atlas-editorial/04-night-edition/build_system.py

Reads   work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json (the dataset, DR-28 to DR-35)
        work/extract/atlas-interactive-concept-v2-data.json (which of the two questions each part answers)
        work/build/scripts/phase-2/atlas_concepts_common.py (palette, icon_svg)
        work/extract/atlas-v7-data.json (the claims and sources behind each figure in the 16 everyday answers)
        work/boards/phase-2/atlas-concepts/shared/atlas-kit.js and atlas-kit.css (behavior, inlined)
        work/build/assets/identity/wordmark/ (the 24 px and 16 px wordmark masters, inlined as delivered)
Writes  work/boards/phase-2/atlas-editorial/04-night-edition/20261105_Editorial-04-Night-Edition.html

Every label, count, sign, grade, delay, example and reform text on the page is read from the data here. Headlines
and decks are studio drafts, listed in the notes. Interface words (buttons, section names, legends) are written here.
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

D = json.loads((ROOT / 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json').read_text())
IC = json.loads((ROOT / 'work/extract/atlas-interactive-concept-v2-data.json').read_text())
KIT_JS = (ROOT / 'work/boards/phase-2/atlas-concepts/shared/atlas-kit.js').read_text()
KIT_CSS = (ROOT / 'work/boards/phase-2/atlas-concepts/shared/atlas-kit.css').read_text()
WORDMARK_24 = (ROOT / 'work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg').read_text()
WORDMARK_16 = (ROOT / 'work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg').read_text()
OUT = HERE / '20261105_Editorial-04-Night-Edition.html'

NODES, LINKS, LOOPS, REFORMS, ISSUES = D['nodes'], D['links'], D['loops'], D['reforms'], D['issues']
PARTS = {p['id']: p for p in D['parts']}
PART_ORDER = [p['id'] for p in D['parts']]                     # X, A, B, C, D, E, EC, TC
CORE = ['A', 'B', 'C', 'D', 'E']
PART_OF = {n: p['id'] for p in D['parts'] for n in p['nodes']}
DOMAINS = {x['id']: x for x in D['domains']}
HUBS = D['hubs']
PATHWAYS = {p['id']: p for p in D['pathways']}
Q = D['questions']
PART_Q = {k: v.get('q', []) for k, v in IC['story']['parts'].items()}  # which question each part answers
COUNTS = D['meta']['counts']
P = acc.PALETTE
MINUS = '−'
SNAP = 'October 15, 2026'

LOWER_OK = {'A', 'An', 'The', 'On', 'In', 'Where', 'Both', 'Two', 'It', 'Its', 'This', 'These', 'That', 'Courts', 'Effects', 'When', 'Voters'}


def asof(text):
    """Every sentence that names the November 3, 2026 ballot opens "As of October 15, 2026," (the snapshot date)."""
    if 'November 3, 2026' not in text:
        return text
    out = []
    for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z])', text):
        if 'November 3, 2026' in sent and 'As of October 15, 2026' not in sent:
            first = sent.split(' ', 1)[0]
            sent = 'As of October 15, 2026, ' + (sent[0].lower() + sent[1:] if first in LOWER_OK else sent)
        out.append(sent)
    return ' '.join(out)


def e(s):
    return html.escape(asof(str(s)), quote=True)


# --------------------------------------------------------------------------------------- words from the data
GRADE = {   # V7 word, plain gloss, texture (M1, M2)
    'documented': ('Documented', 'on the public record', 'solid'),
    'well-supported': ('Well supported', 'strong research evidence', 'solid'),
    'well_supported': ('Well supported', 'strong research evidence', 'solid'),
    'plausible': ('Plausible', 'some evidence', 'dashed'),
    'plausible_contested': ('Contested', 'evidence disputed', 'dashdot'),
    'contested': ('Contested', 'evidence disputed', 'dashdot'),
    'hypothesis': ('Hypothesis', 'untested', 'dotted'),
    'mixed': ('Mixed', 'studies point different ways', 'solid'),
}
RANK = {'hypothesis': 1, 'plausible_contested': 2, 'plausible': 2, 'well-supported': 3, 'documented': 4}
DELAY = {'S': 'under 2 years', 'M': '2 to 10 years', 'L': 'over 10 years'}
TICKS = {'S': 1, 'M': 2, 'L': 3}
DIRECTION = {'running_up': 'Running up', 'running_down': 'Running down', 'running': 'Running', 'unknown': 'Direction not yet clear',
             'disabled': 'Switched off in practice', 'disabled in concentrated sectors': 'Switched off in concentrated sectors',
             'design_target': 'A design goal'}


def grade_word(g):
    return GRADE[g][0]


def grade_gloss(g):
    return GRADE[g][1]


def sign_char(p):
    return '+' if p == '+' else MINUS if p == '-' else ''


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def verb(p):
    return 'raises' if p == '+' else 'lowers' if p == '-' else 'decides'


def sign_words(p):
    if p == '+':
        return 'plus: the two move the same way'
    if p == '-':
        return 'minus: the two move in opposite ways'
    return 'no sign: this line says who decides'


def sent(t):
    t = (t or '').strip()
    return t if t.endswith(('.', '?', '!')) else t + '.'


def lab(n):
    """The short label (the dark atlas's plain layer, DR-35); falls back to the V7 title."""
    return NODES[n]['label']


def lower_first(s):
    return s[0].lower() + s[1:] if s and not s.startswith(('Congress', 'AI ')) else s


def first_sentence(text):
    m = re.match(r'(.+?[.?!])(\s|$)', text or '')
    return m.group(1) if m else (text or '')


def loop_labels(lid):
    """Station labels in order: the short label for variables, the loop's own words for sketched stations."""
    return [lab(s['code']) if s.get('code') else s['label'] for s in LOOPS[lid]['stations']]


COUNT_FIRST = {'Seats', 'Incumbents', 'Rulings', 'Watchdogs', 'Ties'}   # labels that count things take "fewer"
COUNT_LAST = {'seats', 'tests'}


def countable(label):
    w = label.split()
    return (w[0] in COUNT_FIRST or w[-1] in COUNT_LAST) and 'control' not in w


def amount(state, label):
    """"more" or "less", and "fewer" for countable things (red team, shared fix 5)."""
    word = 'more' if state > 0 else ('fewer' if countable(label) else 'less')
    return f'{word} {lower_first(label)}'


def read_aloud(lid):
    """Built from the signs, so it cannot drift (civic education memo, section 2)."""
    names = loop_labels(lid)
    state, parts = 1, []
    for i, st in enumerate(LOOPS[lid]['steps']):
        parts.append(amount(state, names[i]))
        state *= 1 if st['polarity'] == '+' else -1
    parts[0] = parts[0][0].upper() + parts[0][1:]
    return ', '.join(parts) + ', and back to ' + amount(state, names[0]) + '.'


def kind_line(lid):
    L = LOOPS[lid]
    return f"{L['kind_word']}, {L['kind_gloss']}"


def step_grades(lid):
    return [s['evidence'] for s in LOOPS[lid]['steps'] if s.get('evidence')]


def weakest_of(lid):
    """The data's weakest steps; where it lists none and the grades differ, the lowest grade (R3 only, which its
    own evidence summary names as L47)."""
    L = LOOPS[lid]
    if L['conceptual']:
        return []
    if L['weakest']:
        return list(L['weakest'])
    ranks = {s['id']: RANK[s['evidence']] for s in L['steps']}
    if len(set(ranks.values())) == 1:
        return []
    lo = min(ranks.values())
    return [k for k, v in ranks.items() if v == lo]


def weakest_words(lid):
    L = LOOPS[lid]
    if L['conceptual']:
        return 'Sketch: no step is a numbered connection'
    w = weakest_of(lid)
    if w:
        return 'Weakest step' + ('s ' if len(w) > 1 else ' ') + ' and '.join(f"{k}, {grade_word(LINKS[k]['evidence']).lower()}" for k in w)
    return f'Every step {grade_word(step_grades(lid)[0]).lower()}'


def reforms_words(n):
    return 'no reform aims here yet' if n == 0 else f"{n} reform{'s' if n != 1 else ''} aim{'s' if n == 1 else ''} here"


def status_line(lid):
    L = LOOPS[lid]
    return ' · '.join([DIRECTION.get(L['direction'], L['direction'] or ''), f"{L['delay_word']} a turn", weakest_words(lid),
                       reforms_words(len(L['reforms']))])


def disclosure(lid):
    L = LOOPS[lid]
    if L['conceptual']:
        tail = L['how_to_read'].split('; ')[-1].rstrip('.')
        return f"A sketch with no complete numbered chain: {tail}."
    if L['hypothesized']:
        hyp = [s['id'] for s in L['steps'] if s['evidence'] == 'hypothesis']
        return f"Closed with a hypothesized step: {' and '.join(hyp)} {'is' if len(hyp) == 1 else 'are'} graded hypothesis (untested)."
    return ''


def loop_home(lid):
    return LOOPS[lid].get('home') or 'SK'


def part_name(pid):
    return PARTS[pid]['plain_name']


def link_sentence(k):
    l = LINKS[k]
    return f"{lab(l['from'])} {verb(l['polarity'])} {lower_first(lab(l['to']))}"


# --------------------------------------------------------------------------------------- counts
def between(a, b):
    return [k for k, l in LINKS.items() if PART_OF[l['from']] == a and PART_OF[l['to']] == b]


def inside(a):
    return between(a, a)


def links_touching_part(pid):
    return [k for k, l in LINKS.items() if pid in (PART_OF[l['from']], PART_OF[l['to']])]


def loops_home(pid):
    return [k for k in D['loop_order'] if loop_home(k) == pid]


def loops_through(pid):
    return [k for k in D['loop_order'] if any(s.get('code') and PART_OF[s['code']] == pid for s in LOOPS[k]['stations'])]


def reforms_aimed(pid):
    def touches(t):
        if t in NODES:
            return PART_OF[t] == pid
        l = LINKS.get(t)
        return bool(l) and pid in (PART_OF[l['from']], PART_OF[l['to']])
    return [k for k in sorted(REFORMS) if any(touches(t) for t in REFORMS[k]['targets'])]


def issues_in(pid):
    vs = set(PARTS[pid]['nodes'])
    return [k for k, i in ISSUES.items() if not i.get('retired') and vs & set(i.get('nodes') or [])]


N_R = sum(1 for l in LOOPS.values() if l['type'] == 'R')
N_B = sum(1 for l in LOOPS.values() if l['type'] == 'B')
N_WITH_REFORM = sum(1 for l in LOOPS.values() if l['reforms'])
N_BETWEEN = sum(1 for l in LINKS.values() if PART_OF[l['from']] != PART_OF[l['to']])
N_INSIDE = len(LINKS) - N_BETWEEN
WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def cnt(key, n, cls='n'):
    return f'<span class="{cls}" data-count="{key}">{n}</span>'


# --------------------------------------------------------------------------------------- text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False):
    """Rendered width estimate. Inter Tight sets about 6 percent narrower than Inter at display sizes."""
    w = _font(weight).getlength(text) * size / 200
    return w * 0.94 if tight else w


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


def fnum(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


_UID = [0]


def uid(prefix='u'):
    _UID[0] += 1
    return f'{prefix}{_UID[0]}'


def icon(node_or_reform, size, x=None, y=None, edition='newsprint'):
    """A Civic Line icon exactly as drawn (D2-52), one-color Newsprint edition on Charcoal (D2-58)."""
    ic = acc.VARIABLE_ICON.get(node_or_reform) or acc.reform_icon(node_or_reform)
    s = acc.icon_svg(ic, edition, uid=uid('i'), size=size)
    if x is not None:
        s = s.replace('<svg ', f'<svg x="{fnum(x)}" y="{fnum(y)}" ', 1)
    return s


ICON_MIN = {}
_inv = json.loads((ROOT / 'work/build/assets/civic-line/20261029_Civic-Line-Inventory.json').read_text())
for _ic in _inv['icons']:
    ICON_MIN[_ic['id']] = 48 if _ic['tile_min_px']['one-color']['square'] > 48 else 32


# --------------------------------------------------------------------------------------- line machinery
# Design frame memo, section 3: one stroke family (1, 1.5, 2, 3, 6 px), one arrowhead sized by weight, the pointing
# sign tag, delay ticks, the open diamond for authority, and V7's evidence textures as multiples of the line width.
HEAD = {2: (10, 8), 3: (13, 11), 6: (22, 18)}          # length, base
TAG = {2: (20, 16), 3: (21, 17), 6: (26, 22)}          # length, height
BEND = {2: 8, 3: 12, 6: 18}


def unit(dx, dy):
    L = math.hypot(dx, dy) or 1
    return dx / L, dy / L


def seg_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def point_at(pts, s):
    """Point and direction at distance s along a polyline."""
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= L or b is pts[-1]:
            ux, uy = unit(b[0] - a[0], b[1] - a[1])
            t = min(s, L)
            return a[0] + ux * t, a[1] + uy * t, ux, uy
        s -= L
    return pts[-1][0], pts[-1][1], 1, 0


def rounded_d(pts, r):
    """Orthogonal polyline with rounded bends."""
    if len(pts) == 2:
        return f'M{fnum(pts[0][0])} {fnum(pts[0][1])}L{fnum(pts[1][0])} {fnum(pts[1][1])}'
    d = f'M{fnum(pts[0][0])} {fnum(pts[0][1])}'
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        u1 = unit(b[0] - a[0], b[1] - a[1])
        u2 = unit(c[0] - b[0], c[1] - b[1])
        rr = min(r, math.hypot(b[0] - a[0], b[1] - a[1]) / 2, math.hypot(c[0] - b[0], c[1] - b[1]) / 2)
        p1 = (b[0] - u1[0] * rr, b[1] - u1[1] * rr)
        p2 = (b[0] + u2[0] * rr, b[1] + u2[1] * rr)
        d += f'L{fnum(p1[0])} {fnum(p1[1])}Q{fnum(b[0])} {fnum(b[1])} {fnum(p2[0])} {fnum(p2[1])}'
    d += f'L{fnum(pts[-1][0])} {fnum(pts[-1][1])}'
    return d


def path_length(pts, r):
    """Length of the rounded path: each bend saves (2 - pi/2) r."""
    L = seg_len(pts)
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        rr = min(r, math.hypot(b[0] - a[0], b[1] - a[1]) / 2, math.hypot(c[0] - b[0], c[1] - b[1]) / 2)
        L -= (2 - math.pi / 2) * rr
    return L


def texture_of(grade):
    if grade is None:
        return 'hollow'
    return GRADE[grade][2]


def dash(tex, w, length):
    """A dash array fitted to the path so the line starts and ends on ink (design frame memo, rule 3.2)."""
    if tex in ('solid', 'hollow'):
        return ''
    if tex == 'dashed':
        a, g = 4 * w, 2 * w
        n = max(1, round((length - a) / (a + g)))
        k = length / (a + n * (a + g))
        return f' stroke-dasharray="{fnum(a * k)} {fnum(g * k)}"'
    if tex == 'dashdot':
        a, g, b = 4 * w, 1.5 * w, w
        n = max(1, round((length - a) / (a + 2 * g + b)))
        k = length / (a + n * (a + 2 * g + b))
        return f' stroke-dasharray="{fnum(a * k)} {fnum(g * k)} {fnum(b * k)} {fnum(g * k)}"'
    if tex == 'dotted':
        g = 2.5 * w
        n = max(1, round(length / g))
        return f' stroke-dasharray="0 {fnum(length / n)}" stroke-linecap="round"'
    return ''


def head_shape(x, y, ux, uy, w, cls='hd'):
    L, B = HEAD[w]
    bx, by = x - ux * L, y - uy * L
    px, py = -uy, ux
    pts = [(x, y), (bx + px * B / 2, by + py * B / 2), (bx - px * B / 2, by - py * B / 2)]
    return f'<path class="{cls}" d="M{fnum(pts[0][0])} {fnum(pts[0][1])}L{fnum(pts[1][0])} {fnum(pts[1][1])}L{fnum(pts[2][0])} {fnum(pts[2][1])}Z"/>'


def diamond_shape(x, y, ux, uy, cls='dm'):
    """Open diamond, 14 by 11 px, 2 px stroke, ground fill: an authority connection ends here."""
    L, B = 14, 11
    cx, cy = x - ux * L / 2, y - uy * L / 2
    px, py = -uy, ux
    pts = [(x, y), (cx + px * B / 2, cy + py * B / 2), (x - ux * L, y - uy * L), (cx - px * B / 2, cy - py * B / 2)]
    d = 'M' + 'L'.join(f'{fnum(a)} {fnum(b)}' for a, b in pts) + 'Z'
    return f'<path class="{cls}" d="{d}" stroke-width="2"/>'


def tag_shape(cx, cy, ux, uy, sign, w):
    """The pointing tag: a filled body that points the way the step runs, the sign upright inside in the ground color."""
    L, H = TAG[w]
    body = L - 6
    px, py = -uy, ux
    back = (cx - ux * L / 2, cy - uy * L / 2)
    shoulder = (back[0] + ux * body, back[1] + uy * body)
    tip = (cx + ux * L / 2, cy + uy * L / 2)
    pts = [(back[0] + px * H / 2, back[1] + py * H / 2), (shoulder[0] + px * H / 2, shoulder[1] + py * H / 2), tip,
           (shoulder[0] - px * H / 2, shoulder[1] - py * H / 2), (back[0] - px * H / 2, back[1] - py * H / 2)]
    d = 'M' + 'L'.join(f'{fnum(a)} {fnum(b)}' for a, b in pts) + 'Z'
    sx, sy = back[0] + ux * body / 2, back[1] + uy * body / 2      # sign centered on the body
    bar = min(w, 3) if w > 2 else 2
    half = 4 if w <= 3 else 5
    s = f'<path class="tg" d="{d}"/>'
    s += f'<path class="sg" d="M{fnum(sx - half)} {fnum(sy)}H{fnum(sx + half)}" stroke-width="{bar}"/>'
    if sign == '+':
        s += f'<path class="sg" d="M{fnum(sx)} {fnum(sy - half)}V{fnum(sy + half)}" stroke-width="{bar}"/>'
    return s


def tick_marks(pts, r, count, w):
    out = []
    for i in range(count):
        x, y, ux, uy = point_at(pts, 12 + 5 * i)
        px, py = -uy, ux
        h = (w + 8) / 2
        out.append(f'M{fnum(x - px * h)} {fnum(y - py * h)}L{fnum(x + px * h)} {fnum(y + py * h)}')
    return f'<path class="tk" d="{"".join(out)}" stroke-width="2"/>' if out else ''


def wire(pts, w, grade, sign, delay=None, tag_at=0.5, end='head', cls='', authority=False):
    """One step. pts run from 2 px off the source edge to 2 px off the target edge. Returns (marks, path d, length)."""
    r = BEND[w]
    tex = 'solid' if authority else texture_of(grade)
    ex, ey = pts[-1]
    ux, uy = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    stop = HEAD[w][0] if end == 'head' else 14
    body = pts[:-1] + [(ex - ux * stop, ey - uy * stop)]
    if tex == 'dotted':
        body = pts[:-1] + [(ex - ux * (stop + 1.5 * w), ey - uy * (stop + 1.5 * w))]
    d = rounded_d(body, r)
    L = path_length(body, r)
    out = ''
    if tex == 'hollow':
        out += f'<path class="ak-mark ln{cls}" d="{d}" stroke-width="{w + 2}" fill="none"/>'
        out += f'<path class="hl" d="{d}" stroke-width="{max(w - 0.5, 1)}" fill="none"/>'
    else:
        out += f'<path class="ak-case" d="{d}" fill="none"{dash(tex, w, L)}/>'
        out += f'<path class="ak-mark ln{cls}" d="{d}" stroke-width="{w}" fill="none"{dash(tex, w, L)}/>'
    if delay:
        out += tick_marks(body, r, TICKS[delay], w)
    if end == 'head':
        out += head_shape(ex, ey, ux, uy, w)
    elif end == 'diamond':
        out += diamond_shape(ex, ey, ux, uy)
    if sign in ('+', '-') and tag_at is not None:
        tx, ty, tux, tuy = point_at(body, L * tag_at if tag_at <= 1 else tag_at)
        out += tag_shape(tx, ty, tux, tuy, sign, w)
    hit = f'<path class="ak-hit" d="{d}"/>'
    return out + hit, d, L


def wire_tag_end(pts, w, grade, sign, delay=None, cls=''):
    """A small-cycle step: the pointing tag doubles as the arrowhead (dataviz memo, part 1), so the texture runs
    clear from the source to the tag. Returns marks, the tag's centre and direction."""
    tex = texture_of(grade)
    ex, ey = pts[-1]
    ux, uy = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    Lt = TAG[w][0]
    body = pts[:-1] + [(ex - ux * Lt, ey - uy * Lt)]
    if tex == 'dotted':
        body = pts[:-1] + [(ex - ux * (Lt + 1.5 * w), ey - uy * (Lt + 1.5 * w))]
    r = BEND[w]
    d = rounded_d(body, r)
    L = path_length(body, r)
    out = ''
    if tex == 'hollow':
        out += f'<path class="ak-mark ln{cls}" d="{d}" stroke-width="{w + 2}" fill="none"/>'
        out += f'<path class="hl" d="{d}" stroke-width="{w}" fill="none"/>'
    else:
        out += f'<path class="ak-case" d="{d}" fill="none"{dash(tex, w, L)}/>'
        out += f'<path class="ak-mark ln{cls}" d="{d}" stroke-width="{w}" fill="none"{dash(tex, w, L)}/>'
    if delay:
        out += tick_marks(body, r, TICKS[delay], w)
    cx, cy = ex - ux * Lt / 2, ey - uy * Lt / 2
    out += tag_shape(cx, cy, ux, uy, sign, w)
    out += f'<path class="ak-hit" d="{d}"/>'
    return out, (cx, cy, ux, uy), L


def svg_text(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{fnum(x)}" y="{fnum(y)}" class="{cls}"{a}{extra}>{e(s)}</text>'


def svg_lines(x, y, rows, cls, lh, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    spans = ''.join(f'<tspan x="{fnum(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{fnum(x)}" y="{fnum(y)}" class="{cls}"{a}{extra}>{spans}</text>'


# Small-cycle geometry (the loop cards). Wide artboard: shapes after the dark grid Dustin marked "I like this design".
CARD_W, CARD_TILE, CARD_GAPX, CARD_GAPY = 388, 150, 88, 84
CHAIN_W, CHAIN_TILE, CHAIN_GAP, CHAIN_TOP = 320, 262, 70, 80
LBL = (15, 600)     # map label, Inter 600 15/18
NOTE = (13, 500)    # note, Inter 13/16, one weight heavier on Charcoal


def station_label_rows(lid, i, width):
    return wrap(loop_labels(lid)[i], width, *LBL)


def tile_svg(lid, i, x, y, w, h, mode, interactive=False, rel=''):
    st = LOOPS[lid]['stations'][i]
    code = st.get('code')
    name = loop_labels(lid)[i]
    out = ''
    if mode == 'card':
        rows = station_label_rows(lid, i, w - 20)
        if code:
            out += icon(code, 48, x + 10, y + 10)
            ty = y + 10 + 48 + 8 + 13
        else:
            ty = y + 24
        lbl = svg_lines(x + 10, ty, rows, 'tl', 18, extra=(f' data-node="{code}" data-name="{e(name)}"' if code else ''))
        note = '' if code else svg_text(x + 10, y + h - 12, 'Not a model variable', 'nt')
    else:   # chain
        rows = wrap(name, w - 66 - 10, *LBL)
        if code:
            out += icon(code, 48, x + 8, y + (h - 48) / 2)
        lx = x + 66 if code else x + 12
        ty = y + h / 2 - (len(rows) - 1) * 9 + 5
        if not code:
            rows = wrap(name, w - 24, *LBL)
            ty = y + h / 2 - (len(rows) - 1) * 9 - 3
        lbl = svg_lines(lx, ty, rows, 'tl', 18, extra=(f' data-node="{code}" data-name="{e(name)}"' if code else ''))
        note = '' if code else svg_text(lx, y + h - 10, 'Not a model variable', 'nt ph')
    box = f'<rect class="ak-mark bx{"" if code else " bx-sk"}" x="{fnum(x)}" y="{fnum(y)}" width="{fnum(w)}" height="{fnum(h)}"/>'
    body = box + out + lbl + note
    if interactive and code:
        say = f"{code} {name}. {NODES[code]['increase_means']}"
        return (f'<g class="st" data-select="var-{code.lower()}" data-node="{code}" data-rel="{rel}" role="button" '
                f'aria-label="{e(say)}" data-say="{e(say)}">{body}</g>')
    return f'<g class="st"{f" data-node={chr(34)}{code}{chr(34)}" if code else ""}>{body}</g>'


def step_group(lid, k, marks, labels, interactive=False):
    st = LOOPS[lid]['steps'][k]
    if st.get('id'):
        l = LINKS[st['id']]
        attrs = (f'data-link="{st["id"]}" data-sign="{sign_attr(l["polarity"])}" data-grade="{l["evidence"]}" '
                 f'data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}"')
        if interactive:
            say = (f"{st['id']}: {l['name']}. {lab(l['from'])} {verb(l['polarity'])} {lower_first(lab(l['to']))}. "
                   f"{grade_word(l['evidence'])}, {grade_gloss(l['evidence'])}. {DELAY[l['delay']].capitalize()}.")
            rel = f'var-{l["from"].lower()} var-{l["to"].lower()}'
            return (f'<g class="sp" data-select="link-{st["id"].lower()}" {attrs} data-rel="{rel}" role="button" '
                    f'aria-label="{e(say)}" data-say="{e(say)}">{marks}{labels}</g>')
        return f'<g class="sp" {attrs}>{marks}{labels}</g>'
    return f'<g class="sp sp-sk">{marks}{labels}</g>'


def step_words(lid, k):
    """Verb, and for the narrow chain the grade and delay in words; the weakest step says so."""
    L = LOOPS[lid]
    st = L['steps'][k]
    weak = st.get('id') in weakest_of(lid)
    if st.get('id'):
        l = LINKS[st['id']]
        detail = f"{grade_word(l['evidence'])} · {DELAY[l['delay']]}"
    else:
        detail = 'Sketched step'
    return verb(st['polarity']), detail, weak


def cycle_card(lid):
    """Wide artboard: two stations side by side with the return beneath, three as a triangle, four as a square."""
    L = LOOPS[lid]
    n = len(L['stations'])
    TWd = CARD_TILE
    lines = max(len(station_label_rows(lid, i, TWd - 20)) for i in range(n))
    has_sk = any(not s.get('code') for s in L['stations'])
    TH = 10 + 48 + 8 + lines * 18 + 6 if not all(not s.get('code') for s in L['stations']) else 24 + lines * 18 + 30
    if has_sk:
        TH = max(TH, 24 + lines * 18 + 30)
    W = CARD_W
    xl, xr = 0, W - TWd
    cl, cr = xl + TWd / 2, xr + TWd / 2
    yb = TH + CARD_GAPY
    if n == 2:
        tiles = [(xl, 0), (xr, 0)]
        H = TH + 30 + 26
    elif n == 3:
        xm = (W - TWd) / 2
        tiles = [(xm, 0), (xr, yb), (xl, yb)]
        H = yb + TH
    else:
        tiles = [(xl, 0), (xr, 0), (xr, yb), (xl, yb)]
        H = yb + TH
    out = ''
    labels_out = []
    for k, st in enumerate(L['steps']):
        a, b = k, (k + 1) % n
        verb_w, _, weak = step_words(lid, k)
        grade = LINKS[st['id']]['evidence'] if st.get('id') else None
        delay = LINKS[st['id']]['delay'] if st.get('id') else None
        lab_items = []
        ax, ay = tiles[a]
        bx, by = tiles[b]
        if n == 2 and k == 0 or (n == 4 and k in (0, 2)) or (n == 3 and k == 1):
            # horizontal step across the column gap, in the row of both tiles
            yy = ay + TH / 2
            if bx > ax:
                pts = [(ax + TWd + 2, yy), (bx - 2, yy)]
            else:
                pts = [(ax - 2, yy), (bx + TWd + 2, yy)]
            mx = W / 2
            lab_items.append(svg_text(mx, yy - 14, verb_w, 'vb', 'middle'))
            if weak:
                lab_items.append(svg_text(mx, yy + 26, 'weakest', 'wk', 'middle'))
        elif n == 2 and k == 1:
            # the return runs beneath both tiles
            yy = TH + 30
            pts = [(cr, TH + 2), (cr, yy), (cl, yy), (cl, TH + 2)]
            lab_items.append(svg_text(cl + 16, yy - 10, verb_w + (' · weakest' if weak else ''), 'vb' + (' wkv' if weak else '')))
        elif n == 4 and k in (1, 3):
            xx = cr if k == 1 else cl
            if k == 1:
                pts = [(xx, TH + 2), (xx, yb - 2)]
                lx, anc = xx - 14, 'end'
            else:
                pts = [(xx, yb - 2), (xx, TH + 2)]
                lx, anc = xx + 14, 'start'
            my = TH + CARD_GAPY / 2
            lab_items.append(svg_text(lx, my + 4, verb_w, 'vb', anc))
            if weak:
                lab_items.append(svg_text(lx, my + 22, 'weakest', 'wk', anc))
        elif n == 3 and k == 0:
            xm = tiles[0][0]
            pts = [(xm + TWd + 2, TH / 2), (cr, TH / 2), (cr, yb - 2)]
            my = TH + CARD_GAPY / 2
            lab_items.append(svg_text(cr + 14, my + 10, verb_w, 'vb'))
            if weak:
                lab_items.append(svg_text(cr + 14, my + 28, 'weakest', 'wk'))
        else:   # n == 3, k == 2: bottom left back up to the top tile
            xm = tiles[0][0]
            pts = [(cl, yb - 2), (cl, TH / 2), (xm - 2, TH / 2)]
            lab_items.append(svg_text((cl + xm) / 2 - 4, TH / 2 - 14, verb_w, 'vb', 'middle'))
            if weak:
                lab_items.append(svg_text(cl - 12, TH + CARD_GAPY / 2 + 4, 'weakest', 'wk', 'end'))
        marks, _, _ = wire_tag_end(pts, 2, grade, st['polarity'], delay)
        out += step_group(lid, k, marks, ''.join(lab_items))
    for i, (x, y) in enumerate(tiles):
        out += tile_svg(lid, i, x, y, TWd, TH, 'card')
    steps = 'sketch' if L['conceptual'] else ' '.join(s['id'] for s in L['steps'])
    return (f'<svg class="cy cy-wide" data-view="loop-{lid.lower()}-shape" data-loop="{lid}" data-steps="{steps}" '
            f'viewBox="0 0 {W} {fnum(H)}" width="{W}" height="{fnum(H)}" role="img" '
            f'aria-label="{e(kind_line(lid) + ". " + read_aloud(lid))}">{out}</svg>')


def cycle_chain(lid):
    """Narrow artboard for phones: the stations top to bottom, the return up the right side and in from the top."""
    L = LOOPS[lid]
    n = len(L['stations'])
    TWd, TH, G, T = CHAIN_TILE, 64, CHAIN_GAP, CHAIN_TOP
    W = CHAIN_W
    ys = [T + i * (TH + G) for i in range(n)]
    H = ys[-1] + TH
    out = ''
    for k, st in enumerate(L['steps']):
        verb_w, detail, weak = step_words(lid, k)
        grade = LINKS[st['id']]['evidence'] if st.get('id') else None
        delay = LINKS[st['id']]['delay'] if st.get('id') else None
        labs = ''
        line1 = verb_w + (' · weakest' if weak else '')
        if k < n - 1:
            x = 34
            pts = [(x, ys[k] + TH + 2), (x, ys[k + 1] - 2)]
            my = ys[k] + TH + G / 2
            labs += svg_text(x + 22, my - 4, line1, 'vb ph' + (' wkv' if weak else ''))
            labs += svg_text(x + 22, my + 15, detail, 'gw ph')
        else:
            xr, xe = TWd + 34, TWd - 34
            pts = [(TWd + 2, ys[-1] + TH / 2), (xr, ys[-1] + TH / 2), (xr, 12), (xe, 12), (xe, T - 2)]
            parts_ = detail.split(' · ')
            labs += svg_text(xe - 16, 32, line1, 'vb ph' + (' wkv' if weak else ''), 'end')
            labs += svg_text(xe - 16, 51, parts_[0], 'gw ph', 'end')
            if len(parts_) > 1:
                labs += svg_text(xe - 16, 70, parts_[1], 'gw ph', 'end')
        marks, _, _ = wire_tag_end(pts, 2, grade, st['polarity'], delay)
        out += step_group(lid, k, marks, labs)
    for i, y in enumerate(ys):
        out += tile_svg(lid, i, 0, y, TWd, TH, 'chain')
    steps = 'sketch' if L['conceptual'] else ' '.join(s['id'] for s in L['steps'])
    return (f'<svg class="cy cy-narrow" data-view="loop-{lid.lower()}-chain" data-loop="{lid}" data-steps="{steps}" '
            f'viewBox="0 0 {W} {fnum(H)}" width="{W}" height="{fnum(H)}" role="img" '
            f'aria-label="{e(kind_line(lid) + ". " + read_aloud(lid))}">{out}</svg>')


# --------------------------------------------------------------------------------------- the stylesheet
# Night Edition: Charcoal ground; Newsprint for reading ink; Dim Newsprint (T4, 7.26:1) for secondary text; Stone
# (3.10:1) for context lines and card rules; White for the selection when a reform holds the red; Pillar Red (4.49:1)
# only where a reform acts. Locked palette and the two approved tints only: cards are Charcoal with a 1 px Stone rule.
CSS = r'''
:root{--ground:#121212;--panel:#121212;--ink:#DCD9D2;--dim:#A3A19C;--stone:#5D636D;--white:#FFFFFF;--red:#E63946;
 --ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px;--ak-panel-w:420px;
 --f-ui:Inter,system-ui,sans-serif;--f-disp:"Inter Tight",Inter,system-ui,sans-serif;--f-quote:Lora,Georgia,serif}
[data-surface="charcoal"]{--ak-ground:var(--ground);--ak-ink:var(--ink);--ak-muted:var(--stone);--ak-focus:var(--ink);--ak-sel:var(--white);--ak-red:var(--red)}
*{box-sizing:border-box}
html{background:var(--ground);color:var(--ink);-webkit-text-size-adjust:100%;scroll-padding-top:16px}
body{margin:0;background:var(--ground);color:var(--ink);font:400 17px/27px var(--f-ui);font-feature-settings:"cv11","ss01";-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{text-decoration-thickness:2px}
button{font:inherit;color:inherit}
p{margin:0}
h1,h2,h3,h4{margin:0;font-weight:inherit;text-wrap:balance}
ul,ol{margin:0;padding:0}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}

/* type scale, design frame memo section 2; 13 to 15 px text sets one weight heavier on Charcoal */
.eyebrow{font:700 13px/18px var(--f-ui);letter-spacing:.06em;text-transform:uppercase;color:var(--dim)}
.display{font:800 56px/60px var(--f-disp);letter-spacing:-.035em;text-wrap:balance;margin-left:-.04em}
.headline{font:800 40px/44px var(--f-disp);letter-spacing:-.03em;text-wrap:balance}
.deck{font:400 19px/28px var(--f-ui);color:var(--ink);max-width:62ch}
.phead{font:800 22px/26px var(--f-disp);letter-spacing:-.02em}
.body{font:400 17px/27px var(--f-ui)}
.ptext{font:500 15px/23px var(--f-ui)}
.quote{font:italic 400 22px/31px var(--f-quote);letter-spacing:-.005em}
.fig{font:800 40px/40px var(--f-disp);letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.note{font:500 13px/16px var(--f-ui);letter-spacing:.01em}
.caption{font:500 14px/20px var(--f-ui)}
.legend{font:500 13px/18px var(--f-ui)}
.dim{color:var(--dim)}
.n{font-variant-numeric:tabular-nums}

/* ID chips: the type word in an ink cell, the code in an outlined cell (Gate 1, M3) */
.chip{display:inline-flex;align-items:stretch;height:22px;vertical-align:2px;white-space:nowrap;margin-right:8px}
.chip b{display:flex;align-items:center;padding:0 7px;background:var(--ink);color:var(--ground);font:600 13px/1 var(--f-ui);letter-spacing:.06em;text-transform:uppercase}
.chip span{display:flex;align-items:center;padding:0 8px;border:1.5px solid var(--ink);border-left:0;font:700 13px/1 var(--f-ui);font-variant-numeric:tabular-nums}

/* masthead */
.mast{border-bottom:1px solid var(--stone)}
.mast .wrap{display:flex;align-items:center;gap:24px;height:72px}
.wm{display:block;color:var(--ink);line-height:0;flex:none}
.wm svg{display:block;width:221px;height:24px}
.wm .wm16{display:none}
.runhead{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding-left:24px;border-left:1px solid var(--stone);line-height:24px}
.tabs{display:flex;gap:4px;align-items:center}
.tabs a{display:flex;align-items:center;min-height:44px;padding:0 10px;font:600 15px/1 var(--f-ui);text-decoration:none;color:var(--dim);box-shadow:inset 0 -3px 0 transparent}
.tabs a:hover{color:var(--ink);text-decoration:underline}
.tabs a[aria-current="page"]{color:var(--ink);box-shadow:inset 0 -3px 0 var(--ink)}
.crumbrow{padding-top:16px;min-height:44px;color:var(--dim)}
.crumbrow .ak-crumbs a{color:var(--dim);text-decoration-color:var(--stone)}
.crumbrow .ak-crumbs [aria-current]{color:var(--ink)}
.status:empty{display:none}
.status{margin-top:8px;color:var(--ink)}

/* views */
[data-view-root]{padding-bottom:72px}
.vhead{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px;padding-top:24px;align-items:start}
.vhead-main{grid-column:1/span 8}
.vhead-side{grid-column:9/span 4}
.vhead .eyebrow{margin-bottom:14px;display:flex;align-items:center;flex-wrap:wrap;gap:4px 0}
.vhead .deck{margin-top:20px}
.sec{margin-top:72px;padding-top:20px;border-top:1px solid var(--ink)}
.sec-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.sec-head h2{font:800 40px/44px var(--f-disp);letter-spacing:-.03em;text-wrap:balance}
.sec-head p{color:var(--dim);font:500 15px/23px var(--f-ui);max-width:80ch}
.figline{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;max-width:40em;text-wrap:balance;margin-bottom:8px}

/* the questions */
.qcards{display:grid;gap:12px}
.qcard{background:var(--ground);border:1px solid var(--stone);padding:16px 20px 18px;border-top:2px solid var(--ink)}
.qcard .eyebrow{margin:0 0 6px}
.qcard h2{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;margin-bottom:8px}
.qcard p{font:500 15px/23px var(--f-ui);color:var(--dim)}

/* buttons that read as text */
.tbtn{appearance:none;border:0;background:none;padding:0;margin:0;text-align:left;cursor:pointer;font:inherit;color:inherit}
.tbtn:hover{text-decoration:underline;text-underline-offset:3px}
.more{display:inline-flex;align-items:center;gap:6px;min-height:32px;font:600 15px/1.2 var(--f-ui);color:var(--ink);text-decoration:underline;text-decoration-color:var(--stone);text-underline-offset:4px}
.more:hover{text-decoration-color:var(--ink)}
.more::after{content:"\2192"}

/* loop cards */
.lgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:48px 24px}
.lc{position:relative;padding-top:20px;border-top:1px solid var(--stone);display:flex;flex-direction:column;gap:6px}
.lc-art{margin-bottom:14px}
.lc-art svg{display:block;max-width:100%;height:auto}
.lc-art .cy-narrow{display:none}
.lc .lc-kind{font:500 13px/18px var(--f-ui);color:var(--dim);display:flex;align-items:center;flex-wrap:wrap}
.lc h3{font:800 22px/26px var(--f-disp);letter-spacing:-.02em}
.lc h3 a,.lc h3 button{text-decoration:none}
.lc h3 a::after,.lc h3 button::after{content:"";position:absolute;inset:0}
.lc h3 a:hover,.lc h3 button:hover{text-decoration:underline;text-underline-offset:4px}
.lc-title{font:500 15px/23px var(--f-ui);color:var(--dim)}
.lc-read{font:500 15px/23px var(--f-ui)}
.lc-status{font:500 13px/18px var(--f-ui);color:var(--dim);border-top:1px solid var(--stone);padding-top:8px;margin-top:4px}
.lc-disc{font:500 13px/18px var(--f-ui);color:var(--ink)}
.lc[data-ak-sel],.lc:has([data-ak-sel]){border-top-color:var(--ink)}

/* drawings */
svg text{font-family:var(--f-ui)}
.cy .bx,.dr .bx{fill:var(--panel);stroke-width:2px}
.st{color:var(--dim)}
.st .bx-sk{stroke-width:1px}
.sp{color:var(--ink)}
.ln{fill:none;stroke-linejoin:round}
.tg{fill:currentColor}
.hd{fill:var(--ak-hi,currentColor)}
.sg{stroke:var(--ground);fill:none}
.tk{stroke:var(--ak-hi,currentColor);fill:none}
.dm{fill:var(--ground);stroke:var(--ak-hi,currentColor)}
.hl{stroke:var(--ground);fill:none}
.tl{font:600 15px/18px var(--f-ui);fill:var(--ink)}
.vb{font:600 13px var(--f-ui);fill:var(--ink)}
.gw{font:500 13px var(--f-ui);fill:var(--dim)}
.wk,.nt{font:500 13px var(--f-ui);fill:var(--dim)}
.wkv{fill:var(--ink)}
.halo{paint-order:stroke;stroke:var(--ground);stroke-width:8px;stroke-linejoin:round}
[data-select].st:focus-visible,[data-select].sp:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
[data-select].st[data-ak-sel] .bx,.st.ak-target .bx,.st.ak-rel .bx{stroke-width:3px}
.st.ak-target .bx{stroke:var(--red)}
.ak-dim [data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target) .tg,.ak-dim [data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target) .hd{fill:var(--stone)}

/* the reading panel: a drawer on the right from 900 px, the kit's bottom sheet below */
.ak-panel{background:var(--panel);color:var(--ink);font:500 15px/23px var(--f-ui)}
.ak-panel .ak-panel-bar [data-ak-panel-kind]{color:var(--dim)}
.ak-panel h2{font:800 26px/30px var(--f-disp);letter-spacing:-.02em;margin:10px 0 14px}
.ak-panel h3{font:700 13px/18px var(--f-ui);letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin:22px 0 8px}
.ak-panel p+p{margin-top:10px}
.ak-panel dl{gap:6px 16px}
.ak-panel dt{color:var(--dim);font-weight:600}
.ak-panel ul,.ak-panel ol{padding-left:18px}
.ak-panel li+li{margin-top:6px}
.ak-panel .lead{font:500 17px/26px var(--f-ui)}
.ak-panel .pick{appearance:none;background:none;border:0;padding:0;color:var(--ink);text-decoration:underline;text-decoration-color:var(--stone);text-underline-offset:3px;cursor:pointer;font:inherit;text-align:left}
.ak-panel .pick:hover{text-decoration-color:var(--ink)}
.ak-panel .ak-btn{background:transparent;color:var(--ink);border-color:var(--ink)}
@media (min-width:900px){
 .ak-panel{position:fixed;top:0;right:0;bottom:0;width:var(--ak-panel-w);max-height:none;z-index:60;border-left:1px solid var(--stone);padding:24px 28px 40px}
}
@media (max-width:899.98px){.ak-panel{border-top:2px solid var(--ink)}}

/* footer */
.foot{border-top:1px solid var(--stone);padding:20px 0 40px}
.foot .wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
.foot p{font:500 13px/18px var(--f-ui);color:var(--dim)}

@media (max-width:1100px){.lgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:899.98px){
 .wrap{padding:0 20px}
 .mast .wrap{height:auto;flex-wrap:wrap;gap:0;padding-top:20px}
 .wm svg{width:152px;height:16px}
 .wm .wm24{display:none}.wm .wm16{display:block}
 .runhead{display:none}
 .tabs{width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:14px;border-top:1px solid var(--stone)}
 .tabs a{justify-content:center;font-size:14px;padding:0 4px;text-align:center}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline{font-size:30px;line-height:34px}
 .deck{font-size:17px;line-height:25px}
 .phead{font-size:20px;line-height:24px}
 .body{font-size:16px;line-height:25px}
 .quote{font-size:19px;line-height:27px}
 .fig{font-size:32px;line-height:32px}
 .vhead{display:block}
 .vhead-side{margin-top:24px}
 .sec{margin-top:56px}
 .sec-head h2{font-size:26px;line-height:30px}
 .figline{font-size:21px;line-height:26px}
}
@media (max-width:699.98px){
 .lgrid{grid-template-columns:1fr;gap:40px}
 .lc-art .cy-wide{display:none}
 .lc-art .cy-narrow{display:block}
}
'''


# --------------------------------------------------------------------------------------- shared HTML pieces
def chip(kind, code):
    return f'<span class="chip"><b>{e(kind)}</b><span>{e(code)}</span></span>'


TEMPLATES = {}   # data-detail key -> (kind, title, body html); every panel reads from the data


def tpl(key, kind, title, body):
    TEMPLATES[key] = (kind, title, body)


def loop_href(lid):
    return '#loop-r10' if lid == 'R10' else f'#loops/loop-{lid.lower()}'


def loop_card(lid, where='loops'):
    """One loop as a named box-and-arrow cycle with its plain name, V7 title, kind, read-aloud line and status."""
    L = LOOPS[lid]
    name = L['plain_name']
    if lid == 'R10':
        head = (f'<a href="#loop-r10" data-loop="R10" data-name="{e(name)}" '
                f'aria-label="{e(name)}, loop R10. Opens the full loop.">{e(name)}</a>')
    elif where == 'loops':
        head = (f'<button class="tbtn" type="button" data-select="loop-{lid.lower()}" data-loop="{lid}" data-name="{e(name)}" '
                f'data-say="{e(name)}, loop {lid}. {e(kind_line(lid))}.">{e(name)}</button>')
    else:
        head = (f'<a href="{loop_href(lid)}" data-loop="{lid}" data-name="{e(name)}" '
                f'aria-label="{e(name)}, loop {lid}. Opens it in the loop catalog.">{e(name)}</a>')
    disc = disclosure(lid)
    qual = f'<p class="lc-qual"><b>Keep in mind:</b> {e(L["qualification"])}</p>' if lid == 'R1' else ''
    return (f'<article class="lc" id="card-{where}-{lid.lower()}">'
            f'<p class="lc-kind">{chip("Loop", lid)}{e(kind_line(lid))}</p>'
            f'<h3>{head}</h3>'
            f'<p class="lc-title">{e(L["title"])}</p>'
            f'<div class="lc-art">{cycle_card(lid)}{cycle_chain(lid)}</div>'
            f'<p class="lc-sum">{e(first_sentence(L["summary"]))}</p>'
            f'<p class="lc-read"><b>Read it aloud:</b> {e(read_aloud(lid))}</p>{qual}'
            + (f'<p class="lc-disc">{e(disc)}</p>' if disc else '') +
            f'<p class="lc-status">{e(status_line(lid))}</p>'
            '</article>')


def loop_groups():
    """Home parts in story order, then the sketches; two-step loops first in each group (civic memo, section 6)."""
    out = []
    for pid in CORE + ['SK']:
        ls = [k for k in D['loop_order'] if loop_home(k) == pid]
        ls.sort(key=lambda k: (len(LOOPS[k]['stations']), D['loop_order'].index(k)))
        if ls:
            out.append((pid, ls))
    return out


# --------------------------------------------------------------------------------------- view: the loop catalog
def view_loops():
    groups = loop_groups()
    body = ''
    for pid, ls in groups:
        if pid == 'SK':
            title = 'Sketched loops'
            sub = 'Three loops without a complete numbered chain. Hollow lines mark their steps.'
        else:
            P_ = PARTS[pid]
            title = f'{P_["plain_name"]}'
            nr = sum(1 for k in ls if LOOPS[k]['type'] == 'R')
            nb = len(ls) - nr
            kinds = ', '.join(x for x in [f'{nr} reinforcing' if nr else '', f'{nb} balancing' if nb else ''] if x)
            sub = f'{P_["formal_title"]}. {len(ls)} loops live here: {kinds}.'
        body += (f'<section class="lgroup" aria-labelledby="lg-{pid.lower()}">'
                 f'<div class="lg-head"><h2 id="lg-{pid.lower()}" class="phead">{e(title)}</h2><p class="caption dim">{e(sub)}</p></div>'
                 f'<div class="lgrid">{"".join(loop_card(k) for k in ls)}</div></section>')
    head = (f'<header class="vhead"><div class="vhead-main">'
            f'<p class="eyebrow">The loop catalog</p>'
            f'<h1 class="display" data-ak-heading>{cnt("loops_reinforcing", N_R)} of the {cnt("loops", len(LOOPS))} loops can feed themselves. '
            f'{cnt("custom:loops-with-a-reform", N_WITH_REFORM)} have a reform aimed at them.</h1>'
            f'<p class="deck">A loop is a chain of causes that comes back to where it started. Each card draws one as boxes and arrows: '
            f'follow the arrows around, and read each step with its word, raises or lowers. '
            f'{e(next(g["definition"] for g in D["glossary"] if g["term"].startswith("Reinforcing loop")).split(". ")[-1])}</p>'
            f'</div><div class="vhead-side">{key_small()}</div></header>')
    return (f'<section data-view-root="loops" data-crumb="All 23 loops" data-parent="overview" aria-labelledby="h-loops">'
            f'<div class="wrap">{head.replace("data-ak-heading>", "data-ak-heading id=" + chr(34) + "h-loops" + chr(34) + ">", 1)}'
            f'<div class="strip" data-strip="loops">{body}</div></div></section>')


def key_small():
    """The reading key for loop drawings, drawn with the same marks."""
    rows = []
    def sample(tex, sign='+', ticks=None):
        pts = [(2, 12), (70, 12)]
        grade = {'solid': 'well-supported', 'dashed': 'plausible', 'dashdot': 'plausible_contested', 'dotted': 'hypothesis', 'hollow': None}[tex]
        m, _, _ = wire_tag_end(pts, 2, grade, sign, ticks)
        return f'<svg class="kl" data-view="key-{tex}" viewBox="0 0 72 24" width="72" height="24" aria-hidden="true"><g class="sp">{m}</g></svg>'
    rows.append((sample('solid', '+'), '<b>raises</b>: a plus sign. The two move the same way, which is not the same as good.'))
    rows.append((sample('solid', '-'), '<b>lowers</b>: a minus sign. The two move in opposite ways.'))
    rows.append((sample('solid', '+', 'S'), 'Solid: documented or well supported. Ticks count the wait: one, under 2 years; two, 2 to 10; three, over 10.'))
    rows.append((sample('dashed'), 'Dashed: plausible, some evidence.'))
    rows.append((sample('dashdot'), 'Dash and dot: contested, evidence disputed.'))
    rows.append((sample('dotted'), 'Dotted: hypothesis, untested.'))
    rows.append((sample('hollow'), 'Hollow: a sketched step with no numbered connection.'))
    lis = ''.join(f'<li>{s}<span>{t}</span></li>' for s, t in rows)
    return f'<div class="key"><p class="eyebrow">How to read a loop</p><ul class="keyl">{lis}</ul><a class="more" href="#how-to-read">The full key</a></div>'


# --------------------------------------------------------------------------------------- page shell
VIEWS = ['overview', 'area-c', 'loop-r10', 'reform-r01', 'loops', 'how-to-read']
TAB_NAMES = {'overview': 'Overview', 'area-c': 'Elections', 'loop-r10': 'Safe-seat loop', 'reform-r01': 'Reform R-01',
             'loops': 'All loops', 'how-to-read': 'How to read'}


def wordmark():
    w24 = WORDMARK_24.replace('<svg ', '<svg class="wm24" aria-hidden="true" focusable="false" ', 1)
    w16 = WORDMARK_16.replace('<svg ', '<svg class="wm16" aria-hidden="true" focusable="false" ', 1)
    w24 = re.sub(r'<title>.*?</title>', '', w24)
    w16 = re.sub(r'<title>.*?</title>', '', w16)
    return f'<a class="wm" href="#overview" data-red="signature" aria-label="Oath &amp; Action, systems atlas overview">{w24}{w16}</a>'


def masthead():
    tabs = ''.join(f'<a href="#{v}" data-tab="{v}">{e(TAB_NAMES[v])}</a>' for v in VIEWS)
    return (f'<header class="mast"><div class="wrap">{wordmark()}'
            f'<p class="runhead eyebrow">{e(D["meta"]["title"])} · Night Edition</p>'
            f'<nav class="tabs" aria-label="Views">{tabs}</nav></div></header>'
            f'<div class="wrap crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>'
            f'<p class="status" data-ak-status role="status"></p></div>')


def footer():
    c = COUNTS
    src = (f'{e(D["meta"]["title"])} Systems Atlas V7, snapshot {SNAP}. {cnt("variables", c["variables"])} variables, '
           f'{cnt("connections", c["connections"])} connections, {cnt("loops", c["loops"])} loops, {cnt("reforms", c["reforms"])} reforms.')
    return (f'<footer class="foot"><div class="wrap"><p>{src}</p>'
            f'<p>Editorial system 04, Night Edition. Studio draft, November 5, 2026.</p></div></footer>')


def panel_html():
    return ('<aside class="ak-panel" data-ak-panel hidden aria-labelledby="ak-panel-title">'
            '<div class="ak-panel-bar"><p data-ak-panel-kind></p>'
            '<button class="ak-btn" type="button" data-ak-sheet-toggle aria-expanded="false">More</button>'
            '<button class="ak-btn" type="button" data-ak-close>Close</button></div>'
            '<h2 id="ak-panel-title" data-ak-panel-title tabindex="-1"></h2><div data-ak-panel-body></div></aside>')


def templates_html():
    """One JSON block: the kit's detail hook builds a panel when the reader opens one (red team S2: page weight)."""
    blob = json.dumps({k: [asof(kind), asof(title), body] for k, (kind, title, body) in TEMPLATES.items()}, ensure_ascii=False, separators=(',', ':'))
    return f'<script type="application/json" id="panels">{blob.replace("</", "<\\/")}</script>'


PAGE_JS = r'''
(function(){
  // #area-a and the other part keys open that part in the overview's reading panel (the memo's hash grammar)
  function alias(){ var m = location.hash.match(/^#area-(a|b|d|e|x|ec|tc)(\/.*)?$/i);
    if (m) history.replaceState(history.state, '', '#overview/part-' + m[1].toLowerCase()); }
  alias(); addEventListener('hashchange', alias);
  var panels = {}; try { panels = JSON.parse(document.getElementById('panels').textContent); } catch (err) {}
  AtlasKit.init({ detail: function (key) { var d = panels[key]; if (!d) return null;
    var t = document.createElement('template'); t.dataset.kind = d[0]; t.dataset.title = d[1]; t.innerHTML = d[2]; return t; } });
  var view = function(){ return document.querySelector('[data-view-root]:not([hidden])'); };
  // the skip link focuses the view's heading and keeps the view's hash
  document.querySelector('[data-skip]').addEventListener('click', function(ev){ ev.preventDefault();
    var h = view() && view().querySelector('[data-ak-heading]'); if (h) { h.setAttribute('tabindex', '-1'); h.focus(); } });
  // in-page jumps keep the view's hash
  document.addEventListener('click', function(ev){ var a = ev.target.closest('[data-jump]'); if (!a) return; ev.preventDefault();
    var h = document.getElementById(a.dataset.jump); if (h) { h.setAttribute('tabindex', '-1'); h.scrollIntoView({ block: 'start' }); h.focus({ preventScroll: true }); } });
  // a drawing that takes focus says how to move inside it
  var HINT = 'Arrow keys move between items. Enter opens one.';
  document.addEventListener('focusin', function(ev){ var d = ev.target.closest && ev.target.closest('[data-ak-roving]'); if (!d) return;
    if (ev.relatedTarget && d.contains(ev.relatedTarget)) return;
    var v = view(); if (!v) return; v.querySelectorAll('[data-ak-readout]').forEach(function(r){ r.textContent = HINT + ' ' + r.textContent; }); });
  // the panel never hides what the reader picked
  window.atlasReveal = function(item){ if (!item) return; requestAnimationFrame(function(){ requestAnimationFrame(function(){
    if (innerWidth < 900) { var r = item.getBoundingClientRect(), band = innerHeight * 0.52 - 12;
      if (r.top < 8 || r.bottom > band) window.scrollBy(0, r.top - Math.max(16, (band - Math.min(r.height, band)) / 2)); }
    else { var box = item.getBoundingClientRect(), right = innerWidth - (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--ak-panel-w')) || 420);
      if (box.right > right || box.left < 0 || box.top < 0 || box.bottom > innerHeight) item.scrollIntoView({ block: 'nearest', inline: 'center' }); } }); }); };
})();
'''


TAB_JS = r'''
(function(){
  function mark(){var v=(location.hash.slice(1).split('/')[0]||'overview').toLowerCase();
    var known=[].slice.call(document.querySelectorAll('[data-view-root]')).map(function(r){return r.dataset.viewRoot});
    var cur=known.indexOf(v)>=0?v:(document.querySelector('[data-view-root]:not([hidden])')||{dataset:{}}).dataset.viewRoot;
    document.querySelectorAll('[data-tab]').forEach(function(a){if(a.dataset.tab===cur)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});}
  addEventListener('hashchange',function(){setTimeout(mark,0)}); mark(); setTimeout(mark,50);
})();
'''


def page(views_html):
    kit_js = KIT_JS
    # A view may hold two artboards of one drawing (wide and narrow), and a list may repeat an item drawn above: select
    # the copy the reader used, else the first copy the reader can see.
    kit_js = kit_js.replace("const root = rootOf(S.view), item = key && $(`[data-select=\"${key}\"]`, root);",
                            "const root = rootOf(S.view), mine = S.invoker && S.invoker.dataset && S.invoker.dataset.select === key && vis(S.invoker) && root && root.contains(S.invoker) ? S.invoker : null, item = key && (mine || $$(`[data-select=\"${key}\"]`, root || document).find(vis) || $(`[data-select=\"${key}\"]`, root));")
    assert 'find(vis)' in kit_js
    # The panel never hides what the reader picked: after it opens, bring the item into view (beside the column on a
    # desktop, above the sheet on a phone).
    kit_js = kit_js.replace("if (o.focus) { p.scrollTop = 0; $('[data-ak-panel-title]', p).focus(); }",
                            "if (o.focus) { p.scrollTop = 0; $('[data-ak-panel-title]', p).focus({ preventScroll: true }); } if (window.atlasReveal) window.atlasReveal(item);")
    assert 'atlasReveal' in kit_js
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&amp;family=Inter:wght@400;500;600;700;800&amp;'
             'family=Lora:ital,wght@1,400&amp;display=swap" rel="stylesheet">')
    return ('<!doctype html><html lang="en" data-surface="charcoal"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<meta name="atlas-views" content="{" ".join(VIEWS)}">'
            '<meta name="description" content="Editorial atlas system 04, Night Edition: the Oath &amp; Action systems atlas on Charcoal.">'
            f'<title>{e(D["meta"]["title"])} Night Edition</title>{fonts}'
            f'<style>{KIT_CSS}{CSS}{EXTRA_CSS}</style></head>'
            f'<body data-surface="charcoal"><a class="skip" href="#main" data-skip>Skip to the view</a>{masthead()}'
            f'<main id="main" class="ak-stage">{views_html}</main>{panel_html()}{footer()}{templates_html()}'
            f'<script>{kit_js}</script><script>{TAB_JS}{PAGE_JS}</script></body></html>')


EXTRA_CSS = r'''
.lgroup{margin-top:56px}
.lg-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;padding-top:14px;margin-bottom:24px;border-top:2px solid var(--ink)}
.key{background:var(--ground);border:1px solid var(--stone);padding:18px 20px 20px;border-top:2px solid var(--ink)}
.key .eyebrow{margin-bottom:10px}
.keyl{list-style:none;display:grid;gap:8px;margin-bottom:12px}
.keyl li{display:grid;grid-template-columns:72px 1fr;gap:12px;align-items:start;font:500 13px/18px var(--f-ui);color:var(--dim)}
.keyl li b{color:var(--ink);font-weight:600}
.keyl svg{margin-top:-3px}
'''


# --------------------------------------------------------------------------------------- view: overview
BW = 1312                     # the board at 1440 px: 12 columns, 64 px margins
CWS = {'A': 220, 'B': 228, 'C': 220, 'D': 280, 'E': 180}   # Checks holds seven variables; Policy holds two
CG = 46                       # gutters that carry the circuit
CX, _x = {}, 0
for _p in CORE:
    CX[_p] = _x
    _x += CWS[_p] + CG
PAD = 16
CIRCUIT = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]
BACKFLOW = [('C', 'B'), ('D', 'C'), ('E', 'D')]
EC_X = (CX['A'] + 24, CX['C'] + CWS['C'])
TC_X = (CX['D'], CX['E'] + CWS['E'] - 24)
X_COLS = (210, 236)           # outside forces: name block and story widths


def part_story(pid):
    return first_sentence(PARTS[pid]['story'])


def flows_out(pid):
    return [(b, between(pid, b)) for b in PART_ORDER if b != pid and between(pid, b)]


def flows_in(pid):
    return [(a, between(a, pid)) for a in PART_ORDER if a != pid and between(a, pid)]


def nlines(text, width, size, weight, tight=False):
    return len(wrap(text, width - 3, size, weight, tight))


def vars_height(nodes, width):
    """.pc-vars: 15/18 Inter 600 labels, 4 px apart."""
    return sum(18 * nlines(lab(n), width, 15, 600) for n in nodes) + 4 * (len(nodes) - 1)


def core_card_height(pid):
    """Mirrors the .pc rules: border 2, padding 16, name 30, formal 4+18, question 10+22n, story 6+20n,
    variables 12+1+10+list, padding 16."""
    P_ = PARTS[pid]
    w = CWS[pid] - 2 * PAD
    h = 2 + 16 + 26 + 22
    h += 10 + 22 * nlines(P_['plain_question'], w, 17, 600)
    h += 6 + 20 * nlines(part_story(pid), w, 15, 500)
    h += 23 + vars_height(P_['nodes'], w)
    return h + 16


def layer_metrics(pid):
    P_ = PARTS[pid]
    w = (EC_X[1] - EC_X[0]) if pid == 'EC' else (TC_X[1] - TC_X[0])
    inner = w - 2 * PAD
    left = 210
    right = inner - left - 24 - 32
    hl = 26 + 4 + 18 * nlines(P_['formal_title'], left, 13, 500)
    hr = 22 * nlines(P_['plain_question'], right, 17, 600) + 6 + 20 * nlines(part_story(pid), right, 15, 500)
    head = max(hl, hr)
    if P_.get('groups'):
        cw = (inner - 2 * 20) / 3
        body = max(18 * nlines(g['title'], cw, 13, 600) + 6 + vars_height(g['nodes'], cw) for g in P_['groups'])
    else:
        cw = (inner - 20) / 2
        half = (len(P_['nodes']) + 1) // 2
        body = max(vars_height(P_['nodes'][:half], cw), vars_height(P_['nodes'][half:], cw))
    return 2 + 16 + head + 14 + 1 + 12 + body + 16


def x_height():
    w = BW - 2 * PAD
    story = 20 * nlines(part_story('X'), X_COLS[1], 15, 500)
    return 2 + 16 + max(26 + 22, story) + 16


def var_button(n, cls='vbtn'):
    say = f"{n} {lab(n)}. {NODES[n]['increase_means']}"
    return (f'<button type="button" class="{cls}" data-select="var-{n.lower()}" data-node="{n}" data-name="{e(lab(n))}" '
            f'data-say="{e(say)}">{e(lab(n))}</button>')


def flow_words(pid):
    """For the stacked form, where the arrows give way to words: every part this one sends to and hears from."""
    outs = ', '.join(f'{part_name(b)} {len(ks)}' for b, ks in flows_out(pid))
    ins = ', '.join(f'{part_name(a)} {len(ks)}' for a, ks in flows_in(pid))
    s = ''
    if outs:
        s += f'<li><b>Passes on to</b> {e(outs)}</li>'
    if ins:
        s += f'<li><b>Pushed on by</b> {e(ins)}</li>'
    return f'<ul class="pc-flows" aria-label="Connections to other parts, counted">{s}</ul>'


def part_name_control(pid):
    P_ = PARTS[pid]
    if pid == 'C':
        return (f'<a class="pc-name" href="#area-c" aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. Opens the full part.">'
                f'{e(P_["plain_name"])}</a>')
    return (f'<button type="button" class="pc-name tbtn" data-select="part-{pid.lower()}" '
            f'data-say="{e(P_["plain_name"])}, {e(P_["formal_title"])}. Opens the part in the reading panel.">{e(P_["plain_name"])}</button>')


def part_card(pid, x, y, w, h, layout='core'):
    P_ = PARTS[pid]
    q = f'<p class="pc-q">{e(P_["plain_question"])}</p>' if P_['plain_question'] else ''
    badge = '' if pid == 'X' else f'<span class="pc-badge" aria-hidden="true">{pid}</span>'
    name = f'<h3 class="pc-nh">{part_name_control(pid)}</h3><p class="pc-formal">{e(P_["formal_title"])}</p>'
    story = f'<p class="pc-story">{e(part_story(pid))}</p>'
    if layout == 'layer':
        if P_.get('groups'):
            cols = ''.join(f'<div class="pc-group"><p class="pc-gt">{e(g["title"])}</p><ul class="pc-vars">'
                           + ''.join(f'<li>{var_button(n)}</li>' for n in g['nodes']) + '</ul></div>' for g in P_['groups'])
            vars_ = f'<div class="pc-cols pc-cols-3">{cols}</div>'
        else:
            half = (len(P_['nodes']) + 1) // 2
            vars_ = ('<div class="pc-cols pc-cols-2">' + ''.join('<ul class="pc-vars">' + ''.join(f'<li>{var_button(n)}</li>' for n in grp) + '</ul>'
                                                                for grp in (P_['nodes'][:half], P_['nodes'][half:])) + '</div>')
        inner = f'<div class="pc-hrow"><div class="pc-hl">{name}</div><div class="pc-hr">{q}{story}</div></div><div class="pc-body">{vars_}</div>'
    elif layout == 'strip':
        vars_ = '<ul class="pc-vars pc-row">' + ''.join(f'<li>{var_button(n)}</li>' for n in P_['nodes']) + '</ul>'
        inner = f'<div class="pc-hl">{name}</div>{story}{vars_}'
    else:
        vars_ = '<ul class="pc-vars">' + ''.join(f'<li>{var_button(n)}</li>' for n in P_['nodes']) + '</ul>'
        inner = f'{name}{q}{story}{vars_}'
    style = f'left:{fnum(x)}px;top:{fnum(y)}px;width:{fnum(w)}px;height:{fnum(h)}px'
    return (f'<div class="pc pc-{layout}" data-part="{pid}" data-name="{e(P_["plain_name"])}" style="{style}">'
            f'{badge}{inner}{flow_words(pid)}</div>')


def flow_item(a, b, pts, w, cls, label_svg, end='head'):
    ks = between(a, b)
    auth = all(LINKS[k]['type'] == 'authority' for k in ks)
    marks, d, L = wire(pts, w, 'well-supported', None, end='diamond' if auth else end, authority=auth)
    say = f"{part_name(a)} to {part_name(b)}: {len(ks)} connection{'s' if len(ks) != 1 else ''}{', each says who decides' if auth else ''}. Opens the list."
    return (f'<g class="flow {cls}" data-select="flow-{a.lower()}-{b.lower()}" data-rel="part-{a.lower()} part-{b.lower()}" '
            f'role="button" aria-label="{e(say)}" data-say="{e(say)}">{marks}{label_svg}</g>')


def count_text(x, y, n, cls, anchor='middle', extra_word=''):
    t = f'<text x="{fnum(x)}" y="{fnum(y)}" class="{cls}" text-anchor="{anchor}" data-count="custom:flow">{n}</text>'
    if extra_word:
        t += svg_text(x + (tw(str(n), 15, 600) / 2 + 6 if anchor == 'middle' else tw(str(n), 15, 600) + 6), y, extra_word, 'cw', 'start')
    return t


def board():
    CH = max(core_card_height(p) for p in CORE)
    XH = x_height()
    LAYH = max(layer_metrics('EC'), layer_metrics('TC'))
    Y_X = 30
    Y_CORE = Y_X + XH + 44
    CHAN = 64
    Y_LAY = Y_CORE + CH + CHAN
    Y_RET = Y_LAY + LAYH + 22
    H = Y_RET + 34
    cards = part_card('X', 0, Y_X, BW, XH, 'strip')
    for pid in CORE:
        cards += part_card(pid, CX[pid], Y_CORE, CWS[pid], CH)
    cards += part_card('EC', EC_X[0], Y_LAY, EC_X[1] - EC_X[0], LAYH, 'layer')
    cards += part_card('TC', TC_X[0], Y_LAY, TC_X[1] - TC_X[0], LAYH, 'layer')
    s = ''
    right = lambda p: CX[p] + CWS[p]
    # the two questions over the parts that answer them (the dark atlas's question tags)
    segs = [('eco', CX['A'], right('A')), ('dem', CX['B'], right('D')), ('both', CX['E'], right('E'))]
    for k, x0, x1 in segs:
        txt = Q[k]['q'] if k != 'both' else 'Both questions meet'
        s += f'<path class="qb" d="M{fnum(x0)} 0.5H{fnum(x1)}"/>'
        s += svg_text(x0, 19, txt, 'qbt', 'start')
    # outside forces push in
    y0, y1 = Y_X + XH + 2, Y_CORE - 2
    for pid in CORE:
        ks = between('X', pid)
        if ks:
            x = CX[pid] + 44
            s += flow_item('X', pid, [(x, y0), (x, y1)], 2, 'ctx', count_text(x + 10, (y0 + y1) / 2 + 5, len(ks), 'cn', 'start'))
    # the circuit: forward on the upper track, back on the lower
    yf = Y_CORE + 128
    yb = yf + 52
    for a_, b_ in CIRCUIT:
        x0, x1 = right(a_) + 2, CX[b_] - 2
        s += flow_item(a_, b_, [(x0, yf), (x1, yf)], 2, 'main', count_text((x0 + x1) / 2, yf - 12, len(between(a_, b_)), 'cm'))
    for a_, b_ in BACKFLOW:
        x0, x1 = CX[a_] - 2, right(b_) + 2
        s += flow_item(a_, b_, [(x0, yb), (x1, yb)], 2, 'ctx', count_text((x0 + x1) / 2, yb + 24, len(between(a_, b_)), 'cn'))
    # the return line, round the bottom and back into Wealth
    xr0, xr1 = right('E') - 12, CX['A'] + 12
    ret = [(xr0, Y_CORE + CH + 2), (xr0, Y_RET), (xr1, Y_RET), (xr1, Y_CORE + CH + 2)]
    lbl = (count_text(EC_X[0] + 20, Y_RET + 27, len(between('E', 'A')), 'cm', 'start')
           + svg_text(EC_X[0] + 44, Y_RET + 25, 'The return line: ' + lower_first(D['opening']['return']), 'rl'))
    s += flow_item('E', 'A', ret, 2, 'main ret', lbl)
    # the household and technology layers
    ya0, ya1 = Y_CORE + CH + 2, Y_LAY - 2
    xa1, xa2 = CX['A'] + 76, CX['A'] + 136
    ym = (ya0 + ya1) / 2 + 5
    s += flow_item('EC', 'A', [(xa1, ya1), (xa1, ya0)], 2, 'ctx', count_text(xa1 + 10, ym, len(between('EC', 'A')), 'cn', 'start'))
    s += flow_item('A', 'EC', [(xa2, ya0), (xa2, ya1)], 2, 'ctx', count_text(xa2 + 10, ym, len(between('A', 'EC')), 'cn', 'start'))
    xd1 = CX['D'] + 186
    s += flow_item('D', 'TC', [(xd1, ya0), (xd1, ya1)], 2, 'ctx', count_text(xd1 + 10, ym, len(between('D', 'TC')), 'cn', 'start', 'decide'))
    xd0, xe = CX['D'] + 34, EC_X[1] - 34
    yel = Y_CORE + CH + CHAN / 2
    s += flow_item('D', 'EC', [(xd0, ya0), (xd0, yel), (xe, yel), (xe, ya1)], 2, 'ctx',
                   count_text(xe + 12, yel - 9, len(between('D', 'EC')), 'cn', 'start', 'decide'))
    yl = Y_LAY + 64
    s += flow_item('TC', 'EC', [(TC_X[0] - 2, yl), (EC_X[1] + 2, yl)], 2, 'ctx', count_text((TC_X[0] + EC_X[1]) / 2, yl - 12, len(between('TC', 'EC')), 'cn'))
    drawn = {('X', p) for p in CORE} | set(CIRCUIT) | set(BACKFLOW) | {('E', 'A'), ('EC', 'A'), ('A', 'EC'), ('D', 'TC'), ('D', 'EC'), ('TC', 'EC')}
    svg = (f'<svg class="bd" data-view="overview-board" viewBox="0 0 {BW} {fnum(H)}" width="{BW}" height="{fnum(H)}" '
           f'aria-label="Flows between the parts, bundled and counted">{s}</svg>')
    return cards, svg, H, drawn


def not_drawn(drawn):
    rest = []
    for a in PART_ORDER:
        for b in PART_ORDER:
            if a != b and (a, b) not in drawn and between(a, b):
                rest.append((a, b, len(between(a, b))))
    rest.sort(key=lambda t: (-t[2], PART_ORDER.index(t[0])))
    return rest


# --------------------------------------------------------------------------------------- the system at a glance
def best_link(ks):
    """One connection to name a bundle by: the best graded, then the first in V7's order."""
    return sorted(ks, key=lambda k: (-RANK[LINKS[k]['evidence']], list(LINKS).index(k)))[0]


def glance_box(pid, x, y, w, h, name_size=22, q_size=15, inner_w=None, interactive=True, extra=None):
    P_ = PARTS[pid]
    q = P_['plain_question'] or part_story(pid)
    rows = wrap(q, (inner_w or w) - 28, q_size, 500)
    out = f'<rect class="gbx" x="{fnum(x)}" y="{fnum(y)}" width="{fnum(w)}" height="{fnum(h)}"/>'
    out += svg_text(x + 14, y + 30, P_['plain_name'], 'gn')
    out += svg_lines(x + 14, y + 52, rows, 'gq', 19)
    if extra:
        out += svg_lines(x + 14, y + 52 + 19 * len(rows) + 4, extra, 'gx', 19)
    say = f"{P_['plain_name']}, {P_['formal_title']}. {q}"
    if not interactive:
        return f'<g class="gp" data-part="{pid}">{out}</g>'
    if pid == 'C':
        return (f'<a class="gp" href="#area-c" data-part="{pid}" aria-label="{e(say)} Opens the full part." data-say="{e(say)}">{out}</a>')
    return (f'<g class="gp" data-select="part-{pid.lower()}" data-part="{pid}" role="button" aria-label="{e(say)} Opens the part in the reading panel." '
            f'data-say="{e(say)}">{out}</g>')


def glance_wide():
    """Desktop: the eight parts in the board's own columns, named with their questions, the circuit and its counts."""
    right = lambda p_: CX[p_] + CWS[p_]
    XH, YR, YC = 38, 74, 96
    CHh = max(16 + 26 + 19 * len(wrap(PARTS[p_]['plain_question'], CWS[p_] - 28, 15, 500)) + 14 for p_ in CORE)
    YCH = YC + CHh
    YL = YCH + 58
    LH = 58
    H = YL + LH
    xs = sum(len(ks) for _, ks in flows_out('X'))
    s = f'<rect class="gbx gbx-x" x="0" y="0" width="{BW}" height="{XH}"/>'
    s += svg_text(14, 25, PARTS['X']['plain_name'], 'gxn')
    s += svg_text(14 + tw(PARTS['X']['plain_name'], 17, 700) + 12, 25, f'push on every part: {xs} connections. {part_story("X")}', 'gq')
    # the return line over the core row
    xr0, xr1 = right('E') - 28, CX['A'] + 28
    m, _, _ = wire([(xr0, YC - 2), (xr0, YR), (xr1, YR), (xr1, YC - 2)], 2, 'well-supported', None)
    rk = between('E', 'A')
    lbl = f'{len(rk)} back to Wealth, the return line: {lower_first(D["opening"]["return"])}'
    s += f'<g class="flow main">{m}</g>'
    s += f'<text x="{fnum((xr0 + xr1) / 2)}" y="{YR - 9}" class="gq halo" text-anchor="middle">{e(lbl)}</text>'
    for pid in CORE:
        s += glance_box(pid, CX[pid], YC, CWS[pid], CHh)
    for a_, b_ in CIRCUIT:
        x0, x1 = right(a_) + 2, CX[b_] - 2
        y = YC + 34
        m, _, _ = wire([(x0, y), (x1, y)], 2, 'well-supported', None)
        s += f'<g class="flow main">{m}<text x="{fnum((x0 + x1) / 2)}" y="{y - 10}" class="cm" text-anchor="middle">{len(between(a_, b_))}</text></g>'
    # the layers beneath
    for pid, (x0, x1) in (('EC', EC_X), ('TC', TC_X)):
        P_ = PARTS[pid]
        s += (f'<g class="gp" data-select="part-{pid.lower()}" data-part="{pid}" role="button" '
              f'aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. {e(P_["plain_question"])} Opens the part in the reading panel." '
              f'data-say="{e(P_["plain_name"])}. {e(P_["plain_question"])}">'
              f'<rect class="gbx" x="{fnum(x0)}" y="{fnum(YL)}" width="{fnum(x1 - x0)}" height="{LH}"/>'
              + svg_text(x0 + 14, YL + 25, P_['plain_name'], 'gn')
              + svg_text(x0 + 14, YL + 46, P_['plain_question'], 'gq') + '</g>')
    ya0, ya1 = YCH + 2, YL - 2
    pairs = [(('EC', 'A'), CX['A'] + 76, True), (('A', 'EC'), CX['A'] + 136, False), (('D', 'TC'), CX['D'] + 186, False)]
    for (a_, b_), x, up in pairs:
        ks = between(a_, b_)
        auth = all(LINKS[k]['type'] == 'authority' for k in ks)
        pts = [(x, ya1), (x, ya0)] if up else [(x, ya0), (x, ya1)]
        m, _, _ = wire(pts, 2, 'well-supported', None, end='diamond' if auth else 'head', authority=auth)
        word = ' decide' if auth else ''
        s += f'<g class="flow ctx">{m}<text x="{x + 10}" y="{(ya0 + ya1) / 2 + 5}" class="cn">{len(ks)}{word}</text></g>'
    yl = YL + LH / 2
    m, _, _ = wire([(TC_X[0] - 2, yl), (EC_X[1] + 2, yl)], 2, 'well-supported', None)
    s += f'<g class="flow ctx">{m}<text x="{fnum((TC_X[0] + EC_X[1]) / 2)}" y="{yl - 10}" class="cn" text-anchor="middle">{len(between("TC", "EC"))}</text></g>'
    return (f'<svg class="gl-wide" data-view="overview-glance" viewBox="0 0 {BW} {fnum(H)}" width="{BW}" height="{fnum(H)}" role="group" '
            f'data-ak-roving data-ak-nav="spatial" aria-labelledby="h-glance">{s}</svg>')


def glance_narrow():
    """Phone: the circuit top to bottom, drawn for 320 px with text at 15 px or more, so it holds at 320."""
    W, BXW = 320, 262
    y = 0
    s = ''
    xs = sum(len(ks) for _, ks in flows_out('X'))
    rows = wrap(f'{PARTS["X"]["plain_name"]} push on every part: {xs} connections.', W - 24, 15, 500)
    s += f'<rect class="gbx gbx-x" x="0" y="0" width="{W}" height="{14 + 19 * len(rows) + 6}"/>'
    s += svg_lines(12, 24, rows, 'gq', 19)
    y = 14 + 19 * len(rows) + 6 + 24
    tops = {}
    for i, pid in enumerate(CORE):
        q = wrap(PARTS[pid]['plain_question'], BXW - 28, 15, 500)
        h = 16 + 26 + 19 * len(q) + 12
        s += glance_box(pid, 0, y, BXW, h)
        tops[pid] = (y, h)
        y += h
        if i < len(CORE) - 1:
            a_, b_ = CORE[i], CORE[i + 1]
            m, _, _ = wire([(36, y + 2), (36, y + 36)], 2, 'well-supported', None)
            n = len(between(a_, b_))
            s += f'<g class="flow main">{m}<text x="52" y="{y + 24}" class="gq">{n} connection{"s" if n != 1 else ""} to {e(part_name(b_))}</text></g>'
            y += 38
    ya, ha = tops['A']
    ye, he = tops['E']
    m, _, _ = wire([(BXW + 2, ye + he / 2), (W - 22, ye + he / 2), (W - 22, ya + ha / 2), (BXW + 2, ya + ha / 2)], 2, 'well-supported', None)
    s += f'<g class="flow main">{m}</g>'
    y += 10
    rk = between('E', 'A')
    ret = wrap(f'The return line: {len(rk)} connections back to Wealth. {D["opening"]["return"]}', W - 12, 15, 500)
    s += svg_lines(0, y + 15, ret, 'gq', 19)
    y += 19 * len(ret) + 22
    for pid in ('EC', 'TC'):
        P_ = PARTS[pid]
        outs = ', '.join(f'{part_name(b)} {len(ks)}' for b, ks in flows_out(pid))
        ins = ', '.join(f'{part_name(a)} {len(ks)}' for a, ks in flows_in(pid))
        extra = wrap(f'To {outs}. From {ins}.', W - 28, 15, 500)
        q = wrap(P_['plain_question'], W - 28, 15, 500)
        h = 16 + 26 + 19 * len(q) + 4 + 19 * len(extra) + 12
        s += glance_box(pid, 0, y, W, h, extra=extra)
        y += h + 14
    H = y - 14
    return (f'<svg class="gl-narrow" data-view="overview-glance-phone" viewBox="0 0 {W} {fnum(H)}" width="{W}" height="{fnum(H)}" role="group" '
            f'data-ak-roving data-ak-nav="spatial" aria-label="The system at a glance, top to bottom">{s}</svg>')


def map_story(form):
    """The circuit told with the names of its connections, each with its grade, so no step claims more than its
    evidence. Phones read top to bottom."""
    g = lambda k: f'{LINKS[k]["name"]} ({grade_word(LINKS[k]["evidence"]).lower()})'
    lead = 'Read the map from left to right.' if form == 'wide' else 'Read the parts from top to bottom.'
    back = 'Along the bottom, the return line closes the circle:' if form == 'wide' else 'After Policy, the return line leads back to Wealth:'
    return (f'{lead} {g("L01")}, and {lower_first(g("L02"))}. In safe seats, {lower_first(g("L25"))}, '
            f'and {lower_first(g("L51"))}. {back} {lower_first(g("L03"))}.')


def circuit_words():
    cols = ''
    for pid in CORE:
        b = 'A' if pid == 'E' else CORE[CORE.index(pid) + 1]
        ks = between(pid, b)
        k = best_link(ks)
        l = LINKS[k]
        lead = 'The return line to Wealth' if pid == 'E' else f'To {part_name(b)}'
        cols += (f'<li><p class="cw-h"><b>{lead}: {len(ks)}</b></p><p class="cw-t">such as {e(lower_first(l["name"]))} '
                 f'<span class="dim">({grade_word(l["evidence"]).lower()}, {k})</span></p></li>')
    return f'<ul class="cwords" aria-label="The main circuit in words">{cols}</ul>'


def view_overview():
    cards, svg, H, drawn = board()
    rest = not_drawn(drawn)
    n_rest = sum(t[2] for t in rest)
    rest_words = '; '.join(f'{part_name(a)} to {part_name(b)}, {n}' for a, b, n in rest)
    qcards = ''.join(f'<div class="qcard"><p class="eyebrow">{e(Q[k]["short"])}</p><h2>{e(Q[k]["q"])}</h2><p>{e(Q[k]["text"])}</p></div>'
                     for k in ('dem', 'eco'))
    qtexts = ''.join(f'<div class="qt"><p class="eyebrow">{e(Q[k]["short"])}</p><p>{e(Q[k]["text"])}</p></div>' for k in ('dem', 'eco'))
    l03, l01 = LINKS['L03'], LINKS['L01']
    finding = (f'<p class="finding"><b>One finding, from two well-supported connections:</b> {e(l03["name"].lower())}, and '
               f'{e(lower_first(l01["name"]))}.</p>')
    head = (f'<header class="vhead ov-head"><div class="vhead-main">'
            f'<p class="eyebrow">{e(D["opening"]["kicker"])}</p>'
            f'<h1 class="display" id="h-overview" data-ak-heading><span class="q1">{e(Q["dem"]["q"])}</span> <span class="q2">{e(Q["eco"]["q"])}</span></h1>'
            f'<p class="deck">An atlas of {cnt("variables", COUNTS["variables"])} conditions in eight parts, from household wealth to court rulings, '
            f'traced through {cnt("connections", COUNTS["connections"])} connections, one graded connection at a time. '
            f'{cnt("loops", COUNTS["loops"])} loops and {cnt("reforms", COUNTS["reforms"])} reforms sit on the map.</p>{finding}</div>'
            f'<div class="vhead-side qtexts">{qtexts}</div></header>')
    glance_sec = (f'<section class="glance" aria-labelledby="h-glance"><div class="gl-head"><h2 id="h-glance" class="phead">The system at a glance</h2>'
                  f'<p class="caption dim">Eight parts, each with its question. The light arrows run the main circuit; '
                  f'each number counts the connections it bundles. Choose a part to read it, or see every variable on the map below.</p></div>'
                  f'{glance_wide()}{glance_narrow()}<p class="ak-readout caption dim" data-ak-readout>Choose a part to read it.</p>'
                  f'<div class="qtexts-phone">{qtexts}</div></section>')
    howto = (f'<div class="howto"><p><b>How to read the map.</b> Each card is one part, with every variable in it. '
             f'Each arrow bundles the connections from one part to another, and its number counts them. '
             f'The bright route is the main circuit. Choose any name or arrow for the detail.</p>'
             f'<a class="more" href="#how-to-read">How to read the lines</a></div>')
    board_html = (f'<div class="boardwrap"><div class="board" data-ak-roving data-ak-nav="spatial" style="height:{fnum(H)}px" '
                  f'role="group" aria-labelledby="h-system">{svg}{cards}</div></div>')
    sys_sec = (f'<section class="sec sys" aria-labelledby="h-system"><div class="sys-head"><h2 id="h-system">The full map</h2>'
               f'<p class="sys-story"><span class="st-wide">{e(map_story("wide"))}</span><span class="st-phone">{e(map_story("phone"))}</span></p>'
               f'{howto}</div>{board_html}'
               f'{circuit_words()}<p class="caption dim board-note">Not drawn, to keep the map calm: {cnt("custom:not-drawn", n_rest)} smaller connections between parts '
               f'({e(rest_words)}). Each part\'s reading panel lists them. Of the {cnt("connections", len(LINKS))} connections, '
               f'{cnt("custom:between-parts", N_BETWEEN)} run between parts and {cnt("custom:inside-parts", N_INSIDE)} stay inside one.</p></section>')
    # start from your own bill
    hubs = ''
    for h in HUBS:
        qs = IC['story']['hubQ'].get(h['id'], [])
        tags = ''.join(f'<li>{e(Q[q]["q"])}</li>' for q in qs)
        items = ''.join(f'<li><button type="button" class="hq" data-select="pw-{pid.lower()}" '
                        f'data-say="{e(PATHWAYS[pid]["question"])} Opens the short answer.">{e(PATHWAYS[pid]["question"])}</button></li>'
                        for pid in h['pathways'])
        hubs += (f'<article class="hub"><p class="eyebrow">{e(h["title"])}</p><h3>{e(h["question"])}</h3>'
                 f'<ul class="hub-tags" aria-label="Answers">{tags}</ul><ul class="hub-qs">{items}</ul></article>')
    bill = (f'<section class="sec" aria-labelledby="h-bill"><div class="sec-head"><h2 id="h-bill">Start from your own bill</h2>'
            f'<p>{len(PATHWAYS)} everyday questions in {len(HUBS)} topics. Each one follows a bill or a worry to the people who decide '
            f'and to the parts of the map it touches.</p></div>'
            f'<div class="hubs">{hubs}</div></section>')
    # loops
    feat = ['R8', 'R10', 'B4']
    feat_cards = ''.join(loop_card(k, 'overview') for k in feat)
    idx = ''
    for pid, ls in loop_groups():
        title = PARTS[pid]['plain_name'] if pid != 'SK' else 'Sketched'
        idx += (f'<div class="li-col"><p class="eyebrow">{e(title)}</p><ul>'
                + ''.join(f'<li><a href="{loop_href(k)}">{e(LOOPS[k]["plain_name"])}</a> <span class="dim">{k}</span></li>' for k in ls)
                + '</ul></div>')
    loops_sec = (f'<section class="sec" aria-labelledby="h-loops-ov"><div class="sec-head"><h2 id="h-loops-ov">Where a reform can interrupt a loop</h2>'
                 f'<p>{e(D["opening"]["paras"][2])} Three to start with: a two-step loop, the safe-seat loop, and a loop that pushes back.</p></div>'
                 f'<div class="lgrid">{feat_cards}</div>'
                 f'<div class="lindex"><div><p class="li-head"><span><b>Every loop</b>, by the part it lives in.</span> <a class="more" href="#loops">All {len(LOOPS)} loops, drawn</a></p>'
                 f'<div class="li-cols">{idx}</div></div><div>{key_small()}</div></div></section>')
    return (f'<section data-view-root="overview" data-crumb="Overview" aria-labelledby="h-overview"><div class="wrap">'
            f'{head}{glance_sec}{sys_sec}{bill}{loops_sec}</div></section>')


EXTRA_CSS += r'''
/* overview */
.qcards .qcard:first-child{margin-top:4px}
.sec.sys{margin-top:48px}
.sys-head{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px;row-gap:10px;margin-bottom:28px;align-items:start}
.sys-head h2{grid-column:1/span 3;font:800 40px/44px var(--f-disp);letter-spacing:-.03em;text-wrap:balance}
.sys-story{grid-column:4/span 6;font:500 15px/23px var(--f-ui);color:var(--ink)}
.st-phone{display:none}
@media (max-width:899.98px){.st-wide{display:none}.st-phone{display:inline}}
.howto{grid-column:10/span 3;font:500 15px/23px var(--f-ui);color:var(--dim)}
.howto b{color:var(--ink);font-weight:600}
.howto .more{margin-top:8px}
.boardwrap{position:relative}
.board{position:relative;width:1312px}
.board svg.bd{position:absolute;left:0;top:0;overflow:visible;pointer-events:none}
.board .flow{pointer-events:auto;cursor:pointer}
.flow.main{color:var(--ink)}
.flow.ctx{color:var(--stone)}
.flow .hd{fill:var(--ak-hi,currentColor)}
.cm{font:800 22px/1 var(--f-disp);fill:var(--ink);font-variant-numeric:tabular-nums}
.cn{font:600 15px var(--f-ui);fill:var(--dim);font-variant-numeric:tabular-nums}
.cw{font:500 13px var(--f-ui);fill:var(--dim)}
.rl{font:500 15px var(--f-ui);fill:var(--ink)}
.qb{stroke:var(--dim);stroke-width:1px;fill:none}
.qbt{font:600 13px var(--f-ui);fill:var(--dim);letter-spacing:.01em}
.flow:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.flow[data-ak-sel] .cn,.flow.ak-rel .cn{fill:var(--ink)}
.pc{position:absolute;background:var(--ground);padding:16px;display:flex;flex-direction:column;border:1px solid var(--stone);border-top:2px solid var(--ink)}
.pc-badge{position:absolute;top:16px;right:16px;min-width:22px;height:22px;padding:0 5px;border:1.5px solid var(--dim);color:var(--dim);font:700 13px/19px var(--f-ui);text-align:center}
.pc-nh{line-height:26px;padding-right:30px}
.pc-strip .pc-nh,.pc-layer .pc-nh{padding-right:0}
.pc-name{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;color:var(--ink);text-decoration:underline;text-decoration-color:var(--stone);text-decoration-thickness:2px;text-underline-offset:6px}
.pc-name:hover{text-decoration-color:var(--ink)}
.pc-name[data-ak-sel]{text-decoration-color:var(--ak-hi,var(--ink))}
.pc-formal{font:500 13px/18px var(--f-ui);color:var(--dim);margin-top:4px}
.pc-q{font:600 17px/22px var(--f-ui);margin-top:10px;color:var(--ink)}
.pc-story{font:500 15px/20px var(--f-ui);color:var(--dim);margin-top:6px}
.pc-vars{list-style:none;margin-top:12px;padding-top:10px;border-top:1px solid var(--stone);display:grid;gap:4px}
.vbtn{appearance:none;background:none;border:0;padding:0;margin:0;text-align:left;cursor:pointer;font:600 15px/18px var(--f-ui);color:var(--ink);display:block;width:100%}
.vbtn:hover{text-decoration:underline;text-underline-offset:3px}
.vbtn[data-ak-sel]{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px;text-decoration-color:var(--ak-hi,var(--ink))}
.vbtn.ak-rel:not([data-ak-sel]){text-decoration:underline;text-decoration-color:var(--dim);text-underline-offset:3px}
.pc-strip{flex-direction:row;align-items:flex-start;gap:24px}
.pc-strip .pc-hl{width:210px;flex:none}
.pc-strip .pc-story{width:236px;flex:none;margin-top:0}
.pc-strip .pc-row{flex:1;margin:0;padding:0 40px 0 0;border:0;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);gap:16px}
.pc-row li{border-left:1px solid var(--stone);padding-left:12px;min-height:44px}
.pc-layer .pc-hrow{display:flex;gap:24px}
.pc-layer .pc-hl{width:210px;flex:none}
.pc-layer .pc-hr{flex:1;padding-right:32px}
.pc-layer .pc-hr .pc-q{margin-top:0}
.pc-layer .pc-body{margin-top:14px;padding-top:12px;border-top:1px solid var(--stone)}
.pc-layer .pc-vars{margin:0;padding:0;border:0}
.pc-cols{display:grid;gap:20px}
.pc-cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.pc-cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}
.pc-gt{font:600 13px/18px var(--f-ui);color:var(--dim);margin-bottom:6px}
.pc-flows{display:none;list-style:none;font:500 13px/18px var(--f-ui);color:var(--dim);margin-top:12px;padding-top:10px;border-top:1px solid var(--stone)}
.pc-flows b{color:var(--ink);font-weight:600}
.board-note{margin-top:20px;max-width:120ch}
.hubs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px}
.hub{border-top:2px solid var(--ink);padding-top:14px}
.hub h3{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;margin:6px 0 10px;text-wrap:balance}
.hub-tags{list-style:none;display:flex;flex-direction:column;gap:2px;margin-bottom:12px;font:500 13px/18px var(--f-ui);color:var(--dim)}
.hub-qs{list-style:none;display:grid}
.hub-qs li{border-top:1px solid var(--stone)}
.hq{appearance:none;background:none;border:0;width:100%;text-align:left;padding:10px 22px 10px 0;cursor:pointer;font:600 15px/21px var(--f-ui);color:var(--ink);position:relative}
.hq::after{content:"\2192";position:absolute;right:2px;top:10px;color:var(--dim)}
.hq:hover{text-decoration:underline;text-underline-offset:3px}
.hq[data-ak-sel]{box-shadow:inset 3px 0 0 var(--ak-hi,var(--ink));padding-left:10px}
.lindex{margin-top:56px;border-top:1px solid var(--stone);padding-top:16px}
.li-head{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap;margin-bottom:16px}
.li-cols{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px}
.li-col ul{list-style:none;margin-top:8px;display:grid;gap:4px;font:500 15px/22px var(--f-ui)}
.li-col a{text-decoration-color:var(--stone)}
.li-col .dim{font-size:13px}
@media (max-width:1339.98px){
 .board{width:auto;height:auto!important;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
 .board svg.bd{display:none}
 .pc{position:relative;width:auto!important;height:auto!important;left:auto!important;top:auto!important}
 .pc-strip,.pc-layer{grid-column:1/-1}
 .pc-flows{display:block}
 .hubs{grid-template-columns:repeat(3,minmax(0,1fr))}
 .li-cols{grid-template-columns:repeat(3,minmax(0,1fr))}
 .sys-head h2{grid-column:1/-1}.sys-story{grid-column:1/span 7}.howto{grid-column:8/span 5}
}
@media (max-width:899.98px){
 .board{grid-template-columns:1fr}
 .pc-strip,.pc-layer .pc-hrow{flex-direction:column;gap:6px}
 .pc-strip .pc-hl,.pc-layer .pc-hl,.pc-strip .pc-story{width:auto}
 .pc-strip .pc-story{margin-top:6px}
 .pc-layer .pc-hr{padding-right:0}
 .pc-layer .pc-hr .pc-q{margin-top:10px}
 .pc-strip .pc-row{grid-auto-flow:row;padding:10px 0 0;margin-top:12px;border-top:1px solid var(--stone);gap:4px}
 .pc-row li{border-left:0;padding-left:0;min-height:0}
 .pc-cols-3,.pc-cols-2{grid-template-columns:1fr;gap:12px}
 .pc-vars{gap:0}
 .vbtn{padding:6px 0;min-height:32px}
 .hq{padding-top:12px;padding-bottom:12px}
 .sys-head{display:block}.sys-head h2{font-size:26px;line-height:30px}.sys-story,.howto{margin-top:12px}
 .hubs{grid-template-columns:1fr}
 .li-cols{grid-template-columns:1fr 1fr}
 .vhead-side.qcards{margin-top:28px}
}
'''


# --------------------------------------------------------------------------------------- reading-panel templates
def pick(key, text):
    return f'<button type="button" class="pick" data-ak-pick="{key}">{e(text)}</button>'


def conn_li(k, show_ends=True):
    l = LINKS[k]
    g = l['evidence']
    sign = f" {sign_char(l['polarity'])}" if l['polarity'] in ('+', '-') else ''
    ends = f"{lab(l['from'])} <b>{verb(l['polarity'])}{sign}</b> {e(lower_first(lab(l['to'])))}. " if show_ends else ''
    return (f'<li>{chip("Connection", k)}<b>{e(l["name"])}</b><br><span class="dim">{ends}'
            f'{grade_word(g)}: {grade_gloss(g)}. {DELAY[l["delay"]].capitalize()}.</span></li>')


def effects_dl(rid):
    R = REFORMS[rid]
    rows = ''.join(f'<dt>{e(D["families"][f])}</dt><dd>{e(D["effect_codes"].get(c, c))}</dd>' for f, c in R['effects'].items())
    return f'<dl>{rows}</dl><p class="dim">Each family is rated on its own and never added together. Confidence: {e(R["effects_confidence"])}.</p>'


def routes_list(rid):
    out = ''
    for r in REFORMS[rid]['routes']:
        chk = f'checked {date_words(r["checked"])}' if r.get('checked') else 'no check date in V7'
        note = f' {e(r["note"])}' if r.get('note') else ''
        out += (f'<li><b>{e(D["route_names"].get(r["route"], r["route"]))}</b>: {e(r["who"])}. Feasibility {e(r["feasibility"])}, {chk}.'
                f'<span class="dim">{note}</span></li>')
    return f'<ul>{out}</ul>'


MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def date_words(iso):
    y, m, d = iso.split('-')
    return f'{MONTHS[int(m) - 1]} {int(d)}, {y}'


def target_words(t):
    if t in NODES:
        return f'{t} {lab(t)}'
    return f'{t} {LINKS[t]["name"]}'


V7 = json.loads((ROOT / 'work/extract/atlas-v7-data.json').read_text())
V7_PW = {p_['id']: p_ for p_ in V7['pathways']}


def figures(t):
    """Numbers in a sentence, without years."""
    out = set()
    for m in re.finditer(r'\$?\d[\d,]*(?:\.\d+)?', t):
        x = m.group(0).replace('$', '').replace(',', '').rstrip('.')
        if not re.fullmatch(r'(19|20)\d\d', x):
            out.add(x)
    return out


def words(t):
    return {w for w in re.findall(r'[a-z]{4,}', t.lower())}


def sourced_answer(pid, text):
    """Each sentence that prints a figure is followed by the source of the V7 claim that carries that figure: matched by
    the figures they share, ties broken by shared words. A figure no claim carries says so."""
    ids = V7_PW[pid]['claim_ids']
    out = ''
    for sent_ in re.split(r'(?<=[.!?])\s+(?=[A-Z])', text):
        out += f'<p class="lead">{e(sent_)}</p>'
        n = figures(sent_)
        if not n:
            continue
        scored = []
        for cid in ids:
            c = V7['claims'][cid]
            blob = c['claim'] + ' ' + (c.get('supports') or '')
            k = len(n & figures(blob))
            if k:
                scored.append((k, len(words(sent_) & words(blob)), cid))
        if not scored:
            out += '<p class="srcnote">V7 ties no source to this figure.</p>'
            continue
        scored.sort(key=lambda x: (-x[0], -x[1]))
        cid = scored[0][2]
        refs = []
        for sid in V7['claims'][cid]['sources']:
            S = V7['sources'][sid]
            refs.append(f'{S["title"]}, {S.get("publisher") or ""}, {str(S.get("year") or "")[:4]}'.replace(', ,', ','))
        out += f'<p class="srcnote">Source: {e("; ".join(refs))}.</p>'
    return out


def build_templates():
    # parts
    for pid in PART_ORDER:
        P_ = PARTS[pid]
        vs = ''.join(f'<li>{pick("var-" + n.lower(), lab(n))}<br><span class="dim">{e(NODES[n]["increase_means"])}</span></li>' for n in P_['nodes'])
        outs = ''.join(f'<li>{e(part_name(b))}: {len(ks)}</li>' for b, ks in flows_out(pid))
        ins = ''.join(f'<li>{e(part_name(a))}: {len(ks)}</li>' for a, ks in flows_in(pid))
        lh = loops_home(pid)
        loops_ = ''.join(f'<li><a href="{loop_href(k)}">{e(LOOPS[k]["plain_name"])}</a> <span class="dim">{k}, {e(LOOPS[k]["kind_gloss"])}</span></li>' for k in lh)
        rf = reforms_aimed(pid)
        iss = issues_in(pid)
        qs = ' and '.join(f'“{Q[q]["q"]}”' for q in PART_Q.get(pid, []))
        body = (f'<p class="dim">{e(P_["formal_title"])}{" · " + e(P_["plain_question"]) if P_["plain_question"] else ""}</p>'
                f'<p class="lead">{e(P_["story"])}</p>'
                + (f'<p class="dim">Answers {e(qs)}</p>' if qs else '') +
                f'<h3>Its {len(P_["nodes"])} variables</h3><ul class="plain">{vs}</ul>'
                f'<h3>Connections</h3><p>{len(inside(pid))} inside the part.</p>'
                + (f'<p><b>Passes on to</b></p><ul>{outs}</ul>' if outs else '')
                + (f'<p><b>Pushed on by</b></p><ul>{ins}</ul>' if ins else '')
                + (f'<h3>Loops that live here</h3><ul>{loops_}</ul>' if lh else '<h3>Loops</h3><p>No loop lives here.</p>')
                + f'<h3>Reforms and issues</h3><p>{len(rf)} reforms aim at a variable here or a connection that touches one. '
                  f'{len(iss)} issues in V7 name a variable here.</p>'
                + (f'<p><a class="more" href="#area-c">Open {e(P_["plain_name"])}, the full part</a></p>' if pid == 'C' else '')
                + f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'part-{pid.lower()}', f'Part {pid}', P_['plain_name'], body)
    # variables
    for n, N in NODES.items():
        outs = ''.join(conn_li(k) for k in LINKS if LINKS[k]['from'] == n)
        ins = ''.join(conn_li(k) for k in LINKS if LINKS[k]['to'] == n)
        loops_ = ''.join(f'<li><a href="{loop_href(k)}">{e(LOOPS[k]["plain_name"])}</a> <span class="dim">{k}</span></li>' for k in N['loops'])
        rf = [r for r in sorted(REFORMS) if n in REFORMS[r]['targets']]
        rfs = ''.join(f'<li>{chip("Reform", r)}{e(REFORMS[r]["title"])}</li>' for r in rf)
        iss = [k for k, i in ISSUES.items() if n in (i.get('nodes') or []) and not i.get('retired')]
        body = (f'<p class="dim">{e(N["title"])} · {e(part_name(N["part"]))}, {e(PARTS[N["part"]]["formal_title"])}</p>'
                f'<p class="lead">{e(N["description"])}</p><p><b>{e(N["increase_means"])}</b></p>'
                + (f'<p class="dim">{e(N["why"])}</p>' if N.get('why') else '')
                + f'<dl><dt>Kind</dt><dd>{e(N["kind_plain"])}</dd>' + (f'<dt>Measured by</dt><dd>{e(N["indicator"])}</dd>' if N.get('indicator') else '') + '</dl>'
                + (f'<h3>Pushes on</h3><ul class="conns">{outs}</ul>' if outs else '')
                + (f'<h3>Pushed on by</h3><ul class="conns">{ins}</ul>' if ins else '')
                + (f'<h3>Loops</h3><ul>{loops_}</ul>' if loops_ else '<h3>Loops</h3><p>No loop runs through it.</p>')
                + (f'<h3>Reforms aimed here</h3><ul>{rfs}</ul>' if rfs else '')
                + f'<h3>Issues</h3><p>{len(iss)} issues in V7 name this variable.</p>'
                + f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'var-{n.lower()}', f'Variable {n}', lab(n), body)
    # connections
    for k, l in LINKS.items():
        g = l['evidence']
        loops_ = ''.join(f'<li><a href="{loop_href(x)}">{e(LOOPS[x]["plain_name"])}</a> <span class="dim">{x}</span></li>' for x in l['loops'])
        body = (f'<p class="lead">{e(l["plain"])}</p>'
                f'<dl><dt>From</dt><dd>{n_ref(l["from"])}</dd><dt>To</dt><dd>{n_ref(l["to"])}</dd>'
                f'<dt>Sign</dt><dd>{e(sign_words(l["polarity"]))}</dd><dt>Reads</dt><dd>{e(link_sentence(k))}</dd>'
                f'<dt>Kind</dt><dd>{e(l["type"].capitalize())}</dd><dt>Delay</dt><dd>{e(DELAY[l["delay"]])}</dd>'
                f'<dt>Evidence</dt><dd>{grade_word(g)}: {grade_gloss(g)}</dd></dl>'
                + (f'<p class="dim">{e(l["sign_meaning"])}</p>' if l.get('sign_meaning') else '')
                + (f'<h3>How it works</h3><p>{e(sent(l["mechanism"]))}</p>' if l.get('mechanism') else '')
                + (f'<h3>Keep in mind</h3><p>{e(l["qualification"])}</p>' if l.get('qualification') else '')
                + (f'<h3>Loops</h3><ul>{loops_}</ul>' if loops_ else '')
                + f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'link-{k.lower()}', f'Connection {k}', l['name'], body)
    # bundled flows on the overview
    for a in PART_ORDER:
        for b in PART_ORDER:
            ks = between(a, b)
            if a != b and ks:
                body = (f'<p class="lead">{len(ks)} connection{"s" if len(ks) != 1 else ""} run from {e(part_name(a))} to {e(part_name(b))}. '
                        f'The map draws them as one arrow; here they are one by one.</p><ul class="conns">{"".join(conn_li(k) for k in ks)}</ul>'
                        f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
                tpl(f'flow-{a.lower()}-{b.lower()}', 'Flow between parts', f'{part_name(a)} to {part_name(b)}', body)
    # everyday questions
    for pid, pw in PATHWAYS.items():
        refs = pw['model_refs']
        parts_ = []
        for n in refs.get('nodes', []):
            if PART_OF[n] not in parts_:
                parts_.append(PART_OF[n])
        vs = ', '.join(lab(n) for n in refs.get('nodes', []))
        loops_ = ''.join(f'<li><a href="{loop_href(x)}">{e(LOOPS[x]["plain_name"])}</a> <span class="dim">{x}</span></li>' for x in refs.get('loops', []))
        rfs = ''.join(f'<li>{chip("Reform", r)}{e(REFORMS[r]["title"])}</li>' for r in refs.get('reforms', []))
        hub = next(h for h in HUBS if pid in h['pathways'])
        body = (f'<p class="dim">{e(hub["title"])} · {e(pw["title"])}</p>{sourced_answer(pid, pw["short_answer"])}'
                + (f'<h3>Where it sits on the map</h3><p>{", ".join(e(part_name(x)) for x in parts_)}. Variables: {e(vs)}.</p>' if parts_ else '')
                + ('<p><a class="more" href="#area-c">Open Elections</a></p>' if 'C' in parts_ else '')
                + (f'<h3>Loops</h3><ul>{loops_}</ul>' if loops_ else '')
                + (f'<h3>Reforms</h3><ul>{rfs}</ul>' if rfs else '')
                + f'<p class="dim">{len(refs.get("issues", []))} issues in V7 sit on this path.</p>'
                + f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'pw-{pid.lower()}', 'Everyday question', pw['question'], body)
    # loops
    for lid, L in LOOPS.items():
        steps = ''
        for s_ in L['steps']:
            if s_.get('id'):
                steps += conn_li(s_['id'])
            else:
                steps += f'<li>{e(s_["from_label"])} <b>{verb(s_["polarity"])}</b> {e(lower_first(s_["to_label"]))}. <span class="dim">Sketched step, no numbered connection.</span></li>'
        rfs = ''.join(f'<li>{chip("Reform", r)}{e(REFORMS[r]["title"])}</li>' for r in L['reforms'])
        disc = disclosure(lid)
        body = (f'<p class="dim">{e(kind_line(lid))} · {e(L["title"])}</p><p class="lead">{e(L["summary"])}</p>'
                f'<h3>Read it aloud</h3><p>{e(read_aloud(lid))}</p>'
                f'<h3>Steps</h3><ol class="conns">{steps}</ol>'
                f'<h3>Evidence</h3><p>{e(weakest_words(lid))}. {e(L["evidence_summary"])}</p>'
                + (f'<p><b>{e(disc)}</b></p>' if disc else '')
                + f'<dl><dt>Now</dt><dd>{e(DIRECTION.get(L["direction"], L["direction"]))}. {e(L["reference_mode"])}</dd>'
                  f'<dt>One turn</dt><dd>{e(L["delay_word"])}</dd></dl>'
                + (f'<h3>Keep in mind</h3><p>{e(L["qualification"])}</p>' if L.get('qualification') else '')
                + (f'<h3>Reforms aimed at it</h3><ul>{rfs}</ul>' if rfs else '<h3>Reforms</h3><p>No reform aims at this loop yet.</p>')
                + ('<p><a class="more" href="#loop-r10">Open the full loop</a></p>' if lid == 'R10' else '')
                + f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'loop-{lid.lower()}', f'Loop {lid}', L['plain_name'], body)
    # reforms
    for rid, R in REFORMS.items():
        tg = ''.join(f'<li>{e(target_words(t))}</li>' for t in R['targets'])
        lp = ''.join(f'<li><a href="{loop_href(x)}">{e(LOOPS[x]["plain_name"])}</a> <span class="dim">{x}</span></li>' for x in R['loops'])
        body = (f'<p class="dim">Band: {e(R["band"])}</p><p class="lead">{e(R["summary"])}</p>'
                f'<h3>What it changes</h3><p>{e(R["what_it_changes"])}</p>'
                f'<h3>Where it acts</h3><ul>{tg}</ul>'
                + (f'<h3>Loops it sits on</h3><ul>{lp}</ul>' if lp else '')
                + f'<h3>Likely effects</h3>{effects_dl(rid)}'
                f'<h3>Who could adopt it</h3>{routes_list(rid)}'
                f'<h3>Evidence</h3><dl><dt>Problem</dt><dd>{grade_word(R["problem_evidence"]["grade"])}</dd>'
                f'<dt>Remedy</dt><dd>{grade_word(R["remedy_evidence"]["grade"])}</dd></dl>'
                f'<h3>Status</h3><p>{e(R["status"]["text"])}</p>'
                + (f'<p><b>Disclosure.</b> {e(R["disclosure"])}</p>' if R.get('disclosure') else '')
                + ('<p><a class="more" href="#reform-r01">Open the full reform</a></p>' if rid == 'R-01' else '')
                + f'<p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'reform-{rid.lower()}', f'Reform {rid}', R['title'], body)
    # issues
    for iid, I in ISSUES.items():
        if I.get('retired'):
            continue
        pe, fe = I.get('problem_example') or {}, I.get('fix_example') or {}
        def example(x, kind):
            if not x or not x.get('headline'):
                return ''
            src = x.get('source') or {}
            s_ = f'<h3>{kind}</h3><p><b>{e(x["headline"])}</b></p><p>{e(x.get("text") or "")}</p>'
            if x.get('result'):
                s_ += f'<p><b>Result.</b> {e(x["result"])}</p>'
            where = ', '.join(v for v in [x.get('where'), x.get('when')] if v)
            srcline = sent(f'Source: {src.get("title", "")}, {src.get("publisher", "")}, {src.get("year", "")}')
            s_ += f'<p class="dim">{e(sent(where))} {e(srcline)}</p>'
            return s_
        rf = ''.join(f'<li>{chip("Reform", r["id"])}{e(REFORMS[r["id"]]["title"])}<br><span class="dim">{e(r["why"])}</span>'
                     + (f'<br><span><b>Disclosure.</b> {e(REFORMS[r["id"]]["disclosure"])}</span>' if REFORMS[r['id']].get('disclosure') else '')
                     + '</li>' for r in I['aimed_reforms'])
        vs = ', '.join(f'{n} {lab(n)}' for n in I.get('nodes') or [])
        body = (f'<p class="dim">{e(DOMAINS[I["domain"]]["title"])}{" · " + e(I["subsystem"]) if I.get("subsystem") else ""} · '
                f'{grade_word(I["grade"])}: {grade_gloss(I["grade"])}</p>'
                f'<p class="lead">{e(I["summary"])}</p><h3>How it happens</h3><p>{e(I["mechanism"])}</p>'
                + example(pe, 'Where it shows up') + example(fe, 'Where a fix was tried')
                + f'<h3>A response</h3><p>{e(I["response"])}</p><dl><dt>Who acts</dt><dd>{e(I["actor"])}</dd>'
                  f'<dt>Tradeoff</dt><dd>{e(I["tradeoff"])}</dd><dt>Success</dt><dd>{e(I["success_measure"])}</dd></dl>'
                + (f'<h3>Reforms aimed at it</h3><ul>{rf}</ul>' if rf else '<h3>Reforms</h3><p>No reform in V7 aims at it yet.</p>')
                + f'<h3>Variables</h3><p>{e(vs)}</p><p class="src">Atlas V7, snapshot {SNAP}.</p>')
        tpl(f'issue-{iid.lower()}', f'Issue {iid}', I['title'], body)


def n_ref(n):
    return f'{n} {e(lab(n))} <span class="dim">({e(part_name(PART_OF[n]))})</span>'


EXTRA_CSS += r'''
.ak-panel .chip{height:20px;margin-right:6px;vertical-align:1px}
.ak-panel .chip b,.ak-panel .chip span{font-size:13px}
.ak-panel ul.plain{list-style:none;padding:0}
.ak-panel ul.conns{list-style:none;padding:0}
.ak-panel ul.conns li{padding:8px 0;border-top:1px solid var(--stone)}
.ak-panel ol.conns{padding-left:20px}
.ak-panel ol.conns li{padding:6px 0}
.ak-panel .src{margin-top:24px;font:500 13px/18px var(--f-ui);color:var(--dim)}
.ak-panel .srcnote{margin-top:4px;font:500 13px/18px var(--f-ui);color:var(--dim)}
.ak-panel .lead+.lead{margin-top:10px}
.ak-panel .more{font-size:15px}
.ak-panel-bar{gap:8px}
'''


# --------------------------------------------------------------------------------------- big drawings (close-ups)
BIG_TILE = 300
C5_X = 1072                   # Incumbents defeated sits right of the square on the Elections page


def big_tile_rows(n, w):
    lab_rows = wrap(lab(n), w - 76 - 16, 20, 700, True)
    im_rows = wrap(NODES[n]['increase_means'], w - 32, 15, 500)
    return lab_rows, im_rows


def extra_rows(extras, w, ph):
    rows = []
    for t, cls in extras:
        for r in wrap(t, w - 32, 15 if ph else 13, 600):
            rows.append((r, cls))
    return rows


def big_tile_height(n, w, extras, ph=False):
    lr, ir = big_tile_rows(n, w)
    top = 16 + max(48, 18 + 22 * len(lr))
    xr = extra_rows(extras, w, ph)
    return top + 14 + 20 * len(ir) + (10 + (20 if ph else 18) * len(xr) if xr else 0) + 16


def big_tile(n, x, y, w, h, extras, rel, interactive=True, state=None, ph=False):
    lr, ir = big_tile_rows(n, w)
    sfx = ' ph' if ph else ''
    out = f'<rect class="ak-mark bx" x="{fnum(x)}" y="{fnum(y)}" width="{fnum(w)}" height="{fnum(h)}"/>'
    out += icon(n, 48, x + 16, y + 16)
    out += svg_text(x + 76, y + 30, n, 'cd' + sfx)
    out += svg_lines(x + 76, y + 30 + 22, lr, 'sl', 22, extra=f' data-node="{n}" data-name="{e(lab(n))}"')
    ty = y + 16 + max(48, 18 + 22 * len(lr)) + 14 + 13
    out += svg_lines(x + 16, ty, ir, 'im', 20)
    ey = ty + 20 * (len(ir) - 1) + 10 + 18
    for t, cls in extra_rows(extras, w, ph):
        out += svg_text(x + 16, ey, t, cls + sfx)
        ey += 20 if ph else 18
    if state:
        for at, word in state:
            out += f'<text x="{fnum(x + w - 16)}" y="{fnum(y + 30)}" class="stw{sfx}" text-anchor="end" data-ak-at="{at}" hidden>{e(word)}</text>'
    say = f"{n} {lab(n)}. {NODES[n]['increase_means']}"
    if interactive:
        return (f'<g class="st big" data-select="var-{n.lower()}" data-node="{n}" data-rel="{rel}" role="button" '
                f'aria-label="{e(say)}" data-say="{e(say)}">{out}</g>')
    return f'<g class="st big" data-node="{n}">{out}</g>'


def step_label_lines(k, num, extras, ph=False):
    """Name first, then the verb with its sign, then the grade and delay; extras last. Phone artboards set all at 15 px."""
    l = LINKS[k]
    g = l['evidence']
    small = 15 if ph else 13
    sfx = ' ph' if ph else ''
    sign = f' {sign_char(l["polarity"])}' if l['polarity'] in ('+', '-') else ''
    return ([(f'{num}  {l["name"]}' if num else l['name'], 'sn', 15, 600),
             (f'{verb(l["polarity"]).capitalize()}{sign}', 'sv' + sfx, small, 600),
             (f'{grade_word(g)}: {grade_gloss(g)} · {DELAY[l["delay"]]}', 'sd' + sfx, small, 500)] + [(t, c + sfx, small, 600) for t, c in extras])


def label_block(lines, x, y, width, anchor='start', valign='top'):
    """Wrap each line to the width, stack them; y is the first baseline (top) or the last baseline (bottom)."""
    rows = []
    for t, cls, size, wt in lines:
        for r in wrap(t, width, size, wt):
            rows.append((r, cls, 20 if size >= 15 else 17))
    total = sum(h for _, _, h in rows)
    if valign == 'bottom':
        y = y - total + rows[-1][2]
    elif valign == 'middle':
        y = y - total / 2 + 13
    out, yy = '', y
    for r, cls, h in rows:
        out += svg_text(x, yy, r, cls, anchor)
        yy += h
    return out, total


def big_step(k, pts, interactive, label_svg, tag_at=0.5, cls=''):
    l = LINKS[k]
    marks, d, L = wire(pts, 3, l['evidence'], l['polarity'], l['delay'], tag_at=tag_at)
    attrs = (f'data-link="{k}" data-sign="{sign_attr(l["polarity"])}" data-grade="{l["evidence"]}" data-delay="{l["delay"]}" '
             f'data-from="{l["from"]}" data-to="{l["to"]}"')
    say = (f"{k}: {l['name']}. {link_sentence(k)}. {grade_word(l['evidence'])}, {grade_gloss(l['evidence'])}. "
           f"{DELAY[l['delay']].capitalize()}.")
    if interactive:
        return (f'<g class="sp big{cls}" data-select="link-{k.lower()}" {attrs} data-rel="var-{l["from"].lower()} var-{l["to"].lower()}" '
                f'role="button" aria-label="{e(say)}" data-say="{e(say)}">{marks}{label_svg}</g>')
    return f'<g class="sp big{cls}" {attrs}>{marks}{label_svg}</g>'


def reform_notes_for(target, lid='R10'):
    return [r for r in LOOPS[lid]['reforms'] if target in REFORMS[r]['targets']]


def tile_notes(n, lid, notes):
    if notes == 'loops':
        return [('On loops ' + ', '.join(NODES[n]['loops']), 'rn')]
    rs = reform_notes_for(n, lid) if n in [x['code'] for x in LOOPS[lid]['stations']] else []
    if notes == 'r01':
        rs = [r for r in rs if r == 'R-01']
    return [(f'{r} aims here', 'rn') for r in rs]


def step_notes(k, lid, notes):
    if notes == 'loops':
        return []
    rs = reform_notes_for(k, lid)
    if notes == 'r01':
        rs = [r for r in rs if r == 'R-01']
    return [(f'{r} acts on this step', 'rn') for r in rs]


def square_drawing(lid, view, interactive=True, b4=False, stepper=True, notes='reforms'):
    """A four-station loop at full size: stations at the corners, steps along the sides, every step named, with its
    verb, grade and delay in words, the weakest step and each reform marked where it acts. With b4, the Elections page
    adds the accountability loop B4, which shares C3: C3 to C5 to D5 and back to C3."""
    L = LOOPS[lid]
    st = [s['code'] for s in L['stations']]
    steps = [s['id'] for s in L['steps']]
    weak = weakest_of(lid)
    W, TW = 880, BIG_TILE
    GAPY = 196
    extra = ['C5', 'D5'] if b4 else []
    extras = {n: tile_notes(n, lid, notes) for n in st + extra}
    TH = max([big_tile_height(n, TW, extras[n]) for n in st] + [big_tile_height(n, 1312 - C5_X, extras[n]) for n in extra])
    pos = {st[0]: (0, 0), st[1]: (W - TW, 0), st[2]: (W - TW, TH + GAPY), st[3]: (0, TH + GAPY)}
    G3 = 170
    if b4:
        pos['C5'] = (C5_X, TH + GAPY)
        pos['D5'] = (860, 2 * TH + GAPY + G3)
    out = ''
    def state_for(i):
        s_, seq = 1, []
        for j in range(4):
            seq.append(s_)
            s_ *= 1 if L['steps'][j]['polarity'] == '+' else -1
        if i == 0:
            return [(4, 'back to ' + ('more' if s_ > 0 else 'less'))]
        return [(i, 'more' if seq[i] > 0 else 'less')]
    rels = {n: ' '.join(f'link-{k.lower()}' for k in steps if n in (LINKS[k]['from'], LINKS[k]['to'])) for n in st}
    step_svgs = []
    yt, yb_ = 64, TH + GAPY + 64
    xl, xr = TW / 2, W - TW / 2
    for i, k in enumerate(steps):
        ex = ([('Weakest step', 'wkb')] if k in weak else []) + step_notes(k, lid, notes)
        lines = step_label_lines(k, i + 1 if notes != 'loops' else None, ex)
        if i == 0:      # top, left to right
            pts = [(TW + 2, yt), (W - TW - 2, yt)]
            name_svg, _ = label_block(lines[:1], W / 2, yt - 18, W - 2 * TW - 40, 'middle', 'bottom')
            rest_svg, _ = label_block(lines[1:], W / 2, yt + 34, W - 2 * TW - 40, 'middle')
            lab_svg = name_svg + rest_svg
        elif i == 2:    # bottom, right to left
            pts = [(W - TW - 2, yb_), (TW + 2, yb_)]
            name_svg, _ = label_block(lines[:1], W / 2, yb_ - 18, W - 2 * TW - 40, 'middle', 'bottom')
            rest_svg, _ = label_block(lines[1:], W / 2, yb_ + 34, W - 2 * TW - 40, 'middle')
            lab_svg = name_svg + rest_svg
        elif i == 1:    # right side, down
            pts = [(xr, TH + 2), (xr, TH + GAPY - 2)]
            lab_svg, _ = label_block(lines, xr - 22, TH + GAPY / 2, 250, 'end', 'middle')
        else:           # left side, up
            pts = [(xl, TH + GAPY - 2), (xl, TH + 2)]
            lab_svg, _ = label_block(lines, xl + 22, TH + GAPY / 2, 250, 'start', 'middle')
        step_svgs.append(big_step(k, pts, interactive, lab_svg))
    for i, n in enumerate(st):     # document order follows the loop: station, its step, the next station
        x, y = pos[n]
        out += big_tile(n, x, y, TW, TH, extras[n], rels[n], interactive, state_for(i) if stepper else None) + step_svgs[i]
    H = 2 * TH + GAPY
    if b4:
        # B4 in document order from C3: L24 to C5, L54 to D5, L23 back to C3
        y = yb_
        lines = step_label_lines('L24', None, [])
        out += big_step('L24', [(W + 2, y), (C5_X - 2, y)], interactive,
                        label_block(lines[:1], (W + C5_X) / 2, y - 18, C5_X - W - 24, 'middle', 'bottom')[0]
                        + label_block(lines[1:], (W + C5_X) / 2, y + 34, C5_X - W - 16, 'middle')[0])
        cx, cy = pos['C5']
        out += big_tile('C5', cx, cy, 1312 - C5_X, TH, extras['C5'], 'link-l24 link-l54', interactive)
        dx, dy = pos['D5']
        ym = dy + TH / 2
        x54 = C5_X + (1312 - C5_X) / 2 + 40
        lab54, _ = label_block(step_label_lines('L54', None, []), x54 - 22, (cy + TH + dy) / 2, 210, 'end', 'middle')
        out += big_step('L54', [(x54, cy + TH + 2), (x54, ym), (dx + TW + 2, ym)], interactive, lab54, tag_at=0.3)
        out += big_tile('D5', dx, dy, TW, TH, extras['D5'], 'link-l54 link-l23', interactive)
        c3x = W - TW / 2
        lab23, _ = label_block(step_label_lines('L23', None, []), c3x - 22, (cy + TH + dy) / 2, 250, 'end', 'middle')
        out += big_step('L23', [(dx - 2, ym), (c3x, ym), (c3x, cy + TH + 2)], interactive, lab23, tag_at=0.75)
        B = LOOPS['B4']
        note = [(f'B4, the {B["plain_name"].lower()}, {B["kind_gloss"]}.', 'sn', 15, 600),
                (first_sentence(B['qualification']), 'im', 15, 500),
                (f'R10, the {L["plain_name"].lower()}, can feed itself; its weakest step is plausible.', 'sn', 15, 600)]
        out += label_block(note, 0, dy + 24, 520)[0]
        H = dy + TH
    Wt = 1312 if b4 else W
    role = 'role="group" data-ak-roving data-ak-nav="sequence" data-ak-wrap' if interactive else 'role="img"'
    return (f'<svg class="dr dr-wide" data-view="{view}" data-loop="{lid}" data-steps="{" ".join(steps)}" viewBox="0 0 {Wt} {fnum(H)}" '
            f'width="{Wt}" height="{fnum(H)}" {role} aria-label="{e(L["plain_name"] + ", drawn at full size. " + read_aloud(lid))}">{out}</svg>')


def chain_drawing(lid, view, interactive=True, stepper=True, notes='reforms'):
    """The same loop for a phone, drawn for 320 px with every label at 15 px or more: stations top to bottom, the
    return up the right side and in from the top."""
    L = LOOPS[lid]
    st = [s['code'] for s in L['stations']]
    steps = [s['id'] for s in L['steps']]
    weak = weakest_of(lid)
    W, TW = 320, 270
    extras = {n: tile_notes(n, lid, notes) for n in st}
    TH = max(big_tile_height(n, TW, extras[n], ph=True) for n in st)
    labs = []
    for i, k in enumerate(steps):
        ex = ([('Weakest step', 'wkb')] if k in weak else []) + step_notes(k, lid, notes)
        labs.append(step_label_lines(k, i + 1 if notes != 'loops' else None, ex, ph=True))
    fwd_h = [label_block(labs[i], 0, 0, TW - 70)[1] for i in range(len(steps) - 1)]
    G = max(150, max(fwd_h) + 36)
    xe = TW - 40
    ret_h = label_block(labs[-1], 0, 0, xe - 26 - 4)[1]
    TOP = ret_h + 46
    ys = [TOP + i * (TH + G) for i in range(len(st))]
    out = ''
    rels = {n: ' '.join(f'link-{k.lower()}' for k in steps if n in (LINKS[k]['from'], LINKS[k]['to'])) for n in st}
    chain_steps = []
    for i, k in enumerate(steps):
        if i < len(steps) - 1:
            x = 40
            pts = [(x, ys[i] + TH + 2), (x, ys[i + 1] - 2)]
            lab_svg, _ = label_block(labs[i], x + 26, ys[i] + TH + G / 2, TW - 70, 'start', 'middle')
        else:
            xr = TW + 30
            pts = [(TW + 2, ys[-1] + TH / 2), (xr, ys[-1] + TH / 2), (xr, 12), (xe, 12), (xe, TOP - 2)]
            lab_svg, _ = label_block(labs[i], xe - 26, 36, xe - 26 - 4, 'end')
        chain_steps.append(big_step(k, pts, interactive, lab_svg, tag_at=0.5 if i < len(steps) - 1 else 0.92))
    for i, n in enumerate(st):
        out += big_tile(n, 0, ys[i], TW, TH, extras[n], rels[n], interactive, ph=True) + chain_steps[i]
    H = ys[-1] + TH
    role = 'role="group" data-ak-roving data-ak-nav="sequence" data-ak-wrap' if interactive else 'role="img"'
    return (f'<svg class="dr dr-narrow" data-view="{view}" data-loop="{lid}" data-steps="{" ".join(steps)}" viewBox="0 0 {W} {fnum(H)}" '
            f'width="{W}" height="{fnum(H)}" {role} aria-label="{e(L["plain_name"] + ", drawn top to bottom. " + read_aloud(lid))}">{out}</svg>')


EXTRA_CSS += r'''
.dr{display:block;max-width:100%;height:auto;overflow:visible}
.dr-narrow{display:none}
.dr .bx{fill:var(--panel)}
.st.big{color:var(--dim)}
.cd{font:700 13px var(--f-ui);fill:var(--dim);letter-spacing:.04em}
.sl{font:700 20px/22px var(--f-disp);fill:var(--ink);letter-spacing:-.01em}
.im{font:500 15px var(--f-ui);fill:var(--dim)}
.rn{font:600 13px var(--f-ui);fill:var(--ink)}
.stw{font:700 13px var(--f-ui);fill:var(--white);letter-spacing:.04em;text-transform:uppercase}
.sn{font:600 15px var(--f-ui);fill:var(--ink)}
.sv{font:600 13px var(--f-ui);fill:var(--ink)}
.sd{font:500 13px var(--f-ui);fill:var(--dim)}
.wkb{font:700 13px var(--f-ui);fill:var(--white);letter-spacing:.02em}
.sp.big{color:var(--ink)}
.sp.ak-target .ln,.sp.ak-target .hd,.sp.ak-target .tk{--ak-hi:var(--red)}
.sp.ak-target .tg,.sp[data-ak-sel] .tg{fill:var(--ink)}
.ak-stepping .sp.big:not(.ak-now):not(.ak-done):not(.ak-target) .tg,.ak-stepping .sp.big:not(.ak-now):not(.ak-done):not(.ak-target) .hd{fill:var(--stone)}
@media (max-width:899.98px){.dr-wide{display:none}.dr-narrow{display:block;width:100%;height:auto;margin:0}}
'''


# --------------------------------------------------------------------------------------- view: loop R10
def stepper_html(lid):
    L = LOOPS[lid]
    names = loop_labels(lid)
    state, items = 1, ''
    for i, s_ in enumerate(L['steps']):
        l = LINKS[s_['id']]
        a = amount(state, names[i])
        a = a[0].upper() + a[1:]
        state *= 1 if s_['polarity'] == '+' else -1
        b = amount(state, names[(i + 1) % len(names)])
        sign = 'same way' if l['polarity'] == '+' else 'opposite way'
        txt = (f"{s_['id']}, {l['name']}. {a} means {b}. Sign {sign_char(l['polarity'])}, {sign}; "
               f"{grade_word(l['evidence']).lower()}; {DELAY[l['delay']]}.")
        items += f'<li data-ak-step-keys="link-{s_["id"].lower()} var-{l["to"].lower()}">{e(txt)}</li>'
    w = weakest_of(lid)
    soft = any(RANK[LINKS[x['id']]['evidence']] <= 2 for x in L['steps'] if x.get('id'))
    end = (f"The loop is back where it started, so it {'can feed itself' if soft and L['type'] == 'R' else L['kind_gloss']}: {L['kind_word'].lower()}. "
           + (f"Its weakest step is {w[0]}, graded {grade_word(LINKS[w[0]]['evidence']).lower()}." if w else ''))
    first = L['stations'][0]['code']
    idle = f"Start at {first}, {lab(first)}, and suppose it rises. Press Play, or Next step to follow one numbered connection at a time."
    bar = (f'<div class="st-bar"><h2 id="h-step" class="eyebrow">Follow one turn</h2>'
           f'<div class="st-btns"><button class="ak-btn" type="button" data-ak-step="play">Play</button>'
           f'<button class="ak-btn" type="button" data-ak-step="prev">Previous step</button>'
           f'<button class="ak-btn" type="button" data-ak-step="next">Next step</button>'
           f'<button class="ak-btn" type="button" data-ak-step="reset">Reset</button></div>'
           f'<p class="st-status" data-ak-step-status aria-live="polite">{e(idle)}</p></div>')
    lst = f'<ol class="st-list" data-ak-step-list aria-label="The steps in order">{items}</ol>'
    return bar, lst, f'data-ak-stepper data-ak-hold="3200" data-ak-end="{e(end)}"'


def reform_row(rid, here_lid=None, red=False):
    R = REFORMS[rid]
    tg = ', '.join(target_words(t) for t in R['targets'])
    lead = first_sentence(R['summary'])
    swatch = ''
    attrs = f'data-select="reform-{rid.lower()}" data-reform="{rid}" data-targets="{" ".join(R["targets"])}"'
    say = f'{rid}, {R["title"]}. Acts on {tg}.'
    if rid == 'R-01':
        name = f'<a href="#reform-r01" {attrs} data-say="{e(say)}" aria-label="{e(say)} Opens the full reform.">{e(R["title"])}</a>'
    else:
        name = f'<button type="button" class="tbtn" {attrs} data-say="{e(say)}">{e(R["title"])}</button>'
    return (f'<li class="rrow">{swatch}<p class="rr-id">{chip("Reform", rid)}</p><h3 class="rr-t">{name}</h3>'
            f'<p class="rr-lead">{e(lead)}</p><p class="rr-tg"><b>Acts on</b> {e(tg)}</p>'
            + (f'<p class="rr-disc"><b>Disclosure.</b> {e(R["disclosure"])}</p>' if R.get('disclosure') else '') + '</li>')


def view_loop_r10():
    lid = 'R10'
    L = LOOPS[lid]
    home = PARTS[L['home']]
    w = weakest_of(lid)
    head = (f'<header class="vhead"><div class="vhead-main">'
            f'<p class="eyebrow">{chip("Loop", lid)}{e(kind_line(lid))} · lives in {e(home["plain_name"])}</p>'
            f'<h1 class="display" id="h-loop" data-ak-heading data-loop="{lid}" data-name="{e(L["plain_name"])}">{e(L["plain_name"])}</h1>'
            f'<p class="figline lede">{e(L["title"])}.</p>'
            f'<p class="deck">{e(L["summary"])}</p></div>'
            f'<div class="vhead-side"><div class="aloud"><p class="eyebrow">Read it aloud</p>'
            f'<p class="aloud-line">{e(read_aloud(lid))}</p>'
            f'<p class="note dim">Built from the signs: start with more, flip at each minus. '
            f'A plus sign means the two move the same way. It does not mean the change is good.</p></div></div></header>')
    keyline = (f'<p class="redkey">Red marks the three places where R-01, {e(REFORMS["R-01"]["title"].lower())}, acts: '
               f'{", ".join(REFORMS["R-01"]["targets"])}. R-02 and R-03 are named in light type where they act. '
               f'Choose another reform below to move the red to its targets.</p>')
    bar, lst, st_attrs = stepper_html(lid)
    drawing = (f'<section class="loopfig stepper" {st_attrs} aria-labelledby="h-step">{bar}'
               f'<div class="lf-draw">{square_drawing(lid, "loop-r10-full")}{chain_drawing(lid, "loop-r10-phone")}'
               f'<p class="ak-readout caption dim" data-ak-readout>Choose a box or an arrow to read it.</p>{keyline}</div>'
               f'<div class="lf-side">{lst}</div></section>'
               f'<div class="cols2 inwords"><div><p class="eyebrow">The loop in V7\'s words</p><p class="quote">{e(L["how_to_read"])}</p></div>'
               f'<div>{key_small()}</div></div>')
    ev = (f'<section class="sec" aria-labelledby="h-ev"><div class="sec-head"><h2 id="h-ev">How sure, and how slow</h2></div>'
          f'<div class="cols3"><div><h3 class="phead">The weakest step</h3><p class="ptext">'
          f'{e(w[0])}, {e(LINKS[w[0]]["name"])}, is graded {e(grade_word(LINKS[w[0]]["evidence"]).lower())}: {e(grade_gloss(LINKS[w[0]]["evidence"]))}. '
          f'{e(LINKS[w[0]]["qualification"] or "")}</p></div>'
          f'<div><h3 class="phead">The evidence</h3><p class="ptext">{e(L["evidence_summary"])}</p></div>'
          f'<div><h3 class="phead">The timing</h3><p class="ptext">One turn takes {e(L["delay_word"])}. '
          + ' '.join(f'{s_["id"]}: {DELAY[LINKS[s_["id"]]["delay"]]}.' for s_ in L['steps']) +
          f' {e(DIRECTION.get(L["direction"]))}. V7 tracks it by the {e(lower_first(L["reference_mode"]))}.</p>'
          f'<p class="ptext dim">{e(L["closure"].capitalize())}.</p></div></div></section>')
    keep = (f'<section class="sec" aria-labelledby="h-keep"><div class="sec-head"><h2 id="h-keep">Keep in mind</h2></div>'
            f'<div class="cols2"><div><h3 class="phead">The qualification</h3><p class="body">{e(L["qualification"])}</p>'
            f'<h3 class="phead mt">Where it shows up</h3><p class="body">{e(L["case"])}</p></div>'
            f'<div><h3 class="phead">Where it bends</h3><p class="body">{e(sent(L["nonlinearity"]))}</p>'
            f'<h3 class="phead mt">How people adapt</h3><p class="body">{e(sent(L["adaptation"]))}</p></div></div></section>')
    rf = ''.join(reform_row(r, lid, red=(r == 'R-01')) for r in L['reforms'])
    reforms = (f'<section class="sec" aria-labelledby="h-rf"><div class="sec-head"><h2 id="h-rf">Where reforms act on this loop</h2>'
               f'<p>{len(L["reforms"])} reforms aim at it. Each acts on named steps or boxes, shown on the drawing.</p></div>'
               f'<ul class="rrows">{rf}</ul></section>')
    return (f'<section data-view-root="loop-r10" data-crumb="{e(L["plain_name"])}, loop {lid}" data-parent="area-c" '
            f'data-ak-reform="reform-r-01" aria-labelledby="h-loop"><div class="wrap">{head}{drawing}{ev}{keep}{reforms}</div></section>')


# --------------------------------------------------------------------------------------- view: reform R-01
def view_reform_r01():
    rid = 'R-01'
    R = REFORMS[rid]
    pe, re_ = R['problem_evidence'], R['remedy_evidence']
    issues_aimed = [k for k, i in ISSUES.items() if any(a['id'] == rid for a in i['aimed_reforms']) and not i.get('retired')]
    iss = ''.join(issue_row(k) for k in issues_aimed)
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z])', R['summary'])
    stance = ' '.join(x for x in sents if x.startswith('The Atlas takes no position'))
    case = ' '.join(x for x in sents if not x.startswith('The Atlas takes no position'))
    head = (f'<header class="vhead"><div class="vhead-main">'
            f'<p class="eyebrow">{chip("Reform", rid)}Band: {e(R["band"])}</p>'
            f'<h1 class="display" id="h-reform" data-ak-heading data-reform="{rid}" data-name="{e(R["title"])}">{e(R["title"])}</h1>'
            f'<p class="deck">{e(case)}</p>'
            f'<div class="statusline"><p class="eyebrow">Status, checked {date_words(R["status"]["checked"])}</p>'
            f'<p class="ptext">{e(R["status"]["text"])} <span class="dim">Result of the check: {e(R["status"]["result"])}.</span></p></div></div>'
            f'<div class="vhead-side"><aside class="stancebox" aria-labelledby="h-stance"><p class="eyebrow" id="h-stance">Where the Atlas stands, and a disclosure</p>'
            f'<p class="stance">{e(stance)}</p>'
            f'<p class="disc"><b>Disclosure.</b> {e(R["disclosure"])}</p></aside></div></header>')
    R10_ = LOOPS['R10']
    problem = (f'<section class="sec" aria-labelledby="h-prob"><div class="sec-head"><h2 id="h-prob">The problem it answers</h2></div>'
               f'<div class="cols2"><div><p class="eyebrow">The loop it answers: {e(R10_["plain_name"].lower())}, R10</p>'
               f'<p class="body">{e(R10_["summary"])}</p>'
               f'<p class="eyebrow mt">Evidence for the problem: {e(grade_word(pe["grade"]))}, {e(grade_gloss(pe["grade"]))}</p>'
               f'<p class="body">{e(pe["text"])}</p></div>'
               f'<div><p class="eyebrow">Issues it aims at</p><ul class="irows">{iss}</ul></div></div></section>')
    tgt = ''.join(f'<li>{e(target_words(t))}</li>' for t in R['targets'])
    acts = (f'<section class="sec" aria-labelledby="h-acts"><div class="sec-head"><h2 id="h-acts">What it changes, and where it acts</h2></div>'
            f'<p class="body wide">{e(R["what_it_changes"])}</p>'
            f'<div class="loopfig rfig"><div class="lf-draw">{square_drawing("R10", "reform-r01-loop", interactive=True, stepper=False, notes="r01")}'
            f'{chain_drawing("R10", "reform-r01-loop-phone", interactive=True, stepper=False, notes="r01")}'
            f'<p class="ak-readout caption dim" data-ak-readout>The safe-seat loop, R10. Choose a box or an arrow to read it.</p>'
            f'<p class="redkey">Red marks the three places where R-01 acts: {", ".join(R["targets"])}.</p></div>'
            f'<div class="lf-side"><p class="eyebrow">Its three targets, in red</p><ul class="tlist">{tgt}</ul>'
            f'<p class="eyebrow mt">The loops it sits on</p><ul class="tlist">'
            + ''.join(f'<li><a href="{loop_href(x)}">{e(LOOPS[x]["plain_name"])}</a> <span class="dim">{x}, {e(LOOPS[x]["title"])}</span></li>' for x in R['loops'])
            + f'</ul><div class="mt">{key_small()}</div></div></div></section>')
    eff_rows = ''.join(f'<li><span class="ef-f">{e(D["families"][f])}</span><span class="ef-v">{e(D["effect_codes"].get(c, c).capitalize())}</span>'
                       f'{effect_bar(c)}</li>' for f, c in R['effects'].items())
    effects = (f'<section class="sec" aria-labelledby="h-eff"><div class="sec-head"><h2 id="h-eff">Likely effects, family by family</h2>'
               f'<p>Each family is rated on its own scale, so the four are never added into one score. Confidence: {e(R["effects_confidence"])}.</p></div>'
               f'<ul class="efx">{eff_rows}</ul></section>')
    rts = ''
    for r in R['routes']:
        chk = f'Checked {date_words(r["checked"])}' if r.get('checked') else 'No check date in V7'
        rts += (f'<li class="route"><p class="eyebrow">{e(D["route_names"].get(r["route"], r["route"]))}</p><h3>{e(r["who"])}</h3>'
                f'<p class="feas"><b>Feasibility: {e(r["feasibility"])}.</b> {e(D["feasibility_scale"][r["feasibility"]])}</p>'
                + (f'<p class="ptext">{e(r["note"])}</p>' if r.get('note') else '') + f'<p class="note dim">{chk}</p></li>')
    routes = (f'<section class="sec" aria-labelledby="h-rt"><div class="sec-head"><h2 id="h-rt">Who could adopt it</h2>'
              f'<p>{e(first_sentence(R["who_decides"]))}</p></div><ul class="routes">{rts}</ul>'
              f'<div class="cols2 mt"><div><h3 class="phead">Who decides</h3><p class="body">{e(R["who_decides"])}</p></div>'
              f'<div><h3 class="phead">Legal authority</h3><p class="body">{e(R["legal_authority"])}</p></div></div></section>')
    evid = (f'<section class="sec" aria-labelledby="h-evd"><div class="sec-head"><h2 id="h-evd">The evidence, graded twice</h2>'
            f'<p>The problem and the remedy carry separate grades.</p></div><div class="cols2">'
            f'<div><p class="eyebrow">Problem</p><p class="ef-v">{e(grade_word(pe["grade"]))}</p><p class="body">{e(grade_gloss(pe["grade"]).capitalize())}. '
            f'The record for the problem is set out at the top of this page, under the problem it answers.</p></div>'
            f'<div><p class="eyebrow">Remedy</p><p class="ef-v">{e(grade_word(re_["grade"]))}</p><p class="body">{e(grade_gloss(re_["grade"]).capitalize())}. {e(re_["text"])}</p></div></div></section>')
    measures = ''.join(f'<li>{e(m)}</li>' for m in R['success_measures'])
    risks = (f'<section class="sec" aria-labelledby="h-risk"><div class="sec-head"><h2 id="h-risk">Tradeoffs and how it could fail</h2></div>'
             f'<div class="cols2"><div><h3 class="phead">Tradeoffs</h3><p class="body">{e(R["tradeoffs"])}</p>'
             f'<h3 class="phead mt">Costs</h3><p class="body">{e(R["costs"])}</p>'
             f'<h3 class="phead mt">Other options</h3><p class="body">{e(R["alternatives"])}</p></div>'
             f'<div><h3 class="phead">How it could fail</h3><p class="body">{e(R["failure_risks"])}</p>'
             f'<h3 class="phead mt">Carrying it out</h3><p class="body">{e(R["implementation"])}</p>'
             f'<h3 class="phead mt">How to judge results</h3><ul class="blist">{measures}</ul></div></div></section>')
    return (f'<section data-view-root="reform-r01" data-crumb="Reform R-01" data-parent="loop-r10" data-ak-reform="reform-r-01" '
            f'aria-labelledby="h-reform"><div class="wrap">{head}{problem}{acts}{effects}{routes}{evid}{risks}</div></section>')


def effect_bar(code):
    """Categorical marks: three cells, filled by size, a dot for uncertain; never a total."""
    size = {'+S': 1, '+M': 2, '+L': 3, '-S': 1, '-M': 2, '0': 0, '?': 0}.get(code, 0)
    cells = ''.join(f'<span class="ec{" on" if i < size else ""}{" neg" if code.startswith("-") else ""}"></span>' for i in range(3))
    return f'<span class="ebar" aria-hidden="true">{cells}</span>'


def issue_row(k):
    I = ISSUES[k]
    pe = I.get('problem_example') or {}
    ex = (f'<span class="ir-ex"><b>Example:</b> {e(pe["headline"])} ({e(", ".join(v for v in [pe.get("where"), pe.get("when")] if v))})</span>'
          if pe.get('headline') else '<span class="ir-ex dim">No real-world example on record yet.</span>')
    rf = ' '.join(chip('Reform', a['id']) for a in I['aimed_reforms'])
    say = f'Issue {k}: {I["title"]}. Opens it in the reading panel.'
    return (f'<li class="irow"><button type="button" class="ir-btn" data-select="issue-{k.lower()}" data-issue="{k}" data-name="{e(I["title"])}" '
            f'data-say="{e(say)}"><span class="ir-t">{e(I["title"])}</span>{ex}</button>'
            f'<span class="ir-meta"><span>{grade_word(I["grade"])}</span>{rf}<span class="dim">{k}</span></span></li>')


EXTRA_CSS += r'''
.lede{margin-top:10px}
.figs{list-style:none;display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:22px;padding-top:12px;border-top:1px solid var(--stone);max-width:800px;font:500 15px/23px var(--f-ui);color:var(--dim)}
.figi{font:800 22px/1 var(--f-disp);letter-spacing:-.02em;color:var(--ink);margin-right:4px;font-variant-numeric:tabular-nums}
.aloud{border-top:2px solid var(--ink);background:var(--ground);border:1px solid var(--stone);padding:16px 20px 20px}
.aloud .eyebrow{margin-bottom:8px}
.aloud-line{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;margin-bottom:14px}
.aloud .quote{font-size:19px;line-height:27px;color:var(--ink);margin-bottom:10px}
.loopfig{display:grid;grid-template-columns:880px minmax(0,1fr);gap:40px;margin-top:48px;align-items:start}
.lf-side{position:sticky;top:24px}
.st-btns{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.ak-btn{background:var(--ground);color:var(--ink);border-color:var(--ink);min-height:44px}
.st-status{font:600 17px/25px var(--f-ui);min-height:100px;margin-bottom:12px}
.st-list{list-style:none;counter-reset:s;border-top:1px solid var(--stone)}
.st-list li{font:500 15px/22px var(--f-ui);color:var(--dim);padding:10px 0 10px 16px!important;border-bottom:1px solid var(--stone)}
.st-list li[aria-current="step"]{color:var(--ink);box-shadow:inset 4px 0 0 var(--ink)}
.redkey{display:flex;gap:10px;align-items:center;margin-top:10px;font:500 15px/22px var(--f-ui);color:var(--ink)}
.rsw{flex:none;display:inline-block;width:28px;height:3px;background:var(--red)}
.cols3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.cols2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 48px}
.cols3 .phead,.cols2 .phead{margin-bottom:8px}
.mt{margin-top:24px}
.rrows{list-style:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.rrow{position:relative;border-top:1px solid var(--stone);padding-top:14px}
.rrow .rsw{position:absolute;top:-2px;left:0;width:100%;height:3px}
.rr-id{margin-bottom:8px}
.rr-t{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;margin-bottom:8px}
.rr-t a,.rr-t button{text-decoration:underline;text-decoration-color:var(--stone);text-underline-offset:5px}
.rr-t button[data-ak-sel]{text-decoration-color:var(--white)}
.rr-lead{font:500 15px/23px var(--f-ui);color:var(--dim);margin-bottom:8px}
.rr-tg{font:500 13px/18px var(--f-ui);color:var(--dim)}
.rr-tg b{color:var(--ink)}
.rr-disc{margin-top:8px;font:500 13px/18px var(--f-ui);color:var(--ink)}
.rr-disc b{font-weight:700}
.statusbox{border-top:2px solid var(--ink);background:var(--ground);border:1px solid var(--stone);padding:16px 20px 20px}
.statusbox .eyebrow{margin-bottom:8px}
.disc{margin-top:12px;padding-top:12px;border-top:1px solid var(--stone);font:500 15px/23px var(--f-ui)}
.tlist{list-style:none;display:grid;gap:6px;margin-top:8px;font:500 15px/23px var(--f-ui)}
.rfig{margin-top:40px}
.efx{list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
.efx li{border-top:1px solid var(--stone);padding-top:12px;display:grid;gap:6px}
.ef-f{font:700 13px/18px var(--f-ui);letter-spacing:.06em;text-transform:uppercase;color:var(--dim)}
.ef-v{font:800 22px/26px var(--f-disp)}
.ebar{display:flex;gap:4px}
.ec{width:28px;height:10px;border:1.5px solid var(--dim)}
.ec.on{background:var(--ink);border-color:var(--ink)}
.routes{list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
.route{border-top:1px solid var(--stone);padding-top:12px;display:grid;gap:8px;align-content:start}
.route h3{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;text-wrap:balance}
.feas{font:500 15px/23px var(--f-ui)}
.blist{padding-left:20px;font:400 17px/27px var(--f-ui)}
.irows{list-style:none;border-top:1px solid var(--stone)}
.irow{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:start;border-bottom:1px solid var(--stone);padding:12px 0}
.ir-btn{appearance:none;background:none;border:0;padding:0;text-align:left;cursor:pointer;color:var(--ink);display:grid;gap:4px}
.ir-t{font:600 17px/24px var(--f-ui)}
.ir-btn:hover .ir-t{text-decoration:underline;text-underline-offset:3px}
.ir-btn[data-ak-sel] .ir-t{text-decoration:underline;text-decoration-thickness:2px;text-decoration-color:var(--ak-hi,var(--ink))}
.ir-ex{font:500 15px/22px var(--f-ui);color:var(--dim)}
.ir-ex b{color:var(--ink);font-weight:600}
.ir-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end;font:500 13px/18px var(--f-ui);color:var(--ink);max-width:260px}
.ir-meta .chip{margin-right:0}

@media (max-width:899.98px){
 .cols3,.cols2,.rrows,.efx,.routes{grid-template-columns:1fr}
 .irow{grid-template-columns:1fr}.ir-meta{justify-content:flex-start;max-width:none}
 .aloud-line{font-size:18px;line-height:24px}
}
'''


# --------------------------------------------------------------------------------------- view: Elections (area C)
def glyph(k):
    l = LINKS[k]
    m, _, _ = wire_tag_end([(2, 10), (62, 10)], 2, l['evidence'], l['polarity'] if l['polarity'] in ('+', '-') else '+', None)
    return f'<svg class="gl" data-view="glyph-{k.lower()}" viewBox="0 0 64 20" width="64" height="20" aria-hidden="true"><g class="sp">{m}</g></svg>'


def conn_row(k, side):
    l = LINKS[k]
    g = l['evidence']
    far = l['from'] if side == 'in' else l['to']
    say = f"{k}: {l['name']}. {link_sentence(k)}. {grade_word(g)}, {grade_gloss(g)}. {DELAY[l['delay']].capitalize()}."
    return (f'<li class="crow"><button type="button" class="cr-btn" data-select="link-{k.lower()}" data-link="{k}" '
            f'data-sign="{sign_attr(l["polarity"])}" data-grade="{g}" data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}" '
            f'data-say="{e(say)}">{glyph(k)}<span class="cr-txt"><span class="cr-n">{e(l["name"])}</span>'
            f'<span class="cr-s">{e(lab(l["from"]))} <b>{verb(l["polarity"])}</b> {e(lower_first(lab(l["to"])))}</span>'
            f'<span class="cr-g">{grade_word(g)}: {grade_gloss(g)} · {DELAY[l["delay"]]} · {k}</span></span></button></li>')


def var_row(n):
    N = NODES[n]
    ins = [k for k, l in LINKS.items() if l['to'] == n]
    outs = [k for k, l in LINKS.items() if l['from'] == n]
    say = f"{n} {lab(n)}. {N['increase_means']}"
    loops_ = ', '.join(N['loops']) or 'none'
    return (f'<li class="vrow"><div class="vr-icon">{icon(n, 48)}</div>'
            f'<div class="vr-name"><p class="cd2">{chip("Variable", n)}</p><h3><button type="button" class="tbtn" data-select="var-{n.lower()}" '
            f'data-node="{n}" data-name="{e(lab(n))}" data-say="{e(say)}">{e(lab(n))}</button></h3><p class="dim">{e(N["title"])}</p></div>'
            f'<div class="vr-desc"><p class="ptext">{e(N["description"])}</p><p class="ptext vr-im">{e(N["increase_means"])}</p></div>'
            f'<div class="vr-meta"><p>{len(ins)} in · {len(outs)} out</p><p>Loops: {e(loops_)}</p></div></li>')


def view_area_c():
    pid = 'C'
    P_ = PARTS[pid]
    ks = links_touching_part(pid)
    ins_ = [k for k in ks if PART_OF[LINKS[k]['to']] == pid and PART_OF[LINKS[k]['from']] != pid]
    outs_ = [k for k in ks if PART_OF[LINKS[k]['from']] == pid and PART_OF[LINKS[k]['to']] != pid]
    inside_ = inside(pid)
    lt = loops_through(pid)
    rf = reforms_aimed(pid)
    iss = issues_in(pid)
    stats = ''.join(f'<li><span class="fig">{v}</span><span class="note dim">{e(t)}</span></li>' for v, t in [
        (cnt('variables_C', len(P_['nodes'])), 'variables'), (cnt('custom:in', len(ins_)), 'connections in'),
        (cnt('custom:out', len(outs_)), 'connections out'), (cnt('custom:inside', len(inside_)), 'inside'),
        (cnt('custom:loops-through-c', len(lt)), 'loops run through'), (cnt('custom:reforms-c', len(rf)), 'reforms aimed here'),
        (cnt('custom:issues-c', len(iss)), 'issues tracked')])
    head = (f'<header class="vhead"><div class="vhead-main">'
            f'<p class="eyebrow">{chip("Part", pid)}{e(P_["formal_title"])} · {e(P_["chapter"])}</p>'
            f'<h1 class="display" id="h-area" data-ak-heading data-part="C" data-name="{e(P_["plain_name"])}">{e(P_["plain_name"])}: {e(lower_first(P_["plain_question"]))}</h1>'
            f'<p class="deck">{e(P_["story"])}</p></div>'
            f'<div class="vhead-side"><ul class="stats">{stats}</ul></div></header>')
    fig = (f'<section class="sec" aria-labelledby="h-inside"><div class="sec-head"><h2 id="h-inside">Inside Elections</h2>'
           f'<p>The five variables and the {len(inside_)} connections between them, with Quality of public services from Checks, '
           f'which closes the accountability loop.</p></div>'
           f'<p class="figline">{cnt("custom:loops-through-c3", len(NODES["C3"]["loops"]))} loops pass through the risk of losing office. '
           f'Two are drawn here: the safe-seat loop, which can feed itself, and the accountability loop, which pushes back.</p>'
           f'<div class="afig" role="region" aria-label="Inside Elections, drawing" tabindex="-1">'
           f'{square_drawing("R10", "area-c-inside", interactive=True, b4=True, stepper=False, notes="loops")}</div>'
           f'<div class="afig-phone">{chain_drawing("R10", "area-c-inside-phone", interactive=True, stepper=False, notes="loops")}'
           f'<p class="caption dim ph-gap">{e(LOOPS["B4"]["plain_name"])}, which pushes back:</p>'
           f'{chain_drawing("B4", "area-c-b4-phone", interactive=True, stepper=False, notes="loops")}</div>'
           f'<p class="ak-readout caption dim" data-ak-readout>Choose a box or an arrow to read it.</p>'
           f'<div class="cols2 mt"><p class="caption dim">The lines in words: ' + ' '.join(f'{k}, {LINKS[k]["name"]}: {link_sentence(k)}.' for k in inside_ + ['L54', 'L23']) + '</p>'
           f'<div>{key_small()}</div></div></section>')
    def grouped(keys, side):
        groups = {}
        for k in keys:
            far = LINKS[k]['from'] if side == 'in' else LINKS[k]['to']
            groups.setdefault(PART_OF[far], []).append(k)
        out = ''
        for g in PART_ORDER:
            if g in groups:
                out += (f'<div class="cgroup"><h4 class="cg-h"><span class="pc-badge2">{g}</span>{e(part_name(g))} '
                        f'<span class="dim">{e(PARTS[g]["formal_title"])} · {len(groups[g])}</span></h4>'
                        f'<ul class="crows">{"".join(conn_row(k, side) for k in groups[g])}</ul></div>')
        return out
    conn = (f'<section class="sec" aria-labelledby="h-conn"><div class="sec-head"><h2 id="h-conn">What pushes on Elections, and what it pushes on</h2>'
            f'<p>Every connection that crosses the edge of this part, grouped by the part at the other end. The line shows the evidence; the tag shows the sign.</p></div>'
            f'<div class="cols2 conn2"><div><h3 class="phead">Pushed on by · {len(ins_)}</h3>{grouped(ins_, "in")}</div>'
            f'<div><h3 class="phead">Pushes on · {len(outs_)}</h3>{grouped(outs_, "out")}</div></div></section>')
    vars_ = (f'<section class="sec" aria-labelledby="h-vars"><div class="sec-head"><h2 id="h-vars">The five variables</h2>'
             f'<p>Each name is a condition that can rise or fall. The bold line says what a higher value means.</p></div>'
             f'<ul class="vrows">{"".join(var_row(n) for n in P_["nodes"])}</ul></section>')
    loops_ = (f'<section class="sec" aria-labelledby="h-al"><div class="sec-head"><h2 id="h-al">The {len(lt)} loops that run through Elections</h2>'
              f'<p>Each has at least one box in this part. {len([k for k in lt if loop_home(k) == pid])} live here; the others start in a neighboring part.</p></div>'
              f'<div class="lgrid">{"".join(loop_card(k, "area") for k in lt)}</div></section>')
    rrows = ''.join(reform_row(r) for r in rf)
    reforms = (f'<section class="sec" aria-labelledby="h-arf"><div class="sec-head"><h2 id="h-arf">{len(rf)} reforms aimed at Elections</h2>'
               f'<p>Each acts on a variable in this part or on a connection that starts or ends here. Choose one to see its targets in red on the drawing above.</p></div>'
               f'<ul class="rrows">{rrows}</ul></section>')
    by_dom = {}
    for k in iss:
        by_dom.setdefault(ISSUES[k]['domain'], []).append(k)
    order = sorted(by_dom, key=lambda dm: -len(by_dom[dm]))
    ig = ''.join(f'<div class="igroup"><h3 class="ig-h">{e(DOMAINS[dm]["title"])} <span class="dim">{len(by_dom[dm])}</span></h3>'
                 f'<ul class="irows">{"".join(issue_row(k) for k in by_dom[dm])}</ul></div>' for dm in order)
    n_ex = sum(1 for k in iss if (ISSUES[k].get('problem_example') or {}).get('headline'))
    issues = (f'<section class="sec" aria-labelledby="h-iss"><div class="sec-head"><h2 id="h-iss">{len(iss)} problems tracked in Elections</h2>'
              f'<p>Every active issue in V7 that names one of the five variables, grouped by topic; {n_ex} come with a real case. '
              f'Choose one for the evidence, the response and its tradeoff. The reforms aimed at them follow.</p></div>'
              f'<div class="igroups">{ig}</div></section>')
    index = [('h-inside', 'Inside'), ('h-conn', 'Connections'), ('h-vars', 'Variables'), ('h-al', 'Loops'),
             ('h-iss', 'Problems'), ('h-arf', 'Reforms')]
    pidx = ('<nav class="pindex" aria-label="On this page"><p class="eyebrow">On this page</p><ul>'
            + ''.join(f'<li><a href="#area-c" data-jump="{i}">{t}</a></li>' for i, t in index) + '</ul></nav>')
    return (f'<section data-view-root="area-c" data-crumb="Part C, Elections" data-parent="overview" aria-labelledby="h-area">'
            f'<div class="wrap">{head}{pidx}{fig}{conn}{vars_}{loops_}{issues}{reforms}</div></section>')


EXTRA_CSS += r'''
.stats{list-style:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 24px;border-top:2px solid var(--ink);padding-top:16px}
.stats li{display:grid;gap:4px}
.afig{margin-top:24px}
.afig .dr-wide{width:100%;min-width:1140px}
.dr-l24{margin-top:24px}
.conn2 .phead{margin-bottom:12px}
.cgroup{margin-bottom:20px}
.cg-h{font:600 15px/22px var(--f-ui);display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:8px;border-bottom:1px solid var(--ink)}
.cg-h .dim{font-weight:500}
.pc-badge2{display:inline-block;min-width:22px;height:22px;padding:0 5px;border:1.5px solid var(--dim);color:var(--dim);font:700 13px/19px var(--f-ui);text-align:center}
.crows{list-style:none}
.crow{border-bottom:1px solid var(--stone)}
.cr-btn{appearance:none;background:none;border:0;width:100%;text-align:left;cursor:pointer;color:var(--ink);padding:10px 0;display:grid;grid-template-columns:64px minmax(0,1fr);gap:14px;align-items:start}
.cr-btn .gl{margin-top:3px}
.cr-txt{display:grid;gap:2px}
.cr-n{font:600 15px/21px var(--f-ui)}
.cr-s{font:500 15px/21px var(--f-ui);color:var(--ink)}
.cr-g{font:500 13px/18px var(--f-ui);color:var(--dim)}
.cr-btn:hover .cr-n{text-decoration:underline;text-underline-offset:3px}
.cr-btn[data-ak-sel] .cr-n{text-decoration:underline;text-decoration-thickness:2px;text-decoration-color:var(--ak-hi,var(--ink))}
.cr-btn[data-ak-sel] .gl{--ak-hi:inherit}
.vrows{list-style:none;border-top:1px solid var(--ink)}
.vrow{display:grid;grid-template-columns:64px 3fr 6fr 2fr;gap:24px;padding:18px 0;border-bottom:1px solid var(--stone);align-items:start}
.vr-name h3{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;margin:6px 0 4px}
.vr-name h3 button{text-decoration:underline;text-decoration-color:var(--stone);text-underline-offset:5px}
.vr-name .dim{font:500 13px/18px var(--f-ui)}
.vr-im{margin-top:8px;color:var(--ink);font-weight:600}
.vr-desc .ptext:first-child{color:var(--dim)}
.vr-meta{font:500 13px/18px var(--f-ui);color:var(--dim);display:grid;gap:4px}
.igroup{margin-bottom:28px}
.ig-h{font:800 22px/26px var(--f-disp);letter-spacing:-.02em;margin-bottom:8px}
@media (max-width:899.98px){
 .vrow{grid-template-columns:48px minmax(0,1fr);gap:12px 16px}
 .vr-desc,.vr-meta{grid-column:2}
 .vr-icon svg{width:48px;height:48px}
 .stats{grid-template-columns:repeat(3,minmax(0,1fr))}
}
'''


# --------------------------------------------------------------------------------------- view: how to read
def gloss(term_start):
    return next(g['definition'] for g in D['glossary'] if g['term'].startswith(term_start))


def spec_svg(name, body, w=300, h=56, label=''):
    return (f'<svg class="spec" data-view="spec-{name}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{e(label)}">{body}</svg>')


def spec_arrow(grade, sign, delay=None, end='head', w=3, length=240, authority=False, red=False):
    m, _, _ = wire([(4, 28), (length, 28)], w, grade, sign, delay, tag_at=0.55, end=end, authority=authority)
    g = f'<g class="sp big">{m}</g>'
    if red:
        g = f'<g class="sp big ak-target" data-red="working" data-red-job="where a reform acts (specimen)">{m}</g>'
    return g


def view_how_to_read():
    rows = []
    # 1. the tip is the effect
    tip = ''.join(f'<li><div>{spec_svg("sign-" + nm, spec_arrow("well-supported", sg, end=en, authority=au), label=lb)}</div>'
                  f'<p><b>{e(wd.capitalize())}.</b> {e(tx)}</p></li>' for nm, sg, en, au, wd, lb, tx in [
                      ('plus', '+', 'head', False, 'raises', 'An arrow with a plus tag', first_sentence(gloss('Positive sign')) + ' A plus sign does not mean the change is good.'),
                      ('minus', '-', 'head', False, 'lowers', 'An arrow with a minus tag', gloss('Negative sign')),
                      ('authority', None, 'diamond', True, 'decides', 'A line ending in an open diamond', gloss('Authority connection'))])
    rows.append(('The tip is the effect', 'Read every arrow from its tail to its tip: the tail changes, and the tip moves. The tag on the line says which way.', f'<ul class="specs">{tip}</ul>'))
    # 2. texture is the evidence
    tx = ''
    for g, gl in [('documented', 'Documented'), ('well-supported', 'Well-supported'), ('plausible', 'Plausible'),
                  ('plausible_contested', 'Contested'), ('hypothesis', 'Hypothesis')]:
        tx += (f'<li><div>{spec_svg("grade-" + g, spec_arrow(g, "+"), label=grade_word(g) + " line")}</div>'
               f'<p><b>{e(grade_word(g))}: {e(grade_gloss(g))}.</b> {e(gloss(gl))}</p></li>')
    hol = f'<g class="sp big">{wire_tag_end([(4, 28), (240, 28)], 3, None, "+")[0]}</g>'
    tx += (f'<li><div>{spec_svg("grade-sketch", hol, label="Hollow line")}</div>'
           f'<p><b>Hollow: a sketched step.</b> Three loops have steps that are not numbered connections. {e(gloss("Loop closure"))}</p></li>')
    rows.append(('Texture is the evidence', 'The line itself carries the evidence grade, so it survives a black-and-white print.', f'<ul class="specs">{tx}</ul>'))
    # 3. ticks count the wait
    tk = ''.join(f'<li><div>{spec_svg("delay-" + d, spec_arrow("well-supported", "+", d), label=DELAY[d])}</div>'
                 f'<p><b>{"One tick" if d == "S" else "Two ticks" if d == "M" else "Three ticks"}: {e(DELAY[d])}.</b></p></li>' for d in ('S', 'M', 'L'))
    rows.append(('Ticks count the wait', gloss('Delay'), f'<ul class="specs">{tk}</ul>'))
    # 4. loops have a character
    ch = (f'<div class="cols2"><div><p class="phead">Reinforcing: feeds itself</p><p class="body">{e(gloss("Reinforcing loop"))}</p>'
          f'<p class="ptext dim mt">{cnt("loops_reinforcing", N_R)} of the {len(LOOPS)} loops reinforce. Count the minus signs around a loop: '
          f'an even number, or none, makes it reinforcing.</p></div>'
          f'<div><p class="phead">Balancing: pushes back</p><p class="body">{e(gloss("Balancing loop"))}</p>'
          f'<p class="ptext dim mt">{cnt("loops_balancing", N_B)} balance. An odd number of minus signs makes a loop push back.</p></div></div>'
          f'<p class="body mt">{e(gloss("Feedback loop"))}</p>')
    rows.append(('Loops have a character', 'A loop is a chain of causes that comes back to where it started.', ch))
    # 5. color is the layer
    red = spec_svg('red', spec_arrow('well-supported', '+', red=True), label='A red arrow')
    col = (f'<ul class="specs"><li><div>{spec_svg("ink", spec_arrow("well-supported", "+"), label="A bright arrow")}</div>'
           f'<p><b>Light: the route you are reading.</b> On the overview it is the main circuit, from Wealth to Policy and back.</p></li>'
           f'<li><div>{spec_svg("stone", "<g class=" + chr(34) + "flow ctx" + chr(34) + ">" + wire([(4, 28), (240, 28)], 2, "well-supported", None)[0] + "</g>", label="A gray arrow")}</div>'
           f'<p><b>Gray: context.</b> The other large flows between parts.</p></li>'
           f'<li><div>{red}</div><p><b>Red: where a reform acts.</b> One job per view. Red never marks a sign, a grade, a party or harm.</p></li></ul>'
           f'<p class="body mt">The layer is the letter and the place. The core parts, A to E, run across the middle in the order the story moves. '
           f'Outside forces, X, sit above. Your household, EC, and technology, TC, sit below. On this dark ground, hue keeps one job, and the letter carries the layer.</p>')
    rows.append(('Color is the layer', 'In the Night Edition, color marks attention, and the letter marks the layer.', col))
    body = ''.join(f'<section class="sec hrow" aria-labelledby="hr-{i}"><div class="hr-head"><p class="eyebrow">{i + 1} of {len(rows)}</p>'
                   f'<h2 id="hr-{i}" class="headline">{e(t)}</h2><p class="body dim">{e(sub)}</p></div><div class="hr-body">{content}</div></section>'
                   for i, (t, sub, content) in enumerate(rows))
    mix = ''.join(f'<li><p class="mx-q">{e(m["prompt"])}</p><p class="mx-a">{e(m["answer"])}</p>'
                  f'<p class="mx-w"><b>The mix-up:</b> {e(m["wrong"])}</p></li>' for m in D['mixups'])
    mixups = (f'<section class="sec" aria-labelledby="h-mix"><div class="sec-head"><h2 id="h-mix">{len(D["mixups"])} common mix-ups</h2>'
              f'<p>Questions readers ask, with the answer the map supports and the misreading to avoid.</p></div><ul class="mix">{mix}</ul></section>')
    head = (f'<header class="vhead"><div class="vhead-main"><p class="eyebrow">The shared language</p>'
            f'<h1 class="display" id="h-read" data-ak-heading>Every line says what happens next, and how sure we are.</h1>'
            f'<p class="deck">Each name on the map is a variable: {e(lower_first(gloss("Variable")))} Each arrow is a connection: {e(lower_first(gloss("Connection")))}</p></div>'
            f'<div class="vhead-side">{key_small()}</div></header>')
    return (f'<section data-view-root="how-to-read" data-crumb="How to read" data-parent="overview" aria-labelledby="h-read">'
            f'<div class="wrap">{head}{body}{mixups}</div></section>')


EXTRA_CSS += r'''
.hrow{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px}
.hr-head{grid-column:1/span 4}
.hr-head .headline{margin:6px 0 12px}
.hr-body{grid-column:6/span 7}
.specs{list-style:none;display:grid;gap:14px}
.specs li{display:grid;grid-template-columns:300px minmax(0,1fr);gap:24px;align-items:center;border-bottom:1px solid var(--stone);padding-bottom:14px}
.specs p{font:500 15px/23px var(--f-ui);color:var(--dim)}
.specs p b{color:var(--ink);font-weight:600}
.spec{display:block;max-width:100%;height:auto}
.mix{list-style:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 48px}
.mix li{border-top:1px solid var(--stone);padding-top:12px;display:grid;gap:6px}
.mx-q{font:600 17px/24px var(--f-ui)}
.mx-a{font:500 15px/23px var(--f-ui)}
.mx-w{font:500 13px/18px var(--f-ui);color:var(--dim)}
.mx-w b{color:var(--ink)}
@media (max-width:1100px){.hr-head,.hr-body{grid-column:1/-1}.hr-body{margin-top:16px}}
@media (max-width:899.98px){.hrow{display:block}.specs li{grid-template-columns:1fr;gap:8px}.mix{grid-template-columns:1fr}}
'''


EXTRA_CSS += r"""
.inwords{margin-top:28px;border-top:1px solid var(--stone);padding-top:14px;max-width:760px}
.inwords .eyebrow{margin-bottom:8px}
.wide{max-width:960px}
.mt8{margin-top:8px}
.rfig{margin-top:32px}
.rfig .lf-side{padding-top:14px;border-top:2px solid var(--ink)}
"""


EXTRA_CSS += r"""
/* fix pass, November 5 */
main.ak-stage{container-type:inline-size;container-name:main}
.skip{position:absolute;left:16px;top:-120px;z-index:100;padding:12px 16px;background:var(--ground);color:var(--ink);border:2px solid var(--ink);font:600 15px/20px var(--f-ui);text-decoration:none}
.skip:focus,.skip:focus-visible{top:12px}
@media (min-width:900px){html.ak-sheet main,html.ak-sheet .foot{margin-right:var(--ak-panel-w)}html.ak-sheet .boardwrap{overflow-x:auto}}
.ov-head .display .q1,.ov-head .display .q2{display:block}
.ov-head .display .q2{color:var(--dim)}
.ov-head .deck{margin-top:18px}
.finding{margin-top:12px;max-width:62ch;font:500 15px/23px var(--f-ui);color:var(--dim)}
.finding b{color:var(--ink);font-weight:600}
.qtexts{display:grid;gap:14px;border-top:2px solid var(--ink);padding-top:14px;margin-top:6px}
.qt .eyebrow{margin-bottom:4px}
.qt p:last-child{font:500 15px/23px var(--f-ui);color:var(--dim)}
.qtexts-phone{display:none}
.glance{margin-top:28px}
.gl-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:14px}
.gl-head .caption{max-width:110ch}
.gl-wide{display:block;width:1312px;max-width:none;height:auto;overflow:visible}
.gl-narrow{display:none;width:100%;height:auto;overflow:visible}
.gbx{fill:var(--ground);stroke:var(--stone);stroke-width:1px}
.gbx-x{stroke-dasharray:none}
.gp{cursor:pointer}
.gp .gbx{stroke:var(--dim)}
.gp:hover .gbx,.gp.ak-rel .gbx{stroke:var(--ink);stroke-width:2px}
.gp[data-ak-sel] .gbx{stroke:var(--ak-hi,var(--white));stroke-width:2px}
.gp:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.gn{font:800 22px var(--f-disp);fill:var(--ink);letter-spacing:-.02em}
.gxn{font:700 17px var(--f-ui);fill:var(--ink)}
.gq{font:500 15px var(--f-ui);fill:var(--ink)}
.gx{font:500 15px var(--f-ui);fill:var(--dim)}
.cwords{list-style:none;display:grid;grid-template-columns:220px 228px 220px 280px 180px;column-gap:46px;margin-top:18px;width:1312px}
.cwords li{border-top:1px solid var(--stone);padding-top:8px}
.cw-h{font:600 15px/22px var(--f-ui)}
.cw-t{font:500 13px/18px var(--f-ui);color:var(--ink)}
.lindex{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:40px}
.lc-sum{font:500 15px/23px var(--f-ui);color:var(--ink)}
.lc-read b,.lc-qual b{font-weight:600}
.lc-read{color:var(--dim)}
.lc-qual{font:500 13px/18px var(--f-ui);color:var(--ink)}
.lc-art{margin:8px 0 10px}
.loopfig.stepper{grid-template-columns:880px minmax(0,1fr);grid-template-areas:"draw bar" "draw list";row-gap:20px}
.loopfig.stepper .st-bar{grid-area:bar;border-top:2px solid var(--ink);padding-top:14px}
.loopfig.stepper .lf-draw{grid-area:draw}
.loopfig.stepper .lf-side{grid-area:list;position:static}
.st-bar .eyebrow{margin-bottom:12px}
.inwords{margin-top:32px;border-top:1px solid var(--stone);padding-top:14px;max-width:none}
.statusline{margin-top:22px;padding-top:12px;border-top:1px solid var(--stone);max-width:62ch}
.statusline .eyebrow{margin-bottom:6px}
.stancebox{border:2px solid var(--ink);padding:16px 20px 20px}
.stancebox .eyebrow{margin-bottom:10px;color:var(--ink)}
.stance{font:600 17px/25px var(--f-ui)}
.stancebox .disc{margin-top:12px;padding-top:12px;border-top:1px solid var(--stone)}
.pindex{position:sticky;top:0;z-index:20;background:var(--ground);border-bottom:1px solid var(--stone);margin-top:28px;padding:8px 0;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.pindex .eyebrow{margin:0}
.pindex ul{list-style:none;display:flex;flex-wrap:wrap;gap:4px 18px}
.pindex a{display:inline-flex;align-items:center;min-height:32px;font:600 15px/1 var(--f-ui);text-decoration-color:var(--stone)}
.afig{overflow-x:auto}
.afig-phone{display:none}
.ph-gap{margin:28px 0 12px}
.cd.ph,.rn.ph,.sv.ph,.sd.ph,.wkb.ph,.stw.ph,.vb.ph,.gw.ph,.nt.ph{font-size:15px}
.cy-narrow{width:100%;height:auto}
.irow .ir-btn{min-height:44px}
@container main (max-width:1339.98px){
 .loopfig,.loopfig.stepper{grid-template-columns:minmax(0,1fr);grid-template-areas:"bar" "draw" "list"}
 .lf-side{position:static}
 .loopfig.stepper .st-bar{position:sticky;top:0;z-index:15;background:var(--ground);padding-bottom:10px}
 .lgrid{grid-template-columns:repeat(2,minmax(0,1fr))}
 .rrows{grid-template-columns:repeat(2,minmax(0,1fr))}
 .hubs{grid-template-columns:repeat(3,minmax(0,1fr))}
 .efx,.routes{grid-template-columns:repeat(2,minmax(0,1fr))}
 .li-cols{grid-template-columns:repeat(3,minmax(0,1fr))}
 .lindex{grid-template-columns:1fr}
}
@container main (max-width:899.98px){
 .lgrid,.rrows,.hubs,.efx,.routes,.lindex{grid-template-columns:minmax(0,1fr)}
 .li-cols{grid-template-columns:1fr 1fr}
}
@media (max-width:1339.98px){
 .gl-wide{display:none}.gl-narrow{display:block;max-width:440px}
 .cwords{width:auto;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 24px}
}
@media (max-width:899.98px){
 .afig{display:none}.afig-phone{display:block}
 .qtexts{display:none}.qtexts-phone{display:grid;gap:14px;margin-top:20px}
 .gl-narrow{max-width:none}
 .cwords{grid-template-columns:1fr}
 .ov-head .display .q2{margin-top:6px}
 .gl-head .caption{display:none}
 .pindex{position:static}
 .st-btns .ak-btn{padding:4px 10px;font-size:14px}
 .st-status{min-height:0;font-size:15px;line-height:21px}
 .loopfig.stepper .st-bar .eyebrow{display:none}
 .stancebox{margin-top:8px}
}
"""


# --------------------------------------------------------------------------------------- build
def main():
    build_templates()
    views = view_overview() + view_area_c() + view_loop_r10() + view_reform_r01() + view_loops() + view_how_to_read()
    # keep only the panels a reader can open from this page: every data-select, and every pick inside a kept panel
    keys = set(re.findall(r'data-select="([^"]+)"', views))
    frontier = set(keys)
    while frontier:
        nxt = set()
        for k in frontier:
            if k in TEMPLATES:
                nxt |= set(re.findall(r'data-ak-pick="([^"]+)"', TEMPLATES[k][2])) - keys
        keys |= nxt
        frontier = nxt
    for k in list(TEMPLATES):
        if k not in keys:
            del TEMPLATES[k]
    html_ = page(views)
    assert '—' not in re.sub(r'<(script|style)\b.*?</\1>', '', html_, flags=re.S)
    OUT.write_text(html_)
    print('wrote', OUT.relative_to(ROOT), f'{len(html_) / 1e6:.2f} MB', len(TEMPLATES), 'panels')


if __name__ == '__main__':
    main()

