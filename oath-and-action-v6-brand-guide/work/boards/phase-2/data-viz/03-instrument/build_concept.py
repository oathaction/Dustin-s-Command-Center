"""Build chart system concept 03, Instrument, for the data visualization round (November 6, 2026; fix pass the same day).

The chart kit (DR-49). Every chart is a module with seven fixed slots (A index, B title, C measure, D controls,
E figure, F notes, G source) on the Signal Grid's 8 px rhythm. A chart joins the kit with one call:

    register_chart('S03', dataset='rule-changes-by-instrument', gen=ranked_bar, adapter=spec_s03,
                   table=eq_s03, csv_cols=['key', 'value', ...])

The adapter reads the shared data and returns a spec: the copy for each slot and the data the generator draws.
Generators draw at any width, so the module asks for every artboard in CHART_TOKENS['artboards'] (866, 560, 358
and 328 px), for the 680 px still and for the social card:

    big_number(art, spec)       one figure set large, group bars on a 0 to 100 track, vote bars with a threshold
    line_events(art, spec)      lines with unjoined method breaks, event notes and direct labels
    ranked_bar(art, spec)       bars ranked by total, split by a category code; the scale comes from the largest total
    dumbbell(art, spec)         two dots per row on one cropped scale, the change in words
    small_multiples(art, spec)  one panel per group on one shared scale
    tile_map(art, spec)         equal tiles on the studio grid, coded by a status
    strip_timeline(art, spec)   lanes on one true time scale, each dot flagged with its year
    share_bars(art, spec)       100 percent bars, one per row, in the graded fill code
    comparison_table(uid, spec), unit_ledger(uid, spec), event_register(spec, hl)   HTML forms that reflow

Every generator draws through Art, which measures each label with the Inter files in ./fonts and refuses to build when
a label leaves its drawing, two labels touch, or a label meets a line, rule, leader or mark it does not sit in, all with
15 percent headroom for readers who widen text spacing. All copy passes through typo(): curly quotes and apostrophes,
ISO dates in words with no line break inside, the true minus. Chart values live in CHART_TOKENS, which the System
view prints.

Every value is read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json.

Run from the project root:
    python3 -I work/boards/phase-2/data-viz/03-instrument/build_concept.py
Writes 20261106_Data-Viz-03-Instrument.html beside this file, or stops and lists every layout fault it finds.
"""
import csv
import html
import io
import json
import math
import pathlib
import re
import sys

from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATA = json.loads((ROOT / 'work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json').read_text())
GRID = json.loads((ROOT / 'work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json').read_text())
OUT = HERE / '20261106_Data-Viz-03-Instrument.html'
DS = DATA['datasets']
SPECS = {s['id']: s for s in DATA['specimens']}
BUILD_DATE = '20261106'
MINUS, NBSP = '−', ' '

# ------------------------------------------------------------------------------------------------ chart tokens
# One source for every chart value. Generators read it; the System view prints it.
CHART_TOKENS = {
    'artboards': [('w', 866), ('m', 560), ('p', 358), ('n', 328)],   # shown when the module is at least this wide
    'still': 680,
    'social': {'w': 1080, 'h': 1350, 'margin': 64, 'min_scale': 1.3, 'artboard_search': (440, 640, 4), 'artboard_fallback': 600},   # 13 px labels print at 17 px or more on the card
    'page': {'columns': 12, 'gutter': 24, 'margin': 64, 'phone_margin': 16, 'module_columns': 8},
    'slot_space': {'A': 12, 'B': 8, 'C': 8, 'D': 16, 'E': 16, 'F': 16, 'G': 12, 'after': 16},
    'space': [4, 8, 12, 16, 24, 32, 48, 72],
    'type': {   # style: (face, weight, size px, line height px, tracking em)
        'title': ('Inter Tight', 800, 28, 32, -0.025), 'title_phone': ('Inter Tight', 800, 22, 26, -0.02),
        'kind': ('Inter', 700, 13, 18, 0.06), 'grade_words': ('Inter', 400, 13, 18, 0), 'index': ('Inter', 600, 13, 18, 0),
        'measure': ('Inter', 400, 15, 23, 0), 'series': ('Inter', 600, 15, 18, 0), 'data': ('Inter', 600, 13, 16, 0),
        'note': ('Inter', 400, 13, 16, 0), 'notes_slot': ('Inter', 400, 14, 20, 0), 'source': ('Inter', 400, 13, 18, 0),
        'big': ('Inter Tight', 800, 96, 96, -0.03), 'big_small': ('Inter Tight', 800, 72, 72, -0.03)},
    'lines': {'hair': 1, 'outline': 1.5, 'context': 2, 'named': 3, 'lit': 6},
    'bar': {'h': 24, 'pitch': 40},
    'share_bar': {'h': 18, 'pitch': 36},
    'group_bar': {'h': 20, 'pitch': 54},
    'vote_bar': {'h': 24},
    'unit': {'size': 24, 'gap': 4},
    'dot': {'later': 6, 'earlier': 5, 'timeline': 5, 'point': 4, 'vertex': 1.5},
    'tile_pitch': {866: 56, 560: 44, 358: 29, 328: 27},
    'breaks': {'side_labels': 640, 'big_side': 460, 'big_96': 700, 'four_panels': 760, 'two_panels': 460,
               'table_reflow': 640, 'map_years': 460, 'map_notes_beside': 760},
    'label_headroom': 1.15,
    'note_chars': (45, 75),
    'note_gap': 10,
    'big_bearing_em': 0.04,
    'inter_tight_factor': 0.955,
}
CT = CHART_TOKENS

# ------------------------------------------------------------------------------------------------ fonts and measuring
FONT_DIR = HERE / 'fonts'
FONT_FILES = {400: 'Inter-Regular.otf', 600: 'Inter-SemiBold.otf', 700: 'Inter-Bold.otf', 800: 'Inter-ExtraBold.otf'}
_missing = [n for n in FONT_FILES.values() if not (FONT_DIR / n).is_file()]
if _missing:
    raise SystemExit(f'build_concept.py measures labels with the Inter files in {FONT_DIR.name}/ beside it; missing: {", ".join(_missing)}')
_FONTS = {}


def _font(weight):
    weight = {500: 600}.get(weight, weight)
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONT_DIR / FONT_FILES[weight]), 200, layout_engine=ImageFont.Layout.RAQM)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False, track=0.0):
    """Width in px, tabular figures on. Inter Tight is measured as Inter ExtraBold times the tight factor."""
    text = str(text)
    w = _font(weight).getlength(text, features=['tnum']) * size / 200
    if tight:
        w *= CT['inter_tight_factor']
    return w + track * size * max(len(text) - 1, 0)


def wrap(text, width, size, weight=400, tight=False):
    out, line = [], ''
    for word in typo(text).split(' '):   # the copy pipeline first, then split on plain spaces only, so dates and law numbers stay whole
        trial = (line + ' ' + word).strip(' ')
        if line and tw(trial, size, weight, tight) > width:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out or ['']


def wrap_even(text, width, size, weight=400):
    """Wrap, then narrow the measure until no line is a single word left alone."""
    lines = wrap(text, width, size, weight)
    if len(lines) > 1 and len(lines[-1].split(' ')) == 1:
        w = width
        for _ in range(16):
            w -= 10
            alt = wrap(text, w, size, weight)
            if len(alt) == len(lines) and len(alt[-1].split(' ')) > 1:
                return alt
    return lines


# ------------------------------------------------------------------------------------------------ copy
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def date_words(iso):
    y, m, d = str(iso)[:10].split('-')
    return f'{MONTHS[int(m) - 1]}{NBSP}{int(d)},{NBSP}{y}'


MONTH_RE = '|'.join(MONTHS)


def iso_to_words(t):
    return re.sub(r'\b(\d{4})-(\d{2})-(\d{2})\b', lambda m: date_words(m.group(0)), str(t))


def typo(s):
    """The copy pipeline: dates in words, curly quotes and apostrophes, the true minus."""
    s = iso_to_words(s)
    s = re.sub(r"(?<![\w'’])'([^'\n]{1,80}?)'(?!\w)", '‘\\1’', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r'(?<=[\s(])-(?=\d)', MINUS, s)
    s = re.sub(rf'\b({MONTH_RE}) (\d{{1,2}}), (\d{{4}})\b', '\\1' + NBSP + '\\2,' + NBSP + '\\3', s)   # no break inside a date
    s = re.sub(rf'\b({MONTH_RE}) (\d{{1,2}}|\d{{4}})\b', '\\1' + NBSP + '\\2', s)
    s = re.sub(r'\b(H\.R\.|P\.L\.|S\.J\.Res\.|No\.|Question|Proposition|Amendment|Measure) (\d)', '\\1' + NBSP + '\\2', s)
    return s


def tx(s):
    return html.escape(typo(s), quote=False)


def at(s):
    return html.escape(typo(s), quote=True)


def ra(s):
    """A data attribute, exactly as the shared data holds it."""
    return html.escape(str(s), quote=True)


def svg_tx(s):
    """SVG text: figures in tabular tspans, so hyphens inside words keep their own width."""
    return re.sub(r'\d[\d.,%]*', lambda m: f'<tspan class="tn">{m.group(0)}</tspan>', tx(s))


def fmt(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def pct(v, d=1):
    return f'{v:.{d}f}'.replace('-', MINUS)


SENTENCE_END = r'(?<!\bv)(?<!\b[A-Z])\.\s(?=[A-Z])'   # a period before a capital, never after "v." or an initial


def first_sentence(t):
    m = re.search(SENTENCE_END, t)
    return t[:m.start() + 1] if m else t


def first_clause(t, limit=180):
    """The first sentence and its first clause, for the event register. A sentence ends at a period before a capital,
    never after "v." or an initial. A long clause is cut at a comma outside parentheses, or else at a space."""
    m = re.search(SENTENCE_END, t)
    c = (t[:m.start()] if m else t).rstrip('.').split('; ')[0]
    if len(c) <= limit:
        return c + '.'
    depth, commas = 0, []
    for i, ch in enumerate(c[:limit]):
        depth += (ch == '(') - (ch == ')')
        if ch == ',' and depth == 0:
            commas.append(i)
    cut = commas[-1] if commas and commas[-1] > 60 else c.rfind(' ', 0, limit)
    return c[:cut].rstrip(' ,') + '…'


def rows_of(did):
    return DS[did]['rows']


def rowmap(did):
    return {str(r['key']): r for r in DS[did]['rows']}


def frac_year(iso):
    import datetime
    y, m, d = (int(x) for x in str(iso)[:10].split('-'))
    start = datetime.date(y, 1, 1)
    return y + (datetime.date(y, m, d) - start).days / (datetime.date(y + 1, 1, 1) - start).days


def slug(s):
    return '-'.join(w.capitalize() for w in re.findall(r'[A-Za-z0-9]+', s))[:60]


def da(key, value=None, field=None, mark=None, axis=None, scale=None, cat=None, tip=None):
    s = f' data-key="{ra(key)}"'
    if field:
        s += f' data-field="{ra(field)}"'
    if value is not None:
        s += f' data-value="{fmt(value)}"'
    if cat is not None:
        s += f' data-category="{ra(cat)}"'
    if mark:
        s += f' data-mark="{mark}"'
    if axis:
        s += f' data-axis="{axis}"'
    if scale:
        s += f' data-scale="{ra(scale)}"'
    if tip:
        s += f' data-tip="{at(tip)}"'
    return s


# ------------------------------------------------------------------------------------------------ SVG primitives and the layout guard
STY = {'x13': (13, 400), 'x13b': (13, 600), 'x13s': (13, 600), 'x15': (15, 400), 'x15b': (15, 600), 'x15k': (15, 700),
       'xin': (13, 600), 'xint': (13, 600), 'xins': (13, 600), 'xkey': (13, 400)}
HAIR = {'grid', 'lane', 'lead', 'base', 'track'}
PROBLEMS = []


def R(x, y, w, h, cls, attrs=''):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(max(w, 0))}" height="{fmt(h)}" class="{cls}"{attrs}/>'


def LN(x1, y1, x2, y2, cls, attrs=''):
    return f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" class="{cls}"{attrs}/>'


