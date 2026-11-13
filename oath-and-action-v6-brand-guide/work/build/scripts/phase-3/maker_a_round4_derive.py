"""Maker A, Phase 3 round 4: the figure checks for S85 to S88 (proportion and overlap), contract C1.

    python3 -I work/build/scripts/phase-3/maker_a_round4_derive.py --figures

Round 4 needs no derived table: S85 to S88 draw the research lead's frozen files as they stand
(v7-union-membership, census-cog-2022-governments-by-type and census-acs-health-coverage-overlap, with
census-acs-health-coverage-types for the published totals). --figures writes nothing and checks every figure in the
titles, notes, alts and labels of specs S85 to S88 against those files, CL-050's printed name and chip against chapter
10's register, each region's gap against its margin, and the Euler diagram's areas against its counts. Each check is
named in the spec's notes_internal (check S85 to check S88). Standard library only. Exits 1 on any failed check.
"""
import csv
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
DATA = os.path.join(GUIDE, 'work', 'build', 'data')
SPECS = os.path.join(GUIDE, 'work', 'build', 'chart-kit', 'specs')
LABELS = os.path.join(GUIDE, 'work', 'handoffs', 'phase-2', '20261110_Stage-B-Ch10-Labels.json')
LIST41 = os.path.join(GUIDE, 'work', 'build', 'guide', 'specimens', 's-10-list-41.html')
ATLAS = os.path.join(GUIDE, 'work', 'extract', 'atlas-v7-data.json')
FAULTS = []
COUNT = [0]


