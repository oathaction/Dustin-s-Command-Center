"""Build editorial atlas system 02, Economist Register (Newsprint), November 5, 2026.

The system as a register a reader reads across. The overview opens on a headline and deck, a compact diagram of the
flows between the eight parts with their counts, then the register: one row per part, with its plain name over its
formal title, its question, every variable as a chip, counts of variables, connections, loops and reforms, the
evidence mix as a textured bar, and its main loop. Opening a row unfolds its story, its loop as a named chain and the
fix aimed at it. Charts and tables carry a sentence title, a measure line and a source line under a Charcoal rule.
Pillar Red appears only on the loop and reform views, where R-01 acts.

Every label, count, sign, grade, delay, issue, example and reform text is read by script from
work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json. One sentence comes from the V7
extract work/extract/atlas-v7-data.json: the editor's Yes on 3 disclosure, which the editorial dataset leaves out of
R-01's status and which the brief requires on the R-01 view. Headlines, decks and chart titles are studio drafts.

Run from the project root:
    python3 -I work/boards/phase-2/atlas-editorial/02-economist-register/build_system.py
Writes 20261105_Editorial-02-Economist-Register.html beside this file.
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
V7 = json.loads((ROOT / 'work/extract/atlas-v7-data.json').read_text())
KIT_JS = (ROOT / 'work/boards/phase-2/atlas-concepts/shared/atlas-kit.js').read_text()
KIT_CSS = (ROOT / 'work/boards/phase-2/atlas-concepts/shared/atlas-kit.css').read_text()
OUT = HERE / '20261105_Editorial-02-Economist-Register.html'

N, LK, LO, RF, IS = ED['nodes'], ED['links'], ED['loops'], ED['reforms'], ED['issues']
PARTS = {p['id']: p for p in ED['parts']}
PART_OF = {n: p['id'] for p in ED['parts'] for n in p['nodes']}
REG_ORDER = ['A', 'B', 'C', 'D', 'E', 'EC', 'TC', 'X']      # brief rule 1: the circuit, then the outer parts
CORE = ['A', 'B', 'C', 'D', 'E']
COUNT = ED['meta']['counts']
MINUS = '−'
e = lambda s: html.escape(str(s), quote=True)
assert len(N) == COUNT['variables'] == 51 and len(LK) == COUNT['connections'] == 118 and len(LO) == 23 and len(RF) == 50


def date_words(iso):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    y, m, d = iso.split('-')
    return f'{months[int(m) - 1]} {int(d)}, {y}'


SNAP = date_words(ED['meta']['snapshot'])
WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
         'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']


def nw(n, cap=False):
    w = WORDS[n] if n < len(WORDS) else str(n)
    return w[0].upper() + w[1:] if cap else w


def plural(n, one, many=None):
    return one if n == 1 else (many or one + 's')


# ------------------------------------------------------------------------------------------------ words from the data
GRADE = acc.GRADES   # value -> (word, gloss, texture)


def gnorm(g):
    """Issue grades spell well_supported; connections spell well-supported."""
    return {'well_supported': 'well-supported'}.get(g, g)


def gword(g):
    return GRADE[gnorm(g)][0]


def ggloss(g):
    return GRADE[gnorm(g)][1]


def tex_of(g):
    return GRADE[gnorm(g)][2] if gnorm(g) in GRADE else 'solid'


DELAY = acc.DELAYS


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def verb(p):
    return {'+': 'raises', '-': 'lowers'}.get(p, 'decides')


def sign_words(p):
    if p == '+':
        return 'Plus, raises: the two move the same way'
    if p == '-':
        return f'Minus, lowers: the two move opposite ways'
    return 'No sign: this line says who decides'


def low(label):
    w = label.split()[0]
    if w.isupper() or w.startswith('Congress'):
        return label
    return label[0].lower() + label[1:]


def label(code):
    return N[code]['label']


def station_labels(lid):
    return [label(s['code']) if s.get('is_variable') and s.get('code') else s['label'] for s in LO[lid]['stations']]


def read_aloud_parts(lid):
    """[(more/less, label)], from the signs, so it cannot drift (civic education memo, section 2)."""
    labs = station_labels(lid)
    cur, out = 1, [('More', labs[0])]
    steps = LO[lid]['steps']
    for i, s in enumerate(steps):
        cur *= 1 if s['polarity'] == '+' else -1
        word = 'more' if cur > 0 else 'less'
        out.append((word, labs[(i + 1) % len(labs)]))
    return out


def read_aloud(lid, bold=False):
    parts = read_aloud_parts(lid)
    f = (lambda s: f'<b>{e(low(s))}</b>') if bold else (lambda s: low(s))
    body = ', '.join(f'{w} {f(l)}' for w, l in parts[:-1])
    w, l = parts[-1]
    return f'{body}, and back to {w} {f(l)}.'


def step_sentence(s):
    a = label(s['from']) if s.get('from') in N else s['from_label']
    b = label(s['to']) if s.get('to') in N else s['to_label']
    return f'More {low(a)} means {"more" if s["polarity"] == "+" else "less"} {low(b)}.'


def link_say(lid):
    l = LK[lid]
    sign = {'+': 'Sign +, the two move the same way', '-': f'Sign {MINUS}, they move opposite ways'}.get(l['polarity'], 'No sign: it says who decides')
    return (f'{lid}: {l["name"]}. From {l["from"]} {label(l["from"])} to {l["to"]} {label(l["to"])}. {sign}. '
            f'Evidence {gword(l["evidence"]).lower()}. Delay {DELAY[l["delay"]]}.')


def first_sentences(text, n=1):
    parts = re.split(r'(?<=[a-z0-9)%][.!?])(?<! v\.)\s+(?=[A-Z"])', text.strip())
    return ' '.join(parts[:n])


def kind_line(lid):
    L = LO[lid]
    return f'{L["kind_word"]}, {L["kind_gloss"]}'


DIRECTION = {'running_up': 'running up', 'running_down': 'running down', 'running': 'running', 'disabled': 'disabled',
             'unknown': 'direction unknown', 'design_target': 'a design target'}


def direction_words(lid):
    d = LO[lid]['direction']
    return DIRECTION.get(d, d.replace('_', ' '))


def weakest_words(lid):
    L = LO[lid]
    if L['conceptual']:
        return 'No numbered steps: the missing chain is the weakest point'
    if L['weakest']:
        ws = [f'{w}, {gword(LK[w]["evidence"])}' for w in L['weakest']]
        return ('Weakest step ' if len(ws) == 1 else 'Weakest steps ') + ' and '.join(ws)
    grades = sorted({s['evidence'] for s in L['steps']}, key=lambda g: list(GRADE).index(g))
    if len(grades) == 1:
        return f'No single weakest step: every step is {gword(grades[0]).lower()}'
    return 'No single weakest step: steps graded ' + ' and '.join(gword(g).lower() for g in grades)


def disclosure(lid):
    L = LO[lid]
    if L['conceptual']:
        return 'Sketch: ' + L['closure'].split(': ', 1)[1] + '. Each step is drawn as a hollow line.'
    if L['hypothesized']:
        hyp = [s['id'] for s in L['steps'] if s['evidence'] == 'hypothesis']
        return f'Closed with a hypothesized step: {" and ".join(hyp)} {"is" if len(hyp) == 1 else "are"} untested.'
    return ''


def effect_words(code):
    out = []
    for seg in [s.strip() for s in str(code).split(';')]:
        m = re.match(r'^([+-][LMS]|0|\?)\s*(.*)$', seg)
        word = ED['effect_codes'][m.group(1)]
        out.append(word + (f' ({m.group(2)})' if m.group(2) else ''))
    return '; '.join(out)


def best_route(rid):
    order = ['high', 'medium', 'low', 'very low']
    rs = sorted(RF[rid]['routes'], key=lambda r: order.index(r['feasibility']))
    r = rs[0]
    return f'{ED["route_names"][r["route"]]}, {r["feasibility"]}'


# ------------------------------------------------------------------------------------------------ counts by part
def touching(pid):
    return [k for k, l in LK.items() if PART_OF[l['from']] == pid or PART_OF[l['to']] == pid]


def loops_through(pid):
    return [k for k in ED['loop_order'] if any(s.get('code') and PART_OF.get(s['code']) == pid for s in LO[k]['stations'])]


def target_in(t, pid):
    return (t in PART_OF and PART_OF[t] == pid) or (t in LK and pid in (PART_OF[LK[t]['from']], PART_OF[LK[t]['to']]))


def reforms_at(pid):
    return [k for k in sorted(RF) if any(target_in(t, pid) for t in RF[k]['targets'])]


def evidence_mix(lids):
    c = Counter(LK[k]['evidence'] for k in lids)
    return [(g, c.get(g, 0)) for g in GRADE]


def main_loop(pid):
    """The loop with the most stations in the part; a tie goes to the loop more reforms aim at, then model order."""
    cands = []
    for i, k in enumerate(ED['loop_order']):
        n = sum(1 for s in LO[k]['stations'] if s.get('code') and PART_OF.get(s['code']) == pid)
        if n:
            cands.append((-n, -len(LO[k]['reforms']), i, k))
    return sorted(cands)[0][3] if cands else None


def main_reform(pid):
    """The first reform the main loop lists; with no loop, the reform with the most targets in the part."""
    ml = main_loop(pid)
    if ml and LO[ml]['reforms']:
        return LO[ml]['reforms'][0]
    ranked = sorted((-sum(1 for t in r['targets'] if target_in(t, pid)), k) for k, r in RF.items())
    return ranked[0][1] if ranked[0][0] < 0 else None


FLOW = defaultdict(list)            # (from part, to part) -> connection ids
INSIDE = defaultdict(list)
for k, l in LK.items():
    a, b = PART_OF[l['from']], PART_OF[l['to']]
    (INSIDE[a] if a == b else FLOW[(a, b)]).append(k)
CROSS = sum(len(v) for v in FLOW.values())


def pname(pid):
    return PARTS[pid]['plain_name']


STATS = {}
for pid in REG_ORDER:
    t = touching(pid)
    mix = evidence_mix(t)
    STATS[pid] = {'vars': len(PARTS[pid]['nodes']), 'conn': len(t), 'loops': len(loops_through(pid)),
                  'reforms': len(reforms_at(pid)), 'mix': mix,
                  'strong': sum(n for g, n in mix if g in ('documented', 'well-supported'))}
THIN = min(REG_ORDER, key=lambda p: STATS[p]['strong'] / STATS[p]['conn'])
assert THIN == 'E', THIN    # the register's headline names Policy, where the circuit closes
N_R = sum(1 for l in LO.values() if l['type'] == 'R')
N_B = sum(1 for l in LO.values() if l['type'] == 'B')
N_WITH_REFORM = sum(1 for l in LO.values() if l['reforms'])

# Massachusetts Question 3 disclosure, quoted in full from V7 (pathway sub-issue), since ED's R-01 status omits it
DISCLOSURE = None
for pw in V7['pathways']:
    for si in pw.get('sub_issues') or []:
        if 'Question 3' in si.get('title', '') and 'Disclosure:' in si.get('text', ''):
            DISCLOSURE = (si['text'][si['text'].index('Disclosure:'):].strip(), si['title'], pw['id'])
assert DISCLOSURE and 'Yes on 3' in DISCLOSURE[0]
NO_POSITION = [s for s in re.split(r'(?<=\.)\s+', RF['R-01']['summary']) if 'takes no position' in s][0]

# ------------------------------------------------------------------------------------------------ text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False):
    w = _font(weight).getlength(text) * size / 200
    return w * 0.95 if tight else w


def tw_num(n, size, weight=700):
    """Width of a count set in tabular figures (every digit takes the width of a zero)."""
    return len(str(n)) * tw('0', size, weight, True)


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
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{s}</text>'


def svg_lines(x, y, rows, cls, lh, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    spans = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{spans}</text>'


# ------------------------------------------------------------------------------------------------ line machinery
ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 3)}   # body, point, height, sign length, bar


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
    """Stretch the pattern so the line starts and ends on ink (design frame memo, section 3)."""
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
    return d + f'L{f(pts[-1][0])} {f(pts[-1][1])}'


BEND = {2: 8, 3: 12, 6: 18}


def tag_shape(cx, cy, ux, uy, sign, w, cls):
    a, p, h, sl, sb = TAG[w]
    lt = a + p
    vx, vy = -uy, ux
    x0, y0 = cx - ux * lt / 2, cy - uy * lt / 2
    pts = [(0, -h / 2), (a, -h / 2), (lt, 0), (a, h / 2), (0, h / 2)]
    poly = ' '.join(f'{f(x0 + ux * s + vx * t)},{f(y0 + uy * s + vy * t)}' for s, t in pts)
    bx, by = x0 + ux * a / 2, y0 + uy * a / 2
    if abs(ux) > abs(uy):
        g = f'<rect class="sg" x="{f(bx - sl / 2)}" y="{f(by - sb / 2)}" width="{sl}" height="{sb}"/>'
        if sign == '+':
            g += f'<rect class="sg" x="{f(bx - sb / 2)}" y="{f(by - sl / 2)}" width="{sb}" height="{sl}"/>'
    else:   # a vertical tag: the minus bar stays horizontal so the sign reads upright
        g = f'<rect class="sg" x="{f(bx - sl / 2)}" y="{f(by - sb / 2)}" width="{sl}" height="{sb}"/>'
        if sign == '+':
            g += f'<rect class="sg" x="{f(bx - sb / 2)}" y="{f(by - sl / 2)}" width="{sb}" height="{sl}"/>'
    return f'<g class="tag {cls}"><polygon points="{poly}"/>{g}</g>'


def head_shape(tx, ty, ux, uy, w, cls):
    al, ab = ARROW[w]
    bx, by = tx - ux * al, ty - uy * al
    vx, vy = -uy, ux
    return (f'<path class="hd {cls}" d="M{f(bx + vx * ab / 2)} {f(by + vy * ab / 2)}L{f(tx)} {f(ty)}'
            f'L{f(bx - vx * ab / 2)} {f(by - vy * ab / 2)}Z"/>')


def ticks(pts, count, w, cls):
    out = []
    half = w / 2 + 4
    for i in range(count):
        (cx, cy), (ux, uy) = point_at(pts, 12 + i * 5)
        vx, vy = -uy, ux
        out.append(f'<path class="tk {cls}" d="M{f(cx - vx * half)} {f(cy - vy * half)}L{f(cx + vx * half)} {f(cy + vy * half)}"/>')
    return ''.join(out)


def wire_marks(pts, w, grade, delay, polarity, conceptual=False, tag_s=None, lit=True):
    """A connection: its texture, delay ticks after the tail, the pointing tag with the sign, the arrowhead.
    Lit marks (6 px) are drawn as well and shown by CSS when the item is selected, targeted or stepped."""
    ux, uy = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    al = ARROW[w][0]
    body = list(pts[:-1]) + [(pts[-1][0] - ux * al, pts[-1][1] - uy * al)]
    tex = 'solid' if conceptual else tex_of(grade)
    if tex == 'dotted':
        body[-1] = (body[-1][0] - ux * 1.5 * w, body[-1][1] - uy * 1.5 * w)
    length = path_len(body)
    d = rounded_d(body, BEND[w])
    das = {ww: fitted(tex, ww, length) for ww in (2, 3, 6)}
    cap = pattern(tex, w)[1]
    style = ''.join(f'--d{ww}:{das[ww]};' for ww in (2, 3, 6) if das[ww])
    dash = f' stroke-dasharray="{das[w]}"' if das[w] else ''
    st = f' style="{style}"' if style else ''
    out = f'<path class="ak-case" d="{d}" fill="none"{dash}/>'
    if conceptual:   # hollow: two rails with the ground between (design frame memo)
        out += (f'<path class="ak-mark rail" d="{d}" fill="none" stroke-width="{w + 2}"/>'
                f'<path class="railgap" d="{d}" fill="none" stroke-width="{w}"/>')
    else:
        out += f'<path class="ak-mark" d="{d}" fill="none" stroke-width="{w}" stroke-linecap="{cap}"{dash}{st}/>'
    if delay:
        n = {'S': 1, 'M': 2, 'L': 3}[delay]
        out += ticks(pts, n, w, 'lo') + (ticks(pts, n, 6, 'hi') if lit else '')
    out += head_shape(pts[-1][0], pts[-1][1], ux, uy, w, 'lo') + (head_shape(pts[-1][0], pts[-1][1], ux, uy, 6, 'hi') if lit else '')
    if polarity in ('+', '-'):
        s = tag_s if tag_s is not None else length * 0.55
        (cx, cy), (gx, gy) = point_at(body, s)
        out += tag_shape(cx, cy, gx, gy, polarity, w, 'lo') + (tag_shape(cx, cy, gx, gy, polarity, 6, 'hi') if lit else '')
    return out, body


def link_attrs(lid):
    l = LK[lid]
    return (f'data-link="{lid}" data-sign="{sign_attr(l["polarity"])}" data-grade="{l["evidence"]}" '
            f'data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}"')


# ------------------------------------------------------------------------------------------------ small marks
def record_square(x, y):
    return f'<rect class="rec" x="{f(x)}" y="{f(y - 7)}" width="7" height="7"/>'


def glyph(grade, polarity='+', delay='S', authority=False, conceptual=False, W=84, view='key'):
    """A short sample of a connection, for keys, lists and tables. Its grade is always printed beside it."""
    H = 20
    y = 10
    pts = [(2, y), (W - 2, y)]
    if authority:
        body = f'<path class="ak-mark" d="M2 {y}L{W - 16} {y}" stroke-width="2" fill="none"/>'
        body += f'<path class="dia" d="M{W - 16} {y}L{W - 9} {y - 5.5}L{W - 2} {y}L{W - 9} {y + 5.5}Z"/>'
        if delay:
            body += ticks(pts, {'S': 1, 'M': 2, 'L': 3}[delay], 2, 'lo')
    else:
        nt = {'S': 1, 'M': 2, 'L': 3}.get(delay or '', 0)
        body, _ = wire_marks(pts, 2, grade, delay, polarity, conceptual=conceptual, tag_s=12 + 5 * max(nt - 1, 0) + 14, lit=False)
    return (f'<svg class="glyph" data-view="{view}" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true" '
            f'focusable="false">{body}</svg>')


EV_ROWS = (2, 6, 10, 14)


def ev_fill(grade, x, w, H=16):
    if w <= 0:
        return ''
    if grade == 'documented':
        return f'<rect x="{f(x)}" y="0" width="{f(w)}" height="{H}" class="evs"/>'
    tex = tex_of(grade)
    arr, cap = pattern(tex, 2) if tex != 'solid' else (None, 'butt')
    out = ''
    for i, yy in enumerate(EV_ROWS):
        if yy > H:
            break
        da = f' stroke-dasharray="{" ".join(f(a) for a in arr)}"' if arr else ''
        off = f' stroke-dashoffset="{f((arr[0] + arr[1]) / 2 if arr and i % 2 else 0)}"' if arr and tex != 'dotted' else ''
        x0, x1 = (x + 1, x + w - 1) if tex == 'dotted' else (x, x + w)
        out += f'<line x1="{f(x0)}" y1="{yy}" x2="{f(x1)}" y2="{yy}" class="evl" stroke-linecap="{cap}"{da}{off}/>'
    return out


def evbar(mix, W=176, H=16, view='evidence', label=''):
    total = sum(n for _, n in mix)
    segs = [(g, n) for g, n in mix if n]
    gap = 2
    avail = W - gap * (len(segs) - 1)
    widths = [max(5.0, avail * n / total) for _, n in segs]
    scale = (avail - sum(w for w in widths if w == 5.0)) / max(1e-6, sum(w for w in widths if w > 5.0))
    widths = [w if w == 5.0 else w * scale for w in widths]
    x, body = 0.0, ''
    for (g, n), w in zip(segs, widths):
        body += ev_fill(g, x, w, H)
        x += w + gap
    return (f'<svg class="evbar" data-view="{view}" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{e(label)}">{body}</svg>')


def ev_swatch(grade, W=30, H=16):
    return (f'<svg class="evbar sw" data-view="key" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true" '
            f'focusable="false">{ev_fill(grade, 0, W, H)}</svg>')


def mix_words(mix):
    return ', '.join(f'{n} {gword(g).lower()}' for g, n in mix if n)


def icon(icon_id, uid, size):
    """A Civic Line drawing through icon_svg(), unchanged. Its own data-part="base|accent" metadata is renamed
    data-cl-part, because the November verifier reads data-part as an atlas part (A to E, X, EC, TC)."""
    return acc.icon_svg(icon_id, 'black', uid=uid, size=size).replace(' data-part="', ' data-cl-part="')


# ------------------------------------------------------------------------------------------------ chips
def idchip(word, code, compact=False, surface=''):
    c = ' compact' if compact else ''
    return f'<span class="idc{c}"><span class="k">{e(word)}</span><span class="c">{e(code)}</span></span>'


def var_chip(code, rel=True):
    n = N[code]
    rels = sorted({f'var-{(LK[k]["to"] if LK[k]["from"] == code else LK[k]["from"]).lower()}'
                   for k in LK if code in (LK[k]['from'], LK[k]['to'])}) if rel else []
    n_out = sum(1 for l in LK.values() if l['from'] == code)
    n_in = sum(1 for l in LK.values() if l['to'] == code)
    say = f'{code} {n["label"]}. {n["increase_means"]} It pushes on {n_out} and is pushed by {n_in} connections.'
    return (f'<button type="button" class="chip" data-select="var-{code.lower()}" data-node="{code}" '
            f'data-name="{e(n["label"])}" data-rel="{" ".join(rels)}" data-say="{e(say)}" aria-label="{e(say)}">'
            f'<span class="cd">{code}</span><span class="cl">{e(n["label"])}</span></button>')


def loop_href(lid):
    return '#loop-r10' if lid == 'R10' else f'#loops/loop-{lid.lower()}'


def loop_link(lid, text=None):
    t = text or LO[lid]['plain_name']
    return f'<a href="{loop_href(lid)}">{e(t)}</a>'


def fix_flag(x, y, rid):
    """The fix layer's flag: a Prussian tab with the reform's ID in White (no red on the overview)."""
    w = tw(rid, 13, 700) + 12
    return (f'<g class="flag"><rect x="{f(x)}" y="{f(y - 14)}" width="{f(w)}" height="19"/>'
            f'<text x="{f(x + 6)}" y="{f(y)}" class="fl">{e(rid)}</text></g>'), w


# ------------------------------------------------------------------------------------------------ the loop as a chain
SIZES = {
    's': dict(w=2, fs=15, fw=600, tight=False, lh=18, padx=12, h1=36, xr=8, x0=34, adx=22, ldx=18, gmin=64, drop=34),
    'l': dict(w=3, fs=20, fw=700, tight=True, lh=22, padx=18, h1=52, xr=40, x0=88, adx=40, ldx=30, gmin=96, drop=40),
}


def stack_svg(lid, W, size='s', interactive=False, view=None, reform=None, notes=False, uid='', aria=None, stepper=False):
    """The loop as a named box-and-arrow cycle, read top to bottom (DR-30). Boxes carry the variables' short labels;
    each arrow carries raises or lowers beside its sign tag, its evidence texture and its delay ticks; the weakest
    step is named; the closing step returns up the left side to the first box."""
    L = LO[lid]
    cfg = SIZES[size]
    w, fs, lh, padx = cfg['w'], cfg['fs'], cfg['lh'], cfg['padx']
    labs = station_labels(lid)
    codes = [s.get('code') if s.get('is_variable') else None for s in L['stations']]
    steps = L['steps']
    targets = set(RF[reform]['targets']) if reform else set()
    x0, xr, ax = cfg['x0'], cfg['xr'], cfg['x0'] + cfg['adx']
    lx = ax + cfg['ldx']
    flagw = (tw(reform, 13, 700) + 12 + 10) if reform and any(c in targets for c in codes if c) else 0
    if size == 'l':
        BW = max(300.0, min(420.0, max(tw(t, fs, cfg['fw'], True) for t in labs) + 2 * padx + flagw))
        note_x = x0 + BW + 24
    else:
        BW = W - x0 - 6
        note_x = None
    inner = BW - 2 * padx - flagw
    # step label blocks, measured first so each gap fits its words
    blocks = []
    lab_w = (x0 + BW - lx) if size == 'l' else (W - lx - 4)
    for i, s in enumerate(steps):
        rows = []   # (kind, text)
        if size == 'l':
            rows.append(('ey', f'Step {i + 1}' + (f' · {s["id"]}' if s['id'] else '')))
            if s['name']:
                for t in wrap(s['name'], lab_w, 15, 600):
                    rows.append(('nm', t))
            for t in wrap(step_sentence(s), lab_w, 14, 400):
                rows.append(('tx', t))
        rows.append(('sw', s))
        rows.append(('gd', s))
        if s['id'] and s['id'] in L['weakest']:
            rows.append(('wk', 'Weakest step'))
        if s['id'] and s['id'] in targets:
            rows.append(('fl', f'{reform} acts here'))
        blocks.append(rows)
    RH = {'ey': 18, 'nm': 18, 'tx': 20, 'sw': 19, 'gd': 18, 'wk': 18, 'fl': 22} if size == 'l' else \
        {'sw': 18, 'gd': 17, 'wk': 17, 'fl': 22}

    def block_h(rows):
        return sum(RH[k] for k, _ in rows)

    # vertical layout
    boxes, y = [], 8 if size == 's' else 16
    for i, t in enumerate(labs):
        rows = wrap(t, inner, fs, cfg['fw'], cfg['tight'])
        h = cfg['h1'] + lh * (len(rows) - 1)
        note_rows = []
        if notes and codes[i]:
            note_rows = wrap(N[codes[i]]['increase_means'], W - note_x - 4, 14, 400)
            h = max(h, 0)
        boxes.append({'y': y, 'h': h, 'rows': rows, 'code': codes[i], 'label': t, 'notes': note_rows})
        if i < len(labs) - 1:
            gmin = cfg['gmin'] + (24 if (interactive and size == 's') else 0)   # room for the 6 px lit marks
            gap = max(gmin, block_h(blocks[i]) + (14 if size == 's' else 26))
            if notes:
                gap = max(gap, 16 + 20 * len(note_rows) - h + 8)
            y += h + gap
        else:
            y += h
    last_bottom = y
    drop = cfg['drop']
    H = last_bottom + max(drop + 6, block_h(blocks[-1]) + 10) + (8 if size == 'l' else 4)
    if notes:
        H = max(H, boxes[-1]['y'] + 16 + 20 * len(boxes[-1]['notes']) + 8)
    first_cy = boxes[0]['y'] + boxes[0]['h'] / 2

    def label_block(x, y0, rows, s):
        out, top = [], y0
        for k, v in rows:
            yy = top
            top += RH[k]
            if k == 'ey':
                out.append(svg_text(x, yy + 13, e(v.upper()), 'sey'))
            elif k == 'nm':
                out.append(svg_text(x, yy + 13, e(v), 'snm ak-label'))
            elif k == 'tx':
                out.append(svg_text(x, yy + 14, e(v), 'stx'))
            elif k == 'sw':
                big = size == 'l'
                if v['polarity'] in ('+', '-'):
                    extra = ''
                    if big:
                        extra = f'<tspan class="sgc"> \u00b7 {"plus" if v["polarity"] == "+" else "minus"} sign</tspan>'
                    elif v['id']:
                        extra = f'<tspan class="sgc"> \u00b7 {v["id"]}</tspan>'
                    if v['index'] == len(steps):
                        extra += '<tspan class="sgc"> \u00b7 back to the start</tspan>'
                    out.append(svg_text(x, yy + 14, f'<tspan class="swv">{verb(v["polarity"])}</tspan>{extra}', 'ssw'))
            elif k == 'gd':
                if v['conceptual']:
                    out.append(svg_text(x, yy + 13, 'Conceptual step', 'sgd'))
                else:
                    g = v['evidence']
                    gtxt = f'{gword(g)}: {ggloss(g)}' if size == 'l' else gword(g)
                    t = f'{gtxt} \u00b7 {DELAY[v["delay"]]}'
                    if g == 'documented':
                        out.append(record_square(x, yy + 13) + svg_text(x + 11, yy + 13, e(t), 'sgd'))
                    else:
                        out.append(svg_text(x, yy + 13, e(t), 'sgd'))
            elif k == 'wk':
                out.append(svg_text(x, yy + 13, e(v), 'swk'))
            elif k == 'fl':
                fg, fw2 = fix_flag(x, yy + 15, reform)
                out.append(fg + svg_text(x + fw2 + 6, yy + 15, 'acts here', 'swk flagtxt'))
        return ''.join(out)

    parts_svg = []
    # boxes
    for i, b in enumerate(boxes):
        code = b['code']
        y0, h = b['y'], b['h']
        rx = h / 2
        is_var = bool(code)
        cls = 'node' + ('' if is_var else ' concept')
        shape = (f'<rect class="ak-case" x="{f(x0)}" y="{f(y0)}" width="{f(BW)}" height="{f(h)}" rx="{f(rx)}" fill="none"/>'
                 f'<rect class="ak-mark box" x="{f(x0)}" y="{f(y0)}" width="{f(BW)}" height="{f(h)}" rx="{f(rx)}" '
                 f'stroke-width="{2 if is_var else 1}"/>')
        n_rows = len(b['rows'])
        ty = y0 + (h - lh * (n_rows - 1)) / 2 + fs * 0.36
        txt = svg_lines(x0 + padx, ty, b['rows'], 'bl ak-label' + (' blt' if size == 'l' else ''), lh)
        flag = ''
        if code and code in targets:
            fg, _ = fix_flag(x0 + BW - padx - flagw + 10, y0 + h / 2 + 5, reform)
            flag = fg
        note = ''
        if b['notes']:
            note = svg_lines(note_x, y0 + 16 + 14, b['notes'], 'snote', 20)
        marker = ''
        if size == 'l' and stepper and code:
            words = read_aloud_parts(lid)
            if i == 0:
                marker = svg_text(note_x, y0 + 12, f'Start: {words[0][0].lower()}', 'smk', extra=' data-ak-at="0"')
            else:
                marker = svg_text(note_x, y0 + 12, words[i][0], 'smk', extra=f' data-ak-at="{i}"')
            if i == 0:
                note = svg_lines(note_x, y0 + 16 + 14, b['notes'], 'snote', 20)
        if code:
            n = N[code]
            say = f'{code} {n["label"]}. {n["increase_means"]}'
            rel = ' '.join(f'link-{s["id"].lower()}' for s in steps if s['id'] and code in (s['from'], s['to']))
            if interactive:
                parts_svg.append(f'<g class="{cls}" role="button" data-select="var-{code.lower()}" data-node="{code}" '
                                 f'data-name="{e(n["label"])}" data-rel="{rel}" aria-label="{e(say)}" data-say="{e(say)}">'
                                 f'{shape}{txt}{flag}</g>{marker}{note}')
            else:
                parts_svg.append(f'<g class="{cls}" data-node="{code}" data-name="{e(n["label"])}">{shape}{txt}{flag}</g>{note}')
        else:
            parts_svg.append(f'<g class="{cls}">{shape}{txt}</g>')
    # steps
    for i, s in enumerate(steps):
        closing = i == len(steps) - 1
        b0 = boxes[i]
        bottom = b0['y'] + b0['h']
        if not closing:
            top = boxes[i + 1]['y']
            pts = [(ax, bottom + 2), (ax, top - 2)]
            ln = top - bottom - 4
            nt = {'S': 1, 'M': 2, 'L': 3}.get(s['delay'] or '', 0)
            tag_len = TAG[w][0] + TAG[w][1]
            lo_s = 12 + 5 * max(nt - 1, 0) + 3 + tag_len / 2
            hi_s = ln - ARROW[w][0] - 3 - tag_len / 2
            tag_s = max(lo_s, min(hi_s, ln * 0.5))
            lab_y = bottom + (8 if size == 's' else 12)
        else:
            yd = bottom + drop
            pts = [(ax, bottom + 2), (ax, yd), (xr, yd), (xr, first_cy), (x0 - 2, first_cy)]
            tag_s = None
            body_len = path_len(pts)
            tag_s = (drop + (ax - xr) + (yd - first_cy) / 2)
            lab_y = bottom + (8 if size == 's' else 12)
        marks, _ = wire_marks(pts, w, s['evidence'], s['delay'], s['polarity'], conceptual=s['conceptual'], tag_s=tag_s,
                              lit=interactive)
        lbl = label_block(lx, lab_y, blocks[i], s)
        if s['id']:
            l = LK[s['id']]
            say = link_say(s['id'])
            if interactive:
                hit = f'<path class="ak-hit" d="{rounded_d(pts, 0)}"/>'
                parts_svg.append(f'<g class="wire" role="button" data-select="link-{s["id"].lower()}" {link_attrs(s["id"])} '
                                 f'data-rel="var-{l["from"].lower()} var-{l["to"].lower()}" aria-label="{e(say)}" '
                                 f'data-say="{e(say)}">{marks}{hit}{lbl}</g>')
            else:
                parts_svg.append(f'<g class="wire" {link_attrs(s["id"])}>{marks}{lbl}</g>')
        else:
            parts_svg.append(f'<g class="wire concept">{marks}{lbl}</g>')
    # order: boxes and wires interleaved in reading order for the keyboard
    nb = len(boxes)
    ordered = []
    for i in range(nb):
        ordered.append(parts_svg[i])
        ordered.append(parts_svg[nb + i])
    steps_attr = 'sketch' if L['conceptual'] else ' '.join(s['id'] for s in steps)
    al = aria or f'Loop {lid}, {L["plain_name"]}. {read_aloud(lid)}'
    role = (f'role="group" aria-label="{e(al)}" data-ak-roving data-ak-nav="sequence" data-ak-wrap'
            if interactive else f'role="img" aria-label="{e(al)}"')
    cls = 'stack ' + size + (' live' if interactive else '')
    return (f'<svg class="{cls}" data-view="{view or "loop-" + lid.lower()}" data-loop="{lid}" data-steps="{steps_attr}" '
            f'width="{f(W)}" height="{f(H)}" viewBox="0 0 {f(W)} {f(H)}" {role}>{"".join(ordered)}</svg>')


# ------------------------------------------------------------------------------------------------ the circuit (flows)
def flow_say(a, b):
    ks = FLOW[(a, b)]
    return f'{len(ks)} {plural(len(ks), "connection")} from {pname(a)} to {pname(b)}. Open to list them.'


def flow_item(a, b, inner, cls='flow'):
    ks = FLOW[(a, b)]
    say = flow_say(a, b)
    return (f'<g class="{cls}" role="button" data-select="flow-{a.lower()}-{b.lower()}" '
            f'data-rel="{" ".join(f"link-{k.lower()}" for k in ks)}" aria-label="{e(say)}" data-say="{e(say)}">{inner}</g>')


def tri(x, y, up, cls='tri'):
    if up:
        return f'<path class="{cls}" d="M{f(x)} {f(y - 7)}L{f(x + 5)} {f(y + 1)}L{f(x - 5)} {f(y + 1)}Z"/>'
    return f'<path class="{cls}" d="M{f(x - 5)} {f(y - 7)}L{f(x + 5)} {f(y - 7)}L{f(x)} {f(y + 1)}Z"/>'


def outer_cells(pid):
    """For an outer part, its exchanges with each core part: (core part, [(up?, count, from, to)])."""
    rows = {}
    for c in CORE:
        items = []
        into = len(FLOW[(pid, c)])
        outof = len(FLOW[(c, pid)])
        if pid == 'X':
            if into:
                items.append((False, into, pid, c))
        else:
            if into:
                items.append((True, into, pid, c))
            if outof:
                items.append((False, outof, c, pid))
        rows[c] = items
    return rows


def tier_cell(cx, y, items):
    """Counts between an outer part and one part of the circuit, as words: 7 in, 4 out (in = into that part)."""
    parts = []
    for up, n, a, b in items:
        word = 'in' if (a not in CORE) else 'out'
        parts.append((str(n), word, a, b))
    widths = [tw_num(n, 20) + 5 + tw(w, 14) for n, w, _, _ in parts]
    sep = 22
    total = sum(widths) + sep * (len(parts) - 1)
    x = cx - total / 2
    out = []
    for (n, w, a, b), wd in zip(parts, widths):
        inner = (svg_text(x, y, n, 'fcnt', extra=f' data-count="custom:flow-{a.lower()}-{b.lower()}"')
                 + svg_text(x + tw_num(n, 20) + 5, y, w, 'fword')
                 + f'<rect class="ak-hit2" x="{f(x - 6)}" y="{f(y - 22)}" width="{f(wd + 12)}" height="30"/>')
        out.append(flow_item(a, b, inner, 'flow cell'))
        x += wd + sep
    return ''.join(out)


def flows_wide():
    W, cw = 1312, 200
    gap = (W - 5 * cw) / 4
    X = {c: i * (cw + gap) for i, c in enumerate(CORE)}
    box_y, box_h = 72, 84
    out = []
    # outside forces, above: a tier row of counts aligned with the parts they push on
    other = [(p, len(FLOW[('X', p)])) for p in ('EC', 'TC') if FLOW[('X', p)]]
    lab = 'OUTSIDE FORCES'
    out.append(svg_text(0, 15, lab, 'fey'))
    out.append(svg_text(tw(lab, 13, 700) + 13 * 0.06 * len(lab) + 10, 15,
                        e('push in; also ' + ' and '.join(f'{n} into {pname(p)}' for p, n in other)), 'fnote'))
    cells = outer_cells('X')
    for c in CORE:
        out.append(tier_cell(X[c] + cw / 2, 50, cells[c]))
    # core boxes
    for c in CORE:
        x = X[c]
        P = PARTS[c]
        out.append(f'<a href="#reg-{c.lower()}" class="cbox" aria-label="{e(P["plain_name"] + ", " + P["formal_title"] + ". Go to its row in the register.")}">'
                   f'<rect class="cb" x="{f(x)}" y="{box_y}" width="{cw}" height="{box_h}"/>'
                   f'<rect class="cbt" x="{f(x)}" y="{box_y}" width="{cw}" height="3"/>'
                   + svg_text(x + 14, box_y + 36, e(P['plain_name']), 'cbn ak-label')
                   + svg_text(x + 14, box_y + 60, e(P['formal_title']), 'cbf') + '</a>')
    # adjacent flows: forward above (the circuit, in ink), back below (in Stone)
    mid = box_y + box_h / 2
    for i in range(4):
        a, b = CORE[i], CORE[i + 1]
        xa, xb = X[a] + cw + 3, X[b] - 3
        fwd, back = len(FLOW[(a, b)]), len(FLOW[(b, a)])
        if fwd:
            y = mid - 12
            inner = (f'<path class="ak-mark fl3" d="M{f(xa)} {f(y)}L{f(xb - ARROW[3][0])} {f(y)}" stroke-width="3"/>'
                     + head_shape(xb, y, 1, 0, 3, 'lo')
                     + svg_text((xa + xb) / 2, y - 10, str(fwd), 'fcnt big', 'middle', f' data-count="custom:flow-{a.lower()}-{b.lower()}"')
                     + f'<path class="ak-hit" d="M{f(xa)} {f(y - 10)}L{f(xb)} {f(y - 10)}"/>')
            out.append(flow_item(a, b, inner, 'flow main'))
        if back:
            y = mid + 14
            inner = (f'<path class="ak-mark fl2" d="M{f(xb)} {f(y)}L{f(xa + ARROW[2][0])} {f(y)}" stroke-width="2"/>'
                     + head_shape(xa, y, -1, 0, 2, 'lo')
                     + svg_text((xa + xb) / 2, y + 24, str(back), 'fcnt back', 'middle', f' data-count="custom:flow-{b.lower()}-{a.lower()}"')
                     + f'<path class="ak-hit" d="M{f(xa)} {f(y + 8)}L{f(xb)} {f(y + 8)}"/>')
            out.append(flow_item(b, a, inner, 'flow ctx'))
    # the return: Policy feeds back into Wealth
    ry = box_y + box_h + 30
    xe, xw = X['E'] + cw / 2, X['A'] + cw / 2
    ret = [(xe, box_y + box_h + 3), (xe, ry), (xw, ry), (xw, box_y + box_h + 3)]
    body = ret[:-1] + [(xw, box_y + box_h + 3 + ARROW[3][0])]
    n_ret = len(FLOW[('E', 'A')])
    ret_text = ED['opening']['return']
    tx = (xe + xw) / 2
    inner = (f'<path class="ak-mark fl3" d="{rounded_d(body, 12)}" stroke-width="3" fill="none"/>'
             + head_shape(xw, box_y + box_h + 3, 0, -1, 3, 'lo')
             + svg_text(tx - 10, ry + 28, str(n_ret), 'fcnt big', 'end', f' data-count="custom:flow-e-a"')
             + svg_text(tx + 2, ry + 26, e(ret_text), 'fret')
             + f'<path class="ak-hit" d="{rounded_d(ret, 0)}"/>')
    out.append(flow_item('E', 'A', inner, 'flow main ret'))
    # household and technology, below: tier rows of counts
    yy = ry + 74
    for pid in ('EC', 'TC'):
        out.append(f'<path class="tierrule" d="M0 {f(yy - 22)}L{W} {f(yy - 22)}"/>')
        tag_ = pname(pid).upper()
        out.append(svg_text(0, yy, e(tag_), 'fey'))
        other_ = [q for q in ('EC', 'TC') if q != pid][0]
        extra = []
        if FLOW[(pid, other_)]:
            extra.append(f'also {len(FLOW[(pid, other_)])} into {pname(other_)}')
        out.append(svg_text(tw(tag_, 13, 700) + 13 * 0.06 * len(tag_) + 10, yy,
                            e('; '.join(['its connections with each part above'] + extra)), 'fnote'))
        cells = outer_cells(pid)
        for c in CORE:
            if cells[c]:
                out.append(tier_cell(X[c] + cw / 2, yy + 34, cells[c]))
        yy += 74
    H = yy - 30
    al = ('The circuit drawn as five boxes in a row, Wealth, Voice, Elections, Checks and Policy, with the number of '
          'connections each passes to the next, the numbers that run back, and the return from Policy to Wealth. '
          'Rows above and below count the outer parts’ connections into and out of each box. The flows in words follow the drawing.')
    return (f'<svg class="flows wide" data-view="circuit" width="{W}" height="{f(H)}" viewBox="0 0 {W} {f(H)}" role="group" '
            f'aria-label="{e(al)}" data-ak-roving data-ak-nav="spatial">{"".join(out)}</svg>')


def flows_narrow():
    W = 350
    x0, bw, bh, gap = 60, 236, 60, 70
    out = []
    ys = {}
    y = 4
    for c in CORE:
        ys[c] = y
        P = PARTS[c]
        out.append(f'<a href="#reg-{c.lower()}" class="cbox" aria-label="{e(P["plain_name"] + ", " + P["formal_title"] + ". Go to its row in the register.")}">'
                   f'<rect class="cb" x="{x0}" y="{f(y)}" width="{bw}" height="{bh}"/>'
                   f'<rect class="cbt" x="{x0}" y="{f(y)}" width="3" height="{bh}"/>'
                   + svg_text(x0 + 16, y + 27, e(P['plain_name']), 'cbn ak-label')
                   + svg_text(x0 + 16, y + 47, e(P['formal_title']), 'cbf') + '</a>')
        y += bh + gap
    H = y - gap + 8
    fx, bx = x0 + 70, x0 + 160
    for i in range(4):
        a, b = CORE[i], CORE[i + 1]
        ya, yb = ys[a] + bh + 3, ys[b] - 3
        fwd, back = len(FLOW[(a, b)]), len(FLOW[(b, a)])
        if fwd:
            inner = (f'<path class="ak-mark fl3" d="M{fx} {f(ya)}L{fx} {f(yb - ARROW[3][0])}" stroke-width="3"/>'
                     + head_shape(fx, yb, 0, 1, 3, 'lo')
                     + svg_text(fx - 14, (ya + yb) / 2 + 8, str(fwd), 'fcnt big', 'end', f' data-count="custom:flow-{a.lower()}-{b.lower()}"')
                     + f'<path class="ak-hit" d="M{fx - 10} {f(ya)}L{fx - 10} {f(yb)}"/>')
            out.append(flow_item(a, b, inner, 'flow main'))
        if back:
            inner = (f'<path class="ak-mark fl2" d="M{bx} {f(yb)}L{bx} {f(ya + ARROW[2][0])}" stroke-width="2"/>'
                     + head_shape(bx, ya, 0, -1, 2, 'lo')
                     + svg_text(bx + 14, (ya + yb) / 2 + 8, str(back), 'fcnt back', 'start', f' data-count="custom:flow-{b.lower()}-{a.lower()}"')
                     + f'<path class="ak-hit" d="M{bx + 10} {f(ya)}L{bx + 10} {f(yb)}"/>')
            out.append(flow_item(b, a, inner, 'flow ctx'))
    # return on the left
    xl = 24
    ye, yw = ys['E'] + bh / 2, ys['A'] + bh / 2
    pts = [(x0 - 3, ye), (xl, ye), (xl, yw), (x0 - 3, yw)]
    body = pts[:-1] + [(x0 - 3 - ARROW[3][0], yw)]
    n_ret = len(FLOW[('E', 'A')])
    my = (ye + yw) / 2
    inner = (f'<path class="ak-mark fl3" d="{rounded_d(body, 12)}" stroke-width="3" fill="none"/>'
             + head_shape(x0 - 3, yw, 1, 0, 3, 'lo')
             + f'<rect class="halo" x="{xl - 11}" y="{f(my - 17)}" width="22" height="26"/>'
             + svg_text(xl, my + 4, str(n_ret), 'fcnt big', 'middle', ' data-count="custom:flow-e-a"')
             + f'<path class="ak-hit" d="{rounded_d(pts, 0)}"/>')
    out.append(flow_item('E', 'A', inner, 'flow main ret'))
    al = ('The circuit as a column: Wealth, Voice, Elections, Checks and Policy, with the number of connections each '
          'passes down to the next, the numbers that run back up, and the return from Policy to Wealth on the left.')
    return (f'<svg class="flows narrow" data-view="circuit-phone" width="{W}" height="{f(H)}" viewBox="0 0 {W} {f(H)}" '
            f'role="group" aria-label="{e(al)}" data-ak-roving data-ak-nav="sequence">{"".join(out)}</svg>')


def flows_words():
    """The circuit in words: every flow between the eight parts, so nothing rests on the drawing alone."""
    items = []
    for i in range(4):
        a, b = CORE[i], CORE[i + 1]
        back = len(FLOW[(b, a)])
        items.append(f'{pname(a)} to {pname(b)}: {len(FLOW[(a, b)])}; back from {pname(b)} to {pname(a)}: {back if back else "none"}.')
    items.append(f'{pname("E")} back to {pname("A")}, closing the circuit: {len(FLOW[("E", "A")])}.')
    skips = [(a, b) for a in CORE for b in CORE if a != b and abs(CORE.index(a) - CORE.index(b)) > 1 and FLOW[(a, b)]
             and (a, b) != ('E', 'A')]
    if skips:
        items.append('Flows that skip a step: ' + ', '.join(f'{pname(a)} to {pname(b)} {len(FLOW[(a, b)])}' for a, b in skips) + '.')
    for pid in ('X', 'EC', 'TC'):
        ins = [(c, len(FLOW[(pid, c)])) for c in REG_ORDER if c != pid and FLOW[(pid, c)]]
        outs = [(c, len(FLOW[(c, pid)])) for c in REG_ORDER if c != pid and FLOW[(c, pid)]]
        many = pname(pid).endswith('forces')
        s = f'{pname(pid)} {"push" if many else "pushes"} on ' + ', '.join(f'{pname(c)} {n}' for c, n in ins)
        if outs:
            s += f'; {"they are" if many else "it is"} pushed by ' + ', '.join(f'{pname(c)} {n}' for c, n in outs)
        items.append(s + '.')
    return '<ul class="inwords">' + ''.join(f'<li>{e(t)}</li>' for t in items) + '</ul>', skips


# ------------------------------------------------------------------------------------------------ frame pieces
def wordmark(height, master):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    return src.replace('<svg ', f'<svg width="{w:.0f}" height="{height}" role="img" aria-label="Oath &amp; Action" ', 1)


def locator(view):
    rows = []
    for i, pid in enumerate(REG_ORDER):
        loc = ' data-locate="area-c"' if pid == 'C' else ''
        rows.append(f'<rect x="0.5" y="{i * 7 + 0.5}" width="{96 if pid in CORE else 66}" height="4" class="lr"{loc}/>')
    return (f'<a class="locator" href="#overview" aria-label="Overview"><svg data-view="locator-{view}" width="97" height="55" '
            f'viewBox="0 0 97 55" aria-hidden="true" focusable="false">{"".join(rows)}</svg>'
            f'<span>Overview</span></a>')


def chart_open(eyebrow, title, measure, hid, cls=''):
    return (f'<section class="chart {cls}" aria-labelledby="{hid}"><p class="eyebrow">{e(eyebrow)}</p>'
            f'<h2 class="ctitle" id="{hid}">{title}</h2>' + (f'<p class="measure">{measure}</p>' if measure else ''))


def source_line(extra=''):
    return (f'<p class="csource"><span>Source: Who Do They Answer To? Systems Atlas V7, snapshot {SNAP}.{(" " + extra) if extra else ""}</span>'
            f'<span class="credit">Oath &amp; Action</span></p>')


def cnt(key, n, cls='n'):
    return f'<span class="{cls}" data-count="{key}">{n}</span>'


VAR_COUNT_KEY = {'A': 'variables_A', 'B': 'variables_B', 'C': 'variables_C', 'D': 'variables_D', 'E': 'variables_E',
                 'X': 'variables_X', 'TC': 'variables_TC'}


# ------------------------------------------------------------------------------------------------ register
def counts_cell(pid):
    s = STATS[pid]
    vk = VAR_COUNT_KEY.get(pid, f'custom:variables-{pid}')
    rows = [(vk, s['vars'], 'variable'), (f'custom:connections-{pid}', s['conn'], 'connection'),
            (f'custom:loops-{pid}', s['loops'], 'loop'), (f'custom:reforms-{pid}', s['reforms'], 'reform')]
    return '<ul class="counts">' + ''.join(f'<li>{cnt(k, n)}<span class="w">{plural(n, w)}</span></li>' for k, n, w in rows) + '</ul>'


def ev_cell(pid):
    s = STATS[pid]
    lab = f'{pname(pid)}: evidence for {s["conn"]} connections: {mix_words(s["mix"])}.'
    return (f'<div class="evc">{evbar(s["mix"], 176, 16, "evidence-" + pid.lower(), lab)}'
            f'<p class="evt"><span data-count="custom:strong-{pid}">{s["strong"]}</span> of {s["conn"]} documented or well supported</p></div>')


def loop_cell(pid):
    ml = main_loop(pid)
    if not ml:
        return '<div class="lc"><p class="none">No loop runs through this part</p></div>'
    L = LO[ml]
    return (f'<div class="lc"><a class="loopref" href="{loop_href(ml)}" data-loop="{ml}" data-name="{e(L["plain_name"])}">'
            f'<span class="lk">{ml} · {L["kind_word"]}</span><span class="ln">{e(L["plain_name"])}</span></a>'
            f'<p class="lt">{e(L["title"])}</p></div>')


def pushes_words(pid):
    outs = [(c, len(FLOW[(pid, c)])) for c in REG_ORDER if c != pid and FLOW[(pid, c)]]
    ins = [(c, len(FLOW[(c, pid)])) for c in REG_ORDER if c != pid and FLOW[(c, pid)]]

    def lst(xs):
        ws = [f'{pname(c)} {n}' for c, n in xs]
        return ws[0] if len(ws) == 1 else ', '.join(ws[:-1]) + ' and ' + ws[-1]
    out = []
    if outs:
        out.append(f'<p class="pw"><b>Pushes on</b> {e(lst(outs))}</p>')
    else:
        out.append('<p class="pw"><b>Pushes on</b> no other part</p>')
    if ins:
        out.append(f'<p class="pw"><b>Pushed by</b> {e(lst(ins))}</p>')
    else:
        out.append(f'<p class="pw"><b>Pushed by</b> no other part: the model takes it as given</p>')
    if INSIDE[pid]:
        out.append(f'<p class="pw"><b>Inside</b> {len(INSIDE[pid])} {plural(len(INSIDE[pid]), "connection")} between its own variables</p>')
    return ''.join(out)


def fix_card(rid, pid, uid):
    r = RF[rid]
    acts = []
    for t in r['targets']:
        if t in N:
            acts.append(f'<li>{idchip("Variable", t, True)} {e(label(t))}</li>')
        else:
            acts.append(f'<li>{idchip("Connection", t, True)} {e(LK[t]["name"])}</li>')
    eff = ''.join(f'<div><dt>{e(ED["families"][k])}</dt><dd>{e(effect_words(v))}</dd></div>' for k, v in r['effects'].items())
    more = (f'<a class="onp" href="#reform-r01">Read the full profile of R-01</a>' if rid == 'R-01' else
            f'<button type="button" class="onp" data-select="reform-{rid.lower()}" data-reform="{rid}" data-targets="{" ".join(r["targets"])}">'
            f'Read the full profile of {rid}</button>')
    return (f'<section class="fix" data-surface="prussian" aria-labelledby="fx-{uid}"><p class="eyebrow">The fix aimed at it</p>'
            f'<p class="fxid">{idchip("Reform", rid)} <span class="band">{e(r["band"][0].upper() + r["band"][1:])}</span></p>'
            f'<h4 id="fx-{uid}" data-reform="{rid}" data-name="{e(r["title"])}" data-targets="{" ".join(r["targets"])}">{e(r["title"])}</h4>'
            f'<p class="fxs">{e(first_sentences(r["summary"], 1))}</p>'
            f'<p class="fxh">Where it acts</p><ul class="acts">{"".join(acts)}</ul>'
            f'<p class="fxh">Expected effects</p><dl class="eff">{eff}</dl>'
            f'<p class="fxn">Each outcome family is judged on its own and never added together. Most open route: {e(best_route(rid))}.</p>'
            f'{more}</section>')


def unfold(pid):
    P = PARTS[pid]
    ml = main_loop(pid)
    rid = main_reform(pid)
    story = (f'<section class="m-story"><p class="eyebrow">What it is</p><h4 class="chapter">{e(P["chapter"])}</h4>'
             f'<p class="story">{e(P["story"])}</p>{pushes_words(pid)}'
             + (f'<p class="go"><a href="#area-c">Open the Elections page: its conditions, issues and reforms</a></p>' if pid == 'C' else '')
             + '</section>')
    if ml:
        L = LO[ml]
        targ = rid if rid and any(t in set(s['id'] for s in L['steps']) | set(st.get('code') for st in L['stations']) for t in RF[rid]['targets']) else None
        loop = (f'<section class="m-loop"><p class="eyebrow">Its main loop, as a chain</p>'
                f'<h4 class="lname"><a href="{loop_href(ml)}">{e(L["plain_name"])}</a> {idchip("Loop", ml, True)}</h4>'
                f'<p class="lkind">{e(kind_line(ml))}. {e(L["title"])}.</p>'
                + stack_svg(ml, 350, 's', view=f'chain-{pid.lower()}', reform=targ)
                + f'<p class="ra"><span class="eyebrow">Read it aloud</span> {read_aloud(ml, bold=True)}</p>'
                + f'<p class="lstat">{e(weakest_words(ml))} · One turn: {e(L["delay_word"])} · Now {e(direction_words(ml))}</p>'
                + (f'<p class="lstat">{e(disclosure(ml))}</p>' if disclosure(ml) else '')
                + (f'<p class="lstat">The Prussian tab marks where {targ} acts.</p>' if targ else '')
                + '</section>')
    else:
        rows = []
        for c in REG_ORDER:
            if c == pid:
                continue
            ks = FLOW[(pid, c)] + FLOW[(c, pid)]
            if not ks:
                continue
            items = ''.join(f'<li>{glyph(LK[k]["evidence"], LK[k]["polarity"], LK[k]["delay"], LK[k]["type"] == "authority", W=44)}'
                            f'<span>{e(LK[k]["name"])}</span></li>' for k in ks)
            rows.append(f'<p class="grp">With {e(pname(c))} <span>{len(ks)}</span></p><ul class="lks">{items}</ul>')
        loop = (f'<section class="m-loop"><p class="eyebrow">No loop runs through it</p>'
                f'<h4 class="lname">How it reaches the rest of the system</h4>'
                f'<p class="lkind">None of its {STATS[pid]["vars"]} variables sits on one of the 23 loops. These are its connections with other parts.</p>'
                + ''.join(rows) + '</section>')
    fix = fix_card(rid, pid, f'ov-{pid.lower()}') if rid else ''
    return f'<div class="rr-more" id="reg-{pid.lower()}-more"{"" if pid == "C" else " hidden"}>{story}{loop}{fix}</div>'


def part_what(pid):
    """One or two plain sentences on what the part is (DR-29). Where the short text is phrased as a question,
    the story's first sentence describes the part instead."""
    P = PARTS[pid]
    return first_sentences(P['story'], 1) if P['text'].strip().endswith('?') else P['text']


