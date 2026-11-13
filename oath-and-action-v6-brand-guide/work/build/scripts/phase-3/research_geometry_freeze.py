"""research_geometry_freeze.py: the U.S. Census Bureau's 2024 cartographic boundary files, frozen as GeoJSON under the
engineer's contract R1-C7 (ENG-10), research ledger P7-219 and its rows P7-219a to P7-219e.

Run, with the downloaded zips in a folder of their own:

    python3 -I work/build/scripts/phase-3/research_geometry_freeze.py --dl <folder> [--only states,counties,...] [--freeze]

Without --freeze the script reads, converts and checks, and writes nothing. With --freeze it writes each file and its
sidecar to work/build/data/ only when every check passes, and only when the bytes differ, so a rerun writes nothing.

What it does, file by file:
- checks the zip's SHA-256 against the value recorded on November 13, 2026 and stops on a mismatch;
- reads the shapefile (.shp, .dbf) from the zip with the reader below (Python's standard library only), and the use
  constraints from the zip's own ISO metadata (.shp.iso.xml), which the sidecar quotes word for word;
- writes one Feature per state, county or district, sorted by geoid, with only the properties R1-C7 names; a shape with
  more than one outer ring is one MultiPolygon, each hole kept with the outer ring that holds it;
- keeps the coordinates as the Bureau gives them (NAD83 longitude and latitude, unprojected, unsimplified, every vertex),
  rounded to six decimals as R1-C7 allows, with each ring's vertices reversed so outer rings run counterclockwise and
  holes clockwise, as RFC 7946 section 3.1.6 requires (the shapefile runs them the other way).

The 1:5,000,000 counties are frozen for California only (D3-1087): the locator's inset shows one state at a scale the
1:20,000,000 file's terms rule out.
"""
import argparse
import hashlib
import io
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'work/build/data'
RETRIEVED = '2026-11-13'
RETRIEVED_WORDS = 'November 13, 2026'
BASE = 'https://www2.census.gov/geo/tiger/GENZ2024/shp/'
PRODUCT_PAGE = 'https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2024.html'
DESCRIPTION_PAGE = ('https://www.census.gov/programs-surveys/geography/technical-documentation/naming-convention/'
                    'cartographic-boundary-file.html')
CODES_FILE = 'https://www2.census.gov/geo/docs/reference/codes2020/national_state2020.txt'
COORDS = 'NAD83 longitude and latitude as published, unprojected and unsimplified'
MAX_UNZIPPED = 60_000_000

# The two pages' own words, read November 13, 2026 from the fetched HTML (the product page and the description page it
# names for "appropriate usage"). Neither page states a license; the files' metadata states the terms (below).
PRODUCT_PAGE_QUOTE = ('The cartographic boundary files are simplified representations of select geographic areas from '
                      'the Census Bureau’s Master Address File/Topologically Integrated Geographic Encoding and '
                      'Referencing (MAF/TIGER) System. These boundary files are specifically designed for small scale '
                      'thematic mapping. ... For more details about these files, including their appropriate usage, '
                      'please see our Cartographic Boundary File Description page.')
DESCRIPTION_PAGE_QUOTE = ('Limitations. These files should not be used for: geographic analysis including area or '
                          'perimeter calculation. geocoding addresses. determining precise geographic area '
                          'relationships. Some small geographic areas are excluded from these files. Geographic areas '
                          'may not align with the same areas from another year.')

# The four island areas' USPS codes, which the districts file needs and the 20m states file does not hold, from the
# Bureau's national_state2020.txt (CODES_FILE), read November 13, 2026.
ISLAND_CODES = {'60': 'AS', '66': 'GU', '69': 'MP', '78': 'VI'}

