"""Part G: the final Civic Line package, in deliverables/ (DR-07).

    python3 -I make_package.py

Builds deliverables/<date>_Oath-And-Action-Civic-Line-Icons.zip with
everything under one top folder, oath-and-action-civic-line-icons/: the four
bare editions as SVG and PNG, the tiles, the contact and tile sheets, the
reference crops, the catalog page, the inventory, the fidelity and contrast
tables and a readme. If that archive would pass 90 MB (90,000,000 bytes), it writes two instead,
<date>_Oath-And-Action-Civic-Line-Icons-SVG.zip (vectors, catalog and data)
and <date>_Oath-And-Action-Civic-Line-Icons-PNG.zip (rasters and reference
crops), each with the readme and data files and the same top folder, so
unpacking both gives one tree. Entries are sorted and stamped with the package
date. After writing, the script reopens each archive, tests it, counts every
folder and compares each entry's bytes with its source. The earlier _REVIEW
zip in work/build/packages/ is left where it is.
"""
import csv
import hashlib
import os
import statistics
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

DELIV = os.path.join(C.ROOT, "deliverables")
BASE = f"{C.DATE}_Oath-And-Action-Civic-Line-Icons"
TOP = "oath-and-action-civic-line-icons"
README = f"{C.DATE}_Civic-Line-Readme.md"
FIDELITY = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Fidelity-Metrics.csv")
CONTRAST = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Contrast-Table.md")
VERIFY = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Verify-Report.json")
CATALOG = os.path.join(C.ASSETS, f"{C.DATE}_Civic-Line-Icon-Catalog.html")
LIMIT = 90_000_000   # bytes: under 90 MB in decimal and binary units alike
STAMP = (2026, 10, 29, 0, 0, 0)