def register_row(i, pid):
    P = PARTS[pid]
    q = P['plain_question'] or P['chapter']
    chips = ''.join(var_chip(c) for c in P['nodes'])
    is_open = pid == 'C'
    return (f'<article class="reg-row{" open" if is_open else ""}" id="reg-{pid.lower()}">'
            f'<div class="rr-head">'
            f'<p class="c-no" aria-hidden="true">{i:02d}</p>'
            f'<div class="c-part"><h3><button type="button" class="rr-toggle" aria-expanded="{str(is_open).lower()}" '
            f'aria-controls="reg-{pid.lower()}-more"><span class="pn" data-part="{pid}" data-name="{e(P["plain_name"])}">{e(P["plain_name"])}</span>'
            f'<span class="pm" aria-hidden="true"></span><span class="ak-vh"> (open or close its story)</span></button></h3>'
            f'<p class="formal" data-part="{pid}" data-name="{e(P["formal_title"])}">{e(P["formal_title"])}</p>'
            f'<p class="question">{e(q)}</p></div>'
            f'<div class="c-covers"><p class="what">{e(part_what(pid))}</p>'
            f'<div class="chips" data-ak-roving data-ak-nav="sequence" role="group" aria-label="{e(P["plain_name"])}: its {len(P["nodes"])} variables">{chips}</div></div>'
            f'<div class="c-counts">{counts_cell(pid)}</div>'
            f'<div class="c-ev">{ev_cell(pid)}</div>'
            f'<div class="c-loop">{loop_cell(pid)}</div>'
            f'</div>{unfold(pid)}</article>')


