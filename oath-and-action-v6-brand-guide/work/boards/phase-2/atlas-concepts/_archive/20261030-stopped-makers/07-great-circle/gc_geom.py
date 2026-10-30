"""Geometry for concept 07, Great Circle (October 30, 2026).

Angles are in degrees, clockwise from twelve o'clock. Every core variable (areas A to E) has a fixed slot on
the rim in the model's own order; connections are cubic chords that leave and meet the rim square to it.
Imported by build_concept.py, which reads every label, sign, grade and delay from the model export.
"""
import math

CORE = ['A', 'B', 'C', 'D', 'E']


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def ring_layout(area_nodes, weights=None, gap=1.3, anchor=None):
    """Angles for every core variable. weights: {variable or area: weight}; a variable's own weight wins.
    anchor: (variable or area, angle) turns the ring so that item sits at that angle.
    Returns (angles, spans) where spans[area] = (start, end) in degrees, start < end, unwrapped."""
    weights = weights or {}
    pos, spans, t = {}, {}, 0.0
    for a in CORE:
        s0 = t
        for n in area_nodes[a]:
            w = weights.get(n, weights.get(a, 1.0))
            pos[n] = t + w / 2
            t += w
        spans[a] = (s0, t)
        t += gap
    k = 360.0 / t
    ang = {n: v * k for n, v in pos.items()}
    sp = {a: (s * k, e * k) for a, (s, e) in spans.items()}
    if anchor:
        key, target = anchor
        cur = ang[key] if key in ang else (sp[key][0] + sp[key][1]) / 2
        d = target - cur
        ang = {n: v + d for n, v in ang.items()}
        sp = {a: (s + d, e + d) for a, (s, e) in sp.items()}
    return ang, sp


def circ_mean(angles):
    x = sum(math.sin(math.radians(a)) for a in angles)
    y = sum(math.cos(math.radians(a)) for a in angles)
    return math.degrees(math.atan2(x, y))


def norm180(d):
    return (d + 180) % 360 - 180


# ---------------------------------------------------------------- cubic Bezier helpers
def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def bez_tan(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    dx = 3 * u * u * (x1 - x0) + 6 * u * t * (x2 - x1) + 3 * t * t * (x3 - x2)
    dy = 3 * u * u * (y1 - y0) + 6 * u * t * (y2 - y1) + 3 * t * t * (y3 - y2)
    n = math.hypot(dx, dy) or 1.0
    return (dx / n, dy / n)


def bez_split(p, t):
    """de Casteljau: the two halves of p at t."""
    (p0, p1, p2, p3) = p
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a, b, c = lerp(p0, p1), lerp(p1, p2), lerp(p2, p3)
    d, e = lerp(a, b), lerp(b, c)
    f = lerp(d, e)
    return (p0, a, d, f), (f, e, c, p3)


def bez_table(p, n=160):
    pts = [bez(p, i / n) for i in range(n + 1)]
    acc = [0.0]
    for i in range(1, n + 1):
        acc.append(acc[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    return pts, acc


def bez_len(p):
    return bez_table(p)[1][-1]


def t_at(p, s, table=None):
    """Parameter t at arc length s from the start."""
    pts, acc = table or bez_table(p)
    s = max(0.0, min(acc[-1], s))
    n = len(acc) - 1
    for i in range(1, n + 1):
        if acc[i] >= s:
            f = (s - acc[i - 1]) / ((acc[i] - acc[i - 1]) or 1)
            return (i - 1 + f) / n
    return 1.0


def bez_trim(p, s0, s1):
    """The piece of p from arc length s0 to (length - s1)."""
    tab = bez_table(p)
    L = tab[1][-1]
    ta, tb = t_at(p, s0, tab), t_at(p, L - s1, tab)
    _, right = bez_split(p, ta)
    tb2 = (tb - ta) / (1 - ta) if ta < 1 else 1
    left, _ = bez_split(right, tb2)
    return left


def d_of(p):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    return f'M{x0:.1f} {y0:.1f}C{x1:.1f} {y1:.1f} {x2:.1f} {y2:.1f} {x3:.1f} {y3:.1f}'


def chord(cx, cy, r, a0, a1, depth=None, skew=0.0):
    """A chord from rim angle a0 to rim angle a1 that leaves and meets the rim square to it.
    depth: how far the control points sit in from the rim, as a share of r (larger = deeper curve).
    skew bows the curve to the right of travel (used to part two steps that join the same pair)."""
    span = abs(norm180(a1 - a0))
    if depth is None:
        depth = 0.16 + 0.50 * (span / 180) ** 0.9
    p0, p3 = polar(cx, cy, r, a0), polar(cx, cy, r, a1)
    p1, p2 = polar(cx, cy, r * (1 - depth), a0), polar(cx, cy, r * (1 - depth), a1)
    if skew:
        dx, dy = p3[0] - p0[0], p3[1] - p0[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n          # right of travel in screen coordinates (y down)
        off = skew * n
        p1 = (p1[0] + nx * off, p1[1] + ny * off)
        p2 = (p2[0] + nx * off, p2[1] + ny * off)
    return (p0, p1, p2, p3)


def arc_d(cx, cy, r, a0, a1):
    """An SVG arc path from a0 to a1, clockwise."""
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}'


def band_d(cx, cy, r0, r1, a0, a1):
    """A filled annular sector between radii r0 < r1 from a0 to a1 clockwise."""
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = polar(cx, cy, r1, a0)
    x1, y1 = polar(cx, cy, r1, a1)
    x2, y2 = polar(cx, cy, r0, a1)
    x3, y3 = polar(cx, cy, r0, a0)
    return (f'M{x0:.2f} {y0:.2f}A{r1:.2f} {r1:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}'
            f'L{x2:.2f} {y2:.2f}A{r0:.2f} {r0:.2f} 0 {large} 0 {x3:.2f} {y3:.2f}Z')


# ---------------------------------------------------------------- line code (frame memo section 3)
def pattern(texture, w):
    if texture == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if texture == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if texture == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def fitted(texture, w, length):
    """Stretch the pattern a little so the line starts and ends on ink."""
    arr, cap = pattern(texture, w)
    if arr is None:
        return '', cap
    if texture == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.3f}', cap
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.3f}' for x in arr), cap


ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}           # length along the line, base width
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 2)}   # body, point, height, sign length, bar
