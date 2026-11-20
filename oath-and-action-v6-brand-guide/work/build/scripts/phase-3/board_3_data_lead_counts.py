#!/usr/bin/env python3
"""Board 3's counts and finds, by the data visualization lead (board 3 brief, "The decision file" and panel 1).

Run from oath-and-action-v6-brand-guide/ with python3 -I. Reads only files in the repository; writes nothing in it.

  python3 -I <scratch>/board_3_data_lead_counts.py                 # print every section as JSON
  python3 -I <scratch>/board_3_data_lead_counts.py --out <file>    # also write that JSON to a scratch file

Sections, each from the files themselves:

1. rule_01_9: chapter 14 as finished (rounds 0 to 5), one example per plate that draws data, read from the built
   chapter file: each rule plate's examples (entries 14-001 to 14-014), each kit chart once (a rule whose plate is the
   kit's s-14-sNN, read from its spec; Rules 14.127 and 14.128 point to S06 and S13 and add none), and the examples
   Rules 14.143 and 14.144 log in their entries. Sketches draw invented data and count none. By atlas domain and by
   state, against one in four and one in five (Rule 01.9, DR-229); checked against the generator's
   14-example-log.json row by row.
2. dr_229: every example that draws election data (Elections and representation, D02) or voting data (reported voting
   and turnout, counted under taking part, D10), with D3-689's test: a form keeps election data only where the coverage
   plan writes its use as an election question. Board 2's model (board_2_data_lead_counts.py) for the test's words.
3. changed_found: change ledger rows C-108 to C-134 whose text says "listed for board 3" or "board 3 shows", and decision
   log rows that say "board 3 shows" (D3-2127, D3-2140, ...), so panel 1's list is found by script.
4. held_found: every row of the deferred fixes register whose status reads "Held for Dustin (board 3)", wherever it
   stands, with its section; plus Q-12 from the open questions file.
5. routes_who: atlas V7's reforms[].routes[].who values, counted (the research lead's round 4 finding, D3-1861).
"""
import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from math import floor
from pathlib import Path

ROOT = Path.cwd()
CHAPTER = ROOT / "work/build/guide/chapters/14-data-visualization.json"
PLAN = ROOT / "work/handoffs/phase-3/20261112_Chapter-14-Plan.json"
COVERAGE = ROOT / "work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md"
ENTRIES = ROOT / "work/build/guide/entries"
SPECS = ROOT / "work/build/chart-kit/specs"
ATLAS = ROOT / "work/extract/atlas-v7-data.json"
GEN_LOG = ENTRIES / "14-example-log.json"
LEDGER = ROOT / "work/ledger/20261020_Change-Ledger.md"
DLOG = ROOT / "work/ledger/20261020_Decision-Log.md"
REGISTER = ROOT / "work/ledger/20261116_Deferred-Fixes-Register.md"
OPENQ = ROOT / "work/ledger/20261020_Open-Questions.md"
BOARD_2 = ROOT / "work/handoffs/phase-3/20261113_Board-2-Decisions.json"

STATES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
          "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
          "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
          "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
          "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
          "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
          "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
          "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
          "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
NAMES = {v: k for k, v in STATES.items()}
# board 2's words for D3-689's test (board_2_data_lead_counts.py, kept as written there)
ELECTION_USE = re.compile(r"\belection|\bvot(e|es|ing|er|ers)\b|\bballot|\brace(s)?\b|ranked-choice|House district|House seat|"
                          r"seats in a chamber|majority", re.I)
VOTING_DATA = re.compile(r"reported voting|reported turnout|turnout|citizens 18 and over", re.I)
KIT = re.compile(r"s-14-(s\d+)")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def coverage_forms():
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