def register():
    s = STATS[THIN]
    title = f'The evidence is thinnest at {pname(THIN)}, where the circuit closes'
    measure = (f'Eight parts, one per row. Counts: its variables; connections that start or end in it; loops with a step in it; '
               f'reforms aimed at one of its variables or connections. Evidence: the grades of those connections. '
               f'{pname(THIN)}: {s["strong"]} of {s["conn"]} documented or well supported.')
    head = ('<div class="reg-head" aria-hidden="true"><span></span><span>Part</span><span>What it covers, with every variable</span>'
            '<span>Counts</span><span>Evidence behind its connections</span><span>Main loop</span></div>')
    rows = ''.join(register_row(i + 1, pid) for i, pid in enumerate(REG_ORDER))
    none = [pname(p) for p in REG_ORDER if not main_loop(p)]
    notes = (f'<p class="cnote">Main loop: the loop with the most steps in the part; a tie goes to the loop more reforms aim at. '
             f'{", ".join(none[:-1])} and {none[-1]} sit on no loop. The fix in each open row is the first reform its main loop lists, '
             f'or, with no loop, the reform with the most targets in the part. Select a variable to read it; the conditions it connects to light up.</p>')
    return (chart_open('The register', e(title), e(measure), 'h-reg', 'register')
            + head + f'<div class="reg-body">{rows}</div>'
            + '<p class="ak-readout" data-ak-readout>Point at or tab to a variable to see what it connects to.</p>'
            + notes + source_line() + '</section>')


