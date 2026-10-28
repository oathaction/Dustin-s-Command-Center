"""Direction C, Loop Lines: the network, the station table, the router and the track geometry.

Imported by the Direction C drawing and build scripts (python3 -I, imported by file path). Reads Atlas V7 only
through maps_model.py and the 25-row station table:
    work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Station-Table.csv

The table holds every station position as whole grid cells, plus the side its name sits on. Corridors (a pair of
stations joined by one or more numbered-loop connections) are routed by script: a straight run when the two
stations already sit on a 0, 45 or 90 degree line, otherwise the cheapest octilinear path on the grid that keeps
one cell clear of every other station, never shares a cell with an earlier corridor and never leaves a station in
a direction another corridor already uses. Each loop then rides its corridors as one track; tracks sort so a loop
stays on the side of each corridor that faces its own inside, nested loops inner-most, and each direction of a
two-step loop keeps to its right.
"""
import csv
import heapq
import importlib.util
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "work/boards/phase-2/maps-r2/c"
TABLE = ASSETS / "20261028_Loop-Lines-Station-Table.csv"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MM = _load("maps_model", "maps_model.py")
M = MM.build_model()
LOOPS = M["loops"]
NUMBERED = [lid for lid in M["loop_order"] if not LOOPS[lid]["conceptual"]]
SKETCHED = [lid for lid in M["loop_order"] if LOOPS[lid]["conceptual"]]

DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]  # E, SE, S, SW, W, NW, N, NE (y down)


def read_table(path=TABLE):
    rows = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["id"]] = {"id": r["id"], "district": r["district"], "col": int(r["col"]), "row": int(r["row"]),
                             "label": r["label"], "dx": float(r["label_dx"] or 0), "dy": float(r["label_dy"] or 0),
                             "wrap": int(r["wrap"] or 0), "why": r["why"]}
    return rows


def network():
    """Stations, corridors and the connections each numbered loop rides, all from V7 through the model."""
    corridors = {}
    stations = set()
    for lid in NUMBERED:
        for s in LOOPS[lid]["steps"]:
            a, b = sorted((s["from"], s["to"]))
            corridors.setdefault((a, b), []).append({"link": s["id"], "loop": lid, "from": s["from"], "to": s["to"]})
            stations |= {a, b}
    return sorted(stations), corridors


STATIONS, CORRIDORS = network()


def station_loops(sid):
    return [lid for lid in NUMBERED if any(st["code"] == sid for st in LOOPS[lid]["stations"])]


# ------------------------------------------------------------------ routing on the grid

