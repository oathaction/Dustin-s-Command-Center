"""Concept 06, Loop Lines with the Field Guide. Atlas concepts, Phase 2, October 30, 2026.

Builds 20261030_Concept-06-Loop-Lines.html beside this file:
    python3 -I work/boards/phase-2/atlas-concepts/06-loop-lines/build_concept.py

Reads the model export (work/boards/phase-2/maps/20261028_Maps-Model-Data.json) for every label, sign, grade,
delay, count and title, and the October 28 Loop Lines network (work/boards/phase-2/maps-r2/c/
20261028_Loop-Lines-Network-Data.json) for station cells, corridor routes and track order only. The drawing code
is adapted from the October 28 scripts (maps_r2_c_geom.py, maps_r2_c_draw.py, maps_r2_c_views.py) and the shared
specimen (atlas_specimen_build.py). The shared kit (atlas-kit.js, atlas-kit.css) and the identity masters are
inlined unchanged.
"""
import html
import importlib.util
import json
import math
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OUT = HERE / '20261030_Concept-06-Loop-Lines.html'
SHARED = ROOT / 'work/boards/phase-2/atlas-concepts/shared'
_spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acc)

M = acc.load_model()
NET = json.loads((ROOT / 'work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Network-Data.json').read_text())
N, L, LO, RF = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
GROUPS = {g['id']: g for g in M['groups']}
GLOSS = M['glossary']
COUNTS = M['generated']['counts']
E = lambda s: html.escape(str(s), quote=True)

P = acc.PALETTE
NP, CH, RED, PR, ST, VG, WH, DS = (P['newsprint'], P['charcoal'], P['pillar_red'], P['prussian'], P['stone'],
                                    P['verdigris'], P['white'], P['deep_stone'])
# Proposed tint (brief section 10): Prussian mixed 16 percent toward Newsprint in OKLab, the October 28 field step.
# One job: the five area fields on the Prussian poster. White text on it 9.15:1, Newsprint 6.49:1.
FIELD_PR = '#39476D'
MINUS = '−'
SNAP = 'October 15, 2026'
assert M['generated']['snapshot'] == '2026-10-15'

NUMBERED = [k for k in M['loop_order'] if not LO[k]['conceptual']]
SKETCHED = [k for k in M['loop_order'] if LO[k]['conceptual']]

# ------------------------------------------------------------------ font metrics
# Advance widths in em, measured in Chromium with the Google Fonts files the page loads (canvas measureText).
FW_CHARS = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~−’‘“”·é×'
_FW = {
    ('Inter', 400): '281 288 466 633 642 982 644 300 365 365 501 662 288 460 288 360 631 407 610 618 646 593 620 566 619 620 288 302 662 662 662 511 966 690 654 730 722 601 590 746 743 269 571 672 565 903 753 765 639 765 644 642 646 744 690 985 682 679 629 365 360 365 471 456 323 562 612 571 612 583 370 613 591 242 242 549 242 876 591 600 612 612 376 528 327 591 562 818 546 562 552 426 333 426 662 662 261 261 440 440 288 583 662',
    ('Inter', 500): '267 304 494 639 646 993 653 313 369 369 521 667 303 462 303 370 646 415 616 627 656 603 630 571 629 630 303 315 667 667 667 527 982 709 657 733 722 603 589 748 745 272 575 688 565 913 756 767 642 769 648 646 653 740 709 1003 701 696 641 369 370 369 477 463 337 568 618 577 618 587 379 620 602 252 252 559 252 888 602 604 618 618 387 539 340 602 575 829 557 575 559 440 346 440 667 667 277 277 474 471 303 587 667',
    ('Inter', 600): '252 321 523 644 650 1004 663 326 373 373 540 673 319 465 319 379 660 423 623 636 666 612 640 576 640 640 319 329 673 673 673 543 999 728 659 737 722 605 588 749 746 277 580 703 565 922 759 769 645 773 652 650 660 736 728 1020 720 713 652 373 379 373 481 469 351 574 624 583 624 591 389 625 612 262 262 569 262 900 612 609 624 624 397 549 353 612 587 839 569 588 566 455 359 455 673 673 294 294 507 501 319 591 673',
    ('Inter', 700): '237 338 552 649 655 1016 672 339 377 377 559 679 334 468 334 388 674 431 630 646 676 622 649 582 651 649 334 343 679 679 679 560 1016 747 662 740 722 607 587 750 747 281 584 719 565 932 762 771 648 777 657 655 667 732 747 1038 738 731 664 377 388 377 487 476 365 581 630 588 630 596 398 632 623 271 271 580 271 913 623 613 630 630 407 560 366 623 600 850 580 602 573 469 372 469 679 679 311 311 540 532 334 596 679',
    ('Inter Tight', 700): '199 313 527 617 622 827 640 309 344 344 532 647 320 436 305 357 655 399 597 627 645 614 630 551 631 630 305 313 647 647 647 530 998 714 628 719 694 580 552 728 713 247 537 657 535 883 702 749 615 750 624 622 636 697 714 1003 682 692 634 344 357 344 455 444 432 551 598 555 598 563 355 600 594 240 240 549 240 881 591 581 598 598 376 529 355 589 553 817 541 553 539 439 341 439 647 647 322 322 557 548 305 563 647',
    ('Inter Tight', 800): '188 334 564 628 632 847 656 329 354 354 559 658 343 443 327 373 681 414 610 639 662 633 650 563 653 650 327 334 658 658 658 554 1034 743 636 732 702 589 557 738 720 257 551 674 542 896 701 760 624 762 634 632 649 697 743 1035 710 717 652 354 373 354 466 457 447 562 610 568 610 573 369 612 610 256 256 566 256 900 608 591 610 610 393 547 369 607 567 834 557 567 554 460 361 460 658 658 347 347 600 588 327 573 658',
}
FW = {k: [int(x) / 1000 for x in v.split()] for k, v in _FW.items()}


