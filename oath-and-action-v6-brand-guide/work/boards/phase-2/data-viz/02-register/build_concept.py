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
            'tow': LOCK['verdigris'], 'awy': LOCK['prussian'],
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
            'awy': mix(LOCK['prussian'], LOCK['newsprint'], 0.66),    # Prussian lifted 66% toward Newsprint
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
FONTDIR = pathlib.Path('/usr/share/fonts/opentype/inter')
_FONTS = {}


def _font(weight):
    name = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[weight]
    if weight not in _FONTS:
        _FONTS[weight] = ImageFont.truetype(str(FONTDIR / f'Inter-{name}.otf'), 200)
    return _FONTS[weight]


def tw(text, size=13, weight=400):
    return _font(weight).getlength(text) * size / 200 * 1.03   # 3% margin for the web build of Inter


def wrap(text, width, size=13, weight=400):
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


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def txt(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}{extra}>{s}</text>'


def lines(x, y, rows_, cls, lh, anchor='start'):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    t = ''.join(f'<tspan x="{f(x)}" dy="{0 if i == 0 else lh}">{e(r)}</tspan>' for i, r in enumerate(rows_))
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}"{a}>{t}</text>'


def svg(W, H, view, label, body, cls='ab'):
    return (f'<svg class="{cls}" data-view="{view}" viewBox="0 0 {f(W)} {f(H)}" width="{f(W)}" height="{f(H)}" '
            f'role="img" aria-label="{e(label)}" style="--abw:{f(W)}px">{body}</svg>')


# ------------------------------------------------------------------------------------------------ the frame
def source_text(did):
    s = DS[did]['source_line']
    return s if s.startswith('Source:') else 'Source: ' + s


def figure(sid, uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls=''):
    if uid.startswith('system-'):
        return anat_figure(sid, uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls)
    sp = SPEC[sid]
    ds = DS[sp['dataset']]
    kind = ds['evidence']
    nts = ''.join(f'<li>{n}</li>' for n in notes)
    return (f'<figure class="fig {extra_cls}" data-spec="{sid}" data-dataset="{sp["dataset"]}" data-evidence="{kind}" '
            f'aria-labelledby="{uid}-t">'
            f'<div class="fhead"><p class="elab" data-role="evidence-label">{kind} <span class="gr">· {e(grade_words)}</span></p>'
            f'<h3 class="ftitle" data-role="title" id="{uid}-t">{e(title)}</h3>'
            f'<p class="fmeasure" data-role="measure">{e(measure)}</p></div>'
            f'<div class="fbody">{body}</div>'
            + (f'<ol class="fnotes" aria-label="Notes">{nts}</ol>' if notes else '')
            + f'<p class="fsrc" data-role="source">{e(source)}</p>'
            f'<details class="feq" data-role="equivalent"><summary>Show the table</summary><div class="eqb">{equivalent}</div></details>'
            '</figure>')


