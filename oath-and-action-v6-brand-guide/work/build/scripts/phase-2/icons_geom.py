"""Geometry helpers for the Phase 2 icon concepts (design director, October 28, 2026).

Builds on the Phase 1 symbol geometry (work/build/scripts/phase-1/symbols_geom.py), loaded by
explicit path because python3 -I drops the script folder from sys.path (D1-05). Adds the
helpers the icon concepts need: 2-unit walls for closed shapes, inset polygons, annular sectors,
an arrowhead, the Apple-like smoothed square holder and a true superellipse for comparison.

Every shape is a skia-pathops path, so unions and knockouts resolve to clean outlines. Output
path data has three decimals at most.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parent / "phase-1"
for _p in (str(P1), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
if "/root/.local/lib/python3.13/site-packages" not in sys.path:
    sys.path.append("/root/.local/lib/python3.13/site-packages")

import pathops  # noqa: E402
from symbols_geom import (K, circle, d_of, empty, fillet_poly, flatten_segments, intersect, minus,  # noqa: E402,F401
                          poly, rect, rrect, simplify, stroke_path, transform, union)


def area(path):
    """Signed-free area of a pathops path, by flattening its curves."""
    total = 0.0
    for contour in _contours(path):
        a = 0.0
        for i in range(len(contour)):
            x0, y0 = contour[i]
            x1, y1 = contour[(i + 1) % len(contour)]
            a += x0 * y1 - x1 * y0
        total += a / 2
    return abs(total)


def _contours(path, steps=24):
    out, cur = [], []
    for seg in flatten_segments(path):
        if seg[0] == "M":
            cur = [seg[1]]
        elif seg[0] == "L":
            cur.append(seg[2])
        elif seg[0] in ("C", "Q"):
            pts = seg[1:]
            for i in range(1, steps + 1):
                t = i / steps
                cur.append(_bez_pt(pts, t))
        elif seg[0] == "Z":
            if len(cur) > 2:
                out.append(cur)
            cur = []
    if len(cur) > 2:
        out.append(cur)
    return out


def _bez_pt(pts, t):
    mt = 1 - t
    if len(pts) == 4:
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
        return (mt ** 3 * x0 + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x3,
                mt ** 3 * y0 + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * y3)
    (x0, y0), (x1, y1), (x2, y2) = pts
    return (mt * mt * x0 + 2 * mt * t * x1 + t * t * x2, mt * mt * y0 + 2 * mt * t * y1 + t * t * y2)


def is_empty(path):
    try:
        return len(list(path.segments)) == 0
    except Exception:
        return True


def bounds(path):
    return path.bounds


def inset_poly(pts, d):
    """Offset a convex polygon (clockwise on screen) inward by d, with mitered corners."""
    n = len(pts)
    # signed area tells the winding; normals point inward
    s = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sign = 1 if s > 0 else -1
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * sign, dx / L * sign
        lines.append(((x0 + nx * d, y0 + ny * d), (dx, dy)))
    out = []
    for i in range(n):
        (p, u), (q, v) = lines[i - 1], lines[i]
        den = u[0] * v[1] - u[1] * v[0]
        t = ((q[0] - p[0]) * v[1] - (q[1] - p[1]) * v[0]) / den
        out.append((p[0] + u[0] * t, p[1] + u[1] * t))
    return out


def wall_poly(pts, w=2.0):
    """A closed polygon drawn as a wall of width w inside its outline (mitered corners)."""
    return minus(poly(*pts), poly(*inset_poly(pts, w)))


def ring(cx, cy, r_out, r_in):
    return minus(circle(cx, cy, r_out), circle(cx, cy, r_in))


def sector(cx, cy, r_out, r_in, a0, a1):
    """Annular sector from angle a0 to a1 in degrees (screen coordinates, clockwise positive),
    with radial (butt) ends."""
    p = pathops.Path()
    _arc_to(p, cx, cy, r_out, a0, a1, move=True)
    _arc_to(p, cx, cy, r_in, a1, a0, move=False)
    p.close()
    return simplify(p)


def _arc_to(p, cx, cy, r, a0, a1, move):
    n = max(1, int(math.ceil(abs(a1 - a0) / 90 - 1e-9)))
    step = (a1 - a0) / n
    for i in range(n):
        t0 = math.radians(a0 + i * step)
        t1 = math.radians(a0 + (i + 1) * step)
        alpha = 4 / 3 * math.tan((t1 - t0) / 4)
        x0, y0 = cx + r * math.cos(t0), cy + r * math.sin(t0)
        x1, y1 = cx + r * math.cos(t1), cy + r * math.sin(t1)
        c1 = (x0 - alpha * r * math.sin(t0), y0 + alpha * r * math.cos(t0))
        c2 = (x1 + alpha * r * math.sin(t1), y1 - alpha * r * math.cos(t1))
        if i == 0:
            if move:
                p.moveTo(x0, y0)
            else:
                p.lineTo(x0, y0)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], x1, y1)


def disc_seg(cx, cy, r, x_min=None, x_max=None, y_min=None, y_max=None):
    """A disc clipped by axis-aligned half planes."""
    c = circle(cx, cy, r)
    big = 1000
    clip = rect(-big if x_min is None else x_min, -big if y_min is None else y_min,
                (big if x_max is None else x_max) - (-big if x_min is None else x_min),
                (big if y_max is None else y_max) - (-big if y_min is None else y_min))
    return intersect(c, clip)


def rot(path, deg, cx, cy):
    """Rotate a path about (cx, cy)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    p = pathops.Path()
    pen = p.getPen()

    def f(q):
        if q is None:
            return None
        x, y = q[0] - cx, q[1] - cy
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)

    class T:
        def moveTo(self, a_):
            pen.moveTo(f(a_))

        def lineTo(self, a_):
            pen.lineTo(f(a_))

        def curveTo(self, *pts):
            pen.curveTo(*[f(q) for q in pts])

        def qCurveTo(self, *pts):
            pen.qCurveTo(*[f(q) for q in pts])

        def closePath(self):
            pen.closePath()

        def endPath(self):
            pen.endPath()

    path.draw(T())
    return p


