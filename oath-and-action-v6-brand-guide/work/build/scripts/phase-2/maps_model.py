#!/usr/bin/env python3
"""Loop and system model for the Systems Map Directions Board, read from Atlas V7 only.

Run:  python3 -I work/build/scripts/phase-2/maps_model.py
Reads  work/extract/atlas-v7-data.json (never written)
Writes work/boards/phase-2/maps/20261028_Maps-Model-Data.json (every V7 value the drawings use)

Every drawing script imports this module by file path (Python runs with -I, see D1-05) and draws only
from the structures it returns, so no ID, sign, grade, delay or target is copied by hand.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
V7_PATH = ROOT / "work/extract/atlas-v7-data.json"
OUT = ROOT / "work/boards/phase-2/maps/20261028_Maps-Model-Data.json"

# V7 renderer rank (script.js GRADES[].n): documented 4, well supported 3, plausible 2, contested 2, hypothesis 1
GRADE_RANK = {"documented": 4, "well-supported": 3, "plausible": 2, "plausible_contested": 2, "contested": 2,
              "hypothesis": 1}
GRADE_WORD = {"documented": "Documented", "well-supported": "Well supported", "plausible": "Plausible",
              "plausible_contested": "Contested", "contested": "Contested", "hypothesis": "Hypothesis"}
# Mark 2 glosses, from the Phase 1 Systems Marks Board (approved at Gate 1 as M2)
GRADE_GLOSS = {"documented": "on the public record", "well-supported": "strong studies agree on the direction",
               "plausible": "a coherent mechanism with some evidence", "plausible_contested": "credible studies disagree",
               "contested": "credible studies disagree", "hypothesis": "proposed, not yet supported"}
DELAY_WORD = {"S": "under 2 years", "M": "2 to 10 years", "L": "over 10 years"}
DIRECTION_WORD = {"running_up": "running up", "running_down": "running down", "running": "running",
                  "disabled": "switched off", "unknown": "direction unknown", "design_target": "a design target",
                  "disabled in concentrated sectors": "switched off in concentrated sectors"}
KIND_WORD = {"R": ("Reinforcing", "feeds itself"), "B": ("Balancing", "pushes back")}
AREA_ORDER = ["A", "B", "C", "D", "E", "X", "EC", "TC"]
AREA_TITLE_SHORT = {"EC": "Economy layer", "TC": "Technology layer"}


def load_v7():
    return json.loads(V7_PATH.read_text(encoding="utf-8"))


def area_of(node):
    return node["cluster"]


def system_order(v7):
    """The 51 variables in V7's layer and region order: core A to E and X, then economy, then technology."""
    order = []
    for layer in ("core", "economy", "technology"):
        for reg in v7["layers"][layer]["regions"]:
            order.extend(reg["nodes"])
    # A6, C5, D7 sit in the regions' lists already; keep any node V7 lists outside a region at the end of its area
    missing = [k for k in v7["nodes"] if k not in order]
    return order + missing


def areas(v7):
    out = []
    for layer in ("core", "economy", "technology"):
        for reg in v7["layers"][layer]["regions"]:
            out.append({"id": reg["id"], "layer": layer, "title": reg["title"], "text": reg["text"], "nodes": list(reg["nodes"])})
    return out


def node_label(v7, nid, loops_index):
    """Short label: V7's own chain_labels where a loop names the variable, otherwise V7's title."""
    return loops_index.get(nid) or v7["nodes"][nid]["title"]


def chain_label_index(v7):
    idx = {}
    for lp in v7["loops"].values():
        for (code, _), (lab, _) in zip(lp["chain"], lp["chain_labels"]):
            if code in v7["nodes"] and code not in idx:
                idx[code] = lab
    return idx


def loop_group(v7, lp):
    """Catalog group: the area holding most of the loop's numbered variables; ties go to the area first in V7's order.
    Loops without a complete numbered chain form their own group."""
    if not lp["closure"].startswith("closed"):
        return "SK"
    counts = {}
    for code, _ in lp["chain"]:
        a = v7["nodes"][code]["cluster"]
        counts[a] = counts.get(a, 0) + 1
    best = max(counts.values())
    for a in AREA_ORDER:
        if counts.get(a) == best:
            return a


