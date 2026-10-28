#!/usr/bin/env python3
"""Check every Direction A (Field Guide) drawing against Atlas V7, independently of the drawing code.

Run:  python3 -I work/build/scripts/phase-2/maps_r2_a_verify.py
Reads  work/extract/atlas-v7-data.json (raw V7, through the shared verifier's loader, not maps_model.py)
       work/boards/phase-2/maps-r2/a/20261028_A-*.svg, the catalog page and the Direction A board
Writes work/boards/phase-2/maps-r2/a/20261028_A-Verify-Results.json

It imports verify_maps_data.py for V7, its constants and its per-step check, and leaves that file unchanged, so
Directions B and C keep the same interface. The rules here follow the round-two notation budget:
  miniatures and leads   texture, hollow line, sign glyph; no record square, no ticks, no red
  cards and the head     every mark: texture, ticks, sign glyph, record square on documented steps, weakest step
  circuit map            46 loop wires with V7 values and one sign glyph each, 72 connections counted in bundles
                         whose areas match V7, 51 variables, red only at the named reform's targets
Red anywhere else in a drawing, by color, is a mismatch. A mutation test breaks one copy of each kind of
drawing in memory and confirms the checks catch it.
"""
import copy
import csv
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_maps_data as VM  # noqa: E402  (shared verifier: V7 loading, constants, check_step)

ROOT = VM.ROOT
ASSETS = ROOT / "work/boards/phase-2/maps-r2/a"
BOARD = ROOT / "work/boards/20261028_Map-Direction-A-Field-Guide.html"
CATALOG = ASSETS / "20261028_A-Loop-Catalog.html"
CIRCUIT_PAGE = ASSETS / "20261028_A-Circuit-Page.html"      # retired in round two; kept for the appendix
REFORM_PAGE = ASSETS / "20261028_A-R-01-Reform-View.html"
C_DIR = ROOT / "work/boards/phase-2/maps-r2/c"
C_NETWORK = C_DIR / "20261028_Loop-Lines-Network-Data.json"
C_TABLE = C_DIR / "20261028_Loop-Lines-Station-Table.csv"
C_REFORM = C_DIR / "20261028_Loop-Lines-Reform-View-R-01.svg"
CHARCOAL, STONE = "#121212", "#5D636D"
OUT = ASSETS / "20261028_A-Verify-Results.json"
NS = VM.NS
N, L, LOOPS, REF = VM.N, VM.L, VM.LOOPS, VM.REF
RED = "#E63946"
GRADE_WORDS = {"documented": "documented", "well-supported": "well supported", "plausible": "plausible",
               "plausible_contested": "contested", "hypothesis": "hypothesis"}
DELAY_WORDS = {"S": "under 2 years", "M": "2 to 10 years", "L": "over 10 years"}

problems = VM.problems          # the shared list, so check_step reports land here
counts = VM.counts
counts.update({"captions_checked": 0, "bundles_checked": 0, "bundled_links": 0, "red_color_elements": 0,
               "record_squares_absent_checked": 0, "ticks_absent_checked": 0, "locators": 0, "locator_tracks": 0,
               "locator_stations": 0, "tag_directions_checked": 0, "arrowheads_checked": 0})


def fail(f, msg):
    problems.append(f"{f}: {msg}")


def area_of(code):
    n = N[code]
    return n["cluster"] if n["layer"] == "core" else {"economy": "EC", "technology": "TC"}[n["layer"]]


def words(el):
    """The text a group prints, one space between its text lines, with typographic apostrophes and no-break
    spaces read back as V7 writes them."""
    t = " ".join((x.text or "").strip() for x in el.iter(NS + "text"))
    return " ".join(t.replace("\u2019", "'").replace("\u00a0", " ").split())


def parents(root):
    return {c: p for p in root.iter() for c in p}


def red_color_ok(f, root, allowed):
    """Every element painted Pillar Red must sit inside a mark for an allowed target."""
    par = parents(root)
    for e in root.iter():
        if RED.lower() not in ((e.get("stroke") or "") + (e.get("fill") or "")).lower():
            continue
        counts["red_color_elements"] += 1
        a, owner = e, None
        while a is not None:
            key = a.get("data-link") or a.get("data-node") or a.get("data-for")
            if a.get("data-red") or (key and key in allowed):
                owner = key or "red"
                if key is None:
                    # a red path inside a step group: take the group's link
                    b = par.get(a)
                    while b is not None and owner == "red":
                        owner = b.get("data-link") or b.get("data-node") or "red"
                        b = par.get(b)
                break
            a = par.get(a)
        if owner is None or owner not in allowed:
            fail(f, f"red paint on a <{e.tag.replace(NS, '')}> outside the named reform's targets (owner {owner})")