def scale(path, s, dx=0.0, dy=0.0):
    return transform(path, s, dx, dy)


# ------------------------------------------------------------------ holders

def smoothed_square(x, y, size, radius_frac=0.2237, smoothing=0.6):
    """Rounded square with continuous (Apple-like) corners, by the corner-smoothing method Figma
    published in 2018 ("Desperately seeking squircles"). Each corner is a cubic transition, a
    circular arc of radius R spanning 90 x (1 - smoothing) degrees, and a mirror transition, so
    curvature ramps from zero on the straight edge to 1/R in the arc. With R = 0.2237 of the side
    and smoothing 0.6 each corner starts p = (1 + smoothing) x R = 0.358 of the side from the
    corner. Returns a pathops path."""
    R = radius_frac * size
    p_len = (1 + smoothing) * R
    arc_measure = 90 * (1 - smoothing)
    arc_len = math.sin(math.radians(arc_measure / 2)) * R * math.sqrt(2)
    angle_alpha = (90 - arc_measure) / 2
    p3p4 = R * math.tan(math.radians(angle_alpha / 2))
    angle_beta = 45 * smoothing
    c = p3p4 * math.cos(math.radians(angle_beta))
    d = c * math.tan(math.radians(angle_beta))
    b = (p_len - arc_len - c - d) / 3
    a = 2 * b
    W = H = size
    pth = pathops.Path()
    # current point helper with relative commands
    cur = [x + W - p_len, y]
    pth.moveTo(*cur)

    def rc(x1, y1, x2, y2, x3, y3):
        pth.cubicTo(cur[0] + x1, cur[1] + y1, cur[0] + x2, cur[1] + y2, cur[0] + x3, cur[1] + y3)
        cur[0] += x3
        cur[1] += y3

    def rarc(dx, dy, sweep_center):
        # circular arc of radius R from cur to cur + (dx, dy), center given absolutely
        cx_, cy_ = sweep_center
        a0 = math.degrees(math.atan2(cur[1] - cy_, cur[0] - cx_))
        a1 = math.degrees(math.atan2(cur[1] + dy - cy_, cur[0] + dx - cx_))
        while a1 < a0:
            a1 += 360
        _arc_to(pth, cx_, cy_, R, a0, a1, move=False)
        cur[0] += dx
        cur[1] += dy

    def L(x1, y1):
        pth.lineTo(x1, y1)
        cur[0], cur[1] = x1, y1

    # top right
    rc(a, 0, a + b, 0, a + b + c, d)
    rarc(arc_len, arc_len, (x + W - R, y + R))
    rc(d, c, d, b + c, d, a + b + c)
    L(x + W, y + H - p_len)
    # bottom right
    rc(0, a, 0, a + b, -d, a + b + c)
    rarc(-arc_len, arc_len, (x + W - R, y + H - R))
    rc(-c, d, -(b + c), d, -(a + b + c), d)
    L(x + p_len, y + H)
    # bottom left
    rc(-a, 0, -(a + b), 0, -(a + b + c), -d)
    rarc(-arc_len, -arc_len, (x + R, y + H - R))
    rc(-d, -c, -d, -(b + c), -d, -(a + b + c))
    L(x, y + p_len)
    # top left
    rc(0, -a, 0, -(a + b), d, -(a + b + c))
    rarc(arc_len, -arc_len, (x + R, y + R))
    rc(c, -d, b + c, -d, a + b + c, -d)
    pth.close()
    return pth


