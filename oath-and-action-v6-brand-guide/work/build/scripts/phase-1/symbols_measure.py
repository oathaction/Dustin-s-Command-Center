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

# Family specification the consistency check compares against (grid units at 24 px; px at 16 px)
SPEC = {
    "A": {"node_r": {24: 2.0, 16: 1.5}, "seat_w": {24: 1.0, 16: 1.0}, "stroke": 2, "caps": "square or butt", "joins": "miter", "corner": 0},
    "B": {"node_r": {24: 3.0, 16: 2.0}, "seat_w": {24: 1.0, 16: 1.0}, "stroke": 2, "caps": "round", "joins": "round", "corner": 2},
}
# Declared exceptions, shown on the board and counted as consistency failures
EXCEPTIONS = {
    ("A", "line", "act", 16): "Node drawn as a 2 px square in the leaf counter; a 3 px dot with a seat does not fit a 2 px outline",
    ("B", "line", "act", 16): "Node drawn at 2.5 px; the 4 px B node does not fit the leaf counter",
    ("A", "line", "explain", 16): "Node sits in the counter without a seat; the outline already gives the clearance",
    ("A", "line", "connect", 16): "Node sits in the counter without a seat; the arcs already give the clearance",
    ("B", "filled", "explain", 16): "Node held at 3 px with a 1 px seat, as in A; a 4 px B node closes the gap to the lifted square",
    ("B", "filled", "track", 16): "Node held at 3 px with a 1 px seat, as in A; a 4 px B node removes the middle step",
    ("B", "filled", "act", 16): "Node held at 2 px; the 6 px leaf cannot hold a 4 px node with a gap",
    ("A", "filled", "act", 16): "Node held at 2 px with a 1 px seat; the 6 px leaf cannot hold a 3 px dot with a rim",
    ("A", "tile", "act", 16): "Tile micro drawing reuses the 16 px filled master at 10 px, so the node falls below 2 px",
    ("B", "tile", "act", 16): "Tile micro drawing reuses the 16 px filled master at 10 px, so the node falls below 2 px",
}


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
        parts.append(f'<path d="{d_of(lay["node"])}" fill="{node_color or knock}"/>')
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
    """Axis-aligned line segments and all-curve contours (dots, seats) on whole pixels."""
    total = ok = 0
    curves = curves_ok = 0
    off = []
    for key in ("body", "node"):
        path = lay[key]
        segs = list(path.segments)
        contour = []
        cur = None
        for verb, pts in segs:
            if verb == "moveTo":
                contour = [("M", pts[0])]
                cur = pts[0]
            elif verb == "lineTo":
                p = pts[0]
                if abs(p[0] - cur[0]) < 1e-6 or abs(p[1] - cur[1]) < 1e-6:
                    c = p[1] if abs(p[1] - cur[1]) < 1e-6 else p[0]
                    if abs(p[0] - cur[0]) > 1e-6 or abs(p[1] - cur[1]) > 1e-6:
                        total += 1
                        good = abs(c - round(c)) < 0.02
                        ok += good
                        if not good:
                            off.append(f"{'H' if abs(p[1] - cur[1]) < 1e-6 else 'V'} edge at {c:.2f}")
                contour.append(("L", p))
                cur = p
            elif verb in ("curveTo", "qCurveTo"):
                contour.append(("C", pts[-1]))
                cur = pts[-1]
            elif verb in ("closePath", "endPath"):
                if contour and all(k in ("M", "C") for k, _ in contour) and len(contour) > 2:
                    xs = [q[0] for _, q in contour]
                    ys = [q[1] for _, q in contour]
                    curves += 1
                    ext = [min(xs), max(xs), min(ys), max(ys)]
                    good = all(abs(v - round(v)) < 0.06 for v in ext)
                    curves_ok += good
                    if not good:
                        off.append("round contour " + ",".join(f"{v:.2f}" for v in ext))
                contour = []
    return {"axis_edges": total, "on_grid": ok, "curves": curves, "curves_on_grid": curves_ok,
            "share": round((ok + curves_ok) / (total + curves), 2) if (total + curves) else None, "off": off[:4]}


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
        jobs.append({"id": f"w-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": svg_layers(lay, sz, "#000000", WHITE)})
        if sz in (16, 24):
            jobs.append({"id": f"n-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": svg_layers(lay, sz, CHAR, NEWS)})
            jobs.append({"id": f"k-{d}-{t}-{p}-{sz}", "w": sz, "h": sz, "bg": CHAR, "html": svg_layers(lay, sz, NEWS, CHAR)})
        if p == "act" and t != "tile" and sz in (24, 48):
            for sname, bg, ink in SURFACES[:3]:
                nc, sc = accent_for(sname)
                jobs.append({"id": f"r-{d}-{t}-{p}-{sz}-{sname}", "w": sz, "h": sz, "bg": bg, "html": svg_layers(lay, sz, ink, bg, nc, sc)})
    for (n, sz), lay in topics.items():
        jobs.append({"id": f"w-topic-{n}-{sz}", "w": sz, "h": sz, "bg": WHITE, "html": svg_layers(lay, sz, "#000000", WHITE)})
        jobs.append({"id": f"n-topic-{n}-{sz}", "w": sz, "h": sz, "bg": NEWS, "html": svg_layers(lay, sz, CHAR, NEWS)})
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
                cc = load_cov(R / f"{'n' if pol == 'dark_on_light' else 'k'}-{d}-{t}-{p}-{sz}.png", bg, fg)
                if t == "tile":
                    # on a tile the mark is the knocked colour: measure the inverse inside the plate
                    cc = [[1 - v for v in r] for r in cc]
                mask = [[v > .5 for v in r] for r in cc]
                lab, sizes = components(mask)
                b = lay["node"].bounds
                nx, ny = int((b[0] + b[2]) / 2), int((b[1] + b[3]) / 2)
                comp = lab[min(sz - 1, ny)][min(sz - 1, nx)]
                node_area = max(1.0, (b[2] - b[0]) * (b[3] - b[1]) * math.pi / 4)
                sep[pol] = bool(comp) and sizes.get(comp, 0) <= node_area * 2.2
            row["node_separate"] = sep
        res["marks"][key] = row
    # pillar pairs per direction and treatment
    for d in F.DIRECTIONS:
        for t in F.TREATMENTS:
            for sz in (16, 24):
                for a, b in combinations(F.PILLARS, 2):
                    res["pairs"][f"{d}|{t}|{a}|{b}|{sz}"] = sim(cw(f"w-{d}-{t}-{a}-{sz}"), cw(f"w-{d}-{t}-{b}-{sz}"))
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
                cc = load_cov(R / f"n-topic-{n}-{sz}.png", NEWS, CHAR)
                mask = [[v > .5 for v in r] for r in cc]
                lab, sizes = components(mask)
                b = lay["node"].bounds
                comp = lab[int((b[1] + b[3]) / 2)][int((b[0] + b[2]) / 2)]
                res["topics"][f"metrics|{n}|{sz}"]["node_separate"] = bool(comp) and sizes.get(comp, 0) <= max(1, (b[2] - b[0]) ** 2 * math.pi / 4) * 2.2
    # red node edge contrast on rendered pixels
    for d in F.DIRECTIONS:
        for t in ("filled", "line"):
            for sz in (24, 48):
                for sname, bg, ink in SURFACES[:3]:
                    img = Image.open(R / f"r-{d}-{t}-act-{sz}-{sname}.png").convert("RGB")
                    px = img.load()
                    red = hexrgb(RED)
                    reds = [(x, y) for y in range(img.height) for x in range(img.width) if sum(abs(px[x, y][i] - red[i]) for i in range(3)) < 30]
                    edge = []
                    for (x, y) in reds:
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            xx, yy = x + dx, y + dy
                            if 0 <= xx < img.width and 0 <= yy < img.height and (xx, yy) not in reds:
                                q = px[xx, yy]
                                if sum(abs(q[i] - red[i]) for i in range(3)) > 120:
                                    edge.append(contrast_rgb(red, q))
                    edge.sort()
                    res["red"][f"{d}|{t}|{sz}|{sname}"] = {"red_px": len(reds), "edge_min": round(edge[0], 2) if edge else None,
                                                          "edge_median": round(edge[len(edge) // 2], 2) if edge else None,
                                                          "edge_px": len(edge)}
    # palette ratios used by the marks
    for sname, bg, ink in SURFACES:
        res["contrast"][f"ink|{sname}"] = round(contrast(ink, bg), 2)
    res["contrast"]["red|charcoal"] = round(contrast(RED, CHAR), 2)
    res["contrast"]["red|newsprint"] = round(contrast(RED, NEWS), 2)
    res["contrast"]["red|white"] = round(contrast(RED, WHITE), 2)
    res["contrast"]["red|prussian"] = round(contrast(RED, PRUS), 2)
    res["spec"] = SPEC
    res["exceptions"] = {"|".join(map(str, k)): v for k, v in EXCEPTIONS.items()}

    # magnified-view PNGs on Newsprint, copied next to the board
    for f in R.glob("n-*.png"):
        Image.open(f).save(PX / f.name)
    (OUT / "20261021_Symbol-Family-Measurements.json").write_text(json.dumps(res, indent=1))
    write_sprites(marks, topics)
    print("measured", len(jobs), "renders")


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
