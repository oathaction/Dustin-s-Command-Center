"""Verify the Civic Line set and compile the completion ledger.

    python3 -I verify_set.py [--sync-inventory]

Checks membership and counts (122 IDs, 244 SVGs, 488 PNGs at completion),
colour tokens, edition pairs, SVG structure, viewBox, drawn bounds, PNG sizes
and transparency. Icons without a source are reported as 'todo', not as errors,
until the set is complete. Writes qa/20261029_Civic-Line-Completion-Ledger.md
and qa/20261029_Civic-Line-Verify-Report.json. Exit code 1 on any error.
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

LEDGER = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Completion-Ledger.md")
REPORT = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Verify-Report.json")
FORBIDDEN = {"text", "tspan", "textPath", "image", "foreignObject", "use", "script", "style", "pattern", "filter",
             "linearGradient", "radialGradient", "clipPath", "symbol", "a", "switch"}
MASK_COLORS = {"#FFFFFF", "#000000"}
COLOR_ATTRS = ("fill", "stroke", "stop-color", "color", "flood-color", "lighting-color")
HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")


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


def check_svg(path, edition, errs):
    """Structure, colours, viewBox and bounds of one export file."""
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
    allowed = {C.CHARCOAL} | ({C.PILLAR_RED} if edition == "red-black" else set())

    def walk(node, in_mask=False, in_defs=False):
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
                ok = vu in allowed or (in_mask and vu in MASK_COLORS)
                if not ok:
                    errs.append(f"{name}: <{t}> {k}={v} is not an allowed token for the {edition} edition")
            if "style" in ch.attrib:
                errs.append(f"{name}: <{t}> uses a style attribute")
            if t == "rect" and not in_mask and not in_defs:
                w = float(ch.attrib.get("width", 0))
                h = float(ch.attrib.get("height", 0))
                if w >= 0.9 * 128 and h >= 0.9 * 128:
                    errs.append(f"{name}: background-sized <rect> {w} x {h}")
            walk(ch, in_mask or t == "mask", in_defs or t == "defs")

    walk(root)
    for hx in HEX_RE.findall(text):
        hu = hx.upper()
        if edition == "black" and (hu == C.PILLAR_RED or (is_reddish(hu))):
            errs.append(f"{name}: red value {hx} in the black edition")
    groups = [strip(g.tag) == "g" and g.attrib.get("id") for g in root if strip(g.tag) == "g"]
    if not any(g and g.startswith("base") for g in groups):
        errs.append(f"{name}: no base group")
    b, _ = S.drawn_bounds(text.split("?>", 1)[-1])
    if b is None:
        errs.append(f"{name}: draws nothing")
    elif b[0] < 0 or b[1] < 0 or b[2] > 128 or b[3] > 128:
        errs.append(f"{name}: drawing reaches outside 0..128 with stroke counted: {[round(v, 3) for v in b]}")
    return b


def check_png(path, size, errs):
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
    if a.min() != 0 or a[0, 0] != 0 or a[0, -1] != 0 or a[-1, 0] != 0 or a[-1, -1] != 0:
        errs.append(f"{name}: background is not transparent")
    if a.max() == 0:
        errs.append(f"{name}: image is empty")
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    if edge.max() > 0:
        errs.append(f"{name}: ink touches the image edge (possible clipping)")


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
    # files present in the export folders
    folders = {"red-black": "svg_red_black", "black": "svg_black"}
    expected_files = {f: {r["exports"][k] for r in rows} for f, k in folders.items()}
    png_expected = {}
    for px in (256, 512):
        png_expected[f"png-{px}/red-black"] = {r["exports"]["png_red_black"] for r in rows}
        png_expected[f"png-{px}/black"] = {r["exports"]["png_black"] for r in rows}
    for f, exp in list(expected_files.items()) + list(png_expected.items()):
        d = os.path.join(C.ASSETS, f)
        have = set(os.listdir(d)) if os.path.isdir(d) else set()
        for x in sorted(have - exp):
            errs.append(f"{f}/{x}: not an inventory export name")
    per = []
    n_svg = n_png = 0
    pairs_ok = 0
    for r in rows:
        i = r["id"]
        has_src = os.path.exists(os.path.join(C.SRC, f"{i}.svg"))
        st = C.read_json(os.path.join(C.QA, "status", f"{i}.json")) or {}
        rb = os.path.join(C.ASSETS, "red-black", r["exports"]["svg_red_black"])
        bk = os.path.join(C.ASSETS, "black", r["exports"]["svg_black"])
        pngs = [(os.path.join(C.ASSETS, f"png-{px}", ed, r["exports"][key]), px)
                for px in (256, 512) for ed, key in (("red-black", "png_red_black"), ("black", "png_black"))]
        state = st.get("state", "todo") if has_src else "todo"
        e0 = len(errs)
        if has_src:
            for p in (rb, bk):
                if not os.path.exists(p):
                    errs.append(f"{i}: source exists but {os.path.relpath(p, C.ASSETS)} is missing; run build_icon.py {i}")
            if os.path.exists(rb) and os.path.exists(bk):
                n_svg += 2
                check_svg(rb, "red-black", errs)
                check_svg(bk, "black", errs)
                a, b = open(rb, "rb").read(), open(bk, "rb").read()
                if a.replace(C.PILLAR_RED.encode(), C.CHARCOAL.encode()) != b:
                    errs.append(f"{i}: black file is not the red-black file with {C.PILLAR_RED} swapped for {C.CHARCOAL}")
                else:
                    pairs_ok += 1
            for p, px in pngs:
                if not os.path.exists(p):
                    errs.append(f"{i}: {os.path.relpath(p, C.ASSETS)} is missing")
                else:
                    n_png += 1
                    check_png(p, px, errs)
            if not st:
                errs.append(f"{i}: source exists but qa/status/{i}.json is missing; run build_icon.py {i}")
        else:
            for p in [rb, bk] + [q for q, _ in pngs]:
                if os.path.exists(p):
                    errs.append(f"{i}: {os.path.relpath(p, C.ASSETS)} exists without a source")
        lm = st.get("last_metrics", {}) if has_src else {}
        per.append({"id": i, "label": r["label"], "sheet": r["sheet"], "row": r["row"], "column": r["column"],
                    "state": state, "tracer": st.get("tracer") if has_src else None,
                    "iterations": st.get("iterations", 0) if has_src else 0,
                    "silhouette_iou": lm.get("silhouette_iou_1x"), "red_iou": lm.get("red_iou_1x"),
                    "edge_mean": lm.get("edge_mean_px"), "edge_p95": lm.get("edge_p95_px"),
                    "corrections": len(st.get("corrections", [])) if has_src else 0,
                    "last_build": st.get("last_build") if has_src else None, "errors": len(errs) - e0})
    states = {s: sum(1 for p in per if p["state"] == s) for s in ("todo", "traced", "reviewed", "fixed")}
    complete = states["todo"] == 0
    if complete:
        if n_svg != 244:
            errs.append(f"{n_svg} SVGs, expected 244")
        if n_png != 488:
            errs.append(f"{n_png} PNGs, expected 488")
    else:
        notes.append(f"set incomplete: {states['todo']} icons todo; totals so far {n_svg} of 244 SVGs and {n_png} of 488 PNGs")
    report = {"checked": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
              "ids": len(ids), "counts_by_sheet": counts, "order_matches_catalog": cat == ids,
              "svgs": n_svg, "pngs": n_png, "pairs_identical_after_swap": pairs_ok, "states": states,
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
    print(f"IDs {len(ids)} ({counts}); SVGs {n_svg}/244; PNGs {n_png}/488; pairs identical {pairs_ok}; states {states}")
    for n in notes:
        print("note:", n)
    for e in errs:
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
         f"Files: {rep['svgs']} of 244 SVGs, {rep['pngs']} of 488 PNGs. Edition pairs identical after the token swap: {rep['pairs_identical_after_swap']}.",
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