def superellipse(x, y, size, n=5.0, per_quadrant=24):
    """A true superellipse |u|^n + |v|^n = 1 filling the square (x, y, size), as smooth cubic
    Bezier segments through points sampled by angle (Catmull-Rom tangents, so the outline keeps
    one tangent everywhere). Curvature changes continuously all the way around."""
    a = size / 2
    cx, cy = x + a, y + a
    N = 4 * per_quadrant
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        ct, st = math.cos(t), math.sin(t)
        pts.append((cx + a * math.copysign(abs(ct) ** (2 / n), ct), cy + a * math.copysign(abs(st) ** (2 / n), st)))
    p = pathops.Path()
    p.moveTo(*pts[0])
    for i in range(N):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % N], pts[(i + 2) % N]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    p.close()
    return p


def superellipse_curvature(size, n=5.0, samples=400):
    """Exact curvature along one quarter of the superellipse |u|^n + |v|^n = 1 that fills a square
    of this size, from the middle of one edge to the middle of the next. Returns (arc length, k)."""
    a = size / 2

    def pt(t):
        return a * abs(math.cos(t)) ** (2 / n), a * abs(math.sin(t)) ** (2 / n)
    out, s, prev = [], 0.0, None
    for i in range(samples + 1):
        t = (math.pi / 2) * i / samples
        t = min(max(t, 1e-4), math.pi / 2 - 1e-4)
        h = 1e-5
        (x0, y0), (x1, y1), (x2, y2) = pt(t - h), pt(t), pt(t + h)
        dx, dy = (x2 - x0) / (2 * h), (y2 - y0) / (2 * h)
        ddx, ddy = (x2 - 2 * x1 + x0) / h ** 2, (y2 - 2 * y1 + y0) / h ** 2
        k = abs(dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5
        if prev is not None:
            s += math.hypot(x1 - prev[0], y1 - prev[1])
        prev = (x1, y1)
        out.append((s, k))
    return out


def plain_corner_curvature(size, radius_frac):
    """Curvature of a plain rounded square along the same quarter: straight, then 1/R, then straight."""
    R = radius_frac * size
    run = size / 2 - R
    arc = math.pi * R / 2
    return [(0.0, 0.0), (run, 0.0), (run, 1 / R), (run + arc, 1 / R), (run + arc, 0.0), (2 * run + arc, 0.0)]


def superellipse_fit_error(size, n=5.0, per_quadrant=24):
    """Largest distance between the cubic approximation and the exact superellipse, in px."""
    p = superellipse(0, 0, size, n, per_quadrant)
    cont = _contours(p, 32)[0]
    a = size / 2
    worst = 0.0
    for (x, y) in cont:
        u, v = abs(x - a) / a, abs(y - a) / a
        # radial distance to the exact curve along the ray from the center
        r = math.hypot(u, v)
        if r < 1e-9:
            continue
        ux, vy = u / r, v / r
        rho = (ux ** n + vy ** n) ** (-1 / n)
        worst = max(worst, abs(r - rho) * a)
    return worst


def plain_rounded(x, y, size, radius_frac=0.2237):
    return rrect(x, y, size, size, radius_frac * size)


def curvature_profile(path, samples=48):
    """Curvature along the first quarter of a holder outline, for the construction diagram.
    Returns a list of (arc length, curvature)."""
    out = []
    s = 0.0
    prev = None
    for seg in flatten_segments(path):
        if seg[0] not in ("L", "C"):
            continue
        if seg[0] == "L":
            (x0, y0), (x1, y1) = seg[1], seg[2]
            L = math.hypot(x1 - x0, y1 - y0)
            out.append((s, 0.0))
            s += L
            out.append((s, 0.0))
            continue
        pts = seg[1:]
        for i in range(samples):
            t = i / (samples - 1)
            x, y, dx, dy, ddx, ddy = _bez_d(pts, t)
            sp = math.hypot(dx, dy)
            k = abs(dx * ddy - dy * ddx) / sp ** 3 if sp > 1e-9 else 0
            if prev is not None:
                s += math.hypot(x - prev[0], y - prev[1])
            prev = (x, y)
            out.append((s, k))
        prev = None
    return out


def _bez_d(pts, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    mt = 1 - t
    x = mt ** 3 * x0 + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x3
    y = mt ** 3 * y0 + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * y3
    dx = 3 * mt * mt * (x1 - x0) + 6 * mt * t * (x2 - x1) + 3 * t * t * (x3 - x2)
    dy = 3 * mt * mt * (y1 - y0) + 6 * mt * t * (y2 - y1) + 3 * t * t * (y3 - y2)
    ddx = 6 * mt * (x2 - 2 * x1 + x0) + 6 * t * (x3 - 2 * x2 + x1)
    ddy = 6 * mt * (y2 - 2 * y1 + y0) + 6 * t * (y3 - 2 * y2 + y1)
    return x, y, dx, dy, ddx, ddy


def min_dist_to(path, cx, cy, samples=24):
    """Smallest distance from (cx, cy) to any point of the path outline (flattened)."""
    best = 1e9
    for contour in _contours(path, samples):
        for i in range(len(contour)):
            (x0, y0), (x1, y1) = contour[i], contour[(i + 1) % len(contour)]
            dx, dy = x1 - x0, y1 - y0
            L2 = dx * dx + dy * dy
            t = 0 if L2 == 0 else max(0, min(1, ((cx - x0) * dx + (cy - y0) * dy) / L2))
            px, py = x0 + t * dx, y0 + t * dy
            best = min(best, math.hypot(cx - px, cy - py))
    return best


def contains(path, x, y):
    return path.contains((x, y))


def transform(path, s=1.0, dx=0.0, dy=0.0):
    """Scale and move a path. Handles quadratic contours whose last point is implied (None),
    which the Phase 1 helper does not."""
    p = pathops.Path()
    pen = p.getPen()

    def f(q):
        return None if q is None else (q[0] * s + dx, q[1] * s + dy)

    class T:
        def moveTo(self, a):
            pen.moveTo(f(a))

        def lineTo(self, a):
            pen.lineTo(f(a))

        def curveTo(self, *pts):
            pen.curveTo(*[f(q) for q in pts])

        def qCurveTo(self, *pts):
            pen.qCurveTo(*[f(q) for q in pts])

        def closePath(self):
            pen.closePath()

        def endPath(self):
            pen.endPath()

    path.draw(T())
    return p
