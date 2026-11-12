"""Phase 3 parts of the guide build (round 0, November 11, 2026): the chart kit's hook, the weight gates and the projection.

guide_build.py imports this module. It never runs on its own except for its self-test:
    python3 -I work/build/scripts/phase-3/guide_charts.py --self-test

The chart hook (engineer notes, contract C7). A specimen fragment holds <div data-oa-chart="ID"></div> where a chart goes.
The build finds the spec ID.chart.json beside the fragment (the editor's plates, the pilot's specimens) or in
work/build/chart-kit/specs/, asks the kit (node work/build/chart-kit/oa-chart.mjs fragments) for the figure by the chosen
drawing method, runs the kit's checks, and puts the figure in place. Each fault is a build warning. The kit's script and
style go into the page once, marked data-oa-chart-kit, and weigh as their own part, "chart kit", charged to chapter 14.

Drawing methods (the round 0 pilot measures each):
  lean       lean inline SVG: the kit's desktop drawing and its phone drawing, written into the page, switched by CSS
  load       drawn when the page loads: the page carries the words, the table and a data island (the spec and the rows the
             chart draws, every column of the data file, as CSV); the kit's one script draws the SVG in the browser
  load-trim  as load, with the island's rows cut to the columns the spec's encode and table name
  load-table as load, with the rows read back from the chart's own table equivalent: the table is lean (a raw value only
             where its words cannot carry it), and the island holds the drawing's spec with no words and, as CSV, only the
             columns the chart draws that the table lacks

The weight gates (Phase 3 proposal, section 3, DR-227): chapter 13 at most 0.25 MB, chapter 15 at most 0.60 MB (warnings
that --strict turns into failures); chapter 14 with the chart kit at most 2,803,941 bytes (DR-238; 1.75 MB until board 1),
a hard stop in every mode; the fonts as their own part, checked against the font manifest's bytes; a projection of the
whole page, today's bytes plus the allocation of every chapter not yet built, against 15.5 MB; and each chapter 14
specimen against its tier's average.

The per-plate share (board 1 apply, item 3): the build report carries chapter 14's room under its stop, after the chart
renderer grown to every form and the parts of the chapter that are not plates, divided among the finished specimens still
to come (weight.projection.chapter_14_per_plate, and a note printed with the build), so each round sees what one plate
may weigh: its figure, words, table, compressed data and plate frame.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / "work/build/chart-kit"
MB = 1_000_000
# Board 1 (DR-238, Dustin, November 12, 2026): chapter 14's stop rises from 1.75 MB to 2,803,941 bytes, the projection of
# its 97 finished specimens with each chart's data carried compressed and every table kept live (D3-190's recommended
# figure, read by weight_options.py from a fresh strict build and pilot). It stays a hard stop in every mode, and the
# chapter's allocation in the page's projection moves with it.
CHAPTER_14_STOP = 2_803_941
CEILING = {"13": 0.25 * MB, "14": CHAPTER_14_STOP, "15": 0.60 * MB}
HARD_STOP = "14"
PAGE_BUDGET = 15.5 * MB
# The allocation of each chapter not yet built (proposal section 3): Phase 3's three at their ceilings, Phase 4's seven
# sharing 2.54 MB, Phase 5's two sharing 0.40 MB
ALLOCATION = {"13": 0.25 * MB, "14": CHAPTER_14_STOP, "15": 0.60 * MB,
              **{n: 2.54 * MB / 7 for n in ("16", "20", "21", "22", "23", "24", "25")},
              **{n: 0.40 * MB / 2 for n in ("27", "28")}}
# A chapter 14 specimen's average by tier (proposal section 3: words, table equivalent and data); "far over" is three times it
TIER_AVERAGE = {"core": 8 * 1024, "extended": 8 * 1024, "reference": 4 * 1024, "avoid": 2 * 1024}
FAR_OVER = 3.0
# The per-plate share (item 3 of the board 1 apply brief). Chapter 14 holds 97 finished specimens (the proposal's core and
# extended forms, section 3), and its renderer grows to one module per form at today's average. The parts of the chapter
# that are not plates keep the proposal's allocation, as the pilot projects them (chart_pilot.py), until a round builds and
# measures one: then that round sets its entry here to 0, since its bytes now sit in chapter 14's measured section.
PLATES = 97
FORMS = 97
NOT_PLATES = {"reference sketches (22 at 4 KB) and avoid entries (8 at 2 KB)": 22 * 4096 + 8 * 2048,
              "rules, selection guide and palette specification": 300_000,
              "three complex examples": 90_000,
              "shared map geometry": 250_000}
KIT_SIZES = {}                   # set by expand(): the kit's parts as the page carries them, from oa-chart.mjs fragments
METHODS = ("lean", "load", "load-trim", "load-table")
DEFAULT_METHOD = "load-table"    # chosen by the round 0 pilot (engineer notes, "The drawing method")
CHART_RE = re.compile(r'<div data-oa-chart="([a-z0-9][a-z0-9-]*)"(?:\s+data-oa-ground="(newsprint|charcoal)")?\s*>\s*</div>')
KIT_RE = re.compile(r'<(style|script) data-oa-chart-kit>.*?</\1>', re.S)
FONT_TOLERANCE = 0.02            # base64 adds a third; the part may differ from 4/3 of the files by the @font-face text


def spec_for(cid, spec_dirs):
    for d in spec_dirs:
        p = Path(d) / f"{cid}.chart.json"
        if p.exists():
            return p
    p = KIT / "specs" / f"{cid}.json"
    return p if p.exists() else None


def expand(page, method, spec_dirs, warn, where_of=None):
    """Replace every chart placeholder in the page with the kit's figure; return the page and a record of each chart."""
    hits = list(CHART_RE.finditer(page))
    if not hits:
        return page, {}
    if method not in METHODS:
        warn("chart kit", f"drawing method {method!r} is not one of {', '.join(METHODS)}; {DEFAULT_METHOD} is used")
        method = DEFAULT_METHOD
    items, seen = [], {}
    for m in hits:
        cid, ground = m.group(1), m.group(2) or "newsprint"
        if cid in seen:
            warn(f"chart {cid}", "the chart is placed twice; each chart appears once")
            continue
        p = spec_for(cid, spec_dirs)
        if not p:
            warn(f"chart {cid}", f"no spec: write {cid}.chart.json beside the specimen, or work/build/chart-kit/specs/{cid}.json")
            seen[cid] = None
            continue
        seen[cid] = p
        items.append({"key": cid, "spec": str(p), "ground": ground, "fid": f"oac-{cid}", "widths": [1440, 390]})
    out = {}
    if items:
        with tempfile.TemporaryDirectory() as td:
            lp, op = Path(td) / "in.json", Path(td) / "out.json"
            lp.write_text(json.dumps({"method": method, "items": items}))
            r = subprocess.run(["node", str(KIT / "oa-chart.mjs"), "fragments", "--in", str(lp), "--out", str(op)],
                               capture_output=True, text=True, cwd=str(ROOT))
            if r.returncode != 0 or not op.exists():
                warn("chart kit", f"the kit did not draw the charts: {(r.stderr or r.stdout).strip()[:400]}")
                return page, {}
            out = json.loads(op.read_text())
    KIT_SIZES.clear()
    KIT_SIZES.update(out.get("kit_sizes") or {})
    figs = out.get("items", {})
    rec = {}

    def repl(m):
        cid = m.group(1)
        it = figs.get(cid)
        if not it or not it.get("html"):
            return m.group(0)
        for f in it.get("faults", []):
            warn(f"chart {cid}", f)
        rec[cid] = {"id": it.get("id"), "form": it.get("form"), "tier": it.get("tier"), "rows": it.get("rows"),
                    "bytes": len(it["html"].encode()), "spec": (str(Path(seen[cid]).relative_to(ROOT)) if ROOT in Path(seen[cid]).parents else str(seen[cid])) if seen.get(cid) else None}
        return it["html"]

    page = CHART_RE.sub(repl, page)
    if rec:
        style = f"<style data-oa-chart-kit>\n{out['kit_css']}\n</style>"
        page = page.replace("</head>", style + "\n</head>", 1)
        if method in ("load", "load-trim", "load-table"):
            script = f"<script data-oa-chart-kit>\n{out['kit_js']}\nOAChart.words = {json.dumps(out['words'], ensure_ascii=False)};\n</script>"
            i = page.rfind("<script>")
            page = page[:i] + script + "\n" + page[i:]
    return page, rec


