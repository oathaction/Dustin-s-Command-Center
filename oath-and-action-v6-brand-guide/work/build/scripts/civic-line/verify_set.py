"""Verify the Civic Line set and compile the completion ledger.

    python3 -I verify_set.py [--sync-inventory]

Checks, for the four bare editions (DR-07, DR-09): membership and counts
(122 IDs, 488 SVGs, 976 PNGs), each edition's exact ink colors, that every
edition is the red-black file with its ink colours swapped and that the parsed
element trees of all four are identical apart from ink colour, SVG structure,
viewBox, drawn bounds, PNG sizes and transparency.

For the tiles (DR-10): 1,464 SVGs and 2,928 PNGs; each tile's shape comes
first and is the exact square, superellipse or circle; one group with one
uniform transform holds the icon, whose parsed tree equals its bare export of
the matching edition; Charcoal tiles carry only Newsprint and Pillar Red ink,
Newsprint tiles only Charcoal and Pillar Red; every icon keeps the safe margin
from every tile edge; PNGs are RGBA with the right transparency.

Also: reference crops (244), contact sheets (10 dark, 10 light), tile sheets
(12), and a contrast table for every ink and ground pair. Icons without a
source are reported as 'todo', not as errors, until the set is complete.
Writes qa/<date>_Civic-Line-Completion-Ledger.md, qa/<date>_Civic-Line-Verify-Report.json
and qa/<date>_Civic-Line-Contrast-Table.md. Exit code 1 on any error.
--sync-inventory copies each icon's state into the inventory JSON and CSV;
only the main session runs it, so the shared inventory has one writer.
"""
import datetime as dt
import os
import re
import sys
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import cl_svg as S  # noqa: E402
import cl_tiles as T  # noqa: E402

LEDGER = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Completion-Ledger.md")
REPORT = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Verify-Report.json")
CONTRAST = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Contrast-Table.md")
FORBIDDEN = {"text", "tspan", "textPath", "image", "foreignObject", "use", "script", "style", "pattern", "filter",
             "linearGradient", "radialGradient", "clipPath", "symbol", "a", "switch"}
MASK_COLORS = {"#FFFFFF", "#000000"}
COLOR_ATTRS = ("fill", "stroke", "stop-color", "color", "flood-color", "lighting-color")
HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
SWAPS = {"black": {C.PILLAR_RED: C.CHARCOAL}, "red-newsprint": {C.CHARCOAL: C.NEWSPRINT},
         "newsprint": {C.CHARCOAL: C.NEWSPRINT, C.PILLAR_RED: C.NEWSPRINT}}
TILE_INK = {(tl, md): set(C.EDITION_COLOURS[C.TILE_EDITION[(tl, md)]]) for tl in C.TILE_COLOURS for md in C.TILE_MODES}
SHEET_SLUGS = {"01": "Participation", "02": "Government-Tech", "03": "Economy-Issues", "04": "Reforms-01-25", "05": "Reforms-26-50"}


def strip(tag):
    return tag.split("}", 1)[-1]


def is_reddish(hexv):
    h = hexv.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        return False
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return r - max(g, b) > 40


def colour_walk(node, name, allowed, errs, in_mask=False, in_defs=False, bare=True):
    for ch in node:
        t = strip(ch.tag)
        if t in FORBIDDEN:
            errs.append(f"{name}: forbidden <{t}> element")
        if (ch.text or "").strip() and t not in ("title", "desc"):
            errs.append(f"{name}: <{t}> carries text content")
        for k in COLOR_ATTRS:
            v = ch.attrib.get(k)
            if v is None or v == "none":
                continue
            vu = v.upper()
            if not (vu in allowed or (in_mask and vu in MASK_COLORS)):
                errs.append(f"{name}: <{t}> {k}={v} is not an allowed ink here")
        if "style" in ch.attrib:
            errs.append(f"{name}: <{t}> uses a style attribute")
        if bare and t == "rect" and not in_mask and not in_defs:
            w = float(ch.attrib.get("width", 0))
            h = float(ch.attrib.get("height", 0))
            if w >= 0.9 * 128 and h >= 0.9 * 128:
                errs.append(f"{name}: background-sized <rect> {w} x {h}")
        colour_walk(ch, name, allowed, errs, in_mask or t == "mask", in_defs or t == "defs", bare)


