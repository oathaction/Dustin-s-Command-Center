"""Render and measure the Phase 2 icon concepts (design director, October 28, 2026).

Run: python3 -I icons_measure.py
Writes work/boards/phase-2/icons/20261028_Icon-Concepts-Measurements.json.

Every raster comes from Chromium at device scale 1 (icons_render_cells.js). The checks reuse the
Phase 1 measures in work/build/scripts/phase-1/symbols_measure.py:
  pixel fit      D1-17: at least 60 percent of inked pixels are crisp (coverage over 0.9) at 16
                 and 24 px; also the Phase 1 vector test (straight edges and curve extremes on
                 whole pixels)
  similarity     D1-16 and the Phase 1 practice: mean of filled-silhouette overlap and blurred
                 correlation, under 0.60 for every pair in a set at 16 px
  silhouette     Phase 1: crisp share at least 0.60 and ink at least 25 percent of the field at 16
"""
import json
import math
import subprocess
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parent / "phase-1"
for _p in (str(HERE), str(P1)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import icons_common as C  # noqa: E402
import icons_draw as D  # noqa: E402
import icons_geom as g  # noqa: E402
import numpy as np  # noqa: E402
import symbols_measure as M  # noqa: E402  (Phase 1 measures)
from PIL import Image  # noqa: E402

R = C.SCRATCH / "r"


def mono_svg(lay, size, px, ink="#000000", node=None, only=None):
    node = node or ink
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {size} {size}">']
    if only in (None, "ink"):
        parts.append(f'<path d="{g.d_of(lay["ink"])}" fill="{ink}"/>')
    if only in (None, "node"):
        parts.append(f'<path d="{g.d_of(lay["node"])}" fill="{node}"/>')
    parts.append("</svg>")
    return "".join(parts)


def key(c, cut, n, s):
    return f"{c}-{cut}-{n}-{s}"


def cov(id_, bg=C.WHITE, fg="#000000"):
    return M.load_cov(R / f"{id_}.png", bg, fg)


def pixel_fit(lay):
    return M.pixel_fit({"body": lay["ink"], "node": lay["node"]})


def ridge_widths(c):
    """Local stroke width (px) at each inked pixel: the shortest chord through it along the
    horizontal, vertical and both diagonals (diagonal steps count as 1.414 px). Returns a list."""
    a = np.array(c) > 0.5
    h, w = a.shape
    out = []
    dirs = ((1, 0, 1.0), (0, 1, 1.0), (1, 1, 1.4142), (1, -1, 1.4142))
    ys, xs = np.nonzero(a)
    for y, x in zip(ys, xs):
        best = 1e9
        for dx, dy, f in dirs:
            n = 1
            for sgn in (1, -1):
                xx, yy = x + sgn * dx, y + sgn * dy
                while 0 <= xx < w and 0 <= yy < h and a[yy, xx]:
                    n += 1
                    xx += sgn * dx
                    yy += sgn * dy
            best = min(best, n * f)
        out.append(best)
    return out


def node_separate(lay, size, id_dark, id_light):
    out = {}
    for pol, id_, bg, fg in (("dark_on_light", id_dark, C.NEWS, C.CHAR), ("light_on_dark", id_light, C.CHAR, C.NEWS)):
        cc = M.load_cov(R / f"{id_}.png", bg, fg)
        mask = [[v > .5 for v in r] for r in cc]
        b = lay["node"].bounds
        nx, ny = int((b[0] + b[2]) / 2), int((b[1] + b[3]) / 2)
        lab, sizes = M.components(mask)
        comp = lab[min(size - 1, ny)][min(size - 1, nx)]
        node_area = max(1.0, (b[2] - b[0]) * (b[3] - b[1]) * math.pi / 4)
        out[pol] = bool(comp) and sizes.get(comp, 0) <= node_area * 2.2
    return out


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(t):
    return "#%02X%02X%02X" % tuple(int(v) for v in t)


def tile_svg(c, cut, n, shape, color, size, colorway=None):
    """One holder with its icon, as a single SVG at `size` px: the 24 px master in a 40 px
    holder, the display master above that."""
    fill, cw = C.HOLDER_COLORS[color]
    cw = colorway or cw
    lay, s = (D.master(c, cut, n, 24), 24) if size == 40 else (D.display(c, cut, n), 24)
    hp = C.holder_path(shape, size)
    off = size * (1 - C.FIELD_FRACTION) / 2
    sc = size * C.FIELD_FRACTION / s
    ink, node, seat = C.COLORWAYS[cw]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">',
             f'<path d="{g.d_of(hp)}" fill="{fill}"/>',
             f'<path d="{g.d_of(g.transform(lay["ink"], sc, off, off))}" fill="{ink}"/>',
             f'<path d="{g.d_of(g.transform(lay["node"], sc, off, off))}" fill="{node}"/>', "</svg>"]
    return "".join(parts), lay, sc, off


