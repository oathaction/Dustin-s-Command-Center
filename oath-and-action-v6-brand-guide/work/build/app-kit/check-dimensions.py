"""Check every application export against the platform specifications table, and print a pass or fail per file.

Usage:
  python3 -I work/build/app-kit/check-dimensions.py [--exports DIR] [--specs PATH] [--json OUT]
  python3 -I work/build/app-kit/check-dimensions.py --self-test

Reads:
  work/build/exports/phase-4/*_Phase-4-Exports-Manifest.json   the newest one, written by `oa-app.mjs export`: one entry
                     per file, {"file", "spec", "platform", "format", ...}, where "platform" is a row id in the table
  work/research/20261121_Platform-Specifications.json   the research lead's table (DR-292): each row's width, height,
                     unit, aspect, max_bytes, bleed and "match" (exact, min, max or ratio)

Checks, per file:
  PNG     its pixel width and height against the row: exact, at least (min), at most (max), or the ratio alone (ratio);
          a side the row leaves null is not checked, and its aspect is checked where it is set; its bytes under max_bytes
  PDF     every page's trim box (TrimBox, else MediaBox) against the row's size in inches, to 0.01 in; where the row
          states a bleed, the media box and bleed box are the trim size plus the bleed on each side and the trim box sits
          the bleed in from each edge; every font embedded; its bytes under max_bytes
A file the manifest names that is missing, a row id the table lacks, or a format the row does not list, fails.
Exit 0 when every file passes, 1 otherwise.
"""
import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPORTS = ROOT / "work/build/exports/phase-4"
SPECS = ROOT / "work/research/20261121_Platform-Specifications.json"
PT = 72.0
TOL_IN = 0.01


def ratio(s):
    """'4:5' -> Fraction(4, 5); '1.91:1' -> 1.91; None for no aspect."""
    if not s:
        return None
    m = re.fullmatch(r"\s*([\d.]+)\s*:\s*([\d.]+)\s*", str(s))
    if not m:
        return None
    a, b = float(m.group(1)), float(m.group(2))
    return a / b if b else None


def side_ok(got, want, match):
    if want is None:
        return True
    if match == "min":
        return got >= want
    if match == "max":
        return got <= want
    if match == "ratio":
        return True
    return got == want


def check_png(path, row):
    from PIL import Image
    faults, facts = [], {}
    with Image.open(path) as im:
        w, h = im.size
        facts.update(width=w, height=h, mode=im.mode)
    if row.get("unit") not in (None, "px"):
        faults.append(f"the row is in {row.get('unit')}, and a PNG is checked in px")
        return faults, facts
    m = row.get("match") or "exact"
    for side, got, want in (("width", w, row.get("width")), ("height", h, row.get("height"))):
        if not side_ok(got, want, m):
            word = {"min": "at least", "max": "at most"}.get(m, "exactly")
            faults.append(f"{side} is {got} px; the row wants {word} {want} px")
    r = ratio(row.get("aspect"))
    if r and (m == "ratio" or row.get("width") is None or row.get("height") is None):
        if abs(w / h - r) > 0.01 * r:
            faults.append(f"the ratio is {w}:{h} ({w / h:.3f}); the row wants {row.get('aspect')} ({r:.3f})")
    return faults, facts


