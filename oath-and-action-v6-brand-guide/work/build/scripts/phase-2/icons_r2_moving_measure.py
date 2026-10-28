"""Concept 2, Moving part, stage 2: the checks round one ran, and tests 2 to 4.

Run after the masters and assets scripts: python3 -I icons_r2_moving_measure.py
Writes work/boards/phase-2/icons-r2/moving-part/20261028_Moving-Part-Measurements.json and the 1x renders
in px/ that the board magnifies.

Every raster comes from Chromium at device scale 1, through round one's icons_render_cells.js (called
as is). The measures are Phase 1's, imported from work/build/scripts/phase-1/symbols_measure.py:
  pixel fit     D1-17: at least 60 percent of inked pixels crisp (coverage over 0.9) at 16 and 24 px,
                plus the Phase 1 vector test (straight axis edges and large curve extremes on whole pixels)
  similarity    D1-16: mean of filled-silhouette overlap and blurred correlation, under 0.60 for all
                45 pairs at 16 px; the same score against letters, the numeral pair "01", V5 marks and the
                Material Symbols system glyphs the brief bans as reads
  weight        ink and red together as a share of the field at 96 px, within 15 percent of the median
  red share     red as a share of the painted area, in vector and at 96 px; the ceiling is 25 percent
  center of mass  offset of the 96 px render's centroid from the field center, 12 percent limit
  contrast      WCAG ratios for every ink, red and keyline on every surface and tile
  safe area     rendered ink inside the live area of each holder, and inside 0.40 of the diameter
                from the center in the circle
Tests 2 to 4 (the main session runs test 1):
  2 cover the red   red turned to ink and red removed at 16, 24 and 48 px, and White on Prussian:
                    the nearest other icon must stay under 0.60 (a proxy; the naming is by eye)
  3 hold up at 2x   one cut weight per size, counters at the minimum, curves by eye, weight band,
                    center of mass and pixel fit
  4 beside the best the benchmark sheet beside Material Symbols, and the spread of weight in a one-color
                    row of all ten
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
import icons_r2_moving_assets as A  # noqa: E402
import icons_r2_moving_common as C  # noqa: E402
import icons_r2_moving_draw as D  # noqa: E402
import icons_r2_moving_geom as G  # noqa: E402
import icons_r2_moving_masters as MS  # noqa: E402
import numpy as np  # noqa: E402
import symbols_measure as M  # noqa: E402  (Phase 1 measures, read only)
from PIL import Image  # noqa: E402

R = C.SCRATCH / "r"
MEAS = C.OUT / f"{C.DATE}_Moving-Part-Measurements.json"

# Material Symbols glyphs: the nearest subject for the benchmark sheet, and the system glyphs the
# name test bans (reload, sync, expand, crop, record, notification, add, play, pause) plus the CD's
# watch list for each subject.
NEAREST = {"explain": "unarchive", "track": "stairs", "connect": "join", "act": "door_open", "ballot": "how_to_vote",
           "bill": "description", "testify": "record_voice_over", "housing": "home", "money": "payments", "loop": "cycle"}
SYSTEM = ["refresh", "sync", "autorenew", "cached", "open_in_full", "crop", "radio_button_checked", "notifications",
          "add", "play_arrow", "pause"]
WATCH_MS = {"explain": ["crop", "open_in_full", "notifications", "app_badging"], "track": ["bar_chart", "leaderboard"],
            "connect": ["pause", "radio_button_checked", "graphic_eq"], "act": ["logout"], "ballot": ["inbox", "print"],
            "bill": ["receipt_long"], "testify": ["contact_phone"], "housing": ["storefront"], "money": ["wallet"],
            "loop": ["refresh", "sync", "autorenew"]}
WATCH_REF = {"explain": ["letter C", "letter L", "copyright sign"], "track": ["status light", "Signal Grid lockmark"],
             "connect": ["copyright sign", "V5 chain link (pm-connect)"], "act": ["letter D", "chapter number 01", "play button"],
             "ballot": [], "bill": ["letter L"], "testify": [], "housing": [], "money": [], "loop": ["letter C"]}
MS_CSS = ("https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,1,0")


def mono(m, U, px, only=None, fg="#000000"):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {U} {U}">']
    if only in (None, "ink", "removed"):
        parts.append(f'<path d="{m["ink"]}" fill="{fg}"/>')
    if only in (None, "accent"):
        parts.append(f'<path d="{m["accent"]}" fill="{fg}"/>')
    parts.append("</svg>")
    return "".join(parts)


def cov(id_, bg=C.WHITE, fg="#000000"):
    return M.load_cov(R / f"{id_}.png", bg, fg)


def render(jobs, name):
    jp = C.SCRATCH / f"{name}.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(R)], check=True)


def render_ms(names, sizes=(16, 24, 48)):
    """Material Symbols glyphs rendered by Chromium with the Google Fonts stylesheet, one cell each,
    cropped from one capture. Returns {(name, size): coverage}."""
    cells = []
    order = []
    y = 0
    for s in sizes:
        x = 0
        for n in names:
            cells.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;font-family:\'Material Symbols Rounded\';'
                         f'font-size:{s}px;line-height:{s}px;font-variation-settings:\'FILL\' 1,\'wght\' 400,\'opsz\' {min(48, max(20, s))};color:#000">{n}</div>')
            order.append((n, s, x, y))
            x += s + 8
        y += s + 8
    page = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{MS_CSS}">'
            f'<style>html,body{{margin:0;background:#fff}}</style></head><body><div style="position:relative;width:{(48 + 8) * len(names)}px;height:{y}px">{"".join(cells)}</div></body></html>')
    p = C.SCRATCH / "ms-refs.html"
    p.write_text(page)
    png = C.SCRATCH / "ms-refs.png"
    subprocess.run(["node", str(C.SHOT_JS), str(p), str(png), str((48 + 8) * len(names)), "1"], check=True)
    im = Image.open(png).convert("RGB")
    out = {}
    for n, s, x, yy in order:
        crop = im.crop((x, yy, x + s, yy + s))
        cp = R / f"ms-{n}-{s}.png"
        crop.save(cp)
        out[(n, s)] = M.load_cov(cp, C.WHITE, "#000000")
    return out


def centroid(c):
    a = np.array(c)
    tot = a.sum() or 1
    h, w = a.shape
    ys, xs = np.mgrid[0:h, 0:w]
    return float((a * (xs + .5)).sum() / tot / w - .5), float((a * (ys + .5)).sum() / tot / h - .5)


def holes(d):
    """Knock-outs inside a piece: subpaths that wind the other way from the piece's largest contour,
    with their smallest side."""
    import pathops
    from fontTools.pens.areaPen import AreaPen
    from fontTools.svgLib.path import parse_path
    subs = []
    for sp in MS.subpaths(d):
        raw = pathops.Path()
        parse_path(sp, raw.getPen())
        pen = AreaPen()
        raw.draw(pen)
        subs.append((pen.value, raw.bounds))
    if not subs:
        return []
    outer = max(subs, key=lambda t: abs(t[0]))[0]
    return [round(min(b[2] - b[0], b[3] - b[1]), 2) for v, b in subs if v * outer < 0]


def tiles():
    """Safe area and rendered contrast for each icon in each holder, color and size."""
    jobs, meta = [], {}
    for n in D.ICONS:
        for shape in A.SHAPES:
            for color in A.TILE:
                for px in (40, 96):
                    id_ = f"t-{n}-{shape}-{color}-{px}"
                    jobs.append({"id": id_, "w": px, "h": px, "bg": "#7F7F7F", "html": A.tile_svg(n, shape, color, px)})
                    meta[id_] = (n, shape, color, px)
    render(jobs, "tile-jobs")
    import icons_common as RC
    out = {}
    for id_, (n, shape, color, px) in meta.items():
        img = np.array(Image.open(R / f"{id_}.png").convert("RGB")).astype(float)
        fill = np.array([int(A.TILE[color][0][i:i + 2], 16) for i in (1, 3, 5)], float)
        hp = RC.holder_path(shape, px)
        inside = np.array([[hp.contains((x + .5, y + .5)) for x in range(px)] for y in range(px)])
        for _ in range(2):
            pd = np.pad(inside, 1, constant_values=False)
            inside = pd[1:-1, 1:-1] & pd[:-2, 1:-1] & pd[2:, 1:-1] & pd[1:-1, :-2] & pd[1:-1, 2:]
        # a pixel counts as ink when it sits at least 40 percent of the way from the tile color to the
        # icon's ink color, so the antialiased edge of a round form's allowed 0.25-unit overshoot
        # does not count as ink outside the live area
        ink_rgb = np.array([int(C.COLORWAYS[A.TILE[color][1]][0][i:i + 2], 16) for i in (1, 3, 5)], float)
        full = np.abs(ink_rgb - fill).sum()
        ink = (np.abs(img - fill).sum(-1) >= 0.4 * full) & inside
        ys, xs = np.nonzero(ink)
        lo, hi = px * (1 - RC.LIVE_FRACTION) / 2, px * (1 + RC.LIVE_FRACTION) / 2
        bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        rmax = float(np.max(np.hypot(xs + .5 - px / 2, ys + .5 - px / 2))) / px
        ink_c = C.COLORWAYS[A.TILE[color][1]][0]
        row = {"bbox": bbox, "in_live_area": bool(bbox[0] >= lo - .5 and bbox[1] >= lo - .5 and bbox[2] <= hi + .5 and bbox[3] <= hi + .5),
               "r_max_share": round(rmax, 3), "ink_vs_tile": round(C.contrast(ink_c, A.TILE[color][0]), 2)}
        if A.TILE[color][1].endswith("Red"):
            row["red_vs_tile"] = round(C.contrast(C.RED, A.TILE[color][0]), 2)
        if shape == "Circle":
            row["in_circle_safe"] = bool(rmax <= RC.CIRCLE_SAFE + 0.5 / px)
        out[id_[2:]] = row
    # the avatar and the app tile at their own glyph scales
    for label, svgf, px, shape in (("avatar-400", C.CONTEXT / f"{C.DATE}_Moving-Part-Avatar-400.svg", 400, "Circle"),
                                   ("app-1024", A.app_file(), 1024, "Rounded-Square")):
        jobs2 = [{"id": label, "w": px, "h": px, "bg": "#7F7F7F", "html": svgf.read_text()}]
        render(jobs2, f"{label}-job")
        img = np.array(Image.open(R / f"{label}.png").convert("RGB")).astype(float)
        hp = RC.holder_path(shape, px)
        yy, xx = np.mgrid[0:px, 0:px]
        fill = np.array([18, 18, 18], float)
        ink = (np.abs(img - fill).sum(-1) > 24) & (np.abs(img - 127).sum(-1) > 12)
        if shape == "Circle":
            ink &= np.hypot(xx + .5 - px / 2, yy + .5 - px / 2) < px / 2 - 3
        else:
            ink &= (xx > px * .08) & (xx < px * .92) & (yy > px * .08) & (yy < px * .92)
        ys, xs = np.nonzero(ink)
        rmax = float(np.max(np.hypot(xs + .5 - px / 2, ys + .5 - px / 2))) / px
        margin = min(xs.min(), ys.min(), px - xs.max() - 1, px - ys.max() - 1) / px
        out[label] = {"r_max_share": round(rmax, 3), "margin_share": round(float(margin), 3),
                      "in_circle_safe": bool(rmax <= RC.CIRCLE_SAFE + 0.5 / px) if shape == "Circle" else None}
    return out


def main():
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    R.mkdir(parents=True, exist_ok=True)
    C.PX.mkdir(parents=True, exist_ok=True)
    masters = {(n, s, o): C.load(n, s, o) for n in D.ICONS for s in C.SIZES for o in (False, True)}
    jobs = []
    for (n, s, o), m in masters.items():
        U = C.UNITS[s]
        k = f"{n}-{s}-{int(o)}"
        if s == "Display":
            for px in (96, 48):
                jobs.append({"id": f"w{px}-{k}", "w": px, "h": px, "bg": C.WHITE, "html": mono(m, U, px)})
                jobs.append({"id": f"x{px}-{k}", "w": px, "h": px, "bg": C.WHITE, "html": mono(m, U, px, "removed")})
            jobs.append({"id": f"i96-{k}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono(m, U, 96, "ink")})
            jobs.append({"id": f"a96-{k}", "w": 96, "h": 96, "bg": C.WHITE, "html": mono(m, U, 96, "accent")})
        else:
            jobs.append({"id": f"w-{k}", "w": U, "h": U, "bg": C.WHITE, "html": mono(m, U, U)})
            jobs.append({"id": f"x-{k}", "w": U, "h": U, "bg": C.WHITE, "html": mono(m, U, U, "removed")})
            jobs.append({"id": f"i-{k}", "w": U, "h": U, "bg": C.WHITE, "html": mono(m, U, U, "ink")})
            jobs.append({"id": f"a-{k}", "w": U, "h": U, "bg": C.WHITE, "html": mono(m, U, U, "accent")})
            cw = "Charcoal-Red-Keyline" if o else "Charcoal-Red"
            jobs.append({"id": f"px-{k}", "w": U, "h": U, "bg": C.NEWS, "html": C.svg(m, U, cw)})
            jobs.append({"id": f"pxk-{k}", "w": U, "h": U, "bg": C.CHAR, "html": C.svg(m, U, "Newsprint-Red")})
    render(jobs, "jobs")
    # copy the 1x color renders for the board
    for n in D.ICONS:
        for s in ("24px", "16px"):
            for o in (False, True):
                k = f"{n}-{s}-{int(o)}"
                Image.open(R / f"px-{k}.png").save(C.PX / f"{C.DATE}_Moving-Part-{D.FILE_NAME[n]}-{s}{'-Open' if o else ''}.png")
                Image.open(R / f"pxk-{k}.png").save(C.PX / f"{C.DATE}_Moving-Part-{D.FILE_NAME[n]}-{s}{'-Open' if o else ''}-On-Charcoal.png")

    res = {"drawings": {}, "pairs16": {}, "pairs24": {}, "watch": {}, "cover": {}, "sets": {}, "contrast": {}, "hint": {}}
    # vector numbers for the display masters, at rest and open
    import icons_r2_moving_vector_check as V
    for n in D.ICONS:
        for o in (False, True):
            v = V.check(n, D.STEP if o else 0.0)
            m = masters[(n, "Display", o)]
            res["drawings"][f"{n}|Display|{'open' if o else 'rest'}"] = {
                "painted_vector": round(v["painted"], 3), "red_share_vector": round(v["red"], 3), "min_gap": round(v["min_gap"], 2),
                "overlap": v["overlap"], "box": [round(b, 2) for b in v["box"]], "com_vector": [round(c, 3) for c in v["com"]],
                "red_in_badge_zone": round(v["red_in_badge_zone"], 2), "pieces": v["pieces"],
                "counters": sorted(set(holes(m["ink"]) + holes(m["accent"])))}
    for n in D.ICONS:
        for o in (False, True):
            k = f"{n}-Display-{int(o)}"
            row = res["drawings"][f"{n}|Display|{'open' if o else 'rest'}"]
            w96 = cov(f"w96-{k}")
            row["density96"] = round(float(np.mean(w96)), 3)
            row["centroid96"] = [round(c, 3) for c in centroid(w96)]
            ti, ta = float(np.sum(cov(f"i96-{k}"))), float(np.sum(cov(f"a96-{k}")))
            row["red_share_96"] = round(ta / (ti + ta), 3)
    # hinted masters
    hrep = json.loads((C.SCRATCH / "hint-report.json").read_text())
    for n in D.ICONS:
        for s in ("24px", "16px"):
            for o in (False, True):
                k = f"{n}-{s}-{int(o)}"
                m = masters[(n, s, o)]
                w = cov(f"w-{k}")
                cr, dens = M.crisp(w)
                ti, ta = float(np.sum(cov(f"i-{k}"))), float(np.sum(cov(f"a-{k}")))
                pf = M.pixel_fit({"body": G.to_pathops(m["ink"]), "node": G.to_pathops(m["accent"])})
                hr = hrep[f"{n}|{s}|{'open' if o else 'rest'}"]
                res["drawings"][f"{n}|{s}|{'open' if o else 'rest'}"] = {
                    "crisp": cr, "density": dens, "pixel_fit_pass": (cr or 0) >= 0.60, "pixel_fit_vector": pf,
                    "red_share_px": round(ta / (ti + ta), 3), "min_gap_px": hr["min_gap_px"], "shift": hr["shift"],
                    "counters_px": sorted(set(holes(m["ink"]) + holes(m["accent"])))}
    # similarity within the set, at 16 and 24 px, at rest
    for s, key in (("16px", "pairs16"), ("24px", "pairs24")):
        for a, b in combinations(D.ICONS, 2):
            res[key][f"{a}|{b}"] = M.sim(cov(f"w-{a}-{s}-0"), cov(f"w-{b}-{s}-0"))
    # look-alikes: letters, "01", V5 marks and Material Symbols system glyphs
    import icons_measure as RM   # round one, read only: its glyph outline helper for "01"
    refs = {}
    for sz in (16, 24):
        rr = M.reference_svgs(sz)
        rr["chapter number 01"] = RM._glyphs_svg("01", sz, M.FONTS / "Inter-Tight-800-normal.ttf")
        refs[sz] = rr
    rj = [{"id": f"ref-{M.slug(nm)}-{sz}", "w": sz, "h": sz, "bg": C.WHITE, "html": svg} for sz, rr in refs.items() for nm, svg in rr.items()]
    render(rj, "ref-jobs")
    ms_names = sorted(set(SYSTEM + [g for v in WATCH_MS.values() for g in v] + list(NEAREST.values())))
    msc = render_ms(ms_names)
    for n in D.ICONS:
        for s, sz in (("16px", 16), ("24px", 24)):
            w = cov(f"w-{n}-{s}-0")
            for nm in WATCH_REF[n]:
                res["watch"][f"{n}|{nm}|{sz}"] = M.sim(w, cov(f"ref-{M.slug(nm)}-{sz}"))
            for g in sorted(set(SYSTEM + WATCH_MS[n])):
                res["watch"][f"{n}|ms:{g}|{sz}"] = M.sim(w, msc[(g, sz)])
            res["watch"][f"{n}|ms-nearest:{NEAREST[n]}|{sz}"] = M.sim(w, msc[(NEAREST[n], sz)])
    # Material Symbols' own weight at 24 and 48 px, for the benchmark comparison
    res["material_density"] = {f"{g}|{sz}": round(float(np.mean(msc[(g, sz)])), 3) for g in NEAREST.values() for sz in (24, 48)}
    # test 2, cover the red: red removed (and so White on Prussian with no red, the same silhouette)
    for n in D.ICONS:
        for s, idf, wid in (("16px", lambda nn: f"x-{nn}-16px-0", lambda nn: f"w-{nn}-16px-0"),
                            ("24px", lambda nn: f"x-{nn}-24px-0", lambda nn: f"w-{nn}-24px-0"),
                            ("48px", lambda nn: f"x48-{nn}-Display-0", lambda nn: f"w48-{nn}-Display-0")):
            x = cov(idf(n))
            own = M.sim(x, cov(wid(n)))["score"]
            others = {o: M.sim(x, cov(wid(o)))["score"] for o in D.ICONS if o != n}
            near = max(others.items(), key=lambda t: t[1])
            res["cover"][f"{n}|{s}"] = {"own_full": own, "nearest_other": near[0], "nearest_other_score": near[1],
                                        "pass_proxy": near[1] < 0.60 and own > near[1]}
    # sets
    d96 = [res["drawings"][f"{n}|Display|rest"]["density96"] for n in D.ICONS]
    med = float(np.median(d96))
    res["sets"]["density96"] = {"min": min(d96), "max": max(d96), "median": round(med, 3),
                                "band": [round(med * .85, 3), round(med * 1.15, 3)],
                                "outside_band": [n for n, v in zip(D.ICONS, d96) if not (med * .85 <= v <= med * 1.15)],
                                "painted_24_to_32": [n for n, v in zip(D.ICONS, d96) if not (.24 <= v <= .32)]}
    res["sets"]["centroid_max"] = max(max(abs(c) for c in res["drawings"][f"{n}|Display|rest"]["centroid96"]) for n in D.ICONS)
    res["sets"]["centroid_fail"] = [n for n in D.ICONS if max(abs(c) for c in res["drawings"][f"{n}|Display|rest"]["centroid96"]) > 0.12]
    res["sets"]["red_over_25"] = [n for n in D.ICONS if res["drawings"][f"{n}|Display|rest"]["red_share_vector"] > 0.25]
    res["sets"]["red_under_12"] = [n for n in D.ICONS if res["drawings"][f"{n}|Display|rest"]["red_share_vector"] < 0.12]
    for key in ("pairs16", "pairs24"):
        worst = max(res[key].items(), key=lambda t: t[1]["score"])
        res["sets"][key] = {"over_060": [k for k, v in res[key].items() if v["score"] >= 0.60], "worst": [worst[0], worst[1]["score"]]}
    wv = [(k, v["score"]) for k, v in res["watch"].items() if "ms-nearest" not in k]
    res["sets"]["watch_over_060"] = [k for k, v in wv if v >= 0.60]
    res["sets"]["watch_worst"] = max(wv, key=lambda t: t[1])
    for s in ("24px", "16px"):
        cr = [res["drawings"][f"{n}|{s}|rest"]["crisp"] for n in D.ICONS]
        res["sets"][f"crisp_{s}"] = {"min": min(cr), "max": max(cr), "under_060": [n for n, v in zip(D.ICONS, cr) if v < 0.60]}
        cro = [res["drawings"][f"{n}|{s}|open"]["crisp"] for n in D.ICONS]
        res["sets"][f"crisp_{s}_open"] = {"min": min(cro), "max": max(cro)}
        gaps = [res["drawings"][f"{n}|{s}|{st}"]["min_gap_px"] for n in D.ICONS for st in ("rest", "open")]
        res["sets"][f"min_gap_{s}"] = min(gaps)
        res["sets"][f"gap_under_cut_{s}"] = [f"{n}|{st}" for n in D.ICONS for st in ("rest", "open")
                                             if res["drawings"][f"{n}|{s}|{st}"]["min_gap_px"] < (2.0 if s == "24px" else 1.0) - 0.05]
        res["sets"][f"vector_pixel_fit_{s}"] = min((res["drawings"][f"{n}|{s}|rest"]["pixel_fit_vector"]["share"] or 1) for n in D.ICONS)
    res["sets"]["cover_fail"] = [k for k, v in res["cover"].items() if not v["pass_proxy"]]
    # one-color row of all ten at 24 px: weight spread
    d24 = [float(np.mean(cov(f"w-{n}-24px-0"))) for n in D.ICONS]
    m24 = float(np.median(d24))
    res["sets"]["row24_density"] = {"values": dict(zip(D.ICONS, [round(v, 3) for v in d24])), "median": round(m24, 3),
                                    "outside_15": [n for n, v in zip(D.ICONS, d24) if not (m24 * .85 <= v <= m24 * 1.15)]}
    # contrast
    for nm, a, b in (("Charcoal ink on Newsprint", C.CHAR, C.NEWS), ("Charcoal ink on White", C.CHAR, C.WHITE),
                     ("Newsprint ink on Charcoal", C.NEWS, C.CHAR), ("White ink on Prussian", C.WHITE, C.PRUS),
                     ("Red on Newsprint", C.RED, C.NEWS), ("Red on White", C.RED, C.WHITE), ("Red on Charcoal", C.RED, C.CHAR),
                     ("Red against its Charcoal keyline", C.RED, C.CHAR), ("Charcoal keyline on Newsprint", C.CHAR, C.NEWS),
                     ("Red on Prussian (not used)", C.RED, C.PRUS)):
        res["contrast"][nm] = round(C.contrast(a, b), 2)
    res["tiles"] = tiles()
    res["sets"]["tiles_outside_live"] = [k for k, v in res["tiles"].items() if v.get("in_live_area") is False]
    res["sets"]["tiles_outside_circle_safe"] = [k for k, v in res["tiles"].items() if v.get("in_circle_safe") is False]
    MEAS.write_text(json.dumps(res, indent=1))
    for k, v in res["sets"].items():
        print(k, v)


if __name__ == "__main__":
    main()
