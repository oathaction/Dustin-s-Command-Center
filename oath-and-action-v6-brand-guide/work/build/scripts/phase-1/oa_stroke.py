"""Variable-width stroke drawing and Bezier fitting, for the drawn ampersand (option B) and the
condensed wordmark curves.

A stroke is a centreline of cubic Bezier segments plus a width rule. The width comes from a
broad-nib model (thin along the nib angle) times a per-point multiplier, so contrast follows
one consistent axis. Strokes are sampled, offset, joined with shapely, cut by terminal planes,
then the outline is refitted as cubic Beziers (Schneider's method) with nodes at corners and at
horizontal and vertical extrema, the way a type designer places points.
"""
import math
import sys

sys.path.append("/root/.local/lib/python3.13/site-packages")
from shapely.geometry import Polygon, LinearRing, box  # noqa: E402
from shapely.ops import unary_union  # noqa: E402
from shapely import affinity  # noqa: E402


# ---------------------------------------------------------------- centreline

def hobby_handles(p0, a0, p1, a1, tension=1.0):
    """Control points for a cubic from p0 (leaving at angle a0, degrees) to p1 (arriving at a1),
    using Hobby's velocity function so curves look drawn, not mechanical."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = math.hypot(dx, dy)
    phi = math.atan2(dy, dx)
    t0, t1 = math.radians(a0) - phi, phi - math.radians(a1)
    t0 = (t0 + math.pi) % (2 * math.pi) - math.pi
    t1 = (t1 + math.pi) % (2 * math.pi) - math.pi

    def rho(a, b):
        sa, sb, ca, cb = math.sin(a), math.sin(b), math.cos(a), math.cos(b)
        num = 2 + math.sqrt(2) * (sa - sb / 16) * (sb - sa / 16) * (ca - cb)
        den = 1 + (math.sqrt(5) - 1) / 2 * ca + (3 - math.sqrt(5)) / 2 * cb
        return num / den
    r0 = rho(t0, t1) / (3 * tension)
    r1 = rho(t1, t0) / (3 * tension)
    c0 = (p0[0] + d * r0 * math.cos(math.radians(a0)), p0[1] + d * r0 * math.sin(math.radians(a0)))
    c1 = (p1[0] - d * r1 * math.cos(math.radians(a1)), p1[1] - d * r1 * math.sin(math.radians(a1)))
    return c0, c1


def bez(p0, c0, c1, p1, t):
    mt = 1 - t
    return (mt ** 3 * p0[0] + 3 * mt * mt * t * c0[0] + 3 * mt * t * t * c1[0] + t ** 3 * p1[0],
            mt ** 3 * p0[1] + 3 * mt * mt * t * c0[1] + 3 * mt * t * t * c1[1] + t ** 3 * p1[1])


def bez_d(p0, c0, c1, p1, t):
    mt = 1 - t
    return (3 * mt * mt * (c0[0] - p0[0]) + 6 * mt * t * (c1[0] - c0[0]) + 3 * t * t * (p1[0] - c1[0]),
            3 * mt * mt * (c0[1] - p0[1]) + 6 * mt * t * (c1[1] - c0[1]) + 3 * t * t * (p1[1] - c1[1]))


class Stroke:
    """nodes: list of (x, y, angle_deg, width_multiplier[, tension]). Angles give the direction of travel."""

    def __init__(self, nodes, nib_angle=20.0, thin=92.0, thick=155.0, power=1.5, samples=120):
        self.nodes = nodes
        self.nib = nib_angle
        self.thin, self.thick, self.power = thin, thick, power
        self.samples = samples
        self.segs = []
        for a, b in zip(nodes, nodes[1:]):
            ten = a[4] if len(a) > 4 else 1.0
            c0, c1 = hobby_handles(a[:2], a[2], b[:2], b[2], ten)
            self.segs.append((a[:2], c0, c1, b[:2], a[3], b[3]))

    def width(self, ang, mult):
        s = abs(math.sin(ang - math.radians(self.nib))) ** self.power
        return (self.thin + (self.thick - self.thin) * s) * mult

    def points(self):
        out = []
        for si, (p0, c0, c1, p1, m0, m1) in enumerate(self.segs):
            n = self.samples
            for k in range(n + (1 if si == len(self.segs) - 1 else 0)):
                t = k / n
                x, y = bez(p0, c0, c1, p1, t)
                dx, dy = bez_d(p0, c0, c1, p1, t)
                if abs(dx) + abs(dy) < 1e-9:
                    dx, dy = bez_d(p0, c0, c1, p1, min(1, t + 1e-3))
                ang = math.atan2(dy, dx)
                # smoothstep between node multipliers
                u = t * t * (3 - 2 * t)
                m = m0 + (m1 - m0) * u
                out.append((x, y, ang, self.width(ang, m)))
        return out

    def polygon(self, ext0=0.0, ext1=0.0):
        """Union of the swept quads. ext0/ext1 extend the ends straight along the tangent so a
        terminal plane can cut them cleanly."""
        pts = self.points()
        if ext0:
            x, y, a, w = pts[0]
            pts.insert(0, (x - ext0 * math.cos(a), y - ext0 * math.sin(a), a, w))
        if ext1:
            x, y, a, w = pts[-1]
            pts.append((x + ext1 * math.cos(a), y + ext1 * math.sin(a), a, w))
        L, R = [], []
        for x, y, a, w in pts:
            nx, ny = -math.sin(a), math.cos(a)
            L.append((x + nx * w / 2, y + ny * w / 2))
            R.append((x - nx * w / 2, y - ny * w / 2))
        quads = []
        for i in range(len(pts) - 1):
            q = Polygon([L[i], L[i + 1], R[i + 1], R[i]])
            if not q.is_valid:
                q = q.buffer(0)
            quads.append(q)
        return unary_union(quads)

    def centreline_svg(self, k=1.0):
        d = []
        for i, (p0, c0, c1, p1, _, _) in enumerate(self.segs):
            if i == 0:
                d.append(f"M{p0[0] * k:.1f} {p0[1] * k:.1f}")
            d.append(f"C{c0[0] * k:.1f} {c0[1] * k:.1f} {c1[0] * k:.1f} {c1[1] * k:.1f} {p1[0] * k:.1f} {p1[1] * k:.1f}")
        return " ".join(d)


def clean(geom, r=0.6):
    """Remove slivers left by the quad union."""
    return geom.buffer(r, join_style=1).buffer(-2 * r, join_style=1).buffer(r, join_style=1)


# ---------------------------------------------------------------- fitting

def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _mul(a, s):
    return (a[0] * s, a[1] * s)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _norm(a):
    n = math.hypot(*a)
    return (a[0] / n, a[1] / n) if n > 1e-12 else (0.0, 0.0)


def fit_cubic(pts, t_left, t_right, err):
    """Schneider: fit a chain of cubic Beziers to pts with unit end tangents t_left (pointing into
    the curve) and t_right (pointing back into the curve)."""
    if len(pts) == 2:
        d = math.dist(pts[0], pts[1]) / 3
        return [(pts[0], _add(pts[0], _mul(t_left, d)), _add(pts[1], _mul(t_right, d)), pts[1])]
    u = _chord(pts)
    b = _gen(pts, u, t_left, t_right)
    me, split = _maxerr(pts, b, u)
    if me < err:
        return [b]
    if me < err * 4:
        for _ in range(20):
            u = [_newton(b, p, t) for p, t in zip(pts, u)]
            b = _gen(pts, u, t_left, t_right)
            me, split = _maxerr(pts, b, u)
            if me < err:
                return [b]
    split = max(1, min(len(pts) - 2, split))
    tc = _norm(_sub(pts[split - 1], pts[split + 1]))
    return fit_cubic(pts[:split + 1], t_left, tc, err) + fit_cubic(pts[split:], _mul(tc, -1), t_right, err)


def _chord(pts):
    u = [0.0]
    for i in range(1, len(pts)):
        u.append(u[-1] + math.dist(pts[i], pts[i - 1]))
    return [v / u[-1] for v in u]


def _gen(pts, u, tl, tr):
    p0, p3 = pts[0], pts[-1]
    C = [[0, 0], [0, 0]]
    X = [0, 0]
    for p, t in zip(pts, u):
        a1 = _mul(tl, 3 * t * (1 - t) ** 2)
        a2 = _mul(tr, 3 * t * t * (1 - t))
        C[0][0] += _dot(a1, a1); C[0][1] += _dot(a1, a2); C[1][1] += _dot(a2, a2)
        tmp = _sub(p, _add(_mul(p0, (1 - t) ** 3 + 3 * t * (1 - t) ** 2), _mul(p3, 3 * t * t * (1 - t) + t ** 3)))
        X[0] += _dot(a1, tmp); X[1] += _dot(a2, tmp)
    C[1][0] = C[0][1]
    det = C[0][0] * C[1][1] - C[0][1] * C[1][0]
    seg = math.dist(p0, p3)
    if abs(det) > 1e-12:
        al = (X[0] * C[1][1] - X[1] * C[0][1]) / det
        ar = (C[0][0] * X[1] - C[1][0] * X[0]) / det
    else:
        al = ar = seg / 3
    eps = 1e-6 * seg
    if al < eps or ar < eps:
        al = ar = seg / 3
    return (p0, _add(p0, _mul(tl, al)), _add(p3, _mul(tr, ar)), p3)


def _maxerr(pts, b, u):
    me, split = 0.0, len(pts) // 2
    for i, (p, t) in enumerate(zip(pts, u)):
        d = math.dist(bez(*b, t), p)
        if d > me:
            me, split = d, i
    return me, split


def _newton(b, p, t):
    q = bez(*b, t)
    d1 = bez_d(*b, t)
    p0, c0, c1, p1 = b
    mt = 1 - t
    d2 = (6 * mt * (c1[0] - 2 * c0[0] + p0[0]) + 6 * t * (p1[0] - 2 * c1[0] + c0[0]),
          6 * mt * (c1[1] - 2 * c0[1] + p0[1]) + 6 * t * (p1[1] - 2 * c1[1] + c0[1]))
    num = (q[0] - p[0]) * d1[0] + (q[1] - p[1]) * d1[1]
    den = d1[0] ** 2 + d1[1] ** 2 + (q[0] - p[0]) * d2[0] + (q[1] - p[1]) * d2[1]
    if abs(den) < 1e-12:
        return t
    return min(1.0, max(0.0, t - num / den))


def resample(ring, step):
    """Even spacing along a closed ring (list of points, not repeated at the end)."""
    pts = list(ring)
    out = [pts[0]]
    acc = 0.0
    n = len(pts)
    for i in range(1, n + 1):
        a, b = pts[i - 1], pts[i % n]
        seg = math.dist(a, b)
        while acc + seg >= step and seg > 0:
            t = (step - acc) / seg
            a = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            out.append(a)
            seg = math.dist(a, b)
            acc = 0.0
        acc += seg
    return out[:-1] if math.dist(out[-1], out[0]) < step * 0.5 else out


def ring_to_beziers(ring, err=0.8, corner_deg=28.0, step=2.0, look=3):
    """Fit one closed ring. Nodes go at corners (turning angle above corner_deg over a short
    window) and at horizontal and vertical extrema, with axis-aligned handles there."""
    pts = resample(ring, step)
    n = len(pts)

    def turn(i):
        a, b, c = pts[(i - look) % n], pts[i], pts[(i + look) % n]
        v1, v2 = _norm(_sub(b, a)), _norm(_sub(c, b))
        return math.degrees(math.acos(max(-1, min(1, _dot(v1, v2)))))
    turns = [turn(i) for i in range(n)]
    corners = []
    i = 0
    while i < n:
        if turns[i] > corner_deg:
            j = i
            best = i
            while j < n and turns[j] > corner_deg:
                if turns[j] > turns[best]:
                    best = j
                j += 1
            corners.append(best)
            i = j
        else:
            i += 1
    # extrema: sign changes of dx or dy between neighbours, away from corners
    ext = {}
    for i in range(n):
        a, b, c = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        if any(min((i - k) % n, (k - i) % n) <= look + 1 for k in corners):
            continue
        if (b[1] - a[1]) * (c[1] - b[1]) < 0:
            ext[i] = "h"  # tangent horizontal
        elif (b[0] - a[0]) * (c[0] - b[0]) < 0:
            ext[i] = "v"
    nodes = sorted(set(corners) | set(ext))
    if not nodes:
        nodes = [0]
    segs = []
    for k, i0 in enumerate(nodes):
        i1 = nodes[(k + 1) % len(nodes)]
        run = [pts[(i0 + j) % n] for j in range(((i1 - i0) % n or n) + 1)]
        if len(run) < 2:
            continue
        tl = _tangent(run, 0, ext.get(i0), forward=True)
        tr = _tangent(run, len(run) - 1, ext.get(i1), forward=False)
        segs += fit_cubic(run, tl, tr, err)
    return segs


def _tangent(run, idx, axis, forward):
    if forward:
        v = _norm(_sub(run[min(len(run) - 1, 2)], run[0]))
    else:
        v = _norm(_sub(run[max(0, len(run) - 3)], run[-1]))
    if axis == "h":
        v = (1.0 if v[0] >= 0 else -1.0, 0.0)
    elif axis == "v":
        v = (0.0, 1.0 if v[1] >= 0 else -1.0)
    return v


def geom_to_d(geom, err=0.8, nd=1, transform=None, step=2.0, corner_deg=28.0):
    """Shapely polygon(s) to an SVG path string of fitted cubic Beziers."""
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    out = []
    for pg in polys:
        for ring in [pg.exterior] + list(pg.interiors):
            coords = list(ring.coords)[:-1]
            segs = ring_to_beziers(coords, err=err, step=step, corner_deg=corner_deg)
            if not segs:
                continue
            f = transform or (lambda p: p)

            def fm(p):
                q = f(p)
                return f"{q[0]:.{nd}f} {q[1]:.{nd}f}"
            d = [f"M{fm(segs[0][0])}"]
            for p0, c0, c1, p1 in segs:
                if math.dist(p0, c0) < 1e-6 and math.dist(p1, c1) < 1e-6:
                    d.append(f"L{fm(p1)}")
                else:
                    d.append(f"C{fm(c0)} {fm(c1)} {fm(p1)}")
            d.append("Z")
            out.append("".join(d))
    return "".join(out)


def count_nodes(d):
    return d.count("C") + d.count("L")