def tally(rows, dom_title):
    n = len(rows)
    doms = Counter(x["domain"] for x in rows if x["domain"] and x["domain"] != "all")
    sts = Counter(s for x in rows for s in x["states"])
    dl, sl = floor(n / 4), floor(n / 5)
    return {"examples": n, "limit_domain": dl, "limit_state": sl,
            "atlas_wide": sum(1 for x in rows if x["domain"] == "all"),
            "by_domain": [{"domain": d, "title": dom_title[d], "count": k, "limit": dl, "share": round(k / n, 3),
                           "passes": k <= dl} for d, k in sorted(doms.items(), key=lambda kv: (-kv[1], kv[0]))],
            "by_state": [{"state": NAMES.get(s, s), "code": s, "count": k, "limit": sl, "passes": k <= sl}
                         for s, k in sorted(sts.items(), key=lambda kv: (-kv[1], NAMES.get(kv[0], kv[0])))],
            "passes": all(k <= dl for k in doms.values()) and all(k <= sl for k in sts.values())}


def chapter_14(atlas):
    dom_title = {d["id"]: d["title"] for d in atlas["domains"]}
    chap = json.loads(CHAPTER.read_text())
    plan = json.loads(PLAN.read_text())
    by_rule = {f["rule"]: f for f in plan["forms"]}
    log, seen_specs, sketches, none = [], set(), [], []
    for r in chap["rules"]:
        rid = r["id"]
        sp = (r.get("correct") or {}).get("specimen", "")
        n = int(rid.split(".")[1])
        ef = ENTRIES / f"14-{n:03d}.json"
        ent = json.loads(ef.read_text()) if ef.exists() else {}
        m = KIT.fullmatch(sp)
        if ent.get("examples"):
            kind = "rule plate" if n <= 14 else "chart in full"
            for ex in ent["examples"]:
                log.append({"where": f"Rule {rid} plate", "rule": rid, "kind": kind, "domain": ex.get("domain"),
                            "states": ex.get("states") or [], "example": ex.get("example"), "round": 5 if n > 14 else 1,
                            "source": str(ef.relative_to(ROOT))})
        elif m:
            sid = m.group(1).upper()
            if sid in seen_specs:
                continue
            seen_specs.add(sid)
            spec = json.loads((SPECS / f"{sid.lower()}.json").read_text())
            f = by_rule.get(rid, {})
            ds = spec.get("dataset")
            log.append({"where": sid, "rule": rid, "kind": "specimen", "form": f.get("form") or spec.get("form"),
                        "family_section": f.get("family_section"), "domain": spec.get("domain"),
                        "dataset": ds if isinstance(ds, list) else [ds], "states": spec.get("states") or [],
                        "example": spec.get("title", ""), "round": f.get("round", 5),
                        "built_in_phase_2": f.get("status") == "built", "source": f"work/build/chart-kit/specs/{sid.lower()}.json"})
        elif "sketch" in sp:
            sketches.append(rid)
        else:
            none.append({"rule": rid, "specimen": sp or None, "specimen_at": r.get("specimen_at")})
    return log, sketches, none, dom_title


def rule_01_9(atlas):
    log, sketches, none, dom_title = chapter_14(atlas)
    t = tally(log, dom_title)
    gen = json.loads(GEN_LOG.read_text())
    mine = Counter((x["rule"], x["domain"]) for x in log)
    theirs = Counter((x["rule"], x.get("domain")) for x in gen["rows"])
    by_round = Counter(x["round"] for x in log)
    return {
        "limits": {"domain": "1 in 4", "state": "1 in 5"},
        "refs": ["Rule 01.9", "DR-229", "D3-689"],
        "scope": "Chapter 14 as finished: rounds 0 to 5, rule plates included; sketches draw invented data and count none",
        "total_examples": t["examples"], "limit_domain": t["limit_domain"], "limit_state": t["limit_state"],
        "atlas_wide": t["atlas_wide"], "by_domain": t["by_domain"], "by_state": t["by_state"], "passes": t["passes"],
        "make_up": {"rule_plates": sum(1 for x in log if x["kind"] == "rule plate"),
                    "kit_charts": sum(1 for x in log if x["kind"] == "specimen"),
                    "charts_in_full": sum(1 for x in log if x["kind"] == "chart in full"),
                    "by_round": {str(k): v for k, v in sorted(by_round.items())},
                    "sketches_not_counted": len(sketches),
                    "rules_pointing_to_a_shared_chart": [x for x in none if x.get("specimen_at")]},
        "recount": len(log),
        "generator_log": str(GEN_LOG.relative_to(ROOT)),
        "generator_examples": gen.get("examples"),
        "agrees_with_generator_log": mine == theirs and gen.get("examples") == len(log)
                                     and gen.get("all_domains") == t["atlas_wide"],
        "differences": {"only_in_recount": sorted(f"{a} {b}" for a, b in (mine - theirs).elements()),
                        "only_in_log": sorted(f"{a} {b}" for a, b in (theirs - mine).elements())},
        "board_2": None,
        "rows": log,
    }, log


