"""Build the stretch test for chart system 01, Explainer (November 6, 2026; DR-56, DR-57, D2-115).

Six forms the ten Explainer specimens lack, drawn in the Explainer system on Newsprint from the shared chart dataset:
S11 shift arrows, S12 a tile map with a shift arrow in each tile, S13 small-multiple sparklines, S14 monthly columns
with a three-month average, S15 a sortable results table, and S16 a bubble map. Every chart comes from a generator
that takes an artboard width and returns an Art from Explainer's kit, so the label guard, the copy function, the
artboard set, the figure frame and the ground tokens are Explainer's own. This script imports Explainer's
build_concept.py by path and copies nothing from it; the sizes the new forms add sit in STRETCH_TOKENS, which the
page prints in its "New tokens" table.

Every value is read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json, and the facts a title or note
states are asserted against the rows before the page is written. Titles, measure lines and notes are studio drafts.

Run from the project root:
    python3 -I work/boards/phase-2/data-viz/stretch/build_stretch.py
Writes 20261106_Data-Viz-Stretch.html beside this file.
"""
import html
import importlib.util
import json
import math
import pathlib
import re
import sys
from collections import defaultdict

sys.dont_write_bytecode = True      # importing Explainer's module must leave no cache file in its folder

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('explainer_build', HERE.parent / '01-explainer' / 'build_concept.py')
EX = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(EX)          # Explainer builds its own page only under __main__, so this only loads the kit

copy, e, ea, f, tw, wrap, nw = EX.copy, EX.e, EX.ea, EX.f, EX.tw, EX.wrap, EX.nw
Art, Type, da, table_html = EX.Art, EX.Type, EX.da, EX.table_html
TK = EX.CHART_TOKENS
DS, SPECS = EX.DS, EX.SPECS
MINUS = EX.MINUS
HR = TK['guard']['headroom']
OUT = HERE / '20261106_Data-Viz-Stretch.html'
GEO = json.loads((EX.SHARED / 'geo/states-albers-10m.json').read_text())
TILES = EX.TILES
ORDER = ['S11', 'S12', 'S13', 'S14', 'S15', 'S16']

# ------------------------------------------------------------------------------------------------ new tokens
# Every size the six new forms add to CHART_TOKENS, in one place. The newsprint view prints this dict as its
# "New tokens" table, so the kit can adopt it whole.
STRETCH_TOKENS = {
    'arrow': {'shaft': 2, 'head_len': 8, 'head_half': 4.5, 'phone_head_len': 6, 'phone_head_half': 3.5,
              'tail_r': 2.25, 'tip_r': 0.5, 'key_points': 10},
    'shift_axis': {'pitch': 20, 'label': 14, 'break_gap': 32, 'far_segment': (-90, -80), 'near_segment': (-40, 50),
                   'tick_step': 10, 'phone_lollipop_ppp': 20, 'phone_lollipop_pitch': 44},
    'tile': {'size_max': 80, 'gap': 6, 'mid_gap': 4, 'phone_gap': 2.5, 'phone_cols': 11, 'frame': 2, 'phone_steps': (3, 6, 9)},
    'tile_arrow': {'key_points': (1, 5, 10)},
    'spark': {'px_per_point': 2.5, 'phone_px_per_point': 2.5, 'domain': (-15, 20), 'ticks': (-10, 0, 10, 20), 'line': 2,
              'context': 1.5, 'end_r': 3, 'gap_x': 30, 'phone_gap_x': 18},
    'columns': {'fill_share': 0.72, 'avg_line': 3, 'prelim_months': 2, 'vertex_r': 1.5, 'domain': (-200, 850),
                'ticks': (-200, 0, 200, 400, 600, 800), 'height': 360, 'phone_height': 290},
    'bubble': {'r_max': {'wide': 50, 'mid': 34, 'phone': 23, 'small_phone': 21}, 'gap': 2, 'outline': 1, 'ring': 2,
               'bins': (60, 65, 70, 75), 'key_millions': (1, 5, 20), 'key_seg': 64, 'label_pad': 3,
               'leader_clear': 3},
    'results': {'gap': 12, 'bar': 6, 'bar_gap': 4, 'shift_px_per_point': 6.5, 'shift_head': 8, 'shift_min': 130,
                'html_headroom': 1.06, 'two_line_min': 560},
    'tag': {'pad_x': 6, 'height': 18, 'ascent_em': 0.77, 'descent_em': 0.23},
}
ST = STRETCH_TOKENS

# Lines the guard treats as data, so no label may sit on an arrow, a sparkline or the average line
EX.LINE_KIND.update({'s-arw': 'data', 'f-head': 'data', 's-spk': 'data', 's-subd': 'data', 's-even': 'rule', 's-zero': 'rule'})


# ------------------------------------------------------------------------------------------------ data helpers
def rows(did):
    return DS[did]['rows']


SHIFT = 'presidential-shift-by-state'
SECTOR = 'payrolls-by-sector'
MONTHLY = 'payrolls-monthly-change'
TURNOUT = 'turnout-by-state-2024'
PARTY = {1: 'Republicans', -1: 'Democrats'}
LEAD = {1: 'Republican', -1: 'Democratic'}


def sgn(v):
    return 1 if v > 0 else -1


def p1(v):
    """A figure to one decimal with the true minus."""
    s = f'{abs(v):.1f}'
    return (MINUS if v < 0 else '') + s


def signed1(v):
    return ('+' if v >= 0 else MINUS) + f'{abs(v):.1f}'


def lead_text(m, short=False):
    """A margin with the leading party's name printed: 'Republican +5.5'."""
    word = {1: 'Rep.', -1: 'Dem.'}[sgn(m)] if short else LEAD[sgn(m)]
    return f'{word} +{abs(m):.1f}'


def people(thousands, sign=True):
    """A count in thousands as people say it: +3.8 million, +769,000, −245,000."""
    v = thousands
    s = ('+' if v >= 0 else MINUS) if sign else ''
    a = abs(v)
    if a >= 1000:
        return f'{s}{a / 1000:.1f} million'
    return f'{s}{round(a) * 1000:,}'


def short_name(r):
    return 'DC' if r['code'] == 'DC' else r['name']


def month_words(iso):
    y, m = iso[:4], int(iso[5:7])
    return f'{EX.MONTHS[m - 1]} {y}'


# ------------------------------------------------------------------------------------------------ facts the titles state
def shift_facts():
    R = rows(SHIFT)
    assert len(R) == 51 and all(r['shift_pts'] > 0 for r in R), 'every state and DC moved toward the Republican nominee'
    for r in R:
        assert abs(r['margin_2024'] - r['margin_2020'] - r['shift_pts']) < 0.015, r['code']
    lo, hi = min(R, key=lambda r: r['shift_pts']), max(R, key=lambda r: r['shift_pts'])
    assert (lo['name'], round(lo['shift_pts'], 2)) == ('Washington', 0.98) and (hi['name'], round(hi['shift_pts'], 2)) == ('New York', 10.54)
    flips = sorted((r for r in R if sgn(r['margin_2020']) != sgn(r['margin_2024'])), key=lambda r: r['margin_2024'])
    assert [r['name'] for r in sorted(flips, key=lambda r: r['name'])] == ['Arizona', 'Georgia', 'Michigan', 'Nevada', 'Pennsylvania', 'Wisconsin']
    assert all(sgn(r['margin_2020']) < 0 < sgn(r['margin_2024']) for r in flips)
    top4 = sorted(R, key=lambda r: -r['shift_pts'])[:4]
    assert [r['code'] for r in top4] == ['NY', 'NJ', 'FL', 'CA'] and min(r['shift_pts'] for r in top4) >= 9.0
    led24 = {s: sum(1 for r in R if sgn(r['margin_2024']) == s and r['code'] != 'DC') for s in (1, -1)}
    led20 = {s: sum(1 for r in R if sgn(r['margin_2020']) == s and r['code'] != 'DC') for s in (1, -1)}
    assert led24 == {1: 31, -1: 19} and led20 == {1: 25, -1: 25}
    return {'lo': lo, 'hi': hi, 'flips': flips, 'top4': top4, 'led24': led24, 'led20': led20}


def series(sid):
    return sorted((r for r in rows(SECTOR) if r['series_id'] == sid and r['date'] >= '2022-01-01'), key=lambda r: r['date'])


def sector_facts():
    last = {r['series_id']: r for r in rows(SECTOR) if r['date'] == '2026-09-01'}
    assert abs(last['PAYEMS']['pct_change_since_2022_01'] - 6.03) < 0.01
    losers = sorted(r['sector'] for r in last.values() if r['change_since_2022_01_thousands'] < 0)
    assert losers == ['Federal government', 'Information'], losers
    best = max((r for r in last.values() if r['series_id'] not in ('PAYEMS', 'USPRIV', 'USGOVT')), key=lambda r: r['change_since_2022_01_thousands'])
    assert best['sector'] == 'Health care and social assistance' and round(best['change_since_2022_01_thousands'] / 1000, 1) == 3.8
    return last


def monthly_facts():
    """The S14 window is every required month, January 2022 to September 2026, the span both jobs charts share."""
    req = DS[MONTHLY]['required_keys']
    D = [r for r in rows(MONTHLY) if r['key'] in set(req)]
    assert [r['key'] for r in D] == req and req[0] == '2022-01' and req[-1] == '2026-09' and len(D) == 57
    losses = [r for r in D if r['change_thousands'] < 0]
    assert len(losses) == 7
    last = D[-1]
    assert round(last['avg3_thousands']) == 51
    return {'window': D, 'losses': losses, 'last': last}


def turnout_facts():
    R = rows(TURNOUT)
    lo, hi = min(R, key=lambda r: r['voted_pct']), max(R, key=lambda r: r['voted_pct'])
    assert (lo['name'], lo['voted_pct'], hi['code'], hi['voted_pct']) == ('Arkansas', 52.8, 'DC', 79.5)
    assert max(r['moe_pct'] for r in R) == 5.6
    nat = 65.3      # the national rate in the dataset's meta notes; asserted against the note's own words below
    assert any('65.3% of 236,138 thousand citizens' in n for n in DS[TURNOUT]['meta']['notes'])
    assert sum(r['citizen_vap_thousands'] for r in R) == 236138
    big4 = sorted(R, key=lambda r: -r['citizen_vap_thousands'])[:4]
    assert [r['code'] for r in big4] == ['CA', 'TX', 'FL', 'NY']
    # below the nation beyond survey error: the state's whole 90 percent interval sits under the nation's
    below = [r for r in big4 if r['voted_pct'] + r['moe_pct'] < nat - 0.5]
    assert [r['code'] for r in below] == ['TX', 'FL', 'NY'], below
    return {'lo': lo, 'hi': hi, 'nat': nat, 'big4': big4, 'below': below}


# ------------------------------------------------------------------------------------------------ ground tokens added
# The sequential Verdigris steps come from the palette lab (five steps per ground, darkest for the most on light
# grounds, lightest for the most on Charcoal). Label inks for each step are chosen by measured contrast.
LAB_RAMP = {g: [w['hex'] for w in next(s for s in EX.LAB['sets'] if s['name'].startswith('Sequential Verdigris')
                                           and s['ground'] == lab_g)['swatches']]
            for g, lab_g in (('white', 'white'), ('news', 'newsprint'), ('dark', 'charcoal'))}


def stretch_ground(name):
    G = EX.GROUNDS[name]
    ramp = LAB_RAMP[name]
    out = {}
    light_ink, dark_ink = (EX.NEWS, EX.CHAR) if name == 'dark' else (EX.WHITE, EX.CHAR)
    for i, hx in enumerate(ramp, 1):
        out[f'q{i}'] = hx
        best = max((dark_ink, light_ink), key=lambda c: EX.contrast(c, hx))
        assert EX.contrast(best, hx) >= 4.5, (name, hx)
        out[f'qt{i}'] = best
    out['qk'] = ramp[-1] if name != 'dark' else ramp[-1]           # circle outline: the strongest step
    # S12's phone steps by size of shift: four Stone steps, darker for more on light grounds and lighter on Charcoal
    if name == 'dark':
        steps = [EX.mix(EX.STONE, EX.CHAR, 0.75), EX.mix(EX.STONE, EX.CHAR, 0.4), EX.mix(EX.STONE, EX.NEWS, 0.55), EX.mix(EX.STONE, EX.NEWS, 0.85)]
    else:
        steps = [G['lt2'], G['lt'], EX.mix(EX.STONE, EX.CHAR, 0.1), EX.mix(EX.STONE, EX.CHAR, 0.6)]
    for i, hx in enumerate(steps):
        out[f'ps{i}'] = hx
        best = max((dark_ink, EX.NEWS if name == 'news' else light_ink), key=lambda c: EX.contrast(c, hx))
        assert EX.contrast(best, hx) >= 4.5, (name, hx)
        out[f'pt{i}'] = best
    out['land'] = EX.mix(EX.NEWS, EX.WHITE, 0.45) if name == 'news' else (EX.mix(EX.STONE, EX.WHITE, 0.94) if name == 'white' else EX.mix(EX.STONE, EX.CHAR, 0.80))
    out['border'] = G['g']
    return out


SGROUNDS = {k: stretch_ground(k) for k in ('white', 'news', 'dark')}
for _g, _t in SGROUNDS.items():
    # every outline must hold 3:1 against both the ground and the land under it
    assert EX.contrast(_t['qk'], EX.GROUNDS[_g]['g']) >= 3 and EX.contrast(_t['qk'], _t['land']) >= 3, _g


# ------------------------------------------------------------------------------------------------ arrows
def arrow_h(a, x0, x1, y, r, narrow, ink='ink', scale=None):
    """A horizontal shift arrow from the 2020 margin (x0) to the 2024 margin (x1). The tail dot carries margin_2020,
    the shaft carries shift_pts as a length from its own start, and a dot at the tip carries margin_2024. The head
    is drawn over the shaft's end, so the arrow's ink ends at the 2024 margin."""
    A = ST['arrow']
    hl, hh = (A['phone_head_len'], A['phone_head_half']) if narrow else (A['head_len'], A['head_half'])
    L = x1 - x0
    hl_ = min(hl, max(L, 3.5))
    hh = hh * max(0.65, hl_ / hl)
    # the shift moved toward the Republican nominee; each end stands for the party that led in that year
    a.raw('<g data-party="Republicans" class="arw">')
    a.raw(f'<g data-party="{PARTY[sgn(r["margin_2020"])]}">')
    a.circle(x0, y, A['tail_r'], 'f-tail', da(r['key'], r['margin_2020'], field='margin_2020', mark='point', axis='x', scale=scale))
    a.raw('</g>')
    a.line(x0, y, x1, y, 's-arw', da(r['key'], r['shift_pts'], field='shift_pts', mark='bar', axis='x'))
    a.path(f'M{f(x1)} {f(y)}L{f(x1 - hl_)} {f(y - hh)}L{f(x1 - hl_)} {f(y + hh)}Z', 'f-head')
    a.raw(f'<g data-party="{PARTY[sgn(r["margin_2024"])]}">')
    a.circle(x1, y, A['tip_r'], 'f-tip', da(r['key'], r['margin_2024'], field='margin_2024', mark='point', axis='x', scale=scale))
    a.raw('</g></g>')


def arrow_at(a, tx, ty, dx, dy, narrow, attrs='', head=None):
    """An arrow from (tx, ty) to (tx + dx, ty - dy), for the tile map. The shaft carries the data; the head's
    rounded join covers the shaft's end so the ink stops at the tip."""
    A = ST['arrow']
    hl, hh = head or ((A['phone_head_len'], A['phone_head_half']) if narrow else (A['head_len'], A['head_half']))
    L = math.hypot(dx, dy)
    hl = min(hl, L * 0.9)
    hh = hh * min(1, max(0.55, L / (hl * 2.2)))
    ux, uy = dx / L, -dy / L
    px_, py_ = -uy, ux
    x1, y1 = tx + dx, ty - dy
    bx, by = x1 - ux * hl, y1 - uy * hl
    a.line(tx, ty, x1, y1, 's-arw', attrs)
    a.path(f'M{f(x1)} {f(y1)}L{f(bx + px_ * hh)} {f(by + py_ * hh)}L{f(bx - px_ * hh)} {f(by - py_ * hh)}Z', 'f-head')


def tri(a, x, y, d, size, cls='f-ink'):
    """A small pointing triangle beside the axis words: d = -1 points left, 1 points right."""
    a.path(f'M{f(x + d * size)} {f(y)}L{f(x)} {f(y - size * 0.8)}L{f(x)} {f(y + size * 0.8)}Z', cls)


