"""Similarity of the drawn ampersand (option B) against the V5 glyph (Lora Bold) and the serif
ampersands installed on this machine. Each glyph is scaled to the same ink height, centred on its
ink box, rasterised by Chromium at 200 px, and compared by silhouette overlap (intersection over
union). 1.0 means identical silhouettes.

Run: python3 -I p1_similarity.py
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.append("/root/.local/lib/python3.13/site-packages")
import oa_p1 as o  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402
from PIL import Image  # noqa: E402

H = 200


def font_amp(path):
    f = TTFont(path)
    gs = f.getGlyphSet()
    name = f.getBestCmap().get(ord("&"))
    pen = SVGPathPen(gs)
    gs[name].draw(pen)
    p = o.path_from_d(pen.getCommands(), (1, 0, 0, -1, 0, 0))
    return p


def fc_files():
    out = subprocess.run(["fc-list", ":style=Bold", "file", "family"], capture_output=True, text=True).stdout.splitlines()
    picks = {}
    for line in out:
        fpath, _, fam = line.partition(":")
        fam = fam.strip().split(",")[0]
        if any(k in fam for k in ("Serif", "Charter", "Caladea", "Liberation Serif", "FreeSerif")) and "Mono" not in fam and "Sans" not in fam:
            picks.setdefault(fam, fpath.strip())
    return picks


def raster(p, tag):
    b = o.bounds(p)
    k = H / (b[3] - b[1])
    q = o.tx(p, a=k, d=k, e=-b[0] * k, f=-b[1] * k)
    w = (b[2] - b[0]) * k
    W = H + 40
    dx = (W - w) / 2
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" style="left:0;top:0"><path transform="translate({dx:.2f} 0)" d="{o.d_from_path(q)}" fill="#000"/></svg>'
    return {"id": tag, "w": W, "h": H, "bg": "#FFFFFF", "html": svg}


def main():
    cands = {"V5 master (Lora Bold)": o.path_from_d(o.AMP_D, (1, 0, 0, -1, 0, 0))}
    for fam, fp in fc_files().items():
        try:
            cands[fam + " Bold"] = font_amp(fp)
        except Exception:
            pass
    B = o.path_from_d((o.OUT / "05-amp-b/20261021_Amp-B-Drawn-Master.svg").read_text().split(' d="')[1].split('"')[0])
    A = o.path_from_d((o.OUT / "04-amp-a/20261021_Amp-A-Display-Tune.svg").read_text().split(' d="')[1].split('"')[0])
    jobs = [raster(B, "B"), raster(A, "A")] + [raster(p, f"c{i}") for i, p in enumerate(cands.values())]
    od = o.SCRATCH / "similarity"
    o.render(jobs, od, "sim")

    def mask(t):
        im = Image.open(od / f"{t}.png").convert("L")
        return [v < 128 for v in im.getdata()]

    mb, ma = mask("B"), mask("A")
    res = {}
    for i, name in enumerate(cands):
        mc = mask(f"c{i}")
        for lab, m in (("B", mb), ("A", ma)):
            inter = sum(a and b for a, b in zip(m, mc))
            uni = sum(a or b for a, b in zip(m, mc))
            res.setdefault(name, {})[f"IoU with option {lab}"] = round(inter / uni, 3)
    out = o.ROOT / "work/handoffs/phase-1/20261021_Ampersand-Similarity.json"
    out.write_text(json.dumps({"method": __doc__.strip(), "results": res}, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
