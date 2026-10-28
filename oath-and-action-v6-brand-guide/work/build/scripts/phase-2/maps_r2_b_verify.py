#!/usr/bin/env python3
"""Check every Direction B drawing and specimen page against Atlas V7, independently of the drawing code.

Run:  python3 -I work/build/scripts/phase-2/maps_r2_b_verify.py
Reads  work/extract/atlas-v7-data.json, through round one's verify_maps_data.py (raw V7, not maps_model.py)
       work/boards/phase-2/maps-r2/b/20261028_B-*.svg and the five specimen pages
Writes work/boards/phase-2/maps-r2/b/20261028_B-Verify-Results.json

Round one's check_step does the per-step work unchanged: link, from, to, sign, type, delay and grade carried on the
mark, the line texture against V7's dash code, the delay ticks and the sign label with its record square. This module
adds what Direction B draws: the shape from V7's loop type, the Archimedean geometry (every station, the echo and
every curve point read back and tested against p(t) = r (1 + (k - 1) t / 360)), one geometry per scale, the colors
(no red on any miniature, red only at the named reform's targets on a card), constant stroke weight, and the values
printed on the pages. A mutation test plants seven errors and confirms each one is caught.
"""
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_maps_data as VM  # noqa: E402  (round one's verifier, imported for its V7 copy and check_step)

ROOT = HERE.parents[3]
ASSETS = ROOT / "work/boards/phase-2/maps-r2/b"
BOARD = ROOT / "work/boards/20261028_Map-Direction-B-Snowball-And-Thermostat.html"
OUT = ASSETS / "20261028_B-Verify-Results.json"
NS = "{http://www.w3.org/2000/svg}"
N, L, LOOPS, REF = VM.N, VM.L, VM.LOOPS, VM.REF
INK, WHITE, RED, NEWS = "#121212", "#FFFFFF", "#E63946", "#DCD9D2"
HONEST = "Every snowball is drawn the same. The shape shows the kind of loop and never its speed or strength."
DIRECTION_WORD = {"running_up": "Running up", "running_down": "Running down", "running": "Running", "disabled": "Switched off",
                  "unknown": "Direction unknown", "design_target": "A design target",
                  "disabled in concentrated sectors": "Switched off in concentrated sectors"}
DELAY_WORD = {"S": "under 2 years", "M": "2 to 10 years", "L": "over 10 years"}
GRADE_WORD = {"documented": "documented", "well-supported": "well supported", "plausible": "plausible",
              "plausible_contested": "contested", "hypothesis": "hypothesis"}
TOL = 0.06

counts = {"svg_files": 0, "loop_views": 0, "steps_checked": 0, "stations_checked": 0, "echoes_checked": 0, "curve_points_checked": 0,
          "red_marks_checked": 0, "targets_checked": 0, "pages_checked": 0, "page_values_checked": 0, "inline_copies_checked": 0}


def area_group(lid):
    """Catalog group, recomputed here from raw V7: the area holding most of the loop's numbered variables, ties to
    the area first in V7's order; loops without a complete numbered chain form their own group."""
    lp = LOOPS[lid]
    if not lp["closure"].startswith("closed"):
        return "SK"
    c = {}
    for code, _ in lp["chain"]:
        a = N[code]["cluster"]
        c[a] = c.get(a, 0) + 1
    best = max(c.values())
    for a in ["A", "B", "C", "D", "E", "X", "EC", "TC"]:
        if c.get(a) == best:
            return a


def expected_weakest(lid):
    return VM.expected_weakest(lid)


def polar(cx, cy, x, y):
    t = math.degrees(math.atan2(x - cx, -(y - cy))) % 360
    return t, math.hypot(x - cx, y - cy)


