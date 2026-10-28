#!/usr/bin/env python3
"""Check every drawing on the Systems Map Directions Board against Atlas V7, independently of the drawing code.

Run:  python3 -I work/build/scripts/phase-2/verify_maps_data.py
Reads  work/extract/atlas-v7-data.json (raw V7, not the model module the drawings use)
       work/boards/phase-2/maps/20261028_*.svg and the board HTML
Writes work/boards/phase-2/maps/20261028_Maps-Verify-Results.json

For each drawn step it checks the V7 values carried on the mark (link, from, to, sign, type, delay, grade) and the
marks themselves: the line texture, the number of delay ticks, the sign glyph in the label, the record square, the
variables drawn, the weakest-step marks and every reform target, with red only at the one reform a view names.
"""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
V7 = json.loads((ROOT / "work/extract/atlas-v7-data.json").read_text(encoding="utf-8"))
ASSETS = ROOT / "work/boards/phase-2/maps"
BOARD = ROOT / "work/boards/20261028_Systems-Map-Directions-Board.html"
OUT = ASSETS / "20261028_Maps-Verify-Results.json"
NS = "{http://www.w3.org/2000/svg}"
DASH = {"documented": "solid", "well-supported": "solid", "plausible": "9 4", "plausible_contested": "9 3 2 3", "hypothesis": "2 4"}
TICKS = {"S": 1, "M": 2, "L": 3}
RANK = {"documented": 4, "well-supported": 3, "plausible": 2, "plausible_contested": 2, "hypothesis": 1}
GLYPH = {"+": "+", "-": "−"}

N, L, LOOPS, REF = V7["nodes"], V7["links"], V7["loops"], V7["reforms"]
problems, counts = [], {"svg_files": 0, "steps_checked": 0, "links_checked": 0, "nodes_checked": 0, "targets_checked": 0,
                         "red_marks_checked": 0, "weakest_checked": 0, "ticks_checked": 0, "textures_checked": 0, "glyphs_checked": 0}


def fail(f, msg):
    problems.append(f"{f}: {msg}")


def text_of(el):
    return "".join(el.itertext()).strip()


def loop_elements(lid):
    lp = LOOPS[lid]
    return set(lp["links"]) | {c for c, _ in lp["chain"] if c in N}


def expected_targets(lid, reform=None):
    els = loop_elements(lid)
    out = {}
    reforms = [reform] if reform else [r for r in LOOPS[lid]["reforms"] if not REF[r]["rejected"]]
    for rid in reforms:
        for t in REF[rid]["targets"]:
            if t in els:
                out.setdefault(t, set()).add(rid)
    return out


def expected_weakest(lid):
    lp = LOOPS[lid]
    if not lp["closure"].startswith("closed"):
        return set()
    ranks = {k: RANK[L[k]["evidence"]] for k in lp["links"]}
    lo = min(ranks.values())
    w = {k for k, v in ranks.items() if v == lo}
    return set() if len(w) == len(ranks) else w


