"""Atlas concept 11, Flywheels and Governors. Oath & Action Edition 06, Phase 2, October 30, 2026.

Builds 20261030_Concept-11-Flywheels-And-Governors.html beside this file from the model export alone:
    python3 -I work/boards/phase-2/atlas-concepts/11-flywheels-and-governors/build_concept.py

The idea: every loop is a machine part. A reinforcing loop is a flywheel, a balancing loop a governor, and loops that
share a variable are pinned together at a pin named for it. Every label, sign, grade, delay, count and title is read
from work/boards/phase-2/maps/20261028_Maps-Model-Data.json. The machine's wheel and pin positions come from
20261030_Concept-11-Machine-Layout.json, written by machine_layout.py in this folder (positions only, no model facts).
"""
import html
import importlib.util
import json
import math
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

M = acc.load_model()
NODES, LINKS, LOOPS, REFORMS = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
GROUPS = M['groups']
GLOSS = M['glossary']
COUNTS = M['generated']['counts']
SNAP = M['generated']['snapshot']
OUT = HERE / '20261030_Concept-11-Flywheels-And-Governors.html'
LAYOUT = json.loads((HERE / '20261030_Concept-11-Machine-Layout.json').read_text())
SHARED = ROOT / 'work/boards/phase-2/atlas-concepts/shared'

MINUS = '−'
CH, NP, DIM, ST, RED, WH = '#121212', '#DCD9D2', '#A3A19C', '#5D636D', '#E63946', '#FFFFFF'
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def e(s):
    return html.escape(str(s), quote=True)


def n2(x):
    s = f'{x:.2f}'
    return s.rstrip('0').rstrip('.') if '.' in s else s


def long_date(iso):
    y, mo, d = iso.split('-')
    return f'{MONTHS[int(mo) - 1]} {int(d)}, {y}'


SNAP_WORDS = long_date(SNAP)

# ------------------------------------------------------------------ model facts derived by script
LOOP_IDS = M['loop_order']
STATION_COUNT = {}
for _lid in LOOP_IDS:
    for _s in LOOPS[_lid]['stations']:
        if _s['code']:
            STATION_COUNT[_s['code']] = STATION_COUNT.get(_s['code'], 0) + 1
PINS = [n for n in M['order'] if STATION_COUNT.get(n, 0) >= 2]          # variables on two or more loops
ON_NO_LOOP = [n for n in M['order'] if STATION_COUNT.get(n, 0) == 0]
COUPLED = [lid for lid in LOOP_IDS if any(s['code'] in PINS for s in LOOPS[lid]['stations'])]
STANDALONE = [lid for lid in LOOP_IDS if lid not in COUPLED]
LOOPS_OF_PIN = {p: [lid for lid in LOOP_IDS if any(s['code'] == p for s in LOOPS[lid]['stations'])] for p in PINS}
GROUP_OF = {lid: g['id'] for g in GROUPS for lid in g['loops']}
ON_LOOP_LINKS = {s['id'] for lid in LOOP_IDS for s in LOOPS[lid]['steps'] if s['id']}
OFF_LOOP_LINK_COUNT = len(LINKS) - len(ON_LOOP_LINKS)
N_REINF = sum(1 for l in LOOPS.values() if l['type'] == 'R')
N_BAL = sum(1 for l in LOOPS.values() if l['type'] == 'B')
BUSIEST = max(PINS, key=lambda p: len(LOOPS_OF_PIN[p]))
SHARED_STEP = [k for k in sorted(ON_LOOP_LINKS) if sum(1 for lid in LOOP_IDS for s in LOOPS[lid]['steps'] if s['id'] == k) >= 3]
assert len(PINS) == 16 and len(ON_NO_LOOP) == 26 and BUSIEST == 'E1' and SHARED_STEP == ['L42']


def area_of(code):
    return NODES[code]['area']


def label(code):
    return NODES[code]['label']


def lower_first(s):
    return s[0].lower() + s[1:] if len(s) > 1 and s[1].islower() else s


def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


def texture(g):
    return acc.GRADES[g][2] if g else 'hollow'


