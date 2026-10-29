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
        ck(f"{t}: detail shows the 4 editions, Newsprint on Prussian and 12 tiles at 96 px", d["specimens"] == 17 and d["specSizes"] == [96]
           and d["prussian"] == "rgb(31, 45, 90)", f"{d['specimens']} specimens, sizes {d['specSizes']}, Prussian stage {d['prussian']}, first tile stages {d['tileStages']}")
        ck(f"{t}: no id repeats on the page, grid and open detail view", run["info"]["dupIds"] == 0 and d["dupIds"] == 0,
           f"{run['info']['dupIds']} on the grid, {d['dupIds']} with the detail open")
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
    RED, CH, NW = "rgb(230, 57, 70)", "rgb(18, 18, 18)", "rgb(220, 217, 210)"
    want = {"red-black": (RED, CH, NW), "black": (CH, CH, NW), "red-newsprint": (RED, NW, CH), "newsprint": (NW, NW, CH)}
    for ed, (acc, ink, tile) in want.items():
        got = F["editions"][ed]
        ck(f"edition {ed}: accent, ink and tile colors", (got["accent"], got["ink"], got["tile"]) == (acc, ink, tile), json.dumps(got))
    base_w = F["holderNone"]["w"]
    a21 = C.TILE_OPTICAL_SCALE.get("CL-021", 1.0)
    a10, dx10 = C.TILE_OPTICAL_SCALE.get("CL-010", 1.0), C.TILE_OFFSET_X.get("CL-010", 0.0)
    _, _, k22 = C.tile_optics("CL-022", C.inventory_by_id()["CL-022"]["stroke_units"])
    for h in C.TILE_SHAPES:
        fac = C.TILE_FACTORS[h]
        g = F["holders"][h]
        ck(f"holder {h}: shape shown, CL-021 at {fac} times its optical scale {a21}, Charcoal tile on a Newsprint stage",
           g["shown"] == [f"#h-{h}"] and abs(g["w"] / base_w - fac * a21) < 0.005 and g["fill"] == CH and g["stage"] == NW,
           f"shown {g['shown']}, scale {g['w'] / base_w:.4f} against {fac * a21:.4f}, fill {g['fill']}, stage {g['stage']}")
        nums = [float(v) for v in g["cl010"].replace("matrix(", "").replace(")", "").split(",")] if g["cl010"].startswith("matrix(") else []
        want = [fac * a10, 0, 0, fac * a10, fac * dx10, 0]
        ck(f"holder {h}: CL-010 scaled by {fac} times {a10} and moved {fac * dx10:.3f} units right, as its tile files",
           len(nums) == 6 and all(abs(x - y) < 1e-3 for x, y in zip(nums, want)), f"{g['cl010']} against {[round(v, 4) for v in want]}")
        ck(f"holder {h}: CL-022 stroke held at the cap ({3.3508 * k22:.4f} px in the 128 box)", abs(g["cl022Stroke"] - 3.3508 * k22) < 2e-3,
           f"{g['cl022Stroke']}")
    s21 = F["detailTileStrokesCL021"]
    s22 = F["detailTileStrokesCL022"]
    ck("detail tiles draw their strokes as the tile files do (CL-021 3.3508, CL-022 held at the cap)",
       s21 and all(abs(v - 3.3508) < 2e-3 for v in s21) and s22 and all(abs(v - 3.3508 * k22) < 2e-3 for v in s22),
       f"CL-021 {s21}, CL-022 {s22}")
    ck("holder None: CL-022 stroke at its bare width", abs(F["holderNone"]["cl022Stroke"] - 3.3508) < 2e-3, str(F["holderNone"]["cl022Stroke"]))
    M = F["minMarks"]
    n48 = len(C.BARE_FLOOR_48_IDS)
    ck("tile minimum: every two-color rounded tile at 24 px is marked", M["rbRounded24"]["n"] == 122 and M["rbRounded24"]["notes"] == 122,
       f"{M['rbRounded24']['n']} marked, note '{M['rbRounded24']['sample']}'")
    ck("tile minimum: no tile at 128 px is marked", M["rbRounded128"]["n"] == 0, str(M["rbRounded128"]["n"]))
    ck(f"tile minimum: one-color square tiles at 64 px mark the {n48} icons that need 72 px", M["bkSquare64"]["n"] == n48
       and set(M["bkSquare64"]["ids"]) == set(C.BARE_FLOOR_48_IDS), f"{M['bkSquare64']['n']} marked")
    ck("tile minimum: no card is marked without a holder", M["none24"]["n"] == 0, str(M["none24"]["n"]))
    L = F["labels"]
    ck("card labels never break inside a word or overflow, at 1440, 1024, 390 and 360 px and all five sizes",
       all(not x["broken"] and not x["over"] for x in L),
       "; ".join(f"{x['width']}/{x['size']}: {x['broken'][:3]} {x['over'][:3]}" for x in L if x["broken"] or x["over"])[:300])
    ck("no horizontal scroll at 1440, 1024, 390 and 360 px, and no control label wraps inside its segment",
       all(x["scroll"]["docScroll"] <= 0 and all(not g["wrapped"] for g in x["seg"]) for x in L),
       "; ".join(f"{x['width']}: scroll {x['scroll']['docScroll']}, wrapped {[g['wrapped'] for g in x['seg'] if g['wrapped']]}"
                 for x in L if x["scroll"]["docScroll"] > 0 or any(g["wrapped"] for g in x["seg"]))[:300])
    ck("R-35's middle dot stays with 'Rejected' and starts the second line when the label wraps",
       all(x["r35"]["dotWithRejected"] and (not x["r35"]["wraps"] or x["r35"]["dotStartsLine2"]) for x in L),
       "; ".join(f"{x['width']}/{x['size']} card {x['r35']['cardWidth']} px wraps {x['r35']['wraps']}" for x in L if x["r35"]["wraps"])[:300])
    g = F["holderRoundedRedBlack"]
    ck("holder with a dark edition: Newsprint tile on a Charcoal stage", g["fill"] == NW and g["stage"] == CH, json.dumps(g))
    ck("holder None hides every shape", F["holderNone"]["shown"] == [], str(F["holderNone"]["shown"]))
    ck("size control: 128 and 24 px", round(F["size128"]) == 128 and round(F["size24"]) == 24, f"{F['size128']}, {F['size24']}")
    ck("first Tab reaches the search field with a visible outline", F["firstTab"]["id"] == "q" and F["firstTab"]["outline"] != "none",
       json.dumps(F["firstTab"]))
    ck("keyboard order: search, edition, holder, sheet, size, then the first card, which shows a focus outline",
       F["tabOrder"] == ["ed-rb", "ho-none", "sheet", "size", "CL-001"] and F["cardFocus"]["card"] == "CL-001" and F["cardFocus"]["outline"] != "none",
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