def path_points(d):
    """Endpoints of an M ... C ... path: the M point and the last pair of every C."""
    toks = re.findall(r"[MC]|-?\d+(?:\.\d+)?", d)
    pts, i, cmd = [], 0, None
    nums = []
    for t in toks:
        if t in ("M", "C"):
            cmd = t
            nums = []
            continue
        nums.append(float(t))
        if cmd == "M" and len(nums) == 2:
            pts.append(tuple(nums))
            nums = []
        elif cmd == "C" and len(nums) == 6:
            pts.append((nums[4], nums[5]))
            nums = []
    return pts


def bezier_mids(d):
    """Midpoint (t = 0.5) of every cubic piece: (P0 + 3 C1 + 3 C2 + P3) / 8."""
    toks = re.findall(r"[MC]|-?\d+(?:\.\d+)?", d)
    cur, out, cmd, nums = None, [], None, []
    for t in toks:
        if t in ("M", "C"):
            cmd, nums = t, []
            continue
        nums.append(float(t))
        if cmd == "M" and len(nums) == 2:
            cur, nums = (nums[0], nums[1]), []
        elif cmd == "C" and len(nums) == 6:
            c1, c2, p3 = (nums[0], nums[1]), (nums[2], nums[3]), (nums[4], nums[5])
            out.append(((cur[0] + 3 * c1[0] + 3 * c2[0] + p3[0]) / 8, (cur[1] + 3 * c1[1] + 3 * c2[1] + p3[1]) / 8))
            cur, nums = p3, []
    return out


def colors(root):
    out = set()
    for e in root.iter():
        for a in ("fill", "stroke"):
            v = e.get(a)
            if v and v != "none":
                out.add(v.upper())
    return out


