"""Shared paths, palette, colorways, holders and SVG writing for Concept 3, Public sign, stage 2.

Run order (python3 -I for every script):
  icons_r2_sign_assets.py    masters, variants, holders, app tiles, context art, pixel renders
  icons_r2_sign_measure.py   every check, written to the measurements JSON
  icons_r2_sign_board.py     the concept board
  node icons_r2_sign_board_check.js <board> <json> <screens dir>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_common as RC  # noqa: E402  (round one, read only: superellipse holder and contrast)
import icons_r2_sign_draw as D  # noqa: E402
import icons_r2_sign_geom as G  # noqa: E402
import icons_r2_sign_masters as M  # noqa: E402
import numpy as np  # noqa: E402

ROOT = HERE.parents[3]
DATE = "20261028"
BOARDS = ROOT / "work/boards"
OUT = BOARDS / "phase-2/icons-r2/public-sign"
VARIANTS = OUT / "variants"
HOLDERS = OUT / "holders"
CONTEXT = OUT / "context"
PX = OUT / "px"
SCREENS = OUT / "screens"
HANDOFF = ROOT / "work/handoffs/phase-2"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/sign-build")
RENDER_JS = HERE / "icons_render_cells.js"     # round one's renderer, used as is
SHOT_JS = HERE / "icons_r2_sign_shot.js"
BOARD = BOARDS / f"{DATE}_Icon-Concept-3-Public-Sign.html"
NOTES = HANDOFF / f"{DATE}_Icon-Concept-3-Public-Sign-Notes.md"
MEASURE_JSON = OUT / f"{DATE}_Public-Sign-Measurements.json"

NEWS, CHAR, RED, PRUS, WHITE, STONE = "#DCD9D2", "#121212", "#E63946", "#1F2D5A", "#FFFFFF", "#5D636D"
SURFACES = [("newsprint", "Newsprint", NEWS), ("white", "White", WHITE), ("charcoal", "Charcoal", CHAR), ("prussian", "Prussian", PRUS)]
KINDS = ("16px", "24px", "Display")
contrast = RC.contrast

# Colorways: ink color, accent mode, accent color.
#   red     the accent in Pillar Red (standalone: signature red under Rule 05.3)
#   ink     the accent set in the ink color (test 2, red turned to ink)
#   none    the accent removed: the idle state in a row (test 2, red removed)
#   keyline the accent in red with a 1 px Charcoal keyline: the current item in a row on Newsprint
COLORWAYS = {
    "Charcoal-Red": (CHAR, "red"),
    "Charcoal-Red-As-Ink": (CHAR, "ink"),
    "Charcoal-Idle": (CHAR, "none"),
    "Charcoal-Keyline": (CHAR, "keyline"),
    "Newsprint-Red": (NEWS, "red"),
    "Newsprint-Red-As-Ink": (NEWS, "ink"),
    "Newsprint-Idle": (NEWS, "none"),
    "White-Idle": (WHITE, "none"),
}


def stem(name, kind):
    return f"{DATE}_Public-Sign-{D.FILE_NAME[name]}-{kind}"


def layers(name, kind):
    if kind == "Display":
        return D.display(name), 24
    s = int(kind[:-2])
    return M.master(name, s), s


def _keyline(acc, size, kind):
    """A 1 px Charcoal ring around the accent: pixel-dilated for the 16 and 24 px masters."""
    if kind == "Display":
        return None
    m = M.mask(acc, size)
    pd = np.pad(m, 1)
    dil = pd[1:-1, 1:-1] | pd[:-2, 1:-1] | pd[2:, 1:-1] | pd[1:-1, :-2] | pd[1:-1, 2:] | pd[:-2, :-2] | pd[:-2, 2:] | pd[2:, :-2] | pd[2:, 2:]
    ring = dil & ~m
    rects = [G.rect(x, y, 1, 1) for y, x in zip(*np.nonzero(ring))]
    return G.union(*rects) if rects else None


def svg(name, kind, colorway="Charcoal-Red", px=None, title=None, ids=False):
    lay, size = layers(name, kind)
    ink_c, mode = COLORWAYS[colorway]
    px = px or (24 if kind == "Display" else size)
    t = f"<title>{title}</title>" if title else ""
    ink_id = ' id="ink"' if ids else ""
    acc_id = ' id="accent"' if ids else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {size} {size}">{t}']
    if mode == "keyline":
        kl = _keyline(lay["accent"], size, kind)
        if kl is not None:
            parts.append(f'<path d="{G.d_of(kl)}" fill="{CHAR}"/>')
    parts.append(f'<path{ink_id} d="{G.d_of(lay["ink"])}" fill="{ink_c}"/>')
    if mode in ("red", "keyline"):
        if mode == "keyline" and kind == "Display":
            parts.append(f'<path{acc_id} d="{G.d_of(lay["accent"])}" fill="{RED}" stroke="{CHAR}" stroke-width="0.5" paint-order="stroke"/>')
        else:
            parts.append(f'<path{acc_id} d="{G.d_of(lay["accent"])}" fill="{RED}"/>')
    elif mode == "ink":
        parts.append(f'<path{acc_id} d="{G.d_of(lay["accent"])}" fill="{ink_c}"/>')
    parts.append("</svg>")
    return "".join(parts)


def master_file(name, kind):
    return OUT / f"{stem(name, kind)}.svg"


def variant_file(name, kind, colorway):
    if colorway == "Charcoal-Red":
        return master_file(name, kind)
    return VARIANTS / f"{stem(name, kind)}-{colorway}.svg"


def rel(p):
    return str(Path(p).relative_to(BOARDS))


# ---------------------------------------------------------------- holders
# The square sign panel leads: the icon's 24-unit field takes 60 percent of the side and its
# 20-unit live area half the side, as in round one, so 1 unit of the icon grid is 1/40 of the side
# and the panel's 2-unit corner radius is 5 percent of the side. A 24 px master sits in a 40 px
# holder and a 16 px master in a 28 px holder on whole pixels; larger sizes scale the display master.
HOLDER_SHAPES = ["Sign-Panel", "Superellipse", "Circle"]
HOLDER_LABEL = {"Sign-Panel": "Square sign panel", "Superellipse": "Rounded square (superellipse)", "Circle": "Circle"}
HOLDER_COLORS = {"Charcoal": (CHAR, "Newsprint-Red"), "Newsprint": (NEWS, "Charcoal-Red"), "Prussian": (PRUS, "White-Idle")}
FIELD_FRACTION = RC.FIELD_FRACTION      # 0.6
LIVE_FRACTION = RC.LIVE_FRACTION        # 0.5
CIRCLE_SAFE = RC.CIRCLE_SAFE            # 0.40
PANEL_RADIUS = 2 / 40                   # 2 grid units on a 40-unit side


def holder_path(shape, size):
    if shape == "Sign-Panel":
        return G.box(0, 0, size, size, PANEL_RADIUS * size)
    if shape == "Superellipse":
        return G.g.superellipse(0, 0, size, RC.SUPERELLIPSE_N)
    if shape == "Circle":
        return G.circle(size / 2, size / 2, size / 2)
    raise ValueError(shape)


def tile_kind(size):
    return "16px" if size == 28 else ("24px" if size == 40 else "Display")


def tile_svg(name, shape, color, size, title=None, mode=None):
    """One holder with its icon as a single SVG at `size` px."""
    fill, cw = HOLDER_COLORS[color]
    if mode is not None:
        cw = {"none": cw.split("-")[0] + "-Idle"}.get(mode, cw)
    kind = tile_kind(size)
    lay, s = layers(name, kind)
    if size == 28:
        off, sc = 6.0, 1.0
    elif size == 40:
        off, sc = 8.0, 1.0
    else:
        off, sc = size * (1 - FIELD_FRACTION) / 2, size * FIELD_FRACTION / 24
    ink_c, m = COLORWAYS[cw]
    t = f"<title>{title}</title>" if title else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{t}',
             f'<path d="{G.d_of(holder_path(shape, size))}" fill="{fill}"/>',
             f'<path d="{G.d_of(G.g.transform(lay["ink"], sc, off, off))}" fill="{ink_c}"/>']
    if m == "red":
        parts.append(f'<path d="{G.d_of(G.g.transform(lay["accent"], sc, off, off))}" fill="{RED}"/>')
    parts.append("</svg>")
    return "".join(parts), lay, sc, off


def tile_file(name, shape, color, size):
    return HOLDERS / f"{DATE}_Public-Sign-{D.FILE_NAME[name]}-{shape}-{color}-{size}.svg"