def red_marks(root):
    par = parents(root)
    out = set()
    for e in root.iter():
        if not e.get("data-red"):
            continue
        a = e
        while a is not None and not (a.get("data-link") or a.get("data-node")):
            a = par.get(a)
        if a is not None:
            out.add(a.get("data-link") or a.get("data-node"))
    return out


def check_loop(f, root, view):
    """One loop drawing, at any scale. Returns the loop ID."""
    lid = root.get("data-loop")
    if lid not in LOOPS:
        fail(f, f"unknown loop {lid}")
        return None
    lp = LOOPS[lid]
    full = view in ("fg-card", "fg-card-phone", "fg-head", "fg-head-phone")
    conceptual = not lp["closure"].startswith("closed")
    steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
    if conceptual:
        if len(steps) != len(lp["chain"]):
            fail(f, f"{lid} draws {len(steps)} sketched steps, V7 chain has {len(lp['chain'])}")
        labels = [lab for lab, _ in lp["chain_labels"]]
        for i, g in enumerate(steps):
            counts["steps_checked"] += 1
            if g.get("data-sign") != lp["chain"][i][1]:
                fail(f, f"{lid} sketched step {i + 1} sign {g.get('data-sign')}, V7 {lp['chain'][i][1]}")
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
            # the shared check covers link, from, to, sign, grade, delay, type, texture; on full views also the
            # ticks, the sign glyph and the record square
            VM.check_step(f, g, root, require_marks=full, require_ticks=full)
            if not full:
                k = g.get("data-link")
                pills = [p for p in root.iter(NS + "g") if p.get("class") == "pill" and p.get("data-for") == k]
                if len(pills) != 1:
                    fail(f, f"{k} has {len(pills)} sign discs")
                else:
                    counts["glyphs_checked"] += 1
                    gl = [t for t in pills[0].iter(NS + "text") if t.get("data-sign-glyph")]
                    want = VM.GLYPH.get(L[k]["polarity"], "no sign")
                    if not gl or VM.text_of(gl[0]) != want:
                        fail(f, f"{k} sign disc reads {VM.text_of(gl[0]) if gl else None!r}, V7 sign {L[k]['polarity']!r}")
                    counts["record_squares_absent_checked"] += 1
                    if any(r.get("data-record") for r in pills[0].iter(NS + "rect")):
                        fail(f, f"{k} miniature carries a record square; the budget leaves it to the card")
                counts["ticks_absent_checked"] += 1
                if any(t.get("class") == "ticks" for t in g.iter(NS + "g")):
                    fail(f, f"{k} miniature carries delay ticks; the budget leaves them to the card")
    nodes = {g.get("data-node"): g for g in root.iter(NS + "g") if g.get("class") == "var"}
    want_nodes = {c for c, _ in lp["chain"] if c in N}
    if set(nodes) != want_nodes:
        fail(f, f"{lid} draws variables {sorted(nodes)}, V7 chain {sorted(want_nodes)}")
    lab_of = {c: lab for (c, _), (lab, _) in zip(lp["chain"], lp["chain_labels"])}
    for c, g in nodes.items():
        counts["nodes_checked"] += 1
        if g.get("data-label") != lab_of.get(c):
            fail(f, f"{lid} variable {c} label {g.get('data-label')!r}, V7 chain label {lab_of.get(c)!r}")
        shown = words(g)
        if " ".join(lab_of.get(c, "").split()) not in " ".join(shown.split()):
            fail(f, f"{lid} variable {c} does not print its V7 label")
        if view in ("fg-card", "fg-card-phone", "fg-head", "fg-head-phone", "fg-lead") and c not in shown:
            fail(f, f"{lid} variable {c} does not print its ID")
    # sign style: the circled sign keeps an arrowhead on every step; C's pointing tag replaces it and must point
    # the way the step runs
    if full and not conceptual:
        tags = {p.get("data-for"): p for p in root.iter(NS + "g") if p.get("class") == "pill" and p.get("data-sign-style") == "tag"}
        for g in steps:
            k = g.get("data-link")
            heads = [x for x in g.iter(NS + "polygon")]
            counts["arrowheads_checked"] += 1
            if tags and heads:
                fail(f, f"{k} carries an arrowhead beside a pointing tag")
            if not tags and len(heads) != 1:
                fail(f, f"{k} has {len(heads)} arrowheads with the circled sign")
            if tags:
                t = tags.get(k)
                if t is None:
                    fail(f, f"{k} has no pointing tag")
                    continue
                counts["tag_directions_checked"] += 1
                want = travel_dir(g, tag_center(t))
                got = tuple(float(v) for v in (t.get("data-dir") or "0 0").split())
                if want is None or (round(want[0]), round(want[1])) != (round(got[0]), round(got[1])):
                    fail(f, f"{k} tag points {got}, its line runs {want}")
                tip = tag_tip(t)
                c = tag_center(t)
                if tip is None or (tip[0] - c[0]) * got[0] + (tip[1] - c[1]) * got[1] <= 0:
                    fail(f, f"{k} tag's point is not on its leading side")
    # weakest step: cards and the head mark it; miniatures leave it to the caption
    if full:
        counts["weakest_checked"] += 1
        drawn = {e.get("data-weakest") for e in root.iter() if e.get("data-weakest")}
        want = VM.expected_weakest(lid)
        if drawn != want:
            fail(f, f"{lid} weakest marks {sorted(drawn)}, V7 ranks give {sorted(want)}")
    # red: only the named reform's targets that this drawing draws
    rid = root.get("data-reform")
    drawn_els = set(lp["links"]) | want_nodes
    allowed = (set(REF[rid]["targets"]) & drawn_els) if rid else set()
    got = red_marks(root)
    counts["red_marks_checked"] += len(got)
    if got != allowed:
        fail(f, f"red marks at {sorted(got)}, {'reform ' + rid + ' targets drawn here ' if rid else 'expected none '}{sorted(allowed)}")
    red_color_ok(f, root, allowed)
    if rid:
        tg = {e.get("data-node") or e.get("data-link") for e in root.iter() if e.get("data-target") == rid}
        if not tg <= allowed:
            fail(f, f"data-target marks {sorted(tg - allowed)} are not {rid} targets")
    return lid


