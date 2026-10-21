#!/usr/bin/env python3
"""Query Atlas V7 for every value used on the Systems Marks Board, in the V7.1 issue list and in the notes.

Run from anywhere:  python3 -I work/build/scripts/phase-1/systems_marks_data.py

Reads (read-only):
  work/extract/atlas-v7-data.json          the V7 model, extracted in Phase 0
  work/extract/atlas-v7/script.js          the V7 renderer (grade table, legend dashes, type labels)
  work/extract/atlas-v7/styles.css         the V7 renderer styles (edge dashes)
  work/extract/v5-polished/chapters/15-standards.html   V5 Standards rule numbers
Writes:
  work/boards/phase-1/systems/20261021_Systems-Marks-Data.json

Nothing in the V7 model is changed. Every ID, sign, delay, grade, effect, route and date used later is read here.
"""
import html
import json
import re
from collections import Counter, OrderedDict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
V7 = ROOT / "work/extract/atlas-v7-data.json"
JS = ROOT / "work/extract/atlas-v7/script.js"
CSS = ROOT / "work/extract/atlas-v7/styles.css"
STD = ROOT / "work/extract/v5-polished/chapters/15-standards.html"
OUT = ROOT / "work/boards/phase-1/systems/20261021_Systems-Marks-Data.json"

d = json.loads(V7.read_text(encoding="utf-8"))
js = JS.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
N, L, LP, R, I, C = d["nodes"], d["links"], d["loops"], d["reforms"], d["issues"], d["claims"]
SNAP = d["meta"]["snapshot"]

# ------------------------------------------------------------------ colour and contrast (WCAG 2.x formula)
PALETTE = OrderedDict([
    ("Newsprint", "#DCD9D2"), ("White", "#FFFFFF"), ("Charcoal", "#121212"), ("Prussian", "#1F2D5A"),
    ("Pillar Red", "#E63946"), ("Stone", "#5D636D"), ("Verdigris", "#4A7C74"),
    ("Board muted", "#45494F"),
])
SURFACES = ["Newsprint", "White", "Charcoal", "Prussian"]
INK = {"Newsprint": "Charcoal", "White": "Charcoal", "Charcoal": "Newsprint", "Prussian": "Newsprint"}


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexv):
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def gray(hexv):
    """CSS filter grayscale(1): luma weights applied to gamma-encoded sRGB, as browsers implement it."""
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    y = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return "#%02X%02X%02X" % (y, y, y)


contrast_table = {}
for fg in PALETTE:
    contrast_table[fg] = {s: contrast(PALETTE[fg], PALETTE[s]) for s in SURFACES}

chip_contrast = {}
for s in SURFACES:
    ink = PALETTE[INK[s]]
    cell = PALETTE[s]
    chip_contrast[s] = {
        "ink": INK[s],
        "code_text_on_surface": contrast(ink, cell),
        "kind_text_on_ink_fill": contrast(cell, ink),
        "grayscale_code": contrast(gray(ink), gray(cell)),
        "grayscale_kind": contrast(gray(cell), gray(ink)),
        "red_ring_on_surface": contrast(PALETTE["Pillar Red"], cell),
    }
muted_on_light = {s: contrast(PALETTE["Board muted"], PALETTE[s]) for s in ("Newsprint", "White")}

# ------------------------------------------------------------------ renderer facts
grade_table = {}
for m in re.finditer(r"'([a-z -]+)':\s*\{\s*label:\s*'([^']+)',\s*n:\s*(\d),\s*cls:\s*'([^']*)',\s*text:\s*'((?:[^'\\]|\\.)*)'", js):
    grade_table[m.group(1)] = {"label": m.group(2), "meter": int(m.group(3)), "class": m.group(4),
                               "text": m.group(5).replace("\\'", "'")}
