"""Render and measure the Phase 1 symbol family sketches (design director).

Run: python3 -I symbols_measure.py
Writes:
  work/boards/phase-1/symbols/20261021_Symbol-Family-Measurements.json
  work/boards/phase-1/symbols/px/*.png          1x renders on Newsprint for the magnified views
  work/boards/phase-1/symbols/*.svg             the sketch masters as SVG sprites
Every raster comes from Chromium at device scale 1 (symbols_render_cells.js).
"""
import base64
import json
import math
import re
import subprocess
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _p in ("/root/.local/lib/python3.13/site-packages",):
    if _p not in sys.path:
        sys.path.append(_p)

import symbols_family as F  # noqa: E402
from symbols_geom import circle, d_of, poly, rect, stroke_path, transform, union  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = HERE.parents[3]
SPRITE = ROOT / "work/extract/v5-polished/sprite"
FONTS = ROOT / "work/extract/v5-polished/fonts"
OUT = ROOT / "work/boards/phase-1/symbols"
PX = OUT / "px"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/symbols")
RENDER = HERE / "symbols_render_cells.js"

NEWS, CHAR, WHITE, PRUS, RED, STONE, VERD = "#DCD9D2", "#121212", "#FFFFFF", "#1F2D5A", "#E63946", "#5D636D", "#4A7C74"
SURFACES = [("newsprint", NEWS, CHAR), ("white", WHITE, CHAR), ("charcoal", CHAR, NEWS), ("prussian", PRUS, NEWS)]
SIZES = [16, 24, 48, 96]

# Family specification the consistency check compares against.
# Node radius in px at each master size, and the clear ring (seat or gap) around it.
SPEC = {
    "A": {"label": "Geometric solid", "node_r": {"24": 2.0, "16 filled": 1.5, "16 line": 2.0}, "ring": 1.0,
          "stroke": "2 px line treatment", "caps": "butt or square", "joins": "miter", "corner": "0 (square)"},
    "B": {"label": "Line with one accent", "node_r": {"24": 3.0, "16 filled": 1.5, "16 line": 2.0}, "ring": 1.0,
          "stroke": "2 px", "caps": "round", "joins": "round", "corner": "2 px at 24, 1.5 px at 16"},
}
# Declared exceptions, shown on the board and counted as consistency failures
EXCEPTIONS = {
    ("A", "filled", "act", 16): "Handle drawn at 2 px with a 1 px seat; the 6 px leaf cannot hold a 3 px dot with a rim",
    ("B", "filled", "act", 16): "Handle drawn at 2 px with a 1 px seat; the 6 px leaf cannot hold a 3 px dot with a rim",
    ("A", "line", "act", 16): "Handle drawn as a 2 px square in the leaf counter; a 4 px node does not fit a 2 px outline",
    ("B", "line", "act", 16): "Handle drawn as a 2 px dot in the leaf counter; a 4 px node does not fit a 2 px outline",
    ("A", "tile", "explain", 16): "16 px tile holds a 10 px micro drawing; its node is a 2 px square with no seat",
    ("A", "tile", "track", 16): "16 px tile holds a 10 px micro drawing; its node is a 2 px square with no seat",
    ("A", "tile", "act", 16): "16 px tile holds a 10 px micro drawing; the handle is a 2 px hole in the leaf",
    ("B", "tile", "explain", 16): "16 px tile holds the shared 10 px micro drawing, so B loses its round terminals",
    ("B", "tile", "track", 16): "16 px tile holds the shared 10 px micro drawing, so B loses its round terminals",
    ("B", "tile", "connect", 16): "16 px tile holds the shared 10 px micro drawing; the node bridges a 2 px divide",
    ("A", "tile", "connect", 16): "16 px tile holds a 10 px micro drawing; the node bridges a 2 px divide with no seat",
    ("B", "tile", "act", 16): "16 px tile holds the shared 10 px micro drawing; the handle is a 2 px hole in the leaf",
    ("A", "tile", "act", 24): "24 px tile holds the 16 px Act master, so the handle is 2 px",
    ("B", "tile", "act", 24): "24 px tile holds the 16 px Act master, so the handle is 2 px",
}


