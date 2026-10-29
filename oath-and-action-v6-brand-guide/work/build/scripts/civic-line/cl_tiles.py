"""Tile geometry for the Civic Line holders (DR-10): the three shapes, the
continuous-curvature rounded square, ink margins and tile composition.

The rounded square is the Lame superellipse |x|^5 + |y|^5 = 1 filling the
128 box, the same curve as the Phase 2 holder. The Phase 2 path drew it with
96 cubics whose curvature jumps at the joins (median 10 percent, and a sign
flip near each side's midpoint, where the outline briefly turns concave).
This module draws it again: the exact curve is sampled densely, resampled
evenly by arc length, and passed through a periodic C2 cubic spline; each
spline piece becomes one cubic Bezier. A C2 spline with non-zero speed has
continuous curvature, so the joins carry no curvature step.
"""
import math
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree

import cl_common as C
import cl_svg as S

N_EXP = 5.0            # superellipse exponent
SEGMENTS = 96          # cubic pieces in the rounded-square outline
SIZE = 128.0
HALF = SIZE / 2.0


def _exact(n_pts=200000):
    """Dense samples of |x|^5 + |y|^5 = 1 in its polar form, which has no
    singular points: r(phi) = (|cos phi|^5 + |sin phi|^5)^(-1/5)."""
    phi = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
    c, s = np.cos(phi), np.sin(phi)
    r = (np.abs(c) ** N_EXP + np.abs(s) ** N_EXP) ** (-1.0 / N_EXP)
    return HALF + HALF * r * c, HALF + HALF * r * s


def _exact_curvature(x, y):
    """Curvature of the dense closed sample, by central differences."""
    xp, yp = np.gradient(np.r_[x[-1], x, x[0]]), np.gradient(np.r_[y[-1], y, y[0]])
    xpp, ypp = np.gradient(xp), np.gradient(yp)
    k = (xp * ypp - yp * xpp) / np.maximum(np.hypot(xp, yp) ** 3, 1e-30)
    return k[1:-1]


def superellipse_spline(segments=SEGMENTS):
    """Periodic C2 spline through points of the exact curve. Knots are spaced
    evenly in a measure that weights arc length by curvature, so the tight
    corners get more pieces than the nearly flat sides. The spline parameter is
    that measure, which stays smooth, so the speed never drops to zero."""
    x, y = _exact()
    k = np.abs(_exact_curvature(x, y))
    d = np.hypot(np.diff(np.r_[x, x[0]]), np.diff(np.r_[y, y[0]]))
    w = d * (1.0 + 2.5 * k / k.max())
    L = np.r_[0, np.cumsum(w)]
    total = L[-1]
    xs, ys = np.r_[x, x[0]], np.r_[y, y[0]]
    u = np.linspace(0, total, segments, endpoint=False)
    px, py = np.interp(u, L, xs), np.interp(u, L, ys)
    knots = np.r_[u, total]
    sx = CubicSpline(knots, np.r_[px, px[0]], bc_type="periodic")
    sy = CubicSpline(knots, np.r_[py, py[0]], bc_type="periodic")
    return sx, sy, knots


def rounded_path(segments=SEGMENTS, nd=5):
    """Path data for the rounded square: one cubic per spline piece."""
    sx, sy, k = superellipse_spline(segments)
    # The spline can overshoot the box by about 1e-4 near the flat side
    # midpoints; clamping keeps the outline inside 0..128.
    q = lambda v: S.fmt(min(SIZE, max(0.0, float(v))), nd)  # noqa: E731
    parts = [f"M{q(sx(k[0]))} {q(sy(k[0]))}"]
    for i in range(segments):
        a, b = k[i], k[i + 1]
        h = b - a
        p0 = np.array([sx(a), sy(a)])
        p3 = np.array([sx(b), sy(b)])
        d0 = np.array([sx(a, 1), sy(a, 1)])
        d3 = np.array([sx(b, 1), sy(b, 1)])
        p1 = p0 + d0 * h / 3.0
        p2 = p3 - d3 * h / 3.0
        parts.append(f"C{q(p1[0])} {q(p1[1])} {q(p2[0])} {q(p2[1])} {q(p3[0])} {q(p3[1])}")
    return "".join(parts) + "Z"


def path_cubics(d):
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", d)]
    p0 = np.array(nums[:2])
    out = []
    k = 2
    while k + 6 <= len(nums):
        c = np.array(nums[k:k + 6]).reshape(3, 2)
        out.append(np.vstack([p0, c]))
        p0 = c[2]
        k += 6
    return out


def _curv(P, t):
    d1 = 3 * ((1 - t) ** 2 * (P[1] - P[0]) + 2 * (1 - t) * t * (P[2] - P[1]) + t * t * (P[3] - P[2]))
    d2 = 6 * ((1 - t) * (P[2] - 2 * P[1] + P[0]) + t * (P[3] - 2 * P[2] + P[1]))
    return (d1[0] * d2[1] - d1[1] * d2[0]) / np.hypot(*d1) ** 3


