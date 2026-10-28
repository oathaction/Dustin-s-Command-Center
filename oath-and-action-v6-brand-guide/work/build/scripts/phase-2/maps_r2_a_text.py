"""Text measurement with real font metrics for Direction A, Field Guide.

Round one laid out labels from an average character width, and most of its collisions came from that estimate.
This module measures with the Inter, Inter Tight and Lora files extracted from V5 Polished (the same families the
board loads from Google Fonts, D1-19), so wraps and box sizes come from the faces themselves. The rendered check
(maps_r2_a_check.js) still measures every label in the browser and fails on any overflow.
"""
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[4]
FONTS = ROOT / "work/extract/v5-polished/fonts"
FILES = {
    ("inter", 400): "Inter-400-normal.ttf", ("inter", 600): "Inter-600-normal.ttf", ("inter", 700): "Inter-700-normal.ttf",
    ("tight", 600): "Inter-Tight-600-normal.ttf", ("tight", 800): "Inter-Tight-800-normal.ttf",
    ("lora-italic", 400): "Lora-Italic-400-normal.ttf",
}


@lru_cache(maxsize=None)
def _font(family, weight, size):
    key = (family, weight)
    if key not in FILES:
        key = (family, 400 if family != "tight" else 800)
    return ImageFont.truetype(str(FONTS / FILES[key]), size=max(1, round(size * 4)))


def width(text, size, weight=400, family="inter", tracking=0.0):
    """Advance width in CSS px. Measured at 4x and scaled back for sub-pixel accuracy, plus a 2 percent margin
    for kerning and hinting differences between these files and the web fonts."""
    if not text:
        return 0.0
    w = _font(family, weight, size).getlength(text) / 4.0
    return w * 1.02 + tracking * size * len(text)


def wrap(text, max_w, size, weight=400, family="inter", max_lines=None):
    """Greedy wrap on spaces. Never truncates: if max_lines is set and the text needs more, it returns all lines
    and the caller must make room."""
    # split on plain spaces only, so a no-break space (U+00A0) holds a phrase such as "over 10 years" together
    words, lines, cur = [w for w in text.split(" ") if w], [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if width(t, size, weight, family) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def balanced_wrap(text, max_w, size, weight=400, family="inter"):
    """Wrap to the fewest lines that fit, then even out the line lengths, so a two-line label never leaves one
    short word alone on its second line."""
    greedy = wrap(text, max_w, size, weight, family)
    n = len(greedy)
    if n <= 1:
        return greedy
    words = text.split()
    best, best_score = greedy, None
    lo, hi = 0.4 * max_w, max_w
    for _ in range(18):
        mid = (lo + hi) / 2
        trial = wrap(text, mid, size, weight, family)
        if len(trial) <= n and all(width(l, size, weight, family) <= max_w for l in trial):
            hi = mid
            widths = [width(l, size, weight, family) for l in trial]
            score = max(widths) - min(widths)
            if best_score is None or score <= best_score:
                best, best_score = trial, score
        else:
            lo = mid
    return best