FILES = {
    'states': dict(
        name='census-cb-2024-states', table_id='cb_2024_us_state_20m', resolution='1:20,000,000', ledger='P7-219a',
        sha='7bc773d83c01b6df69b8aada9c2b5983d97f22f4551947cc5c00b87c663223ef', count=52, domain='all',
        title='2024 Cartographic Boundary File (SHP), State and Equivalent Entities for United States, 1:20,000,000',
        line_words='states',
        geography='The 50 states, the District of Columbia and Puerto Rico (52 features); the 1:20,000,000 file holds '
                  'no island areas',
        universe='States and equivalent entities in the Bureau’s 1:20,000,000 file; boundaries only, no data values',
        period='2024 vintage; boundaries generalized from the Bureau’s MAF/TIGER database for its 2024 files',
        geoid_re=r'\d{2}', name_field='NAME',
        columns={'geoid': ('id', 'the Bureau’s GEOID: the two-digit state FIPS code'),
                 'code': ('code', 'USPS state code (the Bureau’s STUSPS)'),
                 'name': ('text', 'state name as the Bureau prints it (NAME)')}),
    'counties': dict(
        name='census-cb-2024-counties', table_id='cb_2024_us_county_20m', resolution='1:20,000,000', ledger='P7-219b',
        sha='c9a54fd95422436b8822e0b070a45a9bc3de08eb13f943cdba66e7a9c2a135ff', count=3222, domain='all',
        title='2024 Cartographic Boundary File (SHP), County and Equivalent for United States, 1:20,000,000',
        line_words='counties',
        geography='Every county and county equivalent of the 50 states and DC (3,144, Connecticut’s nine planning '
                  'regions among them) and Puerto Rico’s 78 municipios (3,222 features); no island areas',
        universe='Counties and equivalent entities in the Bureau’s 1:20,000,000 file; boundaries only, no data values',
        period='2024 vintage; county boundaries as of January 1, 2024, as the file’s metadata states',
        geoid_re=r'\d{5}', name_field='NAMELSAD',
        columns={'geoid': ('id', 'the Bureau’s GEOID: state and county FIPS codes, five digits'),
                 'code': ('code', 'USPS state code (the Bureau’s STUSPS)'),
                 'name': ('text', 'county name with its legal description as the Bureau prints it (NAMELSAD), '
                                  'such as "Kern County"')}),
    'cd119': dict(
        name='census-cb-2024-cd119', table_id='cb_2024_us_cd119_5m', resolution='1:5,000,000', ledger='P7-219c',
        sha='17370f9f4070f3a0fa82bb7400042bd418be77c208abc44288b52b3ad2344cc6', count=441, domain='D02',
        title='2024 Cartographic Boundary File (SHP), 119th Congressional Districts for United States, 1:5,000,000',
        line_words='congressional districts of the 119th Congress',
        geography='The 435 districts of the 50 states (six of them at large) and the six delegate areas of DC, '
                  'Puerto Rico, American Samoa, Guam, the Northern Mariana Islands and the U.S. Virgin Islands '
                  '(441 features)',
        universe='Congressional districts of the 119th Congress in the Bureau’s 1:5,000,000 file; boundaries only, '
                 'no data values',
        period='Districts of the 119th Congress, seated January 2025 through December 2026 (elected November 5, '
               '2024), as the states reported them to the Bureau by May 31, 2024',
        geoid_re=r'\d{4}', name_field='NAMELSAD',
        columns={'geoid': ('id', 'the Bureau’s GEOID: state FIPS code and district number, four digits'),
                 'code': ('code', 'USPS state code'),
                 'name': ('text', 'district name as the Bureau prints it (NAMELSAD), such as "Congressional '
                                  'District 23"'),
                 'district': ('text', 'district number as the Bureau gives it, two digits; "AL" for an at-large '
                                      'seat (the Bureau’s 00); "98" for a delegate area, whose member has no vote on '
                                      'the House floor')}),
    'nation': dict(
        name='census-cb-2024-nation', table_id='cb_2024_us_nation_20m', resolution='1:20,000,000', ledger='P7-219d',
        sha='3316da94609c0e72e9194a4052e54e49db05519ebc6738799256701242436213', count=1, domain='all',
        title='2024 Cartographic Boundary File (SHP), United States, 1:20,000,000',
        line_words='United States outline',
        geography='The United States clipped to a generalized coastline: the 50 states, DC and Puerto Rico, one '
                  'MultiPolygon of 82 parts. The metadata includes the island areas "when scale appropriate"; at '
                  '1:20,000,000 the file holds none',
        universe='The nation’s outline in the Bureau’s 1:20,000,000 file; boundaries only, no data values',
        period='2024 vintage',
        geoid_re=r'US', name_field='NAME',
        columns={'geoid': ('id', 'the Bureau’s GEOID for the nation, "US"'),
                 'code': ('code', '"US", the code contract C1 gives the nation'),
                 'name': ('text', 'name as the Bureau prints it (NAME)')}),
    'counties-california-5m': dict(
        name='census-cb-2024-counties-california-5m', table_id='cb_2024_us_county_5m', resolution='1:5,000,000',
        ledger='P7-219e', sha='a867f8734059b45d1d54a0ba56189dd7e73c42eb451418fa56de44c35232614b', count=58,
        domain='D10', states=['CA'], subset='06',
        title='2024 Cartographic Boundary File (SHP), County and Equivalent for United States, 1:5,000,000',
        line_words='counties of California',
        geography='California’s 58 counties (the features whose STATEFP is 06), from the national 1:5,000,000 file',
        universe='Counties of California in the Bureau’s 1:5,000,000 file; boundaries only, no data values',
        period='2024 vintage; county boundaries as of January 1, 2024, as the file’s metadata states',
        geoid_re=r'06\d{3}', name_field='NAMELSAD',
        columns={'geoid': ('id', 'the Bureau’s GEOID: state and county FIPS codes, five digits'),
                 'code': ('code', 'USPS state code (the Bureau’s STUSPS), CA in every row'),
                 'name': ('text', 'county name with its legal description as the Bureau prints it (NAMELSAD), '
                                  'such as "Kern County"')}),
}


