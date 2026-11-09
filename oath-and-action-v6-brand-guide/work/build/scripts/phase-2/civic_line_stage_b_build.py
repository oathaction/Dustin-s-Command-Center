"""Build the stage B Civic Line drawings: sources, exports, previews, manifest.

    python3 -I work/build/scripts/phase-2/civic_line_stage_b_build.py [--only ID] [--proof NAME]

For each option in REGISTRY it writes, in the option's folder:
  src/<date>_<ID>-<Name>-Option-<X>.svg   the source drawing (line 5.5 px)
  svg/<date>_<ID>-<Name>-Option-<X>-Red-Black.svg and -Black.svg (128 box)
  png/... -Red-Black.png, -Red-Black-2x.png, -Black.png, -Black-2x.png
     (128 and 256 px, transparent, as the masters' PNGs are)
and one manifest JSON per folder with the bake figures. --proof writes a
review sheet to the scratch folder: each option at 2x, at 48 px enlarged by
whole pixels, and at 48 and 24 px true size, all on Newsprint.
"""
import argparse
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import civic_line_stage_b_common as C  # noqa: E402
import civic_line_stage_b_drawings as D  # noqa: E402
import civic_line_stage_b_new_topics as N  # noqa: E402

ASSETS = os.path.join(C.ROOT, "work", "build", "assets")
FOLDERS = {"redraw": os.path.join(ASSETS, "civic-line-redraws"),
           "new": os.path.join(ASSETS, "civic-line-new-topics")}

# id, name, option, folder, drawing, within DR-135, what changed (one line)
REGISTRY = [
    ("CL-025", "Congress", "A", "redraw", D.cl025_a, True,
     "Dome, cupola and finial become a flat attic; the columns become walls, windows and a center door, which takes the red."),
    ("CL-025", "Congress", "B", "redraw", D.cl025_b, False,
     "The chamber in session from the gallery: five members on the near bench seen from behind, a far bench in five sections, and the three-tier rostrum with its top tier red."),
    ("CL-025", "Congress", "C", "redraw", D.cl025_c, False,
     "The chamber from the rostrum: members face the reader from two curved benches, and the presiding desk stands red in the foreground."),
    ("CL-014", "Entrenched-Power", "A", "redraw", D.cl014_a, True,
     "Spire, cupola and dome become set A's flat attic; the six columns become two walls. Fence and red door kept."),
    ("CL-014", "Entrenched-Power", "B", "redraw", D.cl014_b, False,
     "Set B's chamber in session without the Speaker's tier, inside a fence opened for 48 px; the red moves from the door to the rostrum's top tier."),
    ("CL-014", "Entrenched-Power", "C", "redraw", D.cl014_c, False,
     "A ballot's arrow runs at the fenced chamber and stops at the fence on a red bar: an election cannot move the body."),
    ("R-13", "Congressional-Capacity", "A", "redraw", D.r13_a, True,
     "Dome arcs and finial go, leaving the drum as a flat attic; the drum columns go and the lower columns become two windows and a door."),
    ("R-13", "Congressional-Capacity", "B", "redraw", D.r13_b, False,
     "Set B's chamber in session replaces the building, above two staff and an analyst's report whose chart line takes the red."),
    ("R-13", "Congressional-Capacity", "C", "redraw", D.r13_c, False,
     "Set C's chamber from the rostrum replaces the building, above two staff and an analyst's report whose chart line takes the red."),
    ("R-42", "Congressional-Tariff-Votes", "A", "redraw", D.r42_a, True,
     "Finial, lantern and dome go, leaving the drum as a flat attic; the columns become a band and windows. Ballot box, chart and red kept."),
    ("R-42", "Congressional-Tariff-Votes", "B", "redraw", D.r42_b, False,
     "Set B's chamber in session, a red vote card with a yes and a no in place of the ballot box, and CL-064's parcel with a tag for imports."),
    ("R-42", "Congressional-Tariff-Votes", "C", "redraw", D.r42_c, False,
     "Set C's chamber from the rostrum, a red vote card with a yes and a no in place of the ballot box, and CL-064's parcel with a tag for imports."),
    ("CL-059", "Credit-Allocation", "A", "redraw", D.cl059_a, True,
     "The four columns become one wall holding a round vault door. Pediment, base, home, factory and red branches kept."),
    ("CL-059", "Credit-Allocation", "B", "redraw", D.cl059_b, False,
     "The pediment goes too: a flat-roofed bank with a round vault door on its face, its wheel's handles standing past the rim."),
    ("CL-059", "Credit-Allocation", "C", "redraw", D.cl059_c, False,
     "The lender and the loan: a small flat-roofed building beside a loan paper marked with a percent sign; the red branches carry the money out."),
    ("R-48", "Agency-Independence", "A", "redraw", D.r48_a, True,
     "The four bays of columns become one wall with a door and two windows. Pediment, band, base, brace and official kept."),
    ("R-48", "Agency-Independence", "B", "redraw", D.r48_b, False,
     "A flat-roofed office building with no columns or pediment, the red brace, and the official at a desk whose arrow stops at it."),
    ("R-48", "Agency-Independence", "C", "redraw", D.r48_c, False,
     "The commission at its table, and the official moves to a desk; a longer arrow from the desk stops at the red brace."),
]


def name_of(row):
    """Redraws carry their master's ID; the new topics have none yet."""
    i, n, o, folder = row[0], row[1], row[2], row[3]
    return f"{C.DATE}_{n}-Option-{o}" if folder == "new" else f"{C.DATE}_{i}-{n}-Option-{o}"


