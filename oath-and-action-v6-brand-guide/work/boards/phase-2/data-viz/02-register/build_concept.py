"""Build chart-system concept 02, Register, for the data visualization round (November 6, 2026).

Register leads with the numbers. Every specimen sits in one frame (rule, evidence label, title, measure line, figure,
notes, source, table), and every figure keeps a register: the numbers a reader would look up, set as a table with
tabular figures, true minus signs, aligned decimals, quiet rules and a sort order that answers the question.
Prussian and Verdigris carry the data, Stone carries context and Charcoal carries the subject the title names.

Every mark, number and word of data is read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json
(and the tile grid from shared/geo/). Every chart and table comes from a generator function below, so a new
dataset drops into the same frame. Titles are studio drafts.

Run from the project root:
    python3 -I work/boards/phase-2/data-viz/02-register/build_concept.py
Writes 20261106_Data-Viz-02-Register.html beside this file.
"""
import functools
import html
import json
import math
import pathlib
import re
from collections import Counter, defaultdict

import numpy as np
from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SHARED = ROOT / 'work/boards/phase-2/data-viz/shared'
D = json.loads((SHARED / '20261106_Chart-Data.json').read_text())
LAB = json.loads((SHARED / '20261106_Palette-Lab.json').read_text())
TILES = json.loads((SHARED / 'geo/us-state-tile-grid.json').read_text())
OUT = HERE / '20261106_Data-Viz-02-Register.html'
DS = D['datasets']
SPEC = {s['id']: s for s in D['specimens']}
MINUS = '−'
VIEWS = [('white', 'White'), ('newsprint', 'Newsprint'), ('dark', 'Charcoal'), ('social', 'Social card'), ('system', 'System')]

for _did, _ds in DS.items():
    assert not _ds.get('pending'), f'{_did} is still pending in the shared data'


# One set of chart values, read by the generators, the CSS and the system sheet (F16).
CHART_TOKENS = {
    'artboards': [866, 560, 358, 328],     # wide; medium; the 390 px phone's column; the 360 px phone's column
    'line': {'hair': 1, 'context': 1.5, 'series': 3, 'select': 6},   # the 1, 1.5, 2, 3 and 6 px family (D2-60)
    'radius': {'point': 3, 'point_named': 5.5, 'dumbbell': 6, 'event': 4.5, 'event_strip': 3.5},
    'unit': 14, 'unit_gap': 2, 'unit_phone': 12,
    'bar_h': 12, 'bar_seg_gap': 1, 'bar_unit_gap': 2,
    'tile': 40, 'tile_gap': 4,
    'leader_max': 120, 'label_headroom': 1.15,
    'note_px': 540, 'measure_px': 620, 'source_px': 540,
    'title': (28, 32), 'title_phone': (22, 27), 'label': 13, 'direct_label': 15,
}
T = CHART_TOKENS
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
NBSP = ' '