legend = {}
lm = re.search(r"function legendHTML\(concept\)\s*\{(.*?)\n\}", js, re.S)
if lm:
    body = lm.group(1)
    for dash, label in re.findall(r"line\('', '#[0-9a-f]+', '([0-9 ]+)'\) \+ '([^'<]+)'", body):
        legend[label.strip()] = dash
    legend["documented or well supported"] = legend.get("documented or well supported", "solid")
    cm = re.search(r"line\('', '(#[0-9a-f]+)', '([0-9 ]+)'\) \+ '<span>conceptual step", body)
    if cm:
        legend["conceptual step"] = cm.group(2) + " in " + cm.group(1)
edge_css = dict(re.findall(r"\.edge\.(u-[a-z]+)\{[^}]*stroke-dasharray:([0-9 ]+)", css))
edge_width = re.search(r"\.dia-view svg \.edge\{[^}]*stroke-width:([0-9.]+)", css).group(1)
kind_label = dict(re.findall(r"(\w+): '([^']+)'", re.search(r"var KIND_LABEL = \{(.*?)\};", js).group(1)))
ambiguous_rule = re.search(r"function ambiguousCode\(kind, id\) \{(.*?)\}", js).group(1).strip()
pill_rx = re.search(r'class="pill[^;]*?rx="(\d+)"', js)
pill_rx = pill_rx.group(1) if pill_rx else None
outside_region = [r["title"] for r in d["layers"]["core"]["regions"] if r["id"] == "X"]

# ------------------------------------------------------------------ glossary and methods quotes
G = {g["term"]: g["definition"] for g in d["glossary"]}
methods = d["methods"]


def sentence_with(text, needle):
    for s in re.split(r"(?<=[.;])\s+", text):
        if needle in s:
            return s.strip()
    return None


quotes = {
    "outside_driver_glossary": G.get("Outside driver"),
    "confidence_label_glossary": G.get("Confidence label"),
    "connection_glossary": G.get("Connection"),
    "issue_record_glossary": G.get("Issue record"),
    "well_supported_glossary": G.get("Well-supported"),
    "documented_glossary": G.get("Documented"),
    "hypothesis_glossary": G.get("Hypothesis"),
    "authority_glossary": G.get("Authority connection"),
    "delay_glossary": G.get("Delay"),
    "loop_closure_glossary": G.get("Loop closure"),
    "positive_sign_glossary": G.get("Positive sign (+)"),
    "repair_log_glossary": G.get("Repair log"),
    "methods_documented": sentence_with(methods["how_claims_are_assessed"], "Documented means"),
    "methods_well_supported": sentence_with(methods["how_claims_are_assessed"], "Well supported means"),
    "methods_plausible": sentence_with(methods["how_claims_are_assessed"], "Plausible means"),
    "methods_mixed": sentence_with(methods["how_claims_are_assessed"], "Mixed means"),
    "methods_contested": sentence_with(methods["how_claims_are_assessed"], "Contested means"),
    "methods_hypothesis": sentence_with(methods["how_claims_are_assessed"], "Hypothesis marks"),
    "methods_identifiers": sentence_with(methods["model_conventions"], "Identifiers are exact"),
    "methods_authority": sentence_with(methods["model_conventions"], "they carry no sign"),
    "methods_sign": sentence_with(methods["model_conventions"], "a plus sign can mark a harmful effect"),
    "methods_no_score": sentence_with(methods["what_this_is"], "add reform effects into a single score"),
    "outcomes_why_not_one_number": d["outcomes"]["why_not_one_number"],
    "effect_codes_note": d["outcomes"]["effect_codes_note"],
    "repair_coding_last": sentence_with(d["repairLog"]["coding_note"], "carries no judgment"),
    "delivery_grade_note": sentence_with(d["deliveryLog"]["intro"], "The evidence grade on each entry"),
}

# ------------------------------------------------------------------ grade vocabulary by record type


def lead_grade(t):
    m = re.match(r"^(Documented|Well[- ]supported|Plausible(?: but contested)?|Contested|Hypothesis|Mixed|Not yet tested|Retired)\b", t or "")
    return m.group(1) if m else None