def readme_text(split):
    sc = C.read_json(C.SCALE_JSON)
    inv = C.load_inventory()
    inv_by = {r["id"]: r for r in inv["icons"]}
    vr = C.read_json(VERIFY) or {}
    rows = list(csv.DictReader(open(FIDELITY, encoding="utf-8")))
    med = lambda k: statistics.median([float(r[k]) for r in rows if r[k]])  # noqa: E731
    lo, hi = inv["stroke_width_units"]
    f = C.TILE_FACTORS
    m = vr.get("tile_margins", {})
    red_np = next((c["ratio"] for c in vr.get("contrast", []) if c["ink_hex"] == C.PILLAR_RED and c["ground_hex"] == C.NEWSPRINT), None)
    red_ch = next((c["ratio"] for c in vr.get("contrast", []) if c["ink_hex"] == C.PILLAR_RED and c["ground_hex"] == C.CHARCOAL), None)
    ok = vr.get("errors") == [] and vr.get("edition_trees_identical") == 122 and vr.get("tiles_matching_bare_geometry") == 1464
    audit = vr.get("id_audit", {})
    check_line = ("A script parsed every file: the four editions of each icon share the same elements and attributes apart from ink color "
                  "and the root of each id, and every tile holds its bare export's geometry under one transform per icon, with its strokes "
                  f"held at the set's heaviest line. No id repeats across the {audit.get('files', 0):,} SVG files." if ok else
                  f"The verification report lists {len(vr.get('errors', []))} problems to fix before release.")
    n48 = len(C.BARE_FLOOR_48_IDS)
    t_lo = min(r["tile_stroke_units"] for r in inv["icons"])
    t_hi = max(r["tile_stroke_units"] for r in inv["icons"])
    offs = [abs(v) * f["rounded"] for v in C.TILE_OFFSET_X.values()]
    shifted = ", ".join(sorted(C.TILE_OFFSET_X)[:-1]) + " and " + sorted(C.TILE_OFFSET_X)[-1]
    at_min = [(r["tile_stroke_units"] * C.TILE_FACTORS[sh] * r["tile_min_px"]["two-color"][sh] / 128, r["id"])
              for r in inv["icons"] for sh in C.TILE_SHAPES]
    full = [v for v, i in at_min if inv_by[i]["tile_stroke_units"] >= C.TILE_STROKE_CAP - 1e-4]
    thin = min(at_min)
    mins = {k: C.tile_min_px(k) for k in ("R-35", C.BARE_FLOOR_48_IDS[0])}
    one, one48, two = mins["R-35"]["one-color"], mins[C.BARE_FLOOR_48_IDS[0]]["one-color"], mins["R-35"]["two-color"]
    min_table = "\n".join([
        "| Tile | Square | Rounded | Circle |", "|---|---:|---:|---:|",
        f"| One-color, the {122 - n48} icons that read at 32 px bare | {one['square']} px | {one['rounded']} px | {one['circle']} px |",
        f"| One-color, the {n48} icons that need 48 px bare | {one48['square']} px | {one48['rounded']} px | {one48['circle']} px |",
        f"| Two-color, all 122 icons | {two['square']} px | {two['rounded']} px | {two['circle']} px |"])
    packing = ("The package comes as two archives that unpack into the same folder: the SVG archive holds the vectors, the catalog page and the data files, "
               "and the PNG archive holds the rasters and the reference crops. Each carries this readme." if split else
               "The package is one archive.")
    return f"""# Oath & Action Civic Line icons

Released on October 29, 2026, after Dustin Cathcart approved the set (DR-07) and its variants (DR-08 to DR-10). {packing}

## What the package holds

- Four bare editions of all 122 icons: `red-black/`, `black/`, `red-newsprint/` and `newsprint/`, 488 SVGs, with transparent PNGs at 256 and 512 px in `png-256/` and `png-512/` (976 PNGs).
- Tiles: twelve per icon in `tiles/<shape>-<tile>/`, each with `svg/`, `png-256/` and `png-512/` (1,464 SVGs and 2,928 PNGs).
- `contact-sheets/`: the five catalog sheets in all four editions, as SVG, PNG and 2x PNG, and `contact-sheets/tiles/`: twelve overview sheets with all 122 tiles of each kind.
- `reference-crops/`: 244 untouched crops of the supplied reference sheets.
- `{os.path.basename(CATALOG)}`: a searchable page with every icon, edition and tile.
- The inventory (`{os.path.basename(C.INVENTORY_JSON)}` and `.csv`), the fidelity measurements (`{os.path.basename(FIDELITY)}`) and the contrast table (`{os.path.basename(CONTRAST)}`).

## The four editions

| Edition | Lines | Accent | Ground it is drawn for |
|---|---|---|---|
| Red-black | Charcoal #121212 | Pillar Red #E63946 | Newsprint #DCD9D2 and White |
| Black | Charcoal #121212 | Charcoal | Newsprint, White and any light ground |
| Red-newsprint | Newsprint #DCD9D2 | Pillar Red #E63946 | Charcoal |
| Newsprint | Newsprint #DCD9D2 | Newsprint | Charcoal and Prussian #1F2D5A, where red never sits |

Each edition is the red-black file with its ink colors swapped, so all four share every coordinate. {check_line} Inside each SVG the main drawing sits in the group marked `data-part="base"` and the colored parts in the group marked `data-part="accent"`; in a tile the shape carries `data-part="tile"` and the icon group `data-part="icon"`. Every id inside a file starts with that file's root id, such as `oa-civic-line-cl-057-red-black` or `oa-civic-line-cl-057-tile-rounded-charcoal-two-color`, so any number of files can be inlined on one page, hidden or shown, without one file's mask reaching into another.

## Size, scale and stroke

Every bare file has a transparent background and a 128 by 128 viewBox. Each icon grows toward 116 of the 128 units by at most 1.25 times the set's shared scale of {sc['s_units_per_source_px']} units per source pixel (DR-08), so strokes run from {lo:.2f} to {hi:.2f} units and every icon sits centered on its own drawing.

The icons read best from 48 px up. At 24 px the stroke is half a pixel wide ({lo * 24 / 128:.2f} to {hi * 24 / 128:.2f} px), and at 32 px {lo * 32 / 128:.2f} to {hi * 32 / 128:.2f} px, so fine details soften. Use below 32 px would need its own small-size drawings.

## Tiles

Each icon comes in a square, a rounded square and a circle (DR-10). The rounded square is the superellipse |x|^5 + |y|^5 = 1 drawn with 96 cubic curves whose curvature runs on without a step at every join, the continuous corner of an app icon rather than a plain rounded corner. A Charcoal tile carries the Newsprint editions and a Newsprint tile the Charcoal editions, each in two-color and one-color. Names end in `-Tile-<Shape>-<Tile>-Two-Color` or `-One-Color`.

In a tile the bare icon scales about the center by {f['square']:g} (square), {f['rounded']:g} (rounded) or {f['circle']:g} (circle), chosen on a calibration board of twenty varied icons at 96 and 192 px; the 48 px rows sit below the tile minimum and are kept for reference. Measured against the side of a square with the tile's area, the icon spans 0.680 of the square, 0.677 of the rounded square and 0.700 of the circle, whose edge closes in at the corners, so the three shapes hold one icon size.

On top of the shape factor, {vr.get('icons_with_optical_scale', len(C.TILE_OPTICAL_SCALE))} icons carry an optical scale between {min(C.TILE_OPTICAL_SCALE.values()):.2f} and {max(C.TILE_OPTICAL_SCALE.values()):.2f}: the dense, squarish drawings come down a little and the compact or thin ones go up, and the four pillar marks are set as one group so they read as equals in a row. Where the larger size would make a line heavier than the set's heaviest stroke, every stroke width in that tile is multiplied down to {C.TILE_STROKE_CAP:.2f} units, so tile lines run from {t_lo:.2f} to {t_hi:.2f} units. {len(C.TILE_OFFSET_X)} icons whose subject is heavy on one side ({shifted}) move {min(offs):.1f} to {max(offs):.1f} units toward their light side in the rounded tile, and in proportion in the other two. The inventory records each icon's optical scale (`tile_optical_scale`), offset (`tile_offset_x`), scale per shape (`tile_scale`) and line weight in the tile (`tile_stroke_units`). The bare editions stay centered on their ink box. Every icon keeps a clear margin from every tile edge; the smallest are {m.get('square', {}).get('min_margin', 0):.1f} units on the square ({m.get('square', {}).get('min_margin_id', '')}), {m.get('rounded', {}).get('min_margin', 0):.1f} on the rounded square ({m.get('rounded', {}).get('min_margin_id', '')}) and {m.get('circle', {}).get('min_margin', 0):.1f} on the circle ({m.get('circle', {}).get('min_margin_id', '')}), out of 128.

### Minimum tile sizes

A tile shrinks its icon, so each tile has a smallest size, recorded per icon in the inventory as `tile_min_px`:

{min_table}

Each minimum is the bare icon's floor (32 px, or 48 px for the {n48} icons listed in the inventory) divided by the shape factor and rounded up to a multiple of 4 px; a two-color tile takes the 48 px floor for every icon, so its Pillar Red reaches its true value. At the two-color minimum the line is {min(full):.2f} to {max(full):.2f} px for the icons at the set's full stroke, and {thin[0]:.2f} px at the least ({thin[1]}, whose tile line is the thinnest in the set).

### Using the tiles

- A two-color tile is for an icon that stands alone: an app tile, an avatar or a single feature icon. In a row or a menu, use one-color tiles and give the red to the current item only (rule 05.3, D2-01).
- A Newsprint tile on a White page has a soft edge (1.41:1). On White, use the Charcoal tile or a bare red-black or black icon.
- For an iOS or Android app icon, supply the square tile at full bleed and let the platform apply its own corner. Never submit the rounded or circle tile, which would round the corner twice. The square tile PNGs carry an alpha channel today; the App Store's icon size and alpha rules and Android's adaptive-icon safe zone get checked on the platforms' own pages in the applications phase (Master Brief section 18).

## Contrast

Charcoal and Newsprint lines meet their grounds at 13.29:1. Pillar Red meets Charcoal at {red_ch:.2f}:1 and White at 4.17:1. On Newsprint it measures {red_np:.2f}:1, under the 3:1 guideline for graphics, so on the red-black edition and the Newsprint two-color tiles the red adds emphasis to a shape that the one-color editions also carry. The full table is in `{os.path.basename(CONTRAST)}`.

## Traced reconstructions and reference crops

The SVGs are traced reconstructions. Each was drawn as clean vector geometry over its reference and measured against it, with one line weight across the set and true circles and straight lines where the drawing means them (DR-03). They are not pixel copies of the sheets. The fidelity table records each trace's silhouette overlap with its reference (median {med('silhouette_iou'):.3f}, where 1 means identical), the overlap of the red parts (median {med('red_iou'):.3f}) and how far its edges sit from the reference's (median of the per-icon means {med('edge_mean_px'):.2f} source pixels).

The reference crops are untouched source pixels: exact copies of each icon's rectangle on the supplied sheets, kept for comparison.

## R-35

R-35 is named "Term Limits · Rejected". It records an option the atlas rejected, and it keeps that name in its file names, the inventory, the sheets and the catalog.

## Contact sheets

The contact sheets repeat the layout of the supplied sheets cell for cell, with the traced icons in place of the raster ones and the approved Edition 06 wordmark (DR-05). All 32 sheets share one header and footer: the wordmark, a rule from x = 49 to 1487, and the title and footer set flush right at x = 1487. The captions in each row share one baseline. Their text is set in Inter and converted to outlines, so no font files are needed.

## Rights

Dustin Cathcart supplied the ten Civic Line reference sheets. The studio traced them into these vector masters under decision DR-02, which grants an exception to the brief's rule on reference images for these sheets only. Inter is licensed under the SIL Open Font License 1.1; the package contains no font files.
"""


