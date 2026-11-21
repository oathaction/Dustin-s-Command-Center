"""Color by screen on a long page (chat 11, contract C5; DR-310, Rule 05.1's second paragraph).

Rule 05.1: every view keeps three limits, Newsprint over 60 to 85 percent of it, one dark panel at most in each section (in
Charcoal or Prussian), and Pillar Red within 5 percent, signature red included. DR-310: on a long page the limits hold for
the first screen and for each section's opening screen; screens of running text between them may hold more Newsprint.

A screen is one window's height at the page's width. The first screen runs from the top of the page; a section's opening
screen runs from the section's top edge (an element marked data-oa-section) one window down, cut at the page's end. A dark
panel is an element painted Charcoal or Prussian, the outermost of nested ones, of 3 percent of a screen's area or more (a
button or a chip is no panel); it counts in the section where its top falls, and the first screen holds those above the
first marked section.

A light page is judged on all three limits; a dark page (DR-204's dark mode) is printed in full and judged on red alone,
since Rule 05.1's Newsprint share is the light view's.

Usage:
  python3 -I work/build/app-kit/tools/screen_shares.py CAPTURE.png --vh 900 [--sections "Track:1320,Act:2980"]
         [--panels "x,y,w,h;x,y,w,h"] [--theme light|dark] [--json OUT]
  python3 -I work/build/app-kit/tools/screen_shares.py --self-test
The application kit calls measure() from export_checks.py with the facts it gathered from the page.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
TOKENS = (ROOT / "work/build/tokens/tokens.css").read_text()
PANEL_MIN = 0.03     # of a screen's area
TOL, RED_TOL = 3, 24


def hexrgb(name):
    h = re.search(r"--oa-color-palette-" + name + r":\s*(#[0-9A-Fa-f]{6})", TOKENS).group(1)
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


NEWSPRINT, CHARCOAL, PRUSSIAN, RED = hexrgb("newsprint"), hexrgb("charcoal"), hexrgb("prussian"), hexrgb("pillar-red")


def near(px, rgb, tol):
    return np.abs(px - np.array(rgb)).max(axis=2) <= tol


def shares(px):
    n = px.shape[0] * px.shape[1] or 1
    return {"newsprint": round(float(near(px, NEWSPRINT, TOL).sum()) / n * 100, 1),
            "dark": round(float((near(px, CHARCOAL, TOL) | near(px, PRUSSIAN, TOL)).sum()) / n * 100, 1),
            "red": round(float(near(px, RED, RED_TOL).sum()) / n * 100, 2)}


def measure(png, vh, sections=(), dark=(), theme="light", width=None):
    """Shares and panels for the first screen and each section's opening screen. sections: [{name, top}]; dark: [{rect:
    [x, y, w, h], color, tag, cls}] as the kit gathers them. Returns a list of screens, each with its verdict."""
    px = np.asarray(Image.open(png).convert("RGB")).astype(int)
    H, W = px.shape[:2]
    width = width or W
    area_min = PANEL_MIN * width * vh
    panels = [d for d in dark if d["rect"][2] * d["rect"][3] >= area_min]
    secs = sorted(({"name": s["name"], "top": int(s["top"])} for s in sections), key=lambda s: s["top"])
    starts = [{"name": "first screen", "top": 0}] + [s for s in secs if s["top"] > 0]
    out = []
    for i, s in enumerate(starts):
        top = s["top"]
        bottom = min(H, top + vh)
        nxt = starts[i + 1]["top"] if i + 1 < len(starts) else H + 1
        mine = [p for p in panels if top <= p["rect"][1] < nxt]
        sh = shares(px[top:bottom])
        faults = []
        if theme == "light":
            if not 60 <= sh["newsprint"] <= 85:
                faults.append(f"Newsprint {sh['newsprint']} percent, outside 60 to 85")
            if len(mine) > 1:
                faults.append(f"{len(mine)} dark panels in the section, past one")
        if sh["red"] > 5:
            faults.append(f"Pillar Red {sh['red']} percent, past 5")
        out.append({"screen": s["name"], "top": top, "bottom": bottom, **sh, "panels": len(mine),
                    "panel_list": [f"{p.get('tag', '?')}.{p.get('cls', '')} {p.get('color', '')} at {p['rect'][1]}" for p in mine],
                    "judged": "all three limits" if theme == "light" else "red only (dark mode)", "faults": faults})
    return out


def line(label, scr):
    return (f"{'PASS' if not scr['faults'] else 'FAIL'} {label}, {scr['screen']} ({scr['top']} to {scr['bottom']} px): "
            f"Newsprint {scr['newsprint']}, dark {scr['dark']}, red {scr['red']}; {scr['panels']} panel(s)"
            + ("".join(f"; {f}" for f in scr["faults"])))


def self_test():
    import tempfile
    bad = 0

    def check(name, ok):
        nonlocal bad
        print(f"{'pass' if ok else 'FAIL'} {name}")
        bad += not ok
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "page.png"
        im = np.zeros((2000, 100, 3), dtype=np.uint8)
        im[:] = NEWSPRINT
        im[0:200] = CHARCOAL             # a masthead band, 20 percent of the first screen
        im[1000:1100] = CHARCOAL         # a panel in section A
        im[1300:1400] = PRUSSIAN         # a second panel in section A
        im[1500:1505, 0:10] = RED
        Image.fromarray(im).save(p)
        dark = [{"rect": [0, 0, 100, 200], "color": "charcoal"}, {"rect": [0, 1000, 100, 100], "color": "charcoal"},
                {"rect": [0, 1300, 100, 100], "color": "prussian"}, {"rect": [0, 1800, 10, 10], "color": "charcoal"}]
        r = measure(p, 1000, [{"name": "A", "top": 1000}], dark)
        check("the first screen: 80 percent Newsprint, 20 dark, one panel, passes", r[0]["newsprint"] == 80.0 and r[0]["dark"] == 20.0 and r[0]["panels"] == 1 and not r[0]["faults"])
        check("a section's opening screen is cut at the page's end", r[1]["top"] == 1000 and r[1]["bottom"] == 2000)
        check("two panels in one section fail; a 10 px square is no panel", r[1]["panels"] == 2 and any("2 dark panels" in f for f in r[1]["faults"]))
        check("its Newsprint share is the screen's own, 80 percent", r[1]["newsprint"] == 80.0)
        r = measure(p, 1000, [{"name": "A", "top": 1000}], dark, theme="dark")
        check("a dark page is judged on red alone", not r[1]["faults"])
        im[:] = NEWSPRINT
        im[0:1000, 0:6] = RED
        Image.fromarray(im).save(p)
        r = measure(p, 1000, [], [])
        check("red past 5 percent fails on any page", any("Pillar Red" in f for f in r[0]["faults"]) and len(r) == 1)
        r = measure(p, 1000, [], [], theme="dark")
        check("and on a dark page too", any("Pillar Red" in f for f in r[0]["faults"]))
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("png", nargs="?")
    ap.add_argument("--vh", type=int)
    ap.add_argument("--sections", default="")
    ap.add_argument("--panels", default="")
    ap.add_argument("--theme", default="light", choices=("light", "dark"))
    ap.add_argument("--json")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(1 if self_test() else 0)
    if not a.png or not a.vh:
        ap.error("give a capture and --vh")
    secs = [{"name": x.rsplit(":", 1)[0], "top": int(x.rsplit(":", 1)[1])} for x in a.sections.split(",") if x.strip()]
    pans = [{"rect": [int(v) for v in x.split(",")], "color": "dark"} for x in a.panels.split(";") if x.strip()]
    res = measure(a.png, a.vh, secs, pans, a.theme)
    for scr in res:
        print(line(Path(a.png).name, scr))
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1))
    sys.exit(1 if any(s["faults"] for s in res) else 0)
