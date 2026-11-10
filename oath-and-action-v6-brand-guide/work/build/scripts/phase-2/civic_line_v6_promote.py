#!/usr/bin/env python3
"""Promote the approved stage B Civic Line drawings and pillar fits into the sets in use (November 10, 2026).

    python3 -I work/build/scripts/phase-2/civic_line_v6_promote.py [--scratch DIR]
    python3 -I work/build/scripts/phase-2/civic_line_v6_promote.py --check-only [--scratch DIR]

The task is item 1 of work/handoffs/phase-2/20261110_Promotion-Brief.md. Decisions: DR-156 to DR-160 and DR-179
(the picks), D2-714 (CL-073 and CL-074), D2-716 (what the folder holds), DR-09 (light editions), DR-10 (tiles),
DR-08 (framing), D2-497 (the black edition under 48 px), D2-634 (16 px on 2x screens).

It writes
  work/build/assets/civic-line-v6/
    red-black/ black/ red-newsprint/ newsprint/   124 SVGs each: the 116 unchanged October masters copied byte for
                                                   byte under their October names, and the 8 finals, named
                                                   20261110_Oath-And-Action-Civic-Line-<ID>-<Slug>-<Edition>.svg
    png-256/<edition>/ png-512/<edition>/          the 8 finals' previews, in the October layout
    tiles/<shape>-<tile>/svg|png-256|png-512/      the 8 finals' 12 tiles each, by the October tile code
    20261110_Civic-Line-V6-Inventory.csv, .json    124 rows; paths are relative to the inventory's own folder
  work/build/assets/pillar-icons/
    svg/ png/ 20261110_Pillar-Icons-Manifest.json  the 24 px fit B and 16 px fit A of the four pillar icons

How a final is made. It is its approved option file with only the root id (and the ids that start with it),
data-id, title and desc changed (and, for a pillar icon, data-size added). The Newsprint and Red-Newsprint
editions come from the red-black final by the October color swap (cl_svg.derive_editions, DR-09). PNGs are drawn
by the October renderer (render_svgs.js). Tiles come from cl_tiles.tile_svg. The eight finals' tile optical scale
and offset come from the variant review's S-1 and S-2 rules (work/handoffs/phase-2/20261029_Civic-Line-Variant-
Review.md), measured on the build's own vector hull (cl_tiles.hull_size), and their bare floor (32 or 48 px) from
reading each final at 32 px, as the October review's section 6 did. These values are set in this process only:
cl_common.py on disk is unchanged.

Checks (run after every build, and alone with --check-only); the script exits 1 on any failure:
  copies   every unchanged SVG hashes the same as its October file (464 files)
  finals   each final, with its root id, data-id, title and desc put back, equals its approved option file byte for
           byte (red-black and black); each light edition equals the October swap of the option's red-black file;
           the stage B source re-bakes to the option file byte for byte (so the inventory's transform is the
           drawing's); the October structure checks (verify_set.check_svg) and edition tree identity
  tiles    verify_set.check_tile on all 96 tile SVGs, ink at least 12 units from every tile edge, PNG sizes and modes
  rules    the S-1 and S-2 rules as applied here, recomputed on the 122 October masters, against the review's table
  counts   124 per edition folder, 124 inventory rows, 16 pillar SVGs and 32 PNGs, ids unique within each file
  pillar   each pillar final, with its ids, title, desc and data-size put back, equals its fit file byte for byte;
           its PNGs equal the fit's stage B PNGs pixel for pixel
"""
import argparse
import copy
import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CL_SCRIPTS = os.path.join(ROOT, "work", "build", "scripts", "civic-line")
sys.path.insert(0, CL_SCRIPTS)
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import cl_common as C  # noqa: E402
import cl_svg as S  # noqa: E402
import cl_tiles as T  # noqa: E402
import stroke_width as SW  # noqa: E402
import verify_set as V  # noqa: E402
import civic_line_stage_b_common as B  # noqa: E402

DATE = "20261110"
ASSETS = os.path.join(ROOT, "work", "build", "assets")
OCT = os.path.join(ASSETS, "civic-line")
V6 = os.path.join(ASSETS, "civic-line-v6")
PILLAR = os.path.join(ASSETS, "pillar-icons")
FITS = os.path.join(ASSETS, "pillar-pixel-fit")
INV_CSV = os.path.join(V6, f"{DATE}_Civic-Line-V6-Inventory.csv")
INV_JSON = os.path.join(V6, f"{DATE}_Civic-Line-V6-Inventory.json")
PILLAR_MANIFEST = os.path.join(PILLAR, f"{DATE}_Pillar-Icons-Manifest.json")
SCRATCH = "/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/promotion/civic-line"
EDITIONS = list(C.EDITIONS)            # red-black, black, red-newsprint, newsprint
UNCHANGED = "October master, unchanged"
SHAPE_NAME = {"square": "Square", "rounded": "Rounded", "circle": "Circle"}
MODE_NAME = {"two-color": "Two-Color", "one-color": "One-Color"}

