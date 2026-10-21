"""Count Pillar Red pixels that touch Prussian (within 3 px) on board screenshots.
Run: python3 -I p1_red_audit.py <slice_dir>"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

RED = np.array((230, 57, 70), float)
PRUS = np.array((31, 45, 90), float)


def dilate(m, r):
    """Square dilation by r px, separable: rows then columns."""
    out = m.copy()
    for k in range(1, r + 1):
        out[k:] |= m[:-k]; out[:-k] |= m[k:]
    m2 = out.copy()
    for k in range(1, r + 1):
        out[:, k:] |= m2[:, :-k]; out[:, :-k] |= m2[:, k:]
    return out


def main():
    d = Path(sys.argv[1])
    red_px = touch_px = 0
    clusters = 0
    for f in sorted(d.glob("s*.png")):
        a = np.asarray(Image.open(f).convert("RGB"), float)
        red = np.linalg.norm(a - RED, axis=2) < 48
        prus = np.linalg.norm(a - PRUS, axis=2) < 24
        t = red & dilate(prus, 3)
        red_px += int(red.sum())
        n = int(t.sum())
        touch_px += n
        if n:
            # rough cluster count: 8 px grid cells that hold a touching pixel
            ys, xs = np.nonzero(t)
            clusters += len({(y // 8, x // 8) for y, x in zip(ys, xs)})
    print(json.dumps({"dir": str(d), "red_pixels": red_px, "red_pixels_touching_prussian": touch_px, "touching_cells_8px": clusters}))


if __name__ == "__main__":
    main()
