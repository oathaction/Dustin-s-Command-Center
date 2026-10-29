"""The variant review's inline-id test (M-2), in Chromium, for every masked icon.

    python3 -I check_inline_ids.py

A page that inlines two Civic Line files, the first inside a hidden element
(display: none, as in a closed menu or tab panel), must draw the visible one
exactly as it draws alone. For each icon with a mask knockout the script
renders two pairs: the rounded Charcoal two-color tile hidden before the
square Newsprint two-color tile, and the red-black bare file hidden before the
red-newsprint bare file. Each visible file is rendered alone and after its
hidden partner, and the two renders must match pixel for pixel. The same pairs
are rendered again with the ids rewritten to the scheme the files used before
the fix (shared mask ids, id="tile", "icon", "base", "accent"), to show the test
catches the fault. For CL-057 it also reads the pixel at the center of the
person's head: the knockout shows the tile there only when it survives.
Writes qa/<date>_Civic-Line-Inline-Id-Check.json and .png. Exit code 1 if a
visible file changes beside its hidden partner with the current ids.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

OUT_JSON = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Inline-Id-Check.json")
OUT_PNG = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Inline-Id-Check.png")
PX = 256


def body(path):
    s = open(path, encoding="utf-8").read().split("?>", 1)[-1].strip()
    return s.replace('width="128" height="128" viewBox="0 0 128 128"', f'width="{PX}" height="{PX}" viewBox="0 0 128 128"', 1)


def old_scheme(text, root, icon_id, bare):
    """The ids as they were before M-2: part groups named base, accent, tile and
    icon, masks named <icon id>-<name>, and a bare root id without the edition."""
    t = re.sub(re.escape(root) + r"-(base(?:-\d+)?|accent(?:-\d+)?|tile|icon)\b", r"\1", text)
    t = t.replace(root + "-", icon_id.lower() + "-")
    if bare:
        t = t.replace(f'id="{root}"', f'id="oa-civic-line-{icon_id.lower()}"')
    return t


def render(jobs):
    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "jobs.json")
        json.dump(jobs, open(jp, "w"))
        r = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("render failed:\n" + r.stderr[-2000:])


def main():
    inv = C.load_inventory()["icons"]
    masked = [r for r in inv if "<mask" in open(C.edition_file(r, "red-black"), encoding="utf-8").read()]
    tmp = tempfile.mkdtemp()
    jobs, cases = [], []
    for r in masked:
        pairs = [("tile", C.tile_file(r, "rounded", "charcoal", "two-color"), C.tile_root(r["id"], "rounded", "charcoal", "two-color"),
                  C.tile_file(r, "square", "newsprint", "two-color"), C.tile_root(r["id"], "square", "newsprint", "two-color"), None),
                 ("bare", C.edition_file(r, "red-black"), C.bare_root(r["id"], "red-black"),
                  C.edition_file(r, "red-newsprint"), C.bare_root(r["id"], "red-newsprint"), C.CHARCOAL)]
        for kind, hp, hroot, vp, vroot, bg in pairs:
            hid, vis = body(hp), body(vp)
            variants = {"current": (hid, vis),
                        "before_fix": (old_scheme(hid, hroot, r["id"], kind == "bare"), old_scheme(vis, vroot, r["id"], kind == "bare"))}
            case = {"id": r["id"], "pair": kind, "hidden": os.path.basename(hp), "visible": os.path.basename(vp), "renders": {}}
            for scheme, (h, v) in variants.items():
                for mode, html in (("alone", v), ("with_hidden", f'<div style="display:none">{h}</div>{v}')):
                    out = os.path.join(tmp, f"{r['id']}-{kind}-{scheme}-{mode}.png")
                    jobs.append({"svg": html, "w": PX, "h": PX, "bg": bg, "out": out})
                    case["renders"][f"{scheme}_{mode}"] = out
            cases.append(case)
    render(jobs)
    fails = []
    for case in cases:
        img = {k: np.asarray(Image.open(p).convert("RGBA")).astype(int) for k, p in case["renders"].items()}
        for scheme in ("current", "before_fix"):
            d = np.abs(img[f"{scheme}_alone"] - img[f"{scheme}_with_hidden"])
            case[f"{scheme}_pixels_changed"] = int((d.max(axis=2) > 0).sum())
        case["survives"] = case["current_pixels_changed"] == 0
        if not case["survives"]:
            fails.append(f"{case['id']} {case['pair']}: {case['current_pixels_changed']} pixels change beside a hidden copy")
    # CL-057: the head of the person cut from the red wedge
    probe = None
    row = next((r for r in masked if r["id"] == "CL-057"), None)
    if row:
        bare = open(C.edition_file(row, "red-black"), encoding="utf-8").read()
        m = re.search(r'<mask .*?<circle cx="([0-9.]+)" cy="([0-9.]+)" r="([0-9.]+)" fill="#000000"', bare, flags=re.S)
        cx, cy = float(m.group(1)), float(m.group(2))
        fa, tx, ty = C.tile_transform("square", *C.tile_optics("CL-057", row["stroke_units"])[:2])
        x, y = int(round((fa * cx + tx) * PX / 128)), int(round((fa * cy + ty) * PX / 128))
        case = next(c for c in cases if c["id"] == "CL-057" and c["pair"] == "tile")
        probe = {"head_center_box_units": [cx, cy], "pixel": [x, y]}
        for k, p in case["renders"].items():
            probe[k] = "#%02X%02X%02X" % tuple(np.asarray(Image.open(p).convert("RGB"))[y, x])
        probe["knockout_shows_tile_now"] = probe["current_with_hidden"] == C.NEWSPRINT
        probe["knockout_lost_before_fix"] = probe["before_fix_with_hidden"] != C.NEWSPRINT
        if not probe["knockout_shows_tile_now"]:
            fails.append(f"CL-057: the head reads {probe['current_with_hidden']} beside a hidden copy, not the Newsprint tile")
        # evidence board
        pad, top, lab = 24, 72, 56
        panels = [("before_fix_alone", "Before the fix, alone"), ("before_fix_with_hidden", "Before the fix, after a hidden copy"),
                  ("current_alone", "Current ids, alone"), ("current_with_hidden", "Current ids, after a hidden copy")]
        W = pad + len(panels) * (PX + pad)
        board = Image.new("RGB", (W, top + PX + lab + pad), (255, 255, 255))
        dr = ImageDraw.Draw(board)
        dr.text((pad, 14), "CL-057 Labor Share: square Newsprint two-color tile inlined after the rounded Charcoal tile in a display:none element",
                fill=(18, 18, 18), font=C.font(16, True))
        dr.text((pad, 38), "The ring marks the pixel read at the center of the person's head. The knockout should show the Newsprint tile there.",
                fill=(18, 18, 18), font=C.font(14))
        for n, (k, t) in enumerate(panels):
            x0 = pad + n * (PX + pad)
            board.paste(Image.open(case["renders"][k]).convert("RGB"), (x0, top))
            dr.text((x0, top + PX + 10), t, fill=(18, 18, 18), font=C.font(14))
            dr.text((x0, top + PX + 30), f"head pixel {probe[k]}", fill=(93, 99, 109), font=C.font(13))
            dr.ellipse([x0 + x - 13, top + y - 13, x0 + x + 13, top + y + 13], outline=(31, 45, 90), width=1)
        board.save(OUT_PNG, optimize=True)
    for case in cases:
        case.pop("renders")
    shutil.rmtree(tmp, ignore_errors=True)
    report = {"test": "two files inlined on one page in Chromium, the first inside display:none; the visible one must render as it does alone",
              "masked_icons": [r["id"] for r in masked], "cases": cases, "cl_057_probe": probe,
              "all_survive": not fails, "pairs_broken_before_fix": sum(1 for c in cases if c["before_fix_pixels_changed"] > 0),
              "failures": fails}
    C.write_json(OUT_JSON, report)
    print(f"inline id test: {len(cases)} pairs over {len(masked)} masked icons; current ids change "
          f"{sum(c['current_pixels_changed'] for c in cases)} pixels in all; the old ids broke {report['pairs_broken_before_fix']} pairs")
    if probe:
        print(f"  CL-057 head at {probe['pixel']}: before the fix {probe['before_fix_with_hidden']} beside a hidden copy "
              f"(alone {probe['before_fix_alone']}); now {probe['current_with_hidden']} (alone {probe['current_alone']})")
    for f_ in fails:
        print("FAIL:", f_)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
