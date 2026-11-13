"""Cartographer, Phase 3 round 3: R2-2's derived tables for the maps (contract C1).

    python3 -I work/build/scripts/phase-3/cartographer_round3_derive.py [--check] [--figures]

Writes, from frozen files in work/build/data/:

- census-gazetteer-2024-cd119-tile-layout: our own tile layout for S82, the district tile map (rule 14.121), one square
  for each of the 435 House districts, built from the Census Bureau's district centers in census-gazetteer-2024-cd119
  (data plan row 111: published hex or tile layouts are study only and never traced). How it is built:
  1. Each district's internal point is projected by an Albers equal-area conic (parallels 29.5 and 45.5 degrees north,
     origin 37.5 north, 96 west), scaled so the lower 48 states span LAYOUT["W"] squares.
  2. Each state is a circle of area equal to its seats, at the mean of its districts' points (where its people live),
     moved by a fixed number of damped steps: circles that overlap push apart, states that share a land border pull
     together until they touch, and every state is pulled weakly toward where it started (Dorling's method).
  3. The squares: those whose centers fall inside a circle, every enclosed gap filled, kept in one piece, then trimmed
     or grown at the edge, nearest the circles first, to exactly one square a seat.
  4. Each state takes its count of squares with the least total squared distance to its circle's center (a
     transportation problem, solved exactly by successive shortest paths), so states keep their order and shape.
  5. A state the transport splits keeps its largest piece and gives each stray piece to the bordering state that
     touches it most; counts are then balanced by passing border cells along a chain of bordering states, and blocks
     tightened by swaps that keep every state in one piece; a square with three open sides moves into a notch beside
     the same state.
  6. Inside each state, districts go to squares by an exact assignment (the Hungarian method) on squared distance,
     after matching the districts' spread to the block's, so district numbers sit where they sit on the ground.
  7. Alaska (one seat) and Hawaii (two) sit apart at the lower left, a square's gap from the mainland.
  Every step is deterministic: no random numbers, ties broken by row, column and name.

- census-acs5-county-median-household-income-classes: S81's county map (rule 14.120). Every county of the 2024
  boundary layer in its geoid order (3,144), with its median, its margin, its class under the data lead's breaks of
  $50,000, $65,000 and $80,000 (ruling (c), round 3: 1 under $50,000 to 4 at $80,000 or more; empty where the Bureau
  publishes no estimate) and the count of breaks its 90 percent interval crosses (0 to 3). The map reads the class, so
  the page carries one small number a county (DL-E1, variant B); the CSV export carries every county's value and margin.
- census-cbp-county-employment-dots: S83's dot density map (rule 14.122). Every county of the layer in its geoid order,
  with its private-sector paid employees and noise flag, and its dots at one dot a 10,000 and a 50,000 employees
  (ruling (b): the count over the unit rounded half up to a whole dot). The two counties the Bureau's file lacks
  (Kalawao County, Hawaii, 15005; King County, Texas, 48269) are kept with no count, so the rows match the layer.
- clerk-house-results-2024-classes: S80 and S82, the district map and the district tile map (rules 14.119 and 14.121),
  one results file drawn two ways. Each of the 435 races from clerk-house-results-2024-by-district with its margin as
  printed (one decimal, half up), its class under the data lead's ruling (f) (1 under 5 points, 2 under 10, 3 under 20,
  4 at 20 or more; unopposed seats 4), its mark (dot: unopposed on the ballot; ring: a race decided another way), and
  its square in the tile layout above, so both maps take one set of classes and the page carries small numbers.

--check writes nothing and fails when a written file differs from what the script computes now. --figures writes nothing
and checks every figure in the titles, notes and alts of S78 to S84 against the data files, each check named in the
spec's notes_internal (check S78 to check S84). Standard library only.
"""
import csv
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data'))
CHECK = '--check' in sys.argv
FAULTS = []
LOG = []
# the layout's settings, chosen by eye from trial layouts (cartographer's notes, round 3)
LAYOUT = dict(W=34.0, PAD=0.0, ATT=0.5, HOME=0.015, LAM=0.8)