# ------------------------------------------------------------------------------------------------ overview
def key_block(uid='k'):
    sw = ''.join(f'<li>{ev_swatch(g)}<span><b>{gword(g)}</b>: {ggloss(g)}</span></li>' for g in GRADE)
    return (f'<p class="howto">Each row of the register is one part of the system. Read across, then open a row for its story, '
            f'its main loop and the fix aimed at it.</p>'
            f'<p class="kh">Evidence: the bars, and the lines in every loop</p><ul class="keyev">{sw}</ul>'
            f'<p class="kn">Each arrow says <b>raises</b> or <b>lowers</b> beside its sign. {e(acc.SIGN_RULE)} '
            f'<a href="#how-to-read">The shared language, in full</a></p>')


def loop_index():
    groups = []
    for g in ED['loop_groups']:
        title = pname(g['id']) if g['id'] in PARTS else 'Sketched loops'
        items = ''.join(f'<li data-loop="{k}" data-steps="{"sketch" if LO[k]["conceptual"] else " ".join(s["id"] for s in LO[k]["steps"])}">'
                        f'<a href="{loop_href(k)}" data-loop="{k}" data-name="{e(LO[k]["plain_name"])}">{e(LO[k]["plain_name"])}</a>'
                        f'<span>{k} · {LO[k]["kind_word"]}</span></li>' for k in g['loops'])
        groups.append(f'<div class="lig"><h3>{e(title)} <span>{len(g["loops"])}</span></h3><ul>{items}</ul></div>')
    title = f'{nw(N_R, True)} of the {cnt("loops", COUNT["loops"], "nn")} loops feed themselves'
    measure = (f'A loop is a chain of causes that comes back to where it started. Reinforcing loops feed themselves: each turn '
               f'makes the next stronger. The other {nw(N_B)} push back. {N_WITH_REFORM} of {COUNT["loops"]} have a reform aimed at them. '
               f'Grouped by the part where each loop starts.')
    return (chart_open('Every loop', title, e(measure), 'h-li', 'loopindex')
            + f'<div class="li">{"".join(groups)}</div>'
            + f'<p class="go"><a href="#loops">See all {COUNT["loops"]} loops drawn as named chains</a></p>' + source_line() + '</section>')


def bill_section():
    hubs = []
    pws = {p['id']: p for p in ED['pathways']}
    for h in ED['hubs']:
        qs = ''.join(f'<li><button type="button" class="qb" data-select="pw-{pid.lower()}"><span class="qt">{e(pws[pid]["title"])}</span>'
                     f'<span class="qq">{e(pws[pid]["question"])}</span></button></li>' for pid in h['pathways'])
        hubs.append(f'<div class="hub"><h3>{e(h["title"])}</h3><p class="hq">{e(h["question"])}</p>'
                    f'<ul class="qs" data-ak-roving data-ak-nav="sequence">{qs}</ul></div>')
    n_pw = len(ED['pathways'])
    return (f'<section class="bill" aria-labelledby="h-bill"><p class="eyebrow">Start from a question</p>'
            f'<h2 class="sect" id="h-bill">Start from your own bill</h2>'
            f'<p class="deck sm">{nw(n_pw, True)} everyday questions in {nw(len(ED["hubs"]))} groups. Each follows a bill or a notice to the '
            f'parts of the system behind it, and to the offices that can change the rules.</p>'
            f'<div class="hubs">{"".join(hubs)}</div></section>')


def overview():
    words, skips = flows_words()
    deck = ('From the money a household has to the rules officials write, these parts push on one another, and in many '
            'places a chain of causes comes back to where it started. The register below gives each part one row.')
    figs = [('custom:parts', len(PARTS), 'parts'), ('variables', COUNT['variables'], 'variables'),
            ('connections', COUNT['connections'], 'connections'), ('loops', COUNT['loops'], 'loops'),
            ('reforms', COUNT['reforms'], 'reforms')]
    strip = ('<ul class="figs" aria-label="The atlas in numbers">'
             + ''.join(f'<li>{cnt(k, n, "fig")}<span>{w}</span></li>' for k, n, w in figs) + '</ul>')
    circuit = (chart_open('The circuit',
                          f'Each part pushes on the next, and {pname("E")} feeds back into {pname("A")}',
                          e(f'Numbered connections between parts, counted by direction. The main circuit runs in black; counts that run '
                            f'back sit in gray under the arrows. Above and below the row: the outer parts\u2019 connections with each part, '
                            f'where in means into that part and out means from it.'),
                          'h-circ', 'circuit')
               + '<div class="ak-scroll widewrap" role="region" tabindex="0" aria-label="The circuit drawing">' + flows_wide() + '</div>'
               + '<div class="narrowwrap">' + flows_narrow() + '</div>'
               + '<p class="ak-readout" data-ak-readout>Select a count to list its connections.</p>'
               + f'<details class="words"><summary>The flows in words</summary>{words}</details>'
               + f'<div class="words-phone"><p class="kh">The flows in words</p>{words}</div>'
               + source_line() + '</section>')
    return (f'<section class="view" data-view-root="overview" data-crumb="Overview" aria-labelledby="h-ov">'
            f'<div class="crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav></div>'
            f'<div class="lede"><div class="lede-main"><p class="eyebrow kicker">{e(ED["meta"]["title"])} · {e(ED["meta"]["subtitle"])}</p>'
            f'<h1 class="display" id="h-ov" data-ak-heading>Eight parts shape who officials answer to</h1>'
            f'<p class="deck">{deck}</p>{strip}'
            f'<details class="keyfold"><summary>How to read this page</summary>{key_block("p")}</details></div>'
            f'<aside class="key" aria-labelledby="h-key"><p class="eyebrow" id="h-key">How to read this page</p>{key_block()}</aside></div>'
            + circuit + register() + bill_section() + loop_index() + '</section>')


# ------------------------------------------------------------------------------------------------ loop cards
def loop_card(lid, uid, W=310, open_link=False):
    L = LO[lid]
    stat = [weakest_words(lid), f'One turn: {L["delay_word"]}', f'Now {direction_words(lid)}',
            (f'{len(L["reforms"])} {plural(len(L["reforms"]), "reform")} aimed at it' if L['reforms'] else 'No reform aimed at it')]
    dis = disclosure(lid)
    steps_attr = 'sketch' if L['conceptual'] else ' '.join(s['id'] for s in L['steps'])
    go = f'<p class="go"><a href="#loop-r10">Open loop R10 at full size</a></p>' if (open_link and lid == 'R10') else ''
    return (f'<article class="lcard" data-loop="{lid}" data-steps="{steps_attr}" id="{uid}-{lid.lower()}">'
            f'<p class="lck">{idchip("Loop", lid, True)} <span>{e(kind_line(lid))}</span></p>'
            f'<h3><button type="button" class="lcb" data-select="loop-{lid.lower()}" data-loop="{lid}" data-name="{e(L["plain_name"])}">{e(L["plain_name"])}</button></h3>'
            f'<p class="lct">{e(L["title"])}</p>'
            + stack_svg(lid, W, 's', view=f'{uid}-{lid.lower()}')
            + f'<p class="lcr">{read_aloud(lid, bold=True)}</p>'
            + f'<p class="lcs">{" · ".join(e(x) for x in stat)}</p>'
            + (f'<p class="lcd">{e(dis)}</p>' if dis else '') + go + '</article>')


def loops_view():
    groups = []
    for g in ED['loop_groups']:
        ks = g['loops']
        nr = sum(1 for k in ks if LO[k]['type'] == 'R')
        nb = len(ks) - nr
        kinds = ', '.join(x for x in [f'{nr} reinforcing' if nr else '', f'{nb} balancing' if nb else ''] if x)
        if g['id'] in PARTS:
            P = PARTS[g['id']]
            head = (f'<h2 class="gh" data-part="{g["id"]}" data-name="{e(P["plain_name"])}">{e(P["plain_name"])}</h2>'
                    f'<p class="ghs">{e(P["formal_title"])} · {e(P["plain_question"])} · {kinds}</p>')
        else:
            head = (f'<h2 class="gh">Sketched loops</h2><p class="ghs">{e(g["title"].split(", ", 1)[1][0].upper() + g["title"].split(", ", 1)[1][1:])} · {kinds}. '
                    f'Their steps are drawn as hollow lines.</p>')
        cards = ''.join(loop_card(k, 'cat') for k in ks)
        groups.append(f'<section class="lgroup">{head}<div class="lgrid">{cards}</div></section>')
    title = f'{nw(N_R, True)} of the {COUNT["loops"]} loops feed themselves, and {nw(N_B)} push back'
    deck = (f'Each loop is drawn as a chain you read from the top: every box is a variable, every arrow says raises or lowers, '
            f'and the line on the left carries the last step back to the start. Reinforcing loops feed themselves; balancing loops push back. '
            f'The glossary puts it plainly: “{[g["definition"] for g in ED["glossary"] if g["term"].startswith("Reinforcing")][0].split(". ")[1]}”')
    return (f'<section class="view" data-view-root="loops" data-crumb="All loops" data-parent="overview" aria-labelledby="h-loops" hidden>'
            f'<div class="crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>{locator("loops")}</div>'
            f'<div class="lede one"><p class="eyebrow">The loop catalog · '
            f'{cnt("loops_reinforcing", N_R, "nn")} reinforcing, {cnt("loops_balancing", N_B, "nn")} balancing, '
            f'{cnt("loops_sketched", sum(1 for l in LO.values() if l["conceptual"]), "nn")} sketched</p>'
            f'<h1 class="headline" id="h-loops" data-ak-heading>{e(title)}</h1><p class="deck">{e(deck)}</p></div>'
            f'<div data-strip="loops">{"".join(groups)}</div>'
            + source_line() + '</section>')


# ------------------------------------------------------------------------------------------------ area C
def area_c():
    pid = 'C'
    P = PARTS[pid]
    nodes = P['nodes']
    t = touching(pid)
    ins = [k for k in t if PART_OF[LK[k]['to']] == pid and PART_OF[LK[k]['from']] != pid]
    outs = [k for k in t if PART_OF[LK[k]['from']] == pid and PART_OF[LK[k]['to']] != pid]
    inside = INSIDE[pid]
    lps = loops_through(pid)
    iss = [i for i in IS.values() if not i.get('retired') and set(i.get('nodes') or []) & set(nodes)]
    rfs = reforms_at(pid)
    story_first = first_sentences(P['story'], 3)
    headline = 'In most districts, the race that decides the seat is the primary'
    stats = [(f'variables_C', len(nodes), 'variables'), ('custom:connections-C', len(t), 'connections'),
             ('custom:loops-C', len(lps), 'loops run through it'), ('custom:issues-C', len(iss), 'issues tracked'),
             ('custom:reforms-C', len(rfs), 'reforms aimed here')]
    statbox = ''.join(f'<li>{cnt(k, n, "fig")}<span>{w}</span></li>' for k, n, w in stats)
    # 1. variables
    vrows = []
    for code in nodes:
        n = N[code]
        lp = ', '.join(n['loops']) if n['loops'] else 'none'
        n_in = sum(1 for l in LK.values() if l['to'] == code)
        n_out = sum(1 for l in LK.values() if l['from'] == code)
        ic = icon(acc.VARIABLE_ICON[code], f'ac-{code.lower()}', 48)
        vrows.append(f'<li class="vrow"><div class="vi">{ic}</div>'
                     f'<div class="vn"><p class="vc">{idchip("Variable", code, True)}</p>'
                     f'<h3><button type="button" class="vb" data-select="var-{code.lower()}" data-node="{code}" data-name="{e(n["label"])}">{e(n["label"])}</button></h3>'
                     + (f'<p class="vt">{e(n["title"])}</p>' if n['title'] != n['label'] else '') + '</div>'
                     f'<div class="vd"><p>{e(n["description"])}</p></div>'
                     f'<div class="vm"><p>{e(n["increase_means"])}</p></div>'
                     f'<div class="vx"><p><b>{n_in}</b> in, <b>{n_out}</b> out</p><p>Loops: {e(lp)}</p></div></li>')
    first, last = label(nodes[0]), label(nodes[-1])
    sec_vars = (chart_open('Its five conditions',
                           e(f'{pname(pid)} holds {nw(len(nodes))} conditions, from {low(first)} to {low(last)}'),
                           e('Each variable can rise or fall. The line beside it says what a higher value means, so a name '
                             'such as safe seats reads as an amount.'), 'h-cv')
                + '<div class="vhead" aria-hidden="true"><span></span><span>Variable</span><span>What it is</span>'
                  '<span>A higher value means</span><span>Connections and loops</span></div>'
                + f'<ul class="vlist" data-ak-roving data-ak-nav="sequence">{"".join(vrows)}</ul>' + source_line() + '</section>')

    # 2. pushes on / pushed by
    def lrow(k, far):
        l = LK[k]
        fp = PART_OF[l[far]]
        say = link_say(k)
        g = l['evidence']
        rec = '<span class="recq" aria-hidden="true"></span>' if g == 'documented' else ''
        return (f'<li><button type="button" class="lrow" data-select="link-{k.lower()}" {link_attrs(k)} data-name="{e(l["name"])}" '
                f'data-rel="var-{l["from"].lower()} var-{l["to"].lower()}" data-say="{e(say)}">'
                f'{glyph(g, l["polarity"], l["delay"], l["type"] == "authority")}'
                f'<span class="lrt"><span class="lrn">{e(l["name"])}</span>'
                f'<span class="lrf">{l["from"]} {e(label(l["from"]))} {verb(l["polarity"])} {l["to"]} {e(label(l["to"]))}</span>'
                f'<span class="lrg">{rec}{gword(g)} · {DELAY[l["delay"]]}{" · on " + ", ".join(l["loops"]) if l["loops"] else " · on no loop"}</span></span></button></li>')

    def grouped(ks, far, heading):
        by = defaultdict(list)
        for k in ks:
            by[PART_OF[LK[k][far]]].append(k)
        out = [f'<h3 class="colh">{heading} <span>{len(ks)}</span></h3>']
        for c in REG_ORDER:
            if by[c]:
                out.append(f'<p class="grp">{e(pname(c))} <span>{len(by[c])}</span></p>'
                           f'<ul class="lks2">{"".join(lrow(k, far) for k in by[c])}</ul>')
        return ''.join(out)
    sec_links = (chart_open('What pushes on it, and what it pushes on',
                            e(f'{pname(pid)} takes {len(ins)} connections in and sends {len(outs)} out'),
                            e(f'Numbered connections that end or start in {pname(pid)}, grouped by the part at the other end, '
                              f'and the {nw(len(inside))} that run inside it. Each line is drawn in its evidence texture, with ticks for the wait.'),
                            'h-cl')
                 + f'<div class="cols3" data-ak-roving data-ak-nav="sequence"><div>{grouped(ins, "from", "Pushed by")}</div>'
                   f'<div>{grouped(inside, "from", "Inside " + pname(pid)).replace(f"<p class=\"grp\">{pname(pid)} <span>{len(inside)}</span></p>", "")}</div>'
                   f'<div>{grouped(outs, "to", "Pushes on")}</div></div>'
                 + source_line() + '</section>')

    # 3. loops through it
    nr = sum(1 for k in lps if LO[k]['type'] == 'R')
    sec_loops = (chart_open('The loops that run through it',
                            e(f'{nw(len(lps), True)} loops run through {pname(pid)}: {nw(nr)} feed themselves and {nw(len(lps) - nr)} {"pushes" if len(lps) - nr == 1 else "push"} back'),
                            e('Each loop drawn as a chain. Select a loop’s name for its steps, evidence and reforms.'), 'h-cloops')
                 + f'<div class="lgrid">{"".join(loop_card(k, "ac", open_link=True) for k in lps)}</div>'
                 + source_line() + '</section>')

    # 4. issues
    dom = {d['id']: d for d in ED['domains']}
    by = defaultdict(list)
    for i in iss:
        by[i['domain']].append(i)
    order = sorted(by, key=lambda d: (-len(by[d]), d))
    irows = []
    for d in order:
        irows.append(f'<li class="igh"><span>{e(dom[d]["title"])}</span> <span class="n">{len(by[d])}</span></li>')
        for i in by[d]:
            g = gnorm(i['grade'])
            ex = i.get('problem_example') or {}
            ex_txt = (f'<span class="exh">{e(ex["headline"])}</span><span class="exw">{e(", ".join(x for x in (ex.get("where"), ex.get("when")) if x))}</span>'
                      if ex else '<span class="exw">No example on record</span>')
            touch = ' '.join(c for c in i['nodes'] if c in nodes)
            irows.append(f'<li class="irow"><button type="button" class="ib" data-select="issue-{i["id"].lower()}" data-issue="{i["id"]}" '
                         f'data-name="{e(i["title"])}">{e(i["title"])}</button>'
                         f'<span class="itouch">{e(touch)}</span>'
                         f'<span class="igr">{ev_swatch(g, 22, 12)}{gword(g)}</span>'
                         f'<span class="iex">{ex_txt}</span></li>')
    top = order[0]
    sec_issues = (chart_open('Problems tracked here',
                             e(f'{len(iss)} issues are tracked in {pname(pid)}, {len(by[top])} of them about {dom[top]["title"].lower()}'),
                             e(f'Active issue records that touch {nodes[0]} to {nodes[-1]}, grouped by topic, each with a real-world example where '
                               f'the record has one. Select an issue for its mechanism, example, response and tradeoffs.'), 'h-ci')
                  + '<div class="ihead" aria-hidden="true"><span>Issue</span><span>Touches</span><span>Evidence</span><span>Real-world example</span></div>'
                  + f'<ul class="ilist" data-ak-roving data-ak-nav="sequence">{"".join(irows)}</ul>' + source_line() + '</section>')

    # 5. reforms
    rrows = []
    for rid in rfs:
        r = RF[rid]
        acts = ' '.join(r['targets'])
        effs = ''.join(f'<span class="ef{" zero" if str(v).strip() == "0" else ""}"><span class="ak-vh">{e(ED["families"][k])}: </span>{e(effect_words(v))}</span>'
                       for k, v in r['effects'].items())
        name_btn = (f'<button type="button" class="rb" data-select="reform-{rid.lower()}" data-reform="{rid}" data-targets="{" ".join(r["targets"])}" '
                    f'data-name="{e(r["title"])}">{e(r["title"])}</button>')
        page = '<a class="rpage" href="#reform-r01">Full profile</a>' if rid == 'R-01' else ''
        rrows.append(f'<li class="rrow"><span class="rid">{idchip("Reform", rid, True)}</span><span class="rt">{name_btn}{page}</span>'
                     f'<span class="racts">{e(acts)}</span>{effs}<span class="rroute">{e(best_route(rid))}</span></li>')
    sec_reforms = (chart_open('The fixes aimed here',
                              e(f'{nw(len(rfs), True)} reforms aim at {pname(pid)}'),
                              e(f'Reforms that target a variable in {pname(pid)} or a connection that starts or ends there. Expected effects by outcome '
                                f'family are judged one at a time and never added together. The last column gives the most open route and its feasibility.'),
                              'h-cr')
                   + '<div class="rhead" aria-hidden="true"><span>Reform</span><span></span><span>Acts on</span>'
                   + ''.join(f'<span>{e(v)}</span>' for v in ED['families'].values()) + '<span>Most open route</span></div>'
                   + f'<ul class="rlist" data-ak-roving data-ak-nav="sequence">{"".join(rrows)}</ul>' + source_line() + '</section>')
    return (f'<section class="view" data-view-root="area-c" data-crumb="Elections" data-parent="overview" aria-labelledby="h-ac" hidden>'
            f'<div class="crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>{locator("area-c")}</div>'
            f'<div class="lede"><div class="lede-main"><p class="eyebrow" data-part="C" data-name="{e(P["plain_name"])}">Part C · {e(P["plain_name"])} · '
            f'<span data-part="C" data-name="{e(P["formal_title"])}">{e(P["formal_title"])}</span></p>'
            f'<h1 class="headline" id="h-ac" data-ak-heading>{e(headline)}</h1>'
            f'<p class="deck"><b>{e(P["plain_question"])}</b> {e(P["text"])} {e(story_first)}</p></div>'
            f'<aside class="statbox" aria-label="Elections in numbers"><p class="eyebrow">{e(pname(pid))} in numbers</p><ul>{statbox}</ul></aside></div>'
            + sec_vars + sec_links + sec_loops + sec_issues + sec_reforms + '</section>')


