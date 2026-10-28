"""Render every cell of the Identity Masters Board with Chromium at device scale 1, build the
overlays and measure what the board reports.

Measures, all from the 1x renders unless marked vector:
  pixel fit (D1-17)    share of ink pixels at 90 percent coverage or more, one color on Newsprint,
                       at 16 and 24 px; a master passes at 0.60 or more
  silhouette at 16 px  counters that stay open: enclosed background regions at 50 percent coverage
  one color            the largest distance, in RGB units, of any pixel from the line between the
                       surface and the ink; antialiasing stays on the line, a second color leaves it
  contrast             median WCAG contrast of ink pixels against the surface, and of the
                       ampersand's (or lever's) pixels, measured with the letters hidden
  red on Prussian      Pillar Red pixels in any cell on Prussian

Run: python3 -I p2_render.py   (after the master scripts)
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p1_render as R1  # noqa: E402
import p2_pairs as PP  # noqa: E402
from PIL import Image  # noqa: E402

PNG = P.BOARD_DIR
MEAS = P.HANDOFF / f"{P.DATE}_Identity-Masters-Measurements.json"
SURF = {s[0]: s for s in o.SURFACES}
ALL_SURF = ["newsprint", "white", "charcoal", "prussian"]


def modes_for(p, s):
    modes = p.get("modes", ["color", "mono"])
    return ["mono"] if s == "prussian" else modes


def jobs_for_pair(p):
    jobs = []
    for vk in ("orig", "prop"):
        for s in p.get("surfaces", ALL_SURF):
            for m in modes_for(p, s):
                for size in PP.SIZES + ["display"]:
                    inner, vb = p[vk][size]
                    h = size if size != "display" else p["display"]
                    fg, v = R1.css_vars(s, m)
                    if p.get("glyph") == "amp" and m == "color" and s != "prussian":
                        fg = o.RED
                    svg, W, H = R1.cell(inner, vb, h, fg, v, SURF[s][2])
                    jobs.append({"id": f"{p['id']}__{vk}__{s}__{m}__{size}", "w": W, "h": H, "bg": SURF[s][2], "html": svg,
                                 "out": f"{p['item'].lower()}/{p['id']}/{vk}__{s}__{m}__{size}.png"})
                    if m == "color" and size in (16, 24) and p.get("glyph") != "amp" and s != "prussian":
                        inner2 = inner.replace('fill="currentColor"', 'fill="none"').replace('stroke="var(--line,#5D636D)"', 'stroke="none"')
                        inner2 = re.sub(r'<g fill="var\(--link,#5D636D\)">.*?</g>', '', inner2)
                        inner2 = re.sub(r'<g stroke="var\(--link,#5D636D\)".*?</g>', '', inner2)
                        svg2, W2, H2 = R1.cell(inner2, vb, h, fg, v, SURF[s][2])
                        jobs.append({"id": f"meas__{p['id']}__{vk}__{s}__{size}", "w": W2, "h": H2, "bg": SURF[s][2], "html": svg2, "out": None})
    if p.get("overlay"):
        for size in PP.SIZES + ["display"]:
            h = size if size != "display" else p["display"]
            (io, vbo), (ip, vbp) = p["orig"][size], p["prop"][size]
            mono = "--amp:currentColor;--lever:currentColor;--link:currentColor;--line:currentColor;"
            if p["overlay"] == "common":
                k = h / vbo[3]
                U = [min(vbo[0], vbp[0]), min(vbo[1], vbp[1])]
                U += [max(vbo[0] + vbo[2], vbp[0] + vbp[2]) - U[0], max(vbo[1] + vbo[3], vbp[1] + vbp[3]) - U[1]]
                for vk, inner, vbx in (("orig", io, vbo), ("prop", ip, vbp)):
                    vbs = " ".join(f"{t:g}" for t in vbx)
                    inner = f'<svg x="{vbx[0]:g}" y="{vbx[1]:g}" width="{vbx[2]:g}" height="{vbx[3]:g}" viewBox="{vbs}" overflow="hidden">{inner}</svg>'
                    svg, W, H = R1.cell(inner, U, U[3] * k, o.CHAR, mono, o.WHITE)
                    jobs.append({"id": f"ov__{p['id']}__{vk}__{size}", "w": W, "h": H, "bg": o.WHITE, "html": svg, "out": None})
            else:
                for vk, (inner, vb) in (("orig", (io, vbo)), ("prop", (ip, vbp))):
                    svg, W, H = R1.cell(inner, vb, h, o.CHAR, mono, o.WHITE)
                    jobs.append({"id": f"ov__{p['id']}__{vk}__{size}", "w": W, "h": H, "bg": o.WHITE, "html": svg, "out": None})
    return jobs


# ---------------------------------------------------------------- minimum sizes (I8) and Prussian (I9)

A = P.ASSETS
MIN_ITEMS = [
    ("L1", "L1 wordmark", (PP.sp("wordmark"), "width", 120), (A / "wordmark/20261028_Wordmark-16px-Master.svg", "height", 16)),
    ("L1C", "L1 wordmark, condensed", (PP.sp("wordmark"), "width", 120), (A / "wordmark-condensed/20261028_Wordmark-Condensed-16px-Master.svg", "height", 16)),
    ("L2", "L2 stacked", (PP.sp("stacked"), "width", 72), (A / "lockups/20261028_L2-Stacked-Master.svg", "width", 90)),
    ("L3", "L3 horizontal", (PP.sp("l3"), "width", 192), (A / "lockups/20261028_L3-Horizontal-Master.svg", "width", 196)),
    ("L8", "L8 monogram", (PP.sp("monogram"), "width", 48), (A / "lockups/20261028_L8-Monogram-Master.svg", "width", 48)),
    ("AMP", "Ampersand, freestanding", (PP.sp("amp-16"), "height", 16), (A / "ampersand/20261028_Amp-B-16px-Master.svg", "height", 16)),
    ("LOCK", "Lockmark", (PP.sp("lockmark"), "height", 16), (A / "lockmark/20261028_Lockmark-16px-Master.svg", "height", 16)),
    ("HINGE", "Hinge diagram, compact", (PP.sp("hinge"), "width", 245), (A / "hinge/20261028_Hinge-Diagram-V2-Compact-Master.svg", "width", 245)),
    ("BADGE", "Hinge-circle badge", (o.ROOT / "work/boards/phase-1/symbols/badge/20261021_Hinge-Badge-16px-Master.svg", "height", 16), (A / "badge/20261028_Hinge-Badge-16px-Master.svg", "height", 16)),
]
PRUSSIAN_ITEMS = [
    ("wordmark", "Wordmark", A / "prussian/20261028_Wordmark-Display-Master-Prussian-White.svg", 48),
    ("wordmark16", "Wordmark, 16 px master", A / "prussian/20261028_Wordmark-16px-Master-Prussian-White.svg", 16),
    ("wordmarkc", "Wordmark, condensed", A / "prussian/20261028_Wordmark-Condensed-Display-Master-Prussian-White.svg", 48),
    ("l2", "L2 stacked", A / "prussian/20261028_L2-Stacked-Master-Prussian-White.svg", 72),
    ("l3", "L3 horizontal", A / "prussian/20261028_L3-Horizontal-Master-Prussian-White.svg", 56),
    ("l8", "L8 monogram", A / "prussian/20261028_L8-Monogram-Master-Prussian-White.svg", 48),
    ("amp", "Ampersand B", A / "prussian/20261028_Amp-B-Display-Master-Prussian-White.svg", 48),
    ("amp16", "Ampersand B, 16 px master", A / "prussian/20261028_Amp-B-16px-Master-Prussian-White.svg", 16),
    ("lock24", "Lockmark, 24 px master", A / "prussian/20261028_Lockmark-24px-Master-Prussian-White.svg", 24),
    ("lock", "Lockmark", A / "prussian/20261028_Lockmark-Master-V5-Prussian-White.svg", 72),
    ("hinge", "Hinge diagram V2, compact", A / "prussian/20261028_Hinge-Diagram-V2-Compact-Master-Prussian-White.svg", 72),
    ("badge", "Hinge-circle badge", A / "prussian/20261028_Hinge-Badge-Display-Master-Prussian-White.svg", 48),
    ("badge16", "Badge, 16 px master", A / "prussian/20261028_Hinge-Badge-16px-Master-Prussian-White.svg", 16),
]


def min_jobs():
    jobs = []
    for mid, lab, orig, prop in MIN_ITEMS:
        for vk, (src, by, size) in (("orig", orig), ("prop", prop)):
            inner, vb = P.svg_parts(src)
            h = size if by == "height" else size * vb[3] / vb[2]
            w = size if by == "width" else None
            for s in ALL_SURF:
                for m in (["mono"] if s == "prussian" else ["color", "mono"]):
                    fg, v = R1.css_vars(s, m)
                    if mid in ("AMP", "BADGE") and m == "color":
                        fg = o.RED
                    svg, W, H = R1.cell(inner, vb, h, fg, v, SURF[s][2], w=w)
                    jobs.append({"id": f"min__{mid}__{vk}__{s}__{m}", "w": W, "h": H, "bg": SURF[s][2], "html": svg, "out": f"i8/{mid}__{vk}__{s}__{m}.png"})
    return jobs


def prussian_jobs():
    jobs = []
    for key, lab, f, h in PRUSSIAN_ITEMS:
        inner, vb = P.svg_parts(f)
        svg, W, H = R1.cell(inner, vb, h, o.WHITE, "", o.PRUS)
        jobs.append({"id": f"pru__{key}", "w": W, "h": H, "bg": o.PRUS, "html": svg, "out": f"i9/{key}.png"})
    # V5 today on Prussian, red ampersand, two labeled cells only (ruled out by Rule 05.3)
    inner, vb = P.svg_parts(PP.sp("wordmark"))
    for h in (16, 96):
        svg, W, H = R1.cell(inner, vb, h, o.WHITE, f"--amp:{o.RED};", o.PRUS)
        jobs.append({"id": f"pru__v5today__{h}", "w": W, "h": H, "bg": o.PRUS, "html": svg, "out": f"i9/v5today__{h}.png"})
    return jobs


def extra_jobs():
    """Same-width comparison for I5, the redrawn letters, the B construction view at 2x, the
    hinge three ways."""
    jobs = []
    for nm, f in (("today", A / "wordmark/20261028_Wordmark-Display-Master.svg"), ("condensed", A / "wordmark-condensed/20261028_Wordmark-Condensed-Display-Master.svg")):
        inner, vb = P.svg_parts(f)
        for wpx in (360, 180):
            fg, v = R1.css_vars("newsprint", "color")
            svg, W, H = R1.cell(inner, vb, wpx * vb[3] / vb[2], fg, v, o.NEWS, w=wpx)
            jobs.append({"id": f"sw__{nm}__{wpx}", "w": W, "h": H, "bg": o.NEWS, "html": svg, "out": f"i5/samewidth__{nm}__{wpx}.png"})
        for hpx in (40,):
            fg, v = R1.css_vars("newsprint", "color")
            svg, W, H = R1.cell(inner, vb, hpx, fg, v, o.NEWS)
            jobs.append({"id": f"sh__{nm}__{hpx}", "w": W, "h": H, "bg": o.NEWS, "html": svg, "out": f"i5/sameheight__{nm}__{hpx}.png"})
    return jobs


# ---------------------------------------------------------------- measurement

def cov(img, bg, ink):
    return R1.cov_np(img, bg, ink)[0]


def holes_16(path, bg, ink):
    c = cov(Image.open(path), bg, ink)
    m = c > 0.5
    h, w = m.shape
    seen = np.zeros_like(m)
    count = 0
    for y in range(h):
        for x in range(w):
            if m[y, x] or seen[y, x]:
                continue
            stack, touches = [(y, x)], False
            seen[y, x] = True
            while stack:
                a, b = stack.pop()
                if a in (0, h - 1) or b in (0, w - 1):
                    touches = True
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    aa, bb = a + da, b + db
                    if 0 <= aa < h and 0 <= bb < w and not m[aa, bb] and not seen[aa, bb]:
                        seen[aa, bb] = True
                        stack.append((aa, bb))
            if not touches:
                count += 1
    return count


def off_line(path, bg, ink):
    """Largest RGB distance of any pixel from the surface-to-ink line (0 = one color exactly)."""
    a = np.asarray(Image.open(path).convert("RGB"), dtype=float)
    b, i = np.array(o.hexrgb(bg), float), np.array(o.hexrgb(ink), float)
    d = i - b
    t = np.clip(((a - b) @ d) / float(d @ d), 0, 1)
    proj = b + t[..., None] * d
    return round(float(np.sqrt(((a - proj) ** 2).sum(axis=2)).max()), 1)


def ink_contrast(path, bg, ink):
    r = R1.red_stats(path, bg, ink)
    return r.get("median_contrast")


def red_pixels(path):
    a = np.asarray(Image.open(path).convert("RGB"), dtype=int)
    red = np.array(o.hexrgb(o.RED))
    return int((np.abs(a - red).sum(axis=2) < 60).sum())


def main():
    pairs = PP.pairs()
    jobs = []
    for p in pairs:
        jobs += jobs_for_pair(p)
    jobs += min_jobs() + prussian_jobs() + extra_jobs()
    print("jobs", len(jobs))
    raw = P.SCRATCH / "board_raw"
    P.render([{k: j[k] for k in ("id", "w", "h", "bg", "html")} for j in jobs], raw, "board2")
    cells = {}
    for j in jobs:
        src = raw / f"{j['id']}.png"
        if j["out"]:
            dst = PNG / j["out"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            Image.open(src).save(dst, optimize=True)
            cells[j["id"]] = {"src": str(dst.relative_to(o.ROOT / "work/boards")), "w": j["w"], "h": j["h"]}
    meas = {}
    for p in pairs:
        pm = {"label": p["label"], "item": p["item"]}
        if p.get("overlay"):
            for size in PP.SIZES + ["display"]:
                outp = PNG / p["item"].lower() / p["id"] / f"overlay__{size}.png"
                pm[f"overlay_{size}"] = R1.overlay(raw / f"ov__{p['id']}__orig__{size}.png", raw / f"ov__{p['id']}__prop__{size}.png", outp)
                im = Image.open(outp)
                cells[f"overlay__{p['id']}__{size}"] = {"src": str(outp.relative_to(o.ROOT / "work/boards")), "w": im.width, "h": im.height}
        for vk in ("orig", "prop"):
            v = {}
            for size in (16, 24):
                f = raw / f"{p['id']}__{vk}__newsprint__mono__{size}.png"
                if f.exists():
                    v[f"crisp_{size}"] = P.crisp_share(Image.open(f), o.NEWS, o.CHAR)
                    if size == 16:
                        v["open_counters_16"] = holes_16(f, o.NEWS, o.CHAR)
            ol, ct = {}, {}
            for s in p.get("surfaces", ALL_SURF):
                bg, ink = SURF[s][2], SURF[s][3]
                for size in (16, 24, 96):
                    f = raw / f"{p['id']}__{vk}__{s}__mono__{size}.png"
                    if f.exists():
                        ol[f"{s} {size}"] = off_line(f, bg, ink)
                        if size in (16, 24):
                            ct[f"{s} {size}"] = ink_contrast(f, bg, ink)
            v["one_color_max_offline"] = ol
            v["ink_contrast_median"] = ct
            rc = {}
            for s in ("newsprint", "white", "charcoal"):
                for size in (16, 24):
                    f = raw / (f"{p['id']}__{vk}__{s}__color__{size}.png" if p.get("glyph") == "amp" else f"meas__{p['id']}__{vk}__{s}__{size}.png")
                    if f.exists():
                        r = R1.red_stats(f, SURF[s][2], o.RED)
                        if r.get("ink_px"):
                            rc[f"{s} {size}"] = r["median_contrast"]
            v["red_median_contrast"] = rc
            red_on_prussian = 0
            for size in PP.SIZES + ["display"]:
                f = raw / f"{p['id']}__{vk}__prussian__mono__{size}.png"
                if f.exists():
                    red_on_prussian += red_pixels(f)
            v["red_pixels_on_prussian"] = red_on_prussian
            pm[vk] = v
        meas[p["id"]] = pm
    # I8 and I9 measures
    mins = {}
    for mid, lab, _, _ in MIN_ITEMS:
        for vk in ("orig", "prop"):
            f = raw / f"min__{mid}__{vk}__newsprint__mono.png"
            im = Image.open(f)
            mins[f"{mid} {vk}"] = {"w": im.width, "h": im.height, "crisp": P.crisp_share(im, o.NEWS, o.CHAR)}
    pru = {}
    for key, lab, f, h in PRUSSIAN_ITEMS:
        rp = raw / f"pru__{key}.png"
        pru[key] = {"label": lab, "red_px": red_pixels(rp), "one_color_max_offline": off_line(rp, o.PRUS, o.WHITE),
                    "median_contrast": ink_contrast(rp, o.PRUS, o.WHITE)}
    for h in (16, 96):
        pru[f"v5today_{h}"] = {"red_px": red_pixels(raw / f"pru__v5today__{h}.png"),
                               "red_median_contrast": R1.red_stats(raw / f"pru__v5today__{h}.png", o.PRUS, o.RED).get("median_contrast")}
    data = {"note": "Phase 2 identity masters, October 28, 2026. Chromium at device scale 1 on Linux. Crisp share: ink pixels at 90 percent coverage or more, over ink pixels at 10 percent or more (D1-17 passes at 0.60). "
                    "Open counters: enclosed background regions at 16 px. One color: largest RGB distance of a pixel from the surface-to-ink line. Contrast: median WCAG contrast of ink pixels against the surface.",
            "pairs": meas, "minimums": mins, "prussian": pru}
    P.save_json(MEAS, data)
    P.save_json(P.SCRATCH / "manifest2.json", {"cells": cells})
    print("cells", len(cells))


if __name__ == "__main__":
    main()
