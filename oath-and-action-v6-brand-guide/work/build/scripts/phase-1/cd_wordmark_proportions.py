"""Creative director, Phase 1: measure wordmark proportions in Dustin's references.

Reads rendered reference pages (work/extract/references/pics-i-like/) and the
brand mockups (source/brand-mockups/, read only), finds the ink bounding box of
the wordmark in a hand-set crop, and reports width divided by height. Compares
with the V5 Polished wordmark master (viewBox 970.71 x 108, cap height 100 units).

Run: python3 -I work/build/scripts/phase-1/cd_wordmark_proportions.py <project root>
The measurement is approximate: crops are set by eye, and generated images are
not drawn to a grid. It supports a direction, never a specification.
"""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(sys.argv[1]).resolve()
PAGES = ROOT / "work/extract/references/pics-i-like"
MOCK = ROOT / "source/brand-mockups"

# (label, file, crop box x0, y0, x1, y1, mode) set by eye around one-line wordmarks.
# mode "dark" counts dark or red pixels on a light ground; "light" counts light or red on a dark ground.
CROPS = [
    ("p01 hero wordmark", PAGES / "page-01.png", (40, 70, 975, 250), "dark"),
    ("p07 primary wordmark", PAGES / "page-07.png", (210, 120, 625, 215), "dark"),
    ("p08 letterhead wordmark", PAGES / "page-08.png", (30, 20, 270, 75), "dark"),
    ("p13 Prussian banner", PAGES / "page-13.png", (215, 30, 870, 150), "light"),
    ("Mockup banner, Prussian", MOCK / "20261021_Mockup-Banner-Prussian-Stewards.webp", (140, 60, 1020, 225), "light"),
    ("Mockup square poster, OATH & line", MOCK / "20261021_Mockup-Square-Wordmark-Stewards.webp", (130, 160, 1120, 375), "dark"),
]


def ink(px, mode):
    r, g, b = px[:3]
    red = r > 150 and g < 110 and b < 110
    if mode == "dark":
        return red or (r + g + b) < 200
    return red or (r + g + b) > 560


def bbox(img, box, mode):
    crop = img.convert("RGB").crop(box)
    w, h = crop.size
    data = crop.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if ink(data[x, y], mode):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def main():
    rows = []
    v5 = {"label": "V5 Polished wordmark master", "width": 970.71, "cap_height": 100.0,
          "ratio_width_to_cap": round(970.71 / 100.0, 2), "note": "viewBox 970.71 x 108; cap height 100 units per the Phase 0 design director audit"}
    rows.append(v5)
    for label, path, box, mode in CROPS:
        img = Image.open(path)
        b = bbox(img, box, mode)
        if b is None:
            rows.append({"label": label, "error": "no ink found"})
            continue
        w = b[2] - b[0] + 1
        h = b[3] - b[1] + 1
        rows.append({"label": label, "file": str(path.relative_to(ROOT)), "ink_width_px": w,
                     "ink_height_px": h, "ratio_width_to_height": round(w / h, 2),
                     "note": "ink height includes the ampersand, which rises slightly above the caps"})
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
