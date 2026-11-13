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
# DR-271 (November 13, 2026): the one fixed limit is the page, one file under 16 MB; past it the build writes no page, in
# every mode. Every allocation inside the page (chapter ceilings, chapter 14's stop, the chart kit and map geometry parts,
# the rules' allowance, a chart's tier average) is a figure the build reports as a note; the projection over 15.5 MB stays a
# warning, the page limit's early warning.
PAGE_LIMIT = 16 * MB
# The allocation of each chapter not yet built (proposal section 3): Phase 3's three at their ceilings, Phase 4's seven
# sharing 2.54 MB, Phase 5's two sharing 0.40 MB
ALLOCATION = {"13": 0.25 * MB, "14": CHAPTER_14_STOP, "15": 0.60 * MB,
              **{n: 2.54 * MB / 7 for n in ("16", "20", "21", "22", "23", "24", "25")},
              **{n: 0.40 * MB / 2 for n in ("27", "28")}}
# A chapter 14 specimen's average by tier (proposal section 3: words, table equivalent and data); "far over" is three times it
TIER_AVERAGE = {"core": 8 * 1024, "extended": 8 * 1024, "reference": 4 * 1024, "avoid": 2 * 1024}
FAR_OVER = 3.0
# Round 0's specimens Dustin approved on board 1 at their measured bytes (DR-237's board, D3-190's projection, which set
# chapter 14's stop with them in it): the far-over test lists them by name with their bytes instead of failing them, up to
# the bytes board 1 measured (the pilot with JSON islands); every other specimen keeps the test
BOARD_1_APPROVED = {"s-14-s05": 31_961, "s-14-s13": 47_212}
# The per-plate share (item 3 of the board 1 apply brief). Chapter 14 holds 97 finished specimens (the proposal's core and
# extended forms, section 3), and its renderer grows to one module per form at today's average. The parts of the chapter
# that are not plates keep the proposal's allocation, as the pilot projects them (chart_pilot.py), until a round builds and
# measures one: then that round sets its entry here to 0, since its bytes now sit in chapter 14's measured section.
PLATES = 97
FORMS = 97
NOT_PLATES = {"reference sketches (22 at 4 KB) and avoid entries (8 at 2 KB)": 22 * 4096 + 8 * 2048,
              # round 1 built rules 14.1 to 14.14 with their plates and the opener, now measured in chapter 14's section;
              # round 5's selection guide and palette specification keep their 0.10 MB (round 1 brief, Editor)
              "selection guide and palette specification": 100_000,
              "three complex examples": 90_000,
              "shared map geometry": 250_000}
# Call 4 (D3-479, round 1 fix pass): rules 14.1 to 14.14 with the opener take 0.20 MB and 12,288 bytes more, moved from
# chapter 14's room, so the eight narrow plates draw at their partner's width; the build measures them and warns past it.
# The sketch entries count whole (the creative director's weight paragraph): each one still to come is reserved at its
# sketch's cap (4,096 bytes for both tiers since D3-486) plus the words and frame the built sketch entries measure.
RULES_ALLOWANCE = 200_000 + 12_288
# R3-2 (round 3): the map geometry (geo.js, every layer every map shares) is carried once and weighed apart, against its
# own allowance; past it the build warns (and --strict fails)
GEOMETRY_ALLOWANCE = NOT_PLATES["shared map geometry"]
SKETCH_ENTRIES = {"reference": 22, "avoid": 8}
SKETCH_CAP = 4096
SKETCH_WORDS_DEFAULT = 3_800     # the creative director's measure of the four built, before the page measures its own
RULE_START = re.compile(r'<div class="rule" id="rule-14-(\d+)" data-rule="14\.\d+">')
NEXT_BLOCK = re.compile(r'<div class="rule"|<div class="rule-group"|<div class="closer"|<nav class="chapnav"|</section>')