def dr_229(log):
    cov = {nm: c for (fam, nm), c in coverage_forms().items()}
    out = []
    for x in log:
        voting = x["domain"] == "D10" and VOTING_DATA.search(x.get("example") or "")
        if x["domain"] != "D02" and not voting:
            continue
        ds = x.get("dataset") or []
        data = ("Reported voting, counted under taking part" if x["domain"] == "D10" else
                "The atlas's log of rule changes, counted under elections" if any(str(d).startswith("v7-repair-log") for d in ds) else
                "The atlas's causal model (a loop), counted under elections" if x["kind"] == "chart in full" else
                "Election results, seats or election rules")
        row = {"where": x["where"], "rule": x["rule"], "kind": x["kind"], "domain": x["domain"], "data": data,
               "dataset": ds, "example": x.get("example"), "round": x["round"]}
        if x["kind"] == "specimen":
            c = cov.get(norm(x["form"]))
            row.update({"form": x["form"], "coverage_use": c["use"] if c else None,
                        "election_use": bool(c and ELECTION_USE.search(c["use"])),
                        "built_in_phase_2": x["built_in_phase_2"], "spec": x["where"]})
            row["test"] = ("Passes" if row["election_use"] else
                           "Not applied: built in Phase 2 and approved on board 1 before the test" if x["built_in_phase_2"]
                           else "Fails")
        elif x["kind"] == "chart in full":
            row["test"] = ("Not applied: one of Gate 2's three named complex examples, approved with the Phase 3 proposal "
                           "(round 5 ruling (g)); it draws no form of the coverage plan")
        else:
            row["test"] = "Not applied: a rule's own plate, whose lesson needs the data"
        row["election_data"] = True
        row["passes"] = True if row["test"] == "Passes" else False if row["test"] == "Fails" else None
        out.append(row)
    return {
        "test": "A form keeps election data only where the coverage plan writes its use as an election question.",
        "refs": ["DR-229", "D3-689"],
        "examples": out, "count": len(out),
        "election_domain": sum(1 for x in out if x["domain"] == "D02"),
        "voting_under_taking_part": sum(1 for x in out if x["domain"] == "D10"),
        "new_forms_pass": sum(1 for x in out if x["kind"] == "specimen" and not x.get("built_in_phase_2") and x["test"] == "Passes"),
        "new_forms_fail": sum(1 for x in out if x["kind"] == "specimen" and not x.get("built_in_phase_2") and x["test"] == "Fails"),
        "built_specimens": sum(1 for x in out if x.get("built_in_phase_2")),
        "rule_plates": sum(1 for x in out if x["kind"] == "rule plate"),
        "charts_in_full": sum(1 for x in out if x["kind"] == "chart in full"),
        "added_since_board_2": [f"{x['where']} (Rule {x['rule']})" for x in out if x["round"] >= 4],
    }


def table_rows(text, start_heading=None):
    rows, sec = [], None
    for l in text.splitlines():
        if l.startswith("#"):
            sec = l.lstrip("#").strip()
            continue
        if l.startswith("|") and not re.match(r"^\|\s*-", l):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            rows.append((sec, c))
    return rows


