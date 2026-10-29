"""Step 1: find every cell on the ten Civic Line sheets, crop each pictogram,
register the red sheet to the black sheet, write masks, untouched reference
crops, enlarged tracer views, the 122-row inventory and the crop check image.

Run with:  python3 -I crop_references.py
Reads the reference PNGs only. It never writes into the reference folder.
"""
import csv
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

MASKS = os.path.join(C.QA, "masks")
ZOOM = os.path.join(C.QA, "ref-zoom")
REFC = os.path.join(C.ASSETS, "reference-crops")
REG_RANGE = 14         # px searched in each direction when registering red to black
MIN_AREA = 3           # components smaller than this are treated as specks
TEXT_MAX_H = 24        # caption glyph height limit
TEXT_MAX_W = 40
EIGHT = np.ones((3, 3), bool)


# ------------------------------------------------------------- sheet analysis

class Sheet:
    def __init__(self, key, kind):
        self.key = key
        self.kind = kind
        self.file = C.SHEETS[key][kind]
        self.path = os.path.join(C.REF_DIR, self.file)
        self.img = Image.open(self.path)
        self.rgb = np.asarray(self.img.convert("RGB"))
        self.H, self.W = self.rgb.shape[:2]
        g = C.green(self.rgb)
        self.full_ink_g = float(np.median(g[g < 60]))
        self.bg_g = float(np.median(g[g > 180]))
        rd = C.redness(self.rgb)
        strong = rd > 120
        self.full_red = float(np.median(rd[strong])) if strong.sum() > 100 else None
        self.thr = (self.bg_g + self.full_ink_g) / 2.0
        self.ink = g < self.thr
        self.lenient = g < (self.bg_g - 25.0)
        self.lab, self.n = ndi.label(self.ink, structure=EIGHT)
        self.objs = ndi.find_objects(self.lab)
        self.areas = ndi.sum(np.ones_like(self.lab), self.lab, index=np.arange(1, self.n + 1))
        self.len_lab, _ = ndi.label(self.lenient, structure=EIGHT)

    def boxes(self):
        out = []
        for i, sl in enumerate(self.objs):
            if sl is None:
                continue
            y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
            out.append({"lab": i + 1, "y0": y0, "y1": y1, "x0": x0, "x1": x1,
                        "h": y1 - y0, "w": x1 - x0, "area": int(self.areas[i]),
                        "cy": (y0 + y1) / 2.0, "cx": (x0 + x1) / 2.0})
        return out


def find_rule(sh):
    rows = sh.ink[:150].sum(1)
    ys = [y for y in range(150) if rows[y] > 0.55 * sh.W]
    if not ys:
        raise SystemExit(f"{sh.file}: header rule not found")
    return max(ys)