def build_loop(v7, lid, labels):
    lp = v7["loops"][lid]
    N, L, R = v7["nodes"], v7["links"], v7["reforms"]
    conceptual = not lp["closure"].startswith("closed")
    stations = []
    for (code, sign), (lab, _) in zip(lp["chain"], lp["chain_labels"]):
        is_var = code in N
        stations.append({"code": code if is_var else None, "label": lab, "is_variable": is_var,
                         "title": N[code]["title"] if is_var else None,
                         "increase_means": N[code]["increase_means"] if is_var else None,
                         "area": N[code]["cluster"] if is_var else None, "out_sign": sign})
    n = len(stations)
    steps = []
    if conceptual:
        for i in range(n):
            a, b = stations[i], stations[(i + 1) % n]
            steps.append({"id": None, "conceptual": True, "from": a["code"], "to": b["code"], "from_label": a["label"],
                          "to_label": b["label"], "polarity": a["out_sign"], "type": None, "delay": None, "evidence": None,
                          "rank": None, "name": None, "index": i + 1, "closing": i == n - 1})
    else:
        for i, k in enumerate(lp["links"]):
            l = L[k]
            steps.append({"id": k, "conceptual": False, "from": l["from"], "to": l["to"], "from_label": labels.get(l["from"]),
                          "to_label": labels.get(l["to"]), "polarity": l["polarity"], "type": l["type"], "delay": l["delay"],
                          "evidence": l["evidence"], "rank": GRADE_RANK[l["evidence"]], "name": l["name"],
                          "index": i + 1, "closing": i == n - 1})
    # weakest step: lowest V7 rank; when every step shares the lowest rank, no single step is weakest
    weakest = []
    if not conceptual:
        lo = min(s["rank"] for s in steps)
        weakest = [s["id"] for s in steps if s["rank"] == lo]
        if len(weakest) == len(steps):
            weakest = []
    # reform targets inside this loop: reforms V7 lists on the loop, minus rejected ones, at targets the loop draws
    elements = {s["id"] for s in steps if s["id"]} | {s["code"] for s in stations if s["code"]}
    targets = {}
    for rid in lp["reforms"]:
        r = R[rid]
        if r["rejected"]:
            continue
        for t in r["targets"]:
            if t in elements:
                targets.setdefault(t, []).append(rid)
    rejected = [rid for rid in lp["reforms"] if R[rid]["rejected"]]
    kind, gloss = KIND_WORD[lp["type"]]
    return {
        "id": lid, "type": lp["type"], "kind_word": kind, "kind_gloss": gloss, "title": lp["title"],
        "closure": lp["closure"], "closure_short": lp["closure"].split(":")[0], "conceptual": conceptual,
        "hypothesized": lp["closure"].startswith("closed with a hypothesized"),
        "evidence_text": lp["evidence"], "evidence_summary": lp["evidence_summary"], "how_to_read": lp["how_to_read"],
        "summary": lp["summary"], "qualification": lp["qualification"],
        "delay": lp["delay"], "delay_word": DELAY_WORD[lp["delay"]],
        "direction": lp["direction"], "direction_word": DIRECTION_WORD.get(lp["direction"], lp["direction"].replace("_", " ")),
        "reference_mode": lp["reference_mode"],
        "stations": stations, "steps": steps, "n": n, "weakest": weakest,
        "reforms": [r for r in lp["reforms"] if not R[r]["rejected"]], "rejected_reforms": rejected,
        "targets": targets, "group": loop_group(v7, lp),
    }


def build_reform(v7, rid):
    r = v7["reforms"][rid]
    return {"id": rid, "title": r["title"], "summary": r["summary"], "targets": list(r["targets"]), "loops": list(r["loops"]),
            "band": r["band"], "effects": dict(r["effects"]), "effects_confidence": r["effects_confidence"],
            "problem_grade": r["problem_evidence"]["grade"], "remedy_grade": r["remedy_evidence"]["grade"],
            "remedy_text": r["remedy_evidence"]["text"], "what_it_changes": r["what_it_changes"],
            "routes": [{"route": x["route"], "who": x["who"], "feasibility": x["feasibility"], "checked": x["checked"]} for x in r["routes"]],
            "rejected": r["rejected"], "status_checked": r["status"]["checked"] if r.get("status") else None}


def build_model():
    v7 = load_v7()
    labels = chain_label_index(v7)
    order = system_order(v7)
    loops = {lid: build_loop(v7, lid, labels) for lid in v7["loops"]}
    links = {}
    for k, l in v7["links"].items():
        links[k] = {"id": k, "from": l["from"], "to": l["to"], "polarity": l["polarity"], "type": l["type"], "delay": l["delay"],
                    "evidence": l["evidence"], "layer": l["layer"], "loops": list(l["loops"]), "name": l["name"],
                    "rank": GRADE_RANK[l["evidence"]]}
    nodes = {}
    for k in order:
        n = v7["nodes"][k]
        nodes[k] = {"id": k, "layer": n["layer"], "type": n["type"], "area": n["cluster"], "title": n["title"],
                    "label": node_label(v7, k, labels), "short": labels.get(k), "domain": n["domain"],
                    "increase_means": n["increase_means"],
                    "loops": sorted({lid for lid, lp in loops.items() for s in lp["stations"] if s["code"] == k})}
    groups = [("A", "Economic structure"), ("B", "Political inputs"), ("C", "Electoral competition"),
              ("D", "Governing institutions"), ("SK", "Sketched loops, without a complete numbered chain")]
    region_titles = {a["id"]: a["title"] for a in areas(v7)}
    model = {
        "generated": {"source": str(V7_PATH.relative_to(ROOT)), "snapshot": v7["meta"]["snapshot"],
                      "title": v7["meta"]["title"], "subtitle": v7["meta"]["subtitle"], "counts": v7["meta"]["counts"]},
        "order": order, "areas": areas(v7), "region_titles": region_titles, "nodes": nodes, "links": links,
        "loops": loops, "loop_order": list(v7["loops"].keys()),
        "groups": [{"id": g, "title": t, "loops": [lid for lid in v7["loops"] if loops[lid]["group"] == g]} for g, t in groups],
        "reforms": {rid: build_reform(v7, rid) for rid in v7["reforms"]},
        "glossary": {g["term"]: g["definition"] for g in v7["glossary"]},
    }
    return model


if __name__ == "__main__":
    m = build_model()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    steps = {lid: lp["n"] for lid, lp in m["loops"].items()}
    by_n = {k: sorted(l for l, v in steps.items() if v == k) for k in (2, 3, 4)}
    print("loops", len(m["loops"]), {k: len(v) for k, v in by_n.items()}, "nodes", len(m["nodes"]), "links", len(m["links"]),
          "reforms", len(m["reforms"]))
    for g in m["groups"]:
        print(g["id"], g["loops"])
    for lid, lp in m["loops"].items():
        print(lid, lp["n"], "weakest", lp["weakest"], "targets", lp["targets"])