def _octi(dx, dy):
    if dx == 0 and dy == 0:
        return None
    if dx == 0 or dy == 0 or abs(dx) == abs(dy):
        g = max(abs(dx), abs(dy))
        return (dx // g if dx else 0, dy // g if dy else 0), g
    return None


def route_all(table):
    """Route every corridor. Returns {(a, b): [cells from a to b]} and the ports used at each station."""
    pos = {k: (v["col"], v["row"]) for k, v in table.items()}
    used_cells, used_diag = set(), set()
    ports = {k: set() for k in pos}
    routes = {}

    def clear_cell(c, a, b):
        for s, p in pos.items():
            if s in (a, b):
                continue
            if max(abs(p[0] - c[0]), abs(p[1] - c[1])) <= 1:
                return False
        return c not in used_cells

    def diag_key(c, d):
        # the two diagonals across one grid square cross each other; record the square
        return (min(c[0], c[0] + d[0]), min(c[1], c[1] + d[1]))

    def commit(a, b, cells):
        routes[(a, b)] = cells
        for c in cells[1:-1]:
            used_cells.add(c)
        for i in range(len(cells) - 1):
            d = (cells[i + 1][0] - cells[i][0], cells[i + 1][1] - cells[i][1])
            if d[0] and d[1]:
                used_diag.add(diag_key(cells[i], d))
        d0 = (cells[1][0] - cells[0][0], cells[1][1] - cells[0][1])
        d1 = (cells[-2][0] - cells[-1][0], cells[-2][1] - cells[-1][1])
        ports[a].add(d0)
        ports[b].add(d1)

    straight, other = [], []
    for (a, b) in CORRIDORS:
        o = _octi(pos[b][0] - pos[a][0], pos[b][1] - pos[a][1])
        (straight if o else other).append((a, b))
    for (a, b) in sorted(straight, key=lambda e: max(abs(pos[e[1]][0] - pos[e[0]][0]), abs(pos[e[1]][1] - pos[e[0]][1]))):
        (d, n) = _octi(pos[b][0] - pos[a][0], pos[b][1] - pos[a][1])
        cells = [(pos[a][0] + d[0] * i, pos[a][1] + d[1] * i) for i in range(n + 1)]
        ok = all(clear_cell(c, a, b) for c in cells[1:-1]) and d not in ports[a] and (-d[0], -d[1]) not in ports[b]
        if not ok:
            other.append((a, b))
            continue
        commit(a, b, cells)
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    bx = (min(xs) - 4, max(xs) + 4)
    by = (min(ys) - 4, max(ys) + 4)
    for (a, b) in sorted(other, key=lambda e: math.hypot(pos[e[1]][0] - pos[e[0]][0], pos[e[1]][1] - pos[e[0]][1])):
        cells = _astar(pos[a], pos[b], a, b, clear_cell, used_diag, ports, bx, by, diag_key)
        if cells is None:
            raise RuntimeError(f"no octilinear route for {a}-{b}")
        commit(a, b, cells)
    return routes, ports


def _astar(start, goal, a, b, clear_cell, used_diag, ports, bx, by, diag_key):
    TURN = {0: 0.0, 1: 0.8, 2: 2.0}
    h = lambda c: math.hypot(goal[0] - c[0], goal[1] - c[1])
    frontier = []
    cnt = 0
    best = {}
    for di, d in enumerate(DIRS):
        if d in ports[a]:
            continue
        heapq.heappush(frontier, (h(start), cnt, 0.0, start, di, [start]))
        cnt += 1
    while frontier:
        f, _, g, c, di, path = heapq.heappop(frontier)
        if c == goal:
            return path
        key = (c, di)
        if key in best and best[key] <= g:
            continue
        best[key] = g
        for turn in (-2, -1, 0, 1, 2):
            if len(path) == 1 and turn != 0:
                continue
            ndi = (di + turn) % 8
            d = DIRS[ndi]
            n = (c[0] + d[0], c[1] + d[1])
            if not (bx[0] <= n[0] <= bx[1] and by[0] <= n[1] <= by[1]):
                continue
            if n == goal:
                if (-d[0], -d[1]) in ports[b]:
                    continue
            elif not clear_cell(n, a, b):
                continue
            if d[0] and d[1] and diag_key(c, d) in used_diag:
                continue
            step = math.sqrt(2) if (d[0] and d[1]) else 1.0
            ng = g + step + TURN[abs(turn)]
            heapq.heappush(frontier, (ng + h(n), cnt, ng, n, ndi, path + [n]))
            cnt += 1
    return None


def simplify(cells):
    """Keep only the cells where the route turns."""
    out = [cells[0]]
    for i in range(1, len(cells) - 1):
        d0 = (cells[i][0] - cells[i - 1][0], cells[i][1] - cells[i - 1][1])
        d1 = (cells[i + 1][0] - cells[i][0], cells[i + 1][1] - cells[i][1])
        if d0 != d1:
            out.append(cells[i])
    out.append(cells[-1])
    return out


# ------------------------------------------------------------------ tracks

def ring_polygon(lid, pos):
    return [pos[st["code"]] for st in LOOPS[lid]["stations"]]


def signed_area(poly):
    s = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        s += x0 * y1 - x1 * y0
    return s / 2


def tracks(table, pitch):
    """Order the tracks inside each corridor. Returns {(a, b): [track dicts with 'offset' to the right of a to b]}."""
    pos = {k: (v["col"], v["row"]) for k, v in table.items()}
    area = {lid: signed_area(ring_polygon(lid, pos)) for lid in NUMBERED}
    out = {}
    for (a, b), items in CORRIDORS.items():
        left, right = [], []
        for it in items:
            lp = LOOPS[it["loop"]]
            fwd = it["from"] == a
            if lp["n"] == 2:
                side = 1 if fwd else -1          # each direction of a two-step loop keeps to its right
                size = 0.0
            else:
                cw = area[it["loop"]] > 0         # screen coordinates: positive area runs clockwise
                side_travel = 1 if cw else -1     # the loop's inside lies right of travel when it runs clockwise
                side = side_travel if fwd else -side_travel
                size = abs(area[it["loop"]])
            (left if side < 0 else right).append(dict(it, side=side, size=size))
        left.sort(key=lambda t: (t["size"], t["loop"]))
        right.sort(key=lambda t: (-t["size"], t["loop"]))
        order = left + right
        k = len(order)
        for i, t in enumerate(order):
            t["offset"] = (i - (k - 1) / 2) * pitch
            t["index"] = i
            t["count"] = k
        out[(a, b)] = order
    return out


# ------------------------------------------------------------------ polyline geometry in px

def unit(dx, dy):
    L = math.hypot(dx, dy)
    return (dx / L, dy / L) if L else (0.0, 0.0)


def offset_poly(pts, d):
    """Offset a polyline by d to the right of travel (screen coordinates), mitred at each bend."""
    if len(pts) == 2:
        u = unit(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
        n = (-u[1], u[0])
        return [(p[0] + n[0] * d, p[1] + n[1] * d) for p in pts]
    segs = []
    for i in range(len(pts) - 1):
        u = unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
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
    """SVG path through pts with every bend rounded. Parallel tracks turn on concentric arcs: a track on the outside
    of a turn takes radius + |offset|, one on the inside radius - |offset|, so the bundle keeps its spacing."""
    if len(pts) == 2:
        return f"M{pts[0][0]:.2f} {pts[0][1]:.2f} L{pts[1][0]:.2f} {pts[1][1]:.2f}", 0.0
    d = [f"M{pts[0][0]:.2f} {pts[0][1]:.2f}"]
    arc_total = 0.0
    for i in range(1, len(pts) - 1):
        p0, v, p1 = pts[i - 1], pts[i], pts[i + 1]
        u0 = unit(v[0] - p0[0], v[1] - p0[1])
        u1 = unit(p1[0] - v[0], p1[1] - v[1])
        z = u0[0] * u1[1] - u0[1] * u1[0]
        cosang = max(-1.0, min(1.0, u0[0] * u1[0] + u0[1] * u1[1]))
        theta = math.acos(cosang)
        r = radius - (1 if z > 0 else -1) * offset
        r = max(2.0, r)
        t = r * math.tan(theta / 2)
        lim = min(math.hypot(v[0] - p0[0], v[1] - p0[1]), math.hypot(p1[0] - v[0], p1[1] - v[1])) * 0.5
        if t > lim:
            t = lim
            r = t / math.tan(theta / 2) if theta > 1e-6 else r
        a = (v[0] - u0[0] * t, v[1] - u0[1] * t)
        b = (v[0] + u1[0] * t, v[1] + u1[1] * t)
        sweep = 1 if z > 0 else 0
        d.append(f"L{a[0]:.2f} {a[1]:.2f} A{r:.2f} {r:.2f} 0 0 {sweep} {b[0]:.2f} {b[1]:.2f}")
        arc_total += r * theta
    d.append(f"L{pts[-1][0]:.2f} {pts[-1][1]:.2f}")
    return " ".join(d), arc_total


def plen(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


def point_at(pts, s):
    acc = 0.0
    for i in range(len(pts) - 1):
        L = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        if acc + L >= s and L > 0:
            t = (s - acc) / L
            u = unit(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t), u
        acc += L
    u = unit(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
    return pts[-1], u


def straight_runs(pts):
    """The straight pieces of a polyline as (start, end, length)."""
    return [(pts[i], pts[i + 1], math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])) for i in range(len(pts) - 1)]


class Layout:
    """One placement of the network at one scale: grid cell size, origin, line pitch and corner radius."""

    def __init__(self, cell, ox, oy, pitch=9.0, radius=22.0, table=None):
        self.table = table or read_table()
        self.cell, self.ox, self.oy, self.pitch, self.radius = cell, ox, oy, pitch, radius
        self.routes_cells, self.ports = route_all(self.table)
        self.tracks = tracks(self.table, pitch)

    def px(self, c):
        return (self.ox + c[0] * self.cell, self.oy + c[1] * self.cell)

    def station_px(self, sid):
        t = self.table[sid]
        return self.px((t["col"], t["row"]))

    def corridor_px(self, a, b):
        return [self.px(c) for c in simplify(self.routes_cells[(a, b)])]

    def track_pts(self, a, b, offset, reverse=False):
        pts = offset_poly(self.corridor_px(a, b), offset)
        return list(reversed(pts)) if reverse else pts

    def bounds(self):
        xs, ys = [], []
        for cells in self.routes_cells.values():
            for c in cells:
                p = self.px(c)
                xs.append(p[0])
                ys.append(p[1])
        return min(xs), min(ys), max(xs), max(ys)
