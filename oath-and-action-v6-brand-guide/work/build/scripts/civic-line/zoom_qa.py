"""Enlarge part of a QA panel, addressed in crop pixel coordinates.

    python3 -I zoom_qa.py <ID> <panel> x0,y0,x1,y1 [--scale 3] [--out PATH]

panel: reference | trace | overlay | diff  (from qa/overlays/<ID>.png)
       black | red                         (the untouched reference crops)
The overlay panels are already 4x; --scale enlarges further (nearest
neighbour). The default output is a file in the system temp folder; nothing
is written under assets/.
"""
import argparse
import os
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

PANELS = ["reference", "trace", "overlay", "diff"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("panel", choices=PANELS + ["black", "red"])
    ap.add_argument("box")
    ap.add_argument("--scale", type=int, default=3)
    ap.add_argument("--out")
    a = ap.parse_args()
    row = C.inventory_by_id()[a.id]
    x0, y0, x1, y1 = [float(v) for v in a.box.split(",")]
    w, h = row["crop"]["w"], row["crop"]["h"]
    if a.panel in ("black", "red"):
        im = Image.open(os.path.join(C.ASSETS, "reference-crops", row["reference_crops"][a.panel])).convert("RGB")
        z = 1
        ox = oy = 0
    else:
        im = Image.open(os.path.join(C.QA, "overlays", f"{a.id}.png")).convert("RGB")
        z = 4
        gap, top, strip = 10, 34, 22   # layout written by build_icon.overlay_panels
        k = PANELS.index(a.panel)
        ox = gap + k * (w * z + gap)
        oy = top + strip
    box = (int(ox + x0 * z), int(oy + y0 * z), int(ox + x1 * z), int(oy + y1 * z))
    part = im.crop(box)
    s = a.scale * (4 if z == 1 else 1)
    part = part.resize((part.width * s, part.height * s), Image.NEAREST)
    out = a.out or os.path.join(tempfile.gettempdir(), f"civic-line-zoom-{a.id}-{a.panel}.png")
    part.save(out)
    print(out)


if __name__ == "__main__":
    main()
