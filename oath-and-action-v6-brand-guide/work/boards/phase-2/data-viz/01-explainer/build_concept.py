"""Build chart system concept 01, Explainer, for the data visualization round (November 6, 2026; DR-44 to DR-51).

The concept leads with the finding. Every chart opens with its evidence label and a sentence title, then a measure
line, then a drawing with one Charcoal subject against Stone context and notes inside the plot that do the teaching.
Charts sit in one reading column, as in a newspaper explainer, and four break wider. Tables appear where a reader
would look something up.

Every chart is drawn by a generator function from the shared chart dataset, never by hand. A generator takes the
artboard width and returns an Art (an SVG drawing that measures its own labels with the Inter font files and refuses
to emit a label that collides with another or leaves the drawing). Each figure carries a wide artboard, a 600 px
artboard and a 320 px phone artboard; CSS container queries show the one that fits, so text keeps its set size.
Colors are CSS custom properties set per ground (White, Newsprint, Charcoal), so the same markup redraws on any
ground. These functions are the seed of the chart kit (DR-49).

Every value is read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json. Titles, measure lines and
notes are studio drafts.

Run from the project root:
    python3 -I work/boards/phase-2/data-viz/01-explainer/build_concept.py
Writes 20261106_Data-Viz-01-Explainer.html beside this file.
"""
import html
import json
import math
import pathlib
import re
from collections import Counter, defaultdict

from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SHARED = ROOT / 'work/boards/phase-2/data-viz/shared'
DATA = json.loads((SHARED / '20261106_Chart-Data.json').read_text())
LAB = json.loads((SHARED / '20261106_Palette-Lab.json').read_text())
TILES = json.loads((SHARED / 'geo/us-state-tile-grid.json').read_text())
OUT = HERE / '20261106_Data-Viz-01-Explainer.html'
DS = DATA['datasets']
SPECS = {s['id']: s for s in DATA['specimens']}
MINUS = '−'


def typo(s):
    """Typographic apostrophes and quotation marks in copy."""
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '\u2019', s)
    return re.sub(r'"([^"<>]*)"', '\u201c\\1\u201d', s)


def e(s):
    return html.escape(typo(str(s)), quote=True)


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def rows(did):
    return DS[did]['rows']


def row(did, key):
    return next(r for r in DS[did]['rows'] if r['key'] == key)


MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def date_words(iso):
    y, m, d = iso.split('-')
    return f'{MONTHS[int(m) - 1]} {int(d)}, {y}'


def iso_to_words(text):
    return re.sub(r'(\d{4})-(\d{2})-(\d{2})', lambda m: date_words(m.group(0)), text)


NUMW = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
        'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']


def nw(n, cap=False, start=False):
    """Numbers under ten in words; any number that opens a sentence in words."""
    w = NUMW[n] if (n < 10 or start) and n < len(NUMW) else str(n)
    return w.capitalize() if cap else w


def pct0(v):
    return f'{round(v):d}%'


# ------------------------------------------------------------------------------------------------ color
# Locked colors (Master Brief section 3), Deep Stone from the token architecture, Dim Newsprint from the palette lab.
WHITE, CHAR, NEWS, RED, PRUS, STONE, VERD = '#FFFFFF', '#121212', '#DCD9D2', '#E63946', '#1F2D5A', '#5D636D', '#4A7C74'
DEEP, DIM = '#4E535B', '#A3A19C'