def chapter14_parts(page):
    """Chapter 14's measured parts on a built page: rules 14.1 to 14.14 (each block with its plates), the opener's plate,
    and every sketch entry whole (its block with its plate) with its sketch's bytes. None when chapter 14 is not there."""
    i = page.find('id="data-visualization"')
    if i < 0:
        return None
    start = page.rfind("<section", 0, i)
    end = page.find("</section>", i)
    sec = page[start:end]
    size = lambda x: len(x.encode())
    rules, sketches = 0, []
    for m in RULE_START.finditer(sec):
        n = m.group(m.lastindex)
        nx = NEXT_BLOCK.search(sec, m.end())
        blk = sec[m.start():nx.start() if nx else len(sec)]
        if int(n) <= 14:
            rules += size(blk)
        k = re.search(r'<figure class="plate plate--(avoid|sketch)\b', blk)
        if k:
            st = re.search(r'data-specimen="s-14-\d+-sketch"[^>]*>(.*?)</div></div><figcaption', blk, re.S)
            sk = sum(size(x) for x in re.findall(r"<svg\b.*?</svg>", st.group(1), re.S)) if st else 0
            sketches.append({"rule": "14." + n, "kind": k.group(1), "bytes": size(blk), "sketch_bytes": sk})
    op = re.search(r'<figure class="plate plate--opener[^"]*"[^>]*>.*?</figure>', sec, re.S)
    opener = size(op.group(0)) if op else 0
    # ED-E13 (round 2): the rule plates' shared style, printed once at the chapter's head, counts with the rules it serves
    pc = re.search(r'<style data-plate-css>.*?</style>', sec, re.S)
    css = size(pc.group(0)) if pc else 0
    return {"rules_1_to_14": rules, "opener": opener, "plate_css": css, "rules_and_opener": rules + opener + css, "allowance": RULES_ALLOWANCE, "sketch_entries": sketches}
# Chapters Phase 3 is still building: the projection counts each at no less than its allocation until its round ends
IN_PROGRESS = ("14", "15")
ENTRY_PLATE = re.compile(r"^s-14-s\d+$")   # an entry's specimen (R1-C3); a chapter-wide rule's plates (s-14-1-line) count under NOT_PLATES
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
    # round 1 (contract R1-C3): chapter 14 places a maker's spec sNN as s-14-sNN, so its weight counts as chapter 14's plate
    m = re.match(r"^s-14-(s\d+)$", cid)
    if not p.exists() and m:
        p = KIT / "specs" / f"{m.group(1)}.json"
    return p if p.exists() else None


def expand(page, method, spec_dirs, warn, where_of=None, note=None):
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
        it = {"key": cid, "spec": str(p), "ground": ground, "fid": f"oac-{cid}", "widths": [1440, 390]}
        # D3-487 (BC S3): a chapter 14 entry whose form changes on a phone also shows its phone drawing at a desk
        if re.match(r"^s-14-s\d+$", cid):
            try:
                if json.loads(Path(p).read_text()).get("phone") == "differs":
                    it["phone_view"] = True
            except (OSError, ValueError):
                pass
        items.append(it)
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
        # round 2 fix pass: the kit's own gate faults (words crossed, red past its share) print as notes here; the kit's
        # build fails them
        for f in it.get("notes", []):
            (note or (lambda m: None))(f"chart {cid}: kit build fault, listed here: {f}")
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