def check_loop_svg(f, raw, prob, scale_reg):
    root = ET.fromstring(raw)
    view = root.get("data-view")
    lid = root.get("data-loop")
    if lid not in LOOPS:
        prob.append(f"{f}: loop {lid} is not in V7")
        return
    counts["loop_views"] += 1
    lp = LOOPS[lid]
    want_shape = "spiral" if lp["type"] == "R" else "ring"
    if root.get("data-shape") != want_shape:
        prob.append(f"{f}: {lid} drawn as {root.get('data-shape')}, V7 type {lp['type']} needs {want_shape}")
    cx, cy, r, k = (float(root.get(a)) for a in ("data-cx", "data-cy", "data-r", "data-k"))
    if want_shape == "ring" and k != 1:
        prob.append(f"{f}: ring drawn with k {k}")
    n = len(lp["chain"])
    if int(root.get("data-n")) != n:
        prob.append(f"{f}: {lid} drawn with {root.get('data-n')} stations, V7 chain has {n}")
    # one geometry per scale and kind
    key = (view, root.get("data-test-k"))
    reg = scale_reg.setdefault(key, {})
    if want_shape == "spiral":
        reg.setdefault("spiral", set()).add((cx, cy, r, k))
    else:
        reg.setdefault("ring", set()).add((cx, cy, r))
    card = view in ("b-card", "b-test-card", "b-reform", "b-card-phone", "b-reform-phone", "b-test-phone")
    rho = lambda t: r * (1 + (k - 1) * t / 360.0)  # noqa: E731
    steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
    conceptual = not lp["closure"].startswith("closed")
    widths = set()
    if conceptual:
        labels = [lab for lab, _ in lp["chain_labels"]]
        if len(steps) != n:
            prob.append(f"{f}: {lid} draws {len(steps)} sketched steps, V7 chain has {n}")
        for i, g in enumerate(steps):
            counts["steps_checked"] += 1
            if g.get("data-sign") != lp["chain"][i][1]:
                prob.append(f"{f}: {lid} sketched step {i + 1} sign {g.get('data-sign')}, V7 {lp['chain'][i][1]}")
            if g.get("data-from-label") != labels[i] or g.get("data-to-label") != labels[(i + 1) % n]:
                prob.append(f"{f}: {lid} sketched step {i + 1} labels differ from V7 chain_labels")
            if not any(p.get("data-texture") == "hollow" for p in g.iter(NS + "path")):
                prob.append(f"{f}: {lid} sketched step {i + 1} is not in the hollow line")
    else:
        drawn = [g.get("data-link") for g in steps]
        if drawn != lp["links"]:
            prob.append(f"{f}: {lid} draws steps {drawn}, V7 {lp['links']}")
        before = len(VM.problems)
        for g in steps:
            counts["steps_checked"] += 1
            VM.check_step(f, g, root, require_marks=card, require_ticks=card)
        prob.extend(VM.problems[before:])
        del VM.problems[before:]
        if not card:
            if any(g.get("class") in ("pill", "ticks") for g in root.iter(NS + "g")):
                prob.append(f"{f}: a miniature carries sign labels or delay ticks, which the notation budget leaves to the card")
    for i, g in enumerate(steps):
        t0w, t1w = 360.0 * i / n, 360.0 * (i + 1) / n
        if abs(float(g.get("data-t0")) - t0w) > 1e-3 or abs(float(g.get("data-t1")) - t1w) > 1e-3:
            prob.append(f"{f}: {lid} step {i + 1} spans {g.get('data-t0')} to {g.get('data-t1')} degrees, equal angles need {t0w} to {t1w}")
        tex = [p for p in g.iter(NS + "path") if p.get("data-texture")]
        if tex:
            widths.add(tex[0].get("stroke-width"))
            for (x, y) in path_points(tex[0].get("d")) + bezier_mids(tex[0].get("d")):
                counts["curve_points_checked"] += 1
                t, p = polar(cx, cy, x, y)
                if t < t0w - 0.5 and t1w >= 359.9 and t < 1:
                    t += 360
                if i == n - 1 and t < 1:
                    t += 360
                if not (t0w - 0.01 <= t <= t1w + 0.01):
                    prob.append(f"{f}: {lid} step {i + 1} curve point at {t:.2f} degrees lies outside its span")
                    break
                if abs(p - rho(t)) > TOL:
                    prob.append(f"{f}: {lid} step {i + 1} curve point off the {'spiral' if k != 1 else 'ring'} by {abs(p - rho(t)):.3f} px")
                    break
    if len(widths) > 1:
        prob.append(f"{f}: stroke weights {sorted(widths)} differ within one view")
    # stations, then the echo
    lab_of = {c: lab for (c, _), (lab, _) in zip(lp["chain"], lp["chain_labels"])}
    vars_ = {g.get("data-node"): g for g in root.iter(NS + "g") if g.get("class") == "var"}
    want_vars = {c for c, _ in lp["chain"] if c in N}
    if set(vars_) != want_vars:
        prob.append(f"{f}: {lid} draws variables {sorted(vars_)}, V7 chain {sorted(want_vars)}")
    seats = [g for g in root.iter(NS + "g") if g.get("class") in ("var", "sketch")]
    for i, (code, _) in enumerate(lp["chain"]):
        counts["stations_checked"] += 1
        tw = 360.0 * i / n
        if code in N:
            g = vars_.get(code)
            if g is None:
                continue
            if g.get("data-label") != lab_of[code]:
                prob.append(f"{f}: {lid} variable {code} label {g.get('data-label')!r}, V7 chain label {lab_of[code]!r}")
            if code not in "".join(g.itertext()):
                prob.append(f"{f}: {lid} variable {code} disc does not print its ID")
        else:
            lab = lp["chain_labels"][i][0]
            g = next((s for s in seats if s.get("class") == "sketch" and s.get("data-concept-label") == lab), None)
            if g is None:
                prob.append(f"{f}: {lid} sketched station {lab!r} not drawn")
                continue
        c = next(g.iter(NS + "circle"))
        x, y = float(c.get("cx")), float(c.get("cy"))
        t, p = polar(cx, cy, x, y)
        if i == 0 and t > 359:
            t -= 360
        if abs(t - tw) > 0.02 or abs(p - rho(tw)) > TOL:
            prob.append(f"{f}: {lid} station {code} at {t:.2f} degrees and {p:.2f} px, geometry needs {tw:.2f} and {rho(tw):.2f}")
    echoes = [g for g in root.iter(NS + "g") if (g.get("class") or "").startswith("echo")]
    if want_shape == "ring":
        if echoes:
            prob.append(f"{f}: ring {lid} draws an echo")
    else:
        counts["echoes_checked"] += 1
        first = lp["chain"][0][0]
        if len(echoes) != 1:
            prob.append(f"{f}: spiral {lid} draws {len(echoes)} echoes, needs 1")
        else:
            e = echoes[0]
            if first in N and e.get("data-node") != first:
                prob.append(f"{f}: {lid} echo names {e.get('data-node')}, first station is {first}")
            if first in N and first not in "".join(e.itertext()):
                prob.append(f"{f}: {lid} echo does not print {first}")
            c = next(e.iter(NS + "circle"))
            t, p = polar(cx, cy, float(c.get("cx")), float(c.get("cy")))
            t = 360.0 if t < 1 else t
            if abs(t - 360) > 0.02 or abs(p - k * r) > TOL:
                prob.append(f"{f}: {lid} echo at {t:.2f} degrees and {p:.2f} px, needs 360 and {k * r:.2f}")
    # color and red
    cols = colors(root)
    rid = root.get("data-reform")
    if not card:
        if RED in cols:
            prob.append(f"{f}: red on a catalog miniature, which names no reform")
        extra = cols - {INK, WHITE}
        if extra:
            prob.append(f"{f}: colors {sorted(extra)} on a miniature; the shape and ink may not vary by loop")
    else:
        drawn_els = {g.get("data-link") for g in steps if g.get("data-link")} | set(vars_)
        want_red = (set(REF[rid]["targets"]) & drawn_els) if rid else set()
        red_at = set()
        for g in steps:
            if any(p.get("data-red") for p in g.iter(NS + "path")):
                red_at.add(g.get("data-link"))
        for g in list(vars_.values()) + echoes:
            if g.get("data-red"):
                red_at.add(g.get("data-node"))
                if g.get("data-target") != rid:
                    prob.append(f"{f}: red at {g.get('data-node')} names {g.get('data-target')}, the view names {rid}")
        for at in red_at:
            counts["red_marks_checked"] += 1
        counts["targets_checked"] += len(want_red)
        if red_at != want_red:
            prob.append(f"{f}: red at {sorted(red_at)}, {rid} targets drawn here {sorted(want_red)}")
        # no stray red: every red fill or stroke sits inside a red-marked step, variable or echo
        red_groups = [g for g in steps if g.get("data-link") in red_at] + [g for g in list(vars_.values()) + echoes if g.get("data-red")]
        inside = set()
        for g in red_groups:
            for e in g.iter():
                inside.add(id(e))
        for e in root.iter():
            if (e.get("fill") or "").upper() == RED or (e.get("stroke") or "").upper() == RED:
                if id(e) not in inside:
                    prob.append(f"{f}: a red mark sits outside the named reform's targets")
                    break
        if RED in cols and root.find(NS + "rect") is not None and (root.find(NS + "rect").get("fill") or "").upper() != WHITE:
            prob.append(f"{f}: red drawn on a ground other than White")