def tw(s, size, weight=400, fam='Inter', track=0.0):
    """Rendered width of s in px."""
    tbl = FW[(fam, weight)]
    tot = sum(tbl[FW_CHARS.index(c)] if c in FW_CHARS else 0.6 for c in s)
    return tot * size + track * size * max(0, len(s) - 1)


def wrap(s, width, size, weight=400, fam='Inter'):
    words, lines, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if not cur or tw(t, size, weight, fam) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap2(s, size, weight=600, fam='Inter'):
    """Two balanced lines."""
    words = s.split()
    if len(words) < 2:
        return [s]
    best = min(((' '.join(words[:i]), ' '.join(words[i:])) for i in range(1, len(words))),
               key=lambda p: max(tw(p[0], size, weight, fam), tw(p[1], size, weight, fam)))
    return list(best)


# ------------------------------------------------------------------ model words
def low(s):
    return s[0].lower() + s[1:] if len(s) > 1 and s[1].islower() else s


def cap(s):
    return s[0].upper() + s[1:] if s else s


def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


TEXTURE = {g: acc.GRADES[g][2] for g in acc.GRADES}   # solid, dashed, dash-dot, dotted
DELAY = acc.DELAYS
TICKS = {'S': 1, 'M': 2, 'L': 3}


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


def verb(p):
    return {'+': 'raises', '-': 'lowers'}.get(p, 'decides')


def same_way(p):
    return {'+': 'the two move the same way', '-': 'the two move opposite ways'}.get(p, 'no direction')


def kind_line(lid):
    o = LO[lid]
    return f"{o['kind_word']}, {o['kind_gloss']}"


def read_aloud(lid):
    """The loop's read-aloud line, built from its signs: more or less at each station, and back to the start."""
    o = LO[lid]
    st = o['stations']
    d, parts = 1, []
    for i, s in enumerate(st):
        parts.append(('More ' if d > 0 else 'less ') if i == 0 else ('more ' if d > 0 else 'less '))
        parts[-1] += low(s['label'])
        d *= 1 if s['out_sign'] == '+' else -1
    back = f"and back to {'more' if d > 0 else 'less'} {low(st[0]['label'])}"
    return ', '.join(parts) + ', ' + back + '.'


def ends_where(lid):
    """+1 when a rise at the first station comes back as a rise (feeds itself), -1 when it comes back as a fall."""
    d = 1
    for s in LO[lid]['stations']:
        d *= 1 if s['out_sign'] == '+' else -1
    return d


for _k in M['loop_order']:
    assert (ends_where(_k) > 0) == (LO[_k]['type'] == 'R'), _k


def weakest_words(lid):
    """The weakest step in words: V7's named step, or what the ranks say when V7 names none."""
    o = LO[lid]
    if o['conceptual']:
        return None
    if o['weakest']:
        ws = o['weakest']
        g = L[ws[0]]['evidence']
        return ws, grade_word(g)
    ranks = {s['rank'] for s in o['steps']}
    grades = sorted({s['evidence'] for s in o['steps']}, key=lambda g: list(acc.GRADES).index(g))
    if len(grades) == 1:
        return [], f"none named; every step is {low(grade_word(grades[0]))}"
    return [], 'none named; V7 ranks its steps equal'


def first_sentence(s):
    m = re.match(r'(.+?[.!?])(\s|$)', s)
    return m.group(1) if m else s


def chip(kind, code, cls='compact'):
    return f'<span class="chip {cls}"><span class="k">{E(kind)}</span><span class="c">{E(code)}</span></span>'


def date_words(iso):
    if not iso:
        return 'no check date in V7'
    y, m_, d = iso.split('-')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return f'{months[int(m_) - 1]} {int(d)}, {y}'


# ------------------------------------------------------------------ the October 28 network, read from its data file
ST_CELL = {k: (v['col'], v['row']) for k, v in NET['stations'].items()}
STATIONS = sorted(ST_CELL, key=lambda s: M['order'].index(s))
CORR = []
for c in NET['corridors']:
    CORR.append({'a': c['stations'][0], 'b': c['stations'][1], 'cells': [tuple(x) for x in c['route_cells']],
                 'tracks': [dict(t, unit=t['offset_px'] / NET['pitch_px']) for t in c['tracks']]})
_tracks = {(t['link'], t['loop']) for c in CORR for t in c['tracks']}
assert _tracks == {(s['id'], k) for k in NUMBERED for s in LO[k]['steps']}, 'network and model disagree'
for _c in CORR:
    for _t in _c['tracks']:
        assert {L[_t['link']]['from'], L[_t['link']]['to']} == {_c['a'], _c['b']}
POSTER_LINKS = sorted({t['link'] for c in CORR for t in c['tracks']}, key=lambda k: (len(k), k))


def station_loops(sid):
    return [k for k in NUMBERED if any(s['code'] == sid for s in LO[k]['stations'])]


# label sides from the October 28 station table, with three changes for this poster's title and key zones
SIDE = {'E1': 'inside', 'B5': 'se', 'B3': 'w', 'A2': 'w', 'A4': 'w', 'A1': 'w', 'B1': 'ne', 'A6': 's', 'A5': 'ne',
        'D1': 'n', 'D2': 'n', 'D4': 's', 'D6': 's', 'B4': 'ne', 'B6': 'n', 'B2': 'n', 'C3': 'e', 'C5': 'n',
        'D5': 'nw', 'E2': 's', 'C2': 'sw', 'C1': 'sw', 'C4': 'e', 'D7': 'w', 'D3': 'e'}
