"""System 5, Architecture (White): the editorial atlas drawn as a building a reader can walk through.

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Governing brief:
work/handoffs/phase-2/20261105_Atlas-Editorial-Brief.md, section 4, System 5.

Usage:
    python3 -I work/boards/phase-2/atlas-editorial/05-architecture/build_system.py

Reads   work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json (every label, count and text)
        work/extract/supplied-20261105/20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html (only the R-01 disclosure)
        work/build/assets/identity/wordmark/ (the approved masters, inlined unchanged)
        work/build/assets/civic-line/ through icon_svg() in atlas_concepts_common.py (icons exactly as drawn)
        work/boards/phase-2/atlas-concepts/shared/atlas-kit.js and atlas-kit.css (behavior, restyled here)
Writes  work/boards/phase-2/atlas-editorial/05-architecture/20261105_Editorial-05-Architecture.html

Nothing on the page is typed by hand except the studio's headlines, decks and section titles, which the notes file
lists as studio drafts. Every label, count, sign, grade, delay, issue, example and reform text is read from the data.
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
_p = ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py'
_spec = importlib.util.spec_from_file_location('acc', _p)
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

DATA = json.loads((ROOT / 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json').read_text())
V7HTML = ROOT / 'work/extract/supplied-20261105/20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html'
KIT = ROOT / 'work/boards/phase-2/atlas-concepts/shared'
OUT = HERE / '20261105_Editorial-05-Architecture.html'

N, L, LO, RF, IS = DATA['nodes'], DATA['links'], DATA['loops'], DATA['reforms'], DATA['issues']
PARTS = {p['id']: p for p in DATA['parts']}
PART_OF = {k: n['part'] for k, n in N.items()}
COUNTS = DATA['meta']['counts']
STACK = ['E', 'D', 'C', 'B', 'A', 'EC', 'TC']          # the building, roof to foundation
CORE = ['A', 'B', 'C', 'D', 'E']
MAIN = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]  # the main circuit, with the return E to A
ADJ = [('D', 'E'), ('C', 'D'), ('B', 'C'), ('A', 'B'), ('EC', 'A'), ('TC', 'EC')]   # (lower, upper)
SNAP = DATA['meta']['snapshot']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']
MINUS = '−'
P = acc.PALETTE


def date_words(iso):
    if not iso:
        return None
    y, m, d = iso.split('-')
    return f'{MONTHS[int(m) - 1]} {int(d)}, {y}'


SNAP_WORDS = date_words(SNAP)


def e(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------------------------------- text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False):
    """Rendered width, from Inter's own metrics. Inter Tight runs about 5 percent narrower than Inter."""
    w = _font(weight).getlength(text) * size / 200
    return w * 0.95 if tight else w


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


# ---------------------------------------------------------------------------------------------------- vocabulary
GRADE = dict(acc.GRADES)
GRADE_ALIAS = {'well_supported': 'well-supported', 'contested': 'plausible_contested', 'well-supported': 'well-supported'}
GRADE_RANK = {'documented': 4, 'well-supported': 3, 'plausible': 2, 'plausible_contested': 1, 'hypothesis': 0}
DELAY = acc.DELAYS
TICKS = {'S': 1, 'M': 2, 'L': 3}


def gkey(g):
    g = GRADE_ALIAS.get(g, g)
    return g if g in GRADE else None


def gword(g):
    k = gkey(g)
    return GRADE[k][0] if k else str(g).replace('_', ' ').capitalize()


def ggloss(g):
    k = gkey(g)
    return GRADE[k][1] if k else ''


def gfull(g):
    gl = ggloss(g)
    return f'{gword(g)}: {gl}' if gl else gword(g)


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def verb(p):
    return {'+': 'raises', '-': 'lowers'}.get(p, 'decides')


def low(label, nid=None):
    """Lower-case a label inside a sentence, except a leading proper noun or acronym.
    A first word counts as a proper noun when the variable's own description capitalizes it mid-sentence."""
    first = label.split()[0]
    base = re.sub(r"'s$", '', first)
    if base.isupper() or (len(base) > 1 and base[1].isupper()):
        return label
    if nid and nid in N:
        for desc in filter(None, [N[nid].get('description'), N[nid].get('title'), N[nid].get('why')]):
            for m in re.finditer(r'\b' + re.escape(base) + r'\b', desc):
                before = desc[:m.start()]
                if before.endswith(' ') and before.rstrip() and (before.rstrip()[-1].isalpha() or before.rstrip()[-1] == ','):
                    return label
    return label[0].lower() + label[1:]


def first_sentence(text):
    m = re.match(r'(.+?[.!?])(\s|$)', text or '')
    return m.group(1) if m else (text or '')


def nw(n):
    return ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'][n] if n <= 10 else str(n)


def plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'


def chip(word, code, compact=False):
    c = ' compact' if compact else ''
    return f'<span class="chip{c}"><span class="k">{e(word)}</span><span class="c">{e(code)}</span></span>'


def cnt(key, n, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<span data-count="{e(key)}"{c}>{n:,}</span>'


def k_var(n):
    return 'var-' + n.lower()


def k_link(l):
    return 'link-' + l.lower()


def k_loop(lp):
    return 'loop-' + lp.lower()


def k_reform(r):
    return 'reform-' + r.lower()


def k_area(pid):
    return 'area-' + pid.lower()


def loop_href(lp):
    return '#loop-r10' if lp == 'R10' else f'#loops/{k_loop(lp)}'


# ---------------------------------------------------------------------------------------------------- the model, computed
def increase_rest(nid):
    s = N[nid].get('increase_means') or ''
    pre = 'A higher value means '
    return (s[len(pre):], True) if s.startswith(pre) else (s, False)


ACTIVE = {k: i for k, i in IS.items() if not i.get('retired')}


def issues_for_nodes(nodes):
    nodes = set(nodes)
    return [i for i in ACTIVE.values() if nodes & set(i.get('nodes') or [])]


def link_touches(lid, nodes):
    l = L[lid]
    return l['from'] in nodes or l['to'] in nodes


def reforms_for_nodes(nodes):
    nodes = set(nodes)
    out = []
    for rid in sorted(RF, key=lambda r: int(r.split('-')[1])):
        r = RF[rid]
        if any(t in nodes or (t in L and link_touches(t, nodes)) for t in r['targets']):
            out.append(rid)
    return out


def loops_through(nodes):
    nodes = set(nodes)
    return [lp for lp in DATA['loop_order'] if any(s.get('code') in nodes for s in LO[lp]['stations'] if s.get('is_variable'))]


HOME = {g['id']: g['loops'] for g in DATA['loop_groups']}


def flows():
    out = {}
    for lid, l in L.items():
        a, b = PART_OF[l['from']], PART_OF[l['to']]
        if a != b:
            out.setdefault((a, b), []).append(lid)
    return out


FLOWS = flows()


def flow_links(a, b):
    return FLOWS.get((a, b), [])


def lead_link(lids):
    """The connection a slab names as its example: on the most loops, then the strongest evidence, then V7 order."""
    order = list(L)
    return sorted(lids, key=lambda k: (-len(L[k]['loops']), -GRADE_RANK.get(L[k]['evidence'], 0), order.index(k)))[0]


INSIDE = [k for k, l in L.items() if PART_OF[l['from']] == PART_OF[l['to']]]
UP = [k for a, b in ADJ for k in flow_links(a, b)]
DOWN = [k for a, b in ADJ for k in flow_links(b, a)]
RETURN = flow_links('E', 'A') + flow_links('E', 'EC')
OUTSIDE = [k for k, l in L.items() if PART_OF[l['from']] == 'X']
_seen = set(INSIDE) | set(UP) | set(DOWN) | set(RETURN) | set(OUTSIDE)
SKIP = [k for k in L if k not in _seen]
assert len(INSIDE) + len(UP) + len(DOWN) + len(RETURN) + len(OUTSIDE) + len(SKIP) == len(L) == COUNTS['connections']
X_TO = {}
for k in OUTSIDE:
    X_TO.setdefault(PART_OF[L[k]['to']], []).append(k)


def pname(pid):
    return PARTS[pid]['plain_name']


def part_sentence(pid):
    """Each part's one-line description: V7's text when it is a statement, else the first sentence of its story."""
    t = PARTS[pid].get('text') or ''
    return t if t.endswith('.') else first_sentence(PARTS[pid]['story'])


def read_aloud(lp):
    """Built from the signs, so it cannot drift: more or less at each station, and back to the start."""
    o = LO[lp]
    st = o['stations']
    labels = []
    for s in st:
        if s.get('is_variable') and s.get('code') in N:
            labels.append(low(N[s['code']]['label'], s['code']))
        else:
            labels.append(low(s['label']))
    signs = [s['polarity'] for s in o['steps']]
    state, parts = 1, [f'more {labels[0]}']
    for i, sg in enumerate(signs):
        state *= 1 if sg == '+' else -1
        word = 'more' if state > 0 else 'less'
        if i == len(signs) - 1:
            parts.append(f'and back to {word} {labels[0]}')
        else:
            parts.append(f'{word} {labels[i + 1]}')
    s = ', '.join(parts) + '.'
    return s[0].upper() + s[1:]


def station_label(s):
    if s.get('is_variable') and s.get('code') in N:
        return N[s['code']]['label']
    return s['label']


def kind_line(lp):
    o = LO[lp]
    return f'{o["kind_word"]}, {o["kind_gloss"]}'


def weakest_words(lp):
    o = LO[lp]
    if o['conceptual']:
        return 'Conceptual: no complete numbered chain'
    if not o['weakest']:
        g = {s['evidence'] for s in o['steps']}
        return f'Every step {gword(g.pop()).lower()}' if len(g) == 1 else 'No single weakest step'
    ws = [f'{w}, {gword(L[w]["evidence"])}' for w in o['weakest']]
    return ('Weakest step ' if len(ws) == 1 else 'Weakest steps ') + ' and '.join(ws)


DIRECTION = {'running_up': 'Running up', 'running_down': 'Running down', 'running': 'Running', 'disabled': 'Disabled',
             'disabled in concentrated sectors': 'Disabled in concentrated sectors', 'unknown': 'Direction unknown',
             'design_target': 'A design target'}


def status_line(lp):
    o = LO[lp]
    bits = [DIRECTION.get(o['direction'], o['direction'] or ''), o['delay_word'], weakest_words(lp),
            plural(len(o['reforms']), 'reform')]
    return ' · '.join(b for b in bits if b)


def closure_note(lp):
    o = LO[lp]
    if o['conceptual']:
        return o['closure']
    if o['hypothesized']:
        return o['closure']
    return None


def v7_interests():
    """The disclosure V7 prints on reform profiles that touch the editor's own work (INTERESTS, INTEREST_TEXT)."""
    s = V7HTML.read_text(encoding='utf-8')
    m = re.search(r'var INTERESTS = \{(.*?)\};', s, re.S)
    pairs = dict(re.findall(r"'(R-\d+)':\s*'(\w+)'", m.group(1)))
    m2 = re.search(r'var INTEREST_TEXT = \{(.*?)\n\};', s, re.S)
    texts = {k: v.replace("\\'", "'") for k, v in re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", m2.group(1))}
    return {r: texts[t] for r, t in pairs.items()}


DISCLOSE = v7_interests()
assert 'Yes on 3' in DISCLOSE['R-01']
GLOSS = {g['term']: g['definition'] for g in DATA['glossary']}


# ---------------------------------------------------------------------------------------------------- SVG primitives
HEAD = {2: (10, 8), 3: (13, 11), 6: (22, 18)}
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 3)}   # body, point, height, sign length, bar


def unit(dx, dy):
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def point_at(pts, s):
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= seg or b == pts[-1]:
            ux, uy = unit(b[0] - a[0], b[1] - a[1])
            s = min(s, seg)
            return a[0] + ux * s, a[1] + uy * s, ux, uy
        s -= seg
    a, b = pts[-2], pts[-1]
    ux, uy = unit(b[0] - a[0], b[1] - a[1])
    return b[0], b[1], ux, uy


def rounded_d(pts, r):
    if len(pts) == 2:
        return f'M{f(pts[0][0])} {f(pts[0][1])}L{f(pts[1][0])} {f(pts[1][1])}'
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(1, len(pts) - 1):
        a, p, b = pts[i - 1], pts[i], pts[i + 1]
        u1 = unit(p[0] - a[0], p[1] - a[1])
        u2 = unit(b[0] - p[0], b[1] - p[1])
        rr = min(r, math.hypot(p[0] - a[0], p[1] - a[1]) / 2, math.hypot(b[0] - p[0], b[1] - p[1]) / 2)
        p1 = (p[0] - u1[0] * rr, p[1] - u1[1] * rr)
        p2 = (p[0] + u2[0] * rr, p[1] + u2[1] * rr)
        d += f'L{f(p1[0])} {f(p1[1])}Q{f(p[0])} {f(p[1])} {f(p2[0])} {f(p2[1])}'
    d += f'L{f(pts[-1][0])} {f(pts[-1][1])}'
    return d


def trim_end(pts, by):
    """Shorten a polyline at its end by `by` px, so the line stops at the arrowhead's base."""
    pts = list(pts)
    while by > 0 and len(pts) >= 2:
        a, b = pts[-2], pts[-1]
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg > by:
            ux, uy = unit(b[0] - a[0], b[1] - a[1])
            pts[-1] = (b[0] - ux * by, b[1] - uy * by)
            return pts
        pts.pop()
        by -= seg
    return pts


def texture(grade):
    k = gkey(grade)
    return GRADE[k][2] if k else 'solid'


def fitted(tex, w, length):
    """A dash pattern in multiples of the line width, fitted so the line starts and ends on ink."""
    if tex == 'dashed':
        d, g = 4 * w, 2 * w
        n = max(2, round((length + g) / (d + g)))
        g2 = (length - n * d) / (n - 1)
        return f'{f(d)} {f(max(g2, 1))}'
    if tex == 'dash-dot':
        a, g, b = 4 * w, 1.5 * w, w
        n = max(1, round((length - a) / (a + b + 2 * g)))
        g2 = (length - (n + 1) * a - n * b) / (2 * n)
        return f'{f(a)} {f(max(g2, 1))} {f(b)} {f(max(g2, 1))}'
    if tex == 'dotted':
        g = 2.5 * w
        n = max(2, round(length / g))
        return f'0 {f(length / n)}'
    return None


BEND = {2: 8, 3: 12, 6: 18}


def tick_marks(pts, w, count):
    """Delay ticks: one, two or three, 2 px wide, 8 px longer than the line, 5 px apart, from 12 px after the tail."""
    out = []
    for i in range(count):
        x, y, ux, uy = point_at(pts, 12 + i * 5)
        nx, ny = -uy, ux
        hl = (w + 8) / 2
        out.append(f'M{f(x - nx * hl)} {f(y - ny * hl)}L{f(x + nx * hl)} {f(y + ny * hl)}')
    return f'<path class="tk" d="{"".join(out)}"/>' if out else ''


