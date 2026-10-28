"""Concept 3, Public sign, stage 2: render and measure every check.

Run: python3 -I icons_r2_sign_measure.py   (after icons_r2_sign_assets.py)
Writes work/boards/phase-2/icons-r2/public-sign/20261028_Public-Sign-Measurements.json.

Every raster comes from Chromium at device scale 1 (icons_r2_sign_render.js, which waits for web
fonts). The measures reuse Phase 1's symbols_measure.py and round one's icons_measure.py, imported
and unchanged:
  pixel fit     D1-17: at least 60 percent of ink pixels crisp (coverage over 0.9) at 16 and 24 px
  similarity    D1-16: mean of filled-silhouette overlap and blurred correlation, under 0.60
  look-alikes   the same score against letters, numerals, Phase 0 watch items and Material Symbols
  weight        ink and red together as a share of the field at 96 px; band 26 to 34 percent
  red share     red pixels over painted pixels at 96 px; ceiling 14 percent
  center of mass  offset of the ink's center from the field's center, as a share of the field;
                Phase 1 limit 12 percent
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
import icons_measure as RM  # noqa: E402  (round one, read only: ridge_widths, _glyphs_svg)
import icons_r2_sign_common as C  # noqa: E402
import numpy as np  # noqa: E402
import symbols_measure as PM  # noqa: E402  (Phase 1, read only)
from icons_r2_sign_common import CHAR, D, G, M, NEWS, PRUS, RED, WHITE  # noqa: E402
from PIL import Image  # noqa: E402

R = C.SCRATCH / "measure"
RENDER = HERE / "icons_r2_sign_render.js"
FONT_HEAD = '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0..1,0" rel="stylesheet">'

# Interface glyphs a reader could take an icon for (Material Symbols, Apache 2.0), with the
# brief's banned readings first: reload, sync, refresh, expand, crop, record, notification, add,
# play, pause, plus the readings the stage 1 test and notes found.
MATERIAL = ["sync", "refresh", "autorenew", "cached", "repeat", "loop", "swap_horiz", "open_in_full", "crop", "crop_free",
            "radio_button_checked", "notifications", "add", "play_arrow", "pause", "home", "house", "open_in_new", "edit_square",
            "mic", "podium", "record_voice_over", "description", "sim_card", "payments", "how_to_vote", "inbox", "print",
            "stairs", "trending_up", "door_open", "exit_to_app", "meeting_room", "link", "favorite", "check_box",
            "do_not_disturb_on", "camera", "tv", "photo_camera", "directions_bike", "mood"]
LETTERS = [("C", "letter C"), ("D", "letter D"), ("G", "letter G"), ("H", "letter H"), ("L", "letter L"), ("Q", "letter Q"),
           ("Z", "letter Z"), ("n", "letter n"), ("i", "letter i"), ("2", "numeral 2"), ("01", "chapter number 01"),
           ("θ", "letter theta"), ("Ω", "letter omega")]


def mono_svg(lay, size, px, mode="full", ink="#000000"):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {size} {size}">']
    if mode in ("full", "ink", "idle"):
        parts.append(f'<path d="{G.d_of(lay["ink"])}" fill="{ink}"/>')
    if mode in ("full", "accent"):
        parts.append(f'<path d="{G.d_of(lay["accent"])}" fill="{ink}"/>')
    parts.append("</svg>")
    return "".join(parts)


def lay_for(name, size):
    if size in (16, 24):
        return M.master(name, size), size
    return D.display(name), 24


def cov(id_, bg=C.WHITE, fg="#000000"):
    return PM.load_cov(R / f"{id_}.png", bg, fg)


def render(jobs, head=""):
    R.mkdir(parents=True, exist_ok=True)
    jp = C.SCRATCH / "measure-jobs.json"
    jp.write_text(json.dumps(jobs))
    args = ["node", str(RENDER), str(jp), str(R)]
    if head:
        hp = C.SCRATCH / "measure-head.html"
        hp.write_text(head)
        args.append(str(hp))
    subprocess.run(args, check=True)


def text_glyph_svg(text, size):
    """The string in Inter Tight 800, or Inter 700 where Inter Tight lacks the glyph."""
    for font in (PM.FONTS / "Inter-Tight-800-normal.ttf", PM.FONTS / "Inter-700-normal.ttf"):
        try:
            return RM._glyphs_svg(text, size, font)
        except KeyError:
            continue
    return None


def components(mask, min_px=1):
    """Separate parts (4-connected), counting only parts of at least min_px pixels."""
    lab, sizes = PM.components(mask.tolist())
    return sum(1 for v in sizes.values() if v >= min_px)


# The display counts come from the 96 px render thresholded at half coverage, where antialiasing
# leaves specks of a pixel or two at joins; parts and holes under 1 square unit (6 px) are ignored.
D96_MIN_PX = 6


def holes(mask, min_px=1):
    """Enclosed background regions of at least min_px pixels: background components that do not
    touch the border."""
    h, w = mask.shape
    bg = ~mask
    seen = np.zeros_like(bg)
    count = 0
    for y in range(h):
        for x in range(w):
            if bg[y, x] and not seen[y, x]:
                stack, touch, n = [(x, y)], False, 0
                seen[y, x] = True
                while stack:
                    a, b = stack.pop()
                    n += 1
                    if a in (0, w - 1) or b in (0, h - 1):
                        touch = True
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = a + dx, b + dy
                        if 0 <= xx < w and 0 <= yy < h and bg[yy, xx] and not seen[yy, xx]:
                            seen[yy, xx] = True
                            stack.append((xx, yy))
                if not touch and n >= min_px:
                    count += 1
    return count


def straight_edges(path):
    from symbols_geom import flatten_segments
    xs, ys = [], []
    for seg in flatten_segments(path):
        if seg[0] == "L":
            (x0, y0), (x1, y1) = seg[1], seg[2]
            if abs(x0 - x1) < 1e-6 and abs(y0 - y1) > 1e-6:
                xs.append(x0)
            elif abs(y0 - y1) < 1e-6 and abs(x0 - x1) > 1e-6:
                ys.append(y0)
    return xs, ys


def main():
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    jobs = []
    for n in D.ICONS:
        for s in (16, 24):
            lay, _ = lay_for(n, s)
            for mode in ("full", "ink", "accent", "idle"):
                jobs.append({"id": f"{mode}-{n}-{s}", "w": s, "h": s, "bg": C.WHITE, "html": mono_svg(lay, s, s, mode)})
            # White on Prussian, red removed (test 2)
            jobs.append({"id": f"prus-{n}-{s}", "w": s, "h": s, "bg": PRUS, "html": mono_svg(lay, s, s, "idle", WHITE)})
        disp = D.display(n)
        for px in (48, 96):
            for mode in ("full", "ink", "accent", "idle"):
                jobs.append({"id": f"{mode}-{n}-d{px}", "w": px, "h": px, "bg": C.WHITE, "html": mono_svg(disp, 24, px, mode)})
        jobs.append({"id": f"prus-{n}-d48", "w": 48, "h": 48, "bg": PRUS, "html": mono_svg(disp, 24, 48, "idle", WHITE)})
    refs = {}
    for s in (16, 24, 48):
        rr = PM.reference_svgs(s) if s in (16, 24) else {}
        for text, nm in LETTERS:
            sv = text_glyph_svg(text, s)
            if sv:
                rr[nm] = sv
        for g in MATERIAL:
            rr[f"Material {g}"] = f'<span class="ms" style="font-size:{s}px;width:{s}px;height:{s}px">{g}</span>'
        refs[s] = rr
        for nm, sv in rr.items():
            jobs.append({"id": f"ref-{PM.slug(nm)}-{s}", "w": s, "h": s, "bg": C.WHITE, "html": sv})
    render(jobs, FONT_HEAD)

    res = {"icons": {}, "pairs": {}, "pairs_idle": {}, "lookalike": {}, "test2": {}, "contrast": {}, "sets": {}, "tiles": {}, "spec": {}}
    for n in D.ICONS:
        row = {}
        for s in (16, 24):
            full = cov(f"full-{n}-{s}")
            cr, dens = PM.crisp(full)
            acc_m = M.mask(lay_for(n, s)[0]["accent"], s)
            ink_m = M.mask(lay_for(n, s)[0]["ink"], s)
            both = ink_m | acc_m
            dmask = np.array(cov(f"full-{n}-d96")) > 0.5
            row[f"m{s}"] = {"crisp": cr, "density": dens, "pixel_fit_pass": (cr or 0) >= 0.60,
                            "red_plus": M.red_plus(acc_m), "components": components(both), "holes": holes(both),
                            "components_display": components(dmask, D96_MIN_PX), "holes_display": holes(dmask, D96_MIN_PX),
                            "red_px": int(acc_m.sum()), "ink_px": int(ink_m.sum())}
        f96, i96, a96 = cov(f"full-{n}-d96"), cov(f"ink-{n}-d96"), cov(f"accent-{n}-d96")
        tot = sum(map(sum, f96))
        # The display SVG paints the accent over the ink, so the red a reader sees is the whole
        # accent; the share of it lying over ink is reported beside it.
        red_px = float(np.array(a96).sum())
        red_over_ink = float(np.minimum(np.array(a96), np.array(i96)).sum())
        cx = sum(f96[y][x] * x for y in range(96) for x in range(96)) / tot
        cy = sum(f96[y][x] * y for y in range(96) for x in range(96)) / tot
        wid = RM.ridge_widths(i96)
        arr = np.array(wid) / 4.0
        lay = D.display(n)
        allp = G.union(lay["ink"], lay["accent"])
        b = allp.bounds
        xs, ys = straight_edges(allp)
        row["d96"] = {"density": round(tot / 9216, 3), "red_share": round(red_px / tot, 3),
                      "red_over_ink_share": round(red_over_ink / red_px, 3) if red_px else 0.0,
                      "centroid": [round((cx + .5) / 96 - .5, 3), round((cy + .5) / 96 - .5, 3)],
                      "stroke_median_units": round(float(np.median(arr)), 2),
                      "stroke_share_at_bar": round(float(np.mean((arr >= 2.5) & (arr <= 3.6))), 3),
                      "bounds": [round(v, 2) for v in b],
                      "straight_edges_in_live": bool(all(1.999 <= v <= 22.001 for v in xs + ys)),
                      "round_overshoot_ok": bool(b[0] >= 1.75 - 1e-6 and b[1] >= 1.75 - 1e-6 and b[2] <= 22.25 + 1e-6 and b[3] <= 22.25 + 1e-6),
                      "badge_red_area": round(G.area(G.intersect(lay["accent"], G.rect(18, 0, 6, 6))), 3)}
        res["icons"][n] = row
    # similarity inside the set: full and idle, at 16, 24 and 48
    for s, tag in ((16, "16"), (24, "24"), (48, "d48")):
        for a, b2 in combinations(D.ICONS, 2):
            res["pairs"][f"{a}|{b2}|{s}"] = PM.sim(cov(f"full-{a}-{tag}"), cov(f"full-{b2}-{tag}"))
            res["pairs_idle"][f"{a}|{b2}|{s}"] = PM.sim(cov(f"idle-{a}-{tag}"), cov(f"idle-{b2}-{tag}"))
    # look-alikes: every icon, full and idle, against every reference at 16, 24 and 48
    for s, tag in ((16, "16"), (24, "24"), (48, "d48")):
        for n in D.ICONS:
            for mode in ("full", "idle"):
                best = []
                for nm in refs[s]:
                    sc = PM.sim(cov(f"{mode}-{n}-{tag}"), cov(f"ref-{PM.slug(nm)}-{s}"))
                    best.append((sc["score"], nm))
                best.sort(reverse=True)
                res["lookalike"][f"{n}|{mode}|{s}"] = [[round(v, 3), nm] for v, nm in best[:5]]
    # test 2, cover the red: red as ink, red removed, and White on Prussian keep the name
    for n in D.ICONS:
        t = {}
        for s, tag in ((16, "16"), (24, "24"), (48, "d48")):
            own = PM.sim(cov(f"full-{n}-{tag}"), cov(f"idle-{n}-{tag}"))["score"]
            nearest = max((PM.sim(cov(f"idle-{n}-{tag}"), cov(f"idle-{o}-{tag}"))["score"], o) for o in D.ICONS if o != n)
            pr = PM.load_cov(R / f"prus-{n}-{tag}.png", PRUS, WHITE)
            pr_nearest = max((PM.sim(pr, cov(f"idle-{o}-{tag}"))["score"], o) for o in D.ICONS if o != n)
            t[str(s)] = {"idle_vs_own_full": round(own, 3), "idle_nearest_other": [round(nearest[0], 3), nearest[1]],
                         "prussian_nearest_other": [round(pr_nearest[0], 3), pr_nearest[1]],
                         "idle_nearest_lookalike": res["lookalike"][f"{n}|idle|{s}"][0]}
        res["test2"][n] = t
    # sets
    d96 = [res["icons"][n]["d96"]["density"] for n in D.ICONS]
    med = float(np.median(d96))
    for s in (16, 24, 48):
        pr = {k: v for k, v in res["pairs"].items() if k.endswith(f"|{s}")}
        pri = {k: v for k, v in res["pairs_idle"].items() if k.endswith(f"|{s}")}
        worst = max(pr.items(), key=lambda kv: kv[1]["score"])
        worst_i = max(pri.items(), key=lambda kv: kv[1]["score"])
        res["sets"][str(s)] = {"pairs_over_060": sum(1 for v in pr.values() if v["score"] >= 0.60), "worst": [worst[0], worst[1]["score"]],
                               "idle_pairs_over_060": sum(1 for v in pri.values() if v["score"] >= 0.60), "idle_worst": [worst_i[0], worst_i[1]["score"]]}
    res["sets"]["density96"] = {"min": min(d96), "max": max(d96), "median": round(med, 3),
                                "dev": [round(min(d96) / med - 1, 3), round(max(d96) / med - 1, 3)]}
    # contrast
    for sname, label, bg in C.SURFACES:
        ink = NEWS if sname == "charcoal" else (WHITE if sname == "prussian" else CHAR)
        res["contrast"][f"ink|{sname}"] = round(C.contrast(ink, bg), 2)
    for sname, label, bg in C.SURFACES[:3]:
        res["contrast"][f"red|{sname}"] = round(C.contrast(RED, bg), 2)
    res["contrast"]["red|charcoal paper (Ballot)"] = round(C.contrast(RED, CHAR), 2)
    res["contrast"]["keyline|newsprint"] = round(C.contrast(CHAR, NEWS), 2)
    res["contrast"]["red|keyline"] = round(C.contrast(RED, CHAR), 2)
    res["tiles"] = measure_tiles()
    res["spec"] = {"bar_units": D.BAR, "head_units": D.HEAD, "node_units": D.NODE, "gap_units": D.GAP,
                   "red_ceiling": 0.14, "weight_band": [0.26, 0.34], "centroid_limit": 0.12, "similarity_limit": 0.60, "pixel_fit_limit": 0.60}
    C.MEASURE_JSON.write_text(json.dumps(res, indent=1))
    print("measured", len(jobs), "renders")
    summary(res)


def measure_tiles():
    """Safe area for every icon in every holder, color and size: ink inside the live area (half
    the side), and in the circle inside 80 percent of the diameter."""
    jobs, meta = [], {}
    for n in D.ICONS:
        for shape in C.HOLDER_SHAPES:
            for color in C.HOLDER_COLORS:
                for size in (28, 40, 96):
                    html, lay, sc, off = C.tile_svg(n, shape, color, size)
                    id_ = f"t-{n}-{shape}-{color}-{size}"
                    jobs.append({"id": id_, "w": size, "h": size, "bg": "#7F7F7F", "html": html})
                    meta[id_] = (n, shape, color, size)
    jp = C.SCRATCH / "tile-jobs.json"
    jp.write_text(json.dumps(jobs))
    rt = C.SCRATCH / "tiles"
    subprocess.run(["node", str(RENDER), str(jp), str(rt)], check=True)
    out = {}
    for id_, (n, shape, color, size) in meta.items():
        img = np.array(Image.open(rt / f"{id_}.png").convert("RGB")).astype(float)
        fill = np.array(PM.hexrgb(C.HOLDER_COLORS[color][0]), float)
        hp = C.holder_path(shape, size)
        inside = np.array([[hp.contains((x + .5, y + .5)) for x in range(size)] for y in range(size)])
        for _ in range(2):
            pd = np.pad(inside, 1, constant_values=False)
            inside = pd[1:-1, 1:-1] & pd[:-2, 1:-1] & pd[2:, 1:-1] & pd[1:-1, :-2] & pd[1:-1, 2:]
        ink = (np.abs(img - fill).sum(-1) > 24) & inside
        ys, xs = np.nonzero(ink)
        lo, hi = size * (1 - C.LIVE_FRACTION) / 2, size * (1 + C.LIVE_FRACTION) / 2
        bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        rmax = float(np.max(np.hypot(xs + .5 - size / 2, ys + .5 - size / 2))) / size
        # Tolerance: half a pixel of antialiasing plus the 0.25-unit overshoot the creative director
        # allows round forms (ruling 4); the vector check holds straight edges to 2 to 22 exactly.
        tol = 0.5 + 0.25 * (size * C.FIELD_FRACTION / 24 if size > 40 else 1.0)
        r = {"bbox": bbox, "in_live_area": bool(bbox[0] >= lo - tol and bbox[1] >= lo - tol and bbox[2] <= hi + tol and bbox[3] <= hi + tol),
             "margin_share": round(min(bbox[0], bbox[1], size - bbox[2], size - bbox[3]) / size, 3), "r_max_share": round(rmax, 3)}
        if shape == "Circle":
            r["in_circle_safe"] = bool(rmax <= C.CIRCLE_SAFE + 0.5 / size)
        out[id_[2:]] = r
    return out


def summary(res):
    for n in D.ICONS:
        r = res["icons"][n]
        d = r["d96"]
        print(f"{n:8s} crisp16 {r['m16']['crisp']} crisp24 {r['m24']['crisp']} dens {d['density']:.3f} red {d['red_share']:.3f} "
              f"com {d['centroid']} stroke {d['stroke_median_units']} plus16 {r['m16']['red_plus']} plus24 {r['m24']['red_plus']} "
              f"comp16 {r['m16']['components']}/{r['m16']['components_display']} holes16 {r['m16']['holes']}/{r['m16']['holes_display']} "
              f"comp24 {r['m24']['components']} holes24 {r['m24']['holes']} live {d['straight_edges_in_live']} over {d['round_overshoot_ok']}")
    for k, v in res["sets"].items():
        print(k, v)
    for n in D.ICONS:
        print(n, "look24", res["lookalike"][f"{n}|full|24"][:3], "idle24", res["lookalike"][f"{n}|idle|24"][:2])
    bad = [k for k, v in res["tiles"].items() if not v["in_live_area"] or v.get("in_circle_safe") is False]
    print("tiles outside safe area:", len(bad), bad[:6])


if __name__ == "__main__":
    main()
