"""Text measurement with real font metrics for Direction B, Snowball and Thermostat.

Measures with the Inter, Inter Tight and Lora files extracted from V5 Polished (the same families the pages load
from Google Fonts, D1-19), so label boxes, wraps and collision tests come from the faces themselves. The rendered
check (maps_r2_b_check.js) still measures every label in the browser and fails on any collision.
"""
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[4]
FONTS = ROOT / "work/extract/v5-polished/fonts"
FILES = {
    ("inter", 400): "Inter-400-normal.ttf", ("inter", 600): "Inter-600-normal.ttf", ("inter", 700): "Inter-700-normal.ttf",
    ("tight", 600): "Inter-Tight-600-normal.ttf", ("tight", 700): "Inter-Tight-800-normal.ttf",
    ("tight", 800): "Inter-Tight-800-normal.ttf", ("lora-italic", 400): "Lora-Italic-400-normal.ttf",
}


@lru_cache(maxsize=None)
def _font(family, weight, size):
    key = (family, weight)
    if key not in FILES:
        key = (family, 400 if family != "tight" else 800)
    return ImageFont.truetype(str(FONTS / FILES[key]), size=max(1, round(size * 4)))


def width(text, size, weight=400, family="inter"):
    """Advance width in CSS px, measured at 4x, plus a 2 percent margin for hinting differences with the web fonts."""
    if not text:
        return 0.0
    return _font(family, weight, size).getlength(text) / 4.0 * 1.02


def wrap(text, max_w, size, weight=400, family="inter"):
    """Greedy wrap on spaces. Never truncates."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if width(t, size, weight, family) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    # no single short word alone on a last line (2x test: nothing sits alone on a line)
    if len(lines) >= 2 and len(lines[-1].split()) == 1 and len(lines[-2].split()) >= 3:
        prev = lines[-2].split()
        cand = " ".join(prev[-1:] + [lines[-1]])
        if width(cand, size, weight, family) <= max_w:
            lines[-2] = " ".join(prev[:-1])
            lines[-1] = cand
    return lines


def block_w(lines, size, weight=400, family="inter"):
    return max((width(s, size, weight, family) for s in lines), default=0.0)
