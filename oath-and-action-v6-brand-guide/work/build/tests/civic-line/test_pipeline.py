"""Tests for the Civic Line pipeline. Runs in a temporary asset tree, so the
real exports, QA files and status files are never touched.

    python3 -I work/build/tests/civic-line/test_pipeline.py

1. The validator rejects each rule break with a clear message.
2. Baking relative commands, arcs and a leading 'm' matches mapping the
   flattened source geometry point by point.
3. A feature source (mask knockout, evenodd hole, fill, fill-stroke, miter,
   butt, data-w, several groups) builds end to end: the knockouts are real
   holes in the transparent PNG, the pair is identical after the swap, the
   bake check is near 1 and verify_set passes on the tree.
4. verify_set catches a tampered black file, a red value in a black file, a
   background rect, a drawing outside 0..128 and a text element.
5. All 244 reference crops are exact pixel copies of their sheet rectangles,
   and the supplied sheets are unchanged against git.
"""
import json
import os
import shutil
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, "..", "..", "scripts", "civic-line"))
sys.path.insert(0, SCRIPTS)
import cl_common as C  # noqa: E402
import cl_svg as S  # noqa: E402

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


GOOD = """<svg xmlns="http://www.w3.org/2000/svg" data-id="R-35" viewBox="0 0 179 123">
  <g data-role="base"><line x1="10" y1="10" x2="50" y2="10"/></g>
</svg>"""
CORR = {"id": "R-35", "tracer": "test", "corrections": []}


def expect_error(name, svg, needle, corr=CORR):
    try:
        S.parse_source(svg, "R-35", 179, 123, corr)
        check(f"validator rejects: {name}", False, "no error raised")
    except S.SourceError as e:
        check(f"validator rejects: {name}", needle in str(e), str(e).splitlines()[-1].strip()[:110])


def validator_tests():
    S.parse_source(GOOD, "R-35", 179, 123, CORR)
    check("validator accepts a minimal source", True)
    rep = lambda a, b: GOOD.replace(a, b)  # noqa: E731
    expect_error("wrong viewBox", rep('viewBox="0 0 179 123"', 'viewBox="0 0 128 128"'), "viewBox must be")
    expect_error("wrong data-id", rep('data-id="R-35"', 'data-id="R-36"'), "data-id must be")
    expect_error("transform", rep('<line ', '<line transform="rotate(5)" '), "transforms are not supported")
    expect_error("fill colour", rep('<line ', '<line fill="#E63946" '), "colors and stroke style come from")
    expect_error("style attribute", rep('<line ', '<line style="stroke:red" '), "attribute 'style' is not allowed")
    expect_error("text element", rep('<line x1="10" y1="10" x2="50" y2="10"/>', '<text x="1" y="1">A</text>'), "<text> is not allowed")
    expect_error("image element", rep('<line x1="10" y1="10" x2="50" y2="10"/>', '<image href="a.png"/>'), "<image> is not allowed")
    expect_error("nested group", rep('<line x1="10" y1="10" x2="50" y2="10"/>', '<g><line x1="1" y1="1" x2="2" y2="2"/></g>'), "groups cannot nest")
    expect_error("unknown role", rep('data-role="base"', 'data-role="red"'), "data-role must be")
    expect_error("unknown class", rep('<line ', '<line class="square" '), "unknown class")
    expect_error("fill with miter", rep('<line ', '<line class="fill miter" '), "'miter' and 'butt' describe a stroke")
    expect_error("data-w without id", rep('<line ', '<line data-w="7" '), "needs an id")
    expect_error("data-w not logged", rep('<line ', '<line id="a" data-w="7" '), "has no correction")
    S.parse_source(rep('<line ', '<line id="a" data-w="7" '), "R-35", 179, 123,
                   {"id": "R-35", "corrections": [{"element": "a", "what": "heavier rule", "why": "sheet shows 7 px"}]})
    check("validator accepts data-w with a logged correction", True)
    expect_error("missing corrections log", GOOD, "is missing", corr=None)
    expect_error("correction without why", GOOD, "needs non-empty 'what' and 'why'",
                 corr={"id": "R-35", "corrections": [{"what": "x"}]})
    expect_error("undefined mask", rep('<g data-role="base">', '<g data-role="base" mask="url(#nope)">'), "referenced but not defined")
    expect_error("unused mask", rep('<g data-role="base">', '<defs><mask id="m"><circle cx="1" cy="1" r="1"/></mask></defs><g data-role="base">'), "never used")
    expect_error("fill-rule on a stroke", rep('<line x1="10" y1="10" x2="50" y2="10"/>', '<path fill-rule="evenodd" d="M0 0 L1 1"/>'), "fill-rule only applies")
    expect_error("bad path data", rep('<line x1="10" y1="10" x2="50" y2="10"/>', '<path d="M0 0 L1"/>'), "multiple of 2")
    expect_error("bad arc flag", rep('<line x1="10" y1="10" x2="50" y2="10"/>', '<path d="M0 0 A5 5 0 2 1 4 4"/>'), "arc flag must be 0 or 1")
    expect_error("not well-formed XML", GOOD.replace("</svg>", ""), "XML parse error")
    keep = GOOD.replace('<g data-role="base">', '<defs><mask id="m"><circle class="fill" cx="20" cy="20" r="9"/>'
                        '<circle class="fill" data-mask="keep" cx="20" cy="20" r="3"/></mask></defs><g data-role="base" mask="url(#m)">')
    src = S.parse_source(keep, "R-35", 179, 123, CORR)
    out = S.crop_space_svg(src, 5.5, {"base": C.CHARCOAL, "accent": C.PILLAR_RED})
    check("mask: cut shapes paint black, data-mask keep paints white, group gets the mask",
          'r="9" fill="#000000"' in out and 'r="3" fill="#FFFFFF"' in out and '<g id="base" mask="url(#m-m)">' in out)