# ------------------------------------------------------------------------------------------------------------------
# A shapefile reader, standard library only: polygons (shape type 5) and the dBASE table
# ------------------------------------------------------------------------------------------------------------------
def read_shp(b):
    code, = struct.unpack('>i', b[0:4])
    flen, = struct.unpack('>i', b[24:28])
    ver, stype = struct.unpack('<ii', b[28:36])
    if code != 9994 or ver != 1000 or stype != 5 or flen * 2 != len(b):
        raise ValueError(f'not a polygon shapefile of the stated length (code {code}, version {ver}, type {stype})')
    shapes, pos = [], 100
    while pos < len(b):
        _num, clen = struct.unpack('>ii', b[pos:pos + 8])
        rec = b[pos + 8:pos + 8 + clen * 2]
        pos += 8 + clen * 2
        st, = struct.unpack('<i', rec[0:4])
        if st == 0:
            shapes.append([])
            continue
        if st != 5:
            raise ValueError(f'shape type {st} in a polygon file')
        nparts, npts = struct.unpack('<ii', rec[36:44])
        parts = list(struct.unpack(f'<{nparts}i', rec[44:44 + 4 * nparts])) + [npts]
        xy = struct.unpack(f'<{2 * npts}d', rec[44 + 4 * nparts:44 + 4 * nparts + 16 * npts])
        pts = [(xy[2 * i], xy[2 * i + 1]) for i in range(npts)]
        shapes.append([pts[parts[i]:parts[i + 1]] for i in range(nparts)])
    return shapes


def read_dbf(b, encoding='utf-8'):
    nrec, hlen, rlen = struct.unpack('<IHH', b[4:12])
    fields, pos = [], 32
    while b[pos] != 0x0D:
        name = b[pos:pos + 11].split(b'\x00', 1)[0].decode('ascii')
        fields.append((name, chr(b[pos + 11]), b[pos + 16]))
        pos += 32
    rows = []
    for i in range(nrec):
        r = b[hlen + i * rlen:hlen + (i + 1) * rlen]
        if r[0:1] == b'*':
            raise ValueError('a deleted record in the table')
        off, row = 1, {}
        for name, _t, size in fields:
            row[name] = r[off:off + size].decode(encoding).strip()
            off += size
        rows.append(row)
    return rows


