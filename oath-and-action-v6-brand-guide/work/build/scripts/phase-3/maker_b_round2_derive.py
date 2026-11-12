"""Maker B, Phase 3 round 2: R2-2's derived summaries for S49, S51 and S52 (D3-652, contract C1).

    python3 -I work/build/scripts/phase-3/maker_b_round2_derive.py [--check]

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
when a written file differs from what the script computes now. Standard library only.
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
    yrs = [num(r['years_as_federal_judge']) for r in rows]
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
        derivation=('Each judge in active service counted once in the two-year bin, closed on the left, that holds the years '
                    'since the first Article III commission, from 0 to 44 years (the data lead\'s ruling (g), round 2)'),
        notes=['%d judges in all; median %.2f years as a federal judge (Python statistics.median of the unrounded years)' % (len(yrs), med),
               'Bin edges checked against inauguration dates: January 20 of 2001, 2009, 2017, 2021 and 2025 sit 25.81, 17.81, 9.81, '
               '5.81 and 1.81 years before November 11, 2026, so no edge falls on one (H09)'])
    write(name, ['bin_start', 'bin_end', 'label', 'judges'], bins, side)
    print('  S49 judges %d, median %.4f, largest bin %s' % (len(yrs), med, max(bins, key=lambda b: b['judges'])))
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
            'margins of error; each region\'s quartiles, whiskers and outliers computed by Oath & Action.')
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


if __name__ == '__main__':
    judges()
    uninsured()
    child_poverty()
    openings_quarterly()
    if FAULTS:
        print('\n'.join('FAULT ' + f for f in FAULTS))
        sys.exit(1)
    print('0 faults' if CHECK else 'done')