def curvature_report(d):
    """Curvature on each side of every join, and the largest relative step."""
    cs = path_cubics(d)
    samples = np.array([_curv(P, t) for P in cs for t in np.linspace(0, 1, 9)])
    peak = float(np.abs(samples).max())
    jumps, rel, signs = [], [], 0
    for i in range(len(cs)):
        a, b = _curv(cs[i], 1.0), _curv(cs[(i + 1) % len(cs)], 0.0)
        jumps.append(abs(a - b) / peak)
        rel.append(abs(a - b) / max(abs(a), abs(b), 1e-12))
        if a * b < 0:
            signs += 1
    concave = int((samples < 0).sum()) if samples.mean() > 0 else int((samples > 0).sum())
    return {"segments": len(cs), "max_jump_vs_peak_curvature": float(max(jumps)),
            "median_jump_vs_peak_curvature": float(np.median(jumps)),
            "max_relative_jump": float(max(rel)), "median_relative_jump": float(np.median(rel)),
            "sign_flips_at_joins": signs, "concave_samples": concave, "peak_curvature": peak}


def deviation_from_exact(d):
    """Largest distance (units) from the drawn outline to the exact curve."""
    x, y = _exact(400000)
    tree = cKDTree(np.c_[x, y])
    pts = np.array([[(1 - t) ** 3 * P[0][j] + 3 * (1 - t) ** 2 * t * P[1][j] + 3 * (1 - t) * t * t * P[2][j] + t ** 3 * P[3][j]
                     for j in (0, 1)] for P in path_cubics(d) for t in np.linspace(0, 1, 17)])
    return float(tree.query(pts)[0].max())


ROUNDED_D = rounded_path()


def shape_element(shape, color, rid=None):
    """The tile shape as one element. With rid, it carries id="<rid>-tile" and data-part="tile"."""
    ida = f' id="{rid}-tile" data-part="tile"' if rid else ""
    if shape == "square":
        return f'<rect{ida} x="0" y="0" width="128" height="128" fill="{color}"/>'
    if shape == "circle":
        return f'<circle{ida} cx="64" cy="64" r="64" fill="{color}"/>'
    if shape == "rounded":
        return f'<path{ida} d="{ROUNDED_D}" fill="{color}"/>'
    raise ValueError(shape)


# ------------------------------------------------------------------ margins

_BOUNDARY = None


def _rounded_tree():
    global _BOUNDARY
    if _BOUNDARY is None:
        x, y = _exact(60000)
        _BOUNDARY = cKDTree(np.c_[x, y])
    return _BOUNDARY


def inside_distance(shape, pts):
    """Distance from each point to the tile edge, positive inside, in units."""
    x, y = pts[:, 0], pts[:, 1]
    if shape == "square":
        return np.minimum.reduce([x, SIZE - x, y, SIZE - y])
    if shape == "circle":
        return HALF - np.hypot(x - HALF, y - HALF)
    if shape == "rounded":
        d = _rounded_tree().query(pts)[0]
        u, v = (x - HALF) / HALF, (y - HALF) / HALF
        inside = np.abs(u) ** N_EXP + np.abs(v) ** N_EXP <= 1.0
        return np.where(inside, d, -d)
    raise ValueError(shape)


def ink_samples(svg_text):
    """(x, y, h) samples of everything an SVG paints outside <defs>: flattened
    outline points with half the stroke width, plus miter tips with h = 0.
    Coordinates are in the coordinate system of the elements (no transforms)."""
    root = ET.fromstring(svg_text.encode("utf-8"))
    out = []

    def walk(node):
        for ch in node:
            t = S._strip(ch.tag)
            if t == "defs":
                continue
            if t == "g":
                walk(ch)
                continue
            if t not in S.GEOM_ATTRS:
                continue
            a = ch.attrib
            stroked = a.get("stroke", "none") != "none"
            h = float(a.get("stroke-width", "0")) / 2 if stroked else 0.0
            polys, closed = S._shape_polys(t, a)
            for p, c in zip(polys, closed):
                for xx, yy in p:
                    out.append((xx, yy, h))
                if stroked and a.get("stroke-linejoin") == "miter":
                    for xx, yy in S._miter_tips(p, c, h):
                        out.append((xx, yy, 0.0))
    walk(root)
    return np.array(out)


def scale_strokes(svg_text, k):
    """Every stroke-width in the markup multiplied by k (S-1: the tile's stroke cap)."""
    if abs(k - 1.0) < 1e-12:
        return svg_text
    return re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{S.fmt4(float(m.group(1)) * k)}"', svg_text)