def text_of_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def check_catalog(f, html_, prob):
    counts["pages_checked"] += 1
    found = {}
    for m in re.finditer(r'<li class="tile" data-loop="([^"]+)" data-kind="([RB])">(.*?)</p></li>', html_, re.S):
        found.setdefault(m.group(1), []).append((m.group(2), m.group(3)))
    if set(found) != set(LOOPS):
        prob.append(f"{f}: catalog holds {len(found)} loops, V7 has {len(LOOPS)}; missing {sorted(set(LOOPS) - set(found))}")
    for lid, rows in found.items():
        if len(rows) != 1:
            prob.append(f"{f}: {lid} appears {len(rows)} times")
        kind, body = rows[0]
        lp = LOOPS[lid]
        counts["page_values_checked"] += 1
        if kind != lp["type"]:
            prob.append(f"{f}: {lid} tile kind {kind}, V7 {lp['type']}")
        want_kw = "Feeds itself" if lp["type"] == "R" else "Pushes back"
        if want_kw not in body:
            prob.append(f"{f}: {lid} tile does not say {want_kw}")
        m = re.search(r'data-direction="([^"]+)" data-delay="([^"]+)">(.*)$', body, re.S)
        if not m:
            prob.append(f"{f}: {lid} tile has no facts line")
            continue
        d, dl, facts = m.group(1), m.group(2), text_of_html(m.group(3))
        if d != lp["direction"] or dl != lp["delay"]:
            prob.append(f"{f}: {lid} facts carry {d}/{dl}, V7 {lp['direction']}/{lp['delay']}")
        if not facts.startswith(DIRECTION_WORD[lp["direction"]] + " "):
            prob.append(f"{f}: {lid} facts read {facts[:40]!r}, V7 direction {lp['direction']}")
        if lp["closure"].startswith("closed"):
            if f"{DELAY_WORD[lp['delay']]} a turn" not in facts:
                prob.append(f"{f}: {lid} facts miss the delay {DELAY_WORD[lp['delay']]}")
            w = expected_weakest(lid)
            if w:
                for k in w:
                    if k not in facts or GRADE_WORD[L[k]["evidence"]] not in facts:
                        prob.append(f"{f}: {lid} facts do not name weakest step {k} with its grade")
            elif "Every step graded" not in facts and "Steps tie" not in facts:
                prob.append(f"{f}: {lid} facts name a weakest step where V7's ranks tie")
            if lp["closure"].startswith("closed with a hypothesized") != ("hypothesized step" in facts):
                prob.append(f"{f}: {lid} facts misstate its closure")
        # stations listed by ID and label, in chain order
        names = re.findall(r"<li><b>([^<]*)</b><span>([^<]*)</span></li>", body)
        want = [(c if c in N else "", lab) for (c, _), (lab, _) in zip(lp["chain"], lp["chain_labels"])]
        if [(a, b.replace("&#x27;", "'").replace("&amp;", "&")) for a, b in names] != want:
            prob.append(f"{f}: {lid} station list {names}, V7 {want}")
        # the miniature inlined in the tile equals the file
        mini = (ASSETS / f"20261028_B-Mini-{lid}.svg").read_text(encoding="utf-8").split("?>", 1)[1].strip()
        counts["inline_copies_checked"] += 1
        if mini not in body:
            prob.append(f"{f}: {lid} tile's drawing differs from 20261028_B-Mini-{lid}.svg")
    # groups by area
    for m in re.finditer(r'<section class="area" id="area-([A-Z]+)" data-group="([A-Z]+)">(.*?)</section>', html_, re.S):
        g = m.group(2)
        ids = re.findall(r'<li class="tile" data-loop="([^"]+)"', m.group(3))
        for lid in ids:
            counts["page_values_checked"] += 1
            if area_group(lid) != g:
                prob.append(f"{f}: {lid} sits in area {g}, V7's chain puts it in {area_group(lid)}")
    nR = sum(1 for lp in LOOPS.values() if lp["type"] == "R")
    nB = sum(1 for lp in LOOPS.values() if lp["type"] == "B")
    for k, want in (("R", f"{nR} feed themselves"), ("B", f"{nB} push back")):
        counts["page_values_checked"] += 1
        if f'data-count="{k}">{want}<' not in html_:
            prob.append(f"{f}: head count for {k} does not read {want!r}")
    if html_.count(HONEST) < 1:
        prob.append(f"{f}: the printed honesty line is missing or altered")
    # the catalog names no reform: its only red is the wordmark's signature ampersand (Rule 05.3)
    body = html_.split("</head>", 1)[1]
    reds = len(re.findall(r"#E63946", body, re.I))
    amp = len(re.findall(r"var\(--amp,#E63946\)", body, re.I))
    counts["page_values_checked"] += 1
    if reds != amp:
        prob.append(f"{f}: {reds - amp} red marks on the catalog beyond the wordmark's signature ampersand")