grades = OrderedDict()
grades["links.evidence"] = Counter(l["evidence"] for l in L.values())
grades["links.contested (flag)"] = Counter("true" if l["contested"] else "false" for l in L.values())
grades["issues.grade"] = Counter(v["grade"] for v in I.values())
grades["issues.remedy_note (first word)"] = Counter(lead_grade(v.get("remedy_note")) or "none" for v in I.values())
grades["claims.confidence"] = Counter(c["confidence"] for c in C.values())
grades["reforms.problem_evidence.grade"] = Counter(r["problem_evidence"]["grade"] for r in R.values())
grades["reforms.remedy_evidence.grade"] = Counter(r["remedy_evidence"]["grade"] for r in R.values())
grades["deliveryLog.rows.evidence_grade"] = Counter(r["evidence_grade"] for r in d["deliveryLog"]["rows"])
grades["loops.evidence (first grade word)"] = Counter(
    (re.match(r"^(documented|well-supported|plausible_contested|plausible|hypothesis)", l["evidence"]) or [None])[0] or "free text"
    for l in LP.values())
grades["repairLog.rows.direction"] = Counter(r["direction"] for r in d["repairLog"]["rows"])
grades["repairLog.rows.verified"] = Counter(str(r["verified"]).lower() for r in d["repairLog"]["rows"])
grades["issues.jurisdiction = mixed"] = Counter("mixed" if v["jurisdiction"] == "mixed" else "other" for v in I.values())
grades["reforms.effects_confidence"] = Counter(
    "plain level" if r["effects_confidence"] in ("high", "medium", "low") else "free text with scopes" for r in R.values())
contested_links = sorted(k for k, l in L.items() if l["contested"])
pc_links = sorted(k for k, l in L.items() if l["evidence"] == "plausible_contested")
mixed_remedy = [k for k, v in I.items() if lead_grade(v.get("remedy_note")) == "Mixed"]
retired_issue = [k for k, v in I.items() if v.get("retired")]
remedy_contested = [(k, r["remedy_evidence"]["grade"]) for k, r in R.items() if r["remedy_evidence"]["grade"] in ("contested", "plausible_contested")]
problem_contested = [(k, r["problem_evidence"]["grade"]) for k, r in R.items() if r["problem_evidence"]["grade"] in ("contested", "plausible_contested")]
text_grade_mentions = Counter()
for v in I.values():
    g = lead_grade(v.get("remedy_note"))
    if g:
        text_grade_mentions[g] += 1
not_yet_tested_uses = sum(1 for v in I.values() if lead_grade(v.get("remedy_note")) == "Not yet tested")

# ------------------------------------------------------------------ examples


def link_rec(k):
    l = L[k]
    return {"id": k, "from": l["from"], "to": l["to"], "polarity": l["polarity"], "type": l["type"], "delay": l["delay"],
            "evidence": l["evidence"], "contested": l["contested"], "name": l["name"], "loops": l["loops"],
            "qualification": l.get("qualification"), "from_title": N[l["from"]]["title"], "to_title": N[l["to"]]["title"]}


def loop_rec(k):
    l = LP[k]
    out = {"id": k, "type": l["type"], "title": l["title"], "closure": l["closure"], "evidence": l["evidence"],
           "delay": l.get("delay"), "chain": l.get("chain"), "chain_labels": l.get("chain_labels"), "links": l.get("links"),
           "evidence_summary": l.get("evidence_summary"), "qualification": l.get("qualification"), "reforms": l.get("reforms"),
           "direction": l.get("direction")}
    out["link_detail"] = [link_rec(x) for x in l.get("links") or []]
    out["node_detail"] = [{"id": c[0], "title": N[c[0]]["title"], "type": N[c[0]]["type"],
                           "increase_means": N[c[0]]["increase_means"], "label": lab[0]}
                          for c, lab in zip(l.get("chain") or [], l.get("chain_labels") or []) if c[0] in N]
    return out


examples = {k: loop_rec(k) for k in ["R1", "R8", "B4", "R10", "R11", "R13", "R16", "R7", "B2", "B3", "R9"]}
shared_c3 = sorted(k for k, l in LP.items() if any(c[0] == "C3" for c in (l.get("chain") or [])))
r11_has_variable_b4 = any(c[0] == "B4" for c in LP["R11"]["chain"])

