"""Pixel audit of the board screenshots: Pillar Red pixels within 3 px of Prussian pixels.

Reads the viewport segments written by p2_check_board.js and writes the board check JSON.
Run: python3 -I p2_red_audit.py <segments dir> [<segments dir with specimens hidden>]
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402

RED, PRUS = np.array([0xE6, 0x39, 0x46]), np.array([0x1F, 0x2D, 0x5A])


def audit(d):
    total = 0
    for seg in sorted(Path(d).glob("seg-*.png")):
        a = np.asarray(Image.open(seg).convert("RGB"), dtype=int)
        red = np.abs(a - RED).sum(axis=2) < 60
        if not red.any():
            continue
        pru = np.abs(a - PRUS).sum(axis=2) < 30
        h, w = pru.shape
        pad = np.zeros((h + 6, w + 6), dtype=bool)
        pad[3:-3, 3:-3] = pru
        near = np.zeros_like(pru)
        for dy in range(7):
            for dx in range(7):
                near |= pad[dy:dy + h, dx:dx + w]          # within 3 px, no wrap at the edges
        total += int((red & near).sum())
    return total


if __name__ == "__main__":
    base = Path(sys.argv[1])
    res = {"check": json.loads((base / "check.json").read_text())}
    res["red_near_prussian_px"] = {d.name: audit(d) for d in sorted(base.iterdir()) if d.is_dir()}
    if len(sys.argv) > 2:
        hid = Path(sys.argv[2])
        res["red_near_prussian_px_specimens_hidden"] = {d.name: audit(d) for d in sorted(hid.iterdir()) if d.is_dir()}
        res["check_specimens_hidden"] = json.loads((hid / "check.json").read_text())
    for k in list(res["check"]):
        res["check"][k].pop("brokenList", None)
    out = P.BOARD_DIR / f"{P.DATE}_Identity-Masters-Board-Check.json"
    P.save_json(out, res)
    print(json.dumps({k: v for k, v in res.items() if k.startswith("red")}, indent=1))