WRAP = {'A4', 'A6', 'D1', 'D2', 'D4', 'D6', 'B4', 'D5', 'C2', 'C4', 'D7', 'D3'}
NUDGE = {'B2': (10, 0)}


# ------------------------------------------------------------------ geometry (adapted from maps_r2_c_geom.py)
def unit(dx, dy):
    ln = math.hypot(dx, dy)
    return (dx / ln, dy / ln) if ln else (0.0, 0.0)


def simplify(cells):
    out = [cells[0]]
    for i in range(1, len(cells) - 1):
        d0 = (cells[i][0] - cells[i - 1][0], cells[i][1] - cells[i - 1][1])
        d1 = (cells[i + 1][0] - cells[i][0], cells[i + 1][1] - cells[i][1])
        if d0[0] * d1[1] - d0[1] * d1[0] != 0 or d0[0] * d1[0] + d0[1] * d1[1] < 0:
            out.append(cells[i])
    out.append(cells[-1])
    return out


def offset_poly(pts, d):
    """Offset a polyline by d to the right of travel (screen coordinates), mitred at each bend."""
    if len(pts) == 2:
        u = unit(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
        n = (-u[1], u[0])
        return [(p[0] + n[0] * d, p[1] + n[1] * d) for p in pts]
    segs = []
    for i in range(len(pts) - 1):
        u = unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        n = (-u[1], u[0])
        segs.append(((pts[i][0] + n[0] * d, pts[i][1] + n[1] * d), (pts[i + 1][0] + n[0] * d, pts[i + 1][1] + n[1] * d), u))
    out = [segs[0][0]]
    for i in range(len(segs) - 1):
        (p0, p1, u0), (q0, q1, u1) = segs[i], segs[i + 1]
        den = u0[0] * u1[1] - u0[1] * u1[0]
        if abs(den) < 1e-9:
            out.append(p1)
            continue
        t = ((q0[0] - p0[0]) * u1[1] - (q0[1] - p0[1]) * u1[0]) / den
        out.append((p0[0] + u0[0] * t, p0[1] + u0[1] * t))
    out.append(segs[-1][1])
    return out


def rounded_path(pts, radius, offset=0.0):
    """SVG path through pts with every bend rounded; parallel tracks turn on concentric arcs."""
    if len(pts) == 2:
        return f'M{pts[0][0]:.2f} {pts[0][1]:.2f}L{pts[1][0]:.2f} {pts[1][1]:.2f}'
    d = [f'M{pts[0][0]:.2f} {pts[0][1]:.2f}']
    for i in range(1, len(pts) - 1):
        p0, v, p1 = pts[i - 1], pts[i], pts[i + 1]
        u0 = unit(v[0] - p0[0], v[1] - p0[1])
        u1 = unit(p1[0] - v[0], p1[1] - v[1])
        z = u0[0] * u1[1] - u0[1] * u1[0]
        theta = math.acos(max(-1.0, min(1.0, u0[0] * u1[0] + u0[1] * u1[1])))
        r = max(2.0, radius - (1 if z > 0 else -1) * offset)
        t = r * math.tan(theta / 2)
        lim = min(math.hypot(v[0] - p0[0], v[1] - p0[1]), math.hypot(p1[0] - v[0], p1[1] - v[1])) * 0.5
        if t > lim:
            t = lim
            r = t / math.tan(theta / 2) if theta > 1e-6 else r
        a = (v[0] - u0[0] * t, v[1] - u0[1] * t)
        b = (v[0] + u1[0] * t, v[1] + u1[1] * t)
        d.append(f'L{a[0]:.2f} {a[1]:.2f}A{r:.2f} {r:.2f} 0 0 {1 if z > 0 else 0} {b[0]:.2f} {b[1]:.2f}')
    d.append(f'L{pts[-1][0]:.2f} {pts[-1][1]:.2f}')
    return ''.join(d)


def plen(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


def point_at(pts, s):
    acc_ = 0.0
    for i in range(len(pts) - 1):
        ln = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        if acc_ + ln >= s and ln > 0:
            t = (s - acc_) / ln
            u = unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t), u
        acc_ += ln
    return pts[-1], unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])


def runs(pts):
    return [(pts[i], pts[i + 1], math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])) for i in range(len(pts) - 1)]


def signed_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def inset_poly(poly, d):
    sa = signed_area(poly)
    return offset_poly(poly + [poly[0], poly[1]], (1 if sa > 0 else -1) * d)[1:-1]


def inside(pt, poly):
    x, y = pt
    c = False
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def seg_box(p, q, b):
    """Liang-Barsky: does segment pq touch box b (x0, y0, x1, y1)?"""
    x0, y0, x1, y1 = b
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def box_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def convex_hit(pa, pb, pad):
    for poly in (pa, pb):
        for i in range(len(poly)):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % len(poly)]
            ax, ay = y1 - y0, x0 - x1
            ln = math.hypot(ax, ay)
            if ln < 1e-9:
                continue
            ax, ay = ax / ln, ay / ln
            a_ = [q[0] * ax + q[1] * ay for q in pa]
            b_ = [q[0] * ax + q[1] * ay for q in pb]
            if max(a_) + pad <= min(b_) or max(b_) + pad <= min(a_):
                return False
    return True