def icon_margin(bare_svg_text, shape, factor, a=1.0, dx=0.0, k=1.0):
    """Smallest clearance (units, in the 128 tile) between the icon's ink and the
    tile edge when the bare export is scaled by factor * a about the center,
    shifted by factor * dx and drawn with its strokes multiplied by k."""
    s = ink_samples(scale_strokes(bare_svg_text.split("?>", 1)[-1], k))
    fa = factor * a
    pts = HALF + fa * (s[:, :2] - HALF)
    pts[:, 0] += factor * dx
    return float((inside_distance(shape, pts) - fa * s[:, 2]).min())


def hull_size(bare_svg_text):
    """Square root of the area inside the convex outline around all the ink
    (outline points widened by half the stroke in 16 directions), in box units,
    and the hull centroid's offset from the ink box center (x, y)."""
    from scipy.spatial import ConvexHull
    s = ink_samples(bare_svg_text.split("?>", 1)[-1])
    ang = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    P = np.vstack([s[:, :2]] + [s[:, :2] + np.c_[np.cos(t) * s[:, 2], np.sin(t) * s[:, 2]] for t in ang])
    V = P[ConvexHull(P).vertices]
    x, y = V[:, 0], V[:, 1]
    x2, y2 = np.roll(x, -1), np.roll(y, -1)
    cr = x * y2 - x2 * y
    area = cr.sum() / 2
    hx = ((x + x2) * cr).sum() / (6 * area)
    hy = ((y + y2) * cr).sum() / (6 * area)
    return float(np.sqrt(abs(area))), float(hx - (P[:, 0].min() + P[:, 0].max()) / 2), float(hy - (P[:, 1].min() + P[:, 1].max()) / 2)


# ------------------------------------------------------------------ composition

def bare_inner(bare_svg_text):
    """Everything inside the bare export's root, minus its title and desc."""
    s = bare_svg_text.split("?>", 1)[-1]
    inner = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    inner = re.sub(r"\s*<title>.*?</title>", "", inner, flags=re.S)
    inner = re.sub(r"\s*<desc>.*?</desc>", "", inner, flags=re.S)
    return inner.strip("\n")


def transform_attr(shape, a=1.0, dx=0.0, factor=None):
    f = C.TILE_FACTORS[shape] if factor is None else factor
    fa = f * a
    return f"matrix({S.fmt(fa, 6)} 0 0 {S.fmt(fa, 6)} {S.fmt(64 * (1 - fa) + f * dx)} {S.fmt(64 * (1 - fa))})"


def tile_svg(bare_svg_text, row, shape, tile, colour_mode, factor=None, optics=None):
    """One tile: the shape first, then the bare export's inner markup in one group
    with one uniform transform. optics = (a, dx, k) overrides the icon's own
    optical scale, offset and stroke multiplier (the calibration board uses it)."""
    icon_id, label = row["id"], row["label"]
    f = C.TILE_FACTORS[shape] if factor is None else factor
    a, dx, k = C.tile_optics(icon_id, row["stroke_units"]) if optics is None else optics
    ground = C.CHARCOAL if tile == "charcoal" else C.NEWSPRINT
    shape_name = {"square": "square", "rounded": "rounded square (superellipse, exponent 5)", "circle": "circle"}[shape]
    ink = ("Newsprint lines with a Pillar Red accent" if colour_mode == "two-color" else "Newsprint lines") if tile == "charcoal" else \
          ("Charcoal lines with a Pillar Red accent" if colour_mode == "two-color" else "Charcoal lines")
    rid = C.tile_root(icon_id, shape, tile, colour_mode)
    broot = S.root_id_of(bare_svg_text)
    inner = scale_strokes(bare_inner(bare_svg_text), k).replace(broot, rid)
    how = f"The icon is its bare export scaled by {S.fmt(f * a, 6)} about the center of the 128 box"
    if dx:
        how += f" and moved {S.fmt(abs(f * dx), 4)} units {'right' if dx > 0 else 'left'}"
    if k < 1:
        how += f", with every stroke width multiplied by {S.fmt(k, 4)} so its line stays at {S.fmt(C.TILE_STROKE_CAP, 4)} units or less"
    desc = escape(f"Oath & Action Civic Line {icon_id} {label}: {shape_name} tile in {tile.capitalize()}, {ink}. {how}. "
                  f"The tile shape has data-part 'tile' and the icon group data-part 'icon'.")
    label = escape(label)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" id="{rid}" data-id="{icon_id}" width="128" height="128" viewBox="0 0 128 128">\n'
            f"  <title>{label}</title>\n  <desc>{desc}</desc>\n  {shape_element(shape, ground, rid)}\n"
            f'  <g id="{rid}-icon" data-part="icon" transform="{transform_attr(shape, a, dx, f)}">\n'
            f"{inner}\n  </g>\n</svg>\n")
