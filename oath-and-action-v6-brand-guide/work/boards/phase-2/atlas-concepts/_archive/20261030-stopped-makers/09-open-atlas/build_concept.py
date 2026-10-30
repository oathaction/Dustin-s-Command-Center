"""Atlas concept 09, Open Atlas (October 30, 2026).

The system as a two-page spread: the economy page (area A and the economy layer) on the verso, the democracy page
(areas B to E) on the recto, technology in the fold and the outside drivers in the head margin. Every label, sign,
grade, delay, count and title on the page is read from the model export; counts the page states are asserted here.

Writes 20261030_Concept-09-Open-Atlas.html beside this file. Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/09-open-atlas/build_concept.py

Text widths for wrapping and label placement are measured with the Inter files installed on this machine
(/usr/share/fonts/opentype/inter), which match the Google Fonts Inter the page loads to within 0.1 px. Inter Tight
widths are taken as 0.94 of Inter's, measured against Chromium on October 30.
"""
import html
import importlib.util
import json
import math
import pathlib
import re
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

OUT = HERE / '20261030_Concept-09-Open-Atlas.html'
SHARED = ROOT / 'work/boards/phase-2/atlas-concepts/shared'

M = acc.load_model()
N, L, LP, RF = M['nodes'], M['links'], M['loops'], M['reforms']
G = M['generated']
COUNTS = G['counts']
AREAS = {a['id']: a for a in M['areas']}
AREA_OF = {n: a['id'] for a in M['areas'] for n in a['nodes']}
ORDER = M['order']
LOOP_ORDER = M['loop_order']
GROUPS = M['groups']
P = acc.PALETTE
NP, CH, RED, PR, ST, VG, WH, DS = (P['newsprint'], P['charcoal'], P['pillar_red'], P['prussian'], P['stone'],
                                    P['verdigris'], P['white'], P['deep_stone'])
MINUS = '−'
e = html.escape
assert G['snapshot'] == '2026-10-15'
SNAP = 'October 15, 2026'

# ------------------------------------------------------------------ the spread's two pages and its fold
ECON_AREAS = ('A', 'production', 'household', 'money')
DEM_AREAS = ('B', 'C', 'D', 'E')


def side(n):
    a = AREA_OF[n]
    return 'econ' if a in ECON_AREAS else 'dem' if a in DEM_AREAS else 'fold' if a == 'TC' else 'margin'


CROSS = sorted((l for l in L.values() if {side(l['from']), side(l['to'])} == {'econ', 'dem'}), key=lambda l: l['id'])
CROSS_IDS = {l['id'] for l in CROSS}
TO_DEM = [l for l in CROSS if side(l['to']) == 'dem']
TO_ECON = [l for l in CROSS if side(l['to']) == 'econ']
FOLD_LOOPS = [k for k in LOOP_ORDER if not LP[k]['conceptual']
              and {side(s['code']) for s in LP[k]['stations'] if s['code']} == {'econ', 'dem'}]
WITHIN_ECON = [l for l in L.values() if side(l['from']) == side(l['to']) == 'econ']
WITHIN_DEM = [l for l in L.values() if side(l['from']) == side(l['to']) == 'dem']
TECH = [l for l in L.values() if 'fold' in (side(l['from']), side(l['to']))]
DRIVER = [l for l in L.values() if side(l['from']) == 'margin']
# Area A could sit on either page. With A on the democracy page, this many connections would cross instead.
ALT_CROSS = sum(1 for l in L.values()
                if {('econ' if AREA_OF[x] in ('production', 'household', 'money') else 'dem' if AREA_OF[x] in 'ABCDE'
                     else 'other') for x in (l['from'], l['to'])} == {'econ', 'dem'})