def read_csv(name):
    with open(os.path.join(DATA, name + '.csv'), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def read_rows(name):
    with open(os.path.join(DATA, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)['rows']


def spec(sid):
    with open(os.path.join(SPECS, sid.lower() + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def flat(s):
    """Every reader word a spec prints, with no-break spaces read as spaces."""
    parts = [s.get(k, '') for k in ('title', 'measure_line', 'alt', 'grade_line', 'source_line')]
    parts += s.get('notes', []) + s.get('chart_notes', [])
    parts.append(json.dumps(s.get('labels', {}), ensure_ascii=False))
    return ' '.join(str(p) for p in parts).replace(' ', ' ')


def check(sid, ok, what):
    COUNT[0] += 1
    if not ok:
        FAULTS.append(f'{sid}: {what}')


def millions(v):
    return f'{v / 1e6:.1f} million'


def s85():
    s, rows = spec('S85'), read_rows('v7-union-membership')
    by = {(r['year'], r['group']): r for r in rows}
    allw = by[(2025, 'All wage and salary workers')]
    n = round(allw['members_pct'])
    check('S85', allw['members_pct'] == 10.0 and n == 10, '10.0 percent draws 10 of 100')
    check('S85', s['title'].startswith('One in ten') and '2025' in s['title'], 'one in ten, 2025 (title)')
    note = s['notes'][0].replace(' ', ' ')
    check('S85', by[(1983, 'All wage and salary workers')]['members_pct'] == 20.1 and '20.1 percent in 1983' in note, '20.1 percent in 1983 (note 1)')
    check('S85', by[(2025, 'Private sector')]['members_pct'] == 5.9 and '5.9 percent' in note, 'private sector 5.9 percent (note 1)')
    check('S85', by[(2025, 'Public sector')]['members_pct'] == 32.9 and '32.9 percent' in note, 'public sector 32.9 percent (note 1)')
    check('S85', allw['members_millions'] == 14.7 and '14.7 million' in note, '14.7 million members (note 1)')
    alt = s['alt'].replace(' ', ' ')
    check('S85', 'first row of 10' in alt and 'other 90' in alt and '100 squares' in alt, '100 squares, 10 filled in the first row, 90 open (alt)')
    check('S85', s['labels']['draw'] == {'year': 2025, 'group': 'All wage and salary workers'}, 'the array draws 2025 alone (data lead condition)')
    # CL-050: the editor's label table and chapter 10's list of 41 (Q-A1, MA-3)
    with open(LABELS, encoding='utf-8') as fh:
        lab = {r['id']: r for r in json.load(fh)['rows']}
    t = s['labels']['topic']
    row = lab.get(t['id'], {})
    check('S85', t['id'] == 'CL-050' and row.get('class') == 'atlas variable', 'CL-050 is an atlas variable in the label table')
    check('S85', t['words'] == row.get('label') == 'Worker bargaining power', 'CL-050 prints its approved label, Worker bargaining power')
    check('S85', t.get('chip') == row.get('v7_chip') == 'Variable A2', 'CL-050 carries its typed chip, Variable A2')
    with open(LIST41, encoding='utf-8') as fh:
        page = fh.read()
    text = re.sub(r'<[^>]*>', '|', page[page.find('data-icon="CL-050"'):][:800])
    check('S85', [w for w in text.split('|') if w.strip()][1:2] == ['Worker bargaining power'], "chapter 10's list of 41 prints CL-050 as Worker bargaining power")
    with open(ATLAS, encoding='utf-8') as fh:
        atlas = json.load(fh)
    a2 = atlas['nodes'].get('A2', {})
    check('S85', 'Union density (BLS, 10.0% 2025)' in a2.get('indicator', ''), "Variable A2's own indicator is the 10.0 percent S85 draws")
    cl = atlas['claims'].get('CL1514', {})
    check('S85', cl.get('confidence') == 'documented' and 'CL1514' in s['v7']['ids'] and s['v7']['grade'] == 'documented', 'CL1514, documented, listed in v7.ids')
    check('S85', 'October 15, 2026' in s['grade_line'] and 'October 15, 2026' not in s['source_line'], "the atlas's date prints once, in the grade line (call 1)")


def s86():
    s, rows = spec('S86'), read_csv('census-cog-2022-governments-by-type')
    g = {r['government_type']: int(r['governments']) for r in rows}
    local = {k: v for k, v in g.items() if k not in ('Federal government', 'State governments')}
    total, ltot = sum(g.values()), sum(local.values())
    big = max(local, key=local.get)
    words = flat(s)
    check('S86', total == 90888 and ltot == 90837, 'U.S. total 90,888, local 90,837')
    check('S86', big == 'Special district governments' and local[big] == 39555, 'special districts the largest local kind, 39,555')
    check('S86', round(100 * local[big] / ltot, 1) == 43.5 and local[big] < ltot / 2, '43.5 percent of local governments, no majority')
    check('S86', '39,555' in s['title'] and '90,888' in s['title'] and '2022' in s['title'] and 'most' in s['title'] and 'majority' not in s['title'], 'title: 39,555 of 90,888 in 2022, the most, no majority claimed')
    check('S86', s['labels']['named'] == ['Special district governments'], 'the named circle is the title\'s kind')
    alt = s['alt'].replace(' ', ' ')
    for name, v in local.items():
        check('S86', f'{v:,}' in alt, f'{name}, {v:,} (alt)')
    check('S86', g['Federal government'] == 1 and g['State governments'] == 50 and 'One federal government and 50 state governments' in alt, 'one federal government and 50 states (alt)')
    check('S86', s['labels']['words_only'] == ['Federal government', 'State governments'], 'the federal government and the states print in words')
    check('S86', sorted(s['labels']['key_steps']) == [1000, 10000, 40000] and max(s['labels']['key_steps']) >= max(local.values()), 'key at 1,000, 10,000 and 40,000, spanning the largest circle (MA-5)')
    # the county circle at the narrowest phone drawing: the form's phone radius is at most 84 px and at least the width
    # left by the longest name; at 256 px the largest is at least 56 px, so counties take at least 0.277 of it
    check('S86', math.sqrt(local['County governments'] / local[big]) * 56 * 2 >= 12, 'counties at least 12 px across at 256 px')
    check('S86', 'school system' in s['notes'][0] and 'state, county, city or township' in s['notes'][0], 'school systems run by a state, county, city or township (note, row 116)')
    check('S86', g['Independent school district governments'] == 12546 and '12,546 independent school districts' in s['notes'][0].replace('\u00a0', ' '), '12,546 independent school districts (note)')


def regions():
    rows = read_csv('census-acs-health-coverage-overlap')
    types = {r['measure_code']: r for r in read_csv('census-acs-health-coverage-types')}
    return {r['region']: r for r in rows}, types


def s87_s88():
    reg, types = regions()
    a, ab, b, no = (int(reg[k]['people']) for k in ('Private coverage only', 'Both private and public coverage', 'Public coverage only', 'No health insurance coverage'))
    total = int(types['DP03_0095']['people'])
    for sid in ('S87', 'S88'):
        check(sid, a + ab + b + no == total == 336838154, 'four regions sum to the population, 336,838,154')
        check(sid, a + ab == int(types['DP03_0097']['people']) and b + ab == int(types['DP03_0098']['people']), 'private and public totals equal the published counts')
    shares = {k: round(float(reg[k]['pct']), 1) for k in reg}
    check('S87', [millions(v) for v in (a, b, ab, no)] == ['189.4 million', '95.4 million', '23.8 million', '28.3 million'], 'four counts in millions')
    t = spec('S87')['title'].replace(' ', ' ')
    check('S87', all(x in t for x in ('189.4 million', '95.4 million', '23.8 million', '28.3 million', '2025')), 'title: the four counts, 2025')
    alt = spec('S87')['alt'].replace(' ', ' ')
    check('S87', all(f'{shares[k]:.1f} percent' in alt for k in reg) and '336.8 million' in alt, 'alt: the four shares and everyone, 336.8 million')
    check('S87', sorted(shares.values()) == [7.1, 8.4, 28.3, 56.2] and round(sum(shares.values()), 1) == 100.0, 'shares 56.2, 28.3, 7.1 and 8.4 percent, summing to 100.0')
    # DR-64: no region ranked against another unless the gap passes its margin; every pair passes
    m = {k: int(reg[k]['people_moe_approx']) for k in reg}
    p = {k: int(reg[k]['people']) for k in reg}
    ks = list(reg)
    worst = min(abs(p[x] - p[y]) / math.sqrt(m[x] ** 2 + m[y] ** 2) for i, x in enumerate(ks) for y in ks[i + 1:])
    for sid in ('S87', 'S88'):
        check(sid, worst > 1, f'every gap between two regions passes its margin (closest: {worst:.1f} times)')
    s = spec('S88')
    t = s['title'].replace(' ', ' ')
    check('S88', all(x in t for x in (millions(a + ab), millions(b + ab), millions(ab), '2025')) and millions(a + ab) == '213.2 million' and millions(b + ab) == '119.1 million', 'title: 213.2 million private, 119.1 million public, 23.8 million both (MA-8)')
    alt = s['alt'].replace(' ', ' ')
    check('S88', all(x in alt for x in ('213.2 million', '119.1 million', '23.8 million', '189.4 million', '95.4 million', '28.3 million')), 'alt: totals and regions')
    check('S88', '336.8 million' in s['measure_line'] and 'frame' not in s['labels'], 'everyone in the measure line, no frame (data lead condition)')
    # the Euler's geometry, as the form computes it: radii by area, the distance that gives the shared area, the third
    # circle at least its own radius apart
    ub, uc = math.sqrt((b + ab) / (a + ab)), math.sqrt(no / (a + ab))
    want = math.pi * ab / (a + ab)

    def lens(r1, r2, d):
        if d >= r1 + r2:
            return 0.0
        return (r1 * r1 * math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1)) + r2 * r2 * math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2))
                - 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)))
    lo, hi = abs(1 - ub), 1 + ub
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if lens(1, ub, mid) > want else (lo, mid)
    d = (lo + hi) / 2
    for r in (40, 60, 84, 96, 124, 132):
        got = lens(r, r * ub, r * d) / (math.pi * r * r) * (a + ab)
        check('S88', abs(got - ab) <= 0.01 * ab, f'shared area within 1 percent of 23,775,140 at a {r} px radius ({got:,.0f})')
    check('S88', abs((ub ** 2) - (b + ab) / (a + ab)) < 1e-9 and abs((uc ** 2) - no / (a + ab)) < 1e-9, 'every circle by area on one scale')


if __name__ == '__main__':
    if '--figures' not in sys.argv:
        print(__doc__)
        sys.exit(0)
    s85()
    s86()
    s87_s88()
    for f in FAULTS:
        print('FAIL', f)
    print(f'{COUNT[0]} checks, {len(FAULTS)} failed')
    sys.exit(1 if FAULTS else 0)