def check_pdf(path, row):
    from pypdf import PdfReader
    faults, facts = [], {}
    rd = PdfReader(str(path))
    facts["pages"] = len(rd.pages)
    if row.get("unit") != "in":
        faults.append(f"the row is in {row.get('unit')}, and a PDF is checked in inches")
        return faults, facts
    bleed = row.get("bleed") or 0
    tw, th = row.get("width"), row.get("height")
    for i, pg in enumerate(rd.pages, 1):
        mb = [float(v) for v in pg.mediabox]
        tb = [float(v) for v in (pg.trimbox if "/TrimBox" in pg else pg.mediabox)]
        bb = [float(v) for v in (pg.bleedbox if "/BleedBox" in pg else pg.mediabox)]
        size = lambda b: ((b[2] - b[0]) / PT, (b[3] - b[1]) / PT)
        facts[f"page {i}"] = {"media_in": [round(x, 3) for x in size(mb)], "trim_in": [round(x, 3) for x in size(tb)],
                              "bleed_in": [round(x, 3) for x in size(bb)]}
        sw, sh = size(tb)
        if tw is not None and abs(sw - tw) > TOL_IN or th is not None and abs(sh - th) > TOL_IN:
            faults.append(f"page {i}'s trim is {sw:.3f} x {sh:.3f} in; the row wants {tw} x {th} in")
        if bleed:
            mw, mh = size(mb)
            if abs(mw - (tw + 2 * bleed)) > TOL_IN or abs(mh - (th + 2 * bleed)) > TOL_IN:
                faults.append(f"page {i}'s media box is {mw:.3f} x {mh:.3f} in; with {bleed} in bleed it should be {tw + 2 * bleed} x {th + 2 * bleed} in")
            if "/TrimBox" not in pg:
                faults.append(f"page {i} has no trim box, so a printer cannot find the trim inside the bleed")
            elif any(abs(a - b) > TOL_IN * PT for a, b in zip(tb, [mb[0] + bleed * PT, mb[1] + bleed * PT, mb[2] - bleed * PT, mb[3] - bleed * PT])):
                faults.append(f"page {i}'s trim box {tb} does not sit {bleed} in inside its media box {mb}")
            if any(abs(a - b) > TOL_IN * PT for a, b in zip(bb, mb)):
                faults.append(f"page {i}'s bleed box {bb} is not its media box {mb}")
    # every font embedded (print preflight's first question)
    fonts, loose = set(), set()
    for pg in rd.pages:
        res = pg.get("/Resources") or {}
        fd = res.get("/Font") or {}
        for _, ref in fd.items():
            f = ref.get_object()
            sub = str(f.get("/Subtype"))
            if sub == "/Type0" and "/DescendantFonts" in f:
                sub = "/Type0 " + str(f["/DescendantFonts"][0].get_object().get("/Subtype"))
            name = str(f.get("/BaseFont") or f.get("/Name") or "(unnamed)")
            fonts.add(f"{name} ({sub.replace('/', '')})")
            if sub == "/Type3":
                continue   # a Type 3 font draws its glyphs from procedures inside the file: embedded, with no font file
            desc = f.get("/FontDescriptor")
            if desc is None and "/DescendantFonts" in f:
                desc = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            desc = desc.get_object() if desc is not None else None
            if desc is None or not any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                loose.add(name)
    facts["fonts"] = sorted(fonts)
    if loose:
        faults.append(f"{len(loose)} font(s) not embedded: {', '.join(sorted(loose))}")
    return faults, facts


def newest_manifest(d):
    ms = sorted(d.glob("*_Phase-4-Exports-Manifest.json"))
    return ms[-1] if ms else None