# The pitch's numbers, verified by script
assert len(CROSS) == 12 and len(TO_DEM) == 5 and len(TO_ECON) == 7, (len(CROSS), len(TO_DEM), len(TO_ECON))
assert sum(1 for l in TO_ECON if l['from'] == 'E1') == 4
assert FOLD_LOOPS == ['R1', 'R5', 'R6', 'R15'], FOLD_LOOPS
assert len(WITHIN_ECON) + len(WITHIN_DEM) + len(CROSS) + len(TECH) + len(DRIVER) == COUNTS['connections'] == len(L)
assert ALT_CROSS == 15
assert not [l for l in L.values() if 'C' in (AREA_OF[l['from']], AREA_OF[l['to']]) and 'econ' in (side(l['from']), side(l['to']))]
ECON_VARS = [n for n in ORDER if side(n) == 'econ']
DEM_VARS = [n for n in ORDER if side(n) == 'dem']
assert len(ECON_VARS) == 18 and len(DEM_VARS) == 20
TECH_ECON = sum(1 for l in TECH if 'econ' in (side(l['from']), side(l['to'])))
TECH_DEM = sum(1 for l in TECH if 'dem' in (side(l['from']), side(l['to'])))
TECH_INNER = sum(1 for l in TECH if side(l['from']) == side(l['to']) == 'fold')
TECH_X = sum(1 for l in TECH if side(l['from']) == 'margin')

# The book: the overview is the opening spread, pages 2 and 3; area C turns to pages 4 and 5; loop R10 to 6 and 7;
# the loop index runs on from page 8. Folios are furniture, not model facts.
FOLIO = {'overview': (2, 3), 'area-c': (4, 5), 'loop-r10': (6, 7), 'loops': (8, 9)}


# ------------------------------------------------------------------ words
def gword(g):
    return acc.GRADES[g][0]


def ggloss(g):
    return acc.GRADES[g][1]


def gtex(g):
    return acc.GRADES[g][2]


def dword(d):
    return acc.DELAYS[d]


def schar(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def sname(p):
    return {'+': '+', '-': '-'}.get(p, 'none')


def verb(l):
    return acc.SIGN_WORDS.get(l['polarity'], 'decides') if l['type'] != 'authority' else 'decides'


def sign_words(p):
    return {'+': 'Sign +, same way', '-': f'Sign {MINUS}, opposite way'}.get(p, 'No sign: it says who decides')


def label(n):
    return N[n]['label']


def link_sentence(l):
    return (f"{l['id']}: {l['name']}. From {l['from']} {label(l['from'])} to {l['to']} {label(l['to'])}. "
            f"{sign_words(l['polarity'])}. Evidence {gword(l['evidence']).lower()}. Delay {dword(l['delay'])}.")


def var_sentence(n):
    return f"{n} {label(n)}. {N[n]['increase_means']}"


def area_name(a):
    return f"Area {a}, {AREAS[a]['title']}" if len(a) == 1 else AREAS[a]['title']


def first_sentence(s):
    m = re.match(r'(.+?[.!?])(\s|$)', s)
    return m.group(1) if m else s


def more_less(loop_id):
    """The read-aloud line, built from the signs: 'More safe seats, more primary decisiveness, ...'."""
    lp = LP[loop_id]
    st = lp['stations']
    word = ['more']
    for s in lp['steps']:
        word.append(word[-1] if s['polarity'] == '+' else ('less' if word[-1] == 'more' else 'more'))
    parts = [f"{word[i]} {st[i]['label'][0].lower() + st[i]['label'][1:]}" for i in range(len(st))]
    back = f"{word[-1]} {st[0]['label'][0].lower() + st[0]['label'][1:]}"
    text = ', '.join(parts) + f', and back to {back}.'
    return text[0].upper() + text[1:], word


def weakest_words(loop_id):
    lp = LP[loop_id]
    if lp['conceptual']:
        return 'No numbered steps to grade'
    if lp['weakest']:
        k = lp['weakest']
        return 'Weakest step ' + ' and '.join(f"{x} {gword(L[x]['evidence'])}" for x in k)
    grades = {s['evidence'] for s in lp['steps']}
    if len(grades) == 1:
        return f"Every step {gword(grades.pop()).lower()}"
    return 'Steps ' + ', '.join(gword(s['evidence']).lower() for s in lp['steps'])


def status_line(loop_id):
    lp = LP[loop_id]
    n = len(lp['reforms'])
    dirw = lp['direction_word']
    return f"{dirw[0].upper() + dirw[1:]} · {lp['delay_word']} · {weakest_words(loop_id)} · {n} reform{'s' if n != 1 else ''}"


# ------------------------------------------------------------------ text measurement
FONT_DIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONT_FILES = {400: 'Inter-Regular.otf', 500: 'Inter-Medium.otf', 600: 'Inter-SemiBold.otf', 700: 'Inter-Bold.otf',
               800: 'Inter-ExtraBold.otf'}
_FONTS = {}
try:
    from PIL import ImageFont
except ImportError:  # measurement falls back to an average width
    ImageFont = None


def tw(s, size, weight=400, tight=False, ls=0.0):
    key = (weight, size)
    f = _FONTS.get(key)
    if f is None and ImageFont is not None and (FONT_DIR / _FONT_FILES[weight]).exists():
        f = _FONTS[key] = ImageFont.truetype(str(FONT_DIR / _FONT_FILES[weight]), size)
    w = f.getlength(s) if f is not None else len(s) * size * 0.56
    if tight:
        w *= 0.94
    return w + ls * size * len(s)


def wrap(s, width, size, weight=400, tight=False, ls=0.0):
    words, lines, cur = s.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if cur and tw(t, size, weight, tight, ls) > width:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def balanced(s, width, size, weight=400, tight=False, ls=0.0):
    """Wrap to the fewest lines, then even the line lengths, as text-wrap: balance does."""
    lines = wrap(s, width, size, weight, tight, ls)
    if len(lines) < 2:
        return lines
    lo, hi = width * 0.5, width
    best = lines
    for _ in range(14):
        mid = (lo + hi) / 2
        t = wrap(s, mid, size, weight, tight, ls)
        if len(t) <= len(lines):
            best, hi = t, mid
        else:
            lo = mid
    return best


# ------------------------------------------------------------------ path geometry
def _q(p0, c, p1, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0], u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1])