def box_poly(b):
    return [(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]


class Lay:
    """One placement of the network: grid cell, origin (E1), track pitch and corner radius, all in px."""

    def __init__(self, cell, ox, oy, pitch, radius):
        self.cell, self.ox, self.oy, self.pitch, self.radius = cell, ox, oy, pitch, radius

    def px(self, c):
        return (self.ox + c[0] * self.cell, self.oy + c[1] * self.cell)

    def st(self, sid):
        return self.px(ST_CELL[sid])

    def corridor(self, c):
        return [self.px(x) for x in simplify(c['cells'])]

    def track(self, c, t):
        """(points in travel order, offset to the right of travel) for one track."""
        base = self.corridor(c)
        off = t['unit'] * self.pitch
        pts = offset_poly(base, off)
        if L[t['link']]['from'] != c['a']:
            return list(reversed(pts)), -off
        return pts, off


# ------------------------------------------------------------------ line textures (shared specimen rules)
def pattern(texture, w):
    if texture == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if texture == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if texture == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def dash_attr(grade, w):
    arr, capstyle = pattern(TEXTURE[grade], w)
    cls = {'dashed': 'tx-dash', 'dash-dot': 'tx-dd', 'dotted': 'tx-dot'}.get(TEXTURE[grade], 'tx-solid')
    if arr is None:
        return f' class="ak-mark {cls}"', cls
    return f' class="ak-mark {cls}" stroke-dasharray="{" ".join(f"{x:g}" for x in arr)}" stroke-linecap="{capstyle}"', cls


def fitted(texture, w, length):
    """Scale the pattern so the line starts and ends on ink."""
    arr, capstyle = pattern(texture, w)
    if arr is None:
        return '', capstyle
    if texture == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.3f}', capstyle
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.3f}' for x in arr), capstyle


def link_attrs(lid):
    l = L[lid]
    return (f' data-link="{lid}" data-from="{l["from"]}" data-to="{l["to"]}" data-sign="{l["polarity"] or "none"}"'
            f' data-grade="{l["evidence"]}" data-delay="{l["delay"]}"')


# ------------------------------------------------------------------ marks
TAG3 = (15.0, 6.0)        # body and point length on 3 px lines (memo section 3: 17 by 21)


def tag_poly(p, u, h, body=15.0, point=6.0):
    """A pointing tag centered on p, pointing along u, h tall."""
    nx, ny = -u[1], u[0]
    half = (body + point) / 2
    back = (p[0] - u[0] * half, p[1] - u[1] * half)
    sh = (p[0] + u[0] * (half - point), p[1] + u[1] * (half - point))
    tip = (p[0] + u[0] * half, p[1] + u[1] * half)
    return [(back[0] + nx * h / 2, back[1] + ny * h / 2), (sh[0] + nx * h / 2, sh[1] + ny * h / 2), tip,
            (sh[0] - nx * h / 2, sh[1] - ny * h / 2), (back[0] - nx * h / 2, back[1] - ny * h / 2)]


def tag_svg(p, u, sign, h, fill, glyph, halo, body=15.0, point=6.0, bar=(9, 3), cls='tag'):
    poly = tag_poly(p, u, h, body, point)
    pts = ' '.join(f'{x:.2f},{y:.2f}' for x, y in poly)
    cx, cy = p[0] - u[0] * point / 2, p[1] - u[1] * point / 2
    sl, sb = bar
    s = (f'<polygon points="{pts}" fill="{fill}" stroke="{halo}" stroke-width="4" stroke-linejoin="round" paint-order="stroke"/>'
         f'<rect x="{cx - sl / 2:.2f}" y="{cy - sb / 2:.2f}" width="{sl}" height="{sb}" fill="{glyph}"/>')
    if sign == '+':
        s += f'<rect x="{cx - sb / 2:.2f}" y="{cy - sl / 2:.2f}" width="{sb}" height="{sl}" fill="{glyph}"/>'
    return f'<g class="{cls}" data-sign-mark="{E(sign)}">{s}</g>'


def ticks_svg(p, u, count, w, ink):
    """Delay ticks across the line, starting at p and stepping along u."""
    half = w / 2 + 4
    nx, ny = -u[1], u[0]
    out = []
    for i in range(count):
        c = (p[0] + u[0] * i * 5, p[1] + u[1] * i * 5)
        a = (c[0] + nx * half, c[1] + ny * half)
        b = (c[0] - nx * half, c[1] - ny * half)
        out.append(f'<path d="M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}" stroke="{ink}" stroke-width="2" fill="none"/>')
    return ''.join(out)


ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}


def arrow_svg(tip, u, w, cls='ak-head'):
    al, ab = ARROW[w]
    nx, ny = -u[1], u[0]
    b = (tip[0] - u[0] * al, tip[1] - u[1] * al)
    pts = [(b[0] + nx * ab / 2, b[1] + ny * ab / 2), tip, (b[0] - nx * ab / 2, b[1] - ny * ab / 2)]
    return f'<path class="{cls}" d="M{pts[0][0]:.2f} {pts[0][1]:.2f}L{pts[1][0]:.2f} {pts[1][1]:.2f}L{pts[2][0]:.2f} {pts[2][1]:.2f}Z"/>'


def text_el(x, y, s, cls, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}"{a}{extra}>{E(s)}</text>'


def lines_el(x, y, lines, cls, lh, anchor='start', extra=''):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    ts = ''.join(f'<tspan x="{x:.1f}" y="{y + i * lh:.1f}">{E(t)}</tspan>' for i, t in enumerate(lines))
    return f'<text class="{cls}"{a}{extra}>{ts}</text>'


# ================================================================== the poster (overview, Prussian)
PW = 1312                       # the poster spans the 12 columns at 1440
PCELL, PPITCH, PLW, PRAD = 32, 8, 3, 12
POX, POY = 473, 462
RING_R, CAP_W, CAP_H = 11, 38, 22

