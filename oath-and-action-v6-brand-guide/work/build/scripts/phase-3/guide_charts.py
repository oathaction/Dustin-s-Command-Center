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

The weight gates (Phase 3 proposal, section 3, DR-227): chapter 13 at most 0.25 MB, chapter 15 at most 0.60 MB (warnings
that --strict turns into failures); chapter 14 with the chart kit at most 1.75 MB, a hard stop in every mode; the fonts as
their own part, checked against the font manifest's bytes; a projection of the whole page, today's bytes plus the
allocation of every chapter not yet built, against 15.5 MB; and each chapter 14 specimen against its tier's average.
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
CEILING = {"13": 0.25 * MB, "14": 1.75 * MB, "15": 0.60 * MB}
HARD_STOP = "14"
PAGE_BUDGET = 15.5 * MB
# The allocation of each chapter not yet built (proposal section 3): Phase 3's three at their ceilings, Phase 4's seven
# sharing 2.54 MB, Phase 5's two sharing 0.40 MB
ALLOCATION = {"13": 0.25 * MB, "14": 1.75 * MB, "15": 0.60 * MB,
              **{n: 2.54 * MB / 7 for n in ("16", "20", "21", "22", "23", "24", "25")},
              **{n: 0.40 * MB / 2 for n in ("27", "28")}}
# A chapter 14 specimen's average by tier (proposal section 3: words, table equivalent and data); "far over" is three times it
TIER_AVERAGE = {"core": 8 * 1024, "extended": 8 * 1024, "reference": 4 * 1024, "avoid": 2 * 1024}
FAR_OVER = 3.0
METHODS = ("lean", "load", "load-trim")
DEFAULT_METHOD = "load-trim"     # chosen by the round 0 pilot (engineer notes, "The drawing method")
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
        if method in ("load", "load-trim"):
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
                f"{CEILING[HARD_STOP] / MB:.2f} MB (DR-227); the build stops in every mode")
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
    if proj > PAGE_BUDGET:
        warn("page weight", f"the projected page weighs {proj / MB:.2f} MB (today's {weights['bytes'] / MB:.2f} MB plus "
                            f"{sum(unbuilt.values()) / MB:.2f} MB for the chapters not yet built), over its budget of {PAGE_BUDGET / MB:.1f} MB")
    return stop, rec


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
    print("guide_charts self-test: " + ("every planted fault caught" if not bad else f"{bad} failed"))
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(__doc__)
