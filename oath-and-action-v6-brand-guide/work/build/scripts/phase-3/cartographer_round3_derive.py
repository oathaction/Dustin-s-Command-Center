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

--check writes nothing and fails when a written file differs from what the script computes now. --figures checks
figures in the cartographer's specs against the data files (added as specs land). Standard library only.
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


def main():
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
    for line in LOG: print(line)
    if FAULTS:
        for f in FAULTS: print('FAULT', f)
        sys.exit(1)
    print('check: 0 faults' if CHECK else 'written')


if __name__ == '__main__':
    main()
