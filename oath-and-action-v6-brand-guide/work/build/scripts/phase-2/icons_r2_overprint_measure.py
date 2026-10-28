"""Concept 1, Overprint: render and measure the ten icons (design director, Phase 2, round two,
October 28, 2026).

Run: python3 -I icons_r2_overprint_measure.py
Writes work/boards/phase-2/icons-r2/overprint/20261028_Overprint-Measurements.json.

Every raster comes from Chromium at device scale 1 through round one's icons_render_cells.js. The
measures reuse the Phase 1 functions in work/build/scripts/phase-1/symbols_measure.py and round
one's glyph helper in icons_measure.py, all imported and unchanged.

Checks (pass marks in brackets):
  pixel fit      D1-17: crisp share of inked pixels at 16 and 24 px, ink and plane together [0.60]
  similarity     D1-16: blurred correlation and silhouette overlap, every pair at 16 and 24 px,
                 as drawn and idle (plane removed) [under 0.60]
  look-alikes    every icon against letters, "01", "n", and interface glyphs (sync, reload, record,
                 pause, notification badge, map pin, crop, eye, printer, inbox) [under 0.60]
  weight         line ink of the display master at 96 px, as a share of the field
                 [16 to 24 percent, and within 15 percent of the set's median]
  red share      the plane's area over the painted area, ink and plane together [15 to 25 percent]
  center of mass display master at 96 px, ink and plane, offset from center [12 percent of the field]
  live area      straight edges inside 2 to 22 units; round forms 0.25 beyond at most
  badge corner   no red in the top-right 6 by 6 units of the field
  contrast       ink on every surface and tile; red on every surface; line over red
  holders        ink and plane inside the live area (half the side) in all 90 tiles at 40, 80 and
                 180 px, and inside 40 percent of the side from the center in the circle
  test 2         the plane turned to ink and removed, at 16, 24 and 48 px and in White on
                 Prussian: still distinct from every other icon and from every look-alike
  test 3         one line weight (ridge widths at 96 px), the smallest clear gap between parts
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
import icons_r2_overprint_common as C  # noqa: E402
import icons_r2_overprint_draw as O  # noqa: E402
import icons_geom as g  # noqa: E402
import icons_measure as IM  # noqa: E402  (round one; its helpers only, never changed)
import numpy as np  # noqa: E402
import symbols_measure as M  # noqa: E402  (Phase 1 measures)
from PIL import Image  # noqa: E402

R = C.SCRATCH / "r"


def mono(L, vbox, px, ink="#000000", plane="ink"):
    """plane: 'ink' prints the plane in the ink color, None drops it."""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {vbox} {vbox}">']
    if plane == "ink" and not g.is_empty(L["accent"]):
        parts.append(f'<path d="{g.d_of(L["accent"])}" fill="{ink}"/>')
    parts.append(f'<path d="{g.d_of(L["ink"])}" fill="{ink}"/>')
    parts.append("</svg>")
    return "".join(parts)


def cov(id_, bg=C.WHITE, fg="#000000"):
    return M.load_cov(R / f"{id_}.png", bg, fg)


# ---------------------------------------------------------------- reference look-alikes

def _refs24():
    """Interface glyphs a reader could take an icon for, drawn on the 24-unit grid at 2 units."""
    P = O
    w = 2.0

    def st(pen):
        return O.stroke(pen, w)
    out = {}
    a1 = st(P.arc_c(12, 12, 7, 200, 340))
    a2 = st(P.arc_c(12, 12, 7, 20, 160))
    h1 = g.union(*[st(p) for p in P.chevron((12 + 7 * math.cos(math.radians(340)), 12 + 7 * math.sin(math.radians(340))), 340 + 90, 3)])
    h2 = g.union(*[st(p) for p in P.chevron((12 + 7 * math.cos(math.radians(160)), 12 + 7 * math.sin(math.radians(160))), 160 + 90, 3)])
    out["sync"] = g.union(a1, a2, h1, h2)
    out["reload"] = g.union(st(P.arc_c(12, 12, 7, -60, 230)), *[st(p) for p in P.chevron((12 + 7 * math.cos(math.radians(230)), 12 + 7 * math.sin(math.radians(230))), 230 + 90, 3)])
    out["record"] = g.union(g.ring(12, 12, 9, 7), g.circle(12, 12, 4))
    out["pause"] = g.union(g.rect(7, 5, 3, 14), g.rect(14, 5, 3, 14))
    out["notification badge"] = g.union(st(P.rrect_c(4, 8, 16, 20, 1)), g.circle(17.5, 6.5, 3.5))
    pin = g.union(g.circle(12, 9, 6), g.poly((7, 12), (17, 12), (12, 21)))
    out["map pin"] = g.minus(pin, g.circle(12, 9, 2.5))
    out["crop"] = g.union(st(P.line_c((7, 3), (7, 17), (21, 17))), st(P.line_c((3, 7), (17, 7), (17, 21))))
    lens = g.union(g.intersect(g.circle(12, 20, 11), g.circle(12, 4, 11)))
    out["eye"] = g.union(g.minus(lens, g.intersect(g.circle(12, 20, 9), g.circle(12, 4, 9))), g.circle(12, 12, 3))
    out["printer"] = g.union(st(P.rrect_c(3, 9, 21, 17, 1)), st(P.line_c((7, 9), (7, 3), (17, 3), (17, 9))), st(P.line_c((7, 14), (7, 21), (17, 21), (17, 14))))
    out["inbox"] = g.union(st(P.rrect_c(3, 3, 21, 21, 1)), st(P.line_c((3, 14), (8, 14), (9, 17), (15, 17), (16, 14), (21, 14))))
    out["expand"] = g.union(*[st(P.line_c(*pts)) for pts in (((4, 9), (4, 4), (9, 4)), ((15, 4), (20, 4), (20, 9)),
                                                            ((20, 15), (20, 20), (15, 20)), ((9, 20), (4, 20), (4, 15)))])
    out["bar chart"] = g.union(g.rect(4, 14, 4, 7), g.rect(10, 9, 4, 12), g.rect(16, 4, 4, 17))
    out["podium"] = g.union(g.rect(3, 13, 6, 8), g.rect(9, 7, 6, 14), g.rect(15, 11, 6, 10))
    out["audio"] = g.union(st(P.arc_c(12, 12, 8, 130, 230)), st(P.arc_c(12, 12, 8, -50, 50)), st(P.arc_c(12, 12, 4.5, 140, 220)), st(P.arc_c(12, 12, 4.5, -40, 40)))
    return out


# Each icon against the readings a reader could take it for: the creative director's watch column,
# the stage 1 blind test's misreadings, the letters and numerals Phase 1 and round one watched.
WATCH = {
    "explain": ["crop", "expand", "notification badge", "letter C", "letter L", "copyright sign"],
    "track": ["bar chart", "podium", "status light", "Signal Grid lockmark"],
    "connect": ["pause", "audio", "record", "copyright sign", "V5 chain link (pm-connect)"],
    "act": ["chapter number 01", "letter n", "letter D", "play button"],
    "ballot": ["inbox", "printer"],
    "bill": ["printer"],
    "testify": ["map pin"],
    "housing": ["letter n"],
    "money": ["record", "chapter number 01"],
    "loop": ["sync", "reload", "eye", "record", "letter C", "letter G"],
}


def ref_jobs():
    jobs = []
    refs24 = _refs24()
    for sz in (16, 24):
        rr = M.reference_svgs(sz)
        rr["chapter number 01"] = IM._glyphs_svg("01", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        rr["letter n"] = IM._glyphs_svg("n", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        rr["letter G"] = IM._glyphs_svg("G", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        rr["letter Q"] = IM._glyphs_svg("Q", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        for nm, shp in refs24.items():
            rr[nm] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{sz}" height="{sz}" viewBox="0 0 24 24"><path d="{g.d_of(shp)}" fill="#000"/></svg>'
        for nm, svg in rr.items():
            jobs.append({"id": f"ref-{M.slug(nm)}-{sz}", "w": sz, "h": sz, "bg": C.WHITE, "html": svg})
    names = list(M.reference_svgs(16).keys()) + ["chapter number 01", "letter n", "letter G", "letter Q"] + list(refs24.keys())
    return jobs, names


# ---------------------------------------------------------------- raster helpers

def ridge_widths(c):
    """Local stroke width at each inked pixel: the shortest run through it along the four axes."""
    a = np.array(c) > 0.5
    h, w = a.shape
    out = []
    ys, xs = np.nonzero(a)
    for y, x in zip(ys, xs):
        best = 1e9
        for dx, dy, f in ((1, 0, 1.0), (0, 1, 1.0), (1, 1, 1.4142), (1, -1, 1.4142)):
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


def centroid(c):
    a = np.array(c)
    tot = a.sum() or 1
    n = a.shape[0]
    ys, xs = np.mgrid[0:n, 0:n]
    return [round(float(((a * (xs + .5)).sum() / tot) / n - .5), 3), round(float(((a * (ys + .5)).sum() / tot) / n - .5), 3)]


# ---------------------------------------------------------------- vector checks

def straight_extent(path):
    """Smallest and largest coordinate reached by straight (line) segments of the outline."""
    lo, hi = 1e9, -1e9
    for seg in M_flat(path):
        if seg[0] == "L":
            for (x, y) in (seg[1], seg[2]):
                lo, hi = min(lo, x, y), max(hi, x, y)
    return lo, hi


def M_flat(path):
    from symbols_geom import flatten_segments
    return flatten_segments(path)


def min_gap(L, size_units=24):
    """Smallest clear distance between separate ink parts of a drawing (vector, by sampling)."""
    import shapely  # noqa: F401
    from shapely.geometry import Polygon
    geom = None
    for cont in g._contours(L["ink"], 16):
        if len(cont) > 2:
            p = Polygon(cont).buffer(0)
            geom = p if geom is None else geom.symmetric_difference(p)   # even-odd: holes stay holes
    if geom is None:
        return None
    parts = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    parts = [q for q in parts if q.area > 0.05]
    if len(parts) < 2:
        return None
    best = 1e9
    for a, b in combinations(parts, 2):
        best = min(best, a.distance(b))
    return round(best, 2)


def holder_ok(name, shape, color, size):
    s, L, sc, off = C.tile_svg(name, shape, color, size)
    shp = g.union(L["ink"], L["accent"]) if not g.is_empty(L["accent"]) else L["ink"]
    shp = g.transform(shp, sc, off, off)
    b = shp.bounds
    lo, hi = size * 0.25, size * 0.75
    tol = 0.25 * sc + 0.01
    inside = b[0] >= lo - tol and b[1] >= lo - tol and b[2] <= hi + tol and b[3] <= hi + tol
    rmax = 0.0
    for cont in g._contours(shp, 16):
        for (x, y) in cont:
            rmax = max(rmax, math.hypot(x - size / 2, y - size / 2))
    row = {"bounds": [round(v, 2) for v in b], "in_live_area": bool(inside), "r_max_share": round(rmax / size, 3),
           "margin_share": round(min(b[0], b[1], size - b[2], size - b[3]) / size, 3)}
    if shape == "Circle":
        row["in_circle_safe"] = bool(rmax / size <= C.RC.CIRCLE_SAFE + 0.004)
    return row


# ---------------------------------------------------------------- main

def main():
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    jobs = []
    for n in O.ICONS:
        for kind, s in (("16px", 16), ("24px", 24)):
            L = C.lay(n, kind)
            jobs.append({"id": f"w-{n}-{s}", "w": s, "h": s, "bg": C.WHITE, "html": mono(L, s, s)})
            jobs.append({"id": f"i-{n}-{s}", "w": s, "h": s, "bg": C.WHITE, "html": mono(L, s, s, plane=None)})
            # test 2 on Prussian: White line, no plane
            jobs.append({"id": f"p-{n}-{s}", "w": s, "h": s, "bg": C.PRUS, "html": mono(L, s, s, ink=C.WHITE, plane=None)})
        D = O.display(n)
        jobs.append({"id": f"w96-{n}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono(D, 24, 96)})
        jobs.append({"id": f"i96-{n}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono(D, 24, 96, plane=None)})
        jobs.append({"id": f"w48-{n}", "w": 48, "h": 48, "bg": C.WHITE, "html": mono(D, 24, 48)})
        jobs.append({"id": f"i48-{n}", "w": 48, "h": 48, "bg": C.WHITE, "html": mono(D, 24, 48, plane=None)})
        jobs.append({"id": f"p48-{n}", "w": 48, "h": 48, "bg": C.PRUS, "html": mono(D, 24, 48, ink=C.WHITE, plane=None)})
    rj, ref_names = ref_jobs()
    jobs += rj
    for k in range(0, len(jobs), 1):
        pass
    jp = C.SCRATCH / "measure-jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(R)], check=True)

    res = {"icons": {}, "pairs": {}, "watch": {}, "sets": {}, "contrast": {}, "tiles": {}, "spec": {}}
    # ---------------- per icon
    for n in O.ICONS:
        row = {}
        for s in (16, 24):
            L = C.lay(n, f"{s}px")
            cr, dens = M.crisp(cov(f"w-{n}-{s}"))
            cri, _ = M.crisp(cov(f"i-{n}-{s}"))
            row[f"crisp_{s}"] = cr
            row[f"crisp_ink_{s}"] = cri
            row[f"density_{s}"] = dens
            row[f"pixel_fit_vector_{s}"] = M.pixel_fit({"body": L["ink"], "node": L["accent"]})
        D = O.display(n)
        i96 = cov(f"i96-{n}")
        w96 = cov(f"w96-{n}")
        row["ink96"] = round(float(np.array(i96).sum()) / (96 * 96), 3)
        row["painted96"] = round(float(np.array(w96).sum()) / (96 * 96), 3)
        row["centroid96"] = centroid(w96)
        ai, aa = g.area(D["ink"]), g.area(D["accent"])
        un = g.area(g.union(D["ink"], D["accent"]))
        under = g.area(g.intersect(D["ink"], D["accent"]))
        row["red_share"] = round(aa / un, 3)
        row["red_share_visible"] = round((aa - under) / un, 3)
        row["red_under_ink"] = round(under / aa, 3) if aa else 0
        row["ink_over_red"] = round(under / ai, 3)
        corner = g.area(g.intersect(D["accent"], g.rect(18, 0, 6, 6)))
        row["badge_corner_red"] = round(corner, 3)
        bnd = g.union(D["ink"], D["accent"]).bounds
        row["bounds"] = [round(v, 2) for v in bnd]
        lo, hi = straight_extent(D["ink"])
        lo2, hi2 = straight_extent(D["accent"]) if aa else (1e9, -1e9)
        row["straight_extent"] = [round(min(lo, lo2), 2), round(max(hi, hi2), 2)]
        row["live_area_ok"] = bool(min(lo, lo2) >= 2 - 1e-6 and max(hi, hi2) <= 22 + 1e-6 and bnd[0] >= 1.75 - 1e-6 and bnd[1] >= 1.75 - 1e-6
                                   and bnd[2] <= 22.25 + 1e-6 and bnd[3] <= 22.25 + 1e-6)
        wid = np.array(ridge_widths(i96)) / 4.0
        row["stroke"] = {"median_units": round(float(np.median(wid)), 2), "share_1p25_to_1p9": round(float(np.mean((wid >= 1.25) & (wid <= 1.9))), 3)}
        row["min_gap_units"] = min_gap(D)
        res["icons"][n] = row
    # ---------------- sets
    inks = [res["icons"][n]["ink96"] for n in O.ICONS]
    med = float(np.median(inks))
    for n in O.ICONS:
        r = res["icons"][n]
        r["ink_dev"] = round(r["ink96"] / med - 1, 3)
        r["weight_pass"] = bool(0.16 <= r["ink96"] <= 0.24 and abs(r["ink_dev"]) <= 0.15)
        r["red_pass"] = bool(0.15 - 1e-9 <= r["red_share"] <= 0.25 + 1e-9)
        r["com_pass"] = bool(max(abs(r["centroid96"][0]), abs(r["centroid96"][1])) <= 0.12)
        r["pixel_fit_pass"] = bool((r["crisp_16"] or 0) >= 0.60 and (r["crisp_24"] or 0) >= 0.60)
    res["sets"]["ink_median"] = round(med, 3)
    # ---------------- similarity
    for s in (16, 24):
        for a, b in combinations(O.ICONS, 2):
            res["pairs"][f"drawn|{a}|{b}|{s}"] = M.sim(cov(f"w-{a}-{s}"), cov(f"w-{b}-{s}"))
            res["pairs"][f"idle|{a}|{b}|{s}"] = M.sim(cov(f"i-{a}-{s}"), cov(f"i-{b}-{s}"))
    for s in (48,):
        for a, b in combinations(O.ICONS, 2):
            res["pairs"][f"idle|{a}|{b}|{s}"] = M.sim(cov(f"i48-{a}"), cov(f"i48-{b}"))
            res["pairs"][f"drawn|{a}|{b}|{s}"] = M.sim(cov(f"w48-{a}"), cov(f"w48-{b}"))
    # Prussian, White line, no plane (coverage read against Prussian)
    for s in (16, 24):
        for a, b in combinations(O.ICONS, 2):
            res["pairs"][f"prussian|{a}|{b}|{s}"] = M.sim(cov(f"p-{a}-{s}", C.PRUS, C.WHITE), cov(f"p-{b}-{s}", C.PRUS, C.WHITE))
    # ---------------- look-alikes
    for n in O.ICONS:
        for s in (16, 24):
            for mode, pre in (("drawn", "w"), ("idle", "i")):
                for nm in WATCH[n]:
                    res["watch"][f"{mode}|{n}|{nm}|{s}"] = M.sim(cov(f"{pre}-{n}-{s}"), cov(f"ref-{M.slug(nm)}-{s}"))
    # ---------------- summaries
    def worst(prefix, s=None):
        items = [(v["score"], k) for k, v in res["pairs"].items() if k.startswith(prefix) and (s is None or k.endswith(f"|{s}"))]
        return max(items) if items else None
    for mode in ("drawn", "idle", "prussian"):
        for s in (16, 24, 48):
            w = worst(f"{mode}|", s)
            if w:
                res["sets"][f"worst_{mode}_{s}"] = [w[1].split("|")[1], w[1].split("|")[2], w[0]]
                res["sets"][f"over_060_{mode}_{s}"] = sum(1 for k, v in res["pairs"].items() if k.startswith(f"{mode}|") and k.endswith(f"|{s}") and v["score"] >= 0.60)
    for n in O.ICONS:
        items = [(v["score"], k) for k, v in res["watch"].items() if f"|{n}|" in k]
        sc, k = max(items)
        res["icons"][n]["watch_worst"] = [k.split("|")[2], k.split("|")[0], int(k.split("|")[3]), sc]
    res["sets"]["act_vs_01_16"] = res["watch"]["drawn|act|chapter number 01|16"]["score"]
    res["sets"]["act_vs_n_16"] = res["watch"]["drawn|act|letter n|16"]["score"]
    res["sets"]["act_idle_vs_01_16"] = res["watch"]["idle|act|chapter number 01|16"]["score"]
    res["sets"]["act_idle_vs_n_16"] = res["watch"]["idle|act|letter n|16"]["score"]
    # ---------------- contrast
    for sname, label, bg in C.SURFACES:
        ink = C.NEWS if sname == "charcoal" else (C.WHITE if sname == "prussian" else C.CHAR)
        res["contrast"][f"ink|{sname}"] = round(C.contrast(ink, bg), 2)
    for sname, label, bg in C.SURFACES[:3]:
        res["contrast"][f"red|{sname}"] = round(C.contrast(C.RED, bg), 2)
    res["contrast"]["charcoal_line_on_red"] = round(C.contrast(C.CHAR, C.RED), 2)
    res["contrast"]["newsprint_line_on_red"] = round(C.contrast(C.NEWS, C.RED), 2)
    res["contrast"]["white_on_prussian"] = round(C.contrast(C.WHITE, C.PRUS), 2)
    # ---------------- holders
    for n in O.ICONS:
        for shape in C.HOLDER_SHAPES:
            for color in C.HOLDER_COLORS:
                for size in (28, 40, 80, 180):
                    res["tiles"][f"{n}|{shape}|{color}|{size}"] = holder_ok(n, shape, color, size)
    t = res["tiles"].values()
    res["sets"]["tiles"] = {"count": len(res["tiles"]), "in_live_area": sum(1 for v in t if v["in_live_area"]),
                            "circle_safe": sum(1 for v in t if v.get("in_circle_safe")),
                            "circle_count": sum(1 for v in t if "in_circle_safe" in v),
                            "min_margin_share": min(v["margin_share"] for v in t),
                            "max_r_share_circle": max(v["r_max_share"] for k, v in res["tiles"].items() if "|Circle|" in k)}
    res["spec"] = {"line_display_units": O.SPEC["display"]["w"], "line_px": 2, "offset_display": O.SPEC["display"]["off"],
                   "offset_24": O.SPEC[24]["off"], "offset_16": O.SPEC[16]["off"], "connect_offset_display": [0.0, 1.5],
                   "node_units": 3, "app_scale": C.APP_SCALE}
    C.MEAS.write_text(json.dumps(res, indent=1))
    print("median ink", med)
    for n in O.ICONS:
        r = res["icons"][n]
        print(f"{n:9s} crisp16 {r['crisp_16']} crisp24 {r['crisp_24']} ink {r['ink96']} dev {r['ink_dev']:+.2f} red {r['red_share']} com {r['centroid96']} live {r['live_area_ok']} gap {r['min_gap_units']} stroke {r['stroke']} watch {r['watch_worst']}")
    for k, v in res["sets"].items():
        print(k, v)


if __name__ == "__main__":
    main()
