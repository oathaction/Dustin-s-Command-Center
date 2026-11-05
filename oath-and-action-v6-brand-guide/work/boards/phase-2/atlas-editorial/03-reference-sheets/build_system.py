"""Editorial atlas, System 3: Reference Sheets (Newsprint). Oath & Action Edition 06, Phase 2, November 5, 2026.

A field guide of numbered sheets and plates, built by script from the editorial dataset (brief section 5).
Every label, count, sign, grade, delay, issue, example and reform text is read from the data; headlines and
decks marked "studio draft" in the notes are the maker's.

Usage, from the project root:
    python3 -I work/boards/phase-2/atlas-editorial/03-reference-sheets/build_system.py

Reads   work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json (the dataset)
        work/extract/atlas-v7-data.json (two fields the dataset leaves out: the R-01 editor's disclosure and the
        three layer titles)
        work/build/scripts/phase-2/atlas_concepts_common.py (palette, grades, icon_svg)
        work/boards/phase-2/atlas-concepts/shared/atlas-kit.js and atlas-kit.css (inlined, with the departures
        listed in the notes)
        work/build/assets/identity/wordmark/ (the 24 px and 16 px masters, inlined unchanged)
Writes  20261105_Editorial-03-Reference-Sheets.html beside this script.
Text widths come from Chromium with the page's own Google Fonts (measure_text.js beside this script, cached in
measure_cache.json), so every label in a drawing wraps on real metrics.
"""
import html
import importlib.util
import json
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc)