def _h2r(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _delin(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklab(h):
    r, g, b = [_lin(c) for c in _h2r(h)]
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = [math.copysign(abs(x) ** (1 / 3), x) for x in (l_, m_, s_)]
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def from_oklab(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bb = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return '#' + ''.join(f'{round(max(0, min(1, _delin(c))) * 255):02X}' for c in (r, g, bb))


def mix(a, b, t):
    """Mix color a toward b by t in OKLab (D1-04)."""
    A, B = oklab(a), oklab(b)
    return from_oklab(*[x + (y - x) * t for x, y in zip(A, B)])


def lum(h):
    r, g, b = [_lin(c) for c in _h2r(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def gray(h):
    """Grayscale as the check's CSS filter draws it (luminance weights), for the grayscale proof."""
    r, g, b = _h2r(h)
    v = round((0.2126 * r + 0.7152 * g + 0.0722 * b) * 255)
    return f'#{v:02X}{v:02X}{v:02X}'


def ground_tokens(name):
    """Every chart color as a role on one ground. Tints are OKLab mixes of locked colors, each with one job."""
    if name == 'dark':
        return {
            'g': CHAR, 'ink': NEWS, 'sec': DIM, 'ctx': mix(STONE, NEWS, 0.35), 'lt': STONE, 'lt2': mix(STONE, CHAR, 0.55),
            'grid': mix(STONE, CHAR, 0.45), 'band': mix(STONE, CHAR, 0.72), 'vup': mix(VERD, NEWS, 0.30),
            'vup2': mix(VERD, CHAR, 0.35), 'sdn': STONE, 'sdn2': mix(STONE, CHAR, 0.45), 'red': RED,
            'chip': NEWS, 'chipfg': CHAR, 'rule': mix(STONE, NEWS, 0.35), 'inv': CHAR}
    gr = WHITE if name == 'white' else NEWS
    return {
        'g': gr, 'ink': CHAR, 'sec': DEEP, 'ctx': STONE, 'lt': mix(STONE, gr, 0.55), 'lt2': mix(STONE, gr, 0.88),
        'grid': mix(STONE, gr, 0.70), 'band': mix(STONE, WHITE, 0.94) if name == 'white' else mix(NEWS, WHITE, 0.45),
        'vup': mix(VERD, gr, 0.55), 'vup2': mix(VERD, gr, 0.80), 'sdn': mix(STONE, gr, 0.55), 'sdn2': mix(STONE, gr, 0.80),
        'red': RED, 'chip': CHAR, 'chipfg': gr, 'rule': STONE, 'inv': WHITE}


GROUNDS = {k: ground_tokens(k) for k in ('white', 'news', 'dark')}
ROLE_WORDS = {
    'ink': 'Subject: the series the title names, labels, baseline', 'sec': 'Secondary text: ticks, notes, measure and source lines',
    'ctx': 'Context marks: other series, leaders', 'lt': 'Light fill: a category under the subject; values printed',
    'lt2': 'Track: the whole a share sits in', 'grid': 'Gridline', 'band': 'Band: a stretch of time a note names',
    'vup': 'Diverging, up (Verdigris side)', 'vup2': 'Diverging, slightly up', 'sdn': 'Diverging, down (Stone side)',
    'sdn2': 'Diverging, flat or down', 'red': 'Pillar Red: the one point a title names'}
ROLE_MIX = {
    'white': {'lt': 'Stone 55% toward White', 'lt2': 'Stone 88% toward White', 'grid': 'Stone 70% toward White',
              'band': 'Stone 94% toward White', 'vup': 'Verdigris 55% toward White', 'vup2': 'Verdigris 80% toward White',
              'sdn': 'Stone 55% toward White', 'sdn2': 'Stone 80% toward White'},
    'news': {'lt': 'Stone 55% toward Newsprint', 'lt2': 'Stone 88% toward Newsprint', 'grid': 'Stone 70% toward Newsprint',
             'band': 'Newsprint 45% toward White', 'vup': 'Verdigris 55% toward Newsprint', 'vup2': 'Verdigris 80% toward Newsprint',
             'sdn': 'Stone 55% toward Newsprint', 'sdn2': 'Stone 80% toward Newsprint'},
    'dark': {'ctx': 'Stone 35% toward Newsprint', 'lt': 'Stone', 'lt2': 'Stone 55% toward Charcoal', 'grid': 'Stone 45% toward Charcoal',
             'band': 'Stone 72% toward Charcoal', 'vup': 'Verdigris 30% toward Newsprint', 'vup2': 'Verdigris 35% toward Charcoal',
             'sdn': 'Stone', 'sdn2': 'Stone 45% toward Charcoal', 'sec': 'Dim Newsprint (palette lab)'}}


def css_vars(name):
    t = GROUNDS[name]
    return ';'.join(f'--{k}:{v}' for k, v in t.items())


# ------------------------------------------------------------------------------------------------ text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200, layout_engine=ImageFont.Layout.RAQM)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False, track=0.0):
    """Rendered width of a string in Inter (tabular figures), the way the page sets it."""
    w = _font(weight).getlength(text, features=['tnum']) * size / 200
    if tight:
        w *= 0.955     # Inter Tight runs about 4.5 percent narrower than Inter at the same weight
    return w + track * size * max(len(text) - 1, 0)


def wrap(text, width, size, weight=400):
    out, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if line and tw(trial, size, weight) > width:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


def spread(ideal, size, lo, hi, gap=0.0):
    """Place intervals near their ideal centers without overlap, inside [lo, hi]. Returns the centers.
    Used for labels that must stack along one axis (end labels, notes, timeline labels on phones)."""
    order = sorted(range(len(ideal)), key=lambda i: ideal[i])
    blocks = []
    for i in order:
        blocks.append({'items': [i]})
        while True:
            b = blocks[-1]
            offs, acc = 0.0, 0.0
            for k in b['items']:
                acc += ideal[k] - size[k] / 2 - offs
                offs += size[k] + gap
            total = offs - gap
            start = max(lo, min(hi - total, acc / len(b['items'])))
            b['start'], b['total'] = start, total
            if len(blocks) > 1 and blocks[-2]['start'] + blocks[-2]['total'] + gap > start + 1e-6:
                prev = blocks.pop(-2)
                b['items'] = prev['items'] + b['items']
                continue
            break
    out = [0.0] * len(ideal)
    for b in blocks:
        y = b['start']
        for k in b['items']:
            out[k] = y + size[k] / 2
            y += size[k] + gap
    return out


# ------------------------------------------------------------------------------------------------ the drawing kit
class Type:
    """Type sizes for one artboard. Phone artboards (under 600 px) set nothing under 14 px so a 320 px drawing
    holds 13 px on a 304 px column; the tile map's state codes are the one 13 px exception."""

    def __init__(self, W, scale=1.0):
        narrow = W < 600
        self.narrow = narrow
        self.s = scale
        self.lbl = 15 * scale if not narrow else 14
        self.tk = 13 * scale if not narrow else 14
        self.nt = 14 * scale if not narrow else 14
        self.lh = round(self.nt * 1.36)
        self.eb = 13 * scale if not narrow else 13


class Art:
    """One SVG artboard. Every text call measures the label; render() refuses collisions and labels outside."""

    def __init__(self, W, uid, t=None):
        self.W, self.uid = W, uid
        self.t = t or Type(W)
        self.out, self.defs, self.boxes = [], [], []
        self.anchors = {}

    # text -------------------------------------------------------------------------------------------
    def text(self, x, y, s, size, cls='tl', weight=600, anchor='start', attrs='', tight=False, track=0.0, box=True):
        w = tw(s, size, weight, tight, track)
        x0 = {'start': x, 'middle': x - w / 2, 'end': x - w}[anchor]
        if box:
            self.boxes.append((x0, y - 0.97 * size, x0 + w, y + 0.25 * size, s))
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        self.out.append(f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{f(size)}"{a}{attrs}>{e(s)}</text>')
        return w

    def rich(self, x, y, parts, size, anchor='start', attrs=''):
        """One line in mixed weights: parts are (text, class, weight)."""
        w = sum(tw(p[0], size, p[2]) for p in parts)
        x0 = {'start': x, 'middle': x - w / 2, 'end': x - w}[anchor]
        self.boxes.append((x0, y - 0.97 * size, x0 + w, y + 0.25 * size, ''.join(p[0] for p in parts)))
        spans = ''.join(f'<tspan class="{p[1]}">{e(p[0])}</tspan>' for p in parts)
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        self.out.append(f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}"{a}{attrs}>{spans}</text>')
        return w

    def block(self, x, y, lines, size, cls, weight, lh, tight=False, attrs=''):
        """Several lines set as one <text> with tspans, for display type set tighter than its text box."""
        w = max(tw(ln, size, weight, tight) for ln in lines)
        self.boxes.append((x, y - 0.97 * size, x + w, y + (len(lines) - 1) * lh + 0.25 * size, ' '.join(lines)))
        sp = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else f(lh)}">{e(ln)}</tspan>' for i, ln in enumerate(lines))
        self.out.append(f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{f(size)}"{attrs}>{sp}</text>')
        return y + (len(lines) - 1) * lh

    def para(self, x, y, s, width, size=None, cls='tn', weight=400, lh=None, anchor='start'):
        """Wrapped note text, one <text> per line. Returns the baseline of the last line."""
        size = size or self.t.nt
        lh = lh or round(size * 1.36)
        lines = wrap(s, width, size, weight)
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size, cls, weight, anchor)
        return y + (len(lines) - 1) * lh

    def para_h(self, s, width, size=None, weight=400, lh=None):
        size = size or self.t.nt
        lh = lh or round(size * 1.36)
        return len(wrap(s, width, size, weight)), lh

    # shapes -----------------------------------------------------------------------------------------
    def rect(self, x, y, w, h, cls, attrs=''):
        self.out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(max(w, 0))}" height="{f(h)}" class="{cls}"{attrs}/>')

    def line(self, x1, y1, x2, y2, cls, attrs=''):
        self.out.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{cls}"{attrs}/>')

    def path(self, d, cls, attrs=''):
        self.out.append(f'<path d="{d}" class="{cls}"{attrs}/>')

    def circle(self, cx, cy, r, cls, attrs=''):
        self.out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="{cls}"{attrs}/>')

    def raw(self, s):
        self.out.append(s)

    def leader(self, pts, cls='s-ld'):
        self.path('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts), cls)

    def hatch(self, name='hatch', gap=5, ln='p-ln'):
        pid = f'{self.uid}-{name}'
        if not any(pid in d for d in self.defs):
            self.defs.append(f'<pattern id="{pid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse" '
                             f'patternTransform="rotate(45)"><rect width="{gap}" height="{gap}" class="p-bg"/>'
                             f'<line x1="0" y1="0" x2="0" y2="{gap}" class="{ln}"/></pattern>')
        return f'url(#{pid})'

    # output -----------------------------------------------------------------------------------------
    def check(self, H):
        bad = []
        for (x0, y0, x1, y1, s) in self.boxes:
            if x0 < -0.5 or x1 > self.W + 0.5 or y0 < -0.5 or y1 > H + 0.5:
                bad.append(f'outside: "{s}" ({x0:.1f},{y0:.1f},{x1:.1f},{y1:.1f}) in {self.W}x{H}')
        bx = self.boxes
        for i in range(len(bx)):
            for j in range(i + 1, len(bx)):
                a, b = bx[i], bx[j]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                    bad.append(f'overlap: "{a[4]}" and "{b[4]}"')
        if bad:
            raise AssertionError(f'{self.uid}: ' + '; '.join(bad[:8]))

    def render(self, H, label, cls, view_name):
        H = math.ceil(H)
        self.check(H)
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        return (f'<svg class="{cls}" data-view="{e(view_name)}" width="{self.W}" height="{H}" viewBox="0 0 {self.W} {H}" '
                f'role="img" aria-label="{e(label)}" focusable="false">{defs}{"".join(self.out)}</svg>')


def da(key=None, value=None, field=None, mark=None, axis=None, scale=None, cat=None):
    """The verifier's data contract as attributes."""
    a = []
    if key is not None:
        a.append(f' data-key="{e(key)}"')
    if field is not None:
        a.append(f' data-field="{e(field)}"')
    if value is not None:
        a.append(f' data-value="{f(value) if isinstance(value, float) else value}"')
    if cat is not None:
        a.append(f' data-category="{e(cat)}"')
    if mark is not None:
        a.append(f' data-mark="{mark}"')
    if axis is not None:
        a.append(f' data-axis="{axis}"')
    if scale is not None:
        a.append(f' data-scale="{e(scale)}"')
    return ''.join(a)


def key_item(art, x, y, kind, label, size, uid_suffix=''):
    """A key swatch drawn in the chart's own encoding, then its words. Returns the width used."""
    sw = 14
    top = y - 11
    if kind == 'ink':
        art.rect(x, top, sw, sw, 'f-ink')
    elif kind == 'ctx':
        art.rect(x, top, sw, sw, 'f-ctx')
    elif kind == 'lt':
        art.rect(x, top, sw, sw, 'f-lt')
    elif kind == 'lt2':
        art.rect(x, top, sw, sw, 'f-lt2')
    elif kind == 'hatch':
        art.rect(x + 0.75, top + 0.75, sw - 1.5, sw - 1.5, 's-ctx15h', f' style="fill:{art.hatch()}"')
    elif kind == 'dash':
        art.rect(x + 0.75, top + 0.75, sw - 1.5, sw - 1.5, 's-dash')
    elif kind == 'half':
        art.rect(x + 0.75, top + 0.75, sw - 1.5, sw - 1.5, 's-ctx15 f-g')
        art.path(f'M{f(x + 0.75)} {f(top + sw - 0.75)}L{f(x + sw - 0.75)} {f(top + 0.75)}L{f(x + sw - 0.75)} {f(top + sw - 0.75)}Z', 'f-ctx')
    elif kind == 'some':
        art.rect(x + 1, top + 1, sw - 2, sw - 2, 's-ink2 f-g')
        art.rect(x + 1, top + sw - 5, sw - 2, 4, 'f-ink')
    w = art.text(x + sw + 7, y, label, size, 'tr', 400)
    return sw + 7 + w


def flow_key(art, x0, y0, items, width, size, gap=22, lh=24):
    """Lay key items left to right, wrapping inside the width. Returns the baseline of the last row."""
    x, y = x0, y0
    for kind, label in items:
        w = 14 + 7 + tw(label, size, 400)
        if x > x0 and x + w > x0 + width:
            x, y = x0, y + lh
        key_item(art, x, y, kind, label, size)
        x += w + gap
    return y


# ------------------------------------------------------------------------------------------------ S01 big number
def gen_s01(W, uid, t=None, compact=False):
    """Big number in context: one figure large, the party figures beside it on a 0 to 100 track, then the votes.
    compact drops the two notes for the social card, whose measure line carries the survey date."""
    a = Art(W, uid, t)
    t = a.t
    R = {r['key']: r for r in rows('stock-trading-ban')}
    narrow = W < 600
    s = t.s
    big = 116 * s if not narrow else 88
    lbl = t.lbl
    # the large figure
    yb = big * 0.98
    a.text(0, yb, f'{R["support-all"]["value"]}%', big, 'tb', 800, tight=True,
           attrs=da('support-all', R['support-all']['value'], mark='label'))
    a.anchors['big'] = (0, yb - big * 0.5)
    lw = 250 * s if not narrow else W
    y = yb + 0.25 * big + 22 * s
    y = a.para(0, y, 'of registered voters favored a ban on stock trading by members of Congress', lw, lbl + 1 * s, 'tl', 600, round((lbl + 1 * s) * 1.4))
    if not compact:
        y += 26 * s
        y = a.para(0, y, 'Survey of 2,625 registered voters, May 19 to 30, 2023, three years before either vote.', lw, t.nt, 'tn', 400)
    left_bottom = y
    # the party figures (DR-48: neutral inks, names printed on the marks, ordered by value)
    if narrow:
        x0, rw, ytop = 0, W, left_bottom + 36
    else:
        x0 = 330 * s
        rw, ytop = W - x0, 22 * s
    a.text(x0, ytop, 'BY PARTY', t.eb, 'te', 700, track=0.06)
    parties = sorted([R['support-democrats'], R['support-republicans']], key=lambda r: (-r['value'], r['group']))
    y = ytop + 34 * s
    bh = 24 * s
    for r in parties:
        g = []
        name = r['group']
        a.raw(f'<g data-party="{e(name)}">')
        a.text(x0, y, name, lbl, 'tl', 600)
        a.rect(x0, y + 9 * s, rw, bh, 'f-lt2')
        bw = rw * r['value'] / 100
        a.rect(x0, y + 9 * s, bw, bh, 'f-ink', da(r['key'], r['value'], mark='bar', axis='x'))
        a.text(x0 + bw - 8 * s, y + 9 * s + bh / 2 + lbl * 0.36, f'{r["value"]}%', lbl, 'ti', 600, 'end',
               attrs=da(r['key'], r['value'], mark='label'))
        a.raw('</g>')
        y += 9 * s + bh + 32 * s
    yt = y - 32 * s + 22 * s
    a.text(x0, yt, '0', t.tk, 'tk', 400)
    a.text(x0 + rw, yt, '100%', t.tk, 'tk', 400, 'end')
    if not narrow and not compact:
        a.para(x0, yt + 30 * s, 'The two parties sit one point apart, and the bars run from 0 to 100 percent.', rw, t.nt, 'tn', 400)
    bottom = max(left_bottom, yt + (52 * s if not narrow and not compact else 0))
    # what Congress did
    yd = bottom + 34 * s
    a.line(0, yd, W, yd, 's-grid')
    y = yd + 34 * s
    a.text(0, y, 'WHAT CONGRESS DID NEXT', t.eb, 'te', 700, track=0.06)
    y += 36 * s
    for ch in ('house', 'senate'):
        yes, no = R[f'{ch}-yes'], R[f'{ch}-no']
        tot = yes['value'] + no['value']
        if ch == 'house':
            head, when = 'The House passed the ban', 'July 22, 2026'
        else:
            head, when = 'The Senate vote to take it up fell short', 'September 30, 2026'
        score = f'{yes["value"]} to {no["value"]}'
        if narrow:
            a.text(0, y, head, lbl, 'tl', 600)
            y += 20
            a.text(0, y, when, t.tk, 'tk', 400)
            a.text(W, y, score, lbl, 'tl', 600, 'end')
        else:
            hw = a.text(0, y, head, lbl, 'tl', 600)
            a.text(hw + 10 * s, y, when, t.tk, 'tk', 400)
            a.text(W, y, score, lbl, 'tl', 600, 'end')
        yb2 = y + 10 * s
        gap = 2
        k = (W - gap) / tot
        wy, wn = yes['value'] * k, no['value'] * k
        a.rect(0, yb2, wy, bh, 'f-ink', da(yes['key'], yes['value'], mark='bar', axis='x', scale=ch))
        a.rect(wy + gap, yb2, wn, bh, 'f-lt', da(no['key'], no['value'], mark='bar', axis='x', scale=ch))
        a.text(8 * s, yb2 + bh / 2 + lbl * 0.36, f'{yes["value"]} for', lbl, 'ti', 600)
        a.text(W - 8 * s, yb2 + bh / 2 + lbl * 0.36, f'{no["value"]} against', lbl, 'tl', 600, 'end')
        y = yb2 + bh
        if ch == 'senate':
            need = R['senate-needed']['value']
            xn = need * k + gap
            xy = wy
            a.line(xn, yb2 - 7 * s, xn, y + 14 * s, 's-mark', da('senate-needed', need, mark='point', axis='x', scale='senate'))
            yk = y + 14 * s
            a.path(f'M{f(xy)} {f(y + 6 * s)}V{f(yk)}H{f(xn)}', 's-ld')
            short = f'{need - yes["value"]} votes short of the {need} needed'
            sw_ = tw(short, lbl, 600)
            if xy + sw_ <= W:
                a.text(xy, yk + 20 * s, short, lbl, 'tl', 600)
            else:
                a.text(max(0, W - sw_), yk + 20 * s, short, lbl, 'tl', 600)
            y = yk + 26 * s
        y += 42 * s
    return a, y - 42 * s + 6


# ------------------------------------------------------------------------------------------------ S02 line with events
def line_segments(rws, year_key='year'):
    """Split a series at method breaks: a break year has an 'earlier' row that ends a segment and a 'later' row
    that starts the next. Never bridges a break (R16)."""
    by = defaultdict(list)
    for r in rws:
        by[r[year_key]].append(r)
    segs, cur = [], []
    for y in sorted(by):
        rs = by[y]
        if len(rs) == 1:
            cur.append(rs[0])
        else:
            early = next(r for r in rs if r['comparable_with'] == 'earlier')
            late = next(r for r in rs if r['comparable_with'] == 'later')
            cur.append(early)
            segs.append(cur)
            cur = [late]
    segs.append(cur)
    return segs


def gen_s02(W, uid, t=None, red=True, anatomy=False):
    """Line with event notes: the Supplemental Poverty Measure for children in Charcoal, the official measure in
    Stone, method breaks drawn as steps, and notes at 2021 and 2022."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    D = rows('child-poverty-spm')
    spm = [r for r in D if r['measure'] == 'spm']
    off = [r for r in D if r['measure'] == 'official']
    gut = 40
    top = 18 if not narrow else 50
    ph = 300 if not narrow else 250
    x0, x1 = gut + 14, W - (52 if not narrow else 46)
    yb = top + ph

    def X(yr):
        return x0 + (yr - 2009) / (2025 - 2009) * (x1 - x0)

    def Y(v):
        return yb - v / 25 * ph
    for v in (0, 5, 10, 15, 20, 25):
        if v:
            a.line(gut, Y(v), W, Y(v), 's-grid')
        a.text(gut - 6, Y(v) + 4.5, f'{v}%' if v == 25 else str(v), t.tk, 'tk', 400, 'end')
    a.line(gut, yb, W, yb, 's-base')
    a.anchors.update(m4=(gut + 10, Y(25)), m5=(X(2011), Y(10)), m6=(X(2010), yb - 13))
    for yr in (2009, 2013, 2017, 2021, 2025):
        a.text(X(yr), yb + 20, str(yr), t.tk, 'tk', 400, 'middle')

    def draw(series, cls, r_dot, dot_cls, keyed=True):
        for seg in line_segments(series):
            pts = [(X(r['year']), Y(r['percent'])) for r in seg]
            if len(pts) > 1:
                a.path('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts), cls)
            for r, (x, y) in zip(seg, pts):
                if red and r['key'] == 'spm|2021|standard':
                    continue
                a.circle(x, y, r_dot, dot_cls, da(r['key'], r['percent'], mark='point', axis='y') if keyed else '')
    draw(off, 's-ctx', 2.25, 'f-ctx')
    draw(spm, 's-sub', 3, 'f-ink')
    p21 = row('child-poverty-spm', 'spm|2021|standard')
    cx, cy = X(2021), Y(p21['percent'])
    if red:
        job = 'specimen' if anatomy else 'working'
        a.raw(f'<g data-red="{job}" data-red-job="the 2021 low the title names">')
        a.circle(cx, cy, 6.5, 'redpt', da(p21['key'], p21['percent'], mark='point', axis='y'))
        a.raw('</g>')
    else:
        a.circle(cx, cy, 6.5, 'f-ink s-gring', da(p21['key'], p21['percent'], mark='point', axis='y'))
    a.anchors['m9'] = (cx + 20, cy)
    # direct labels for the two series, in open space at the left
    o10 = next(r for r in off if r['year'] == 2010)
    s11 = next(r for r in spm if r['year'] == 2011)
    if not narrow:
        wo = a.text(X(2009), Y(o10['percent']) - 12, 'Official measure', t.lbl, 'ts', 600)
        ws = a.text(X(2009) + 2, Y(18) - 10, 'Supplemental measure', t.lbl, 'tl', 600)
        a.anchors['m8'] = (X(2009) + wo + 18, Y(o10['percent']) - 17)
        a.anchors['m7'] = (X(2009) + 2 + ws + 18, Y(18) - 15)
    else:
        # on a phone the lines run too close for labels at the line, so a key in the chart's own marks
        ky = 16
        a.line(gut + 10, ky - 5, gut + 34, ky - 5, 's-sub')
        ws = a.text(gut + 40, ky, 'Supplemental', t.lbl, 'tl', 600)
        a.line(gut + 52 + ws, ky - 5, gut + 76 + ws, ky - 5, 's-ctx')
        wo = a.text(gut + 82 + ws, ky, 'Official', t.lbl, 'ts', 600)
        a.anchors['m7'] = (gut - 5, ky - 5)
        a.anchors['m8'] = (gut + 64 + ws, ky + 17)
    # the low point the title names, labeled under the point
    a.text(cx, cy + 25, f'{p21["percent"]}%', t.lbl, 'tl', 600, 'middle')
    p22 = row('child-poverty-spm', 'spm|2022|standard')
    x22, y22 = X(2022), Y(p22['percent'])
    n21 = '2021: the expanded child tax credit was in force. Census reads a change between years as a description, not the effect of one policy.'
    n2 = f'2022: {p22["percent"]}%, after the expanded credit lapsed.'
    if not narrow:
        # 2021 note in the open space below the line, left of the dip
        nw = 250
        nx = X(2019.55) - nw
        nl, lh = a.para_h(n21, nw)
        ny = yb - 12 - (nl - 1) * lh
        a.para(nx, ny, n21, nw)
        a.leader([(nx + nw + 2, ny - 5), (cx - 7, cy + 1)])
        a.anchors['m10'] = (nx - 16, ny - 5)
        # 2022 note below the line at right
        nx2 = x22 + 10
        nw2 = W - nx2
        nl2, lh2 = a.para_h(n2, nw2)
        ny2 = y22 + 34
        assert ny2 + (nl2 - 1) * lh2 < cy - 4
        a.para(nx2, ny2, n2, nw2)
        a.leader([(x22 + 4, ny2 - 5), (x22 + 1, y22 + 7)])
    # both measures land on 13.4 in 2025: one end label, in the empty top right
    p25 = row('child-poverty-spm', 'spm|2025|standard')
    o25 = next(r for r in off if r['year'] == 2025)
    assert p25['percent'] == o25['percent']
    xe, ye = X(2025), Y(p25['percent'])
    end_txt = f'Both measures: {p25["percent"]}% in 2025' if not narrow else f'Both: {p25["percent"]}% in 2025'
    ew = tw(end_txt, t.lbl, 600)
    ex = min(W - ew, xe - ew + 30) if not narrow else W - ew
    ey = Y(21.6) if not narrow else Y(23.2)
    a.text(ex, ey, end_txt, t.lbl, 'tl', 600)
    a.leader([(xe, ey + 7), (xe, ye - 7)])
    a.anchors['m12'] = (ex - 16, ey - 5) if not narrow else (W - 11, ey - 22)
    # the encoding a reader could misread: method breaks
    yn = yb + 50
    step_x = 6
    a.circle(step_x, yn - 9, 3, 'f-ink')
    a.circle(step_x, yn + 2, 3, 'f-ink')
    bt = ('Census changed its survey or method in 2013, 2017 and 2019. The line breaks there, '
          'and each of those years shows two estimates, one for each method.')
    last = a.para(20, yn, bt, W - 20)
    if narrow:
        nw_ = W - 28 if anatomy else W
        a.anchors['m10'] = (W - 11, last + 25)
        last = a.para(0, last + 30, n21, nw_)
        last = a.para(0, last + 26, n2, nw_)
    a.anchors['m11'] = (X(2017) + 16, Y(12.2) if not narrow else Y(10.4))
    return a, last + 10


# ------------------------------------------------------------------------------------------------ S03 ranked bar
DIR_ORDER = ['away from voters', 'toward voters', 'voters kept existing rules', 'mixed', 'pending']
DIR_KIND = {'away from voters': 'ink', 'toward voters': 'ctx', 'voters kept existing rules': 'lt', 'mixed': 'hatch', 'pending': 'dash'}
DIR_WORD = {'away from voters': 'Away from voters', 'toward voters': 'Toward voters',
            'voters kept existing rules': 'Voters kept existing rules', 'mixed': 'Mixed', 'pending': 'Pending'}


def seg_rect(a, x, y, w, h, kind, attrs):
    if kind == 'ink':
        a.rect(x, y, w, h, 'f-ink', attrs)
    elif kind == 'ctx':
        a.rect(x, y, w, h, 'f-ctx', attrs)
    elif kind == 'lt':
        a.rect(x, y, w, h, 'f-lt', attrs)
    elif kind == 'hatch':
        a.rect(x, y, w, h, 'hatchf', f' style="fill:{a.hatch()}"' + attrs)
        a.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 's-ctx15 nofill')
    elif kind == 'dash':
        a.rect(x, y, w, h, 'nofill', attrs)
        a.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 's-dash')


def gen_s03(W, uid, t=None):
    """Ranked bar: instruments ranked by how many entries they made in the repair log, each bar split by the
    atlas's direction code, away from voters at the baseline because the title names it."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    D = rows('rule-changes-by-instrument')
    D = sorted(D, key=lambda r: -r['value'])
    lbl = t.lbl
    yk = flow_key(a, 0, 16, [(DIR_KIND[d], DIR_WORD[d]) for d in DIR_ORDER], W, t.tk + 1 if not narrow else 14)
    vmax = max(r['value'] for r in D)
    if narrow:
        BX, NOTE_W = 0, 0
        bar_w = W - 34
    else:
        LW = max(tw(r['key'], lbl, 600) for r in D) + 16
        NOTE_W = 196
        BX = LW
        bar_w = W - BX - NOTE_W - 44
    k = bar_w / vmax
    bh = 24 if not narrow else 20
    pitch = 42 if not narrow else 58
    y = yk + (34 if not narrow else 30)
    first = y
    rowy = {}
    for r in D:
        if narrow:
            a.text(0, y, r['key'], lbl, 'tl', 600)
            by = y + 8
        else:
            by = y - bh / 2 - 5
            a.text(0, y, r['key'], lbl, 'tl', 600)
        x = BX
        for d in DIR_ORDER:
            v = r[d]
            if not v:
                continue
            w = v * k
            seg_rect(a, x, by, w, bh, DIR_KIND[d], da(r['key'], v, field=d, mark='bar', axis='x'))
            if w >= 20:
                cls = 'ti' if DIR_KIND[d] in ('ink', 'ctx') else 'tl'
                a.text(x + w / 2, by + bh / 2 + lbl * 0.36, str(v), lbl - 1, cls, 600, 'middle')
            x += w
        a.text(BX + r['value'] * k + 8, by + bh / 2 + lbl * 0.36, str(r['value']), lbl, 'tl', 600,
               attrs=da(r['key'], r['value'], mark='label'))
        rowy[r['key']] = (by, by + bh, BX + r['value'] * k + 8 + tw(str(r['value']), lbl, 600))
        y += pitch
    last_bar = rowy[D[-1]['key']][1]
    a.line(BX, rowy[D[0]['key']][0] - 6, BX, last_bar + 6, 's-base')
    bi, ss = row('rule-changes-by-instrument', 'Ballot initiative'), row('rule-changes-by-instrument', 'State statute')
    notes = [
        ('Ballot initiative', f'None of the {bi["value"]} initiatives moved the rules away from voters. '
                              f'{nw(bi["voters kept existing rules"], cap=True)} failed, which left the rules in force.'),
        ('State statute', f'{nw(ss["away from voters"], cap=True, start=True)} of {ss["value"]} statutes moved the rules away from voters, '
                          'the largest share of any instrument.'),
        ('Executive or agency action', 'The studio grouped an agency rule, an executive action and an executive order, '
                                       'and a city law with a council funding vote.'),
    ]
    if not narrow:
        nx = W - NOTE_W
        heights, ideals, items = [], [], []
        for key, txt in notes:
            n, lh = a.para_h(txt, NOTE_W)
            heights.append(n * lh)
            by0, by1, _ = rowy[key]
            ideals.append(by0 - 6 + n * lh / 2 if key != 'Executive or agency action' else (by0 + rowy['Local law or funding vote'][1]) / 2)
            items.append((key, txt, n, lh))
        cs = spread(ideals, heights, 0, 2000, 10)
        for (key, txt, n, lh), c, h in zip(items, cs, heights):
            ytop = c - h / 2
            a.para(nx, ytop + t.nt, txt, NOTE_W)
            by0, by1, xe = rowy[key]
            ym = (by0 + by1) / 2
            if key == 'Executive or agency action':
                for kk in ('Executive or agency action', 'Local law or funding vote'):
                    b0, b1, xe2 = rowy[kk]
                    a.leader([(xe2 + 6, (b0 + b1) / 2), (nx - 8, (b0 + b1) / 2)])
            else:
                a.leader([(xe + 6, ym), (nx - 8, ym)])
        H = max(last_bar + 14, max(c + h / 2 for c, h in zip(cs, heights)) + 8)
    else:
        y = last_bar + 34
        for key, txt in notes:
            y = a.para(0, y, txt, W) + 26
        H = y - 26 + 8
    return a, H


# ------------------------------------------------------------------------------------------------ S04 dumbbell
AGE_WORD = {'18_to_24': '18 to 24', '25_to_44': '25 to 44', '45_to_64': '45 to 64', '65_and_over': '65 and over'}


def gen_s04(W, uid, t=None):
    """Dot plot with two elections per row: 2020 open, 2024 filled, the change in words and numbers."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    base = 'citizen_voting_age_population'
    R = {(r['age_group'], r['year']): r for r in rows('turnout-by-age') if r['base'] == base}
    groups = ['18_to_24', '25_to_44', '45_to_64', '65_and_over']
    lo, hi = 40, 80
    if narrow:
        LX, x0, x1 = 0, 12, W - 12
    else:
        LX = 0
        x0, x1 = 128, W - 176
    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    y = 18
    for v in range(lo, hi + 1, 10):
        anc = 'middle' if not narrow or lo < v < hi else ('start' if v == lo else 'end')
        a.text(X(v) + (-6 if narrow and v == lo else 6 if narrow and v == hi else 0), y, f'{v}%' if v == hi else str(v), t.tk, 'tk', 400, anc)
    y += 50 if not narrow else 30
    pitch = 54 if not narrow else 76
    r_dot = 6.5
    first = True
    for g in groups:
        r0, r1 = R[(g, 2020)], R[(g, 2024)]
        v0, v1 = r0['voted_pct'], r1['voted_pct']
        ch = round(v1 - v0, 1)
        word = ('Down' if ch < 0 else 'Up') + f' {abs(ch):.1f} points'
        if narrow:
            a.text(0, y, AGE_WORD[g], t.lbl, 'tl', 600)
            a.text(W, y, word, t.lbl, 'tl', 600, 'end')
            cy = y + (40 if first else 26)
        else:
            cy = y
            a.text(0, cy + 5, AGE_WORD[g], t.lbl, 'tl', 600)
            a.text(W, cy + 5, word, t.lbl, 'tl', 600, 'end')
        a.line(x0, cy, x1, cy, 's-grid')
        xa, xb = X(v0), X(v1)
        if abs(xa - xb) > 2 * r_dot:
            a.line(min(xa, xb) + r_dot, cy, max(xa, xb) - r_dot, cy, 's-ctx')
        a.circle(xb, cy, r_dot, 'f-ink', da(r1['key'], v1, mark='point', axis='x'))
        a.circle(xa, cy, r_dot - 1, 's-ring2', da(r0['key'], v0, mark='point', axis='x'))
        # values: the lower one to the left, the higher to the right
        lo_k, hi_k = ((r1, xb), (r0, xa)) if v1 < v0 else ((r0, xa), (r1, xb))
        for (rr, xx), side in ((lo_k, 'end'), (hi_k, 'start')):
            cls = 'tl' if rr['year'] == 2024 else 'ts'
            dx = -(r_dot + 6) if side == 'end' else r_dot + 6
            a.text(xx + dx, cy + 5, f'{rr["voted_pct"]}', t.lbl if not narrow else 14, cls, 600, side,
                   attrs=da(rr['key'], rr['voted_pct'], mark='label'))
        if first:
            (rl, xl), (rr_, xr_) = sorted(((r0, xa), (r1, xb)), key=lambda q: q[1])
            a.text(xl + 7, cy - 16, str(rl['year']), t.tk, 'tl' if rl['year'] == 2024 else 'ts', 600, 'end')
            a.text(xr_ - 7, cy - 16, str(rr_['year']), t.tk, 'tl' if rr_['year'] == 2024 else 'ts', 600, 'start')
            first = False
        y = cy + pitch if not narrow else cy + 46
    # the gap the title names, and the survey caution
    g20 = R[('65_and_over', 2020)]['voted_pct'] - R[('18_to_24', 2020)]['voted_pct']
    g24 = R[('65_and_over', 2024)]['voted_pct'] - R[('18_to_24', 2024)]['voted_pct']
    y = y - (pitch if not narrow else 46) + 44
    y = a.para(0, y, f'The gap between citizens 18 to 24 and those 65 and over: {g20:.1f} points in 2020, {g24:.1f} in 2024.',
               W if narrow else W - 40, t.nt, 'th', 600) + 26
    y = a.para(0, y, 'These rates are what people told a Census survey, which runs higher than counted ballots. '
                     'The table gives no margins of error, so a change of a point or two may sit within survey error.',
               W if narrow else W - 40)
    return a, y + 8


# ------------------------------------------------------------------------------------------------ S05 small multiples
HO_GROUP = {'all_households': 'All households', 'non_hispanic_white': 'Non-Hispanic White', 'black': 'Black',
            'hispanic': 'Hispanic (any race)'}


def ho_segments(g):
    """Annual homeownership for one group, split where the Census changed its method: 2002 has an original and a
    revised estimate (reweighted to the 2000 Census); Black and non-Hispanic White change race categories in 2003."""
    rs = sorted([r for r in rows('homeownership-by-race') if r['group'] == g], key=lambda r: r['year'])
    a_ = [r for r in rs if r['year'] < 2002 or (r['year'] == 2002 and r['series_variant'] == 'original')]
    b_ = [r for r in rs if r['year'] > 2002]
    rev = next(r for r in rs if r['year'] == 2002 and r['series_variant'] == 'revised_2000_census')
    if g in ('all_households', 'hispanic'):
        b_ = [rev] + b_
        lone = []
    else:
        lone = [rev]
    return [a_, b_], lone


def gen_s05(W, uid, t=None):
    """Small multiples: one panel per group on one 40 to 80 percent scale; each panel draws its group in Charcoal
    over the others in Stone. Brackets in two panels give the gap the title names."""
    a = Art(W, uid, t)
    t = a.t
    order = ['all_households', 'non_hispanic_white', 'hispanic', 'black']
    last = {g: [r for r in rows('homeownership-by-race') if r['group'] == g and r['year'] == 2025][0] for g in order}
    if W >= 900:
        cols, gut, gapx = 4, 38, 26
    elif W >= 560:
        cols, gut, gapx = 2, 38, 32
    else:
        cols, gut, gapx = 1, 38, 0
    pw = (W - gut - gapx * (cols - 1)) / cols
    ph = 190 if cols != 1 else 172
    lo, hi = 40, 80
    head_h = 54
    foot_h = 30
    rows_n = math.ceil(len(order) / cols)
    gapy = 44 if cols != 1 else 30
    y_top = 0
    first_panel = True
    for i, g in enumerate(order):
        c, rr = i % cols, i // cols
        px = gut + c * (pw + gapx)
        py = y_top + rr * (head_h + ph + foot_h + gapy) + head_h
        x0, x1 = px, px + pw - 14

        def X(yr):
            return x0 + (yr - 1994) / (2025 - 1994) * (x1 - x0)

        def Y(v):
            return py + ph - (v - lo) / (hi - lo) * ph
        a.text(px, py - 34, HO_GROUP[g], t.lbl, 'tl', 600)
        for v in range(lo, hi + 1, 10):
            a.line(px, Y(v), px + pw, Y(v), 's-grid' if v != lo else 's-grid')
            if c == 0:
                a.text(px - 6, Y(v) + 4.5, f'{v}%' if v == hi else str(v), t.tk, 'tk', 400, 'end')
        for yr in (1994, 2003, 2025):
            anc = 'start' if yr == 1994 else ('end' if yr == 2025 else 'middle')
            a.text(X(yr) + (-2 if yr == 1994 else 0), py + ph + 23, str(yr), t.tk, 'tk', 400, anc)
        for og in order:
            if og == g:
                continue
            segs, lone = ho_segments(og)
            for seg in segs:
                a.path('M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg), 's-ctx15')
        segs, lone = ho_segments(g)
        for seg in segs:
            a.path('M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg), 's-sub')
            for r in seg:
                a.circle(X(r['year']), Y(r['rate_pct']), 2.2, 'f-ink', da(r['key'], r['rate_pct'], mark='point', axis='y', scale=f'p-{g}'))
        for r in lone:
            a.circle(X(r['year']), Y(r['rate_pct']), 2.2, 'f-ink', da(r['key'], r['rate_pct'], mark='point', axis='y', scale=f'p-{g}'))
        lv = last[g]
        a.rich(px, py - 13, [('2025: ', 'tn', 400), (f'{lv["rate_pct"]}%', 'th', 600)], t.nt, 'start',
               attrs=da(lv['key'], lv['rate_pct'], mark='label'))
        if g in ('black', 'hispanic'):
            H5 = rows('homeownership-by-race')

            def val(gg, yr):
                return next(r for r in H5 if r['group'] == gg and r['year'] == yr and r['series_variant'] == 'standard')['rate_pct']

            def clear_mid(y0, y1):
                lo_ = max(r['rate_pct'] for r in H5 if r['group'] == g and y0 <= r['year'] <= y1)
                hi_ = min(r['rate_pct'] for r in H5 if r['group'] == 'all_households' and y0 <= r['year'] <= y1)
                return (lo_ + hi_) / 2
            for yr, xb, side, span in ((2003, X(2003) - 5, -1, (1994, 2002)), (2025, x1 + 5, -1, (2018, 2025))):
                wv, gv = val('non_hispanic_white', yr), val(g, yr)
                arm = xb + 4 if yr == 2003 else xb - 4
                a.path(f'M{f(arm)} {f(Y(wv))}H{f(xb)}V{f(Y(gv))}H{f(arm)}', 's-ld')
                cy_ = Y(clear_mid(*span))
                a.text(xb - 5, cy_ + 5, f'{wv - gv:.1f}', t.nt, 'th', 600, 'end')
    yb = y_top + rows_n * (head_h + ph + foot_h + gapy) - gapy
    y = yb + 26
    note = ('The lines break where the Census changed its method: in 2002 it reweighted its estimates to the 2000 Census, '
            'so that year shows two values, and in 2003 it changed its race categories, so the Black and non-Hispanic White lines start again. '
            'Brackets give the gap to non-Hispanic White households in 2003 and 2025, in percentage points.')
    y = a.para(0, y, note, W if W < 900 else 760)
    return a, y + 8


# ------------------------------------------------------------------------------------------------ S06 comparison table
CLS_TINT = {'up': 'c-up', 'slightly up': 'c-up2', 'flat': 'c-flat', 'flat or down': 'c-dn2', 'down': 'c-dn',
            'mixed': 'c-mix', 'same as ii': 'c-same'}
CLS_WORD = {'up': 'Up', 'slightly up': 'Slightly up', 'flat': 'Flat', 'flat or down': 'Flat or down', 'down': 'Down',
            'mixed': 'Mixed', 'same as ii': 'Same as scenario ii'}


def glyph(cls):
    """The studio's reading of V7's direction words as a 16 px glyph: shape carries direction in grayscale."""
    p = {
        'up': '<path d="M8 2.5L14 13.5H2Z"/>',
        'slightly up': '<path d="M8 6L12 13H4Z"/>',
        'flat': '<rect x="2" y="6.75" width="12" height="2.5"/>',
        'flat or down': '<rect x="2" y="4" width="12" height="2.5"/><path d="M8 14L11.5 9H4.5Z"/>',
        'down': '<path d="M8 13.5L14 2.5H2Z"/>',
        'mixed': '<path d="M8 2L14 8L8 14L2 8Z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 2V14L2 8Z"/>',
        'same as ii': '<rect x="2" y="4.5" width="12" height="2.5"/><rect x="2" y="9" width="12" height="2.5"/>',
    }[cls]
    return f'<svg class="gl" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">{p}</svg>'


def gen_s06_table(view):
    D = DS['scenarios-2030']
    fam = D['families']
    head = ''.join(f'<th scope="col">{e(fam[k])}</th>' for k in ('DQ', 'GE', 'EP', 'EQ'))
    body = []
    for r in D['rows']:
        cells = []
        for k in ('DQ', 'GE', 'EP', 'EQ'):
            c = r[f'{k}_class']
            cells.append(f'<td class="{CLS_TINT[c]}" data-label="{e(fam[k])}"{da(r["key"], field=k, cat=r[k], mark="cell")}>'
                         f'<span class="gw"{da(r["key"], field=f"{k}_class", cat=c, mark="cell")}>{glyph(c)}'
                         f'<span class="vh2">{e(CLS_WORD[c])}: </span></span><span class="cw">{e(r[k][0].upper() + r[k][1:])}</span></td>')
        body.append(f'<tr><th scope="row"><span class="sk">{e(r["key"])}</span> {e(r["name"])}</th>{"".join(cells)}</tr>')
    key = ''.join(f'<li class="{CLS_TINT[c]}">{glyph(c)}<span>{e(CLS_WORD[c])}</span></li>'
                  for c in ('up', 'slightly up', 'flat', 'flat or down', 'down', 'mixed', 'same as ii'))
    return (f'<div class="cmpkey"><p class="kh">The studio\'s reading of the atlas\'s words, by arrow and tint</p><ul>{key}</ul></div>'
            f'<div class="tw" role="region" tabindex="0" aria-label="Scenario table, scrolls sideways when narrow">'
            f'<table class="cmp"><caption class="vh2">Direction each outcome family would take by 2036 under eight scenarios, in the atlas\'s words</caption>'
            f'<thead><tr><th scope="col">Scenario</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
            '<p class="tnote">Directions hold only if each scenario\'s assumptions hold. They are no forecast and give no odds. '
            'The four families are read separately and never added together. In the baseline, no family rises.</p>')


# ------------------------------------------------------------------------------------------------ S07 tile map
STATUS_KIND = {'bans in all elections': 'all', 'bans in some elections': 'some', 'no ban': 'none'}
STATUS_WORD = {'bans in all elections': 'Bans it in all elections', 'bans in some elections': 'Bans it in some elections',
               'no ban': 'No state ban'}


def gen_s07(W, uid, t=None):
    """Tile map: one square per state, so each state weighs the same whatever its land area."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    R = {r['key']: r for r in rows('rcv-bans')}
    if narrow:
        tile, gap = 24, 2.5
    else:
        gap = 4
        tile = min(52, (W + gap) / 12 - gap)
    pitch = tile + gap
    gw = 12 * pitch - gap
    ox = (W - gw) / 2 if narrow else 0
    oy = 0
    if narrow:
        y = 16
        some = [R[k]['name'] for k in R if R[k]['status'] == 'bans in some elections']
        items = [('ink', 'Bans it in all elections'), ('some', 'Bans it in some elections'), ('lt2', 'No state ban')]
        for kind, lab in items:
            key_item(a, 0, y, kind, lab, 14)
            y += 24
        y = a.para(21, y - 4, f'{" and ".join(sorted(some))} ban it in some elections only.', W - 21) + 14
        oy = y
    for tl in TILES:
        r = R[tl['code']]
        x, y = ox + tl['col'] * pitch, oy + tl['row'] * pitch
        kind = STATUS_KIND[r['status']]
        yr = f', {r["enacted_year"]}' if r['enacted_year'] else ''
        tip = f'{r["name"]}: {STATUS_WORD[r["status"]].lower()}{yr}'
        attrs = da(r['key'], field='status', cat=r['status'], mark='cell')
        a.raw(f'<g class="tile"><title>{e(tip)}</title>')
        if kind == 'all':
            a.rect(x, y, tile, tile, 'f-ink', attrs)
            tcls = 'ti'
        elif kind == 'some':
            a.rect(x + 1, y + 1, tile - 2, tile - 2, 's-ink2 f-g', attrs)
            band = round(tile * 0.24)
            a.rect(x + 1, y + tile - 1 - band, tile - 2, band, 'f-ink')
            tcls = 'tl'
        else:
            a.rect(x, y, tile, tile, 'f-lt2', attrs)
            tcls = 'tl'
        if narrow:
            ty = y + tile / 2 + 4.6 - (2.5 if kind == 'some' else 0)
            a.text(x + tile / 2, ty, tl['code'], 13, tcls, 600, 'middle')
        else:
            if kind == 'some':
                a.text(x + 7, y + 20, tl['code'], 14, 'tl', 600)
                a.text(x + 7, y + 37, str(r['enacted_year']), 13, 'tr', 400)
            elif kind == 'all':
                a.text(x + 7, y + 20, tl['code'], 14, 'ti', 600)
                a.text(x + 7, y + 37, str(r['enacted_year']), 13, 'ti4', 400)
            else:
                a.text(x + 7, y + 20, tl['code'], 14, 'tl', 600)
        a.raw('</g>')
    H = oy + 8 * pitch - gap
    if not narrow:
        # key in the empty top row, notes in the empty bottom right
        some = [R[k]['name'] for k in R if R[k]['status'] == 'bans in some elections']
        kx, ky = ox + pitch + 6, oy + 18
        key_item(a, kx, ky, 'ink', 'Bans it in all elections, with the year it became law', 14)
        key_item(a, kx, ky + 24, 'some', f'Bans it in some elections: {" and ".join(sorted(some))}', 14)
        key_item(a, kx, ky + 48, 'lt2', 'No state ban', 14)
        yrs = Counter(r['enacted_year'] for r in R.values() if r['enacted_year'])
        n2425 = yrs.get(2024, 0) + yrs.get(2025, 0)
        nb = sum(1 for r in R.values() if r['prohibits_rcv'])
        nx = ox + 10 * pitch + 4
        a.para(nx, oy + 5 * pitch + 18, f'{nw(n2425, cap=True, start=True)} of the {nb} bans became law in 2024 or 2025.', 2 * pitch - 6)
        a.para(ox + 2, oy + 6 * pitch + 18, 'Each square is one state, whatever its size.', 4 * pitch - 8)
    else:
        yrs = Counter(r['enacted_year'] for r in R.values() if r['enacted_year'])
        n2425 = yrs.get(2024, 0) + yrs.get(2025, 0)
        nb = sum(1 for r in R.values() if r['prohibits_rcv'])
        y = H + 28
        y = a.para(0, y, f'{nw(n2425, cap=True, start=True)} of the {nb} bans became law in 2024 or 2025. Each square is one state, whatever its size.', W)
        H = y + 6
    return a, H


# ------------------------------------------------------------------------------------------------ S08 unit chart
REDRAWS = ['RL38', 'RL40', 'RL41', 'RL50']


def unit_shape(a, x, y, s, d, attrs):
    """One unit per repair-log row. Self-closing marks, so each row is one element."""
    if d == 'toward voters' or d == 'away from voters':
        a.rect(x, y, s, s, 'f-ink', attrs)
    elif d == 'voters kept existing rules':
        a.rect(x, y, s, s, 'f-ctx', attrs)
    elif d == 'mixed':
        a.rect(x + 0.75, y + 0.75, s - 1.5, s - 1.5, 's-ctx15 f-g', attrs)
        a.path(f'M{f(x + 0.75)} {f(y + s - 0.75)}L{f(x + s - 0.75)} {f(y + 0.75)}L{f(x + s - 0.75)} {f(y + s - 0.75)}Z', 'f-ctx')
    elif d == 'pending':
        a.rect(x + 0.75, y + 0.75, s - 1.5, s - 1.5, 's-dash', attrs)


def gen_s08(W, uid, t=None, keyed=True):
    """Unit chart: one square per entry in the repair log, by year; toward voters stacks above the year line, away
    below it, and entries that went neither way sit in their own band. Dotted squares are mid-decade redraws."""
    a = Art(W, uid, t)
    t = a.t
    D = sorted(rows('rule-changes'), key=lambda r: (r['date'], r['key']))
    narrow = W < 900          # the year columns need about 60 px each; under that, years run down the page

    def attrs(r):
        if keyed:
            return da(r['key'], field='direction', cat=r['direction'], mark='unit')
        return f' data-row="{r["key"]}" data-dir="{e(r["direction"])}"'
    bins = [('early', '1965 to 2012', lambda r: r['year'] < 2013)] + [(str(y), str(y), (lambda yy: lambda r: r['year'] == yy)(y)) for y in range(2013, 2027)]
    neither = ('voters kept existing rules', 'mixed', 'pending')
    s, g = 14, 3
    drawn = Counter()
    if not narrow:
        LW = 146
        colw = (W - LW) / len(bins)
        per = max(1, int((colw - 10 + g) // (s + g)))
        cw = per * (s + g) - g

        def stack_h(n):
            return math.ceil(n / per) * (s + g) - g if n else 0
        up_max = max(stack_h(sum(1 for r in D if fn(r) and r['direction'] == 'toward voters')) for _, _, fn in bins)
        dn_max = max(stack_h(sum(1 for r in D if fn(r) and r['direction'] == 'away from voters')) for _, _, fn in bins)
        ne_max = max(stack_h(sum(1 for r in D if fn(r) and r['direction'] in neither)) for _, _, fn in bins)
        top_note = 64
        yA = top_note + up_max + 8          # bottom of the toward stacks
        band = 30 if per > 2 else 44
        yB = yA + band                      # top of the away stacks
        yC = yB + dn_max + 40               # top of the neither band
        a.line(LW - 6, yA, W, yA, 's-base')
        a.line(LW - 6, yB, W, yB, 's-base')
        a.text(0, yA - 6, 'Toward voters', t.lbl, 'tl', 600)
        a.text(0, yB + 16, 'Away from voters', t.lbl, 'tl', 600)
        a.line(LW - 6, yC - 12, W, yC - 12, 's-grid')
        a.text(0, yC + 12, 'Neither way', t.lbl, 'ts', 600)
        cx_of = {}
        for i, (bk, lab, fn) in enumerate(bins):
            cx = LW + i * colw + (colw - cw) / 2
            cx_of[bk] = cx
            ins = [r for r in D if fn(r)]
            labs = ['To 2012'] if bk == 'early' else [lab]
            for j, ln in enumerate(labs):
                yy = yA + band / 2 + 5 - (len(labs) - 1) * 8 + j * 16
                a.text(cx + cw / 2, yy, ln, t.tk, 'tk', 400, 'middle')
            for d, y0, sign in (('toward voters', yA - s, -1), ('away from voters', yB, 1)):
                rs = [r for r in ins if r['direction'] == d]
                for n, r in enumerate(rs):
                    x = cx + (n % per) * (s + g)
                    yy = y0 + sign * (n // per) * (s + g)
                    unit_shape(a, x, yy, s, d, attrs(r))
                    drawn[d] += 1
                    if r['key'] in REDRAWS:
                        a.circle(x + s / 2, yy + s / 2, 2.6, 'f-g')
            rs = sorted([r for r in ins if r['direction'] in neither], key=lambda r: (neither.index(r['direction']), r['date']))
            for n, r in enumerate(rs):
                x = cx + (n % per) * (s + g)
                yy = yC + (n // per) * (s + g)
                unit_shape(a, x, yy, s, r['direction'], attrs(r))
                drawn[r['direction']] += 1
        assert sum(drawn.values()) == len(D)
        # notes: the two periods the title compares
        pre = Counter(r['direction'] for r in D if r['date'] < '2025-01-01')
        post = Counter(r['direction'] for r in D if r['date'] >= '2025-01-01')
        xa0, xa1 = cx_of['early'], cx_of['2024'] + cw
        xb0, xb1 = cx_of['2025'], cx_of['2026'] + cw
        yt = 20
        a.path(f'M{f(xa0)} {f(yt + 18)}V{f(yt + 12)}H{f(xa1)}V{f(yt + 18)}', 's-ld')
        a.path(f'M{f(xb0)} {f(yt + 18)}V{f(yt + 12)}H{f(xb1)}V{f(yt + 18)}', 's-ld')
        a.text(xa0, yt + 2, f'1965 through 2024: {pre["toward voters"]} toward, {pre["away from voters"]} away', t.nt, 'th', 600)
        txt = f'Since January 2025: {post["toward voters"]} toward, {post["away from voters"]} away'
        a.text(xb1, yt + 2, txt, t.nt, 'th', 600, 'end')
        # neither band key
        nk = yC + ne_max + 34
        xk = LW
        for d, lab in (('voters kept existing rules', 'Voters kept existing rules: a ballot measure failed'),
                       ('mixed', 'Mixed'), ('pending', 'Pending on November 3, 2026')):
            unit_shape(a, xk, nk - 11, s, d, '')
            w = a.text(xk + s + 7, nk, lab, t.nt, 'tr', 400)
            xk += s + 7 + w + 22
        ring_y = nk + 30
        a.rect(LW, ring_y - 11, s, s, 'f-ink')
        a.circle(LW + s / 2, ring_y - 11 + s / 2, 2.6, 'f-g')
        a.para(LW + s + 14, ring_y, 'Dotted: mid-decade congressional maps, coded away from voters whichever party drew them '
                                    '(Texas and Missouri in 2025, California in 2025 and Virginia in 2026).', W - LW - s - 14)
        n, lh = a.para_h('x', 10)
        H = ring_y + (len(wrap('Dotted: mid-decade congressional maps, coded away from voters whichever party drew them (Texas and Missouri in 2025, California in 2025 and Virginia in 2026).', W - LW - s - 14, t.nt)) - 1) * t.lh + 8
        return a, H
    # phone: years run down; away grows left of the year column, toward right; neither in its own block below
    yearw = 50
    cxm = W / 2
    left_edge, right_edge = 0, W
    per = int(((cxm - yearw / 2 - 6) + g) // (s + g))
    s2 = s
    y = 18
    pre = Counter(r['direction'] for r in D if r['date'] < '2025-01-01')
    post = Counter(r['direction'] for r in D if r['date'] >= '2025-01-01')
    a.text(cxm - yearw / 2 - 6, y, 'Away from voters', 14, 'tl', 600, 'end')
    a.text(cxm + yearw / 2 + 6, y, 'Toward voters', 14, 'tl', 600)
    y += 18
    a.line(cxm - yearw / 2, y - 4, cxm - yearw / 2, y, 's-none')
    first_row_y = y
    rowpos = {}
    for bk, lab, fn in bins:
        ins = [r for r in D if fn(r)]
        tow = [r for r in ins if r['direction'] == 'toward voters']
        awy = [r for r in ins if r['direction'] == 'away from voters']
        nrows = max(1, math.ceil(len(tow) / per), math.ceil(len(awy) / per))
        h = nrows * (s + g) - g
        rowpos[bk] = (y, h)
        labs = ['To 2012'] if bk == 'early' else [lab]
        hh = max(h, 19 * len(labs) - 3)
        for j, ln in enumerate(labs):
            a.text(cxm, y + 11 + j * 19, ln, 14, 'tk', 400, 'middle')
        for n, r in enumerate(tow):
            x = cxm + yearw / 2 + 4 + (n % per) * (s + g)
            yy = y + (n // per) * (s + g)
            unit_shape(a, x, yy, s, r['direction'], attrs(r))
            if r['key'] in REDRAWS:
                a.circle(x + s / 2, yy + s / 2, 2.6, 'f-g')
            drawn[r['direction']] += 1
        for n, r in enumerate(awy):
            x = cxm - yearw / 2 - 4 - s - (n % per) * (s + g)
            yy = y + (n // per) * (s + g)
            unit_shape(a, x, yy, s, r['direction'], attrs(r))
            if r['key'] in REDRAWS:
                a.circle(x + s / 2, yy + s / 2, 2.6, 'f-g')
            drawn[r['direction']] += 1
        y += hh + 9
    a.line(cxm - yearw / 2, first_row_y - 4, cxm - yearw / 2, y - 6, 's-base')
    a.line(cxm + yearw / 2, first_row_y - 4, cxm + yearw / 2, y - 6, 's-base')
    y += 18
    y = a.para(0, y, f'1965 through 2024: {pre["toward voters"]} toward, {pre["away from voters"]} away. '
                     f'Since January 2025: {post["toward voters"]} toward, {post["away from voters"]} away.', W, 14, 'th', 600) + 34
    a.text(0, y, 'Neither way', 14, 'ts', 600)
    y += 14
    nrow = [r for r in D if r['direction'] in neither]
    by_year = defaultdict(list)
    for r in nrow:
        by_year[r['year']].append(r)
    for yr in sorted(by_year):
        rs = sorted(by_year[yr], key=lambda r: (neither.index(r['direction']), r['date']))
        a.text(0, y + 12, str(yr), 14, 'tk', 400)
        for n, r in enumerate(rs):
            unit_shape(a, 48 + n * (s + g), y, s, r['direction'], attrs(r))
            drawn[r['direction']] += 1
        y += s + 10
    assert sum(drawn.values()) == len(D)
    y += 18
    for d, lab in (('voters kept existing rules', 'Voters kept existing rules: a ballot measure failed'),
                   ('mixed', 'Mixed'), ('pending', 'Pending on November 3, 2026')):
        unit_shape(a, 0, y - 11, s, d, '')
        y = a.para(s + 8, y, lab, W - s - 8, 14, 'tr', 400) + 24
    a.rect(0, y - 6, s, s, 'f-ink')
    a.circle(s / 2, y - 6 + s / 2, 2.6, 'f-g')
    y = a.para(s + 14, y + 5, 'Dotted: mid-decade congressional maps, coded away from voters whichever party drew them '
                              '(Texas and Missouri in 2025, California in 2025 and Virginia in 2026).', W - s - 14)
    return a, y + 8


# ------------------------------------------------------------------------------------------------ S09 timeline
THREADS = ['who_counts', 'who_governs', 'who_owns', 'who_checks']
SHORT = {
    'E01': 'Fifteenth Amendment', 'E02': 'Mississippi constitution', 'E03': 'Seventeenth Amendment',
    'E04': 'Nineteenth Amendment', 'E05': 'House fixed at 435', 'E06': 'Wagner Act', 'E07': 'Taft-Hartley Act',
    'E08': 'Reynolds v. Sims', 'E09': 'Voting Rights Act', 'E10': 'McGovern-Fraser rules',
    'E11': 'Budget and Impoundment Control Act', 'E12': 'Buckley v. Valeo', 'E13': 'Proposition 13',
    'E14': 'Inspector General Act', 'E15': '104th Congress opens', 'E16': 'Gramm-Leach-Bliley Act',
    'E17': 'Citizens United v. FEC', 'E18': 'Shelby County v. Holder', 'E19': 'Nuclear option for nominations',
    'E20': 'Tax Cuts and Jobs Act', 'E21': 'Electoral Count Reform Act', 'E22': 'Budget reconciliation law',
    'E23': 'Louisiana v. Callais', 'E24': 'Trump v. Slaughter and Trump v. Cook'}
STRETCHES = [(1964, 1978), (2010, 2026)]


def dec_year(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return y + (m - 1) / 12 + (d - 1) / 365


def _rows_for(items, anchors):
    """Row assignment for one choice of anchors, or None when two labels cover each other's dots."""
    iv = [(it['x'] - 4, it['x'] + it['w'] + 6) if an == 'start' else (it['x'] - it['w'] - 6, it['x'] + 4)
          for it, an in zip(items, anchors)]
    n = len(items)
    cover = {i: [j for j in range(n) if j != i and iv[i][0] <= items[j]['x'] <= iv[i][1]] for i in range(n)}
    order, seen, temp = [], set(), set()

    def visit(i):
        if i in seen:
            return True
        if i in temp:
            return False
        temp.add(i)
        for j in cover[i]:
            if not visit(j):
                return False
        temp.discard(i)
        seen.add(i)
        order.append(i)
        return True
    for i in range(n):
        if not visit(i):
            return None
    rows_, placed = {}, defaultdict(list)
    for i in order:
        r = max([rows_[j] + 1 for j in cover[i]] + [0])
        while any(not (iv[i][1] <= p_[0] or iv[i][0] >= p_[1]) for p_ in placed[r]):
            r += 1
        rows_[i] = r
        placed[r].append(iv[i])
    return rows_, iv


def stack_rows(items, left, right):
    """Rows for labels above a lane. A label that covers another event's dot sits above it, so no leader crosses a
    label, and labels in one row never overlap. Tries every anchor choice (label to the right of its dot, or to
    the left) that fits the plot and keeps the one with the fewest rows, then the most labels to the right."""
    import itertools
    best = None
    for anchors in itertools.product(('start', 'end'), repeat=len(items)):
        if any((an == 'start' and it['x'] + it['w'] + 4 > right) or (an == 'end' and it['x'] - it['w'] - 4 < left)
               for it, an in zip(items, anchors)):
            continue
        res = _rows_for(items, anchors)
        if res is None:
            continue
        rows_, iv = res
        score = (max(rows_.values()) + 1, sum(rows_.values()), sum(an == 'end' for an in anchors))
        if best is None or score < best[0]:
            best = (score, anchors, rows_, iv)
    if best is None:
        raise AssertionError('timeline labels cannot be placed in this lane')
    _, anchors, rows_, iv = best
    for i, it in enumerate(items):
        it['anchor'], it['row'], it['iv'] = anchors[i], rows_[i], iv[i]
    return items


def gen_s09(W, uid, t=None):
    """Timeline: twenty-four dated rule changes on a true time scale, one lane per thread, every event named."""
    a = Art(W, uid, t)
    t = a.t
    D = DS['history-events']
    ev = sorted(D['rows'], key=lambda r: r['date'])
    TH = {th['id']: th for th in D['threads']}
    size = t.lbl - 1 if W >= 900 else 14
    if W >= 900:
        LW = 168
        x0, x1 = LW + 8, W - 6
        y0r, y1r = 1870, 2027

        def X(yr):
            return x0 + (yr - y0r) / (y1r - y0r) * (x1 - x0)
        row_h = 21
        ytop = 84
        lane_y = {}
        y = ytop
        lanes = {}
        for th in THREADS:
            items = []
            for r in ev:
                if r['thread'] != th:
                    continue
                lab_y, lab_n = str(r['year']) + ' ', SHORT[r['key']]
                w = tw(lab_y, size, 600) + tw(lab_n, size, 400)
                items.append({'r': r, 'x': X(dec_year(r['date'])), 'w': w, 'parts': [(lab_y, 'th', 600), (lab_n, 'tr', 400)]})
            stack_rows(items, x0 - 2, x1)
            nrow = max(it['row'] for it in items) + 1
            qh = len(wrap(TH[th]['question'], LW - 14, 14)) * 19 + 26
            h = max(nrow * row_h + 22, qh)
            lanes[th] = (y, h, items)
            y += h + 22
        H = y - 22 + 34
        # the two stretches the title names, as bands behind the lanes
        for s0, s1 in STRETCHES:
            bx0, bx1 = X(s0), X(s1 + 1) if s1 < 2026 else x1
            a.rect(bx0, ytop - 56, bx1 - bx0, H - 34 - ytop + 56 + 8, 'f-band')
            n_in = sum(1 for r in ev if s0 <= r['year'] <= s1)
            anc = 'start' if s1 < 2026 else 'end'
            xx = bx0 + 6 if s1 < 2026 else bx1 - 6
            a.text(xx, ytop - 36, f'{s0} to {s1}', t.nt, 'th', 600, anc)
            a.text(xx, ytop - 17, f'{n_in} changes', t.nt, 'tn', 400, anc)
        for th in THREADS:
            ly, h, items = lanes[th]
            base = ly + h - 10
            a.line(x0, base, x1, base, 's-grid')
            a.text(0, ly + 16, TH[th]['label'], t.lbl, 'tl', 600)
            a.para(0, ly + 36, TH[th]['question'], LW - 14, 14, 'tn', 400, 19)
            for it in items:
                r = it['r']
                ty = base - 14 - it['row'] * row_h
                xx = it['x']
                a.line(xx, base - 4, xx, ty + 4, 's-ld')
                tx = xx + 3 if it['anchor'] == 'start' else xx - 3
                a.rich(tx, ty, it['parts'], size, it['anchor'])
                a.circle(xx, base, 4.5, 'f-ink', da(r['key'], field='date', cat=r['date'], mark='point'))
        yb = H - 34
        a.line(x0, yb, x1, yb, 's-base')
        for yr in range(1875, 2027, 25):
            a.line(X(yr), yb, X(yr), yb + 5, 's-base')
            a.text(X(yr), yb + 22, str(yr), t.tk, 'tk', 400, 'middle')
        return a, H
    # phone and middle widths: time runs down one axis; each label names its thread
    ax = 48 if W < 600 else 70
    lx = ax + 26
    lwid = W - lx
    y0p = 54
    py = 1050 if W < 600 else 980
    yr0, yr1 = 1870, 2027

    def Yp(yr):
        return y0p + (yr - yr0) / (yr1 - yr0) * py
    blocks = []
    for r in ev:
        lines = wrap(SHORT[r['key']], lwid - tw(f'{r["year"]} ', 14, 600), 14)
        h = 18 + 19 * len(lines)
        blocks.append((r, lines, h))
    cs = spread([Yp(dec_year(r['date'])) + h / 2 - 9 for r, _, h in blocks], [h for _, _, h in blocks], 30, 3000, 8)
    for s0, s1 in STRETCHES:
        b0, b1 = Yp(s0), Yp(s1 + 1)
        a.rect(0, b0, ax + 12, b1 - b0, 'f-band')
    for yr in range(1875, 2027, 25):
        a.line(ax - 4, Yp(yr), ax, Yp(yr), 's-base')
        a.text(ax - 8, Yp(yr) + 5, str(yr), 14, 'tk', 400, 'end')
    for (r, lines, h), c in zip(blocks, cs):
        yy = Yp(dec_year(r['date']))
        top = c - h / 2
        a.leader([(ax + 6, yy), (lx - 12, yy), (lx - 6, top + 6), (lx - 2, top + 6)])
        a.text(lx, top + 11, TH[r['thread']]['label'].upper(), 13, 'te', 700, track=0.06)
        for i, ln in enumerate(lines):
            if i == 0:
                a.rich(lx, top + 30, [(f'{r["year"]} ', 'th', 600), (ln, 'tr', 400)], 14)
            else:
                a.text(lx, top + 30 + 19 * i, ln, 14, 'tr', 400)
        a.circle(ax, yy, 4, 'f-ink', da(r['key'], field='date', cat=r['date'], mark='point'))
    endy = max(Yp(yr1), max(c + h / 2 for (_, _, h), c in zip(blocks, cs)))
    a.line(ax, y0p - 10, ax, Yp(yr1), 's-base')
    n1 = sum(1 for r in ev if 1964 <= r['year'] <= 1978)
    n2 = sum(1 for r in ev if 2010 <= r['year'] <= 2026)
    a.para(0, 14, f'Shaded: 1964 to 1978 ({n1} changes) and 2010 to 2026 ({n2}).', W, 14, 'th', 600)
    return a, endy + 10


# ------------------------------------------------------------------------------------------------ S10 evidence mix
GRADES = ['documented', 'well-supported', 'plausible', 'contested']
GRADE_WORD = {'documented': 'Documented', 'well-supported': 'Well supported', 'plausible': 'Plausible', 'contested': 'Contested'}
GRADE_KIND = {'documented': 'ink', 'well-supported': 'ctx', 'plausible': 'lt', 'contested': 'hatch'}


def gen_s10(W, uid, t=None):
    """Evidence mix: each answer's claims split by grade, sorted by the documented share. Grades step from Charcoal
    to a hatch, never red; the vertical rule gives the share across all 433 claims."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    D = DS['claims-by-grade']
    R = sorted(D['rows'], key=lambda r: (-r['documented'] / r['value'], r['key']))
    tot = D['totals']
    allshare = tot['documented'] / sum(tot.values())
    lbl = t.lbl - 1 if not narrow else 14
    yk = flow_key(a, 0, 16, [(GRADE_KIND[g], f'{GRADE_WORD[g]}: {D["grade_meaning"][g]}') for g in GRADES], W, 14, 22, 24)
    if narrow:
        BX, BW = 0, W - 46
        pitch = 54
    else:
        LW = min(272, max(tw(r['title'], lbl, 600) for r in R) + 4)
        BX = LW + 10
        NOTE_W = 146
        BW = W - BX - 56 - NOTE_W - 14
        pitch = 36
    bh = 16 if not narrow else 14
    y = yk + 54
    xr = BX + BW * allshare
    ref = f'All {sum(tot.values())} claims: {pct0(allshare * 100)} documented'
    rw_ = tw(ref, t.nt, 600)
    rx = min(max(xr - rw_ / 2, 0), BX + BW - rw_ if not narrow else W - rw_)
    a.text(rx, y - 22, ref, t.nt, 'th', 600)
    a.text(BX + BW + 8 if not narrow else W, y - 22, 'Documented', t.tk, 'tk', 400, 'start' if not narrow else 'end') if not narrow else None
    rows_y = {}
    ytop = y - 10
    for r in R:
        if narrow:
            lines = wrap(r['title'], W - 50, 14, 600)
            for i, ln in enumerate(lines[:2]):
                a.text(0, y + i * 18, ln, 14, 'tl', 600)
            by = y + 8 + (len(lines[:2]) - 1) * 18
        else:
            lines = wrap(r['title'], LW, lbl, 600)
            by = y - bh / 2
            for i, ln in enumerate(lines):
                a.text(0, y + 5 + (i - (len(lines) - 1) / 2) * 17, ln, lbl, 'tl', 600)
        x = BX
        for g in GRADES:
            v = r[g]
            if not v:
                continue
            w = BW * v / r['value']
            seg_rect(a, x, by, w, bh, GRADE_KIND[g], da(r['key'], v, field=g, mark='bar', axis='x', scale=r['key']))
            x += w
        share = r['documented'] / r['value'] * 100
        a.text(BX + BW + 8 if not narrow else W, by + bh / 2 + 5, pct0(share), t.lbl, 'tl', 600, 'start' if not narrow else 'end',
               attrs=da(r['key'], r['documented'], field='documented', mark='label'))
        rows_y[r['key']] = (by, by + bh)
        y = by + bh + (pitch - bh) if narrow else y + pitch
    ybot = max(v[1] for v in rows_y.values())
    a.line(xr, ytop, xr, ybot + 6, 's-mark')
    a.line(BX, ytop, BX, ybot + 6, 's-base')
    top, low = R[0], R[-1]
    con = max(R, key=lambda r: (r['contested'], r['key']))
    notes = [(top['key'], f'{top["title"]}: {top["documented"]} of {top["value"]} claims documented, the highest share.'),
             (con['key'], f'{con["title"]}: {con["contested"]} of {con["value"]} claims contested, the most of any answer.'),
             (low['key'], f'{low["title"]}: {low["documented"]} of {low["value"]} documented, the lowest share.')]
    if not narrow:
        nx = W - NOTE_W
        hs, ideals = [], []
        for k, txt in notes:
            n, lh = a.para_h(txt, NOTE_W)
            hs.append(n * lh)
            b0, b1 = rows_y[k]
            ideals.append((b0 + b1) / 2 - 5 + n * lh / 2 - lh / 2)
        cs = spread(ideals, hs, 0, 5000, 12)
        for (k, txt), c, h in zip(notes, cs, hs):
            ytop_n = c - h / 2 + t.nt * 0.75
            a.para(nx, ytop_n, txt, NOTE_W)
            b0, b1 = rows_y[k]
            a.leader([(BX + BW + 44, (b0 + b1) / 2), (nx - 8, (b0 + b1) / 2)])
        H = max(ybot + 14, max(c + h / 2 for c, h in zip(cs, hs)) + 10)
    else:
        y = ybot + 36
        for k, txt in notes:
            y = a.para(0, y, txt, W) + 26
        H = y - 26 + 8
    return a, H


# ------------------------------------------------------------------------------------------------ the figure frame
GRADE_LINE = {
    'S01': 'Documented: a published survey and two recorded votes',
    'S02': 'Official statistic: Census Bureau survey estimates',
    'S03': "Documented: the atlas's dated log, coded by the atlas",
    'S04': 'Official statistic: what survey respondents reported',
    'S05': 'Official statistic: Census Bureau survey estimates',
    'S06': 'Conditional directions: no forecast and no odds',
    'S07': 'Secondary compilation: Ballotpedia, checked against the atlas',
    'S08': "Documented: the atlas's dated log, coded by the atlas",
    'S09': 'Documented: every event rests on an official record',
    'S10': "Documented: the atlas's own register of graded claims",
}


def source_text(sid):
    ds = DS[SPECS[sid]['dataset']]
    s = iso_to_words(ds['source_line'])
    s = re.sub(r'^Source:\s*', '', s)
    s = s.replace('Snapshot of', 'snapshot of').replace('. snapshot of', '. Snapshot of')
    return s


def table_html(caption, header, body, num_cols=(), cls='eqt'):
    th = ''.join(f'<th scope="col"{" class=num" if i in num_cols else ""}>{e(h)}</th>' for i, h in enumerate(header))
    trs = []
    for r in body:
        cells = []
        for i, c in enumerate(r):
            if i == 0:
                cells.append(f'<th scope="row">{e(c)}</th>')
            else:
                cells.append(f'<td{" class=num" if i in num_cols else ""}>{e(c)}</td>')
        trs.append('<tr>' + ''.join(cells) + '</tr>')
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{e(caption)}, table">'
            f'<table class="{cls}"><caption>{e(caption)}</caption><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>')


def artboards(view, sid, gen, wide, label, **kw):
    """Draw one generator at the figure's full width, at 600 px and at 320 px."""
    out = []
    for W, cls in ((wide, 'ab ab-w'), (600, 'ab ab-m'), (320, 'ab ab-n')):
        uid = f'{view}-{sid.lower()}-{W}'
        art, H = gen(W, uid, **kw)
        out.append(art.render(H, label, cls, f'{sid.lower()}-{view}-{W}'))
    return f'<div class="art w{wide}">{"".join(out)}</div>'


def figure(view, sid, title, measure, body, notes, table, wide=False, extra='', source=None):
    spec = SPECS[sid]
    ds = DS[spec['dataset']]
    ev = ds['evidence']
    src = source or source_text(sid)
    note_html = ''.join(f'<li>{e(n)}</li>' for n in notes)
    eq = (f'<details class="eq" data-role="equivalent"><summary>Show the table and notes</summary>'
          f'<div class="eqb"><p class="eqh">Notes in the chart</p><ul class="eqn">{note_html}</ul>{table}'
          f'<p class="src">Source: {e(src)}</p></div></details>')
    return (f'<figure class="fig{" wide" if wide else ""}" id="{view}-{sid.lower()}-fig" data-spec="{sid}" '
            f'data-dataset="{spec["dataset"]}" data-evidence="{ev}">'
            f'<div class="evrow"><p class="ev" data-role="evidence-label">{ev}</p><p class="grade">{e(GRADE_LINE[sid])}</p></div>'
            f'<h3 class="ct" data-role="title">{e(title)}</h3>'
            f'<p class="ms" data-role="measure">{e(measure)}</p>'
            f'{body}{extra}'
            f'<div class="srcrow"><p class="src" data-role="source"><span class="sl">Source:</span> {e(src)}</p>'
            f'<p class="src credit">Chart: Oath &amp; Action</p></div>{eq}</figure>')


def strip(view, sid, why):
    spec = SPECS[sid]
    return (f'<div class="strip"><p class="stag">Studio note, not part of the chart</p>'
            f'<h2 class="sid" id="{view}-{sid.lower()}-h">{sid} <span>{e(spec["form"])}</span></h2>'
            f'<dl><dt>Reader question</dt><dd>{e(spec["reader_question"])}</dd>'
            f'<dt>Why this form</dt><dd>{e(why)}</dd></dl></div>')


# ------------------------------------------------------------------------------------------------ the ten specimens
WHY = {
    'S01': 'One large figure gives the fact a reader repeats; the party bars and the two votes put it in context in the same drawing.',
    'S02': 'A line shows the rise and fall in order, and notes at 2021 and at the method breaks explain what a reader could misread.',
    'S03': 'Ranked bars answer who acted most, and splitting each bar by the atlas\'s direction code shows which way each instrument moved the rules.',
    'S04': 'A dumbbell puts two elections on one line for each age group, so the level and the change read at once.',
    'S05': 'Small multiples give each group its own panel on one scale, so a reader follows one line at a time and still sees the others.',
    'S06': 'A table lets a reader look up one scenario and one outcome; the atlas\'s own words sit in every cell beside the studio\'s arrow.',
    'S07': 'A tile map gives each state the same weight, so the count reads true where a land map would favor large western states.',
    'S08': 'One square per entry lets a reader count, and placing toward above the year line and away below it shows the turn without a second chart.',
    'S09': 'A true time scale shows when changes bunch together, and four lanes keep each thread readable.',
    'S10': 'A bar split by grade shows how much of each answer rests on the record, and sorting by that share puts the answers in order.',
}


def spec_s01(view):
    R = {r['key']: r for r in rows('stock-trading-ban')}
    title = 'Nearly nine in ten Republican and Democratic voters favored a ban on stock trading by members of Congress.'
    measure = ('Registered voters who favor a ban, percent, by party, survey of May 2023, United States; '
               'votes on H.R. 7008 in the House (July 22, 2026) and the Senate (September 30, 2026)')
    body = artboards(view, 'S01', gen_s01, 720, 'Big number: 86 percent of registered voters favored a ban; 88 percent of Democrats and 87 percent of Republicans. The House passed it 232 to 198; the Senate vote to take it up was 53 to 47, 7 short of the 60 needed. The table below carries every value.')
    notes = ['Survey of 2,625 registered voters, May 19 to 30, 2023, three years before either vote.',
             'The two parties sit one point apart; the bars run from 0 to 100 percent.',
             'The Senate vote to take up the bill fell 7 votes short of the 60 needed.']
    table = table_html('Support for a ban and the votes that followed', ['Group', 'Measure', 'Value'],
                       [[r['group'], r['measure'], str(r['value'])] for r in rows('stock-trading-ban')], (2,))
    return figure(view, 'S01', title, measure, body, notes, table)


def spec_s02(view, red=True):
    D = rows('child-poverty-spm')
    p20, p21, p22 = (row('child-poverty-spm', f'spm|{y}|standard')['percent'] for y in (2020, 2021, 2022))
    title = (f'Child poverty fell to {p21} percent in 2021, the lowest since the series began in 2009, '
             'and more than doubled the next year.')
    assert p21 == min(r['percent'] for r in D if r['measure'] == 'spm') and p22 > 2 * p21
    measure = ('Children under 18 below the Supplemental Poverty Measure, percent, United States, 2009 to 2025, '
               'with the official measure in gray for comparison')
    body = artboards(view, 'S02', gen_s02, 720,
                     f'Line chart: child poverty under the Supplemental Poverty Measure fell from {p20} percent in 2020 to {p21} percent in 2021, '
                     f'then rose to {p22} percent in 2022 and 13.4 percent in 2025. The table below carries every value.', red=red)
    notes = ['2021: the expanded child tax credit was in force. Census reads a change between years as a description, not the effect of one policy.',
             f'2022: {p22} percent, after the expanded credit lapsed.',
             'Both measures read 13.4 percent in 2025.',
             'Census changed its survey or method in 2013, 2017 and 2019; the line breaks there and those years show two estimates.']
    body_rows = []
    for r in sorted(D, key=lambda r: (r['year'], r['measure'], r['series_variant'])):
        body_rows.append([str(r['year']), 'Supplemental' if r['measure'] == 'spm' else 'Official',
                          r['series_variant'].replace('_', ' '), f'{r["percent"]:.1f}',
                          f'{r["moe_pct"]:.1f}' if isinstance(r['moe_pct'], float) else 'not given'])
    table = table_html('Children in poverty, percent', ['Year', 'Measure', 'Estimate', 'Percent', 'Margin of error (90%)'],
                       body_rows, (3, 4))
    return figure(view, 'S02', title, measure, body, notes, table)


def spec_s03(view):
    D = rows('rule-changes-by-instrument')
    ss = row('rule-changes-by-instrument', 'State statute')
    title = f'{nw(ss["away from voters"], cap=True, start=True)} of the {ss["value"]} state statutes in the atlas\'s log moved the rules away from voters.'
    assert ss['away from voters'] == max(r['away from voters'] for r in D)
    measure = ("Entries in the atlas's repair log by how the rule changed and by the atlas's direction code, "
               'August 1965 to the November 3, 2026 ballot')
    body = artboards(view, 'S03', gen_s03, 720,
                     'Ranked bar chart of the 64 repair-log entries by instrument, each split by direction. The table below carries every value.')
    coding = DS['rule-changes']['coding_note']
    extra = (f'<details class="code"><summary>How the atlas codes direction</summary><p>{e(coding)}</p></details>')
    notes = ['None of the 17 initiatives moved the rules away from voters; eight failed, which left the rules in force.',
             'Nine of 11 statutes moved the rules away from voters, the largest share of any instrument.',
             DS['rule-changes-by-instrument']['notes'][0], 'Directions are the atlas\'s own codes, set out in its coding note.']
    hdr = ['Instrument', 'All'] + [DIR_WORD[d] for d in DIR_ORDER]
    table = table_html('Repair-log entries by instrument and direction', hdr,
                       [[r['key'], str(r['value'])] + [str(r[d]) for d in DIR_ORDER] for r in sorted(D, key=lambda r: -r['value'])],
                       tuple(range(1, 7)))
    return figure(view, 'S03', title, measure, body, notes, table, extra=extra)


def spec_s04(view):
    base = 'citizen_voting_age_population'
    R = {(r['age_group'], r['year']): r for r in rows('turnout-by-age') if r['base'] == base}
    g20 = R[('65_and_over', 2020)]['voted_pct'] - R[('18_to_24', 2020)]['voted_pct']
    g24 = R[('65_and_over', 2024)]['voted_pct'] - R[('18_to_24', 2024)]['voted_pct']
    title = (f'The gap in reported voting between citizens 18 to 24 and those 65 and over grew from '
             f'{round(g20)} points in 2020 to {round(g24)} in 2024.')
    measure = 'Citizens who reported voting in November, percent, by age group, 2020 and 2024 presidential elections, United States'
    body = artboards(view, 'S04', gen_s04, 720,
                     'Dot plot of reported voting by age group in 2020 and 2024. The table below carries every value.')
    notes = [f'The gap between citizens 18 to 24 and those 65 and over: {g20:.1f} points in 2020, {g24:.1f} in 2024.',
             'These rates are what people told a Census survey, which runs higher than counted ballots.',
             'The table gives no margins of error, so a change of a point or two may sit within survey error.']
    body_rows = []
    for g in AGE_WORD:
        v0, v1 = R[(g, 2020)]['voted_pct'], R[(g, 2024)]['voted_pct']
        ch = v1 - v0
        body_rows.append([AGE_WORD[g], f'{v0:.1f}', f'{v1:.1f}', (MINUS if ch < 0 else '+') + f'{abs(ch):.1f}'])
    table = table_html('Reported voting, citizens, percent', ['Age group', '2020', '2024', 'Change, points'], body_rows, (1, 2, 3))
    return figure(view, 'S04', title, measure, body, notes, table)


def spec_s05(view):
    H = rows('homeownership-by-race')
    w25 = next(r for r in H if r['group'] == 'non_hispanic_white' and r['year'] == 2025)['rate_pct']
    b25 = next(r for r in H if r['group'] == 'black' and r['year'] == 2025)['rate_pct']
    w03 = next(r for r in H if r['group'] == 'non_hispanic_white' and r['year'] == 2003)['rate_pct']
    b03 = next(r for r in H if r['group'] == 'black' and r['year'] == 2003)['rate_pct']
    assert 29 < w25 - b25 < 30 and (w25 - b25) > (w03 - b03)
    title = 'Non-Hispanic White and Black homeownership rates were nearly 30 points apart in 2025, a wider gap than in 2003.'
    measure = ('Households that own their home, percent, by race and ethnicity of householder, annual averages, '
               'United States, 1994 to 2025. Every panel runs from 40 to 80 percent.')
    body = artboards(view, 'S05', gen_s05, 1024,
                     f'Four small line charts of homeownership, 1994 to 2025. In 2025: non-Hispanic White {w25} percent, Black {b25} percent. The table below carries every value.')
    notes = [f'Gap to non-Hispanic White households, Black: {w03 - b03:.1f} points in 2003, {w25 - b25:.1f} in 2025.',
             'Gap to non-Hispanic White households, Hispanic: 28.7 points in 2003, 25.8 in 2025.',
             'The lines break where the Census changed its method: 2002 shows an original and a reweighted value, and race categories changed in 2003.']
    hisp = {y: next(r for r in H if r['group'] == 'hispanic' and r['year'] == y)['rate_pct'] for y in (2003, 2025)}
    assert round(w03 - hisp[2003], 1) == 28.7 and round(w25 - hisp[2025], 1) == 25.8
    years = sorted({(r['year'], r['series_variant']) for r in H if r['group'] == 'all_households'})
    body_rows = []
    for y, sv in years:
        cells = [str(y) + (' (original)' if sv == 'original' else ' (reweighted)' if sv == 'revised_2000_census' else '')]
        for g in ('all_households', 'non_hispanic_white', 'black', 'hispanic'):
            r = next((r for r in H if r['group'] == g and r['year'] == y and r['series_variant'] == sv), None)
            cells.append(f'{r["rate_pct"]:.1f}' if r else '')
        body_rows.append(cells)
    table = table_html('Homeownership rate, percent', ['Year'] + [HO_GROUP[g] for g in ('all_households', 'non_hispanic_white', 'black', 'hispanic')],
                       body_rows, (1, 2, 3, 4))
    return figure(view, 'S05', title, measure, body, notes, table, wide=True)


def spec_s06(view):
    D = DS['scenarios-2030']
    lift = [r for r in D['rows'] if r['key'] != 'i' and any(r[f'{k}_class'] in ('up', 'slightly up') or
            (r[f'{k}_class'] == 'same as ii' and row('scenarios-2030', 'ii')[f'{k}_class'] in ('up', 'slightly up')) for k in ('DQ', 'GE', 'EP', 'EQ'))]
    others = len(D['rows']) - 1
    assert len(lift) == 5 and others == 7
    title = f'If their assumptions hold, {nw(len(lift))} of the {nw(others)} scenarios beyond the baseline would lift at least one outcome family by 2036.'
    measure = ("The direction each outcome family would take by 2036 under eight scenarios, in the atlas's words, "
               'United States, from a 2026 baseline')
    body = f'<div class="art tbl">{gen_s06_table(view)}</div>'
    why = []
    for r in D['rows']:
        why.append(f'<h4>{e(r["key"])}. {e(r["name"])}</h4><p><b>Assumptions:</b> {e("; ".join(r["assumptions"]))}.</p><ul>')
        for k in ('DQ', 'GE', 'EP', 'EQ'):
            w = r.get(f'{k}_why') or 'The atlas gives no separate reason.'
            why.append(f'<li><b>{e(D["families"][k])}, {e(r[k])}:</b> {e(w)}</li>')
        why.append('</ul>')
    notes = ['Arrow and tint are the studio\'s reading of the atlas\'s words, by the class method in the shared data.',
             D['class_method'], 'Directions hold only if each scenario\'s assumptions hold; they are no forecast and give no odds.',
             'The four families are read separately and never added together. In the baseline, no family rises.']
    table = f'<div class="why">{"".join(why)}</div>'
    return figure(view, 'S06', title, measure, body, notes, table, wide=True)


def spec_s07(view):
    D = rows('rcv-bans')
    nb = sum(1 for r in D if r['prohibits_rcv'])
    na = sum(1 for r in D if r['status'] == 'bans in all elections')
    title = f'{"Nineteen" if nb == 19 else nb} states ban ranked-choice voting as of November 2026, {na} of them in all elections.'
    measure = ('State laws that prohibit ranked-choice voting, by scope, 50 states and the District of Columbia, '
               'as of November 2026. Each square is one state.')
    body = artboards(view, 'S07', gen_s07, 720,
                     f'Tile map of the 50 states and DC: {nb} states ban ranked-choice voting, {na} in all elections. Hover a square for its state. The table below lists every state.')
    some = [r for r in D if r['status'] == 'bans in some elections']
    notes = ['Twelve of the 19 bans became law in 2024 or 2025.', 'Each square is one state, whatever its size.'] + \
            [f'{r["name"]}: {r["scope_note"]}' for r in some] + \
            ['Ballotpedia is a secondary source; the atlas cites the National Conference of State Legislatures, whose page refused automated reading.']
    body_rows = [[r['name'], STATUS_WORD[r['status']], str(r['enacted_year']) if r['enacted_year'] else '', r['measure'] or ''] for r in sorted(D, key=lambda r: r['name'])]
    table = table_html('Ranked-choice voting bans by state', ['State', 'Status', 'Year', 'Measure'], body_rows, (2,))
    return figure(view, 'S07', title, measure, body, notes, table)


def spec_s08(view):
    D = rows('rule-changes')
    pre = Counter(r['direction'] for r in D if r['date'] < '2025-01-01')
    post = Counter(r['direction'] for r in D if r['date'] >= '2025-01-01')
    assert DS['rule-changes']['counts'] == dict(Counter(r['direction'] for r in D))
    title = (f'Since January 2025, {post["away from voters"]} changes in the atlas\'s log moved the rules away from voters '
             f'and {post["toward voters"]} moved them toward voters.')
    measure = ("Each square is one entry in the atlas's repair log, placed by year and by the atlas's direction code, "
               '1965 to the November 3, 2026 ballot. The log is the atlas\'s record and runs denser in recent years.')
    out = []
    for W, cls, keyed in ((1024, 'ab ab-w', True), (600, 'ab ab-m', False), (320, 'ab ab-n', False)):
        art, H = gen_s08(W, f'{view}-s08-{W}', keyed=keyed)
        out.append(art.render(H, 'Unit chart of the 64 repair-log entries by year and direction. The table below lists every entry.', cls, f's08-{view}-{W}'))
    body = f'<div class="art w1024">{"".join(out)}</div>'
    coding = DS['rule-changes']['coding_note']
    extra = (f'<details class="code"><summary>How the atlas codes direction</summary><p>{e(coding)}</p></details>')
    notes = [f'1965 through 2024: {pre["toward voters"]} toward voters, {pre["away from voters"]} away.',
             f'Since January 2025: {post["toward voters"]} toward voters, {post["away from voters"]} away.',
             'Dotted: mid-decade congressional maps, coded away from voters whichever party drew them (Texas and Missouri in 2025, California in 2025 and Virginia in 2026).',
             'Neither way: voters kept existing rules when a ballot measure failed; mixed; pending on November 3, 2026.',
             'Directions are the atlas\'s own codes. The log is denser for recent years and counts what the atlas recorded, not every rule change.']
    body_rows = [[r['key'], date_words(r['date']), r['jurisdiction'], r['instrument_group'], DIR_WORD[r['direction']]] for r in D]
    table = table_html('Every entry in the repair log', ['Entry', 'Date', 'Where', 'Instrument', 'Direction'], body_rows)
    return figure(view, 'S08', title, measure, body, notes, table, wide=True, extra=extra)


def spec_s09(view):
    D = DS['history-events']
    ev = D['rows']
    n1 = sum(1 for r in ev if 1964 <= r['year'] <= 1978)
    n2 = sum(1 for r in ev if 2010 <= r['year'] <= 2026)
    words = {15: 'Fifteen'}
    title = f'{words.get(n1 + n2, n1 + n2)} of the {len(ev)} rule changes the atlas dates since 1870 fall in two stretches: 1964 to 1978 and 2010 to 2026.'
    measure = ('Changes in the rules on four threads, dated by the atlas, United States, February 1870 to June 2026. '
               'Every event is documented; the atlas chose which to date.')
    body = artboards(view, 'S09', gen_s09, 1024,
                     'Timeline of 24 rule changes from 1870 to 2026 on four lanes. The table below lists every event.')
    notes = [f'Shaded: 1964 to 1978 ({n1} changes) and 2010 to 2026 ({n2} changes).', D['events_note'],
             'Event keys E01 to E24 are the studio\'s, in date order. Labels shorten each event\'s name; the table gives it in full.']
    body_rows = [[r['key'], date_words(r['date']), r['thread_label'], r['title'], r['mechanism']] for r in sorted(ev, key=lambda r: r['date'])]
    table = table_html('Twenty-four rule changes since 1870', ['Event', 'Date', 'Thread', 'Change', 'What it did'], body_rows)
    return figure(view, 'S09', title, measure, body, notes, table, wide=True)


def spec_s10(view):
    D = DS['claims-by-grade']
    tot = D['totals']
    n = sum(tot.values())
    share = tot['documented'] / n
    assert 0.72 < share < 0.76
    title = f'About three in four claims behind the atlas\'s {len(D["rows"])} everyday answers are documented on the public record.'
    measure = (f"Claims in the atlas's register by evidence grade, share of each answer's claims, {n} claims, "
               'checked through October 15, 2026, United States')
    body = artboards(view, 'S10', gen_s10, 720,
                     f'Sixteen bars, one per everyday answer, split by evidence grade and sorted by the documented share. Across all {n} claims, {pct0(share * 100)} are documented. The table below carries every value.')
    R = sorted(D['rows'], key=lambda r: (-r['documented'] / r['value'], r['key']))
    notes = [f'All {n} claims: {pct0(share * 100)} documented.', 'Grades are the atlas\'s own; a claim\'s grade covers that claim, not the whole answer.',
             'Clean drinking water has the highest documented share; algorithms in daily life the lowest; pay and working conditions the most contested claims.']
    body_rows = [[r['title'], str(r['value'])] + [str(r[g]) for g in GRADES] + [pct0(r['documented'] / r['value'] * 100)] for r in R]
    table = table_html('Claims by evidence grade for each everyday answer', ['Answer', 'Claims'] + [GRADE_WORD[g] for g in GRADES] + ['Documented share'],
                       body_rows, (1, 2, 3, 4, 5, 6))
    return figure(view, 'S10', title, measure, body, notes, table)


SPEC_FN = {'S01': spec_s01, 'S02': spec_s02, 'S03': spec_s03, 'S04': spec_s04, 'S05': spec_s05,
           'S06': spec_s06, 'S07': spec_s07, 'S08': spec_s08, 'S09': spec_s09, 'S10': spec_s10}


def specimen(view, sid, **kw):
    return (f'<section class="spec" id="{view}-{sid.lower()}" aria-labelledby="{view}-{sid.lower()}-h">'
            f'{strip(view, sid, WHY[sid])}{SPEC_FN[sid](view, **kw)}</section>')


# ------------------------------------------------------------------------------------------------ page frame
def wordmark(height, master, cls):
    """The wordmark master, never live type (as the atlas pick's helper draws it)."""
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    return src.replace('<svg ', f'<svg class="{cls}" data-view="wordmark" width="{w:.0f}" height="{height}" role="img" '
                                f'aria-label="Oath &amp; Action" focusable="false" ', 1)


VIEWS = [('white', 'White'), ('newsprint', 'Newsprint'), ('dark', 'Charcoal'), ('social', 'Social card'), ('system', 'System')]
VIEW_GROUND = {'white': 'white', 'newsprint': 'news', 'dark': 'dark', 'social': 'white', 'system': 'white'}
ORDER = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']


def masthead():
    tabs = ''.join(f'<li><a href="#{v}">{e(t)}</a></li>' for v, t in VIEWS)
    return ('<header class="mast"><div class="wrap mrow">'
            '<a class="wm" href="#white" data-red="signature" aria-label="Oath &amp; Action, chart system 01, first view">'
            f'{wordmark(24, "20261028_Wordmark-24px-Master.svg", "wm24")}{wordmark(16, "20261028_Wordmark-16px-Master.svg", "wm16")}</a>'
            '<p class="run">Chart system 01 · Explainer</p>'
            f'<nav class="tabs" aria-label="Views"><ul>{tabs}</ul></nav></div></header>')


def footer():
    return ('<footer class="foot"><div class="wrap frow">'
            '<p class="src">Data: Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026, and public series from the '
            'U.S. Census Bureau and Ballotpedia retrieved November 6, 2026. Every chart is drawn by a generator in build_concept.py.</p>'
            '<p class="src right">Chart system 01, Explainer. Studio draft for Board 3; titles and notes are drafts by the studio.</p>'
            '</div></footer>')


def view_head(view, eyebrow, h1, deck, links=True, extra=''):
    lk = ''
    if links:
        desc = {'white': 'the ten charts on White', 'newsprint': 'the same ten charts on the warm ground',
                'dark': 'two charts and the dark palette', 'social': 'one chart at 1080 by 1350',
                'system': 'the rules on one sheet, and how to read our charts'}
        items = ''.join(f'<li><a href="#{v}">{e(t)}</a> <span>{e(desc[v])}</span></li>' for v, t in VIEWS if v != view)
        lk = f'<nav class="vlinks" aria-label="Other views of this concept"><p class="eyebrow">Other views</p><ul>{items}</ul></nav>'
    return (f'<header class="vhead"><div><p class="eyebrow">{e(eyebrow)}</p>'
            f'<h1 class="display" id="{view}-h1" tabindex="-1">{e(h1)}</h1><div class="deck">{deck}</div>{extra}</div>{lk}</header>')


def index_nav(view):
    li = ''.join(f'<li><a href="#{view}/{s.lower()}"><b>{s}</b> {e(SPECS[s]["form"])}</a></li>' for s in ORDER)
    return f'<nav class="index" aria-label="The ten charts on this view"><ol>{li}</ol></nav>'


DECK_WHITE = ('<p>Explainer leads with the finding. Each chart opens with the kind of evidence and a sentence that says what the '
              'data shows, then a line that names the measure, unit, place and period. The drawing keeps one subject in Charcoal '
              'against Stone context, and notes inside the plot teach what a reader could otherwise miss. Charts sit in one reading '
              'column, the way an explainer runs, and four break wider where the data needs room. The scenario chart is a table, '
              'because a reader looks it up.</p>'
              '<p>The working red appears once on this view, on the 2021 point that chart S02\'s title names.</p>')


def view_white():
    body = ''.join(specimen('white', s) for s in ORDER)
    return (f'<section class="view" data-view-root="white" data-ground="white" aria-labelledby="white-h1"><div class="wrap">'
            f'{view_head("white", "Chart system 01 · A concept for Board 3", "Explainer", DECK_WHITE)}{index_nav("white")}{body}</div></section>')


def view_newsprint():
    t = GROUNDS['news']
    deck = ('<p>The same ten charts from the same generators, with the ground changed. Gridlines take Stone mixed 70 percent '
            'toward Newsprint, secondary text stays in Deep Stone, which measures '
            f'{contrast(DEEP, NEWS):.2f}:1 here where Stone measures {contrast(STONE, NEWS):.2f}:1, and any text on a light fill turns Charcoal. '
            f'Pillar Red measures {contrast(RED, NEWS):.2f}:1 on Newsprint, under the 3:1 a mark needs, so the one red point takes a '
            '1 px Charcoal keyline.</p>')
    body = ''.join(specimen('newsprint', s) for s in ORDER)
    return (f'<section class="view" data-view-root="newsprint" data-ground="news" aria-labelledby="newsprint-h1" hidden><div class="wrap">'
            f'{view_head("newsprint", "Chart system 01 · Explainer", "On Newsprint", deck)}{index_nav("newsprint")}{body}</div></section>')


def view_dark():
    t = GROUNDS['dark']
    rowsx = ''.join(f'<tr><th scope="row"><span class="swx" style="background:{t[k]}"'
                    f'{" data-red=\"specimen\" data-red-job=\"palette swatch\"" if k == "red" else ""}></span>{e(ROLE_WORDS[k])}</th>'
                    f'<td>{t[k]}</td><td>{e(ROLE_MIX["dark"].get(k, {"ink": "Newsprint", "g": "Charcoal", "red": "Pillar Red"}.get(k, "")))}</td>'
                    f'<td class="num">{contrast(t[k], CHAR):.2f}:1</td></tr>'
                    for k in ('ink', 'sec', 'ctx', 'lt', 'grid', 'red'))
    pal = (f'<div class="tw" role="region" tabindex="0" aria-label="Proposed dark palette, table"><table class="eqt pal">'
           f'<caption>The proposed dark palette, measured on Charcoal</caption><thead><tr><th scope="col">Role</th><th scope="col">Hex</th>'
           f'<th scope="col">Made from</th><th scope="col" class="num">Contrast</th></tr></thead><tbody>{rowsx}</tbody></table></div>')
    deck = ('<p>Two charts with the proposed dark palette. Newsprint carries the subject; Dim Newsprint carries secondary text; '
            'context lines take Stone mixed 35 percent toward Newsprint; gridlines drop to Stone mixed 45 percent toward Charcoal. '
            'On Charcoal, lifted Prussian and lifted Verdigris land too close to tell apart, so dark charts keep to few categories '
            'and label every series directly. The grade ramp steps from Newsprint to Stone mixed 35 percent toward Newsprint, '
            'then Stone, then a hatch, so it keeps its order by lightness.</p>')
    body = specimen('dark', 'S02') + specimen('dark', 'S10')
    return (f'<section class="view" data-view-root="dark" data-ground="dark" aria-labelledby="dark-h1" hidden><div class="wrap">'
            f'{view_head("dark", "Chart system 01 · Explainer", "On Charcoal", deck, extra=pal)}{body}</div></section>')


# ------------------------------------------------------------------------------------------------ social card
def place(dst, src, dx, dy):
    """Copy one Art into another at an offset, keeping its label boxes for the collision check."""
    dst.out.append(f'<g transform="translate({f(dx)} {f(dy)})">' + ''.join(src.out) + '</g>')
    dst.defs += src.defs
    for (x0, y0, x1, y1, s) in src.boxes:
        dst.boxes.append((x0 + dx, y0 + dy, x1 + dx, y1 + dy, s))


def social_card():
    """S01 as a 1080 by 1350 portrait card: the same generator at 1.5 times the type, with the card's own frame."""
    W, H, P = 1080, 1350, 72
    c = Art(W, 'social-card')
    c.rect(0, 0, W, H, 'f-g')
    wm = wordmark(40, '20261028_Wordmark-Display-Master.svg', 'cwm')
    wm_w = float(re.search(r'width="(\d+)"', wm).group(1))
    c.out.append(f'<g data-red="signature" transform="translate({P} {P})">{wm.replace("<svg ", "<svg x=\"0\" y=\"0\" ", 1)}</g>')
    y = P + 40 + 62
    ev = DS['stock-trading-ban']['evidence']
    ew = tw(ev.upper(), 20, 700, track=0.06) + 24
    c.rect(P, y - 26, ew, 36, 'f-ink')
    c.text(P + 12, y, ev, 20, 'ti cap', 700, track=0.06, attrs=' data-role="evidence-label"')
    c.boxes[-1] = (P + 12, y - 0.97 * 20, P + ew - 12, y + 0.25 * 20, ev)
    c.text(P + ew + 16, y, GRADE_LINE['S01'], 22, 'tn', 400)
    y += 82
    title = 'Nearly nine in ten Republican and Democratic voters favored a ban on stock trading by members of Congress.'
    tl = []
    line = ''
    for wd in title.split():
        trial = (line + ' ' + wd).strip()
        if line and tw(trial, 54, 800, tight=True) > W - 2 * P:
            tl.append(line)
            line = wd
        else:
            line = trial
    tl.append(line)
    y = c.block(P, y, tl, 54, 'tb', 800, 59, tight=True, attrs=' data-role="title"') + 48
    c.out.append('<g data-role="measure">')
    y = c.para(P, y, 'Registered voters who favor a ban, by party, in a May 2023 survey; then the 2026 votes in Congress, three years later', W - 2 * P, 24, 'tn', 400, 33)
    c.out.append('</g>')
    y += 40
    t = Type(W - 2 * P, scale=1.25)
    chart, ch = gen_s01(W - 2 * P, 'social-s01', t=t, compact=True)
    place(c, chart, P, y)
    y += ch + 26
    src = 'Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, May 19 to 30, 2023; U.S. House Roll Call 280; U.S. Senate Vote 253; as recorded in Oath & Action, Who Do They Answer To? Systems Atlas V7.'
    n_src = len(wrap(src, W - 2 * P, 20, 400))
    ys = H - P - (n_src - 1) * 28          # the source sits on the card's foot
    assert ys - 40 > y, f'social card runs to {y}'
    c.line(P, ys - 36, W - P, ys - 36, 's-grid')
    c.out.append('<g data-role="source">')
    c.para(P, ys, src, W - 2 * P, 20, 'tn', 400, 28)
    c.out.append('</g>')
    return c.render(H, 'Social card, 1080 by 1350 pixels: ' + title + ' 86 percent of registered voters favored a ban; '
                    '88 percent of Democrats and 87 percent of Republicans. The House passed it 232 to 198; the Senate vote to take it up '
                    'was 53 to 47, 7 short of the 60 needed. Source: Program for Public Consultation survey, May 2023, and the House and Senate roll calls.',
                    'card', 'social-card-1080'), src


def view_social():
    svg, src = social_card()
    R = rows('stock-trading-ban')
    table = table_html('Support for a ban and the votes that followed', ['Group', 'Measure', 'Value'],
                       [[r['group'], r['measure'], str(r['value'])] for r in R], (2,))
    fig = (f'<figure class="cardfig" data-spec="S01" data-dataset="stock-trading-ban" data-evidence="Finding">'
           f'<div class="cardbox" data-ground="news" role="region" tabindex="0" aria-label="Social card at true size, 1080 by 1350 pixels; scroll sideways on a phone">{svg}</div>'
           f'<details class="eq" data-role="equivalent"><summary>Show the table and notes</summary><div class="eqb">'
           f'<ul class="eqn"><li>Survey of 2,625 registered voters, May 19 to 30, 2023, three years before either vote.</li>'
           f'<li>The Senate vote to take up the bill fell 7 votes short of the 60 needed.</li></ul>{table}<p class="src">{e(src)}</p></div></details></figure>')
    deck = ('<p>One chart as a portrait post at 1080 by 1350 pixels, the size Instagram and LinkedIn use. It is chart S01 from the '
            'same generator, with type at one and a quarter times its page size so labels hold at a phone\'s feed width. The card '
            'keeps the evidence label, the title, the measure line, the source and the wordmark, so it still makes sense when '
            'it travels without the page. It sits on Newsprint, the ground a feed of white cards does not use.</p>')
    strip_html = ('<div class="strip"><p class="stag">Studio note, not part of the card</p><h2 class="sid" id="social-s01-h">S01 '
                  '<span>Social card, 1080 by 1350</span></h2><dl><dt>Reader question</dt><dd>Do Republicans and Democrats agree on anything about Congress?</dd>'
                  '<dt>Why this chart</dt><dd>A shared view that both parties hold is the finding most likely to travel, and it takes no side.</dd></dl></div>')
    return (f'<section class="view" data-view-root="social" data-ground="white" aria-labelledby="social-h1" hidden><div class="wrap">'
            f'{view_head("social", "Chart system 01 · Explainer", "Social card", deck)}'
            f'<section class="spec cardspec" aria-labelledby="social-s01-h">{strip_html}{fig}</section></div></section>')


# ------------------------------------------------------------------------------------------------ system sheet
def sys_art(gen, widths, label, name, **kw):
    out = []
    for W, cls in widths:
        a, H = gen(W, f'system-{name}-{W}', **kw)
        out.append(a.render(H, label, cls, f'{name}-system-{W}'))
    return ''.join(out)


def anatomy_art(W, uid):
    a, H = gen_s02(W, uid, anatomy=True)
    for n in range(4, 13):
        cx, cy = a.anchors[f'm{n}']
        a.circle(cx, cy, 10.5, 'f-mk')
        a.text(cx, cy + 4.6, str(n), 13, 'ti', 700, 'middle')
    return a, H


ANATOMY = [
    ('Evidence label', 'The kind of evidence in a Charcoal chip: Finding, Association, Estimate or Illustration. The grade follows in words.'),
    ('Title', 'One sentence that states the finding, in Inter Tight 800. Its verb matches the grade: record words for documented, "can" or "may" for plausible, "would" for a scenario.'),
    ('Measure line', 'The measure, unit, place and period, in Inter 400 Deep Stone. It says when a scale is cropped.'),
    ('Unit on the top tick', 'The unit appears once, on the top tick or the first label. Other ticks stay bare.'),
    ('Gridlines', 'Horizontal 1 px hairlines in the grid tint. No vertical grid and no tick marks.'),
    ('Baseline', 'A 1.5 px Charcoal line at zero. Bars always start here.'),
    ('Subject', 'The series the title names: 3 px Charcoal, labeled directly in Inter 600.'),
    ('Context', 'Other series in 2 px Stone, labeled in Deep Stone. They recede so the subject reads first.'),
    ('The one red point', 'Pillar Red marks only the point the title names, once per view. On Newsprint it takes a 1 px Charcoal keyline.'),
    ('Note and leader', 'Notes sit inside the drawing in Inter 14 px Deep Stone, joined to the data by a 1 px leader.'),
    ('Odd encoding, explained once', 'Here the steps at 2013, 2017 and 2019 are method breaks. The line never bridges them.'),
    ('End note', 'A note in open space names the value a reader would look for, with a leader to the point.'),
    ('Source line and credit', 'Publisher, table, period, geography, date retrieved and the qualification, in that order. The credit sits at right.'),
    ('Table and notes', 'One click opens every value and every note, so the chart has a full equivalent.'),
]


def type_ramp():
    rows_ = [
        ('View title', '<span class="display" style="display:block">Explainer</span>', 'Inter Tight 800, 56/60, −0.035em; 36/40 on phones'),
        ('Chart title', '<span class="ct" style="display:block">A sentence that states the finding.</span>', 'Inter Tight 800, 28/33, −0.02em; 22/27 on phones'),
        ('Evidence label', '<span class="ev">Finding</span>', 'Inter 700, 13/18, capitals, 0.06em; Charcoal chip'),
        ('Measure line', '<span class="ms" style="margin:0">Percent, United States, 2009 to 2025</span>', 'Inter 400, 17/25, Deep Stone; 15/22 on phones'),
        ('Big number', '<span class="bigx">86%</span>', 'Inter Tight 800, 116 px; 88 px on phones'),
        ('Direct label', '<span class="lblx">Supplemental Poverty Measure</span>', 'Inter 600, 15 px, tabular figures; 14 px on phones'),
        ('Tick label', '<span class="tkx">25%  20  15</span>', 'Inter 400, 13 px, Deep Stone; 14 px on phones'),
        ('Note', '<span class="ntx">2021: the expanded credit was in force.</span>', 'Inter 400, 14/19, Deep Stone; note heads Inter 600 Charcoal'),
        ('Source line', '<span class="src">Source: U.S. Census Bureau, P60-290, Table 8.</span>', 'Inter 400, 13/18, Deep Stone'),
        ('Quotation', '<span class="q">\u201cClarity is our duty. Action is our promise.\u201d</span>', 'Lora Italic, quoted words only, never a title'),
    ]
    body = ''.join(f'<tr><th scope="row">{e(n)}</th><td>{s}</td><td>{e(spec)}</td></tr>' for n, s, spec in rows_)
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Type ramp, table"><table class="eqt ramp"><caption>Type ramp</caption>'
            f'<thead><tr><th scope="col">Role</th><th scope="col">Sample</th><th scope="col">Specification</th></tr></thead><tbody>{body}</tbody></table></div>')


def marks_art(W, uid):
    """The mark specifications, drawn by the same kit: a sample at left, its rule at right."""
    a = Art(W, uid)
    narrow = W < 600
    SW = 120 if not narrow else 84
    TX = SW + 16
    y = [18]

    def head(txt):
        a.text(0, y[0], txt, 13, 'te', 700, track=0.06)
        y[0] += 34

    def row(draw, txt):
        base = y[0]
        draw(base)
        last = a.para(TX, base, txt, W - TX, 14, 'tr', 400)
        y[0] = last + 30
    head('LINE FAMILY')
    for wv, name in ((1, 'Gridline and leader, 1 px'), (1.5, 'Baseline and reference, 1.5 px'), (2, 'Context series, 2 px Stone'),
                     (3, 'Subject series, 3 px Charcoal'), (6, 'Selected on an interactive chart, 6 px')):
        cls = 's-ctx' if wv == 2 else 's-sub'
        row(lambda b, wv=wv, cls=cls: a.raw(f'<line x1="0" y1="{f(b - 5)}" x2="{SW}" y2="{f(b - 5)}" class="{cls}" style="stroke-width:{wv}px"/>'), name)
    y[0] += 10
    head('DOTS, BARS AND UNITS')

    def dots(b):
        a.circle(8, b - 5, 6.5, 'f-ink')
        a.circle(32, b - 5, 5.5, 's-open')
        a.circle(54, b - 5, 3, 'f-ink')
    row(dots, 'Dots: 13 px for a subject value, 11 px open for the earlier value, 6 px for a line vertex, 4.5 px in small multiples')
    row(lambda b: a.rect(0, b - 17, SW, 24, 'f-ink'), 'Bars: 24 px with 18 px between rows; 16 px when a chart runs past ten rows; segments meet with no gap')

    def units(b):
        for i in range(4):
            a.rect(i * 17, b - 14, 14, 14, 'f-ink')
    row(units, 'Units: 14 px squares, 3 px apart, one per record')

    def hatch(b):
        a.rect(0, b - 15, SW, 18, 'hatchf', f' style="fill:{a.hatch()}"')
        a.rect(0.75, b - 14.25, SW - 1.5, 16.5, 's-ctx15')
    row(hatch, 'Hatch: 1.5 px Stone at 45 degrees on a 5 px pitch, for the weakest category')

    def dot(b):
        a.rect(0, b - 14, 14, 14, 'f-ink')
        a.circle(7, b - 7, 2.6, 'f-g')
        a.rect(17, b - 14, 14, 14, 'f-ink')
    row(dot, 'Inner dot: a 5 px ground-colored dot inside a unit picks out the records a note names')

    def brk(b):
        a.circle(8, b - 16, 3, 'f-ink')
        a.circle(8, b - 4, 3, 'f-ink')
    row(brk, 'Break: two estimates at one date, never joined by a line')
    return a, y[0] - 30 + 12


def swatch_table(name):
    t = GROUNDS[name]
    g = t['g']
    keys = ['ink', 'sec', 'ctx', 'lt', 'lt2', 'grid', 'band', 'vup', 'vup2', 'sdn2', 'sdn', 'red']
    base_mix = {'ink': 'Charcoal' if name != 'dark' else 'Newsprint', 'sec': 'Deep Stone' if name != 'dark' else 'Dim Newsprint',
                'ctx': 'Stone', 'red': 'Pillar Red'}
    out = []
    for k in keys:
        hexv = t[k]
        cr = contrast(hexv, g)
        if k in ('ink', 'sec'):
            use = 'text' if cr >= 4.5 else 'fails text'
        elif k in ('ctx', 'red'):
            use = 'mark' if cr >= 3 else 'mark with keyline'
        else:
            use = {'lt': 'fill, values printed', 'lt2': 'track behind a printed share', 'grid': 'hairline; values printed',
                   'band': 'background tint behind a note', 'vup': 'cell tint, words printed', 'vup2': 'cell tint, words printed',
                   'sdn': 'cell tint, words printed', 'sdn2': 'cell tint, words printed'}[k]
        made = ROLE_MIX[name].get(k) or base_mix.get(k, '')
        red_attr = ' data-red="specimen" data-red-job="palette swatch"' if k == 'red' else ''
        out.append(f'<tr><th scope="row"><span class="swx" style="background:{hexv}"{red_attr}></span>{e(ROLE_WORDS[k])}</th>'
                   f'<td>{hexv}</td><td>{e(made)}</td><td class="num">{cr:.2f}:1</td><td>{e(use)}</td>'
                   f'<td><span class="swx" style="background:{gray(hexv)}"></span>{gray(hexv)}</td></tr>')
    label = {'white': 'White', 'news': 'Newsprint', 'dark': 'Charcoal'}[name]
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Chart colors on {label}, table"><table class="eqt pal">'
            f'<caption>On {label} ({g})</caption><thead><tr><th scope="col">Role</th><th scope="col">Hex</th><th scope="col">Made from</th>'
            f'<th scope="col" class="num">Contrast</th><th scope="col">Use</th><th scope="col">Grayscale</th></tr></thead>'
            f'<tbody>{"".join(out)}</tbody></table></div>')


def lab_ramps():
    """Sequential and diverging ramps from the palette lab, with its measured contrast, for reference."""
    out = []
    for s in LAB['sets']:
        if s['kind'] not in ('sequential', 'diverging') or s['ground'] not in ('white', 'newsprint'):
            continue
        cells = ''.join(f'<li><span class="swx big" style="background:{w["hex"]}"></span><span>{e(w["label"])}</span>'
                        f'<span class="mono">{w["hex"]} · {w["contrast_on_ground"]:.2f}:1</span></li>' for w in s['swatches'])
        out.append(f'<div class="ramp"><p class="kh">{e(s["name"])}, on {e(s["ground"].capitalize())}. Neighbors at least '
                   f'{s["min_lightness_step"]:.3f} apart in OKLab lightness; grayscale order {"kept" if s["grayscale_monotonic"] else "not kept, so labels carry it"}.</p><ul>{cells}</ul></div>')
    return ''.join(out)


RULE_053 = ("“The wordmark’s ampersand and the lockmark’s lever are signature red and do not count, and neither do the ampersands "
            "inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with "
            "the wordmark and never stands in for the hinge divider. An icon’s red accent counts as signature red when the icon stands "
            "alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one "
            "keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: "
            "an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is "
            "where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline’s ampersand uses "
            "the view’s working red. The hinge divider’s ampersand takes its surface’s ink: Charcoal on Newsprint and White, Newsprint "
            "on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red "
            "never sits on Prussian.”")


def red_demo():
    a1 = sys_art(gen_s02, ((600, 'ab ab-m'), (320, 'ab ab-n')), 'Demonstration: the 2021 point in Pillar Red, the one point the title names.', 'reda', anatomy=True)
    a2 = sys_art(gen_s02, ((600, 'ab ab-m'), (320, 'ab ab-n')), 'Demonstration: the same chart with the 2021 point in Charcoal, because an ask holds the red.', 'redb', red=False)
    return ('<div class="demo"><div class="dpanel"><p class="dlab">Demonstration A, a specimen: red marks the point the title names</p>'
            f'<div class="art w600">{a1}</div><p class="dcap">With nothing else in the view asking for red, the 2021 low takes it. Red points; it never encodes a series.</p></div>'
            '<div class="dpanel"><p class="dlab">Demonstration B, a specimen: an ask takes the red, and the point steps down</p>'
            f'<div class="art w600">{a2}</div><p class="dcap"><span class="askbtn" data-red="specimen" data-red-job="the step a reader can take now">'
            'Find your state’s child poverty rate</span></p><p class="dcap">The step a reader can take now outranks the point the title names, '
            'so the ask keeps the red and the 2021 point turns Charcoal with a ground-colored ring to hold it apart from the line.</p></div></div>')


HOW_TO_READ = [
    ('Start with the label.', 'The black chip says what kind of evidence the chart shows. A Finding is something measured. '
     'An Association is a pattern that does not show one thing caused another. An Estimate says what would happen if something '
     'else happened first. An Illustration shows how a chart works, with made-up numbers.'),
    ('Read the title as the answer.', 'It is one sentence that says what the numbers show. If the title says "would" or "may," the evidence is less certain.'),
    ('Check what was counted.', 'The gray line under the title names what was measured, in what unit, where and when.'),
    ('Look for the dark line.', 'The black line, bar or dot is what the title is about. Gray marks are there for comparison.'),
    ('Read the notes in the chart.', 'Short notes point at the record, the turning point or anything drawn in an unusual way, such as a line that breaks where a survey changed.'),
    ('Red points at one thing.', 'When a chart uses red, it marks the single point the title names. Red never means a party, good or bad.'),
    ('Find where the numbers came from.', 'The source line names who collected the data, when, and what to keep in mind. Open the table to see every value.'),
]


def view_system():
    anat = sys_art(anatomy_art, ((720, 'ab ab-w'), (600, 'ab ab-m'), (320, 'ab ab-n')), 'Anatomy of a chart: chart S02 with its parts numbered 4 to 12; the list beside names each part.', 'anatomy')
    p21 = row('child-poverty-spm', 'spm|2021|standard')['percent']
    anat_fig = ('<div class="anat"><div class="anfig" data-ground="white">'
                '<div class="evrow"><span class="mk">1</span><p class="ev">Finding</p><p class="grade">Official statistic: Census Bureau survey estimates</p></div>'
                f'<p class="ct"><span class="mk">2</span>Child poverty fell to {p21} percent in 2021, the lowest since the series began in 2009, and more than doubled the next year.</p>'
                '<p class="ms"><span class="mk">3</span>Children under 18 below the Supplemental Poverty Measure, percent, United States, 2009 to 2025, with the official measure in gray for comparison</p>'
                f'<div class="art w720">{anat}</div>'
                f'<div class="srcrow"><p class="src"><span class="mk">13</span><span class="sl">Source:</span> {e(source_text("S02"))}</p><p class="src credit">Chart: Oath &amp; Action</p></div>'
                '<p class="fakesum"><span class="mk">14</span>Show the table and notes</p></div>'
                '<ol class="parts">' + ''.join(f'<li><b>{e(n)}.</b> {e(d)}</li>' for n, d in ANATOMY) + '</ol></div>')
    marks = sys_art(marks_art, ((720, 'ab ab-w'), (600, 'ab ab-m'), (320, 'ab ab-n')), 'Mark specifications: line weights, dots, bars, units, hatch, ring and break.', 'marks')
    rules_notes = ''.join(f'<li>{e(x)}</li>' for x in [
        'Name the record, give a reader’s scale, or explain an unusual encoding once. A note that does none of these comes out.',
        'Put the note in open space near its data and join it with a 1 px Stone leader. Leaders run straight or with one bend, never across a label.',
        'Notes are Inter 14 px in Deep Stone; a note head that states a number is Inter 600 in Charcoal.',
        'State the qualification in the drawing when it changes the reading: self-reported rates, method breaks, a survey older than the votes.',
        'A note may say what a measure did over time. It never says a policy caused it unless the source grades that cause.',
        'Label series at the line or the bar. Use a key only when labels cannot fit, and draw the key in the chart’s own marks.'])
    rules_src = ''.join(f'<li>{e(x)}</li>' for x in [
        'Order: publisher, title or table, observation period, geography, date retrieved, qualification (Master Brief section 15).',
        'Start from the dataset’s source line. Shorten only by dropping words, never facts. Dates read as words: October 15, 2026.',
        'Inter 400, 13/18, Deep Stone, under a grid-tint hairline, with "Chart: Oath & Action" at the right.',
        'A secondary source says so in the line, as the ranked-choice map does for Ballotpedia.',
        'The table under every chart repeats the source, so the equivalent stands on its own.'])
    read = ''.join(f'<li><b>{e(h)}</b> {e(d)}</li>' for h, d in HOW_TO_READ)
    deck = ('<p>Everything a builder needs to make the next chart in this system, and a short guide for the people who read them. '
            'Every drawing on this sheet comes from the same generators as the ten charts.</p>')
    return (f'<section class="view" data-view-root="system" data-ground="white" aria-labelledby="system-h1" hidden><div class="wrap">'
            f'{view_head("system", "Chart system 01 · Explainer", "The system on one sheet", deck)}'
            f'<section class="ssec" aria-labelledby="sys-anat"><h2 class="headline" id="sys-anat">Anatomy of a chart</h2>'
            f'<p class="lede">Chart S02 with every part numbered. The red point here is a specimen, so it does not count toward this view’s red.</p>{anat_fig}</section>'
            f'<section class="ssec" aria-labelledby="sys-type"><h2 class="headline" id="sys-type">Type</h2>'
            f'<p class="lede">The locked faces only. Inter Tight sets titles and big numbers, Inter sets every label and number with tabular figures and a true minus (−), and Lora Italic appears only for quoted words. Nothing on screen goes under 13 px; phone drawings set nothing under 14 px so they hold 13 px on a 320 px phone.</p>{type_ramp()}</section>'
            f'<section class="ssec" aria-labelledby="sys-marks"><h2 class="headline" id="sys-marks">Marks</h2>'
            f'<p class="lede">Line weights follow the studio’s family of 1, 1.5, 2, 3 and 6 px (D2-60).</p><div class="art w720">{marks}</div></section>'
            f'<section class="ssec" aria-labelledby="sys-color"><h2 class="headline" id="sys-color">Color, measured on each ground</h2>'
            f'<p class="lede">Every chart color is a role, and every tint is an OKLab mix of locked colors with one job. Contrast is measured against the ground (WCAG 2.x). '
            f'Text needs 4.5:1; a mark needs 3:1; a fill under 3:1 is used only where every value is printed or the table carries it, which is a design judgment. '
            f'Categories never rest on Verdigris against Stone alone: they sit {abs(oklab(VERD)[0] - oklab(STONE)[0]):.2f} apart in OKLab lightness, so position or a label carries them too.</p>'
            f'<div class="pals">{swatch_table("white")}{swatch_table("news")}{swatch_table("dark")}</div>'
            f'<h3 class="sub">Ramps from the palette lab</h3><p class="lede">The scenario table (S06) uses diverging A, read as Stone for down and Verdigris for up, with an arrow in every cell. Diverging B is the two-sided alternative for Board 3. Neither pairs red with blue.</p>{lab_ramps()}</section>'
            f'<section class="ssec" aria-labelledby="sys-notes"><h2 class="headline" id="sys-notes">Notes and source lines</h2>'
            f'<div class="two"><div><h3 class="sub">Notes in the drawing</h3><ul class="rl">{rules_notes}</ul></div>'
            f'<div><h3 class="sub">Source lines</h3><ul class="rl">{rules_src}</ul></div></div></section>'
            f'<section class="ssec" aria-labelledby="sys-red"><h2 class="headline" id="sys-red">Red, once</h2>'
            f'<p class="lede">Rule 05.3, as Dustin approved it (D2-01):</p><blockquote class="q rule">{e(RULE_053)}</blockquote>'
            f'<p class="lede">On a chart page each chart counts as one view. In this concept the working red goes to one chart per page view, S02, on the point its title names. Party marks, grades, scales and categories never take red.</p>{red_demo()}</section>'
            f'<section class="ssec" aria-labelledby="sys-read"><h2 class="headline" id="sys-read">How to read our charts</h2>'
            f'<p class="lede">For readers, in plain words. This text can run under any chart or on a help page.</p><ol class="read">{read}</ol></section>'
            '</div></section>')


# ------------------------------------------------------------------------------------------------ CSS and JS
def ground_css():
    out = []
    for name in ('white', 'news', 'dark'):
        out.append(f'[data-ground="{name}"]{{{css_vars(name)}}}')
    return '\n'.join(out)


CSS = r"""
html{-webkit-text-size-adjust:100%;background:var(--g)}
body{margin:0;background:var(--g);color:var(--ink);font:400 17px/27px Inter,system-ui,sans-serif}
*,*::before,*::after{box-sizing:border-box}
[data-view-root]{background:var(--g);color:var(--ink)}
[hidden]{display:none!important}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.skip{position:absolute;left:16px;top:-200px;z-index:200;padding:10px 14px;background:var(--g);border:2px solid var(--ink);font:600 15px/1 Inter,sans-serif;color:var(--ink)}
.skip:focus{top:12px}
.vh2{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
/* masthead, after the atlas pick */
.mast{border-bottom:1px solid var(--rule);background:var(--g)}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;color:var(--ink);padding:0}
.wm16{display:none}
.run{margin:0 0 0 48px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.tabs ul{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;min-height:44px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:var(--ink)}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ink)}
.tabs a:hover{text-decoration:underline}
/* view head */
.view{padding:40px 0 96px}
.vhead{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:24px 64px;align-items:end;padding-bottom:32px;border-bottom:2px solid var(--ink)}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;margin-left:-.04em}
.display:focus{outline:none}
.deck p{margin:16px 0 0;font:400 19px/28px Inter,sans-serif;max-width:40em}
.deck p+p{font-size:17px;line-height:26px;color:var(--sec)}
.vlinks ul{margin:0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.vlinks li{padding:8px 0;border-bottom:1px solid var(--grid);font:400 15px/22px Inter,sans-serif;color:var(--sec)}
.vlinks a{display:inline-flex;align-items:center;min-height:24px;font-weight:600;color:var(--ink);margin-right:6px}
.index ol{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0 24px;margin:20px 0 0;padding:0;list-style:none}
.index li{border-bottom:1px solid var(--grid)}
.index a{display:flex;gap:8px;align-items:center;min-height:44px;font:400 15px/20px Inter,sans-serif;text-decoration:none}
.index a b{font:800 15px/20px "Inter Tight",sans-serif}
.index a:hover{text-decoration:underline}
.headline{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;text-wrap:balance}
.lede{margin:12px 0 0;font:400 17px/27px Inter,sans-serif;max-width:46em}
.sub{margin:28px 0 8px;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.q{font:italic 400 19px/29px Lora,serif}
/* a specimen: the studio strip at left, the chart in the reading column */
.spec{display:grid;grid-template-columns:232px minmax(0,1fr);column-gap:56px;margin-top:72px;padding-top:20px;border-top:1px solid var(--ink)}
.index+.spec{margin-top:48px}
.strip{align-self:start;position:sticky;top:20px;border:1px dashed var(--ctx);padding:12px 14px 2px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.stag{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.sid{margin:0 0 12px;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em;color:var(--ink)}
.sid span{display:block;margin-top:2px;font:600 15px/20px Inter,sans-serif;letter-spacing:0}
.strip dl{margin:0}.strip dt{font-weight:700;color:var(--ink)}.strip dd{margin:0 0 12px}
.fig{margin:0;max-width:720px}
.fig.wide{max-width:1024px}
.evrow{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;margin:0 0 12px}
.ev{margin:0;display:inline-flex;align-items:center;min-height:24px;padding:3px 8px;background:var(--chip);color:var(--chipfg);font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.grade{margin:0;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.ct{margin:0;font:800 28px/33px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em;text-wrap:balance;max-width:30em}
.ms{margin:10px 0 0;font:400 17px/25px Inter,sans-serif;color:var(--sec);max-width:42em}
.art{margin:28px 0 0;container-type:inline-size}
.art .ab{display:none}
.art .ab-n{display:block;width:100%;max-width:440px;height:auto}
@container (min-width:600px){.art .ab-n{display:none}.art .ab-m{display:block}}
@container (min-width:720px){.art.w720 .ab-m{display:none}.art.w720 .ab-w{display:block}}
@container (min-width:1024px){.art.w1024 .ab-m{display:none}.art.w1024 .ab-w{display:block}}
svg.ab{overflow:hidden}
svg text{font-family:Inter,system-ui,sans-serif;font-variant-numeric:tabular-nums}
.tl,.th{font-weight:600;fill:var(--ink)}.tr{font-weight:400;fill:var(--ink)}.tk,.tn{font-weight:400;fill:var(--sec)}
.ts{font-weight:600;fill:var(--sec)}.te{font-weight:700;fill:var(--sec);letter-spacing:.06em}
.tb{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;fill:var(--ink);letter-spacing:-.02em}
.ti{font-weight:600;fill:var(--inv)}.ti4{font-weight:400;fill:var(--inv)}.cap{text-transform:uppercase;letter-spacing:.06em}
.f-ink{fill:var(--ink)}.f-ctx{fill:var(--ctx)}.f-lt{fill:var(--lt)}.f-lt2{fill:var(--lt2)}.f-g{fill:var(--g)}.f-band{fill:var(--band)}
.f-mk{fill:var(--ink)}.nofill{fill:none}
.s-grid{stroke:var(--grid);stroke-width:1px;fill:none;vector-effect:non-scaling-stroke}
.s-base{stroke:var(--ink);stroke-width:1.5px;fill:none;vector-effect:non-scaling-stroke}
.s-ld{stroke:var(--ctx);stroke-width:1px;fill:none;vector-effect:non-scaling-stroke}
.s-mark{stroke:var(--ink);stroke-width:1.5px;fill:none;vector-effect:non-scaling-stroke}
.s-ring{stroke:var(--ink);stroke-width:1px;fill:none;vector-effect:non-scaling-stroke}
.s-sub{stroke:var(--ink);stroke-width:3px;fill:none;stroke-linejoin:round;stroke-linecap:round}
.s-ctx{stroke:var(--ctx);stroke-width:2px;fill:none;stroke-linejoin:round;stroke-linecap:round}
.s-ctx15{stroke:var(--ctx);stroke-width:1.5px;fill:none;stroke-linejoin:round}.s-ctx15h{stroke:var(--ctx);stroke-width:1.5px}
.s-ink2{stroke:var(--ink);stroke-width:2px}
.s-dash{stroke:var(--ctx);stroke-width:1.5px;stroke-dasharray:3 2;fill:none}
.s-open{stroke:var(--ctx);stroke-width:2px;fill:var(--g)}.s-ring2{stroke:var(--ctx);stroke-width:2px;fill:none}
.s-gring{stroke:var(--g);stroke-width:2px}
.s-none{stroke:none}
.p-bg{fill:var(--g)}.p-ln{stroke:var(--ctx);stroke-width:1.5px}
.redpt{fill:var(--red)}
[data-ground="news"] .redpt{stroke:#121212;stroke-width:1px}
.tile:hover rect{stroke:var(--ink);stroke-width:2px}
.code{margin:14px 0 0;font:400 15px/23px Inter,sans-serif;max-width:46em}
.code summary,.eq summary{display:flex;align-items:center;min-height:44px;font:600 15px/20px Inter,sans-serif;cursor:pointer;width:max-content;max-width:100%}
.code p{margin:4px 0 0;color:var(--ink)}
.srcrow{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-top:20px;padding-top:10px;border-top:1px solid var(--grid)}
.src{margin:0;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.src .sl{font-weight:600;color:var(--ink)}
.credit{white-space:nowrap}
.eq{margin-top:6px;border-bottom:1px solid var(--grid)}
.eqb{padding:4px 0 20px}
.eqh{margin:4px 0 4px;font:600 15px/22px Inter,sans-serif}
.eqn{margin:0 0 16px;padding-left:18px;font:400 15px/22px Inter,sans-serif}
.eqb>.src{margin-top:12px}
.tw{overflow-x:auto;max-width:100%}
table.eqt{border-collapse:collapse;width:100%;font:400 14px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
table.eqt caption{text-align:left;font:600 15px/22px Inter,sans-serif;padding:0 0 8px}
table.eqt th,table.eqt td{padding:6px 14px 6px 0;border-top:1px solid var(--grid);text-align:left;vertical-align:top}
table.eqt thead th{border-top:1px solid var(--ink);font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
table.eqt tbody th{font-weight:600}
.num{text-align:right!important}
/* S06: the comparison table */
.art.tbl{margin-top:20px}
.cmpkey{margin:0 0 14px}
.kh{margin:0 0 8px;font:600 14px/20px Inter,sans-serif}
.cmpkey ul{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.cmpkey li{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 8px;font:400 14px/20px Inter,sans-serif}
.gl{flex:none;fill:currentColor;color:var(--ink)}
table.cmp{border-collapse:separate;border-spacing:3px;width:100%;margin:0 -3px;font:400 15px/21px Inter,sans-serif}
table.cmp thead th{padding:0 10px 6px;text-align:left;vertical-align:bottom;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid var(--ink)}
table.cmp tbody th{padding:10px 14px 10px 0;text-align:left;vertical-align:top;font:600 15px/21px Inter,sans-serif;width:23%;border-bottom:1px solid var(--grid)}
table.cmp .sk{display:inline-block;min-width:34px;font:800 15px/21px "Inter Tight",sans-serif}
table.cmp td{padding:9px 10px 11px;vertical-align:top}
.gw{display:flex;align-items:center;margin:0 0 4px}
.c-up{background:var(--vup)}.c-up2{background:var(--vup2)}.c-dn{background:var(--sdn)}.c-dn2{background:var(--sdn2)}
.c-flat,.c-mix,.c-same{background:var(--g);box-shadow:inset 0 0 0 1px var(--grid)}
.tnote{margin:14px 0 0;font:400 15px/23px Inter,sans-serif;max-width:46em}
@container (max-width:760px){
 table.cmp,table.cmp tbody,table.cmp tr,table.cmp th,table.cmp td{display:block;width:auto}
 table.cmp{margin:0;border-spacing:0}
 table.cmp thead{display:none}
 table.cmp tr{margin:0 0 18px;border-top:2px solid var(--ink);padding-top:8px}
 table.cmp tbody th{border:0;padding:0 0 8px;width:auto}
 table.cmp td{margin:0 0 4px}
 table.cmp td::before{content:attr(data-label);display:block;margin-bottom:4px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
}
.why h4{margin:16px 0 4px;font:600 15px/22px Inter,sans-serif}
.why p,.why li{font:400 14px/21px Inter,sans-serif;margin:0 0 4px}
.why ul{margin:0;padding-left:18px}
/* social */
.cardspec .strip{position:static}
.cardfig{margin:0;max-width:1082px}
.cardbox{overflow:auto;max-width:100%;border:1px solid var(--rule);background:var(--g)}
.cardbox svg{display:block;width:1080px;height:1350px;max-width:none}
/* system */
.ssec{margin-top:80px;padding-top:16px;border-top:2px solid var(--ink)}
.anat{display:grid;grid-template-columns:minmax(0,720px) minmax(0,1fr);gap:48px;margin-top:28px;align-items:start}
.anfig .ct,.anfig .ms,.anfig .src{position:relative}
.mk{display:inline-flex;align-items:center;justify-content:center;width:21px;height:21px;margin-right:8px;border-radius:50%;background:var(--ink);color:var(--g);font:700 13px/1 Inter,sans-serif;vertical-align:3px;letter-spacing:0}
.ct .mk{vertical-align:6px}
.fakesum{margin:10px 0 0;font:600 15px/20px Inter,sans-serif;display:flex;align-items:center}
.parts{margin:0;padding-left:28px;font:400 15px/22px Inter,sans-serif}
.parts li{margin:0 0 10px}
.ramp,.pal{margin-top:12px}
table.ramp td:nth-child(2){min-width:280px}
.bigx{font:800 48px/50px "Inter Tight",sans-serif;letter-spacing:-.02em}
.lblx{font:600 15px/20px Inter,sans-serif}.tkx{font:400 13px/18px Inter,sans-serif;color:var(--sec);white-space:pre}
.ntx{font:400 14px/19px Inter,sans-serif;color:var(--sec)}
.pals{display:grid;gap:32px;margin-top:20px}
.swx{display:inline-block;width:18px;height:18px;margin-right:8px;vertical-align:-4px;border:1px solid var(--grid)}
.swx.big{width:40px;height:28px;margin:0}
.ramp ul{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin:0 0 20px;padding:0;list-style:none}
.ramp li{display:grid;gap:4px;font:400 14px/20px Inter,sans-serif}
.mono{color:var(--sec);font-size:13px;line-height:18px;font-variant-numeric:tabular-nums}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px}
.rl{margin:0;padding-left:20px;font:400 16px/25px Inter,sans-serif}.rl li{margin-bottom:8px}
blockquote.rule{margin:16px 0 0;padding-left:20px;border-left:3px solid var(--ink);max-width:46em;font-size:18px;line-height:28px}
.demo{display:grid;grid-template-columns:repeat(2,minmax(0,600px));gap:48px;margin-top:28px}
.dlab{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.dcap{margin:12px 0 0;font:400 15px/23px Inter,sans-serif}
.askbtn{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;background:var(--red);color:#121212;font:700 19px/1 Inter,sans-serif}
.read{margin:20px 0 0;padding-left:24px;max-width:46em;font:400 17px/27px Inter,sans-serif}
.read li{margin-bottom:10px}
/* footer */
.foot{border-top:1px solid var(--rule);background:var(--g)}
.frow{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:24px;padding-top:16px;padding-bottom:40px}
.foot .right{text-align:right}
@media (max-width:1199.98px){
 .spec{grid-template-columns:minmax(0,1fr)}
 .strip{position:static;margin-bottom:24px;max-width:720px}
 .index ol{grid-template-columns:repeat(2,minmax(0,1fr))}
 .anat,.demo{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:899.98px){
 .wrap{padding:0 16px}
 .mrow{grid-template-columns:1fr;gap:8px;padding-top:16px}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
 .vhead{grid-template-columns:minmax(0,1fr)}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline{font-size:30px;line-height:34px}
 .deck p{font-size:17px;line-height:26px}
 .ct{font-size:22px;line-height:27px}
 .ms{font-size:15px;line-height:22px}
 .index ol{grid-template-columns:minmax(0,1fr)}
 .spec{margin-top:56px}
 .srcrow{flex-direction:column;gap:4px}
 .two,.frow{grid-template-columns:minmax(0,1fr)}
 .foot .right{text-align:left}
 .ramp ul{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:339.98px){.wrap{padding:0 8px}}
"""

JS = r"""
(function(){
  'use strict';
  var VIEWS=['white','newsprint','dark','social','system'], GROUND={white:'white',newsprint:'news',dark:'dark',social:'white',system:'white'};
  var last=null;
  function parse(){var p=decodeURIComponent(location.hash.slice(1)).toLowerCase().split('/'); var v=VIEWS.indexOf(p[0])>=0?p[0]:'white'; return {v:v,sub:p[1]||null};}
  function show(){
    var p=parse();
    [].forEach.call(document.querySelectorAll('[data-view-root]'),function(r){r.hidden=r.getAttribute('data-view-root')!==p.v;});
    document.documentElement.setAttribute('data-ground',GROUND[p.v]);
    [].forEach.call(document.querySelectorAll('.tabs a'),function(a){ if(a.getAttribute('href')==='#'+p.v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');});
    if(p.sub){var t=document.getElementById(p.v+'-'+p.sub); if(t){t.scrollIntoView({block:'start'}); var h=t.querySelector('h2'); if(h){h.setAttribute('tabindex','-1'); h.focus({preventScroll:true});}}}
    else if(last!==null&&last!==p.v){window.scrollTo(0,0); var h1=document.getElementById(p.v+'-h1'); if(h1) h1.focus({preventScroll:true});}
    last=p.v;
  }
  addEventListener('hashchange',show);
  var skip=document.querySelector('.skip');
  if(skip) skip.addEventListener('click',function(ev){ev.preventDefault(); var h=document.getElementById(parse().v+'-h1'); if(h){h.focus(); h.scrollIntoView({block:'start'});}});
  show();
})();
"""


def build():
    views = ' '.join(v for v, _ in VIEWS)
    page = ('<!doctype html><html lang="en" data-ground="white"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Explainer Chart System</title>'
            f'<meta name="chart-views" content="{views}">'
            '<meta name="description" content="Chart system 01, Explainer, for the Oath &amp; Action brand guide: ten charts that lead with the finding, on White, Newsprint and Charcoal, with a social card and the system sheet.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800'
            '&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{ground_css()}{CSS}</style></head><body>'
            '<a class="skip" href="#white">Skip to the view</a>'
            + masthead() + '<main id="main">'
            + view_white() + view_newsprint() + view_dark() + view_social() + view_system()
            + '</main>' + footer() + f'<script>{JS}</script></body></html>')
    text_only = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    assert '—' not in text_only, 'em dash in page'
    for m in re.finditer(r'(?:(?<=\s)|(?<=\())-\d', re.sub(r'<[^>]+>', ' ', text_only)):
        raise AssertionError(f'hyphen used as a minus: {text_only[m.start() - 20:m.end() + 10]}')
    OUT.write_text(page)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1024:.0f} KB')


if __name__ == '__main__':
    build()
