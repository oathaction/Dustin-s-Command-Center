#!/usr/bin/env python3
"""Board 2's counts, by the data visualization lead (board 2 brief, "Who does what"; D3-689; DR-229; ruling (g)).

Run from the repository (python3 -I). Reads only files in the repository; writes nothing unless --write is given.

  python3 -I work/build/scripts/phase-3/board_2_data_lead_counts.py            # print the counts as JSON
  python3 -I work/build/scripts/phase-3/board_2_data_lead_counts.py --write \
      work/handoffs/phase-3/20261113_Board-2-Decisions.json                    # set its "counts" and "checks" keys only

What it counts, each from the files themselves:

1. Tiers (checks.tiers). Every form of rounds 1 to 3 in the chapter 14 plan, against the coverage plan's tier
   (work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md), the data plans' tier column (rounds 1 and 2 plan,
   rows 1 to 82; round 3 plan, rows 83 to 114), the entry file's tier and the spec's tier. A form whose tier differs
   anywhere is listed.
2. Datasets (checks.datasets). Every spec of rounds 1 to 3 against the dataset its data plan row names: the spec's
   files are traced through each derived sidecar's derived_from to the public files, and a spec none of whose public
   files the plan row names, or whose plan row names a file the spec does not reach, is listed.
3. Rule 01.9 (counts.rule_01_9). Chapter 14's examples as the guide's generator places them (the rule plates' examples
   in entries 14-001 to 14-014, and each spec of rounds 1 to 3 once, by its spec's domain and states), plus round 4's
   data-bearing rows as its plan gives them, by atlas domain and by state, against one in four and one in five.
4. DR-229 under D3-689's test (counts.dr_229). Every example that draws election data (the Elections and
   representation domain) or voting data (reported voting and turnout, counted under taking part), with its form's use
   as the coverage plan writes it and whether that use is an election question.
"""
import argparse
import glob
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from math import floor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PLAN = ROOT / "work/handoffs/phase-3/20261112_Chapter-14-Plan.json"
COVERAGE = ROOT / "work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md"
PLAN_12 = ROOT / "work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md"
PLAN_3 = ROOT / "work/handoffs/phase-3/20261112_Round-3-Data-Plan.md"
PLAN_4 = ROOT / "work/handoffs/phase-3/20261112_Round-4-Data-Plan.md"
ENTRIES = ROOT / "work/build/guide/entries"
SPECS = ROOT / "work/build/chart-kit/specs"
DATA = ROOT / "work/build/data"
ATLAS = ROOT / "work/extract/atlas-v7-data.json"
GEN_LOG = ENTRIES / "14-example-log.json"
RULING_G = 108   # the data lead's round 3 ruling (g): chapter 14 holds 108 examples with round 4 as planned

STATES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
          "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
          "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
          "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
          "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
          "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
          "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
          "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
          "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}

# D3-689's test reads the coverage plan's "Oath & Action uses it for" cell; a use is an election question when it
# names an election, a vote or ballot, a race, House districts or seats, or ranked-choice voting
ELECTION_USE = re.compile(r"\belection|\bvot(e|es|ing|er|ers)\b|\bballot|\brace(s)?\b|ranked-choice|House district|House seat|"
                          r"seats in a chamber|majority", re.I)
# voting data counted under taking part (rounds 1 and 2 plan, counting rule 5): reported voting and turnout
VOTING_DATA = re.compile(r"reported voting|reported turnout|turnout|citizens 18 and over", re.I)


def tier_of(t):
    return (t or "").strip().lower().split(",")[0].strip()


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def md_rows(text, start=None, stop=None):
    """Rows of the pipe tables between two headings, each a list of cells."""
    lines = text.splitlines()
    i0 = 0 if start is None else next(i for i, l in enumerate(lines) if l.startswith(start))
    i1 = len(lines) if stop is None else next(i for i, l in enumerate(lines) if i > i0 and l.startswith(stop))
    out = []
    for l in lines[i0:i1]:
        if l.startswith("|") and not re.match(r"^\|\s*-", l):
            out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out


def coverage_forms():
    """{(family_section, form name): {tier, use, data}} from the coverage plan's section 3 tables."""
    out, fam = {}, None
    for l in COVERAGE.read_text().splitlines():
        m = re.match(r"^### (3\.\d+) ", l)
        if m:
            fam = m.group(1)
            continue
        if l.startswith("## 4."):
            break
        if fam and l.startswith("|") and not re.match(r"^\|\s*-", l):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if c[0] == "Form" or len(c) < 4:
                continue
            out[(fam, norm(c[0]))] = {"form": c[0], "tier": c[1], "use": c[2], "data": c[3]}
    return out