def _c(p0, c1, c2, p1, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p1[0],
            u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p1[1])


class Path:
    """Absolute segments: ('M', p), ('L', p), ('Q', c, p), ('C', c1, c2, p)."""

    def __init__(self, segs=None):
        self.segs = list(segs or [])

    def d(self, tf=None):
        f = tf or (lambda p: p)
        out = []
        for s in self.segs:
            pts = [f(p) for p in s[1:]]
            out.append(s[0] + ' '.join(f'{x:.2f} {y:.2f}' for x, y in pts))
        return ''.join(out)

    def poly(self, per=28):
        pts, cur = [], None
        for s in self.segs:
            if s[0] == 'M':
                cur = s[1]
                pts.append(cur)
            elif s[0] == 'L':
                pts.append(s[1])
                cur = s[1]
            elif s[0] == 'Q':
                pts += [_q(cur, s[1], s[2], i / per) for i in range(1, per + 1)]
                cur = s[2]
            elif s[0] == 'C':
                pts += [_c(cur, s[1], s[2], s[3], i / per) for i in range(1, per + 1)]
                cur = s[3]
        return pts

    def length(self):
        p = self.poly()
        return sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1))

    def at(self, s):
        """Point and direction (radians) at distance s along the path."""
        p = self.poly()
        acc_ = 0
        for i in range(len(p) - 1):
            seg = math.dist(p[i], p[i + 1])
            if seg and acc_ + seg >= s:
                t = (s - acc_) / seg
                return ((p[i][0] + t * (p[i + 1][0] - p[i][0]), p[i][1] + t * (p[i + 1][1] - p[i][1])),
                        math.atan2(p[i + 1][1] - p[i][1], p[i + 1][0] - p[i][0]))
            acc_ += seg
        return p[-1], math.atan2(p[-1][1] - p[-2][1], p[-1][0] - p[-2][0])