def gates(weights, charts, fonts_file_bytes, present, warn, note=None):
    """The Phase 3 weight gates on a weighed page. Returns (stop message or None, the projection record). DR-271: the page's
    16 MB limit stops the build; an allocation past its figure goes to note(where, message), reported and never failing;
    the projection and the fonts' agreement with their manifest still warn."""
    note = note or (lambda w, m: None)
    ch = {n: v["bytes"] for n, v in weights["chapters"].items()}
    # R3-2: the page weighs the map geometry apart from the renderer; inside chapter 14's stop they count together
    kit = weights["parts"].get("chart kit", 0) + weights["parts"].get("map geometry", 0)
    for n in ("13", "15"):
        if n in ch and ch[n] > CEILING[n]:
            note(f"chapter {n}", f"weighs {ch[n] / MB:.3f} MB, over its Phase 3 ceiling of {CEILING[n] / MB:.2f} MB (proposal section 3), reported (DR-271)")
    stop = None
    if weights["bytes"] > PAGE_LIMIT:
        stop = (f"the page weighs {weights['bytes']:,} bytes, over the one fixed limit of {PAGE_LIMIT:,} (one file under 16 MB, DR-271); "
                "the build stops in every mode")
    c14 = ch.get("14", 0) + (kit if charts or "14" in ch else 0)
    if c14 > CEILING[HARD_STOP]:
        note("chapter 14", f"with the chart kit weighs {c14:,} bytes ({c14 / MB:.3f} MB), over its stop of {CEILING[HARD_STOP]:,.0f} bytes "
                           "(DR-227, raised by DR-238), reported; the studio raises it and logs the raise (DR-271)")
    # the fonts as their own part, against the manifest's files
    fp = weights["parts"].get("fonts", 0)
    if fonts_file_bytes:
        want = fonts_file_bytes * 4 / 3
        if abs(fp - want) > want * FONT_TOLERANCE + 4096:
            warn("page weight", f"the fonts part weighs {fp:,} bytes; the font manifest's files come to {want:,.0f} as embedded data")
    # each chapter 14 specimen against its tier's average
    approved = {}
    for cid, r in sorted(charts.items()):
        if not cid.startswith("s-14-"):
            continue
        avg = TIER_AVERAGE.get(r.get("tier") or "core", TIER_AVERAGE["core"])
        if r["bytes"] > FAR_OVER * avg and cid in BOARD_1_APPROVED and r["bytes"] <= BOARD_1_APPROVED[cid]:
            approved[cid] = {"bytes": r["bytes"], "board_1_bytes": BOARD_1_APPROVED[cid], "tier_average": avg}
        elif r["bytes"] > FAR_OVER * avg:
            note(f"chart {cid}", f"weighs {r['bytes']:,} bytes, far over its tier's average of {avg:,} ({FAR_OVER:g} times is {FAR_OVER * avg:,.0f}), "
                                 "reported (DR-271)")
    # the projection: today's bytes plus every unbuilt chapter's allocation
    unbuilt = {n: a for n, a in ALLOCATION.items() if n not in present}
    built14 = "14" in present
    # a chapter still being built (IN_PROGRESS) counts at no less than its allocation: round 1 places part of chapter 15,
    # and its measured bytes alone would hand the rest of its allocation to the page's room
    held = {}
    for n in IN_PROGRESS:
        if n in present:
            now = ch.get(n, 0) + (kit if n == "14" else 0)
            if now < ALLOCATION[n]:
                held[n] = ALLOCATION[n] - now
    proj = weights["bytes"] + sum(unbuilt.values()) - (kit if not built14 and kit else 0) + sum(held.values())
    rec = {"page_bytes": weights["bytes"], "unbuilt": {n: round(a) for n, a in sorted(unbuilt.items())},
           "held_to_allocation": {n: round(v) for n, v in sorted(held.items())},
           "projected_bytes": round(proj), "budget": PAGE_BUDGET, "chapter_14_with_kit": c14, "chart_kit": kit,
           "far_over_approved": approved}
    parts14 = weights.get("chapter_14_parts")
    if parts14:
        rec["chapter_14_rules"] = {k: parts14.get(k, 0) for k in ("rules_1_to_14", "opener", "plate_css", "rules_and_opener", "allowance")}
        if parts14["rules_and_opener"] > RULES_ALLOWANCE:
            note("chapter 14", f"rules 14.1 to 14.14 with the opener weigh {parts14['rules_and_opener']:,} bytes, over their {RULES_ALLOWANCE:,} "
                               "(0.20 MB and the 12,288 bytes call 4 moved to them), reported (DR-271)")
    geo = weights["parts"].get("map geometry") or ((KIT_SIZES or {}).get("geo", 0) if kit else 0)
    if geo:
        rec["map_geometry"] = {"bytes": geo, "allowance": GEOMETRY_ALLOWANCE, "room": GEOMETRY_ALLOWANCE - geo}
        if geo > GEOMETRY_ALLOWANCE:
            note("chart kit", f"the shared map geometry (geo.js) weighs {geo:,} bytes, over its {GEOMETRY_ALLOWANCE:,} byte allowance (R3-2), reported (DR-271)")
    share = per_plate(ch.get("14", 0), kit, charts, KIT_SIZES, parts14)
    if share:
        rec["chapter_14_per_plate"] = share
    if proj > PAGE_BUDGET:
        warn("page weight", f"the projected page weighs {proj / MB:.2f} MB (today's {weights['bytes'] / MB:.2f} MB plus "
                            f"{sum(unbuilt.values()) / MB:.2f} MB for the chapters not yet built and {sum(held.values()) / MB:.2f} MB still to come in "
                            f"chapters being built), over its budget of {PAGE_BUDGET / MB:.1f} MB")
    return stop, rec