def expected_node(d, t, p, sz):
    if t == "tile":
        if sz == 16:
            return None
        inner = "filled" if d == "A" else "line"
        return SPEC[d]["node_r"][f"16 {inner}"]
    if sz == 16:
        return SPEC[d]["node_r"][f"16 {t}"]
    return SPEC[d]["node_r"]["24"]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in hexrgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def contrast_rgb(a, b):
    return contrast("#%02X%02X%02X" % a, "#%02X%02X%02X" % b)


# ------------------------------------------------------------------ svg serialisation

def svg_layers(lay, size, ink, surface, node_color=None, seat_color=None, vb=None):
    vb = vb or size
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {vb} {vb}">']
    if "plate" in lay:
        parts.append(f'<path d="{d_of(lay["plate"])}" fill="{ink}"/>')
        knock = surface
        parts.append(f'<path d="{d_of(lay["body"])}" fill="{knock}"/>')
        if seat_color:
            parts.append(f'<path d="{d_of(lay["seat"])}" fill="{seat_color}"/>')
        parts.append(f'<path d="{d_of(lay["node"])}" fill="{node_color or (ink if lay.get("hole") else knock)}"/>')
    else:
        parts.append(f'<path d="{d_of(lay["body"])}" fill="{ink}"/>')
        if seat_color:
            parts.append(f'<path d="{d_of(lay["seat"])}" fill="{seat_color}"/>')
        parts.append(f'<path d="{d_of(lay["node"])}" fill="{node_color or ink}"/>')
    parts.append("</svg>")
    return "".join(parts)


def accent_for(surface_name):
    """Red node rule: red sits inside an ink ring on light surfaces, in a knocked seat on Charcoal, never on Prussian."""
    if surface_name in ("newsprint", "white"):
        return RED, CHAR
    if surface_name == "charcoal":
        return RED, None
    return None, None


# ------------------------------------------------------------------ reference glyphs for the watch points

def glyph_path(char, font_file, box, field):
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen
    f = TTFont(str(font_file))
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord(char)]
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    x0, y0, x1, y1 = bp.bounds
    s = min(box / (x1 - x0), box / (y1 - y0))
    w, h = (x1 - x0) * s, (y1 - y0) * s
    tx = (field - w) / 2 - x0 * s
    ty = (field - h) / 2 + y1 * s
    pen = SVGPathPen(gs)
    gs[name].draw(pen)
    return f'<path transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f} {-s:.5f})" d="{pen.getCommands()}" fill="#000"/>'


def reference_svgs(size):
    live = size - 2 if size == 16 else size - 4
    tight = FONTS / "Inter-Tight-800-normal.ttf"
    inter = FONTS / "Inter-700-normal.ttf"
    out = {}
    for ch, nm, fnt in (("C", "letter C", tight), ("D", "letter D", tight), ("©", "copyright sign", inter), ("L", "letter L", tight), ("Z", "letter Z", tight)):
        out[nm] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{glyph_path(ch, fnt, live, size)}</svg>'
    s = size / 24
    play = poly((6 * s, 3 * s), (21 * s, 12 * s), (6 * s, 21 * s))
    out["play button"] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}"><path d="{d_of(play)}" fill="#000"/></svg>'
    lights = union(circle(5 * s, 12 * s, 4 * s), circle(12 * s, 12 * s, 4 * s), circle(19 * s, 12 * s, 4 * s), rect(1 * s, 11.5 * s, 22 * s, 1 * s))
    out["status light"] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}"><path d="{d_of(lights)}" fill="#000"/></svg>'
    for nm, sym in (("V5 chain link (pm-connect)", "pm-connect-s" if size <= 24 else "pm-connect"), ("V5 outbound arrow (pm-act)", "pm-act-s" if size <= 24 else "pm-act"),
                    ("outbound arrow (ui-external)", "ui-external"), ("Signal Grid lockmark", "lockmark")):
        out[nm] = v5_svg(sym, size, mono=True)
    return out