def measure_tiles():
    """Safe area and rendered contrast for every icon in every holder and tile color, and for
    the bare icon on every surface."""
    jobs, meta = [], {}
    for (c, cut) in C.DRAWINGS:
        for n in D.ICONS:
            for shape in C.HOLDER_SHAPES:
                for color in C.HOLDER_COLORS:
                    for size in (40, 80):
                        html, lay, sc, off = tile_svg(c, cut, n, shape, color, size)
                        id_ = f"t-{c}-{cut}-{n}-{shape}-{color}-{size}"
                        jobs.append({"id": id_, "w": size, "h": size, "bg": "#7F7F7F", "html": html})
                        meta[id_] = (c, cut, n, shape, color, size, lay, sc, off)
            for sname, label, bg in C.SURFACES:
                cw = {"newsprint": "Ink-Charcoal-Red", "white": "Ink-Charcoal-Red", "charcoal": "Ink-Newsprint-Red", "prussian": "Ink-White"}[sname]
                lay = D.display(c, cut, n)
                id_ = f"s-{c}-{cut}-{n}-{sname}"
                jobs.append({"id": id_, "w": 96, "h": 96, "bg": bg, "html": C.svg_doc(lay, 24, cw, px=96)})
                meta[id_] = (c, cut, n, sname, bg, cw, lay)
    jp = C.SCRATCH / "tile-jobs.json"
    jp.write_text(json.dumps(jobs))
    rt = C.SCRATCH / "rt"
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(rt)], check=True)
    tiles, surf = {}, {}
    for id_, m in meta.items():
        img = np.array(Image.open(rt / f"{id_}.png").convert("RGB")).astype(float)
        if id_.startswith("t-"):
            c, cut, n, shape, color, size, lay, sc, off = m
            fill = np.array(_rgb(C.HOLDER_COLORS[color][0]), float)
            hmask = np.zeros(img.shape[:2], bool)
            yy, xx = np.mgrid[0:size, 0:size]
            hp = C.holder_path(shape, size)
            inside = np.array([[hp.contains((x + .5, y + .5)) for x in range(size)] for y in range(size)])
            for _ in range(2):  # erode two pixels, so the holder's own antialiased edge is not read as ink
                pd = np.pad(inside, 1, constant_values=False)
                inside = pd[1:-1, 1:-1] & pd[:-2, 1:-1] & pd[2:, 1:-1] & pd[1:-1, :-2] & pd[1:-1, 2:]
            diff = np.abs(img - fill).sum(-1) > 24
            ink = diff & inside
            ys, xs = np.nonzero(ink)
            lo, hi = size * (1 - C.LIVE_FRACTION) / 2, size * (1 + C.LIVE_FRACTION) / 2
            bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
            in_live = bbox[0] >= lo - 0.5 and bbox[1] >= lo - 0.5 and bbox[2] <= hi + 0.5 and bbox[3] <= hi + 0.5
            rmax = float(np.max(np.hypot(xs + .5 - size / 2, ys + .5 - size / 2))) / size
            margin = min(bbox[0], bbox[1], size - bbox[2], size - bbox[3]) / size
            # rendered colors: ink core and node core, and the ring around the node
            ink_c, node_c, seat_c = C.COLORWAYS[C.HOLDER_COLORS[color][1]]
            cx, cy = lay["center"]
            ncx, ncy = cx * sc + off, cy * sc + off
            rn, rs = 2.0 * sc, 3.0 * sc
            dist = np.hypot(xx + .5 - ncx, yy + .5 - ncy)
            core = img[dist <= max(0.6, rn - 0.8)]
            band = img[(dist >= rn + 0.25 * (rs - rn)) & (dist <= rs - 0.25 * (rs - rn))]
            node_med = np.median(core, 0) if len(core) else None
            band_med = np.median(band, 0) if len(band) else None
            full = ink & (np.abs(img - np.array(_rgb(ink_c), float)).sum(-1) < 30)
            row = {"bbox": bbox, "in_live_area": bool(in_live), "r_max_share": round(rmax, 3), "margin_share": round(margin, 3),
                   "ink_vs_tile": round(C.contrast(ink_c, C.HOLDER_COLORS[color][0]), 2),
                   "ink_full_px": int(full.sum())}
            if node_med is not None and band_med is not None:
                row["node_core"] = _hex(node_med)
                row["node_ring"] = _hex(band_med)
                row["node_vs_ring"] = round(C.contrast(_hex(node_med), _hex(band_med)), 2)
            if shape == "Circle":
                row["in_circle_safe"] = bool(rmax <= C.CIRCLE_SAFE + 0.5 / size)
            tiles[id_[2:]] = row
        else:
            c, cut, n, sname, bg, cw, lay = m
            cx, cy = lay["center"]
            sc = 4.0
            yy, xx = np.mgrid[0:96, 0:96]
            dist = np.hypot(xx + .5 - cx * sc, yy + .5 - cy * sc)
            core = img[dist <= 2.0 * sc - 1.0]
            band = img[(dist >= 2.0 * sc + 1.0) & (dist <= 3.0 * sc - 1.0)]
            ink_c = C.COLORWAYS[cw][0]
            surf[id_[2:]] = {"ink_vs_surface": round(C.contrast(ink_c, bg), 2),
                             "node_core": _hex(np.median(core, 0)), "node_ring": _hex(np.median(band, 0)),
                             "node_vs_ring": round(C.contrast(_hex(np.median(core, 0)), _hex(np.median(band, 0))), 2)}
    return tiles, surf


