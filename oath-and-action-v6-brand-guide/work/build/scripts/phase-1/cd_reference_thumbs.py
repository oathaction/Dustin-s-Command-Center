"""Creative director, Phase 1: review thumbnails of Dustin's references for the strategy board.

Reads rendered pages in work/extract/references/pics-i-like/ and the mockups in
source/brand-mockups/ (opened read only, never modified), and writes JPEG review
copies to work/boards/phase-1/strategy/refs/. These copies exist only so Dustin can
see which slide a principle came from. They are study material and never ship.

Run: python3 -I work/build/scripts/phase-1/cd_reference_thumbs.py <project root>
"""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(sys.argv[1]).resolve()
PAGES = ROOT / "work/extract/references/pics-i-like"
MOCK = ROOT / "source/brand-mockups"
OUT = ROOT / "work/boards/phase-1/strategy/refs"
WIDTH = 880

ITEMS = [(f"20261021_Ref-Page-{n:02d}.jpg", PAGES / f"page-{n:02d}.png")
         for n in (1, 3, 4, 5, 7, 8, 14, 15, 17, 24, 25, 40, 41)]
ITEMS += [
    ("20261021_Ref-Mockup-Square-Poster.jpg", MOCK / "20261021_Mockup-Square-Wordmark-Stewards.webp"),
    ("20261021_Ref-Mockup-Banner.jpg", MOCK / "20261021_Mockup-Banner-Prussian-Stewards.webp"),
    ("20261021_Ref-Mockup-Hinge-Newsprint.jpg", MOCK / "20261021_Mockup-Hinge-Diagram-Newsprint.webp"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    for name, src in ITEMS:
        with Image.open(src) as im:
            im = im.convert("RGB")
            w, h = im.size
            scale = min(1.0, WIDTH / w)
            size = (round(w * scale), round(h * scale))
            im = im.resize(size, Image.LANCZOS)
            dest = OUT / name
            im.save(dest, "JPEG", quality=72, optimize=True)
            report.append({"file": str(dest.relative_to(ROOT)), "from": str(src.relative_to(ROOT)),
                           "size": list(size), "bytes": dest.stat().st_size})
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