def bake_tests():
    d = "m10 10 l20 0 a8 8 0 0 1 8 8 v12 h-10 q-5 5 -10 0 t-10 0 s-5 -5 -3 -10 c1 -2 2 -3 5 -3 z M60 60 A12 6 30 1 0 80 70 Z"
    segs = S.tokenize_path(d, "t")
    s, cx, cy = 0.487395, 96.5, 60.5
    M = S.Mapping(s, cx, cy, 64, 64)
    baked = S.transform_path(segs, M.X, M.Y, M.s)
    a = [p for poly in S.flatten_path(segs) for p in poly]
    b = [p for poly in S.flatten_path(baked) for p in poly]
    err = max(max(abs(M.X(x) - X), abs(M.Y(y) - Y)) for (x, y), (X, Y) in zip(a, b))
    check("bake: relative commands, arcs and a leading m map point for point (4-decimal output)", len(a) == len(b) and err < 5e-4,
          f"max error {err:.2e} units")
    txt = S.path_string(baked)
    back = [p for poly in S.flatten_path(S.tokenize_path(txt, "t")) for p in poly]
    err2 = max(max(abs(X - x2), abs(Y - y2)) for (X, Y), (x2, y2) in zip(b, back))
    check("bake: serialised path re-reads within the output rounding", err2 < 5e-4, f"max error {err2:.5f} units")
    arc_centre_test()


def svg_arc_centre(x1, y1, rx, ry, fa, fs, x2, y2):
    """Centre a renderer computes for an unrotated arc (SVG 1.1 F.6.5, with radius scaling)."""
    import math
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    lam = (dx / rx) ** 2 + (dy / ry) ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * dy * dy - ry * ry * dx * dx
    den = rx * rx * dy * dy + ry * ry * dx * dx
    co = math.sqrt(max(0.0, num / den))
    if fa == fs:
        co = -co
    return co * rx * dy / ry + (x1 + x2) / 2, -co * ry * dx / rx + (y1 + y2) / 2