def read(name):
    with open(os.path.join(DATA, name + '.csv'), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def meta(name):
    with open(os.path.join(DATA, name + '.meta.json'), encoding='utf-8') as fh:
        return json.load(fh)


def csv_text(columns, rows):
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n')
    w.writerow(columns)
    for r in rows:
        w.writerow([r[c] for c in columns])
    return out.getvalue()


def write(name, columns, rows, side):
    text = csv_text(columns, rows)
    side_text = json.dumps(side, ensure_ascii=False, indent=1) + '\n'
    for path, body in ((os.path.join(DATA, name + '.csv'), text), (os.path.join(DATA, name + '.meta.json'), side_text)):
        if CHECK:
            if not os.path.exists(path) or open(path, encoding='utf-8').read() != body:
                FAULTS.append('differs from what the script computes: ' + os.path.basename(path))
        else:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(body)


# the states that share a land border, lower 48 (Four Corners' point contacts left out)
NB = {"AL": "FL GA MS TN", "AZ": "CA CO NM NV UT", "AR": "LA MO MS OK TN TX", "CA": "AZ NV OR", "CO": "AZ KS NE NM OK UT WY",
      "CT": "MA NY RI", "DE": "MD NJ PA", "FL": "AL GA", "GA": "AL FL NC SC TN", "ID": "MT NV OR UT WA WY", "IL": "IA IN KY MO WI",
      "IN": "IL KY MI OH", "IA": "IL MN MO NE SD WI", "KS": "CO MO NE OK", "KY": "IL IN MO OH TN VA WV", "LA": "AR MS TX", "ME": "NH",
      "MD": "DE PA VA WV", "MA": "CT NH NY RI VT", "MI": "IN OH WI", "MN": "IA ND SD WI", "MS": "AL AR LA TN", "MO": "AR IA IL KS KY NE OK TN",
      "MT": "ID ND SD WY", "NE": "CO IA KS MO SD WY", "NV": "AZ CA ID OR UT", "NH": "MA ME VT", "NJ": "DE NY PA", "NM": "AZ CO OK TX UT",
      "NY": "CT MA NJ PA VT", "NC": "GA SC TN VA", "ND": "MN MT SD", "OH": "IN KY MI PA WV", "OK": "AR CO KS MO NM TX", "OR": "CA ID NV WA",
      "PA": "DE MD NJ NY OH WV", "RI": "CT MA", "SC": "GA NC", "SD": "IA MN MT ND NE WY", "TN": "AL AR GA KY MO MS NC VA", "TX": "AR LA NM OK",
      "UT": "AZ CO ID NV WY", "VT": "MA NH NY", "VA": "KY MD NC TN WV", "WA": "ID OR", "WV": "KY MD OH PA VA", "WI": "IA IL MI MN",
      "WY": "CO ID MT NE SD UT"}


def hungarian(a):
    """An exact assignment of rows to columns at least cost (rows <= columns), the Hungarian method."""
    nr, nc = len(a), len(a[0]); u = [0] * (nr + 1); v = [0] * (nc + 1); p = [0] * (nc + 1); way = [0] * (nc + 1)
    for i in range(1, nr + 1):
        p[0] = i; j0 = 0; minv = [float('inf')] * (nc + 1); used = [False] * (nc + 1)
        while True:
            used[j0] = True; i0 = p[j0]; delta = float('inf'); j1 = 0
            for j in range(1, nc + 1):
                if not used[j]:
                    cur = a[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]: minv[j] = cur; way[j] = j0
                    if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(nc + 1):
                if used[j]: u[p[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if p[j0] == 0: break
        while True:
            j1 = way[j0]; p[j0] = p[j1]; j0 = j1
            if j0 == 0: break
    res = [None] * nr
    for j in range(1, nc + 1):
        if p[j]: res[p[j] - 1] = j - 1
    return res


def tile_layout():
    rows = [r for r in read('census-gazetteer-2024-cd119') if r['state'] != 'DC']
    ARGS = LAYOUT
    P1, P2, P0, L0 = map(math.radians, (29.5, 45.5, 37.5, -96.0))
    n = (math.sin(P1) + math.sin(P2)) / 2; C = math.cos(P1) ** 2 + 2 * n * math.sin(P1); rho0 = math.sqrt(C - 2 * n * math.sin(P0)) / n
    def albers(lon, lat):
        t = n * (math.radians(lon) - L0); rho = math.sqrt(C - 2 * n * math.sin(math.radians(lat))) / n
        return rho * math.sin(t), -(rho0 - rho * math.cos(t))
    main = [r for r in rows if r['state'] not in ('AK', 'HI')]
    for r in rows: r['x'], r['y'] = albers(float(r['lon']), float(r['lat']))
    xs = [r['x'] for r in main]; ys = [r['y'] for r in main]
    s = ARGS['W'] / (max(xs) - min(xs))
    for r in rows: r['gx'] = (r['x'] - min(xs)) * s; r['gy'] = (r['y'] - min(ys)) * s
    states = {}
    for r in main: states.setdefault(r['state'], []).append(r)
    S = sorted(states)
    NB = {"AL":"FL GA MS TN","AZ":"CA CO NM NV UT","AR":"LA MO MS OK TN TX","CA":"AZ NV OR","CO":"AZ KS NE NM OK UT WY",
    "CT":"MA NY RI","DE":"MD NJ PA","FL":"AL GA","GA":"AL FL NC SC TN","ID":"MT NV OR UT WA WY","IL":"IA IN KY MO WI",
    "IN":"IL KY MI OH","IA":"IL MN MO NE SD WI","KS":"CO MO NE OK","KY":"IL IN MO OH TN VA WV","LA":"AR MS TX","ME":"NH",
    "MD":"DE PA VA WV","MA":"CT NH NY RI VT","MI":"IN OH WI","MN":"IA ND SD WI","MS":"AL AR LA TN","MO":"AR IA IL KS KY NE OK TN",
    "MT":"ID ND SD WY","NE":"CO IA KS MO SD WY","NV":"AZ CA ID OR UT","NH":"MA ME VT","NJ":"DE NY PA","NM":"AZ CO OK TX UT",
    "NY":"CT MA NJ PA VT","NC":"GA SC TN VA","ND":"MN MT SD","OH":"IN KY MI PA WV","OK":"AR CO KS MO NM TX","OR":"CA ID NV WA",
    "PA":"DE MD NJ NY OH WV","RI":"CT MA","SC":"GA NC","SD":"IA MN MT ND NE WY","TN":"AL AR GA KY MO MS NC VA","TX":"AR LA NM OK",
    "UT":"AZ CO ID NV WY","VT":"MA NH NY","VA":"KY MD NC TN WV","WA":"ID OR","WV":"KY MD OH PA VA","WI":"IA IL MI MN",
    "WY":"CO ID MT NE SD UT"}
    PAIRS = sorted(set(tuple(sorted((a, b))) for a, v in NB.items() for b in v.split()))
    # 1. Dorling circles of area n cells at each state's mean district center, pulled toward bordering states
    cen = {k: [sum(r['gx'] for r in v) / len(v), sum(r['gy'] for r in v) / len(v)] for k, v in states.items()}
    orig = {k: list(v) for k, v in cen.items()}
    rad = {k: math.sqrt(len(states[k]) / math.pi) for k in S}
    for it in range(3000):
        F = {k: [0.0, 0.0] for k in S}
        for i, a in enumerate(S):
            for b in S[i + 1:]:
                dx = cen[b][0] - cen[a][0]; dy = cen[b][1] - cen[a][1]; d = math.hypot(dx, dy) or 1e-6
                ov = rad[a] + rad[b] + ARGS['PAD'] - d
                if ov > 0:
                    ux, uy = dx / d, dy / d
                    F[a][0] -= ux * ov; F[a][1] -= uy * ov; F[b][0] += ux * ov; F[b][1] += uy * ov
        for a, b in PAIRS:
            dx = cen[b][0] - cen[a][0]; dy = cen[b][1] - cen[a][1]; d = math.hypot(dx, dy) or 1e-6
            gap = d - (rad[a] + rad[b] + ARGS['PAD'])
            if gap > 0:
                ux, uy = dx / d, dy / d; g = gap * ARGS['ATT']
                F[a][0] += ux * g; F[a][1] += uy * g; F[b][0] -= ux * g; F[b][1] -= uy * g
        for k in S:
            F[k][0] += (orig[k][0] - cen[k][0]) * ARGS['HOME']; F[k][1] += (orig[k][1] - cen[k][1]) * ARGS['HOME']
            m = len(states[k]) ** 0.5
            cen[k][0] += 0.25 * F[k][0] / m; cen[k][1] += 0.25 * F[k][1] / m
    # 2. the cells: inside the circles, holes filled, the edge trimmed or grown to exactly one cell a district
    NEED = sum(len(v) for v in states.values())
    x0 = int(min(cen[k][0] - rad[k] for k in S)) - 4; x1 = int(max(cen[k][0] + rad[k] for k in S)) + 4
    y0 = int(min(cen[k][1] - rad[k] for k in S)) - 4; y1 = int(max(cen[k][1] + rad[k] for k in S)) + 4
    E = {}
    for gy in range(y0, y1 + 1):
        for gx in range(x0, x1 + 1):
            E[(gx, gy)] = min(math.hypot(gx + 0.5 - cen[k][0], gy + 0.5 - cen[k][1]) - rad[k] for k in S)
    def nb4(c): return [(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)]
    def exterior(U):
        out = {(x0, y0)}; st = [(x0, y0)]
        while st:
            c = st.pop()
            for q in nb4(c):
                if q in E and q not in U and q not in out: out.add(q); st.append(q)
        return out
    U = set(k for k, e in E.items() if e <= 0)
    def upieces(U):
        seen = set(); out = []
        for c in sorted(U, key=lambda z: (z[1], z[0])):
            if c in seen: continue
            part = [c]; seen.add(c); st = [c]
            while st:
                for q in nb4(st.pop()):
                    if q in U and q not in seen: seen.add(q); st.append(q); part.append(q)
            out.append(part)
        return sorted(out, key=len, reverse=True)
    while True:
        U = set(upieces(U)[0])
        ext = exterior(U)
        U |= set(k for k in E if k not in U and k not in ext)
        if len(U) == NEED: break
        if len(U) > NEED:
            edge = [k for k in U if any(q in ext for q in nb4(k))]
            U.discard(max(edge, key=lambda k: (E[k], k[1], k[0])))
        else:
            rim = [k for k in ext if any(q in U for q in nb4(k))]
            U.add(min(rim, key=lambda k: (E[k], k[1], k[0])))
    
    cells = sorted(U, key=lambda k: (k[1], k[0])); M = len(cells)
    def dc(c, k): return ((c[0] + 0.5 - cen[k][0]) ** 2 + (c[1] + 0.5 - cen[k][1]) ** 2)
    # 3. transport: each state its count of cells, least total squared distance to its center (successive shortest paths)
    cost = {k: [dc(c, k) for c in cells] for k in S}
    owner = [None] * M; left = {k: len(states[k]) for k in S}; own = {k: set() for k in S}
    while any(left.values()):
        dist = {k: (0.0 if left[k] > 0 else float('inf')) for k in S}; prev = {k: None for k in S}
        free_best = {}
        for k in S:
            cs = cost[k]; bi = min((i for i in range(M) if owner[i] is None), key=lambda i: cs[i]); free_best[k] = (cs[bi], bi)
        edge = {}
        for sk in S:
            cs = cost[sk]
            for tk in S:
                if tk == sk or not own[tk]: continue
                ct = cost[tk]; bi = min(own[tk], key=lambda i: (cs[i] - ct[i], i)); edge[(sk, tk)] = (cs[bi] - ct[bi], bi)
        for _ in range(len(S)):
            ch = False
            for (a, b), (w, i) in edge.items():
                if dist[a] + w < dist[b] - 1e-12: dist[b] = dist[a] + w; prev[b] = (a, i); ch = True
            if not ch: break
        end = min(S, key=lambda k: (dist[k] + free_best[k][0], k))
        k, cell = end, free_best[end][1]
        while True:
            old = owner[cell]
            if old is not None: own[old].discard(cell)
            owner[cell] = k; own[k].add(cell)
            if prev[k] is None or (left[k] > 0 and dist[k] == 0.0): break
            k, cell = prev[k]
        left[k] -= 1
    O = {cells[i]: owner[i] for i in range(M)}
    def mine(k): return [c for c, o in O.items() if o == k]
    def pieces(cs):
        cs = set(cs); seen = set(); out = []
        for c in sorted(cs, key=lambda z: (z[1], z[0])):
            if c in seen: continue
            part = [c]; seen.add(c); st = [c]
            while st:
                for q in nb4(st.pop()):
                    if q in cs and q not in seen: seen.add(q); st.append(q); part.append(q)
            out.append(part)
        return sorted(out, key=lambda p: (-len(p), min(p, key=lambda z: (z[1], z[0]))))
    def whole(k, without=None):
        cs = [c for c in mine(k) if c != without]
        return len(cs) > 0 and len(pieces(cs)) == 1
    split0 = [k for k in S if len(pieces(mine(k))) > 1]
    # 4. a stray piece joins the bordering state that shares the most edges with it
    for k in S:
        for p in pieces(mine(k))[1:]:
            pset = set(p); touch = {}
            for c in p:
                for q in nb4(c):
                    o = O.get(q)
                    if o is not None and o != k and q not in pset: touch[o] = touch.get(o, 0) + 1
            if not touch: raise RuntimeError('an island of %s' % k)
            to = max(sorted(touch), key=lambda o: touch[o])
            for c in p: O[c] = to
    # 5. balance the counts: a state with too many cells passes border cells along a chain of neighbors to one with too few
    def count(k): return sum(1 for o in O.values() if o == k)
    def gives(X, Y):
        """X's cells beside Y that X can lose and stay whole, those furthest from X's center first"""
        out = [g for g in mine(X) if any(O.get(q) == Y for q in nb4(g)) and whole(X, g)]
        return sorted(out, key=lambda g: (dc(g, Y) - dc(g, X), g[1], g[0]))
    steps = 0
    while True:
        over = [k for k in S if count(k) > len(states[k])]
        if not over: break
        steps += 1
        if steps > 3000: raise RuntimeError('balance did not finish')
        # breadth-first from the states with too many cells to one with too few, over neighbors X -> Y where X can give to Y
        prev = {k: None for k in over}; queue = list(over); hit = None
        while queue and hit is None:
            X = queue.pop(0)
            ys = sorted(set(O.get(q) for g in mine(X) for q in nb4(g)) - {None, X})
            for Y in ys:
                if Y in prev or not gives(X, Y): continue
                prev[Y] = X
                if count(Y) < len(states[Y]): hit = Y; break
                queue.append(Y)
        if hit is None: raise RuntimeError('no chain')
        chain = [hit]
        while prev[chain[-1]] is not None: chain.append(prev[chain[-1]])
        chain.reverse()
        for X, Y in zip(chain, chain[1:]):
            g = gives(X, Y)
            if not g: break   # the chain changed under us; the loop finds another
            O[g[0]] = Y
    # 6. tighten: swap two cells of bordering states wherever both stay whole and the cost falls
    def borders(c): return sum(1 for q in nb4(c) if O.get(q) != O[c])
    def local(cs):
        zone = set(cs)
        for c in cs: zone |= set(q for q in nb4(c) if q in O)
        return sum(borders(z) for z in zone)
    LAM = ARGS['LAM']
    for rnd in range(60):
        better = 0
        for c in sorted(O, key=lambda z: (z[1], z[0])):
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    q = (c[0] + dx, c[1] + dy)
                    if q not in O or q <= c: continue
                    A, B = O[c], O[q]
                    if A == B: continue
                    if not (any(O.get(z) == B for z in nb4(c)) and any(O.get(z) == A for z in nb4(q))): continue
                    before = dc(c, A) / rad[A] ** 2 + dc(q, B) / rad[B] ** 2 + LAM * local([c, q])
                    O[c], O[q] = B, A
                    after = dc(c, B) / rad[B] ** 2 + dc(q, A) / rad[A] ** 2 + LAM * local([c, q])
                    if after < before - 1e-9 and whole(A) and whole(B): better += 1
                    else: O[c], O[q] = A, B
        if not better: break
    # 6b. smooth the edge: a cell on the map's edge may move to an empty cell beside the same state, where the state stays
    # whole, the map stays in one piece with no hole, and the cost falls
    def map_ok():
        UU = set(O)
        if len(upieces(UU)) != 1: return False
        ext = exterior(UU)
        return all(k in UU or k in ext for k in E)
    for rnd2 in range(3):
        moved = 0
        for c in sorted(O, key=lambda z: (z[1], z[0])):
            A = O[c]
            if count(A) == 1 or sum(1 for q in nb4(c) if q not in O) < 3: continue
            spots = sorted(set(e for g in mine(A) for e in nb4(g) if e in E and e not in O and sum(1 for z in nb4(e) if z in O and z != c) >= 2), key=lambda z: (z[1], z[0]))
            best = None
            for e in spots:
                before = dc(c, A) / rad[A] ** 2 + LAM * local([c] + [z for z in nb4(e) if z in O])
                del O[c]; O[e] = A
                ok = whole(A) and map_ok()
                after = dc(e, A) / rad[A] ** 2 + LAM * local([e] + [z for z in nb4(c) if z in O])
                del O[e]; O[c] = A
                if ok and after < before - 1e-9 and (best is None or after - before < best[0]): best = (after - before, e)
            if best:
                del O[c]; O[best[1]] = A; moved += 1
        if not moved: break
    bad = [k for k in S if len(pieces(mine(k))) != 1 or count(k) != len(states[k])]
    LOG.append('layout: %d split by the transport %s, %d balance steps, %d tightening rounds; faults %s' % (len(split0), split0, steps, rnd + 1, bad))
    if bad: FAULTS.append('layout: states split or miscounted: %s' % bad)
    # 7. districts to their state's cells: an assignment on squared distance after matching centers and spread
    def hungarian(a):
        nr, nc = len(a), len(a[0]); u = [0] * (nr + 1); v = [0] * (nc + 1); p = [0] * (nc + 1); way = [0] * (nc + 1)
        for i in range(1, nr + 1):
            p[0] = i; j0 = 0; minv = [float('inf')] * (nc + 1); used = [False] * (nc + 1)
            while True:
                used[j0] = True; i0 = p[j0]; delta = float('inf'); j1 = 0
                for j in range(1, nc + 1):
                    if not used[j]:
                        cur = a[i0 - 1][j - 1] - u[i0] - v[j]
                        if cur < minv[j]: minv[j] = cur; way[j] = j0
                        if minv[j] < delta: delta = minv[j]; j1 = j
                for j in range(nc + 1):
                    if used[j]: u[p[j]] += delta; v[j] -= delta
                    else: minv[j] -= delta
                j0 = j1
                if p[j0] == 0: break
            while True:
                j1 = way[j0]; p[j0] = p[j1]; j0 = j1
                if j0 == 0: break
        res = [None] * nr
        for j in range(1, nc + 1):
            if p[j]: res[p[j] - 1] = j - 1
        return res
    out = []
    for k in S:
        ds = sorted(states[k], key=lambda d: d['district']); cs = sorted(mine(k), key=lambda z: (z[1], z[0]))
        mx = sum(d['gx'] for d in ds) / len(ds); my = sum(d['gy'] for d in ds) / len(ds)
        cx = sum(c[0] + .5 for c in cs) / len(cs); cy = sum(c[1] + .5 for c in cs) / len(cs)
        sx = math.sqrt(sum((d['gx'] - mx) ** 2 for d in ds) / len(ds)) or 1; sy = math.sqrt(sum((d['gy'] - my) ** 2 for d in ds) / len(ds)) or 1
        tx = math.sqrt(sum((c[0] + .5 - cx) ** 2 for c in cs) / len(cs)) or 1; ty = math.sqrt(sum((c[1] + .5 - cy) ** 2 for c in cs) / len(cs)) or 1
        pts = [((d['gx'] - mx) / sx * tx + cx, (d['gy'] - my) / sy * ty + cy) for d in ds]
        res = hungarian([[(p[0] - c[0] - .5) ** 2 + (p[1] - c[1] - .5) ** 2 for c in cs] for p in pts])
        for d, j in zip(ds, res): out.append((d['state'], d['district'], cs[j][0], cs[j][1]))
    # Alaska and Hawaii, apart at the lower left: a square's gap below the mainland's lowest square in the first columns
    minx = min(c[2] for c in out); low = max(c[3] for c in out if c[2] <= minx + 6)
    ak = sorted(d['district'] for d in rows if d['state'] == 'AK'); hi = sorted(d['district'] for d in rows if d['state'] == 'HI')
    yy = low + 2
    out += [('AK', ak[0], minx, yy)] + [('HI', d, minx + 2 + i, yy) for i, d in enumerate(hi)]
    x0_, y0_ = min(c[2] for c in out), min(c[3] for c in out)
    out = sorted(((s_, d_, x - x0_, y - y0_) for s_, d_, x, y in out), key=lambda t: (t[0], t[1]))
    return [{'state': s_, 'district': d_, 'col': x, 'row': y} for s_, d_, x, y in out]


INCOME_BREAKS = [50000, 65000, 80000]


def layer_ids():
    """The county layer's geoids in order: the 2024 boundary file's counties of the 50 states and DC, as geo.js carries them."""
    with open(os.path.join(DATA, 'census-cb-2024-counties.geojson'), encoding='utf-8') as fh:
        gj = json.load(fh)
    return [f['properties']['geoid'] for f in gj['features'] if not f['properties']['geoid'].startswith('72')]


def county_income_classes():
    src = [r for r in read('census-acs5-county-median-household-income') if r['geoid'] != 'US']
    by = {r['geoid']: r for r in src}
    ids = layer_ids()
    if sorted(by) != ids: FAULTS.append('income: the counties differ from the boundary layer')
    out = []
    for g in ids:
        r = by[g]
        if r['median_household_income'] in ('', None):
            out.append({'geoid': g, 'name': r['name'], 'state': r['state'], 'median_household_income': '', 'moe': r['moe'] or '', 'income_class': '', 'breaks_crossed': ''})
            continue
        v, m = int(r['median_household_income']), int(r['moe'])
        out.append({'geoid': g, 'name': r['name'], 'state': r['state'], 'median_household_income': v, 'moe': m,
                    'income_class': 1 + sum(1 for b in INCOME_BREAKS if v >= b),
                    'breaks_crossed': sum(1 for b in INCOME_BREAKS if v - m < b < v + m)})
    m0 = meta('census-acs5-county-median-household-income')
    n = [sum(1 for r in out if r['income_class'] == k) for k in (1, 2, 3, 4)]
    x1 = sum(1 for r in out if r['breaks_crossed'] not in ('',) and r['breaks_crossed'] >= 1)
    x2 = sum(1 for r in out if r['breaks_crossed'] not in ('',) and r['breaks_crossed'] >= 2)
    LOG.append('income classes %s, none %d; intervals crossing a break %d, two %d' % (n, sum(1 for r in out if r['income_class'] == ''), x1, x2))
    side = {
        "file": "census-acs5-county-median-household-income-classes.csv", "kind": "derived",
        "publisher": m0["publisher"], "title_or_table": m0["title_or_table"] + ", with class and break crossings for the county map",
        "table_id": m0.get("table_id"), "url": m0.get("url"), "observation_period": m0.get("observation_period"),
        "geography": "Every county and county equivalent of the 50 states and DC in the 2024 boundary files, in geoid order (Connecticut’s nine planning regions)",
        "universe_or_base": m0.get("universe_or_base"), "unit": m0.get("unit"), "date_retrieved": m0.get("date_retrieved"), "vintage": m0.get("vintage"),
        "qualification": m0.get("qualification", "") + " Classes: 1, under $50,000; 2, $50,000 to under $65,000; 3, $65,000 to under $80,000; 4, $80,000 or more; empty where the Bureau publishes no estimate (De Baca County, New Mexico).",
        "columns": {
            "geoid": {"type": "id", "description": "county FIPS code"},
            "name": {"type": "text", "description": "county name and state, as the Bureau prints it"},
            "state": {"type": "code", "description": "USPS state code"},
            "median_household_income": {"type": "integer", "description": "median household income, 2024 dollars", "unit": "dollars"},
            "moe": {"type": "integer", "description": "90 percent margin of error, as published", "unit": "dollars"},
            "income_class": {"type": "integer", "description": "class under the breaks $50,000, $65,000 and $80,000, 1 to 4; empty with no estimate"},
            "breaks_crossed": {"type": "integer", "description": "breaks inside the 90 percent interval (value less margin to value plus margin), 0 to 3"}
        },
        "printed_source_line": m0["printed_source_line"],
        "ledger_row": m0.get("ledger_row"), "domain": m0.get("domain"), "states": [],
        "derived_from": ["census-acs5-county-median-household-income.csv"],
        "derivation": "Each county's class by the data lead's breaks (round 3 ruling (c)) and the count of breaks strictly inside its 90 percent interval; rows in the geoid order of the boundary file census-cb-2024-counties.geojson, the national row left out (the map prints it beside itself) (cartographer_round3_derive.py)",
        "margin_columns": {"median_household_income": "moe"},
        "notes": LOG[-1:]
    }
    write('census-acs5-county-median-household-income-classes', ['geoid', 'name', 'state', 'median_household_income', 'moe', 'income_class', 'breaks_crossed'], out, side)


def half_up(x):
    return int(math.floor(x + 0.5))


def cbp_dots():
    src = read('census-cbp-county-employment')
    by = {r['geoid']: r for r in src}
    out = []
    for g in layer_ids():
        r = by.get(g)
        if r is None:
            out.append({'geoid': g, 'name': '', 'state': '', 'paid_employees': '', 'emp_noise_flag': '', 'emp_noise_words': 'not in the Bureau’s county file', 'dots_10k': '', 'dots_50k': ''})
            continue
        e = int(r['paid_employees'])
        out.append({'geoid': g, 'name': r['name'], 'state': r['state'], 'paid_employees': e, 'emp_noise_flag': r['emp_noise_flag'], 'emp_noise_words': r['emp_noise_words'],
                    'dots_10k': half_up(e / 10000), 'dots_50k': half_up(e / 50000)})
    # the two counties the file lacks: their names from the boundary file
    with open(os.path.join(DATA, 'census-cb-2024-counties.geojson'), encoding='utf-8') as fh:
        props = {f['properties']['geoid']: f['properties'] for f in json.load(fh)['features']}
    st = {r['geoid'][:2]: r['state'] for r in src}
    for r in out:
        if r['name'] == '':
            p0 = props[r['geoid']]; r['state'] = p0.get('code') or st.get(r['geoid'][:2], '')
            sname = next(x['name'].split(', ')[-1] for x in src if x['geoid'][:2] == r['geoid'][:2])
            r['name'] = p0['name'] + ', ' + sname
    has = [r for r in out if r['paid_employees'] != '']
    none10 = [r for r in has if r['dots_10k'] == 0]
    LOG.append('dots: %d at 10,000 and %d at 50,000; %d counties draw no dot at 10,000, holding %d employees; counties sum %d; missing %s'
               % (sum(r['dots_10k'] for r in has), sum(r['dots_50k'] for r in has), len(none10), sum(r['paid_employees'] for r in none10),
                  sum(r['paid_employees'] for r in has), [r['geoid'] for r in out if r['paid_employees'] == '']))
    m0 = meta('census-cbp-county-employment')
    side = {
        "file": "census-cbp-county-employment-dots.csv", "kind": "derived",
        "publisher": m0["publisher"], "title_or_table": m0["title_or_table"] + ", with dots for the dot density map",
        "table_id": m0.get("table_id"), "url": m0.get("url"), "observation_period": m0.get("observation_period"),
        "geography": "Every county and county equivalent of the 50 states and DC in the 2024 boundary files, in geoid order",
        "universe_or_base": m0.get("universe_or_base"), "unit": m0.get("unit"), "date_retrieved": m0.get("date_retrieved"), "vintage": m0.get("vintage"),
        "qualification": m0.get("qualification", "") + " Dots: one a 10,000 or a 50,000 employees, the count over the unit rounded half up; a dot is a count, placed at random inside its county, never an address.",
        "columns": {
            "geoid": {"type": "id", "description": "county FIPS code"},
            "name": {"type": "text", "description": "county name and state"},
            "state": {"type": "code", "description": "USPS state code"},
            "paid_employees": {"type": "integer", "description": "private-sector paid employees, week of March 12, as published; empty for the two counties the file lacks", "unit": "employees"},
            "emp_noise_flag": {"type": "category", "description": "the Bureau's noise flag: G, H or J"},
            "emp_noise_words": {"type": "text", "description": "the flag in words"},
            "dots_10k": {"type": "integer", "description": "dots at one a 10,000 employees"},
            "dots_50k": {"type": "integer", "description": "dots at one a 50,000 employees"}
        },
        "printed_source_line": m0["printed_source_line"],
        "ledger_row": m0.get("ledger_row"), "domain": m0.get("domain"), "states": [],
        "derived_from": ["census-cbp-county-employment.csv"],
        "derivation": "Each county's dots at one a 10,000 and one a 50,000 paid employees, rounded half up; rows in the geoid order of the boundary file census-cb-2024-counties.geojson, with the two counties the Bureau's file lacks kept empty (cartographer_round3_derive.py)",
        "notes": LOG[-1:]
    }
    write('census-cbp-county-employment-dots', ['geoid', 'name', 'state', 'paid_employees', 'emp_noise_flag', 'emp_noise_words', 'dots_10k', 'dots_50k'], out, side)


RING_KINDS = ['one-party contest (top-two)', 'ranked-choice, first round (the Clerk prints the first round)',
              'ranked-choice, final round (the Clerk prints the final round)', 'Louisiana open primary, decided in November']


def house_classes(lay):
    src = read('clerk-house-results-2024-by-district')
    at = {(r['state'], r['district']): r for r in lay}
    out = []
    for r in src:
        t = at.get((r['state'], r['district']))
        if t is None: FAULTS.append('house: no square for %s %s' % (r['state'], r['district'])); continue
        m = r['margin_pct']
        printed = '' if m == '' else '%.1f' % (math.floor(float(m) * 10 + 0.5) / 10)
        cls = 4 if printed == '' else (1 if float(printed) < 5 else 2 if float(printed) < 10 else 3 if float(printed) < 20 else 4)
        mark = 'dot' if r['seat_kind'] == 'unopposed on the ballot' else 'ring' if r['seat_kind'] in RING_KINDS else ''
        if r['seat_kind'] not in RING_KINDS + ['unopposed on the ballot', 'Republican and Democratic', 'other pairing']: FAULTS.append('house: a kind of seat with no rule: ' + r['seat_kind'])
        # ST-M4 (review fix pass): a close race as S82's table names it, the district, the winner's party and the margin
        # as printed ("7 (Republican, 3.7)", "at large (Republican, 2.0)"), only where the race was decided by under 5
        # points as printed (class 1), so the grouped table's list names those seats alone
        close = '%s (%s, %s)' % ('at large' if r['district'] == '00' else str(int(r['district'])), r['winner_group'], printed) if cls == 1 else ''
        out.append({'state': r['state'], 'district': r['district'], 'winner': r['winner'], 'winner_group': r['winner_group'],
                    'runner_up': r['runner_up'], 'runner_up_group': r['runner_up_group'], 'margin_pct': m, 'margin_printed': printed,
                    'margin_class': cls, 'seat_kind': r['seat_kind'], 'mark': mark, 'close_seat': close,
                    'party': {'Democratic': 'D', 'Republican': 'R'}[r['winner_group']], 'col': t['col'], 'row': t['row']})
    import collections
    k = collections.Counter((str(r['margin_class']) if r['mark'] != 'dot' else 'unopposed', r['winner_group']) for r in out)
    LOG.append('house classes (class, party): %s' % sorted(k.items()))
    m0 = meta('clerk-house-results-2024-by-district')
    side = {
        "file": "clerk-house-results-2024-classes.csv", "kind": "derived",
        "publisher": m0["publisher"], "title_or_table": m0["title_or_table"] + ", with margin classes and tile squares for the district maps",
        "table_id": m0.get("table_id"), "url": m0.get("url"), "observation_period": m0.get("observation_period"),
        "geography": m0.get("geography"), "universe_or_base": m0.get("universe_or_base"), "unit": m0.get("unit"),
        "date_retrieved": m0.get("date_retrieved"), "vintage": m0.get("vintage"),
        "qualification": m0.get("qualification", "") + " Classes follow the margin as printed to one decimal: 1, under 5 points; 2, 5 to under 10; 3, 10 to under 20; 4, 20 or more, and every seat unopposed on the ballot. Marks: dot, unopposed on the ballot; ring, a race decided another way (one-party contests, Alaska’s first round, Maine’s 2nd district’s final round, Louisiana’s open primaries). Squares: Oath & Action’s tile layout (census-gazetteer-2024-cd119-tile-layout).",
        "columns": {
            "state": {"type": "code", "description": "USPS state code"},
            "district": {"type": "text", "description": "district number; 00 at large"},
            "winner": {"type": "text", "description": "candidate with the most votes"},
            "winner_group": {"type": "category", "description": "the winner's party: Republican or Democratic (Minnesota’s DFL included)"},
            "runner_up": {"type": "text", "description": "candidate with the second most votes"},
            "runner_up_group": {"type": "category", "description": "the runner-up's party, Republican, Democratic or other"},
            "margin_pct": {"type": "number", "description": "winner less runner-up, percentage points of all votes for the office", "unit": "percentage points"},
            "margin_printed": {"type": "number", "description": "the margin as printed, one decimal, half up", "unit": "percentage points"},
            "margin_class": {"type": "integer", "description": "1 under 5 points, 2 under 10, 3 under 20, 4 at 20 or more and unopposed"},
            "seat_kind": {"type": "category", "description": "kind of seat, in the source file's words"},
            "mark": {"type": "category", "description": "dot, unopposed on the ballot; ring, decided another way; empty otherwise"},
            "close_seat": {"type": "text", "description": "a close race as S82's table names it: the district, the winner's party and the margin as printed (\"7 (Republican, 3.7)\", \"at large (Republican, 2.0)\"), only where the margin as printed is under 5 points; empty otherwise"},
            "party": {"type": "category", "description": "the winner's party as one letter, D or R, the column the tile map's panels read (its island carries 435 of them; the table and the CSV print winner_group in words)"},
            "col": {"type": "integer", "description": "tile layout column"},
            "row": {"type": "integer", "description": "tile layout row"}
        },
        "printed_source_line": m0["printed_source_line"],
        "source_line_variants": {
            "with_tile_layout": "Source: Office of the Clerk, U.S. House of Representatives, Statistics of the Presidential and Congressional Election of November 5, 2024, 435 House districts; U.S. Census Bureau, 2024 Gazetteer Files, congressional districts of the 119th Congress. Retrieved November 12, 2026. Margins computed by Oath & Action from the official counts; tile layout by Oath & Action from the Bureau’s district centers."
        },
        "ledger_row": m0.get("ledger_row"), "domain": m0.get("domain"), "states": [],
        "derived_from": ["clerk-house-results-2024-by-district.csv", "census-gazetteer-2024-cd119-tile-layout.csv"],
        "derivation": "Each race's printed margin, class (data lead's ruling (f), round 3), mark and, for a race under 5 points as printed, the words the closest-races list prints for it (ST-M4, review fix pass), and the winner's party as one letter for the drawing, joined to its square in the tile layout by state and district (cartographer_round3_derive.py)",
        "notes": LOG[-1:]
    }
    write('clerk-house-results-2024-classes', ['state', 'district', 'winner', 'winner_group', 'runner_up', 'runner_up_group', 'margin_pct', 'margin_printed', 'margin_class', 'seat_kind', 'mark', 'close_seat', 'party', 'col', 'row'], out, side)


SPECS = os.path.normpath(os.path.join(HERE, '..', '..', 'chart-kit', 'specs'))


def spec_words(sid):
    with open(os.path.join(SPECS, sid.lower() + '.json'), encoding='utf-8') as fh:
        d = json.load(fh)
    parts = [d['title'], d['measure_line'], d['alt']] + d.get('notes', []) + [json.dumps(d.get('labels', {}), ensure_ascii=False)]
    return ' '.join(parts)


def figures():
    bad = []
    def has(sid, words, why):
        if words not in spec_words(sid): bad.append('%s: "%s" not found (%s)' % (sid, words, why))
    def eq(sid, a, b, why):
        if a != b: bad.append('%s: %s: %r against %r' % (sid, why, a, b))
    # S78: fixed broadband, classes at 71, 75 and 79 percent
    bb = read('census-acs-broadband-by-state'); us = [r for r in bb if r['code'] == 'US'][0]; st = [r for r in bb if r['code'] != 'US']
    eq('S78', '%.1f' % float(us['broadband_fixed_pct']), '76.6', 'national figure'); eq('S78', us['broadband_fixed_pct_moe_s2801'], '0.1', 'national margin')
    cl = lambda v: 1 if v < 71 else 2 if v < 75 else 3 if v < 79 else 4
    byc = {k: [r['code'] for r in st if cl(float(r['broadband_fixed_pct'])) == k] for k in (1, 2, 3, 4)}
    eq('S78', [len(byc[k]) for k in (1, 2, 3, 4)], [9, 11, 20, 11], 'class counts')
    eq('S78', 'DC' in byc[4] and 'DC' not in byc[1], True, 'DC in the top class, so 10 states and DC; nine states at the bottom')
    has('S78', '10 states and DC', 'title'); has('S78', 'under 71 in nine.', 'title')
    # ST-S12 (review fix pass, the data lead's rule): count on the figures the table prints, one decimal half up; a place
    # crosses where its printed interval reaches a value in another class, an interval ending exactly on a break reaching
    # the class that begins there
    import decimal
    p1 = lambda x: float(decimal.Decimal(str(x)).quantize(decimal.Decimal('0.1'), rounding=decimal.ROUND_HALF_UP))
    pr = {r['code']: (p1(r['broadband_fixed_pct']), float(r['broadband_fixed_pct_moe_s2801'])) for r in st}
    eq('S78', [c for c in pr if cl(pr[c][0]) != cl(float([r for r in st if r['code'] == c][0]['broadband_fixed_pct']))], [], 'rounding moves no class')
    cross = sorted(c for c, (e, m) in pr.items() if cl(round(e - m, 1)) != cl(e) or cl(round(e + m, 1)) != cl(e))
    eq('S78', cross, ['AR', 'CA', 'CO', 'DC', 'DE', 'KS', 'ND', 'NE', 'OK', 'VT', 'WI', 'WY'], 'intervals crossing a break, on the printed figures')
    has('S78', 'On the figures the table prints, 11 states and the District of Columbia sit close enough to a class line', 'note 1')
    # ST-S5: the alt names a state in a class only where its printed interval sits inside it
    clear_top = sorted(c for c in byc[4] if round(pr[c][0] - pr[c][1], 1) >= 79)
    eq('S78', clear_top, ['CT', 'HI', 'MA', 'MD', 'NH', 'NJ', 'UT', 'WA'], 'alt: the top class clear of the line')
    has('S78', 'eight of them stay in it even at the low end of the survey’s margin of error: Connecticut, Hawaii, Maryland, Massachusetts, New Hampshire, New Jersey, Utah and Washington', 'alt')
    for code in ('AK', 'MS', 'WV', 'MT', 'NM'): eq('S78', code in byc[1] and round(pr[code][0] + pr[code][1], 1) < 71, True, 'alt: %s under 71 across its margin' % code)
    has('S78', 'United States {value}% (±{margin})', 'national label')
    # S79: the distance and bearing between the Gazetteer's internal points; the photograph's credit
    pl = {r['name']: r for r in read('census-gazetteer-2024-places')}
    a, b = pl['Bakersfield city'], pl['Lake Isabella CDP']
    p1, p2 = math.radians(float(a['lat'])), math.radians(float(b['lat'])); dl = math.radians(float(b['lon']) - float(a['lon']))
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    miles = 2 * 3958.7613 * math.asin(math.sqrt(h)); brg = (math.degrees(math.atan2(math.sin(dl) * math.cos(p2), math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl))) + 360) % 360
    eq('S79', round(miles), 37, 'miles'); eq('S79', 22.5 <= brg < 67.5, True, 'bearing northeast')
    has('S79', 'about 37 miles northeast of Bakersfield', 'title')
    plate = open(os.path.normpath(os.path.join(HERE, '..', '..', 'guide', 'specimens', 's-01-8-correct.html')), encoding='utf-8').read()
    eq('S79', 'Isabella Lake Dam safety project' in plate and 'March 27, 2014' in plate and 'Lake Isabella, California' in plate, True, "the photograph's caption in chapter 01's plate (pho-04r)")
    # S80 and S82: the shared classes
    hc = read('clerk-house-results-2024-classes'); mi = [r for r in hc if r['state'] == 'MI']
    eq('S80', len(mi), 13, 'districts'); eq('S80', sum(1 for r in mi if r['winner_group'] == 'Democratic'), 6, 'Democratic seats')
    closest = min((r for r in mi if r['margin_printed']), key=lambda r: float(r['margin_printed']))
    eq('S80', (closest['district'], closest['margin_printed']), ('07', '3.7'), 'closest race'); has('S80', 'in the 7th district, was decided by 3.7 points', 'title')
    eq('S80', sum(1 for r in mi if r['margin_class'] == '4'), 7, 'races at 20 or more'); has('S80', 'seven of its 13 races by 20 points or more', 'title')
    eq('S80', all(r['seat_kind'] == 'Republican and Democratic' for r in mi), True, 'note 1: every race a Republican against a Democrat')
    eq('S82', (sum(1 for r in hc if r['winner_group'] == 'Republican'), sum(1 for r in hc if r['winner_group'] == 'Democratic')), (220, 215), 'seats')
    for sid in ('S80', 'S82'): has(sid, 'Republicans won 220' if sid == 'S82' else 'Republicans won 220 House seats and Democrats 215', 'national result')
    u5 = [r for r in hc if r['margin_class'] == '1']
    eq('S82', (len(u5), sum(1 for r in u5 if r['winner_group'] == 'Democratic')), (36, 22), 'under 5 points')
    eq('S82', sum(1 for r in hc if r['mark'] == 'dot'), 22, 'unopposed'); eq('S82', sum(1 for r in hc if r['mark'] == 'ring'), 14, 'rings')
    one = sorted((r['state'], r['district']) for r in hc if r['seat_kind'] == 'one-party contest (top-two)')
    eq('S82', one, [('CA', '12'), ('CA', '16'), ('CA', '20'), ('CA', '34'), ('WA', '04'), ('WA', '09')], 'one-party contests')
    has('S82', '36 of the 435 races were decided by under 5 points', 'title'); has('S82', '22 won by Democrats and 14 by Republicans, and 22 seats', 'alt')
    # ST-M4: the list column names exactly the 36 seats under 5 points as printed
    cs = [r for r in hc if r['close_seat']]; eq('S82', (len(cs), len(set(r['state'] for r in cs)), sorted(r['state'] + r['district'] for r in cs) == sorted(r['state'] + r['district'] for r in u5)), (36, 21, True), 'closest races listed')
    eq('S82', all(r['close_seat'].endswith('(%s, %s)' % (r['winner_group'], r['margin_printed'])) for r in cs), True, 'each close seat with its party and printed margin')
    # ST-S4: the six non-voting members, the district-98 features of the boundary file
    with open(os.path.join(DATA, 'census-cb-2024-cd119.geojson'), encoding='utf-8') as fh:
        d98 = sorted(f['properties']['geoid'] for f in json.load(fh)['features'] if f['properties'].get('district') == '98')
    eq('S82', d98, ['1198', '6098', '6698', '6998', '7298', '7898'], 'six non-voting members: DC, American Samoa, Guam, Northern Mariana Islands, Puerto Rico, Virgin Islands')
    has('S82', 'the six members who have no vote on the House floor: the delegates of the District of Columbia, American Samoa, Guam, the Northern Mariana Islands and the U.S. Virgin Islands, and Puerto Rico’s Resident Commissioner', 'note 4')
    # S81: county classes and crossings, the nation
    ic = read('census-acs5-county-median-household-income-classes'); usr = [r for r in read('census-acs5-county-median-household-income') if r['geoid'] == 'US'][0]
    eq('S81', [sum(1 for r in ic if r['income_class'] == str(k)) for k in (1, 2, 3, 4)], [371, 1138, 1049, 585], 'class counts')
    est = [r for r in ic if r['income_class'] != '']
    eq('S81', (len(est), sum(1 for r in est if int(r['breaks_crossed']) >= 1), sum(1 for r in est if int(r['breaks_crossed']) >= 2)), (3143, 1707, 182), 'crossings')
    eq('S81', (usr['median_household_income'], usr['moe']), ('80734', '166'), 'nation'); has('S81', '$80,734 (±$166)', 'national label')
    eq('S81', [r['name'] for r in ic if r['income_class'] == ''], ['De Baca County, New Mexico'], 'no estimate')
    for w in ('585 counties and under $50,000 in 371', '1,707 of 3,143', '182 two classes away'): has('S81', w, 'title and note')
    eq('S81', sum(1 for r in est if int(r['median_household_income']) >= int(usr['median_household_income'])), 549, 'counties at or above the nation (ST-S7)')
    has('S81', '549 of the 3,143 counties sit at or above it', 'note 2')
    # S83: dots and the county sum
    dd = read('census-cbp-county-employment-dots'); e = [r for r in dd if r['paid_employees'] != '']
    tot = sum(int(r['paid_employees']) for r in e); eq('S83', (len(e), tot), (3142, 132151802), 'counties and their sum')
    srt = sorted((int(r['paid_employees']) for r in e), reverse=True); acc = 0; n_half = None
    for i, v in enumerate(srt):
        acc += v
        if acc >= tot / 2: n_half = i + 1; break
    eq('S83', n_half, 100, 'counties holding half'); has('S83', 'Half of the 132.2 million', 'title'); has('S83', '100 of the 3,142 counties', 'title')
    none = [r for r in e if r['dots_10k'] == '0']; eq('S83', (len(none), sum(int(r['paid_employees']) for r in none)), (1354, 2841136), 'no dot')
    none5 = [r for r in e if r['dots_50k'] == '0']; eq('S83', (len(none5), sum(int(r['paid_employees']) for r in none5)), (2426, 15370827), 'no dot at 50,000 (ST-S1)')
    has('S83', '1,354 counties holding 2.8 million employees. On a phone, where a dot stands for 50,000, 2,426 counties holding 15.4 million draw none.', 'note 1')
    cbm = meta('census-cbp-county-employment'); eq('S83', any('139,831,742' in n and '7,679,940' in n for n in cbm.get('notes', [])), True, 'the national total and the gap in the sidecar')
    eq('S83', 139831742 - tot, 7679940, 'gap'); has('S83', 'Another 7.7 million', 'note 4'); has('S83', 'The dots draw the 132.2 million', 'note 4')
    eq('S83', (sum(1 for r in e if r['emp_noise_flag'] == 'H'), sum(1 for r in e if r['emp_noise_flag'] == 'J')), (378, 29), 'flags'); has('S83', '378 counties’ counts by 2 to under 5 percent and 29 by 5 percent or more', 'note 3')
    top = sorted(e, key=lambda r: -int(r['paid_employees']))[:20]; ids = set(r['geoid'] for r in top)
    for g, nm in (('36061', 'New York'), ('06037', 'Los Angeles'), ('17031', 'Chicago'), ('48113', 'Dallas'), ('48201', 'Houston'), ('13121', 'Atlanta')): eq('S83', g in ids, True, 'alt: %s among the 20 largest counties' % nm)
    # S84: the panels and the atlas's sentence
    mw = read('dol-state-minimum-wage-classes')
    for y, want in (('2010', (15, 26, 10)), ('2014', (24, 19, 8)), ('2019', (30, 14, 7)), ('2024', (31, 13, 7))):
        rs = [r for r in mw if r['year'] == y]
        eq('S84', tuple(sum(1 for r in rs if r['class'] == k) for k in ('above $7.25', 'at $7.25', 'below $7.25 or no state minimum')), want, 'panel ' + y)
        eq('S84', [r['class'] for r in rs if r['code'] == 'DC'], ['above $7.25'], 'DC above in ' + y)
    for w in ('Thirty states and DC', '14 states and DC on January 1, 2010', '23 and DC in 2014, 29 and DC in 2019 and 30 and DC in 2024'): has('S84', w, 'title and alt')
    # ST-S4 and AX-S3: the places the Department lists and the map does not draw; the marks in the four years
    hist = read('dol-state-minimum-wage-history')
    eq('S84', sorted(set(r['code'] for r in hist) - set(r['code'] for r in mw) - {'US'}), ['GU', 'PR', 'VI'], 'places the table lists and the map does not draw')
    has('S84', 'also lists Guam, Puerto Rico and the U.S. Virgin Islands, which the map does not draw', 'note 3')
    import re as _re, collections as _co
    four = [r for r in mw if r['year'] in ('2010', '2014', '2019', '2024')]
    mk = _co.Counter(m for r in four for m in _re.findall(r'\[[a-z]\]|\([a-z]\)', r['rate_as_published']))
    eq('S84', dict(mk), {'[c]': 14, '(g)': 12, '(e)': 11, '(d)': 4}, 'marks in the four years')
    eq('S84', sum(1 for r in four if r['rate_as_published'] == '...'), 20, 'cells printed "..." (No state law)')
    key = ' '.join(meta('dol-state-minimum-wage-history').get('notes', []))
    for w in ('[c] - Rates applicable to employers of four or more', '(d) - Rates applicable to employers of six or more', '(e) - Rates applicable to employers of two or more', '(g) - Minnesota sets a lower rate'): eq('S84', w in key, True, 'the Department\'s key: ' + w)
    has('S84', '[c] marks a rate for employers of four or more workers, (d) of six or more and (e) of two or more, and (g) a state that sets a lower rate for some smaller businesses', 'note 4')
    with open(os.path.normpath(os.path.join(HERE, '..', '..', '..', 'extract', 'atlas-v7-data.json')), encoding='utf-8') as fh:
        atlas = json.load(fh)
    def find(o):
        if isinstance(o, dict):
            if o.get('id') == 'CL1516': return o
            o = list(o.values())
        if isinstance(o, list):
            for v in o:
                hit = find(v)
                if hit: return hit
        return None
    c0 = find(atlas) or {}
    eq('S84', c0.get('confidence'), 'documented', 'CL1516 graded documented')
    cl = c0.get('supports', '') + ' ' + c0.get('claim', '')
    for w in ('30 states and DC above $7.25', '13 states at $7.25', 'Georgia and Wyoming at $5.15', 'five states with no minimum wage law', 'July 1, 2026'):
        eq('S84', w in cl, True, 'V7 CL1516 holds "%s"' % w)
    for w in ('30 states and DC set a minimum wage above $7.25, 13 states set $7.25, Georgia and Wyoming set $5.15, and five states had no minimum wage law', 'atlas snapshot of October 15, 2026'): has('S84', w, 'note 1')
    for line in bad: print('FIGURE', line)
    print('figures: %d fault(s)' % len(bad))
    return bad


def main():
    if '--figures' in sys.argv:
        sys.exit(1 if figures() else 0)
    lay = tile_layout()
    g = meta('census-gazetteer-2024-cd119')
    side = {
        "file": "census-gazetteer-2024-cd119-tile-layout.csv",
        "kind": "derived",
        "publisher": g["publisher"],
        "title_or_table": "Oath & Action’s tile layout of the 435 House districts of the 119th Congress, from the Census Bureau’s 2024 Gazetteer district centers",
        "table_id": g["table_id"],
        "url": g["url"],
        "observation_period": g["observation_period"],
        "geography": "The 435 House districts of the 50 states; the District of Columbia’s delegate area left out, since its delegate has no vote on the House floor",
        "universe_or_base": "House districts, one square each",
        "unit": "grid columns and rows, counted from the upper left",
        "date_retrieved": g["date_retrieved"],
        "vintage": g["vintage"],
        "qualification": "A layout, not geography: each district is one square of the same size, placed so states keep their order and districts their order inside each state. Alaska and Hawaii sit apart at the lower left. Built by our own script from the Bureau’s district centers; no published layout was traced.",
        "columns": {
            "state": {"type": "code", "description": "USPS state code"},
            "district": {"type": "text", "description": "district number; 00 at large"},
            "col": {"type": "integer", "description": "grid column, from 0 at the left"},
            "row": {"type": "integer", "description": "grid row, from 0 at the top"}
        },
        "printed_source_line": "Source: U.S. Census Bureau, 2024 Gazetteer Files, congressional districts of the 119th Congress, 50 states. Retrieved November 12, 2026. Tile layout by Oath & Action.",
        "ledger_row": g.get("ledger_row"),
        "domain": "D02",
        "states": [],
        "derived_from": ["census-gazetteer-2024-cd119.csv"],
        "derivation": "One square for each district: districts' internal points projected (Albers equal-area), states as circles of area equal to their seats moved apart and together by Dorling's method, the squares inside the circles with every gap filled, each state given its squares by an exact transportation solution on squared distance and kept in one piece, districts placed inside each state by an exact assignment, Alaska and Hawaii set apart; deterministic, settings " + json.dumps(LAYOUT, sort_keys=True) + " (cartographer_round3_derive.py)",
        "notes": LOG[:]
    }
    write('census-gazetteer-2024-cd119-tile-layout', ['state', 'district', 'col', 'row'], lay, side)
    cols = max(r['col'] for r in lay) + 1; rws = max(r['row'] for r in lay) + 1
    print('tile layout: %d squares on a %d by %d grid' % (len(lay), cols, rws))
    house_classes(lay)
    county_income_classes()
    cbp_dots()
    for line in LOG: print(line)
    if FAULTS:
        for f in FAULTS: print('FAULT', f)
        sys.exit(1)
    print('check: 0 faults' if CHECK else 'written')


if __name__ == '__main__':
    main()
