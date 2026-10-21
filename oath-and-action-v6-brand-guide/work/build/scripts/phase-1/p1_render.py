"""Render every cell of the Identity Refinement Board with Chromium at device scale 1, build the
raster overlays, and measure what the board reports (red pixel contrast, solid share, joins).

Run: python3 -I p1_render.py
Writes PNGs to work/boards/phase-1/identity/png/ and the measurements to
work/handoffs/phase-1/20261021_Identity-Refinement-Measurements.json.
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
import p1_pairs as PP  # noqa: E402
from PIL import Image  # noqa: E402

PNG = o.OUT / "png"
MEAS = o.ROOT / "work/handoffs/phase-1/20261021_Identity-Refinement-Measurements.json"
SURF = {s[0]: s for s in o.SURFACES}


def css_vars(surface, mode, style=None, size=None):
    sid = surface
    fg = {"newsprint": o.CHAR, "white": o.CHAR, "charcoal": o.NEWS, "prussian": o.WHITE}[sid]
    dark = sid in ("charcoal", "prussian")
    if mode == "mono":
        v = "--amp:currentColor;--lever:currentColor;--link:currentColor;--line:currentColor;"
    else:
        link = o.WHITE if sid == "prussian" else (o.NEWS if sid == "charcoal" else o.STONE)
        v = f"--amp:{o.RED};--lever:{o.RED};--link:{link};--line:{o.NEWS if dark else o.STONE};"
    if sid == "prussian" and mode == "color" and style not in ("displayonly", "keyline", "newsprint", "v5red"):
        # Rule 05.3, treatment D: identity marks on Prussian are one color, White, ampersand and lever included
        v = "--amp:currentColor;--lever:currentColor;--link:currentColor;--line:currentColor;"
    if style == "displayonly":
        v += "--amp:currentColor;" if size in (16, 24) else f"--amp:{o.RED};"
    elif style == "newsprint":
        v += f"--amp:{o.NEWS};"
    elif style == "mono":
        v += "--amp:currentColor;"
    return fg, v


def cell(inner, vb, h, fg, vars_, bg, w=None, extra_style=""):
    w = w if w is not None else h * vb[2] / vb[3]
    vbs = " ".join(f"{v:g}" for v in vb)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{vbs}" width="{w:.3f}" height="{h:.3f}" '
           f'style="left:0;top:0;color:{fg};{vars_}{extra_style}">{inner}</svg>')
    return svg, math.ceil(w - 1e-6), math.ceil(h - 1e-6)


def disp_h(pair):
    return pair["display"]


def jobs_for_pair(p):
    jobs = []
    surfaces = p.get("surfaces", ["newsprint", "white", "charcoal", "prussian"])
    modes = p.get("modes", ["color", "mono"]) if p["panel"] != 10 else ["color"]
    for vk in ("orig", "prop"):
        var = p[vk]
        for s in surfaces:
            for m in modes:
                for size in PP.SIZES + ["display"]:
                    inner, vb = var[size]
                    h = size if size != "display" else disp_h(p)
                    style = p.get("prop_style") if vk == "prop" else None
                    fg, v = css_vars(s, m, style, size)
                    if p.get("glyph") == "amp" and m == "color" and s != "prussian":
                        fg = o.RED  # a freestanding ampersand is Pillar Red, except on Prussian (Rule 05.3, treatment D)
                    svg, W, H = cell(inner, vb, h, fg, v, SURF[s][2])
                    jobs.append({"id": f"{p['id']}__{vk}__{s}__{m}__{size}", "w": W, "h": H, "bg": SURF[s][2], "html": svg,
                                 "out": f"{p['id']}/{vk}__{s}__{m}__{size}.png"})
                    # isolated ampersand for red measurements (letters hidden), colour only
                    if m == "color" and p["panel"] in (2, 3, 4, 5, 6, 10) and size != "display" and p.get("glyph") != "amp":
                        inner2 = inner.replace('fill="currentColor"', 'fill="none"')
                        svg2, W2, H2 = cell(inner2, vb, h, fg, v, SURF[s][2])
                        jobs.append({"id": f"meas__{p['id']}__{vk}__{s}__{size}", "w": W2, "h": H2, "bg": SURF[s][2], "html": svg2,
                                     "out": f"_meas/{p['id']}__{vk}__{s}__{size}.png"})
    # overlays: both variants in Charcoal on White, same height (or a common frame)
    if p.get("overlay"):
        for size in PP.SIZES + ["display"]:
            h = size if size != "display" else disp_h(p)
            (io, vbo), (ip, vbp) = p["orig"][size], p["prop"][size]
            if p["overlay"] == "common":
                k = h / vbo[3]
                U = [min(vbo[0], vbp[0]), min(vbo[1], vbp[1])]
                U += [max(vbo[0] + vbo[2], vbp[0] + vbp[2]) - U[0], max(vbo[1] + vbo[3], vbp[1] + vbp[3]) - U[1]]
                hh = U[3] * k
                for vk, inner, vbx in (("orig", io, vbo), ("prop", ip, vbp)):
                    vbs = " ".join(f"{t:g}" for t in vbx)
                    inner = f'<svg x="{vbx[0]:g}" y="{vbx[1]:g}" width="{vbx[2]:g}" height="{vbx[3]:g}" viewBox="{vbs}" overflow="hidden">{inner}</svg>'
                    svg, W, H = cell(inner, U, hh, o.CHAR, "--amp:currentColor;--lever:currentColor;--link:currentColor;--line:currentColor;", o.WHITE)
                    jobs.append({"id": f"ov__{p['id']}__{vk}__{size}", "w": W, "h": H, "bg": o.WHITE, "html": svg, "out": f"_ov/{p['id']}__{vk}__{size}.png"})
            else:
                for vk, (inner, vb) in (("orig", (io, vbo)), ("prop", (ip, vbp))):
                    svg, W, H = cell(inner, vb, h, o.CHAR, "--amp:currentColor;--lever:currentColor;--link:currentColor;--line:currentColor;", o.WHITE)
                    jobs.append({"id": f"ov__{p['id']}__{vk}__{size}", "w": W, "h": H, "bg": o.WHITE, "html": svg, "out": f"_ov/{p['id']}__{vk}__{size}.png"})
    return jobs


# ---------------------------------------------------------------- minimum sizes (panel 9)

def l5_proposal():
    wm, _ = PP.svg_parts(PP.sp("wordmark"))
    tl, _ = PP.svg_parts(o.OUT / "01-reexport/20261021_Tagline-1-Line-Reexported.svg")
    inner = wm + f'<g transform="translate(0 143.04) scale(0.24)">{tl}</g>'
    return inner, [0, 0, 970.71, 175.0]


MIN_ITEMS = [
    # id, label, original (inner, vb, size_by, size), proposal
    ("L1", "L1 wordmark", (PP.sp("wordmark"), "width", 120), (PP.WM / "20261021_Wordmark-16px-Amp-B.svg", "height", 16)),
    ("L2", "L2 stacked", (PP.sp("stacked"), "width", 72), (o.OUT / "01-reexport/20261021_Stacked-L2-Reexported.svg", "width", 88)),
    ("L5", "L5 wordmark and tagline", (PP.sp("l5"), "width", 240), ("L5PROP", "width", 384)),
    ("AMP", "Freestanding ampersand", (PP.sp("amp-16"), "height", 16), (o.OUT / "05-amp-b/20261021_Amp-B-Small-Master-16px.svg", "height", 16)),
    ("LOCK", "Lockmark", (PP.sp("lockmark"), "height", 16), (o.OUT / "08-lockmark/20261021_Lockmark-16px-Master.svg", "height", 16)),
    ("HINGE", "Hinge diagram, compact", (PP.sp("hinge"), "width", 241), (o.OUT / "07-hinge/20261021_Hinge-Compact-Master_V2.svg", "width", 241)),
]


def min_jobs():
    jobs = []
    for mid, lab, orig, prop in MIN_ITEMS:
        for vk, (src, by, size) in (("orig", orig), ("prop", prop)):
            inner, vb = l5_proposal() if src == "L5PROP" else PP.svg_parts(src)
            h = size if by == "height" else size * vb[3] / vb[2]
            w = size if by == "width" else None
            for s in ("newsprint", "white", "charcoal", "prussian"):
                for m in ("color", "mono"):
                    fg, v = css_vars(s, m)
                    svg, W, H = cell(inner, vb, h, fg, v, SURF[s][2], w=w)
                    jobs.append({"id": f"min__{mid}__{vk}__{s}__{m}", "w": W, "h": H, "bg": SURF[s][2], "html": svg, "out": f"p09/{mid}__{vk}__{s}__{m}.png"})
    return jobs


def extra_jobs():
    jobs = []
    # same width comparison for the condensed panel: 360 px wide, Newsprint, colour
    for nm, f in (("current", PP.WM / "20261021_Wordmark-Display-Amp-B.svg"), ("condensed", o.OUT / "06-condensed/20261021_Wordmark-Condensed-7-5-To-1-Display.svg"),
                  ("condensed60", o.OUT / "06-condensed/20261021_Wordmark-Condensed-6-0-To-1-Display.svg")):
        inner, vb = PP.svg_parts(f)
        for wpx in (360, 180):
            fg, v = css_vars("newsprint", "color")
            svg, W, H = cell(inner, vb, wpx * vb[3] / vb[2], fg, v, o.NEWS, w=wpx)
            jobs.append({"id": f"sw__{nm}__{wpx}", "w": W, "h": H, "bg": o.NEWS, "html": svg, "out": f"p06/samewidth__{nm}__{wpx}.png"})
    # the hinge diagram three ways, for the side-by-side figure: V5, the dotted first draft, V2
    for nm, f in (("v5", PP.sp("hinge")), ("draft", o.OUT / "07-hinge/20261021_Hinge-Display-Master.svg"), ("v2", o.OUT / "07-hinge/20261021_Hinge-Display-Master_V2.svg")):
        inner, vb = PP.svg_parts(f)
        fg, v = css_vars("newsprint", "color")
        svg, W, H = cell(inner, vb, 640 * vb[3] / vb[2], fg, v, o.NEWS, w=640)
        jobs.append({"id": f"h3__{nm}", "w": W, "h": H, "bg": o.NEWS, "html": svg, "out": f"p07/threeup__{nm}.png"})
    return jobs


# ---------------------------------------------------------------- measurement

def cov_np(img, bg, ink):
    a = np.asarray(img.convert("RGB"), dtype=float)
    bgc = np.array(o.hexrgb(bg), dtype=float)
    inkc = np.array(o.hexrgb(ink), dtype=float)
    d = inkc - bgc
    c = ((a - bgc) @ d) / max(1e-9, float(d @ d))
    return np.clip(c, 0, 1), a


def lum_np(a):
    c = a / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c[..., 0] * 0.2126 + c[..., 1] * 0.7152 + c[..., 2] * 0.0722


def red_stats(path, bg, ink=None):
    img = Image.open(path)
    cov, a = cov_np(img, bg, ink or o.RED)
    L = lum_np(a)
    lb = o.lum(o.hexrgb(bg))
    con = (np.maximum(L, lb) + 0.05) / (np.minimum(L, lb) + 0.05)
    # a pixel counts as ink when it moves away from the surface at all
    m = np.abs(a - np.array(o.hexrgb(bg), dtype=float)).sum(axis=2) > 12
    n = int(m.sum())
    if not n:
        return {"ink_px": 0}
    vals = np.sort(con[m])
    solid = float(((cov >= 0.9) & m).sum()) / n
    return {"ink_px": n, "solid_share": round(solid, 2), "median_contrast": round(float(vals[n // 2]), 2),
            "max_contrast": round(float(vals[-1]), 2), "share_at_or_above_3": round(float((vals >= 3).mean()), 2)}


def ink_solid(path, bg, ink):
    cov, _ = cov_np(Image.open(path), bg, ink)
    m = cov > 0.1
    n = int(m.sum())
    return round(float((cov[m] >= 0.9).sum()) / n, 2) if n else None


def overlay(pa, pb, outp):
    A = Image.open(pa).convert("RGB")
    B = Image.open(pb).convert("RGB")
    w, h = max(A.width, B.width), max(A.height, B.height)
    ca = np.zeros((h, w)); cb = np.zeros((h, w))
    c1, _ = cov_np(A, o.WHITE, o.CHAR); c2, _ = cov_np(B, o.WHITE, o.CHAR)
    ca[:A.height, :A.width] = c1; cb[:B.height, :B.width] = c2
    m = np.minimum(ca, cb); oa = ca - m; ob = cb - m
    both = np.array(o.hexrgb(o.CHAR), float); oo = np.array((168, 172, 178), float); po = np.array(o.hexrgb(o.VERD), float)
    out = (255 * (1 - m - oa - ob))[..., None] + both * m[..., None] + oo * oa[..., None] + po * ob[..., None]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(outp, optimize=True)
    tot = float((ca > 0.1).sum() + (cb > 0.1).sum()) / 2 or 1
    return {"original_only_px": round(float(oa.sum()), 1), "proposal_only_px": round(float(ob.sum()), 1),
            "changed_share": round(float(oa.sum() + ob.sum()) / (2 * tot), 3)}


def glyph_boxes(inner):
    """Boxes of the letter glyphs in an SVG (paths filled currentColor), in viewBox units, left to right."""
    ds = re.findall(r'<path fill="currentColor" d="([^"]+)"', inner)
    if not ds:
        return None
    p = o.union(*[o.path_from_d(d) for d in ds])
    gl = o.split_glyphs(p)
    return sorted([o.bounds(g) for g in gl], key=lambda b: b[0])


def joins(p, vk, size, path):
    inner, vb = p[vk][size]
    boxes = glyph_boxes(inner)
    if not boxes or len(boxes) != 10:
        return None
    k = size / vb[3]
    img = Image.open(path)
    cov, _ = cov_np(img, o.NEWS, o.CHAR)
    out = {}
    for nm, (i, j) in (("T-H", (2, 3)), ("T-I", (6, 7)), ("I-O", (7, 8)), ("O-N", (8, 9))):
        a, b = boxes[i], boxes[j]
        y0 = (a[1]) * k
        y1 = (a[1] + (a[3] - a[1]) * (0.2 if nm.startswith("T") else 0.9)) * k
        best = 0.0
        for x in range(int(math.floor(a[2] * k)), int(math.ceil(b[0] * k)) + 1):
            if 0 <= x < cov.shape[1]:
                col = cov[int(y0):int(math.ceil(y1)), x]
                if col.size:
                    best = max(best, 1 - float(col.mean()))
        out[nm] = round(best, 2)
    return out


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    pairs = [p for p in PP.pairs() if not only or any(p["id"].startswith(x) for x in only)]
    jobs = []
    for p in pairs:
        jobs += jobs_for_pair(p)
    jobs += min_jobs() + extra_jobs()
    print("jobs", len(jobs))
    raw = o.SCRATCH / "board_raw"
    o.render([{k: j[k] for k in ("id", "w", "h", "bg", "html")} for j in jobs], raw, "board")
    PNG.mkdir(parents=True, exist_ok=True)
    manifest = {"cells": {}, "measures": {}}
    if only and (o.SCRATCH / "manifest.json").exists():
        manifest = json.loads((o.SCRATCH / "manifest.json").read_text())
    for j in jobs:
        src = raw / f"{j['id']}.png"
        dst = PNG / j["out"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if j["out"].startswith(("_meas", "_ov")):
            dst = o.SCRATCH / "board_tmp" / j["out"]
            dst.parent.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(dst, optimize=True)
        manifest["cells"][j["id"]] = {"src": str(dst.relative_to(o.ROOT / "work/boards")) if str(dst).startswith(str(o.ROOT)) else str(dst), "w": j["w"], "h": j["h"]}
    tmp = o.SCRATCH / "board_tmp"
    for p in pairs:
        pm = {}
        if p.get("overlay"):
            for size in PP.SIZES + ["display"]:
                outp = PNG / p["id"] / f"overlay__{size}.png"
                pm[f"overlay_{size}"] = overlay(tmp / f"_ov/{p['id']}__orig__{size}.png", tmp / f"_ov/{p['id']}__prop__{size}.png", outp)
                im = Image.open(outp)
                manifest["cells"][f"overlay__{p['id']}__{size}"] = {"src": str(outp.relative_to(o.ROOT / "work/boards")), "w": im.width, "h": im.height}
        # red stats: freestanding glyph pairs use the main colour cells, others the isolated cells
        rs = {}
        surfaces = p.get("surfaces", ["newsprint", "white", "charcoal", "prussian"])
        if p["panel"] in (1, 2, 3, 4, 5, 6, 10) and (p.get("glyph") == "amp" or p["panel"] != 1):
            for vk in ("orig", "prop"):
                for s in surfaces:
                    for size in (16, 24, 48, 96):
                        if p.get("glyph") == "amp":
                            f = PNG / p["id"] / f"{vk}__{s}__color__{size}.png"
                        else:
                            f = tmp / f"_meas/{p['id']}__{vk}__{s}__{size}.png"
                        ink = o.RED
                        st = p.get("prop_style") if vk == "prop" else None
                        if st == "newsprint":
                            ink = o.NEWS
                        elif st == "mono" or (st == "displayonly" and size in (16, 24)):
                            ink = o.WHITE
                        if f.exists():
                            rs[f"{vk} {s} {size}"] = red_stats(f, SURF[s][2], ink)
        if rs:
            pm["red"] = rs
        # solid share of ink, one colour on Newsprint, at 16 and 24
        sol = {}
        for vk in ("orig", "prop"):
            for size in (16, 24):
                f = PNG / p["id"] / f"{vk}__newsprint__mono__{size}.png"
                if f.exists():
                    sol[f"{vk} {size}"] = ink_solid(f, o.NEWS, o.CHAR)
        pm["solid_share_mono_newsprint"] = sol
        if p["panel"] in (2, 3, 4, 5, 6):
            jn = {}
            for vk in ("orig", "prop"):
                for size in (16, 24):
                    f = PNG / p["id"] / f"{vk}__newsprint__mono__{size}.png"
                    r = joins(p, vk, size, f)
                    if r:
                        jn[f"{vk} {size}"] = r
            pm["joins_openness"] = jn
        manifest["measures"][p["id"]] = pm
    # panel 9 red stats for the ampersand at minimum
    MEAS.write_text(json.dumps({"note": "Phase 1 identity refinement measurements, October 21, 2026. Chromium, device scale 1, Linux. "
                                        "Red stats: every pixel that differs from the surface, its WCAG contrast against the surface. "
                                        "Solid share: share of ink pixels at 90 percent coverage or more. Joins: lightest column between two letters, 1 = clear.",
                                "measures": manifest["measures"]}, indent=1))
    (o.SCRATCH / "manifest.json").write_text(json.dumps(manifest))
    print("cells", len(manifest["cells"]))


if __name__ == "__main__":
    main()
