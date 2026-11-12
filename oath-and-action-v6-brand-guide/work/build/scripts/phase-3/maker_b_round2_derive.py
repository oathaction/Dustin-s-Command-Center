"""Maker B, Phase 3 round 2: R2-2's derived summaries for S49, S51 and S52 (D3-652, contract C1).

    python3 -I work/build/scripts/phase-3/maker_b_round2_derive.py [--check] [--figures]

Reads three frozen files in work/build/data/ and writes four derived tables with their sidecars, by the data lead's
ruling (g) of November 12, 2026 (work/handoffs/phase-3/20261112_Round-2-Data-Lead-Notes.md):

- fjc-article-iii-judges-years-bins: two-year bins of years as a federal judge, closed on the left, 0 to 44 (S49)
- census-sahie-county-uninsured-box-by-region: Tukey's box for county uninsured rates in each Census region (S51)
- census-sahie-county-uninsured-outliers: each county past its region's whiskers (S51)
- census-saipe-county-child-poverty-bins: two-point bins of county child poverty, 2019 and 2024, closed on the left,
  0 to 74 (S52)
- fred-unemployment-and-job-openings-quarterly: quarterly averages of the two monthly series, first quarter of 2001 to
  third quarter of 2026, with no unemployment average for a quarter that lacks a month's rate (S56; the monthly table of
  310 rows put the plate over its far-over limit, so the chart draws the quarters)

Each county or judge counts once. Quartiles are Python's statistics.quantiles(method="inclusive"), linear
interpolation between ranked values. Prints every figure a title or note may use. --check writes nothing and fails
when a written file differs from what the script computes now. --figures writes nothing and checks every figure in the
titles, notes, alts and labels of specs S49 to S59 against the data files, each check named in the spec's notes_internal
(check S49 to check S59). Standard library only.
"""
import csv
import io
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data'))
CHECK = '--check' in sys.argv