r01 = R["R-01"]
reform_r01 = {
    "id": "R-01", "title": r01["title"], "targets": r01["targets"], "loops": r01["loops"], "band": r01["band"],
    "effects": r01["effects"], "effects_confidence": r01["effects_confidence"],
    "problem_grade": r01["problem_evidence"]["grade"], "remedy_grade": r01["remedy_evidence"]["grade"],
    "routes": r01["routes"], "status_checked": r01["status"]["checked"], "rejected": r01["rejected"],
    "target_detail": [{"id": t, "kind": "connection" if t in L else "variable",
                       "title": (L[t]["name"] if t in L else N[t]["title"])} for t in r01["targets"]],
    "loop_titles": {k: LP[k]["title"] for k in r01["loops"]},
}

grade_examples = {g: sorted(k for k, l in L.items() if l["evidence"] == g)[:4] for g in
                  ["documented", "well-supported", "plausible", "plausible_contested", "hypothesis"]}
grade_example_detail = {k: link_rec(k) for k in ["L08", "L25", "L02", "L09", "T01", "L42", "L53"]}

# ------------------------------------------------------------------ identifiers and collisions
ns = OrderedDict()
ns["variable"] = list(N)
ns["connection"] = list(L)
ns["loop"] = list(LP)
ns["reform"] = list(R)
ns["issue"] = list(I)
ns["claim"] = list(C)
ns["source"] = list(d["sources"])
ns["pathway"] = [p["id"] for p in d["pathways"]]
ns["domain"] = [x["id"] for x in d["domains"]]
ns["route"] = [r["code"] for r in d["routes"]["items"]]
ns["repair"] = [r["id"] for r in d["repairLog"]["rows"]]
ns["delivery"] = [r["id"] for r in d["deliveryLog"]["rows"]]
ns["overlay"] = [o["id"] for o in d["overlays"]]
ns["check"] = [c["id"] for c in d["checks"]]
ns["rejected_link"] = [r["id"] for r in d["rejectedLinks"]]
ns["era"] = [e.get("id") for e in d["history"]["eras"] if e.get("id")]
ns["region"] = [r["id"] for lay in d["layers"].values() for r in lay["regions"]]

std = STD.read_text(encoding="utf-8")
std_text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", std, flags=re.S))))
std_rules = OrderedDict()
for m in re.finditer(r"\bR(10|[1-9]) ([A-Z][^.]{2,80}\.)", std_text):
    std_rules.setdefault("R" + m.group(1), m.group(2))
ns["v5_standards_rule"] = list(std_rules)


def norm(x):
    m = re.match(r"^([A-Za-z]+)-?0*(\d+)([a-z]?)$", x)
    return (m.group(1).upper() + m.group(2) + m.group(3)) if m else x.upper()


exact = {}
normed = {}
for kind, ids in ns.items():
    for x in ids:
        exact.setdefault(x, set()).add(kind)
        normed.setdefault(norm(x), set()).add((kind, x))
exact_collisions = sorted((x, sorted(k)) for x, k in exact.items() if len(k) > 1)
near_collisions = []
for key, members in normed.items():
    kinds = {k for k, _ in members}
    if len(kinds) > 1:
        near_collisions.append({"normalized": key, "members": sorted(members)})
near_collisions.sort(key=lambda m: m["normalized"])
# Suffix neighbours: an ID that equals another with a letter suffix removed (B1 and B1a; R4 does not exist).
suffix_neighbours = []
allids = {x: k for k, ids in ns.items() for x in ids}
for x, k in allids.items():
    m = re.match(r"^([A-Z]+\d+)([a-z])$", x)
    if m and m.group(1) in allids and allids[m.group(1)] != k:
        suffix_neighbours.append((m.group(1), allids[m.group(1)], x, k))

prefix_candidates = {}
all_prefixes = Counter(re.match(r"^[A-Za-z]+", x).group(0).upper() for ids in ns.values() for x in ids if re.match(r"^[A-Za-z]+", x))
for cand in ["STD", "ST", "G", "QA", "OA"]:
    clash = sorted(p for p in all_prefixes if p == cand)
    starts = sorted(p for p in all_prefixes if p != cand and (p.startswith(cand) or cand.startswith(p)))
    prefix_candidates[cand] = {"exact_prefix_in_v7": clash, "prefixes_that_share_letters": starts}

