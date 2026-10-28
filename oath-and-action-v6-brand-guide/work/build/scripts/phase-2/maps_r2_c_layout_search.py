#!/usr/bin/env python3
"""Direction C, Loop Lines: search for station positions on the octilinear grid (the routing step before refinement).

Run:  python3 -I work/build/scripts/phase-2/maps_r2_c_layout_search.py [seed] [iterations]
Reads Atlas V7 through maps_model.py. Prints the best layout found as grid cells; writes nothing.
The chosen layout is copied into the 25-row station table by hand and refined there by eye
(work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Station-Table.csv).

Objective, lowest wins: crossings between corridors (a corridor is a station pair joined by one or more
numbered-loop connections), stations sitting on corridors they do not belong to, corridors that leave a
station in the same direction, stations closer than two cells, corridors off the 0/45/90 degree set,
total corridor length, and districts out of their sector (E at the center; A west, B north, C east, D south).
"""
import importlib.util
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("maps_model", HERE / "maps_model.py")
MM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MM)


def network(model):
    """Stations and corridors of the 20 numbered loops."""
    corr = {}
    stations = set()
    for lid, lp in model["loops"].items():
        if lp["conceptual"]:
            continue
        for s in lp["steps"]:
            a, b = sorted((s["from"], s["to"]))
            corr.setdefault((a, b), []).append((s["id"], lid))
            stations |= {a, b}
    return sorted(stations), corr


SECTOR = {"A": 180, "B": 90, "C": 0, "D": 270}
COLS, ROWS = 17, 10


def seg_cross(p1, p2, p3, p4):
    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(p3, p4, p1), o(p3, p4, p2), o(p1, p2, p3), o(p1, p2, p4)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def pt_seg(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    L = ax * ax + ay * ay
    t = max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L)) if L else 0
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * ay)


def cost(pos, stations, corr, area, detail=False):
    c = {"cross": 0, "near": 0, "port": 0, "close": 0, "octi": 0, "len": 0, "sector": 0, "label": 0}
    edges = list(corr.keys())
    for i in range(len(edges)):
        a, b = edges[i]
        for j in range(i + 1, len(edges)):
            p, q = edges[j]
            if len({a, b, p, q}) < 4:
                continue
            if seg_cross(pos[a], pos[b], pos[p], pos[q]):
                c["cross"] += 1000
    for (a, b), items in corr.items():
        for s in stations:
            if s in (a, b):
                continue
            if pt_seg(pos[s], pos[a], pos[b]) < 0.75:
                c["near"] += 400
        dx, dy = pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]
        ang = math.degrees(math.atan2(dy, dx)) % 45
        dev = min(ang, 45 - ang)
        c["octi"] += 0 if dev < 0.5 else 25 + dev
        c["len"] += 4 * math.hypot(dx, dy) * (1 + 0.3 * (len(items) - 1))
    for s in stations:
        dirs = []
        for (a, b) in edges:
            if s in (a, b):
                o = b if s == a else a
                dirs.append(math.atan2(pos[o][1] - pos[s][1], pos[o][0] - pos[s][0]))
        for i in range(len(dirs)):
            for j in range(i + 1, len(dirs)):
                d = abs((dirs[i] - dirs[j] + math.pi) % (2 * math.pi) - math.pi)
                if d < math.radians(40):
                    c["port"] += 500
    for i, s in enumerate(stations):
        for t in stations[i + 1:]:
            dx, dy = abs(pos[s][0] - pos[t][0]), abs(pos[s][1] - pos[t][1])
            if math.hypot(dx, dy) < 2:
                c["close"] += 300
            if dy < 1 and dx < 3:
                c["label"] += 120
    cx, cy = (COLS - 1) / 2, (ROWS - 1) / 2
    for s in stations:
        ar = area[s]
        if ar == "E":
            c["sector"] += 30 * math.hypot(pos[s][0] - cx, pos[s][1] - cy)
            continue
        ang = math.degrees(math.atan2(-(pos[s][1] - cy), pos[s][0] - cx)) % 360
        d = abs((ang - SECTOR[ar] + 180) % 360 - 180)
        c["sector"] += max(0, d - 55) * 2.5
    total = sum(c.values())
    return (total, c) if detail else total


def search(seed=1, iters=60000):
    model = MM.build_model()
    stations, corr = network(model)
    area = {s: model["nodes"][s]["area"] for s in stations}
    rnd = random.Random(seed)
    cells = [(x, y) for x in range(COLS) for y in range(ROWS)]
    free = cells[:]
    rnd.shuffle(free)
    pos = {s: free[i] for i, s in enumerate(stations)}
    cur = cost(pos, stations, corr, area)
    best, bestpos = cur, dict(pos)
    T0 = 400.0
    for k in range(iters):
        T = T0 * (1 - k / iters) + 1
        s = rnd.choice(stations)
        old = pos[s]
        if rnd.random() < 0.5:
            nx, ny = old[0] + rnd.randint(-2, 2), old[1] + rnd.randint(-2, 2)
        else:
            nx, ny = rnd.randrange(COLS), rnd.randrange(ROWS)
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            continue
        occ = [t for t in stations if pos[t] == (nx, ny)]
        if occ:
            t = occ[0]
            pos[t], pos[s] = old, (nx, ny)
        else:
            pos[s] = (nx, ny)
        new = cost(pos, stations, corr, area)
        if new < cur or rnd.random() < math.exp((cur - new) / T):
            cur = new
            if new < best:
                best, bestpos = new, dict(pos)
        else:
            if occ:
                pos[t], pos[s] = (nx, ny), old
            else:
                pos[s] = old
    return best, bestpos, stations, corr, area


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 60000
    best, pos, stations, corr, area = search(seed, iters)
    total, parts = cost(pos, stations, corr, area, detail=True)
    print("seed", seed, "cost", round(total), {k: round(v) for k, v in parts.items()})
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            s = [t for t in stations if pos[t] == (x, y)]
            row += (s[0] if s else " .").rjust(4)
        print(row)
    print({s: pos[s] for s in stations})
