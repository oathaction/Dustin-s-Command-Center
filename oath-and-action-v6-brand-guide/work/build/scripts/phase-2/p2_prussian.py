"""I9. Treatment D on Prussian: every identity mark in one color, White, ampersand and lever included.

Rule 05.3 ends: "Red never sits on Prussian." Treatment D sets the whole mark in White (#FFFFFF,
13.28:1 on Prussian). Each master gets an explicit-color variant with every fill and stroke White,
so a producer can place it on Prussian without CSS. Backgrounds stay transparent.

Run: python3 -I p2_prussian.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402

SOURCES = [
    "wordmark/20261028_Wordmark-Display-Master.svg", "wordmark/20261028_Wordmark-24px-Master.svg", "wordmark/20261028_Wordmark-16px-Master.svg",
    "wordmark-condensed/20261028_Wordmark-Condensed-Display-Master.svg", "wordmark-condensed/20261028_Wordmark-Condensed-24px-Master.svg",
    "wordmark-condensed/20261028_Wordmark-Condensed-16px-Master.svg",
    "lockups/20261028_L2-Stacked-Master.svg", "lockups/20261028_L2-Stacked-Condensed-Master.svg",
    "lockups/20261028_L3-Horizontal-Master.svg", "lockups/20261028_L3-Horizontal-Condensed-Master.svg",
    "lockups/20261028_L8-Monogram-Master.svg", "lockups/20261028_L8-Monogram-Condensed-Master.svg",
    "ampersand/20261028_Amp-B-Display-Master.svg", "ampersand/20261028_Amp-B-24px-Master.svg", "ampersand/20261028_Amp-B-16px-Master.svg",
    "lockmark/20261028_Lockmark-Master-V5.svg", "lockmark/20261028_Lockmark-24px-Master.svg", "lockmark/20261028_Lockmark-16px-Master.svg",
    "hinge/20261028_Hinge-Diagram-V2-Display-Master.svg", "hinge/20261028_Hinge-Diagram-V2-Compact-Master.svg",
    "hinge/20261028_Hinge-Diagram-V2-Display-Condensed-Master.svg", "hinge/20261028_Hinge-Diagram-V2-Compact-Condensed-Master.svg",
    "badge/20261028_Hinge-Badge-Display-Master.svg", "badge/20261028_Hinge-Badge-24px-Master.svg", "badge/20261028_Hinge-Badge-16px-Master.svg",
]
WHITE = "#FFFFFF"


def whiten(svg):
    s = re.sub(r'var\(--[a-z-]+,\s*#[0-9A-Fa-f]{6}\)', WHITE, svg)
    s = s.replace('"currentColor"', f'"{WHITE}"').replace("currentColor", WHITE)
    s = re.sub(r'stroke="#[0-9A-Fa-f]{6}"', f'stroke="{WHITE}"', s)
    s = re.sub(r'fill="#(?!FFFFFF)[0-9A-Fa-f]{6}"', f'fill="{WHITE}"', s)
    s = re.sub(r'color:#[0-9A-Fa-f]{6}', f'color:{WHITE}', s)
    s = re.sub(r"<title>(.*?)</title>", lambda m: f"<title>{m.group(1)}. Treatment D for Prussian: one color, White</title>", s, count=1)
    return s


def run():
    out = {}
    for rel in SOURCES:
        src = P.ASSETS / rel
        s = whiten(src.read_text())
        colors = sorted(set(re.findall(r'#[0-9A-Fa-f]{6}', s)))
        dst = P.asset("prussian", src.stem + "-Prussian-White.svg")
        dst.write_text(s)
        out[rel] = {"file": P.rel(dst), "colors_in_file": colors, "one_color": colors == [WHITE]}
    P.save_json(P.SCRATCH / "specs/prussian.json", out)
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v["one_color"] for k, v in r.items()}, indent=1))
    print("all one color:", all(v["one_color"] for v in r.values()))
