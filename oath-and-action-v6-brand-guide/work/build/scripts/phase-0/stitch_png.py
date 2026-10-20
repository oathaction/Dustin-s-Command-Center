"""Stitch the slices written by screenshot_board.js into one PNG.
Run: python3 -I stitch_png.py <out.png>"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

out = Path(sys.argv[1])
meta = json.loads(Path(str(out) + ".parts.json").read_text())
Image.MAX_IMAGE_PIXELS = None
canvas = Image.new("RGB", (meta["width"], meta["total"]), "white")
y = 0
for p in meta["parts"]:
    im = Image.open(p).convert("RGB")
    canvas.paste(im, (0, y))
    y += im.height
canvas.save(out, optimize=True)
shutil.rmtree(str(out) + ".parts")
Path(str(out) + ".parts.json").unlink()
print(out, canvas.size, out.stat().st_size)
