"""Rebuild and export the whole Civic Line set in one command.

    python3 -I export_all.py [--keep-going]

Runs, in order:
  1. build_all.py               every icon with a source: exports, PNGs, QA, metrics
  2. contact_sheets.py          ten contact sheets and the sheet-compare images
  3. record_sheets.py           pillar side by side (DR-04) and the size ladder
  4. build_catalog.py           the catalog page
  5. check_catalog.py           axe-core, scroll, screenshots and controls on the page
  6. verify_set.py --sync-inventory   set checks, edition trees, counts, ledger
  7. write_fidelity.py          the fidelity metrics CSV
  8. make_package.py            the review zip
It stops at the first failing step unless --keep-going is given, and prints a
summary with each step's exit code. It never edits src/ or the status files.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [["build_all.py"], ["contact_sheets.py"], ["record_sheets.py"], ["build_catalog.py"], ["check_catalog.py"],
         ["verify_set.py", "--sync-inventory"], ["write_fidelity.py"], ["make_package.py"]]


def main():
    keep = "--keep-going" in sys.argv
    summary = []
    for step in STEPS:
        t = time.time()
        print(f"\n=== {' '.join(step)} ===", flush=True)
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, step[0])] + step[1:], cwd=HERE)
        summary.append((" ".join(step), r.returncode, time.time() - t))
        if r.returncode and not keep:
            break
    print("\n=== summary ===")
    for name, code, secs in summary:
        print(f"{'ok  ' if code == 0 else 'FAIL'} {name}  ({secs:.0f} s, exit {code})")
    if len(summary) < len(STEPS):
        print("stopped early; rerun with --keep-going to run the remaining steps anyway")
    sys.exit(1 if any(c for _, c, _ in summary) or len(summary) < len(STEPS) else 0)


if __name__ == "__main__":
    main()
