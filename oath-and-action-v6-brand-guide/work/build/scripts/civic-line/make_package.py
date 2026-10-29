"""Part F: the review package.

    python3 -I make_package.py

Writes work/build/packages/<date>_Oath-And-Action-Civic-Line-Icons_REVIEW.zip
with one top folder, oath-and-action-civic-line-icons/, holding red-black/,
black/, png-256/, png-512/, contact-sheets/, reference-crops/, the inventory
(JSON and CSV), the fidelity metrics CSV and a short readme. Entries are
sorted and stamped with the package date, so a rerun on the same files gives
the same archive. After writing, the script reopens the archive, tests it,
counts every folder and compares each entry's bytes with its source file.
The package stays out of deliverables/ until Dustin approves it.
"""
import csv
import hashlib
import io
import os
import statistics
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

PKG_DIR = os.path.join(C.ROOT, "work", "build", "packages")
ZIP = os.path.join(PKG_DIR, f"{C.DATE}_Oath-And-Action-Civic-Line-Icons_REVIEW.zip")
TOP = "oath-and-action-civic-line-icons"
README = f"{C.DATE}_Civic-Line-Readme.md"
FIDELITY = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Fidelity-Metrics.csv")
STAMP = (2026, 10, 29, 0, 0, 0)
EXPECT = {"red-black": 122, "black": 122, "png-256/red-black": 122, "png-256/black": 122,
          "png-512/red-black": 122, "png-512/black": 122, "contact-sheets": 30, "reference-crops": 244}


def readme_text():
    sc = C.read_json(C.SCALE_JSON)
    rows = list(csv.DictReader(open(FIDELITY, encoding="utf-8")))

    def med(k):
        v = [float(r[k]) for r in rows if r[k]]
        return statistics.median(v) if v else float("nan")
    states = {}
    for r in rows:
        states[r["state"]] = states.get(r["state"], 0) + 1
    st_txt = ", ".join(f"{n} {s}" for s, n in sorted(states.items()))
    u = sc["stroke_width_units"]
    vr = C.read_json(os.path.join(C.QA, f"{C.DATE}_Civic-Line-Verify-Report.json")) or {}
    n_tree = vr.get("edition_trees_identical", 0)
    if n_tree == 122 and not vr.get("errors"):
        tree_txt = "A script parsed all 122 pairs and found the same elements and attributes in each, with colour as the only difference."
    else:
        tree_txt = (f"A script parsed the pairs and found {n_tree} of 122 identical apart from colour; "
                    f"the verification report lists {len(vr.get('errors', []))} problems to fix before approval.")
    return f"""# Oath & Action Civic Line icons: review package

Prepared on October 29, 2026 for Dustin Cathcart's review. This is a review copy. It moves to `deliverables/` once Dustin approves it.

## What the package holds

- `red-black/` and `black/`: 122 SVG masters in each edition, 244 in all.
- `png-256/` and `png-512/`: transparent PNGs of every SVG at 256 and 512 px, each with `red-black/` and `black/` folders, 488 in all.
- `contact-sheets/`: the five catalogue sheets in both editions, each as SVG, PNG and a 2x PNG.
- `reference-crops/`: 244 untouched crops of the supplied reference sheets, one from the black sheet and one from the red sheet per icon.
- `{os.path.basename(C.INVENTORY_JSON)}` and `.csv`: one row per icon with its ID, name, sheet, row, column, crop rectangle, file names and status.
- `{os.path.basename(FIDELITY)}`: the measurements of each trace against its reference.

## The two editions

The red-black edition draws each icon in Charcoal (#121212) and the parts the catalogue names in Pillar Red (#E63946). It is drawn for Newsprint (#DCD9D2) and White grounds. The black edition draws every part in Charcoal. Each black file is its red-black file with Pillar Red swapped for Charcoal, so the two share every coordinate. {tree_txt}

Inside each SVG the main drawing sits in a group with the id `base` and the coloured parts in a group with the id `accent`.

## Size, scale and stroke

Every file has a transparent background. The SVGs contain no background shape, and the PNGs are transparent outside the drawing.

Every SVG uses a 128 by 128 viewBox with one stroke width of {u:.2f} units, measured from the sheets as {sc['W_source_px']} source pixels. One scale serves the whole set, {sc['s_units_per_source_px']} units per source pixel, so each icon keeps its size relative to the others, as on the sheets. The widest icon, {sc['largest_extent_id']}, spans 116 units, and each icon is centred on its own drawing.

The icons read best from 48 px up. At 24 px the stroke is half a pixel wide ({u * 24 / 128:.2f} px), and at 32 px it is {u * 32 / 128:.2f} px, so fine details soften. Use below 32 px would need its own small-size drawings.

## Traced reconstructions and reference crops

The SVGs are traced reconstructions. Each was drawn as clean vector geometry over its reference and measured against it, with one line weight across the set and true circles and straight lines where the drawing means them (decision DR-03). They are not pixel copies of the sheets. The fidelity CSV records each trace's silhouette overlap with its reference (median {med('silhouette_iou'):.3f}, where 1 means identical), the overlap of the red parts (median {med('red_iou'):.3f}) and how far its edges sit from the reference's (median of the per-icon means {med('edge_mean_px'):.2f} source pixels). Status today: {st_txt}.

The reference crops are untouched source pixels: exact copies of each icon's rectangle on the supplied sheets, kept for comparison.

## R-35

R-35 is named "Term Limits · Rejected". It records an option the atlas rejected, and it keeps that name in its file names, the inventory and the contact sheets.

## Contact sheets

The contact sheets repeat the layout of the supplied sheets cell for cell, with the traced icons in place of the raster ones. They carry the approved Edition 06 wordmark (decision DR-05). Their text is set in Inter and converted to outlines, so the sheets need no font files.

## Rights

Dustin Cathcart supplied the ten Civic Line reference sheets. The studio traced them into these vector masters under decision DR-02, which grants an exception to the brief's rule on reference images for these sheets only. Inter is licensed under the SIL Open Font License 1.1; the package contains no font files.
"""


