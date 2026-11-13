"""Write the chart kit's shared map geometry, work/build/chart-kit/geo.js, from the 2024 Census boundary files.

Usage:
    python3 -I work/build/chart-kit/tools/geo_build.py [--check] [--report FILE] [--out FILE]

Round 3 (contract R3-2, ENG-10; DR-249, R3-4). Reads the frozen boundary files in work/build/data/ (R1-C7: RFC 7946
GeoJSON in NAD83 longitude and latitude, unprojected and unsimplified) and the studio's tile grid, and writes one classic
script that sets OAChartGeo. The page carries it once, for every map that shares it, and the build weighs it apart, against
the shared map geometry's 250,000 bytes (guide_charts.py).

What it does, layer by layer (LAYERS below):
  1. keeps the features a layer draws (the 50 states and DC; no map draws Puerto Rico, and no map's data holds it);
  2. finds the shared borders: a vertex where three or more distinct neighbors meet is a junction, each ring is cut at its
     junctions into arcs, and an arc two features share is kept once (so neighbors share one simplified border and no
     sliver opens between them);
  3. projects each vertex as d3.geoAlbersUsa().scale(1300).translate([487.5, 305]) does, into a 975 by 610 frame: the
     lower 48 on an Albers equal-area conic (parallels 29.5 and 45.5), Alaska (at 0.35 of the scale, parallels 55 and 65)
     and Hawaii (parallels 8 and 18) set apart at the lower left, as the tile maps place them; a feature goes to Alaska or
     Hawaii by its state code, so the Aleutians west of 180 degrees (positive longitudes in the Bureau's file) sit with
     the rest of Alaska. A state-level layer (one state's districts or counties) is drawn on the lower 48's projection
     and fitted to a frame 975 units wide;
  4. simplifies each arc once (Douglas-Peucker) to half a pixel of the widest map drawing, 720 px (TOL_PX), its ends held,
     and drops an island ring smaller than a pixel's area, never a feature's largest ring;
  5. writes the vertices on a grid of QUANTUM frame units, each arc as its first point and then the steps between points,
     each number a zigzag varint in a 64-character alphabet (five bits a character; a step of under 16 grid units, most
     of them, takes one character);
  6. carries for each layer: its features' geoids (as steps between the numbers), each feature's polygons as rings of arc
     references, and, for the states, a label point (the point inside the largest polygon farthest from its edges) and
     how far that is from the nearest edge, so a map can set a state's name inside it or beside it with a leader.

The tile grid stays the studio's own (Phase 2's us-state-tile-grid.json). K.geo in parts.js decodes the layers once a page
loads and draws them; OAChartGeo.land, .borders and .centers stay as the bubble map reads them, now from the 2024 states.
--check exits 1 when geo.js differs from what this script would write.
"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATA = ROOT / 'work/build/data'
GRID = ROOT / 'work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json'
OUT = ROOT / 'work/build/chart-kit/geo.js'
if '--out' in sys.argv:
    OUT = pathlib.Path(sys.argv[sys.argv.index('--out') + 1]).resolve()

FRAME = (975, 610)
WIDEST_PX = 720            # the widest a map draws in the guide (a reading chart); the frame's 975 units scale to it
TOL_PX = 0.5               # simplified to half a pixel at that width
TOL = TOL_PX * FRAME[0] / WIDEST_PX
QUANTUM = 0.5              # frame units per grid step (0.37 px at 720 px)
MIN_RING_PX2 = 1.0         # an island ring under a pixel's area at 720 px is left out (never a feature's largest)
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_$'

# name, file, keep(properties), frame ('nation' or 'fit'), id digits, label points
LAYERS = [
    ('states', 'census-cb-2024-states', lambda p: p['code'] != 'PR', 'nation', 2, True),
    ('counties', 'census-cb-2024-counties', lambda p: p['code'] != 'PR', 'nation', 5, False),
    ('cd119-mi', 'census-cb-2024-cd119', lambda p: p['code'] == 'MI', 'fit', 4, True),
    ('counties-ca', 'census-cb-2024-counties-california-5m', lambda p: True, 'fit', 5, False),
]


# ---- the projection: d3-geo's conicEqualArea, rotate, center, scale and translate, as geoAlbersUsa composes them ----
def conic(par0, par1, rot, center, scale, translate):
    y0, y1 = math.radians(par0), math.radians(par1)
    sy0 = math.sin(y0)
    n = (sy0 + math.sin(y1)) / 2
    c = 1 + sy0 * (2 * n - sy0)
    r0 = math.sqrt(c) / n
    dl = math.radians(rot)

    def raw(lam, phi):
        r = math.sqrt(max(0.0, c - 2 * n * math.sin(phi))) / n
        lam *= n
        return r * math.sin(lam), r0 - r * math.cos(lam)

    cx, cy = raw(math.radians(center[0]), math.radians(center[1]))

    def wrap(l):
        while l > math.pi:
            l -= 2 * math.pi
        while l < -math.pi:
            l += 2 * math.pi
        return l

    def project(lon, lat):
        x, y = raw(wrap(math.radians(lon) + dl), math.radians(lat))
        return translate[0] + scale * (x - cx), translate[1] - scale * (y - cy)
    return project


K_SCALE, TX, TY = 1300, 487.5, 305
LOWER48 = conic(29.5, 45.5, 96, (-0.6, 38.7), K_SCALE, (TX, TY))
ALASKA = conic(55, 65, 154, (-2, 58.5), K_SCALE * 0.35, (TX - 0.307 * K_SCALE, TY + 0.201 * K_SCALE))
HAWAII = conic(8, 18, 157, (-3, 19.9), K_SCALE, (TX - 0.205 * K_SCALE, TY + 0.212 * K_SCALE))
PROJ = {'AK': ALASKA, 'HI': HAWAII}
# the same constants the runtime projects points with (K.geo.project in parts.js)
PROJ_PARAMS = {'scale': K_SCALE, 'translate': [TX, TY],
               'lower48': [29.5, 45.5, 96, -0.6, 38.7, 1, 0, 0], 'AK': [55, 65, 154, -2, 58.5, 0.35, -0.307, 0.201],
               'HI': [8, 18, 157, -3, 19.9, 1, -0.205, 0.212]}


# ---- arcs ----
def rings_of(geom):
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    return [[[tuple(p) for p in ring[:-1]] for ring in poly] for poly in polys]   # drop each ring's closing point


def build_arcs(features):
    """Cut every ring at its junctions; return (arcs as lists of source points, features as polygons of rings of signed
    arc references)."""
    nb = {}
    for f in features:
        for poly in f['rings']:
            for ring in poly:
                L = len(ring)
                for i, p in enumerate(ring):
                    s = nb.setdefault(p, set())
                    s.add(ring[i - 1])
                    s.add(ring[(i + 1) % L])
    junction = {p for p, s in nb.items() if len(s) > 2}
    arcs, index = [], {}

    def add(pts):
        key = tuple(pts)
        if key in index:
            return index[key]
        rk = tuple(reversed(pts))
        if rk in index:
            return ~index[rk]
        arcs.append(list(pts))
        index[key] = len(arcs) - 1
        return len(arcs) - 1

    for f in features:
        f['refs'] = []
        for poly in f['rings']:
            prefs = []
            for ring in poly:
                cuts = [i for i, p in enumerate(ring) if p in junction]
                if not cuts:
                    # a ring with no junction (an island, or a ring two features share whole): one closed arc, started at
                    # its least point, so the same ring met twice (either way round) is one arc
                    k = min(range(len(ring)), key=lambda i: ring[i])
                    r = ring[k:] + ring[:k]
                    rr = [r[0]] + list(reversed(r[1:]))
                    a = add(r + [r[0]]) if tuple(rr + [rr[0]]) not in index else ~index[tuple(rr + [rr[0]])]
                    prefs.append([a])
                    continue
                r = ring[cuts[0]:] + ring[:cuts[0]]
                cs = [i - cuts[0] if i >= cuts[0] else i + len(ring) - cuts[0] for i in cuts]
                cs.append(len(r))
                refs = []
                for a, b in zip(cs, cs[1:]):
                    seg = r[a:b + 1] if b < len(r) else r[a:] + [r[0]]
                    refs.append(add(seg))
                prefs.append(refs)
            f['refs'].append(prefs)
    return arcs


def dp(pts, tol):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    closed = pts[0] == pts[-1]
    stack = []
    if closed:
        # a closed arc: split at the point farthest from its start first
        far = max(range(1, len(pts) - 1), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
        keep[far] = True
        stack = [(0, far), (far, len(pts) - 1)]
    else:
        stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        best, bi = 0, None
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / L if L else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, i
        if bi is not None and best > tol:
            keep[bi] = True
            stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


# ---- encoding ----
def varint(n):
    out = []
    while n >= 32:
        out.append(ALPHA[32 + (n & 31)])
        n >>= 5
    out.append(ALPHA[n])
    return ''.join(out)


def zz(v):
    return v * 2 if v >= 0 else -v * 2 - 1


def enc(v):
    return varint(zz(v))


def area(r):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1])) / 2


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0 if not L2 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def inside(rings, x, y):
    c = False
    for r in rings:
        for i in range(len(r)):
            (ax, ay), (bx, by) = r[i], r[i - 1]
            if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
                c = not c
    return c


def label_point(rings):
    """The point inside a polygon (outer ring and holes) farthest from its edges, by a grid search refined twice."""
    xs = [p[0] for p in rings[0]]
    ys = [p[1] for p in rings[0]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    edges = [(r[i - 1], r[i]) for r in rings for i in range(len(r))]

    def dist(x, y):
        return min(seg_dist(x, y, a[0], a[1], b[0], b[1]) for a, b in edges)
    best = (-1, (x0 + x1) / 2, (y0 + y1) / 2)
    step = max(x1 - x0, y1 - y0) / 24 or 1
    cx, cy, span = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) / 2 + step
    for _ in range(3):
        y = cy - span
        while y <= cy + span:
            x = cx - span
            while x <= cx + span:
                if inside(rings, x, y):
                    d = dist(x, y)
                    if d > best[0]:
                        best = (d, x, y)
                x += step
            y += step
        cx, cy, span, step = best[1], best[2], step * 2, step / 6
    return best


def build_layer(name, file, keep, frame, digits, labels):
    gj = json.loads((DATA / f'{file}.geojson').read_text())
    meta = json.loads((DATA / f'{file}.meta.json').read_text())
    feats = [{'geoid': f['properties']['geoid'], 'code': f['properties']['code'], 'rings': rings_of(f['geometry'])}
             for f in gj['features'] if keep(f['properties'])]
    feats.sort(key=lambda f: f['geoid'])
    src_arcs = build_arcs(feats)
    # which projection each arc takes: its first feature's state
    arc_proj = {}
    for f in feats:
        for poly in f['refs']:
            for ring in poly:
                for a in ring:
                    arc_proj.setdefault(a if a >= 0 else ~a, f['code'])
    proj = lambda code: PROJ.get(code, LOWER48)
    arcs = [[proj(arc_proj[i])(lon, lat) for lon, lat in a] for i, a in enumerate(src_arcs)]
    fit = None
    if frame == 'fit':
        xs = [p[0] for a in arcs for p in a]
        ys = [p[1] for a in arcs for p in a]
        pad = 0.02
        s = FRAME[0] * (1 - 2 * pad) / (max(xs) - min(xs))
        tx, ty = FRAME[0] * pad - s * min(xs), FRAME[0] * pad - s * min(ys)
        h = math.ceil(s * (max(ys) - min(ys)) + 2 * FRAME[0] * pad)
        arcs = [[(s * x + tx, s * y + ty) for x, y in a] for a in arcs]
        fit = [s, tx, ty]
        fr = [FRAME[0], h]
    else:
        fr = list(FRAME)
    simple = [dp(a, TOL) for a in arcs]
    q = [[(round(x / QUANTUM), round(y / QUANTUM)) for x, y in a] for a in simple]
    q = [[p for i, p in enumerate(a) if i == 0 or p != a[i - 1]] for a in q]

    def ring_pts(refs):
        out = []
        for r in refs:
            a = q[r] if r >= 0 else q[~r][::-1]
            out.extend(a if not out else a[1:])
        return out
    min_area = MIN_RING_PX2 * (FRAME[0] / WIDEST_PX) ** 2 / QUANTUM ** 2
    dropped = 0
    for f in feats:
        polys = []
        best = max(range(len(f['refs'])), key=lambda k: abs(area(ring_pts(f['refs'][k][0]))))
        for k, poly in enumerate(f['refs']):
            outer = ring_pts(poly[0])
            if k != best and (len(outer) < 4 or abs(area(outer)) < min_area):
                dropped += 1
                continue
            polys.append([ring for j, ring in enumerate(poly) if j == 0 or (len(ring_pts(ring)) >= 4 and abs(area(ring_pts(ring))) >= min_area)])
        f['keep'] = polys
    used = sorted({(r if r >= 0 else ~r) for f in feats for poly in f['keep'] for ring in poly for r in ring})
    renum = {old: new for new, old in enumerate(used)}
    # each arc: its length, its first point as a step from the last arc's last point (arcs follow their rings, so most
    # start where the one before ended), then the steps between its points
    arc_s, last = [], (0, 0)
    for old in used:
        a = q[old]
        s = varint(len(a)) + enc(a[0][0] - last[0]) + enc(a[0][1] - last[1])
        for (x0, y0), (x1, y1) in zip(a, a[1:]):
            s += enc(x1 - x0) + enc(y1 - y0)
        arc_s.append(s)
        last = a[-1]
    # each ring's arcs: a reference is the step from the ring's last reference (zigzag of the arc's number, ~n when the
    # ring runs it backward), so a ring of arcs found in order takes one character an arc
    shape_s = []
    for f in feats:
        s = varint(len(f['keep']))
        for poly in f['keep']:
            s += varint(len(poly))
            for ring in poly:
                s += varint(len(ring))
                prev = 0
                for r in ring:
                    v = zz(renum[r]) if r >= 0 else zz(~renum[~r])
                    s += enc(v - prev)
                    prev = v
        shape_s.append(s)
    prev, ids = 0, ''
    for f in feats:
        v = int(f['geoid'])
        ids += enc(v - prev)
        prev = v
    out = {'file': file, 'frame': fr, 'digits': digits, 'n': len(feats), 'ids': ids, 'arcs': ''.join(arc_s), 'shapes': ''.join(shape_s),
           'credit': meta['printed_source_line']}
    if fit:
        out['fit'] = [round(v, 6) for v in fit]
    if labels:
        lab = ''
        for f in feats:
            polys = [[[(x * QUANTUM, y * QUANTUM) for x, y in ring_pts(ring)] for ring in poly] for poly in f['keep']]
            big = max(polys, key=lambda p: abs(area(p[0])))
            d, x, y = label_point(big)
            lab += enc(round(x / QUANTUM)) + enc(round(y / QUANTUM)) + varint(max(0, round(d / QUANTUM)))
        out['labels'] = lab
    pts_in = sum(len(a) for a in src_arcs)
    pts_out = sum(len(q[i]) for i in used)
    report = {'layer': name, 'file': file, 'features': len(feats), 'source_vertices': sum(len(r) for f in feats for p in f['rings'] for r in p),
              'arcs': len(used), 'arc_vertices_before': pts_in, 'arc_vertices_after': pts_out, 'islands_dropped': dropped,
              'bytes': len(json.dumps(out, separators=(',', ':')))}
    return out, report


def main():
    grid = json.loads(GRID.read_text())
    layers, reports = {}, []
    for spec in LAYERS:
        lay, rep = build_layer(*spec)
        layers[spec[0]] = lay
        reports.append(rep)
    G = {'frame': list(FRAME), 'quantum': QUANTUM, 'alpha': ALPHA, 'projection': PROJ_PARAMS,
         'tiles': {g['code']: [g['col'], g['row'], g['fips'], g['name']] for g in grid},
         'layers': layers,
         'credit': 'Map: U.S. Census Bureau, Cartographic Boundary Files, 2024.', 'tolerance_px': TOL_PX, 'widest_px': WIDEST_PX}
    js = ('// Generated by work/build/chart-kit/tools/geo_build.py from the 2024 Census boundary files in work/build/data/ (R3-2).\n'
          '// Do not edit by hand. The states, counties and districts are works of the U.S. government (17 U.S.C. 105).\n'
          '(function (root) {\n  root.OAChartGeo = ' + json.dumps(G, separators=(',', ':'), ensure_ascii=False) + ';\n'
          '})(typeof globalThis !== \'undefined\' ? globalThis : this);\n')
    if '--check' in sys.argv:
        same = OUT.exists() and OUT.read_text() == js
        print(('geo.js is current' if same else 'geo.js differs from the boundary files; run tools/geo_build.py'))
        return 0 if same else 1
    OUT.write_text(js)
    if '--report' in sys.argv:
        pathlib.Path(sys.argv[sys.argv.index('--report') + 1]).write_text(json.dumps(reports, indent=1))
    for r in reports:
        print(f"{r['layer']}: {r['features']} features, {r['source_vertices']:,} vertices in the file, {r['arcs']:,} arcs, "
              f"{r['arc_vertices_before']:,} arc vertices before and {r['arc_vertices_after']:,} after, {r['islands_dropped']} islands dropped, {r['bytes']:,} bytes")
    print(f'wrote {OUT}: {len(js.encode()):,} bytes ({len(grid)} tiles, tolerance {TOL_PX} px at {WIDEST_PX} px, grid {QUANTUM} units)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