def kit_bytes(page):
    return sum(len(m.group(0).encode()) for m in KIT_RE.finditer(page))


def gates(weights, charts, fonts_file_bytes, present, warn):
    """The Phase 3 weight gates on a weighed page. Returns (stop message or None, the projection record)."""
    ch = {n: v["bytes"] for n, v in weights["chapters"].items()}
    kit = weights["parts"].get("chart kit", 0)
    for n in ("13", "15"):
        if n in ch and ch[n] > CEILING[n]:
            warn(f"chapter {n}", f"weighs {ch[n] / MB:.3f} MB, over its Phase 3 ceiling of {CEILING[n] / MB:.2f} MB (proposal section 3)")
    stop = None
    c14 = ch.get("14", 0) + (kit if charts or "14" in ch else 0)
    if c14 > CEILING[HARD_STOP]:
        stop = (f"chapter 14 with the chart kit weighs {c14:,} bytes ({c14 / MB:.3f} MB), over its hard stop of "
                f"{CEILING[HARD_STOP]:,.0f} bytes (DR-227, raised by DR-238); the build stops in every mode")
    # the fonts as their own part, against the manifest's files
    fp = weights["parts"].get("fonts", 0)
    if fonts_file_bytes:
        want = fonts_file_bytes * 4 / 3
        if abs(fp - want) > want * FONT_TOLERANCE + 4096:
            warn("page weight", f"the fonts part weighs {fp:,} bytes; the font manifest's files come to {want:,.0f} as embedded data")
    # each chapter 14 specimen against its tier's average
    for cid, r in sorted(charts.items()):
        if not cid.startswith("s-14-"):
            continue
        avg = TIER_AVERAGE.get(r.get("tier") or "core", TIER_AVERAGE["core"])
        if r["bytes"] > FAR_OVER * avg:
            warn(f"chart {cid}", f"weighs {r['bytes']:,} bytes, far over its tier's average of {avg:,} ({FAR_OVER:g} times is {FAR_OVER * avg:,.0f}); "
                                 "trim the table equivalent or the island, or move rows to a download")
    # the projection: today's bytes plus every unbuilt chapter's allocation
    unbuilt = {n: a for n, a in ALLOCATION.items() if n not in present}
    built14 = "14" in present
    proj = weights["bytes"] + sum(unbuilt.values()) - (kit if not built14 and kit else 0)
    rec = {"page_bytes": weights["bytes"], "unbuilt": {n: round(a) for n, a in sorted(unbuilt.items())},
           "projected_bytes": round(proj), "budget": PAGE_BUDGET, "chapter_14_with_kit": c14, "chart_kit": kit}
    share = per_plate(ch.get("14", 0), kit, charts, KIT_SIZES)
    if share:
        rec["chapter_14_per_plate"] = share
    if proj > PAGE_BUDGET:
        warn("page weight", f"the projected page weighs {proj / MB:.2f} MB (today's {weights['bytes'] / MB:.2f} MB plus "
                            f"{sum(unbuilt.values()) / MB:.2f} MB for the chapters not yet built), over its budget of {PAGE_BUDGET / MB:.1f} MB")
    return stop, rec