def entries():
    """(arcname, source path or None, bytes or None) in sorted order."""
    out = []
    for folder in ("red-black", "black", "png-256/red-black", "png-256/black", "png-512/red-black", "png-512/black",
                   "contact-sheets", "reference-crops"):
        d = os.path.join(C.ASSETS, folder)
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                out.append((f"{TOP}/{folder}/{f}", p, None))
    for p in (C.INVENTORY_JSON, C.INVENTORY_CSV, FIDELITY):
        out.append((f"{TOP}/{os.path.basename(p)}", p, None))
    out.append((f"{TOP}/{README}", None, readme_text().encode("utf-8")))
    return sorted(out, key=lambda e: e[0])


def main():
    os.makedirs(PKG_DIR, exist_ok=True)
    if "—" in readme_text():
        raise SystemExit("em dash in the readme")
    es = entries()
    tmp = ZIP + ".tmp"
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, src, data in es:
            zi = zipfile.ZipInfo(arc, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data if data is not None else open(src, "rb").read())
    os.replace(tmp, ZIP)
    # reopen and check
    problems = []
    with zipfile.ZipFile(ZIP) as z:
        bad = z.testzip()
        if bad:
            problems.append(f"corrupt entry {bad}")
        names = z.namelist()
        for arc, src, data in es:
            want = data if data is not None else open(src, "rb").read()
            if hashlib.sha256(z.read(arc)).digest() != hashlib.sha256(want).digest():
                problems.append(f"{arc} differs from its source")
    counts = {k: sum(1 for n in names if n.startswith(f"{TOP}/{k}/") and n.count("/") == k.count("/") + 2) for k in EXPECT}
    for k, n in EXPECT.items():
        if counts[k] != n:
            problems.append(f"{k}: {counts[k]} files, expected {n}")
    top_files = sorted(n.split("/", 1)[1] for n in names if n.count("/") == 1)
    size = os.path.getsize(ZIP)
    print(f"wrote {os.path.relpath(ZIP, C.ROOT)}: {len(names)} entries, {size / 1024 / 1024:.2f} MB")
    print("  folders:", ", ".join(f"{k} {v}" for k, v in counts.items()))
    print("  top level:", ", ".join(top_files))
    for p in problems:
        print("PROBLEM:", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