def collect():
    """(arcname, source path) for every file, grouped as vector or raster."""
    vec, ras = [], []

    def add(lst, folder, ext):
        d = os.path.join(C.ASSETS, folder)
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.isfile(p) and f.endswith(ext):
                lst.append((f"{TOP}/{folder}/{f}", p))
    for ed in C.EDITIONS:
        add(vec, ed, ".svg")
        for px in (256, 512):
            add(ras, f"png-{px}/{ed}", ".png")
    for sh in C.TILE_SHAPES:
        for tl in C.TILE_COLOURS:
            add(vec, f"tiles/{sh}-{tl}/svg", ".svg")
            for px in (256, 512):
                add(ras, f"tiles/{sh}-{tl}/png-{px}", ".png")
    for folder in ("contact-sheets", "contact-sheets/tiles"):
        add(vec, folder, ".svg")
        add(ras, folder, ".png")
    add(ras, "reference-crops", ".png")
    vec.append((f"{TOP}/{os.path.basename(CATALOG)}", CATALOG))
    data = [(f"{TOP}/{os.path.basename(p)}", p) for p in (C.INVENTORY_JSON, C.INVENTORY_CSV, FIDELITY, CONTRAST)]
    return vec, ras, data


def write_zip(path, entries, readme):
    tmp = path + ".tmp"
    items = sorted(entries + [(f"{TOP}/{README}", None)], key=lambda e: e[0])
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, src in items:
            zi = zipfile.ZipInfo(arc, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, readme.encode("utf-8") if src is None else open(src, "rb").read())
    os.replace(tmp, path)
    problems = []
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            problems.append(f"{os.path.basename(path)}: corrupt entry {bad}")
        for arc, src in items:
            want = readme.encode("utf-8") if src is None else open(src, "rb").read()
            if hashlib.sha256(z.read(arc)).digest() != hashlib.sha256(want).digest():
                problems.append(f"{arc} differs from its source")
        names = z.namelist()
    return names, problems