def check_card_page(f, html_, lid, rid, prob):
    counts["pages_checked"] += 1
    lp = LOOPS[lid]
    rows = re.findall(r'<tr data-link="([^"]+)" data-from="([^"]+)" data-to="([^"]+)" data-sign="([^"]*)" data-grade="([^"]+)" data-delay="([^"]+)">', html_)
    if [r[0] for r in rows] != lp["links"]:
        prob.append(f"{f}: step table lists {[r[0] for r in rows]}, V7 {lp['links']}")
    for k, fr, to, sg, gr, dl in rows:
        counts["page_values_checked"] += 1
        l = L[k]
        if (fr, to, sg, gr, dl) != (l["from"], l["to"], l["polarity"], l["evidence"], l["delay"]):
            prob.append(f"{f}: step table row {k} reads {(fr, to, sg, gr, dl)}, V7 {(l['from'], l['to'], l['polarity'], l['evidence'], l['delay'])}")
    if rid:
        r = REF[rid]
        eff = dict(re.findall(r'<tr data-family="([A-Z]+)" data-effect="([^"]*)">', html_))
        counts["page_values_checked"] += len(eff)
        if {k: v.replace("&#x27;", "'") for k, v in eff.items()} != r["effects"]:
            prob.append(f"{f}: effects {eff}, V7 {r['effects']}")
        routes = re.findall(r'<tr data-route="([A-Z]+)" data-checked="([^"]*)">', html_)
        counts["page_values_checked"] += len(routes)
        want = [(x["route"], x["checked"] or "") for x in r["routes"]]
        if routes != want:
            prob.append(f"{f}: routes {routes}, V7 {want}")
        if "Not checked" not in html_ and any(not x["checked"] for x in r["routes"]):
            prob.append(f"{f}: an undated route is not shown as unchecked")


