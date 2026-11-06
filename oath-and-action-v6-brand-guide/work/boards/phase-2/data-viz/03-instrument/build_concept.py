"""Build chart system concept 03, Instrument, for the data visualization round (November 6, 2026).

Every chart is a module with seven fixed slots (index, title, measure, controls, figure, notes, source), set on the
Signal Grid's 8 px rhythm. One generator function per chart form draws every artboard (866, 560 and 328 px for the
panel, 680 px for the still, 468 px at 1.7x for the social card) from the shared chart data, so the page doubles as
the seed of the chart kit. Atlas record numbers (RL07, PW15, E09) print as small index labels; texture and fill
against outline carry the second code after color, as the atlas's evidence lines do.

Every value is read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json. Titles, measure lines, notes
and studio strips are studio drafts (see work/handoffs/phase-2/20261106_Data-Viz-03-Notes.md).

Run from the project root:
    python3 -I work/boards/phase-2/data-viz/03-instrument/build_concept.py
Writes 20261106_Data-Viz-03-Instrument.html beside this file.
"""
import csv
import html
import io
import json
import math
import pathlib
import re

from PIL import ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATA = json.loads((ROOT / 'work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json').read_text())
GRID = json.loads((ROOT / 'work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json').read_text())
OUT = HERE / '20261106_Data-Viz-03-Instrument.html'
DS = DATA['datasets']
SPECS = {s['id']: s for s in DATA['specimens']}
ORDER = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']
MINUS = '−'
ARTS = [('w', 866), ('m', 560), ('n', 328)]


def esc(s):
    return html.escape(str(s), quote=True)


def fmt(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def pct(v, d=1):
    s = f'{v:.{d}f}'
    return s.replace('-', MINUS)


# ------------------------------------------------------------------------------------------------ text metrics
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size, weight=400, tight=False):
    """Width of a run of text in px. Digits get a tabular allowance; Inter Tight runs about 4.5% narrower."""
    w = _font(weight).getlength(text) * size / 200
    w += sum(1 for c in text if c.isdigit()) * size * 0.012
    return w * 0.955 if tight else w


def wrap(text, width, size, weight=400, tight=False):
    out, line = [], ''
    for word in str(text).split():
        trial = (line + ' ' + word).strip()
        if line and tw(trial, size, weight, tight) > width:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out or ['']


# SVG text styles: class -> (size, weight). Sizes are rendered px at 1x.
STY = {'x13': (13, 400), 'x13b': (13, 600), 'x13s': (13, 600), 'x15': (15, 400), 'x15b': (15, 600), 'x15k': (15, 700),
       'xin': (13, 600), 'xint': (13, 600), 'xins': (13, 600), 'x14': (14, 400)}


def sw(text, cls):
    size, weight = STY[cls]
    return tw(text, size, weight)


def T(x, y, s, cls, anchor=None, attrs=''):
    a = f' text-anchor="{anchor}"' if anchor and anchor != 'start' else ''
    return f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}"{a}{attrs}>{esc(s)}</text>'


def TL(x, y, rows, cls, lh, anchor=None, attrs=''):
    a = f' text-anchor="{anchor}"' if anchor and anchor != 'start' else ''
    spans = ''.join(f'<tspan x="{fmt(x)}" dy="{0 if i == 0 else lh}">{esc(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}"{a}{attrs}>{spans}</text>'


def R(x, y, w, h, cls, attrs=''):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(max(w, 0))}" height="{fmt(h)}" class="{cls}"{attrs}/>'


def LN(x1, y1, x2, y2, cls, attrs=''):
    return f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" class="{cls}"{attrs}/>'


def da(key, value=None, field=None, mark=None, axis=None, scale=None, cat=None, tip=None):
    """Data-contract attributes for one mark."""
    s = f' data-key="{esc(key)}"'
    if field:
        s += f' data-field="{esc(field)}"'
    if value is not None:
        s += f' data-value="{fmt(value)}"'
    if cat is not None:
        s += f' data-category="{esc(cat)}"'
    if mark:
        s += f' data-mark="{mark}"'
    if axis:
        s += f' data-axis="{axis}"'
    if scale:
        s += f' data-scale="{esc(scale)}"'
    if tip:
        s += f' data-tip="{esc(tip)}"'
    return s


def svg(uid, art, W, H, body, label, defs='', extra_cls=''):
    d = f'<defs>{defs}</defs>' if defs else ''
    return (f'<svg class="art art-{art}{extra_cls}" data-view="{uid}-{art}" viewBox="0 0 {fmt(W)} {fmt(H)}" width="{fmt(W)}" '
            f'height="{fmt(H)}" role="img" aria-label="{esc(label)}" focusable="false">{d}{body}</svg>')


def date_words(iso):
    y, m, d = iso.split('-')
    mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
           'November', 'December'][int(m) - 1]
    return f'{mon} {int(d)}, {y}'


def first_sentence(t):
    m = re.match(r'(.+?\.)(\s|$)', t)
    return m.group(1) if m else t


def rows_of(did):
    return DS[did]['rows']


def rowmap(did):
    return {str(r['key']): r for r in DS[did]['rows']}


# ------------------------------------------------------------------------------------------------ color
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


# The grounds. Every chart ink is a CSS custom property, so one generator draws every ground.
# Values: locked palette, the token architecture's derived values and the palette lab's OKLab tints.
GROUNDS = {
    'white': {'gr': '#FFFFFF', 'ink': '#121212', 'ctx': '#5D636D', 'sec': '#4E535B', 'grid': '#CBCED1', 'rule': '#5D636D',
              'alt': '#DCD9D2', 'focus': '#4A7C74', 'tow': '#3C5F59', 'on-tow': '#FFFFFF', 'away': '#121212',
              'on-away': '#FFFFFF', 'kept': '#B3B6BB', 'some': '#5D636D', 'on-some': '#FFFFFF', 'g2': '#616161',
              'vdl': '#ACC2BE', 'vdxl': '#DDE6E5', 'prl': '#A2AABF', 'prxl': '#DCDFE7', 'pr': '#1F2D5A', 'red': '#E63946'},
    'newsprint': {'gr': '#DCD9D2', 'ink': '#121212', 'ctx': '#5D636D', 'sec': '#4E535B', 'grid': '#B4B4B3', 'rule': '#5D636D',
                  'alt': '#FFFFFF', 'focus': '#4A7C74', 'tow': '#3C5F59', 'on-tow': '#FFFFFF', 'away': '#121212',
                  'on-away': '#DCD9D2', 'kept': '#A1A2A3', 'some': '#5D636D', 'on-some': '#FFFFFF', 'g2': '#565553',
                  'vdl': '#9AAEA6', 'vdxl': '#C1C8C0', 'prl': '#8E94A4', 'prxl': '#BEBFC1', 'pr': '#1F2D5A', 'red': '#E63946'},
    'charcoal': {'gr': '#121212', 'ink': '#DCD9D2', 'ctx': '#A3A19C', 'sec': '#A3A19C', 'grid': '#393C41', 'rule': '#878A8F',
                 'alt': '#121212', 'focus': '#DCD9D2', 'tow': '#76978F', 'on-tow': '#121212', 'away': '#DCD9D2',
                 'on-away': '#121212', 'kept': '#393C41', 'some': '#878A8F', 'on-some': '#121212', 'g2': '#A3A19C',
                 'vdl': '#3F655E', 'vdxl': '#2E4340', 'prl': '#80889C', 'prxl': '#393C41', 'pr': '#80889C', 'red': '#E63946'},
}
GCLS = {'white': 'g-white', 'newsprint': 'g-news', 'charcoal': 'g-dark'}


def ground_css():
    out = []
    for g, t in GROUNDS.items():
        out.append(f'.{GCLS[g]}{{' + ';'.join(f'--{k}:{v}' for k, v in t.items()) + f';background:{t["gr"]};color:{t["ink"]}}}')
    return '\n'.join(out)


# ------------------------------------------------------------------------------------------------ shared codes
# The repair log's direction code: tint, then fill against outline, then position.
DIRS = [('away from voters', 'away', 'Away from voters'), ('toward voters', 'tow', 'Toward voters'),
        ('voters kept existing rules', 'kept', 'Kept existing rules'), ('mixed', 'mixed', 'Mixed'),
        ('pending', 'pend', 'Pending')]
DIR_CLS = {d: c for d, c, _ in DIRS}
DIR_WORD = {d: w for d, _, w in DIRS}
FILL = {'away': 'f-away', 'tow': 'f-tow', 'kept': 'f-kept', 'pend': 'f-pend', 'mixed': 'f-tow'}
ONTXT = {'away': 'xin', 'tow': 'xint', 'kept': 'x13b', 'pend': 'x13b', 'mixed': 'xin'}


def dir_shape(x, y, w, h, c, attrs=''):
    """One direction-coded rect; 'mixed' adds a Charcoal lower-right triangle: both directions in one mark."""
    s = R(x, y, w, h, FILL[c], attrs)
    if c == 'mixed':
        s += f'<path d="M{fmt(x + w)} {fmt(y)}V{fmt(y + h)}H{fmt(x)}Z" class="f-away" aria-hidden="true"/>'
    return s


GRADES = [('documented', 'Documented', 'on the public record'), ('well-supported', 'Well supported', 'strong research evidence'),
          ('plausible', 'Plausible', 'some evidence'), ('contested', 'Contested', 'evidence disputed')]


def grade_defs(uid):
    """Fills for grades that echo the atlas's evidence lines: 2 px dashes at 8 on 4, dash-dot at 8, 3, 2, 3."""
    return (f'<pattern id="{uid}-pl" width="12" height="6" patternUnits="userSpaceOnUse"><path d="M0 3H8" class="pt"/></pattern>'
            f'<pattern id="{uid}-ct" width="16" height="6" patternUnits="userSpaceOnUse"><path d="M0 3H8M11 3H13" class="pt"/></pattern>')


