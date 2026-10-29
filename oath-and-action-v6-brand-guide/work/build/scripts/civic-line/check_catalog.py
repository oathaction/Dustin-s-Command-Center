"""Check the catalog page: axe-core 4.10.2 at 1440 and 390 px in light and dark,
horizontal scroll, screenshots into qa/catalog-screens/, and the controls.

    python3 -I check_catalog.py

Writes qa/catalog-screens/<date>_Catalog-Check.json and prints one line per
check. Exit code 1 if any check fails.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
from build_catalog import OUT as CATALOG  # noqa: E402

SCREENS = os.path.join(C.QA, "catalog-screens")
AXE = os.path.join(C.ROOT, "work", "build", "node_modules", "axe-core", "axe.min.js")
REPORT = os.path.join(SCREENS, f"{C.DATE}_Catalog-Check.json")


def main():
    os.makedirs(SCREENS, exist_ok=True)
    r = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_catalog.js"),
                        CATALOG, SCREENS, AXE], capture_output=True, text=True, timeout=900)
    if r.returncode:
        raise SystemExit("check_catalog.js failed:\n" + r.stderr[-3000:])
    raw = os.path.join(SCREENS, "check.json")
    res = json.load(open(raw))
    os.replace(raw, REPORT)
    checks = []

    def ck(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
    ck("file under 12 MB", res["bytes"] < 12 * 1024 * 1024, f"{res['bytes'] / 1024 / 1024:.2f} MB")
    for run in res["runs"]:
        t = run["tag"]
        v = run["axe"]["violations"]
        vd = run["axeDetail"]["violations"]
        ck(f"{t}: axe {run['axe']['version']} on the grid, no violations", not v, "; ".join(f"{x['id']} ({x['impact']}, {x['nodes']})" for x in v))
        ck(f"{t}: axe on the open detail view, no violations", not vd, "; ".join(f"{x['id']} ({x['impact']}, {x['nodes']})" for x in vd))
        ck(f"{t}: no horizontal scroll", run["scroll"]["docScroll"] <= 0 and run["scroll"]["bodyScroll"] <= 0
           and run["scrollDetail"]["docScroll"] <= 0, json.dumps(run["scroll"]))
        ck(f"{t}: opens with all 122 cards visible", run["info"]["cards"] == 122, str(run["info"]["cards"]))
        ck(f"{t}: icon tiles are Newsprint", run["info"]["tileBg"] == "rgb(220, 217, 210)", run["info"]["tileBg"])
        d = run["detail"]
        ck(f"{t}: detail shows the reference crop and the trace at one scale",
           d["imgShown"] == d["svgShown"] and d["imgNatural"][0] > 0, f"img {d['imgShown']} svg {d['svgShown']}, natural {d['imgNatural']}")
        ck(f"{t}: Escape closes the detail view and focus returns to its card",
           not run["afterClose"]["open"] and run["afterClose"]["focus"] == "R-35", json.dumps(run["afterClose"]))
        ck(f"{t}: no script errors", not run["errors"], "; ".join(run["errors"])[:200])
        ck(f"{t}: Inter Tight available", run["info"]["interTight"], ", ".join(run["info"]["fontsLoaded"])[:160])
    F = res["functional"]
    ck("search 'term limits' finds R-35 only", F["searchTermLimits"] == ["R-35"], str(F["searchTermLimits"]))
    ck("search 'r-35' finds R-35 only", F["searchR35"] == ["R-35"], str(F["searchR35"]))
    ck("search 'cl-021' finds CL-021 only", F["searchCL021"] == ["CL-021"], str(F["searchCL021"]))
    ck("no match shows the empty state", F["emptyState"]["visible"] == 0 and F["emptyState"]["emptyShown"], F["emptyState"]["text"])
    ck("sheet filter 04 shows 25", F["sheet04"]["visible"] == 25, F["sheet04"]["count"])
    ck("edition toggle: accent Pillar Red, then Charcoal", F["accentRedBlack"] == "rgb(230, 57, 70)" and F["accentBlack"] == "rgb(18, 18, 18)",
       f"{F['accentRedBlack']} then {F['accentBlack']}")
    ck("size control: 128 and 24 px", round(F["size128"]) == 128 and round(F["size24"]) == 24, f"{F['size128']}, {F['size24']}")
    ck("first Tab reaches the search field with a visible outline", F["firstTab"]["id"] == "q" and F["firstTab"]["outline"] != "none",
       json.dumps(F["firstTab"]))
    ck("keyboard order: search, edition, sheet, size, then the first card, which shows a focus outline",
       F["tabOrder"] == ["ed-rb", "sheet", "size", "CL-001"] and F["cardFocus"]["card"] == "CL-001" and F["cardFocus"]["outline"] != "none",
       f"{F['tabOrder']}, {json.dumps(F['cardFocus'])}")
    ck("Enter opens the detail view; Next steps on; Escape closes", bool(F["enterOpens"]) and F["nextGoesTo"].startswith("CL-002")
       and F["escapeCloses"], f"{F['enterOpens']} -> {F['nextGoesTo']}, hash {F['hash']}")
    ck("a #r-35 link opens R-35", F["hashOpens"] and F["hashOpens"].startswith("R-35"), str(F["hashOpens"]))
    ck("data-theme dark wins over a light OS", F["os-light-theme-dark"]["bg"] == "rgb(18, 18, 18)", json.dumps(F["os-light-theme-dark"]))
    ck("data-theme light wins over a dark OS", F["os-dark-theme-light"]["bg"] == "rgb(255, 255, 255)", json.dumps(F["os-dark-theme-light"]))
    ck("reduced motion removes the tile transition", F["reducedMotionTransition"] == "0s",
       f"reduce {F['reducedMotionTransition']}, normal {F['normalMotionTransition']}")
    ck("page works when localStorage throws", F["storageBlocked"] == 122 and F["storageBlockedEditionWorks"] == "black"
       and not F["storageBlockedErrors"], str(F["storageBlockedErrors"])[:160])
    ck("no external request failed", not res.get("failedRequests"), "; ".join(res.get("failedRequests", []))[:200])
    res["checks"] = checks
    C.write_json(REPORT, res)
    for c in checks:
        print(("PASS " if c["pass"] else "FAIL ") + c["check"] + (f"  [{c['detail']}]" if c["detail"] else ""))
    n = sum(1 for c in checks if not c["pass"])
    print(f"{len(checks) - n} passed, {n} failed. Screens: {os.path.relpath(SCREENS, C.ROOT)}")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