def arc_centre_test():
    """Half circles whose ends sit a diameter apart, and near-half circles, keep
    their centre through the bake within 0.01 source px."""
    import math
    import random
    rnd = random.Random(7)
    s = 0.487395
    worst = 0.0
    for _ in range(4000):
        cx, cy, r, th = rnd.uniform(20, 150), rnd.uniform(20, 110), rnd.uniform(3, 50), rnd.uniform(0, 2 * math.pi)
        dt = 0.0 if rnd.random() < 0.5 else rnd.uniform(0.0005, 0.05)
        x1, y1 = cx + r * math.cos(th), cy + r * math.sin(th)
        x2, y2 = cx + r * math.cos(th + math.pi - dt), cy + r * math.sin(th + math.pi - dt)
        fs = rnd.randint(0, 1)
        tcx, tcy = rnd.uniform(60, 120), rnd.uniform(40, 80)
        X = lambda v: s * (v - tcx) + 64  # noqa: E731
        Y = lambda v: s * (v - tcy) + 64  # noqa: E731
        want = svg_arc_centre(X(x1), Y(y1), r * s, r * s, 0, fs, X(x2), Y(y2))
        (_, m), (_, a) = S.transform_path([("M", [x1, y1]), ("A", [r, r, 0, 0, fs, x2, y2])], X, Y, s)
        got = svg_arc_centre(m[0], m[1], a[0], a[1], 0, fs, a[5], a[6])
        worst = max(worst, math.hypot(got[0] - want[0], got[1] - want[1]) / s)
    check("bake: 4000 half and near-half arcs keep their centre within 0.01 source px", worst < 0.01, f"worst {worst:.5f} px")


FEATURE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" data-id="R-35" viewBox="0 0 179 123">
  <defs>
    <mask id="x-cut">
      <line x1="126" y1="77" x2="146" y2="97"/>
      <line x1="146" y1="77" x2="126" y2="97"/>
    </mask>
  </defs>
  <g data-role="base">
    <circle cx="44" cy="22" r="10"/>
    <path class="miter" d="M20 62 h60 v8 h-60 z"/>
    <rect class="fill-stroke miter" x="30" y="80" width="12" height="20"/>
    <path class="fill" fill-rule="evenodd" d="M60 80 h20 v20 h-20 z M65 85 h10 v10 h-10 z"/>
    <polyline class="butt" points="24,104 50,104"/>
    <line id="heavy" data-w="8" x1="60" y1="110" x2="90" y2="110"/>
  </g>
  <g data-role="accent">
    <circle class="fill" cx="136" cy="87" r="22" mask="url(#x-cut)"/>
  </g>
  <g data-role="base">
    <path d="m110 20 a20 20 0 1 1 0 0.01"/>
  </g>