def path_points(d):
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", d or "")]
    return list(zip(nums[0::2], nums[1::2])) if not re.search(r"[AaCcQq]", d or "") else None


def tag_poly(t):
    poly = t.find(NS + "polygon")
    if poly is None:
        return None
    return [tuple(float(v) for v in xy.split(",")) for xy in poly.get("points").split()]


def tag_center(t):
    pts = tag_poly(t)
    if not pts:
        return (0.0, 0.0)
    body = [pts[0], pts[1], pts[3], pts[4]]
    return (sum(x for x, _ in body) / 4, sum(y for _, y in body) / 4)


def tag_tip(t):
    pts = tag_poly(t)
    return pts[2] if pts and len(pts) == 5 else None


def travel_dir(g, c):
    """Direction of the step's line at the point nearest c, in drawing order (from the source box to the target)."""
    best, out = None, None
    for p in g.iter(NS + "path"):
        pts = path_points(p.get("d"))
        if not pts:
            continue
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 1e-6:
                continue
            t = max(0.0, min(1.0, ((c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])) / L ** 2))
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            dd = math.hypot(q[0] - c[0], q[1] - c[1])
            if best is None or dd < best:
                best, out = dd, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    return out


def check_locator(f, root):
    """C's working map as drawn on A's pages: every numbered loop's tracks with V7's values, stations at C's grid
    cells, the lit loops in Charcoal at the stated weight and every other line in Stone, and no red."""
    counts["locators"] += 1
    net = json.loads(C_NETWORK.read_text(encoding="utf-8"))
    table = {}
    with open(C_TABLE, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            table[r["id"]] = (int(r["col"]), int(r["row"]))
    if root.get("data-source") != C_NETWORK.name:
        fail(f, f"locator names source {root.get('data-source')!r}")
    cell, ox, oy = float(root.get("data-cell")), float(root.get("data-ox")), float(root.get("data-oy"))
    pitch = float(root.get("data-pitch"))
    lit = (root.get("data-lit") or "").split()
    w_lit, w_other = float(root.get("data-lit-width")), float(root.get("data-other-width"))
    numbered = [lid for lid, lp in LOOPS.items() if lp["closure"].startswith("closed")]
    for lid in lit:
        if lid not in numbered:
            fail(f, f"locator lights {lid}, which has no numbered chain")
    want = {(lid, k) for lid in numbered for k in LOOPS[lid]["links"]}
    drawn = {}
    pos = {k: (ox + c * cell, oy + r * cell) for k, (c, r) in table.items()}
    for g in root.iter(NS + "g"):
        if g.get("class") != "step":
            continue
        key = (g.get("data-loop"), g.get("data-link"))
        if key in drawn:
            fail(f, f"track {key} drawn twice")
        drawn[key] = g
        counts["locator_tracks"] += 1
        k = key[1]
        if k not in L:
            fail(f, f"track {key} is not a V7 connection")
            continue
        l = L[k]
        for attr, val in (("data-from", l["from"]), ("data-to", l["to"]), ("data-sign", l["polarity"] or "none"),
                          ("data-grade", l["evidence"]), ("data-delay", l["delay"]), ("data-type", l["type"])):
            if g.get(attr) != val:
                fail(f, f"{k} on {key[0]} {attr} drawn {g.get(attr)!r}, V7 {val!r}")
        path = g.find(NS + "path")
        tex = VM.DASH[l["evidence"]]
        if path.get("data-texture") != tex:
            fail(f, f"{k} on {key[0]} texture {path.get('data-texture')}, V7 grade needs {tex}")
        da = path.get("stroke-dasharray")
        if tex == "solid":
            if da:
                fail(f, f"{k} on {key[0]} is dashed, V7 grade is solid")
        else:
            a = [float(x) for x in (da or "").split()]
            b = [float(x) for x in tex.split()]
            if len(a) != len(b) or not a or len({round(x / y, 3) for x, y in zip(a, b)}) != 1:
                fail(f, f"{k} on {key[0]} dashes {da!r} are not V7's {tex!r} pattern")
        on = key[0] in lit
        if bool(g.get("data-lit")) != on:
            fail(f, f"{k} on {key[0]} lit flag {g.get('data-lit')!r}, lit loops {lit}")
        col, w = path.get("stroke"), float(path.get("stroke-width"))
        if on and (col != CHARCOAL or abs(w - w_lit) > 1e-6):
            fail(f, f"{k} on lit {key[0]} drawn {col} at {w} px, needs Charcoal at {w_lit}")
        if not on and (col != STONE or abs(w - w_other) > 1e-6):
            fail(f, f"{k} on {key[0]} drawn {col} at {w} px, needs Stone at {w_other}")
        # the track runs between its two stations, offset by at most one and a half pitches
        nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", path.get("d"))]
        ends = [(nums[0], nums[1]), (nums[-2], nums[-1])]
        a, b = pos.get(l["from"]), pos.get(l["to"])
        if a is None or b is None:
            fail(f, f"{k} joins a station missing from C's table")
            continue
        tol = 1.5 * pitch + 0.6
        ok = (math.dist(ends[0], a) <= tol and math.dist(ends[1], b) <= tol) or (math.dist(ends[0], b) <= tol and math.dist(ends[1], a) <= tol)
        if not ok:
            fail(f, f"{k} on {key[0]} ends at {ends}, its stations sit at {a} and {b}")
    if set(drawn) != want:
        fail(f, f"locator draws {len(drawn)} tracks, V7's numbered loops ride {len(want)}; missing {sorted(want - set(drawn))[:4]}, extra {sorted(set(drawn) - want)[:4]}")
    # tracks follow C's corridors exactly
    c_tracks = {(t["loop"], t["link"]) for co in net["corridors"] for t in co["tracks"]}
    if c_tracks != want:
        fail(f, f"C's network data holds {len(c_tracks)} tracks, V7 gives {len(want)}")
    lit_st = {c for lid in lit for c, _ in LOOPS[lid]["chain"] if c in N}
    seen = set()
    for g in root.iter(NS + "g"):
        if g.get("class") != "var":
            continue
        k = g.get("data-node")
        seen.add(k)
        counts["locator_stations"] += 1
        if k not in table:
            fail(f, f"station {k} is not in C's table")
            continue
        x, y = pos[k]
        if abs(float(g.get("data-cx")) - x) > 0.01 or abs(float(g.get("data-cy")) - y) > 0.01:
            fail(f, f"station {k} at {g.get('data-cx')}, {g.get('data-cy')}; C's cell gives {x:.2f}, {y:.2f}")
        shape = next(iter([e for e in g if e.tag in (NS + "circle", NS + "rect")]), None)
        if shape is None:
            fail(f, f"station {k} has no shape")
            continue
        if shape.tag == NS + "circle":
            sx, sy = float(shape.get("cx")), float(shape.get("cy"))
        else:
            sx = float(shape.get("x")) + float(shape.get("width")) / 2
            sy = float(shape.get("y")) + float(shape.get("height")) / 2
        if abs(sx - x) > 0.05 or abs(sy - y) > 0.05:
            fail(f, f"station {k} drawn at {sx:.2f}, {sy:.2f}, not at its cell")
        on = k in lit_st
        if bool(g.get("data-lit")) != on:
            fail(f, f"station {k} lit flag {g.get('data-lit')!r}, lit loops {lit}")
        if on and shape.get("fill") != CHARCOAL:
            fail(f, f"lit station {k} filled {shape.get('fill')}, needs Charcoal")
        if on and root.get("data-size") in ("rail", "phone"):
            t = g.find(NS + "text")
            if t is None or (t.text or "").strip() != k or float(t.get("font-size")) < 13:
                fail(f, f"lit station {k} does not print its ID at 13 px or more")
    want_st = {c for lid in numbered for c, _ in LOOPS[lid]["chain"] if c in N}
    if seen != want_st or set(table) != want_st:
        fail(f, f"locator draws {len(seen)} stations, C's table holds {len(table)}, V7's numbered loops have {len(want_st)}")
    if red_marks(root):
        fail(f, "locator carries red marks")
    red_color_ok(f, root, set())
    return lit


def check_circuit(f, root):
    rid = root.get("data-reform")
    loop_links = {k for k, l in L.items() if l["loops"]}
    wires = [g for g in root.iter(NS + "g") if g.get("class") == "link" and g.get("data-link")]
    ids = [g.get("data-link") for g in wires]
    if len(ids) != len(set(ids)):
        fail(f, "a loop connection is drawn as more than one wire")
    if set(ids) != loop_links:
        fail(f, f"draws {len(set(ids))} wires, V7 has {len(loop_links)} loop connections; "
                f"missing {sorted(loop_links - set(ids))[:5]}, extra {sorted(set(ids) - loop_links)[:5]}")
    for g in wires:
        counts["links_checked"] += 1
        VM.check_step(f, g, root, require_marks=False, require_ticks=False)
        gl = [t for t in g.iter(NS + "text") if t.get("data-sign-glyph")]
        counts["glyphs_checked"] += 1
        want = VM.GLYPH.get(L[g.get("data-link")]["polarity"], "no sign")
        if len(gl) != 1 or VM.text_of(gl[0]) != want:
            fail(f, f"{g.get('data-link')} wire carries {len(gl)} sign glyphs {[VM.text_of(t) for t in gl]}, V7 sign {want!r}")
    bundled = []
    for b in root.iter(NS + "g"):
        if b.get("class") != "bundle":
            continue
        counts["bundles_checked"] += 1
        ks = (b.get("data-links") or "").split()
        if str(len(ks)) != b.get("data-count"):
            fail(f, f"bundle {b.get('data-from-area')} to {b.get('data-to-area')} lists {len(ks)} links, data-count {b.get('data-count')}")
        printed = words(b)
        m = re.match(r"(\d+)", printed)
        if printed and ((m and int(m.group(1)) != len(ks)) or (not m and not (printed.startswith("No other") and not ks))):
            fail(f, f"bundle {b.get('data-from-area')} to {b.get('data-to-area')} prints {printed[:30]!r}, lists {len(ks)}")
        for k in ks:
            if k not in L:
                fail(f, f"bundle lists {k}, not a V7 connection")
                continue
            fa, ta = area_of(L[k]["from"]), area_of(L[k]["to"])
            if (fa, ta) != (b.get("data-from-area"), b.get("data-to-area")):
                fail(f, f"{k} runs {fa} to {ta} in V7, bundled as {b.get('data-from-area')} to {b.get('data-to-area')}")
            if L[k]["loops"]:
                fail(f, f"{k} sits on a loop in V7 but is bundled")
        bundled += ks
    counts["bundled_links"] += len(bundled)
    if len(bundled) != len(set(bundled)):
        fail(f, "a connection is counted in more than one bundle")
    if set(bundled) | set(ids) != set(L) or set(bundled) & set(ids):
        fail(f, f"wires plus bundles give {len(set(bundled) | set(ids))} connections, V7 has {len(L)}")
    nodes = {g.get("data-node") for g in root.iter(NS + "g") if g.get("class") == "var"}
    counts["nodes_checked"] += len(nodes)
    if nodes != set(N):
        fail(f, f"draws {len(nodes)} variables, V7 has {len(N)}; missing {sorted(set(N) - nodes)[:5]}")
    want = set(REF[rid]["targets"]) if rid else set()
    got = red_marks(root)
    counts["red_marks_checked"] += len(got)
    if got != want:
        fail(f, f"red marks at {sorted(got)}, expected {sorted(want)}")
    red_color_ok(f, root, want)
    return len(set(ids)), len(bundled)


def check_captions(html):
    """The miniature budget moves kind, one turn and the least certain step into the caption: check each against V7."""
    seen = set()
    for m in re.finditer(r'<article class="fga-tile[^"]*" data-loop="([^"]+)">(.*?)</article>', html, re.S):
        lid, body = m.group(1), m.group(2)
        seen.add(lid)
        cap = re.search(r'<p class="fga-cap">(.*?)</p>', body, re.S)
        if not cap:
            fail("catalog", f"{lid} tile has no caption")
            continue
        t = re.sub(r"<[^>]+>", "", cap.group(1))
        lp = LOOPS[lid]
        counts["captions_checked"] += 1
        kind = "Feeds itself." if lp["type"] == "R" else "Pushes back."
        if not t.startswith(kind):
            fail("catalog", f"{lid} caption kind {t[:14]!r}, V7 type {lp['type']}")
        if f"One turn: {DELAY_WORDS[lp['delay']]}." not in t:
            fail("catalog", f"{lid} caption turn differs from V7 delay {lp['delay']}")
        if not lp["closure"].startswith("closed"):
            if "Sketched in V7" not in t:
                fail("catalog", f"{lid} is sketched in V7, caption does not say so")
            continue
        want = VM.expected_weakest(lid)
        part = t.split("Least certain:", 1)[1] if "Least certain:" in t else ""
        named = set(re.findall(r"\b(L\d\d|LE\d\d|LT\d\d|LX\d|T\d\d)\b", part))
        if named != want:
            fail("catalog", f"{lid} caption names least certain {sorted(named)}, V7 ranks give {sorted(want)}")
        for k in want:
            if GRADE_WORDS[L[k]["evidence"]] not in part:
                fail("catalog", f"{lid} caption omits the grade of {k}")
        if not want and "no single step" not in part:
            fail("catalog", f"{lid} has no single least certain step, caption does not say so")
    if seen != set(LOOPS):
        fail("catalog", f"catalog tiles cover {len(seen)} loops, V7 has {len(LOOPS)}; missing {sorted(set(LOOPS) - seen)}")
    return len(seen)


def view_of(raw):
    m = re.search(r'data-view="([^"]+)"', raw)
    return m.group(1) if m else None


def run_file(f, root):
    view = root.get("data-view")
    if view in ("fg-mini", "fg-mini-phone", "fg-lead", "fg-card", "fg-card-phone", "fg-head", "fg-head-phone"):
        return view, check_loop(f, root, view)
    if view == "circuit-map":
        return view, check_circuit(f, root)
    if view == "fg-locator":
        return view, check_locator(f, root)
    fail(f, f"unknown view {view}")
    return view, None


def mutation_test():
    """Break one copy of each kind of drawing and confirm the checks catch every break."""
    cases = []

    def attempt(name, fname, mutate):
        root = ET.fromstring((ASSETS / fname).read_text(encoding="utf-8"))
        mutated = mutate(copy.deepcopy(root))
        before = len(problems)
        run_file("mutation:" + fname, mutated)
        caught = len(problems) - before
        del problems[before:]
        cases.append({"break": name, "file": fname, "caught": caught > 0, "reports": caught})

    def flip_sign(r):
        for t in r.iter(NS + "text"):
            if t.get("data-sign-glyph"):
                t.text = "−" if t.text == "+" else "+"
                break
        return r

    def drop_texture(r):
        for p in r.iter(NS + "path"):
            if p.get("data-texture") and p.get("data-texture") != "hollow":
                p.set("data-texture", "solid" if p.get("data-texture") != "solid" else "9 4")
                break
        return r

    def add_red(r):
        for g in r.iter(NS + "g"):
            if g.get("class") == "var" and not g.get("data-red"):
                g.set("data-red", "1")
                break
        return r

    def paint_red(r):
        for p in r.iter(NS + "rect"):
            p.set("fill", RED)
            break
        return r

    def drop_wire(r):
        for par in r.iter():
            for c in list(par):
                if c.get("class") == "link":
                    par.remove(c)
                    return r
        return r

    def miscount(r):
        for g in r.iter(NS + "g"):
            if g.get("class") == "bundle":
                g.set("data-count", str(int(g.get("data-count")) + 1))
                break
        return r

    def add_record(r):
        for g in r.iter(NS + "g"):
            if g.get("class") == "pill":
                ET.SubElement(g, NS + "rect", {"data-record": "1", "width": "4", "height": "4"})
                break
        return r

    def drop_weakest(r):
        for e in r.iter():
            if e.get("data-weakest"):
                del e.attrib["data-weakest"]
        return r

    def shift_delay(r):
        for g in r.iter(NS + "g"):
            if g.get("class") == "ticks":
                g.set("data-ticks", str(int(g.get("data-ticks")) % 3 + 1))
                break
        return r

    attempt("sign glyph flipped", "20261028_A-Mini-R1.svg", flip_sign)
    attempt("line texture changed", "20261028_A-Mini-R5.svg", drop_texture)
    attempt("red on a catalog variable", "20261028_A-Mini-R6.svg", add_red)
    attempt("record square on a miniature", "20261028_A-Mini-R12.svg", add_record)
    attempt("delay ticks miscounted", "20261028_A-Card-R8.svg", shift_delay)
    attempt("sign glyph flipped", "20261028_A-Card-R10.svg", flip_sign)
    attempt("weakest step mark removed", "20261028_A-Card-R10.svg", drop_weakest)
    attempt("red paint outside the targets", "20261028_A-Card-R10.svg", paint_red)
    attempt("one loop wire removed", "20261028_A-Circuit.svg", drop_wire)
    attempt("bundle count off by one", "20261028_A-Circuit.svg", miscount)
    def move_station(r):
        for g in r.iter(NS + "g"):
            if g.get("class") == "var":
                for e in g:
                    if e.tag == NS + "circle":
                        e.set("cx", str(float(e.get("cx")) + 6))
                        return r
        return r

    def unlight(r):
        for g in r.iter(NS + "g"):
            if g.get("class") == "step" and g.get("data-lit"):
                del g.attrib["data-lit"]
                break
        return r

    def flip_tag(r):
        for g in r.iter(NS + "g"):
            if g.get("data-sign-style") == "tag":
                a, b = (g.get("data-dir") or "0 0").split()
                g.set("data-dir", f"{-float(a):.0f} {-float(b):.0f}")
                break
        return r

    attempt("station moved off its cell", "20261028_A-Locator-Card-R8.svg", move_station)
    attempt("lit track unlit", "20261028_A-Locator-Card-R10.svg", unlight)
    attempt("red on a locator station", "20261028_A-Locator-Plate-B.svg", add_red)
    attempt("pointing tag turned around", "20261028_A-Card-R8-Tag.svg", flip_tag)
    return cases


def main():
    files = sorted(ASSETS.glob("20261028_A-*.svg"))
    board = BOARD.read_text(encoding="utf-8") if BOARD.exists() else ""
    circuit_page = CIRCUIT_PAGE.read_text(encoding="utf-8")
    views, catalogs, maps, locs = {}, {}, {}, {}
    # Direction C's reform view is embedded unchanged on the R-01 page and the board (fix 8); C's verifier checks
    # its data
    c_raw = C_REFORM.read_text(encoding="utf-8")
    c_body = c_raw.split("?>", 1)[1].strip() if c_raw.startswith("<?xml") else c_raw.strip()
    c_embeds = {name: (c_body in text) for name, text in (("R-01 page", REFORM_PAGE.read_text(encoding="utf-8")), ("board", board))}
    for name, ok in c_embeds.items():
        if not ok:
            fail(name, "Direction C's reform view is missing or differs from C's file")
    for path in files:
        f = path.name
        raw = path.read_text(encoding="utf-8")
        body = raw.split("?>", 1)[1].strip() if raw.startswith("<?xml") else raw
        home = circuit_page if view_of(raw) == "circuit-map" else board
        if body not in home:
            fail(f, "drawing file differs from every copy on " + ("the retired circuit page" if home is circuit_page else "the Direction A board"))
        root = ET.fromstring(raw)
        counts["svg_files"] += 1
        view, res = run_file(f, root)
        views[view] = views.get(view, 0) + 1
        if view in ("fg-mini", "fg-lead") and not ("Touches" in f or "Reform-" in f):
            catalogs.setdefault("fg-mini and fg-lead", set()).add(res)
        elif view == "fg-mini-phone" and not ("Touches" in f or "Reform-" in f):
            catalogs.setdefault("fg-mini-phone", set()).add(res)
        if view == "circuit-map":
            maps[f] = res
        if view == "fg-locator":
            locs[f] = res
    for k, s in catalogs.items():
        if s != set(LOOPS):
            fail(k, f"catalog draws {len(s)} loops, V7 has {len(LOOPS)}; missing {sorted(set(LOOPS) - s)}")
    n_caps = check_captions(CATALOG.read_text(encoding="utf-8"))
    real = list(problems)
    final = json.loads(json.dumps(counts))  # counts from the real drawings, before the mutation test adds its own
    cases = mutation_test()
    counts.clear()
    counts.update(final)
    missed = [c for c in cases if not c["caught"]]
    result = {
        "run_note": "Checked against work/extract/atlas-v7-data.json, independently of maps_model.py and the drawing code",
        "counts": counts, "views": views, "catalog_loops": {k: len(v) for k, v in catalogs.items()},
        "mismatches": len(real), "problems": real[:200],
        "mutation_test": {"cases": cases, "all_caught": not missed},
        "summary": [
            f"Data check against V7: {len(real)} mismatches across {counts['svg_files']} Direction A drawings and {n_caps} catalog captions.",
            f"All 23 loops drawn in the catalog: {len(catalogs.get('fg-mini and fg-lead', ()))} as miniatures and leads at 1440, {len(catalogs.get('fg-mini-phone', ()))} as phone miniatures at 390.",
            f"Checked {counts['steps_checked']} drawn loop steps and {counts['links_checked']} circuit wires for link, from, to, sign, type, delay and grade; "
            f"{counts['textures_checked']} line textures, {counts['ticks_checked']} delay-tick sets and {counts['glyphs_checked']} sign glyphs; "
            f"{counts['record_squares_absent_checked']} miniature sign discs carry no record square and {counts['ticks_absent_checked']} miniature steps carry no ticks.",
            "; ".join(f"{'the R-01 circuit' if 'Reform' in k else 'The circuit'} draws {v[0]} wires and counts {v[1]} connections in bundles" for k, v in maps.items()) + "; "
            f"{counts['bundles_checked']} bundle groups checked for count and V7 areas.",
            f"Checked {counts['red_marks_checked']} red marks, {counts['red_color_elements']} red-painted elements and {counts['weakest_checked']} weakest-step markings.",
            f"Locators: {counts['locators']} insets from Direction C's network data and station table; {counts['locator_tracks']} tracks checked against V7 and C's corridors, "
            f"{counts['locator_stations']} stations against C's grid cells, lit loops in Charcoal and every other line in Stone, no red.",
            f"Sign marks: {counts['arrowheads_checked']} steps checked for an arrowhead with the circled sign or none with the pointing tag; {counts['tag_directions_checked']} pointing tags point the way their step runs.",
            f"Direction C's reform view is embedded byte for byte on the R-01 page and the board ({sum(c_embeds.values())} of 2); its data is C's verifier's to check. The retired circuit is checked on its own page.",
            f"Mutation test: {len(cases) - len(missed)} of {len(cases)} deliberate breaks caught.",
        ],
    }
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(result["summary"]))
    for p in real[:40]:
        print("  ", p)
    for c in missed:
        print("   MISSED:", c)
    return 0 if not real and not missed else 1


if __name__ == "__main__":
    sys.exit(main())