def plan_rows():
    """{data plan row number: {tier, dataset cell, domain cell, states cell}} from the three data plans."""
    rows = {}
    t12 = PLAN_12.read_text()
    for c in md_rows(t12, "## Round 1: 41 forms", "## Rule 01.9 count"):
        if c and c[0].isdigit():
            rows[int(c[0])] = {"form": c[1], "tier": c[2], "dataset": " | ".join(c[4:]), "domain": c[8], "states": c[9],
                               "status": c[10], "file": str(PLAN_12.relative_to(ROOT))}
    t3 = PLAN_3.read_text()
    for c in md_rows(t3, "## Round 3: 32 forms", "Twenty rows take new data"):
        if c and c[0].isdigit():
            rows[int(c[0])] = {"form": c[2], "tier": c[3], "dataset": " | ".join(c[5:]), "domain": c[9], "states": c[10],
                               "status": c[11], "file": str(PLAN_3.relative_to(ROOT))}
    return rows


def round_4_rows():
    t4 = PLAN_4.read_text()
    out = []
    for c in md_rows(t4, "## Round 4: 13 forms", "Eleven rows draw data"):
        if c and c[0].isdigit():
            out.append({"row": int(c[0]), "rule": c[1], "form": c[2], "tier": c[3], "dataset": c[5], "domain": c[9],
                        "states": c[10], "status": c[11]})
    return out


def is_dataset(name):
    return any((DATA / f"{name}{ext}").exists() for ext in (".csv", ".meta.json", ".geojson", ".json"))


def backticked(cell):
    """The dataset files a plan row names anywhere in its cells (a source line variant or a path is not one)."""
    return [x for x in re.findall(r"`([^`]+)`", cell or "") if is_dataset(x)]


