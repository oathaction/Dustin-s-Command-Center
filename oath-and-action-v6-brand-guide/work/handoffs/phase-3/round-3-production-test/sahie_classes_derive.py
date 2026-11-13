"""Production test 1 (simulated designer, round 3): derive a class column for a county map of the share of people under 65
without health insurance, from the frozen SAHIE county file, by Rule 14.9's test for class maps.

Run with python3 -I. Reads work/build/data/census-sahie-county-uninsured.csv (read only); writes the derived file and its
sidecar beside this script, never into work/build/. Prints the class counts, the crossings and the two-classes-apart test.
"""
import csv, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'work', 'build', 'data', 'census-sahie-county-uninsured.csv')
BREAKS = [float(x) for x in (sys.argv[1] if len(sys.argv) > 1 else '8,12,16').split(',')]
OUT = 'census-sahie-county-uninsured-classes'

def cls(v):
    if v is None: return None
    k = 1
    for b in BREAKS:
        if v >= b: k += 1
    return k

rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
out = []
for r in rows:
    v = float(r['uninsured_pct']) if r['uninsured_pct'] else None
    m = float(r['uninsured_moe']) if r['uninsured_moe'] else None
    k = cls(v)
    crossed = None
    if v is not None and m is not None:
        crossed = sum(1 for b in BREAKS if v - m < b <= v + m)
    out.append(dict(geoid=r['geoid'], name=r['county'], state=r['code'], uninsured_pct=r['uninsured_pct'], uninsured_moe=r['uninsured_moe'],
                    uninsured_people=r['uninsured_people'], uninsured_class='' if k is None else k, breaks_crossed='' if crossed is None else crossed))
n = len(BREAKS) + 1
counts = [sum(1 for o in out if o['uninsured_class'] == k) for k in range(1, n + 1)]
none = sum(1 for o in out if o['uninsured_class'] == '')
moes = [float(o['uninsured_moe']) for o in out if o['uninsured_moe']]
widths = [BREAKS[i + 1] - BREAKS[i] for i in range(len(BREAKS) - 1)]
cross1 = sum(1 for o in out if o['breaks_crossed'] not in ('', 0))
cross2 = sum(1 for o in out if o['breaks_crossed'] not in ('', 0, 1))
nomoe = [o['name'] for o in out if o['uninsured_pct'] and not o['uninsured_moe']]
# Rule 14.9, second test: no two places drawn two or more classes apart sit within their gap's margin
pts = sorted([(float(o['uninsured_pct']), float(o['uninsured_moe']), o['uninsured_class'], o['name']) for o in out if o['uninsured_moe'] and o['uninsured_pct']])
bad = []
for i, a in enumerate(pts):
    for b in pts[i + 1:]:
        if b[0] - a[0] > 2 * 3.3 * math.sqrt(2): break
        if abs(b[2] - a[2]) >= 2 and (b[0] - a[0]) <= math.sqrt(a[1] ** 2 + b[1] ** 2):
            bad.append((a[3], a[0], a[1], b[3], b[0], b[1]))
print('breaks', BREAKS, 'inner class widths', widths, 'widest margin', max(moes), 'widest interval', 2 * max(moes))
print('classes', counts, 'no estimate', none, 'counties with a margin', len(moes), 'no margin published:', nomoe)
print('intervals crossing a break', cross1, 'of', len(moes), '; crossing two', cross2)
print('pairs two classes apart within their gap margin', len(bad), bad[:5])
if '--write' in sys.argv:
    cols = list(out[0].keys())
    with open(os.path.join(HERE, OUT + '.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    meta = json.load(open(SRC.replace('.csv', '.meta.json'), encoding='utf-8'))
    meta.update({'file': OUT + '.csv', 'kind': 'derived', 'derived_from': ['census-sahie-county-uninsured.csv'],
                 'derivation': f'Each county\'s class by breaks at {BREAKS} percent (Rule 14.9: every inner class at least as wide as the widest published margin, {max(moes)} points) and the count of breaks inside its 90 percent interval; rows in the source file\'s geoid order (production test, simulated designer, sahie_classes_derive.py)',
                 'margin_columns': {'uninsured_pct': 'uninsured_moe'},
                 'notes': meta.get('notes', []) + [f'classes {counts}, none {none}; intervals crossing a break {cross1}, two {cross2}; pairs two classes apart within margin {len(bad)}']})
    meta['columns'] = {'geoid': meta['columns']['geoid'], 'name': {'type': 'text', 'description': 'county name with state'}, 'state': {'type': 'code', 'description': 'USPS state code'},
                       'uninsured_pct': meta['columns']['uninsured_pct'], 'uninsured_moe': meta['columns']['uninsured_moe'], 'uninsured_people': meta['columns']['uninsured_people'],
                       'uninsured_class': {'type': 'integer', 'description': f'class 1 to {n} by the breaks; empty with no estimate'},
                       'breaks_crossed': {'type': 'integer', 'description': 'breaks inside the 90 percent interval; empty with no margin'}}
    json.dump(meta, open(os.path.join(HERE, OUT + '.meta.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('wrote', OUT)
