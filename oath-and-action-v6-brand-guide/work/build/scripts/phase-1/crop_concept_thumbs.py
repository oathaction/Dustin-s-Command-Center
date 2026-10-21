#!/usr/bin/env python3
"""Crop reference thumbnails of the five atlas bases from the Phase 0 Concepts V2 screenshots.

Run:  python3 -I work/build/scripts/phase-1/crop_concept_thumbs.py
Reads the 1440 px tiles in work/boards/screens/concepts-v2/ (Phase 0 captures of the supplied Concepts V2 file).
Writes JPEG thumbnails to work/boards/phase-1/systems/. Crops are for review only and are not assets.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "work/boards/screens/concepts-v2"
OUT = ROOT / "work/boards/phase-1/systems"

# (output name, [(tile, top, bottom), ...]) in 1440 px tile coordinates; parts are stacked vertically.
CROPS = [
    ("20261021_Concept-03-Field-Manual.jpg", [("02.jpg", 1112, 1800), ("03.jpg", 0, 205)]),
    ("20261021_Concept-04-Broadsheet.jpg", [("03.jpg", 492, 1382)]),
    ("20261021_Concept-07-Loop-Card.jpg", [("05.jpg", 428, 1406)]),
    ("20261021_Concept-09-Circuit.jpg", [("07.jpg", 16, 1142)]),
    ("20261021_Concept-10-Who-Can-Act.jpg", [("07.jpg", 1432, 1800), ("08.jpg", 0, 976)]),
    ("20261021_Concept-11-Register.jpg", [("08.jpg", 1266, 1800), ("09.jpg", 0, 498)]),
]

for name, parts in CROPS:
    pieces = [Image.open(SRC / tile).convert("RGB").crop((0, top, 1440, bottom)) for tile, top, bottom in parts]
    h = sum(p.height for p in pieces)
    canvas = Image.new("RGB", (1440, h), (220, 217, 210))
    y = 0
    for p in pieces:
        canvas.paste(p, (0, y))
        y += p.height
    w = 720
    thumb = canvas.resize((w, round(h * w / 1440)), Image.LANCZOS)
    thumb.save(OUT / name, "JPEG", quality=72, optimize=True)
    print(name, thumb.size)