# District fields on the station grid (cells). Adapted from the October 28 field table, with the top-left corner
# (the title) and the top-right corner (how to read it) left as open ground. The notches run parallel to the R4b arch.
FIELDS = [
    ('A', 'main', [(-13.4, -6.85), (-8.5, -6.85), (-8.5, -4.5), (-2, -4.5), (-2, 12.2), (-13.4, 12.2)], False),
    ('B', 'main', [(-8.5, -6.85), (0.25, -6.85), (4.3, -10.9), (10.75, -10.9), (18.65, -3.0), (18.65, -0.5),
                   (11.5, -0.5), (11.5, -4.5), (-8.5, -4.5)], False),
    ('B', 'b1', [(-2, 4.5), (2.5, 4.5), (2.5, 12.2), (-2, 12.2)], False),
    ('E', 'main', [(-2, -4.5), (1.5, -4.5), (1.5, 4.5), (-2, 4.5)], False),
    ('C', 'main', [(8.5, -0.5), (24.4, -0.5), (24.4, 7.5), (11.5, 7.5), (11.5, 2.5), (8.5, 2.5)], False),
    ('D', 'main', [(1.5, -4.5), (11.5, -4.5), (11.5, -0.5), (8.5, -0.5), (8.5, 2.5), (11.5, 2.5), (11.5, 7.5),
                   (24.4, 7.5), (24.4, 12.2), (2.5, 12.2), (2.5, 4.5), (1.5, 4.5)], False),
    ('E', 'e2', [(4, 6), (9.5, 6), (9.5, 10.5), (4.9, 10.5), (4, 9.6)], True),
]
DNAME = {'A': (-12.9, -2.35, True), 'B': (7.2, -9.35, False), 'C': (18.9, 1.55, True), 'D': (18.9, 11.45, True),
         'E': (4.75, 10.05, False)}
PATCH_LETTER = {('B', 'b1'): (-1.55, 11.65), ('E', 'main'): (-1.5, -2.95)}
FIELD_GAP = 8.0


def field_polys(lay, fields=FIELDS, gap=FIELD_GAP):
    out = []
    for d, part, cells, island in fields:
        pts = [lay.px(c) for c in cells]
        out.append({'district': d, 'part': part, 'island': island, 'raw': pts, 'poly': inset_poly(pts, gap / 2)})
    return out


def field_at(fpolys, pt):
    hit = None
    for f in fpolys:
        if inside(pt, f['poly']):
            hit = f
    return hit


def fields_svg(fpolys, fill, ground, edge=None):
    out = []
    for f in sorted(fpolys, key=lambda f: f['island']):
        if f['island']:
            moat = inset_poly(f['raw'], -FIELD_GAP / 2)
            out.append(f'<path d="M{"L".join(f"{x:.1f} {y:.1f}" for x, y in moat)}Z" fill="{ground}"/>')
        d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in f['poly']) + 'Z'
        st = f' stroke="{edge}" stroke-width="1"' if edge else ''
        out.append(f'<path class="field" data-district="{f["district"]}" data-part="{f["part"]}" d="{d}" fill="{fill}"{st}/>')
    return ''.join(out)