# ------------------------------------------------------------------------------------------------ S11 shift arrows
def s11_scale(W, narrow, R, lab_w):
    """A margin axis with one break: the far Democratic segment holds only DC, then the axis skips to 40 points.
    Both segments keep one scale, so every arrow's length compares. The pads leave room for the labels, which sit
    outside each arrow on the side of the state's 2024 leader; the scan keeps the largest scale that fits them."""
    A, AR = ST['shift_axis'], ST['arrow']
    far, near = A['far_segment'], A['near_segment']
    G = A['break_gap']
    fs, span = far[1] - far[0], (far[1] - far[0]) + (near[1] - near[0])
    dem = [r for r in R if r['margin_2024'] < 0 and r['code'] != 'DC']
    rep = [r for r in R if r['margin_2024'] > 0 or r['code'] == 'DC']

    def make(P, k):
        def X(v):
            return P + (v - far[0]) * k if v <= far[1] + 1e-9 else P + fs * k + G + (v - near[0]) * k
        return X
    q = 12.0
    while q < W / 2:
        # the smallest left pad for this right pad, from each Democratic-led row's label width
        P = 12.0
        for r in dem:
            u = (fs + r['margin_2020'] - near[0]) / span          # X(m) = P + G + (W - P - q - G) * u
            c = lab_w(r) + 6 + AR['tail_r']
            P = max(P, (c - G - (W - q - G) * u) / (1 - u))
        k = (W - P - q - G) / span
        X = make(P, k)
        if all(X(r['margin_2024']) + 8 + lab_w(r) <= W for r in rep):
            return X, k, P, W - q
        q += 0.25
    raise AssertionError('S11 labels do not fit at this width')


TAG = 'Leader changed'


def tag_w(size=13):
    """The tag's width: its measured text plus 6 px a side, as S15's HTML tag pads it."""
    return tw(TAG, size, 600) + 2 * ST['tag']['pad_x']


def svg_tag(a, x, y, size=13):
    """The boxed "Leader changed" tag, the device S15 uses in HTML, drawn in SVG with its left edge at x on baseline y.
    The box is sized to the text, and the text sits centered in it, so the descender of the g clears the bottom rule."""
    T = ST['tag']
    w = tag_w(size)
    h = T['height'] * size / 13
    ink_mid = y - size * (T['ascent_em'] - T['descent_em']) / 2     # the middle of the letters, from the top of the d to the foot of the g
    top = ink_mid - h / 2
    assert y + size * T['descent_em'] + 1.5 <= top + h - 0.5, 'the g touches the tag rule'
    a.rect(x, top, w, h, 's-tag')
    a.text(x + w / 2, y, TAG, size, 'tl', 600, 'middle')
    return w


def national():
    """The United States row from the dataset's extra_rows, and the facts its note states."""
    US = DS[SHIFT]['extra_rows'][0]
    assert US['key'] == 'US' and US['name'] == 'United States'
    R = rows(SHIFT)
    below = [r for r in R if r['shift_pts'] < US['shift_pts']]
    big4 = sorted(R, key=lambda r: -r['total_votes_2024'])[:4]
    assert len(below) == 39 and [r['code'] for r in big4] == ['CA', 'TX', 'FL', 'NY'] and min(r['shift_pts'] for r in big4) >= 8.0
    assert abs(sum(r['total_votes_2024'] for r in R) - US['total_votes_2024']) < 1      # the nation sums from the states
    assert abs(US['margin_2024'] - US['margin_2020'] - US['shift_pts']) < 0.015 and US['margin_2020'] < 0 < US['margin_2024']
    return US, below, big4


BREAK_NOTE = 'The scale skips from 80 to 40 points on the Democratic side so DC fits. Every arrow keeps one scale.'
FLIP_HEAD = 'Six states changed leader'


def flip_body(F):
    names = [r['name'] for r in F['flips']]
    return 'from the Democratic to the Republican nominee: ' + ', '.join(names[:-1]) + f' and {names[-1]}. Each carries a tag.'


def gen_s11(W, uid, t=None):
    """Shift arrows: one row per state, sorted by its 2024 margin, each arrow from the 2020 margin to the 2024
    margin on one axis with the party names at its ends. The name and the shift sit outside the arrow on the side
    of the state's 2024 leader, so nothing but the arrows that changed leader crosses the even line. The United
    States sits above the states, under its own rule. Phones draw a ranked change lollipop instead."""
    if W < 600:
        return gen_s11_phone(W, uid, t)
    a = Art(W, uid, t)
    narrow = False
    A, AR = ST['shift_axis'], ST['arrow']
    size = A['label']
    tk = a.t.tk
    pitch = A['pitch']
    F = shift_facts()
    US, _, _ = national()
    flips = {r['code'] for r in F['flips']}
    R = sorted(rows(SHIFT), key=lambda r: (r['margin_2024'], r['code']))
    far, near = A['far_segment'], A['near_segment']
    assert all(far[0] <= r[m] <= far[1] for r in R if r['code'] == 'DC' for m in ('margin_2020', 'margin_2024'))
    assert all(near[0] <= r[m] <= near[1] for r in R + [US] if r['code'] != 'DC' for m in ('margin_2020', 'margin_2024'))

    def num(r):
        return f'{r["shift_pts"]:.1f}'

    def lab_w(r):
        w_ = (tw(short_name(r), size, 600) + tw(num(r) + ' ', size, 400)) * HR
        return w_ + (8 + tag_w() if r['code'] in flips else 0)
    X, k, x_lo, x_hi = s11_scale(W, narrow, R + [US], lab_w)
    # header: the party words at the axis ends, then the ticks
    yw, yt = 16, 42
    wl, wr = min(x_lo, X(far[0])), W
    tri(a, wl + 7, yw - 5, -1, 6)
    a.text(wl + 12, yw, 'Democratic nominee led', size, 'tl', 600)
    tri(a, wr - 7, yw - 5, 1, 6)
    a.text(wr - 12, yw, 'Republican nominee led', size, 'tl', 600, 'end')
    ticks = [far[0], far[1]] + [v for v in range(near[0], near[1] + 1, A['tick_step'])]
    y_us = yt + 22
    y_rule = y_us + pitch / 2 + 6
    y0 = y_rule + 6 + pitch / 2
    ylast = y0 + (len(R) - 1) * pitch
    yb = ylast + pitch / 2 + 20

    def tick_txt(v):
        return 'Even' if v == 0 else (f'{abs(v)} points' if v == near[1] else str(abs(v)))

    def tick_row(y):
        for v in ticks:
            if v == near[1]:
                # the figure stays centered on its tick and the unit runs to the right of it
                a.text(X(v) - tw(str(v), tk) * HR / 2, y, tick_txt(v), tk, 'tk', 400)
            else:
                a.text(X(v), y, tick_txt(v), tk, 'tk', 400, 'middle')
        # the break mark: two short slashes between the tick labels either side of the skip
        le = X(far[1]) + tw(str(abs(far[1])), tk) * HR / 2
        ri = X(near[0]) - tw(str(abs(near[0])), tk) * HR / 2
        assert ri - le >= 11, f'{uid}: no room for the break mark'
        cx = (le + ri) / 2
        for dx in (-2.75, 2.75):
            a.line(cx + dx - 1.25, y + 1, cx + dx + 1.25, y - 9, 's-mark')
    tick_row(yt)
    tick_row(yb)
    # the even line: the zero baseline, crossed only by the arrows that changed leader
    a.line(X(0), y_us - pitch / 2 - 2, X(0), ylast + pitch / 2 + 2, 's-even')

    def row(r, yc):
        x0, x1 = X(r['margin_2020']), X(r['margin_2024'])
        arrow_h(a, x0, x1, yc, r, narrow, scale='far' if r['code'] == 'DC' else None)
        lab = da(r['key'], r['shift_pts'], field='shift_pts', mark='label')
        if r['margin_2024'] < 0 and r['code'] != 'DC':
            a.rich(x0 - AR['tail_r'] - 6, yc + size * 0.36, [(short_name(r), 'tl', 600), (' ' + num(r), 'tn', 400)], size, 'end', attrs=lab)
        else:
            w_ = a.rich(x1 + 8, yc + size * 0.36, [(num(r), 'tn', 400), (' ' + short_name(r), 'tl', 600)], size, attrs=lab)
            if r['code'] in flips:
                svg_tag(a, x1 + 8 + w_ * HR + 8, yc + size * 0.36)
    # the nation first, set apart from the states by a rule
    row(US, y_us)
    a.line(0, y_rule, W, y_rule, 's-grid')
    for i, r in enumerate(R):
        row(r, y0 + i * pitch)

    # the key, in the open space right of the even line beside the Democratic-led rows
    kx = X(0) + 22
    kw = W - kx
    ky = y0 + pitch * 0.5
    eb = next(x for x in ('HOW TO READ AN ARROW', 'READING AN ARROW', 'KEY') if tw(x, 13, 700, track=0.06) * HR <= kw)
    a.text(kx, ky, eb, 13, 'te', 700, track=0.06)
    ky += 30
    kp = AR['key_points']
    s_len = kp * k                      # drawn at the chart's own scale
    sx0 = kx + AR['tail_r']
    sx1 = sx0 + s_len
    hl = AR['head_len']
    a.circle(sx0, ky, AR['tail_r'], 'f-tail')
    a.line(sx0, ky, sx1, ky, 's-arw')
    a.path(f'M{f(sx1)} {f(ky)}L{f(sx1 - hl)} {f(ky - AR["head_half"])}L{f(sx1 - hl)} {f(ky + AR["head_half"])}Z', 'f-head')
    a.text(sx1 + 8, ky + size * 0.36, f'{kp:.1f}', size, 'tn', 400)
    if s_len >= tw('2020', tk) * HR + tw('2024', tk) * HR / 2 + 6:
        a.text(sx0 - AR['tail_r'], ky + 24, '2020', tk, 'tk', 400)
        a.text(sx1, ky + 24, '2024', tk, 'tk', 400, 'middle')
        ky += 50
    else:
        ky += 30
    key_txt = ("Each arrow runs from a state's 2020 margin, at the dot, to its 2024 margin, at the tip. The figure beside "
               f'it is the shift in percentage points; this one shows {nw(kp)}, at the same scale as the chart.')
    ky = a.para(kx, ky, key_txt, kw, size, 'tn', 400, round(size * 1.36))
    ky += 28
    ky = a.para(kx, ky, BREAK_NOTE, kw, size, 'tn', 400, round(size * 1.36))
    assert ky < y0 + 19.5 * pitch, f'{uid}: key runs into the Republican-led rows'

    # the six states that changed leader, named in the open space left of their rows
    fl = [i for i, r in enumerate(R) if r['code'] in flips]
    bx = min(X(R[i]['margin_2020']) for i in fl) - AR['tail_r'] - 14
    nwid = min(bx, 300)
    nx = bx - nwid
    ny = y0 + min(fl) * pitch + 4
    ny = a.para(nx, ny, FLIP_HEAD, nwid, size, 'th', 600, round(size * 1.36))
    a.para(nx, ny + round(size * 1.36), flip_body(F), nwid, size, 'tn', 400, round(size * 1.36))
    return a, yb + 8


def gen_s11_phone(W, uid, t=None):
    """The phone form: a change lollipop. One row per state, ranked by shift, every arrow from one shared start at
    zero, with the state's 2024 leader and margin in words on the row; the nation first, under its own rule."""
    a = Art(W, uid, t)
    AR, A = ST['arrow'], ST['shift_axis']
    size = 14
    ppp = A['phone_lollipop_ppp']
    pitch = A['phone_lollipop_pitch']
    F = shift_facts()
    US, _, _ = national()
    flips = {r['code'] for r in F['flips']}
    R = sorted(rows(SHIFT), key=lambda r: (-r['shift_pts'], r['name']))
    x0 = 1.5
    assert x0 + max(r['shift_pts'] for r in R) * ppp + 7 + tw('10.5', size) * HR <= W
    y = 16
    y = a.para(0, y, 'Each arrow starts at zero and runs as far as the margin moved toward the Republican nominee, at one '
                     'scale. Under each state, its 2024 leader and margin.', W, size, 'tn', 400, 19)
    y += 34
    ticks = (0, 5, 10)

    def tick_row(yy):
        for v in ticks:
            txt = f'{v} points' if v == ticks[-1] else str(v)
            a.text(x0 + v * ppp, yy, txt, 14, 'tk', 400, 'start' if v == 0 else 'middle')
    tick_row(y)
    top = y + 8

    def row(r, yy):
        # line 1: the name, a tag where the leader changed, and the 2024 leader in words at the right
        a.text(0, yy, short_name(r), size, 'tl', 600)
        m = r['margin_2024']
        a.raw(f'<g data-party="{PARTY[sgn(m)]}">')
        a.text(W, yy, f'2024: {lead_text(m)}', size, 'tn', 400, 'end', attrs=da(r['key'], m, field='margin_2024', mark='label'))
        a.raw('</g>')
        # line 2: the arrow from the shared start, the shift, and a tag where the leader changed
        ya = yy + 16
        a.line(x0, ya - 7, x0, ya + 7, 's-base')           # the zero line, drawn beside each arrow and never through a name
        L = r['shift_pts'] * ppp
        hl = min(AR['phone_head_len'], max(L, 3.5))
        a.raw('<g data-party="Republicans" class="arw">')
        a.line(x0, ya, x0 + L, ya, 's-arw', da(r['key'], r['shift_pts'], field='shift_pts', mark='bar', axis='x'))
        a.path(f'M{f(x0 + L)} {f(ya)}L{f(x0 + L - hl)} {f(ya - AR["phone_head_half"])}L{f(x0 + L - hl)} {f(ya + AR["phone_head_half"])}Z', 'f-head')
        a.raw('</g>')
        wv = a.text(x0 + L + 7, ya + size * 0.36, f'{r["shift_pts"]:.1f}', size, 'tn', 400, attrs=da(r['key'], r['shift_pts'], field='shift_pts', mark='label'))
        if r['code'] in flips:
            svg_tag(a, x0 + L + 7 + wv * HR + 10, ya + size * 0.36)
    y += 30
    row(US, y)
    y_rule = y + 16 + 16
    a.line(0, y_rule, W, y_rule, 's-grid')
    y = y_rule + 24
    for r in R:
        row(r, y)
        y += pitch
    last = y - pitch + 16
    y = last + 34
    tick_row(y)
    return a, y + 8


def spec_s11(view):
    F = shift_facts()
    US, below, big4 = national()
    R = sorted(rows(SHIFT), key=lambda r: (r['margin_2024'], r['code']))
    lo, hi = F['lo'], F['hi']
    title = (f'The margin in every state and DC moved toward the Republican nominee from 2020 to 2024, by {lo["shift_pts"]:.1f} point in '
             f'{lo["name"]} to {hi["shift_pts"]:.1f} points in {hi["name"]}.')
    measure = ("Presidential margin by state in 2020 and 2024: the Republican nominee's share of all presidential votes "
               "minus the Democratic nominee's, in percentage points, 50 states and DC, with the United States above them")
    flips = [r['name'] for r in F['flips']]
    label = (f'Shift arrows for the United States, 50 states and DC. Every arrow points toward the Republican nominee. '
             f'The United States moved {US["shift_pts"]:.1f} points, from {lead_text(US["margin_2020"])} to {lead_text(US["margin_2024"])}. '
             f'States run from {lo["shift_pts"]:.1f} points in {lo["name"]} to {hi["shift_pts"]:.1f} in {hi["name"]}. '
             f'Six states changed leader, from the Democratic to the Republican nominee: {", ".join(flips[:-1])} and {flips[-1]}. '
             'The table under the chart lists every state.')
    body, strings = EX.artboards(view, 'S11', gen_s11, TK['artboard']['wide'], label)
    notes = ["Margin: the Republican nominee's share of all presidential votes minus the Democratic nominee's. "
             'Right of Even, the Republican nominee led; left of it, the Democratic nominee led.',
             f'The national margin moved {US["shift_pts"]:.1f} points, more than the margin in {len(below)} of the 51 states, because the '
             'states with the most voters moved most: ' + ', '.join(r['name'] for r in big4[:-1]) + f' and {big4[-1]["name"]} each moved 8 points or more.',
             "New York's figures count every ballot line each nominee held, including the Working Families and Conservative lines.",
             'Maine and Nebraska split their electoral votes by district; these margins are statewide.',
             "The 2024 figures come from the Federal Election Commission's compilation of state results, dated January 16, 2025; "
             'its Federal Elections 2024 report may revise them.']
    drawn = ['Axis: right of Even, the Republican nominee led; left of it, the Democratic nominee led. ' + BREAK_NOTE,
             f'The United States sits above the states: {lead_text(US["margin_2020"])} in 2020 to {lead_text(US["margin_2024"])} in 2024, a shift of {US["shift_pts"]:.1f}.',
             "How to read an arrow: each arrow runs from a state's 2020 margin, at the dot, to its 2024 margin, at the tip. The figure beside it is the shift in percentage points; the sample shows 10, at the same scale as the chart.",
             f'{FLIP_HEAD} {flip_body(F)}',
             'On phones the chart ranks the states by shift, each arrow from one start at zero, with the 2024 leader and margin in words on each row. '
             'Each arrow starts at zero and runs as far as the margin moved toward the Republican nominee, at one scale. Under each state, its 2024 leader and margin.']
    body_rows = [[US['name'], lead_text(US['margin_2020']), lead_text(US['margin_2024']), f'{US["shift_pts"]:.2f}']]
    body_rows += [[r['name'], lead_text(r['margin_2020']), lead_text(r['margin_2024']), f'{r["shift_pts"]:.2f}'] for r in R]
    table = table_html('Presidential margin, the United States and each state, 2020 and 2024, with the shift', ['Place', '2020 margin', '2024 margin', 'Shift toward the Republican nominee, points'], body_rows, (3,))
    return dict(sid='S11', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=drawn, table=table, wide=True, grade_line='Documented: official results the states reported, compiled by the Federal Election Commission')