def head_shape(tip, u, w):
    hl, hb = HEAD[w]
    ang = math.degrees(math.atan2(u[1], u[0]))
    return (f'<g transform="translate({f(tip[0])} {f(tip[1])}) rotate({f(ang)})">'
            f'<path class="hd" d="M0 0L{-hl} {-hb / 2}L{-hl} {hb / 2}Z"/></g>')


def tag_shape(cx, cy, u, sign, w):
    """The pointing tag: a body and a point along the line, the sign upright in the ground color."""
    body, point, h, sl, bar = TAG[w]
    total = body + point
    ang = math.degrees(math.atan2(u[1], u[0]))
    x0 = -total / 2
    pent = (f'M{f(x0)} {f(-h / 2)}H{f(x0 + body)}L{f(x0 + total)} 0L{f(x0 + body)} {f(h / 2)}H{f(x0)}Z')
    bx = cx + u[0] * (x0 + body / 2)
    by = cy + u[1] * (x0 + body / 2)
    hs = sl / 2
    bars = f'M{f(bx - hs)} {f(by)}H{f(bx + hs)}'
    if sign == '+':
        bars += f'M{f(bx)} {f(by - hs)}V{f(by + hs)}'
    sbar = f'<path class="tgs" d="{bars}" stroke-width="{bar}"/>' if sign in ('+', '-') else ''
    return (f'<g transform="translate({f(cx)} {f(cy)}) rotate({f(ang)})"><path class="tgb" d="{pent}"/></g>{sbar}')


def diamond(tip, u, w=2):
    """Authority connections end in an open diamond, 14 by 11 px, ground fill."""
    ang = math.degrees(math.atan2(u[1], u[0]))
    return (f'<g transform="translate({f(tip[0])} {f(tip[1])}) rotate({f(ang)})">'
            f'<path class="dm" d="M0 0L-7 -5.5L-14 0L-7 5.5Z" stroke-width="{w}"/></g>')


def wire(pts, w, grade, sign, delay, *, attrs='', labels='', conceptual=False, tag_at=0.5, authority=False,
         lo=2, hi=3, sel=6, tag_pos=None):
    """One connection drawn to the frame's grammar: texture for evidence, ticks for delay, a pointing tag for the sign,
    one closed arrowhead. `attrs` makes it a kit item; `labels` is placed text."""
    w = int(w)
    tex = 'solid' if conceptual else texture(grade)
    hl = HEAD[w][0] if not authority else 14
    extra = 1.5 * w if tex == 'dotted' else 0
    body = trim_end(pts, hl + extra)
    length = poly_len(body)
    d = rounded_d(body, BEND.get(w, 8))
    css = ''
    if tex != 'solid':
        css = (f' style="--da-lo:{fitted(tex, lo, length)};--da-hi:{fitted(tex, hi, length)};'
               f'--da-sel:{fitted(tex, sel, length)}"')
    tcls = {'dashed': ' tx-dash', 'dash-dot': ' tx-dd', 'dotted': ' tx-dot'}.get(tex, '')
    tip = pts[-1]
    u = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    parts = []
    if conceptual:
        parts.append(f'<path class="hol-o ak-mark" d="{d}" fill="none" stroke-width="{w + 2}"/>'
                     f'<path class="hol-i" d="{d}" fill="none" stroke-width="{w}"/>')
    else:
        parts.append(f'<path class="ak-case{tcls}" d="{d}" fill="none"{css}/>'
                     f'<path class="ak-mark{tcls}" d="{d}" fill="none" stroke-width="{w}"{css}/>')
    if delay in TICKS and not conceptual:
        parts.append(tick_marks(body, w, TICKS[delay]))
    parts.append(diamond(tip, u, 2) if authority else head_shape(tip, u, w))
    if sign in ('+', '-'):
        if tag_pos is not None:
            cx, cy, tu = tag_pos
        else:
            tl = poly_len(body)
            cx, cy, ux, uy = point_at(body, tl * tag_at)
            tu = (ux, uy)
        parts.append(tag_shape(cx, cy, tu, sign, w))
    parts.append(f'<path class="ak-hit" d="{d}"/>')
    if attrs:
        return f'<g class="wire"{attrs}>{"".join(parts)}{labels}</g>'
    return f'<g class="wire">{"".join(parts)}{labels}</g>'


def link_attrs(lid, key=True, rel='', say=None, extra=''):
    l = L[lid]
    sg = l['polarity'] if l['polarity'] in ('+', '-') else 'none'
    a = (f' data-link="{lid}" data-sign="{sg}" data-grade="{l["evidence"]}" data-delay="{l["delay"]}"'
         f' data-from="{l["from"]}" data-to="{l["to"]}"')
    if key:
        say = say or link_say(lid)
        a = (f' role="button" data-select="{k_link(lid)}"{a} data-rel="{e(rel or (k_var(l["from"]) + " " + k_var(l["to"])))}"'
             f' aria-label="{e(say)}" data-say="{e(say)}"')
    return a + extra


def link_say(lid):
    l = L[lid]
    sg = l['polarity']
    sign = f'Sign {sign_char(sg)}, {verb(sg)}' if sg in ('+', '-') else 'No sign: a line of authority'
    return (f'{lid}: {l["name"]}. From {l["from"]} {N[l["from"]]["label"]} to {l["to"]} {N[l["to"]]["label"]}. '
            f'{sign}. Evidence {gword(l["evidence"]).lower()}. Delay {DELAY[l["delay"]]}.')


def var_say(nid):
    n = N[nid]
    return f'{nid} {n["label"]}. {n.get("increase_means") or ""}'.strip()