def run(exports, specs_path, out=None):
    table = json.loads(Path(specs_path).read_text())
    rows = {r["id"]: r for r in table["rows"]}
    man_path = newest_manifest(exports)
    if not man_path:
        print(f"FAIL no exports manifest in {exports}")
        return 1, []
    man = json.loads(man_path.read_text())
    results, bad = [], 0
    for ent in man["files"]:
        f = exports / ent["file"]
        # a studio proof that no platform governs (the report page's 96 ppi sheet) names its exact size in "expect"
        row = rows.get(ent["platform"]) if ent.get("platform") else (
            {"width": ent["expect"]["width"], "height": ent["expect"]["height"], "unit": "px", "match": "exact", "status": "studio proof"}
            if ent.get("expect") else None)
        faults, facts = [], {}
        if row is None:
            faults.append(f"the table has no row {ent.get('platform')}")
        elif not f.exists():
            faults.append("the file is missing")
        else:
            fmt = ent.get("format") or f.suffix.lstrip(".").lower()
            if row.get("formats") and fmt not in [x.lower() for x in row["formats"]] and not (fmt == "png" and row.get("basis") == "studio-choice"):
                faults.append(f"{fmt} is not among the row's formats ({', '.join(row['formats'])})")
            if fmt == "png":
                fa, facts = check_png(f, row)
            elif fmt == "pdf":
                fa, facts = check_pdf(f, row)
            else:
                fa = [f"no check for {fmt}"]
            faults += fa
            size = f.stat().st_size
            facts["bytes"] = size
            if row.get("max_bytes") and size > row["max_bytes"]:
                faults.append(f"{size:,} bytes, over the row's {row['max_bytes']:,}")
        ok = not faults
        bad += not ok
        results.append({"file": ent["file"], "platform": ent["platform"], "pass": ok, "faults": faults, "facts": facts,
                        "row": {k: row.get(k) for k in ("width", "height", "unit", "aspect", "match", "bleed", "status")} if row else None})
        want = ""
        if row:
            want = f"{row.get('width')} x {row.get('height')} {row.get('unit')}" + (f", {row.get('match')}" if row.get("match") not in (None, "exact") else "") \
                   + (f", bleed {row.get('bleed')} in" if row.get("bleed") else "")
        got = (f"{facts.get('width')} x {facts.get('height')} px" if "width" in facts else
               (f"trim {facts['page 1']['trim_in'][0]} x {facts['page 1']['trim_in'][1]} in, media {facts['page 1']['media_in'][0]} x {facts['page 1']['media_in'][1]} in"
                if "page 1" in facts else ""))
        print(f"{'PASS' if ok else 'FAIL'} {ent['file']}  [{ent['platform']}: {want}]  {got}")
        for x in faults:
            print(f"  - {x}")
    print(f"{len(results) - bad} of {len(results)} exports pass ({man_path.name}; {Path(specs_path).name}, checked {table.get('checked')})")
    if out:
        Path(out).write_text(json.dumps({"manifest": str(man_path), "specs": str(specs_path), "results": results}, indent=1))
    return (1 if bad else 0), results


def self_test():
    import tempfile
    from PIL import Image
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        Image.new("RGB", (1080, 1350), "white").save(d / "a.png")
        Image.new("RGB", (1080, 1349), "white").save(d / "b.png")
        Image.new("RGB", (1440, 3000), "white").save(d / "c.png")
        Image.new("RGB", (1200, 630), "white").save(d / "e.png")
        from pypdf import PdfWriter
        from pypdf.generic import RectangleObject
        w = PdfWriter()
        p = w.add_blank_page(width=630, height=810)
        p.trimbox = RectangleObject([9, 9, 621, 801])
        p.bleedbox = RectangleObject([0, 0, 630, 810])
        w.write(str(d / "f.pdf"))
        w = PdfWriter()
        w.add_blank_page(width=612, height=792)
        w.write(str(d / "g.pdf"))
        specs = {"checked": "test", "rows": [
            {"id": "ig.p", "width": 1080, "height": 1350, "unit": "px", "aspect": "4:5", "match": "exact", "formats": ["png"]},
            {"id": "web", "width": 1440, "height": None, "unit": "px", "match": "exact"},
            {"id": "og", "width": 1200, "height": 630, "unit": "px", "match": "min", "aspect": "1.91:1"},
            {"id": "letter", "width": 8.5, "height": 11, "unit": "in", "bleed": 0.125, "match": "exact", "formats": ["pdf"]}]}
        (d / "specs.json").write_text(json.dumps(specs))
        man = {"files": [{"file": "a.png", "platform": "ig.p"}, {"file": "b.png", "platform": "ig.p"}, {"file": "c.png", "platform": "web"},
                         {"file": "e.png", "platform": "og"}, {"file": "f.pdf", "platform": "letter"}, {"file": "g.pdf", "platform": "letter"},
                         {"file": "h.png", "platform": "ig.p"}, {"file": "a.png", "platform": "nowhere"}]}
        (d / "20260101_Phase-4-Exports-Manifest.json").write_text(json.dumps(man))
        code, res = run(d, d / "specs.json")
        want = [True, False, True, True, True, False, False, False]
        got = [r["pass"] for r in res]
        ok = got == want and code == 1
        print(f"{'pass' if ok else 'FAIL'} self-test: exact PNG, a pixel short, a free height, a minimum, a PDF with bleed, a PDF with none, a missing file and an unknown row: {got}")
        bad += not ok
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exports", default=str(EXPORTS))
    ap.add_argument("--specs", default=str(SPECS))
    ap.add_argument("--json")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(1 if self_test() else 0)
    code, _ = run(Path(a.exports), a.specs, a.json)
    sys.exit(code)