def iso_to_words(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return f'{MONTHS[m - 1]}{NBSP}{d},{NBSP}{y}'


def typo(s):
    """The one copy function: curly quotes and apostrophes, ISO dates in words, no break inside a date, true minus."""
    s = re.sub(r'\b(\d{4})-(\d{2})-(\d{2})\b', lambda m: iso_to_words(m.group(0)), s)
    s = re.sub(r'\b(' + '|'.join(MONTHS) + r') (\d{1,2}), (\d{4})', lambda m: f'{m.group(1)}{NBSP}{m.group(2)},{NBSP}{m.group(3)}', s)
    s = re.sub(r"(?<=\w)'(?=\w)", '’', s)
    s = re.sub(r"(?<![\w'])'(?=\d\d\b)", '’', s)
    s = re.sub(r'(^|[\s(\[ ])"', lambda m: m.group(1) + '“', s)
    s = s.replace('"', '”')
    s = re.sub(r"(^|[\s(\[ ])'", lambda m: m.group(1) + '‘', s)
    s = s.replace("'", '’')
    s = re.sub(r'(?<=[\s(])-(?=\d)', MINUS, s)
    return s


def typo_html(page):
    """Run typo() over every text node of the page; tags, attributes, scripts and styles stay as written."""
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', page, flags=re.S)
    for i in range(0, len(parts), 2):
        if parts[i]:
            parts[i] = html.escape(typo(html.unescape(parts[i])), quote=False)
    return ''.join(parts)


def rows(did):
    return DS[did]['rows']


def byk(did):
    return {r['key']: r for r in rows(did)}


def e(s):
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------------------------------------------ numbers
def num(v, d=0):
    """A figure with thousands separators and a true minus sign."""
    s = f'{abs(v):,.{d}f}'
    return (MINUS + s) if v < 0 and float(s.replace(',', '')) != 0 else s


def signed(v, d=1):
    s = f'{abs(v):,.{d}f}'
    if float(s) == 0:
        return s
    return ('+' if v > 0 else MINUS) + s


WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'}


def date_words(iso):
    y, m, d = iso.split('-')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return f'{months[int(m) - 1]} {int(d)}, {y}'


def dyear(iso):
    """A date as a decimal year, for a true time scale."""
    y, m, d = (int(x) for x in iso.split('-'))
    import datetime
    a = datetime.date(y, 1, 1)
    b = datetime.date(y + 1, 1, 1)
    return y + (datetime.date(y, m, d) - a).days / (b - a).days


# ------------------------------------------------------------------------------------------------ color
def _hex(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _delin(c):
    c = min(1.0, max(0.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)


def _to_oklab(rgb_lin):
    r, g, b = rgb_lin
    l = _cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = _cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = _cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklab(h):
    return _to_oklab([_lin(c) for c in _hex(h)])


def from_oklab(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return '#' + ''.join(f'{round(_delin(c) * 255):02X}' for c in rgb)


def mix(h1, h2, t):
    """Mix two colors in OKLab (D1-04): t = 0 gives h1, t = 1 gives h2."""
    a, b = oklab(h1), oklab(h2)
    return from_oklab(*[x + (y - x) * t for x, y in zip(a, b)])


def lum(h):
    r, g, b = [_lin(c) for c in _hex(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


CVD = {  # Machado, Oliveira and Fernandes (2009), severity 1.0, applied to linear RGB
    'deuteranopia': ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    'protanopia': ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    'tritanopia': ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def delta_e(h1, h2, sim=None):
    def lab(h):
        c = [_lin(x) for x in _hex(h)]
        if sim:
            M = CVD[sim]
            c = [max(0.0, min(1.0, sum(M[i][j] * c[j] for j in range(3)))) for i in range(3)]
        return _to_oklab(c)
    a, b = lab(h1), lab(h2)
    return math.dist(a, b)


def gray(h):
    """The grayscale proof of a color: its OKLab lightness with no chroma."""
    return from_oklab(oklab(h)[0], 0, 0)


LOCK = {'white': '#FFFFFF', 'newsprint': '#DCD9D2', 'charcoal': '#121212', 'red': '#E63946', 'prussian': '#1F2D5A',
        'stone': '#5D636D', 'verdigris': '#4A7C74'}
DEEP = '#4E535B'


def lab_set(name, ground):
    s = next(x for x in LAB['sets'] if x['name'].startswith(name) and x['ground'] == ground)
    return [w['hex'] for w in s['swatches']]


# Grounds. Lab values where the palette lab measured them; Register's own tints are mixed in OKLab and named.
def ground_tokens(gname):
    if gname in ('white', 'newsprint'):
        bg = LOCK[gname]
        roles = lab_set('Roles', gname)
        seqv = lab_set('Sequential Verdigris', gname)
        seqp = lab_set('Sequential Prussian', gname)
        divb = lab_set('Diverging B', gname)
        diva = lab_set('Diverging A', gname)
        grades = lab_set('Evidence grade ramp', gname)
        t = {
            'bg': bg, 'ink': LOCK['charcoal'], 'sec': DEEP, 'ctx': LOCK['stone'], 'grid': roles[3],
            'rq': mix(LOCK['stone'], bg, 0.84),            # quiet table rule: Stone 84% toward the ground
            'tow': LOCK['verdigris'], 'awy': LOCK['charcoal'],      # direction: Verdigris squares toward, Charcoal dots away
            'kept': mix(LOCK['stone'], bg, 0.62),          # voters kept the rules: Stone 62% toward the ground
            'some': mix(LOCK['stone'], bg, 0.55),          # map: a ban in some elections
            'g1': grades[0], 'g2': grades[1], 'g3': grades[2], 'g4': grades[3],
            'dv1': divb[4], 'dv2': divb[3], 'dv3': divb[2], 'dv4': divb[1], 'dv5': divb[0],
            'da1': diva[4], 'da2': diva[3], 'da3': diva[2], 'da4': diva[1], 'da5': diva[0],
            'sv': seqv, 'sp': seqp, 'red': LOCK['red'],
            'on': bg,                                      # text on a Charcoal or Prussian mark
        }
    else:
        bg = LOCK['charcoal']
        roles = lab_set('Roles', 'charcoal')
        t = {
            'bg': bg, 'ink': LOCK['newsprint'], 'sec': roles[1], 'ctx': roles[2], 'grid': roles[3],
            'rq': mix(LOCK['newsprint'], bg, 0.80),
            'tow': mix(LOCK['verdigris'], LOCK['newsprint'], 0.04),   # Verdigris lifted 4% toward Newsprint
            'awy': LOCK['newsprint'],                                 # away from voters: Newsprint dots
            'kept': mix(LOCK['newsprint'], bg, 0.62),
            'some': mix(LOCK['newsprint'], bg, 0.55),
            'g1': LOCK['newsprint'], 'g2': mix(LOCK['newsprint'], bg, 0.35), 'g3': mix(LOCK['newsprint'], bg, 0.58),
            'g4': mix(LOCK['newsprint'], bg, 0.76),
            'red': LOCK['red'], 'on': bg,
        }
    return t


G = {'white': ground_tokens('white'), 'newsprint': ground_tokens('newsprint'), 'dark': ground_tokens('charcoal')}
GCLS = {'white': 'g-white', 'newsprint': 'g-news', 'dark': 'g-dark'}

# measured guards: everything that carries meaning clears its threshold on its ground
for _g, _t in G.items():
    assert contrast(_t['sec'], _t['bg']) >= 4.5, _g
    assert contrast(_t['ink'], _t['bg']) >= 4.5, _g
    assert contrast(_t['tow'], _t['bg']) >= 3.0, (_g, _t['tow'], contrast(_t['tow'], _t['bg']))
    assert contrast(_t['awy'], _t['bg']) >= 3.0, _g
    assert abs(oklab(_t['tow'])[0] - oklab(_t['awy'])[0]) >= 0.1, (_g, 'direction pair too close in lightness')
assert mix('#5D636D', '#FFFFFF', 0.70) == '#CBCED1', mix('#5D636D', '#FFFFFF', 0.70)   # our mixer reproduces the lab


def css_vars(t):
    keys = ['bg', 'ink', 'sec', 'ctx', 'grid', 'rq', 'tow', 'awy', 'kept', 'some', 'g1', 'g2', 'g3', 'g4', 'red', 'on']
    out = [f'--{k}:{t[k]}' for k in keys]
    for k in ['dv1', 'dv2', 'dv3', 'dv4', 'dv5']:
        if k in t:
            out.append(f'--{k}:{t[k]}')
    return ';'.join(out)


# ------------------------------------------------------------------------------------------------ text metrics
# Inter is measured from files found by path; the script stops and names the file when none is found (F16).
FONT_DIRS = [HERE / 'fonts', ROOT / 'work/build/assets/fonts/inter', pathlib.Path('/usr/share/fonts/opentype/inter')]
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        for d in FONT_DIRS:
            p = d / f'Inter-{name}.otf'
            if p.exists():
                _FONTS[weight] = ImageFont.truetype(str(p), 200)
                break
        else:
            raise SystemExit(f'Inter-{name}.otf is missing; looked in ' + ', '.join(str(d) for d in FONT_DIRS))
    return _FONTS[weight]


def tw(text, size=13, weight=400):
    """Measured width with headroom for readers who widen text spacing (WCAG 1.4.12)."""
    return _font(weight).getlength(text) * size / 200 * T['label_headroom']


def wrap(text, width, size=13, weight=400):
    words = []
    for word in text.split():
        if tw(word, size, weight) > width and '-' in word:
            parts = word.split('-')
            words += [x + '-' for x in parts[:-1]] + [parts[-1]]
        else:
            words.append(word)
    out, line = [], ''
    for word in words:
        trial = (line + word) if line.endswith('-') else (line + ' ' + word).strip()
        if line and tw(trial, size, weight) > width:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def txt(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{s}</text>'


def lines(x, y, rows_, cls, lh, anchor='start'):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    t = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows_))
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}>{t}</text>'


SVG_TYPE = {'tk': (13, 400), 'th': (13, 600), 'lab': (15, 600), 'lab-s': (13, 600), 'lab-ctx': (15, 600), 'lab-b': (15, 700),
            'nt': (13, 400), 'nt-b': (13, 600), 'num': (15, 400), 'num-b': (15, 700), 'yr': (13, 700), 'ev': (13, 400),
            'tc': (13, 600), 'ty': (13, 400)}
GUARD_LINES = {'lead', 'base', 'lane', 'comb', 'brk', 'db', 'db-ctx', 'ln-main', 'ln-ctx', 'ln-sm', 'rq'}


def guard(body, W, H, view):
    """Layout guard: no label leaves the drawing, overlaps another label, or is crossed by a line, rule or leader
    (gridlines pass under a ground-colored halo). A drawing that fails does not build (F18)."""
    boxes = []
    for m in re.finditer(r'<text x="([\d.-]+)" y="([\d.-]+)" class="([\w-]+)"(?: text-anchor="(\w+)")?[^>]*>(.*?)</text>', body, re.S):
        x, y, cls, anc, inner = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4) or 'start', m.group(5)
        size, wt = SVG_TYPE.get(cls, (13, 400))
        spans = re.findall(r'<tspan x="([\d.-]+)" dy="([\d.-]+)">(.*?)</tspan>', inner) or [(str(x), '0', inner)]
        yy = y
        for sx, dy, s in spans:
            yy += float(dy)
            t_ = html.unescape(re.sub(r'<[^>]+>', '', s))
            w = tw(t_, size, wt) / T['label_headroom']
            x0 = float(sx) - (w if anc == 'end' else w / 2 if anc == 'middle' else 0)
            boxes.append((x0 + 1, yy - 0.72 * size + 1, x0 + w - 1, yy + 0.2 * size - 1, t_))
    errs = []
    for b in boxes:
        if b[0] < -1 or b[2] > W + 1 or b[1] < -1 or b[3] > H + 1:
            errs.append(f'outside: {b[4]}')
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                errs.append(f'overlap: {a[4]} / {b[4]}')
    segs = []
    for m in re.finditer(r'<line class="([\w-]+)" x1="([\d.-]+)"(?: y1="([\d.-]+)" x2="([\d.-]+)"| x2="([\d.-]+)" y1="([\d.-]+)") y2="([\d.-]+)"', body):
        cls = m.group(1)
        if m.group(3) is not None:
            x1, y1, x2, y2 = float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(7))
        else:
            x1, x2, y1, y2 = float(m.group(2)), float(m.group(5)), float(m.group(6)), float(m.group(7))
        segs.append((cls, x1, y1, x2, y2))
    for m in re.finditer(r'<path class="([\w-]+)"[^>]* d="([^"]+)"', body):
        cls, d = m.group(1), m.group(2)
        pts, cur = [], None
        for cmd, a1, a2 in re.findall(r'([MLHV])\s*([\d.-]+)(?:[ ,]([\d.-]+))?', d):
            if cmd in 'ML':
                cur = (float(a1), float(a2))
            elif cmd == 'H':
                cur = (float(a1), cur[1])
            else:
                cur = (cur[0], float(a1))
            if cmd == 'M' and pts:
                for p_, q_ in zip(pts, pts[1:]):
                    segs.append((cls, *p_, *q_))
                pts = []
            pts.append(cur)
        for p_, q_ in zip(pts, pts[1:]):
            segs.append((cls, *p_, *q_))
    for cls, x1, y1, x2, y2 in segs:
        if cls not in GUARD_LINES:
            continue
        n = int(max(abs(x2 - x1), abs(y2 - y1))) + 1
        for b in boxes:
            if max(x1, x2) < b[0] or min(x1, x2) > b[2] or max(y1, y2) < b[1] or min(y1, y2) > b[3]:
                continue
            if any(b[0] <= x1 + (x2 - x1) * k / n <= b[2] and b[1] <= y1 + (y2 - y1) * k / n <= b[3] for k in range(n + 1)):
                errs.append(f'{cls} line crosses "{b[4]}"')
                break
    if errs:
        raise SystemExit(f'layout guard, {view}: ' + '; '.join(sorted(set(errs))[:12]))


def tab_digits(body):
    """Tabular figures on runs of digits only, so a hyphen inside a word keeps its width (F18)."""
    out, depth = [], 0
    for part in re.split(r'(<[^>]+>)', body):
        if part.startswith('<'):
            if re.match(r'<text\b', part):
                depth += 1
            elif part.startswith('</text'):
                depth -= 1
            out.append(part)
        elif depth and re.search(r'\d', part):
            out.append(re.sub(r'&#?\w+;|\d(?:[\d,.:]*\d)?',
                              lambda m: m.group(0) if m.group(0).startswith('&') else f'<tspan class="d">{m.group(0)}</tspan>', part))
        else:
            out.append(part)
    return ''.join(out)


def svg(W, H, view, label, body, cls='ab', check=True):
    if check:
        guard(body, W, H, view)
    body = tab_digits(body)
    return (f'<svg class="{cls}" data-view="{view}" viewBox="0 0 {f(W)} {f(H)}" width="{f(W)}" height="{f(H)}" '
            f'role="img" aria-label="{e(label)}" style="--abw:{f(W)}px">{body}</svg>')


# ------------------------------------------------------------------------------------------------ the frame
def source_text(did, drop=()):
    """The dataset's source line, shortened only by dropping words (never facts)."""
    s = DS[did]['source_line']
    for d in drop:
        assert d in s, d
        s = s.replace(d, '')
    return s if s.startswith('Source:') else 'Source: ' + s


HOWTO = {'white': '#white-howto', 'newsprint': '#newsprint-howto'}


def disclosure_html(did):
    req = DS[did].get('required_text') or []
    return ''.join(f'<p class="fdisc"><b>Disclosure:</b> {e(t_)}</p>' for t_ in req)


def figure(sid, uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls='', sub='', coding=''):
    """The frame every specimen shares: rule, evidence label, title, measure line, figure, notes, the atlas's coding
    rule and the editor's disclosure where the data needs them, source with credit, and the table toggle."""
    if uid.startswith('system-'):
        return anat_figure(sid, uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls, sub, coding)
    sp = SPEC[sid]
    ds = DS[sp['dataset']]
    kind = ds['evidence']
    view = uid.split('-')[0]
    nts = ''.join(f'<li>{n}</li>' for n in notes)
    howto = HOWTO.get(view, '#system-read')
    return (f'<figure class="fig {extra_cls}" data-spec="{sid}" data-dataset="{sp["dataset"]}" data-evidence="{kind}" '
            f'aria-labelledby="{uid}-t">'
            f'<div class="fhead"><p class="elab" data-role="evidence-label">{kind} <span class="gr">· {e(grade_words)}</span></p>'
            f'<h2 class="ftitle" data-role="title" id="{uid}-t" tabindex="-1">{e(title)}</h2>'
            f'<p class="fmeasure" data-role="measure">{e(measure)}</p>'
            + (f'<p class="fsub">{e(sub)}</p>' if sub else '') + '</div>'
            f'<div class="fbody">{body}</div>'
            + (f'<ol class="fnotes" aria-label="Notes on {sid}">{nts}</ol>' if notes else '')
            + coding + disclosure_html(sp['dataset'])
            + f'<div class="fsrcrow"><p class="fsrc" data-role="source">{e(source)}</p>'
            f'<p class="fcred">Chart: Oath &amp; Action<br><a href="{howto}">How to read our charts</a></p></div>'
            f'<details class="feq" data-role="equivalent"><summary><span><span class="s-show">Show</span><span class="s-hide">Hide</span> '
            f'the <span class="vh">{sid} </span>table</span></summary><div class="eqb">{equivalent}</div></details>'
            '</figure>')


def anat_figure(sid, uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls='', sub='', coding=''):
    """The same figure with the anatomy numbers of the system sheet on its parts."""
    h = figure(sid, 'anat-' + uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls, sub, coding)
    h = h.replace('id="anat-', 'id="').replace('aria-labelledby="anat-', 'aria-labelledby="')
    h = h.replace('<figure ', '<figure data-anat="1" ', 1)
    for old, num_ in [('<p class="elab"', 2), ('<h2 class="ftitle"', 3), ('<p class="fmeasure"', 4),
                      ('<div class="fbody"', 5), ('<span class="rnote"', 6), ('<ol class="fnotes"', 7), ('<p class="fsrc"', 8),
                      ('<details class="feq"', 9)]:
        assert old in h, old
        h = h.replace(old, old + f' data-anat="{num_}"', 1)
    return h


def strip(sid, why):
    sp = SPEC[sid]
    return (f'<aside class="strip" aria-label="Studio note on specimen {sid}">'
            f'<p class="st-k">Studio note · not part of the chart</p>'
            f'<p class="st-id">{sid} <span>{e(sp["form"])}</span></p>'
            f'<p class="st-q"><span>Reader question</span>{e(sp["reader_question"])}</p>'
            f'<p class="st-w"><span>Why this form</span>{e(why)}</p></aside>')


def plate(view, sid, fig_html, why):
    return f'<article class="plate" id="{view}-{sid.lower()}">{fig_html}{strip(sid, why)}</article>'


def table(cols, data, caption, uid, sortable=False, sort_col=None, sort_dir='descending', cls='reg rf'):
    """A register table. cols: (label, getter, kind) where kind is 'h' (row header), 'hid' (row header holding an ID or
    a year, set in tabular figures), 'n' (number) or 't' (text). getter returns (display_html, sort_value). Numbers sit
    right-aligned in tabular figures; a long table lets the reader re-sort it."""
    head = []
    for i, (lab, _, kind) in enumerate(cols):
        al = ' class="n"' if kind == 'n' else ''
        if sortable:
            srt = f' aria-sort="{sort_dir}"' if sort_col == i else ''
            head.append(f'<th scope="col"{al}{srt}><button type="button" class="sb" data-sort="{i}">{lab}</button></th>')
        else:
            head.append(f'<th scope="col"{al}>{lab}</th>')
    body = []
    for r in data:
        cells = []
        for lab, get, kind in cols:
            disp, sv = get(r)
            plain = re.sub(r'<[^>]+>', '', lab)
            sva = f' data-sv="{e(sv)}"' if sortable else ''
            if kind in ('h', 'hid'):
                tn = ' class="tn"' if kind == 'hid' else ''
                cells.append(f'<th scope="row"{tn} data-label="{e(plain)}"{sva}>{disp}</th>')
            else:
                c = ' class="n"' if kind == 'n' else ''
                cells.append(f'<td{c} data-label="{e(plain)}"{sva}>{disp}</td>')
        body.append('<tr>' + ''.join(cells) + '</tr>')
    return (f'<div class="tw"><table class="{cls}" id="{uid}"><caption>{e(caption)}</caption>'
            f'<thead><tr>{"".join(head)}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def eq_extra(notes_plain, source, extra=()):
    """What a sighted reader gets beyond the table: every note in or under the drawing, any key, and the source."""
    out = '<div class="eqn"><p class="eqh">Notes</p><ul>' + ''.join(f'<li>{e(n)}</li>' for n in notes_plain) + '</ul>'
    for head, items in extra:
        out += f'<p class="eqh">{e(head)}</p><ul>' + ''.join(f'<li>{e(n)}</li>' for n in items) + '</ul>'
    return out + f'<p class="eqh">Source</p><p>{e(source)}</p></div>'


def reg_bar(key, parts, scale):
    """An in-row bar: parts are (field, value, kind); each part's width is its value over the scale (the largest row,
    or the row's own total for a 100 percent bar). Kinds draw the direction code as unit glyphs, or the grade ramp."""
    spans = []
    for field, v, kind in parts:
        if v:
            spans.append(f'<span class="seg k-{kind}" data-key="{e(key)}" data-field="{e(field)}" data-value="{v}" data-mark="bar" '
                         f'data-axis="x" style="width:{100 * v / scale:.4f}%;--n:{v}"></span>')
    return f'<span class="reg-track" aria-hidden="true">{"".join(spans)}</span>'


def ranked_register(uid, caption, cols, groups, foot=None, cls=''):
    """The concept's register generator. cols: dicts with head, kind ('h', 'bar', 'n'), label (for the phone reflow),
    cell(row) -> html, and optionally group(rows) -> html. groups: [(group label or None, rows)], already in the order
    that answers the question. foot: a list of cell html for a total row."""
    head = ''.join(f'<th scope="col" class="{"n" if c["kind"] == "n" else "c-" + c["kind"]}">{c["head"]}</th>' for c in cols)
    bodies = []
    for glab, rs in groups:
        trs = []
        if glab:
            cells = [f'<th scope="rowgroup" class="c-h">{e(glab)}</th>']
            for c in cols[1:]:
                g = c.get('group')
                v = g(rs) if g else ''
                k = 'n' if c['kind'] == 'n' else 'c-' + c['kind']
                cells.append(f'<td class="{k}" data-label="{e(c["label"])}">{v}</td>' if v != '' else f'<td class="{k} empty"></td>')
            trs.append('<tr class="grp">' + ''.join(cells) + '</tr>')
        for r in rs:
            cells = []
            for c in cols:
                if c['kind'] == 'h':
                    cells.append(f'<th scope="row" class="c-h">{c["cell"](r)}</th>')
                elif c['kind'] == 'bar':
                    cells.append(f'<td class="c-bar">{c["cell"](r)}</td>')
                else:
                    v = c['cell'](r)
                    z = ' z' if re.sub(r'<[^>]+>', '', str(v)).strip() in ('0', '0.0') else ''
                    cells.append(f'<td class="n{z}" data-label="{e(c["label"])}">{v}</td>')
            trs.append('<tr>' + ''.join(cells) + '</tr>')
        bodies.append('<tbody>' + ''.join(trs) + '</tbody>')
    tf = ''
    if foot:
        tf = '<tfoot><tr>' + ''.join(foot) + '</tr></tfoot>'
    return (f'<div class="tw"><table class="reg reg-r {cls}" id="{uid}"><caption>{e(caption)}</caption>'
            f'<thead><tr>{head}</tr></thead>{"".join(bodies)}{tf}</table></div>')


# ================================================================================================ S01
def s01_numbers():
    R = byk('stock-trading-ban')
    return R


def s01(view, card=False):
    R = s01_numbers()
    uid = f'{view}-s01' + ('-card' if card else '')
    title = 'Nearly nine in ten Republicans and Democrats favored a ban on stock trading by members of Congress.'
    measure = ('Share of registered voters who favor a ban, by party, United States, survey fielded May 19 to 30, 2023; '
               'with the votes in the House and Senate in 2026')
    assert R['support-republicans']['value'] >= 85 and R['support-democrats']['value'] >= 85
    parties = sorted([R['support-democrats'], R['support-republicans']], key=lambda r: (-r['value'], r['group']))

    def prow(r):
        party = r['group']
        return (f'<li class="prow" data-party="{e(party)}"><span class="pn">{e(party)}</span>'
                f'<span class="ptrk" aria-hidden="true"><span class="pbar" data-key="{r["key"]}" data-value="{r["value"]}" '
                f'data-mark="bar" data-axis="x" style="width:{r["value"]}%"></span></span>'
                f'<span class="pv"><span data-key="{r["key"]}" data-value="{r["value"]}" data-mark="label">{r["value"]}</span>%</span></li>')
    allr = R['support-all']
    big = (f'<div class="s01-big"><p class="bign"><span data-key="support-all" data-value="{allr["value"]}" data-mark="label">'
           f'{allr["value"]}</span><span class="pc">%</span></p>'
           f'<p class="bigc">of registered voters favored a ban on stock trading by members of Congress</p></div>')
    reg = ('<div class="s01-reg"><p class="regh" id="' + uid + '-pr">By party, highest first</p>'
           f'<ul class="plist" aria-labelledby="{uid}-pr">' + ''.join(prow(p) for p in parties) + '</ul>'
           '<p class="scale" aria-hidden="true"><span>0</span><span>100%</span></p></div>')
    hy, hn = R['house-yes']['value'], R['house-no']['value']
    sy, sn, need = R['senate-yes']['value'], R['senate-no']['value'], R['senate-needed']['value']
    short = need - sy
    votes = ('<div class="tw"><table class="reg s01v"><caption>What Congress did next</caption><thead><tr>'
             '<th scope="col">Vote</th><th scope="col">Date</th><th scope="col" class="n">For</th>'
             '<th scope="col" class="n">Against</th><th scope="col">Result</th></tr></thead><tbody>'
             f'<tr><th scope="row" data-label="Vote">House, passage of H.R. 7008, a stock-trading ban</th><td data-label="Date">July 22, 2026</td>'
             f'<td class="n" data-label="For"><span data-key="house-yes" data-value="{hy}" data-mark="label">{hy}</span></td>'
             f'<td class="n" data-label="Against"><span data-key="house-no" data-value="{hn}" data-mark="label">{hn}</span></td>'
             '<td data-label="Result">Passed</td></tr>'
             f'<tr><th scope="row" data-label="Vote">Senate, vote to take up the bill (cloture)</th><td data-label="Date">September 30, 2026</td>'
             f'<td class="n" data-label="For"><span data-key="senate-yes" data-value="{sy}" data-mark="label">{sy}</span></td>'
             f'<td class="n" data-label="Against"><span data-key="senate-no" data-value="{sn}" data-mark="label">{sn}</span></td>'
             f'<td data-label="Result">Fell {WORDS[short]} short of the <span data-key="senate-needed" data-value="{need}" '
             f'data-mark="label">{need}</span> votes needed</td></tr></tbody></table></div>')
    notes = ['The survey was fielded in May 2023, three years before both votes.',
             f'Taking up the bill needed {need} votes, three-fifths of the Senate, to end debate (cloture).',
             'Both parties are drawn the same way and listed by value. The vote totals carry no party split.']
    body = f'<div class="s01">{big}{reg}</div>{votes}'
    src = source_text('stock-trading-ban')
    eq = table([('Group or vote', lambda r: (e(r['group']), r['group']), 'h'), ('Measure', lambda r: (e(r['measure']), r['measure']), 't'),
                ('Value', lambda r: (num(r['value']), r['value']), 'n')], rows('stock-trading-ban'),
               'Every row of the stock-trading dataset', f'{uid}-eq') + eq_extra(notes, src)
    if card:
        return s01_card(uid, title, measure, parties, allr, src, eq, hy, hn, sy, sn, need)
    return figure('S01', uid, title, measure, body, [e(n) for n in notes], src, eq, 'a published survey and two recorded votes')


def s01_card(uid, title, measure, parties, allr, src, eq, hy, hn, sy, sn, need):
    rows_ = ''.join(
        f'<li class="crow" data-party="{e(p["group"])}"><span class="cn">{e(p["group"])}</span>'
        f'<span class="ctrk" aria-hidden="true"><span class="cbar" data-key="{p["key"]}" data-value="{p["value"]}" data-mark="bar" '
        f'data-axis="x" style="width:{p["value"]}%"></span></span>'
        f'<span class="cv"><span data-key="{p["key"]}" data-value="{p["value"]}" data-mark="label">{p["value"]}</span>%</span></li>'
        for p in parties)
    allrow = (f'<li class="crow all"><span class="cn">All registered voters</span><span class="ctrk" aria-hidden="true">'
              f'<span class="cbar" data-key="support-all" data-value="{allr["value"]}" data-mark="bar" data-axis="x" style="width:{allr["value"]}%"></span></span>'
              f'<span class="cv"><span data-key="support-all" data-value="{allr["value"]}" data-mark="label">{allr["value"]}</span>%</span></li>')
    ctx = (f'<p class="cctx">The House passed a ban, H.R. 7008, <span data-key="house-yes" data-value="{hy}" data-mark="label">{hy}</span> to '
           f'<span data-key="house-no" data-value="{hn}" data-mark="label">{hn}</span> on July 22, 2026. On September 30 the Senate '
           f'voted <span data-key="senate-yes" data-value="{sy}" data-mark="label">{sy}</span> to '
           f'<span data-key="senate-no" data-value="{sn}" data-mark="label">{sn}</span> to take it up. Taking up the bill needed '
           f'<span data-key="senate-needed" data-value="{need}" data-mark="label">{need}</span> votes, three-fifths of the Senate, to end debate (cloture).</p>')
    card = (f'<div class="card g-news">'
            f'<p class="celab" data-role="evidence-label">Finding <span>· a published survey and two recorded votes</span></p>'
            f'<h2 class="ctitle" data-role="title" id="{uid}-t">{e(title)}</h2>'
            f'<p class="cmeasure" data-role="measure">{e(measure)}</p>'
            f'<ul class="crows">{rows_}{allrow}</ul><p class="cscale" aria-hidden="true"><span>0</span><span>100%</span></p>'
            f'{ctx}<p class="csrc" data-role="source">{e(src)}</p>'
            f'<div class="cfoot">{wordmark_card()}<p>From Who Do They Answer To?, the Oath &amp; Action systems atlas</p></div></div>')
    return (f'<figure class="cardfig" data-spec="S01" data-dataset="stock-trading-ban" data-evidence="Finding" aria-labelledby="{uid}-t">'
            f'<div class="cardscroll" role="region" tabindex="0" aria-label="Social card from specimen S01, 1080 by 1350 pixels at true size">'
            f'{card}</div>'
            f'<details class="feq" data-role="equivalent"><summary><span><span class="s-show">Show</span><span class="s-hide">Hide</span> '
            f'the <span class="vh">S01 card </span>table</span></summary><div class="eqb">{eq}</div></details></figure>')


# ================================================================================================ note placer
class Occ:
    """An occupancy grid for one drawing, so notes find free space beside the data instead of on it. Series lines are
    also kept on their own grid, because a leader may never cross a series."""

    def __init__(self, W, H, cell=2):
        self.c, self.W, self.H = cell, W, H
        self.g = np.zeros((int(H / cell) + 3, int(W / cell) + 3), dtype=np.int16)
        self.lab = np.zeros_like(self.g)
        self.ser = np.zeros_like(self.g)

    def _sl(self, x0, y0, x1, y1):
        c = self.c
        r0, c0 = max(0, int(y0 // c)), max(0, int(x0 // c))
        r1, c1 = max(0, int(math.ceil(y1 / c))), max(0, int(math.ceil(x1 / c)))
        return slice(r0, r1 + 1), slice(c0, c1 + 1)

    def box(self, x0, y0, x1, y1, label=False, series=False):
        sl = self._sl(x0, y0, x1, y1)
        self.g[sl] = 1
        if label:
            self.lab[sl] = 1
        if series:
            self.ser[sl] = np.maximum(self.ser[sl], 1)   # never wipe a centerline already marked

    def poly(self, pts, pad=4, series=False):
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            n = int(max(abs(xb - xa), abs(yb - ya)) / 2) + 1
            for i in range(n + 1):
                t_ = i / n
                x, y = xa + (xb - xa) * t_, ya + (yb - ya) * t_
                self.box(x - pad, y - pad, x + pad, y + pad, series=series)
                if series:
                    sl = self._sl(x - 1, y - 1, x + 1, y + 1)
                    self.ser[sl] = 2

    def free(self, x0, y0, x1, y1):
        if x0 < 0 or y0 < 0 or x1 > self.W or y1 > self.H:
            return False
        return not self.g[self._sl(x0, y0, x1, y1)].any()

    def seg_ok(self, xa, ya, xb, yb):
        """A leader may cross no label and no series line."""
        L = math.hypot(xb - xa, yb - ya)
        n = int(L / 2) + 1
        for i in range(1, n):
            t_ = i / n
            if t_ * L < 9 or (1 - t_) * L < 3:    # the leader itself starts 7 px from its mark
                continue
            x, y = xa + (xb - xa) * t_, ya + (yb - ya) * t_
            sl = self._sl(x - 1, y - 1, x + 1, y + 1)
            if self.lab[sl].any() or (self.ser[sl] == 2).any():
                return False
        return True


def place_note(occ, rows_, cls, target, region, pref, size=13, weight=400, lh=16, gap=6, step=4, lead=True, fallback=None):
    """Put a note where it touches no line, mark or other note, as close as it can to its target and its preferred
    corner. When it sits away from the target, a 1 px leader joins them; the leader stays under the token length and
    crosses no series and no label. A shorter fallback wording is tried if the first finds no room. Returns SVG."""
    if fallback:
        for i, wording in enumerate([rows_] + list(fallback)):
            try:
                return place_note(occ, wording, cls, target, region, pref, size, weight, lh, gap, step, lead)
            except SystemExit:
                if i == len(fallback):
                    raise
    w = max(tw(r, size, weight) for r in rows_)
    h = lh * len(rows_) - (lh - size) + 2
    tx, ty = target
    best = None
    rx0, ry0, rx1, ry1 = region
    for y in range(int(ry0), int(ry1 - h) + 1, step):
        for x in range(int(rx0), int(rx1 - w) + 1, step):
            if not occ.free(x - gap, y - gap, x + w + gap, y + h + gap):
                continue
            nx, ny = min(max(tx, x), x + w / T['label_headroom']), min(max(ty, y), y + h)
            d = math.hypot(nx - tx, ny - ty)
            if d > T['leader_max']:
                continue
            cost = d + 0.35 * math.hypot(x - pref[0], y - pref[1])
            if best is not None and cost >= best[0]:
                continue
            if d > 9 and not occ.seg_ok(tx, ty, nx, ny):
                continue
            best = (cost, x, y, nx, ny, d)
    if best is None:
        raise SystemExit(f'no room for the note "{rows_[0]}"')
    _, x, y, nx, ny, d = best
    out = []
    if lead and d > 9:
        ang = math.atan2(ny - ty, nx - tx)
        sx, sy = tx + 7 * math.cos(ang), ty + 7 * math.sin(ang)
        ex, ey = nx - 3 * math.cos(ang), ny - 3 * math.sin(ang)
        out.append(f'<line class="lead" x1="{f(sx)}" y1="{f(sy)}" x2="{f(ex)}" y2="{f(ey)}"/>')
        occ.poly([(sx, sy), (ex, ey)], pad=2)
    occ.box(x, y, x + w, y + h, label=True)
    out.append(lines(x, y + size - 2, rows_, cls, lh))
    return ''.join(out)


# ================================================================================================ S02 line
def s02_data():
    rs = rows('child-poverty-spm')
    spm = [r for r in rs if r['measure'] == 'spm']
    off = [r for r in rs if r['measure'] == 'official']

    def segments(series):
        segs, cur = [], []
        for y in sorted({r['year'] for r in series}):
            here = [r for r in series if r['year'] == y]
            if len(here) == 1:
                cur.append(here[0])
            else:
                early = next(r for r in here if r['comparable_with'] == 'earlier')
                late = next(r for r in here if r['comparable_with'] == 'later')
                cur.append(early)
                segs.append(cur)
                cur = [late]
        segs.append(cur)
        return segs
    return spm, off, segments(spm), segments(off)


S02_NOTES = {
    'wide': {'low': ['2021: 5.1%, the lowest from 2009 to 2025.', 'The expanded child tax credit was paid that',
                     'year. The timing alone does not show how', 'much of the drop came from the credit.'],
             'y22': ['2022: 12.0%, the first year after', 'the expanded credit expired'],
             'y22+': [['2022: 12.0%, the first', 'year after the expanded', 'credit expired'],
                      ['2022: 12.0%,', 'the first year', 'after the expanded', 'credit expired']],
             'law': ['July 2025: P.L. 119-21 set the child tax', 'credit at up to $2,200 per child'],
             'law+': [['July 2025: P.L. 119-21 set', 'the child tax credit at up', 'to $2,200 per child']],
             'brk': ['Census changed its method in 2013, 2017', 'and 2019. Each of those years has two',
                     'estimates, and the line does not join them.'],
             'brk+': [['Census changed its method in', '2013, 2017 and 2019. Each has', 'two estimates, not joined.'],
                      ['Census changed its method', 'in 2013, 2017 and 2019.', 'Each of those years has two', 'estimates, not joined.']],
             'off': ['Official measure, which counts', 'pretax cash income only'],
             'off+': [['Official measure']],
             'spm': ['Supplemental Poverty Measure, which', 'adds tax credits and other aid'],
             'spm+': [['Supplemental Poverty Measure'], ['Supplemental', 'Poverty Measure']]},
    'narrow': {'low': ['2021: 5.1%, the low', 'for 2009 to 2025'], 'y22': ['2022: 12.0%, after', 'the credit expired'],
               'y22+': [['2022: 12.0%,', 'after the', 'credit expired'], ['2022:', '12.0%, after', 'the credit', 'expired']],
               'off': ['Official measure'], 'spm': ['Supplemental', 'Poverty Measure'], 'spm+': [['Supplemental Poverty Measure']]},
}
S02_UNDER = {   # notes that move under the plot on an artboard with no room for them in the drawing (R25)
    'y22': '2022: 12.0 percent, the first year after the expanded credit expired.',
    'low': 'The expanded child tax credit was paid in 2021. The timing alone does not show how much of the drop came from the credit.',
    'law': 'July 2025: P.L. 119-21 set the child tax credit at up to $2,200 per child.',
    'brk': 'Census changed its method in 2013, 2017 and 2019. Each of those years has two estimates, and the line does not join them.',
}


@functools.lru_cache(maxsize=None)
def s02_layout(W):
    """Geometry and notes for one artboard width; shared by every ground, so the views stay identical."""
    spm, off, sseg, oseg = s02_data()
    by = {(r['year'], r['comparable_with']): r for r in spm}
    low = min(spm, key=lambda r: r['percent'])
    assert low['year'] == 2021
    narrow = W < 500
    gut, R_ = 30, (74 if narrow else 80)
    H = 380 if narrow else 460
    top, bot = 26, 32
    x0, x1, y0, y1 = gut, W - R_, top, H - bot
    X = lambda yr: x0 + (yr - 2009) / (2025 - 2009) * (x1 - x0)
    Y = lambda v: y1 - v / 25 * (y1 - y0)
    occ = Occ(W, H)
    p = []
    for v in (0, 5, 10, 15, 20, 25):
        yy = round(Y(v)) + 0.5   # whole pixel plus a half, so the hairline sits on one device row
        p.append(f'<line class="{"base" if v == 0 else "grid"}" x1="0" x2="{f(x1 + 6)}" y1="{f(yy)}" y2="{f(yy)}"/>')
        lab = f'{v}%' if v == 25 else str(v)
        p.append(txt(0, yy - 5, lab, 'tk'))
        occ.box(0, yy - 17, tw(lab) + 4, yy - 2, label=True)
    ticks = [2009, 2013, 2017, 2021, 2025] if narrow else [2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025]
    for yr in ticks:
        p.append(txt(X(yr), H - 10, str(yr), 'tk', 'middle' if yr not in (2009, 2025) else ('start' if yr == 2009 else 'end')))
    occ.box(0, y1 + 2, W, H, label=True)
    occ.box(0, 0, W, y0 - 6)
    pts = lambda seg, key: [(X(r['year']), Y(r[key])) for r in seg]
    for seg in oseg:
        p.append('<path class="ln-ctx" d="M' + 'L'.join(f'{f(a)} {f(b)}' for a, b in pts(seg, 'percent')) + '"/>')
        occ.poly(pts(seg, 'percent'), 4, series=True)
        for r in seg:
            p.append(f'<circle class="vx-ctx" cx="{f(X(r["year"]))}" cy="{f(Y(r["percent"]))}" r="1.75" data-key="{r["key"]}" '
                     f'data-value="{r["percent"]}" data-mark="vertex"/>')
    for seg in sseg:
        p.append('<path class="ln-main" d="M' + 'L'.join(f'{f(a)} {f(b)}' for a, b in pts(seg, 'percent')) + '"/>')
        occ.poly(pts(seg, 'percent'), 5, series=True)
    for r in spm:
        if r is not low:
            p.append(f'<circle class="pt-main" cx="{f(X(r["year"]))}" cy="{f(Y(r["percent"]))}" r="{T["radius"]["point"]}" '
                     f'data-key="{r["key"]}" data-value="{r["percent"]}" data-mark="point" data-axis="y"/>')
    lx, ly = X(2021), Y(low['percent'])
    occ.box(lx - 9, ly - 9, lx + 9, ly + 9)
    s25 = by[(2025, 'both')]
    ey = Y(s25['percent'])
    p.append(txt(x1 + 8, ey + 5, f'{s25["percent"]}%', 'lab-b'))
    p.append(lines(x1 + 8, ey + 22, ['on both', 'measures'], 'nt', 16))
    occ.box(x1 + 4, ey - 10, W, ey + 44, label=True)
    N = S02_NOTES['narrow' if narrow else 'wide']
    plot = (x0 + 2, y0, x1, y1)
    r22 = by[(2022, 'both')]
    o11 = next(r for r in off if r['year'] == 2011)
    b17 = [r for r in spm if r['year'] == 2017]
    s11 = by[(2011, 'both')]
    right = (x0 + 2, y0, W, y1)    # notes for the last years may use the margin under the end label
    notes = [
        ('spm', 'lab-s', (X(2010.5), (Y(by[(2010, 'both')]['percent']) + Y(s11['percent'])) / 2), (X(2009.2), Y(15)), plot),
        ('off', 'nt', (X(2011), Y(o11['percent'])), (X(2009.3), Y(24.5)), plot),
        ('low', 'nt-b', (lx, ly), (X(2014.5), Y(4.5)), plot),
        ('law', 'nt', (X(2025), ey), (X(2023.2), Y(10)), right),
        ('y22', 'nt', (X(2022), Y(r22['percent'])), (X(2022.6), Y(4)), right),
        ('brk', 'nt', (X(2017), Y(sum(r['percent'] for r in b17) / 2)), (X(2015.5), Y(10)), plot),
    ]
    under = []
    for key, cls, target, pref, region in notes:
        if key not in N:
            under.append(key)
            continue
        wt = 600 if cls in ('nt-b', 'lab-s') else 400
        try:
            p.append(place_note(occ, N[key], cls, target, region, pref, weight=wt, fallback=N.get(key + '+')))
        except SystemExit:
            if key not in S02_UNDER:
                raise
            under.append(key)      # no room in this drawing: the note prints under it instead
    if narrow:
        under = ['low'] + under
    return ''.join(p), H, (lx, ly), low, tuple(under)


def s02_svg(W, view, red='none'):
    body, H, (lx, ly), low, _ = s02_layout(W)
    if red == 'working':
        rd = ' data-red="working" data-red-job="the 2021 low the title names"'
    elif red == 'specimen':
        rd = ' data-red="specimen"'
    else:
        rd = ''
    pcls = 'pt-red' if red in ('working', 'specimen') else 'pt-main'
    dot = (f'<g{rd}><circle class="{pcls}" cx="{f(lx)}" cy="{f(ly)}" r="{T["radius"]["point_named"]}" data-key="{low["key"]}" '
           f'data-value="{low["percent"]}" data-mark="point" data-axis="y"/></g>')
    lab = ('Line chart of child poverty, 2009 to 2025. Under the Supplemental Poverty Measure, which adds tax credits and other '
           'aid, it fell to 5.1 percent in 2021, the lowest from 2009 to 2025, and rose to 12.0 percent in 2022, the first year '
           'after the expanded child tax credit expired, and 13.5 percent in 2023 and 2024; it was 13.4 percent in 2025. The '
           'official measure, which counts pretax cash income only, ran from 22.0 percent in 2010 to 13.4 percent in 2025. '
           'Census changed its method in 2013, 2017 and 2019; those years have two estimates each, not joined. July 2025: '
           'P.L. 119-21 set the child tax credit at up to $2,200 per child.')
    return svg(W, H, f's02-{view}-{W}', lab, body + dot, 'ab')


def artboards(fn, view, *args):
    """One drawing per artboard width in the tokens; the figure's width picks one, shown at its natural size."""
    return '<div class="abs">' + ''.join(fn(W, view, *args) for W in T['artboards']) + '</div>'


def s02(view, red='none'):
    uid = f'{view}-s02'
    spm, off, sseg, oseg = s02_data()
    low = min(spm, key=lambda r: r['percent'])
    r22 = next(r for r in spm if r['year'] == 2022)
    assert r22['percent'] > 2 * low['percent']
    title = (f'Child poverty fell to {low["percent"]} percent in {low["year"]}, its lowest from 2009 to 2025, '
             'and more than doubled the next year.')
    measure = ('Children under 18 below the poverty line, Supplemental Poverty Measure, United States, 2009 to 2025, '
               'in percent, with the official measure for context')
    body = artboards(s02_svg, view, red)
    notes = ['The Supplemental Poverty Measure counts tax credits and other aid that the official measure leaves out. '
             'Census describes a change between two years and credits it to no single policy.',
             'The Census Bureau revised 2019 to 2024 in August 2026. The atlas prints the first-published 9.7, 5.2 and 13.4 percent '
             'for 2020, 2021 and 2024; the current table reads 9.6, 5.1 and 13.5.',
             'Survey estimates carry margins of error of 0.4 to 0.9 points at the 90 percent level; the table gives each one.']
    src = source_text('child-poverty-spm')
    where = {k: [i for i, W in enumerate(T['artboards']) if k in s02_layout(W)[4]] for k in S02_UNDER}
    shown = [e(n) for n in notes] + [f'<span class="u-only {" ".join(f"u-a{i}" for i in ix)}">{e(S02_UNDER[k])}</span>'
                                     for k, ix in where.items() if ix]
    offy = {(r['year'], r['comparable_with']): r for r in off}

    def ov(r):
        o = offy.get((r['year'], r['comparable_with'])) or offy.get((r['year'], 'both'))
        return (f'{o["percent"]:.1f}', o['percent']) if o else ('not given', -1)
    variant = {'standard': '', 'corrected_2026_method': 'Method used from 2019 on', 'original_2011_method': 'Original 2011 method',
               'updated_processing': 'Updated processing', 'legacy_processing': 'Earlier processing',
               'redesigned_income_questions': 'Redesigned income questions', 'traditional_income_questions': 'Traditional income questions'}
    data = sorted(spm, key=lambda r: (-r['year'], r['comparable_with'] != 'later'))
    eq = table([('Year', lambda r: (str(r['year']), r['year']), 'hid'),
                ('Estimate', lambda r: (e(variant.get(r['series_variant'], r['series_variant'])) or 'Standard', r['series_variant']), 't'),
                ('Supplemental measure, %', lambda r: (f'<span data-key="{r["key"]}" data-value="{r["percent"]}" data-mark="label">{r["percent"]:.1f}</span>', r['percent']), 'n'),
                ('Margin of error, points', lambda r: (f'{float(r["moe_pct"]):.1f}', r['moe_pct']), 'n'),
                ('Official measure, %', ov, 'n')], data, 'Child poverty by year, both measures', f'{uid}-eq') \
        + eq_extra([' '.join(S02_NOTES['wide']['low']), ' '.join(S02_NOTES['wide']['y22']) + '.', ' '.join(S02_NOTES['wide']['law']) + '.',
                    ' '.join(S02_NOTES['wide']['brk']), '2025: 13.4 percent on both measures.',
                    'Line labels: ' + ' '.join(S02_NOTES['wide']['spm']) + '; ' + ' '.join(S02_NOTES['wide']['off']) + '.'] + notes, src)
    return figure('S02', uid, title, measure, body, shown, src, eq, 'official statistic from a Census Bureau survey')


# ================================================================================================ S03 register
S03_ACTORS = [('Voters at the ballot box', ['Ballot initiative', 'Referendum']),
              ('Legislatures and councils', ['State statute', 'Federal statute', 'Local law or funding vote']),
              ('Courts', ['Court ruling']),
              ('Executives and agencies', ['Executive or agency action'])]
DIRS = [('away from voters', 'Away', 'awy'), ('toward voters', 'Toward', 'tow'), ('voters kept existing rules', 'Kept', 'kept'),
        ('mixed', 'Mixed', 'mix'), ('pending', 'Pending', 'pend')]


def swatch(kind):
    return f'<span class="sw sw-{kind}" aria-hidden="true"></span>'


def log_facts():
    """Facts about the repair log that every chart drawn from it prints (F1, D2-103), computed from the rows."""
    rs = rows('rule-changes')
    n = len(rs)
    recent = sum(1 for r in rs if r['year'] >= 2025)
    R = {r['key']: r for r in rs}
    assert (R['RL38']['jurisdiction'], R['RL38']['direction'], R['RL38']['date'][:7]) == ('Texas', 'away from voters', '2025-08')
    assert (R['RL41']['jurisdiction'], R['RL41']['direction'], R['RL41']['date'][:7]) == ('California', 'away from voters', '2025-11')
    bans = [r for r in rows('rcv-bans') if r['prohibits_rcv']]
    own = {'MO', 'IN'}   # the two bans with log rows of their own (RL30, RL46)
    early = sum(1 for r in bans if r['code'] not in own and int(r['enacted_year']) < 2025)
    note = DS['rule-changes']['coding_note']
    neutral = ("A row's direction describes the rule's effect on who officials answer to and carries no judgment of the people "
               "or parties involved.")
    assert note.endswith(neutral)
    coding = note[:-len(neutral)].strip()
    assert coding.count('the reform profiles R-01 and R-02 rate') == 1
    coding = coding.replace('the reform profiles R-01 and R-02 rate', 'the reform profiles rate')
    return dict(n=n, recent=recent, early=early, n_bans=len(bans) - len(own), coding=coding, neutral=neutral)


def log_block():
    """The coding rule in full, its neutrality line and one map example from each side, as HTML that wraps."""
    L = log_facts()
    return ('<div class="fcode"><p class="fch">How the atlas codes direction</p>'
            f'<p>{e(L["coding"])}</p><p class="fneu">{e(L["neutral"])}</p>'
            '<p>A map redrawn in the middle of a decade counts as away from voters whichever party draws it: Texas\'s HB 4 '
            '(August 2025) and California\'s Proposition 50 (November 2025) both count as away.</p></div>')


def log_notes():
    L = log_facts()
    assert (L['n'], L['recent']) == (64, 33)
    return [f'The log holds the {L["n"]} changes the atlas chose to record, not every rule change in the country. It records more '
            f'of recent years: {L["recent"]} of the {L["n"]} entries fall in 2025 and 2026.',
            'One entry, RL47 (March 2026), stands for all 19 state bans on ranked-choice voting; Missouri\'s and Indiana\'s bans '
            'also have entries of their own.']


def s03_numbers():
    R = byk('rule-changes-by-instrument')
    grp = []
    for name, keys in S03_ACTORS:
        rs = sorted([R[k] for k in keys], key=lambda r: -r['value'])
        tot = {d: sum(r[d] for r in rs) for d, _, _ in DIRS}
        grp.append((name, rs, sum(r['value'] for r in rs), tot))
    grp.sort(key=lambda g: -g[2])
    assert sum(g[2] for g in grp) == 64
    return R, grp


def s03(view):
    uid = f'{view}-s03'
    R, grp = s03_numbers()
    away = {g[0]: g[3]['away from voters'] for g in grp}
    leg_courts = away['Legislatures and councils'] + away['Courts']
    total_away = sum(away.values())
    assert (leg_courts, total_away) == (19, 24)
    bi, ss, rf = R['Ballot initiative'], R['State statute'], R['Referendum']
    passed = bi['toward voters'] + bi['away from voters'] + bi['mixed']
    assert (bi['value'], passed, bi['toward voters'], bi['away from voters'], bi['voters kept existing rules'], bi['pending']) == (17, 7, 7, 0, 8, 2)
    assert (ss['away from voters'], ss['value']) == (9, 11) and rf['away from voters'] == 3
    title = f'Legislatures and courts made {leg_courts} of the {total_away} rule changes the atlas codes as moving away from voters.'
    measure = ('Rule changes in our atlas\'s repair log, by how each was made and by direction, United States, '
               'August 6, 1965 to the November 3, 2026 ballot')
    mx = max(r['value'] for r in R.values())
    row_note = {'Ballot initiative': f'All {passed} that passed moved toward voters.',
                'State statute': f'{ss["away from voters"]} of {ss["value"]} moved away from voters.'}

    def bar(r):
        parts = [(d, r[d], k) for d, _, k in DIRS]
        note = f'<span class="rnote">{e(row_note[r["key"]])}</span>' if r['key'] in row_note else ''
        return reg_bar(r['key'], parts, mx) + note
    cols = [dict(head='How the change was made', kind='h', label='', cell=lambda r: e(r['key'])),
            dict(head='Rule changes, one glyph each', kind='bar', label='', cell=bar),
            dict(head='All', kind='n', label='All', cell=lambda r: f'<span data-key="{e(r["key"])}" data-value="{r["value"]}" data-mark="label">{r["value"]}</span>',
                 group=lambda rs: str(sum(r['value'] for r in rs)))]
    for d, lab, k in DIRS:
        cols.append(dict(head=f'{swatch(k)}{lab}', kind='n', label=lab, cell=(lambda d: lambda r: str(r[d]))(d),
                         group=(lambda d: lambda rs: str(sum(r[d] for r in rs)))(d)))
    tots = {d: sum(g[3][d] for g in grp) for d, _, _ in DIRS}
    foot = (['<th scope="row" class="c-h">All 64 changes</th>', '<td class="c-bar empty"></td>', '<td class="n" data-label="All">64</td>']
            + [f'<td class="n" data-label="{lab}">{tots[d]}</td>' for d, lab, _ in DIRS])
    reg = ranked_register(f'{uid}-reg', 'Rule changes by how they were made, grouped by who acted', cols,
                          [(name, rs) for name, rs, _, _ in grp], foot)
    notes = log_notes()[:1] + [
        f'Citizen ballot initiatives: {bi["value"]} entries. All {passed} that passed moved the rules toward voters; '
        f'{bi["voters kept existing rules"]} failed and left the rules in force, and {bi["pending"]} are pending. Referendums are '
        f'ballot measures too: {rf["away from voters"]} of their {rf["value"]} entries moved the rules away from voters.',
        f'State statutes moved the rules away from voters in {ss["away from voters"]} of {ss["value"]} entries as logged, and in '
        f'{ss["away from voters"] - 1} of {ss["value"] - 1} without RL47.',
        'One federal entry is a statute that lapsed: the expanded child tax credit expired at the end of 2021 when Congress did '
        'not extend it.',
        log_notes()[1],
        'We grouped five one-row instruments (agency rule, executive action and executive order; municipal ordinance and council '
        'funding vote), and grouped instruments by who acted. The instruments are the atlas\'s.',
        f'Bars share one scale, from 0 to {mx} changes. Each dot or square is one change, and every count is printed.']
    src = source_text('rule-changes-by-instrument', drop=())
    eqrows = [r for _, rs, _, _ in grp for r in rs]
    eq = table([('Instrument', lambda r: (e(r['key']), r['key']), 'h'), ('All', lambda r: (str(r['value']), r['value']), 'n')]
               + [(lab, (lambda d: (lambda r: (str(r[d]), r[d])))(d), 'n') for d, lab, _ in DIRS],
               eqrows, 'Rule changes by instrument and direction', f'{uid}-eq') + eq_extra(
        [row_note['Ballot initiative'].replace('All', 'Ballot initiatives: all'), 'State statutes: ' + row_note['State statute']] + notes, src,
        extra=[('How the atlas codes direction', [log_facts()['coding'], log_facts()['neutral'],
                                                  'A map redrawn in the middle of a decade counts as away from voters whichever party draws it: '
                                                  'Texas\'s HB 4 (August 2025) and California\'s Proposition 50 (November 2025) both count as away.']),
               ('Key', ['Dots: away from voters. Squares: toward voters. Hollow squares: voters kept existing rules. Hatched squares: '
                        'mixed. Dashed squares: pending.'])])
    return figure('S03', uid, title, measure, reg, [e(n) for n in notes], src, eq, 'the atlas\'s dated log, directions coded by the atlas',
                  coding=log_block())


# ================================================================================================ S04 dumbbell
AGE = [('18_to_24', '18 to 24'), ('25_to_44', '25 to 44'), ('45_to_64', '45 to 64'), ('65_and_over', '65 and over'), ('all', 'All citizens')]


def s04_numbers():
    R = byk('turnout-by-age')
    base = 'citizen_voting_age_population'
    out = []
    for k, lab in AGE:
        a, b = R[f'{k}|2020|{base}'], R[f'{k}|2024|{base}']
        out.append((k, lab, a, b, round(b['voted_pct'] - a['voted_pct'], 1)))
    return out


def change_words(ch):
    """A change of two points or less is called a change, never a fall or a rise (Table A-1 has no margins of error)."""
    if abs(ch) < 2:
        return f'Little change, {signed(ch)}'
    return f'{"Up" if ch > 0 else "Down"} {abs(ch):.1f} points'


def dumbbell(xa, xb, y, a, b, ctx, red=''):
    """Two years on one row: the earlier year a hollow ring drawn on top, the later year a filled dot, joined edge to edge."""
    out = []
    r = T['radius']['dumbbell']
    if abs(xb - xa) - 2 * r - 1 > 0:
        d = 1 if xb > xa else -1
        out.append(f'<line class="{"db-ctx" if ctx else "db"}" x1="{f(xa + d * (r + .5))}" x2="{f(xb - d * (r + .5))}" y1="{f(y)}" y2="{f(y)}"/>')
    dot = (f'<circle class="{"pt-red" if red else "d24"}{" c" if ctx else ""}" cx="{f(xb)}" cy="{f(y)}" r="{r}" data-key="{b["key"]}" '
           f'data-value="{b["voted_pct"]}" data-mark="point" data-axis="x"/>')
    out.append(f'<g data-red="{red}">{dot}</g>' if red else dot)
    out.append(f'<circle class="d20h" cx="{f(xa)}" cy="{f(y)}" r="{r}"/>')
    out.append(f'<circle class="d20{" c" if ctx else ""}" cx="{f(xa)}" cy="{f(y)}" r="{r}" data-key="{a["key"]}" data-value="{a["voted_pct"]}" data-mark="point" data-axis="x"/>')
    return ''.join(out)


def s04_svg(W, view, red=''):
    data = s04_numbers()
    narrow = W < 500
    lo, hi = 40, 80
    p = []
    if not narrow:
        lx, px0, px1 = (0, 170, 560) if W >= 800 else (0, 112, W - 150)
        c20, c24, cch = (px1 + 70, px1 + 140, W) if W >= 800 else (px1, px1, W)
        X = lambda v: px0 + (v - lo) / (hi - lo) * (px1 - px0)
        top, rh = 52, 46
        if W >= 800:
            p.append(txt(c20, 16, '2020, %', 'th', 'end'))
            p.append(txt(c24, 16, '2024, %', 'th', 'end'))
        p.append(txt(cch, 16, 'Change, points', 'th', 'end'))
        p.append(f'<line class="base" x1="0" x2="{W}" y1="26.5" y2="26.5"/>')
        for i, (k, lab, a, b, ch) in enumerate(data):
            y = top + i * rh + (12 if k == 'all' else 0)
            ctx = k == 'all'
            if ctx:
                p.append(f'<line class="grid" x1="0" x2="{W}" y1="{f(round(y - 29) + .5)}" y2="{f(round(y - 29) + .5)}"/>')
            p.append(txt(lx, y + 5, e(lab), 'lab' if not ctx else 'lab-ctx'))
            xa, xb = X(a['voted_pct']), X(b['voted_pct'])
            p.append(dumbbell(xa, xb, y, a, b, ctx, red if i == 0 else ''))
            if i == 0:
                for xx, lab_, cls_ in ((xa, '2020', 'nt'), (xb, '2024', 'nt-b')):
                    other = xb if xx == xa else xa
                    p.append(txt(xx + (6 if xx > other else -6), y - 13, lab_, cls_, 'start' if xx > other else 'end'))
            if W >= 800:
                p.append(txt(c20, y + 5, f'<tspan data-key="{a["key"]}" data-value="{a["voted_pct"]}" data-mark="label">{a["voted_pct"]:.1f}</tspan>', 'num', 'end'))
                p.append(txt(c24, y + 5, f'<tspan data-key="{b["key"]}" data-value="{b["voted_pct"]}" data-mark="label">{b["voted_pct"]:.1f}</tspan>', 'num-b', 'end'))
            p.append(txt(cch, y + 5, e(change_words(ch) if W >= 800 or abs(ch) >= 2 else signed(ch)), 'num', 'end'))
        ys = top + len(data) * rh + 4
        for v in range(lo, hi + 1, 10):
            p.append(txt(X(v), ys, f'{v}%' if v == hi else str(v), 'tk', 'middle'))
        p.append(txt(px0 - 14, ys, 'Scale', 'tk', 'end'))
        H = ys + 6
    else:
        X = lambda v: 7 + (v - lo) / (hi - lo) * (W - 14)
        y = 18
        for i, (k, lab, a, b, ch) in enumerate(data):
            ctx = k == 'all'
            if ctx:
                y += 8
                p.append(f'<line class="grid" x1="0" x2="{W}" y1="{f(round(y - 18) + .5)}" y2="{f(round(y - 18) + .5)}"/>')
            p.append(txt(0, y, e(lab), 'lab' if not ctx else 'lab-ctx'))
            p.append(txt(W, y, e(change_words(ch)), 'num', 'end'))
            yd = y + 20
            xa, xb = X(a['voted_pct']), X(b['voted_pct'])
            p.append(dumbbell(xa, xb, yd, a, b, ctx, red if i == 0 else ''))
            p.append(txt(0, yd + 26, f'2020: <tspan data-key="{a["key"]}" data-value="{a["voted_pct"]}" data-mark="label">{a["voted_pct"]:.1f}</tspan>%'
                         f' · 2024: <tspan class="b" data-key="{b["key"]}" data-value="{b["voted_pct"]}" data-mark="label">{b["voted_pct"]:.1f}</tspan>%', 'nt'))
            y = yd + 58
        ys = y - 6
        p.append(txt(X(40), ys, '40', 'tk', 'start'))
        p.append(txt(X(60), ys, '60', 'tk', 'middle'))
        p.append(txt(X(80), ys, '80%', 'tk', 'end'))
        H = ys + 6
    lab = ('Dot plot of reported voting by age among citizens, 2020 and 2024: ' + '; '.join(
        f'{lab} {a["voted_pct"]:.1f} percent in 2020 and {b["voted_pct"]:.1f} in 2024, {change_words(ch).lower()}' for k, lab, a, b, ch in data)
        + '. Ring: 2020. Dot: 2024. Scale from 40 to 80 percent.')
    return svg(W, H, f's04-{view}-{W}', lab, ''.join(p))


def s04(view):
    uid = f'{view}-s04'
    data = s04_numbers()
    y24 = {k: b['voted_pct'] for k, _, _, b, _ in data}
    ch = {k: c for k, _, _, _, c in data}
    assert y24['18_to_24'] < y24['25_to_44'] < y24['45_to_64'] < y24['65_and_over']
    assert ch['18_to_24'] < -2 and ch['25_to_44'] < -2 and abs(ch['45_to_64']) < 2 and abs(ch['65_and_over']) < 2
    title = (f'Reported voting rose with age in 2024, from {y24["18_to_24"]:.1f} percent of citizens 18 to 24 '
             f'to {y24["65_and_over"]:.1f} percent of those 65 and over.')
    measure = ('Citizens 18 and over who said they voted, by age, United States, November 2020 and November 2024, in percent; '
               'the scale starts at 40 percent')
    body = artboards(s04_svg, view)
    notes = ['The two younger groups reported voting less in 2024 than in 2020; the two older groups held about level.',
             'These are rates people reported to a Census survey, which run higher than counts of ballots cast. Table A-1 '
             'publishes no margins of error, so a change of a point or two may sit within survey error.',
             'A ring marks 2020 and a dot marks 2024.']
    src = source_text('turnout-by-age')
    eq = table([('Age', lambda t: (e(t[1]), t[1]), 'h'),
                ('2020, %', lambda t: (f'{t[2]["voted_pct"]:.1f}', t[2]['voted_pct']), 'n'),
                ('2024, %', lambda t: (f'{t[3]["voted_pct"]:.1f}', t[3]['voted_pct']), 'n'),
                ('Change, points', lambda t: (signed(t[4]), t[4]), 'n')], data,
               'Reported voting by age, 2020 and 2024', f'{uid}-eq') + eq_extra(notes, src)
    return figure('S04', uid, title, measure, body, [e(n) for n in notes], src, eq, 'official statistic: what survey respondents reported')


# ================================================================================================ S05 small multiples
GROUPS = [('non_hispanic_white', 'Non-Hispanic White'), ('all_households', 'All households'), ('hispanic', 'Hispanic'), ('black', 'Black')]


def s05_series():
    """Each group's line, split wherever the base changes: the 2002 reweighting to 2000 Census controls, and for Black and
    non-Hispanic White householders the 2003 change in race categories. Segments are never joined (R16)."""
    rs = rows('homeownership-by-race')
    out = {}
    for g, _ in GROUPS:
        mine = sorted([r for r in rs if r['group'] == g],
                      key=lambda r: (r['year'], 0 if r['series_variant'] == 'original' else 1))
        segs, cur, base = [], [], None
        for r in mine:
            weights = 'old' if r['year'] < 2002 or (r['year'] == 2002 and r['series_variant'] == 'original') else 'new'
            b = (weights, r['race_definition'])
            if base is not None and b != base:
                segs.append(cur)
                cur = []
            cur.append(r)
            base = b
        segs.append(cur)
        out[g] = segs
    return out


def s05_numbers():
    S = s05_series()
    v = {g: {r['year']: r['rate_pct'] for seg in S[g] for r in seg if r['series_variant'] != 'revised_2000_census'} for g, _ in GROUPS}
    order = sorted(GROUPS, key=lambda g: -v[g[0]][2025])
    return S, v, order


@functools.lru_cache(maxsize=None)
def s05_body(W):
    S, v, order = s05_numbers()
    cols = 4 if W > 700 else (2 if W > 500 else 1)
    gut, gap = 36, 24
    pw = (W - gut - gap * (cols - 1)) / cols
    ph = 156 if cols == 4 else 132
    hdr = ['Dark line: the panel\'s group. Gray lines: the other three groups.']
    if tw(hdr[0]) > W:
        hdr = ['Dark line: the panel\'s group.', 'Gray lines: the other three groups.']
    head, top = 48, 30 + 16 * (len(hdr) - 1)
    lo, hi = 40, 80
    p = [lines(0, 14, hdr, 'nt', 16)]
    for i, (g, name) in enumerate(order):
        cx, cy = gut + (i % cols) * (pw + gap), top + (i // cols) * (ph + head + 38)
        X = lambda yr: cx + 3 + (yr - 1994) / (2025 - 1994) * (pw - 14)
        Y = lambda val: cy + head + (hi - val) / (hi - lo) * ph
        p.append(txt(cx, cy + 15, e(name), 'lab' if cols != 2 else 'lab-s'))
        p.append(txt(cx, cy + 33, f'{v[g][2025]:.1f}% in 2025', 'nt'))
        for t in range(lo, hi + 1, 10):
            yy = round(Y(t)) + 0.5
            p.append(f'<line class="grid" x1="{f(cx)}" x2="{f(cx + pw)}" y1="{f(yy)}" y2="{f(yy)}"/>')
            if i % cols == 0:
                p.append(txt(gut - 6, yy + 4.5, f'{t}%' if t == hi else str(t), 'tk', 'end'))
        for og, _ in GROUPS:
            if og != g:
                for seg in S[og]:
                    if len(seg) > 1:
                        p.append('<path class="ln-ctx" d="M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg) + '"/>')
        for seg in S[g]:
            if len(seg) > 1:
                p.append('<path class="ln-sm" d="M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg) + '"/>')
            for r in seg:
                p.append(f'<circle class="pt-sm" cx="{f(X(r["year"]))}" cy="{f(Y(r["rate_pct"]))}" r="2" data-key="{r["key"]}" '
                         f'data-value="{r["rate_pct"]}" data-mark="point" data-axis="y" data-scale="{g}"/>')
        p.append(txt(cx, Y(lo) + 18, '1994', 'tk'))
        p.append(txt(cx + pw, Y(lo) + 18, '2025', 'tk', 'end'))
        if g == 'black':
            nw, bk = v['non_hispanic_white'][2025], v['black'][2025]
            xg = X(2025) + 6
            p.append(f'<path class="brk" d="M{f(xg - 4)} {f(Y(nw))}H{f(xg)}V{f(Y(bk))}H{f(xg - 4)}"/>')
            p.append(txt(xg - 7, Y(57.5) + 4, f'{nw - bk:.1f} points', 'nt-b', 'end'))
    rows_n = math.ceil(len(order) / cols)
    H = top + rows_n * (ph + head + 38) - 14
    return ''.join(p), H


def s05_svg(W, view):
    S, v, order = s05_numbers()
    body, H = s05_body(W)
    lab = ('Four small charts of homeownership rates, 1994 to 2025, one per group, on one scale from 40 to 80 percent. Dark '
           'line: the panel\'s group; gray lines: the other three groups. '
           + '; '.join(f'{n} {v[g][2025]:.1f} percent in 2025' for g, n in order) + '. Each line breaks at the 2002 '
           'reweighting, and the Black and non-Hispanic White lines also break at the 2003 change in race categories. In 2025 '
           f'Black householders trailed non-Hispanic White householders by {v["non_hispanic_white"][2025] - v["black"][2025]:.1f} points.')
    return svg(W, H, f's05-{view}-{W}', lab, body)


def s05(view):
    uid = f'{view}-s05'
    S, v, order = s05_numbers()
    gap03 = v['non_hispanic_white'][2003] - v['black'][2003]
    gap25 = v['non_hispanic_white'][2025] - v['black'][2025]
    hgap03 = v['non_hispanic_white'][2003] - v['hispanic'][2003]
    hgap25 = v['non_hispanic_white'][2025] - v['hispanic'][2025]
    assert gap25 > gap03 and hgap25 < hgap03
    title = (f'In 2025 the homeownership gap between Black and non-Hispanic White householders was {gap25:.1f} points, '
             f'wider than the {gap03:.1f} points of 2003.')
    measure = ('Households that own their home, by race and ethnicity of the householder, United States, annual averages, '
               '1994 to 2025, in percent; one scale from 40 to 80 percent in every panel')
    reg_rows = []
    for g, name in order:
        a, b = v[g][2003], v[g][2025]
        gp = ((f'{v["non_hispanic_white"][2003] - a:.1f}', f'{v["non_hispanic_white"][2025] - b:.1f}') if g in ('black', 'hispanic')
              else ('reference', 'reference') if g == 'non_hispanic_white' else ('not compared', 'not compared'))
        reg_rows.append((name, a, b, b - a, gp))
    regt = ('<div class="tw"><table class="reg s05r"><caption>Since 2003, by group, with the gap to non-Hispanic White householders</caption>'
            '<thead><tr><th scope="col">Householder</th><th scope="col" class="n">2003, %</th><th scope="col" class="n">2025, %</th>'
            '<th scope="col" class="n">Change, points</th><th scope="col" class="n">Gap in 2003, points</th><th scope="col" class="n">Gap in 2025, points</th></tr></thead><tbody>'
            + ''.join(f'<tr><th scope="row">{e(n)}</th><td class="n" data-label="2003, %">{a:.1f}</td><td class="n" data-label="2025, %">{b:.1f}</td>'
                      f'<td class="n" data-label="Change, points">{signed(c)}</td><td class="n{" z" if gp[0][0].isalpha() else ""}" data-label="Gap in 2003">{gp[0]}</td>'
                      f'<td class="n{" z" if gp[1][0].isalpha() else ""}" data-label="Gap in 2025">{gp[1]}</td></tr>' for n, a, b, c, gp in reg_rows)
            + '</tbody></table></div>')
    body = artboards(s05_svg, view) + regt
    notes = [f'The gap between Hispanic and non-Hispanic White householders narrowed, from {hgap03:.1f} points in 2003 to {hgap25:.1f} in 2025.',
             'The Census Bureau asks readers to use caution comparing 2020 with other years, after interviews moved to the phone.',
             'Every line breaks at 2002, when the Bureau reweighted the survey to 2000 Census counts; 2002 shows both values, as '
             'first published and revised. The Black and non-Hispanic White lines break again at 2003, when race categories changed.',
             'The 2025 average leaves out October 2025, when no data were collected. Margins of error for 2025 are 0.5 points or less.',
             'Hispanic householders may be of any race. A dot marks each annual average.']
    src = source_text('homeownership-by-race')
    years = sorted({r['year'] for r in rows('homeownership-by-race')}, reverse=True)
    R = rows('homeownership-by-race')
    piv = []
    for y in years:
        for var in (['revised_2000_census', 'original'] if y == 2002 else ['standard']):
            row = {'year': y, 'var': var}
            for g, _ in GROUPS:
                m = next((r for r in R if r['year'] == y and r['group'] == g and r['series_variant'] == var), None)
                row[g] = m
            piv.append(row)
    vlab = {'standard': '', 'original': 'as first published', 'revised_2000_census': 'revised to 2000 Census weights'}
    eq = table([('Year', lambda r: (f'{r["year"]}' + (f' <span class="vs">{vlab[r["var"]]}</span>' if vlab[r['var']] else ''), r['year']), 'hid')]
               + [(f'{n}, %', (lambda g: (lambda r: ((f'{r[g]["rate_pct"]:.1f}' if r[g] else 'not given'), r[g]['rate_pct'] if r[g] else -1)))(g), 'n')
                  for g, n in GROUPS], piv, 'Homeownership rate by year and group', f'{uid}-eq') + eq_extra(
        ['Dark line: the panel\'s group. Gray lines: the other three groups.',
         f'Black panel, 2025: {gap25:.1f} points below non-Hispanic White householders.'] + notes, src)
    return figure('S05', uid, title, measure, body, [e(n) for n in notes], src, eq, 'official statistic from a Census Bureau survey')


# ================================================================================================ S06 comparison table
FAM = [('DQ', 'Quality of democracy'), ('GE', 'Government efficacy'), ('EP', 'Economic performance'), ('EQ', 'Income and wealth equality')]
CLS = {'up': ('c-up', 0, 'up'), 'slightly up': ('c-sup', 45, 'slightly up'), 'flat': ('c-flat', 90, 'flat'),
       'flat or down': ('c-fod', 135, 'flat or down'), 'down': ('c-down', 180, 'down'), 'mixed': ('c-mix', None, 'mixed'),
       'same as ii': ('c-same', None, 'same as scenario ii')}


def glyph(cls_name, key=None, field=None, cat=None, size=20):
    c, rot, _ = CLS[cls_name]
    mark = (f' data-key="{e(key)}" data-field="{field}" data-category="{e(cat)}" data-mark="cell"' if key else '')
    rect = f'<rect class="{c}" x="0.75" y="0.75" width="18.5" height="18.5"{mark}/>'
    if rot is not None:
        arrow = f'<path class="ga" transform="rotate({rot} 10 10)" d="M10 3.6 15.2 9.4H11.6V16.4H8.4V9.4H4.8Z"/>'
    elif cls_name == 'mixed':
        arrow = '<path class="ga" d="M10 2.8 14.2 7.4H5.8ZM10 17.2 5.8 12.6H14.2ZM8.6 7.2H11.4V12.8H8.6Z"/>'
    else:
        arrow = '<path class="ga" d="M5 7.4H15V9.4H5ZM5 10.6H15V12.6H5Z"/>'
    return (f'<svg class="gl" viewBox="0 0 20 20" width="{size}" height="{size}" aria-hidden="true" focusable="false">'
            f'{rect}{arrow}</svg>')


S06_GLOSS = {   # a few plain words under each scenario name, written by Oath & Action from the atlas's assumptions
    'i': 'Current law runs as written.',
    'ii': 'Some states and cities adopt reforms; federal rules stay the same.',
    'iii': 'Congress changes the filibuster and passes rules on elections, government and a child credit.',
    'iv-a': 'Fusion voting lets one candidate run on more than one party\'s ballot line; parties get public funding.',
    'iv-b': 'Rebuilds the career civil service, tax enforcement at the IRS, inspectors general (the officials who audit each '
            'agency), congressional staff and public digital teams.',
    'iv-c': 'Stronger enforcement on mergers, market power and labor law.',
    'iv-d': 'Changes made by amending the Constitution.',
    'iv-e': 'Forbearance: officials hold back from using every power they hold, with no new rules.',
}


def s06_numbers():
    rs = rows('scenarios-2030')
    lifts = [r['key'] for r in rs if r['key'] != 'i' and any(r[k + '_class'] in ('up', 'slightly up') for k, _ in FAM)]
    return rs, lifts


def s06(view):
    uid = f'{view}-s06'
    rs, lifts = s06_numbers()
    beyond = [r for r in rs if r['key'] != 'i']
    assert (len(lifts), len(beyond)) == (5, 7), lifts
    title = (f'If their assumptions hold, {WORDS[len(lifts)]} of the {WORDS[len(beyond)]} scenarios beyond the baseline would '
             'raise at least one outcome family by 2036.')
    measure = ('Direction each outcome family would take under each scenario, in the atlas\'s words, United States, '
               '2026 baseline to 2036; conditional directions that make no forecast')
    sub = 'Up means better for each family; for income and wealth equality, more equal.'
    key = ('<div class="gkey"><p class="gkh">The glyph is Oath &amp; Action\'s reading of the atlas\'s words</p><ul>'
           + ''.join(f'<li>{glyph(c)}<span>{e(CLS[c][2])}</span></li>' for c in ['up', 'slightly up', 'flat', 'flat or down', 'down', 'mixed', 'same as ii'])
           + '</ul></div>')
    head = '<thead><tr><th scope="col">Scenario</th>' + ''.join(f'<th scope="col">{e(n)}</th>' for _, n in FAM) + '</tr></thead>'
    body = []
    for r in rs:
        cells = ''.join(
            f'<td data-label="{e(n)}"><span class="cell">{glyph(r[k + "_class"], r["key"], k + "_class", r[k + "_class"])}'
            f'<span class="cw"><span class="vh">Our reading: {e(CLS[r[k + "_class"]][2])}. </span>'
            f'<span data-key="{e(r["key"])}" data-field="{k}" data-category="{e(r[k])}" data-mark="label">{e(r[k])}</span></span></span></td>'
            for k, n in FAM)
        body.append(f'<tr><th scope="row"><span class="sk">{e(r["key"])}</span><span class="sn">{e(r["name"])}</span>'
                    f'<span class="sg">{e(S06_GLOSS[r["key"]])}</span></th>{cells}</tr>')
    reg = (f'{key}<div class="tw"><table class="reg s06"><caption>Eight scenarios and four outcome families</caption>{head}'
           f'<tbody>{"".join(body)}</tbody></table></div>')
    notes = ['Each scenario gives a direction only if its assumptions hold. It makes no forecast and gives no odds. The table '
             'under "Show the table" lists every assumption.',
             'The four families are read one at a time and never added together.',
             'Where the atlas writes "same as scenario ii", the glyph marks that pointer and draws no direction of its own.',
             'Each glyph is a boxed arrow, so the reading holds on a black-and-white copy.']
    src = source_text('scenarios-2030')
    flat = [(r, k, n) for r in rs for k, n in FAM]
    eq = (table([('Scenario', lambda t: (f'{e(t[0]["key"])}, {e(t[0]["name"])}', t[0]['key']), 'h'),
                 ('Family', lambda t: (e(t[2]), t[2]), 't'),
                 ('The atlas\'s words', lambda t: (e(t[0][t[1]]), t[0][t[1]]), 't'),
                 ('Our reading', lambda t: (e(CLS[t[0][t[1] + "_class"]][2]), t[0][t[1] + '_class']), 't'),
                 ('The atlas\'s reason', lambda t: (e(t[0].get(t[1] + '_why', '')), ''), 't')], flat,
                'Every cell, with the atlas\'s reason', f'{uid}-eq')
          + table([('Scenario', lambda r: (f'{e(r["key"])}, {e(r["name"])}', r['key']), 'h'),
                   ('Assumptions', lambda r: ('; '.join(e(a) for a in r['assumptions']), ''), 't')], rs,
                  'What each scenario assumes', f'{uid}-eqa')
          + eq_extra([sub] + notes, src, extra=[('Glyphs', [f'{CLS[c][2]}: a boxed arrow' for c in ['up', 'slightly up', 'flat', 'flat or down', 'down']]
                                                + ['mixed: a boxed double arrow', 'same as scenario ii: a dashed box with two bars'])]))
    return figure('S06', uid, title, measure, reg, [e(n) for n in notes], src, eq, 'conditional directions: no forecast and no odds',
                  sub=sub)


# ================================================================================================ S07 tile map
STATUS = [('bans in all elections', 'all', 'Bans it in all elections'), ('bans in some elections', 'some', 'Bans it in some elections'),
          ('no ban', 'none', 'No state ban')]


def seps(t):
    """Thousands separators in counts that the source prints bare (Missouri's certified returns)."""
    return re.sub(r'\b\d{5,}\b', lambda m: f'{int(m.group()):,}', t)


def s07_numbers():
    R = byk('rcv-bans')
    cnt = Counter(r['status'] for r in R.values())
    years = defaultdict(list)
    for r in R.values():
        if r['prohibits_rcv']:
            years[int(r['enacted_year'])].append(r)
    return R, cnt, years


def s07_svg(W, view):
    R, cnt, years = s07_numbers()
    big = W >= 500
    gp = T['tile_gap'] if big else 2
    t = T['tile'] if big else int((W + gp) / 12) - gp
    p = []
    for tl in sorted(TILES, key=lambda x: (x['row'], x['col'])):
        r = R[tl['code']]
        k = next(s[1] for s in STATUS if s[0] == r['status'])
        x, y = tl['col'] * (t + gp), tl['row'] * (t + gp)
        tip = f'{r["name"]}: {next(s[2] for s in STATUS if s[0] == r["status"]).lower()}'
        if r['prohibits_rcv']:
            tip += f' ({seps(r["measure"])}, {int(r["enacted_year"])})'
        p.append(f'<g class="tile t-{k}"><title>{e(tip)}</title>'
                 f'<rect x="{x}" y="{y}" width="{t}" height="{t}" data-key="{tl["code"]}" data-field="status" '
                 f'data-category="{e(r["status"])}" data-mark="cell"/>')
        if not big:
            p.append(txt(x + t / 2, y + t / 2 + 4.5, tl['code'], 'tc', 'middle'))
        else:
            p.append(txt(x + t / 2, y + (16 if r['prohibits_rcv'] else 25), tl['code'], 'tc', 'middle'))
            if r['prohibits_rcv']:
                p.append(txt(x + t / 2, y + 32, '’' + str(int(r['enacted_year']))[2:], 'ty', 'middle'))
        p.append('</g>')
    Wd = 12 * (t + gp) - gp
    H = 8 * (t + gp) - gp
    if big:
        p.append(txt(0, H + 22, 'Two digits under a code give the year the ban became law.', 'nt'))
        H += 30
    lab = (f'Tile map of the 50 states and DC, one square each, the same size whatever the state\'s area. '
           f'{cnt["bans in all elections"]} states ban ranked-choice voting in all elections, {cnt["bans in some elections"]} in '
           f'some (Ohio and Tennessee), and {cnt["no ban"] - 1} states and DC have no state ban, as of November 2026.')
    return svg(Wd, H, f's07-{view}-{W}', lab, ''.join(p))


def s07(view):
    uid = f'{view}-s07'
    R, cnt, years = s07_numbers()
    nban = cnt['bans in all elections'] + cnt['bans in some elections']
    assert (nban, cnt['bans in all elections'], cnt['no ban'] - 1) == (19, 17, 31)
    title = f'Nineteen states ban ranked-choice voting, {cnt["bans in all elections"]} of them in all elections, as of November 2026.'
    measure = 'States that prohibit ranked-choice voting by statute or constitution, 50 states and DC, as of November 2026'
    words = {'bans in all elections': str(cnt['bans in all elections']), 'bans in some elections': str(cnt['bans in some elections']),
             'no ban': f'{cnt["no ban"] - 1} states and DC'}
    keyl = ''.join(f'<li><span class="tsw tsw-{k}" aria-hidden="true"></span><span>{e(lab)}</span><b>{words[s]}</b></li>'
                   for s, k, lab in STATUS)
    reg = ['<table class="reg s07r"><caption>Bans by year enacted</caption><thead><tr><th scope="col">Year</th>'
           '<th scope="col" class="n">Bans</th><th scope="col">States</th></tr></thead><tbody>']
    for y in sorted(years):
        sts = sorted(years[y], key=lambda r: r['name'])
        names = ', '.join(e(r['name']) + (' (some elections)' if r['scope'] == 'some' else '') for r in sts)
        reg.append(f'<tr><th scope="row" class="tn">{y}</th><td class="n">{len(sts)}</td><td>{names}</td></tr>')
    reg.append(f'</tbody><tfoot><tr><th scope="row">All</th><td class="n">{nban}</td><td></td></tr></tfoot></table>')
    body = (f'<ul class="tkey">{keyl}</ul><div class="s07"><div class="mapw">{artboards(s07_svg, view)}</div>'
            f'<div class="s07reg"><div class="tw">{"".join(reg)}</div></div></div>')
    notes = ['Ranked-choice voting: voters rank candidates in order; if no one wins a majority of first choices, the last-place '
             'candidate drops out and those ballots count for their next choice, round by round.',
             'A state with no ban may still keep its cities from adopting it, because many cities need the state\'s permission. '
             'The map shows bans only.',
             'Ohio\'s ban leaves an opening for home-rule cities, at the cost of state funds; Tennessee\'s names statewide and local '
             'offices only.',
             'Missouri\'s ban is in its constitution; the other 18 are statutes.',
             'Each square is one state, the same size whatever its area.']
    src = (source_text('rcv-bans') + ' Ballotpedia is a secondary source; the atlas cites the National Conference of State '
           'Legislatures.')
    data = sorted(R.values(), key=lambda r: (r['status'] == 'no ban', r['name']))
    eq = table([('State', lambda r: (e(r['name']), r['name']), 'h'),
                ('Status', lambda r: (f'<span data-key="{r["key"]}" data-field="status" data-category="{e(r["status"])}" data-mark="label">{e(r["status"])}</span>', r['status']), 't'),
                ('Enacted', lambda r: ((str(int(r['enacted_year'])) if r['prohibits_rcv'] else 'no ban'), r['enacted_year'] or 0), 'n'),
                ('Measure', lambda r: (e(seps(r['measure'])) if r['measure'] else 'no ban', r['measure']), 't'),
                ('Scope', lambda r: (e(r['scope_note']), r['scope_note']), 't')], data,
               'Every state and DC', f'{uid}-eq', sortable=True, sort_col=1, sort_dir='ascending') + eq_extra(
        ['Two digits under a code give the year the ban became law.'] + notes, src,
        extra=[('Key', [f'Dark square: bans it in all elections ({words["bans in all elections"]}). Gray square: bans it in some '
                        f'elections ({words["bans in some elections"]}). Outlined square: no state ban ({words["no ban"]}).'])])
    return figure('S07', uid, title, measure, body, [e(n) for n in notes], src, eq, 'a secondary list compiled by Ballotpedia')


# ================================================================================================ S08 unit chart
UNIT_KIND = {'toward voters': 'tow', 'away from voters': 'awy', 'voters kept existing rules': 'kept', 'mixed': 'mix', 'pending': 'pend'}


def unit(r):
    """One record, one mark: toward voters a square, away from voters a dot, kept a hollow square, mixed a hatched square,
    pending a dashed square. RL47, which stands for 19 state bans, is a ringed dot."""
    k = UNIT_KIND[r['direction']]
    a = f'data-key="{r["key"]}" data-category="{e(r["direction"])}" data-mark="unit"'
    u = T['unit']
    if r['key'] == 'RL47':
        shape = f'<circle class="u-roll" cx="7" cy="7" r="5.5" {a}/><circle class="u-awy" cx="7" cy="7" r="2"/>'
    elif k == 'tow':
        shape = f'<rect class="u-tow" x="0.5" y="0.5" width="13" height="13" {a}/>'
    elif k == 'awy':
        shape = f'<circle class="u-awy" cx="7" cy="7" r="6.5" {a}/>'
    elif k == 'kept':
        shape = f'<rect class="u-kept" x="0.75" y="0.75" width="12.5" height="12.5" {a}/>'
    elif k == 'mix':
        shape = (f'<rect class="u-mix" x="0.75" y="0.75" width="12.5" height="12.5" {a}/>'
                 '<path class="u-hatch" d="M1 9 9 1M1 13.5 13.5 1M5 13.5 13.5 5"/>')
    else:
        shape = f'<rect class="u-pend" x="0.75" y="0.75" width="12.5" height="12.5" {a}/>'
    return f'<svg class="u" viewBox="0 0 {u} {u}" aria-hidden="true" focusable="false">{shape}</svg>'


def s08_numbers():
    rs = rows('rule-changes')
    cols = ['early'] + list(range(2010, 2027))
    col_of = lambda r: 'early' if r['year'] < 2010 else r['year']
    per = Counter(col_of(r) for r in rs)
    return rs, cols, col_of, per


def s08(view):
    uid = f'{view}-s08'
    rs, cols, col_of, per = s08_numbers()
    cnt = DS['rule-changes']['counts']
    L = log_facts()
    assert (cnt['toward voters'], cnt['away from voters'], L['n'], L['early'], L['n_bans']) == (24, 24, 64, 10, 17)
    title = (f'The atlas\'s log codes {cnt["toward voters"]} of its {L["n"]} rule changes as moving toward voters and '
             f'{cnt["away from voters"]} as moving away.')
    measure = ('Rule changes in our atlas\'s repair log, one mark per change, by year and the atlas\'s direction code, '
               'United States, 1965 to the November 3, 2026 ballot')
    bands = [('Toward voters', ['toward voters'], 'tow'), ('Away from voters', ['away from voters'], 'awy'),
             ('Neither way', ['voters kept existing rules', 'mixed', 'pending'], 'nei')]
    per_txt = ', '.join(f'{"1965 and 1988" if c == "early" else c}: {per.get(c, 0)}' for c in cols)
    kept24 = sum(1 for r in rs if r['year'] == 2024 and r['direction'] == 'voters kept existing rules')
    assert kept24 == 8
    out = [f'<div class="uc" style="--nc:{len(cols) - 1}" role="img" aria-label="' + e(
        f'Unit chart, one mark per entry in the atlas\'s log, by year. Toward voters, squares: {cnt["toward voters"]}. Away from '
        f'voters, dots: {cnt["away from voters"]}; a ringed dot in 2026 is one entry that stands for 19 state bans. Neither way: '
        f'voters kept existing rules {cnt["voters kept existing rules"]} (hollow squares; voters turned down {kept24} ballot measures '
        f'in 2024), mixed {cnt["mixed"]} (hatched), pending {cnt["pending"]} on the November 3, 2026 ballot (dashed). '
        f'Entries per year: {per_txt}.') + '">']
    order = {'toward voters': 0, 'away from voters': 0, 'voters kept existing rules': 0, 'mixed': 1, 'pending': 2}
    for name, dirs, k in bands:
        n = sum(cnt[d] for d in dirs)
        if k == 'nei':
            sub = ''.join(f'<span class="ukey">{unit_key(d)}{e(lab)} {cnt[d]}</span>' for d, lab in
                          [('voters kept existing rules', 'Voters kept rules'), ('mixed', 'Mixed'), ('pending', 'Pending')])
            label = f'<p class="ub-n">{e(name)} <b>{n}</b></p><p class="ub-s">{sub}</p>'
        else:
            label = f'<p class="ub-n">{unit_key(dirs[0])}{e(name)} <b>{n}</b></p>'
        cells = []
        for i, c in enumerate(cols):
            mine = sorted([r for r in rs if col_of(r) == c and r['direction'] in dirs], key=lambda r: (order[r['direction']], r['date']))
            cells.append(f'<div class="uc-col" style="grid-column:{i + 1}">{"".join(unit(r) for r in mine)}</div>')
        notes = ''
        if k == 'awy':
            c0 = cols.index(2026) + 1
            notes = ('<p class="uc-nt" style="grid-column:2 / -1">The ringed dot is one entry that stands for 19 state bans</p>'
                     f'<span class="uc-br" style="grid-column:{c0} / -1" aria-hidden="true"></span>')
        if k == 'nei':
            c0 = cols.index(2024) + 1
            notes = (f'<p class="uc-nt" style="grid-column:2 / {c0 + 1}">Voters turned down {kept24} ballot measures in 2024</p>'
                     f'<span class="uc-br" style="grid-column:{c0} / {c0 + 1}" aria-hidden="true"></span>')
        out.append(f'<div class="uc-band b-{k}"><div class="uc-lab">{label}</div>'
                   f'<div class="uc-cols">{notes}{"".join(cells)}</div></div>')
    base = ''.join(f'<span class="ubase{" z" if not per.get(c) else ""}" style="grid-column:{i + 1}">{per.get(c, 0)}</span>'
                   for i, c in enumerate(cols))
    out.append(f'<div class="uc-band uc-base"><div class="uc-lab"><p class="ub-b">All entries, per year</p></div>'
               f'<div class="uc-cols">{base}</div></div>')
    yl = []
    for i, c in enumerate(cols):
        if c == 'early':
            yl.append('<span class="uy uy0" style="grid-column:1">1965<br>1988</span><span class="uy-brk" style="grid-column:1" aria-hidden="true">//</span>')
        else:
            show = 'w' if c % 2 == 0 else ''
            if c in (2012, 2016, 2020):
                show += ' n'
            if c == 2026:
                show = 'w n end'
            if show:
                yl.append(f'<span class="uy {show}" style="grid-column:{i + 1}">{c}</span>')
    out.append(f'<div class="uc-band uc-axis"><div class="uc-lab"></div><div class="uc-cols">{"".join(yl)}</div></div>')
    out.append('</div>')
    body = ''.join(out)
    notes = log_notes()[:1] + [
        f'Toward and away each hold {cnt["toward voters"]} of the {L["n"]} entries. The other {L["n"] - 48}: voters kept existing '
        f'rules in {cnt["voters kept existing rules"]}, {cnt["mixed"]} are mixed and {cnt["pending"]} are pending.',
        log_notes()[1] + f' That entry is dated March 2026, though {WORDS[L["early"]]} of the other {L["n_bans"]} bans it stands '
        'for passed before 2025.',
        'The first column holds the two oldest entries, 1965 and 1988; 2011, 2012 and 2023 have none. One entry rests on a source '
        'the atlas did not check.']
    src = source_text('rule-changes', drop=())
    data = sorted(rs, key=lambda r: r['date'], reverse=True)
    eq = table([('ID', lambda r: (r['key'], r['key']), 'hid'), ('Date', lambda r: (date_words(r['date']), r['date']), 't'),
                ('Where', lambda r: (e(r['jurisdiction']), r['jurisdiction']), 't'),
                ('Direction', lambda r: (e(r['direction']), r['direction']), 't'),
                ('How', lambda r: (e(r['instrument_group']), r['instrument_group']), 't'),
                ('What changed', lambda r: (e(r['rule']), ''), 't')], data,
               'The 64 rule changes in the repair log, newest first', f'{uid}-eq', sortable=True, sort_col=1) + eq_extra(
        ['The ringed dot is one entry that stands for 19 state bans.', f'Voters turned down {kept24} ballot measures in 2024.',
         f'All entries, per year: {per_txt}.'] + notes, src,
        extra=[('How the atlas codes direction', [L['coding'], L['neutral'],
                                                  'A map redrawn in the middle of a decade counts as away from voters whichever party draws it: '
                                                  'Texas\'s HB 4 (August 2025) and California\'s Proposition 50 (November 2025) both count as away.']),
               ('Key', ['Squares: toward voters. Dots: away from voters. Hollow squares: voters kept existing rules. Hatched squares: '
                        'mixed. Dashed squares: pending.'])])
    return figure('S08', uid, title, measure, body, [e(n) for n in notes], src, eq, 'the atlas\'s dated log, directions coded by the atlas',
                  coding=log_block())


def unit_key(d):
    k = UNIT_KIND[d]
    cls = {'tow': '<rect class="u-tow" x="0.5" y="0.5" width="13" height="13"/>',
           'awy': '<circle class="u-awy" cx="7" cy="7" r="6.5"/>',
           'kept': '<rect class="u-kept" x="0.75" y="0.75" width="12.5" height="12.5"/>',
           'mix': '<rect class="u-mix" x="0.75" y="0.75" width="12.5" height="12.5"/><path class="u-hatch" d="M1 9 9 1M1 13.5 13.5 1M5 13.5 13.5 5"/>',
           'pend': '<rect class="u-pend" x="0.75" y="0.75" width="12.5" height="12.5"/>'}[k]
    return f'<svg class="uk" viewBox="0 0 14 14" aria-hidden="true" focusable="false">{cls}</svg>'


# ================================================================================================ S09 timeline
def ev_short(t):
    return t.split(' (')[0]


def first_clause(m):
    """The first clause of the atlas's 'what it did', for the phone list (no words added)."""
    m = re.split(r'(?<=\.)\s', m.split('; ')[0])[0].rstrip('.')
    if len(m) > 110:
        cut = m.rfind(', ', 0, 110)
        m = m[:cut] if cut > 40 else m[:m.rfind(' ', 0, 110)]
    return m + '.'


@functools.lru_cache(maxsize=None)
def s09_body(W):
    ds = DS['history-events']
    evs = ds['rows']
    threads = ds['threads']
    p = []
    r_ev = T['radius']['event']
    if W >= 500:
        # four lanes side by side; time runs down on one true scale
        gut, gap = 44, 16
        cw = (W - gut - gap * 3) / 4
        heads = [[th['label']] + wrap(th['question'], cw - 4, 13, 400) for th in threads]
        hh = max(len(h) for h in heads) * 17 + 8
        top = hh + 18
        ppy = 4.1 if W > 700 else 4.6
        Y = lambda dy: top + (dy - 1870) * ppy
        for yr in range(1870, 2027, 20):
            yy = round(Y(yr)) + 0.5
            p.append(f'<line class="grid" x1="0" x2="{W}" y1="{f(yy)}" y2="{f(yy)}"/>')
            p.append(txt(0, yy - 5, str(yr), 'tk'))
        bottom = Y(2027)
        for i, th in enumerate(threads):
            cx = gut + i * (cw + gap)
            p.append(txt(cx, 15, e(heads[i][0]), 'lab'))
            p.append(lines(cx, 33, heads[i][1:], 'nt', 17))
            lx = cx + 6
            p.append(f'<line class="lane" x1="{f(lx)}" x2="{f(lx)}" y1="{f(top - 8)}" y2="{f(Y(2026.6))}"/>')
            mine = sorted([r for r in evs if r['thread'] == th['id']], key=lambda r: r['date'])
            prev = top - 30
            placed = []
            last_y, side = -99, 1
            for r in mine:
                rows_ = wrap(ev_short(r['title']), cw - 24, 13, 400)
                h = 16 * (1 + len(rows_))
                yd = Y(dyear(r['date']))
                if yd - last_y < 2 * r_ev + 1:    # dots closer than one diameter step aside, along the lane's width only
                    side = -side
                    dx = 4 * side
                else:
                    side, dx = 1, 0
                last_y = yd
                by_ = max(yd - 8, prev + 8)
                placed.append((r, yd, by_, rows_, h, dx))
                prev = by_ + h
            bottom = max(bottom, prev + 6)
            for r, yd, by_, rows_, h, dx in placed:
                p.append(f'<path class="lead" d="M{f(lx + dx + 6)} {f(yd)}L{f(cx + 18)} {f(by_ + 7)}"/>')
                p.append(txt(cx + 21, by_ + 11, str(r['year']), 'yr'))
                p.append(lines(cx + 21, by_ + 27, rows_, 'ev', 16))
            for r, yd, by_, rows_, h, dx in placed:
                p.append(f'<circle class="ev-pt" cx="{f(lx + dx)}" cy="{f(yd)}" r="{r_ev}" data-key="{r["key"]}" data-field="year" '
                         f'data-value="{dyear(r["date"]):.4f}" data-mark="point" data-axis="y"/>')
        H = bottom + 4
    else:
        # a strip on the true time scale, then the four thread questions and every event in date order
        lw = 92
        x0, x1 = lw, W - 6
        X = lambda dy: x0 + (dy - 1870) / (2027 - 1870) * (x1 - x0)
        for i, th in enumerate(threads):
            y = 18 + i * 26
            p.append(txt(0, y + 5, e(th['label']), 'lab-s'))
            p.append(f'<line class="lane" x1="{x0}" x2="{x1}" y1="{y}" y2="{y}"/>')
        ya = 18 + 4 * 26 - 8
        p.append(f'<line class="base" x1="{x0}" x2="{x1}" y1="{ya + .5}" y2="{ya + .5}"/>')
        for yr, anc in ((1870, 'start'), (1950, 'middle'), (2026, 'end')):
            p.append(txt(X(yr + (0.6 if yr == 2026 else 0)), ya + 18, str(yr), 'tk', anc))
        for i, th in enumerate(threads):
            y = 18 + i * 26
            for r in sorted([r for r in evs if r['thread'] == th['id']], key=lambda r: r['date']):
                p.append(f'<circle class="ev-pt sm" cx="{f(X(dyear(r["date"])))}" cy="{y}" r="{T["radius"]["event_strip"]}" '
                         f'data-key="{r["key"]}" data-field="year" data-value="{dyear(r["date"]):.4f}" data-mark="point" data-axis="x"/>')
        y = ya + 46
        for th in threads:
            qs = wrap(f'{th["label"]}: {th["question"]}', W - 4, 13, 400)
            p.append(lines(0, y, qs, 'nt', 16))
            y += 16 * len(qs) + 4
        y += 14
        p.append(txt(0, y, 'Every change, in date order', 'th'))
        y += 10
        thl = {t['id']: t['label'] for t in threads}
        for r in sorted(evs, key=lambda r: r['date']):
            rows_ = wrap(ev_short(r['title']), W - 46, 13, 600)
            did = wrap(first_clause(r['mechanism']), W - 46, 13, 400)
            p.append(f'<line class="rq" x1="0" x2="{W}" y1="{f(y + .5)}" y2="{f(y + .5)}"/>')
            p.append(txt(0, y + 18, str(r['year']), 'yr'))
            p.append(txt(44, y + 18, e(thl[r['thread']]), 'nt'))
            p.append(lines(44, y + 34, rows_, 'lab-s', 16))
            p.append(lines(44, y + 34 + 16 * len(rows_), did, 'ev', 16))
            y += 28 + 16 * (len(rows_) + len(did))
        H = y + 4
    return ''.join(p), H


def s09_svg(W, view):
    ds = DS['history-events']
    body, H = s09_body(W)
    lab = ('Timeline of 24 rule changes from 1870 to 2026 on four threads, six each, one dot per change on a true time scale. '
           + ' '.join(f'{th["label"]} ({th["question"]}): ' + ', '.join(
               f'{ev_short(r["title"])} ({r["year"]})' for r in sorted(ds['rows'], key=lambda r: r['date']) if r['thread'] == th['id']) + '.'
               for th in ds['threads']))
    return svg(W, H, f's09-{view}-{W}', lab, body)


def s09(view):
    uid = f'{view}-s09'
    ds = DS['history-events']
    cnt = Counter(r['thread'] for r in ds['rows'])
    assert set(cnt.values()) == {6} and len(ds['rows']) == 24
    title = ('The atlas traces 24 documented rule changes from 1870 to 2026 on four threads: who counts, who governs, who owns '
             'and who checks.')
    measure = ('Rule changes in our atlas\'s history, by thread and date, United States, February 3, 1870 to June 29, 2026; '
               'one dot per change on a true time scale')
    body = artboards(s09_svg, view)
    notes = ['Every event is on the public record: a statute, a ruling, a constitutional text or another official record. The '
             'atlas chose which 24 to date.',
             'Names are shortened at the first bracket; the table gives them whole, with what each change did.',
             'The four threads ask who gets to vote, how votes become seats, who keeps the gains and who can check an abuse of power.']
    src = source_text('history-events')
    th = {t['id']: t['label'] for t in ds['threads']}

    def mech(r):
        m = r['mechanism']
        if '5.2%' in m:
            m += ' (5.2 percent as first published; the revised Census table reads 5.1.)'
        return e(m)
    eq = table([('ID', lambda r: (r['key'], r['key']), 'hid'), ('Date', lambda r: (date_words(r['date']), r['date']), 't'),
                ('Thread', lambda r: (e(th[r['thread']]), r['thread']), 't'), ('Change', lambda r: (e(r['title']), r['title']), 't'),
                ('What it did', lambda r: (mech(r), ''), 't')], ds['rows'], 'The 24 events in date order', f'{uid}-eq',
               sortable=True, sort_col=1, sort_dir='ascending') + eq_extra(
        ['Event numbers E01 to E24 are ours, in date order.'] + notes, src,
        extra=[('The four threads', [f'{t["label"]}: {t["question"]}' for t in ds['threads']])])
    return figure('S09', uid, title, measure, body, [e(n) for n in notes], src, eq, 'documented: each event is on the public record')


# ================================================================================================ S10 evidence register
GRADES = [('documented', 'Documented', 'on the public record', 'g1'), ('well-supported', 'Well supported', 'strong research evidence', 'g2'),
          ('plausible', 'Plausible', 'some evidence', 'g3'), ('contested', 'Contested', 'evidence disputed', 'g4')]


def s10_numbers():
    rs = rows('claims-by-grade')
    tot = DS['claims-by-grade']['totals']
    n = sum(tot.values())
    share_all = 100 * tot['documented'] / n
    data = sorted(rs, key=lambda r: (-r['documented'] / r['value'], r['key']))
    return data, n, share_all


def s10(view):
    uid = f'{view}-s10'
    data, n, share_all = s10_numbers()
    lo, hi = data[-1], data[0]
    slo, shi = 100 * lo['documented'] / lo['value'], 100 * hi['documented'] / hi['value']
    assert (lo['key'], hi['key']) == ('PW16', 'PW12') and all(r['documented'] / r['value'] > 0.5 for r in data)
    title = (f'Most claims behind every everyday answer are documented on the public record, from {slo:.0f} percent for '
             f'algorithms to {shi:.0f} percent for tap water.')
    measure = (f'Share of the claims behind each of our atlas\'s 16 everyday answers, by evidence grade, {n} claims, United States, '
               'checked through October 15, 2026')
    key = ('<ul class="grkey">' + ''.join(f'<li><span class="gsw k-{k}" aria-hidden="true"></span><b>{lab}</b> {e(mean)}</li>' for _, lab, mean, k in GRADES)
           + '</ul><p class="gkn">Here the bars follow the grade code, darkest for documented, in place of the usual rule that '
           'the darkest ink marks what the title names.</p>')
    cols = [dict(head='Everyday answer', kind='h', label='',
                 cell=lambda r: f'<span class="aq">{e(r["title"])}</span><span class="aqq">{e(r["question"])}</span>'),
            dict(head='Claims', kind='n', label='Claims',
                 cell=lambda r: f'<span data-key="{r["key"]}" data-value="{r["value"]}" data-mark="label">{r["value"]}</span>'),
            dict(head='Evidence mix', kind='bar', label='',
                 cell=lambda r: reg_bar(r['key'], [(g, r[g], k) for g, _, _, k in GRADES], r['value'])),
            dict(head='Documented, %', kind='n', label='Documented, %', cell=lambda r: f'<b>{100 * r["documented"] / r["value"]:.1f}</b>'),
            dict(head=f'Documented share compared with all claims ({share_all:.1f}%)', kind='n', label='Compared with all claims',
                 cell=lambda r: signed(100 * r['documented'] / r['value'] - share_all))]
    tot = DS['claims-by-grade']['totals']
    foot = ['<th scope="row" class="c-h">All 16 answers</th>', f'<td class="n" data-label="Claims">{n}</td>',
            '<td class="c-bar"><span class="reg-track" aria-hidden="true">'
            + ''.join(f'<span class="seg k-{k}" style="width:{100 * tot[g] / n:.4f}%"></span>' for g, _, _, k in GRADES) + '</span></td>',
            f'<td class="n" data-label="Documented, %"><b>{share_all:.1f}</b></td>', '<td class="n" data-label="Compared with all claims">0.0</td>']
    reg = key + ranked_register(f'{uid}-reg', 'Evidence behind each everyday answer, most documented first', cols, [(None, data)],
                                foot, cls='reg-share')
    notes = ['Grades are the atlas\'s own, defined on its evidence page. Each grade covers one claim, and the count of claims '
             'prints beside every share.',
             'The grades step from dark to light, and contested claims add a hatch, so the mix reads on a black-and-white copy.']
    src = source_text('claims-by-grade')
    eq = table([('Answer', lambda r: (e(r['title']), r['title']), 'h'), ('Claims', lambda r: (str(r['value']), r['value']), 'n')]
               + [(lab, (lambda g: (lambda r: (str(r[g]), r[g])))(g), 'n') for g, lab, _, _ in GRADES]
               + [('Documented, %', lambda r: (f'{100 * r["documented"] / r["value"]:.1f}', 100 * r['documented'] / r['value']), 'n')],
               data, 'Claims by grade for each answer', f'{uid}-eq', sortable=True, sort_col=6) + eq_extra(
        notes, src, extra=[('Grades', [f'{lab}: {mean}' for _, lab, mean, _ in GRADES])])
    return figure('S10', uid, title, measure, reg, [e(n) for n in notes], src, eq, 'the atlas\'s own register of graded claims')


# ================================================================================================ plates and views
WHY = {
    'S01': 'One figure carries the story; the party register beside it shows the agreement with two bars on one scale, and the votes '
           'sit underneath as dated context.',
    'S02': 'A line shows a level over time; notes inside the plot name the dated events, and breaks in method stay visible.',
    'S03': 'A ranked register answers "who" by grouping the instruments by who acted; each glyph in a bar is one change, and the '
           'direction columns read across a row and down a column.',
    'S04': 'Two dots per row show the level and the change at once; the change column says it in words and numbers.',
    'S05': 'Four panels on one scale keep each group readable on its own; the register under them carries the gaps.',
    'S06': 'A comparison table keeps the atlas\'s words in every cell; a boxed arrow adds a reading that survives a photocopy.',
    'S07': 'Equal tiles give every state the same weight, and the register beside the map lists the bans by the year they came.',
    'S08': 'One mark per record lets a reader count; three bands on one year axis keep direction in position and shape, and the '
           'base row shows how many entries each year holds.',
    'S09': 'Four lanes on one true time scale show when each thread changed, and every event is named on the drawing.',
    'S10': 'A register sorted by documented share answers the question row by row, with the claim count and the full mix in each row.',
}
BUILDERS = {'S01': s01, 'S02': s02, 'S03': s03, 'S04': s04, 'S05': s05, 'S06': s06, 'S07': s07, 'S08': s08, 'S09': s09, 'S10': s10}


def view_links(cur):
    return ' · '.join(f'<a href="#{v}">{t}</a>' for v, t in VIEWS if v != cur)


def contents(view):
    rws = []
    for s in D['specimens']:
        ds = DS[s['dataset']]
        src = 'Oath & Action\'s atlas' if ds['kind'] == 'v7' else ('Ballotpedia, secondary' if s['id'] == 'S07' else 'U.S. Census Bureau')
        rws.append(f'<tr><th scope="row" class="tn"><a class="cl" href="#{view}-{s["id"].lower()}">{s["id"]}</a></th><td data-label="Form">{e(s["form"])}</td>'
                   f'<td data-label="Reader question">{e(s["reader_question"])}</td><td data-label="Data">{e(src)}</td>'
                   f'<td data-label="Evidence">{e(ds["evidence"])}</td></tr>')
    return ('<div class="tw"><table class="reg rf contents"><caption class="vh">The ten charts on this page</caption><thead><tr><th scope="col">ID</th>'
            '<th scope="col">Form</th><th scope="col">Reader question</th><th scope="col">Data</th><th scope="col">Evidence</th></tr></thead>'
            f'<tbody>{"".join(rws)}</tbody></table></div>')


HOWTO_SHORT = [
    ('The label', 'says what kind of evidence a chart holds: a Finding is measured; an Estimate depends on stated assumptions.'),
    ('The title', 'is the claim. "Would" and "may" mark claims that are less sure.'),
    ('The measure line', 'says what was counted, where and when, and whether the scale starts above zero.'),
    ('The darkest ink', 'marks what the title names; gray gives context.'),
    ('The register and notes', 'print every number and say what the chart leaves out.'),
    ('Red', 'marks the single point a title names, when a chart uses it. Red never means a party, good or bad.'),
]


def howto_short(view):
    items = ''.join(f'<li><b>{e(a)}</b> {e(b)}</li>' for a, b in HOWTO_SHORT)
    return (f'<details class="lead-d howto" id="{view}-howto" open><summary>How to read our charts</summary>'
            f'<ol class="howto-l">{items}</ol><p class="howto-m">The full guide is on the '
            '<a href="#system-read">System view, section 8</a>.</p></details>')


def specimen_plates(view):
    out = []
    for sid in [s['id'] for s in D['specimens']]:
        out.append(plate(view, sid, BUILDERS[sid](view), WHY[sid]))
    return ''.join(out)


def view_white():
    return (f'<section class="view g g-white" data-view-root="white" data-title="Register chart system" aria-labelledby="white-h"><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02</p><h1 class="display" id="white-h" tabindex="-1">Register</h1>'
            '<p class="deck">Register leads with the numbers. Every chart sits in the same frame, so a reader learns its parts once, '
            'and every chart carries a register: the figures a reader would look up, set in a table under or beside it.</p>'
            f'<p class="views">Other views: {view_links("white")}</p></header>'
            f'<div class="lead">{howto_short("white")}<details class="lead-d idx" open><summary>The ten charts on this page</summary>'
            f'{contents("white")}</details></div>'
            f'<div class="plates">{specimen_plates("white")}</div></div></section>')


def view_newsprint():
    return ('<section class="view g g-news" data-view-root="newsprint" data-title="Newsprint · Register chart system" aria-labelledby="news-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="news-h" tabindex="-1">On Newsprint</h1>'
            '<p class="deck">The same ten charts from the same generators, with the ground changed. Secondary text stays Deep Stone, '
            'which measures 5.49:1 here; Verdigris measures 3.37:1 and Stone 4.29:1, so neither carries text.</p>'
            f'<p class="views">Other views: {view_links("newsprint")}</p></header>'
            f'<div class="lead">{howto_short("newsprint")}</div>'
            f'<div class="plates">{specimen_plates("newsprint")}</div></div></section>')


def view_dark():
    t = G['dark']
    sw = [('Newsprint', 'Ink: titles, labels, the named series; away-from-voters dots', t['ink']), ('Dim Newsprint', 'Secondary text', t['sec']),
          ('Stone toward Newsprint', 'Context lines, hollow squares', t['ctx']), ('Verdigris lifted 4%', 'Toward-voters squares', t['tow'])]
    rowsd = ''.join(f'<tr><th scope="row"><span class="sw2" style="background:{h}" aria-hidden="true"></span>{e(n)}</th><td data-label="Job">{e(j)}</td>'
                    f'<td data-label="Hex">{h}</td><td class="n" data-label="Contrast">{contrast(h, t["bg"]):.2f}</td>'
                    f'<td class="n" data-label="OKLab L">{oklab(h)[0]:.3f}</td></tr>' for n, j, h in sw)
    pal = ('<div class="tw"><table class="reg rf dpal"><caption>The Charcoal palette, measured against #121212</caption><thead><tr>'
           '<th scope="col">Ink</th><th scope="col">Job</th><th scope="col">Hex</th><th scope="col" class="n">Contrast</th>'
           f'<th scope="col" class="n">OKLab L</th></tr></thead><tbody>{rowsd}</tbody></table></div>')
    plates = plate('dark', 'S02', s02('dark'), WHY['S02']) + plate('dark', 'S03', s03('dark'), WHY['S03'])
    return ('<section class="view g g-dark" data-view-root="dark" data-title="Charcoal · Register chart system" aria-labelledby="dark-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="dark-h" tabindex="-1">On Charcoal</h1>'
            '<p class="deck">Two charts on Charcoal: a line and a register. Newsprint carries the subject, the text and the dots for changes '
            f'away from voters. Verdigris, lifted 4% toward Newsprint, carries the squares for changes toward voters at '
            f'{contrast(t["tow"], t["bg"]):.2f}:1. The two differ in shape as well as lightness, and every count is printed.</p>'
            f'{pal}<p class="views">Other views: {view_links("dark")}</p></header><div class="plates">{plates}</div></div></section>')


def view_social():
    fig = s01('social', card=True)
    return ('<section class="view g g-white" data-view-root="social" data-title="Social card · Register chart system" aria-labelledby="social-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="social-h" tabindex="-1">Social card</h1>'
            '<p class="deck">Chart S01 as a portrait post at 1080 by 1350 pixels, the size Instagram and LinkedIn use. It is live type at '
            'true size, so the box below scrolls on a phone. The card keeps the frame: evidence label, title, measure line, the party '
            'register, the dated votes and the full source line.</p>'
            f'<p class="views">Other views: {view_links("social")}</p></header><div class="socialw">{fig}'
            '<aside class="cardnote" aria-label="About the card"><p class="eyebrow">Alt text for the exported image</p>'
            '<p>A card from Oath &amp; Action. Finding: Nearly nine in ten Republicans and Democrats favored a ban on stock trading by '
            'members of Congress. Bars show 88 percent of Democrats, 87 percent of Republicans and 86 percent of all registered voters, '
            'from a survey fielded May 19 to 30, 2023. The House passed a ban, H.R. 7008, 232 to 198 on July 22, 2026; on September 30 '
            'the Senate voted 53 to 47 to take it up, short of the 60 votes, three-fifths of the Senate, needed to end debate. From Who '
            'Do They Answer To?, the Oath &amp; Action systems atlas.</p>'
            '<p class="eyebrow">Rules for cards</p><ul class="bul"><li>Type keeps its system roles at card size: label 26 px, title 60 px, '
            'figures 68 px, party names 32 px, votes 28 px, source 20 px.</li><li>The source line prints whole on the card itself.</li>'
            '<li>Party rows share one ink and print the party name.</li><li>The card names Oath &amp; Action and the atlas; it carries '
            'no web address until the site is settled.</li><li>The wordmark sits at the foot; it is the only red on the card.</li></ul></aside>'
            '</div></div></section>')


# ------------------------------------------------------------------------------------------------ system sheet
def swatch_rows(gname, entries):
    t = G[gname]
    out = []
    for name, job, h in entries:
        cr = contrast(h, t['bg'])
        red = ' data-red="specimen"' if h.upper() == LOCK['red'] else ''
        out.append(f'<tr><th scope="row"><span class="sw2"{red} style="background:{h}" aria-hidden="true"></span>{e(name)}</th>'
                   f'<td data-label="Job">{e(job)}</td><td data-label="Hex">{h}</td><td class="n" data-label="Contrast">{cr:.2f}</td>'
                   f'<td class="n" data-label="OKLab L">{oklab(h)[0]:.3f}</td>'
                   f'<td data-label="Grayscale"><span class="sw2" style="background:{gray(h)}" aria-hidden="true"></span>{gray(h)}</td></tr>')
    return ''.join(out)


def palette_table(gname, label):
    t = G[gname]
    dark = gname == 'dark'
    common = [('Newsprint' if dark else 'Charcoal', 'Ink: titles, labels, the named series, baselines; away-from-voters dots', t['ink']),
              ('Dim Newsprint' if dark else 'Deep Stone', 'Secondary text: measure lines, notes, sources', t['sec']),
              ('Stone toward Newsprint' if dark else 'Stone', 'Context series and hollow marks', t['ctx']),
              ('Gridline', 'Horizontal hairlines', t['grid']), ('Quiet rule', 'Table rows (Register tint)', t['rq']),
              ('Verdigris lifted 4%' if dark else 'Verdigris', 'Toward-voters squares; up', t['tow']),
              ('Map tint', 'Bans ranked-choice voting in some elections (Register tint)', t['some']),
              ('Documented', 'Grade ramp, step 1', t['g1']), ('Well supported', 'Grade ramp, step 2', t['g2']),
              ('Plausible', 'Grade ramp, step 3', t['g3']), ('Contested', 'Grade ramp, step 4, with hatch', t['g4']),
              ('Pillar Red', 'The one point a title names, when a chart uses red', LOCK['red'])]
    if not dark:
        common[-1:-1] = [('Up, strong', 'Diverging B, step 5', t['dv1']), ('Up, light', 'Diverging B, step 4', t['dv2']),
                         ('Midpoint', 'Diverging B, step 3', t['dv3']), ('Down, light', 'Diverging B, step 2', t['dv4']),
                         ('Down, strong (Prussian)', 'Diverging B, step 1', t['dv5'])]
    return (f'<div class="tw"><table class="reg rf pal"><caption>{e(label)}, ground {t["bg"]}</caption><thead><tr><th scope="col">Ink</th>'
            '<th scope="col">Job</th><th scope="col">Hex</th><th scope="col" class="n">Contrast</th><th scope="col" class="n">OKLab L</th>'
            f'<th scope="col">Grayscale</th></tr></thead><tbody>{swatch_rows(gname, common)}</tbody></table></div>')


RULE_053 = ('"The wordmark\'s ampersand and the lockmark\'s lever are signature red and do not count, and neither do the ampersands '
            'inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with '
            'the wordmark and never stands in for the hinge divider. An icon\'s red accent counts as signature red when the icon stands '
            'alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one '
            'keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: '
            'an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is '
            'where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline\'s ampersand uses '
            'the view\'s working red. The hinge divider\'s ampersand takes its surface\'s ink: Charcoal on Newsprint and White, Newsprint '
            'on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. '
            'Red never sits on Prussian."')


def anatomy():
    arts = ', '.join(str(w) for w in T['artboards'][:-1]) + f' and {T["artboards"][-1]}'
    parts = [('Rule', '2 px Charcoal across the figure. It opens every figure and nothing else on the page uses it.'),
             ('Evidence label', 'Inter 700, 13/18, capitals, 0.06em. The kind (Finding, Association, Estimate, Illustration), then a few '
                                'words on where the numbers come from.'),
             ('Title', f'Inter Tight 800, {T["title"][0]}/{T["title"][1]} ({T["title_phone"][0]}/{T["title_phone"][1]} on phones). A '
                       'sentence that states the finding, with a verb that matches the grade.'),
             ('Measure line', 'Inter 400, 15/23, Deep Stone, at most 75 characters a line. Measure, unit, place and period; a '
                              'cropped scale is said here.'),
             ('Figure', f'The chart or the register. Artboards at {arts} px, each shown at its own size, so nothing scales.'),
             ('Note in the drawing', 'Inter 400 or 600, 13/16, with a ground-colored halo, joined to its data by a 1 px leader that '
                                     'crosses no series.'),
             ('Notes', 'Inter 400, 14/20, Deep Stone, numbered, 45 to 75 characters a line. What a reader needs to read the figure '
                       'fairly; then the coding rule and the disclosure where the data needs them.'),
             ('Source line', 'Inter 400, 13/18, Deep Stone. Publisher, table, period, place, date retrieved, qualification. The credit '
                             '"Chart: Oath & Action" and the link to the reading guide sit beside it.'),
             ('Table', '"Show the S0n table": every value, every note and the source, readable by a screen reader.'),
             ('Studio note', 'Dashed box beside the figure, used in the guide only.')]
    return ('<ol class="anat">' + ''.join(f'<li><b>{e(n)}</b><span>{e(d)}</span></li>' for n, d in parts) + '</ol>')


def type_ramp():
    ramp = [('Display', 'Inter Tight 800', '56/60', MINUS + '0.035em', 'Register', 'display'),
            ('Figure title', 'Inter Tight 800', f'{T["title"][0]}/{T["title"][1]}', MINUS + '0.02em', 'A sentence that states the finding.', 'r-title'),
            ('Big figure', 'Inter Tight 800', '128/112', MINUS + '0.04em', '86%', 'r-big'),
            ('Register figure', 'Inter Tight 800', '22/26', MINUS + '0.01em', '24 · 17 · 9.6', 'r-fig'),
            ('Evidence label', 'Inter 700, capitals', '13/18', '0.06em', 'Finding · official statistic', 'r-lab'),
            ('Measure line', 'Inter 400, Deep Stone', '15/23', '0', 'Share of registered voters, United States, 2023', 'r-meas'),
            ('Table cell', 'Inter 400, tabular figures', '15/22', '0', '1,080 · 95.8 · ' + MINUS + '3.7', 'r-cell'),
            ('Column head', 'Inter 600, Deep Stone', '13/18', '0', 'Documented, %', 'r-head'),
            ('Chart label', 'Inter 600, tabular figures', '13/16', '0', '2021: 5.1%', 'r-clab'),
            ('Note', 'Inter 400, Deep Stone', '14/20', '0', 'The table gives each margin of error.', 'r-note'),
            ('Source', 'Inter 400, Deep Stone', '13/18', '0', 'Source: U.S. Census Bureau', 'r-src')]
    rws = ''.join(f'<tr><th scope="row">{e(a)}</th><td data-label="Face">{e(b)}</td><td data-label="Size">{c}</td>'
                  f'<td data-label="Tracking">{d}</td><td data-label="Sample"><span class="{k}">{e(s)}</span></td></tr>' for a, b, c, d, s, k in ramp)
    return ('<div class="tw"><table class="reg rf ramp"><caption>Type ramp, desktop sizes in px</caption><thead><tr><th scope="col">Role</th>'
            '<th scope="col">Face</th><th scope="col">Size/line</th><th scope="col">Tracking</th><th scope="col">Sample</th></tr></thead>'
            f'<tbody>{rws}</tbody></table></div>')


def marks_sheet(W, view='system'):
    """Every mark of the system at true size, drawn from CHART_TOKENS, with its specification."""
    L, R = T['line'], T['radius']

    def b_lines(x, y0):
        out = []
        for i, (n, w, cls) in enumerate([('Gridline', L['hair'], 'grid'), ('Baseline at zero', L['hair'], 'base'),
                                         ('Leader', L['hair'], 'lead'), ('Context series', L['context'], 'ln-ctx'),
                                         ('Series, small multiples', L['series'], 'ln-sm'), ('Named series', L['series'], 'ln-main')]):
            y = y0 + 14 + i * 30 + 0.5
            out.append(f'<line class="{cls}" x1="{f(x)}" x2="{f(x + 96)}" y1="{f(y)}" y2="{f(y)}"/>')
            out.append(txt(x + 108, y + 5, e(f'{n}, {w} px'), 'nt'))
        return out, 180

    def b_dots(x, y0):
        out = []
        for i, (n, r, cls) in enumerate([(f'Year point, r {R["point"]}', R['point'], 'pt-main'),
                                         (f'Named point, r {R["point_named"]}', R['point_named'], 'pt-main'),
                                         (f'Dumbbell, later year, r {R["dumbbell"]}', R['dumbbell'], 'd24'),
                                         (f'Dumbbell, earlier year, r {R["dumbbell"]}', R['dumbbell'], 'd20'),
                                         (f'Timeline event, r {R["event"]}', R['event'], 'ev-pt')]):
            y = y0 + 14 + i * 30
            out.append(f'<circle class="{cls}" cx="{f(x + 8)}" cy="{f(y)}" r="{r}"/>')
            out.append(txt(x + 26, y + 5, e(n), 'nt'))
        return out, 150

    def b_other(x, y0):
        u, bh = T['unit'], T['bar_h']
        out = [f'<rect class="u-tow" x="{f(x + .5)}" y="{f(y0 + 7.5)}" width="{u - 1}" height="{u - 1}"/>',
               f'<circle class="u-awy" cx="{f(x + u + T["unit_gap"] + u / 2)}" cy="{f(y0 + 7 + u / 2)}" r="{u / 2 - .5}"/>',
               txt(x + 40, y0 + 19, f'Units {u} px, gap {T["unit_gap"]}', 'nt')]
        for j in range(5):
            out.append(f'<circle class="u-awy" cx="{f(x + 6 + j * 12.8)}" cy="{f(y0 + 45)}" r="5"/>')
        for j in range(3):
            out.append(f'<rect class="u-tow" x="{f(x + 64 + j * 12.8)}" y="{f(y0 + 39)}" width="10.8" height="{bh}"/>')
        out.append(lines(x + 112, y0 + 44, [f'In-row bar, {bh} px,', 'one glyph per change'], 'nt', 16))
        out += [f'<rect class="tile-s" x="{f(x)}" y="{f(y0 + 76)}" width="{T["tile"]}" height="{T["tile"]}"/>',
                txt(x + 52, y0 + 94, f'Map tile {T["tile"]} px,', 'nt'), txt(x + 52, y0 + 110, f'gap {T["tile_gap"]}', 'nt')]
        return out, 120

    cols = 3 if W > 700 else (2 if W > 500 else 1)
    cw = W / cols
    p, y0, row_h = [], 0, 0
    for i, blk in enumerate([b_lines, b_dots, b_other]):
        c = i % cols
        if i and c == 0:
            y0 += row_h + 16
            row_h = 0
        out, h = blk(c * cw, y0)
        p += out
        row_h = max(row_h, h)
    H = y0 + row_h + 4
    return svg(W, H, f'{view}-marks-{W}', f'Mark specimens drawn from the chart tokens: line weights {L["hair"]}, {L["context"]} and '
               f'{L["series"]} px; points of radius {R["point"]} to {R["dumbbell"]}; units of {T["unit"]} px; in-row bars of '
               f'{T["bar_h"]} px; map tiles of {T["tile"]} px.', ''.join(p))


def red_demo():
    d4 = s04_numbers()
    y = d4[0][3]['voted_pct']
    assert y == min(b['voted_pct'] for k, _, _, b, _ in d4)
    t4 = f'Citizens 18 to 24 reported voting at {y:.1f} percent in 2024, the lowest of any age group.'
    a = ('<div class="rdemo"><p class="rdh">A chart posted alone: the point its title names takes the red</p>'
         f'<p class="rdt">{e(t4)}</p><div class="rdc">{s04_svg(328, "sysa", "specimen")}</div>'
         '<p class="rdn">Pillar Red on the 2024 dot for 18 to 24, 4.17:1 on White. On Newsprint it takes a 1 px Charcoal keyline.</p></div>')
    b = ('<div class="rdemo"><p class="rdh">The same chart on a page with an ask: the point steps down to Charcoal</p>'
         f'<p class="rdt">{e(t4)}</p><div class="rdc">{s04_svg(328, "sysb")}</div>'
         '<p class="rdask"><a class="ask" data-red="specimen" href="#system-red">Check your voter registration</a> '
         '<span class="ill">Illustrative ask</span></p>'
         '<p class="rdn">The step a reader can take now outranks the title\'s point, so the button keeps the red and the dot turns '
         'Charcoal at the same size.</p></div>')
    return f'<div class="rdemos">{a}{b}</div>'


def view_system():
    t = G['white']
    dpair = (f'{delta_e(t["tow"], t["awy"]):.3f} ({delta_e(t["tow"], t["awy"], "deuteranopia"):.3f} under deuteranopia, '
             f'{delta_e(t["tow"], t["awy"], "protanopia"):.3f} under protanopia, {delta_e(t["tow"], t["awy"], "tritanopia"):.3f} under tritanopia)')
    anat_fig = s03('system')
    src_parts = [('Publisher', 'U.S. Census Bureau'), ('Title or table', 'Poverty in the United States: 2025 (P60-290), Table 8'),
                 ('Observation period', '2009 to 2025'), ('Geography', 'United States'), ('Date retrieved', 'Retrieved November 6, 2026'),
                 ('Qualification', 'Figures for 2019 to 2024 include the Bureau\'s August 2026 revision')]
    srcl = ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in src_parts)
    read = [('Start with the label.', 'It names the kind of evidence. A Finding is a measured result with a source and a period. An '
                                      'Association is a pattern that does not show cause. An Estimate is a modeled value that holds only '
                                      'if its stated assumptions do. An Illustration uses made-up numbers to show how a chart works, and '
                                      'says "Illustrative data" beside it.'),
            ('Read the words after the label.', 'They say where the numbers come from. "Official statistic" is a figure a government '
                                                 'agency publishes; "self-reported" is what survey respondents said; "documented" means '
                                                 'on the public record; "a secondary list" was compiled by someone other than the '
                                                 'original source.'),
            ('Read the title as the claim.', 'Its verb says how sure the evidence is: words such as "passed", "fell" or "ban" for '
                                             'documented facts; a plain statement for well-supported findings; "can" or "may" for '
                                             'plausible ones; "would" for estimates that hold only if their assumptions do; '
                                             '"untested" for a hypothesis; and both readings where the evidence is contested.'),
            ('Check the measure line.', 'It says what was counted, where and when, and whether the scale starts above zero.'),
            ('Find the darkest ink.', 'It marks the series or the point the title names; gray gives context. A chart with its own code, '
                                      'such as the evidence grades, says so in its key.'),
            ('Know what red means.', 'When a chart uses red, it marks the single point the title names. Red never means a party, good '
                                     'or bad.'),
            ('Allow for survey error.', 'Survey numbers come from a sample of people, so each has a margin of error. A margin of 0.5 '
                                        'points means the true figure most likely sits within half a point either way, and a smaller '
                                        'change may be chance.'),
            ('Know what "the atlas" is.', 'Who Do They Answer To? is Oath & Action\'s own research record of the rules. Charts drawn from '
                                          'it say so, and the directions they show are its codes, printed under the chart.'),
            ('Look up the numbers.', 'The register under each chart prints the figures, and "Show the table" holds every value, note '
                                     'and source.')]
    readl = ''.join(f'<li><b>{e(a)}</b> {e(b)}</li>' for a, b in read)
    return ('<section class="view g g-white" data-view-root="system" data-title="System · Register chart system" aria-labelledby="sys-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="sys-h" tabindex="-1">The system on one sheet</h1>'
            '<p class="deck">The rules a designer or a builder needs to make the next chart: the frame and its parts, the type, the marks, '
            'the palettes with measured contrast, the table rules, notes and sources, red, and the guide for readers.</p>'
            f'<p class="views">Other views: {view_links("system")}</p></header>'
            '<section class="sys" aria-labelledby="sys-1"><h2 class="sh" id="sys-1"><span>1</span>The frame</h2>'
            '<div class="sys2"><div class="anatfig">' + plate('system', 'S03', anat_fig, WHY['S03']) + '</div>'
            f'<div><p class="sp">Every figure uses the same ten parts in the same order, so a reader learns them once.</p>{anatomy()}'
            '<p class="sp">Grid: 12 columns at 1440 px with 64 px margins and 24 px gutters; the figure takes 866 px and the studio note '
            'the rest. On phones, 16 px margins, one column, the figure first.</p>'
            '<p class="sp">The kit: every chart comes from a generator that takes rows, and the frame, the register generator and '
            'the chart tokens are shared. A drawing that puts a line through a word, or a label outside its box, stops the build.</p></div></div></section>'
            '<section class="sys" aria-labelledby="sys-2"><h2 class="sh" id="sys-2"><span>2</span>Type</h2>'
            f'<p class="sp">Locked faces only: Inter Tight for titles and big figures, Inter for everything else, Lora Italic for quoted '
            f'words only. Every number is tabular, every minus is the true minus ({MINUS}), quotes and apostrophes are curly, dates print '
            f'in words, and nothing falls under 13 px.</p>{type_ramp()}</section>'
            '<section class="sys" aria-labelledby="sys-3"><h2 class="sh" id="sys-3"><span>3</span>Marks</h2>'
            f'<div class="cq">{artboards(marks_sheet, "system")}</div><ul class="bul cols2">'
            '<li>Bars start at zero; in-row bars share one scale per table, and every bar\'s value is printed.</li>'
            '<li>Lines may start above zero only when the measure line says so. Missing years and method changes break the line.</li>'
            '<li>Points sit on one straight scale per panel. Small multiples share one scale.</li>'
            f'<li>One mark per record: squares toward voters, dots away from voters, hollow squares for no change, hatched for mixed, '
            f'dashed for pending. Units are {T["unit"]} px; in a register bar each glyph is one change.</li>'
            '<li>Gridlines are horizontal hairlines on the half pixel, with no ticks; the baseline at zero is Charcoal.</li>'
            '<li>Every label in a drawing carries a ground-colored halo, so a gridline never runs through a word.</li>'
            '<li>Charts do not move. A later animated chart starts with a reduced-motion path that shows its final state.</li></ul></section>'
            '<section class="sys" aria-labelledby="sys-4"><h2 class="sh" id="sys-4"><span>4</span>Palettes, measured</h2>'
            '<p class="sp">Lab values come from the shared palette lab; Register\'s own tints (the quiet rule, the map tint and the '
            'Verdigris lift on Charcoal) are mixed in OKLab from locked colors, each with one job. Contrast is WCAG 2 against the ground. '
            'Marks that carry meaning clear 3:1. Light fills inside a scale (the plausible and contested grades, the map tint, the light '
            'diverging steps) sit under 3:1 only where every value prints in the register or the table, a design judgment. In a '
            'contrast theme a tint never carries meaning that its glyph or its printed value does not also carry.</p>'
            f'<p class="sp">The direction pair, Verdigris squares and Charcoal dots on White, differs by OKLab distance {dpair}, and by '
            'shape. Neither is Prussian or red. Stone and Verdigris never separate two categories alone.</p>'
            f'{palette_table("white", "On White")}{palette_table("newsprint", "On Newsprint")}{palette_table("dark", "On Charcoal")}'
            '<p class="sp">Diverging scales never pair red with blue. Register tests candidate B, Prussian through the ground to Verdigris, in '
            'S06; candidate A, Stone through a neutral to Verdigris, stays with the other concepts for Gate 2. No state map and no '
            'direction code uses Prussian, so a blue mark never reads as a party.</p></section>'
            '<section class="sys" aria-labelledby="sys-5"><h2 class="sh" id="sys-5"><span>5</span>Tables</h2><ul class="bul cols2">'
            '<li>Numbers sit right-aligned in tabular figures, with one count of decimals per column, so the decimal points align.</li>'
            f'<li>A change column prints its sign: +0.2, {MINUS}3.7. Zero prints as 0 in Deep Stone; a missing value prints as words.</li>'
            '<li>Column heads carry the unit, once: "Documented, %". Rows carry no unit.</li>'
            '<li>Rules stay quiet: Charcoal under the head, a quiet tint between rows, Stone above a group, Charcoal above the total.</li>'
            '<li>The default sort answers the question: ranked by value, grouped by who acted, or by date. Long tables let a reader re-sort.</li>'
            f'<li>A bar inside the row, {T["bar_h"]} px high, shows the shape; the printed figure carries the value. Bars stay visible '
            'in Windows contrast themes.</li>'
            '<li>On a phone each row reflows into labeled lines, so no table scrolls sideways.</li>'
            '<li>Group and total rows carry their own counts in bold, and they sum.</li></ul></section>'
            '<section class="sys" aria-labelledby="sys-6"><h2 class="sh" id="sys-6"><span>6</span>Notes, sources and fairness</h2><div class="sys2"><div>'
            '<ul class="bul"><li>A note inside the drawing does one job: names the record, explains an odd encoding, or gives a reader\'s scale.</li>'
            '<li>Join a note to its data with a 1 px leader or a bracket. Never hide a note behind hover.</li>'
            '<li>Notes under the figure say what the reader needs to read it fairly: revisions, breaks, coding rules, margins of error, '
            'and the editor\'s disclosure on charts about the rules his campaigns concern.</li>'
            '<li>Notes, measure lines and sources run 45 to 75 characters a line. Reader-facing words name no colors and no source codes.</li>'
            '<li>Before a title ships, read it once as a reader on the left and once as a reader on the right.</li>'
            '<li>Label illustrative items beside the item. Titles say what the evidence supports and nothing more.</li></ul></div>'
            f'<div><p class="sp">The source line keeps section 15 order. Shorten it only by dropping words; every fact stays.</p><ol class="srcl">{srcl}</ol></div></div></section>'
            '<section class="sys" id="system-red" aria-labelledby="sys-7"><h2 class="sh" id="sys-7"><span>7</span>Red</h2>'
            f'<blockquote class="rule">{e(RULE_053)}<footer>Rule 05.3 (D2-01)</footer></blockquote>'
            '<p class="sp">On a chart page red never encodes a series, a category, a grade or a scale. It may mark the one point a title names, '
            'and only when no error or ask holds the view\'s red. A chart posted alone may mark the point its title names in red; a chart '
            'added to a page takes red only when the page\'s red job moves to it. The chart views of this page carry no working red. The '
            'two drawings below are guide specimens, so their red does not count.</p>'
            f'{red_demo()}</section>'
            '<section class="sys" id="system-read" aria-labelledby="sys-8"><h2 class="sh" id="sys-8" tabindex="-1"><span>8</span>How to read our charts</h2>'
            f'<p class="sp">For readers, printed once in a report and linked from every chart.</p><ol class="readl">{readl}</ol></section>'
            '</div></section>')


# ------------------------------------------------------------------------------------------------ page
def wordmark(height, master, cls):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    return src.replace('<svg ', f'<svg class="{cls}" data-view="wordmark" width="{w:.0f}" height="{height}" role="img" '
                                f'aria-label="Oath &amp; Action" ', 1)


def wordmark_card():
    return f'<span class="cwm" data-red="signature">{wordmark(40, "20261028_Wordmark-Display-Master.svg", "wmc")}</span>'


def masthead():
    tabs = ''.join(f'<li><a href="#{v}">{t}</a></li>' for v, t in VIEWS)
    return ('<header class="mast"><div class="wrap mrow">'
            '<a class="wm" href="#white" data-red="signature" aria-label="Oath &amp; Action, Register, first view">'
            f'{wordmark(24, "20261028_Wordmark-24px-Master.svg", "wm24")}{wordmark(16, "20261028_Wordmark-16px-Master.svg", "wm16")}</a>'
            '<p class="run">Chart system concept 02 · Register</p>'
            f'<nav class="tabs" aria-label="Views"><ul>{tabs}</ul></nav></div></header>')


def footer():
    return ('<footer class="foot"><div class="wrap frow"><p>Data: Oath &amp; Action, Who Do They Answer To? Systems Atlas V7, snapshot of '
            '2026-10-15; U.S. Census Bureau tables retrieved November 6, 2026; Ballotpedia, retrieved November 6, 2026. Every source line '
            'sits under its chart.</p><p>Chart system concept 02, Register. Studio draft for Dustin Cathcart; titles and notes are '
            'studio drafts.</p></div></footer>')


CSS = r"""
:root{--white:#FFFFFF;--newsprint:#DCD9D2;--charcoal:#121212;--pillar:#E63946;--prussian:#1F2D5A;--stone:#5D636D;--verdigris:#4A7C74;--deep:#4E535B}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#FFFFFF;color:#121212;font:400 17px/27px Inter,system-ui,sans-serif}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--ink,#121212);outline-offset:3px}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.g{background:var(--bg);color:var(--ink)}
.view[hidden]{display:none}
.skip{position:absolute;left:16px;top:-200px;z-index:50;padding:10px 14px;background:#FFFFFF;border:2px solid #121212;font:600 15px/1 Inter,sans-serif;color:#121212}
.skip:focus{top:12px}
/* masthead: one White chrome for every view */
.mast{background:#FFFFFF;border-bottom:1px solid #5D636D;color:#121212}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;align-items:center;padding:14px 0;color:#121212}
.wm16{display:none}
.run{margin:0 0 0 40px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#4E535B}
.tabs ul{display:flex;gap:14px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:0 4px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:#121212}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 #121212}
.tabs a:hover{text-decoration:underline}
/* view heads and the lead block */
.vhead{padding:48px 0 32px;max-width:980px}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.display{width:fit-content;margin:0 0 0 -.04em;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em}
.display:focus-visible{outline-offset:6px}
.deck{margin:16px 0 0;font:400 19px/29px Inter,sans-serif;max-width:37em;text-wrap:pretty}
.views{margin:10px 0 0;font:600 15px/23px Inter,sans-serif}
.views a{display:inline-flex;align-items:center;min-height:44px}
.lead{margin:0 0 72px;border-top:1px solid var(--ink)}
.lead-d{border-bottom:1px solid var(--rq)}
.lead-d>summary,.feq>summary{display:flex;align-items:center;gap:10px;min-height:44px;cursor:pointer;list-style:none}
.lead-d>summary{min-height:48px;font:700 15px/20px Inter,sans-serif}
.lead-d>summary::-webkit-details-marker,.feq>summary::-webkit-details-marker{display:none}
.lead-d>summary::before,.feq>summary::before{content:"+" / "";display:inline-block;width:14px;flex:none;font:700 19px/1 Inter,sans-serif}
.lead-d[open]>summary::before,.feq[open]>summary::before{content:"\2212" / ""}
.howto-l{margin:0 0 4px;padding:0 0 0 22px;columns:2;column-gap:48px;max-width:1000px;font:400 15px/23px Inter,sans-serif}
.howto-l li{break-inside:avoid;margin:0 0 8px;text-wrap:pretty}
.howto-l b{font-weight:600}
.howto-m{margin:0 0 12px;font:400 15px/23px Inter,sans-serif;color:var(--sec)}
.howto-m a{color:var(--ink);font-weight:600}
.idx .tw{padding:0 0 16px}
.reg.contents tbody th,.reg.contents tbody td{vertical-align:middle;padding-top:0;padding-bottom:0}
.contents a.cl{display:inline-flex;align-items:center;min-height:44px;min-width:44px;font:800 17px/1 "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
/* plates and the frame */
.plates{padding-bottom:40px}
.plate{display:grid;grid-template-columns:$AB0px minmax(0,1fr);column-gap:56px;align-items:start;padding:0 0 104px;scroll-margin-top:24px}
.fig{margin:0;min-width:0;border-top:2px solid var(--ink);padding-top:12px;container-type:inline-size}
.elab{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.elab .gr{font-weight:400;letter-spacing:0;text-transform:none;color:var(--sec)}
.ftitle{margin:8px 0 0;font:800 $T0px/$T1px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em;max-width:30em;text-wrap:balance}
.ftitle:focus-visible{outline-offset:6px}
.fmeasure{margin:8px 0 0;font:400 15px/23px Inter,sans-serif;color:var(--sec);max-width:$MEASpx;text-wrap:pretty}
.fsub{margin:6px 0 0;font:600 15px/23px Inter,sans-serif;max-width:$MEASpx;text-wrap:pretty}
.fbody{margin-top:24px}
.fnotes{margin:24px 0 0;padding:0;list-style:none;counter-reset:n;font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:$NOTEpx}
.fnotes li{counter-increment:n;position:relative;padding-left:22px;margin:0 0 8px;text-wrap:pretty;break-inside:avoid}
.fnotes li::before{content:counter(n);position:absolute;left:0;top:0;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
@container (min-width:760px){.fnotes{columns:2;column-gap:40px;max-width:none}}
.fcode{margin:16px 0 0;max-width:$NOTEpx;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.fcode p{margin:0 0 8px;text-wrap:pretty}
.fcode .fch{margin:0 0 4px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.fcode .fneu{color:var(--ink)}
.fdisc{margin:12px 0 0;max-width:$NOTEpx;font:400 14px/20px Inter,sans-serif;color:var(--ink);text-wrap:pretty}
.fdisc b{font-weight:700}
.fsrcrow{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:4px 32px;margin-top:16px;padding-top:10px;border-top:1px solid var(--rq)}
.fsrc{margin:0;flex:1 1 320px;max-width:$SRCpx;font:400 13px/18px Inter,sans-serif;color:var(--sec);text-wrap:pretty}
.fcred{margin:0;flex:none;font:400 13px/18px Inter,sans-serif;color:var(--sec);text-align:right}
.fcred a{display:inline-flex;align-items:center;min-height:44px;font-weight:600;color:var(--ink)}
.feq{margin-top:4px;border-top:1px solid var(--rq)}
.feq>summary{font:600 15px/20px Inter,sans-serif}
.feq[open] .s-show,.feq:not([open]) .s-hide{display:none}
.eqb{padding:4px 0 8px}
.eqb .tw+.tw{margin-top:24px}
.eqn{margin-top:16px;font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:$NOTEpx}
.eqn ul{margin:4px 0 12px;padding-left:18px}.eqn p{margin:0}
.eqn .eqh{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);margin:0 0 4px}
.vs{display:block;font-weight:400;font-size:13px;color:var(--sec)}
/* studio strip: visibly apart from the chart */
.strip{border:1px dashed var(--sec);padding:14px 16px 6px;font:400 14px/20px Inter,sans-serif;color:var(--sec);margin-top:2px;max-width:380px}
.strip p{margin:0 0 10px}
.st-k{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.st-id{font:800 22px/26px "Inter Tight",sans-serif;color:var(--ink);font-variant-numeric:tabular-nums}
.st-id span{display:block;font:600 14px/20px Inter,sans-serif;color:var(--sec)}
.st-q span,.st-w span{display:block;font-weight:600;color:var(--ink)}
/* artboards: each drawn at the width it shows, at natural size; a drawing never scales up */
.abs{display:block}
.abs>.ab{display:none;width:var(--abw);height:auto;max-width:none}
.abs>.ab:nth-child(1){display:block}
@container (max-width:$AB0Qpx){.abs>.ab:nth-child(1){display:none}.abs>.ab:nth-child(2){display:block}}
@container (max-width:$AB1Qpx){.abs>.ab:nth-child(2){display:none}.abs>.ab:nth-child(3){display:block}}
@container (max-width:$AB2Qpx){.abs>.ab:nth-child(3){display:none}.abs>.ab:nth-child(4){display:block;max-width:100%}}
.fnotes li:has(.u-only){display:none}
$UNDER
.cq{container-type:inline-size;margin-bottom:20px}
/* svg type: a ground-colored halo on every label; tabular figures set after the font shorthand */
svg text{font-family:Inter,sans-serif;fill:var(--ink);paint-order:stroke;stroke:var(--bg);stroke-width:3px;stroke-linejoin:round}
svg .tile text{stroke:none}
svg .tk{font:400 13px Inter,sans-serif;fill:var(--sec)}
svg .th{font:600 13px Inter,sans-serif;fill:var(--sec)}
svg .lab{font:600 15px Inter,sans-serif}
svg .lab-s{font:600 13px Inter,sans-serif}
svg .lab-ctx{font:600 15px Inter,sans-serif;fill:var(--sec)}
svg .lab-b{font:700 15px Inter,sans-serif}
svg .nt{font:400 13px Inter,sans-serif;fill:var(--sec)}
svg .nt-b{font:600 13px Inter,sans-serif}
svg .num{font:400 15px Inter,sans-serif}
svg .num-b{font:700 15px Inter,sans-serif}
svg .b{font-weight:700;fill:var(--ink)}
svg .yr{font:700 13px Inter,sans-serif}
svg .ev{font:400 13px Inter,sans-serif}
svg .tc{font:600 13px Inter,sans-serif}
svg .ty{font:400 13px Inter,sans-serif}
svg .d,svg .tk,svg .yr,svg .ty,svg .num,svg .num-b{font-variant-numeric:tabular-nums}
svg line,svg path,svg circle,svg rect{vector-effect:non-scaling-stroke}
.rq{stroke:var(--rq);stroke-width:1}
.grid{stroke:var(--grid);stroke-width:1}
.base{stroke:var(--ink);stroke-width:1}
.lead{stroke:var(--ctx);stroke-width:1;fill:none}
.brk{stroke:var(--ink);stroke-width:1;fill:none}
.comb{stroke:var(--ctx);stroke-width:1;fill:none}
.lane{stroke:var(--ctx);stroke-width:1}
.ln-main{stroke:var(--ink);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round}
.ln-sm{stroke:var(--ink);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round}
.ln-ctx{stroke:var(--ctx);stroke-width:1.5;fill:none;stroke-linejoin:round}
.pt-main{fill:var(--ink);stroke:var(--bg);stroke-width:1}
.pt-sm{fill:var(--ink)}
.vx-ctx{fill:var(--ctx)}
.pt-red{fill:var(--red);stroke:var(--bg);stroke-width:1.5}
.g-news .pt-red{stroke:var(--ink);stroke-width:1}
.ev-pt{fill:var(--ink);stroke:var(--bg);stroke-width:1.5}
.ev-pt.sm{stroke-width:1}
.db{stroke:var(--ctx);stroke-width:2}.db-ctx{stroke:var(--grid);stroke-width:2}
.d20h{fill:none;stroke:var(--bg);stroke-width:6}
.d20{fill:none;stroke:var(--ink);stroke-width:2}
.d24{fill:var(--ink)}
.d20.c{stroke:var(--ctx)}.d24.c{fill:var(--ctx)}
.u-tow{fill:var(--tow)}.u-awy{fill:var(--awy)}
.u-roll{fill:var(--bg);stroke:var(--awy);stroke-width:1.5}
.u-kept{fill:var(--bg);stroke:var(--ctx);stroke-width:1.5}
.u-mix{fill:var(--bg);stroke:var(--ctx);stroke-width:1.5}
.u-hatch{stroke:var(--ctx);stroke-width:1;fill:none}
.u-pend{fill:var(--bg);stroke:var(--ink);stroke-width:1.5;stroke-dasharray:3 2}
.bar-s{fill:var(--ink)}
.tile-s{fill:var(--ink)}
/* tables: the register */
.tw{max-width:100%}
.reg{width:100%;border-collapse:collapse;font:400 15px/22px Inter,sans-serif;color:var(--ink)}
.reg caption{text-align:left;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:0 0 10px}
.reg thead th{font:600 13px/18px Inter,sans-serif;color:var(--sec);text-align:left;vertical-align:bottom;padding:0 14px 8px 0;border-bottom:1px solid var(--ink)}
.reg tbody th,.reg tbody td,.reg tfoot th,.reg tfoot td{padding:9px 14px 9px 0;border-bottom:1px solid var(--rq);text-align:left;vertical-align:top}
.reg .n,.reg thead .n,.reg tbody .n,.reg tfoot .n{text-align:right}
.reg tbody th{font-weight:600}
.reg tr>*:last-child{padding-right:0}
.reg tfoot th,.reg tfoot td{border-top:1px solid var(--ink);border-bottom:0;font-weight:700}
.reg .z{color:var(--sec)}
.reg .n,.reg .tn,.reg [data-value],.reg .gt{font-variant-numeric:tabular-nums lining-nums}
.reg .sb{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:flex-end;gap:4px;min-height:44px;min-width:44px;padding-bottom:1px;font:inherit;color:inherit}
.reg th.n .sb{justify-content:flex-end}
.reg .sb:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.reg th[aria-sort] .sb{color:var(--ink)}
.reg th[aria-sort="ascending"] .sb::after{content:"\2191" / ""}
.reg th[aria-sort="descending"] .sb::after{content:"\2193" / ""}
/* the ranked register: group rows, one total row, a bar inside each row */
.reg-r td.c-bar{width:280px}
.reg-r tr.grp th,.reg-r tr.grp td{padding-top:22px;vertical-align:bottom;border-bottom:1px solid var(--ctx)}
.reg-r tr.grp th{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.reg-r tr.grp td{font:700 15px/22px Inter,sans-serif;font-variant-numeric:tabular-nums lining-nums}
.reg-r tfoot td{font-variant-numeric:tabular-nums lining-nums}
.reg-track{display:flex;height:$BARHpx;margin-top:5px}
.seg{display:block;flex:none;height:100%;background-repeat:repeat-x;background-position:left center;background-size:calc(100% / var(--n,1)) 100%}
.rnote{display:block;margin-top:6px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.k-g1{background:var(--g1)}.k-g2{background:var(--g2)}.k-g3{background:var(--g3)}
.k-g4{background:repeating-linear-gradient(135deg,var(--g2) 0 1.5px,var(--g4) 1.5px 4.5px)}
.reg-share .seg{box-shadow:inset -1px 0 0 var(--bg)}
.sw{display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-1px;background-repeat:no-repeat;background-size:12px 12px}
.sw2{display:inline-block;width:18px;height:18px;margin-right:8px;vertical-align:-4px;box-shadow:inset 0 0 0 1px var(--ctx)}
/* S01 */
.s01{display:grid;grid-template-columns:330px minmax(0,1fr);gap:48px;align-items:end}
.bign{margin:0 0 0 -.04em;font:800 128px/112px "Inter Tight",sans-serif;letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.bigc{margin:12px 0 0;font:400 17px/25px Inter,sans-serif;max-width:19em}
.regh{margin:0 0 10px;font:600 13px/18px Inter,sans-serif;color:var(--sec);border-bottom:1px solid var(--ink);padding-bottom:8px}
.plist{margin:0;padding:0;list-style:none}
.prow{display:grid;grid-template-columns:120px minmax(0,1fr) 84px;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--rq)}
.pn{font:600 17px/24px Inter,sans-serif}
.ptrk{display:block;height:16px;background:var(--rq)}
.pbar{display:block;height:100%;background:var(--ink)}
.pv{font:800 28px/32px "Inter Tight",sans-serif;text-align:right;font-variant-numeric:tabular-nums}
.scale{display:flex;justify-content:space-between;margin:6px 98px 0 134px;font:400 13px/18px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.s01v{margin-top:32px}
.s01v tbody tr:last-child>*{border-bottom:0}
/* S05 register */
.s05r{margin-top:28px;max-width:860px}
/* S06 */
.gkey{margin:0 0 16px}
.gkh{margin:0 0 6px;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.gkey ul{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0;padding:0;list-style:none;font:400 14px/20px Inter,sans-serif}
.gkey li{display:inline-flex;align-items:center;gap:6px}
.gl{flex:none;display:block}
.c-up{fill:var(--dv1)}.c-sup{fill:var(--dv2)}.c-flat{fill:var(--dv3);stroke:var(--ctx);stroke-width:1}
.c-fod{fill:var(--dv4)}.c-down{fill:var(--dv5)}.c-mix{fill:var(--dv3);stroke:var(--ctx);stroke-width:1}
.c-same{fill:var(--bg);stroke:var(--ctx);stroke-width:1.5;stroke-dasharray:3 2}
.gl .ga{fill:var(--ink)}
.c-up+.ga,.c-down+.ga{fill:var(--bg)}
.s06 .cell{display:flex;gap:8px;align-items:flex-start}
.s06 .cell .gl{margin-top:1px}
.s06 td{width:19%}
.s06 .sk{display:block;font:800 15px/20px "Inter Tight",sans-serif}
.s06 .sn{display:block;font-weight:600}
.s06 .sg{display:block;margin-top:2px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
/* S07 */
.tkey{display:flex;flex-wrap:wrap;gap:6px 24px;margin:0 0 16px;padding:0;list-style:none;font:400 15px/22px Inter,sans-serif}
.tkey li{display:inline-flex;align-items:center;gap:8px}
.tkey b{font-variant-numeric:tabular-nums}
.tsw{display:inline-block;width:18px;height:18px}
.tsw-all{background:var(--ink)}.tsw-some{background:var(--some)}.tsw-none{background:var(--bg);box-shadow:inset 0 0 0 1px var(--ctx)}
.s07{display:grid;grid-template-columns:528px minmax(0,1fr);gap:40px;align-items:start}
.t-all rect{fill:var(--ink)}.t-all text{fill:var(--on)}
.t-some rect{fill:var(--some)}
.t-none rect{fill:var(--bg);stroke:var(--ctx);stroke-width:1}
@container (max-width:820px){.s07{grid-template-columns:minmax(0,1fr);gap:24px}}
/* S08 */
.uc{--u:$UNITpx;--ucw:204px}
.uc-band{display:grid;grid-template-columns:var(--ucw) minmax(0,1fr);column-gap:16px;padding:10px 0 0}
.uc-lab{align-self:end;padding-bottom:4px}
.ub-n{margin:0;font:600 15px/22px Inter,sans-serif;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ub-n b{font:800 22px/26px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
.ub-s{margin:6px 0 0;font:400 13px/18px Inter,sans-serif;color:var(--sec);display:grid;gap:3px;font-variant-numeric:tabular-nums}
.ub-b{margin:0;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.ukey{display:inline-flex;align-items:center;gap:6px}
.uk{width:14px;height:14px;flex:none;display:block}
.uc-cols{display:grid;grid-template-columns:var(--c0,40px) repeat(var(--nc),minmax(0,1fr));grid-template-rows:auto auto auto;column-gap:4px;align-items:end;border-bottom:1px solid var(--ink)}
.uc-col{grid-row:3;display:flex;flex-wrap:wrap-reverse;justify-content:center;align-content:flex-start;gap:$UGAPpx;padding-bottom:2px}
.uc-col:first-of-type{border-right:1px dashed var(--grid);padding-right:4px}
.u{display:block;width:var(--u);height:var(--u);flex:none}
.uc-nt{grid-row:1;margin:0 0 4px;font:400 13px/18px Inter,sans-serif;color:var(--sec);text-align:right;text-wrap:balance}
.uc-br{grid-row:2;height:7px;border:1px solid var(--ctx);border-bottom:0;margin:0 0 4px;align-self:end}
.uc-base{padding-top:0}
.uc-base .uc-lab{align-self:center;padding-bottom:0}
.uc-base .uc-cols{grid-template-rows:auto;border-bottom:1px solid var(--rq);align-items:center}
.ubase{grid-row:1;justify-self:center;padding:3px 0;font:600 13px/18px Inter,sans-serif;font-variant-numeric:tabular-nums}
.ubase.z{color:var(--sec);font-weight:400}
.ubase:first-child{justify-self:stretch;text-align:center;border-right:1px dashed var(--grid);padding-right:4px}
.uc-axis{padding-top:0}
.uc-axis .uc-cols{border-bottom:0;align-items:start;grid-template-rows:auto}
.uy{grid-row:1;display:none;justify-self:center;white-space:nowrap;padding-top:6px;font:400 13px/18px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.uy.w{display:block}.uy0{display:block;justify-self:start;line-height:16px}
.uy.end{justify-self:end}
.uy-brk{grid-row:1;justify-self:end;align-self:start;margin:-10px -8px 0 0;padding:0 2px;background:var(--bg);font:700 13px/16px Inter,sans-serif;letter-spacing:-.08em;color:var(--ink)}
/* S10 */
.grkey{display:flex;flex-wrap:wrap;gap:6px 22px;margin:0 0 8px;padding:0;list-style:none;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.grkey li{display:inline-flex;align-items:center;gap:7px}.grkey b{color:var(--ink);font-weight:600}
.gsw{display:inline-block;width:16px;height:16px;flex:none}
.gkn{margin:0 0 18px;max-width:$NOTEpx;font:400 14px/20px Inter,sans-serif;color:var(--sec);text-wrap:pretty}
.reg-share td.c-bar{width:220px}
.reg-share .aq{display:block}
.reg-share .aqq{display:block;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
/* social card */
.socialw{display:grid;grid-template-columns:minmax(0,1104px);gap:32px;align-items:start;padding-bottom:96px}
.cardnote{display:grid;grid-template-columns:240px minmax(0,1fr);gap:0 40px;max-width:1104px;font:400 15px/23px Inter,sans-serif}
.cardnote p{margin:0 0 14px}
.cardfig{margin:0;min-width:0}
.cardscroll{overflow:auto;width:1104px;max-width:100%;border:1px solid #5D636D;padding:11px;background:#FFFFFF}
.card{width:1080px;height:1350px;padding:84px 84px 64px;display:flex;flex-direction:column;background:var(--bg);color:var(--ink)}
.celab{margin:0;font:700 26px/32px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;border-top:4px solid var(--ink);padding-top:22px}
.celab span{font-weight:400;letter-spacing:0;text-transform:none;color:var(--sec)}
.ctitle{margin:22px 0 0;font:800 60px/64px "Inter Tight",sans-serif;letter-spacing:-.025em;text-wrap:balance}
.cmeasure{margin:18px 0 0;font:400 24px/33px Inter,sans-serif;color:var(--sec);text-wrap:pretty}
.crows{margin:40px 0 0;padding:0;list-style:none}
.crow{display:grid;grid-template-columns:320px minmax(0,1fr) 180px;align-items:center;gap:26px;padding:12px 0;border-bottom:2px solid var(--rq)}
.crow .cn{font:600 32px/40px Inter,sans-serif}
.ctrk{display:block;height:34px;background:var(--rq)}
.cbar{display:block;height:100%;background:var(--ink)}
.crow.all .cbar{background:var(--ctx)}
.crow.all .cn{color:var(--sec)}
.cv{font:800 68px/72px "Inter Tight",sans-serif;text-align:right;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.cscale{display:flex;justify-content:space-between;margin:8px 206px 0 346px;font:400 20px/28px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.cctx{margin:32px 0 0;font:400 28px/39px Inter,sans-serif;text-wrap:pretty}
.csrc{margin:auto 0 0;padding-top:24px;font:400 20px/28px Inter,sans-serif;color:var(--sec);text-wrap:pretty}
.cfoot{display:flex;justify-content:space-between;align-items:flex-end;gap:40px;margin-top:28px;border-top:2px solid var(--ink);padding-top:22px;font:400 20px/28px Inter,sans-serif;color:var(--sec)}
.cfoot p{margin:0;text-align:right;max-width:420px}
.cwm{display:inline-flex;color:var(--ink)}
.bul{margin:0 0 14px;padding-left:18px}.bul li{margin-bottom:6px}
/* system */
.sys{padding:0 0 72px}
.sh{display:flex;gap:14px;align-items:baseline;margin:0 0 20px;padding-top:14px;border-top:2px solid #121212;font:800 40px/44px "Inter Tight",sans-serif;letter-spacing:-.03em}
.sh span{font-size:22px;color:#4E535B;font-variant-numeric:tabular-nums}
.sp{max-width:44em;margin:0 0 16px;text-wrap:pretty}
.sys2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:48px;align-items:start}
.anatfig{padding-left:40px}
.anatfig .plate{grid-template-columns:minmax(0,1fr);row-gap:20px;padding-bottom:0}
.anatfig [data-anat]{position:relative}
.anatfig [data-anat]::before{content:attr(data-anat) / "";position:absolute;left:-38px;top:-1px;width:22px;height:22px;border-radius:50%;
background:#121212;color:#FFFFFF;font:700 13px/22px Inter,sans-serif;text-align:center;font-style:normal;letter-spacing:0;text-transform:none;font-variant-numeric:tabular-nums}
.anatfig .fig[data-anat]::before{top:-13px}
.anatfig .rnote[data-anat]::before{position:static;display:inline-block;margin-right:6px;vertical-align:1px}
.anatfig .strip{position:relative}
.anatfig .strip::before{content:"10" / "";position:absolute;left:-39px;top:-1px;width:22px;height:22px;border-radius:50%;background:#121212;color:#FFFFFF;font:700 13px/22px Inter,sans-serif;text-align:center}
.anat{margin:0 0 20px;padding:0;list-style:none;counter-reset:a;font:400 15px/22px Inter,sans-serif}
.anat li{counter-increment:a;display:grid;grid-template-columns:28px minmax(0,1fr);column-gap:8px;padding:8px 0;border-bottom:1px solid var(--rq)}
.anat li::before{content:counter(a);grid-row:span 2;font:800 17px/22px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
.anat b{font-weight:600}
.anat span{color:var(--sec)}
.cols2{columns:2;column-gap:48px;max-width:1040px}
.cols2 li{break-inside:avoid}
.pal{margin-bottom:28px}
.ramp .display{font-size:56px;line-height:60px}
.r-title{font:800 $T0px/$T1px "Inter Tight",sans-serif;letter-spacing:-.02em}
.r-big{display:inline-block;margin-left:-.04em;font:800 128px/112px "Inter Tight",sans-serif;letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.r-fig{font:800 22px/26px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
.r-lab{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.r-meas{font:400 15px/23px Inter,sans-serif;color:var(--sec)}
.r-cell{font:400 15px/22px Inter,sans-serif;font-variant-numeric:tabular-nums}
.r-head{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.r-clab{font:600 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums}
.r-note{font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.r-src{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.srcl{margin:0;padding:0;list-style:none;counter-reset:s}
.srcl li{counter-increment:s;display:grid;grid-template-columns:28px 150px minmax(0,1fr);gap:8px;padding:8px 0;border-bottom:1px solid var(--rq);font:400 15px/22px Inter,sans-serif}
.srcl li::before{content:counter(s);font:800 17px/22px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
.srcl b{font-weight:600}
.rule{margin:0 0 24px;padding:4px 0 4px 20px;border-left:2px solid #121212;max-width:56em;font:400 16px/25px Inter,sans-serif}
.rule footer{margin-top:8px;font:600 13px/18px Inter,sans-serif;font-style:normal;color:#4E535B}
.rdemos{display:grid;grid-template-columns:repeat(2,minmax(0,360px));gap:48px;margin-top:24px}
.rdemo{border-top:1px solid #121212;padding-top:10px}
.rdh{margin:0 0 12px;font:600 15px/22px Inter,sans-serif}
.rdt{margin:0 0 14px;font:800 22px/27px "Inter Tight",sans-serif;letter-spacing:-.02em;text-wrap:balance}
.rdn{margin:10px 0 0;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.rdc .ab{display:block;width:var(--abw);max-width:100%;height:auto}
.rdask{margin:14px 0 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.ask{display:inline-flex;align-items:center;min-height:48px;padding:0 18px;background:#E63946;color:#121212;font:700 19px/1 Inter,sans-serif;text-decoration:none}
.ill{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#4E535B}
.readl{margin:0;padding-left:22px;max-width:44em}.readl li{margin-bottom:10px;text-wrap:pretty}
.readl b{font-weight:600}
.dpal{margin:24px 0 8px;max-width:900px}
/* footer */
.foot{border-top:1px solid #5D636D;background:#FFFFFF;color:#4E535B}
.frow{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:24px;padding-top:16px;padding-bottom:40px;font:400 13px/18px Inter,sans-serif}
.frow p{margin:0}
/* forced colors: drawings and in-row bars keep their own ground and inks, so no mark is painted away */
@media (forced-colors:active){
 svg.ab,svg.u,svg.uk,svg.gl,.reg-track,.ptrk,.ctrk,.sw,.sw2,.gsw,.tsw{forced-color-adjust:none}
 svg.ab,svg.u,svg.uk,svg.gl,.sw,.reg-r:not(.reg-share) .seg{background-color:var(--bg)}
 .ptrk,.ctrk{background:Canvas;outline:1px solid CanvasText}
 .pbar,.cbar{background:CanvasText}
 .reg-share .seg,.gsw,.tsw,.sw2{outline:1px solid CanvasText;outline-offset:-1px}
 .tabs a[aria-current="page"]{box-shadow:none;text-decoration:underline;text-decoration-thickness:3px}
}
/* narrower desktops: the studio note moves under the figure */
@media (max-width:1309.98px){
 .plate{grid-template-columns:minmax(0,1fr);row-gap:20px}
 .strip{max-width:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:20px}
 .socialw{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:1000px){.sys2{grid-template-columns:minmax(0,1fr)}.strip{grid-template-columns:repeat(2,minmax(0,1fr))}.howto-l{columns:1}}
/* phones */
@media (max-width:899.98px){
 .cardnote{grid-template-columns:minmax(0,1fr)}
 .wrap{padding:0 16px}
 .mrow{grid-template-columns:1fr;gap:0;padding-top:0}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
 .tabs a{justify-content:flex-start}
 .vhead{padding:28px 0 24px}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .deck{font-size:17px;line-height:26px}
 .lead{margin-bottom:40px}
 .plate{padding-bottom:72px}
 .strip{display:block}
 .ftitle{font-size:$TP0px;line-height:$TP1px}
 .fbody{margin-top:18px}
 .fsrcrow{display:block}
 .fcred{text-align:left;margin-top:6px}
 .s01{grid-template-columns:minmax(0,1fr);gap:18px}
 .bign{font-size:96px;line-height:88px}
 .prow{grid-template-columns:104px minmax(0,1fr) 64px;gap:10px}
 .pv{font-size:24px}
 .scale{margin:6px 74px 0 114px}
 .uc{--u:$UNITPpx;--ucw:1fr}
 .uc-band{grid-template-columns:minmax(0,1fr);row-gap:6px;padding-top:16px}
 .uc-base,.uc-axis{padding-top:0}
 .uc-lab{padding-bottom:0}
 .uc-cols{--c0:34px;column-gap:2px}
 .uy.w{display:none}.uy.n{display:block}.uy0{display:block}
 .ub-s{grid-template-columns:repeat(3,auto);justify-content:start;column-gap:14px}
 .ubase{font-weight:400;font-variant-numeric:proportional-nums}
 .cols2{columns:1}
 .sh{font-size:30px;line-height:34px}
 .rdemos{grid-template-columns:minmax(0,1fr)}
 .srcl li{grid-template-columns:28px minmax(0,1fr)}
 .srcl li span{grid-column:2}
 .frow{grid-template-columns:minmax(0,1fr)}
 .socialw{padding-bottom:64px}
 .r-big{font-size:96px;line-height:88px}
 .anatfig{padding-left:34px}
 /* tables reflow to labeled rows, so none scrolls sideways */
 .reg.rf thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .reg.rf,.reg.rf tbody,.reg.rf tr,.reg.rf th,.reg.rf td{display:block;width:auto}
 .reg.rf tr{padding:10px 0;border-bottom:1px solid var(--rq)}
 .reg.rf tbody th,.reg.rf tbody td{border:0;padding:2px 0;text-align:left}
 .reg.rf td[data-label]::before{content:attr(data-label) ": ";font-weight:600;color:var(--sec)}
 .reg.rf td.n{text-align:left}
 .reg.rf caption,.reg-r caption,.s06 caption,.s01v caption,.s05r caption{display:block;width:auto}
 .reg.rf .sb::after{content:none}
 .contents a.cl{min-height:44px}
 /* the ranked register: name, bar, then the counts on labeled lines */
 .reg-r thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .reg-r,.reg-r tbody,.reg-r tfoot{display:block}
 .reg-r tr{display:flex;flex-wrap:wrap;column-gap:16px;row-gap:2px;padding:10px 0;border-bottom:1px solid var(--rq)}
 .reg-r tr>*{border:0!important;padding:0!important}
 .reg-r .c-h{flex:1 0 100%;order:0}
 .reg-r td.c-bar{flex:0 1 280px;width:auto;order:1;margin:4px 0 6px}
 .reg-r td.c-bar.empty{display:none}
 .reg-r td.n{order:2;text-align:left}
 .reg-r td.n::before{content:attr(data-label) " ";font:600 13px/18px Inter,sans-serif;color:var(--sec)}
 .reg-r td.empty{display:none}
 .reg-r tr.grp{padding-top:22px;border-bottom:1px solid var(--ctx)}
 .reg-r tfoot tr{border-top:1px solid var(--ink)}
 .reg-r .c-bar+td.n{flex-basis:auto}
 /* S06 on phones */
 .s06 thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .s06,.s06 tbody,.s06 tr,.s06 th,.s06 td{display:block;width:auto}
 .s06 tr{padding:12px 0;border-bottom:1px solid var(--rq)}
 .s06 tr>*{border:0!important;padding:3px 0!important}
 .s06 td::before{content:attr(data-label);display:block;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
 .s06 td{width:auto}
 /* S01 and S05 small registers */
 .s01v thead,.s05r thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .s01v,.s01v tbody,.s01v tr,.s01v th,.s01v td,.s05r,.s05r tbody,.s05r tr,.s05r th,.s05r td{display:block;width:auto}
 .s01v tr,.s05r tr{padding:10px 0;border-bottom:1px solid var(--rq)}
 .s01v tr>*,.s05r tr>*{border:0!important;padding:2px 0!important;text-align:left!important}
 .s01v td::before,.s05r td::before{content:attr(data-label) ": ";font-weight:600;color:var(--sec)}
}
"""

JS = r"""
(function(){
  'use strict';
  var VIEWS=['white','newsprint','dark','social','system'];
  var cur=null, first=true;
  function each(sel,fn){[].forEach.call(document.querySelectorAll(sel),fn);}
  function openTo(el){for(var p=el;p;p=p.parentElement){if(p.tagName==='DETAILS'&&!p.open)p.open=true;}}
  function focusIn(t){
    var f=(t.matches('[tabindex="-1"],summary,a,button')?t:null)||t.querySelector('.ftitle,[tabindex="-1"],summary');
    if(!f){f=t.querySelector('h1,h2');if(f)f.setAttribute('tabindex','-1');}
    if(f)f.focus({preventScroll:true});
  }
  // phones: the short guide and the index start closed, so the first chart's title sits on the first screen
  if(window.matchMedia&&matchMedia('(max-width:899.98px)').matches) each('.lead-d',function(d){d.open=false;});
  function route(){
    var h=decodeURIComponent(location.hash.slice(1)), v=h.split('-')[0];
    if(VIEWS.indexOf(v)<0) v='white';
    var root=document.querySelector('[data-view-root="'+v+'"]');
    each('[data-view-root]',function(r){r.hidden=r!==root;});
    each('.tabs a',function(a){if(a.getAttribute('href')==='#'+v)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    if(root&&root.getAttribute('data-title')) document.title=root.getAttribute('data-title');
    var t=h.indexOf('-')>0?document.getElementById(h):null;
    if(t){openTo(t);t.scrollIntoView();if(!first)focusIn(t);}
    else if(!first){window.scrollTo(0,0);var h1=root&&root.querySelector('h1');if(h1)h1.focus({preventScroll:true});}
    cur=v;first=false;
  }
  addEventListener('hashchange',route); route();
  // sortable registers: a header button sorts by that column; aria-sort says how
  document.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('button[data-sort]'); if(!b) return;
    var th=b.closest('th'), table=b.closest('table'), i=+b.getAttribute('data-sort');
    var dir=th.getAttribute('aria-sort')==='ascending'?'descending':'ascending';
    [].forEach.call(table.querySelectorAll('thead th[aria-sort]'),function(x){x.removeAttribute('aria-sort');});
    th.setAttribute('aria-sort',dir);
    var tb=table.tBodies[0], rs=[].slice.call(tb.rows);
    rs.sort(function(a,c){var x=a.cells[i].getAttribute('data-sv'), y=c.cells[i].getAttribute('data-sv');
      var nx=parseFloat(x), ny=parseFloat(y), r=(!isNaN(nx)&&!isNaN(ny)&&/^-?[\d.]+$/.test(x)&&/^-?[\d.]+$/.test(y))?nx-ny:String(x).localeCompare(String(y));
      return dir==='ascending'?r:-r;});
    rs.forEach(function(r){tb.appendChild(r);});
  });
  var skip=document.querySelector('.skip');
  if(skip) skip.addEventListener('click',function(ev){ev.preventDefault();
    var r=document.querySelector('[data-view-root]:not([hidden]) h1'); if(!r) return; r.focus(); r.scrollIntoView();});
})();
"""


def glyph_uri(kind, t):
    """The direction code as one 12 px glyph, drawn once per ground: the in-row bars repeat it, one glyph per change."""
    shape = {'tow': f"<rect x='.5' y='.5' width='11' height='11' fill='{t['tow']}'/>",
             'awy': f"<circle cx='6' cy='6' r='5.5' fill='{t['awy']}'/>",
             'kept': f"<rect x='.75' y='.75' width='10.5' height='10.5' fill='{t['bg']}' stroke='{t['ctx']}' stroke-width='1.5'/>",
             'mix': (f"<rect x='.75' y='.75' width='10.5' height='10.5' fill='{t['bg']}' stroke='{t['ctx']}' stroke-width='1.5'/>"
                     f"<path d='M1 7.7 7.7 1M1 11.4 11.4 1M4.3 11.4 11.4 4.3' stroke='{t['ctx']}' stroke-width='1' fill='none'/>"),
             'pend': (f"<rect x='.75' y='.75' width='10.5' height='10.5' fill='{t['bg']}' stroke='{t['ink']}' stroke-width='1.5' "
                      "stroke-dasharray='3 2'/>")}[kind]
    s_ = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'>{shape}</svg>"
    return 'url("data:image/svg+xml,' + s_.replace('#', '%23').replace('<', '%3C').replace('>', '%3E') + '")'


def ground_css():
    out = []
    for g, cls in GCLS.items():
        out.append(f'.{cls}{{{css_vars(G[g])}}}')
        for _, _, k in DIRS:
            u = glyph_uri(k, G[g])
            out.append(f'.{cls} .seg.k-{k},.{cls} .sw-{k}{{background-image:{u}}}')
    return '\n'.join(out)


def css():
    """The stylesheet, with the chart tokens written in (F16)."""
    ab = T['artboards']
    sub = {'$AB0Q': f'{ab[0] - .02:g}', '$AB1Q': f'{ab[1] - .02:g}', '$AB2Q': f'{ab[2] - .02:g}', '$AB0': str(ab[0]),
           '$UNITP': str(T['unit_phone']), '$UNIT': str(T['unit']), '$UGAP': str(T['unit_gap']), '$BARH': str(T['bar_h']),
           '$NOTE': str(T['note_px']), '$MEAS': str(T['measure_px']), '$SRC': str(T['source_px']),
           '$TP0': str(T['title_phone'][0]), '$TP1': str(T['title_phone'][1]), '$T0': str(T['title'][0]), '$T1': str(T['title'][1])}
    rng = [f'(min-width:{ab[0]}px)'] + [f'(min-width:{ab[i + 1]}px) and (max-width:{ab[i] - .02:g}px)' for i in range(len(ab) - 2)] \
        + [f'(max-width:{ab[-2] - .02:g}px)']
    sub['$UNDER'] = '\n'.join(f'@container {q}{{.fnotes li:has(.u-a{i}){{display:list-item}}}}' for i, q in enumerate(rng))
    out = CSS
    for k in sorted(sub, key=len, reverse=True):
        out = out.replace(k, sub[k])
    assert '$' not in out, re.findall(r'\$\w+', out)
    return out


ATTR_COPY = re.compile(r'\b(aria-label|data-title|title)="([^"]*)"')


def copy_pass(page):
    """The one copy function over the whole page: text nodes, and the names a screen reader reads (F16, RG-S1)."""
    page = typo_html(page)
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', page, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = ATTR_COPY.sub(lambda m: f'{m.group(1)}="{e(typo(html.unescape(m.group(2))))}"', parts[i])
    return ''.join(parts)


def text_nodes(page):
    page = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    return [html.unescape(t) for t in re.split(r'<[^>]+>', page) if t.strip()]


def build():
    views = ' '.join(v for v, _ in VIEWS)
    body = view_white() + view_newsprint() + view_dark() + view_social() + view_system()
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Register chart system</title>'
            f'<meta name="chart-views" content="{views}">'
            '<meta name="description" content="Chart-system concept 02 for the Oath &amp; Action brand guide: the numbers lead, every chart in one frame, with a register of the figures under it.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800'
            '&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{ground_css()}{css()}</style></head><body>'
            '<a class="skip" href="#main">Skip to the view</a>' + masthead()
            + f'<main id="main">{body}</main>' + footer() + f'<script>{JS}</script></body></html>')
    page = copy_pass(page)
    words = text_nodes(page)
    flat = ' '.join(words)
    assert '—' not in flat, 'em dash in page'
    assert "'" not in flat and '"' not in flat, [w for w in words if "'" in w or '"' in w][:5]
    assert not re.search(r'\b\d{4}-\d{2}-\d{2}\b', flat), 'ISO date in reader copy'
    assert not re.search(r'(?:^|[\s(])-\d', flat), 'hyphen used as a minus'
    # F12: the face of a chart names no colors, no source codes and no studio (the tables and the studio notes excepted)
    for m in re.finditer(r'<figure\b.*?</figure>', page, flags=re.S):
        face = re.sub(r'<details class="feq".*?</details>', '', m.group(0), flags=re.S)
        face = ' '.join(text_nodes(face))
        bad = re.findall(r'\b(Charcoal|Stone|Verdigris|Prussian|studio|N40|K1908|W035)\b', face)
        assert not bad, (m.group(0)[:80], bad)
    OUT.write_text(page)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1024:.0f} KB')


if __name__ == '__main__':
    build()