def check_svg(path, edition, errs):
    """Structure, colors, viewBox and bounds of one bare export."""
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    name = os.path.basename(path)
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        errs.append(f"{name}: XML parse error {e}")
        return None
    if strip(root.tag) != "svg":
        errs.append(f"{name}: root is not <svg>")
    if root.attrib.get("viewBox") != "0 0 128 128":
        errs.append(f"{name}: viewBox is '{root.attrib.get('viewBox')}', expected '0 0 128 128'")
    if root.attrib.get("width") != "128" or root.attrib.get("height") != "128":
        errs.append(f"{name}: width/height must be 128")
    if "transform" in text:
        errs.append(f"{name}: contains a transform")
    colour_walk(root, name, set(C.EDITION_COLOURS[edition]), errs)
    used = {h.upper() for h in HEX_RE.findall(text)} - MASK_COLORS
    if used != set(C.EDITION_COLOURS[edition]) and not (used < set(C.EDITION_COLOURS[edition])):
        errs.append(f"{name}: ink colors {sorted(used)}, expected {C.EDITION_COLOURS[edition]}")
    if edition in ("black", "newsprint"):
        for hx in used:
            if hx == C.PILLAR_RED or is_reddish(hx):
                errs.append(f"{name}: red value {hx} in the {edition} edition")
    groups = [g.attrib.get("id") for g in root if strip(g.tag) == "g"]
    if not any(g and g.startswith("base") for g in groups):
        errs.append(f"{name}: no base group")
    b, _ = S.drawn_bounds(text.split("?>", 1)[-1])
    if b is None:
        errs.append(f"{name}: draws nothing")
    elif b[0] < 0 or b[1] < 0 or b[2] > 128 or b[3] > 128:
        errs.append(f"{name}: drawing reaches outside 0..128 with stroke counted: {[round(v, 3) for v in b]}")
    return b


def tree_identity(rb_path, other_path, edition):
    """Compare the parsed element trees of the red-black file and another edition:
    same tags in the same order, same attributes with the same values
    (coordinates, masks, ids, fill and stroke assignments, text), except a
    color attribute that carries the edition's ink swap. Returns
    (ok, elements compared, color swaps, first difference)."""
    swap = SWAPS[edition]
    a = ET.parse(rb_path).getroot()
    b = ET.parse(other_path).getroot()
    ea, eb = list(a.iter()), list(b.iter())
    if len(ea) != len(eb):
        return False, 0, 0, f"{len(ea)} elements against {len(eb)}"
    swaps = 0
    for k, (x, y) in enumerate(zip(ea, eb)):
        if x.tag != y.tag:
            return False, k, swaps, f"element {k}: <{strip(x.tag)}> against <{strip(y.tag)}>"
        if set(x.attrib) != set(y.attrib):
            return False, k, swaps, f"element {k} <{strip(x.tag)}>: attributes {sorted(set(x.attrib) ^ set(y.attrib))} differ"
        for key, va in x.attrib.items():
            vb = y.attrib[key]
            if va == vb and not (key in COLOR_ATTRS and va.upper() in swap):
                continue
            if key in COLOR_ATTRS and swap.get(va.upper()) == vb.upper():
                swaps += 1
                continue
            return False, k, swaps, f"element {k} <{strip(x.tag)}> {key}: '{va}' against '{vb}'"
        if (x.text or "").strip() != (y.text or "").strip():
            return False, k, swaps, f"element {k} <{strip(x.tag)}>: text differs"
    return True, len(ea), swaps, ""


def same_tree(a, b):
    """Exact equality of two element lists (tags, attributes, text, children)."""
    if len(a) != len(b):
        return f"{len(a)} children against {len(b)}"
    for x, y in zip(a, b):
        if x.tag != y.tag or x.attrib != y.attrib or (x.text or "").strip() != (y.text or "").strip():
            return f"<{strip(x.tag)} {x.attrib.get('id', '')}> differs"
        why = same_tree(list(x), list(y))
        if why:
            return why
    return ""


