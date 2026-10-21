"""Geometry helpers for the Phase 1 symbol family (design director).

Shapes are built as skia-pathops paths so knockouts and unions resolve to clean
outlines. Circles are four cubic arcs (k = 0.5523). Output is SVG path data with
coordinates rounded to 3 decimals.

Import from a script run with python3 -I after adding this folder to sys.path.
"""
import math
import sys

for _p in ("/root/.local/lib/python3.13/site-packages",):
    if _p not in sys.path:
        sys.path.append(_p)

import pathops  # noqa: E402

K = 0.5522847498


def _fmt(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class _Pen:
    def __init__(self):
        self.out = []

    def moveTo(self, p):
        self.out.append(f"M{_fmt(p[0])} {_fmt(p[1])}")

    def lineTo(self, p):
        self.out.append(f"L{_fmt(p[0])} {_fmt(p[1])}")

    def curveTo(self, *pts):
        (a, b), (c, d), (e, f) = pts[-3], pts[-2], pts[-1]
        self.out.append(f"C{_fmt(a)} {_fmt(b)} {_fmt(c)} {_fmt(d)} {_fmt(e)} {_fmt(f)}")

    def qCurveTo(self, *pts):
        (a, b), (e, f) = pts[-2], pts[-1]
        self.out.append(f"Q{_fmt(a)} {_fmt(b)} {_fmt(e)} {_fmt(f)}")

    def closePath(self):
        self.out.append("Z")

    def endPath(self):
        pass


def d_of(path):
    pen = _Pen()
    path.draw(pen)
    return "".join(pen.out)


def poly(*pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def rect(x, y, w, h):
    return poly((x, y), (x + w, y), (x + w, y + h), (x, y + h))


def rrect(x, y, w, h, r):
    if r <= 0:
        return rect(x, y, w, h)
    p = pathops.Path()
    k = K * r
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.cubicTo(x + w - r + k, y, x + w, y + r - k, x + w, y + r)
    p.lineTo(x + w, y + h - r)
    p.cubicTo(x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h)
    p.lineTo(x + r, y + h)
    p.cubicTo(x + r - k, y + h, x, y + h - r + k, x, y + h - r)
    p.lineTo(x, y + r)
    p.cubicTo(x, y + r - k, x + r - k, y, x + r, y)
    p.close()
    return p


def circle(cx, cy, r):
    p = pathops.Path()
    k = K * r
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p


def stroke_path(segments, width, cap="round", join="round"):
    """Outline an open or closed polyline/arc path given as SVG-like commands.

    segments: list of ("M", x, y) | ("L", x, y) | ("A", cx, cy, r, a0, a1) | ("Z",)
    Arcs are approximated by cubics. Returns a filled outline path.
    """
    p = pathops.Path()
    for s in segments:
        if s[0] == "M":
            p.moveTo(s[1], s[2])
        elif s[0] == "L":
            p.lineTo(s[1], s[2])
        elif s[0] == "A":
            _arc(p, *s[1:])
        elif s[0] == "Z":
            p.close()
    capm = {"round": pathops.LineCap.ROUND_CAP, "butt": pathops.LineCap.BUTT_CAP, "square": pathops.LineCap.SQUARE_CAP}[cap]
    joinm = {"round": pathops.LineJoin.ROUND_JOIN, "miter": pathops.LineJoin.MITER_JOIN, "bevel": pathops.LineJoin.BEVEL_JOIN}[join]
    p.stroke(width, capm, joinm, 4)
    return simplify(p)


def _arc(p, cx, cy, r, a0, a1):
    """Append an arc from angle a0 to a1 (degrees, screen coordinates, clockwise positive)."""
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
        if i == 0 and not _has_point(p):
            p.moveTo(x0, y0)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], x1, y1)


def _has_point(p):
    try:
        return len(list(p.segments)) > 0
    except Exception:
        return False


def simplify(p):
    return pathops.simplify(p, clockwise=True)


def union(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = pathops.op(out, q, pathops.PathOp.UNION)
    return simplify(out)


def minus(a, *bs):
    out = a
    for b in bs:
        out = pathops.op(out, b, pathops.PathOp.DIFFERENCE)
    return simplify(out)


def intersect(a, b):
    return simplify(pathops.op(a, b, pathops.PathOp.INTERSECTION))


def transform(path, s=1.0, dx=0.0, dy=0.0):
    p = pathops.Path()
    pen = p.getPen()

    class T:
        def moveTo(self, a):
            pen.moveTo((a[0] * s + dx, a[1] * s + dy))

        def lineTo(self, a):
            pen.lineTo((a[0] * s + dx, a[1] * s + dy))

        def curveTo(self, *pts):
            pen.curveTo(*[(q[0] * s + dx, q[1] * s + dy) for q in pts])

        def qCurveTo(self, *pts):
            pen.qCurveTo(*[(q[0] * s + dx, q[1] * s + dy) for q in pts])

        def closePath(self):
            pen.closePath()

        def endPath(self):
            pen.endPath()

    path.draw(T())
    return p


def empty():
    return pathops.Path()