# ------------------------------------------------------------------------------------------------ loop R10 and reform R-01
def r10_steps_list(lid):
    L = LO[lid]
    items = []
    for i, s in enumerate(L['steps']):
        l = LK[s['id']]
        keys = f'link-{s["id"].lower()} var-{s["to"].lower()}'
        flag = ' R-01 acts on this step.' if s['id'] in RF['R-01']['targets'] else ''
        wk = ' The weakest step.' if s['id'] in L['weakest'] else ''
        items.append(f'<li data-ak-step-keys="{keys}"><b>{s["id"]}, {e(l["name"])}.</b> {e(step_sentence(s))} '
                     f'{"Plus" if l["polarity"] == "+" else "Minus"}, {verb(l["polarity"])}; {gword(l["evidence"]).lower()}; {DELAY[l["delay"]]}.{wk}{flag}</li>')
    return ''.join(items)


def loop_r10():
    lid = 'R10'
    L = LO[lid]
    end = (f'The loop is back where it started, so it {L["kind_gloss"]}: {L["kind_word"].lower()}. '
           f'Its weakest step is {L["weakest"][0]}, graded {gword(LK[L["weakest"][0]]["evidence"]).lower()}.')
    idle = (f'Start at {L["stations"][0]["code"]}, {label(L["stations"][0]["code"])}, and suppose it rises. '
            f'Press Play, or Next step to follow one numbered link at a time.')
    wide = stack_svg(lid, 760, 'l', interactive=True, view='loop-r10', reform='R-01', notes=True, stepper=True)
    narrow = stack_svg(lid, 350, 's', interactive=True, view='loop-r10-phone', reform='R-01')
    reform_rows = []
    for rid in L['reforms']:
        r = RF[rid]
        tg = ', '.join(f'{t} {label(t)}' if t in N else f'{t} {LK[t]["name"]}' for t in r['targets'])
        reform_rows.append(f'<li><button type="button" class="rb" data-select="reform-{rid.lower()}" data-reform="{rid}" '
                           f'data-targets="{" ".join(r["targets"])}" data-name="{e(r["title"])}">{e(r["title"])}</button>'
                           f' <span class="rid2">{rid}</span><span class="rtg">Acts on {e(tg)}</span></li>')
    case_box = (f'<div><h3 class="sh">A real case</h3><p>{e(L["case"])}</p></div>')
    measure = (f'{L["plain_name"]}. {nw(len(L["steps"]), True)} steps, each a numbered connection. One turn takes {L["delay_word"]}. '
               f'Now {direction_words(lid)}: {L["reference_mode"]}.')
    return (f'<section class="view" data-view-root="loop-r10" data-crumb="Loop R10" data-parent="area-c" data-ak-reform="reform-r-01" '
            f'data-red-ok aria-labelledby="h-r10" hidden>'
            f'<div class="crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>{locator("loop-r10")}</div>'
            f'<div class="lede one"><p class="eyebrow">{idchip("Loop", lid, True)} {e(kind_line(lid))}</p>'
            f'<h1 class="headline" id="h-r10" data-ak-heading data-loop="{lid}" data-name="{e(L["title"])}">{e(L["title"])}</h1>'
            f'<p class="measure big">{e(measure)}</p></div>'
            f'<div class="r10grid"><figure class="r10fig chart" aria-labelledby="h-r10d">'
            f'<p class="eyebrow">The loop, step by step</p><h2 class="ctitle" id="h-r10d">Read it from the top: each step raises or lowers the next</h2>'
            f'<p class="measure">Boxes are variables. Each arrow carries its sign tag, its evidence texture and one tick per band of delay. '
            f'Red marks the three points where reform R-01 acts; the Prussian tab names it.</p>'
            f'<div class="r10wide">{wide}</div><div class="r10narrow">{narrow}</div>'
            f'<p class="ak-readout" data-ak-readout>Select a box or an arrow to read it.</p>' + source_line() + '</figure>'
            f'<div class="r10side"><p class="eyebrow">Read it aloud</p><p class="ra-big">{read_aloud(lid, bold=True)}</p>'
            f'<p class="eyebrow">In the model’s words</p><blockquote class="quote">“{e(L["how_to_read"])}”</blockquote>'
            f'<section class="stepper" data-ak-stepper data-ak-hold="3200" data-ak-end="{e(end)}" aria-labelledby="h-steps">'
            f'<h2 class="sh" id="h-steps">Follow one change around the loop</h2>'
            f'<div class="sbtns"><button type="button" class="ak-btn" data-ak-step="play">Play</button>'
            f'<button type="button" class="ak-btn" data-ak-step="prev">Previous step</button>'
            f'<button type="button" class="ak-btn" data-ak-step="next">Next step</button>'
            f'<button type="button" class="ak-btn" data-ak-step="reset">Reset</button></div>'
            f'<p class="sstatus" data-ak-step-status aria-live="polite">{e(idle)}</p>'
            f'<ol class="slist" data-ak-step-list>{r10_steps_list(lid)}</ol></section></div></div>'
            f'<div class="r10notes">'
            f'<div><h3 class="sh">What the evidence says</h3><p>{e(L["evidence_summary"])}</p></div>'
            f'<div><h3 class="sh">Keep in mind</h3><p>{e(L["qualification"])}</p><p class="small">{e(acc.SIGN_RULE)}</p></div>'
            f'{case_box}</div>'
            + chart_open('Where reforms act on this loop', e(f'{nw(len(L["reforms"]), True)} reforms aim at the {L["plain_name"].lower()}'),
                         e('Select a reform to move the red to the points where it acts. R-01 is shown by default.'), 'h-r10r')
            + f'<ul class="r10reforms" data-ak-roving data-ak-nav="sequence">{"".join(reform_rows)}</ul>'
            + f'<p class="go"><a href="#reform-r01">Read the full profile of R-01</a></p>' + source_line() + '</section>'
            + '</section>')


def effect_mark(code):
    """A categorical mark for one family's expected effect: squares by size either side of a center line. Never summed."""
    m = re.match(r'^([+-][LMS]|0|\?)', str(code).strip())
    c = m.group(1)
    W, cx = 92, 46
    out = f'<path class="emc" d="M{cx} 0L{cx} 14"/>'
    if c == '?':
        out += f'<text x="{cx + 8}" y="12" class="emq">?</text>'
    elif c != '0':
        k = {'S': 1, 'M': 2, 'L': 3}[c[1]]
        for i in range(k):
            x = cx + 5 + i * 13 if c[0] == '+' else cx - 15 - i * 13
            out += f'<rect class="ems" x="{x}" y="2" width="10" height="10"/>'
    return (f'<svg class="emark" data-view="key" width="{W}" height="14" viewBox="0 0 {W} 14" aria-hidden="true" '
            f'focusable="false">{out}</svg>')


def feas_mark(level):
    order = ['very low', 'low', 'medium', 'high']
    k = order.index(level) + 1
    cells = ''.join(f'<rect x="{i * 12}" y="0" width="10" height="10" class="{"fon" if i < k else "foff"}"/>' for i in range(4))
    return f'<svg class="feas" data-view="key" width="46" height="10" viewBox="0 0 46 10" aria-hidden="true" focusable="false">{cells}</svg>'


def reform_r01():
    rid = 'R-01'
    r = RF[rid]
    L = LO['R10']
    eff_rows = ''.join(f'<tr><th scope="row">{e(ED["families"][k])}</th><td>{effect_mark(v)}</td><td>{e(effect_words(v))}</td></tr>' for k, v in r['effects'].items())
    route_rows = ''.join(
        f'<tr><th scope="row">{e(ED["route_names"][x["route"]])}</th><td data-label="Who decides">{e(x["who"])}</td>'
        f'<td data-label="Feasibility"><span class="fw">{feas_mark(x["feasibility"])}{e(x["feasibility"][0].upper() + x["feasibility"][1:])}</span></td>'
        f'<td data-label="Note">{e(x["note"] or "None in V7")}</td><td data-label="Last checked">{e(date_words(x["checked"])) if x["checked"] else "No check date in V7"}</td></tr>'
        for x in r['routes'])
    feas_key = ''.join(f'<li>{feas_mark(k)}<span><b>{e(k[0].upper() + k[1:])}</b>: {e(v)}</span></li>' for k, v in ED['feasibility_scale'].items())
    wide = stack_svg('R10', 760, 'l', interactive=True, view='reform-r01-loop', reform=rid, notes=True)
    narrow = stack_svg('R10', 350, 's', interactive=True, view='reform-r01-loop-phone', reform=rid)
    others = ', '.join(f'{k} ({LO[k]["plain_name"].lower()})' for k in r['loops'] if k != 'R10')
    pe, re_ = r['problem_evidence'], r['remedy_evidence']

    def ev_card(title, ev):
        g = ev['grade']
        return (f'<div class="evcard"><h3 class="sh">{title}</h3><p class="evg">{glyph(g, "+", None)}'
                f'<span><b>{gword(g)}</b>: {ggloss(g)}</span></p><p>{e(ev["text"])}</p></div>')
    status = r['status']
    tg = ', '.join(f'{t} {label(t)}' if t in N else f'{t} {LK[t]["name"]}' for t in r['targets'])
    succ = ''.join(f'<li>{e(x)}</li>' for x in r['success_measures'])
    ricon = icon('R-01', 'rf-r01', 64)
    return (f'<section class="view" data-view-root="reform-r01" data-crumb="Reform R-01" data-parent="overview" data-ak-reform="reform-r-01" '
            f'data-red-ok aria-labelledby="h-rf" hidden>'
            f'<div class="crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>{locator("reform-r01")}</div>'
            f'<div class="lede one rflede"><div class="rficon">{ricon}</div><div><p class="eyebrow">{idchip("Reform", rid, True)} '
            f'{e(r["band"][0].upper() + r["band"][1:])} · {e(r["short"])}</p>'
            f'<h1 class="headline" id="h-rf" data-ak-heading data-reform="{rid}" data-name="{e(r["title"])}" data-targets="{" ".join(r["targets"])}">{e(r["title"])}</h1>'
            f'<p class="deck">{e(first_sentences(r["summary"], 2))}</p><p class="nopos">{e(NO_POSITION)}</p></div></div>'
            f'<div class="r10grid"><figure class="r10fig chart" aria-labelledby="h-rfw">'
            f'<p class="eyebrow">Where it acts</p><h2 class="ctitle" id="h-rfw">{e(f"R-01 acts on {nw(len(r["targets"]))} points of the {L["plain_name"].lower()}")}</h2>'
            f'<p class="measure">{e(f"Loop R10, {L["title"]}. Red marks the targets: {tg}. It also sits on {others}.")}</p>'
            f'<div class="r10wide">{wide}</div><div class="r10narrow">{narrow}</div>'
            f'<p class="ak-readout" data-ak-readout>Select a box or an arrow to read it.</p>' + source_line() + '</figure>'
            f'<div class="r10side"><h2 class="sh first">The problem it answers</h2><p>{e(L["summary"])}</p>'
            f'<p><a href="#loop-r10">Open loop R10, step by step</a></p>'
            f'<h2 class="sh">What it changes</h2><p>{e(r["what_it_changes"])}</p></div></div>'
            + chart_open('Effects by outcome family', 'Four families, each judged on its own',
                         e(f'Expected direction of change in each family. The families use different units and are never added together. '
                           f'Confidence: {r["effects_confidence"]}.'), 'h-rfe', 'half')
            + f'<table class="rtab eff"><thead><tr><th scope="col">Family</th><th scope="col"><span class="ak-vh">Mark</span></th><th scope="col">Expected effect</th></tr></thead><tbody>{eff_rows}</tbody></table>'
            + '<p class="small">Each square is one step of size: small, moderate, large. Squares right of the center line mean a rise; left of it, a fall. No squares: no expected effect.</p>'
            + source_line() + '</section>'
            + chart_open('Routes to adoption', e(f'{nw(len(r["routes"]), True)} routes, from a state ballot to Congress'),
                         e('Who could adopt it, how open each route is for 2026 to 2030, and when the Atlas last checked.'), 'h-rfr')
            + f'<table class="rtab routes"><thead><tr><th scope="col">Route</th><th scope="col">Who decides</th><th scope="col">Feasibility</th>'
              f'<th scope="col">Note</th><th scope="col">Last checked</th></tr></thead><tbody>{route_rows}</tbody></table>'
            + f'<ul class="feaskey">{feas_key}</ul>' + source_line() + '</section>'
            + f'<div class="evgrid">{ev_card("Problem evidence", pe)}{ev_card("Remedy evidence", re_)}</div>'
            + f'<div class="r10notes"><div><h3 class="sh">Tradeoffs</h3><p>{e(r["tradeoffs"])}</p></div>'
              f'<div><h3 class="sh">How it could fail</h3><p>{e(r["failure_risks"])}</p></div>'
              f'<div><h3 class="sh">How to judge it</h3><ul class="succ">{succ}</ul></div></div>'
            + f'<section class="status" aria-labelledby="h-rfs"><p class="eyebrow">Status</p><h2 class="sh" id="h-rfs">Where it stands, as of {e(date_words(status["checked"]))}</h2>'
              f'<p>{e(status["text"])}</p><p class="disc"><b>{e(DISCLOSURE[0].split(":", 1)[0])}:</b>{e(DISCLOSURE[0].split(":", 1)[1])}</p>'
              f'<p class="small">{e(NO_POSITION)} Source of the disclosure: Atlas V7, \u201c{e(DISCLOSURE[1])}\u201d.</p></section>'
            + source_line() + '</section>')


# ------------------------------------------------------------------------------------------------ how to read
def specimen(lid, W=300, sign_note=True):
    l = LK[lid]
    H = 64
    pts = [(10, 40), (W - 10, 40)]
    marks, _ = wire_marks(pts, 3, l['evidence'], l['delay'], l['polarity'], tag_s=(W - 20) * 0.55, lit=False)
    return marks