def check_png(path, size, errs, opaque_corners=False, centre_opaque=False):
    name = os.path.relpath(path, C.ASSETS)
    try:
        im = Image.open(path)
        im.load()
    except Exception as e:  # noqa: BLE001
        errs.append(f"{name}: cannot open ({e})")
        return
    if im.size != (size, size):
        errs.append(f"{name}: size {im.size}, expected {size} x {size}")
    if im.mode != "RGBA":
        errs.append(f"{name}: mode {im.mode}, expected RGBA")
        return
    a = np.asarray(im)[..., 3]
    corners = [a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]
    if opaque_corners:
        if min(corners) != 255:
            errs.append(f"{name}: a square tile must be opaque to its corners")
    else:
        if a.min() != 0 or max(corners) != 0:
            errs.append(f"{name}: background is not transparent")
    if centre_opaque and a[size // 2, size // 2] != 255:
        errs.append(f"{name}: tile centre is not opaque")
    if a.max() == 0:
        errs.append(f"{name}: image is empty")
    if not opaque_corners and not centre_opaque:
        edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
        if edge.max() > 0:
            errs.append(f"{name}: ink touches the image edge (possible clipping)")


# ------------------------------------------------------------------ tiles

def expected_shape(shape, fill):
    el = ET.fromstring(f'<svg xmlns="{S.SVG_NS}">' + T.shape_element(shape, fill) + "</svg>")[0]
    return el


def check_tile(path, row, shape, tile, mode, bare_tree, errs):
    name = os.path.basename(path)
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        errs.append(f"{name}: XML parse error {e}")
        return False
    if root.attrib.get("viewBox") != "0 0 128 128" or root.attrib.get("width") != "128":
        errs.append(f"{name}: viewBox or size is not 128")
    kids = [k for k in root if strip(k.tag) not in ("title", "desc")]
    if len(kids) != 2:
        errs.append(f"{name}: expected the tile shape and one icon group, found {len(kids)} elements")
        return False
    tile_el, grp = kids
    want = expected_shape(shape, C.TILE_FILL[tile])
    if tile_el.tag != want.tag or tile_el.attrib != want.attrib:
        errs.append(f"{name}: the first shape is not the {shape} tile in {C.TILE_FILL[tile]}")
    f = C.TILE_FACTORS[shape]
    t = 64 * (1 - f)
    if strip(grp.tag) != "g" or grp.attrib.get("id") != "icon" or grp.attrib.get("transform") != f"matrix({f:g} 0 0 {f:g} {S.fmt(t)} {S.fmt(t)})":
        errs.append(f"{name}: icon group or its transform is not the {shape} factor {f:g} about the centre")
    if set(grp.attrib) - {"id", "transform"}:
        errs.append(f"{name}: icon group carries extra attributes")
    why = same_tree(list(grp), bare_tree)
    if why:
        errs.append(f"{name}: icon geometry differs from its bare export: {why}")
    colour_walk(grp, name, TILE_INK[(tile, mode)], errs, bare=False)
    text = open(path, encoding="utf-8").read()
    if text.count("transform=") != 1:
        errs.append(f"{name}: more than one transform")
    return not why


def contrast_ratio(a, b):
    def lum(hx):
        r, g, bl = [v / 255 for v in C.hex_rgb(hx)]
        f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4  # noqa: E731
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(bl)
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


CONTRAST_PAIRS = [
    ("Charcoal lines", C.CHARCOAL, "Newsprint tile", C.NEWSPRINT, "red-black, black; Newsprint tiles"),
    ("Pillar Red accent", C.PILLAR_RED, "Newsprint tile", C.NEWSPRINT, "red-black; Newsprint two-color tiles"),
    ("Newsprint lines", C.NEWSPRINT, "Charcoal tile", C.CHARCOAL, "red-newsprint, newsprint; Charcoal tiles"),
    ("Pillar Red accent", C.PILLAR_RED, "Charcoal tile", C.CHARCOAL, "red-newsprint; Charcoal two-color tiles"),
    ("Charcoal lines", C.CHARCOAL, "White ground", "#FFFFFF", "red-black, black on White"),
    ("Pillar Red accent", C.PILLAR_RED, "White ground", "#FFFFFF", "red-black on White"),
    ("Newsprint lines", C.NEWSPRINT, "Prussian ground", "#1F2D5A", "newsprint on Prussian (red never sits on Prussian)"),
    ("Charcoal tile", C.CHARCOAL, "White page", "#FFFFFF", "tile edge"),
    ("Newsprint tile", C.NEWSPRINT, "White page", "#FFFFFF", "tile edge"),
    ("Newsprint tile", C.NEWSPRINT, "Charcoal page", C.CHARCOAL, "tile edge"),
    ("Charcoal tile", C.CHARCOAL, "Newsprint page", C.NEWSPRINT, "tile edge"),
]


def contrast_table():
    rows = []
    for ink, a, ground, b, use in CONTRAST_PAIRS:
        r = contrast_ratio(a, b)
        rows.append({"ink": ink, "ink_hex": a, "ground": ground, "ground_hex": b, "ratio": round(r, 2),
                     "meets_3_to_1": r >= 3.0, "use": use})
    L = ["# Civic Line contrast table", "",
         "WCAG 2.2 contrast ratios for every ink and ground the Civic Line editions and tiles use, computed from the brand hex values. "
         "The guideline for graphics needed to understand content (1.4.11, non-text contrast) is 3:1.", "",
         "| Ink | Ground | Ratio | 3:1 for graphics | Where it occurs |", "|---|---|---:|---|---|"]
    for r in rows:
        L.append(f"| {r['ink']} {r['ink_hex']} | {r['ground']} {r['ground_hex']} | {r['ratio']:.2f}:1 | "
                 f"{'meets' if r['meets_3_to_1'] else 'falls short'} | {r['use']} |")
    red_np = contrast_ratio(C.PILLAR_RED, C.NEWSPRINT)
    np_white = contrast_ratio(C.NEWSPRINT, "#FFFFFF")
    L += ["", f"Pillar Red on Newsprint measures {red_np:.2f}:1, under the 3:1 guideline. Every red part is a drawn shape that the one-color editions carry in Charcoal "
          "or Newsprint, so color is never the only carrier of meaning; on Newsprint the red adds emphasis to a shape that is already there. "
          f"A Newsprint tile on a White page has a soft edge ({np_white:.2f}:1); the tile shape is decoration there, not information.", ""]
    with open(CONTRAST, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return rows


# ------------------------------------------------------------------ main

def main():
    inv = C.load_inventory()
    rows = inv["icons"]
    errs, notes = [], []
    ids = [r["id"] for r in rows]
    counts = {k: sum(1 for r in rows if r["sheet"] == k) for k in C.SHEETS}
    expect = {"01": 24, "02": 24, "03": 24, "04": 25, "05": 25}
    if len(ids) != 122 or len(set(ids)) != 122:
        errs.append(f"inventory has {len(ids)} rows, {len(set(ids))} unique IDs; expected 122")
    if counts != expect:
        errs.append(f"sheet counts {counts}, expected {expect}")
    cat = [e["id"] for e in C.parse_catalog()]
    if cat != ids:
        errs.append("inventory order differs from the catalogue")
    # stray files in the export folders
    for ed in C.EDITIONS:
        for folder, kind, size in [(ed, "svg", None), (f"png-256/{ed}", "png", 256), (f"png-512/{ed}", "png", 512)]:
            want = {os.path.basename(C.edition_file(r, ed, kind, size)) for r in rows}
            d = os.path.join(C.ASSETS, folder)
            have = set(os.listdir(d)) if os.path.isdir(d) else set()
            for x in sorted(have - want):
                errs.append(f"{folder}/{x}: not an inventory export name")
    for sh in C.TILE_SHAPES:
        for tl in C.TILE_COLOURS:
            for sub, ext in (("svg", ".svg"), ("png-256", ".png"), ("png-512", ".png")):
                want = {C.tile_name(r["id"], r["slug"], sh, tl, md) + ext for r in rows for md in C.TILE_MODES}
                d = os.path.join(C.ASSETS, "tiles", f"{sh}-{tl}", sub)
                have = set(os.listdir(d)) if os.path.isdir(d) else set()
                for x in sorted(have - want):
                    errs.append(f"tiles/{sh}-{tl}/{sub}/{x}: not an inventory tile name")
    per = []
    n_svg = n_png = n_tile_svg = n_tile_png = 0
    derived_ok = trees_ok = tree_elements = tree_swaps = tiles_ok = 0
    margins = {sh: {} for sh in C.TILE_SHAPES}
    for r in rows:
        i = r["id"]
        has_src = os.path.exists(os.path.join(C.SRC, f"{i}.svg"))
        st = C.read_json(os.path.join(C.QA, "status", f"{i}.json")) or {}
        state = st.get("state", "todo") if has_src else "todo"
        e0 = len(errs)
        paths = {ed: C.edition_file(r, ed) for ed in C.EDITIONS}
        pngs = [(C.edition_file(r, ed, "png", px), px) for ed in C.EDITIONS for px in (256, 512)]
        if has_src:
            missing = [p for p in paths.values() if not os.path.exists(p)]
            for p in missing:
                errs.append(f"{i}: source exists but {os.path.relpath(p, C.ASSETS)} is missing; run build_icon.py {i}")
            if not missing:
                n_svg += 4
                for ed, p in paths.items():
                    check_svg(p, ed, errs)
                rb_text = open(paths["red-black"], encoding="utf-8").read()
                want = S.derive_editions(rb_text)
                if all(open(paths[ed], encoding="utf-8").read() == want[ed] for ed in C.EDITIONS):
                    derived_ok += 1
                else:
                    errs.append(f"{i}: an edition file is not the red-black file with its ink colors swapped")
                for ed in ("black", "red-newsprint", "newsprint"):
                    ok, n_el, n_sw, why = tree_identity(paths["red-black"], paths[ed], ed)
                    if not ok:
                        errs.append(f"{i}: {ed} tree differs from red-black: {why}")
                    else:
                        tree_elements += n_el
                        tree_swaps += n_sw
                if not any(e.startswith(f"{i}: ") and "tree differs" in e for e in errs[e0:]):
                    trees_ok += 1
                # tiles
                bare_trees = {}
                for ed, p in paths.items():
                    root = ET.parse(p).getroot()
                    bare_trees[ed] = [k for k in root if strip(k.tag) not in ("title", "desc")]
                for sh in C.TILE_SHAPES:
                    margins[sh][i] = round(T.icon_margin(rb_text, sh, C.TILE_FACTORS[sh]), 3)
                    if margins[sh][i] < C.TILE_SAFE_MARGIN:
                        errs.append(f"{i}: ink comes within {margins[sh][i]:.2f} units of the {sh} tile edge (safe margin {C.TILE_SAFE_MARGIN})")
                    for tl in C.TILE_COLOURS:
                        for md in C.TILE_MODES:
                            tp = C.tile_file(r, sh, tl, md)
                            if not os.path.exists(tp):
                                errs.append(f"{i}: {os.path.relpath(tp, C.ASSETS)} is missing; run build_tiles.py")
                                continue
                            n_tile_svg += 1
                            if check_tile(tp, r, sh, tl, md, bare_trees[C.TILE_EDITION[(tl, md)]], errs):
                                tiles_ok += 1
                            for px in (256, 512):
                                pp = C.tile_file(r, sh, tl, md, "png", px)
                                if not os.path.exists(pp):
                                    errs.append(f"{i}: {os.path.relpath(pp, C.ASSETS)} is missing")
                                    continue
                                n_tile_png += 1
                                check_png(pp, px, errs, opaque_corners=(sh == "square"), centre_opaque=True)
            for p, px in pngs:
                if not os.path.exists(p):
                    errs.append(f"{i}: {os.path.relpath(p, C.ASSETS)} is missing")
                else:
                    n_png += 1
                    check_png(p, px, errs)
            if not st:
                errs.append(f"{i}: source exists but qa/status/{i}.json is missing; run build_icon.py {i}")
        else:
            for p in list(paths.values()) + [q for q, _ in pngs]:
                if os.path.exists(p):
                    errs.append(f"{i}: {os.path.relpath(p, C.ASSETS)} exists without a source")
        mj = C.read_json(os.path.join(C.QA, "metrics", f"{i}.json")) if has_src else None
        lm = {}
        if mj:  # qa/metrics is refreshed by every build, including build_all
            ed = mj.get("edge_distance_px") or {}
            lm = {"silhouette_iou_1x": mj["silhouette_iou_1x"], "red_iou_1x": mj["red_iou_1x"],
                  "edge_mean_px": (ed.get("symmetric") or {}).get("mean"), "edge_p95_px": (ed.get("symmetric") or {}).get("p95"),
                  "bake_4x": mj.get("bake_check_iou_4x")}
        per.append({"id": i, "label": r["label"], "sheet": r["sheet"], "row": r["row"], "column": r["column"],
                    "state": state, "tracer": st.get("tracer") if has_src else None,
                    "iterations": st.get("iterations", 0) if has_src else 0,
                    "silhouette_iou": lm.get("silhouette_iou_1x"), "red_iou": lm.get("red_iou_1x"),
                    "edge_mean": lm.get("edge_mean_px"), "edge_p95": lm.get("edge_p95_px"),
                    "corrections": len(st.get("corrections", [])) if has_src else 0,
                    "last_build": st.get("last_build") if has_src else None, "errors": len(errs) - e0})
    states = {s: sum(1 for p in per if p["state"] == s) for s in ("todo", "traced", "reviewed", "fixed")}
    complete = states["todo"] == 0
    # reference crops
    want_refs = {r["reference_crops"][k] for r in rows for k in ("black", "red")}
    have_refs = set(os.listdir(os.path.join(C.ASSETS, "reference-crops")))
    n_refs = len(want_refs & have_refs)
    if n_refs != 244 or len(want_refs) != 244:
        errs.append(f"reference crops: {n_refs} of 244 present")
    for x in sorted(have_refs - want_refs):
        errs.append(f"reference-crops/{x}: not an inventory reference name")
    # sheets
    cs_dir = os.path.join(C.ASSETS, "contact-sheets")
    dark = [f"{C.DATE}_Oath-And-Action-Civic-Line-{k}-{v}-{ed}" for k, v in SHEET_SLUGS.items() for ed in ("Red-Black", "Black")]
    light = [f"{C.DATE}_Oath-And-Action-Civic-Line-{k}-{v}-{ed}" for k, v in SHEET_SLUGS.items() for ed in ("Red-Newsprint", "Newsprint")]
    tsh = {"square": "Square", "rounded": "Rounded", "circle": "Circle"}
    tile_sheets = [f"{C.DATE}_Oath-And-Action-Civic-Line-Tiles-{tsh[sh]}-{tl.capitalize()}-{md.title().replace(' ', '-')}"
                   for sh in C.TILE_SHAPES for tl in C.TILE_COLOURS for md in C.TILE_MODES]
    have_cs = set(f for f in os.listdir(cs_dir) if os.path.isfile(os.path.join(cs_dir, f))) if os.path.isdir(cs_dir) else set()
    have_ts = set(os.listdir(os.path.join(cs_dir, "tiles"))) if os.path.isdir(os.path.join(cs_dir, "tiles")) else set()
    exts = (".svg", ".png", "-2x.png")
    done = {"dark": [n for n in dark if all(n + x in have_cs for x in exts)],
            "light": [n for n in light if all(n + x in have_cs for x in exts)],
            "tiles": [n for n in tile_sheets if all(n + x in have_ts for x in exts)]}
    for kind, want_n in (("dark", 10), ("light", 10), ("tiles", 12)):
        if len(done[kind]) != want_n:
            (errs if complete else notes).append(f"{kind} sheets: {len(done[kind])} of {want_n} complete (SVG, PNG and 2x PNG)")
    for x in sorted(have_cs - {n + e for n in dark + light for e in exts}):
        errs.append(f"contact-sheets/{x}: unexpected file")
    for x in sorted(have_ts - {n + e for n in tile_sheets for e in exts}):
        errs.append(f"contact-sheets/tiles/{x}: unexpected file")
    expect_counts = {"svgs": 488, "pngs": 976, "tile_svgs": 1464, "tile_pngs": 2928}
    got_counts = {"svgs": n_svg, "pngs": n_png, "tile_svgs": n_tile_svg, "tile_pngs": n_tile_png}
    if complete:
        for k, v in expect_counts.items():
            if got_counts[k] != v:
                errs.append(f"{got_counts[k]} {k.replace('_', ' ')}, expected {v}")
    else:
        notes.append(f"set incomplete: {states['todo']} icons todo")
    margin_summary = {sh: {"factor": C.TILE_FACTORS[sh], "min_margin": min(m.values()) if m else None,
                           "min_margin_id": min(m, key=m.get) if m else None} for sh, m in margins.items()}
    contrast = contrast_table()
    report = {"checked": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
              "ids": len(ids), "counts_by_sheet": counts, "order_matches_catalog": cat == ids,
              "svgs": n_svg, "pngs": n_png, "tile_svgs": n_tile_svg, "tile_pngs": n_tile_png,
              "editions_derived_by_swap": derived_ok, "edition_trees_identical": trees_ok,
              "edition_tree_elements_compared": tree_elements, "edition_tree_colour_swaps": tree_swaps,
              "tiles_matching_bare_geometry": tiles_ok, "tile_margins": margin_summary,
              "reference_crops": n_refs, "contact_sheets_dark": len(done["dark"]), "contact_sheets_light": len(done["light"]),
              "tile_sheets": len(done["tiles"]), "contrast": contrast, "states": states,
              "complete": complete, "errors": errs, "notes": notes, "icons": per}
    C.write_json(REPORT, report)
    write_ledger(report)
    if "--sync-inventory" in sys.argv:
        from crop_references import write_csv
        by = {p["id"]: p["state"] for p in per}
        for r in rows:
            r["status"] = by[r["id"]]
        C.write_json(C.INVENTORY_JSON, inv)
        write_csv(rows)
        print("inventory status synced from qa/status")
    print(f"IDs {len(ids)} ({counts}); bare SVGs {n_svg}/488, PNGs {n_png}/976; tile SVGs {n_tile_svg}/1464, PNGs {n_tile_png}/2928; "
          f"reference crops {n_refs}/244; sheets dark {len(done['dark'])}/10, light {len(done['light'])}/10, tiles {len(done['tiles'])}/12")
    print(f"editions derived by swap {derived_ok}; edition trees identical {trees_ok} ({tree_elements} elements, {tree_swaps} color swaps); "
          f"tiles matching bare geometry {tiles_ok}; states {states}")
    for sh, v in margin_summary.items():
        print(f"  {sh} tile, factor {v['factor']:g}: smallest margin {v['min_margin']:.2f} units ({v['min_margin_id']})")
    for c in contrast:
        print(f"  contrast {c['ink']} on {c['ground']}: {c['ratio']:.2f}:1{'' if c['meets_3_to_1'] else '  (under 3:1)'}")
    for n in notes:
        print("note:", n)
    for e in errs[:60]:
        print("ERROR:", e)
    print(f"{len(errs)} error(s). Ledger: {os.path.relpath(LEDGER, C.ROOT)}")
    sys.exit(1 if errs else 0)


def fmtv(v, nd=3):
    return "" if v is None else f"{v:.{nd}f}"


def write_ledger(rep):
    s = rep["states"]
    L = ["# Civic Line completion ledger", "",
         f"Compiled by `verify_set.py` from the per-icon status files on {rep['checked']}. Rerun it to refresh; do not edit by hand.", "",
         f"Done: {s['traced'] + s['reviewed'] + s['fixed']} of 122 traced ({s['traced']} traced, {s['reviewed']} reviewed, {s['fixed']} fixed). To do: {s['todo']}.",
         f"Bare exports: {rep['svgs']} of 488 SVGs and {rep['pngs']} of 976 PNGs in four editions. Tiles: {rep['tile_svgs']} of 1,464 SVGs and {rep['tile_pngs']} of 2,928 PNGs.",
         f"Reference crops: {rep['reference_crops']} of 244. Sheets: {rep['contact_sheets_dark']} of 10 dark, {rep['contact_sheets_light']} of 10 light, {rep['tile_sheets']} of 12 tile sheets.",
         f"Editions derived from red-black by ink swap: {rep['editions_derived_by_swap']}. Parsed trees identical apart from ink color: {rep['edition_trees_identical']} "
         f"({rep['edition_tree_elements_compared']} elements, {rep['edition_tree_colour_swaps']} color swaps). Tiles whose icon geometry matches its bare export: {rep['tiles_matching_bare_geometry']}.",
         "Smallest ink-to-edge margins: " + "; ".join(f"{sh} {v['min_margin']:.2f} units ({v['min_margin_id']})" for sh, v in rep["tile_margins"].items()) + ".",
         f"Verification errors: {len(rep['errors'])}.", ""]
    if rep["errors"]:
        L += ["## Errors", ""] + [f"- {e}" for e in rep["errors"]] + [""]
    todo = [p["id"] for p in rep["icons"] if p["state"] == "todo"]
    L += ["## Remaining IDs", "", ", ".join(todo) if todo else "None.", "",
          "## All icons", "",
          "| ID | Label | Sheet | Row | Col | State | Tracer | Iter. | Silhouette IoU | Red IoU | Edge mean (px) | Edge p95 (px) | Corrections |",
          "|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|"]
    for p in rep["icons"]:
        L.append(f"| {p['id']} | {p['label']} | {p['sheet']} | {p['row']} | {p['column']} | {p['state']} | {p['tracer'] or ''} | "
                 f"{p['iterations']} | {fmtv(p['silhouette_iou'])} | {fmtv(p['red_iou'])} | {fmtv(p['edge_mean'], 2)} | "
                 f"{fmtv(p['edge_p95'], 2)} | {p['corrections']} |")
    L.append("")
    with open(LEDGER, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    main()