renderer_types_only_when = ambiguous_rule

chip_examples = OrderedDict([
    ("variable", {"code": "B4", "name": N["B4"]["title"]}),
    ("connection", {"code": "L25", "name": L["L25"]["name"]}),
    ("loop", {"code": "B4", "name": LP["B4"]["title"]}),
    ("reform", {"code": "R-01", "name": R["R-01"]["title"]}),
    ("issue", {"code": "I006", "name": I["I006"]["title"]}),
    ("claim", {"code": "CL1400", "name": C["CL1400"]["claim"]}),
    ("domain", {"code": "D02", "name": [x for x in d["domains"] if x["id"] == "D02"][0]["title"]}),
    ("route", {"code": "BI", "name": [r for r in d["routes"]["items"] if r["code"] == "BI"][0]["name"]}),
    ("standard", {"code": "Std-05", "name": std_rules.get("R5"), "v5_code": "R5"}),
])
collision_pairs = [
    {"a": ("variable", "B4", N["B4"]["title"]), "b": ("loop", "B4", LP["B4"]["title"])},
    {"a": ("loop", "R1", LP["R1"]["title"]), "b": ("reform", "R-01", R["R-01"]["title"])},
    {"a": ("variable", "D1", N["D1"]["title"]), "b": ("domain", "D01", [x for x in d["domains"] if x["id"] == "D01"][0]["title"])},
    {"a": ("variable", "X1", N["X1"]["title"]), "b": ("issue", "X01", I["X01"]["title"])},
    {"a": ("variable", "B1", N["B1"]["title"]), "b": ("loop", "B1a", LP["B1a"]["title"])},
    {"a": ("loop", "R5", LP["R5"]["title"]), "b": ("reform", "R-05", R["R-05"]["title"]),
     "c": ("standard", "Std-05", "V5 Standards rule R5: " + (std_rules.get("R5") or ""))},
]

# ------------------------------------------------------------------ effects
CODES = ["+L", "+M", "+S", "0", "-S", "-M", "?"]
effect_words = d["outcomes"]["effect_codes"]
families = {k: v["name"] for k, v in d["outcomes"]["families"].items()}
all_effects = [(rid, fam, v, r["rejected"]) for rid, r in R.items() for fam, v in r["effects"].items()]
plain = [e for e in all_effects if e[2] in CODES]
qualified = [e for e in all_effects if e[2] not in CODES]
TOK = re.compile(r"(?<![\w$])([+\-\u2212](?:S|M|L)|0|\?)(?![\w,])")


def parse_effect(v):
    """Split a V7 effect string into the codes it states. Range ends ('0 to -S', '+S to +M') become open pips."""
    clauses = [c.strip() for c in re.split(r";", v)]
    gain = cost = 0
    gain_open = cost_open = 0
    zero = uncertain = False
    for cl in clauses:
        toks = TOK.findall(cl)
        is_range = " to " in cl and len(toks) == 2
        for i, t in enumerate(toks):
            t = t.replace("\u2212", "-")
            if t == "0":
                zero = True
                continue
            if t == "?":
                uncertain = True
                continue
            size = {"S": 1, "M": 2, "L": 3}[t[1]]
            far_end = is_range and i == 1
            if t[0] == "+":
                if far_end:
                    gain_open = max(gain_open, size)
                else:
                    gain = max(gain, size)
            else:
                if far_end:
                    cost_open = max(cost_open, size)
                else:
                    cost = max(cost, size)
    qualifier = None if v in CODES else v
    return {"gain": gain, "gain_open": max(gain_open, gain) if gain_open else 0, "cost": cost,
            "cost_open": max(cost_open, cost) if cost_open else 0, "zero": zero, "uncertain": uncertain, "qualifier": qualifier}