# ------------------------------------------------------------------------------------------------ S12 tile map of shifts
def phone_tiles():
    """On phones the grid drops to eleven columns: Alaska and Hawaii move to the bottom row, as many newsroom maps
    place them, and every other state keeps its place."""
    out = []
    for t in TILES:
        if t['code'] == 'AK':
            out.append({**t, 'col': 0, 'row': 7})
        elif t['code'] == 'HI':
            out.append({**t, 'col': 1, 'row': 7})
        else:
            out.append({**t, 'col': t['col'] - 1})
    cells = {(t['row'], t['col']) for t in out}
    assert len(cells) == 51 and min(t['col'] for t in out) == 0 and max(t['col'] for t in out) == 10
    return out


def shift_lists(n=4):
    R = rows(SHIFT)
    big = sorted(R, key=lambda r: -r['shift_pts'])[:n]
    small = sorted(R, key=lambda r: r['shift_pts'])[:n]
    return big, small


DIRECTION_NOTE = 'All 51 arrows point right, toward the Republican nominee. A longer arrow means a larger shift.'
FRAME_NOTE = 'Frame: the leader changed, from the Democratic to the Republican nominee'
STEP_WORDS = ['Under 3 points', '3 to 5.9', '6 to 8.9', '9 or more']


def shift_step(s):
    """Phone fill step for a shift, binned on the figure as printed, to one decimal."""
    v = round(s, 1)
    return sum(1 for b in ST['tile']['phone_steps'] if v >= b)


def tile_key_arrows(a, x, base, k, narrow, hd, lbl, gap):
    """The size key: flat sample arrows at the map's own scale."""
    for sp_ in ST['tile_arrow']['key_points']:
        dx = sp_ * k
        arrow_at(a, x + 1, base, dx, 0, narrow, head=hd)
        w_ = a.text(x + 1 + dx + 8, base + lbl * 0.36, f'{sp_} point{"s" if sp_ != 1 else ""}', lbl, 'tr', 400)
        x += 1 + dx + 8 + w_ * HR + gap
    return x


def gen_s12(W, uid, t=None):
    """Tile map: one square per state on the shared tile grid. On the wide and middle maps each square holds a flat
    arrow pointing right whose length is the shift toward the Republican nominee, at one scale across the map. On
    phones, where an arrow would shrink to a speck, each square takes one of four Stone steps by the size of its shift.
    A frame marks the six states where the leader changed. The largest and smallest shifts are named under the map."""
    a = Art(W, uid, t)
    T, AR = ST['tile'], ST['arrow']
    narrow = W < 600
    R = {r['key']: r for r in rows(SHIFT)}
    F = shift_facts()
    flips = {r['code'] for r in F['flips']}
    if narrow:
        tiles, cols, gap = phone_tiles(), T['phone_cols'], T['phone_gap']
    else:
        tiles, cols, gap = TILES, 12, (T['gap'] if W >= 900 else T['mid_gap'])
    tile = min(T['size_max'], (W + gap) / cols - gap)
    pitch = tile + gap
    wide = W >= 900
    stack = W < 900          # under 900 px the key sits above the map
    pad, top_band = (8, 26) if wide else (6, 22)
    smax = max(r['shift_pts'] for r in R.values())
    k = (tile - 2 * pad) / smax          # one scale across the map: the longest arrow fills its square
    hd = (AR['head_len'], AR['head_half']) if wide else (6, 3.5)
    lbl = 14
    oy = 0
    if stack:
        y = 16
        if not narrow:
            a.text(0, y, 'SIZE OF SHIFT', 13, 'te', 700, track=0.06)
            tile_key_arrows(a, 0, y + 24, k, narrow, hd, lbl, 22)
            y += 24 + 34
        else:
            a.text(0, y, 'SIZE OF SHIFT', 13, 'te', 700, track=0.06)
            y += 26
            x = 0
            for i, wd in enumerate(STEP_WORDS):
                w_ = 22 + tw(wd, lbl) * HR
                if x > 0 and x + w_ > W:
                    x, y = 0, y + 24
                a.rect(x, y - 12, 16, 16, f'ps{i}')
                a.text(x + 22, y, wd, lbl, 'tr', 400)
                x += w_ + 16
            y += 30
            # one key arrow: every state moved the same way
            a.raw('<g data-party="Republicans">')
            arrow_at(a, 1, y - 5, 24, 0, narrow, head=(6, 3.5))
            a.raw('</g>')
            y = a.para(34, y, 'Every state moved toward the Republican nominee.', W - 34, lbl, 'tr', 400, 19) + 26
        a.rect(1, y - 13, 16, 16, 'f-lt2')
        a.rect(1, y - 13, 16, 16, 's-frame')
        lines = wrap(FRAME_NOTE, (W - 26) / HR, lbl)
        for i, ln in enumerate(lines):
            a.text(26, y + i * 19, ln, lbl, 'tr', 400)
        y += 19 * len(lines) + 4
        if not narrow:
            y = a.para(0, y + 6, DIRECTION_NOTE, W, lbl, 'tn', 400, 19)
        oy = y + 22
    for tl in tiles:
        r = R[tl['code']]
        x, y = tl['col'] * pitch, oy + tl['row'] * pitch
        a.raw('<g class="tile">')
        if narrow:
            st_ = shift_step(r['shift_pts'])
            a.rect(x, y, tile, tile, f'ps{st_}', da(r['key'], r['shift_pts'], field='shift_pts', mark='cell'))
        else:
            a.rect(x, y, tile, tile, 'f-lt2')
        if r['code'] in flips:
            a.raw('<g data-party="Republicans">')
            if narrow:
                # on phones the frame sits just outside the square, in the gap, so the code keeps 3 px of air
                assert 0 < tl['col'] < cols - 1 and shift_step(r['shift_pts']) <= 1
                a.rect(x - 1.25, y - 1.25, tile + 2.5, tile + 2.5, 's-frame')
            else:
                a.rect(x + 1, y + 1, tile - 2, tile - 2, 's-frame')
            a.raw('</g>')
        if narrow:
            cs = TK['type']['tile_code_phone']
            cw = tw(r['code'], cs, 600)
            if r['code'] in flips:
                assert (tile - cw) / 2 + 0.25 >= 3, (W, r['code'])
            a.text(x + tile / 2, y + tile / 2 + cs * 0.36, r['code'], cs, f'pt{st_}', 600, 'middle', on_mark=True)
        else:
            if wide:
                # the shift beside the code, so the arrow keeps the rest of the square
                a.rich(x + pad - 1, y + 20, [(r['code'], 'tl', 600), (f' {r["shift_pts"]:.1f}', 'tn', 400)], lbl,
                       attrs=' class="nh"' + da(r['key'], r['shift_pts'], field='shift_pts', mark='label'), on_mark=True)
            else:
                a.text(x + pad - 1, y + 16, r['code'], lbl, 'tl', 600, on_mark=True)
            dx = r['shift_pts'] * k
            ty = y + (top_band + tile - pad) / 2
            a.raw('<g data-party="Republicans">')
            arrow_at(a, x + pad, ty, dx, 0, narrow, attrs=da(r['key'], r['shift_pts'], field='shift_pts', mark='bar', axis='x'), head=hd)
            a.raw('</g>')
        a.raw('</g>')
    H = oy + 8 * pitch - gap
    big, small = shift_lists()
    if not stack:
        # the key in the open top rows
        kx, ky = pitch + 2, 16
        a.text(kx, ky, 'SIZE OF SHIFT', 13, 'te', 700, track=0.06)
        base = ky + 30
        x = tile_key_arrows(a, kx, base, k, narrow, hd, lbl, 28)
        fx = x + 12
        a.rect(fx, base - 8, 16, 16, 'f-lt2')
        a.rect(fx, base - 8, 16, 16, 's-frame')
        fw = 11 * pitch - fx - 30
        lines = wrap(FRAME_NOTE, fw / HR, lbl)
        for i, ln in enumerate(lines):
            a.text(fx + 24, base + 5 - (len(lines) - 1) * 19 / 2 + i * 19, ln, lbl, 'tr', 400)
        a.para(0, pitch + 26, DIRECTION_NOTE, 6 * pitch - gap - 12, lbl, 'tn', 400, 19)
    # under the map: the largest and smallest shifts, named, so a reader need not hunt for them
    y = H + 36
    for head, rs in (('LARGEST SHIFTS', big), ('SMALLEST SHIFTS', small)):
        y = flow_items(a, 0, y, head, [(short_name(r), f'{r["shift_pts"]:.1f}', da(r['key'], r['shift_pts'], field='shift_pts', mark='label')) for r in rs], W, lbl) + 32
    return a, y - 32 + 8


def eyebrow(a, x, y, options, W):
    """The first of several eyebrow wordings that fits the width."""
    txt = next((o for o in options if tw(o, 13, 700, track=0.06) * HR <= W - x), options[-1])
    a.text(x, y, txt, 13, 'te', 700, track=0.06)
    return txt


def flow_items(a, x0, y, head, items, W, size):
    """An eyebrow head, then name-and-figure pairs in one line that wraps between pairs, never inside one.
    Returns the baseline of the last line."""
    hw = tw(head, 13, 700, track=0.06) * HR
    inline = hw + 16 + sum((tw(n, size, 600) + tw(' ' + v, size, 400)) * HR + 20 for n, v, _ in items) <= W
    if inline:
        a.text(x0, y, head, 13, 'te', 700, track=0.06)
        x = x0 + hw + 16
    else:
        a.text(x0, y, head, 13, 'te', 700, track=0.06)
        y += 22
        x = x0
    for n, v, attrs in items:
        w = (tw(n, size, 600) + tw(' ' + v, size, 400)) * HR
        if x > x0 and x + w > x0 + W:
            x, y = x0, y + 21
        a.rich(x, y, [(n, 'tl', 600), (' ' + v, 'tn', 400)], size, attrs=attrs)
        x += w + 20
    return y


S12_WIDE_NOTE = "Each arrow's length shows the shift, at one scale across the map."
S12_PHONE_NOTE = "Each square's shade shows the size of the shift, in four steps; the lists name the largest and smallest shifts."
# notes that differ by artboard: the first shows beside the 1,024 and 600 px drawings, the second beside the 358 and 328 px ones
WIDTH_NOTES = {'S12': (S12_WIDE_NOTE, S12_PHONE_NOTE)}


def spec_s12(view):
    F = shift_facts()
    big, small = shift_lists()
    top4 = F['top4']
    title = (f'{", ".join(r["name"] for r in top4[:-1])} and {top4[-1]["name"]} moved furthest toward the Republican nominee, '
             f'each by {math.floor(min(r["shift_pts"] for r in top4)):d} points or more.')
    measure = ("Shift in the presidential margin, the Republican nominee's share of all presidential votes minus the Democratic "
               "nominee's, from 2020 to 2024, in percentage points, 50 states and DC. Each square is one state, whatever its size.")
    by_step = defaultdict(list)
    for r in rows(SHIFT):
        by_step[shift_step(r['shift_pts'])].append(r['code'])
    label = ('Tile map of 50 states and DC, one square each. On the desktop map every square holds an arrow pointing right, toward the '
             'Republican nominee, its length the shift; on phones each square is shaded by the size of its shift: '
             + '; '.join(f'{STEP_WORDS[i].lower()}: {", ".join(sorted(by_step[i]))}' for i in sorted(by_step))
             + '. Largest: ' + ', '.join(f'{r["name"]} {r["shift_pts"]:.1f}' for r in big)
             + '. Smallest: ' + ', '.join(f'{short_name(r)} {r["shift_pts"]:.1f}' for r in small)
             + '. A frame marks the six states where the leader changed. The table under the chart lists every state.')
    body, strings = EX.artboards(view, 'S12', gen_s12, TK['artboard']['wide'], label)
    notes = [S12_WIDE_NOTE,
             "New York's figures count every ballot line each nominee held, including the Working Families and Conservative lines."]
    drawn = ['Size of shift: sample arrows for 1, 5 and 10 points. ' + FRAME_NOTE + '. ' + DIRECTION_NOTE,
             'On phones each square takes one of four steps by the size of its shift: ' + ', '.join(STEP_WORDS)
             + '. Every state moved toward the Republican nominee.',
             'Largest shifts: ' + '; '.join(f'{short_name(r)} {r["shift_pts"]:.1f}' for r in big) + '. Smallest shifts: '
             + '; '.join(f'{short_name(r)} {r["shift_pts"]:.1f}' for r in small) + '.']
    R = sorted(rows(SHIFT), key=lambda r: r['name'])
    body_rows = [[r['name'], f'{r["shift_pts"]:.2f}', 'Yes' if sgn(r['margin_2020']) != sgn(r['margin_2024']) else 'No'] for r in R]
    table = table_html('Shift toward the Republican nominee by state, 2020 to 2024', ['State', 'Shift, points', 'Leader changed'], body_rows, (1,))
    return dict(sid='S12', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=drawn, table=table, wide=True,
                grade_line='Documented: official results the states reported, compiled by the Federal Election Commission')



# ------------------------------------------------------------------------------------------------ S13 sparklines
TOTALS = [('PAYEMS', 'All nonfarm jobs', 0), ('USPRIV', 'Private industries', 1), ('USGOVT', 'Government, all levels', 1),
          ('CES9091000001', 'Federal government', 2)]
PRIVATE = ['USMINE', 'USCONS', 'MANEMP', 'USWTRADE', 'USTRADE', 'CES4300000001', 'CES4422000001', 'USINFO', 'USFIRE',
           'USPBS', 'CES6561000001', 'CES6562000001', 'USLAH', 'USSERV']


def sector_check():
    """The fourteen private industries add up to total private, and private plus government is all nonfarm, so the
    panels are true parts and the totals rows above them hold the wholes."""
    last = {r['series_id']: r for r in rows(SECTOR) if r['date'] == '2026-09-01'}
    assert set(last) == set(PRIVATE) | {t[0] for t in TOTALS}
    priv = sum(last[s_]['employees_thousands'] for s_ in PRIVATE)
    assert abs(priv - last['USPRIV']['employees_thousands']) / priv < 0.002, priv
    assert abs(last['USPRIV']['employees_thousands'] + last['USGOVT']['employees_thousands'] - last['PAYEMS']['employees_thousands']) < 2
    return last


def spark_path(sid, X, Y):
    return 'M' + 'L'.join(f'{f(X(r["date"]))} {f(Y(r["pct_change_since_2022_01"]))}' for r in series(sid))


PRELIM_NOTE = ("August and September 2026 are preliminary: the Bureau of Labor Statistics revises each month's first estimate in "
               'the next two monthly reports, and a yearly benchmark revision can move earlier months.')