def changed_found():
    rows = []
    for l in LEDGER.read_text().splitlines():
        m = re.match(r"^\| (C-(\d+)) \|", l)
        if not m or not 108 <= int(m.group(2)) <= 134:
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        hit = re.findall(r"[^;|.]*(?:listed for board 3|board 3 shows|shown on board 3)[^;|]*", l, re.I)
        rows.append({"code": c[0], "date": c[1], "area": c[2], "matched": bool(hit),
                     "board_3_words": [h.strip() for h in hit], "approved_at": c[-1]})
    dl = []
    for l in DLOG.read_text().splitlines():
        m = re.match(r"^\| ((?:D3|DR)-\d+) \|", l)
        if m and re.search(r"board 3 shows|shows? on board 3|shown on board 3|listed for board 3", l, re.I):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            dl.append({"code": c[0], "decision": c[1][:300]})
    return {"ledger": str(LEDGER.relative_to(ROOT)), "rows_read": "C-108 to C-134",
            "match": ["listed for board 3", "board 3 shows", "shown on board 3"],
            "rows": [r for r in rows if r["matched"]], "rows_read_count": len(rows),
            "found": [r["code"] for r in rows if r["matched"]],
            "decision_log": {"file": str(DLOG.relative_to(ROOT)), "rows": dl}}


def held_found():
    text = REGISTER.read_text()
    held, sec = [], None
    head = None
    for l in text.splitlines():
        if l.startswith("#"):
            sec = l.lstrip("#").strip()
            head = None
            continue
        if l.startswith("|") and not re.match(r"^\|\s*-", l):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if c[0] == "Code" or c[0] == "Field":
                head = c
                continue
            if head and len(c) == len(head) and re.search(r"held for dustin \(board 3\)", c[-1], re.I):
                held.append({"section": sec, **{h.lower().replace(" ", "_"): v for h, v in zip(head, c)}})
    q = None
    for l in OPENQ.read_text().splitlines():
        if l.startswith("| Q-12 "):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            q = {"code": c[0], "question": c[1], "why": c[2], "default": c[3], "raised_by": c[4]}
            break
    in_section = [h for h in held if h["section"] == "Held for Dustin (board 3)"]
    return {"register": str(REGISTER.relative_to(ROOT)), "section": "Held for Dustin (board 3)",
            "rows_in_section": len(in_section), "rows_held_anywhere": len(held),
            "held_elsewhere": [{"section": h["section"], "code": h["code"]} for h in held if h["section"] != "Held for Dustin (board 3)"],
            "rows": held, "q_12": q}


def routes_who(atlas):
    vals = []
    reforms = atlas["reforms"]
    for r in (reforms.values() if isinstance(reforms, dict) else reforms):
        rid = r.get("id")
        for rt in r.get("routes") or []:
            vals.append({"reform": rid, "route": rt.get("id") or rt.get("code") or rt.get("route"), "who": rt.get("who")})
    c = Counter(v["who"] for v in vals)
    verb = re.compile(r"^(Repeal|Restructure|Codify|Rescind|Legalize|Require|Create|Pass|Adopt|Amend|Ban|Allow|End|Set|Give|Make|"
                      r"Expand|Enact|Establish|Reverse|Raise|Lower|Cap|Limit|Fund|Reform|Replace|Abolish|Extend|Strengthen)\b")
    return {"field": "reforms[].routes[].who", "entries": len(vals), "distinct": len(c),
            "top": [{"who": k, "count": n} for k, n in c.most_common(12)],
            "verb_led": [v for v in vals if v["who"] and verb.match(v["who"])],
            "empty": sum(1 for v in vals if not v["who"])}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out")
    a = ap.parse_args()
    atlas = json.loads(ATLAS.read_text())
    r9, log = rule_01_9(atlas)
    b2 = json.loads(BOARD_2.read_text()).get("counts", {}).get("rule_01_9", {})
    r9["board_2"] = {"file": str(BOARD_2.relative_to(ROOT)), "built": (b2.get("built") or {}).get("examples"),
                     "with_round_4_planned": b2.get("total_examples")}
    out = {"script": "scratch: c08/data-lead/board_3_data_lead_counts.py",
           "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "rule_01_9": r9, "dr_229": dr_229(log), "changed_found": changed_found(), "held_found": held_found(),
           "routes_who": routes_who(atlas)}
    s = json.dumps(out, indent=1, ensure_ascii=False)
    if a.out:
        Path(a.out).write_text(s + "\n")
    print(s)


if __name__ == "__main__":
    main()