</svg>
"""
FEATURE_JSON = {"id": "R-35", "tracer": "test", "corrections": [
    {"element": "heavy", "what": "data-w 8 test", "why": "exercise the override"}], "notes": "pipeline test source, not a trace"}


def feature_build_test():
    tmp = tempfile.mkdtemp(prefix="civic-line-test-")
    try:
        assets = os.path.join(tmp, "assets")
        for sub in ["src", "red-black", "black", "png-256/red-black", "png-256/black", "png-512/red-black", "png-512/black",
                    "reference-crops", "qa/masks", "qa/metrics", "qa/overlays", "qa/blink", "qa/sizes", "qa/status"]:
            os.makedirs(os.path.join(assets, sub), exist_ok=True)
        inv = C.load_inventory()
        row = [r for r in inv["icons"] if r["id"] == "R-35"][0]
        for f in os.listdir(os.path.join(C.ASSETS, "reference-crops")):   # all 244, so the package count can pass
            shutil.copy(os.path.join(C.ASSETS, "reference-crops", f), os.path.join(assets, "reference-crops"))
        for suf in ("ink", "red"):
            shutil.copy(os.path.join(C.QA, "masks", f"R-35-{suf}.png"), os.path.join(assets, "qa", "masks"))
        shutil.copy(C.SCALE_JSON, os.path.join(assets, "qa"))
        shutil.copy(C.INVENTORY_JSON, assets)
        with open(os.path.join(assets, "src", "R-35.svg"), "w") as fh:
            fh.write(FEATURE_SVG)
        with open(os.path.join(assets, "src", "R-35.json"), "w") as fh:
            json.dump(FEATURE_JSON, fh)
        # point the modules at the temporary tree
        C.ASSETS = assets
        C.SRC = os.path.join(assets, "src")
        C.QA = os.path.join(assets, "qa")
        C.INVENTORY_JSON = os.path.join(assets, os.path.basename(C.INVENTORY_JSON))
        C.SCALE_JSON = os.path.join(C.QA, os.path.basename(C.SCALE_JSON))
        import build_icon as B
        res, fail = B.build(["R-35"], tracer="test")
        check("feature source builds", not fail and "R-35" in res, str(fail)[:200])
        if fail:
            return
        m = C.read_json(os.path.join(C.QA, "metrics", "R-35.json"))
        check("feature: bake check IoU at 4x (main) and 1x near 1", m["bake_check_iou_4x"] > 0.999 and m["bake_check_iou_1x"] > 0.995,
              f"{m['bake_check_iou_1x']}, {m['bake_check_iou_4x']}")
        check("feature: pair identical after the token swap", m["pair_identical_after_swap"])
        check("feature: drawing inside 0..128 with stroke", m["export_inside_0_128"], str(m["export_drawn_bounds"]))
        rb_name = row["exports"]["png_red_black"]
        png = np.asarray(Image.open(os.path.join(assets, "png-512", "red-black", rb_name)))
        t = row["transform"]
        to_px = lambda x, y: (int(round((t["s"] * (x - t["cx"]) + 64) * 4)), int(round((t["s"] * (y - t["cy"]) + 64) * 4)))  # noqa: E731
        xc, yc = to_px(136, 87)      # centre of the X knockout
        xd, yd = to_px(136, 72)      # inside the disc, clear of the X
        xh, yh = to_px(70, 90)       # centre of the evenodd hole
        xf, yf = to_px(62, 82)       # inside the evenodd frame
        check("feature: mask knockout is a real hole (alpha 0 at the X centre)", png[yc, xc, 3] == 0, f"alpha {png[yc, xc, 3]}")
        check("feature: disc around the knockout is Pillar Red", png[yd, xd, 3] == 255 and tuple(png[yd, xd, :3]) == C.hex_rgb(C.PILLAR_RED),
              f"{tuple(png[yd, xd])}")
        check("feature: evenodd hole is transparent", png[yh, xh, 3] == 0, f"alpha {png[yh, xh, 3]}")
        check("feature: evenodd frame is Charcoal", png[yf, xf, 3] == 255 and tuple(png[yf, xf, :3]) == C.hex_rgb(C.CHARCOAL),
              f"{tuple(png[yf, xf])}")
        bkp = np.asarray(Image.open(os.path.join(assets, "png-512", "black", row["exports"]["png_black"])))
        check("feature: black edition keeps the knockout open", bkp[yc, xc, 3] == 0 and tuple(bkp[yd, xd, :3]) == C.hex_rgb(C.CHARCOAL))
        txt = open(os.path.join(assets, "red-black", row["exports"]["svg_red_black"])).read()
        check("feature: two base groups numbered, accent single", 'id="base-1"' in txt and 'id="base-2"' in txt and 'id="accent"' in txt)
        check("feature: mask region set in user space over the canvas",
              'maskUnits="userSpaceOnUse" x="0" y="0" width="128" height="128"' in txt)
        check("feature: data-w scaled into the export", f'stroke-width="{S.fmt4(8 * t["s"])}"' in txt)
        for k in ("overlays/R-35.png", "blink/R-35.gif", "sizes/R-35.png", "status/R-35.json"):
            check(f"feature: wrote qa/{k}", os.path.exists(os.path.join(C.QA, k)))
        st = C.read_json(os.path.join(C.QA, "status", "R-35.json"))
        check("feature: status traced, 1 iteration, corrections copied", st["state"] == "traced" and st["iterations"] == 1
              and len(st["corrections"]) == 1)
        B.build(["R-35"], state="reviewed", note="looked at overlay")
        st = C.read_json(os.path.join(C.QA, "status", "R-35.json"))
        check("feature: --state and --note update the status", st["state"] == "reviewed" and st["iterations"] == 2 and st["notes"])
        # verify_set on the temporary tree
        import verify_set as V
        V.LEDGER = os.path.join(C.QA, "ledger.md")
        V.REPORT = os.path.join(C.QA, "report.json")
        code = run_verify(V)
        rep = C.read_json(V.REPORT)
        check("verify: clean tree passes", code == 0 and not rep["errors"], "; ".join(rep["errors"])[:200])
        check("verify: missing sources counted as todo", rep["states"]["todo"] == 121)
        bk = os.path.join(assets, "black", row["exports"]["svg_black"])
        orig = open(bk).read()
        tamper(V, bk, orig.replace('r="', 'r="1', 1), "tampered black geometry", "is not the red-black file")
        tamper(V, bk, orig.replace(C.CHARCOAL, C.PILLAR_RED, 1), "red token in the black file", "red value")
        sw = 'stroke-width="' + S.fmt4(5.5 * row["transform"]["s"]) + '"'
        tamper(V, bk, orig.replace(sw, 'stroke-width="3"', 1), "a stroke width changed in the black tree", "edition trees differ")
        rbp = os.path.join(assets, "red-black", row["exports"]["svg_red_black"])
        rb_orig = open(rbp).read()
        bg = rb_orig.replace('<g id="base-1">', '<rect x="0" y="0" width="128" height="128" fill="#121212"/><g id="base-1">')
        tamper(V, rbp, bg, "background rect", "background-sized", also=(bk, bg.replace(C.PILLAR_RED, C.CHARCOAL)))
        out = rb_orig.replace('<circle cx="', '<circle cx="1', 1)
        tamper(V, rbp, out, "drawing outside 0..128", "outside 0..128", also=(bk, out.replace(C.PILLAR_RED, C.CHARCOAL)))
        tx = rb_orig.replace('</svg>', '<text x="5" y="5">A</text></svg>')
        tamper(V, rbp, tx, "text element in an export", "forbidden <text>", also=(bk, tx.replace(C.PILLAR_RED, C.CHARCOAL)))
        open(bk, "w").write(orig)
        open(rbp, "w").write(rb_orig)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_verify(V):
    try:
        V.main()
    except SystemExit as e:
        return e.code or 0
    return 0


def tamper(V, path, text, name, needle, also=None):
    keep = open(path).read()
    keep2 = open(also[0]).read() if also else None
    open(path, "w").write(text)
    if also:
        open(also[0], "w").write(also[1])
    code = run_verify(V)
    rep = C.read_json(V.REPORT)
    check(f"verify catches: {name}", code == 1 and any(needle in e for e in rep["errors"]),
          next((e for e in rep["errors"] if needle in e), "; ".join(rep["errors"])[:120]))
    open(path, "w").write(keep)
    if also:
        open(also[0], "w").write(keep2)


def main():
    reference_tests()
    validator_tests()
    bake_tests()
    feature_build_test()
    n_fail = sum(1 for r in RESULTS if not r[1])
    print(f"\n{len(RESULTS) - n_fail} passed, {n_fail} failed")
    sys.exit(1 if n_fail else 0)


def reference_tests():
    """Reference crops are exact pixel copies; the supplied sheets are unchanged."""
    import subprocess
    inv = C.load_inventory()["icons"]
    bad = 0
    sheets = {}
    for r in inv:
        for kind, key, rect in (("black", "sheet_black", r["crop"]), ("red", "sheet_red", r["red_crop"])):
            f = r[key]
            if f not in sheets:
                sheets[f] = np.asarray(Image.open(os.path.join(C.REF_DIR, f)))
            want = sheets[f][rect["y0"]:rect["y1"], rect["x0"]:rect["x1"]]
            got = np.asarray(Image.open(os.path.join(C.ASSETS, "reference-crops", r["reference_crops"][kind])))
            if got.shape != want.shape or not np.array_equal(got, want):
                bad += 1
    check("reference crops: all 244 are exact pixel copies of their sheet rectangles", bad == 0, f"{bad} differ")
    out = subprocess.run(["git", "status", "--porcelain", "--", C.REF_DIR], capture_output=True, text=True, cwd=C.ROOT)
    check("reference sheets: unchanged against git", out.returncode == 0 and out.stdout.strip() == "", out.stdout.strip()[:120])
    n = len([f for f in os.listdir(os.path.join(C.ASSETS, "reference-crops")) if f.endswith(".png")])
    check("reference crops: 244 files", n == 244, str(n))



if __name__ == "__main__":
    main()