def station_shape(x, y, sid, n_loops, r=RING_R, capw=CAP_W, cls='ak-mark', fill=PR, idcls='sid', hub=False):
    """(svg, box). A ring for a variable on one loop, a capsule for one several loops share."""
    if hub:
        lines = wrap2(N[sid]['label'], 15, 600)
        w = max(tw(t, 15, 600) for t in lines) + 26
        h = 20 + 18 * len(lines) + 10
        s = (f'<rect class="{cls}" x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" '
             f'fill="{fill}" stroke-width="2"/>')
        s += text_el(x, y - h / 2 + 19, sid, idcls, 'middle')
        s += lines_el(x, y - h / 2 + 19 + 19, lines, 'ak-label lab', 18, 'middle',
                      f' data-node="{sid}" data-name="{E(N[sid]["label"])}"')
        return s, (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if n_loops == 1:
        s = f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke-width="2"/>'
        box = (x - r, y - r, x + r, y + r)
    else:
        s = (f'<rect class="{cls}" x="{x - capw / 2:.1f}" y="{y - r:.1f}" width="{capw}" height="{2 * r}" rx="{r}" '
             f'fill="{fill}" stroke-width="2"/>')
        box = (x - capw / 2, y - r, x + capw / 2, y + r)
    s += text_el(x, y + 4.6, sid, idcls, 'middle')
    return s, box


def label_block(x, y, box, side, lines, size, lh, gap=6, dx=0, dy=0):
    """Anchor, first baseline and box of a label beside a station box, on the side named."""
    x0, y0, x1, y1 = box
    hgt = lh * (len(lines) - 1) + size * 0.98
    wid = max(tw(t, size, 600) for t in lines)
    asc = size * 0.76
    if side == 'e':
        ax, anc, ty = x1 + gap, 'start', y - hgt / 2 + asc
    elif side == 'w':
        ax, anc, ty = x0 - gap, 'end', y - hgt / 2 + asc
    elif side == 'n':
        ax, anc, ty = x, 'middle', y0 - gap - hgt + asc
    elif side == 's':
        ax, anc, ty = x, 'middle', y1 + gap + asc
    elif side == 'ne':
        ax, anc, ty = x1 - 2, 'start', y0 - gap - hgt + asc
    elif side == 'nw':
        ax, anc, ty = x0 + 2, 'end', y0 - gap - hgt + asc
    elif side == 'se':
        ax, anc, ty = x1 - 2, 'start', y1 + gap + asc
    else:
        ax, anc, ty = x0 + 2, 'end', y1 + gap + asc
    ax += dx
    ty += dy
    left = ax if anc == 'start' else (ax - wid if anc == 'end' else ax - wid / 2)
    return ax, ty, anc, (left, ty - asc, left + wid, ty - asc + hgt)


def tag_height(n_tracks, pitch, lw, base=17.0):
    return max(base, (n_tracks - 1) * pitch + lw + 8)


def tag_cost(poly, obstacles, placed):
    xs, ys = [q[0] for q in poly], [q[1] for q in poly]
    bx = (min(xs), min(ys), max(xs), max(ys))
    c = sum(1000 for ob in obstacles if box_hit(bx, ob, 1))
    c += sum(1000 for o in placed if convex_hit(poly, o, 1.5))
    return c


def offset_point(pts, s, mo):
    p, u = point_at(pts, s)
    return (p[0] - u[1] * mo, p[1] + u[0] * mo), u


def place_tags(lay, obstacles, lw, h_base=17.0, body=15.0, point=6.0, keep=13.0, shift=None):
    """One tag per connection, on the longest straight run of its corridor, slid by the least distance that clears
    the stations, names and tags already placed. The two directions of a two-step loop are placed together."""
    shift = shift or {}
    placed, out = [], []
    half = (body + point) / 2
    for c in CORR:
        base = lay.corridor(c)
        by_link = {}
        for t in c['tracks']:
            by_link.setdefault(t['link'], []).append(t)
        rr = runs(base)
        longest = max(rr, key=lambda r_: r_[2])
        s0 = sum(r_[2] for r_ in rr[:rr.index(longest)])
        lo, hi = s0 + keep + half, s0 + longest[2] - keep - half
        Lp = plen(base)
        info = []
        for link, grp in by_link.items():
            fwd = L[link]['from'] == c['a']
            pts = base if fwd else list(reversed(base))
            offs = [t['unit'] * lay.pitch * (1 if fwd else -1) for t in grp]
            h = tag_height(len(grp), lay.pitch, lw, h_base)
            info.append((link, fwd, pts, sum(offs) / len(offs), h))
        mid = s0 + longest[2] / 2
        if len(info) == 2:
            best = None
            lead = next(i for i, x in enumerate(info) if x[1])
            for order in ('out', 'in'):
                for sep in (48, 44, 40, 36, 32, 28, 24):
                    for d in sorted(range(-48, 49, 3), key=abs):
                        polys, pos = [], {}
                        for i, (link, fwd, pts, mo, h) in enumerate(info):
                            ahead = (i == lead) == (order == 'out')
                            sb = min(max(mid + d + (sep / 2 if ahead else -sep / 2), lo), hi)
                            sp = sb if fwd else Lp - sb
                            p, u = offset_point(pts, sp, mo)
                            pos[link] = (p, u, h)
                            polys.append(tag_poly(p, u, h, body, point))
                        cost = (sum(tag_cost(pg, obstacles, placed) for pg in polys) + abs(d) * 0.4 + (48 - sep) * 0.6
                                + (0 if order == 'out' else 4))
                        if convex_hit(polys[0], polys[1], 1.5):
                            cost += 1000
                        if best is None or cost < best[0]:
                            best = (cost, pos)
            for link, (p, u, h) in best[1].items():
                placed.append(tag_poly(p, u, h, body, point))
                out.append((link, p, u, h, c))
        else:
            for link, fwd, pts, mo, h in info:
                pref = (mid if fwd else Lp - mid) + shift.get(link, 0.0)
                lo2, hi2 = (lo, hi) if fwd else (Lp - hi, Lp - lo)
                best = None
                for d in sorted(range(-60, 61, 3), key=abs):
                    sp = min(max(pref + d, lo2), hi2)
                    p, u = offset_point(pts, sp, mo)
                    cost = tag_cost(tag_poly(p, u, h, body, point), obstacles, placed) + abs(sp - pref) * 0.4
                    if best is None or cost < best[0]:
                        best = (cost, p, u)
                placed.append(tag_poly(best[1], best[2], h, body, point))
                out.append((link, best[1], best[2], h, c))
    return out, placed


BUL_H = 22.0


def bullet_w(lid):
    return tw(lid, 14, 700) + 16


def own_corridors(lid):
    return [c for c in CORR if all(t['loop'] == lid for t in c['tracks'])]


def box_entry(q0, c, box):
    t_in = 0.0
    for k in (0, 1):
        d = c[k] - q0[k]
        if abs(d) < 1e-9:
            continue
        lo_, hi_ = (box[0], box[2]) if k == 0 else (box[1], box[3])
        t1, t2 = (lo_ - q0[k]) / d, (hi_ - q0[k]) / d
        t_in = max(t_in, min(t1, t2))
    return (q0[0] + (c[0] - q0[0]) * t_in, q0[1] + (c[1] - q0[1]) * t_in)


def bullet_candidates(lay, lid, lw):
    first = LO[lid]['stations'][0]['code']
    w, h = bullet_w(lid), BUL_H
    out = []
    for c in own_corridors(lid):
        base = lay.corridor(c)
        if first == c['b']:
            base = list(reversed(base))
        touches = first in (c['a'], c['b'])
        hw_c = ((len(c['tracks']) - 1) * lay.pitch + lw) / 2
        acc_ = 0.0
        for (p0, p1, ln) in runs(base):
            for f in (0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8):
                s_ = acc_ + ln * f
                p, u = point_at(base, s_)
                ext = abs(u[0]) * w / 2 + abs(u[1]) * h / 2
                if min(f, 1 - f) * ln >= ext + 6:
                    out.append((p, (0 if touches else 40) + s_ / 40, None))
                n = (-u[1], u[0])
                dirs = [n, (-n[0], -n[1])]
                if abs(u[0]) > 0.3 and abs(u[1]) > 0.3:
                    dirs += [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dv in dirs:
                    cross = abs(dv[0] * n[0] + dv[1] * n[1])
                    edge = hw_c / max(cross, 0.3)
                    ext_d = abs(dv[0]) * w / 2 + abs(dv[1]) * h / 2
                    for g in (9, 16, 26, 38):
                        q0 = (p[0] + dv[0] * edge, p[1] + dv[1] * edge)
                        cc = (p[0] + dv[0] * (edge + g + ext_d), p[1] + dv[1] * (edge + g + ext_d))
                        bx = (cc[0] - w / 2, cc[1] - h / 2, cc[0] + w / 2, cc[1] + h / 2)
                        q1 = box_entry(q0, cc, bx)
                        bend = 0 if dv in (n, (-n[0], -n[1])) else 15
                        out.append((cc, 150 + g + bend + (0 if touches else 20) + s_ / 40, (q0, q1)))
            acc_ += ln
    return out


def seg_hits_box(p, q, bx, pad=2.0):
    n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 2))
    for i in range(n + 1):
        t = i / n
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if bx[0] - pad <= x <= bx[2] + pad and bx[1] - pad <= y <= bx[3] + pad:
            return True
    return False