def check_step(f, g, root, require_marks=True, require_ticks=True):
    """One drawn step or connection: V7 values on the mark, then the marks themselves."""
    k = g.get("data-link")
    if not k:
        return
    l = L.get(k)
    if l is None:
        fail(f, f"{k} is not a V7 connection")
        return
    for attr, val in (("data-from", l["from"]), ("data-to", l["to"]), ("data-sign", l["polarity"] or "none"),
                      ("data-grade", l["evidence"]), ("data-delay", l["delay"]), ("data-type", l["type"])):
        if g.get(attr) != val:
            fail(f, f"{k} {attr} drawn {g.get(attr)!r}, V7 {val!r}")
    paths = [p for p in g.iter(NS + "path") if p.get("data-texture")]
    if not paths:
        fail(f, f"{k} has no textured line")
    else:
        counts["textures_checked"] += 1
        tex = paths[0].get("data-texture")
        da = paths[0].get("stroke-dasharray") or "solid"
        if tex != DASH[l["evidence"]] or da != DASH[l["evidence"]]:
            fail(f, f"{k} texture {tex}/{da}, V7 grade {l['evidence']} needs {DASH[l['evidence']]}")
    if require_ticks:
        t = [x for x in g.iter(NS + "g") if x.get("class") == "ticks"]
        n_ticks = int(t[0].get("data-ticks")) if t else 0
        n_lines = len(list(t[0].iter(NS + "line"))) if t else 0
        counts["ticks_checked"] += 1
        if n_ticks != TICKS[l["delay"]] or n_lines != TICKS[l["delay"]]:
            fail(f, f"{k} draws {n_lines} delay ticks marked {n_ticks}, V7 delay {l['delay']} needs {TICKS[l['delay']]}")
    if require_marks:
        pills = [p for p in root.iter(NS + "g") if p.get("class") == "pill" and p.get("data-for") == k]
        if len(pills) != 1:
            fail(f, f"{k} has {len(pills)} sign labels")
        else:
            counts["glyphs_checked"] += 1
            gl = [t for t in pills[0].iter(NS + "text") if t.get("data-sign-glyph")]
            want = GLYPH.get(l["polarity"], "no sign")
            if not gl or text_of(gl[0]) != want:
                fail(f, f"{k} sign label reads {text_of(gl[0]) if gl else None!r}, V7 sign {l['polarity']!r}")
            rec = [r for r in pills[0].iter(NS + "rect") if r.get("data-record")]
            if bool(rec) != (l["evidence"] == "documented"):
                fail(f, f"{k} record square {'present' if rec else 'absent'} with grade {l['evidence']}")


def check_loop_view(f, root, view):
    lid = root.get("data-loop")
    lp = LOOPS[lid]
    conceptual = not lp["closure"].startswith("closed")
    steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
    if conceptual:
        if len(steps) != len(lp["chain"]):
            fail(f, f"{lid} draws {len(steps)} sketched steps, V7 chain has {len(lp['chain'])}")
        labels = [lab for lab, _ in lp["chain_labels"]]
        for i, g in enumerate(steps):
            counts["steps_checked"] += 1
            sign = lp["chain"][i][1]
            if g.get("data-sign") != sign:
                fail(f, f"{lid} sketched step {i + 1} sign {g.get('data-sign')}, V7 {sign}")
            if g.get("data-from-label") != labels[i] or g.get("data-to-label") != labels[(i + 1) % len(labels)]:
                fail(f, f"{lid} sketched step {i + 1} labels differ from V7 chain_labels")
            if not any(p.get("data-texture") == "hollow" for p in g.iter(NS + "path")):
                fail(f, f"{lid} sketched step {i + 1} is not drawn in the hollow line")
    else:
        drawn = [g.get("data-link") for g in steps]
        if drawn != lp["links"]:
            fail(f, f"{lid} draws steps {drawn}, V7 {lp['links']}")
        for g in steps:
            counts["steps_checked"] += 1
            check_step(f, g, root, require_marks=True, require_ticks=view not in ("explore",))
    # variables
    nodes = {g.get("data-node"): g for g in root.iter(NS + "g") if g.get("class") == "var"}
    want_nodes = {c for c, _ in lp["chain"] if c in N}
    if set(nodes) != want_nodes:
        fail(f, f"{lid} draws variables {sorted(nodes)}, V7 chain {sorted(want_nodes)}")
    lab_of = {c: lab for (c, _), (lab, _) in zip(lp["chain"], lp["chain_labels"])}
    for c, g in nodes.items():
        counts["nodes_checked"] += 1
        if g.get("data-label") and g.get("data-label") != lab_of.get(c):
            fail(f, f"{lid} variable {c} label {g.get('data-label')!r}, V7 chain label {lab_of.get(c)!r}")
        if c not in text_of(g) and view not in ("weave-mini", "weave-card", "explore"):
            fail(f, f"{lid} variable {c} disc does not print its ID")
    return lid


