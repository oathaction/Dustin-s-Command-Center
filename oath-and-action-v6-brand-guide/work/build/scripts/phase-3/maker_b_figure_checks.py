"""Maker B's figure checks (Phase 3, round 1): figures typed into a spec's words, read back against the frozen data.

    python3 -I work/build/scripts/phase-3/maker_b_figure_checks.py

Exits 1 when a typed figure no longer matches its data file, so a data refresh (Phase 5) cannot leave one stale.
Check 1, S13: the federal government's peak label, labels.totals[3].peak, against fred-payrolls-by-sector-change.csv:
the month of the highest pct_change_since_2022_01 for CES9091000001 must also hold its highest employees_thousands,
and that level, in thousands, must print as the label's figure.
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

for f in faults:
    print("FAIL", f)
print(f"maker_b_figure_checks: {1 - len(faults) and 1} check, {len(faults)} fault(s)" if False else f"maker_b_figure_checks: 1 check, {len(faults)} fault(s)")
sys.exit(1 if faults else 0)