# ---------------------------------------------------------------- the eight finals
# shows: what the drawing shows, from the approving DR. floor32: whether the subject still reads at 32 px, my
# reading of each final at 32 px true size and enlarged (as the October review's section 6 read the 122).
FINALS = [
    dict(id="CL-025", folder="civic-line-redraws", stem="20261109_CL-025-Congress-Option-B", dr="DR-156", pick="set B",
         shows="The House chamber in session, seen from the gallery: five members on the near bench seen from behind, "
               "a far bench in five sections, and a three-tier rostrum whose top tier is red.",
         construction="the House chamber seen from the gallery. A near bench curves up at both ends and holds five "
                      "members seen from behind, each a hollow head over open, round-cornered shoulders. A far bench "
                      "in five short sections curves round a rostrum about a third of the drawing's width, stepped in "
                      "three tiers. The bench sections leave no center aisle. No dome, column or flag.",
         red="the rostrum's top tier, where the Speaker sits. The benches, the members and the two lower tiers stay "
             "black.", floor32=True),
    dict(id="CL-014", folder="civic-line-redraws", stem="20261109_CL-014-Entrenched-Power-Option-C", dr="DR-156",
         pick="option C",
         shows="A ballot's arrow runs at the fenced chamber and stops at the fence on a red bar, so an election cannot "
               "move the body.",
         construction="at left a square ballot with a check mark; a short arrow runs from it to an upright bar at "
                      "the fence. At right set B's chamber with a two-tier rostrum and its members, inside an oval "
                      "fence with three pickets a side at the front and none behind. No dome, spire or column.",
         red="the bar at the fence where the ballot's arrow stops. The ballot, the arrow, the fence and the chamber "
             "stay black.", floor32=False),
    dict(id="R-13", folder="civic-line-redraws", stem="20261109_R-13-Congressional-Capacity-Option-B", dr="DR-156",
         pick="set B",
         shows="The House chamber in session, seen from the gallery, above two staff and an analyst's report whose "
               "chart line is red.",
         construction="set B's chamber on a top tier at three quarters of CL-025's size: the three-tier rostrum, the "
                      "far bench in sections and the near bench with five members. Below it at left two staff, each "
                      "a hollow head over open shoulders, and at right an analyst's report: an upright page with two "
                      "text lines and a rising chart line. No dome, column or book.",
         red="the chart line on the analyst's report. The chamber, the two staff and the report's frame stay black.",
         floor32=False),
    dict(id="R-42", folder="civic-line-redraws", stem="20261109_R-42-Congressional-Tariff-Votes-Option-B", dr="DR-156",
         pick="set B",
         shows="The House chamber in session, seen from the gallery, above a red vote card with a yes and a no and a "
               "parcel with a tag for imports.",
         construction="set B's chamber on a top tier at three quarters of CL-025's size. Below it at left an upright "
                      "vote card holding a yes, drawn as a check, above a no, drawn as a cross; at right CL-064's "
                      "parcel, a box drawn in perspective with a taped top, and a tag hanging at its side. No dome, "
                      "column or ballot box.",
         red="the vote card with its yes and its no. The chamber, the parcel and its tag stay black.", floor32=False),
    dict(id="CL-059", folder="civic-line-redraws", stem="20261109_CL-059-Credit-Allocation-Option-B", dr="DR-157",
         pick="option B",
         shows="A flat-roofed bank with a round vault door on its face, above the red path that branches to a home "
               "and a factory.",
         construction="a flat-roofed bank: a square front between a roof line and a base line that both run past "
                      "its walls, with a round vault door on its face. The door has a hub ring and four diagonal "
                      "spokes that run past the rim as handle ends. Below, a path leaves the bank, splits in two and "
                      "runs down to a house at left and a factory with a saw-tooth roof and a chimney at right. No "
                      "pediment or column.",
         red="the branching path from the bank to the home and the factory. The bank, its vault door, the home and "
             "the factory stay black.", floor32=True),
    dict(id="R-48", folder="civic-line-redraws", stem="20261109_R-48-Agency-Independence-Option-C", dr="DR-158",
         pick="option C",
         shows="The commission at its table and the official at a desk, whose arrow stops at the red brace.",
         construction="at left a commission of three, each a hollow head over open shoulders, seated at one table on "
                      "two legs. At center a tall bracket that opens toward the commission, with a small nub on its "
                      "outer side. At right an official seated at a desk; an arrow runs left from the official and "
                      "stops at the bracket. No building, column or pediment.",
         red="the brace between the commission and the official. The commission, its table, the official, the desk "
             "and the arrow stay black.", floor32=False),
    dict(id="CL-073", folder="civic-line-new-topics", stem="20261109_Testify-Option-A", dr="DR-159", pick="option A",
         label="Testify", slug="Testify", sheet="01", row=5, column=1, src_id="Testify",
         construction="a raised, curved dais with three officials seen from the front above the witness, who sits "
                      "below at a table drawn as a top over a front panel, with an upright microphone (capsule, "
                      "holder, stem and base) on the table. No gavel, scales, robe, flag or nameplate letter.",
         shows="A raised, curved dais with three officials above the witness, who sits at a table with a red "
               "microphone.",
         red="the microphone on the witness table. The dais, the officials, the witness and the table stay black.",
         floor32=True),
    dict(id="CL-074", folder="civic-line-new-topics", stem="20261109_Contact-An-Official-Option-A", dr="DR-160",
         pick="option A", label="Contact an Official", slug="Contact-An-Official", sheet="01", row=5, column=2,
         src_id="Contact-An-Official",
         construction="a standing person at left and an official seated at a desk at right, joined by one level "
                      "line that carries a speech mark at its middle. The official wears no tie, and the two never "
                      "sit level across a table.",
         shows="A person and an official at a desk, joined by one line that carries a red speech mark.",
         red="the speech mark on the line. The person, the official, the desk and the line stay black.",
         floor32=False),
]
FINAL_IDS = [f["id"] for f in FINALS]


def option_file(f, ed):
    return os.path.join(ASSETS, f["folder"], "svg", f"{f['stem']}-{C.EDITIONS[ed]['suffix']}.svg")


def option_src(f):
    return os.path.join(ASSETS, f["folder"], "src", f"{f['stem']}.svg")


def final_name(f, ed, ext="svg"):
    return f"{DATE}_Oath-And-Action-Civic-Line-{f['id']}-{f['slug']}-{C.EDITIONS[ed]['suffix']}.{ext}"


def final_tile_name(f, shape, tile, mode):
    return f"{DATE}_Oath-And-Action-Civic-Line-{f['id']}-{f['slug']}-Tile-{SHAPE_NAME[shape]}-{tile.capitalize()}-{MODE_NAME[mode]}"


def sha(path_or_bytes):
    b = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    return hashlib.sha256(b).hexdigest()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def render(jobs, scratch):
    """The October renderer: one Chromium launch for the list."""
    if not jobs:
        return
    with tempfile.TemporaryDirectory(dir=scratch) as d:
        for k in range(0, len(jobs), 600):
            jp = os.path.join(d, "jobs.json")
            with open(jp, "w") as fh:
                json.dump(jobs[k:k + 600], fh)
            r = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
            if r.returncode:
                raise SystemExit("render failed:\n" + r.stderr[-2000:])


def sized(svg, px, base=128):
    body = svg.split("?>", 1)[-1].lstrip()
    return body.replace(f'width="{base}" height="{base}"', f'width="{px}" height="{px}"', 1)


TITLE_RE = re.compile(r"<title>.*?</title>", re.S)
DESC_RE = re.compile(r"<desc>.*?</desc>", re.S)


def root_of(text):
    return S.root_id_of(text)


# ---------------------------------------------------------------- inventory rows and optics

