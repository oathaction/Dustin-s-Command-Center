"""Shared paths, palette, master loading and SVG writing for Concept 2, Moving part, stage 2.

Design director, Phase 2 round two, October 28, 2026. Run every script with python3 -I.
  icons_r2_moving_masters.py      display, 24 px and 16 px masters, at rest and open, and the color variants
  icons_r2_moving_assets.py       holders, the 1024 px app tile and its glyph-scale test, the eight contexts
  icons_r2_moving_measure.py      the checks and tests 2 to 4, written as JSON
  icons_r2_moving_board.py        the concept board
  icons_r2_moving_board_check.js  layout check and captures of the board
Round one's icons_common.py is imported for its palette, holder geometry and contrast function,
never changed.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_common as RC  # noqa: E402  (round one, read only)
import icons_r2_moving_draw as D  # noqa: E402

ROOT = HERE.parents[3]
DATE = "20261028"
BOARDS = ROOT / "work/boards"
OUT = BOARDS / "phase-2/icons-r2/moving-part"
VARIANTS = OUT / "variants"
HOLDERS = OUT / "holders"
APP = OUT / "app-tile"
CONTEXT = OUT / "context"
PX = OUT / "px"
BENCH = OUT / "benchmark"
HANDOFF = ROOT / "work/handoffs/phase-2"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/r2-moving-part/build")
RENDER_JS = HERE / "icons_render_cells.js"           # round one's renderer, called as is
SHOT_JS = HERE / "icons_r2_moving_shot.js"
FONTS = ROOT / "work/extract/v5-polished/fonts"

NEWS, CHAR, RED, PRUS, WHITE, STONE = RC.NEWS, RC.CHAR, RC.RED, RC.PRUS, RC.WHITE, RC.STONE
contrast = RC.contrast

SIZES = ["Display", "24px", "16px"]
UNITS = {"Display": 24, "24px": 24, "16px": 16}      # viewBox side

# Colorways: (ink fill, accent fill or None to remove the red piece, keyline fill or None)
COLORWAYS = {
    "Charcoal-Red": (CHAR, RED, None),            # standalone on Newsprint or White; Newsprint tile
    "Charcoal": (CHAR, CHAR, None),               # one color: the red piece turned to ink (idle row item)
    "Charcoal-No-Red": (CHAR, None, None),        # the red piece removed (cover-the-red test)
    "Newsprint-Red": (NEWS, RED, None),           # standalone on Charcoal; Charcoal tile
    "Newsprint": (NEWS, NEWS, None),              # one color on Charcoal
    "Newsprint-No-Red": (NEWS, None, None),
    "White": (WHITE, WHITE, None),                # Prussian: White, no red
    "White-No-Red": (WHITE, None, None),
    "Charcoal-Red-Keyline": (CHAR, RED, CHAR),    # current item on Newsprint at 16 and 24 px
}


def master_file(name, size, open_=False):
    return OUT / f"{DATE}_Moving-Part-{D.FILE_NAME[name]}-{size}{'-Open' if open_ else ''}.svg"


def variant_file(name, size, colorway, open_=False):
    if colorway == "Charcoal-Red":
        return master_file(name, size, open_)
    return VARIANTS / f"{DATE}_Moving-Part-{D.FILE_NAME[name]}-{size}{'-Open' if open_ else ''}-{colorway}.svg"


_PATH = re.compile(r'<path id="(\w+)" d="([^"]*)"')


def load(name, size, open_=False):
    """The master as {"ink": d, "accent": d, "keyline": d or ""} read from its SVG file."""
    s = master_file(name, size, open_).read_text()
    out = {"ink": "", "accent": "", "keyline": ""}
    out.update({k: v for k, v in _PATH.findall(s)})
    return out


def svg(m, units, colorway="Charcoal-Red", px=None, title=None, bg=None, carry_keyline=False):
    """One icon as SVG. m holds the ink, accent and keyline path data. A master carries its keyline
    unfilled (carry_keyline), the way round one's masters carried the seat."""
    ink, acc, key = COLORWAYS[colorway]
    px = px or units
    t = f"<title>{title}</title>" if title else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {units} {units}">{t}']
    if bg:
        parts.append(f'<rect width="{units}" height="{units}" fill="{bg}"/>')
    parts.append(f'<path id="ink" d="{m["ink"]}" fill="{ink}"/>')
    if key and m.get("keyline"):
        parts.append(f'<path id="keyline" d="{m["keyline"]}" fill="{key}"/>')
    elif carry_keyline and m.get("keyline"):
        parts.append(f'<path id="keyline" d="{m["keyline"]}" fill="none"/>')
    if acc:
        parts.append(f'<path id="accent" d="{m["accent"]}" fill="{acc}"/>')
    parts.append("</svg>")
    return "".join(parts)


def inner(m, units, colorway="Charcoal-Red", scale=1.0, dx=0.0, dy=0.0):
    """The icon's paths as a <g> for placing inside another SVG (holders, tiles, cards)."""
    ink, acc, key = COLORWAYS[colorway]
    parts = [f'<g transform="translate({dx:.3f} {dy:.3f}) scale({scale:.5f})">', f'<path d="{m["ink"]}" fill="{ink}"/>']
    if key and m.get("keyline"):
        parts.append(f'<path d="{m["keyline"]}" fill="{key}"/>')
    if acc:
        parts.append(f'<path d="{m["accent"]}" fill="{acc}"/>')
    parts.append("</g>")
    return "".join(parts)


def best(px):
    """The master to set at a display size: 16 px at 16 and under, 24 px up to 47, the display master above."""
    return "16px" if px <= 16 else ("24px" if px < 48 else "Display")


def rel(p):
    """Path relative to work/boards/, for the board's src attributes."""
    return str(Path(p).relative_to(BOARDS))


def font_css():
    """Local @font-face rules for renders made outside the board (contexts, sheets)."""
    rules = []
    for fam, f, w, st in (("Inter", "Inter-400-normal.ttf", 400, "normal"), ("Inter", "Inter-600-normal.ttf", 600, "normal"),
                          ("Inter", "Inter-700-normal.ttf", 700, "normal"), ("Inter Tight", "Inter-Tight-600-normal.ttf", 600, "normal"),
                          ("Inter Tight", "Inter-Tight-800-normal.ttf", 800, "normal"), ("Lora", "Lora-Italic-400-normal.ttf", 400, "italic")):
        if (FONTS / f).exists():
            rules.append(f"@font-face{{font-family:'{fam}';src:url('file://{FONTS / f}');font-weight:{w};font-style:{st}}}")
    return "".join(rules)
