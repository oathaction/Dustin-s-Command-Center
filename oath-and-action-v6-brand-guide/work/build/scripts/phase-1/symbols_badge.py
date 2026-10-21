"""Hinge-circle badge for decision S9 (Phase 1 proposal, design director).

Ampersand B inside the hinge diagram's ring, no words, one color per surface.
Writes three masters to work/boards/phase-1/symbols/badge/ and a measurement file.

  16 px: a pixel ring (1 px, drawn as whole pixels) around a hand-fitted 9 by 9 pixel
         ampersand drawn from ampersand B's 16 px master and outline.
  24 px: a 1 px pixel ring around ampersand B's own 16 px master, unchanged.
  Display: the V2 hinge ring proportions (ring 2.2 cap across, ampersand 1.25 cap tall)
         with the ring raised from 3.5 to 4.6 units so it reaches 1 px at 48 px.

Run: python3 -I symbols_badge.py   (after symbols_measure.py)
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import symbols_family as F  # noqa: E402
import symbols_measure as M  # noqa: E402
from symbols_geom import circle, d_of, empty, minus, rect, transform, union  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = HERE.parents[3]
IDENT = ROOT / "work/boards/phase-1/identity"
OUT = ROOT / "work/boards/phase-1/symbols/badge"
SCR = M.SCRATCH / "badge"
AMP_DRAWN = IDENT / "05-amp-b/20261021_Amp-B-Drawn-Master.svg"
AMP_16 = IDENT / "05-amp-b/20261021_Amp-B-Small-Master-16px.svg"
REF_PAGE = ROOT / "work/boards/phase-1/strategy/refs/20261021_Ref-Page-41.jpg"
REF_SEAL_BOX = (622, 305, 676, 359)   # first seal on page 41, in page pixels (880 by 495 render)

AMP_MAP_16 = [            # rows 3 to 11 of the 16 px field; '#' is ink
    "....###.........",
    "...##.##........",
    "...##.##........",
    "....###..##.....",
    "...####.##......",
    "..##..###.......",
    "..##...##.......",
    "..##...###......",
    "...#########....",
]
AMP_16_OFFSET = (1, 3)


def _d(svg_file):
    return re.search(r' d="([^"]+)"', svg_file.read_text()).group(1)


def _pixmap(rows, ox, oy):
    p = empty()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                p = union(p, rect(x + ox, y + oy, 1, 1))
    return p


def _pixring(n, r_out, r_in):
    c = n / 2
    p = empty()
    for y in range(n):
        for x in range(n):
            k = sum(r_in <= math.hypot(x + (sx + .5) / 4 - c, y + (sy + .5) / 4 - c) <= r_out for sy in range(4) for sx in range(4))
            if k >= 8:
                p = union(p, rect(x, y, 1, 1))
    return p


def _amp_path(svg_file, s, dx, dy):
    """Ampersand outline from an identity SVG, scaled and moved, as a pathops path."""
    from fontTools.svgLib.path import parse_path
    import pathops
    p = pathops.Path()
    parse_path(_d(svg_file), p.getPen())
    return transform(p, s, dx, dy)


def masters():
    m16 = {"ring": _pixring(16, 8, 7), "amp": _pixmap(AMP_MAP_16, *AMP_16_OFFSET)}
    m24 = {"ring": _pixring(24, 12, 11), "amp": _amp_path(AMP_16, 1, 5, 4)}
    # display: viewBox 240, ring radius 110 (2.2 cap across), stroke 4.6; ampersand 125 units tall (1.25 cap)
    s = 125 / 103.14
    w = 93.43 * s
    md = {"ring": minus(circle(120, 120, 112.3), circle(120, 120, 107.7)),
          "amp": _amp_path(AMP_DRAWN, s, 120 - w / 2, 120 - 125 / 2 + 1.43 * s)}
    return {16: m16, 24: m24, "display": md}


def svg_text(m, vb, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}"><title>{title}</title>'
            f'<path fill="currentColor" d="{d_of(union(m["ring"], m["amp"]))}"/></svg>\n')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SCR.mkdir(parents=True, exist_ok=True)
    ms = masters()
    files = {16: "20261021_Hinge-Badge-16px-Master.svg", 24: "20261021_Hinge-Badge-24px-Master.svg", "display": "20261021_Hinge-Badge-Display-Master.svg"}
    vbs = {16: 16, 24: 24, "display": 240}
    titles = {16: "Hinge-circle badge, 16 px master on the pixel grid (proposal for decision S9, Phase 1)",
              24: "Hinge-circle badge, 24 px master: ampersand B 16 px master in a 1 px ring (proposal for decision S9, Phase 1)",
              "display": "Hinge-circle badge, display master: ampersand B in the hinge diagram ring (proposal for decision S9, Phase 1)"}
    for k, f in files.items():
        (OUT / f).write_text(svg_text(ms[k], vbs[k], titles[k]))

    def badge_svg(size, ink="#000000"):
        key = size if size in (16, 24) else "display"
        vb = vbs[key]
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {vb} {vb}"><path d="{d_of(union(ms[key]["ring"], ms[key]["amp"]))}" fill="{ink}"/></svg>'

    fav = re.sub(r"<title>.*?</title>", "", AMP_16.read_text())
    fav16 = fav.replace("<svg ", '<svg width="14" height="16" style="position:absolute;left:1px;top:0;color:#000" ', 1)
    jobs = []
    for sz in (16, 24, 48, 96):
        jobs.append({"id": f"badge-{sz}", "w": sz, "h": sz, "bg": "#FFFFFF", "html": badge_svg(sz)})
        jobs.append({"id": f"nbadge-{sz}", "w": sz, "h": sz, "bg": M.NEWS, "html": badge_svg(sz, M.CHAR)})
        jobs.append({"id": f"kbadge-{sz}", "w": sz, "h": sz, "bg": M.CHAR, "html": badge_svg(sz, M.NEWS)})
        jobs.append({"id": f"rbadge-{sz}", "w": sz, "h": sz, "bg": M.NEWS, "html": badge_svg(sz, M.RED)})
    jobs.append({"id": "fav-16", "w": 16, "h": 16, "bg": "#FFFFFF", "html": fav16})
    jobs.append({"id": "nfav-16", "w": 16, "h": 16, "bg": M.NEWS, "html": fav16.replace("color:#000", "color:#121212")})
    fav24 = fav.replace("<svg ", '<svg width="14" height="16" style="position:absolute;left:5px;top:4px;color:#000" ', 1)
    jobs.append({"id": "fav-24", "w": 24, "h": 24, "bg": "#FFFFFF", "html": fav24})
    for p in F.PILLARS:
        for sz in (16, 24):
            jobs.append({"id": f"tile-{p}-{sz}", "w": sz, "h": sz, "bg": "#FFFFFF", "html": M.svg_layers(F.draw(p, "A", "tile", sz), sz, "#000000", "#FFFFFF")})
            if sz == 16:
                jobs.append({"id": f"ntile-{p}-16", "w": 16, "h": 16, "bg": M.NEWS, "html": M.svg_layers(F.draw(p, "A", "tile", 16), 16, M.CHAR, M.NEWS)})
    jp = SCR / "jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(M.RENDER), str(jp), str(SCR / "r")], check=True)
    R = SCR / "r"
    cw = lambda i: M.load_cov(R / f"{i}.png", "#FFFFFF", "#000000")
    res = {"masters": files, "sizes": {}, "similarity": {}, "contrast": {}, "pixel_fit": {}}
    for sz in (16, 24, 48, 96):
        cr, dens = M.crisp(cw(f"badge-{sz}"))
        res["sizes"][sz] = {"crisp": cr, "density": dens}
    c96 = cw("badge-96")
    tot = sum(map(sum, c96))
    cx = sum(v * (x + .5) for r in c96 for x, v in enumerate(r)) / tot
    cy = sum(v * (y + .5) for y, r in enumerate(c96) for v in r) / tot
    res["centroid_96"] = [round(cx / 96 - .5, 3), round(cy / 96 - .5, 3)]   # offset from field center, share of field
    for k in (16, 24):
        lay = {"body": ms[k]["ring"], "node": ms[k]["amp"]}
        res["pixel_fit"][k] = M.pixel_fit(lay)
        # the ampersand stays its own shape inside the ring, in both polarities
        sep = {}
        for pol, pre, bg, fg in (("dark_on_light", "n", M.NEWS, M.CHAR), ("light_on_dark", "k", M.CHAR, M.NEWS)):
            cc = M.load_cov(R / f"{pre}badge-{k}.png", bg, fg)
            lab, sizes = M.components([[v > .5 for v in r] for r in cc])
            ring_lab = lab[0][k // 2] or lab[k // 2][0]
            amp_labs = {lab[y][x] for y in range(k) for x in range(k) if lab[y][x] and math.hypot(x + .5 - k / 2, y + .5 - k / 2) < k / 2 - 2.5}
            sep[pol] = bool(ring_lab) and ring_lab not in amp_labs and len(amp_labs) >= 1
        res["pixel_fit"][f"{k}_amp_separate"] = sep
    for sz in (16, 24):
        res["similarity"][f"favicon|{sz}"] = M.sim(cw(f"badge-{sz}"), cw(f"fav-{sz}"))
        for p in F.PILLARS:
            res["similarity"][f"tile-{p}|{sz}"] = M.sim(cw(f"badge-{sz}"), cw(f"tile-{p}-{sz}"))
    # the generated reference seal, reduced to 16 and 24 px, for the seal question only
    ref = Image.open(REF_PAGE).convert("L").crop(REF_SEAL_BOX)
    for sz in (16, 24):
        r = ref.resize((sz, sz), Image.LANCZOS)
        px = r.load()
        bgl = 238.0
        cov = [[max(0.0, min(1.0, (bgl - px[x, y]) / (bgl - 18))) for x in range(sz)] for y in range(sz)]
        res["similarity"][f"seal|{sz}"] = M.sim(cw(f"badge-{sz}"), cov)
        res["similarity"][f"seal-vs-favicon|{sz}"] = M.sim(cw(f"fav-{sz}"), cov)
    for sname, bg, ink in (("newsprint", M.NEWS, M.RED), ("white", M.WHITE, M.RED), ("charcoal", M.CHAR, M.RED), ("prussian", M.PRUS, M.WHITE)):
        res["contrast"][sname] = {"ink": ink, "ratio": round(M.contrast(ink, bg), 2)}
    cr, _ = M.crisp(M.load_cov(R / "rbadge-16.png", M.NEWS, M.RED))
    res["red_on_newsprint_16_crisp"] = cr
    (OUT / "20261021_Hinge-Badge-Measurements.json").write_text(json.dumps(res, indent=1))
    for f in ("nbadge-16", "nbadge-24", "nfav-16", "ntile-explain-16", "ntile-act-16"):
        Image.open(R / f"{f}.png").save(ROOT / "work/boards/phase-1/symbols/px" / f"{f}.png")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
