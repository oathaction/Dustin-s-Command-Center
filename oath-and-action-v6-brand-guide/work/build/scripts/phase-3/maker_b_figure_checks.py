"""Maker B's figure checks (Phase 3, round 1): figures typed into a spec's words, read back against the frozen data.

    python3 -I work/build/scripts/phase-3/maker_b_figure_checks.py

Exits 1 when a typed figure no longer matches its data file, so a data refresh (Phase 5) cannot leave one stale.
Check 1, S13: the federal government's peak label, labels.totals[3].peak, against fred-payrolls-by-sector-change.csv:
the month of the highest pct_change_since_2022_01 for CES9091000001 must also hold its highest employees_thousands,
and that level, in thousands, must print as the label's figure.
Check 2, S05: each gap bracket's figure and note 1's two changes against the homeownership and gap-margin files.
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

for f in faults:
    print("FAIL", f)
print(f"maker_b_figure_checks: 2 checks, {len(faults)} fault(s)")
sys.exit(1 if faults else 0)