def build_one(row, proof_jobs=None, scratch=None):
    icon_id, name, opt, folder, fn, within, change = row
    base = FOLDERS[folder]
    stem = name_of(row)
    groups = fn()
    text = C.source_svg(icon_id, groups, vb=(0, 0, 400, 300))
    src = C.parse(icon_id, text)
    x0, y0, x1, y1 = C.ink_box(src)
    if x0 < 0 or y0 < 0:
        raise SystemExit(f"{stem}: drawing leaves the source canvas ({x0:.1f}, {y0:.1f})")
    vb = (0, 0, math.ceil(x1 + 8), math.ceil(y1 + 8))
    text = C.source_svg(icon_id, groups, vb=vb)
    src = C.parse(icon_id, text)
    m = C.bake(src)
    title = f"{name.replace('-', ' ')}, option {opt}"
    what = (f"{icon_id} {name.replace('-', ' ')}, stage B redraw, option {opt}, {'within' if within else 'outside'} DR-135."
            if folder == "redraw" else f"{name.replace('-', ' ')}, new topic drawing (DR-141, DR-147), option {opt}.")
    desc = (f"Oath & Action Civic Line {what} {change} Drawn in Civic Line's hand: "
            f"one line weight, round caps and joins, one red accent, the capped fit of DR-08. The group with data-part "
            f"'accent' holds the red parts.")
    root = f"oa-civic-line-{(name if folder == 'new' else icon_id).lower()}-option-{opt.lower()}"
    rb, bk = C.export(src, m, root, title, desc)
    for sub in ("src", "svg", "png"):
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    with open(os.path.join(base, "src", stem + ".svg"), "w", encoding="utf-8") as fh:
        fh.write(text)
    out = {}
    for ed, s in (("Red-Black", rb), ("Black", bk)):
        p = os.path.join(base, "svg", f"{stem}-{ed}.svg")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(s)
        out[ed] = p
    jobs = []
    for ed, s in (("Red-Black", rb), ("Black", bk)):
        for z, suf in ((1, ""), (2, "-2x")):
            jobs.append({"svg": C.sized(s, 128 * z), "w": 128 * z, "h": 128 * z, "bg": None,
                         "out": os.path.join(base, "png", f"{stem}-{ed}{suf}.png")})
    if proof_jobs is not None:
        for px in (256, 48, 24):
            proof_jobs.append({"svg": C.sized(rb if px > 24 else bk, px), "w": px, "h": px, "bg": C.NEWSPRINT,
                               "out": os.path.join(scratch, "r", f"{stem}-{px}.png")})
    rec = {"id": icon_id, "name": name.replace("-", " "), "option": opt, "within_dr135": within if folder == "redraw" else None,
           "change": change, "stem": stem, "folder": os.path.relpath(base, C.ROOT),
           "svg_red_black": os.path.relpath(out["Red-Black"], C.ROOT), "svg_black": os.path.relpath(out["Black"], C.ROOT),
           "scale": round(m["s"], 6), "stroke_units": round(m["stroke_units"], 4), "extent_units": round(m["extent_units"], 2),
           "ink_px": [round(m["w_px"], 1), round(m["h_px"], 1)], "at_cap": m["at_cap"]}
    return rec, jobs


def proof(recs, scratch, name):
    rows = []
    for r in recs:
        s = r["stem"]
        R = os.path.join(scratch, "r")
        row = os.path.join(R, s + "-row.png")
        subprocess.run(["convert", os.path.join(R, s + "-256.png"),
                        "(", os.path.join(R, s + "-48.png"), "-filter", "point", "-resize", "400%", ")",
                        os.path.join(R, s + "-48.png"), os.path.join(R, s + "-24.png"),
                        "-bordercolor", C.NEWSPRINT, "-border", "4", "-background", C.NEWSPRINT, "-gravity", "center",
                        "+append", row], check=True)
        rows += ["-label", f"{r['id']} {r['option']}  stroke {r['stroke_units']}", row]
    subprocess.run(["montage", *rows, "-tile", "1x", "-geometry", "+4+4", "-background", "#c8c4bb", "-pointsize", "13",
                    os.path.join(scratch, name + ".png")], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--proof")
    ap.add_argument("--scratch", default=os.environ.get("CL_SCRATCH", "/tmp/cl-stage-b"))
    a = ap.parse_args()
    reg = [r for r in REGISTRY + N.REGISTRY if not a.only or r[0] in a.only or f"{r[0]}-{r[2]}" in a.only]
    recs, jobs, pj = [], [], ([] if a.proof else None)
    for row in reg:
        rec, j = build_one(row, pj, a.scratch)
        recs.append(rec)
        jobs += j
    C.render(jobs + (pj or []), os.path.join(a.scratch, "tmp"))
    if a.proof:
        proof(recs, a.scratch, a.proof)
    if not a.only:
        for folder, base in FOLDERS.items():
            mine = [r for r in recs if r["folder"] == os.path.relpath(base, C.ROOT)]
            if mine:
                with open(os.path.join(base, f"{C.DATE}_Stage-B-Drawings-Manifest.json"), "w", encoding="utf-8") as fh:
                    json.dump({"date": C.DATE, "rule": "s = min(116 / extent, 1.25 x 0.487395), line 5.5 source px (DR-08)",
                               "options": mine}, fh, indent=1)
    for r in recs:
        print(f"{r['id']:7} {r['option']}  s {r['scale']:.4f}  stroke {r['stroke_units']:.3f}  ink {r['ink_px']}")


if __name__ == "__main__":
    main()
