"""Maker B's figure checks (Phase 3, round 1): figures typed into a spec's words, read back against the frozen data.

    python3 -I work/build/scripts/phase-3/maker_b_figure_checks.py

Exits 1 when a typed figure no longer matches its data file, so a data refresh (Phase 5) cannot leave one stale.
Check 1, S13: the federal government's peak label, labels.totals[3].peak, against fred-payrolls-by-sector-change.csv:
the month of the highest pct_change_since_2022_01 for CES9091000001 must also hold its highest employees_thousands,
and that level, in thousands, must print as the label's figure.
Check 2, S05: each gap bracket's figure and note 1's two changes against the homeownership and gap-margin files.
Checks 3 to 9 (round 1 review fix pass): every figure the fix pass printed or kept in S24, S25, S26, S27, S31, S33 and S34,
read from the spec's words (title, notes, alt, chart notes, measure line) and computed from the frozen data file.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
faults = []

spec = json.loads((ROOT / "work/build/chart-kit/specs/s13.json").read_text(encoding="utf-8"))
label = next(t for t in spec["labels"]["totals"] if t["value"] == "CES9091000001")["peak"]
rows = [r for r in csv.DictReader(open(ROOT / "work/build/data/fred-payrolls-by-sector-change.csv", encoding="utf-8"))
        if r["series_id"] == "CES9091000001"]
by_pct = max(rows, key=lambda r: float(r["pct_change_since_2022_01"]))
by_level = max(rows, key=lambda r: float(r["employees_thousands"]))
want = f"{round(float(by_level['employees_thousands']) * 1000):,}"
got = re.search(r"[\d,]{5,}", label)
if by_pct["month"] != by_level["month"]:
    faults.append(f"S13: the peak by percent ({by_pct['month']}) and by level ({by_level['month']}) differ")
if not got or got.group(0) != want:
    faults.append(f"S13: the peak label prints {got.group(0) if got else 'no figure'}, the data gives {want} in {by_level['month']}")

# Check 2, S05: each gap bracket's figure against census-hvs-homeownership-by-race-annual.csv (standard rows), and the
# changes note 1 states (2.3 and 2.9 points) against the gap-margin file's 90 percent margins, combined
import math
s05 = json.loads((ROOT / "work/build/chart-kit/specs/s05.json").read_text(encoding="utf-8"))
rate = {(r["year"], r["group"]): float(r["rate_pct"]) for r in csv.DictReader(open(ROOT / "work/build/data/census-hvs-homeownership-by-race-annual.csv", encoding="utf-8"))
        if r["series_variant"] == "standard"}
for a in s05.get("annotations", []):
    y = str(a["at"]["x"]); want = f"{rate[(y, a['to_series'])] - rate[(y, a['panel'])]:.1f}"
    if a["text"] != want:
        faults.append(f"S05: the {a['panel']} bracket at {y} prints {a['text']}, the data gives {want}")
moe = {(r["year"], r["row"]): float(r["moe_90"]) for r in csv.DictReader(open(ROOT / "work/build/data/census-hvs-homeownership-gap-moe.csv", encoding="utf-8"))}
for g, said in (("black", "2.3"), ("hispanic", "2.9")):
    change = abs((rate[("2025", "non_hispanic_white")] - rate[("2025", g)]) - (rate[("2003", "non_hispanic_white")] - rate[("2003", g)]))
    m = math.sqrt(sum(moe[(y, k)] ** 2 for y in ("2003", "2025") for k in ("non_hispanic_white", g)))
    if f"{change:.1f}" != said or said not in s05["notes"][0] or change <= m:
        faults.append(f"S05: the {g} gap changed by {change:.1f} points against a margin of {m:.2f}; note 1 says {said}")

# ---- Checks 3 to 9, round 1 review fix pass ------------------------------------------------------------------------
def spec(sid):
    return json.loads((ROOT / f"work/build/chart-kit/specs/{sid}.json").read_text(encoding="utf-8"))
def words(d):
    """every reader word of a spec, joined: title, measure line, reading guide, notes, chart notes, alt, phone note"""
    out = [d.get(k) or "" for k in ("title", "measure_line", "reading_guide", "alt", "phone_note", "source_line")]
    out += d.get("notes", []) + d.get("chart_notes", [])
    return "\n".join(out)
def rows(name):
    return list(csv.DictReader(open(ROOT / f"work/build/data/{name}.csv", encoding="utf-8")))
def need(sid, text, *figs):
    for x in figs:
        if x not in text:
            faults.append(f"{sid}: the words should print {x!r}, which the data gives")

# Check 3, S24: the national rise, Wyoming's rise and counts, the order behind it and the smallest rise
d = spec("s24"); t = words(d)
bfs = {r["code"]: r for r in rows("census-bfs-business-applications-change-by-state")}
pct = {k: float(r["change_pct"]) for k, r in bfs.items()}
states = {k: v for k, v in pct.items() if k != "US"}
top = sorted(states, key=states.get, reverse=True)
if top[0] != "WY" or min(states.values()) <= 0 or min(states, key=states.get) != "DC":
    faults.append("S24: Wyoming is not the largest rise, a state fell, or DC is not the smallest")
wy = bfs["WY"]; ratio = int(wy["applications_2025"]) / int(wy["applications_2019"])
if not 4 <= ratio < 4.5:
    faults.append(f"S24: Wyoming's 2025 count is {ratio:.2f} times 2019, which 'quadrupled' does not fit")
need("S24", t, f"by {round(pct['US'])} percent nationwide", f"{int(wy['applications_2019']):,}", f"{int(wy['applications_2025']):,}",
     f"+{round(pct['WY'])}%", f"{round(pct[top[1]])} and {round(pct[top[2]])} percent", f"{round(pct['DC'])} percent")
if [bfs[top[1]]["name"], bfs[top[2]]["name"]] != ["New Mexico", "Delaware"]:
    faults.append("S24: the alt text names New Mexico and Delaware second and third, the data does not")

# Check 4, S25: the net change, the shrinking count, the January 2025 spans and the alt's figures
d = spec("s25"); t = words(d)
opm = {r["department_code"]: r for r in rows("opm-federal-employment-by-agency")}
a = opm["ALL"]; n22, n25, n26 = int(a["employees_2022_01"]), int(a["employees_2025_01"]), int(a["employees_2026_08"])
big = [r for k, r in opm.items() if k != "ALL" and r["size_1000_plus"] == "true"]
largest = sorted((r for k, r in opm.items() if k != "ALL"), key=lambda r: -int(r["employees_2022_01"]))[:len(big)]
if {r["department_code"] for r in big} != {r["department_code"] for r in largest}:
    faults.append("S25: the agencies drawn are not the largest in January 2022")
shrank = sum(1 for r in big if int(r["change"]) < 0)
need("S25", t, f"{n22 - n26:,} fewer", f"{shrank} of the {len(big)} largest", f"{n25:,} employees", f"{n25 - n22:,} more than in January 2022",
     f"{n25 - n26:,} more than in August 2026", f"{-int(opm['DOD']['change']):,}", f"Veterans Affairs {int(opm['VA']['change']):,}",
     f"Homeland Security {int(opm['HS']['change']):,}", f"Interior {int(opm['IN']['change'])}", f"Government Publishing Office {int(opm['LP']['change'])}",
     f"{100 * sum(int(r['employees_2022_01']) for r in big) / n22:.1f} percent", f"all {len(opm) - 1} agencies")
if (n25 - n22) + (n26 - n25) != n26 - n22 or int(a["change_2022_01_to_2025_01"]) != n25 - n22 or int(a["change_2025_01_to_2026_08"]) != n26 - n25:
    faults.append("S25: the two spans do not sum to the window's change")

# Check 5, S26: the title's lead, the record since 1951, the majorities and changes of control, the largest lead
d = spec("s26"); t = words(d)
hh = sorted(rows("house-history-party-divisions"), key=lambda r: int(r["congress"]))
lead = {int(r["congress"]): int(r["majority_advantage_seats"]) for r in hh}
if lead[119] != 5 or any(v <= 5 for k, v in lead.items() if k != 119) or int(hh[0]["first_year"]) != 1951:
    faults.append("S26: the 119th's lead is not 5, or another Congress since 1951 led by as little")
if int(next(r for r in hh if int(r["congress"]) == 119)["republicans"]) - int(next(r for r in hh if int(r["congress"]) == 119)["democrats"]) != 5:
    faults.append("S26: Republicans did not win five more seats than Democrats in the 119th's first count")
dem = sum(1 for r in hh if r["majority_party"] == "Democrats"); rep = len(hh) - dem
flips = sum(1 for p, q in zip(hh, hh[1:]) if p["majority_party"] != q["majority_party"])
mx = max(hh, key=lambda r: int(r["majority_advantage_seats"]))
need("S26", t, "five more House seats", f"for {dem} of the {len(hh)} Congresses and Republicans for {rep}", "seven times" if flips == 7 else f"{flips} times",
     f"{mx['majority_advantage_seats']} seats, for Democrats in the {mx['congress']}th Congress, which opened in {mx['first_year']}")

# Check 6, S27: the two highest states, each more than seven times early 1991, the nation, the lowest
d = spec("s27"); t = words(d)
fh = [r for r in rows("fhfa-house-price-index-by-state") if r["quarter"] == "2" and r["year"] == "2026"]
v = {r["code"]: float(r["index_sa"]) for r in fh}
st = {k: x for k, x in v.items() if k != "US"}
hi2 = sorted(st, key=st.get, reverse=True)[:2]
if set(hi2) != {"MT", "UT"} or min(st[k] for k in hi2) <= 700 or min(st, key=st.get) != "CT" or min(st.values()) <= 100:
    faults.append("S27: Montana and Utah are not the two highest above 700, or Connecticut is not the lowest above 100")
need("S27", t, "most in Montana and Utah, each more than seven times", f"Montana, {round(v['MT'])}", f"Utah, {round(v['UT'])}",
     f"{round(v['MT'])} and {round(v['UT'])}", f"United States, {round(v['US'])}", f"reached {round(v['US'])}", f"to {round(v['CT'])}")

# Check 7, S31: the low, the high after the gap, the rise against the monthly interval, the latest rate, the gap
d = spec("s31"); t = words(d)
un = {r["month"]: r["unemployment_rate"] for r in rows("fred-unemployment-and-job-openings") if "2022-01" <= r["month"] <= "2026-10"}
vals = {k: float(x) for k, x in un.items() if x}
lo = min(vals, key=vals.get); rise = vals["2025-11"] - vals[lo]
moe = re.search(r"plus or minus ([\d.]+) point", json.loads((ROOT / "work/build/data/fred-unemployment-and-job-openings.meta.json").read_text(encoding="utf-8"))["source_line_variants"]["with_margin"])
if un.get("2025-10") or lo != "2023-04" or not moe or not 3 < rise / float(moe.group(1)) < 4:
    faults.append("S31: October 2025 holds a rate, the low is not April 2023, or the rise is not more than three times the interval")
need("S31", t, f"{vals[lo]:.1f} percent in April 2023", f"{vals['2025-11']:.1f} percent in November 2025", f"{rise:.1f} points",
     f"{vals['2026-10']:.1f} percent in October 2026")
need("S31", "\n".join(d["notes"]), f"plus or minus {moe.group(1) if moe else '?'} point", "more than three times")   # the note, apart from the source line

# Check 8, S33: customs duties' index and its peak, all receipts, the dollars and the share
d = spec("s33"); t = words(d)
mts = {}
for r in rows("treasury-mts-receipts-by-source"):
    mts.setdefault(r["source"], {})[int(r["fiscal_year"])] = float(r["receipts_dollars"])
ix = {k: {y: x / s_[2016] * 100 for y, x in s_.items() if 2016 <= y <= 2026} for k, s_ in mts.items()}
if max(ix, key=lambda k: ix[k][2026]) != "Customs Duties":
    faults.append("S33: customs duties is not the highest index in 2026")
cu, tot = mts["Customs Duties"], mts["Total"]
need("S33", t, f"to {round(ix['Customs Duties'][2026])} in 2026", f"peak of {round(max(ix['Customs Duties'].values()))} in 2025",
     f"reached {round(ix['Total'][2026])}", f"${cu[2016] / 1e9:.1f} billion", f"${cu[2026] / 1e9:.1f} billion", f"{100 * cu[2026] / tot[2026]:.1f} percent",
     f"${tot[2016] / 1e9:,.1f} billion", f"${tot[2026] / 1e9:,.1f} billion", f"fell to {round(ix['Miscellaneous Receipts'][2026])} percent")
if not 4.9 < ix["Customs Duties"][2026] / 100 < 5:
    faults.append("S33: 'almost five times' does not fit customs duties' 2026 index")

# Check 9, S34: the most votes, the Congress still in session and its date, the Congresses before 1971
d = spec("s34"); t = words(d)
sc = rows("senate-cloture-motions-by-congress")
mx = max(sc, key=lambda r: int(r["votes_on_cloture"])); cur = next(r for r in sc if r["complete"] == "false")
early = [r for r in sc if int(r["first_year"]) < 1971]
dated = "through November 10, 2026" in json.loads((ROOT / "work/build/data/senate-cloture-motions-by-congress.meta.json").read_text(encoding="utf-8"))["printed_source_line"]
if mx["congress"] != "116" or not dated:
    faults.append("S34: the 116th does not hold the most votes, or the sidecar's line does not carry the date note 3 prints")
need("S34", t, f"{mx['votes_on_cloture']} votes to end debate in 2019 and 2020", f"its {cur['votes_on_cloture']} votes through November 10, 2026",
     f"held {cur['votes_on_cloture']} through November 10, 2026", f"the {len(early)} Congresses from 1917 to 1970, {sum(int(r['votes_on_cloture']) for r in early)} votes",
     "no more than seven" if max(int(r["votes_on_cloture"]) for r in early) == 7 else "no more than ?")

for f in faults:
    print("FAIL", f)
print(f"maker_b_figure_checks: 9 checks, {len(faults)} fault(s)")
sys.exit(1 if faults else 0)