def gen_s13(W, uid, t=None):
    """Small-multiple sparklines on one vertical scale. The totals sit first as an indented table of sparklines (the
    whole, its two parts, and federal jobs within government), so no total reads as a peer of its parts. The
    fourteen private industries follow as panels, largest gain first, each with all nonfarm jobs as a gray line."""
    a = Art(W, uid, t)
    SP = ST['spark']
    narrow = W < 600
    last = sector_check()
    sector_facts()
    lbl = 14
    kpp = SP['phone_px_per_point'] if narrow else SP['px_per_point']
    months = [r['date'] for r in series('PAYEMS')]
    m_index = {d: i for i, d in enumerate(months)}
    n_m = len(months) - 1
    hr = HR

    def people_of(sid):
        return people(last[sid]['change_since_2022_01_thousands'])

    # ---- the totals rows
    y = 16
    eyebrow(a, 0, y, ('THE TOTAL, ITS TWO PARTS AND FEDERAL JOBS', 'THE TOTALS'), W)
    y += 14
    lo_t = min(r['pct_change_since_2022_01'] for sid, _, _ in TOTALS for r in series(sid))
    hi_t = max(r['pct_change_since_2022_01'] for sid, _, _ in TOTALS for r in series(sid))
    above, below = math.ceil(hi_t) * kpp + 6, math.ceil(-lo_t) * kpp + 6
    if not narrow:
        name_w = 220
        sx0, sw = name_w, min(300, W - name_w - 300)
        vx = sx0 + sw + 26
        px_ = vx + 150
    else:
        pct_w = max(tw(signed1(last[sid]['pct_change_since_2022_01']) + '%', lbl) for sid, _, _ in TOTALS) * HR
        val_w = max(tw(people(last[sid]['change_since_2022_01_thousands']), lbl, 600) for sid, _, _ in TOTALS) * HR
        px_ = W
        vx = W - pct_w - 10
        sx0 = 2 * 18 + 6                 # past the deepest indent, so the tree connectors never cross a sparkline
        sw = vx - val_w - 14 - sx0
    name_base = {}
    below_extra = 0
    for sid, nm, lev in TOTALS:
        r_last = last[sid]
        if narrow:
            y += 22
            a.text(lev * 18, y, nm, lbl, 'tl' if lev else 'th', 600)
            y_name = y
            y += 6
        top = y + 4
        zero = top + above
        Xs = lambda d, sx0=sx0, sw=sw: sx0 + m_index[d] / n_m * sw
        Ys = lambda v, zero=zero: zero - v * kpp
        if lev:
            a.line(sx0, zero, sx0 + sw, zero, 's-zero')
        else:
            a.line(sx0, zero, sx0 + sw, zero, 's-zero')
        a.path(spark_path(sid, Xs, Ys), 's-spk')
        a.circle(Xs(r_last['date']), Ys(r_last['pct_change_since_2022_01']), SP['end_r'], 'f-ink',
                 da(r_last['key'], r_last['pct_change_since_2022_01'], mark='point', axis='y', scale=f'band-{sid}'))
        base = zero + 5
        if not narrow:
            a.text(lev * 18, base, nm, lbl, 'tl' if lev else 'th', 600)
            name_base[sid] = base
        else:
            name_base[sid] = y_name
        a.text(vx, base, people_of(sid), lbl, 'th', 600, 'start' if not narrow else 'end',
               attrs=da(r_last['key'], r_last['change_since_2022_01_thousands'], field='change_since_2022_01_thousands', mark='label'))
        a.text(px_, base, signed1(r_last['pct_change_since_2022_01']) + '%', lbl, 'tn', 400, 'end',
               attrs=da(r_last['key'], r_last['pct_change_since_2022_01'], mark='label'))
        if sid == 'CES9091000001':
            # the federal row: its peak and its latest level, dated, and no cause
            S_ = series(sid)
            pk = max(S_, key=lambda r: r['employees_thousands'])
            a.circle(Xs(pk['date']), Ys(pk['pct_change_since_2022_01']), 2.5, 'f-ink',
                     da(pk['key'], pk['pct_change_since_2022_01'], mark='point', axis='y', scale=f'band-{sid}'))
            fed_lines = [(f'Peak: {pk["employees_thousands"] * 1000:,.0f} in {month_words(pk["date"])}', pk),
                         (f'{month_words(r_last["date"])}: {r_last["employees_thousands"] * 1000:,.0f}', r_last)]
            if W >= 900:
                fx_ = px_ + 24
                for j, (txt, rr_) in enumerate(fed_lines):
                    a.text(fx_, zero - 6 + j * 19, txt, lbl, 'tn', 400, attrs=da(rr_['key'], rr_['employees_thousands'], field='employees_thousands', mark='label'))
            else:
                yy = zero + below + 8
                for j, (txt, rr_) in enumerate(fed_lines):
                    a.text(sx0, yy + j * 19, txt, lbl, 'tn', 400, attrs=da(rr_['key'], rr_['employees_thousands'], field='employees_thousands', mark='label'))
                below_extra = 8 + 19 + 6
        y = zero + below + (below_extra if sid == 'CES9091000001' and W < 900 else 0)
    # a tree connector shows which rows are parts of which: all jobs holds private and government; government holds federal
    for parent, kids, lev in (('PAYEMS', ('USPRIV', 'USGOVT'), 0), ('USGOVT', ('CES9091000001',), 1)):
        cx = lev * 18 + 5
        a.path(f'M{f(cx)} {f(name_base[parent] + 6)}V{f(name_base[kids[-1]] - 5)}H{f(cx + 8)}', 's-ld')
        for kd in kids[:-1]:
            a.line(cx, name_base[kd] - 5, cx + 8, name_base[kd] - 5, 's-ld')
    # ---- the fourteen private industries
    y += 34
    eb_ = 'PRIVATE INDUSTRIES, LARGEST PERCENT GAIN FIRST'
    if tw(eb_, 13, 700, track=0.06) * HR <= W:
        a.text(0, y, eb_, 13, 'te', 700, track=0.06)
    else:
        a.text(0, y, 'PRIVATE INDUSTRIES,', 13, 'te', 700, track=0.06)
        y += 19
        a.text(0, y, 'LARGEST PERCENT GAIN FIRST', 13, 'te', 700, track=0.06)
    y += 22
    # the gray line, explained once, in its own ink
    a.line(0, y - 5, 22, y - 5, 's-ctx15')
    y = a.para(30, y, f'Gray line in every panel: all nonfarm jobs, {signed1(last["PAYEMS"]["pct_change_since_2022_01"])}%', W - 30, lbl, 'tn', 400, 19)
    y += 18
    order = sorted(PRIVATE, key=lambda s_: -last[s_]['pct_change_since_2022_01'])
    lo, hi = SP['domain']
    assert all(lo <= r['pct_change_since_2022_01'] <= hi for s_ in PRIVATE + ['PAYEMS'] for r in series(s_))
    cols = 4 if W >= 900 else (3 if W >= 600 else 2)
    gut = 52 if not narrow else 56
    gx = SP['gap_x'] if not narrow else SP['phone_gap_x']
    pw = (W - gut - gx * (cols - 1)) / cols
    ph = (hi - lo) * kpp
    name_lines = {s_: wrap(last[s_]['sector'], pw / hr, lbl, 600) for s_ in order}
    for ri in range(math.ceil(len(order) / cols)):
        row_ids = order[ri * cols:(ri + 1) * cols]
        nl = max(len(name_lines[s_]) for s_ in row_ids)
        head_h = nl * 18
        two_row = any((tw(people_of(s_) + ',', lbl, 600) + tw(' ' + signed1(last[s_]['pct_change_since_2022_01']) + '%', lbl, 400)) * hr > pw
                      for s_ in row_ids)
        ptop = y + head_h + 30 + (18 if two_row else 0)      # room for a two-line end label above a gain near the top
        Y = lambda v, ptop=ptop: ptop + (hi - v) * kpp
        top_tick = max(SP['ticks'])
        for v in SP['ticks']:
            a.text(gut - 8, Y(v) + 4.5, (f'+{v}%' if v == top_tick else (f'+{v}' if v > 0 else ('0' if v == 0 else f'{MINUS}{-v}'))), 13 if not narrow else 14, 'tk', 400, 'end')
        year_y = Y(lo) + 22
        for ci, s_ in enumerate(row_ids):
            px0 = gut + ci * (pw + gx)
            inset = SP['end_r'] + 2          # the end dot stays clear of the panel's right edge
            X = lambda d, px0=px0: px0 + m_index[d] / n_m * (pw - inset)
            for i, ln in enumerate(name_lines[s_]):
                a.text(px0, y + 14 + i * 18, ln, lbl, 'tl', 600)
            for v in SP['ticks']:
                if v:
                    a.line(px0, Y(v), px0 + pw, Y(v), 's-grid')
            S_ = series(s_)
            area = (f'M{f(X(S_[0]["date"]))} {f(Y(0))}' + ''.join(f'L{f(X(r["date"]))} {f(Y(r["pct_change_since_2022_01"]))}' for r in S_)
                    + f'L{f(X(S_[-1]["date"]))} {f(Y(0))}Z')
            a.path(area, 'f-area')
            a.line(px0, Y(0), px0 + pw, Y(0), 's-zero')
            a.path(spark_path('PAYEMS', X, Y), 's-ctx15')
            a.path(spark_path(s_, X, Y), 's-spk')
            rl = last[s_]
            ex, ey = X(rl['date']), Y(rl['pct_change_since_2022_01'])
            a.circle(ex, ey, SP['end_r'], 'f-ink', da(rl['key'], rl['pct_change_since_2022_01'], mark='point', axis='y', scale=f'row-{ri}'))
            # the end label: the change in jobs and in percent, above a gain and below a loss, clear of both lines;
            # one line where it fits the panel, else two
            t1, t2 = people_of(s_), signed1(rl['pct_change_since_2022_01']) + '%'
            one = (tw(t1 + ',', lbl, 600) + tw(' ' + t2, lbl, 400)) * hr
            two = one > pw
            lw_ = max(tw(t1, lbl, 600), tw(t2, lbl, 400)) * hr if two else one
            lx = max(px0, min(ex - lw_ * 0.5, px0 + pw - lw_))
            gain = rl['change_since_2022_01_thousands'] >= 0
            near = [Y(r['pct_change_since_2022_01']) for s2 in (s_, 'PAYEMS') for r in series(s2) if lx - 2 <= X(r['date']) <= lx + lw_ + 2]
            la = da(rl['key'], rl['change_since_2022_01_thousands'], field='change_since_2022_01_thousands', mark='label')
            lb = da(rl['key'], rl['pct_change_since_2022_01'], mark='label')
            if gain:
                ly2 = min(near + [ey]) - 9
                ly1 = ly2 - 18 if two else ly2
            else:
                ly1 = max(near + [ey]) + lbl + 7
                ly2 = ly1 + 18 if two else ly1
            if two:
                a.text(lx, ly1, t1, lbl, 'th', 600, attrs=la)
                a.text(lx, ly2, t2, lbl, 'tn', 400, attrs=lb)
            else:
                a.rich(lx, ly1, [(t1 + ',', 'th', 600), (' ' + t2, 'tn', 400)], lbl, attrs=la)
            year_y = max(year_y, ly2 + 22)
        for ci, s_ in enumerate(row_ids):
            px0 = gut + ci * (pw + gx)
            a.text(px0, year_y, '2022', 13 if not narrow else 14, 'tk', 400)
            a.text(px0 + pw, year_y, '2026', 13 if not narrow else 14, 'tk', 400, 'end')
        y = year_y + 30
    return a, y - 30 + 8


def spec_s13(view):
    last = sector_facts()
    sector_check()
    hc = last['CES6562000001']
    sl_change = last['USGOVT']['change_since_2022_01_thousands'] - last['CES9091000001']['change_since_2022_01_thousands']
    assert sl_change > 0 and round(sl_change / 1000, 1) == 1.5
    fed_pk = max(series('CES9091000001'), key=lambda r: r['employees_thousands'])
    fed_last = last['CES9091000001']
    assert (fed_pk['date'], fed_pk['employees_thousands'], fed_last['employees_thousands']) == ('2024-10-01', 3013.0, 2682.0)
    title = (f'Health care and social assistance added {people(hc["change_since_2022_01_thousands"], sign=False)} jobs from January 2022 '
             'to September 2026, the most of any industry; information and the federal government lost jobs.')
    measure = ('Payroll jobs by industry, seasonally adjusted, change since January 2022 in percent, United States, '
               'January 2022 to September 2026, the span both jobs charts share. Every sparkline shares one vertical scale; '
               'labels give the change in jobs and in percent.')
    order = sorted(PRIVATE, key=lambda s_: -last[s_]['pct_change_since_2022_01'])
    label = ('Sparklines of payroll jobs since January 2022. Totals: ' + '; '.join(
        f'{nm}, {people(last[sid]["change_since_2022_01_thousands"])} jobs, {signed1(last[sid]["pct_change_since_2022_01"])} percent' for sid, nm, _ in TOTALS)
        + '. Private industries, largest percent gain first: ' + '; '.join(
        f'{last[s_]["sector"]}, {people(last[s_]["change_since_2022_01_thousands"])}, {signed1(last[s_]["pct_change_since_2022_01"])} percent' for s_ in order) + '.')
    body, strings = EX.artboards(view, 'S13', gen_s13, TK['artboard']['wide'], label)
    notes = ['The first rows hold the totals: all nonfarm jobs, its two parts, private industries and government, and federal jobs, which are part of government. '
             'The fourteen panels below add up to private industries.',
             f'Government, all levels, gained {people(last["USGOVT"]["change_since_2022_01_thousands"], sign=False)} jobs and federal jobs fell by '
             f'{people(-last["CES9091000001"]["change_since_2022_01_thousands"], sign=False)}, so state and local payrolls, which this dataset does not '
             f'carry on their own, grew by about {people(sl_change, sign=False)}.',
             PRELIM_NOTE]
    drawn = ['The total, its two parts and federal jobs: ' + '; '.join(f'{nm} {people(last[sid]["change_since_2022_01_thousands"])}, {signed1(last[sid]["pct_change_since_2022_01"])}%' for sid, nm, _ in TOTALS) + '.',
             f'Private industries, largest percent gain first. Gray line in every panel: all nonfarm jobs, {signed1(last["PAYEMS"]["pct_change_since_2022_01"])}%. '
             'Each panel ends with the change in jobs and in percent since January 2022, and its scale runs from −15 to +20 percent, January 2022 to September 2026.',
             f'Federal government: peak {fed_pk["employees_thousands"] * 1000:,.0f} in {month_words(fed_pk["date"])}; '
             f'{fed_last["employees_thousands"] * 1000:,.0f} in {month_words(fed_last["date"])}.']
    body_rows = [[nm, people(last[sid]['change_since_2022_01_thousands']), signed1(last[sid]['pct_change_since_2022_01']), f'{last[sid]["employees_thousands"]:,.0f}']
                 for sid, nm, _ in TOTALS]
    body_rows += [[last[s_]['sector'], people(last[s_]['change_since_2022_01_thousands']), signed1(last[s_]['pct_change_since_2022_01']), f'{last[s_]["employees_thousands"]:,.0f}'] for s_ in order]
    table = table_html('Change in payroll jobs since January 2022, as of September 2026', ['Series', 'Change in jobs', 'Change, percent', 'Jobs, thousands, September 2026'], body_rows, (1, 2, 3))
    return dict(sid='S13', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=drawn, table=table, wide=True,
                grade_line='Official statistic: a Bureau of Labor Statistics survey of employers, as copied by FRED')



# ------------------------------------------------------------------------------------------------ S14 columns and average
def boxes_clear(box, rects, pad=3, rules=()):
    """True when a label box keeps clear of every column, so no label sits on a Stone mark, and of every gridline,
    so no line runs behind a word."""
    x0, y0, x1, y1 = box
    if any(y0 - 1 <= gy <= y1 + 1 for gy in rules):
        return False
    return all(x1 + pad <= rx or x0 - pad >= rx + rw or y1 + pad <= ry or y0 - pad >= ry + rh for rx, ry, rw, rh in rects)