parsed_ok = 0
for rid, fam, v, rej in all_effects:
    p = parse_effect(v)
    if p["gain"] or p["cost"] or p["gain_open"] or p["cost_open"] or p["zero"] or p["uncertain"]:
        parsed_ok += 1
costs_live = [(rid, fam, v) for rid, fam, v, rej in all_effects if not rej and (parse_effect(v)["cost"] or parse_effect(v)["cost_open"])]
effect_examples = OrderedDict()
for rid in ["R-01", "R-12", "R-07", "R-28", "R-06", "R-20", "R-29", "R-25"]:
    effect_examples[rid] = {"title": R[rid]["title"], "effects": R[rid]["effects"],
                            "parsed": {f: parse_effect(v) for f, v in R[rid]["effects"].items()},
                            "effects_confidence": R[rid]["effects_confidence"],
                            "remedy_grade": R[rid]["remedy_evidence"]["grade"]}

# ------------------------------------------------------------------ routes
route_entries = [(rid, x["route"], x["feasibility"], x["checked"], r["rejected"]) for rid, r in R.items() for x in r["routes"]]
route_checked = [e for e in route_entries if e[3]]

# ------------------------------------------------------------------ events
INSTR_FAMILY = {
    "ballot initiative": "Ballot measure", "referendum": "Ballot measure",
    "federal statute": "Statute or local law", "state statute": "Statute or local law",
    "municipal ordinance (local law)": "Statute or local law", "council funding vote": "Statute or local law",
    "court ruling": "Court ruling",
    "agency rule": "Executive or agency action", "executive action": "Executive or agency action",
    "executive order": "Executive or agency action",
}
repair_rows = []
for r in d["repairLog"]["rows"]:
    m = re.match(r"Loop (\S+):", r["loop"] or "")
    repair_rows.append({"id": r["id"], "date": r["date"], "jurisdiction": r["jurisdiction"], "direction": r["direction"],
                        "instrument": r["instrument"], "family": INSTR_FAMILY.get(r["instrument"]),
                        "loop": m.group(1) if m else None, "verified": r["verified"], "rule": r["rule"]})
unmapped_instruments = sorted({r["instrument"] for r in repair_rows if not r["family"]})


def parse_period(s, jurisdiction):
    """Delivery log period rule. Returns start, end (ISO), precision, kind and the verbatim label."""
    s0 = s.strip()
    m = re.match(r"^(\d{4})-(\d{4})$", s0)
    if m:
        return {"start": f"{m.group(1)}-01-01", "end": f"{m.group(2)}-12-31", "precision": "year", "kind": "span"}
    m = re.match(r"^(\d{4})-(\d{4}), published (\d{4})$", s0)
    if m:
        return {"start": f"{m.group(1)}-01-01", "end": f"{m.group(2)}-12-31", "precision": "year", "kind": "span",
                "extra_point": {"date": f"{m.group(3)}-01-01", "label": "published " + m.group(3)}}
    m = re.match(r"^(\d{4}-\d{2}-\d{2}) onward$", s0)
    if m:
        return {"start": m.group(1), "end": SNAP, "precision": "day", "kind": "open span"}
    m = re.match(r"^(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})$", s0)
    if m:
        return {"start": m.group(1), "end": m.group(2), "precision": "day", "kind": "span"}
    m = re.match(r"^(\d{4})-(\d{2}) to (\d{4})-(\d{2})$", s0)
    if m:
        y2, m2 = int(m.group(3)), int(m.group(4))
        last = (date(y2 + (m2 == 12), (m2 % 12) + 1, 1) - date.resolution).isoformat()
        return {"start": f"{m.group(1)}-{m.group(2)}-01", "end": last, "precision": "month", "kind": "span"}
    m = re.match(r"^FY(\d{4})$", s0)
    if m and jurisdiction.startswith("federal"):
        y = int(m.group(1))
        return {"start": f"{y - 1}-10-01", "end": f"{y}-09-30", "precision": "federal fiscal year", "kind": "span"}
    m = re.match(r"^(\d{4}) analysis$", s0)
    if m:
        return {"start": f"{m.group(1)}-01-01", "end": None, "precision": "year", "kind": "point (analysis date)"}
    return None