def per_plate(ch14, kit, charts, sizes):
    """Chapter 14's room under its stop, divided among the finished specimens still to come.

    room = the stop, less the renderer grown to FORMS forms (the kit in the page without its map geometry, plus a module at
    today's average for each form still to come), less the parts that are not plates (NOT_PLATES), less what chapter 14's
    section weighs now; plates to come = PLATES less the core and extended charts placed in chapter 14. Each plate's share
    covers its figure, words, table equivalent, compressed data and plate frame. None while the page carries no kit."""
    if not kit or not sizes or not sizes.get("registered"):
        return None
    forms_bytes = sum((sizes.get("forms") or {}).values())
    avg = forms_bytes / sizes["registered"]
    renderer = kit - sizes.get("geo", 0) + max(0, FORMS - sizes["registered"]) * avg
    placed = sum(1 for cid, r in charts.items() if cid.startswith("s-14-") and (r.get("tier") or "core") in ("core", "extended"))
    to_come = max(1, PLATES - placed)
    reserved = sum(NOT_PLATES.values())
    room = CEILING[HARD_STOP] - renderer - reserved - ch14
    share = room / to_come
    line = (f"chapter 14's share per plate: {share:,.0f} bytes for each of the {to_come} finished specimens still to come "
            f"({room:,.0f} bytes of room under its {CEILING[HARD_STOP]:,.0f} byte stop, after the renderer grown to {FORMS} forms, "
            f"{renderer:,.0f}, the parts that are not plates, {reserved:,}, and the chapter as built, {ch14:,}); a plate's share covers "
            "its figure, words, table, compressed data and plate frame")
    return {"per_plate": round(share), "plates_to_come": to_come, "plates_placed": placed, "room": round(room),
            "stop": CEILING[HARD_STOP], "renderer_grown": round(renderer), "renderer_now": kit - sizes.get("geo", 0),
            "forms_registered": sizes["registered"], "form_average": round(avg), "not_plates": NOT_PLATES,
            "chapter_14_now": ch14, "line": line}