def not_plates(parts14):
    """The reserve for chapter 14's parts that are not finished core and extended plates. With the page's measure (call 4):
    the sketch entries still to come whole, and what rules 14.1 to 14.14 have not yet spent of their allowance; without
    it, the proposal's figures."""
    if not parts14:
        return dict(NOT_PLATES)
    built = parts14.get("sketch_entries") or []
    words = (sum(x["bytes"] - x["sketch_bytes"] for x in built) / len(built)) if built else SKETCH_WORDS_DEFAULT
    to_come = max(0, sum(SKETCH_ENTRIES.values()) - len(built))
    out = {k: v for k, v in NOT_PLATES.items() if not k.startswith("reference sketches")}
    out[f"sketch entries whole ({to_come} to come at {SKETCH_CAP:,} bytes of sketch and {words:,.0f} of words and frame)"] = round(to_come * (SKETCH_CAP + words))
    out["rules 14.1 to 14.14 with the opener, unspent of their allowance (call 4)"] = max(0, RULES_ALLOWANCE - parts14["rules_and_opener"])
    return out


def per_plate(ch14, kit, charts, sizes, parts14=None):
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
    placed = sum(1 for cid, r in charts.items() if ENTRY_PLATE.match(cid)
                 and (r.get("tier") or "core").split(",")[0] in ("core", "extended"))
    to_come = max(1, PLATES - placed)
    reserve = not_plates(parts14)
    reserved = sum(reserve.values())
    room = CEILING[HARD_STOP] - renderer - reserved - ch14
    share = room / to_come
    line = (f"chapter 14's share per plate: {share:,.0f} bytes for each of the {to_come} finished specimens still to come "
            f"({room:,.0f} bytes of room under its {CEILING[HARD_STOP]:,.0f} byte stop, after the renderer grown to {FORMS} forms, "
            f"{renderer:,.0f}, the parts that are not plates, {reserved:,}, and the chapter as built, {ch14:,}); a plate's share covers "
            "its figure, words, table, compressed data and plate frame")
    return {"per_plate": round(share), "plates_to_come": to_come, "plates_placed": placed, "room": round(room),
            "stop": CEILING[HARD_STOP], "renderer_grown": round(renderer), "renderer_now": kit - sizes.get("geo", 0),
            "forms_registered": sizes["registered"], "form_average": round(avg), "not_plates": reserve,
            "chapter_14_now": ch14, "line": line}


