"""I4 check: ampersand B (refined) against every serif ampersand installed on this machine.

Candidates: every font file fontconfig lists in a serif family (book serifs, and the serif
typewriter faces Courier 10 Pitch, FreeMono and Liberation Mono), every style, plus the three Lora
files extracted from V5 Polished, Lora Bold being the V5 master's source. Sans, monospaced sans
and symbol fonts are left out.

Two measures, the same as Phase 1 and the symbol board:
  silhouette overlap   each glyph scaled to the same ink height (200 px), centered on its ink box,
                       rendered by Chromium, then intersection over union of the ink (1.0 = identical)
  small-size score     at 16 and 24 px tall: the mean of filled-silhouette overlap and blurred
                       correlation (the Phase 0 similarity score behind D1-16)

Pass rules (studio thresholds, stated before the run):
  recognition   B overlaps the V5 glyph (Lora Bold) at 0.70 or more, so a reader still knows it
  distinctness  B overlaps no other installed face as closely as one face's Regular and Bold
                overlap each other (the median same-family weight pair): at that distance two
                ampersands count as one design

Run: python3 -I p2_amp_similarity.py
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p2_amp_b as B2  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402
from PIL import Image  # noqa: E402
import numpy as np  # noqa: E402

H = 200
SERIF_FAMILIES = ("Bitstream Charter", "Caladea", "Courier 10 Pitch", "DejaVu Serif", "FreeMono", "FreeSerif",
                  "Liberation Mono", "Liberation Serif")
OUT = P.HANDOFF / f"{P.DATE}_Ampersand-B-Similarity.json"


def installed():
    lines = subprocess.run(["fc-list", "--format", "%{family[0]}|%{style[0]}|%{file}\n"], capture_output=True, text=True).stdout.splitlines()
    out = {}
    for ln in sorted(set(lines)):
        fam, sty, f = ln.split("|")
        out[f"{fam} {sty}"] = {"family": fam, "style": sty, "file": f, "serif": fam in SERIF_FAMILIES}
    return out


def glyph_path(fpath):
    if fpath.endswith(".pfb"):
        from fontTools.t1Lib import T1Font
        gs = T1Font(fpath).getGlyphSet()
        name = "ampersand"
    else:
        f = TTFont(fpath)
        gs = f.getGlyphSet()
        name = f.getBestCmap().get(ord("&"))
    pen = SVGPathPen(gs)
    gs[name].draw(pen)
    return o.path_from_d(pen.getCommands(), (1, 0, 0, -1, 0, 0))   # y down


def raster_job(p, tag, h=H, pad=None):
    b = o.bounds(p)
    k = h / (b[3] - b[1])
    q = o.tx(p, a=k, d=k, e=-b[0] * k, f=-b[1] * k)
    w = (b[2] - b[0]) * k
    W = h + (40 if pad is None else pad) if h >= 100 else h
    if h < 100:
        W = h
        s = min(1.0, h / w)  # fit wide glyphs into a square cell at small sizes
        q = o.tx(q, a=s, d=s, f=(h - h * s) / 2)
        w = w * s
    dx = (W - w) / 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" style="left:0;top:0">'
           f'<path transform="translate({dx:.2f} 0)" d="{o.d_from_path(q)}" fill="#000"/></svg>')
    return {"id": tag, "w": W, "h": h, "bg": "#FFFFFF", "html": svg}


def cov(path):
    a = np.asarray(Image.open(path).convert("L"), dtype=float)
    return 1 - a / 255.0


def iou(a, b):
    ma, mb = a > 0.5, b > 0.5
    return float((ma & mb).sum() / max(1, (ma | mb).sum()))


def main():
    fonts = installed()
    cands = {name: v for name, v in fonts.items() if v["serif"]}
    for f, lab in (("Lora-700-normal.ttf", "Lora Bold (V5 master source)"), ("Lora-Italic-400-normal.ttf", "Lora Italic"),
                   ("Lora-Italic-500-normal.ttf", "Lora Medium Italic")):
        cands[lab] = {"family": "Lora", "style": lab.split(" ", 1)[1], "file": str(o.FONTS / f), "serif": True, "extracted_from_v5": True}
    paths = {}
    for name, v in cands.items():
        paths[name] = glyph_path(v["file"])
    bp = B2.to_symbol(B2.glyph(), o.bounds(B2.glyph())[0])  # y down
    import p1_amp_b as B1
    b1 = B1.to_symbol(B1.glyph(), o.bounds(B1.glyph())[0])
    probes = {"B refined (Phase 2)": bp, "B first drawing (Phase 1)": b1}
    allp = {**probes, **paths}
    tags = {n: f"g{i}" for i, n in enumerate(allp)}
    jobs = []
    for n, p in allp.items():
        jobs.append(raster_job(p, tags[n]))
        for s in (16, 24):
            jobs.append(raster_job(p, f"{tags[n]}_{s}", h=s))
    od = P.SCRATCH / "similarity"
    P.render(jobs, od, "sim2")
    C = {n: cov(od / f"{tags[n]}.png") for n in allp}
    import symbols_measure as M
    small = {n: {s: Image.open(od / f"{tags[n]}_{s}.png") for s in (16, 24)} for n in allp}

    def small_score(a, b, s):
        ca = M.load_cov(od / f"{tags[a]}_{s}.png", "#FFFFFF", "#000000")
        cb = M.load_cov(od / f"{tags[b]}_{s}.png", "#FFFFFF", "#000000")
        return M.sim(ca, cb)["score"]
    res = {}
    for probe in probes:
        rows = {}
        for n in paths:
            rows[n] = {"silhouette_overlap_200px": round(iou(C[probe], C[n]), 3),
                       "score_16px": small_score(probe, n, 16), "score_24px": small_score(probe, n, 24)}
        res[probe] = rows
    # calibration: Regular against Bold inside each installed family that has both
    same = {}
    for fam in SERIF_FAMILIES:
        reg = next((n for n, v in cands.items() if v["family"] == fam and v["style"] in ("Regular", "Book")), None)
        bold = next((n for n, v in cands.items() if v["family"] == fam and v["style"] == "Bold"), None)
        if reg and bold:
            same[fam] = round(iou(C[reg], C[bold]), 3)
    vals = sorted(same.values())
    med = vals[len(vals) // 2] if len(vals) % 2 else round((vals[len(vals) // 2 - 1] + vals[len(vals) // 2]) / 2, 3)
    probe = "B refined (Phase 2)"
    lora = res[probe]["Lora Bold (V5 master source)"]["silhouette_overlap_200px"]
    others = {n: r["silhouette_overlap_200px"] for n, r in res[probe].items() if not n.startswith("Lora")}
    nearest = max(others, key=others.get)
    verdict = {
        "recognition": {"rule": "overlap with Lora Bold at 0.70 or more", "value": lora, "pass": lora >= 0.70},
        "distinctness": {"rule": f"overlap with every other installed face below the median Regular-to-Bold overlap of one family ({med})",
                         "nearest_face": nearest, "value": others[nearest], "threshold": med, "pass": others[nearest] < med},
        "faces_checked": len(paths), "families_checked": sorted({v['family'] for v in cands.values()}),
    }
    verdict["pass"] = verdict["recognition"]["pass"] and verdict["distinctness"]["pass"]
    data = {"method": __doc__.strip(), "calibration_regular_vs_bold": same, "calibration_median": med,
            "verdict_B_refined": verdict, "results": res,
            "fonts": {n: {"file": v["file"], "family": v["family"], "style": v["style"]} for n, v in cands.items()},
            "not_checked": "Commercial faces are not installed and could not be checked."}
    P.save_json(OUT, data)
    # contact sheet for the board: B refined beside every candidate at 96 px, and the overlay with the nearest
    sheet = []
    for n in [probe] + list(paths):
        sheet.append(raster_job(allp[n], f"sheet_{tags[n]}", h=96, pad=24))
    P.render(sheet, P.BOARD_DIR / "04-amp-b" / "similarity", "simsheet")
    names = {f"sheet_{tags[n]}": n for n in [probe] + list(paths)}
    P.save_json(P.SCRATCH / "similarity_sheet.json", names)
    print(json.dumps(verdict, indent=1))
    print(json.dumps({n: r["silhouette_overlap_200px"] for n, r in sorted(res[probe].items(), key=lambda kv: -kv[1]["silhouette_overlap_200px"])}, indent=1))
    print("calibration", same, med)


if __name__ == "__main__":
    main()