def place_bullets(lay, station_boxes, other_boxes, tag_polys, lw):
    segs = []
    for c in CORR:
        hw = ((len(c['tracks']) - 1) * lay.pitch + lw) / 2 + 3
        pts = lay.corridor(c)
        for i in range(len(pts) - 1):
            segs.append((id(c), pts[i], pts[i + 1], hw, c))

    def score(lid, cand, placed):
        (cx, cy), pref, leader = cand
        w, h = bullet_w(lid), BUL_H
        bx = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
        sc = pref
        mine = {id(c) for c in own_corridors(lid)}
        for cid, p, q, hw, c in segs:
            if cid in mine and leader is None:
                continue
            if seg_box(p, q, (bx[0] - hw, bx[1] - hw, bx[2] + hw, bx[3] + hw)):
                sc += 1000
            if leader is not None and cid not in mine and seg_hits_box(leader[0], leader[1], (min(p[0], q[0]) - hw, min(p[1], q[1]) - hw, max(p[0], q[0]) + hw, max(p[1], q[1]) + hw), 0) and \
                    seg_box(leader[0], leader[1], (min(p[0], q[0]) - hw, min(p[1], q[1]) - hw, max(p[0], q[0]) + hw, max(p[1], q[1]) + hw)):
                pass
        for ob in station_boxes:
            if box_hit(bx, ob, 7):
                sc += 1000
            if leader is not None and seg_hits_box(leader[0], leader[1], ob):
                sc += 1000
        for ob in other_boxes + placed:
            if box_hit(bx, ob, 3):
                sc += 1000
            if leader is not None and seg_hits_box(leader[0], leader[1], ob):
                sc += 1000
        bp = box_poly(bx)
        for tp in tag_polys:
            if convex_hit(bp, tp, 4):
                sc += 1000
            if leader is not None and convex_hit([leader[0], leader[1]], tp, 2):
                sc += 1000
        return sc

    cands = {lid: bullet_candidates(lay, lid, lw) for lid in NUMBERED}
    free = {lid: sum(1 for c in cands[lid] if score(lid, c, []) < 1000) for lid in NUMBERED}
    chosen, placed = {}, []
    for lid in sorted(NUMBERED, key=lambda k: (free[k], NUMBERED.index(k))):
        best = min(((score(lid, c, placed), c) for c in cands[lid]), key=lambda x: x[0])
        chosen[lid] = (best[1], best[0])
        (cx, cy) = best[1][0]
        w = bullet_w(lid)
        placed.append((cx - w / 2, cy - BUL_H / 2, cx + w / 2, cy + BUL_H / 2))
    return chosen


def bullet_svg(cx, cy, lid, ground, leader=None):
    w, h = bullet_w(lid), BUL_H
    x, y = cx - w / 2, cy - h / 2
    s = ''
    if leader:
        (x0, y0), (x1, y1) = leader
        s += f'<path class="leader" d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" stroke-width="1" fill="none"/>'
    s += (f'<rect class="bul" x="{x + 0.75:.1f}" y="{y + 0.75:.1f}" width="{w - 1.5:.1f}" height="{h - 1.5:.1f}" '
          f'fill="{ground}" stroke-width="1.5"/>')
    s += text_el(cx, cy + 5, lid, 'bul-t', 'middle')
    return f'<g class="bullet" data-bullet="{lid}">{s}</g>'


def loop_say(lid):
    o = LO[lid]
    stations = ', '.join(f"{s['code']} {s['label']}" for s in o['stations'])
    return f"Loop {lid}, {kind_line(lid)}: {o['title']}. Stations {stations}."


def station_say(sid):
    return f"{sid} {N[sid]['label']}. {N[sid]['increase_means']}"