def how_to_read():
    def spec_line(lid, W=350):
        l = LK[lid]
        ra, rb = wrap(label(l['from']), 96, 15, 600), wrap(label(l['to']), 96, 15, 600)
        n = max(len(ra), len(rb))
        H = max(74, 40 + 18 * n)
        ly = 34 + 9 * (n - 1)
        marks, _ = wire_marks([(104, ly), (W - 104, ly)], 3, l['evidence'], l['delay'], l['polarity'], tag_s=(W - 208) * 0.5, lit=False)
        a = svg_lines(0, ly + 5 - 9 * (len(ra) - 1), ra, 'bl2', 18)
        b = svg_lines(W - 96, ly + 5 - 9 * (len(rb) - 1), rb, 'bl2', 18)
        cap = svg_text(W / 2, ly - 16, f'{verb(l["polarity"])}', 'swv2', 'middle')
        return (f'<svg class="spec" data-view="how-{lid.lower()}" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
                f'aria-label="{e(link_say(lid))}"><g {link_attrs(lid)}>{marks}</g>{a}{b}{cap}</svg>')
    sign_ex = [k for k in ('L08', 'L25') if k in LK]
    grades = Counter(l['evidence'] for l in LK.values())
    ex_by_grade = {}
    for g in GRADE:
        ex_by_grade[g] = next(k for k in ('L08', 'L25', 'L53', 'L47', 'T01', 'L01', 'L02', 'L46', 'L18') if LK[k]['evidence'] == g)
    tex_rows = ''.join(
        f'<li><span class="tg">{glyph(g, "+", None, W=72, view="how-tex")}</span><span class="tw"><b>{gword(g)}</b>: {ggloss(g)}</span>'
        f'<span class="tn"><span data-count="custom:grade-{g}">{grades[g]}</span> of {COUNT["connections"]} connections</span>'
        f'<span class="te">For example, {ex_by_grade[g]}: {e(LK[ex_by_grade[g]]["name"])}</span></li>' for g in GRADE)
    tex_rows += (f'<li><span class="tg">{glyph(None, "+", None, conceptual=True, W=72, view="how-tex")}</span><span class="tw"><b>Conceptual</b>: '
                 f'a step with no numbered connection</span><span class="tn">{sum(1 for l in LO.values() if l["conceptual"])} sketched loops</span>'
                 f'<span class="te">B2, B3 and R9 are drawn this way.</span></li>')
    n_auth = sum(1 for l in LK.values() if l['type'] == 'authority')
    tex_rows += (f'<li><span class="tg">{glyph("documented", None, None, authority=True, W=72, view="how-tex")}</span><span class="tw"><b>Decides</b>: '
                 f'an authority connection</span><span class="tn"><span data-count="authority_connections">{n_auth}</span> connections</span>'
                 f'<span class="te">It says who holds the power, carries no sign and never closes a loop.</span></li>')
    delays = Counter(l['delay'] for l in LK.values())
    tick_ex = {d: next(k for k in ('L08', 'L53', 'L03', 'L25', 'L42') if LK[k]['delay'] == d) for d in ('S', 'M', 'L')}
    tick_rows = ''.join(f'<li><span class="tg">{glyph("documented" if d != "L" else "well-supported", "+", d, W=72, view="how-ticks")}</span>'
                        f'<span class="tw"><b>{nw({"S": 1, "M": 2, "L": 3}[d], True)} {plural({"S": 1, "M": 2, "L": 3}[d], "tick")}</b>: {DELAY[d]}</span>'
                        f'<span class="tn"><span data-count="custom:delay-{d}">{delays[d]}</span> connections</span>'
                        f'<span class="te">For example, {tick_ex[d]}: {e(LK[tick_ex[d]]["name"])}</span></li>' for d in ('S', 'M', 'L'))
    r8 = loop_card('R8', 'how', W=300)
    b4 = loop_card('B4', 'how', W=300)
    color_rows = [
        ('ch', 'Charcoal', 'The system: every variable, arrow and count, and the route a headline names.'),
        ('st', 'Stone', 'Context: counts that run back, rules and hairlines.'),
        ('pr', 'Prussian', 'The fix layer: reform cards and the tab that names a reform where it acts.'),
        ('rd', 'Pillar Red', 'Where a reform acts, on the loop and reform pages only. One job per view, never on Prussian.'),
    ]
    colors = ''.join(f'<li><span class="sw2 {c}"{" data-red=\"working\" data-red-job=\"palette swatch\"" if c == "rd" else ""}></span>'
                     f'<span><b>{n}</b>: {t}</span></li>' for c, n, t in color_rows)
    sec = lambda no, title, body, aside='': (f'<section class="htr"><p class="htn">{no}</p><div class="htb"><h2 class="sect">{title}</h2>{body}</div>'
                                             f'<div class="hta">{aside}</div></section>')
    s1 = sec(1, 'The tip is the effect',
             f'<p>An arrow runs from a cause to its effect. The word beside it says <b>raises</b> or <b>lowers</b>, and the tag on the line '
             f'carries the sign. {e(acc.SIGN_RULE)}</p><p class="small">The tag points the way the step runs. A plus means the two move '
             f'together; a minus means they move apart.</p>',
             spec_line('L08') + spec_line('L25'))
    s2 = sec(2, 'Texture is the evidence', f'<p>Every connection carries a grade for how strong its evidence is, and the grade sets the line’s '
             f'texture. Solid lines rest on the public record or strong research; broken lines mark weaker evidence. The register’s '
             f'evidence bars fill each grade with its own texture, so the mix reads in gray as well as in color.</p>',
             f'<ul class="texlist">{tex_rows}</ul>')
    s3 = sec(3, 'Ticks count the wait', '<p>Small ticks just after the start of a line count how long the effect takes to arrive.</p>',
             f'<ul class="texlist">{tick_rows}</ul>')
    s4 = sec(4, 'Loops have a character',
             f'<p>Follow a loop around and count the minus signs. An even count, or none, makes it reinforcing: it feeds itself. An odd count '
             f'makes it balancing: it pushes back. {nw(N_R, True)} of the {COUNT["loops"]} loops feed themselves. “'
             f'{[g["definition"] for g in ED["glossary"] if g["term"].startswith("Reinforcing")][0].split(". ")[1]}”</p>',
             f'<div class="lgrid two">{r8}{b4}</div>')
    s5 = sec(5, 'Color is the layer', '<p>Few inks, each with one job. Labels and patterns carry every meaning as well, so a page '
             'printed in gray loses nothing.</p>', f'<ul class="colors">{colors}</ul>')
    return (f'<section class="view" data-view-root="how-to-read" data-crumb="How to read" data-parent="overview" aria-labelledby="h-htr" hidden>'
            f'<div class="crumbrow"><nav class="ak-crumbs" data-ak-crumbs aria-label="Breadcrumb"></nav>{locator("how-to-read")}</div>'
            f'<div class="lede one"><p class="eyebrow">The shared language</p>'
            f'<h1 class="headline" id="h-htr" data-ak-heading>Every line says what happens next, and how sure we are</h1>'
            f'<p class="deck">Five rules carry every drawing in this atlas. Learn them once and every loop, chain and register row reads the same way.</p></div>'
            + s1 + s2 + s3 + s4 + s5 + source_line() + '</section>')


# ------------------------------------------------------------------------------------------------ panel templates
SRC = f'<p class="src">Atlas V7, snapshot {SNAP}.</p>'


def tpl(key, kind, title, body):
    return f'<template data-detail="{key}" data-kind="{e(kind)}" data-title="{e(title)}">{body}{SRC}</template>'


def link_li(k, show_from=True):
    l = LK[k]
    return (f'<li>{glyph(l["evidence"], l["polarity"], l["delay"], l["type"] == "authority", W=64, view="panel")}'
            f'<span><b>{k}</b> {e(l["name"])}<span class="pm2">{verb(l["polarity"])} · {gword(l["evidence"]).lower()} · {DELAY[l["delay"]]}</span></span></li>')


def reforms_aiming(code):
    return [k for k in sorted(RF) if code in RF[k]['targets'] or any(t in LK and code in (LK[t]['from'], LK[t]['to']) for t in RF[k]['targets'])]


def tpl_var(code):
    n = N[code]
    outs = [k for k, l in LK.items() if l['from'] == code]
    ins = [k for k, l in LK.items() if l['to'] == code]

    def grouped(ks, end):
        by = defaultdict(list)
        for k in ks:
            by[PART_OF[LK[k][end]]].append(k)
        return ''.join(f'<p class="pg">{e(pname(c))}</p><ul class="pl">{"".join(link_li(k) for k in by[c])}</ul>' for c in REG_ORDER if by[c])
    lps = ''.join(f'<li><a href="{loop_href(k)}">{k} {e(LO[k]["plain_name"])}</a></li>' for k in n['loops']) or '<li>None</li>'
    rfs = reforms_aiming(code)
    rfl = ''.join(f'<li><b>{k}</b> {e(RF[k]["title"])}</li>' for k in rfs[:12]) or '<li>None</li>'
    part = PARTS[PART_OF[code]]
    nxt = '<p class="next"><a href="#area-c">Open the Elections page</a></p>' if PART_OF[code] == 'C' else ''
    body = ((f'<p class="lead">{e(n["title"])}</p>' if n['title'] != n['label'] else '') + f'<p>{e(n["description"])}</p><p><b>{e(n["increase_means"])}</b></p>'
            f'<p>{e(n["why"] or "")}</p><dl><dt>Part</dt><dd>{e(part["plain_name"])} ({e(part["formal_title"])})</dd>'
            f'<dt>Kind</dt><dd>{e(n["kind_plain"] or n["type"])}</dd><dt>Measured by</dt><dd>{e(n["indicator"] or "Not given")}</dd></dl>'
            f'<h3>Pushes on ({len(outs)})</h3>{grouped(outs, "to") or "<p>Nothing in the model.</p>"}'
            f'<h3>Pushed by ({len(ins)})</h3>{grouped(ins, "from") or "<p>Nothing in the model.</p>"}'
            f'<h3>Loops through it</h3><ul class="pl">{lps}</ul><h3>Reforms aimed at it or its connections ({len(rfs)})</h3><ul class="pl">{rfl}</ul>{nxt}')
    return tpl(f'var-{code.lower()}', f'Variable {code}', n['label'], body)


def tpl_link(k):
    l = LK[k]
    lps = ', '.join(l['loops']) if l['loops'] else 'None'
    body = (f'<p class="lead">{e(l["plain"])}</p><dl><dt>From</dt><dd>{l["from"]} {e(label(l["from"]))}</dd>'
            f'<dt>To</dt><dd>{l["to"]} {e(label(l["to"]))}</dd><dt>Sign</dt><dd>{e(sign_words(l["polarity"]))}</dd>'
            f'<dt>Type</dt><dd>{e(l["type"])}</dd><dt>Delay</dt><dd>{DELAY[l["delay"]]}</dd>'
            f'<dt>Evidence</dt><dd>{gword(l["evidence"])}: {ggloss(l["evidence"])}</dd><dt>Loops</dt><dd>{e(lps)}</dd></dl>'
            f'<p>{e(l["sign_meaning"] or "")}</p>'
            + (f'<h3>Keep in mind</h3><p>{e(l["qualification"])}</p>' if l.get('qualification') else ''))
    return tpl(f'link-{k.lower()}', f'Connection {k}', l['name'], body)


def tpl_loop(lid):
    L = LO[lid]
    steps = ''.join(f'<li>{(s["id"] + ", " + e(LK[s["id"]]["name"]) + ". ") if s["id"] else ""}{e(step_sentence(s))} '
                    f'{(gword(s["evidence"]) + ", " + DELAY[s["delay"]]) if s["evidence"] else "Conceptual step."}</li>' for s in L['steps'])
    rfl = ''.join(f'<li><b>{k}</b> {e(RF[k]["title"])}: acts on {", ".join(RF[k]["targets"])}</li>' for k in L['reforms']) or '<li>None in the model</li>'
    nxt = '<p class="next"><a href="#loop-r10">Open loop R10 at full size</a></p>' if lid == 'R10' else ''
    body = (f'<p class="lead">{e(L["title"])}</p><p><b>{e(kind_line(lid))}.</b> {e(L["summary"])}</p>'
            f'<h3>Read it aloud</h3><p>{read_aloud(lid, True)}</p><h3>Steps</h3><ol>{steps}</ol>'
            f'<dl><dt>Weakest</dt><dd>{e(weakest_words(lid))}</dd><dt>Closure</dt><dd>{e(L["closure"])}</dd>'
            f'<dt>One turn</dt><dd>{e(L["delay_word"])}</dd><dt>Now</dt><dd>{e(direction_words(lid))}: {e(L["reference_mode"])}</dd></dl>'
            f'<h3>Reforms aimed at it</h3><ul>{rfl}</ul><h3>Keep in mind</h3><p>{e(L["qualification"])}</p>'
            + (f'<p>{e(disclosure(lid))}</p>' if disclosure(lid) else '') + nxt)
    return tpl(f'loop-{lid.lower()}', f'Loop {lid}', L['plain_name'], body)


def tpl_reform(rid):
    r = RF[rid]
    tg = ''.join(f'<li><b>{t}</b> {e(label(t)) if t in N else e(LK[t]["name"])}</li>' for t in r['targets'])
    eff = ''.join(f'<dt>{e(ED["families"][k])}</dt><dd>{e(effect_words(v))}</dd>' for k, v in r['effects'].items())
    routes = ''.join(f'<li><b>{e(ED["route_names"][x["route"]])}</b>, {e(x["feasibility"])}: {e(x["who"])}. '
                     f'{"Checked " + date_words(x["checked"]) if x["checked"] else "No check date in V7"}.</li>' for x in r['routes'])
    nxt = '<p class="next"><a href="#reform-r01">Open the full profile of R-01</a></p>' if rid == 'R-01' else ''
    body = (f'<p class="lead">{e(r["summary"])}</p><h3>What it changes</h3><p>{e(r["what_it_changes"])}</p>'
            f'<h3>Where it acts</h3><ul>{tg}</ul><h3>Expected effects, never added together</h3><dl>{eff}</dl>'
            f'<p>Confidence: {e(r["effects_confidence"])}.</p><dl><dt>Problem evidence</dt><dd>{gword(r["problem_evidence"]["grade"])}</dd>'
            f'<dt>Remedy evidence</dt><dd>{gword(r["remedy_evidence"]["grade"])}</dd></dl><h3>Routes</h3><ul>{routes}</ul>'
            f'<h3>Status</h3><p>{e(r["status"]["text"])}</p>' + nxt)
    return tpl(f'reform-{rid.lower()}', f'Reform {rid}', r['title'], body)


def tpl_issue(iid):
    i = IS[iid]
    g = gnorm(i['grade'])

    def ex(x, kind):
        if not x:
            return ''
        src = x.get('source') or {}
        s = ', '.join(v for v in (src.get('title'), src.get('publisher'), str(src.get('year') or '')) if v)
        return (f'<h3>{kind}</h3><p><b>{e(x["headline"])}</b></p><p>{e(x["text"])}</p>'
                + (f'<p>{e(x["result"])}</p>' if x.get('result') else '')
                + f'<p class="small">{e(", ".join(v for v in (x.get("where"), x.get("when")) if v))}{". Source: " + e(s) if s else ""}</p>')
    aimed = ''.join(f'<li><b>{a["id"]}</b> {e(RF[a["id"]]["title"])}: {e(a["why"])}</li>' for a in (i.get('aimed_reforms') or []) if a['id'] in RF)
    body = (f'<p class="lead">{e(i["summary"])}</p><dl><dt>Evidence</dt><dd>{gword(g)}: {ggloss(g)}</dd>'
            f'<dt>Touches</dt><dd>{", ".join(i["nodes"])}</dd><dt>Loops</dt><dd>{", ".join(i["loops"]) or "None"}</dd></dl>'
            f'<h3>How it works</h3><p>{e(i["mechanism"])}</p>' + ex(i.get('problem_example'), 'A real-world example')
            + ex(i.get('fix_example'), 'A fix that was tried')
            + f'<h3>A response</h3><p>{e(i["response"])}</p><dl><dt>Who acts</dt><dd>{e(i["actor"])}</dd></dl>'
            f'<h3>Tradeoffs</h3><p>{e(i["tradeoff"])}</p><h3>How to judge success</h3><p>{e(i["success_measure"])}</p>'
            + (f'<h3>Reforms aimed at it</h3><ul>{aimed}</ul>' if aimed else ''))
    return tpl(f'issue-{iid.lower()}', f'Issue {iid}', i['title'], body)


def tpl_pathway(pid):
    p = next(x for x in ED['pathways'] if x['id'] == pid)
    refs = p['model_refs']
    parts = []
    for n in refs.get('nodes', []):
        if n in PART_OF and PART_OF[n] not in parts:
            parts.append(PART_OF[n])
    vars_ = ', '.join(f'{n} {label(n)}' for n in refs.get('nodes', []) if n in N)
    lps = ''.join(f'<li><a href="{loop_href(k)}">{k} {e(LO[k]["plain_name"])}</a></li>' for k in refs.get('loops', []) if k in LO) or '<li>None</li>'
    rfl = ''.join(f'<li><b>{k}</b> {e(RF[k]["title"])}' + (' <a href="#reform-r01">Full profile</a>' if k == 'R-01' else '') + '</li>'
                  for k in refs.get('reforms', []) if k in RF) or '<li>None</li>'
    nxt = '<p class="next"><a href="#area-c">Open the Elections page</a></p>' if 'C' in parts else ''
    body = (f'<p class="lead">{e(p["short_answer"])}</p><h3>Where it sits in the atlas</h3>'
            f'<p><b>Parts:</b> {e(", ".join(pname(x) for x in parts))}.</p><p><b>Variables:</b> {e(vars_)}.</p>'
            f'<h3>Loops</h3><ul>{lps}</ul><h3>Reforms</h3><ul>{rfl}</ul>'
            f'<p>{len(refs.get("issues", []))} issue records follow this question.</p>{nxt}')
    return tpl(f'pw-{pid.lower()}', f'Question · {p["title"]}', p['question'], body)


def tpl_flow(a, b):
    ks = FLOW[(a, b)]
    body = (f'<p class="lead">{len(ks)} numbered {plural(len(ks), "connection")} run from {e(pname(a))} ({e(PARTS[a]["formal_title"])}) '
            f'to {e(pname(b))} ({e(PARTS[b]["formal_title"])}).</p><ul class="pl">{"".join(link_li(k) for k in ks)}</ul>')
    return tpl(f'flow-{a.lower()}-{b.lower()}', 'Flow between parts', f'{pname(a)} to {pname(b)}', body)


def templates(page):
    keys = sorted(set(re.findall(r'data-select="([^"]+)"', page)))
    out = []
    for k in keys:
        kind, _, rest = k.partition('-')
        if kind == 'var':
            out.append(tpl_var(rest.upper()))
        elif kind == 'link':
            out.append(tpl_link(rest.upper()))
        elif kind == 'loop':
            lid = next(x for x in LO if x.lower() == rest)
            out.append(tpl_loop(lid))
        elif kind == 'reform':
            out.append(tpl_reform(rest.upper()))
        elif kind == 'issue':
            out.append(tpl_issue(rest.upper()))
        elif kind == 'pw':
            out.append(tpl_pathway(rest.upper()))
        elif kind == 'flow':
            a, b = rest.split('-')
            out.append(tpl_flow(a.upper(), b.upper()))
        else:
            raise ValueError(k)
    return ''.join(out)