def q_sub(p0, c, p1, t0, t1):
    """The part of a quadratic curve between t0 and t1, as (start, control, end)."""
    a, b = _q(p0, c, p1, t0), _q(p0, c, p1, t1)
    # control point of the sub-curve: point on tangent lines
    d0 = (2 * ((1 - t0) * (c[0] - p0[0]) + t0 * (p1[0] - c[0])), 2 * ((1 - t0) * (c[1] - p0[1]) + t0 * (p1[1] - c[1])))
    k = (t1 - t0) / 2
    return a, (a[0] + d0[0] * k, a[1] + d0[1] * k), b


def ortho(points, r):
    """A polyline at 0 and 90 degrees with rounded bends of radius r (quadratic corners)."""
    segs = [('M', points[0])]
    for i in range(1, len(points) - 1):
        a, b, c = points[i - 1], points[i], points[i + 1]
        d1, d2 = math.dist(a, b), math.dist(b, c)
        rr = min(r, d1 / 2, d2 / 2)
        if rr < 0.5:
            segs.append(('L', b))
            continue
        p = (b[0] + (a[0] - b[0]) * rr / d1, b[1] + (a[1] - b[1]) * rr / d1)
        q = (b[0] + (c[0] - b[0]) * rr / d2, b[1] + (c[1] - b[1]) * rr / d2)
        segs += [('L', p), ('Q', b, q)]
    segs.append(('L', points[-1]))
    return Path(segs)


# ------------------------------------------------------------------ line marks (design frame memo, section 3)
ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 2)}


def pattern(tex, w):
    if tex == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if tex == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if tex == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def fitted(tex, w, length):
    """Scale the pattern so the line starts and ends on ink."""
    arr, cap = pattern(tex, w)
    if arr is None:
        return '', cap
    if tex == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.3f}', cap
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.3f}' for x in arr), cap


def arrow_head(tip, ang, w, cls='ak-head'):
    al, ab = ARROW[w]
    bx, by = tip[0] - al * math.cos(ang), tip[1] - al * math.sin(ang)
    nx, ny = -math.sin(ang) * ab / 2, math.cos(ang) * ab / 2
    return (f'<path class="{cls}" d="M{bx + nx:.2f} {by + ny:.2f}L{tip[0]:.2f} {tip[1]:.2f}'
            f'L{bx - nx:.2f} {by - ny:.2f}Z"/>')


def diamond(tip, ang, ground, w=2):
    """The open diamond of an authority connection, 14 by 11 px, 2 px stroke, ground fill."""
    hl, hw = 14, 11
    cx, cy = tip[0] - hl / 2 * math.cos(ang), tip[1] - hl / 2 * math.sin(ang)
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -uy, ux
    pts = [(cx + ux * hl / 2, cy + uy * hl / 2), (cx + vx * hw / 2, cy + vy * hw / 2),
           (cx - ux * hl / 2, cy - uy * hl / 2), (cx - vx * hw / 2, cy - vy * hw / 2)]
    return (f'<path class="ak-diamond" d="M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) +
            f'Z" fill="{ground}" stroke-width="{w}" stroke-linejoin="miter"/>')