def gen_s14(W, uid, t=None):
    """Columns from zero in Stone for each month's change, the three-month average as the Charcoal line over them,
    the two preliminary months hatched and the average dashed where it leans on them, and the latest month labeled.
    The chart draws January 2022 to September 2026, the span both jobs charts share."""
    a = Art(W, uid, t)
    C = ST['columns']
    narrow = W < 600
    lbl = 14
    tk = a.t.tk
    F = monthly_facts()
    D = F['window']
    lo, hi = C['domain']
    assert lo < min(r['change_thousands'] for r in D) and max(r['change_thousands'] for r in D) < hi
    prelim = {r['key'] for r in D[-C['prelim_months']:]}
    ticks = C['ticks']

    def tick_txt(v):
        return '0' if v == 0 else (('+' if v > 0 else MINUS) + f'{abs(v) * 1000:,}')
    gut = max(tw(tick_txt(v), tk) for v in ticks) * HR + 10
    # the key: what a column is, and the hatch for preliminary months
    y = 16
    kx = 0
    a.rect(kx, y - 11, 14, 14, 'f-ctx')
    w1 = a.text(kx + 21, y, 'Jobs added or lost in the month', lbl, 'tr', 400)
    x2 = kx + 21 + w1 * HR + 22
    items2 = 'Preliminary: August and September 2026'
    if x2 + 21 + tw(items2, lbl) * HR > W:
        x2, y = 0, y + 24
    a.rect(x2 + 0.75, y - 10.25, 12.5, 12.5, 'hatchf', f' style="fill:{a.hatch()}"')
    a.rect(x2 + 0.75, y - 10.25, 12.5, 12.5, 's-ctx15 nofill')
    y = a.para(x2 + 21, y, items2, W - x2 - 21, lbl, 'tr', 400, 19)
    top = y + 34
    ph = C['height'] if not narrow else C['phone_height']
    k = ph / (hi - lo)
    x0, x1 = gut, W - 2

    def Y(v):
        return top + (hi - v) * k
    pitch = (x1 - x0) / len(D)
    bw = pitch * C['fill_share']

    def X(i):
        return x0 + i * pitch + pitch / 2
    for v in ticks:
        if v:
            a.line(x0, Y(v), x1, Y(v), 's-grid')
        a.text(gut - 8, Y(v) + 4.5, tick_txt(v), tk, 'tk', 400, 'end')
    rects = []
    for i, r in enumerate(D):
        v = r['change_thousands']
        bx, by, bh = X(i) - bw / 2, Y(max(v, 0)), abs(v) * k
        rects.append((bx, by, bw, bh))
        attrs = da(r['key'], v, mark='bar', axis='y')
        if r['key'] in prelim:
            a.rect(bx, by, bw, bh, 'hatchf', f' style="fill:{a.hatch()}"' + attrs)
            a.rect(bx + 0.75, by + 0.75, bw - 1.5, bh - 1.5, 's-ctx15 nofill')
        else:
            a.rect(bx, by, bw, bh, 'f-ctx', attrs)
    a.line(x0, Y(0), x1, Y(0), 's-base')
    # year labels at January
    for i, r in enumerate(D):
        if r['key'].endswith('-01'):
            a.text(X(i), Y(lo) + 22, r['key'][:4], tk, 'tk', 400, 'middle')
    # the average: solid where every month in it is final, dashed where it leans on a preliminary month
    pts = [(X(i), Y(r['avg3_thousands'])) for i, r in enumerate(D)]
    n_final = len(D) - C['prelim_months']
    a.path('M' + 'L'.join(f'{f(x)} {f(y_)}' for x, y_ in pts), 's-case')        # a ground-colored casing, so the line parts from the columns it crosses
    a.path('M' + 'L'.join(f'{f(x)} {f(y_)}' for x, y_ in pts[:n_final]), 's-sub')
    a.path('M' + 'L'.join(f'{f(x)} {f(y_)}' for x, y_ in pts[n_final - 1:]), 's-subd')
    for i, r in enumerate(D):
        a.circle(pts[i][0], pts[i][1], C['vertex_r'], 'f-ink', da(r['key'], r['avg3_thousands'], field='avg3_thousands', mark='point', axis='y'))

    def place_text(lines, x, y_last, anchor='start', size=lbl):
        """Set one to three lines ending at baseline y_last; returns their box. The caller checks it."""
        lh = round(size * 1.36)
        ws = [tw(ln, size, 600 if j == 0 else 400) * HR for j, ln in enumerate(lines)]
        wmax = max(ws)
        bx0 = x if anchor == 'start' else x - wmax
        y_first = y_last - (len(lines) - 1) * lh
        return (bx0, y_first - 0.97 * size, bx0 + wmax, y_last + 0.25 * size), y_first, lh

    def put(lines, x, y_last, anchor='start', attrs=''):
        box, y_first, lh = place_text(lines, x, y_last, anchor)
        for j, ln in enumerate(lines):
            a.text(x, y_first + j * lh, ln, lbl, 'th' if j == 0 else 'tn', 600 if j == 0 else 400, anchor,
                   attrs=attrs if j == 0 else '')
        return box
    grid_y = [Y(v) for v in ticks if v]
    # the latest month, labeled above everything to its left and joined to its column by a leader
    last = D[-1]
    lines = [f'{people(last["change_thousands"])} jobs', f'in {month_words(last["key"])}, preliminary']
    yl = Y(last['change_thousands']) - 46
    while not boxes_clear(place_text(lines, x1, yl, 'end')[0], rects, rules=grid_y):
        yl -= 1
    box = put(lines, x1, yl, 'end', da(last['key'], last['change_thousands'], mark='label'))
    a.leader([(X(len(D) - 1), box[3] + 3), (X(len(D) - 1), Y(last['change_thousands']) - 4)])
    if W >= 700:
        # the average, named on the line in the open space of 2023
        i_lab = next(i for i, r in enumerate(D) if r['key'] == '2023-06')
        al = ['Three-month average']
        yl = pts[i_lab][1] - 30
        while not boxes_clear(place_text(al, X(i_lab - 2), yl)[0], rects, rules=grid_y):
            yl -= 1
        box = put(al, X(i_lab - 2), yl)
        a.leader([(X(i_lab), box[3] + 3), (X(i_lab), pts[i_lab][1] - 5)])
        # the months with a loss, counted once, in the open space under zero before the first of them
        first_loss = next(i for i, r in enumerate(D) if r['change_thousands'] < 0)
        ll = [f'{nw(len(F["losses"]), cap=True)} months with a loss']
        fl = D[first_loss]
        nx_ = X(first_loss) - bw / 2 - 30
        box, y_first, lh = place_text(ll, nx_, Y(0) + 34, 'end')
        assert boxes_clear(box, rects, rules=grid_y), 'the losses note crosses a column or gridline'
        put(ll, nx_, Y(0) + 34, 'end')
        a.leader([(box[2] + 5, y_first - 5), (X(first_loss) - bw / 2 - 3, Y(fl['change_thousands'] / 2))])
        end = Y(lo) + 30
    else:
        end = Y(lo) + 30
        y = end + 10
        a.line(0, y - 5, 24, y - 5, 's-sub')
        y = a.para(32, y, 'Three-month average', W - 32, lbl, 'tr', 400, 19) + 28
        y = a.para(0, y, f'{nw(len(F["losses"]), cap=True)} months show a loss: {loss_months(F)}.', W, lbl, 'tn', 400, 19)
        end = y + 4
    return a, end


def loss_months(F):
    """The months with a loss, named in date order with the year once per run, and no period split."""
    by_year = defaultdict(list)
    for r in F['losses']:
        by_year[r['key'][:4]].append(EX.MONTHS[int(r['key'][5:]) - 1])
    parts = []
    for yr in sorted(by_year):
        ms = by_year[yr]
        parts.append((', '.join(ms[:-1]) + f' and {ms[-1]}' if len(ms) > 1 else ms[0]) + f' {yr}')
    return ', and '.join(parts) if len(parts) == 2 else ', '.join(parts)


def spec_s14(view):
    F = monthly_facts()
    D = F['window']
    title = (f'The three-month average of monthly job change stood at {people(F["last"]["avg3_thousands"], sign=False)} in '
             f'September 2026, a preliminary figure, and payrolls shrank in {nw(len(F["losses"]))} of the {len(D)} months charted.')
    measure = ('Monthly change in payroll jobs, all nonfarm, seasonally adjusted, United States, January 2022 to September 2026, '
               'the span both jobs charts share, with the three-month average. The scale runs from −200,000 to +850,000.')
    label = (f'Column chart of the monthly change in jobs from January 2022 to September 2026, with the three-month average as a line. '
             f'The average stood at {people(F["last"]["avg3_thousands"], sign=False)} in September 2026, a preliminary figure. '
             f'Months with a loss: ' + ', '.join(f'{month_words(r["key"])} ({people(r["change_thousands"])})' for r in F['losses'])
             + f'. The latest month, September 2026, shows {people(D[-1]["change_thousands"])}, preliminary.')
    body, strings = EX.artboards(view, 'S14', gen_s14, TK['artboard']['reading'], label)
    notes = ["The three-month average for a month is the mean of that month's change and the two before it.",
             PRELIM_NOTE + ' The average is dashed where it includes a preliminary month.',
             f'Payrolls shrank in {nw(len(F["losses"]))} months: {loss_months(F)}.']
    drawn = ['Key: a Stone column is the jobs added or lost in the month; hatched columns are preliminary, August and September 2026.',
             'Three-month average: the dark line.',
             f'{nw(len(F["losses"]), cap=True)} months with a loss. {nw(len(F["losses"]), cap=True)} months show a loss: {loss_months(F)}.',
             f'Latest: {people(D[-1]["change_thousands"])} jobs in September 2026, preliminary.']
    body_rows = [[month_words(r['key']), people(r['change_thousands']), people(r['avg3_thousands']), 'Preliminary' if r['key'] >= '2026-08' else '']
                 for r in D]
    table = table_html('Monthly change in payroll jobs and its three-month average', ['Month', 'Change in jobs', 'Three-month average', 'Status'], body_rows, (1, 2))
    return dict(sid='S14', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=drawn, table=table,
                grade_line='Official statistic: a Bureau of Labor Statistics survey of employers, as copied by FRED')



# ------------------------------------------------------------------------------------------------ S15 results table
def s15_layout():
    """Column widths for the full table, measured from the copy the cells print in Inter, with 6 percent headroom
    for HTML text, which wraps rather than spills. Names wrap inside the state column, so only the longest name takes
    two lines. The table switches to cards wherever its container is narrower than the sum, so no cell ever prints
    over its neighbor."""
    T = ST['results']
    R = rows(SHIFT)
    size, hh = 14, T['html_headroom']
    tagw = tw(TAG, 13, 600) * hh + 14
    names = sorted(tw(r['name'], 15, 600) * hh for r in R)
    state = max(tagw, names[-2]) + T['gap']             # the widest name wraps; every other fits on one line
    dl = [lead_text(r[m]) for r in R for m in ('margin_2020', 'margin_2024') if r[m] < 0]
    rl = [lead_text(r[m]) for r in R for m in ('margin_2020', 'margin_2024') if r[m] > 0]
    half_d = max(tw(x, size, 600) for x in dl) * hh + T['gap']
    half_r = max(tw(x, size, 600) for x in rl) * hh + T['gap']
    dmax = max(-r[m] for r in R for m in ('margin_2020', 'margin_2024'))
    rmax = max(r[m] for r in R for m in ('margin_2020', 'margin_2024'))
    ppp = min((half_d - 2) / dmax, (half_r - 2) / rmax)      # one scale for every margin bar, fitted to its half
    kk = T['shift_px_per_point']
    smax = max(r['shift_pts'] for r in R)
    shift = max(T['gap'] + smax * kk + 10 + tw('10.5', size) * hh + 8, T['shift_min'])
    widths = [state, half_d + half_r, half_d + half_r, shift]
    return {'state': state, 'half_d': half_d, 'half_r': half_r, 'ppp': ppp, 'kk': kk, 'shift': shift,
            'widths': widths, 'total': sum(widths)}


def margin_cell(r, field, cls, L):
    """One margin in its half of a split cell: left of the center line for a Democratic lead, right of it for a
    Republican lead, with the party named and a 6 px bar from the center line whose length is the margin."""
    m = r[field]
    side = 'r' if m > 0 else 'd'
    w = abs(m) * L['ppp']
    yr = field[-4:]
    inner = (f'<span data-party="{PARTY[sgn(m)]}" class="mi"><span class="mt"><span class="yr">{yr} </span>{e(lead_text(m))}</span>'
             f'<span class="mb" style="width:{w:.3f}px"{da(r["key"], m, field=field, mark="bar", axis="x", scale="margin")}></span></span>')
    halves = (f'<span class="half d">{inner if side == "d" else ""}</span><span class="half r">{inner if side == "r" else ""}</span>')
    return f'<td role="cell" class="mc {cls}"><span class="mcw">{halves}</span></td>'


def gen_s15(view):
    """The results table: one row per state with both margins in split cells, the party named in each, and the
    shift as an arrow whose length is the shift. It sorts by any column; sorted by the 2024 margin, a row marks the
    even line. Where the full row does not fit, each row becomes a card of three lines, with the shift in words.
    Explicit table roles keep every cell tied to its header when the rows change display."""
    L = s15_layout()
    F = shift_facts()
    R = sorted(rows(SHIFT), key=lambda r: (r['margin_2024'], r['code']))
    flips = {r['code'] for r in F['flips']}
    assert all(abs(r[m]) * L['ppp'] <= (L['half_d'] if r[m] < 0 else L['half_r']) for r in R for m in ('margin_2020', 'margin_2024'))
    tid = f'{view}-s15-table'

    def th(key, label, extra='', sort=None):
        a_sort = f' aria-sort="{sort}"' if sort else ''
        return (f'<th scope="col" role="columnheader" data-sort="{key}"{a_sort}{extra}><button type="button" class="sortb" aria-describedby="{view}-s15-sorthint">'
                f'{e(label)}<span class="sa" aria-hidden="true"></span></button></th>')
    head = (th('name', 'State') + th('m24', '2024 margin', ' class="mh"', 'ascending') + th('m20', '2020 margin', ' class="mh"')
            + th('shift', 'Shift toward the Republican nominee', ' class="shh"'))
    sub = ('<tr class="subhead" aria-hidden="true"><td></td>'
           + ''.join('<td class="mh2"><span class="mcw"><span class="half d"><span class="sl2">Democratic lead</span></span>'
                     '<span class="half r"><span class="sl2">Republican lead</span></span></span></td>' for _ in range(2))
           + '<td></td></tr>')
    asc_txt = 'Even line. In every row above, the Democratic nominee led in 2024; in every row below, the Republican nominee led.'
    desc_txt = 'Even line. In every row above, the Republican nominee led in 2024; in every row below, the Democratic nominee led.'
    body = []
    for r in R:
        if r['margin_2024'] > 0 and not any('data-divider' in b for b in body):
            body.append(f'<tr role="row" class="evenrow" data-divider data-asc="{e(asc_txt)}" data-desc="{e(desc_txt)}">'
                        f'<td role="cell" colspan="4" aria-colspan="4"><span class="evtext">{e(asc_txt)}</span></td></tr>')
        tag = f'<span class="chg">{TAG}</span>' if r['code'] in flips else ''
        sh = r['shift_pts']
        body.append(
            f'<tr role="row" data-row data-name="{ea(r["name"])}" data-m24="{r["margin_2024"]}" data-m20="{r["margin_2020"]}" data-shift="{sh}">'
            f'<th scope="row" role="rowheader"><span class="stn">{e(r["name"])}</span>{tag}</th>'
            + margin_cell(r, 'margin_2024', 'c24', L) + margin_cell(r, 'margin_2020', 'c20', L)
            + f'<td role="cell" class="sc"><span data-party="Republicans" class="sci"><span class="arwh" style="width:{sh * L["kk"]:.3f}px"'
              f'{da(r["key"], sh, field="shift_pts", mark="bar", axis="x", scale="shift")}></span>'
              f'<span class="sv"{da(r["key"], sh, field="shift_pts", mark="label")}>{sh:.1f}<span class="swd"> toward the Republican nominee</span></span></span></td></tr>')
    key = ("Each margin sits on the side of the nominee who led, with the party named: left of the center line, the Democratic "
           'nominee; right of it, the Republican nominee. Bars grow from the center line, and every arrow points toward the Republican nominee.')
    card_key = ('Each card names the leader and margin in each year and gives the shift toward the Republican nominee in words, '
                'beside its arrow.')
    hint = 'Sorts the table by this column; press again to reverse the order.'
    cols = ''.join(f'<col style="width:{w:.1f}px">' for w in L['widths'])
    return (f'<div class="rtw"><p class="rkey rk-full">{e(key)}</p><p class="rkey rk-card">{e(card_key)}</p><p class="rsort"><b>Sort by any column.</b> {e("The table opens in order of the 2024 margin.")}</p>'
            f'<p class="vh2" id="{view}-s15-sorthint">{e(hint)}</p>'
            f'<table class="results" role="table" id="{tid}" style="width:{L["total"]:.1f}px"><caption class="vh2">{e("Presidential margin by state, 2024 and 2020, with the shift toward the Republican nominee")}</caption>'
            f'<colgroup>{cols}</colgroup><thead role="rowgroup"><tr role="row">{head}</tr>{sub}</thead><tbody role="rowgroup">{"".join(body)}</tbody></table>'
            f'<p class="vh2" aria-live="polite" id="{view}-s15-status"></p></div>')


def s15_css():
    """The table's stylesheet, with the switch to two-line rows set at the full row's measured width."""
    L = s15_layout()
    cq = math.ceil(L['total'])
    return (S15_CSS.replace('HALF_D', f'{L["half_d"]:.1f}px').replace('HALF_R', f'{L["half_r"]:.1f}px')
            .replace('CQ_WIDTH', f'{cq - 0.02:.2f}px').replace('TWO_LINE', f'{ST["results"]["two_line_min"]}px')
            .replace('BAR_GAP', f'{ST["results"]["bar_gap"]}px').replace('BAR_H', f'{ST["results"]["bar"]}px')
            .replace('SHIFT_HEAD', f'{ST["results"]["shift_head"]}px'))