def grade_rect(uid, g, x, y, w, h, attrs=''):
    if g == 'documented':
        return R(x, y, w, h, 'f-ink', attrs)
    if g == 'well-supported':
        return R(x, y, w, h, 'f-g2', attrs)
    pid = f'{uid}-pl' if g == 'plausible' else f'{uid}-ct'
    return (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" class="f-tex" fill="url(#{pid})"{attrs}/>')


def red_mark(d, ground, red=True):
    """The one working red: the headline's point. On Newsprint it takes a 1 px Charcoal keyline (R09)."""
    key = f'<path d="{d}" class="redkey"/>' if ground == 'newsprint' and red else ''
    cls = 'redmark' if red else 'inkmark'
    attrs = ' data-red="working" data-red-job="headline point"' if red else ''
    return f'<g class="redg"{attrs}>{key}<path d="{d}" class="{cls}"/></g>'


# ------------------------------------------------------------------------------------------------ S01 big number
def g_s01(W, uid, g):
    rm = rowmap('stock-trading-ban')
    o = []
    side = W >= 460
    fs = 96 if W >= 700 else 72
    bigw = tw('86%', fs, 800, tight=True)
    lc = max(bigw + 20, round(W * 0.3)) if side else W
    yb = round(0.97 * fs) + 4
    o.append(f'<text x="0" y="{yb}" class="xbig" style="font-size:{fs}px"{da("support-all", rm["support-all"]["value"], mark="label")}>'
             f'{rm["support-all"]["value"]}%</text>')
    cap = wrap('of registered voters favored a ban', lc - 12, 15)
    y = yb + round(0.25 * fs) + 18
    o.append(TL(0, y, cap, 'x15', 20))
    y += 20 * (len(cap) - 1) + 20
    o.append(T(0, y, 'Survey, May 2023', 'x13'))
    big_bottom = y + 8
    # party bars, ordered by value: Democrats 88, Republicans 87, then all voters in Stone
    x0 = lc + 28 if side else 0
    rw = W - x0
    y = 16 if side else big_bottom + 28
    k = (rw - 52) / 100
    o.append(T(x0, y, 'Favored a ban, by group', 'x13') + T(x0 + 100 * k, y, '100%', 'x13', 'end'))
    y += 14
    for key, name, party in (('support-democrats', 'Democrats', 'Democrats'), ('support-republicans', 'Republicans', 'Republicans'),
                             ('support-all', 'All registered voters', None)):
        v = rm[key]['value']
        cls = 'f-ink' if party else 'f-ctx'
        inner = (T(x0, y + 15, name, 'x15b') + R(x0, y + 22, 100 * k, 20, 'track', ' aria-hidden="true"') +
                 R(x0, y + 22, v * k, 20, cls, da(key, v, mark='bar', axis='x', scale='support')) +
                 T(x0 + v * k + 6, y + 37, f'{v}%', 'x15k', attrs=da(key, v, mark='label')))
        o.append(f'<g data-party="{party}">{inner}</g>' if party else inner)
        y += 54
    y_top_end = max(big_bottom, y - 8)
    # Congress, full width: every vote cast in each chamber
    y = y_top_end + 28
    o.append(LN(0, y - 18, W, y - 18, 'grid', ' aria-hidden="true"'))
    o.append(T(0, y, 'What Congress did in 2026', 'x13'))
    y += 26
    hl = wrap('House: passed H.R. 7008, July 22, 2026', W, 15, 600)
    o.append(TL(0, y, hl, 'x15b', 19))
    y += 19 * (len(hl) - 1) + 9
    hy, hn = rm['house-yes']['value'], rm['house-no']['value']
    kh = W / (hy + hn)
    o.append(R(0, y, hy * kh, 24, 'f-away', da('house-yes', hy, mark='bar', axis='x', scale='house')))
    o.append(R(hy * kh, y, hn * kh, 24, 'f-kept', da('house-no', hn, mark='bar', axis='x', scale='house')))
    o.append(T(8, y + 17, f'{hy} for', 'xin', attrs=da('house-yes', hy, mark='label')))
    o.append(T(W - 8, y + 17, f'{hn} against', 'x13b', 'end', attrs=da('house-no', hn, mark='label')))
    y += 24 + 30
    sl = wrap('Senate: vote to take up the bill, September 30, 2026', W, 15, 600)
    o.append(TL(0, y, sl, 'x15b', 19))
    y += 19 * (len(sl) - 1) + 18
    sn = rm['senate-needed']['value']
    o.append(T(0, y, f'{sn} of 100 votes needed, three-fifths of the Senate', 'x13'))
    y += 12
    syes, sno = rm['senate-yes']['value'], rm['senate-no']['value']
    ks = W / (syes + sno)
    o.append(R(0, y, syes * ks, 24, 'f-away', da('senate-yes', syes, mark='bar', axis='x', scale='senate')))
    o.append(R(syes * ks, y, sno * ks, 24, 'f-kept', da('senate-no', sno, mark='bar', axis='x', scale='senate')))
    o.append(T(8, y + 17, f'{syes} for', 'xin', attrs=da('senate-yes', syes, mark='label')))
    o.append(T(W - 8, y + 17, f'{sno} against', 'x13b', 'end', attrs=da('senate-no', sno, mark='label')))
    xn = sn * ks
    o.append(LN(xn, y - 6, xn, y + 24 + 16, 'tick2', da('senate-needed', sn, mark='label')))
    yr = y + 24 + 12
    o.append(red_mark(f'M{fmt(syes * ks + 1.5)} {fmt(yr - 7)}V{fmt(yr)}H{fmt(xn - 1.5)}V{fmt(yr - 7)}', g['ground'], g.get('red', True)))
    lab = wrap(f'{sn - syes} votes short of the {sn} needed', max(W - xn - 10, 110), 13, 600)
    lx = xn + 8 if W - xn - 10 >= 110 else 0
    ly = yr + 5 if lx else yr + 22
    o.append(TL(lx, ly, lab, 'x13b', 16))
    H = ly + 16 * (len(lab) - 1) + 8
    label = (f'Chart. 86% of registered voters favored a ban in May 2023: 88% of Democrats and 87% of Republicans. '
             f'The House passed H.R. 7008 by {hy} to {hn} on July 22, 2026. On September 30, 2026 the Senate vote to take it up '
             f'got {syes} of the {sn} votes needed, {sn - syes} short. The Table button lists every value.')
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S02 line with event notes
def poverty_segments(measure):
    rows = [r for r in rows_of('child-poverty-spm') if r['measure'] == measure]
    years = sorted({r['year'] for r in rows})
    segs, cur = [], []
    for y in years:
        ry = [r for r in rows if r['year'] == y]
        if len(ry) == 1:
            cur.append(ry[0])
        else:
            early = next(r for r in ry if r['comparable_with'] == 'earlier')
            late = next(r for r in ry if r['comparable_with'] == 'later')
            cur.append(early)
            segs.append(cur)
            cur = [late]
    segs.append(cur)
    return segs


BREAK_WORDS = {2013: 'Survey change', 2017: 'Processing change', 2019: 'Method change'}


def g_s02(W, uid, g):
    o = []
    narrow = W < 460
    y0, y1 = 0, 25
    top = 64 if narrow else 48
    ph = 210 if narrow else 260
    pb = top + ph
    px0, px1 = 46, W - (16 if narrow else 104)
    X = lambda yr: px0 + (yr - 2009) * (px1 - px0) / 16
    Y = lambda v: pb - (v - y0) * ph / (y1 - y0)
    for v in range(0, 26, 5):
        o.append(LN(px0 - 8, Y(v), W, Y(v), 'base' if v == 0 else 'grid', ' aria-hidden="true"'))
        o.append(T(px0 - 12, Y(v) + 4.5, f'{v}%' if v == 25 else str(v), 'x13', 'end'))
    for yr in (2009, 2013, 2017, 2021, 2025):
        anchor = 'end' if narrow and yr == 2025 else 'middle'
        o.append(T(min(X(yr) + (14 if anchor == 'end' else 0), W), pb + 20, str(yr), 'x13', anchor))
    # method breaks: labels in tiers, 1 px leaders down to the higher of the two estimates
    placed = []
    for yr, word in BREAK_WORDS.items():
        w = sw(word, 'x13')
        x = min(max(X(yr) - 3, px0), W - w)
        tier = 0
        while any(t == tier and not (x + w + 10 < a or x > b + 10) for a, b, t in placed):
            tier += 1
        placed.append((x, x + w, tier))
        ty = 14 + tier * 17
        hi = max(r['percent'] for r in rows_of('child-poverty-spm') if r['year'] == yr and r['comparable_with'] in ('earlier', 'later'))
        o.append(LN(X(yr), ty + 5, X(yr), Y(hi) - 7, 'lead', ' aria-hidden="true"'))
        o.append(T(x, ty, word, 'x13'))
    # official measure in Stone, the supplemental measure in Charcoal; breaks are never bridged
    for measure, line_cls, r_pt in (('official', 'l-ctx2', 1.5), ('spm', 'l-ink', 1.5)):
        for seg in poverty_segments(measure):
            pts = [(X(r['year']), Y(r['percent'])) for r in seg]
            if len(pts) > 1:
                o.append(f'<path d="M{" L".join(f"{fmt(a)} {fmt(b)}" for a, b in pts)}" class="{line_cls}" aria-hidden="true"/>')
            for r in seg:
                cls = 'f-ink' if measure == 'spm' else 'f-ctx'
                rad = 4 if (measure == 'spm' and (r['year'] in (2021, 2025) or r['comparable_with'] != 'both')) else r_pt
                if measure == 'official' and r['comparable_with'] != 'both':
                    rad = 3
                mname = 'Supplemental measure' if measure == 'spm' else 'Official measure'
                tip = f'{mname}, {r["year"]}: {pct(r["percent"])}%'
                o.append(f'<circle cx="{fmt(X(r["year"]))}" cy="{fmt(Y(r["percent"]))}" r="{rad}" class="{cls}"'
                         f'{da(r["key"], r["percent"], mark="point", axis="y", tip=tip)}/>')
    # direct labels
    if narrow:
        o.append(T(X(2009), Y(23.2), 'Official measure', 'x13s'))
        o.append(T(X(2009), Y(11.8), 'Supplemental measure', 'x13b'))
    elif W < 760:
        o.append(T(X(2009), Y(23.5), 'Official measure', 'x13s'))
        o.append(T(X(2009), Y(14.2), 'Supplemental measure', 'x13b'))
        o.append(T(px1 + 10, Y(13.4) + 5, '13.4%', 'x13b'))
        o.append(T(px1 + 10, Y(13.4) + 21, 'on both', 'x13'))
    else:
        o.append(T(X(2009), Y(23.5), 'Official measure', 'x15b', attrs=' style="fill:var(--sec)"'))
        o.append(T(X(2009), Y(14.6), 'Supplemental Poverty Measure', 'x15b'))
        o.append(T(px1 + 10, Y(13.4) + 5, '13.4%', 'x13b'))
        o.append(T(px1 + 10, Y(13.4) + 21, 'on both', 'x13'))
    # event note joined to 2021 by a leader
    rm = rowmap('child-poverty-spm')
    v21, v22 = rm['spm|2021|standard']['percent'], rm['spm|2022|standard']['percent']
    note = (f'2021: {pct(v21)}%. The expanded child tax credit paid out that year, half in monthly installments (RL15). '
            f'It expired after 2021 (RL16); in 2022 the rate was {pct(v22)}%.')
    nw = 230 if not narrow else W - 8
    lines = wrap(note, nw, 13)
    if narrow:
        ny = pb + 46
        o.append(TL(0, ny, lines, 'x13', 16))
        H = ny + 16 * (len(lines) - 1) + 8
        both = f'2025: {pct(13.4)}% on both measures'
        o.append(T(0, H + 12, both, 'x13b'))
        H += 20
    else:
        # set to the left of 2021, under the line, so no segment crosses it; a leader joins it to the point
        nx = X(2020) - 10
        ny = Y(8.2)
        o.append(f'<path d="M{fmt(nx + 4)} {fmt(Y(v21))}H{fmt(X(2021) - 6)}" class="lead" aria-hidden="true"/>')
        o.append(TL(nx, ny, lines, 'x13', 16, 'end'))
        H = pb + 30
    label = (f'Line chart of child poverty, 2009 to 2025. Under the Supplemental Poverty Measure the rate was 17.0% in 2009, fell to '
             f'{pct(v21)}% in 2021 and stood at 12.0% in 2022 and 13.4% in 2025. The official measure ran from 20.7% to 13.4%. '
             f'The lines break in 2013, 2017 and 2019, when the Census Bureau changed its survey, processing or method. The Table button lists every value.')
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S03 ranked bar
def key_row(items, W, y, uid=None):
    """Inline key: (swatch markup function, words). Wraps at W. Returns markup and the y below it."""
    o, x = [], 0
    for draw, words in items:
        w = 14 + 6 + sw(words, 'x13') + 18
        if x and x + w > W:
            x, y = 0, y + 22
        o.append(draw(x, y - 11) + T(x + 20, y, words, 'x13'))
        x += w
    return ''.join(o), y + 12


def dir_key(W, y):
    items = [((lambda c: (lambda x, yy: dir_shape(x, yy, 14, 14, c, ' aria-hidden="true"')))(c), w) for _, c, w in DIRS]
    return key_row(items, W, y)


def g_s03(W, uid, g):
    rows = rows_of('rule-changes-by-instrument')
    o = []
    kmark, y = dir_key(W, 14)
    o.append(kmark)
    y += 14
    side = W >= 640
    lw = (max(sw(r['key'], 'x15b') for r in rows) + 14) if side else 0
    rmax = sw(f'{rows[0]["value"]} changes', 'x15k') + 12
    k = (W - lw - rmax) / 17 if side else W / 17
    bh = 24
    for i, r in enumerate(rows):
        name = r['key']
        if side:
            by = y
            o.append(T(0, by + 17, name, 'x15b'))
            if r['away from voters'] == 0 and r['value'] >= 10:
                o.append(T(0, by + 34, 'None away from voters', 'x13'))
        else:
            o.append(T(0, y + 15, name, 'x15b'))
            o.append(T(W, y + 15, f'{r["value"]} changes' if i == 0 else str(r['value']), 'x15k', 'end', da(name, r['value'], mark='label')))
            by = y + 22
        x = lw
        for d, c, _ in DIRS:
            v = r[d]
            if not v:
                continue
            w = v * k
            o.append(dir_shape(x, by, w, bh, c, da(name, v, field=d, mark='bar', axis='x')))
            if w >= 18:
                o.append(T(x + w / 2, by + 17, str(v), ONTXT[c], 'middle', da(name, v, field=d, mark='label')))
            x += w
        tot = f'{r["value"]} changes' if i == 0 else str(r['value'])
        if side:
            o.append(T(x + 8, by + 17, tot, 'x15k', attrs=da(name, r['value'], mark='label')))
        xe = x + 8 + sw(tot, 'x15k') + 14
        extra = 0
        if name == 'State statute':
            note = f'{r["away from voters"]} of its {r["value"]} moved the rules away from voters'
            if side and W - xe >= 150:
                lines = wrap(note, W - xe, 13)
                o.append(TL(xe, by + 17 - 8 * (len(lines) - 1), lines, 'x13', 16))
            else:
                o.append(T(0, by + bh + 18, note, 'x13'))
                extra = 22
        if not side and r['away from voters'] == 0 and r['value'] >= 10:
            o.append(T(0, by + bh + 18, 'None away from voters', 'x13'))
            extra = 22
        y = by + bh + 16 + extra if side else by + bh + 18 + extra
        if side and r['away from voters'] == 0 and r['value'] >= 10:
            y += 4
    H = y + 2
    label = ('Ranked bar chart of the 64 rule changes by how they were made. ' +
             '; '.join(f'{r["key"]}: {r["value"]}, of them {r["away from voters"]} away from voters and {r["toward voters"]} toward' for r in rows) +
             '. The Table button lists every value.')
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S04 dumbbell
AGES = [('18_to_24', '18 to 24'), ('25_to_44', '25 to 44'), ('45_to_64', '45 to 64'), ('65_and_over', '65 and over'),
        ('all', 'All citizens 18 and over')]


def turnout(age, year):
    return rowmap('turnout-by-age')[f'{age}|{year}|citizen_voting_age_population']


def change_words(a, b, first):
    d = round(b - a, 1)
    unit = ' points' if first else ''
    if d > 0:
        return f'Up {d:.1f}{unit}'
    if d < 0:
        return f'Down {abs(d):.1f}{unit}'
    return 'No change'


def g_s04(W, uid, g):
    o = []
    side = W >= 560
    lw = 190 if side else 0
    cw = 116 if side else 0
    x0 = lw + (10 if side else 14)
    x1 = W - cw - 26 if side else W - 34
    lo, hi = 40, 80
    X = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)
    y = 14
    for v in range(lo, hi + 1, 10):
        o.append(T(X(v), y, f'{v}%' if v == hi else str(v), 'x13', 'middle'))
    y += 18
    first = True
    for age, name in AGES:
        a, b = turnout(age, 2020), turnout(age, 2024)
        ctx = age == 'all'
        if ctx:
            o.append(LN(0, y - 2, W, y - 2, 'grid', ' aria-hidden="true"'))
            y += 10
        if side:
            cy = y + 26
            o.append(T(0, cy + 5, name, 'x15b' if not ctx else 'x15', attrs='' if not ctx else ' style="fill:var(--sec)"'))
            o.append(T(W, cy + 5, change_words(a['voted_pct'], b['voted_pct'], first), 'x13b', 'end'))
        else:
            o.append(T(0, y + 15, name, 'x15b' if not ctx else 'x15', attrs='' if not ctx else ' style="fill:var(--sec)"'))
            o.append(T(W, y + 15, change_words(a['voted_pct'], b['voted_pct'], first), 'x13b', 'end'))
            cy = y + 48
        xa, xb = X(a['voted_pct']), X(b['voted_pct'])
        o.append(LN(min(xa, xb), cy, max(xa, xb), cy, 'l-ctx2', ' aria-hidden="true"'))
        fill = 'f-ink' if not ctx else 'f-ctx'
        o.append(f'<circle cx="{fmt(xb)}" cy="{fmt(cy)}" r="6" class="{fill}"{da(b["key"], b["voted_pct"], mark="point", axis="x")}/>')
        o.append(f'<circle cx="{fmt(xa)}" cy="{fmt(cy)}" r="5" class="ring"{da(a["key"], a["voted_pct"], mark="point", axis="x")}/>')
        # values: the lower one to the left, the higher to the right
        lo_r, hi_r = (a, b) if a['voted_pct'] <= b['voted_pct'] else (b, a)
        o.append(T(min(xa, xb) - 10, cy + 5, pct(lo_r['voted_pct']), 'x13b', 'end', da(lo_r['key'], lo_r['voted_pct'], mark='label')))
        o.append(T(max(xa, xb) + 10, cy + 5, pct(hi_r['voted_pct']), 'x13b', attrs=da(hi_r['key'], hi_r['voted_pct'], mark='label')))
        if first:
            ky = cy - 14
            (xl, wl), (xr, wr) = sorted([(xa, '2020'), (xb, '2024')])
            o.append(T(xl + 6, ky, wl, 'x13', 'end'))
            o.append(T(xr - 6, ky, wr, 'x13'))
            first = False
        y = cy + (24 if side else 22)
    H = y + 4
    parts = '; '.join(f'{n}: {turnout(a, 2020)["voted_pct"]}% in 2020 and {turnout(a, 2024)["voted_pct"]}% in 2024' for a, n in AGES)
    label = f'Dot chart of reported voting among citizens by age, 2020 and 2024. {parts}. The Table button lists every value.'
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S05 small multiples
HGROUPS = [('all_households', 'All households'), ('non_hispanic_white', 'Non-Hispanic White'), ('black', 'Black'),
           ('hispanic', 'Hispanic, of any race')]


def home_segments(group):
    """Annual rows for one group. 2002 uses the value revised to 2000 Census controls. Black and non-Hispanic White
    break at 2003, when race categories changed."""
    rows = [r for r in rows_of('homeownership-by-race') if r['group'] == group and
            (r['series_variant'] == 'standard' or (r['year'] == 2002 and r['series_variant'] == 'revised_2000_census'))]
    rows.sort(key=lambda r: r['year'])
    if group in ('black', 'non_hispanic_white'):
        return [[r for r in rows if r['year'] < 2003], [r for r in rows if r['year'] >= 2003]]
    return [rows]


def g_s05(W, uid, g):
    o = []
    cols = 4 if W >= 760 else (2 if W >= 460 else 1)
    gap = 20
    gut = 40
    pw = (W - gut - gap * (cols - 1)) / cols
    lo, hi = 20, 80
    ph = 210 if cols == 4 else 180
    head = 30
    endw = 50
    rm = rowmap('homeownership-by-race')
    gap25 = rm['non_hispanic_white|2025|race_alone|standard']['rate_pct'] - rm['black|2025|race_alone|standard']['rate_pct']
    gap03 = rm['non_hispanic_white|2003|race_alone|standard']['rate_pct'] - rm['black|2003|race_alone|standard']['rate_pct']
    H = 0
    for i, (grp, name) in enumerate(HGROUPS):
        c, rr = i % cols, i // cols
        ox = gut + c * (pw + gap)
        oy = rr * (head + ph + 44)
        top = oy + head
        X = lambda yr, ox=ox: ox + 2 + (yr - 1994) * (pw - endw - 4) / 31
        Y = lambda v, top=top: top + (hi - v) * ph / (hi - lo)
        o.append(T(ox, oy + 16, name, 'x15b'))
        for v in range(lo, hi + 1, 10):
            o.append(LN(ox, Y(v), ox + pw, Y(v), 'grid', ' aria-hidden="true"'))
            if c == 0:
                o.append(T(ox - 8, Y(v) + 4.5, f'{v}%' if v == hi else str(v), 'x13', 'end'))
        for yr in (1994, 2025):
            o.append(T(X(yr), Y(lo) + 18, str(yr), 'x13', 'middle' if yr == 1994 and False else ('start' if yr == 1994 else 'end')))
        sc = f'panel-{grp}'
        # the other three groups in Stone, then this group in Charcoal
        for og, _ in HGROUPS:
            if og == grp:
                continue
            for seg in home_segments(og):
                pts = ' L'.join(f'{fmt(X(r["year"]))} {fmt(Y(r["rate_pct"]))}' for r in seg)
                o.append(f'<path d="M{pts}" class="l-ctx" aria-hidden="true"/>')
        for seg in home_segments(grp):
            pts = ' L'.join(f'{fmt(X(r["year"]))} {fmt(Y(r["rate_pct"]))}' for r in seg)
            o.append(f'<path d="M{pts}" class="l-ink" aria-hidden="true"/>')
            for r in seg:
                ends = r['year'] in (2002, 2003) and grp in ('black', 'non_hispanic_white')
                o.append(f'<circle cx="{fmt(X(r["year"]))}" cy="{fmt(Y(r["rate_pct"]))}" r="{2.5 if ends else 1.5}" class="f-ink"'
                         f'{da(r["key"], r["rate_pct"], mark="point", axis="y", scale=sc)}/>')
        last = rm[next(k for k in rm if k.startswith(grp + '|2025|'))]
        o.append(T(X(2025) + 6, Y(last['rate_pct']) + 4, f'{pct(last["rate_pct"])}%', 'x13b', attrs=da(last['key'], last['rate_pct'], mark='label')))
        nx = ox + 2
        if grp == 'non_hispanic_white':
            lines = wrap('The line breaks at 2003, when race categories changed.', pw - 8, 13)
            o.append(TL(nx, Y(31.5), lines, 'x13', 16))
        if grp == 'black':
            lines = wrap(f'{pct(gap25)} points below non-Hispanic White in 2025; {pct(gap03)} in 2003', pw - 8, 13)
            o.append(TL(nx, Y(31.5), lines, 'x13b', 16))
        H = max(H, top + ph + 26)
    label = ('Four line charts of the homeownership rate, 1994 to 2025, on one scale. In 2025: ' +
             '; '.join(f'{n} {rm[next(k for k in rm if k.startswith(gp + "|2025|"))]["rate_pct"]}%' for gp, n in HGROUPS) +
             f'. Non-Hispanic White householders led Black householders by {pct(gap25)} points in 2025 and {pct(gap03)} in 2003. '
             'The Table button lists every value.')
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S06 comparison table (HTML)
FAMS = [('DQ', 'Quality of democracy'), ('GE', 'Government efficacy'), ('EP', 'Economic performance'), ('EQ', 'Income and wealth equality')]
CLASS_CSS = {'up': 'c-up', 'slightly up': 'c-sup', 'flat': 'c-flat', 'flat or down': 'c-fod', 'down': 'c-down', 'mixed': 'c-mix',
             'same as ii': 'c-same'}
CLASS_WORD = {'up': 'Up', 'slightly up': 'Slightly up', 'flat': 'Flat', 'flat or down': 'Flat or down', 'down': 'Down',
              'mixed': 'Mixed', 'same as ii': 'Same as scenario ii'}
GLYPH = {
    'up': '<path d="M8 2.5L14.5 13.5H1.5Z" class="gf-up"/>',
    'slightly up': '<path d="M8 4.2L13.2 12.8H2.8Z" class="gs-up"/>',
    'flat': '<path d="M1.5 6.75H14.5V9.25H1.5Z" class="gf-flat"/>',
    'flat or down': '<path d="M1.5 2.5H14.5V4.75H1.5Z" class="gf-flat"/><path d="M8 14L12.6 7.6H3.4Z" class="gs-down"/>',
    'down': '<path d="M8 13.5L14.5 2.5H1.5Z" class="gf-down"/>',
    'mixed': '<path d="M4.8 1.5L8.6 7.6H1Z" class="gf-up"/><path d="M11.2 14.5L15 8.4H7.4Z" class="gf-down"/>',
    'same as ii': '<path d="M2 4.6H14V6.8H2ZM2 9.2H14V11.4H2Z" class="gf-flat"/>',
}


def glyph(c, size=16):
    return (f'<svg class="gl" viewBox="0 0 16 16" width="{size}" height="{size}" aria-hidden="true" focusable="false">'
            f'{GLYPH[c]}</svg>')


def g_s06_html(uid, g):
    rows = rows_of('scenarios-2030')
    key = ''.join(f'<li>{glyph(c)}<span>{esc(CLASS_WORD[c])}</span></li>' for c in CLASS_WORD)
    head = ''.join(f'<th scope="col">{esc(n)}</th>' for _, n in FAMS)
    body = []
    for r in rows:
        cells = []
        for f, fname in FAMS:
            c = r[f + '_class']
            cells.append(f'<td class="{CLASS_CSS[c]}"{da(r["key"], field=f, cat=r[f], mark="cell")}>'
                         f'<span class="fam-l">{esc(fname)}</span><span class="cw">{glyph(c)}<span>{esc(r[f])}</span></span></td>')
        body.append(f'<tr><th scope="row"><span class="sid">{esc(r["key"])}</span> <span class="sname">{esc(r["name"])}</span></th>{"".join(cells)}</tr>')
    return (f'<div class="sg"><p class="sg-kh">Glyph and tint: the studio\'s reading of the atlas\'s words, which print in every cell</p>'
            f'<ul class="sg-key">{key}</ul>'
            f'<table class="sgt"><caption class="vh">Direction each outcome family would take by 2036 in eight scenarios, in the atlas\'s words</caption>'
            f'<thead><tr><th scope="col">Scenario</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


# ------------------------------------------------------------------------------------------------ S07 tile map
STATUS = [('bans in all elections', 'f-away', 'xin', 'Bans it in every election'),
          ('bans in some elections', 'f-some', 'xins', 'Bans it in some elections'),
          ('no ban', 'f-none', 'x13b', 'No state ban')]
ST_FILL = {s: (f, t) for s, f, t, _ in STATUS}


def g_s07(W, uid, g):
    rows = rowmap('rcv-bans')
    o = []
    wide = W >= 760
    mid = 460 <= W < 760
    pitch = 56 if wide else (44 if mid else 27)
    gap = 4 if not (not wide and not mid) else 2
    t = pitch - gap
    cnt = {s: sum(1 for r in rows.values() if r['status'] == s) for s, *_ in STATUS}
    words = {'bans in all elections': f'Bans it in every election ({cnt["bans in all elections"]})',
             'bans in some elections': f'Bans it in some elections ({cnt["bans in some elections"]})',
             'no ban': f'No state ban ({cnt["no ban"] - 1} states and DC)'}
    if wide:
        ky, kx = 20, pitch + 4
        for s, f, _, _ in STATUS:
            o.append(R(kx, ky - 11, 14, 14, f, ' aria-hidden="true"') + T(kx + 22, ky, words[s], 'x13'))
            ky += 24
        gy = 0
    else:
        kmark, ky = key_row([((lambda f: (lambda x, yy: R(x, yy, 14, 14, f, ' aria-hidden="true"')))(f), words[s]) for s, f, _, _ in STATUS], W, 14)
        o.append(kmark)
        gy = ky + 10
    for tcell in GRID:
        r = rows[tcell['code']]
        f, tc = ST_FILL[r['status']]
        x, y = tcell['col'] * pitch, gy + tcell['row'] * pitch
        yr = f', {date_words(r["enacted_date"])}' if r['enacted_date'] else ''
        tip = f'{r["name"]}: {r["status"]}{yr}. {r["scope_note"]}' if r['prohibits_rcv'] else f'{r["name"]}: no state ban'
        o.append(R(x, y, t, t, f, da(r['key'], field='status', cat=r['status'], mark='cell', tip=tip)))
        if wide or mid:
            o.append(T(x + t / 2, y + (22 if wide else 18), r['key'], tc, 'middle'))
            if r['prohibits_rcv']:
                o.append(T(x + t / 2, y + (40 if wide else 34), str(r['enacted_year']), tc.replace('x13b', 'x13'), 'middle',
                           ' style="font-weight:400"'))
        else:
            o.append(T(x + t / 2, y + t / 2 + 4.5, r['key'], tc, 'middle'))
    gb = gy + 8 * pitch - gap
    notes = [f'Ohio, 2026: home-rule cities may still adopt it, but they lose state local government fund money while it is in effect.',
             'Tennessee, 2022: county election commissions may not use it for state or local offices.',
             'Missouri wrote its ban into the state constitution in 2024; the other 18 are statutes.',
             'The map shows state bans only. Whether a city in a state with no ban may adopt it depends on other state law, which the map does not show.']
    if wide:
        nx = 12 * pitch + 14
        nw = W - nx
        ny = 14
        for n in notes:
            lines = wrap(n, nw, 13)
            o.append(TL(nx, ny, lines, 'x13', 16))
            ny += 16 * len(lines) + 10
        H = max(gb, ny) + 4
    else:
        ny = gb + 24
        for n in notes:
            lines = wrap(n, W, 13)
            o.append(TL(0, ny, lines, 'x13', 16))
            ny += 16 * len(lines) + 8
        H = ny - 6
    label = (f'Tile map of the 50 states and DC. {cnt["bans in all elections"]} states ban ranked-choice voting in every election: ' +
             ', '.join(r['name'] for r in rows.values() if r['status'] == 'bans in all elections') +
             '. Ohio and Tennessee ban it in some elections. The other 31 states and DC have no state ban. The Table button lists every state.')
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S08 unit chart
def unit_svg(r):
    """One repair-log record: a 28 px square in its direction code, numbered by its record."""
    c = DIR_CLS[r['direction']]
    tip = f'{r["key"]}, {date_words(r["date"])}, {r["jurisdiction"]}. {DIR_WORD[r["direction"]]}. {first_sentence(r["rule"])}'
    return (f'<svg class="u" viewBox="0 0 28 28" width="28" height="28" aria-hidden="true" focusable="false">'
            f'{dir_shape(0.75, 0.75, 26.5, 26.5, c, da(r["key"], cat=r["direction"], mark="unit", tip=tip))}'
            f'{T(14, 18.5, r["key"][2:], ONTXT[c], "middle")}</svg>')


def g_s08_html(uid, g):
    """The unit chart is one HTML grid, so every record is drawn once and the layout reflows: direction rows across two
    period panels when the module is 700 px or wider, the two panels stacked below that."""
    rows = sorted(rows_of('rule-changes'), key=lambda r: (r['date'], r['key']))
    panels = [('1965 to 2024', [r for r in rows if r['year'] < 2025]), ('2025 and 2026', [r for r in rows if r['year'] >= 2025])]
    c = DS['rule-changes']['counts']
    label = ('Unit chart: one square per change in the repair log, split at January 1, 2025. Before 2025: ' +
             ', '.join(f'{sum(1 for r in panels[0][1] if r["direction"] == d)} {w.lower()}' for d, _, w in DIRS) +
             '. In 2025 and 2026: ' + ', '.join(f'{sum(1 for r in panels[1][1] if r["direction"] == d)} {w.lower()}' for d, _, w in DIRS) +
             f'. In all: {c["toward voters"]} toward voters and {c["away from voters"]} away. The Table button lists every change.')
    out = [f'<div class="ul" role="img" aria-label="{esc(label)}"><div class="ul-h0" aria-hidden="true"></div>']
    for i, (title, rs) in enumerate(panels):
        out.append(f'<div class="ul-ph{" b" if i else ""}" style="--o:{i * 6}"><p class="ul-pt">{esc(title)}</p><p class="ul-pn">{len(rs)} changes</p></div>')
    for j, (d, cc, word) in enumerate(DIRS):
        parts = [[r for r in rs if r['direction'] == d] for _, rs in panels]
        out.append(f'<div class="ul-dl"><p class="ul-dw">{esc(word)}</p><p class="ul-dn">{sum(len(pp) for pp in parts)} in all</p></div>')
        for i, pp in enumerate(parts):
            units = ''.join(unit_svg(r) for r in pp)
            cnt = f'<span class="ul-c">{len(pp)}</span>' if pp else '<span class="ul-none">none</span>'
            out.append(f'<div class="ul-cell{" b" if i else ""}" style="--o:{i * 6 + j + 1}"><p class="ul-cw">{esc(word)}</p>'
                       f'<div class="ul-us">{units}{cnt}</div></div>')
    out.append('</div>')
    return ''.join(out)


# ------------------------------------------------------------------------------------------------ S09 timeline
def lead_name(t):
    return t.split(' (')[0]


def dec_year(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return y + ((m - 1) * 30.4 + d - 1) / 365


def place_flags(items, x_max, gap=10):
    """Tier flag labels above a time line so no label covers another's leader.

    items: dicts with x (dot), w (label width). A label at tier t spanning [a, b] that covers another dot's x must sit
    above that dot's label; overlapping labels never share a tier. Start-anchored labels cover dots to their right and
    end-anchored ones cover dots to their left, so the leftmost label of any mutual cover flips to end-anchored first.
    Tiers are then assigned in an order where every covered label is placed before the label that covers it."""
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
    left = list(items)
    done = []
    while left:
        ready = [i for i in left if not any(covers(i, k) for k in left)]
        if not ready:  # a cycle survived: fall back to the leftmost label
            ready = [min(left, key=lambda i: i['x'])]
        for i in sorted(ready, key=lambda i: i['x']):
            a, b = span(i)
            t = max([k['t'] + 1 for k in done if covers(i, k)] + [0])
            while any(k['t'] == t and not (b + gap < k['a'] or a > k['b'] + gap) for k in done):
                t += 1
            i['t'], i['a'], i['b'] = t, a, b
            done.append(i)
            left.remove(i)
    return items


def g_s09(W, uid, g):
    """Four lanes on one true time scale. Each dot carries its studio key (E01 to E24) as an index label, and the list
    under each lane gives every event's year and lead name, so names print in full at every width without stacking."""
    ds = DS['history-events']
    rows = ds['rows']
    threads = ds['threads']
    o = []
    lw = 176 if W >= 760 else 0
    ax0 = lw
    aw = W - ax0
    px0, px1 = ax0 + 8, W - 8
    X = lambda dy: px0 + (dy - 1870) * (px1 - px0) / (2026.6 - 1870)
    cols = 3 if aw >= 600 else (2 if aw >= 440 else 1)
    cg = 20
    cw = (aw - cg * (cols - 1)) / cols
    ticks = (1870, 1900, 1930, 1960, 1990, 2020) if aw >= 440 else (1870, 2026)
    y = 0
    for li, th in enumerate(threads):
        ev = sorted([r for r in rows if r['thread'] == th['id']], key=lambda r: r['date'])
        ql = wrap(th['question'], (lw - 20) if lw else W, 13)
        if lw:
            o.append(T(0, y + 16, th['label'], 'x15b') + TL(0, y + 34, ql, 'x13', 16))
            top = y
        else:
            o.append(T(0, y + 16, th['label'], 'x15b') + TL(0, y + 34, ql, 'x13', 16))
            top = y + 34 + 16 * (len(ql) - 1) + 10
        # index labels over the dots, in tiers where they would touch
        flags = [{'x': X(dec_year(r['date'])), 'w': sw(r['key'], 'x13s') + 5, 'r': r} for r in ev]
        place_flags(flags, W, gap=6)
        tiers = max(f_['t'] for f_ in flags) + 1
        line_y = top + tiers * 17 + 12
        o.append(LN(px0 - 6, line_y, px1 + 6, line_y, 'lane', ' aria-hidden="true"'))
        for f_ in flags:
            x, r = f_['x'], f_['r']
            ty = line_y - 13 - f_['t'] * 17
            o.append(LN(x, line_y - 5, x, ty - 10, 'lead', ' aria-hidden="true"'))
            o.append(T(x + 4 if f_['anchor'] == 'start' else x - 4, ty, r['key'], 'x13s', f_['anchor']))
            tip = f'{r["key"]}, {date_words(r["date"])}. {r["title"]}. {r["mechanism"]}'
            o.append(f'<circle cx="{fmt(x)}" cy="{fmt(line_y)}" r="{5 if lw else 4.5}" class="f-ink"'
                     f'{da(r["key"], round(dec_year(r["date"]), 3), field="year", mark="point", axis="x", tip=tip)}/>')
        for i, yr in enumerate(ticks):
            anchor = 'start' if i == 0 else ('end' if yr == 2026 else 'middle')
            o.append(T(X(yr) if yr != 2026 else W, line_y + 19, str(yr), 'x13', anchor))
        # the list: index, year, lead name, in date order across the columns
        ly = line_y + 46
        for rstart in range(0, len(ev), cols):
            row = ev[rstart:rstart + cols]
            hmax = 1
            for ci, r in enumerate(row):
                cx = ax0 + ci * (cw + cg)
                nl = wrap(lead_name(r['title']), cw - 76, 13, 600)
                hmax = max(hmax, len(nl))
                o.append(T(cx, ly, r['key'], 'x13s') + T(cx + 34, ly, str(r['year']), 'x13') + TL(cx + 76, ly, nl, 'x13b', 16))
            ly += 16 * hmax + 8
        y = max(ly, top + 16 * (len(ql) + 2)) + 14
        if li < len(threads) - 1:
            o.append(LN(0, y - 12, W, y - 12, 'grid', ' aria-hidden="true"'))
            y += 8
    H = y - 14
    label = ('Timeline of 24 documented rule changes on four threads, 1870 to 2026. ' +
             '. '.join(f'{th["label"]}: ' + ', '.join(f'{r["year"]} {lead_name(r["title"])}' for r in sorted(rows, key=lambda r: r['date']) if r['thread'] == th['id'])
                       for th in threads) + '. The Table button lists every event.')
    return ''.join(o), H, '', label


# ------------------------------------------------------------------------------------------------ S10 evidence mix
def g_s10(W, uid, g):
    rows = sorted(rows_of('claims-by-grade'), key=lambda r: (-r['documented'] / r['value'], r['key']))
    o = []
    defs = grade_defs(uid)
    items = [((lambda gk: (lambda x, yy: grade_rect(uid, gk, x, yy, 26, 14, ' aria-hidden="true"')))(gk), f'{w}: {gl}')
             for gk, w, gl in GRADES]
    o_key = []
    x, y = 0, 14
    for draw, words in items:
        w = 26 + 8 + sw(words, 'x13') + 20
        if x and x + w > W:
            x, y = 0, y + 22
        o_key.append(draw(x, y - 11) + T(x + 34, y, words, 'x13'))
        x += w
    o.append(''.join(o_key))
    y += 26
    side = W >= 560
    idw, nmw = (44, max(sw(r['title'], 'x15') for r in rows) + 16) if side else (0, 0)
    rw = 96 if side else 58
    bx0 = idw + nmw
    bw = W - bx0 - rw
    if side:
        o.append(T(bx0, y, '0', 'x13') + T(bx0 + bw, y, '100%', 'x13', 'end'))
        o.append(T(W, y, 'Documented', 'x13', 'end'))
    else:
        o.append(T(W, y, 'Documented', 'x13', 'end'))
    y += 10
    bh = 18
    for i, r in enumerate(rows):
        if side:
            by = y
            o.append(T(0, by + 14, r['key'], 'x13s') + T(idw, by + 14, r['title'], 'x15'))
        else:
            o.append(T(0, y + 14, r['key'], 'x13s') + T(42, y + 14, r['title'], 'x15'))
            by = y + 22
        x = bx0
        k = bw / r['value']
        segs = []
        for gk, _, _ in GRADES:
            v = r[gk]
            if not v:
                continue
            o.append(grade_rect(uid, gk, x, by, v * k, bh, da(r['key'], v, field=gk, mark='bar', axis='x', scale=r['key'])))
            segs.append(x + v * k)
            x += v * k
        for sx in segs[:-1]:
            o.append(LN(sx, by - 1, sx, by + bh + 1, 'sep', ' aria-hidden="true"'))
        share = 100 * r['documented'] / r['value']
        o.append(T(W, by + 14, f'{share:.0f}%', 'x15k', 'end', da(r['key'], r['documented'], field='documented', mark='label')))
        y = by + bh + (14 if side else 16)
    # the record: the question with the largest share of plausible or contested claims
    pick = max(rows, key=lambda r: (r['plausible'] + r['contested']) / r['value'])
    n = pick['plausible'] + pick['contested']
    note = (f'{pick["key"]}, {pick["title"].lower()}: {n} of its {pick["value"]} claims are plausible or contested, '
            f'the largest share of any question.')
    lines = wrap(note, (W - bx0 - 8) if side else W, 13)
    o.append(TL(bx0 if side else 0, y + 12, lines, 'x13', 16))
    H = y + 12 + 16 * (len(lines) - 1) + 8
    tot = DS['claims-by-grade']['totals']
    label = (f'Stacked bars, one per everyday question, showing the share of its claims by evidence grade, sorted by the documented share. '
             f'Across all 433 claims: {tot["documented"]} documented, {tot["well-supported"]} well supported, {tot["plausible"]} plausible, '
             f'{tot["contested"]} contested. ' + '; '.join(f'{r["key"]} {r["title"]} {100 * r["documented"] / r["value"]:.0f}% documented' for r in rows) +
             '. The Table button lists every count.')
    return ''.join(o), H, defs, label


# ------------------------------------------------------------------------------------------------ table equivalents and CSV
def table(head, rows, cls='eqt', caption=''):
    th = ''.join(f'<th scope="col">{esc(h)}</th>' for h in head)
    body = []
    for r in rows:
        cells = []
        for j, c in enumerate(r):
            if j == 0:
                cells.append(f'<th scope="row">{esc(c)}</th>')
            else:
                cells.append(f'<td data-label="{esc(head[j])}"><span class="tl">{esc(head[j])}</span>{esc(c)}</td>')
        body.append('<tr>' + ''.join(cells) + '</tr>')
    cap = f'<caption>{esc(caption)}</caption>' if caption else ''
    return f'<div class="tbl"><table class="{cls}">{cap}<thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def num_cell(v):
    return pct(v) if isinstance(v, float) and not float(v).is_integer() else str(int(v)) if isinstance(v, (int, float)) else str(v)


def eq_s01():
    rs = rows_of('stock-trading-ban')
    return table(['Group', 'Measure', 'Value'], [[r['group'], r['measure'], r['value']] for r in rs], caption='Survey shares and votes')


def eq_s02():
    rs = sorted(rows_of('child-poverty-spm'), key=lambda r: (r['year'], r['measure'], r['comparable_with'] != 'earlier'))
    out = []
    for r in rs:
        est = {'both': '', 'earlier': 'joins earlier years', 'later': 'joins later years'}[r['comparable_with']]
        out.append([r['year'], 'Supplemental' if r['measure'] == 'spm' else 'Official', pct(r['percent']),
                    pct(r['moe_pct']) if r['moe_pct'] not in ('', None) else 'not given', est])
    return table(['Year', 'Measure', 'Percent of children', 'Margin of error, points', 'Break-year estimate'], out,
                 caption='Children under 18 in poverty')


def eq_s03():
    rs = rows_of('rule-changes-by-instrument')
    return table(['Instrument', 'All', 'Away from voters', 'Toward voters', 'Kept existing rules', 'Mixed', 'Pending'],
                 [[r['key'], r['value'], r['away from voters'], r['toward voters'], r['voters kept existing rules'], r['mixed'], r['pending']]
                  for r in rs], caption='Rule changes by instrument and direction')


def eq_s04():
    out = []
    for a, n in AGES:
        x, y = turnout(a, 2020), turnout(a, 2024)
        out.append([n, pct(x['voted_pct']), pct(y['voted_pct']), change_words(x['voted_pct'], y['voted_pct'], True)])
    return table(['Age group', '2020', '2024', 'Change'], out, caption='Reported voting among citizens, percent')


def eq_s05():
    out = []
    years = sorted({r['year'] for r in rows_of('homeownership-by-race')})
    for yr in years:
        row = [yr]
        for grp, _ in HGROUPS:
            seg = [r for s in home_segments(grp) for r in s if r['year'] == yr]
            row.append(pct(seg[0]['rate_pct']) if seg else '')
        out.append(row)
    return table(['Year'] + [n for _, n in HGROUPS], out, caption='Homeownership rate, percent. 2002 uses the value revised to 2000 Census controls; '
                 'Black and non-Hispanic White rates before 2003 use the older race categories.')


def eq_s06():
    rows = rows_of('scenarios-2030')
    out = []
    for r in rows:
        for f, n in FAMS:
            out.append([f'{r["key"]}. {r["name"]}', n, r[f], CLASS_WORD[r[f + '_class']], r[f + '_why'] or 'Same reasoning as scenario ii'])
    return table(['Scenario', 'Outcome family', 'Direction, atlas\'s words', 'Studio\'s reading', 'Why, atlas\'s words'], out,
                 caption='Eight scenarios, four outcome families')


def eq_s07():
    rs = rows_of('rcv-bans')
    return table(['State', 'Status', 'Enacted', 'Law', 'Scope, as the source describes it'],
                 [[r['name'], r['status'], date_words(r['enacted_date']) if r['enacted_date'] else '', r['measure'] or '', r['scope_note'] or '']
                  for r in rs], caption='State laws on ranked-choice voting, as of November 2026')


def eq_s08():
    rs = sorted(rows_of('rule-changes'), key=lambda r: (r['date'], r['key']))
    return table(['Record', 'Date', 'Where', 'Direction', 'Instrument', 'What changed'],
                 [[r['key'] + ('' if r['verified'] else ' (source not checked by the atlas)'), date_words(r['date']), r['jurisdiction'],
                   DIR_WORD[r['direction']], r['instrument'], r['rule']] for r in rs], caption='The repair log, 64 changes')


def eq_s09():
    rs = rows_of('history-events')
    return table(['Event', 'Date', 'Thread', 'What happened', 'Mechanism'],
                 [[r['key'], date_words(r['date']), r['thread_label'], r['title'], r['mechanism']] for r in rs], caption='24 documented events')


def eq_s10():
    rs = sorted(rows_of('claims-by-grade'), key=lambda r: (-r['documented'] / r['value'], r['key']))
    return table(['Question', 'Documented', 'Well supported', 'Plausible', 'Contested', 'All claims', 'Documented share'],
                 [[f'{r["key"]} {r["title"]}', r['documented'], r['well-supported'], r['plausible'], r['contested'], r['value'],
                   f'{100 * r["documented"] / r["value"]:.0f}%'] for r in rs], caption='Claims by evidence grade')


CSV_COLS = {
    'S01': ['key', 'group', 'measure', 'value'],
    'S02': ['key', 'year', 'measure', 'series_variant', 'comparable_with', 'percent', 'moe_pct', 'source_table'],
    'S03': ['key', 'value', 'away from voters', 'toward voters', 'voters kept existing rules', 'mixed', 'pending'],
    'S04': ['key', 'year', 'age_group', 'base', 'voted_pct'],
    'S05': ['key', 'year', 'group', 'race_definition', 'series_variant', 'rate_pct', 'moe_pct'],
    'S06': ['key', 'name', 'DQ', 'GE', 'EP', 'EQ', 'DQ_class', 'GE_class', 'EP_class', 'EQ_class'],
    'S07': ['key', 'name', 'status', 'scope', 'instrument', 'enacted_date', 'measure', 'scope_note'],
    'S08': ['key', 'date', 'jurisdiction', 'direction', 'instrument', 'instrument_group', 'rule', 'verified', 'source_url'],
    'S09': ['key', 'date', 'thread_label', 'title', 'mechanism', 'source_text'],
    'S10': ['key', 'title', 'documented', 'well-supported', 'plausible', 'contested', 'value'],
}


def csv_rows(sid):
    did = SPECS[sid]['dataset']
    rs = rows_of(did)
    if sid == 'S02':
        pass
    elif sid == 'S04':
        keep = {turnout(a, y)['key'] for a, _ in AGES for y in (2020, 2024)}
        rs = [r for r in rs if r['key'] in keep]
    elif sid == 'S05':
        keep = {r['key'] for g_, _ in HGROUPS for s in home_segments(g_) for r in s}
        rs = [r for r in rs if r['key'] in keep]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(CSV_COLS[sid])
    for r in rs:
        w.writerow([r.get(c, '') for c in CSV_COLS[sid]])
    return buf.getvalue()


# ------------------------------------------------------------------------------------------------ the ten modules' copy
def src_text(sid):
    s = DS[SPECS[sid]['dataset']]['source_line']
    return s[len('Source: '):] if s.startswith('Source: ') else s


RL = DS['rule-changes']
CODING_LINE = ("Directions are the atlas's own codes: a change counts toward voters when it widens who can vote or have a ballot counted, "
               "weighs votes more equally, opens the contest that decides the seat, limits or shows political money, strengthens an "
               "independent check, or adds automatic household security; away from voters means the reverse.")

META = {
    'S01': dict(gen=g_s01, kit='big_number()', table=eq_s01,
                title='The Senate fell 7 votes short of taking up a stock-trading ban that 88% of Democrats and 87% of Republicans favored in 2023.',
                measure='Registered voters who favored banning stock trading by members of Congress, percent, United States, May 2023; House and Senate votes on H.R. 7008, July and September 2026',
                index='Atlas sources N40, K1908, W035',
                notes=['Each chamber\'s bar holds every vote cast there: 430 in the House and 100 in the Senate. The 86% for all registered voters comes from the survey\'s own release.'],
                why='A big number answers yes at a glance; the party bars beside it show the two figures one point apart, and the votes show what Congress did three years later.'),
    'S02': dict(gen=g_s02, kit='line_events()', table=eq_s02,
                title='Child poverty under the Supplemental Poverty Measure fell to 5.1% in 2021, the year the expanded child tax credit paid out, and was 12.0% in 2022.',
                measure='Children under 18 below the poverty line, percent, United States, 2009 to 2025; Supplemental Poverty Measure in Charcoal, official measure in Stone',
                index='Census P60-290 Tables 3 and 8; atlas RL15, RL16',
                notes=['The Census Bureau describes a change between two years; it does not credit one policy with it.',
                       'Figures for 2019 to 2024 include the Bureau\'s August 2026 revision. The atlas prints the first-published 9.7%, 5.2% and 13.4% for 2020, 2021 and 2024; this table reads 9.6%, 5.1% and 13.5%.',
                       'In 2013, 2017 and 2019 the Bureau gives two estimates, one that joins the earlier years and one that joins the later years, so the lines break there. The official measure counts pretax money income and leaves out tax credits.'],
                why='A line shows the fall to 2021 and the climb back; the official measure in Stone shows what the supplemental measure counts, and the breaks show where the Census Bureau changed its method.'),
    'S03': dict(gen=g_s03, kit='ranked_bar()', table=eq_s03,
                title='State statutes moved the rules away from voters in 9 of 11 logged changes; ballot initiatives did so in none of 17.',
                measure='Rule changes in the atlas\'s repair log by how they were made, split by the atlas\'s direction code, United States, August 1965 to the November 3, 2026 ballot',
                index='Repair log RL01 to RL64',
                notes=[CODING_LINE,
                       'Five instruments with one change each are grouped: an agency rule, an executive action and an executive order as executive or agency action; a city ordinance and a council funding vote as local law or funding vote. The grouping is the studio\'s; the instruments are the atlas\'s.'],
                why='Seven instruments ranked by count answer who made the most changes; splitting each bar by the atlas\'s direction code shows which way each instrument moved the rules.'),
    'S04': dict(gen=g_s04, kit='dumbbell()', table=eq_s04,
                title='Reported turnout in 2024 ran from 47.7% of citizens 18 to 24 to 74.7% of those 65 and over; every group under 65 fell from 2020.',
                measure='Citizens who reported voting in the November presidential election, percent, by age, United States, 2020 and 2024; the scale starts at 40%',
                index='Census Table A-1',
                notes=['These are the shares of citizens who told the Census Bureau\'s November survey that they voted. Reported voting runs higher than counted ballots.'],
                why='Two dots per age group show the level and the change at once; printed values and the change in words carry the numbers without a grid.'),
    'S05': dict(gen=g_s05, kit='small_multiples()', table=eq_s05,
                title='The homeownership gap between non-Hispanic White and Black households was 29.6 points in 2025, wider than the 27.3 points of 2003.',
                measure='Owner households as a percent of all households in each group, by race and ethnicity of householder, United States, 1994 to 2025; one scale, starting at 20%',
                index='Census HVS Table 22',
                notes=['Race categories changed in 2003, so the Black and non-Hispanic White lines break there. 2002 uses the value the Census Bureau revised to 2000 Census controls.',
                       'The 2025 average leaves out October 2025, when no data were collected. The latest quarter, the third quarter of 2026, reads 75.1% for non-Hispanic White and 44.4% for Black householders.'],
                why='One panel per group on one scale lets a reader compare each group with the other three, which sit behind it in Stone.'),
    'S06': dict(gen=None, html=g_s06_html, kit='comparison_table()', table=eq_s06,
                title='Two of eight scenarios would move all four outcome families up by 2036: the federal package and capacity first.',
                measure='Direction each outcome family would take by 2036 if a scenario\'s assumptions hold, in the atlas\'s words, United States, from a 2026 baseline',
                index='Scenarios i to iv-e',
                notes=['Glyphs and tints are the studio\'s reading of the atlas\'s words, which print in every cell. Capacity first reaches "up" on economic performance through "same as scenario ii".',
                       'These are conditional directions with no forecast and no odds. The four families are read one at a time and never added together.'],
                why='A table keeps the atlas\'s words in every cell; a glyph and a tint let a reader scan the up and down moves across eight rows without red or blue.'),
    'S07': dict(gen=g_s07, kit='tile_map()', table=eq_s07,
                title='Nineteen states ban ranked-choice voting, 17 of them in every election, as of November 2026.',
                measure='State laws that prohibit ranked-choice voting, by scope and year enacted, 50 states and DC, as of November 2026',
                index='Atlas repair log RL47',
                notes=['Ballotpedia is a secondary source. The atlas cites the National Conference of State Legislatures, whose page refused an automated read; both list the same 19 states, as does the atlas\'s repair log row RL47.'],
                why='Equal tiles give every state the same weight and room for its code and the year of its ban; true shapes would hide the small eastern states.'),
    'S08': dict(gen=None, html=g_s08_html, kit='unit_ledger()', table=eq_s08,
                title='Seventeen of the 24 logged changes that moved rules away from voters came in 2025 and 2026.',
                measure='Each square is one dated change in the atlas\'s repair log, numbered by its record, by the atlas\'s direction code, United States, August 1965 to the November 3, 2026 ballot',
                index='Repair log RL01 to RL64',
                notes=[CODING_LINE + ' The split at January 1, 2025 is the studio\'s.'],
                coding=True,
                why='One square per record lets a reader count every change and find each one by number; two panels split at 2025 show when the changes away from voters came.'),
    'S09': dict(gen=g_s09, kit='timeline()', table=eq_s09,
                title='The atlas traces 24 documented rule changes on four threads, from the Fifteenth Amendment in 1870 to Trump v. Slaughter in 2026.',
                measure='Dated changes in the atlas\'s history, by thread, United States, February 3, 1870 to June 29, 2026',
                index='Events E01 to E24, studio keys',
                notes=['Every event is documented: each rests on a statute, ruling, constitutional text or official record. The keys E01 to E24 are the studio\'s, in date order. The list gives each event\'s lead name; the table gives the full entry, with the events the atlas pairs with it.'],
                why='Four lanes on one true time scale show when each thread changed; each dot carries its record key, and the list under the lane names every event in date order.'),
    'S10': dict(gen=g_s10, kit='evidence_mix()', table=eq_s10,
                title='The public record backs 74% of the atlas\'s 433 claims, from 96% for drinking water to 59% for algorithms.',
                measure='Share of each everyday question\'s claims by evidence grade, percent of claims, atlas claims register, United States, checked through October 15, 2026',
                index='Questions PW01 to PW16',
                notes=['Fills follow the atlas\'s evidence lines: solid for documented and well supported, dashed for plausible, dash-dot for contested. A claim\'s grade covers that claim, not the whole answer.'],
                why='A 100% bar per question compares the mix across questions of different sizes; sorting by the documented share puts the firmest answers first.'),
}
READOUT = {'S07': 'Point at a state to read its law. The table lists every state.',
           'S08': 'Point at a square to read its record. The table lists every change.',
           'S09': 'Point at a dot to read the event. The table lists every event.',
           'S10': 'The table lists every count.'}


# ------------------------------------------------------------------------------------------------ the module
def artboards(sid, uid, g, sizes):
    m = META[sid]
    out = []
    first_label = ''
    for art, W in sizes:
        body, H, defs, label = m['gen'](W, f'{uid}-{art}', g)
        first_label = first_label or label
        out.append(svg(uid, art, W, H, body, label, defs))
    return ''.join(out), first_label


def module(sid, view, ground, mode='panel', inst='', anat=False, red=True, hl=2, extra_cls='', sizes=None):
    m = META[sid]
    spec = SPECS[sid]
    did = spec['dataset']
    uid = f'{view}{inst}-{sid.lower()}'
    g = {'ground': ground, 'red': red}
    sm = (lambda L: f'<span class="slotmark" aria-hidden="true">{L}</span>') if anat else (lambda L: '')
    if m.get('html'):
        fig, alt = m['html'](uid, g), ''
    else:
        fig, alt = artboards(sid, uid, g, sizes or (ARTS if mode == 'panel' else [('s', 680)]))
    ev = spec['evidence']
    idx = f'<p class="idx">{esc(m["index"])}</p>'
    head = (f'<div class="slot sa" data-slot="A">{sm("A")}<p class="ev" data-role="evidence-label">{esc(ev)}</p>{idx}</div>'
            f'<div class="slot sb" data-slot="B">{sm("B")}<h{hl} class="mt" id="{uid}-t" data-role="title">{esc(m["title"])}</h{hl}></div>'
            f'<div class="slot sc" data-slot="C">{sm("C")}<p class="ms" data-role="measure">{esc(m["measure"])}</p></div>')
    notes = ''.join(f'<p>{esc(n)}</p>' for n in m['notes'])
    if m.get('coding'):
        notes += (f'<details class="cn"><summary>Read the atlas\'s full coding note</summary><p>{esc(RL["coding_note"])}</p></details>')
    src = (f'<div class="slot sg2" data-slot="G">{sm("G")}<p class="src" data-role="source"><span class="s1">Source: {esc(src_text(sid))}</span>'
           f'<span class="s2">Chart: Oath &amp; Action</span></p></div>')
    if mode == 'panel':
        has_svg = not m.get('html')
        dls = (f'<div class="dls"><span class="dlh">Download</span>'
               f'<button type="button" class="dl" data-dl="csv" data-for="{sid}" aria-label="Download the {sid} data as CSV">CSV</button>'
               + (f'<button type="button" class="dl" data-dl="svg" data-for="{sid}" aria-label="Download this chart as SVG">SVG</button>' if has_svg else '')
               + '</div>')
        ctl = (f'<div class="slot sd" data-slot="D">{sm("D")}<div class="ctl"><div class="sw" role="group" aria-label="Show {sid} as">'
               f'<button type="button" data-sw="c" aria-pressed="true" aria-controls="{uid}-pc">Chart</button>'
               f'<button type="button" data-sw="t" aria-pressed="false" aria-controls="{uid}-pt">Table</button></div>{dls}</div></div>')
        ro = f'<p class="readout" aria-hidden="true">{esc(READOUT[sid])}</p>' if sid in READOUT and sid != 'S10' else ''
        body = (f'<div class="slot se" data-slot="E">{sm("E")}<div class="pane pane-c" id="{uid}-pc">{fig}{ro}</div>'
                f'<div class="pane pane-t" id="{uid}-pt" hidden data-role="equivalent">'
                f'<p class="eqh">Every value in the chart, with its notes. The source line stays below.</p>{m["table"]()}</div></div>')
        return (f'<figure class="mod {extra_cls}" id="{uid}" data-spec="{sid}" data-dataset="{did}" data-evidence="{esc(ev)}" '
                f'aria-labelledby="{uid}-t">{head}{ctl}{body}<div class="slot sf" data-slot="F">{sm("F")}<div class="notes">{notes}</div></div>'
                f'{src}</figure>')
    # still: no controls, no readout; the alt text travels as the equivalent
    alt_txt = re.sub(r' The Table button lists every (value|change|event|state|count)\.$', '', alt or m['title'])
    alt_txt += ' Source: ' + src_text(sid)
    body = f'<div class="slot se" data-slot="E">{sm("E")}<div class="pane">{fig}</div></div>'
    still_note = '<p>Table and data: with the interactive version of this chart.</p>'
    return (f'<figure class="mod still {extra_cls}" id="{uid}" data-spec="{sid}" data-dataset="{did}" data-evidence="{esc(ev)}" '
            f'aria-labelledby="{uid}-t">{head}{body}<div class="slot sf" data-slot="F">{sm("F")}<div class="notes">{notes}{still_note}</div></div>'
            f'{src}<div class="alt" data-role="equivalent"><p class="alt-h">Alt text, sent with the image</p><p>{esc(alt_txt)}</p></div></figure>')


def strip(sid, size='Column module, 866 px; artboards 866, 560 and 328 px'):
    m, s = META[sid], SPECS[sid]
    return (f'<aside class="strip" aria-label="Studio note on {sid}"><p class="sn-h">Studio note, not chart copy</p>'
            f'<p class="sn-id">{sid} · {esc(s["form"])}</p>'
            f'<p><span class="k">Reader question.</span> {esc(s["reader_question"])}</p>'
            f'<p><span class="k">Why this form.</span> {esc(m["why"])}</p>'
            f'<p class="sn-kit"><span class="k">Kit.</span> Drawn by {esc(m["kit"])}. {esc(size)}.</p></aside>')


def spec_row(sid, view, ground, **kw):
    size = {'S06': 'Column module, 866 px; one HTML table that reflows under 640 px',
            'S08': 'Column module, 866 px; one HTML grid of 28 px units that stacks its two panels under 700 px'}.get(
        sid, 'Column module, 866 px; artboards 866, 560 and 328 px')
    return f'<div class="spec-row">{module(sid, view, ground, **kw)}{strip(sid, size)}</div>'


# ------------------------------------------------------------------------------------------------ identity
def wordmark(height, master, cls):
    src = (ROOT / 'work/build/assets/identity/wordmark' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    src = src.replace('<svg ', f'<svg class="{cls}" data-view="wordmark" width="{w:.0f}" height="{height}" role="img" '
                               f'aria-label="Oath &amp; Action" ', 1)
    return src


VIEWS = [('white', 'White'), ('newsprint', 'Newsprint'), ('dark', 'Charcoal'), ('social', 'Social card'), ('system', 'System')]
VIEW_GROUND = {'white': 'white', 'newsprint': 'newsprint', 'dark': 'charcoal', 'social': 'white', 'system': 'white'}


def masthead():
    tabs = ''.join(f'<li><a href="#{v}">{esc(t)}</a></li>' for v, t in VIEWS)
    return ('<a class="skip" href="#main">Skip to the charts</a><header class="mast"><div class="wrap mrow">'
            f'<a class="wm" href="#white" data-red="signature" aria-label="Oath &amp; Action, concept 03 first view">'
            f'{wordmark(24, "20261028_Wordmark-24px-Master.svg", "wm24")}{wordmark(16, "20261028_Wordmark-16px-Master.svg", "wm16")}</a>'
            '<p class="run">Chart system 03 · Instrument</p>'
            f'<nav class="tabs" aria-label="Views"><ul>{tabs}</ul></nav></div></header>')


# ------------------------------------------------------------------------------------------------ views
def view_white():
    links = [('newsprint', 'Newsprint', 'The same ten modules on the warm ground, from the same generators.'),
             ('dark', 'Charcoal', 'Two modules on the dark ground, with the dark palette.'),
             ('social', 'Social card', 'One module set as a 1080 by 1350 card.'),
             ('system', 'System', 'The kit on one sheet: slots, sizes, type, marks, codes, palettes and rules.')]
    lk = ''.join(f'<li><a href="#{v}"><span class="vl-t">{esc(t)}</span><span class="vl-d">{esc(d)}</span></a></li>' for v, t, d in links)
    rows = ''.join(spec_row(s, 'white', 'white') for s in ORDER)
    return (f'<section class="view g-white" data-view-root="white" aria-labelledby="h-white"><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system · Concept 03 · View 1 of 5, White</p>'
            '<h1 class="display" id="h-white">Instrument</h1>'
            '<p class="deck">Every chart here is a module with the same seven slots, in the same order, on the Signal Grid\'s 8 px rhythm. '
            'One generator per chart form draws each module at three widths, so a builder can make the next chart from the kit without asking. '
            'Atlas record numbers print as small index labels where they help a reader find the record, and texture or an open mark carries the '
            'second code after color, as the atlas\'s evidence lines do. The same module works as a still image and as a panel with a '
            'Chart and Table switch; the System view says which parts change.</p>'
            f'<nav class="vlinks" aria-label="Other views"><ul>{lk}</ul></nav>'
            '<p class="howto">Each chart sits in its module. The tinted panel beside it is the studio\'s note for reviewers and is not chart copy.</p>'
            f'</header><div class="specs">{rows}</div></div></section>')


def view_newsprint():
    rows = ''.join(spec_row(s, 'newsprint', 'newsprint') for s in ORDER)
    return (f'<section class="view g-news" data-view-root="newsprint" aria-labelledby="h-news" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">View 2 of 5 · Newsprint</p>'
            '<h1 class="headline" id="h-news">The same ten modules on Newsprint</h1>'
            '<p class="deck">The generators are the ones that drew the White view; only the ground and its tokens change. On Newsprint, Stone context '
            'measures 4.29:1 and Verdigris 3.37:1, the toward-voters fill stays at 5.01:1, and the one red mark in S01 takes a 1 px Charcoal keyline, '
            'because Pillar Red alone measures 2.96:1 here. The studio note panel turns White.</p>'
            f'</header><div class="specs">{rows}</div></div></section>')


def view_dark():
    dark_tokens = [('Named series and away from voters', '#DCD9D2', 'Newsprint'), ('Context and secondary text', '#A3A19C', 'Dim Newsprint'),
                   ('Toward voters', '#76978F', 'Verdigris, 30% toward Newsprint'), ('Middle level and quieter context', '#878A8F', 'Stone, 35% toward Newsprint'),
                   ('Well supported', '#A3A19C', 'Dim Newsprint'), ('Gridline, decorative', '#393C41', 'Stone, 45% toward Charcoal'),
                   ('The headline\'s point', '#E63946', 'Pillar Red')]
    items = ''.join(f'<li><span class="sw2" style="background:{h}"{" data-red=\"swatch\"" if h == "#E63946" else ""}></span>'
                    f'<span><strong>{esc(j)}.</strong> {esc(n)}, {h}, {contrast(h, "#121212"):.2f}:1</span></li>' for j, h, n in dark_tokens)
    rows = spec_row('S01', 'dark', 'charcoal') + spec_row('S10', 'dark', 'charcoal')
    return (f'<section class="view g-dark" data-view-root="dark" aria-labelledby="h-dark" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">View 3 of 5 · Charcoal</p>'
            '<h1 class="headline" id="h-dark">Two modules on Charcoal</h1>'
            '<p class="deck">The dark palette swaps roles, not meanings: Newsprint carries the named series, Dim Newsprint the context, and texture '
            'still carries the evidence grade. Text from 13 to 15 px sets one weight heavier. Lifted Prussian and lifted Verdigris sit only 0.022 '
            'apart in lightness here, so dark charts keep to two inks and label every mark.</p>'
            f'<ul class="dtok">{items}</ul><p class="dtn">Contrast measured against Charcoal, #121212.</p>'
            f'</header><div class="specs">{rows}</div></div></section>')


SOCIAL = {}


def social_card():
    sid = 'S01'
    m = META[sid]
    cw = 1080 - 2 * 64
    tl = len(wrap(m['title'], cw / 0.95, 50, 800, tight=True))  # Inter Tight at -0.03 em runs about 5% under the Inter estimate
    ml = len(wrap(m['measure'], cw, 22))
    sl = len(wrap('Source: ' + src_text(sid), cw, 20))
    avail = 1350 - 2 * 64 - 40 - 36 - 54 * tl - 14 - 30 * ml - 28 - 24 - 28 * sl - 24
    # the narrowest artboard that fills the card's width and still fits its height gives the largest type
    W0 = next((w for w in range(440, 640, 4) if g_s01(w, 'probe', {'ground': 'newsprint'})[1] * cw / w <= avail), 600)
    body, H, defs, label = g_s01(W0, 'social-s01-c', {'ground': 'newsprint', 'red': True})
    scale = round(min(cw / W0, avail / H), 3)
    SOCIAL['scale'], SOCIAL['w0'] = scale, W0
    art = (f'<svg class="art-c" data-view="social-s01-c" viewBox="0 0 {W0} {fmt(H)}" width="{fmt(W0 * scale)}" height="{fmt(H * scale)}" '
           f'role="img" aria-label="{esc(label)}" focusable="false">{body}</svg>')
    card = (f'<div class="card g-news"><div class="c-top">{wordmark(40, "20261028_Wordmark-Display-Master.svg", "wmd")}'
            f'<p class="c-ev" data-role="evidence-label">{esc(SPECS[sid]["evidence"])}</p></div>'
            f'<h2 class="c-t" data-role="title">{esc(m["title"])}</h2><p class="c-m" data-role="measure">{esc(m["measure"])}</p>'
            f'<div class="c-art">{art}</div><p class="c-s" data-role="source">Source: {esc(src_text(sid))}</p></div>')
    alt = re.sub(r' The Table button lists every value\.$', '', f'{m["title"]} {label}') + ' Source: ' + src_text(sid)
    return (f'<figure class="social" data-spec="{sid}" data-dataset="{SPECS[sid]["dataset"]}" data-evidence="{SPECS[sid]["evidence"]}" aria-label="Social card built from S01">'
            f'<div class="cardbox" role="region" tabindex="0" aria-label="Social card at true size, 1080 by 1350 pixels. Scroll inside the box to see all of it.">'
            f'<span data-red="signature" class="sigwrap">{card}</span></div>'
            f'<div class="alt" data-role="equivalent"><p class="alt-h">Alt text, posted with the card</p><p>{esc(alt)}</p></div></figure>')


def view_social():
    card_html = social_card()
    return (f'<section class="view g-white" data-view-root="social" aria-labelledby="h-social" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">View 4 of 5 · Social card</p>'
            '<h1 class="headline" id="h-social">S01 as a 1080 by 1350 card</h1>'
            f'<p class="deck">The card is the S01 module with its controls removed. big_number() draws a {SOCIAL["w0"]} px artboard and the card sets it at '
            f'{SOCIAL["scale"]:.2f} times, so the smallest chart label reads at {13 * SOCIAL["scale"]:.0f} px. The slots keep their order: evidence label, title, measure, '
            'figure, source. The wordmark comes from the display master, and the one red mark is the Senate shortfall the title names.</p>'
            f'</header><div class="socwrap">{card_html}<aside class="strip" aria-label="Studio note on the social card">'
            '<p class="sn-h">Studio note, not chart copy</p><p class="sn-id">Social card · built from S01</p>'
            '<p><span class="k">What changes.</span> The switch, the downloads and the readout drop. The title, measure, figure, notes and source stay. The table travels as the alt text.</p>'
            '<p><span class="k">Size.</span> 1080 by 1350 px, the portrait post for Instagram and LinkedIn; 64 px margins on the 8 px rhythm.</p>'
            '<p><span class="k">Kit.</span> social_card(spec) measures the title, measure and source, then asks the generator for the narrowest artboard that fills the card\'s 952 px width and still fits the height left over. A module whose scale would fall under 1.6 times needs a shorter title or a shorter artboard.</p>'
            '</aside></div></div></section>')


# ------------------------------------------------------------------------------------------------ the system sheet
def sys_section(n, title, body, lead=''):
    lead_html = f'<p class="lede">{lead}</p>' if lead else ''
    return f'<section class="ssec" aria-labelledby="sys-{n}"><h2 class="sh" id="sys-{n}"><span class="sn">{n:02d}</span> {esc(title)}</h2>{lead_html}{body}</section>'


SLOTS = [('A', 'Index', 'Evidence label at left; the atlas record index at right', 'Inter 700, 13/18, capitals, +0.06 em; index Inter 600, 13/18, tabular, Deep Stone', '2 px Charcoal rule, then 12'),
         ('B', 'Title', 'One sentence that states the finding, its verb matched to the grade', 'Inter Tight 800, 28/32, −0.025 em; 22/26 on phones', '8'),
         ('C', 'Measure', 'Measure, unit, place and period; says where a scale starts if not at zero', 'Inter 400, 15/22, Deep Stone', '8'),
         ('D', 'Controls', 'Chart and Table switch at left, downloads at right. Panel only', 'Inter 600, 14; 32 px targets, 44 on phones', '16'),
         ('E', 'Figure', 'One artboard at 866, 560 or 328 px with its notes inside the drawing; or the table', 'Labels Inter 600, 13; notes Inter 400, 13', '16'),
         ('F', 'Notes', 'Coding notes and qualifications a reader needs; the key only when labels cannot fit', 'Inter 400, 14/20', '16'),
         ('G', 'Source', 'Source line in section 15 order, credit at right; then a 1 px Stone rule', 'Inter 400, 13/18, Deep Stone', '12, then 16 below')]


def sys_anatomy():
    tbl = ''.join(f'<tr><th scope="row"><span class="slk">{a}</span> {esc(n)}</th><td>{esc(h)}</td><td>{esc(t)}</td><td>{esc(s)}</td></tr>'
                  for a, n, h, t, s in SLOTS)
    return (f'<div class="anat-grid"><div class="anat">{module("S03", "system", "white", inst="a", anat=True, hl=3)}</div>'
            f'<div class="anat-spec"><div class="tbl"><table class="st2"><caption class="vh">The seven slots</caption><thead><tr><th scope="col">Slot</th><th scope="col">Holds</th>'
            f'<th scope="col">Type</th><th scope="col">Space above, px</th></tr></thead><tbody>{tbl}</tbody></table></div>'
            '<p class="small">A slot never moves and never changes job. An empty slot closes up, except B, C, E and G, which every chart fills. '
            'The figure slot holds one artboard at a time: a container query picks 866 px when the module is that wide, 560 px from 560, and 328 px below, '
            'drawn to fill 328 to 358 px so labels never fall under 13 px.</p></div></div>')


def sys_sizes():
    rows = [('Column module', 866, '8 of 12 columns at 1440; the default for atlas pages and reports'),
            ('Still', 680, 'Substack and email body; exported at 2x'),
            ('Medium artboard', 560, 'Tablets and narrow windows'),
            ('Social card artboard', SOCIAL['w0'], f'Chosen by social_card() and set at {SOCIAL["scale"]:.2f}x to fill the 952 px content width of the 1080 by 1350 card'),
            ('Phone artboard', 328, 'Drawn at 328, shown at 328 to 358 for 360 and 390 px phones')]
    rows.sort(key=lambda r: -r[1])
    bars = ''.join(f'<li><span class="szb" style="width:{100 * w / 866:.2f}%"></span><span class="szl"><strong>{esc(n)}</strong>, {w} px. {esc(d)}</span></li>'
                   for n, w, d in rows)
    steps = ''.join(f'<li><span class="sp" style="width:{s}px;height:{s}px"></span><span>{s}</span></li>' for s in (4, 8, 12, 16, 24, 32, 48, 72))
    return (f'<div class="two-col"><div><h3 class="sh3">Widths</h3><ul class="sizes">{bars}</ul></div>'
            '<div><h3 class="sh3">Spacing</h3><p class="small">Every gap is a step of the Signal Grid\'s 8 px rhythm, with its 4 px half step. '
            f'Modules stack 72 px apart; slots sit 8 to 16 px apart; rows in a chart sit on 32 or 40 px.</p><ul class="steps">{steps}</ul></div></div>')


def sys_type():
    rows = [('Chart title', 'Inter Tight 800, 28/32, −0.025 em; 22/26 on phones', 'mt-s', 'Seventeen of the 24 changes came in 2025 and 2026.'),
            ('Evidence label', 'Inter 700, 13/18, capitals, +0.06 em', 'ev-s', 'Finding'),
            ('Measure line', 'Inter 400, 15/22, Deep Stone', 'ms-s', 'Rule changes by how they were made, United States, 1965 to 2026'),
            ('Big figure', 'Inter Tight 800, 96/96, tabular; 72 under 700 px', 'big-s', '86%'),
            ('Series label', 'Inter 600, 15/18', 'sl-s', 'Toward voters'),
            ('Data label', 'Inter 600, 13/16, tabular, true minus', 'dl-s', f'Down 3.7 points, {MINUS}3.7'),
            ('Index label', 'Inter 600, 13/16, tabular, Deep Stone', 'ix-s', 'RL07 · PW15 · E09'),
            ('Note in a drawing', 'Inter 400, 13/16, Deep Stone; the named record in Inter 600, Charcoal', 'nt-s', '9 of its 11 moved the rules away from voters'),
            ('Notes slot', 'Inter 400, 14/20', 'ns-s', 'The split at January 1, 2025 is the studio\'s.'),
            ('Source line', 'Inter 400, 13/18, Deep Stone', 'sr-s', 'Source: U.S. Census Bureau, Table A-1, United States. Retrieved November 6, 2026.')]
    items = ''.join(f'<li><p class="tr-n">{esc(n)}</p><p class="tr-sp">{esc(s)}</p><p class="{c}">{esc(t)}</p></li>' for n, s, c, t in rows)
    return (f'<ul class="ramp">{items}</ul><p class="small">Lora Italic sets quoted words inside a note and nothing else; no chart title or label uses a serif. '
            'On Charcoal, text from 13 to 15 px sets one weight heavier.</p>')


def mk(svgbody, w, h):
    return f'<svg class="mks" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true" focusable="false">{svgbody}</svg>'


def sys_marks():
    lines = [(1, 'Hairline: gridlines in Stone 70% toward the ground, leaders, rules, the bar track', 'grid'),
             (1.5, 'Context lines in small multiples; the open ring for an earlier year; the pending outline', 'l-ctx'),
             (2, 'Context series in a line chart; the 60-vote threshold; dumbbell connectors', 'l-ctx2'),
             (3, 'The series the title names, in Charcoal; the red point mark', 'l-ink'),
             (6, 'The lit selection in an interactive panel only', 'l-sel')]
    li = ''.join(f'<li>{mk(f"<path d=\"M2 10H118\" class=\"{c}\" style=\"stroke-width:{w}px\"/>", 120, 20)}<span><strong>{fmt(w)} px.</strong> {esc(d)}</span></li>'
                 for w, d, c in lines)
    shapes = [
        (mk('<rect x="2" y="2" width="28" height="28" class="f-tow"/><rect x="36" y="2" width="28" height="28" class="f-away"/>'
            '<rect x="70" y="2" width="28" height="28" class="f-kept"/><rect x="104" y="2" width="28" height="28" class="f-pend"/>', 136, 32),
         'Units: 28 px squares on a 32 px pitch, numbered in Inter 600 13 px. Fill or outline carries the second code.'),
        (mk('<rect x="2" y="4" width="160" height="24" class="f-away"/><rect x="2" y="36" width="110" height="24" class="f-tow"/>', 164, 64),
         'Ranked bars: 24 px tall on a 40 px pitch, a 16 px gap, counts inside when the segment is 18 px or wider. 100% bars: 18 px on a 32 px pitch.'),
        (mk('<line x1="8" y1="16" x2="70" y2="16" class="l-ctx2"/><circle cx="70" cy="16" r="6" class="f-ink"/><circle cx="8" cy="16" r="5" class="ring"/>'
            '<circle cx="104" cy="16" r="5" class="f-ink"/><circle cx="124" cy="16" r="4" class="f-ink"/>', 136, 32),
         'Dots: 6 px radius for the later year, a 5 px open ring for the earlier; 5 px on a timeline; 4 px on a line where a note points.'),
    ]
    sh = ''.join(f'<li>{s}<span>{esc(d)}</span></li>' for s, d in shapes)
    return f'<div class="two-col"><div><h3 class="sh3">Line weights</h3><ul class="mklist">{li}</ul></div><div><h3 class="sh3">Marks</h3><ul class="mklist">{sh}</ul></div></div>'


def sys_codes():
    dirs = ''.join(f'<li>{mk(dir_shape(2, 2, 28, 28, c), 32, 32)}<span><strong>{esc(w)}.</strong> {d}</span></li>' for (_, c, w), d in zip(DIRS, [
        'Charcoal fill. The named series when a title names it.', 'Verdigris strong fill: Verdigris 25% toward Charcoal in OKLab.', 'Stone light fill with a Stone outline.',
        'Split: both fills in one mark.', 'Open: a 1.5 px Charcoal outline on the ground, not yet decided.']))
    uid = 'sys-codes'
    grades = ''.join(f'<li>{mk(grade_rect(uid, gk, 2, 4, 40, 18), 44, 26)}<span><strong>{esc(w)}.</strong> {esc(gl[0].upper() + gl[1:])}. '
                     f'{d}</span></li>' for (gk, w, gl), d in zip(GRADES, ['Solid Charcoal.', 'Solid gray, a step lighter.',
                                                                            '2 px dashes, 8 on and 4 off, the atlas\'s plausible line.',
                                                                            'Dash-dot at 8, 3, 2 and 3, the atlas\'s contested line.']))
    gdefs = f'<svg width="0" height="0" class="vh" aria-hidden="true" focusable="false"><defs>{grade_defs(uid)}</defs></svg>'
    glyphs = ''.join(f'<li>{glyph(c, 20)}<span><strong>{esc(CLASS_WORD[c])}.</strong></span></li>' for c in CLASS_WORD)
    return (f'{gdefs}<div class="three-col"><div><h3 class="sh3">Direction code, repair log</h3><ul class="mklist">{dirs}</ul>'
            '<p class="small">Grayscale holds the order: Charcoal, Verdigris strong, Stone light, ground. Row position in S08 and segment order in S03 add a third code.</p></div>'
            f'<div><h3 class="sh3">Evidence code</h3><ul class="mklist">{grades}</ul><p class="small">Grades never take red, and hypothesis, the dotted line, has no fill: '
            'no claim in the register carries it.</p></div>'
            f'<div><h3 class="sh3">Direction glyphs, scenarios</h3><ul class="mklist gl-list">{glyphs}</ul><p class="small">Shape carries the direction; a Verdigris or Prussian tint '
            'carries the side, never red against blue. Party marks take neutral inks with the party\'s name printed on them, ordered by value or alphabet.</p></div></div>')


PAL = [('Ground', 'gr', 'White, Newsprint, Charcoal'), ('Named series, baseline, away from voters', 'ink', 'Charcoal; Newsprint on Charcoal'),
       ('Context', 'ctx', 'Stone; Dim Newsprint on Charcoal'), ('Secondary text', 'sec', 'Deep Stone; Dim Newsprint on Charcoal'),
       ('Toward voters, up glyph', 'tow', 'Verdigris 25% toward Charcoal; on Charcoal, Verdigris 30% toward Newsprint'),
       ('Middle level: some elections', 'some', 'Stone; on Charcoal, Stone 35% toward Newsprint'),
       ('Kept existing rules (values printed)', 'kept', 'Stone 55% toward the ground; on Charcoal, the gridline gray with an outline'),
       ('Well supported', 'g2', 'Charcoal 38% toward the ground; Dim Newsprint on Charcoal'),
       ('Up tint (words print in the cell)', 'vdl', 'Verdigris 55% toward the ground'), ('Down tint (words print in the cell)', 'prl', 'Prussian 62% toward the ground'),
       ('Down glyph', 'pr', 'Prussian; on Charcoal, Prussian 55% toward Newsprint'), ('Gridline, decorative', 'grid', 'Stone 70% toward the ground'),
       ('The headline\'s point', 'red', 'Pillar Red; 1 px Charcoal keyline on Newsprint'), ('Focus ring', 'focus', 'Verdigris; Newsprint on Charcoal')]


def sys_palettes():
    head = '<tr><th scope="col">Job</th>' + ''.join(f'<th scope="col">{n}</th>' for n in ('White', 'Newsprint', 'Charcoal')) + '</tr>'
    body = []
    for job, tok, name in PAL:
        cells = []
        for gname in ('white', 'newsprint', 'charcoal'):
            h = GROUNDS[gname][tok]
            gr = GROUNDS[gname]['gr']
            c = contrast(h, gr)
            red = ' data-red="swatch"' if h == '#E63946' else ''
            mark = '' if tok == 'gr' else f'{c:.2f}:1'
            cells.append(f'<td><span class="pal"><span class="sw3" style="background:{h};outline-color:{gr}"{red}></span>'
                         f'<span class="hx">{h}</span><span class="cr">{mark}</span></span></td>')
        body.append(f'<tr><th scope="row">{esc(job)}<span class="pn">{esc(name)}</span></th>{"".join(cells)}</tr>')
    return (f'<div class="tbl"><table class="st2 paltab"><caption class="vh">Chart palette with measured contrast against each ground</caption>'
            f'<thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'
            '<p class="small">Contrast is WCAG 2 against the ground, computed by the build script. Every tint is one of the palette lab\'s OKLab mixes of locked colors; the build script recovered each mix and prints it above. '
            'identity colors never change. Kept existing rules, the up and down tints and the gridline fall under 3:1 by design: each kept segment prints its count and '
            'carries a Stone outline, each tinted cell prints the atlas\'s words, and gridlines carry no meaning. Verdigris and Stone sit 0.05 apart in lightness, so no '
            'chart separates two categories by those two inks alone. Pillar Red appears in the table as a swatch, which Rule 05.3 does not count.</p>')


RULE_053 = ("The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge "
            "diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with the wordmark and never stands in "
            "for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single "
            "feature icon. In a row or a menu, icons go one color and only the current one keeps its red. Each view (one screen, card, slide or printed "
            "page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point "
            "the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A "
            "hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, "
            "Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian.")


def sys_red():
    url = next(s['url'] for s in DS['stock-trading-ban']['sources'] if s['id'] == 'W035')
    return (f'<blockquote class="rule"><p>{esc(RULE_053)}</p><footer>Rule 05.3, the red rule (D2-01)</footer></blockquote>'
            '<p class="body2">On a chart page each module counts as one view. Red never codes a series, a category, a scale, a party or a grade. It may mark the one point '
            'a title names, here the 7 votes the Senate fell short in S01, and only when no error or ask holds the view. Press the button to put an ask in this view: '
            'the ask takes the red, and the shortfall steps down to Charcoal at the same 3 px weight.</p>'
            f'<div class="askbar"><button type="button" class="tgl" aria-pressed="false" data-ask="system-r-s01">Put an ask in this view</button>'
            f'<span class="askwrap" id="ask-demo" hidden><a class="ask" href="{esc(url)}" data-red="working" data-red-job="ask">See how each senator voted</a>'
            '<span class="ill">Illustrative ask</span></span></div>'
            f'<div class="redmod">{module("S01", "system", "white", inst="-r", hl=3)}</div>')


def sys_rules():
    rules = [('Notes sit inside the drawing.', 'Inter 13 in Deep Stone, joined to the data by 1 px leaders; the named record in Inter 600, Charcoal. A note names the record, explains an odd encoding once, or gives a reader\'s scale.'),
             ('Label directly.', 'Labels sit on the mark or at its end. A key appears only when labels cannot fit, and it sits inside the drawing above the marks it explains.'),
             ('Write the unit once.', 'On the top tick or the first label: "100%", "17 changes", "Down 3.7 points". Other ticks stay bare.'),
             ('Numbers are tabular, and minus is the true minus.', f'{MINUS}3.7, never a hyphen.'),
             ('Scales are honest.', 'Bars start at zero. A line or dot scale may start elsewhere when the measure line says so. Small multiples share one scale. Missing years and method breaks stay open; the line never bridges them.'),
             ('Hover adds, never hides.', 'The readout under a chart repeats what the table holds. Every value is printed, in the notes or in the table.'),
             ('The source line goes under every chart.', 'In section 15 order: publisher, title or table, observation period, geography, date retrieved, qualification. Shorten by dropping words, never facts. The credit sits at the right.'),
             ('Index labels point at records.', 'RL07 is repair log row 7, PW15 is everyday question 15, E09 is the studio\'s key for the ninth history event. They print where they help a reader find the record, and nowhere for decoration.'),
             ('Illustrative items carry the word.', '"Illustrative data" or "Illustrative ask" sits beside the item, never in a footnote.')]
    return '<ol class="rules">' + ''.join(f'<li><strong>{esc(a)}</strong> {esc(b)}</li>' for a, b in rules) + '</ol>'


def sys_still():
    changes = [('Stays', 'Slots A, B, C, E, F and G in the same order and the same type; every printed number; every note; the source line.'),
               ('Drops', 'Slot D: the Chart and Table switch and the downloads. The hover readout.'),
               ('Adds', 'Alt text with every value, sent with the image, and a line in the notes that says where the table and data live.'),
               ('Changes', 'The figure uses a 680 px artboard drawn by the same generator and exports at 2x for Substack and email. Nothing moves between slots.')]
    lst = ''.join(f'<li><strong>{a}.</strong> {esc(b)}</li>' for a, b in changes)
    return (f'<div class="stillgrid"><div class="stillmod">{module("S03", "system", "white", mode="still", inst="-s", hl=3)}</div>'
            f'<div><h3 class="sh3">Still and panel</h3><ul class="chg">{lst}</ul><p class="small">This page offers CSV and SVG from the panel. A PNG still would come from '
            'an export step in the kit, which this concept does not build yet.</p></div></div>')


def sys_read():
    items = ['The small label above the title says what kind of claim the chart makes: a finding, an association, an estimate or an illustration.',
             'The title says what the chart found. The line under it names what was measured, where and when.',
             'The darkest mark is the one the title is about. Gray marks are there for comparison.',
             'A red mark, when a chart has one, points at the single thing the title names. It never stands for a party, a side or a group.',
             'Texture tells you how sure the atlas is. Solid means documented or well supported, dashes mean plausible, dash-dot means contested.',
             'Codes such as RL07 or PW15 are record numbers. Search the atlas for them to read the full record.',
             'Every chart has a Table button, and its source sits under it in both states. The downloads give you the same numbers.']
    return '<ol class="readers">' + ''.join(f'<li>{esc(i)}</li>' for i in items) + '</ol>'


def view_system():
    secs = [
        sys_section(1, 'The module', sys_anatomy(), 'One chart, every part named. The letters in the margin match the table.'),
        sys_section(2, 'Sizes and spacing', sys_sizes()),
        sys_section(3, 'Type ramp', sys_type(), 'Inter Tight for titles and big figures, Inter for everything a reader reads in or around a chart.'),
        sys_section(4, 'Marks', sys_marks()),
        sys_section(5, 'Codes after color', sys_codes(), 'Every code survives grayscale through a second channel: fill against outline, texture, shape or position.'),
        sys_section(6, 'Palettes, measured', sys_palettes()),
        sys_section(7, 'Red', sys_red()),
        sys_section(8, 'Annotation and source lines', sys_rules()),
        sys_section(9, 'Still image and interactive panel', sys_still()),
        sys_section(10, 'How to read our charts', sys_read(), 'For readers. This list can run on the atlas\'s help page and under a report\'s first chart.'),
    ]
    return (f'<section class="view g-white" data-view-root="system" aria-labelledby="h-sys" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">View 5 of 5 · System</p><h1 class="headline" id="h-sys">The kit on one sheet</h1>'
            '<p class="deck">What a builder needs to make the next chart without asking: the module\'s seven slots, its sizes, the type ramp, the marks, '
            'the codes, the palettes with measured contrast, the red rule, the annotation and source rules, and what changes between a still image and a panel.</p>'
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
:focus-visible{outline:2px solid var(--focus,#4A7C74);outline-offset:2px}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.skip{position:absolute;left:16px;top:-200px;z-index:200;padding:10px 14px;background:#FFFFFF;border:2px solid #121212;font:600 15px/1 Inter,sans-serif;color:#121212}
.skip:focus{top:12px}
/* masthead */
.mast{border-bottom:1px solid var(--rule)}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;color:var(--ink)}
.wm svg{--amp:#E63946}
.wm16{display:none}
.run{margin:0 0 0 48px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.tabs ul{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;min-height:44px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:var(--ink)}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 var(--ink)}
.tabs a:hover{text-decoration:underline}
/* view heads */
.view{padding-bottom:96px}
.vhead{padding:40px 0 8px;max-width:1080px}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;margin-left:-.04em}
.headline{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;text-wrap:balance}
.deck{margin:16px 0 0;font:400 19px/28px Inter,sans-serif;max-width:46em}
.lede{margin:8px 0 24px;font:400 17px/27px Inter,sans-serif;max-width:46em}
.howto{margin:16px 0 0;font:400 15px/23px Inter,sans-serif;color:var(--sec)}
.vlinks ul{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 24px;margin:24px 0 0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.vlinks a{display:grid;gap:2px;padding:10px 0 12px;min-height:44px;text-decoration:none}
.vlinks a:hover .vl-t{text-decoration:underline}
.vl-t{font:600 17px/24px Inter,sans-serif}.vl-d{font:400 14px/20px Inter,sans-serif;color:var(--sec)}
/* spec rows: module in 8 columns, the studio note in the last 3 */
.specs{display:grid;gap:72px;margin-top:48px}
.spec-row{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:var(--gut);align-items:start}
.spec-row>.mod{grid-column:1/span 8}
.spec-row>.strip{grid-column:10/span 3}
/* the module */
.mod{margin:0;border-top:2px solid var(--ink);border-bottom:1px solid var(--rule);padding-top:12px;container-type:inline-size;container-name:mod;min-width:0}
.slot{position:relative}
.sa{display:flex;justify-content:space-between;align-items:baseline;gap:4px 16px;flex-wrap:wrap}
.ev{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.idx{margin:0;font:600 13px/18px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.mt{margin:8px 0 0;font:800 28px/32px "Inter Tight",Inter,sans-serif;letter-spacing:-.025em;max-width:30em;text-wrap:balance}
.ms{margin:8px 0 0;font:400 15px/22px Inter,sans-serif;color:var(--sec);max-width:54em}
.ctl{display:flex;justify-content:space-between;align-items:center;gap:8px 16px;flex-wrap:wrap;margin-top:16px}
.sw{display:inline-flex;border:1px solid var(--ink)}
.sw button{min-height:32px;min-width:72px;padding:0 14px;border:0;background:var(--gr);color:var(--ink);font:600 14px/1 Inter,sans-serif;cursor:pointer}
.sw button+button{border-left:1px solid var(--ink)}
.sw button[aria-pressed="true"]{background:var(--ink);color:var(--gr)}
.dls{display:flex;gap:8px;align-items:center}
.dlh{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.dl{min-height:32px;min-width:48px;padding:0 10px;border:1px solid var(--ctx);background:var(--gr);color:var(--ink);font:600 14px/1 Inter,sans-serif;cursor:pointer}
.dl:hover,.sw button:hover{text-decoration:underline;text-underline-offset:3px}
.se{margin-top:16px}
.pane-c{min-height:20px}
.art{display:none;width:100%;height:auto;overflow:visible}
.art-n{display:block;max-width:358px}
@container mod (min-width:560px){.art-n{display:none}.art-m{display:block;max-width:560px}}
@container mod (min-width:866px){.art-m{display:none}.art-w{display:block;max-width:866px}}
.still .art{display:block;max-width:680px}
.readout{margin:12px 0 0;min-height:20px;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.sf{margin-top:16px}
.notes{font:400 14px/20px Inter,sans-serif;max-width:52em}
.notes p{margin:0 0 6px}
.cn summary{display:flex;align-items:center;min-height:32px;font:600 14px/20px Inter,sans-serif;cursor:pointer;text-decoration:underline;text-underline-offset:3px;width:max-content;max-width:100%}
.cn p{margin:4px 0 8px;padding-left:12px;border-left:2px solid var(--ink)}
.sg2{margin-top:12px;padding-bottom:16px}
.src{margin:0;display:flex;justify-content:space-between;gap:4px 24px;font:400 13px/18px Inter,sans-serif;color:var(--sec);overflow-wrap:anywhere}
.src .s1{max-width:52em}.src .s2{flex:none;white-space:nowrap}
.eqh{margin:0 0 8px;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.alt{margin:0 0 16px;padding:10px 12px;border-left:2px solid var(--ink);font:400 14px/20px Inter,sans-serif;max-width:52em}
.alt p{margin:0 0 4px}.alt-h{font-weight:600}
/* tables */
.tbl{max-width:100%}
table.eqt,table.st2{width:100%;border-collapse:collapse;font:400 14px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
.eqt caption{text-align:left;font:600 14px/20px Inter,sans-serif;padding-bottom:6px}
.eqt th,.eqt td,.st2 th,.st2 td{border-top:1px solid var(--grid);padding:6px 12px 6px 0;text-align:left;vertical-align:top}
.eqt thead th,.st2 thead th{border-top:1px solid var(--ink);font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.eqt tbody th{font-weight:600}
.tl{display:none}
/* S06 comparison table */
.sg-kh{margin:0 0 6px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.sg-key{display:flex;flex-wrap:wrap;gap:4px 18px;margin:0 0 12px;padding:0;list-style:none;font:400 13px/18px Inter,sans-serif}
.sg-key li{display:inline-flex;gap:6px;align-items:center}
.sgt{width:100%;border-collapse:collapse;table-layout:fixed;font:400 14px/19px Inter,sans-serif}
.sgt thead th{text-align:left;vertical-align:bottom;padding:0 8px 6px;border-bottom:1px solid var(--ink);font:600 13px/17px Inter,sans-serif}
.sgt thead th:first-child{width:30%;padding-left:0}
.sgt tbody th{text-align:left;vertical-align:top;padding:8px 8px 8px 0;font:600 14px/19px Inter,sans-serif;border-bottom:1px solid var(--grid)}
.sgt td{vertical-align:top;padding:8px;border-bottom:1px solid var(--grid);border-left:2px solid var(--gr)}
.sid{display:inline-block;min-width:34px;font:600 13px/19px Inter,sans-serif;color:var(--sec)}
.cw{display:flex;gap:6px;align-items:flex-start}.cw .gl{flex:none;margin-top:1px}
.fam-l{display:none}
.c-up{background:var(--vdl)}.c-sup{background:var(--vdxl)}.c-fod{background:var(--prxl)}.c-down{background:var(--prl)}
.gl .gf-up{fill:var(--tow)}.gl .gs-up{fill:none;stroke:var(--tow);stroke-width:1.6}
.gl .gf-down{fill:var(--pr)}.gl .gs-down{fill:none;stroke:var(--pr);stroke-width:1.6}
.gl .gf-flat{fill:var(--ctx)}
@container mod (max-width:639px){
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
/* S08 unit grid */
.ul{display:grid;grid-template-columns:160px minmax(0,1fr) minmax(0,1fr);column-gap:0}
.ul p{margin:0}
.ul-ph{padding:0 0 10px 16px}.ul-ph:not(.b){padding-left:0;padding-right:16px}
.ul-pt{font:600 15px/20px Inter,sans-serif}.ul-pn{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.ul-dl,.ul-cell{border-top:1px solid var(--grid);padding:10px 16px 12px 0}
.ul-cell.b,.ul-ph.b{border-left:1px solid var(--grid);padding-left:16px}
.ul-dw{font:600 15px/20px Inter,sans-serif}.ul-dn{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.ul-cw{display:none;font:600 13px/18px Inter,sans-serif;margin-bottom:6px}
.ul-us{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.u{display:block;flex:none;overflow:visible}
.ul-c{margin-left:4px;font:700 15px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
.ul-none{font:400 13px/18px Inter,sans-serif;color:var(--sec);min-height:28px;display:inline-flex;align-items:center}
@container mod (max-width:699px){
 .ul{display:flex;flex-direction:column}
 .ul-h0,.ul-dl{display:none}
 .ul-ph,.ul-cell{order:var(--o)}
 .ul-ph,.ul-ph:not(.b),.ul-ph.b,.ul-cell,.ul-cell.b{border-left:0;padding-left:0;padding-right:0}
 .ul-ph{border-top:1px solid var(--ink);padding-top:8px;margin-top:8px}
 .ul-ph.b{margin-top:20px}
 .ul-cell{padding:8px 0 10px}
 .ul-cw{display:block}
}
/* studio strip: on the other ground, so nobody reads it as chart copy */
.strip{background:var(--alt);padding:16px 16px 8px;font:400 14px/20px Inter,sans-serif;color:var(--ink)}
.g-dark .strip{border:1px solid var(--ctx)}
.strip p{margin:0 0 10px}
.sn-h{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.sn-id{font:800 20px/24px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em}
.strip .k{font-weight:600}
/* SVG chart styles */
svg text{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums}
.x13{font-size:13px;font-weight:400;fill:var(--sec)}
.x13b{font-size:13px;font-weight:600;fill:var(--ink)}
.x13s{font-size:13px;font-weight:600;fill:var(--sec)}
.x14{font-size:14px;font-weight:400;fill:var(--ink)}
.x15{font-size:15px;font-weight:400;fill:var(--ink)}
.x15b{font-size:15px;font-weight:600;fill:var(--ink)}
.x15k{font-size:15px;font-weight:700;fill:var(--ink)}
.xin{font-size:13px;font-weight:600;fill:var(--on-away)}
.xint{font-size:13px;font-weight:600;fill:var(--on-tow)}
.xins{font-size:13px;font-weight:600;fill:var(--on-some)}
.xbig{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;letter-spacing:-.03em;fill:var(--ink)}
.g-dark .x13,.g-dark .x15,.g-dark .x14{font-weight:500}
.grid{stroke:var(--grid);stroke-width:1}
.base{stroke:var(--ink);stroke-width:1}
.lane{stroke:var(--ctx);stroke-width:1}
.lead{stroke:var(--ctx);stroke-width:1;fill:none}
.sep{stroke:var(--gr);stroke-width:2}
.track{fill:none;stroke:var(--grid);stroke-width:1}
.tick2{stroke:var(--ink);stroke-width:2}
.f-ink{fill:var(--ink)}.f-ctx{fill:var(--ctx)}.f-g2{fill:var(--g2)}
.f-away{fill:var(--away)}.f-tow{fill:var(--tow)}
.f-kept{fill:var(--kept);stroke:var(--ctx);stroke-width:1}
.f-pend{fill:var(--gr);stroke:var(--ink);stroke-width:1.5}
.f-some{fill:var(--some)}
.f-none{fill:var(--gr);stroke:var(--ctx);stroke-width:1}
.f-tex{stroke:var(--ink);stroke-width:1}
.pt{stroke:var(--ink);stroke-width:2;fill:none}
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
/* social */
.socwrap{display:grid;grid-template-columns:minmax(0,1fr);gap:24px;margin-top:32px;align-items:start}
.socwrap>.strip{max-width:866px}
.social{margin:0;min-width:0}
.cardbox{overflow:auto;width:max-content;max-width:100%;border:1px solid var(--rule)}
.sigwrap{display:block;width:1080px}
.card{width:1080px;height:1350px;padding:64px;display:flex;flex-direction:column;overflow:hidden}
.c-top{display:flex;justify-content:space-between;align-items:center;height:40px;color:#121212}
.wmd{--amp:#E63946;display:block}
.c-ev{margin:0;font:700 24px/32px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#121212}
.c-t{margin:36px 0 0;font:800 50px/54px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;color:#121212}
.c-m{margin:14px 0 0;font:400 22px/30px Inter,sans-serif;color:#4E535B}
.c-art{margin-top:28px}
.c-art svg{display:block}
.c-s{margin:auto 0 0;padding-top:24px;font:400 20px/28px Inter,sans-serif;color:#4E535B}
/* system sheet */
.ssec{margin-top:72px;padding-top:16px;border-top:2px solid var(--ink)}
.sh{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em}
.sh .sn{color:var(--sec)}
.sh3{margin:0 0 12px;font:800 22px/26px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em}
.small{font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:52em}
.body2{font:400 17px/27px Inter,sans-serif;max-width:46em}
.anat-grid{display:grid;grid-template-columns:minmax(0,914px);gap:32px;align-items:start;margin-top:8px}
.anat{padding-left:48px}
.anat .slot{border-left:0}
.slotmark{position:absolute;left:-48px;top:0;display:flex;align-items:center;justify-content:center;width:24px;height:24px;background:#121212;color:#FFFFFF;font:700 13px/1 Inter,sans-serif}
.anat .slot::before{content:"";position:absolute;left:-14px;top:2px;bottom:2px;border-left:1px solid var(--ctx)}
.slk{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#121212;color:#FFFFFF;font:700 13px/1 Inter,sans-serif;margin-right:6px}
.st2 tbody th{font-weight:600;white-space:nowrap}
.two-col{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;margin-top:8px}
.three-col{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;margin-top:8px}
.sizes{margin:0;padding:0;list-style:none}
.sizes li{padding:8px 0 10px;border-top:1px solid var(--grid)}
.szb{display:block;height:16px;background:#121212;margin-bottom:6px}
.szl{font:400 14px/20px Inter,sans-serif}
.steps{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;margin:16px 0 0;padding:0;list-style:none}
.steps li{display:grid;justify-items:center;gap:6px;font:600 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums}
.sp{display:block;background:#121212}
.ramp{margin:0;padding:0;list-style:none}
.ramp li{display:grid;grid-template-columns:200px 300px minmax(0,1fr);gap:16px;align-items:baseline;padding:12px 0;border-top:1px solid var(--grid)}
.ramp p{margin:0}
.tr-n{font:600 15px/22px Inter,sans-serif}.tr-sp{font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.mt-s{font:800 28px/32px "Inter Tight",Inter,sans-serif;letter-spacing:-.025em}
.ev-s{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.ms-s{font:400 15px/22px Inter,sans-serif;color:var(--sec)}
.big-s{font:800 96px/96px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.sl-s{font:600 15px/18px Inter,sans-serif}
.dl-s{font:600 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums}
.ix-s{font:600 13px/16px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.nt-s{font:400 13px/16px Inter,sans-serif;color:var(--sec)}
.ns-s{font:400 14px/20px Inter,sans-serif}
.sr-s{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.mklist{margin:0;padding:0;list-style:none}
.mklist li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;align-items:center;padding:10px 0;border-top:1px solid var(--grid);font:400 14px/20px Inter,sans-serif}
.mks{display:block;overflow:visible}
.gl-list li{grid-template-columns:20px minmax(0,1fr)}
.paltab td,.paltab th{vertical-align:middle}
.pal{display:inline-flex;gap:8px;align-items:center;white-space:nowrap}
.sw3{display:inline-block;width:28px;height:20px;outline:1px solid;outline-offset:0;box-shadow:inset 0 0 0 1px rgba(93,99,109,.5)}
.hx{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.cr{font:600 14px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
.pn{display:block;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.rule{margin:8px 0 24px;padding:4px 0 4px 16px;border-left:2px solid var(--ink);max-width:60em;font:400 15px/23px Inter,sans-serif}
.rule p{margin:0 0 8px}.rule footer{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.askbar{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;margin:16px 0 24px}
.tgl{min-height:40px;padding:0 16px;border:1.5px solid var(--ink);background:var(--gr);color:var(--ink);font:600 15px/1 Inter,sans-serif;cursor:pointer}
.tgl[aria-pressed="true"]{background:var(--ink);color:var(--gr)}
.askwrap{display:inline-flex;gap:12px;align-items:center}
.ask{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;background:#E63946;color:#FFFFFF;font:700 19px/1 Inter,sans-serif;text-decoration:none}
.ill{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.redmod{max-width:866px}
.rules,.readers{margin:8px 0 0;padding-left:24px;max-width:60em;font:400 16px/25px Inter,sans-serif}
.rules li,.readers li{margin-bottom:10px}
.stillgrid{display:grid;grid-template-columns:minmax(0,680px) minmax(0,1fr);gap:40px;align-items:start;margin-top:8px}
.chg{margin:0 0 12px;padding-left:20px;font:400 15px/23px Inter,sans-serif}.chg li{margin-bottom:8px}
.dtok{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 24px;margin:20px 0 0;padding:0;list-style:none;font:500 14px/20px Inter,sans-serif}
.dtok li{display:flex;gap:10px;align-items:center}
.sw2{flex:none;width:28px;height:18px;box-shadow:inset 0 0 0 1px #878A8F}
.dtn{margin:8px 0 0;font:500 13px/18px Inter,sans-serif;color:var(--sec)}
/* page widths */
@media (max-width:1299.98px){
 .spec-row>.mod,.spec-row>.strip{grid-column:1/-1}
 .spec-row>.strip{max-width:866px;margin-top:16px}
 .anat-grid,.stillgrid{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:1099.98px){
 .socwrap{grid-template-columns:minmax(0,1fr)}
 .three-col{grid-template-columns:minmax(0,1fr)}
 .ramp li{grid-template-columns:minmax(0,1fr);gap:4px}
}
@media (max-width:899.98px){
 .wrap{padding:0 16px}
 .mrow{grid-template-columns:1fr;gap:8px;padding-top:16px}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .headline,.sh{font-size:30px;line-height:34px}
 .deck{font-size:17px;line-height:25px}
 .vlinks ul{grid-template-columns:minmax(0,1fr)}
 .specs{gap:56px;margin-top:32px}
 .mt{font-size:22px;line-height:26px}
 .sw button,.dl,.cn summary{min-height:44px}
 .src{flex-direction:column}
 .two-col{grid-template-columns:minmax(0,1fr)}
 .anat{padding-left:0}
 .slotmark,.anat .slot::before{display:none}
 .dtok{grid-template-columns:minmax(0,1fr)}
 table.st2,table.st2 tbody,table.st2 tr,table.st2 th,table.st2 td{display:block;width:auto}
 table.st2 thead{display:none}
 table.st2 tr{border-top:1px solid var(--ink);padding:6px 0}
 table.st2 th,table.st2 td{border:0;padding:2px 0}
 .st2 tbody th{white-space:normal}
}
"""

JS = r"""
(function(){
  var views=[].slice.call(document.querySelectorAll('[data-view-root]'));
  var ground={white:'g-white',newsprint:'g-news',dark:'g-dark',social:'g-white',system:'g-white'};
  var current=null;
  function show(first){
    var v=location.hash.slice(1);
    var known=views.some(function(e){return e.getAttribute('data-view-root')===v;});
    if(!known){ if(current&&!first) return; v='white'; }
    current=v;
    views.forEach(function(e){ e.hidden = e.getAttribute('data-view-root')!==v; });
    document.body.className=ground[v];
    [].forEach.call(document.querySelectorAll('.tabs a'),function(a){
      if(a.getAttribute('href')==='#'+v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    if(!first) window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',function(){show(false);});
  show(true);
  function save(name,type,text){
    var b=new Blob([text],{type:type}); var a=document.createElement('a');
    a.href=URL.createObjectURL(b); a.download=name; document.body.appendChild(a); a.click();
    setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();},800);
  }
  var P=['fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','font-family','font-size','font-weight','letter-spacing','font-variant-numeric','text-anchor','paint-order'];
  function svgText(s){
    var c=s.cloneNode(true), src=[s].concat([].slice.call(s.querySelectorAll('*'))), dst=[c].concat([].slice.call(c.querySelectorAll('*')));
    src.forEach(function(el,i){ var cs=getComputedStyle(el); P.forEach(function(p){ var v=cs.getPropertyValue(p); if(v) dst[i].style.setProperty(p,v); }); });
    c.setAttribute('xmlns','http://www.w3.org/2000/svg');
    var bg=document.createElementNS('http://www.w3.org/2000/svg','rect');
    bg.setAttribute('width','100%'); bg.setAttribute('height','100%');
    bg.setAttribute('fill',getComputedStyle(s).getPropertyValue('--gr').trim()||'#FFFFFF');
    c.insertBefore(bg,c.firstChild);
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
    var d=e.target.closest('[data-dl]');
    if(d){
      var sid=d.getAttribute('data-for'), kind=d.getAttribute('data-dl'), mod=d.closest('.mod');
      if(kind==='csv'){ save(sid+'-data.csv','text/csv;charset=utf-8',JSON.parse(document.getElementById('csv-'+sid).textContent)); }
      else{
        var arts=[].slice.call(mod.querySelectorAll('svg.art')).filter(function(s){return s.getBoundingClientRect().width>0;});
        if(arts.length) save(sid+'-chart.svg','image/svg+xml',svgText(arts[0]));
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
    csvs = ''.join(f'<script type="application/json" id="csv-{s}">{json.dumps(csv_rows(s)).replace("</", "<\\/")}</script>' for s in ORDER)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta name="chart-views" content="white newsprint dark social system">'
            '<title>Chart system 03, Instrument</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{ground_css()}{CSS}</style></head><body class="g-white">'
            f'{masthead()}<main id="main" tabindex="-1">{view_white()}{view_newsprint()}{view_dark()}{view_social()}{view_system()}</main>'
            f'{csvs}<script>{JS}</script></body></html>')
    if '—' in page:
        raise SystemExit('em dash in page')
    OUT.write_text(page, encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)} ({len(page) // 1024} KB)')


if __name__ == '__main__':
    build()
