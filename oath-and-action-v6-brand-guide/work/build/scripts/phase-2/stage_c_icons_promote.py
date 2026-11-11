#!/usr/bin/env python3
"""Promote drawings board C's approved drawings into the sets in use (November 11, 2026).

    python3 -I work/build/scripts/phase-2/stage_c_icons_promote.py                 every part, then the checks
    python3 -I work/build/scripts/phase-2/stage_c_icons_promote.py --part fits     one part: fits, housing, inventory,
                                                                                   utility (each runs its own checks)
    python3 -I work/build/scripts/phase-2/stage_c_icons_promote.py --check-only    the checks alone
    --scratch DIR   temporary files and the checks' JSON (default: the promotion C icon scratchpad)

The task is owner 1 of work/handoffs/phase-2/20261111_Promotion-Stage-C-Brief.md. Decisions: DR-207 (Housing option A),
DR-208 (the 16 px Pause redraw and Filter option A), DR-209 (the 37 fits, the pillar icons' switch), D2-1262 (CL-075),
D2-1263 (files first made here carry 20261111), D2-1264 (the replaced utility files move to _archive/), D2-1265
(fit-24/ and its sprite symbols), D2-1236 and D2-1238 (Housing at 48 px and up, tiles on the 48 px floor), and the
November 10 promotion's conventions (D2-716, DR-09, DR-10, DR-08).

It writes
  work/build/assets/civic-line-v6/
    fit-24/20261111_Civic-Line-<ID>-<Slug>-24px-Fit-Black.svg     the 37 fits in use
    fit-24/png/<same stem>.png and -2x.png                         previews at 1x and 2x
    fit-24/20261111_Civic-Line-24px-Fits-In-Use-Manifest.json
    <edition>/20261111_Oath-And-Action-Civic-Line-CL-075-Housing-<Edition>.svg     four editions
    png-256/<edition>/, png-512/<edition>/                         CL-075's previews
    tiles/<shape>-<tile>/svg|png-256|png-512/                      CL-075's 12 tiles, by the October tile code
    20261110_Civic-Line-V6-Inventory.csv and .json                 a 125th row, CL-075, after CL-072 (sheet 03)
  work/build/assets/utility/
    svg-16/20261111_Utility-Pause-16px.svg, svg-16/20261111_Utility-Filter-16px.svg
    png/20261111_Utility-<Pause|Filter>-16px.png and -2x.png
    _archive/svg-16/ and _archive/png/                             the replaced stage B files, moved by git mv
    20261110_Utility-Icons-Manifest.json                           the two 16 px rows, now DR-208

How a file in use is made. It is its approved file with only its ids, title, description (or, for a utility icon, its
comment line) and file name changed. CL-075's light editions come from the October color swap (cl_svg.derive_editions,
DR-09), as the option's did; its tiles from cl_tiles.tile_svg with the optics the option's tiles carry. Previews are
drawn by the renderer that drew the approved files' previews (render_svgs.js for Civic Line and the fits) or by the
utility promotion's own Chromium step (utility_icons_promote.run_node), as the other utility previews in use were.

Checks (after every part, and alone with --check-only); the script exits 1 on any failure:
  fits       each fit in use, with its root id and desc put back, equals its approved file byte for byte; root
             attributes; its PNGs equal the approved previews pixel for pixel; 37 SVGs, 74 PNGs, the manifest
  housing    each edition, with its root id, data-id, title and desc put back, equals option A's file byte for byte;
             the option's source re-bakes to its red-black file; October's structure and edition-tree checks; each
             tile, put back the same way, equals option A's tile byte for byte, and passes verify_set.check_tile;
             every preview and tile PNG passes verify_set.check_png and equals the option's pixel for pixel
  inventory  125 rows in JSON and CSV; every other row and CSV line as it stood in git HEAD; every path it names
             exists; no empty CSV cell outside flags
  utility    each final's drawing (every byte after its comment line) and root tag equal its approved redraw's; the
             archived files hash as they did in git HEAD; svg-16/ holds one file per icon; the PNGs equal the redraws'
             pixel for pixel; the manifest's two rows
  ids        no id repeats across the SVGs in civic-line-v6/ (fit-24/ and the tiles included) and pillar-icons/
"""
import argparse
import copy
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "work", "build", "scripts", "civic-line"))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import cl_common as C  # noqa: E402
import cl_svg as S  # noqa: E402
import cl_tiles as T  # noqa: E402
import verify_set as V  # noqa: E402
import civic_line_stage_b_common as B  # noqa: E402
import civic_line_v6_promote as PROMO  # noqa: E402
import utility_icons_promote as UP  # noqa: E402

DATE = "20261111"
ASSETS = os.path.join(ROOT, "work", "build", "assets")
V6 = os.path.join(ASSETS, "civic-line-v6")
FIT_IN = os.path.join(ASSETS, "civic-line-24-fit")
FIT_OUT = os.path.join(V6, "fit-24")
FIT_MANIFEST = os.path.join(FIT_OUT, f"{DATE}_Civic-Line-24px-Fits-In-Use-Manifest.json")
TOPICS = os.path.join(ASSETS, "civic-line-new-topics")
UTIL = os.path.join(ASSETS, "utility")
UTIL_IN = os.path.join(ASSETS, "utility-16-redraw")
UTIL_MANIFEST = os.path.join(UTIL, "20261110_Utility-Icons-Manifest.json")
INV_JSON, INV_CSV = PROMO.INV_JSON, PROMO.INV_CSV
SCRATCH = "/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/icons"
EDITIONS = list(C.EDITIONS)
DESC_RE, TITLE_RE = PROMO.DESC_RE, PROMO.TITLE_RE


def sha(x):
    return hashlib.sha256(x if isinstance(x, bytes) else open(x, "rb").read()).hexdigest()