def anat_figure(sid, uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls=''):
    """The same figure with the anatomy numbers of the system sheet on its parts."""
    h = figure(sid, 'anat-' + uid, title, measure, body, notes, source, equivalent, grade_words, extra_cls)
    h = h.replace('id="anat-', 'id="').replace('aria-labelledby="anat-', 'aria-labelledby="')
    for old, num in [('<figure class="fig', 1), ('<p class="elab"', 2), ('<h3 class="ftitle"', 3), ('<p class="fmeasure"', 4),
                     ('<div class="fbody"', 5), ('<span class="rnote"', 6), ('<ol class="fnotes"', 7), ('<p class="fsrc"', 8),
                     ('<details class="feq"', 9)]:
        assert old in h, old
        h = h.replace(old, old + f' data-anat="{num}"', 1)
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
    """A register table. cols: (label, getter, kind) where kind is 'h' (row header), 'n' (number) or 't' (text).
    getter returns (display_html, sort_value). Numbers sit right-aligned in tabular figures."""
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
            if kind == 'h':
                cells.append(f'<th scope="row" data-label="{e(plain)}"{sva}>{disp}</th>')
            else:
                c = ' class="n"' if kind == 'n' else ''
                cells.append(f'<td{c} data-label="{e(plain)}"{sva}>{disp}</td>')
        body.append('<tr>' + ''.join(cells) + '</tr>')
    return (f'<div class="tw"><table class="{cls}" id="{uid}"><caption>{e(caption)}</caption>'
            f'<thead><tr>{"".join(head)}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def eq_extra(notes_plain, source):
    """What a sighted reader gets beyond the table: the notes in the drawing and the source."""
    return ('<div class="eqn"><p class="eqh">Notes in the drawing</p><ul>' + ''.join(f'<li>{e(n)}</li>' for n in notes_plain)
            + f'</ul><p class="eqh">Source</p><p>{e(source)}</p></div>')


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

    def prow(r, big=False):
        party = r['group']
        return (f'<div class="prow" data-party="{e(party)}"><span class="pn">{e(party)}</span>'
                f'<span class="ptrk" aria-hidden="true"><span class="pbar" data-key="{r["key"]}" data-value="{r["value"]}" '
                f'data-mark="bar" data-axis="x" style="width:{r["value"]}%"></span></span>'
                f'<span class="pv"><span data-key="{r["key"]}" data-value="{r["value"]}" data-mark="label">{r["value"]}</span>%</span></div>')
    allr = R['support-all']
    big = (f'<div class="s01-big"><p class="bign"><span data-key="support-all" data-value="{allr["value"]}" data-mark="label">'
           f'{allr["value"]}</span><span class="pc">%</span></p>'
           f'<p class="bigc">of registered voters favored a ban on stock trading by members of Congress</p></div>')
    reg = ('<div class="s01-reg"><p class="regh">By party, in one ink, highest first</p>' + ''.join(prow(p) for p in parties)
           + '<p class="scale"><span>0</span><span>100%</span></p></div>')
    hy, hn = R['house-yes']['value'], R['house-no']['value']
    sy, sn, need = R['senate-yes']['value'], R['senate-no']['value'], R['senate-needed']['value']
    short = need - sy
    votes = ('<div class="tw"><table class="reg s01v"><caption>What Congress did next</caption><thead><tr>'
             '<th scope="col">Vote</th><th scope="col">Date</th><th scope="col" class="n">For</th>'
             '<th scope="col" class="n">Against</th><th scope="col">Result</th></tr></thead><tbody>'
             f'<tr><th scope="row" data-label="Vote">House, passage of H.R. 7008</th><td data-label="Date">July 22, 2026</td>'
             f'<td class="n" data-label="For"><span data-key="house-yes" data-value="{hy}" data-mark="label">{hy}</span></td>'
             f'<td class="n" data-label="Against"><span data-key="house-no" data-value="{hn}" data-mark="label">{hn}</span></td>'
             '<td data-label="Result">Passed</td></tr>'
             f'<tr><th scope="row" data-label="Vote">Senate, cloture on the motion to proceed</th><td data-label="Date">September 30, 2026</td>'
             f'<td class="n" data-label="For"><span data-key="senate-yes" data-value="{sy}" data-mark="label">{sy}</span></td>'
             f'<td class="n" data-label="Against"><span data-key="senate-no" data-value="{sn}" data-mark="label">{sn}</span></td>'
             f'<td data-label="Result">Fell {WORDS[short]} short of the <span data-key="senate-needed" data-value="{need}" '
             f'data-mark="label">{need}</span> votes needed</td></tr></tbody></table></div>')
    notes = ['The survey came three years before both votes.',
             'Cloture is the Senate vote that ends debate. Taking up this bill needed three-fifths of the Senate, 60 votes.',
             'Both parties are drawn in the same ink and ordered by value.']
    body = f'<div class="s01">{big}{reg}</div>{votes}'
    src = source_text('stock-trading-ban')
    eq = table([('Group or vote', lambda r: (e(r['group']), r['group']), 'h'), ('Measure', lambda r: (e(r['measure']), r['measure']), 't'),
                ('Value', lambda r: (num(r['value']), r['value']), 'n')], rows('stock-trading-ban'),
               'Every row of the stock-trading dataset', f'{uid}-eq') + eq_extra(notes, src)
    if card:
        return s01_card(uid, title, measure, parties, allr, src, eq, hy, hn, sy, sn, need)
    return figure('S01', uid, title, measure, body, [e(n) for n in notes], src, eq, 'documented record')


def s01_card(uid, title, measure, parties, allr, src, eq, hy, hn, sy, sn, need):
    rows_ = ''.join(
        f'<div class="crow" data-party="{e(p["group"])}"><span class="cn">{e(p["group"])}</span>'
        f'<span class="ctrk" aria-hidden="true"><span class="cbar" data-key="{p["key"]}" data-value="{p["value"]}" data-mark="bar" '
        f'data-axis="x" style="width:{p["value"]}%"></span></span>'
        f'<span class="cv"><span data-key="{p["key"]}" data-value="{p["value"]}" data-mark="label">{p["value"]}</span>%</span></div>'
        for p in parties)
    allrow = (f'<div class="crow all"><span class="cn">All registered voters</span><span class="ctrk" aria-hidden="true">'
              f'<span class="cbar" data-key="support-all" data-value="{allr["value"]}" data-mark="bar" data-axis="x" style="width:{allr["value"]}%"></span></span>'
              f'<span class="cv"><span data-key="support-all" data-value="{allr["value"]}" data-mark="label">{allr["value"]}</span>%</span></div>')
    ctx = (f'<p class="cctx">The House passed a ban <span data-key="house-yes" data-value="{hy}" data-mark="label">{hy}</span> to '
           f'<span data-key="house-no" data-value="{hn}" data-mark="label">{hn}</span> on July 22, 2026. On September 30 the Senate '
           f'voted <span data-key="senate-yes" data-value="{sy}" data-mark="label">{sy}</span> to '
           f'<span data-key="senate-no" data-value="{sn}" data-mark="label">{sn}</span> to take it up, short of the '
           f'<span data-key="senate-needed" data-value="{need}" data-mark="label">{need}</span> votes it needed.</p>')
    card = (f'<div class="card g-news">'
            f'<p class="celab" data-role="evidence-label">Finding <span>· documented record</span></p>'
            f'<h3 class="ctitle" data-role="title" id="{uid}-t">{e(title)}</h3>'
            f'<p class="cmeasure" data-role="measure">{e(measure)}</p>'
            f'<div class="crows">{rows_}{allrow}<p class="cscale" aria-hidden="true"><span>0</span><span>100%</span></p></div>'
            f'{ctx}<p class="csrc" data-role="source">{e(src)}</p>'
            f'<div class="cfoot">{wordmark_card()}<p>Survey fielded three years before both votes. Studio draft.</p></div></div>')
    return (f'<figure class="cardfig" data-spec="S01" data-dataset="stock-trading-ban" data-evidence="Finding" aria-labelledby="{uid}-t">'
            f'<div class="cardscroll" role="region" tabindex="0" aria-label="Social card from specimen S01, 1080 by 1350 pixels at true size">'
            f'{card}</div>'
            f'<details class="feq" data-role="equivalent"><summary>Show the table</summary><div class="eqb">{eq}</div></details></figure>')


# ================================================================================================ note placer
class Occ:
    """An occupancy grid for one drawing, so notes find free space beside the data instead of on it."""

    def __init__(self, W, H, cell=2):
        self.c, self.W, self.H = cell, W, H
        self.g = np.zeros((int(H / cell) + 3, int(W / cell) + 3), dtype=np.int16)
        self.lab = np.zeros_like(self.g)

    def _sl(self, x0, y0, x1, y1):
        c = self.c
        r0, c0 = max(0, int(y0 // c)), max(0, int(x0 // c))
        r1, c1 = max(0, int(math.ceil(y1 / c))), max(0, int(math.ceil(x1 / c)))
        return slice(r0, r1 + 1), slice(c0, c1 + 1)

    def box(self, x0, y0, x1, y1, label=False):
        sl = self._sl(x0, y0, x1, y1)
        self.g[sl] = 1
        if label:
            self.lab[sl] = 1

    def poly(self, pts, pad=4):
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            n = int(max(abs(xb - xa), abs(yb - ya)) / 2) + 1
            for i in range(n + 1):
                t = i / n
                x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
                self.box(x - pad, y - pad, x + pad, y + pad)

    def free(self, x0, y0, x1, y1, grid=None):
        if x0 < 0 or y0 < 0 or x1 > self.W or y1 > self.H:
            return False
        return not (self.g if grid is None else grid)[self._sl(x0, y0, x1, y1)].any()

    def seg_free(self, xa, ya, xb, yb):
        n = int(max(abs(xb - xa), abs(yb - ya)) / 2) + 1
        for i in range(1, n):
            t = i / n
            x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
            if self.lab[self._sl(x - 1, y - 1, x + 1, y + 1)].any():
                return False
        return True


def place_note(occ, rows_, cls, target, region, pref, size=13, weight=400, lh=16, gap=6, step=4, lead=True, fallback=None):
    """Put a note where it touches no line, mark or other note, as close as it can to its target and its preferred
    corner, with a 1 px leader when it sits away from the target. A shorter fallback wording is tried if the first finds
    no room. Returns the SVG for the note."""
    if fallback:
        try:
            return place_note(occ, rows_, cls, target, region, pref, size, weight, lh, gap, step, lead)
        except SystemExit:
            return place_note(occ, fallback, cls, target, region, pref, size, weight, lh, gap, step, lead)
    w = max(tw(r, size, weight) for r in rows_)
    h = lh * len(rows_) - (lh - size) + 2
    tx, ty = target
    best = None
    rx0, ry0, rx1, ry1 = region
    for y in range(int(ry0), int(ry1 - h) + 1, step):
        for x in range(int(rx0), int(rx1 - w) + 1, step):
            if not occ.free(x - gap, y - gap, x + w + gap, y + h + gap):
                continue
            nx, ny = min(max(tx, x), x + w), min(max(ty, y), y + h)
            d = math.hypot(nx - tx, ny - ty)
            cost = d + 0.35 * math.hypot(x - pref[0], y - pref[1])
            if (best is None or cost < best[0]) and (d <= 9 or occ.seg_free(tx, ty, nx, ny)):
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
    'wide': {'red': ['2021: 5.1%, the lowest from 2009 to 2025.', 'The expanded child tax credit was paid',
                     'that year, half of it in monthly installments.'],
             'y22': ['2022: 12.0%, the first year', 'after the expanded credit expired'],
             'brk': ['Census changed its method in 2013, 2017', 'and 2019. Each of those years has two',
                     'estimates, and the line does not join them.'],
             'off': ['Official measure, which counts', 'pretax cash income only'],
             'spm': ['Supplemental Poverty Measure, which', 'adds tax credits and other aid'], 'spm2': ['Supplemental Poverty Measure']},
    'narrow': {'red': ['2021: 5.1%, the low', 'for 2009 to 2025'], 'y22': ['2022: 12.0%, after', 'the credit expired'],
               'brk': ['Two estimates in', '2013, 2017 and', '2019, not joined'],
               'off': ['Official measure'], 'spm': ['Supplemental', 'Poverty Measure'], 'spm2': ['Supplemental Poverty Measure']},
}


@functools.lru_cache(maxsize=None)
def s02_layout(W):
    """Geometry and notes for one artboard width; shared by every ground, so the views stay identical."""
    spm, off, sseg, oseg = s02_data()
    by = {(r['year'], r['comparable_with']): r for r in spm}
    low = min(spm, key=lambda r: r['percent'])
    assert low['year'] == 2021
    narrow = W < 500
    gut, R_ = 30, (72 if narrow else 76)
    H = 360 if narrow else 440
    T, B = 26, 32
    x0, x1, y0, y1 = gut, W - R_, T, H - B
    X = lambda yr: x0 + (yr - 2009) / (2025 - 2009) * (x1 - x0)
    Y = lambda v: y1 - v / 25 * (y1 - y0)
    occ = Occ(W, H)
    p = []
    for v in (0, 5, 10, 15, 20, 25):
        p.append(f'<line class="{"base" if v == 0 else "grid"}" x1="0" x2="{f(x1 + 6)}" y1="{f(Y(v))}" y2="{f(Y(v))}"/>')
        lab = f'{v}%' if v == 25 else str(v)
        p.append(txt(0, Y(v) - 5, lab, 'tk'))
        occ.box(0, Y(v) - 17, tw(lab) + 4, Y(v) - 2, label=True)
    ticks = [2009, 2013, 2017, 2021, 2025] if narrow else [2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025]
    for yr in ticks:
        p.append(txt(X(yr), H - 10, str(yr), 'tk', 'middle'))
    occ.box(0, y1 + 2, W, H, label=True)
    occ.box(0, 0, W, y0 - 6)
    pts = lambda seg, key: [(X(r['year']), Y(r[key])) for r in seg]
    for seg in oseg:
        p.append('<path class="ln-ctx" d="M' + 'L'.join(f'{f(a)} {f(b)}' for a, b in pts(seg, 'percent')) + '"/>')
        occ.poly(pts(seg, 'percent'), 4)
        for r in seg:
            p.append(f'<circle class="vx-ctx" cx="{f(X(r["year"]))}" cy="{f(Y(r["percent"]))}" r="1.75" data-key="{r["key"]}" '
                     f'data-value="{r["percent"]}" data-mark="vertex"/>')
    for seg in sseg:
        p.append('<path class="ln-main" d="M' + 'L'.join(f'{f(a)} {f(b)}' for a, b in pts(seg, 'percent')) + '"/>')
        occ.poly(pts(seg, 'percent'), 5)
    for r in spm:
        if r is not low:
            p.append(f'<circle class="pt-main" cx="{f(X(r["year"]))}" cy="{f(Y(r["percent"]))}" r="3" data-key="{r["key"]}" '
                     f'data-value="{r["percent"]}" data-mark="point" data-axis="y"/>')
    lx, ly = X(2021), Y(low['percent'])
    occ.box(lx - 9, ly - 9, lx + 9, ly + 9)
    s25 = by[(2025, 'both')]
    ey = Y(s25['percent'])
    p.append(txt(x1 + 8, ey + 5, f'{s25["percent"]}%', 'lab-b'))
    p.append(lines(x1 + 8, ey + 22, ['on both', 'measures'] if narrow else ['on both', 'measures'], 'nt', 16))
    occ.box(x1 + 4, ey - 10, W, ey + 44, label=True)
    N = S02_NOTES['narrow' if narrow else 'wide']
    plot = (x0 + 2, y0, x1, y1)
    r22 = by[(2022, 'both')]
    o11 = next(r for r in off if r['year'] == 2011)
    s10 = by[(2010, 'both')]
    b13 = [r for r in spm if r['year'] == 2013]
    notes = [
        ('red', 'nt-b', (lx, ly), (X(2014.5), Y(4.5))),
        ('y22', 'nt', (X(2022), Y(r22['percent'])), (X(2018.5), Y(24))),
        ('off', 'nt', (X(2011), Y(o11['percent'])), (X(2009.3), Y(24.5))),
        ('brk', 'nt', (X(2013), Y(sum(r['percent'] for r in b13) / 2)), (X(2010.5), Y(9))),
        ('spm', 'lab-s', (X(2010), Y(s10['percent'])), (X(2009.3), Y(14.5))),
    ]
    if narrow:   # on the phone artboard the method note moves under the plot (R25), listed in the figure's notes
        notes = [n for n in notes if n[0] != 'brk']
    for key, cls, target, pref in notes:
        wt = 600 if cls in ('nt-b', 'lab-s') else 400
        p.append(place_note(occ, N[key], cls, target, plot, pref, weight=wt, fallback=N.get(key + '2')))
    return ''.join(p), H, (lx, ly), low


def s02_svg(W, view, red):
    body, H, (lx, ly), low = s02_layout(W)
    if red == 'working':
        rd = ' data-red="working" data-red-job="the 2021 low the title names"'
    elif red == 'specimen':
        rd = ' data-red="specimen"'
    else:
        rd = ''
    pcls = 'pt-red' if red in ('working', 'specimen') else 'pt-main'
    dot = (f'<g{rd}><circle class="{pcls}" cx="{f(lx)}" cy="{f(ly)}" r="5.5" data-key="{low["key"]}" data-value="{low["percent"]}" '
           f'data-mark="point" data-axis="y"/></g>')
    lab = ('Line chart of child poverty, 2009 to 2025. Under the Supplemental Poverty Measure it fell to 5.1 percent in 2021 and '
           'rose to 12.0 percent in 2022 and 13.5 percent in 2023 and 2024; it was 13.4 percent in 2025. The official measure, '
           'drawn for context, ran from 22.0 percent in 2010 to 13.4 percent in 2025.')
    return svg(W, H, f's02-{view}-{W}', lab, body + dot, 'ab')


def s02(view, red='working'):
    uid = f'{view}-s02'
    spm, off, sseg, oseg = s02_data()
    title = 'Child poverty fell to 5.1 percent in 2021, its lowest from 2009 to 2025, while the expanded child tax credit was paid.'
    measure = ('Children under 18 below the poverty line, Supplemental Poverty Measure, United States, 2009 to 2025, '
               'in percent, with the official measure for context')
    body = (f'<div class="abs">{s02_svg(866, view, red)}{s02_svg(560, view, red)}{s02_svg(328, view, red)}</div>')
    notes = ['The Supplemental Poverty Measure counts tax credits and other aid that the official measure leaves out. '
             'Census treats a change between two years as a description, not the effect of one policy.',
             'The Census Bureau revised 2019 to 2024 in August 2026. Atlas V7 prints the first-published 9.7, 5.2 and 13.4 percent '
             'for 2020, 2021 and 2024; the current table reads 9.6, 5.1 and 13.5.',
             'Margins of error run from 0.4 to 0.9 points at the 90 percent level; the table gives each one.']
    src = source_text('child-poverty-spm')
    shown = [e(n) for n in notes] + ['<span class="n-only">Census changed its method in 2013, 2017 and 2019. Each of those years has '
                                     'two estimates, and the line does not join them.</span>']
    offy = {(r['year'], r['comparable_with']): r for r in off}

    def ov(r):
        o = offy.get((r['year'], r['comparable_with'])) or offy.get((r['year'], 'both'))
        return (f'{o["percent"]:.1f}', o['percent']) if o else ('not given', -1)
    variant = {'standard': '', 'corrected_2026_method': 'Method used from 2019 on', 'original_2011_method': 'Original 2011 method',
               'updated_processing': 'Updated processing', 'legacy_processing': 'Earlier processing',
               'redesigned_income_questions': 'Redesigned income questions', 'traditional_income_questions': 'Traditional income questions'}
    data = sorted(spm, key=lambda r: (-r['year'], r['comparable_with'] != 'later'))
    eq = table([('Year', lambda r: (str(r['year']), r['year']), 'h'),
                ('Estimate', lambda r: (e(variant.get(r['series_variant'], r['series_variant'])) or 'Standard', r['series_variant']), 't'),
                ('Supplemental measure, %', lambda r: (f'<span data-key="{r["key"]}" data-value="{r["percent"]}" data-mark="label">{r["percent"]:.1f}</span>', r['percent']), 'n'),
                ('Margin of error, points', lambda r: (f'{float(r["moe_pct"]):.1f}', r['moe_pct']), 'n'),
                ('Official measure, %', ov, 'n')], data, 'Child poverty by year, both measures', f'{uid}-eq') \
        + eq_extra(S02_NOTES['wide']['red'][:1] + ['The expanded child tax credit was paid in 2021, half of it in monthly installments.',
                                                   '2022: 12.0 percent, the first year after the expanded credit expired.',
                                                   'Census changed its method in 2013, 2017 and 2019; each of those years has two estimates, and the line does not join them.',
                                                   '2025: 13.4 percent on both measures.'] + notes, src)
    return figure('S02', uid, title, measure, body, shown, src, eq, 'official statistic')


# ================================================================================================ S03 register
S03_ACTORS = [('Voters at the ballot box', ['Ballot initiative', 'Referendum']),
              ('Legislatures and councils', ['State statute', 'Federal statute', 'Local law or funding vote']),
              ('Courts', ['Court ruling']),
              ('Executives and agencies', ['Executive or agency action'])]
DIRS = [('away from voters', 'Away', 'awy'), ('toward voters', 'Toward', 'tow'), ('voters kept existing rules', 'Kept', 'kept'),
        ('mixed', 'Mixed', 'mix'), ('pending', 'Pending', 'pend')]


def swatch(kind):
    return f'<span class="sw sw-{kind}" aria-hidden="true"></span>'


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
    assert R['Ballot initiative']['away from voters'] == 0 and (R['State statute']['away from voters'], R['State statute']['value']) == (9, 11)
    title = f'Legislatures and courts made {leg_courts} of the {total_away} rule changes the atlas codes as moving away from voters.'
    measure = ('Rule changes in the atlas\'s repair log, by how each was made and by direction, United States, '
               'August 6, 1965 to the November 3, 2026 ballot')
    mx = max(r['value'] for r in R.values())
    head = ('<thead><tr><th scope="col">How the change was made</th><th scope="col" class="bc">Rule changes</th>'
            + ''.join(f'<th scope="col" class="n dc">{swatch(k)}{lab}</th>' for _, lab, k in DIRS) + '</tr></thead>')
    notes_row = {'Ballot initiative': 'None of 17 moved the rules away from voters.',
                 'State statute': '9 of 11 moved the rules away from voters.'}
    body = []
    for name, rs, tot, dt in grp:
        body.append('<tbody>')
        body.append(f'<tr class="grp"><th scope="rowgroup">{e(name)}</th><td class="bc gt">{tot}</td>'
                    + ''.join(f'<td class="n gt" data-label="{lab}">{dt[d]}</td>' for d, lab, _ in DIRS) + '</tr>')
        for r in rs:
            segs = ''.join(
                f'<span class="seg s-{k}" data-key="{e(r["key"])}" data-field="{d}" data-value="{r[d]}" data-mark="bar" '
                f'data-axis="x" style="width:{100 * r[d] / mx:.3f}%"></span>' for d, _, k in DIRS if r[d])
            note = f'<span class="rnote">{e(notes_row[r["key"]])}</span>' if r['key'] in notes_row else ''
            cells = ''.join(f'<td class="n{" z" if r[d] == 0 else ""}" data-label="{lab}">{r[d]}</td>' for d, lab, _ in DIRS)
            body.append(f'<tr><th scope="row">{e(r["key"])}{note}</th>'
                        f'<td class="bc"><span class="bar"><span class="trk" aria-hidden="true">{segs}</span>'
                        f'<span class="bt" data-key="{e(r["key"])}" data-value="{r["value"]}" data-mark="label">{r["value"]}</span></span></td>'
                        f'{cells}</tr>')
        body.append('</tbody>')
    tots = {d: sum(g[3][d] for g in grp) for d, _, _ in DIRS}
    foot = ('<tfoot><tr><th scope="row">All 64 changes</th><td class="bc gt">64</td>'
            + ''.join(f'<td class="n gt" data-label="{lab}">{tots[d]}</td>' for d, lab, _ in DIRS) + '</tr></tfoot>')
    reg = (f'<div class="tw"><table class="reg s03"><caption>Rule changes by how they were made, grouped by who acted</caption>'
           f'{head}{"".join(body)}{foot}</table></div>')
    notes = ['Directions are the atlas\'s own codes, set out in its coding note: "toward voters" means a change widens who can vote '
             'or have a ballot counted, opens the deciding contest, limits or shows political money, or strengthens a check on officials. '
             'A direction carries no judgment of the people or parties involved.',
             'The studio grouped five one-row instruments (agency rule, executive action and executive order; municipal ordinance and '
             'council funding vote), and grouped instruments by who acted. The instruments are V7\'s.',
             f'Bars share one scale, from 0 to {mx} changes, and every count is printed.']
    src = source_text('rule-changes-by-instrument')
    eqrows = [r for _, rs, _, _ in grp for r in rs]
    eq = table([('Instrument', lambda r: (e(r['key']), r['key']), 'h'), ('All', lambda r: (str(r['value']), r['value']), 'n')]
               + [(lab, (lambda d: (lambda r: (str(r[d]), r[d])))(d), 'n') for d, lab, _ in DIRS],
               eqrows, 'Rule changes by instrument and direction', f'{uid}-eq') + eq_extra(
        ['None of 17 ballot initiatives moved the rules away from voters.', '9 of 11 state statutes moved the rules away from voters.'] + notes, src)
    return figure('S03', uid, title, measure, reg, [e(n) for n in notes], src, eq, 'documented record')


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
    if ch == 0:
        return 'No change'
    return f'{"Up" if ch > 0 else "Down"} {abs(ch):.1f} points'


def dumbbell(xa, xb, y, a, b, ctx):
    """Two years on one row: the earlier year a hollow ring drawn on top, the later year a filled dot, joined edge to edge."""
    out = []
    gapx = abs(xb - xa) - 13
    if gapx > 0:
        d = 1 if xb > xa else -1
        out.append(f'<line class="{"db-ctx" if ctx else "db"}" x1="{f(xa + d * 6.5)}" x2="{f(xb - d * 6.5)}" y1="{f(y)}" y2="{f(y)}"/>')
    out.append(f'<circle class="d24{" c" if ctx else ""}" cx="{f(xb)}" cy="{f(y)}" r="6" data-key="{b["key"]}" data-value="{b["voted_pct"]}" data-mark="point" data-axis="x"/>')
    out.append(f'<circle class="d20{" c" if ctx else ""}" cx="{f(xa)}" cy="{f(y)}" r="6" data-key="{a["key"]}" data-value="{a["voted_pct"]}" data-mark="point" data-axis="x"/>')
    return ''.join(out)


def s04_svg(W, view):
    data = s04_numbers()
    narrow = W < 500
    lo, hi = 40, 80
    p = []
    if not narrow:
        lx, px0, px1 = 0, 170, 520 if W < 800 else 560
        c20, c24, cch = (px1 + 70, px1 + 140, W) if W >= 800 else (px1 + 0, px1 + 0, W)
        X = lambda v: px0 + (v - lo) / (hi - lo) * (px1 - px0)
        top = 62
        rh = 46
        for v in range(lo, hi + 1, 10):
            p.append(txt(X(v), 18, f'{v}%' if v == hi else str(v), 'tk', 'middle'))
        if W >= 800:
            p.append(txt(c20, 18, '2020', 'th', 'end'))
            p.append(txt(c24, 18, '2024', 'th', 'end'))
            p.append(txt(cch, 18, 'Change', 'th', 'end'))
        p.append(f'<line class="base" x1="0" x2="{W}" y1="28" y2="28"/>')
        for i, (k, lab, a, b, ch) in enumerate(data):
            y = top + i * rh + (12 if k == 'all' else 0) - (0 if i else 0)
            ctx = k == 'all'
            if ctx:
                p.append(f'<line class="grid" x1="0" x2="{W}" y1="{f(y - 29)}" y2="{f(y - 29)}"/>')
            p.append(txt(lx, y + 5, e(lab), 'lab' if not ctx else 'lab-ctx'))
            xa, xb = X(a['voted_pct']), X(b['voted_pct'])
            p.append(dumbbell(xa, xb, y, a, b, ctx))
            if i == 0:
                for xx, lab_, cls_ in ((xa, '2020', 'nt'), (xb, '2024', 'nt-b')):
                    other = xb if xx == xa else xa
                    p.append(txt(xx + (6 if xx > other else -6), y - 13, lab_, cls_, 'start' if xx > other else 'end'))
            if W >= 800:
                p.append(txt(c20, y + 5, f'<tspan data-key="{a["key"]}" data-value="{a["voted_pct"]}" data-mark="label">{a["voted_pct"]:.1f}</tspan>', 'num', 'end'))
                p.append(txt(c24, y + 5, f'<tspan data-key="{b["key"]}" data-value="{b["voted_pct"]}" data-mark="label">{b["voted_pct"]:.1f}</tspan>', 'num-b', 'end'))
                p.append(txt(cch, y + 5, e(change_words(ch)), 'num', 'end'))
            else:
                p.append(txt(W, y + 5, e(change_words(ch)), 'num', 'end'))
        H = top + len(data) * rh + 4
    else:
        X = lambda v: 6 + (v - lo) / (hi - lo) * (W - 12)
        p.append(txt(X(40), 16, '40', 'tk', 'start'))
        p.append(txt(X(60), 16, '60', 'tk', 'middle'))
        p.append(txt(X(80), 16, '80%', 'tk', 'end'))
        p.append(f'<line class="base" x1="0" x2="{W}" y1="26" y2="26"/>')
        y = 50
        for i, (k, lab, a, b, ch) in enumerate(data):
            ctx = k == 'all'
            if ctx:
                y += 8
                p.append(f'<line class="grid" x1="0" x2="{W}" y1="{f(y - 18)}" y2="{f(y - 18)}"/>')
            p.append(txt(0, y, e(lab), 'lab' if not ctx else 'lab-ctx'))
            p.append(txt(W, y, e(change_words(ch)), 'num', 'end'))
            yd = y + 20
            xa, xb = X(a['voted_pct']), X(b['voted_pct'])
            p.append(dumbbell(xa, xb, yd, a, b, ctx))
            p.append(txt(0, yd + 26, f'2020 <tspan data-key="{a["key"]}" data-value="{a["voted_pct"]}" data-mark="label">{a["voted_pct"]:.1f}</tspan>%'
                         f'  ·  2024 <tspan class="b" data-key="{b["key"]}" data-value="{b["voted_pct"]}" data-mark="label">{b["voted_pct"]:.1f}</tspan>%', 'nt'))
            y = yd + 56
        H = y - 16
    lab = ('Dot plot of reported voting by age among citizens, 2020 and 2024: ' + '; '.join(
        f'{lab} {a["voted_pct"]:.1f} percent in 2020 and {b["voted_pct"]:.1f} in 2024, {change_words(ch).lower()}' for k, lab, a, b, ch in data) + '.')
    return svg(W, H, f's04-{view}-{W}', lab, ''.join(p))


def s04(view):
    uid = f'{view}-s04'
    data = s04_numbers()
    y24 = {k: b['voted_pct'] for k, _, _, b, _ in data}
    assert y24['18_to_24'] < y24['25_to_44'] < y24['45_to_64'] < y24['65_and_over']
    title = (f'Reported voting rose with age in 2024, from {y24["18_to_24"]:.1f} percent of citizens 18 to 24 '
             f'to {y24["65_and_over"]:.1f} percent of those 65 and over.')
    measure = ('Citizens 18 and over who said they voted, by age, United States, November 2020 and November 2024, in percent; '
               'the scale runs from 40 to 80 percent')
    body = f'<div class="abs">{s04_svg(866, view)}{s04_svg(560, view)}{s04_svg(328, view)}</div>'
    notes = ['These are the rates people reported to the Census survey, which run higher than counts of ballots cast.',
             'Every group under 65 reported voting less in 2024 than in 2020; the youngest fell most.',
             'The table gives no margins of error.']
    src = source_text('turnout-by-age')
    eq = table([('Age', lambda t: (e(t[1]), t[1]), 'h'),
                ('2020, %', lambda t: (f'{t[2]["voted_pct"]:.1f}', t[2]['voted_pct']), 'n'),
                ('2024, %', lambda t: (f'{t[3]["voted_pct"]:.1f}', t[3]['voted_pct']), 'n'),
                ('Change, points', lambda t: (signed(t[4]), t[4]), 'n')], data,
               'Reported voting by age, 2020 and 2024', f'{uid}-eq') + eq_extra(notes, src)
    return figure('S04', uid, title, measure, body, [e(n) for n in notes], src, eq, 'official statistic, self-reported')


# ================================================================================================ S05 small multiples
GROUPS = [('non_hispanic_white', 'Non-Hispanic White'), ('all_households', 'All households'), ('hispanic', 'Hispanic'), ('black', 'Black')]


def s05_series():
    rs = rows('homeownership-by-race')
    out = {}
    for g, _ in GROUPS:
        mine = [r for r in rs if r['group'] == g and r['series_variant'] in ('standard', 'original')]
        a = sorted([r for r in mine if r['year'] <= 2002], key=lambda r: r['year'])
        b = sorted([r for r in mine if r['year'] >= 2003], key=lambda r: r['year'])
        out[g] = (a, b)
    return out


def s05_numbers():
    S = s05_series()
    v = {g: {r['year']: r['rate_pct'] for r in S[g][0] + S[g][1]} for g, _ in GROUPS}
    order = sorted(GROUPS, key=lambda g: -v[g[0]][2025])
    return S, v, order


@functools.lru_cache(maxsize=None)
def s05_body(W):
    S, v, order = s05_numbers()
    narrow = W < 500
    cols = 2 if narrow else 4
    gut, gap = 36, (18 if narrow else 24)
    pw = (W - gut - gap * (cols - 1)) / cols
    ph = 128 if narrow else 156
    head = 48
    lo, hi = 40, 80
    p = []
    for i, (g, name) in enumerate(order):
        cx, cy = gut + (i % cols) * (pw + gap), (i // cols) * (ph + head + 38)
        X = lambda yr: cx + 3 + (yr - 1994) / (2025 - 1994) * (pw - 14)
        Y = lambda val: cy + head + (hi - val) / (hi - lo) * ph
        p.append(txt(cx, cy + 15, e(name), 'lab-s' if narrow else 'lab'))
        p.append(txt(cx, cy + 33, f'{v[g][2025]:.1f}% in 2025', 'nt'))
        for t in range(lo, hi + 1, 10):
            p.append(f'<line class="grid" x1="{f(cx)}" x2="{f(cx + pw)}" y1="{f(Y(t))}" y2="{f(Y(t))}"/>')
            if i % cols == 0:
                p.append(txt(gut - 6, Y(t) + 4.5, f'{t}%' if t == hi else str(t), 'tk', 'end'))
        for og, _ in GROUPS:
            if og != g:
                for seg in S[og]:
                    p.append('<path class="ln-ctx" d="M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg) + '"/>')
        for seg in S[g]:
            p.append('<path class="ln-sm" d="M' + 'L'.join(f'{f(X(r["year"]))} {f(Y(r["rate_pct"]))}' for r in seg) + '"/>')
            for r in seg:
                p.append(f'<circle class="pt-sm" cx="{f(X(r["year"]))}" cy="{f(Y(r["rate_pct"]))}" r="1.9" data-key="{r["key"]}" '
                         f'data-value="{r["rate_pct"]}" data-mark="point" data-axis="y" data-scale="{g}"/>')
        p.append(txt(cx, Y(lo) + 18, '1994', 'tk'))
        p.append(txt(cx + pw, Y(lo) + 18, '2025', 'tk', 'end'))
        if g == 'black':
            nw, bk = v['non_hispanic_white'][2025], v['black'][2025]
            xg = X(2025) + 6
            p.append(f'<path class="brk" d="M{f(xg - 4)} {f(Y(nw))}H{f(xg)}V{f(Y(bk))}H{f(xg - 4)}"/>')
            p.append(txt(xg - 7, Y(57.5) + 4, f'{nw - bk:.1f} pts', 'nt-b', 'end'))
        if i == 0 and not narrow:
            xb = (X(2002) + X(2003)) / 2
            p.append(f'<line class="lead" x1="{f(xb)}" y1="{f(Y(77.2))}" x2="{f(xb)}" y2="{f(Y(79))}"/>')
            p.append(txt(xb - 4, Y(78.1) + 4, 'break', 'nt', 'end'))
    rows_n = math.ceil(len(order) / cols)
    H = rows_n * (ph + head + 38) - 14
    return ''.join(p), H


def s05_svg(W, view):
    S, v, order = s05_numbers()
    body, H = s05_body(W)
    lab = ('Four small charts of homeownership rates, 1994 to 2025, one per group, on one scale from 40 to 80 percent: '
           + '; '.join(f'{n} {v[g][2025]:.1f} percent in 2025' for g, n in order) + '. Each line breaks at 2003. In 2025 Black '
           'householders trailed non-Hispanic White householders by '
           f'{v["non_hispanic_white"][2025] - v["black"][2025]:.1f} points.')
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
            '<th scope="col" class="n">Change, points</th><th scope="col" class="n">Gap in 2003</th><th scope="col" class="n">Gap in 2025</th></tr></thead><tbody>'
            + ''.join(f'<tr><th scope="row">{e(n)}</th><td class="n" data-label="2003, %">{a:.1f}</td><td class="n" data-label="2025, %">{b:.1f}</td>'
                      f'<td class="n" data-label="Change, points">{signed(c)}</td><td class="n{" z" if gp[0][0].isalpha() else ""}" data-label="Gap in 2003">{gp[0]}</td>'
                      f'<td class="n{" z" if gp[1][0].isalpha() else ""}" data-label="Gap in 2025">{gp[1]}</td></tr>' for n, a, b, c, gp in reg_rows)
            + '</tbody></table></div>')
    body = f'<div class="abs">{s05_svg(866, view)}{s05_svg(560, view)}{s05_svg(328, view)}</div>{regt}'
    notes = [f'The gap between Hispanic and non-Hispanic White householders narrowed, from {hgap03:.1f} points in 2003 to {hgap25:.1f} in 2025.',
             'Each line breaks at 2003, when race categories changed. Earlier years use the older categories, and 2002 has two values in '
             'the table (as first published and revised to 2000 Census weights); the lines use the first.',
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
    eq = table([('Year', lambda r: (f'{r["year"]}' + (f' <span class="vs">{vlab[r["var"]]}</span>' if vlab[r['var']] else ''), r['year']), 'h')]
               + [(f'{n}, %', (lambda g: (lambda r: ((f'{r[g]["rate_pct"]:.1f}' if r[g] else 'not given'), r[g]['rate_pct'] if r[g] else -1)))(g), 'n')
                  for g, n in GROUPS], piv, 'Homeownership rate by year and group', f'{uid}-eq') + eq_extra(
        [f'Black panel, 2025: {gap25:.1f} points below non-Hispanic White householders.'] + notes, src)
    return figure('S05', uid, title, measure, body, [e(n) for n in notes], src, eq, 'official statistic')


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


def s06_numbers():
    rs = rows('scenarios-2030')
    R = {r['key']: r for r in rs}

    def resolved(r, fam):
        c = r[f'{fam}_class']
        return R['ii'][f'{fam}_class'] if c == 'same as ii' else c
    allup = [r['key'] for r in rs if all(resolved(r, k) in ('up', 'slightly up') for k, _ in FAM)]
    return rs, allup


def s06(view):
    uid = f'{view}-s06'
    rs, allup = s06_numbers()
    assert allup == ['iii', 'iv-b'], allup
    title = 'Two of the eight reform paths would move all four outcome families up by 2036, if their assumptions hold.'
    measure = ('Direction each outcome family would take under each scenario, in Atlas V7\'s words, United States, '
               '2026 baseline to 2036; conditional directions, not forecasts')
    key = ('<div class="gkey"><p class="gkh">The glyph is the studio\'s reading of V7\'s words</p><ul>'
           + ''.join(f'<li>{glyph(c)}<span>{e(CLS[c][2])}</span></li>' for c in ['up', 'slightly up', 'flat', 'flat or down', 'down', 'mixed', 'same as ii'])
           + '</ul></div>')
    head = '<thead><tr><th scope="col">Scenario</th>' + ''.join(f'<th scope="col">{e(n)}</th>' for _, n in FAM) + '</tr></thead>'
    body = []
    for r in rs:
        tag = '<span class="tag">All four up</span>' if r['key'] in allup else ''
        cells = ''.join(
            f'<td data-label="{e(n)}"><span class="cell">{glyph(r[k + "_class"], r["key"], k + "_class", r[k + "_class"])}'
            f'<span class="cw" data-key="{e(r["key"])}" data-field="{k}" data-category="{e(r[k])}" data-mark="label">{e(r[k])}</span></span></td>'
            for k, n in FAM)
        body.append(f'<tr{" class=hl" if r["key"] in allup else ""}><th scope="row"><span class="sk">{e(r["key"])}</span>'
                    f'<span class="sn">{e(r["name"])}</span>{tag}</th>{cells}</tr>')
    reg = (f'{key}<div class="tw"><table class="reg s06"><caption>Eight scenarios and four outcome families</caption>{head}'
           f'<tbody>{"".join(body)}</tbody></table></div>')
    notes = ['Each scenario gives a direction only if its assumptions hold. It makes no forecast and gives no odds.',
             'The four families are read one at a time and never added together.',
             'Where V7 writes "same as scenario ii", the glyph shows that pointer; the title reads scenario ii\'s direction there.',
             'Up is Verdigris and down is Prussian, each with its own arrow, so the reading holds without color.']
    src = source_text('scenarios-2030')
    flat = [(r, k, n) for r in rs for k, n in FAM]
    eq = table([('Scenario', lambda t: (f'{e(t[0]["key"])}, {e(t[0]["name"])}', t[0]['key']), 'h'),
                ('Family', lambda t: (e(t[2]), t[2]), 't'),
                ('V7\'s words', lambda t: (e(t[0][t[1]]), t[0][t[1]]), 't'),
                ('Studio\'s reading', lambda t: (e(CLS[t[0][t[1] + "_class"]][2]), t[0][t[1] + '_class']), 't'),
                ('V7\'s reason', lambda t: (e(t[0].get(t[1] + '_why', '')), ''), 't')], flat,
               'Every cell, with V7\'s reason', f'{uid}-eq') + eq_extra(notes, src)
    return figure('S06', uid, title, measure, reg, [e(n) for n in notes], src, eq, 'conditional estimate, no forecast')


# ================================================================================================ S07 tile map
STATUS = [('bans in all elections', 'all', 'Bans it in all elections'), ('bans in some elections', 'some', 'Bans it in some elections'),
          ('no ban', 'none', 'No state ban')]


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
    narrow = W < 500
    t = 25 if narrow else 40
    gp = 2 if narrow else 4
    p = []
    for tl in sorted(TILES, key=lambda x: (x['row'], x['col'])):
        r = R[tl['code']]
        k = next(s[1] for s in STATUS if s[0] == r['status'])
        x, y = tl['col'] * (t + gp), tl['row'] * (t + gp)
        tip = f'{r["name"]}: {next(s[2] for s in STATUS if s[0] == r["status"]).lower()}'
        if r['prohibits_rcv']:
            tip += f' ({r["measure"]}, {int(r["enacted_year"])})'
        p.append(f'<g class="tile t-{k}"><title>{e(tip)}</title>'
                 f'<rect x="{x}" y="{y}" width="{t}" height="{t}" data-key="{tl["code"]}" data-field="status" '
                 f'data-category="{e(r["status"])}" data-mark="cell"/>')
        if narrow:
            p.append(txt(x + t / 2, y + t / 2 + 4.5, tl['code'], 'tc', 'middle'))
        else:
            p.append(txt(x + t / 2, y + (16 if r['prohibits_rcv'] else 25), tl['code'], 'tc', 'middle'))
            if r['prohibits_rcv']:
                p.append(txt(x + t / 2, y + 32, str(int(r['enacted_year']))[2:].rjust(3, '’'), 'ty', 'middle'))
        p.append('</g>')
    Wd = 12 * (t + gp) - gp
    H = 8 * (t + gp) - gp
    lab = (f'Tile map of the 50 states and DC, one square each. {cnt["bans in all elections"]} states ban ranked-choice voting in all '
           f'elections, {cnt["bans in some elections"]} in some (Ohio and Tennessee), and {cnt["no ban"]} states and DC have no state ban, '
           'as of November 2026.')
    return svg(Wd, H, f's07-{view}-{W}', lab, ''.join(p), 'ab ' + ('ab-n' if narrow else 'ab-wm'))


def s07(view):
    uid = f'{view}-s07'
    R, cnt, years = s07_numbers()
    nban = cnt['bans in all elections'] + cnt['bans in some elections']
    assert (nban, cnt['bans in all elections']) == (19, 17)
    title = f'Nineteen states ban ranked-choice voting, {cnt["bans in all elections"]} of them in all elections, as of November 2026.'
    measure = 'States that prohibit ranked-choice voting by statute or constitution, 50 states and DC, as of November 2026'
    keyl = ''.join(f'<li><span class="tsw tsw-{k}" aria-hidden="true"></span><span>{e(lab)}</span><b>{cnt[s] if s != "no ban" else str(cnt[s] - 1) + " states and DC"}</b></li>'
                   for s, k, lab in STATUS)
    reg = ['<table class="reg s07r"><caption>Bans by year enacted</caption><thead><tr><th scope="col">Year</th>'
           '<th scope="col" class="n">Bans</th><th scope="col">States</th></tr></thead><tbody>']
    for y in sorted(years):
        sts = sorted(years[y], key=lambda r: r['name'])
        names = ', '.join(e(r['name']) + (' (some elections)' if r['scope'] == 'some' else '') for r in sts)
        reg.append(f'<tr><th scope="row">{y}</th><td class="n">{len(sts)}</td><td>{names}</td></tr>')
    reg.append(f'</tbody><tfoot><tr><th scope="row">All</th><td class="n">{nban}</td><td></td></tr></tfoot></table>')
    body = (f'<ul class="tkey">{keyl}</ul><div class="s07"><div class="mapw">{s07_svg(866, view)}{s07_svg(328, view)}'
            f'<p class="mapn">Each square is one state, the same size whatever its area. On wide screens two digits under a code give the year the ban was enacted; the register lists them all.</p></div>'
            f'<div class="s07reg"><div class="tw">{"".join(reg)}</div></div></div>')
    notes = ['A state without a ban may still give its cities no way to adopt ranked-choice voting. The map shows bans only.',
             'Ohio\'s ban leaves an opening for home-rule cities, at the cost of state funds; Tennessee\'s names statewide and local offices only.',
             'Missouri\'s ban is in its constitution; the other 18 are statutes.',
             'Ranked-choice voting lets voters rank candidates; the count runs in rounds until one has a majority.']
    src = source_text('rcv-bans') + ' Ballotpedia is a secondary source; Atlas V7 cites the National Conference of State Legislatures, whose page refused automated reading.'
    data = sorted(R.values(), key=lambda r: (r['status'] == 'no ban', r['name']))
    eq = table([('State', lambda r: (e(r['name']), r['name']), 'h'),
                ('Status', lambda r: (f'<span data-key="{r["key"]}" data-field="status" data-category="{e(r["status"])}" data-mark="label">{e(r["status"])}</span>', r['status']), 't'),
                ('Enacted', lambda r: ((str(int(r['enacted_year'])) if r['prohibits_rcv'] else 'no ban'), r['enacted_year'] or 0), 'n'),
                ('Measure', lambda r: (e(r['measure']) if r['measure'] else 'no ban', r['measure']), 't'),
                ('Scope', lambda r: (e(r['scope_note']), r['scope_note']), 't')], data,
               'Every state and DC', f'{uid}-eq', sortable=True, sort_col=1, sort_dir='ascending') + eq_extra(notes, src)
    return figure('S07', uid, title, measure, body, [e(n) for n in notes], src, eq, 'secondary compilation')


# ================================================================================================ S08 unit chart
UNIT_KIND = {'toward voters': 'tow', 'away from voters': 'awy', 'voters kept existing rules': 'kept', 'mixed': 'mix', 'pending': 'pend'}


def unit(r):
    k = UNIT_KIND[r['direction']]
    a = f'data-key="{r["key"]}" data-category="{e(r["direction"])}" data-mark="unit"'
    if k in ('tow', 'awy'):
        shape = f'<rect class="u-{k}" x="0" y="0" width="14" height="14" {a}/>'
    elif k == 'kept':
        shape = f'<rect class="u-kept" x="0.75" y="0.75" width="12.5" height="12.5" {a}/>'
    elif k == 'mix':
        shape = (f'<rect class="u-mix" x="0.75" y="0.75" width="12.5" height="12.5" {a}/>'
                 '<path class="u-hatch" d="M1 9 9 1M1 13.5 13.5 1M5 13.5 13.5 5"/>')
    else:
        shape = f'<rect class="u-pend" x="0.75" y="0.75" width="12.5" height="12.5" {a}/>'
    return f'<svg class="u" viewBox="0 0 14 14" aria-hidden="true" focusable="false">{shape}</svg>'


def s08_numbers():
    rs = rows('rule-changes')
    cols = ['early'] + list(range(2010, 2027))
    col_of = lambda r: 'early' if r['year'] < 2010 else r['year']
    since = Counter(r['direction'] for r in rs if r['year'] >= 2025)
    before = Counter(r['direction'] for r in rs if r['year'] < 2025)
    return rs, cols, col_of, since, before


def s08(view):
    uid = f'{view}-s08'
    rs, cols, col_of, since, before = s08_numbers()
    cnt = DS['rule-changes']['counts']
    assert since['away from voters'] == 17 and cnt['away from voters'] == 24 and before['away from voters'] == 7
    title = (f'Seventeen of the {cnt["away from voters"]} rule changes the atlas codes as moving away from voters came in '
             '2025 and 2026.')
    measure = ('Rule changes in the atlas\'s repair log, one square per change, by year and the atlas\'s direction code, '
               'United States, 1965 to the November 3, 2026 ballot')
    bands = [('Toward voters', ['toward voters'], 'tow'), ('Away from voters', ['away from voters'], 'awy'),
             ('Neither way', ['voters kept existing rules', 'mixed', 'pending'], 'nei')]
    out = ['<div class="uc" role="img" aria-label="' + e(
        f'Unit chart, one square per rule change, by year. Toward voters: {cnt["toward voters"]}, of which 8 came in 2025 and 2026. '
        f'Away from voters: {cnt["away from voters"]}, of which 17 came in 2025 and 2026 (6 in 2025, 11 in 2026). '
        f'Neither way: voters kept existing rules {cnt["voters kept existing rules"]} (8 of them in 2024), mixed {cnt["mixed"]}, '
        f'pending {cnt["pending"]} on the November 3, 2026 ballot.') + '">']
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
            c0 = cols.index(2025) + 1
            notes = (f'<p class="uc-nt" style="grid-column:2 / -1">{since["away from voters"]} of the {cnt["away from voters"]} came in 2025 and 2026</p>'
                     f'<span class="uc-br" style="grid-column:{c0} / -1" aria-hidden="true"></span>')
        if k == 'nei':
            c0 = cols.index(2024) + 1
            notes = (f'<p class="uc-nt" style="grid-column:2 / {c0 + 1}">Voters turned down 8 ballot measures in 2024</p>'
                     f'<span class="uc-br" style="grid-column:{c0} / {c0 + 1}" aria-hidden="true"></span>')
        out.append(f'<div class="uc-band b-{k}"><div class="uc-lab">{label}</div>'
                   f'<div class="uc-cols">{notes}{"".join(cells)}</div></div>')
    yl = []
    for i, c in enumerate(cols):
        if c == 'early':
            yl.append('<span class="uy uy0" style="grid-column:1">1965<br>1988</span>')
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
    notes = [f'Toward and away each total {cnt["toward voters"]}. Before 2025 the log holds {before["toward voters"]} changes toward voters and '
             f'{before["away from voters"]} away; since January 2025, {since["toward voters"]} toward and {since["away from voters"]} away.',
             'Directions are the atlas\'s own codes, set out in its coding note. A partisan mid-decade redraw counts as away from voters '
             'whichever party draws it.',
             'Counts are entries in the atlas\'s log. One row, RL02, rests on a source the atlas did not check.',
             'The first column holds the two oldest entries, 1965 and 1988. 2011, 2012 and 2023 have none.']
    src = source_text('rule-changes')
    data = sorted(rs, key=lambda r: r['date'], reverse=True)
    eq = table([('ID', lambda r: (r['key'], r['key']), 'h'), ('Date', lambda r: (date_words(r['date']), r['date']), 't'),
                ('Where', lambda r: (e(r['jurisdiction']), r['jurisdiction']), 't'),
                ('Direction', lambda r: (e(r['direction']), r['direction']), 't'),
                ('How', lambda r: (e(r['instrument_group']), r['instrument_group']), 't'),
                ('What changed', lambda r: (e(r['rule']), ''), 't')], data,
               'The 64 rule changes in the repair log, newest first', f'{uid}-eq', sortable=True, sort_col=1) + eq_extra(
        ['17 of the 24 changes away from voters came in 2025 and 2026.', 'Voters turned down 8 ballot measures in 2024.'] + notes, src)
    return figure('S08', uid, title, measure, body, [e(n) for n in notes], src, eq, 'documented record')


def unit_key(d):
    k = UNIT_KIND[d]
    cls = {'tow': '<rect class="u-tow" x="0" y="0" width="14" height="14"/>',
           'awy': '<rect class="u-awy" x="0" y="0" width="14" height="14"/>',
           'kept': '<rect class="u-kept" x="0.75" y="0.75" width="12.5" height="12.5"/>',
           'mix': '<rect class="u-mix" x="0.75" y="0.75" width="12.5" height="12.5"/><path class="u-hatch" d="M1 9 9 1M1 13.5 13.5 1M5 13.5 13.5 5"/>',
           'pend': '<rect class="u-pend" x="0.75" y="0.75" width="12.5" height="12.5"/>'}[k]
    return f'<svg class="uk" viewBox="0 0 14 14" aria-hidden="true" focusable="false">{cls}</svg>'


# ================================================================================================ S09 timeline
def ev_short(t):
    return t.split(' (')[0]


@functools.lru_cache(maxsize=None)
def s09_body(W):
    ds = DS['history-events']
    evs = ds['rows']
    threads = ds['threads']
    p = []
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
            p.append(f'<line class="grid" x1="0" x2="{W}" y1="{f(Y(yr))}" y2="{f(Y(yr))}"/>')
            p.append(txt(0, Y(yr) - 5, str(yr), 'tk'))
        bottom = Y(2027)
        for i, th in enumerate(threads):
            cx = gut + i * (cw + gap)
            p.append(txt(cx, 15, e(heads[i][0]), 'lab'))
            p.append(lines(cx, 33, heads[i][1:], 'nt', 17))
            lx = cx + 5
            p.append(f'<line class="lane" x1="{f(lx)}" x2="{f(lx)}" y1="{f(top - 8)}" y2="{f(Y(2026.6))}"/>')
            mine = sorted([r for r in evs if r['thread'] == th['id']], key=lambda r: r['date'])
            prev = top - 30
            placed = []
            for r in mine:
                rows_ = wrap(ev_short(r['title']), cw - 18, 13, 400)
                h = 16 * (1 + len(rows_))
                yd = Y(dyear(r['date']))
                by_ = max(yd - 8, prev + 8)
                placed.append((r, yd, by_, rows_, h))
                prev = by_ + h
            bottom = max(bottom, prev + 6)
            for r, yd, by_, rows_, h in placed:
                p.append(f'<path class="lead" d="M{f(lx + 5)} {f(yd)}L{f(cx + 14)} {f(by_ + 7)}"/>')
                p.append(txt(cx + 16, by_ + 11, str(r['year']), 'yr'))
                p.append(lines(cx + 16, by_ + 27, rows_, 'ev', 16))
            for r, yd, by_, rows_, h in placed:
                p.append(f'<circle class="ev-pt" cx="{f(lx)}" cy="{f(yd)}" r="4.5" data-key="{r["key"]}" data-field="year" '
                         f'data-value="{dyear(r["date"]):.3f}" data-mark="point" data-axis="y"/>')
        H = bottom + 4
    else:
        # a strip on the true time scale, then the register of events in date order
        lw = 92
        x0, x1 = lw, W - 6
        X = lambda dy: x0 + (dy - 1870) / (2027 - 1870) * (x1 - x0)
        for i, th in enumerate(threads):
            y = 18 + i * 26
            p.append(txt(0, y + 5, e(th['label']), 'lab-s'))
            p.append(f'<line class="lane" x1="{x0}" x2="{x1}" y1="{y}" y2="{y}"/>')
        ya = 18 + 4 * 26 - 8
        p.append(f'<line class="base" x1="{x0}" x2="{x1}" y1="{ya}" y2="{ya}"/>')
        for yr, anc in ((1870, 'start'), (1950, 'middle'), (2026, 'end')):
            p.append(txt(X(yr + (0.6 if yr == 2026 else 0)), ya + 18, str(yr), 'tk', anc))
        for i, th in enumerate(threads):
            y = 18 + i * 26
            for r in sorted([r for r in evs if r['thread'] == th['id']], key=lambda r: r['date']):
                p.append(f'<circle class="ev-pt sm" cx="{f(X(dyear(r["date"])))}" cy="{y}" r="3.5" data-key="{r["key"]}" '
                         f'data-field="year" data-value="{dyear(r["date"]):.3f}" data-mark="point" data-axis="x"/>')
        y = ya + 44
        p.append(txt(0, y, 'Every change, in date order', 'th'))
        y += 10
        thl = {t['id']: t['label'] for t in threads}
        for r in sorted(evs, key=lambda r: r['date']):
            rows_ = wrap(ev_short(r['title']), W - 46, 13, 400)
            p.append(f'<line class="rq" x1="0" x2="{W}" y1="{f(y)}" y2="{f(y)}"/>')
            p.append(txt(0, y + 18, str(r['year']), 'yr'))
            p.append(txt(44, y + 18, e(thl[r['thread']]), 'nt'))
            p.append(lines(44, y + 34, rows_, 'ev', 16))
            y += 26 + 16 * len(rows_)
        H = y + 4
    return ''.join(p), H


def s09_svg(W, view):
    ds = DS['history-events']
    body, H = s09_body(W)
    lab = ('Timeline of 24 rule changes from 1870 to 2026 on four threads, six each: ' + '; '.join(
        f'{th["label"]}: ' + ', '.join(f'{ev_short(r["title"])} ({r["year"]})' for r in sorted(ds['rows'], key=lambda r: r['date']) if r['thread'] == th['id'])
        for th in ds['threads']) + '.')
    return svg(W, H, f's09-{view}-{W}', lab, body)


def s09(view):
    uid = f'{view}-s09'
    ds = DS['history-events']
    cnt = Counter(r['thread'] for r in ds['rows'])
    assert set(cnt.values()) == {6} and len(ds['rows']) == 24
    title = 'The atlas dates today\'s rules to 24 changes since 1870, six on each of four threads.'
    measure = ('Rule changes in the atlas\'s history, by thread and date, United States, February 3, 1870 to June 29, 2026; '
               'one dot per change on a true time scale')
    body = f'<div class="abs">{s09_svg(866, view)}{s09_svg(560, view)}{s09_svg(328, view)}</div>'
    notes = ['Every event is on the public record: a statute, a ruling, a constitutional text or another official record.',
             'Event numbers E01 to E24 are the studio\'s, in date order. Names are shortened at the first bracket; the table gives them whole.',
             'The four threads ask who gets to vote, how votes become seats, who keeps the gains and who can check an abuse of power.']
    src = source_text('history-events')
    th = {t['id']: t['label'] for t in ds['threads']}

    def mech(r):
        m = r['mechanism']
        if '5.2%' in m:
            m += ' (5.2 percent as first published; the revised Census table reads 5.1.)'
        return e(m)
    eq = table([('ID', lambda r: (r['key'], r['key']), 'h'), ('Date', lambda r: (date_words(r['date']), r['date']), 't'),
                ('Thread', lambda r: (e(th[r['thread']]), r['thread']), 't'), ('Change', lambda r: (e(r['title']), r['title']), 't'),
                ('What it did', lambda r: (mech(r), ''), 't')], ds['rows'], 'The 24 events in date order', f'{uid}-eq',
               sortable=True, sort_col=1, sort_dir='ascending') + eq_extra(notes, src)
    return figure('S09', uid, title, measure, body, [e(n) for n in notes], src, eq, 'documented record')


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
    assert (lo['key'], hi['key']) == ('PW16', 'PW12')
    title = (f'Documented fact carries most of every everyday answer, from {slo:.0f} percent of the claims on algorithms '
             f'to {shi:.0f} percent on tap water.')
    measure = (f'Share of the claims behind each of the atlas\'s 16 everyday answers, by evidence grade, {n} claims, United States, '
               'checked through October 15, 2026')
    key = ('<ul class="grkey">' + ''.join(f'<li><span class="gsw gs-{k}" aria-hidden="true"></span><b>{lab}</b> {e(mean)}</li>' for _, lab, mean, k in GRADES)
           + '</ul>')
    head = ('<thead><tr><th scope="col">Everyday answer</th><th scope="col" class="n">Claims</th><th scope="col" class="mixc">Evidence mix</th>'
            f'<th scope="col" class="n">Documented, %</th><th scope="col" class="n">Points from all {n} claims</th></tr></thead>')
    body = []
    for r in data:
        segs = ''.join(f'<span class="gseg gs-{k}" data-key="{r["key"]}" data-field="{g}" data-value="{r[g]}" data-mark="bar" data-axis="x" '
                       f'style="width:{100 * r[g] / r["value"]:.3f}%"></span>' for g, _, _, k in GRADES if r[g])
        sh = 100 * r['documented'] / r['value']
        body.append(f'<tr><th scope="row"><span class="aq">{e(r["title"])}</span><span class="aqq">{e(r["question"])}</span></th>'
                    f'<td class="n" data-label="Claims"><span data-key="{r["key"]}" data-value="{r["value"]}" data-mark="label">{r["value"]}</span></td>'
                    f'<td class="mixc"><span class="gmix" aria-hidden="true">{segs}</span></td>'
                    f'<td class="n nb" data-label="Documented, %">{sh:.1f}</td>'
                    f'<td class="n" data-label="Points from all claims">{signed(sh - share_all)}</td></tr>')
    foot = (f'<tfoot><tr><th scope="row">All 16 answers</th><td class="n">{n}</td><td class="mixc"><span class="gmix" aria-hidden="true">'
            + ''.join(f'<span class="gseg gs-{k}" style="width:{100 * DS["claims-by-grade"]["totals"][g] / n:.3f}%"></span>' for g, _, _, k in GRADES)
            + f'</span></td><td class="n nb">{share_all:.1f}</td><td class="n">0.0</td></tr></tfoot>')
    reg = f'{key}<div class="tw"><table class="reg s10"><caption>Evidence behind each everyday answer, most documented first</caption>{head}<tbody>{"".join(body)}</tbody>{foot}</table></div>'
    notes = ['Grades are the atlas\'s own, defined on its evidence page. A claim\'s grade covers that claim, not the whole answer.',
             'The grades step from dark to light, and contested claims add a hatch, so the mix reads in grayscale. Grades never take red.',
             'Light fills fall under 3:1 against the ground; the table under "Show the table" prints every count, a studio judgment.']
    src = source_text('claims-by-grade')
    eq = table([('Answer', lambda r: (e(r['title']), r['title']), 'h'), ('Claims', lambda r: (str(r['value']), r['value']), 'n')]
               + [(lab, (lambda g: (lambda r: (str(r[g]), r[g])))(g), 'n') for g, lab, _, _ in GRADES]
               + [('Documented, %', lambda r: (f'{100 * r["documented"] / r["value"]:.1f}', 100 * r['documented'] / r['value']), 'n')],
               data, 'Claims by grade for each answer', f'{uid}-eq', sortable=True, sort_col=6) + eq_extra(notes, src)
    return figure('S10', uid, title, measure, reg, [e(n) for n in notes], src, eq, 'documented record')


# ================================================================================================ plates and views
WHY = {
    'S01': 'One figure carries the story; the party register beside it proves the agreement with two bars on one scale, and the votes '
           'sit underneath as dated context.',
    'S02': 'A line shows a level over time; the notes name the two dated events inside the plot, and breaks in method stay visible.',
    'S03': 'A ranked register answers "who" by grouping the instruments by who acted, and its direction columns let a reader read '
           'across a row and down a column.',
    'S04': 'Two dots per row show the level and the change at once; the change column says it in words and numbers.',
    'S05': 'Four panels on one scale keep each group readable on its own; the register under them carries the gaps.',
    'S06': 'A comparison table keeps V7\'s words in every cell; the glyph adds a quick reading that survives grayscale.',
    'S07': 'Equal tiles give every state the same weight, and the register beside the map lists the bans by the year they came.',
    'S08': 'One square per record lets a reader count; three bands on one year axis keep direction in position as well as tint.',
    'S09': 'Four lanes on one true time scale show when each thread changed, and every event is named on the drawing.',
    'S10': 'A register sorted by documented share answers the question row by row, with the full mix in each bar.',
}
BUILDERS = {'S01': s01, 'S02': s02, 'S03': s03, 'S04': s04, 'S05': s05, 'S06': s06, 'S07': s07, 'S08': s08, 'S09': s09, 'S10': s10}


def view_links(cur):
    return ' · '.join(f'<a href="#{v}">{t}</a>' for v, t in VIEWS if v != cur)


def contents(view):
    rws = []
    for s in D['specimens']:
        ds = DS[s['dataset']]
        src = 'Atlas V7' if ds['kind'] == 'v7' else ('Ballotpedia, secondary' if s['id'] == 'S07' else 'U.S. Census Bureau')
        rws.append(f'<tr><th scope="row"><a href="#{view}-{s["id"].lower()}">{s["id"]}</a></th><td data-label="Form">{e(s["form"])}</td>'
                   f'<td data-label="Reader question">{e(s["reader_question"])}</td><td data-label="Data">{e(src)}</td>'
                   f'<td data-label="Evidence">{e(ds["evidence"])}</td></tr>')
    return ('<div class="tw"><table class="reg rf contents"><caption>The ten specimens</caption><thead><tr><th scope="col">ID</th>'
            '<th scope="col">Form</th><th scope="col">Reader question</th><th scope="col">Data</th><th scope="col">Evidence</th></tr></thead>'
            f'<tbody>{"".join(rws)}</tbody></table></div>')


def specimen_plates(view):
    out = []
    for sid in [s['id'] for s in D['specimens']]:
        out.append(plate(view, sid, BUILDERS[sid](view), WHY[sid]))
    return ''.join(out)


def view_white():
    return (f'<section class="view g g-white" data-view-root="white" aria-labelledby="white-h"><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02</p><h1 class="display" id="white-h">Register</h1>'
            '<p class="deck">Register leads with the numbers. Every chart sits in the same frame, so a reader learns its parts once: '
            'evidence label, title, measure line, figure, notes, source and table. Under or beside each figure, a register sets out the '
            'figures a reader would look up, with tabular figures, quiet rules and an order that answers the question. Prussian and '
            'Verdigris carry the data, with Stone for context and Charcoal for the subject a title names.</p>'
            f'<p class="views">Other views: {view_links("white")}</p></header>'
            f'{contents("white")}<div class="plates">{specimen_plates("white")}</div></div></section>')


def view_newsprint():
    return ('<section class="view g g-news" data-view-root="newsprint" aria-labelledby="news-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="news-h">On Newsprint</h1>'
            '<p class="deck">The same ten specimens from the same generators, with the ground changed. Secondary text stays Deep Stone, '
            'which measures 5.49:1 here. Verdigris marks measure 3.37:1 and Stone 4.29:1, so neither carries text. The one red point '
            'takes a 1 px Charcoal keyline, since Pillar Red measures 2.96:1 on Newsprint.</p>'
            f'<p class="views">Other views: {view_links("newsprint")}</p></header>'
            f'<div class="plates">{specimen_plates("newsprint")}</div></div></section>')


def view_dark():
    t = G['dark']
    sw = [('Newsprint', 'Ink: titles, labels, the named series', t['ink']), ('Dim Newsprint', 'Secondary text', t['sec']),
          ('Stone toward Newsprint', 'Context lines', t['ctx']), ('Verdigris lifted 4%', 'Toward voters, up', t['tow']),
          ('Prussian lifted 66%', 'Away from voters, down', t['awy'])]
    rowsd = ''.join(f'<tr><th scope="row"><span class="sw2" style="background:{h}" aria-hidden="true"></span>{e(n)}</th><td data-label="Job">{e(j)}</td>'
                    f'<td data-label="Hex">{h}</td><td class="n" data-label="Contrast">{contrast(h, t["bg"]):.2f}</td>'
                    f'<td class="n" data-label="OKLab L">{oklab(h)[0]:.3f}</td></tr>' for n, j, h in sw)
    pal = ('<div class="tw"><table class="reg rf dpal"><caption>The Charcoal palette, measured against #121212</caption><thead><tr>'
           '<th scope="col">Ink</th><th scope="col">Job</th><th scope="col">Hex</th><th scope="col" class="n">Contrast</th>'
           f'<th scope="col" class="n">OKLab L</th></tr></thead><tbody>{rowsd}</tbody></table></div>')
    plates = plate('dark', 'S02', s02('dark'), WHY['S02']) + plate('dark', 'S03', s03('dark'), WHY['S03'])
    return ('<section class="view g g-dark" data-view-root="dark" aria-labelledby="dark-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="dark-h">On Charcoal</h1>'
            '<p class="deck">Two specimens on Charcoal: a line and a register. Newsprint carries the subject and the text. The palette lab '
            'found that Prussian and Verdigris, lifted the same amount, land only 0.022 apart in lightness here, so Register lifts them '
            f'unequally: Verdigris 4% toward Newsprint and Prussian 66%. The pair then sits {abs(oklab(t["tow"])[0] - oklab(t["awy"])[0]):.2f} apart in lightness and keeps its grayscale order, '
            'and every count is still printed. Pillar Red measures 4.49:1 on Charcoal and needs no keyline.</p>'
            f'{pal}<p class="views">Other views: {view_links("dark")}</p></header><div class="plates">{plates}</div></div></section>')


def view_social():
    fig = s01('social', card=True)
    return ('<section class="view g g-white" data-view-root="social" aria-labelledby="social-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="social-h">Social card</h1>'
            '<p class="deck">Specimen S01 as a portrait post at 1080 by 1350 pixels, the size Instagram and LinkedIn use. It is live type at '
            'true size, so the box below scrolls on a phone. The card keeps the frame: evidence label, title, measure line, the party '
            'register, the dated votes and the full source line.</p>'
            f'<p class="views">Other views: {view_links("social")}</p></header><div class="socialw">{fig}'
            '<aside class="cardnote" aria-label="About the card"><p class="eyebrow">Alt text for the exported image</p>'
            '<p>A card from Oath &amp; Action. Finding: Nearly nine in ten Republicans and Democrats favored a ban on stock trading by '
            'members of Congress. Bars show 88 percent of Democrats, 87 percent of Republicans and 86 percent of all registered voters, '
            'from a survey fielded May 19 to 30, 2023. The House passed a ban 232 to 198 on July 22, 2026; on September 30 the Senate '
            'voted 53 to 47 to take it up, short of the 60 votes it needed.</p>'
            '<p class="eyebrow">Rules for cards</p><ul class="bul"><li>Type keeps its system sizes, scaled once for the card: title 64 px, '
            'figures 96 px, labels 28 px, source 20 px.</li><li>The source line prints whole on the card, never in the caption only.</li>'
            '<li>Party rows share one ink and print the party name.</li><li>The wordmark sits at the foot; it is the only red on the card.</li></ul></aside>'
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
    common = [('Charcoal' if gname != 'dark' else 'Newsprint', 'Ink: titles, labels, the named series, baselines', t['ink']),
              ('Deep Stone' if gname != 'dark' else 'Dim Newsprint', 'Secondary text: measure lines, notes, sources', t['sec']),
              ('Stone' if gname != 'dark' else 'Stone toward Newsprint', 'Context series and hollow marks', t['ctx']),
              ('Gridline', 'Horizontal hairlines', t['grid']), ('Quiet rule', 'Table rows (Register tint)', t['rq']),
              ('Verdigris' if gname != 'dark' else 'Verdigris lifted 4%', 'Toward voters; up', t['tow']),
              ('Prussian' if gname != 'dark' else 'Prussian lifted 66%', 'Away from voters; down', t['awy']),
              ('Kept tint', 'Voters kept the rules (Register tint)', t['kept']),
              ('Documented', 'Grade ramp, step 1', t['g1']), ('Well supported', 'Grade ramp, step 2', t['g2']),
              ('Plausible', 'Grade ramp, step 3', t['g3']), ('Contested', 'Grade ramp, step 4, with hatch', t['g4']),
              ('Pillar Red', 'The one point a title names', LOCK['red'])]
    if gname != 'dark':
        common[12:12] = [('Up, strong', 'Diverging B, step 5', t['dv1']), ('Up, light', 'Diverging B, step 4', t['dv2']),
                         ('Midpoint', 'Diverging B, step 3', t['dv3']), ('Down, light', 'Diverging B, step 2', t['dv4']),
                         ('Down, strong', 'Diverging B, step 1', t['dv5'])]
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
    parts = [('Rule', '2 px Charcoal across the figure. It opens every figure and nothing else on the page uses it.'),
             ('Evidence label', 'Inter 700, 13/18, capitals, 0.06em. The kind (Finding, Association, Estimate, Illustration), then the grade in words.'),
             ('Title', 'Inter Tight 800, 28/32 (22/27 on phones). A sentence that states the finding, with a verb that matches the grade.'),
             ('Measure line', 'Inter 400, 15/22, Deep Stone. Measure, unit, place and period; any cropped scale is said here.'),
             ('Figure', 'The chart or the register. Wide artboard at 866 px, a 560 px artboard below that, a 328 px artboard on phones.'),
             ('Note in the drawing', 'Inter 400 or 600, 13/16, joined to its data by a 1 px leader.'),
             ('Notes', 'Inter 400, 14/20, Deep Stone, numbered, above a quiet rule. What a reader needs to read the figure fairly.'),
             ('Source line', 'Inter 400, 13/18, Deep Stone. Publisher, table, period, place, date retrieved, qualification.'),
             ('Table', '"Show the table": every value, the notes and the source, readable by a screen reader.'),
             ('Studio note', 'Dashed box beside the figure, for the guide only. Never part of a published chart.')]
    return ('<ol class="anat">' + ''.join(f'<li><b>{e(n)}</b><span>{e(d)}</span></li>' for n, d in parts) + '</ol>')


def type_ramp():
    ramp = [('Display', '"Inter Tight" 800', '56/60', '−0.035em', 'Register', 'display'),
            ('Figure title', '"Inter Tight" 800', '28/32', '−0.02em', 'A sentence that states the finding.', 'r-title'),
            ('Big figure', '"Inter Tight" 800', '128/112', '−0.04em', '86%', 'r-big'),
            ('Register figure', '"Inter Tight" 800', '22/26', '−0.01em', '24 · 17 · 9.6', 'r-fig'),
            ('Evidence label', 'Inter 700, capitals', '13/18', '0.06em', 'Finding · documented record', 'r-lab'),
            ('Measure line', 'Inter 400, Deep Stone', '15/22', '0', 'Share of registered voters, United States, 2023', 'r-meas'),
            ('Table cell', 'Inter 400, tabular', '15/22', '0', '1,080 · 95.8 · ' + MINUS + '3.7', 'r-cell'),
            ('Column head', 'Inter 600, Deep Stone', '13/18', '0', 'Documented, %', 'r-head'),
            ('Chart label', 'Inter 600, tabular', '13/16', '0', '2021: 5.1%', 'r-clab'),
            ('Note and source', 'Inter 400, Deep Stone', '13/18', '0', 'Source: U.S. Census Bureau', 'r-src')]
    rws = ''.join(f'<tr><th scope="row">{e(a)}</th><td data-label="Face">{e(b)}</td><td data-label="Size">{c}</td>'
                  f'<td data-label="Tracking">{d}</td><td data-label="Sample"><span class="{k}">{e(s)}</span></td></tr>' for a, b, c, d, s, k in ramp)
    return ('<div class="tw"><table class="reg rf ramp"><caption>Type ramp, desktop sizes in px</caption><thead><tr><th scope="col">Role</th>'
            '<th scope="col">Face</th><th scope="col">Size/line</th><th scope="col">Tracking</th><th scope="col">Sample</th></tr></thead>'
            f'<tbody>{rws}</tbody></table></div>')


def marks_sheet(W):
    """Every mark of the system at true size, with its specification, in one, two or three columns."""
    def b_lines(x, y0):
        out = []
        for i, (n, w, cls) in enumerate([('Gridline', 1, 'grid'), ('Baseline at zero', 1, 'base'), ('Leader', 1, 'lead'),
                                         ('Context series', 1.5, 'ln-ctx'), ('Small multiple series', 2.5, 'ln-sm'),
                                         ('Named series', 3, 'ln-main')]):
            y = y0 + 14 + i * 30
            out.append(f'<line class="{cls}" x1="{f(x)}" x2="{f(x + 96)}" y1="{f(y)}" y2="{f(y)}"/>')
            out.append(txt(x + 108, y + 5, e(f'{n}, {w} px'), 'nt'))
        return out, 180

    def b_dots(x, y0):
        out = []
        for i, (n, r, cls) in enumerate([('Year point, r 3', 3, 'pt-main'), ('Highlighted point, r 5.5', 5.5, 'pt-main'),
                                         ('Dumbbell, later year, r 6', 6, 'd24'), ('Dumbbell, earlier year, r 6', 6, 'd20'),
                                         ('Timeline event, r 4.5', 4.5, 'ev-pt')]):
            y = y0 + 14 + i * 30
            out.append(f'<circle class="{cls}" cx="{f(x + 8)}" cy="{f(y)}" r="{r}"/>')
            out.append(txt(x + 26, y + 5, e(n), 'nt'))
        return out, 150

    def b_other(x, y0):
        out = [f'<rect class="u-tow" x="{f(x)}" y="{f(y0 + 7)}" width="14" height="14"/>',
               f'<rect class="u-awy" x="{f(x + 16)}" y="{f(y0 + 7)}" width="14" height="14"/>',
               txt(x + 40, y0 + 19, 'Unit 14 px, gap 2', 'nt'),
               f'<rect class="bar-s" x="{f(x)}" y="{f(y0 + 39)}" width="70" height="12"/>',
               f'<rect class="u-tow" x="{f(x + 71)}" y="{f(y0 + 39)}" width="30" height="12"/>',
               txt(x + 112, y0 + 50, 'In-row bar 12 px', 'nt'),
               f'<rect class="tile-s" x="{f(x)}" y="{f(y0 + 68)}" width="40" height="40"/>',
               txt(x + 52, y0 + 86, 'Map tile 40 px,', 'nt'), txt(x + 52, y0 + 102, 'gap 4', 'nt')]
        return out, 112

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
    return svg(W, H, f'system-marks-{W}', 'Mark specimens: line weights 1, 1.5, 2.5 and 3 px; points of radius 3 to 6; '
               'units of 14 px; in-row bars of 12 px; map tiles of 40 px.', ''.join(p))


def red_demo():
    a = ('<div class="rdemo"><p class="rdh">The point the title names takes the view\'s red</p>'
         + f'<div class="rdc">{s02_svg(328, "sysa", "specimen")}</div>'
         '<p class="rdn">Pillar Red on the 2021 point, 4.17:1 on White. On Newsprint it takes a 1 px Charcoal keyline.</p></div>')
    b = ('<div class="rdemo"><p class="rdh">An ask arrives, so the point steps down to Charcoal</p>'
         + f'<div class="rdc">{s02_svg(328, "sysb", "none")}</div>'
         '<p class="rdask"><a class="ask" data-red="specimen" href="#system-red">Read how the 2021 credit was paid</a> '
         '<span class="ill">Illustrative ask</span></p>'
         '<p class="rdn">The step a reader can take now outranks the headline\'s point, so the button keeps the red and the point '
         'turns Charcoal at the same 5.5 px radius.</p></div>')
    return f'<div class="rdemos">{a}{b}</div>'


def view_system():
    t = G['white']
    dpair = ' · '.join(f'{s}: {delta_e(t["tow"], t["awy"], s if s != "normal" else None):.3f}' for s in ['normal', 'deuteranopia', 'protanopia', 'tritanopia'])
    anat_fig = s03('system')
    src_parts = [('Publisher', 'U.S. Census Bureau'), ('Title or table', 'Poverty in the United States: 2025 (P60-290), Table 8'),
                 ('Observation period', '2009 to 2025'), ('Geography', 'United States'), ('Date retrieved', 'Retrieved November 6, 2026'),
                 ('Qualification', 'Figures for 2019 to 2024 include the Bureau\'s August 2026 revision')]
    srcl = ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in src_parts)
    read = [('Start with the label.', 'It says what kind of evidence the chart holds. A Finding is measured; an Estimate depends on assumptions.'),
            ('Read the title as the claim.', 'It is one sentence, and its verb says how sure the evidence is.'),
            ('Check the measure line.', 'It says what was counted, where and when, and whether the scale starts above zero.'),
            ('Dark is the subject; gray is context.', 'The series the title names is drawn in the darkest ink.'),
            ('Look up the numbers.', 'The register under each chart prints the figures, so nothing depends on reading a bar by eye.'),
            ('Read the notes and the source.', 'They say what the figure leaves out and where the numbers came from.'),
            ('Open the table.', '"Show the table" holds every value behind the chart.')]
    readl = ''.join(f'<li><b>{e(a)}</b> {e(b)}</li>' for a, b in read)
    return ('<section class="view g g-white" data-view-root="system" aria-labelledby="sys-h" hidden><div class="wrap">'
            '<header class="vhead"><p class="eyebrow">Chart system concept 02 · Register</p><h1 class="display" id="sys-h">The system on one sheet</h1>'
            '<p class="deck">The rules a designer or a builder needs to make the next chart: the frame and its parts, the type, the marks, '
            'the palettes with measured contrast, the table rules, notes and sources, red, and a short guide for readers.</p>'
            f'<p class="views">Other views: {view_links("system")}</p></header>'
            '<section class="sys" aria-labelledby="sys-1"><h2 class="sh" id="sys-1"><span>1</span>The frame</h2>'
            '<div class="sys2"><div class="anatfig">' + plate('system', 'S03', anat_fig, WHY['S03']) + '</div>'
            f'<div><p class="sp">Every figure uses the same ten parts in the same order, so a reader learns them once.</p>{anatomy()}'
            '<p class="sp">Grid: 12 columns at 1440 px with 64 px margins and 24 px gutters; the figure takes 866 px and the studio note '
            'the rest. On phones, 16 px margins, one column, the figure first.</p></div></div></section>'
            '<section class="sys" aria-labelledby="sys-2"><h2 class="sh" id="sys-2"><span>2</span>Type</h2>'
            f'<p class="sp">Locked faces only: Inter Tight for titles and big figures, Inter for everything else, Lora Italic for quoted '
            f'words only. Every number is tabular, every minus is the true minus ({MINUS}), and nothing falls under 13 px.</p>{type_ramp()}</section>'
            '<section class="sys" aria-labelledby="sys-3"><h2 class="sh" id="sys-3"><span>3</span>Marks</h2>'
            f'<div class="cq"><div class="abs">{marks_sheet(866)}{marks_sheet(560)}{marks_sheet(328)}</div></div><ul class="bul cols2">'
            '<li>Bars start at zero; in-row bars share one scale per table, and every bar\'s value is printed.</li>'
            '<li>Lines may start above zero only when the measure line says so. Missing years and method changes break the line.</li>'
            '<li>Points sit on one straight scale per panel. Small multiples share one scale.</li>'
            '<li>Units are 14 px squares, one per record. Solid means a direction, hollow means no change, hatched means mixed, dashed means pending.</li>'
            '<li>Gridlines are horizontal hairlines with no ticks; the baseline at zero is Charcoal.</li>'
            '<li>The unit prints once, on the top tick or the first label.</li></ul></section>'
            '<section class="sys" aria-labelledby="sys-4"><h2 class="sh" id="sys-4"><span>4</span>Palettes, measured</h2>'
            '<p class="sp">Lab values come from the shared palette lab; Register\'s own tints (the quiet rule, the kept tint and the two '
            'Charcoal lifts) are mixed in OKLab from locked colors, each with one job. Contrast is WCAG 2 against the ground. Marks that '
            'carry meaning clear 3:1; light fills inside a scale sit under 3:1 only where every value is printed, a studio judgment.</p>'
            f'<p class="sp">The direction pair, Verdigris and Prussian on White, differs by OKLab distance {dpair}. Stone and Verdigris never '
            'separate two categories alone.</p>'
            f'{palette_table("white", "On White")}{palette_table("newsprint", "On Newsprint")}{palette_table("dark", "On Charcoal")}'
            '<p class="sp">Diverging scales never pair red with blue. Register tests candidate B, Prussian through the ground to Verdigris, in '
            'S06; candidate A, Stone through a neutral to Verdigris, stays with the other concepts for Gate 2. No US state map uses '
            'Prussian, so a blue state never reads as a party.</p></section>'
            '<section class="sys" aria-labelledby="sys-5"><h2 class="sh" id="sys-5"><span>5</span>Tables</h2><ul class="bul cols2">'
            '<li>Numbers sit right-aligned in tabular figures, with one count of decimals per column, so the decimal points align.</li>'
            f'<li>A change column prints its sign: +0.2, {MINUS}3.7. Zero prints as 0 in Deep Stone; a missing value prints as words.</li>'
            '<li>Column heads carry the unit, once: "Documented, %". Rows carry no unit.</li>'
            '<li>Rules stay quiet: Charcoal under the head, a quiet tint between rows, Stone above a group, Charcoal above the total.</li>'
            '<li>The default sort answers the question: ranked by value, grouped by who acted, or by date. Long tables let a reader re-sort.</li>'
            '<li>A bar inside the row shows the shape; the printed figure carries the value.</li>'
            '<li>On a phone each row reflows into labeled lines, so no table scrolls sideways.</li>'
            '<li>Group and total rows carry their own counts in bold, and they sum.</li></ul></section>'
            '<section class="sys" aria-labelledby="sys-6"><h2 class="sh" id="sys-6"><span>6</span>Notes and sources</h2><div class="sys2"><div>'
            '<ul class="bul"><li>A note inside the drawing does one job: names the record, explains an odd encoding, or gives a reader\'s scale.</li>'
            '<li>Join a note to its data with a 1 px leader or a bracket. Never hide a note behind hover.</li>'
            '<li>Notes under the figure say what the reader needs to read it fairly: revisions, breaks, coding rules, margins of error.</li>'
            '<li>Label illustrative items beside the item. Titles say what the evidence supports and nothing more.</li></ul></div>'
            f'<div><p class="sp">The source line keeps section 15 order. Shorten it only by dropping words, never facts.</p><ol class="srcl">{srcl}</ol></div></div></section>'
            '<section class="sys" id="system-red" aria-labelledby="sys-7"><h2 class="sh" id="sys-7"><span>7</span>Red</h2>'
            f'<blockquote class="rule">{e(RULE_053)}<footer>Rule 05.3 (D2-01)</footer></blockquote>'
            '<p class="sp">On a chart page red never encodes a series, a category, a grade or a scale. It may mark the one point a title names, '
            'and only when no error or ask holds the view\'s red. On the White and Newsprint views that point is S02\'s 2021 low; the Charcoal '
            'view repeats it. The two drawings below are guide specimens, so their red does not count.</p>'
            f'{red_demo()}</section>'
            '<section class="sys" aria-labelledby="sys-8"><h2 class="sh" id="sys-8"><span>8</span>How to read our charts</h2>'
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
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.g{background:var(--bg);color:var(--ink)}
.view[hidden]{display:none}
.skip{position:absolute;left:16px;top:-200px;z-index:50;padding:10px 14px;background:#FFFFFF;border:2px solid #121212;font:600 15px/1 Inter,sans-serif;color:#121212}
.skip:focus{top:12px}
/* masthead: one White chrome for every view */
.mast{background:#FFFFFF;border-bottom:1px solid #5D636D;color:#121212}
.mrow{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;min-height:72px}
.wm{display:inline-flex;color:#121212}
.wm16{display:none}
.run{margin:0 0 0 40px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#4E535B}
.tabs ul{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.tabs a{display:inline-flex;align-items:center;min-height:44px;font:600 15px/1 Inter,sans-serif;text-decoration:none;color:#121212}
.tabs a[aria-current="page"]{box-shadow:inset 0 -3px 0 #121212}
.tabs a:hover{text-decoration:underline}
/* view heads */
.vhead{padding:48px 0 40px;max-width:980px}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;margin-left:-.04em}
.deck{margin:16px 0 0;font:400 19px/29px Inter,sans-serif;max-width:46em}
.views{margin:16px 0 0;font:600 15px/23px Inter,sans-serif}
.views a{display:inline-block;min-height:24px}
.contents{margin:0 0 88px}
.contents th a{font:800 17px/1 "Inter Tight",sans-serif}
/* plates */
.plates{padding-bottom:40px}
.plate{display:grid;grid-template-columns:866px minmax(0,1fr);column-gap:56px;align-items:start;padding:0 0 104px;scroll-margin-top:24px}
.fig{margin:0;min-width:0;border-top:2px solid var(--ink);padding-top:12px;container-type:inline-size}
.elab{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.elab .gr{font-weight:400;letter-spacing:0;text-transform:none;color:var(--sec)}
.ftitle{margin:8px 0 0;font:800 28px/32px "Inter Tight",Inter,sans-serif;letter-spacing:-.02em;max-width:31em;text-wrap:balance}
.fmeasure{margin:8px 0 0;font:400 15px/22px Inter,sans-serif;color:var(--sec);max-width:50em}
.fbody{margin-top:24px}
.fnotes{margin:22px 0 0;padding:12px 0 0;border-top:1px solid var(--rq);list-style:none;counter-reset:n;font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:62em}
.fnotes li{counter-increment:n;position:relative;padding-left:22px;margin:0 0 6px}
.fnotes li::before{content:counter(n);position:absolute;left:0;top:0;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
.fsrc{margin:10px 0 0;font:400 13px/18px Inter,sans-serif;color:var(--sec);max-width:66em}
.feq{margin-top:12px;border-top:1px solid var(--rq)}
.feq>summary{display:flex;align-items:center;min-height:44px;font:600 15px/1 Inter,sans-serif;cursor:pointer;list-style:none;gap:10px}
.feq>summary::-webkit-details-marker{display:none}
.feq>summary::before{content:"+";font:700 19px/1 Inter,sans-serif;width:14px}
.feq[open]>summary::before{content:"\2212"}
.eqb{padding:4px 0 8px}
.eqn{margin-top:16px;font:400 14px/20px Inter,sans-serif;color:var(--sec);max-width:62em}
.eqn ul{margin:4px 0 12px;padding-left:18px}.eqn p{margin:0}
.eqh{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);margin:0 0 4px!important}
.vs{display:block;font-weight:400;font-size:13px;color:var(--sec)}
/* studio strip: visibly apart from the chart */
.strip{border:1px dashed var(--sec);padding:14px 16px 6px;font:400 14px/20px Inter,sans-serif;color:var(--sec);margin-top:2px;max-width:380px}
.strip p{margin:0 0 10px}
.st-k{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.st-id{font:800 22px/26px "Inter Tight",sans-serif;color:var(--ink)}
.st-id span{display:block;font:600 14px/20px Inter,sans-serif;color:var(--sec)}
.st-q span,.st-w span{display:block;font-weight:600;color:var(--ink)}
/* artboards: natural size, never shrunk below their text size */
.abs{display:block}
.ab{display:block;height:auto;max-width:none}
.abs>.ab:nth-child(1){width:var(--abw)}
.abs>.ab:nth-child(2),.abs>.ab:nth-child(3){display:none}
@container (max-width:865.98px){.abs>.ab:nth-child(1){display:none}.abs>.ab:nth-child(2){display:block;width:var(--abw)}}
@container (max-width:559.98px){.abs>.ab:nth-child(2){display:none}.abs>.ab:nth-child(3){display:block;width:100%;max-width:420px}}
.fnotes li:has(.n-only){display:none}
@container (max-width:559.98px){.fnotes li:has(.n-only){display:list-item}}
.cq{container-type:inline-size;margin-bottom:20px}
/* svg type and marks */
svg text{font-family:Inter,sans-serif;fill:var(--ink)}
svg .tk,svg .num,svg .num-b,svg .yr,svg .lab-b,svg .ty{font-variant-numeric:tabular-nums}
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
.rq{stroke:var(--rq);stroke-width:1}
.ev-pt.sm{stroke-width:1}
svg .ty{font:400 13px Inter,sans-serif}
.grid{stroke:var(--grid);stroke-width:1}
.base{stroke:var(--ink);stroke-width:1}
.lead{stroke:var(--sec);stroke-width:1;fill:none}
.brk{stroke:var(--ink);stroke-width:1;fill:none}
.comb{stroke:var(--ctx);stroke-width:1;fill:none}
.lane{stroke:var(--ctx);stroke-width:1}
.ln-main{stroke:var(--ink);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round}
.ln-sm{stroke:var(--ink);stroke-width:2.5;fill:none;stroke-linejoin:round;stroke-linecap:round}
.ln-ctx{stroke:var(--ctx);stroke-width:1.5;fill:none;stroke-linejoin:round}
.pt-main{fill:var(--ink);stroke:var(--bg);stroke-width:1}
.pt-sm{fill:var(--ink)}
.vx-ctx{fill:var(--ctx)}
.pt-red{fill:var(--red);stroke:var(--bg);stroke-width:1.5}
.g-news .pt-red{stroke:var(--ink);stroke-width:1}
.ev-pt{fill:var(--ink);stroke:var(--bg);stroke-width:1.5}
.db{stroke:var(--ctx);stroke-width:2}.db-ctx{stroke:var(--grid);stroke-width:2}
.d20{fill:none;stroke:var(--ink);stroke-width:2}
.d24{fill:var(--ink)}
.d20.c{stroke:var(--ctx)}.d24.c{fill:var(--ctx)}
.u-tow{fill:var(--tow)}.u-awy{fill:var(--awy)}
.u-kept{fill:var(--bg);stroke:var(--ctx);stroke-width:1.5}
.u-mix{fill:var(--bg);stroke:var(--ctx);stroke-width:1.5}
.u-hatch{stroke:var(--ctx);stroke-width:1.2;fill:none}
.u-pend{fill:var(--bg);stroke:var(--ink);stroke-width:1.5;stroke-dasharray:3 2}
.bar-s{fill:var(--ink)}
.tile-s{fill:var(--ink)}
/* tables: the register */
.tw{max-width:100%}
.reg{width:100%;border-collapse:collapse;font:400 15px/22px Inter,sans-serif;color:var(--ink)}
.reg .n,.reg .bt,.reg .gt,.reg [data-value]{font-variant-numeric:tabular-nums lining-nums}
.reg caption{text-align:left;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:0 0 10px}
.reg thead th{font:600 13px/18px Inter,sans-serif;color:var(--sec);text-align:left;vertical-align:bottom;padding:0 14px 8px 0;border-bottom:1px solid var(--ink)}
.reg .n{text-align:right}
.reg tbody th,.reg tbody td,.reg tfoot th,.reg tfoot td{padding:9px 14px 9px 0;border-bottom:1px solid var(--rq);text-align:left;vertical-align:top}
.reg tbody .n,.reg tfoot .n,.reg thead .n{text-align:right}
.reg tbody th{font-weight:600}
.reg tr>*:last-child{padding-right:0}
.reg tfoot th,.reg tfoot td{border-top:1px solid var(--ink);border-bottom:0;font-weight:700}
.reg .z{color:var(--sec)}
.reg .sb{all:unset;cursor:pointer;display:inline-flex;align-items:flex-end;gap:4px;min-height:24px;font:inherit;color:inherit}
.reg .sb:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.reg th[aria-sort] .sb{color:var(--ink)}
.reg th[aria-sort="ascending"] .sb::after{content:"\2191"}
.reg th[aria-sort="descending"] .sb::after{content:"\2193"}
.sw{display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-1px}
.sw-awy{background:var(--awy)}.sw-tow{background:var(--tow)}
.sw-kept{background:var(--kept)}
.sw-mix{background:repeating-linear-gradient(135deg,var(--ctx) 0 1.5px,var(--bg) 1.5px 4px);box-shadow:inset 0 0 0 1px var(--ctx)}
.sw-pend{background:var(--bg);border:1.5px dashed var(--ink)}
.sw2{display:inline-block;width:18px;height:18px;margin-right:8px;vertical-align:-4px;box-shadow:inset 0 0 0 1px rgba(127,127,127,.35)}
/* S01 */
.s01{display:grid;grid-template-columns:330px minmax(0,1fr);gap:48px;align-items:end}
.bign{margin:0;font:800 128px/112px "Inter Tight",sans-serif;letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.bign .pc{font-size:64px;letter-spacing:0;vertical-align:top;line-height:80px;margin-left:4px}
.bigc{margin:12px 0 0;font:400 17px/25px Inter,sans-serif;max-width:19em}
.regh{margin:0 0 10px;font:600 13px/18px Inter,sans-serif;color:var(--sec);border-bottom:1px solid var(--ink);padding-bottom:8px}
.prow{display:grid;grid-template-columns:120px minmax(0,1fr) 84px;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--rq)}
.pn{font:600 17px/24px Inter,sans-serif}
.ptrk{display:block;height:16px;background:var(--rq)}
.pbar{display:block;height:100%;background:var(--ink)}
.pv{font:800 28px/32px "Inter Tight",sans-serif;text-align:right;font-variant-numeric:tabular-nums}
.scale{display:flex;justify-content:space-between;margin:6px 98px 0 134px;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.s01v{margin-top:32px}
/* S03 */
.s03 .bc{width:270px}
.s03 .dc{width:74px;white-space:nowrap}
.s03 .bar{display:flex;align-items:center;gap:10px}
.s03 .trk{display:flex;flex:1 1 auto;height:14px}
.s03 .bt{flex:0 0 28px;text-align:right;font-weight:700}
.seg{display:block;height:100%;box-shadow:inset -1px 0 0 var(--bg)}
.s-awy{background:var(--awy)}.s-tow{background:var(--tow)}.s-kept{background:var(--kept)}
.s-mix{background:repeating-linear-gradient(135deg,var(--ctx) 0 1.5px,var(--bg) 1.5px 4px);box-shadow:inset 0 0 0 1px var(--ctx)}
.s-pend{background:var(--bg);box-shadow:inset 0 0 0 1.5px var(--ink)}
.rnote{display:block;font:400 13px/18px Inter,sans-serif;color:var(--sec);margin-top:2px}
.reg tr.grp th,.reg tr.grp td{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding-top:20px;border-bottom:1px solid var(--ctx)}
.reg tr.grp td{letter-spacing:0;font-size:15px}
.reg tr.grp td.bc{text-align:right;padding-right:0}
.reg tfoot td.bc{text-align:right}
.gt{font-weight:700}
/* S05 register */
.s05r{margin-top:28px;max-width:760px}
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
.s06 .sn{display:block;font-weight:400}
.s06 tr.hl .sn{font-weight:600}
.tag{display:inline-block;margin-top:6px;padding:0 6px;border:1px solid var(--ink);font:700 13px/20px Inter,sans-serif;letter-spacing:.04em;text-transform:uppercase}
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
.mapn{margin:10px 0 0;font:400 13px/18px Inter,sans-serif;color:var(--sec);max-width:528px}
.abs7{display:block}
.ab-n{display:none}
@container (max-width:820px){.s07{grid-template-columns:minmax(0,1fr)}}
@container (max-width:559.98px){.ab-wm{display:none}.ab-n{display:block;width:100%;max-width:420px}}
/* S08 */
.uc{--u:14px;--ucw:204px}
.uc-band{display:grid;grid-template-columns:var(--ucw) minmax(0,1fr);column-gap:16px;padding:10px 0 0}
.uc-lab{align-self:end;padding-bottom:4px}
.ub-n{margin:0;font:600 15px/22px Inter,sans-serif;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ub-n b{font:800 22px/26px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
.ub-s{margin:6px 0 0;font:400 13px/18px Inter,sans-serif;color:var(--sec);display:grid;gap:3px}
.ukey{display:inline-flex;align-items:center;gap:6px}
.uk{width:14px;height:14px;flex:none;display:block}
.uc-cols{display:grid;grid-template-columns:var(--c0,40px) repeat(17,minmax(0,1fr));grid-template-rows:auto auto auto;column-gap:4px;align-items:end;border-bottom:1px solid var(--ink)}
.uc-col{grid-row:3;display:flex;flex-wrap:wrap-reverse;justify-content:center;align-content:flex-start;gap:2px;padding-bottom:2px}
.uc-col:first-of-type{border-right:1px dashed var(--grid);padding-right:4px}
.u{display:block;width:var(--u);height:var(--u);flex:none}
.uc-nt{grid-row:1;margin:0 0 4px;font:400 13px/18px Inter,sans-serif;color:var(--sec);text-align:right}
.uc-br{grid-row:2;height:7px;border:1px solid var(--sec);border-bottom:0;margin:0 0 4px;align-self:end}
.uc-axis .uc-cols{border-bottom:0;align-items:start;grid-template-rows:auto}
.uy{grid-row:1;display:none;justify-self:center;white-space:nowrap;font:400 13px/18px Inter,sans-serif;color:var(--sec);padding-top:6px;font-variant-numeric:tabular-nums}
.uy.w{display:block}.uy0{display:block;justify-self:start;line-height:16px}
.uy.end{justify-self:end}
/* S10 */
.grkey{display:flex;flex-wrap:wrap;gap:6px 22px;margin:0 0 14px;padding:0;list-style:none;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.grkey li{display:inline-flex;align-items:center;gap:7px}.grkey b{color:var(--ink);font-weight:600}
.gsw{display:inline-block;width:16px;height:16px}
.gs-g1{background:var(--g1)}.gs-g2{background:var(--g2)}.gs-g3{background:var(--g3)}
.gs-g4{background:repeating-linear-gradient(135deg,var(--g2) 0 1.5px,var(--g4) 1.5px 4.5px)}
.s10 .mixc{width:300px}
.gmix{display:flex;height:14px;margin-top:4px}
.gseg{display:block;height:100%;box-shadow:inset -1px 0 0 var(--bg)}
.s10 .aq{display:block}
.s10 .aqq{display:block;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.s10 .nb{font-weight:700}
/* social card */
.socialw{display:grid;grid-template-columns:minmax(0,1104px);gap:32px;align-items:start;padding-bottom:96px}
.cardnote{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px;max-width:1104px}
.cardfig{margin:0;min-width:0}
.cardscroll{overflow:auto;width:1104px;max-width:100%;border:1px solid #5D636D;padding:11px;background:#FFFFFF}
.card{width:1080px;height:1350px;padding:84px 84px 64px;display:flex;flex-direction:column;background:var(--bg);color:var(--ink)}
.celab{margin:0;font:700 26px/32px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;border-top:4px solid var(--ink);padding-top:22px}
.celab span{font-weight:400;letter-spacing:0;text-transform:none;color:var(--sec)}
.ctitle{margin:22px 0 0;font:800 60px/64px "Inter Tight",sans-serif;letter-spacing:-.025em}
.cmeasure{margin:18px 0 0;font:400 24px/33px Inter,sans-serif;color:var(--sec)}
.crows{margin-top:40px}
.crow{display:grid;grid-template-columns:320px minmax(0,1fr) 180px;align-items:center;gap:26px;padding:12px 0;border-bottom:2px solid var(--rq)}
.crow .cn{font:600 32px/40px Inter,sans-serif}
.ctrk{display:block;height:34px;background:var(--rq)}
.cbar{display:block;height:100%;background:var(--ink)}
.crow.all .cbar{background:var(--ctx)}
.crow.all .cn{color:var(--sec)}
.cv{font:800 68px/72px "Inter Tight",sans-serif;text-align:right;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.cscale{display:flex;justify-content:space-between;margin:8px 206px 0 346px;font:400 20px/28px Inter,sans-serif;color:var(--sec)}
.cctx{margin:32px 0 0;font:400 28px/39px Inter,sans-serif}
.csrc{margin:auto 0 0;padding-top:24px;font:400 20px/28px Inter,sans-serif;color:var(--sec)}
.cfoot{display:flex;justify-content:space-between;align-items:flex-end;margin-top:28px;border-top:2px solid var(--ink);padding-top:22px;font:400 20px/28px Inter,sans-serif;color:var(--sec)}
.cfoot p{margin:0}
.cwm{display:inline-flex;color:var(--ink)}
.cardnote{font:400 15px/23px Inter,sans-serif}
.cardnote p{margin:0 0 14px}
.bul{margin:0 0 14px;padding-left:18px}.bul li{margin-bottom:6px}
/* system */
.sys{padding:0 0 72px}
.sh{display:flex;gap:14px;align-items:baseline;margin:0 0 20px;padding-top:14px;border-top:2px solid #121212;font:800 40px/44px "Inter Tight",sans-serif;letter-spacing:-.03em}
.sh span{font-size:22px;color:#4E535B}
.sp{max-width:52em;margin:0 0 16px}
.sys2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:48px;align-items:start}
.anatfig{padding-left:40px}
.anatfig .plate{grid-template-columns:minmax(0,1fr);row-gap:20px;padding-bottom:0}
.anatfig [data-anat]{position:relative}
.anatfig [data-anat]::before{content:attr(data-anat) / "";position:absolute;left:-40px;top:-2px;width:26px;height:26px;border-radius:50%;
background:#121212;color:#FFFFFF;font:700 13px/26px Inter,sans-serif;text-align:center;font-style:normal;letter-spacing:0;text-transform:none}
.anatfig .fig[data-anat]::before{top:-14px}
.anatfig .rnote[data-anat]{display:block}
.anatfig .strip{position:relative}
.anatfig .strip::before{content:"10" / "";position:absolute;left:-41px;top:-1px;width:26px;height:26px;border-radius:50%;background:#121212;color:#FFFFFF;font:700 13px/26px Inter,sans-serif;text-align:center}
.anat{margin:0 0 20px;padding:0;list-style:none;counter-reset:a;font:400 15px/22px Inter,sans-serif}
.anat li{counter-increment:a;display:grid;grid-template-columns:28px minmax(0,1fr);column-gap:8px;padding:8px 0;border-bottom:1px solid var(--rq)}
.anat li::before{content:counter(a);grid-row:span 2;font:800 17px/22px "Inter Tight",sans-serif}
.anat b{font-weight:600}
.anat span{color:var(--sec)}
.cols2{columns:2;column-gap:48px;max-width:1100px}
.cols2 li{break-inside:avoid}
.pal{margin-bottom:28px}
.ramp .display{font-size:56px;line-height:60px}
.r-title{font:800 28px/32px "Inter Tight",sans-serif;letter-spacing:-.02em}
.r-big{font:800 64px/64px "Inter Tight",sans-serif;letter-spacing:-.04em}
.r-fig{font:800 22px/26px "Inter Tight",sans-serif}
.r-lab{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.r-meas{font:400 15px/22px Inter,sans-serif;color:var(--sec)}
.r-cell{font:400 15px/22px Inter,sans-serif;font-variant-numeric:tabular-nums}
.r-head{font:600 13px/18px Inter,sans-serif;color:var(--sec)}
.r-clab{font:600 13px/16px Inter,sans-serif;font-variant-numeric:tabular-nums}
.r-src{font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.srcl{margin:0;padding:0;list-style:none;counter-reset:s}
.srcl li{counter-increment:s;display:grid;grid-template-columns:28px 150px minmax(0,1fr);gap:8px;padding:8px 0;border-bottom:1px solid var(--rq);font:400 15px/22px Inter,sans-serif}
.srcl li::before{content:counter(s);font:800 17px/22px "Inter Tight",sans-serif}
.srcl b{font-weight:600}
.rule{margin:0 0 24px;padding:4px 0 4px 20px;border-left:2px solid #121212;max-width:56em;font:400 16px/25px Inter,sans-serif}
.rule footer{margin-top:8px;font:600 13px/18px Inter,sans-serif;font-style:normal;color:#4E535B}
.rdemos{display:grid;grid-template-columns:repeat(2,minmax(0,360px));gap:48px}
.rdemo{border-top:1px solid #121212;padding-top:10px}
.rdh{margin:0 0 12px;font:600 15px/22px Inter,sans-serif}
.rdn{margin:10px 0 0;font:400 14px/20px Inter,sans-serif;color:var(--sec)}
.rdc .ab{width:328px}
.rdask{margin:12px 0 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.ask{display:inline-flex;align-items:center;min-height:48px;padding:0 18px;background:#E63946;color:#121212;font:700 19px/1 Inter,sans-serif;text-decoration:none}
.ill{font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#4E535B}
.readl{margin:0;padding-left:22px;max-width:52em}.readl li{margin-bottom:8px}
.readl b{font-weight:600}
.dpal{margin:24px 0 8px;max-width:900px}
/* footer */
.foot{border-top:1px solid #5D636D;background:#FFFFFF;color:#4E535B}
.frow{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:24px;padding-top:16px;padding-bottom:40px;font:400 13px/18px Inter,sans-serif}
.frow p{margin:0}
/* narrower desktops: the studio note moves under the figure */
@media (max-width:1309.98px){
 .plate{grid-template-columns:minmax(0,1fr);row-gap:20px}
 .strip{max-width:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:20px}
 .socialw{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:1000px){.sys2{grid-template-columns:minmax(0,1fr)}.strip{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* phones */
@media (max-width:899.98px){
 .wrap{padding:0 16px}
 .mrow{grid-template-columns:1fr;gap:4px;padding-top:14px}
 .wm24{display:none}.wm16{display:block}
 .run{display:none}
 .tabs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
 .vhead{padding:32px 0 28px}
 .display{font-size:36px;line-height:40px;letter-spacing:-.03em}
 .deck{font-size:17px;line-height:26px}
 .plate{padding-bottom:72px}
 .strip{display:block}
 .ftitle{font-size:22px;line-height:27px}
 .fbody{margin-top:18px}
 .s01{grid-template-columns:minmax(0,1fr);gap:18px}
 .bign{font-size:96px;line-height:88px}
 .bign .pc{font-size:48px;line-height:60px}
 .prow{grid-template-columns:104px minmax(0,1fr) 64px;gap:10px}
 .pv{font-size:24px}
 .scale{margin:6px 74px 0 114px}
 .s07{grid-template-columns:minmax(0,1fr);gap:24px}
 .uc{--u:12px;--ucw:1fr}
 .uc-band{grid-template-columns:minmax(0,1fr);row-gap:6px;padding-top:16px}
 .uc-lab{padding-bottom:0}
 .uc-cols{--c0:34px;column-gap:2px}
 .uc-col{gap:2px}
 .uy.w{display:none}.uy.n{display:block}.uy0{display:block}
 .ub-s{grid-template-columns:repeat(3,auto);justify-content:start;column-gap:14px}
 .cols2{columns:1}
 .sh{font-size:30px;line-height:34px}
 .rdemos{grid-template-columns:minmax(0,1fr)}
 .rdc .ab{width:100%;max-width:328px}
 .srcl li{grid-template-columns:28px minmax(0,1fr)}
 .srcl li span{grid-column:2}
 .frow{grid-template-columns:minmax(0,1fr)}
 .cardscroll{max-width:100%}
 .socialw{padding-bottom:64px}
 /* registers reflow to labeled rows */
 .reg.rf thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .reg.rf,.reg.rf tbody,.reg.rf tr,.reg.rf th,.reg.rf td{display:block;width:auto}
 .reg.rf tr{padding:10px 0;border-bottom:1px solid var(--rq)}
 .reg.rf tbody th,.reg.rf tbody td{border:0;padding:2px 0;text-align:left}
 .reg.rf td[data-label]::before{content:attr(data-label) ": ";font-weight:600;color:var(--sec)}
 .reg.rf td.n{text-align:left}
 .reg.rf caption,.s03 caption,.s10 caption,.s06 caption,.s01v caption,.s05r caption{display:block;width:auto}
 .reg.rf .sb::after{content:none}
 /* S03 register on phones */
 .s03 thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .s03,.s03 tbody,.s03 tfoot{display:block}
 .s03 tr{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));column-gap:6px;padding:10px 0;border-bottom:1px solid var(--rq)}
 .s03 tr>*{border:0!important;padding:0!important}
 .s03 tr>th{grid-column:1 / -1}
 .s03 td.bc{grid-column:1 / -1;width:auto;margin:6px 0 8px}
 .s03 td.n{text-align:left;font-size:15px}
 .s03 td.n::before{content:attr(data-label);display:block;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
 .s03 tr.grp{padding-top:22px;border-bottom:1px solid var(--ctx)}
 .s03 tr.grp td.bc{margin:4px 0;text-align:left;font-size:15px}
 .s03 tr.grp td.bc::before{content:"Rule changes: ";font-weight:600;color:var(--sec)}
 .s03 tfoot tr{border-top:1px solid var(--ink)}
 .s03 tfoot td.bc{margin:4px 0;text-align:left}
 .s03 tfoot td.bc::before{content:"Rule changes: ";font-weight:600;color:var(--sec)}
 /* S10 register on phones */
 .s10 thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .s10,.s10 tbody,.s10 tfoot{display:block}
 .s10 tr{display:grid;grid-template-columns:minmax(0,1fr) auto auto;column-gap:16px;padding:10px 0;border-bottom:1px solid var(--rq)}
 .s10 tr>*{border:0!important;padding:0!important}
 .s10 tr>th{grid-column:1 / -1}
 .s10 td.mixc{grid-column:1 / -1;width:auto;order:-1;margin:2px 0 6px;grid-row:2}
 .s10 td.n{text-align:left}
 .s10 td.n::before{content:attr(data-label);display:block;font:600 13px/18px Inter,sans-serif;color:var(--sec)}
 .s10 tfoot td.n::before{content:none}
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
 .s07r{max-width:none}
}
"""

JS = r"""
(function(){
  'use strict';
  var VIEWS=['white','newsprint','dark','social','system'];
  var first=true;
  function route(){
    var h=decodeURIComponent(location.hash.slice(1)), v=h.split('-')[0];
    if(VIEWS.indexOf(v)<0) v='white';
    [].forEach.call(document.querySelectorAll('[data-view-root]'),function(r){r.hidden=r.getAttribute('data-view-root')!==v;});
    [].forEach.call(document.querySelectorAll('.tabs a'),function(a){
      if(a.getAttribute('href')==='#'+v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');});
    var t=h.indexOf('-')>0?document.getElementById(h):null;
    if(t) t.scrollIntoView(); else if(!first) window.scrollTo(0,0);
    first=false;
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
    var r=document.querySelector('[data-view-root]:not([hidden]) h1'); if(!r) return; r.setAttribute('tabindex','-1'); r.focus(); r.scrollIntoView();});
})();
"""


def ground_css():
    out = []
    for g, cls in GCLS.items():
        out.append(f'.{cls}{{{css_vars(G[g])}}}')
    return '\n'.join(out)


def build():
    views = ' '.join(v for v, _ in VIEWS)
    body = view_white() + view_newsprint() + view_dark() + view_social() + view_system()
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Register Chart System</title>'
            f'<meta name="chart-views" content="{views}">'
            '<meta name="description" content="Chart-system concept 02 for the Oath &amp; Action brand guide: the numbers lead, every chart in one frame, with a register of the figures under it.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800'
            '&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{ground_css()}{CSS}</style></head><body>'
            '<a class="skip" href="#main">Skip to the view</a>' + masthead()
            + f'<main id="main">{body}</main>' + footer() + f'<script>{JS}</script></body></html>')
    text_only = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    assert '—' not in text_only, 'em dash in page'
    assert not re.search(r'(?:^|[\s(>])-\d', re.sub(r'<[^>]+>', ' ', text_only)), 'hyphen used as a minus'
    OUT.write_text(page)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1024:.0f} KB')


if __name__ == '__main__':
    build()
