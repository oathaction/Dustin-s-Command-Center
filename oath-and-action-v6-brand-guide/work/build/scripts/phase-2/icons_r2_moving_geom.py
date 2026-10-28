"""Contour builder for Concept 2, Moving part (design director, Phase 2 round two, October 28, 2026).

Every piece is authored by hand as a closed contour of straight lines and circular arcs on the
24-unit grid. Convex corners take an exact fillet (1 unit in the display master), concave corners
stay square, and the result is written as SVG path data with only M, L, H, V, A and Z, so a
producer reading the file sees the geometry as it was drawn.

Conventions (screen coordinates, y down):
  - A solid contour runs clockwise on screen and a hole runs counterclockwise, so the solid always
    lies to the right of the direction of travel.
  - A contour is a list of items. A point is (x, y) or (x, y, r), where r is the fillet radius at
    that corner (0 or omitted for a sharp corner). An arc marker ("arc", cx, cy, cw) between two
    points says the edge between them follows the circle with that center, clockwise on screen when
    cw is True. The radius is the distance from the center to the point before it.

Run with python3 -I. Loads pathops and fontTools from the user site, as round one does.
"""
import math
import sys

if "/root/.local/lib/python3.13/site-packages" not in sys.path:
    sys.path.append("/root/.local/lib/python3.13/site-packages")

import pathops  # noqa: E402
from fontTools.svgLib.path import parse_path  # noqa: E402

EPS = 1e-9


def fmt(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "", "-") else s


# ---------------------------------------------------------------- segments

class Seg:
    """A line (c is None) or a circular arc from p0 to p1 around center c, clockwise on screen
    when cw is True."""

    def __init__(self, p0, p1, c=None, cw=True):
        self.p0, self.p1, self.c, self.cw = p0, p1, c, cw
        self.R = math.dist(p0, c) if c is not None else None

    def is_arc(self):
        return self.c is not None

    def dir_at(self, p):
        """Unit tangent in the direction of travel at point p."""
        if not self.is_arc():
            dx, dy = self.p1[0] - self.p0[0], self.p1[1] - self.p0[1]
            L = math.hypot(dx, dy)
            return dx / L, dy / L
        ux, uy = (p[0] - self.c[0]) / self.R, (p[1] - self.c[1]) / self.R
        return (-uy, ux) if self.cw else (uy, -ux)

    def offset(self, r):
        """The same edge moved r toward the solid (the right of travel)."""
        if not self.is_arc():
            dx, dy = self.dir_at(self.p0)
            nx, ny = -dy, dx
            return ("line", (self.p0[0] + nx * r, self.p0[1] + ny * r), (dx, dy))
        return ("circle", self.c, self.R - r if self.cw else self.R + r)

    def foot(self, q):
        """The point of this edge's line or circle nearest q."""
        if not self.is_arc():
            dx, dy = self.dir_at(self.p0)
            t = (q[0] - self.p0[0]) * dx + (q[1] - self.p0[1]) * dy
            return self.p0[0] + dx * t, self.p0[1] + dy * t
        vx, vy = q[0] - self.c[0], q[1] - self.c[1]
        L = math.hypot(vx, vy)
        return self.c[0] + vx / L * self.R, self.c[1] + vy / L * self.R


def _intersect(a, b):
    """Intersections of two offset curves, each a line or a circle."""
    if a[0] == "circle" and b[0] == "line":
        a, b = b, a
    if a[0] == "line" and b[0] == "line":
        (p, u), (q, v) = (a[1], a[2]), (b[1], b[2])
        den = u[0] * v[1] - u[1] * v[0]
        if abs(den) < EPS:
            return []
        t = ((q[0] - p[0]) * v[1] - (q[1] - p[1]) * v[0]) / den
        return [(p[0] + u[0] * t, p[1] + u[1] * t)]
    if a[0] == "line" and b[0] == "circle":
        (p, u), (c, R) = (a[1], a[2]), (b[1], b[2])
        fx, fy = p[0] - c[0], p[1] - c[1]
        bb = fx * u[0] + fy * u[1]
        cc = fx * fx + fy * fy - R * R
        disc = bb * bb - cc
        if disc < -EPS:
            return []
        s = math.sqrt(max(0.0, disc))
        return [(p[0] + u[0] * t, p[1] + u[1] * t) for t in (-bb - s, -bb + s)]
    (c1, R1), (c2, R2) = (a[1], a[2]), (b[1], b[2])
    d = math.dist(c1, c2)
    if d < EPS or d > R1 + R2 + EPS or d < abs(R1 - R2) - EPS:
        return []
    x = (d * d + R1 * R1 - R2 * R2) / (2 * d)
    h = math.sqrt(max(0.0, R1 * R1 - x * x))
    ex, ey = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
    mx, my = c1[0] + ex * x, c1[1] + ey * x
    return [(mx - ey * h, my + ex * h), (mx + ey * h, my - ex * h)]


