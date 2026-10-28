#!/usr/bin/env python3
"""Measure the proposed loop-kind marks (spiral and ring) with the studio's Phase 1 measures.

Run after maps_r2_b_check.js, which renders the marks in Chromium at device scale 1, Charcoal on White:
      python3 -I work/build/scripts/phase-2/maps_r2_b_marks.py
Reads  work/boards/phase-2/maps-r2/b/20261028_B-Kind-Mark-{Snowball,Thermostat}-{16,24}px.png
Writes work/boards/phase-2/maps-r2/b/20261028_B-Kind-Mark-Measurements.json

Measures, from work/build/scripts/phase-1/symbols_measure.py:
  pixel fit   D1-17: at least 60 percent of inked pixels crisp (coverage over 0.9)
  similarity  D1-16: mean of filled-silhouette overlap and blurred correlation, under 0.60 for a distinct pair
  silhouette  Phase 1: crisp share at least 0.60 and ink at least 25 percent of the field at 16 px
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "phase-1"))
import symbols_measure as SM  # noqa: E402

ROOT = HERE.parents[3]
ASSETS = ROOT / "work/boards/phase-2/maps-r2/b"
OUT = ASSETS / "20261028_B-Kind-Mark-Measurements.json"


def main():
    res = {"method": "work/build/scripts/phase-1/symbols_measure.py: crisp, sim; renders by maps_r2_b_check.js at device scale 1",
           "marks": {}, "pairs": {}}
    cov = {}
    for kind in ("Snowball", "Thermostat"):
        for size in (16, 24):
            p = ASSETS / f"20261028_B-Kind-Mark-{kind}-{size}px.png"
            if not p.exists():
                print("missing", p.name)
                return 1
            c = SM.load_cov(p, SM.WHITE, SM.CHAR)
            cov[(kind, size)] = c
            crisp, density = SM.crisp(c)
            res["marks"][f"{kind} {size}"] = {"crisp": crisp, "ink_share": density, "pixel_fit_pass": (crisp or 0) >= 0.60,
                                             "silhouette_pass": ((crisp or 0) >= 0.60 and density >= 0.25) if size == 16 else None}
    for size in (16, 24):
        s = SM.sim(cov[("Snowball", size)], cov[("Thermostat", size)])
        s["distinct"] = s["score"] < 0.60
        res["pairs"][f"spiral vs ring {size}"] = s
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
