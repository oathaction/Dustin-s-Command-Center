"""Shared paths, palette, colorways, SVG writers and holders for Concept 1, Overprint (design
director, Phase 2, round two, October 28, 2026).

Scripts, in rebuild order (each run with python3 -I):
  icons_r2_overprint_assets.py    masters, variants, holders, tiles, app tile, pixel renders
  icons_r2_overprint_contexts.py  the eight contexts, rendered to PNG
  icons_r2_overprint_measure.py   the checks and tests 2 to 4, written to JSON
  icons_r2_overprint_board.py     the concept board
then node icons_board_check.js (round one's layout check, unchanged) on the board.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_overprint_draw as O  # noqa: E402
import icons_geom as g  # noqa: E402
import icons_common as RC  # noqa: E402  (round one: holder geometry; imported, never changed)

ROOT = HERE.parents[3]
DATE = "20261028"
BOARDS = ROOT / "work/boards"
OUT = BOARDS / "phase-2/icons-r2/overprint"
VARIANTS = OUT / "variants"
HOLDERS = OUT / "holders"
CONTEXT = OUT / "context"
PX = OUT / "px"
SCREENS = OUT / "screens"
HANDOFF = ROOT / "work/handoffs/phase-2"
FONTS = ROOT / "work/extract/v5-polished/fonts"
SPRITE = ROOT / "work/extract/v5-polished/sprite"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/overprint/build")
RENDER_JS = HERE / "icons_render_cells.js"        # round one's cell renderer, unchanged
SHOT_JS = HERE / "icons_r2_overprint_shot.js"
BOARD = BOARDS / f"{DATE}_Icon-Concept-1-Overprint.html"
NOTES = HANDOFF / f"{DATE}_Icon-Concept-1-Overprint-Notes.md"
MEAS = OUT / f"{DATE}_Overprint-Measurements.json"

NEWS, CHAR, RED, PRUS, WHITE, STONE = "#DCD9D2", "#121212", "#E63946", "#1F2D5A", "#FFFFFF", "#5D636D"
SURFACES = [("newsprint", "Newsprint", NEWS), ("white", "White", WHITE), ("charcoal", "Charcoal", CHAR), ("prussian", "Prussian", PRUS)]
KINDS = ["16px", "24px", "Display"]

# Colorways: ink color and plane color (None drops the plane).
COLORWAYS = {
    "Charcoal-Red": (CHAR, RED),        # alone on Newsprint or White, the Newsprint tile, the current item in a row
    "Charcoal": (CHAR, None),           # idle in a row on a light surface
    "Newsprint-Red": (NEWS, RED),       # alone on Charcoal, the Charcoal tile
    "Newsprint": (NEWS, None),          # idle in a row on Charcoal
    "White": (WHITE, None),             # Prussian: one color, no red
    "Charcoal-Plane-Ink": (CHAR, CHAR),  # test 2: the plane turned to ink
}


def lay(name, kind):
    if kind == "Display":
        return O.display(name)
    return O.master(name, int(kind[:-2]))


def vb(kind):
    return 16 if kind == "16px" else 24


def stem(name, kind):
    return f"{DATE}_Overprint-{O.FILE_NAME[name]}-{kind}"


def master_file(name, kind):
    return OUT / f"{stem(name, kind)}.svg"


def variant_file(name, kind, cw):
    if cw == "Charcoal-Red":
        return master_file(name, kind)
    return VARIANTS / f"{stem(name, kind)}-{cw}.svg"


def svg(lay_, kind, px=None, cw="Charcoal-Red", title=None):
    ink, acc = COLORWAYS[cw]
    return O.svg(lay_, px or vb(kind), ink=ink, accent=acc, title=title, vb=vb(kind))


def best_kind(px):
    """The master for a display size: 16 px master at 16 and under, 24 px master to 47, display above."""
    if px <= 16:
        return "16px"
    if px < 48:
        return "24px"
    return "Display"


def rel(p):
    return str(Path(p).relative_to(BOARDS))


# ---------------------------------------------------------------- holders
# Round one's holder geometry (RC): the rounded square is a true superellipse with exponent 5; the
# icon's 24-unit field is 60 percent of the side, so its 20-unit live area is half the side; in the
# circle, ink stays within 40 percent of the side from the center.
HOLDER_SHAPES = ["Square", "Rounded-Square", "Circle"]
HOLDER_COLORS = {"Charcoal": (CHAR, "Newsprint-Red"), "Newsprint": (NEWS, "Charcoal-Red"), "Prussian": (PRUS, "White")}
FIELD = RC.FIELD_FRACTION


def tile_svg(name, shape, color, size, field=FIELD, cw=None, title=None):
    """One holder with its icon as a single SVG at `size` px. A 40 px holder takes the 24 px master
    on whole pixels, a 28 px holder the 16 px master; larger holders scale the display master."""
    fill, cw0 = HOLDER_COLORS[color]
    cw = cw or cw0
    ink_c, acc_c = COLORWAYS[cw]
    if size == 40 and abs(field - FIELD) < 1e-9:
        kind, s, sc, off = "24px", 24, 1.0, 8.0
    elif size == 28 and abs(field - FIELD) < 1e-9:
        kind, s, sc, off = "16px", 16, 1.0, 6.0
    else:
        kind, s = "Display", 24
        sc = size * field / 24
        off = size * (1 - field) / 2
    L = lay(name, kind)
    hp = RC.holder_path(shape, size)
    t = f"<title>{title}</title>" if title else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{t}',
             f'<path d="{g.d_of(hp)}" fill="{fill}"/>']
    if acc_c and not g.is_empty(L["accent"]):
        parts.append(f'<path id="accent" d="{g.d_of(g.transform(L["accent"], sc, off, off))}" fill="{acc_c}"/>')
    parts.append(f'<path id="ink" d="{g.d_of(g.transform(L["ink"], sc, off, off))}" fill="{ink_c}"/>')
    parts.append("</svg>")
    return "".join(parts), L, sc, off


def holder_file(shape, color):
    return HOLDERS / f"{DATE}_Overprint-Holder-{shape}-{color}.svg"


def tile_file(name, shape, color):
    return HOLDERS / f"{DATE}_Overprint-{O.FILE_NAME[name]}-{shape}-{color}.svg"


APP_SCALES = [0.56, 0.62, 0.66]     # the icon's 20-unit live area as a share of the tile's side
APP_ICON = "act"
APP_SCALE = 0.62                    # chosen by eye at 180, 60 and 29 px; logged in the notes


def app_tile_file(scale=None):
    sc = APP_SCALE if scale is None else scale
    return CONTEXT / f"{DATE}_Overprint-App-Tile-1024-{int(round(sc * 100))}.svg"


def app_tile_svg(scale, color="Charcoal", size=1024):
    """The app tile: the superellipse in Charcoal with the Act display master in Newsprint and its
    red plane. The icon's 20-unit live area is `scale` of the side."""
    field = scale * 24 / 20
    s, L, sc, off = tile_svg(APP_ICON, "Rounded-Square", color, size, field=field,
                             title=f"Oath &amp; Action app tile, Concept 1 Overprint, live area {int(round(scale * 100))} percent of the side. Proposal only.")
    return s


def contrast(a, b):
    return RC.contrast(a, b)