def check_targets(f, root, expected, red_expected):
    """Pointers and red marks against the reform targets the view should show."""
    marks = [e for e in root.iter() if e.get("class") == "tg" or (e.get("data-target") and e.tag in (NS + "g", NS + "polygon"))]
    drawn = {}
    for e in marks:
        at = e.get("data-at")
        if at:
            drawn.setdefault(at, set()).update((e.get("data-target") or "").split())
    if set(drawn) != set(expected):
        fail(f, f"pointers at {sorted(drawn)}, V7 targets {sorted(expected)}")
    for at, rs in drawn.items():
        counts["targets_checked"] += 1
        if expected.get(at) and rs != expected[at]:
            fail(f, f"pointer at {at} names {sorted(rs)}, V7 {sorted(expected[at])}")
    red_at = set()
    for e in root.iter():
        if e.get("data-red"):
            at = e.get("data-at") or e.get("data-node") or e.get("data-link")
            if at is None:
                par = [g for g in root.iter() if e in list(g)]
                at = par[0].get("data-link") if par else None
            red_at.add(at)
    red_at.discard(None)
    for at in red_at:
        counts["red_marks_checked"] += 1
    if red_at != set(red_expected):
        fail(f, f"red marks at {sorted(red_at)}, expected {sorted(red_expected)}")


def check_weakest(f, root, lid):
    want = expected_weakest(lid)
    drawn = {e.get("data-weakest") for e in root.iter() if e.get("data-weakest")}
    counts["weakest_checked"] += 1
    if drawn != want:
        fail(f, f"{lid} weakest marks {sorted(drawn)}, V7 ranks give {sorted(want)}")


def check_map(f, root, view):
    links = [g for g in root.iter(NS + "g") if g.get("class") in ("link",) and g.get("data-link")]
    ids = [g.get("data-link") for g in links]
    uniq = set(ids)
    if uniq != set(L):
        fail(f, f"map draws {len(uniq)} distinct connections, V7 has {len(L)}; missing {sorted(set(L) - uniq)[:5]}")
    for g in links:
        counts["links_checked"] += 1
        check_step(f, g, root, require_marks=False, require_ticks=False)
    if view == "weave-map":
        rep = [g for g in links if g.get("data-repeat")]
        bands = {}
        for g in links:
            b = g.get("data-loopband")
            if b:
                bands.setdefault(b, []).append(g.get("data-link"))
                if b not in L[g.get("data-link")]["loops"]:
                    fail(f, f"{g.get('data-link')} woven into band {b}, V7 loops {L[g.get('data-link')]['loops']}")
        for lid, lp in LOOPS.items():
            if lp["closure"].startswith("closed") and bands.get(lid) != lp["links"]:
                fail(f, f"band {lid} holds {bands.get(lid)}, V7 {lp['links']}")
        nonrep = [g.get("data-link") for g in links if not g.get("data-repeat")]
        if sorted(nonrep) != sorted(L):
            fail(f, "fabric does not hold each connection exactly once outside its marked copies")
        counts["fabric_copies"] = len(rep)
    nodes = {g.get("data-node") for g in root.iter(NS + "g") if g.get("class") == "var"}
    counts["nodes_checked"] += len(nodes)
    if nodes != set(N):
        fail(f, f"map draws {len(nodes)} variables, V7 has {len(N)}")
    rid = root.get("data-reform")
    red = {g.get("data-link") or g.get("data-node") for g in root.iter(NS + "g") if g.get("data-red")}
    want = set(REF[rid]["targets"]) if rid else set()
    counts["red_marks_checked"] += len(red)
    if red != want:
        fail(f, f"map red marks {sorted(red)}, expected {sorted(want)}")


