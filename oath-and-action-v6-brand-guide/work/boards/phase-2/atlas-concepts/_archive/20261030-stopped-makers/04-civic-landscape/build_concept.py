"""Atlas concept 04, Civic Landscape (Oath & Action Edition 06, Phase 2, October 30, 2026).

The system as one printed map: each V7 area a territory, each variable a named place, the connections between
areas as crossings and roads, and each loop a trail a reader can follow back to where it started.

Builds 20261030_Concept-04-Civic-Landscape.html beside this file from the model export
work/boards/phase-2/maps/20261028_Maps-Model-Data.json. Every label, sign, grade, delay, count and title on the page
is read from the model. Label widths are measured in Chromium with the locked Google Fonts (measure_labels.js) and
cached in label-metrics.json, so the label placer can keep every label clear of every other.

Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/04-civic-landscape/build_concept.py
"""
import html
import importlib.util
import json
import math
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

M = acc.load_model()
P = acc.PALETTE
NP, CH, RED, PR, ST, VG, WH, DS = (P['newsprint'], P['charcoal'], P['pillar_red'], P['prussian'], P['stone'],
                                    P['verdigris'], P['white'], P['deep_stone'])
MINUS = '−'
e = html.escape
N, L, LOOPS, REF = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
AREA_OF = {}
for _a in M['areas']:
    for _n in _a['nodes']:
        AREA_OF[_n] = _a['id']
COUNTS = M['generated']['counts']
SNAP_DATE = 'October 15, 2026'
assert M['generated']['snapshot'] == '2026-10-15'
OUT = HERE / '20261030_Concept-04-Civic-Landscape.html'

DEG = {k: 0 for k in N}
for _l in L.values():
    DEG[_l['from']] += 1
    DEG[_l['to']] += 1


def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


def texture(g):
    return acc.GRADES[g][2]


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def sign_attr(p):
    return p if p in ('+', '-') else 'none'


def verb(p):
    return acc.SIGN_WORDS[p]


def delay_words(d):
    return acc.DELAYS[d]


def kind_line(lp):
    return f'{lp["kind_word"]}, {lp["kind_gloss"]}'


def area_key(aid):
    return 'area-' + aid.lower()


def vkey(v):
    return 'var-' + v.lower()


def lkey(k):
    return 'link-' + k.lower()


def loopkey(k):
    return 'loop-' + k.lower()


def rkey(k):
    return 'reform-' + k.lower()


def lower_first(s):
    return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s


# ------------------------------------------------------------------ text measurement
STYLES = {
    # key: (CSS font, letter-spacing em, uppercase, line height)
    'town_s': ('400 13px Inter', 0, False, 16),          # Note: places with 1 to 3 connections
    'town_m': ('600 15px Inter', 0, False, 18),          # Map label: places with 4 or more
    'town_l': ('700 20px "Inter Tight"', -0.01, False, 22),   # Station label
    'terr': ('800 22px "Inter Tight"', -0.02, False, 26),     # Panel head: territory names
    'letter': ('800 40px "Inter Tight"', -0.03, False, 40),   # Figure: the area letter
    'eyebrow': ('700 13px Inter', 0.06, True, 18),
    'box': ('700 14px Inter', 0, False, 14),             # ID chip code style: counts in boxes
    'legend': ('500 13px Inter', 0, False, 18),
    'caption': ('400 14px Inter', 0, False, 20),
    'ptext': ('400 15px Inter', 0, False, 23),
    'chipk': ('600 13px Inter', 0.06, True, 13),
    'chipc': ('700 13px Inter', 0, False, 13),
}
_METRICS = HERE / 'label-metrics.json'
_cache = json.loads(_METRICS.read_text()) if _METRICS.exists() else {'widths': {}, 'fonts': []}
_want = {}


def _mk(style, text):
    return f'{style}|{text}'


def width(style, text):
    k = _mk(style, text)
    if k in _cache['widths']:
        return _cache['widths'][k]
    _want[k] = (style, text)
    f, ls, up, lh = STYLES[style]
    px = float(re.search(r'(\d+)px', f).group(1))
    return len(text) * px * 0.56   # rough until measured