# ---------------------------------------------------------------- contours

def _parse(items):
    pts, arcs = [], {}
    for it in items:
        if it[0] == "arc":
            arcs[len(pts) - 1] = ((it[1], it[2]), it[3])
        else:
            pts.append((float(it[0]), float(it[1]), float(it[2]) if len(it) > 2 else 0.0))
    n = len(pts)
    segs = []
    for i in range(n):
        p0, p1 = pts[i][:2], pts[(i + 1) % n][:2]
        if i in arcs:
            c, cw = arcs[i]
            segs.append(Seg(p0, p1, c, cw))
        else:
            segs.append(Seg(p0, p1))
    return pts, segs


def contour_d(items):
    """SVG path data for one closed contour with its fillets."""
    pts, segs = _parse(items)
    n = len(pts)
    corner = []  # per vertex: (t_in, t_out, r) or None
    for i in range(n):
        r = pts[i][2]
        if r <= 0:
            corner.append(None)
            continue
        a, b = segs[i - 1], segs[i]
        V = pts[i][:2]
        # convex check: turning right (clockwise) at the vertex
        da, db = a.dir_at(V), b.dir_at(V)
        cross = da[0] * db[1] - da[1] * db[0]
        if cross <= EPS:
            raise ValueError(f"fillet asked at a concave or straight corner {V}")
        cands = _intersect(a.offset(r), b.offset(r))
        if not cands:
            raise ValueError(f"no fillet of radius {r} at {V}")
        F = min(cands, key=lambda q: math.dist(q, V))
        corner.append((a.foot(F), b.foot(F), r))

    def start_of(i):
        return corner[i][1] if corner[i] else pts[i][:2]

    def end_of(i):  # end point of segment i: the arrival at vertex i+1
        j = (i + 1) % n
        return corner[j][0] if corner[j] else pts[j][:2]

    out = [f"M{fmt(start_of(0)[0])} {fmt(start_of(0)[1])}"]
    cur = start_of(0)
    for i in range(n):
        s = segs[i]
        e = end_of(i)
        if s.is_arc():
            a0 = math.atan2(cur[1] - s.c[1], cur[0] - s.c[0])
            a1 = math.atan2(e[1] - s.c[1], e[0] - s.c[0])
            span = (a1 - a0) % (2 * math.pi) if s.cw else (a0 - a1) % (2 * math.pi)
            large = 1 if span > math.pi else 0
            out.append(f"A{fmt(s.R)} {fmt(s.R)} 0 {large} {1 if s.cw else 0} {fmt(e[0])} {fmt(e[1])}")
        else:
            if abs(e[0] - cur[0]) < 1e-6 and abs(e[1] - cur[1]) > 1e-6:
                out.append(f"V{fmt(e[1])}")
            elif abs(e[1] - cur[1]) < 1e-6 and abs(e[0] - cur[0]) > 1e-6:
                out.append(f"H{fmt(e[0])}")
            elif math.dist(e, cur) > 1e-6:
                out.append(f"L{fmt(e[0])} {fmt(e[1])}")
        cur = e
        j = (i + 1) % n
        if corner[j]:
            t_in, t_out, r = corner[j]
            if math.dist(t_in, t_out) > 1e-6:
                out.append(f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(t_out[0])} {fmt(t_out[1])}")
            cur = t_out
    out.append("Z")
    return "".join(out)


def path_d(*contours):
    return "".join(contour_d(c) for c in contours)


# ---------------------------------------------------------------- shape helpers
# Each returns contour items. Solids run clockwise on screen.

def rect(x, y, w, h, r=0.0):
    return [(x, y, r), (x + w, y, r), (x + w, y + h, r), (x, y + h, r)]