S15_CSS = r"""
.rtw{container-type:inline-size}
.rkey{margin:0 0 6px;font:400 15px/23px Inter,sans-serif;max-width:46em;text-wrap:pretty}
.rk-card{display:none}
.rsort{margin:0 0 14px;font:400 15px/23px Inter,sans-serif;color:var(--sec)}.rsort b{color:var(--ink);font-weight:600}
table.results{border-collapse:collapse;table-layout:fixed;max-width:100%;font:400 14px/20px Inter,sans-serif;font-variant-numeric:tabular-nums}
table.results thead th{text-align:left;vertical-align:bottom;padding:0 12px 6px 0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
table.results thead th.mh{text-align:center;padding:0 0 6px}
table.results thead th.shh{padding-left:12px}
.sortb{display:inline-block;min-height:44px;padding:13px 0;margin:0;border:0;background:none;cursor:pointer;font:inherit;letter-spacing:inherit;text-transform:inherit;color:var(--ink);text-align:inherit}
.sortb:hover{text-decoration:underline;text-underline-offset:3px}
.sa{display:inline-block;width:0;height:0;margin-left:7px;vertical-align:1px;border-left:5px solid transparent;border-right:5px solid transparent;border-top:6px solid var(--grid)}
th[aria-sort="ascending"] .sa{border-top:0;border-bottom:6px solid var(--ink)}
th[aria-sort="descending"] .sa{border-top:6px solid var(--ink)}
table.results .subhead td{padding:0 0 6px;border-bottom:1px solid var(--ink)}
.sl2{font:400 13px/18px Inter,sans-serif;color:var(--sec);padding:0 8px}
table.results tbody th,table.results tbody td{padding:0 12px 0 0;border-top:1px solid var(--grid);vertical-align:middle;text-align:left}
table.results tbody th{font:600 15px/20px Inter,sans-serif;padding:8px 12px 8px 0}
.stn{display:block;white-space:normal}
.chg{display:inline-block;margin-top:4px;padding:1px 6px;border:1px solid var(--ink);font:600 13px/16px Inter,sans-serif;white-space:nowrap}
td.mc{position:relative;padding:0!important}
td.mc::before,td.mh2::before{content:"";position:absolute;left:HALF_D;top:0;bottom:0;border-left:1px solid var(--ink)}
td.mh2{position:relative;padding:0 0 6px!important}
.mcw{display:grid;grid-template-columns:HALF_D HALF_R}
.half{display:flex;flex-direction:column;justify-content:center;min-width:0}
.half.d{align-items:flex-end;text-align:right}.half.r{align-items:flex-start}
.mi{display:flex;flex-direction:column;gap:BAR_GAP;align-items:inherit;padding:8px 0}
.mt{font:600 14px/18px Inter,sans-serif;padding:0 8px}
.c20 .mt{font-weight:400;color:var(--sec)}
.yr{display:none}
.mb{display:block;height:BAR_H;background:var(--ink)}
.c20 .mb{background:var(--lt)}
td.sc{white-space:nowrap;padding-left:12px!important}
.sci{display:inline-flex;align-items:center;gap:10px}
.arwh{position:relative;display:inline-block;flex:none;height:2px;background:var(--ink)}
.arwh::after{content:"";position:absolute;right:0;top:-4px;border-left:SHIFT_HEAD solid var(--ink);border-top:5px solid transparent;border-bottom:5px solid transparent}
.sv{font:400 14px/20px Inter,sans-serif}
.swd{display:none}
table.results tr.evenrow td{padding:9px 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);font:600 14px/20px Inter,sans-serif;text-align:center}
@media (forced-colors:active){.mb,.arwh{forced-color-adjust:none;background:CanvasText}.arwh::after{forced-color-adjust:none;border-left-color:CanvasText}}
@container (max-width:CQ_WIDTH){
 table.results{width:100%!important}
 table.results colgroup{display:none}
 table.results,table.results thead,table.results tbody{display:block}
 table.results thead tr:first-child{display:flex;flex-wrap:wrap;gap:0 18px;border-bottom:1px solid var(--ink)}
 table.results thead th,table.results thead th.mh,table.results thead th.shh{display:block;padding:0;text-align:left}
 table.results .subhead{display:none}
 table.results tbody tr[data-row]{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);grid-template-areas:"name name" "m24 m20" "shift shift";gap:3px 14px;padding:9px 0 11px;border-top:1px solid var(--grid)}
 table.results tbody th,table.results tbody td{display:block;border:0;padding:0}
 table.results tbody th{grid-area:name}
 td.sc{grid-area:shift;padding:2px 0 0!important;white-space:normal}
 td.c24{grid-area:m24}td.c20{grid-area:m20}
 td.mc::before{display:none}
 .mcw{display:block}.half:empty{display:none}.half.d,.half.r{align-items:flex-start;text-align:left}
 .mi{padding:0}.mt{padding:0;white-space:normal}
 .mb{display:none}
 .yr{display:inline;font-weight:600;color:var(--sec)}
 .swd{display:inline}
 .rk-full{display:none}.rk-card{display:block}
 table.results tr.evenrow{display:block}table.results tr.evenrow td{display:block;text-align:left}
}
@container (min-width:TWO_LINE) and (max-width:CQ_WIDTH){
 table.results tbody tr[data-row]{grid-template-areas:"name shift" "m24 m20"}
 td.sc{justify-self:end;padding:0!important}
 td.c20{justify-self:end}
 td.c20 .half.d,td.c20 .half.r{align-items:flex-end;text-align:right}
}
"""


def spec_s15(view):
    F = shift_facts()
    close = [r for r in F['flips'] if r['margin_2024'] < 2.5]   # ST-S8: Georgia prints 2.2, so the bound reads 2.5
    assert len(close) == 4 and len(F['flips']) == 6 and F['led24'][1] - F['led20'][1] == 6
    title = (f'The Republican nominee led in {F["led24"][1]} states in 2024, {nw(F["led24"][1] - F["led20"][1])} more than in 2020; '
             f'in {nw(len(close))} of the {nw(len(F["flips"]))} states that changed leader, the lead was under 2.5 points.')
    measure = ("Presidential margin by state in 2024 and 2020: the leading nominee's share of all presidential votes minus the "
               "other's, in percentage points, with the shift between the two elections; 50 states and DC")
    body = f'<div class="art tbl">{gen_s15(view)}</div>'
    notes = ["Margin: the Republican nominee's share of all presidential votes minus the Democratic nominee's, printed as the leader's lead. "
             'A state whose leader changed carries a tag.',
             f'The Democratic nominee led in {F["led24"][-1]} states and DC in 2024. The four close changes of leader: '
             + ', '.join(f'{r["name"]} {lead_text(r["margin_2024"])}' for r in sorted(close, key=lambda r: r['margin_2024'])) + '.',
             "New York's figures count every ballot line each nominee held, including the Working Families and Conservative lines.",
             'Maine and Nebraska split their electoral votes by district; these margins are statewide.']
    R = sorted(rows(SHIFT), key=lambda r: r['name'])
    body_rows = [[r['name'], f'{r["dem_pct_2024"]:.2f}', f'{r["rep_pct_2024"]:.2f}', f'{int(r["total_votes_2024"]):,}'] for r in R]
    table = table_html('Vote shares and total presidential votes by state, 2024', ['State', 'Democratic nominee, percent', 'Republican nominee, percent', 'Total votes'], body_rows, (1, 2, 3))
    drawn = ['Each margin sits on the side of the nominee who led, with the party named. Bars grow from the center line; arrows give the shift toward the Republican nominee. '
             'The table opens in order of the 2024 margin, with a row at the even line, and sorts by any column. '
             'Where a full row does not fit, each row becomes a card that names the leader and margin in each year and gives the shift in words.']
    return dict(sid='S15', title=title, measure=measure, body=body, strings=[], label='', notes=notes,
                drawn_notes=drawn, table=table, wide=True,
                grade_line='Documented: official results the states reported, compiled by the Federal Election Commission')



# ------------------------------------------------------------------------------------------------ S16 bubble map
def topo_states():
    """Decode the shared TopoJSON (already projected to a 975 by 610 frame) into rings per state code. The western
    Aleutians, which fall left of the frame, are dropped, as the geography notes allow."""
    sc, tr = GEO['transform']['scale'], GEO['transform']['translate']
    arcs = []
    for arc in GEO['arcs']:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)

    def ring(ids):
        out = []
        for i in ids:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(seg if not out else seg[1:])
        return out
    code_of = {t['fips']: t['code'] for t in TILES}
    states = {}
    for g in GEO['objects']['states']['geometries']:
        polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
        rings = [[ring(r) for r in poly] for poly in polys]
        states[code_of[g['id']]] = [p_ for p_ in rings if max(x for x, _ in p_[0]) > 0]
    assert len(states) == 51
    return states


STATE_RINGS = topo_states()


def ring_area_centroid(pts):
    a2 = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a2 += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    if abs(a2) < 1e-12:
        return 0.0, (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts))
    return a2 / 2, (cx / (3 * a2), cy / (3 * a2))


def simplify(pts, tol):
    """Douglas-Peucker on one ring, in output pixels."""
    if len(pts) < 4:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        (x0, y0), (x1, y1) = pts[i], pts[j]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy) or 1e-9
        best, bi = -1, None
        for k_ in range(i + 1, j):
            x, y = pts[k_]
            d = abs(dy * x - dx * y + x1 * y0 - y1 * x0) / n if n > 1e-9 else math.hypot(x - x0, y - y0)
            if d > best:
                best, bi = d, k_
        if bi is not None and best > tol:
            keep[bi] = True
            stack += [(i, bi), (bi, j)]
    return [p_ for p_, k_ in zip(pts, keep) if k_]