def caption_lines(sh, boxes, content_top, n_rows):
    """Caption baselines: y bands where small glyph-sized components line up
    across the full sheet width."""
    small = [b for b in boxes if b["h"] <= TEXT_MAX_H and b["w"] <= TEXT_MAX_W and b["y0"] > content_top]
    cy = np.array([b["cy"] for b in small])
    cx = np.array([b["cx"] for b in small])
    hist = np.bincount((cy // 2).astype(int), minlength=sh.H // 2 + 2)
    win = np.convolve(hist, np.ones(9, int), "same")
    peaks = []
    for i in range(len(win)):
        lo, hi = max(0, i - 10), i + 11
        if win[i] >= 12 and win[i] == win[lo:hi].max():
            yc = i * 2 + 1
            sel = np.abs(cy - yc) < 10
            cov = len(set((cx[sel] // 128).astype(int)))
            if cov >= 8 and (not peaks or yc - peaks[-1] > 20):
                peaks.append(yc)
    if len(peaks) != n_rows:
        raise SystemExit(f"{sh.file}: expected {n_rows} caption lines, found {peaks}")
    return peaks


def group_by_gaps(items, key0, key1, gap):
    items = sorted(items, key=lambda b: b[key0])
    groups = []
    for b in items:
        if groups and b[key0] - max(x[key1] for x in groups[-1]) <= gap:
            groups[-1].append(b)
        else:
            groups.append([b])
    return groups


def analyse_sheet(key):
    spec = C.SHEETS[key]
    sh = Sheet(key, "black")
    boxes = [b for b in sh.boxes() if b["area"] >= MIN_AREA]
    specks = [b for b in sh.boxes() if b["area"] < MIN_AREA]
    rule_y = find_rule(sh)
    content_top = rule_y + 3
    caps = caption_lines(sh, boxes, content_top, spec["rows"])
    text_labels = set()
    rows = []
    for r, yc in enumerate(caps):
        cap = [b for b in boxes if abs(b["cy"] - yc) <= 12 and b["h"] <= TEXT_MAX_H and b["w"] <= TEXT_MAX_W * 2]
        groups = group_by_gaps(cap, "x0", "x1", 30)
        if len(groups) != spec["cols"]:
            raise SystemExit(f"{sh.file} row {r + 1}: {len(groups)} caption groups, expected {spec['cols']}")
        row = {"caption_center": yc, "cells": []}
        for g in groups:
            for b in g:
                text_labels.add(b["lab"])
            cell = {"cap_x0": min(b["x0"] for b in g), "cap_x1": max(b["x1"] for b in g),
                    "cap_y0": min(b["y0"] for b in g), "cap_y1": max(b["y1"] for b in g),
                    "cap_glyphs": len(g),
                    "cap_glyph_boxes": [(b["x0"], b["y0"], b["x1"], b["y1"]) for b in sorted(g, key=lambda b: b["x0"])]}
            cell["cap_cx"] = (cell["cap_x0"] + cell["cap_x1"]) / 2.0
            row["cells"].append(cell)
        rows.append(row)
    col_centers = [float(np.median([rows[r]["cells"][c]["cap_cx"] for r in range(spec["rows"])]))
                   for c in range(spec["cols"])]
    bounds = [0] + [int(round((col_centers[i] + col_centers[i + 1]) / 2.0)) for i in range(spec["cols"] - 1)] + [sh.W]
    # Reform ID lines sit just above each caption, in a smaller face.
    for r, row in enumerate(rows):
        for c, cell in enumerate(row["cells"]):
            cell["id_y0"] = cell["id_y1"] = None
            if not spec["reform"]:
                continue
            cand = [b for b in boxes if b["lab"] not in text_labels and b["h"] <= 16 and b["w"] <= 20
                    and cell["cap_y0"] - 30 <= b["cy"] <= cell["cap_y0"] - 2
                    and abs(b["cx"] - cell["cap_cx"]) <= 40]
            if not cand:
                raise SystemExit(f"{sh.file} row {r + 1} col {c + 1}: reform ID line not found")
            med = float(np.median([b["cy"] for b in cand]))
            ids = [b for b in cand if abs(b["cy"] - med) <= 5]
            for b in ids:
                text_labels.add(b["lab"])
            cell["id_y0"] = min(b["y0"] for b in ids)
            cell["id_y1"] = max(b["y1"] for b in ids)
            cell["id_x0"] = min(b["x0"] for b in ids)
            cell["id_x1"] = max(b["x1"] for b in ids)
            cell["id_glyphs"] = len(ids)
            cell["id_glyph_boxes"] = [(b["x0"], b["y0"], b["x1"], b["y1"]) for b in sorted(ids, key=lambda b: b["x0"])]
    footer = [b for b in boxes if b["y0"] > rows[-1]["cells"][0]["cap_y1"] + 4 and b["lab"] not in text_labels]
    for b in footer:
        text_labels.add(b["lab"])
    footer_y0 = min((b["y0"] for b in footer), default=sh.H)
    # header: everything above the content top is header ink
    header_labels = {b["lab"] for b in boxes if b["y1"] <= content_top + 1}
    return {"sheet": sh, "boxes": boxes, "specks": specks, "rule_y": rule_y, "content_top": content_top,
            "rows": rows, "col_centers": col_centers, "bounds": bounds, "text_labels": text_labels,
            "header_labels": header_labels, "footer_y0": footer_y0}


# ------------------------------------------------------------- crops

def cell_components(A, r, c):
    sh = A["sheet"]
    row = A["rows"][r]
    cell = row["cells"][c]
    x_lo, x_hi = A["bounds"][c], A["bounds"][c + 1]
    if r == 0:
        y_lo = A["content_top"]
    else:
        y_lo = max(cc["cap_y1"] for cc in A["rows"][r - 1]["cells"]) + 1
    y_text = cell["id_y0"] if cell["id_y0"] is not None else cell["cap_y0"]
    own = []
    crossing = []
    for b in A["boxes"]:
        if b["lab"] in A["text_labels"] or b["lab"] in A["header_labels"]:
            continue
        if x_lo <= b["cx"] < x_hi and y_lo <= b["cy"] < y_text:
            own.append(b)
            if b["x0"] < x_lo or b["x1"] > x_hi:
                crossing.append(b["lab"])
    return own, {"x_lo": x_lo, "x_hi": x_hi, "y_lo": y_lo, "y_text": y_text}, crossing


def foreign_ink(sh, boxes, own_labels, own_mask):
    """Lenient-threshold ink that belongs to something other than this pictogram:
    any lenient component holding a strict component (area >= MIN_AREA) that is
    not one of this pictogram's own. Faint specks with no strict core are neutral."""
    other = [b["lab"] for b in boxes if b["lab"] not in own_labels]
    other_mask = np.isin(sh.lab, other)
    foreign_len = set(np.unique(sh.len_lab[other_mask])) - {0}
    m = np.isin(sh.len_lab, list(foreign_len))
    return m & ~ndi.binary_dilation(own_mask, iterations=1)


def clamp_rect(rect, bbox, foreign):
    """Shrink margin sides until the rectangle holds no foreign ink.
    rect and bbox are [x0, y0, x1, y1) in sheet px. Returns rect and notes."""
    x0, y0, x1, y1 = rect
    bx0, by0, bx1, by1 = bbox
    notes = []
    for _ in range(400):
        sub = foreign[y0:y1, x0:x1]
        if not sub.any():
            break
        fy, fx = np.nonzero(sub)
        fy = fy + y0
        fx = fx + x0
        best = None
        inside = 0
        for yy, xx in zip(fy, fx):
            opts = []
            if yy >= by1:
                opts.append(("y1", yy, (y1 - yy) * (x1 - x0)))
            if yy < by0:
                opts.append(("y0", yy + 1, (yy + 1 - y0) * (x1 - x0)))
            if xx >= bx1:
                opts.append(("x1", xx, (x1 - xx) * (y1 - y0)))
            if xx < bx0:
                opts.append(("x0", xx + 1, (xx + 1 - x0) * (y1 - y0)))
            if not opts:
                inside += 1
                continue
            o = min(opts, key=lambda t: t[2])
            if best is None or o[2] > best[2]:
                best = o  # take the cut that the worst pixel needs
        if best is None:
            notes.append(f"{inside} foreign ink px inside the pictogram box")
            break
        side, val, _ = best
        if side == "y1":
            y1 = val
        elif side == "y0":
            y0 = val
        elif side == "x1":
            x1 = val
        else:
            x0 = val
    return [x0, y0, x1, y1], notes


def register(black_mask, red_sheet, rect, rng=REG_RANGE):
    x0, y0, x1, y1 = rect
    best = None
    H, W = red_sheet.ink.shape
    for dy in range(-rng, rng + 1):
        for dx in range(-rng, rng + 1):
            if y0 + dy < 0 or x0 + dx < 0 or y1 + dy > H or x1 + dx > W:
                continue
            m = red_sheet.ink[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
            inter = np.logical_and(m, black_mask).sum()
            uni = np.logical_or(m, black_mask).sum()
            iou = inter / uni if uni else 0.0
            if best is None or iou > best[0]:
                best = (iou, dx, dy)
    return best


def iou(a, b):
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 1.0


def scale_probe(black_crop_mask, red_rgb_full, rect, dx, dy, thr_g):
    """Diagnostic only, run for icons below 0.90: can a fractional shift or a
    small uniform scale about the crop center beat integer translation?
    Returns (best_iou, scale, fdx, fdy) with fractional offsets in px."""
    x0, y0, x1, y1 = rect
    h, w = y1 - y0, x1 - x0
    g = red_rgb_full[..., 1].astype(np.float64)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    best = (0.0, 1.0, float(dx), float(dy))
    for s in [0.98, 0.99, 1.0, 1.01, 1.02]:
        for fdy in np.arange(-1.0, 1.01, 0.25):
            for fdx in np.arange(-1.0, 1.01, 0.25):
                sy = (yy - cy) / s + cy + y0 + dy + fdy
                sx = (xx - cx) / s + cx + x0 + dx + fdx
                v = ndi.map_coordinates(g, [sy, sx], order=1, mode="nearest")
                v = iou(v < thr_g, black_crop_mask)
                if v > best[0]:
                    best = (v, s, float(dx + fdx), float(dy + fdy))
    return best


# ------------------------------------------------------------- images

def ref_zoom(black_rgb, red_rgb, path, icon_id, label):
    z = 4
    h, w = black_rgb.shape[:2]
    pad_l, pad_t, gap = 34, 44, 24
    W = pad_l + w * z + gap + pad_l + w * z + 12
    H = pad_t + h * z + 16
    out = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(out)
    f = C.font(11)
    ft = C.font(14, bold=True)
    d.text((pad_l, 6), f"{icon_id} {label}  |  black sheet (left), red sheet (right)  |  4x nearest, grid every 10 crop px",
           fill=(0, 0, 0), font=ft)
    for k, arr in enumerate([black_rgb, red_rgb]):
        ox = pad_l + k * (w * z + gap + pad_l)
        oy = pad_t
        big = Image.fromarray(arr).resize((w * z, h * z), Image.NEAREST)
        out.paste(big, (ox, oy))
        ov = Image.new("RGBA", big.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        for x in range(0, w + 1, 10):
            a = 150 if x % 50 == 0 else 80
            od.line([(x * z, 0), (x * z, h * z)], fill=(0, 140, 255, a), width=1)
        for y in range(0, h + 1, 10):
            a = 150 if y % 50 == 0 else 80
            od.line([(0, y * z), (w * z, y * z)], fill=(0, 140, 255, a), width=1)
        region = out.crop((ox, oy, ox + w * z, oy + h * z)).convert("RGBA")
        out.paste(Image.alpha_composite(region, ov).convert("RGB"), (ox, oy))
        for x in range(0, w + 1, 10):
            d.text((ox + x * z - 6, oy - 14), str(x), fill=(0, 90, 170), font=f)
        for y in range(0, h + 1, 10):
            d.text((ox - 30, oy + y * z - 6), str(y), fill=(0, 90, 170), font=f)
    out.save(path)


def crop_check(rows, sheets, path):
    """All 122 crops with 14 px of washed-out context and the crop edge drawn."""
    ctx = 14
    tiles = []
    for r in rows:
        sh = sheets[r["sheet"]]["black"]
        x0, y0, x1, y1 = r["crop"]["x0"], r["crop"]["y0"], r["crop"]["x1"], r["crop"]["y1"]
        X0, Y0 = max(0, x0 - ctx), max(0, y0 - ctx)
        X1, Y1 = min(sh.W, x1 + ctx), min(sh.H, y1 + ctx)
        arr = sh.rgb[Y0:Y1, X0:X1].astype(np.float64)
        wash = arr * 0.35 + 255 * 0.65
        inside = np.zeros(arr.shape[:2], bool)
        inside[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = True
        arr[~inside] = wash[~inside]
        im = Image.fromarray(arr.astype(np.uint8))
        d = ImageDraw.Draw(im)
        d.rectangle([x0 - X0 - 1, y0 - Y0 - 1, x1 - X0, y1 - Y0], outline=(0, 120, 255))
        tiles.append((r["id"], im))
    cols = 8
    cw = max(t[1].width for t in tiles) + 10
    chh = max(t[1].height for t in tiles) + 26
    nrows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGB", (cols * cw + 10, nrows * chh + 40), (255, 255, 255))
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Civic Line crop check: crop edge in blue, 14 px of washed context outside it", fill=(0, 0, 0), font=C.font(18, True))
    f = C.font(14, True)
    for i, (iid, im) in enumerate(tiles):
        gx, gy = 10 + (i % cols) * cw, 40 + (i // cols) * chh
        d.text((gx, gy), iid, fill=(200, 0, 40), font=f)
        out.paste(im, (gx, gy + 20))
    out.save(path)


# ------------------------------------------------------------- main

def main():
    for p in [MASKS, ZOOM, REFC]:
        os.makedirs(p, exist_ok=True)
    catalog = C.parse_catalog()
    cat_by_pos = {(e["sheet"], e["row"], e["column"]): e for e in catalog}
    sheets = {}
    analyses = {}
    report = {"sheets": {}, "flags": []}
    for key in C.SHEETS:
        A = analyse_sheet(key)
        analyses[key] = A
        red = Sheet(key, "red")
        sheets[key] = {"black": A["sheet"], "red": red}
        report["sheets"][key] = {
            "black": A["sheet"].file, "red": red.file, "rule_y": A["rule_y"],
            "caption_centers": [row["caption_center"] for row in A["rows"]],
            "column_centers": [round(c, 1) for c in A["col_centers"]], "column_bounds": A["bounds"],
            "full_ink_g_black": A["sheet"].full_ink_g, "full_ink_g_red": red.full_ink_g,
            "full_red": red.full_red, "specks_ignored": len(A["specks"]),
            "caption_glyph_counts": [[c["cap_glyphs"] for c in row["cells"]] for row in A["rows"]],
        }
    rows_out = []
    for key in C.SHEETS:
        A = analyses[key]
        sh = sheets[key]["black"]
        red = sheets[key]["red"]
        spec = C.SHEETS[key]
        # foreign ink map in the black sheet = lenient ink of every text, header and footer component
        for r in range(spec["rows"]):
            for c in range(spec["cols"]):
                e = cat_by_pos[(key, r + 1, c + 1)]
                own, cellgeo, crossing = cell_components(A, r, c)
                if not own:
                    raise SystemExit(f"{e['id']}: no pictogram ink in cell")
                own_labels = {b["lab"] for b in own}
                own_mask = np.isin(sh.lab, list(own_labels))
                ys, xs = np.nonzero(own_mask)
                bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
                rect = [max(0, bbox[0] - C.CROP_MARGIN), max(0, bbox[1] - C.CROP_MARGIN),
                        min(sh.W, bbox[2] + C.CROP_MARGIN), min(sh.H, bbox[3] + C.CROP_MARGIN)]
                foreign = foreign_ink(sh, A["boxes"], own_labels, own_mask)
                rect, notes = clamp_rect(rect, bbox, foreign)
                x0, y0, x1, y1 = rect
                bmask = sh.ink[y0:y1, x0:x1] & own_mask[y0:y1, x0:x1]
                full_bmask_rect = sh.ink[y0:y1, x0:x1]
                reg_iou, dx, dy = register(full_bmask_rect, red, rect)
                # Red-sheet check: red lenient components that touch the black sheet's
                # foreign ink (captions, IDs, neighbors; grown by 3 px and shifted by
                # the registration) are the red sheet's own captions and neighbors.
                def red_foreign_map(dx, dy):
                    fb = ndi.binary_dilation(foreign, iterations=3)
                    fb = np.roll(np.roll(fb, dy, axis=0), dx, axis=1)
                    labs = set(np.unique(red.len_lab[fb & (red.len_lab > 0)])) - {0}
                    m = np.isin(red.len_lab, list(labs))
                    m &= ~np.roll(np.roll(ndi.binary_dilation(own_mask, iterations=1), dy, axis=0), dx, axis=1)
                    return np.roll(np.roll(m, -dy, axis=0), -dx, axis=1)  # back in black-sheet coordinates
                rf = red_foreign_map(dx, dy)
                if rf[y0:y1, x0:x1].any():
                    rect2, n2 = clamp_rect(rect, bbox, rf | foreign)
                    notes += [f"red sheet clamp: {n}" for n in n2]
                    if rect2 != rect:
                        notes.append(f"rectangle shrunk for red-sheet ink from {rect} to {[int(v) for v in rect2]}")
                        rect = [int(v) for v in rect2]
                        x0, y0, x1, y1 = rect
                        bmask = sh.ink[y0:y1, x0:x1] & own_mask[y0:y1, x0:x1]
                        full_bmask_rect = sh.ink[y0:y1, x0:x1]
                        reg_iou, dx, dy = register(full_bmask_rect, red, rect)
                black_crop = sh.rgb[y0:y1, x0:x1]
                red_crop = red.rgb[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
                bg_b = C.local_background(black_crop)
                bg_r = C.local_background(red_crop)
                ink_b = C.ink_mask(black_crop, bg_b, sh.full_ink_g)
                ink_r = C.ink_mask(red_crop, bg_r, sh.full_ink_g)
                redm = C.red_mask(red_crop, bg_r, red.full_red)
                sheet_iou = iou(ink_b, ink_r)
                foreign_in_crop = int((foreign[y0:y1, x0:x1]).sum())
                red_foreign_in_crop = int(red_foreign_map(dx, dy)[y0:y1, x0:x1].sum())
                ids = e["id"]
                C.save_mask(ink_b, os.path.join(MASKS, f"{ids}-ink.png"))
                C.save_mask(redm, os.path.join(MASKS, f"{ids}-red.png"))
                C.save_mask(ink_r, os.path.join(MASKS, f"{ids}-red-sheet-ink.png"))
                names = C.export_names(ids, e["slug"])
                sh.img.crop((x0, y0, x1, y1)).save(os.path.join(REFC, names["ref_black"]))
                red.img.crop((x0 + dx, y0 + dy, x1 + dx, y1 + dy)).save(os.path.join(REFC, names["ref_red"]))
                ref_zoom(black_crop, red_crop, os.path.join(ZOOM, f"{ids}.png"), ids, e["label"])
                ys, xs = np.nonzero(ink_b)
                ink_box = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
                flags = []
                if sheet_iou < 0.90:
                    flags.append("sheet-iou-below-0.90")
                if crossing:
                    flags.append("component-crosses-column-bound")
                if notes:
                    flags.append("crop-clamp-note")
                if foreign_in_crop:
                    flags.append("foreign-ink-in-crop")
                if red_foreign_in_crop:
                    flags.append("foreign-ink-in-red-crop")
                margins = {"left": bbox[0] - x0, "top": bbox[1] - y0, "right": x1 - bbox[2], "bottom": y1 - bbox[3]}
                row = {
                    "id": ids, "label": e["label"], "slug": e["slug"], "sheet": key,
                    "row": e["row"], "column": e["column"],
                    "sheet_black": sh.file, "sheet_red": red.file,
                    "crop": {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "w": x1 - x0, "h": y1 - y0},
                    "crop_margins": margins,
                    "pictogram_box_sheet": {"x0": bbox[0], "y0": bbox[1], "x1": bbox[2], "y1": bbox[3]},
                    "ink_box_crop": {"x0": ink_box[0], "y0": ink_box[1], "x1": ink_box[2], "y1": ink_box[3]},
                    "components": len(own),
                    "registration": {"dx": dx, "dy": dy, "search_iou": round(float(reg_iou), 4)},
                    "red_crop": {"x0": x0 + dx, "y0": y0 + dy, "x1": x1 + dx, "y1": y1 + dy},
                    "sheet_iou": round(sheet_iou, 4),
                    "mask_params": {
                        "bg_black_rgb": [round(float(v), 1) for v in bg_b],
                        "bg_red_rgb": [round(float(v), 1) for v in bg_r],
                        "full_ink_g": sh.full_ink_g, "full_red": red.full_red,
                        "ink_threshold_g": round(C.ink_threshold(bg_b, sh.full_ink_g), 2),
                        "red_threshold": round(C.red_threshold(bg_r, red.full_red), 2),
                        "ink_px": int(ink_b.sum()), "red_px": int(redm.sum()),
                    },
                    "construction": e["construction"], "red_text": e["red"],
                    "exports": {
                        "svg_red_black": names["svg_red_black"], "svg_black": names["svg_black"],
                        "png_red_black": names["png_red_black"], "png_black": names["png_black"],
                        "paths": [f"red-black/{names['svg_red_black']}", f"black/{names['svg_black']}",
                                  f"png-256/red-black/{names['png_red_black']}", f"png-256/black/{names['png_black']}",
                                  f"png-512/red-black/{names['png_red_black']}", f"png-512/black/{names['png_black']}"],
                    },
                    "reference_crops": {"black": names["ref_black"], "red": names["ref_red"]},
                    "status": "todo",
                    "flags": flags, "crop_notes": notes,
                }
                if sheet_iou < 0.90:
                    probe = scale_probe(ink_b, red.rgb, rect, dx, dy, C.ink_threshold(bg_r, sh.full_ink_g))
                    row["registration"]["scale_probe"] = {"iou": round(probe[0], 4), "scale": probe[1],
                                                          "dx": probe[2], "dy": probe[3]}
                rows_out.append(row)
                if flags:
                    report["flags"].append({"id": ids, "flags": flags, "notes": notes, "sheet_iou": row["sheet_iou"],
                                            "crossing": crossing})
    # Independent check that each catalog label sits in its cell: the caption's
    # glyph components should number one per character (two for i and j), less
    # one or two where neighboring glyphs touch.
    cap_bad = []
    for r in rows_out:
        got = report["sheets"][r["sheet"]]["caption_glyph_counts"][r["row"] - 1][r["column"] - 1]
        exp = sum(2 if ch in "ij" else 1 for ch in r["label"] if ch != " ")
        r["caption_check"] = {"glyph_components": got, "expected_from_label": exp}
        if not (exp - 2 <= got <= exp):
            cap_bad.append(r["id"])
    report["caption_check"] = {
        "rule": "detected caption glyph components vs one per label character (two for i and j); touching glyphs may merge",
        "exact": sum(1 for r in rows_out if r["caption_check"]["glyph_components"] == r["caption_check"]["expected_from_label"]),
        "one_short": sum(1 for r in rows_out if r["caption_check"]["glyph_components"] == r["caption_check"]["expected_from_label"] - 1),
        "mismatch": cap_bad,
    }
    # order and counts
    counts = {k: sum(1 for r in rows_out if r["sheet"] == k) for k in C.SHEETS}
    order_ok = [r["id"] for r in rows_out] == [e["id"] for e in catalog]
    report["counts"] = counts
    report["order_matches_catalog"] = order_ok
    report["total"] = len(rows_out)
    inv = {"title": "Civic Line inventory", "date": C.DATE, "count": len(rows_out), "counts_by_sheet": counts,
           "order_matches_catalog": order_ok,
           "pixel_rules": {
               "ink": "green channel darker than the midpoint between the crop's local background (median of its 3 px outer ring) and full ink (median green of the sheet's core ink, G < 60)",
               "red": "redness R - max(G, B) above the midpoint between the local background redness and full red (median redness of the red sheet's strong red pixels)",
           },
           "icons": rows_out}
    C.write_json(C.INVENTORY_JSON, inv)
    write_csv(rows_out)
    crop_check(rows_out, sheets, os.path.join(C.QA, f"{C.DATE}_Civic-Line-Crop-Check.png"))
    C.write_json(os.path.join(C.QA, f"{C.DATE}_Civic-Line-Crop-Report.json"), report)
    print(json.dumps({"counts": counts, "order_ok": order_ok, "flags": len(report["flags"]),
                      "caption_check": report["caption_check"]}, indent=1))
    for f in report["flags"]:
        print(f)


def write_csv(rows):
    fields = ["id", "label", "slug", "sheet", "row", "column", "sheet_black", "sheet_red",
              "crop_x0", "crop_y0", "crop_x1", "crop_y1", "reg_dx", "reg_dy", "sheet_iou",
              "construction", "red_text", "svg_red_black", "svg_black", "svg_red_newsprint", "svg_newsprint",
              "png_red_black", "png_black", "png_red_newsprint", "png_newsprint",
              "ref_black", "ref_red", "status", "scale_s", "transform", "stroke_units", "stroke_median_px", "tiles",
              "tile_optical_scale", "tile_offset_x", "tile_stroke_units",
              "tile_scale_square", "tile_scale_rounded", "tile_scale_circle",
              "tile_min_px_one_color_square", "tile_min_px_one_color_rounded", "tile_min_px_one_color_circle",
              "tile_min_px_two_color_square", "tile_min_px_two_color_rounded", "tile_min_px_two_color_circle", "flags"]
    with open(C.INVENTORY_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        for r in rows:
            t = r.get("transform") or {}
            w.writerow([r["id"], r["label"], r["slug"], r["sheet"], r["row"], r["column"], r["sheet_black"], r["sheet_red"],
                        r["crop"]["x0"], r["crop"]["y0"], r["crop"]["x1"], r["crop"]["y1"],
                        r["registration"]["dx"], r["registration"]["dy"], r["sheet_iou"],
                        r["construction"], r["red_text"],
                        r["exports"]["svg_red_black"], r["exports"]["svg_black"],
                        r["exports"].get("svg_red_newsprint", ""), r["exports"].get("svg_newsprint", ""),
                        r["exports"]["png_red_black"], r["exports"]["png_black"],
                        r["exports"].get("png_red_newsprint", ""), r["exports"].get("png_newsprint", ""),
                        r["reference_crops"]["black"], r["reference_crops"]["red"], r["status"],
                        t.get("s", ""), t.get("formula", ""), r.get("stroke_units", ""), r.get("stroke_median_px", ""),
                        len(r.get("tiles", [])),
                        r.get("tile_optical_scale", ""), r.get("tile_offset_x", ""), r.get("tile_stroke_units", ""),
                        *[(r.get("tile_scale") or {}).get(sh, "") for sh in ("square", "rounded", "circle")],
                        *[((r.get("tile_min_px") or {}).get(md) or {}).get(sh, "") for md in ("one-color", "two-color")
                          for sh in ("square", "rounded", "circle")],
                        ";".join(r.get("flags", []))])


if __name__ == "__main__":
    main()