# ------------------------------------------------------------------------------------------------ styles
CSS = r"""
:root{--np:#DCD9D2;--ch:#121212;--rd:#E63946;--pr:#1F2D5A;--st:#5D636D;--vg:#4A7C74;--wh:#FFFFFF;--ds:#4E535B;
--ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px;--ak-w-case:8px;--ground:var(--np);--gut:64px}
*{box-sizing:border-box}
html{background:var(--np);color:var(--ch);scroll-padding-top:16px}
body{margin:0;background:var(--np);color:var(--ch);font:400 17px/27px Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{text-decoration-thickness:2px}
button{font:inherit;color:inherit}
p{margin:0}
.wrap{width:min(1312px,calc(100% - 2*var(--gut)));margin:0 auto}
.skip{position:absolute;left:16px;top:-80px;background:var(--wh);padding:10px 14px;z-index:100;font:600 15px/20px Inter}
.skip:focus{top:12px}
.eyebrow{font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--ch);margin:0 0 8px}
.kicker{color:var(--ds)}
/* masthead */
.mast{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:center;height:72px;border-bottom:1px solid var(--st)}
.mast .wm{grid-column:1/4;display:flex;align-items:center;color:var(--ch);height:24px}
.mast .wm svg{display:block}
.mast .wm16{display:none}
.mast .rh{grid-column:4/7;font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--ds)}
.views{grid-column:7/13;display:flex;justify-content:flex-end;gap:22px;height:72px}
.views a{display:flex;align-items:center;height:72px;font:600 15px/20px Inter;text-decoration:none;white-space:nowrap}
.views a:hover{text-decoration:underline}
.views a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ch)}
/* crumbs and locator */
.crumbrow{display:flex;justify-content:space-between;align-items:flex-start;padding-top:16px;min-height:44px}
.ak-crumbs ol{font:500 14px/20px Inter}
.ak-crumbs a{color:var(--ds)}
.ak-crumbs [aria-current]{font-weight:600;color:var(--ch)}
.locator{display:flex;align-items:center;gap:10px;text-decoration:none;font:500 13px/18px Inter;color:var(--ds)}
.locator svg{display:block}
.locator .lr{fill:none;stroke:var(--st);stroke-width:1}
.locator .lr.ak-here{fill:var(--ch);stroke:var(--ch)}
/* ledes */
.lede{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;margin-top:20px}
.lede-main{grid-column:1/9}
.lede.one{display:block;max-width:880px}
.display{font:800 56px/60px 'Inter Tight',Inter,sans-serif;letter-spacing:-.035em;margin:0 0 18px;text-wrap:balance;margin-left:-.04em}
.headline{font:800 40px/44px 'Inter Tight',Inter,sans-serif;letter-spacing:-.03em;margin:0 0 16px;text-wrap:balance}
.deck{font:400 19px/28px Inter;max-width:62ch;margin:0}
.deck.sm{margin-bottom:28px}
.deck b{font-weight:600}
.measure{font:400 15px/23px Inter;color:var(--ds);max-width:900px}
.measure.big{font:400 19px/28px Inter;color:var(--ch)}
.key{grid-column:9/13;border-top:1px solid var(--ch);padding-top:14px}
.key .howto{font:400 15px/23px Inter;margin-bottom:12px}
.key .kh{font:600 15px/18px Inter;margin:14px 0 6px}
.key .kn{font:400 15px/23px Inter;margin-top:8px}
.keyev{list-style:none;margin:0;padding:0}
.keyev li{display:flex;align-items:center;gap:10px;font:500 13px/18px Inter;margin:5px 0}
.keyev b{font-weight:600}
/* chart frame: a Charcoal rule with a tab, sentence title, measure line, source line */
.chart{position:relative;margin-top:64px;border-top:1px solid var(--ch);padding-top:20px}
.chart::before{content:"";position:absolute;left:0;top:-1px;width:48px;height:5px;background:var(--ch)}
.ctitle{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 6px;text-wrap:balance;max-width:960px}
.chart .measure{margin-bottom:20px}
.csource{display:flex;justify-content:space-between;gap:24px;font:400 13px/18px Inter;color:var(--ds);margin-top:16px}
.csource .credit{font-weight:600;color:var(--ch);white-space:nowrap}
.sect{font:800 40px/44px 'Inter Tight',Inter,sans-serif;letter-spacing:-.03em;margin:0 0 12px}
.small{font:400 14px/20px Inter;color:var(--ds);margin-top:8px}
.go{margin-top:14px;font:600 15px/23px Inter}
/* circuit */
.widewrap{overflow-x:auto}
.flows text{font-family:Inter,sans-serif}
.fey{font:700 13px/1 Inter;letter-spacing:.06em;fill:var(--ch)}
.fnote{font:400 14px/1 Inter;fill:var(--ds)}
.fcnt{font:700 20px/1 'Inter Tight',Inter,sans-serif;fill:var(--ch);font-variant-numeric:tabular-nums}
.fcnt.big{font-weight:800;font-size:22px}
.fcnt.back{fill:var(--ds);font-weight:700;font-size:20px}
.fret{font:400 14px/1 Inter;fill:var(--ch)}
.fword{font:400 14px/1 Inter;fill:var(--ds)}
.tierrule{stroke:var(--st);stroke-width:1}
.cb{fill:var(--wh);stroke:var(--ch);stroke-width:1}
.cbt{fill:var(--ch)}
.cbn{font:800 22px/1 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;fill:var(--ch)}
.cbf{font:400 14px/1 Inter;fill:var(--ds)}
.cbox:hover .cb{stroke-width:2}
.cbox:focus-visible .cb{stroke:var(--vg);stroke-width:3}
.flow .ak-mark{fill:none}
.flow.main .ak-mark{stroke:var(--ch)}
.flow.ctx .ak-mark{stroke:var(--st)}
.flow .hd.lo{fill:currentColor}
.flow.main{color:var(--ch)}
.flow.ctx{color:var(--st)}
.tri{fill:var(--ch)}
.ak-hit2{fill:transparent}
.flow:focus-visible .ak-hit2,.flow:focus-visible .ak-hit{stroke:var(--vg);stroke-width:2}
.flow:focus-visible .ak-hit2{fill:none}
.flow[data-ak-sel] .fcnt{text-decoration:underline}
.flow[data-ak-sel].main .ak-mark,.flow[data-ak-sel].ctx .ak-mark{stroke:var(--ch);stroke-width:6px}
.halo{fill:var(--np)}
.narrowwrap{display:none}
details.words{margin-top:10px;font:400 15px/23px Inter}
details.words summary,details.keyfold summary{cursor:pointer;font-weight:600;min-height:32px;display:list-item;padding-top:4px}
.words-phone,.keyfold{display:none}
.words-phone .kh{font:600 15px/23px Inter;margin:12px 0 4px}
.words-phone .inwords{font:400 15px/23px Inter}
.cnote{font:400 14px/20px Inter;color:var(--ds);margin-top:10px;max-width:960px}
.inwords{margin:6px 0 0;padding-left:20px;max-width:900px}
.ak-readout{font:400 15px/23px Inter;color:var(--ch);min-height:23px;margin-top:10px}
/* register */
.reg-head,.rr-head{display:grid;grid-template-columns:40px 212px minmax(0,1fr) 150px 176px 196px;column-gap:20px}
.reg-head{border-bottom:2px solid var(--ch);padding:0 0 8px;margin-top:6px}
.reg-head span{font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase}
.rr-head{padding:22px 0 24px;border-bottom:1px solid var(--st);align-items:start}
.reg-row.open .rr-head{border-bottom:0}
.c-no{font:700 20px/24px 'Inter Tight',Inter,sans-serif;color:var(--ds);font-variant-numeric:tabular-nums;padding-top:2px}
.c-part h3{margin:0}
.rr-toggle{display:flex;align-items:center;gap:10px;background:none;border:0;padding:0;cursor:pointer;text-align:left;min-height:32px}
.rr-toggle .pn{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em}
.rr-toggle:hover .pn{text-decoration:underline;text-underline-offset:4px}
.pm{position:relative;width:18px;height:18px;border:1.5px solid var(--ch);flex:none}
.pm::before,.pm::after{content:"";position:absolute;left:3px;right:3px;top:7.25px;height:1.5px;background:var(--ch)}
.pm::after{transform:rotate(90deg)}
.rr-toggle[aria-expanded="true"] .pm::after{display:none}
.formal{font:400 14px/20px Inter;color:var(--ds);margin-top:2px}
.question{font:600 15px/23px Inter;margin-top:8px}
.layer{font:400 13px/18px Inter;color:var(--ds);margin-top:4px}
.what{font:400 15px/23px Inter;margin-bottom:10px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:7px;min-height:28px;padding:3px 10px 3px 7px;background:var(--wh);border:0;box-shadow:inset 0 0 0 1px transparent;cursor:pointer;text-align:left}
.chip .cd{font:700 13px/18px Inter;font-variant-numeric:tabular-nums;color:var(--ds)}
.chip .cl{font:400 14px/20px Inter}
.chip:hover{box-shadow:inset 0 0 0 1px var(--ch)}
.chip.ak-rel{box-shadow:inset 0 0 0 2px var(--ch)}
.chip[data-ak-sel]{background:var(--ch);color:var(--wh);box-shadow:none}
.chip[data-ak-sel] .cd{color:var(--np)}
.chip.ak-target{box-shadow:inset 0 0 0 2px var(--pr)}
.counts{list-style:none;margin:0;padding:0}
.counts li{display:grid;grid-template-columns:30px 1fr;column-gap:8px;align-items:baseline}
.counts .n{font:700 20px/24px 'Inter Tight',Inter,sans-serif;text-align:right;font-variant-numeric:tabular-nums}
.counts .w{font:400 14px/20px Inter}
.evc .evbar{display:block;margin-top:4px}
.evt{font:500 13px/18px Inter;margin-top:8px}
.evs{fill:var(--ch)}
.evl{stroke:var(--ch);stroke-width:2}
.loopref{display:block;text-decoration:none}
.loopref .lk{display:block;font:500 13px/18px Inter;color:var(--ds)}
.loopref .ln{display:block;font:600 15px/23px Inter;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
.loopref:hover .ln{text-decoration-thickness:2px}
.lt{font:400 14px/20px Inter;color:var(--ds);margin-top:4px}
.none{font:400 14px/20px Inter;color:var(--ds)}
.rr-more{display:grid;grid-template-columns:minmax(0,1fr) 350px 400px;column-gap:40px;padding:4px 0 36px 60px;border-bottom:1px solid var(--st)}
.m-story .chapter{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 10px}
.m-story .story{font:400 17px/27px Inter;margin-bottom:14px}
.pw{font:400 15px/23px Inter;margin-top:4px}
.pw b{font-weight:600}
.m-loop .lname{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 6px;display:flex;align-items:center;flex-wrap:wrap;gap:10px}
.m-loop .lname a{text-decoration:none}
.m-loop .lname a:hover{text-decoration:underline}
.lkind{font:400 14px/20px Inter;color:var(--ds);margin-bottom:12px}
.ra{font:400 15px/23px Inter;margin-top:10px}
.ra .eyebrow{display:block;margin:0 0 4px}
.ra b,.lcr b,.ra-big b{font-weight:600}
.lstat{font:400 14px/20px Inter;color:var(--ds);margin-top:8px}
.grp{font:600 15px/23px Inter;margin:14px 0 4px;display:flex;justify-content:space-between;border-bottom:1px solid var(--st);padding-bottom:3px}
.grp span{font-variant-numeric:tabular-nums}
.lks{list-style:none;margin:0;padding:0}
.lks li{display:flex;align-items:center;gap:10px;font:400 14px/20px Inter;padding:3px 0}
.lks .glyph{flex:none}
/* fix card, on Prussian */
.fix{background:var(--pr);color:var(--wh);padding:20px 22px 22px;align-self:start}
.fix .eyebrow{color:var(--np)}
.fix h4{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:10px 0 8px;color:var(--wh)}
.fix p,.fix li,.fix dd,.fix dt{font-weight:500}
.fxid{display:flex;align-items:center;gap:10px}
.fxid .band{font:500 13px/18px Inter;color:var(--np)}
.fxs{font:500 15px/23px Inter}
.fxh{font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase;color:var(--np);margin:16px 0 6px}
.acts{list-style:none;margin:0;padding:0}
.acts li{font:500 14px/20px Inter;margin:5px 0;display:flex;gap:8px;align-items:flex-start}
.eff{margin:0}
.eff div{display:grid;grid-template-columns:150px 1fr;gap:10px;padding:5px 0;border-top:1px solid rgba(220,217,210,.5)}
.eff dt{font:500 14px/20px Inter;color:var(--np)}
.eff dd{margin:0;font:500 14px/20px Inter;color:var(--wh)}
.fxn{font:500 14px/20px Inter;color:var(--np);margin-top:12px}
.onp{display:inline-flex;align-items:center;min-height:32px;margin-top:14px;font:600 15px/20px Inter;color:var(--wh);background:none;border:1px solid var(--np);padding:5px 12px;cursor:pointer;text-decoration:none}
.onp:hover{text-decoration:underline}
.fix :focus-visible{outline-color:var(--np)}
/* two-part ID chips */
.idc{white-space:nowrap;display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 Inter;vertical-align:middle;flex:none}
.idc .k{display:flex;align-items:center;padding:0 7px;background:var(--ch);color:var(--np);letter-spacing:.06em;text-transform:uppercase}
.idc .c{letter-spacing:0;display:flex;align-items:center;padding:0 8px;box-shadow:inset 0 0 0 1.5px var(--ch);font:700 14px/1 Inter;font-variant-numeric:tabular-nums}
.idc.compact{height:22px}
.idc.compact .c{font-size:13px}
[data-surface="prussian"] .idc .k{background:var(--wh);color:var(--pr)}
[data-surface="prussian"] .idc .c{box-shadow:inset 0 0 0 1.5px var(--wh);color:var(--wh)}
/* stack drawings */
.stack{display:block;max-width:100%;height:auto;overflow:visible}
.stack .box{fill:var(--wh);stroke:var(--ak-hi,currentColor)}
.stack .concept .box{stroke:var(--ch)}
.stack .bl{font:600 15px/1 Inter;fill:var(--ch)}
.stack .blt{font:700 20px/1 'Inter Tight',Inter,sans-serif;letter-spacing:-.01em}
.stack .ak-mark{fill:none}
.stack .wire .ak-mark{stroke:var(--ak-hi,currentColor)}
.stack .hd,.stack .tag polygon{fill:var(--ak-hi,currentColor)}
.stack .tk{stroke:var(--ak-hi,currentColor);stroke-width:2;fill:none}
.stack .sg{fill:var(--np)}
.stack .railgap{stroke:var(--np)}
.stack .rail{stroke:var(--ch)}
.stack .hi{display:none}
.stack .rec{fill:var(--ch)}
.ssw{font:400 13px/1 Inter;fill:var(--ch)}
.swv{font:600 15px/1 Inter;fill:var(--ch)}
.sgc{font:400 13px/1 Inter;fill:var(--ds)}
.sgd{font:400 13px/1 Inter;fill:var(--ds)}
.swk{font:700 13px/1 Inter;fill:var(--ch)}
.flag rect{fill:var(--pr)}
.rf-other .stack .flag,.rf-other .stack .flagtxt{display:none}
.flag .fl{font:700 13px/1 Inter;fill:var(--wh)}
.stack.l .ssw .swv{font-size:17px}
.stack.l .sgc{font-size:14px}
.stack.l .sgd{font-size:14px}
.stack.l .swk{font-size:14px}
.sey{font:700 13px/1 Inter;letter-spacing:.06em;fill:var(--ch)}
.snm{font:600 15px/1 Inter;fill:var(--ch)}
.stx{font:400 14px/1 Inter;fill:var(--ch)}
.snote{font:400 14px/1 Inter;fill:var(--ds)}
.smk{font:700 15px/1 Inter;fill:var(--ch)}
.stack.live [data-select]:focus-visible .ak-hit{stroke:var(--vg);stroke-width:2;stroke-dasharray:none}
.stack.live .node:focus-visible .box{stroke:var(--vg);stroke-width:3}
.stack .ak-hit{fill:none;stroke:transparent;stroke-width:18px}
/* lit states: 6 px marks, patterns rescaled */
.stack.live [data-ak-sel] .ak-mark,.stack.live .ak-target .ak-mark,.stack.live .ak-now .ak-mark{stroke-width:6px}
.stack.live .wire[data-ak-sel] .ak-mark,.stack.live .wire.ak-target .ak-mark,.stack.live .wire.ak-now .ak-mark{stroke-dasharray:var(--d6,none)}
.stack.live [data-ak-sel] .lo,.stack.live .ak-target .lo,.stack.live .ak-now .lo{display:none}
.stack.live [data-ak-sel] .hi,.stack.live .ak-target .hi,.stack.live .ak-now .hi{display:inline}
.stack.live .ak-target .tag polygon,.stack.live .ak-target .hd{stroke:var(--ak-keyline,none);stroke-width:1}
.stack.l .ak-rel .ak-mark{stroke-width:3px}
.stack.s.live .ak-rel .ak-mark{stroke-width:3px}
.stack.s.live .wire.ak-rel .ak-mark{stroke-dasharray:var(--d3,none)}
.ak-dim .stack.live [data-select]:not(.ak-rel):not([data-ak-sel]):not(.ak-target) .ak-mark{stroke:var(--st)}
.ak-stepping .stack.live [data-select]:not(.ak-now):not(.ak-done):not(.ak-target) .ak-mark{stroke:var(--st)}
[data-view-root]:not([data-red-ok]) .ak-target{--ak-hi:var(--ak-sel)}
/* loop cards */
.lgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:40px 24px}
.lgrid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.lcard{border-top:2px solid var(--ch);padding-top:12px;min-width:0}
.lck{display:flex;align-items:center;gap:10px;font:500 13px/18px Inter;color:var(--ds)}
.lcard h3{margin:10px 0 4px}
.lcb{background:none;border:0;padding:0;text-align:left;cursor:pointer;font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em}
.lcb:hover{text-decoration:underline;text-underline-offset:4px}
.lcb[data-ak-sel]{text-decoration:underline;text-decoration-thickness:3px}
.lct{font:400 15px/23px Inter;margin-bottom:14px}
.lcr{font:400 15px/23px Inter;margin-top:10px}
.lcs{font:400 14px/20px Inter;color:var(--ds);margin-top:8px}
.lcd{font:600 14px/20px Inter;margin-top:6px}
.lgroup{margin-top:56px}
.gh{font:800 40px/44px 'Inter Tight',Inter,sans-serif;letter-spacing:-.03em;margin:0 0 4px}
.ghs{font:400 15px/23px Inter;color:var(--ds);margin-bottom:22px}
/* loop index */
.li{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px}
.lig h3{display:flex;justify-content:space-between;font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 8px;padding-bottom:6px;border-bottom:2px solid var(--ch)}
.lig h3 span{font-variant-numeric:tabular-nums}
.lig ul{list-style:none;margin:0;padding:0}
.lig li{padding:7px 0;border-bottom:1px solid var(--st)}
.lig li a{display:block;font:600 15px/23px Inter}
.lig li span{display:block;font:400 13px/18px Inter;color:var(--ds)}
/* bill */
.bill{margin-top:88px;border-top:1px solid var(--ch);padding-top:20px;position:relative}
.bill::before{content:"";position:absolute;left:0;top:-1px;width:48px;height:5px;background:var(--ch)}
.hubs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px}
.hub h3{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 6px;text-wrap:balance;min-height:52px}
.hq{font:400 15px/23px Inter;color:var(--ds);margin-bottom:12px;min-height:46px}
.qs{list-style:none;margin:0;padding:0}
.qb{display:block;width:100%;text-align:left;background:var(--wh);border:0;padding:10px 12px 12px;margin:0 0 8px;cursor:pointer;box-shadow:inset 0 0 0 1px transparent}
.qb:hover{box-shadow:inset 0 0 0 1px var(--ch)}
.qb[data-ak-sel]{box-shadow:inset 4px 0 0 var(--ch)}
.qt{display:block;font:500 13px/18px Inter;color:var(--ds)}
.qq{display:block;font:600 15px/23px Inter;margin-top:2px}
/* area C */
.figs{list-style:none;margin:28px 0 0;padding:14px 0 0;display:flex;gap:40px;border-top:1px solid var(--ch);max-width:760px}
.figs li{display:flex;flex-direction:column}
.figs li span:last-child{font:400 14px/20px Inter;margin-top:4px}
.statbox{grid-column:9/13;border-top:1px solid var(--ch);padding-top:14px}
.statbox ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:14px 20px}
.statbox li{display:flex;flex-direction:column}
.fig{font:800 40px/40px 'Inter Tight',Inter,sans-serif;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.statbox li span:last-child{font:400 14px/20px Inter}
.vhead,.vrow{display:grid;grid-template-columns:64px 240px minmax(0,1fr) 300px 200px;column-gap:24px}
.vhead{border-bottom:2px solid var(--ch);padding-bottom:8px}
.vhead span,.ihead span,.rhead span{font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase}
.vlist,.ilist,.rlist{list-style:none;margin:0;padding:0}
.vrow{padding:18px 0;border-bottom:1px solid var(--st);align-items:start}
.vi svg{display:block;color:var(--ch)}
.vn h3{margin:6px 0 2px}
.vb,.ib,.rb,.lrow{background:none;border:0;padding:0;text-align:left;cursor:pointer}
.vb{font:700 20px/22px 'Inter Tight',Inter,sans-serif;letter-spacing:-.01em}
.vb:hover,.ib:hover,.rb:hover{text-decoration:underline;text-underline-offset:3px}
.vb[data-ak-sel],.ib[data-ak-sel],.rb[data-ak-sel]{text-decoration:underline;text-decoration-thickness:3px}
.vt{font:400 14px/20px Inter;color:var(--ds)}
.vd p,.vm p{font:400 15px/23px Inter}
.vm p{font-weight:600}
.vx p{font:400 14px/20px Inter}
.cols3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px}
.colh{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:0;display:flex;justify-content:space-between;border-bottom:2px solid var(--ch);padding-bottom:6px}
.lks2{list-style:none;margin:0;padding:0}
.lrow{display:grid;grid-template-columns:84px minmax(0,1fr);column-gap:12px;width:100%;padding:8px 0;border-bottom:1px solid rgba(93,99,109,.45)}
.lrow .glyph{margin-top:3px}
.lrow:hover .lrn{text-decoration:underline}
.lrow[data-ak-sel]{box-shadow:inset 4px 0 0 var(--ch);padding-left:8px}
.lrt{display:flex;flex-direction:column}
.lrn{font:600 15px/23px Inter}
.lrf{font:400 14px/20px Inter}
.lrg{font:400 13px/18px Inter;color:var(--ds);display:flex;align-items:center;gap:6px}
.recq{display:inline-block;width:7px;height:7px;background:var(--ch);flex:none}
.glyph{display:block;overflow:visible}
.glyph .ak-mark{stroke:var(--ch);fill:none}
.glyph .hd,.glyph .tag polygon{fill:var(--ch)}
.glyph .tk{stroke:var(--ch);stroke-width:2}
.glyph .sg{fill:var(--np)}
.glyph .railgap{stroke:var(--np)}
.glyph .dia{fill:var(--np);stroke:var(--ch);stroke-width:2}
.glyph .hi{display:none}
.ihead,.irow{display:grid;grid-template-columns:minmax(0,1fr) 120px 170px minmax(0,1.1fr);column-gap:24px}
.ihead{border-bottom:2px solid var(--ch);padding-bottom:8px}
.igh{display:flex;justify-content:space-between;font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase;padding:18px 0 6px;border-bottom:1px solid var(--ch)}
.irow{padding:10px 0;border-bottom:1px solid rgba(93,99,109,.45);align-items:start}
.ib{font:600 15px/23px Inter}
.itouch{font:500 13px/23px Inter;font-variant-numeric:tabular-nums}
.igr{display:flex;align-items:center;gap:8px;font:400 14px/23px Inter}
.iex{font:400 14px/20px Inter}
.iex .exh{display:block}
.iex .exw{display:block;color:var(--ds)}
.rhead,.rrow{display:grid;grid-template-columns:118px minmax(0,1fr) 116px repeat(4,112px) 150px;column-gap:18px}
.rhead{border-bottom:2px solid var(--ch);padding-bottom:8px}
.rrow{padding:14px 0;border-bottom:1px solid rgba(93,99,109,.45);align-items:start}
.rb{font:600 15px/23px Inter}
.rpage{display:block;font:500 14px/20px Inter;margin-top:4px}
.racts{font:500 14px/23px Inter;font-variant-numeric:tabular-nums}
.ef{font:600 14px/20px Inter}
.ef.zero{font-weight:400;color:var(--ds)}
.rroute{font:400 14px/20px Inter}
/* loop and reform pages */
.r10grid{display:grid;grid-template-columns:784px minmax(0,1fr);column-gap:48px;margin-top:8px}
.r10fig{margin:40px 0 0}
.r10wide svg{display:block}
.r10narrow{display:none}
.r10side{margin-top:40px;border-top:1px solid var(--ch);padding-top:20px}
.ra-big{font:400 19px/28px Inter;margin-bottom:22px}
.ra-big b{font-weight:600}
.quote{font:italic 400 22px/31px Lora,serif;letter-spacing:-.005em;margin:0 0 24px}
.sh{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em;margin:28px 0 8px}
.sh.first{margin-top:0}
.r10side > p:not(.eyebrow):not(.ra-big){font:400 17px/27px Inter;margin-bottom:10px}
.stepper{border-top:1px solid var(--st);padding-top:4px}
.sbtns{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 12px}
.sstatus{font:400 15px/23px Inter;min-height:46px}
.slist{margin:10px 0 0;padding:0 0 0 20px;font:400 15px/23px Inter}
.slist li{margin:4px 0}
.r10notes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;margin-top:48px;border-top:1px solid var(--ch);padding-top:4px}
.r10notes p{font:400 17px/27px Inter}
.r10reforms{list-style:none;margin:0;padding:0}
.r10reforms li{align-items:start;display:grid;grid-template-columns:minmax(0,1fr) 80px minmax(0,1.2fr);column-gap:24px;padding:12px 0;border-bottom:1px solid rgba(93,99,109,.45)}
.rid2{font:700 14px/23px Inter;font-variant-numeric:tabular-nums}
.rtg{font:400 15px/23px Inter}
.lede.one.rflede{display:flex;gap:28px;align-items:flex-start;max-width:1040px}
.rficon svg{display:block;color:var(--ch)}
.nopos{font:600 15px/23px Inter;margin-top:12px}
.rtab{width:100%;border-collapse:collapse;font:400 15px/23px Inter}
.rtab th,.rtab td{text-align:left;vertical-align:top;padding:10px 16px 10px 0;border-bottom:1px solid rgba(93,99,109,.45)}
.rtab thead th{font:700 13px/18px Inter;letter-spacing:.06em;text-transform:uppercase;border-bottom:2px solid var(--ch)}
.rtab tbody th{font-weight:600}
.rtab.eff{max-width:760px}
.fw{display:inline-flex;align-items:center;gap:8px;white-space:nowrap}
.feas .fon{fill:var(--ch)}
.emark{display:block}
.emc{stroke:var(--ch);stroke-width:1}
.ems{fill:var(--ch)}
.emq{font:700 13px/1 Inter;fill:var(--ch)}
.rtab.eff tbody th{width:280px}
.rtab.eff td:nth-child(2){width:110px}
.rtab.routes th:first-child{width:120px}
.rtab.routes td:nth-child(3){width:150px}
.rtab.routes td:nth-child(5){width:140px}
.feas .foff{fill:none;stroke:var(--ch);stroke-width:1}
.feaskey{list-style:none;margin:16px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6px 32px}
.feaskey li{display:flex;gap:10px;align-items:baseline;font:400 14px/20px Inter}
.chart.half{max-width:none}
.evgrid{display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:56px}
.evcard{border-top:1px solid var(--ch);padding-top:4px}
.evcard p{font:400 17px/27px Inter}
.evg{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.succ{margin:0;padding-left:20px;font:400 17px/27px Inter}
.status{margin-top:56px;background:var(--wh);padding:24px 28px 28px;border-top:4px solid var(--ch)}
.status p:not(.eyebrow){font:400 17px/27px Inter;max-width:78ch;margin-bottom:12px}
.status p.small{font:400 14px/20px Inter;color:var(--ds)}
.status .disc{font-weight:400}
.status .disc b{font-weight:700}
/* how to read */
.htr{display:grid;grid-template-columns:60px minmax(0,1fr) 640px;column-gap:32px;margin-top:56px;border-top:1px solid var(--ch);padding-top:20px}
.htn{font:800 40px/40px 'Inter Tight',Inter,sans-serif;font-variant-numeric:tabular-nums}
.htb .sect{font-size:40px}
.htb p{font:400 17px/27px Inter;margin-bottom:10px}
.spec{display:block;margin-bottom:12px}
.spec .ak-mark{stroke:var(--ch);fill:none}
.spec .hd,.spec .tag polygon{fill:var(--ch)}
.spec .tk{stroke:var(--ch);stroke-width:2}
.spec .sg{fill:var(--np)}
.spec .hi{display:none}
.bl2{font:600 15px/1 Inter;fill:var(--ch)}
.swv2{font:600 15px/1 Inter;fill:var(--ch)}
.texlist{list-style:none;margin:0;padding:0}
.texlist li{display:grid;grid-template-columns:96px 1fr 172px;column-gap:16px;padding:9px 0;border-bottom:1px solid rgba(93,99,109,.45);align-items:center}
.texlist .tw{font:400 15px/23px Inter}
.texlist .tn{font:500 14px/20px Inter;text-align:right;font-variant-numeric:tabular-nums}
.texlist .te{grid-column:2/4;font:400 14px/20px Inter;color:var(--ds)}
.colors{list-style:none;margin:0;padding:0}
.colors li{display:flex;gap:14px;align-items:center;padding:8px 0;font:400 15px/23px Inter;border-bottom:1px solid rgba(93,99,109,.45)}
.sw2{width:48px;height:28px;flex:none;box-shadow:inset 0 0 0 1px var(--ch)}
.sw2.ch{background:var(--ch)}.sw2.st{background:var(--st)}.sw2.pr{background:var(--pr)}.sw2.rd{background:var(--rd)}
/* panel: a drawer on the right on wide screens */
.ak-panel{font:400 15px/23px Inter}
.ak-panel .lead{font:400 17px/27px Inter;margin-bottom:12px}
.ak-panel p{margin:0 0 10px}
.ak-panel h2{font:800 22px/26px 'Inter Tight',Inter,sans-serif;letter-spacing:-.02em}
.ak-panel h3{color:var(--ch)}
.ak-panel dl{margin:10px 0}
.ak-panel .pg{font:600 14px/20px Inter;margin:10px 0 2px}
.ak-panel .pl{list-style:none;padding:0}
.ak-panel .pl li{display:grid;grid-template-columns:64px minmax(0,1fr);column-gap:10px;align-items:start;font:400 14px/20px Inter;padding:6px 0;border-bottom:1px solid rgba(93,99,109,.3)}
.ak-panel .pl .pm2{display:block}
.ak-panel .pl .glyph{flex:none;margin-top:0}
.ak-panel .pm2{color:var(--ds)}
.ak-panel .src{font:400 13px/18px Inter;color:var(--ds);margin-top:16px}
.ak-panel .next{font:600 15px/23px Inter;margin-top:14px}
.ak-panel .small{font:400 14px/20px Inter}
.ak-panel .glyph .sg,.ak-panel .glyph .railgap,.ak-panel .glyph .dia{fill:var(--wh)}
.ak-panel .glyph .railgap{stroke:var(--wh)}
.ak-panel .glyph .dia{fill:var(--wh)}
@media (min-width:900px){
 .ak-panel{position:fixed;top:0;right:0;bottom:0;width:420px;max-height:none;z-index:80;border-left:1px solid var(--ch);overflow:auto}
}
/* footer */
.foot{margin-top:88px;border-top:1px solid var(--st);padding:14px 0 40px;display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px}
.foot p{font:400 13px/18px Inter;color:var(--ds)}
.foot .fl1{grid-column:1/9}
.foot .fl2{grid-column:9/13;text-align:right}
/* views */
[data-view-root]{padding-bottom:8px}
[data-view-root] > .csource{margin-top:48px}
/* phone */
@media (max-width:899.98px){
 :root{--gut:20px}
 body{font:400 16px/25px Inter}
 .mast{display:block;height:auto;border-bottom:1px solid var(--st)}
 .mast .wm{padding:20px 0 0;height:auto}
 .mast .wm24{display:none}.mast .wm16{display:block}
 .mast .rh{display:none}
 .views{display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:auto;margin-top:12px}
 .views a{height:44px;font-size:15px;justify-content:flex-start}
 .lede{display:block}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline,.sect,.gh,.htb .sect{font-size:30px;line-height:34px}
 .deck{font-size:17px;line-height:25px}
 .measure.big{font-size:17px;line-height:25px}
 .statbox{margin-top:24px}
 .key{display:none}
 .keyfold{display:block;margin-top:20px;border-top:1px solid var(--ch);padding-top:8px}
 .keyfold .howto{font:400 15px/23px Inter;margin:8px 0}
 .keyfold .kh{font:600 15px/18px Inter;margin:12px 0 6px}
 .keyfold .kn{font:400 15px/23px Inter;margin-top:8px}
 details.words{display:none}
 .words-phone{display:block}
 .widewrap{display:none}
 .narrowwrap{display:block}
 .reg-head{display:none}
 .rr-head{grid-template-columns:1fr;row-gap:14px}
 .c-no{display:none}
 .counts{display:grid;grid-template-columns:repeat(4,1fr)}
 .counts li{display:flex;flex-direction:column}
 .counts .n{text-align:left}
 .rr-more{grid-template-columns:1fr;padding:0 0 28px;row-gap:28px}
 .eff div{grid-template-columns:120px 1fr}
 .lgrid,.lgrid.two{grid-template-columns:1fr}
 .li{grid-template-columns:1fr}
 .hubs{grid-template-columns:1fr}
 .hq{min-height:0}
 .vhead,.ihead,.rhead{display:none}
 .vrow{grid-template-columns:56px minmax(0,1fr);row-gap:10px}
 .vd,.vm,.vx{grid-column:1/3}
 .cols3{grid-template-columns:1fr}
 .irow{grid-template-columns:1fr;row-gap:4px}
 .rrow{grid-template-columns:1fr;row-gap:6px}
 .reffs{grid-template-columns:1fr 1fr}
 .r10grid{display:block}
 .r10wide{display:none}
 .r10narrow{display:block}
 .r10notes,.evgrid{grid-template-columns:1fr}
 .r10reforms li{grid-template-columns:1fr;row-gap:2px}
 .rflede{display:block}
 .rficon{margin-bottom:12px}
 .rtab.routes,.rtab.routes tbody,.rtab.routes tr,.rtab.routes th,.rtab.routes td{display:block}
 .rtab.routes thead{display:none}
 .rtab.routes tr{padding:10px 0;border-bottom:1px solid rgba(93,99,109,.45)}
 .rtab.routes th,.rtab.routes td{border:0;padding:2px 0;width:auto!important}
 .rtab.routes td::before{content:attr(data-label) ": ";font-weight:600}
 .rtab.eff td:nth-child(2){width:96px}
 .feaskey{grid-template-columns:1fr}
 .locator{display:none}
 .figs{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px}
 .fig{font-size:32px;line-height:32px}
 .m-story .story,.r10notes p,.evcard p,.status p:not(.eyebrow),.htb p,.succ{font-size:16px;line-height:25px}
 .lrow{grid-template-columns:84px minmax(0,1fr)}
 .htr{grid-template-columns:1fr;row-gap:12px}
 .texlist li{grid-template-columns:84px 1fr}
 .texlist .tn{grid-column:2;text-align:left}
 .texlist .te{grid-column:1/3}
 .spec{max-width:100%;height:auto}
 .foot{display:block}
 .foot .fl2{text-align:left;margin-top:8px}
 .csource{flex-direction:column;gap:4px}
 .status{padding:18px 18px 22px}
}
"""