def sign_tag(c, ang, sign, w, ground, cls='tag'):
    """The pointing tag: a solid tag pointing the way the step runs, sign bars upright in the ground color."""
    a, p, h, sl, sb = TAG[w]
    Lg = a + p
    x0 = -Lg / 2
    pts = [(x0, -h / 2), (x0 + a, -h / 2), (x0 + Lg, 0), (x0 + a, h / 2), (x0, h / 2)]
    ca, sa = math.cos(ang), math.sin(ang)
    P_ = [(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in pts]
    bx = x0 + a / 2
    gx, gy = c[0] + bx * ca, c[1] + bx * sa
    s = (f'<path class="{cls}" d="M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in P_) +
         f'Z" stroke="{ground}" stroke-width="4" stroke-linejoin="round" paint-order="stroke"/>')
    s += f'<rect class="tag-g" x="{gx - sl / 2:.2f}" y="{gy - sb / 2:.2f}" width="{sl}" height="{sb}" fill="{ground}"/>'
    if sign == '+':
        s += f'<rect class="tag-g" x="{gx - sb / 2:.2f}" y="{gy - sl / 2:.2f}" width="{sb}" height="{sl}" fill="{ground}"/>'
    return s


def delay_ticks(path, delay, w, start=12):
    n = {'S': 1, 'M': 2, 'L': 3}[delay]
    half = w / 2 + 4
    out = []
    for i in range(n):
        (x, y), ang = path.at(start + i * 5)
        nx, ny = -math.sin(ang) * half, math.cos(ang) * half
        out.append(f'<path class="tick" d="M{x - nx:.2f} {y - ny:.2f}L{x + nx:.2f} {y + ny:.2f}" stroke-width="2"/>')
    return ''.join(out)


def line_attrs(l):
    return (f'data-link="{l["id"]}" data-sign="{sname(l["polarity"])}" data-grade="{l["evidence"]}" '
            f'data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}"')


def draw_line(l, path, w, ground, cls='', tag_at=None, ticks=True, tag=True, say=None, rel=None, extra='',
              head=None):
    """One connection: case, mark, head (arrow or diamond), sign tag, delay ticks and an 18 px hit stroke.
    The path runs from the tail to the head's base; head is (tip, angle) or None."""
    tex = gtex(l['evidence'])
    length = path.length()
    end_inset = 1.5 * w if tex == 'dotted' else 0
    da, cap = fitted(tex, w, length - end_inset)
    dash = f' stroke-dasharray="{da}"' if da else ''
    d = path.d()
    out = [f'<path class="ak-case" d="{d}" fill="none"{dash} stroke-linecap="{cap}"/>',
           f'<path class="ak-mark tx-{tex}" d="{d}" fill="none" stroke-width="{w}" stroke-linecap="{cap}"{dash}/>']
    if head:
        tip, ang = head
        if l['type'] == 'authority':
            out.append(diamond(tip, ang, ground))
        else:
            out.append(arrow_head(tip, ang, w))
    if tag and l['polarity'] in ('+', '-'):
        if tag_at is None:
            tag_at = path.at(length / 2)
        out.append(f'<g class="tagw">{sign_tag(tag_at[0], tag_at[1], l["polarity"], w, ground)}</g>')
    if ticks:
        out.append(f'<g class="ticks">{delay_ticks(path, l["delay"], w)}</g>')
    out.append(f'<path class="ak-hit" d="{d}"/>')
    rel = rel if rel is not None else f'var-{l["from"].lower()} var-{l["to"].lower()}'
    say = say or link_sentence(l)
    return (f'<g class="wire {cls}" role="button" data-select="link-{l["id"].lower()}" {line_attrs(l)} '
            f'data-rel="{rel}" aria-label="{e(say)}" data-say="{e(say)}"{extra}>' + ''.join(out) + '</g>')


# ------------------------------------------------------------------ identity
def wordmark(master='wordmark/20261028_Wordmark-24px-Master.svg', height=24, cls='wm'):
    src = (ROOT / 'work/build/assets/identity' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    src = src.replace('<svg ', f'<svg class="{cls}" width="{w:.0f}" height="{height}" role="img" '
                      f'aria-label="Oath &amp; Action" focusable="false" ', 1)
    return f'<span class="wm-wrap {cls}-wrap" data-red="signature">{src}</span>'


ICON_UID = defaultdict(int)


def icon(key, edition='black', size=48):
    ICON_UID[key] += 1
    uid = f'i{ICON_UID[key]}-{key.lower()}'
    ic = acc.VARIABLE_ICON.get(key) or acc.reform_icon(key)
    return acc.icon_svg(ic, edition, uid=uid, size=size)


def chip(word, code, cls=''):
    return f'<span class="chip {cls}"><span class="k">{e(word)}</span><span class="c">{e(code)}</span></span>'