def v5_svg(name, size, mono=False):
    s = (SPRITE / f"{name}.svg").read_text()
    s = re.sub(r"<title>.*?</title>", "", s)
    css = "--pc:currentColor;--dot:currentColor;--link:currentColor;--lever:currentColor;" if mono else ""
    return re.sub(r'<svg ([^>]*?)style="color:#121212"', lambda m: f'<svg {m.group(1)}width="{size}" height="{size}" style="color:#000;{css}"', s, count=1)


# ------------------------------------------------------------------ raster metrics

def load_cov(path, bg, fg):
    img = Image.open(path).convert("RGB")
    b, f = hexrgb(bg), hexrgb(fg)
    d = [f[i] - b[i] for i in range(3)]
    dd = sum(v * v for v in d)
    px = img.load()
    return [[max(0.0, min(1.0, sum((px[x, y][i] - b[i]) * d[i] for i in range(3)) / dd)) for x in range(img.width)] for y in range(img.height)]


def crisp(c):
    ink = [v for row in c for v in row if v > 0.1]
    return (round(sum(v > 0.9 for v in ink) / len(ink), 2) if ink else None), round(sum(map(sum, c)) / (len(c) * len(c[0])), 3)


def silhouette(mask):
    h, w = len(mask), len(mask[0])
    seen = [[False] * w for _ in range(h)]
    st = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while st:
        x, y = st.pop()
        if 0 <= x < w and 0 <= y < h and not seen[y][x] and not mask[y][x]:
            seen[y][x] = True
            st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [[mask[y][x] or not seen[y][x] for x in range(w)] for y in range(h)]


def iou(a, b):
    i = sum(1 for y in range(len(a)) for x in range(len(a[0])) if a[y][x] and b[y][x])
    u = sum(1 for y in range(len(a)) for x in range(len(a[0])) if a[y][x] or b[y][x])
    return i / u if u else 0


def blur(c):
    h, w = len(c), len(c[0])
    return [[sum(c[yy][xx] for yy in range(max(0, y - 1), min(h, y + 2)) for xx in range(max(0, x - 1), min(w, x + 2))) / 9 for x in range(w)] for y in range(h)]


def corr(a, b):
    fa = [v for r in a for v in r]
    fb = [v for r in b for v in r]
    ma, mb = sum(fa) / len(fa), sum(fb) / len(fb)
    num = sum((x - ma) * (y - mb) for x, y in zip(fa, fb))
    den = math.sqrt(sum((x - ma) ** 2 for x in fa) * sum((y - mb) ** 2 for y in fb))
    return num / den if den else 0


def sim(ca, cb):
    s_iou = iou(silhouette([[v > .5 for v in r] for r in ca]), silhouette([[v > .5 for v in r] for r in cb]))
    b = corr(blur(ca), blur(cb))
    return {"silhouette_iou": round(s_iou, 2), "blurred_corr": round(b, 2), "score": round((s_iou + b) / 2, 3)}


def components(mask):
    h, w = len(mask), len(mask[0])
    lab = [[0] * w for _ in range(h)]
    n = 0
    sizes = {}
    for y in range(h):
        for x in range(w):
            if mask[y][x] and not lab[y][x]:
                n += 1
                st = [(x, y)]
                lab[y][x] = n
                cnt = 0
                while st:
                    a, b = st.pop()
                    cnt += 1
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = a + dx, b + dy
                        if 0 <= xx < w and 0 <= yy < h and mask[yy][xx] and not lab[yy][xx]:
                            lab[yy][xx] = n
                            st.append((xx, yy))
                sizes[n] = cnt
    return lab, sizes


# ------------------------------------------------------------------ vector checks

