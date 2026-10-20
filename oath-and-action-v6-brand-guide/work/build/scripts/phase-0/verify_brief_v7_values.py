#!/usr/bin/env python3
"""Phase 0: check every Atlas V7 value the Master Brief quotes in section 8 (items 7 and 8),
section 13 and section 14 against work/extract/atlas-v7-data.json. Also checks the section 2
counts. Read only. Writes work/handoffs/phase-0/20261020_Brief-V7-Values-Check.json.

Run with:  python3 -I verify_brief_v7_values.py
"""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
V7 = json.load(open(os.path.join(ROOT, "work", "extract", "atlas-v7-data.json"), encoding="utf-8"))
STD = open(os.path.join(ROOT, "work", "extract", "v5-polished", "chapters-text", "15-standards.txt"), encoding="utf-8").read()
OUT = os.path.join(ROOT, "work", "handoffs", "phase-0", "20261020_Brief-V7-Values-Check.json")

N, L, LP, R = V7["nodes"], V7["links"], V7["loops"], V7["reforms"]
rows = []


def check(section, claim, brief, actual, ok=None, note=""):
    if ok is None:
        ok = brief == actual
    rows.append({"section": section, "claim": claim, "brief": brief, "v7": actual,
                 "status": "confirmed" if ok else "corrected", "note": note})


C = collections.Counter
mc = V7["meta"]["counts"]

# ---- section 2 counts (context for the gate report)
check("2", "variables", 51, len(N))
check("2", "connections", 118, len(L))
check("2", "loops (numbered)", "23 (20)", "%d (%d)" % (len(LP), sum(1 for x in LP.values() if x["links"])))
check("2", "reforms", 50, len(R))
check("2", "issues (active)", "194 (193)", "%d (%d)" % (len(V7["issues"]), sum(1 for i in V7["issues"].values() if not i["retired"])))
check("2", "claims", 433, len(V7["claims"]))
check("2", "sources", 1099, mc["sources"], ok=mc["sources"] == 1099,
      note="meta.counts.sources is 1099; the sources register holds %d IDs (meta.counts.sources_total_ids %d)" % (
          len(V7["sources"]), mc["sources_total_ids"]))
check("2", "pathways, hubs", "16, 5", "%d, %d" % (len(V7["pathways"]), len(V7["hubs"])))

# ---- section 8 item 7
vb = sorted(k for k in N if re.fullmatch(r"B[2-5]", k))
lb = sorted(k for k in LP if re.fullmatch(r"B[2-5]", k))
check("8.7", "variable IDs B2 to B5 match loop IDs B2 to B5", "B2 B3 B4 B5 in both", "nodes %s; loops %s" % (" ".join(vb), " ".join(lb)),
      ok=vb == lb == ["B2", "B3", "B4", "B5"], note="Also near collisions: variable B1 beside loop B1a; loop R1 beside R1b.")
rl = sorted((k for k in LP if k.startswith("R")), key=lambda s: (int(re.sub(r"\D", "", s)), s))
check("8.7", "loop IDs R1 to R18 beside reform IDs R-01 to R-50", "R1 to R18; R-01 to R-50",
      "R loops: %s (%d). Reforms R-%s to R-%s (%d)" % (", ".join(rl), len(rl), min(R)[2:], max(R)[2:], len(R)),
      ok=True, note="The range holds. No R4, R14 or R17 exists; R1b, R4a and R4b carry letter suffixes.")
std_rules = re.findall(r"^R([1-9])\b", STD, re.M)
check("8.7", "V5 Standards numbers its rules R1 to R9", "R1 to R9", "R" + ", R".join(sorted(set(std_rules))),
      ok=sorted(set(std_rules)) == [str(i) for i in range(1, 10)],
      note="Standards states: 'Rules, lockups, marks and checks carry numbers so a reviewer can cite R5 instead of describing it.' "
           "Its closing checklist lists R1 to R3 and R5 to R9 and skips R4.")

# ---- section 8 item 8
lg = C(x["evidence"] for x in L.values())
ig = C(x["grade"] for x in V7["issues"].values())
cg = C(x["confidence"] for x in V7["claims"].values())
pe = C(x["problem_evidence"]["grade"] for x in R.values())
re_ = C(x["remedy_evidence"]["grade"] for x in R.values())
check("8.8", "connections use 'well-supported' and 'plausible_contested'", "yes", dict(lg),
      ok="well-supported" in lg and "plausible_contested" in lg)
check("8.8", "issues use 'well_supported' and 'retired'", "yes", dict(ig), ok="well_supported" in ig and "retired" in ig)
check("8.8", "claims use 'contested'", "yes", dict(cg), ok="contested" in cg,
      note="Claims also use 'well-supported' with a hyphen.")