def ancestors(name, seen=None):
    """A dataset and every file it is derived from, through each derived sidecar's derived_from."""
    seen = set() if seen is None else seen
    if name in seen:
        return set()
    seen.add(name)
    out = {name}
    meta = DATA / f"{name}.meta.json"
    if not meta.exists():
        return out
    m = json.loads(meta.read_text())
    src = m.get("derived_from") if m.get("kind") == "derived" else None
    if not src:
        return out
    if isinstance(src, str):
        src = re.findall(r"[\w.-]+\.(?:csv|geojson|json)", src)
    for s in src:
        out |= ancestors(re.sub(r"\.(csv|geojson|json)$", "", s), seen)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", help="a decisions JSON file whose counts and checks keys this run sets")
    a = ap.parse_args()

    atlas = json.loads(ATLAS.read_text())
    dom_title = {d["id"]: d["title"] for d in atlas["domains"]}
    dom_code = {norm(v): k for k, v in dom_title.items()}
    plan = json.loads(PLAN.read_text())
    forms = [f for f in plan["forms"] if f.get("round") in (1, 2, 3)]
    cov = coverage_forms()
    prow = plan_rows()

    # 1. tiers
    tiers, unmatched = [], []
    for f in forms:
        c = cov.get((f["family_section"], norm(f["form"])))
        if not c:
            unmatched.append(f"{f['rule']} {f['form']}")
        e = json.loads((ENTRIES / f"14-{int(f['rule'].split('.')[1]):03d}.json").read_text()) \
            if (ENTRIES / f"14-{int(f['rule'].split('.')[1]):03d}.json").exists() else {}
        sp = json.loads((SPECS / f"{f['spec_id'].lower()}.json").read_text()) if f.get("spec_id") else {}
        pr = prow.get(f.get("data_plan_row"), {})
        seen = {"coverage plan": tier_of(c["tier"]) if c else None, "chapter 14 plan": tier_of(f["tier"]),
                "data plan": tier_of(pr.get("tier")) if pr else None, "entry": tier_of(e.get("tier")) if e else None}
        if sp and f.get("spec_id") and not f["spec_id"] in ("S06", "S13"):   # S06 and S13 each serve two forms of two tiers
            seen["spec"] = tier_of(sp.get("tier"))
        vals = {v for v in seen.values() if v}
        tiers.append({"rule": f["rule"], "form": f["form"], "round": f["round"], **{k: v for k, v in seen.items()},
                      "changed": len(vals) > 1})
    tier_changed = [t for t in tiers if t["changed"]]
    by_tier = Counter(tier_of(f["tier"]) for f in forms)

    # 2. datasets
    datasets = []
    for f in forms:
        if not f.get("spec_id"):
            continue
        pr = prow.get(f.get("data_plan_row"), {})
        planned = set(backticked(pr.get("dataset")))
        sp = json.loads((SPECS / f"{f['spec_id'].lower()}.json").read_text())
        ds = sp.get("dataset")
        ds = ds if isinstance(ds, list) else [ds]
        anc = {d: ancestors(d) for d in ds}
        reached = set().union(*anc.values())
        geometry = lambda x: x.startswith("census-cb-2024-") or "tile-layout" in x or x.startswith("census-gazetteer-2024-cd119")
        missing = sorted(planned - reached)                                         # a planned file the spec does not reach
        extra = sorted(d for d in ds if not (anc[d] & planned) and not geometry(d))  # a spec file with no planned file behind it
        if not planned:
            status = "plan row names no file (an atlas file or a built specimen)"
        elif not (reached & planned):
            status = "none of the planned files"
        elif missing:
            status = "a planned file is not reached"
        elif extra:
            status = "adds a file the plan row does not name"
        else:
            status = "as planned"
        datasets.append({"rule": f["rule"], "spec": f["spec_id"], "plan_row": f.get("data_plan_row"),
                         "planned": sorted(planned), "spec_dataset": ds, "reaches": sorted(reached),
                         "missing": missing, "extra": extra, "status": status})

    # 3. Rule 01.9
    log = []
    placed = set()
    for ef in sorted(ENTRIES.glob("14-0[01][0-9].json")):
        n = int(ef.stem.split("-")[1])
        if n > 14:
            continue
        for ex in json.loads(ef.read_text()).get("examples") or []:
            log.append({"where": f"Rule 14.{n} plate", "rule": f"14.{n}", "domain": ex.get("domain"),
                        "states": ex.get("states") or [], "example": ex.get("example"), "kind": "rule plate"})
    for f in sorted(forms, key=lambda r: [int(x) for x in r["rule"].split(".")]):
        sid = f.get("spec_id")
        if not sid or sid in placed:
            continue
        placed.add(sid)
        sp = json.loads((SPECS / f"{sid.lower()}.json").read_text())
        dset = sp.get("dataset")
        log.append({"where": sid, "rule": f["rule"], "form": f["form"], "domain": sp.get("domain"),
                    "dataset": dset if isinstance(dset, list) else [dset],
                    "states": sp.get("states") or [], "example": sp.get("title", ""), "kind": "specimen",
                    "built_in_phase_2": f.get("status") == "built", "round": f["round"]})
    built = len(log)
    r4 = []
    for r in round_4_rows():
        if r["status"].lower().startswith("rule only"):
            continue
        dom = r["domain"].split(" (")[0]
        code = dom_code.get(norm(dom), "all" if "atlas-wide" in dom.lower() else None)
        sts = []
        if not r["states"].lower().startswith("none"):
            sts = [STATES[s] for s in STATES if re.search(rf"\b{re.escape(s)}\b", r["states"])]
        r4.append({"where": f"Round 4 row {r['row']}", "rule": r["rule"], "form": r["form"], "domain": code, "states": sts,
                   "kind": "planned", "round": 4})
    whole = log + r4

    def tally(rows):
        n = len(rows)
        doms = Counter(x["domain"] for x in rows if x["domain"] and x["domain"] != "all")
        sts = Counter(s for x in rows for s in x["states"])
        dl, sl = floor(n / 4), floor(n / 5)
        names = {v: k for k, v in STATES.items()}
        return {"examples": n, "limit_domain": dl, "limit_state": sl,
                "atlas_wide": sum(1 for x in rows if x["domain"] == "all"),
                "by_domain": [{"domain": d, "title": dom_title[d], "count": k, "limit": dl, "share": round(k / n, 3),
                               "passes": k <= dl} for d, k in sorted(doms.items(), key=lambda kv: (-kv[1], kv[0]))],
                "by_state": [{"state": names.get(s, s), "code": s, "count": k, "limit": sl, "passes": k <= sl}
                             for s, k in sorted(sts.items(), key=lambda kv: (-kv[1], names.get(kv[0], kv[0])))],
                "passes": all(k <= dl for k in doms.values()) and all(k <= sl for k in sts.values())}

    gen = json.loads(GEN_LOG.read_text()) if GEN_LOG.exists() else {}
    gen_dom = gen.get("by_domain", {})
    built_t = tally(log)
    mine_dom = {d["domain"]: d["count"] for d in built_t["by_domain"]}
    whole_t = tally(whole)
    rule_01_9 = {
        # the board's table (the data lead's schema): chapter 14 as a whole, round 4 as planned; "built" is rounds 0 to 3
        "limits": {"domain": "1 in 4", "state": "1 in 5"},
        "refs": ["DR-229", "D3-689"],
        "total_examples": whole_t["examples"],
        "limit_domain": whole_t["limit_domain"], "limit_state": whole_t["limit_state"],
        "atlas_wide": whole_t["atlas_wide"],
        "by_domain": whole_t["by_domain"], "by_state": whole_t["by_state"], "passes": whole_t["passes"],
        "built": built_t,
        "ruling_g": RULING_G,
        "recount": len(whole),
        "agrees_with_generator_log": gen.get("examples") == built and gen_dom == mine_dom
                                     and gen.get("all_domains") == built_t["atlas_wide"],
        "generator_log": str(GEN_LOG.relative_to(ROOT)),
        "round_4_rows": r4,
    }

    # 4. DR-229 under D3-689's test
    cov_by_form = {}
    for (fam, nm), c in cov.items():
        cov_by_form[nm] = c
    elect = []
    for x in log:
        voting = x["domain"] == "D10" and VOTING_DATA.search(x.get("example") or "")
        if x["domain"] != "D02" and not voting:
            continue
        ds = x.get("dataset") or []
        data = ("Reported voting, counted under taking part" if x["domain"] == "D10" else
                "The atlas's log of rule changes, counted under elections" if any(str(d).startswith("v7-repair-log") for d in ds) else
                "Election results, seats or election rules")
        row = {"where": x["where"], "rule": x["rule"], "kind": x["kind"], "domain": x["domain"], "data": data,
               "dataset": ds, "example": x.get("example")}
        if x["kind"] == "specimen":
            c = cov_by_form.get(norm(x["form"]))
            row.update({"form": x["form"], "coverage_use": c["use"] if c else None,
                        "election_use": bool(c and ELECTION_USE.search(c["use"])),
                        "built_in_phase_2": x["built_in_phase_2"]})
            row["spec"] = x["where"]
            row["test"] = ("Passes" if row["election_use"] else
                           "Not applied: built in Phase 2 and approved on board 1 before the test" if x["built_in_phase_2"]
                           else "Fails")
        else:
            row["test"] = "Not applied: a rule's own plate, whose lesson needs the data"
        row["election_data"] = True
        # true or false only where the test applies; null where it was not applied
        row["passes"] = True if row["test"] == "Passes" else False if row["test"] == "Fails" else None
        elect.append(row)
    r4_elect = [x for x in r4 if x["domain"] == "D02"]
    dr_229 = {
        "test": "A form keeps election data only where the coverage plan writes its use as an election question",
        "refs": ["DR-229", "D3-689"],
        "examples": elect,
        "count": len(elect),
        "election_domain": sum(1 for x in elect if x["domain"] == "D02"),
        "voting_under_taking_part": sum(1 for x in elect if x["domain"] == "D10"),
        "new_forms_pass": sum(1 for x in elect if x["kind"] == "specimen" and not x.get("built_in_phase_2") and x["test"] == "Passes"),
        "new_forms_fail": sum(1 for x in elect if x["kind"] == "specimen" and not x.get("built_in_phase_2") and x["test"] == "Fails"),
        "built_specimens": sum(1 for x in elect if x.get("built_in_phase_2")),
        "rule_plates": sum(1 for x in elect if x["kind"] == "rule plate"),
        "round_4_planned_election_rows": len(r4_elect),
    }

    out = {
        "script": str(Path(__file__).resolve().relative_to(ROOT)),
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "counts": {"rule_01_9": rule_01_9, "dr_229": dr_229},
        "checks": {
            "tiers": {"forms": len(forms), "by_tier": dict(by_tier), "changed": tier_changed,
                      "unmatched_in_coverage_plan": unmatched, "rows": tiers},
            "datasets": {"specs": len(datasets),
                         "not_as_planned": [d for d in datasets if d["status"] not in
                                            ("as planned", "plan row names no file (an atlas file or a built specimen)")],
                         "rows": datasets},
        },
    }
    if a.write:
        p = Path(a.write)
        doc = json.loads(p.read_text())
        old = doc.get("counts") or {}
        new = {"script": out["script"], "run_utc": out["run_utc"], **out["counts"]}
        for k in ("rule_01_9", "dr_229"):   # a note is words (the editor's); a run keeps it
            if isinstance(old.get(k), dict) and old[k].get("note"):
                new[k]["note"] = old[k]["note"]
        doc["counts"] = new
        doc["checks"] = {"script": out["script"], "run_utc": out["run_utc"], **out["checks"]}
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"wrote counts and checks into {p}")
    else:
        json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
        print()


if __name__ == "__main__":
    main()
