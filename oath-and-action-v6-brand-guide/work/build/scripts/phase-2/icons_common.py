"""Shared paths, palette, drawing registry and SVG writing for the Phase 2 icon concepts.

Run every icon script with python3 -I. Scripts: icons_assets.py writes the masters, variants,
holders and pixel renders; icons_measure.py runs the checks; icons_board_build.py writes the board;
icons_board_check.js checks the board's layout and captures it.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_draw as D  # noqa: E402
import icons_geom as g  # noqa: E402

ROOT = HERE.parents[3]
DATE = "20261028"
BOARDS = ROOT / "work/boards"
OUT = BOARDS / "phase-2/icons"            # masters live here
VARIANTS = OUT / "variants"
HOLDERS = OUT / "holders"
PX = OUT / "px"
BASELINE = OUT / "baseline"
CONTEXT = OUT / "context"
HANDOFF = ROOT / "work/handoffs/phase-2"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/icons-build")
RENDER_JS = HERE / "icons_render_cells.js"
SPRITE = ROOT / "work/extract/v5-polished/sprite"
P1_SYMBOLS = BOARDS / "phase-1/symbols"

NEWS, CHAR, RED, PRUS, WHITE, STONE = "#DCD9D2", "#121212", "#E63946", "#1F2D5A", "#FFFFFF", "#5D636D"
SURFACES = [("newsprint", "Newsprint", NEWS), ("white", "White", WHITE), ("charcoal", "Charcoal", CHAR), ("prussian", "Prussian", PRUS)]

# Drawing keys: (concept, cut). C has two cuts; its line cut starts at 24 px.
DRAWINGS = [("A", "line"), ("B", "flat"), ("C", "line"), ("C", "flat")]
CONCEPT_NAME = {"A": "Line and node", "B": "Flat kit", "C": "One drawing, two cuts"}
CUT_NAME = {("A", "line"): "Line", ("B", "flat"): "Flat", ("C", "line"): "Line cut", ("C", "flat"): "Flat cut"}


def sizes(concept, cut):
    return D.SIZES_FOR[(concept, cut)]


def stem(concept, cut, name, size):
    """Dated Title-Case file stem for a master, for example 20261028_Concept-A-Explain-24px."""
    c = f"Concept-{concept}" + (f"-{cut.title()}" if concept == "C" else "")
    return f"{DATE}_{c}-{D.FILE_NAME[name]}-{size}px"


def best_size(concept, cut, size):
    """The master to use for a display size: the 16 px master at 16, the 24 px master above."""
    s = sizes(concept, cut)
    return 16 if (size <= 16 and 16 in s) else 24


# Colorways: ink color, node color, seat fill.
COLORWAYS = {
    "Ink-Charcoal-Red": (CHAR, RED, None),        # standalone on Newsprint, White, Newsprint tile (signature red)
    "Ink-Charcoal-Keyline": (CHAR, RED, CHAR),    # current item in a row on Newsprint (working red, 1 px keyline)
    "Ink-Charcoal": (CHAR, CHAR, None),            # one color, light surfaces
    "Ink-Newsprint-Red": (NEWS, RED, None),       # standalone on Charcoal, Charcoal tile
    "Ink-Newsprint": (NEWS, NEWS, None),           # one color on Charcoal
    "Ink-White": (WHITE, WHITE, None),             # Prussian: one color, no red
}


def lay_for(concept, cut, name, size):
    return D.draw(concept, cut, name, size)


def svg_doc(lay, size, colorway="Ink-Charcoal-Red", px=None, title=None, master=False):
    ink, node, seat = COLORWAYS[colorway]
    px = px or size
    t = f"<title>{title}</title>" if title else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {size} {size}">{t}']
    parts.append(f'<path id="ink" d="{g.d_of(lay["ink"])}" fill="{ink}"/>')
    if master:
        parts.append(f'<path id="seat" d="{g.d_of(lay["seat"])}" fill="none"/>')
    elif seat:
        parts.append(f'<path id="seat" d="{g.d_of(lay["seat"])}" fill="{seat}"/>')
    parts.append(f'<path id="node" d="{g.d_of(lay["node"])}" fill="{node}"/>')
    parts.append("</svg>")
    return "".join(parts)


def rel(p):
    """Path relative to work/boards/, for the board's src attributes."""
    return str(Path(p).relative_to(BOARDS))


def variant_path(concept, cut, name, size, colorway):
    if colorway == "Ink-Charcoal-Red":
        return OUT / f"{stem(concept, cut, name, size)}.svg"
    return VARIANTS / f"{stem(concept, cut, name, size)}-{colorway}.svg"


# ---------------------------------------------------------------- holders
# The icon's 20-unit live area is half the holder's side. A 24 px master sits in a 40 px holder,
# a 16 px master in a 28 px holder; larger sizes scale the vectors.
HOLDER_SHAPES = ["Square", "Rounded-Square", "Circle"]
HOLDER_COLORS = {"Charcoal": (CHAR, "Ink-Newsprint-Red"), "Newsprint": (NEWS, "Ink-Charcoal-Red"), "Prussian": (PRUS, "Ink-White")}
LIVE_FRACTION = 0.5          # live area side as a share of the holder side
FIELD_FRACTION = 0.6         # the 24-unit icon field as a share of the holder side
CORNER_RADIUS = 0.2237       # smoothed-corner radius as a share of the side
CORNER_SMOOTHING = 0.6
CIRCLE_SAFE = 0.40           # ink stays within this share of the diameter from the center


def holder_path(shape, size):
    if shape == "Square":
        return g.rect(0, 0, size, size)
    if shape == "Rounded-Square":
        return g.smoothed_square(0, 0, size, CORNER_RADIUS, CORNER_SMOOTHING)
    if shape == "Circle":
        return g.circle(size / 2, size / 2, size / 2)
    raise ValueError(shape)


def holder_file(shape, color):
    return HOLDERS / f"{DATE}_Holder-{shape}-{color}.svg"


def contrast(a, b):
    def lum(h):
        h = h.lstrip("#")
        r, gg, bb = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4  # noqa: E731
        return 0.2126 * f(r) + 0.7152 * f(gg) + 0.0722 * f(bb)
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
