"""Shared helpers for the Phase 1 identity refinement scripts.

Geometry runs on skia-pathops paths so outlines stay as Bezier curves through every
boolean step. SVG path strings are read with fontTools' SVG parser and written with
its SVGPathPen. Rasters come from Chromium (render_cells_p1.js), never from a home-made
rasteriser, so every number on the board is what a browser draws at device scale 1.

Run scripts that import this with python3 -I; the user site-packages path is appended
below because -I drops it.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

for _p in ("/root/.local/lib/python3.13/site-packages",):
    if _p not in sys.path:
        sys.path.append(_p)

import pathops  # noqa: E402
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402
from fontTools.pens.transformPen import TransformPen  # noqa: E402
from fontTools.pens.boundsPen import BoundsPen  # noqa: E402
from fontTools.svgLib.path import parse_path  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
SPRITE = ROOT / "work/extract/v5-polished/sprite"
FONTS = ROOT / "work/extract/v5-polished/fonts"
OUT = ROOT / "work/boards/phase-1/identity"
HERE = Path(__file__).resolve().parent
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/p1")

RED, CHAR, NEWS, PRUS, STONE, WHITE, VERD = "#E63946", "#121212", "#DCD9D2", "#1F2D5A", "#5D636D", "#FFFFFF", "#4A7C74"
SURFACES = [("newsprint", "Newsprint", NEWS, CHAR), ("white", "White", WHITE, CHAR),
            ("charcoal", "Charcoal", CHAR, NEWS), ("prussian", "Prussian", PRUS, WHITE)]
NUM = r"-?\d*\.?\d+(?:[eE]-?\d+)?"

# Lora Bold ampersand as placed in the V5 wordmark: translate(365.5 104) scale(0.14 -0.14)
AMP_D = re.search(r' d="([^"]+)"', (SPRITE / "amp.svg").read_text()).group(1)


# ---------------------------------------------------------------- colour

def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    a = hexrgb(a) if isinstance(a, str) else a
    b = hexrgb(b) if isinstance(b, str) else b
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- paths

def path_from_d(d, transform=(1, 0, 0, 1, 0, 0)):
    p = pathops.Path()
    pen = TransformPen(p.getPen(), transform)
    parse_path(d, pen)
    return p


def d_from_path(p, nd=2):
    pen = SVGPathPen(None, ntos=lambda v: _fmt(v, nd))
    p.draw(pen)
    return pen.getCommands()


def _fmt(v, nd):
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def tx(p, a=1, b=0, c=0, d=1, e=0, f=0):
    """Affine transform (SVG matrix order a b c d e f) returning a new path."""
    q = pathops.Path()
    pen = TransformPen(q.getPen(), (a, b, c, d, e, f))
    p.draw(pen)
    return q


def union(*paths):
    ps = [p for p in paths if p is not None]
    out = ps[0]
    for p in ps[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def diff(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE)


def inter(a, b):
    return pathops.op(a, b, pathops.PathOp.INTERSECTION)


def simplify(p):
    q = pathops.Path()
    p.draw(q.getPen())
    q.simplify()
    return q


def bounds(p):
    bp = BoundsPen(None)
    p.draw(bp)
    return bp.bounds  # xMin, yMin, xMax, yMax, exact for curves


def embolden(p, delta):
    """Grow (delta > 0) or shrink (delta < 0) an outline by |delta| on every side.
    Uses skia's stroker with round joins, so curves stay curves."""
    if abs(delta) < 1e-9:
        return simplify(p)
    s = pathops.Path()
    p.draw(s.getPen())
    s.stroke(abs(delta) * 2, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    return union(p, s) if delta > 0 else diff(simplify(p), s)


def rect(x0, y0, x1, y1):
    p = pathops.Path()
    p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
    return p


def poly(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def circle(cx, cy, r):
    k = 0.5522847498 * r
    p = pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p


def ring(cx, cy, r_out, r_in):
    return diff(circle(cx, cy, r_out), circle(cx, cy, r_in))


# ---------------------------------------------------------------- sprite reading

def sprite(name):
    return (SPRITE / f"{name}.svg").read_text()


def viewbox(s):
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]


def strip_defs(s):
    if "<defs>" in s:
        s = s[: s.find("<defs>")] + s[s.find("</defs>") + 7:]
    return s


def sprite_paths(name):
    """Every <path> of a sprite symbol as (pathops path, fill attr), transforms applied."""
    s = strip_defs(sprite(name))
    out = []
    for m in re.finditer(r"<path([^>]*)/>", s):
        attrs = m.group(1)
        d = re.search(r' d="([^"]+)"', attrs).group(1)
        t = (1, 0, 0, 1, 0, 0)
        tm = re.search(r'transform="translate\((' + NUM + r") (" + NUM + r")\) scale\((" + NUM + r") (" + NUM + r")\)", attrs)
        if tm:
            a, b, c, e = [float(tm.group(k)) for k in range(1, 5)]
            t = (c, 0, 0, e, a, b)
        out.append(path_from_d(d, t))
    return out


def amp_glyph(tx_=365.5, ty_=104.0, s=0.14):
    """The Lora Bold ampersand outline in wordmark units."""
    return path_from_d(AMP_D, (s, 0, 0, -s, tx_, ty_))


def wordmark_letters():
    """The ten Inter Tight 800 capitals of the V5 wordmark as separate paths, in wordmark units."""
    letters = [p for p in sprite_paths("wordmark")]
    left, amp, right = letters[0], letters[1], letters[2]
    glyphs = []
    for p in (left, right):
        for c in split_glyphs(p):
            glyphs.append(c)
    glyphs.sort(key=lambda g: bounds(g)[0])
    return glyphs, amp


def split_glyphs(p):
    """Group contours into glyphs: a contour whose bounds sit inside another's joins it."""
    cons = []
    for c in p.contours:
        q = pathops.Path()
        c.draw(q.getPen())
        cons.append(q)
    boxes = [bounds(c) for c in cons]
    order = sorted(range(len(cons)), key=lambda k: -(boxes[k][2] - boxes[k][0]) * (boxes[k][3] - boxes[k][1]))
    groups = []
    for k in order:
        b = boxes[k]
        for g in groups:
            gb = g["box"]
            if b[0] >= gb[0] - 0.01 and b[2] <= gb[2] + 0.01 and b[1] >= gb[1] - 0.01 and b[3] <= gb[3] + 0.01:
                g["cons"].append(cons[k])
                break
        else:
            groups.append({"box": b, "cons": [cons[k]]})
    out = []
    for g in groups:
        q = pathops.Path()
        for c in g["cons"]:
            c.draw(q.getPen())
        out.append(q)
    return out


# ---------------------------------------------------------------- geometry measures

def polyline(p, steps=32):
    """Flatten a path into closed polylines (for gap measures only)."""
    polys = []
    cur = []
    last = None
    for verb, pts in p.segments:
        if verb == "moveTo":
            if cur:
                polys.append(cur)
            cur = [pts[0]]
            last = pts[0]
        elif verb == "lineTo":
            cur.append(pts[0]); last = pts[0]
        elif verb == "qCurveTo":
            # pathops gives one off-curve per quad here
            p0 = last
            offs = list(pts[:-1]); end = pts[-1]
            # expand implied on-curves
            seq = [p0]
            for j, o in enumerate(offs):
                seq.append(o)
                if j < len(offs) - 1:
                    nxt = offs[j + 1]
                    seq.append(((o[0] + nxt[0]) / 2, (o[1] + nxt[1]) / 2))
            seq.append(end)
            for j in range(0, len(seq) - 2, 2):
                a, c, b = seq[j], seq[j + 1], seq[j + 2]
                for s in range(1, steps + 1):
                    t = s / steps
                    cur.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
                                (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]))
            last = end
        elif verb == "curveTo":
            c1, c2, e = pts
            a = last
            for s in range(1, steps + 1):
                t = s / steps
                mt = 1 - t
                cur.append((mt ** 3 * a[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * e[0],
                            mt ** 3 * a[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * e[1]))
            last = e
        elif verb == "closePath" or verb == "endPath":
            if cur:
                polys.append(cur)
            cur = []
    if cur:
        polys.append(cur)
    return [q for q in polys if len(q) > 2]


def crossings(polys, y):
    xs = []
    for pl in polys:
        n = len(pl)
        for j in range(n):
            (x1, y1), (x2, y2) = pl[j], pl[(j + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    return sorted(xs)


def pair_gap(pa, pb, cap_top=4.0, base=104.0, step=0.25, depth=20.0):
    """Nearest ink gap and depth-limited area gap (per unit of cap band) between two glyph paths
    placed side by side. Same method as the Phase 0 audit."""
    la, lb = polyline(pa), polyline(pb)
    gaps = []
    y = cap_top + step / 2
    while y < base:
        xa = crossings(la, y)
        xb = crossings(lb, y)
        if xa and xb:
            gaps.append((y, xb[0] - xa[-1]))
        y += step
    gmin = min(g for _, g in gaps)
    ymin = [yy for yy, g in gaps if abs(g - gmin) < 1e-9][0]
    area = sum(min(g, gmin + depth) for _, g in gaps) * step / (base - cap_top)
    return {"min": round(gmin, 2), "min_at_y": round(ymin, 2), "area": round(area, 2)}


# ---------------------------------------------------------------- svg output

def svg_doc(viewbox_, body, title, w=None, h=None, extra=""):
    vb = " ".join(_fmt(v, 2) for v in viewbox_)
    size = f' width="{_fmt(w, 3)}" height="{_fmt(h, 3)}"' if w else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{size}{extra}>'
            f'<title>{title}</title>{body}</svg>')


def write_svg(path, viewbox_, body, title):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg_doc(viewbox_, body, title) + "\n")


# ---------------------------------------------------------------- rendering

def render(jobs, outdir, tag):
    """Render cells with Chromium at device scale 1. jobs: list of dicts with id, w, h, bg, html."""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jp = SCRATCH / f"jobs_{tag}.json"
    jp.write_text(json.dumps(jobs))
    outdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["node", str(HERE / "render_cells_p1.js"), str(jp), str(outdir)], check=True)


def coverage(img, bg, ink):
    """Per-pixel ink coverage estimated by projecting each pixel onto the bg->ink colour line."""
    bgc, inkc = hexrgb(bg), hexrgb(ink)
    d = [inkc[i] - bgc[i] for i in range(3)]
    dd = sum(x * x for x in d) or 1
    px = img.convert("RGB").load()
    out = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            p = px[x, y]
            a = sum((p[i] - bgc[i]) * d[i] for i in range(3)) / dd
            row.append(max(0.0, min(1.0, a)))
        out.append(row)
    return out


def ink_stats(img, bg, ink, box=None):
    """Contrast and solidity of pixels that carry a given ink colour."""
    cov = coverage(img, bg, ink)
    px = img.convert("RGB").load()
    bgc = hexrgb(bg)
    x0, y0, x1, y1 = box or (0, 0, img.width, img.height)
    vals, solid = [], 0
    for y in range(max(0, y0), min(img.height, y1)):
        for x in range(max(0, x0), min(img.width, x1)):
            a = cov[y][x]
            if a > 0.1:
                vals.append(contrast(px[x, y], bgc))
                solid += a >= 0.9
    vals.sort()
    n = len(vals)
    if not n:
        return {"ink_px": 0}
    return {"ink_px": n, "solid_share": round(solid / n, 2), "median_contrast": round(vals[n // 2], 2),
            "max_contrast": round(vals[-1], 2), "share_at_or_above_3": round(sum(v >= 3 for v in vals) / n, 2)}


def overlay_img(a, b, bg_a, ink_a, bg_b, ink_b):
    """Raster overlay of two renders of the same size: both = Charcoal, original only = light Stone,
    proposal only = Verdigris. Returns an RGB image."""
    w, h = max(a.width, b.width), max(a.height, b.height)
    ca, cb = coverage(a, bg_a, ink_a), coverage(b, bg_b, ink_b)
    out = Image.new("RGB", (w, h), hexrgb(WHITE))
    px = out.load()
    o_only = (176, 180, 186)
    p_only = hexrgb(VERD)
    both = hexrgb(CHAR)
    for y in range(h):
        for x in range(w):
            va = ca[y][x] if y < a.height and x < a.width else 0
            vb = cb[y][x] if y < b.height and x < b.width else 0
            m = min(va, vb)
            oa, ob = va - m, vb - m
            col = [255, 255, 255]
            for k in range(3):
                col[k] = round(255 * (1 - m - oa - ob) + both[k] * m + o_only[k] * oa + p_only[k] * ob)
                col[k] = max(0, min(255, col[k]))
            px[x, y] = tuple(col)
    return out


def column_openness(img, bg, ink, x_a, x_b, y_a, y_b):
    """Lightest column between two pixel x positions inside a band: 1 means a full column of background."""
    cov = coverage(img, bg, ink)
    best = 0.0
    for x in range(int(math.floor(x_a)), int(math.ceil(x_b))):
        if 0 <= x < img.width:
            col = [cov[y][x] for y in range(int(y_a), int(math.ceil(y_b))) if 0 <= y < img.height]
            if col:
                best = max(best, 1 - sum(col) / len(col))
    return round(best, 2)