D = json.loads((ROOT / 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json').read_text())
V7 = json.loads((ROOT / 'work/extract/atlas-v7-data.json').read_text())
KIT_JS = (ROOT / 'work/boards/phase-2/atlas-concepts/shared/atlas-kit.js').read_text()
KIT_CSS = (ROOT / 'work/boards/phase-2/atlas-concepts/shared/atlas-kit.css').read_text()
WM24 = (ROOT / 'work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg').read_text()
WM16 = (ROOT / 'work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg').read_text()
OUT = HERE / '20261105_Editorial-03-Reference-Sheets.html'
CACHE = HERE / 'measure_cache.json'

# Fix pass (brief fix 3): every mention of the November 3, 2026 ballot opens "As of October 15, 2026," because the
# dataset is the October 15 snapshot and these pages are dated after the vote. Applied by script to V7's prose.
BALLOT = 'November 3, 2026'
AS_OF = 'As of October 15, 2026,'
_LOWER_OK = {'A', 'The', 'On', 'Two', 'Both', 'It', 'This', 'These', 'Each', 'Its', 'Voters', 'Courts'}


def _date_clause(c):
    if BALLOT not in c or c.startswith(AS_OF) or c.lower().startswith(AS_OF.lower()):
        return c
    first = c.split()[0] if c.split() else ''
    body = (c[0].lower() + c[1:]) if first in _LOWER_OK else c
    return f'{AS_OF} {body}'


def dated(text):
    if not isinstance(text, str) or BALLOT not in text:
        return text
    out = []
    for sent in re.split(r'(?<=[.?!])\s+(?=[A-Z"])', text):
        if BALLOT not in sent or sent.startswith(AS_OF):
            out.append(sent)
            continue
        head, sep, tail = '', '', sent
        m = re.search(r'(; |: )', sent)
        if m and BALLOT not in sent[:m.start()]:
            head, sep, tail = sent[:m.start()], m.group(1), sent[m.end():]
            out.append(head + sep + _date_clause(tail)[0].lower() + _date_clause(tail)[1:])
        else:
            out.append(_date_clause(sent))
    return ' '.join(out)


_KEEP = {'id', 'title', 'name', 'label', 'plain_name', 'headline', 'short'}


def _date_all(o, key=None):
    if isinstance(o, dict):
        return {k: _date_all(v, k) for k, v in o.items()}
    if isinstance(o, list):
        return [_date_all(v, key) for v in o]
    if isinstance(o, str) and key not in _KEEP:
        return dated(o)
    return o


for _k in ('links', 'loops', 'reforms', 'issues', 'numbers', 'pathways'):
    D[_k] = _date_all(D[_k])
NODES, LINKS, LOOPS, REFORMS, ISSUES = D['nodes'], D['links'], D['loops'], D['reforms'], D['issues']
PARTS = {p['id']: p for p in D['parts']}
PART_OF = {k: v['part'] for k, v in NODES.items()}
COUNTS = D['meta']['counts']
CORE = ['A', 'B', 'C', 'D', 'E']
NEXT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'A'}
SNAP = 'October 15, 2026'
MINUS = '−'
P = acc.PALETTE
LAYER_TITLE = {k: V7['layers'][k]['title'] for k in ('core', 'economy', 'technology')}
LAYER_OF_PART = {'X': 'core', 'A': 'core', 'B': 'core', 'C': 'core', 'D': 'core', 'E': 'core', 'EC': 'economy', 'TC': 'technology'}
ACCENT = {'core': P['prussian'], 'economy': P['verdigris'], 'technology': P['stone']}


def e(s):
    return html.escape(str(s), quote=True)


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def low(label):
    """A short label inside running text: lower-case the first letter unless the word is an acronym."""
    first = label.split()[0]
    if first.isupper() or first.startswith('Congress'):
        return label
    return label[0].lower() + label[1:]


def sentences(text):
    return [s for s in re.split(r'(?<=[.?!])\s+(?=[A-Z0-9"])', text.strip()) if s]


WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']


def nw(n):
    return WORDS[n] if 0 <= n < len(WORDS) else str(n)


def plural(n, one, many=None):
    return one if n == 1 else (many or one + 's')


# ------------------------------------------------------------------------------------------- vocabulary
def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


def tex_of(g):
    return acc.GRADES[g][2] if g in acc.GRADES else 'solid'


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def verb(p):
    return {'+': 'raises', '-': 'lowers'}.get(p, 'decides')


def delay_words(code):
    return acc.DELAYS[code]


def kind_words(lid):
    L = LOOPS[lid]
    return f'{L["kind_word"]}, {L["kind_gloss"]}'


DIRECTION_WORDS = {'running_up': 'Running up', 'running_down': 'Running down', 'running': 'Running',
                   'disabled': 'Not running', 'unknown': 'Direction unknown', 'design_target': 'A design target',
                   'disabled in concentrated sectors': 'Not running in concentrated sectors'}


def node_label(nid):
    return NODES[nid]['label']


# Labels that name countable things take "fewer" (brief fix 5; red team S3). A wording rule, not model data.
COUNTABLE = {'Safe seats', 'Seats settled in the primary', 'Incumbents defeated', 'Watchdogs and enforcement',
             'Ties across groups', 'State and local reform tests', 'Pricing algorithms'}


def less_word(label):
    return 'fewer' if label in COUNTABLE else 'less'


def read_aloud(lid):
    """More and less along the chain, multiplied from the signs, ending back at the start (civic memo, section 2)."""
    L = LOOPS[lid]
    if L['conceptual']:
        labels = [s['label'] for s in L['stations']]
    else:
        labels = [node_label(s['from']) for s in L['steps']]
    signs = [s['polarity'] for s in L['steps']]
    state, parts = '+', []
    for i, lab in enumerate(labels):
        parts.append(('more' if state == '+' else less_word(lab), low(lab)))
        state = '+' if (state == '+') == (signs[i] == '+') else '-'
    back = ('more' if state == '+' else less_word(labels[0]), low(labels[0]))
    return parts, back


def read_aloud_text(lid):
    parts, back = read_aloud(lid)
    body = ', '.join(f'{w} {lab}' for w, lab in parts)
    s = f'{body}, and back to {back[0]} {back[1]}.'
    return s[0].upper() + s[1:]


def read_aloud_html(lid):
    parts, back = read_aloud(lid)
    body = ', '.join(f'<b>{w}</b> {e(lab)}' for w, lab in parts)
    s = f'{body}, and back to <b>{back[0]}</b> {e(back[1])}.'
    return s[:3] + s[3].upper() + s[4:]


def weakest_words(lid):
    L = LOOPS[lid]
    if L['conceptual']:
        return 'A sketch: no step is a numbered connection'
    if L['weakest']:
        ws = [LINKS[w] for w in L['weakest']]
        if len(ws) == 1:
            return f'Weakest step {ws[0]["id"]}, {grade_word(ws[0]["evidence"]).lower()}'
        return 'Weakest steps ' + ', '.join(w['id'] for w in ws[:-1]) + f' and {ws[-1]["id"]}, {grade_word(ws[0]["evidence"]).lower()}'
    grades = {s['evidence'] for s in L['steps']}
    if len(grades) == 1:
        g = grades.pop()
        return f'Every step {grade_word(g).lower()}'
    return 'No single weakest step: ' + ' and '.join(grade_word(s['evidence']).lower() for s in L['steps'])


def weakest_short(lid):
    w = weakest_words(lid)
    for pre in ('Weakest steps ', 'Weakest step '):
        if w.startswith(pre):
            return w[len(pre):]
    return 'None: a sketch' if LOOPS[lid]['conceptual'] else w


def closure_note(lid):
    L = LOOPS[lid]
    if L['conceptual']:
        return 'A sketch. No step is a numbered connection, so the loop is drawn with hollow lines.'
    if L['hypothesized']:
        hyp = [s['id'] for s in L['steps'] if s['evidence'] == 'hypothesis']
        if len(hyp) == len(L['steps']):
            return f'Closed with hypothesized steps: {" and ".join(hyp)} are untested, so the loop holds only if they do.'
        return f'Closed with a hypothesized step: {hyp[-1]} is untested, so the loop closes only if {hyp[-1]} holds.'
    return None


def sign_rule():
    return acc.SIGN_RULE


def gloss(term):
    """A V7 glossary entry, without its notes on how V7 itself draws the term (these sheets draw it their own way)."""
    for g in D['glossary']:
        if g['term'] == term:
            return ' '.join(x for x in sentences(g['definition']) if not x.startswith('Drawn '))
    raise KeyError(term)


MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def date_words(iso):
    y, m, d_ = iso.split('-')
    return f'{MONTHS[int(m) - 1]} {int(d_)}, {y}'


IMPROVE = sentences(gloss('Reinforcing loop (R)'))[-1]          # "Improvement or decline can reinforce itself."
DISCLOSURE = D['reforms']['R-01']['disclosure']   # V7's own words, carried by the shared dataset
assert DISCLOSURE and 'Yes on 3' in DISCLOSURE

# ------------------------------------------------------------------------------------------- the model's flows
FLOW = {}
INSIDE = {}
for l in sorted(LINKS.values(), key=lambda l: l['id']):
    a, b = PART_OF[l['from']], PART_OF[l['to']]
    if a == b:
        INSIDE.setdefault(a, []).append(l['id'])
    else:
        FLOW.setdefault((a, b), []).append(l['id'])
CROSS = sum(len(v) for v in FLOW.values())
WITHIN = sum(len(v) for v in INSIDE.values())
assert CROSS + WITHIN == COUNTS['connections']
RANK = {'documented': 4, 'well-supported': 3, 'plausible': 2, 'plausible_contested': 1, 'hypothesis': 0}


def passes_on(p):
    """One connection a part passes on along the circuit: the best-evidenced one on a loop, lowest ID on a tie."""
    ids = FLOW.get((p, NEXT[p]), [])
    ids = sorted(ids, key=lambda k: (0 if LINKS[k]['loops'] else 1, -RANK[LINKS[k]['evidence']], -len(LINKS[k]['loops']), k))
    return LINKS[ids[0]]


def loops_home(p):
    return [k for k in D['loop_order'] if LOOPS[k]['home'] == p]


def issues_on(nids):
    return [i for i in ISSUES.values() if not i.get('retired') and any(n in (i.get('nodes') or []) for n in nids)]


def part_name(p):
    return PARTS[p]['plain_name']


# ------------------------------------------------------------------------------------------- text metrics
STY = {   # name: family, weight, size, line height, tracking (em), capitals, tabular
    'disp': ('Inter Tight', 800, 56, 60, -0.035, False, False),
    'head': ('Inter Tight', 800, 40, 44, -0.03, False, False),
    'deck': ('Inter', 400, 19, 28, 0, False, False),
    'phead': ('Inter Tight', 800, 22, 26, -0.02, False, False),
    'eyebrow': ('Inter', 700, 13, 18, 0.06, True, False),
    'body': ('Inter', 400, 17, 27, 0, False, False),
    'ptext': ('Inter', 400, 15, 20, 0, False, False),
    'station': ('Inter Tight', 700, 20, 22, -0.01, False, False),
    'map': ('Inter', 600, 15, 18, 0, False, False),
    'note': ('Inter', 400, 13, 16, 0.01, False, False),
    'noteb': ('Inter', 600, 13, 16, 0.01, False, False),
    'cap': ('Inter', 400, 14, 18, 0, False, False),
    'legend': ('Inter', 500, 13, 18, 0, False, False),
    'code': ('Inter', 700, 13, 16, 0, False, True),
    'count': ('Inter Tight', 800, 22, 22, -0.02, False, True),
    'fig': ('Inter Tight', 800, 40, 40, -0.03, False, True),
    'q': ('Inter', 600, 15, 20, 0, False, False),
}
_cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
_pending = {}


def _fontkey(sty):
    fam, wt, size, lh, ls, caps, tab = STY[sty]
    fam = f'"{fam}"' if ' ' in fam else fam
    return f'{wt} {size}px {fam}', round(ls * size, 3)


def tw(s, sty):
    """Rendered width of one run of text in a style, measured in Chromium (estimated until measured)."""
    s = s.upper() if STY[sty][5] else s
    font, ls = _fontkey(sty)
    key = f'{font}|{ls:g}|{s}' if ls else f'{font}|0|{s}'
    if key in _cache:
        return _cache[key] * (1.015 if STY[sty][6] else 1.0)
    _pending[key] = {'font': font, 'ls': ls, 'text': s}
    return len(s) * STY[sty][2] * 0.62


def wrap(s, sty, width):
    """Greedy line breaks on measured word widths (each word and the space measured once, so one pass settles it)."""
    words, out, line, lw = s.split(), [], [], 0.0
    sp = tw('a a', sty) - 2 * tw('a', sty)
    for w in words:
        ww = tw(w, sty)
        trial = lw + (sp if line else 0) + ww
        if line and trial > width:
            out.append(' '.join(line))
            line, lw = [w], ww
        else:
            line.append(w)
            lw = trial
    if line:
        out.append(' '.join(line))
    return out


def measure_pending():
    if not _pending:
        return False
    req = HERE / '.measure_requests.json'
    res = HERE / '.measure_results.json'
    req.write_text(json.dumps(list(_pending.values())))
    subprocess.run(['node', str(HERE / 'measure_text.js'), str(req), str(res)], check=True, cwd=str(HERE))
    got = json.loads(res.read_text())
    got.pop('__loaded', None)
    _cache.update(got)
    CACHE.write_text(json.dumps(_cache, sort_keys=True))
    req.unlink()
    res.unlink()
    _pending.clear()
    return True


def T(x, y, s, sty, anchor='start', cls='', attrs=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    s = s.upper() if STY[sty][5] else s
    return f'<text x="{f(x)}" y="{f(y)}" class="s-{sty}{(" " + cls) if cls else ""}"{a}{attrs}>{e(s)}</text>'


def TL(x, y, rows, sty, anchor='start', cls='', attrs='', lh=None):
    lh = lh or STY[sty][3]
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    rows = [r.upper() for r in rows] if STY[sty][5] else rows
    spans = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{f(x)}" y="{f(y)}" class="s-{sty}{(" " + cls) if cls else ""}"{a}{attrs}>{spans}</text>'


# ------------------------------------------------------------------------------------------- line machinery
HEAD = {2: (10, 8), 3: (13, 11), 6: (22, 18)}     # arrowhead length by base, by line width (design frame memo 3)
BEND = {2: 8, 3: 12, 6: 18}


def pattern(tex, w):
    if tex == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if tex == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if tex == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def fitted(tex, w, length):
    """Stretch the pattern so a textured line starts and ends on ink (design frame memo, rule 3.2)."""
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


def unit(dx, dy):
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def point_at(pts, s):
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= seg or b is pts[-1]:
            ux, uy = unit(b[0] - a[0], b[1] - a[1])
            return a[0] + ux * s, a[1] + uy * s, ux, uy
        s -= seg
    return pts[-1][0], pts[-1][1], 1, 0


def rounded(pts, r):
    """An orthogonal polyline with each corner rounded by r (an arc of a circle)."""
    if len(pts) < 3 or r <= 0:
        return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        u0, u1 = unit(x1 - x0, y1 - y0), unit(x2 - x1, y2 - y1)
        rr = min(r, math.hypot(x1 - x0, y1 - y0) / 2, math.hypot(x2 - x1, y2 - y1) / 2)
        ax, ay = x1 - u0[0] * rr, y1 - u0[1] * rr
        bx, by = x1 + u1[0] * rr, y1 + u1[1] * rr
        sweep = 1 if (u0[0] * u1[1] - u0[1] * u1[0]) > 0 else 0
        d += f' L{f(ax)} {f(ay)} A{f(rr)} {f(rr)} 0 0 {sweep} {f(bx)} {f(by)}'
    d += f' L{f(pts[-1][0])} {f(pts[-1][1])}'
    return d


def rounded_len(pts, r):
    L = plen(pts)
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        rr = min(r, math.hypot(x1 - x0, y1 - y0) / 2, math.hypot(x2 - x1, y2 - y1) / 2)
        L -= 2 * rr - math.pi * rr / 2
    return L


def head_poly(tx, ty, ux, uy, w):
    """A closed, filled arrowhead whose tip sits at (tx, ty), pointing along (ux, uy)."""
    hl, hb = HEAD[w]
    bx, by = tx - ux * hl, ty - uy * hl
    px, py = -uy, ux
    pts = [(tx, ty), (bx + px * hb / 2, by + py * hb / 2), (bx - px * hb / 2, by - py * hb / 2)]
    return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ' Z'


def diamond_poly(tx, ty, ux, uy):
    """The open diamond on an authority connection, 14 by 11 px, its tip at the target."""
    L, W = 14, 11
    px, py = -uy, ux
    c = (tx - ux * L / 2, ty - uy * L / 2)
    pts = [(tx, ty), (c[0] + px * W / 2, c[1] + py * W / 2), (tx - ux * L, ty - uy * L), (c[0] - px * W / 2, c[1] - py * W / 2)]
    return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ' Z'


def trimmed(pts, cut):
    """Shorten a polyline's last segment by cut, so the stroke stops at the arrowhead's base."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ux, uy = unit(x1 - x0, y1 - y0)
    return pts[:-1] + [(x1 - ux * cut, y1 - uy * cut)], (x1, y1, ux, uy)


def ticks(pts, n, w, start=12):
    """Delay ticks: one per band, 2 px wide, 8 px longer than the line is wide, 5 px apart (M4)."""
    out = []
    half = (w + 8) / 2
    for i in range(n):
        x, y, ux, uy = point_at(pts, start + 5 * i)
        px, py = -uy, ux
        out.append(f'M{f(x - px * half)} {f(y - py * half)} L{f(x + px * half)} {f(y + py * half)}')
    return f'<path d="{" ".join(out)}" class="tick" stroke-width="2"/>'


DELAY_N = {'S': 1, 'M': 2, 'L': 3}


def sign_glyph(cx, cy, sign, r=9, cls='sg'):
    """The sign in a circle, as on Dustin's Atlas Visual System sheet: ground-filled, ink ring, bars in ink."""
    bar = r - 3
    d = f'M{f(cx - bar)} {f(cy)} H{f(cx + bar)}'
    if sign == '+':
        d += f' M{f(cx)} {f(cy - bar)} V{f(cy + bar)}'
    return (f'<g class="{cls}" aria-hidden="true"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="sg-ring"/>'
            f'<path d="{d}" class="sg-bar"/></g>')


def wire(pts, w=2, tex='solid', head='arrow', r=None, cls='', n_ticks=0, halo=False, hollow=False, extra=''):
    """One drawn line: case (for keylines), mark, optional ticks and head, and a wide invisible hit path."""
    r = BEND.get(w, 8) if r is None else r
    if head == 'arrow':
        pts2, (tx, ty, ux, uy) = trimmed(pts, HEAD[w][0])
        hd = f'<path d="{head_poly(tx, ty, ux, uy, w)}" class="head"/>'
    elif head == 'diamond':
        pts2, (tx, ty, ux, uy) = trimmed(pts, 14)
        hd = f'<path d="{diamond_poly(tx, ty, ux, uy)}" class="diamond" stroke-width="2"/>'
    else:
        pts2, hd = pts, ''
    d = rounded(pts2, r)
    L = rounded_len(pts2, r)
    if tex == 'dotted':
        L -= 1.5 * w
    dash, cap = fitted(tex, w, L)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    lc = f' stroke-linecap="{cap}"' if cap != 'butt' else ''
    out = ''
    if halo:
        out += f'<path d="{d}" class="halo" stroke-width="{w + 8}"/>'
    if hollow:
        out += (f'<path d="{d}" class="ak-mark" fill="none" stroke-width="{w + 2}"/>'
                f'<path d="{d}" class="hollow-core" fill="none" stroke-width="{w}"/>')
    else:
        out += (f'<path d="{d}" class="ak-case" fill="none"{da}{lc}/>'
                f'<path d="{d}" class="ak-mark" fill="none" stroke-width="{w}"{da}{lc}/>')
    if n_ticks:
        out += ticks(pts2, n_ticks, w)
    out += hd
    out += f'<path d="{rounded(pts, r)}" class="ak-hit"/>'
    return out


def bracket_h(x0, x1, y, side=1, depth=9):
    """A reform bracket on a horizontal line: a U that hugs the line from one side (Atlas Visual System 06)."""
    yy = y + side * depth
    return f'M{f(x0)} {f(y - side * 4)} V{f(yy)} H{f(x1)} V{f(y - side * 4)}'


def bracket_v(y0, y1, x, side=1, depth=9):
    xx = x + side * depth
    return f'M{f(x - side * 4)} {f(y0)} H{f(xx)} V{f(y1)} H{f(x - side * 4)}'


def red(d, job='R-01 targets', w=3, fill='none'):
    """A working-red mark on Newsprint: a 1 px Charcoal keyline each side of the red stroke (design frame memo 5)."""
    return (f'<g data-red="working" data-red-job="{job}"><path d="{d}" class="red-case" stroke-width="{w + 2}" fill="none"/>'
            f'<path d="{d}" class="red-mark" stroke-width="{w}" fill="{fill}"/></g>')


# ------------------------------------------------------------------------------------------- HTML pieces
def chip(word, code, compact=False, tag='span', attrs=''):
    c = ' chip-c' if compact else ''
    return f'<{tag} class="chip{c}"{attrs}><span class="chip-w">{e(word)}</span><span class="chip-k">{e(code)}</span></{tag}>'


def cnt(key, n, cls='', tag='span'):
    return f'<{tag} data-count="{key}"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>{n}</{tag}>'


def link_attrs(lid):
    l = LINKS[lid]
    return (f'data-link="{lid}" data-sign="{sign_attr(l["polarity"])}" data-grade="{l["evidence"]}" '
            f'data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}"')


def tex_swatch(g, w=36):
    """A short sample of a grade's line texture, for text rows (inline SVG, decorative)."""
    tex = tex_of(g)
    dash, cap = fitted(tex, 2, w - 2)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    lc = f' stroke-linecap="{cap}"' if cap != 'butt' else ''
    return (f'<svg class="swatch" width="{w}" height="10" viewBox="0 0 {w} 10" aria-hidden="true">'
            f'<path d="M1 5 H{w - 1}" stroke="currentColor" stroke-width="2" fill="none"{da}{lc}/></svg>')


def sign_svg(sign, size=18):
    r = size / 2 - 1
    return (f'<svg class="signsvg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-hidden="true">'
            f'{sign_glyph(size / 2, size / 2, sign, r)}</svg>')


def link_row(lid, show_from=True, show_to=True, tag='li'):
    """One connection in words, with its sign glyph, verb, grade texture and delay (the lines in words)."""
    l = LINKS[lid]
    s = l['polarity']
    mark = sign_svg(s) if s in ('+', '-') else '<span class="dia" aria-hidden="true"></span>'
    ends = []
    if show_from:
        ends.append(f'{l["from"]} {e(node_label(l["from"]))}')
    if show_to:
        ends.append(f'{l["to"]} {e(node_label(l["to"]))}')
    where = ' to '.join(ends)
    signw = {'+': '+, the two move the same way', '-': f'{MINUS}, they move opposite ways'}.get(s, 'no sign: it says who decides')
    return (f'<{tag} class="lrow" {link_attrs(lid)}>{mark}<span class="lrow-t"><b>{e(verb(s))}</b> '
            f'<span class="code">{lid}</span> <span data-link="{lid}" data-sign="{sign_attr(s)}" data-grade="{l["evidence"]}" data-name="{e(l["name"])}">{e(l["name"])}</span>'
            f'<span class="lrow-m">{where}. Sign {signw}. {tex_swatch(l["evidence"])} {grade_word(l["evidence"])}: {grade_gloss(l["evidence"])}. {delay_words(l["delay"]).capitalize()}.</span></span></{tag}>')


# ------------------------------------------------------------------------------------------- shared: keys and ids
def var_key(n):
    return f'var-{n.lower()}'


def part_key(p):
    return f'area-{p.lower()}'   # so #area-a, the interaction memo's hash for Wealth, opens Wealth's record


def flow_key(a, b):
    return f'flow-{a.lower()}-{b.lower()}'


def loop_key(k):
    return f'loop-{k.lower()}'


def link_key(k):
    return f'link-{k.lower()}'


def neighbors(n):
    out = set()
    for l in LINKS.values():
        if l['from'] == n:
            out.add(var_key(l['to']))
        if l['to'] == n:
            out.add(var_key(l['from']))
    return sorted(out)


def var_say(n):
    N = NODES[n]
    return f'{n} {N["label"]}. {N["increase_means"]}'


def loop_steps_attr(k):
    return 'sketch' if LOOPS[k]['conceptual'] else ' '.join(s['id'] for s in LOOPS[k]['steps'])


def loop_href(k):
    return '#loop-r10' if k == 'R10' else f'#loops/{loop_key(k)}'


def flow_words(a, b):
    n = len(FLOW[(a, b)])
    return f'{part_name(a)} to {part_name(b)}: {n} {plural(n, "connection")}'


# ------------------------------------------------------------------------------------------- 01 overview: the circuit
CW = 1312                    # drawing width at 1440 px (12 columns)
LANE_L, LANE_R = 8, CW - 8   # edge lanes for outside forces into the channel
CX0, CX1, GAP = 36, CW - 36, 52
CARD_W = (CX1 - CX0 - 4 * GAP) / 5
STRIP_H, DROP = 88, 52


def card_x(p):
    return CX0 + CORE.index(p) * (CARD_W + GAP)


def part_card(p, x, y, w, sec=None, red_c2=False):
    """A part as a reference card: plain name over formal title, question, what it is, every variable, what it
    passes on, inside count and the loops based here. Four sections, aligned across the five cards when sec gives
    each section's height. Returns (svg, [section heights])."""
    P_ = PARTS[p]
    acc_col = ACCENT[LAYER_OF_PART[p]]
    L = x + 20
    inner = w - 32
    o = []
    hs = []
    # section 1: names, question, what it is
    y0 = y
    yy = y + 34
    o.append(f'<a href="#area-c" class="pname" aria-label="Elections, Electoral competition. Opens sheet 02.">' if p == 'C' else
             f'<g role="button" data-select="{part_key(p)}" class="pname" aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. {e(P_["text"])}">')
    o.append(T(L, yy, P_['plain_name'], 'phead', attrs=f' data-part="{p}" data-name="{e(P_["plain_name"])}"', cls='ak-label'))
    yy += 20
    o.append(T(L, yy, f'{p} · {P_["formal_title"]}', 'legend', cls='muted', attrs=f' data-part="{p}" data-name="{e(P_["formal_title"])}"'))
    o.append('</a>' if p == 'C' else '</g>')
    yy += 28
    q = wrap(P_['plain_question'], 'q', inner)
    o.append(TL(L, yy, q, 'q'))
    yy += STY['q'][3] * (len(q) - 1) + 22
    t = wrap(P_['text'], 'cap', inner)
    o.append(TL(L, yy, t, 'cap', cls='muted'))
    yy += STY['cap'][3] * (len(t) - 1) + 18
    hs.append(yy - y0)
    yy = y0 + (sec[0] if sec else hs[0])
    o.append(f'<path d="M{f(x + 20)} {f(yy)} H{f(x + w - 12)}" class="hair"/>')
    # section 2: every variable
    y1 = yy
    yy += 24
    for n in P_['nodes']:
        lab = wrap(node_label(n), 'ptext', inner - 36)
        rows = len(lab)
        o.append(f'<g role="button" data-select="{var_key(n)}" data-rel="{" ".join(neighbors(n))}" aria-label="{e(var_say(n))}" class="vrow">'
                 f'<rect x="{f(x + 12)}" y="{f(yy - 15)}" width="{f(w - 20)}" height="{f(rows * 20 + 4)}" class="vhit"/>'
                 + TL(L, yy, lab, 'ptext', cls='ak-label', attrs=f' data-node="{n}" data-name="{e(node_label(n))}"')
                 + T(x + w - 14, yy, n, 'legend', anchor='end', cls='muted')
                 + '</g>')
        if red_c2 and n == 'C2':
            cx, cy = x + w - 22, yy - 5
            o.append(red(f'M{f(cx - 7)} {f(cy)} a7 7 0 1 0 14 0 a7 7 0 1 0 -14 0', w=2))
            o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="2.5" class="red-dot" data-red="working" data-red-job="R-01 targets"/>')
        yy += rows * 20 + 6
    yy += 4
    hs.append(yy - y1)
    yy = y1 + (sec[1] if sec else hs[1])
    o.append(f'<path d="M{f(x + 20)} {f(yy)} H{f(x + w - 12)}" class="hair"/>')
    # section 3: what it passes on along the circuit
    y2 = yy
    yy += 24
    po = passes_on(p)
    eb = wrap(('Passes back to ' if p == 'E' else 'Passes on to ') + part_name(NEXT[p]), 'eyebrow', inner)
    o.append(TL(L, yy, eb, 'eyebrow'))
    yy += 18 * (len(eb) - 1) + 20
    nm = wrap(f'{po["name"]} ({po["id"]})', 'cap', inner)
    o.append(f'<g role="button" data-select="{link_key(po["id"])}" aria-label="{e(po["id"])}: {e(po["name"])}" class="porow">'
             + TL(L, yy, nm, 'cap', cls='ak-label', attrs=f' {link_attrs(po["id"])} data-name="{e(po["name"])}"') + '</g>')
    yy += STY['cap'][3] * (len(nm) - 1) + 14
    hs.append(yy - y2)
    yy = y2 + (sec[2] if sec else hs[2])
    o.append(f'<path d="M{f(x + 20)} {f(yy)} H{f(x + w - 12)}" class="hair"/>')
    # section 4: a reform at work (Elections only), inside count, loops based here
    y3 = yy
    yy += 22
    n_in = len(INSIDE.get(p, []))
    ins = wrap(f'{nw(n_in).capitalize() if n_in == 0 else n_in} {plural(n_in, "connection")} inside this part', 'note', inner)
    o.append(TL(L, yy, ins, 'note', cls='muted'))
    yy += 16 * (len(ins) - 1) + 22
    hl = loops_home(p)
    o.append(T(L, yy, 'Loops based here' if hl else 'No loop is based here', 'note', cls='muted'))
    if hl:
        yy += 8
        cx_ = L
        for k in hl:
            wk = tw(k, 'code') + 14
            if cx_ + wk > x + w - 12:
                cx_ = L
                yy += 30
            o.append(f'<a href="{loop_href(k)}" class="lchip" data-loop="{k}" data-steps="{loop_steps_attr(k)}" aria-label="Loop {k}, {e(LOOPS[k]["plain_name"])}. Opens it.">'
                     f'<rect x="{f(cx_)}" y="{f(yy)}" width="{f(wk)}" height="24" class="lchip-r"/>'
                     + T(cx_ + 7, yy + 17, k, 'code') + '</a>')
            cx_ += wk + 6
        yy += 24
    if red_c2:
        yy += 28
        tg = REFORMS['R-01']['targets']
        cx = L + 7
        o.append(red(f'M{f(cx - 7)} {f(yy - 5)} a7 7 0 1 0 14 0 a7 7 0 1 0 -14 0', w=2))
        o.append(f'<circle cx="{f(cx)}" cy="{f(yy - 5)}" r="2.5" class="red-dot" data-red="working" data-red-job="R-01 targets"/>')
        rl = wrap(f'Reform R-01 acts on {" and ".join(sorted(t for t in tg if t in NODES))} and on {" and ".join(sorted(t for t in tg if t in LINKS))}.', 'noteb', inner - 22)
        o.append(f'<a href="#reform-r01" aria-label="Reform R-01 acts on C2, L08 and L25. Opens sheet 04.">' + TL(L + 22, yy, rl, 'noteb', cls='ak-label') + '</a>')
        yy += STY['note'][3] * (len(rl) - 1) + 24
    yy += 18
    hs.append(yy - y3)
    hh = sum(sec) if sec else sum(hs)
    frame = (f'<rect x="{f(x + 0.5)}" y="{f(y + 0.5)}" width="{f(w - 1)}" height="{f(hh - 1)}" class="card"/>'
             f'<rect x="{f(x)}" y="{f(y)}" width="6" height="{f(hh)}" fill="{acc_col}" class="accent"/>')
    return frame + ''.join(o), hs


def strip_svg(y):
    X = PARTS['X']
    o = [f'<rect x="0.5" y="{f(y + 0.5)}" width="{CW - 1}" height="{STRIP_H - 1}" class="frame-open"/>']
    o.append(f'<g role="button" data-select="part-x" aria-label="{e(X["plain_name"])}, {e(X["formal_title"])}. {e(X["text"])}" class="pname">'
             + T(24, y + 36, X['plain_name'], 'phead', cls='ak-label', attrs=f' data-part="X" data-name="{e(X["plain_name"])}"')
             + T(24, y + 58, X['formal_title'] + ', taken as given', 'legend', cls='muted', attrs=f' data-part="X" data-name="{e(X["formal_title"])}"') + '</g>')
    t = wrap(X['text'], 'cap', 250)
    o.append(TL(236, y + 32, t, 'cap', cls='muted'))
    xs = 540
    span = (CW - 24 - xs) / 5
    for i, n in enumerate(X['nodes']):
        xx = xs + i * span
        lab = wrap(node_label(n), 'ptext', span - 60)
        o.append(f'<g role="button" data-select="{var_key(n)}" data-rel="{" ".join(neighbors(n))}" aria-label="{e(var_say(n))}" class="vrow">'
                 f'<rect x="{f(xx - 6)}" y="{f(y + 18)}" width="{f(span - 4)}" height="52" class="vhit"/>'
                 + TL(xx, y + 38, lab, 'ptext', cls='ak-label', attrs=f' data-node="{n}" data-name="{e(node_label(n))}"')
                 + T(xx + span - 22, y + 38, n, 'legend', anchor='end', cls='muted') + '</g>')
    return ''.join(o)


class Flows:
    """Bundled flows between parts: each a button holding its route, its count and gap patches where it passes over."""

    def __init__(self):
        self.groups = []
        self.keys = set()

    def add(self, a, b, pts, w=2, label=None, over=(), extra_pts=None):
        ids = FLOW[(a, b)]
        self.keys.add((a, b))
        n = len(ids)
        gaps = ''.join(f'<rect x="{f(gx - 4)}" y="{f(gy - w / 2 - 5)}" width="8" height="{f(w + 10)}" class="gap"/>' if horiz else
                       f'<rect x="{f(gx - w / 2 - 5)}" y="{f(gy - 4)}" width="{f(w + 10)}" height="8" class="gap"/>'
                       for gx, gy, horiz in over)
        body = wire(pts, w=w, tex='solid', head='arrow')
        if extra_pts:
            for ep in extra_pts:
                body += wire(ep, w=w, tex='solid', head='arrow')
        lab = ''
        if label:
            lx, ly, sty, anchor, pad = label
            if pad:
                wd = tw(str(n), sty) + 10
                hgt = STY[sty][2] + 4
                lab += f'<rect x="{f(lx - wd / 2)}" y="{f(ly - hgt + 4)}" width="{f(wd)}" height="{f(hgt)}" class="gap"/>'
            lab += T(lx, ly, str(n), sty, anchor=anchor, cls='ak-label cnt', attrs=f' data-count="custom:flow {a}-{b}"')
        ends = sorted({var_key(LINKS[k]['from']) for k in ids} | {var_key(LINKS[k]['to']) for k in ids})
        say = f'{flow_words(a, b)}. Opens the list of connections.'
        self.groups.append(f'<g role="button" data-select="{flow_key(a, b)}" data-rel="{" ".join(ends)}" aria-label="{e(say)}" class="flow{" main" if w == 3 else ""}">{gaps}{body}{lab}</g>')

    def svg(self):
        return ''.join(self.groups)


def overview_circuit():
    """The whole system after Dustin's Concept 09, simplified: five cards read left to right, outside forces above,
    the household and technology channel beneath, and only bundled flows with their counts."""
    y_strip = 0
    cy = STRIP_H + DROP
    # card heights: lay out once to measure, then equalize
    secs = [part_card(p, card_x(p), cy, CARD_W, red_c2=(p == 'C'))[1] for p in CORE]
    sec = [max(h[i] for h in secs) for i in range(4)]
    ch_card = sum(sec)
    cards = ''.join(part_card(p, card_x(p), cy, CARD_W, sec=sec, red_c2=(p == 'C'))[0] for p in CORE)
    yb = cy + ch_card
    X = {p: card_x(p) for p in CORE}
    W_ = CARD_W
    l1a, l1b, l2, l3 = yb + 22, yb + 42, yb + 64, yb + 100
    bus_t, bus_e = yb + 134, yb + 158
    ych = yb + 196
    # channel cards
    ec_x, ec_w = X['A'], X['C'] + W_ - X['A']
    tc_x, tc_w = X['D'], X['E'] + W_ - X['D']
    ec_svg, ec_h = channel_card('EC', ec_x, ych, ec_w)
    tc_svg, tc_h = channel_card('TC', tc_x, ych, tc_w)
    hh = max(ec_h, tc_h)
    ec_svg, _ = channel_card('EC', ec_x, ych, ec_w, hh)
    tc_svg, _ = channel_card('TC', tc_x, ych, tc_w, hh)
    H = ych + hh + 4
    F = Flows()
    # outside forces: drops into each core card, edge lanes into the channel
    for p in CORE:
        x = X[p] + 24
        F.add('X', p, [(x, STRIP_H + 2), (x, cy - 2)], label=(x + 8, STRIP_H + DROP / 2 + 6, 'map', 'start', False))
    F.add('X', 'EC', [(LANE_L, STRIP_H + 2), (LANE_L, ych + 34), (ec_x - 2, ych + 34)], label=(LANE_L + 8, STRIP_H + 26, 'map', 'start', False))
    F.add('X', 'TC', [(LANE_R, STRIP_H + 2), (LANE_R, ych + 34), (tc_x + tc_w + 2, ych + 34)], label=(LANE_R - 8, STRIP_H + 26, 'map', 'end', False))
    # A and the household, straight down and up
    F.add('A', 'EC', [(X['A'] + 28, yb + 2), (X['A'] + 28, ych - 2)], label=(X['A'] + 36, yb + 18, 'map', 'start', False))
    F.add('EC', 'A', [(X['A'] + 60, ych - 2), (X['A'] + 60, yb + 2)], label=(X['A'] + 68, ych - 8, 'map', 'start', False))
    # technology up to Voice and Wealth: one trunk from the technology card, branching
    x_tc = tc_x + 22
    F.add('TC', 'B', [(x_tc, ych - 2), (x_tc, bus_t), (X['B'] + 28, bus_t), (X['B'] + 28, yb + 2)],
          label=(X['B'] + 36, yb + 18, 'map', 'start', False))
    F.add('TC', 'A', [(x_tc, ych - 2), (x_tc, bus_t), (X['A'] + 112, bus_t), (X['A'] + 112, yb + 2)],
          label=(X['A'] + 120, yb + 18, 'map', 'start', False))
    # checks and technology, straight down and up
    xd_tc, xtc_d, xd_ec = X['D'] + 150, X['D'] + 182, X['D'] + 112
    F.add('D', 'TC', [(xd_tc, yb + 2), (xd_tc, ych - 2)], label=(xd_tc + 8, yb + 18, 'map', 'start', False))
    F.add('TC', 'D', [(xtc_d, ych - 2), (xtc_d, yb + 2)], label=(xtc_d + 8, ych - 8, 'map', 'start', False))
    # checks and policy into the household, one trunk along the lower bus (passes over the technology lines)
    x_land = X['C'] + W_ - 40
    over_e = [(xtc_d, bus_e, False), (xd_tc, bus_e, False), (x_tc, bus_e, False)]
    F.add('D', 'EC', [(xd_ec, yb + 2), (xd_ec, bus_e), (x_land, bus_e), (x_land, ych - 2)], label=(xd_ec + 8, yb + 18, 'map', 'start', False),
          over=[(x_tc, bus_e, False)])
    F.add('E', 'EC', [(X['E'] + 150, yb + 2), (X['E'] + 150, bus_e), (x_land, bus_e), (x_land, ych - 2)], label=(X['E'] + 158, yb + 18, 'map', 'start', False),
          over=over_e)
    # skips under the row: Voice and Checks both ways, Voice to Policy
    F.add('B', 'D', [(X['B'] + 172, yb + 2), (X['B'] + 172, l1a), (X['D'] + 28, l1a), (X['D'] + 28, yb + 2)],
          label=(X['C'] + 62, l1a + 5, 'map', 'middle', True))
    F.add('D', 'B', [(X['D'] + 60, yb + 2), (X['D'] + 60, l1b), (X['B'] + 134, l1b), (X['B'] + 134, yb + 2)],
          label=(X['C'] + W_ / 2, l1b + 5, 'map', 'middle', True))
    F.add('B', 'E', [(X['B'] + 94, yb + 2), (X['B'] + 94, l2), (X['E'] + 28, l2), (X['E'] + 28, yb + 2)],
          label=(X['C'] + W_ - 62, l2 + 5, 'map', 'middle', True), over=[(xd_ec, l2, False), (xd_tc, l2, False), (xtc_d, l2, False)])
    # the main circuit: forward across each gap, and the return line along the bottom
    for a in CORE[:-1]:
        b = NEXT[a]
        x0, x1 = X[a] + W_ + 2, X[b] - 2
        yf = cy + 44
        F.add(a, b, [(x0, yf), (x1, yf)], w=3, label=((x0 + x1) / 2, yf - 12, 'count', 'middle', False))
        if (b, a) in FLOW:
            yk = cy + 92
            F.add(b, a, [(x1, yk), (x0, yk)], label=((x0 + x1) / 2, yk + 24, 'map', 'middle', False))
    F.add('E', 'A', [(X['E'] + 72, yb + 2), (X['E'] + 72, l3), (X['A'] + 164, l3), (X['A'] + 164, yb + 2)], w=3,
          label=(X['C'] + W_ / 2, l3 + 8, 'count', 'middle', True),
          over=[(xd_ec, l3, False), (xd_tc, l3, False), (xtc_d, l3, False), (X['B'] + 28, l3, False)])
    F.add('TC', 'EC', [(tc_x - 2, ych + 60), (ec_x + ec_w + 2, ych + 60)], label=((tc_x + ec_x + ec_w) / 2, ych + 50, 'map', 'middle', False))
    ret_note = T(X['C'] + W_ / 2, l3 + 26, 'The return line', 'eyebrow', anchor='middle')
    svg = (f'<svg data-view="overview" class="draw circuit" viewBox="0 0 {CW} {f(H)}" width="{CW}" height="{f(H)}" role="group" '
           f'aria-labelledby="ov-h" aria-describedby="ov-words" data-ak-roving data-ak-nav="spatial">'
           f'{strip_svg(y_strip)}{cards}{ec_svg}{tc_svg}{F.svg()}{ret_note}</svg>')
    return svg


def channel_card(p, x, y, w, h=None):
    P_ = PARTS[p]
    acc_col = ACCENT[LAYER_OF_PART[p]]
    L = x + 20
    o = []
    yy = y + 34
    o.append(f'<g role="button" data-select="{part_key(p)}" class="pname" aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. {e(P_["text"])}">'
             + T(L, yy, P_['plain_name'], 'phead', cls='ak-label', attrs=f' data-part="{p}" data-name="{e(P_["plain_name"])}"'))
    o.append(T(L + tw(P_['plain_name'], 'phead') + 12, yy, P_['formal_title'], 'legend', cls='muted', attrs=f' data-part="{p}" data-name="{e(P_["formal_title"])}"') + '</g>')
    yy += 26
    qw = tw(P_['plain_question'], 'q')
    o.append(T(L, yy, P_['plain_question'], 'q'))
    n_in = len(INSIDE.get(p, []))
    o.append(T(L + qw + 14, yy, f'Inside: {n_in} {plural(n_in, "connection")}', 'note', cls='muted'))
    yy += 18
    groups = P_['groups'] or [{'title': None, 'nodes': P_['nodes'][:4]}, {'title': None, 'nodes': P_['nodes'][4:]}]
    colw = (w - 40) / len(groups)
    top = yy + 14
    bottom = top
    for gi, g in enumerate(groups):
        gx = L + gi * colw
        gy = top
        if g['title']:
            gy += 14
            o.append(T(gx, gy, g['title'], 'noteb'))
            gy += 22
        else:
            gy += 18
        for n in g['nodes']:
            lab = wrap(node_label(n), 'ptext', colw - 66)
            o.append(f'<g role="button" data-select="{var_key(n)}" data-rel="{" ".join(neighbors(n))}" aria-label="{e(var_say(n))}" class="vrow">'
                     f'<rect x="{f(gx - 8)}" y="{f(gy - 15)}" width="{f(colw - 8)}" height="{f(len(lab) * 20 + 4)}" class="vhit"/>'
                     + TL(gx, gy, lab, 'ptext', cls='ak-label', attrs=f' data-node="{n}" data-name="{e(node_label(n))}"')
                     + T(gx + colw - 22, gy, n, 'legend', anchor='end', cls='muted') + '</g>')
            gy += len(lab) * 20 + 6
        bottom = max(bottom, gy)
    yy = bottom + 10
    hh = h or (yy - y)
    frame = (f'<rect x="{f(x + 0.5)}" y="{f(y + 0.5)}" width="{f(w - 1)}" height="{f(hh - 1)}" class="card"/>'
             f'<rect x="{f(x)}" y="{f(y)}" width="6" height="{f(hh)}" fill="{acc_col}" class="accent"/>')
    return frame + ''.join(o), yy - y


def overview_cards():
    """Plate 01.2: every part and every condition, as reference cards with no wiring (the flows live on plate 01.1
    and in the flow table)."""
    cy = STRIP_H + 24
    secs = [part_card(p, card_x(p), cy, CARD_W)[1] for p in CORE]
    sec = [max(h[i] for h in secs) for i in range(4)]
    cards = ''.join(part_card(p, card_x(p), cy, CARD_W, sec=sec)[0] for p in CORE)
    yb = cy + sum(sec)
    X = {p: card_x(p) for p in CORE}
    ych = yb + 24
    ec_x, ec_w = X['A'], X['C'] + CARD_W - X['A']
    tc_x, tc_w = X['D'], X['E'] + CARD_W - X['D']
    hh = max(channel_card('EC', ec_x, ych, ec_w)[1], channel_card('TC', tc_x, ych, tc_w)[1])
    ec_svg, _ = channel_card('EC', ec_x, ych, ec_w, hh)
    tc_svg, _ = channel_card('TC', tc_x, ych, tc_w, hh)
    H = ych + hh + 2
    return (f'<svg data-view="overview-cards" class="draw cards" viewBox="0 0 {CW} {f(H)}" width="{CW}" height="{f(H)}" role="group" '
            f'aria-labelledby="ov-cards-h" data-ak-roving data-ak-nav="spatial">{strip_svg(0)}{cards}{ec_svg}{tc_svg}</svg>')


def circuit_compact():
    """Plate 01.1, the first screen: all eight parts by plain name, formal title and question, and the main flows
    between them with their counts. Seven small bundles that skip a part are left to the flow table (plate 01.3)."""
    X = {p: card_x(p) for p in CORE}
    BW = CARD_W
    SH, DR = 52, 36
    o = []
    # outside forces
    Xp = PARTS['X']
    o.append(f'<rect x="0.5" y="0.5" width="{CW - 1}" height="{SH - 1}" class="frame-open"/>')
    o.append(f'<g role="button" data-select="{part_key("X")}" aria-label="{e(Xp["plain_name"])}, {e(Xp["formal_title"])}. {e(Xp["text"])}" class="pname">'
             f'<rect x="1" y="1" width="{CW - 2}" height="{SH - 2}" class="vhit"/>'
             + T(24, 34, Xp['plain_name'], 'phead', cls='ak-label', attrs=f' data-part="X" data-name="{e(Xp["plain_name"])}"')
             + T(24 + tw(Xp['plain_name'], 'phead') + 12, 34, Xp['formal_title'], 'legend', cls='muted', attrs=f' data-part="X" data-name="{e(Xp["formal_title"])}"')
             + T(CW - 24, 34, Xp['text'], 'cap', anchor='end', cls='muted') + '</g>')
    yc = SH + DR
    # the five core blocks
    qs = {p: wrap(PARTS[p]['plain_question'], 'q', BW - 34) for p in CORE}
    BH = 72 + 20 * max(len(q) - 1 for q in qs.values()) + 18
    for p in CORE:
        P_ = PARTS[p]
        x = X[p]
        inner = (T(x + 18, yc + 30, P_['plain_name'], 'phead', cls='ak-label', attrs=f' data-part="{p}" data-name="{e(P_["plain_name"])}"')
                 + T(x + 18, yc + 48, P_['formal_title'], 'legend', cls='muted', attrs=f' data-part="{p}" data-name="{e(P_["formal_title"])}"')
                 + TL(x + 18, yc + 72, qs[p], 'q'))
        frame = (f'<rect x="{f(x + 0.5)}" y="{f(yc + 0.5)}" width="{f(BW - 1)}" height="{f(BH - 1)}" class="card"/>'
                 f'<rect x="{f(x)}" y="{f(yc)}" width="6" height="{f(BH)}" fill="{ACCENT["core"]}" class="accent"/>')
        if p == 'C':
            o.append(f'<a href="#area-c" class="pname" aria-label="Elections, Electoral competition. {e(P_["plain_question"])} Opens the Elections sheet.">{frame}{inner}</a>')
        else:
            o.append(f'<g role="button" data-select="{part_key(p)}" aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. {e(P_["plain_question"])} {e(P_["text"])}" class="pname">{frame}{inner}</g>')
    yb = yc + BH
    yr = yb + 32
    ych = yr + 46
    # the channel
    ec_x, ec_w = X['A'], X['C'] + BW - X['A']
    tc_x, tc_w = X['D'], X['E'] + BW - X['D']
    CHH = 0
    chans = []
    for pid, cx, cw in (('EC', ec_x, ec_w), ('TC', tc_x, tc_w)):
        CHH = 72
        chans.append((pid, cx, cw, None))
    for pid, cx, cw, txt in chans:
        P_ = PARTS[pid]
        nm_w = tw(P_['plain_name'], 'phead')
        inner = (T(cx + 18, ych + 30, P_['plain_name'], 'phead', cls='ak-label', attrs=f' data-part="{pid}" data-name="{e(P_["plain_name"])}"')
                 + T(cx + 18 + nm_w + 12, ych + 30, P_['formal_title'], 'legend', cls='muted', attrs=f' data-part="{pid}" data-name="{e(P_["formal_title"])}"')
                 + T(cx + 18, ych + 55, P_['plain_question'], 'q'))
        o.append(f'<g role="button" data-select="{part_key(pid)}" aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. {e(P_["plain_question"])} {e(P_["text"])}" class="pname">'
                 f'<rect x="{f(cx + 0.5)}" y="{f(ych + 0.5)}" width="{f(cw - 1)}" height="{f(CHH - 1)}" class="card"/>'
                 f'<rect x="{f(cx)}" y="{f(ych)}" width="6" height="{f(CHH)}" fill="{ACCENT[LAYER_OF_PART[pid]]}" class="accent"/>{inner}</g>')
    H = ych + CHH + 2
    F = Flows()
    for p in CORE:
        x = X[p] + 30
        F.add('X', p, [(x, SH + 1), (x, yc - 2)], label=(x + 9, SH + DR / 2 + 6, 'map', 'start', False))
    F.add('X', 'EC', [(10, SH + 1), (10, ych + 40), (ec_x - 2, ych + 40)], label=(19, SH + DR / 2 + 6, 'map', 'start', False))
    F.add('X', 'TC', [(CW - 10, SH + 1), (CW - 10, ych + 40), (tc_x + tc_w + 2, ych + 40)], label=(CW - 19, SH + DR / 2 + 6, 'map', 'end', False))
    for a in CORE[:-1]:
        b = NEXT[a]
        x0, x1 = X[a] + BW + 2, X[b] - 2
        F.add(a, b, [(x0, yc + 40), (x1, yc + 40)], w=3, label=((x0 + x1) / 2, yc + 28, 'count', 'middle', False))
        if (b, a) in FLOW:
            F.add(b, a, [(x1, yb - 28), (x0, yb - 28)], label=((x0 + x1) / 2, yb - 7, 'map', 'middle', False))
    xa_d, xa_u = X['A'] + 30, X['A'] + 58
    F.add('A', 'EC', [(xa_d, yb + 2), (xa_d, ych - 2)], label=(xa_d - 8, yb + 19, 'map', 'end', False))
    F.add('EC', 'A', [(xa_u, ych - 2), (xa_u, yb + 2)], label=(xa_u + 8, ych - 8, 'map', 'start', False))
    xd_d, xd_u = X['D'] + 30, X['D'] + 58
    F.add('D', 'TC', [(xd_d, yb + 2), (xd_d, ych - 2)], label=(xd_d - 8, yb + 19, 'map', 'end', False))
    F.add('TC', 'D', [(xd_u, ych - 2), (xd_u, yb + 2)], label=(xd_u + 8, ych - 8, 'map', 'start', False))
    F.add('TC', 'EC', [(tc_x - 2, ych + 40), (ec_x + ec_w + 2, ych + 40)], label=((tc_x + ec_x + ec_w) / 2, ych + 30, 'map', 'middle', False))
    xr0, xr1 = X['E'] + BW - 40, X['A'] + BW - 40
    F.add('E', 'A', [(xr0, yb + 2), (xr0, yr), (xr1, yr), (xr1, yb + 2)], w=3,
          label=(X['C'] + BW / 2 + 60, yr + 8, 'count', 'middle', True), over=[(xd_d, yr, False), (xd_u, yr, False)])
    po = passes_on('E')
    rx = X['A'] + BW + 30
    n_ret = len(FLOW[('E', 'A')])
    note = f'{po["name"]} ({po["id"]}), and {nw(n_ret - 1)} more'
    tw(note, 'note')
    if rx + tw('The return line', 'eyebrow') + 10 + tw(note, 'note') > X['D'] + 22:   # keep clear of the Checks lines
        note = f'{po["id"]} and {nw(n_ret - 1)} more'
    ret = (T(rx, yr + 24, 'The return line', 'eyebrow')
           + T(rx + tw('The return line', 'eyebrow') + 10, yr + 24, note, 'note', cls='muted'))
    skipped = [(a, b) for (a, b) in FLOW if (a, b) not in F.keys]
    return (f'<svg data-view="overview" class="draw circuit" viewBox="0 0 {CW} {f(H)}" width="{CW}" height="{f(H)}" role="group" '
            f'aria-labelledby="ov-circ-h" aria-describedby="ov-words" data-ak-roving data-ak-nav="spatial">'
            + ''.join(o) + F.svg() + ret + '</svg>'), skipped


def flow_matrix():
    """Plate 01.3: every flow between parts as a table read like a distance chart. Rows send, columns receive."""
    order = ['X'] + CORE + ['EC', 'TC']
    main = {(a, NEXT[a]) for a in CORE}
    head = ''.join(f'<th scope="col"><span class="mx-n">{e(part_name(q))}</span></th>' for q in order)
    rows = []
    for a in order:
        cells = []
        for b in order:
            if a == b:
                n = len(INSIDE.get(a, []))
                cells.append(f'<td class="mx-in"><span title="Inside {e(part_name(a))}">{n if n else ""}</span></td>')
            elif (a, b) in FLOW:
                n = len(FLOW[(a, b)])
                cells.append(f'<td class="{"mx-main" if (a, b) in main else ""}"><button type="button" class="mx-b" data-select="{flow_key(a, b)}" '
                             f'aria-label="{e(flow_words(a, b))}. Opens the list."><span data-count="custom:flow {a}-{b}">{n}</span></button></td>')
            else:
                cells.append('<td class="mx-0"><span aria-label="none">·</span></td>')
        out = sum(len(v) for (x, _), v in FLOW.items() if x == a)
        rows.append(f'<tr><th scope="row"><span class="mx-n">{e(part_name(a))}</span><span class="mx-f">{e(PARTS[a]["formal_title"])}</span></th>{"".join(cells)}'
                    f'<td class="mx-t">{out}</td></tr>')
    tot = ''.join(f'<td class="mx-t">{sum(len(v) for (_, y), v in FLOW.items() if y == b)}</td>' for b in order)
    return (f'<div class="mx-wrap"><table class="mx t-cap" data-ak-roving data-ak-nav="spatial" aria-describedby="mx-cap">'
            f'<caption id="mx-cap" class="t-cap">Read across a row to see where a part sends its influence, and down a column to see where it comes from. '
            f'Bold boxes are the main circuit. Gray cells count the connections inside a part. Select a number to list its connections.</caption>'
            f'<thead><tr><th scope="col" class="mx-corner">From ↓ to →</th>{head}<th scope="col">Out</th></tr></thead>'
            f'<tbody>{"".join(rows)}<tr class="mx-tr"><th scope="row">In</th>{tot}<td class="mx-t">{CROSS}</td></tr></tbody></table></div>'
            f'<p class="ak-readout t-cap" data-ak-readout>Arrow keys move between numbers. Enter opens one.</p>')


def mini_circuit():
    """The phone's first two screens: the eight parts in circuit order, each with its question, joined by counts."""
    def item(p):
        P_ = PARTS[p]
        q = P_['plain_question'] or P_['text']
        nm = (f'<a href="#area-c">{e(P_["plain_name"])}</a>' if p == 'C' else
              f'<button type="button" class="mc-b" data-select="{part_key(p)}" aria-label="{e(P_["plain_name"])}, {e(P_["formal_title"])}. Opens its record.">{e(P_["plain_name"])}</button>')
        return (f'<li class="mc-i lay-{LAYER_OF_PART[p]}{" open-frame" if p == "X" else ""}"><p class="mc-n"><span class="t-phead">{nm}</span> '
                f'<span class="mc-f t-legend muted">{e(P_["formal_title"])}</span></p><p class="mc-q">{e(q)}</p></li>')

    def conn(text, n, cls=''):
        return f'<li class="mc-c {cls}" aria-hidden="true"><span class="mc-cn">{n}</span>{e(text)}</li>'
    x_out = sum(len(v) for (a, _), v in FLOW.items() if a == 'X')
    li = [item('X'), conn('reach the system from outside', x_out)]
    for p in CORE:
        li.append(item(p))
        if p != 'E':
            li.append(conn(f'pass on to {part_name(NEXT[p])}', len(FLOW[(p, NEXT[p])])))
    li.append(conn('carry policy back to Wealth: the return line', len(FLOW[('E', 'A')]), 'ret'))
    li.append(item('EC'))
    li.append(conn(f'from Wealth, and {len(FLOW[("EC", "A")])} back to Wealth', len(FLOW[('A', 'EC')])))
    li.append(item('TC'))
    li.append(conn('into Your household', len(FLOW[('TC', 'EC')])))
    return f'<ol class="mini" aria-label="The eight parts in circuit order">{"".join(li)}</ol>'


# ------------------------------------------------------------------------------------------- sheets and plates
SHEETS = [   # view, sheet number, tab name, crumb, parent
    ('how-to-read', '00', 'How to read', 'Sheet 00, How to read', 'overview'),
    ('overview', '01', 'The system', 'Overview', None),
    ('area-c', '02', 'Elections', 'Sheet 02, Elections', 'overview'),
    ('loop-r10', '03', 'Loop R10', 'Sheet 03, Loop R10', 'area-c'),
    ('reform-r01', '04', 'Reform R-01', 'Sheet 04, Reform R-01', 'overview'),
    ('loops', '05', 'All loops', 'Sheet 05, All 23 loops', 'overview'),
]
SHEET_NO = {v: n for v, n, *_ in SHEETS}


def keyplan(here):
    """A locator: a small copy of the overview's circuit, the current part in ink (interaction memo, locator)."""
    w, h = 132, 80
    o = [f'<svg class="keyplan" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    o.append(f'<rect x="0.5" y="0.5" width="{w - 1}" height="12" class="kp-open"/>')
    cw, g = 22, 5
    for i, p in enumerate(CORE):
        x = 4 + i * (cw + g)
        on = p in here
        o.append(f'<rect x="{x + 0.5}" y="20.5" width="{cw - 1}" height="30" class="{"kp-on" if on else "kp"}"/>')
    o.append(f'<rect x="4.5" y="58.5" width="{3 * cw + 2 * g - 1}" height="18" class="{"kp-on" if "EC" in here else "kp"}"/>')
    o.append(f'<rect x="{4 + 3 * (cw + g) + 0.5}" y="58.5" width="{2 * cw + g - 1}" height="18" class="{"kp-on" if "TC" in here else "kp"}"/>')
    o.append('</svg>')
    return f'<a href="#overview" class="kp-link" aria-label="You are here. Opens the whole system.">{"".join(o)}<span class="t-note">You are here</span></a>'


def evidence_key(hollow=False, lead='Every connection carries a grade for its evidence'):
    """The evidence key (fix 12): the five V7 grades with their textures and glosses."""
    grades = ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis']
    items = ''.join(f'<li>{tex_swatch(g, 36)}<span><b>{grade_word(g)}</b> {grade_gloss(g)}</span></li>' for g in grades)
    if hollow:
        items += f'<li><svg class="swatch" width="36" height="10" viewBox="0 0 36 10" aria-hidden="true"><path d="M1 5 H35" stroke="currentColor" stroke-width="4"/><path d="M1 5 H35" stroke="#DCD9D2" stroke-width="2"/></svg><span><b>Hollow</b> a sketched step</span></li>'
    return f'<div class="evkey"><p class="t-eyebrow">{e(lead)}</p><ul class="t-legend">{items}</ul></div>'


def sheet_head(view, eyebrow, title, deck_html, side_html='', here=(), title_attrs=''):
    """The sheet's head. An "On this sheet" list passed in side_html becomes a bar that stays in view (red team S3)."""
    no = SHEET_NO[view]
    bar = ''
    m = re.search(r'<nav class="toc".*?</nav>', side_html, flags=re.S)
    if m:
        bar = m.group(0).replace('class="toc"', 'class="toc platebar"', 1)
        side_html = side_html.replace(m.group(0), '')
    return (f'<header class="sheet-head">'
            f'<div class="sh-main"><p class="sh-no"><span class="t-fig">{no}</span><span class="t-eyebrow">{eyebrow}</span></p>'
            f'<h1 class="{"t-disp" if view == "overview" else "t-head h1-sub"}" data-ak-heading id="h-{view}"{title_attrs}>{title}</h1>'
            + (f'<div class="t-deck sh-deck">{deck_html}</div>' if deck_html else '') + '</div>'
            f'<aside class="sh-side">{"" if view == "overview" else keyplan(here)}{side_html}</aside></header>{bar}')


def plate(pid, no, title, dek_html, body, foot='', cls=''):
    return (f'<section class="plate {cls}" id="{pid}" aria-labelledby="{pid}-h">'
            f'<header class="plate-head"><p class="plate-no t-eyebrow">{no}</p>'
            f'<h2 class="t-head" id="{pid}-h">{title}</h2>'
            + (f'<div class="plate-dek t-deck">{dek_html}</div>' if dek_html else '') + '</header>'
            f'{body}'
            + (f'<p class="plate-foot t-note"><span>{foot}</span><span>Atlas V7, snapshot {SNAP}</span></p>' if foot else '')
            + '</section>')


def toc(items):
    lis = ''.join(f'<li><a href="#{pid}" data-toc><span class="tn">{no}</span> {e(t)}</a></li>' for pid, no, t in items)
    return f'<nav class="toc" aria-label="On this sheet"><p class="t-eyebrow">On this sheet</p><ol>{lis}</ol></nav>'


# ------------------------------------------------------------------------------------------- 01 overview: HTML
def flows_of(p):
    out = [(b, FLOW[(a, b)]) for (a, b) in FLOW if a == p]
    inn = [(a, FLOW[(a, b)]) for (a, b) in FLOW if b == p]
    order = ['X'] + CORE + ['EC', 'TC']
    return sorted(out, key=lambda t: order.index(t[0])), sorted(inn, key=lambda t: order.index(t[0]))


def stack_card(p):
    P_ = PARTS[p]
    lay = LAYER_OF_PART[p]
    vars_ = ''.join(f'<li><button type="button" class="vbtn" data-select="{var_key(n)}" aria-label="{e(var_say(n))}">'
                    f'<span class="ak-label" data-node="{n}" data-name="{e(node_label(n))}">{e(node_label(n))}</span><span class="vcode">{n}</span></button></li>'
                    for n in P_['nodes'])
    out, inn = flows_of(p)

    def fl(lst, to):
        items = []
        for q, ids in lst:
            a, b = (p, q) if to else (q, p)
            main = (b == NEXT.get(a)) and a in CORE
            items.append(f'<li><button type="button" class="fbtn{" main" if main else ""}" data-select="{flow_key(a, b)}" aria-label="{e(flow_words(a, b))}. Opens the list.">'
                         f'<span class="fnum" data-count="custom:flow {a}-{b}">{len(ids)}</span> {"to" if to else "from"} {e(part_name(q))}</button></li>')
        return ''.join(items)
    q = f'<p class="sc-q">{e(P_["plain_question"])}</p>' if P_['plain_question'] else ''
    open_c = '<p class="sc-open"><a href="#area-c" class="btnlink">Open the Elections sheet</a></p>' if p == 'C' else ''
    loops = loops_home(p)
    lp = ('<div class="sc-loops"><p class="t-eyebrow">Loops based here</p><p>' + ''.join(f'<a class="lpill" href="{loop_href(k)}" data-loop="{k}" data-steps="{loop_steps_attr(k)}" aria-label="Loop {k}, {e(LOOPS[k]["plain_name"])}">{k}</a>' for k in loops) + '</p></div>') if loops else ''
    po = passes_on(p) if p in CORE else None
    pas = (f'<p class="sc-pass"><span class="t-eyebrow">{"Passes back to " if p == "E" else "Passes on to "}{e(part_name(NEXT[p]))}</span> '
           f'<span {link_attrs(po["id"])} data-name="{e(po["name"])}">{e(po["name"])}</span> <span class="vcode">{po["id"]}</span></p>') if po else ''
    return (f'<li class="scard lay-{lay}{" open-frame" if p == "X" else ""}"><div class="sc-head">'
            f'<h3 class="t-phead"><span data-part="{p}" data-name="{e(P_["plain_name"])}">{e(P_["plain_name"])}</span></h3>'
            f'<p class="t-legend muted"><span data-part="{p}" data-name="{e(P_["formal_title"])}">{e(P_["formal_title"])}</span></p>{q}'
            f'<p class="t-cap muted">{e(P_["text"])}</p></div>'
            f'<ul class="sc-vars">{vars_}</ul>{pas}'
            f'<div class="sc-flows"><div><p class="t-eyebrow">Flows out</p><ul>{fl(out, True)}</ul></div>'
            + (f'<div><p class="t-eyebrow">Flows in</p><ul>{fl(inn, False)}</ul></div>' if inn else '') + f'</div>{lp}{open_c}</li>')


def overview_stack():
    items = [stack_card('X')]
    for i, p in enumerate(CORE):
        items.append(stack_card(p))
        if p != 'E':
            n = len(FLOW[(p, NEXT[p])])
            items.append(f'<li class="sconn" aria-hidden="true"><span class="sconn-n">{n}</span> {plural(n, "connection")} pass on to {e(part_name(NEXT[p]))}</li>')
    n = len(FLOW[('E', 'A')])
    items.append(f'<li class="sconn ret" aria-hidden="true"><span class="sconn-n">{n}</span> {plural(n, "connection")} carry policy back to Wealth: the return line</li>')
    items.append(stack_card('EC'))
    items.append(stack_card('TC'))
    return f'<ol class="stack" aria-label="The whole system, part by part">{"".join(items)}</ol>'


def pathway_target(pw):
    refs = pw['model_refs']
    if refs.get('loops'):
        k = refs['loops'][0]
        return loop_href(k), f'Open loop {k}, the {low(LOOPS[k]["plain_name"])}'
    if refs.get('nodes'):
        p = PART_OF[refs['nodes'][0]]
        return (f'#area-c' if p == 'C' else f'#overview/{part_key(p)}'), f'Open {part_name(p)}'
    return '#overview', 'Overview'


def questions_html():
    """Each question opens its short answer first, with the loop or part it runs through as a link (civic finding 4)."""
    pws = {p['id']: p for p in D['pathways']}
    rows = []
    for h in D['hubs']:
        lis = []
        for pid in h['pathways']:
            pw = pws[pid]
            href, lab = pathway_target(pw)
            parts = []
            for n in pw['model_refs'].get('nodes', []):
                pn = part_name(PART_OF[n])
                if pn not in parts:
                    parts.append(pn)
            loops = pw['model_refs'].get('loops', [])
            meta = 'Runs through ' + ', '.join(parts[:-1]) + (' and ' if len(parts) > 1 else '') + parts[-1] if parts else ''
            if loops:
                meta += f' · {plural(len(loops), "Loop")} ' + ', '.join(loops)
            lis.append(f'<li><details class="qd"><summary><span class="qlink">{e(pw["question"])}</span><span class="t-note muted">{e(meta)}</span></summary>'
                       f'<div class="qa"><p class="t-ptext">{e(pw["short_answer"])}</p><p class="t-cap"><a class="tlink" href="{href}">{e(lab)}</a></p></div></details></li>')
        rows.append(f'<div class="hub"><div class="hub-h"><p class="t-eyebrow">{e(h["title"])}</p><h3 class="t-phead">{e(h["question"])}</h3></div><ol>{"".join(lis)}</ol></div>')
    return f'<div class="hubs">{"".join(rows)}</div>'


def flows_in_words():
    order = ['X'] + CORE + ['EC', 'TC']
    items = []
    for (a, b) in sorted(FLOW, key=lambda t: (order.index(t[0]), order.index(t[1]))):
        ids = FLOW[(a, b)]
        items.append(f'<li><b>{e(flow_words(a, b))}.</b> ' + '; '.join(f'{k} {e(LINKS[k]["name"])}' for k in ids) + '.</li>')
    return items


def overview_view():
    n_parts = len(D['parts'])
    deck = ('<p class="t-ptext">Read the five parts from left to right: wealth, voice, elections, checks and policy. Each passes influence to '
            'the next, and policy passes some of it back to wealth. Every connection carries a grade for how strong its evidence is.</p>')
    spec = (f'<p class="t-cap counts"><b>{cnt("variables", COUNTS["variables"])}</b> conditions in {nw(n_parts)} parts · '
            f'<b>{cnt("connections", COUNTS["connections"])}</b> connections, {cnt("custom:crossing", CROSS)} between parts · '
            f'<b>{cnt("loops", COUNTS["loops"])}</b> loops · <b>{cnt("reforms", COUNTS["reforms"])}</b> reforms</p>')
    links = ('<p class="t-cap sh-links"><a href="#how-to-read">How to read every mark</a> · <a href="#area-c">Open one part, Elections</a> · '
             f'<a href="#ov-questions" data-toc>Start from a question</a></p>')
    head = (f'<header class="sheet-head sh-ov"><p class="sh-no"><span class="t-fig">01</span><span class="t-eyebrow">Who Do They Answer To? \u00b7 The whole system</span></p>'
            f'<h1 class="t-disp" data-ak-heading id="h-overview">The system runs as a circuit, from wealth back to wealth.</h1>'
            f'<div class="sh-side">{deck}{spec}{links}</div></header>')
    key = (f'<div class="ckey t-legend" aria-hidden="true">'
           f'<span><svg width="44" height="12"><path d="M1 6 H30" stroke="currentColor" stroke-width="3"/><path d="M43 6 L30 0.5 L30 11.5 Z" fill="currentColor"/></svg>Main circuit</span>'
           f'<span><svg width="44" height="12"><path d="M1 6 H33" stroke="currentColor" stroke-width="2"/><path d="M43 6 L33 2 L33 10 Z" fill="currentColor"/></svg>Other flows between parts</span>'
           f'<span><b class="kn">5</b>Connections in the bundle</span>'
           f'<span><svg width="30" height="20"><path d="M15 1 V8 M15 12 V19" stroke="currentColor" stroke-width="2"/><path d="M1 10 H29" stroke="currentColor" stroke-width="2"/></svg>Lines cross without joining</span></div>')
    circ, skipped = circuit_compact()
    n_sk = sum(len(FLOW[k]) for k in skipped)
    words = flows_in_words()
    circuit = (f'<section class="circ" aria-labelledby="ov-circ-h"><div class="circ-top"><h2 class="t-eyebrow" id="ov-circ-h">01.1 The circuit at a glance</h2>{key}</div>'
               f'<div class="wide-only"><div class="ak-scroll circuit-wrap" id="ov-region" role="region" tabindex="0" aria-label="The circuit at a glance, drawing" style="--ak-min:{CW}px">{circ}</div>'
               f'<div class="circ-foot">{evidence_key(lead="Bundles are drawn solid. Each connection inside one carries its own grade")}'
               f'<p class="t-cap circ-note">{nw(len(skipped)).capitalize()} smaller bundles that skip a part, {n_sk} connections in all, sit in the <a href="#ov-flows" data-toc>flow table</a>.</p></div>'
               f'<p class="ak-readout t-cap" data-ak-readout>Point at, tab to or tap a part or a line to read its record.</p></div>'
               f'<div class="narrow-only">{mini_circuit()}<div class="ov-after">{spec}{links}</div>{evidence_key()}</div>'
               f'<details class="words" id="ov-words"><summary class="t-legend">Every flow between parts, in words ({len(words)} bundles)</summary><ol class="t-cap">{"".join(words)}</ol></details></section>')
    cards = plate('ov-cards', '01.2', 'Every part and every condition',
                  '<p>Each card lists every condition its part tracks, what it passes on along the circuit, and the loops based there. Select any name to read its record.</p>',
                  f'<div class="wide-only"><div class="ak-scroll" role="region" tabindex="0" aria-label="Every part and every condition, drawing" style="--ak-min:{CW}px">{overview_cards()}</div>'
                  f'<p class="ak-readout t-cap" data-ak-readout>Point at, tab to or tap a condition to read its record.</p></div>'
                  f'<div class="narrow-only">{overview_stack()}</div>')
    cards = cards.replace('id="ov-cards-h"', 'id="ov-cards-h"', 1)
    flows = plate('ov-flows', '01.3', 'Every flow between parts',
                  f'<p>All {CROSS} connections that cross from one part to another, counted by where they start and where they land.</p>',
                  f'<div class="wide-only">{flow_matrix()}</div><p class="narrow-only t-cap">On a phone, each card above lists its flows out and in. Select a number to list the connections.</p>')
    n_r = sum(1 for l in LOOPS.values() if l['type'] == 'R')
    n_b = sum(1 for l in LOOPS.values() if l['type'] == 'B')
    n_sk = sum(1 for l in LOOPS.values() if l['conceptual'])
    sk = plate('ov-sketch', '01.5', 'Where the loops sit',
               f'<p>Each card lists the loops based in its part. Of the {cnt("loops", COUNTS["loops"])} loops, {cnt("loops_reinforcing", n_r)} feed themselves and '
               f'{cnt("loops_balancing", n_b)} push back. {cnt("loops_sketched", n_sk)} of the {COUNTS["loops"]} are sketches with no complete numbered chain: '
               + ', '.join(f'<a href="{loop_href(k)}" data-loop="{k}" data-steps="sketch" data-name="{e(LOOPS[k]["plain_name"])}">{k}, {e(LOOPS[k]["plain_name"])}</a>' for k in D['loop_order'] if LOOPS[k]['conceptual'])
               + f'.</p><p><a class="btnlink" href="#loops">Open all 23 loops</a></p>', '')
    qs = plate('ov-questions', '01.4', 'Start from a question',
               f'<p>Pick the question closest to your own life. Each one opens a short answer and the part of the system it runs through. '
               f'There are {nw(len(D["hubs"]))} topics and {len(D["pathways"])} questions.</p>', questions_html())
    return (f'<section data-view-root="overview" data-crumb="Overview" aria-labelledby="h-overview">{head}{circuit}{cards}{flows}{qs}{sk}</section>')


# ------------------------------------------------------------------------------------------- panel records
def tpl(key, kind, title, body):
    return f'<template data-detail="{key}" data-kind="{e(kind)}" data-title="{e(title)}">{body}</template>'


def var_tpl(n):
    N = NODES[n]
    p = N['part']
    outs = [l for l in sorted(LINKS.values(), key=lambda l: l['id']) if l['from'] == n]
    ins = [l for l in sorted(LINKS.values(), key=lambda l: l['id']) if l['to'] == n]
    lp = N['loops']
    iss = issues_on([n])
    nxt = (f'<p class="pn-next"><a href="#area-c">Open the Elections sheet</a></p>' if p == 'C' else '')
    body = ((f'<p class="pn-lead">{e(N["title"])}</p>' if N['title'] != N['label'] else '') + f'<p>{e(N["description"])}</p>'
            f'<p class="pn-means"><b>{e(N["increase_means"])}</b></p>'
            + (f'<p>{e(N["why"])}</p>' if N.get('why') else '')
            + f'<dl><dt>Part</dt><dd>{e(part_name(p))} ({e(PARTS[p]["formal_title"])})</dd>'
            f'<dt>Kind</dt><dd>{e(N["kind_plain"])}</dd><dt>Measured by</dt><dd>{e(N["indicator"])}</dd>'
            f'<dt>Issues</dt><dd>{len(iss)} tracked here</dd></dl>'
            + (f'<h3>Pushes on ({len(outs)})</h3><ul class="lrows">' + ''.join(link_row(l['id'], show_from=False) for l in outs) + '</ul>' if outs else '')
            + (f'<h3>Pushed by ({len(ins)})</h3><ul class="lrows">' + ''.join(link_row(l['id'], show_to=False) for l in ins) + '</ul>' if ins else '')
            + (f'<h3>Loops through it</h3><p>' + ', '.join(f'<a href="{loop_href(k)}">{k} {e(LOOPS[k]["plain_name"])}</a>' for k in lp) + '</p>' if lp else '<h3>Loops through it</h3><p>None. It sits on no loop.</p>')
            + nxt + f'<p class="pn-src">Atlas V7, snapshot {SNAP}.</p>')
    return tpl(var_key(n), f'Variable {n}', N['label'], body)


def part_tpl(p):
    P_ = PARTS[p]
    out, inn = flows_of(p)
    lp = loops_home(p)
    q = f'<p class="pn-lead">{e(P_["plain_question"])}</p>' if P_['plain_question'] else ''
    body = (f'<p class="pn-lead">{e(P_["formal_title"])}</p>{q}<p>{e(P_["story"])}</p>'
            f'<dl><dt>Conditions</dt><dd>{len(P_["nodes"])}</dd><dt>Inside</dt><dd>{len(INSIDE.get(p, []))} connections</dd>'
            f'<dt>Flows out</dt><dd>' + ('; '.join(f'{len(ids)} to {e(part_name(q_))}' for q_, ids in out) or 'none') + '</dd>'
            f'<dt>Flows in</dt><dd>' + ('; '.join(f'{len(ids)} from {e(part_name(q_))}' for q_, ids in inn) or 'none') + '</dd></dl>'
            f'<h3>Conditions</h3><ul>' + ''.join(f'<li><span class="code">{n}</span> {e(node_label(n))}: {e(NODES[n]["increase_means"])}</li>' for n in P_['nodes']) + '</ul>'
            + (f'<h3>Loops based here</h3><p>' + ', '.join(f'<a href="{loop_href(k)}">{k} {e(LOOPS[k]["plain_name"])}</a>' for k in lp) + '</p>' if lp else '')
            + f'<p class="pn-src">Atlas V7, snapshot {SNAP}.</p>')
    return tpl(part_key(p), f'Part {p}', P_['plain_name'], body)


def flow_tpl(a, b):
    ids = FLOW[(a, b)]
    body = (f'<p class="pn-lead">{len(ids)} {plural(len(ids), "connection")} run from {e(part_name(a))} to {e(part_name(b))}. '
            f'Each one names the condition it starts from and the one it moves.</p><ul class="lrows">' + ''.join(link_row(k) for k in ids) + '</ul>'
            f'<p class="pn-src">{e(sign_rule())} Atlas V7, snapshot {SNAP}.</p>')
    return tpl(flow_key(a, b), 'Flow between parts', f'{part_name(a)} to {part_name(b)}', body)


def link_tpl(k):
    l = LINKS[k]
    s = l['polarity']
    lp = l['loops']
    body = (f'<p class="pn-lead">{e(l["plain"])}</p>'
            f'<dl><dt>From</dt><dd>{l["from"]} {e(node_label(l["from"]))}</dd><dt>To</dt><dd>{l["to"]} {e(node_label(l["to"]))}</dd>'
            f'<dt>Sign</dt><dd>{sign_svg(s) if s in ("+", "-") else ""} {e(verb(s))}: {e(l["sign_meaning"])}</dd>'
            f'<dt>Evidence</dt><dd>{tex_swatch(l["evidence"])} {grade_word(l["evidence"])}: {grade_gloss(l["evidence"])}</dd>'
            f'<dt>Delay</dt><dd>{delay_words(l["delay"])}</dd><dt>Kind</dt><dd>{e(l["type"])} connection</dd></dl>'
            f'<h3>How it works</h3><p>{e(l["mechanism"])}</p>'
            + (f'<h3>Keep in mind</h3><p>{e(l["qualification"])}</p>' if l.get('qualification') else '')
            + (f'<h3>Loops</h3><p>' + ', '.join(f'<a href="{loop_href(x)}">{x} {e(LOOPS[x]["plain_name"])}</a>' for x in lp) + '</p>' if lp else '<h3>Loops</h3><p>None. This connection sits on no loop.</p>')
            + f'<p class="pn-src">Atlas V7, snapshot {SNAP}.</p>')
    return tpl(link_key(k), f'Connection {k}', l['name'], f'<div {link_attrs(k)}>{body}</div>')


def reform_tpl(rid):
    r = REFORMS[rid]
    eff = ''.join(f'<dt>{e(D["families"][fam])}</dt><dd>{e(effect_words(code))}</dd>' for fam, code in r['effects'].items())
    tg = '; '.join(f'{t} {e(node_label(t) if t in NODES else LINKS[t]["name"])}' for t in r['targets'])
    body = (f'<p class="pn-lead">{e(sentences(r["summary"])[0])}</p>'
            + (f'<p><b>Disclosure.</b> {e(r["disclosure"])}</p>' if r.get('disclosure') else '')
            + f'<dl><dt>Aims at</dt><dd>{tg}</dd><dt>Problem</dt><dd>{grade_word(r["problem_evidence"]["grade"])}</dd>'
            f'<dt>Remedy</dt><dd>{grade_word(r["remedy_evidence"]["grade"])}</dd></dl>'
            f'<h3>Expected effects, never added together</h3><dl>{eff}</dl>'
            + ('<p class="pn-next"><a href="#reform-r01">Open the full reform</a></p>' if rid == 'R-01' else '')
            + f'<p class="pn-src">Atlas V7, snapshot {SNAP}.</p>')
    return tpl(f'reform-{rid.lower()}', f'Reform {rid}', r['title'], f'<div data-reform="{rid}" data-targets="{" ".join(r["targets"])}">{body}</div>')


def loop_tpl(k):
    L = LOOPS[k]
    steps = ''
    if not L['conceptual']:
        steps = '<h3>Steps</h3><ol class="lrows">' + ''.join(link_row(s['id']) for s in L['steps']) + '</ol>'
    else:
        steps = '<h3>Stations</h3><p>' + ', '.join(e(s['label']) for s in L['stations']) + '. No step is a numbered connection.</p>'
    cn = closure_note(k)
    rf = L['reforms']
    body = (f'<p class="pn-lead">{e(L["title"])}</p><p>{e(kind_words(k))}. {e(L["summary"])}</p>'
            f'<h3>Read it aloud</h3><p>{read_aloud_html(k)}</p>{steps}'
            f'<dl><dt>Weakest</dt><dd>{e(weakest_words(k))}</dd><dt>One turn</dt><dd>{e(L["delay_word"])}</dd>'
            f'<dt>Now</dt><dd>{e(DIRECTION_WORDS.get(L["direction"], L["direction"]))}</dd></dl>'
            + (f'<h3>Keep in mind</h3><p>{e(cn)}</p>' if cn else '')
            + (f'<p>{e(L["qualification"])}</p>' if L.get('qualification') else '')
            + f'<h3>Reforms aimed at it</h3><p>' + (', '.join(f'{r} {e(REFORMS[r]["title"])}' for r in rf) if rf else 'None in V7.') + '</p>'
            + f'<p class="pn-src">Atlas V7, snapshot {SNAP}.</p>')
    return tpl(loop_key(k), f'Loop {k}', L['plain_name'], body)


# ------------------------------------------------------------------------------------------- page
def kit_js():
    js = KIT_JS
    a = "const root = rootOf(S.view), item = key && $(`[data-select=\"${key}\"]`, root);"
    assert a in js
    js = js.replace(a, "const root = rootOf(S.view), mine = S.invoker && S.invoker.dataset && S.invoker.dataset.select === key && root && root.contains(S.invoker) && vis(S.invoker), item = key && (mine ? S.invoker : ($$(`[data-select=\"${key}\"]`, root).find(vis) || $(`[data-select=\"${key}\"]`, root)));   // System 3: the copy the reader picked, else the visible one")
    b = "const selected = () => S.sel && $(`[data-select=\"${S.sel}\"]`, rootOf(S.view));"
    assert b in js
    js = js.replace(b, "const selected = () => S.sel && ($$(`[data-select=\"${S.sel}\"]`, rootOf(S.view)).find(vis) || $(`[data-select=\"${S.sel}\"]`, rootOf(S.view)));")
    c = "if (sel && !reform && !busy) mark(sel, 'selected item');"
    assert c in js
    js = js.replace(c, "/* System 3: selection stays in ink; the one working red marks only where R-01 acts. */ void sel; void busy;")
    return js


CSS = r"""
:root{--ns:#DCD9D2;--ch:#121212;--red:#E63946;--pr:#1F2D5A;--st:#5D636D;--vd:#4A7C74;--wh:#FFFFFF;--ds:#4E535B;
--ak-w-lo:2px;--ak-w-hi:3px;--ak-w-sel:6px;--ak-focus:#121212;--ak-panel-w:420px;--m:64px}
html{background:var(--ns);color:var(--ch);-webkit-text-size-adjust:100%}
body{margin:0;font:400 17px/27px Inter,system-ui,sans-serif;background:var(--ns);color:var(--ch);font-feature-settings:"ss01" 0}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{text-decoration-thickness:2px}
p{margin:0}
.wrap{max-width:1312px;margin:0 auto;padding:0 var(--m)}
@media (max-width:1439.98px){:root{--m:clamp(20px,4.4vw,64px)}}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.muted{color:var(--ds);fill:var(--ds)}
.code{font:700 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums;color:var(--ds)}
/* type scale (design frame memo 2) */
.t-disp{font:800 56px/60px "Inter Tight",sans-serif;letter-spacing:-.035em;margin:0;text-wrap:balance;margin-left:-.04em}
.t-head{font:800 40px/44px "Inter Tight",sans-serif;letter-spacing:-.03em;margin:0;text-wrap:balance}
.t-deck{font:400 19px/28px Inter,sans-serif}
.t-phead{font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em;margin:0}
.t-eyebrow{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;margin:0}
.t-body{font:400 17px/27px Inter,sans-serif}
.t-ptext{font:400 15px/23px Inter,sans-serif}
.t-cap{font:400 14px/20px Inter,sans-serif}
.t-note{font:400 13px/16px Inter,sans-serif;letter-spacing:.01em}
.t-legend{font:500 13px/18px Inter,sans-serif}
.t-fig{font:800 40px/40px "Inter Tight",sans-serif;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.t-station{font:700 20px/22px "Inter Tight",sans-serif;letter-spacing:-.01em}
.t-quote{font:italic 400 22px/31px Lora,serif;letter-spacing:-.005em}
/* svg text */
.s-disp{font:800 56px "Inter Tight",sans-serif;letter-spacing:-1.96px}
.s-head{font:800 40px "Inter Tight",sans-serif;letter-spacing:-1.2px}
.s-phead{font:800 22px "Inter Tight",sans-serif;letter-spacing:-.44px}
.s-eyebrow{font:700 13px Inter,sans-serif;letter-spacing:.78px}
.s-ptext{font:400 15px Inter,sans-serif}
.s-station{font:700 20px "Inter Tight",sans-serif;letter-spacing:-.2px}
.s-map{font:600 15px Inter,sans-serif}
.s-note{font:400 13px Inter,sans-serif;letter-spacing:.13px}
.s-noteb{font:600 13px Inter,sans-serif;letter-spacing:.13px}
.s-cap{font:400 14px Inter,sans-serif}
.s-legend{font:500 13px Inter,sans-serif}
.s-code{font:700 13px Inter,sans-serif;font-variant-numeric:tabular-nums}
.s-count{font:800 22px "Inter Tight",sans-serif;letter-spacing:-.44px;font-variant-numeric:tabular-nums}
.s-fig{font:800 40px "Inter Tight",sans-serif;letter-spacing:-1.2px;font-variant-numeric:tabular-nums}
.s-q{font:600 15px Inter,sans-serif}
.s-deck{font:400 19px Inter,sans-serif}
svg text{fill:var(--ch)}
svg text.muted{fill:var(--ds)}
/* masthead */
.mast{border-bottom:1px solid var(--st)}
.mast .wrap{display:grid;grid-template-columns:auto 1fr auto;align-items:center;min-height:72px;gap:24px}
.wm{display:block;color:var(--ch);line-height:0}
.wm svg{display:block}
.wm .wm16{display:none}
.runhead{color:var(--ds)}
.sheets ol{display:flex;gap:4px;list-style:none;margin:0;padding:0}
.sheets a{display:flex;align-items:center;gap:6px;min-height:44px;padding:0 10px;font:600 15px/1 Inter,sans-serif;text-decoration:none;box-shadow:inset 0 -3px 0 transparent}
.sheets a .n{font:700 13px/1 Inter,sans-serif;color:var(--ds);font-variant-numeric:tabular-nums}
.sheets a:hover{text-decoration:underline}
.sheets a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ch)}
.crumbs{padding-top:16px}
.ak-crumbs ol{font:500 14px/20px Inter,sans-serif}
.ak-crumbs a{color:var(--ds)}
.ak-crumbs [aria-current]{color:var(--ch)}
/* sheet header */
.sheet-head{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;padding:24px 0 8px}
.sh-main{grid-column:1/span 8}
.sh-side{grid-column:10/span 3;display:flex;flex-direction:column;gap:20px;padding-top:4px}
.sh-no{display:flex;align-items:baseline;gap:14px;margin-bottom:12px}
.sh-no .t-fig{font-size:40px}
.sh-deck{margin-top:16px;max-width:62ch}
.sh-deck p+p{margin-top:12px}
.sh-read p+p{margin-top:8px}
.kp-link{display:inline-flex;flex-direction:column;gap:4px;text-decoration:none;color:var(--ds)}
.keyplan .kp,.keyplan .kp-open{fill:none;stroke:var(--st);stroke-width:1}
.keyplan .kp-on{fill:var(--ch);stroke:var(--ch);stroke-width:1}
.spec{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin:28px 0 0}
.sh-side .spec{grid-template-columns:1fr 1fr;gap:16px 20px;margin:0}
.spec div{border-top:1px solid var(--ch);padding-top:12px}
.spec dt,.spec dd{margin:0}
.spec dd.t-note{margin-top:6px;color:var(--ds)}
.toc ol{list-style:none;margin:8px 0 0;padding:0;font:500 14px/20px Inter,sans-serif}
.toc li{border-top:1px solid var(--st)}
.toc a{display:block;padding:6px 0;text-decoration:none}
.toc a:hover{text-decoration:underline}
/* plates */
.plate{border-top:1px solid var(--ch);padding:24px 0 48px;margin-top:40px}
.plate-head{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;margin-bottom:28px}
.plate-no{grid-column:1/span 12;margin-bottom:10px;color:var(--ds)}
.plate-head h2{grid-column:1/span 8}
.plate-dek{grid-column:1/span 8;margin-top:12px;max-width:62ch}
.plate-dek p+p{margin-top:10px}
.plate-foot{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--st);margin-top:28px;padding-top:8px;color:var(--ds)}
/* drawings */
.draw{display:block;overflow:visible}
.draw .card{fill:var(--wh);stroke:var(--ch);stroke-width:1}
.draw .frame-open{fill:none;stroke:var(--ch);stroke-width:1}
.draw .hair{stroke:var(--st);stroke-width:1;fill:none}
.draw .gap{fill:var(--ns)}
.draw .vhit{fill:transparent}
.draw .lchip-r{fill:none;stroke:var(--ch);stroke-width:1}
.draw .lchip:hover .lchip-r{stroke-width:2}
.draw .head{fill:var(--ak-hi,currentColor)}
.draw .diamond{fill:var(--ns);stroke:var(--ak-hi,currentColor)}
.draw .tick{stroke:var(--ak-hi,currentColor);fill:none}
.draw .hollow-core{stroke:var(--ns)}
.draw .sg-ring{fill:var(--ns);stroke:currentColor;stroke-width:2}
.draw .sg-bar{stroke:currentColor;stroke-width:2;fill:none}
.red-case{stroke:var(--ch);fill:none}
.red-mark{stroke:var(--red)}
.red-dot{fill:var(--red)}
.ak-dim [data-select]:not(.ak-rel):not([data-ak-sel]) .head{fill:var(--st)}
.flow{color:var(--ch)}
.flow .cnt{fill:var(--ch)}
.vrow:hover .ak-label,.pname:hover .ak-label,.porow:hover .ak-label{text-decoration:underline;text-underline-offset:3px}
.vrow.ak-rel .ak-label{text-decoration:underline;text-underline-offset:3px}
[data-ak-sel] .ak-label{font-weight:700}
.vrow[data-ak-sel] .vhit{fill:var(--ns)}
svg [data-select]:focus{outline:none}
svg [data-select]:focus-visible .vhit{stroke:var(--ch);stroke-width:2}
svg [data-select]:focus-visible{outline:2px solid var(--ch);outline-offset:2px}
svg a:focus-visible{outline:2px solid var(--ch);outline-offset:2px}
.circuit-wrap{margin-top:16px}
.ckey{display:flex;flex-wrap:wrap;gap:8px 28px;align-items:center;margin-top:28px;color:var(--ch)}
.ckey span{display:inline-flex;align-items:center;gap:8px}
.ckey .kn{font:800 22px/1 "Inter Tight",sans-serif}
.ak-readout{color:var(--ds);margin-top:12px}
.words{margin-top:20px;border-top:1px solid var(--st);padding-top:8px}
.words summary{cursor:pointer;min-height:32px;display:flex;align-items:center}
.words ol{margin:8px 0 0;padding-left:20px;columns:2;column-gap:48px}
.words li{break-inside:avoid;margin-bottom:6px}
.narrow-only{display:none}
/* questions */
.hubs{display:grid;grid-template-columns:repeat(5,1fr);gap:24px}
.hub{border-top:3px solid var(--ch);padding-top:12px}
.hub h3{margin:8px 0 12px;font-size:20px;line-height:24px}
.hub ol{list-style:none;margin:0;padding:0}
.hub li{border-top:1px solid var(--st);padding:10px 0;display:flex;flex-direction:column;gap:4px}
.qlink{font:600 15px/20px Inter,sans-serif;text-decoration:none}
.qlink:hover{text-decoration:underline}
.btnlink{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border:1px solid var(--ch);font:600 15px/1 Inter,sans-serif;text-decoration:none;background:var(--wh)}
.btnlink:hover{box-shadow:inset 0 0 0 1px var(--ch)}
a.tlink{display:inline-block;min-height:24px;padding:3px 0;box-sizing:border-box}
/* chips */
.chip{display:inline-flex;align-items:stretch;height:26px;vertical-align:middle;font:600 13px/1 Inter,sans-serif}
.chip-w{display:flex;align-items:center;padding:0 7px;background:var(--ch);color:var(--ns);letter-spacing:.06em;text-transform:uppercase}
.chip-k{display:flex;align-items:center;padding:0 8px;box-shadow:inset 0 0 0 1.5px var(--ch);font:700 14px/1 Inter,sans-serif;font-variant-numeric:tabular-nums}
.chip-c{height:22px}.chip-c .chip-k{font-size:13px}
/* the panel: a drawer on the right at 900 px and wider, a bottom sheet below (interaction memo 5) */
.ak-panel{background:var(--wh);color:var(--ch)}
.ak-panel .pn-lead{font:600 17px/25px Inter,sans-serif;margin-bottom:10px}
.ak-panel p{margin:0 0 10px}
.ak-panel h3{color:var(--ds)}
.ak-panel .lrows{list-style:none;padding:0}
.ak-panel .pn-src{color:var(--ds);font-size:13px;margin-top:20px;border-top:1px solid var(--st);padding-top:8px}
.ak-panel .pn-next a{font-weight:600}
.lrow{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px solid #DCD9D2}
.lrow .signsvg,.lrow .dia{flex:none;margin-top:2px}
.lrow .dia{width:14px;height:14px;border:2px solid var(--ch);transform:rotate(45deg) scale(.8);box-sizing:border-box;display:inline-block}
.lrow-t{display:block}.lrow-t .code{margin:0 4px}
.lrow-m{display:block;color:var(--ds);font-size:14px;line-height:20px;margin-top:2px}
.lrow-m .swatch{vertical-align:middle}
.signsvg .sg-ring{fill:var(--wh);stroke:var(--ch);stroke-width:2}
.signsvg .sg-bar{stroke:var(--ch);stroke-width:2}
.swatch{color:var(--ch)}
.ak-panel-bar .ak-btn{min-height:44px}
@media (min-width:900px){
 .ak-panel{position:fixed;top:0;right:0;bottom:0;width:var(--ak-panel-w);max-height:none;z-index:80;border-left:1px solid var(--ch);overflow:auto;padding:24px 28px 32px}
}
/* footer */
.foot{border-top:1px solid var(--st);margin-top:56px;padding:12px 0 40px}
.foot .wrap{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;color:var(--ds)}
.foot .src{grid-column:1/span 8}
.foot .who{grid-column:9/span 4;text-align:right}
/* phone and narrow screens */
@media (max-width:899.98px){
 .wide-only{display:none}
 .narrow-only{display:block}
 .mast .wrap{grid-template-columns:1fr;gap:12px;padding-top:20px;padding-bottom:0}
 .wm .wm24{display:none}.wm .wm16{display:block}
 .runhead{display:none}
 .sheets ol{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
 .sheets a{padding:0 4px;font-size:14px;justify-content:flex-start}
 .sheet-head{display:block;padding:20px 0 24px}
 .sh-side{margin-top:24px;gap:16px}
 .t-disp{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .t-head{font-size:30px;line-height:34px}
 .t-deck{font-size:17px;line-height:25px}
 .t-body{font-size:16px;line-height:25px}
 .t-quote{font-size:19px;line-height:27px}
 .t-fig{font-size:32px;line-height:32px}
 .spec{grid-template-columns:repeat(2,1fr);gap:16px}
 .plate-head{display:block}
 .hubs{grid-template-columns:1fr}
 .words ol{columns:1}
 .foot .wrap{display:block}.foot .who{text-align:left;margin-top:8px}
 .plate-foot{flex-direction:column;gap:2px}
}

/* loop drawings */
.draw .box{fill:var(--wh);stroke:var(--ch)}
.draw .box-open{fill:none;stroke:var(--ch)}
.draw .badge-ring{fill:none;stroke:var(--ch);stroke-width:2}
.draw .red-card{fill:var(--wh);stroke:var(--red)}
.draw .red-card-key{fill:none;stroke:var(--ch);stroke-width:1}
.bx.ak-now .ak-mark,.bx[data-ak-sel] .ak-mark{stroke-width:3px}
.st:hover .ak-label,.bx:hover .ak-label{text-decoration:underline;text-underline-offset:3px}
.cardlink:hover text{text-decoration:underline}
.readaloud{border-left:3px solid var(--ch);padding:4px 0 4px 18px;margin:0 0 24px;max-width:960px}
.ra-text{font:400 22px/31px Inter,sans-serif;margin-top:6px}
.ra-text b{font-weight:700}
.loop-id{margin-bottom:12px}
.loop-id b{font-weight:600}
.phone-chain{margin-top:16px}
.stepper{max-width:900px}
.st-btns{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.st-status{min-height:46px;max-width:70ch}
.st-list{margin:16px 0 0;padding:0 0 0 0;list-style:none;counter-reset:st}
.st-list li{counter-increment:st;border-top:1px solid var(--st);padding:10px 0 10px 40px;position:relative}
.st-list li::before{content:counter(st);position:absolute;left:12px;top:10px;font:800 15px/20px "Inter Tight",sans-serif}
.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 24px}
.nblock{border-top:1px solid var(--ch);padding-top:10px}
.nblock .t-ptext{margin-top:8px}
.nblock p+p{margin-top:8px}
.rcards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.rcard{background:var(--wh);border:1px solid var(--ch);padding:16px 18px 18px}
.rcard h3{margin:10px 0 8px}
.rcard p+p{margin-top:8px}
@media (max-width:899.98px){.notes,.rcards{grid-template-columns:1fr}.ra-text{font-size:19px;line-height:27px}}


/* Elections */
.sub{margin-bottom:14px}
.spec5{grid-template-columns:repeat(5,1fr)}
.vcards{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
.vcard{background:var(--wh);border:1px solid var(--ch);box-shadow:inset 6px 0 0 var(--pr);padding:14px 14px 16px 22px;display:flex;flex-direction:column;gap:8px}
.vc-top{display:flex;justify-content:space-between;align-items:flex-start}
.vcard h3{margin:4px 0 0}
.vc-name{all:unset;cursor:pointer}
.vc-name:focus-visible{outline:2px solid var(--ch);outline-offset:2px}
.vc-name:hover .ak-label{text-decoration:underline;text-underline-offset:3px}
.vc-facts{margin:4px 0 0;border-top:1px solid var(--st);padding-top:8px;display:grid;gap:6px}
.vc-facts dt{color:var(--ds);font-weight:600}.vc-facts dd{margin:0}
.cwords{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:12px}
.cwords h3{font-size:17px;line-height:22px;margin-bottom:6px}
ul.plain{list-style:none;margin:0;padding:0}
.cwords .grp>p{margin-top:12px}
.cwords .lrows{list-style:none;margin:0;padding:0}
.cwords .lrow{border-top:1px solid var(--st);font-size:14px;line-height:20px}
.cw-wrap{margin-top:24px}
.lcards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.lcard{background:var(--wh);border:1px solid var(--ch);padding:16px 16px 18px;display:flex;flex-direction:column;gap:10px;min-width:0}
.lc-top{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.lc-name{all:unset;cursor:pointer}
a.lc-name{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
.lc-name:hover{text-decoration:underline;text-underline-offset:4px}
.lc-name:focus-visible{outline:2px solid var(--ch);outline-offset:2px}
.lc-title{color:var(--ds)}
.lc-draw{margin:6px 0 2px}
.lc-draw svg{max-width:100%;height:auto}
.lc-draw .gap,.lcard .draw .sg-ring{fill:var(--wh)}
.draw .hollow-core{fill:none}
.lcard .draw .hollow-core{stroke:var(--wh)}
.lcard .draw .sg-ring{fill:var(--wh)}
.lc-ra .t-eyebrow{display:block;margin-bottom:2px}
.lc-facts{display:grid;grid-template-columns:repeat(2,1fr);gap:8px 16px;margin:0;border-top:1px solid var(--st);padding-top:10px}
.lc-facts dt{color:var(--ds);font-weight:600}.lc-facts dd{margin:0}
.lc-note{border-left:3px solid var(--ch);padding-left:10px}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:16px}
.filters .ak-btn[aria-pressed="true"]{background:var(--ch);color:var(--ns);box-shadow:none}
.ihead,.issue summary{display:grid;grid-template-columns:64px minmax(0,4fr) 140px 150px minmax(0,3fr);gap:16px;align-items:baseline}
.ihead{color:var(--ds);font-weight:600;border-bottom:1px solid var(--ch);padding:0 0 6px 28px}
.issues{list-style:none;margin:0;padding:0}
.issues>li{border-bottom:1px solid var(--st)}
.issue summary{cursor:pointer;padding:10px 0 10px 28px;list-style:none;position:relative;min-height:44px;box-sizing:border-box}
.issue summary::-webkit-details-marker{display:none}
.issue summary::before{content:"+";position:absolute;left:4px;top:8px;font:700 17px/24px Inter,sans-serif}
.issue[open] summary::before{content:"\2212"}
.i-title{font:600 15px/20px Inter,sans-serif}
.issue summary:hover .i-title{text-decoration:underline;text-underline-offset:3px}
.i-body{padding:4px 0 20px 108px;max-width:1100px}
.i-body>p{margin-bottom:12px}
.ixs{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:8px 0 16px}
.ix{background:var(--wh);border:1px solid var(--st);padding:12px 14px}
.ix p+p{margin-top:6px}
.i-body dl{display:grid;gap:8px;margin:0}
.i-body dt{font-weight:600}.i-body dd{margin:0}
.effects{list-style:none;margin:6px 0 0;padding:0}
.effects li{display:flex;justify-content:space-between;gap:12px;border-top:1px solid #DCD9D2;padding:5px 0}
.rc-t{margin-top:10px}.rc-t .t-eyebrow{display:block;margin-bottom:2px}
.rc-e{margin-top:12px}
.rc-disc{margin-top:12px;border-left:3px solid var(--ch);padding-left:10px}
.rc-more{margin-top:10px}.rc-more summary{cursor:pointer;min-height:32px;display:flex;align-items:center}
@media (max-width:1439.98px){.vcards{grid-template-columns:repeat(3,1fr)}.lcards{grid-template-columns:repeat(2,1fr)}}
@media (max-width:899.98px){
 .spec5{grid-template-columns:repeat(2,1fr)}
 .vcards,.lcards,.cwords,.ixs{grid-template-columns:1fr}
 .ihead{display:none}
 .issue summary{grid-template-columns:1fr;gap:4px;padding-left:28px}
 .i-body{padding-left:0}
 .lcard{padding:14px 0 16px;border-left:0;border-right:0}
}


/* reform */
.h-icon{display:inline-block;vertical-align:middle;margin-right:12px}
.h-icon svg{width:48px;height:48px;display:block}
.ev2{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}
.hd-disc{margin-top:12px;border-left:3px solid var(--ch);padding-left:12px}
.ev2 .ixs{grid-template-columns:1fr;margin:0}
.evb{background:var(--wh);border:1px solid var(--ch);padding:16px 18px}
.evb .evg{margin:8px 0 10px}.evb .evg .swatch{vertical-align:middle;margin-right:6px}
.notes.n2{grid-template-columns:repeat(3,1fr)}
.nblock ul{margin:0;padding-left:18px}
.effgrid{max-width:960px}
.ef-head,.eff li{display:grid;grid-template-columns:260px 170px 1fr;gap:24px;align-items:center}
.ef-head{color:var(--ds);font-weight:600;border-bottom:1px solid var(--ch);padding-bottom:6px}
.scale-head{display:flex;gap:0}.scale-head span{width:26px;text-align:center}
.eff{list-style:none;margin:0 0 12px;padding:0}
.eff li{border-bottom:1px solid var(--st);padding:12px 0;font:400 15px/20px Inter,sans-serif}
.ef-w{font-weight:600}
.scale .sc-on{fill:var(--ch);stroke:var(--ch);stroke-width:1}
.scale .sc-off{fill:none;stroke:var(--st);stroke-width:1}
.routes{width:100%;border-collapse:collapse;margin-bottom:28px}
.routes th,.routes td{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-bottom:1px solid var(--st)}
.routes thead th{font:600 13px/18px Inter,sans-serif;color:var(--ds);border-bottom:1px solid var(--ch)}
.routes tbody th{font-weight:600;width:18%}
.routes .fz b{margin:0 0 0 6px}.routes .fz .t-note{display:block;margin-top:4px}
.status{max-width:900px}
.status .t-body{margin:8px 0 10px}
.disclose{border:1px solid var(--ch);background:var(--wh);padding:16px 20px;margin-top:20px}
.disclose .t-body{margin-top:6px}
.r01-note{margin-top:10px}
@media (max-width:899.98px){.ev2,.notes.n2{grid-template-columns:1fr}.ef-head{display:none}.eff li{grid-template-columns:1fr;gap:6px}
 .routes,.routes tbody,.routes tr,.routes th,.routes td{display:block;width:auto}.routes thead{display:none}.routes tr{border-bottom:1px solid var(--ch);padding:8px 0}.routes th,.routes td{border:0;padding:4px 0}}


/* catalog and conventions */
.lgroup{border-top:1px solid var(--ch);margin-top:40px;padding-top:20px}
.lg-head{margin-bottom:24px;max-width:900px}
.lg-head h2{margin:8px 0 8px}
.lindex{margin-top:28px}
.lidx{display:grid;grid-template-columns:repeat(5,1fr);gap:12px 24px;margin-top:10px}
.lidx-g>p{border-bottom:1px solid var(--ch);padding-bottom:4px}
.lidx li{border-bottom:1px solid var(--st)}
.lidx ol{list-style:none;margin:4px 0 0;padding:0;font:500 13px/18px Inter,sans-serif}
.lidx a{display:block;padding:3px 0;text-decoration:none}.lidx a:hover{text-decoration:underline}
.lidx .code{display:inline-block;min-width:30px}
.t-quote{display:inline}
.convs{list-style:none;margin:0;padding:0}
.conv{display:grid;grid-template-columns:180px 1fr;gap:24px;align-items:start;border-top:1px solid var(--st);padding:14px 0}
.cv-mark{padding-top:2px}
.cv-t .t-ptext{margin-top:4px}.cv-t .t-cap{margin-top:4px}
.conv-wide{display:flex;gap:28px;align-items:center;flex-wrap:wrap}
.lcard.untested{background:transparent;border:1px solid var(--ch)}
.unt-h{font-size:30px;line-height:34px;margin:6px 0 8px}
.layers{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.layer{background:var(--wh);border:1px solid var(--ch);box-shadow:inset 6px 0 0 var(--pr);padding:14px 14px 16px 22px}
.layer.lay-economy{box-shadow:inset 6px 0 0 var(--vd)}.layer.lay-technology{box-shadow:inset 6px 0 0 var(--st)}
.layer.lay-open{background:transparent;box-shadow:none}
.layer .t-cap{margin-top:8px}
.draw .leader{stroke:var(--st);stroke-width:1;fill:none}
.anat-wrap{overflow-x:auto}
.anat-phone{display:none}
.anat-list{margin:16px 0 0;padding-left:22px}.anat-list li{padding:3px 0}
@media (max-width:899.98px){.anat-phone{display:block}}
.gloss{display:grid;grid-template-columns:repeat(3,1fr);gap:16px 24px;margin:0}
.gloss div{border-top:1px solid var(--st);padding-top:8px}
.gloss dt{font-weight:600}.gloss dd{margin:4px 0 0}
@media (max-width:899.98px){.conv{grid-template-columns:1fr;gap:6px}.layers,.gloss,.lidx{grid-template-columns:1fr}.lcard.untested{border-left:0;border-right:0}}


/* ---------------- fix pass, November 5 ---------------- */
h1,h2,h3{text-wrap:balance}
.h1-sub{margin-top:2px}
.ak-btn{font:600 15px/1.2 Inter,sans-serif}
.skip{position:absolute;left:8px;top:-80px;z-index:200;background:var(--ch);color:var(--ns);padding:12px 16px;font:600 15px/1 Inter,sans-serif;text-decoration:none}
.skip:focus{top:8px;outline:2px solid var(--ch);outline-offset:2px}
.status{margin:6px 0 0;padding-left:10px;border-left:3px solid var(--ch)}
.status:empty{display:none}
/* the panel as a column the layout makes room for (fix 8) */
@media (min-width:900px){
 html.ak-sheet body{padding-right:var(--ak-panel-w)}
}
/* the sticky plate bar */
.platebar{position:sticky;top:0;z-index:30;background:var(--ns);border-bottom:1px solid var(--st);display:flex;align-items:flex-start;gap:20px;margin-top:12px}
.platebar>.t-eyebrow{flex:none;color:var(--ds);line-height:44px}
.platebar ol{display:flex;flex-wrap:wrap;gap:0 18px;margin:0;padding:0;list-style:none;font:500 14px/20px Inter,sans-serif}
.platebar li{border:0}
.platebar a{display:flex;align-items:center;min-height:44px;text-decoration:none}
.platebar a:hover{text-decoration:underline}
.platebar .tn{color:var(--ds);margin-right:6px;font-variant-numeric:tabular-nums}
.platebar + .plate{border-top:0;margin-top:8px}
/* the evidence key */
.evkey .t-eyebrow{margin-bottom:8px}
.evkey ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 18px}
.evkey li{display:flex;align-items:center;gap:8px}
.sh-side .evkey ul{flex-direction:column;gap:6px}
/* the overview head */
.sh-side .t-ptext + .spec{margin-top:16px}
.spec-s{grid-template-columns:repeat(4,auto);gap:12px 18px}
.spec-s div{padding-top:6px}
.t-figs{font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.spec-s dd.t-note{margin-top:2px}
.sh-links{margin-top:14px}
/* 01.1 the circuit */
.circ{margin-top:20px}
.circ-top{display:flex;align-items:center;justify-content:space-between;gap:12px 24px;flex-wrap:wrap;margin-bottom:12px}
.circ-top .ckey{margin-top:0}
.circ-top h2{color:var(--ds)}
.circ-foot{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-top:14px}
.circ-note{max-width:34ch;text-align:right}
.cards{margin-top:4px}
/* 01.3 the flow table */
.mx-wrap{overflow-x:auto}
.mx{border-collapse:collapse;width:100%;background:var(--wh);font-variant-numeric:tabular-nums}
.mx{table-layout:fixed}
.mx thead th:first-child{width:220px}
.mx thead th:last-child{width:64px}
.mx caption{caption-side:top;text-align:left;margin-bottom:12px;max-width:80ch}
.mx th,.mx td{border:1px solid var(--st);padding:0;text-align:center;vertical-align:middle}
.mx thead th{font:600 14px/18px Inter,sans-serif;padding:8px 6px;background:var(--ns);border-color:var(--ch)}
.mx tbody th{text-align:left;padding:6px 12px;background:var(--ns);border-color:var(--ch);white-space:nowrap}
.mx-n{display:block;font:600 15px/20px Inter,sans-serif}
.mx-f{display:block;font:400 13px/16px Inter,sans-serif;color:var(--ds)}
.mx-corner{font:500 13px/16px Inter,sans-serif!important;color:var(--ds)}
.mx-b{all:unset;box-sizing:border-box;display:flex;align-items:center;justify-content:center;width:100%;min-height:48px;cursor:pointer;font:800 22px/1 "Inter Tight",sans-serif}
.mx-b:hover{text-decoration:underline;text-underline-offset:4px}
.mx-b:focus-visible{outline:2px solid var(--ch);outline-offset:-5px}
.mx-b[data-ak-sel]{background:var(--ch);color:var(--wh)}
td.mx-main{box-shadow:inset 0 0 0 3px var(--ch)}
td.mx-in{background:var(--ns);color:var(--ds);font:600 15px/1 Inter,sans-serif}
td.mx-0{color:var(--ds)}
td.mx-t,.mx-tr th{font:600 15px/1 Inter,sans-serif;background:var(--ns)}
/* the phone's mini circuit */
.mini{list-style:none;margin:20px 0 0;padding:0}
.mc-i{background:var(--wh);border:1px solid var(--ch);box-shadow:inset 6px 0 0 var(--pr);padding:12px 14px 12px 22px}
.mc-i.lay-economy{box-shadow:inset 6px 0 0 var(--vd)}.mc-i.lay-technology{box-shadow:inset 6px 0 0 var(--st)}
.mc-i.open-frame{background:transparent;box-shadow:none}
.mc-n a,.mc-b{all:unset;cursor:pointer;display:inline-flex;align-items:center;min-height:32px;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
.mc-b:focus-visible,.mc-n a:focus-visible{outline:2px solid var(--ch);outline-offset:2px}
.mc-q{font:600 15px/20px Inter,sans-serif;margin-top:2px}
.mc-n .t-phead{margin-right:6px}
.mc-c{display:flex;align-items:center;gap:10px;margin:0 0 0 22px;padding:8px 0 8px 16px;border-left:3px solid var(--ch);font:600 14px/20px Inter,sans-serif}
.mc-cn{font:800 22px/1 "Inter Tight",sans-serif}
.mc-c.ret{border-left-color:var(--ch);margin-bottom:8px}
.narrow-only .evkey{margin-top:20px}
/* 01.4 questions */
.hubs{display:block}
.hub{display:grid;grid-template-columns:3fr 9fr;gap:24px;border-top:3px solid var(--ch);padding:14px 0 22px}
.hub h3{margin:8px 0 0;font-size:22px;line-height:26px}
.hub ol{list-style:none;margin:0;padding:0}
.hub ol li{border:0;padding:0;display:block}
.hub ol li:last-child .qd{border-bottom:1px solid var(--st)}
.qd summary{cursor:pointer;list-style:none;display:flex;flex-direction:column;gap:2px;padding:10px 0 10px 26px;position:relative;border-top:1px solid var(--st);min-height:44px;box-sizing:border-box}
.qd summary::-webkit-details-marker{display:none}
.qd summary::before{content:"+";position:absolute;left:4px;top:8px;font:700 17px/24px Inter,sans-serif}
.qd[open] summary::before{content:"\2212"}
.qd summary:hover .qlink{text-decoration:underline;text-underline-offset:3px}
.qa{padding:0 0 16px 26px;max-width:72ch}
.qa p+p{margin-top:8px}
/* the loop sheet */
.p-first{border-top:0;margin-top:8px;padding-top:12px}
.p-eb{color:var(--ds);margin-bottom:10px}
.r10-grid{display:grid;grid-template-columns:minmax(0,940px) minmax(280px,1fr);gap:28px;align-items:start}
.r10-side{border-left:1px solid var(--st);padding-left:24px}
.r10-side .how{margin:16px 0 0;border-top:1px solid var(--st);padding-top:12px}
.r10-side .stepper{margin-top:8px}
.r10-side .st-list li{padding:8px 0 8px 32px}
.r10-side .st-list li::before{left:6px;top:8px}
.loop-keys{display:flex;flex-direction:column;gap:14px;margin-top:16px}
.loop-keys .ckey{margin-top:0}
.facts{display:grid;gap:0;margin:0}
.facts div{display:grid;grid-template-columns:140px 1fr;gap:12px;border-top:1px solid var(--st);padding:6px 0}
.facts dt{font-weight:600}.facts dd{margin:0}
.r01c{background:var(--wh);border:1px solid var(--ch);padding:16px 18px 18px}
.r01c h3{margin:8px 0}
.r01c p+p{margin-top:8px}
.stand{background:var(--wh);border:2px solid var(--ch);padding:14px 16px}
.stand p+p{margin-top:8px}
.draw .red-key{stroke:var(--ch);fill:none}
.draw .red-head{fill:var(--red);stroke:var(--ch)}
.draw .red-mark{stroke:var(--red)}
.draw.chain{max-width:100%;height:auto}
/* catalog cards */
.lc-sum{margin-top:2px}
.lc-q{border-left:3px solid var(--ch);padding-left:10px}
/* Elections */
.drawtoggle{margin-top:24px}
.drawtoggle>summary{list-style:none;cursor:pointer;display:inline-flex}
.drawtoggle>summary::-webkit-details-marker{display:none}
.drawtoggle[open]>summary{margin-bottom:16px}
.ar{list-style:none;margin:0;padding:0}
.ar li+li{margin-top:6px}
.ar-d{display:block;margin-top:2px}
.fcode{font-weight:500}
.vbtn .vcode,.sc-pass .vcode{margin-left:auto;font:500 13px/20px Inter,sans-serif;color:var(--ds)}
.sc-pass .vcode{margin-left:4px}
.lpill{display:inline-flex;align-items:center;justify-content:center;min-width:44px;min-height:44px;padding:0 8px;margin:6px 6px 0 0;border:1px solid var(--ch);box-sizing:border-box;font:700 13px/1 Inter,sans-serif;text-decoration:none;background:var(--wh)}
.lpill:hover{box-shadow:inset 0 0 0 1px var(--ch)}
.sc-loops{margin-top:12px}
.draw .card,.draw .accent{pointer-events:none}
@media (max-width:1199.98px){.r10-grid{grid-template-columns:1fr}.r10-side{border-left:0;padding-left:0}}
@media (max-width:899.98px){
 .platebar{position:static;display:block;border-bottom:0;margin-top:16px}
 .platebar>.t-eyebrow{margin-bottom:4px}
 .platebar ol{display:flex;flex-wrap:wrap;gap:0 18px}
 .platebar li{border:0}
 .hub{grid-template-columns:1fr;gap:6px}
 .circ-foot{display:block}
 .spec-s{grid-template-columns:repeat(2,1fr)}
 .r10-grid{display:block}
 .r10-side{margin-top:20px}
 .facts div{grid-template-columns:110px 1fr}
}
@media (max-width:899.98px){.circ-top .ckey{display:none}.mc-i{padding:10px 14px 10px 22px}.mc-c{padding:6px 0 6px 16px}.mc-q{margin-top:2px}.circ{margin-top:12px}}
@media (max-width:389.98px){.sheets a .n{display:none}.sheets a{white-space:nowrap}}
@media (max-width:359.98px){:root{--m:10px}}


.sh-ov{grid-template-rows:auto auto}
.sh-ov .sh-no{grid-column:1/-1}
.sh-ov h1{grid-column:1/span 8;align-self:start}
.sh-ov .sh-side{grid-column:9/span 4;gap:10px;padding-top:6px}
.sh-ov .counts b{font-weight:700}
.sh-ov .sh-links{margin-top:0}
@media (max-width:899.98px){.sh-ov .sh-side{margin-top:16px}.sh-ov .counts,.sh-ov .sh-links{display:none}.ov-after{margin-top:18px}.ov-after .sh-links{margin-top:8px}}

/* the phone stack of the overview */
.stack{list-style:none;margin:24px 0 0;padding:0}
.scard{background:var(--wh);border:1px solid var(--ch);box-shadow:inset 6px 0 0 var(--pr);padding:16px 16px 16px 22px}
.scard.lay-economy{box-shadow:inset 6px 0 0 var(--vd)}
.scard.lay-technology{box-shadow:inset 6px 0 0 var(--st)}
.scard.open-frame{background:transparent;box-shadow:none}
.scard + .scard{margin-top:16px}
.sc-head .t-legend{margin-top:2px}
.sc-q{font:600 15px/20px Inter,sans-serif;margin-top:10px}
.sc-head .t-cap{margin-top:6px}
.sc-vars{list-style:none;margin:12px 0 0;padding:0;border-top:1px solid var(--st)}
.vbtn,.fbtn{all:unset;box-sizing:border-box;display:flex;gap:10px;align-items:baseline;width:100%;min-height:44px;padding:11px 0;cursor:pointer;font:400 15px/20px Inter,sans-serif;border-bottom:1px solid #DCD9D2}
.vbtn .code{min-width:34px}
.vbtn:focus-visible,.fbtn:focus-visible{outline:2px solid var(--ch);outline-offset:2px}
.vbtn[data-ak-sel] .ak-label,.fbtn[data-ak-sel]{font-weight:700}
.sc-pass{margin-top:12px;font:400 14px/20px Inter,sans-serif}
.sc-pass .t-eyebrow{display:block;margin-bottom:2px}
.sc-flows{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:14px}
.sc-flows ul{list-style:none;margin:4px 0 0;padding:0}
.fbtn{min-height:44px;padding:10px 0;font-size:14px}
.fbtn .fnum{font:800 17px/20px "Inter Tight",sans-serif;min-width:20px}
.fbtn.main .fnum{font-size:22px}
.sc-loops{margin-top:10px}
.sc-loops a{display:inline-block;min-height:24px;padding:4px 2px}
.sc-open{margin-top:12px}
.sconn{list-style:none;display:flex;align-items:center;gap:10px;margin:0 0 0 22px;padding:14px 0 14px 18px;border-left:3px solid var(--ch);font:600 14px/20px Inter,sans-serif}
.sconn-n{font:800 22px/1 "Inter Tight",sans-serif}
.sconn.ret{border-left-style:solid;margin-top:16px;margin-bottom:16px}
"""


PAGE_JS = r"""
(function(){
  // Hash aliases (fix 10; red team S4): #reform-r-01 is the memo's spelling of the reform sheet.
  var h = location.hash;
  if (/^#reform-r-01(\/|$)/i.test(h)) history.replaceState(null, '', '#reform-r01' + h.replace(/^#reform-r-01/i, ''));
})();
"""

PAGE_JS_AFTER = r"""
(function(){
  var $$ = function(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function cur(){ var v=(AtlasKit.state().view||'overview');
    $$('.sheets a').forEach(function(a){ if(a.getAttribute('href')==='#'+v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); }); }
  addEventListener('hashchange',function(){ setTimeout(cur, 0); }); cur();
  // In-page jumps keep the view's hash, so a reload stays on the sheet.
  document.addEventListener('click',function(ev){
    var a=ev.target.closest&&ev.target.closest('a[data-toc]'); if(!a) return;
    var t=document.getElementById(a.getAttribute('href').slice(1)); if(!t) return;
    ev.preventDefault(); var d=t.closest('details'); if(d) d.open=true;
    t.scrollIntoView({block:'start'}); var h=t.querySelector('h2')||t; h.setAttribute('tabindex','-1'); h.focus({preventScroll:true});
  });
  // Skip link: focus the current view's heading and keep the view's hash (fix 10).
  var skip=document.querySelector('.skip');
  if(skip) skip.addEventListener('click',function(ev){ ev.preventDefault(); var v=AtlasKit.state().view;
    var h=document.querySelector('[data-view-root="'+v+'"] [data-ak-heading]'); if(h){ h.setAttribute('tabindex','-1'); h.focus(); } });
  // Issue filters.
  $$('[data-filter-group]').forEach(function(g){
    var list=document.getElementById(g.getAttribute('data-filter-group'));
    g.addEventListener('click',function(ev){ var b=ev.target.closest('button[data-filter]'); if(!b) return;
      $$('button[data-filter]', g).forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});
      var k=b.getAttribute('data-filter'), n=0;
      $$('[data-vars]', list).forEach(function(r){ var on=k==='all'||r.getAttribute('data-vars').split(' ').indexOf(k)>=0; r.hidden=!on; if(on) n++; });
      var out=document.getElementById(g.getAttribute('data-filter-group')+'-n'); if(out) out.textContent=n;
    });
  });
  // Arrow keys explained when a drawing takes focus (fix 10; red team X2).
  var HINT='Arrow keys move between items. Enter opens one.';
  document.addEventListener('focusin',function(ev){
    var d=ev.target.closest&&ev.target.closest('[data-ak-roving]'); if(!d) return;
    if(ev.relatedTarget && d.contains(ev.relatedTarget)) return;
    var root=d.closest('[data-view-root]'); if(!root) return;
    $$('[data-ak-readout]', root).forEach(function(ro){ if(ro.textContent.indexOf(HINT)!==0) ro.textContent = HINT + ' ' + ro.textContent; });
  });
  // The panel never hides the pick (fix 8): a column on desktop, and on a phone the item scrolls above the sheet.
  var panel=document.querySelector('[data-ak-panel]');
  function reveal(){
    if(!panel || panel.hidden) return;
    var root=document.querySelector('[data-view-root="'+AtlasKit.state().view+'"]'); if(!root) return;
    var it=$$('[data-ak-sel]', root).filter(function(x){ return x.getClientRects().length; })[0]; if(!it) return;
    var wide=matchMedia('(min-width: 900px)').matches;
    var reg=it.closest('.ak-scroll');
    if(reg){ var r=it.getBoundingClientRect(), rr=reg.getBoundingClientRect();
      if(r.right>rr.right-8 || r.left<rr.left+8) reg.scrollLeft += (r.left+r.width/2) - (rr.left+rr.width/2); }
    var r2=it.getBoundingClientRect(), band=wide ? innerHeight : innerHeight*0.52;
    if(r2.top<8 || r2.bottom>band-12){ var target=wide ? innerHeight*0.35 : band*0.4; scrollBy({top:(r2.top+r2.height/2)-target, behavior:'instant'}); }
  }
  if(panel) new MutationObserver(function(){ requestAnimationFrame(reveal); }).observe(panel,{attributes:true,attributeFilter:['hidden']});
  document.addEventListener('click',function(ev){ if(ev.target.closest&&ev.target.closest('[data-select]')) requestAnimationFrame(function(){ requestAnimationFrame(reveal); }); });
})();
"""


def wordmark(svg, cls):
    svg = re.sub(r'<title>.*?</title>', '', svg, flags=re.S)
    vb = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', svg)
    return svg.replace('<svg ', f'<svg class="{cls}" width="{vb.group(1)}" height="{vb.group(2)}" aria-hidden="true" focusable="false" ', 1)


def page(views_html, templates):
    nav = ''.join(f'<li><a href="#{v}"><span class="n">{n}</span>{e(t)}</a></li>' for v, n, t, *_ in SHEETS)
    meta_views = 'overview area-c loop-r10 reform-r01 loops how-to-read'
    src = (f'Who Do They Answer To? Systems Atlas V7, snapshot {SNAP}. {cnt("variables", COUNTS["variables"])} variables, '
           f'{cnt("connections", COUNTS["connections"])} connections, {cnt("loops", COUNTS["loops"])} loops, {cnt("reforms", COUNTS["reforms"])} reforms.')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="atlas-views" content="{meta_views}">
<title>Reference Sheets | Who Do They Answer To? | Oath &amp; Action</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&amp;family=Inter:wght@400;500;600;700&amp;family=Lora:ital@1&amp;display=swap">
<style>{KIT_CSS}
{CSS}</style>
</head>
<body>
<a class="skip" href="#main-sheet">Skip to the sheet</a>
<header class="mast"><div class="wrap">
<a class="wm" href="#overview" aria-label="Oath &amp; Action. The whole system, sheet 01."><span data-red="signature">{wordmark(WM24, 'wm24')}{wordmark(WM16, 'wm16')}</span></a>
<p class="runhead t-eyebrow">Reference sheets</p>
<nav class="sheets" aria-label="Sheets"><ol>{nav}</ol></nav>
</div></header>
<div class="wrap crumbs"><nav class="ak-crumbs" aria-label="Breadcrumb" data-ak-crumbs></nav><p class="status t-cap" role="status" data-ak-status></p></div>
<main class="wrap ak-stage" id="main-sheet">
{views_html}
</main>
<aside class="ak-panel" data-ak-panel hidden aria-labelledby="panel-title">
<div class="ak-panel-bar"><p data-ak-panel-kind></p><button type="button" class="ak-btn" data-ak-sheet-toggle aria-expanded="false">More</button><button type="button" class="ak-btn" data-ak-close>Close</button></div>
<h2 id="panel-title" data-ak-panel-title tabindex="-1"></h2>
<div data-ak-panel-body></div>
</aside>
<footer class="foot"><div class="wrap"><p class="src t-note">{src}</p><p class="who t-note">Editorial system 03, Reference sheets. Headlines are studio drafts.</p></div></footer>
{''.join(templates)}
<script>{PAGE_JS}</script>
<script>{kit_js()}</script>
<script>AtlasKit.init();</script>
<script>{PAGE_JS_AFTER}</script>
</body>
</html>
"""


def stub(view, crumb, parent, title):
    return (f'<section data-view-root="{view}" data-crumb="{crumb}" data-parent="{parent}" aria-labelledby="h-{view}">'
            + sheet_head(view, 'Draft', e(title), '<p>In progress.</p>') + '</section>')


def build():
    views = [overview_view()]
    for v, n, t, crumb, parent in SHEETS:
        if v == 'overview':
            continue
        fn = globals().get('view_' + v.replace('-', '_'))
        views.append(fn() if fn else stub(v, crumb, parent, t))
    templates = ([var_tpl(n) for n in NODES] + [part_tpl(p) for p in PARTS] + [flow_tpl(a, b) for (a, b) in FLOW]
                 + [link_tpl(k) for k in sorted(LINKS)] + [loop_tpl(k) for k in D['loop_order']] + [reform_tpl('R-01')])
    return page('\n'.join(views), templates)


def main():
    for i in range(12):
        out = build()
        if not measure_pending():
            break
        print('measured new text, rebuilding')
    OUT.write_text(out)
    print('wrote', OUT.relative_to(ROOT), f'{len(out) / 1e3:.0f} kB')



# ------------------------------------------------------------------------------------------- loop drawings
def loop_stations(k):
    """Stations in order: (code or None, label, part or None)."""
    L = LOOPS[k]
    if L['conceptual']:
        return [(s['code'], NODES[s['code']]['label'] if s['code'] else s['label'], s.get('area')) for s in L['stations']]
    return [(s['from'], node_label(s['from']), PART_OF[s['from']]) for s in L['steps']]


def step_list(k):
    """Steps in order: dict(id, polarity, evidence, delay, name) with None for a sketched step's id."""
    L = LOOPS[k]
    out = []
    for s in L['steps']:
        if s['id']:
            l = LINKS[s['id']]
            out.append({'id': l['id'], 'polarity': l['polarity'], 'evidence': l['evidence'], 'delay': l['delay'], 'name': l['name']})
        else:
            out.append({'id': None, 'polarity': s['polarity'], 'evidence': None, 'delay': None, 'name': None})
    return out


def sign_arith(k):
    st = step_list(k)
    n, m = len(st), sum(1 for s in st if s['polarity'] == '-')
    even = m % 2 == 0
    kind = 'reinforcing: it feeds itself' if even else 'balancing: it pushes back'
    if m == 0:
        return f'Every step raises the next condition, so a change comes back the same way it left. The loop is {kind}.'
    return (f'{nw(m).capitalize()} of the {nw(n)} steps {"lowers" if m == 1 else "lower"} the next condition. '
            f'An {"even" if even else "odd"} number of lowering steps makes a loop {kind}.')


def step_words(s, weakest=False):
    if s['id'] is None:
        return 'Conceptual step'
    g = f'{grade_word(s["evidence"])}, {delay_words(s["delay"])}'
    return ('Weakest step: ' + g[0].lower() + g[1:]) if weakest else g


CH_GAP = 70


def red_wire(pts, w=3, tex='solid', job='R-01 targets', kind='working'):
    """A reform target drawn in the working red (fix 7): the line and its arrowhead, with a 1 px Charcoal keyline on
    each side because red on Newsprint is 2.96:1 (design frame memo 5). Straight runs only."""
    pts2, (tx, ty, ux, uy) = trimmed(pts, HEAD[w][0])
    (x0, y0), (x1, y1) = pts2[0], pts2[-1]
    px, py = -uy, ux
    off = w / 2 + 0.5
    L = plen(pts2)
    dash, cap = fitted(tex, w, L)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    keys = ''.join(f'<path d="M{f(x0 + px * o)} {f(y0 + py * o)} L{f(x1 + px * o)} {f(y1 + py * o)}" class="red-key" stroke-width="1"/>' for o in (off, -off))
    line = f'<path d="M{f(x0)} {f(y0)} L{f(x1)} {f(y1)}" class="red-mark" stroke-width="{w}" fill="none"{da}/>'
    head = f'<path d="{head_poly(tx, ty, ux, uy, w)}" class="red-head" stroke-width="1"/>'
    jb = f' data-red-job="{job}"' if kind == 'working' else ''
    return f'<g data-red="{kind}"{jb}>{keys}{line}{head}</g>'


def red_box(x, y, w, h, job='R-01 targets'):
    """A target box outlined in the working red, inside its own Charcoal frame, against the box's White fill."""
    return (f'<g data-red="working" data-red-job="{job}"><rect x="{f(x + 2.5)}" y="{f(y + 2.5)}" width="{f(w - 5)}" height="{f(h - 5)}" '
            f'class="red-mark" fill="none" stroke-width="3"/></g>')


def chain_svg(k, width=300, interactive=False, red_targets=(), view='', title_id=None):
    """A loop as a named box-and-arrow cycle read from top to bottom. The return step runs up the right side and is
    labelled at the bottom, where the chain closes (civic polish 9). Drawn in a 320-unit viewBox for small phones."""
    L = LOOPS[k]
    st = loop_stations(k)
    steps = step_list(k)
    n = len(st)
    BW = width - 36
    LX = width - 6
    AX = 22
    weak = set(L['weakest'])
    sketch = L['conceptual']
    o = []
    y = 2
    boxes = []
    for i, (code, lab, part) in enumerate(st):
        lines = wrap(lab, 'map', BW - 14 - (34 if code else 10))
        h = 14 + 18 * len(lines) + 10
        boxes.append((y, h, code, lab, part, lines))
        y += h + (CH_GAP if i < n - 1 else 0)
    red_marks = []
    for i, (by, bh, code, lab, part, lines) in enumerate(boxes):
        open_ = code is None
        accent = '' if open_ else f'<rect x="0" y="{f(by)}" width="6" height="{f(bh)}" fill="{ACCENT[LAYER_OF_PART[part]]}"/>'
        label = TL(16, by + 26, lines, 'map', cls='ak-label', attrs=(f' data-node="{code}" data-name="{e(lab)}"' if code else ''))
        codet = T(BW - 10, by + 26, code, 'legend', anchor='end', cls='muted') if code else ''
        frame = (f'<path d="M0.5 {f(by + 0.5)} H{f(BW - 0.5)} V{f(by + bh - 0.5)} H0.5 Z" class="box-open ak-mark" stroke-width="1"/>' if open_ else
                 f'<rect x="0.5" y="{f(by + 0.5)}" width="{f(BW - 1)}" height="{f(bh - 1)}" class="box ak-mark" stroke-width="1"/>')
        say = var_say(code) if code else f'{lab}, a station in a sketched loop'
        rb = red_box(0, by, BW, bh) if code and code in red_targets else ''
        if interactive and code:
            o.append(f'<g role="button" data-select="{var_key(code)}" aria-label="{e(say)}" class="bx">{frame}{accent}{rb}{codet}{label}</g>')
        else:
            o.append(f'<g class="bx">{frame}{accent}{rb}{codet}{label}</g>')
    for i, s in enumerate(steps[:-1]):
        by, bh = boxes[i][0], boxes[i][1]
        ny = boxes[i + 1][0]
        pts = [(AX, by + bh + 2), (AX, ny - 2)]
        tex = 'solid' if sketch else tex_of(s['evidence'])
        body = wire(pts, w=2, tex=tex, n_ticks=0 if sketch else DELAY_N[s['delay']], hollow=sketch)
        if s['id'] and s['id'] in red_targets:
            body += red_wire(pts, w=2, tex=tex)
        lab_y = by + bh + 27
        g_ = sign_glyph(AX + 24, lab_y - 5, s['polarity'], r=8)
        vt = T(AX + 38, lab_y, verb(s['polarity']), 'noteb')
        ct = T(AX + 44 + tw(verb(s['polarity']), 'noteb'), lab_y, s['id'], 'note', cls='muted') if s['id'] else ''
        isw = s['id'] in weak
        l2 = TL(AX + 16, lab_y + 18, wrap(step_words(s, isw), 'noteb' if isw else 'note', BW - AX - 20), 'noteb' if isw else 'note', cls='' if isw else 'muted', lh=16)
        attrs = (f' {link_attrs(s["id"])}' if s['id'] else '')
        if interactive and s['id']:
            l_ = LINKS[s['id']]
            o.append(f'<g role="button" data-select="{link_key(s["id"])}"{attrs} aria-label="{e(s["id"])}: {e(l_["name"])}. {verb(s["polarity"]).capitalize()}. {grade_word(s["evidence"])}, {delay_words(s["delay"])}." class="st">{body}{g_}{vt}{ct}{l2}</g>')
        else:
            o.append(f'<g class="st"{attrs}>{body}{g_}{vt}{ct}{l2}</g>')
    # the return step: out of the last box, up the right side, into the first box from the right
    ret = steps[-1]
    lb, fb = boxes[-1], boxes[0]
    yl = lb[0] + lb[1] / 2
    yf = fb[0] + fb[1] / 2
    pts = [(BW + 2, yl), (LX, yl), (LX, yf), (BW + 2, yf)]
    tex = 'solid' if sketch else tex_of(ret['evidence'])
    body = wire(pts, w=2, tex=tex, n_ticks=0 if sketch else DELAY_N[ret['delay']], hollow=sketch)
    ry = lb[0] + lb[1] + 26
    first = st[0][1]
    head = f'Back to {low(first)}' if len(first) < 22 else 'Back to the start'
    hw = tw(head, 'noteb')
    lab = [T(0, ry, head, 'noteb'), sign_glyph(hw + 15, ry - 5, ret['polarity'], r=8), T(hw + 29, ry, verb(ret['polarity']), 'noteb')]
    if ret['id']:
        lab.append(T(hw + 35 + tw(verb(ret['polarity']), 'noteb'), ry, ret['id'], 'note', cls='muted'))
    isw = ret['id'] in weak
    rw = wrap(step_words(ret, isw), 'noteb' if isw else 'note', BW)
    lab.append(TL(0, ry + 18, rw, 'noteb' if isw else 'note', cls='' if isw else 'muted', lh=16))
    H = ry + 18 + 16 * (len(rw) - 1) + 8
    attrs = (f' {link_attrs(ret["id"])}' if ret['id'] else '')
    if interactive and ret['id']:
        l_ = LINKS[ret['id']]
        o.append(f'<g role="button" data-select="{link_key(ret["id"])}"{attrs} aria-label="{e(ret["id"])}: {e(l_["name"])}. The return step. {verb(ret["polarity"]).capitalize()}. {grade_word(ret["evidence"])}, {delay_words(ret["delay"])}." class="st">{body}{"".join(lab)}</g>')
    else:
        o.append(f'<g class="st"{attrs}>{body}{"".join(lab)}</g>')
    desc = f'Loop {k}, {L["plain_name"]}. {read_aloud_text(k)}'
    role = (f'role="group" aria-labelledby="{title_id}" data-ak-roving data-ak-nav="sequence" data-ak-wrap' if interactive
            else f'role="img" aria-label="{e(desc)}"')
    return (f'<svg data-view="{view or "loop-" + k.lower()}" class="draw chain" viewBox="0 0 {width} {f(H)}" width="{width}" height="{f(H)}" {role}>'
            + ''.join(o) + ''.join(red_marks) + '</svg>'), H


RING = dict(bw=300, bh=150, col=600, top=30, row=440)
RING_W = 940


def reform_tags(k, reform):
    """Which reforms aim at which stations of the loop, for the ink tags on the drawing (after System 4)."""
    L = LOOPS[k]
    stations = [c for c, _, _ in loop_stations(k)]
    out = []
    for rid in L['reforms']:
        on = [t for t in REFORMS[rid]['targets'] if t in stations or t in L['links']]
        out.append((rid, on))
    return out


def ring_svg(k='R10', red_on=True, view='loop-r10', title_id='h-loop-r10', reform='R-01'):
    """The full-size sheet after Dustin's Atlas Visual System R1 sheet: four boxes with accent rules, labelled
    arrows clockwise, the weakest step marked. R-01's three targets are drawn in the working red, and an ink tag
    names each reform that aims at the loop."""
    L = LOOPS[k]
    st = loop_stations(k)
    steps = step_list(k)
    assert len(st) == 4
    bw, bh, col, top, row = RING['bw'], RING['bh'], RING['col'], RING['top'], RING['row']
    pos = [(0, top), (col, top), (col, top + row), (0, top + row)]     # clockwise: TL, TR, BR, BL
    W = RING_W
    weak = set(L['weakest'])
    o = []
    tg = set(REFORMS[reform]['targets']) if red_on else set()
    for i, ((code, lab, part), (x, y)) in enumerate(zip(st, pos)):
        N = NODES[code]
        icon = acc.icon_svg(acc.VARIABLE_ICON[code], 'black', uid=f'{view}-{code}', size=48)
        lines = wrap(lab, 'station', bw - 22 - 16 - 56)
        means = wrap(N['increase_means'], 'cap', bw - 22 - 16)
        yy = y + 30
        body = T(x + 22, yy, f'Variable {code}', 'eyebrow', cls='muted')
        yy += 28
        body += TL(x + 22, yy, lines, 'station', cls='ak-label', attrs=f' data-node="{code}" data-name="{e(lab)}"')
        yy += 22 * (len(lines) - 1) + 24
        body += TL(x + 22, yy, means, 'cap', cls='muted')
        frame = (f'<rect x="{f(x + 0.5)}" y="{f(y + 0.5)}" width="{bw - 1}" height="{bh - 1}" class="box ak-mark" stroke-width="1"/>'
                 f'<rect x="{x}" y="{y}" width="6" height="{bh}" fill="{ACCENT[LAYER_OF_PART[part]]}"/>')
        rb = red_box(x, y, bw, bh) if code in tg else ''
        ic = f'<g transform="translate({x + bw - 60},{y + 12})">{icon}</g>'
        o.append(f'<g role="button" data-select="{var_key(code)}" aria-label="{e(var_say(code))}" class="bx">{frame}{rb}{body}{ic}</g>')
    cy_top, cy_bot = top + bh / 2, top + row + bh / 2
    xr, xl = col + 60, bw - 60
    paths = [
        [(bw + 2, cy_top), (col - 2, cy_top)],
        [(xr, top + bh + 2), (xr, top + row - 2)],
        [(col - 2, cy_bot), (bw + 2, cy_bot)],
        [(xl, top + row - 2), (xl, top + bh + 2)],
    ]
    label_at = [
        ((bw + col) / 2, cy_top + 26, 'middle', col - bw - 40),
        (xr + 22, top + bh + 128, 'start', W - xr - 26),
        ((bw + col) / 2, cy_bot + 26, 'middle', col - bw - 40),
        (xl - 22, top + bh + 128, 'end', bw - 90),
    ]
    for i, (s, pts) in enumerate(zip(steps, paths)):
        l = LINKS[s['id']]
        isweak = s['id'] in weak
        body = wire(pts, w=3, tex=tex_of(s['evidence']), n_ticks=DELAY_N[s['delay']])
        if s['id'] in tg:
            body += red_wire(pts, w=3, tex=tex_of(s['evidence']))
        lx, ly, anchor, width = label_at[i]
        lab = []
        eb = f'Step {i + 1} · {s["id"]}' + (' · the return' if i == 3 else '') + (' · weakest' if isweak else '')
        lab.append(T(lx, ly, eb, 'eyebrow', anchor=anchor, cls='muted'))
        nm = wrap(l['name'], 'map', width)
        lab.append(TL(lx, ly + 22, nm, 'map', anchor=anchor, cls='ak-label', attrs=f' data-link="{s["id"]}" data-sign="{sign_attr(s["polarity"])}" data-grade="{s["evidence"]}" data-name="{e(l["name"])}"'))
        yy = ly + 22 + 18 * (len(nm) - 1) + 26
        vw = tw(verb(s['polarity']), 'noteb')
        gx = lx - (vw + 30) / 2 + 11 if anchor == 'middle' else (lx - vw - 30 + 11 if anchor == 'end' else lx + 11)
        lab.append(sign_glyph(gx, yy - 5, s['polarity'], r=11))
        lab.append(T(gx + 19, yy, verb(s['polarity']), 'noteb'))
        yy += 22
        for ln in wrap(f'{grade_word(s["evidence"])}: {grade_gloss(s["evidence"])}', 'note', width):
            lab.append(T(lx, yy, ln, 'note', anchor=anchor, cls='muted'))
            yy += 16
        lab.append(T(lx, yy, delay_words(s['delay']).capitalize(), 'note', anchor=anchor, cls='muted'))
        if isweak:
            yy += 24
            for ln in wrap('The weakest step: the loop holds only as firmly as this link.', 'noteb', width):
                lab.append(T(lx, yy, ln, 'noteb', anchor=anchor))
                yy += 16
        say = f'Step {i + 1}, {s["id"]}: {l["name"]}. {verb(s["polarity"]).capitalize()}. {grade_word(s["evidence"])}, {delay_words(s["delay"])}.' + (' The weakest step.' if isweak else '') + (f' Reform {reform} acts here.' if s['id'] in tg else '')
        o.append(f'<g role="button" data-select="{link_key(s["id"])}" {link_attrs(s["id"])} aria-label="{e(say)}" class="st">{body}{"".join(lab)}</g>')
    bx_, by_ = (bw + col) / 2, top + bh + (row - bh) / 2 + 30
    o.append(f'<g aria-hidden="true" class="badge"><circle cx="{f(bx_)}" cy="{f(by_)}" r="38" class="badge-ring"/>'
             + T(bx_, by_ - 8, 'Loop', 'eyebrow', anchor='middle', cls='muted') + T(bx_, by_ + 16, k, 'phead', anchor='middle')
             + T(bx_, by_ + 66, L['kind_word'], 'map', anchor='middle') + T(bx_, by_ + 84, L['kind_gloss'], 'note', anchor='middle', cls='muted') + '</g>')
    # ink tags: which reform aims where. The red marks R-01's targets; the tags name every reform on the loop.
    where = {c: i for i, (c, _, _) in enumerate(st)}
    for rid, on in reform_tags(k, reform):
        boxes_on = [t for t in on if t in where]
        if not boxes_on:
            continue
        i = where[boxes_on[0]]
        x, y = pos[i]
        verb_ = 'acts on' if rid == reform else 'aims at'
        txt = f'{rid} {verb_} {", ".join(on[:-1]) + " and " + on[-1] if len(on) > 1 else on[0]}'
        ty = y - 14 if i in (0, 1) else y + bh + 24
        tx = x + bw if i in (1, 2) else x
        anchor = 'end' if i in (1, 2) else 'start'
        tag = T(tx, ty, txt, 'noteb', anchor=anchor)
        if rid == reform:
            o.append(f'<a href="#reform-r01" aria-label="Reform {rid} acts on {", ".join(on)}. Opens the reform sheet.">{tag}</a>')
        else:
            o.append(f'<g aria-label="Reform {rid}, {e(REFORMS[rid]["title"])}, aims at {", ".join(on)}.">{tag}</g>')
    H = top + row + bh + 120
    return (f'<svg data-view="{view}" class="draw ring" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="group" aria-labelledby="{title_id}" '
            f'data-ak-roving data-ak-nav="sequence" data-ak-wrap>' + ''.join(o) + '</svg>')


def r01_card(compact=False):
    """R-01 at a glance, in HTML beside the drawing: what it is, where it acts, its disclosure (D2-80)."""
    R = REFORMS['R-01']
    tg = sorted(R['targets'], key=lambda t: (t not in LINKS, t))
    on = '; '.join(f'{t}, {e(node_label(t) if t in NODES else LINKS[t]["name"])}' for t in tg)
    return (f'<div class="r01c" data-reform="R-01" data-targets="{" ".join(R["targets"])}"><p class="t-eyebrow">Reform R-01 · where it acts, in red</p>'
            f'<h3 class="t-phead"><button type="button" class="vc-name" data-select="reform-r-01" aria-label="Reform R-01, {e(R["title"])}. Opens its record."><span data-reform="R-01" data-name="{e(R["title"])}">{e(R["title"])}</span></button></h3>'
            f'<p class="t-cap">It acts on {on}.</p>'
            f'<p class="t-cap muted">Problem evidence {grade_word(R["problem_evidence"]["grade"]).lower()}; remedy evidence {grade_word(R["remedy_evidence"]["grade"]).lower()}.</p>'
            f'<p class="t-note rc-disc"><b>Disclosure.</b> {e(R["disclosure"])}</p>'
            f'<p class="t-cap"><a class="tlink" href="#reform-r01">Open the full reform, sheet 04</a></p></div>')


# ------------------------------------------------------------------------------------------- 03 loop R10
def note_block(title, html_):
    return f'<div class="nblock"><p class="t-eyebrow">{e(title)}</p><div class="t-ptext">{html_}</div></div>'


def stepper_html(k):
    L = LOOPS[k]
    steps = L['steps']
    first = node_label(steps[0]['from'])
    parts, back = read_aloud(k)
    items = []
    for i, s in enumerate(steps):
        l = LINKS[s['id']]
        a_word, a_lab = parts[i]
        b_word, b_lab = parts[i + 1] if i + 1 < len(parts) else back
        sent = f'{l["id"]}, {l["name"]}. {a_word.capitalize()} {a_lab} means {b_word} {b_lab}. Sign {"+" if l["polarity"] == "+" else MINUS}, {"same way" if l["polarity"] == "+" else "opposite way"}; {grade_word(l["evidence"]).lower()}; {delay_words(l["delay"])}.'
        items.append(f'<li data-ak-step-keys="{link_key(s["id"])} {var_key(s["to"])}" {link_attrs(s["id"])}>{e(sent)}</li>')
    wk = L['weakest'][0] if L['weakest'] else None
    end = f'The loop is back where it started, so it {L["kind_gloss"]}: {L["kind_word"].lower()}.' + (f' Its weakest step is {wk}, graded {grade_word(LINKS[wk]["evidence"]).lower()}.' if wk else '')
    idle = f'Start at {steps[0]["from"]}, {first}, and suppose it rises. Press Play, or Next step to follow one numbered connection at a time.'
    return (f'<section class="stepper" data-ak-stepper data-ak-hold="3200" data-ak-end="{e(end)}" aria-labelledby="r10-follow-h">'
            f'<div class="st-btns"><button type="button" class="ak-btn" data-ak-step="play">Play</button>'
            f'<button type="button" class="ak-btn" data-ak-step="prev">Previous step</button>'
            f'<button type="button" class="ak-btn" data-ak-step="next">Next step</button>'
            f'<button type="button" class="ak-btn" data-ak-step="reset">Reset</button></div>'
            f'<p class="st-status t-ptext" data-ak-step-status aria-live="polite">{e(idle)}</p>'
            f'<ol class="st-list t-cap" data-ak-step-list>{"".join(items)}</ol></section>')


def red_legend(text):
    """The key entry for the working red: a short red line with its keylines, as drawn on the loop."""
    svg = ('<svg width="36" height="12" viewBox="0 0 36 12" aria-hidden="true">'
           '<path d="M1 4 H35 M1 8 H35" stroke="#121212" stroke-width="1"/><path d="M1 6 H35" stroke="#E63946" stroke-width="3"/></svg>')
    return f'<span class="kred" data-red="working" data-red-job="R-01 targets">{svg}{e(text)}</span>'


def loop_legend():
    return (f'<div class="ckey t-legend" aria-hidden="true">'
            f'<span>{sign_svg("+", 22)} raises: the two move the same way</span><span>{sign_svg("-", 22)} lowers: they move opposite ways</span>'
            f'<span><svg width="30" height="14"><path d="M1 7 H29 M8 1 V13 M13 1 V13" stroke="currentColor" stroke-width="2"/></svg>Ticks count the wait: one under 2 years, two for 2 to 10, three over 10</span>'
            + red_legend('Red marks where reform R-01 acts') + '</div>')


def loop_facts(k):
    L = LOOPS[k]
    rows = [('Kind', kind_words(k)), ('One turn', L['delay_word']), ('Now', DIRECTION_WORDS.get(L['direction'], L['direction'])),
            ('Weakest step', weakest_short(k)), ('Reforms aimed at it', ', '.join(L['reforms']))]
    return '<dl class="facts t-cap">' + ''.join(f'<div><dt>{a_}</dt><dd>{e(b_)}</dd></div>' for a_, b_ in rows) + '</dl>'


def view_loop_r10():
    k = 'R10'
    L = LOOPS[k]
    R = REFORMS['R-01']
    wk = LINKS[L['weakest'][0]]
    headline = f'Safe seats can keep themselves safe, through one {grade_word(wk["evidence"]).lower()} step.'
    deck = (f'<p class="loop-id">{chip("Loop", k)} <b>{e(L["plain_name"])}</b>, {e(kind_words(k).lower())}. '
            f'<span data-loop="{k}" data-steps="{loop_steps_attr(k)}" data-name="{e(L["title"])}">{e(L["title"])}</span>.</p>')
    side = toc([('r10-loop', '03.1', 'The loop, step by step'), ('r10-reforms', '03.2', 'Where reforms act'),
                ('r10-evidence', '03.3', 'What holds it up')])
    head = sheet_head('loop-r10', f'Loop {k} · {L["kind_word"]}, {L["kind_gloss"]}', headline, deck, side, here={'C'})
    ra = f'<div class="readaloud"><p class="t-eyebrow">Read it aloud</p><p class="ra-text">{read_aloud_html(k)}</p></div>'
    chain, _ = chain_svg(k, interactive=True, red_targets=set(R['targets']), view='loop-r10-phone', title_id='r10-loop-h')
    how = f'<p class="t-cap how">Start at {L["steps"][0]["from"]}, top left, and follow the arrows clockwise. {e(sign_arith(k))}</p>'
    side_col = (f'<aside class="r10-side"><h3 class="t-eyebrow" id="r10-follow-h">Follow one change around the loop</h3>{stepper_html(k)}{how}</aside>')
    p1 = (f'<section class="plate p-first" id="r10-loop" aria-labelledby="r10-loop-h"><h2 class="t-eyebrow p-eb" id="r10-loop-h">03.1 The loop, step by step</h2>'
          f'{ra}<div class="r10-grid"><div class="r10-draw">'
          f'<div class="wide-only"><div class="ak-scroll" role="region" tabindex="0" aria-label="Loop R10, drawing" style="--ak-min:{RING_W}px">{ring_svg(k)}</div>'
          f'<p class="ak-readout t-cap" data-ak-readout>Point at, tab to or tap a box or a step to read its record.</p></div>'
          f'<div class="narrow-only phone-chain">{chain}<p class="t-cap r01-note">Red marks where reform R-01 acts: {", ".join(sorted(R["targets"]))}. '
          f'<a class="tlink" href="#reform-r01">Open the reform</a>.</p></div></div>{side_col}</div>'
          f'<div class="loop-keys">{loop_legend()}{evidence_key()}</div>'
          f'<p class="plate-foot t-note"><span>Loop {k} · variables {", ".join(s["from"] for s in L["steps"])} · connections {", ".join(L["links"])} · reform R-01 targets {", ".join(R["targets"])}</span><span>Atlas V7, snapshot {SNAP}</span></p></section>')
    rcards = [r01_card()]
    for rid in L['reforms']:
        if rid == 'R-01':
            continue
        r = REFORMS[rid]
        on = [t for t in r['targets'] if t in L['links'] or t in [s['from'] for s in L['steps']]]
        rcards.append(f'<div class="rcard" data-reform="{rid}" data-targets="{" ".join(r["targets"])}">'
                      f'<p>{chip("Reform", rid, compact=True)}</p><h3 class="t-phead" data-reform="{rid}" data-name="{e(r["title"])}">{e(r["title"])}</h3>'
                      f'<p class="t-cap">Aims at this loop at {", ".join(on) if on else "no step directly"}; its targets are {", ".join(r["targets"])}.</p>'
                      f'<p class="t-cap muted">{e(sentences(r["summary"])[0])}</p>'
                      + (f'<p class="t-note rc-disc"><b>Disclosure.</b> {e(r["disclosure"])}</p>' if r.get('disclosure') else '') + '</div>')
    p2 = plate('r10-reforms', '03.2', 'Where reforms act',
               f'<p>{nw(len(L["reforms"])).capitalize()} reforms aim at this loop. Each acts at named points, and their effects are rated one by one, never added together. '
               f'Red on the drawing marks R-01’s three targets; ink tags name the others.</p>',
               f'<div class="rcards">{"".join(rcards)}</div>')
    notes = ''.join([
        note_block('What the loop says', f'<p>{e(L["summary"])}</p>'),
        note_block(f'Loop {k} at a glance', loop_facts(k)),
        note_block('The weakest step', f'<p><b>{wk["id"]}, {e(wk["name"])}</b>, is graded {grade_word(wk["evidence"]).lower()}, which means {grade_gloss(wk["evidence"])}. The loop holds only as firmly as this step.</p>'),
        note_block('Keep the qualification', f'<p>{e(L["qualification"])}</p>'),
        note_block('What the evidence shows', f'<p>{e(L["evidence_summary"])}</p>'),
        note_block('How long one turn takes', f'<p>{e(L["delay_word"].capitalize())}. ' + ' '.join(f'{s["id"]} acts in {delay_words(s["delay"])}.' for s in L['steps']) + '</p>'),
        note_block('Where it stands now', f'<p>{e(DIRECTION_WORDS[L["direction"]])}, measured by the {e(low(L["reference_mode"]))}. {e(IMPROVE)}</p>'),
        note_block('How to read the signs', f'<p>{e(sign_arith(k))} {e(sign_rule())}</p>'),
        note_block('A real case', f'<p>{e(L["case"])}</p>'),
    ])
    p3 = plate('r10-evidence', '03.3', 'What holds it up', '', f'<div class="notes">{notes}</div>')
    return (f'<section data-view-root="loop-r10" data-crumb="Safe-seat loop R10" data-parent="area-c" aria-labelledby="h-loop-r10">'
            f'{head}{p1}{p2}{p3}</section>')



# ------------------------------------------------------------------------------------------- 02 Elections
def issue_grade(g):
    return {'well_supported': 'well-supported'}.get(g, g)


def effect_lead(v):
    m = re.match(r'\s*([+-][LMS]|0|\?)', v)
    return m.group(1) if m else '?'


def effect_words(v):
    """An effect in words only, with V7's qualifier kept as words (brief fix 6): "+S entry; -S extremity" reads
    "small positive for entry; small negative for extremity"."""
    code = r'([+-][LMS]|0|\?)'
    segs = []
    for seg in [x.strip() for x in v.split(';')]:
        words = re.sub(code, lambda m: D['effect_codes'][m.group(1)], seg)
        lead = re.match(r'\s*(?:[+-][LMS]|0|\?)(?:\s*(?:to|/)\s*(?:[+-][LMS]|0|\?))*', seg)
        rest = seg[lead.end():].strip() if lead and lead.end() else ''
        if lead and lead.end() and rest:
            head = re.sub(code, lambda m: D['effect_codes'][m.group(1)], seg[:lead.end()]).strip().replace(' / ', ' or ')
            first = rest.split()[0]
            joiner = ' ' if first in ('in', 'at', 'if', 'over', 'where', 'to', 'for', 'during') else ' for '
            if first in ('long', 'short', 'delayed', 'direct', 'indirect,', 'indirect', 'contested', 'conditional', 'hypothesis', 'precondition', 'structure', 'risk'):
                words = f'{head} ({rest})'
            else:
                words = f'{head}{joiner}{rest}'
        segs.append(words.replace(' / ', ' or '))
    return '; '.join(segs)


def bez_wire(x0, y0, x1, y1, w=2, tex='solid', n_ticks=0, head='arrow'):
    """A connection drawn as a smooth curve with horizontal ends, its texture fitted to its length."""
    hl = HEAD[w][0] if head == 'arrow' else 14
    xe = x1 - hl
    dx = (xe - x0) * 0.5
    d = f'M{f(x0)} {f(y0)} C{f(x0 + dx)} {f(y0)} {f(xe - dx)} {f(y1)} {f(xe)} {f(y1)}'
    pts = []
    for i in range(41):
        t = i / 40
        x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * (x0 + dx) + 3 * (1 - t) * t ** 2 * (xe - dx) + t ** 3 * xe
        y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * y0 + 3 * (1 - t) * t ** 2 * y1 + t ** 3 * y1
        pts.append((x, y))
    L = plen(pts) - (1.5 * w if tex == 'dotted' else 0)
    dash, cap = fitted(tex, w, L)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    lc = f' stroke-linecap="{cap}"' if cap != 'butt' else ''
    hd = (f'<path d="{head_poly(x1, y1, 1, 0, w)}" class="head"/>' if head == 'arrow' else
          f'<path d="{diamond_poly(x1, y1, 1, 0)}" class="diamond" stroke-width="2"/>')
    tk = ticks([(x0, y0), (x0 + 40, y0)], n_ticks, w, start=12) if n_ticks else ''
    return (f'<path d="{d}" class="ak-case" fill="none"{da}{lc}/><path d="{d}" class="ak-mark" fill="none" stroke-width="{w}"{da}{lc}/>'
            f'{tk}{hd}<path d="{d}" class="ak-hit"/>')


def c_links():
    C = PARTS['C']['nodes']
    ins = [l for l in LINKS.values() if l['to'] in C and l['from'] not in C]
    outs = [l for l in LINKS.values() if l['from'] in C and l['to'] not in C]
    inside = [l for l in LINKS.values() if l['from'] in C and l['to'] in C]
    return sorted(ins, key=lambda l: l['id']), sorted(outs, key=lambda l: l['id']), sorted(inside, key=lambda l: l['id'])


def best_tracks(links, y_far, y_near, far_is_from):
    """Order the vertical tracks of horizontal-vertical-horizontal routes so they cross as little as possible.
    Brute force over every order (at most 8 lines)."""
    import itertools
    ids = [l['id'] for l in links]

    def crossings(order):
        t = {k: i for i, k in enumerate(order)}
        n = 0
        for a_ in ids:
            for b_ in ids:
                if a_ == b_:
                    continue
                # a's vertical against b's two horizontals
                lo, hi = sorted((y_far[a_], y_near[a_]))
                # the far-side horizontal of b runs from the far box to b's track
                if far_is_from:
                    if t[a_] < t[b_] and lo < y_far[b_] < hi:
                        n += 1
                    if t[a_] > t[b_] and lo < y_near[b_] < hi:
                        n += 1
                else:
                    if t[a_] > t[b_] and lo < y_far[b_] < hi:
                        n += 1
                    if t[a_] < t[b_] and lo < y_near[b_] < hi:
                        n += 1
        return n
    best, bn = None, None
    for order in itertools.permutations(ids):
        c = crossings(order)
        if bn is None or c < bn:
            best, bn = order, c
    return list(best), bn


def neighborhood_svg():
    """After the V8 "What pushes on it and what it pushes on": the part in the middle, the conditions that push on it
    on the left and those it pushes on to the right, grouped by part. Lines run in their own tracks, so each label
    sits on a straight lead-in that no other line crosses."""
    ins, outs, inside = c_links()
    C = PARTS['C']['nodes']
    order = ['X'] + CORE + ['EC', 'TC']
    W = 1312
    LW, RW = 256, 256
    LBL = 122                      # label lead-in
    TRK = 12                       # track spacing
    LX0, CX = 0, LW + LBL + 8 * TRK + 26
    CWd = 340
    RX = W - RW
    o = []
    nports = {'L': {}, 'R': {}}
    for l in ins:
        nports['L'][l['from']] = nports['L'].get(l['from'], 0) + 1
    for l in outs:
        nports['R'][l['to']] = nports['R'].get(l['to'], 0) + 1

    def column(vars_, x, w, title, side):
        by_part = {}
        for v in vars_:
            by_part.setdefault(PART_OF[v], []).append(v)
        y = 70
        pos = {}
        o.append(T(x, 26, title, 'eyebrow'))
        for p in sorted(by_part, key=order.index):
            o.append(T(x, y, part_name(p), 'map') + T(x + tw(part_name(p), 'map') + 8, y, PARTS[p]['formal_title'], 'note', cls='muted'))
            y += 14
            for v in sorted(by_part[p], key=lambda n: list(NODES).index(n)):
                lines = wrap(node_label(v), 'ptext', w - 60)
                h = max(20 * len(lines) + 20, 26 * nports[side][v] + 14)
                acc_col = ACCENT[LAYER_OF_PART[p]]
                o.append(f'<g role="button" data-select="{var_key(v)}" aria-label="{e(var_say(v))}" class="bx">'
                         f'<rect x="{x + 0.5}" y="{f(y + 0.5)}" width="{w - 1}" height="{h - 1}" class="box ak-mark" stroke-width="1"/>'
                         + ('' if p == 'X' else f'<rect x="{x}" y="{f(y)}" width="6" height="{h}" fill="{acc_col}"/>')
                         + T(x + 16, y + h / 2 + 5 - 10 * (len(lines) - 1), v, 'code', cls='muted')
                         + TL(x + 52, y + h / 2 + 5 - 10 * (len(lines) - 1), lines, 'ptext', cls='ak-label', attrs=f' data-node="{v}" data-name="{e(node_label(v))}"') + '</g>')
                pos[v] = (y, h)
                y += h + 10
            y += 26
        return pos, y

    src = sorted({l['from'] for l in ins}, key=lambda n: (order.index(PART_OF[n]), list(NODES).index(n)))
    tgt = sorted({l['to'] for l in outs}, key=lambda n: (order.index(PART_OF[n]), list(NODES).index(n)))
    lpos, lh = column(src, LX0, LW, f'Pushes on Elections ({len(ins)})', 'L')
    rpos, rh = column(tgt, RX, RW, f'Elections pushes on ({len(outs)})', 'R')
    P_ = PARTS['C']
    cy0 = 44
    o.append(T(CX + 16, cy0 + 30, P_['plain_name'], 'phead', attrs=' data-part="C" data-name="Elections"')
             + T(CX + 16 + tw(P_['plain_name'], 'phead') + 10, cy0 + 30, P_['formal_title'], 'legend', cls='muted', attrs=' data-part="C" data-name="Electoral competition"'))
    cpos = {}
    y = cy0 + 50
    bx0, bw0 = CX + 16, CWd - 32
    for v in C:
        h = 52
        o.append(f'<g role="button" data-select="{var_key(v)}" aria-label="{e(var_say(v))}" class="bx">'
                 f'<rect x="{bx0 + 0.5}" y="{f(y + 0.5)}" width="{bw0 - 1}" height="{h - 1}" class="box ak-mark" stroke-width="1"/>'
                 f'<rect x="{bx0}" y="{f(y)}" width="6" height="{h}" fill="{ACCENT["core"]}"/>'
                 + T(bx0 + 18, y + 31, v, 'code', cls='muted') + T(bx0 + 50, y + 31, node_label(v), 'map', cls='ak-label', attrs=f' data-node="{v}" data-name="{e(node_label(v))}"') + '</g>')
        cpos[v] = (y, h)
        y += h + 20
    y += 12
    o.append(T(bx0, y, f'Inside Elections ({len(inside)})', 'eyebrow'))
    y += 6
    for l in inside:
        y += 40
        say = f'{l["id"]}: {l["name"]}. {verb(l["polarity"]).capitalize()}. {grade_word(l["evidence"])}, {delay_words(l["delay"])}.'
        lead = f'{l["from"]} {verb(l["polarity"])} {l["to"]}'
        o.append(f'<g role="button" data-select="{link_key(l["id"])}" {link_attrs(l["id"])} aria-label="{e(say)}" class="st">'
                 f'<rect x="{bx0 - 4}" y="{f(y - 18)}" width="{bw0 + 8}" height="38" class="vhit"/>'
                 + T(bx0, y, l['id'], 'code', cls='muted') + sign_glyph(bx0 + 48, y - 5, l['polarity'], r=8)
                 + T(bx0 + 62, y, lead, 'noteb', cls='ak-label')
                 + T(bx0 + 62, y + 16, f'{grade_word(l["evidence"])}, {delay_words(l["delay"])}', 'note', cls='muted') + '</g>')
    ch = y + 34
    o.insert(0, f'<rect x="{CX + 0.5}" y="{cy0 + 0.5}" width="{CWd - 1}" height="{f(ch - cy0 - 1)}" class="frame-open"/>')
    H = max(lh, rh, ch) + 10

    def spread(items, posd):
        """Ports along a box edge, ordered by the other end's height."""
        out = {}
        groups = {}
        for key_, other_y, lid in items:
            groups.setdefault(key_, []).append((other_y, lid))
        for v, lst in groups.items():
            lst.sort()
            yb, hb = posd[v]
            n = len(lst)
            for i, (_, lid) in enumerate(lst):
                out[lid] = yb + hb / 2 + (i - (n - 1) / 2) * (26 if posd is not cpos else 12)
        return out

    def centre(posd, v):
        yb, hb = posd[v]
        return yb + hb / 2
    # far ends (left and right columns) and near ends (the Elections boxes)
    in_far = spread([(l['from'], centre(cpos, l['to']), l['id']) for l in ins], lpos)
    in_near = spread([(l['to'], in_far[l['id']], l['id']) for l in ins], cpos)
    out_far = spread([(l['to'], centre(cpos, l['from']), l['id']) for l in outs], rpos)
    out_near = spread([(l['from'], out_far[l['id']], l['id']) for l in outs], cpos)
    in_order, in_x = best_tracks(ins, in_far, in_near, True)
    out_order, out_x = best_tracks(outs, out_far, out_near, False)
    tr_in0 = LW + LBL + 14
    tr_out0 = CX + CWd + 14
    for l in ins:
        lid = l['id']
        tx = tr_in0 + in_order.index(lid) * TRK
        y0, y1 = in_far[lid], in_near[lid]
        pts = [(LW + 2, y0), (tx, y0), (tx, y1), (bx0 - 2, y1)] if abs(y1 - y0) > 0.5 else [(LW + 2, y0), (bx0 - 2, y1)]
        o.append(nb_link(l, pts, LW + 9, y0))
    for l in outs:
        lid = l['id']
        tx = tr_out0 + out_order.index(lid) * TRK
        y0, y1 = out_near[lid], out_far[lid]
        pts = [(bx0 + bw0 + 2, y0), (tx, y0), (tx, y1), (RX - 2, y1)] if abs(y1 - y0) > 0.5 else [(bx0 + bw0 + 2, y0), (RX - 2, y1)]
        o.append(nb_link(l, pts, RX - 10, y1, right=True))
    return (f'<svg data-view="area-c" class="draw nb" viewBox="0 0 {W} {f(H)}" width="{W}" height="{f(H)}" role="group" aria-labelledby="c-push-h" '
            f'aria-describedby="c-push-words" data-ak-roving data-ak-nav="spatial">' + ''.join(o) + '</svg>')


def nb_link(l, pts, lx, ly, right=False):
    auth = l['type'] == 'authority'
    body = wire(pts, w=2, tex=tex_of(l['evidence']), head='diamond' if auth else 'arrow', r=8)
    lab_w = tw(l['id'], 'code') + 8 + 18 + tw(verb(l['polarity']), 'noteb')
    x = (lx - lab_w - 14) if right else lx
    pad = f'<rect x="{f(x - 6)}" y="{f(ly - 11)}" width="{f(lab_w + 12)}" height="22" class="gap"/>'
    lab = (T(x, ly + 5, l['id'], 'code', cls='muted') + sign_glyph(x + tw(l['id'], 'code') + 17, ly, l['polarity'], r=8)
           + T(x + tw(l['id'], 'code') + 30, ly + 5, verb(l['polarity']), 'noteb', cls='ak-label'))
    say = f'{l["id"]}: {l["name"]}. From {l["from"]} {node_label(l["from"])} to {l["to"]} {node_label(l["to"])}. {verb(l["polarity"]).capitalize()}. {grade_word(l["evidence"])}, {delay_words(l["delay"])}.'
    return f'<g role="button" data-select="{link_key(l["id"])}" {link_attrs(l["id"])} data-rel="{var_key(l["from"])} {var_key(l["to"])}" aria-label="{e(say)}" class="st">{body}{pad}{lab}</g>'


def c_words_html():
    ins, outs, inside = c_links()
    order = ['X'] + CORE + ['EC', 'TC']

    def grp(lst, end):
        by = {}
        for l in lst:
            by.setdefault(PART_OF[l[end]], []).append(l)
        out = ''
        for p in sorted(by, key=order.index):
            out += f'<li class="grp"><p class="t-eyebrow">{e(part_name(p))}</p><ul class="lrows">' + ''.join(link_row(l['id']) for l in by[p]) + '</ul></li>'
        return out
    return (f'<div class="cwords" id="c-push-words"><div><h3 class="t-phead">Pushes on Elections ({len(ins)})</h3><ul class="plain">{grp(ins, "from")}</ul></div>'
            f'<div><h3 class="t-phead">Elections pushes on ({len(outs)})</h3><ul class="plain">{grp(outs, "to")}</ul></div>'
            f'<div><h3 class="t-phead">Inside Elections ({len(inside)})</h3><ul class="lrows">{"".join(link_row(l["id"]) for l in inside)}</ul></div></div>')


def loop_card(k, red_targets=(), level='h3'):
    L = LOOPS[k]
    svg, _ = chain_svg(k, red_targets=red_targets)
    rf = L['reforms']
    cn = closure_note(k)
    is_r10 = k == 'R10'
    name_el = (f'<a href="#loop-r10" class="lc-name" data-loop="{k}" data-name="{e(L["plain_name"])}">{e(L["plain_name"])}</a>' if is_r10 else
               f'<button type="button" class="lc-name" data-select="{loop_key(k)}" aria-label="{e(L["plain_name"])}, loop {k}. Opens its record." data-loop="{k}" data-name="{e(L["plain_name"])}">{e(L["plain_name"])}</button>')
    return (f'<article class="lcard{" sketch" if L["conceptual"] else ""}" data-loop="{k}" data-steps="{loop_steps_attr(k)}">'
            f'<p class="lc-top">{chip("Loop", k, compact=True)}<span class="t-legend">{e(kind_words(k))}</span></p>'
            f'<{level} class="t-phead">{name_el}</{level}>'
            f'<p class="lc-title t-cap" data-loop="{k}" data-name="{e(L["title"])}">{e(L["title"])}</p>'
            f'<p class="lc-sum t-ptext">{e(sentences(L["summary"])[0])}</p>'
            + (f'<p class="lc-q t-cap"><b>Keep in mind.</b> {e(L["qualification"])}</p>' if k == 'R1' else '')
            + f'<div class="lc-draw">{svg}</div>'
            f'<p class="lc-ra t-cap"><span class="t-eyebrow">Read it aloud</span> {read_aloud_html(k)}</p>'
            f'<dl class="lc-facts t-note"><div><dt>Weakest step</dt><dd>{e(weakest_short(k))}</dd></div>'
            f'<div><dt>One turn</dt><dd>{e(L["delay_word"])}</dd></div><div><dt>Now</dt><dd>{e(DIRECTION_WORDS.get(L["direction"], L["direction"]))}</dd></div>'
            f'<div><dt>Reforms</dt><dd data-count="custom:reforms on {k}">{len(rf)}</dd></div></dl>'
            + (f'<p class="lc-note t-note">{e(cn)}</p>' if cn else '')
            + (f'<p class="lc-open t-note"><a class="tlink" href="#loop-r10">Open the safe-seat loop at full size</a></p>' if is_r10 else '')
            + '</article>')


def view_area_c():
    P_ = PARTS['C']
    C = P_['nodes']
    ins, outs, inside = c_links()
    through = [k for k in D['loop_order'] if any(code in C for code, _, _ in loop_stations(k) if code)]
    iss = issues_on(C)
    refs = [r for r in REFORMS.values() if any((t in C) or (t in LINKS and (LINKS[t]['from'] in C or LINKS[t]['to'] in C)) for t in r['targets'])]
    st_count = {v: sum(1 for k in through if v in [c for c, _, _ in loop_stations(k)]) for v in C}
    top = max(st_count.values())
    busiest = [v for v in C if st_count[v] == top]
    spec = (f'<dl class="spec spec5">'
            f'<div><dt><span class="t-fig" data-count="variables_C">{len(C)}</span></dt><dd class="t-note">conditions</dd></div>'
            f'<div><dt><span class="t-fig" data-count="custom:touch C">{len(ins) + len(outs) + len(inside)}</span></dt><dd class="t-note">connections touch it: {len(inside)} inside, {len(ins)} in, {len(outs)} out</dd></div>'
            f'<div><dt><span class="t-fig" data-count="custom:loops through C">{len(through)}</span></dt><dd class="t-note">loops run through it</dd></div>'
            f'<div><dt><span class="t-fig" data-count="custom:issues on C">{len(iss)}</span></dt><dd class="t-note">issues tracked here</dd></div>'
            f'<div><dt><span class="t-fig" data-count="custom:reforms on C">{len(refs)}</span></dt><dd class="t-note">reforms aimed here</dd></div></dl>')
    deck = (f'<p class="sub t-station"><span data-part="C" data-name="{e(P_["formal_title"])}">{e(P_["formal_title"])}</span>. {e(P_["plain_question"])}</p>'
            f'<p>{e(P_["story"])}</p>{spec}')
    side = evidence_key() + toc([('c-vars', '02.1', 'The five conditions'), ('c-push', '02.2', 'What pushes on it'), ('c-loops', '02.3', 'Loops that run through it'),
                ('c-issues', '02.4', 'Issues tracked here'), ('c-reforms', '02.5', 'Reforms aimed here')])
    head = sheet_head('area-c', 'Part C · A close-up', f'<span data-part="C" data-name="Elections">Elections</span>', deck, side, here={'C'})
    # 02.1 the five conditions
    cards = []
    for v in C:
        N = NODES[v]
        lp = N['loops']
        n_iss = len(issues_on([v]))
        icon = acc.icon_svg(acc.VARIABLE_ICON[v], 'black', uid=f'c-card-{v}', size=48)
        cards.append(f'<article class="vcard"><div class="vc-top">{chip("Variable", v, compact=True)}{icon}</div>'
                     f'<h3 class="t-station"><button type="button" class="vc-name" data-select="{var_key(v)}" aria-label="{e(var_say(v))}"><span class="ak-label" data-node="{v}" data-name="{e(N["label"])}">{e(N["label"])}</span></button></h3>'
                     f'<p class="t-cap muted">{e(N["title"])}</p><p class="t-ptext vc-desc">{e(N["description"])}</p>'
                     f'<p class="t-ptext vc-means"><b>{e(N["increase_means"])}</b></p>'
                     f'<dl class="t-note vc-facts">'
                     f'<div><dt>Loops</dt><dd>' + (', '.join(f'<a href="{loop_href(k)}">{k}</a>' for k in lp) or 'none') + f'</dd></div><div><dt>Issues</dt><dd>{n_iss}</dd></div></dl></article>')
    p1 = plate('c-vars', '02.1', 'The five conditions', f'<p>Each condition can rise or fall. The bold line says what a higher value means, so a label such as “{e(NODES[C[0]]["label"])}” reads as an amount.</p>',
               f'<div class="vcards">{"".join(cards)}</div>')
    # 02.2 what pushes on it
    p2 = plate('c-push', '02.2', 'What pushes on it and what it pushes on',
               f'<p>{len(ins)} connections arrive from other parts and {len(outs)} leave for them, grouped by the part at the far end. Each one names what it does, says whether it raises or lowers the condition it reaches, and gives its evidence and its delay.</p>',
               f'{c_words_html()}'
               f'<details class="wide-only drawtoggle"><summary class="btnlink">Show the same connections as a drawing</summary>'
               f'<h3 class="vh" id="c-push-h">What pushes on Elections and what it pushes on</h3>'
               f'<div class="ak-scroll" role="region" tabindex="0" aria-label="What pushes on Elections, drawing" style="--ak-min:1312px">{neighborhood_svg()}</div>'
               f'<p class="ak-readout t-cap" data-ak-readout>Point at, tab to or tap a line or a box to read its record.</p></details>',
               foot=f'Part C · {len(ins)} in, {len(outs)} out, {len(inside)} inside')
    # 02.3 loops
    fin = (f'{nw(len(through)).capitalize()} loops run through Elections. ' + ' and '.join(f'{node_label(v)} ({v})' for v in busiest)
           + f' {"sits" if len(busiest) == 1 else "each sit"} on {nw(top)} of them, more than any other condition here.')
    b4, r10 = LOOPS['B4'], LOOPS['R10']
    meet = (f'Two loops meet at {node_label("C3").lower()} (C3): the {low(b4["plain_name"])} (B4), which pushes back, and the {low(r10["plain_name"])} (R10), which feeds itself. '
            + sentences(b4['qualification'])[0].replace('The loop', f'The {low(b4["plain_name"])}', 1) + f' R10 starts from {node_label("C1").lower()} (C1).')
    p3 = plate('c-loops', '02.3', 'Loops that run through it', f'<p>{e(fin)}</p><p>{e(meet)}</p>',
               '<div class="lcards">' + ''.join(loop_card(k) for k in through) + '</div>')
    # 02.4 issues
    rows = []
    for i in sorted(iss, key=lambda i: i['id']):
        cv = [n for n in i['nodes'] if n in C]
        g = issue_grade(i['grade'])
        pe, fe = i.get('problem_example') or {}, i.get('fix_example') or {}
        ex = pe.get('headline') or 'No example in V7'

        def exhtml(x, label):
            if not x:
                return ''
            src = x.get('source') or {}
            s_ = f' <span class="muted">Source: {e(src.get("publisher") or "")}{", " + e(src.get("year")) if src.get("year") else ""}.</span>' if src else ''
            wh = f' <span class="muted">{e(x.get("where") or "")}, {e(x.get("when") or "")}.</span>' if x.get('where') else ''
            return f'<div class="ix"><p class="t-eyebrow">{label}</p><p><b>{e(x["headline"])}</b>{wh}</p><p>{e(x["text"])}{s_}</p></div>'
        ar = i.get('aimed_reforms') or []
        rows.append(f'<li data-vars="{" ".join(cv)}"><details class="issue" data-issue="{i["id"]}" data-name="{e(i["title"])}">'
                    f'<summary><span class="i-id code">{i["id"]}</span><span class="i-title">{e(i["title"])}</span>'
                    f'<span class="i-vars t-note">{" ".join(cv)}</span><span class="i-grade t-note">{tex_swatch(g, 28)} {grade_word(g)}</span>'
                    f'<span class="i-ex t-note muted">{e(ex)}</span></summary>'
                    f'<div class="i-body t-ptext"><p>{e(i["summary"])}</p><div class="ixs">{exhtml(pe, "Where it happened")}{exhtml(fe, "A fix tried elsewhere")}</div>'
                    f'<dl class="t-cap"><div><dt>Evidence</dt><dd>{e(i.get("evidence_note") or "")}</dd></div>'
                    f'<div><dt>Proposed response</dt><dd>{e(i.get("response") or "")}' + (f' <span class="muted">({e(i["actor"])})</span>' if i.get('actor') else '') + '</dd></div>'
                    f'<div><dt>Tradeoff</dt><dd>{e(i.get("tradeoff") or "")}</dd></div><div><dt>How to tell it works</dt><dd>{e(i.get("success_measure") or "")}</dd></div>'
                    + (f'<div><dt>Reforms aimed at it</dt><dd><ul class="ar">' + ''.join(f'<li><b>{a["id"]}</b> {e(a["why"])}' + (f' <span class="ar-d"><b>Disclosure.</b> {e(REFORMS[a["id"]]["disclosure"])}</span>' if REFORMS[a['id']].get('disclosure') else '') + '</li>' for a in ar) + '</ul></dd></div>' if ar else '')
                    + '</dl></div></details></li>')
    filt = (f'<div class="filters" data-filter-group="c-issue-list" role="group" aria-label="Show issues on one condition">'
            f'<button type="button" class="ak-btn" data-filter="all" aria-pressed="true">All {len(iss)}</button>'
            + ''.join(f'<button type="button" class="ak-btn" data-filter="{v}" aria-pressed="false">{e(node_label(v))} <span class="fcode">{v}</span> {len(issues_on([v]))}</button>' for v in C)
            + f'<p class="t-note muted" aria-live="polite">Showing <span id="c-issue-list-n">{len(iss)}</span></p></div>')
    head_row = '<div class="ihead t-note" aria-hidden="true"><span>ID</span><span>Issue</span><span>On</span><span>Evidence</span><span>Real-world example</span></div>'
    p4 = plate('c-issues', '02.4', 'Issues tracked here',
               f'<p>{len(iss)} active issue records touch C1 to C5. Each names a problem in plain words, grades its evidence and gives a real place where it happened. Open any row for the full record.</p>',
               filt + head_row + f'<ol class="issues" id="c-issue-list">{"".join(rows)}</ol>')
    # 02.5 reforms
    rc = []
    for r in sorted(refs, key=lambda r: r['id']):
        eff = ''.join(f'<li><span>{e(D["families"][fam])}</span><b>{e(effect_words(code))}</b></li>' for fam, code in r['effects'].items())
        tg = ', '.join(f'{t} {e(node_label(t) if t in NODES else LINKS[t]["name"])}' for t in r['targets'])
        link = '<p class="t-cap"><a class="tlink" href="#reform-r01">Open the full reform, sheet 04</a></p>' if r['id'] == 'R-01' else ''
        rc.append(f'<article class="rcard" data-reform="{r["id"]}" data-targets="{" ".join(r["targets"])}">'
                  f'<p>{chip("Reform", r["id"], compact=True)}</p><h3 class="t-phead" data-reform="{r["id"]}" data-name="{e(r["title"])}">{e(r["title"])}</h3>'
                  f'<p class="t-cap">{e(sentences(r["summary"])[0])}</p>'
                  f'<p class="t-note rc-t"><span class="t-eyebrow">Aims at</span> {tg}</p>'
                  f'<p class="t-eyebrow rc-e">Expected effects, never added together</p><ul class="effects t-note">{eff}</ul>'
                  f'<details class="rc-more"><summary class="t-note">What it changes</summary><p class="t-cap">{e(r["what_it_changes"])}</p></details>{link}'
                  + (f'<p class="t-note rc-disc"><b>Disclosure.</b> {e(r["disclosure"])}</p>' if r.get('disclosure') else '') + '</article>')
    p5 = plate('c-reforms', '02.5', 'Reforms aimed here',
               f'<p>{len(refs)} reforms aim at a condition in Elections or at a connection that touches one. Each card says what it would change. Effects are rated family by family and never summed.</p>',
               f'<div class="rcards">{"".join(rc)}</div>')
    return (f'<section data-view-root="area-c" data-crumb="Elections" data-parent="overview" aria-labelledby="h-area-c">'
            f'{head}{p1}{p2}{p3}{p4}{p5}</section>')


# ------------------------------------------------------------------------------------------- 04 reform R-01
SCALE = ['-M', '-S', '0', '+S', '+M', '+L']
FEAS = ['very low', 'low', 'medium', 'high']


def scale_svg(code):
    """An ordinal scale of six cells, the rated cell filled. Categorical: nothing is added up."""
    lead = effect_lead(code)
    cells = []
    for i, c in enumerate(SCALE):
        on = c == lead
        cells.append(f'<rect x="{i * 26 + 0.5}" y="0.5" width="23" height="15" class="{"sc-on" if on else "sc-off"}"/>')
    return f'<svg class="scale" width="{len(SCALE) * 26}" height="16" viewBox="0 0 {len(SCALE) * 26} 16" aria-hidden="true">{"".join(cells)}</svg>'


def scale_head():
    labs = ''.join(f'<span>{c.replace("-", MINUS)}</span>' for c in SCALE)
    return f'<span class="scale-head t-note" aria-hidden="true">{labs}</span>'


def feas_svg(level):
    n = FEAS.index(level) + 1
    cells = ''.join(f'<rect x="{i * 18 + 0.5}" y="0.5" width="15" height="11" class="{"sc-on" if i < n else "sc-off"}"/>' for i in range(4))
    return f'<svg class="scale" width="72" height="12" viewBox="0 0 72 12" aria-hidden="true">{cells}</svg>'


def view_reform_r01():
    rid = 'R-01'
    R = REFORMS[rid]
    L = LOOPS['R10']
    icon = acc.icon_svg(rid, 'black', uid='r01-head', size=64)
    nopos = [x for x in sentences(R['summary']) if x.startswith('The Atlas takes no position')]
    case = ' '.join(x for x in sentences(R['summary']) if x not in nopos)
    deck = (f'<p class="loop-id"><span class="h-icon">{icon}</span>{chip("Reform", rid)} <span data-reform="{rid}" data-targets="{" ".join(R["targets"])}">aims at {", ".join(R["targets"])}</span> · band: {e(R["band"])}</p>'
            f'<p>{e(case)}</p>')
    stand = (f'<div class="stand" role="note" aria-labelledby="r01-stand-h"><p class="t-eyebrow" id="r01-stand-h">Where the atlas stands</p>'
             + ''.join(f'<p class="t-ptext"><b>{e(x)}</b></p>' for x in nopos)
             + f'<p class="t-ptext"><b>Disclosure.</b> {e(DISCLOSURE)}</p></div>')
    side = stand + toc([('r01-problem', '04.1', 'The problem it answers'), ('r01-where', '04.2', 'Where it acts'), ('r01-change', '04.3', 'What it changes'),
                ('r01-effects', '04.4', 'Expected effects'), ('r01-routes', '04.5', 'Routes and who can act'), ('r01-evidence', '04.6', 'Evidence'),
                ('r01-risks', '04.7', 'Tradeoffs and risks'), ('r01-status', '04.8', 'Status and disclosure')])
    head = sheet_head('reform-r01', f'Reform {rid} · aimed at the safe-seat loop',
                      f'<span data-reform="{rid}" data-name="{e(R["title"])}">{e(R["title"])}</span>', deck, side, here={'C'})
    # 04.1 the problem
    aimed = [i for i in sorted(ISSUES.values(), key=lambda i: i['id']) if not i.get('retired') and any(a['id'] == rid for a in (i.get('aimed_reforms') or []))]
    pe = R['problem_evidence']
    iss_html = ''.join(
        f'<div class="ix" data-issue="{i["id"]}" data-name="{e(i["title"])}"><p class="t-eyebrow">Issue {i["id"]}' + (f' · example from {e(i["problem_example"]["when"])}' if i.get('problem_example') else '') + '</p>'
        f'<p><b>{e(i["title"])}</b></p><p class="t-cap">{e(i["summary"])}</p>'
        + (f'<p class="t-cap"><b>{e(i["problem_example"]["headline"])}.</b> {e(i["problem_example"]["text"])}</p>' if i.get('problem_example') else '')
        + f'<p class="t-note muted">Why R-01 answers it: {e(next(a["why"] for a in i["aimed_reforms"] if a["id"] == rid))}</p></div>' for i in aimed)
    pe_year = max(re.findall(r'20[0-9][0-9]', pe['text']))
    ex_years = sorted({i['problem_example']['when'] for i in aimed if i.get('problem_example')})
    p1 = plate('r01-problem', '04.1', 'The problem it answers',
               f'<p>R-01 answers <a href="#loop-r10">loop R10, the safe-seat loop</a>: {e(L["summary"].split(".")[0])}. {nw(len(aimed)).capitalize()} issue records name the same problem. '
               f'The problem evidence counts {pe_year} seats; the issue records quote their own examples, from {", ".join(ex_years)}, so their counts differ.</p>',
               f'<div class="ev2"><div class="evb"><p class="t-eyebrow">Problem evidence, as of {SNAP}</p><p class="evg">{tex_swatch(pe["grade"], 44)} <b>{grade_word(pe["grade"])}</b>: {grade_gloss(pe["grade"])}</p><p class="t-ptext">{e(pe["text"])}</p></div>'
               f'<div class="ixs">{iss_html}</div></div>')
    # 04.2 where it acts
    chain, _ = chain_svg('R10', interactive=True, red_targets=set(R['targets']), view='reform-r01-phone', title_id='r01-where-h')
    loops = ', '.join(f'<a href="{loop_href(k)}">{k} {e(LOOPS[k]["plain_name"])}</a>' for k in R['loops'])
    p2 = plate('r01-where', '04.2', 'Where it acts',
               f'<p>It acts at three named points on the safe-seat loop, drawn in red: the step into the primary, the step out of it, and the primary itself. '
               f'It also sits on {loops}.</p>',
               f'<div class="r10-grid"><div class="r10-draw"><div class="wide-only"><div class="ak-scroll" role="region" tabindex="0" aria-label="Where R-01 acts, drawing" style="--ak-min:{RING_W}px">{ring_svg("R10", view="reform-r01", title_id="r01-where-h")}</div>'
               f'<p class="ak-readout t-cap" data-ak-readout>Point at, tab to or tap a box or a step to read its record.</p></div>'
               f'<div class="narrow-only phone-chain">{chain}<p class="t-cap r01-note">Red marks where R-01 acts: {", ".join(sorted(R["targets"]))}.</p></div></div>'
               f'<aside class="r10-side"><p class="t-ptext">{e(sentences(R["what_it_changes"])[0])} {e(sentences(R["what_it_changes"])[1])}</p>'
               f'<div class="loop-keys">{loop_legend()}</div></aside></div>',
               foot=f'Reform {rid} · targets {", ".join(R["targets"])} · loops {", ".join(R["loops"])}')
    # 04.3 what it changes
    p3 = plate('r01-change', '04.3', 'What it changes', '',
               f'<div class="notes n2">{note_block("What it changes", f"<p>{e(R['what_it_changes'])}</p>")}'
               f'{note_block("How it would be put in place", f"<p>{e(R['implementation'])}</p>")}'
               f'{note_block("What it costs", f"<p>{e(R['costs'])}</p>")}</div>')
    # 04.4 effects
    rows = ''.join(f'<li><span class="ef-f">{e(D["families"][fam])}</span>{scale_svg(code)}<b class="ef-w">{e(effect_words(code))}</b></li>' for fam, code in R['effects'].items())
    p4 = plate('r01-effects', '04.4', 'Expected effects, family by family',
               '<p>Each outcome family is rated on its own scale, from moderate negative on the left to large positive on the right. The four ratings are never added together.</p>',
               f'<div class="effgrid"><div class="ef-head t-note"><span>Outcome family</span><span>Scale</span><span>Rating</span></div><ul class="eff">{rows}</ul>'
               f'<p class="t-cap muted">Confidence in these ratings: {e(R["effects_confidence"])}.</p></div>')
    # 04.5 routes
    rrows = []
    for r in R['routes']:
        chk = f'Checked {date_words(r["checked"])}' if r['checked'] else 'No check date in V7'
        rrows.append(f'<tr><th scope="row"><span class="code">{r["route"]}</span> {e(D["route_names"][r["route"]])}</th><td>{e(r["who"])}</td>'
                     f'<td class="fz">{feas_svg(r["feasibility"])} <b>{e(r["feasibility"])}</b><span class="t-note muted">{e(D["feasibility_scale"][r["feasibility"]])}</span></td>'
                     f'<td>{e(r["note"] or "")}</td><td class="t-note">{chk}</td></tr>')
    p5 = plate('r01-routes', '04.5', 'Routes and who can act',
               f'<p>{e(sentences(R["who_decides"])[0])}</p>',
               f'<table class="routes t-cap"><thead><tr><th scope="col">Route</th><th scope="col">Who acts</th><th scope="col">Feasibility, 2026 to 2030</th><th scope="col">Note</th><th scope="col">Checked</th></tr></thead>'
               f'<tbody>{"".join(rrows)}</tbody></table>'
               f'<div class="notes n2">{note_block("Who decides", f"<p>{e(R['who_decides'])}</p>")}'
               f'{note_block("The law", f"<p>{e(R['legal_authority'])}</p>")}</div>')
    # 04.6 evidence
    re_ = R['remedy_evidence']
    p6 = plate('r01-evidence', '04.6', 'Evidence for the problem and for the remedy',
               '<p>The atlas grades the problem and the remedy separately. A well-evidenced problem can have an unproven fix.</p>',
               f'<div class="ev2 even"><div class="evb"><p class="t-eyebrow">The problem</p><p class="evg">{tex_swatch(pe["grade"], 44)} <b>{grade_word(pe["grade"])}</b>: {grade_gloss(pe["grade"])}</p><p class="t-ptext">{e(pe["text"])}</p></div>'
               f'<div class="evb"><p class="t-eyebrow">The remedy</p><p class="evg">{tex_swatch(re_["grade"], 44)} <b>{grade_word(re_["grade"])}</b>: {grade_gloss(re_["grade"])}</p><p class="t-ptext">{e(re_["text"])}</p></div></div>')
    # 04.7 risks
    sm = ''.join(f'<li>{e(x)}</li>' for x in R['success_measures'])
    comp = ', '.join(f'{c} {e(REFORMS[c]["title"])}' for c in R['complements'])
    p7 = plate('r01-risks', '04.7', 'Tradeoffs, risks and how to tell it works', '',
               f'<div class="notes">{note_block("Tradeoffs", f"<p>{e(R['tradeoffs'])}</p>")}'
               f'{note_block("How it could fail", f"<p>{e(R['failure_risks'])}</p>")}'
               f'{note_block("How to tell it works", f"<ul>{sm}</ul>")}'
               f'{note_block("Other options", f"<p>{e(R['alternatives'])}</p>")}'
               f'{note_block("Works alongside", f"<p>{comp}.</p>")}</div>')
    # 04.8 status and disclosure
    st = R['status']
    p8 = plate('r01-status', '04.8', 'Status and disclosure', '',
               f'<div class="status"><p class="t-eyebrow">Status, checked {date_words(st["checked"])}</p><p class="t-body">{e(st["text"])}</p>'
               f'<p class="t-cap muted">Sources in V7: {", ".join(st["sources"])}.</p>'
               f'<div class="disclose"><p class="t-eyebrow">Where the atlas stands</p>' + ''.join(f'<p class="t-body">{e(x)}</p>' for x in nopos)
               + f'<p class="t-body"><b>Disclosure.</b> {e(DISCLOSURE)}</p></div></div>')
    return (f'<section data-view-root="reform-r01" data-crumb="Reform R-01" data-parent="overview" aria-labelledby="h-reform-r01">'
            f'{head}{p1}{p2}{p3}{p4}{p5}{p6}{p7}{p8}</section>')


# ------------------------------------------------------------------------------------------- 05 the loop catalog
def view_loops():
    n_r = sum(1 for l in LOOPS.values() if l['type'] == 'R')
    n_b = sum(1 for l in LOOPS.values() if l['type'] == 'B')
    n_sk = sum(1 for l in LOOPS.values() if l['conceptual'])
    n_hy = sum(1 for l in LOOPS.values() if l['hypothesized'])
    n_rf = sum(1 for l in LOOPS.values() if l['reforms'])
    groups = [(p, loops_home(p)) for p in CORE] + [(None, [k for k in D['loop_order'] if LOOPS[k]['home'] is None])]
    groups = [(p, ks) for p, ks in groups if ks]
    deck = (f'<p>A loop is a chain of causes that returns to where it started. {cnt("loops_reinforcing", n_r)} of the {cnt("loops", len(LOOPS))} feed themselves, '
            f'so a change comes back stronger, and {cnt("loops_balancing", n_b)} push back. <span class="t-quote">“{e(IMPROVE)}”</span></p>'
            f'<p>Every card draws its loop as boxes and arrows, read from the top; the return step closes it at the bottom. {nw(n_hy).capitalize()} loops close only through an untested step, and '
            f'{cnt("loops_sketched", n_sk)} are sketches with no numbered chain. <span data-count="custom:loops with a reform">{n_rf}</span> of the {len(LOOPS)} have at least one reform aimed at them.</p>')
    idx = []
    for p, ks in groups:
        title = f'{part_name(p)}' if p else 'Sketches'
        idx.append(f'<div class="lidx-g"><p class="t-eyebrow">{e(title)}</p><ol>' + ''.join(
            f'<li><a href="#lc-{k.lower()}" data-toc><span class="code">{k}</span> {e(LOOPS[k]["plain_name"])}</a></li>' for k in ks) + '</ol></div>')
    side = (f'<nav class="toc" aria-label="Loops on this sheet"><p class="t-eyebrow">Index of loops</p><div class="lidx">{"".join(idx)}</div></nav>')
    head = sheet_head('loops', 'The loop catalog', f'Of {len(LOOPS)} loops, {n_r} feed themselves and {n_b} push back.', deck, evidence_key(hollow=True), here=set(CORE))
    head += f'<nav class="lindex" aria-label="Index of loops"><p class="t-eyebrow">Index of loops</p><div class="lidx">{"".join(idx)}</div></nav>'
    body = []
    for p, ks in groups:
        if p:
            P_ = PARTS[p]
            kr = sum(1 for k in ks if LOOPS[k]['type'] == 'R')
            kb = len(ks) - kr
            mix = ', '.join(x for x in [f'{nw(kr)} reinforcing' if kr else '', f'{nw(kb)} balancing' if kb else ''] if x)
            gh = (f'<header class="lg-head"><p class="t-eyebrow">Based in part {p}</p><h2 class="t-head"><span data-part="{p}" data-name="{e(P_["plain_name"])}">{e(P_["plain_name"])}</span></h2>'
                  f'<p class="t-cap muted"><span data-part="{p}" data-name="{e(P_["formal_title"])}">{e(P_["formal_title"])}</span>. {e(P_["text"])} {mix.capitalize()}.</p></header>')
        else:
            gh = (f'<header class="lg-head"><p class="t-eyebrow">No home part</p><h2 class="t-head">Sketches</h2>'
                  f'<p class="t-cap muted">These loops have no complete numbered chain. Their stations are ideas the atlas has not yet modelled as variables, so the lines are drawn hollow.</p></header>')
        cards = ''.join(f'<div id="lc-{k.lower()}" class="lc-wrap">{loop_card(k, level="h3")}</div>' for k in ks)
        body.append(f'<section class="lgroup">{gh}<div class="lcards">{cards}</div></section>')
    return (f'<section data-view-root="loops" data-crumb="All loops" data-parent="overview" aria-labelledby="h-loops">{head}'
            f'<div class="catalog" data-strip="loops">{"".join(body)}</div></section>')


# ------------------------------------------------------------------------------------------- 00 how to read
def spec_line(kind, w=140, sign=None, tex='solid', delay=None, head='arrow', red_on=False):
    """One specimen line at actual size: the conventions sheet draws every mark the way the sheets do."""
    H = 44
    y = 26
    pts = [(4, y), (w - 6, y)]
    body = wire(pts, w=2, tex=tex, head=head, n_ticks=DELAY_N[delay] if delay else 0, hollow=(kind == 'hollow'))
    g = sign_glyph(w - 22, y - 16, sign, r=8) if sign else ''
    rm = ''
    if red_on:
        rm = red(bracket_h(w / 2 - 16, w / 2 + 16, y, side=1, depth=10))
    return (f'<svg class="draw spec-svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" aria-hidden="true">'
            f'<g class="st">{body}</g>{g}{rm}</svg>')


def view_how_to_read():
    grades = ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis']
    gcount = {g: sum(1 for l in LINKS.values() if l['evidence'] == g) for g in grades}
    dcount = {d: sum(1 for l in LINKS.values() if l['delay'] == d) for d in 'SML'}
    auth = [l for l in LINKS.values() if l['type'] == 'authority']
    deck = ('<p>Every sheet in this atlas uses one small set of marks. A box is a condition that can rise or fall. An arrow says that one '
            'condition raises or lowers another. The rest of the marks say how sure the atlas is, how long the effect takes and where a reform would act.</p>')
    side = toc([('h-effect', '00.1', 'The tip is the effect'), ('h-evidence', '00.2', 'Texture is the evidence'), ('h-time', '00.3', 'Ticks count the wait'),
                ('h-loops', '00.4', 'Loops have a character'), ('h-layer', '00.5', 'Color is the layer'), ('h-reform', '00.6', 'Red marks a reform'),
                ('h-card', '00.7', 'How to read a card'), ('h-words', '00.8', 'Words on these sheets')])
    head = sheet_head('how-to-read', 'The conventions sheet', 'Every mark on these sheets makes one claim.', deck, side, here=set())
    l08, l25, le = LINKS['L08'], LINKS['L25'], auth[0]

    def row(svg, title, text, ex=''):
        return f'<li class="conv"><div class="cv-mark">{svg}</div><div class="cv-t"><p class="t-eyebrow">{title}</p><p class="t-ptext">{text}</p>{ex}</div></li>'
    p1 = plate('h-effect', '00.1', 'The tip is the effect',
               f'<p>An arrow runs from the condition that changes to the condition it moves. {e(sign_rule())}</p>',
               '<ul class="convs">'
               + row(spec_line('a', sign='+'), 'Raises, plus sign', 'If the first condition rises, the second tends to rise too, other things held steady.',
                     f'<p class="t-cap muted">Example: <span {link_attrs("L08")} data-name="{e(l08["name"])}">{e(l08["name"])}</span> ({l08["id"]}).</p>')
               + row(spec_line('a', sign='-'), 'Lowers, minus sign', 'If the first condition rises, the second tends to fall. The minus sign does not mean harm.',
                     f'<p class="t-cap muted">Example: <span {link_attrs("L25")} data-name="{e(l25["name"])}">{e(l25["name"])}</span> ({l25["id"]}).</p>')
               + row(spec_line('a', head='diamond'), 'Decides, open diamond', f'{e(sentences(gloss("Authority connection"))[1])} The atlas has {cnt("authority_connections", len(auth))} of these.',
                     f'<p class="t-cap muted">Example: <span {link_attrs(le["id"])} data-name="{e(le["name"])}">{e(le["name"])}</span> ({le["id"]}).</p>')
               + '</ul>')
    ev_rows = ''
    for g in grades:
        ev_rows += row(spec_line('a', tex=tex_of(g), head=None), f'{grade_word(g)}', f'{grade_gloss(g).capitalize()}. <span class="muted"><span data-count="custom:grade {g}">{gcount[g]}</span> connections.</span>')
    ev_rows += row(spec_line('hollow', head=None), 'Hollow, a conceptual step', f'A step in one of the {nw(sum(1 for l in LOOPS.values() if l["conceptual"]))} sketched loops. It is an idea with no numbered connection.')
    p2 = plate('h-evidence', '00.2', 'Texture is the evidence',
               '<p>A solid line rests on the public record or strong research. Breaks in the line mean weaker evidence, down to dots for a claim nobody has tested. Line weight never shows size.</p>',
               f'<ul class="convs">{ev_rows}</ul>')
    t_rows = ''.join(row(spec_line('a', delay=d), f'{"One tick" if d == "S" else "Two ticks" if d == "M" else "Three ticks"}',
                         f'{delay_words(d).capitalize()}. <span class="muted"><span data-count="custom:delay {d}">{dcount[d]}</span> connections.</span>') for d in 'SML')
    p3 = plate('h-time', '00.3', 'Ticks count the wait', '<p>Ticks sit just after the start of a line. The more ticks, the longer the change takes to arrive.</p>',
               f'<ul class="convs">{t_rows}</ul>')
    r16 = LOOPS['R16']
    hyp = [s['id'] for s in r16['steps'] if s['evidence'] == 'hypothesis'][-1]
    p4 = plate('h-loops', '00.4', 'Loops have a character',
               f'<p>Multiply the signs around a loop. An even number of lowering steps makes it reinforcing: a change comes back stronger. An odd number makes it balancing: the loop pushes back. '
               f'<span class="t-quote">“{e(IMPROVE)}”</span></p>',
               '<div class="lcards">' + loop_card('R8') + loop_card('B4')
               + f'<div class="lcard untested"><p class="t-eyebrow">Make the untested step visible</p><p class="t-head unt-h">The loop closes only if {hyp} holds.</p>'
               + f'<p class="t-cap">Loop R16, the {e(low(r16["plain_name"]))}. {e(closure_note("R16"))}</p>' + chain_svg('R16')[0] + '</div></div>')
    lay = []
    for key, part_ids, cls in [('core', CORE, 'core'), ('economy', ['EC'], 'economy'), ('technology', ['TC'], 'technology')]:
        n = sum(len(PARTS[p]['nodes']) for p in part_ids)
        names = ', '.join(part_name(p) for p in part_ids)
        lay.append(f'<li class="layer lay-{cls}"><p class="t-phead">{e(LAYER_TITLE[key])}</p><p class="t-cap">{e(names)}. <span data-count="custom:layer {key}">{n}</span> conditions.</p></li>')
    nx = len(PARTS['X']['nodes'])
    lay.append(f'<li class="layer lay-open"><p class="t-phead">{e(part_name("X"))}</p><p class="t-cap">{e(PARTS["X"]["formal_title"])}, taken as given: an open frame with no rule. <span data-count="custom:layer X">{nx}</span> conditions.</p></li>')
    p5 = plate('h-layer', '00.5', 'Color is the layer',
               '<p>The rule down the left edge of a box tells you which layer of the system it belongs to. The color only repeats what the name already says, so the sheets read the same in black and white.</p>',
               f'<ul class="layers">{"".join(lay)}</ul>')
    R = REFORMS['R-01']
    rsvg = (f'<svg class="draw spec-svg" width="280" height="96" viewBox="0 0 280 96" aria-hidden="true"><g class="st">{wire([(4, 34), (272, 34)], w=3, tex=tex_of(l25["evidence"]))}'
            + red_wire([(4, 34), (272, 34)], w=3, tex=tex_of(l25['evidence']), kind='specimen') + '</g>'
            + T(4, 16, f'{l25["id"]}, {grade_word(l25["evidence"]).lower()}', 'noteb')
            + T(4, 64, 'R-01 acts on L25', 'noteb') + T(4, 84, 'Another reform: an ink tag, R-02 aims at C3', 'note', cls='muted') + '</svg>')
    p6 = plate('h-reform', '00.6', 'Red marks where a reform acts',
               '<p>A reform aims at named points: a connection, a condition, or both. On the loop and reform sheets, the one working red marks each point where '
               'reform R-01, the worked example, acts: the line and its arrowhead, or the box. An ink tag names each other reform that aims at the loop. '
               'Red does no other job on these sheets. Effects are rated family by family and never added up.</p>',
               f'<div class="conv-wide">{rsvg}<p class="t-cap">On the safe-seat loop, R-01 takes the red on its three targets: {", ".join(sorted(R["targets"]))}. This sample is a specimen.</p></div>')
    # anatomy of a card: the Elections card at actual size, with callouts
    secs = part_card('C', 0, 0, CARD_W)[1]
    card, _ = part_card('C', 0, 0, CARD_W, sec=secs)
    card = re.sub(r'data-select="[^"]+"', '', card).replace('role="button"', '')
    card = card.replace('<a href="#area-c"', '<g data-a="1"').replace('</a>', '</g>').replace('<a href="#reform-r01"', '<g')
    card = re.sub(r'<a href="[^"]+" class="lchip"', '<g class="lchip"', card)
    hc = sum(secs)
    notes = [(34, 'Plain name, then the formal title'), (82, 'The question this part answers'), (110, 'What it is, in one sentence'),
             (secs[0] + 30, 'Every condition, with its code'), (secs[0] + secs[1] + 24, 'What it passes on along the circuit'),
             (sum(secs[:3]) + 24, 'How many connections stay inside'), (sum(secs[:3]) + 48, 'The loops based here')]
    callouts, nums = '', ''
    for i, (yy, t) in enumerate(notes):
        callouts += (f'<path d="M{f(CARD_W - 8)} {f(yy - 4)} H{f(CARD_W + 40)}" class="leader"/>'
                     + T(CARD_W + 48, yy, f'{i + 1}', 'noteb') + T(CARD_W + 66, yy, t, 'cap'))
        nums += f'<path d="M{f(CARD_W - 8)} {f(yy - 4)} H{f(CARD_W + 16)}" class="leader"/>' + T(CARD_W + 22, yy, f'{i + 1}', 'noteb')
    an_svg = (f'<svg class="draw anat" style="width:{f(CARD_W + 350)}px" width="{f(CARD_W + 350)}" height="{f(hc + 2)}" viewBox="0 0 {f(CARD_W + 350)} {f(hc + 2)}" role="img" '
              f'aria-label="The Elections card from sheet 01, with a note on each section.">{card}{callouts}</svg>')
    an_phone = (f'<svg class="draw anat" style="width:{f(CARD_W + 40)}px" width="{f(CARD_W + 40)}" height="{f(hc + 2)}" viewBox="0 0 {f(CARD_W + 40)} {f(hc + 2)}" aria-hidden="true">'
                + card.replace('id="', 'id="ph-') + nums + '</svg>')
    an_list = '<ol class="anat-list t-cap">' + ''.join(f'<li>{e(t)}</li>' for _, t in notes) + '</ol>'
    p7 = plate('h-card', '00.7', 'How to read a card', '<p>Each part of the system appears on the overview as a card. Every card has the same sections in the same order, so the five read across like a table.</p>',
               f'<div class="wide-only"><div class="anat-wrap">{an_svg}</div></div><div class="narrow-only anat-phone">{an_phone}{an_list}</div>')
    terms = ['Variable', 'Connection', 'Feedback loop', 'Reinforcing loop (R)', 'Balancing loop (B)', 'Outside driver', 'Stock', 'Flow', 'Delay',
             'Documented', 'Well-supported', 'Plausible', 'Contested', 'Hypothesis', 'Reform profile', 'Problem evidence', 'Remedy evidence', 'Feasibility']
    gl = ''.join(f'<div><dt>{e(t)}</dt><dd>{e(gloss(t))}</dd></div>' for t in terms)
    p8 = plate('h-words', '00.8', 'Words on these sheets', '', f'<dl class="gloss t-ptext">{gl}</dl>')
    return (f'<section data-view-root="how-to-read" data-crumb="How to read" data-parent="overview" aria-labelledby="h-how-to-read">'
            f'{head}{p1}{p2}{p3}{p4}{p5}{p6}{p7}{p8}</section>')


# ------------------------------------------------------------------------------------------- run
if __name__ == '__main__':
    main()
