"""Add the stretch test's six specimens (S11 to S16, D2-115) to the shared chart dataset.

Usage:
    python3 -I work/build/scripts/phase-2/dataviz_stretch_data.py

Reads the committed work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json and the research lead's CSVs in
shared/public/ (fec-presidential-results-by-state, fred-payrolls-by-sector, census-cps-2024-turnout-by-state, each
with a .meta.json sidecar), and writes the dataset back with the stretch datasets and specimens added. It needs no
V7 extract, so a fresh clone can run it. A dataset whose CSV is missing is marked pending. Run it again after
dataviz_shared_data.py, which rebuilds the file from V7 and drops these additions.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
SHARED = ROOT / 'work/boards/phase-2/data-viz/shared'
OUT = SHARED / '20261106_Chart-Data.json'
PUB = SHARED / 'public'
D = json.loads(OUT.read_text())
DS = D['datasets']


def load(stem):
    p = PUB / f'{stem}.csv'
    if not p.exists():
        return None, None
    rows = list(csv.DictReader(p.open(newline='')))
    meta_p = PUB / f'{stem}.meta.json'
    return rows, (json.loads(meta_p.read_text()) if meta_p.exists() else {})


def num(v):
    try:
        return float(str(v).replace(',', ''))
    except (TypeError, ValueError):
        return None


def pending(did, spec, stem):
    DS[did] = {'spec': spec, 'kind': 'public', 'pending': True, 'title': f'waiting for {stem}.csv'}


# S11, S12, S15: presidential margin by state, 2020 and 2024 (FEC). margin_pts > 0 means a Republican lead.
rows, meta = load('fec-presidential-results-by-state')
if rows:
    by = {}
    for r in rows:
        by.setdefault(r['code'], {'code': r['code'], 'name': r['name']})[int(float(r['year']))] = r
    out = []
    for code, s in sorted(by.items()):
        if 2020 in s and 2024 in s:
            m20, m24 = num(s[2020]['margin_pts']), num(s[2024]['margin_pts'])
            out.append({'key': code, 'code': code, 'name': s['name'], 'margin_2020': m20, 'margin_2024': m24,
                        'shift_pts': round(m24 - m20, 2) if m20 is not None and m24 is not None else None,
                        'dem_pct_2024': num(s[2024]['dem_pct']), 'rep_pct_2024': num(s[2024]['rep_pct']),
                        'total_votes_2024': num(s[2024]['total_votes'])})
    nat = {}
    for r in rows:
        y = int(float(r['year']))
        t = nat.setdefault(y, [0, 0, 0])
        t[0] += num(r['total_votes']); t[1] += num(r['dem_votes']); t[2] += num(r['rep_votes'])
    shares = {y: (round(100 * d / tv, 2), round(100 * rp / tv, 2), round(100 * (rp - d) / tv, 2)) for y, (tv, d, rp) in nat.items()}
    national = {'key': 'US', 'code': 'US', 'name': 'United States', 'scope': 'nation',
                'margin_2020': shares[2020][2], 'margin_2024': shares[2024][2], 'shift_pts': round(shares[2024][2] - shares[2020][2], 2),
                'dem_pct_2024': shares[2024][0], 'rep_pct_2024': shares[2024][1], 'total_votes_2024': nat[2024][0]}
    DS['presidential-shift-by-state'] = {
        'spec': 'S11', 'kind': 'public', 'title': 'Presidential margin by state, 2020 and 2024', 'evidence': 'Finding',
        'grade': 'official results', 'key': 'key', 'value_field': 'shift_pts', 'rows': out,
        'required_keys': [r['key'] for r in out], 'source_line': meta.get('source_line'), 'source_tokens': ['Federal Election Commission'],
        'meta': dict(meta, rounding='shift_pts is the difference of the margins as rounded to two decimals in the FEC file\'s shares; in nine states it differs by 0.01 from the difference of unrounded shares (Washington 0.98 against 0.985). No figure printed to one decimal changes (D2-126).'),
        'extra_rows': [national],
        'notes': ['margin_pts is Republican share minus Democratic share, so a positive margin is a Republican lead and a positive shift moved toward Republicans.',
                  'extra_rows holds the United States, summed from the state rows\' vote counts, which match the FEC national totals: it is context for a chart, never one of the 51 rows a chart must draw (D2-126).',
                  'Party marks take neutral inks with the party name printed; arrows, position and words carry direction (DR-48, DR-58). Never Pillar Red or Prussian for a party.',
                  'Marks: data-field="margin_2020" and "margin_2024" for the two ends of an arrow; data-value carries the number.']}
else:
    pending('presidential-shift-by-state', 'S11', 'fec-presidential-results-by-state')

# S13, S14: payrolls by sector (FRED copies of BLS series)
rows, meta = load('fred-payrolls-by-sector')
if rows:
    series = {}
    for r in rows:
        series.setdefault(r['series_id'], []).append(r)
    out, change = [], []
    for sid, rs in series.items():
        rs.sort(key=lambda r: r['date'])
        base = next((num(r['employees_thousands']) for r in rs if r['date'].startswith('2022-01')), None)
        for r in rs:
            v = num(r['employees_thousands'])
            out.append({'key': f"{sid}|{r['date'][:7]}", 'series_id': sid, 'sector': r['sector'], 'date': r['date'][:10],
                        'employees_thousands': v, 'pct_change_since_2022_01': round((v / base - 1) * 100, 2) if base and v is not None else None,
                        'change_since_2022_01_thousands': round(v - base, 1) if base and v is not None else None})
        if sid == 'PAYEMS':
            vals = [(r['date'][:7], num(r['employees_thousands'])) for r in rs]
            diffs = [(vals[i][0], round(vals[i][1] - vals[i - 1][1], 1)) for i in range(1, len(vals)) if vals[i][1] is not None and vals[i - 1][1] is not None]
            for i, (dt, d) in enumerate(diffs):
                w = [x for _, x in diffs[max(0, i - 2):i + 1]]
                change.append({'key': dt, 'date': dt, 'change_thousands': d, 'avg3_thousands': round(sum(w) / len(w), 1) if len(w) == 3 else None})
    latest = {}
    for r in out:
        if r['date'] >= latest.get(r['series_id'], ('', None))[0]:
            latest[r['series_id']] = (r['date'], r['key'])
    REV = ('Seasonally adjusted. The Bureau of Labor Statistics revises each month\'s first estimate in the next two monthly reports, '
           'so August and September 2026 are preliminary, and a yearly benchmark revision can move earlier months.')
    meta = dict(meta, qualification=REV + ' FRED copies the Bureau of Labor Statistics series; bls.gov refuses automated requests, so the studio read FRED (DR-60).',
                revision_basis='BLS Employment Situation technical note and CES benchmark notes, read as search snippets from bls.gov on November 6, 2026 (bls.gov refuses automated page reads): the establishment survey revises its initial monthly estimates twice, in the immediately succeeding two months, and a yearly benchmark re-anchors the series to unemployment insurance tax records (D2-126)')
    LINE = ('Source: U.S. Bureau of Labor Statistics, Current Employment Statistics, {what}, seasonally adjusted, January 2022 to September 2026, '
            'United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 6, 2026. August and September 2026 are preliminary and will be revised.')
    DS['payrolls-by-sector'] = {
        'spec': 'S13', 'kind': 'public', 'title': 'Payroll employment by sector, monthly', 'evidence': 'Finding', 'grade': 'official statistic',
        'key': 'key', 'value_field': 'pct_change_since_2022_01', 'rows': out,
        'required_keys': [k for _, k in latest.values()], 'source_line': LINE.format(what='all employees by industry'), 'source_tokens': ['FRED'],
        'meta': meta, 'notes': ['FRED copies Bureau of Labor Statistics series; the source line names both (DR-60).',
                                'Sparklines plot pct_change_since_2022_01; the end label prints change_since_2022_01_thousands in words such as "+3.8 million".']}
    DS['payrolls-monthly-change'] = {
        'spec': 'S14', 'kind': 'public', 'title': 'Monthly change in total nonfarm payrolls', 'evidence': 'Finding', 'grade': 'official statistic',
        'key': 'key', 'value_field': 'change_thousands', 'rows': change,
        'required_keys': [r['key'] for r in change if r['date'] >= '2022-01'], 'source_line': LINE.format(what='all nonfarm employees, monthly change'), 'source_tokens': ['FRED'],
        'meta': meta, 'notes': ['avg3_thousands is the three-month moving average ending in that month (the studio computes it from the monthly change).',
                                'Both jobs charts draw January 2022 to September 2026, one window for both (D2-126). Never split a period at January 2025 or at any inauguration date (fix pass F2).',
                                'Mark a month with no release, if any, as a gap with a note; never bridge it (R16).']}
else:
    pending('payrolls-by-sector', 'S13', 'fred-payrolls-by-sector')
    pending('payrolls-monthly-change', 'S14', 'fred-payrolls-by-sector')

# S16: turnout and eligible voters by state, 2024 (Census CPS)
rows, meta = load('census-cps-2024-turnout-by-state')
if rows:
    out = [{'key': r['code'], 'code': r['code'], 'name': r['name'], 'voted_pct': num(r['voted_pct']),
            'citizen_vap_thousands': num(r['citizen_vap_thousands']), 'moe_pct': num(r.get('moe_pct'))}
           for r in rows if str(r.get('year', '2024')).startswith('2024')]
    DS['turnout-by-state-2024'] = {
        'spec': 'S16', 'kind': 'public', 'title': 'Reported turnout and eligible voters by state, 2024', 'evidence': 'Finding',
        'grade': 'official statistic', 'key': 'key', 'value_field': 'voted_pct', 'rows': out, 'required_keys': [r['key'] for r in out],
        'source_line': meta.get('source_line'), 'source_tokens': ['Census Bureau'], 'meta': meta,
        'notes': ['Bubble area, never radius, is proportional to citizen_vap_thousands (data-field="citizen_vap_thousands").',
                  'Rates are self-reported and run higher than counted ballots; say so on the chart.']}
else:
    pending('turnout-by-state-2024', 'S16', 'census-cps-2024-turnout-by-state')

STRETCH = [
    ('S11', 'Shift arrows', 'presidential-shift-by-state', 'Which states moved toward which party between 2020 and 2024, and how far?',
     'One arrow per state from its 2020 margin to its 2024 margin; party direction in words and position; neutral inks (DR-58).'),
    ('S12', 'Tile-grid map with shift arrows', 'presidential-shift-by-state', 'Where did the shift happen?',
     'One tile per state on the shared tile grid, an arrow in each whose angle and length follow the shift; a size-of-shift key.'),
    ('S13', 'Small-multiple sparklines', 'payrolls-by-sector', 'Which sectors added jobs since January 2022, and which lost them?',
     'One panel per sector on a shared scale, an end label with the change in words, a line at zero.'),
    ('S14', 'Columns with a moving average', 'payrolls-monthly-change', 'How many jobs did the economy add each month?',
     'Monthly change as columns from zero in Stone, the three-month average as a Charcoal line, the latest month labeled.'),
    ('S15', 'Results table', 'presidential-shift-by-state', 'How did each state vote in 2024, and how did that compare with 2020?',
     'Margin cells with party names printed, a shift column with arrows, sortable on the atlas site, readable as cards on a phone.'),
    ('S16', 'Bubble map', 'turnout-by-state-2024', 'Where did eligible voters turn out, and where are most of them?',
     'Circles by area for citizen voting-age population, shaded by turnout in one sequential ink, labeled where they fit.'),
]
D['specimens'] = [s for s in D['specimens'] if s['id'] not in {x[0] for x in STRETCH}]
D['specimens'] += [{'id': i, 'form': f, 'dataset': ds, 'reader_question': q, 'requirements': req, 'evidence': 'Finding', 'stretch': True}
                   for i, f, ds, q, req in STRETCH]
OUT.write_text(json.dumps(D, indent=1, ensure_ascii=False))
pend = [k for k in ('presidential-shift-by-state', 'payrolls-by-sector', 'payrolls-monthly-change', 'turnout-by-state-2024') if DS[k].get('pending')]
print(f'wrote {OUT.relative_to(ROOT)}: {len(D["specimens"])} specimens; stretch pending: {pend or "none"}')