def pixel_fit(lay):
    """Pixel-fit test for 16 and 24 px masters.

    1. Every axis-aligned straight edge lies on a whole pixel.
    2. Every horizontal or vertical tangent of the node, and of every body curve with a
       radius of 2.4 px or more (discs, arcs, seats), lies on a whole pixel. Tighter
       curves (round caps, round joins and corner fillets) are exempt: their tangents
       meet straight edges that the first test already checks, and a cap at the end of a
       diagonal arc cannot land on the grid.
    Diagonal straight edges are exempt.
    """
    from symbols_geom import flatten_segments
    total = ok = 0
    off = []
    seen = set()
    for key in ("body", "node", "plate"):
        if key not in lay:
            continue
        for seg in flatten_segments(lay[key]):
            if seg[0] == "L":
                (x0, y0), (x1, y1) = seg[1], seg[2]
                if abs(x0 - x1) < 1e-6 and abs(y0 - y1) > 1e-6:
                    c = x0
                elif abs(y0 - y1) < 1e-6 and abs(x0 - x1) > 1e-6:
                    c = y0
                else:
                    continue
                total += 1
                good = abs(c - round(c)) < 0.02
                ok += good
                if not good:
                    off.append(f"straight edge at {c:.2f}")
            elif seg[0] in ("C", "Q"):
                pts = seg[1:]
                for i in range(0, 65):
                    t = i / 64
                    x, y, dx, dy, ddx, ddy = _bez(pts, t)
                    sp = math.hypot(dx, dy)
                    if sp < 1e-9:
                        continue
                    curv = abs(dx * ddy - dy * ddx) / sp ** 3
                    radius = 1 / curv if curv > 1e-9 else 1e9
                    if key == "body" and radius < 2.4:
                        continue
                    for coord, deriv in ((x, dx), (y, dy)):
                        if abs(deriv) / sp < 0.02:
                            k = (round(x, 1), round(y, 1))
                            if k in seen:
                                continue
                            seen.add(k)
                            total += 1
                            good = abs(coord - round(coord)) < 0.06
                            ok += good
                            if not good:
                                off.append(f"curve tangent at {coord:.2f} (r {radius:.1f})")
    return {"checked": total, "on_grid": ok, "share": round(ok / total, 2) if total else None, "off": off[:4]}


def _bez(pts, t):
    if len(pts) == 4:
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
        mt = 1 - t
        x = mt ** 3 * x0 + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x3
        y = mt ** 3 * y0 + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * y3
        dx = 3 * mt * mt * (x1 - x0) + 6 * mt * t * (x2 - x1) + 3 * t * t * (x3 - x2)
        dy = 3 * mt * mt * (y1 - y0) + 6 * mt * t * (y2 - y1) + 3 * t * t * (y3 - y2)
        ddx = 6 * mt * (x2 - 2 * x1 + x0) + 6 * t * (x3 - 2 * x2 + x1)
        ddy = 6 * mt * (y2 - 2 * y1 + y0) + 6 * t * (y3 - 2 * y2 + y1)
        return x, y, dx, dy, ddx, ddy
    (x0, y0), (x1, y1), (x2, y2) = pts
    mt = 1 - t
    x = mt * mt * x0 + 2 * mt * t * x1 + t * t * x2
    y = mt * mt * y0 + 2 * mt * t * y1 + t * t * y2
    dx = 2 * mt * (x1 - x0) + 2 * t * (x2 - x1)
    dy = 2 * mt * (y1 - y0) + 2 * t * (y2 - y1)
    return x, y, dx, dy, 2 * (x2 - 2 * x1 + x0), 2 * (y2 - 2 * y1 + y0)


def node_metrics(lay):
    b = lay["node"].bounds
    nr = round((b[2] - b[0]) / 2, 2)
    sb = lay["seat"].bounds if list(lay["seat"].segments) else None
    seat_w = round(((sb[2] - sb[0]) - (b[2] - b[0])) / 2, 2) if sb else 0.0
    return nr, seat_w