def sign_glyph(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def verb(p):
    return acc.SIGN_WORDS.get(p if p in ('+', '-') else None)


def loop_kind(lid):
    L = LOOPS[lid]
    return f"{L['kind_word']}, {L['kind_gloss']}"


def machine_word(lid):
    return 'flywheel' if LOOPS[lid]['type'] == 'R' else 'governor'


def steps_attr(lid):
    L = LOOPS[lid]
    return 'sketch' if L['conceptual'] else ' '.join(s['id'] for s in L['steps'])


def station_name(st):
    return st['label']


def read_aloud(lid):
    """More/less along the chain, from the signs alone, so the sentence cannot drift from the model."""
    L = LOOPS[lid]
    sts = L['stations']
    sign = 1
    parts = [f'More {lower_first(station_name(sts[0]))}']
    for i, step in enumerate(L['steps']):
        sign *= -1 if step['polarity'] == '-' else 1
        nxt = sts[(i + 1) % len(sts)]
        word = 'more' if sign > 0 else 'less'
        if i == len(L['steps']) - 1:
            parts.append(f'and back to {word} {lower_first(station_name(nxt))}')
        else:
            parts.append(f'{word} {lower_first(station_name(nxt))}')
    return ', '.join(parts) + '.'


def first_sentence(s):
    m = re.match(r'(.+?[.!?])(\s|$)', s)
    return m.group(1) if m else s


def cap(s):
    return s[0].upper() + s[1:]


def join_words(items):
    items = list(items)
    if len(items) <= 1:
        return ''.join(items)
    if len(items) == 2:
        return f'{items[0]} and {items[1]}'
    return ', '.join(items[:-1]) + f' and {items[-1]}'


NUM_WORDS = {2: 'Both', 3: 'All three', 4: 'All four'}


def weakest_line(lid):
    L = LOOPS[lid]
    if L['conceptual']:
        return 'No numbered steps to grade'
    if L['weakest']:
        ws = L['weakest']
        g = grade_word(LINKS[ws[0]]['evidence'])
        return f"Weakest step{'s' if len(ws) > 1 else ''} {join_words(ws)}, {g}"
    grades = [s['evidence'] for s in L['steps']]
    if len(set(grades)) == 1:
        return f"{NUM_WORDS[len(grades)]} steps {grade_word(grades[0]).lower()}"
    return 'Steps graded ' + join_words(sorted({grade_word(g) for g in grades}, key=lambda w: w))


def reform_count_line(lid):
    n = len(LOOPS[lid]['reforms'])
    return 'No reform listed' if n == 0 else f"{n} reform{'s' if n != 1 else ''}"


def status_line(lid):
    L = LOOPS[lid]
    return ' · '.join([cap(L['direction_word']), cap(L['delay_word']), weakest_line(lid), reform_count_line(lid)])


def closure_flag(lid):
    L = LOOPS[lid]
    if L['conceptual']:
        return 'Sketch: no complete numbered chain'
    if L['hypothesized']:
        return 'Closed with a hypothesized step'
    return ''


def shares_line(lid):
    """Which other loops this wheel is pinned to, and at which variable."""
    out = []
    for s in LOOPS[lid]['stations']:
        if s['code'] in PINS:
            others = [x for x in LOOPS_OF_PIN[s['code']] if x != lid]
            out.append((s['code'], s['label'], others))
    return out


# ------------------------------------------------------------------ text measure (Inter, approximate advance widths)
_NARROW = set("iIjl.,:;'!|")
_SEMI = set('ftr()[]-/')
_WIDE = set('mwMW')


def tw(s, size, weight=500, face='inter'):
    w = 0.0
    for c in s:
        if c in _NARROW:
            k = 0.26
        elif c == ' ':
            k = 0.27
        elif c in _SEMI:
            k = 0.36
        elif c in _WIDE:
            k = 0.86
        elif c.isupper():
            k = 0.68
        elif c.isdigit():
            k = 0.62
        else:
            k = 0.56
        w += k
    w *= size
    w *= {400: 1.0, 500: 1.02, 600: 1.05, 700: 1.08, 800: 1.1}[weight]
    if face == 'tight':
        w *= 0.92
    return w


def wrap(s, maxw, size, weight=500, face='inter'):
    words, lines, cur = s.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if cur and tw(t, size, weight, face) > maxw:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def svg_text(x, y, lines, size, lh, cls, anchor='start', extra=''):
    """Multi-line SVG text; y is the first baseline."""
    out = [f'<text x="{n2(x)}" y="{n2(y)}" class="{cls}" text-anchor="{anchor}"{extra}>']
    for i, ln in enumerate(lines):
        out.append(f'<tspan x="{n2(x)}" dy="{0 if i == 0 else lh}">{e(ln)}</tspan>')
    out.append('</text>')
    return ''.join(out)


# ------------------------------------------------------------------ line code (design frame memo, section 3)
ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 2)}   # body, point, height, sign length, bar


