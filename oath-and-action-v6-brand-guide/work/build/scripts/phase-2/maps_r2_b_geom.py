"""Geometry for Direction B, Snowball and Thermostat. Pure math, no drawing.

Angles run clockwise from twelve o'clock, in radians. A point at angle t and radius p sits at
(cx + p sin t, cy - p cos t) in screen coordinates.

Snowball (reinforcing loop, V7 type R): one turn of an Archimedean spiral, p(t) = r (1 + (k - 1) t / 2 pi) for t in
[0, 2 pi]. It leaves the first variable at radius r and returns to it one lap further out, at radius k r.
Thermostat (balancing loop, V7 type B): a circle at radius r that closes on its start.

Stations sit at equal angles, t_i = 2 pi i / n, clockwise from twelve o'clock. The angle names the variable. The
outward step means one more turn and never an amount: k is one constant for every reinforcing loop and is never set
from V7's delay, direction, grade or valence.

Curves are written as cubic Bezier pieces of at most 8 degrees, with control points from the exact derivative
(Hermite form), so the drawn line stays within 0.01 px of the true spiral at card size. maps_r2_b_verify.py reads
the endpoints back and checks them against p(t).
"""
import math

TAU = 2 * math.pi


def rho(t, r, k):
    return r * (1 + (k - 1) * t / TAU)


def pt(cx, cy, p, t):
    return (cx + p * math.sin(t), cy - p * math.cos(t))


def deriv(t, r, k):
    """dP/dt for P(t) = (p sin t, -p cos t)."""
    p = rho(t, r, k)
    b = r * (k - 1) / TAU
    return (b * math.sin(t) + p * math.cos(t), -b * math.cos(t) + p * math.sin(t))


def stations(n, r, k):
    """[(t, p)] for the n stations, then the echo (t = 2 pi) for a spiral. A ring has k = 1 and no echo."""
    out = [(TAU * i / n, rho(TAU * i / n, r, k)) for i in range(n)]
    if k != 1:
        out.append((TAU, rho(TAU, r, k)))
    return out


def sample(t0, t1, r, k, cx, cy, step_deg=0.5):
    n = max(2, int(abs(t1 - t0) / math.radians(step_deg)) + 1)
    return [pt(cx, cy, rho(t0 + (t1 - t0) * i / n, r, k), t0 + (t1 - t0) * i / n) for i in range(n + 1)]


def arclen(t0, t1, r, k):
    """Arc length between two angles, by Simpson's rule on |dP/dt|."""
    n = max(8, int(abs(t1 - t0) / math.radians(1)) * 2)
    if n % 2:
        n += 1
    h = (t1 - t0) / n

    def f(t):
        dx, dy = deriv(t, r, k)
        return math.hypot(dx, dy)
    s = f(t0) + f(t1) + sum((4 if i % 2 else 2) * f(t0 + i * h) for i in range(1, n))
    return abs(s * h / 3)


def t_at(t0, s, r, k, direction=1):
    """The angle reached after arc length s from t0 (direction +1 forward, -1 backward)."""
    lo, hi = 0.0, math.pi
    for _ in range(60):
        m = (lo + hi) / 2
        if arclen(t0, t0 + direction * m, r, k) < s:
            lo = m
        else:
            hi = m
    return t0 + direction * (lo + hi) / 2


def bezier_d(t0, t1, r, k, cx, cy, max_deg=8.0, move=True):
    """SVG path data for the curve from t0 to t1 as cubic Bezier pieces (Hermite control points)."""
    n = max(1, math.ceil(abs(t1 - t0) / math.radians(max_deg)))
    h = (t1 - t0) / n
    x, y = pt(cx, cy, rho(t0, r, k), t0)
    d = [f"M{x:.2f} {y:.2f}"] if move else []
    for i in range(n):
        a, b = t0 + i * h, t0 + (i + 1) * h
        pa, pb = pt(cx, cy, rho(a, r, k), a), pt(cx, cy, rho(b, r, k), b)
        da, db = deriv(a, r, k), deriv(b, r, k)
        c1 = (pa[0] + da[0] * h / 3, pa[1] + da[1] * h / 3)
        c2 = (pb[0] - db[0] * h / 3, pb[1] - db[1] * h / 3)
        d.append(f"C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {pb[0]:.2f} {pb[1]:.2f}")
    return " ".join(d)


def tangent(t, r, k):
    dx, dy = deriv(t, r, k)
    L = math.hypot(dx, dy) or 1
    return dx / L, dy / L


def outward(t):
    """Unit vector pointing away from the center at angle t."""
    return math.sin(t), -math.cos(t)


def extents(n, r, k, disc, cx=0.0, cy=0.0, pad=0.0):
    """Bounding box of the curve plus every disc, for layout."""
    pts = sample(0, TAU, r, k, cx, cy, 1.0)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    for t, p in stations(n, r, k):
        x, y = pt(cx, cy, p, t)
        xs += [x - disc, x + disc]
        ys += [y - disc, y + disc]
    return min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad


def seg_dist(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    L = vx * vx + vy * vy
    if L == 0:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    u = max(0, min(1, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L))
    return math.hypot(p[0] - a[0] - u * vx, p[1] - a[1] - u * vy)


def rect_clear_of_poly(rect, poly, margin):
    """True when an axis-aligned rect (x0, y0, x1, y1) keeps at least margin px from every point of a polyline."""
    x0, y0, x1, y1 = rect
    for p in poly:
        dx = max(x0 - p[0], 0, p[0] - x1)
        dy = max(y0 - p[1], 0, p[1] - y1)
        if math.hypot(dx, dy) < margin:
            return False
    return True


def rect_clear_of_disc(rect, c, rad, margin):
    x0, y0, x1, y1 = rect
    dx = max(x0 - c[0], 0, c[0] - x1)
    dy = max(y0 - c[1], 0, c[1] - y1)
    return math.hypot(dx, dy) >= rad + margin


def rects_overlap(a, b, margin=0):
    return not (a[2] + margin <= b[0] or b[2] + margin <= a[0] or a[3] + margin <= b[1] or b[3] + margin <= a[1])
