"""C1's measure (DR-331): the two pages run.sh built from one tree, C1 off and on, read from their build reports.

  python3 -I measure.py OFF-Build-Report.json ON-Build-Report.json [--md OUT.md]

Prints the page's bytes both ways, each chapter's and each part's, what C1's steps took, the projection both ways and the
forecast beside it, as a Markdown table.
"""
import json
import sys
from pathlib import Path


def main():
    off = json.loads(Path(sys.argv[1]).read_text())
    on = json.loads(Path(sys.argv[2]).read_text())
    wo, wn = off["weight"], on["weight"]
    L = []
    L.append(f"| | C1 off | C1 on | Saved |")
    L.append("|---|---|---|---|")
    L.append(f"| The page | {off['bytes']:,} | {on['bytes']:,} | {off['bytes'] - on['bytes']:,} |")
    for n in sorted(set(wo["chapters"]) | set(wn["chapters"])):
        a, b = wo["chapters"].get(n, {}).get("bytes", 0), wn["chapters"].get(n, {}).get("bytes", 0)
        L.append(f"| Chapter {n} | {a:,} | {b:,} | {a - b:,} |")
    for k in sorted(set(wo["parts"]) | set(wn["parts"])):
        a, b = wo["parts"].get(k, 0), wn["parts"].get(k, 0)
        L.append(f"| Part: {k} | {a:,} | {b:,} | {a - b:,} |")
    po, pn = wo["projection"], wn["projection"]
    L.append(f"| Projection, as the build computes it | {po['projected_bytes']:,} | {pn['projected_bytes']:,} | {po['projected_bytes'] - pn['projected_bytes']:,} |")
    L.append(f"| Held to allocation | {po['held_to_allocation']} | {pn['held_to_allocation']} | |")
    c1 = wn.get("c1") or {}
    steps = "; ".join(f"{s} {c1[s]['bytes_saved']:,}" for s in ("3a", "3b", "3c", "3d") if s in c1)
    out = "\n".join(L) + f"\n\nC1's steps on this page: {steps}; in all {c1.get('bytes_saved', 0):,}.\n"
    for label, w in (("C1 off", wo), ("C1 on", wn)):
        fc = w.get("forecast")
        if fc:
            t, p = fc["totals"], fc["projection_with_forecast"]
            out += (f"\n{label}, 1b's forecast: chapters 22 to 25, 27 and 28 low {t['low']:,}, mid {t['mid']:,}, high {t['high']:,} against "
                    f"{fc['allocated']:,} allocated; the projection with them low {p['low']:,}, mid {p['mid']:,}, high {p['high']:,}; mid by chapter "
                    + ", ".join(f"{n} {fc['chapters'][n]['mid']:,}" for n in ("22", "23", "24", "25", "27", "28")) + ".\n")
    print(out)
    if "--md" in sys.argv:
        Path(sys.argv[sys.argv.index("--md") + 1]).write_text(out)


if __name__ == "__main__":
    main()
