"""Build chart system concept 01, Explainer, for the data visualization round (November 6, 2026; DR-44 to DR-51).

The concept leads with the finding. Every chart opens with its evidence label and a sentence title, then a measure
line, then a drawing with one dark subject against gray context. Short labels and notes inside the drawing do the
teaching; longer notes sit in HTML under the drawing, where they wrap. Charts sit in one reading column, as in a
newspaper explainer, and four break wider. Tables appear where a reader would look something up.

Every chart is drawn by a generator function from the shared chart dataset, never by hand. A generator takes the
artboard width and returns an Art: an SVG drawing that measures its labels with the Inter font files and refuses to
build if a label collides with another label, leaves the drawing, or is crossed by a rule, leader, baseline or data
line (a gridline may pass behind a label, which carries a ground-colored knockout). Label boxes carry 15 percent
headroom for readers who widen text spacing. Each figure carries artboards at its full width, 600, 358 and 328 px;
container queries show the one that fits at its natural size, so a drawing never scales up. Colors are CSS custom
properties set per ground (White, Newsprint, Charcoal), so the same markup redraws on any ground. Every size the
generators use lives in CHART_TOKENS, which the system sheet also reads. These functions are the seed of the chart
kit (DR-49).

Every value is read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json. Titles, measure lines and
notes are studio drafts.

Run from the project root:
    python3 -I work/boards/phase-2/data-viz/01-explainer/build_concept.py
Writes 20261106_Data-Viz-01-Explainer.html beside this file.
"""
import datetime
import html
import itertools
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
MINUS = '\u2212'

# ------------------------------------------------------------------------------------------------ chart tokens
# Every size a generator draws with, in one place. The system sheet prints from this dict, so the sheet and the
# drawings cannot disagree (F16).
CHART_TOKENS = {
    'artboard': {'wide': 1024, 'reading': 720, 'mid': 600, 'phone': 358, 'small_phone': 328},
    'type': {'label': 15, 'tick': 13, 'note': 14, 'note_leading': 19, 'phone_min': 14, 'tile_code_phone': 13,
             'big': 116, 'big_phone': 88, 'eyebrow': 13, 'title': (28, 32), 'title_phone': (22, 27), 'measure': (17, 27)},
    'line': {'hairline': 1, 'baseline': 1.5, 'context': 2, 'subject': 3, 'selected': 6},
    'dot': {'subject_r': 6.5, 'open_r': 5.5, 'vertex_r': 3, 'small_vertex_r': 2.25},
    'bar': {'height': 24, 'pitch': 42, 'dense_height': 16, 'dense_pitch': 36, 'phone_height': 20, 'phone_pitch': 58},
    'unit': {'size': 14, 'gap': 3},
    'note': {'width': 520, 'min_chars': 45, 'max_chars': 75, 'gap': 10, 'leader_min': 12},
    'guard': {'headroom': 1.15, 'line_pad': 1.0},
    'halo': 4,
    'hatch': {'pitch': 5, 'weight': 1.5},
    'keyline': 1,
    'gap_years': 1,          # the unit chart gives each year its own column after the last run of two or more empty years
}
TK = CHART_TOKENS


# ------------------------------------------------------------------------------------------------ copy
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']
ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
        'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def date_words(iso):
    y, m, d = iso.split('-')
    return f'{MONTHS[int(m) - 1]} {int(d)}, {y}'


def copy(s):
    """The one copy function: ISO dates in words, curly quotes and apostrophes, the true minus before a figure, and
    no line break inside a date."""
    s = str(s)
    s = re.sub(r'\b(\d{4})-(\d{2})-(\d{2})\b', lambda m: date_words(m.group(0)), s)
    s = re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", '\u2018\\1\u2019', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '\u2019', s)
    s = re.sub(r'"([^"<>]*)"', '\u201c\\1\u201d', s)
    s = re.sub(r'(?<![\w.\-])-(?=\d)', MINUS, s)
    s = re.sub(r'\b(' + '|'.join(MONTHS) + r') (\d{1,2}), (\d{4})', '\\1\u00a0\\2,\u00a0\\3', s)
    return s


def e(s):
    """Escape reader-facing copy after the copy function."""
    return html.escape(copy(s), quote=True)


def ea(s):
    """Escape a data attribute exactly as the data has it."""
    return html.escape(str(s), quote=True)


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def num_word(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ('-' + ONES[n % 10] if n % 10 else '')
    raise ValueError(f'{n} opens a sentence; rewrite the sentence so it does not start with a figure')


def nw(n, cap=False, start=False):
    """Numbers under ten in words; any number that opens a sentence in words (to 99, else the build stops)."""
    w = num_word(n) if (n < 10 or start) else str(n)
    return w[0].upper() + w[1:] if cap else w


def pct0(v):
    return f'{round(v):d}%'


def frac_year(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    start = datetime.date(y, 1, 1)
    return y + (datetime.date(y, m, d) - start).days / (datetime.date(y + 1, 1, 1) - start).days


def rows(did):
    return DS[did]['rows']


def row(did, key):
    return next(r for r in DS[did]['rows'] if r['key'] == key)


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
    return ';'.join(f'--{k}:{v}' for k, v in GROUNDS[name].items())


# ------------------------------------------------------------------------------------------------ text metrics
# Fonts are measured from the kit's own copy when it is present (found relative to this script), then from the
# system copy. If neither holds all four files, the build stops and names the files it needs.
FONT_FILES = {400: 'Inter-Regular.otf', 600: 'Inter-SemiBold.otf', 700: 'Inter-Bold.otf', 800: 'Inter-ExtraBold.otf'}
FONT_DIRS = [HERE / 'fonts', ROOT / 'work/build/assets/fonts/inter', pathlib.Path('/usr/share/fonts/opentype/inter')]


def font_dir():
    for d in FONT_DIRS:
        if all((d / n).exists() for n in FONT_FILES.values()):
            return d
    need = ', '.join(str((FONT_DIRS[1] / n).relative_to(ROOT)) for n in FONT_FILES.values())
    raise SystemExit(f'Inter 4.0 font files not found. Put {need} in place and run again.')


FONTDIR = font_dir()
_FONTS = {}
NUMERIC = re.compile(r'^[\d\s.,%+\u2212$:()\u2013-]*\d[\d\s.,%+\u2212$:()\u2013-]*$')


def is_num(s):
    """A string of figures: it takes tabular figures; words never do, so hyphens keep their width (F18)."""
    return bool(NUMERIC.match(s))


def _font(weight):
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / FONT_FILES[weight]), 200, layout_engine=ImageFont.Layout.RAQM)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False, track=0.0):
    """Rendered width of a string in Inter, with tabular figures only when the string is a number."""
    w = _font(weight).getlength(text, features=['tnum'] if is_num(text) else None) * size / 200
    if tight:
        w *= 0.955     # Inter Tight runs about 4.5 percent narrower than Inter at the same weight
    return w + track * size * max(len(text) - 1, 0)


def wrap(text, width, size, weight=400):
    """Wrap on ordinary spaces only, so a date set with no-break spaces stays on one line."""
    out, line = [], ''
    for word in copy(text).split(' '):
        trial = (line + ' ' + word).strip(' ')
        if line and tw(trial, size, weight) > width:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


def spread(ideal, size, lo, hi, gap=0.0):
    """Place intervals near their ideal centers without overlap, inside [lo, hi]. Returns the centers."""
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
    """Type sizes for one artboard. Phone artboards (under 600 px) set nothing under 14 px; the tile map's state
    codes are the one 13 px exception."""

    def __init__(self, W, scale=1.0):
        T = TK['type']
        self.narrow = W < 600
        self.s = scale
        self.lbl = T['label'] * scale if not self.narrow else T['phone_min']
        self.tk = T['tick'] * scale if not self.narrow else T['phone_min']
        self.nt = T['note'] * scale if not self.narrow else T['phone_min']
        self.lh = round(self.nt * 1.36)
        self.eb = T['eyebrow'] * scale


LINE_KIND = {'s-grid': 'grid', 's-base': 'rule', 's-mark': 'rule', 's-ld': 'rule', 's-ring': 'rule', 's-redk': 'rule',
             's-sub': 'data', 's-ctx': 'data', 's-ctx15': 'data'}


def _path_segments(d):
    toks = re.findall(r'[MLHVZ]|-?\d+(?:\.\d+)?', d)
    segs, x, y, i, start = [], 0.0, 0.0, 0, None
    cmd = None
    while i < len(toks):
        t = toks[i]
        if t in 'MLHVZ':
            cmd = t
            i += 1
            if cmd == 'Z' and start:
                segs.append((x, y, start[0], start[1]))
                x, y = start
            continue
        if cmd == 'M':
            x, y = float(toks[i]), float(toks[i + 1])
            start = (x, y)
            i += 2
            cmd = 'L'
        elif cmd == 'L':
            nx, ny = float(toks[i]), float(toks[i + 1])
            segs.append((x, y, nx, ny))
            x, y = nx, ny
            i += 2
        elif cmd == 'H':
            nx = float(toks[i])
            segs.append((x, y, nx, y))
            x = nx
            i += 1
        elif cmd == 'V':
            ny = float(toks[i])
            segs.append((x, y, x, ny))
            y = ny
            i += 1
        else:
            i += 1
    return segs


def _seg_hits_box(x1, y1, x2, y2, b):
    """Liang-Barsky: does the segment enter the box (x0, y0, x1, y1)?"""
    bx0, by0, bx1, by1 = b
    if bx1 <= bx0 or by1 <= by0:
        return False
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


class Art:
    """One SVG artboard. Every text call measures the label; check() refuses a drawing where two labels collide, a
    label leaves the drawing, or a rule, leader, baseline or data line crosses a label (a gridline may pass behind a
    label, which carries a ground-colored knockout). Label boxes carry the guard's headroom."""

    def __init__(self, W, uid, t=None):
        self.W, self.uid = W, uid
        self.t = t or Type(W)
        self.out, self.defs, self.boxes, self.segs = [], [], [], []
        self.anchors = {}
        self.strings = []
        self.lpad = 0.0      # room left of x = 0 for a big number set optically flush (its side bearing)

    # text -------------------------------------------------------------------------------------------
    def _box(self, x0, w, y, size, s, halo, track_exempt=False):
        hw = w * (1 if track_exempt else TK['guard']['headroom'])
        self.boxes.append((x0, y - 0.97 * size, x0 + hw, y + 0.25 * size, s, halo))

    def text(self, x, y, s, size, cls='tl', weight=600, anchor='start', attrs='', tight=False, track=0.0,
             on_mark=False, bearing=0.0, box=True):
        s = copy(s)
        w = tw(s, size, weight, tight, track)
        hw = w * TK['guard']['headroom']
        if bearing < 0 and x + bearing < 0:
            self.lpad = max(self.lpad, -(x + bearing))
        x0 = {'start': x, 'middle': x - hw / 2, 'end': x - hw}[anchor]
        if box:
            self.boxes.append((x0, y - 0.97 * size, x0 + hw, y + 0.25 * size, s, not on_mark))
        self.strings.append(s)
        cl = cls + (' num' if is_num(s) else '') + (' nh' if on_mark else '')
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        self.out.append(f'<text x="{f(x + bearing)}" y="{f(y)}" class="{cl}" font-size="{f(size)}"{a}{attrs}>'
                        f'{html.escape(s)}</text>')
        return w

    def rich(self, x, y, parts, size, anchor='start', attrs='', on_mark=False):
        """One line in mixed weights: parts are (text, class, weight)."""
        parts = [(copy(p[0]), p[1], p[2]) for p in parts]
        w = sum(tw(p[0], size, p[2]) for p in parts)
        hw = w * TK['guard']['headroom']
        x0 = {'start': x, 'middle': x - hw / 2, 'end': x - hw}[anchor]
        joined = ''.join(p[0] for p in parts)
        self.boxes.append((x0, y - 0.97 * size, x0 + hw, y + 0.25 * size, joined, not on_mark))
        self.strings.append(joined)
        spans = ''.join(f'<tspan class="{p[1]}{" num" if is_num(p[0].strip()) else ""}">{html.escape(p[0])}</tspan>'
                        for p in parts)
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        self.out.append(f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}"{a}{attrs}>{spans}</text>')
        return w

    def block(self, x, y, lines, size, cls, weight, lh, tight=False, attrs=''):
        """Several lines set as one <text> with tspans, for display type set tighter than its text box."""
        lines = [copy(ln) for ln in lines]
        w = max(tw(ln, size, weight, tight) for ln in lines)
        self.boxes.append((x, y - 0.97 * size, x + w * TK['guard']['headroom'], y + (len(lines) - 1) * lh + 0.25 * size,
                           ' '.join(lines), True))
        self.strings.append(' '.join(lines))
        sp = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else f(lh)}">{html.escape(ln)}</tspan>' for i, ln in enumerate(lines))
        self.out.append(f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{f(size)}"{attrs}>{sp}</text>')
        return y + (len(lines) - 1) * lh

    def para(self, x, y, s, width, size=None, cls='tn', weight=400, lh=None, anchor='start'):
        """Wrapped text, one <text> per line, wrapped at width / headroom so the widened box still fits.
        Returns the baseline of the last line."""
        size = size or self.t.nt
        lh = lh or round(size * 1.36)
        lines = wrap(s, width / TK['guard']['headroom'], size, weight)
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size, cls, weight, anchor)
        return y + (len(lines) - 1) * lh

    def para_h(self, s, width, size=None, weight=400, lh=None):
        size = size or self.t.nt
        lh = lh or round(size * 1.36)
        return len(wrap(s, width / TK['guard']['headroom'], size, weight)), lh

    # shapes -----------------------------------------------------------------------------------------
    def rect(self, x, y, w, h, cls, attrs=''):
        self.out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(max(w, 0))}" height="{f(h)}" class="{cls}"{attrs}/>')

    def line(self, x1, y1, x2, y2, cls, attrs=''):
        if cls.split()[0] == 's-grid':
            # a 1 px hairline on a half pixel lands on one device row at 1x (craft SH-6)
            if abs(y1 - y2) < 1e-6:
                y1 = y2 = math.floor(y1) + 0.5
            elif abs(x1 - x2) < 1e-6:
                x1 = x2 = math.floor(x1) + 0.5
        k = LINE_KIND.get(cls.split()[0])
        if k:
            self.segs.append((x1, y1, x2, y2, k))
        self.out.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{cls}"{attrs}/>')

    def path(self, d, cls, attrs=''):
        k = LINE_KIND.get(cls.split()[0])
        if k:
            for s_ in _path_segments(d):
                self.segs.append((*s_, k))
        self.out.append(f'<path d="{d}" class="{cls}"{attrs}/>')

    def circle(self, cx, cy, r, cls, attrs=''):
        self.out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="{cls}"{attrs}/>')

    def raw(self, s):
        self.out.append(s)

    def leader(self, pts, cls='s-ld'):
        length = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        assert length >= TK['note']['leader_min'] - 0.01, f'{self.uid}: leader of {length:.1f} px is shorter than the minimum'
        assert len(pts) <= 3, f'{self.uid}: a leader takes one bend at most'
        self.path('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts), cls)

    def hatch(self, name='hatch', ln='p-ln'):
        gap = TK['hatch']['pitch']
        pid = f'{self.uid}-{name}'
        if not any(pid in d for d in self.defs):
            self.defs.append(f'<pattern id="{pid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse" '
                             f'patternTransform="rotate(45)"><rect width="{gap}" height="{gap}" class="p-bg"/>'
                             f'<line x1="0" y1="0" x2="0" y2="{gap}" class="{ln}"/></pattern>')
        return f'url(#{pid})'

    # output -----------------------------------------------------------------------------------------
    def check(self, H):
        bad = []
        pad = TK['guard']['line_pad']
        for (x0, y0, x1, y1, s, halo) in self.boxes:
            if x0 < -0.5 or x1 > self.W + 0.5 or y0 < -0.5 or y1 > H + 0.5:
                bad.append(f'outside: "{s}" ({x0:.1f},{y0:.1f},{x1:.1f},{y1:.1f}) in {self.W}x{H}')
        bx = self.boxes
        for i in range(len(bx)):
            for j in range(i + 1, len(bx)):
                a, b = bx[i], bx[j]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                    bad.append(f'overlap: "{a[4]}" and "{b[4]}"')
        for (x0, y0, x1, y1, s, halo) in self.boxes:
            inner = (x0 + pad, y0 + 0.18 * (y1 - y0), x1 - pad, y1 - pad)   # cap height to descender
            for (sx1, sy1, sx2, sy2, kind) in self.segs:
                if kind == 'grid' and halo:
                    continue
                if _seg_hits_box(sx1, sy1, sx2, sy2, inner):
                    bad.append(f'{kind} line through "{s}"')
                    break
        if bad:
            raise AssertionError(f'{self.uid}: ' + '; '.join(bad[:8]))

    def render(self, H, label, cls, view_name):
        H = math.ceil(H)
        self.check(H)
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        p = math.ceil(self.lpad)
        style = ''
        if p:
            # the drawing reaches p px left of the column so a big number's ink, not its advance box, meets the edge
            style = f' style="margin-left:-{p}px' + (f';width:calc(100% + {p}px);max-width:{self.W + p}px"' if 'ab-s' in cls else '"')
        return (f'<svg class="{cls}" data-view="{ea(view_name)}" width="{self.W + p}" height="{H}" viewBox="{-p} 0 {self.W + p} {H}"{style} '
                f'role="img" aria-label="{e(label)}" focusable="false">{defs}{"".join(self.out)}</svg>')


def da(key=None, value=None, field=None, mark=None, axis=None, scale=None, cat=None):
    """The verifier's data contract as attributes, escaped exactly as the data has them."""
    a = []
    if key is not None:
        a.append(f' data-key="{ea(key)}"')
    if field is not None:
        a.append(f' data-field="{ea(field)}"')
    if value is not None:
        a.append(f' data-value="{f(value) if isinstance(value, float) else value}"')
    if cat is not None:
        a.append(f' data-category="{ea(cat)}"')
    if mark is not None:
        a.append(f' data-mark="{mark}"')
    if axis is not None:
        a.append(f' data-axis="{axis}"')
    if scale is not None:
        a.append(f' data-scale="{ea(scale)}"')
    return ''.join(a)


def swatch(art, x, top, kind, sw=14):
    """A key swatch in the chart's own marks."""
    if kind == 'ink':
        art.rect(x, top, sw, sw, 'f-ink')
    elif kind == 'open':
        art.rect(x + 1, top + 1, sw - 2, sw - 2, 's-ink2 f-g')
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
    elif kind == 'dot':
        art.rect(x + 0.75, top + 0.75, sw - 1.5, sw - 1.5, 's-dot')
    elif kind == 'half':
        art.rect(x + 0.75, top + 0.75, sw - 1.5, sw - 1.5, 's-ctx15 f-g')
        art.path(f'M{f(x + 0.75)} {f(top + sw - 0.75)}L{f(x + sw - 0.75)} {f(top + 0.75)}L{f(x + sw - 0.75)} {f(top + sw - 0.75)}Z', 'f-ctx')
    elif kind == 'some':
        art.rect(x + 1, top + 1, sw - 2, sw - 2, 's-ink2 f-g')
        art.rect(x + 1, top + sw - 5, sw - 2, 4, 'f-ink')


def key_item(art, x, y, kind, label, size):
    swatch(art, x, y - 11, kind)
    w = art.text(x + 21, y, label, size, 'tr', 400)
    return 21 + w * TK['guard']['headroom']


def flow_key(art, x0, y0, items, width, size, gap=20, lh=24):
    """Lay key items left to right, wrapping inside the width. Returns the baseline of the last row."""
    x, y = x0, y0
    hr = TK['guard']['headroom']
    for kind, label in items:
        w = 21 + tw(copy(label), size, 400) * hr
        if x > x0 and x + w > x0 + width:
            x, y = x0, y + lh
        if w > width:
            # an item wider than the key wraps under its own label, clear of the swatch
            lines = wrap(label, (width - 21) / hr, size)
            key_item(art, x, y, kind, lines[0], size)
            for ln in lines[1:]:
                y += lh - 4
                art.text(x + 21, y, ln, size, 'tr', 400)
            x, y = x0, y + lh
            continue
        key_item(art, x, y, kind, label, size)
        x += w + gap
    return y if x > x0 else y - lh


# ------------------------------------------------------------------------------------------------ S01 big number
def gen_s01(W, uid, t=None, compact=False, red=None):
    """Big number in context: one figure large, the two party figures on a 0 to 100 track, then the two votes.
    red='specimen' draws the Senate shortfall in Pillar Red (the system sheet's demonstration A); red='stepdown'
    draws it in the darkest ink, as when an ask holds the view's red (demonstration B)."""
    a = Art(W, uid, t)
    t = a.t
    R = {r['key']: r for r in rows('stock-trading-ban')}
    narrow = W < 600
    s = t.s
    big = TK['type']['big'] * s if not narrow else TK['type']['big_phone']
    lbl = t.lbl
    bh = TK['bar']['height'] * s
    yb = big
    a.text(0, yb, f'{R["support-all"]["value"]}%', big, 'tb', 800, tight=True, bearing=-0.045 * big,
           attrs=da('support-all', R['support-all']['value'], mark='label'))
    a.anchors['big'] = (0, yb)
    lw = 280 * s if not narrow else W
    y = yb + 0.25 * big + 20 * s
    y = a.para(0, y, 'of registered voters favored a ban on stock trading by members of Congress', lw, lbl, 'tl', 600, round(lbl * 1.4))
    left_bottom = y
    if narrow:
        x0, rw, ytop = 0, W, left_bottom + 40
    else:
        x0 = 340 * s
        rw, ytop = W - x0, 22 * s
    a.text(x0, ytop, 'BY PARTY', t.eb, 'te', 700, track=0.06)
    parties = sorted([R['support-democrats'], R['support-republicans']], key=lambda r: (-r['value'], r['group']))
    y = ytop + 34 * s
    for r in parties:
        a.raw(f'<g data-party="{ea(r["group"])}">')
        a.text(x0, y, r['group'], lbl, 'tl', 600)
        a.rect(x0, y + 9 * s, rw, bh, 'f-lt2')
        bw = rw * r['value'] / 100
        a.rect(x0, y + 9 * s, bw, bh, 'f-ink', da(r['key'], r['value'], mark='bar', axis='x'))
        a.text(x0 + bw - 8 * s, y + 9 * s + bh / 2 + lbl * 0.36, f'{r["value"]}%', lbl, 'ti', 600, 'end', on_mark=True,
               attrs=da(r['key'], r['value'], mark='label'))
        a.raw('</g>')
        y += 9 * s + bh + 32 * s
    yt = y - 32 * s + 22 * s
    a.text(x0, yt, '0', t.tk, 'tk', 400)
    a.text(x0 + rw, yt, '100%', t.tk, 'tk', 400, 'end')
    bottom = max(left_bottom, yt)
    yd = bottom + 36 * s
    a.line(0, yd, W, yd, 's-grid')
    y = yd + 34 * s
    a.text(0, y, 'WHAT CONGRESS DID NEXT', t.eb, 'te', 700, track=0.06)
    y += 36 * s
    for ch in ('house', 'senate'):
        yes, no = R[f'{ch}-yes'], R[f'{ch}-no']
        tot = yes['value'] + no['value']
        when = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})$', yes['group']).group(1)      # the vote's date, from the data
        bill = re.search(r'H\.R\. \d+', R['house-yes']['group']).group(0)
        head = f'The House passed a ban ({bill})' if ch == 'house' else 'The Senate vote to take it up fell short'
        score = f'{yes["value"]} to {no["value"]}'
        if narrow:
            a.text(0, y, head, lbl, 'tl', 600)
            y += 20
            a.text(0, y, when, t.tk, 'tk', 400)
            a.text(W, y, score, lbl, 'tl', 600, 'end')
        else:
            hw = a.text(0, y, head, lbl, 'tl', 600)
            a.text(hw * TK['guard']['headroom'] + 10 * s, y, when, t.tk, 'tk', 400)
            a.text(W, y, score, lbl, 'tl', 600, 'end')
        yb2 = y + 10 * s
        gap = 2
        k = (W - gap) / tot
        wy, wn = yes['value'] * k, no['value'] * k
        a.rect(0, yb2, wy, bh, 'f-ink', da(yes['key'], yes['value'], mark='bar', axis='x', scale=ch))
        a.rect(wy + gap, yb2, wn, bh, 'f-lt', da(no['key'], no['value'], mark='bar', axis='x', scale=ch))
        a.text(8 * s, yb2 + bh / 2 + lbl * 0.36, f'{yes["value"]} for', lbl, 'ti', 600, on_mark=True)
        a.text(W - 8 * s, yb2 + bh / 2 + lbl * 0.36, f'{no["value"]} against', lbl, 'tl', 600, 'end', on_mark=True)
        y = yb2 + bh
        if ch == 'senate':
            need = R['senate-needed']['value']
            xn = need * k + gap
            xy = wy
            yk = y + 14 * s
            a.line(xn, yb2 - 7 * s, xn, yk, 's-mark', da('senate-needed', need, mark='point', axis='x', scale='senate'))
            bracket = f'M{f(xy)} {f(y + 6 * s)}V{f(yk)}H{f(xn)}'
            if red == 'specimen':
                # the 7 votes the title names: the span of the bar from 53 to 60, filled, and its bracket
                a.raw('<g data-red="specimen" data-red-job="the Senate shortfall the title names">')
                a.rect(wy + gap, yb2, xn - wy - gap, bh, 'f-red')
                a.path(bracket, 's-redk')
                a.raw('</g>')
            else:
                a.path(bracket, 's-mark' if red == 'stepdown' else 's-ld')
            short = f'{need - yes["value"]} votes short of the {need} needed'
            sw_ = tw(short, lbl, 600) * TK['guard']['headroom']
            a.text(xy if xy + sw_ <= W else max(0, W - sw_), yk + 20 * s, short, lbl, 'tl', 600)
            a.anchors['short'] = (xy, yk)
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
            cur.append(next(r for r in rs if r['comparable_with'] == 'earlier'))
            segs.append(cur)
            cur = [next(r for r in rs if r['comparable_with'] == 'later')]
    segs.append(cur)
    return segs


