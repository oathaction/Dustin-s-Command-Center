"""Concept 2, Moving part: vector checks on the display masters, at rest and in the row state.

Run: python3 -I icons_r2_moving_vector_check.py
Prints, for each subject and state: painted share of the 24-unit field, red share of the painted area,
the smallest gap between any two pieces, overlaps, the bounding box, the center of mass as a share of
the field, and the share of red inside the badge corner (x 16 to 22, y 2 to 8).
"""
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import icons_r2_moving_draw as D  # noqa: E402
import icons_r2_moving_geom as G  # noqa: E402
import pathops  # noqa: E402


def centroid(d):
    p = G.to_pathops(d)
    from fontTools.pens.statisticsPen import StatisticsPen
    pen = StatisticsPen()
    p.draw(pen)
    return abs(pen.area), pen.meanX, pen.meanY


def check(name, step):
    pcs = D.pieces(name, step)
    ink = sum(G.area_of(d) for r, d in pcs if r == "ink")
    acc = sum(G.area_of(d) for r, d in pcs if r == "accent")
    gaps = [G.gap_between(a, b) for (_, a), (_, b) in itertools.combinations(pcs, 2)]
    mg = min(g for g, o in gaps)
    ov = any(o for g, o in gaps)
    bb = [G.to_pathops(d).bounds for r, d in pcs]
    box = (min(b[0] for b in bb), min(b[1] for b in bb), max(b[2] for b in bb), max(b[3] for b in bb))
    A = mx = my = 0.0
    for r, d in pcs:
        a, x, y = centroid(d)
        A += a; mx += a * x; my += a * y
    com = ((mx / A - 12) / 24, (my / A - 12) / 24)
    red = G.to_pathops("".join(d for r, d in pcs if r == "accent"))
    zone = G.to_pathops(G.contour_d(G.rect(16, 2, 6, 6)))
    inter = pathops.op(red, zone, pathops.PathOp.INTERSECTION)
    from icons_geom import d_of
    zin = G.area_of(d_of(inter)) if list(inter.segments) else 0.0
    return {"painted": (ink + acc) / 576, "red": acc / (ink + acc), "min_gap": mg, "overlap": ov, "box": box,
            "com": com, "red_in_badge_zone": zin / acc if acc else 0, "pieces": len(pcs)}


if __name__ == "__main__":
    for n in D.ICONS:
        for st in (0.0, D.STEP):
            r = check(n, st)
            b = r["box"]
            print(f"{n:8s} step {st:.0f}  painted {r['painted']*100:5.1f}%  red {r['red']*100:5.1f}%  gap {r['min_gap']:4.2f} ov {r['overlap']!s:5s}"
                  f"  box {b[0]:5.2f} {b[1]:5.2f} {b[2]:5.2f} {b[3]:5.2f}  com {r['com'][0]*100:+5.1f} {r['com'][1]*100:+5.1f}%  badge {r['red_in_badge_zone']*100:4.0f}%  pieces {r['pieces']}")
