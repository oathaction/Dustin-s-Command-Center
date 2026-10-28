"""Concept 3, Public sign: hinted 16 and 24 px masters (design director, Phase 2 round two).

The 24 px master is the display drawing fitted to whole pixels (Feedback loop and Campaign money
are drawn on the pixel grid first, see draw24 in icons_r2_sign_draw.py); the 16 px master is the
separate 16-unit drawing in icons_r2_sign_draw.py fitted the same way.

Fitting keeps a pixel when its center falls inside the layer, sampled a hair off center so an
edge that runs exactly through pixel centers resolves the same way every time, and traces the
kept pixels as one outline per layer. Center sampling gives true pixel discs (a 4.5-unit node
becomes a 5 px disc with its corners cut), keeps 3 px bars at 3 px, and squares off round ends.
Round one's area-coverage fitter (pixel_shape in icons_draw.py) turned these discs into crosses,
so this module uses its own fitter and leaves round one's untouched.

Layers: "ink" and "accent". Where the red sits on ink (Ballot's check on its paper), the accent
pixels win and the ink keeps its pixels underneath, so removing the red leaves the paper whole.
Everywhere else ink wins a pixel both layers claim, so red never paints over the drawing.

Straight red strokes that are short take square ends before fitting: a round end fitted to whole
pixels turns a 3 by 5 px bar into a plus, and the family keeps every red plus shape out.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_sign_draw as D  # noqa: E402
import icons_r2_sign_geom as G  # noqa: E402
import numpy as np  # noqa: E402

RED_ON_INK = {"ballot"}

# 24 px: straight red strokes drawn with square ends before fitting (same footprint as the round
# ended display stroke, so the drawing does not move).
SQUARE_RED_24 = {
    "housing": lambda: G.rect(10.0, 15.5, 3.0, 6.5),
    "bill": lambda: G.rect(8.5, 15.0, 5.5, 3.0),
}


def _fit(shape, size):
    """Trace the pixels whose (nudged) centers fall inside the shape, merged into row runs."""
    if G.g.is_empty(shape):
        return G.empty()
    shape = G.union(shape, G.empty())
    b = shape.bounds
    kept = []
    for y in range(max(0, int(b[1]) - 1), min(size, int(b[3]) + 2)):
        row = [x for x in range(max(0, int(b[0]) - 1), min(size, int(b[2]) + 2)) if shape.contains((x + 0.5013, y + 0.5007))]
        i = 0
        while i < len(row):
            j = i
            while j + 1 < len(row) and row[j + 1] == row[j] + 1:
                j += 1
            kept.append(G.rect(row[i], y, row[j] - row[i] + 1, 1))
            i = j + 1
    return G.union(*kept) if kept else G.empty()


def master(name, size):
    """{"ink": path, "accent": path} on whole pixels for size 16 or 24."""
    if size == 24:
        d = D.draw24(name)
        acc_src = SQUARE_RED_24[name]() if name in SQUARE_RED_24 else d["accent"]
    elif size == 16:
        d = D.draw16(name)
        acc_src = d["accent"]
    else:
        raise ValueError(size)
    ink = _fit(d["ink"], size)
    acc = _fit(acc_src, size)
    if name not in RED_ON_INK:
        acc = G.minus(acc, ink)
    return {"ink": ink, "accent": acc}


def mask(path, size):
    m = np.zeros((size, size), bool)
    for y in range(size):
        for x in range(size):
            m[y, x] = path.contains((x + .5, y + .5))
    return m


def red_plus(acc_mask):
    """Any red pixel whose four side neighbors are red and four corner neighbors are not, inside a
    red component of 9 pixels or fewer: the shape of a small plus."""
    h, w = acc_mask.shape
    m = np.pad(acc_mask, 1)
    hits = []
    for y in range(1, h + 1):
        for x in range(1, w + 1):
            if m[y, x] and m[y - 1, x] and m[y + 1, x] and m[y, x - 1] and m[y, x + 1] and not (
                    m[y - 1, x - 1] or m[y - 1, x + 1] or m[y + 1, x - 1] or m[y + 1, x + 1]):
                hits.append((x - 1, y - 1))
    if not hits:
        return []
    # keep hits inside small components only
    from collections import deque
    out = []
    for (x0, y0) in hits:
        seen, q = {(x0, y0)}, deque([(x0, y0)])
        while q and len(seen) <= 9:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and acc_mask[yy, xx] and (xx, yy) not in seen:
                    seen.add((xx, yy))
                    q.append((xx, yy))
        if len(seen) <= 9:
            out.append((x0, y0))
    return out