def rel(p, start=ROOT):
    return os.path.relpath(p, start)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def head_bytes(path):
    """The file's bytes in git HEAD, or None."""
    r = subprocess.run(["git", "show", f"HEAD:{rel(path, git_top())}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


_TOP = []


def git_top():
    if not _TOP:
        _TOP.append(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, capture_output=True,
                                   text=True, check=True).stdout.strip())
    return _TOP[0]


def same_pixels(a, b):
    x = np.asarray(Image.open(a).convert("RGBA")).astype(int)
    y = np.asarray(Image.open(b).convert("RGBA")).astype(int)
    return x.shape == y.shape and int(np.abs(x - y).max()) == 0


def body(svg_text):
    """The stage C renderer's input: no XML declaration, no comments (civic_line_stage_c_drawings.body)."""
    s = re.sub(r"<\?xml[^>]*>\s*", "", svg_text)
    return re.sub(r"<!--.*?-->\s*", "", s, flags=re.S)


def render(jobs, scratch):
    if jobs:
        B.render(jobs, os.path.join(scratch, "render"))


# ================================================================== the 37 fits (DR-209, D2-1265)

def fit_rows():
    man = json.load(open(os.path.join(FIT_IN, "20261110_Civic-Line-24px-Fits-Manifest.json"), encoding="utf-8"))
    inv = {r["id"]: r for r in json.load(open(INV_JSON, encoding="utf-8"))["icons"]}
    out = []
    for x in man["fits"]:
        r = inv[x["id"]]
        src = os.path.join(ROOT, x["svg"])
        stem = f"{DATE}_Civic-Line-{x['id']}-{r['slug']}-24px-Fit-Black"
        out.append(dict(id=x["id"], word=x["word"], atlas=x["atlas_id"], slug=r["slug"], kept=x["kept"], src=src,
                        src_png=(os.path.join(ROOT, x["png_1x"]), os.path.join(ROOT, x["png_2x"])),
                        stem=stem, out=os.path.join(FIT_OUT, stem + ".svg"),
                        png=(os.path.join(FIT_OUT, "png", stem + ".png"), os.path.join(FIT_OUT, "png", stem + "-2x.png")),
                        master=os.path.join(V6, "black", r["exports"]["svg_black"])))
    return out


def fit_src_root(i):
    return f"oa-civic-line-24-fit-{i.lower()}-black"


def fit_root(i):
    return f"oa-civic-line-{i.lower()}-24px-fit-black"


def fit_desc(f):
    return escape(f"Oath & Action Civic Line {f['id']} {f['word']}, the 24 px pixel fit in use: drawn pixel by pixel "
                  f"on the 24 px grid with a one-pixel line, every pixel Charcoal or empty, keeping the parts that make "
                  f"its master read. One color, the black edition only (D2-1132). Use it at 24 px on 1x screens; from "
                  f"2x the master draws instead, the pillar icons' switch (DR-179). Approved by name on drawings board "
                  f"C (DR-209) and put into use on November 11, 2026.")


def fit_final(f):
    t = read(f["src"])
    assert t.count(fit_src_root(f["id"])) == 2, f["id"]
    t = t.replace(fit_src_root(f["id"]), fit_root(f["id"]))
    assert len(DESC_RE.findall(t)) == 1
    return DESC_RE.sub(lambda m: f"<desc>{fit_desc(f)}</desc>", t, count=1)


def fit_revert(f, text):
    src = read(f["src"])
    t = text.replace(fit_root(f["id"]), fit_src_root(f["id"]))
    return DESC_RE.sub(lambda m: DESC_RE.search(src).group(0), t, count=1)


def build_fits(scratch):
    fits = fit_rows()
    jobs = []
    for f in fits:
        t = fit_final(f)
        write(f["out"], t)
        for z, out in zip((1, 2), f["png"]):
            jobs.append({"svg": body(t).replace('width="24" height="24"', f'width="{24 * z}" height="{24 * z}"', 1),
                         "w": 24 * z, "h": 24 * z, "bg": None, "out": out})
    render(jobs, scratch)
    write_fit_manifest(fits)
    print(f"fits: {len(fits)} SVGs and {len(jobs)} PNGs in {rel(FIT_OUT)}")


def write_fit_manifest(fits):
    rows = []
    for f in fits:
        rows.append({
            "id": f["id"], "word": f["word"], "family": "atlas" if f["atlas"] else "topic", "atlas_id": f["atlas"],
            "approved": "DR-209",
            "svg": rel(f["out"], FIT_OUT), "png_1x": rel(f["png"][0], FIT_OUT), "png_2x": rel(f["png"][1], FIT_OUT),
            "sprite_symbol": f"oa-sym-{f['id'].lower()}-24px",
            "master_from_2x": {"svg": rel(f["master"], FIT_OUT), "sprite_symbol": f"oa-sym-{f['id'].lower()}"},
            "source_file": rel(f["src"], FIT_OUT),
            "source_sha256": sha(f["src"]), "sha256": sha(f["out"]),
            "drawing_sha256": sha(re.search(r'\sd="([^"]+)"', read(f["out"])).group(1).encode()),
            "kept": f["kept"],
        })
    out = {
        "title": "Civic Line 24 px pixel fits in use: the 37 topic and atlas drawings",
        "date": DATE,
        "made_by": "icon designer (oa-design-director), work/build/scripts/phase-2/stage_c_icons_promote.py, under "
                   "20261111_Promotion-Stage-C-Brief.md",
        "status": "In use. Dustin approved all 37 by name on drawings board C (DR-209). Each file is its approved fit "
                  "with only its root id, description and file name changed; the approved fits stay in "
                  "civic-line-24-fit/ as the record.",
        "decisions": ["DR-209", "DR-198", "DR-205", "DR-179", "D2-1132", "D2-1265", "D2-1263", "DR-136", "D2-587",
                      "D2-971", "D2-1237"],
        "rules": {
            "screens": "The pillar icons' switch (DR-179, DR-209): on 1x screens a topic or atlas symbol set at 24 px "
                       "draws its fit (oa-sym-<id>-24px); from 2x it draws its Civic Line master (oa-sym-<id>), "
                       "listed under master_from_2x.",
            "list": "Only the 37 here and the four pillar icons may be set at 24 px (the list of 41, DR-136, D2-587).",
            "edition": "One color, the black edition only (D2-1132). On Charcoal the sprite sets the ink to Newsprint, "
                       "as it does for the masters.",
            "sizes": "Use each fit at 24 px only.",
            "root_attributes": "data-id is the Civic Line ID and data-size is 24.",
            "neighbors": "CL-023, CL-028, R-08, R-27 and R-45 never share a view at small sizes (D2-971); nor do R-06, "
                         "R-41 and R-44 (D2-1237).",
        },
        "paths_relative_to": "work/build/assets/civic-line-v6/fit-24/",
        "order": "20261110_Stage-B-Ch10-Construction.md, section 10, as the approved fits' manifest",
        "count": len(rows),
        "fits": rows,
    }
    write(FIT_MANIFEST, json.dumps(out, indent=1, ensure_ascii=False) + "\n")


def check_fits(res, errs):
    fits = fit_rows()
    r = {"files": {}, "svg": 0, "png": 0}
    for f in fits:
        if not os.path.exists(f["out"]):
            errs.append(f"fit missing: {rel(f['out'])}")
            continue
        text = read(f["out"])
        back = fit_revert(f, text)
        same = back.encode("utf-8") == open(f["src"], "rb").read()
        root = ET.fromstring(text.split("?>", 1)[-1].encode())
        d_out = [e.attrib.get("d") for e in root.iter() if e.attrib.get("d")]
        d_src = [e.attrib.get("d") for e in ET.fromstring(read(f["src"]).split("?>", 1)[-1].encode()).iter() if e.attrib.get("d")]
        ids = [e.attrib["id"] for e in root.iter() if "id" in e.attrib]
        x = {"sha256": sha(f["out"]), "source_sha256": sha(f["src"]), "reverts_to_source_byte_for_byte": same,
             "path_data_equal": d_out == d_src,
             "root": {k: root.attrib.get(k) for k in ("id", "data-id", "data-size", "viewBox", "shape-rendering")}}
        if not same or d_out != d_src:
            errs.append(f"fit {f['id']}: does not revert to its approved file")
        if root.attrib.get("data-id") != f["id"] or root.attrib.get("data-size") != "24" or root.attrib.get("viewBox") != "0 0 24 24":
            errs.append(f"fit {f['id']}: root attributes wrong")
        if len(ids) != len(set(ids)) or any(not i.startswith(root.attrib["id"]) for i in ids):
            errs.append(f"fit {f['id']}: ids repeat or do not start with the root id")
        if "not in use" in text or "For approval" in text or "DR-209" not in text:
            errs.append(f"fit {f['id']}: description still reads as a proposal")
        for out, src, k in zip(f["png"], f["src_png"], ("png_1x", "png_2x")):
            ok = os.path.exists(out) and same_pixels(out, src)
            x[k + "_equals_approved_preview"] = ok
            if not ok:
                errs.append(f"fit {f['id']}: {k} differs from the approved preview")
            else:
                r["png"] += 1
        r["svg"] += 1 if same else 0
        r["files"][f["id"]] = x
    n_svg = len([n for n in os.listdir(FIT_OUT) if n.endswith(".svg")])
    n_png = len(os.listdir(os.path.join(FIT_OUT, "png")))
    r["counts"] = {"svg": n_svg, "png": n_png}
    if n_svg != 37 or n_png != 74:
        errs.append(f"fit-24: {n_svg} SVGs and {n_png} PNGs, expected 37 and 74")
    m = json.load(open(FIT_MANIFEST, encoding="utf-8"))
    r["manifest"] = {"rows": len(m["fits"]), "families": {k: sum(1 for x in m["fits"] if x["family"] == k) for k in ("topic", "atlas")}}
    for x in m["fits"]:
        if not os.path.exists(os.path.normpath(os.path.join(FIT_OUT, x["svg"]))) or \
           not os.path.exists(os.path.normpath(os.path.join(FIT_OUT, x["source_file"]))) or \
           not os.path.exists(os.path.normpath(os.path.join(FIT_OUT, x["master_from_2x"]["svg"]))):
            errs.append(f"fit manifest {x['id']}: a path does not resolve")
        if x["sha256"] != sha(os.path.join(FIT_OUT, x["svg"])):
            errs.append(f"fit manifest {x['id']}: hash out of date")
    res["fits"] = r
    print(f"fits: {r['svg']} of 37 revert byte for byte, {r['png']} of 74 PNGs equal the approved previews; "
          f"manifest {r['manifest']}")


# ================================================================== CL-075 Housing (DR-207, D2-1262)

HOUSING = dict(
    id="CL-075", label="Housing", slug="Housing", folder="civic-line-new-topics", stem="20261110_Housing-Option-A",
    src_id="Housing", dr="DR-207", pick="option A", sheet="03", row=5, column=1, floor32=False,
    shows="An apartment block of three floors beside a pitched-roof house on one ground line, red on one window of "
          "the block: homes of more than one kind, renters' and owners' alike.",
)
TILE_SHAPE = {"square": "Square", "rounded": "Rounded", "circle": "Circle"}
TILE_MODE = {"two-color": "Two-Color", "one-color": "One-Color"}


def housing_manifest_a():
    m = json.load(open(os.path.join(TOPICS, "20261110_Stage-C-Housing-Manifest.json"), encoding="utf-8"))
    return next(o for o in m["options"] if o["option"] == "A")


def housing_desc():
    h = HOUSING
    return (f"Oath & Action Civic Line {h['id']} {h['label']}. {h['shows']} The final drawing, approved by name on "
            f"drawings board C as option A ({h['dr']}) and put into use on November 11, 2026. A new topic drawing, "
            f"numbered CL-075 (D2-1262) and filed with sheet 03, Economy & Public Issues. It is set at 48 px and up "
            f"and stays off the list of drawings set at 24 px (D2-1238). Drawn in Civic Line's hand: one line weight, "
            f"round caps and joins, the capped fit of DR-08. The group with data-part 'base' is the main drawing; the "
            f"group with data-part 'accent' holds the accent parts, red in the two-color editions. Every id in the "
            f"file starts with the file's root id.")


def housing_final():
    h = HOUSING
    opt = read(PROMO.option_file(h, "red-black"))
    t = opt.replace(S.root_id_of(opt), C.bare_root(h["id"], "red-black"))
    t = re.sub(r'(<svg\b[^>]*?\sdata-id=")[^"]*(")', lambda m: m.group(1) + h["id"] + m.group(2), t, count=1)
    assert len(TITLE_RE.findall(t)) == 1 and len(DESC_RE.findall(t)) == 1
    t = TITLE_RE.sub(lambda m: f"<title>{escape(h['label'])}</title>", t, count=1)
    t = DESC_RE.sub(lambda m: f"<desc>{escape(housing_desc())}</desc>", t, count=1)
    return S.derive_editions(t)


def housing_name(ed, ext="svg"):
    return f"{DATE}_Oath-And-Action-Civic-Line-CL-075-Housing-{C.EDITIONS[ed]['suffix']}.{ext}"


def housing_tile_base(sh, tl, md):
    return f"{DATE}_Oath-And-Action-Civic-Line-CL-075-Housing-Tile-{TILE_SHAPE[sh]}-{tl.capitalize()}-{TILE_MODE[md]}"


def option_tile_base(sh, tl, md):
    return f"20261110_Housing-Option-A-Tile-{sh.capitalize()}-{tl.capitalize()}-{md.title().replace(' ', '-')}"


def housing_setup(scratch, need_stroke=True):
    """Labels, final texts, optics, bake and stroke measures; sets CL-075's tile optics and floor in this process."""
    h = dict(HOUSING)
    a_opt = housing_manifest_a()
    h.update(construction=a_opt["construction"], red=a_opt["red"])
    h["eds"] = housing_final()
    median = PROMO.hull_median(PROMO.october_inventory()["icons"])
    a, dx, rule = PROMO.optics_rule(h["eds"]["red-black"], median)
    h.update(a=a, dx=dx, rule=rule, median=median, option_optics=a_opt["tile_optics"])
    src = B.parse(h["src_id"], read(PROMO.option_src(h)))
    h.update(src=src, bake=B.bake(src))
    if need_stroke:
        h["stroke8"], h["stroke1"], _ = PROMO.stroke_on_source(h, scratch)
    PROMO.set_final_optics({h["id"]: (a, dx, h["floor32"])})
    return h


def tile_row(h):
    return {"id": h["id"], "label": h["label"], "stroke_units": round(h["bake"]["stroke_units"], 4)}


def build_housing(scratch):
    h = housing_setup(scratch, need_stroke=False)
    jobs = []
    for ed in EDITIONS:
        write(os.path.join(V6, ed, housing_name(ed)), h["eds"][ed])
        for px in (256, 512):
            jobs.append({"svg": PROMO.sized(h["eds"][ed], px), "w": px, "h": px, "bg": None,
                         "out": os.path.join(V6, f"png-{px}", ed, housing_name(ed, "png"))})
    for sh in C.TILE_SHAPES:
        for tl in C.TILE_COLOURS:
            for md in C.TILE_MODES:
                svg = T.tile_svg(h["eds"][C.TILE_EDITION[(tl, md)]], tile_row(h), sh, tl, md)
                base = housing_tile_base(sh, tl, md)
                write(os.path.join(V6, "tiles", f"{sh}-{tl}", "svg", base + ".svg"), svg)
                for px in (256, 512):
                    jobs.append({"svg": PROMO.sized(svg, px), "w": px, "h": px, "bg": None, "tile": True,
                                 "out": os.path.join(V6, "tiles", f"{sh}-{tl}", f"png-{px}", base + ".png")})
    PROMO.render([{k: v for k, v in j.items() if k != "tile"} for j in jobs], scratch)
    for j in jobs:      # tiles are re-saved as the October build and the option's tiles were: RGBA, recompressed
        if j.get("tile"):
            Image.open(j["out"]).convert("RGBA").save(j["out"], optimize=True)
    print(f"housing: 4 SVGs, 8 PNGs, 12 tile SVGs and 24 tile PNGs for CL-075 in {rel(V6)}")


def housing_tile_revert(text):
    t = text.replace("oa-civic-line-cl-075-tile-", "oa-civic-line-housing-option-a-tile-")
    t = t.replace('data-id="CL-075"', 'data-id="Housing-Option-A"', 1)
    return t.replace("Oath &amp; Action Civic Line CL-075 Housing:", "Oath &amp; Action Civic Line Housing-Option-A Housing:", 1)


def check_housing(res, errs, scratch):
    h = housing_setup(scratch, need_stroke=False)
    r = {"editions": {}, "tiles": {"svg": 0, "png": 0, "png_equal_option": 0}, "optics": {
        "a": h["a"], "dx": h["dx"], "option_a": h["option_optics"]["a"], "option_dx": h["option_optics"]["dx"],
        "rule": h["rule"], "hull_median_units": round(h["median"], 3)}}
    if (h["a"], h["dx"]) != (h["option_optics"]["a"], h["option_optics"]["dx"]):
        errs.append("CL-075: tile optics differ from the option's")
    for ed in EDITIONS:
        p = os.path.join(V6, ed, housing_name(ed))
        if not os.path.exists(p):
            errs.append(f"CL-075 {ed}: missing")
            continue
        text = read(p)
        back = PROMO.revert_final(h, ed, text)
        opt = PROMO.option_file(h, ed)
        same = back.encode("utf-8") == open(opt, "rb").read()
        x = {"sha256": sha(p), "option_file": rel(opt), "option_sha256": sha(opt), "reverts_to_option_byte_for_byte": same}
        if not same:
            errs.append(f"CL-075 {ed}: does not revert to option A's file")
        e2 = []
        V.check_svg(p, ed, e2, h["id"])
        errs += e2
        x["verify_set_check_svg_errors"] = len(e2)
        if ed != "red-black":
            ok, n, swaps, why = V.tree_identity(os.path.join(V6, "red-black", housing_name("red-black")), p, ed)
            x["tree_identity"] = {"ok": ok, "elements": n, "color_swaps": swaps}
            if not ok:
                errs.append(f"CL-075 {ed}: tree identity fails: {why}")
        if 'data-id="CL-075"' not in text or "<title>Housing</title>" not in text or "DR-207" not in text:
            errs.append(f"CL-075 {ed}: data-id, title or DR missing")
        for px in (256, 512):
            pp = os.path.join(V6, f"png-{px}", ed, housing_name(ed, "png"))
            e2 = []
            V.check_png(pp, px, e2)
            errs += e2
            if px == 256:   # the option's -2x preview is the same drawing at 256 px, by the same renderer
                op = os.path.join(TOPICS, "png", f"{h['stem']}-{C.EDITIONS[ed]['suffix']}-2x.png")
                ok = same_pixels(pp, op)
                x["png_256_equals_option_2x_preview"] = ok
                if not ok:
                    errs.append(f"CL-075 {ed}: the 256 px preview differs from the option's")
        r["editions"][ed] = x
    # the drawing behind the transform: option A's source re-bakes to its red-black file
    opt_rb = read(PROMO.option_file(h, "red-black"))
    oroot = ET.fromstring(opt_rb.split("?>", 1)[-1].encode())
    otitle = next(e.text for e in oroot if V.strip(e.tag) == "title")
    odesc = next(e.text for e in oroot if V.strip(e.tag) == "desc")
    rb, _ = B.export(h["src"], h["bake"], S.root_id_of(opt_rb)[:-len("-red-black")], otitle, odesc)
    r["source_rebakes_to_option"] = rb == opt_rb
    if rb != opt_rb:
        errs.append("CL-075: option A's source does not re-bake to its red-black file")
    # tiles
    trow = {**tile_row(h), "tile_stroke_units": round(min(h["bake"]["stroke_units"] * h["a"], C.TILE_STROKE_CAP), 4)}
    margins = {}
    for sh in C.TILE_SHAPES:
        margins[sh] = round(T.icon_margin(h["eds"]["red-black"], sh, C.TILE_FACTORS[sh], *C.tile_optics(h["id"], trow["stroke_units"])), 3)
        if margins[sh] < C.TILE_SAFE_MARGIN:
            errs.append(f"CL-075: ink {margins[sh]} units from the {sh} edge")
        for tl in C.TILE_COLOURS:
            for md in C.TILE_MODES:
                ed = C.TILE_EDITION[(tl, md)]
                bare = ET.parse(os.path.join(V6, ed, housing_name(ed))).getroot()
                bare_tree = [k for k in bare if V.strip(k.tag) not in ("title", "desc")]
                base = housing_tile_base(sh, tl, md)
                p = os.path.join(V6, "tiles", f"{sh}-{tl}", "svg", base + ".svg")
                if not os.path.exists(p):
                    errs.append(f"CL-075 tile missing: {base}")
                    continue
                e2 = []
                if V.check_tile(p, trow, sh, tl, md, bare_tree, bare.attrib["id"], e2):
                    r["tiles"]["svg"] += 1
                errs += e2
                op = os.path.join(TOPICS, "tiles", f"{sh}-{tl}", "svg", option_tile_base(sh, tl, md) + ".svg")
                if housing_tile_revert(read(p)).encode("utf-8") != open(op, "rb").read():
                    errs.append(f"CL-075 tile {base}: does not revert to option A's tile")
                else:
                    r["tiles"].setdefault("svg_revert_to_option", 0)
                    r["tiles"]["svg_revert_to_option"] += 1
                for px in (256, 512):
                    pp = os.path.join(V6, "tiles", f"{sh}-{tl}", f"png-{px}", base + ".png")
                    e2 = []
                    V.check_png(pp, px, e2, opaque_corners=(sh == "square"), centre_opaque=True)
                    errs += e2
                    r["tiles"]["png"] += 0 if e2 else 1
                    opp = os.path.join(TOPICS, "tiles", f"{sh}-{tl}", f"png-{px}", option_tile_base(sh, tl, md) + ".png")
                    if same_pixels(pp, opp):
                        r["tiles"]["png_equal_option"] += 1
                    else:
                        errs.append(f"CL-075 tile {base} {px}: pixels differ from option A's tile")
    r["tiles"]["margins_units"] = margins
    if r["tiles"]["svg"] != 12 or r["tiles"]["png"] != 24:
        errs.append(f"CL-075: {r['tiles']['svg']} of 12 tile SVGs and {r['tiles']['png']} of 24 tile PNGs pass")
    res["housing"] = r
    print(f"housing: editions revert {[r['editions'][e]['reverts_to_option_byte_for_byte'] for e in EDITIONS if e in r['editions']]}, "
          f"re-bake {r['source_rebakes_to_option']}, tiles {r['tiles']}, optics a {h['a']} dx {h['dx']}")


# ================================================================== the inventory's 125th row

def housing_row(h):
    old_date = PROMO.DATE
    PROMO.DATE = DATE           # the row's file names carry this promotion's date (D2-1263)
    try:
        row = PROMO.final_row(h, None)
    finally:
        PROMO.DATE = old_date
    fin = row["final"]
    fin["approved"] = "DR-207, option A, approved by name on drawings board C, November 10, 2026"
    fin["option_stem"] = h["stem"]
    fin["new_id"] = "D2-1262: the next topic number after CL-074"
    fin["measured_on"] = ("No supplied sheet exists for this drawing, so the sheet fields (sheet_black, sheet_red, "
                          "crop, registration, sheet_iou, mask_params, reference_crops, components, caption_check) are "
                          "null. The stroke medians are the October estimators (stroke_width.py) run on the drawing's "
                          "own source, built with the stage B family code and rendered black at 1x on Newsprint; the "
                          "transform is that code's bake (DR-08), which re-bakes to the option file byte for byte.")
    fin["reads_at_px"] = {"32": None, "24": False,
                          "reader": "The tiles keep the 48 px bare floor (D2-1236), since no 32 px reading is "
                                    "approved for Housing. The icon designer, an agent, read option A at 24 px on 1x "
                                    "screens as two buildings whose windows close up (round 0 notes), and Housing "
                                    "stays off the list of drawings set at 24 px (D2-1238)."}
    fin["sizes"] = "48 px and up (DR-207, D2-1238)"
    return row


def check_roundtrip():
    """The inventory's JSON and CSV as they stand rewrite byte for byte, so rewriting them changes only the new row."""
    j = json.load(open(INV_JSON, encoding="utf-8"))
    buf = io.StringIO()
    json.dump(j, buf, indent=2, ensure_ascii=False, default=C._np_default)
    buf.write("\n")
    jok = buf.getvalue().encode("utf-8") == open(INV_JSON, "rb").read()
    cbuf = io.StringIO(newline="")
    w = csv.writer(cbuf)
    w.writerow(PROMO.CSV_FIELDS)
    for r in j["icons"]:
        w.writerow(PROMO.csv_row(r))
    cok = cbuf.getvalue().encode("utf-8") == open(INV_CSV, "rb").read()
    return jok, cok


def build_inventory(scratch):
    h = housing_setup(scratch)
    inv = json.load(open(INV_JSON, encoding="utf-8"))
    rows = [r for r in inv["icons"] if r["id"] != "CL-075"]
    if len(rows) != 124:
        raise SystemExit(f"inventory holds {len(rows)} rows besides CL-075, expected 124")
    k = next(n for n, r in enumerate(rows) if r["id"] == "CL-072")
    rows.insert(k + 1, housing_row(h))
    counts, by_source = {}, {}
    for r in rows:
        counts[r["sheet"]] = counts.get(r["sheet"], 0) + 1
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    strokes = [r["stroke_units"] for r in rows]
    out = {}
    for key, v in inv.items():      # keep the file's own key order, with its fields brought up to date
        out[key] = v
        if key == "date":
            out["updated"] = DATE
    out["count"] = len(rows)
    out["counts_by_sheet"] = dict(sorted(counts.items()))
    out["counts_by_source"] = by_source
    out["decisions"] = {**inv["decisions"], "finals": "DR-156 to DR-160, DR-207",
                        "new_ids": "D2-714 (CL-073, CL-074), D2-1262 (CL-075)"}
    out["layout"] = ("The four SVG editions of all 125 drawings sit in this folder. PNG previews and tiles sit here for "
                     "the nine finals only; the 116 unchanged rows point at their October PNGs and tiles in "
                     "../civic-line/ (D2-716). A row's PNG is <png_256_dir>/<edition>/<png name>, its tiles "
                     "<tiles_dir>/<shape>-<tile>/svg|png-256|png-512/<tile name>. The 24 px fits of the 37 sit in "
                     "fit-24/ with their own manifest (D2-1265).")
    out["order"] = ("The October order, with each final in its original's place, CL-073 and CL-074 after CL-024 at the "
                    "end of sheet 01 (D2-714), and CL-075 after CL-072 at the end of sheet 03 (D2-1262).")
    out["stroke_width_units"] = [min(strokes), max(strokes)]
    tr = copy.deepcopy(inv["tiles_rule"])
    tr["finals"] = inv["tiles_rule"]["finals"] + (
        f" CL-075 Housing (DR-207) takes the same rules: optical scale {h['a']} and offset {h['dx']} by the same form, "
        "and its tiles on the 48 px bare floor (D2-1236).")
    out["tiles_rule"] = tr
    out["icons"] = rows
    C.write_json(INV_JSON, out)
    with open(INV_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(PROMO.CSV_FIELDS)
        for r in rows:
            w.writerow(PROMO.csv_row(r))
    print(f"inventory: {len(rows)} rows, CL-075 after CL-072 (sheet 03, row 5, column 1)")


def check_inventory(res, errs):
    inv = json.load(open(INV_JSON, encoding="utf-8"))
    csv_rows = list(csv.reader(open(INV_CSV, encoding="utf-8")))
    r = {"json_rows": len(inv["icons"]), "csv_rows": len(csv_rows) - 1}
    if len(inv["icons"]) != 125 or len(csv_rows) != 126:
        errs.append(f"inventory: {len(inv['icons'])} JSON rows and {len(csv_rows) - 1} CSV rows, expected 125")
    ids = [x["id"] for x in inv["icons"]]
    if len(set(ids)) != len(ids):
        errs.append("inventory ids repeat")
    hj, hc = head_bytes(INV_JSON), head_bytes(INV_CSV)
    if hj is not None:
        old = json.loads(hj.decode("utf-8"))["icons"]
        new = [x for x in inv["icons"] if x["id"] != "CL-075"]
        r["other_rows_equal_head"] = old == new
        if old != new:
            errs.append("inventory: a row other than CL-075 changed against git HEAD")
        oc = hc.decode("utf-8").split("\r\n")
        nc = open(INV_CSV, encoding="utf-8", newline="").read().split("\r\n")
        nc_wo = [line for line in nc if not line.startswith("CL-075,")]
        r["other_csv_lines_equal_head"] = oc == nc_wo
        if oc != nc_wo:
            errs.append("inventory CSV: a line other than CL-075's changed against git HEAD")
    k = ids.index("CL-075") if "CL-075" in ids else -1
    r["cl_075_position"] = {"index": k, "after": ids[k - 1] if k > 0 else None, "before": ids[k + 1] if 0 <= k < len(ids) - 1 else None}
    if k < 1 or ids[k - 1] != "CL-072":
        errs.append("inventory: CL-075 does not follow CL-072")
    empty = [(x[0], PROMO.CSV_FIELDS[n]) for x in csv_rows[1:] for n, v in enumerate(x) if v == "" and PROMO.CSV_FIELDS[n] != "flags"]
    r["csv_empty_cells_outside_flags"] = len(empty)
    if empty:
        errs.append(f"inventory CSV: {len(empty)} empty cells, first {empty[:3]}")
    missing, n = [], 0
    for x in inv["icons"]:
        for p in x["exports"]["paths"] + x["tiles"] + x["tile_pngs"] + [x["source_file"]]:
            n += 1
            if not os.path.exists(os.path.normpath(os.path.join(V6, p))):
                missing.append(p)
    r["paths_checked"], r["paths_missing"] = n, len(missing)
    if missing:
        errs.append(f"inventory names {len(missing)} missing files, first {missing[:3]}")
    hrow = inv["icons"][k] if k >= 0 else {}
    r["cl_075"] = {key: hrow.get(key) for key in ("label", "slug", "sheet", "row", "column", "source", "source_file",
                                                   "status", "stroke_units", "stroke_median_px", "stroke_median_1x_px",
                                                   "tile_optical_scale", "tile_offset_x", "tile_min_px")}
    if hrow.get("source") != "DR-207":
        errs.append("inventory: CL-075's source is not DR-207")
    for ed in EDITIONS:
        if hrow.get("sha256", {}).get(ed) != sha(os.path.join(V6, ed, housing_name(ed))):
            errs.append(f"inventory: CL-075's {ed} hash is out of date")
    for ed in EDITIONS:
        n_ed = len([x for x in os.listdir(os.path.join(V6, ed)) if x.endswith(".svg")])
        r.setdefault("edition_counts", {})[ed] = n_ed
        if n_ed != 125:
            errs.append(f"{ed}: {n_ed} SVGs, expected 125")
    res["inventory"] = r
    print(f"inventory: {r['json_rows']} JSON rows, {r['csv_rows']} CSV rows, CL-075 at {r['cl_075_position']}, "
          f"other rows as in HEAD: {r.get('other_rows_equal_head')} / {r.get('other_csv_lines_equal_head')}, "
          f"{r['paths_checked']} paths, {r['paths_missing']} missing")


# ================================================================== utility at 16 px (DR-208, D2-1264)

UTIL_PICKS = [
    dict(name="Pause", icon="U-pause", src="20261110_Utility-Pause-16px-Redraw.svg", old_dr="DR-171",
         drawing="Two upright bars, each 5 px wide, so its inside keeps one whole open pixel on 1x screens",
         approved="the 16 px Pause redraw"),
    dict(name="Filter", icon="U-filter", src="20261110_Utility-Filter-16px-Redraw-A.svg", old_dr="DR-169",
         drawing="A funnel with a slanted spout, the spout 5 px wide with both outer edges on whole pixels, so its "
                 "inside keeps one whole open pixel on 1x screens",
         approved="Filter option A"),
]


def util_paths(p):
    old = f"20261110_Utility-{p['name']}-16px"
    new = f"{DATE}_Utility-{p['name']}-16px"
    return {
        "src": os.path.join(UTIL_IN, "svg", p["src"]),
        "src_png": (os.path.join(UTIL_IN, "png", p["src"][:-4] + ".png"), os.path.join(UTIL_IN, "png", p["src"][:-4] + "-2x.png")),
        "out": os.path.join(UTIL, "svg-16", new + ".svg"),
        "png": (os.path.join(UTIL, "png", new + ".png"), os.path.join(UTIL, "png", new + "-2x.png")),
        "old": os.path.join(UTIL, "svg-16", old + ".svg"),
        "old_png": (os.path.join(UTIL, "png", old + ".png"), os.path.join(UTIL, "png", old + "-2x.png")),
        "arch": os.path.join(UTIL, "_archive", "svg-16", old + ".svg"),
        "arch_png": (os.path.join(UTIL, "_archive", "png", old + ".png"), os.path.join(UTIL, "_archive", "png", old + "-2x.png")),
    }


def util_comment(p):
    return (f"  <!-- Oath & Action utility icon: {p['name']}, 16 px master, final. {p['drawing']}. 16-unit grid, 1.5 px "
            f"line, round caps and joins, currentColor, no red. The final approved on drawings board C: Dustin approved "
            f"{p['approved']} by name on November 10, 2026 (DR-208), and it went into use on November 11, 2026. Its "
            f"drawing is the approved file, {p['src']}, unchanged. It replaces the stage B final ({p['old_dr']}), which "
            f"stays as the record in utility/_archive/svg-16/ (D2-1264). -->")


def git_mv(src, dst):
    if os.path.exists(dst) and not os.path.exists(src):
        return "already moved"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(["git", "mv", src, dst], cwd=ROOT, check=True)
    return "moved"


def build_utility(scratch):
    jobs = {"ink": UP.INK, "previews": []}
    for p in UTIL_PICKS:
        q = util_paths(p)
        root, _, drawing = UP.split(read(q["src"]))
        write(q["out"], root + "\n" + util_comment(p) + "\n" + drawing)
        for scale, out in zip((1, 2), q["png"]):
            jobs["previews"].append({"svg": q["out"], "size": 16, "scale": scale, "out": out})
    UP.run_node(jobs, os.path.join(scratch, "utility-render"))
    moves = []
    for p in UTIL_PICKS:
        q = util_paths(p)
        moves.append((rel(q["old"]), git_mv(q["old"], q["arch"])))
        for a, b in zip(q["old_png"], q["arch_png"]):
            moves.append((rel(a), git_mv(a, b)))
    write_util_manifest()
    print(f"utility: 2 SVGs and 4 PNGs written; moves: {moves}")


def write_util_manifest():
    m = json.load(open(UTIL_MANIFEST, encoding="utf-8"))
    for p in UTIL_PICKS:
        q = util_paths(p)
        icon = next(x for x in m["icons"] if x["id"] == p["icon"])
        old = icon["sizes"]["16"]
        prev = old.get("replaces") or {"dr": p["old_dr"], "svg": rel(q["arch"]), "png_1x": rel(q["arch_png"][0]),
                                        "png_2x": rel(q["arch_png"][1]), "source": old["source"],
                                        "sha256": old["sha256"], "drawing_sha256": old["drawing_sha256"]}
        _, _, drawing = UP.split(read(q["out"]))
        icon["sizes"]["16"] = {
            "svg": rel(q["out"]), "png_1x": rel(q["png"][0]), "png_2x": rel(q["png"][1]),
            "line_px": 1.5, "sprite_symbol_id": f"oa-sym-{p['icon'].lower()}-16px",
            "source": rel(q["src"]), "source_sha256": sha(q["src"]), "sha256": sha(q["out"]),
            "drawing_sha256": sha(drawing.encode("utf-8")),
            "approved": {"what": p["approved"], "dr": "DR-208", "redraw_dr": "DR-197",
                         "board": "Drawings board C, approved by name", "date": "2026-11-10", "in_use": "2026-11-11",
                         "drawing": p["drawing"]},
            "replaces": prev,
        }
    m["updated"] = "2026-11-11"
    m["updates"] = [{"date": "2026-11-11", "dr": "DR-208",
                     "what": "The 16 px Pause and Filter are drawings board C's approved redraws (the Pause redraw and "
                             "Filter option A). The stage B 16 px files and their previews moved to _archive/ (D2-1264), "
                             "so svg-16/ and png/ hold one file per icon and size. Every 24 px file and every other "
                             "16 px file stays as approved."}]
    keys = list(m.keys())
    order = [k for k in keys if k not in ("updated", "updates", "icons")]
    out = {}
    for k in order:
        out[k] = m[k]
        if k == "date":
            out["updated"] = m["updated"]
    out["updates"] = m["updates"]
    out["icons"] = m["icons"]
    with open(UTIL_MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def check_utility(res, errs):
    r = {"files": {}}
    for p in UTIL_PICKS:
        q = util_paths(p)
        x = {}
        if not os.path.exists(q["out"]):
            errs.append(f"utility {p['name']}: missing")
            continue
        froot, fcom, fdraw = UP.split(read(q["out"]))
        sroot, _, sdraw = UP.split(read(q["src"]))
        x["sha256"], x["source_sha256"] = sha(q["out"]), sha(q["src"])
        x["drawing_equal"] = fdraw == sdraw
        x["root_tag_equal"] = froot == sroot
        x["drawing_sha256"] = sha(fdraw.encode("utf-8"))
        x["elements_equal"] = UP.elements(read(q["out"]))[1] == UP.elements(read(q["src"]))[1]
        a = UP.attrs(froot)
        x["root"] = {k: a.get(k) for k in ("data-icon", "data-icon-family", "data-size", "aria-hidden", "focusable")}
        if not (x["drawing_equal"] and x["root_tag_equal"] and x["elements_equal"]):
            errs.append(f"utility {p['name']}: the final's drawing or root tag differs from the approved redraw")
        if a.get("data-icon") != p["icon"] or a.get("data-icon-family") != "utility" or a.get("data-size") != "16" or "data-option" in a:
            errs.append(f"utility {p['name']}: root attributes wrong")
        if "DR-208" not in fcom or "--" in fcom[6:-5]:
            errs.append(f"utility {p['name']}: comment line wrong")
        for out, src, k in zip(q["png"], q["src_png"], ("png_1x", "png_2x")):
            ok = os.path.exists(out) and same_pixels(out, src)
            x[k + "_equals_redraw_preview"] = ok
            if not ok:
                errs.append(f"utility {p['name']}: {k} differs from the approved redraw's preview")
        arch = {}
        for a_path, o_path in zip((q["arch"],) + q["arch_png"], (q["old"],) + q["old_png"]):
            hb = head_bytes(o_path) or head_bytes(a_path)
            ok = os.path.exists(a_path) and not os.path.exists(o_path) and hb is not None and sha(a_path) == sha(hb)
            arch[rel(a_path)] = {"sha256": sha(a_path) if os.path.exists(a_path) else None,
                                 "head_sha256": sha(hb) if hb else None, "moved_bytes_unchanged": ok}
            if not ok:
                errs.append(f"utility archive: {rel(a_path)} missing, left behind or changed")
        x["archive"] = arch
        r["files"][p["name"]] = x
    names = sorted(os.listdir(os.path.join(UTIL, "svg-16")))
    stems = [re.sub(r"^\d{8}_", "", n) for n in names]
    r["svg_16"] = {"files": len(names), "one_per_icon": len(set(stems)) == len(stems)}
    if len(names) != 18 or len(set(stems)) != 18:
        errs.append(f"utility svg-16: {len(names)} files, {len(set(stems))} icons; expected 18 and 18")
    pngs = sorted(os.listdir(os.path.join(UTIL, "png")))
    pstems = [re.sub(r"^\d{8}_", "", n) for n in pngs]
    r["png"] = {"files": len(pngs), "one_per_icon_size_scale": len(set(pstems)) == len(pstems)}
    if len(pngs) != 72 or len(set(pstems)) != 72:
        errs.append(f"utility png: {len(pngs)} files, {len(set(pstems))} distinct; expected 72")
    m = json.load(open(UTIL_MANIFEST, encoding="utf-8"))
    r["manifest_icons"] = len(m["icons"])
    for p in UTIL_PICKS:
        s16 = next(x for x in m["icons"] if x["id"] == p["icon"])["sizes"]["16"]
        q = util_paths(p)
        if s16["svg"] != rel(q["out"]) or s16["approved"]["dr"] != "DR-208" or s16["sha256"] != sha(q["out"]):
            errs.append(f"utility manifest {p['name']}: the 16 px row is not up to date")
    hb = head_bytes(UTIL_MANIFEST)
    if hb is not None:
        old = json.loads(hb.decode("utf-8"))
        changed = []
        for a, b in zip(old["icons"], m["icons"]):
            for size in ("24", "16"):
                if a["sizes"][size] != b["sizes"][size]:
                    changed.append(f"{a['id']} {size}")
            if {k: v for k, v in a.items() if k != "sizes"} != {k: v for k, v in b.items() if k != "sizes"}:
                changed.append(f"{a['id']} fields")
        r["manifest_changed_against_head"] = changed
        if sorted(changed) != sorted(["U-pause 16", "U-filter 16"]):
            errs.append(f"utility manifest: changed entries {changed}, expected the two 16 px rows only")
    res["utility"] = r
    print(f"utility: {json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'archive'} for k, v in r['files'].items()})}")
    print(f"utility: svg-16 {r['svg_16']}, png {r['png']}, manifest changes {r.get('manifest_changed_against_head')}")


# ================================================================== ids across the sets in use

def check_ids(res, errs):
    seen, dup, n_files, refs, unresolved = {}, [], 0, 0, []
    for top in (V6, os.path.join(ASSETS, "pillar-icons")):
        for d, _, files in os.walk(top):
            for nme in files:
                if not nme.endswith(".svg"):
                    continue
                p = os.path.join(d, nme)
                n_files += 1
                text = read(p)
                ids = re.findall(r'\sid="([^"]+)"', text)
                for i in ids:
                    if i in seen:
                        dup.append((i, rel(p), seen[i]))
                    else:
                        seen[i] = rel(p)
                own = set(ids)
                for ref in re.findall(r'(?:href|url\()\s*=?\s*"?#([^")\s]+)', text):
                    refs += 1
                    if ref not in own:
                        unresolved.append((rel(p), ref))
    res["ids"] = {"files": n_files, "ids": len(seen), "repeats": len(dup), "references": refs, "unresolved": len(unresolved)}
    if dup:
        errs.append(f"ids repeat across the sets in use: {dup[:3]}")
    if unresolved:
        errs.append(f"references that do not resolve: {unresolved[:3]}")
    print(f"ids: {res['ids']}")


# ================================================================== main

def run_checks(scratch, parts):
    res, errs = {"date": DATE}, []
    if "fits" in parts:
        check_fits(res, errs)
    if "housing" in parts:
        check_housing(res, errs, scratch)
    if "inventory" in parts:
        check_inventory(res, errs)
    if "utility" in parts:
        check_utility(res, errs)
    check_ids(res, errs)
    res["errors"] = errs
    os.makedirs(scratch, exist_ok=True)
    out = os.path.join(scratch, f"{DATE}_Promotion-C-Icons-Checks.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    print(f"checks written to {out}")
    print(f"{len(errs)} errors" + ("" if not errs else ":\n  " + "\n  ".join(errs[:40])))
    return 1 if errs else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=["fits", "housing", "inventory", "utility"])
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--scratch", default=SCRATCH)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    parts = [a.part] if a.part else ["fits", "housing", "inventory", "utility"]
    if not a.check_only:
        for part in parts:
            {"fits": build_fits, "housing": build_housing, "inventory": build_inventory, "utility": build_utility}[part](a.scratch)
    sys.exit(run_checks(a.scratch, parts))


if __name__ == "__main__":
    main()