def pattern(tex, w):
    if tex == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if tex == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if tex == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def fitted(tex, w, length):
    arr, capstyle = pattern(tex, w)
    if arr is None:
        return 'none', capstyle
    if tex == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.3f}', capstyle
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.3f}' for x in arr), capstyle


def pt(cx, cy, r, a):
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc_d(cx, cy, r, a0, a1):
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) > math.pi else 0
    return f'M{n2(x0)} {n2(y0)}A{n2(r)} {n2(r)} 0 {large} 1 {n2(x1)} {n2(y1)}'


def tag_svg(x, y, ang, sign, w):
    """The pointing tag (D2-56): a solid tag along the line, pointing the way the step runs, sign bars in the ground."""
    a, p, h, sl, sb = TAG[w]
    Lt = a + p
    pts = [(-Lt / 2, -h / 2), (-Lt / 2 + a, -h / 2), (Lt / 2, 0), (-Lt / 2 + a, h / 2), (-Lt / 2, h / 2)]
    bx = -Lt / 2 + a / 2
    deg = math.degrees(ang)
    poly = ' '.join(f'{n2(px)},{n2(py)}' for px, py in pts)
    s = f'<g class="tag" transform="translate({n2(x)} {n2(y)}) rotate({n2(deg)})">'
    s += f'<polygon class="tagb" points="{poly}"/>'
    # the sign stays upright inside the tag
    s += f'<g transform="translate({n2(bx)} 0) rotate({n2(-deg)})">'
    s += f'<rect class="tags" x="{n2(-sl / 2)}" y="{n2(-sb / 2)}" width="{sl}" height="{sb}"/>'
    if sign == '+':
        s += f'<rect class="tags" x="{n2(-sb / 2)}" y="{n2(-sl / 2)}" width="{sb}" height="{sl}"/>'
    s += '</g></g>'
    return s


def head_svg(cx, cy, r, a_tip, w):
    """A closed head whose tip sits on the arc; the path stops at its base."""
    al, ab = ARROW[w]
    a_base = a_tip - al / r
    tx, ty = pt(cx, cy, r, a_tip)
    bx, by = pt(cx, cy, r, a_base)
    nx, ny = math.cos(a_base), math.sin(a_base)
    p1 = (bx + nx * ab / 2, by + ny * ab / 2)
    p2 = (bx - nx * ab / 2, by - ny * ab / 2)
    return f'<path class="head" d="M{n2(p1[0])} {n2(p1[1])}L{n2(tx)} {n2(ty)}L{n2(p2[0])} {n2(p2[1])}Z"/>'


def tick_svg(cx, cy, r, a, w):
    half = w / 2 + 4
    x0, y0 = pt(cx, cy, r - half, a)
    x1, y1 = pt(cx, cy, r + half, a)
    return f'<line class="tick" x1="{n2(x0)}" y1="{n2(y0)}" x2="{n2(x1)}" y2="{n2(y1)}"/>'


DELAY_TICKS = {'S': 1, 'M': 2, 'L': 3}