def rect_hole(x, y, w, h):
    """A rectangular hole, counterclockwise."""
    return [(x, y), (x, y + h), (x + w, y + h), (x + w, y)]


def circle_d(cx, cy, r, hole=False):
    """A full circle as two arcs. Clockwise for a solid, counterclockwise for a hole."""
    sw = 0 if hole else 1
    return (f"M{fmt(cx + r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 {sw} {fmt(cx - r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 {sw} {fmt(cx + r)} {fmt(cy)}Z")


def ellipse_d(cx, cy, rx, ry, hole=False):
    sw = 0 if hole else 1
    return (f"M{fmt(cx + rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 0 {sw} {fmt(cx - rx)} {fmt(cy)}"
            f"A{fmt(rx)} {fmt(ry)} 0 0 {sw} {fmt(cx + rx)} {fmt(cy)}Z")


def pt_on(cx, cy, R, deg):
    """The point at angle deg (screen degrees: 0 is +x, 90 is down) on a circle."""
    a = math.radians(deg)
    return cx + R * math.cos(a), cy + R * math.sin(a)


def ring_sector(cx, cy, r_out, r_in, a0, a1, r=0.0):
    """An annular sector from a0 to a1 degrees, clockwise on screen, with flat radial ends.
    Fillet r on its four convex corners."""
    p0, p1 = pt_on(cx, cy, r_out, a0), pt_on(cx, cy, r_out, a1)
    q1, q0 = pt_on(cx, cy, r_in, a1), pt_on(cx, cy, r_in, a0)
    return [(*p0, r), ("arc", cx, cy, True), (*p1, r), (*q1, r), ("arc", cx, cy, False), (*q0, r)]


# ---------------------------------------------------------------- measuring

def to_pathops(d):
    p = pathops.Path()
    parse_path(d, p.getPen())
    return pathops.simplify(p, clockwise=True)


def area_of(d):
    """Area of the filled region of path data, by flattening."""
    p = to_pathops(d)
    total = 0.0
    from fontTools.pens.areaPen import AreaPen
    pen = AreaPen()
    p.draw(pen)
    total = abs(pen.value)
    return total


def gap_between(d1, d2, step=0.05):
    """Smallest distance between two filled regions, sampled on their outlines."""
    import numpy as np
    def outline(d):
        p = to_pathops(d)
        from fontTools.pens.recordingPen import RecordingPen
        rec = RecordingPen()
        p.draw(rec)
        pts, cur, start = [], None, None
        for op, args in rec.value:
            if op == "closePath" and cur is not None and start is not None:
                a = start
                n = max(2, int(math.dist(cur, a) / step))
                pts += [(cur[0] + (a[0] - cur[0]) * k / n, cur[1] + (a[1] - cur[1]) * k / n) for k in range(1, n + 1)]
                cur = a
                continue
            if op == "moveTo":
                cur = args[0]
                start = cur
                pts.append(cur)
            elif op == "lineTo":
                a = args[0]
                n = max(2, int(math.dist(cur, a) / step))
                pts += [(cur[0] + (a[0] - cur[0]) * k / n, cur[1] + (a[1] - cur[1]) * k / n) for k in range(1, n + 1)]
                cur = a
            elif op in ("curveTo", "qCurveTo"):
                ctrl = [cur] + list(args)
                for k in range(1, 41):
                    t = k / 40
                    if len(ctrl) == 4:
                        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = ctrl
                        mt = 1 - t
                        pts.append((mt ** 3 * x0 + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x3,
                                    mt ** 3 * y0 + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * y3))
                    else:
                        (x0, y0), (x1, y1), (x2, y2) = ctrl[:3]
                        mt = 1 - t
                        pts.append((mt * mt * x0 + 2 * mt * t * x1 + t * t * x2, mt * mt * y0 + 2 * mt * t * y1 + t * t * y2))
                cur = args[-1]
        return np.array(pts)
    a, b = outline(d1), outline(d2)
    best = 1e9
    for i in range(0, len(a), 256):
        chunk = a[i:i + 256]
        dd = np.sqrt(((chunk[:, None, :] - b[None, :, :]) ** 2).sum(-1))
        best = min(best, float(dd.min()))
    overlap = not pathops.op(to_pathops(d1), to_pathops(d2), pathops.PathOp.INTERSECTION).bounds == (0, 0, 0, 0)
    return best, overlap