def seg_hits_box(seg, box):
    """Liang-Barsky: does the segment enter the box?"""
    x1, y1, x2, y2 = seg
    l, t, r, b = box
    if r <= l or b <= t:
        return False
    dx, dy = x2 - x1, y2 - y1
    u0, u1 = 0.0, 1.0
    for p, q in ((-dx, x1 - l), (dx, r - x1), (-dy, y1 - t), (dy, b - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            u = q / p
            if p < 0:
                u0 = max(u0, u)
            else:
                u1 = min(u1, u)
            if u0 > u1:
                return False
    return True


def boxes_overlap(a, b, pad=0.0):
    return min(a[2], b[2]) - max(a[0], b[0]) > pad and min(a[3], b[3]) - max(a[1], b[1]) > pad


class Art:
    """One artboard. Records every label, line and mark it draws, so check() can refuse a faulty drawing."""
    HR = CT['label_headroom']

    def __init__(self, W, name, g):
        self.W, self.name, self.g = W, name, g
        self.H, self.bleed, self.defs = 0.0, 0.0, ''
        self.o, self.texts, self.lines, self.rects, self.strings = [], [], [], [], []

    def _add(self, m):
        self.o.append(m)
        return len(self.o)

    def raw(self, m):
        self._add(m)

    def rect(self, x, y, w, h, cls, attrs='', host=False, block=True):
        self._add(R(x, y, w, h, cls, attrs))
        self.rects.append({'box': (x, y, x + w, y + h), 'block': block})
        return len(self.rects) - 1

    def circle(self, cx, cy, r, cls, attrs=''):
        self._add(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" class="{cls}"{attrs}/>')
        self.rects.append({'box': (cx - r, cy - r, cx + r, cy + r), 'block': True})

    def line(self, x1, y1, x2, y2, cls, kind='rule', attrs=''):
        if cls in HAIR:   # 1 px hairlines on half pixels, so a still exported at 1x prints them crisp
            if y1 == y2:
                y1 = y2 = math.floor(y1) + 0.5
            if x1 == x2:
                x1 = x2 = math.floor(x1) + 0.5
        order = self._add(LN(x1, y1, x2, y2, cls, attrs if 'aria-hidden' in attrs else attrs + ' aria-hidden="true"'))
        self.lines.append({'seg': (x1, y1, x2, y2), 'kind': kind, 'order': order})

    def poly(self, pts, cls, kind='series'):
        d = 'M' + ' L'.join(f'{fmt(p)} {fmt(q)}' for p, q in pts)
        order = self._add(f'<path d="{d}" class="{cls}" aria-hidden="true"/>')
        for (p, q), (r, s) in zip(pts, pts[1:]):
            self.lines.append({'seg': (p, q, r, s), 'kind': kind, 'order': order})

    def marks(self, markup, segs, kind='mark'):
        order = self._add(markup)
        for s in segs:
            self.lines.append({'seg': s, 'kind': kind, 'order': order})

    def text(self, x, y, s, cls, anchor='start', attrs='', rows=None, lh=16, inside=None, knock=False, record=True):
        rows = rows if rows is not None else [s]
        size, weight = STY[cls]
        w = max(tw(r, size, weight) for r in rows)
        x0 = x if anchor == 'start' else (x - w if anchor == 'end' else x - w / 2)
        yb = y + lh * (len(rows) - 1)
        if knock:   # a band in the ground color, so gridlines drawn earlier stop short of the words
            self._add(R(x0 - 4, y - 0.8 * size - 2, w + 8, yb - y + 1.05 * size + 4, 'knock', ' aria-hidden="true"'))
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        if len(rows) == 1:
            m = f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}"{a}{attrs}>{svg_tx(rows[0])}</text>'
        else:
            spans = ''.join(f'<tspan x="{fmt(x)}" dy="{0 if i == 0 else lh}">{svg_tx(r)}</tspan>' for i, r in enumerate(rows))
            m = f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}"{a}{attrs}>{spans}</text>'
        order = self._add(m)
        self.texts.append({'x0': x0, 'w': w, 'anchor': anchor, 'y': y, 'yb': yb, 'size': size, 'inside': inside,
                           'knock': knock, 'order': order, 's': ' '.join(rows)})
        if record:
            self.strings.append(' '.join(rows))
        return w

    def custom_text(self, markup, x0, y, w, size, s):
        order = self._add(markup)
        self.texts.append({'x0': x0, 'w': w, 'anchor': 'start', 'y': y, 'yb': y, 'size': size, 'inside': None,
                           'knock': False, 'order': order, 's': s})

    def _box(self, t, full=True, head=True):
        w = t['w'] * (self.HR if head else 1)
        if t['anchor'] == 'start':
            l, r = t['x0'], t['x0'] + w
        elif t['anchor'] == 'end':
            r = t['x0'] + t['w']
            l = r - w
        else:
            c = t['x0'] + t['w'] / 2
            l, r = c - w / 2, c + w / 2
        if full:
            return (l, t['y'] - 0.97 * t['size'], r, t['yb'] + 0.25 * t['size'])
        return (l, t['y'] - 0.74 * t['size'], r, t['yb'] + 0.22 * t['size'])

    def check(self):
        P, tag = [], f'{self.name} at {fmt(self.W)} px'
        for t in self.texts:
            b = self._box(t)
            if b[0] < -self.bleed - 0.5 or b[2] > self.W + 0.5 or b[1] < -0.5 or b[3] > self.H + 0.5:
                P.append(f'{tag}: "{t["s"][:40]}" leaves the drawing, with 15% headroom')
        for i, t in enumerate(self.texts):
            for u in self.texts[i + 1:]:
                if boxes_overlap(self._box(t), self._box(u), 1.5):
                    P.append(f'{tag}: "{t["s"][:30]}" touches "{u["s"][:30]}"')
        for t in self.texts:
            ink = self._box(t, full=False)
            core = (ink[0] + 0.5, ink[1] + 0.5, ink[2] - 0.5, ink[3] - 0.5)
            for ln in self.lines:
                if t['knock'] and ln['kind'] in ('grid', 'lane', 'rule', 'base') and ln['order'] < t['order']:
                    continue
                if seg_hits_box(ln['seg'], core):
                    P.append(f'{tag}: a {ln["kind"]} line crosses "{t["s"][:40]}"')
            for k, rc in enumerate(self.rects):
                if k == t['inside'] or not rc['block']:
                    continue
                if boxes_overlap(ink, rc['box'], 1.0):
                    P.append(f'{tag}: "{t["s"][:40]}" sits on a mark it does not label')
            if t['inside'] is not None:
                hb = self.rects[t['inside']]['box']
                own = self._box(t, full=False, head=False)
                if own[0] < hb[0] + 1 or own[2] > hb[2] - 1:
                    P.append(f'{tag}: "{t["s"][:30]}" does not fit inside its mark')
        return P

    def svg(self, uid, art, label, extra_cls=''):
        PROBLEMS.extend(self.check())
        aid = f'{uid}-{art}'   # pattern ids, unique per view and artboard, with no spaces, so url(#...) resolves
        d = f'<defs>{self.defs}</defs>'.replace(ART_ID, aid) if self.defs else ''
        body = ''.join(self.o).replace(ART_ID, aid)
        wt = self.W + self.bleed
        style = f' style="margin-left:{fmt(-self.bleed)}px"' if self.bleed else ''
        return (f'<svg class="art art-{art}{extra_cls}" data-view="{uid}-{art}" data-w="{fmt(self.W)}" viewBox="{fmt(-self.bleed)} 0 {fmt(wt)} {fmt(self.H)}" '
                f'width="{fmt(wt)}" height="{fmt(self.H)}"{style} role="img" aria-label="{at(label)}" focusable="false">{d}{body}</svg>')


def place_flags(items, x_max, gap=6.0):
    """Tier flag labels above a line so no label covers another's leader: a label that covers another dot sits above
    that dot's label, and labels that overlap never share a tier."""
    for it in items:
        it['anchor'] = 'start' if it['x'] + it['w'] <= x_max else 'end'

    def span(it):
        return (it['x'], it['x'] + it['w']) if it['anchor'] == 'start' else (it['x'] - it['w'], it['x'])

    def covers(i, k):
        a, b = span(i)
        return i is not k and a - 3 <= k['x'] <= b + 3

    for _ in range(len(items) * 2):
        flip = next((i for i in items for k in items if i['anchor'] == 'start' and covers(i, k) and covers(k, i)), None)
        if not flip:
            break
        flip['anchor'] = 'end'
    left, done = list(items), []
    while left:
        ready = [i for i in left if not any(covers(i, k) for k in left)] or [min(left, key=lambda i: i['x'])]
        for i in sorted(ready, key=lambda i: i['x']):
            a, b = span(i)
            t = max([k['t'] + 1 for k in done if covers(i, k)] + [0])
            while any(k['t'] == t and not (b + gap < k['a'] or a > k['b'] + gap) for k in done):
                t += 1
            i['t'], i['a'], i['b'] = t, a, b
            done.append(i)
            left.remove(i)
    return items


# ------------------------------------------------------------------------------------------------ grounds
GROUNDS = {
    'white': {'gr': '#FFFFFF', 'ink': '#121212', 'ctx': '#5D636D', 'sec': '#4E535B', 'grid': '#CBCED1', 'rule': '#5D636D',
              'alt': '#DCD9D2', 'focus': '#121212', 'tow': '#3C5F59', 'on-tow': '#FFFFFF', 'away': '#121212',
              'on-away': '#FFFFFF', 'kept': '#B3B6BB', 'some': '#5D636D', 'on-some': '#FFFFFF', 'g2': '#616161', 'pl': '#B3B6BB',
              'vdl': '#ACC2BE', 'vdxl': '#DDE6E5', 'prl': '#A2AABF', 'prxl': '#DCDFE7', 'pr': '#1F2D5A', 'red': '#E63946'},
    'newsprint': {'gr': '#DCD9D2', 'ink': '#121212', 'ctx': '#5D636D', 'sec': '#4E535B', 'grid': '#B4B4B3', 'rule': '#5D636D',
                  'alt': '#FFFFFF', 'focus': '#121212', 'tow': '#3C5F59', 'on-tow': '#FFFFFF', 'away': '#121212',
                  'on-away': '#DCD9D2', 'kept': '#A1A2A3', 'some': '#5D636D', 'on-some': '#FFFFFF', 'g2': '#565553', 'pl': '#A1A2A3',
                  'vdl': '#9AAEA6', 'vdxl': '#C1C8C0', 'prl': '#8E94A4', 'prxl': '#BEBFC1', 'pr': '#1F2D5A', 'red': '#E63946'},
    'charcoal': {'gr': '#121212', 'ink': '#DCD9D2', 'ctx': '#A3A19C', 'sec': '#A3A19C', 'grid': '#393C41', 'rule': '#878A8F',
                 'alt': '#121212', 'focus': '#DCD9D2', 'tow': '#76978F', 'on-tow': '#121212', 'away': '#DCD9D2',
                 'on-away': '#121212', 'kept': '#393C41', 'some': '#878A8F', 'on-some': '#121212', 'g2': '#A3A19C', 'pl': '#5D636D',
                 'vdl': '#3F655E', 'vdxl': '#2E4340', 'prl': '#80889C', 'prxl': '#393C41', 'pr': '#80889C', 'red': '#E63946'},
}
GCLS = {'white': 'g-white', 'newsprint': 'g-news', 'charcoal': 'g-dark'}
MIX = {   # each lab tint as the OKLab mix the palette lab made, recovered by script (zero error)
    'tow': 'Verdigris 25% toward Charcoal', 'kept': 'Stone 55% toward the ground', 'pl': 'Stone 55% toward the ground',
    'g2': 'Charcoal 38% toward the ground', 'vdl': 'Verdigris 55% toward the ground', 'vdxl': 'Verdigris 82% toward the ground',
    'prl': 'Prussian 62% toward the ground', 'prxl': 'Prussian 86% toward the ground', 'grid': 'Stone 70% toward the ground'}


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def ground_css():
    return '\n'.join(f'.{GCLS[g]}{{' + ';'.join(f'--{k}:{v}' for k, v in t.items()) + f';background:{t["gr"]};color:{t["ink"]}}}'
                     for g, t in GROUNDS.items())


# ------------------------------------------------------------------------------------------------ codes after color
DIRS = [('away from voters', 'away', 'Away from voters'), ('toward voters', 'tow', 'Toward voters'),
        ('voters kept existing rules', 'kept', 'Kept existing rules'), ('mixed', 'mixed', 'Mixed'), ('pending', 'pend', 'Pending')]
DIR_CLS = {d: c for d, c, _ in DIRS}
DIR_WORD = {d: w for d, _, w in DIRS}
FILL = {'away': 'f-away', 'tow': 'f-tow', 'kept': 'f-kept', 'pend': 'f-pend', 'mixed': 'f-tow'}
ONTXT = {'away': 'xin', 'tow': 'xint', 'kept': 'x13b', 'pend': 'x13b', 'mixed': 'xin'}


def dir_markup(x, y, w, h, c, attrs=''):
    """The repair log's direction code. Away: solid Charcoal. Toward: Verdigris strong with an inner frame in the
    ground color, so the two differ by fill as well as shade. Kept: light fill with an outline. Mixed: both fills
    split on the diagonal. Pending: an open outline."""
    s = R(x, y, w, h, FILL[c], attrs)
    if c == 'tow' and w >= 10 and h >= 10:
        s += R(x + 3, y + 3, w - 6, h - 6, 'frame', ' aria-hidden="true"')
    if c == 'mixed':
        s += f'<path d="M{fmt(x + w)} {fmt(y)}V{fmt(y + h)}H{fmt(x)}Z" class="f-away" aria-hidden="true"/>'
    return s


def dir_shape(a, x, y, w, h, c, attrs=''):
    a.raw(dir_markup(x, y, w, h, c, attrs))
    a.rects.append({'box': (x, y, x + w, y + h), 'block': True})
    return len(a.rects) - 1


GRADES = [('documented', 'Documented', 'on the public record', 'solid', 'record language: was, passed, logged'),
          ('well-supported', 'Well supported', 'strong research evidence', 'solid', 'a direct finding: raises, lowers'),
          ('plausible', 'Plausible', 'some evidence', 'dashed', '“can” or “may”'),
          ('contested', 'Contested', 'evidence disputed', 'dash-dot', 'both readings, side by side'),
          ('hypothesis', 'Hypothesis', 'untested', 'dotted', '“untested”')]
GRADE_FILL = {'documented': 'Solid, the darkest ink', 'well-supported': 'Solid, a gray step lighter',
              'plausible': 'Light solid tint with an outline', 'contested': 'Diagonal hatch with an outline',
              'hypothesis': 'Dots with an outline'}
LINE_DASH = {'solid': '', 'dashed': '8 4', 'dash-dot': '8 3 2 3', 'dotted': '0 5'}


ART_ID = '@ART@'   # stands for the artboard's id until Art.svg() writes it


def grade_defs(uid):
    return (f'<pattern id="{uid}-ct" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="5" height="5" class="pbg"/><path d="M0 0V5" class="phs"/></pattern>'
            f'<pattern id="{uid}-hy" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" class="pbg"/>'
            f'<circle cx="3" cy="3" r="1.2" class="pdt"/></pattern>')


def grade_markup(uid, g, x, y, w, h, attrs=''):
    if g == 'documented':
        return R(x, y, w, h, 'f-ink', attrs)
    if g == 'well-supported':
        return R(x, y, w, h, 'f-g2', attrs)
    if g == 'plausible':
        return R(x, y, w, h, 'f-pl', attrs)
    pid = f'{uid}-ct' if g == 'contested' else f'{uid}-hy'
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" class="f-tex" fill="url(#{pid})"{attrs}/>'


def line_sample(style, w=36):
    dash = LINE_DASH[style]
    da_ = f' stroke-dasharray="{dash}"' if dash else ''
    cap = ' stroke-linecap="round"' if style == 'dotted' else ''
    return (f'<svg class="mks" viewBox="0 0 {w} 10" width="{w}" height="10" aria-hidden="true" focusable="false">'
            f'<path d="M1 5H{w - 1}" class="lsam"{da_}{cap}/></svg>')


def red_mark(path_d, ground, red=True):
    """The one working red: the point the title names. On Newsprint it takes a 1 px Charcoal keyline (R09)."""
    key = f'<path d="{path_d}" class="redkey"/>' if ground == 'newsprint' and red else ''
    cls = 'redmark' if red else 'inkmark'
    attrs = ' data-red="working" data-red-job="headline point"' if red else ''
    return f'<g class="redg"{attrs}>{key}<path d="{path_d}" class="{cls}"/></g>'


def key_row(a, items, y, W=None):
    """An inline key inside the drawing: (draw, words) pairs that wrap at the drawing's width."""
    W = W or a.W
    x = 0
    for draw, words in items:
        w = 20 + tw(words, 13) * CT['label_headroom'] + 18
        if x and x + w > W:
            x, y = 0, y + 22
        draw(x, y - 11)
        a.text(x + 20, y, words, 'xkey')
        x += w
    return y + 12


# ------------------------------------------------------------------------------------------------ generators
def big_number(a, s):
    """One figure set large; group bars on a 0 to 100 track with names printed; vote bars holding every vote cast,
    with a threshold tick and, when the title names it, the shortfall in red."""
    W, g = a.W, a.g
    side = W >= CT['breaks']['big_side']
    fs = CT['type']['big'][2] if W >= CT['breaks']['big_96'] else CT['type']['big_small'][2]
    fig = s['figure']
    txt = f'{fig["value"]}%'
    bigw = tw(txt, fs, 800, tight=True, track=-0.03)
    lc = max(bigw + 28, round(W * 0.3)) if side else W
    yb = round(0.97 * fs) + 4
    a.bleed = round(CT['big_bearing_em'] * fs, 1)   # set the figure's ink flush with the title's left edge
    a.custom_text(f'<text x="{fmt(-a.bleed)}" y="{yb}" class="xbig" style="font-size:{fs}px"{da(fig["key"], fig["value"], mark="label")}>'
                  f'<tspan class="tn">{fig["value"]}</tspan>%</text>', -a.bleed, yb, bigw, fs, txt)
    y = yb + round(0.25 * fs) + 18
    cap = wrap(fig['caption'], lc - 16, 15)
    a.text(0, y, '', 'x15', rows=cap, lh=20)
    y += 20 * (len(cap) - 1) + 20
    a.text(0, y, fig['sub'], 'x13')
    big_bottom = y + 8
    x0 = lc + 28 if side else 0
    lab_w = tw('100%', 15, 700) * CT['label_headroom'] + 10
    k = (W - x0 - lab_w) / 100
    y = 16 if side else big_bottom + 30
    a.text(x0, y, s['group_head'], 'x13')
    a.text(x0 + 100 * k, y, '100%', 'x13', 'end')
    y += 12
    gb = CT['group_bar']
    for grp in s['groups']:
        cls = 'f-ctx' if grp.get('context') else 'f-ink'
        if grp.get('party'):
            a.raw(f'<g data-party="{ra(grp["party"])}">')
        a.text(x0, y + 15, grp['label'], 'x15b')
        a.raw(R(x0, y + 22, 100 * k, gb['h'], 'track', ' aria-hidden="true"'))
        for seg in ((x0, y + 22, x0 + 100 * k, y + 22), (x0, y + 22 + gb['h'], x0 + 100 * k, y + 22 + gb['h']),
                    (x0 + 100 * k, y + 22, x0 + 100 * k, y + 22 + gb['h'])):
            a.lines.append({'seg': seg, 'kind': 'track', 'order': len(a.o)})
        a.rect(x0, y + 22, grp['value'] * k, gb['h'], cls, da(grp['key'], grp['value'], mark='bar', axis='x', scale='groups'))
        a.text(x0 + 100 * k + 8, y + 22 + 15, f'{grp["value"]}%', 'x15k', attrs=da(grp['key'], grp['value'], mark='label'))
        if grp.get('party'):
            a.raw('</g>')
        y += gb['pitch']
    y = max(big_bottom, y - 14) + 30
    a.line(0, y - 20, W, y - 20, 'grid', 'grid')
    a.text(0, y, s['vote_head'], 'x13')
    y += 26
    vb = CT['vote_bar']['h']
    for v in s['votes']:
        hl = wrap_even(v['label'], W / CT['label_headroom'], 15, 600)
        a.text(0, y, '', 'x15b', rows=hl, lh=19)
        y += 19 * (len(hl) - 1)
        if v.get('sub'):
            sl = wrap_even(v['sub'], W / CT['label_headroom'], 13)
            a.text(0, y + 18, '', 'x13', rows=sl, lh=16)
            y += 18 + 16 * (len(sl) - 1)
        y += 12
        total = sum(sg['value'] for sg in v['segs'])
        kv = W / total
        x = 0
        for i, sg in enumerate(v['segs']):
            host = dir_shape(a, x, y, sg['value'] * kv, vb, sg['code'], da(sg['key'], sg['value'], mark='bar', axis='x', scale=v['scale']))
            words = f'{sg["value"]} {sg["word"]}'
            if i == 0:
                a.text(x + 8, y + 17, words, ONTXT[sg['code']], attrs=da(sg['key'], sg['value'], mark='label'), inside=host)
            else:
                a.text(x + sg['value'] * kv - 8, y + 17, words, ONTXT[sg['code']], 'end', da(sg['key'], sg['value'], mark='label'), inside=host)
            x += sg['value'] * kv
        th = v.get('threshold')
        if th:
            xn = th['value'] * kv
            a.line(xn, y - 6, xn, y + vb + 16, 'tick2', 'tick', da(th['key'], th['value'], mark='label'))
            rd = v['red']
            yr = y + vb + 12
            x1, x2 = rd['from'] * kv + 1.5, xn - 1.5
            d = f'M{fmt(x1)} {fmt(yr - 7)}V{fmt(yr)}H{fmt(x2)}V{fmt(yr - 7)}'
            a.marks(red_mark(d, g['ground'], g.get('red', True)), [(x1, yr - 7, x1, yr), (x1, yr, x2, yr), (x2, yr, x2, yr - 7)])
            room = W - xn - 12
            lab = wrap_even(rd['words'], room / CT['label_headroom'], 13, 600) if room >= 120 else wrap_even(rd['words'], W / CT['label_headroom'], 13, 600)
            lx, ly = (xn + 10, yr + 5) if room >= 120 else (0, yr + 22)
            a.text(lx, ly, '', 'x13b', rows=lab, lh=16)
            y = ly + 16 * (len(lab) - 1) + 8
        else:
            y += vb + 30
    a.H = y


def line_events(a, s):
    """Lines on one value scale. Estimates that change method at a break year are never joined; notes sit at their
    point with a 1 px leader, or under the plot on narrow drawings."""
    W = a.W
    narrow = W < CT['breaks']['big_side']
    x_lo, x_hi = s['x_range']
    y_max, step = s['y_max'], s['y_step']
    flags = []
    for b in s['breaks']:
        flags.append({'x': 0, 'w': tw(b['word'], 13) * CT['label_headroom'] + 6, 'brk': b})
    px0 = 46
    px1 = W - (16 if narrow else s['right_margin'])
    X = lambda v: px0 + (v - x_lo) * (px1 - px0) / (x_hi - x_lo)
    for f_ in flags:
        f_['x'] = X(f_['brk']['x'])
    place_flags(flags, W, gap=10)
    tiers = max(f_['t'] for f_ in flags) + 1 if flags else 0
    top = 14 + tiers * 18 + 8
    ph = s['plot_h'][1 if narrow else 0]
    pb = top + ph
    Y = lambda v: pb - v * ph / y_max
    for v in range(0, y_max + 1, step):
        a.line(px0 - 8, Y(v), W, Y(v), 'base' if v == 0 else 'grid', 'base' if v == 0 else 'grid')
        a.text(px0 - 12, Y(v) + 4.5, f'{v}%' if v == y_max else str(v), 'x13', 'end')
    for i, yr in enumerate(s['x_ticks']):
        anchor = 'end' if (narrow and i == len(s['x_ticks']) - 1) else 'middle'
        a.text(min(X(yr) + (14 if anchor == 'end' else 0), W), pb + 20, str(yr), 'x13', anchor)
    for f_ in flags:
        b = f_['brk']
        ty = 14 + (tiers - 1 - f_['t']) * 18   # tier 0 sits nearest the plot
        tx_ = f_['x'] + 4 if f_['anchor'] == 'start' else f_['x'] - 4
        a.text(tx_, ty, b['word'], 'x13', f_['anchor'])
        a.line(f_['x'], ty - 10, f_['x'], Y(b['top']) - 8, 'lead', 'lead')
    for ser in s['series']:
        for seg in ser['segments']:
            pts = [(X(p['x']), Y(p['v'])) for p in seg]
            if len(pts) > 1:
                a.poly(pts, ser['line'])
            for p in seg:
                r = ser['dot_big'] if p.get('big') else ser['dot']
                a.circle(X(p['x']), Y(p['v']), r, ser['fill'], da(p['key'], p['v'], mark='point', axis='y', tip=p['tip']))
    wide = W >= CT['breaks']['four_panels']
    for lb in s['labels']['wide' if wide else 'other']:
        if lb['text']:
            a.text(X(lb['x']), Y(lb['v']), lb['text'], lb['cls'], lb.get('anchor', 'start'), lb.get('attrs', ''), knock=True)
    y_end = pb + 30
    for nt in s['plot_notes']:
        if not wide:
            rows = wrap_even(nt.get('text_other', nt['text']), W / CT['label_headroom'], 13)
            a.text(0, y_end + 16, '', 'x13', rows=rows, lh=16)
            y_end += 16 * len(rows) + 10
            continue
        rows = wrap_even(nt['text'], nt['chars'] * 6.4, 13)
        ty, xr = Y(nt['top']), (W - 2 if nt.get('edge') else X(nt['right']))
        a.text(xr, ty, '', 'x13', 'end', rows=rows, lh=16, knock=True)
        yl, yb_ = Y(nt['v']), ty + 16 * (len(rows) - 1)
        if ty - 12 <= yl <= yb_ + 4:   # the point sits beside the block: a level leader
            a.line(xr + 6, yl, X(nt['x']) - 7, yl, 'lead', 'lead')
        else:                           # the point sits above the block: a leader down to its top
            a.line(X(nt['x']), yl + 7, X(nt['x']), ty - 15, 'lead', 'lead')
    a.H = y_end - 4


def ranked_bar(a, s):
    """Rows ranked by total, each bar split by a category code with the count inside where it fits. The scale comes
    from the largest total in the rows, so any rows drop in."""
    W = a.W
    rows = s['rows']
    top_total = max(r['total'] for r in rows)
    y = key_row(a, [((lambda c: (lambda x, yy: dir_shape(a, x, yy, 14, 14, c)))(c), w) for c, w in s['key']], 14) + 12
    side = W >= CT['breaks']['side_labels']
    unit_label = f'{top_total} {s["unit"]}'
    if side:
        lw = max(tw(r['label'], 15, 600) for r in rows) * CT['label_headroom'] + 14
        rmax = tw(unit_label, 15, 700) * CT['label_headroom'] + 12
        k = (W - lw - rmax) / top_total
    else:
        lw, k = 0, W / top_total
    bh = CT['bar']['h']
    for i, r in enumerate(rows):
        tot_txt = unit_label if i == 0 else str(r['total'])
        if side:
            by = y
            a.text(0, by + 17, r['label'], 'x15b')
            if r.get('sub'):
                a.text(0, by + 35, r['sub'], 'x13')
        else:
            a.text(0, y + 15, r['label'], 'x15b')
            a.text(W, y + 15, tot_txt, 'x15k', 'end', da(r['key'], r['total'], mark='label'))
            by = y + 22
        x = lw
        for sg in r['segs']:
            if not sg['value']:
                continue
            w = sg['value'] * k
            host = dir_shape(a, x, by, w, bh, sg['code'], da(r['key'], sg['value'], field=sg['field'], mark='bar', axis='x'))
            if w >= 18:
                a.text(x + w / 2, by + 17, str(sg['value']), ONTXT[sg['code']], 'middle', da(r['key'], sg['value'], field=sg['field'], mark='label'), inside=host)
            x += w
        extra = 0
        if side:
            a.text(x + 8, by + 17, tot_txt, 'x15k', attrs=da(r['key'], r['total'], mark='label'))
            xe = x + 8 + tw(tot_txt, 15, 700) * CT['label_headroom'] + 14
            if r.get('note'):
                room = W - xe
                rows_ = wrap_even(r['note'], room / CT['label_headroom'], 13) if room >= 150 else None
                if rows_ and len(rows_) <= 2:
                    a.text(xe, by + 17 - 8 * (len(rows_) - 1), '', 'x13', rows=rows_, lh=16)
                else:
                    a.text(lw, by + bh + 18, r['note'], 'x13')
                    extra = 24
            y = by + bh + 16 + extra + (8 if r.get('sub') else 0)
        else:
            for nt in (r.get('sub'), r.get('note')):
                if nt:
                    rows_ = wrap_even(nt, W / CT['label_headroom'], 13)
                    a.text(0, by + bh + 18 + extra, '', 'x13', rows=rows_, lh=16)
                    extra += 16 * len(rows_) + 6
            y = by + bh + 18 + extra
    a.H = y


def dumbbell(a, s):
    """Two dots per row on one scale; the later year filled, the earlier an open ring; values printed beside the
    dots and the change in words at the right. The scale is cropped to whole tens around the data."""
    W = a.W
    side = W >= CT['breaks']['side_labels']
    vals = [v for r in s['rows'] for v in (r['a']['v'], r['b']['v'])]
    lo = int(math.floor((min(vals) - 4) / 10) * 10)
    hi = int(math.ceil((max(vals) + 4) / 10) * 10)
    lw = (max(tw(r['label'], 15, 600) for r in s['rows']) * CT['label_headroom'] + 16) if side else 0
    cw = (max(tw(r['change'], 13, 600) for r in s['rows']) * CT['label_headroom'] + 16) if side else 0
    x0 = lw + 22
    x1 = W - cw - 34 if side else W - 34
    X = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)
    y = 14
    for v in range(lo, hi + 1, 10):
        a.text(X(v), y, f'{v}%' if v == hi else str(v), 'x13', 'middle')
    y += 20
    dot = CT['dot']
    first = True
    for r in s['rows']:
        if r.get('context'):
            a.line(0, y - 2, W, y - 2, 'grid', 'grid')
            y += 10
        lab_cls = 'x15' if r.get('context') else 'x15b'
        if side:
            cy = y + (40 if first else 24)
            a.text(0, cy + 5, r['label'], lab_cls)
            a.text(W, cy + 5, r['change'], 'x13b', 'end')
        else:
            a.text(0, y + 15, r['label'], lab_cls)
            two = (tw(r['label'], 15, 600) + tw(r['change'], 13, 600)) * CT['label_headroom'] + 16 > W
            a.text(W if not two else 0, y + (15 if not two else 33), r['change'], 'x13b', 'end' if not two else 'start')
            cy = y + (66 if first else 46) + (18 if two else 0)
        xa, xb = X(r['a']['v']), X(r['b']['v'])
        if abs(xa - xb) > dot['later'] + dot['earlier']:
            a.line(min(xa, xb) + 5, cy, max(xa, xb) - 5, cy, 'l-ctx2', 'series')
        fill = 'f-ctx' if r.get('context') else 'f-ink'
        a.circle(xb, cy, dot['later'], fill, da(r['b']['key'], r['b']['v'], mark='point', axis='x'))
        a.circle(xa, cy, dot['earlier'], 'ring', da(r['a']['key'], r['a']['v'], mark='point', axis='x'))
        lo_r, hi_r = (r['a'], r['b']) if r['a']['v'] <= r['b']['v'] else (r['b'], r['a'])
        a.text(min(xa, xb) - 11, cy + 5, pct(lo_r['v']), 'x13b', 'end', da(lo_r['key'], lo_r['v'], mark='label'))
        a.text(max(xa, xb) + 11, cy + 5, pct(hi_r['v']), 'x13b', attrs=da(hi_r['key'], hi_r['v'], mark='label'))
        if first:
            ky = cy - 20
            (xl, wl), (xr, wr) = sorted([(xa, s['years'][0]), (xb, s['years'][1])])
            a.text(xl + 5, ky, wl, 'x13', 'end')
            a.text(xr - 5, ky, wr, 'x13')
            first = False
        y = cy + (26 if side else 22)
    a.H = y + 2


def small_multiples(a, s):
    """One panel per group on one shared scale; the panel's group in the dark line, the other groups in gray. Notes
    sit in the empty band under the lines, on a band in the ground color."""
    W = a.W
    cols = 4 if W >= CT['breaks']['four_panels'] else (2 if W >= CT['breaks']['two_panels'] else 1)
    gap, gut, endw = 20, 46, 60
    pw = (W - gut - gap * (cols - 1)) / cols
    lo, hi = s['y_range']
    x_lo, x_hi = s['x_range']
    ph = 220 if cols == 4 else 190
    head = 30
    H = 0
    for i, p in enumerate(s['panels']):
        c, rr = i % cols, i // cols
        ox = gut + c * (pw + gap)
        top = rr * (head + ph + 44) + head
        X = lambda yr, ox=ox: ox + 2 + (yr - x_lo) * (pw - endw - 4) / (x_hi - x_lo)
        Y = lambda v, top=top: top + (hi - v) * ph / (hi - lo)
        a.text(ox, top - 14, p['name'], 'x15b')
        for v in range(lo, hi + 1, 10):
            a.line(ox, Y(v), ox + pw, Y(v), 'grid', 'grid')
            if c == 0:
                a.text(ox - 8, Y(v) + 4.5, f'{v}%' if v == hi else str(v), 'x13', 'end')
        a.text(X(x_lo), Y(lo) + 18, str(x_lo), 'x13')
        a.text(X(x_hi), Y(lo) + 18, str(x_hi), 'x13', 'end')
        for q in s['panels']:
            if q is not p:
                for seg in q['segments']:
                    if len(seg) > 1:
                        a.poly([(X(r['x']), Y(r['v'])) for r in seg], 'l-ctx', 'series')
        for seg in p['segments']:
            if len(seg) > 1:
                a.poly([(X(r['x']), Y(r['v'])) for r in seg], 'l-ink', 'series')
            for r in seg:
                big = r.get('end')
                a.raw(f'<circle cx="{fmt(X(r["x"]))}" cy="{fmt(Y(r["v"]))}" r="{2.5 if big else 1.5}" class="f-ink"'
                      f'{da(r["key"], r["v"], mark="point", axis="y", scale="panel-" + p["id"])}/>')
        last = p['last']
        a.text(X(last['x']) + 6, Y(last['v']) + 4, f'{pct(last["v"])}%', 'x13b', attrs=da(last['key'], last['v'], mark='label'), knock=True)
        if p.get('note'):
            rows_ = wrap_even(p['note'], (pw - 12) / CT['label_headroom'], 13, p.get('note_weight', 400))
            a.text(ox + 2, Y(s['note_at']), '', 'x13b' if p.get('note_weight') == 600 else 'x13', rows=rows_, lh=16, knock=True)
        H = max(H, top + ph + 26)
    a.H = H


def tile_map(a, s):
    """Equal tiles on the studio grid, one per state, coded by status with a fill step that holds in grayscale; each
    tile prints its code and, where room allows, the year of its law."""
    W = a.W
    pitch = CT['tile_pitch'].get(int(W), 27 if W < 460 else 44)
    gap = 4 if pitch >= 44 else 2
    t = pitch - gap
    cols = max(c['col'] for c in GRID) + 1
    rows_n = max(c['row'] for c in GRID) + 1
    beside = W >= CT['breaks']['map_notes_beside']
    years = W >= CT['breaks']['map_years']
    items = [((lambda f: (lambda x, yy: a.rect(x, yy, 14, 14, f)))(f), words) for f, words in s['key']]
    if beside:
        kx, ky = pitch + 4, 20
        for draw, words in items:
            draw(kx, ky - 11)
            a.text(kx + 22, ky, words, 'xkey')
            ky += 24
        rows_ = wrap_even(s['size_note'], (5 * pitch - 24) / CT['label_headroom'], 13)
        a.text(kx, ky - 2, '', 'x13', rows=rows_, lh=16)
        gy = 0
    else:
        yy = key_row(a, items, 14)
        a.text(0, yy + 14, s['size_note'], 'x13')
        gy = yy + 32
    for tl in s['tiles']:
        x, y = tl['col'] * pitch, gy + tl['row'] * pitch
        host = a.rect(x, y, t, t, tl['fill'], da(tl['key'], field='status', cat=tl['status'], mark='cell', tip=tl['tip']))
        if years:
            a.text(x + t / 2, y + (22 if pitch >= 56 else 18), tl['key'], tl['txt'], 'middle', inside=host)
            if tl.get('year'):
                a.text(x + t / 2, y + (40 if pitch >= 56 else 34), str(tl['year']), tl['txt'], 'middle', ' style="font-weight:400"', inside=host, record=False)
        else:
            a.text(x + t / 2, y + t / 2 + 4.5, tl['key'], tl['txt'], 'middle', inside=host)
    a.H = gy + rows_n * pitch - gap + 4
    del cols


def strip_timeline(a, s):
    """Lanes on one true time scale. Each dot sits at its exact date and flies its year; flags tier so no leader runs
    through a label. The events' names and what each did sit in the register under the drawing."""
    W = a.W
    lw = 128 if W >= CT['breaks']['side_labels'] else 0
    px0, px1 = lw + 10, W - 10
    x_lo, x_hi = s['x_range']
    X = lambda v: px0 + (v - x_lo) * (px1 - px0) / (x_hi - x_lo)
    y = 0
    for li, lane in enumerate(s['lanes']):
        if lw:
            top = y
        else:
            a.text(0, y + 16, lane['label'], 'x15b')
            top = y + 24
        flags = [{'x': X(e['x']), 'w': tw(str(e['year']), 13) * CT['label_headroom'] + 6, 'e': e} for e in lane['events']]
        place_flags(flags, W, gap=6)
        tiers = max(f_['t'] for f_ in flags) + 1
        line_y = top + tiers * 17 + 14
        if lw:
            a.text(0, line_y + 5, lane['label'], 'x15b')
        a.line(px0 - 6, line_y, px1 + 6, line_y, 'lane', 'lane')
        for f_ in flags:
            e = f_['e']
            ty = line_y - 15 - f_['t'] * 17
            a.line(f_['x'], line_y - 6, f_['x'], ty - 10, 'lead', 'lead')
            a.text(f_['x'] + 4 if f_['anchor'] == 'start' else f_['x'] - 4, ty, str(e['year']), 'x13', f_['anchor'], record=False)
            a.circle(f_['x'], line_y, CT['dot']['timeline'] if lw else 4.5, 'f-ink',
                     da(e['key'], round(e['x'], 4), field='date', mark='point', axis='x', tip=e['tip']))
        y = line_y + 22
    for i, yr in enumerate(s['ticks']):
        anchor = 'start' if i == 0 else ('end' if i == len(s['ticks']) - 1 else 'middle')
        a.text(X(yr) - (4 if anchor == 'start' else 0) + (4 if anchor == 'end' else 0), y + 4, str(yr), 'x13', anchor, record=False)
    a.H = y + 12


def share_bars(a, s):
    """A 100 percent bar per row in the graded fill code, sorted by the share the title names, with that share and
    the row's base printed at the right."""
    W = a.W
    a.defs = grade_defs(ART_ID)
    side = W >= CT['breaks']['side_labels']
    y = 14
    x = 0
    for gk, word, gloss, line_style, _ in [gr for gr in GRADES if gr[0] in s['grades']]:
        words = f'{word}: {gloss}'
        w = 24 + 6 + tw(words, 13) * CT['label_headroom'] + 20
        if x and x + w > W:
            x, y = 0, y + 22
        a.raw(grade_markup(ART_ID, gk, x, y - 11, 24, 14, ' aria-hidden="true"'))
        a.rects.append({'box': (x, y - 11, x + 24, y + 3), 'block': True})
        a.text(x + 30, y, words, 'xkey')
        x += w
    y += 30
    rw = max(tw(f'{r["share"]:.0f}% of {r["total"]} {s["unit"]}' if i == 0 else f'{r["share"]:.0f}% of {r["total"]}', 15, 700)
             for i, r in enumerate(s['rows'])) * CT['label_headroom'] + 14
    nmw = (max(tw(r['label'], 15) for r in s['rows']) * CT['label_headroom'] + 16) if side else 0
    bx0 = nmw
    bw = W - bx0 - rw
    a.text(bx0, y, '0', 'x13')
    a.text(bx0 + bw, y, '100%', 'x13', 'end')
    a.text(W, y, s['right_head'], 'x13', 'end')
    y += 12
    bh = CT['share_bar']['h']
    for i, r in enumerate(s['rows']):
        if side:
            by = y
            a.text(0, by + 14, r['label'], 'x15')
        else:
            a.text(0, y + 14, r['label'], 'x15')
            by = y + 22
        x = bx0
        k = bw / r['total']
        edges = []
        for gk, v in r['segs']:
            if not v:
                continue
            a.raw(grade_markup(ART_ID, gk, x, by, v * k, bh, da(r['key'], v, field=gk, mark='bar', axis='x', scale=r['key'])))
            a.rects.append({'box': (x, by, x + v * k, by + bh), 'block': True})
            edges.append(x + v * k)
            x += v * k
        for ex in edges[:-1]:
            a.raw(LN(ex, by - 1, ex, by + bh + 1, 'sep', ' aria-hidden="true"'))
        right = f'{r["share"]:.0f}% of {r["total"]} {s["unit"]}' if i == 0 else f'{r["share"]:.0f}% of {r["total"]}'
        a.text(W, by + 14, right, 'x15k', 'end', da(r['key'], r[s['share_field']], field=s['share_field'], mark='label'))
        y = by + bh + (CT['share_bar']['pitch'] - bh if side else 16)
    a.H = y + 4


# ------------------------------------------------------------------------------------------------ HTML forms
def boxed_arrow(c, size=20):
    """Scenario glyphs: an arrow in a box, so the direction survives a black-and-white copy on its own."""
    shapes = {
        'up': '<path d="M8.6 16V8H5L10 2.5L15 8H11.4V16Z" class="gf-up"/>',
        'slightly up': '<path d="M5.2 15.6L12.2 8.6" class="gs-up"/><path d="M9 6H15V12Z" class="gf-up"/>',
        'flat': '<path d="M3.5 10H12.5" class="gs-flat"/><path d="M11.5 6L16.5 10L11.5 14Z" class="gf-flat"/>',
        'flat or down': '<path d="M5.2 4.4L12.2 11.4" class="gs-down"/><path d="M9 14H15V8Z" class="gf-down"/>',
        'down': '<path d="M8.6 4V12H5L10 17.5L15 12H11.4V4Z" class="gf-down"/>',
        'mixed': '<path d="M10 6V14" class="gs-mix"/><path d="M6 7L10 2.6L14 7Z M6 13L10 17.4L14 13Z" class="gf-mix"/>',
        'same as ii': '<path d="M5 7H15V9H5Z M5 11H15V13H5Z" class="gf-flat"/>',
    }
    return (f'<svg class="gl" viewBox="0 0 20 20" width="{size}" height="{size}" aria-hidden="true" focusable="false">'
            f'<rect x="0.5" y="0.5" width="19" height="19" class="gbox"/>{shapes[c]}</svg>')


CLASS_CSS = {'up': 'c-up', 'slightly up': 'c-sup', 'flat': 'c-flat', 'flat or down': 'c-fod', 'down': 'c-down', 'mixed': 'c-mix', 'same as ii': 'c-same'}
CLASS_WORD = {'up': 'Up', 'slightly up': 'Slightly up', 'flat': 'Flat', 'flat or down': 'Flat or down', 'down': 'Down',
              'mixed': 'Mixed', 'same as ii': 'Same as scenario ii'}


def comparison_table(uid, s, hl=2):
    key = ''.join(f'<li>{boxed_arrow(c)}<span>{tx(CLASS_WORD[c])}</span></li>' for c in CLASS_WORD)
    head = ''.join(f'<th scope="col">{tx(n)}</th>' for _, n in s['families'])
    body = []
    for r in s['rows']:
        cells = []
        for f, fname in s['families']:
            c = r[f + '_class']
            cells.append(f'<td class="{CLASS_CSS[c]}"{da(r["key"], field=f, cat=r[f], mark="cell")}>'
                         f'<span class="fam-l">{tx(fname)}</span><span class="cw">{boxed_arrow(c)}'
                         f'<span><span class="vh">Oath &amp; Action’s reading: {tx(CLASS_WORD[c].lower())}. The atlas: </span>{tx(r[f])}</span></span></td>')
        body.append(f'<tr><th scope="row"><span class="sid">{tx(r["key"])}</span><span class="snm"><span class="sname">{tx(r["name"])}</span>'
                    f'<span class="sgl">{tx(r["gloss"])}</span></span></th>{"".join(cells)}</tr>')
    return (f'<div class="sg"><p class="sg-kh">{tx(s["key_head"])}</p><ul class="sg-key">{key}</ul>'
            f'<table class="sgt"><caption class="vh">{tx(s["caption"])}</caption>'
            f'<thead><tr><th scope="col">Scenario</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def unit_svg(r, code, roll=None, key=False):
    """One record, one square. A roll-up record keeps one square's footprint, so rows still compare by length, and
    prints its count inside."""
    u = CT['unit']['size']
    attrs = '' if key else da(r['key'], cat=r['direction'], mark='unit', tip=roll['tip'] if roll else r['tip'])
    mark = dir_markup(0.75, 0.75, u - 1.5, u - 1.5, code, attrs)
    if roll:
        mark += (f'<text x="{fmt(u / 2)}" y="{fmt(u / 2 + 4)}" class="{ONTXT[code]}" text-anchor="middle">{svg_tx(str(roll["count"]))}</text>')
    return (f'<svg class="u{" roll" if roll else ""}" viewBox="0 0 {u} {u}" width="{u}" height="{u}" aria-hidden="true" focusable="false">'
            f'{mark}</svg>')


def unit_ledger(uid, s):
    """One mark per record in a row per category, in date order. HTML, so every record is drawn once. Each row's
    label sits above its marks, so at full width every row runs on one line at the same pitch and rows compare like bars.
    A key under the rows names each roll-up mark."""
    out = [f'<div class="ul" role="img" aria-label="{at(s["label"])}">']
    keys = []
    for code, word, recs in s['rows']:
        units = ''.join(unit_svg(r, code, s['rollups'].get(r['key'])) for r in recs)
        keys += [unit_svg(r, code, s['rollups'][r['key']], key=True) + f'<span><strong>{tx(s["rollups"][r["key"]]["label"])}:</strong> '
                 f'{tx(s["rollups"][r["key"]]["key"])}</span>' for r in recs if r['key'] in s['rollups']]
        out.append(f'<div class="ul-row"><p class="ul-w"><span class="ul-dw">{tx(word)}</span> <span class="ul-dn">{len(recs)}</span></p>'
                   f'<div class="ul-us">{units or "<span class=ul-none>none</span>"}</div></div>')
    out.append('</div>')
    out += [f'<p class="ul-k">{k}</p>' for k in keys]
    return ''.join(out)


def event_register(s, hl=3):
    """The events behind the timeline, by lane: year, lead name and what each did, in date order."""
    cols = []
    for lane in s['lanes']:
        items = ''.join(f'<li><span class="er-y">{tx(e["date_words"])}</span><span class="er-n">{tx(e["name"])}</span>'
                        f'<span class="er-d">{tx(e["did"])}</span></li>' for e in lane['events'])
        cols.append(f'<section class="er-c"><h{hl} class="er-h">{tx(lane["label"])}</h{hl}><p class="er-q">{tx(lane["question"])}</p><ol class="er-l">{items}</ol></section>')
    return f'<div class="ereg">{"".join(cols)}</div>'


# ------------------------------------------------------------------------------------------------ copy shared by the repair-log charts (F1)
RLD = DS['rule-changes']
DISCLOSURE = DS['rule-changes']['required_text'][0]
RL_ROWS = sorted(RLD['rows'], key=lambda r: (r['date'], r['key']))
RL_N = len(RL_ROWS)
RL_RECENT = sum(1 for r in RL_ROWS if r['year'] >= 2025)
RCV = rowmap('rcv-bans')
RCV_BANS = [r for r in RCV.values() if r['prohibits_rcv']]
RCV_EARLY = sorted(r['code'] for r in RCV_BANS if r['enacted_date'] < '2025-01-01')
RCV_OWN = [r['jurisdiction'] for r in RL_ROWS   # states whose ban also has a log entry of its own, in date order
           if r['key'] != 'RL47' and r['direction'] == 'away from voters' and 'ranked-choice' in r['rule']
           and 'ban' in r['rule'].lower() and r['jurisdiction'] in {b['name'] for b in RCV_BANS}]
RCV_EARLY_ALONE = [c for c in RCV_EARLY if RCV[c]['name'] not in RCV_OWN]


def reader_words(note):
    """The coding note with its two record IDs put in reader words (the creative director's fix before Board 3)."""
    old = 'the reform profiles R-01 and R-02'
    assert old in note, 'the shared coding note changed; check the reader-words fix'
    return note.replace(old, "the atlas's profiles of those two reforms")


def log_notes(extra_first=()):
    n38, n41 = rowmap('rule-changes')['RL38'], rowmap('rule-changes')['RL41']
    assert n38['direction'] == n41['direction'] == 'away from voters'
    return list(extra_first) + [
        f'The log holds the {RL_N} changes the atlas chose to record, not every rule change in the country. It records more of recent years: {RL_RECENT} of the {RL_N} entries fall in 2025 and 2026.',
        ('How the atlas codes direction, in its own words:', reader_words(RLD['coding_note'])),
        "A map redrawn in the middle of a decade counts as away from voters whichever party draws it: Texas's HB 4 (August 2025) and California's Proposition 50 (November 2025) both count as away.",
        f"One entry stands for all {len(RCV_BANS)} state bans on ranked-choice voting; {' and '.join(n + chr(39) + 's' for n in RCV_OWN)} bans also have entries of their own.",
    ]


# ------------------------------------------------------------------------------------------------ the specimens: adapters read the shared data
def spec_s01():
    rm = rowmap('stock-trading-ban')
    d, r_, al = rm['support-democrats']['value'], rm['support-republicans']['value'], rm['support-all']['value']
    sy, sn, need = rm['senate-yes']['value'], rm['senate-no']['value'], rm['senate-needed']['value']
    hy, hn = rm['house-yes']['value'], rm['house-no']['value']
    groups = sorted([{'key': 'support-democrats', 'label': 'Democrats', 'value': d, 'party': 'Democrats'},
                     {'key': 'support-republicans', 'label': 'Republicans', 'value': r_, 'party': 'Republicans'}],
                    key=lambda x: (-x['value'], x['label'])) + [{'key': 'support-all', 'label': 'All registered voters', 'value': al, 'context': True}]
    return {
        'kind_words': 'Documented: a published survey and two recorded votes',
        'title': f'In 2023, {d}% of Democrats and {r_}% of Republicans favored a ban on stock trading by members of Congress; in 2026 the Senate fell {need - sy} votes short of taking one up.',
        'measure': ['Registered voters who favored banning stock trading by members of Congress, percent, United States, survey of May 2023; House and Senate votes on H.R. 7008, July and September 2026'],
        'index': '',
        'figure': {'key': 'support-all', 'value': al, 'caption': 'of registered voters favored a ban', 'sub': 'Survey, May 2023'},
        'group_head': 'Favored a ban, by group',
        'groups': groups,
        'vote_head': 'What Congress did in 2026',
        'votes': [
            {'label': 'House: passed a ban, H.R. 7008, July 22, 2026', 'scale': 'house',
             'segs': [{'key': 'house-yes', 'value': hy, 'word': 'for', 'code': 'away'}, {'key': 'house-no', 'value': hn, 'word': 'against', 'code': 'kept'}]},
            {'label': 'Senate: vote to take up the bill, September 30, 2026', 'scale': 'senate',
             'sub': f'Taking up the bill needed {need} votes, three-fifths of the Senate, to end debate (cloture).',
             'segs': [{'key': 'senate-yes', 'value': sy, 'word': 'for', 'code': 'away'}, {'key': 'senate-no', 'value': sn, 'word': 'against', 'code': 'kept'}],
             'threshold': {'key': 'senate-needed', 'value': need},
             'red': {'from': sy, 'words': f'{need - sy} votes short of the {need} needed'}}],
        'notes': [f"Each chamber's bar holds every vote cast there: {hy + hn} in the House and {sy + sn} in the Senate.",
                  f"The {al}% for all registered voters comes from the survey's own release. The survey came three years before H.R. 7008 reached either chamber."],
        'drawn': ['of registered voters favored a ban', 'Survey, May 2023', 'Favored a ban, by group', 'What Congress did in 2026',
                  'House: passed a ban, H.R. 7008, July 22, 2026', 'Senate: vote to take up the bill, September 30, 2026',
                  f'Taking up the bill needed {need} votes, three-fifths of the Senate, to end debate (cloture).',
                  f'{hy} for, {hn} against', f'{sy} for, {sn} against', f'{need - sy} votes short of the {need} needed',
                  'Democrats', 'Republicans', 'All registered voters'],
        'label': (f'Chart. {al}% of registered voters favored a ban in May 2023: {d}% of Democrats and {r_}% of Republicans. '
                  f'The House passed a ban, H.R. 7008, by {hy} to {hn} on July 22, 2026. On September 30, 2026 the Senate vote to take it up '
                  f'got {sy} of the {need} votes needed to end debate, {need - sy} short.'),
        'why': 'A big number answers yes at a glance; the party bars beside it show the two figures one point apart, and the votes show what Congress did three years later.',
    }


def poverty_segments(measure):
    rows = [r for r in rows_of('child-poverty-spm') if r['measure'] == measure]
    segs, cur = [], []
    for y in sorted({r['year'] for r in rows}):
        ry = [r for r in rows if r['year'] == y]
        if len(ry) == 1:
            cur.append(ry[0])
        else:
            cur.append(next(r for r in ry if r['comparable_with'] == 'earlier'))
            segs.append(cur)
            cur = [next(r for r in ry if r['comparable_with'] == 'later')]
    segs.append(cur)
    return segs


def spec_s02():
    rm = rowmap('child-poverty-spm')
    spm = [r for r in rows_of('child-poverty-spm') if r['measure'] == 'spm']
    low = min(spm, key=lambda r: r['percent'])
    v21, v22 = rm['spm|2021|standard']['percent'], rm['spm|2022|standard']['percent']
    assert low['year'] == 2021 and v22 > 2 * v21
    first_year = min(r['year'] for r in spm)
    rl = rowmap('rule-changes')
    rl15, rl16, rl35 = rl['RL15'], rl['RL16'], rl['RL35']
    breaks = sorted({r['year'] for r in spm if r['comparable_with'] != 'both'})
    words = {2013: 'Survey change', 2017: 'Processing change', 2019: 'Method change'}

    def pts(measure):
        out = []
        for seg in poverty_segments(measure):
            out.append([{'x': r['year'], 'v': r['percent'], 'key': r['key'],
                         'big': measure == 'spm' and (r['year'] in (2021, 2025) or r['comparable_with'] != 'both'),
                         'tip': f'{"Supplemental measure" if measure == "spm" else "Official measure"}, {r["year"]}: {pct(r["percent"])}%'} for r in seg])
        return out
    v25 = rm['spm|2025|standard']['percent']
    o25 = rm['official|2025|standard']['percent']
    end_both = v25 == o25
    note21 = (f'2021: {pct(v21)}%. The expanded child tax credit paid half in monthly installments for 2021 only, and expired after it. '
              'The timing alone does not show how much of the drop came from the credit.')
    note25 = f'July 2025: P.L. 119-21 set the child tax credit at up to $2,200 per child.'
    assert '2,200' in rl35['rule'] and 'monthly installments for 2021 only' in rl15['rule'] and rl16['direction']
    return {
        'kind_words': 'Official statistic: a Census Bureau survey',
        'title': f'Child poverty fell to {pct(v21)}% in 2021, the lowest since the series began in {first_year}, and more than doubled the next year.',
        'measure': ['Children under 18 below the poverty line, percent, United States, 2009 to 2025. The dark line is the Supplemental Poverty Measure, which counts tax credits and other aid; the gray line is the official measure, which counts pretax cash income only'],
        'index': 'Atlas records RL15, RL16, RL35',
        'x_range': (min(r['year'] for r in spm), max(r['year'] for r in spm)), 'x_ticks': [2009, 2013, 2017, 2021, 2025],
        'y_max': 25, 'y_step': 5, 'plot_h': (260, 210), 'right_margin': 108,
        'breaks': [{'x': y, 'word': words[y], 'top': max(r['percent'] for r in rows_of('child-poverty-spm') if r['year'] == y and r['comparable_with'] != 'both')} for y in breaks],
        'series': [{'segments': pts('official'), 'line': 'l-ctx2', 'fill': 'f-ctx', 'dot': 1.5, 'dot_big': 3},
                   {'segments': pts('spm'), 'line': 'l-ink', 'fill': 'f-ink', 'dot': 1.5, 'dot_big': 4}],
        'labels': {
            'wide': [{'x': 2009, 'v': 23.4, 'text': 'Official measure', 'cls': 'x15b', 'attrs': ' style="fill:var(--sec)"'},
                     {'x': 2009, 'v': 14.2, 'text': 'Supplemental Poverty Measure', 'cls': 'x15b'},
                     {'x': 2025.35, 'v': 13.4 + 0.25, 'text': f'{pct(v25)}%' if end_both else '', 'cls': 'x13b'},
                     {'x': 2025.35, 'v': 13.4 - 1.35, 'text': 'on both' if end_both else '', 'cls': 'x13'}],
            'other': [{'x': 2009, 'v': 23.2, 'text': 'Official', 'cls': 'x13s'},
                      {'x': 2009, 'v': 13.9, 'text': 'Supplemental', 'cls': 'x13b'}]},
        'plot_notes': [{'x': 2021, 'v': v21, 'text': note21, 'right': 2020, 'top': 8.0, 'chars': 46},
                  {'x': 2025, 'v': v25, 'text': note25, 'text_other': note25 + (f' Both measures read {pct(v25)}% in 2025.' if end_both else ''),
                   'edge': True, 'top': 9.4, 'chars': 26}],
        'html_notes': ['The Census Bureau describes the change between two years and credits no single policy with it.',
                       "Figures for 2019 to 2024 include the Bureau's August 2026 revision. The atlas prints the first-published 9.7%, 5.2% and 13.4% for 2020, 2021 and 2024; this table reads 9.6%, 5.1% and 13.5%.",
                       'In 2013, 2017 and 2019 the Bureau gives two estimates, one that joins the earlier years and one that joins the later years, so the lines break there.'],
        'drawn': ['Official measure', 'Supplemental Poverty Measure', 'on both', note21, note25 + ' Both measures read 13.4% in 2025.'] + list(words.values()),
        'label': (f'Line chart of child poverty, 2009 to 2025. Under the Supplemental Poverty Measure the rate was 17.0% in 2009, fell to '
                  f'{pct(v21)}% in 2021 and stood at {pct(v22)}% in 2022 and {pct(v25)}% in 2025. The official measure ran from 20.7% to {pct(o25)}%. '
                  'The lines break in 2013, 2017 and 2019, when the Census Bureau changed its survey, processing or method.'),
        'why': 'A line shows the fall to 2021 and the climb back; the official measure in gray shows what the supplemental measure counts, and the breaks show where the Census Bureau changed its method.',
    }


def spec_s03():
    rows = rows_of('rule-changes-by-instrument')
    rm = {r['key']: r for r in rows}
    ss, bi, rf = rm['State statute'], rm['Ballot initiative'], rm['Referendum']
    passed = bi['toward voters'] + bi['away from voters'] + bi['mixed']
    shares = {r['key']: r['away from voters'] / r['value'] for r in rows}
    assert max(shares, key=shares.get) == 'State statute'
    rl47_away = rowmap('rule-changes')['RL47']['direction'] == 'away from voters'
    out_rows = []
    for r in rows:
        note = None
        if r['key'] == 'State statute':
            note = f'{r["away from voters"]} of {r["value"]} away from voters'
        sub = None
        if r['key'] == 'Ballot initiative':
            sub = f'{passed} passed, all toward voters'
        out_rows.append({'key': r['key'], 'label': r['key'], 'total': r['value'], 'note': note, 'sub': sub,
                         'segs': [{'field': d, 'value': r[d], 'code': c} for d, c, _ in DIRS]})
    return {
        'kind_words': "Documented: the atlas's dated log, coded by the atlas",
        'title': f'The atlas codes {ss["away from voters"]} of {ss["value"]} logged state statutes as moving the rules away from voters, the largest share of any instrument.',
        'measure': [f"Rule changes in Oath & Action's own atlas log of {RL_N}, by how each was made and by the log's direction code, United States, August 1965 to the November 3, 2026 ballot"],
        'index': 'Repair log RL01 to RL64',
        'key': [(c, w) for _, c, w in DIRS], 'unit': 'changes', 'rows': out_rows,
        'notes': [f'Citizen ballot initiatives: {bi["value"]} entries. {passed} passed, and all {bi["toward voters"]} moved the rules toward voters; '
                  f'{bi["voters kept existing rules"]} failed and left the rules in force; {bi["pending"]} are pending. Referendums are ballot measures too, and {rf["away from voters"]} of {rf["value"]} moved the rules away from voters.',
                  f'State statutes: {ss["away from voters"]} of {ss["value"]} moved the rules away from voters as logged, '
                  f'and {ss["away from voters"] - (1 if rl47_away else 0)} of {ss["value"] - 1} without the single entry that stands for all {len(RCV_BANS)} state bans on ranked-choice voting.',
                  'Oath & Action grouped five instruments with one change each: an agency rule, an executive action and an executive order as executive or agency action; a city ordinance and a council funding vote as local law or funding vote. The instruments are the atlas\'s.'] + log_notes(),
        'drawn': [w for _, _, w in DIRS] + [r['key'] for r in rows] + ['changes', f'{passed} passed, all toward voters', f'{ss["away from voters"]} of {ss["value"]} away from voters'],
        'label': ('Ranked bar chart of the 64 rule changes by how they were made. ' +
                  '; '.join(f'{r["key"]}: {r["value"]}, of them {r["away from voters"]} away from voters and {r["toward voters"]} toward' for r in rows) + '.'),
        'why': "Seven instruments ranked by count answer who made the most changes; splitting each bar by the atlas's direction code shows which way each instrument moved the rules.",
    }


AGES = [('18_to_24', '18 to 24'), ('25_to_44', '25 to 44'), ('45_to_64', '45 to 64'), ('65_and_over', '65 and over'), ('all', 'All citizens 18 and over')]


def turnout(age, year):
    return rowmap('turnout-by-age')[f'{age}|{year}|citizen_voting_age_population']


def change_words(a, b, first):
    d = round(b - a, 1)
    unit = ' points' if first else ''
    if abs(d) <= 2.0:
        return f'Little changed, {pct(d) if d < 0 else "+" + pct(d)}'
    return f'Down {abs(d):.1f}{unit}' if d < 0 else f'Up {d:.1f}{unit}'


def spec_s04():
    rows = []
    first = True
    for age, name in AGES:
        a_, b_ = turnout(age, 2020), turnout(age, 2024)
        rows.append({'label': name, 'context': age == 'all', 'change': change_words(a_['voted_pct'], b_['voted_pct'], first),
                     'a': {'key': a_['key'], 'v': a_['voted_pct']}, 'b': {'key': b_['key'], 'v': b_['voted_pct']}})
        first = False
    lo_, hi_ = turnout('18_to_24', 2024)['voted_pct'], turnout('65_and_over', 2024)['voted_pct']
    return {
        'kind_words': 'Official statistic: what survey respondents reported',
        'title': f'Reported turnout in 2024 ran from {pct(lo_)}% of citizens 18 to 24 to {pct(hi_)}% of those 65 and over.',
        'measure': ['Citizens who reported voting in the November presidential election, percent, by age, United States, 2020 and 2024; the scale runs from 40 to 80 percent'],
        'index': '', 'rows': rows, 'years': ('2020', '2024'),
        'notes': ["These are the shares of citizens who told the Census Bureau's November survey that they voted. Reported voting runs higher than counted ballots.",
                  'Table A-1 publishes no margins of error, so a change of a point or two may sit within survey error. Changes of 2 points or less print as little changed.',
                  'Where the two years nearly match, the open ring for 2020 sits over the dot for 2024.'],
        'drawn': [r['label'] for r in rows] + [r['change'] for r in rows] + ['2020', '2024'],
        'label': 'Dot chart of reported voting among citizens by age, 2020 and 2024. ' + '; '.join(f'{r["label"]}: {pct(r["a"]["v"])}% in 2020 and {pct(r["b"]["v"])}% in 2024' for r in rows) + '.',
        'why': 'Two dots per age group show the level and the change at once; printed values and the change in words carry the numbers without a grid.',
    }


HGROUPS = [('all_households', 'All households'), ('non_hispanic_white', 'Non-Hispanic White'), ('black', 'Black'), ('hispanic', 'Hispanic, of any race')]


def home_segments(group):
    """Three runs at most: 1994 to 2002 with 2002's original value; for All and Hispanic, the value revised to 2000
    Census controls starts the later run; for Black and non-Hispanic White, race categories change in 2003, so the
    revised 2002 value stands alone and the later run starts in 2003. No run is joined across a break."""
    rows = sorted([r for r in rows_of('homeownership-by-race') if r['group'] == group], key=lambda r: r['year'])
    early = [r for r in rows if r['year'] < 2002 or (r['year'] == 2002 and r['series_variant'] == 'original')]
    rev = [r for r in rows if r['year'] == 2002 and r['series_variant'] == 'revised_2000_census']
    late = [r for r in rows if r['year'] >= 2003]
    if group in ('black', 'non_hispanic_white'):
        return [early, rev, late]
    return [early, rev + late]


def spec_s05():
    rm = rowmap('homeownership-by-race')
    g = lambda grp, y: rm[next(k for k in rm if k.startswith(f'{grp}|{y}|') and (y != 2002))]['rate_pct']
    gap25, gap03 = g('non_hispanic_white', 2025) - g('black', 2025), g('non_hispanic_white', 2003) - g('black', 2003)
    hgap25, hgap03 = g('non_hispanic_white', 2025) - g('hispanic', 2025), g('non_hispanic_white', 2003) - g('hispanic', 2003)
    q = [r for r in rows_of('homeownership-by-race-quarterly') if r['year'] == 2026 and r['quarter'] == 3]
    qv = {r['group']: r['rate_pct'] for r in q}
    panels = []
    for grp, name in HGROUPS:
        segs = []
        for seg in home_segments(grp):
            segs.append([{'x': r['year'] + (0.0 if r['series_variant'] != 'revised_2000_census' else 0.0), 'v': r['rate_pct'], 'key': r['key'],
                          'end': r['year'] in (2002, 2003)} for r in seg])
        last = next(r for r in rows_of('homeownership-by-race') if r['group'] == grp and r['year'] == 2025)
        note, weight = None, 400
        if grp == 'all_households':
            note = 'Gray lines: the other three groups.'
        elif grp == 'non_hispanic_white':
            note = 'Breaks at 2002, when the Bureau reweighted, and 2003, when race categories changed.'
        elif grp == 'black':
            note, weight = f'{pct(gap25)} points below non-Hispanic White in 2025; {pct(gap03)} in 2003.', 600
        elif grp == 'hispanic':
            note, weight = f'{pct(hgap25)} points below non-Hispanic White in 2025; {pct(hgap03)} in 2003.', 600
        panels.append({'id': grp, 'name': name, 'segments': segs, 'last': {'x': 2025, 'v': last['rate_pct'], 'key': last['key']},
                       'note': note, 'note_weight': weight})
    return {
        'kind_words': 'Official statistic: a Census Bureau survey',
        'title': f'The homeownership gap between non-Hispanic White and Black households was {pct(gap25)} points in 2025, wider than the {pct(gap03)} points of 2003.',
        'measure': ['Owner households as a percent of all households in each group, by race and ethnicity of householder, United States, 1994 to 2025; one scale, starting at 20 percent'],
        'index': '', 'panels': panels, 'y_range': (20, 80), 'x_range': (1994, 2025), 'note_at': 37,
        'notes': ['The Census Bureau asks readers to use caution comparing 2020 with other years, after interviews moved to the phone.',
                  'Each line breaks where the table gives two values for 2002, before and after the Bureau reweighted to 2000 Census counts, and the Black and non-Hispanic White lines break again at 2003, when race categories changed. Both 2002 values are drawn.',
                  f'The 2025 average leaves out October 2025, when no data were collected. The latest quarter, the third quarter of 2026, reads {pct(qv["non_hispanic_white"])}% for non-Hispanic White and {pct(qv["black"])}% for Black householders: a single quarter\'s estimate, with a margin of error up to 0.9 points.'],
        'drawn': [n for _, n in HGROUPS] + [p['note'] for p in panels if p['note']],
        'label': ('Four line charts of the homeownership rate, 1994 to 2025, on one scale. In 2025: ' +
                  '; '.join(f'{p["name"]} {pct(p["last"]["v"])}%' for p in panels) +
                  f'. Non-Hispanic White householders led Black householders by {pct(gap25)} points in 2025 and {pct(gap03)} in 2003, and Hispanic householders by {pct(hgap25)} and {pct(hgap03)}.'),
        'why': 'One panel per group on one scale lets a reader compare each group with the other three, which sit behind it in gray.',
    }


FAMS = [('DQ', 'Quality of democracy'), ('GE', 'Government efficacy'), ('EP', 'Economic performance'), ('EQ', 'Income and wealth equality')]
GLOSS = {'i': 'Current law runs as written, and the Senate keeps the filibuster',
         'ii': 'Some states pass reforms; no federal rule changes',
         'iii': 'The Senate changes the filibuster and passes rules for elections and government',
         'iv-a': 'Fusion voting lets more than one party nominate the same candidate',
         'iv-b': 'Inspectors general are the watchdogs inside federal agencies',
         'iv-c': 'Stronger competition rules and faster labor-law remedies',
         'iv-d': 'Changes adopted by constitutional amendment',
         'iv-e': 'Officials hold back from using every power they have'}


def spec_s06():
    rows = []
    for r in rows_of('scenarios-2030'):
        rows.append(dict(r, gloss=GLOSS[r['key']]))
    beyond = [r for r in rows if r['key'] != 'i']
    lift = sum(1 for r in beyond if any(r[f + '_class'] in ('up', 'slightly up') for f, _ in FAMS))
    words = {5: 'five', 6: 'six', 7: 'seven', 4: 'four', 3: 'three'}
    return {
        'kind_words': 'Conditional directions: no forecast and no odds',
        'title': f'If their assumptions hold, {words.get(lift, lift)} of the {words.get(len(beyond), len(beyond))} scenarios beyond the baseline would lift at least one outcome family by 2036.',
        'measure': ["Direction each outcome family would take by 2036 if a scenario's assumptions hold, in the words of Oath & Action's atlas, United States, from a 2026 baseline",
                    'Up means better for each family; for income and wealth equality, more equal.'],
        'index': 'Scenarios i to iv-e', 'rows': rows, 'families': FAMS,
        'key_head': "Arrow and tint: Oath & Action's reading of the atlas's words, which print in every cell",
        'caption': "Direction each outcome family would take by 2036 in eight scenarios, in the atlas's words",
        'notes': ["Arrows and tints are Oath & Action's reading of the atlas's words, which print in every cell. The four families are read one at a time and never added together.",
                  'These are conditional directions with no forecast and no odds. The table lists the assumptions behind each scenario.'],
        'why': "A table keeps the atlas's words in every cell; a boxed arrow and a tint let a reader scan the moves across eight rows, and the arrow alone carries each move on a black-and-white copy.",
    }


STATUS = [('bans in all elections', 'f-away', 'xin', 'Bans it in all elections'), ('bans in some elections', 'f-some', 'xins', 'Bans it in some elections'),
          ('no ban', 'f-none', 'x13b', 'No state ban')]


def spec_s07():
    rows = RCV
    cnt = {s_: sum(1 for r in rows.values() if r['status'] == s_) for s_, *_ in STATUS}
    no_states = cnt['no ban'] - (1 if rows['DC']['status'] == 'no ban' else 0)
    words = {'bans in all elections': f'Bans it in all elections ({cnt["bans in all elections"]})',
             'bans in some elections': f'Bans it in some elections ({cnt["bans in some elections"]})',
             'no ban': f'No state ban ({no_states} states and DC)'}
    fills = {s_: (f, t) for s_, f, t, _ in STATUS}
    tiles = []
    for c in GRID:
        r = rows[c['code']]
        f, t = fills[r['status']]
        tip = (f'{r["name"]}: {r["status"]}, {date_words(r["enacted_date"])}. {r["scope_note"]}' if r['prohibits_rcv'] else f'{r["name"]}: no state ban')
        tiles.append({'col': c['col'], 'row': c['row'], 'key': r['key'], 'status': r['status'], 'fill': f, 'txt': t,
                      'year': r['enacted_year'] if r['prohibits_rcv'] else None, 'tip': tip})
    total_bans = cnt['bans in all elections'] + cnt['bans in some elections']
    return {
        'kind_words': "A secondary source: Ballotpedia's list, checked against the atlas",
        'title': f'As of November 2026, {total_bans} states ban ranked-choice voting, {cnt["bans in all elections"]} of them in all elections as Ballotpedia reads the laws.',
        'measure': ['State laws that prohibit ranked-choice voting, by scope and year enacted, 50 states and DC, as of November 2026'],
        'index': 'Atlas repair log RL47',
        'key': [(fills[s_][0], words[s_]) for s_, *_ in STATUS], 'tiles': tiles, 'size_note': 'Each square is one state, whatever its size.',
        'notes': ['Ranked-choice voting: voters rank candidates in order; if no one wins a majority of first choices, the last-place candidate drops out and those ballots count for their next choice, round by round.',
                  f'{no_states} states and DC have no state ban. A state with no ban may still keep its cities from adopting it, because many cities need the state\'s permission.',
                  'Ohio, 2026: home-rule cities may still adopt it, but they lose state local government fund money while it is in effect. Tennessee, 2022: county election commissions may not use it for state or local offices.',
                  f'Missouri wrote its ban into the state constitution in 2024; the other {total_bans - 1} are statutes. Ballotpedia reads 17 bans as covering all elections; Mississippi\'s quoted text does not name congressional district races.',
                  "Ballotpedia is a secondary source. The atlas cites the National Conference of State Legislatures, whose page could not be read by script; both list the same 19 states, as does the atlas's repair log."],
        'drawn': list(words.values()) + ['Each square is one state, whatever its size.'] + [t['key'] for t in tiles],
        'label': (f'Tile map of the 50 states and DC, one equal square each. {cnt["bans in all elections"]} states ban ranked-choice voting in all elections: ' +
                  ', '.join(r['name'] for r in rows.values() if r['status'] == 'bans in all elections') +
                  f'. Ohio and Tennessee ban it in some elections. {no_states} states and DC have no state ban.'),
        'why': 'Equal tiles give every state the same weight and room for its code and the year of its ban; true shapes would hide the small eastern states.',
    }


def spec_s08():
    tw_, aw_ = RLD['counts']['toward voters'], RLD['counts']['away from voters']
    rows = []
    for d, c, w in [DIRS[1], DIRS[0], DIRS[2], DIRS[3], DIRS[4]]:
        recs = []
        for r in RL_ROWS:
            if r['direction'] == d:
                recs.append(dict(r, tip=f'{r["key"]}, {date_words(r["date"])}, {r["jurisdiction"]}. {DIR_WORD[r["direction"]]}. {first_sentence(r["rule"])}'))
        rows.append((c, w, recs))
    r47 = rowmap('rule-changes')['RL47']
    rollups = {'RL47': {'label': f'{len(RCV_BANS)} states', 'count': len(RCV_BANS),
                        'key': f'the square marked {len(RCV_BANS)} is one entry that stands for every state ban on ranked-choice voting.',
                        'tip': f'RL47, {date_words(r47["date"])}: one entry for all {len(RCV_BANS)} state bans on ranked-choice voting. {first_sentence(r47["rule"])}'}}
    label = (f'Unit chart: one square per change in the repair log, in date order within each row. Toward voters {tw_}; away from voters {aw_}, '
             f'one of them a single entry for {len(RCV_BANS)} state bans; kept existing rules {RLD["counts"]["voters kept existing rules"]}; '
             f'mixed {RLD["counts"]["mixed"]}; pending {RLD["counts"]["pending"]}.')
    return {
        'kind_words': "Documented: the atlas's dated log, coded by the atlas",
        'title': f"The atlas's log codes {tw_} of its {RL_N} rule changes as moving toward voters and {aw_} as moving away.",
        'measure': [f"Each square is one dated change in Oath & Action's own atlas log of {RL_N}, in date order within each row, by the log's direction code, United States, August 1965 to the November 3, 2026 ballot"],
        'index': 'Repair log RL01 to RL64', 'rows': rows, 'rollups': rollups, 'label': label,
        'notes': log_notes() + [f'The atlas dates that entry {date_words(r47["date"])}, though {len(RCV_EARLY)} of its {len(RCV_BANS)} bans became law before 2025; '
                                f'{len(RCV_EARLY_ALONE)} of those {len(RCV_EARLY)} have no entry of their own.'],
        'why': 'One square per record lets a reader count every change; rows by direction show the whole log at once, with no period chosen for them.',
    }


def spec_s09():
    ds = DS['history-events']
    lanes = []
    for th in ds['threads']:
        evs = []
        for r in sorted([r for r in ds['rows'] if r['thread'] == th['id']], key=lambda r: r['date']):
            evs.append({'key': r['key'], 'x': frac_year(r['date']), 'year': r['year'], 'date_words': date_words(r['date']),
                        'name': r['title'].split(' (')[0], 'did': first_clause(r['mechanism']),
                        'tip': f'{date_words(r["date"])}. {r["title"]}. {r["mechanism"]}'})
        lanes.append({'label': th['label'], 'question': th['question'], 'events': evs})
    return {
        'kind_words': 'Documented: each event rests on a statute, ruling or official record',
        'title': 'The atlas traces 24 documented rule changes on four threads, from 1870 to 2026.',
        'measure': ["Dated changes in the history that Oath & Action's atlas traces, by thread, United States, February 3, 1870 to June 29, 2026; each dot sits at its date"],
        'index': 'Events E01 to E24, keys by Oath & Action',
        'lanes': lanes, 'x_range': (1868, 2028), 'ticks': [1870, 1900, 1930, 1960, 1990, 2026],
        'notes': ['Every event is documented: each rests on a statute, ruling, constitutional text or official record. The register under the drawing gives each event\'s lead name and the first part of what it did; the table gives the full entry, with the events the atlas pairs with it.'],
        'drawn': [th['label'] for th in ds['threads']],
        'label': ('Timeline of 24 documented rule changes on four threads, 1870 to 2026. ' +
                  '. '.join(f'{ln["label"]}: ' + ', '.join(f'{e["year"]} {e["name"]}' for e in ln['events']) for ln in lanes) + '.'),
        'why': 'Four lanes on one true time scale show when each thread changed; the register under the drawing names every event and what it did, in date order.',
    }


def spec_s10():
    rs = sorted(rows_of('claims-by-grade'), key=lambda r: (-r['documented'] / r['value'], r['key']))
    tot = DS['claims-by-grade']['totals']
    alln = sum(tot.values())
    top, bot = rs[0], rs[-1]
    rows = [{'key': r['key'], 'label': r['title'], 'total': r['value'], 'documented': r['documented'],
             'share': 100 * r['documented'] / r['value'], 'segs': [(g, r[g]) for g in ('documented', 'well-supported', 'plausible', 'contested')]} for r in rs]
    pick = max(rs, key=lambda r: (r['plausible'] + r['contested']) / r['value'])
    return {
        'kind_words': "Documented: the atlas's claims register, graded by the atlas",
        'title': (f"{tot['documented']} of the atlas's {alln} claims are documented on the public record, from "
                  f"{top['documented']} of {top['value']} on {top['title'].lower()} to {bot['documented']} of {bot['value']} on {bot['title'].lower()}."),
        'measure': ["Share of each everyday question's claims by evidence grade, percent of claims, with each question's count of claims; the claims register of Oath & Action's atlas, United States, checked through October 15, 2026"],
        'index': 'Questions PW01 to PW16',
        'grades': ['documented', 'well-supported', 'plausible', 'contested'], 'rows': rows, 'unit': 'claims',
        'share_field': 'documented', 'right_head': 'Documented',
        'notes': ["Here the {strongest} marks documented claims: the grade code replaces the rule that the {strongest} marks the title's subject.",
                  'Fills follow the atlas\'s evidence lines: documented and well supported are solid like its solid lines, plausible is a light tint where its line is dashed, and contested is hatched where its line is dash-dot. A claim\'s grade covers that claim alone.',
                  f'{pick["title"]}: {pick["plausible"] + pick["contested"]} of its {pick["value"]} claims are plausible or contested, the largest share of any question.'],
        'drawn': [f'{w}: {gl}' for _, w, gl, _, _ in GRADES[:4]] + [r['label'] for r in rows] + ['Documented', 'claims'],
        'label': (f'Stacked bars, one per everyday question, showing the share of its claims by evidence grade, sorted by the documented share. '
                  f'Across all {alln} claims: {tot["documented"]} documented, {tot["well-supported"]} well supported, {tot["plausible"]} plausible, '
                  f'{tot["contested"]} contested. ' + '; '.join(f'{r["label"]} {r["share"]:.0f}% documented of {r["total"]}' for r in rows) + '.'),
        'why': 'A 100% bar per question compares the mix across questions of different sizes; sorting by the documented share puts the firmest answers first, and the count beside each share shows its base.',
    }


# ------------------------------------------------------------------------------------------------ equivalents (tables) and CSV
def table(head, rows, caption='', num_cols=()):
    th = ''.join(f'<th scope="col">{tx(h)}</th>' for h in head)
    body = []
    for r in rows:
        cells = []
        for j, c in enumerate(r):
            if j == 0:
                cells.append(f'<th scope="row">{tx(c)}</th>')
            else:
                cls = ' class="n"' if j in num_cols else ''
                cells.append(f'<td{cls}><span class="tl">{tx(head[j])}</span>{tx(c)}</td>')
        body.append('<tr>' + ''.join(cells) + '</tr>')
    cap = f'<caption>{tx(caption)}</caption>' if caption else ''
    return f'<div class="tbl"><table class="eqt">{cap}<thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def eq_s01():
    return table(['Group', 'Measure', 'Value'], [[r['group'], r['measure'], r['value']] for r in rows_of('stock-trading-ban')], 'Survey shares and votes', (2,))


def eq_s02():
    rs = sorted(rows_of('child-poverty-spm'), key=lambda r: (r['year'], r['measure'], r['comparable_with'] != 'earlier'))
    out = [[r['year'], 'Supplemental' if r['measure'] == 'spm' else 'Official', pct(r['percent']),
            pct(r['moe_pct']) if r['moe_pct'] not in ('', None) else 'not given',
            {'both': '', 'earlier': 'joins earlier years', 'later': 'joins later years'}[r['comparable_with']]] for r in rs]
    return table(['Year', 'Measure', 'Percent of children', 'Margin of error, points', 'Break-year estimate'], out, 'Children under 18 in poverty', (2, 3))


def eq_s03():
    return table(['Instrument', 'All', 'Away from voters', 'Toward voters', 'Kept existing rules', 'Mixed', 'Pending'],
                 [[r['key'], r['value'], r['away from voters'], r['toward voters'], r['voters kept existing rules'], r['mixed'], r['pending']]
                  for r in rows_of('rule-changes-by-instrument')], 'Rule changes by instrument and direction', (1, 2, 3, 4, 5, 6))


def eq_s04():
    out = [[n, pct(turnout(a, 2020)['voted_pct']), pct(turnout(a, 2024)['voted_pct']), change_words(turnout(a, 2020)['voted_pct'], turnout(a, 2024)['voted_pct'], True)] for a, n in AGES]
    return table(['Age group', '2020', '2024', 'Change'], out, 'Reported voting among citizens, percent', (1, 2))


def eq_s05():
    years = sorted({r['year'] for r in rows_of('homeownership-by-race')})
    out = []
    for yr in years:
        for variant in (['original', 'revised_2000_census'] if yr == 2002 else [None]):
            row = [f'{yr}, {"original" if variant == "original" else "revised to 2000 Census counts"}' if variant else yr]
            for grp, _ in HGROUPS:
                m = [r for r in rows_of('homeownership-by-race') if r['group'] == grp and r['year'] == yr and (variant is None or r['series_variant'] == variant)]
                row.append(pct(m[0]['rate_pct']) if m else '')
            out.append(row)
    return table(['Year'] + [n for _, n in HGROUPS], out, 'Homeownership rate, percent. Black and non-Hispanic White rates before 2003 use the older race categories.', (1, 2, 3, 4))


def eq_s06():
    out = []
    for r in rows_of('scenarios-2030'):
        for f, n in FAMS:
            out.append([f'{r["key"]}. {r["name"]}', n, r[f], CLASS_WORD[r[f + '_class']], r[f + '_why'] or 'Same reasoning as scenario ii'])
    assum = [[f'{r["key"]}. {r["name"]}', '; '.join(r['assumptions'])] for r in rows_of('scenarios-2030')]
    return (table(['Scenario', 'Outcome family', "Direction, atlas's words", "Oath & Action's reading", "Why, atlas's words"], out, 'Eight scenarios, four outcome families') +
            table(['Scenario', "Assumptions, atlas's words"], assum, 'What each scenario assumes'))


def eq_s07():
    return table(['State', 'Status', 'Enacted', 'Law', 'Scope, as the source describes it'],
                 [[r['name'], r['status'], date_words(r['enacted_date']) if r['enacted_date'] else '', r['measure'] or '', r['scope_note'] or ''] for r in rows_of('rcv-bans')],
                 'State laws on ranked-choice voting, as of November 2026')


def eq_s08():
    return table(['Record', 'Date', 'Where', 'Direction', 'Instrument', 'What changed'],
                 [[r['key'] + ('' if r['verified'] else ' (source not checked by the atlas)'), date_words(r['date']), r['jurisdiction'],
                   DIR_WORD[r['direction']], r['instrument'], r['rule']] for r in RL_ROWS], f'The repair log, {RL_N} changes')


def eq_s09():
    th = {t['id']: t for t in DS['history-events']['threads']}
    return table(['Event', 'Date', 'Thread', 'What happened', 'Mechanism'],
                 [[r['key'], date_words(r['date']), f'{r["thread_label"]}: {th[r["thread"]]["question"]}', r['title'], r['mechanism']] for r in rows_of('history-events')],
                 '24 documented events')


def eq_s10():
    rs = sorted(rows_of('claims-by-grade'), key=lambda r: (-r['documented'] / r['value'], r['key']))
    return table(['Question', 'Documented', 'Well supported', 'Plausible', 'Contested', 'All claims', 'Documented share'],
                 [[f'{r["key"]} {r["title"]}: {r["question"]}', r['documented'], r['well-supported'], r['plausible'], r['contested'], r['value'],
                   f'{100 * r["documented"] / r["value"]:.0f}%'] for r in rs], 'Claims by evidence grade. Documented: on the public record; well supported: strong research evidence; plausible: some evidence; contested: evidence disputed.', (1, 2, 3, 4, 5, 6))


# ------------------------------------------------------------------------------------------------ the registry
CHARTS = {}


def register_chart(cid, dataset, gen=None, html_gen=None, adapter=None, table=None, csv_cols=None, csv_filter=None, readout=None, size_note=None):
    """Add a chart to the kit: one call, and the module, equivalents, downloads and page pick it up."""
    CHARTS[cid] = {'dataset': dataset, 'gen': gen, 'html': html_gen, 'adapter': adapter, 'table': table, 'csv_cols': csv_cols,
                   'csv_filter': csv_filter, 'readout': readout,
                   'size_note': size_note or 'Column module, 866 px; artboards 866, 560, 358 and 328 px'}


def csv_text(cid):
    c = CHARTS[cid]
    rs = rows_of(c['dataset'])
    if c['csv_filter']:
        rs = [r for r in rs if c['csv_filter'](r)]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(c['csv_cols'])
    for r in rs:
        w.writerow([r.get(k, '') for k in c['csv_cols']])
    return buf.getvalue()


_S04_KEYS = {turnout(a, y)['key'] for a, _ in AGES for y in (2020, 2024)}
register_chart('S01', 'stock-trading-ban', big_number, adapter=spec_s01, table=eq_s01, csv_cols=['key', 'group', 'measure', 'value'])
register_chart('S02', 'child-poverty-spm', line_events, adapter=spec_s02, table=eq_s02,
               csv_cols=['key', 'year', 'measure', 'series_variant', 'comparable_with', 'percent', 'moe_pct', 'source_table'])
register_chart('S03', 'rule-changes-by-instrument', ranked_bar, adapter=spec_s03, table=eq_s03,
               csv_cols=['key', 'value', 'away from voters', 'toward voters', 'voters kept existing rules', 'mixed', 'pending'])
register_chart('S04', 'turnout-by-age', dumbbell, adapter=spec_s04, table=eq_s04, csv_cols=['key', 'year', 'age_group', 'base', 'voted_pct'],
               csv_filter=lambda r: r['key'] in _S04_KEYS)
register_chart('S05', 'homeownership-by-race', small_multiples, adapter=spec_s05, table=eq_s05,
               csv_cols=['key', 'year', 'group', 'race_definition', 'series_variant', 'rate_pct', 'moe_pct'])
register_chart('S06', 'scenarios-2030', html_gen=comparison_table, adapter=spec_s06, table=eq_s06,
               csv_cols=['key', 'name', 'DQ', 'GE', 'EP', 'EQ', 'DQ_class', 'GE_class', 'EP_class', 'EQ_class'],
               size_note='Column module, 866 px; one HTML table that reflows under 640 px')
register_chart('S07', 'rcv-bans', tile_map, adapter=spec_s07, table=eq_s07,
               csv_cols=['key', 'name', 'status', 'scope', 'instrument', 'enacted_date', 'measure', 'scope_note'],
               readout='Tap or point at a state to read its law. The table lists every state.')
register_chart('S08', 'rule-changes', html_gen=unit_ledger, adapter=spec_s08, table=eq_s08,
               csv_cols=['key', 'date', 'jurisdiction', 'direction', 'instrument', 'instrument_group', 'rule', 'verified', 'source_url'],
               readout='Tap or point at a square to read its record. The table lists every change.',
               size_note='Column module, 866 px; one HTML grid of 24 px units that reflows')
register_chart('S09', 'history-events', strip_timeline, adapter=spec_s09, table=eq_s09,
               csv_cols=['key', 'date', 'thread_label', 'title', 'mechanism', 'source_text'],
               readout='Tap or point at a dot to read the event. The register below lists every event.')
register_chart('S10', 'claims-by-grade', share_bars, adapter=spec_s10, table=eq_s10,
               csv_cols=['key', 'title', 'documented', 'well-supported', 'plausible', 'contested', 'value'])
ORDER = list(CHARTS)
_SPEC_CACHE = {}


def spec(cid):
    if cid not in _SPEC_CACHE:
        _SPEC_CACHE[cid] = CHARTS[cid]['adapter']()
    return _SPEC_CACHE[cid]


def src_text(cid):
    s = DS[CHARTS[cid]['dataset']]['source_line']
    return s[len('Source: '):] if s.startswith('Source: ') else s


# ------------------------------------------------------------------------------------------------ the module
WORD_RX = re.compile(r"[A-Za-z][A-Za-z’'-]{3,}")


def coverage(cid, strings, text):
    """F15: every word drawn inside an SVG with role="img" appears in its name or its equivalent."""
    hay = typo(text).lower().replace('’', "'")
    for s in strings:
        for w in WORD_RX.findall(typo(s)):
            if w.lower().replace('’', "'") not in hay:
                PROBLEMS.append(f'{cid}: "{w}" is drawn but not in the image name or the equivalent ("{s[:40]}")')
                break


def module(cid, view, ground, mode='panel', inst='', anat=False, red=True, hl=2, extra_cls=''):
    c, s = CHARTS[cid], spec(cid)
    sp = SPECS[cid]
    did = c['dataset']
    uid = f'{view}{inst}-{cid.lower()}'
    g = {'ground': ground, 'red': red}
    sm = (lambda L: f'<span class="slotmark" aria-hidden="true">{L}</span>') if anat else (lambda L: '')
    strings = []
    if c['html']:
        fig = c['html'](uid, s) if cid != 'S06' else c['html'](uid, s, hl)
    else:
        arts = CT['artboards'] if mode == 'panel' else [('s', CT['still'])]
        out = []
        for art, W in arts:
            a = Art(W, f'{cid} {art}', g)
            c['gen'](a, s)
            strings.extend(a.strings)
            out.append(a.svg(uid, art, s['label'] + (' The Table button lists every value and note in the chart.' if mode == 'panel' else '')))
        fig = ''.join(out)
        if cid == 'S09':
            fig += event_register(s, hl + 1)
    ev = sp['evidence']
    idx = f'<p class="idx">{tx(s["index"])}</p>' if s.get('index') else ''
    head = (f'<div class="slot sa" data-slot="A">{sm("A")}<p class="ev" data-role="evidence-label">{tx(ev)}<span class="gw"> · {tx(s["kind_words"])}</span></p>{idx}</div>'
            f'<div class="slot sb" data-slot="B">{sm("B")}<h{hl} class="mt" id="{uid}-t" tabindex="-1" data-role="title">{tx(s["title"])}</h{hl}></div>'
            f'<div class="slot sc" data-slot="C">{sm("C")}<p class="ms" data-role="measure">{tx(s["measure"][0])}</p>'
            + ''.join(f'<p class="ms ms2">{tx(m)}</p>' for m in s['measure'][1:]) + '</div>')
    strongest = 'brightest fill' if ground == 'charcoal' else 'darkest ink'   # the subject's mark, named for this ground
    notes_list = [n.replace('{strongest}', strongest) if isinstance(n, str) else n
                  for n in list(s.get('html_notes', [])) + list(s.get('notes', []))]
    notes = ''.join(f'<p><strong>{tx(n[0])}</strong> {tx(n[1])}</p>' if isinstance(n, tuple) else f'<p>{tx(n)}</p>' for n in notes_list)
    if DS[did].get('required_text'):
        notes += ''.join(f'<p class="disc"><strong>Disclosure:</strong> {tx(t)}</p>' for t in DS[did]['required_text'])
    fname = f'{BUILD_DATE}_Oath-And-Action-{cid}-{slug(DS[did]["title"])}'
    src = (f'<div class="slot sg2" data-slot="G">{sm("G")}<p class="src" data-role="source"><span class="s1">Source: {tx(src_text(cid))}</span>'
           f'<span class="s2">Chart: Oath &amp; Action · <a href="#how-to-read">How to read our charts</a></span></p></div>')
    drawn_list = ''.join(f'<li>{tx(d)}</li>' for d in s.get('drawn', []))
    in_chart = (f'<p class="eqh">Labels and notes in the chart</p><ul class="eql">{drawn_list}</ul>' if drawn_list else '')
    equiv = (f'<p class="eqh">Every value in the chart. The notes and the source line stay below.</p>{c["table"]()}{in_chart}')
    if mode == 'panel':
        coverage(cid, strings, s.get('label', '') + ' ' + re.sub(r'<[^>]+>', ' ', html.unescape(equiv)))
        has_svg = not c['html']
        dls = (f'<div class="dls"><span class="dlh">Download</span>'
               f'<button type="button" class="dl" data-dl="csv" data-for="{cid}" data-file="{fname}" aria-label="Download the {cid} data as CSV">CSV</button>'
               + (f'<button type="button" class="dl" data-dl="svg" data-for="{cid}" data-file="{fname}" aria-label="Download {cid} as SVG">SVG</button>' if has_svg else '')
               + '</div>')
        ctl = (f'<div class="slot sd" data-slot="D">{sm("D")}<div class="ctl"><div class="sw" role="group" aria-label="Show {cid} as a chart or a table">'
               f'<button type="button" data-sw="c" aria-pressed="true" aria-controls="{uid}-pc" aria-label="Show the {cid} chart">Chart</button>'
               f'<button type="button" data-sw="t" aria-pressed="false" aria-controls="{uid}-pt" aria-label="Show the {cid} table">Table</button></div>{dls}</div></div>')
        ro = f'<p class="readout" aria-hidden="true">{tx(c["readout"])}</p>' if c['readout'] else ''
        body = (f'<div class="slot se" data-slot="E">{sm("E")}<div class="pane pane-c" id="{uid}-pc">{fig}{ro}</div>'
                f'<div class="pane pane-t" id="{uid}-pt" hidden data-role="equivalent">{equiv}</div></div>')
        return (f'<figure class="mod {extra_cls}" id="{uid}" data-spec="{cid}" data-dataset="{did}" data-evidence="{tx(ev)}" '
                f'data-title="{at(s["title"])}" data-desc="{at(s.get("label", s["title"]))}" aria-labelledby="{uid}-t">{head}{ctl}{body}'
                f'<div class="slot sf" data-slot="F">{sm("F")}<div class="notes">{notes}</div></div>{src}</figure>')
    alt_txt = s.get('label', s['title']) + ' Source: ' + src_text(cid)
    body = f'<div class="slot se" data-slot="E">{sm("E")}<div class="pane">{fig}</div></div>'
    still_note = '<p>Table and data: with the interactive version of this chart.</p>'
    # a still is a fixed-size image: it carries its own labeled scroll box, so it needs no outer wrapper on a narrow screen
    return (f'<div class="stillbox" role="region" tabindex="0" aria-label="The {cid} still at true size, {CT["still"]} pixels wide. On a narrow screen, scroll inside the box.">'
            f'<figure class="mod still {extra_cls}" id="{uid}" data-spec="{cid}" data-dataset="{did}" data-evidence="{tx(ev)}" '
            f'aria-labelledby="{uid}-t">{head}{body}<div class="slot sf" data-slot="F">{sm("F")}<div class="notes">{notes}{still_note}</div></div>'
            f'{src}<div class="alt" data-role="equivalent"><p class="alt-h">Alt text, sent with the image</p><p>{tx(alt_txt)}</p></div></figure></div>')


def strip(cid):
    c, s, sp = CHARTS[cid], spec(cid), SPECS[cid]
    fn = (c['gen'] or c['html']).__name__
    return (f'<aside class="strip" aria-label="Studio note on {cid}"><p class="sn-h">Studio note for reviewers</p>'
            f'<p class="sn-id">{cid} · {tx(sp["form"])}</p>'
            f'<p><span class="k">Reader question.</span> {tx(sp["reader_question"])}</p>'
            f'<p><span class="k">Why this form.</span> {tx(s["why"])}</p>'
            f'<p class="sn-kit"><span class="k">Kit.</span> register_chart(‘{cid}’, gen={fn}, adapter=spec_{cid.lower()}). {tx(c["size_note"])}.</p></aside>')


def spec_row(cid, view, ground):
    return f'<div class="spec-row">{module(cid, view, ground)}{strip(cid)}</div>'


# ------------------------------------------------------------------------------------------------ identity and views
def wordmark(height, master, cls, signature=False):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    sig = ' data-red="signature"' if signature else ''
    return src.replace('<svg ', f'<svg class="{cls}" data-view="wordmark"{sig} width="{w:.0f}" height="{height}" role="img" aria-label="Oath &amp; Action" ', 1)


VIEWS = [('white', 'White'), ('newsprint', 'Newsprint'), ('dark', 'Charcoal'), ('social', 'Social card'), ('system', 'System')]


def masthead():
    # one inline span holds the whole label, so the space before "card" survives inside the flex link
    tabs = ''.join(f'<li><a href="#{v}"><span>{tx(t).replace(" card", " <span class=t-more>card</span>")}</span></a></li>' for v, t in VIEWS)
    return ('<a class="skip" href="#main">Skip to the charts</a><header class="mast"><div class="wrap mrow">'
            '<a class="wm" href="#white" data-red="signature" aria-label="Oath &amp; Action, concept 03 first view">'
            f'{wordmark(24, "20261028_Wordmark-24px-Master.svg", "wm24")}{wordmark(16, "20261028_Wordmark-16px-Master.svg", "wm16")}</a>'
            '<p class="run">Chart system 03 · Instrument</p>'
            f'<nav class="tabs" aria-label="Views"><ul>{tabs}</ul></nav></div></header>')


HOWTO_SHORT = [('Kind and grade.', 'The label over each title names the kind of claim and how sure its evidence is.'),
               ('Title and measure.', 'The title states the finding; the line under it gives what, where and when.'),
               ('Dark and gray.', 'The darkest mark is what the title is about; gray marks are there for comparison.'),
               ('Red.', 'A red mark points at the one thing the title names; it never marks a party or a side.'),
               ('Check it.', 'Every chart has a Table button, notes and a source line.')]


def howto_short(view):
    items = ''.join(f'<li><strong>{tx(a)}</strong> {tx(b)}</li>' for a, b in HOWTO_SHORT)
    return (f'<section class="howto-s" aria-labelledby="{view}-howto"><div class="hs-top"><h2 class="hs-h" id="{view}-howto">How to read these charts</h2>'
            f'<p class="hs-more"><a href="#how-to-read">The full guide</a></p></div><ul>{items}</ul></section>')


def module_index(view):
    items = ''.join(f'<li><a href="#{view}-{cid.lower()}"><span class="mi-id">{cid}</span> {tx(SPECS[cid]["form"])}</a></li>' for cid in ORDER)
    return f'<nav class="mindex" aria-label="The ten charts on this view"><ul>{items}</ul></nav>'


def view_white():
    links = [('newsprint', 'Newsprint', 'The same ten modules on the warm ground.'), ('dark', 'Charcoal', 'Two modules on the dark ground.'),
             ('social', 'Social card', 'One module set as a 1080 by 1350 card.'), ('system', 'System', 'The kit on one sheet, and the full reading guide.')]
    lk = ''.join(f'<li><a href="#{v}"><span class="vl-t">{tx(t)}</span><span class="vl-d">{tx(d)}</span></a></li>' for v, t, d in links)
    rows = ''.join(spec_row(c, 'white', 'white') for c in ORDER)
    return ('<section class="view g-white" data-view-root="white" data-title="White" aria-labelledby="h-white"><div class="wrap">'
            '<header class="vhead"><div class="vh-main"><p class="eyebrow">Chart system · Concept 03 · White</p>'
            '<h1 class="display" id="h-white" tabindex="-1">Instrument</h1>'
            '<p class="deck">Every chart is a module with the same seven slots, built by one function per chart form, so the next chart comes from the kit. '
            '<span class="deck-more">Texture and open marks carry a second code after color, as the atlas’s evidence lines do, and each module works as a still image and as a panel with a Chart and Table switch.</span></p>'
            f'<nav class="vlinks" aria-label="Other views"><ul>{lk}</ul></nav></div>{howto_short("white")}</header>'
            f'{module_index("white")}<div class="specs">{rows}</div></div></section>')


def view_newsprint():
    rows = ''.join(spec_row(c, 'newsprint', 'newsprint') for c in ORDER)
    return ('<section class="view g-news" data-view-root="newsprint" data-title="Newsprint" aria-labelledby="h-news" hidden><div class="wrap">'
            '<header class="vhead"><div class="vh-main"><p class="eyebrow">Chart system · Concept 03 · Newsprint</p>'
            '<h1 class="headline" id="h-news" tabindex="-1">The same ten modules on Newsprint</h1>'
            '<p class="deck">The White view’s generators drew these; only the ground and its tokens change. '
            '<span class="deck-more">On Newsprint, Stone context measures 4.29:1, the toward-voters fill 5.01:1, and the one red mark in S01 takes a 1 px Charcoal keyline, because Pillar Red alone measures 2.96:1 here.</span></p></div>'
            f'{howto_short("newsprint")}</header>{module_index("newsprint")}<div class="specs">{rows}</div></div></section>')


def view_dark():
    toks = [('Named series and away from voters', 'ink', 'Newsprint'), ('Context and secondary text', 'ctx', 'Dim Newsprint'),
            ('Toward voters', 'tow', 'Verdigris, 30% toward Newsprint'), ('Middle level', 'some', 'Stone, 35% toward Newsprint'),
            ('Plausible fill', 'pl', 'Stone'), ('Gridline, decorative', 'grid', 'Stone, 45% toward Charcoal'), ("The headline's point", 'red', 'Pillar Red')]
    items = ''.join(f'<li><span class="sw2" style="background:{GROUNDS["charcoal"][t]}"{" data-red=\"swatch\"" if t == "red" else ""}></span>'
                    f'<span><strong>{tx(j)}.</strong> {tx(n)}, {GROUNDS["charcoal"][t]}, {contrast(GROUNDS["charcoal"][t], "#121212"):.2f}:1</span></li>' for j, t, n in toks)
    rows = spec_row('S01', 'dark', 'charcoal') + spec_row('S10', 'dark', 'charcoal')
    return ('<section class="view g-dark" data-view-root="dark" data-title="Charcoal" aria-labelledby="h-dark" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system · Concept 03 · Charcoal</p>'
            '<h1 class="headline" id="h-dark" tabindex="-1">Two modules on Charcoal</h1>'
            '<p class="deck">On Charcoal, Newsprint carries the named series, Dim Newsprint the context, and texture still carries the evidence grade. '
            'Text from 13 to 15 px sets one weight heavier. Lifted Prussian and lifted Verdigris sit only 0.022 apart in lightness here, so dark charts keep to two inks and label every mark.</p>'
            f'<ul class="dtok">{items}</ul><p class="dtn">Contrast measured against Charcoal, #121212.</p>'
            f'</header><div class="specs">{rows}</div></div></section>')


SOCIAL = {}


def social_card():
    cid = 'S01'
    s = spec(cid)
    sc = CT['social']
    cw = sc['w'] - 2 * sc['margin']
    tl = len(wrap(s['title'], cw / 0.95, 50, 800, tight=True))
    ml = len(wrap(s['measure'][0], cw, 22))
    sl = len(wrap('Source: ' + src_text(cid), cw, 20))
    avail = sc['h'] - 2 * sc['margin'] - 40 - 36 - 54 * tl - 14 - 30 * ml - 28 - 24 - 28 * sl - 28 - 24
    W0 = None
    for w in range(*sc['artboard_search']):
        a = Art(w, 'probe', {'ground': 'newsprint'})
        big_number(a, s)
        if a.H * cw / w <= avail:
            W0 = w
            break
    W0 = W0 or sc['artboard_fallback']
    a = Art(W0, 'S01 social card', {'ground': 'newsprint', 'red': True})
    big_number(a, s)
    PROBLEMS.extend(a.check())
    scale = round(min(cw / W0, avail / a.H), 3)
    if scale < sc['min_scale']:
        PROBLEMS.append(f'social card: {cid} sets at {scale:.2f}x, under the {sc["min_scale"]}x floor; shorten the title or the artboard')
    SOCIAL.update(scale=scale, w0=W0)
    bl = a.bleed
    art = (f'<svg class="art-c" data-view="social-s01-c" viewBox="{fmt(-bl)} 0 {fmt(W0 + bl)} {fmt(a.H)}" width="{fmt((W0 + bl) * scale)}" height="{fmt(a.H * scale)}" '
           f'style="margin-left:{fmt(-bl * scale)}px" role="img" aria-label="{at(s["label"])}" focusable="false">{"".join(a.o)}</svg>')
    card = (f'<div class="card g-news"><div class="c-top">{wordmark(40, "20261028_Wordmark-Display-Master.svg", "wmd", signature=True)}'
            f'<p class="c-ev" data-role="evidence-label">{tx(SPECS[cid]["evidence"])}</p></div>'
            f'<h2 class="c-t" data-role="title">{tx(s["title"])}</h2><p class="c-m" data-role="measure">{tx(s["measure"][0])}</p>'
            f'<div class="c-art">{art}</div><p class="c-s" data-role="source">Source: {tx(src_text(cid))}</p>'
            '<p class="c-cr">Chart: Oath &amp; Action, from its atlas, Who Do They Answer To?</p></div>')
    alt = s['title'] + ' ' + s['label'] + ' Source: ' + src_text(cid)
    return (f'<figure class="social" data-spec="{cid}" data-dataset="{CHARTS[cid]["dataset"]}" data-evidence="{SPECS[cid]["evidence"]}" aria-label="Social card built from S01">'
            f'<div class="cardbox" role="region" tabindex="0" aria-label="Social card at true size, 1080 by 1350 pixels. Scroll inside the box to see all of it.">{card}</div>'
            f'<div class="alt" data-role="equivalent"><p class="alt-h">Alt text, posted with the card</p><p>{tx(alt)}</p></div></figure>')


def view_social():
    card_html = social_card()
    return ('<section class="view g-white" data-view-root="social" data-title="Social card" aria-labelledby="h-social" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system · Concept 03 · Social card</p>'
            '<h1 class="headline" id="h-social" tabindex="-1">S01 as a 1080 by 1350 card</h1>'
            f'<p class="deck">The card is the S01 module with its controls removed. big_number() draws a {SOCIAL["w0"]} px artboard and the card sets it at '
            f'{SOCIAL["scale"]:.2f} times, so the smallest chart label reads at {13 * SOCIAL["scale"]:.0f} px. The card keeps the source line and names Oath &amp; Action and the atlas; it carries no web address until the site is settled.</p>'
            f'</header><div class="socwrap">{card_html}<aside class="strip" aria-label="Studio note on the social card">'
            '<p class="sn-h">Studio note for reviewers</p><p class="sn-id">Social card · built from S01</p>'
            '<p><span class="k">What changes.</span> The switch, the downloads and the readout drop. The title, measure, figure and source stay. The table travels as the alt text.</p>'
            '<p><span class="k">Size.</span> 1080 by 1350 px, the portrait post for Instagram and LinkedIn; 64 px margins on the 8 px rhythm.</p>'
            '<p><span class="k">Kit.</span> social_card() measures the title, measure and source, then asks the generator for the narrowest artboard that fills the card’s 952 px width and fits the height left over. A module whose scale would fall under ' + f'{CT["social"]["min_scale"]}' + ' times stops the build until its title or artboard is shorter.</p>'
            '</aside></div></div></section>')


# ------------------------------------------------------------------------------------------------ the system sheet
def sys_section(n, title, body, lead='', sid=None):
    lead_html = f'<p class="lede">{tx(lead)}</p>' if lead else ''
    hid = sid or f'sys-{n}'
    return f'<section class="ssec" aria-labelledby="{hid}"><h2 class="sh" id="{hid}" tabindex="-1"><span class="sn">{n:02d}</span> {tx(title)}</h2>{lead_html}{body}</section>'


def ty(name):
    f, w, s, lh, tr = CT['type'][name]
    track = f', {tr:+.3f} em'.replace('-', MINUS).replace('+', '+') if tr else ''
    return f'{f} {w}, {s}/{lh}{track}'


def sys_slots():
    sp = CT['slot_space']
    return [('A', 'Index', 'The evidence kind and its grade in words at left; the atlas record index at right, when the chart has one', f'Kind {ty("kind")}, capitals; grade {ty("grade_words")}; index {ty("index")}, Deep Stone', f'2 px Charcoal rule, then {sp["A"]}'),
            ('B', 'Title', 'One sentence that states the finding, its verb matched to the grade', f'{ty("title")}; {ty("title_phone")} on phones', str(sp['B'])),
            ('C', 'Measure', 'Measure, unit, place and period; where a scale starts if not at zero', f'{ty("measure")}, Deep Stone, 38 em at most', str(sp['C'])),
            ('D', 'Controls', 'Chart and Table switch at left, downloads at right. Panel only', 'Inter 600, 14; 32 px targets, 44 on phones', str(sp['D'])),
            ('E', 'Figure', 'One artboard at the module’s width, its notes inside the drawing; or an HTML table or grid that reflows', f'Labels {ty("data")}; notes {ty("note")}', str(sp['E'])),
            ('F', 'Notes', 'What a reader needs to read the chart honestly: coding rules, qualifications, the disclosure', f'{ty("notes_slot")}, 36 em at most (45 to 75 characters)', str(sp['F'])),
            ('G', 'Source', 'Source line in section 15 order; the credit and the reading guide link at right; then a 1 px Stone rule', f'{ty("source")}, Deep Stone', f'{sp["G"]}, then {sp["after"]} below')]


def sys_anatomy():
    tbl = ''.join(f'<tr><th scope="row"><span class="slk">{a}</span> {tx(n)}</th><td>{tx(h)}</td><td>{tx(t)}</td><td class="n">{tx(sp_)}</td></tr>' for a, n, h, t, sp_ in sys_slots())
    return (f'<div class="anat-grid"><div class="anat">{module("S03", "system", "white", inst="a", anat=True, hl=3)}</div>'
            f'<div class="anat-spec"><div class="tbl"><table class="st2"><caption class="vh">The seven slots</caption><thead><tr><th scope="col">Slot</th><th scope="col">Holds</th>'
            f'<th scope="col">Type</th><th scope="col">Space above, px</th></tr></thead><tbody>{tbl}</tbody></table></div>'
            '<p class="small">A slot never moves and never changes job. An empty slot closes up, except B, C, E and G, which every chart fills. '
            'The figure slot holds one artboard at a time: a container query shows the widest artboard that fits the module, so a drawing is never scaled up or down and every line stays in the 1, 1.5, 2, 3 and 6 px family.</p></div></div>')


def sys_sizes():
    rows = [('Column module', CT['artboards'][0][1], '8 of 12 columns at 1440; the default for atlas pages and reports'),
            ('Still', CT['still'], 'Substack and email body; exported at 2x'),
            ('Medium artboard', CT['artboards'][1][1], 'Tablets and narrow windows'),
            ('Social card artboard', SOCIAL['w0'], f'Chosen by social_card() and set at {SOCIAL["scale"]:.2f}x inside the 1080 by 1350 card'),
            ('Phone artboard, 390', CT['artboards'][2][1], 'Drawn at 358, the column of a 390 px phone'),
            ('Phone artboard, 360', CT['artboards'][3][1], 'Drawn at 328, the column of a 360 px phone')]
    rows.sort(key=lambda r: -r[1])
    bars = ''.join(f'<li><span class="szb" style="width:{100 * w / CT["artboards"][0][1]:.2f}%"></span><span class="szl"><strong>{tx(n)}</strong>, {w} px. {tx(d)}</span></li>' for n, w, d in rows)
    steps = ''.join(f'<li><span class="sp" style="width:{s_}px;height:{s_}px"></span><span>{s_}</span></li>' for s_ in CT['space'])
    brk = ''.join(f'<li><strong>{tx(k.replace("_", " "))}</strong>: from {v} px</li>' for k, v in CT['breaks'].items())
    return (f'<div class="two-col"><div><h3 class="sh3">Widths</h3><ul class="sizes">{bars}</ul></div>'
            '<div><h3 class="sh3">Spacing</h3><p class="small">Every gap is a step of the Signal Grid’s 8 px rhythm, with its 4 px half step. '
            f'Modules stack 72 px apart; slots sit 8 to 16 px apart; rows in a chart sit on 32 to 40 px.</p><ul class="steps">{steps}</ul>'
            f'<h3 class="sh3 sh3b">Layout switches inside generators</h3><ul class="brks">{brk}</ul></div></div>')


def sys_type():
    samples = {'title': 'The atlas codes 9 of 11 logged state statutes as away from voters.', 'kind': 'Finding', 'grade_words': 'Documented: the atlas’s dated log',
               'index': 'Repair log RL01 to RL64', 'measure': 'Rule changes by how they were made, United States, 1965 to 2026',
               'big': '86%', 'series': 'Toward voters', 'data': f'Down 3.7 points, {MINUS}3.7', 'note': '9 of 11 away from voters',
               'notes_slot': 'The log holds the 64 changes the atlas chose to record.', 'source': 'Source: U.S. Census Bureau, Table A-1. Retrieved November 6, 2026.'}
    names = {'title': 'Chart title', 'kind': 'Evidence kind', 'grade_words': 'Grade in words', 'index': 'Index', 'measure': 'Measure line', 'big': 'Big figure',
             'series': 'Series label', 'data': 'Data label', 'note': 'Note in a drawing', 'notes_slot': 'Notes slot', 'source': 'Source line'}
    items = ''.join(f'<li><p class="tr-n">{tx(names[k])}</p><p class="tr-sp">{tx(ty(k))}</p><p class="ts-{k}">{tx(samples[k])}</p></li>' for k in names)
    return (f'<ul class="ramp">{items}</ul><p class="small">Figures are tabular only where they are figures, so a hyphen inside a word keeps its own width. '
            'Lora Italic sets quoted words inside a note and nothing else; no chart title or label uses a serif. On Charcoal, text from 13 to 15 px sets one weight heavier.</p>')


def mk(svgbody, w, h):
    return f'<svg class="mks" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true" focusable="false">{svgbody}</svg>'


def sys_marks():
    L = CT['lines']
    lines = [(L['hair'], 'Hairline: gridlines, leaders, rules and the bar track, on half pixels so a 1x export prints them crisp', 'grid'),
             (L['outline'], 'Context lines in small multiples; the open ring for an earlier year; outlines', 'l-ctx'),
             (L['context'], 'Context series in a line chart; the threshold tick; dumbbell connectors', 'l-ctx2'),
             (L['named'], 'The series the title names; the red point mark', 'l-ink'),
             (L['lit'], 'The lit selection in an interactive panel only', 'l-sel')]
    li = ''.join(f'<li>{mk(f"<path d=\"M2 10H118\" class=\"{c}\" style=\"stroke-width:{w}px\"/>", 120, 20)}<span><strong>{fmt(w)} px.</strong> {tx(d)}</span></li>' for w, d, c in lines)
    u, b, sb, d = CT['unit'], CT['bar'], CT['share_bar'], CT['dot']
    shapes = [(mk(dir_markup(1, 1, u['size'], u['size'], 'tow') + dir_markup(1 + u['size'] + u['gap'], 1, u['size'], u['size'], 'away'), 2 * u['size'] + u['gap'] + 2, u['size'] + 2),
               f'Units: {u["size"]} px squares {u["gap"]} px apart, one per record. A roll-up record draws as a stack three units wide and says what it holds.'),
              (mk(R(2, 4, 160, b['h'], 'f-away') + R(2, 4 + b['pitch'], 110, b['h'], 'f-tow') + R(5, 7 + b['pitch'], 104, b['h'] - 6, 'frame'), 164, b['pitch'] + b['h'] + 6),
               f'Ranked bars: {b["h"]} px tall on a {b["pitch"]} px pitch; counts inside when the segment is 18 px or wider. 100% bars: {sb["h"]} px on a {sb["pitch"]} px pitch.'),
              (mk('<line x1="8" y1="16" x2="64" y2="16" class="l-ctx2"/>' + f'<circle cx="70" cy="16" r="{d["later"]}" class="f-ink"/><circle cx="8" cy="16" r="{d["earlier"]}" class="ring"/>'
                  f'<circle cx="104" cy="16" r="{d["timeline"]}" class="f-ink"/><circle cx="124" cy="16" r="{d["point"]}" class="f-ink"/>', 136, 32),
               f'Dots: {d["later"]} px radius for the later year, a {d["earlier"]} px open ring for the earlier; {d["timeline"]} px on a timeline; {d["point"]} px where a note points.')]
    sh = ''.join(f'<li>{s_}<span>{tx(t)}</span></li>' for s_, t in shapes)
    return f'<div class="two-col"><div><h3 class="sh3">Line weights</h3><ul class="mklist">{li}</ul></div><div><h3 class="sh3">Marks</h3><ul class="mklist">{sh}</ul></div></div>'


def sys_codes():
    dirs = ''.join(f'<li>{mk(dir_markup(2, 2, 28, 28, c), 32, 32)}<span><strong>{tx(w)}.</strong> {tx(dsc)}</span></li>' for (_, c, w), dsc in zip(DIRS, [
        'Solid Charcoal.', 'Verdigris strong with an inner frame in the ground color: the frame sets it apart from away on any copy.',
        'Light fill with a Stone outline.', 'Split: both fills in one mark.', 'Open: an outline on the ground, for a change still undecided.']))
    uid = 'sys-codes'
    grows = ''.join(f'<tr><th scope="row">{tx(w)}</th><td>{tx(k)}</td><td>{tx(gl)}</td><td>{mk(grade_markup(uid, k, 1, 3, 40, 16), 42, 22)} {tx(GRADE_FILL[k])}</td>'
                    f'<td>{line_sample(ls)} {tx(ls)}</td><td>{tx(vb)}</td></tr>' for k, w, gl, ls, vb in GRADES)
    gdefs = f'<svg width="0" height="0" class="vh" aria-hidden="true" focusable="false"><defs>{grade_defs(uid)}</defs></svg>'
    glyphs = ''.join(f'<li>{boxed_arrow(c, 24)}<span><strong>{tx(CLASS_WORD[c])}.</strong></span></li>' for c in CLASS_WORD)
    return (f'{gdefs}<div class="two-col"><div><h3 class="sh3">Direction code, repair log</h3><ul class="mklist">{dirs}</ul>'
            '<p class="small">Grayscale holds the order: Charcoal, Verdigris strong with its frame, Stone light, ground. Rows in S08 and segment order in S03 add a third code.</p></div>'
            f'<div><h3 class="sh3">Scenario arrows</h3><ul class="mklist gl-list">{glyphs}</ul><p class="small">The arrow in its box carries the direction on a black-and-white copy; '
            'a Verdigris or Prussian tint carries the side as a second code. No scale pairs red with blue. Party marks take neutral inks with the party’s name printed on them, ordered by value or alphabet.</p></div></div>'
            f'<h3 class="sh3 sh3b">Evidence grades: one table for every V7 label</h3><div class="tbl"><table class="st2 gtab"><caption class="vh">Evidence grades</caption><thead><tr>'
            '<th scope="col">Display word</th><th scope="col">V7 key</th><th scope="col">Reader’s meaning</th><th scope="col">Fill, in this order</th><th scope="col">Line on the atlas</th><th scope="col">Title verb</th></tr></thead>'
            f'<tbody>{grows}</tbody></table></div><p class="small">The code covers claims and connections alike. V7’s key plausible_contested prints as Contested. Grades never take red. '
            'Where a chart’s categories carry their own code, as grades do, rank the rows by the code’s order or draw every bar in one ink and print the grade, so the darkest-ink rule never points at a grade by accident.</p>')


PAL = [('Ground', 'gr', 'White, Newsprint, Charcoal'), ('Named series, baseline, away from voters', 'ink', 'Charcoal; Newsprint on Charcoal'),
       ('Context', 'ctx', 'Stone; Dim Newsprint on Charcoal'), ('Secondary text', 'sec', 'Deep Stone; Dim Newsprint on Charcoal'),
       ('Toward voters, up arrow', 'tow', 'Verdigris 25% toward Charcoal; on Charcoal, Verdigris 30% toward Newsprint'),
       ('Middle level: some elections', 'some', 'Stone; on Charcoal, Stone 35% toward Newsprint'),
       ('Kept existing rules; plausible (values printed)', 'kept', 'Stone 55% toward the ground'),
       ('Well supported', 'g2', 'Charcoal 38% toward the ground; Dim Newsprint on Charcoal'),
       ('Up tint (words print in the cell)', 'vdl', 'Verdigris 55% toward the ground'), ('Down tint (words print in the cell)', 'prl', 'Prussian 62% toward the ground'),
       ('Down arrow', 'pr', 'Prussian; on Charcoal, Prussian 55% toward Newsprint'), ('Gridline, decorative', 'grid', 'Stone 70% toward the ground'),
       ("The headline's point", 'red', 'Pillar Red; 1 px Charcoal keyline on Newsprint'), ('Focus ring', 'focus', 'Charcoal; Newsprint on Charcoal')]


def sys_palettes():
    head = '<tr><th scope="col">Job</th>' + ''.join(f'<th scope="col">{n}</th>' for n in ('White', 'Newsprint', 'Charcoal')) + '</tr>'
    body = []
    for job, tok, name in PAL:
        cells = []
        for gname in ('white', 'newsprint', 'charcoal'):
            h = GROUNDS[gname][tok]
            gr = GROUNDS[gname]['gr']
            red = ' data-red="swatch"' if h == '#E63946' else ''
            mark = '' if tok == 'gr' else f'{contrast(h, gr):.2f}:1'
            cells.append(f'<td><span class="pal"><span class="sw3" style="background:{h}"{red}></span><span class="hx">{h}</span><span class="cr">{mark}</span></span></td>')
        body.append(f'<tr><th scope="row">{tx(job)}<span class="pn">{tx(name)}</span></th>{"".join(cells)}</tr>')
    return (f'<div class="tbl"><table class="st2 paltab"><caption class="vh">Chart palette with measured contrast against each ground</caption><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'
            '<p class="small">Contrast is WCAG 2 against the ground, computed by the build script. Every tint is one of the palette lab’s OKLab mixes of locked colors; the script recovered each mix and prints it above. '
            'Kept existing rules, the plausible tint, the up and down tints and the gridline fall under 3:1 by design: each kept segment prints its count and carries a Stone outline, each plausible segment carries an outline, '
            'each tinted cell prints the atlas’s words beside an arrow, and gridlines carry no meaning. Pillar Red appears in the table as a swatch, which Rule 05.3 does not count.</p>')


RULE_053 = ("The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge "
            "diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with the wordmark and never stands in "
            "for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single "
            "feature icon. In a row or a menu, icons go one color and only the current one keeps its red. Each view (one screen, card, slide or printed "
            "page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point "
            "the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A "
            "hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, "
            "Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian.")


def sys_red():
    url = next(s_['url'] for s_ in DS['stock-trading-ban']['sources'] if s_['id'] == 'W035')
    return (f'<blockquote class="rule"><p>{tx(RULE_053)}</p><footer>Rule 05.3, the red rule (D2-01)</footer></blockquote>'
            '<p class="body2">On a chart page each module counts as one view. Red never codes a series, a category, a scale, a party or a grade. It may mark the one point '
            'a title names, here the 7 votes the Senate fell short in S01, and only when no error or ask holds the view. Press the button to put an ask in this view: '
            'the ask takes the red, and the shortfall steps down to Charcoal at the same 3 px weight.</p>'
            '<p class="body2"><strong>A chart on its own, or added to a page.</strong> A chart posted alone, as a card or a still, may mark the point its title names in red. '
            'A chart added to a page takes red only when the page’s red job moves to it.</p>'
            f'<div class="askbar"><button type="button" class="tgl" aria-pressed="false" data-ask="system-r-s01">Put an ask in this view</button>'
            f'<span class="askwrap" id="ask-demo" hidden><a class="ask" href="{at(url)}" data-red="working" data-red-job="ask">See how each senator voted</a>'
            '<span class="ill">Illustrative ask</span></span></div>'
            f'<div class="redmod">{module("S01", "system", "white", inst="-r", hl=3)}</div>')


def sys_rules():
    rules = [('Notes sit inside the drawing when they are short.', 'Inter 13 in Deep Stone, joined to the data by 1 px leaders, clear of every gridline or on a band in the ground color. Long notes go in the notes slot, where they wrap at 45 to 75 characters a line.'),
             ('Label directly.', 'Labels sit on the mark or at its end. A key appears only when labels cannot fit, and it sits inside the drawing above the marks it explains.'),
             ('Write the unit once.', 'On the top tick or the first label: “100%”, “17 changes”, “Down 3.7 points”. Other ticks stay bare.'),
             ('Numbers are tabular, and minus is the true minus.', f'Write {MINUS}3.7 with U+2212. Dates print in words with no line break inside them.'),
             ('Scales are honest.', 'Bars start at zero. A line or dot scale may start elsewhere when the measure line says so. Small multiples share one scale. Missing years and method breaks stay open; no line joins them.'),
             ('Small changes are changes.', 'A change of a point or two in a survey with no published margin of error prints as “little changed”, never as a fall or a rise.'),
             ('Hover repeats the table.', 'The readout under a chart repeats what the table holds. Every value is printed, in the notes or in the table.'),
             ('The source line goes under every chart.', 'In section 15 order: publisher, title or table, observation period, geography, date retrieved, qualification. Shorten by dropping words; every fact stays. The credit and the link to the reading guide sit at the right.'),
             ('Record IDs stay in the index and the tables.', 'RL07, PW15 and E09 print in slot A and in the table, where a reader looks a record up, and nowhere on the face of a drawing. When a dataset mixes ID prefixes, the index prints the count and the prefixes: “118 connections, IDs L, LE, LT, LX and T”.'),
             ('No reader sees studio words.', 'No color names, source codes or “the studio” on the face of a chart or in its notes; say “the dark line”, “the gray bars”, “Oath & Action”.'),
             ('Read every title twice.', 'Before a title ships, read it once as a reader on the left and once as a reader on the right. If either would take it as a side, rewrite it.'),
             ('Disclose where the editor works on the subject.', 'Charts on nomination, ranked-ballot or election-rule data print the editor’s disclosure in the notes, labeled “Disclosure:”.'),
             ('Illustrative items carry the word.', '“Illustrative data” or “Illustrative ask” sits beside the item itself.')]
    return '<ol class="rules">' + ''.join(f'<li><strong>{tx(a)}</strong> {tx(b)}</li>' for a, b in rules) + '</ol>'


def sys_kit():
    gens = [('big_number(art, spec)', 'figure, group_head, groups (key, label, value, party, context), vote_head, votes (label, sub, scale, segs, threshold, red)', 'S01'),
            ('line_events(art, spec)', 'x_range, x_ticks, y_max, y_step, series (segments of points, line and dot classes), breaks (x, word, top), labels per layout, notes (point, text, side)', 'S02'),
            ('ranked_bar(art, spec)', 'rows (key, label, total, segs of field, value and code, note, sub), key, unit; the scale comes from the largest total', 'S03'),
            ('dumbbell(art, spec)', 'rows (label, a and b points, change words, context), years; the scale crops to whole tens around the data', 'S04'),
            ('small_multiples(art, spec)', 'panels (id, name, segments, last, note), y_range, x_range, note_at', 'S05'),
            ('comparison_table(uid, spec)', 'rows with the atlas’s words and a class per family, families, key_head, caption', 'S06'),
            ('tile_map(art, spec)', 'tiles (col, row, key, status, fill, year, tip), key, size_note; the grid comes from geo/us-state-tile-grid.json', 'S07'),
            ('unit_ledger(uid, spec)', 'rows (code, word, records), rollups (key: label and tip), label', 'S08'),
            ('strip_timeline(art, spec)', 'lanes (label, question, events with exact fractional dates), x_range, ticks', 'S09'),
            ('share_bars(art, spec)', 'rows (key, label, total, segs of grade and count), grades, unit, share_field, right_head', 'S10')]
    rows = ''.join(f'<tr><th scope="row"><code>{tx(n)}</code></th><td>{tx(i)}</td><td>{tx(e)}</td></tr>' for n, i, e in gens)
    example = ("register_chart('X01', 'link-grades', share_bars, adapter=spec_x01, table=eq_x01,\n"
               "               csv_cols=['key', 'documented', 'well-supported', 'plausible', 'contested', 'hypothesis'])\n\n"
               "def spec_x01():\n    return {'kind_words': ..., 'title': ..., 'measure': [...], 'index': '118 connections, IDs L, LE, LT, LX and T',\n"
               "            'rows': [...], 'grades': [...], 'unit': 'links', 'share_field': 'documented', 'right_head': 'Documented',\n"
               "            'notes': [...], 'drawn': [...], 'label': ..., 'why': ...}")
    return (f'<p class="body2">A chart joins the kit with one call to <code>register_chart()</code>: its dataset, its generator, an adapter that reads the shared data into a spec, '
            'a table builder for the equivalent and the CSV columns. The module then supplies all seven slots, the Chart and Table switch, both downloads, the still and the coverage check. '
            'Every generator draws through <code>Art</code>, which measures each label with the Inter files in <code>./fonts</code> and stops the build when a label leaves its drawing, '
            'touches another, or meets a line, rule, leader or mark, with 15% headroom for wider text spacing.</p>'
            f'<div class="tbl"><table class="st2 kittab"><caption class="vh">Generators and their inputs</caption><thead><tr><th scope="col">Generator</th><th scope="col">Spec it reads</th><th scope="col">Used by</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<h3 class="sh3 sh3b">A worked example</h3><pre class="code"><code>{html.escape(example, quote=False)}</code></pre>'
            '<p class="small">Downloads name their files <code>YYYYMMDD_Oath-And-Action-&lt;ID&gt;-&lt;Dataset-Title&gt;</code>; the SVG carries the chart’s title and alt text as &lt;title&gt; and &lt;desc&gt;. '
            'The SVG names its fonts and carries no font files, so a design tool needs Inter and Inter Tight installed. A PNG still would come from an export step the kit does not build yet. '
            'Motion is not in the kit yet; the first animated chart arrives with a reduced-motion path that shows the final state.</p>')


def sys_still():
    changes = [('Stays', 'Slots A, B, C, E, F and G in the same order and the same type; every printed number; every note; the source line.'),
               ('Drops', 'Slot D: the Chart and Table switch and the downloads. The tap and hover readout.'),
               ('Adds', 'Alt text with every value and the source, sent with the image, and a line in the notes that says where the table and data live.'),
               ('Changes', f'The figure uses a {CT["still"]} px artboard drawn by the same generator and exports at 2x for Substack and email. Nothing moves between slots.')]
    lst = ''.join(f'<li><strong>{a}.</strong> {tx(b)}</li>' for a, b in changes)
    return (f'<div class="stillgrid"><div>{module("S03", "system", "white", mode="still", inst="-s", hl=3)}</div>'
            f'<div><h3 class="sh3">Still and panel</h3><ul class="chg">{lst}</ul></div></div>')


READ_FULL = [
    ('What kind of claim.', 'The small label above the title says what kind of claim the chart makes. A Finding reports what the data shows: a count, a measured rate or a record. '
     'An Association says two things move together and does not say one causes the other. An Estimate says what would or may happen if stated assumptions hold. '
     'An Illustration explains an idea with an example; its numbers are made up and labeled so.'),
    ('How sure.', 'After the kind come a few words on the evidence: documented means on the public record; an official statistic comes from a government survey or count; '
     'a secondary source is someone else’s list that Oath & Action checked against its own record.'),
    ('The verb in the title.', 'The verb matches the evidence. Documented facts take plain record words: was, passed, logged. A strong research finding says raises or lowers. '
     'Some evidence says can or may. Disputed evidence gives both readings. An untested idea says untested. A scenario says would or may.'),
    ('The line under the title.', 'It names what was measured, where and when, and says when a scale does not start at zero.'),
    ('Dark and gray.', 'The darkest mark is the one the title is about; gray marks are there for comparison. Where a chart uses a code of its own, such as the grades, its key says so.'),
    ('Red.', 'A red mark, when a chart has one, points at the single thing the title names. It never marks a party or a side, and it carries no verdict on either.'),
    ('Texture.', 'In the evidence charts, solid means documented or well supported, a light tint means plausible, and a hatch means contested, as solid, dashed and dash-dot lines do on the atlas.'),
    ('Survey numbers.', 'Survey numbers come from a sample of people, so each has a margin of error. A margin of 0.5 points means the true figure most likely sits within half a point either way, '
     'and a smaller change may be chance. When a table publishes no margin, a change of a point or two prints as little changed.'),
    ('Records.', 'Codes such as RL07 or PW15 in a chart’s top line are record numbers. Search the atlas for them to read the full record.'),
    ('Check it.', 'Every chart has a Table button, and its source sits under it in both states. The downloads give you the same numbers.')]


def sys_read():
    return '<ol class="readers">' + ''.join(f'<li><strong>{tx(a)}</strong> {tx(b)}</li>' for a, b in READ_FULL) + '</ol>'


def view_system():
    secs = [
        sys_section(1, 'How to read our charts', sys_read(), 'For readers. Every chart’s source line links here, and this list can run on the atlas’s help page and under a report’s first chart.', sid='how-to-read'),
        sys_section(2, 'The module', sys_anatomy(), 'One chart, every part named. The letters in the margin match the table.'),
        sys_section(3, 'Sizes and spacing', sys_sizes()),
        sys_section(4, 'Type ramp', sys_type(), 'Inter Tight for titles and big figures, Inter for everything a reader reads in or around a chart. Every value here is read from CHART_TOKENS in the build script.'),
        sys_section(5, 'Marks', sys_marks()),
        sys_section(6, 'Codes after color', sys_codes(), 'Every code survives grayscale through a second channel: fill against outline, texture, shape or position.'),
        sys_section(7, 'Palettes, measured', sys_palettes()),
        sys_section(8, 'Red', sys_red()),
        sys_section(9, 'Annotation, sources and reader words', sys_rules()),
        sys_section(10, 'The kit', sys_kit()),
        sys_section(11, 'Still image and interactive panel', sys_still()),
    ]
    return ('<section class="view g-white" data-view-root="system" data-title="System" aria-labelledby="h-sys" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system · Concept 03 · System</p><h1 class="headline" id="h-sys" tabindex="-1">The kit on one sheet</h1>'
            '<p class="deck">The reading guide first, then what a builder needs to make the next chart without asking: the module’s seven slots, its sizes, the type ramp, the marks, '
            'the codes, the palettes with measured contrast, the red rule, the annotation and source rules, the generators and what changes between a still image and a panel.</p>'
            f'</header>{"".join(secs)}</div></section>')


# ------------------------------------------------------------------------------------------------ CSS and JS
CSS = r"""
:root{--gut:24px}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:400 17px/27px Inter,system-ui,sans-serif;background:#FFFFFF;color:#121212}
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none!important}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--focus,#121212);outline-offset:2px}
[tabindex="-1"]:focus{outline:none}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.skip{position:absolute;left:16px;top:-200px;z-index:200;padding:10px 14px;background:#FFFFFF;border:2px solid #121212;font:600 15px/1 Inter,sans-serif;color:#121212}
.skip:focus{top:12px}
.tn{font-variant-numeric:tabular-nums}
/* masthead */
.mast{border-bottom:1px solid var(--rule)}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;color:var(--ink);padding:14px 0}
.wm svg{--amp:#E63946}
.wm16{display:none}
.run{margin:0 0 0 48px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.tabs ul{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:var(--ink)}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ink)}
.tabs a:hover{text-decoration:underline}
/* view heads */
.view{padding-bottom:96px}
.vhead{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:24px 48px;padding:40px 0 8px;align-items:start}
.g-dark .vhead,[data-view-root="social"] .vhead,[data-view-root="system"] .vhead{display:block;max-width:1080px}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;margin-left:-.04em}
.headline{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;text-wrap:balance}
.deck{margin:16px 0 0;font:400 19px/28px Inter,sans-serif;max-width:40em;text-wrap:pretty}
.lede{margin:8px 0 24px;font:400 17px/27px Inter,sans-serif;max-width:46em}
.vlinks ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px;margin:24px 0 0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.vlinks a{display:grid;gap:2px;padding:10px 0 12px;min-height:44px;text-decoration:none}
.vlinks a:hover .vl-t{text-decoration:underline}
.vl-t{font:600 17px/24px Inter,sans-serif}.vl-d{font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.howto-s{border-top:2px solid var(--ink);padding-top:10px}
.hs-h{margin:0;font:800 22px/26px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em}
.howto-s ul{margin:0;padding:0;list-style:none;font:400 15px/22px Inter,sans-serif}
.howto-s li{padding:5px 0;border-top:1px solid var(--grid)}
.hs-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:0 16px}
.hs-more{margin:0;font:600 15px/22px Inter,sans-serif}
.hs-more a{display:inline-flex;align-items:center;min-height:44px}
.mindex ul{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0 24px;margin:32px 0 0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.mindex a{display:flex;gap:8px;align-items:center;min-height:44px;border-bottom:1px solid var(--grid);font:400 15px/20px Inter,sans-serif;text-decoration:none}
.mindex a:hover{text-decoration:underline}
.mi-id{font:600 13px/18px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
/* spec rows: module in 8 columns, the studio note in the last 3 */
.specs{display:grid;gap:72px;margin-top:48px}
.spec-row{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:var(--gut);align-items:start}
.spec-row>.mod{grid-column:1/span 8}
.spec-row>.strip{grid-column:10/span 3}
/* the module */
.mod{margin:0;border-top:2px solid var(--ink);border-bottom:1px solid var(--rule);padding-top:12px;container-type:inline-size;container-name:mod;min-width:0;scroll-margin-top:16px}
.slot{position:relative}
.sa{display:flex;justify-content:space-between;align-items:baseline;gap:4px 16px;flex-wrap:wrap}
.ev{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.gw{font-weight:400;letter-spacing:0;text-transform:none;color:var(--sec)}
.idx{margin:0;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.mt{margin:8px 0 0;font:800 28px/32px "Inter Tight",Inter,sans-serif;letter-spacing:-.025em;max-width:30em;text-wrap:balance}
.ms{margin:8px 0 0;font:400 15px/23px Inter,sans-serif;color:var(--sec);max-width:38em;text-wrap:pretty}
.ms2{margin-top:4px;color:var(--ink)}
.ctl{display:flex;justify-content:space-between;align-items:center;gap:8px 16px;flex-wrap:wrap;margin-top:16px}
.sw{display:inline-flex;border:1px solid var(--ink)}
.sw button{min-height:32px;min-width:84px;padding:0 14px;border:0;background:var(--gr);color:var(--ink);font:600 14px/1 Inter,sans-serif;cursor:pointer}
.sw button+button{border-left:1px solid var(--ink)}
.sw button[aria-pressed="true"]{background:var(--ink);color:var(--gr)}
.sw button[aria-pressed="true"]::before{content:"\2713\00a0" / ""}
.dls{display:flex;gap:8px;align-items:center}
.dlh{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.dl{min-height:32px;min-width:48px;padding:0 10px;border:1px solid var(--ctx);background:var(--gr);color:var(--ink);font:600 14px/1 Inter,sans-serif;cursor:pointer}
.dl:hover,.sw button:hover{text-decoration:underline;text-underline-offset:3px}
.se{margin-top:16px}
.pane-c{min-height:20px}
.art{display:none;height:auto;max-width:none;overflow:visible}
.art-n{display:block}
@container mod (min-width:§art_p§px){.art-n{display:none}.art-p{display:block}}
@container mod (min-width:§art_m§px){.art-p{display:none}.art-m{display:block}}
@container mod (min-width:§art_w§px){.art-m{display:none}.art-w{display:block}}
.mod.still{width:§still§px;max-width:none}
.still .art{display:block}
.readout{margin:12px 0 0;min-height:20px;font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:36em}
.sf{margin-top:16px}
.notes{font:400 14px/20px Inter,sans-serif;max-width:36em;text-wrap:pretty}
.notes p{margin:0 0 8px}
.disc{padding-left:10px;border-left:2px solid var(--ink)}
.sg2{margin-top:12px;padding-bottom:16px}
.src{margin:0;display:flex;justify-content:space-between;gap:4px 24px;font:400 13px/18px Inter,sans-serif;color:var(--sec);text-wrap:pretty}
.src .s1{max-width:46em}.src .s2{flex:none;max-width:16em;text-align:right}
.src a{color:var(--ink)}
.eqh{margin:0 0 8px;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.eql{margin:0 0 8px;padding-left:18px;font:400 14px/20px Inter,sans-serif;max-width:36em}
.alt{margin:0 0 16px;padding:10px 12px;border-left:2px solid var(--ink);font:400 14px/20px Inter,sans-serif;max-width:36em}
.alt p{margin:0 0 4px}.alt-h{font-weight:600}
/* tables */
.tbl{max-width:100%}
table.eqt,table.st2{width:100%;border-collapse:collapse;font:400 14px/20px Inter,sans-serif}
.eqt caption{text-align:left;font:600 14px/20px Inter,sans-serif;padding-bottom:6px}
.eqt th,.eqt td,.st2 th,.st2 td{border-top:1px solid var(--grid);padding:6px 12px 6px 0;text-align:left;vertical-align:top}
.eqt thead th,.st2 thead th{border-top:1px solid var(--ink);font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.eqt tbody th{font-weight:600}
td.n,.st2 td.n{font-variant-numeric:tabular-nums}
.eqt+.tbl,.tbl+.tbl{margin-top:16px}
.tl{display:none}
/* S06 comparison table */
.sg-kh{margin:0 0 6px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.sg-key{display:flex;flex-wrap:wrap;gap:4px 18px;margin:0 0 12px;padding:0;list-style:none;font:400 13px/18px Inter,sans-serif}
.sg-key li{display:inline-flex;gap:6px;align-items:center}
.sgt{width:100%;border-collapse:collapse;table-layout:fixed;font:400 14px/19px Inter,sans-serif}
.sgt thead th{text-align:left;vertical-align:bottom;padding:0 8px 6px;border-bottom:1px solid var(--ink);font:600 13px/17px Inter,sans-serif}
.sgt thead th:first-child{width:31%;padding-left:0}
.sgt tbody th{text-align:left;vertical-align:top;padding:8px 8px 8px 0;font:600 14px/19px Inter,sans-serif;border-bottom:1px solid var(--grid)}
.sgt td{vertical-align:top;padding:8px;border-bottom:1px solid var(--grid);border-left:2px solid var(--gr)}
.sid{float:left;width:40px;font:600 13px/19px Inter,sans-serif;color:var(--sec)}
.snm{display:block;margin-left:40px}
.sgl{display:block;margin-top:2px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.cw{display:flex;gap:7px;align-items:flex-start}.cw .gl{flex:none}
.fam-l{display:none}
.c-up{background:var(--vdl)}.c-sup{background:var(--vdxl)}.c-fod{background:var(--prxl)}.c-down{background:var(--prl)}
.gl .gbox{fill:var(--gr);stroke:var(--ctx);stroke-width:1}
.gl .gf-up{fill:var(--tow)}.gl .gs-up{fill:none;stroke:var(--tow);stroke-width:2.2}
.gl .gf-down{fill:var(--pr)}.gl .gs-down{fill:none;stroke:var(--pr);stroke-width:2.2}
.gl .gf-flat{fill:var(--ctx)}.gl .gs-flat{fill:none;stroke:var(--ctx);stroke-width:2.4}
.gl .gf-mix{fill:var(--ink)}.gl .gs-mix{fill:none;stroke:var(--ink);stroke-width:2}
@container mod (max-width:§table_reflow§px){
 .sgt,.sgt tbody,.sgt tr,.sgt th,.sgt td{display:block;width:auto}
 .sgt thead{display:none}
 .sgt tr{border-top:1px solid var(--ink);padding:6px 0 10px}
 .sgt tbody th{border:0;padding:4px 0 6px}
 .sgt td{border:0;border-top:1px solid var(--gr);padding:6px 8px}
 .fam-l{display:block;font:600 13px/18px Inter,sans-serif;color:var(--ink)}
 .eqt,.eqt tbody,.eqt tr,.eqt th,.eqt td{display:block;width:auto}
 .eqt thead{display:none}
 .eqt tr{border-top:1px solid var(--ink);padding:6px 0}
 .eqt th,.eqt td{border:0;padding:2px 0}
 .eqt .tl{display:block;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
}
/* S08 unit ledger */
.ul{display:grid;gap:0}
.ul-row{display:grid;gap:6px;border-top:1px solid var(--grid);padding:10px 0 12px}
.ul p{margin:0}
.ul-dw{font:600 15px/20px Inter,sans-serif}.ul-dn{font:700 15px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
.ul-us{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.u{display:block;flex:none;overflow:visible}
.ul-k{display:flex;gap:8px;align-items:center;margin:4px 0 0;font:400 14px/20px Inter,sans-serif}.ul-k .u{flex:none}
.ul-none{font:400 13px/18px Inter,sans-serif;color:var(--sec);min-height:24px;display:inline-flex;align-items:center}
/* S09 event register */
.ereg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px 20px;margin-top:20px}
.er-c{border-top:1px solid var(--ink);padding-top:8px}
.er-h{margin:0;font:600 15px/20px Inter,sans-serif}
.er-q{margin:2px 0 8px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.er-l{margin:0;padding:0;list-style:none;font:400 13px/18px Inter,sans-serif}
.er-l li{display:grid;gap:1px;padding:6px 0;border-top:1px solid var(--grid)}
.er-y{color:var(--sec)}.er-n{font-weight:600}.er-d{color:var(--sec)}
@container mod (max-width:§four_panels§px){.ereg{grid-template-columns:repeat(2,minmax(0,1fr))}}
@container mod (max-width:§two_panels§px){.ereg{grid-template-columns:minmax(0,1fr)}}
/* studio strip: on the other ground, so nobody reads it as chart copy */
.strip{background:var(--alt);padding:16px 16px 8px;font:400 14px/20px Inter,sans-serif;color:var(--ink)}
.g-dark .strip{border:1px solid var(--ctx)}
.strip p{margin:0 0 10px}
.sn-h{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.sn-id{font:800 20px/24px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em}
.strip .k{font-weight:600}
/* SVG chart styles */
svg text{font-family:Inter,sans-serif}
.x13{font-size:13px;font-weight:400;fill:var(--sec)}
.xkey{font-size:13px;font-weight:400;fill:var(--ink)}
.x13b{font-size:13px;font-weight:600;fill:var(--ink)}
.x13s{font-size:13px;font-weight:600;fill:var(--sec)}
.x15{font-size:15px;font-weight:400;fill:var(--ink)}
.x15b{font-size:15px;font-weight:600;fill:var(--ink)}
.x15k{font-size:15px;font-weight:700;fill:var(--ink)}
.xin{font-size:13px;font-weight:600;fill:var(--on-away)}
.xint{font-size:13px;font-weight:600;fill:var(--on-tow)}
.xins{font-size:13px;font-weight:600;fill:var(--on-some)}
.xbig{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;letter-spacing:-.03em;fill:var(--ink)}
.g-dark .x13,.g-dark .x15,.g-dark .xkey{font-weight:500}
.grid{stroke:var(--grid);stroke-width:1}
.base{stroke:var(--ink);stroke-width:1}
.lane{stroke:var(--ctx);stroke-width:1}
.lead{stroke:var(--ctx);stroke-width:1;fill:none}
.sep{stroke:var(--gr);stroke-width:2}
.track{fill:none;stroke:var(--grid);stroke-width:1}
.tick2{stroke:var(--ink);stroke-width:2}
.knock{fill:var(--gr)}
.frame{fill:none;stroke:var(--gr);stroke-width:1.5}
.f-ink{fill:var(--ink)}.f-ctx{fill:var(--ctx)}.f-g2{fill:var(--g2)}
.f-away{fill:var(--away)}.f-tow{fill:var(--tow)}
.f-kept{fill:var(--kept);stroke:var(--ctx);stroke-width:1}
.f-pend{fill:var(--gr);stroke:var(--ink);stroke-width:1.5}
.f-some{fill:var(--some)}
.f-none{fill:var(--gr);stroke:var(--ctx);stroke-width:1}
.f-pl{fill:var(--pl);stroke:var(--ink);stroke-width:1}
.f-tex{stroke:var(--ink);stroke-width:1}
.pbg{fill:var(--gr)}.phs{stroke:var(--ink);stroke-width:1.5}.pdt{fill:var(--ink)}
.lsam{stroke:var(--ink);stroke-width:2;fill:none}
.ring{fill:var(--gr);stroke:var(--ink);stroke-width:1.5}
.l-ink{stroke:var(--ink);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round}
.l-ctx{stroke:var(--ctx);stroke-width:1.5;fill:none;stroke-linejoin:round}
.l-ctx2{stroke:var(--ctx);stroke-width:2;fill:none;stroke-linejoin:round}
.l-sel{stroke:var(--ink);fill:none}
.redmark{stroke:var(--red);stroke-width:3;fill:none;stroke-linecap:square}
.redkey{stroke:var(--ink);stroke-width:5;fill:none;stroke-linecap:square}
.inkmark{stroke:var(--ink);stroke-width:3;fill:none}
.stepdown .redmark{stroke:var(--ink)}
.stepdown .redkey{display:none}
[data-tip]{cursor:default}
@media (forced-colors:active){
 .art,.u,.gl,.mks,.art-c{forced-color-adjust:none}
 .sw button[aria-pressed="true"]{forced-color-adjust:none;background:Highlight;color:HighlightText}
}
/* social */
.socwrap{display:grid;grid-template-columns:minmax(0,1fr);gap:24px;margin-top:32px;align-items:start}
.socwrap>.strip{max-width:866px}
.social{margin:0;min-width:0}
.cardbox{overflow:auto;width:max-content;max-width:100%;border:1px solid var(--rule)}
.card{width:1080px;height:1350px;padding:64px;display:flex;flex-direction:column;overflow:hidden}
.c-top{display:flex;justify-content:space-between;align-items:center;height:40px;color:#121212}
.wmd{--amp:#E63946;display:block}
.c-ev{margin:0;font:700 24px/32px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#121212}
.c-t{margin:36px 0 0;font:800 50px/54px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;color:#121212}
.c-m{margin:14px 0 0;font:400 22px/30px Inter,sans-serif;color:#4E535B}
.c-art{margin-top:28px}
.c-art svg{display:block}
.c-s{margin:auto 0 0;padding-top:24px;font:400 20px/28px Inter,sans-serif;color:#4E535B}
.c-cr{margin:6px 0 0;font:600 20px/28px Inter,sans-serif;color:#121212}
/* system sheet */
.ssec{margin-top:72px;padding-top:16px;border-top:2px solid var(--ink)}
.sh{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em}
.sh .sn{color:var(--sec)}
.sh3{margin:0 0 12px;font:800 22px/26px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em}
.sh3b{margin-top:28px}
.small{font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:52em}
.body2{font:400 17px/27px Inter,sans-serif;max-width:40em}
.anat-grid{display:grid;grid-template-columns:minmax(0,914px);gap:32px;align-items:start;margin-top:8px}
.anat{padding-left:48px}
.slotmark{position:absolute;left:-48px;top:0;display:flex;align-items:center;justify-content:center;width:24px;height:24px;background:#121212;color:#FFFFFF;font:700 13px/1 Inter,sans-serif}
.anat .slot::before{content:"";position:absolute;left:-14px;top:2px;bottom:2px;border-left:1px solid var(--ctx)}
.slk{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#121212;color:#FFFFFF;font:700 13px/1 Inter,sans-serif;margin-right:6px}
.st2 tbody th{font-weight:600}
.two-col{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;margin-top:8px}
.sizes{margin:0;padding:0;list-style:none}
.sizes li{padding:8px 0 10px;border-top:1px solid var(--grid)}
.szb{display:block;height:16px;background:#121212;margin-bottom:6px}
.szl{font:400 14px/20px Inter,sans-serif}
.steps{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;margin:16px 0 0;padding:0;list-style:none}
.steps li{display:grid;justify-items:center;gap:6px;font:600 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums}
.sp{display:block;background:#121212}
.brks{margin:0;padding-left:18px;font:400 14px/20px Inter,sans-serif;columns:2;column-gap:24px}
.ramp{margin:0;padding:0;list-style:none}
.ramp li{display:grid;grid-template-columns:180px 320px minmax(0,1fr);gap:16px;align-items:baseline;padding:12px 0;border-top:1px solid var(--grid)}
.ramp p{margin:0}
.tr-n{font:600 15px/22px Inter,sans-serif}.tr-sp{font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.ts-title{font:800 28px/32px "Inter Tight",Inter,sans-serif;letter-spacing:-.025em}
.ts-kind{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.ts-grade_words{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.ts-index{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.ts-measure{font:400 15px/23px Inter,sans-serif;color:var(--sec)}
.ts-big{font:800 96px/96px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;font-variant-numeric:tabular-nums;margin-left:-.04em}
.ts-series{font:600 15px/18px Inter,sans-serif}
.ts-data{font:600 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums}
.ts-note{font:400 13px/16px Inter,sans-serif;color:var(--sec)}
.ts-notes_slot{font:400 14px/20px Inter,sans-serif}
.ts-source{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.mklist{margin:0;padding:0;list-style:none}
.mklist li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;align-items:center;padding:10px 0;border-top:1px solid var(--grid);font:400 14px/20px Inter,sans-serif}
.mks{display:inline-block;vertical-align:middle;overflow:visible}
.gl-list li{grid-template-columns:24px minmax(0,1fr)}
.gtab td{vertical-align:middle}
.paltab td,.paltab th{vertical-align:middle}
.pal{display:inline-flex;gap:8px;align-items:center;white-space:nowrap}
.sw3{display:inline-block;width:28px;height:20px;box-shadow:inset 0 0 0 1px #5D636D}
.hx{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.cr{font:600 14px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
.pn{display:block;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.rule{margin:8px 0 24px;padding:4px 0 4px 16px;border-left:2px solid var(--ink);max-width:60em;font:400 15px/23px Inter,sans-serif}
.rule p{margin:0 0 8px}.rule footer{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.askbar{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;margin:16px 0 24px}
.tgl{min-height:44px;padding:0 16px;border:1.5px solid var(--ink);background:var(--gr);color:var(--ink);font:600 15px/1 Inter,sans-serif;cursor:pointer}
.tgl[aria-pressed="true"]{background:var(--ink);color:var(--gr)}
.askwrap{display:inline-flex;gap:12px;align-items:center}
.ask{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;background:#E63946;color:#FFFFFF;font:700 19px/1 Inter,sans-serif;text-decoration:none}
.ill{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.redmod{max-width:866px}
.rules,.readers{margin:8px 0 0;padding-left:32px;max-width:46em;font:400 16px/25px Inter,sans-serif}
.rules li,.readers li{margin-bottom:10px}
.code{margin:0 0 12px;padding:12px 14px;background:var(--alt);overflow-x:auto;font:400 13px/19px Inter,sans-serif;white-space:pre-wrap;max-width:60em}
code{font:inherit;font-weight:600}
.stillgrid{display:grid;grid-template-columns:minmax(0,682px) minmax(0,1fr);gap:40px;align-items:start;margin-top:8px}
.stillbox{overflow:auto;max-width:100%;width:max-content}
.chg{margin:0 0 12px;padding-left:20px;font:400 15px/23px Inter,sans-serif}.chg li{margin-bottom:8px}
.dtok{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 24px;margin:20px 0 0;padding:0;list-style:none;font:500 14px/20px Inter,sans-serif}
.dtok li{display:flex;gap:10px;align-items:center}
.sw2{flex:none;width:28px;height:18px;box-shadow:inset 0 0 0 1px #878A8F}
.dtn{margin:8px 0 0;font:500 13px/18px Inter,sans-serif;color:var(--sec)}
/* page widths */
@media (max-width:1299.98px){
 .spec-row>.mod,.spec-row>.strip{grid-column:1/-1}
 .spec-row>.strip{max-width:866px;margin-top:16px}
 .stillgrid{grid-template-columns:minmax(0,1fr)}
 .mindex ul{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:1099.98px){
 .vhead{grid-template-columns:minmax(0,1fr)}
 .ramp li{grid-template-columns:minmax(0,1fr);gap:4px}
}
@media (max-width:899.98px){
 .wrap{padding:0 16px}
 .mrow{grid-template-columns:1fr;gap:0;padding-top:4px}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{justify-content:space-between;gap:8px}
 .tabs a{font-size:14px;white-space:nowrap}
 .t-more{display:none}
 .vhead{padding-top:20px;gap:16px}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline,.sh{font-size:30px;line-height:34px}
 .deck{font-size:16px;line-height:24px;margin-top:8px}
 .deck-more,.vlinks,.mindex{display:none}
 .hs-h{font-size:20px;line-height:24px}
 .howto-s ul{font-size:14px;line-height:20px}
 .howto-s li{padding:3px 0}
 .specs{gap:56px;margin-top:24px}
 .mt{font-size:22px;line-height:26px;letter-spacing:-.02em}
 .sw button,.dl{min-height:44px}
 .src{flex-direction:column}.src .s2{text-align:left;max-width:none}
 .two-col{grid-template-columns:minmax(0,1fr)}
 .brks{columns:1}
 .anat{padding-left:0}
 .slotmark,.anat .slot::before{display:none}
 .dtok{grid-template-columns:minmax(0,1fr)}
 table.st2,table.st2 tbody,table.st2 tr,table.st2 th,table.st2 td{display:block;width:auto}
 table.st2 thead{display:none}
 table.st2 tr{border-top:1px solid var(--ink);padding:6px 0}
 table.st2 th,table.st2 td{border:0;padding:2px 0}
}
"""


def css():
    """The stylesheet with its container breakpoints read from CHART_TOKENS, so the artboards and reflows match the kit."""
    art, br = dict(CT['artboards']), CT['breaks']
    vals = {'art_p': art['p'], 'art_m': art['m'], 'art_w': art['w'], 'still': CT['still'],
            'table_reflow': br['table_reflow'] - 1, 'four_panels': br['four_panels'] - 1, 'two_panels': br['two_panels'] - 1}
    out = re.sub(r'§(\w+)§', lambda m: str(vals[m.group(1)]), CSS)
    assert '§' not in out
    return out

JS = r"""
(function(){
  var views=[].slice.call(document.querySelectorAll('[data-view-root]'));
  var ground={white:'g-white',newsprint:'g-news',dark:'g-dark',social:'g-white',system:'g-white'};
  var base=document.title, current=null;
  function rootOf(el){ return el && el.closest('[data-view-root]'); }
  function activate(v){
    current=v;
    views.forEach(function(e){ e.hidden = e.getAttribute('data-view-root')!==v; });
    document.body.className=ground[v];
    var r=document.querySelector('[data-view-root="'+v+'"]');
    document.title=(r.getAttribute('data-title')||v)+' · '+base;
    [].forEach.call(document.querySelectorAll('.tabs a'),function(a){
      if(a.getAttribute('href')==='#'+v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    return r;
  }
  function route(first){
    var h=location.hash.slice(1);
    var isView=views.some(function(e){return e.getAttribute('data-view-root')===h;});
    if(isView){
      var r=activate(h);
      if(!first){ window.scrollTo(0,0); var hd=r.querySelector('h1'); if(hd) hd.focus({preventScroll:true}); }
      return;
    }
    var el=h&&document.getElementById(h), r2=rootOf(el);
    if(r2){
      activate(r2.getAttribute('data-view-root'));
      var target=el.matches('figure')?el.querySelector('[data-role="title"]'):el;
      el.scrollIntoView();
      if(!first&&target&&target.focus) target.focus({preventScroll:true});
      return;
    }
    if(!current) activate('white');
  }
  window.addEventListener('hashchange',function(){route(false);});
  route(true);
  function save(name,type,text){
    var b=new Blob([text],{type:type}); var a=document.createElement('a');
    a.href=URL.createObjectURL(b); a.download=name; document.body.appendChild(a); a.click();
    setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();},800);
  }
  var P=['fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','stroke-dasharray','font-family','font-size','font-weight','letter-spacing','font-variant-numeric','text-anchor'];
  function svgText(s,title,desc){
    var hidden=s.closest('[hidden]'); if(hidden) hidden.hidden=false;
    var c=s.cloneNode(true), src=[s].concat([].slice.call(s.querySelectorAll('*'))), dst=[c].concat([].slice.call(c.querySelectorAll('*')));
    src.forEach(function(el,i){ var cs=getComputedStyle(el); P.forEach(function(p){ var v=cs.getPropertyValue(p); if(v) dst[i].style.setProperty(p,v); }); });
    if(hidden) hidden.hidden=true;
    var NS='http://www.w3.org/2000/svg';
    c.setAttribute('xmlns',NS); c.removeAttribute('style'); c.setAttribute('role','img');
    var t=document.createElementNS(NS,'title'); t.textContent=title;
    var d=document.createElementNS(NS,'desc'); d.textContent=desc;
    var bg=document.createElementNS(NS,'rect'); var vb=s.viewBox.baseVal;
    bg.setAttribute('x',vb.x); bg.setAttribute('y',vb.y); bg.setAttribute('width',vb.width); bg.setAttribute('height',vb.height);
    bg.setAttribute('fill',getComputedStyle(s.closest('.mod')).getPropertyValue('--gr').trim()||'#FFFFFF');
    c.insertBefore(bg,c.firstChild); c.insertBefore(d,c.firstChild); c.insertBefore(t,c.firstChild);
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+new XMLSerializer().serializeToString(c);
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-sw]');
    if(b){
      var m=b.closest('.mod'), want=b.getAttribute('data-sw');
      [].forEach.call(m.querySelectorAll('[data-sw]'),function(x){x.setAttribute('aria-pressed', x===b?'true':'false');});
      m.querySelector('.pane-c').hidden = want!=='c';
      m.querySelector('.pane-t').hidden = want!=='t';
      return;
    }
    var dl=e.target.closest('[data-dl]');
    if(dl){
      var cid=dl.getAttribute('data-for'), kind=dl.getAttribute('data-dl'), mod=dl.closest('.mod'), file=dl.getAttribute('data-file');
      if(kind==='csv'){ save(file+'.csv','text/csv;charset=utf-8',JSON.parse(document.getElementById('csv-'+cid).textContent)); }
      else{
        var w=mod.clientWidth, arts=[].slice.call(mod.querySelectorAll('svg.art'));
        arts.sort(function(a,b){return (+b.getAttribute('data-w'))-(+a.getAttribute('data-w'));});
        var pick=arts.filter(function(s){return +s.getAttribute('data-w')<=w+1;})[0]||arts[arts.length-1];
        if(pick) save(file+'.svg','image/svg+xml',svgText(pick,mod.getAttribute('data-title'),mod.getAttribute('data-desc')));
      }
      return;
    }
    var t=e.target.closest('[data-ask]');
    if(t){
      var on=t.getAttribute('aria-pressed')!=='true';
      t.setAttribute('aria-pressed',on?'true':'false');
      t.textContent=on?'Take the ask out of this view':'Put an ask in this view';
      document.getElementById(t.getAttribute('data-ask')).classList.toggle('stepdown',on);
      document.getElementById('ask-demo').hidden=!on;
    }
  });
  document.addEventListener('pointerover',function(e){
    var t=e.target.closest&&e.target.closest('[data-tip]'); if(!t) return;
    var m=t.closest('.mod'); var r=m&&m.querySelector('.readout'); if(r) r.textContent=t.getAttribute('data-tip');
  });
})();
"""


def build():
    pages = [masthead(), '<main id="main" tabindex="-1">', view_white(), view_newsprint(), view_dark(), view_social(), view_system(), '</main>']
    csvs = ''.join(f'<script type="application/json" id="csv-{c}">{json.dumps(csv_text(c)).replace("</", "<\\/")}</script>' for c in CHARTS)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="chart-views" content="white newsprint dark social system">'
            '<title>Chart system 03, Instrument</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{ground_css()}{css()}</style></head><body class="g-white">{"".join(pages)}{csvs}<script>{JS}</script></body></html>')
    if '—' in page:
        raise SystemExit('em dash in page')
    straight = len(re.findall(r"(?<=\w)'(?=\w)", re.sub(r'<(script|style|pre)[^>]*>.*?</\1>|<[^>]+>', ' ', page, flags=re.S)))
    if straight:
        PROBLEMS.append(f'{straight} straight apostrophes in page text')
    if PROBLEMS and '--draft' not in sys.argv:
        print(f'build_concept.py: {len(PROBLEMS)} layout or copy faults; nothing written. Run with --draft to write the page anyway.')
        for p in PROBLEMS[:200]:
            print('  - ' + p)
        raise SystemExit(1)
    OUT.write_text(page, encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)} ({len(page) // 1024} KB){", with " + str(len(PROBLEMS)) + " faults (draft)" if PROBLEMS else ""}')
    for p in PROBLEMS[:200]:
        print('  - ' + p)


if __name__ == '__main__':
    build()