def step_on_rim(cx, cy, r, a_from, a_to, step, w, gap_from, gap_to, ticks=False, tag=True, hit=False,
                sizes=(2, 3, 6)):
    """One step as an arc of the rim, clockwise from a_from to a_to (radians, a_to > a_from).
    Returns svg, and the arc's mid angle. Dash patterns are fitted per state weight and swapped by CSS."""
    al, _ = ARROW[w]
    a0 = a_from + gap_from / r
    a_tip = a_to - gap_to / r
    a_base = a_tip - al / r
    tex = texture(step.get('evidence'))
    parts = []
    if tex == 'hollow':
        for rr in (r - (w + 1) / 2, r + (w + 1) / 2):
            parts.append(f'<path class="rail" d="{arc_d(cx, cy, rr, a0, a_base)}"/>')
        mark = f'<path class="ak-mark rimhit" d="{arc_d(cx, cy, r, a0, a_base)}" stroke="none"/>'
        parts.insert(0, mark)
    else:
        inset = w / 2 if tex == 'dotted' else 0
        end_inset = 1.5 * w if tex == 'dotted' else 0
        b0 = a0 + inset / r
        b1 = a_base - end_inset / r
        length = r * (b1 - b0)
        styles = []
        for sw in sizes:
            da, capstyle = fitted(tex, sw, length)
            styles.append(f'--d{sw}:{da}')
        da0, capstyle = fitted(tex, w, length)
        d = arc_d(cx, cy, r, b0, b1)
        st = ';'.join(styles)
        if hit:
            parts.append(f'<path class="ak-case" d="{d}" style="{st}" stroke-linecap="{capstyle}"/>')
        parts.append(f'<path class="ak-mark" d="{d}" stroke-width="{w}" stroke-linecap="{capstyle}" '
                     f'stroke-dasharray="{da0}" style="{st}"/>')
    parts.append(head_svg(cx, cy, r, a_tip, w))
    tick_end = 0
    if ticks and step.get('delay'):
        k = DELAY_TICKS[step['delay']]
        for i in range(k):
            parts.append(tick_svg(cx, cy, r, a0 + (12 + 5 * i) / r, w))
        tick_end = 12 + 5 * (k - 1) + 2
    a_mid = (a0 + a_base) / 2
    if tag and step.get('polarity') in ('+', '-'):
        tl = TAG[w][0] + TAG[w][1]
        arc_len = r * (a_base - a0)
        s_mid = max(arc_len / 2, tick_end + 6 + tl / 2) if ticks else arc_len / 2
        a_tag = a0 + s_mid / r
        x, y = pt(cx, cy, r, a_tag)
        parts.append(tag_svg(x, y, a_tag + math.pi / 2, step['polarity'], w))
        a_mid = a_tag
    if hit:
        parts.append(f'<path class="ak-hit" d="{arc_d(cx, cy, r, a0, a_tip)}"/>')
    return ''.join(parts), a_mid


# ------------------------------------------------------------------ wheel glyphs
CANON = {2: -math.pi / 2, 3: -math.pi / 2, 4: -3 * math.pi / 4}


def station_angles(lid, phase=None):
    n = LOOPS[lid]['n']
    ph = CANON[n] if phase is None else phase
    return [ph + 2 * math.pi * k / n for k in range(n)]


def flywheel_inner(cx, cy, r, angs):
    ri = r - max(6, r * 0.13)
    hub = max(4, r * 0.09)
    s = [f'<circle class="hair" cx="{n2(cx)}" cy="{n2(cy)}" r="{n2(ri)}"/>']
    for a in angs:
        x0, y0 = pt(cx, cy, hub, a)
        x1, y1 = pt(cx, cy, ri, a)
        s.append(f'<line class="hair" x1="{n2(x0)}" y1="{n2(y0)}" x2="{n2(x1)}" y2="{n2(y1)}"/>')
    s.append(f'<circle class="hair" cx="{n2(cx)}" cy="{n2(cy)}" r="{n2(hub)}"/>')
    s.append(f'<circle class="fillink" cx="{n2(cx)}" cy="{n2(cy)}" r="{n2(max(1.6, hub * 0.4))}"/>')
    return ''.join(s)


