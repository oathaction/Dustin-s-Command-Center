"""Compare the V5 master ampersand outline with the ampersand in the embedded Lora 700 font.
Run: python3 -I amp_vs_lora.py <ROOT>"""
import re
import sys
from pathlib import Path

sys.path.append("/root/.local/lib/python3.13/site-packages")  # fontTools install location
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.pens.recordingPen import RecordingPen  # noqa: E402

root = Path(sys.argv[1])
font = TTFont(root / "work/extract/v5-polished/fonts/Lora-700-normal.ttf")
gs = font.getGlyphSet()
name = font.getBestCmap()[ord("&")]
pen = RecordingPen()
gs[name].draw(pen)
pts = []
for op, args in pen.value:
    for a in args:
        pts.append((round(a[0]), round(a[1])))
amp = (root / "work/extract/v5-polished/sprite/amp.svg").read_text()
d = re.search(r' d="([^"]+)"', amp).group(1)
nums = [float(v) for v in re.findall(r"-?\d*\.?\d+", d)]
svgpts = {(round(nums[i]), round(nums[i + 1])) for i in range(0, len(nums) - 1, 2)}
fontset = set(pts)
print("glyph", name, "UPM", font["head"].unitsPerEm, "advance", font["hmtx"][name][0])
print("font points", len(fontset), "svg points", len(svgpts), "shared", len(fontset & svgpts))
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
print("font bbox", min(xs), min(ys), max(xs), max(ys))
os2 = font["OS/2"]
print("Lora capHeight", getattr(os2, "sCapHeight", None), "xHeight", getattr(os2, "sxHeight", None))