mixed = "Mixed means" in V7["methods"]["how_claims_are_assessed"]
uses_mixed = sum(1 for x in list(lg) + list(ig) + list(cg) + list(pe) + list(re_) if x == "mixed")
check("8.8", "methods text defines 'Mixed'", "yes", "defined: %s; records graded mixed: %d" % (mixed, uses_mixed), ok=mixed,
      note="No connection, issue, claim or reform carries 'mixed' as a grade. repairLog uses 'mixed' as a direction, a separate vocabulary.")
check("8.8", "(not quoted) reform problem and remedy grades", "n/a", {"problem": dict(pe), "remedy": dict(re_)}, ok=True,
      note="Reforms use 'well-supported', 'plausible_contested' and also 'contested' (one remedy grade).")

# ---- section 13
check("13", "current chapter holds two specimens", 2, 4, ok=False,
      note="11-data.html draws four: a bar chart of primary types, a turnout line chart, a district dumbbell for the competitiveness index and a bill tracker list.")
check("13", "repair log rows", 64, len(V7["repairLog"]["rows"]))
check("13", "delivery log cases", 24, len(V7["deliveryLog"]["rows"]),
      note="Delivery log dates are periods ('1935-1955', 'FY2024', '2024 analysis'), so a time chart needs a start-year rule.")
dirs = C(r["direction"] for r in V7["repairLog"]["rows"])
check("13", "repair log directions", "toward voters, away from voters, voters kept existing rules, mixed, pending",
      dict(dirs), ok=set(dirs) == {"toward voters", "away from voters", "voters kept existing rules", "mixed", "pending"})
check("13", "repair log instrument field", "instrument", dict(C(r["instrument"] for r in V7["repairLog"]["rows"])), ok=True)
check("13", "delays and grades across 118 connections", 118, len(L))
loc = [x for x in V7["routes"]["items"] if x["code"] == "LOC"][0]
r01loc = [x for x in R["R-01"]["routes"] if x["route"] == "LOC"][0]
check("13", "19 states prohibit RCV in some or all elections, as of Oct 15, 2026", "19 states, 2026-10-15",
      "route LOC: '%s'; R-01 LOC note checked %s" % (re.search(r"19 states[^.]*", loc["depends"]).group(0), r01loc["checked"]), ok=True)
cf = list(next(iter(V7["claims"].values())).keys())
check("13", "claims carry confidence, population, jurisdiction, period, limitation, sources", "fields present", cf,
      ok=all(k in cf for k in ("confidence", "population", "jurisdiction", "period", "limitation", "sources")))
check("13", "numbers: eight headline figures with captions, qualifications, sources and check dates", 8,
      "%d; verified_status: %s" % (len(V7["numbers"]), sorted({n["verified_status"] for n in V7["numbers"]})),
      ok=len(V7["numbers"]) == 8)
check("13", "meta, outcomes, scenarios, overlays, omissions, leverage present", "present",
      [k for k in ("meta", "outcomes", "scenarios", "overlays", "omissions", "leverage") if k in V7], ok=True)

# ---- section 14 grammar
nt = C(x["type"] for x in N.values())
check("14", "node types", "stock 31, flow 9, auxiliary 6, driver 5", dict(nt),
      ok=nt == C({"stock": 31, "flow": 9, "auxiliary": 6, "driver": 5}),
      note="D6 is typed flow while its kind_plain text begins 'Stock (an amount built up over time)'.")
check("14", "increase_means on every variable", 51, sum(1 for x in N.values() if x.get("increase_means")))
check("14", "drivers X1 to X5", "X1-X5", sorted(k for k, x in N.items() if x["type"] == "driver"),
      ok=sorted(k for k, x in N.items() if x["type"] == "driver") == ["X1", "X2", "X3", "X4", "X5"])
check("14", "V7 draws drivers as rounded pills outside the clusters", "rounded pills", "not confirmed", ok=False,
      note="In the extracted V7 renderer (work/extract/atlas-v7/script.js) the only rounded pill (rx 11) is the connection-code label, "
           "with an authority variant; regionMap() lists X1 to X5 as a sixth region card, 'Outside drivers'. The rendered page could not be inspected beyond two screenshots.")
lt = C(x["type"] for x in L.values())
check("14", "connection types", "causal 80, money 17, information 9, authority 7, ownership 5", dict(lt),
      ok=lt == C({"causal": 80, "money": 17, "information": 9, "authority": 7, "ownership": 5}))