def self_test():
    """Plant chapter 14 one byte over, a specimen far over its form's average and a projection over the budget; each
    must be caught. Also: chapters 13 and 15 over their ceilings, and a fonts part that disagrees with the manifest."""
    bad = 0

    def run(weights, charts, fonts, present):
        got, noted = [], []
        stop, rec = gates(weights, charts, fonts, present, lambda w, m: got.append(f"{w}: {m}"), lambda w, m: noted.append(f"{w}: {m}"))
        run.noted = noted
        return stop, rec, got

    base = {"bytes": 9_500_000, "parts": {"chart kit": 100_000, "fonts": int(300_000 * 4 / 3)}, "chapters": {}}
    cases = []
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": int(CEILING["14"]) - 100_000 + 1}
    cases.append(("DR-271: chapter 14 one byte over its stop is reported, never stopped", w, {}, 300_000, {"14"}, "note", "over its stop of 2,803,941"))
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": int(CEILING["14"]) - 100_000}
    cases.append(("chapter 14 exactly at its stop passes", w, {}, 300_000, {"14"}, "no stop", None))
    cases.append(("DR-271: a specimen far over its form's average is reported", base, {"s-14-s99": {"tier": "core", "bytes": 3 * 8 * 1024 + 1}}, 300_000, set(), "note", "far over"))
    cases.append(("a specimen just under three times passes", base, {"s-14-s98": {"tier": "core", "bytes": 3 * 8 * 1024}}, 300_000, set(), "none", "far over"))
    w = json.loads(json.dumps(base)); w["bytes"] = int(PAGE_BUDGET - sum(ALLOCATION.values()) + 1 + 100_000)
    cases.append(("a projection over the budget", w, {}, 300_000, set(), "warn", "projected page"))
    w = json.loads(json.dumps(base)); w["chapters"]["13"] = {"bytes": int(CEILING["13"]) + 1}
    cases.append(("DR-271: chapter 13 over its ceiling is reported", w, {}, 300_000, {"13"}, "note", "chapter 13"))
    w = json.loads(json.dumps(base)); w["chapters"]["15"] = {"bytes": int(CEILING["15"]) + 1}
    cases.append(("DR-271: chapter 15 over its ceiling is reported", w, {}, 300_000, {"15"}, "note", "chapter 15"))
    w = json.loads(json.dumps(base)); w["bytes"] = PAGE_LIMIT + 1
    cases.append(("DR-271: a page one byte over 16 MB stops", w, {}, 300_000, set(), "stop", None))
    w = json.loads(json.dumps(base)); w["bytes"] = PAGE_LIMIT
    cases.append(("DR-271: a page at 16,000,000 bytes is not stopped by the limit", w, {}, 300_000, set(), "no stop", None))
    cases.append(("fonts that disagree with the manifest", base, {}, 200_000, set(), "warn", "fonts part"))
    # board 1 (DR-238): the stop is 2,803,941 bytes, a hard stop at that figure; the old 1.75 MB stop no longer stops
    w = json.loads(json.dumps(base)); w["chapters"]["14"] = {"bytes": 2_803_941 - 100_000 + 1}
    cases.append(("DR-271: chapter 14 at 2,803,942 bytes with the kit is reported, never stopped", w, {}, 300_000, {"14"}, "no stop", None))
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
        elif want == "note":
            ok = stop is None and any(text in g for g in run.noted) and not any(text in g for g in got)
        else:
            ok = not any(text in g for g in got)
        print(f"{'pass' if ok else 'FAIL'} {name}")
        bad += not ok
    # the hook's pattern and the kit's marks
    page = '<html><head></head><body><div data-oa-chart="s-14-s01"></div><script>x</script></body></html>'
    ok = [m.group(1) for m in CHART_RE.finditer(page)] == ["s-14-s01"]
    print(f"{'pass' if ok else 'FAIL'} the hook finds a placeholder")
    bad += not ok
    ok = spec_for("s-14-s03", []) == KIT / "specs" / "s03.json" and spec_for("s-14-s999", []) is None
    print(f"{'pass' if ok else 'FAIL'} chapter 14's s-14-sNN finds the maker's spec sNN.json")
    bad += not ok
    ok = kit_bytes('<style data-oa-chart-kit>abc</style><script data-oa-chart-kit>de</script>') == len('<style data-oa-chart-kit>abc</style>') + len('<script data-oa-chart-kit>de</script>')
    print(f"{'pass' if ok else 'FAIL'} the chart kit weighs as its own part")
    bad += not ok
    # board 1's approved specimens are listed, not failed, up to the bytes board 1 measured; a new one over keeps failing
    _, rec, got = run(base, {"s-14-s05": {"tier": "core", "bytes": 30_524}, "s-14-s99": {"tier": "core", "bytes": 30_524}}, 300_000, set())
    ok = "s-14-s05" in rec["far_over_approved"] and not any("s-14-s05" in g for g in got + run.noted) and any("s-14-s99" in g for g in run.noted)
    print(f"{'pass' if ok else 'FAIL'} S05, approved on board 1, is listed with its bytes; a new specimen as heavy is reported (DR-271)")
    bad += not ok
    _, rec, got = run(base, {"s-14-s13": {"tier": "core", "bytes": 47_213}}, 300_000, set())
    ok = any("s-14-s13" in g for g in run.noted) and not rec["far_over_approved"]
    print(f"{'pass' if ok else 'FAIL'} S13 one byte over its board 1 weight is reported again (DR-271)")
    bad += not ok
    # a chapter still being built counts at its allocation in the projection, and at its bytes once past it
    w = json.loads(json.dumps(base)); w["chapters"]["15"] = {"bytes": 200_000}
    _, rec, _ = run(w, {}, 300_000, {"15"})
    ok = rec["held_to_allocation"].get("15") == 400_000 and rec["projected_bytes"] == round(w["bytes"] + sum(a for n, a in ALLOCATION.items() if n != "15") - 100_000 + 400_000)
    print(f"{'pass' if ok else 'FAIL'} chapter 15 built in part (0.20 MB) still projects at its 0.60 MB allocation")
    bad += not ok
    w = json.loads(json.dumps(base)); w["chapters"]["15"] = {"bytes": 590_000}; w["chapters"]["14"] = {"bytes": 1_000_000}
    _, rec, _ = run(w, {}, 300_000, {"14", "15"})
    ok = rec["held_to_allocation"] == {"14": round(CHAPTER_14_STOP - 1_100_000), "15": 10_000}
    print(f"{'pass' if ok else 'FAIL'} chapter 14 in part counts with its kit against its allocation")
    bad += not ok
    # the stop's figure, its allocation in the projection, and the per-plate share's arithmetic
    ok = CEILING[HARD_STOP] == 2_803_941 and ALLOCATION["14"] == 2_803_941 and HARD_STOP == "14"
    print(f"{'pass' if ok else 'FAIL'} chapter 14's stop and allocation are 2,803,941 bytes (DR-238)")
    bad += not ok
    sz = {"registered": 10, "geo": 5_000, "forms": {"a.js": 30_000, "b.js": 10_000}}
    sh = per_plate(0, 105_000, {"s-14-s01": {"tier": "core"}, "s-14-s02": {"tier": "reference"}, "s-13-1-correct": {"tier": "core"},
                                "s-14-3-correct": {"tier": "core"}, "s-14-1-line": {"tier": "core"}}, sz)
    want = (2_803_941 - (100_000 + 87 * 4_000) - sum(NOT_PLATES.values())) / 96
    ok = sh is not None and sh["plates_to_come"] == 96 and sh["renderer_grown"] == 448_000 and abs(sh["per_plate"] - want) < 1
    print(f"{'pass' if ok else 'FAIL'} the per-plate share: the stop less the grown renderer and the parts that are not plates, over the core and extended plates to come")
    bad += not ok
    ok = per_plate(0, 0, {}, {}) is None
    print(f"{'pass' if ok else 'FAIL'} no per-plate share on a page with no chart kit")
    bad += not ok
    # call 4 (round 1 fix pass): the rules' allowance and the sketch entries counted whole, from the page's measure
    p14 = {"rules_1_to_14": 190_000, "opener": 4_000, "rules_and_opener": 194_000, "allowance": RULES_ALLOWANCE,
           "sketch_entries": [{"rule": "14.24", "kind": "avoid", "bytes": 6_000, "sketch_bytes": 2_000}, {"rule": "14.43", "kind": "sketch", "bytes": 7_000, "sketch_bytes": 3_000}]}
    rs = not_plates(p14)
    want = 28 * (4096 + 4_000) + (RULES_ALLOWANCE - 194_000) + 100_000 + 90_000 + 250_000
    ok = abs(sum(rs.values()) - want) <= 1
    print(f"{'pass' if ok else 'FAIL'} call 4: 28 sketch entries to come whole at the built ones' words, and the rules' unspent 18,288 bytes, reserved")
    bad += not ok
    w = json.loads(json.dumps(base)); w["chapter_14_parts"] = dict(p14, rules_and_opener=RULES_ALLOWANCE + 1)
    _, rec, got = run(w, {}, 300_000, set())
    ok = any("over their 212,288" in g for g in run.noted) and not any("212,288" in g for g in got)
    print(f"{'pass' if ok else 'FAIL'} rules 14.1 to 14.14 with the opener one byte over 212,288 are reported (DR-271)")
    bad += not ok
    pg = ('<section class="chapter" id="data-visualization"><figure class="plate plate--opener" id="fig-s-14-opener"><p>Op</p></figure>'
          '<div class="rule" id="rule-14-1" data-rule="14.1"><p>One</p></div><div class="rule" id="rule-14-24" data-rule="14.24"><p>W</p></div>'
          '<figure class="plate plate--avoid" id="fig-s-14-24-sketch"><div class="plate-scroll"><div class="plate-stage" data-specimen="s-14-24-sketch">'
          '<svg class="oac-svg oac-sketch">x</svg></div></div><figcaption>c</figcaption></figure><div class="closer" id="x"></div></section>')
    m = chapter14_parts(pg)
    ok = m is not None and m["rules_1_to_14"] == len('<div class="rule" id="rule-14-1" data-rule="14.1"><p>One</p></div>') and m["opener"] > 0 \
        and len(m["sketch_entries"]) == 1 and m["sketch_entries"][0]["sketch_bytes"] == len('<svg class="oac-svg oac-sketch">x</svg>')
    print(f"{'pass' if ok else 'FAIL'} the page's measure finds rules 14.1 to 14.14, the opener and each sketch entry whole")
    bad += not ok
    css = '<style data-plate-css>@scope (#data-visualization [data-specimen]) {\n.a { color: var(--x) }\n}</style>'
    m2 = chapter14_parts(pg.replace('<figure class="plate plate--opener"', css + '<figure class="plate plate--opener"', 1))
    ok = m2 is not None and m2["plate_css"] == len(css) and m2["rules_and_opener"] == m["rules_and_opener"] + len(css)
    print(f"{'pass' if ok else 'FAIL'} ED-E13: the chapter's shared plate style counts with rules 14.1 to 14.14 and the opener")
    bad += not ok
    # R3-2: the map geometry is weighed apart, against its 250,000 bytes
    KIT_SIZES.clear(); KIT_SIZES.update({"geo": GEOMETRY_ALLOWANCE + 1, "registered": 1, "forms": {"a.js": 1}})
    _, rec, got = run(base, {}, 300_000, set())
    over = any("shared map geometry" in g for g in run.noted) and rec["map_geometry"]["room"] == -1
    KIT_SIZES.update({"geo": GEOMETRY_ALLOWANCE})
    _, rec, got = run(base, {}, 300_000, set())
    ok = over and not any("shared map geometry" in g for g in got + run.noted) and rec["map_geometry"]["bytes"] == 250_000
    KIT_SIZES.clear()
    print(f"{'pass' if ok else 'FAIL'} R3-2: map geometry one byte over its 250,000 bytes is reported (DR-271), and at them nothing")
    bad += not ok
    print("guide_charts self-test: " + ("every planted fault caught" if not bad else f"{bad} failed"))
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(__doc__)
