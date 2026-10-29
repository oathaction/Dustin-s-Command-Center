"""Shared constants and helpers for the Civic Line icon pipeline.

Paths, the catalog parser, filename slugs, the midpoint ink and red rules,
and small image helpers. Every other script in this folder imports this one.
"""
import json
import os
import re

import numpy as np
from PIL import Image, ImageFont

DATE = "20261029"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REF_DIR = os.path.join(ROOT, "work", "research", "chat-references", "civic-line")
CATALOG = os.path.join(ROOT, "brief", "phase-prompts", "20261029_Civic-Line-Icon-Reconstruction-Prompt.md")
ASSETS = os.path.join(ROOT, "work", "build", "assets", "civic-line")
SRC = os.path.join(ASSETS, "src")
QA = os.path.join(ASSETS, "qa")
INVENTORY_JSON = os.path.join(ASSETS, f"{DATE}_Civic-Line-Inventory.json")
INVENTORY_CSV = os.path.join(ASSETS, f"{DATE}_Civic-Line-Inventory.csv")
SCALE_JSON = os.path.join(QA, f"{DATE}_Civic-Line-Scale-And-Stroke.json")
RENDER_JS = os.path.join(HERE, "render_svgs.js")

CHARCOAL = "#121212"
PILLAR_RED = "#E63946"
NEWSPRINT = "#DCD9D2"

VIEW = 128.0          # export viewBox size
FILL_EXTENT = 116.0   # the largest pictogram extent maps to this many units
CROP_MARGIN = 8       # source px around the pictogram ink box
FRAMING_CAP = 1.25    # DR-08: an icon grows toward FILL_EXTENT by at most this times the shared scale

# The four bare editions (DR-07, DR-09). Each is the red-black file with its ink
# colours swapped; mask colours (#FFFFFF, #000000) are mask semantics and stay.
EDITIONS = {
    "red-black": {"suffix": "Red-Black", "ink": "#121212", "accent": "#E63946", "ground": "light"},
    "black": {"suffix": "Black", "ink": "#121212", "accent": "#121212", "ground": "light"},
    "red-newsprint": {"suffix": "Red-Newsprint", "ink": "#DCD9D2", "accent": "#E63946", "ground": "dark"},
    "newsprint": {"suffix": "Newsprint", "ink": "#DCD9D2", "accent": "#DCD9D2", "ground": "dark"},
}
EDITION_COLOURS = {k: sorted({v["ink"], v["accent"]}) for k, v in EDITIONS.items()}

# Tiles (DR-10): three shapes, two tile colours, two colour modes. A Charcoal
# tile carries the light editions, a Newsprint tile the dark ones.
TILE_SHAPES = ["square", "rounded", "circle"]
TILE_COLOURS = ["charcoal", "newsprint"]
TILE_MODES = ["two-color", "one-color"]
TILE_EDITION = {("charcoal", "two-color"): "red-newsprint", ("charcoal", "one-color"): "newsprint",
                ("newsprint", "two-color"): "red-black", ("newsprint", "one-color"): "black"}
TILE_FILL = {"charcoal": "#121212", "newsprint": "#DCD9D2"}
# One uniform factor per shape, applied to the option-3 icon box; chosen on the
# calibration board (qa/<date>_Civic-Line-Tile-Calibration.png).
TILE_FACTORS = {"square": 0.68, "rounded": 0.66, "circle": 0.62}
TILE_SAFE_MARGIN = 12.0   # units of 128: the least clearance ink may keep from any tile edge

SHEETS = {
    "01": {"black": f"{DATE}_Oath-And-Action-Civic-Line-01-Participation-Black.png",
           "red": f"{DATE}_Oath-And-Action-Civic-Line-01-Participation-Red.png",
           "cols": 6, "rows": 4, "reform": False},
    "02": {"black": f"{DATE}_Oath-And-Action-Civic-Line-02-Government-Tech-Black.png",
           "red": f"{DATE}_Oath-And-Action-Civic-Line-02-Government-Tech-Red.png",
           "cols": 6, "rows": 4, "reform": False},
    "03": {"black": f"{DATE}_Oath-And-Action-Civic-Line-03-Economy-Issues-Black.png",
           "red": f"{DATE}_Oath-And-Action-Civic-Line-03-Economy-Issues-Red.png",
           "cols": 6, "rows": 4, "reform": False},
    "04": {"black": f"{DATE}_Oath-And-Action-Civic-Line-04-Reforms-01-25-Black.png",
           "red": f"{DATE}_Oath-And-Action-Civic-Line-04-Reforms-01-25-Red.png",
           "cols": 5, "rows": 5, "reform": True},
    "05": {"black": f"{DATE}_Oath-And-Action-Civic-Line-05-Reforms-26-50-Black.png",
           "red": f"{DATE}_Oath-And-Action-Civic-Line-05-Reforms-26-50-Red.png",
           "cols": 5, "rows": 5, "reform": True},
}


# ---------------------------------------------------------------- catalog

ENTRY_RE = re.compile(r"^((?:CL|R)-\d+) · (.+) · Row (\d+), column (\d+)\s*$")
SHEET_RE = re.compile(r"^Sheet (\d\d): (.+?)\s*$")


def slugify(label):
    """Title-Case words joined by hyphens. '&' -> 'And', the middle dot is dropped,
    'AI' stays uppercase, existing hyphens stay."""
    s = label.replace("&", " And ").replace("·", " ")
    words = [w for w in re.split(r"\s+", s) if w]
    out = []
    for w in words:
        parts = w.split("-")
        fixed = []
        for p in parts:
            if p == "AI":
                fixed.append("AI")
            elif p:
                fixed.append(p[0].upper() + p[1:])
            else:
                fixed.append(p)
        out.append("-".join(fixed))
    return "-".join(out)