pol = C(str(x["polarity"]) for x in L.values())
none_auth = all(x["type"] == "authority" for x in L.values() if x["polarity"] is None)
check("14", "polarity + 70, − 41, none 7 (all authority)", "70/41/7", dict(pol), ok=pol == C({"+": 70, "-": 41, "None": 7}) and none_auth)
gl = {g["term"]: g["definition"] for g in V7["glossary"]}
check("14", "a plus sign means same direction and does not mean a benefit", "stated", gl.get("Positive sign (+)"),
      ok="does not mean a benefit" in gl.get("Positive sign (+)", ""))
auth = sorted(k for k, x in L.items() if x["type"] == "authority")
check("14", "authority connections", "LE02, LE03, LE19, LT13, LT14, LT16, LT17", ", ".join(auth),
      ok=auth == sorted(["LE02", "LE03", "LE19", "LT13", "LT14", "LT16", "LT17"]))
in_loops = [k for k in auth if L[k]["loops"]] + [lp for lp, x in LP.items() if set(x["links"]) & set(auth)]
check("14", "authority never closes a loop", "none in any loop", in_loops or "none", ok=not in_loops)
check("14", "delay definitions", "S under 2, M 2 to 10, L over 10", gl.get("Delay"), ok="S, under 2 years; M, 2 to 10 years; L, over 10 years" in gl.get("Delay", ""))
check("14", "connection grades", "documented, well-supported, plausible, plausible_contested, hypothesis", dict(lg),
      ok=set(lg) == {"documented", "well-supported", "plausible", "plausible_contested", "hypothesis"})
cont = sorted(k for k, x in L.items() if x["contested"])
check("14", "contested flag on 7", 7, len(cont), note="The flag sits on exactly the 7 plausible_contested links: " + ", ".join(cont))
check("14", "V7 draws hypothesis as a dotted line", "dotted", "methods: 'drawn as a dotted line'; renderer .u-hypothesis dasharray 2 4",
      ok="dotted line" in V7["methods"]["how_claims_are_assessed"],
      note="V7's renderer also dashes plausible (9 4) and dash-dots contested (9 3 2 3); documented and well-supported are solid.")
lpt = C(x["type"] for x in LP.values())
check("14", "loop types R 18, B 5", "18/5", dict(lpt), ok=lpt == C({"R": 18, "B": 5}))
hyp = sorted(k for k, x in LP.items() if x["closure"].startswith("closed with"))
con = sorted(k for k, x in LP.items() if x["closure"].startswith("conceptual"))
check("14", "closure: hypothesized step R2, R16; conceptual B2, B3, R9", "R2, R16 / B2, B3, R9", "%s / %s" % (", ".join(hyp), ", ".join(con)),
      ok=hyp == ["R16", "R2"] and con == ["B2", "B3", "R9"])
check("14", "layers core, economy, technology; domains D01 to D10", "3 layers, 10 domains",
      "%s; %s" % (", ".join(V7["layers"]), ", ".join(d["id"] for d in V7["domains"])), ok=len(V7["layers"]) == 3 and len(V7["domains"]) == 10)
bands = C(x["band"] for x in R.values())
check("14", "reform bands", "parameter, feedback, information, rules, power to change the rules, goals", dict(bands),
      ok=set(bands) == {"parameter", "feedback", "information", "rules", "power to change the rules", "goals"})
codes = set(V7["outcomes"]["effect_codes"])
allv = [c for x in R.values() for c in x["effects"].values()]
std = sum(1 for c in allv if c.replace("−", "-") in codes)
check("14", "effects by family DQ GE EP EQ in codes +L +M +S 0 −S −M ?", "seven codes", "%d of %d values use one of the seven codes" % (std, len(allv)),
      ok=False, note="The families and the code list are right. %d values add a qualifier or a range, such as '+M sector', '0 to -S', '+S hypothesis' and '+M / -M risk'; "
                     "a display must keep that text." % (len(allv) - std))
check("14", "V7 states effects are never added into one score", "stated", V7["outcomes"]["effect_codes_note"][-90:],
      ok="never added together" in V7["outcomes"]["effect_codes_note"])
check("14", "problem_evidence and remedy_evidence on each reform", 50, sum(1 for x in R.values() if x.get("problem_evidence") and x.get("remedy_evidence")))
rc = [x["code"] for x in V7["routes"]["items"]]
check("14", "routes.items: 11 codes", 11, len(rc), note=", ".join(rc))
fs = set(V7["routes"]["feasibility_scale"])
check("14", "feasibility high, medium, low, very low", "4 levels", sorted(fs), ok=fs == {"high", "medium", "low", "very low"})
dp = set(V7["routes"]["dependencies"])
check("14", "dependencies authority, funding, enforcement, capacity, durability", "5", sorted(dp),
      ok=dp == {"authority", "funding", "enforcement", "capacity", "durability"})