def poster(view='overview'):
    lay = Lay(PCELL, POX, POY, PPITCH, PRAD)
    fp = field_polys(lay)
    # stations and names first; tags and bullets keep clear of them
    st_items, st_boxes, lab_boxes = {}, [], []
    for sid in STATIONS:
        x, y = lay.st(sid)
        nl = len(station_loops(sid))
        hub = SIDE[sid] == 'inside'
        shape, box = station_shape(x, y, sid, nl, hub=hub)
        lab = ''
        if not hub:
            lines = wrap2(N[sid]['label'], 15) if sid in WRAP else [N[sid]['label']]
            dx, dy = NUDGE.get(sid, (0, 0))
            ax, ty, anc, lb = label_block(x, y, box, SIDE[sid], lines, 15, 18, 6, dx, dy)
            lab = lines_el(ax, ty, lines, 'ak-label lab', 18, anc, f' data-node="{sid}" data-name="{E(N[sid]["label"])}"')
            lab_boxes.append(lb)
        st_boxes.append(box)
        rel = ' '.join('loop-' + k.lower() for k in station_loops(sid))
        say = station_say(sid)
        st_items[sid] = (f'<g class="stn" role="button" data-select="var-{sid.lower()}" data-node="{sid}" data-rel="{rel}" '
                         f'aria-label="{E(say)}" data-say="{E(say)}">{shape}{lab}</g>')
    # district names
    dn_svg, dn_boxes = {}, []
    for d, (cx, cy, wrapit) in DNAME.items():
        x, y = lay.px((cx, cy))
        lw_ = tw(d, 40, 800, 'Inter Tight', -0.03)
        title = AREAS[d]['title']
        parts = [text_el(x, y, d, 'dl')]
        if wrapit:
            l1, l2 = wrap2(title, 22, 800, 'Inter Tight')
            parts.append(lines_el(x + lw_ + 8, y - 26, [l1, l2], 'dn', 26))
            nw = max(tw(l1, 22, 800, 'Inter Tight'), tw(l2, 22, 800, 'Inter Tight'))
            bx = (x - 2, y - 50, x + lw_ + 8 + nw + 2, y + 6)
        else:
            parts.append(text_el(x + lw_ + 8, y - 2, title, 'dn'))
            nw = tw(title, 22, 800, 'Inter Tight')
            bx = (x - 2, y - 32, x + lw_ + 8 + nw + 2, y + 6)
        dn_svg[d] = ''.join(parts)
        dn_boxes.append(bx)
    for (d, part), (cx, cy) in PATCH_LETTER.items():
        x, y = lay.px((cx, cy))
        dn_svg[d] += text_el(x, y, d, 'dl', extra=' aria-hidden="true"')
        dn_boxes.append((x - 2, y - 32, x + 30, y + 4))
    avoid = list(POSTER_AVOID)
    tags, tag_polys = place_tags(lay, st_boxes + lab_boxes + dn_boxes + avoid, PLW, shift={'L56': 26.0, 'L06': 14.0, 'L55': -16.0})
    bul = place_bullets(lay, st_boxes, lab_boxes + dn_boxes + avoid, tag_polys, PLW)
    # loop lines, grouped per loop so a loop lights as one line
    loop_svg = []
    for lid in NUMBERED:
        o = LO[lid]
        parts = []
        for c in CORR:
            for t in c['tracks']:
                if t['loop'] != lid:
                    continue
                pts, off = lay.track(c, t)
                d = rounded_path(pts, lay.radius, off)
                da, _ = dash_attr(L[t['link']]['evidence'], PLW)
                parts.append(f'<g class="trk"{link_attrs(t["link"])}><path d="{d}" fill="none" stroke-width="{PLW}"{da}/>'
                             f'<path class="ak-hit" d="{d}"/></g>')
        (cc, pref, leader), sc = bul[lid]
        parts.append(bullet_svg(cc[0], cc[1], lid, PR, leader))
        steps = ' '.join(s['id'] for s in o['steps'])
        rel = ' '.join('var-' + s['code'].lower() for s in o['stations'])
        say = loop_say(lid)
        if lid == 'R10':
            say_r = say + ' Opens the field card.'
            loop_svg.append(f'<a href="#loop-r10" class="loop" data-select="loop-r10" data-loop="{lid}" data-steps="{steps}" '
                            f'data-rel="{rel}" aria-label="{E(say_r)}" data-say="{E(say_r)}">{"".join(parts)}</a>')
        else:
            loop_svg.append(f'<g class="loop" role="button" data-select="loop-{lid.lower()}" data-loop="{lid}" '
                            f'data-steps="{steps}" data-rel="{rel}" aria-label="{E(say)}" data-say="{E(say)}">{"".join(parts)}</g>')
    tag_svg_ = []
    for link, p, u, h, c in tags:
        f = field_at(fp, p)
        halo = FIELD_PR if f else PR
        tag_svg_.append(tag_svg(p, u, L[link]['polarity'], h, NP, PR, halo))
    # fields: C is the door into its close-up; the others are ground
    fsvg = []
    for f in fp:
        pass
    body = []
    body.append(fields_svg([f for f in fp if f['district'] != 'C'], FIELD_PR, PR))
    cpoly = [f for f in fp if f['district'] == 'C']
    c_say = f"Area C, {AREAS['C']['title']}. {AREAS['C']['text']} Opens the close-up."
    # district names; C's name and field are one link
    names = []
    for d in 'ABDE':
        a = AREAS[d]
        say = f"Area {d}, {a['title']}. {a['text']}"
        rel = ' '.join('var-' + v.lower() for v in a['nodes'] if v in ST_CELL)
        names.append(f'<g class="dname" role="button" data-select="area-{d.lower()}" data-rel="{rel}" aria-label="{E(say)}" '
                     f'data-say="{E(say)}">{dn_svg[d]}</g>')
    body.append(f'<a href="#area-c" class="cdoor" aria-label="{E(c_say)}" data-say="{E(c_say)}">'
                + fields_svg(cpoly, FIELD_PR, PR) + f'<g class="dname">{dn_svg["C"]}</g></a>')
    body += names
    body += loop_svg
    body.append('<g class="tags" aria-hidden="true">' + ''.join(tag_svg_) + '</g>')
    body += [st_items[s] for s in STATIONS]
    ys = [b[3] for b in st_boxes + lab_boxes + dn_boxes]
    height = POSTER_H
    svg = (f'<svg class="poster-svg" data-view="{view}" viewBox="0 0 {PW} {height}" width="{PW}" height="{height}" '
           f'role="group" aria-labelledby="h-overview" data-ak-roving data-ak-nav="spatial">'
           + ''.join(body) + '</svg>')
    info = {'lay': lay, 'fields': fp, 'height': height, 'st_boxes': st_boxes, 'lab_boxes': lab_boxes,
            'dn_boxes': dn_boxes, 'bul': bul, 'tags': tags, 'max_y': max(ys)}
    return svg, info


POSTER_H = 900
# open-ground zones the HTML cartouches occupy on the poster (px): title, how to read it, key
POSTER_AVOID = [(0, 0, 700, 250), (950, 0, 1312, 250), (16, 700, 400, 880)]