def parse_catalog(path=CATALOG):
    """Return the 122 catalog entries in file order with construction and red text."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    entries = []
    sheet = None
    cur = None
    for line in lines[127:]:
        m = SHEET_RE.match(line)
        if m:
            sheet = m.group(1)
            continue
        m = ENTRY_RE.match(line)
        if m:
            cur = {"id": m.group(1), "label": m.group(2), "row": int(m.group(3)),
                   "column": int(m.group(4)), "sheet": sheet, "construction": "", "red": ""}
            entries.append(cur)
            continue
        if cur is None:
            continue
        if line.startswith("Construction:"):
            cur["construction"] = line[len("Construction:"):].strip()
        elif line.startswith("Red:"):
            cur["red"] = line[len("Red:"):].strip()
    for e in entries:
        e["slug"] = slugify(e["label"])
    return entries


def export_names(icon_id, slug):
    base = f"{DATE}_Oath-And-Action-Civic-Line-{icon_id}-{slug}"
    out = {"ref_black": f"{base}-Reference-Black.png", "ref_red": f"{base}-Reference-Red.png"}
    for ed, e in EDITIONS.items():
        key = ed.replace("-", "_")
        out[f"svg_{key}"] = f"{base}-{e['suffix']}.svg"
        out[f"png_{key}"] = f"{base}-{e['suffix']}.png"
    return out


def edition_file(row, edition, kind="svg", size=None):
    """Path of a bare export: kind 'svg', or 'png' with size 256 or 512."""
    key = f"{kind}_{edition.replace('-', '_')}"
    name = export_names(row["id"], row["slug"])[key]
    if kind == "svg":
        return os.path.join(ASSETS, edition, name)
    return os.path.join(ASSETS, f"png-{size}", edition, name)


def tile_name(icon_id, slug, shape, tile, mode):
    sh = {"square": "Square", "rounded": "Rounded", "circle": "Circle"}[shape]
    md = {"two-color": "Two-Color", "one-color": "One-Color"}[mode]
    return f"{DATE}_Oath-And-Action-Civic-Line-{icon_id}-{slug}-Tile-{sh}-{tile.capitalize()}-{md}"


def tile_file(row, shape, tile, mode, kind="svg", size=None):
    base = tile_name(row["id"], row["slug"], shape, tile, mode)
    folder = os.path.join(ASSETS, "tiles", f"{shape}-{tile}")
    if kind == "svg":
        return os.path.join(folder, "svg", base + ".svg")
    return os.path.join(folder, f"png-{size}", base + ".png")


def framed_scale(extent_px, s_shared):
    """DR-08 capped fit: grow toward FILL_EXTENT, by at most FRAMING_CAP times the shared scale."""
    return min(FILL_EXTENT / extent_px, FRAMING_CAP * s_shared)


# ---------------------------------------------------------------- pixel rules
#
# Ink: the green channel. On the black sheet the ink is neutral, so green equals
# luminance within a level or two. On the red sheet green separates both inks
# from the background by the same amount (bg G about 219, black G about 7,
# Pillar Red G about 16 to 30), so red and black strokes threshold alike.
# A pixel is ink when its green value is darker than the midpoint between the
# local background and full ink.
#
# Red: redness = R - max(G, B). Background redness is about 1, full red about
# 185. A pixel is red when its redness passes the midpoint between the local
# background redness and full red.

def green(rgb):
    return rgb[..., 1].astype(np.float64)


def redness(rgb):
    a = rgb.astype(np.float64)
    return a[..., 0] - np.maximum(a[..., 1], a[..., 2])


def border_ring(arr, width=3):
    h, w = arr.shape[:2]
    m = np.zeros((h, w), bool)
    m[:width, :] = m[-width:, :] = True
    m[:, :width] = m[:, -width:] = True
    return arr[m]


def local_background(rgb):
    """Median RGB of the crop's outer ring, which by construction holds no ink."""
    ring = border_ring(rgb, 3).reshape(-1, 3).astype(np.float64)
    g = ring[:, 1]
    keep = g > np.percentile(g, 20)  # ignore any stray dark pixel on the ring
    return np.median(ring[keep], axis=0)


def ink_threshold(bg_rgb, full_ink_g):
    return (float(bg_rgb[1]) + float(full_ink_g)) / 2.0


def red_threshold(bg_rgb, full_red):
    bg_r = float(bg_rgb[0]) - max(float(bg_rgb[1]), float(bg_rgb[2]))
    return (bg_r + float(full_red)) / 2.0


def ink_mask(rgb, bg_rgb, full_ink_g):
    return green(rgb) < ink_threshold(bg_rgb, full_ink_g)


def red_mask(rgb, bg_rgb, full_red):
    return redness(rgb) > red_threshold(bg_rgb, full_red)


# ---------------------------------------------------------------- io helpers

def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"))


def save_mask(mask, path):
    Image.fromarray((mask.astype(np.uint8) * 255)).save(path)


def load_mask(path):
    return np.asarray(Image.open(path).convert("L")) > 127


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _np_default(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"not JSON serializable: {type(o)}")


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False, default=_np_default)
        fh.write("\n")
    os.replace(tmp, path)


def load_inventory():
    inv = read_json(INVENTORY_JSON)
    if inv is None:
        raise SystemExit(f"Inventory missing: {INVENTORY_JSON}. Run crop_references.py first.")
    return inv


def inventory_by_id():
    return {r["id"]: r for r in load_inventory()["icons"]}


def font(size, bold=False):
    names = ["/usr/share/fonts/opentype/inter/Inter-SemiBold.otf" if bold else
             "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for n in names:
        if os.path.exists(n):
            return ImageFont.truetype(n, size)
    return ImageFont.load_default(size=size)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
