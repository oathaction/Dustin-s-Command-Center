"""Write the trim box and bleed box into a PDF Chromium printed at the sheet's size (it writes only the media box), and its
title. Usage: python3 -I work/build/app-kit/tools/pdf_boxes.py FILE.pdf BLEED_PT [TITLE]"""
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

path, bleed = sys.argv[1], float(sys.argv[2])
title = sys.argv[3] if len(sys.argv) > 3 else None
rd = PdfReader(path)
w = PdfWriter(clone_from=rd)
for pg in w.pages:
    x0, y0, x1, y1 = (float(v) for v in pg.mediabox)
    pg.bleedbox = RectangleObject([x0, y0, x1, y1])
    pg.trimbox = RectangleObject([x0 + bleed, y0 + bleed, x1 - bleed, y1 - bleed])
if title:
    meta = dict(rd.metadata or {})
    meta["/Title"] = title
    w.add_metadata(meta)
with open(path, "wb") as f:
    w.write(f)
print(f"{path}: trim and bleed boxes written, bleed {bleed} pt")