def inline_copies(f, html_, files, prob):
    for p in files:
        body = p.read_text(encoding="utf-8").split("?>", 1)[1].strip()
        # pages tag the desktop and phone figure with a class; compare without it
        h = html_.replace('<svg class="desk" ', "<svg ").replace('<svg class="phone" ', "<svg ")
        counts["inline_copies_checked"] += 1
        if body not in h:
            prob.append(f"{f}: inline copy of {p.name} differs from the file")


def run(files_text=None, pages_text=None, board_text=None):
    """Run every check. files_text and pages_text let the mutation test pass edited copies."""
    prob = []
    scale_reg = {}
    svgs = files_text or {p.name: p.read_text(encoding="utf-8") for p in sorted(ASSETS.glob("20261028_B-*.svg"))}
    for name, raw in svgs.items():
        counts["svg_files"] += 1
        root = ET.fromstring(raw.split("?>", 1)[1] if raw.startswith("<?xml") else raw)
        if root.get("data-loop"):
            check_loop_svg(name, raw.split("?>", 1)[1] if raw.startswith("<?xml") else raw, prob, scale_reg)
    for key, reg in scale_reg.items():
        for kind, s in reg.items():
            if len(s) > 1:
                prob.append(f"{key[0]}: {len(s)} different {kind} geometries at one scale; every loop of a kind must share one")
        if "spiral" in reg and "ring" in reg:
            (sx, sy, sr, sk), = list(reg["spiral"])[:1] if len(reg["spiral"]) == 1 else [next(iter(reg["spiral"]))]
            (rx, ry, rr), = list(reg["ring"])[:1] if len(reg["ring"]) == 1 else [next(iter(reg["ring"]))]
            if (sx, sy, sr) != (rx, ry, rr):
                prob.append(f"{key[0]}: the ring is not drawn at the spiral's starting radius and center")
    ks = {k for key, reg in scale_reg.items() if key[1] is None for (_, _, _, k) in reg.get("spiral", set())}
    if len(ks) > 1:
        prob.append(f"spiral growth k differs across scales: {sorted(ks)}")
    minis = {n for n in svgs if n.startswith("20261028_B-Mini-")}
    if {n[len("20261028_B-Mini-"):-4] for n in minis} != set(LOOPS):
        prob.append(f"miniatures drawn for {len(minis)} loops, V7 has {len(LOOPS)}")
    pages = pages_text or {p.name: p.read_text(encoding="utf-8") for p in sorted(ASSETS.glob("20261028_Direction-B-*.html"))}
    for name, h in pages.items():
        if "Loop-Catalog" in name:
            check_catalog(name, h, prob)
        m = re.search(r"Loop-Card-(R8|R10|B4)", name)
        if m:
            lid = m.group(1)
            rid = re.search(r'<article data-loop="[^"]+" data-reform="([^"]*)"', h).group(1)
            check_card_page(name, h, lid, rid, prob)
            inline_copies(name, h, [ASSETS / f"20261028_B-Card-{lid}.svg", ASSETS / f"20261028_B-Card-Phone-{lid}.svg"], prob)
        if "Reform-View-R-01" in name:
            counts["pages_checked"] += 1
            t1 = dict(re.findall(r'<tr data-family="([A-Z]+)" data-effect="([^"]*)">', h))
            if t1 != REF["R-01"]["effects"]:
                prob.append(f"{name}: effects {t1}, V7 {REF['R-01']['effects']}")
            routes = re.findall(r'<tr data-route="([A-Z]+)" data-checked="([^"]*)">', h)
            if routes != [(x["route"], x["checked"] or "") for x in REF["R-01"]["routes"]]:
                prob.append(f"{name}: routes {routes} differ from V7")
            counts["page_values_checked"] += len(t1) + len(routes)
            inline_copies(name, h, [ASSETS / "20261028_B-Reform-R-01-On-R10.svg", ASSETS / "20261028_B-Reform-R-01-On-R10-Phone.svg",
                                    ASSETS / "20261028_B-Mini-B4.svg", ASSETS / "20261028_B-Mini-R11.svg"], prob)
    board = board_text if board_text is not None else (BOARD.read_text(encoding="utf-8") if BOARD.exists() else None)
    if board:
        inl = [p for p in sorted(ASSETS.glob("20261028_B-Test-*.svg"))] + [ASSETS / f"20261028_B-Kind-Mark-{k}-24.svg" for k in ("Snowball", "Thermostat")]
        inline_copies(BOARD.name, board, inl, prob)
        if HONEST not in board:
            prob.append(f"{BOARD.name}: the printed honesty line is missing")
    return prob