delivery_rows = []
for r in d["deliveryLog"]["rows"]:
    p = parse_period(r["date"], r["jurisdiction"])
    delivery_rows.append({"id": r["id"], "date": r["date"], "jurisdiction": r["jurisdiction"], "grade": r["evidence_grade"],
                          "what": r["what_was_done"], "period": p,
                          "loop": (re.match(r"Loop (\S+):", r["loop"]) or [None, None])[1] if r["loop"] else None})
unparsed_periods = [r["id"] for r in delivery_rows if not r["period"]]
v7_order_is_chronological = [r["period"]["start"] for r in delivery_rows if r["period"]] == sorted(
    r["period"]["start"] for r in delivery_rows if r["period"])

# ------------------------------------------------------------------ authority and delay
authority = [link_rec(k) for k, l in L.items() if l["type"] == "authority"]
authority_in_loops = [a["id"] for a in authority if a["loops"]]
delay_counts = Counter(l["delay"] for l in L.values())
order = {"S": 1, "M": 2, "L": 3}
loop_delay_rule = []
for k, l in LP.items():
    if l.get("links"):
        slowest = max((L[x]["delay"] for x in l["links"]), key=lambda z: order[z])
        loop_delay_rule.append((k, l["delay"], slowest, l["delay"] == slowest))
loop_sign_rule = []
for k, l in LP.items():
    if l.get("links"):
        neg = sum(1 for x in l["links"] if L[x]["polarity"] == "-")
        loop_sign_rule.append((k, l["type"], neg, ("R" if neg % 2 == 0 else "B") == l["type"]))

# ------------------------------------------------------------------ model consistency facts used by the issue list
d6 = N["D6"]
compound_domains = [(k, n["domain"]) for k, n in N.items() if "/" in str(n["domain"])]
conceptual_chain_items = {k: [c[0] for c in LP[k]["chain"]] for k in ["B2", "B3", "R9"]}
conceptual_chain_non_ids = {k: [x for x in v if x not in N] for k, v in conceptual_chain_items.items()}
conceptual_loop_grades = {k: LP[k]["evidence"] for k in ["B2", "B3", "R9"]}
counts_meta = d["meta"]["counts"]
counts_live = {"sources_register_ids": len(d["sources"]), "issues_records": len(I),
               "issues_active": sum(1 for v in I.values() if not v.get("retired"))}
glossary_connection_prefixes = re.findall(r"\b(LX|LE|LT|L|T)\b", G.get("Connection", ""))
link_prefixes = Counter(re.match(r"[A-Z]+", k).group(0) for k in L)

data = OrderedDict()
data["generated"] = {"script": "work/build/scripts/phase-1/systems_marks_data.py", "run_date": "2026-10-21",
                     "source": "work/extract/atlas-v7-data.json", "snapshot": SNAP, "meta_counts": counts_meta,
                     "counts_live": counts_live}
data["palette"] = PALETTE
data["contrast_table"] = contrast_table
data["chip_contrast"] = chip_contrast
data["muted_on_light"] = muted_on_light
data["grayscale_values"] = {k: gray(v) for k, v in PALETTE.items()}
data["renderer"] = {"grade_table": grade_table, "legend_dashes": legend, "edge_css_dashes": edge_css, "edge_width": edge_width,
                    "kind_label": kind_label, "ambiguous_rule": renderer_types_only_when, "pill_rx": pill_rx,
                    "outside_driver_region": outside_region}
data["quotes"] = quotes
data["grades"] = {k: dict(v) for k, v in grades.items()}
data["grade_facts"] = {"contested_flag_links": contested_links, "plausible_contested_links": pc_links,
                       "flag_equals_grade": contested_links == pc_links, "mixed_remedy_issue": mixed_remedy,
                       "retired_issue": retired_issue, "remedy_contested": remedy_contested, "problem_contested": problem_contested,
                       "not_yet_tested_uses": not_yet_tested_uses, "grade_examples": grade_examples}