def measure_pending():
    """Measure every string the build asked for and that the cache lacks. Returns True when new widths arrived."""
    if not _want:
        return False
    reqs = []
    for k, (style, text) in _want.items():
        f, ls, up, lh = STYLES[style]
        reqs.append({'k': k, 't': text, 'f': f, 'ls': ls, 'up': up})
    tmp = HERE / '.measure-requests.json'
    tmp.write_text(json.dumps(reqs))
    out = HERE / '.measure-out.json'
    subprocess.run(['node', str(HERE / 'measure_labels.js'), str(tmp), str(out)], check=True, cwd=str(HERE))
    res = json.loads(out.read_text())
    tmp.unlink()
    out.unlink()
    _cache['widths'].update(res['widths'])
    _cache['fonts'] = res['fonts']
    _METRICS.write_text(json.dumps(_cache, indent=0, sort_keys=True))
    _want.clear()
    return True


def wrap(style, text, maxw):
    """Greedy wrap by measured line widths. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if cur and width(style, trial) > maxw:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def block_w(style, lines):
    return max(width(style, ln) for ln in lines)


# ------------------------------------------------------------------ geometry
def poly_d(pts, close=True):
    s = 'M' + ' L'.join(f'{x:g} {y:g}' for x, y in pts)
    return s + (' Z' if close else '')


def signed_area(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) / 2


def clockwise(pts):
    return pts if signed_area(pts) > 0 else list(reversed(pts))   # y down: positive area is clockwise on screen


def outline_and_borders(polys):
    """Union outline(s) and shared borders of territory polygons that share vertices exactly."""
    edges = []
    for pts in polys:
        pts = clockwise(pts)
        for i in range(len(pts)):
            edges.append((tuple(pts[i]), tuple(pts[(i + 1) % len(pts)])))
    es = set(edges)
    inner = [(a, b) for a, b in edges if (b, a) in es]
    outer = [(a, b) for a, b in edges if (b, a) not in es]
    nxt = {}
    for a, b in outer:
        nxt[a] = b
    loops, seen = [], set()
    for a, _ in outer:
        if a in seen:
            continue
        loop, p = [], a
        while p not in seen:
            seen.add(p)
            loop.append(p)
            p = nxt[p]
        loops.append(loop)
    borders, done = [], set()
    for a, b in inner:
        if (b, a) in done:
            continue
        done.add((a, b))
        borders.append((a, b))
    return loops, borders


def point_in_poly(x, y, pts):
    inside = False
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                inside = not inside
    return inside


def rect_in_poly(r, pts, pad=3):
    x0, y0, x1, y1 = r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad
    for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1), ((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1), (x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)):
        if not point_in_poly(x, y, pts):
            return False
    for x, y in pts:
        if x0 < x < x1 and y0 < y < y1:
            return False
    return True


def rects_hit(a, b, pad=0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


class Arc:
    """A step drawn as a circular arc from p0 to p1. sag > 0 bows to the left of travel; 0 is straight."""

    def __init__(self, p0, p1, sag=0.0):
        self.p0, self.p1, self.sag = p0, p1, sag
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        self.c = math.hypot(dx, dy)
        if abs(sag) < 0.5:
            self.straight = True
            self.len = self.c
            return
        self.straight = False
        s = abs(sag)
        r = (self.c ** 2 / 4 + s ** 2) / (2 * s)
        self.r = r
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        nx, ny = dy / self.c, -dx / self.c        # left normal on screen (y down)
        side = 1 if sag > 0 else -1
        d = r - s
        self.cx, self.cy = mx - side * nx * d, my - side * ny * d
        apex = (mx + side * nx * s, my + side * ny * s)
        self.a0 = math.atan2(p0[1] - self.cy, p0[0] - self.cx)
        minor = 2 * math.asin(min(1, self.c / (2 * r)))
        tabs = minor if s <= r else 2 * math.pi - minor
        best = None
        for th in (tabs, -tabs):
            am = self.a0 + th / 2
            dd = math.hypot(self.cx + r * math.cos(am) - apex[0], self.cy + r * math.sin(am) - apex[1])
            if best is None or dd < best[0]:
                best = (dd, th)
        self.theta = best[1]
        self.len = abs(self.theta) * r

    def at(self, t):
        if self.straight:
            return (self.p0[0] + (self.p1[0] - self.p0[0]) * t, self.p0[1] + (self.p1[1] - self.p0[1]) * t)
        a = self.a0 + self.theta * t
        return (self.cx + self.r * math.cos(a), self.cy + self.r * math.sin(a))

    def tangent(self, t):
        if self.straight:
            return ((self.p1[0] - self.p0[0]) / self.c, (self.p1[1] - self.p0[1]) / self.c)
        a = self.a0 + self.theta * t
        sgn = 1 if self.theta > 0 else -1
        return (-math.sin(a) * sgn, math.cos(a) * sgn)

    def t_of(self, dist):
        return max(0.0, min(1.0, dist / self.len)) if self.len else 0.0

    def d(self, t0, t1):
        a, b = self.at(t0), self.at(t1)
        if self.straight:
            return f'M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}'
        sweep = 1 if self.theta > 0 else 0
        large = 1 if abs(self.theta * (t1 - t0)) > math.pi else 0
        return f'M{a[0]:.2f} {a[1]:.2f}A{self.r:.2f} {self.r:.2f} 0 {large} {sweep} {b[0]:.2f} {b[1]:.2f}'


# ------------------------------------------------------------------ the coded line (design frame memo, section 3)
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


def tag_shape(cx, cy, ang, sign, w, cls='ak-fill'):
    """The pointing tag: a solid five-sided tag pointing the way the step runs, the sign upright inside, in the ground."""
    a, p, h, sl, sb = TAG[w]
    Lt = a + p
    pts = [(-Lt / 2, -h / 2), (-Lt / 2 + a, -h / 2), (Lt / 2, 0), (-Lt / 2 + a, h / 2), (-Lt / 2, h / 2)]
    ca, sa = math.cos(ang), math.sin(ang)
    P2 = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
    bx, by = cx + (-Lt / 2 + a / 2) * ca, cy + (-Lt / 2 + a / 2) * sa
    poly = ' '.join(f'{x:.2f},{y:.2f}' for x, y in P2)
    s = f'<polygon class="{cls} tagb" points="{poly}"/>'
    s += f'<rect class="glyph" x="{bx - sl / 2:.2f}" y="{by - sb / 2:.2f}" width="{sl}" height="{sb}"/>'
    if sign == '+':
        s += f'<rect class="glyph" x="{bx - sb / 2:.2f}" y="{by - sl / 2:.2f}" width="{sb}" height="{sl}"/>'
    return s


def arrowhead(tip, tan, w):
    al, ab = ARROW[w]
    bx, by = tip[0] - tan[0] * al, tip[1] - tan[1] * al
    nx, ny = -tan[1], tan[0]
    pts = [(bx + nx * ab / 2, by + ny * ab / 2), tip, (bx - nx * ab / 2, by - ny * ab / 2)]
    return '<polygon class="ak-fill head" points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts) + '"/>'


def ticks(arc, t_start, count, w):
    out = ''
    half = w / 2 + 4
    for i in range(count):
        t = arc.t_of(arc.len * t_start + 12 + i * 5)
        x, y = arc.at(t)
        tx, ty = arc.tangent(t)
        nx, ny = -ty, tx
        out += (f'<line class="ak-mark tick" x1="{x + nx * half:.2f}" y1="{y + ny * half:.2f}" x2="{x - nx * half:.2f}" '
                f'y2="{y - ny * half:.2f}" stroke-width="2"/>')
    return out


def coded_step(arc, w, tex, sign, gap0, gap1, with_tag=True, tag_at=0.5, with_ticks=0, sketch=False, tag_end=False):
    """One version of a step at weight w: case, mark, arrowhead (or end tag), sign tag and delay ticks."""
    al, ab = ARROW[w]
    L_ = arc.len
    t_tail = arc.t_of(gap0)
    if tag_end:
        a, p, h, sl, sb = TAG[w]
        tip_d = L_ - gap1
        t_tip = arc.t_of(tip_d)
        tan = arc.tangent(t_tip)
        tip = arc.at(t_tip)
        cxy = (tip[0] - tan[0] * (a + p) / 2, tip[1] - tan[1] * (a + p) / 2)
        base_d = tip_d - (a + p)
    else:
        tip_d = L_ - gap1
        base_d = tip_d - al
    inset0 = w / 2 if tex == 'dotted' else 0
    inset1 = 1.5 * w if tex == 'dotted' else 0
    run = base_d - gap0 - inset0 - inset1
    da, cap = fitted(tex, w, max(run, 1))
    d = arc.d(arc.t_of(gap0 + inset0), arc.t_of(base_d - inset1))
    dash = f' stroke-dasharray="{da}"' if da else ''
    out = ''
    if sketch:
        out += f'<path class="ak-case" d="{d}" fill="none"/>'
        out += f'<path class="ak-mark rail" d="{d}" fill="none" stroke-width="{w + 2}"/>'
        out += f'<path class="gap" d="{d}" fill="none" stroke-width="{w}"/>'
    else:
        out += f'<path class="ak-case" d="{d}" fill="none" stroke-linecap="{cap}"{dash}/>'
        out += f'<path class="ak-mark" d="{d}" fill="none" stroke-width="{w}" stroke-linecap="{cap}"{dash}/>'
    if tag_end:
        tan = arc.tangent(arc.t_of(tip_d))
        out += tag_shape(cxy[0], cxy[1], math.atan2(tan[1], tan[0]), sign, w)
    else:
        tt = arc.t_of(tip_d)
        out += arrowhead(arc.at(tt), arc.tangent(tt), w)
        if with_tag:
            tm = arc.t_of(gap0 + (base_d - gap0) * tag_at)
            x, y = arc.at(tm)
            tx, ty = arc.tangent(tm)
            out += tag_shape(x, y, math.atan2(ty, tx), sign, w)
    if with_ticks:
        out += ticks(arc, arc.t_of(gap0) if False else gap0 / max(L_, 1), with_ticks, w)
    return out


def hit_path(arc, gap0, gap1):
    return f'<path class="ak-hit" d="{arc.d(arc.t_of(gap0), arc.t_of(arc.len - gap1))}"/>'


# ------------------------------------------------------------------ the overview map: geography
# The plan keeps V7's ring order (A, B, C across the top; E and D below), so each variable sits near its slot in the
# shared loop-route plan. Areas that exchange the most connections share a border; the economy and technology
# layers are islands of their own, and the outside drivers lie on the far shore across the strait.
OW, OH = 1312, 620
FAR = [(0, 0), (952, 0), (952, 24), (928, 48), (864, 48), (848, 64), (704, 64), (688, 48), (568, 48), (552, 64),
       (408, 64), (392, 48), (232, 48), (216, 64), (56, 64), (40, 48), (0, 48)]
TERR = {
    'A': [(320, 144), (344, 120), (472, 120), (488, 104), (520, 104), (520, 216), (536, 232), (536, 360), (520, 376),
          (520, 408), (504, 424), (320, 424), (320, 312), (304, 296), (304, 232), (320, 216)],
    'B': [(520, 104), (632, 104), (648, 120), (704, 120), (720, 104), (760, 104), (760, 208), (744, 224), (744, 360),
          (672, 360), (656, 376), (584, 376), (520, 376), (536, 360), (536, 232), (520, 216)],
    'C': [(760, 104), (880, 104), (896, 120), (936, 120), (960, 144), (960, 248), (976, 264), (976, 336), (960, 352),
          (960, 376), (864, 376), (848, 360), (744, 360), (744, 224), (760, 208)],
    'D': [(584, 376), (656, 376), (672, 360), (744, 360), (848, 360), (864, 376), (960, 376), (960, 480), (944, 496),
          (944, 560), (920, 584), (728, 584), (712, 600), (600, 600), (600, 496), (584, 480)],
    'E': [(320, 424), (504, 424), (520, 408), (520, 376), (584, 376), (584, 480), (600, 496), (600, 600), (448, 600),
          (432, 584), (344, 584), (320, 560)],
    'money': [(16, 144), (48, 112), (224, 112), (240, 128), (264, 128), (264, 264), (200, 264), (184, 280), (16, 280)],
    'household': [(16, 280), (184, 280), (200, 264), (264, 264), (264, 312), (280, 328), (280, 400), (264, 416),
                  (264, 440), (104, 440), (88, 456), (16, 456)],
    'production': [(16, 456), (88, 456), (104, 440), (264, 440), (264, 568), (240, 592), (40, 592), (16, 568)],
    'TC': [(1008, 352), (1032, 328), (1272, 328), (1296, 352), (1296, 568), (1272, 592), (1136, 592), (1120, 576),
           (1024, 576), (1000, 552), (1000, 456), (984, 440), (984, 376)],
}
ISLANDS = {'core': ['A', 'B', 'C', 'D', 'E'], 'economy': ['money', 'household', 'production'], 'technology': ['TC']}
# Territory names: top-left of the name block and the lines it breaks into
TNAME = {
    'A': (336, 152, ['Economic', 'structure']),
    'B': (552, 152, ['Political', 'inputs']),
    'C': (776, 152, ['Electoral', 'competition']),
    'D': (616, 408, ['Governing', 'institutions']),
    'E': (336, 456, ['Legitimacy']),
    'money': (32, 152, ['Credit, trade', 'and environment']),
    'household': (32, 304, ['Household budgets', 'and wealth']),
    'production': (32, 480, ['Production', 'and income']),
    'TC': (1016, 368, ['Technology mechanisms']),
    'X': (16, 0, []),
}
# Places: position and the label sides to try, in order
TOWN = {
    'X5': (32, 24, 'r'), 'X3': (232, 24, 'r'), 'X4': (448, 24, 'r'), 'X1': (608, 24, 'r'), 'X2': (792, 24, 'r'),
    'A1': (344, 232, 'r'), 'A3': (440, 232, 'rb'), 'A5': (344, 288, 'r'), 'A2': (440, 296, 'rb'), 'A6': (344, 352, 'r'),
    'A4': (440, 376, 'rl'),
    'B6': (568, 232, 'r'), 'B4': (664, 232, 'rb'), 'B3': (568, 288, 'r'), 'B2': (664, 304, 'r'), 'B1': (568, 344, 'r'),
    'B5': (672, 344, 'rl'),
    'C2': (800, 224, 'r'), 'C1': (936, 272, 'l'), 'C3': (800, 304, 'r'), 'C4': (920, 344, 'l'), 'C5': (792, 344, 'b'),
    'D5': (632, 480, 'r'), 'D2': (760, 456, 'r'), 'D3': (872, 456, 'r'), 'D4': (632, 552, 'r'), 'D1': (760, 528, 'r'),
    'D6': (872, 528, 'r'), 'D7': (888, 408, 'l'),
    'E2': (456, 488, 'r'), 'E1': (456, 552, 'r'),
    'EC11': (40, 208, 'r'), 'EC10': (152, 208, 'r'), 'EC5': (40, 240, 'r'), 'EC12': (152, 240, 'r'),
    'EC9': (40, 360, 'r'), 'EC6': (152, 360, 'r'), 'EC7': (40, 408, 'r'), 'EC8': (152, 408, 'r'),
    'EC3': (40, 528, 'r'), 'EC4': (152, 528, 'r'), 'EC1': (40, 568, 'r'), 'EC2': (152, 568, 'r'),
    'TC1': (1016, 416, 'r'), 'TC2': (1160, 416, 'r'), 'TC3': (1016, 464, 'r'), 'TC4': (1160, 464, 'r'),
    'TC5': (1016, 512, 'r'), 'TC6': (1160, 512, 'r'), 'TC7': (1016, 552, 'r'), 'TC8': (1160, 552, 'r'),
}


def town_class(v):
    d = DEG[v]
    return 1 if d <= 3 else 2 if d <= 6 else 3 if d <= 9 else 4


SYM_R = {1: 4.5, 2: 6, 3: 8, 4: 10.5}          # outer radius of each place symbol, stroke included
CLASS_WORDS = {1: '1 to 3', 2: '4 to 6', 3: '7 to 9', 4: '10 or more'}


def town_style(v):
    return 'town_s' if DEG[v] <= 3 else 'town_m'


def town_symbol(x, y, cls, extra=''):
    """Place symbols scale with the connections that touch a variable: a dot, a larger dot, a ring, a double ring."""
    if cls == 1:
        s = f'<circle class="ak-mark sym" cx="{x}" cy="{y}" r="3.5" stroke-width="2"/>'
    elif cls == 2:
        s = f'<circle class="ak-mark sym" cx="{x}" cy="{y}" r="5" stroke-width="2"/>'
    elif cls == 3:
        s = (f'<circle class="ak-mark symo" cx="{x}" cy="{y}" r="7" stroke-width="2"/>'
             f'<circle class="symd" cx="{x}" cy="{y}" r="3"/>')
    else:
        s = (f'<circle class="ak-mark symo" cx="{x}" cy="{y}" r="9.5" stroke-width="2"/>'
             f'<circle class="symo2" cx="{x}" cy="{y}" r="5" stroke-width="2"/>'
             f'<circle class="symd" cx="{x}" cy="{y}" r="2"/>')
    return f'<circle class="selring" cx="{x}" cy="{y}" r="{SYM_R[cls] + 4}"/>' + s


def splits(style, text, n):
    words = text.split()
    if n == 1:
        return [[text]]
    if len(words) < n:
        return []
    out = []
    if n == 2:
        for i in range(1, len(words)):
            out.append([' '.join(words[:i]), ' '.join(words[i:])])
    elif n == 3:
        for i in range(1, len(words) - 1):
            for j in range(i + 1, len(words)):
                out.append([' '.join(words[:i]), ' '.join(words[i:j]), ' '.join(words[j:])])
    out.sort(key=lambda ls: block_w(style, ls))
    return out[:2]


class Placer:
    """Cartographic label placement: try each side and line count in order, keep the first that stays inside its
    territory and clear of every placed label, symbol, name and box."""

    def __init__(self):
        self.obst = []
        self.warn = []

    def add(self, r, tag=''):
        self.obst.append((r, tag))

    def free(self, r, pad=3, ignore=()):
        return not any(rects_hit(r, o, pad) for o, t in self.obst if t not in ignore)

    def place(self, x, y, rad, style, text, sides, region, maxw=178, ignore=(), key=''):
        f, ls, up, lh = STYLES[style]
        fs = float(re.search(r'(\d+)px', f).group(1))
        best = None
        order = list(sides) + [s for s in 'rlbt' if s not in sides]
        for side in order:
            for n in (1, 2, 3):
                for lines in splits(style, text, n):
                    w = block_w(style, lines)
                    if w > (maxw if side in 'rl' else 140) and n < 3:
                        continue
                    h = n * lh
                    if side == 'r':
                        x0, y0 = x + rad + 5, y - h / 2
                    elif side == 'l':
                        x0, y0 = x - rad - 5 - w, y - h / 2
                    elif side == 'b':
                        x0, y0 = x - w / 2, y + rad + 2
                    else:
                        x0, y0 = x - w / 2, y - rad - 2 - h
                    r = (x0, y0 + 1, x0 + w, y0 + h - 1)
                    ok_region = region is None or rect_in_poly(r, region, pad=3)
                    ok = ok_region and self.free(r, ignore=ignore)
                    cand = (side, lines, x0, y0, r, w, h)
                    if ok:
                        best = cand
                        break
                    if best is None and ok_region:
                        best = ('?',) + cand[1:]
                if best and best[0] != '?':
                    break
            if best and best[0] != '?':
                break
        if best is None:
            best = ('?', [text], x + rad + 5, y - lh / 2, (x + rad + 5, y - lh / 2, x + rad + 5 + width(style, text), y + lh / 2),
                    width(style, text), lh)
        if best[0] == '?':
            self.warn.append(f'label {key} {text!r} could not be placed clear')
        side, lines, x0, y0, r, w, h = best
        self.add(r, 'label')
        anchor = 'start'
        tx = x0
        if side in 'bt':
            anchor, tx = 'middle', x0 + w / 2
        base = [y0 + i * lh + lh / 2 + fs * 0.35 for i in range(len(lines))]
        return {'lines': lines, 'x': tx, 'base': base, 'anchor': anchor, 'rect': r, 'side': side}


def text_lines(lab, cls, attrs=''):
    tsp = ''.join(f'<tspan x="{lab["x"]:.1f}" y="{b:.1f}">{e(t)}</tspan>' for t, b in zip(lab['lines'], lab['base']))
    return f'<text class="{cls}" text-anchor="{lab["anchor"]}"{attrs}>{tsp}</text>'
