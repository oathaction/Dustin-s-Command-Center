"""Round 4, the infographics maker's checks: every figure a title, note, alt, card or callout of S89 to S95 prints,
checked against the data file it comes from (round 3 brief, call 12). Derives nothing: every round 4 infographic draws
a file the research lead froze, so no derived file is written.

    python3 -I work/build/scripts/phase-3/maker_i_round4_derive.py --figures          # all seven
    python3 -I work/build/scripts/phase-3/maker_i_round4_derive.py --figures S90 S94  # some
    ... --specs DIR    reads the specs from DIR in place of the kit's specs folder

Each check prints PASS or FAIL with what it compared; the script exits 1 on any failure. Paths are relative to the
repository's brand guide folder, found from this file.
"""
import csv
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "work/build/data"
SPECS = ROOT / "work/build/chart-kit/specs"
FAILS = []


def rows(name):
    with open(DATA / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def spec(sid):
    return json.loads((SPECS / f"{sid.lower()}.json").read_text(encoding="utf-8"))


def words(s):
    """Every word field a reader meets: title, measure, notes, alt, chart notes, phone note, labels' words."""
    out = [s.get("title", ""), s.get("measure_line", ""), s.get("alt", ""), s.get("phone_note", ""), s.get("grade_line", "")]
    out += s.get("notes", []) + s.get("chart_notes", []) + s.get("phone_notes", [])
    out.append(json.dumps(s.get("labels", {}), ensure_ascii=False))
    return " ".join(out).replace(" ", " ")


def check(sid, what, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {sid}: {what}{(' (' + detail + ')') if detail else ''}")
    if not ok:
        FAILS.append(f"{sid}: {what}")


def has(sid, text, phrase, what):
    check(sid, f"prints {what}: \"{phrase}\"", phrase in text)


def s89():
    sid, s, r = "S89", spec("S89"), {x["order"]: x for x in rows("govinfo-disaster-declaration-steps")}
    t = words(s)
    main = [k for k, x in r.items() if x["path"] == "main"]
    check(sid, "eight main steps, numbered 1 to 8", len(main) == 8, f"{len(main)} rows with path main")
    check(sid, "one branch, row 4, the emergency request", [k for k, x in r.items() if x["path"] == "branch"] == ["4"])
    check(sid, "30 days: row 3's limit", r["3"]["time_limit"].startswith("Within 30 days of the incident"))
    has(sid, t, "within 30 days", "the request's limit")
    check(sid, "5 days and 30 days: row 4's limit", r["4"]["time_limit"].startswith("Within 5 days after the need becomes apparent and no later than 30 days"))
    check(sid, "60 days: row 8's limit", r["8"]["time_limit"] == "60 days after the declaration")
    check(sid, "30 days after designation: row 9's limit", r["9"]["time_limit"] == "30 days after the area is designated")
    check(sid, "the tribal chief executive may ask directly: row 3", "a tribal government’s chief executive may ask directly" in r["3"]["what_happens"])
    check(sid, "an emergency request leads only to an emergency declaration or a denial: row 6", "an emergency request can lead only to an emergency declaration or a denial" in r["6"]["what_happens"])
    lanes = {lv for l in s["labels"]["lanes"] for lv in l["levels"]}
    used = {v.strip() for x in r.values() for v in x["level"].split(";")}
    check(sid, "every level the file names has a lane", used <= lanes, f"file {sorted(used)}, lanes {sorted(lanes)}")


def s90():
    sid, s = "S90", spec("S90")
    r = {x["order"]: x for x in rows("census-school-system-finances-2024")}
    v = {k: float(x["value"]) for k, x in r.items()}
    # the figures the form prints from the rows: before + the kit's format of value times scale + after
    def fmt(val, f):
        kind, _, nd = f.partition(":")
        nd = int(nd or 0)
        if kind == "billions":
            return f"{val / 1e9:,.{nd}f} billion"
        if kind == "millions":
            return f"{val / 1e6:,.{nd}f} million"
        if kind == "dollars":
            return f"${val:,.{nd}f}"
        if kind == "integer":
            return f"{round(val):,}"
        return str(val)
    figs = [f.get("before", "") + fmt(v[str(f["figure"])] * f.get("scale", 1), f.get("format", "number")) + f.get("after", "") for f in s["labels"]["facts"]]
    check(sid, "four to six facts", 4 <= len(figs) <= 6, f"{len(figs)}")
    t = words(s) + " " + " ".join(figs)
    print("     figures printed large:", figs)
    rev_b = round(v["1"] / 1e6, 1)
    has(sid, t, f"${rev_b:,.1f}", "total revenue, billions (Table 1)")
    cents = [round(v["2"]), round(v["3"]), round(v["4"])]
    check(sid, "the three shares round to whole cents that sum to 100", sum(cents) == 100, f"{cents}")
    for c_ in cents:
        has(sid, t, f"{c_} cents", "a share in cents (Table 5)")
    check(sid, "the three shares sum to 100.0 percent", abs(v["2"] + v["3"] + v["4"] - 100) < 0.01, f"{v['2'] + v['3'] + v['4']:.4f}")
    has(sid, t, f"${round(v['6']):,}", "spending per pupil (Table 8)")
    has(sid, t, f"${round(v['7']):,}", "New York's spending per pupil (Table 11)")
    has(sid, t, f"${round(v['8']):,}", "Idaho's spending per pupil (Table 11)")
    check(sid, "New York ranks first and Idaho last of 51", r["7"]["code"] == "NY" and "Rank 1" in r["7"]["note"] and r["8"]["code"] == "ID" and "Rank 51" in r["8"]["note"])
    has(sid, t, f"{v['9'] / 1e6:.1f} million", "students enrolled, fall 2023 (Table 19)")
    relief = round(v["5"] / 1e6, 1)
    has(sid, t, f"${relief:.1f}", "COVID-19 relief, billions (all data items file)")
    fed_b = round(v["1"] * v["4"] / 100 / 1e6, 1)
    check(sid, "federal revenue is $115.1 billion (Table 1 times Table 5's share)", fed_b == 115.1, f"{fed_b}")
    check(sid, "88 cents: the state and local shares together", round(v["2"] + v["3"]) == 88 and "88 cents" in t, f"{v['2'] + v['3']:.4f}")
    check(sid, "states named are NY and ID", sorted(s.get("states", [])) == ["ID", "NY"], f"{s.get('states')}")


def s91():
    sid, s = "S91", spec("S91")
    r = {x["order"]: x for x in rows("uscode-federal-trial-judges")}
    t = words(s)
    check(sid, "345 bankruptcy seats against the table's 316", int(r["2"]["seats"]) == 345 and int(r["2"]["seats_in_statute_table"]) == 316)
    has(sid, t, "except in Guam, the Northern Mariana Islands and the Virgin Islands", "the territorial judges' exception, the three territories named")
    has(sid, t, "full-time magistrate judges for eight", "the full-time magistrate term")
    check(sid, "677 district seats = 673 in the statute + 4 territorial", int(r["1"]["seats"]) == 677 and int(r["1"]["seats_in_statute_table"]) + int(r["1"]["seats_in_territorial_courts"]) == 677)
    check(sid, "a card field prints the seats column", any(f["field"] == "seats" for f in s["labels"]["fields"]))
    has(sid, t, "four", "the territorial courts' seats")
    check(sid, "345 bankruptcy judgeships", int(r["2"]["seats"]) == 345)
    check(sid, "593 magistrate judge positions", int(r["3"]["seats"]) == 593)
    check(sid, "14-year bankruptcy terms; 8 and 4 for magistrate judges", r["2"]["term"].startswith("14 years") and r["3"]["term"].startswith("8 years full time, 4 years part time"))
    check(sid, "seats counted September 30, 2025", all(x["seats_as_of"] == "2025-09-30" for x in r.values()))
    for word in ("Democrat", "Republican", "Biden", "Trump", "Obama", "Bush", "Clinton"):
        check(sid, f"no party or president: \"{word}\"", word not in t)


def s92():
    sid, s = "S92", spec("S92")
    r = {x["order"]: x for x in rows("govinfo-foia-request-steps")}
    t = words(s)
    check(sid, "20 working days and up to 10 more: row 5", r["5"]["time_limit"] == "20 working days, and up to 10 more in unusual circumstances")
    check(sid, "90 days to appeal, 20 working days to decide: row 6", r["6"]["time_limit"] == "At least 90 days to appeal; the agency decides within 20 working days")
    check(sid, "10 days to decide on expediting: row 4", r["4"]["time_limit"] == "The agency decides whether to expedite within 10 days")
    check(sid, "two hours and 100 pages free: row 3", "first two hours of search and the first 100 pages free" in r["3"]["what_happens"])
    has(sid, t, "20 working days", "the agency's limit to decide")
    check(sid, "two optional steps, rows 4 and 7", [k for k, x in r.items() if x["path"] == "branch"] == ["4", "7"])


def s93():
    sid, s = "S93", spec("S93")
    r = {x["order"]: x for x in rows("govinfo-pl-119-12-first-page")}
    keys = [str(b["key"]) for b in s["labels"]["layout"]]
    check(sid, "the page draws every part but the citation, which the running head holds", sorted(keys + ["4"], key=int) == sorted(r, key=int), f"{keys}")
    check(sid, "row 11's margin short title sits beside section 1 with row 10", [b.get("beside") for b in s["labels"]["layout"] if b["key"] in (10, 11)] == [9, 9])
    head = r["1"]["printed_text"].split("; ")
    check(sid, "the running head's last piece is the Statutes at Large citation", head[-1] == r["4"]["printed_text"], f"{head[-1]!r} {r['4']['printed_text']!r}")
    check(sid, "the running head's first piece is the Public Law number in capitals", head[0] == r["2"]["printed_text"].upper())
    for b in s["labels"]["layout"]:
        for br in b.get("breaks", []) + ([b["lead"]] if b.get("lead") else []):
            check(sid, f"row {b['key']} holds \"{br}\" where the page breaks a line", br in r[str(b["key"])]["printed_text"])
    # the drawing's words reach a screen reader through its table, which prints every part with its words as printed and
    # what it tells, in the order the parts sit on the page; the alt stays short (the accessibility lead, R4-3 item 5)
    cols = [c["field"] for c in s["table"]["columns"]]
    check(sid, "the table prints each part, its words as printed and what it tells", all(f in cols for f in ("part", "printed_text", "what_it_tells")), f"{cols}")
    order = [str(v) for v in s["sort"][0]["values"]]
    check(sid, "the parts read top to bottom: the citation beside the running head second, the margin short title (row 11) before the U.S. Code note (row 10)", order == ["1", "4", "2", "3", "7", "5", "6", "8", "9", "11", "10"])
    nums = s["table"]["columns"][0].get("words", {})
    check(sid, "the table's numbers match the drawing's: each part's place in that order", all(nums.get(k) == str(i + 1) for i, k in enumerate(order)))
    em = "—"
    check(sid, "no em dash in any word field", em not in json.dumps(s, ensure_ascii=False))


def s94():
    sid, s = "S94", spec("S94")
    rr = rows("govinfo-budget-and-tax-deadlines-2027")
    t = words(s)
    days = {x["date"] for x in rr}
    cons = [x for x in rr if not x["consequence"].startswith("None")]
    check(sid, "16 events on 13 days", len(rr) == 16 and len(days) == 13, f"{len(rr)} events, {len(days)} days")
    check(sid, "7 events carry a consequence in law and 9 do not", len(cons) == 7, f"{len(cons)}")
    for x in rr:
        d = datetime.date.fromisoformat(x["date"])
        check(sid, f"{x['date']} is a {x['weekday']}", d.strftime("%A") == x["weekday"])
    taxes = [x for x in rr if x["track"] == "tax"]
    check(sid, "no 2027 tax date falls on a weekend", all(datetime.date.fromisoformat(x["date"]).weekday() < 5 for x in taxes))
    check(sid, "no date moved under 26 U.S.C. 7503", all(x["moved_to_next_business_day"] == "false" for x in rr))
    check(sid, "May 15, 2027 is a Saturday", datetime.date(2027, 5, 15).strftime("%A") == "Saturday")
    both = sorted({x["date"] for x in rr if any(y["date"] == x["date"] and y["consequence"].startswith("None") for y in rr) and any(y["date"] == x["date"] and not y["consequence"].startswith("None") for y in rr)})
    check(sid, "April 15 and June 15 hold both kinds", both == ["2027-04-15", "2027-06-15"], f"{both}")
    check(sid, "six tax dates, and October 1 the seventh with a consequence", len(taxes) == 6 and all(not x["consequence"].startswith("None") for x in taxes) and [x["date"] for x in cons if x["track"] == "budget"] == ["2027-10-01"])
    has(sid, t, "16 deadlines on 13 days", "the count of deadlines and days")
    has(sid, t, "a consequence to seven: the six tax deadlines", "the deadlines with a consequence")
    check(sid, "the six tax deadlines fall on five days", len({x["date"] for x in taxes}) == 5)
    for n in re.findall(r"\b(\d+) (?:dates|events|days)\b", t):
        check(sid, f"a count the words print, {n}, is one the data gives", int(n) in (16, 13, 7, 9, 12), n)


def s95():
    sid, s = "S95", spec("S95")
    r = {x["code"]: x for x in rows("bjs-imprisonment-rate-by-state")}
    t = words(s)
    states = {k: v for k, v in r.items() if k not in ("US", "FED", "STATE")}
    rates = {k: float(v["rate_2023"]) for k, v in states.items()}
    hi, lo = max(rates, key=rates.get), min(rates, key=rates.get)
    check(sid, "50 states", len(states) == 50, f"{len(states)}")
    check(sid, "Mississippi the highest at 652", hi == "MS" and round(rates[hi]) == 652)
    check(sid, "Massachusetts the lowest at 96", lo == "MA" and round(rates[lo]) == 96)
    check(sid, "all states together 318", round(float(r["STATE"]["rate_2023"])) == 318)
    has(sid, t, "652", "Mississippi's rate")
    has(sid, t, "96", "Massachusetts's rate")


CHECKS = {"S89": s89, "S90": s90, "S91": s91, "S92": s92, "S93": s93, "S94": s94, "S95": s95}

if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--specs" in argv:   # read specs from another folder first (a maker's scratch, before they land)
        i = argv.index("--specs")
        SPECS = Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if a != "--figures"]
    if "--figures" not in sys.argv:
        print(__doc__)
        sys.exit(2)
    for sid in [a.upper() for a in args] or list(CHECKS):
        if not (SPECS / f"{sid.lower()}.json").exists():
            print(f"SKIP {sid}: no spec yet")
            continue
        CHECKS[sid]()
    print(f"{len(FAILS)} failed" if FAILS else "all passed")
    sys.exit(1 if FAILS else 0)