data["links_example"] = grade_example_detail
data["loops"] = examples
data["loops_through_C3"] = shared_c3
data["r11_has_variable_b4"] = r11_has_variable_b4
data["reform_R01"] = reform_r01
data["namespaces"] = {k: {"count": len(v), "sample": v[:6]} for k, v in ns.items()}
data["v5_standards_rules"] = std_rules
data["collisions"] = {"exact": exact_collisions, "near": near_collisions, "suffix_neighbours": suffix_neighbours,
                      "prefix_candidates": prefix_candidates, "pairs": collision_pairs}
data["chip_examples"] = chip_examples
data["effects"] = {"total": len(all_effects), "plain": len(plain), "qualified": len(qualified),
                   "qualified_list": qualified, "plain_counts": dict(Counter(e[2] for e in plain)), "words": effect_words,
                   "families": families, "costs_live": costs_live, "parser_covered": parsed_ok, "examples": effect_examples}
data["routes"] = {"entries": len(route_entries), "checked": len(route_checked), "checked_list": route_checked,
                  "feasibility": dict(Counter(e[2] for e in route_entries)),
                  "scale": d["routes"]["feasibility_scale"], "names": {r["code"]: r["name"] for r in d["routes"]["items"]}}
data["repair"] = {"rows": repair_rows, "direction_counts": dict(Counter(r["direction"] for r in repair_rows)),
                  "instrument_counts": dict(Counter(r["instrument"] for r in repair_rows)),
                  "family_counts": dict(Counter(r["family"] for r in repair_rows)), "unmapped_instruments": unmapped_instruments,
                  "loop_counts": dict(Counter(r["loop"] for r in repair_rows)), "coding_note": d["repairLog"]["coding_note"]}
data["delivery"] = {"rows": delivery_rows, "unparsed": unparsed_periods, "v7_order_is_chronological": v7_order_is_chronological,
                    "grade_counts": dict(Counter(r["grade"] for r in delivery_rows))}
data["authority"] = {"links": authority, "in_loops": authority_in_loops}
data["delay"] = {"counts": dict(delay_counts), "definition": G.get("Delay"), "loop_delay_rule": loop_delay_rule,
                 "loop_delay_rule_holds": all(x[3] for x in loop_delay_rule), "loop_sign_rule": loop_sign_rule,
                 "loop_sign_rule_holds": all(x[3] for x in loop_sign_rule)}
data["model_facts"] = {"D6": {"type": d6["type"], "kind_plain": d6["kind_plain"], "title": d6["title"]},
                       "compound_domains": compound_domains, "conceptual_chain_items": conceptual_chain_items,
                       "conceptual_chain_non_ids": conceptual_chain_non_ids, "conceptual_loop_grades": conceptual_loop_grades,
                       "glossary_connection_prefixes": glossary_connection_prefixes, "link_prefixes": dict(link_prefixes),
                       "rejected_reforms": [k for k, r in R.items() if r["rejected"]],
                       "loop_closure_counts": dict(Counter(l["closure"] for l in LP.values()))}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")

# Console summary for the session log
print("snapshot", SNAP)
print("grade fields", {k: dict(v) for k, v in list(grades.items())[:8]})
print("exact collisions", exact_collisions)
print("near collisions", [(m["normalized"], m["members"]) for m in near_collisions][:30])
print("suffix neighbours", suffix_neighbours)
print("prefix candidates", prefix_candidates)
print("effects", len(all_effects), len(plain), len(qualified), "parser covered", parsed_ok, "live costs", costs_live)
print("routes checked", len(route_checked), "of", len(route_entries))
print("unparsed periods", unparsed_periods, "chronological", v7_order_is_chronological)
print("loop delay rule holds", data["delay"]["loop_delay_rule_holds"], "sign rule holds", data["delay"]["loop_sign_rule_holds"])
print("renderer grade table", {k: (v["label"], v["meter"]) for k, v in grade_table.items()})
print("legend", legend, edge_css, "width", edge_width, "pill rx", pill_rx)
print("chip contrast", chip_contrast)
print("muted", muted_on_light)
print("std rules", std_rules)
print("wrote", OUT.relative_to(ROOT))