GLUE_JS = r"""
(function(){
  const $$=(s,r=document)=>[...r.querySelectorAll(s)];
  function setRow(btn, open){const id=btn.getAttribute('aria-controls'), el=document.getElementById(id); if(!el) return;
    btn.setAttribute('aria-expanded', String(open)); el.hidden=!open; btn.closest('.reg-row').classList.toggle('open', open);}
  document.addEventListener('click', (e)=>{
    const b=e.target.closest('.rr-toggle'); if(b){ setRow(b, b.getAttribute('aria-expanded')!=='true'); return; }
    const a=e.target.closest('a[href^="#reg-"]'); if(a){ const row=document.getElementById(a.getAttribute('href').slice(1));
      if(row){ e.preventDefault(); const t=row.querySelector('.rr-toggle'); if(t) setRow(t, true); row.scrollIntoView({block:'start'}); t && t.focus({preventScroll:true}); } }
  });
  function tabs(){ const v=(AtlasKit.state().view||'overview'); $$('.views a').forEach(a=>{ if(a.getAttribute('href')==='#'+v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); }); }
  AtlasKit.init({selRed:false});
  // With another reform selected, the red moves to its targets, so the tabs naming R-01 step aside.
  function flags(){ const st=AtlasKit.state(), other=!!(st.sel && st.sel.indexOf('reform-')===0 && st.sel!=='reform-r-01');
    $$('[data-view-root]').forEach(r=>r.classList.toggle('rf-other', other && r.dataset.viewRoot===st.view)); }
  document.addEventListener('click', ()=>setTimeout(flags,0)); document.addEventListener('keydown', ()=>setTimeout(flags,0));
  tabs(); flags(); addEventListener('hashchange', ()=>{ tabs(); setTimeout(flags,0); });
})();
"""


def patch_kit(js):
    # 1. Selection never takes the working red in this system; only R-01's targets do, on the views marked data-red-ok.
    js = js.replace("const mark = (x, job) => { x.setAttribute('data-ak-red', ''); if (!pru) {",
                    "const okRed = root.hasAttribute('data-red-ok');\n    const mark = (x, job) => { x.setAttribute('data-ak-red', ''); if (!pru && okRed) {")
    js = js.replace("if (sel && !reform && !busy) mark(sel, 'selected item');",
                    "if (sel && !reform && !busy && S.opts.selRed !== false) mark(sel, 'selected item');")
    # 2. A view that holds a wide and a phone copy of one drawing selects the copy on screen.
    js = js.replace("const root = rootOf(S.view), item = key && $(`[data-select=\"${key}\"]`, root);",
                    "const root = rootOf(S.view), cands = key ? $$(`[data-select=\"${key}\"]`, root) : [], item = cands.find(vis) || cands[0] || null;")
    js = js.replace("const selected = () => S.sel && $(`[data-select=\"${S.sel}\"]`, rootOf(S.view));",
                    "const selected = () => S.sel && ($$(`[data-select=\"${S.sel}\"]`, rootOf(S.view)).find(vis) || $(`[data-select=\"${S.sel}\"]`, rootOf(S.view)));")
    assert js.count('okRed') == 2 and 'selRed' in js and 'cands.find(vis)' in js and '.find(vis) ||' in js, 'kit patch failed'
    return js


# ------------------------------------------------------------------------------------------------ assemble
def page():
    views = overview() + area_c() + loop_r10() + reform_r01() + loops_view() + how_to_read()
    tpls = templates(views)
    wm24 = wordmark(24, '20261028_Wordmark-24px-Master.svg')
    wm16 = wordmark(16, '20261028_Wordmark-16px-Master.svg')
    tabs = ''.join(f'<a href="#{v}">{t}</a>' for v, t in [('overview', 'Overview'), ('area-c', 'Elections'), ('loop-r10', 'Loop R10'),
                                                          ('reform-r01', 'Reform R-01'), ('loops', 'All loops'), ('how-to-read', 'How to read')])
    foot = (f'<footer class="foot"><p class="fl1">{e(ED["meta"]["title"])} Systems Atlas V7, snapshot {SNAP}. '
            f'{cnt("variables", COUNT["variables"], "nn")} variables, {cnt("connections", COUNT["connections"], "nn")} connections, '
            f'{cnt("loops", COUNT["loops"], "nn")} loops, {cnt("reforms", COUNT["reforms"], "nn")} reforms.</p>'
            f'<p class="fl2">Editorial system 02, Economist Register. Studio draft.</p></footer>')
    panel = ('<aside class="ak-panel" data-ak-panel data-surface="white" aria-labelledby="ak-panel-title" hidden>'
             '<div class="ak-panel-bar"><p data-ak-panel-kind></p>'
             '<button type="button" class="ak-btn" data-ak-sheet-toggle aria-expanded="false">More</button>'
             '<button type="button" class="ak-btn" data-ak-close>Close</button></div>'
             '<h2 id="ak-panel-title" data-ak-panel-title tabindex="-1"></h2><div data-ak-panel-body></div></aside>')
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="atlas-views" content="overview area-c loop-r10 reform-r01 loops how-to-read">
<title>Who Do They Answer To? | Economist Register</title>
<meta name="description" content="Editorial atlas system 02, Economist Register: the Oath &amp; Action systems atlas as a register of eight parts. Studio draft, November 5, 2026.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&amp;family=Inter:wght@400;500;600;700&amp;family=Lora:ital,wght@1,400&amp;display=swap" rel="stylesheet">
<style>{KIT_CSS}</style>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the page</a>
<header class="wrap mast"><div class="wm"><span class="wm24" data-red="signature">{wm24}</span><span class="wm16" data-red="signature">{wm16}</span></div>
<p class="rh">System 02 / Economist Register</p><nav class="views" aria-label="Views">{tabs}</nav></header>
<main class="wrap ak-stage" id="main">
<p class="ak-vh" data-ak-status role="status"></p>
{views}
</main>
<div class="wrap">{foot}</div>
{panel}
{tpls}
<script>{patch_kit(KIT_JS)}</script>
<script>{GLUE_JS}</script>
</body>
</html>
"""
    return doc


def main():
    doc = page()
    assert '—' not in re.sub(r'<(script|style)\b.*?</\1>', '', doc, flags=re.S), 'em dash in page text'
    OUT.write_text(doc)
    print('wrote', OUT.relative_to(ROOT), f'{len(doc) / 1e3:.0f} kB')


if __name__ == '__main__':
    main()