def read(name):
    with open(os.path.join(DATA, name + '.csv'), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def meta(name):
    with open(os.path.join(DATA, name + '.meta.json'), encoding='utf-8') as fh:
        return json.load(fh)


def num(s):
    return float(s) if s not in (None, '') else None


def fmt(v):
    """A number as the CSV holds it: integers bare, others to four decimals with trailing zeros dropped."""
    if isinstance(v, int):
        return str(v)
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return s


def csv_text(columns, rows):
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n')
    w.writerow(columns)
    for r in rows:
        w.writerow([fmt(r[c]) if isinstance(r[c], (int, float)) else r[c] for c in columns])
    return out.getvalue()


FAULTS = []


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
    print(('checked ' if CHECK else 'wrote ') + name + ' (%d rows)' % len(rows))


def base_side(src, name, **over):
    """A derived sidecar from its source's: C1's required fields, with kind, derived_from and derivation."""
    m = meta(src)
    side = {
        'file': name + '.csv',
        'kind': 'derived',
        'publisher': m['publisher'],
        'title_or_table': m['title_or_table'],
        'table_id': m['table_id'],
        'url': m['url'],
        'observation_period': m['observation_period'],
        'geography': m['geography'],
        'universe_or_base': m['universe_or_base'],
        'unit': '',
        'date_retrieved': m['date_retrieved'],
        'vintage': m['vintage'],
        'qualification': m['qualification'],
        'columns': {},
        'printed_source_line': '',
        'ledger_row': m['ledger_row'],
        'domain': m['domain'],
        'states': [],
        'derived_from': [src + '.csv'],
        'derivation': '',
    }
    side.update(over)
    return side


# ---------------------------------------------------------------------------------------------------------------
# S49: judges, two-year bins of years as a federal judge (ruling (g))
# ---------------------------------------------------------------------------------------------------------------
def judges():
    src = 'fjc-article-iii-judges'
    rows = read(src)
    # the unit is the judge, counted once by FJC ID (nid): four judges in shared judgeships hold two or three service
    # records, each with the same first commission and so the same years (the data lead's corrected ruling (g))
    by = {}
    for r in rows:
        by.setdefault(r['nid'], []).append(num(r['years_as_federal_judge']))
    assert all(len(set(v)) == 1 for v in by.values()), 'a judge with differing years on two records'
    shared = sorted(k for k, v in by.items() if len(v) > 1)
    yrs = [v[0] for v in by.values()]
    assert all(v is not None for v in yrs), 'a judge has no years'
    lo, hi, step = 0, 44, 2
    assert max(yrs) < hi, 'a judge past the last bin'
    bins = []
    for a in range(lo, hi, step):
        n = sum(1 for v in yrs if a <= v < a + step)
        bins.append({'bin_start': a, 'bin_end': a + step, 'label': '%d to under %d years' % (a, a + step), 'judges': n})
    assert sum(b['judges'] for b in bins) == len(yrs)
    med = statistics.median(yrs)
    name = src + '-years-bins'
    side = base_side(src, name,
        universe_or_base=('Judges in active service, each counted once by FJC ID: %d judges from the export\'s %d service records of '
                          'Article III judges with no senior-status or termination date' % (len(yrs), len(rows))),
        unit='judges in active service in each two-year bin of years as a federal judge; bin_start and bin_end in years',
        columns={
            'bin_start': {'type': 'number', 'description': 'lower edge of the bin, in the bin', 'unit': 'years'},
            'bin_end': {'type': 'number', 'description': 'upper edge of the bin, not in the bin', 'unit': 'years'},
            'label': {'type': 'text', 'description': 'the bin in words'},
            'judges': {'type': 'integer', 'description': 'judges whose years as a federal judge fall in the bin', 'unit': 'judges'},
        },
        printed_source_line=('Source: Federal Judicial Center, Biographical Directory of Article III Federal Judges, judges in active '
                             'service, as of November 11, 2026, United States. Retrieved November 11, 2026. Judges on senior status '
                             'are not counted; years as a federal judge computed from first commission dates and grouped in two-year '
                             'bins by Oath & Action.'),
        derivation=('Each judge in active service counted once by FJC ID (nid) in the two-year bin, closed on the left, that holds '
                    'the years since the first Article III commission, from 0 to 44 years (the data lead\'s corrected ruling (g), round 2)'),
        notes=['%d judges in all, from %d service records; median %.2f years as a federal judge (Python statistics.median of the unrounded years)' % (len(yrs), len(rows), med),
               'Judges with more than one service record, in shared judgeships across districts (FJC IDs): ' + ', '.join(shared),
               'Bin edges checked against inauguration dates: January 20 of 2001, 2009, 2017, 2021 and 2025 sit 25.81, 17.81, 9.81, '
               '5.81 and 1.81 years before November 11, 2026, so no edge falls on one (H09)'])
    write(name, ['bin_start', 'bin_end', 'label', 'judges'], bins, side)
    print('  S49 judges %d from %d records (shared: %s), median %.4f, counts %s, largest bin %s' % (len(yrs), len(rows), shared, med, [b['judges'] for b in bins], max(bins, key=lambda b: b['judges'])))
    return med


# ---------------------------------------------------------------------------------------------------------------
# S51: county uninsured rates by region, Tukey's box (ruling (g))
# ---------------------------------------------------------------------------------------------------------------
REGIONS = ['Northeast', 'Midwest', 'South', 'West']


def uninsured():
    src = 'census-sahie-county-uninsured'
    rows = read(src)
    missing = [r['county'] for r in rows if num(r['uninsured_pct']) is None]
    box, outs = [], []
    for reg in REGIONS:
        rr = [r for r in rows if r['region'] == reg and num(r['uninsured_pct']) is not None]
        v = sorted(num(r['uninsured_pct']) for r in rr)
        q1, md, q3 = statistics.quantiles(v, n=4, method='inclusive')
        iqr = q3 - q1
        lf, hf = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        inside = [x for x in v if lf <= x <= hf]
        ol = sorted([r for r in rr if not (lf <= num(r['uninsured_pct']) <= hf)], key=lambda r: (-num(r['uninsured_pct']), r['geoid']))
        box.append({'region': reg, 'counties': len(v), 'minimum': v[0], 'whisker_low': min(inside), 'q1': round(q1, 4),
                    'median': round(md, 4), 'q3': round(q3, 4), 'whisker_high': max(inside), 'maximum': v[-1], 'outliers': len(ol)})
        for r in ol:
            outs.append({'region': reg, 'geoid': r['geoid'], 'county': r['county'], 'code': r['code'], 'uninsured_pct': num(r['uninsured_pct'])})
    name = src + '-box-by-region'
    line = ('Source: U.S. Census Bureau, Small Area Health Insurance Estimates, people under 65 without health insurance, 2024, '
            'counties in the 50 states and DC. Retrieved November 11, 2026. Model-based estimates; small counties carry wide '
            'margins of error; each region’s quartiles, whiskers and outliers computed by Oath & Action.')
    side = base_side(src, name,
        geography='Counties and county equivalents in the 50 states and DC with an estimate, by Census region',
        unit=('percent of people under 65 without health insurance; counties and outliers in counties. Quartiles by linear '
              'interpolation between ranked counties; whiskers at the last county inside 1.5 times the middle half'),
        columns={
            'region': {'type': 'category', 'description': 'Census region'},
            'counties': {'type': 'integer', 'description': 'counties with an estimate, each counted once', 'unit': 'counties'},
            'minimum': {'type': 'number', 'description': 'lowest county rate', 'unit': 'percent'},
            'whisker_low': {'type': 'number', 'description': 'lowest county rate at or above the lower fence', 'unit': 'percent'},
            'q1': {'type': 'number', 'description': 'first quartile', 'unit': 'percent'},
            'median': {'type': 'number', 'description': 'median county rate', 'unit': 'percent'},
            'q3': {'type': 'number', 'description': 'third quartile', 'unit': 'percent'},
            'whisker_high': {'type': 'number', 'description': 'highest county rate at or below the upper fence', 'unit': 'percent'},
            'maximum': {'type': 'number', 'description': 'highest county rate', 'unit': 'percent'},
            'outliers': {'type': 'integer', 'description': 'counties past a fence', 'unit': 'counties'},
        },
        printed_source_line=line,
        derivation=('For each Census region, the counties with an estimate, each counted once: quartiles by Python\'s '
                    'statistics.quantiles (method inclusive), fences at 1.5 times the middle half past each quartile, whiskers '
                    'at the last county inside them, and a count of the counties past them (Tukey\'s box, the data lead\'s ruling (g))'),
        notes=['Counties with no estimate, left out: ' + '; '.join(missing)])
    write(name, ['region', 'counties', 'minimum', 'whisker_low', 'q1', 'median', 'q3', 'whisker_high', 'maximum', 'outliers'], box, side)
    name2 = src + '-outliers'
    side2 = base_side(src, name2,
        geography='The counties past their region\'s whiskers, in the 50 states and DC',
        unit='percent of people under 65 without health insurance',
        columns={
            'region': {'type': 'category', 'description': 'Census region'},
            'geoid': {'type': 'id', 'description': 'county FIPS code'},
            'county': {'type': 'text', 'description': 'county name with its state, as the Bureau prints it'},
            'code': {'type': 'code', 'description': 'USPS state code'},
            'uninsured_pct': {'type': 'number', 'description': 'percent of people under 65 without health insurance', 'unit': 'percent'},
        },
        printed_source_line=line,
        derivation=('The counties whose rate falls past their region\'s fences, 1.5 times the middle half beyond the first or '
                    'third quartile, by the same quartiles as census-sahie-county-uninsured-box-by-region'),
        notes=['Every outlier lies above its region\'s box' if all(o['uninsured_pct'] > [b for b in box if b['region'] == o['region']][0]['q3'] for o in outs) else 'Outliers lie on both sides'])
    write(name2, ['region', 'geoid', 'county', 'code', 'uninsured_pct'], outs, side2)
    for b in box:
        print('  S51 %(region)s counties %(counties)d min %(minimum)s whisker %(whisker_low)s q1 %(q1)s median %(median)s q3 %(q3)s whisker %(whisker_high)s max %(maximum)s outliers %(outliers)d' % b)
    print('  S51 outliers %d; missing %s' % (len(outs), missing))
    return box


# ---------------------------------------------------------------------------------------------------------------
# S52: county child poverty, two-point bins, 2019 and 2024 (ruling (g))
# ---------------------------------------------------------------------------------------------------------------
def child_poverty():
    src = 'census-saipe-county-child-poverty'
    rows = read(src)
    out, med = [], {}
    lo, hi, step = 0, 74, 2
    for yr in ('2019', '2024'):
        v = [num(r['child_poverty_pct']) for r in rows if r['year'] == yr and num(r['child_poverty_pct']) is not None]
        miss = [r['county'] + ', ' + r['code'] for r in rows if r['year'] == yr and num(r['child_poverty_pct']) is None]
        assert max(v) < hi, 'a county past the last bin'
        med[yr] = (len(v), statistics.median(v), miss)
        for a in range(lo, hi, step):
            out.append({'year': int(yr), 'bin_start': a, 'bin_end': a + step, 'label': '%d to under %d percent' % (a, a + step),
                        'counties': sum(1 for x in v if a <= x < a + step)})
        assert sum(o['counties'] for o in out if o['year'] == int(yr)) == len(v)
    name = src + '-bins'
    side = base_side(src, name,
        unit='counties in each two-point bin of the share of people under 18 in poverty; bin_start and bin_end in percent',
        columns={
            'year': {'type': 'year', 'description': 'calendar year of the estimate'},
            'bin_start': {'type': 'number', 'description': 'lower edge of the bin, in the bin', 'unit': 'percent'},
            'bin_end': {'type': 'number', 'description': 'upper edge of the bin, not in the bin', 'unit': 'percent'},
            'label': {'type': 'text', 'description': 'the bin in words'},
            'counties': {'type': 'integer', 'description': 'counties whose estimate falls in the bin, each counted once', 'unit': 'counties'},
        },
        printed_source_line=('Source: U.S. Census Bureau, Small Area Income and Poverty Estimates, people under 18 in poverty, 2019 '
                             'and 2024, counties in the 50 states and DC. Retrieved November 11, 2026. Model-based estimates under '
                             'the official poverty measure, which leaves out tax credits; counties grouped in two-point bins by '
                             'Oath & Action.'),
        derivation=('For each year, every county with an estimate counted once in the two-point bin, closed on the left, that '
                    'holds its share of people under 18 in poverty, from 0 to 74 percent, the same edges for both years (the '
                    'data lead\'s ruling (g))'),
        notes=['%s: %d counties, median %.2f percent; no estimate: %s' % (y, med[y][0], med[y][1], '; '.join(med[y][2]) or 'none') for y in ('2019', '2024')])
    write(name, ['year', 'bin_start', 'bin_end', 'label', 'counties'], out, side)
    for y in ('2019', '2024'):
        yr_rows = [o for o in out if o['year'] == int(y)]
        print('  S52 %s counties %d median %.4f modal bin %s missing %s' % (y, med[y][0], med[y][1], max(yr_rows, key=lambda o: o['counties']), med[y][2]))
    return med


# ---------------------------------------------------------------------------------------------------------------
# S56: unemployment and job openings, quarterly averages (maker B's call; the data lead signs off)
# ---------------------------------------------------------------------------------------------------------------
QWORDS = {1: 'First', 2: 'Second', 3: 'Third', 4: 'Fourth'}
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def openings_quarterly():
    src = 'fred-unemployment-and-job-openings'
    rows = {r['month']: r for r in read(src)}
    out = []
    for yr in range(2001, 2027):
        for q in (1, 2, 3, 4):
            months = ['%d-%02d' % (yr, 3 * (q - 1) + m) for m in (1, 2, 3)]
            if any(m not in rows for m in months):
                continue
            u = [num(rows[m]['unemployment_rate']) for m in months]
            o = [num(rows[m]['job_openings_thousands']) for m in months]
            if any(v is None for v in o):
                continue   # the last quarter with job openings for all three months ends the file
            miss = [m for m, v in zip(months, u) if v is None]
            out.append({'quarter': '%d-Q%d' % (yr, q), 'quarter_start': months[0], 'label': '%s quarter of %d' % (QWORDS[q], yr),
                        'unemployment_rate': round(sum(u) / 3, 4) if not miss else '', 'job_openings_millions': round(sum(o) / 3000, 4),
                        'note': ('no average: no unemployment rate was published for ' + ', '.join(MONTHS[int(m[5:]) - 1] + ' ' + m[:4] for m in miss)) if miss else ''})
    name = src + '-quarterly'
    side = base_side(src, name,
        observation_period='Quarterly averages, first quarter of 2001 to third quarter of 2026',
        unit=('unemployment_rate in percent and job_openings_millions in millions of openings, each the average of the '
              'quarter\'s three seasonally adjusted monthly values, rounded to four decimals'),
        columns={
            'quarter': {'type': 'id', 'description': 'calendar quarter, such as 2001-Q1'},
            'quarter_start': {'type': 'month', 'description': 'the quarter\'s first month'},
            'label': {'type': 'text', 'description': 'the quarter in words'},
            'unemployment_rate': {'type': 'number', 'description': 'average of the three monthly rates; empty where a month has none', 'unit': 'percent'},
            'job_openings_millions': {'type': 'number', 'description': 'average of the three monthly counts, in millions', 'unit': 'millions of openings'},
            'note': {'type': 'text', 'description': 'why a cell is empty'},
        },
        printed_source_line=('Source: U.S. Bureau of Labor Statistics, Current Population Survey and Job Openings and Labor Turnover '
                             'Survey, releases for October 2026 (November 6, 2026) and September 2026 (November 3, 2026), '
                             'unemployment rate and job openings, seasonally adjusted, 2001 to 2026, United States, via FRED, '
                             'Federal Reserve Bank of St. Louis. Retrieved November 11, 2026. Quarterly averages computed by '
                             'Oath & Action; no unemployment rate was published for October 2025, so the fourth quarter of 2025 '
                             'has no average; recent months are preliminary and will be revised.'),
        derivation=('For each calendar quarter from the first of 2001 to the third of 2026 in which job openings cover all three '
                    'months, the average of the three monthly values of each series (job openings in millions); a quarter '
                    'with a month that has no unemployment rate takes no unemployment average'),
        notes=['The monthly file starts job openings in December 2000; the first full quarter is the first of 2001. October 2026\'s '
               'unemployment rate is left out, since its quarter is not complete'])
    write(name, ['quarter', 'quarter_start', 'label', 'unemployment_rate', 'job_openings_millions', 'note'], out, side)
    have = [o for o in out if o['unemployment_rate'] != '']
    print('  S56 quarters %d (%s to %s); no average: %s' % (len(out), out[0]['quarter'], out[-1]['quarter'], [o['quarter'] for o in out if o['unemployment_rate'] == '']))
    print('  S56 openings peak %s; rate peak %s; last %s' % (max(out, key=lambda o: o['job_openings_millions']), max(have, key=lambda o: o['unemployment_rate']), out[-1]))


# ---------------------------------------------------------------------------------------------------------------
# --figures: every figure maker B's round 2 specs print, read from the data
# ---------------------------------------------------------------------------------------------------------------
SPECS = os.path.normpath(os.path.join(HERE, '..', '..', 'chart-kit', 'specs'))


def spec_words(sid):
    with open(os.path.join(SPECS, sid + '.json'), encoding='utf-8') as fh:
        sp = json.load(fh)
    words = [sp.get('title', ''), sp.get('measure_line', ''), sp.get('reading_guide', ''), sp.get('alt', '')] + sp.get('notes', []) + sp.get('chart_notes', [])
    return sp, ' '.join(words)


def figures():
    bad = []

    def want(sid, text, piece, why):
        if piece not in text:
            bad.append('%s: "%s" missing (%s)' % (sid, piece, why))

    def same(sid, a, b, why):
        if a != b:
            bad.append('%s: %r is not %r (%s)' % (sid, a, b, why))
    # S49
    sp, t = spec_words('s49')
    bins = read('fjc-article-iii-judges-years-bins')
    js = read('fjc-article-iii-judges')
    by = {}
    for r in js:
        by.setdefault(r['nid'], num(r['years_as_federal_judge']))
    med = statistics.median(by.values())
    same('S49', sum(int(b['judges']) for b in bins), len(by), 'bins sum to the judges')
    want('S49', t, '%d federal judges' % len(by), 'judges counted once')
    want('S49', t, 'median of %.1f years' % med, 'median')
    same('S49', round(sp['labels']['marker']['value'], 4), round(med, 4), 'the marker is the median')
    top = max(bins, key=lambda b: int(b['judges']))
    want('S49', t, '%s to under %s years, holds %s of the %d judges' % (top['bin_start'], top['bin_end'], top['judges'], len(by)), 'tallest bin')
    want('S49', t, 'four who serve more than one district', 'shared judgeships')
    same('S49', len(js) - len(by), 5, 'four judges hold five extra records')
    # S50
    sp, t = spec_words('s50')
    stc = [r for r in read('census-stc-state-tax-collections') if r['code'] not in ('US', 'DC')]
    hi = max(stc, key=lambda r: num(r['taxes_per_resident'])); lo = min(stc, key=lambda r: num(r['taxes_per_resident']))
    us = [r for r in read('census-stc-state-tax-collections') if r['code'] == 'US'][0]
    same('S50', (hi['code'], lo['code'], len(stc)), ('VT', 'AK', 50), 'the ends')
    want('S50', t, 'Vermont collected ${:,.0f}'.format(num(hi['taxes_per_resident'])), 'Vermont')
    want('S50', t, 'Alaska ${:,.0f}'.format(num(lo['taxes_per_resident'])), 'Alaska')
    want('S50', t, '${:,.0f}'.format(num(us['taxes_per_resident'])), 'all 50 states')
    same('S50', round(int(us['total_taxes_thousands']) * 1000 / int(us['population_july_2024']), 2), round(sum(int(r['total_taxes_thousands']) for r in stc) * 1000 / sum(int(r['population_july_2024']) for r in stc), 2), 'the US row sums the 50 states')
    # S51
    sp, t = spec_words('s51')
    box = {r['region']: r for r in read('census-sahie-county-uninsured-box-by-region')}
    outs = read('census-sahie-county-uninsured-outliers')
    meds = {k: num(v['median']) for k, v in box.items()}
    same('S51', max(meds, key=meds.get), 'South', 'highest median')
    want('S51', t, '%.1f percent of people under 65' % meds['South'], 'South median')
    want('S51', t, '7.2 percent in the Northeast, 8.8 in the Midwest, 12.4 in the West and 13.9 in the South', 'alt medians')
    same('S51', ('%.1f' % meds['Northeast'], '%.1f' % meds['Midwest'], '%.2f' % meds['West']), ('7.2', '8.8', '12.35'), 'medians (12.35 prints 12.4, half up)')
    want('S51', t, 'from %.1f to %.1f percent' % (num(box['South']['q1']), num(box['South']['q3']) + 1e-9), 'South middle half')
    want('S51', t, 'All %d counties past a whisker' % len(outs), 'outliers')
    same('S51', all(num(o['uninsured_pct']) > num(box[o['region']]['q3']) for o in outs), True, 'every outlier above its box')
    o1 = max(outs, key=lambda o: num(o['uninsured_pct']))
    want('S51', t, 'Gaines County, Texas, at %.1f percent' % num(o1['uninsured_pct']), 'highest county')
    same('S51', o1['county'], 'Gaines County, TX', 'highest county')
    sah = {r['geoid']: r for r in read('census-sahie-county-uninsured')}
    g = sah[o1['geoid']]
    nxt = sorted([r for r in sah.values() if r['uninsured_pct'] and r['geoid'] != o1['geoid']], key=lambda r: -num(r['uninsured_pct']))
    top2 = [r for r in nxt if num(r['uninsured_pct']) == num(nxt[0]['uninsured_pct'])]
    same('S51', sorted(r['county'] for r in top2), ['Presidio County, TX', 'Starr County, TX'], 'the next counties')
    gap51 = num(g['uninsured_pct']) - num(top2[0]['uninsured_pct'])
    want('S51', t, '%.1f points above the next counties, past both margins' % gap51, 'Gaines over the next')
    same('S51', all(gap51 > (num(g['uninsured_moe']) ** 2 + num(r['uninsured_moe']) ** 2) ** 0.5 for r in top2), True, 'past both margins')
    # S52
    sp, t = spec_words('s52')
    raw = read('census-saipe-county-child-poverty')
    for y, m in (('2019', '18.7'), ('2024', '17.1')):
        v = [num(r['child_poverty_pct']) for r in raw if r['year'] == y and num(r['child_poverty_pct']) is not None]
        same('S52', '%.1f' % statistics.median(v), m, 'median ' + y)
    want('S52', t, 'fell from 18.7 percent in 2019 to 17.1 percent in 2024', 'title')
    for y in ('2019', '2024'):
        v = [num(r['child_poverty_pct']) for r in raw if r['year'] == y and num(r['child_poverty_pct']) is not None]
        same('S52', sp['labels']['medians'][y], round(statistics.median(v), 1), 'median tick ' + y)
    b52a = read('census-saipe-county-child-poverty-bins')
    far = {y: [(b['bin_start'], b['bin_end']) for b in b52a if b['year'] == y and int(b['bin_start']) >= 56 and int(b['counties'])] for y in ('2019', '2024')}
    same('S52', far, {'2019': [('62', '64')], '2024': [('72', '74')]}, 'the counties past 56 percent')
    same('S52', [int(b['counties']) for b in b52a if (b['year'], b['bin_start']) in (('2019', '62'), ('2024', '72'))], [1, 1], 'one county each')
    want('S52', t, 'at 62 to 64 percent in 2019 and 72 to 74 percent in 2024', 'chart note tail')
    b52 = read('census-saipe-county-child-poverty-bins')
    for y, n in (('2019', 3141), ('2024', 3143)):
        same('S52', sum(int(b['counties']) for b in b52 if b['year'] == y), n, 'counties ' + y)
    want('S52', t, '3,141 counties in 2019 and 3,143 in 2024', 'counts')
    for y, lo_ in (('2019', '18'), ('2024', '14')):
        top = max([b for b in b52 if b['year'] == y], key=lambda b: int(b['counties']))
        same('S52', top['bin_start'], lo_, 'modal bin ' + y)
    want('S52', t, 'from 18 to under 20 percent in 2019 to 14 to under 16 percent in 2024', 'modal bins')
    ct = {y: sum(1 for r in raw if r['year'] == y and r['code'] == 'CT') for y in ('2019', '2024')}
    same('S52', (ct['2019'], ct['2024']), (8, 9), 'Connecticut')
    # S53
    sp, t = spec_words('s53')
    pep = read('census-pep-population-by-age-sex')
    band = sum(int(r['population_july_2025']) for r in pep if r['sex'] in ('male', 'female') and 55 <= int(r['age']) <= 64)
    want('S53', t, '%.1f million people aged 55 to 64' % (band / 1e6), 'band')
    same('S53', sp['labels']['band_words'].replace('\u00a0', ' '), 'Ages 55 to %d: %.1f million' % (64, band / 1e6), 'band words')
    same('S53', (sp['labels'].get('named'), 'point' in sp['labels']), ({'from': 55, 'to': 64}, False), 'the band in the subject ink, no red (RF-1)')
    want('S53', t, 'qualify for Medicare at 65', 'title reason (CD B-S3)')
    same('S53', [w for w in ('Red bars', 'red bars', 'are red') if w in t], [], 'no color named for the band (AX S4)')
    # S54 and S55
    rent = {r['code']: r for r in read('census-acs-rent-and-income-by-state')}
    st = [r for k, r in rent.items() if k != 'US']
    share = sorted(st, key=lambda r: -num(r['rent_pct_of_income']))
    a, b = share[0], share[1]
    gap = num(a['rent_pct_of_income']) - num(b['rent_pct_of_income'])
    same('S54', (a['code'], b['code']), ('FL', 'CA'), 'largest share')
    same('S54', gap > (num(a['rent_pct_of_income_moe']) ** 2 + num(b['rent_pct_of_income_moe']) ** 2) ** 0.5, True, 'Florida past California')
    U = rent['US']
    for k in ('CA', 'ND'):
        r = rent[k]
        same('S54', abs(num(r['rent_pct_of_income']) - num(U['rent_pct_of_income'])) > (num(r['rent_pct_of_income_moe']) ** 2 + num(U['rent_pct_of_income_moe']) ** 2) ** 0.5, True, k + ' past the nation')
    c3 = share[:3]
    same('S54', [r['code'] for r in c3], ['FL', 'CA', 'HI'], 'the three highest shares')
    for r in c3[1:]:
        same('S54', num(a['rent_pct_of_income']) - num(r['rent_pct_of_income']) > (num(a['rent_pct_of_income_moe']) ** 2 + num(r['rent_pct_of_income_moe']) ** 2) ** 0.5, True, 'Florida past ' + r['code'])
    nd, wy = share[-1], share[-2]
    same('S54', (nd['code'], wy['code']), ('ND', 'WY'), 'the two smallest shares')
    same('S54', num(wy['rent_pct_of_income']) - num(nd['rent_pct_of_income']) < (num(wy['rent_pct_of_income_moe']) ** 2 + num(nd['rent_pct_of_income_moe']) ** 2) ** 0.5, True, 'Wyoming within North Dakota’s margin')
    for sid in ('s54', 's55'):
        sp, t = spec_words(sid)
        want(sid.upper(), t, 'Florida, 35.5 percent' if sid == 's54' else 'the median renter paid the largest share of income in rent, 35.5 percent', 'title')
        want(sid.upper(), t, 'Florida’s 35.5 percent (margin 0.5) passes the next figures, California’s 32.9 (0.3) and Hawaii’s 32.8 (1.2), by more than their margins', 'note 2')
        want(sid.upper(), t, 'North Dakota has the smallest figure, 23.8 percent (margin 1.2); Wyoming’s 25.5 (2.0) sits within its margin', 'North Dakota')
        same(sid.upper(), sp['scale']['x'][1] > max(num(r['renter_median_income']) for r in st), True, 'the income scale holds every state')
    sp, t = spec_words('s54')
    lr = min(st, key=lambda r: num(r['median_gross_rent'])); hr = max(st, key=lambda r: num(r['median_gross_rent']))
    want('S54', t, 'West Virginia’s ${:,}'.format(int(lr['median_gross_rent'])), 'lowest rent')
    want('S54', t, 'California’s ${:,}'.format(int(hr['median_gross_rent'])), 'highest rent')
    same('S54', (lr['code'], hr['code']), ('WV', 'CA'), 'rent ends')
    sp, t = spec_words('s55')
    want('S55', t, 'home to %.1f million renter households' % (int(rent['FL']['renter_households']) / 1e6), 'Florida households')
    want('S55', t, 'California’s %.1f million renter households' % (int(rent['CA']['renter_households']) / 1e6), 'California households')
    same('S55', max(st, key=lambda r: int(r['renter_households']))['code'], 'CA', 'most renter households')
    # S56
    sp, t = spec_words('s56')
    q = read('fred-unemployment-and-job-openings-quarterly')
    pk = max(q, key=lambda r: num(r['job_openings_millions']))
    same('S56', pk['quarter'], '2022-Q1', 'openings peak')
    want('S56', t, 'openings averaged %.1f million in early 2022, when the rate averaged %.1f percent' % (num(pk['job_openings_millions']), num(pk['unemployment_rate'])), 'title')
    hv = [r for r in q if r['unemployment_rate'] != '']
    ur = max(hv, key=lambda r: num(r['unemployment_rate']))
    want('S56', t, '%.1f percent unemployment in the spring of 2020' % num(ur['unemployment_rate']), 'rate peak')
    same('S56', ur['quarter'], '2020-Q2', 'rate peak')
    want('S56', t, 'near %.1f percent and %.1f million in the latest quarter' % (num(q[-1]['unemployment_rate']), num(q[-1]['job_openings_millions'])), 'latest')
    same('S56', [r['quarter'] for r in q if r['unemployment_rate'] == ''], ['2025-Q4'], 'the gap')
    pre = max([r for r in hv if r['quarter'] < '2020'], key=lambda r: num(r['unemployment_rate']))
    same('S56', pre['quarter'], '2009-Q4', 'the end of 2009, the highest unemployment before 2020')
    want('S56', t, 'the end of 2009, the highest unemployment before 2020', 'chart note reason')
    # S57
    sp, t = spec_words('s57')
    er = read('census-acs-earnings-ratio-by-state')
    us57 = [r for r in er if r['code'] == 'US'][0]
    U, UM = num(us57['women_pct_of_men']), num(us57['women_pct_of_men_moe'])
    past = [r for r in er if r['code'] != 'US' and abs(num(r['women_pct_of_men']) - U) > (num(r['women_pct_of_men_moe']) ** 2 + UM ** 2) ** 0.5]
    above = [r for r in past if num(r['women_pct_of_men']) > U]
    same('S57', (len(past), len(above), len(past) - len(above), 'DC' in [r['code'] for r in above]), (26, 14, 12, True), 'past the margin')
    want('S57', t, '82.0 percent of men’s in 2025, and in 25 states and the District of Columbia', 'title')
    want('S57', t, '13 states and the District of Columbia sit above the nation and 12 states below it', 'note 2')
    want('S57', t, 'Fourteen filled dots above the nation’s line and 12 below it', 'alt')
    want('S57', t, 'the open dots of the other %d states' % (51 - len(past)), 'alt within')
    # S58
    sp, t = spec_words('s58')
    inc = read('census-cps-median-household-income')
    y25 = [r for r in inc if r['year'] == '2025'][0]; y24 = [r for r in inc if r['year'] == '2024'][0]
    same('S58', max(inc, key=lambda r: int(r['median_income']))['year'], '2025', 'highest')
    want('S58', t, '${:,}'.format(int(y25['median_income'])), '2025')
    want('S58', t, '${:,}'.format(int(y25['median_moe'])), '2025 margin')
    g = int(y25['median_income']) - int(y24['median_income']); gm = (int(y25['median_moe']) ** 2 + int(y24['median_moe']) ** 2) ** 0.5
    same('S58', g > gm, True, 'the rise past its margin')
    want('S58', t, '2024’s ${:,}'.format(int(y24['median_income'])), '2024')
    nx = sorted(inc, key=lambda r: -int(r['median_income']))[1]
    same('S58', nx['year'], '2019', 'the next highest year')
    same('S58', int(y25['median_income']) - int(nx['median_income']) > (int(y25['median_moe']) ** 2 + int(nx['median_moe']) ** 2) ** 0.5, True, 'the lead over 2019 past its margin')
    want('S58', t, 'its lead over 2019’s ${:,}, the next highest year'.format(int(nx['median_income'])), 'note 1')
    y13 = sorted(int(r['median_income']) for r in inc if r['year'] == '2013'); y17 = sorted(int(r['median_income']) for r in inc if r['year'] == '2017')
    want('S58', t, '${:,} apart'.format(y13[1] - y13[0]), '2013 gap')
    want('S58', t, '${:,} apart'.format(y17[1] - y17[0]), '2017 gap')
    want('S58', t, '${:,} in 1967'.format(int([r for r in inc if r['year'] == '1967'][0]['median_income'])), '1967')
    # S59
    sp, t = spec_words('s59')
    fo = {r['period']: r for r in read('frb-fomc-projections-unemployment')}
    same('S59', [fo[y]['median'] for y in ('2026', '2027', '2028', '2029')], ['4.1'] * 4, 'medians')
    want('S59', t, 'median unemployment rate of 4.1 percent for each year through 2029', 'title')
    want('S59', t, 'range at %.1f to %.1f percent' % (num(fo['2029']['band_70_low']), num(fo['2029']['band_70_high'])), '2029 band')
    want('S59', t, 'apart at %s percent' % fo['longer_run']['median'], 'longer run')
    for y in ('2026', '2027', '2028', '2029'):
        same('S59', round(num(fo[y]['median']) - num(fo[y]['historical_error']), 4), num(fo[y]['band_70_low']), 'band ' + y)
    for f in bad:
        print('FAULT ' + f)
    print('figures: %d faults' % len(bad))
    return len(bad)


if __name__ == '__main__':
    if '--figures' in sys.argv:
        sys.exit(1 if figures() else 0)
    judges()
    uninsured()
    child_poverty()
    openings_quarterly()
    if FAULTS:
        print('\n'.join('FAULT ' + f for f in FAULTS))
        sys.exit(1)
    print('0 faults' if CHECK else 'done')