def text_el(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{e(s)}</text>'


def text_lines(x, y, rows, cls, lh, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    sp = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{sp}</text>'


# ---------------------------------------------------------------------------------------------------- loop cycles
CARD_W = 350
SM = dict(bw=124, label=15, lh=18, wt=600, pad=10, gap_v=84, diag=70)


def box_svg(x, y, w, h, lines, *, lh, cls_lab='bxl', nid=None, concept=False, key=None, rel='', code=None,
            interactive=False, size=15, weight=600):
    rect = (f'<rect class="bx{" bx-c" if concept else ""}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
            f'stroke-width="{1 if concept else 2}"/>')
    ty = y + (h - len(lines) * lh) / 2 + lh * 0.74
    label = text_lines(x + w / 2, ty, lines, f'{cls_lab}{" ak-label" if interactive else ""}{" bxl-c" if concept else ""}',
                       lh, 'middle')
    if nid:
        name = N[nid]['label']
        if interactive:
            say = var_say(nid)
            return (f'<g class="stn" role="button" data-select="{k_var(nid)}" data-node="{nid}" data-name="{e(name)}" '
                    f'data-rel="{e(rel)}" aria-label="{e(say)}" data-say="{e(say)}">{rect}{label}</g>')
        return f'<g class="stn" data-node="{nid}" data-name="{e(name)}">{rect}{label}</g>'
    return f'<g class="stn">{rect}{label}</g>'


def cycle_geometry(n, W, bw, bh, gap_v, diag):
    """Box origins and step routes for a cycle of n stations, clockwise from the top left."""
    if n == 2:
        b = [(0, 0), (W - bw, 0)]
        y = bh / 2
        yr = bh + 36
        routes = [
            [(bw + 2, y), (W - bw - 2, y)],
            [(W - bw / 2, bh + 2), (W - bw / 2, yr), (bw / 2, yr), (bw / 2, bh + 2)],
        ]
        H = yr
        return b, routes, H
    if n == 3:
        x0 = (W - bw) / 2
        y1 = bh + 4 + diag
        b = [(x0, 0), (W - bw, y1), (0, y1)]
        sx = x0 + bw - 22
        routes = [
            [(sx, bh + 2), (sx + diag, bh + 2 + diag)],
            [(W - bw - 2, y1 + bh / 2), (bw + 2, y1 + bh / 2)],
            [(W - sx, y1 - 2), (W - sx + diag, y1 - 2 - diag)],
        ]
        return b, routes, y1 + bh
    # four stations
    y2 = bh + gap_v
    b = [(0, 0), (W - bw, 0), (W - bw, y2), (0, y2)]
    routes = [
        [(bw + 2, bh / 2), (W - bw - 2, bh / 2)],
        [(W - bw / 2, bh + 2), (W - bw / 2, y2 - 2)],
        [(W - bw - 2, y2 + bh / 2), (bw + 2, y2 + bh / 2)],
        [(bw / 2, y2 - 2), (bw / 2, bh + 2)],
    ]
    return b, routes, y2 + bh


def step_label_pos(n, i, route, W, bw, bh):
    """Where a small cycle's step label sits, as (x, y, anchor, below)."""
    (x1, y1), (x2, y2) = route[0], route[-1]
    if n == 2:
        if i == 0:
            return (W / 2, y1 - 12, 'middle', 'split')
        return (W / 2, route[1][1] + 26, 'middle', 'stack')
    if n == 3:
        if i == 0:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            return (mx + 16, my - 4, 'start', 'stack')
        if i == 1:
            return (W / 2, y1 - 12, 'middle', 'split')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        return (mx - 16, my - 4, 'end', 'stack')
    if i == 0:
        return (W / 2, y1 - 12, 'middle', 'split')
    if i == 1:
        return (x1 - 16, (y1 + y2) / 2 - 4, 'end', 'stack')
    if i == 2:
        return (W / 2, y1 - 12, 'middle', 'split')
    return (x1 + 16, (y1 + y2) / 2 - 4, 'start', 'stack')


def cycle_svg(lp, *, uid, interactive=False, numbered=False, view='loop'):
    """A loop as a named box-and-arrow cycle at card size (350 px wide, text 13 to 15 px at 1:1)."""
    o = LO[lp]
    st = o['stations']
    n = len(st)
    W, bw = CARD_W, SM['bw']
    labs = [wrap(station_label(s), bw - 2 * SM['pad'], SM['label'], SM['wt']) for s in st]
    bh = max(len(x) for x in labs) * SM['lh'] + 22
    boxes, routes, H = cycle_geometry(n, W, bw, bh, SM['gap_v'], SM['diag'])
    top = 4
    parts, wires = [], []
    for i, s in enumerate(o['steps']):
        route = [(x, y + top) for x, y in routes[i]]
        lab_x, lab_y, anchor, mode = step_label_pos(n, i, route, W, bw, bh)
        weakest = s['id'] in (o['weakest'] or [])
        vw = verb(s['polarity'])
        word = f'{s["index"]} {vw}' if numbered else vw
        if mode == 'split':
            lab = text_el(lab_x, lab_y, word, 'wl', anchor)
            if weakest:
                lab += text_el(lab_x, lab_y + 36, 'weakest step', 'wn', anchor)
        else:
            rows = [word] + (['weakest step'] if weakest else [])
            lab = text_lines(lab_x, lab_y, rows, 'wl', 17, anchor)
            if weakest:
                lab = (text_el(lab_x, lab_y, word, 'wl', anchor) + text_el(lab_x, lab_y + 17, 'weakest step', 'wn', anchor))
        if s['conceptual']:
            wires.append(wire(route, 2, None, s['polarity'], None, conceptual=True, labels=lab))
        else:
            to = s['to']
            rel = f'{k_var(s["from"])} {k_var(to)}'
            attrs = link_attrs(s['id'], key=interactive, rel=rel)
            wires.append(wire(route, 2, s['evidence'], s['polarity'], s['delay'], attrs=attrs, labels=lab))
    for i, s in enumerate(st):
        bx, by = boxes[i]
        nid = s['code'] if s.get('is_variable') and s.get('code') in N else None
        rel = ''
        if nid and interactive:
            rel = ' '.join(k_link(x['id']) for x in o['steps'] if x['id'] and nid in (x['from'], x['to']))
        parts.append(box_svg(bx, by + top, bw, bh, labs[i], lh=SM['lh'], nid=nid, concept=not nid,
                             interactive=interactive and bool(nid), rel=rel))
    Ht = H + top + (50 if n == 2 else 8)
    if n == 2:
        Ht = routes[1][1][1] + top + 26 + 22
    steps = 'sketch' if o['conceptual'] else ' '.join(x['id'] for x in o['steps'])
    seq = ''
    if interactive:
        # DOM order is the loop's order, so the arrow keys walk it: station, step, station, step
        order = []
        for i in range(n):
            order.append(parts[i])
            order.append(wires[i])
        body = ''.join(order)
        seq = ' data-ak-roving data-ak-nav="sequence" data-ak-wrap'
    else:
        body = ''.join(wires) + ''.join(parts)
    lab = f' role="group" aria-label="{e(lp + ", " + o["plain_name"] + ": " + read_aloud(lp))}"' if not interactive else \
        f' role="group" aria-labelledby="h-{view}"'
    return (f'<svg class="cyc" data-view="{e(view)}-{uid}" viewBox="0 0 {W} {f(Ht)}" width="{W}" height="{f(Ht)}"'
            f'{lab}{seq} style="--ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px">{body}</svg>'), steps


# the R10 loop at full size, with its step labels written out and R-01's targets marked by the kit
def r10_large(lp='R10', uid='lg', marks=True, view='loop-r10'):
    o = LO[lp]
    st = o['stations']
    W, bw, bh, gv, top = 880, 280, 0, 212, 40
    # box contents: icon, chip, label, and "a higher value means"
    rows = []
    for s in st:
        nid = s['code']
        lab = wrap(N[nid]['label'], bw - 32 - 48 - 14, 20, 700, tight=True)
        inc = wrap(N[nid]['increase_means'], bw - 32, 14, 400)
        rows.append((lab, inc))
    bh = max(16 + max(48, 26 + len(lb) * 22) + 12 + len(inc) * 20 + 14 for lb, inc in rows)
    y2 = bh + gv
    pos = [(0, 0), (W - bw, 0), (W - bw, y2), (0, y2)]
    routes = [
        [(bw + 2, bh / 2), (W - bw - 2, bh / 2)],
        [(W - bw / 2, bh + 2), (W - bw / 2, y2 - 2)],
        [(W - bw - 2, y2 + bh / 2), (bw + 2, y2 + bh / 2)],
        [(bw / 2, y2 - 2), (bw / 2, bh + 2)],
    ]
    items = []
    state = 1
    markers = []
    for i, s in enumerate(st):
        nid = s['code']
        x, y = pos[i]
        y += top
        lab, inc = rows[i]
        rel = ' '.join(k_link(x2['id']) for x2 in o['steps'] if nid in (x2['from'], x2['to']))
        ic = icon_svg(acc.VARIABLE_ICON[nid], 'black', uid=f'{uid}-{nid.lower()}', size=48)
        ic = ic.replace('<svg ', f'<svg x="{f(x + 16)}" y="{f(y + 16)}" ', 1)
        tl = text_el(x + 16 + 48 + 14, y + 16 + 15, nid, 'bxc')
        tlab = text_lines(x + 16 + 48 + 14, y + 16 + 26 + 17, lab, 'bxs ak-label', 22)
        ty = y + 16 + max(48, 26 + len(lab) * 22) + 12 + 14
        tinc = text_lines(x + 16, ty, inc, 'bxi', 20)
        say = var_say(nid)
        items.append((i, f'<g class="stn" role="button" data-select="{k_var(nid)}" data-node="{nid}" data-name="{e(N[nid]["label"])}" '
                         f'data-rel="{e(rel)}" aria-label="{e(say)}" data-say="{e(say)}">'
                         f'<rect class="bx" x="{f(x)}" y="{f(y)}" width="{bw}" height="{f(bh)}" stroke-width="3"/>'
                         f'{ic}{tl}{tlab}{tinc}</g>'))
    # step labels
    for i, s in enumerate(o['steps']):
        lid = s['id']
        lk = L[lid]
        route = [(x, y + top) for x, y in routes[i]]
        weakest = lid in (o['weakest'] or [])
        head = f'Step {s["index"]} · {lid}'
        name = wrap(lk['name'], 300 if i in (0, 2) else 250, 15, 600)
        v = f'{sign_char(lk["polarity"])} {verb(lk["polarity"])} · {DELAY[lk["delay"]]}'
        g = gfull(lk['evidence'])
        tail = ['The weakest step'] if weakest else []
        if i in (0, 2):
            cx = W / 2
            ly = route[0][1]
            above = text_el(cx, ly - 14 - 18 * len(name) - 4, head, 'sh', 'middle') + \
                text_lines(cx, ly - 14 - 18 * (len(name) - 1), name, 'sn', 18, 'middle')
            below = text_lines(cx, ly + 30, [v, g] + tail, 'sv', 19, 'middle')
            lab = above + below
        else:
            x1 = route[0][0]
            anchor = 'end' if i == 1 else 'start'
            lx = x1 - 22 if i == 1 else x1 + 22
            my = (route[0][1] + route[-1][1]) / 2
            block = [(head, 'sh', 17)] + [(r, 'sn', 18) for r in name] + [(v, 'sv', 19), (g, 'sv', 19)] + [(t, 'sv', 19) for t in tail]
            hgt = sum(b[2] for b in block)
            yy = my - hgt / 2 + 13
            lab = ''
            for t, c, lh in block:
                lab += text_el(lx, yy, t, c, anchor)
                yy += lh
        rel = f'{k_var(s["from"])} {k_var(s["to"])}'
        items.append((i + 0.5, wire(route, 3, s['evidence'], s['polarity'], s['delay'], attrs=link_attrs(lid, rel=rel),
                                    labels=lab, lo=3, hi=3, sel=6)))
        # the stepper's markers: what each station reads as the change travels
        state *= 1 if s['polarity'] == '+' else -1
        word = 'more' if state > 0 else 'less'
        if marks:
            tx, ty = pos[(i + 1) % 4]
            ty += top
            if (i + 1) % 4 == 0:
                markers.append(text_el(tx + bw, ty - 12, f'Back here: {word} again', 'mk', 'end', f' data-ak-at="{i + 1}"'))
            elif (i + 1) % 4 in (1,):
                markers.append(text_el(tx + bw, ty - 12, f'Step {i + 1}: {word}', 'mk', 'end', f' data-ak-at="{i + 1}"'))
            else:
                markers.append(text_el(tx + bw, ty + bh + 22, f'Step {i + 1}: {word}', 'mk', 'end', f' data-ak-at="{i + 1}"'))
    if marks:
        markers.append(text_el(pos[0][0], pos[0][1] + top - 12, f'Start: more {low(N[st[0]["code"]]["label"], st[0]["code"])}',
                               'mk', 'start', ' data-ak-at="0"'))
    H = y2 + bh + top + 34
    body = ''.join(x[1] for x in sorted(items, key=lambda t: t[0])) + ''.join(markers)
    return (f'<svg class="cyc-lg" data-view="{view}-{uid}" viewBox="0 0 {W} {f(H)}" width="{W}" height="{f(H)}" role="group" '
            f'aria-labelledby="h-{view}" data-ak-roving data-ak-nav="sequence" data-ak-wrap '
            f'style="--ak-w-lo:3px;--ak-w-hi:3px;--ak-w-sel:6px">{body}</svg>')


# ---------------------------------------------------------------------------------------------------- area C floor drawing
def floor_c_svg(uid='fc'):
    """The Elections floor as a plan: five rooms in a row and the five connections inside the floor."""
    nodes = PARTS['C']['nodes']
    W, bw = 944, 128
    gap = (W - 5 * bw) / 4
    top = 70
    labs = [wrap(N[n]['label'], bw - 20, 15, 600) for n in nodes]
    bh = 16 + 48 + 10 + max(len(x) for x in labs) * 18 + 12
    X = {n: i * (bw + gap) for i, n in enumerate(nodes)}
    inside = [k for k in INSIDE if PART_OF[L[k]['from']] == 'C']
    parts = []
    for n in nodes:
        x = X[n]
        rel = ' '.join(k_link(k) for k in L if n in (L[k]['from'], L[k]['to']) and k in inside)
        ic = icon_svg(acc.VARIABLE_ICON[n], 'black', uid=f'{uid}-{n.lower()}', size=48)
        ic = ic.replace('<svg ', f'<svg x="{f(x + bw / 2 - 24)}" y="{f(top + 14)}" ', 1)
        say = var_say(n)
        parts.append(f'<g class="stn" role="button" data-select="{k_var(n)}" data-node="{n}" data-name="{e(N[n]["label"])}" '
                     f'data-rel="{e(rel)}" aria-label="{e(say)}" data-say="{e(say)}">'
                     f'<rect class="bx" x="{f(x)}" y="{top}" width="{bw}" height="{f(bh)}" stroke-width="2"/>'
                     f'{text_el(x + 10, top + 22, n, "bxc")}{ic}'
                     f'{text_lines(x + bw / 2, top + 16 + 48 + 10 + 14, labs[nodes.index(n)], "bxl ak-label", 18, "middle")}</g>')
    wires = []
    ymid = top + bh / 2
    for k in inside:
        l = L[k]
        a, b = l['from'], l['to']
        ia, ib = nodes.index(a), nodes.index(b)
        weak = any(k in (LO[lp]['weakest'] or []) for lp in ('R10',))
        rel = f'{k_var(a)} {k_var(b)}'
        if ib == ia + 1:
            x1, x2 = X[a] + bw + 2, X[b] - 2
            route = [(x1, ymid), (x2, ymid)]
            lab = text_el((x1 + x2) / 2, ymid - 14, verb(l['polarity']), 'wl', 'middle')
            lab += text_el((x1 + x2) / 2, ymid + 30, k, 'wn', 'middle')
        elif ib < ia:
            ya = top + bh + 44
            xa, xb = X[a] + bw / 2, X[b] + bw / 2
            route = [(xa, top + bh + 2), (xa, ya), (xb, ya), (xb, top + bh + 2)]
            lab = text_el((xa + xb) / 2, ya + 26, f'{k} {verb(l["polarity"])}', 'wl', 'middle')
        else:
            ya = top - 40
            xa, xb = X[a] + bw / 2 + 20, X[b] + bw / 2
            route = [(xa, top - 2), (xa, ya), (xb, ya), (xb, top - 2)]
            lab = text_el((xa + xb) / 2, ya - 12, f'{k} {verb(l["polarity"])}', 'wl', 'middle')
        wires.append(wire(route, 2, l['evidence'], l['polarity'], l['delay'], attrs=link_attrs(k, rel=rel), labels=lab))
    H = top + bh + 44 + 40
    return (f'<svg class="floorplan" data-view="area-c-floor" viewBox="0 0 {W} {f(H)}" width="{W}" height="{f(H)}" role="group" '
            f'aria-labelledby="h-floor" data-ak-roving data-ak-nav="spatial" style="--ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px">'
            f'{"".join(wires)}{"".join(parts)}</svg>')


def floor_c_svg_v(uid='fv'):
    """The same floor plan for a phone: rooms stacked, the return on the left, the skip on the right, 350 px wide."""
    nodes = PARTS['C']['nodes']
    W, x0, bw, bh, gap, top = 350, 44, 238, 72, 76, 6
    inside = [k for k in INSIDE if PART_OF[L[k]['from']] == 'C']
    Y = {n: top + i * (bh + gap) for i, n in enumerate(nodes)}
    parts = []
    for n in nodes:
        y = Y[n]
        rel = ' '.join(k_link(k) for k in inside if n in (L[k]['from'], L[k]['to']))
        lab = wrap(N[n]['label'], bw - 12 - 48 - 12 - 10, 15, 600)
        ic = icon_svg(acc.VARIABLE_ICON[n], 'black', uid=f'{uid}-{n.lower()}', size=48)
        ic = ic.replace('<svg ', f'<svg x="{x0 + 12}" y="{f(y + (bh - 48) / 2)}" ', 1)
        ty = y + (bh - (16 + len(lab) * 18)) / 2 + 13
        say = var_say(n)
        parts.append(f'<g class="stn" role="button" data-select="{k_var(n)}" data-node="{n}" data-name="{e(N[n]["label"])}" '
                     f'data-rel="{e(rel)}" aria-label="{e(say)}" data-say="{e(say)}">'
                     f'<rect class="bx" x="{x0}" y="{f(y)}" width="{bw}" height="{bh}" stroke-width="2"/>{ic}'
                     f'{text_el(x0 + 12 + 48 + 12, ty, n, "bxc")}'
                     f'{text_lines(x0 + 12 + 48 + 12, ty + 18, lab, "bxl ak-label", 18)}</g>')
    wires = []
    cx = x0 + bw / 2
    for k in inside:
        l = L[k]
        a, b = l['from'], l['to']
        ia, ib = nodes.index(a), nodes.index(b)
        rel = f'{k_var(a)} {k_var(b)}'
        word = f'{verb(l["polarity"])} · {k}'
        if ib == ia + 1:
            route = [(cx, Y[a] + bh + 2), (cx, Y[b] - 2)]
            lab = text_el(cx + 18, Y[a] + bh + gap / 2 + 5, word, 'wl')
        elif ib < ia:
            xr = 18
            ya, yb = Y[a] + bh / 2, Y[b] + bh / 2
            route = [(x0 - 2, ya), (xr, ya), (xr, yb), (x0 - 2, yb)]
            gy = Y[nodes[1]] + bh + gap / 2 + 5
            lab = text_el(xr + 12, gy, word, 'wl')
        else:
            xr = W - 14
            ya, yb = Y[a] + bh / 2, Y[b] + bh / 2
            route = [(x0 + bw + 2, ya), (xr, ya), (xr, yb), (x0 + bw + 2, yb)]
            gy = Y[nodes[3]] + bh + gap / 2 + 5
            lab = text_el(xr - 12, gy, word, 'wl', 'end')
        wires.append(wire(route, 2, l['evidence'], l['polarity'], l['delay'], attrs=link_attrs(k, rel=rel), labels=lab))
    H = Y[nodes[-1]] + bh + 8
    return (f'<svg class="floorplan" data-view="area-c-floor-v" viewBox="0 0 {W} {f(H)}" width="{W}" height="{f(H)}" role="group" '
            f'aria-labelledby="h-floor" data-ak-roving data-ak-nav="spatial" style="--ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px">'
            f'{"".join(wires)}{"".join(parts)}</svg>')


def conn_line_svg(lid, uid):
    """A connection drawn on its own: texture, ticks, tag and head, 136 px long."""
    l = L[lid]
    auth = l['type'] == 'authority'
    w = wire([(2, 12), (134, 12)], 2, l['evidence'], l['polarity'], l['delay'], authority=auth)
    return f'<svg class="cline" data-view="line-{uid}" viewBox="0 0 136 24" width="136" height="24" aria-hidden="true">{w}</svg>'


# ---------------------------------------------------------------------------------------------------- locator
def locator_svg(here, uid, note):
    """A small elevation of the building: the floor in view in heavy ink, the rest in outline. Never red."""
    rows = STACK
    W, rh, gap = 196, 14, 4
    out = []
    y = 4
    for pid in rows:
        on = pid in here
        out.append(f'<rect x="1" y="{y}" width="40" height="{rh}" class="{"lc-on" if on else "lc-off"}"/>'
                   f'{text_el(50, y + 11, pname(pid), "lct" + (" on" if on else ""))}')
        y += rh + gap
        if pid == 'A':
            out.append(f'<path d="M0 {y - 2}H44" class="lc-ground"/>')
    H = y + 2
    return (f'<svg class="loc" data-view="locator-{uid}" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{e(note)}">{"".join(out)}</svg>')


def mini_floors(nodes, uid):
    """A loop card's tiny elevation: the floors its stations stand on."""
    on = {PART_OF[n] for n in nodes if n in PART_OF}
    out, y = [], 1
    for pid in STACK:
        out.append(f'<rect x="1" y="{y}" width="30" height="6" class="{"lc-on" if pid in on else "lc-off"}"/>')
        y += 9
    return f'<svg class="mini" viewBox="0 0 32 {y}" width="32" height="{y}" aria-hidden="true">{"".join(out)}</svg>'


# ---------------------------------------------------------------------------------------------------- panel templates
def src_line():
    return f'<p class="p-src">Atlas V7, snapshot {SNAP_WORDS}.</p>'


def h3(t):
    return f'<h3>{e(t)}</h3>'


def tpl(key, kind, title, body):
    return f'<template data-detail="{e(key)}" data-kind="{e(kind)}" data-title="{e(title)}">{body}{src_line()}</template>'


def link_li(lid, show_ends=True):
    l = L[lid]
    sg = l['polarity']
    ends = f' <span class="p-ends">{e(N[l["from"]]["label"])} to {e(N[l["to"]]["label"])}</span>' if show_ends else ''
    sign = f'{sign_char(sg)} {verb(sg)}' if sg in ('+', '-') else 'decides'
    return (f'<li>{chip("Connection", lid, True)} {e(l["name"])}.{ends} '
            f'<span class="p-meta">{e(sign)} · {e(gword(l["evidence"]))} · {e(DELAY[l["delay"]])}</span></li>')


def loop_li(lp):
    o = LO[lp]
    return (f'<li><a href="{loop_href(lp)}">{chip("Loop", lp, True)} {e(o["plain_name"])}</a> '
            f'<span class="p-meta">{e(kind_line(lp))}</span></li>')


def reform_li(rid):
    r = RF[rid]
    inner = f'{chip("Reform", rid, True)} {e(r["title"])}'
    if rid == 'R-01':
        inner = f'<a href="#reform-r01">{inner}</a>'
    return f'<li>{inner}</li>'


def issue_titles(iss, cap=8):
    out = ''.join(f'<li>{e(i["title"])} <span class="p-meta">{e(gword(i["grade"]))}</span></li>' for i in iss[:cap])
    more = f'<li class="p-more">and {len(iss) - cap} more</li>' if len(iss) > cap else ''
    return f'<ul class="p-list">{out}{more}</ul>'


def tpl_var(nid):
    n = N[nid]
    rest, ok = increase_rest(nid)
    outs = [k for k, l in L.items() if l['from'] == nid]
    ins = [k for k, l in L.items() if l['to'] == nid]
    iss = issues_for_nodes([nid])
    refs = [r for r in sorted(RF, key=lambda r: int(r.split('-')[1])) if nid in RF[r]['targets']
            or any(t in L and nid in (L[t]['from'], L[t]['to']) for t in RF[r]['targets'])]
    b = f'<p class="p-formal">{e(n["title"])}</p>' if n['title'] != n['label'] else ''
    b += h3('What it is') + f'<p>{e(n.get("description") or "")}</p>'
    b += (h3('A higher value means') + f'<p>{e(rest)}</p>') if ok else (h3('Reading it') + f'<p>{e(rest)}</p>')
    if n.get('why'):
        b += h3('Why it matters') + f'<p>{e(n["why"])}</p>'
    if n['loops']:
        b += h3(f'Its loops ({len(n["loops"])})') + '<ul class="p-list">' + ''.join(loop_li(x) for x in n['loops']) + '</ul>'
    else:
        b += h3('Its loops') + '<p>No loop runs through this variable.</p>'
    b += h3(f'Pushes on ({len(outs)})') + '<ul class="p-list">' + ''.join(link_li(k) for k in outs) + '</ul>'
    b += h3(f'Pushed by ({len(ins)})') + '<ul class="p-list">' + ''.join(link_li(k) for k in ins) + '</ul>'
    b += h3(f'Issues tracked here ({len(iss)})') + (issue_titles(iss) if iss else '<p>No issue record names it.</p>')
    b += h3(f'Reforms aimed here ({len(refs)})') + ('<ul class="p-list">' + ''.join(reform_li(r) for r in refs) + '</ul>'
                                                     if refs else '<p>No reform aims at it or its connections.</p>')
    if PART_OF[nid] == 'C':
        b += '<p class="p-next"><a href="#area-c">Open the Elections floor</a></p>'
    return tpl(k_var(nid), f'Variable {nid}', n['label'], b)


def part_counts(pid):
    nodes = PARTS[pid]['nodes']
    return dict(vars=len(nodes), loops=len(loops_through(nodes)), home=len(HOME.get(pid, [])),
                issues=len(issues_for_nodes(nodes)), reforms=len(reforms_for_nodes(nodes)))


def tpl_part(pid):
    p = PARTS[pid]
    nodes = p['nodes']
    c = part_counts(pid)
    b = f'<p class="p-lead">{e(p["formal_title"])}</p>'
    if p.get('plain_question'):
        b += f'<p class="p-q">{e(p["plain_question"])}</p>'
    b += h3(p['chapter'] or 'What it is') + f'<p>{e(p["story"])}</p>'
    b += h3(f'Its variables ({len(nodes)})') + '<ul class="p-list">' + ''.join(
        f'<li>{chip("Variable", nid, True)} {e(N[nid]["label"])}</li>' for nid in nodes) + '</ul>'
    fl = []
    for (a, bb), ks in sorted(FLOWS.items(), key=lambda t: (-len(t[1]), t[0])):
        if a == pid:
            fl.append(f'<li>{len(ks)} to {e(pname(bb))}</li>')
    fi = []
    for (a, bb), ks in sorted(FLOWS.items(), key=lambda t: (-len(t[1]), t[0])):
        if bb == pid:
            fi.append(f'<li>{len(ks)} from {e(pname(a))}</li>')
    ins = sum(1 for k in INSIDE if PART_OF[L[k]['from']] == pid)
    b += h3('Connections') + f'<p>{plural(ins, "connection")} inside this floor.</p>'
    if fl:
        b += f'<p class="p-sub">Pushes on</p><ul class="p-list">{"".join(fl)}</ul>'
    if fi:
        b += f'<p class="p-sub">Pushed by</p><ul class="p-list">{"".join(fi)}</ul>'
    home = HOME.get(pid, [])
    thr = loops_through(nodes)
    if thr:
        b += h3(f'Loops through it ({len(thr)})') + '<ul class="p-list">' + ''.join(loop_li(x) for x in thr) + '</ul>'
    iss = issues_for_nodes(nodes)
    b += h3(f'Issues tracked here ({len(iss)})') + (issue_titles(iss, 10) if iss else '<p>None.</p>')
    refs = reforms_for_nodes(nodes)
    b += h3(f'Reforms aimed here ({len(refs)})') + ('<ul class="p-list">' + ''.join(reform_li(r) for r in refs) + '</ul>'
                                                     if refs else '<p>None.</p>')
    if pid == 'C':
        b += '<p class="p-next"><a href="#area-c">Open the Elections floor</a></p>'
    code = pid
    return tpl(k_area(pid), f'Area {code}', p['plain_name'], b)


def tpl_flow(a, bb):
    up, down = flow_links(a, bb), flow_links(bb, a)
    b = f'<p class="p-lead">{plural(len(up), "connection")} pass up from {e(pname(a))} to {e(pname(bb))}.</p>'
    b += '<ul class="p-list">' + ''.join(link_li(k) for k in up) + '</ul>'
    if down:
        b += h3(f'Back down from {pname(bb)} to {pname(a)} ({len(down)})') + '<ul class="p-list">' + ''.join(
            link_li(k) for k in down) + '</ul>'
    else:
        b += h3('Back down') + f'<p>No connection runs from {e(pname(bb))} down to {e(pname(a))}.</p>'
    b += f'<p class="p-note">{e(GLOSS["Positive sign (+)"])}</p>'
    return tpl(f'flow-{a.lower()}-{bb.lower()}', 'Flow between floors', f'{pname(a)} to {pname(bb)}', b)


def tpl_return():
    b = f'<p class="p-quote">{e(DATA["opening"]["return"])}</p>'
    b += (f'<p class="p-lead">{plural(len(RETURN), "connection")} run back down from Policy: '
          f'{len(flow_links("E", "A"))} into Wealth and {len(flow_links("E", "EC"))} into Your household.</p>')
    b += '<ul class="p-list">' + ''.join(link_li(k) for k in RETURN) + '</ul>'
    b += h3('Why it matters') + f'<p>{e(DATA["opening"]["paras"][1])}</p>'
    return tpl('flow-return', 'Return line', 'Policy back down to Wealth', b)


def tpl_pathway(pw):
    refs = pw['model_refs']
    hub = next(h for h in DATA['hubs'] if h['id'] == pw['hub'])
    b = f'<p class="p-lead">{e(hub["title"])}: {e(pw["title"])}</p>'
    b += h3('The short answer') + f'<p>{e(pw["short_answer"])}</p>'
    on = {}
    for nid in refs['nodes']:
        on.setdefault(PART_OF[nid], []).append(nid)
    rows = ''.join(f'<li><strong>{e(pname(pid))}</strong>: ' + ', '.join(e(N[n]["label"]) for n in on[pid]) + '</li>'
                   for pid in STACK + ['X'] if pid in on)
    b += h3('Where it sits in the building') + f'<p>The lit tiles show it.</p><ul class="p-list">{rows}</ul>'
    if refs['loops']:
        b += h3(f'Loops ({len(refs["loops"])})') + '<ul class="p-list">' + ''.join(loop_li(x) for x in refs['loops']) + '</ul>'
    if refs['reforms']:
        b += h3(f'Reforms ({len(refs["reforms"])})') + '<ul class="p-list">' + ''.join(reform_li(r) for r in refs['reforms']) + '</ul>'
    iss = [IS[i] for i in refs['issues'] if i in IS]
    if iss:
        b += h3(f'Issues ({len(iss)})') + issue_titles(iss, 6)
    return tpl('q-' + pw['id'].lower(), f'Question {pw["id"]}', pw['question'], b)


def tpl_link(lid):
    l = L[lid]
    sg = l['polarity']
    b = f'<p class="p-lead">{e(l.get("plain") or "")}</p>'
    sign = f'{sign_char(sg)} {verb(sg)}' if sg in ('+', '-') else 'No sign'
    b += ('<dl class="p-dl">'
          f'<dt>From</dt><dd>{chip("Variable", l["from"], True)} {e(N[l["from"]]["label"])}</dd>'
          f'<dt>To</dt><dd>{chip("Variable", l["to"], True)} {e(N[l["to"]]["label"])}</dd>'
          f'<dt>Sign</dt><dd>{e(sign)}. {e(l.get("sign_meaning") or "")}</dd>'
          f'<dt>Kind</dt><dd>{e(l["type"].capitalize())}</dd>'
          f'<dt>Delay</dt><dd>{e(DELAY[l["delay"]].capitalize())}</dd>'
          f'<dt>Evidence</dt><dd>{e(gfull(l["evidence"]))}</dd></dl>')
    if l.get('mechanism'):
        b += h3('How it works') + f'<p>{e(l["mechanism"])}</p>'
    if l.get('qualification'):
        b += h3('Keep in mind') + f'<p>{e(l["qualification"])}</p>'
    if l.get('counterevidence'):
        b += h3('Counterevidence') + f'<p>{e(l["counterevidence"])}</p>'
    if l['loops']:
        b += h3(f'On loops ({len(l["loops"])})') + '<ul class="p-list">' + ''.join(loop_li(x) for x in l['loops']) + '</ul>'
    refs = [r for r in sorted(RF, key=lambda r: int(r.split('-')[1])) if lid in RF[r]['targets']]
    if refs:
        b += h3('Reforms aimed at it') + '<ul class="p-list">' + ''.join(reform_li(r) for r in refs) + '</ul>'
    return tpl(k_link(lid), f'Connection {lid}', l['name'], b)


def steps_list(lp):
    o = LO[lp]
    if o['conceptual']:
        rows = ''.join(f'<li>{e(s["from_label"])} {verb(s["polarity"])} {e(low(s["to_label"]))}. '
                       f'<span class="p-meta">Conceptual step, no numbered connection</span></li>' for s in o['steps'])
    else:
        rows = ''.join(link_li(s['id']) for s in o['steps'])
    return f'<ol class="p-list">{rows}</ol>'


def tpl_loop(lp):
    o = LO[lp]
    b = f'<p class="p-lead">{e(o["title"])}</p><p class="p-kind">{e(lp)} · {e(kind_line(lp))}</p>'
    cn = closure_note(lp)
    if cn:
        b += f'<p class="p-note">{e(cn.capitalize())}.</p>'
    b += h3('Read it aloud') + f'<p class="p-read">{e(read_aloud(lp))}</p>'
    b += h3('What happens') + f'<p>{e(o["summary"])}</p>'
    b += h3('Steps') + steps_list(lp)
    b += h3('Status') + f'<p>{e(status_line(lp))}</p>'
    if o.get('evidence_summary'):
        b += h3('Evidence') + f'<p>{e(o["evidence_summary"])}</p>'
    if o.get('qualification'):
        b += h3('Keep in mind') + f'<p>{e(o["qualification"])}</p>'
    if o['reforms']:
        b += h3(f'Reforms aimed at it ({len(o["reforms"])})') + '<ul class="p-list">' + ''.join(reform_li(r) for r in o['reforms']) + '</ul>'
    if lp == 'R10':
        b += '<p class="p-next"><a href="#loop-r10">Open loop R10 at full size</a></p>'
    return tpl(k_loop(lp), f'Loop {lp}', o['plain_name'], b)


def effects_rows(rid):
    r = RF[rid]
    rows = ''
    for fam, name in DATA['families'].items():
        code = r['effects'].get(fam)
        rows += f'<dt>{e(name)}</dt><dd>{e(DATA["effect_codes"].get(code, code or "not rated").capitalize())}</dd>'
    return f'<dl class="p-dl">{rows}</dl><p class="p-note">The four families are never added together.</p>'


def tpl_reform(rid):
    r = RF[rid]
    tg = ', '.join(r['targets'])
    b = f'<p class="p-lead">{e(r["summary"])}</p>'
    if rid in DISCLOSE:
        b += f'<p class="p-disc"><strong>Disclosure.</strong> {e(DISCLOSE[rid])}</p>'
    b += ('<dl class="p-dl">'
          f'<dt>Targets</dt><dd>{e(tg)}</dd><dt>Loops</dt><dd>{e(", ".join(r["loops"]) or "None")}</dd>'
          f'<dt>Band</dt><dd>{e((r.get("band") or "").capitalize())}</dd>'
          f'<dt>Problem evidence</dt><dd>{e(gfull(r["problem_evidence"]["grade"]))}</dd>'
          f'<dt>Remedy evidence</dt><dd>{e(gfull(r["remedy_evidence"]["grade"]))}</dd></dl>')
    b += h3('What it changes') + f'<p>{e(r["what_it_changes"])}</p>'
    b += h3('Likely effects') + effects_rows(rid)
    st = r.get('status') or {}
    if st.get('text'):
        b += h3('Status') + f'<p>{e(st["text"])}</p><p class="p-meta">Checked {e(date_words(st.get("checked")) or "with no date in V7")}</p>'
    if rid == 'R-01':
        b += '<p class="p-next"><a href="#reform-r01">Open reform R-01 in full</a></p>'
    return tpl(k_reform(rid), f'Reform {rid}', r['title'], b)


# ---------------------------------------------------------------------------------------------------- icons
def icon_svg(icon_id, edition='black', uid='', size=None):
    """icon_svg() exactly as drawn. Only the icons' own data-part metadata (base, accent) is renamed data-icon-part,
    because the atlas contract reads data-part as an atlas part (A to E, X, EC, TC). No path, stroke or color changes."""
    return acc.icon_svg(icon_id, edition, uid=uid, size=size).replace(' data-part="', ' data-icon-part="')


def icon(nid_or_icon, edition='black', uid='', size=48, variable=True):
    ic = acc.VARIABLE_ICON[nid_or_icon] if variable else nid_or_icon
    return icon_svg(ic, edition, uid=uid, size=size)


HUB_ICON = {'cost-of-living': 'CL-063', 'health-and-care': 'CL-067', 'work-and-security': 'CL-061',
            'community-services': 'CL-031', 'voice-and-power': 'CL-001'}


# ---------------------------------------------------------------------------------------------------- overview
def tile(nid, uid):
    n = N[nid]
    rel = set()
    for k, l in L.items():
        if nid in (l['from'], l['to']):
            other = l['to'] if l['from'] == nid else l['from']
            rel.add(k_var(other))
            a, b = PART_OF[l['from']], PART_OF[l['to']]
            for lo_, up_ in ADJ:
                if {a, b} == {lo_, up_}:
                    rel.add(f'flow-{lo_.lower()}-{up_.lower()}')
            if k in RETURN:
                rel.add('flow-return')
    say = var_say(nid)
    return (f'<li><button type="button" class="tile" data-select="{k_var(nid)}" data-node="{nid}" data-name="{e(n["label"])}" '
            f'data-rel="{e(" ".join(sorted(rel)))}" data-say="{e(say)}">'
            f'<span class="tl-code">{nid}</span>'
            f'<span class="tl-ic k">{icon(nid, "black", f"{uid}-{nid.lower()}")}</span>'
            f'<span class="tl-ic r">{icon(nid, "red-black", f"{uid}-{nid.lower()}r")}</span>'
            f'<span class="tl-lab">{e(n["label"])}</span></button></li>')


def floor_id(pid):
    p = PARTS[pid]
    nodes = p['nodes']
    rel = [k_var(x) for x in nodes]
    for lo_, up_ in ADJ:
        if pid in (lo_, up_):
            rel.append(f'flow-{lo_.lower()}-{up_.lower()}')
    if pid in ('E', 'A', 'EC'):
        rel.append('flow-return')
    q = p.get('plain_question')
    say = f'{p["plain_name"]}, {p["formal_title"]}. {q or ""} {part_sentence(pid)}'.replace('  ', ' ')
    qh = f'<span class="fl-q">{e(q)}</span>' if q else ''
    return (f'<button type="button" class="fl-id" data-select="{k_area(pid)}" data-part="{pid}" data-name="{e(p["plain_name"])}" '
            f'data-rel="{e(" ".join(rel))}" data-say="{e(say)}">'
            f'<span class="fl-mark" aria-hidden="true">{pid}</span>'
            f'<span class="fl-name">{e(p["plain_name"])}</span>'
            f'<span class="fl-formal">{e(p["formal_title"])}</span>{qh}</button>')


def floor_html(pid, row):
    p = PARTS[pid]
    c = part_counts(pid)
    nodes = p['nodes']
    surface = ' data-surface="newsprint"' if pid in ('EC', 'TC') else ''
    if p.get('groups'):
        tiles = ''.join(f'<div class="grp"><p class="grp-t">{e(g["title"])}</p>'
                        f'<ul class="tiles" style="--cols:2">{"".join(tile(n, "ov") for n in g["nodes"])}</ul></div>'
                        for g in p['groups'])
        tiles = f'<div class="grps">{tiles}</div>'
    else:
        cols = len(nodes) if len(nodes) <= 6 else math.ceil(len(nodes) / 2)
        tiles = f'<ul class="tiles" style="--cols:{cols}">{"".join(tile(n, "ov") for n in nodes)}</ul>'
    bits = []
    if c['loops']:
        bits.append(f'{cnt("custom:loops-through-" + pid, c["loops"])} loops pass through')
    if c['issues']:
        bits.append(f'{cnt("custom:issues-" + pid, c["issues"])} issues tracked')
    if c['reforms']:
        bits.append(f'{cnt("custom:reforms-" + pid, c["reforms"])} reforms aimed here')
    counts = ' · '.join(f'<span class="nb">{b}</span>' for b in bits)
    open_c = ''
    if pid == 'C':
        open_c = '<a class="fl-open" href="#area-c">Open the Elections floor <span aria-hidden="true">→</span></a>'
    return (f'<div class="floor" data-floor="{pid}" data-xin="{len(X_TO.get(pid, []))}" style="grid-row:{row}"{surface}>'
            f'<div class="fl-head">{floor_id(pid)}{open_c}</div>'
            f'<div class="fl-body">{tiles}<p class="fl-text">{e(part_sentence(pid))} <span class="fl-counts">{counts}</span></p></div>'
            f'</div>')


def arrow_svg(uid, direction='up', w=3, h=44):
    """A short arrow between floors. Drawn in the frame's grammar: one closed head, sized by weight."""
    x = 12
    if direction == 'up':
        pts = [(x, h - 2), (x, 2)]
    else:
        pts = [(x, 2), (x, h - 2)]
    hl, hb = HEAD[w]
    body = trim_end(pts, hl)
    u = (0, -1) if direction == 'up' else (0, 1)
    return (f'<svg class="fa" data-view="flow-{uid}" viewBox="0 0 24 {h}" width="24" height="{h}" aria-hidden="true">'
            f'<path class="ak-mark" d="{rounded_d(body, 0)}" fill="none" stroke-width="{w}"/>{head_shape(pts[-1], u, w)}</svg>')


def slab_html(lower, upper, row):
    up, down = flow_links(lower, upper), flow_links(upper, lower)
    main = (lower, upper) in MAIN
    lead = lead_link(up)
    key = f'flow-{lower.lower()}-{upper.lower()}'
    rel = ' '.join(sorted({k_var(L[k]['from']) for k in up + down} | {k_var(L[k]['to']) for k in up + down}))
    say = (f'{len(up)} connections pass up from {pname(lower)} to {pname(upper)}, such as {lead}, {L[lead]["name"]}.'
           + (f' {len(down)} come back down.' if down else ''))
    dn = ''
    if down:
        dn = (f'<span class="sl-down">{arrow_svg(key + "-d", "down", 2, 28)}'
              f'{cnt("custom:" + key + "-down", len(down), "sl-fig2")}<span> back down</span></span>')
    return (f'<div class="slab{" main" if main else ""}" style="grid-row:{row}">'
            f'<button type="button" class="flow" data-select="{key}" data-rel="{e(rel)}" data-say="{e(say)}">'
            f'<span class="sl-up">{arrow_svg(key, "up", 3 if main else 2)}'
            f'{cnt("custom:" + key + "-up", len(up), "sl-fig")}'
            f'<span class="sl-t"><span class="sl-w">pass up to {e(pname(upper))}, such as</span> '
            f'<span class="sl-n">{e(L[lead]["name"])}</span></span></span>{dn}</button></div>')


def outside_html(rows):
    p = PARTS['X']
    nodes = p['nodes']
    say = f'{p["plain_name"]}, {p["formal_title"]}. {part_sentence("X")}'
    rel = ' '.join(k_var(n) for n in nodes)
    order = sorted(X_TO.items(), key=lambda t: (-len(t[1]), STACK.index(t[0]) if t[0] in STACK else 9))
    pushes = ''.join(f'<li><span>{e(pname(pid))}</span>{cnt("custom:x-to-" + pid, len(ks))}</li>' for pid, ks in order)
    return (f'<aside class="outside" style="grid-row:{rows}" aria-label="Outside forces, beside the building">'
            f'<button type="button" class="fl-id ox ox-phone" data-select="area-x" data-part="X" data-name="{e(p["plain_name"])}" '
            f'data-rel="{e(rel)}" data-say="{e(say)}"><span class="fl-mark" aria-hidden="true">X</span>'
            f'<span class="fl-name">{e(p["plain_name"])}</span><span class="fl-formal">{e(p["formal_title"])}</span>'
            f'<span class="ox-text">{e(part_sentence("X"))}</span></button>'
            f'<p class="ox-cap" aria-hidden="true"><span class="fl-mark">X</span></p>'
            f'<ul class="tiles ox-tiles" style="--cols:1">{"".join(tile(n, "ov") for n in nodes)}</ul>'
            f'<div class="ox-push"><p class="ox-h">{cnt("custom:x-out", len(OUTSIDE))} connections push in</p>'
            f'<ul>{pushes}</ul></div></aside>')


def outside_head():
    """Outside forces named in the roof, as a note over the column that stands beside the building."""
    p = PARTS['X']
    rel = ' '.join(k_var(n) for n in p['nodes'])
    say = f'{p["plain_name"]}, {p["formal_title"]}. {part_sentence("X")}'
    return (f'<button type="button" class="ox-roof" data-select="area-x" data-part="X" data-name="{e(p["plain_name"])}" '
            f'data-rel="{e(rel)}" data-say="{e(say)}"><span class="ret-h">Beside the building</span>'
            f'<span class="ox-rn">{e(p["plain_name"])}</span><span class="ox-rf">{e(p["formal_title"])}</span>'
            f'<span class="ox-rt">{e(part_sentence("X"))}</span></button>')


def building_html():
    rows = []
    r = 2
    floor_rows = {}
    html_parts = []
    for i, pid in enumerate(STACK):
        floor_rows[pid] = r
        html_parts.append(floor_html(pid, r))
        r += 1
        if i < len(STACK) - 1:
            lower = STACK[i + 1]
            html_parts.append(slab_html(lower, pid, r))
            r += 1
    last = r
    ret_rel = ' '.join(sorted({k_var(L[k]['from']) for k in RETURN} | {k_var(L[k]['to']) for k in RETURN}))
    ret_say = f'Return line. {len(RETURN)} connections run back down from Policy. {DATA["opening"]["return"]}'
    roof = (f'<div class="roof" style="grid-row:1">'
            f'<button type="button" class="ret" data-select="flow-return" data-rel="{e(ret_rel)}" data-say="{e(ret_say)}">'
            f'<span class="ret-h">The return line</span>'
            f'<span class="ret-b">{cnt("custom:return", len(RETURN), "ret-fig")}<span class="ret-t">connections run back down from Policy: '
            f'{len(flow_links("E", "A"))} into Wealth, {len(flow_links("E", "EC"))} into Your household.</span></span>'
            f'<span class="ret-q">{e(DATA["opening"]["return"])}</span></button>'
            f'{outside_head()}</div>')
    outside = outside_html(f'{floor_rows["E"]} / {floor_rows["TC"] + 1}')
    census = (f'<p class="census" style="grid-row:{last}">Where the {cnt("connections", COUNTS["connections"])} connections run: '
              f'{cnt("custom:inside", len(INSIDE))} inside one floor, {cnt("custom:up", len(UP))} up to the next floor, '
              f'{cnt("custom:down", len(DOWN))} back down one floor, {cnt("custom:return-n", len(RETURN))} on the return line, '
              f'{cnt("custom:outside-n", len(OUTSIDE))} in from outside forces and {cnt("custom:skip", len(SKIP))} that skip a floor. '
              f'Tap a floor to see all of its own.</p>')
    return (f'<div class="bldg" data-ak-roving data-ak-nav="spatial" role="group" aria-labelledby="h-bldg" '
            f'data-ret-a="{len(flow_links("E", "A"))}" data-ret-ec="{len(flow_links("E", "EC"))}">'
            f'{roof}{"".join(html_parts)}{outside}{census}'
            f'<svg class="bl-lines" data-view="overview-lines" aria-hidden="true"></svg></div>')


def building_words():
    items = []
    for pid in STACK + ['X']:
        p = PARTS[pid]
        vs = ', '.join(f'{n} {N[n]["label"]}' for n in p['nodes'])
        bits = [f'<strong>{e(p["plain_name"])}, {e(p["formal_title"])}.</strong> {e(part_sentence(pid))} Variables: {e(vs)}.']
        for lo_, up_ in ADJ:
            if lo_ == pid:
                bits.append(f'{len(flow_links(lo_, up_))} connections pass up to {e(pname(up_))}'
                            + (f', and {len(flow_links(up_, lo_))} come back down.' if flow_links(up_, lo_) else '.'))
        if pid == 'E':
            bits.append(f'{len(RETURN)} connections run back down on the return line.')
        if pid == 'X':
            bits.append(f'{len(OUTSIDE)} connections push into the building.')
        items.append(f'<li>{" ".join(bits)}</li>')
    return f'<ol class="words">{"".join(items)}</ol>'


def question_cards():
    PW = {p['id']: p for p in DATA['pathways']}
    cards = []
    for i, h in enumerate(DATA['hubs']):
        qs = []
        floors = []
        for pid in h['pathways']:
            pw = PW[pid]
            rel = ' '.join(k_var(n) for n in pw['model_refs']['nodes'])
            for n in pw['model_refs']['nodes']:
                if PART_OF[n] not in floors:
                    floors.append(PART_OF[n])
            say = f'{pw["question"]} {pw["title"]}. Lights the tiles it reaches.'
            qs.append(f'<li><button type="button" class="qq" data-select="q-{pid.lower()}" data-rel="{e(rel)}" data-say="{e(say)}">'
                      f'<span>{e(pw["question"])}</span><span class="qq-a" aria-hidden="true">→</span></button></li>')
        fl = ', '.join(pname(x) for x in sorted(floors, key=lambda x: (STACK + ['X']).index(x)))
        cards.append(f'<li class="qcard"><div class="qc-top"><span class="qc-ic">{icon(HUB_ICON[h["id"]], "black", "hub" + str(i), 48, variable=False)}</span>'
                     f'<p class="qc-hub">{e(h["title"])}</p><p class="qc-n">{cnt("custom:hub-" + h["id"], len(h["pathways"]))} questions</p></div>'
                     f'<p class="qc-q">{e(h["question"])}</p><ul class="qc-list">{"".join(qs)}</ul>'
                     f'<p class="qc-foot">Reaches {e(fl)}</p></li>')
    return f'<ol class="qcards" data-ak-roving data-ak-nav="spatial" aria-label="Five topics and their questions">{"".join(cards)}</ol>'


def loop_index():
    groups = []
    for g in DATA['loop_groups']:
        name = pname(g['id']) if g['id'] in PARTS else 'Sketched loops'
        sub = PARTS[g['id']]['formal_title'] if g['id'] in PARTS else 'Without a complete numbered chain'
        items = []
        for lp in g['loops']:
            o = LO[lp]
            steps = 'sketch' if o['conceptual'] else ' '.join(s['id'] for s in o['steps'])
            rel = ' '.join(k_var(s['code']) for s in o['stations'] if s.get('is_variable') and s.get('code') in N)
            items.append(f'<li><span class="li-c">{lp}</span><span class="li-b"><a href="{loop_href(lp)}" data-loop="{lp}" data-steps="{steps}" '
                         f'data-name="{e(o["plain_name"])}" data-rel="{e(rel)}" data-say="{e(lp + ", " + o["plain_name"] + ". " + o["title"])}">'
                         f'{e(o["plain_name"])}</a><span class="li-k">{e(kind_line(lp))}</span></span></li>')
        groups.append(f'<div class="li-g"><p class="li-h">{e(name)}</p><p class="li-s">{e(sub)}</p><ul>{"".join(items)}</ul></div>')
    return f'<div class="li-groups" data-ak-roving data-ak-nav="spatial">{"".join(groups)}</div>'


def key_block():
    """The reading key that holds the panel's place on the overview."""
    def spec(grade):
        return wire([(2, 10), (78, 10)], 2, grade, None, None)
    rows = ''.join(f'<li><svg data-view="key-{gkey(g)}" viewBox="0 0 80 20" width="80" height="20" aria-hidden="true">{spec(g)}</svg>'
                   f'<span>{e(gfull(g))}</span></li>' for g in ['documented', 'plausible', 'plausible_contested', 'hypothesis'])
    return (f'<div class="idle"><p class="t-eyebrow">How to read the building</p>'
            f'<ol class="kb">'
            f'<li><strong>Floors</strong> are the parts of the system, roof to foundation. Each names its question.</li>'
            f'<li><strong>Tiles</strong> are variables: {e(GLOSS["Variable"][0].lower() + GLOSS["Variable"][1:])}</li>'
            f'<li><strong>Arrows between floors</strong> count the connections that pass up. The heavy ones trace the main circuit.</li>'
            f'<li><strong>The return line</strong> at left carries policy&#8217;s effects back down to Wealth.</li>'
            f'<li><strong>Below the heavy ground line</strong> sit the economy and technology layers, on Newsprint.</li>'
            f'</ol><p class="t-eyebrow kb-h">Inside a floor, lines carry their evidence</p><ul class="kg">{rows}</ul>'
            f'<p class="kb-note">{e(GLOSS["Positive sign (+)"])}</p>'
            f'<p class="kb-go"><a href="#how-to-read">The full key</a></p></div>')


# ---------------------------------------------------------------------------------------------------- views
def counts_block():
    return ('<dl class="ov-counts">'
            f'<div><dt>variables</dt><dd>{cnt("variables", COUNTS["variables"])}</dd></div>'
            f'<div><dt>connections</dt><dd>{cnt("connections", COUNTS["connections"])}</dd></div>'
            f'<div><dt>loops</dt><dd>{cnt("loops", COUNTS["loops"])}</dd></div>'
            f'<div><dt>reforms</dt><dd>{cnt("reforms", COUNTS["reforms"])}</dd></div>'
            f'</dl><p class="ov-snap">Snapshot {e(SNAP_WORDS)}. {cnt("issues_active", COUNTS["issues_active"])} issue records '
            f'and {cnt("sources", COUNTS["sources"])} sources sit beneath.</p>')


def slot(idle):
    return f'<div class="slot" data-panel-slot>{idle}</div>'


def view_overview():
    q = DATA['questions']['dem']['q']
    deck = ('The atlas draws democracy and the economy as one building, from your household up to policy. '
            'Each floor passes something up to the next, and policy sends its effects back down.')
    howto = ('Each tile is a variable, a condition that can rise or fall. Each arrow between floors counts the connections '
             'that run that way. Tap any floor, tile or arrow to read it, or start from a question.')
    entry = GLOSS['Entry document']
    return f'''<section class="view" data-view-root="overview" data-crumb="Overview" aria-labelledby="h-overview">
<header class="vhead">
  <div class="vh-main">
    <p class="t-eyebrow">{e(DATA["meta"]["subtitle"])}</p>
    <h1 id="h-overview" class="t-display" data-ak-heading>{e(q)}</h1>
    <p class="t-deck">{e(deck)}</p>
    <p class="howto"><span class="t-eyebrow">How to read this</span> {e(howto)}</p>
  </div>
  <div class="vh-side">{counts_block()}</div>
</header>
<section class="qsec" aria-labelledby="h-q">
  <div class="sec-head"><h2 id="h-q" class="t-head2">Follow a question from your week</h2>
  <p class="sec-deck">Start from an entry document, {e(entry[0].lower() + entry[1:])} Pick a question and the building lights the tiles it reaches.</p></div>
  {question_cards()}
</section>
<div class="vbody">
  <div class="vmain">
    <div class="sec-head"><h2 id="h-bldg" class="t-head2">The building, floor by floor</h2>
    <p class="sec-deck">Seven floors stand from the foundation up, and outside forces stand beside them. Every one of the {cnt("variables", COUNTS["variables"])} variables is a tile.</p></div>
    {building_html()}
    <p class="ak-readout" data-ak-readout>Point at, tap or tab to a floor, a tile or an arrow to read it.</p>
    <details class="words-d"><summary>The building in words</summary>{building_words()}</details>
  </div>
  {slot(key_block())}
</div>
<section class="lsec" aria-labelledby="h-li">
  <div class="sec-head"><h2 id="h-li" class="t-head2">The {cnt("loops", COUNTS["loops"])} loops, by home floor</h2>
  <p class="sec-deck">A loop is a chain of causes that returns to where it started. Point at one to light its tiles in the building; open one to walk it. <a href="#loops">Open the loop catalog</a></p></div>
  {loop_index()}
</section>
</section>'''


def conn_rows(lids, direction):
    """Connections grouped by the part at their far end, each drawn on its own and named."""
    groups = {}
    for k in lids:
        far = L[k]['from'] if direction == 'in' else L[k]['to']
        groups.setdefault(PART_OF[far], []).append(k)
    order = sorted(groups, key=lambda pid: (-len(groups[pid]), (STACK + ['X']).index(pid)))
    out = ''
    for pid in order:
        rows = ''
        for k in groups[pid]:
            l = L[k]
            sg = l['polarity']
            far, near = (l['from'], l['to']) if direction == 'in' else (l['to'], l['from'])
            say = link_say(k)
            fr = f'<span class="cr-v"><span class="cr-c">{l["from"]}</span> {e(N[l["from"]]["label"])}</span>'
            to = f'<span class="cr-v"><span class="cr-c">{l["to"]}</span> {e(N[l["to"]]["label"])}</span>'
            sign = f'{sign_char(sg)} {verb(sg)}' if sg in ('+', '-') else 'decides'
            rows += (f'<li><button type="button" class="crow"{link_attrs(k, rel=k_var(near) + " " + k_var(far), say=say)[len(" role=\"button\""):]}>'
                     f'<span class="cr-top">{fr}{conn_line_svg(k, k.lower() + direction)}{to}</span>'
                     f'<span class="cr-name">{chip("Connection", k, True)} {e(l["name"])}</span>'
                     f'<span class="cr-meta">{e(sign)} · {e(gfull(l["evidence"]))} · {e(DELAY[l["delay"]])}</span></button></li>')
        verbw = 'From' if direction == 'in' else 'To'
        out += f'<div class="cr-g"><p class="cr-h">{verbw} {e(pname(pid))} <span>{len(groups[pid])}</span></p><ul>{rows}</ul></div>'
    return out


def issue_details(i):
    pe, fe = i.get('problem_example'), i.get('fix_example')

    def ex(x, label):
        if not x:
            return ''
        s = x.get('source') or {}
        src = ', '.join(t for t in [s.get('publisher'), s.get('title'), s.get('year')] if t)
        res = f'<p class="ex-r">{e(x["result"])}</p>' if x.get('result') else ''
        wh = ' · '.join(t for t in [x.get('where'), x.get('when')] if t)
        return (f'<div class="ex"><p class="ex-l">{label}</p><p class="ex-h">{e(x["headline"])}</p><p>{e(x["text"])}</p>{res}'
                f'<p class="ex-s">{e(wh)}{" · " if wh and src else ""}Source: {e(src)}</p></div>')
    reforms = ''.join(f'<li>{chip("Reform", a["id"], True)} {e(RF[a["id"]]["title"])}. {e(a.get("why") or "")}</li>'
                      for a in (i.get('aimed_reforms') or []) if a['id'] in RF)
    body = (f'<p>{e(i["summary"])}</p>'
            f'<div class="ex2">{ex(pe, "The problem, in the real world")}{ex(fe, "A fix, in the real world")}</div>'
            f'<dl class="idl"><dt>How it works</dt><dd>{e(i.get("mechanism") or "")}</dd>'
            f'<dt>Evidence</dt><dd>{e(i.get("evidence_note") or "")}</dd>'
            f'<dt>Response</dt><dd>{e(i.get("response") or "")}</dd>'
            f'<dt>Who acts</dt><dd>{e(i.get("actor") or "")}</dd>'
            f'<dt>Tradeoff</dt><dd>{e(i.get("tradeoff") or "")}</dd>'
            f'<dt>Success looks like</dt><dd>{e(i.get("success_measure") or "")}</dd></dl>'
            + (f'<p class="ex-l">Reforms aimed at it</p><ul class="irf">{reforms}</ul>' if reforms else ''))
    tex = texture(i['grade'])
    return (f'<li><details class="iss"><summary data-issue="{i["id"]}" data-name="{e(i["title"])}">'
            f'<span class="iss-t">{e(i["title"])}'
            + (f'<span class="iss-x">In the real world: {e(pe["headline"])}</span>' if pe else '') + '</span>'
            f'<span class="iss-g g-{tex}">{e(gword(i["grade"]))}</span><span class="iss-id">{i["id"]}</span></summary>'
            f'<div class="iss-b">{body}</div></details></li>')


def reform_card(rid, uid):
    r = RF[rid]
    say = f'{rid}, {r["title"]}. Its targets take the red: {", ".join(r["targets"])}.'
    eff = ' · '.join(f'{DATA["families"][k]} {DATA["effect_codes"].get(v, v)}' for k, v in r['effects'].items())
    link = '<a class="rc-open" href="#reform-r01">Open reform R-01 <span aria-hidden="true">→</span></a>' if rid == 'R-01' else ''
    return (f'<li class="rc"><button type="button" class="rcard" data-select="{k_reform(rid)}" data-reform="{rid}" '
            f'data-targets="{" ".join(r["targets"])}" data-name="{e(r["title"])}" data-say="{e(say)}">'
            f'<span class="rc-ic">{icon(rid, "black", uid + rid.lower(), 48, variable=False)}</span>'
            f'<span class="rc-b"><span class="rc-id">{rid}</span><span class="rc-t">{e(r["title"])}</span>'
            f'<span class="rc-x">{e(first_sentence(r["what_it_changes"]))}</span>'
            f'<span class="rc-tg">Targets {e(", ".join(r["targets"]))} · {e(eff)}</span></span></button>{link}</li>')


def view_area_c():
    p = PARTS['C']
    nodes = p['nodes']
    c = part_counts('C')
    ins = [k for k in L if PART_OF[L[k]['to']] == 'C' and PART_OF[L[k]['from']] != 'C']
    outs = [k for k in L if PART_OF[L[k]['from']] == 'C' and PART_OF[L[k]['to']] != 'C']
    inside = [k for k in INSIDE if PART_OF[L[k]['from']] == 'C']
    thr = loops_through(nodes)
    iss = issues_for_nodes(nodes)
    refs = reforms_for_nodes(nodes)
    headline = 'Safe seats move the deciding vote to the primary and lower the risk of losing office.'
    deck = (f'{p["plain_question"]} {p["text"]} Five variables share this floor; '
            f'{len(ins) + len(outs) + len(inside)} connections touch them, and {nw(len(thr))} loops pass through.')
    rooms = ''
    for nid in nodes:
        n = N[nid]
        rest, ok = increase_rest(nid)
        rooms += (f'<li class="room"><div class="rm-h"><span class="rm-ic">{icon(nid, "black", "rm" + nid.lower())}</span>'
                  f'<div><span class="rm-c">{nid}</span><p class="rm-l">{e(n["label"])}</p><p class="rm-f">{e(n["title"])}</p></div></div>'
                  f'<p class="rm-d">{e(n.get("description") or "")}</p>'
                  f'<p class="rm-i"><span class="t-eyebrow">A higher value means</span> {e(rest)}</p>'
                  f'<p class="rm-w"><span class="t-eyebrow">Why it matters</span> {e(n.get("why") or "")}</p></li>')
    loops = ''
    for lp in thr:
        loops += loop_card(lp, 'ac', compact=True)
    by_dom = {}
    for i in iss:
        by_dom.setdefault(i.get('domain'), []).append(i)
    dom_t = {d['id']: d['title'] for d in DATA['domains']}
    issues_html = ''
    for d in sorted(by_dom, key=lambda d: (-len(by_dom[d]), d or '')):
        rows = ''.join(issue_details(i) for i in by_dom[d])
        issues_html += f'<div class="iss-g"><p class="cr-h">{e(dom_t.get(d, "Other"))} <span>{len(by_dom[d])}</span></p><ul>{rows}</ul></div>'
    words = ''.join(f'<li>{e(link_say(k))}</li>' for k in inside)
    loc = locator_svg({'C'}, 'ac', 'You are on the Elections floor, the middle of the five core floors.')
    return f'''<section class="view" data-view-root="area-c" data-crumb="Elections, area C" data-parent="overview" aria-labelledby="h-area-c" hidden>
<header class="vhead">
  <div class="vh-main">
    <p class="t-eyebrow">Area C · {e(p["plain_name"])} · {e(p["formal_title"])}</p>
    <h1 id="h-area-c" class="t-head" data-ak-heading>{e(headline)}</h1>
    <p class="t-deck">{e(deck)}</p>
  </div>
  <a class="vh-side locator" href="#overview" aria-label="Back to the overview. You are on the Elections floor.">
    <span class="t-eyebrow">You are here</span>{loc}</a>
</header>
<div class="vbody">
  <div class="vmain">
    <section class="blk" aria-labelledby="h-floor">
      <div class="sec-head"><h2 id="h-floor" class="t-head2">The floor plan</h2>
      <p class="sec-deck">The five rooms of Elections and the {nw(len(inside))} connections between them. The safe-seat loop runs along the row and back underneath.</p></div>
      <div class="ak-scroll fc-h" id="fc-region" role="region" tabindex="0" aria-label="Elections floor plan" style="--ak-min:944px;--ak-full-w:944px">{floor_c_svg()}</div>
      <div class="fc-v">{floor_c_svg_v()}</div>
      <p class="ak-readout" data-ak-readout>Point at, tap or tab to a room or a connection to read it.</p>
      <details class="words-d"><summary>The floor plan in words</summary><ol class="words">{words}</ol></details>
      <ol class="rooms">{rooms}</ol>
    </section>
    <section class="blk" aria-labelledby="h-push">
      <div class="sec-head"><h2 id="h-push" class="t-head2">What pushes on Elections, and what it pushes on</h2>
      <p class="sec-deck">{nw(len(ins)).capitalize()} connections arrive from other floors and {nw(len(outs))} leave, grouped by the floor at the far end. Each line shows its sign, its evidence and its delay.</p></div>
      <div class="cr-cols" data-ak-roving data-ak-nav="spatial">
        <div><p class="t-eyebrow cr-hh">Coming in · {cnt("custom:c-in", len(ins))}</p>{conn_rows(ins, "in")}</div>
        <div><p class="t-eyebrow cr-hh">Going out · {cnt("custom:c-out", len(outs))}</p>{conn_rows(outs, "out")}</div>
      </div>
    </section>
    <section class="blk" aria-labelledby="h-cl">
      <div class="sec-head"><h2 id="h-cl" class="t-head2">The {nw(len(thr))} loops that run through Elections</h2>
      <p class="sec-deck">Each is a cycle you can read aloud. Four make their home here; three start on other floors and pass through.</p></div>
      <ol class="lcards two" data-ak-roving data-ak-nav="spatial">{loops}</ol>
    </section>
    <section class="blk" aria-labelledby="h-iss">
      <div class="sec-head"><h2 id="h-iss" class="t-head2">The issues tracked here</h2>
      <p class="sec-deck">{cnt("custom:c-issues", len(iss))} active issue records touch these five variables. Open any one for its real-world problem, a fix tried somewhere, and what the evidence says.</p></div>
      {issues_html}
    </section>
    <section class="blk" aria-labelledby="h-rf">
      <div class="sec-head"><h2 id="h-rf" class="t-head2">The reforms aimed here</h2>
      <p class="sec-deck">{cnt("custom:c-reforms", len(refs))} reforms aim at a variable on this floor or a connection that touches it. Select one to see its targets marked in red on the floor plan.</p></div>
      <ol class="rcards" data-ak-roving data-ak-nav="spatial">{"".join(reform_card(r, "acr") for r in refs)}</ol>
    </section>
  </div>
  {slot(line_key("Reading a connection"))}
</div>
</section>'''


def line_key(title):
    def spec(grade):
        return wire([(2, 10), (78, 10)], 2, grade, None, None)
    rows = ''.join(f'<li><svg data-view="lk-{gkey(g)}-{abs(hash(title)) % 997}" viewBox="0 0 80 20" width="80" height="20" aria-hidden="true">{spec(g)}</svg>'
                   f'<span>{e(gfull(g))}</span></li>' for g in ['documented', 'plausible', 'plausible_contested', 'hypothesis'])
    tag = wire([(2, 12), (78, 12)], 2, 'documented', '+', 'M')
    return (f'<div class="idle"><p class="t-eyebrow">{e(title)}</p>'
            f'<div class="lk-ex"><svg data-view="lk-tag-{abs(hash(title)) % 997}" viewBox="0 0 80 24" width="80" height="24" aria-hidden="true">{tag}</svg>'
            f'<p>The tag carries the sign: plus raises, minus lowers. Ticks count the wait: one, under 2 years; two, 2 to 10 years; three, over 10 years.</p></div>'
            f'<p class="t-eyebrow kb-h">Texture is the evidence</p><ul class="kg">{rows}</ul>'
            f'<p class="kb-note">{e(GLOSS["Positive sign (+)"])}</p>'
            f'<p class="kb-go">Select anything to read it here.</p></div>')


def loop_card(lp, uid, compact=False):
    o = LO[lp]
    svg, steps = cycle_svg(lp, uid=f'{uid}-{lp.lower()}', view='cy')
    note = closure_note(lp)
    flag = f'<p class="lc-flag">{e(note.capitalize())}</p>' if note else ''
    rel = ' '.join(k_var(s['code']) for s in o['stations'] if s.get('is_variable') and s.get('code') in N)
    nodes = [s['code'] for s in o['stations'] if s.get('is_variable')]
    open_r10 = '<a class="lc-open" href="#loop-r10">Walk it step by step <span aria-hidden="true">→</span></a>' if lp == 'R10' else ''
    say = f'{lp}, {o["plain_name"]}. {kind_line(lp)}. {o["title"]}.'
    return (f'<li class="lcard" id="card-{lp.lower()}"><button type="button" class="lc-btn" data-select="{k_loop(lp)}" data-loop="{lp}" '
            f'data-steps="{steps}" data-name="{e(o["plain_name"])}" data-rel="{e(rel)}" data-say="{e(say)}">'
            f'<span class="lc-h"><span class="lc-id">{lp}</span><span class="lc-kind">{e(kind_line(lp))}</span>{mini_floors(nodes, uid + lp)}</span>'
            f'<span class="lc-name">{e(o["plain_name"])}</span><span class="lc-title">{e(o["title"])}</span></button>'
            f'{flag}<div class="lc-svg">{svg}</div>'
            f'<p class="lc-read"><span class="t-eyebrow">Read it aloud</span> {e(read_aloud(lp))}</p>'
            f'<p class="lc-status">{e(status_line(lp))}</p>{open_r10}</li>')


def stepper_r10():
    o = LO['R10']
    lis = []
    d = 1
    for st in o['steps']:
        a = 'More' if d > 0 else 'Less'
        d2 = d * (1 if st['polarity'] == '+' else -1)
        b = 'more' if d2 > 0 else 'less'
        keys = f'{k_link(st["id"])} {k_var(st["to"])}'
        fl = low(N[st['from']]['label'], st['from'])
        tl = low(N[st['to']]['label'], st['to'])
        txt = (f'{st["id"]}, {L[st["id"]]["name"]}. {a} {fl} means {b} {tl}. '
               f'Sign {sign_char(st["polarity"])}, {verb(st["polarity"])}; {gword(st["evidence"]).lower()}; {DELAY[st["delay"]]}.')
        lis.append(f'<li data-ak-step-keys="{keys}">{e(txt)}</li>')
        d = d2
    w = o['weakest'][0]
    end = (f'The loop is back where it started, so it {o["kind_gloss"]}: {o["kind_word"].lower()}. '
           f'Its weakest step is {w}, graded {gword(L[w]["evidence"]).lower()}.')
    s0 = o['steps'][0]['from']
    idle = (f'Start at {s0}, {N[s0]["label"]}, and suppose it rises. Press Play, or Next step to follow one numbered '
            f'connection at a time.')
    return (f'<section class="stepper" data-ak-stepper data-ak-hold="3200" data-ak-end="{e(end)}" aria-labelledby="h-steps">'
            f'<h2 id="h-steps" class="t-eyebrow">Walk the loop</h2>'
            f'<div class="controls"><button type="button" class="ak-btn" data-ak-step="play">Play</button>'
            f'<button type="button" class="ak-btn" data-ak-step="prev">Previous step</button>'
            f'<button type="button" class="ak-btn" data-ak-step="next">Next step</button>'
            f'<button type="button" class="ak-btn" data-ak-step="reset">Reset</button></div>'
            f'<p class="status" data-ak-step-status aria-live="polite">{e(idle)}</p>'
            f'<ol data-ak-step-list>{"".join(lis)}</ol></section>')


def reform_buttons(rids, uid):
    out = ''
    for rid in rids:
        r = RF[rid]
        say = f'{rid}, {r["title"]}. Its targets take the red: {", ".join(r["targets"])}.'
        out += (f'<li><button type="button" class="rbtn" data-select="{k_reform(rid)}" data-reform="{rid}" data-targets="{" ".join(r["targets"])}" '
                f'data-name="{e(r["title"])}" data-say="{e(say)}"><span class="rb-id">{rid}</span> <span class="rb-t">{e(r["title"])}</span>'
                f'<span class="rb-g">Targets {e(", ".join(r["targets"]))}</span></button></li>')
    return out


def view_loop_r10():
    o = LO['R10']
    big = r10_large()
    small, _ = cycle_svg('R10', uid='sm', interactive=True, numbered=True, view='loop-r10')
    steps_detail = ''
    for st in o['steps']:
        l = L[st['id']]
        weak = st['id'] in o['weakest']
        steps_detail += (f'<li class="sd{" weak" if weak else ""}"><p class="sd-h"><span class="t-eyebrow">Step {st["index"]}</span> '
                         f'{chip("Connection", st["id"], True)}{" <span class=\"sd-w\">The weakest step</span>" if weak else ""}</p>'
                         f'<p class="sd-n">{e(l["name"])}</p><p class="sd-p">{e(l.get("plain") or "")}</p>'
                         f'<p class="sd-m">{e(sign_char(l["polarity"]))} {e(verb(l["polarity"]))} · {e(gfull(l["evidence"]))} · {e(DELAY[l["delay"]])}</p>'
                         + (f'<p class="sd-q"><span class="t-eyebrow">Keep in mind</span> {e(l["qualification"])}</p>' if l.get('qualification') else '')
                         + '</li>')
    rf = RF['R-01']
    loc = locator_svg({'C'}, 'r10', 'Loop R10 runs on the Elections floor.')
    return f'''<section class="view" data-view-root="loop-r10" data-crumb="Loop R10, {e(o["plain_name"])}" data-parent="area-c" data-ak-reform="reform-r-01" aria-labelledby="h-loop-r10" hidden>
<header class="vhead">
  <div class="vh-main">
    <p class="t-eyebrow">Loop R10 · {e(o["plain_name"])} · {e(kind_line("R10"))}</p>
    <h1 id="h-loop-r10" class="t-head" data-ak-heading>{e(o["title"])}</h1>
    <p class="read-big"><span class="t-eyebrow">Read it aloud</span> {e(read_aloud("R10"))}</p>
  </div>
  <a class="vh-side locator" href="#overview" aria-label="Back to the overview. This loop runs on the Elections floor.">
    <span class="t-eyebrow">You are here</span>{loc}</a>
</header>
<div class="vbody">
  <div class="vmain">
    <p class="sec-deck r10-deck">{e(o["summary"])}</p>
    <div class="r10-lg">{big}</div>
    <div class="r10-sm">{small}</div>
    <p class="ak-readout" data-ak-readout>Point at, tap or tab to a box or a step to read it.</p>
    <p class="r10-cap">Red marks where reform R-01, {e(rf["short"])}, acts: on {e(", ".join(rf["targets"]))}. Select another reform to move the red to its targets.</p>
    <ul class="rbtns" data-ak-roving data-ak-nav="sequence">{reform_buttons(o["reforms"], "r10")}</ul>
    {stepper_r10()}
    <section class="blk" aria-labelledby="h-sd"><div class="sec-head"><h2 id="h-sd" class="t-head2">Step by step</h2></div><ol class="sds">{steps_detail}</ol></section>
    <section class="blk two-col" aria-labelledby="h-ev">
      <div><h2 id="h-ev" class="t-eyebrow">The evidence</h2><p>{e(o["evidence_summary"])}</p></div>
      <div><h2 class="t-eyebrow">Keep in mind</h2><p>{e(o["qualification"])}</p></div>
      <div><h2 class="t-eyebrow">In the real world</h2><p>{e(o["case"])}</p></div>
      <div><h2 class="t-eyebrow">Where it is heading</h2><p>{e(DIRECTION.get(o["direction"], ""))}, {e(o["delay_word"])} a turn. Measured by: {e(o["reference_mode"])}.</p>
      <p class="lora">{e(GLOSS["Reinforcing loop (R)"].split(". ")[-1])}</p></div>
    </section>
  </div>
  {slot(line_key("Reading the loop"))}
</div>
</section>'''


def view_reform_r01():
    rid = 'R-01'
    r = RF[rid]
    feature = icon(rid, 'red-black', 'feat', 96, variable=False)
    probs = [i for i in ACTIVE.values() if any(a['id'] == rid for a in (i.get('aimed_reforms') or []))]
    prob_html = ''.join(f'<li><p class="pr-t">{e(i["title"])}</p><p>{e(i["summary"])}</p></li>' for i in probs)
    loop_draw = r10_large(uid='rf', marks=False, view='reform-r01')
    eff = ''
    for fam, name in DATA['families'].items():
        code = r['effects'].get(fam)
        words = DATA['effect_codes'].get(code, code)
        steps = ['-M', '-S', '0', '+S', '+M', '+L']
        cells = ''.join(f'<span class="ef-c{" on" if s == code else ""}" title="{e(DATA["effect_codes"].get(s, s))}"></span>' for s in steps)
        eff += (f'<li><span class="ef-f">{e(name)}</span><span class="ef-s" aria-hidden="true">{cells}</span>'
                f'<span class="ef-w">{e(words.capitalize())}</span></li>')
    routes = ''
    for rt in r['routes']:
        feas = rt['feasibility']
        lvl = ['very low', 'low', 'medium', 'high'].index(feas) + 1 if feas in ('very low', 'low', 'medium', 'high') else 0
        bars = ''.join(f'<span class="fz{" on" if i < lvl else ""}"></span>' for i in range(4))
        chk = f'Checked {date_words(rt["checked"])}' if rt.get('checked') else 'No check date in V7'
        routes += (f'<tr><th scope="row">{e(DATA["route_names"].get(rt["route"], rt["route"]))}<span class="rt-who">{e(rt["who"])}</span></th>'
                   f'<td><span class="fzs" aria-hidden="true">{bars}</span> {e(feas.capitalize())}<span class="rt-sc">{e(DATA["feasibility_scale"].get(feas, ""))}</span></td>'
                   f'<td>{e(rt.get("note") or "")}</td><td class="rt-d">{e(chk)}</td></tr>')
    pe, re_ = r['problem_evidence'], r['remedy_evidence']
    st = r['status']
    loc = locator_svg({'C'}, 'rf', 'Reform R-01 acts on the Elections floor.')
    return f'''<section class="view" data-view-root="reform-r01" data-crumb="Reform R-01" data-parent="overview" data-ak-reform="reform-r-01" aria-labelledby="h-reform-r01" hidden>
<header class="vhead">
  <div class="vh-main rf-head">
    <span class="rf-ic" data-red="signature">{feature}</span>
    <div><p class="t-eyebrow">Reform R-01 · {e((r["band"] or "").capitalize())} · {e(r["short"])}</p>
    <h1 id="h-reform-r01" class="t-head" data-ak-heading>{e(r["title"])}</h1>
    <p class="rf-deck">{e(r["summary"])}</p></div>
  </div>
  <a class="vh-side locator" href="#overview" aria-label="Back to the overview. This reform acts on the Elections floor.">
    <span class="t-eyebrow">Where it acts</span>{loc}</a>
</header>
<div class="vbody">
  <div class="vmain">
    <section class="blk" aria-labelledby="h-rp"><div class="sec-head"><h2 id="h-rp" class="t-head2">The problem it answers</h2>
      <p class="sec-deck">{e(pe["text"])}</p></div>
      <ul class="probs">{prob_html}</ul></section>
    <section class="blk" aria-labelledby="h-rc"><div class="sec-head"><h2 id="h-rc" class="t-head2">What it changes</h2></div>
      <p class="body">{e(r["what_it_changes"])}</p></section>
    <section class="blk" aria-labelledby="h-rw"><div class="sec-head"><h2 id="h-rw" class="t-head2">Where it acts</h2>
      <p class="sec-deck">On the safe-seat loop, R-01 aims at {e(", ".join(r["targets"]))}, marked in red. It also sits on loops {e(" and ".join(x for x in r["loops"] if x != "R10"))}.</p></div>
      <div class="r10-lg">{loop_draw}</div>
      <div class="r10-sm">{cycle_svg("R10", uid="rfsm", interactive=True, numbered=True, view="reform-r01")[0]}</div>
      <ul class="rbtns" hidden>{reform_buttons(["R-01"], "rf")}</ul>
      <p class="ak-readout" data-ak-readout>Point at, tap or tab to a box or a step to read it.</p></section>
    <section class="blk" aria-labelledby="h-re"><div class="sec-head"><h2 id="h-re" class="t-head2">Likely effects, family by family</h2>
      <p class="sec-deck">Each family is rated on its own and never added to the others. Confidence: {e(r["effects_confidence"])}.</p></div>
      <div class="ef-hd" aria-hidden="true"><span></span><span class="ef-s">{"".join(f'<span>{e(c.replace("-", MINUS))}</span>' for c in ['-M', '-S', '0', '+S', '+M', '+L'])}</span><span></span></div>
      <ul class="effs">{eff}</ul></section>
    <section class="blk" aria-labelledby="h-rr"><div class="sec-head"><h2 id="h-rr" class="t-head2">Routes to adoption</h2>
      <p class="sec-deck">{e(r["who_decides"])}</p></div>
      <div class="tbl-wrap" role="region" tabindex="0" aria-label="Routes to adoption"><table class="routes"><thead><tr><th scope="col">Route</th><th scope="col">Feasibility, 2026 to 2030</th><th scope="col">Note</th><th scope="col">Checked</th></tr></thead><tbody>{routes}</tbody></table></div></section>
    <section class="blk" aria-labelledby="h-rv"><div class="sec-head"><h2 id="h-rv" class="t-head2">The evidence, graded twice</h2></div>
      <div class="ev2"><div class="evc"><p class="t-eyebrow">Problem evidence</p><p class="ev-g">{e(gfull(pe["grade"]))}</p><p>{e(pe["text"])}</p></div>
      <div class="evc"><p class="t-eyebrow">Remedy evidence</p><p class="ev-g">{e(gfull(re_["grade"]))}</p><p>{e(re_["text"])}</p></div></div></section>
    <section class="blk two-col" aria-labelledby="h-rt">
      <div><h2 id="h-rt" class="t-eyebrow">Tradeoffs</h2><p>{e(r["tradeoffs"])}</p></div>
      <div><h2 class="t-eyebrow">How it could fail</h2><p>{e(r["failure_risks"])}</p></div>
    </section>
    <section class="blk status" aria-labelledby="h-rs"><div class="sec-head"><h2 id="h-rs" class="t-head2">Status</h2></div>
      <p class="body">{e(st["text"])}</p>
      <p class="st-chk">Checked {e(date_words(st["checked"]))}.</p>
      <p class="disc"><strong>Disclosure.</strong> {e(DISCLOSE[rid])}</p></section>
  </div>
  {slot(line_key("Reading the drawing"))}
</div>
</section>'''


def view_loops():
    n_r = sum(1 for x in LO.values() if x['type'] == 'R')
    n_b = sum(1 for x in LO.values() if x['type'] == 'B')
    n_ref = sum(1 for x in LO.values() if x['reforms'])
    headline = f'{n_r} of the {len(LO)} loops feed themselves, and {n_ref} have a reform aimed at them.'
    groups = ''
    for g in DATA['loop_groups']:
        name = pname(g['id']) if g['id'] in PARTS else 'Sketched loops'
        sub = PARTS[g['id']]['formal_title'] if g['id'] in PARTS else 'Without a complete numbered chain'
        kinds = [LO[x]['type'] for x in g['loops']]
        kc = ', '.join(t for t in [f'{kinds.count("R")} reinforcing' if kinds.count('R') else '',
                                   f'{kinds.count("B")} balancing' if kinds.count('B') else ''] if t)
        text = PARTS[g['id']]['text'] if g['id'] in PARTS else LO[g['loops'][0]]['closure'].capitalize() + '.'
        cards = ''.join(loop_card(lp, 'lc') for lp in g['loops'])
        groups += (f'<section class="lgroup" aria-labelledby="lg-{g["id"].lower()}"><div class="lg-h">'
                   f'<h2 id="lg-{g["id"].lower()}" class="t-head2">{e(name)} <span class="lg-f">{e(sub)}</span></h2>'
                   f'<p class="lg-k">{e(kc)} · {e(text)}</p></div><ol class="lcards two">{cards}</ol></section>')
    return f'''<section class="view" data-view-root="loops" data-crumb="Loop catalog" data-parent="overview" aria-labelledby="h-loops" hidden>
<header class="vhead">
  <div class="vh-main">
    <p class="t-eyebrow">Loop catalog · {cnt("loops", COUNTS["loops"])} loops</p>
    <h1 id="h-loops" class="t-head" data-ak-heading>{e(headline)}</h1>
    <p class="t-deck">{cnt("loops_reinforcing", n_r)} reinforcing and {cnt("loops_balancing", n_b)} balancing loops, grouped by the floor each calls home. <span class="lora">{e(GLOSS["Reinforcing loop (R)"].split(". ")[-1])}</span></p>
  </div>
</header>
<div class="vbody">
  <div class="vmain" data-strip="loops">
    <div data-ak-roving data-ak-nav="spatial">{groups}</div>
  </div>
  {slot(loop_key())}
</div>
</section>'''


def loop_key():
    tag = wire([(2, 12), (78, 12)], 2, 'documented', '+', 'S')
    hol = wire([(2, 12), (78, 12)], 2, None, '-', None, conceptual=True)
    rows = ''.join(f'<li><svg data-view="lpk-{gkey(g)}" viewBox="0 0 80 20" width="80" height="20" aria-hidden="true">{wire([(2, 10), (78, 10)], 2, g, None, None)}</svg>'
                   f'<span>{e(gfull(g))}</span></li>' for g in ['documented', 'plausible', 'plausible_contested', 'hypothesis'])
    return (f'<div class="idle"><p class="t-eyebrow">Reading a loop card</p>'
            f'<div class="lk-ex"><svg data-view="lpk-tag" viewBox="0 0 80 24" width="80" height="24" aria-hidden="true">{tag}</svg>'
            f'<p>Each arrow says whether it raises or lowers the next box. The tag carries the sign; ticks count the wait.</p></div>'
            f'<ul class="kg">{rows}</ul>'
            f'<div class="lk-ex"><svg data-view="lpk-hol" viewBox="0 0 80 24" width="80" height="24" aria-hidden="true">{hol}</svg>'
            f'<p>An open line is a conceptual step with no numbered connection. Thin boxes are ideas outside the model&#8217;s variables.</p></div>'
            f'<p class="kb-note">The tiny building on each card shows the floors the loop stands on.</p>'
            f'<p class="kb-go">Select a card to read the loop here.</p></div>')


def view_how():
    def demo(pts, grade, sign, delay, uid, w=2, concept=False, auth=False, wd=220, ht=40):
        return (f'<svg data-view="how-{uid}" viewBox="0 0 {wd} {ht}" width="{wd}" height="{ht}" aria-hidden="true">'
                f'{wire(pts, w, grade, sign, delay, conceptual=concept, authority=auth)}</svg>')
    tex_rows = ''.join(
        f'<li>{demo([(4, 20), (216, 20)], g, None, None, "t" + str(i))}<p><strong>{e(gword(g))}</strong>, {e(ggloss(g))}. {e(first_sentence(GLOSS.get(gword(g).replace("Well supported", "Well-supported"), "")))}</p></li>'
        for i, g in enumerate(['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis']))
    tex_rows += f'<li>{demo([(4, 20), (216, 20)], None, "+", None, "tc", concept=True)}<p><strong>Conceptual step</strong>, an open line: a step in a sketched loop with no numbered connection.</p></li>'
    tick_rows = ''.join(f'<li>{demo([(4, 20), (216, 20)], "documented", None, d, "d" + d)}<p><strong>{e(DELAY[d].capitalize())}</strong>. {nw(TICKS[d]).capitalize()} tick{"s" if TICKS[d] > 1 else ""}.</p></li>'
                        for d in ['S', 'M', 'L'])
    sign_rows = (f'<li>{demo([(4, 20), (216, 20)], "documented", "+", None, "sp")}<p><strong>Plus, raises.</strong> {e(GLOSS["Positive sign (+)"])}</p></li>'
                 f'<li>{demo([(4, 20), (216, 20)], "documented", "-", None, "sm")}<p><strong>Minus, lowers.</strong> {e(GLOSS["Negative sign (−)"])}</p></li>'
                 f'<li>{demo([(4, 20), (216, 20)], "documented", None, None, "sa", auth=True)}<p><strong>Open diamond, decides.</strong> {e(GLOSS["Authority connection"])}</p></li>')
    r8, _ = cycle_svg('R8', uid='how8', view='how')
    b4, _ = cycle_svg('B4', uid='howb4', view='how')
    layers = (f'<div class="lay"><div class="lay-w"><p class="t-eyebrow">White floors</p><p>The core of the model: Wealth, Voice, Elections, Checks and Policy, with outside forces beside them.</p></div>'
              f'<div class="lay-n" data-surface="newsprint"><p class="t-eyebrow">Newsprint, below the ground line</p><p>{e(PARTS["EC"]["plain_name"])} and {e(PARTS["TC"]["plain_name"])}: the economy and technology layers the core stands on.</p></div></div>')
    mix = ''.join(f'<li><details class="mx"><summary>{e(m["prompt"])}</summary><p class="mx-a">{e(m["answer"])}</p>'
                  f'<p class="mx-w"><span class="t-eyebrow">The common mistake</span> {e(m["wrong"])}</p></details></li>' for m in DATA['mixups'])
    terms = ['Variable', 'Connection', 'Feedback loop', 'Reinforcing loop (R)', 'Balancing loop (B)', 'Delay', 'Documented',
             'Well-supported', 'Plausible', 'Contested', 'Hypothesis', 'Authority connection', 'Outside driver', 'Issue record',
             'Reform profile', 'Outcome family', 'Feasibility', 'Route', 'Pathway', 'Entry document', 'Snapshot']
    gl = ''.join(f'<div><dt>{e(t)}</dt><dd>{e(GLOSS[t])}</dd></div>' for t in terms if t in GLOSS)
    return f'''<section class="view" data-view-root="how-to-read" data-crumb="How to read" data-parent="overview" aria-labelledby="h-how-to-read" hidden>
<header class="vhead">
  <div class="vh-main">
    <p class="t-eyebrow">How to read the atlas · the shared language</p>
    <h1 id="h-how-to-read" class="t-head" data-ak-heading>Every line says what happens next, and how sure we are.</h1>
    <p class="t-deck">Five habits carry through every drawing in the atlas. Learn them once here and they hold on every floor, loop and reform.</p>
  </div>
</header>
<div class="how">
  <section class="lesson"><p class="ls-n">1</p><div><h2 class="t-head2">The tip is the effect</h2><p class="ls-d">Every arrow ends at what changes. The tag on the line says which way.</p><ul class="demo">{sign_rows}</ul></div></section>
  <section class="lesson"><p class="ls-n">2</p><div><h2 class="t-head2">Texture is the evidence</h2><p class="ls-d">Solid lines rest on the record or on strong research. Broken lines carry less. The pattern stays the same at every weight and survives a black and white print.</p><ul class="demo">{tex_rows}</ul></div></section>
  <section class="lesson"><p class="ls-n">3</p><div><h2 class="t-head2">Ticks count the wait</h2><p class="ls-d">{e(GLOSS["Delay"])}</p><ul class="demo">{tick_rows}</ul></div></section>
  <section class="lesson"><p class="ls-n">4</p><div><h2 class="t-head2">Loops have a character</h2><p class="ls-d">{e(GLOSS["Feedback loop"])}</p>
    <div class="ls-loops"><figure><figcaption><strong>R8 · {e(LO["R8"]["plain_name"])}</strong> {e(kind_line("R8"))}</figcaption>{r8}<p class="lc-read">{e(read_aloud("R8"))}</p></figure>
    <figure><figcaption><strong>B4 · {e(LO["B4"]["plain_name"])}</strong> {e(kind_line("B4"))}</figcaption>{b4}<p class="lc-read">{e(read_aloud("B4"))}</p></figure></div></div></section>
  <section class="lesson"><p class="ls-n">5</p><div><h2 class="t-head2">Color is the layer</h2><p class="ls-d">The ground under a floor says which layer of the model it belongs to. Red marks one thing per view: where a reform acts, or the item you selected.</p>{layers}</div></section>
  <section class="lesson wide"><p class="ls-n">?</p><div><h2 class="t-head2">Common mix-ups</h2><p class="ls-d">Questions readers get wrong, with the atlas&#8217;s answer.</p><ul class="mxs">{mix}</ul></div></section>
  <section class="lesson wide"><p class="ls-n">A</p><div><h2 class="t-head2">Terms</h2><dl class="gl">{gl}</dl></div></section>
</div>
</section>'''


# ---------------------------------------------------------------------------------------------------- templates for every item
def templates():
    out = []
    for nid in N:
        out.append(tpl_var(nid))
    for pid in PARTS:
        out.append(tpl_part(pid))
    for a, b in ADJ:
        out.append(tpl_flow(a, b))
    out.append(tpl_return())
    for pw in DATA['pathways']:
        out.append(tpl_pathway(pw))
    shown = set(k for k in INSIDE if PART_OF[L[k]['from']] == 'C') | {k for k in L if 'C' in (PART_OF[L[k]['from']], PART_OF[L[k]['to']])}
    shown |= set(LO['R10']['links'])
    for k in sorted(shown):
        out.append(tpl_link(k))
    for lp in DATA['loop_order']:
        out.append(tpl_loop(lp))
    rset = set(reforms_for_nodes(PARTS['C']['nodes'])) | set(LO['R10']['reforms'])
    for rid in sorted(rset, key=lambda r: int(r.split('-')[1])):
        out.append(tpl_reform(rid))
    return '\n'.join(out)


# ---------------------------------------------------------------------------------------------------- styles
CSS = (HERE / 'system.css').read_text() if (HERE / 'system.css').exists() else ''
JS = (HERE / 'system.js').read_text() if (HERE / 'system.js').exists() else ''


def kit():
    css = (KIT / 'atlas-kit.css').read_text()
    js = (KIT / 'atlas-kit.js').read_text()
    old = "const root = rootOf(S.view), item = key && $(`[data-select=\"${key}\"]`, root);"
    assert old in js, 'kit select line changed'
    # One departure: when a view holds a desktop and a phone drawing, select the copy the reader can see.
    js = js.replace(old, "const root = rootOf(S.view), cands = key ? $$(`[data-select=\"${key}\"]`, root) : [], "
                         "item = cands.find(vis) || cands[0] || null;")
    return css, js


def wordmark(height, master):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    return src.replace('<svg ', f'<svg width="{w:.0f}" height="{height}" aria-hidden="true" focusable="false" ', 1)


def page():
    kcss, kjs = kit()
    wm24 = wordmark(24, '20261028_Wordmark-24px-Master.svg').replace('<svg ', '<svg class="wm24" ', 1)
    wm16 = wordmark(16, '20261028_Wordmark-16px-Master.svg').replace('<svg ', '<svg class="wm16" ', 1)
    source = (f'{e(DATA["meta"]["title"])} Systems Atlas V7, snapshot {SNAP_WORDS}. '
              f'{cnt("variables", COUNTS["variables"])} variables, {cnt("connections", COUNTS["connections"])} connections, '
              f'{cnt("loops", COUNTS["loops"])} loops, {cnt("reforms", COUNTS["reforms"])} reforms.')
    tabs = [('overview', 'Overview'), ('area-c', 'Elections'), ('loop-r10', 'Loop R10'), ('reform-r01', 'Reform R-01'),
            ('loops', 'Loops'), ('how-to-read', 'How to read')]
    tabs_html = ''.join(f'<a href="#{v}" data-tab="{v}">{t}</a>' for v, t in tabs)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="atlas-views" content="overview area-c loop-r10 reform-r01 loops how-to-read">
<title>Atlas Architecture</title>
<meta name="description" content="Atlas system 05, Architecture: the Oath &amp; Action systems atlas drawn as a building a reader can walk through.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">
<style>{kcss}</style>
<style>{CSS}</style>
</head>
<body data-surface="white">
<a class="skip" href="#main">Skip to the atlas</a>
<div class="wrap">
<header class="mast">
  <a class="wm" href="#overview" data-red="signature" aria-label="Oath &amp; Action, back to the overview">{wm24}{wm16}</a>
  <p class="runhead">Atlas system 05 / Architecture</p>
  <nav class="tabs" aria-label="Views">{tabs_html}</nav>
</header>
<div class="crumbrow"><nav class="ak-crumbs" aria-label="Breadcrumb" data-ak-crumbs></nav></div>
<p class="ak-vh" role="status" data-ak-status></p>
<main class="ak-stage" id="main">
{view_overview()}
{view_area_c()}
{view_loop_r10()}
{view_reform_r01()}
{view_loops()}
{view_how()}
</main>
<footer class="foot">
  <p class="t-source">{source}</p>
  <p class="t-source right">Atlas system 05, Architecture. Studio draft, November 5, 2026.</p>
</footer>
</div>
<aside class="ak-panel" data-ak-panel aria-labelledby="ak-panel-title" hidden>
  <div class="ak-panel-bar"><p data-ak-panel-kind></p><button type="button" class="ak-btn" data-ak-sheet-toggle aria-expanded="false">More</button><button type="button" class="ak-btn" data-ak-close>Close</button></div>
  <h2 id="ak-panel-title" data-ak-panel-title tabindex="-1"></h2>
  <div data-ak-panel-body></div>
</aside>
{templates()}
<script>{kjs}</script>
<script>{JS}</script>
</body>
</html>'''


if __name__ == '__main__':
    out = page()
    OUT.write_text(out)
    print('wrote', OUT.relative_to(ROOT), f'{len(out) / 1e6:.2f} MB')
