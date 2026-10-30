"""Build concept 07, Great Circle, for the Oath & Action systems atlas (Phase 2, October 30, 2026).

The five core areas drawn as one ring. Every core variable has a fixed place on the rim, every connection is a
chord, and every loop is a closed shape inside the ring. Reads every label, sign, grade, delay, count and title
from the model export; nothing on the page is typed by hand except studio-draft headlines and decks.

Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/07-great-circle/build_concept.py
Writes 20261030_Concept-07-Great-Circle.html beside this file.
"""
import html
import importlib.util
import json
import math
import pathlib
import re
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


acc = _load('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
g = _load('gc_geom', HERE / 'gc_geom.py')
OUT = HERE / '20261030_Concept-07-Great-Circle.html'

M = acc.load_model()
N, L, LO, RF = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
AN = {a['id']: list(a['nodes']) for a in M['areas']}
AREA_OF = {}
for a in M['areas']:
    for n in a['nodes']:
        AREA_OF[n] = a['id']
COUNTS = M['generated']['counts']
GLOSS = M['glossary']
P = acc.PALETTE
NP, CH, RED, PR, ST, VG, WH, DS = (P['newsprint'], P['charcoal'], P['pillar_red'], P['prussian'], P['stone'],
                                    P['verdigris'], P['white'], P['deep_stone'])
MINUS = '−'
E = lambda s: html.escape(str(s), quote=True)
CORE = g.CORE
CORE_VARS = [n for n in M['order'] if AREA_OF[n] in CORE]
ECO = ('production', 'household', 'money')
SAT_ORDER = ['X', 'production', 'household', 'money', 'TC']
SNAP_DATE = 'October 15, 2026'
assert M['generated']['snapshot'] == '2026-10-15'

# ------------------------------------------------------------------ words
TEX = {k: v[2] for k, v in acc.GRADES.items()}            # documented -> solid ...


def gword(ev):
    return acc.GRADES[ev][0]


def ggloss(ev):
    return acc.GRADES[ev][1]


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def verb(p):
    return acc.SIGN_WORDS.get(p if p in ('+', '-') else None)


def delay_words(d):
    return acc.DELAYS[d]


def low(s):
    return s[0].lower() + s[1:] if len(s) > 1 and not s[:2].isupper() else s


def key(kind, i):
    return f'{kind}-{i.lower()}'


def wrap(text, n):
    out, line = [], ''
    for w in text.split():
        if line and len(line) + 1 + len(w) > n:
            out.append(line)
            line = w
        else:
            line = (line + ' ' + w).strip()
    return out + ([line] if line else [])


def first_sentence(s):
    m = re.match(r'(.+?[.!?])(\s|$)', s)
    return m.group(1) if m else s


def link_say(l):
    s = l['polarity']
    if l['type'] == 'authority':
        sign = 'No sign: an authority connection says who decides'
    else:
        sign = f'Sign {sign_char(s)}, {"same way" if s == "+" else "opposite way"}'
    return (f"{l['id']}: {l['name']}. From {l['from']} {N[l['from']]['label']} to {l['to']} {N[l['to']]['label']}. "
            f"{sign}. Evidence {gword(l['evidence']).lower()}. Delay {delay_words(l['delay'])}.")


def var_say(n):
    return f"{n} {N[n]['label']}. {N[n]['increase_means']}"


def kind_line(lp):
    o = LO[lp]
    return f"{o['kind_word']}, {o['kind_gloss']}"


def read_aloud(lp):
    """The more-and-less chain, built from the signs (civic education memo, section 2)."""
    o = LO[lp]
    d, parts = 1, []
    sts = o['stations']
    for i, st in enumerate(o['steps']):
        lab = sts[i]['label'] if sts[i]['code'] is None else N[sts[i]['code']]['label']
        parts.append(f"{'more' if d > 0 else 'less'} {low(lab)}")
        d *= 1 if st['polarity'] == '+' else -1
    lab0 = sts[0]['label'] if sts[0]['code'] is None else N[sts[0]['code']]['label']
    end = f"and back to {'more' if d > 0 else 'less'} {low(lab0)}"
    s = ', '.join(parts) + ', ' + end + '.'
    return s[0].upper() + s[1:]


def status_line(lp):
    o = LO[lp]
    bits = [o['direction_word'][0].upper() + o['direction_word'][1:], o['delay_word']]
    if o['weakest']:
        w = o['weakest']
        bits.append(f"Weakest step {' and '.join(w)}, {gword(L[w[0]]['evidence'])}")
    elif o['conceptual']:
        bits.append('No numbered step to grade')
    else:
        bits.append('No weak step named')
    nr = len(o['reforms'])
    bits.append(f"{nr} reform{'s' if nr != 1 else ''}")
    return ' · '.join(bits)


def disclosure(lp):
    o = LO[lp]
    if o['conceptual']:
        return 'A sketch: no complete numbered chain. Its steps are drawn as hollow lines, which claim no grade.'
    if o['hypothesized']:
        hyp = [s['id'] for s in o['steps'] if s['evidence'] == 'hypothesis']
        return (f"Closed with a hypothesized step. {' and '.join(hyp)} {'is' if len(hyp) == 1 else 'are'} graded "
                f"hypothesis (untested), so the loop is complete only if {'that step holds' if len(hyp) == 1 else 'those steps hold'}.")
    return ''


# ------------------------------------------------------------------ counts the page prints, all computed here
core_links = [l for l in L.values() if AREA_OF[l['from']] in CORE and AREA_OF[l['to']] in CORE]
pair = Counter((AREA_OF[l['from']], AREA_OF[l['to']]) for l in L.values())
FWD = {CORE[i]: pair[(CORE[i], CORE[(i + 1) % 5])] for i in range(5)}
BACK = {CORE[i]: pair[(CORE[(i + 1) % 5], CORE[i])] for i in range(5)}
N_FWD, N_BACK = sum(FWD.values()), sum(BACK.values())
assert (N_FWD, N_BACK) == (20, 11), (N_FWD, N_BACK)        # the pitch's claim, verified by script
N_NEIGHBOR = N_FWD + N_BACK
N_CORE_LINKS = len(core_links)
N_CORE_VARS = len(CORE_VARS)
loop_links = {s['id'] for o in LO.values() for s in o['steps'] if s['id']}
N_R = sum(1 for o in LO.values() if o['type'] == 'R')
N_B = sum(1 for o in LO.values() if o['type'] == 'B')


def sat_of(n):
    a = AREA_OF[n]
    return a if a not in CORE else None


# ------------------------------------------------------------------ marks
def fmt(v):
    return f'{v:.1f}'


def tag_svg(pt, tan, sign, w, cls='tag'):
    """The pointing tag (frame memo section 3): points the way the step runs, the sign upright inside."""
    a, p, h, sl, sb = g.TAG[w]
    Lt = a + p
    ang = math.degrees(math.atan2(tan[1], tan[0]))
    x0 = -Lt / 2
    pts = [(x0, -h / 2), (x0 + a, -h / 2), (x0 + Lt, 0), (x0 + a, h / 2), (x0, h / 2)]
    poly = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    bx = x0 + a / 2
    # the glyph stays upright: draw it in the unrotated frame at the tag body's centre
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    gx, gy = pt[0] + bx * c, pt[1] + bx * s_
    glyph = f'<rect x="{gx - sl / 2:.2f}" y="{gy - sb / 2:.2f}" width="{sl}" height="{sb}"/>'
    if sign == '+':
        glyph += f'<rect x="{gx - sb / 2:.2f}" y="{gy - sl / 2:.2f}" width="{sb}" height="{sl}"/>'
    return (f'<g class="{cls}" data-sign-mark="{E(sign)}"><polygon class="tagb" points="{poly}" '
            f'transform="translate({pt[0]:.2f} {pt[1]:.2f}) rotate({ang:.2f})"/><g class="tagg">{glyph}</g></g>')


def head_svg(tip, tan, w, authority=False, cls='head'):
    if authority:
        hl, hw = 14, 11
        bx, by = tip[0] - tan[0] * hl, tip[1] - tan[1] * hl
        mx, my = (tip[0] + bx) / 2, (tip[1] + by) / 2
        nx, ny = -tan[1], tan[0]
        return (f'<path class="{cls} dia" d="M{fmt(tip[0])} {fmt(tip[1])}L{fmt(mx + nx * hw / 2)} {fmt(my + ny * hw / 2)}'
                f'L{fmt(bx)} {fmt(by)}L{fmt(mx - nx * hw / 2)} {fmt(my - ny * hw / 2)}Z"/>')
    hl, hw = g.ARROW[w]
    bx, by = tip[0] - tan[0] * hl, tip[1] - tan[1] * hl
    nx, ny = -tan[1], tan[0]
    return (f'<path class="{cls}" d="M{fmt(tip[0])} {fmt(tip[1])}L{fmt(bx + nx * hw / 2)} {fmt(by + ny * hw / 2)}'
            f'L{fmt(bx - nx * hw / 2)} {fmt(by - ny * hw / 2)}Z"/>')


def ticks_svg(body, delay, w, cls='ticks'):
    n = {'S': 1, 'M': 2, 'L': 3}[delay]
    tab = g.bez_table(body)
    out = []
    for i in range(n):
        s = 12 + i * 5
        t = g.t_at(body, s, tab)
        (x, y), (tx, ty) = g.bez(body, t), g.bez_tan(body, t)
        nx, ny = -ty, tx
        half = w / 2 + 4
        out.append(f'M{fmt(x + nx * half)} {fmt(y + ny * half)}L{fmt(x - nx * half)} {fmt(y - ny * half)}')
    return f'<path class="{cls}" d="{"".join(out)}"/>'


def stroke_body(p, w, texture, authority=False):
    """The line from tail to the head's base, with its texture fitted so it starts and ends on ink."""
    hl = 14 if authority else g.ARROW[w][0]
    inset = w / 2 if texture == 'dotted' else 0
    end_inset = 1.5 * w if texture == 'dotted' else 0
    body = g.bez_trim(p, inset, hl + end_inset)
    da, cap = g.fitted(texture, w, g.bez_len(body))
    return body, da, cap


def wire_marks(p, l, w, *, tag=True, ticks=True, tag_at=0.55, cls=''):
    """Case, mark, head, tag and delay ticks for one connection at weight w."""
    tex = TEX[l['evidence']]
    auth = l['type'] == 'authority'
    body, da, cap = stroke_body(p, w, tex, auth)
    dash = f' stroke-dasharray="{da}"' if da else ''
    d = g.d_of(body)
    s = (f'<path class="ak-case {cls}" d="{d}" stroke-linecap="{cap}"{dash}/>'
         f'<path class="ak-mark {cls}" d="{d}" stroke-width="{w}" stroke-linecap="{cap}"{dash}/>')
    tip, tan = p[3], g.bez_tan(p, 1)
    s += head_svg(tip, tan, w, auth, cls=f'head {cls}')
    if ticks:
        s += ticks_svg(body, l['delay'], w, cls=f'ticks {cls}')
    if tag and not auth:
        tab = g.bez_table(body)
        t = g.t_at(body, tab[1][-1] * tag_at, tab)
        s += tag_svg(g.bez(body, t), g.bez_tan(body, t), sign_char(l['polarity']), w, cls=f'tag {cls}')
    return s, body


def wire(l, p, w, *, rel, label='', tag=True, ticks=True, tag_at=0.55, extra_cls='', interactive=True, lit=True):
    """One connection as a selectable item: three-path wire (case, mark, hit) plus its lit form at 6 px."""
    base, body = wire_marks(p, l, w, tag=tag, ticks=ticks, tag_at=tag_at, cls='base')
    litm = ''
    if lit and w != 6:
        lm, _ = wire_marks(p, l, 6, tag=tag, ticks=False, tag_at=tag_at, cls='lit')
        litm = f'<g class="litg">{lm}</g>'
    say = link_say(l)
    sign = l['polarity'] if l['polarity'] in ('+', '-') else 'none'
    role = ' role="button"' if interactive else ''
    return (f'<g class="wire w{w} {extra_cls}"{role} data-select="{key("link", l["id"])}" data-link="{l["id"]}" '
            f'data-sign="{sign}" data-grade="{l["evidence"]}" data-delay="{l["delay"]}" data-from="{l["from"]}" '
            f'data-to="{l["to"]}" data-rel="{rel}" aria-label="{E(say)}" data-say="{E(say)}" style="--ak-w-case:{w + 2}px">'
            f'{base}{litm}<path class="ak-hit" d="{g.d_of(p)}"/>{label}</g>'), body


def text_lines(x, y, lines, cls, lh, anchor='start', extra=''):
    ts = ''.join(f'<tspan x="{fmt(x)}" dy="{0 if i == 0 else lh}">{E(t)}</tspan>' for i, t in enumerate(lines))
    return f'<text class="{cls}" x="{fmt(x)}" y="{fmt(y)}" text-anchor="{anchor}"{extra}>{ts}</text>'


def tw(s, size, weight=400):
    """Rough text width for layout (Inter); the browser check measures the real boxes."""
    k = {400: 0.54, 500: 0.56, 600: 0.58, 700: 0.60, 800: 0.62}[weight]
    return len(s) * size * k


# ------------------------------------------------------------------ the ring
class Ring:
    def __init__(self, cx, cy, r, band, weights=None, gap=1.3, anchor=('A', 315), off=1.6):
        self.cx, self.cy, self.r, self.band = cx, cy, r, band
        self.ang, self.spans = g.ring_layout(AN, weights, gap, anchor)
        self.off = off                       # departures leave a little anticlockwise, arrivals land clockwise

    def pt(self, n, r=None, d=0.0):
        return g.polar(self.cx, self.cy, self.r if r is None else r, self.ang[n] + d)

    def chord(self, l, r_end=None, skew=0.0, depth=None):
        r_end = (self.r - 2) if r_end is None else r_end
        a0 = self.ang[l['from']] - self.off
        a1 = self.ang[l['to']] + self.off
        return g.chord(self.cx, self.cy, r_end, a0, a1, depth=depth, skew=skew)

    def mid(self, a):
        s, e = self.spans[a]
        return (s + e) / 2


def dup_skews(links):
    seen = Counter()
    out = {}
    for l in links:
        k = (l['from'], l['to'])
        out[l['id']] = 0.12 * seen[k]
        seen[k] += 1
    return out


SKEW = dup_skews(L.values())


def rel_of_var(n, drawn_links, drawn_vars):
    ks = []
    for l in drawn_links:
        if n in (l['from'], l['to']):
            ks.append(key('link', l['id']))
            o = l['to'] if l['from'] == n else l['from']
            if o in drawn_vars:
                ks.append(key('var', o))
    return ' '.join(dict.fromkeys(ks))


# ================================================================== OVERVIEW
OV_W, OV_H = 978, 800
OV = Ring(489, 418, 226, 24, anchor=('A', 0))


def gate_svg(ring, i):
    """Between neighbouring areas: an arrow forward (clockwise) and one back, each with its count."""
    a, b = CORE[i], CORE[(i + 1) % 5]
    ja = (ring.spans[a][1] + ring.spans[b][0] + (360 if i == 4 else 0)) / 2
    ro = ring.r + ring.band
    out = []
    for kind, rr, sgn, n in (('fwd', ro + 13, 1, FWD[a]), ('back', ro + 30, -1, BACK[a])):
        a0, a1 = ja - 6.5, ja + 6.5
        d = g.arc_d(ring.cx, ring.cy, rr, a0, a1)
        tip_a = a1 if sgn > 0 else a0
        tip = g.polar(ring.cx, ring.cy, rr, tip_a)
        tdeg = tip_a + 90 * sgn
        tan = (math.sin(math.radians(tdeg)), -math.cos(math.radians(tdeg)))
        # stop the arc at the head's base
        base_a = tip_a - sgn * math.degrees(10 / rr)
        d = g.arc_d(ring.cx, ring.cy, rr, a0, base_a) if sgn > 0 else g.arc_d(ring.cx, ring.cy, rr, base_a, a1)
        out.append(f'<path class="gate-line" d="{d}"/>')
        out.append(head_svg(tip, tan, 2, cls='gate-head'))
        lx, ly = g.polar(ring.cx, ring.cy, rr, tip_a + sgn * 5.6)
        out.append(f'<text class="gate-n" x="{fmt(lx)}" y="{fmt(ly + 7.5)}" text-anchor="middle" '
                   f'data-count="custom:{kind}-{a}{b}">{n}</text>')
    lab = f'{a} to {b}: {FWD[a]} forward, {BACK[a]} back'
    return f'<g class="gate" aria-hidden="true" data-pair="{a}{b}"><title>{E(lab)}</title>{"".join(out)}</g>'


# Where each area's name sits beside its arc: (side, vertical placement, wrap width for its text, nudge x, nudge y)
OV_LABEL = {'A': ('top', 'above', 44, 0, 0), 'B': ('right', 'middle', 24, 0, 0), 'C': ('right', 'below', 24, 0, -6),
            'D': ('left', 'middle', 24, 0, 18), 'E': ('left', 'middle', 24, 0, -8)}


def area_label_svg(ring, a, r_lab, spec):
    """Letter as a drop cap, title beside it, the area's one line of text under the title. Left-aligned."""
    side, vpos, wrap_w, nx, ny = spec
    mid = ring.mid(a)
    x, y = g.polar(ring.cx, ring.cy, r_lab, mid)
    x, y = x + nx, y + ny
    title = AREAS[a]['title']
    tlines = [title] if side == 'top' else wrap(title, 12)
    lines = wrap(AREAS[a]['text'], wrap_w)
    lw = 36
    bw = lw + max([tw(t, 22, 800) for t in tlines] + [tw(t, 14, 400) for t in lines])
    h = 30 + 26 * (len(tlines) - 1) + 8 + 20 * len(lines)
    if side == 'right':
        left = x
    elif side == 'left':
        left = x - bw
    else:
        left = x - bw / 2
    top = y - h if vpos == 'above' else (y if vpos == 'below' else y - h / 2)
    base = top + 30
    s = f'<text class="a-letter" x="{fmt(left)}" y="{fmt(base)}">{a}</text>'
    s += text_lines(left + lw, base, tlines, 'ak-label a-title', 26, 'start')
    s += text_lines(left + lw, base + 26 * (len(tlines) - 1) + 24, lines, 'a-text', 20, 'start')
    return s


OV_SAT = {'X': (900, 70, 32), 'production': (40, 40, 26), 'household': (40, 106, 26), 'money': (40, 172, 26),
          'TC': (40, 740, 32)}


def overview_svg():
    R = OV
    ro = R.r + R.band
    core_set = set(CORE_VARS)
    rel_links = defaultdict(list)
    chords, satl = [], []
    # --- the 61 core chords, one quiet layer
    for l in core_links:
        p = R.chord(l, r_end=R.r - 9, skew=SKEW[l['id']])
        # start 2 px off the station's edge
        p = (g.polar(R.cx, R.cy, R.r - 9, R.ang[l['from']] - R.off), p[1], p[2], p[3])
        rel = f'{key("var", l["from"])} {key("var", l["to"])}'
        s, _ = wire(l, p, 2, rel=rel, tag=False, ticks=False, interactive=False, extra_cls='ctx')
        chords.append(s)
    # --- satellites: outside drivers, the three economy areas and technology, as discs beyond the rim
    SAT = OV_SAT
    sat_links = [l for l in L.values() if sat_of(l['from']) or sat_of(l['to'])]

    def sat_pt(sa, toward):
        sx, sy, sr = SAT[sa]
        dx, dy = toward[0] - sx, toward[1] - sy
        n = math.hypot(dx, dy) or 1
        return (sx + dx / n * (sr + 3), sy + dy / n * (sr + 3))

    for l in sat_links:
        fs, ts = sat_of(l['from']), sat_of(l['to'])
        if fs and ts and fs == ts:
            continue                         # inside one satellite area: listed, not drawn on the ring
        if fs and ts:
            a0 = sat_pt(fs, SAT[ts][:2])
            a1 = sat_pt(ts, SAT[fs][:2])
            mx, my = (a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2
            p = (a0, ((a0[0] * 2 + mx) / 3, (a0[1] * 2 + my) / 3), ((a1[0] * 2 + mx) / 3, (a1[1] * 2 + my) / 3), a1)
        elif fs:
            end = R.pt(l['to'], R.r - 9, R.off)
            far = R.pt(l['to'], R.r + 120, R.off)
            a0 = sat_pt(fs, far)
            inner = R.pt(l['to'], R.r - 60, R.off)
            p = (a0, far, inner, end)
        else:
            st = R.pt(l['from'], R.r - 9, -R.off)
            far = R.pt(l['from'], R.r + 120, -R.off)
            a1 = sat_pt(ts, far)
            inner = R.pt(l['from'], R.r - 60, -R.off)
            p = (st, inner, far, a1)
        if SKEW[l['id']]:
            p = (p[0], (p[1][0] + 10, p[1][1] + 10), (p[2][0] + 10, p[2][1] + 10), p[3])
        rel = ' '.join(key('var', x) for x in (l['from'], l['to']) if x in core_set)
        s, _ = wire(l, p, 2, rel=rel, tag=False, ticks=False, interactive=False, extra_cls='sat-link')
        satl.append(s)
        for x in (l['from'], l['to']):
            rel_links[x].append(l)
    # --- interactive layer
    items = []
    gates = ''.join(gate_svg(R, i) for i in range(5))
    lab_r = ro + 50
    for a in CORE:
        s0, s1 = R.spans[a]
        vs = AN[a]
        rel = [key('var', v) for v in vs] + [key('link', l['id']) for l in core_links if a in (AREA_OF[l['from']], AREA_OF[l['to']])]
        nlinks = sum(1 for l in L.values() if a in (AREA_OF[l['from']], AREA_OF[l['to']]))
        say = f"Area {a}, {AREAS[a]['title']}. {AREAS[a]['text']} {len(vs)} variables, {nlinks} connections."
        inner = (f'<path class="band" d="{g.band_d(R.cx, R.cy, R.r, ro, s0, s1)}"/>'
                 f'<path class="ak-case selarc" d="{g.arc_d(R.cx, R.cy, ro + 5, s0, s1)}"/>'
                 f'<path class="ak-mark selarc" d="{g.arc_d(R.cx, R.cy, ro + 5, s0, s1)}"/>'
                 + area_label_svg(R, a, lab_r, OV_LABEL[a]))
        if a == 'C':
            items.append(f'<a class="area" href="#area-c" data-area="C" data-rel="{" ".join(rel)}" '
                         f'aria-label="{E(say)} Opens the close-up." data-say="{E(say)} Opens the close-up.">{inner}</a>')
        else:
            items.append(f'<g class="area" role="button" data-select="area-{a.lower()}" data-area="{a}" data-rel="{" ".join(rel)}" '
                         f'aria-label="{E(say)} Opens its record." data-say="{E(say)} Opens its record.">{inner}</g>')
    # loops: a badge inside the ring at the middle of the loop's own shape, holding its lit route
    items += loop_badges(R)
    # stations on the rim
    for n in CORE_VARS:
        x, y = R.pt(n)
        cx_, cy_ = R.pt(n, R.r + R.band / 2)
        rel = rel_of_var(n, [l for l in L.values() if n in (l['from'], l['to'])], core_set)
        say = var_say(n)
        items.append(f'<g class="stn" role="button" data-select="{key("var", n)}" data-node="{n}" data-rel="{rel}" '
                     f'aria-label="{E(say)}" data-say="{E(say)}" style="--ak-w-case:4px">'
                     f'<circle class="ak-case" cx="{fmt(x)}" cy="{fmt(y)}" r="6"/>'
                     f'<circle class="ak-mark node" cx="{fmt(x)}" cy="{fmt(y)}" r="6" stroke-width="2"/>'
                     f'<circle class="hitc" cx="{fmt((x + cx_) / 2)}" cy="{fmt((y + cy_) / 2)}" r="13"/>'
                     f'<text class="code ak-label" x="{fmt(cx_)}" y="{fmt(cy_ + 4.6)}" text-anchor="middle">{n}</text></g>')
    # satellites
    for sa in SAT_ORDER:
        sx, sy, sr = SAT[sa]
        vs = AN[sa]
        ls = [l for l in L.values() if sa in (AREA_OF[l['from']], AREA_OF[l['to']])]
        to_core = [l for l in ls if (AREA_OF[l['from']] in CORE) or (AREA_OF[l['to']] in CORE)]
        rel = ' '.join(dict.fromkeys([key('link', l['id']) for l in ls] +
                                     [key('var', x) for l in ls for x in (l['from'], l['to']) if x in core_set]))
        title = AREAS[sa]['title']
        say = f"Area {sa if sa in ('X', 'TC') else title}, {title}. {AREAS[sa]['text']} {len(vs)} variables, {len(to_core)} connections with the ring."
        lines = wrap(title, 16)
        lh = 18
        ty = sy + 5 - lh * (len(lines) - 1) / 2
        if sa == 'X':
            tx, anchor = sx - sr - 10, 'end'
        else:
            tx, anchor = sx + sr + 10, 'start'
        items.append(
            f'<g class="sat" role="button" data-select="area-{sa.lower()}" data-area="{sa}" data-rel="{rel}" '
            f'aria-label="{E(say)}" data-say="{E(say)}" style="--ak-w-case:4px">'
            f'<circle class="ak-case" cx="{sx}" cy="{sy}" r="{sr}"/>'
            f'<circle class="ak-mark disc" cx="{sx}" cy="{sy}" r="{sr}" stroke-width="2"/>'
            f'<text class="sat-n" x="{sx}" y="{sy + 8}" text-anchor="middle" data-count="variables_{sa}">{len(vs)}</text>'
            + text_lines(tx, ty, lines, 'ak-label sat-t', lh, anchor)
            + '</g>')
    svg = (f'<svg class="ov" data-view="overview" viewBox="0 0 {OV_W} {OV_H}" role="group" aria-labelledby="h-overview">'
           f'<g class="layer-chords" aria-hidden="true">{"".join(chords)}</g>'
           f'<g class="layer-sat" aria-hidden="true">{"".join(satl)}</g>'
           f'<g class="layer-gates">{gates}</g>'
           f'<g class="layer-items" data-ak-roving data-ak-nav="spatial">{"".join(items)}</g></svg>')
    return svg


# ------------------------------------------------------------------ loops on a ring
def loop_route(ring, lp, w, r_end, *, cls='route', heads=True, tags=True):
    """The loop's steps as chords on this ring, with stations. Sketched loops draw hollow."""
    o = LO[lp]
    out = []
    pts = []
    if o['conceptual']:
        # stations that are not variables sit inside the ring beside the variables the sketch is tied to
        anchors = SKETCH_ANCHOR[lp]
        base = g.circ_mean([ring.ang[a] for a in anchors])
        k = len(o['stations'])
        spts = []
        for i, st in enumerate(o['stations']):
            if st['code']:
                spts.append(ring.pt(st['code'], r_end))
            else:
                aa = base + (i - (k - 1) / 2) * 16
                spts.append(g.polar(ring.cx, ring.cy, ring.r * 0.62, aa))
        for i in range(k):
            a, b = spts[i], spts[(i + 1) % k]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx, dy = b[0] - a[0], b[1] - a[1]
            nn = math.hypot(dx, dy) or 1
            bow = 0.22 * nn
            q = (mx - dy / nn * bow, my + dx / nn * bow)
            p = (a, ((a[0] + 2 * q[0]) / 3, (a[1] + 2 * q[1]) / 3), ((b[0] + 2 * q[0]) / 3, (b[1] + 2 * q[1]) / 3), b)
            body = g.bez_trim(p, 8, 9)
            d = g.d_of(body)
            gap = w if w < 6 else 6
            rail = 1 if w < 6 else 2
            out.append(f'<path class="hollow-o {cls}" d="{d}" stroke-width="{gap + 2 * rail}"/>'
                       f'<path class="hollow-i" d="{d}" stroke-width="{gap}"/>')
            if heads:
                out.append(head_svg(body[3], g.bez_tan(body, 1), 2 if w < 6 else 6, cls=f'head {cls}'))
        for i, (st, pt_) in enumerate(zip(o['stations'], spts)):
            if st['code']:
                out.append(f'<circle class="stn-dot" cx="{fmt(pt_[0])}" cy="{fmt(pt_[1])}" r="4.5"/>')
            else:
                out.append(f'<circle class="stn-open" cx="{fmt(pt_[0])}" cy="{fmt(pt_[1])}" r="6"/>')
            pts.append(pt_)
        return ''.join(out), pts
    for st in o['steps']:
        l = L[st['id']]
        p = ring.chord(l, r_end=r_end, skew=SKEW[l['id']])
        p = (g.polar(ring.cx, ring.cy, r_end, ring.ang[l['from']] - ring.off), p[1], p[2], p[3])
        m, body = wire_marks(p, l, w, tag=tags, ticks=False, tag_at=0.5, cls=cls)
        out.append(m)
        tab = g.bez_table(body)
        pts += [tab[0][i] for i in range(0, len(tab[0]), 8)]
    return ''.join(out), pts


SKETCH_ANCHOR = {}
for _lp in ('B2', 'B3', 'R9'):
    # B2 and B3 take their place from the variables their reforms target; R9 touches E2 itself
    o = LO[_lp]
    codes = [s['code'] for s in o['stations'] if s['code']]
    if codes:
        SKETCH_ANCHOR[_lp] = codes
    else:
        tg = [t for r in o['reforms'] for t in RF[r]['targets'] if t in N and AREA_OF[t] in CORE]
        SKETCH_ANCHOR[_lp] = list(dict.fromkeys(tg))


def loop_badges(R):
    items = []
    placed = []
    pos = {}
    for lp in M['loop_order']:
        o = LO[lp]
        _, pts = loop_route(R, lp, 6, R.r - 9)
        x = sum(p[0] for p in pts) / len(pts)
        y = sum(p[1] for p in pts) / len(pts)
        pos[lp] = [x, y]
    # relax: keep the pills apart and inside the ring, pulled toward each loop's own middle
    anchor = {k: tuple(v) for k, v in pos.items()}
    wd = {lp: 14 + 8.6 * len(lp) for lp in pos}
    for _ in range(400):
        for a in pos:
            for b in pos:
                if a >= b:
                    continue
                dx = pos[b][0] - pos[a][0]
                dy = pos[b][1] - pos[a][1]
                ox = (wd[a] + wd[b]) / 2 + 6 - abs(dx)
                oy = 22 + 6 - abs(dy)
                if ox > 0 and oy > 0:
                    if ox < oy:
                        s = 1 if dx >= 0 else -1
                        pos[a][0] -= s * ox / 2
                        pos[b][0] += s * ox / 2
                    else:
                        s = 1 if dy >= 0 else -1
                        pos[a][1] -= s * oy / 2
                        pos[b][1] += s * oy / 2
        for a in pos:
            pos[a][0] += (anchor[a][0] - pos[a][0]) * 0.02
            pos[a][1] += (anchor[a][1] - pos[a][1]) * 0.02
            dx, dy = pos[a][0] - R.cx, pos[a][1] - R.cy
            dd = math.hypot(dx, dy)
            lim = R.r - 40
            if dd > lim:
                pos[a][0] = R.cx + dx / dd * lim
                pos[a][1] = R.cy + dy / dd * lim
    for lp in M['loop_order']:
        o = LO[lp]
        route, _ = loop_route(R, lp, 6, R.r - 9, cls='rt')
        x, y = pos[lp]
        w = wd[lp]
        steps = 'sketch' if o['conceptual'] else ' '.join(s['id'] for s in o['steps'])
        codes = [s['code'] for s in o['stations'] if s['code']]
        rel = ' '.join(key('var', c) for c in codes)
        say = f"Loop {lp}, {kind_line(lp)}: {o['title']}."
        pill = (f'<rect class="ak-case pill" x="{fmt(x - w / 2)}" y="{fmt(y - 11)}" width="{fmt(w)}" height="22"/>'
                f'<rect class="ak-mark pill" x="{fmt(x - w / 2)}" y="{fmt(y - 11)}" width="{fmt(w)}" height="22" stroke-width="1.5"/>'
                f'<text class="ak-label pill-t" x="{fmt(x)}" y="{fmt(y + 5)}" text-anchor="middle">{lp}</text>')
        inner = f'<g class="route">{route}</g>{pill}'
        if lp == 'R10':
            items.append(f'<a class="lb" href="#loop-r10" data-loop="{lp}" data-steps="{steps}" data-rel="{rel}" '
                         f'aria-label="{E(say)} Opens the loop." data-say="{E(say)} Opens the loop." style="--ak-w-case:8px">{inner}</a>')
        else:
            items.append(f'<g class="lb" role="button" data-select="{key("loop", lp)}" data-loop="{lp}" data-steps="{steps}" '
                         f'data-rel="{rel}" aria-label="{E(say)}" data-say="{E(say)}" style="--ak-w-case:8px">{inner}</g>')
    return items