S02_NOTE_2021 = ('2021: the expanded child tax credit was in force, and it lapsed after that year. '
                 'The timing alone does not show how much of the drop came from the credit.')


def s02_law_note():
    rl35 = row('rule-changes', 'RL35')
    assert rl35['rule'].startswith('P.L. 119-21 set the child tax credit at up to $2,200 per child')
    return 'In July 2025, P.L. 119-21 set the child tax credit at up to $2,200 per child.'


def gen_s02(W, uid, t=None, anatomy=False):
    """Line with event notes: the Supplemental Poverty Measure for children as the dark subject line, the official
    measure as gray context, method breaks drawn as two dots at one year, and notes at 2021 and 2025."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    D = rows('child-poverty-spm')
    order = {'earlier': 0, 'both': 1, 'later': 2}
    spm = sorted((r for r in D if r['measure'] == 'spm'), key=lambda r: (r['year'], order[r['comparable_with']]))
    off = sorted((r for r in D if r['measure'] == 'official'), key=lambda r: (r['year'], order[r['comparable_with']]))
    years = sorted({r['year'] for r in D})
    y0r, y1r = years[0], years[-1]
    vmax = 5 * math.ceil(max(r['percent'] for r in D) / 5)
    gut = max(40, math.ceil(tw(f'{vmax}%', t.tk, 400) * TK['guard']['headroom']) + 8)
    top = 18 if not narrow else 50
    ph = 300 if not narrow else 250
    x0, x1 = gut + 14, W - (52 if not narrow else 30)
    yb = top + ph

    def X(yr):
        return x0 + (yr - y0r) / (y1r - y0r) * (x1 - x0)

    def Y(v):
        return yb - v / vmax * ph
    for v in range(0, vmax + 1, 5):
        if v:
            a.line(gut, Y(v), W, Y(v), 's-grid')
        a.text(gut - 6, Y(v) + 4.5, f'{v}%' if v == vmax else str(v), t.tk, 'tk', 400, 'end')
    a.line(gut, yb, W, yb, 's-base')
    for yr in range(y0r, y1r + 1, 4):
        a.text(X(yr), yb + t.tk + 8, str(yr), t.tk, 'tk', 400, 'middle')

    def draw(series, cls, r_dot, dot_cls):
        for seg in line_segments(series):
            pts = [(X(r['year']), Y(r['percent'])) for r in seg]
            if len(pts) > 1:
                a.path('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts), cls)
            for r, (x, y) in zip(seg, pts):
                if r['measure'] == 'spm' and r['percent'] == min(q['percent'] for q in spm):
                    continue
                a.circle(x, y, r_dot, dot_cls, da(r['key'], r['percent'], mark='point', axis='y'))
    draw(off, 's-ctx', TK['dot']['small_vertex_r'], 'f-ctx')
    draw(spm, 's-sub', TK['dot']['vertex_r'], 'f-ink')
    low = min(spm, key=lambda r: r['percent'])
    cx, cy = X(low['year']), Y(low['percent'])
    a.circle(cx, cy, TK['dot']['subject_r'], 'f-ink s-gring', da(low['key'], low['percent'], mark='point', axis='y'))
    a.text(cx, cy + 25, f'{low["percent"]}%', t.lbl, 'tl', 600, 'middle')
    a.anchors['m9'] = (cx + 30, cy + 20)
    nxt = next(r for r in spm if r['year'] == low['year'] + 1)
    xn_, yn_ = X(nxt['year']), Y(nxt['percent'])
    a.text(xn_ + 6, yn_ + 20, f'{nxt["percent"]}%', t.lbl, 'tl', 600)
    o_first = off[0]
    if not narrow:
        o_hi = max((r for r in off if r['year'] <= y0r + 1), key=lambda r: r['percent'])
        wo = a.text(X(y0r), Y(o_hi['percent']) - 12, 'Official measure', t.lbl, 'ts', 600)
        sw_ = tw('Supplemental measure', t.lbl, 600) * TK['guard']['headroom']
        # below the subject line, clear of every point the label spans
        low_y = max(Y(r['percent']) for r in spm if X(r['year']) <= X(y0r) + 2 + sw_ + 6)
        sy = low_y + t.lbl + 9
        ws = a.text(X(y0r) + 2, sy, 'Supplemental measure', t.lbl, 'tl', 600)
        a.anchors['m8'] = (X(y0r) + wo * TK['guard']['headroom'] + 14, Y(o_hi['percent']) - 17)
        a.anchors['m7'] = (X(y0r) + 2 + ws * TK['guard']['headroom'] + 14, sy - 5)
    else:
        ky = 16
        a.line(gut + 10, ky - 5, gut + 34, ky - 5, 's-sub')
        ws = a.text(gut + 40, ky, 'Supplemental', t.lbl, 'tl', 600) * TK['guard']['headroom']
        a.line(gut + 52 + ws, ky - 5, gut + 76 + ws, ky - 5, 's-ctx')
        a.text(gut + 82 + ws, ky, 'Official', t.lbl, 'ts', 600)
        a.anchors['m7'] = (gut - 5, ky - 5)
        a.anchors['m8'] = (gut + 64 + ws, ky + 17)
    a.anchors.update(m4=(gut + 10, Y(vmax)), m5=(x1 - 14, Y(10)) if not narrow else (X(y0r + 3), Y(5)), m6=(X(y0r + 1), yb - 13))
    end = spm[-1]
    o_end = off[-1]
    xe, ye = X(end['year']), Y(end['percent'])
    if not narrow:
        # 2021 note in the open space below the line, left of the dip
        nw_ = min(360, cx - 28 - gut - 12)
        nx = cx - 28 - nw_
        nl, lh = a.para_h(S02_NOTE_2021, nw_)
        ny = yb - 12 - (nl - 1) * lh
        a.para(nx, ny, S02_NOTE_2021, nw_)
        a.leader([(nx + nw_ * 0.98, ny - 5), (cx - 7, cy + 2)])
        a.anchors['m10'] = (nx - 16, ny - 5)
        # 2025: both measures, and the 2025 law, in the open top right
        both = f'Both measures: {end["percent"]}% in {end["year"]}.' if end['percent'] == o_end['percent'] else f'{end["year"]}: {end["percent"]}%.'
        txt = f'{both} {s02_law_note()}'
        bw = min(430, W - (X(y0r) + wo * TK['guard']['headroom'] + 24))
        nl2, lh2 = a.para_h(txt, bw)
        by = Y(vmax - 0.9)
        a.para(W, by, txt, bw, anchor='end')
        a.leader([(xe, by + (nl2 - 1) * lh2 + 6), (xe, ye - 8)])
        first_line = wrap(txt, bw / TK['guard']['headroom'], t.nt)[0]
        a.anchors['m12'] = (W - tw(first_line, t.nt) - 18, by - 5)
    else:
        both = f'Both: {end["percent"]}% in {end["year"]}'
        ew = tw(both, t.lbl, 600) * TK['guard']['headroom']
        ey = Y(vmax - 1.8)
        a.text(W - ew, ey, both, t.lbl, 'tl', 600)
        a.leader([(xe, ey + 7), (xe, ye - 8)])
        a.anchors['m12'] = (W - 13, ey - 22)
    # the encoding a reader could misread: method breaks
    breaks = sorted({r['year'] for r in D if r['comparable_with'] in ('earlier', 'later')})
    yn = yb + 50
    a.circle(6, yn - 9, 3, 'f-ink')
    a.circle(6, yn + 2, 3, 'f-ink')
    yrs = ', '.join(str(b) for b in breaks[:-1]) + f' and {breaks[-1]}'
    bt = (f'Census changed its survey or method in {yrs}. The line breaks there, and each of those years shows two '
          'estimates, one for each method.')
    last = a.para(20, yn, bt, (TK['note']['width'] if not narrow else W - 20))
    later = min(r['percent'] for r in spm if r['year'] == breaks[1])
    a.anchors['m11'] = (X(breaks[1]), Y(later) + 17)      # under the break it explains
    if narrow:
        a.anchors['m10'] = (W - 13, last + 25)
        last = a.para(0, last + 30, S02_NOTE_2021, W - (28 if anatomy else 0))
        last = a.para(0, last + 26, s02_law_note(), W - (28 if anatomy else 0))
    return a, last + 10


# ------------------------------------------------------------------------------------------------ S03 ranked bar
DIR_ORDER = ['away from voters', 'toward voters', 'voters kept existing rules', 'mixed', 'pending']
DIR_KIND = {'away from voters': 'ink', 'toward voters': 'open', 'voters kept existing rules': 'lt', 'mixed': 'hatch', 'pending': 'dash'}
DIR_WORD = {'away from voters': 'Away from voters', 'toward voters': 'Toward voters',
            'voters kept existing rules': 'Voters kept existing rules', 'mixed': 'Mixed', 'pending': 'Pending'}


def seg_rect(a, x, y, w, h, kind, attrs):
    """A bar segment in its category's mark; the data rect carries the exact geometry."""
    if kind == 'ink':
        a.rect(x, y, w, h, 'f-ink', attrs)
    elif kind == 'ctx':
        a.rect(x, y, w, h, 'f-ctx', attrs)
    elif kind == 'lt':
        a.rect(x, y, w, h, 'f-lt', attrs)
    elif kind == 'open':
        a.rect(x, y, w, h, 'f-g', attrs)
        a.rect(x + 1, y + 1, w - 2, h - 2, 's-ink2 nofill')
    elif kind == 'hatch':
        a.rect(x, y, w, h, 'hatchf', f' style="fill:{a.hatch()}"' + attrs)
        a.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 's-ctx15 nofill')
    elif kind == 'dash':
        a.rect(x, y, w, h, 'nofill', attrs)
        a.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 's-dash')
    elif kind == 'dot':
        a.rect(x, y, w, h, 'nofill', attrs)
        a.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 's-dot')


def s03_annotations(D):
    """Short labels at two bars, chosen from the data: the largest share away from voters, and the largest
    instrument with none away."""
    hi = max(D, key=lambda r: (r['away from voters'] / r['value'], r['value']))
    zero = max((r for r in D if r['away from voters'] == 0), key=lambda r: r['value'])
    return {hi['key']: f'{nw(hi["away from voters"])} away from voters', zero['key']: 'none away from voters'}


def gen_s03(W, uid, t=None):
    """Ranked bar: instruments ranked by how many entries they made in the repair log, each bar split by the
    atlas's direction code. Away from voters sits at the baseline in solid ink because the title names it; toward
    voters is an open bar of the same ink, so the two differ by fill as well as position."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    D = sorted(rows('rule-changes-by-instrument'), key=lambda r: -r['value'])
    lbl = t.lbl
    hr = TK['guard']['headroom']
    ann = s03_annotations(D)

    def endw(r):
        w_ = tw(str(r['value']), lbl, 600) + (tw(f', {ann[r["key"]]}', lbl, 400) if r['key'] in ann else 0)
        return w_ * hr
    yk = flow_key(a, 0, 16, [(DIR_KIND[d], DIR_WORD[d]) for d in DIR_ORDER], W, 14)
    vmax = max(r['value'] for r in D)
    if narrow:
        BX = 0
        bh, pitch = TK['bar']['phone_height'], TK['bar']['phone_pitch']
        k = min(min((W - 8 - endw(r)) / r['value'] for r in D), (W - 40) / vmax)
    else:
        BX = max(tw(r['key'], lbl, 600) for r in D) * hr + 16
        bh, pitch = TK['bar']['height'], TK['bar']['pitch']
        k = min((W - BX - 8 - endw(r)) / r['value'] for r in D)
    y = yk + (34 if not narrow else 30)
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
            if w >= 20 + (4 if DIR_KIND[d] == 'open' else 0) and DIR_KIND[d] in ('ink', 'ctx', 'lt', 'open'):
                cls = 'ti' if DIR_KIND[d] in ('ink', 'ctx') else 'tl'
                a.text(x + w / 2, by + bh / 2 + lbl * 0.36, str(v), lbl, cls, 600, 'middle', on_mark=True, box=False)
            x += w
        end = f'{r["value"]}, {ann[r["key"]]}' if r['key'] in ann else str(r['value'])
        if r['key'] in ann:
            a.rich(BX + r['value'] * k + 8, by + bh / 2 + lbl * 0.36, [(str(r['value']), 'tl', 600), (f', {ann[r["key"]]}', 'tr', 400)], lbl,
                   attrs=da(r['key'], r['value'], mark='label'))
        else:
            a.text(BX + r['value'] * k + 8, by + bh / 2 + lbl * 0.36, end, lbl, 'tl', 600, attrs=da(r['key'], r['value'], mark='label'))
        rowy[r['key']] = (by, by + bh)
        if narrow:
            a.line(0, by - 3, 0, by + bh + 3, 's-base')
        y += pitch
    if not narrow:
        a.line(BX, rowy[D[0]['key']][0] - 6, BX, rowy[D[-1]['key']][1] + 6, 's-base')
    return a, rowy[D[-1]['key']][1] + 10


# ------------------------------------------------------------------------------------------------ S04 dumbbell
def age_words(key):
    return key.replace('_', ' ')


def gen_s04(W, uid, t=None):
    """Dot plot with two elections per row: the earlier year as an open ring drawn over the later year's dot, the
    change in words and numbers, and a scale cropped to 40 to 80 percent (said in the measure line)."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    hr = TK['guard']['headroom']
    base = 'citizen_voting_age_population'
    years = (2020, 2024)
    R = {(r['age_group'], r['year']): r for r in rows('turnout-by-age') if r['base'] == base}
    groups = [g for g in dict.fromkeys(r['age_group'] for r in rows('turnout-by-age')) if g != 'all' and (g, years[1]) in R]
    groups.sort(key=lambda g: int(re.match(r'\d+', g).group(0)))
    vals = [R[(g, y)]['voted_pct'] for g in groups for y in years]
    lo, hi = 10 * math.floor(min(vals) / 10 - 0.5), 10 * math.ceil(max(vals) / 10)
    x0, x1 = (12, W - 12) if narrow else (128, W - 186)

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    y = 18
    for v in range(lo, hi + 1, 10):
        anc = 'middle' if not narrow or lo < v < hi else ('start' if v == lo else 'end')
        a.text(X(v) + (-6 if narrow and v == lo else 6 if narrow and v == hi else 0), y, f'{v}%' if v == hi else str(v), t.tk, 'tk', 400, anc)
    y += 50 if not narrow else 34
    pitch = 54 if not narrow else 72
    r_dot = TK['dot']['subject_r']
    first = True
    for g in groups:
        r0, r1 = R[(g, years[0])], R[(g, years[1])]
        v0, v1 = r0['voted_pct'], r1['voted_pct']
        ch = round(v1 - v0, 1)
        word = (('Down' if ch < 0 else 'Up') + f' {abs(ch):.1f} points') if abs(ch) > 2 else f'Little change ({MINUS if ch < 0 else "+"}{abs(ch):.1f})'
        if narrow:
            a.text(0, y, age_words(g), t.lbl, 'tl', 600)
            a.text(W, y, word, t.lbl, 'tl', 600, 'end')
            cy = y + (40 if first else 26)
        else:
            cy = y
            a.text(0, cy + 5, age_words(g), t.lbl, 'tl', 600)
            a.text(W, cy + 5, word, t.lbl, 'tl', 600, 'end')
        xa, xb = X(v0), X(v1)
        (lr, lx), (rr, rx) = sorted(((r0, xa), (r1, xb)), key=lambda q: (q[1], q[0]['year']))
        size = t.lbl
        lw_ = tw(f'{lr["voted_pct"]}', size, 600) * hr
        rw_ = tw(f'{rr["voted_pct"]}', size, 600) * hr
        lab_l0 = lx - r_dot - 6 - lw_
        lab_r1 = rx + r_dot + 6 + rw_
        # the row line stops short of the value labels, so no rule runs through a figure
        if lab_l0 - 4 > x0:
            a.line(x0, cy, lab_l0 - 4, cy, 's-grid')
        if lab_r1 + 4 < x1:
            a.line(lab_r1 + 4, cy, x1, cy, 's-grid')
        if rx - lx > 2 * r_dot:
            a.line(lx + r_dot, cy, rx - r_dot, cy, 's-ctx')
        a.circle(xb, cy, r_dot, 'f-ink', da(r1['key'], v1, mark='point', axis='x'))
        a.circle(xa, cy, TK['dot']['open_r'], 's-ring2', da(r0['key'], v0, mark='point', axis='x'))
        for rr_, xx, side in ((lr, lx, 'end'), (rr, rx, 'start')):
            cls = 'tl' if rr_['year'] == years[1] else 'ts'
            dx = -(r_dot + 6) if side == 'end' else r_dot + 6
            a.text(xx + dx, cy + 5, f'{rr_["voted_pct"]}', size, cls, 600, side, attrs=da(rr_['key'], rr_['voted_pct'], mark='label'))
        if first:
            a.text(lx + 7, cy - 16, str(lr['year']), t.tk, 'tl' if lr['year'] == years[1] else 'ts', 600, 'end')
            a.text(rx - 7, cy - 16, str(rr['year']), t.tk, 'tl' if rr['year'] == years[1] else 'ts', 600, 'start')
            first = False
        y = cy + pitch if not narrow else cy + 46
    gl = [R[(groups[-1], yy)]['voted_pct'] - R[(groups[0], yy)]['voted_pct'] for yy in years]
    y = y - (pitch if not narrow else 46) + 44
    nwid = TK['note']['width'] if not narrow else W
    y = a.para(0, y, f'The gap between citizens {age_words(groups[0])} and those {age_words(groups[-1])}: '
                     f'{gl[0]:.1f} points in {years[0]}, {gl[1]:.1f} in {years[1]}.', nwid, t.nt, 'th', 600) + 26
    y = a.para(0, y, 'These rates are what people told a Census survey, which runs higher than counted ballots. '
                     'Table A-1 publishes no margins of error, so a change of a point or two may sit within survey error.', nwid)
    return a, y + 8