def governor_inner(cx, cy, r):
    """The flyball governor: a spindle, two arms, two weights and a sliding collar. It stands upright."""
    top = cy - 0.56 * r
    bot = cy + 0.52 * r
    piv = (cx, cy - 0.44 * r)
    collar = cy + 0.24 * r
    bx = 0.36 * r
    by = cy - 0.02 * r
    br = max(2.6, 0.1 * r)
    s = [f'<line class="hair" x1="{n2(cx)}" y1="{n2(top)}" x2="{n2(cx)}" y2="{n2(bot)}"/>']
    for sx in (-1, 1):
        s.append(f'<line class="hair" x1="{n2(piv[0])}" y1="{n2(piv[1])}" x2="{n2(cx + sx * bx)}" y2="{n2(by)}"/>')
        s.append(f'<line class="hair" x1="{n2(cx + sx * bx)}" y1="{n2(by)}" x2="{n2(cx)}" y2="{n2(collar)}"/>')
    for sx in (-1, 1):
        s.append(f'<circle class="fillink" cx="{n2(cx + sx * bx)}" cy="{n2(by)}" r="{n2(br)}"/>')
    cw = max(5, 0.16 * r)
    s.append(f'<line class="hair" x1="{n2(cx - cw)}" y1="{n2(collar)}" x2="{n2(cx + cw)}" y2="{n2(collar)}"/>')
    s.append(f'<circle class="fillink" cx="{n2(piv[0])}" cy="{n2(piv[1])}" r="{n2(max(1.6, br * 0.55))}"/>')
    s.append(f'<line class="hair" x1="{n2(cx - cw * 1.4)}" y1="{n2(bot)}" x2="{n2(cx + cw * 1.4)}" y2="{n2(bot)}"/>')
    return ''.join(s)


def station_mark(x, y, st, size='m'):
    code = st['code']
    if not code:
        rr = {'s': 3.5, 'm': 4.5, 'l': 7}[size]
        return f'<circle class="stn-open" cx="{n2(x)}" cy="{n2(y)}" r="{rr}"/>', rr
    if code in PINS:
        rr = {'s': 4.5, 'm': 6, 'l': 11}[size]
        dot = {'s': 1.6, 'm': 2, 'l': 3.5}[size]
        return (f'<circle class="pinring" cx="{n2(x)}" cy="{n2(y)}" r="{rr}"/>'
                f'<circle class="fillink" cx="{n2(x)}" cy="{n2(y)}" r="{dot}"/>'), rr + 1
    rr = {'s': 3.2, 'm': 4, 'l': 7}[size]
    return f'<circle class="fillink stn" cx="{n2(x)}" cy="{n2(y)}" r="{rr}"/>', rr


def wheel_body(lid, cx, cy, r, angs):
    if LOOPS[lid]['type'] == 'R':
        return flywheel_inner(cx, cy, r, angs)
    return governor_inner(cx, cy, r)


def step_attrs(step):
    if not step['id']:
        return 'data-step="conceptual"'
    lk = LINKS[step['id']]
    return (f'data-link="{step["id"]}" data-sign="{sign_attr(lk["polarity"])}" data-grade="{lk["evidence"]}" '
            f'data-delay="{lk["delay"]}" data-from="{lk["from"]}" data-to="{lk["to"]}"')


def wheel_rim(lid, cx, cy, r, angs, w=2, size='m', tags=True, ticks=False, interactive=False, sizes=(2, 3, 6),
              red=False):
    """All steps of a loop as arcs on one rim, then the stations on top. Returns svg and the station points."""
    L = LOOPS[lid]
    n = L['n']
    marks, gaps, pts = [], [], []
    for k, st in enumerate(L['stations']):
        x, y = pt(cx, cy, r, angs[k])
        m_svg, rr = station_mark(x, y, st, size)
        marks.append(m_svg)
        gaps.append(rr)
        pts.append((x, y))
    out = []
    for k, step in enumerate(L['steps']):
        a_from = angs[k]
        a_to = angs[(k + 1) % n] if k + 1 < n else angs[0] + 2 * math.pi
        svg, _ = step_on_rim(cx, cy, r, a_from, a_to, step, w, gaps[k] + 3, gaps[(k + 1) % n] + 2,
                             ticks=ticks, tag=tags, hit=interactive, sizes=sizes)
        out.append(f'<g class="arc" {step_attrs(step)}>{svg}</g>')
    return ''.join(out), ''.join(marks), pts
