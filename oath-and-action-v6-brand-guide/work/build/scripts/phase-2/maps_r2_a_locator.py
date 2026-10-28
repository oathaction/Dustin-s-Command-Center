"""The locator inset for Direction A's pages: Direction C's working map, small, with one or more loops lit.

CD round two, fix 7. Built by script from Direction C's own files, read at build time:
    work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Network-Data.json   corridors, their routed grid cells and
                                                                          the tracks each loop rides, with offsets
    work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Station-Table.csv   every station's grid cell
Station positions come from C's station table, so a station C moves moves here on the next build. The track
geometry follows C's (maps_r2_c_geom.offset_poly and rounded_path: tracks offset to the right of travel, parallel
tracks turning on concentric arcs) and is re-implemented here so this module does not import C's scripts while
C's maker edits them.

Styling is fix 3's: the lit loop in Charcoal at 6 px with Charcoal-filled stations and Newsprint IDs, every other
line in Stone at 2 px, on Newsprint. The band locator in the catalog scales that down (3.5 px against 1.25 px)
and drops the IDs, which would fall under 13 px. No locator carries red: it finds a loop; the card marks the reform.
"""
import csv
import json
import math
from pathlib import Path

import maps_draw as D
import maps_r2_a_fg as FG
import maps_r2_a_text as TX

ROOT = Path(__file__).resolve().parents[4]
C_DIR = ROOT / "work/boards/phase-2/maps-r2/c"
NETWORK = C_DIR / "20261028_Loop-Lines-Network-Data.json"
TABLE = C_DIR / "20261028_Loop-Lines-Station-Table.csv"

SIZES = {
    # cell, margin, track pitch, lit width, other width, corner radius, station IDs, ID capsule padding
    "rail": dict(cell=10.25, margin=16.25, pitch=5.0, lit=6.0, other=2.0, radius=7.0, ids=True, pad=8.0),
    "phone": dict(cell=9.85, margin=15.25, pitch=5.0, lit=6.0, other=2.0, radius=6.5, ids=True, pad=6.0),
    "band": dict(cell=6.0, margin=8.0, pitch=3.0, lit=3.5, other=1.25, radius=4.0, ids=False, pad=0.0),
}
LIT_DASH_SCALE = 1.6   # M1 dash lengths grow with the 6 px lit line so dashes stay readable


