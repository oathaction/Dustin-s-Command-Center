"""Recover the spacing applied to the stock Inter Tight 800 capitals in the V5 wordmark.
Run: python3 -I wordmark_vs_inter_tight.py <ROOT>"""
import json
import sys
from pathlib import Path

sys.path.append("/root/.local/lib/python3.13/site-packages")  # fontTools install location
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fontTools.ttLib import TTFont  # noqa: E402
from oa_geom import collect_polys, group_glyphs, strip_defs  # noqa: E402

root = Path(sys.argv[1])
f = TTFont(root / "work/extract/v5-polished/fonts/Inter-Tight-800-normal.ttf")
glyf, hmtx = f["glyf"], f["hmtx"]
cap = f["OS/2"].sCapHeight
s = 100.0 / cap  # wordmark cap height is 100 units
wm = strip_defs((root / "work/extract/v5-polished/sprite/wordmark.svg").read_text())
letters = [p for pp, a in collect_polys(wm) if not a for p in pp]
gl = group_glyphs(letters)
names = list("OATHACTION")
rows = []
origins = []
for n, g in zip(names, gl):
    gg = glyf[n]
    origin = g["box"][0] - gg.xMin * s
    origins.append(origin)
    rows.append({"glyph": n, "x_min": round(g["box"][0], 2), "font_xMin": gg.xMin, "advance_units": round(hmtx[n][0] * s, 2), "origin": round(origin, 2)})
adj = []
for i in range(len(names) - 1):
    if i == 3:
        continue  # the ampersand sits between H and the second A
    a = origins[i + 1] - origins[i] - hmtx[names[i]][0] * s
    adj.append({"pair": names[i] + names[i + 1], "adjust_units": round(a, 2), "adjust_em_pct": round(a / (f["head"].unitsPerEm * s) * 100, 2)})
em = f["head"].unitsPerEm * s
# kerning pairs from the GPOS table are class based; report the size of the em and the adjustments only
print(json.dumps({"em_units": round(em, 2), "scale": s, "rows": rows, "pair_adjustments": adj}, indent=1))