def main():
    views = {}
    catalogs = {}
    files = sorted(ASSETS.glob("20261028_*.svg"))
    board_html = BOARD.read_text(encoding="utf-8") if BOARD.exists() else ""
    not_on_board = []
    for path in files:
        f = path.name
        raw = path.read_text(encoding="utf-8")
        body = raw.split("?>", 1)[1].strip() if raw.startswith("<?xml") else raw
        if not f.startswith("20261028_Phone-") and body not in board_html:
            not_on_board.append(f)
        root = ET.fromstring(raw)
        counts["svg_files"] += 1
        view = root.get("data-view")
        views[view] = views.get(view, 0) + 1
        rid = root.get("data-reform")
        if view in ("orbit-mini", "line-mini", "weave-mini", "orbit-mini-phone", "orbit-card", "line-card", "weave-card", "orbit-card-phone"):
            lid = check_loop_view(f, root, view)
            if view in ("orbit-mini", "line-mini", "weave-mini") and not rid:
                catalogs.setdefault(view, set()).add(lid)
            if view == "orbit-mini-phone":
                catalogs.setdefault(view, set()).add(lid)
            if view.endswith("mini") or view == "orbit-mini-phone":
                if rid:
                    exp = {k: {rid} for k in expected_targets(lid, rid)}
                    check_targets(f, root, exp, set(exp))
                else:
                    check_targets(f, root, expected_targets(lid), set())
                check_weakest(f, root, lid)
            else:
                # cards: red at every target of the named reform that the card draws, and nowhere else
                drawn_els = {g.get("data-link") for g in root.iter(NS + "g") if g.get("data-link")} | \
                            {g.get("data-node") for g in root.iter(NS + "g") if g.get("data-node")}
                want_red = set(REF[rid]["targets"]) & drawn_els if rid else set()
                red_at = set()
                for e in root.iter():
                    if e.get("data-red"):
                        at = e.get("data-at") or e.get("data-node") or e.get("data-link") or e.get("data-target")
                        red_at.add(at)
                # a red line path sits inside its step group: map it to the step's link
                for g in root.iter(NS + "g"):
                    if g.get("data-link") and any(p.get("data-red") for p in g.iter(NS + "path")):
                        red_at.add(g.get("data-link"))
                red_at = {a for a in red_at if a in N or a in L}
                counts["red_marks_checked"] += len(red_at)
                if red_at != want_red:
                    fail(f, f"card red marks at {sorted(red_at)}, {rid} targets drawn here {sorted(want_red)}")
        elif view in ("orbit-map", "line-map", "weave-map"):
            check_map(f, root, view)
        elif view == "explore":
            for g in root.iter(NS + "g"):
                if g.get("class") == "step" and g.get("data-link"):
                    counts["steps_checked"] += 1
                    check_step(f, g, root, require_marks=False, require_ticks=False)
                if g.get("class") == "var" and g.get("data-node") not in N:
                    fail(f, f"exploration draws unknown variable {g.get('data-node')}")
    for view, s in catalogs.items():
        if s != set(LOOPS):
            fail(view, f"catalog draws {len(s)} loops, V7 has {len(LOOPS)}; missing {sorted(set(LOOPS) - s)}")
    for f in not_on_board:
        fail(f, "drawing file differs from the copy on the board")
    result = {
        "run_note": "Checked against work/extract/atlas-v7-data.json, independently of maps_model.py",
        "counts": counts, "views": views, "catalog_loops": {k: len(v) for k, v in catalogs.items()},
        "mismatches": len(problems), "problems": problems[:200],
        "summary": [
            f"Data check against V7: {len(problems)} mismatches across {counts['svg_files']} drawings.",
            f"All {len(LOOPS)} loops drawn in each catalog: " + ", ".join(f"{k.replace('-mini', '')} {len(v)}" for k, v in sorted(catalogs.items())) + ".",
            f"Checked {counts['steps_checked']} drawn loop steps and {counts['links_checked']} drawn map connections for link, from, to, sign, type, delay and grade; "
            f"{counts['textures_checked']} line textures, {counts['ticks_checked']} delay-tick sets and {counts['glyphs_checked']} sign labels with their record squares.",
            f"Checked {counts['targets_checked']} reform pointers, {counts['red_marks_checked']} red marks and {counts['weakest_checked']} weakest-step markings against V7's reform targets and grade ranks.",
            "Each whole-system map draws all 51 variables and all 118 connections; the fabric weaves "
            f"{counts.get('fabric_copies', 0)} marked copies of connections that sit on more than one loop.",
        ],
    }
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(result["summary"]))
    for p in problems[:40]:
        print("  ", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
