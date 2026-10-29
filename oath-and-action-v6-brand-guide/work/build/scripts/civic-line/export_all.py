"""Rebuild and export the whole Civic Line set in one command.

    python3 -I export_all.py [--keep-going]

Runs, in order:
   1. apply_framing.py            DR-08 capped fit into the inventory, with export and tile names
   2. build_all.py                every icon: four bare editions as SVG and PNG, QA images, metrics
   3. build_tiles.py              DR-10 tiles: 1,464 SVGs and 2,928 PNGs, ink margins
   4. check_inline_ids.py         the inline-id test in Chromium (M-2) for every masked icon
   5. contact_sheets.py           ten dark and ten light contact sheets, sheet compares
   6. tile_sheets.py              twelve tile overview sheets
   7. tile_calibration.py         the tile factor calibration board
   8. record_sheets.py            pillar side by side (DR-04) and the size ladder
   9. build_catalog.py            the catalog page
  10. check_catalog.py            axe-core, scroll, screenshots and controls on the page
  11. verify_set.py --sync-inventory   editions, tiles, ids, sheets, counts, contrast, ledger
  12. write_fidelity.py           the fidelity metrics CSV
  13. tests/civic-line/test_pipeline.py   the pipeline tests, in a temporary tree
  14. make_package.py             the final package in deliverables/
It stops at the first failing step unless --keep-going is given, and prints a
summary with each step's exit code. It never edits src/ or the status files.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.abspath(os.path.join(HERE, "..", "..", "tests", "civic-line", "test_pipeline.py"))
STEPS = [["apply_framing.py"], ["build_all.py"], ["build_tiles.py"], ["check_inline_ids.py"], ["contact_sheets.py"], ["tile_sheets.py"],
         ["tile_calibration.py"], ["record_sheets.py"], ["build_catalog.py"], ["check_catalog.py"],
         ["verify_set.py", "--sync-inventory"], ["write_fidelity.py"], [TESTS], ["make_package.py"]]


def main():
    keep = "--keep-going" in sys.argv
    summary = []
    for step in STEPS:
        t = time.time()
        script = step[0] if os.path.isabs(step[0]) else os.path.join(HERE, step[0])
        name = " ".join([os.path.basename(step[0])] + step[1:])
        print(f"\n=== {name} ===", flush=True)
        r = subprocess.run([sys.executable, "-I", script] + step[1:], cwd=HERE)
        summary.append((name, r.returncode, time.time() - t))
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