MUTATIONS = [
    ("L39 drawn dashed though V7 grades it well supported", "20261028_B-Card-R8.svg",
     lambda s: s.replace('data-link="L39"', 'data-link="L39"', 1).replace('stroke-width="2.5" data-texture="solid" data-red="1"', 'stroke-width="2.5" stroke-dasharray="9 4" data-texture="9 4" data-red="1"', 1)),
    ("C2 disc moved 6 px off its angle on the R10 miniature", "20261028_B-Mini-R10.svg",
     lambda s: re.sub(r'(<g class="var" data-node="C2"[^>]*><circle cx=")([\d.]+)', lambda m: m.group(1) + f"{float(m.group(2)) + 6:.2f}", s, count=1)),
    ("R1 miniature claims a different growth k", "20261028_B-Mini-R1.svg",
     lambda s: s.replace('data-k="1.8"', 'data-k="1.6"', 1)),
    ("L38 turned red on the R8 card, though R-30 does not target it", "20261028_B-Card-R8.svg",
     lambda s: re.sub(r'(<g class="step"[^>]*data-link="L38"[^>]*><path [^>]*?)stroke="#121212"([^>]*?)data-texture="solid"', r'\1stroke="#E63946"\2data-texture="solid" data-red="1"', s, count=1)),
    ("B4 drawn as a spiral", "20261028_B-Mini-B4.svg",
     lambda s: s.replace('data-shape="ring"', 'data-shape="spiral"', 1)),
    ("one delay tick removed from L53 on the R10 card", "20261028_B-Card-R10.svg",
     lambda s: re.sub(r'(data-link="L53".*?<g class="ticks" data-ticks="2">)(<line[^>]*/>)', r"\1", s, count=1, flags=re.S)),
    ("R5 tile says running up though V7 records running down", "20261028_Direction-B-Loop-Catalog.html",
     lambda s: s.replace('data-loop="R5" data-kind="R">', 'data-loop="R5" data-kind="R">', 1).replace(
         'data-direction="running_down" data-delay="L">Running down', 'data-direction="running_up" data-delay="L">Running up', 1)),
]