WATCH = {"explain": ["letter C", "letter L", "copyright sign"], "track": ["status light", "Signal Grid lockmark"],
         "connect": ["copyright sign", "V5 chain link (pm-connect)"], "act": ["letter D", "chapter number 01", "play button"],
         "loop": ["letter C", "letter G"], "search": ["letter Q"], "ballot": [], "money": []}


def _glyphs_svg(text, size, font):
    """Glyph outlines for a short string, scaled to the live area and centered, like Phase 1."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    f = TTFont(str(font))
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    x = 0
    parts = []
    for ch in text:
        name = cmap[ord(ch)]
        parts.append((name, x))
        x += gs[name].width
    bp = BoundsPen(gs)
    for name, dx in parts:
        gs[name].draw(TransformPen(bp, (1, 0, 0, 1, dx, 0)))
    x0, y0, x1, y1 = bp.bounds
    live = size - 2
    sc = min(live / (x1 - x0), live / (y1 - y0))
    tx = (size - (x1 - x0) * sc) / 2 - x0 * sc
    ty = (size - (y1 - y0) * sc) / 2 + y1 * sc
    out = []
    for name, dx in parts:
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (1, 0, 0, 1, dx, 0)))
        out.append(f'<path transform="translate({tx:.3f} {ty:.3f}) scale({sc:.5f} {-sc:.5f})" d="{pen.getCommands()}" fill="#000"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{"".join(out)}</svg>'


def measure_watch():
    """Each icon against the shapes a reader could take it for, at 16 px (24 px for C's line cut)."""
    refs = {}
    for sz in (16, 24):
        rr = M.reference_svgs(sz)
        rr["chapter number 01"] = _glyphs_svg("01", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        rr["letter Q"] = _glyphs_svg("Q", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        rr["letter G"] = _glyphs_svg("G", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        refs[sz] = rr
    jobs = []
    for sz, rr in refs.items():
        for nm, svg in rr.items():
            jobs.append({"id": f"ref-{M.slug(nm)}-{sz}", "w": sz, "h": sz, "bg": C.WHITE, "html": svg})
    jp = C.SCRATCH / "watch-jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(R)], check=True)
    # the Phase 1 Act frame (a head over the opening only), redrawn in each 16 px grammar, as the baseline
    from icons_geom import poly, rect, union, wall_poly
    old = {"A-line": D.hinted(D.layers(union(wall_poly([(1, 1), (10, 4.375), (10, 15), (1, 15)]), D._ln([(12, 2), (14, 2), (14, 15)])), 5.5, 8.5, 16), 16),
           "B-flat": D.hinted(D.layers(union(poly((1, 1), (9, 4), (9, 15), (1, 15)), rect(10, 1, 5, 2), rect(13, 1, 2, 14)), 4.5, 8.5, 16), 16)}
    jobs2 = [{"id": f"oldact-{k}", "w": 16, "h": 16, "bg": C.WHITE, "html": mono_svg(v, 16, 16)} for k, v in old.items()]
    jp2 = C.SCRATCH / "watch-old.json"
    jp2.write_text(json.dumps(jobs2))
    subprocess.run(["node", str(C.RENDER_JS), str(jp2), str(R)], check=True)
    out = {}
    for k in old:
        out[f"phase1-frame|{k}|act|chapter number 01|16"] = M.sim(cov(f"oldact-{k}"), cov("ref-chapter-number-01-16"))
    for (c, cut) in C.DRAWINGS:
        sz = 16 if 16 in C.sizes(c, cut) else 24
        for n in D.ICONS:
            for nm in WATCH[n]:
                out[f"{c}-{cut}|{n}|{nm}|{sz}"] = M.sim(cov(f"w-{key(c, cut, n, sz)}"), cov(f"ref-{M.slug(nm)}-{sz}"))
    return out


def main():
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    jobs = []
    lays = {}
    for (c, cut) in C.DRAWINGS:
        for n in D.ICONS:
            for s in C.sizes(c, cut):
                lay = D.master(c, cut, n, s)
                lays[(c, cut, n, s)] = lay
                k = key(c, cut, n, s)
                jobs.append({"id": f"w-{k}", "w": s, "h": s, "bg": C.WHITE, "html": mono_svg(lay, s, s)})
                jobs.append({"id": f"i-{k}", "w": s, "h": s, "bg": C.WHITE, "html": mono_svg(lay, s, s, only="ink")})
                jobs.append({"id": f"n-{k}", "w": s, "h": s, "bg": C.WHITE, "html": mono_svg(lay, s, s, only="node")})
                jobs.append({"id": f"mn-{k}", "w": s, "h": s, "bg": C.NEWS, "html": mono_svg(lay, s, s, ink=C.CHAR)})
                jobs.append({"id": f"k-{k}", "w": s, "h": s, "bg": C.CHAR, "html": mono_svg(lay, s, s, ink=C.NEWS)})
                jobs.append({"id": f"u-{k}", "w": s, "h": s, "bg": C.WHITE, "html": mono_svg(D.draw(c, cut, n, s), s, s)})
            lay24 = D.display(c, cut, n)
            k24 = key(c, cut, n, 24)
            jobs.append({"id": f"w96-{k24}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono_svg(lay24, 24, 96)})
            jobs.append({"id": f"i96-{k24}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono_svg(lay24, 24, 96, only="ink")})
            jobs.append({"id": f"n96-{k24}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono_svg(lay24, 24, 96, only="node")})
    (C.SCRATCH / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(C.SCRATCH / "jobs.json"), str(R)], check=True)

    res = {"drawings": {}, "pairs": {}, "sets": {}, "contrast": {}, "spec": {}}
    for (c, cut, n, s), lay in lays.items():
        k = key(c, cut, n, s)
        w = cov(f"w-{k}")
        cr, dens = M.crisp(w)
        sil = M.silhouette([[v > .5 for v in r] for r in w])
        sil_d = sum(map(sum, sil)) / (s * s)
        ink_c, node_c = cov(f"i-{k}"), cov(f"n-{k}")
        si, sn = sum(map(sum, ink_c)), sum(map(sum, node_c))
        row = {"crisp": cr, "crisp_unhinted": M.crisp(cov(f"u-{k}"))[0], "density": dens, "silhouette_fill": round(sil_d, 3), "pixel_fit": pixel_fit(lay),
               "red_share_px": round(sn / (si + sn), 3) if si + sn else None,
               "node_separate": node_separate(lay, s, f"mn-{k}", f"k-{k}")}
        a_ink, a_node = g.area(lay["ink"]), g.area(lay["node"])
        row["area_ink"], row["area_node"] = round(a_ink, 2), round(a_node, 2)
        row["red_share_vector"] = round(a_node / (a_ink + a_node), 3)
        b = g.union(lay["ink"], lay["node"]).bounds
        row["bounds"] = [round(v, 2) for v in b]
        row["silhouette_pass"] = (cr or 0) >= 0.60 and dens >= 0.25 if s == 16 else None
        row["pixel_fit_pass"] = (cr or 0) >= 0.60
        if s == 24:
            k96 = k
            w96 = cov(f"w96-{k96}")
            tot = sum(map(sum, w96)) or 1
            cx = sum(w96[y][x] * x for y in range(96) for x in range(96)) / tot
            cy = sum(w96[y][x] * y for y in range(96) for x in range(96)) / tot
            row["density96"] = round(tot / (96 * 96), 3)
            row["centroid96"] = [round((cx + .5) / 96 - .5, 3), round((cy + .5) / 96 - .5, 3)]
            i96, n96 = cov(f"i96-{k96}"), cov(f"n96-{k96}")
            ti, tn = sum(map(sum, i96)), sum(map(sum, n96))
            row["red_share_96"] = round(tn / (ti + tn), 3)
            if cut == "line":
                wid = ridge_widths(i96)
                arr = np.array(wid) / 4.0 if wid else np.array([])
                row["stroke"] = {"ink_px": len(wid), "median_units": round(float(np.median(arr)), 2) if len(arr) else None,
                                 "share_at_2": round(float(np.mean((arr >= 1.75) & (arr <= 2.4))), 3) if len(arr) else None,
                                 "share_over_3": round(float(np.mean(arr > 3.0)), 3) if len(arr) else None}
        res["drawings"][k] = row
    # similarity within each set
    for (c, cut) in C.DRAWINGS:
        for s in C.sizes(c, cut):
            for a, b in combinations(D.ICONS, 2):
                res["pairs"][f"{c}-{cut}|{a}|{b}|{s}"] = M.sim(cov(f"w-{key(c, cut, a, s)}"), cov(f"w-{key(c, cut, b, s)}"))
    # set summaries
    for (c, cut) in C.DRAWINGS:
        for s in C.sizes(c, cut):
            rows = [res["drawings"][key(c, cut, n, s)] for n in D.ICONS]
            pr = [v for kk, v in res["pairs"].items() if kk.startswith(f"{c}-{cut}|") and kk.endswith(f"|{s}")]
            worst = max(((v["score"], kk) for kk, v in res["pairs"].items() if kk.startswith(f"{c}-{cut}|") and kk.endswith(f"|{s}")))
            res["sets"][f"{c}-{cut}-{s}"] = {
                "crisp_min": min(r["crisp"] for r in rows), "crisp_max": max(r["crisp"] for r in rows),
                "pixel_fit_vector_min": min((r["pixel_fit"]["share"] or 1) for r in rows),
                "red_share_vector": [min(r["red_share_vector"] for r in rows), max(r["red_share_vector"] for r in rows)],
                "red_share_px": [min(r["red_share_px"] for r in rows), max(r["red_share_px"] for r in rows)],
                "area_ink_total": [round(min(r["area_ink"] + r["area_node"] for r in rows), 1), round(max(r["area_ink"] + r["area_node"] for r in rows), 1)],
                "pairs_over_060": sum(1 for v in pr if v["score"] >= 0.60),
                "worst_pair": [worst[1].split("|")[1], worst[1].split("|")[2], worst[0]],
                "max_blurred_corr": max(v["blurred_corr"] for v in pr),
            }
            if s == 24:
                d96 = [r["density96"] for r in rows]
                med = float(np.median(d96))
                res["sets"][f"{c}-{cut}-{s}"]["density96"] = [min(d96), max(d96), round(med, 3)]
                res["sets"][f"{c}-{cut}-{s}"]["density96_dev"] = [round(min(d96) / med - 1, 3), round(max(d96) / med - 1, 3)]
                res["sets"][f"{c}-{cut}-{s}"]["centroid_max"] = max(max(abs(r["centroid96"][0]), abs(r["centroid96"][1])) for r in rows)
    for sname, label, bg in C.SURFACES:
        ink = C.NEWS if sname in ("charcoal",) else (C.WHITE if sname == "prussian" else C.CHAR)
        res["contrast"][f"ink|{sname}"] = round(C.contrast(ink, bg), 2)
    for sname, label, bg in C.SURFACES[:3]:
        res["contrast"][f"red|{sname}"] = round(C.contrast(C.RED, bg), 2)
    res["contrast"]["keyline|newsprint"] = round(C.contrast(C.CHAR, C.NEWS), 2)
    res["contrast"]["red|keyline"] = round(C.contrast(C.RED, C.CHAR), 2)
    res["tiles"], res["surfaces_rendered"] = measure_tiles()
    res["watch"] = measure_watch()
    out = C.OUT / f"{C.DATE}_Icon-Concepts-Measurements.json"
    C.OUT.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print("measured", len(jobs), "renders")
    for kk, v in res["sets"].items():
        print(kk, v)


if __name__ == "__main__":
    main()
