#!/usr/bin/env python3
"""Check every Direction C drawing against Atlas V7 and the station table, independently of the drawing code.

Run:  python3 -I work/build/scripts/phase-2/maps_r2_c_verify.py            (checks the drawings in maps-r2/c)
      python3 -I work/build/scripts/phase-2/maps_r2_c_verify.py --mutate   (plants five errors in copies and
                                                                            confirms the checks catch each one)
Reads  work/extract/atlas-v7-data.json through round one's verify_maps_data.py (raw V7, not maps_model.py), its
       grade dash code, tick counts, grade ranks, sign glyphs, weakest-step and reform-target rules
       work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Station-Table.csv (the 25 station positions)
       work/boards/phase-2/maps-r2/c/20261028_*.svg and the pages that inline them
Writes work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Verify-Results.json
"""
import csv
import importlib.util
import json
import math
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("verify_maps_data", HERE / "verify_maps_data.py")
VM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VM)            # round one's verifier: raw V7 and its rules; its main() is not run

ROOT = VM.ROOT
ASSETS = ROOT / "work/boards/phase-2/maps-r2/c"
TABLE = ASSETS / "20261028_Loop-Lines-Station-Table.csv"
OUT = ASSETS / "20261028_Loop-Lines-Verify-Results.json"
NS = VM.NS
V7, N, L, LOOPS, REF = VM.V7, VM.N, VM.L, VM.LOOPS, VM.REF
RED = "#E63946"
CHARCOAL, NEWSPRINT, STONE = "#121212", "#DCD9D2", "#5D636D"
FULL_VIEWS = ("c-poster", "c-poster-print", "c-working", "c-reform")
NUMBERED = [k for k, lp in LOOPS.items() if lp["closure"].startswith("closed")]
SKETCHED = [k for k, lp in LOOPS.items() if not lp["closure"].startswith("closed")]
LOOP_VARS = sorted({c for k in NUMBERED for c, _ in LOOPS[k]["chain"]})
LOOP_LINKS = sorted({x for k in NUMBERED for x in LOOPS[k]["links"]})


def chain_label_index():
    idx = {}
    for lp in LOOPS.values():
        for (code, _), (lab, _) in zip(lp["chain"], lp["chain_labels"]):
            if code in N and code not in idx:
                idx[code] = lab
    return idx


LABEL = chain_label_index()


def loops_of_var(v):
    return sorted(k for k in NUMBERED if any(c == v for c, _ in LOOPS[k]["chain"]))


def area(v):
    return N[v]["cluster"]


def frame_group(v):
    n = N[v]
    if n["layer"] == "economy":
        return "EC"
    if n["layer"] == "technology":
        return "TC"
    return n["cluster"]