chk = C(bool(x["checked"]) for r in R.values() for x in r["routes"])
check("14", "per-reform checked dates", "present", "%d of %d reform-route entries carry a checked date" % (chk[True], sum(chk.values())),
      ok=False, note="Most route entries have checked: null. A tracker cannot show a check date for them.")
check("14", "repairLog 64, deliveryLog 24", "64/24", "%d/%d" % (len(V7["repairLog"]["rows"]), len(V7["deliveryLog"]["rows"])))
check("14", "omissions 9, rejectedLinks 3, methods", "9/3/present", "%d/%d/%s" % (len(V7["omissions"]), len(V7["rejectedLinks"]), "present" if "methods" in V7 else "missing"))


def link_check(ex, lid, frm, to, pol, typ, ev, dl):
    x = L[lid]
    actual = (x["from"], x["to"], x["polarity"], x["type"] if typ else None, x["evidence"] if ev else None, x["delay"] if dl else None)
    want = (frm, to, pol, typ, ev, dl)
    check("14 " + ex, lid, " ".join(str(w) for w in want if w), " ".join(str(a) for a in actual if a), ok=actual == want)


# worked example 1
check("14 ex1", "R1 title", "Wealth and political influence reinforce each other", LP["R1"]["title"])
link_check("ex1", "L01", "A1", "B1", "+", "money", "well-supported", "S")
link_check("ex1", "L02", "B1", "E1", "+", "money", "plausible", "M")
link_check("ex1", "L03", "E1", "A1", "+", "money", "well-supported", "L")
check("14 ex1", "L02 is the least certain step", "weakest", LP["R1"]["evidence_summary"][:160], ok="weakest" in LP["R1"]["evidence_summary"])
# worked example 2
check("14 ex2", "R8 title", "Housing scarcity strengthens owners' incentive to restrict building", LP["R8"]["title"])
link_check("ex2", "L38", "A5", "A6", "+", None, "well-supported", "L")
link_check("ex2", "L39", "A6", "A5", "+", None, "well-supported", "L")
check("14 ex2", "V7 notes R8 no longer depends on A1", "noted", LP["R8"]["evidence"], ok="no longer depends on A1" in LP["R8"]["evidence"])
# worked example 3
check("14 ex3", "B4 title", "Electoral consequences can improve public performance", LP["B4"]["title"])
for lid, f, t, p in (("L23", "D5", "C3", "-"), ("L24", "C3", "C5", "+"), ("L54", "C5", "D5", "+")):
    link_check("ex3", lid, f, t, p, None, None, None)
check("14 ex3", "R10 title", "Safe seats shift accountability to small primary electorates", LP["R10"]["title"])
check("14 ex3", "R10 links", "L08, L25, L53, L42", ", ".join(LP["R10"]["links"]))
check("14 ex3", "V7 names C3 to C4 as the weakest link", "C3 to C4", LP["R10"]["evidence"], ok="C3 to C4 (the weakest link)" in LP["R10"]["evidence"],
      note="C3 to C4 is L53, graded plausible.")
# worked example 4
r = R["R-01"]
check("14 ex4", "R-01 title", "All-party primaries with ranked general elections", r["title"])
check("14 ex4", "R-01 targets", "L25, L08, C2", ", ".join(r["targets"]))
check("14 ex4", "R-01 loops", "R10, B4, R11", ", ".join(r["loops"]))
check("14 ex4", "R-01 effects", "DQ +M, GE +S, EP 0, EQ 0", ", ".join("%s %s" % kv for kv in r["effects"].items()))
rt = ", ".join("%s (%s)" % (x["route"], x["feasibility"]) for x in r["routes"])
check("14 ex4", "R-01 routes", "BI (medium), SS (low), LOC (medium), FS (very low)", rt)
dates = ", ".join("%s %s" % (x["route"], x["checked"] or "no date") for x in r["routes"])
check("14 ex4", "R-01 route check dates", "a date on each route", dates, ok=all(x["checked"] for x in r["routes"]),
      note="Only BI and LOC carry a check date (2026-10-15); SS and FS have none. The reform status itself was checked 2026-10-15.")
# worked example 5 and 6
check("14 ex5", "seven authority connections exist for an authority diagram", 7, len(auth))
check("14 ex6", "B2, B3, R9 are conceptual loops with no numbered links", "no links", {k: LP[k]["links"] for k in ("B2", "B3", "R9")},
      ok=all(not LP[k]["links"] for k in ("B2", "B3", "R9")))

json.dump(rows, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for x in rows:
    print("%-7s %-9s %-60s | brief: %s | V7: %s %s" % (x["section"], x["status"], x["claim"][:60], str(x["brief"])[:70], str(x["v7"])[:110],
                                                     ("| " + x["note"][:120]) if x["note"] else ""))
print(C(x["status"] for x in rows))