def signed_area2(ring):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:]))


def inside(pt, ring):
    x, y = pt
    c = False
    for (x0, y0), (x1, y1) in zip(ring, ring[1:]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def bbox(ring):
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    return min(xs), min(ys), max(xs), max(ys)


def group_rings(rings):
    """Shapefile rings to polygons: outer rings run clockwise (negative signed area), holes counterclockwise. Each hole
    goes with the smallest outer ring that holds a vertex of it that the outer ring does not share."""
    outers, holes = [], []
    for r in rings:
        a = signed_area2(r)
        if a == 0:
            raise ValueError('a ring with no area')
        (outers if a < 0 else holes).append(r)
    polys = [[o] for o in outers]
    for h in holes:
        hb = bbox(h)
        cands = []
        for i, o in enumerate(outers):
            ob = bbox(o)
            if not (ob[0] <= hb[0] and ob[1] <= hb[1] and ob[2] >= hb[2] and ob[3] >= hb[3]):
                continue
            ov = set(o)
            pt = next((p for p in h if p not in ov), None)
            if pt is not None and inside(pt, o):
                cands.append((abs(signed_area2(o)), i))
        if not cands:
            raise ValueError('a hole that no outer ring holds')
        polys[min(cands)[1]].append(h)
    return polys


# ------------------------------------------------------------------------------------------------------------------
# Conversion and checks
# ------------------------------------------------------------------------------------------------------------------
def r6(ring, dropped):
    """Six decimals, as R1-C7 allows. Two published vertices less than 0.1 meter apart can round to one point; the
    second is dropped and counted, so no ring holds a segment of no length. Both districts that share such an edge drop
    the same vertex, so the shared edge stays the same in each."""
    out = []
    for x, y in ring:
        p = [round(x, 6), round(y, 6)]
        if out and p == out[-1]:
            dropped[0] += 1
            continue
        out.append(p)
    return out


def use_constraints(xml_bytes):
    root = ET.fromstring(xml_bytes)  # ElementTree resolves no external entities
    found = [' '.join(' '.join(el.itertext()).split()) for el in root.iter() if el.tag.endswith('}otherConstraints')]
    use = [t for t in found if t.startswith('Use Constraints:')]
    acc = [t for t in found if t.startswith('Access constraints:')]
    if len(use) != 1 or len(acc) != 1:
        raise ValueError('the metadata does not hold one use constraint and one access constraint')
    return acc[0], use[0]


def convert(key, cfg, zbytes, state_codes):
    zf = zipfile.ZipFile(io.BytesIO(zbytes))
    if sum(i.file_size for i in zf.infolist()) > MAX_UNZIPPED:
        raise ValueError('the zip unpacks larger than expected')
    base = cfg['table_id']
    shp = zf.read(f'{base}.shp')
    dbf = zf.read(f'{base}.dbf')
    cpg = zf.read(f'{base}.cpg').decode('ascii').strip()
    prj = zf.read(f'{base}.prj').decode('ascii')
    if cpg.upper() != 'UTF-8' or 'North_American_1983' not in prj or 'PROJCS' in prj:
        raise ValueError(f'unexpected encoding or coordinate system ({cpg}; {prj[:60]})')
    access, use = use_constraints(zf.read(f'{base}.shp.iso.xml'))
    if cfg['resolution'] not in use or 'acknowledgement must be given to the U.S. Census Bureau' not in use:
        raise ValueError('the use constraint does not name the resolution and the credit')
    shapes, rows = read_shp(shp), read_dbf(dbf)
    if len(shapes) != len(rows):
        raise ValueError('the shapes and the table differ in length')
    feats, nverts_in, drops = [], 0, {}
    for shape, row in zip(shapes, rows):
        if cfg.get('subset') and row['STATEFP'] != cfg['subset']:
            continue
        if not shape:
            raise ValueError(f'a null shape at {row.get("GEOID")}')
        nverts_in += sum(len(r) for r in shape)
        dropped = [0]
        # RFC 7946, section 3.1.6: outer rings counterclockwise, holes clockwise, the reverse of the shapefile's order
        polys = [[r6(r, dropped)[::-1] for r in p] for p in group_rings(shape)]
        if dropped[0]:
            drops[row['GEOID']] = dropped[0]
        geom = ({'type': 'Polygon', 'coordinates': polys[0]} if len(polys) == 1
                else {'type': 'MultiPolygon', 'coordinates': polys})
        props = {'geoid': row['GEOID']}
        if key == 'cd119':
            props['code'] = state_codes.get(row['STATEFP']) or ISLAND_CODES[row['STATEFP']]
        elif key == 'nation':
            props['code'] = 'US'
        else:
            props['code'] = row['STUSPS']
        props['name'] = row[cfg['name_field']]
        if key == 'cd119':
            props['district'] = 'AL' if row['CD119FP'] == '00' else row['CD119FP']
        feats.append({'type': 'Feature', 'properties': props, 'geometry': geom})
    feats.sort(key=lambda f: f['properties']['geoid'])
    lines = [json.dumps(f, ensure_ascii=False, separators=(',', ':')) for f in feats]
    text = '{"type":"FeatureCollection","features":[\n' + ',\n'.join(lines) + '\n]}\n'
    return text, nverts_in, access, use, drops


def check(key, cfg, text, nverts_in, ndropped):
    """R1-C7, read back from the text that would be written. Returns faults."""
    faults = []
    if text.startswith('﻿'):
        faults.append('a byte-order mark')
    if re.search(r'\d\.\d{7,}', text) or re.search(r'\d[eE][-+]?\d', text):
        faults.append('a coordinate with more than six decimals or an exponent')
    if '—' in text or '‑' in text:
        faults.append('an em dash or U+2011')
    d = json.loads(text)
    if set(d) != {'type', 'features'} or d['type'] != 'FeatureCollection':
        faults.append('the top level is not a bare FeatureCollection')
    fs = d['features']
    if len(fs) != cfg['count']:
        faults.append(f'{len(fs)} features, {cfg["count"]} expected')
    want = list(cfg['columns'])
    ids = [f['properties'].get('geoid') for f in fs]
    if ids != sorted(ids) or len(set(ids)) != len(ids):
        faults.append('features not sorted by a unique geoid')
    nverts = 0
    for f in fs:
        p = f['properties']
        if list(f) != ['type', 'properties', 'geometry'] or f['type'] != 'Feature':
            faults.append(f'{p.get("geoid")}: a feature holds keys beyond type, properties and geometry')
        if list(p) != want or any(not isinstance(v, str) or not v for v in p.values()):
            faults.append(f'{p.get("geoid")}: properties {list(p)} are not {want}, each a string')
        if not re.fullmatch(cfg['geoid_re'], p['geoid']) or not re.fullmatch(r'[A-Z]{2}', p['code']):
            faults.append(f'{p["geoid"]}: geoid or code out of pattern')
        if key == 'cd119' and not re.fullmatch(r'AL|98|\d{2}', p['district']):
            faults.append(f'{p["geoid"]}: district {p["district"]!r}')
        g = f['geometry']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        if g['type'] not in ('Polygon', 'MultiPolygon') or (g['type'] == 'MultiPolygon' and len(polys) < 2):
            faults.append(f'{p["geoid"]}: geometry type {g["type"]} with {len(polys)} parts')
        for poly in polys:
            for i, ring in enumerate(poly):
                nverts += len(ring)
                if len(ring) < 4 or ring[0] != ring[-1]:
                    faults.append(f'{p["geoid"]}: a ring that is not closed or has under four points')
                if any(a == b for a, b in zip(ring, ring[1:])):
                    faults.append(f'{p["geoid"]}: two equal vertices in a row after rounding')
                a = signed_area2([tuple(c) for c in ring])
                if (i == 0) != (a > 0):
                    faults.append(f'{p["geoid"]}: ring {i} runs the wrong way for its role after rounding')
                if any(not (-180 <= x <= 180 and -90 <= y <= 90) for x, y in ring):
                    faults.append(f'{p["geoid"]}: a coordinate out of range')
    if nverts + ndropped != nverts_in:
        faults.append(f'{nverts} vertices written and {ndropped} dropped, {nverts_in} read: every other vertex stays')
    return sorted(set(faults))


def sidecar(key, cfg, raw_sha, access, use, n, drops):
    cols = {k: {'type': t, 'description': desc} for k, (t, desc) in cfg['columns'].items()}
    zipname = cfg['table_id'] + '.zip'
    subset = cfg.get('subset')
    m = {
        'file': cfg['name'] + '.geojson',
        'kind': 'public',
        'publisher': 'U.S. Census Bureau',
        'title_or_table': cfg['title'],
        'table_id': cfg['table_id'],
        'url': [BASE + zipname, PRODUCT_PAGE, DESCRIPTION_PAGE] + ([CODES_FILE] if key == 'cd119' else []),
        'observation_period': cfg['period'],
        'geography': cfg['geography'],
        'universe_or_base': cfg['universe'],
        'unit': 'decimal degrees of longitude and latitude, NAD83',
        'date_retrieved': RETRIEVED,
        'vintage': '2024 Cartographic Boundary Files (GENZ2024), posted April 10, 2025; metadata dated May 2025',
        'qualification': (f'Generalized for display at {cfg["resolution"]} or smaller and clipped to a simplified '
                          'coastline, so some small areas and offshore parts are left out; not for measuring area or '
                          'perimeter, geocoding addresses, or settling precise boundaries (the Bureau’s terms). '
                          'A boundary file carries no data values: a map’s CSV joins on geoid or code. The kit projects '
                          'and simplifies at build.'),
        'columns': cols,
        'printed_source_line': (f'Source: U.S. Census Bureau, Cartographic Boundary Files, 2024, {cfg["line_words"]}, '
                                f'{cfg["resolution"]}. Retrieved {RETRIEVED_WORDS}.'),
        'ledger_row': cfg['ledger'],
        'domain': cfg['domain'],
        'states': cfg.get('states', []),
        'geometry_type': 'Polygon and MultiPolygon',
        'source_resolution': cfg['resolution'],
        'raw_file': zipname,
        'raw_file_sha256': raw_sha,
        'feature_count': n,
        'coordinates': COORDS,
        'terms_of_use': {
            'file_metadata': use,
            'file_metadata_access': access,
            'product_page': PRODUCT_PAGE_QUOTE,
            'description_page': DESCRIPTION_PAGE_QUOTE,
            'read': (f'Read {RETRIEVED_WORDS}: the use and access constraints in the zip’s own ISO metadata '
                     f'({cfg["table_id"]}.shp.iso.xml), quoted word for word; the product page ({PRODUCT_PAGE}) and '
                     f'the description page it names for appropriate usage ({DESCRIPTION_PAGE}). Neither page states '
                     'a license. A work of the U.S. government, with no U.S. copyright (17 U.S.C. 105); the credit '
                     'the metadata asks for is the printed source line.'),
        },
        'notes': [
            'Converted by work/build/scripts/phase-3/research_geometry_freeze.py with its own shapefile reader '
            '(Python standard library), checked against pyshp 3.1.8 feature by feature, run with python3 -I.',
            'Coordinates are rounded to six decimals (about 0.1 meter), as R1-C7 allows. ' + (
                f'Every vertex is kept but {sum(drops.values())}: rounding made each of those equal to the vertex '
                f'before it, less than 0.1 meter away in the Bureau’s file, in {len(drops)} features '
                f'({", ".join(sorted(drops))}), and each was dropped so no segment has zero length. Neighboring '
                'districts drop the same vertex, so their shared edges stay identical.' if drops else
                'Every vertex is kept; no two in a row became equal in rounding.'),
            'Rings follow RFC 7946, section 3.1.6: outer rings counterclockwise, holes clockwise. That is the '
            'reverse of the shapefile’s order, so each ring’s vertices run in the reverse of the Bureau’s sequence, '
            'with no value changed. d3-geo expects the shapefile’s order and would need each ring reversed; a '
            'planar projection fills either way.',
        ],
    }
    if key in ('states', 'counties', 'nation'):
        m['notes'].append('Alaska’s Aleutian Islands west of the 180th meridian carry positive longitudes, as the Bureau '
                          'publishes them; a projection must place them beside the rest of Alaska.')
    if key == 'cd119':
        m['notes'].append('The file has no STUSPS field. code comes from the 20m states file for the 50 states, DC and '
                          'Puerto Rico, and from the Bureau’s national_state2020.txt for American Samoa (60, AS), '
                          'Guam (66, GU), the Northern Mariana Islands (69, MP) and the U.S. Virgin Islands (78, VI).')
        m['notes'].append('At-large seats read "AL" here (R1-C7) and "00" in the Clerk’s results file and the '
                          'Gazetteer file; join on geoid. The 1:5,000,000 file holds no area coded ZZ.')
    if subset:
        m['notes'].append(f'Subset rule (D3-1087): the features of the national file {zipname} whose STATEFP is '
                          f'{subset}, California, and no others. raw_file_sha256 is the whole national zip’s.')
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dl', required=True, help='folder holding the downloaded zips')
    ap.add_argument('--only', default=','.join(FILES))
    ap.add_argument('--freeze', action='store_true')
    a = ap.parse_args()
    dl = Path(a.dl)
    keys = [k for k in a.only.split(',') if k]
    bad = [k for k in keys if k not in FILES]
    if bad:
        sys.exit(f'unknown files: {bad}')
    raw = {}
    for k in set(keys) | {'states'}:
        cfg = FILES[k]
        b = (dl / (cfg['table_id'] + '.zip')).read_bytes()
        h = hashlib.sha256(b).hexdigest()
        if h != cfg['sha']:
            sys.exit(f'{cfg["table_id"]}.zip: SHA-256 {h} is not the recorded {cfg["sha"]}; stopping')
        raw[k] = (b, h)
    st = zipfile.ZipFile(io.BytesIO(raw['states'][0]))
    state_codes = {r['STATEFP']: r['STUSPS'] for r in read_dbf(st.read('cb_2024_us_state_20m.dbf'))}
    total = 0
    for k in keys:
        cfg = FILES[k]
        text, nin, access, use, drops = convert(k, cfg, raw[k][0], state_codes)
        faults = check(k, cfg, text, nin, sum(drops.values()))
        n = text.count('"type":"Feature"')
        meta = json.dumps(sidecar(k, cfg, raw[k][1], access, use, n, drops), indent=1, ensure_ascii=False) + '\n'
        if '—' in meta or '‑' in meta:
            faults.append('an em dash or U+2011 in the sidecar')
        for f in faults:
            print(f'FAULT {cfg["name"]}: {f}')
        total += len(faults)
        state = 'checked'
        if a.freeze and not faults:
            changed = []
            for path, body in ((OUT / (cfg['name'] + '.geojson'), text), (OUT / (cfg['name'] + '.meta.json'), meta)):
                if not path.exists() or path.read_text(encoding='utf-8') != body:
                    path.write_text(body, encoding='utf-8')
                    changed.append(path.name)
            state = 'written: ' + ', '.join(changed) if changed else 'unchanged'
        print(f'{cfg["name"]}: {n} features, {nin} vertices read, {sum(drops.values())} dropped in rounding, '
              f'{len(text.encode("utf-8"))} bytes, {len(faults)} faults, {state}')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