# ------------------------------------------------------------------ main

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PX.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jobs = []
    marks = {}
    for d in F.DIRECTIONS:
        for t in F.TREATMENTS:
            for p in F.PILLARS:
                for sz in SIZES:
                    marks[(d, t, p, sz)] = F.draw(p, d, t, sz)
    topics = {(n, sz): F.topic(n, sz) for n in F.TOPICS for sz in (16, 24, 48)}

    # measurement renders: black on white
    for (d, t, p, sz), lay in marks.items():
        mark_only = markonly(lay)
        jobs.append({"id": f"w-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": svg_layers(mark_only, sz, "#000000", WHITE)})
        if sz in (16, 24):
            jobs.append({"id": f"n-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": svg_layers(lay, sz, CHAR, NEWS)})
            jobs.append({"id": f"mn-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": svg_layers(mark_only, sz, CHAR, NEWS)})
            jobs.append({"id": f"k-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": CHAR, "html": svg_layers(mark_only, sz, NEWS, CHAR)})
        if p == "act" and t != "tile" and sz in (24, 48):
            for sname, bg, ink in SURFACES[:3]:
                nc, sc = accent_for(sname)
                jobs.append({"id": f"r-{d}-{t}-{p}-{sz}-{sname}", "w": sz, "h": sz, "bg": bg, "html": svg_layers(lay, sz, ink, bg, nc, sc)})
    for (n, sz), lay in topics.items():
        jobs.append({"id": f"w-topic-{n}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": svg_layers(lay, sz, "#000000", WHITE)})
        jobs.append({"id": f"n-topic-{n}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": svg_layers(lay, sz, CHAR, NEWS)})
        jobs.append({"id": f"k-topic-{n}-{sz}", "w": sz, "h": sz, "bg": CHAR, "html": svg_layers(lay, sz, NEWS, CHAR)})
        v5 = v5_svg(f"ic-{n}-{sz}", sz, mono=True).replace('style="color:#000;', 'style="color:#000000;')
        jobs.append({"id": f"w-v5topic-{n}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": v5})
        jobs.append({"id": f"n-v5topic-{n}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": v5_svg(f"ic-{n}-{sz}", sz, mono=True).replace("color:#000;", "color:#121212;")})
    for p in F.PILLARS:
        for sz in (16, 24, 96):
            nm = f"pm-{p}-s" if sz <= 24 else f"pm-{p}"
            jobs.append({"id": f"w-v5-{p}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": v5_svg(nm, sz, mono=True)})
            if sz != 96:
                jobs.append({"id": f"n-v5-{p}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": v5_svg(nm, sz, mono=True).replace("color:#000;", "color:#121212;")})
    refs = {sz: reference_svgs(sz) for sz in (16, 24)}
    for sz, rr in refs.items():
        for nm, svg in rr.items():
            jobs.append({"id": f"w-ref-{slug(nm)}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": svg})
            jobs.append({"id": f"n-ref-{slug(nm)}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": svg.replace('fill="#000"', f'fill="{CHAR}"').replace("color:#000;", "color:#121212;")})
    jp = SCRATCH / "jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(RENDER), str(jp), str(SCRATCH / "r")], check=True)
    R = SCRATCH / "r"

    def cw(id_, bg=WHITE, fg="#000000"):
        return load_cov(R / f"{id_}.png", bg, fg)

    res = {"marks": {}, "pairs": {}, "watch": {}, "topics": {}, "v5": {}, "red": {}, "contrast": {}}
    # per drawing
    for (d, t, p, sz), lay in marks.items():
        key = f"{d}|{t}|{p}|{sz}"
        c = cw(f"w-{d}-{t}-{p}-{sz}")
        cr, dens = crisp(c)
        tot = sum(map(sum, c)) or 1
        cx = sum(c[y][x] * x for y in range(sz) for x in range(sz)) / tot
        cy = sum(c[y][x] * y for y in range(sz) for x in range(sz)) / tot
        row = {"crisp": cr, "density": dens, "centroid": [round((cx + .5) / sz - .5, 3), round((cy + .5) / sz - .5, 3)]}
        if sz in (16, 24):
            row["pixel_fit"] = pixel_fit(lay)
            nr, sw = node_metrics(lay)
            row["node_r"], row["seat_w"] = nr, sw
            # monochrome: node separated from body, dark on light and light on dark
            sep = {}
            for pol, bg, fg in (("dark_on_light", NEWS, CHAR), ("light_on_dark", CHAR, NEWS)):
                cc = load_cov(R / f"{'mn' if pol == 'dark_on_light' else 'k'}-{d}-{t}-{p}-{sz}.png", bg, fg)
                mask = [[v > .5 for v in r] for r in cc]
                b = lay["node"].bounds
                nx, ny = int((b[0] + b[2]) / 2), int((b[1] + b[3]) / 2)
                if lay.get("hole"):
                    # a hole-style handle: background at its centre, ink on all four sides
                    sep[pol] = (not mask[ny][nx]) and all(mask[ny + dy][nx + dx] for dx, dy in ((-2, 0), (1, 0), (0, -2), (0, 1)))
                    continue
                lab, sizes = components(mask)
                comp = lab[min(sz - 1, ny)][min(sz - 1, nx)]
                node_area = max(1.0, (b[2] - b[0]) * (b[3] - b[1]) * math.pi / 4)
                sep[pol] = bool(comp) and sizes.get(comp, 0) <= node_area * 2.2
            row["node_separate"] = sep
        res["marks"][key] = row
    # pillar pairs per direction and treatment
    def crop(c, sz):
        lo, hi = (3, 13) if sz == 16 else (4, 20)
        return [row[lo:hi] for row in c[lo:hi]]
    for d in F.DIRECTIONS:
        for t in F.TREATMENTS:
            for sz in (16, 24):
                for a, b in combinations(F.PILLARS, 2):
                    ca, cb = cw(f"w-{d}-{t}-{a}-{sz}"), cw(f"w-{d}-{t}-{b}-{sz}")
                    if t == "tile":
                        ca, cb = crop(ca, sz), crop(cb, sz)
                    res["pairs"][f"{d}|{t}|{a}|{b}|{sz}"] = sim(ca, cb)
    for sz in (16, 24):
        for a, b in combinations(F.PILLARS, 2):
            res["pairs"][f"V5|current|{a}|{b}|{sz}"] = sim(cw(f"w-v5-{a}-{sz}"), cw(f"w-v5-{b}-{sz}"))
    # watch points
    WATCH = {"track": ["status light", "Signal Grid lockmark"], "act": ["letter D", "play button", "outbound arrow (ui-external)", "V5 outbound arrow (pm-act)"],
             "explain": ["copyright sign", "letter C", "letter L"], "connect": ["V5 chain link (pm-connect)", "copyright sign"]}
    for d in F.DIRECTIONS:
        for t in F.TREATMENTS:
            for p, names in WATCH.items():
                for nm in names:
                    for sz in (16, 24):
                        res["watch"][f"{d}|{t}|{p}|{nm}|{sz}"] = sim(cw(f"w-{d}-{t}-{p}-{sz}"), cw(f"w-ref-{slug(nm)}-{sz}"))
    for p, names in WATCH.items():
        for nm in names:
            for sz in (16, 24):
                res["watch"][f"V5|current|{p}|{nm}|{sz}"] = sim(cw(f"w-v5-{p}-{sz}"), cw(f"w-ref-{slug(nm)}-{sz}"))
    # V5 pillar baseline metrics
    for p in F.PILLARS:
        for sz in (16, 24, 96):
            cr, dens = crisp(cw(f"w-v5-{p}-{sz}"))
            res["v5"][f"{p}|{sz}"] = {"crisp": cr, "density": dens}
    # topics
    for sz in (16, 24):
        for a, b in combinations(F.TOPICS, 2):
            res["topics"][f"new|{a}|{b}|{sz}"] = sim(cw(f"w-topic-{a}-{sz}"), cw(f"w-topic-{b}-{sz}"))
            res["topics"][f"v5|{a}|{b}|{sz}"] = sim(cw(f"w-v5topic-{a}-{sz}"), cw(f"w-v5topic-{b}-{sz}"))
        for a in F.TOPICS:
            res["topics"][f"vsold|{a}|{sz}"] = sim(cw(f"w-topic-{a}-{sz}"), cw(f"w-v5topic-{a}-{sz}"))
            for p in F.PILLARS:
                res["topics"][f"vspillar|{a}|{p}|{sz}"] = sim(cw(f"w-topic-{a}-{sz}"), cw(f"w-A-filled-{p}-{sz}"))
    for n in F.TOPICS:
        for sz in (16, 24, 48):
            cr, dens = crisp(cw(f"w-topic-{n}-{sz}"))
            cr5, dens5 = crisp(cw(f"w-v5topic-{n}-{sz}"))
            res["topics"][f"metrics|{n}|{sz}"] = {"crisp": cr, "density": dens, "v5_crisp": cr5, "v5_density": dens5}
            if sz in (16, 24):
                res["topics"][f"metrics|{n}|{sz}"]["pixel_fit"] = pixel_fit(topics[(n, sz)])
                lay = topics[(n, sz)]
                b = lay["node"].bounds
                seps = {}
                for pol, pre, bg, fg in (("dark_on_light", "n", NEWS, CHAR), ("light_on_dark", "k", CHAR, NEWS)):
                    cc = load_cov(R / f"{pre}-topic-{n}-{sz}.png", bg, fg)
                    mask = [[v > .5 for v in r] for r in cc]
                    lab, sizes = components(mask)
                    comp = lab[int((b[1] + b[3]) / 2)][int((b[0] + b[2]) / 2)]
                    seps[pol] = bool(comp) and sizes.get(comp, 0) <= max(1, (b[2] - b[0]) ** 2 * math.pi / 4) * 2.2
                res["topics"][f"metrics|{n}|{sz}"]["node_separate"] = seps
                nr, sw = node_metrics(lay)
                res["topics"][f"metrics|{n}|{sz}"]["node_r"] = nr
                res["topics"][f"metrics|{n}|{sz}"]["seat_w"] = sw
    # red node: the colour of the ring band just outside the node, on rendered pixels
    for d in F.DIRECTIONS:
        for t in ("filled", "line"):
            for sz in (24, 48):
                lay = marks[(d, t, "act", sz)]
                b = lay["node"].bounds
                cx, cy, r = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, (b[2] - b[0]) / 2
                ring = (sz / 24) * 1.0
                for sname, bg, ink in SURFACES[:3]:
                    img = Image.open(R / f"r-{d}-{t}-act-{sz}-{sname}.png").convert("RGB")
                    px = img.load()
                    band = []
                    core = []
                    for y in range(img.height):
                        for x in range(img.width):
                            dist = math.hypot(x + .5 - cx, y + .5 - cy)
                            if r + 0.15 * ring <= dist <= r + 0.85 * ring:
                                band.append(px[x, y])
                            if dist <= r - 0.7:
                                core.append(px[x, y])
                    lumsort = sorted(band, key=lambda q: lum("#%02X%02X%02X" % q))
                    med = lumsort[len(lumsort) // 2] if lumsort else None
                    corec = sorted(core, key=lambda q: lum("#%02X%02X%02X" % q))[len(core) // 2] if core else None
                    res["red"][f"{d}|{t}|{sz}|{sname}"] = {
                        "core": "#%02X%02X%02X" % corec if corec else None,
                        "ring_median": "#%02X%02X%02X" % med if med else None,
                        "ring_vs_red": round(contrast_rgb(hexrgb(RED), med), 2) if med else None,
                        "ring_vs_surface": round(contrast_rgb(med, hexrgb(bg)), 2) if med else None,
                        "band_px": len(band)}
    # palette ratios used by the marks
    for sname, bg, ink in SURFACES:
        res["contrast"][f"ink|{sname}"] = round(contrast(ink, bg), 2)
    res["contrast"]["red|charcoal"] = round(contrast(RED, CHAR), 2)
    res["contrast"]["red|newsprint"] = round(contrast(RED, NEWS), 2)
    res["contrast"]["red|white"] = round(contrast(RED, WHITE), 2)
    res["contrast"]["red|prussian"] = round(contrast(RED, PRUS), 2)
    res["spec"] = SPEC
    for (d, t, p, sz) in marks:
        if sz in (16, 24):
            row = res["marks"][f"{d}|{t}|{p}|{sz}"]
            exp = expected_node(d, t, p, sz)
            row["node_expected"] = exp
            exc = EXCEPTIONS.get((d, t, p, sz))
            row["exception"] = exc
            row["consistent"] = (exc is None) and exp is not None and abs(row["node_r"] - exp) < 0.06
    res["exceptions"] = {"|".join(map(str, k)): v for k, v in EXCEPTIONS.items()}

    # magnified-view PNGs on Newsprint, copied next to the board
    for f in R.glob("n-*.png"):
        Image.open(f).save(PX / f.name)
    (OUT / "20261021_Symbol-Family-Measurements.json").write_text(json.dumps(res, indent=1))
    write_sprites(marks, topics)
    print("measured", len(jobs), "renders")


def markonly(lay):
    """The mark without its tile plate. A hole-style node becomes a separate dot cut from the body."""
    if "plate" not in lay:
        return lay
    out = {"body": lay["body"], "seat": lay["seat"], "node": lay["node"]}
    if lay.get("hole"):
        out = {"body": lay["body"], "seat": lay["seat"], "node": F.empty(), "hole": True}
    return out


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def write_sprites(marks, topics):
    """Write the sketch masters as SVG sprites (one per direction, one for topics)."""
    for d in F.DIRECTIONS:
        parts = ['<svg xmlns="http://www.w3.org/2000/svg">', f"<!-- Oath & Action V6, Phase 1 symbol family sketches, Direction {d}. Proposals only, October 21, 2026. "
                 "Layers: body (ink), seat (clear ring), node (hinge node). Not a master. -->"]
        for t in F.TREATMENTS:
            for p in F.PILLARS:
                for sz in ((16, 24) if t != "tile" else (16, 24, 48, 96)):
                    lay = marks[(d, t, p, sz)]
                    parts.append(f'<symbol id="oa-sketch-{d.lower()}-{t}-{p}-{sz}" viewBox="0 0 {sz} {sz}"><title>{p.title()}, Direction {d}, {t}, {sz} px</title>')
                    if "plate" in lay:
                        parts.append(f'<path class="plate" d="{d_of(lay["plate"])}" fill="currentColor"/>')
                        parts.append(f'<path class="body" d="{d_of(lay["body"])}" fill="var(--knock,#DCD9D2)"/>')
                        parts.append(f'<path class="seat" d="{d_of(lay["seat"])}" fill="var(--seat,none)"/>')
                        parts.append(f'<path class="node" d="{d_of(lay["node"])}" fill="var(--node,var(--knock,#DCD9D2))"/>')
                    else:
                        parts.append(f'<path class="body" d="{d_of(lay["body"])}" fill="currentColor"/>')
                        parts.append(f'<path class="seat" d="{d_of(lay["seat"])}" fill="var(--seat,none)"/>')
                        parts.append(f'<path class="node" d="{d_of(lay["node"])}" fill="var(--node,currentColor)"/>')
                    parts.append("</symbol>")
        parts.append("</svg>")
        (OUT / f"20261021_Pillar-Sketches-Direction-{d}.svg").write_text("\n".join(parts))
    parts = ['<svg xmlns="http://www.w3.org/2000/svg">', "<!-- Oath & Action V6, Phase 1 topic grammar proof in Direction A. Proposals only, October 21, 2026. Not a master. -->"]
    for n in F.TOPICS:
        for sz in (16, 24):
            lay = topics[(n, sz)]
            parts.append(f'<symbol id="oa-sketch-topic-{n}-{sz}" viewBox="0 0 {sz} {sz}"><title>{F.TOPIC_LABELS[n]}, Direction A, {sz} px</title>'
                         f'<path class="body" d="{d_of(lay["body"])}" fill="currentColor"/><path class="seat" d="{d_of(lay["seat"])}" fill="var(--seat,none)"/>'
                         f'<path class="node" d="{d_of(lay["node"])}" fill="var(--node,currentColor)"/></symbol>')
    parts.append("</svg>")
    (OUT / "20261021_Topic-Sketches-Direction-A.svg").write_text("\n".join(parts))


if __name__ == "__main__":
    main()