def october_inventory():
    with open(C.INVENTORY_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def hull_median(oct_rows):
    hs = [T.hull_size(open(C.edition_file(r, "red-black"), encoding="utf-8").read())[0] for r in oct_rows]
    return float(np.median(hs))


def optics_rule(rb_text, median):
    """S-1 and S-2 on the vector hull. S-1: a = clamp((median / hull) ** 0.5, 0.94, 1.10), rounded to 0.01, used
    where the unrounded value differs from 1 by 0.04 or more. S-2: 0.35 times the hull centroid's offset, in rounded
    tile units (box units times 0.66 times a), rounded to half a tile unit, capped at 2.5 and used from 1.5, toward
    the light side; stored in box units to 0.1. The median is the vector hull's own median over the 122 masters, the
    same measure as the hull it divides."""
    hs, hx, _ = T.hull_size(rb_text)
    raw = (median / hs) ** 0.5
    a = round(min(1.10, max(0.94, raw)), 2) if abs(raw - 1) >= 0.04 else 1.0
    f = C.TILE_FACTORS["rounded"]
    tile_units = math.floor(0.35 * abs(hx) * f * a * 2 + 0.5) / 2
    dx = 0.0
    if tile_units >= 1.5:
        dx = round(-math.copysign(min(tile_units, 2.5) / f, hx), 1)
    return a, dx, {"hull_size_units": round(hs, 2), "hull_centroid_offset_x_units": round(hx, 2),
                   "s1_unrounded": round(raw, 4), "s2_tile_units": tile_units}


def rule_reproduction(oct_rows, median):
    """The rules as applied here, on the 122 October masters, against the review's table in cl_common."""
    s1, s2 = [], []
    for r in oct_rows:
        i = r["id"]
        a, dx, m = optics_rule(open(C.edition_file(r, "red-black"), encoding="utf-8").read(), median)
        if i not in C.PILLAR_GROUP and abs(a - ORIG_OPT.get(i, 1.0)) > 1e-9:
            s1.append({"id": i, "rule": a, "table": ORIG_OPT.get(i, 1.0), "hull": m["hull_size_units"]})
        # S-2 is read with the table's own a, as the review measured it on tiles that carried it
        hx = m["hull_centroid_offset_x_units"]
        f = C.TILE_FACTORS["rounded"]
        tu = math.floor(0.35 * abs(hx) * f * ORIG_OPT.get(i, 1.0) * 2 + 0.5) / 2
        d2 = round(-math.copysign(min(tu, 2.5) / f, hx), 1) if tu >= 1.5 else 0.0
        if abs(d2 - ORIG_OFF.get(i, 0.0)) > 1e-9:
            s2.append({"id": i, "rule": d2, "table": ORIG_OFF.get(i, 0.0)})
    return {"s1_icons_compared": len([r for r in oct_rows if r["id"] not in C.PILLAR_GROUP]), "s1_differences": s1,
            "s2_icons_compared": len(oct_rows), "s2_differences": s2}


ORIG_OPT = dict(C.TILE_OPTICAL_SCALE)
ORIG_OFF = dict(C.TILE_OFFSET_X)
ORIG_FLOOR48 = list(C.BARE_FLOOR_48_IDS)


def set_final_optics(per_final):
    """Set the eight finals' optics and floors in this process, so the October tile code and checks use them."""
    for i, (a, dx, floor32) in per_final.items():
        if a != 1.0:
            C.TILE_OPTICAL_SCALE[i] = a
        else:
            C.TILE_OPTICAL_SCALE.pop(i, None)
        if dx != 0.0:
            C.TILE_OFFSET_X[i] = dx
        else:
            C.TILE_OFFSET_X.pop(i, None)
        if floor32 and i in C.BARE_FLOOR_48_IDS:
            C.BARE_FLOOR_48_IDS.remove(i)
        if not floor32 and i not in C.BARE_FLOOR_48_IDS:
            C.BARE_FLOOR_48_IDS.append(i)


def stroke_on_source(f, scratch):
    """The October stroke estimators (stroke_width.py, 8x and 1x) on the final's own drawing, rendered black at 1x
    in its stage B source space on Newsprint. A redrawn or new drawing has no sheet, so its own drawing is measured."""
    text = open(option_src(f), encoding="utf-8").read()
    src = B.parse(f.get("src_id", f["id"]), text)
    view = B.parse(f.get("src_id", f["id"]), text)       # a second parse with numeric box sizes, for drawing only
    view.vb_w, view.vb_h = float(view.vb_w), float(view.vb_h)
    svg = S.crop_space_svg(view, B.W, {"base": C.CHARCOAL, "accent": C.CHARCOAL}, 1)
    out = os.path.join(scratch, "measure", f"{f['id']}-source-1x.png")
    render([{"svg": svg, "w": int(view.vb_w), "h": int(view.vb_h), "bg": C.NEWSPRINT, "out": out}], scratch)
    g = C.green(C.load_rgb(out))
    thr = (C.hex_rgb(C.NEWSPRINT)[1] + C.hex_rgb(C.CHARCOAL)[1]) / 2.0
    w8, _ = SW.measure(g, thr)
    w1, _ = SW.robust_median(SW.skeleton_widths(g < thr, 1))
    return round(w8, 3), round(w1, 3), src


def final_desc(f, label):
    if f["id"] in ("CL-073", "CL-074"):
        place = ("A new topic drawing, numbered and filed with sheet 01, Participation (D2-714).")
    else:
        place = ("It replaces the October master in the set in use, and the October master stays in the October "
                 "set as the record (D2-464, D2-716).")
    return (f"Oath & Action Civic Line {f['id']} {label}. {f['shows']} The final drawing, approved by name on the "
            f"stage B drawings board as {f['pick']} ({f['dr']}) and promoted to the set in use on November 10, 2026. "
            f"{place} Drawn in Civic Line's hand: one line weight, round caps and joins, the capped fit of DR-08. The "
            f"group with data-part 'base' is the main drawing; the group with data-part 'accent' holds the accent "
            f"parts, red in the two-color editions. Every id in the file starts with the file's root id.")


def make_final(f, label):
    """Red-black final text and the four editions, from the approved option's red-black file."""
    opt = open(option_file(f, "red-black"), encoding="utf-8").read()
    oroot = root_of(opt)
    froot = C.bare_root(f["id"], "red-black")
    text = opt.replace(oroot, froot)
    text = re.sub(r'(<svg\b[^>]*?\sdata-id=")[^"]*(")', lambda m: m.group(1) + f["id"] + m.group(2), text, count=1)
    assert len(TITLE_RE.findall(text)) == 1 and len(DESC_RE.findall(text)) == 1
    text = TITLE_RE.sub(lambda m: f"<title>{escape(label)}</title>", text, count=1)
    text = DESC_RE.sub(lambda m: f"<desc>{escape(final_desc(f, label))}</desc>", text, count=1)
    return S.derive_editions(text)


def revert_final(f, ed, final_text):
    """The final with its root id, data-id, title and desc put back to the option file's."""
    opt = open(option_file(f, "red-black"), encoding="utf-8").read()
    oroot_rb = root_of(opt)
    ostem = oroot_rb[:-len("red-black")]
    froot = root_of(final_text)
    t = final_text.replace(froot, ostem + ed)
    odata = re.search(r'<svg\b[^>]*?\sdata-id="([^"]*)"', opt).group(1)
    t = re.sub(r'(<svg\b[^>]*?\sdata-id=")[^"]*(")', lambda m: m.group(1) + odata + m.group(2), t, count=1)
    t = TITLE_RE.sub(lambda m: TITLE_RE.search(opt).group(0), t, count=1)
    t = DESC_RE.sub(lambda m: DESC_RE.search(opt).group(0), t, count=1)
    return t


def oct_paths(r, prefix):
    """October export and tile paths, relative to the v6 folder: SVGs local, PNGs and tiles under prefix."""
    ex = r["exports"]
    paths = []
    for ed in EDITIONS:
        k = ed.replace("-", "_")
        paths.append(f"{ed}/{ex['svg_' + k]}")
        paths.append(f"{prefix}png-256/{ed}/{ex['png_' + k]}")
        paths.append(f"{prefix}png-512/{ed}/{ex['png_' + k]}")
    return paths


def tile_lists(i, slug, date, prefix):
    svgs, pngs = [], []
    for sh in C.TILE_SHAPES:
        for tl in C.TILE_COLOURS:
            for md in C.TILE_MODES:
                base = (f"{date}_Oath-And-Action-Civic-Line-{i}-{slug}-Tile-{SHAPE_NAME[sh]}-{tl.capitalize()}-"
                        f"{MODE_NAME[md]}")
                svgs.append(f"{prefix}tiles/{sh}-{tl}/svg/{base}.svg")
                for px in (256, 512):
                    pngs.append(f"{prefix}tiles/{sh}-{tl}/png-{px}/{base}.png")
    return svgs, pngs


# ---------------------------------------------------------------- build

def build(scratch, check_only=False):
    os.makedirs(scratch, exist_ok=True)
    inv = october_inventory()
    oct_rows = inv["icons"]
    by_id = {r["id"]: r for r in oct_rows}
    median = hull_median(oct_rows)
    report = {"date": DATE, "hull_median_units": round(median, 3)}

    # finals: labels, texts, optics, measures
    finals = []
    for f in FINALS:
        f = dict(f)
        if f["id"] in by_id:
            o = by_id[f["id"]]
            f.update(label=o["label"], slug=o["slug"], sheet=o["sheet"], row=o["row"], column=o["column"])
        eds = make_final(f, f["label"])
        a, dx, m = optics_rule(eds["red-black"], median)
        f.update(eds=eds, a=a, dx=dx, rule=m)
        w8, w1, src = stroke_on_source(f, scratch)
        f.update(stroke8=w8, stroke1=w1, bake=B.bake(src), src=src)
        finals.append(f)
    set_final_optics({f["id"]: (f["a"], f["dx"], f["floor32"]) for f in finals})

    jobs = []
    if not check_only:
        # 1. the 116 unchanged masters, byte for byte
        for r in oct_rows:
            if r["id"] in FINAL_IDS:
                continue
            for ed in EDITIONS:
                src = C.edition_file(r, ed)
                dst = os.path.join(V6, ed, os.path.basename(src))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
        # 2. the eight finals, their previews and tiles
        for f in finals:
            for ed in EDITIONS:
                p = os.path.join(V6, ed, final_name(f, ed))
                write(p, f["eds"][ed])
                for px in (256, 512):
                    jobs.append({"svg": sized(f["eds"][ed], px), "w": px, "h": px, "bg": None,
                                 "out": os.path.join(V6, f"png-{px}", ed, final_name(f, ed, "png"))})
            row = {"id": f["id"], "label": f["label"], "stroke_units": round(f["bake"]["stroke_units"], 4)}
            for sh in C.TILE_SHAPES:
                for tl in C.TILE_COLOURS:
                    for md in C.TILE_MODES:
                        svg = T.tile_svg(f["eds"][C.TILE_EDITION[(tl, md)]], row, sh, tl, md)
                        base = final_tile_name(f, sh, tl, md)
                        write(os.path.join(V6, "tiles", f"{sh}-{tl}", "svg", base + ".svg"), svg)
                        for px in (256, 512):
                            jobs.append({"svg": sized(svg, px), "w": px, "h": px, "bg": None, "tile": True,
                                         "out": os.path.join(V6, "tiles", f"{sh}-{tl}", f"png-{px}", base + ".png")})
        render([{k: v for k, v in j.items() if k != "tile"} for j in jobs], scratch)
        for j in jobs:   # tiles are re-saved as the October build did: RGBA, recompressed
            if j.get("tile"):
                Image.open(j["out"]).convert("RGBA").save(j["out"], optimize=True)
        # 3. the pillar icons
        build_pillar(scratch)

    rows = inventory_rows(oct_rows, finals)
    if not check_only:
        write_inventory(inv, rows, finals, report, median)
    return check(oct_rows, finals, rows, median, scratch, report)


def inventory_rows(oct_rows, finals):
    fin = {f["id"]: f for f in finals}
    out = []
    for r in oct_rows:
        if r["id"] in fin:
            out.append(final_row(fin[r["id"]], r))
        else:
            out.append(unchanged_row(r))
        if r["id"] == "CL-024":          # D2-714: CL-073 and CL-074 are filed with sheet 01, after its 24 drawings
            out.append(final_row(fin["CL-073"], None))
            out.append(final_row(fin["CL-074"], None))
    return out


def unchanged_row(r):
    n = copy.deepcopy(r)
    n["exports"]["paths"] = oct_paths(r, "../civic-line/")
    n["tiles"], n["tile_pngs"] = tile_lists(r["id"], r["slug"], C.DATE, "../civic-line/")
    n["source"] = UNCHANGED
    n["source_file"] = f"../civic-line/red-black/{r['exports']['svg_red_black']}"
    n["png_256_dir"], n["png_512_dir"], n["tiles_dir"] = "../civic-line/png-256", "../civic-line/png-512", "../civic-line/tiles"
    n["sha256"] = {ed: sha(C.edition_file(r, ed)) for ed in EDITIONS}
    return n


def final_row(f, o):
    i = f["id"]
    s, cx, cy = f["bake"]["s"], f["bake"]["cx"], f["bake"]["cy"]
    a, dx, k = C.tile_optics(i, f["bake"]["stroke_units"])
    names = {}
    for ed in EDITIONS:
        key = ed.replace("-", "_")
        names[f"svg_{key}"] = final_name(f, ed)
        names[f"png_{key}"] = final_name(f, ed, "png")
    paths = []
    for ed in EDITIONS:
        paths += [f"{ed}/{final_name(f, ed)}", f"png-256/{ed}/{final_name(f, ed, 'png')}",
                  f"png-512/{ed}/{final_name(f, ed, 'png')}"]
    tiles, tile_pngs = tile_lists(i, f["slug"], DATE, "")
    rel_src = os.path.relpath(option_file(f, "red-black"), V6)
    margins = {sh: round(T.icon_margin(f["eds"]["red-black"], sh, C.TILE_FACTORS[sh], a, dx, k), 3) for sh in C.TILE_SHAPES}
    row = {
        "id": i, "label": f["label"], "slug": f["slug"], "sheet": f["sheet"], "row": f["row"], "column": f["column"],
        "sheet_black": None, "sheet_red": None, "crop": None, "crop_margins": None, "pictogram_box_sheet": None,
        "ink_box_crop": None, "components": None, "registration": None, "red_crop": None, "sheet_iou": None,
        "mask_params": None,
        "construction": f["construction"],
        "red_text": f["red"],
        "exports": {**{k2: v for k2, v in names.items()}, "paths": paths},
        "reference_crops": None, "status": "reviewed", "flags": [], "crop_notes": [], "caption_check": None,
        "stroke_median_px": f["stroke8"], "stroke_median_1x_px": f["stroke1"],
        "extent_px": round(f["bake"]["extent_px"], 3), "extent_units": round(f["bake"]["extent_units"], 3),
        "transform": {"s": round(s, 6), "s_shared": B.S_SHARED, "cap": B.CAP,
                      "framing": "DR-08 capped fit" + ("" if f["bake"]["at_cap"] else ", filling 116 units"),
                      "cx": round(cx, 4), "cy": round(cy, 4),
                      "formula": f"X = {s:.6f} * (x - {S.fmt(cx, 4)}) + 64; Y = {s:.6f} * (y - {S.fmt(cy, 4)}) + 64",
                      "matrix": [round(s, 6), 0, 0, round(s, 6), round(64 - s * cx, 6), round(64 - s * cy, 6)]},
        "stroke_units": round(f["bake"]["stroke_units"], 4),
        "tiles": tiles,
        "tile_optical_scale": a, "tile_offset_x": dx, "tile_stroke_scale": round(k, 6),
        "tile_stroke_units": round(min(f["bake"]["stroke_units"] * a, C.TILE_STROKE_CAP), 4),
        "tile_scale": {sh: round(fac * a, 6) for sh, fac in C.TILE_FACTORS.items()},
        "tile_min_px": C.tile_min_px(i),
        "tile_pngs": tile_pngs,
        "source": f["dr"], "source_file": rel_src,
        "png_256_dir": "png-256", "png_512_dir": "png-512", "tiles_dir": "tiles",
        "sha256": {ed: sha(os.path.join(V6, ed, final_name(f, ed))) for ed in EDITIONS},
        "final": {"approved": f"{f['dr']}, {f['pick']}, approved by name on the stage B drawings board, November 10, 2026",
                  "option_stem": f["stem"], "option_folder": os.path.relpath(os.path.join(ASSETS, f["folder"]), V6),
                  "source_drawing": os.path.relpath(option_src(f), V6),
                  "replaces": (f"../civic-line/red-black/{o['exports']['svg_red_black']}" if o else None),
                  "measured_on": "No supplied sheet exists for this drawing, so the sheet fields (sheet_black, sheet_red, "
                                 "crop, registration, sheet_iou, mask_params, reference_crops, components, "
                                 "caption_check) are null. The stroke medians are the October estimators "
                                 "(stroke_width.py) run on the drawing's own stage B source, rendered black at 1x on "
                                 "Newsprint; the transform is the stage B bake (DR-08), which re-bakes to the option "
                                 "file byte for byte.",
                  "reads_at_px": {"32": f["floor32"], "24": False,
                                  "reader": "the Civic Line icon designer, an agent, November 10, at true size and "
                                            "enlarged, as the October review's section 6 read the 122"},
                  "tile_rule": f["rule"], "tile_margins_units": margins},
    }
    return row


CSV_FIELDS = ["id", "label", "slug", "sheet", "row", "column", "sheet_black", "sheet_red", "crop_x0", "crop_y0",
              "crop_x1", "crop_y1", "reg_dx", "reg_dy", "sheet_iou", "construction", "red_text", "svg_red_black",
              "svg_black", "svg_red_newsprint", "svg_newsprint", "png_red_black", "png_black", "png_red_newsprint",
              "png_newsprint", "ref_black", "ref_red", "status", "scale_s", "transform", "stroke_units",
              "stroke_median_px", "tiles", "tile_optical_scale", "tile_offset_x", "tile_stroke_units",
              "tile_scale_square", "tile_scale_rounded", "tile_scale_circle", "tile_min_px_one_color_square",
              "tile_min_px_one_color_rounded", "tile_min_px_one_color_circle", "tile_min_px_two_color_square",
              "tile_min_px_two_color_rounded", "tile_min_px_two_color_circle", "flags",
              "source", "source_file", "png_256_dir", "png_512_dir", "tiles_dir"]
NONE = "none"


def csv_row(r):
    """The October writer's columns (crop_references.write_csv), then the five added columns. A field with no
    value for a redrawn or new drawing (it has no supplied sheet) reads 'none'."""
    t = r.get("transform") or {}
    n = lambda v: NONE if v is None else v  # noqa: E731
    crop = r.get("crop") or {}
    reg = r.get("registration") or {}
    refs = r.get("reference_crops") or {}
    sheet_less = r.get("crop") is None
    return [r["id"], r["label"], r["slug"], r["sheet"], r["row"], r["column"], n(r["sheet_black"]), n(r["sheet_red"]),
            *([NONE] * 4 if sheet_less else [crop["x0"], crop["y0"], crop["x1"], crop["y1"]]),
            *([NONE] * 2 if sheet_less else [reg["dx"], reg["dy"]]), n(r["sheet_iou"]),
            r["construction"], r["red_text"],
            r["exports"]["svg_red_black"], r["exports"]["svg_black"], r["exports"]["svg_red_newsprint"],
            r["exports"]["svg_newsprint"], r["exports"]["png_red_black"], r["exports"]["png_black"],
            r["exports"]["png_red_newsprint"], r["exports"]["png_newsprint"],
            refs.get("black", NONE), refs.get("red", NONE), r["status"],
            t.get("s", ""), t.get("formula", ""), r.get("stroke_units", ""), r.get("stroke_median_px", ""),
            len(r.get("tiles", [])), r.get("tile_optical_scale", ""), r.get("tile_offset_x", ""),
            r.get("tile_stroke_units", ""),
            *[(r.get("tile_scale") or {}).get(sh, "") for sh in ("square", "rounded", "circle")],
            *[((r.get("tile_min_px") or {}).get(md) or {}).get(sh, "") for md in ("one-color", "two-color")
              for sh in ("square", "rounded", "circle")],
            ";".join(r.get("flags", [])),
            r["source"], r["source_file"], r["png_256_dir"], r["png_512_dir"], r["tiles_dir"]]


def write_inventory(inv, rows, finals, report, median):
    counts = {}
    for r in rows:
        counts[r["sheet"]] = counts.get(r["sheet"], 0) + 1
    by_source = {}
    for r in rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    strokes = [r["stroke_units"] for r in rows]
    tiles_rule = copy.deepcopy(inv["tiles_rule"])
    tiles_rule["finals"] = ("The eight finals take the same factors, transform, stroke cap and minimum-size rule. "
                            "Their optical scale and offset follow S-1 and S-2 on the build's vector hull "
                            f"(cl_tiles.hull_size), with {median:.2f} units, that hull's median over the 122 October "
                            "masters; this form gives the review's table for 116 of the 118 masters outside the pillar "
                            "group under S-1 (CL-072 and R-44 come out one step lower) and for 122 of 122 under S-2. "
                            "Their bare floor (32 or 48 px) comes from reading each at 32 px.")
    out = {
        "title": "Civic Line inventory in use",
        "date": DATE,
        "count": len(rows),
        "counts_by_sheet": dict(sorted(counts.items())),
        "counts_by_source": by_source,
        "decisions": {"set_in_use": "D2-716", "finals": "DR-156 to DR-160", "new_ids": "D2-714",
                      "light_editions": "DR-09", "tiles": "DR-10", "framing": "DR-08", "record": "D2-464, D2-718"},
        "paths_relative_to": "work/build/assets/civic-line-v6/",
        "layout": ("The four SVG editions of all 124 drawings sit in this folder. PNG previews and tiles sit here for "
                   "the eight finals only; the 116 unchanged rows point at their October PNGs and tiles in "
                   "../civic-line/ (D2-716). A row's PNG is <png_256_dir>/<edition>/<png name>, its tiles "
                   "<tiles_dir>/<shape>-<tile>/svg|png-256|png-512/<tile name>."),
        "order": ("The October order, with each final in its original's place, and CL-073 and CL-074 after CL-024 at "
                  "the end of sheet 01 (D2-714)."),
        "october_inventory": "../civic-line/20261029_Civic-Line-Inventory.json",
        "order_matches_catalog": False,
        "pixel_rules": inv["pixel_rules"],
        "W_source_px": inv["W_source_px"],
        "s_units_per_source_px": inv["s_units_per_source_px"],
        "stroke_width_units": [min(strokes), max(strokes)],
        "framing": inv["framing"],
        "tiles_rule": tiles_rule,
        "csv_none": "In the CSV, 'none' marks a sheet field that a redrawn or new drawing does not have; the JSON holds null.",
        "icons": rows,
    }
    C.write_json(INV_JSON, out)
    with open(INV_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_FIELDS)
        for r in rows:
            w.writerow(csv_row(r))


# ---------------------------------------------------------------- pillar icons

PILLARS = [("CL-019", "Explain"), ("CL-020", "Track"), ("CL-021", "Connect"), ("CL-022", "Act")]
PILLAR_SIZES = [(24, "B", 1), (16, "A", 1)]       # DR-179: 24 px fit B, 16 px fit A (the only 16 px fit)
P_EDITIONS = [("black", "Black"), ("red-black", "Red-Black")]


def fit_file(i, word, size, fit, suffix, ext="svg", tail=""):
    sub = "svg" if ext == "svg" else "png"
    return os.path.join(FITS, sub, f"20261109_{i}-{word}-{size}px-Fit-{fit}-{suffix}{tail}.{ext}")


def pillar_name(i, word, size, suffix, ext="svg", tail=""):
    return f"{DATE}_Pillar-Icon-{i}-{word}-{size}px-{suffix}{tail}.{ext}"


def pillar_root(i, size, ed):
    return f"oa-pillar-icon-{i.lower()}-{size}px-{ed}"


def pillar_desc(i, word, size, fit, ed):
    screens = ("On 2x screens a 24 px pillar icon draws its Civic Line master instead (DR-179)." if size == 24 else
               "On 2x screens a 16 px pillar icon keeps this fit (D2-634).")
    edition = ("This black edition is the one in use under 48 px (D2-497)." if ed == "black" else
               "The black edition is the one in use under 48 px (D2-497); this red-black edition is kept as the "
               "record of DR-133's red placements.")
    return (f"Oath & Action Civic Line {i} {word}, pillar icon for {size} px on 1x screens: pixel fit {fit}, a 1 px "
            f"line drawn pixel by pixel on the {size} px grid, every feature and red placement of the master kept, the "
            f"red its own shape in the accent group (DR-133). The final, approved by name on the stage B drawings "
            f"board (DR-179) and promoted on November 10, 2026. {screens} {edition}")


def make_pillar(i, word, size, fit, ed, suffix):
    opt = open(fit_file(i, word, size, fit, suffix), encoding="utf-8").read()
    oroot = root_of(opt)
    t = opt.replace(oroot, pillar_root(i, size, ed))
    t = t.replace(f'data-id="{i}"', f'data-id="{i}" data-size="{size}"', 1)
    t = TITLE_RE.sub(lambda m: f"<title>{escape(word)}</title>", t, count=1)
    t = DESC_RE.sub(lambda m: f"<desc>{escape(pillar_desc(i, word, size, fit, ed))}</desc>", t, count=1)
    return t, opt


def build_pillar(scratch):
    jobs = []
    for i, word in PILLARS:
        for size, fit, _ in PILLAR_SIZES:
            for ed, suffix in P_EDITIONS:
                t, _ = make_pillar(i, word, size, fit, ed, suffix)
                write(os.path.join(PILLAR, "svg", pillar_name(i, word, size, suffix)), t)
                for z, tail in ((1, ""), (2, "-2x")):
                    jobs.append({"svg": sized(t, size * z, base=size), "w": size * z, "h": size * z, "bg": None,
                                 "out": os.path.join(PILLAR, "png", pillar_name(i, word, size, suffix, "png", tail))})
    render(jobs, scratch)
    write_pillar_manifest()


def write_pillar_manifest():
    fm = json.load(open(os.path.join(FITS, "20261109_Pillar-Pixel-Fit-Manifest.json"), encoding="utf-8"))
    by = {(x["id"], x["size_px"], x["fit"]): x for x in fm["fits"]}
    icons = []
    masters = {}
    for i, word in PILLARS:
        masters[i] = {ed: os.path.relpath(os.path.join(V6, ed, f"{C.DATE}_Oath-And-Action-Civic-Line-{i}-{word}-{C.EDITIONS[ed]['suffix']}.svg"), PILLAR)
                      for ed in ("black", "red-black")}
        for size, fit, line in PILLAR_SIZES:
            x = by[(i, size, fit)]
            for ed, suffix in P_EDITIONS:
                p = os.path.join(PILLAR, "svg", pillar_name(i, word, size, suffix))
                icons.append({
                    "id": i, "word": word, "size_px": size, "fit": fit, "line_px": line, "edition": ed,
                    "in_use": ed == "black",
                    "sprite_symbol": f"oa-sym-{i.lower()}-{size}px" if ed == "black" else None,
                    "screens": "1x screens" if size == 24 else "1x and 2x screens",
                    "svg": os.path.relpath(p, PILLAR),
                    "png_1x": f"png/{pillar_name(i, word, size, suffix, 'png')}",
                    "png_2x": f"png/{pillar_name(i, word, size, suffix, 'png', '-2x')}",
                    "source_file": os.path.relpath(fit_file(i, word, size, fit, suffix), PILLAR),
                    "approved": "DR-179",
                    "sha256": sha(p),
                    "red_px": x["red_px"], "black_px": x["black_px"], "map": x["map"],
                })
    out = {
        "title": "Pillar icons in use under 48 px",
        "date": DATE,
        "paths_relative_to": "work/build/assets/pillar-icons/",
        "rules": {
            "screens": ("DR-179: on 1x screens the pillar icons draw these pixel fits, fit B at 24 px and fit A, the "
                        "only fit, at 16 px. On 2x screens a 24 px pillar icon draws its Civic Line master instead "
                        "(listed under masters). The 16 px fit serves 2x screens too (D2-634)."),
            "edition": ("D2-497: the black edition is the one in use under 48 px. The red-black edition is kept as "
                        "the record of DR-133's red placements and is not drawn in the guide."),
            "sizes": "Use each file at its own size only: 24 px files at 24 px, 16 px files at 16 px.",
            "root_attributes": "data-id is the Civic Line ID, data-size the size in px (24 or 16).",
        },
        "decisions": ["DR-133", "DR-179", "D2-497", "D2-634", "D2-611", "D2-612", "D2-613", "D2-614"],
        "masters": masters,
        "icons": icons,
    }
    C.write_json(PILLAR_MANIFEST, out)


# ---------------------------------------------------------------- checks

def check(oct_rows, finals, rows, median, scratch, report):
    errs = []
    res = {"copies": {}, "finals": {}, "tiles": {}, "pillar": {}, "counts": {}}
    # copies
    n_same = 0
    digest = hashlib.sha256()
    for r in oct_rows:
        if r["id"] in FINAL_IDS:
            continue
        for ed in EDITIONS:
            src = C.edition_file(r, ed)
            dst = os.path.join(V6, ed, os.path.basename(src))
            a, b = sha(src), (sha(dst) if os.path.exists(dst) else None)
            if a == b:
                n_same += 1
            else:
                errs.append(f"copy differs or missing: {ed}/{os.path.basename(src)}")
            digest.update(f"{ed}/{os.path.basename(src)} {a}\n".encode())
    res["copies"] = {"files": n_same, "expected": 116 * 4, "digest_of_name_hash_list": digest.hexdigest()}

    # finals
    for f in finals:
        fr = {}
        for ed in EDITIONS:
            p = os.path.join(V6, ed, final_name(f, ed))
            if not os.path.exists(p):
                errs.append(f"missing final {p}")
                continue
            text = open(p, encoding="utf-8").read()
            back = revert_final(f, ed, text)
            if ed in ("red-black", "black"):
                opt_b = open(option_file(f, ed), "rb").read()
                same = back.encode("utf-8") == opt_b
                fr[ed] = {"final_sha256": sha(p), "option_sha256": sha(opt_b), "reverts_to_option_byte_for_byte": same}
                if not same:
                    errs.append(f"{f['id']} {ed}: the final does not revert to its option file")
            else:
                want = S.derive_editions(open(option_file(f, "red-black"), encoding="utf-8").read())[ed]
                same = back == want
                fr[ed] = {"final_sha256": sha(p), "reverts_to_option_swap_byte_for_byte": same}
                if not same:
                    errs.append(f"{f['id']} {ed}: the light edition is not the option's October swap")
            e2 = []
            V.check_svg(p, ed, e2, f["id"])
            errs += e2
            if ed != "red-black":
                ok, n, swaps, why = V.tree_identity(os.path.join(V6, "red-black", final_name(f, "red-black")), p, ed)
                fr[ed]["tree_identity"] = {"ok": ok, "elements": n, "color_swaps": swaps}
                if not ok:
                    errs.append(f"{f['id']} {ed}: tree identity fails: {why}")
            if "<title>" + escape(f["label"]) + "</title>" not in text or f'data-id="{f["id"]}"' not in text:
                errs.append(f"{f['id']} {ed}: title or data-id wrong")
            if f["dr"] not in text:
                errs.append(f"{f['id']} {ed}: the desc does not cite {f['dr']}")
        # the stage B source re-bakes to the option file
        opt_rb = open(option_file(f, "red-black"), encoding="utf-8").read()
        oroot = ET.fromstring(opt_rb.split("?>", 1)[-1].encode())
        otitle = next(e.text for e in oroot if V.strip(e.tag) == "title")
        odesc = next(e.text for e in oroot if V.strip(e.tag) == "desc")
        rb, _ = B.export(f["src"], f["bake"], root_of(opt_rb)[:-len("-red-black")], otitle, odesc)
        fr["source_rebakes_to_option"] = rb == opt_rb
        if not fr["source_rebakes_to_option"]:
            errs.append(f"{f['id']}: the stage B source does not re-bake to the option file")
        # previews
        for ed in EDITIONS:
            for px in (256, 512):
                e2 = []
                V.check_png(os.path.join(V6, f"png-{px}", ed, final_name(f, ed, "png")), px, e2)
                errs += e2
        res["finals"][f["id"]] = fr

    # tiles
    for f in finals:
        row = next(r for r in rows if r["id"] == f["id"])
        trow = {"id": f["id"], "label": f["label"], "stroke_units": row["stroke_units"],
                "tile_stroke_units": row["tile_stroke_units"]}
        tr = {"svg": 0, "png": 0, "margins": row["final"]["tile_margins_units"]}
        for sh in C.TILE_SHAPES:
            if row["final"]["tile_margins_units"][sh] < C.TILE_SAFE_MARGIN:
                errs.append(f"{f['id']}: ink {row['final']['tile_margins_units'][sh]} units from the {sh} edge")
            for tl in C.TILE_COLOURS:
                for md in C.TILE_MODES:
                    ed = C.TILE_EDITION[(tl, md)]
                    bare = ET.parse(os.path.join(V6, ed, final_name(f, ed))).getroot()
                    bare_tree = [k for k in bare if V.strip(k.tag) not in ("title", "desc")]
                    base = final_tile_name(f, sh, tl, md)
                    p = os.path.join(V6, "tiles", f"{sh}-{tl}", "svg", base + ".svg")
                    e2 = []
                    if V.check_tile(p, trow, sh, tl, md, bare_tree, bare.attrib["id"], e2):
                        tr["svg"] += 1
                    errs += e2
                    for px in (256, 512):
                        e2 = []
                        V.check_png(os.path.join(V6, "tiles", f"{sh}-{tl}", f"png-{px}", base + ".png"), px, e2,
                                    opaque_corners=(sh == "square"), centre_opaque=True)
                        errs += e2
                        tr["png"] += 0 if e2 else 1
        res["tiles"][f["id"]] = tr
        if tr["svg"] != 12 or tr["png"] != 24:
            errs.append(f"{f['id']}: {tr['svg']} of 12 tile SVGs and {tr['png']} of 24 tile PNGs pass")

    # counts and inventory
    for ed in EDITIONS:
        n = len([x for x in os.listdir(os.path.join(V6, ed)) if x.endswith(".svg")])
        res["counts"][ed] = n
        if n != 124:
            errs.append(f"{ed}: {n} SVGs, expected 124")
    for px in (256, 512):
        for ed in EDITIONS:
            n = len(os.listdir(os.path.join(V6, f"png-{px}", ed)))
            res["counts"][f"png-{px}/{ed}"] = n
            if n != 8:
                errs.append(f"png-{px}/{ed}: {n} PNGs, expected 8")
    nt = sum(len(os.listdir(os.path.join(V6, "tiles", d, k))) for d in os.listdir(os.path.join(V6, "tiles"))
             for k in ("svg", "png-256", "png-512"))
    res["counts"]["tile_files"] = nt
    if nt != 8 * 12 * 3:
        errs.append(f"tiles: {nt} files, expected 288")
    inv6 = json.load(open(INV_JSON, encoding="utf-8"))
    csv_rows = list(csv.reader(open(INV_CSV, encoding="utf-8")))
    res["counts"]["inventory_json_rows"] = len(inv6["icons"])
    res["counts"]["inventory_csv_rows"] = len(csv_rows) - 1
    if len(inv6["icons"]) != 124 or len(csv_rows) != 125:
        errs.append("inventory row count is not 124")
    empty = [(r[0], CSV_FIELDS[k]) for r in csv_rows[1:] for k, v in enumerate(r) if v == "" and CSV_FIELDS[k] != "flags"]
    res["counts"]["csv_empty_cells_outside_flags"] = len(empty)
    if empty:
        errs.append(f"inventory CSV has {len(empty)} empty cells, first {empty[:3]}")
    missing = []
    for r in inv6["icons"]:
        for p in r["exports"]["paths"] + r["tiles"] + r["tile_pngs"] + [r["source_file"]]:
            if not os.path.exists(os.path.normpath(os.path.join(V6, p))):
                missing.append(p)
    res["counts"]["inventory_paths_checked"] = sum(len(r["exports"]["paths"]) + len(r["tiles"]) + len(r["tile_pngs"]) + 1
                                                   for r in inv6["icons"])
    res["counts"]["inventory_paths_missing"] = len(missing)
    if missing:
        errs.append(f"inventory names {len(missing)} missing files, first {missing[:3]}")
    ids = [r["id"] for r in inv6["icons"]]
    if len(set(ids)) != 124:
        errs.append("inventory ids repeat")

    # rule reproduction on the October masters
    res["rules"] = rule_reproduction(oct_rows, median)
    res["rules"]["finals"] = {f["id"]: {"a": f["a"], "dx": f["dx"], **f["rule"],
                                        "a_with_review_median_74_4": optics_rule(f["eds"]["red-black"], 74.4)[0]}
                              for f in finals}

    # pillar
    pr = {}
    for i, word in PILLARS:
        for size, fit, _ in PILLAR_SIZES:
            for ed, suffix in P_EDITIONS:
                p = os.path.join(PILLAR, "svg", pillar_name(i, word, size, suffix))
                text = open(p, encoding="utf-8").read()
                opt = open(fit_file(i, word, size, fit, suffix), encoding="utf-8").read()
                back = text.replace(pillar_root(i, size, ed), root_of(opt)).replace(f' data-size="{size}"', "", 1)
                back = TITLE_RE.sub(lambda m: TITLE_RE.search(opt).group(0), back, count=1)
                back = DESC_RE.sub(lambda m: DESC_RE.search(opt).group(0), back, count=1)
                k = f"{i}-{size}px-{suffix}"
                pr[k] = {"sha256": sha(p), "source_sha256": sha(opt.encode()), "reverts_to_fit_byte_for_byte": back == opt}
                if back != opt:
                    errs.append(f"pillar {k}: does not revert to its fit file")
                root = ET.fromstring(text.encode())
                if root.attrib.get("data-id") != i or root.attrib.get("data-size") != str(size):
                    errs.append(f"pillar {k}: data-id or data-size wrong")
                idl = [e.attrib["id"] for e in root.iter() if "id" in e.attrib]
                if len(idl) != len(set(idl)) or any(not x.startswith(root.attrib["id"]) for x in idl):
                    errs.append(f"pillar {k}: ids repeat or do not start with the root id")
                if ed == "black" and C.PILLAR_RED in text:
                    errs.append(f"pillar {k}: red in the black edition")
                for z, tail in ((1, ""), (2, "-2x")):
                    a = np.asarray(Image.open(os.path.join(PILLAR, "png", pillar_name(i, word, size, suffix, "png", tail))).convert("RGBA")).astype(int)
                    b = np.asarray(Image.open(fit_file(i, word, size, fit, suffix, "png", tail)).convert("RGBA")).astype(int)
                    same = a.shape == b.shape and int(np.abs(a - b).max()) == 0
                    pr[k][f"png{tail or '-1x'}_equals_stage_b"] = same
                    if not same:
                        errs.append(f"pillar {k}{tail}: PNG differs from the stage B preview")
    n_svg = len(os.listdir(os.path.join(PILLAR, "svg")))
    n_png = len(os.listdir(os.path.join(PILLAR, "png")))
    res["pillar"] = {"files": pr, "svg": n_svg, "png": n_png}
    if n_svg != 16 or n_png != 32:
        errs.append(f"pillar-icons: {n_svg} SVGs and {n_png} PNGs, expected 16 and 32")

    res["errors"] = errs
    out = os.path.join(scratch, f"{DATE}_Civic-Line-V6-Promote-Checks.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(f"copies: {n_same} of {116 * 4} hash the same as October")
    for f in finals:
        fr = res["finals"][f["id"]]
        print(f"{f['id']:7} rb {fr['red-black']['reverts_to_option_byte_for_byte']}  bk {fr['black']['reverts_to_option_byte_for_byte']}  "
              f"rn {fr['red-newsprint']['reverts_to_option_swap_byte_for_byte']}  nw {fr['newsprint']['reverts_to_option_swap_byte_for_byte']}  "
              f"rebake {fr['source_rebakes_to_option']}  a {f['a']}  dx {f['dx']}  tiles {res['tiles'][f['id']]['svg']}/12 svg "
              f"{res['tiles'][f['id']]['png']}/24 png  margins {res['tiles'][f['id']]['margins']}")
    print("rules on the October masters:", len(res["rules"]["s1_differences"]), "S-1 differences,",
          len(res["rules"]["s2_differences"]), "S-2 differences")
    print("counts:", res["counts"])
    print(f"pillar: {n_svg} SVGs, {n_png} PNGs; all revert: {all(v['reverts_to_fit_byte_for_byte'] for v in pr.values())}")
    print(f"checks written to {out}")
    print(f"{len(errs)} errors" + ("" if not errs else ":\n  " + "\n  ".join(errs[:40])))
    return 1 if errs else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=SCRATCH)
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    sys.exit(build(a.scratch, a.check_only))


if __name__ == "__main__":
    main()