def self_test():
    """Plant chapter 14 one byte over, a specimen far over its form's average and a projection over the budget; each
    must be caught. Also: chapters 13 and 15 over their ceilings, and a fonts part that disagrees with the manifest."""
    bad = 0

    def run(weights, charts, fonts, present):
        got = []
        stop, rec = gates(weights, charts, fonts, present, lambda w, m: got.append(f"{w}: {m}"))
        return stop, rec, got

    base = {"bytes": 9_500_000, "parts": {"chart kit": 100_000, "fonts": int(300_000 * 4 / 3)}, "chapters": {}}
    cases = []
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": int(CEILING["14"]) - 100_000 + 1}
    cases.append(("chapter 14 one byte over its hard stop", w, {}, 300_000, {"14"}, "stop", None))
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": int(CEILING["14"]) - 100_000}
    cases.append(("chapter 14 exactly at its stop passes", w, {}, 300_000, {"14"}, "no stop", None))
    cases.append(("a specimen far over its form's average", base, {"s-14-s99": {"tier": "core", "bytes": 3 * 8 * 1024 + 1}}, 300_000, set(), "warn", "far over"))
    cases.append(("a specimen just under three times passes", base, {"s-14-s98": {"tier": "core", "bytes": 3 * 8 * 1024}}, 300_000, set(), "none", "far over"))
    w = json.loads(json.dumps(base)); w["bytes"] = int(PAGE_BUDGET - sum(ALLOCATION.values()) + 1 + 100_000)
    cases.append(("a projection over the budget", w, {}, 300_000, set(), "warn", "projected page"))
    w = json.loads(json.dumps(base)); w["chapters"]["13"] = {"bytes": int(CEILING["13"]) + 1}
    cases.append(("chapter 13 over its ceiling", w, {}, 300_000, {"13"}, "warn", "chapter 13"))
    w = json.loads(json.dumps(base)); w["chapters"]["15"] = {"bytes": int(CEILING["15"]) + 1}
    cases.append(("chapter 15 over its ceiling", w, {}, 300_000, {"15"}, "warn", "chapter 15"))
    cases.append(("fonts that disagree with the manifest", base, {}, 200_000, set(), "warn", "fonts part"))
    # board 1 (DR-238): the stop is 2,803,941 bytes, a hard stop at that figure; the old 1.75 MB stop no longer stops
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": 2_803_941 - 100_000 + 1}
    cases.append(("chapter 14 at 2,803,942 bytes with the kit stops (DR-238)", w, {}, 300_000, {"14"}, "stop", None))
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": 2_803_941 - 100_000}
    cases.append(("chapter 14 at 2,803,941 bytes with the kit passes", w, {}, 300_000, {"14"}, "no stop", None))
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": 1_750_000 - 100_000 + 1}
    cases.append(("chapter 14 one byte over the old 1.75 MB stop passes now", w, {}, 300_000, {"14"}, "no stop", None))
    w = json.loads(json.dumps(base)); w["bytes"] = int(PAGE_BUDGET - sum(ALLOCATION.values()) + 100_000)
    cases.append(("a projection exactly at 15.5 MB, chapter 14 at its new allocation, passes", w, {}, 300_000, set(), "none", "projected page"))
    for name, weights, charts, fonts, present, want, text in cases:
        stop, rec, got = run(weights, charts, fonts, present)
        if want == "stop":
            ok = stop is not None
        elif want == "no stop":
            ok = stop is None
        elif want == "warn":
            ok = any(text in g for g in got)
        else:
            ok = not any(text in g for g in got)
        print(f"{'pass' if ok else 'FAIL'} {name}")
        bad += not ok
    # the hook's pattern and the kit's marks
    page = '<html><head></head><body><div data-oa-chart="s-14-s01"></div><script>x</script></body></html>'
    ok = [m.group(1) for m in CHART_RE.finditer(page)] == ["s-14-s01"]
    print(f"{'pass' if ok else 'FAIL'} the hook finds a placeholder")
    bad += not ok
    ok = kit_bytes('<style data-oa-chart-kit>abc</style><script data-oa-chart-kit>de</script>') == len('<style data-oa-chart-kit>abc</style>') + len('<script data-oa-chart-kit>de</script>')
    print(f"{'pass' if ok else 'FAIL'} the chart kit weighs as its own part")
    bad += not ok
    # the stop's figure, its allocation in the projection, and the per-plate share's arithmetic
    ok = CEILING[HARD_STOP] == 2_803_941 and ALLOCATION["14"] == 2_803_941 and HARD_STOP == "14"
    print(f"{'pass' if ok else 'FAIL'} chapter 14's stop and allocation are 2,803,941 bytes (DR-238)")
    bad += not ok
    sz = {"registered": 10, "geo": 5_000, "forms": {"a.js": 30_000, "b.js": 10_000}}
    sh = per_plate(0, 105_000, {"s-14-s01": {"tier": "core"}, "s-14-s02": {"tier": "reference"}, "s-13-1-correct": {"tier": "core"}}, sz)
    want = (2_803_941 - (100_000 + 87 * 4_000) - sum(NOT_PLATES.values())) / 96
    ok = sh is not None and sh["plates_to_come"] == 96 and sh["renderer_grown"] == 448_000 and abs(sh["per_plate"] - want) < 1
    print(f"{'pass' if ok else 'FAIL'} the per-plate share: the stop less the grown renderer and the parts that are not plates, over the core and extended plates to come")
    bad += not ok
    ok = per_plate(0, 0, {}, {}) is None
    print(f"{'pass' if ok else 'FAIL'} no per-plate share on a page with no chart kit")
    bad += not ok
    print("guide_charts self-test: " + ("every planted fault caught" if not bad else f"{bad} failed"))
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(__doc__)