def read_network():
    net = json.loads(NETWORK.read_text(encoding="utf-8"))
    table = {}
    with open(TABLE, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            table[r["id"]] = (int(r["col"]), int(r["row"]))
    return net, table


def _unit(dx, dy):
    L = math.hypot(dx, dy)
    return (dx / L, dy / L) if L else (0.0, 0.0)


def offset_poly(pts, d):
    """Offset a polyline by d to the right of travel (screen coordinates), mitred at each bend (C's rule)."""
    segs = []
    for i in range(len(pts) - 1):
        u = _unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        n = (-u[1], u[0])
        segs.append(((pts[i][0] + n[0] * d, pts[i][1] + n[1] * d), (pts[i + 1][0] + n[0] * d, pts[i + 1][1] + n[1] * d), u))
    out = [segs[0][0]]
    for i in range(len(segs) - 1):
        (p0, p1, u0), (q0, q1, u1) = segs[i], segs[i + 1]
        den = u0[0] * u1[1] - u0[1] * u1[0]
        if abs(den) < 1e-9:
            out.append(p1)
            continue
        t = ((q0[0] - p0[0]) * u1[1] - (q0[1] - p0[1]) * u1[0]) / den
        out.append((p0[0] + u0[0] * t, p0[1] + u0[1] * t))
    out.append(segs[-1][1])
    return out


def rounded_path(pts, radius, offset=0.0):
    """Path through pts with every bend rounded; a track outside a turn takes radius + |offset| (C's rule)."""
    if len(pts) == 2:
        return f"M{pts[0][0]:.2f} {pts[0][1]:.2f} L{pts[1][0]:.2f} {pts[1][1]:.2f}"
    d = [f"M{pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for i in range(1, len(pts) - 1):
        p0, v, p1 = pts[i - 1], pts[i], pts[i + 1]
        u0 = _unit(v[0] - p0[0], v[1] - p0[1])
        u1 = _unit(p1[0] - v[0], p1[1] - v[1])
        z = u0[0] * u1[1] - u0[1] * u1[0]
        theta = math.acos(max(-1.0, min(1.0, u0[0] * u1[0] + u0[1] * u1[1])))
        r = max(2.0, radius - (1 if z > 0 else -1) * offset)
        t = r * math.tan(theta / 2)
        lim = min(math.hypot(v[0] - p0[0], v[1] - p0[1]), math.hypot(p1[0] - v[0], p1[1] - v[1])) * 0.5
        if t > lim:
            t = lim
            r = t / math.tan(theta / 2) if theta > 1e-6 else r
        a = (v[0] - u0[0] * t, v[1] - u0[1] * t)
        b = (v[0] + u1[0] * t, v[1] + u1[1] * t)
        d.append(f"L{a[0]:.2f} {a[1]:.2f} A{r:.2f} {r:.2f} 0 0 {1 if z > 0 else 0} {b[0]:.2f} {b[1]:.2f}")
    d.append(f"L{pts[-1][0]:.2f} {pts[-1][1]:.2f}")
    return " ".join(d)


def build(model, lit, size="rail", label=None):
    """The locator with the loops in `lit` drawn in Charcoal. Returns (svg, meta)."""
    sz = SIZES[size]
    net, table = read_network()
    c, m, P = sz["cell"], sz["margin"], sz["pitch"]
    pitch_c = float(net["pitch_px"])
    cells = [tuple(x) for co in net["corridors"] for x in co["route_cells"]] + list(table.values())
    c0, c1 = min(x for x, _ in cells), max(x for x, _ in cells)
    r0, r1 = min(y for _, y in cells), max(y for _, y in cells)
    ox, oy = m - c0 * c, m - r0 * c
    W, H = (c1 - c0) * c + 2 * m, (r1 - r0) * c + 2 * m
    px = lambda cell: (ox + cell[0] * c, oy + cell[1] * c)
    lit = list(lit)
    lit_set = set(lit)
    links = model["links"]
    under, over = [], []
    for co in net["corridors"]:
        pts = [px(x) for x in co["route_cells"]]
        for tr in co["tracks"]:
            off = tr["offset_px"] / pitch_c * P
            path_pts = offset_poly(pts, off) if abs(off) > 1e-9 else pts
            d = rounded_path(path_pts, sz["radius"], off)
            l = links[tr["link"]]
            on = tr["loop"] in lit_set
            w = sz["lit"] if on else sz["other"]
            dash = D.DASH.get(l["evidence"])
            da = ""
            if dash:
                if on:
                    dash = " ".join(f"{float(v) * LIT_DASH_SCALE:g}" for v in dash.split())
                da = f' stroke-dasharray="{dash}"'
            tex = D.DASH.get(l["evidence"]) or "solid"
            g = (f'<g class="step" data-loop="{tr["loop"]}"{D.link_attrs(l)}' + (' data-lit="1"' if on else "") + ">"
                 f'<path d="{d}" fill="none" stroke="{D.INK if on else D.STONE}" stroke-width="{w}"{da} data-texture="{tex}"/></g>')
            (over if on else under).append(g)
    lit_st = {s["code"] for lid in lit for s in model["loops"][lid]["stations"] if s["is_variable"]}
    st_under, st_over = [], []
    for k, (col, row) in sorted(table.items()):
        x, y = px((col, row))
        nm = model["nodes"][k]["label"]
        attrs = f' data-node="{k}" data-label="{D.esc(nm)}" data-col="{col}" data-row="{row}" data-cx="{x:.2f}" data-cy="{y:.2f}"'
        if k in lit_st:
            if sz["ids"]:
                tw = TX.width(k, 13, 700)
                w = tw + sz["pad"]   # half-width stays inside the margin, and C1 and C4, three cells apart, keep a gap
                st_over.append(f'<g class="var" data-lit="1"{attrs}><rect x="{x - w / 2:.2f}" y="{y - 9:.2f}" width="{w:.2f}" height="18" rx="9" fill="{D.INK}"/>'
                               + FG.T(x, y + 4.6, k, 13, 700, D.NEWS, "middle") + "</g>")
            else:
                st_over.append(f'<g class="var" data-lit="1"{attrs}><circle cx="{x:.2f}" cy="{y:.2f}" r="3.6" fill="{D.INK}"/></g>')
        else:
            r = 3.6 if sz["ids"] else 2.2
            st_under.append(f'<g class="var"{attrs}><circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{D.NEWS}" stroke="{D.STONE}" stroke-width="{1.5 if sz["ids"] else 1}"/></g>')
    n_loops = len({tr["loop"] for co in net["corridors"] for tr in co["tracks"]})
    names = ", ".join(lit)
    label = label or (f"Locator: Loop {names} lit in Charcoal on Direction C's working map; the other "
                      f"{n_loops - len(lit)} loop lines in Stone")
    body = (f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" rx="4" fill="{D.NEWS}"/>'
            + "".join(under) + "".join(st_under) + "".join(over) + "".join(st_over))
    svg = FG.svg_doc(W, H, body, label, "fg-locator",
                     f' data-lit="{" ".join(lit)}" data-size="{size}" data-cell="{c:g}" data-ox="{ox:g}" data-oy="{oy:g}" data-pitch="{P:g}"'
                     f' data-lit-width="{sz["lit"]:g}" data-other-width="{sz["other"]:g}" data-source="{NETWORK.name}"')
    return svg, {"W": W, "H": H, "loops": n_loops, "lit_stations": sorted(lit_st)}