def folder_counts(names):
    out = {}
    for n in names:
        parts = n.split("/")[1:-1]
        key = "/".join(parts) or "."
        out[key] = out.get(key, 0) + 1
    return out


def main():
    os.makedirs(DELIV, exist_ok=True)
    vec, ras, data = collect()
    single = os.path.join(DELIV, BASE + ".zip")
    svg_zip, png_zip = os.path.join(DELIV, BASE + "-SVG.zip"), os.path.join(DELIV, BASE + "-PNG.zip")
    names, problems = write_zip(single, vec + ras + data, readme_text(False))
    outputs = [single]
    if os.path.getsize(single) > LIMIT:
        os.remove(single)
        readme = readme_text(True)
        n1, p1 = write_zip(svg_zip, vec + data, readme)
        n2, p2 = write_zip(png_zip, ras + data, readme)
        names, problems, outputs = n1 + n2, p1 + p2, [svg_zip, png_zip]
    else:
        for p in (svg_zip, png_zip):
            if os.path.exists(p):
                os.remove(p)
    if "—" in readme_text(True):
        problems.append("em dash in the readme")
    for p in outputs:
        size = os.path.getsize(p)
        mb = size / 1e6
        print(f"wrote {os.path.relpath(p, C.ROOT)}: {mb:.2f} MB ({size:,} bytes)" + ("  (OVER 90 MB)" if size > LIMIT else ""))
        if size > LIMIT:
            problems.append(f"{os.path.basename(p)} is over 90 MB")
    counts = folder_counts(names)
    expect = {ed: 122 for ed in C.EDITIONS}
    expect.update({f"png-{px}/{ed}": 122 for px in (256, 512) for ed in C.EDITIONS})
    expect.update({f"tiles/{sh}-{tl}/{sub}": 244 for sh in C.TILE_SHAPES for tl in C.TILE_COLOURS for sub in ("svg", "png-256", "png-512")})
    expect.update({"contact-sheets": 60, "contact-sheets/tiles": 36, "reference-crops": 244})
    for k, v in expect.items():
        if counts.get(k) != v:
            problems.append(f"{k}: {counts.get(k)} files, expected {v}")
    print("  folders: " + ", ".join(f"{k} {counts.get(k)}" for k in sorted(expect)))
    for p in problems:
        print("PROBLEM:", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