def map_frame(W):
    xs = [x for rings in STATE_RINGS.values() for poly in rings for x, _ in poly[0]]
    ys = [y for rings in STATE_RINGS.values() for poly in rings for _, y in poly[0]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s_ = W / (x1 - x0)
    return (lambda x: (x - x0) * s_), (lambda y: (y - y0) * s_), s_, (y1 - y0) * s_


_DORLING = {}


def bubble_layout(W, rmax, top):
    """Circles at each state's center (the centroid of its largest piece), area true to citizens 18 and over, then
    pushed apart where they would overlap and pulled back toward their states, so no circle covers another."""
    key = (W, rmax, round(top, 2))
    if key in _DORLING:
        return _DORLING[key]
    MX, MY, s_, mh = map_frame(W)
    R = {r['code']: r for r in rows(TURNOUT)}
    vmax = max(r['citizen_vap_thousands'] for r in R.values())
    cen, rad = {}, {}
    for c, rings in STATE_RINGS.items():
        big = max(rings, key=lambda poly: abs(ring_area_centroid(poly[0])[0]))
        _, (cx, cy) = ring_area_centroid(big[0])
        cen[c] = (MX(cx), top + MY(cy))
        rad[c] = rmax * math.sqrt(R[c]['citizen_vap_thousands'] / vmax)
    gap = ST['bubble']['gap']
    pos = dict(cen)
    codes = sorted(pos)
    for it in range(500):
        moved = 0.0
        for i, a_ in enumerate(codes):
            for b_ in codes[i + 1:]:
                (xa, ya), (xb, yb) = pos[a_], pos[b_]
                dx, dy = xb - xa, yb - ya
                d = math.hypot(dx, dy) or 1e-6
                need = rad[a_] + rad[b_] + gap
                if d < need:
                    push = need - d
                    wa, wb = rad[b_] / (rad[a_] + rad[b_]), rad[a_] / (rad[a_] + rad[b_])
                    ux, uy = dx / d, dy / d
                    pos[a_] = (xa - ux * push * wa, ya - uy * push * wa)
                    pos[b_] = (xb + ux * push * wb, yb + uy * push * wb)
                    moved += push
        for c in codes:
            x, y = pos[c]
            cx, cy = cen[c]
            x, y = x + (cx - x) * 0.02, y + (cy - y) * 0.02
            # keep every circle, and the 2 px ring some carry, inside the drawing
            x = min(max(x, rad[c] + 3), W - rad[c] - 3)
            y = min(max(y, top + rad[c] + 3), top + mh + 24 - rad[c])
            pos[c] = (x, y)
        if moved < 0.01 and it > 50:
            break
    for i, a_ in enumerate(codes):
        for b_ in codes[i + 1:]:
            d = math.hypot(pos[a_][0] - pos[b_][0], pos[a_][1] - pos[b_][1])
            assert d >= rad[a_] + rad[b_] + gap * 0.5 - 0.05, (W, a_, b_)
    out = (pos, rad, cen, MX, MY, mh)
    _DORLING[key] = out
    return out


def turnout_bin(v):
    return 1 + sum(1 for b in ST['bubble']['bins'] if v >= b)


BIN_WORDS = ['Under 60%', '60 to 64.9', '65 to 69.9', '70 to 74.9', '75 or more']
RING_NOTE = "Ringed: of the four largest states, the three below the nation by more than the survey's margin of error"   # ST-M6


def seg_gap(s1, s2):
    """The shortest distance between two line segments, 0 where they cross."""
    (ax, ay, bx, by), (cx, cy, dx, dy) = s1, s2

    def orient(px, py, qx, qy, rx, ry):
        return (qx - px) * (ry - py) - (qy - py) * (rx - px)
    if (orient(cx, cy, dx, dy, ax, ay) * orient(cx, cy, dx, dy, bx, by) < 0 and
            orient(ax, ay, bx, by, cx, cy) * orient(ax, ay, bx, by, dx, dy) < 0):
        return 0.0

    def pt_seg(px, py, x0, y0, x1, y1):
        L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2
        t_ = 0 if L2 == 0 else max(0, min(1, ((px - x0) * (x1 - x0) + (py - y0) * (y1 - y0)) / L2))
        return math.hypot(px - x0 - t_ * (x1 - x0), py - y0 - t_ * (y1 - y0))
    return min(pt_seg(ax, ay, cx, cy, dx, dy), pt_seg(bx, by, cx, cy, dx, dy),
               pt_seg(cx, cy, ax, ay, bx, by), pt_seg(dx, dy, ax, ay, bx, by))


def gen_s16(W, uid, t=None):
    """Bubble map: a light map of the states, a circle for each state whose area follows its citizens 18 and over,
    stepped in one Verdigris ink by the share who said they voted. The step key marks the national rate on itself,
    and the three states the title names carry a 2 px ring. Codes sit inside circles where they fit and beside their
    own circle where there is room, else on a short leader. Under the map: the largest states, and the range with its
    margins of error."""
    a = Art(W, uid, t)
    B = ST['bubble']
    narrow = W < 600
    F = turnout_facts()
    R = {r['code']: r for r in rows(TURNOUT)}
    rk = 'wide' if W >= 900 else ('mid' if W >= 600 else ('phone' if W >= 358 else 'small_phone'))
    rmax = B['r_max'][rk]
    lbl = 14
    tk = 13 if not narrow else 14
    code_size = 14 if not narrow else 13
    vmax = max(r['citizen_vap_thousands'] for r in R.values())
    ringed = {r['code'] for r in F['below']}
    stack_keys = W < 900
    # the step key: five steps in a bar, with the national rate marked on it
    y = 16
    eyebrow(a, 0, y, ('SHARE OF CITIZENS 18 AND OVER WHO SAID THEY VOTED, PERCENT', 'SHARE WHO SAID THEY VOTED, PERCENT', 'SAID THEY VOTED, PERCENT'),
            W if stack_keys else W * 0.6)
    seg = min(B['key_seg'], (W - 4) / 5)
    bar_top = y + 46
    for i in range(5):
        a.rect(i * seg, bar_top, seg, 12, f'bub q{i + 1}')
    for j, b in enumerate(B['bins']):
        a.text((j + 1) * seg, bar_top + 12 + 18, str(b), tk, 'tk', 400, 'middle')
    nat = F['nat']
    lo_b, hi_b = B['bins'][1], B['bins'][2]
    assert lo_b <= nat < hi_b
    xn = (2 + (nat - lo_b) / (hi_b - lo_b)) * seg
    a.line(xn, bar_top - 5, xn, bar_top + 17, 's-mark')
    a.text(xn, bar_top - 10, f'Nation {nat}%', tk, 'th', 600, 'middle')
    y = bar_top + 12 + 18 + 30
    # the ring, explained in the key
    a.circle(9, y - 5, 8, 'bub q2 bubring')
    lines = wrap(RING_NOTE, ((W if stack_keys else W * 0.6) - 26) / HR, lbl)
    for i, ln in enumerate(lines):
        a.text(26, y + i * 19, ln, lbl, 'tr', 400)
    y_shade_end = y + 19 * (len(lines) - 1)
    if stack_keys:
        sy, sx = y_shade_end + 36, 0
    else:
        sx, sy = W * 0.66, 16
    eyebrow(a, sx, sy, ('CITIZENS 18 AND OVER', 'CITIZENS 18+'), W)
    cx_ = sx
    rk_max = rmax * math.sqrt(max(B['key_millions']) * 1000 / vmax)
    base = sy + 14 + 2 * rk_max
    for mil in B['key_millions']:
        rr = rmax * math.sqrt(mil * 1000 / vmax)
        lab = f'{mil} million'
        slot = max(2 * rr, tw(lab, lbl) * HR)
        a.circle(cx_ + slot / 2, base - rr, rr, 'f-none s-keyc')
        a.text(cx_ + slot / 2, base + 18, lab, lbl, 'tr', 400, 'middle')
        cx_ += slot + 18
    top = max(y_shade_end, base + 18) + 30
    pos, rad, cen, MX, MY, mh = bubble_layout(W, rmax, top)
    # the land: every state as a light shape, borders in the ground color
    tol = 0.45
    for c, rings in sorted(STATE_RINGS.items()):
        d = ''
        for poly in rings:
            for rg in poly:
                pts = simplify([(MX(x), top + MY(y_)) for x, y_ in rg], tol)
                if len(pts) >= 3:
                    d += 'M' + 'L'.join(f'{x:.1f} {y_:.1f}' for x, y_ in pts) + 'Z'
        a.raw(f'<path d="{d}" class="f-land"/>')
    # circles, largest first
    order = sorted(R, key=lambda c: -R[c]['citizen_vap_thousands'])
    for c in order:
        r = R[c]
        (x, y_), rr = pos[c], rad[c]
        # area, never radius, follows the count: checked here, since the rendered check cannot measure area
        assert abs(math.pi * rr ** 2 / (math.pi * rmax ** 2) - r['citizen_vap_thousands'] / vmax) < 1e-9
        b = turnout_bin(r['voted_pct'])
        a.raw(f'<g{da(r["key"], r["voted_pct"], field="voted_pct", mark="cell")}>')
        a.circle(x, y_, rr, f'bub q{b}' + (' bubring' if c in ringed else ''),
                 da(r['key'], r['citizen_vap_thousands'], field='citizen_vap_thousands', mark='cell'))
        a.raw('</g>')
    # labels: inside where the code fits; beside the circle where the label sits nearer its own circle than any
    # other; else on a short leader
    pad = B['label_pad']
    placed, skipped, leaders, led = [], [], [], []

    def hits_circle(box, clear=1.5, own=None):
        """True where the box comes within `clear` px of a circle; a leader's label keeps further from every circle
        but its own, so it never sits beside a neighbor."""
        bx0, by0, bx1, by1 = box
        for c2 in R:
            (x2, y2), r2 = pos[c2], rad[c2]
            nx_, ny_ = min(max(x2, bx0), bx1), min(max(y2, by0), by1)
            if math.hypot(nx_ - x2, ny_ - y2) < r2 + (1.5 if c2 == own else clear):
                return True
        return False

    def nearest_is_own(box, c):
        """The label's nearest circle, measured from the box to each circle's edge, must be its own."""
        bx0, by0, bx1, by1 = box

        def gap_to(c2):
            (x2, y2), r2 = pos[c2], rad[c2]
            nx_, ny_ = min(max(x2, bx0), bx1), min(max(y2, by0), by1)
            return math.hypot(nx_ - x2, ny_ - y2) - r2
        own = gap_to(c)
        return all(own + 2 < gap_to(c2) for c2 in R if c2 != c)

    def away_angles(c):
        """Leader angles, best first: facing away from the neighbors nearest this circle's edge."""
        (x, y_), rr = pos[c], rad[c]
        vx = vy = 0.0
        for c2 in R:
            if c2 == c:
                continue
            dx_, dy_ = x - pos[c2][0], y_ - pos[c2][1]
            d = math.hypot(dx_, dy_)
            gap = d - rr - rad[c2]
            if gap < 40 and d > 0:
                vx += dx_ / d / (gap + 4)
                vy += dy_ / d / (gap + 4)
        if math.hypot(vx, vy) < 1e-9:
            return list(range(0, 360, 15))
        return sorted(range(0, 360, 15), key=lambda g: -(math.cos(math.radians(g)) * vx + math.sin(math.radians(g)) * vy))

    def free(box):
        return (box[0] >= 0 and box[2] <= W and box[1] >= top - 6 and
                all(box[2] <= q[0] or box[0] >= q[2] or box[3] <= q[1] or box[1] >= q[3] for q in placed) and
                not any(EX._seg_hits_box(*ld, (box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2)) for ld in leaders))
    def beside(c):
        """A label beside its circle, where its nearest circle is its own."""
        (x, y_), rr = pos[c], rad[c]
        w_ = tw(c, code_size, 600) * HR
        for dx_, dy_, anc in ((rr + 4, code_size * 0.36, 'start'), (-rr - 4, code_size * 0.36, 'end'),
                              (0, -rr - 5, 'middle'), (0, rr + code_size + 2, 'middle'),
                              (rr * 0.75 + 3, -rr * 0.75 - 2, 'start'), (-rr * 0.75 - 3, -rr * 0.75 - 2, 'end'),
                              (rr * 0.75 + 3, rr * 0.75 + code_size, 'start'), (-rr * 0.75 - 3, rr * 0.75 + code_size, 'end')):
            tx, ty = x + dx_, y_ + dy_
            x0 = {'start': tx, 'middle': tx - w_ / 2, 'end': tx - w_}[anc]
            box = (x0, ty - 0.97 * code_size, x0 + w_, ty + 0.25 * code_size)
            if free(box) and not hits_circle(box) and nearest_is_own(box, c):
                return dict(tx=tx, ty=ty, anc=anc, box=box, seg=None)
        return None

    def with_leader(c):
        """A short leader to the nearest free spot, tried at growing distances, facing away from the neighbors first.
        The leader crosses no circle, label or other leader, and its label keeps clear of every other circle."""
        (x, y_), rr = pos[c], rad[c]
        w_ = tw(c, code_size, 600) * HR
        for dist in (14, 20, 28, 38, 50):
            for ang in away_angles(c):
                ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                tx, ty = x + ux * (rr + dist), y_ + uy * (rr + dist)
                anc = 'start' if ux > 0.3 else ('end' if ux < -0.3 else 'middle')
                x0 = {'start': tx, 'middle': tx - w_ / 2, 'end': tx - w_}[anc]
                box = (x0, ty - 0.97 * code_size + 0.36 * code_size, x0 + w_, ty + 0.25 * code_size + 0.36 * code_size)
                if not (free(box) and not hits_circle(box, clear=B['leader_clear'], own=c)):
                    continue
                seg = (x + ux * (rr + 2), y_ + uy * (rr + 2), x + ux * (rr + dist - 3), y_ + uy * (rr + dist - 3))
                lx0, ly0, lx1, ly1 = seg
                if math.hypot(lx1 - lx0, ly1 - ly0) < TK['note']['leader_min']:
                    continue
                if any(EX._seg_hits_box(*seg, (q[0] - 2, q[1] - 2, q[2] + 2, q[3] + 2)) for q in placed + [box]):
                    continue
                if any(seg_gap(seg, ld) < 3 for ld in leaders):      # no two leaders cross or touch
                    continue
                if any(math.hypot(px - pos[c2][0], py - pos[c2][1]) < rad[c2] + 1 for c2 in R if c2 != c
                       for px, py in ((lx0 + (lx1 - lx0) * q / 8, ly0 + (ly1 - ly0) * q / 8) for q in range(9))):
                    continue
                return dict(tx=tx, ty=ty + code_size * 0.36, anc=anc, box=box, seg=seg)
        return None

    labels = {}

    def put_label(c, p_):
        labels[c] = p_
        placed.append(p_['box'])
        if p_['seg']:
            leaders.append(p_['seg'])

    def take_label(c):
        p_ = labels.pop(c)
        placed.remove(p_['box'])
        if p_['seg']:
            leaders.remove(p_['seg'])
        return p_

    def place(c):
        p_ = beside(c) or with_leader(c)
        if p_:
            put_label(c, p_)
        return p_
    for c in order:
        r = R[c]
        (x, y_), rr = pos[c], rad[c]
        w_ = tw(c, code_size, 600) * HR
        b = turnout_bin(r['voted_pct'])
        if 2 * rr >= w_ + 2 * pad and 2 * rr >= code_size + 6:
            a.text(x, y_ + code_size * 0.36, c, code_size, f'qt{b}', 600, 'middle', on_mark=True)
            placed.append((x - w_ / 2, y_ - code_size * 0.62, x + w_ / 2, y_ + code_size * 0.5))
            continue
        if not place(c):
            skipped.append(c)
    # a second pass: a state left without a label may take a near neighbor's spot, where both can then be labeled
    for c in list(skipped):
        near = sorted((t for t in labels if math.dist(pos[t], pos[c]) < 90), key=lambda t: math.dist(pos[t], pos[c]))
        for t in near:
            old = take_label(t)
            if place(c):
                if place(t):
                    skipped.remove(c)
                    break
                take_label(c)
            put_label(t, old)
    for c in order:
        if c in labels:
            p_ = labels[c]
            if p_['seg']:
                a.leader([p_['seg'][:2], p_['seg'][2:]])
                led.append(c)
            a.text(p_['tx'], p_['ty'], c, code_size, 'tl', 600, p_['anc'])
    leaders = [labels[c]['seg'] for c in led]
    a.anchors['skipped'] = skipped
    a.anchors['leaders'] = dict(zip(led, leaders))
    assert all(seg_gap(l1, l2) >= 3 for i, l1 in enumerate(leaders) for l2 in leaders[i + 1:]), f'{uid}: two leaders cross'
    if W >= 900:
        assert not skipped, f'{uid}: no room for {skipped}'
    # under the map: the largest states, then the range with its margins of error
    y = top + mh + 24 + 34
    big = sorted(R.values(), key=lambda r: -r['citizen_vap_thousands'])[:4]
    y = flow_items(a, 0, y, 'MOST CITIZENS 18 AND OVER', [(short_name(r), f'{r["citizen_vap_thousands"] / 1000:.1f} million, {r["voted_pct"]}%',
                                                          da(r['key'], r['voted_pct'], field='voted_pct', mark='label')) for r in big], W, lbl) + 32
    y = a.para(0, y, range_text(F), W, lbl, 'tn', 400, 19)
    return a, y + 8


def range_text(F):
    lo, hi = F['lo'], F['hi']
    return (f'Range: {short_name(lo)} {lo["voted_pct"]}% (±{lo["moe_pct"]}) to {short_name(hi)} {hi["voted_pct"]}% '
            f'(±{hi["moe_pct"]}). Gaps of a few points between states may not be real.')


def spec_s16(view):
    F = turnout_facts()
    below = F['below']
    title = (f'{below[0]["name"]}, {below[1]["name"]} and {below[2]["name"]}, three of the four states with the most citizens 18 and over, '
             f'reported turnout below the national {F["nat"]} percent by more than the survey’s margin of error.')
    measure = ('Citizens 18 and over who said they voted in November 2024, percent, by state; circles sized by the number of '
               'citizens 18 and over; 50 states and DC')
    R = rows(TURNOUT)
    by_bin = defaultdict(list)
    for r in R:
        by_bin[turnout_bin(r['voted_pct'])].append(r['code'])
    label = ('Bubble map of 50 states and DC. Circle area follows the number of citizens 18 and over; shade steps with the share who said they voted. '
             + '; '.join(f'{BIN_WORDS[b - 1]}: {", ".join(sorted(by_bin[b]))}' for b in sorted(by_bin))
             + f'. Nation: {F["nat"]} percent. Ringed, of the four largest states, the three below the nation by more than the margin of error: '
             + ', '.join(r['name'] for r in below)
             + '. The four largest: ' + ', '.join(f'{r["name"]} {r["citizen_vap_thousands"] / 1000:.1f} million, {r["voted_pct"]} percent' for r in F['big4'])
             + '. The table under the chart lists every state.')
    body, strings = EX.artboards(view, 'S16', gen_s16, TK['artboard']['wide'], label)
    notes = [f'These rates are what people told a Census survey, which runs higher than counted ballots. The states’ 90 percent margins of error run from '
             f'{min(r["moe_pct"] for r in R)} to {max(r["moe_pct"] for r in R)} points, so a gap of a few points between two states may not be real.',
             f'{below[0]["name"]}, {below[1]["name"]} and {below[2]["name"]} each sit below the national rate by more than their 90 percent margins of error; '
             f'California’s {F["big4"][0]["voted_pct"]} percent is within its margin of the nation’s {F["nat"]}.',
             'Each circle’s area follows the number of citizens 18 and over. Circles sit at each state’s center and move apart '
             'only where they would overlap, most in the Northeast. The table names every state.',
             'Map: U.S. Census Bureau cartographic boundary files (2017), via us-atlas 3.0.1 by Mike Bostock (ISC license).']
    drawn = [f'Shade: the share of citizens 18 and over who said they voted, in five steps, under 60, 60 to 64.9, 65 to 69.9, 70 to 74.9, and 75 percent or more. '
             f'The nation, {F["nat"]}%, is marked on the step key. {RING_NOTE}.',
             'Circle size: citizens 18 and over; the key shows 1, 5 and 20 million. State codes sit inside the circles where they fit and beside their own circle where there is room.',
             'Most citizens 18 and over: ' + '; '.join(f'{short_name(r)} {r["citizen_vap_thousands"] / 1000:.1f} million, {r["voted_pct"]}%' for r in F['big4'])
             + '. ' + range_text(F)]
    body_rows = [[r['name'], f'{r["citizen_vap_thousands"]:,.0f}', f'{r["voted_pct"]:.1f}', f'{r["moe_pct"]:.1f}'] for r in sorted(R, key=lambda r: r['name'])]
    table = table_html('Citizens 18 and over and the share who said they voted, by state, 2024',
                       ['State', 'Citizens 18 and over, thousands', 'Said they voted, percent', 'Margin of error, points (90%)'], body_rows, (1, 2, 3))
    # the chart draws 2024 only, so it carries the dataset's 2024-only source line
    src = re.sub(r'^Source:\s*', '', copy(DS[TURNOUT]['meta']['source_line_2024_only']))
    return dict(sid='S16', title=title, measure=measure, body=body, strings=strings, label=label, notes=notes,
                drawn_notes=drawn, table=table, wide=True, source=src,
                grade_line='Official statistic: a Census Bureau survey; the rates are self-reported')


# ------------------------------------------------------------------------------------------------ the frame
WHY = {
    'S11': 'Arrows on one margin axis show where each state stood and how far it moved, and the six arrows that cross the even line show where the leader changed. On phones a ranked lollipop gives every shift one start.',
    'S12': ('A tile gives every state the same weight, and an arrow inside it puts the size of the shift where the state sits, so a reader '
            'finds a region before a number. On phones the map drops to eleven columns, with Alaska and Hawaii in the bottom row, and each '
            'square takes a gray step by the size of its shift.'),
    'S13': 'Small panels on one scale let a reader compare fourteen industries at a glance, ordered by percent gain, and the totals sit in their own rows, apart from the parts they hold.',
    'S14': "Columns show each month's change, noise and all, and the three-month average drawn over them gives the trend a reader can repeat.",
    'S15': 'A table answers a lookup: a reader finds a state, reads both margins with the leader named, and sorts by any column to find the biggest shifts.',
    'S16': 'Circles sized by citizens 18 and over show where most of them live, and one ink stepped by turnout shows how many said they voted, so size and rate read together.',
}
QUESTION = {'S16': 'Where did citizens 18 and over turn out, and where are most of them?'}
SPEC_FN = {}
VIEWS = [('newsprint', 'Newsprint'), ('dark', 'Charcoal'), ('phone', 'Phones')]
VIEW_GROUND = {'newsprint': 'news', 'dark': 'dark', 'phone': 'news'}


def stretch_figure(view, sid):
    """Explainer's figure frame, with the guide link pointed at this page's own short guide."""
    sp = SPEC_FN[sid](view)
    out = EX.figure(view, sp).replace('href="#system/read"', 'href="#newsprint/read"')
    if sid in WIDTH_NOTES:
        # the notes list sits outside the drawing's container, so it gets a container of its own, as wide as the drawing's,
        # and the note that matches the drawing shown takes its place
        wide, phone = WIDTH_NOTES[sid]
        old = f'<li>{e(wide)}</li>'
        assert out.count(old) == 1 and out.count('<ul class="fnotes">') == 1
        out = out.replace(old, f'<li class="n-wide">{e(wide)}</li><li class="n-phone">{e(phone)}</li>')
        start = out.index('<ul class="fnotes">')
        end = out.index('</ul>', start) + len('</ul>')
        out = out[:start] + '<div class="fnw">' + out[start:end] + '</div>' + out[end:]
    return out


def stretch_strip(view, sid):
    """Explainer's studio strip; where the page words a reader question more exactly than the shared data, its text is swapped in."""
    out = EX.strip(view, sid, WHY[sid])
    if sid in QUESTION:
        old = e(SPECS[sid]['reader_question'])
        assert old in out
        out = out.replace(old, e(QUESTION[sid]))
    return out


def specimen(view, sid):
    return (f'<section class="spec" id="{view}-{sid.lower()}" aria-labelledby="{view}-{sid.lower()}-t">'
            f'{stretch_figure(view, sid)}{stretch_strip(view, sid)}</section>')


def masthead():
    tabs = ''.join(f'<li><a href="#{v}">{e(t)}</a></li>' for v, t in VIEWS)
    return ('<header class="mast"><div class="wrap mrow">'
            '<a class="wm" href="#newsprint" data-red="signature" aria-label="Oath &amp; Action, the stretch test, first view">'
            f'{EX.wordmark(24, "20261028_Wordmark-24px-Master.svg", "wm24")}{EX.wordmark(16, "20261028_Wordmark-16px-Master.svg", "wm16")}</a>'
            '<p class="run">Chart system 01 · Explainer · Stretch test</p>'
            f'<nav class="tabs" aria-label="Views"><ul>{tabs}</ul></nav></div></header>')


def footer():
    return ('<footer class="foot"><div class="wrap frow">'
            '<p class="src">Data: Federal Election Commission official results for 2020 and 2024; U.S. Bureau of Labor Statistics '
            'payroll series via FRED, Federal Reserve Bank of St. Louis; U.S. Census Bureau, Current Population Survey, November 2024; '
            'all retrieved November 6, 2026. Map: U.S. Census Bureau cartographic boundary files (2017), via us-atlas 3.0.1 by Mike '
            f'Bostock (ISC license). {e("Every chart is drawn by a generator in build_stretch.py on Explainer’s kit.")}</p>'
            '<p class="src right">Chart system 01, Explainer: the stretch test. Studio draft for Board 4; titles and notes are drafts by the studio.</p>'
            '</div></footer>')


VIEW_DESC = {'newsprint': 'the six charts and the new tokens',
             'dark': 'two of the six on Charcoal',
             'phone': 'all six phone drawings side by side'}


def view_head(view, eyebrow_, h1, deck, extra=''):
    items = ''.join(f'<li><a href="#{v}">{e(t)}</a> <span>{e(VIEW_DESC[v])}</span></li>' for v, t in VIEWS if v != view)
    lk = f'<nav class="vlinks" aria-label="Other views of the stretch test"><p class="eyebrow">Other views</p><ul>{items}</ul></nav>'
    return (f'<header class="vhead"><div><p class="eyebrow">{e(eyebrow_)}</p>'
            f'<h1 class="display" id="{view}-h1" tabindex="-1">{e(h1)}</h1><div class="deck">{EX.copy_html(deck)}</div>{extra}</div>{lk}</header>')


def how_short(view):
    li = ''.join(f'<li>{e(x)}</li>' for x in EX.HOW_SHORT)
    return (f'<details class="howto" id="{view}-read" open><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> how to read our charts, in short</span></summary>'
            f'<ol>{li}</ol></details>')


def index_nav(view):
    li = ''.join(f'<li><a href="#{view}/{s.lower()}"><b>{s}</b> {e(SPECS[s]["form"])}</a></li>' for s in ORDER)
    return (f'<details class="index" open><summary><span><span class="sw-c">Show</span><span class="sw-o">Hide</span> the six charts</span></summary>'
            f'<nav aria-label="The six charts on this view"><ol>{li}</ol></nav></details>')


TOKEN_USE = {
    'arrow': 'S11, S12, S15',
    'shift_axis': 'S11',
    'tile': 'S12',
    'tile_arrow': 'S12',
    'spark': 'S13',
    'columns': 'S14',
    'bubble': 'S16',
    'results': 'S15',
    'tag': 'S11',
}
TOKEN_UNITS = {
    'arrow': {'shaft': 'px, line width', 'head_len': 'px', 'head_half': 'px', 'phone_head_len': 'px', 'phone_head_half': 'px',
              'tail_r': 'px, radius', 'tip_r': 'px, radius', 'key_points': 'percentage points'},
    'shift_axis': {'pitch': 'px between rows', 'label': 'px, type size', 'break_gap': 'px', 'far_segment': 'percentage points',
                   'near_segment': 'percentage points', 'tick_step': 'percentage points', 'phone_lollipop_ppp': 'px per point',
                   'phone_lollipop_pitch': 'px between rows'},
    'tile': {'size_max': 'px', 'gap': 'px', 'mid_gap': 'px', 'phone_gap': 'px', 'phone_cols': 'columns', 'frame': 'px, line width',
             'phone_steps': 'percentage points, lower edges of steps 2 to 4'},
    'tile_arrow': {'key_points': 'percentage points'},
    'spark': {'px_per_point': 'px per percentage point', 'phone_px_per_point': 'px per percentage point', 'domain': 'percent change',
              'ticks': 'percent change', 'line': 'px, line width', 'context': 'px, line width', 'end_r': 'px, radius',
              'gap_x': 'px', 'phone_gap_x': 'px'},
    'columns': {'fill_share': 'share of a month’s width', 'avg_line': 'px, line width', 'prelim_months': 'months', 'vertex_r': 'px, radius',
                'domain': 'thousand jobs', 'ticks': 'thousand jobs', 'height': 'px', 'phone_height': 'px'},
    'bubble': {'r_max': 'px, radius of the largest circle per artboard', 'gap': 'px', 'outline': 'px, line width', 'ring': 'px, line width',
               'bins': 'percent, lower edges of steps 2 to 5', 'key_millions': 'million people', 'key_seg': 'px per step',
               'label_pad': 'px', 'leader_clear': 'px between a leader’s label and any other circle'},
    'results': {'gap': 'px', 'bar': 'px, bar height', 'bar_gap': 'px', 'shift_px_per_point': 'px per point', 'shift_head': 'px',
                'shift_min': 'px, column width', 'html_headroom': 'ratio applied to measured HTML text',
                'two_line_min': 'px, narrowest container for two-line cards'},
    'tag': {'pad_x': 'px each side of the measured text', 'height': 'px, box height for 13 px text',
            'ascent_em': 'em, top of the d above the baseline', 'descent_em': 'em, foot of the g below the baseline'},
}


def tokens_table():
    """One row per token, printed exactly as the code writes it, outside the copy function."""
    rows_ = []
    for grp, d in STRETCH_TOKENS.items():
        for k_, v in d.items():
            unit = TOKEN_UNITS[grp][k_]
            rows_.append(f'<tr><th scope="row"><code>{html.escape(grp)}.{html.escape(k_)}</code></th>'
                         f'<td><code>{html.escape(repr(v))}</code></td><td>{e(unit)}</td><td>{e(TOKEN_USE[grp])}</td></tr>')
    assert all(set(d) == set(TOKEN_UNITS[g]) for g, d in STRETCH_TOKENS.items())
    return (f'<section class="ssec" id="newsprint-tokens" aria-labelledby="tok-h"><h2 class="headline" id="tok-h">New tokens</h2>'
            f'<p class="lede">{e("The sizes these six forms add to Explainer’s chart tokens, one row each, as the code writes them, so the kit can adopt them. Every other size on this page is an Explainer token.")}</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="New tokens, table"><table class="eqt toktbl"><caption>STRETCH_TOKENS, which extends CHART_TOKENS</caption>'
            f'<thead><tr><th scope="col">Token</th><th scope="col">Value</th><th scope="col">Unit</th><th scope="col">Used by</th></tr></thead><tbody>{"".join(rows_)}</tbody></table></div></section>')


DECK = ('<p>Six forms the ten Explainer charts lack, from the range of Dustin\'s newspaper references: shift arrows, a tile map '
        'of shifts, small-multiple sparklines, monthly columns with an average, a results table and a bubble map. Each is drawn '
        'by a generator on Explainer\'s kit, on Newsprint, from the shared chart data.</p>'
        '<p class="wideonly">Three of the six show election results. Party marks stay in neutral inks with the party named in words, and '
        'arrows and position carry direction. No chart on this page takes the working red, and only the results table moves: '
        'it sorts by any column.</p>')


def view_newsprint():
    body = ''.join(specimen('newsprint', s) for s in ORDER if s in SPEC_FN)
    return (f'<section class="view" data-view-root="newsprint" data-ground="news" aria-labelledby="newsprint-h1"><div class="wrap">'
            f'{view_head("newsprint", "Chart system 01 · Explainer · Stretch test", "Six new forms", DECK)}{how_short("newsprint")}'
            f'{index_nav("newsprint")}{body}{tokens_table()}</div></section>')


DARK_PICK = ('S14', 'S16')


def view_dark():
    deck = ('<p>Two of the six on Charcoal. The jobs chart, because charts of monthly numbers travel as dark social cards; '
            'the bubble map, because its turnout ramp has to run the other way on a dark ground, lighter for more.</p>')
    body = ''.join(specimen('dark', s) for s in DARK_PICK if s in SPEC_FN)
    return (f'<section class="view" data-view-root="dark" data-ground="dark" aria-labelledby="dark-h1" hidden><div class="wrap">'
            f'{view_head("dark", "Chart system 01 · Explainer · Stretch test", "On Charcoal", deck)}{body}</div></section>')


def view_phone():
    deck = ('<p>Every figure at 358 pixels, the width its phone drawing is made for, set side by side so all six read on one '
            'screen. These are the same figures as on Newsprint, with the same data and attributes.</p>')
    figs = ''.join(f'<div class="pcell">{stretch_figure("phone", s)}</div>' for s in ORDER if s in SPEC_FN)
    return (f'<section class="view" data-view-root="phone" data-ground="news" aria-labelledby="phone-h1" hidden><div class="wrap">'
            f'{view_head("phone", "Chart system 01 · Explainer · Stretch test", "On phones", deck)}<div class="pgrid">{figs}</div></div></section>')


def css_add():
    """The added stylesheet, with its sizes read from STRETCH_TOKENS so the printed table and the drawing agree."""
    return (CSS_ADD.replace('BUB_OUTLINE', f'{ST["bubble"]["outline"]}px').replace('BUB_RING', f'{ST["bubble"]["ring"]}px')
            .replace('TILE_FRAME', f'{ST["tile"]["frame"]}px'))


def stretch_ground_css():
    return '\n'.join(f'[data-ground="{name}"]{{{";".join(f"--{k}:{v}" for k, v in SGROUNDS[name].items())}}}' for name in ('white', 'news', 'dark'))


CSS_ADD = r"""
.s-arw{stroke:var(--ink);stroke-width:2px;fill:none;stroke-linecap:butt}
.f-head{fill:var(--ink)}
.f-tail,.f-tip{fill:var(--ink)}
.s-even{stroke:var(--ink);stroke-width:1.5px;fill:none}
.s-spk{stroke:var(--ink);stroke-width:2px;fill:none;stroke-linejoin:round;stroke-linecap:round}
.s-subd{stroke:var(--ink);stroke-width:3px;fill:none;stroke-dasharray:5 3;stroke-linecap:butt}
.s-frame{stroke:var(--ink);stroke-width:TILE_FRAME;fill:none}
.s-tag{stroke:var(--ink);stroke-width:1px;fill:none}
.fnw{container-type:inline-size}
.fnw .n-phone{display:none}
@container (max-width:599.98px){.fnw .n-wide{display:none}.fnw .n-phone{display:list-item}}
.s-zero{stroke:var(--ink);stroke-width:1px;fill:none}
.s-case{stroke:var(--g);stroke-width:7px;fill:none;stroke-linejoin:round;stroke-linecap:round}
.f-area{fill:var(--lt2)}
.f-land{fill:var(--land);stroke:var(--border);stroke-width:0.75px}
.ps0{fill:var(--ps0)}.ps1{fill:var(--ps1)}.ps2{fill:var(--ps2)}.ps3{fill:var(--ps3)}
.pt0{fill:var(--pt0)}.pt1{fill:var(--pt1)}.pt2{fill:var(--pt2)}.pt3{fill:var(--pt3)}
.q1{fill:var(--q1)}.q2{fill:var(--q2)}.q3{fill:var(--q3)}.q4{fill:var(--q4)}.q5{fill:var(--q5)}
.qt1{fill:var(--qt1)}.qt2{fill:var(--qt2)}.qt3{fill:var(--qt3)}.qt4{fill:var(--qt4)}.qt5{fill:var(--qt5)}
.bub{stroke:var(--qk);stroke-width:BUB_OUTLINE}
.bub.bubring{stroke:var(--ink);stroke-width:BUB_RING}
.f-none{fill:none}.s-keyc{stroke:var(--ink);stroke-width:1px}
.s-arw,.f-head,.s-even,.s-spk,.s-subd,.s-frame,.s-tag,.s-zero,.s-case,.f-land,.bub,.s-keyc{vector-effect:non-scaling-stroke}
.vhead+.spec{margin-top:0;border-top:0}
.pgrid{display:grid;grid-template-columns:repeat(3,358px);justify-content:space-between;gap:72px 40px;margin-top:40px}
.pcell{min-width:0}
.pcell .fig{max-width:358px}
.pcell .ct{font-size:22px;line-height:27px}
.pcell .ms{font-size:15px;line-height:22px}
.pcell .srcrow{flex-direction:column;gap:4px}
.pcell .credit{white-space:normal}
.toktbl code{font-size:13px;line-height:18px;word-break:break-word}
.toktbl tbody th code{white-space:nowrap;word-break:normal}
.index ol{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:899.98px){.index ol{grid-template-columns:minmax(0,1fr)}}
@media (max-width:1199.98px){.pgrid{grid-template-columns:repeat(2,358px);justify-content:start}}
@media (max-width:899.98px){.pgrid{grid-template-columns:minmax(0,358px);gap:56px}}
"""

JS = r"""
(function(){
  'use strict';
  var VIEWS=['newsprint','dark','phone'], GROUND={newsprint:'news',dark:'dark',phone:'news'};
  var NAMES={newsprint:'Newsprint',dark:'Charcoal',phone:'Phones'};
  var last=null;
  function parse(){var p=decodeURIComponent(location.hash.slice(1)).toLowerCase().split('/'); var v=VIEWS.indexOf(p[0])>=0?p[0]:'newsprint'; return {v:v,sub:p[1]||null};}
  function show(){
    var p=parse();
    [].forEach.call(document.querySelectorAll('[data-view-root]'),function(r){r.hidden=r.getAttribute('data-view-root')!==p.v;});
    document.documentElement.setAttribute('data-ground',GROUND[p.v]);
    document.title=NAMES[p.v]+' · Stretch Test · Explainer Chart System';
    [].forEach.call(document.querySelectorAll('.tabs a'),function(a){ if(a.getAttribute('href')==='#'+p.v) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');});
    if(p.sub){var t=document.getElementById(p.v+'-'+p.sub); if(t){ if(t.tagName==='DETAILS') t.open=true; t.scrollIntoView({block:'start'}); var h=t.querySelector('h2,summary'); if(h){ if(h.tagName==='H2') h.setAttribute('tabindex','-1'); h.focus({preventScroll:true});}}}
    else if(last!==null&&last!==p.v){window.scrollTo(0,0); var h1=document.getElementById(p.v+'-h1'); if(h1) h1.focus({preventScroll:true});}
    last=p.v;
  }
  addEventListener('hashchange',show);
  var skip=document.querySelector('.skip');
  if(skip) skip.addEventListener('click',function(ev){ev.preventDefault(); var h=document.getElementById(parse().v+'-h1'); if(h){h.focus(); h.scrollIntoView({block:'start'});}});
  if(innerWidth<600){[].forEach.call(document.querySelectorAll('details.howto,details.index'),function(d){d.removeAttribute('open');});}
  [].forEach.call(document.querySelectorAll('table.results'),function(t){
    var tb=t.tBodies[0], status=document.getElementById(t.id.replace('-table','-status'));
    var FIRST={name:'ascending',m24:'ascending',m20:'ascending',shift:'descending'};
    var WORDS={name:'state name',m24:'2024 margin',m20:'2020 margin',shift:'shift toward the Republican nominee'};
    function sortBy(key,dir){
      var rows=[].slice.call(tb.querySelectorAll('tr[data-row]')), div=tb.querySelector('tr[data-divider]');
      rows.sort(function(a,b){
        var x=a.getAttribute('data-'+key), y=b.getAttribute('data-'+key);
        var c=key==='name'?x.localeCompare(y):parseFloat(x)-parseFloat(y);
        if(c===0) c=a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
        return dir==='ascending'?c:-c;
      });
      rows.forEach(function(r){tb.appendChild(r);});
      if(div){
        if(key==='m24'){
          var s0=parseFloat(rows[0].getAttribute('data-m24'))>0, i=0;
          while(i<rows.length&&(parseFloat(rows[i].getAttribute('data-m24'))>0)===s0) i++;
          div.querySelector('.evtext').textContent=div.getAttribute(dir==='ascending'?'data-asc':'data-desc');
          tb.insertBefore(div,rows[i]||null); div.hidden=false;
        } else { div.hidden=true; }
      }
      [].forEach.call(t.querySelectorAll('thead th[data-sort]'),function(th){ if(th.getAttribute('data-sort')===key) th.setAttribute('aria-sort',dir); else th.removeAttribute('aria-sort');});
      var how={name:['A to Z','Z to A'],shift:['smallest first','largest first'],m24:['largest Democratic lead first','largest Republican lead first'],m20:['largest Democratic lead first','largest Republican lead first']}[key];
      if(status) status.textContent='Sorted by '+WORDS[key]+', '+how[dir==='ascending'?0:1]+'.';
    }
    [].forEach.call(t.querySelectorAll('thead th[data-sort] button'),function(b){
      b.addEventListener('click',function(){
        var th=b.parentNode, key=th.getAttribute('data-sort'), cur=th.getAttribute('aria-sort');
        sortBy(key, cur==='ascending'?'descending':cur==='descending'?'ascending':FIRST[key]);
      });
    });
  });
  show();
})();
"""


def build():
    views = ' '.join(v for v, _ in VIEWS)
    page = ('<!doctype html><html lang="en" data-ground="news"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Newsprint · Stretch Test · Explainer Chart System</title>'
            f'<meta name="chart-views" content="{views}">'
            f'<meta name="chart-specs" content="{" ".join(ORDER)}">'
            '<meta name="description" content="The stretch test for chart system 01, Explainer: six new chart forms on Newsprint, two on Charcoal and all six at phone width.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800'
            '&family=Lora:ital@1&display=swap" rel="stylesheet">'
            f'<style>{EX.ground_css()}\n{stretch_ground_css()}{EX.CSS}{css_add()}{s15_css()}</style></head><body>'
            '<a class="skip" href="#newsprint">Skip to the view</a>'
            + masthead() + '<main id="main">'
            + view_newsprint() + view_dark() + view_phone()
            + '</main>' + footer() + f'<script>{JS}</script></body></html>')
    text_only = re.sub(r'<(script|style|pre|code)\b.*?</\1>', '', page, flags=re.S)   # code prints tokens exactly as written
    assert '—' not in text_only, 'em dash in page'
    visible = html.unescape(re.sub(r'<[^>]+>', ' ', text_only))
    for m in re.finditer(r'(?:(?<=\s)|(?<=\())-\d', visible):
        raise AssertionError(f'hyphen used as a minus: {visible[m.start() - 20:m.end() + 10]}')
    straight = re.findall(r"\w'\w|\"", re.sub(r'\s+', ' ', visible))
    assert not straight, f'straight quotes in copy: {straight[:5]}'
    OUT.write_text(page)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1024:.0f} KB; fonts from {EX.FONTDIR}')


SPEC_FN.update({'S11': spec_s11, 'S12': spec_s12, 'S13': spec_s13, 'S14': spec_s14, 'S15': spec_s15, 'S16': spec_s16})

if __name__ == '__main__':
    build()
