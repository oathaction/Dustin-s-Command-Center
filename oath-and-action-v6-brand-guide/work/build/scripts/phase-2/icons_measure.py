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
        row = {"crisp": cr, "density": dens, "silhouette_fill": round(sil_d, 3), "pixel_fit": pixel_fit(lay),
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
    out = C.OUT / f"{C.DATE}_Icon-Concepts-Measurements.json"
    C.OUT.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print("measured", len(jobs), "renders")
    for kk, v in res["sets"].items():
        print(kk, v)


if __name__ == "__main__":
    main()