def mutation_test():
    svgs = {p.name: p.read_text(encoding="utf-8") for p in sorted(ASSETS.glob("20261028_B-*.svg"))}
    pages = {p.name: p.read_text(encoding="utf-8") for p in sorted(ASSETS.glob("20261028_Direction-B-*.html"))}
    base = len(run(dict(svgs), dict(pages), ""))
    out = []
    for desc, name, fn in MUTATIONS:
        s2, p2 = dict(svgs), dict(pages)
        if name in s2:
            new = fn(s2[name])
            changed = new != s2[name]
            s2[name] = new
        else:
            new = fn(p2[name])
            changed = new != p2[name]
            p2[name] = new
        found = run(s2, p2, "")
        out.append({"planted": desc, "file": name, "edit_applied": changed, "caught": len(found) > base,
                    "first_report": (found[0] if found else None)})
    return base, out


def main():
    global counts
    prob = run()
    final_counts = dict(counts)
    for k in counts:
        counts[k] = 0
    base, mut = mutation_test()
    for k in counts:
        counts[k] = 0
    result = {
        "run_note": "Checked against work/extract/atlas-v7-data.json through verify_maps_data.py, independently of maps_model.py and the drawing code",
        "counts": final_counts, "mismatches": len(prob), "problems": prob[:200],
        "mutation_test": {"baseline_mismatches": base, "planted": mut, "all_caught": all(m["caught"] and m["edit_applied"] for m in mut)},
        "summary": [
            f"Data check against V7: {len(prob)} mismatches across {final_counts['svg_files']} drawings and {final_counts['pages_checked']} specimen pages.",
            f"All {len(LOOPS)} loops drawn as miniatures and listed on the catalog page; each shape follows V7's loop type (spiral for R, ring for B).",
            f"Checked {final_counts['steps_checked']} drawn steps (link, from, to, sign, type, delay, grade, texture; ticks and sign labels on cards), "
            f"{final_counts['stations_checked']} stations and {final_counts['echoes_checked']} echoes against the equal-angle Archimedean geometry, "
            f"and {final_counts['curve_points_checked']} curve points (every Bezier endpoint and midpoint) against p(t) within {TOL} px.",
            f"Checked {final_counts['red_marks_checked']} red marks against {final_counts['targets_checked']} targets of the reform each card names; "
            "no miniature carries red or any ink but Charcoal on White.",
            f"Checked {final_counts['page_values_checked']} printed values on the pages (directions, delays, weakest steps, step tables, effects, routes) "
            f"and {final_counts['inline_copies_checked']} inline drawing copies against their files.",
            "Mutation test: " + ", ".join(f"{'caught' if m['caught'] else 'MISSED'}: {m['planted']}" for m in mut) + ".",
        ],
    }
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(result["summary"]))
    for p in prob[:40]:
        print("  ", p)
    return 0 if not prob and result["mutation_test"]["all_caught"] else 1


if __name__ == "__main__":
    sys.exit(main())