class Run:
    def __init__(self, assets):
        self.assets = Path(assets)
        self.problems = []
        self.c = {k: 0 for k in ("svg_files", "steps_checked", "textures_checked", "signs_checked", "ticks_checked",
                                 "records_checked", "stations_checked", "positions_checked", "bullets_checked",
                                 "red_marks_checked", "weakest_checked", "ghosts_checked", "entries_checked",
                                 "fields_checked", "sketched_steps_checked", "pages_checked", "catalog_cards_checked",
                                 "bullet_tracks_checked", "lit_steps_checked", "lit_stations_checked")}
        self.table = self.read_table()

    def fail(self, f, msg):
        self.problems.append(f"{f}: {msg}")

    def read_table(self):
        rows = {}
        with open(self.assets / TABLE.name, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                rows[r["id"]] = r
        return rows

    # ------------------------------------------------------------ shared pieces
    def check_step_attrs(self, f, g):
        k = g.get("data-link")
        l = L.get(k)
        if l is None:
            self.fail(f, f"{k} is not a V7 connection")
            return None
        for attr, val in (("data-from", l["from"]), ("data-to", l["to"]), ("data-sign", l["polarity"] or "none"),
                          ("data-grade", l["evidence"]), ("data-delay", l["delay"]), ("data-type", l["type"])):
            if g.get(attr) != val:
                self.fail(f, f"{k} {attr} drawn {g.get(attr)!r}, V7 {val!r}")
        lid = g.get("data-loop")
        if lid and lid not in l["loops"]:
            self.fail(f, f"{k} drawn on loop {lid}, V7 lists it on {l['loops']}")
        path = next((p for p in g.iter(NS + "path") if p.get("data-texture")), None)
        if path is None:
            self.fail(f, f"{k} has no textured line")
            return l
        code = VM.DASH[l["evidence"]]
        w = float(path.get("data-weight") or 2)
        want = None if code == "solid" else " ".join(f"{float(x) * w / 2:g}" for x in code.split())
        got = path.get("stroke-dasharray")
        self.c["textures_checked"] += 1
        if path.get("data-texture") != code or (got or None) != want:
            self.fail(f, f"{k} texture {path.get('data-texture')}/{got}, V7 grade {l['evidence']} needs {code} scaled to {want}")
        return l

    def check_sign(self, f, sg, l, k):
        gl = [t for t in sg.iter(NS + "text") if t.get("data-sign-glyph")]
        want = VM.GLYPH.get(l["polarity"], "")
        self.c["signs_checked"] += 1
        if not gl or VM.text_of(gl[0]) != want:
            self.fail(f, f"{k} sign glyph {VM.text_of(gl[0]) if gl else None!r}, V7 sign {l['polarity']!r}")

    def tag_points(self, sg):
        poly = next(sg.iter(NS + "polygon"), None)
        if poly is None:
            return None
        pts = [tuple(float(v) for v in p.split(",")) for p in poly.get("points").split()]
        return pts

    def svg_pos(self, g):
        c = next(g.iter(NS + "circle"), None)
        if c is not None:
            return float(c.get("cx")), float(c.get("cy"))
        r = next(g.iter(NS + "rect"), None)
        return float(r.get("x")) + float(r.get("width")) / 2, float(r.get("y")) + float(r.get("height")) / 2

    def red_elements(self, root):
        """Every element painted Pillar Red, mapped to the connection or variable it belongs to."""
        hits = set()
        parent = {c: p for p in root.iter() for c in p}
        for e in root.iter():
            if (e.get("stroke") or "").upper() == RED or (e.get("fill") or "").upper() == RED or e.get("data-red"):
                x = e
                at = None
                while x is not None:
                    at = x.get("data-link") or x.get("data-node")
                    if at:
                        break
                    x = parent.get(x)
                hits.add(at)
        return hits

    # ------------------------------------------------------------ network views
    def check_network(self, f, root, view):
        steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
        pairs = {}
        for g in steps:
            self.c["steps_checked"] += 1
            l = self.check_step_attrs(f, g)
            key = (g.get("data-loop"), g.get("data-link"))
            pairs[key] = pairs.get(key, 0) + 1
        want = {(k, x) for k in NUMBERED for x in LOOPS[k]["links"]}
        if set(pairs) != want:
            self.fail(f, f"draws {len(pairs)} loop tracks, V7 numbered loops need {len(want)}; missing {sorted(want - set(pairs))[:5]}, extra {sorted(set(pairs) - want)[:5]}")
        dup = [k for k, v in pairs.items() if v != 1]
        if dup:
            self.fail(f, f"tracks drawn more than once: {dup[:5]}")
        loops_drawn = {k for k, _ in pairs}
        if loops_drawn != set(NUMBERED):
            self.fail(f, f"loops drawn {sorted(loops_drawn)}, V7 numbered {sorted(NUMBERED)}")
        # stations and their positions from the table
        cell, ox, oy = float(root.get("data-cell")), float(root.get("data-ox")), float(root.get("data-oy"))
        vars_ = {g.get("data-node"): g for g in root.iter(NS + "g") if g.get("class") == "var"}
        if set(vars_) != set(LOOP_VARS):
            self.fail(f, f"draws {len(vars_)} stations, V7 numbered loops run through {len(LOOP_VARS)}")
        if len(self.table) != 25 or set(self.table) != set(LOOP_VARS):
            self.fail(f, f"station table holds {len(self.table)} rows {sorted(self.table)}, V7 needs {LOOP_VARS}")
        for v, g in vars_.items():
            self.c["stations_checked"] += 1
            if g.get("data-label") != LABEL.get(v):
                self.fail(f, f"{v} label {g.get('data-label')!r}, V7 chain label {LABEL.get(v)!r}")
            lps = sorted(g.get("data-loops", "").split())
            if lps != loops_of_var(v):
                self.fail(f, f"{v} marked on loops {lps}, V7 {loops_of_var(v)}")
            kind = g.get("data-kind")
            want_kind = "ring" if len(loops_of_var(v)) == 1 else ("hub" if len(loops_of_var(v)) >= 5 else "capsule")
            if view in FULL_VIEWS and kind != want_kind:
                self.fail(f, f"{v} drawn as {kind}, a station on {len(loops_of_var(v))} loops is a {want_kind}")
            if view in FULL_VIEWS and v not in VM.text_of(g):
                self.fail(f, f"{v} station does not print its ID")
            t = self.table.get(v)
            if t:
                self.c["positions_checked"] += 1
                x, y = self.svg_pos(g)
                ex, ey = ox + int(t["col"]) * cell, oy + int(t["row"]) * cell
                if abs(x - ex) > 0.6 or abs(y - ey) > 0.6:
                    self.fail(f, f"{v} drawn at ({x:.1f}, {y:.1f}), station table puts it at ({ex:.1f}, {ey:.1f})")
                if area(v) != t["district"]:
                    self.fail(f, f"{v} table district {t['district']}, V7 cluster {area(v)}")
        # signs: one per connection, glyph and the way it points
        signs = [g for g in root.iter(NS + "g") if g.get("class") == "sign" and g.get("data-for")]
        if signs or view in FULL_VIEWS:
            got = sorted(g.get("data-for") for g in signs)
            if got != LOOP_LINKS:
                self.fail(f, f"{len(got)} sign tags, V7 numbered loops ride {len(LOOP_LINKS)} connections; missing {sorted(set(LOOP_LINKS) - set(got))[:5]}")
            for sg in signs:
                k = sg.get("data-for")
                l = L.get(k)
                if not l:
                    continue
                self.check_sign(f, sg, l, k)
                pts = self.tag_points(sg)
                if pts and l["from"] in self.table and l["to"] in self.table:
                    cx = sum(p[0] for p in pts) / len(pts)
                    cy = sum(p[1] for p in pts) / len(pts)
                    tip = pts[2]
                    a, b = self.table[l["from"]], self.table[l["to"]]
                    dx, dy = int(b["col"]) - int(a["col"]), int(b["row"]) - int(a["row"])
                    if (tip[0] - cx) * dx + (tip[1] - cy) * dy <= 0:
                        self.fail(f, f"{k} sign tag points against the step's direction {l['from']} to {l['to']}")
        # bullets
        bullets = [g for g in root.iter(NS + "g") if g.get("class") == "bullet"]
        if bullets or view == "c-poster":
            ids = sorted(g.get("data-bullet") for g in bullets)
            if ids != sorted(NUMBERED):
                self.fail(f, f"bullets {ids}, V7 numbered loops {sorted(NUMBERED)}")
            for g in bullets:
                self.c["bullets_checked"] += 1
                lid = g.get("data-bullet")
                if g.get("data-kind") != LOOPS.get(lid, {}).get("type") or lid not in VM.text_of(g):
                    self.fail(f, f"bullet {lid} kind {g.get('data-kind')}, V7 {LOOPS.get(lid, {}).get('type')}")
                if g.get("data-first") and g.get("data-first") != LOOPS[lid]["chain"][0][0]:
                    self.fail(f, f"bullet {lid} first station {g.get('data-first')}, V7 chain starts {LOOPS[lid]['chain'][0][0]}")
                self.check_bullet_track(f, root, g, lid)
                glyphs = [x for x in g.iter(NS + "g") if x.get("class") == "kind"]
                if view == "c-poster-print":
                    if len(glyphs) != 1 or glyphs[0].get("data-kind") != LOOPS[lid]["type"]:
                        self.fail(f, f"print bullet {lid} carries kind glyph {[x.get('data-kind') for x in glyphs]}, V7 kind {LOOPS[lid]['type']}")
                elif glyphs:
                    self.fail(f, f"screen bullet {lid} carries a kind glyph, which draws under 24 px on screen")
        # red
        rid = root.get("data-reform")
        reds = self.red_elements(root)
        self.c["red_marks_checked"] += len(reds)
        want_red = set(REF[rid]["targets"]) & (set(LOOP_LINKS) | set(LOOP_VARS)) if rid else set()
        if reds != want_red:
            self.fail(f, f"red at {sorted(x for x in reds if x)}, expected {sorted(want_red)}")
        if root.get("fill") == "#1F2D5A" or (next(root.iter(NS + "rect")).get("fill") or "").upper() == "#1F2D5A":
            if reds:
                self.fail(f, "red sits on Prussian")
        if root.get("data-lit") and view in ("c-working", "c-reform", "c-locator"):
            self.check_lit(f, root, view)
        # sketched loops and the register note on the poster views
        if view in FULL_VIEWS:
            kinds = " ".join(VM.text_of(t) for t in root.iter(NS + "text") if t.get("data-note") == "kinds")
            if "R: feeds itself." not in kinds or "B: pushes back." not in kinds:
                self.fail(f, f"legend kind line reads {kinds!r}")
            sk = [g for g in root.iter(NS + "g") if g.get("class") == "sketched"]
            if not sk or sorted(sk[0].get("data-sketched", "").split()) != sorted(SKETCHED):
                self.fail(f, f"sketched loops listed {sk[0].get('data-sketched') if sk else None}, V7 {sorted(SKETCHED)}")
            note = " ".join(VM.text_of(t) for t in root.iter(NS + "text") if t.get("data-note") == "register")
            for n_, what in ((len(NUMBERED), "numbered loops"), (len(LOOP_VARS), "variables"), (len(LOOP_LINKS), "connections"),
                             (len(N), "variables"), (len(L), "connections")):
                if f"{n_} " not in note:
                    self.fail(f, f"register note lacks the count {n_} {what}: {note!r}")
            spacing = [t for t in root.iter(NS + "text") if t.get("data-note") == "spacing"]
            if not spacing or "no meaning" not in VM.text_of(spacing[0]):
                self.fail(f, "the poster does not say that spacing carries no meaning")
            self.check_frame(f, root)
            self.check_fields(f, root, cell, ox, oy)

    def check_frame(self, f, root):
        """Each band of the frame is one line of words: its variable count and, per area, how many of its
        connections reach that area, all recounted from V7."""
        counts = {}
        for k, l in L.items():
            a, b = frame_group(l["from"]), frame_group(l["to"])
            for g, d in ((a, b), (b, a)):
                if g in ("EC", "TC", "X") and d in "ABCDE":
                    counts.setdefault((g, d), set()).add(k)
        seen = set()
        if [e for e in root.iter(NS + "g") if e.get("class") == "entry"]:
            self.fail(f, "the frame still draws entry ticks")
        for t in root.iter(NS + "text"):
            g = t.get("data-frame-note")
            if not g:
                continue
            seen.add(g)
            txt = VM.text_of(t)
            total = sum(len(v) for (gg, d), v in counts.items() if gg == g)
            nvars = sum(1 for v in N if frame_group(v) == g)
            if int(t.get("data-total")) != total or f"{total} connections" not in txt:
                self.fail(f, f"frame note {g} total {t.get('data-total')}, V7 {total}")
            if int(t.get("data-vars")) != nvars or f"{nvars} variables" not in txt:
                self.fail(f, f"frame note {g} counts {t.get('data-vars')} variables, V7 {nvars}")
            drawn = dict(x.split(":") for x in t.get("data-counts", "").split())
            for d in "ABCDE":
                n = len(counts.get((g, d), ()))
                self.c["entries_checked"] += 1
                if int(drawn.get(d, 0)) != n:
                    self.fail(f, f"frame note {g} gives {drawn.get(d, 0)} connections into area {d}, V7 {n}")
                if n and not (f"{n} into area {d}" in txt or re.search(rf"\b{n} each into areas [A-E, and]*\b{d}\b", txt)):
                    self.fail(f, f"frame note {g} does not say its {n} connections into area {d}: {txt!r}")
        if seen != {"X", "EC", "TC"}:
            self.fail(f, f"frame notes for {sorted(seen)}, V7 groups X, EC and TC")

    def check_bullet_track(self, f, root, g, lid):
        """A bullet sits on a stretch only its own loop rides: on its track, or on a 1 px leader from that track."""
        on = g.get("data-on", "")
        a, _, b = on.partition("-")
        here = {x for x, l in L.items() if {l["from"], l["to"]} == {a, b}}
        riders = {k for x in here for k in L[x]["loops"] if k in NUMBERED}
        self.c["bullet_tracks_checked"] += 1
        if not here or riders != {lid}:
            self.fail(f, f"bullet {lid} set on {on}, which loops {sorted(riders)} ride; a bullet goes on a stretch only its loop rides")
            return
        polys = []
        for st in root.iter(NS + "g"):
            if st.get("class") == "step" and st.get("data-loop") == lid and st.get("data-link") in here:
                p = next((x for x in st.iter(NS + "path") if x.get("data-texture")), None)
                if p is not None:
                    polys.append(_path_points(p.get("d")))
        lead = g.get("data-leader")
        cx, cy = float(g.get("data-cx")), float(g.get("data-cy"))
        if lead:
            x0, y0, x1, y1 = (float(v) for v in lead.split())
            d0 = min(_dist_poly((x0, y0), pl) for pl in polys) if polys else 1e9
            rects = [r for r in g.iter(NS + "rect")]
            bx0 = min(float(r.get("x")) for r in rects)
            bx1 = max(float(r.get("x")) + float(r.get("width")) for r in rects)
            by0 = min(float(r.get("y")) for r in rects)
            by1 = max(float(r.get("y")) + float(r.get("height")) for r in rects)
            on_edge = (bx0 - 1.5 <= x1 <= bx1 + 1.5 and by0 - 1.5 <= y1 <= by1 + 1.5 and
                       min(abs(x1 - bx0), abs(x1 - bx1), abs(y1 - by0), abs(y1 - by1)) <= 1.5)
            if d0 > 4.5 or not on_edge or math.hypot(x1 - x0, y1 - y0) > 60:
                self.fail(f, f"bullet {lid} leader runs from {d0:.1f} px off its track to {'the' if on_edge else 'off the'} bullet")
        else:
            d = min(_dist_poly((cx, cy), pl) for pl in polys) if polys else 1e9
            if d > 6.5:
                self.fail(f, f"bullet {lid} sits {d:.1f} px from its own track on {on}")

    def check_lit(self, f, root, view):
        """A lit view: the lit loops at 6 px Charcoal (red at the reform's targets), every other loop at 2 px Stone,
        stations on a lit loop filled Charcoal with their IDs in Newsprint."""
        lit = set(root.get("data-lit").split())
        rid = root.get("data-reform")
        targets = set(REF[rid]["targets"]) if rid else set()
        lw, dw = set(), set()
        for g in root.iter(NS + "g"):
            if g.get("class") != "step":
                continue
            p = next((x for x in g.iter(NS + "path") if x.get("data-texture")), None)
            w = float(p.get("data-weight"))
            col = (p.get("stroke") or "").upper()
            self.c["lit_steps_checked"] += 1
            if g.get("data-loop") in lit:
                lw.add(w)
                want = RED if g.get("data-link") in targets else CHARCOAL
                if col != want:
                    self.fail(f, f"lit step {g.get('data-link')} on {g.get('data-loop')} drawn {col}, needs {want}")
            else:
                dw.add(w)
                if col != STONE:
                    self.fail(f, f"unlit step {g.get('data-link')} on {g.get('data-loop')} drawn {col}, needs Stone")
        if view in ("c-working", "c-reform"):
            if lw != {6.0} or dw != {2.0}:
                self.fail(f, f"lit lines at {sorted(lw)} px and the rest at {sorted(dw)} px; the lit view needs 6 and 2")
        elif len(lw) != 1 or len(dw) != 1 or abs(min(lw) / min(dw) - 3) > 0.01:
            self.fail(f, f"locator lit lines at {sorted(lw)} px against {sorted(dw)} px; the lit line is three times the rest")
        for g in root.iter(NS + "g"):
            if g.get("class") != "var":
                continue
            self.c["lit_stations_checked"] += 1
            on = bool(lit & set(g.get("data-loops", "").split()))
            shape = next((x for x in g if x.tag in (NS + "circle", NS + "rect")), None)
            fill = (shape.get("fill") or "").upper()
            ids = [x for x in g.iter(NS + "text") if VM.text_of(x) == g.get("data-node")]
            if on and (fill != CHARCOAL or any((x.get("fill") or "").upper() != NEWSPRINT for x in ids)):
                self.fail(f, f"{g.get('data-node')} on a lit loop drawn fill {fill}, IDs {[x.get('fill') for x in ids]}; needs Charcoal with a Newsprint ID")
            if not on and fill == CHARCOAL:
                self.fail(f, f"{g.get('data-node')} is on no lit loop but is filled Charcoal")

    def check_fields(self, f, root, cell, ox, oy):
        polys = {}
        rr = 0
        for p in root.iter(NS + "path"):
            if p.get("class") != "field":
                continue
            pts = [tuple(float(v) for v in xy.split()) for xy in re.findall(r"[-\d.]+ [-\d.]+", p.get("d"))]
            polys.setdefault(p.get("data-district"), []).append(pts)
            rr = float(p.get("stroke-width")) / 2
        for v, t in self.table.items():
            self.c["fields_checked"] += 1
            x, y = ox + int(t["col"]) * cell, oy + int(t["row"]) * cell
            ok = any(_inside_or_near((x, y), poly, rr) for poly in polys.get(t["district"], []))
            if not ok:
                self.fail(f, f"{v} sits outside the field of district {t['district']}")

    # ------------------------------------------------------------ miniatures, sketched tiles, cards
    def check_mini(self, f, root):
        lid = root.get("data-loop")
        lp = LOOPS[lid]
        steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
        drawn = [g.get("data-link") for g in steps]
        if drawn != lp["links"]:
            self.fail(f, f"{lid} draws steps {drawn}, V7 {lp['links']}")
        for g in steps:
            self.c["steps_checked"] += 1
            self.check_step_attrs(f, g)
        vars_ = {g.get("data-node"): g for g in root.iter(NS + "g") if g.get("class") == "var"}
        if set(vars_) != {c for c, _ in lp["chain"]}:
            self.fail(f, f"{lid} stations {sorted(vars_)}, V7 chain {[c for c, _ in lp['chain']]}")
        for v, g in vars_.items():
            self.c["stations_checked"] += 1
            if g.get("data-label") != LABEL.get(v):
                self.fail(f, f"{lid} {v} label {g.get('data-label')!r}, V7 {LABEL.get(v)!r}")
        names = {t.get("data-name-for"): VM.text_of(t) for t in root.iter(NS + "text") if t.get("data-name-for")}
        if root.get("data-view") == "c-mini":
            for v in vars_:
                if v not in names or not LABEL[v].startswith(names[v]):
                    self.fail(f, f"{lid} miniature names {v} {names.get(v)!r}, V7 {LABEL[v]!r}")
        for p in root.iter(NS + "path"):
            gh = p.get("data-ghost")
            if not gh:
                continue
            self.c["ghosts_checked"] += 1
            at = p.get("data-at")
            for k in gh.split():
                if k not in L or at not in (L[k]["from"], L[k]["to"]) or k in lp["links"]:
                    self.fail(f, f"{lid} ghost {k} at {at} is not another loop connection at that station")
        if self.red_elements(root) - {None}:
            self.fail(f, f"{lid} miniature carries red")
        if [g for g in root.iter(NS + "g") if g.get("class") == "sign"]:
            self.fail(f, f"{lid} miniature carries signs; the notation budget gives signs to Direction A only")

    def check_sketched(self, f, root):
        lid = root.get("data-loop")
        lp = LOOPS[lid]
        steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
        if len(steps) != len(lp["chain"]):
            self.fail(f, f"{lid} draws {len(steps)} sketched steps, V7 chain has {len(lp['chain'])}")
        labels = [lab for lab, _ in lp["chain_labels"]]
        for i, g in enumerate(steps):
            self.c["sketched_steps_checked"] += 1
            if g.get("data-sign") != lp["chain"][i][1]:
                self.fail(f, f"{lid} sketched step {i + 1} sign {g.get('data-sign')}, V7 {lp['chain'][i][1]}")
            if g.get("data-from-label") != labels[i] or g.get("data-to-label") != labels[(i + 1) % len(labels)]:
                self.fail(f, f"{lid} sketched step {i + 1} labels differ from V7 chain_labels")
            if not any(p.get("data-texture") == "hollow" for p in g.iter(NS + "path")):
                self.fail(f, f"{lid} sketched step {i + 1} is not drawn in the hollow line")

    def check_card(self, f, root):
        lid = root.get("data-loop")
        lp = LOOPS[lid]
        rid = root.get("data-reform")
        steps = [g for g in root.iter(NS + "g") if g.get("class") == "step"]
        drawn = [g.get("data-link") for g in steps]
        if drawn != lp["links"]:
            self.fail(f, f"{lid} card draws steps {drawn}, V7 {lp['links']}")
        labelled = root.get("data-view") == "c-card"
        for g in steps:
            self.c["steps_checked"] += 1
            l = self.check_step_attrs(f, g)
            if not l:
                continue
            t = [x for x in g.iter(NS + "g") if x.get("class") == "ticks"]
            self.c["ticks_checked"] += 1
            n_t = int(t[0].get("data-ticks")) if t else 0
            n_l = len(list(t[0].iter(NS + "line"))) if t else 0
            if n_t != VM.TICKS[l["delay"]] or n_l != VM.TICKS[l["delay"]]:
                self.fail(f, f"{g.get('data-link')} draws {n_l} delay ticks marked {n_t}, V7 delay {l['delay']} needs {VM.TICKS[l['delay']]}")
            sg = [x for x in g.iter(NS + "g") if x.get("class") == "sign"]
            if len(sg) != 1:
                self.fail(f, f"{g.get('data-link')} has {len(sg)} sign tags")
            else:
                self.check_sign(f, sg[0], l, g.get("data-link"))
        if labelled:
            for sl in root.iter(NS + "g"):
                if sl.get("class") != "steplabel":
                    continue
                k = sl.get("data-for")
                self.c["records_checked"] += 1
                rec = [r for r in sl.iter(NS + "rect") if r.get("data-record")]
                if bool(rec) != (L[k]["evidence"] == "documented"):
                    self.fail(f, f"{k} record square {'present' if rec else 'absent'} with grade {L[k]['evidence']}")
                if k not in VM.text_of(sl) or L[k]["name"].split()[0] not in VM.text_of(sl):
                    self.fail(f, f"{k} step label does not carry its ID and V7 name")
            want = VM.expected_weakest(lid)
            drawn_w = {e.get("data-weakest") for e in root.iter() if e.get("data-weakest")}
            self.c["weakest_checked"] += 1
            if drawn_w != want:
                self.fail(f, f"{lid} weakest marks {sorted(drawn_w)}, V7 ranks give {sorted(want)}")
        vars_ = {g.get("data-node") for g in root.iter(NS + "g") if g.get("class") == "var"}
        if vars_ != {c for c, _ in lp["chain"]}:
            self.fail(f, f"{lid} card stations {sorted(vars_)}")
        reds = self.red_elements(root) - {None}
        self.c["red_marks_checked"] += len(reds)
        want_red = (set(REF[rid]["targets"]) & (set(lp["links"]) | {c for c, _ in lp["chain"]})) if rid else set()
        if reds != want_red:
            self.fail(f, f"{lid} card red at {sorted(reds)}, {rid} targets drawn here {sorted(want_red)}")

    # ------------------------------------------------------------ pages
    def check_pages(self, svgs):
        pages = {p.name: p.read_text(encoding="utf-8") for p in self.assets.glob("20261028_*.html")}
        for name, raw in svgs.items():
            body = raw.split("?>", 1)[1].strip() if raw.startswith("<?xml") else raw
            if not any(body in html for html in pages.values()):
                self.fail(name, "drawing is not inlined, unchanged, on any page")
        for pname, phone, cols in (("20261028_Loop-Lines-Catalog.html", False, 4), ("20261028_Loop-Lines-Catalog-Phone.html", True, 2)):
            html = pages.get(pname, "")
            self.c["pages_checked"] += 1
            cards = re.findall(r'<article class="card[^"]*" data-loop="([^"]+)" data-span="(\d)"', html)
            ids = [c for c, _ in cards]
            if sorted(ids) != sorted(NUMBERED + SKETCHED) or len(ids) != len(set(ids)):
                self.fail(pname, f"catalog cards {ids}, V7 loops {sorted(NUMBERED + SKETCHED)}")
            used = 0
            last = -1
            for lid, sp in cards:
                self.c["catalog_cards_checked"] += 1
                sp = int(sp)
                if lid in NUMBERED:
                    areas = {area(c) for c, _ in LOOPS[lid]["chain"]}
                    want = 2 if len(areas) >= 3 else 1
                    if sp != want:
                        self.fail(pname, f"{lid} card spans {sp}, it crosses {len(areas)} areas so it spans {want}")
                    idx = max("ABCDE".index(a) for a in areas)
                    if idx < last:
                        self.fail(pname, f"{lid} breaks district order")
                    last = max(last, idx)
                elif last < 5:
                    last = 5
                used += sp
                if used > cols:
                    self.fail(pname, f"{lid} overhangs a row")
                    used = sp
                if used == cols:
                    used = 0
            if used:
                self.fail(pname, f"the last row holds {used} of {cols} columns")

    def run(self):
        svgs = {}
        for path in sorted(self.assets.glob("20261028_*.svg")):
            f = path.name
            raw = path.read_text(encoding="utf-8")
            svgs[f] = raw
            root = ET.fromstring(raw)
            self.c["svg_files"] += 1
            view = root.get("data-view")
            if view in FULL_VIEWS + ("c-band", "c-band-phone", "c-locator"):
                self.check_network(f, root, view)
            elif view in ("c-mini", "c-mini-phone"):
                self.check_mini(f, root)
            elif view == "c-sketched":
                self.check_sketched(f, root)
            elif view in ("c-card", "c-card-phone"):
                self.check_card(f, root)
            else:
                self.fail(f, f"unknown view {view}")
        minis = {ET.fromstring(svgs[k]).get("data-loop") for k in svgs if "-Mini-R" in k or "-Mini-B" in k}
        if minis != set(NUMBERED):
            self.fail("catalog", f"miniatures drawn for {sorted(minis)}, V7 numbered {sorted(NUMBERED)}")
        self.check_pages(svgs)
        return self.problems


def _path_points(d):
    """The vertices of a step path (M, L and arc end points), as a polyline."""
    pts = []
    for cmd, args in re.findall(r"([MLA])([^MLA]*)", d):
        nums = [float(x) for x in re.findall(r"-?[\d.]+", args)]
        if cmd in "ML":
            pts += [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
        else:
            pts.append((nums[5], nums[6]))
    return pts


def _dist_poly(pt, pts):
    best = 1e9
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = max(0, min(1, ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / L2)) if L2 else 0
        best = min(best, math.hypot(pt[0] - a[0] - t * dx, pt[1] - a[1] - t * dy))
    return best


def _inside_or_near(pt, poly, tol):
    x, y = pt
    c = False
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    if c:
        return True
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = max(0, min(1, ((x - a[0]) * dx + (y - a[1]) * dy) / L2)) if L2 else 0
        if math.hypot(x - a[0] - t * dx, y - a[1] - t * dy) <= tol:
            return True
    return False


def mutation_test():
    """Copy the drawings, plant one error per check family, and confirm each is caught (eight plants)."""
    plants = [
        ("20261028_Loop-Lines-Poster.svg", 'data-link="L02"', lambda s: s.replace('data-texture="9 4" data-weight="4.0"', 'data-texture="solid" data-weight="4.0"', 1),
         "texture"),
        ("20261028_Loop-Lines-Poster.svg", 'data-for="L25"', lambda s: re.sub(r'(data-for="L25" data-sign="-"><polygon[^>]*/><text[^>]*>)−', r'\1+', s, count=1), "sign glyph"),
        ("20261028_Loop-Lines-Card-R10.svg", "ticks", lambda s: s.replace('data-ticks="1"', 'data-ticks="2"', 1), "delay ticks"),
        ("20261028_Loop-Lines-Station-Table.csv", "C3", lambda s: s.replace("C3,C,13,1", "C3,C,13,2", 1), "station position"),
        ("20261028_Loop-Lines-Reform-View-R-01.svg", "red", lambda s: s.replace('data-node="C3" data-label', 'data-node="C3" data-red="1" data-label', 1), "red mark"),
        ("20261028_Loop-Lines-Poster.svg", "bullet", lambda s: s.replace('data-on="C4-D7"', 'data-on="C1-D7"', 1), "bullet off its own track"),
        ("20261028_Loop-Lines-Poster.svg", "frame", lambda s: s.replace("5 into area A", "4 into area A", 1), "frame count in words"),
        ("20261028_Loop-Lines-Working-Map-R10-Lit.svg", "lit", lambda s: s.replace('stroke-width="6.0" data-texture="solid" data-weight="6.0"', 'stroke-width="4.0" data-texture="solid" data-weight="4.0"', 1), "lit line weight"),
    ]
    out = []
    for fname, _, fn, what in plants:
        tmp = Path(tempfile.mkdtemp())
        for p in ASSETS.glob("20261028_*"):
            if p.suffix in (".svg", ".html", ".csv"):
                shutil.copy(p, tmp / p.name)
        t = tmp / fname
        before = t.read_text(encoding="utf-8")
        after = fn(before)
        t.write_text(after, encoding="utf-8")
        if fname.endswith(".svg"):
            # keep the page copies equal so only the planted error differs
            for h in tmp.glob("*.html"):
                hs = h.read_text(encoding="utf-8")
                b0 = before.split("?>", 1)[1].strip()
                if b0 in hs:
                    h.write_text(hs.replace(b0, after.split("?>", 1)[1].strip()), encoding="utf-8")
        probs = Run(tmp).run()
        out.append({"planted": what, "file": fname, "changed": before != after, "caught": len(probs), "first": probs[:2]})
        shutil.rmtree(tmp)
    return out


def main():
    if "--mutate" in sys.argv:
        res = mutation_test()
        for r in res:
            print(f"planted {r['planted']} in {r['file']}: changed={r['changed']}, caught {r['caught']}: {r['first'][:1]}")
        prev = json.loads(OUT.read_text()) if OUT.exists() else {}
        prev["mutation_test"] = res
        OUT.write_text(json.dumps(prev, indent=1, ensure_ascii=False), encoding="utf-8")
        return 0 if all(r["changed"] and r["caught"] for r in res) else 1
    run = Run(ASSETS)
    problems = run.run()
    c = run.c
    result = {
        "run_note": "Checked against work/extract/atlas-v7-data.json through verify_maps_data.py, independently of the Direction C drawing modules",
        "counts": c, "numbered_loops": NUMBERED, "sketched_loops": SKETCHED, "loop_variables": LOOP_VARS, "loop_connections": len(LOOP_LINKS),
        "mismatches": len(problems), "problems": problems[:200],
        "summary": [
            f"Data check against V7: {len(problems)} mismatches across {c['svg_files']} drawings.",
            f"All {len(NUMBERED)} numbered loops drawn on every network view and as miniatures; sketched loops listed: {', '.join(SKETCHED)}.",
            f"Checked {c['steps_checked']} drawn steps for link, from, to, sign, type, delay, grade and loop; {c['textures_checked']} line textures; "
            f"{c['signs_checked']} sign glyphs and their direction; {c['ticks_checked']} delay-tick sets; {c['records_checked']} record squares.",
            f"Checked {c['stations_checked']} stations and {c['positions_checked']} station positions against the 25-row station table, "
            f"{c['fields_checked']} stations inside their district field, {c['bullets_checked']} line bullets ({c['bullet_tracks_checked']} on a stretch only their loop rides) and {c['entries_checked']} frame counts in words.",
            f"Checked {c['lit_steps_checked']} steps and {c['lit_stations_checked']} stations on the lit views: lit loops at 6 px Charcoal, the rest at 2 px Stone, lit stations filled Charcoal with Newsprint IDs.",
            f"Checked {c['red_marks_checked']} red marks and {c['weakest_checked']} weakest-step markings; red sits only at the targets of the reform each view names, never on Prussian.",
            f"Checked {c['catalog_cards_checked']} catalog cards for district order, width by reach and full rows, and that every drawing file sits unchanged on a page.",
        ],
    }
    if OUT.exists():
        prev = json.loads(OUT.read_text())
        if "mutation_test" in prev:
            result["mutation_test"] = prev["mutation_test"]
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(result["summary"]))
    for p in problems[:60]:
        print("  ", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