# ------------------------------------------------------------------------------------------------ S05 small multiples
def group_words(g):
    """Display words for a homeownership group key."""
    words = {'all_households': 'All households', 'non_hispanic_white': 'Non-Hispanic White', 'hispanic': 'Hispanic (any race)'}
    return words.get(g, g.replace('_', ' ').capitalize())


def ho_segments(g):
    """Annual homeownership for one group, split where the Census changed its method: 2002 has an original and a
    revised estimate (reweighted to the 2000 Census); Black and non-Hispanic White change race categories in 2003."""
    rs = sorted([r for r in rows('homeownership-by-race') if r['group'] == g], key=lambda r: r['year'])
    rev = next(r for r in rs if r['series_variant'].startswith('revised'))
    ry = rev['year']
    a_ = [r for r in rs if r['year'] < ry or (r['year'] == ry and r['series_variant'] == 'original')]
    b_ = [r for r in rs if r['year'] > ry]
    if rev['race_definition'] == b_[0]['race_definition']:
        return [a_, [rev] + b_], []
    return [a_, b_], [rev]


def gen_s05(W, uid, t=None):
    """Small multiples: one panel per group on one scale; each panel draws its group as the dark line over the other
    three in gray. Brackets give the gap to the highest group in the first and last years of the current method."""
    a = Art(W, uid, t)
    t = a.t
    H5 = rows('homeownership-by-race')
    last_year = max(r['year'] for r in H5)
    groups = list(dict.fromkeys(r['group'] for r in H5))
    latest = {g: next(r for r in H5 if r['group'] == g and r['year'] == last_year) for g in groups}
    order = ['all_households'] + sorted([g for g in groups if g != 'all_households'], key=lambda g: -latest[g]['rate_pct'])
    top_g = order[1]
    vals = [r['rate_pct'] for r in H5]
    lo, hi = 10 * math.floor(min(vals) / 10), 10 * math.ceil(max(vals) / 10)
    gut = max(38, math.ceil(tw(f'{hi}%', t.tk, 400) * TK['guard']['headroom']) + 8)
    if W >= 900:
        cols, gapx = 4, 26
    elif W >= 560:
        cols, gapx = 2, 32
    else:
        cols, gapx = 1, 0
    pw = (W - gut - gapx * (cols - 1)) / cols
    ph = 190 if cols != 1 else 172
    y0r, y1r = min(r['year'] for r in H5), last_year
    head_h, foot_h = 54, 30
    gapy = 44 if cols != 1 else 30
    y_top = 30
    a.text(0, 16, f'Gray lines: the other {nw(len(order) - 1)} groups.', t.nt, 'tn', 400)
    cat_year = min(r['year'] for r in H5 if r['race_definition'] == 'race_alone')
    for i, g in enumerate(order):
        c, rr = i % cols, i // cols
        px = gut + c * (pw + gapx)
        py = y_top + rr * (head_h + ph + foot_h + gapy) + head_h
        x0, x1 = px, px + pw - 14

        def X(yr):
            return x0 + (yr - y0r) / (y1r - y0r) * (x1 - x0)

        def Y(v):
            return py + ph - (v - lo) / (hi - lo) * ph
        a.text(px, py - 34, group_words(g), t.lbl, 'tl', 600)
        lv = latest[g]
        a.rich(px, py - 13, [(f'{last_year}: ', 'tn', 400), (f'{lv["rate_pct"]}%', 'th', 600)], t.nt,
               attrs=da(lv['key'], lv['rate_pct'], mark='label'))
        for v in range(lo, hi + 1, 10):
            a.line(px, Y(v), px + pw, Y(v), 's-grid')
            if c == 0:
                a.text(px - 6, Y(v) + 4.5, f'{v}%' if v == hi else str(v), t.tk, 'tk', 400, 'end')
        for yr in (y0r, cat_year, y1r):
            anc = 'start' if yr == y0r else ('end' if yr == y1r else 'middle')
            a.text(X(yr) + (-2 if yr == y0r else 0), py + ph + 23, str(yr), t.tk, 'tk', 400, anc)
        for og in order:
            if og == g:
                continue
            segs, _ = ho_segments(og)
            for seg in segs:
                a.path('M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg), 's-ctx15')
        segs, lone = ho_segments(g)
        for seg in segs:
            a.path('M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg), 's-sub')
            for r in seg:
                a.circle(X(r['year']), Y(r['rate_pct']), TK['dot']['small_vertex_r'], 'f-ink',
                         da(r['key'], r['rate_pct'], mark='point', axis='y', scale=f'p-{g}'))
        for r in lone:
            a.circle(X(r['year']), Y(r['rate_pct']), TK['dot']['small_vertex_r'], 'f-ink',
                     da(r['key'], r['rate_pct'], mark='point', axis='y', scale=f'p-{g}'))
        if g not in ('all_households', top_g):
            def val(gg, yr):
                return next(r for r in H5 if r['group'] == gg and r['year'] == yr and r['series_variant'] == 'standard')['rate_pct']

            def clear_mid(span):
                lo_ = max(r['rate_pct'] for r in H5 if r['group'] == g and span[0] <= r['year'] <= span[1])
                hi_ = min(r['rate_pct'] for r in H5 if r['group'] == 'all_households' and span[0] <= r['year'] <= span[1])
                return (lo_ + hi_) / 2
            for yr, xb, span in ((cat_year, X(cat_year) - 5, (y0r, cat_year - 1)), (y1r, x1 + 5, (y1r - 7, y1r))):
                wv, gv = val(top_g, yr), val(g, yr)
                arm = xb + 4 if yr == cat_year else xb - 4
                a.path(f'M{f(arm)} {f(Y(wv))}H{f(xb)}V{f(Y(gv))}H{f(arm)}', 's-ld')
                cy_ = Y(clear_mid(span))
                a.text(xb - 5, cy_ - 3, f'{wv - gv:.1f}', t.nt, 'th', 600, 'end')
                a.text(xb - 5, cy_ + 15, 'points', t.nt, 'tn', 400, 'end')
    yb = y_top + math.ceil(len(order) / cols) * (head_h + ph + foot_h + gapy) - gapy
    return a, yb + 6


# ------------------------------------------------------------------------------------------------ S06 comparison table
TNOTE = ("Directions hold only if each scenario's assumptions hold. They are no forecast and give no odds. "
         'The four families are read separately and never added together. In the baseline, no family rises.')
CLS_TINT = {'up': 'c-up', 'slightly up': 'c-up2', 'flat': 'c-flat', 'flat or down': 'c-dn2', 'down': 'c-dn',
            'mixed': 'c-mix', 'same as ii': 'c-same'}
CLS_WORD = {'up': 'Up', 'slightly up': 'Slightly up', 'flat': 'Flat', 'flat or down': 'Flat or down', 'down': 'Down',
            'mixed': 'Mixed', 'same as ii': 'Same as scenario ii'}
# A few plain words for each scenario name, so a first-time reader can follow the row (F5). The words come from
# each scenario's own assumptions in the shared data.
SCENARIO_GLOSS = {
    'i': 'Current law runs as written.',
    'ii': 'Some states and cities change their rules; federal rules stay as they are.',
    'iii': 'Congress passes rules for elections and government together.',
    'iv-a': 'Fusion voting lets more than one party nominate the same candidate.',
    'iv-b': 'Rebuilds career staff, tax enforcement and watchdogs; inspectors general are the watchdogs inside agencies.',
    'iv-c': 'Merger, market and labor-law enforcement come first.',
    'iv-d': 'Changes made by amending the Constitution.',
    'iv-e': 'Forbearance: officials hold back from using every power they have, with no new rules.',
}


def glyph(cls):
    """Oath & Action's reading of the atlas's words as a boxed 22 px glyph: shape alone carries direction on a
    black-and-white copy."""
    p = {
        'up': '<path d="M11 4.5L17 16H5Z"/>',
        'slightly up': '<path d="M11 8L14.5 14.5H7.5Z"/>',
        'flat': '<rect x="5" y="9.75" width="12" height="2.5"/>',
        'flat or down': '<rect x="5" y="6.5" width="12" height="2.5"/><path d="M11 17L14.5 11.5H7.5Z"/>',
        'down': '<path d="M11 17.5L17 6H5Z"/>',
        'mixed': '<path d="M11 4L18 11L11 18L4 11Z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M11 4V18L4 11Z"/>',
        'same as ii': '<rect x="5" y="7.5" width="12" height="2.5"/><rect x="5" y="12" width="12" height="2.5"/>',
    }[cls]
    return (f'<svg class="gl" width="22" height="22" viewBox="0 0 22 22" aria-hidden="true" focusable="false">'
            f'<rect x="0.75" y="0.75" width="20.5" height="20.5" fill="none" stroke="currentColor" stroke-width="1.5"/>{p}</svg>')


def gen_s06_table(view):
    D = DS['scenarios-2030']
    fam = D['families']
    keys = list(fam)
    head = ''.join(f'<th scope="col">{e(fam[k])}</th>' for k in keys)
    body = []
    for r in D['rows']:
        cells = []
        for k in keys:
            c = r[f'{k}_class']
            cells.append(f'<td class="{CLS_TINT[c]}" data-label="{e(fam[k])}"{da(r["key"], field=k, cat=r[k], mark="cell")}>'
                         f'<span class="gw"{da(r["key"], field=f"{k}_class", cat=c, mark="cell")}>{glyph(c)}'
                         f'<span class="vh2">{e(CLS_WORD[c])}: </span></span><span class="cw">{e(r[k])}</span></td>')
        body.append(f'<tr><th scope="row"><span class="sk">{e(r["key"])}</span><span class="sn">{e(r["name"])}'
                    f'<span class="sg">{e(SCENARIO_GLOSS[r["key"]])}</span></span></th>{"".join(cells)}</tr>')
    key = ''.join(f'<li class="{CLS_TINT[c]}">{glyph(c)}<span>{e(CLS_WORD[c])}</span></li>'
                  for c in ('up', 'slightly up', 'flat', 'flat or down', 'down', 'mixed', 'same as ii'))
    return (f'<p class="upnote">{e("Up means better for each family; for income and wealth equality, more equal.")}</p>'
            f'<div class="cmpkey"><p class="kh">{e("Oath & Action’s reading of the atlas’s words, by arrow and tint")}</p><ul>{key}</ul></div>'
            f'<div class="tw"><table class="cmp"><caption class="vh2">{e("Direction each outcome family would take by 2036 under eight scenarios, in the atlas’s words")}</caption>'
            f'<thead><tr><th scope="col">Scenario</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
            f'<p class="tnote">{e(TNOTE)} Each scenario’s assumptions are listed in the table under this chart.</p>')


# ------------------------------------------------------------------------------------------------ S07 tile map
STATUS_KIND = {'bans in all elections': 'all', 'bans in some elections': 'some', 'no ban': 'none'}
STATUS_WORD = {'bans in all elections': 'Bans it in all elections', 'bans in some elections': 'Bans it in some elections',
               'no ban': 'No state ban'}


def s07_counts():
    R = rows('rcv-bans')
    none = [r for r in R if r['status'] == 'no ban']
    return {'bans': sum(1 for r in R if r['prohibits_rcv']), 'all': sum(1 for r in R if r['status'] == 'bans in all elections'),
            'some': sorted(r['name'] for r in R if r['status'] == 'bans in some elections'),
            'none_states': sum(1 for r in none if r['code'] != 'DC'), 'none_dc': any(r['code'] == 'DC' for r in none)}


def gen_s07(W, uid, t=None):
    """Tile map: one square per state, so each state weighs the same whatever its land area."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    R = {r['key']: r for r in rows('rcv-bans')}
    C = s07_counts()
    none_word = f'No state ban: {C["none_states"]} states' + (' and DC' if C['none_dc'] else '')
    some_word = f'Bans it in some elections: {" and ".join(C["some"])}'
    if narrow:
        gap = 2.5
        tile = (W + gap) / 12 - gap
    else:
        gap = 4
        tile = min(52, (W + gap) / 12 - gap)
    pitch = tile + gap
    oy = 0
    stack = W < 700     # under 700 px the key sits above the map, where no tile can meet it
    if stack:
        y = 16
        for kind, lab in (('ink', 'Bans it in all elections'), ('some', some_word), ('lt2', none_word)):
            for i, ln in enumerate(wrap(lab, (W - 21) / TK['guard']['headroom'], 14)):
                if i == 0:
                    key_item(a, 0, y, kind, ln, 14)
                else:
                    a.text(21, y, ln, 14, 'tr', 400)
                y += 22
            y += 2
        oy = y + 2
    for tl in TILES:
        r = R[tl['code']]
        x, y = tl['col'] * pitch, oy + tl['row'] * pitch
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
            a.rect(x + 1, y + tile - 1 - 4, tile - 2, 4, 'f-ink')
            tcls = 'tl'
        else:
            a.rect(x, y, tile, tile, 'f-lt2', attrs)
            tcls = 'tl'
        if narrow:
            ty = y + tile / 2 + 4.6 - (1.5 if kind == 'some' else 0)
            a.text(x + tile / 2, ty, tl['code'], TK['type']['tile_code_phone'], tcls, 600, 'middle', on_mark=True)
        else:
            a.text(x + 7, y + min(20, tile * 0.4), tl['code'], 14, tcls, 600, on_mark=True)
            if r['enacted_year']:
                a.text(x + 7, y + min(37, tile - 11), str(r['enacted_year']), 13, 'ti4' if kind == 'all' else 'tr', 400, on_mark=True)
        a.raw('</g>')
    H = oy + 8 * pitch - gap
    if not stack:
        kx, ky = pitch + 6, oy + 18
        key_item(a, kx, ky, 'ink', 'Bans it in all elections, with the year it became law', 14)
        key_item(a, kx, ky + 24, 'some', some_word, 14)
        key_item(a, kx, ky + 48, 'lt2', none_word, 14)
    return a, H + 4


# ------------------------------------------------------------------------------------------------ S08 unit chart
ROLLUP_KEY = 'RL47'   # the one entry that stands for many: drawn as a distinct roll-up mark (D2-103)


def s08_bins(D):
    """Year columns from the data: every year gets its own column after the last run of empty years longer than the
    token allows; everything before sits in one first column."""
    years = sorted({r['year'] for r in D})
    first = years[0]
    for a_, b_ in zip(years, years[1:]):
        if b_ - a_ - 1 > TK['gap_years']:
            first = b_
    bins = []
    if years[0] < first:
        bins.append(('early', f'To {first - 1}', lambda r, f_=first: r['year'] < f_))
    bins += [(str(y), str(y), (lambda yy: lambda r: r['year'] == yy)(y)) for y in range(first, years[-1] + 1)]
    return bins, first


def unit_shape(a, x, y, s, d, attrs):
    """One unit per repair-log row, one self-closing element that carries the data."""
    if d == 'away from voters':
        a.rect(x, y, s, s, 'f-ink', attrs)
    elif d == 'toward voters':
        a.rect(x + 1, y + 1, s - 2, s - 2, 's-ink2 f-g', attrs)
    elif d == 'voters kept existing rules':
        a.rect(x, y, s, s, 'f-ctx', attrs)
    elif d == 'mixed':
        a.rect(x + 0.75, y + 0.75, s - 1.5, s - 1.5, 's-ctx15 f-g', attrs)
        a.path(f'M{f(x + 0.75)} {f(y + s - 0.75)}L{f(x + s - 0.75)} {f(y + 0.75)}L{f(x + s - 0.75)} {f(y + s - 0.75)}Z', 'f-ctx')
    elif d == 'pending':
        a.rect(x + 0.75, y + 0.75, s - 1.5, s - 1.5, 's-dash', attrs)


def s08_order(rs):
    """Date order inside a stack, with the roll-up entry last so its label can sit clear of the stack."""
    return sorted(rs, key=lambda r: (r['key'] == ROLLUP_KEY, r['date'], r['key']))


def gen_s08(W, uid, t=None):
    """Unit chart: one square per entry in the repair log, by year. Toward voters stacks above the year band as open
    squares, away from voters below it as solid squares, and entries that went neither way sit in their own band.
    The top row prints how many entries the log holds each year. The roll-up entry carries a ring and a label."""
    a = Art(W, uid, t)
    t = a.t
    D = sorted(rows('rule-changes'), key=lambda r: (r['date'], r['key']))
    bins, first = s08_bins(D)
    neither = ('voters kept existing rules', 'mixed', 'pending')
    s, g = TK['unit']['size'], TK['unit']['gap']
    drawn = Counter()
    hr = TK['guard']['headroom']
    roll = row('rule-changes', ROLLUP_KEY)
    first_word = roll['jurisdiction'].split()[0].lower()
    roll_n = ONES.index(first_word) if first_word in ONES else int(first_word)

    def attrs(r):
        return da(r['key'], field='direction', cat=r['direction'], mark='unit')
    if W >= 900:
        LW = 150
        colw = (W - LW) / len(bins)
        per = max(1, int((colw - 10 + g) // (s + g)))
        cw = per * (s + g) - g

        def stack_h(n):
            return math.ceil(n / per) * (s + g) - g if n else 0
        cnt = {bk: Counter(r['direction'] for r in D if fn(r)) for bk, _, fn in bins}
        up_max = max(stack_h(c['toward voters']) for c in cnt.values())
        dn_max = max(stack_h(c['away from voters']) for c in cnt.values())
        ne_max = max(stack_h(sum(c[d] for d in neither)) for c in cnt.values())
        yT = 18
        yA = yT + 18 + up_max + 8
        band = 30
        yB = yA + band
        a.text(0, yT, 'All entries', t.lbl, 'ts', 600)
        a.line(LW - 6, yA, W, yA, 's-base')
        a.line(LW - 6, yB, W, yB, 's-base')
        swatch(a, 0, yA - 22, 'open')
        a.text(21, yA - 9, 'Toward voters', t.lbl, 'tl', 600)
        swatch(a, 0, yB + 8, 'ink')
        a.text(21, yB + 21, 'Away from voters', t.lbl, 'tl', 600)
        cx_of = {}
        roll_pos = None
        for i, (bk, lab, fn) in enumerate(bins):
            cx = LW + i * colw + (colw - cw) / 2
            cx_of[bk] = cx
            ins = [r for r in D if fn(r)]
            a.text(cx + cw / 2, yT, str(len(ins)), t.tk, 'tk', 400, 'middle')
            a.text(cx + cw / 2, yA + band / 2 + 5, lab, t.tk, 'tk', 400, 'middle')
            for d, y0, sign in (('toward voters', yA - s, -1), ('away from voters', yB, 1)):
                for n, r in enumerate(s08_order([r for r in ins if r['direction'] == d])):
                    x = cx + (n % per) * (s + g)
                    yy = y0 + sign * (n // per) * (s + g)
                    unit_shape(a, x, yy, s, d, attrs(r))
                    drawn[d] += 1
                    if r['key'] == ROLLUP_KEY:
                        a.rect(x - 2.5, yy - 2.5, s + 5, s + 5, 's-ring')
                        roll_pos = (x, yy)
            for n, r in enumerate(sorted([r for r in ins if r['direction'] in neither], key=lambda r: (neither.index(r['direction']), r['date']))):
                unit_shape(a, cx + (n % per) * (s + g), yB + dn_max + 64 + (n // per) * (s + g), s, r['direction'], attrs(r))
                drawn[r['direction']] += 1
        assert sum(drawn.values()) == len(D)
        rx, ry = roll_pos
        lab = f'{roll_n} states'
        lx = min(rx + s / 2, W - tw(lab, t.lbl, 600) * hr / 2 - 1)
        a.leader([(rx + s / 2, ry + s + 3), (rx + s / 2, ry + s + 17)])
        a.text(lx, ry + s + 33, lab, t.lbl, 'tl', 600, 'middle')
        yC = yB + dn_max + 64
        a.line(LW - 6, yC - 12, W, yC - 12, 's-grid')
        a.text(0, yC + 12, 'Neither way', t.lbl, 'ts', 600)
        nk = yC + ne_max + 34
        xk = LW
        for d, lab in (('voters kept existing rules', 'Voters kept existing rules: a ballot measure failed'),
                       ('mixed', 'Mixed'), ('pending', 'Pending on November 3, 2026')):
            unit_shape(a, xk, nk - 11, s, d, '')
            w = a.text(xk + s + 7, nk, lab, t.nt, 'tr', 400)
            xk += s + 7 + w * hr + 22
        return a, nk + 10
    # phone: years run down; away grows left of the year column, toward right; neither way in its own block below
    yearw = 66
    cxm = W / 2
    per = int(((cxm - yearw / 2 - 6) + g) // (s + g))
    y = 18
    left_w = cxm - yearw / 2 - 6
    swatch(a, cxm + yearw / 2 + 4, y - 11, 'open')
    rlines = wrap('Toward voters', (W - cxm - yearw / 2 - 25) / hr, 14, 600)
    for i, ln in enumerate(rlines):
        a.text(cxm + yearw / 2 + 25, y + i * 18, ln, 14, 'tl', 600)
    lines = wrap('Away from voters', (left_w - 21) / hr, 14, 600)
    for i, ln in enumerate(lines):
        a.text(cxm - yearw / 2 - 25, y + i * 18, ln, 14, 'tl', 600, 'end')
    swatch(a, cxm - yearw / 2 - 18, y - 11, 'ink')
    y += 18 * max(len(lines), len(rlines)) + 4
    a.text(W, y, 'All', 14, 'ts', 600, 'end')
    y += 10
    first_row_y = y
    rows_end = y
    for bk, lab, fn in bins:
        ins = [r for r in D if fn(r)]
        tow = s08_order([r for r in ins if r['direction'] == 'toward voters'])
        awy = s08_order([r for r in ins if r['direction'] == 'away from voters'])
        nrows = max(1, math.ceil(len(tow) / per), math.ceil(len(awy) / per))
        h = nrows * (s + g) - g
        a.text(cxm, y + 11, lab, 14, 'tk', 400, 'middle')
        a.text(W, y + 11, str(len(ins)), 14, 'tk', 400, 'end')
        roll_here = None
        for n, r in enumerate(tow):
            x = cxm + yearw / 2 + 4 + (n % per) * (s + g)
            unit_shape(a, x, y + (n // per) * (s + g), s, r['direction'], attrs(r))
            drawn[r['direction']] += 1
        for n, r in enumerate(awy):
            x = cxm - yearw / 2 - 4 - s - (n % per) * (s + g)
            yy = y + (n // per) * (s + g)
            unit_shape(a, x, yy, s, r['direction'], attrs(r))
            if r['key'] == ROLLUP_KEY:
                a.rect(x - 2.5, yy - 2.5, s + 5, s + 5, 's-ring')
                roll_here = (x, yy)
            drawn[r['direction']] += 1
        y += max(h, 16) + 9
        rows_end = y
        if roll_here:
            rx, ry = roll_here
            a.leader([(rx + s / 2, ry + s + 3), (rx + s / 2, ry + s + 17)])
            a.text(rx + s / 2, ry + s + 33, f'{roll_n} states', 14, 'tl', 600, 'middle')
            y = max(y, ry + s + 44)
    a.line(cxm - yearw / 2, first_row_y - 4, cxm - yearw / 2, rows_end - 6, 's-base')
    a.line(cxm + yearw / 2, first_row_y - 4, cxm + yearw / 2, rows_end - 6, 's-base')
    y += 24
    a.text(0, y, 'Neither way', 14, 'ts', 600)
    y += 14
    by_year = defaultdict(list)
    for r in D:
        if r['direction'] in neither:
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
    return a, y - 24 + 8


# ------------------------------------------------------------------------------------------------ S09 timeline
STRETCHES = [(1964, 1978), (2010, 2026)]


def event_label(r):
    """The event's name as the atlas gives it, before any parenthesis; the year leads unless the name holds it."""
    name = r['title'].split(' (')[0]
    return ('', name) if str(r['year']) in name else (f'{r["year"]} ', name)


def _rows_for(items, choice):
    """Row assignment for one choice of anchor and line count per label, or None when two labels cover each other's
    dots. A label that covers another event's dot sits above that event's whole label."""
    iv = []
    for it, (an, v) in zip(items, choice):
        w = it['variants'][v]['w']
        iv.append((it['x'] - 4, it['x'] + w + 6) if an == 'start' else (it['x'] - w - 6, it['x'] + 4))
    nl = [it['variants'][v]['nl'] for it, (an, v) in zip(items, choice)]
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

    def clash(i, r):
        return any(not (iv[i][1] <= p_[0] or iv[i][0] >= p_[1]) for k in range(nl[i]) for p_ in placed[r + k])
    for i in order:
        r = max([rows_[j] + nl[j] for j in cover[i]] + [0])
        while clash(i, r):
            r += 1
        rows_[i] = r
        for k in range(nl[i]):
            placed[r + k].append(iv[i])
    return rows_, iv, nl


def label_variants(pre, name, size, wrap_over):
    """One line, and for a long name also two balanced lines, each as rich parts with a measured width."""
    hr = TK['guard']['headroom']
    one = {'lines': [[(pre, 'th', 600), (name, 'tr', 400)] if pre else [(name, 'tr', 400)]], 'nl': 1,
           'w': (tw(pre, size, 600) + tw(name, size, 400)) * hr}
    out = [one]
    words = name.split(' ')
    if one['w'] > wrap_over and len(words) > 2:
        best = None
        for k in range(1, len(words)):
            l1, l2 = ' '.join(words[:k]), ' '.join(words[k:])
            w1, w2 = tw(pre, size, 600) + tw(l1, size, 400), tw(l2, size, 400)
            if best is None or max(w1, w2) < best[0]:
                best = (max(w1, w2), l1, l2)
        _, l1, l2 = best
        out.append({'lines': [[(pre, 'th', 600), (l1, 'tr', 400)] if pre else [(l1, 'tr', 400)], [(l2, 'tr', 400)]],
                    'nl': 2, 'w': best[0] * hr})
    return out


def stack_rows(items, left, right):
    """Rows for labels above a lane. A label that covers another event's dot sits above it, so no leader crosses a
    label, and labels in one row never overlap. Tries every anchor and line choice that fits and keeps the fewest
    rows, then the fewest two-line labels."""
    best = None
    opts = [[(an, v) for an in ('start', 'end') for v in range(len(it['variants']))] for it in items]
    for choice in itertools.product(*opts):
        if any((an == 'start' and it['x'] + it['variants'][v]['w'] + 4 > right)
               or (an == 'end' and it['x'] - it['variants'][v]['w'] - 4 < left)
               for it, (an, v) in zip(items, choice)):
            continue
        res = _rows_for(items, choice)
        if res is None:
            continue
        rows_, iv, nl = res
        score = (max(rows_[i] + nl[i] for i in rows_), sum(nl) , sum(rows_.values()), sum(an == 'end' for an, _ in choice))
        if best is None or score < best[0]:
            best = (score, choice, rows_, iv)
    if best is None:
        raise AssertionError('timeline labels cannot be placed in this lane')
    _, choice, rows_, iv = best
    for i, it in enumerate(items):
        an, v = choice[i]
        it['anchor'], it['row'], it['iv'] = an, rows_[i], iv[i]
        it['lines'], it['nl'] = it['variants'][v]['lines'], it['variants'][v]['nl']
    return items


def gen_s09(W, uid, t=None):
    """Timeline: the atlas's 24 dated rule changes on a true time scale, one lane per thread, every event named
    as the atlas names it. Shaded bands mark where the atlas's picks cluster."""
    a = Art(W, uid, t)
    t = a.t
    D = DS['history-events']
    ev = sorted(D['rows'], key=lambda r: r['date'])
    TH = {th['id']: th for th in D['threads']}
    threads = [th['id'] for th in D['threads']]
    hr = TK['guard']['headroom']
    y0r, y1r = (ev[0]['year'] // 5) * 5, ev[-1]['year'] + 1
    if W >= 900:
        size = TK['type']['note']
        LW = 170
        x0, x1 = LW + 8, W - 6

        def X(yr):
            return x0 + (yr - y0r) / (y1r - y0r) * (x1 - x0)
        row_h = 21
        ytop = 92
        y = ytop
        lanes = {}
        for th in threads:
            items = []
            for r in ev:
                if r['thread'] != th:
                    continue
                pre, name = event_label(r)
                items.append({'r': r, 'x': X(frac_year(r['date'])), 'variants': label_variants(pre, name, size, 300)})
            stack_rows(items, x0 - 2, x1)
            nrow = max(it['row'] + it['nl'] for it in items)
            qh = len(wrap(TH[th]['question'], (LW - 14) / hr, 14)) * 19 + 26
            h = max(nrow * row_h + 28, qh)
            lanes[th] = (y, h, items)
            y += h + 22
        H = y - 22 + 34
        for s0, s1 in STRETCHES:
            bx0, bx1 = X(s0), (X(s1 + 1) if s1 < ev[-1]['year'] else x1)
            a.rect(bx0, ytop - 62, bx1 - bx0, H - 34 - ytop + 62 + 8, 'f-band')
            n_in = sum(1 for r in ev if s0 <= r['year'] <= s1)
            anc = 'start' if s1 < ev[-1]['year'] else 'end'
            xx = bx0 + 6 if anc == 'start' else bx1 - 6
            a.text(xx, ytop - 42, f'{s0} to {s1}', t.nt, 'th', 600, anc)
            a.text(xx, ytop - 23, f'{nw(n_in)} of the {len(ev)} picks', t.nt, 'tn', 400, anc)
        for th in threads:
            ly, h, items = lanes[th]
            base = ly + h - 10
            a.line(x0, base, x1, base, 's-grid')
            a.text(0, ly + 16, TH[th]['label'], t.lbl, 'tl', 600)
            a.para(0, ly + 36, TH[th]['question'], LW - 14, 14, 'tn', 400, 19)
            for it in items:
                r = it['r']
                ty = base - 20 - it['row'] * row_h      # the shortest leader runs 12 px
                xx = it['x']
                a.line(xx, base - 4, xx, ty + 4, 's-ld')
                for k, parts in enumerate(it['lines']):
                    a.rich(xx + 3 if it['anchor'] == 'start' else xx - 3, ty - (it['nl'] - 1 - k) * row_h, parts, size, it['anchor'])
                a.circle(xx, base, 4.5, 'f-ink', da(r['key'], round(frac_year(r['date']), 4), field='date', mark='point', axis='x'))
        yb = H - 34
        a.line(x0, yb, x1, yb, 's-base')
        for yr in range(y0r + (25 - y0r % 25) % 25, y1r, 25):
            a.line(X(yr), yb, X(yr), yb + 5, 's-base')
            half = tw(str(yr), t.tk, 400) * hr / 2
            if X(yr) + half > W:
                a.text(W, yb + 22, str(yr), t.tk, 'tk', 400, 'end')
            else:
                a.text(X(yr), yb + 22, str(yr), t.tk, 'tk', 400, 'middle')
        return a, H
    # phone and middle widths: the four threads first, then time down one axis, each label naming its thread
    y = 16
    for th in threads:
        a.text(0, y, TH[th]['label'].upper(), 13, 'te', 700, track=0.06)
        y = a.para(0, y + 19, TH[th]['question'], W, 14, 'tn', 400, 19) + 26
    ax = max(48 if W < 600 else 70, math.ceil(tw('2000', 14, 400) * hr) + 12)
    lx = ax + 26
    lwid = W - lx
    y0p = y + 28
    py = 1060 if W < 600 else 980

    def Yp(yr):
        return y0p + (yr - y0r) / (y1r - y0r) * py
    blocks = []
    for r in ev:
        pre, name = event_label(r)
        first_w = lwid / hr - tw(pre, 14, 600)
        lines = wrap(name, first_w, 14)
        h = 18 + 19 * len(lines)
        blocks.append((r, pre, lines, h))
    cs = spread([Yp(frac_year(r['date'])) + h / 2 - 9 for r, _, _, h in blocks], [h for *_, h in blocks], y0p - 20, 1e6, 8)
    for s0, s1 in STRETCHES:
        a.rect(0, Yp(s0), ax + 12, Yp(s1 + 1) - Yp(s0), 'f-band')
    for yr in range(y0r + (25 - y0r % 25) % 25, y1r, 25):
        a.line(ax - 4, Yp(yr), ax, Yp(yr), 's-base')
        a.text(ax - 8, Yp(yr) + 5, str(yr), 14, 'tk', 400, 'end')
    for (r, pre, lines, h), c in zip(blocks, cs):
        yy = Yp(frac_year(r['date']))
        top = c - h / 2
        a.leader([(ax + 6, yy), (lx - 12, yy), (lx - 4, top + 6)] if abs(top + 6 - yy) > 0.5 else [(ax + 6, yy), (lx - 4, yy)])
        a.text(lx, top + 11, TH[r['thread']]['label'].upper(), 13, 'te', 700, track=0.06)
        for i, ln in enumerate(lines):
            if i == 0 and pre:
                a.rich(lx, top + 30, [(pre, 'th', 600), (ln, 'tr', 400)], 14)
            else:
                a.text(lx, top + 30 + 19 * i, ln, 14, 'tr', 400)
        a.circle(ax, yy, 4, 'f-ink', da(r['key'], round(frac_year(r['date']), 4), field='date', mark='point', axis='y'))
    endy = max(Yp(y1r), max(c + h / 2 for (*_, h), c in zip(blocks, cs)))
    a.line(ax, y0p - 10, ax, Yp(y1r), 's-base')
    return a, endy + 10


# ------------------------------------------------------------------------------------------------ S10 evidence mix
# One grade table for every chart that draws V7's evidence grades (production EX-S4): the key, the reader's words,
# the mark, and the title verbs the grade allows (Master Brief section 15).
GRADE_TABLE = [
    {'key': 'documented', 'word': 'Documented', 'meaning': 'on the public record', 'mark': 'ink', 'verbs': 'record language: passed, ruled, was'},
    {'key': 'well-supported', 'word': 'Well supported', 'meaning': 'strong research evidence', 'mark': 'ctx', 'verbs': 'a direct finding: raises, lowers'},
    {'key': 'plausible', 'word': 'Plausible', 'meaning': 'some evidence', 'mark': 'lt', 'verbs': '"can" or "may"'},
    {'key': 'contested', 'word': 'Contested', 'meaning': 'evidence disputed', 'mark': 'hatch', 'verbs': 'both readings, side by side'},
    {'key': 'hypothesis', 'word': 'Hypothesis', 'meaning': 'not yet tested', 'mark': 'dot', 'verbs': '"untested"'},
]
GRADE = {g['key']: g for g in GRADE_TABLE}
S10_CODE_NOTE = ('In this chart the shade is the grade code, darkest for documented; it replaces the usual rule that the '
                 'darkest mark is the subject.')


def gen_s10(W, uid, t=None):
    """Evidence mix: each answer's claims split by grade, sorted by the documented share, with the claim count
    beside each share. Grades step from the darkest ink to a hatch, never red; the vertical rule gives the share
    across every claim."""
    a = Art(W, uid, t)
    t = a.t
    narrow = W < 600
    hr = TK['guard']['headroom']
    D = DS['claims-by-grade']
    grades = D['grades']
    R = sorted(D['rows'], key=lambda r: (-r['documented'] / r['value'], r['key']))
    tot = D['totals']
    n_all = sum(tot.values())
    allshare = tot['documented'] / n_all
    lbl = t.lbl - 1 if not narrow else 14
    yk = flow_key(a, 0, 16, [(GRADE[g]['mark'], f'{GRADE[g]["word"]}: {D["grade_meaning"][g]}') for g in grades], W, 14, 20, 24)
    yk = a.para(0, yk + 26, S10_CODE_NOTE, TK['note']['width'] if not narrow else W)
    lab_w = max(tw(f'{pct0(r["documented"] / r["value"] * 100)} of {r["value"]}', t.lbl, 600) for r in R) * hr
    if narrow:
        BX, BW = 0, W - lab_w - 8
        bh, pitch = 14, 54
    else:
        LW = max(tw(r['title'], lbl, 600) for r in R) * hr + 4
        BX = LW + 10
        BW = W - BX - lab_w - 10
        bh, pitch = TK['bar']['dense_height'], TK['bar']['dense_pitch']
    head = 'Documented share'
    hw_ = tw(head, t.tk, 400) * hr
    ref = f'All {n_all} claims: {pct0(allshare * 100)} documented'
    rw_ = tw(ref, t.nt, 600) * hr
    stacked = rw_ + hw_ + 20 > W       # on phones the reference label takes its own line above the column head
    y = yk + 58 + (22 if stacked else 0)
    xr = BX + BW * allshare
    a.text(W, y - 24, head, t.tk, 'tk', 400, 'end')
    if stacked:
        a.text(min(max(xr - rw_ / 2, 0), W - rw_), y - 46, ref, t.nt, 'th', 600)
    else:
        a.text(min(max(xr - rw_ / 2, 0), W - hw_ - 20 - rw_), y - 24, ref, t.nt, 'th', 600)
    rows_y = {}
    ytop = y - 10
    for r in R:
        if narrow:
            lines = wrap(r['title'], W / hr, 14, 600)
            for i, ln in enumerate(lines[:2]):
                a.text(0, y + i * 18, ln, 14, 'tl', 600)
            by = y + 8 + (len(lines[:2]) - 1) * 18
        else:
            by = y - bh / 2
            a.text(0, y + 5, r['title'], lbl, 'tl', 600)
        x = BX
        for g in grades:
            v = r[g]
            if not v:
                continue
            w = BW * v / r['value']
            seg_rect(a, x, by, w, bh, GRADE[g]['mark'], da(r['key'], v, field=g, mark='bar', axis='x', scale=r['key']))
            x += w
        share = r['documented'] / r['value'] * 100
        a.rich(W, by + bh / 2 + 5, [(pct0(share), 'tl', 600), (f' of {r["value"]}', 'tr', 400)], t.lbl, 'end',
               attrs=da(r['key'], r['documented'], field='documented', mark='label'))
        rows_y[r['key']] = (by, by + bh)
        if narrow:
            a.line(0, by - 3, 0, by + bh + 3, 's-base')
            a.line(xr, by - 3, xr, by + bh + 3, 's-mark')
        y = by + bh + (pitch - bh) if narrow else y + pitch
    ybot = max(v[1] for v in rows_y.values())
    if not narrow:
        a.line(xr, ytop, xr, ybot + 6, 's-mark')
        a.line(BX, ytop, BX, ybot + 6, 's-base')
    return a, ybot + 10


# ------------------------------------------------------------------------------------------------ the figure frame
GRADE_LINE = {
    'S01': 'Documented: a published survey and two recorded votes',
    'S02': 'Official statistic: a Census Bureau survey',
    'S03': "Documented: the atlas's dated log, coded by the atlas",
    'S04': 'Official statistic: what survey respondents reported',
    'S05': 'Official statistic: a Census Bureau survey',
    'S06': 'Conditional directions: no forecast and no odds',
    'S07': 'A compiled list: Ballotpedia, checked against the atlas',
    'S08': "Documented: the atlas's dated log, coded by the atlas",
    'S09': 'Documented: every event rests on an official record',
    'S10': "Documented: the atlas's own register of graded claims",
}
ATLAS_WORDS = "the atlas, Oath & Action's own research"
ARTBOARDS = (('wide', 'ab-w'), ('mid', 'ab-m'), ('phone', 'ab-p'), ('small_phone', 'ab-s'))


def source_text(did):
    """The dataset's source line for readers: no record codes (F12) and no corrective negation, facts kept."""
    s = DS[did]['source_line']

    def dated(m):
        r = next(r for d_ in DS.values() if isinstance(d_, dict) and isinstance(d_.get('rows'), list)
                 for r in d_['rows'] if isinstance(r, dict) and r.get('key') == m.group(1) and 'date' in r)
        return f'One row, dated {date_words(r["date"])},'
    s = re.sub(r'One row \((RL\d+)\)', dated, s)
    s = s.replace("a claim's grade covers that claim, not the whole answer", "a claim's grade covers that claim alone")
    assert not re.search(r'\b(RL|PW|E)\d\d\b', s), s
    return re.sub(r'^Source:\s*', '', copy(s)).replace('Snapshot of', 'snapshot of').replace('. snapshot of', '. Snapshot of')


def table_html(caption, header, body, num_cols=(), cls='eqt'):
    th = ''.join(f'<th scope="col"{" class=num" if i in num_cols else ""}>{e(h)}</th>' for i, h in enumerate(header))
    trs = []
    for r in body:
        cells = []
        for i, c in enumerate(r):
            cells.append(f'<th scope="row">{e(c)}</th>' if i == 0 else f'<td{" class=num" if i in num_cols else ""}>{e(c)}</td>')
        trs.append('<tr>' + ''.join(cells) + '</tr>')
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{e(caption)}, table">'
            f'<table class="{cls}"><caption>{e(caption)}</caption><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>')


def artboards(view, sid, gen, wide, label, **kw):
    """Draw one generator at the figure's full width and at the 600, 358 and 328 px artboards. Returns the HTML and
    every string the drawings print, for the equivalent check."""
    out, strings = [], []
    widths = [(wide, 'ab-w')] + [(TK['artboard'][k], c) for k, c in ARTBOARDS[1:]]
    for W, cls in widths:
        art, H = gen(W, f'{view}-{sid.lower()}-{W}', **kw)
        out.append(art.render(H, label, f'ab {cls}', f'{sid.lower()}-{view}-{W}'))
        strings += art.strings
    return f'<div class="art w{wide}">{"".join(out)}</div>', strings


def _norm(s):
    return re.sub(r'\s+', ' ', copy(s).replace(' ', ' ').replace('’', "'").replace('‘', "'")
                  .replace('“', '"').replace('”', '"')).strip().lower()


def figure(view, sp):
    """One chart in the system's frame, built from one spec object. sp holds: sid, title, measure, body, strings
    (drawn), drawn_notes, notes (shown under the drawing), table, label, extra, wide, and optionally dataset,
    evidence, grade_line, source and disclosure. A new chart passes those five; S01 to S10 fall back to the shared
    data by ID. Every string the drawing prints must reach the image name or the equivalent (F15); the build stops
    if one does not."""
    sid = sp['sid']
    did = sp.get('dataset') or SPECS[sid]['dataset']
    ds = DS.get(did, {})
    ev = sp.get('evidence') or ds['evidence']
    src = sp.get('source') or source_text(did)
    grade_line = sp.get('grade_line') or GRADE_LINE[sid]
    notes = sp.get('notes', [])
    disclosure = sp.get('disclosure', ds.get('required_text', []))
    vis = ''
    if notes or disclosure:
        vis = '<ul class="fnotes">' + ''.join(f'<li>{e(n)}</li>' for n in notes) + '</ul>'
        vis += ''.join(f'<p class="disc"><b>Disclosure:</b> {e(d)}</p>' for d in disclosure)
    drawn = sp.get('drawn_notes', [])
    pool = _norm(' '.join([sp.get('label', ''), sp['title'], sp['measure'], ' '.join(drawn), ' '.join(notes),
                           re.sub(r'<[^>]+>', ' ', sp['table'])]))
    missing = []
    for s_ in dict.fromkeys(sp.get('strings', [])):
        if is_num(s_) or _norm(s_) in pool or len(s_.strip()) < 2:
            continue
        missing.append(s_)
    if missing:
        drawn = drawn + ['Also in the drawing: ' + '; '.join(m.rstrip('.') for m in missing) + '.']
    note_html = ''.join(f'<li>{e(n)}</li>' for n in drawn)
    eq = (f'<details class="eq" data-role="equivalent"><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> '
          f'the table and notes<span class="vh2"> for {sid}</span></span></summary>'
          f'<div class="eqb"><p class="eqh">Notes in the chart</p><ul class="eqn">{note_html}</ul>{sp["table"]}'
          f'<p class="src">Source: {e(src)}</p></div></details>')
    return (f'<figure class="fig{" wide" if sp.get("wide") else ""}" id="{view}-{sid.lower()}-fig" data-spec="{sid}" '
            f'data-dataset="{ea(did)}" data-evidence="{ea(ev)}">'
            f'<div class="evrow"><p class="ev" data-role="evidence-label">{e(ev)}</p><p class="grade">{e(grade_line)}</p></div>'
            f'<h2 class="ct" id="{view}-{sid.lower()}-t" data-role="title">{e(sp["title"])}</h2>'
            f'<p class="ms" data-role="measure">{e(sp["measure"])}</p>'
            f'{sp["body"]}{sp.get("extra", "")}{vis}'
            f'<div class="srcrow"><p class="src" data-role="source"><span class="sl">Source:</span> {e(src)}</p>'
            f'<p class="src credit"><a href="#system/read">How to read our charts</a><span aria-hidden="true"> · </span>Chart: Oath &amp; Action</p></div>'
            f'{eq}</figure>')


def strip(view, sid, why):
    spec = SPECS[sid]
    return (f'<div class="strip"><p class="stag">Studio note, not part of the chart</p>'
            f'<h3 class="sid">{sid} <span>{e(spec["form"])}</span></h3>'
            f'<dl><dt>Reader question</dt><dd>{e(spec["reader_question"])}</dd>'
            f'<dt>Why this form</dt><dd>{e(why)}</dd></dl></div>')


# ------------------------------------------------------------------------------------------------ the ten specimens
WHY = {
    'S01': 'One large figure gives the fact a reader repeats; the party bars and the two votes put it in context in the same drawing.',
    'S02': 'A line shows the rise and fall in order, and notes at 2021, 2025 and the method breaks explain what a reader could misread.',
    'S03': "Ranked bars answer who acted most, and splitting each bar by the atlas's direction code shows which way each instrument moved the rules.",
    'S04': 'A dumbbell puts two elections on one line for each age group, so the level and the change read at once.',
    'S05': 'Small multiples give each group its own panel on one scale, so a reader follows one line at a time and still sees the others.',
    'S06': "A table lets a reader look up one scenario and one outcome; the atlas's own words sit in every cell beside our arrow.",
    'S07': 'A tile map gives each state the same weight, so the count reads true where a land map would favor large western states.',
    'S08': 'One square per entry lets a reader count, and placing toward above the year band and away below it shows both sides of the log at once.',
    'S09': 'A true time scale shows when the atlas’s picks bunch together, and four lanes keep each thread readable.',
    'S10': 'A bar split by grade shows how much of each answer rests on the record, and sorting by that share puts the answers in order.',
}


def log_notes():
    """The repair log's shared notes (F1): what the log is, the coding rule in full, one map example from each side,
    the roll-up entry, and the atlas's neutrality line word for word."""
    D = rows('rule-changes')
    recent = sum(1 for r in D if r['year'] >= 2025)
    assert recent == 33 and len(D) == 64
    rl38, rl41 = row('rule-changes', 'RL38'), row('rule-changes', 'RL41')
    assert rl38['direction'] == rl41['direction'] == 'away from voters'
    note = DS['rule-changes']['coding_note']
    assert 'the reform profiles R-01 and R-02 rate' in note
    neutral = 'A row\'s direction describes the rule\'s effect on who officials answer to and carries no judgment of the people or parties involved.'
    assert neutral in note
    return [
        f'The log holds the {len(D)} changes the atlas chose to record, not every rule change in the country. '
        f'It records more of recent years: {recent} of the {len(D)} entries fall in 2025 and 2026.',
        'How the atlas codes direction: ' + note.replace(' ' + neutral, '').replace(
            'the reform profiles R-01 and R-02 rate', "the atlas's profiles of those two reforms rate"),
        "A map redrawn in the middle of a decade counts as away from voters whichever party draws it: Texas's HB 4 "
        "(August 2025) and California's Proposition 50 (November 2025) both count as away.",
        'One entry, dated March 2026, stands for all 19 state bans on ranked-choice voting; Missouri\'s and Indiana\'s bans also have entries of their own.',
        neutral,
    ]


def spec_s01(view):
    R = {r['key']: r for r in rows('stock-trading-ban')}
    title = 'Nearly nine in ten Republican and Democratic voters favored a ban on stock trading by members of Congress.'
    measure = ('Registered voters who favor a ban, percent, by party, survey of May 2023, United States; '
               'votes on H.R. 7008 in the House (July 22, 2026) and the Senate (September 30, 2026)')
    label = ('Big number: 86 percent of registered voters favored a ban; by party, 88 percent of Democrats and 87 percent of Republicans. '
             'The House passed a ban, H.R. 7008, 232 to 198; the Senate vote to take it up was 53 to 47, 7 votes short of the 60 needed.')
    body, strings = artboards(view, 'S01', gen_s01, TK['artboard']['reading'], label)
    notes = ['Survey of 2,625 registered voters, May 19 to 30, 2023, three years before either vote.',
             'The two parties sit one point apart; the bars run from 0 to 100 percent.',
             'Taking up the bill needed 60 votes, three-fifths of the Senate, to end debate (cloture).']
    table = table_html('Support for a ban and the votes that followed', ['Group', 'Measure', 'Value'],
                       [[r['group'], r['measure'], str(r['value'])] for r in rows('stock-trading-ban')], (2,))
    return dict(sid='S01', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=['What Congress did next: the House passed a ban (H.R. 7008); the Senate vote to take it up fell short, 7 votes short of the 60 needed.'],
                table=table)


def spec_s02(view):
    D = rows('child-poverty-spm')
    spm = [r for r in D if r['measure'] == 'spm']
    low = min(spm, key=lambda r: r['percent'])
    p20 = next(r for r in spm if r['year'] == low['year'] - 1)['percent']
    p22 = next(r for r in spm if r['year'] == low['year'] + 1)['percent']
    assert p22 > 2 * low['percent']
    title = (f'Child poverty fell to {low["percent"]} percent in {low["year"]}, the lowest since the series began in '
             f'{min(r["year"] for r in D)}, and more than doubled the next year.')
    measure = ('Children under 18 below the Supplemental Poverty Measure, which counts tax credits and other aid, percent, '
               'United States, 2009 to 2025; the official measure, which counts pretax cash income only, in gray. The scale starts at zero.')
    label = (f'Line chart: child poverty under the Supplemental Poverty Measure fell from {p20} percent in 2020 to {low["percent"]} percent '
             f'in 2021, then rose to {p22} percent in 2022 and 13.4 percent in 2025; the official measure ran from 22.0 to 13.4 percent.')
    body, strings = artboards(view, 'S02', gen_s02, TK['artboard']['reading'], label)
    drawn = [S02_NOTE_2021, f'{low["year"] + 1}: {p22}%.', 'Both measures: 13.4% in 2025. ' + s02_law_note(),
             'Census changed its survey or method in 2013, 2017 and 2019. The line breaks there, and each of those years shows two estimates, one for each method.',
             'Lines: the dark line is the Supplemental Poverty Measure; the gray line is the official measure. The scale runs from 0 to 25 percent.']
    body_rows = [[str(r['year']), 'Supplemental' if r['measure'] == 'spm' else 'Official', r['series_variant'].replace('_', ' '),
                  f'{r["percent"]:.1f}', f'{r["moe_pct"]:.1f}' if isinstance(r['moe_pct'], float) else 'not given']
                 for r in sorted(D, key=lambda r: (r['year'], r['measure'], r['series_variant']))]
    table = table_html('Children in poverty, percent', ['Year', 'Measure', 'Estimate', 'Percent', 'Margin of error (90%)'], body_rows, (3, 4))
    return dict(sid='S02', title=title, measure=measure, body=body, strings=strings, label=label, drawn_notes=drawn, table=table)


def spec_s03(view):
    D = sorted(rows('rule-changes-by-instrument'), key=lambda r: -r['value'])
    ss = row('rule-changes-by-instrument', 'State statute')
    bi = row('rule-changes-by-instrument', 'Ballot initiative')
    rf = row('rule-changes-by-instrument', 'Referendum')
    assert ss['away from voters'] == max(r['away from voters'] for r in D)
    passed = bi['toward voters'] + bi['away from voters'] + bi['mixed']
    assert bi['away from voters'] == 0 and passed == bi['toward voters']
    title = f'The atlas codes {nw(ss["away from voters"])} of the {ss["value"]} state statutes in its log as moving the rules away from voters.'
    measure = (f"Entries in the repair log of {ATLAS_WORDS}, by how the rule changed and by the atlas's direction code, "
               'August 1965 to the November 3, 2026 ballot')
    label = ('Ranked bar chart of the 64 entries by instrument, each split by the atlas\'s direction code: '
             + '; '.join(f'{r["key"]} {r["value"]}, {r["away from voters"]} away from voters, {r["toward voters"]} toward' for r in D) + '.')
    body, strings = artboards(view, 'S03', gen_s03, TK['artboard']['reading'], label)
    roll = row('rule-changes', ROLLUP_KEY)
    assert roll['instrument_group'] == 'State statute' and roll['direction'] == 'away from voters'
    st_rows = [r for r in rows('rule-changes') if r['instrument_group'] == 'State statute' and r['direction'] == 'away from voters']
    rcv = [r for r in st_rows if 'ranked-choice' in r['rule'] or 'ranked choice' in r['rule']]
    maps_ = [r for r in st_rows if 'congressional' in r['rule'] and ('map' in r['rule'] or 'districts' in r['rule'])]
    assert len(rcv) == 3 and len(maps_) == 5, (len(rcv), len(maps_))
    notes = [
        f'Citizen ballot initiatives: {bi["value"]} entries. {nw(passed, cap=True)} passed, and all {nw(passed)} moved the rules toward voters; '
        f'{nw(bi["voters kept existing rules"])} failed and left the rules in force; {nw(bi["pending"])} are pending. '
        f'Referendums are ballot measures too, and {nw(rf["away from voters"])} of {rf["value"]} moved the rules away from voters.',
        f'State statutes: {nw(len(maps_))} of the {nw(ss["away from voters"])} are mid-decade congressional maps and {nw(len(rcv))} limit '
        f'ranked-choice voting, entries the atlas says readers may weigh differently. Without those {nw(len(rcv))}, '
        f'{nw(ss["away from voters"] - len(rcv))} of {nw(ss["value"] - len(rcv))} statutes moved the rules away from voters, still the largest share. '
        f'Without the roll-up entry for 19 states, {nw(ss["away from voters"] - 1)} of {nw(ss["value"] - 1)} did.',
        'Oath & Action grouped an agency rule, an executive action and an executive order as one instrument, and a city law with a council funding vote as another.',
    ] + log_notes()
    hdr = ['Instrument', 'All'] + [DIR_WORD[d] for d in DIR_ORDER]
    table = table_html('Repair-log entries by instrument and direction', hdr,
                       [[r['key'], str(r['value'])] + [str(r[d]) for d in DIR_ORDER] for r in D], tuple(range(1, 7)))
    return dict(sid='S03', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=['Labels at the bars: ' + '; '.join(f'{k}, {v}' for k, v in s03_annotations(D).items()) + '.'], table=table)


def spec_s04(view):
    base = 'citizen_voting_age_population'
    R = {(r['age_group'], r['year']): r for r in rows('turnout-by-age') if r['base'] == base}
    g20 = R[('65_and_over', 2020)]['voted_pct'] - R[('18_to_24', 2020)]['voted_pct']
    g24 = R[('65_and_over', 2024)]['voted_pct'] - R[('18_to_24', 2024)]['voted_pct']
    title = (f'The gap in reported voting between citizens 18 to 24 and those 65 and over grew from '
             f'{round(g20)} points in 2020 to {round(g24)} in 2024.')
    measure = ('Citizens who reported voting in November, percent, by age group, 2020 and 2024 presidential elections, United States; '
               'the scale runs from 40 to 80 percent')
    groups = ['18_to_24', '25_to_44', '45_to_64', '65_and_over']
    label = ('Dot plot of reported voting by age group: ' + '; '.join(
        f'{age_words(g)}, {R[(g, 2020)]["voted_pct"]} in 2020 and {R[(g, 2024)]["voted_pct"]} in 2024' for g in groups) + '.')
    body, strings = artboards(view, 'S04', gen_s04, TK['artboard']['reading'], label)
    drawn = [f'The gap between citizens 18 to 24 and those 65 and over: {g20:.1f} points in 2020, {g24:.1f} in 2024.',
             'These rates are what people told a Census survey, which runs higher than counted ballots. Table A-1 publishes no margins of error, so a change of a point or two may sit within survey error.',
             'Changes of two points or less read as little change.']
    body_rows = []
    for g in groups:
        v0, v1 = R[(g, 2020)]['voted_pct'], R[(g, 2024)]['voted_pct']
        ch = v1 - v0
        body_rows.append([age_words(g), f'{v0:.1f}', f'{v1:.1f}', (MINUS if ch < 0 else '+') + f'{abs(ch):.1f}'])
    table = table_html('Reported voting, citizens, percent', ['Age group', '2020', '2024', 'Change, points'], body_rows, (1, 2, 3))
    return dict(sid='S04', title=title, measure=measure, body=body, strings=strings, label=label, drawn_notes=drawn, table=table)


def spec_s05(view):
    H = rows('homeownership-by-race')

    def v(g, y):
        return next(r for r in H if r['group'] == g and r['year'] == y and r['series_variant'] == 'standard')['rate_pct']
    w25, b25, w03, b03 = v('non_hispanic_white', 2025), v('black', 2025), v('non_hispanic_white', 2003), v('black', 2003)
    h25, h03 = v('hispanic', 2025), v('hispanic', 2003)
    assert 29 < w25 - b25 < 30 and (w25 - b25) > (w03 - b03)
    title = 'Non-Hispanic White and Black homeownership rates were nearly 30 points apart in 2025, a wider gap than in 2003.'
    measure = ('Households that own their home, percent, by race and ethnicity of householder, annual averages, '
               'United States, 1994 to 2025. Every panel runs from 40 to 80 percent.')
    label = (f'Four small line charts of homeownership, 1994 to 2025, one per group. In 2025: all households {v("all_households", 2025)} percent, '
             f'non-Hispanic White {w25}, Hispanic {h25}, Black {b25}. Gap to non-Hispanic White: Black {w03 - b03:.1f} points in 2003 and '
             f'{w25 - b25:.1f} in 2025; Hispanic {w03 - h03:.1f} and {w25 - h25:.1f}.')
    body, strings = artboards(view, 'S05', gen_s05, TK['artboard']['wide'], label)
    notes = ['The lines break where the Census changed its method: in 2002 it reweighted its estimates to the 2000 Census, so that year '
             'shows two values, and in 2003 it changed its race categories, so the Black and non-Hispanic White lines start again.',
             'The Census Bureau asks readers to use caution comparing 2020 with other years, after interviews moved to the phone.',
             'Brackets give the gap to non-Hispanic White households in 2003 and 2025, in percentage points.']
    years = sorted({(r['year'], r['series_variant']) for r in H if r['group'] == 'all_households'})
    groups = ['all_households', 'non_hispanic_white', 'black', 'hispanic']
    body_rows = []
    for y, sv in years:
        cells = [str(y) + (' (original)' if sv == 'original' else ' (reweighted)' if sv.startswith('revised') else '')]
        for g in groups:
            r = next((r for r in H if r['group'] == g and r['year'] == y and r['series_variant'] == sv), None)
            cells.append(f'{r["rate_pct"]:.1f}' if r else '')
        body_rows.append(cells)
    table = table_html('Homeownership rate, percent', ['Year'] + [group_words(g) for g in groups], body_rows, (1, 2, 3, 4))
    return dict(sid='S05', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=['Gray lines: the other three groups. Each panel heads with the group and its 2025 rate.'], table=table, wide=True)


def spec_s06(view):
    D = DS['scenarios-2030']
    ii = row('scenarios-2030', 'ii')
    lift = [r for r in D['rows'] if r['key'] != 'i' and any(
        r[f'{k}_class'] in ('up', 'slightly up') or (r[f'{k}_class'] == 'same as ii' and ii[f'{k}_class'] in ('up', 'slightly up'))
        for k in D['families'])]
    others = len(D['rows']) - 1
    assert len(lift) == 5 and others == 7
    title = f'If their assumptions hold, {nw(len(lift))} of the {nw(others)} scenarios beyond the baseline would lift at least one outcome family by 2036.'
    measure = (f"The direction each outcome family would take by 2036 under eight scenarios, in the words of {ATLAS_WORDS}, "
               'United States, from a 2026 baseline')
    body = f'<div class="art tbl">{gen_s06_table(view)}</div>'
    why = []
    for r in D['rows']:
        why.append(f'<h3>{e(r["key"])}. {e(r["name"])}</h3><p><b>Assumptions:</b> {e("; ".join(r["assumptions"]))}.</p><ul>')
        for k in D['families']:
            w = r.get(f'{k}_why') or 'The atlas gives no separate reason.'
            why.append(f'<li><b>{e(D["families"][k])}, {e(r[k])}:</b> {e(w)}</li>')
        why.append('</ul>')
    rule = D['class_method'][D['class_method'].index('Words that start'):]
    notes = ["Arrow and tint are Oath & Action's reading of the atlas's words, which always print beside them. " + rule,
             'The atlas wrote the eight scenarios and their assumptions; the assumptions sit in the table under the chart.',
             'Up means better for each family; for income and wealth equality, more equal.']
    return dict(sid='S06', title=title, measure=measure, body=body, strings=[], label='', notes=notes,
                drawn_notes=[TNOTE], table=f'<div class="why">{"".join(why)}</div>', wide=True)


def spec_s07(view):
    D = rows('rcv-bans')
    C = s07_counts()
    title = f'{nw(C["bans"], cap=True, start=True)} states ban ranked-choice voting as of November 2026, {C["all"]} of them in all elections.'
    measure = ('State laws that prohibit ranked-choice voting, by scope, 50 states and the District of Columbia, '
               'as of November 2026. Each square is one state.')
    label = (f'Tile map of the 50 states and DC: {C["bans"]} states ban ranked-choice voting, {C["all"]} in all elections and '
             f'{len(C["some"])} in some ({" and ".join(C["some"])}); {C["none_states"]} states and DC have no state ban. The table below lists every state.')
    body, strings = artboards(view, 'S07', gen_s07, TK['artboard']['reading'], label)
    yrs = Counter(r['enacted_year'] for r in D if r['enacted_year'])
    some = [r for r in D if r['status'] == 'bans in some elections']
    ms = row('rcv-bans', 'MS')
    notes = ['Ranked-choice voting: voters rank candidates in order; if no one wins a majority of first choices, the last-place '
             'candidate drops out and those ballots count for their next choice, round by round.',
             f'{C["none_states"]} states and DC have no state ban. A state with no ban may still keep its cities from adopting it, '
             'because many cities need the state\'s permission. The map shows bans only.',
             f'{nw(yrs.get(2024, 0) + yrs.get(2025, 0), cap=True, start=True)} of the {C["bans"]} bans became law in 2024 or 2025. Each square is one state, whatever its size.']
    notes += [f'{r["name"]}: {r["scope_note"]}.' for r in some]
    notes += [f'Ballotpedia reads {C["all"]} of the bans as covering all elections; Mississippi\'s quoted text does not name congressional races. '
              'Ballotpedia is a secondary source; the atlas cites the National Conference of State Legislatures.']
    assert 'congressional' in ms['scope_note']
    body_rows = [[r['name'], STATUS_WORD[r['status']], str(r['enacted_year']) if r['enacted_year'] else '', r['measure'] or '']
                 for r in sorted(D, key=lambda r: r['name'])]
    table = table_html('Ranked-choice voting bans by state', ['State', 'Status', 'Year', 'Measure'], body_rows, (2,))
    return dict(sid='S07', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=['Key: bans it in all elections, with the year it became law; bans it in some elections; no state ban.'], table=table)


def spec_s08(view):
    D = rows('rule-changes')
    c = Counter(r['direction'] for r in D)
    assert DS['rule-changes']['counts'] == dict(c)
    bins, first = s08_bins(D)
    roll = row('rule-changes', ROLLUP_KEY)
    listed = re.findall(r'([A-Z][a-z]+(?: [A-Z][a-z]+)?) (20\d\d)', roll['rule'].split(':', 1)[1].split('.')[0])
    own = {r['jurisdiction'] for r in D if r['key'] != ROLLUP_KEY and r['direction'] == 'away from voters'
           and re.search(r'ranked[- ]choice', r['rule'])}      # states whose ban has its own entry
    before = [st for st, yr in listed if int(yr) < 2025]
    before_alone = [st for st in before if st not in own]
    assert len(listed) == 19 and len(before) == 11 and len(before_alone) == 10, (len(listed), before, before_alone)
    title = (f'Of the {len(D)} rule changes in its log, the atlas codes {c["toward voters"]} as moving the rules toward voters '
             f'and {c["away from voters"]} as moving them away.')
    measure = (f"Each square is one entry in the repair log of {ATLAS_WORDS}, placed by year and by the atlas's direction code, "
               '1965 to the November 3, 2026 ballot. The count beside each year gives every entry the log holds that year.')
    per_year = Counter(r['year'] for r in D)
    label = (f'Unit chart of the {len(D)} entries: {c["toward voters"]} toward voters, {c["away from voters"]} away, '
             f'{c["voters kept existing rules"]} where voters kept existing rules, {c["mixed"]} mixed and {c["pending"]} pending. '
             'Entries per year: ' + ', '.join(f'{y} {n}' for y, n in sorted(per_year.items())) + '.')
    body, strings = artboards(view, 'S08', gen_s08, TK['artboard']['wide'], label)
    notes = [f'The first year group, To {first - 1}, holds every entry from {min(per_year)} to {first - 1}.',
             f'The ringed square marked 19 states is one entry dated March 2026. {nw(len(before), cap=True, start=True)} of its 19 bans passed '
             f'before 2025, and {nw(len(before_alone))} of those have no entry of their own.',
             'Open squares count toward voters and solid squares away from voters; the band below holds entries that went neither way.'] + log_notes()
    body_rows = [[r['key'], date_words(r['date']), r['jurisdiction'], r['instrument_group'], DIR_WORD[r['direction']]] for r in D]
    table = table_html('Every entry in the repair log', ['Entry', 'Date', 'Where', 'Instrument', 'Direction'], body_rows)
    return dict(sid='S08', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=['Rows: all entries per year; toward voters; away from voters; neither way (voters kept existing rules when a ballot measure failed, mixed, or pending on November 3, 2026).'],
                table=table, wide=True)


def spec_s09(view):
    D = DS['history-events']
    ev = D['rows']
    threads = D['threads']
    title = ('The atlas traces 24 rule changes since 1870 on four threads: '
             + ', '.join(th['label'].lower() for th in threads[:-1]) + f' and {threads[-1]["label"].lower()}.')
    assert len(ev) == 24 and len(threads) == 4
    measure = ('Changes in the rules on four threads, dated by the atlas, United States, February 1870 to June 2026. '
               'Every event is documented; the atlas chose which to date.')
    by_th = Counter(r['thread_label'] for r in ev)
    label = ('Timeline of 24 rule changes from 1870 to 2026 on four lanes: ' + '; '.join(f'{th["label"]}, {by_th[th["label"]]}' for th in threads)
             + '. Shaded: 1964 to 1978 and 2010 to 2026, where the atlas\'s picks cluster.')
    body, strings = artboards(view, 'S09', gen_s09, TK['artboard']['wide'], label)
    n1 = sum(1 for r in ev if 1964 <= r['year'] <= 1978)
    n2 = sum(1 for r in ev if 2010 <= r['year'] <= 2026)
    notes = [f'Shaded: the two stretches where the atlas\'s picks cluster, {nw(n1)} changes from 1964 to 1978 and {nw(n2)} from 2010 to 2026. '
             'The atlas chose which changes to date, so the bands describe its picks.',
             D['events_note']]
    drawn = ['Threads: ' + '; '.join(f'{th["label"]}: {th["question"]}' for th in threads),
             'Event names are the atlas\'s, shortened at any parenthesis; the table gives each in full.']
    body_rows = [[r['key'], date_words(r['date']), r['thread_label'], r['title'], r['mechanism']] for r in sorted(ev, key=lambda r: r['date'])]
    table = table_html('Twenty-four rule changes since 1870', ['Event', 'Date', 'Thread', 'Change', 'What it did'], body_rows)
    return dict(sid='S09', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=drawn, table=table, wide=True)


def spec_s10(view):
    D = DS['claims-by-grade']
    tot = D['totals']
    n = sum(tot.values())
    share = tot['documented'] / n
    assert 0.72 < share < 0.76
    R = sorted(D['rows'], key=lambda r: (-r['documented'] / r['value'], r['key']))
    title = f'About three in four claims behind the atlas\'s {len(D["rows"])} everyday answers are documented on the public record.'
    measure = (f"Claims in the register of {ATLAS_WORDS}, by evidence grade, as a share of each answer's claims, {n} claims, "
               'checked through October 15, 2026, United States')
    label = (f'Sixteen bars, one per everyday answer, split by evidence grade and sorted by the documented share: '
             + '; '.join(f'{r["title"]} {pct0(r["documented"] / r["value"] * 100)} of {r["value"]}' for r in R)
             + f'. Across all {n} claims, {pct0(share * 100)} are documented.')
    body, strings = artboards(view, 'S10', gen_s10, TK['artboard']['reading'], label)
    top, low = R[0], R[-1]
    con = max(R, key=lambda r: (r['contested'], r['key']))
    notes = [f'{top["title"]}: {top["documented"]} of {top["value"]} claims documented, the highest share. '
             f'{low["title"]}: {low["documented"]} of {low["value"]}, the lowest. '
             f'{con["title"]}: {con["contested"]} of {con["value"]} claims contested, the most of any answer.',
             'Grades: ' + '; '.join(f'{GRADE[g]["word"].lower()} means {D["grade_meaning"][g]}' for g in D['grades']) + '.',
             "A claim's grade covers that claim and says nothing about the rest of its answer."]
    body_rows = [[r['title'], r['question'], str(r['value'])] + [str(r[g]) for g in D['grades']] + [pct0(r['documented'] / r['value'] * 100)] for r in R]
    table = table_html('Claims by evidence grade for each everyday answer', ['Answer', 'Reader question', 'Claims'] + [GRADE[g]['word'] for g in D['grades']] + ['Documented share'],
                       body_rows, (2, 3, 4, 5, 6, 7))
    return dict(sid='S10', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=[S10_CODE_NOTE, f'All {n} claims: {pct0(share * 100)} documented. Each row prints its documented share and its number of claims.'],
                table=table)


SPEC_FN = {'S01': spec_s01, 'S02': spec_s02, 'S03': spec_s03, 'S04': spec_s04, 'S05': spec_s05,
           'S06': spec_s06, 'S07': spec_s07, 'S08': spec_s08, 'S09': spec_s09, 'S10': spec_s10}


def specimen(view, sid):
    """A chart section: the figure first, then the studio strip (shown at left on wide screens)."""
    return (f'<section class="spec" id="{view}-{sid.lower()}" aria-labelledby="{view}-{sid.lower()}-t">'
            f'{figure(view, SPEC_FN[sid](view))}{strip(view, sid, WHY[sid])}</section>')


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


def copy_html(h):
    """Run the copy function over the text between tags only, so attribute quotes stay straight."""
    return re.sub(r'(^|>)([^<]+)', lambda m: m.group(1) + html.escape(copy(html.unescape(m.group(2))), quote=False), h)


def view_head(view, eyebrow, h1, deck, links=True, extra=''):
    lk = ''
    if links:
        desc = {'white': 'the ten charts on White', 'newsprint': 'the same ten charts on the warm ground',
                'dark': 'two charts and the dark palette', 'social': 'one chart at 1080 by 1350',
                'system': 'the rules on one sheet, and how to read our charts'}
        items = ''.join(f'<li><a href="#{v}">{e(t)}</a> <span>{e(desc[v])}</span></li>' for v, t in VIEWS if v != view)
        lk = f'<nav class="vlinks" aria-label="Other views of this concept"><p class="eyebrow">Other views</p><ul>{items}</ul></nav>'
    return (f'<header class="vhead"><div><p class="eyebrow">{e(eyebrow)}</p>'
            f'<h1 class="display" id="{view}-h1" tabindex="-1">{e(h1)}</h1><div class="deck">{copy_html(deck)}</div>{extra}</div>{lk}</header>')


HOW_SHORT = [
    'The black label names the kind of evidence. A Finding is something measured; an Estimate depends on stated assumptions.',
    'The title is the answer in one sentence. "Would" or "may" in a title marks a less certain claim.',
    'The gray line under the title says what was counted, in what unit, where and when.',
    'The dark mark is what the title is about; gray marks are there to compare.',
    'Notes in and under the chart explain anything drawn in an unusual way, such as a line that breaks.',
    'The source line says who collected the numbers. Open the table under any chart to see every value.',
]


def how_short(view):
    li = ''.join(f'<li>{e(x)}</li>' for x in HOW_SHORT)
    return (f'<details class="howto" open><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> how to read our charts, in short</span></summary>'
            f'<ol>{li}</ol><p><a href="#system/read">The full guide on the system sheet</a></p></details>')


def index_nav(view):
    li = ''.join(f'<li><a href="#{view}/{s.lower()}"><b>{s}</b> {e(SPECS[s]["form"])}</a></li>' for s in ORDER)
    return (f'<details class="index" open><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> the ten charts</span></summary>'
            f'<nav aria-label="The ten charts on this view"><ol>{li}</ol></nav></details>')


DECK_WHITE = ('<p>Explainer leads with the finding. Each chart opens with the kind of evidence and a sentence that says what the '
              'data shows, and notes in the drawing teach what a reader could otherwise miss.</p>'
              '<p class="wideonly">Charts sit in one reading column, the way an explainer runs, and four break wider where the data '
              'needs room. The scenario chart is a table, because a reader looks it up. No chart on these views takes the working red; '
              'the system sheet shows how red behaves.</p>')


def view_white():
    body = ''.join(specimen('white', s) for s in ORDER)
    return (f'<section class="view" data-view-root="white" data-ground="white" aria-labelledby="white-h1"><div class="wrap">'
            f'{view_head("white", "Chart system 01 · A concept for Board 3", "Explainer", DECK_WHITE)}{how_short("white")}'
            f'{index_nav("white")}{body}</div></section>')


def view_newsprint():
    deck = ('<p>The same ten charts from the same generators, with the ground changed.</p>'
            '<p class="wideonly">Gridlines take Stone mixed 70 percent toward Newsprint, secondary text stays in Deep Stone, which measures '
            f'{contrast(DEEP, NEWS):.2f}:1 here where Stone measures {contrast(STONE, NEWS):.2f}:1, and text on a dark bar turns White. '
            f'Pillar Red measures {contrast(RED, NEWS):.2f}:1 on Newsprint, under the 3:1 a mark needs, so a red point here takes a '
            '1 px Charcoal keyline, as the system sheet shows.</p>')
    body = ''.join(specimen('newsprint', s) for s in ORDER)
    return (f'<section class="view" data-view-root="newsprint" data-ground="news" aria-labelledby="newsprint-h1" hidden><div class="wrap">'
            f'{view_head("newsprint", "Chart system 01 · Explainer", "On Newsprint", deck)}{how_short("newsprint")}'
            f'{index_nav("newsprint")}{body}</div></section>')


def view_dark():
    t = GROUNDS['dark']
    made = {'ink': 'Newsprint', 'red': 'Pillar Red'}
    rowsx = ''.join(f'<tr><th scope="row"><span class="swx" style="background:{t[k]}"'
                    f'{" data-red=&quot;specimen&quot; data-red-job=&quot;palette swatch&quot;".replace("&quot;", chr(34)) if k == "red" else ""}></span>{e(ROLE_WORDS[k])}</th>'
                    f'<td>{t[k]}</td><td>{e(ROLE_MIX["dark"].get(k, made.get(k, "")))}</td>'
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
    """Copy one Art into another at an offset, keeping its label boxes and lines for the guard."""
    dst.out.append(f'<g transform="translate({f(dx)} {f(dy)})">' + ''.join(src.out) + '</g>')
    dst.defs += src.defs
    for (x0, y0, x1, y1, s, h) in src.boxes:
        dst.boxes.append((x0 + dx, y0 + dy, x1 + dx, y1 + dy, s, h))
    for (a1, b1, a2, b2, k) in src.segs:
        dst.segs.append((a1 + dx, b1 + dy, a2 + dx, b2 + dy, k))
    dst.strings += src.strings


def balanced(text, width, size, weight, tight=False):
    """Break a display line into the fewest lines that fit, with the widths as even as possible (no widow)."""
    words = copy(text).split(' ')
    best = None
    for n in range(1, 6):
        for cuts in itertools.combinations(range(1, len(words)), n - 1):
            parts = [' '.join(words[i:j]) for i, j in zip((0,) + cuts, cuts + (len(words),))]
            ws = [tw(p, size, weight, tight) for p in parts]
            if max(ws) * TK['guard']['headroom'] > width:
                continue
            score = max(ws) - min(ws)
            if best is None or score < best[0]:
                best = (score, parts)
        if best:
            return best[1]
    raise AssertionError('title does not fit')


def social_card():
    """S01 as a 1080 by 1350 portrait card: the same generator at 1.25 times the type, with the card's own frame."""
    W, H, P = 1080, 1350, 72
    c = Art(W, 'social-card')
    c.rect(0, 0, W, H, 'f-g')
    wm = wordmark(40, '20261028_Wordmark-Display-Master.svg', 'cwm')
    c.out.append(f'<g data-red="signature" transform="translate({P} {P})">{wm.replace("<svg ", "<svg x=\"0\" y=\"0\" ", 1)}</g>')
    y = P + 40 + 50
    ev = DS['stock-trading-ban']['evidence']
    ew = tw(ev.upper(), 20, 700, track=0.06) + 24
    c.rect(P, y - 26, ew, 36, 'f-ink')
    c.text(P + 12, y, ev, 20, 'ti cap', 700, track=0.06, attrs=' data-role="evidence-label"', on_mark=True, box=False)
    c.text(P + ew + 16, y, GRADE_LINE['S01'], 22, 'tn', 400)
    y += 76
    title = 'Nearly nine in ten Republican and Democratic voters favored a ban on stock trading by members of Congress.'
    y = c.block(P, y, balanced(title, W - 2 * P, 54, 800, tight=True), 54, 'tb', 800, 59, tight=True, attrs=' data-role="title"') + 44
    c.out.append('<g data-role="measure">')
    y = c.para(P, y, 'Registered voters who favor a ban, by party, in a May 2023 survey; then the 2026 votes in Congress, three years later',
               W - 2 * P, 24, 'tn', 400, 33)
    c.out.append('</g>')
    y += 32
    chart, ch = gen_s01(W - 2 * P, 'social-s01', t=Type(W - 2 * P, scale=1.25), compact=True)
    place(c, chart, P, y)
    y += ch + 16
    src = ('Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, May 19 to 30, 2023, '
           'United States; U.S. House, Roll Call 280, July 22, 2026; U.S. Senate, Vote 253, September 30, 2026; '
           'as recorded in Oath\u00a0&\u00a0Action, Who Do They Answer To? Systems Atlas V7, snapshot of October 15, 2026.')
    n_src = len(wrap(src, (W - 2 * P) / TK['guard']['headroom'], 20, 400))
    ys = H - P - (n_src - 1) * 28
    assert ys - 40 > y, f'social card runs to {y}'
    c.line(P, ys - 36, W - P, ys - 36, 's-grid')
    c.out.append('<g data-role="source">')
    c.para(P, ys, src, W - 2 * P, 20, 'tn', 400, 28)
    c.out.append('</g>')
    alt = ('Social card, 1080 by 1350 pixels, from Oath & Action: ' + title + ' 86 percent of registered voters favored a ban; '
           '88 percent of Democrats and 87 percent of Republicans. The House passed a ban, H.R. 7008, 232 to 198; the Senate vote to take '
           'it up was 53 to 47, 7 votes short of the 60 needed.')
    return c.render(H, alt + ' ' + src, 'card', 'social-card-1080'), src


def view_social():
    svg, src = social_card()
    R = rows('stock-trading-ban')
    table = table_html('Support for a ban and the votes that followed', ['Group', 'Measure', 'Value'],
                       [[r['group'], r['measure'], str(r['value'])] for r in R], (2,))
    fig = (f'<figure class="cardfig" data-spec="S01" data-dataset="stock-trading-ban" data-evidence="Finding">'
           f'<div class="cardbox" data-ground="news" role="region" tabindex="0" aria-label="Social card at true size, 1080 by 1350 pixels; scroll sideways on a phone">{svg}</div>'
           f'<details class="eq" data-role="equivalent"><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> the table and notes'
           f'<span class="vh2"> for the social card</span></span></summary><div class="eqb">'
           f'<ul class="eqn"><li>{e("Survey of 2,625 registered voters, May 19 to 30, 2023, three years before either vote.")}</li>'
           f'<li>{e("Taking up the bill needed 60 votes, three-fifths of the Senate, to end debate (cloture).")}</li></ul>{table}<p class="src">{e(src)}</p></div></details></figure>')
    deck = ('<p>One chart as a portrait post at 1080 by 1350 pixels, the size Instagram and LinkedIn use. It is chart S01 from the '
            "same generator, with type at one and a quarter times its page size so labels hold at a phone's feed width. The card "
            'keeps the evidence label, the title, the measure line, the full source and the wordmark, so it still makes sense when '
            'it travels without the page. It names Oath & Action and the atlas and carries no web address until the site is settled. '
            'It sits on Newsprint, the ground a feed of white cards does not use.</p>')
    strip_html = ('<div class="strip"><p class="stag">Studio note, not part of the card</p><h2 class="sid">S01 '
                  '<span>Social card, 1080 by 1350</span></h2><dl><dt>Reader question</dt><dd>Do Republicans and Democrats agree on anything about Congress?</dd>'
                  '<dt>Why this chart</dt><dd>A shared view that both parties hold is the finding most likely to travel, and it takes no side.</dd></dl></div>')
    return (f'<section class="view" data-view-root="social" data-ground="white" aria-labelledby="social-h1" hidden><div class="wrap">'
            f'{view_head("social", "Chart system 01 · Explainer", "Social card", deck)}'
            f'<section class="spec cardspec" aria-label="The social card">{fig}{strip_html}</section></div></section>')


# ------------------------------------------------------------------------------------------------ system sheet
def sys_art(gen, widths, label, name, **kw):
    out = []
    for W, cls in widths:
        a, H = gen(W, f'system-{name}-{W}', **kw)
        out.append(a.render(H, label, f'ab {cls}', f'{name}-system-{W}'))
    return ''.join(out)


def all_widths(wide):
    return [(wide, 'ab-w')] + [(TK['artboard'][k], c) for k, c in ARTBOARDS[1:]]


def anatomy_art(W, uid):
    a, H = gen_s02(W, uid, anatomy=True)
    for n in range(4, 13):
        cx, cy = a.anchors[f'm{n}']
        a.circle(cx, cy, 10.5 if n < 10 else 12, 'f-mk')
        a.text(cx, cy + 4.6, str(n), 13, 'ti', 700, 'middle', on_mark=True, box=False)
    return a, H


ANATOMY = [
    ('Evidence label', 'The kind of evidence in a dark chip: Finding, Association, Estimate or Illustration. The grade follows in words.'),
    ('Title', 'One sentence that states the finding, in Inter Tight 800. Its verb matches the grade: record words for documented, "can" or "may" for plausible, "would" for a scenario.'),
    ('Measure line', 'The measure, unit, place and period, in Inter 400 Deep Stone. It says when a scale is cropped and what each measure counts.'),
    ('Unit on the top tick', 'The unit appears once, on the top tick or the first label. Other ticks stay bare.'),
    ('Gridlines', 'Horizontal 1 px hairlines in the grid tint. No vertical grid and no tick marks. A gridline passes behind a label, never through it.'),
    ('Baseline', 'A 1.5 px Charcoal line at zero. Bars always start here.'),
    ('Subject', 'The series the title names: 3 px Charcoal, labeled directly in Inter 600.'),
    ('Context', 'Other series in 2 px Stone, labeled in Deep Stone. They recede so the subject reads first.'),
    ('Point label', 'The value the title names, printed beside its point in Inter 600.'),
    ('Note and leader', 'Notes sit in open space in Inter 14 px Deep Stone, 45 to 75 characters a line, joined to the data by a 1 px leader at least 12 px long, with one bend at most.'),
    ('Odd encoding, explained once', 'Here the steps at 2013, 2017 and 2019 are method breaks. The line never bridges them.'),
    ('End note', 'A note in open space names the value a reader would look for, and the event that bears on it.'),
    ('Source line, guide link and credit', 'Publisher, table, period, geography, date retrieved and the qualification, in that order. "How to read our charts" and the credit sit at right.'),
    ('Table and notes', 'One click opens every value and every note; the toggle names the chart and shows whether it is open.'),
]


def type_ramp():
    T = TK['type']
    rows_ = [
        ('View title', '<span class="display" style="display:block">Explainer</span>', 'Inter Tight 800, 56/60, −0.035em; 36/40 on phones'),
        ('Chart title', '<span class="ct" style="display:block">A sentence that states the finding.</span>', f'Inter Tight 800, {T["title"][0]}/{T["title"][1]}, −0.02em; {T["title_phone"][0]}/{T["title_phone"][1]} on phones'),
        ('Evidence label', '<span class="ev">Finding</span>', 'Inter 700, 13/18, capitals, 0.06em; dark chip'),
        ('Measure line', '<span class="ms" style="margin:0">Percent, United States, 2009 to 2025</span>', f'Inter 400, {T["measure"][0]}/{T["measure"][1]}, Deep Stone; 15/22 on phones'),
        ('Big number', '<span class="bigx">86%</span>', f'Inter Tight 800, {T["big"]} px; {T["big_phone"]} px on phones; set 0.045 em left so its ink aligns'),
        ('Direct label', '<span class="lblx">Supplemental measure</span>', f'Inter 600, {T["label"]} px; {T["phone_min"]} px in dense rows and on phones'),
        ('Key label', '<span class="ntx" style="color:inherit">Toward voters</span>', f'Inter 400, {T["note"]} px, beside a {TK["unit"]["size"]} px swatch drawn in the chart\'s own mark'),
        ('Tick label', '<span class="tkx">25%  20  15</span>', f'Inter 400, {T["tick"]} px, Deep Stone, tabular figures; {T["phone_min"]} px on phones'),
        ('Note', '<span class="ntx">2021: the expanded credit was in force.</span>', f'Inter 400, {T["note"]}/{T["note_leading"]}, Deep Stone; note heads Inter 600'),
        ('Tile code', '<span class="tkx" style="color:inherit;font-weight:600">MA</span>', f'Inter 600, {T["note"]} px, with the year in Inter 400, {T["tick"]} px; on phones the code alone at {T["tile_code_phone"]} px, the one drawing text under {T["phone_min"]} px there'),
        ('Source line', '<span class="src">Source: U.S. Census Bureau, P60-290, Table 8.</span>', 'Inter 400, 13/18, Deep Stone'),
        ('Quotation', '<span class="q">“Clarity is our duty. Action is our promise.”</span>', 'Lora Italic, quoted words only, never a title'),
    ]
    body = ''.join(f'<tr><th scope="row">{e(n)}</th><td>{s}</td><td>{e(spec)}</td></tr>' for n, s, spec in rows_)
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Type ramp, table"><table class="eqt ramp"><caption>Type ramp</caption>'
            f'<thead><tr><th scope="col">Role</th><th scope="col">Sample</th><th scope="col">Specification</th></tr></thead><tbody>{body}</tbody></table></div>')


def marks_art(W, uid):
    """The mark specifications, drawn by the same kit from CHART_TOKENS: a sample at left, its rule at right."""
    a = Art(W, uid)
    narrow = W < 600
    SW = 120 if not narrow else 84
    TX = SW + 16
    y = [18]
    L, B, U, Dt = TK['line'], TK['bar'], TK['unit'], TK['dot']

    def head(txt):
        a.text(0, y[0], txt, 13, 'te', 700, track=0.06)
        y[0] += 34

    def row_(draw, txt):
        draw(y[0])
        y[0] = a.para(TX, y[0], txt, W - TX, 14, 'tr', 400) + 30
    head('LINE FAMILY')
    for wv, name, cls in ((L['hairline'], f'Gridline and leader, {L["hairline"]} px', 'sp-ink'), (L['baseline'], f'Baseline and reference, {L["baseline"]} px', 'sp-ink'),
                          (L['context'], f'Context series, {L["context"]} px Stone', 'sp-ctx'), (L['subject'], f'Subject series, {L["subject"]} px Charcoal', 'sp-ink'),
                          (L['selected'], f'Selected on an interactive chart, {L["selected"]} px', 'sp-ink')):
        row_(lambda b, wv=wv, cls=cls: a.raw(f'<line x1="0" y1="{f(b - 5)}" x2="{SW}" y2="{f(b - 5)}" class="{cls}" style="stroke-width:{wv}px"/>'), name)
    y[0] += 10
    head('DOTS, BARS AND UNITS')

    def dots(b):
        a.circle(8, b - 5, Dt['subject_r'], 'f-ink')
        a.circle(32, b - 5, Dt['open_r'], 's-ring2')
        a.circle(54, b - 5, Dt['vertex_r'], 'f-ink')
        a.circle(70, b - 5, Dt['small_vertex_r'], 'f-ink')
    row_(dots, f'Dots: {2 * Dt["subject_r"]:g} px for a subject value, {2 * Dt["open_r"]:g} px open for the earlier value, '
               f'{2 * Dt["vertex_r"]:g} px for a line vertex, {2 * Dt["small_vertex_r"]:g} px in small multiples')
    row_(lambda b: a.rect(0, b - 17, SW, B['height'], 'f-ink'),
         f'Bars: {B["height"]} px on a {B["pitch"]} px pitch; {B["dense_height"]} px on {B["dense_pitch"]} past ten rows; '
         f'{B["phone_height"]} px on phones; segments meet with no gap')

    def units(b):
        a.rect(0, b - 14, U['size'], U['size'], 'f-ink')
        a.rect(U['size'] + U['gap'] + 1, b - 13, U['size'] - 2, U['size'] - 2, 's-ink2 f-g')
        a.rect(2 * (U['size'] + U['gap']), b - 14, U['size'], U['size'], 'f-ctx')
    row_(units, f'Units: {U["size"]} px squares, {U["gap"]} px apart, one per record; solid and open squares differ by fill as well as position')

    def hatch(b):
        a.rect(0, b - 15, SW, 18, 'hatchf', f' style="fill:{a.hatch()}"')
        a.rect(0.75, b - 14.25, SW - 1.5, 16.5, 's-ctx15h nofill')
    row_(hatch, f'Hatch: {TK["hatch"]["weight"]} px Stone at 45 degrees on a {TK["hatch"]["pitch"]} px pitch, for contested claims')

    def dotted(b):
        a.rect(0.75, b - 14.25, SW - 1.5, 16.5, 's-dot')
    row_(dotted, 'Dotted outline: hypothesis, the untested grade, after the atlas\'s dotted line')

    def ring(b):
        a.rect(2.5, b - 14, 14, 14, 'f-ink')
        a.rect(0, b - 16.5, 19, 19, 's-ring')
    row_(ring, 'Ring: 1 px, 2.5 px outside a unit, for the one entry that stands for many')

    def brk(b):
        a.circle(8, b - 16, 3, 'f-ink')
        a.circle(8, b - 4, 3, 'f-ink')
    row_(brk, 'Break: two estimates at one date, never joined by a line')
    return a, y[0] - 30 + 12


def swatch_table(name):
    t = GROUNDS[name]
    g = t['g']
    keys = ['ink', 'sec', 'ctx', 'lt', 'lt2', 'grid', 'band', 'vup', 'vup2', 'sdn2', 'sdn', 'red']
    base_mix = {'ink': 'Charcoal' if name != 'dark' else 'Newsprint', 'sec': 'Deep Stone' if name != 'dark' else 'Dim Newsprint',
                'ctx': 'Stone', 'red': 'Pillar Red'}
    use_words = {'lt': 'fill, values printed', 'lt2': 'track behind a printed share', 'grid': 'hairline; values printed',
                 'band': 'background tint behind a note', 'vup': 'cell tint, words printed', 'vup2': 'cell tint, words printed',
                 'sdn': 'cell tint, words printed', 'sdn2': 'cell tint, words printed'}
    out = []
    for k in keys:
        hexv = t[k]
        cr = contrast(hexv, g)
        if k in ('ink', 'sec'):
            use = 'text' if cr >= 4.5 else 'fails text'
        elif k in ('ctx', 'red'):
            use = 'mark' if cr >= 3 else 'mark with keyline'
        else:
            use = use_words[k]
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
    out = []
    for s in LAB['sets']:
        if s['kind'] not in ('sequential', 'diverging') or s['ground'] not in ('white', 'newsprint'):
            continue
        cells = ''.join(f'<li><span class="swx big" style="background:{w["hex"]}"></span><span>{e(w["label"])}</span>'
                        f'<span class="mono">{w["hex"]} · {w["contrast_on_ground"]:.2f}:1</span></li>' for w in s['swatches'])
        out.append(f'<div class="ramp"><p class="kh">{e(s["name"])}, on {e(s["ground"].capitalize())}. Neighbors at least '
                   f'{s["min_lightness_step"]:.3f} apart in OKLab lightness; grayscale order {"kept" if s["grayscale_monotonic"] else "not kept, so labels carry it"}.</p><ul>{cells}</ul></div>')
    return ''.join(out)


def grade_sheet():
    def sw(kind):
        a = Art(40, f'grade-{kind}')
        swatch(a, 1, 3, kind, 18)
        return a.render(24, '', 'gsw', f'grade-swatch-{kind}').replace('role="img" aria-label=""', 'aria-hidden="true"')
    body = ''.join(f'<tr><th scope="row">{sw(g["mark"])}{e(g["word"])}</th><td>{e(g["meaning"])}</td><td>{e(g["verbs"])}</td></tr>' for g in GRADE_TABLE)
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Evidence grades, table"><table class="eqt"><caption>One grade table for every chart</caption>'
            f'<thead><tr><th scope="col">Grade</th><th scope="col">Means</th><th scope="col">Title verbs</th></tr></thead><tbody>{body}</tbody></table></div>')


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
    widths = [(TK['artboard'][k], c) for k, c in ARTBOARDS[1:]]
    a1 = sys_art(gen_s01, widths, 'Demonstration A: the Senate shortfall of 7 votes marked in Pillar Red, the one point a title on the shortfall names.', 'reda', red='specimen')
    a2 = sys_art(gen_s01, widths, 'Demonstration B: the same chart with the shortfall in the darkest ink, because an ask holds the red.', 'redb', red='stepdown')
    return ('<div class="demo"><div class="dpanel"><p class="dlab">Demonstration A, a specimen</p>'
            '<p class="dt">Title for this demonstration: The Senate vote to take up the ban fell 7 votes short of the 60 needed.</p>'
            f'<div class="art w600">{a1}</div><p class="dcap">With nothing else in the view asking for red, the shortfall the title names takes it. Red marks the one point the title names.</p></div>'
            '<div class="dpanel"><p class="dlab">Demonstration B, a specimen: an ask takes the red</p>'
            '<p class="dt">Same title. The view now holds a step the reader can take.</p>'
            f'<div class="art w600">{a2}</div><p class="dcap"><span class="askbtn" data-red="specimen" data-red-job="the step a reader can take now">'
            'See how your senators voted</span> <span class="illus">Illustrative ask</span></p><p class="dcap">The step a reader can take now outranks the point the title names, '
            'so the ask keeps the red and the shortfall steps down to the darkest ink.</p></div></div>')


HOW_TO_READ = [
    ('Start with the label.', 'The black chip says what kind of evidence the chart shows. A Finding is something measured, with a source and a period. '
     'An Association links two things without showing that one caused the other. An Estimate says what would happen if stated assumptions hold. '
     'An Illustration shows how a chart works, with made-up numbers, and says so beside the chart.'),
    ('Read the title as the answer.', 'It is one sentence that says what the numbers show, and its verb tells you how sure it is. Record words such as '
     '"passed" and "fell" mean the facts are on the public record. "Raises" or "lowers" means strong research evidence. "Can" or "may" means '
     'some evidence. "Would" means an estimate that depends on assumptions. "Untested" means nobody has tested it yet. When the evidence is '
     'disputed, the title gives both readings.'),
    ('Check what was counted.', 'The gray line under the title names what was measured, in what unit, where and when, and says when the scale does not start at zero.'),
    ('Look for the dark mark.', 'The dark line, bar or dot is what the title is about. Gray marks are there for comparison. A chart that shows evidence grades uses shade for the grade instead, and says so.'),
    ('Read the notes in and under the chart.', 'Short notes point at the record, the turning point or anything drawn in an unusual way, such as a line that breaks where a survey changed.'),
    ('Allow for survey error.', 'Survey numbers come from a sample of people, so each has a margin of error. A margin of 0.5 points means the true figure most likely sits within half a point either way, and a smaller change may be chance.'),
    ('Red marks one thing.', 'When a chart uses red, it marks the single point the title names, or the step you can take now. Red never stands for a party, a side, or good or bad.'),
    ('Find where the numbers came from.', 'The source line names who collected the data, when, and what to keep in mind. Open the table under any chart to see every value and every note.'),
]

KIT_API = [
    ('gen_s01(W, uid, t=None, compact=False, red=None)', 'Big number, party bars and two votes. compact drops notes for a card; red marks the Senate shortfall for the red demonstration.'),
    ('gen_s02(W, uid, t=None, anatomy=False)', 'Line with event notes and method breaks, from rows with year, percent and comparable_with.'),
    ('gen_s03(W, uid, t=None)', 'Ranked bar split by a category code; short labels at the bars are chosen from the data.'),
    ('gen_s04(W, uid, t=None)', 'Dumbbell for two years per group; the scale and the words for a small change come from the data.'),
    ('gen_s05(W, uid, t=None)', 'Small multiples on one scale, one panel per group, breaks where the method changed.'),
    ('gen_s06_table(view)', 'Comparison table with the source words in every cell and a boxed glyph for the reading.'),
    ('gen_s07(W, uid, t=None)', 'Tile map from the shared tile grid, one square per state.'),
    ('gen_s08(W, uid, t=None)', 'Unit chart: one square per record, by year column, with per-year counts and a roll-up mark.'),
    ('gen_s09(W, uid, t=None)', 'Timeline on a true time scale with lanes; labels stack so no leader crosses a label.'),
    ('gen_s10(W, uid, t=None)', 'One 100 percent bar per row from the grade table, with the count beside each share.'),
    ('figure(view, spec) and specimen(view, sid)', 'The frame, built from one spec object: evidence label, title, measure, drawing, notes, disclosure, source with the guide link, and the table toggle. A new chart passes its dataset, evidence kind, grade line and source in the spec; S01 to S10 look theirs up by ID.'),
    ('copy(s), source_text(dataset) and nw(n)', 'The copy pipeline: curly quotes and apostrophes, dates in words with no break inside, the true minus, record codes kept off source lines, and numbers in words to 99 (it stops the build beyond that).'),
    ('Art(W, uid) with text(), para(), line(), path(), leader() and render()', 'The drawing: render() refuses a label that collides, leaves the drawing or is crossed by a line.'),
]


def view_system():
    anat = sys_art(anatomy_art, all_widths(TK['artboard']['reading']), 'Anatomy of a chart: chart S02 with its parts numbered 4 to 12; the list beside names each part.', 'anatomy')
    low = min((r for r in rows('child-poverty-spm') if r['measure'] == 'spm'), key=lambda r: r['percent'])
    anat_fig = ('<div class="anat"><div class="anfig" data-ground="white">'
                '<div class="evrow"><span class="mk">1</span><p class="ev">Finding</p><p class="grade">Official statistic: a Census Bureau survey</p></div>'
                f'<p class="ct"><span class="mk">2</span>Child poverty fell to {low["percent"]} percent in {low["year"]}, the lowest since the series began in 2009, and more than doubled the next year.</p>'
                f'<p class="ms"><span class="mk">3</span>{e("Children under 18 below the Supplemental Poverty Measure, which counts tax credits and other aid, percent, United States, 2009 to 2025; the official measure, which counts pretax cash income only, in gray.")}</p>'
                f'<div class="art w720">{anat}</div>'
                f'<div class="srcrow"><p class="src"><span class="mk">13</span><span class="sl">Source:</span> {e(source_text("child-poverty-spm"))}</p><p class="src credit">How to read our charts · Chart: Oath &amp; Action</p></div>'
                '<p class="fakesum"><span class="mk">14</span>+ Show the table and notes</p></div>'
                '<ol class="parts">' + ''.join(f'<li><b>{e(n)}.</b> {e(d)}</li>' for n, d in ANATOMY) + '</ol></div>')
    marks = sys_art(marks_art, all_widths(TK['artboard']['reading']), 'Mark specifications: line weights, dots, bars, units, hatch, dotted outline, ring and break.', 'marks')
    rules_notes = ''.join(f'<li>{e(x)}</li>' for x in [
        'Name the record, give a reader\'s scale, or explain an unusual encoding once. A note that does none of these comes out.',
        'Put a short note in open space near its data and join it with a 1 px Stone leader, at least 12 px long, with one bend at most. Leaders and rules never cross a label; a gridline passes behind one.',
        'Keep notes in the drawing short. Longer notes, the coding rules and any disclosure sit in HTML under the drawing, 45 to 75 characters a line, where they wrap.',
        'State the qualification where it changes the reading: self-reported rates, method breaks, a survey older than the votes, the one entry that stands for many.',
        'A note may say what a measure did over time. It never says a policy caused it unless the source grades that cause.',
        'Label series at the line or the bar. Use a key only when labels cannot fit, and draw the key in the chart\'s own marks.',
        'Read every title twice before it ships, once as a reader on the left and once as a reader on the right. If either would take it as a side, rewrite it.'])
    rules_src = ''.join(f'<li>{e(x)}</li>' for x in [
        'Order: publisher, title or table, observation period, geography, date retrieved, qualification (Master Brief section 15).',
        'Start from the dataset\'s source line. Shorten only by dropping words, never facts. Dates read as words and never break across a line.',
        'Inter 400, 13/18, Deep Stone, under a grid-tint hairline, with "How to read our charts" and "Chart: Oath & Action" at the right.',
        'A compiled list says so in the line, as the ranked-choice map does for Ballotpedia.',
        'Charts on nomination, ranked-ballot or election-rule data print the editor\'s disclosure word for word, labeled "Disclosure:", with the chart.',
        'The table under every chart repeats the source, so the equivalent stands on its own.'])
    read = ''.join(f'<li><b>{e(h)}</b> {e(d)}</li>' for h, d in HOW_TO_READ)
    api = ''.join(f'<tr><th scope="row"><code>{e(n)}</code></th><td>{e(d)}</td></tr>' for n, d in KIT_API)
    tok = html.escape(json.dumps(CHART_TOKENS, indent=1))
    deck = ('<p>Everything a builder needs to make the next chart in this system, and a guide for the people who read them. '
            'Every drawing on this sheet comes from the same generators as the ten charts, and every size comes from one token set.</p>')
    return (f'<section class="view" data-view-root="system" data-ground="white" aria-labelledby="system-h1" hidden><div class="wrap">'
            f'{view_head("system", "Chart system 01 · Explainer", "The system on one sheet", deck)}'
            f'<section class="ssec" id="system-read" aria-labelledby="sys-read"><h2 class="headline" id="sys-read">How to read our charts</h2>'
            f'<p class="lede">For readers, in plain words. This guide can run under any chart or on a help page; every chart links here.</p><ol class="read">{read}</ol></section>'
            f'<section class="ssec" aria-labelledby="sys-anat"><h2 class="headline" id="sys-anat">Anatomy of a chart</h2>'
            f'<p class="lede">Chart S02 with every part numbered.</p>{anat_fig}</section>'
            f'<section class="ssec" aria-labelledby="sys-grade"><h2 class="headline" id="sys-grade">Evidence grades</h2>'
            f'<p class="lede">One table sets each grade’s words, mark and title verbs for every chart that draws grades. Grades never take red, and a chart that shades by grade says so in its key.</p>{grade_sheet()}</section>'
            f'<section class="ssec" aria-labelledby="sys-type"><h2 class="headline" id="sys-type">Type</h2>'
            f'<p class="lede">The locked faces only. Inter Tight sets titles and big numbers, Inter sets every label and number, and Lora Italic appears only for quoted words. Figures take tabular widths; words never do, so a hyphen keeps its width. Nothing on screen goes under 13 px.</p>{type_ramp()}</section>'
            f'<section class="ssec" aria-labelledby="sys-marks"><h2 class="headline" id="sys-marks">Marks</h2>'
            f'<p class="lede">Line weights follow the studio’s family of 1, 1.5, 2, 3 and 6 px (D2-60). Each drawing comes at 1,024 or 720, 600, 358 and 328 px and shows at its natural size, so no weight scales up.</p><div class="art w720">{marks}</div></section>'
            f'<section class="ssec" aria-labelledby="sys-color"><h2 class="headline" id="sys-color">Color, measured on each ground</h2>'
            f'<p class="lede">Every chart color is a role, and every tint is an OKLab mix of locked colors with one job. Contrast is measured against the ground (WCAG 2.x). '
            f'Text needs 4.5:1; a mark needs 3:1; a fill under 3:1 is used only where every value is printed or the table carries it, which is a design judgment. '
            f'Categories never rest on Verdigris against Stone alone: they sit {abs(oklab(VERD)[0] - oklab(STONE)[0]):.2f} apart in OKLab lightness, so position, fill or a label carries them too. '
            'In forced colors, tints drop away and the glyph or label carries the meaning.</p>'
            f'<div class="pals">{swatch_table("white")}{swatch_table("news")}{swatch_table("dark")}</div>'
            f'<h3 class="sub">Ramps from the palette lab</h3><p class="lede">The scenario table (S06) uses diverging A, read as Stone for down and Verdigris for up, with a boxed arrow in every cell. Diverging B is the two-sided alternative for Board 3. Neither pairs red with blue.</p>{lab_ramps()}</section>'
            f'<section class="ssec" aria-labelledby="sys-notes"><h2 class="headline" id="sys-notes">Notes and source lines</h2>'
            f'<div class="two"><div><h3 class="sub">Notes</h3><ul class="rl">{rules_notes}</ul></div>'
            f'<div><h3 class="sub">Source lines</h3><ul class="rl">{rules_src}</ul></div></div></section>'
            f'<section class="ssec" aria-labelledby="sys-red"><h2 class="headline" id="sys-red">Red, once</h2>'
            f'<p class="lede">Rule 05.3, as Dustin approved it (D2-01):</p><blockquote class="q rule">{e(RULE_053)}</blockquote>'
            '<p class="lede">On a chart page each chart counts as one view. A chart posted alone may mark the point its title names in red; a chart added to a page takes red only when the page’s red job moves to it. '
            'The ten charts in this concept take no working red: the one candidate, the 2021 low in S02, sits on a year most readers tie to one policy, so the demonstrations use the Senate shortfall in S01. Party marks, grades, scales and categories never take red.</p>'
            f'{red_demo()}</section>'
            f'<section class="ssec" aria-labelledby="sys-kit"><h2 class="headline" id="sys-kit">The chart kit</h2>'
            f'<p class="lede">The generators in build_concept.py, the seed of the kit (DR-49). Each takes a width and data from the shared dataset and returns a drawing that has passed the label guard. No chart here moves; an animated chart must offer a still version for readers who ask for reduced motion.</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="Generators, table"><table class="eqt"><caption>Generators</caption><thead><tr><th scope="col">Call</th><th scope="col">What it draws</th></tr></thead><tbody>{api}</tbody></table></div>'
            f'<details class="eq toks"><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> the chart tokens</span></summary><pre>{tok}</pre></details></section>'
            '</div></section>')


# ------------------------------------------------------------------------------------------------ CSS and JS
def ground_css():
    return '\n'.join(f'[data-ground="{name}"]{{{css_vars(name)}}}' for name in ('white', 'news', 'dark'))


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
.mast{border-bottom:1px solid var(--rule);background:var(--g)}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;color:var(--ink);padding:10px 0}
.wm16{display:none}
.run{margin:0 0 0 48px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.tabs ul{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;min-height:44px;min-width:44px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:var(--ink)}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ink)}
.tabs a:hover{text-decoration:underline}
.view{padding:40px 0 96px}
.vhead{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:24px 64px;align-items:end;padding-bottom:28px;border-bottom:2px solid var(--ink)}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;margin-left:-.04em}
.display:focus{outline:none}
.deck p{margin:16px 0 0;font:400 19px/28px Inter,sans-serif;max-width:40em;text-wrap:pretty}
.deck p+p{font-size:17px;line-height:27px;color:var(--sec)}
.vlinks ul{margin:0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.vlinks li{display:flex;flex-wrap:wrap;align-items:center;gap:0 6px;padding:0;border-bottom:1px solid var(--grid);font:400 15px/22px Inter,sans-serif;color:var(--sec)}
.vlinks a{display:inline-flex;align-items:center;min-height:44px;font-weight:600;color:var(--ink)}
details>summary{list-style:none;cursor:pointer}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"+" / "";display:inline-block;width:18px;font:700 18px/1 Inter,sans-serif}
details[open]>summary::before{content:"\2212" / ""}
.sw-o{display:none}details[open]>summary .sw-o{display:inline}details[open]>summary .sw-c{display:none}
.howto,.index{margin:20px 0 0;border-bottom:1px solid var(--grid)}
.howto>summary,.index>summary{display:flex;align-items:center;min-height:44px;font:600 15px/20px Inter,sans-serif;width:max-content;max-width:100%}
.howto ol{margin:4px 0 8px;padding-left:22px;max-width:46em;font:400 15px/23px Inter,sans-serif;columns:2;column-gap:48px}
.howto li{margin:0 0 6px;break-inside:avoid}
.howto p{margin:0 0 14px;font:600 15px/23px Inter,sans-serif}
.howto a{display:inline-flex;min-height:44px;align-items:center}
.index ol{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0 24px;margin:0 0 8px;padding:0;list-style:none}
.index li{border-bottom:1px solid var(--grid)}
.index a{display:flex;gap:8px;align-items:center;min-height:44px;font:400 15px/20px Inter,sans-serif;text-decoration:none}
.index a b{font:800 15px/20px "Inter Tight",sans-serif}
.index a:hover{text-decoration:underline}
.headline{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;text-wrap:balance}
.lede{margin:12px 0 0;font:400 17px/27px Inter,sans-serif;max-width:46em;text-wrap:pretty}
.sub{margin:28px 0 8px;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.q{font:italic 400 19px/29px Lora,serif}
.spec{display:grid;grid-template-columns:232px minmax(0,1fr);column-gap:56px;margin-top:72px;padding-top:20px;border-top:1px solid var(--ink)}
.spec>.fig,.spec>.cardfig{grid-column:2;grid-row:1}
.spec>.strip{grid-column:1;grid-row:1}
.index+.spec{margin-top:40px}
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
.ct{margin:0;font:800 28px/32px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em;text-wrap:balance;max-width:30em}
.ms{margin:10px 0 0;font:400 17px/27px Inter,sans-serif;color:var(--sec);max-width:42em;text-wrap:pretty}
.art{margin:28px 0 0;container-type:inline-size}
.art .ab{display:none;max-width:none;height:auto}
.art .ab-s{display:block;width:100%;max-width:328px}
@container (min-width:358px){.art .ab-s{display:none}.art .ab-p{display:block}}
@container (min-width:600px){.art .ab-p{display:none}.art .ab-m{display:block}}
@container (min-width:720px){.art.w720 .ab-m{display:none}.art.w720 .ab-w{display:block}}
@container (min-width:1024px){.art.w1024 .ab-m{display:none}.art.w1024 .ab-w{display:block}}
svg.ab{overflow:hidden}
svg text{font-family:Inter,system-ui,sans-serif;font-variant-numeric:proportional-nums;paint-order:stroke;stroke:var(--g);stroke-width:4px;stroke-linejoin:round}
svg .num,svg text .num{font-variant-numeric:tabular-nums}
svg text.nh,svg text.ti,svg text.ti4{stroke:none}
.tl,.th{font-weight:600;fill:var(--ink)}.tr{font-weight:400;fill:var(--ink)}.tk,.tn{font-weight:400;fill:var(--sec)}
.ts{font-weight:600;fill:var(--sec)}.te{font-weight:700;fill:var(--sec);letter-spacing:.06em}
.tb{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;fill:var(--ink);letter-spacing:-.02em}
.ti{font-weight:600;fill:var(--inv)}.ti4{font-weight:400;fill:var(--inv)}.cap{text-transform:uppercase;letter-spacing:.06em}
.f-ink{fill:var(--ink)}.f-ctx{fill:var(--ctx)}.f-lt{fill:var(--lt)}.f-lt2{fill:var(--lt2)}.f-g{fill:var(--g)}.f-band{fill:var(--band)}
.f-mk{fill:var(--ink)}.f-red{fill:var(--red)}.nofill{fill:none}
.s-grid,.s-base,.s-ld,.s-mark,.s-ring,.s-sub,.s-ctx,.s-ctx15,.s-ctx15h,.s-ink2,.s-dash,.s-dot,.s-ring2,.s-gring,.s-redk,.sp-ink,.sp-ctx{vector-effect:non-scaling-stroke}
.s-grid{stroke:var(--grid);stroke-width:1px;fill:none}
.s-base{stroke:var(--ink);stroke-width:1.5px;fill:none}
.s-ld{stroke:var(--ctx);stroke-width:1px;fill:none}
.s-mark{stroke:var(--ink);stroke-width:1.5px;fill:none}
.s-ring{stroke:var(--ink);stroke-width:1px;fill:none}
.s-redk{stroke:var(--red);stroke-width:3px;fill:none}
.s-sub{stroke:var(--ink);stroke-width:3px;fill:none;stroke-linejoin:round;stroke-linecap:round}
.s-ctx{stroke:var(--ctx);stroke-width:2px;fill:none;stroke-linejoin:round;stroke-linecap:round}
.s-ctx15{stroke:var(--ctx);stroke-width:1.5px;fill:none;stroke-linejoin:round}.s-ctx15h{stroke:var(--ctx);stroke-width:1.5px}
.s-ink2{stroke:var(--ink);stroke-width:2px}
.s-dash{stroke:var(--ctx);stroke-width:1.5px;stroke-dasharray:3 2;fill:none}
.s-dot{stroke:var(--ink);stroke-width:1.5px;stroke-dasharray:1.5 2.5;stroke-linecap:round;fill:none}
.s-ring2{stroke:var(--ctx);stroke-width:2px;fill:none}
.s-gring{stroke:var(--g);stroke-width:2px}
.sp-ink{stroke:var(--ink)}.sp-ctx{stroke:var(--ctx)}
.p-bg{fill:var(--g)}.p-ln{stroke:var(--ctx);stroke-width:1.5px}
.tile:hover rect{stroke:var(--ink);stroke-width:2px}
.fnotes{margin:22px 0 0;padding:14px 0 0 18px;border-top:1px solid var(--grid);max-width:38em;font:400 15px/23px Inter,sans-serif;color:var(--ink)}
.fnotes li{margin:0 0 8px;text-wrap:pretty}
.disc{margin:10px 0 0;max-width:38em;padding:8px 0 0 12px;border-left:2px solid var(--ink);font:400 15px/23px Inter,sans-serif;text-wrap:pretty}
.srcrow{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-top:20px;padding-top:10px;border-top:1px solid var(--grid)}
.src{margin:0;font:400 13px/18px Inter,sans-serif;color:var(--sec);text-wrap:pretty}
.src .sl{font-weight:600;color:var(--ink)}
.credit{white-space:nowrap}
.credit a{display:inline-flex;align-items:center;min-height:24px;color:var(--ink);font-weight:600}
.eq{margin-top:6px;border-bottom:1px solid var(--grid)}
.eq>summary{display:flex;align-items:center;min-height:44px;font:600 15px/20px Inter,sans-serif;width:max-content;max-width:100%}
.eqb{padding:4px 0 20px}
.eqh{margin:4px 0 4px;font:600 15px/22px Inter,sans-serif}
.eqn{margin:0 0 16px;padding-left:18px;font:400 15px/22px Inter,sans-serif;max-width:46em}
.eqb>.src{margin-top:12px}
.tw{overflow-x:auto;max-width:100%}
table.eqt{border-collapse:collapse;width:100%;font:400 14px/20px Inter,sans-serif}
table.eqt caption{text-align:left;font:600 15px/22px Inter,sans-serif;padding:0 0 8px}
table.eqt th,table.eqt td{padding:6px 14px 6px 0;border-top:1px solid var(--grid);text-align:left;vertical-align:top}
table.eqt thead th{border-top:1px solid var(--ink);font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
table.eqt tbody th{font-weight:600}
.num{text-align:right!important;font-variant-numeric:tabular-nums}
.why h3{margin:16px 0 4px;font:600 15px/22px Inter,sans-serif}
.why p,.why li{font:400 14px/21px Inter,sans-serif;margin:0 0 4px}
.why ul{margin:0;padding-left:18px}
.art.tbl{margin-top:20px}
.upnote{margin:0 0 12px;font:600 15px/23px Inter,sans-serif}
.cmpkey{margin:0 0 14px}
.kh{margin:0 0 8px;font:600 14px/20px Inter,sans-serif}
.cmpkey ul{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.cmpkey li{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 6px;font:400 14px/20px Inter,sans-serif}
.gl{flex:none;fill:currentColor;color:var(--ink);forced-color-adjust:auto}
table.cmp{border-collapse:separate;border-spacing:3px;width:100%;margin:0 -3px;font:400 15px/21px Inter,sans-serif}
table.cmp thead th{padding:0 10px 6px;text-align:left;vertical-align:bottom;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid var(--ink)}
table.cmp thead th:first-child{padding-left:0}
table.cmp tbody th{display:grid;grid-template-columns:44px minmax(0,1fr);padding:10px 14px 10px 0;text-align:left;vertical-align:top;font:600 15px/21px Inter,sans-serif;border-bottom:1px solid var(--grid)}
table.cmp .sk{font:800 15px/21px "Inter Tight",sans-serif}
table.cmp .sg{display:block;margin-top:4px;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
table.cmp td{padding:9px 10px 11px;vertical-align:top}
table.cmp tbody tr>th{width:auto}
.gw{display:inline-flex;vertical-align:-6px;margin-right:6px}
.c-up{background:var(--vup)}.c-up2{background:var(--vup2)}.c-dn{background:var(--sdn)}.c-dn2{background:var(--sdn2)}
.c-flat,.c-mix,.c-same{background:var(--g);box-shadow:inset 0 0 0 1px var(--grid)}
.tnote{margin:14px 0 0;font:400 15px/23px Inter,sans-serif;max-width:46em}
@container (max-width:760px){
 table.cmp,table.cmp tbody,table.cmp tr,table.cmp td{display:block;width:auto}
 table.cmp tbody th{border:0;padding:0 0 8px}
 table.cmp{margin:0;border-spacing:0}
 table.cmp thead{display:none}
 table.cmp tr{margin:0 0 18px;border-top:2px solid var(--ink);padding-top:8px}
 table.cmp td{margin:0 0 4px}
 table.cmp td::before{content:attr(data-label);display:block;margin-bottom:4px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
}
.cardspec .strip{position:static}
.cardfig{margin:0;max-width:1082px}
.cardbox{overflow:auto;max-width:100%;border:1px solid var(--rule);background:var(--g)}
.cardbox svg{display:block;width:1080px;height:1350px;max-width:none}
.ssec{margin-top:80px;padding-top:16px;border-top:2px solid var(--ink)}
.ssec>.tw,.ssec .pals{margin-top:24px}
.anat{display:grid;grid-template-columns:minmax(0,720px) minmax(0,1fr);gap:48px;margin-top:28px;align-items:start}
.mk{display:inline-flex;align-items:center;justify-content:center;width:21px;height:21px;margin-right:8px;border-radius:50%;background:var(--ink);color:var(--g);font:700 13px/1 Inter,sans-serif;vertical-align:3px;letter-spacing:0}
.ct .mk{vertical-align:6px}
.fakesum{margin:10px 0 0;font:600 15px/20px Inter,sans-serif;display:flex;align-items:center}
.parts{margin:0;padding-left:28px;font:400 15px/22px Inter,sans-serif}
.parts li{margin:0 0 10px}
.ramp,.pal{margin-top:12px}
table.ramp td:nth-child(2){min-width:280px}
.bigx{font:800 48px/50px "Inter Tight",sans-serif;letter-spacing:-.02em}
.lblx{font:600 15px/20px Inter,sans-serif}.tkx{font:400 13px/18px Inter,sans-serif;color:var(--sec);white-space:pre;font-variant-numeric:tabular-nums}
.ntx{font:400 14px/19px Inter,sans-serif;color:var(--sec)}
.pals{display:grid;gap:32px;margin-top:20px}
.swx{display:inline-block;width:18px;height:18px;margin-right:8px;vertical-align:-4px;border:1px solid var(--ctx)}
.swx.big{width:40px;height:28px;margin:0}
.gsw{display:inline-block;vertical-align:-6px;margin-right:6px}
.ramp ul{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin:0 0 20px;padding:0;list-style:none}
.ramp li{display:grid;gap:4px;font:400 14px/20px Inter,sans-serif}
.mono{color:var(--sec);font-size:13px;line-height:18px;font-variant-numeric:tabular-nums}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px}
.rl{margin:0;padding-left:20px;font:400 16px/25px Inter,sans-serif}.rl li{margin-bottom:8px}
blockquote.rule{margin:16px 0 0;padding-left:20px;border-left:3px solid var(--ink);max-width:46em;font-size:18px;line-height:28px}
.demo{display:grid;grid-template-columns:repeat(2,minmax(0,600px));gap:48px;margin-top:28px}
.dlab{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.dt{margin:8px 0 0;font:600 15px/23px Inter,sans-serif}
.dcap{margin:12px 0 0;font:400 15px/23px Inter,sans-serif}
.askbtn{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;background:var(--red);color:#121212;font:700 19px/1 Inter,sans-serif}
.illus{margin-left:10px;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.read{margin:20px 0 0;padding-left:24px;max-width:46em;font:400 17px/27px Inter,sans-serif}
.read li{margin-bottom:10px}
.toks pre{font:400 13px/18px ui-monospace,monospace;white-space:pre-wrap;max-width:100%;overflow:auto}
code{font:400 14px/20px ui-monospace,monospace}
.foot{border-top:1px solid var(--rule);background:var(--g)}
.frow{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:24px;padding-top:16px;padding-bottom:40px}
.foot .right{text-align:right}
@media (forced-colors:active){.c-up,.c-up2,.c-dn,.c-dn2{border:1px solid CanvasText}}
@media (max-width:1199.98px){
 .spec{grid-template-columns:minmax(0,1fr)}
 .spec>.fig,.spec>.cardfig,.spec>.strip{grid-column:1;grid-row:auto}
 .strip{position:static;margin-top:28px;max-width:720px}
 .index ol{grid-template-columns:repeat(2,minmax(0,1fr))}
 .anat,.demo{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:899.98px){
 .wrap{padding:0 16px}
 .mrow{grid-template-columns:1fr;gap:0;padding-top:4px}
 .wm{padding:14px 0}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
 .view{padding-top:24px}
 .vhead{grid-template-columns:minmax(0,1fr);padding-bottom:20px}
 .vlinks,.wideonly{display:none}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline{font-size:30px;line-height:34px}
 .deck p{font-size:17px;line-height:26px;margin-top:10px}
 .ct{font-size:22px;line-height:27px}
 .ms{font-size:15px;line-height:22px}
 .howto ol{columns:1}
 .index ol{grid-template-columns:minmax(0,1fr)}
 .spec{margin-top:48px}
 .index+.spec{margin-top:32px}
 .srcrow{flex-direction:column;gap:4px}
 .credit{white-space:normal}
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
  var NAMES={white:'White',newsprint:'Newsprint',dark:'Charcoal',social:'Social card',system:'System'};
  var last=null;
  function parse(){var p=decodeURIComponent(location.hash.slice(1)).toLowerCase().split('/'); var v=VIEWS.indexOf(p[0])>=0?p[0]:'white'; return {v:v,sub:p[1]||null};}
  function show(){
    var p=parse();
    [].forEach.call(document.querySelectorAll('[data-view-root]'),function(r){r.hidden=r.getAttribute('data-view-root')!==p.v;});
    document.documentElement.setAttribute('data-ground',GROUND[p.v]);
    document.title=NAMES[p.v]+' · Explainer Chart System';
    [].forEach.call(document.querySelectorAll('.tabs a'),function(a){ if(a.getAttribute('href')==='#'+p.v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');});
    if(p.sub){var t=document.getElementById(p.v+'-'+p.sub); if(t){t.scrollIntoView({block:'start'}); var h=t.querySelector('h2'); if(h){h.setAttribute('tabindex','-1'); h.focus({preventScroll:true});}}}
    else if(last!==null&&last!==p.v){window.scrollTo(0,0); var h1=document.getElementById(p.v+'-h1'); if(h1) h1.focus({preventScroll:true});}
    last=p.v;
  }
  addEventListener('hashchange',show);
  var skip=document.querySelector('.skip');
  if(skip) skip.addEventListener('click',function(ev){ev.preventDefault(); var h=document.getElementById(parse().v+'-h1'); if(h){h.focus(); h.scrollIntoView({block:'start'});}});
  if(innerWidth<600){[].forEach.call(document.querySelectorAll('details.howto,details.index'),function(d){d.removeAttribute('open');});}
  show();
})();
"""


def build():
    views = ' '.join(v for v, _ in VIEWS)
    page = ('<!doctype html><html lang="en" data-ground="white"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>White · Explainer Chart System</title>'
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
    text_only = re.sub(r'<(script|style|pre)\b.*?</\1>', '', page, flags=re.S)
    assert '—' not in text_only, 'em dash in page'
    visible = html.unescape(re.sub(r'<[^>]+>', ' ', text_only))
    for m in re.finditer(r'(?:(?<=\s)|(?<=\())-\d', visible):
        raise AssertionError(f'hyphen used as a minus: {visible[m.start() - 20:m.end() + 10]}')
    straight = re.findall(r"\w'\w|\"", re.sub(r'\s+', ' ', visible))
    assert not straight, f'straight quotes in copy: {straight[:5]}'
    assert 'January 2025' not in visible, 'no period split at January 2025 (F2)'
    OUT.write_text(page)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1024:.0f} KB; fonts from {FONTDIR}')


if __name__ == '__main__':
    build()
