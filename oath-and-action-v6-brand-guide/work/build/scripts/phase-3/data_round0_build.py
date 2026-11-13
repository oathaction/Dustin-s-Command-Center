"""Move the data of S01 to S16 into work/build/data/ under the round 0 contract (engineer notes, C1).

Usage:
    python3 -I work/build/scripts/phase-3/data_round0_build.py [--check]

Reads Phase 2's frozen board files, which stay where they are as records:
  work/boards/phase-2/data-viz/shared/public/<name>.csv and <name>.meta.json   (the research lead's November 6 files)
  work/extract/atlas-v7-data.json                                               (Atlas V7, snapshot of October 15, 2026)
and writes, in work/build/data/:
  the public tables S02, S04, S05, S07, S11 to S16 draw, copied byte for byte, each with a sidecar in the contract's form;
  three derived tables (the FEC margin shift by state, payrolls by sector with change since January 2022, and the
  monthly change in total payrolls with its three-month average), each naming its source file and method;
  six Atlas V7 tables (v7-*.json) for S01, S03, S06, S08, S09 and S10.
The retired disclosure (DR-100, D2-1756) is dropped: no sidecar carries it or a required_text that holds it.
--check reads the folder back and fails on any contract fault; it writes nothing. Since round 3 (R3-2) it reads boundary
files too: a .geojson file in R1-C7's shape (check_geojson below) with its sidecar's extra fields.
"""
import collections
import csv
import hashlib
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PUB = ROOT / 'work/boards/phase-2/data-viz/shared/public'
V7P = ROOT / 'work/extract/atlas-v7-data.json'
OUT = ROOT / 'work/build/data'
SNAP = '2026-10-15'
SNAP_WORDS = 'October 15, 2026'
# The atlas as the guide names it to readers (chapter 02's source lines): "Atlas V7" is the studio's name for the file
ATLAS_PUB = 'Oath & Action’s systems atlas, Who Do They Answer To?'
ATLAS_LINE = 'Source: Oath & Action’s systems atlas, Who Do They Answer To?'
OLD_ATLAS = ('Source: Oath & Action, Who Do They Answer To? Systems Atlas V7', 'Oath & Action, Who Do They Answer To? Systems Atlas V7')
DISCLOSURE_RE = re.compile(r'Yes on 3|Veterans for All Voters|Ranked Choice Melrose|Disclosure:', re.I)
TYPES = {'number', 'integer', 'text', 'category', 'date', 'month', 'year', 'code', 'id', 'boolean'}
REQUIRED = ('file', 'kind', 'publisher', 'title_or_table', 'table_id', 'url', 'observation_period', 'geography',
            'universe_or_base', 'unit', 'date_retrieved', 'vintage', 'qualification', 'columns', 'printed_source_line',
            'ledger_row', 'domain', 'states')
KINDS = {'public', 'secondary', 'v7', 'derived', 'illustrative'}
DOMAINS = {f'D{i:02d}' for i in range(1, 11)} | {'all'}
# Fields a Phase 2 sidecar carries that do not travel: the old source line names (replaced by printed_source_line)
DROP = {'source_line', 'required_text'}


def smart(s):
    """Typographic apostrophes, as the printed pages set them."""
    return re.sub(r"(\w)'(\w)", '’'.join([r'\1', r'\2']), s).replace("s' ", 's’ ') if isinstance(s, str) else s


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def col(t, desc, unit=None):
    d = {'type': t, 'description': desc}
    if unit:
        d['unit'] = unit
    return d


def write_meta(name, meta):
    meta = {k: v for k, v in meta.items() if k not in DROP}
    (OUT / f'{name}.meta.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False) + '\n')


def read_csv(p):
    with p.open(newline='') as fh:
        return list(csv.DictReader(fh))


def write_csv(name, columns, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(columns)
    for r in rows:
        w.writerow(['' if r.get(c) is None else r[c] for c in columns])
    (OUT / f'{name}.csv').write_text(buf.getvalue())


def write_v7(name, columns, rows):
    clean = [{c: r.get(c) for c in columns} for r in rows]
    (OUT / f'{name}.json').write_text(json.dumps({'rows': clean}, indent=1, ensure_ascii=False) + '\n')


def num(v):
    try:
        return float(str(v).replace(',', ''))
    except (TypeError, ValueError):
        return None


def fmt(v, nd=1):
    return None if v is None else round(v, nd)


# A derived value keeps the publisher's precision: computed from the counts or levels and stored to six decimals, so the kit
# rounds it once, to the spec's format (D3-95, ENG-8). Six decimals only drop floating-point noise.
def keep(v):
    return None if v is None else round(v, 6)


# ---------------------------------------------------------------------------------------------------------------
# Public tables, copied byte for byte. Column types and the round 0 fields are added; Phase 2's other fields travel.
# ---------------------------------------------------------------------------------------------------------------
# The research ledger's Part 7 rows for the Phase 2 tables (research lead's request ENG-4, November 11, 2026)
LEDGER = {'ballotpedia-rcv-prohibitions-by-state': 'P7-101', 'census-cps-2024-turnout-by-state': 'P7-102', 'census-cps-reported-voting': 'P7-103',
          'census-hvs-homeownership-by-race-annual': 'P7-104', 'census-spm-child-poverty': 'P7-105', 'fec-presidential-results-by-state': 'P7-106',
          'fec-presidential-shift-by-state': 'P7-107', 'fred-payrolls-by-sector': 'P7-108', 'fred-payrolls-by-sector-change': 'P7-109',
          'fred-payrolls-monthly-change': 'P7-110'}
# Printed lines the research lead corrected in the fix pass (ENG-5 for statistics M3, ENG-6 for S17): {name: {field: (old start, new text)}}
SPM_NEW_END = ("Figures for 2019 to 2024 include the Bureau's August 2026 correction to the poverty thresholds, and 2024 also takes new "
               "population weights; they differ by up to 0.4 points from the earlier release.")
LINE_FIXES = {
    'census-spm-child-poverty': {
        'end_from': "Figures for 2019 to 2024 include the Bureau's August 2026 revision", 'end_to': SPM_NEW_END,
        'variants': {'source_line_first_published': (
            "Source: U.S. Census Bureau, Poverty in the United States: 2024 (P60-287), Table B-2, Supplemental Poverty Measure, children under 18, "
            "2020, 2021 and 2024, United States. Retrieved November 6, 2026. Rates as published before the Bureau's August 2026 correction; "
            "P60-277 (September 13, 2022) printed the same 2020 and 2021 rates.")},
    },
    'ballotpedia-rcv-prohibitions-by-state': {
        'printed': ("Source: Ballotpedia, a secondary source, Ranked-choice voting (RCV), state laws prohibiting RCV, as of November 2026, "
                    "50 states and DC. Retrieved November 6, 2026. Ohio's and Tennessee's bans cover some elections; the other 17 cover all."),
    },
}
# Rows the research lead read after Phase 2 and asked to add (ENG-7, statistics S18): the nation, from Table 4a's United States rows
# ENG-13 (round 1 fix pass, ST S12): columns the research lead read and asked to add, by state code; empty where there is no ban
CITY_REACH_YES = ('AL', 'AR', 'FL', 'ID', 'IN', 'IA', 'KS', 'KY', 'LA', 'MS', 'MO', 'MT', 'ND', 'OK', 'SD', 'WV', 'WY', 'TN')
ADDED_COLUMNS = {
    'ballotpedia-rcv-prohibitions-by-state': {
        'reaches_city_elections': {'type': 'category', 'description': 'whether the ban reaches a city’s own elections',
                                   'values': dict({c: 'yes' for c in CITY_REACH_YES}, OH='partly')},
        'city_reach_note': {'type': 'text', 'description': 'the source of that reading where it needs one',
                            'values': {'TN': ('Public Chapter 621 bars a county election commission from ranked-choice voting for a statewide or local '
                                              'government office, and defines local government to include an incorporated city or town (read November 12, 2026)'),
                                       'OH': ('Home-rule cities may still adopt it, but lose state local government fund distributions while it is in effect '
                                              '(Ballotpedia; the act’s text not read)'),
                                       'MO': 'Ballotpedia says the amendment prohibits ranked-choice voting; the amendment’s text was not read'}},
    },
}
ADDED_ROWS = {
    'census-cps-2024-turnout-by-state': {
        'rows': ['US,United States,2020,231593,66.8,0.4', 'US,United States,2024,236138,65.3,0.5'],
        'note': ('Code US is the national figure, read November 11, 2026 from the United States rows of Table 4a (vote04a_2024.xlsx, SHA-256 '
                 'prefix 068e47d3c7fc9701; table04a.xlsx for 2020, 8afd077c560de260); a chart draws it set apart from the states and labeled (DR-64).'),
    },
}

# Notes the research lead asked to add (ENG-2, ENG-3; ENG-9 for the payroll sampling errors and the survey's margin)
V7_NOTES = {
    'v7-stock-trading-ban': ('The Program for Public Consultation gives the full sample’s margin of error as plus or minus 1.9 percent '
                             '(https://publicconsultation.org/united-states/stock-trading-by-members-of-congress/, read November 11 and 12, 2026); '
                             'it gives none for each party’s voters and states no confidence level.'),
}
EXTRA_NOTES = {
    'fred-payrolls-by-sector': ('The Bureau of Labor Statistics publishes sampling errors for levels and for one-, three- and twelve-month changes '
                                '(All Employees Standard Error Tables, https://www.bls.gov/web/empsit/cesvarae.htm, read November 11, 2026), '
                                'none for longer changes, and none for government sectors.'),
    'census-cps-reported-voting': 'Margins for the 2020 and 2024 age-gap figures are in census-cps-voting-age-gap-moe: the gap between citizens 65 and over and citizens 18 to 24 grew 3.9 points with a margin of about 2.0 points.',
    # ENG-11 (round 1): the research lead's re-read after the November 3, 2026 election, printed as the decision tree's as-of date
    'ballotpedia-rcv-prohibitions-by-state': ('Re-read November 12, 2026, after the November 3, 2026 election: the same 19 states. The only 2026 measures on '
                                              'electoral systems, Alaska Ballot Measure 2 (trailing, uncertified) and Massachusetts Question 3 (rejected), '
                                              'add or remove no ban (research ledger P7-218).'),
    'census-hvs-homeownership-by-race-annual': 'Margins for 2003 and the 2003 to 2025 gaps are in census-hvs-homeownership-gap-moe: the non-Hispanic White and Black gap widened 2.3 points with a margin of about 0.7 points.',
}

PUBLIC = {
    'census-spm-child-poverty': {
        'specimens': ['S02'], 'kind': 'public', 'domain': 'D08', 'states': [],
        'types': {'year': 'year', 'measure': 'category', 'age_group': 'category', 'vintage': 'category', 'series_variant': 'category',
                  'comparable_with': 'category', 'percent': 'number', 'moe_pct': 'number', 'below_poverty_thousands': 'number',
                  'moe_thousands': 'number', 'population_thousands': 'number', 'source_table': 'text', 'note': 'text'},
        'units': {'percent': 'percent', 'moe_pct': 'percentage points', 'below_poverty_thousands': 'thousands of people',
                  'moe_thousands': 'thousands of people', 'population_thousands': 'thousands of people'},
        'variants': ('source_line_official_measure', 'source_line_first_published'),
        'extra_variants': {'source_line_both_measures': ('Source: U.S. Census Bureau, Poverty in the United States: 2025 (P60-290), Table 8, Supplemental Poverty Measure, '
                                                         'and Table 3, official poverty measure, children under 18, 2009 to 2025, United States. Retrieved November 6, 2026. '
                                                         'Figures for 2019 to 2024 include the Bureau\u2019s August 2026 revision and differ by up to 0.4 points from those first published.')},
    },
    'census-cps-reported-voting': {
        'specimens': ['S04'], 'kind': 'public', 'domain': 'D10', 'states': [],
        'domain_note': 'Reported turnout measures who takes part, the Participation subsystem of V7 domain D10; election rules and results stay under D02',
        'types': {'year': 'year', 'election_type': 'category', 'age_group': 'category', 'base': 'category', 'voted_pct': 'number',
                  'total_voting_age_population_thousands': 'number', 'note': 'text'},
        'units': {'voted_pct': 'percent', 'total_voting_age_population_thousands': 'thousands of people'},
        'variants': ('source_line_citizen_only',),
    },
    'census-hvs-homeownership-by-race-annual': {
        'specimens': ['S05'], 'kind': 'public', 'domain': 'D09', 'states': [],
        'types': {'year': 'year', 'group': 'category', 'rate_pct': 'number', 'moe_pct': 'number', 'race_definition': 'category',
                  'series_variant': 'category', 'source_table': 'text', 'note': 'text'},
        'units': {'rate_pct': 'percent', 'moe_pct': 'percentage points'},
    },
    'ballotpedia-rcv-prohibitions-by-state': {
        'specimens': ['S07'], 'kind': 'secondary', 'domain': 'D02', 'states': [],
        'types': {'code': 'code', 'name': 'text', 'fips': 'code', 'prohibits_rcv': 'integer', 'scope': 'category', 'instrument': 'category',
                  'enacted_date': 'date', 'enacted_year': 'year', 'measure': 'text', 'scope_note': 'text', 'checked_against': 'text'},
        'descs': {'code': 'USPS state code', 'name': 'state name', 'fips': 'FIPS state code', 'prohibits_rcv': '1 when the state bans ranked-choice voting, else 0',
                  'scope': 'all (every election) or some (some elections); empty when there is no ban', 'instrument': 'how the ban was made',
                  'enacted_date': 'date the ban took effect or was signed, as Ballotpedia prints it', 'enacted_year': 'year of enactment',
                  'measure': 'bill or measure, as Ballotpedia prints it', 'scope_note': 'what the ban covers',
                  'checked_against': 'the page and revision read'},
    },
    'census-cps-2024-turnout-by-state': {
        'specimens': ['S16'], 'kind': 'public', 'domain': 'D10', 'states': [],
        'domain_note': 'Reported turnout measures who takes part, the Participation subsystem of V7 domain D10',
        'types': {'code': 'code', 'name': 'text', 'year': 'year', 'citizen_vap_thousands': 'number', 'voted_pct': 'number', 'moe_pct': 'number'},
        'descs': {'code': 'USPS state code', 'name': 'state name', 'year': 'election year', 'citizen_vap_thousands': 'citizens 18 and over, thousands',
                  'voted_pct': 'percent of citizens 18 and over who reported voting', 'moe_pct': '90 percent margin of error, percentage points'},
        'units': {'citizen_vap_thousands': 'thousands of people', 'voted_pct': 'percent', 'moe_pct': 'percentage points'},
        'variants': ('source_line_2024_only',),
    },
    'fec-presidential-results-by-state': {
        'specimens': [], 'kind': 'public', 'domain': 'D02', 'states': [],
        'types': {'code': 'code', 'name': 'text', 'year': 'year', 'total_votes': 'integer', 'dem_votes': 'integer', 'rep_votes': 'integer',
                  'dem_pct': 'number', 'rep_pct': 'number', 'margin_pts': 'number'},
        'descs': {'code': 'USPS state code', 'name': 'state name', 'year': 'election year', 'total_votes': 'all presidential votes cast',
                  'dem_votes': 'votes for the Democratic nominee', 'rep_votes': 'votes for the Republican nominee',
                  'dem_pct': 'Democratic share of all presidential votes, percent', 'rep_pct': 'Republican share of all presidential votes, percent',
                  'margin_pts': 'Republican share minus Democratic share, percentage points; positive is a Republican lead'},
        'units': {'dem_pct': 'percent', 'rep_pct': 'percent', 'margin_pts': 'percentage points'},
    },
    'fred-payrolls-by-sector': {
        'specimens': [], 'kind': 'public', 'domain': 'D07', 'states': [],
        'types': {'series_id': 'id', 'sector': 'category', 'date': 'date', 'employees_thousands': 'number'},
        'descs': {'series_id': 'FRED series ID', 'sector': 'industry sector as BLS names it', 'date': 'first day of the month',
                  'employees_thousands': 'all employees, thousands, seasonally adjusted'},
        'units': {'employees_thousands': 'thousands of jobs'},
    },
}


def public_meta(name, spec):
    p = PUB / f'{name}.meta.json'
    m = json.loads(p.read_text())
    rows = read_csv(PUB / f'{name}.csv')
    cols = list(rows[0].keys())
    old = m.get('columns') if isinstance(m.get('columns'), dict) else {}
    out_cols = {}
    for c in cols:
        t = spec['types'].get(c)
        if t not in TYPES:
            raise SystemExit(f'{name}: column {c} has no type')
        desc = old.get(c) or spec.get('descs', {}).get(c) or c.replace('_', ' ')
        out_cols[c] = col(t, desc, spec.get('units', {}).get(c))
    meta = {'file': f'{name}.csv', 'kind': spec['kind']}
    for k in ('publisher', 'title_or_table', 'table_id', 'url', 'observation_period', 'geography', 'universe_or_base', 'unit',
              'date_retrieved', 'vintage', 'qualification'):
        meta[k] = m.get(k)
    meta['columns'] = out_cols
    meta['printed_source_line'] = smart(m['source_line'])
    variants = {v: smart(m[v]) for v in spec.get('variants', ()) if m.get(v)}
    variants.update(spec.get('extra_variants', {}))
    fx = LINE_FIXES.get(name)
    if fx:
        if fx.get('printed'):
            meta['printed_source_line'] = smart(fx['printed'])
        if fx.get('end_from'):
            def fix_end(line):
                i = line.find(smart(fx['end_from']))
                return line if i < 0 else line[:i] + smart(fx['end_to'])
            meta['printed_source_line'] = fix_end(meta['printed_source_line'])
            variants = {k: fix_end(v) for k, v in variants.items()}
        for k, v in (fx.get('variants') or {}).items():
            variants[k] = smart(v)
    if variants:
        meta['source_line_variants'] = variants
    meta['ledger_row'] = LEDGER.get(name, 'none yet')
    meta['domain'] = spec['domain']
    if spec.get('domain_note'):
        meta['domain_note'] = spec['domain_note']
    meta['states'] = spec['states']
    meta['specimens'] = spec['specimens']
    meta['copied_from'] = f'work/boards/phase-2/data-viz/shared/public/{name}.csv'
    meta['copied_sha256_prefix'] = sha(PUB / f'{name}.csv')
    # Phase 2's other fields travel as they are
    for k, v in m.items():
        if k not in meta and k not in DROP and k != 'columns' and not k.startswith('source_line'):
            meta[k] = v
    if name in EXTRA_NOTES:
        meta['notes'] = list(meta.get('notes') or []) + [EXTRA_NOTES[name]]
    if name == 'census-hvs-homeownership-by-race-annual' and isinstance(meta.get('unconfirmed'), list):
        meta['unconfirmed'] = [('Margins of error before 2025, other than 2003 and the 2003 to 2025 gaps, which census-hvs-homeownership-gap-moe now holds'
                                if 'margin' in u.lower() else u) for u in meta['unconfirmed']]
    return meta


def copy_public():
    for name, spec in PUBLIC.items():
        raw = (PUB / f'{name}.csv').read_bytes()
        meta = public_meta(name, spec)
        add = ADDED_ROWS.get(name)
        if add:
            # the Phase 2 rows byte for byte, then the rows read since, each named in the sidecar
            raw = raw.rstrip(b'\n') + b'\n' + '\n'.join(add['rows']).encode() + b'\n'
            meta['added_rows'] = add['rows']
            meta['notes'] = list(meta.get('notes') or []) + [add['note']]
        cols = ADDED_COLUMNS.get(name)
        if cols:
            # the Phase 2 file's rows and columns as they were, each row extended by the columns read since (ENG-13)
            rows = list(csv.reader(io.StringIO(raw.decode('utf-8'))))
            head, body = rows[0], rows[1:]
            ci = head.index('code')
            bans = {r[ci] for r in body if r[head.index('prohibits_rcv')] == '1'}
            if not set(cols['reaches_city_elections']['values']) <= bans:
                raise SystemExit(f'ENG-13: {sorted(set(cols["reaches_city_elections"]["values"]) - bans)} carry a city reading but no ban')
            if bans - set(cols['reaches_city_elections']['values']):
                raise SystemExit(f'ENG-13: {sorted(bans - set(cols["reaches_city_elections"]["values"]))} ban ranked-choice voting with no city reading')
            out = io.StringIO()
            w = csv.writer(out, lineterminator='\n')
            w.writerow(head + list(cols))
            for r in body:
                w.writerow(r + [cols[k]['values'].get(r[ci], '') for k in cols])
            raw = out.getvalue().encode('utf-8')
            for k, v in cols.items():
                meta['columns'][k] = {'type': v['type'], 'description': v['description']}
        (OUT / f'{name}.csv').write_bytes(raw)
        write_meta(name, meta)


# ---------------------------------------------------------------------------------------------------------------
# Derived tables: each its own file, naming the file it comes from and its method
# ---------------------------------------------------------------------------------------------------------------
def derive_fec_shift():
    rows = read_csv(PUB / 'fec-presidential-results-by-state.csv')
    m = json.loads((PUB / 'fec-presidential-results-by-state.meta.json').read_text())
    by = {}
    for r in rows:
        by.setdefault(r['code'], {'code': r['code'], 'name': r['name']})[int(float(r['year']))] = r
    out = []
    nat = {}
    for r in rows:
        t = nat.setdefault(int(float(r['year'])), [0, 0, 0])
        t[0] += num(r['total_votes']); t[1] += num(r['dem_votes']); t[2] += num(r['rep_votes'])
    # every share from the vote counts, unrounded (ENG-8): margin = (Republican - Democratic) / total votes x 100
    sh = {y: (100 * d / tv, 100 * rp / tv, 100 * (rp - d) / tv) for y, (tv, d, rp) in nat.items()}
    out.append({'code': 'US', 'name': 'United States', 'scope': 'nation', 'margin_2020': keep(sh[2020][2]), 'margin_2024': keep(sh[2024][2]),
                'shift_pts': keep(sh[2024][2] - sh[2020][2]), 'dem_pct_2024': keep(sh[2024][0]), 'rep_pct_2024': keep(sh[2024][1]),
                'total_votes_2024': int(nat[2024][0])})

    def share(r, k):
        return 100 * num(r[k]) / num(r['total_votes'])

    def margin(r):
        return 100 * (num(r['rep_votes']) - num(r['dem_votes'])) / num(r['total_votes'])
    for code, s in sorted(by.items()):
        m20, m24 = margin(s[2020]), margin(s[2024])
        out.append({'code': code, 'name': s['name'], 'scope': 'state', 'margin_2020': keep(m20), 'margin_2024': keep(m24),
                    'shift_pts': keep(m24 - m20), 'dem_pct_2024': keep(share(s[2024], 'dem_votes')), 'rep_pct_2024': keep(share(s[2024], 'rep_votes')),
                    'total_votes_2024': int(num(s[2024]['total_votes']))})
    cols = ['code', 'name', 'scope', 'margin_2020', 'margin_2024', 'shift_pts', 'dem_pct_2024', 'rep_pct_2024', 'total_votes_2024']
    write_csv('fec-presidential-shift-by-state', cols, out)
    meta = {
        'file': 'fec-presidential-shift-by-state.csv', 'kind': 'derived',
        'publisher': m['publisher'], 'title_or_table': m['title_or_table'], 'table_id': m['table_id'], 'url': m['url'],
        'observation_period': 'November 2020 and November 2024 presidential general elections', 'geography': '50 states and DC, with the United States in one row set apart',
        'universe_or_base': 'All presidential votes cast in each state', 'unit': 'Margins and shift in percentage points; shares in percent; votes as counted',
        'date_retrieved': m['date_retrieved'], 'vintage': m['vintage'], 'qualification': m['qualification'],
        'columns': {
            'code': col('code', 'USPS state code; US for the nation'), 'name': col('text', 'state name'),
            'scope': col('category', 'state, or nation for the United States row (DR-64: the national figure on every chart of state results, set apart and labeled)'),
            'margin_2020': col('number', 'Republican share minus Democratic share in 2020; positive is a Republican lead', 'percentage points'),
            'margin_2024': col('number', 'Republican share minus Democratic share in 2024; positive is a Republican lead', 'percentage points'),
            'shift_pts': col('number', 'margin_2024 minus margin_2020; positive moved toward the Republican nominee', 'percentage points'),
            'dem_pct_2024': col('number', 'Democratic share of all presidential votes in 2024', 'percent'),
            'rep_pct_2024': col('number', 'Republican share of all presidential votes in 2024', 'percent'),
            'total_votes_2024': col('integer', 'all presidential votes cast in 2024'),
        },
        'printed_source_line': smart(m['source_line']), 'ledger_row': LEDGER['fec-presidential-shift-by-state'], 'domain': 'D02', 'states': [],
        'specimens': ['S11', 'S12', 'S15'],
        'derived_from': ['fec-presidential-results-by-state.csv'],
        'derivation': ('One row per state from the two years\' rows; shift_pts is the difference of the two margins as rounded in the FEC file. '
                       'The United States row sums the state rows\' vote counts, which match the FEC national totals, and is context for a chart, '
                       'set apart and labeled (D2-126, DR-64). In nine states shift_pts differs by 0.01 from the difference of unrounded shares; '
                       'no figure printed to one decimal changes (D2-126).'),
        'notes': ['Party marks take neutral inks with the party name printed; arrows, position and words carry direction (DR-48, DR-58).',
                  'A map has no tile for US; it draws the national figure beside the map.'],
    }
    write_meta('fec-presidential-shift-by-state', meta)


FRED_LINE = ('Source: U.S. Bureau of Labor Statistics, Current Employment Statistics, {what}, seasonally adjusted, January 2022 to September 2026, '
             'United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 6, 2026. August and September 2026 are preliminary and will be revised.')
FRED_REV = ('Seasonally adjusted. The Bureau of Labor Statistics revises each month’s first estimate in the next two monthly reports, '
            'so August and September 2026 are preliminary, and a yearly benchmark revision can move earlier months. FRED copies the Bureau of Labor '
            'Statistics series; bls.gov refuses automated requests, so the studio read FRED (DR-60).')


def derive_fred():
    rows = read_csv(PUB / 'fred-payrolls-by-sector.csv')
    m = json.loads((PUB / 'fred-payrolls-by-sector.meta.json').read_text())
    series = collections.OrderedDict()
    for r in rows:
        series.setdefault(r['series_id'], []).append(r)
    prelim = {'2026-08', '2026-09'}
    sect, change = [], []
    for sid, rs in series.items():
        rs.sort(key=lambda r: r['date'])
        base = next((num(r['employees_thousands']) for r in rs if r['date'].startswith('2022-01')), None)
        for r in rs:
            mo = r['date'][:7]
            if mo < '2022-01':
                continue
            v = num(r['employees_thousands'])
            sect.append({'series_id': sid, 'sector': r['sector'], 'month': mo, 'employees_thousands': v,
                         'pct_change_since_2022_01': keep((v / base - 1) * 100) if base and v is not None else None,
                         'change_since_2022_01_thousands': keep(v - base) if base and v is not None else None,
                         'status': 'preliminary' if mo in prelim else 'final'})
        if sid == 'PAYEMS':
            vals = [(r['date'][:7], num(r['employees_thousands'])) for r in rs]
            diffs = [(vals[i][0], keep(vals[i][1] - vals[i - 1][1])) for i in range(1, len(vals))
                     if vals[i][1] is not None and vals[i - 1][1] is not None]
            for i, (dt, d) in enumerate(diffs):
                w = [x for _, x in diffs[max(0, i - 2):i + 1]]
                if dt < '2022-01':
                    continue
                change.append({'month': dt, 'change_thousands': d, 'avg3_thousands': keep(sum(w) / len(w)) if len(w) == 3 else None,
                               'status': 'preliminary' if dt in prelim else 'final'})
    write_csv('fred-payrolls-by-sector-change', ['series_id', 'sector', 'month', 'employees_thousands', 'pct_change_since_2022_01',
                                                 'change_since_2022_01_thousands', 'status'], sect)
    write_csv('fred-payrolls-monthly-change', ['month', 'change_thousands', 'avg3_thousands', 'status'], change)
    common = {'publisher': 'U.S. Bureau of Labor Statistics, via FRED, Federal Reserve Bank of St. Louis', 'title_or_table': m['title_or_table'],
              'table_id': m['table_id'], 'url': m['url'], 'geography': 'United States', 'universe_or_base': m['universe_or_base'],
              'date_retrieved': m['date_retrieved'], 'vintage': m['vintage'], 'qualification': FRED_REV,
              'domain': 'D07', 'states': [], 'derived_from': ['fred-payrolls-by-sector.csv']}
    write_meta('fred-payrolls-by-sector-change', dict(
        file='fred-payrolls-by-sector-change.csv', kind='derived', ledger_row=LEDGER['fred-payrolls-by-sector-change'], **common,
        observation_period='Monthly, January 2022 to September 2026', unit='Thousands of jobs; percent change since January 2022',
        columns={'series_id': col('id', 'FRED series ID'), 'sector': col('category', 'industry sector as BLS names it'),
                 'month': col('month', 'month of the estimate'), 'employees_thousands': col('number', 'all employees, seasonally adjusted', 'thousands of jobs'),
                 'pct_change_since_2022_01': col('number', 'percent change from the sector’s January 2022 level', 'percent'),
                 'change_since_2022_01_thousands': col('number', 'change from the sector’s January 2022 level', 'thousands of jobs'),
                 'status': col('category', 'preliminary for August and September 2026, else final')},
        printed_source_line=FRED_LINE.format(what='all employees by industry'), specimens=['S13'],
        derivation='Rows from January 2022 on; pct_change_since_2022_01 and change_since_2022_01_thousands compare each month with the same series in January 2022 (D2-126: both jobs charts draw January 2022 to September 2026, one window).',
    ))
    write_meta('fred-payrolls-monthly-change', dict(
        file='fred-payrolls-monthly-change.csv', kind='derived', ledger_row=LEDGER['fred-payrolls-monthly-change'], **common,
        observation_period='Monthly, January 2022 to September 2026', unit='Thousands of jobs',
        columns={'month': col('month', 'month of the change'),
                 'change_thousands': col('number', 'total nonfarm payrolls minus the month before', 'thousands of jobs'),
                 'avg3_thousands': col('number', 'mean of this month’s change and the two before it', 'thousands of jobs'),
                 'status': col('category', 'preliminary for August and September 2026, else final')},
        printed_source_line=FRED_LINE.format(what='all nonfarm employees, monthly change'), specimens=['S14'],
        # D3-219 (round 1): the line S14 prints with the survey's margin, in the editor's words (its round 0 notes, "Board 1
        # apply"); the figure is the research ledger's P7-042, the Bureau's Employment Situation technical note
        source_line_variants={'with_margin': FRED_LINE.format(what='all nonfarm employees, monthly change') + (
            ' The margin of error is the Bureau’s 90 percent interval for a month’s change in its survey of employers, plus or minus '
            '122,000, from its Employment Situation technical note, October 2026 release.')},
        derivation='From series PAYEMS: each month’s level minus the month before; avg3_thousands is the three-month moving average ending in that month, computed from December 2021 on so January 2022 has one. Rows from January 2022 on.',
    ))


# ---------------------------------------------------------------------------------------------------------------
# Atlas V7 tables
# ---------------------------------------------------------------------------------------------------------------
def v7_meta(name, table, table_id, period, geography, universe, unit, qual, columns, line, domain, specimens, states=(), **extra):
    old = line.replace(ATLAS_LINE, OLD_ATLAS[0]).replace('as recorded in ' + ATLAS_PUB + ',', 'as recorded in ' + OLD_ATLAS[1] + ',')
    if old != line:
        extra.setdefault('source_line_variants', {})['phase_2_wording'] = old
    meta = {'file': f'{name}.json', 'kind': extra.pop('kind', 'v7'), 'publisher': ATLAS_PUB, 'title_or_table': table, 'table_id': table_id,
            'url': 'work/extract/atlas-v7-data.json', 'observation_period': period, 'geography': geography, 'universe_or_base': universe,
            'unit': unit, 'date_retrieved': SNAP, 'vintage': f'Atlas V7 snapshot of {SNAP_WORDS}', 'qualification': qual, 'columns': columns,
            'printed_source_line': line, 'ledger_row': 'not needed: Atlas V7, read by script', 'domain': domain, 'states': list(states),
            'snapshot': SNAP, 'specimens': specimens, 'extract_script': 'work/build/scripts/phase-3/data_round0_build.py'}
    meta.update(extra)
    if name in V7_NOTES:
        meta['notes'] = list(meta.get('notes') or []) + [V7_NOTES[name]]
    write_meta(name, meta)


GROUP = {
    'ballot initiative': 'Ballot initiative', 'court ruling': 'Court ruling', 'state statute': 'State statute',
    'referendum': 'Referendum', 'federal statute': 'Federal statute',
    'agency rule': 'Executive or agency action', 'executive action': 'Executive or agency action', 'executive order': 'Executive or agency action',
    'municipal ordinance (local law)': 'Local law or funding vote', 'council funding vote': 'Local law or funding vote',
}
DIRS = ['toward voters', 'away from voters', 'voters kept existing rules', 'mixed', 'pending']
FAM = {'DQ': 'Quality of democracy', 'GE': 'Government efficacy', 'EP': 'Economic performance', 'EQ': 'Income and wealth equality'}


def dclass(w):
    """Phase 2's coarse reading of V7's direction words (dataviz_shared_data.py, D2-102), for a glyph or tint only."""
    w = w.lower()
    if w.startswith('same as scenario'):
        return 'same as ii'
    if w.startswith('down or flat') or w.startswith('flat, or down'):
        return 'flat or down'
    if w.startswith('down'):
        return 'down'
    if w.startswith('mixed') or 'mixed' in w and w.startswith('prices'):
        return 'mixed'
    if w.startswith('slightly up') or w.startswith('small') or w.startswith('up modestly'):
        return 'slightly up'
    if w.startswith('up'):
        return 'up'
    if w.startswith('flat') or w.startswith('near trend'):
        return 'flat'
    raise SystemExit(f'unclassed scenario word: {w}')


def v7_tables():
    V7 = json.loads(V7P.read_text())
    if V7['meta']['snapshot'] != SNAP:
        raise SystemExit(f'Atlas V7 snapshot is {V7["meta"]["snapshot"]}, expected {SNAP}')

    # S01: the shared view on a stock trading ban, headline figure 7, and the votes its qualification names
    n7 = next(n for n in V7['numbers'] if n['figure'].startswith('87%'))
    q = n7['qualification']
    for frag in ('232 to 198', 'July 22, 2026', '53 to 47', 'September 30, 2026', '60 votes'):
        if frag not in q:
            raise SystemExit(f'S01: V7 figure 7 no longer says {frag!r}')
    n40 = V7['sources'].get('N40', {})
    rows = [
        {'key': 'support-all', 'group': 'All registered voters', 'value': 86, 'measure': 'percent who favor a ban', 'body': 'survey', 'source_id': 'N40'},
        {'key': 'support-republicans', 'group': 'Republicans', 'value': 87, 'measure': 'percent who favor a ban', 'body': 'survey', 'source_id': 'N40'},
        {'key': 'support-democrats', 'group': 'Democrats', 'value': 88, 'measure': 'percent who favor a ban', 'body': 'survey', 'source_id': 'N40'},
        {'key': 'house-yes', 'group': 'House, passage of H.R. 7008, July 22, 2026', 'value': 232, 'measure': 'votes for', 'body': 'House', 'source_id': 'K1908'},
        {'key': 'house-no', 'group': 'House, passage of H.R. 7008, July 22, 2026', 'value': 198, 'measure': 'votes against', 'body': 'House', 'source_id': 'K1908'},
        {'key': 'senate-yes', 'group': 'Senate, cloture on the motion to proceed, September 30, 2026', 'value': 53, 'measure': 'votes for', 'body': 'Senate', 'source_id': 'W035'},
        {'key': 'senate-no', 'group': 'Senate, cloture on the motion to proceed, September 30, 2026', 'value': 47, 'measure': 'votes against', 'body': 'Senate', 'source_id': 'W035'},
        {'key': 'senate-needed', 'group': 'Senate, cloture on the motion to proceed, September 30, 2026', 'value': 60, 'measure': 'votes needed (three-fifths)', 'body': 'Senate', 'source_id': 'W035'},
    ]
    if '86' not in json.dumps(n40):
        print('note: S01 overall 86 percent not found in V7 source N40; kept from Phase 2 (D2-104)', file=sys.stderr)
    cols = ['key', 'group', 'value', 'measure', 'body', 'source_id']
    write_v7('v7-stock-trading-ban', cols, rows)
    v7_meta('v7-stock-trading-ban', 'headline figure 7, a shared view on a stock trading ban by members of Congress, and the votes it records',
            'numbers[figure 87% and 88%]; sources N40, K1908, W035, N12',
            'Survey fielded May 19 to 30, 2023; House vote July 22, 2026; Senate vote September 30, 2026', 'United States',
            'Registered voters in the survey; members voting in each chamber', 'Percent of registered voters; votes',
            'The survey predates both votes by three years. Both chambers’ party splits are in congress-hr7008-roll-calls, read November 11, 2026.',
            {'key': col('id', 'row key, the studio’s'), 'group': col('text', 'who the figure describes'),
             'value': col('number', 'the figure: percent for the survey rows, votes for the chamber rows'),
             'measure': col('text', 'what the value counts'), 'body': col('category', 'survey, House or Senate'),
             'source_id': col('id', 'the V7 source the row rests on')},
            ('Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, '
             'United States; U.S. House of Representatives, Roll Call 280, July 22, 2026; U.S. Senate, Vote 253, September 30, 2026; '
             'as recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. The survey predates both votes by three years.'),
            'D03', ['S01'], domain_note='Members’ stock trading is a conflict of interest, the Conflicts subsystem of V7 domain D03',
            source_line_variants={'with_bill_text': ('Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, '
                                                     'United States; U.S. Government Publishing Office, H.R. 7008, Stop Insider Trading Act, text as passed by the House, sections 2 and 3; '
                                                     'U.S. House of Representatives, Roll Call 280, July 22, 2026; U.S. Senate, Vote 253, September 30, 2026; as recorded in Oath & Action’s systems atlas, '
                                                     'Who Do They Answer To?, snapshot of October 15, 2026. Bill text retrieved November 11, 2026. The survey predates both votes by three years.'),
                                  # maker A's A5 (round 1): S41 and S42 show the survey rows alone (D3-89)
                                  'survey_only': ('Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, '
                                                  'United States, as recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. '
                                                  'A margin of error of plus or minus 1.9 points for the whole sample, with none by party.'),
                                  # ENG-12 (round 1 fix pass, ST S11): the margin credited to the Program's page, reread November 12
                                  'survey_only_margin_credited': ('Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, '
                                                                  'United States, as recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. '
                                                                  'A margin of error of plus or minus 1.9 points for the whole sample, with none by party, from the Program’s survey page, read November 12, 2026.')},
            v7_figure=n7, notes=['The 86 percent overall figure is in the survey source note (N40), not in the headline figure caption.',
                                 'DR-98: a chart names "H.R. 7008, the Stop Insider Trading Act" with both provisions at first mention; the spec carries those words.'])

    # S08: the repair log, one row per dated rule change; S03: the same grouped by instrument
    RL = V7['repairLog']
    rl = []
    for r in RL['rows']:
        rl.append({'id': r['id'], 'date': r['date'], 'year': int(r['date'][:4]), 'jurisdiction': r['jurisdiction'], 'direction': r['direction'],
                   'instrument': r['instrument'], 'instrument_group': GROUP[r['instrument']], 'rule': r['rule'], 'margin': r['margin'],
                   'reversed_by': r.get('reversed_by'), 'loop': r.get('loop'), 'source_title': r['source_title'], 'source_url': r['source_url'],
                   'verified': r['verified']})
    rl.sort(key=lambda x: (x['date'], x['id']))
    rl_line = (f'{ATLAS_LINE}, repair log of 64 dated rule changes, August 6, 1965 to the November 3, 2026 ballot, United States: federal, state and local. '
               f'Snapshot of {SNAP_WORDS}. Directions are the atlas’s own codes, set out in its coding note; each row cites its own source. '
               'One entry, New York City’s 1988 small-donor matching law, rests on a source the atlas did not check.')
    rl_cols = ['id', 'date', 'year', 'jurisdiction', 'direction', 'instrument', 'instrument_group', 'rule', 'margin', 'reversed_by', 'loop',
               'source_title', 'source_url', 'verified']
    write_v7('v7-repair-log', rl_cols, rl)
    v7_meta('v7-repair-log', 'repair log of 64 dated rule changes', 'repairLog.rows', 'August 6, 1965 to the November 3, 2026 ballot',
            'United States: federal, state and local', 'Dated changes to the rules that decide who officials answer to', 'One row per rule change',
            'Directions are the atlas’s own codes, set out in its coding note; each row cites its own source.',
            {'id': col('id', 'V7 repair log ID, RL01 to RL64'), 'date': col('date', 'date of the change'), 'year': col('year', 'year of the change'),
             'jurisdiction': col('text', 'where the rule applies'), 'direction': col('category', 'V7’s code: ' + ', '.join(DIRS)),
             'instrument': col('category', 'how the change was made, V7’s word'),
             'instrument_group': col('category', 'the studio’s grouping of instruments with one row each (D2-102)'),
             'rule': col('text', 'what changed, V7’s words'), 'margin': col('text', 'the vote or ruling, V7’s words'),
             'reversed_by': col('text', 'a later change that reversed it, if any'), 'loop': col('text', 'the loop V7 ties it to'),
             'source_title': col('text', 'the row’s own source'), 'source_url': col('text', 'its address'),
             'verified': col('text', 'V7’s verification note')},
            rl_line, 'D02', ['S08'], intro=RL['intro'], coding_note=RL['coding_note'],
            domain_note='53 of the 64 rows change election, ballot, district or campaign rules, V7 domain D02')
    by = collections.OrderedDict()
    for r in rl:
        g = by.setdefault(r['instrument_group'], {'instrument_group': r['instrument_group'], 'total': 0, **{d: 0 for d in DIRS}})
        g['total'] += 1
        g[r['direction']] += 1
    inst = sorted(by.values(), key=lambda x: (-x['total'], x['instrument_group']))
    inst = [{'instrument_group': g['instrument_group'], 'total': g['total'], 'toward_voters': g['toward voters'], 'away_from_voters': g['away from voters'],
             'voters_kept_existing_rules': g['voters kept existing rules'], 'mixed': g['mixed'], 'pending': g['pending']} for g in inst]
    write_v7('v7-repair-log-by-instrument', ['instrument_group', 'total', 'toward_voters', 'away_from_voters', 'voters_kept_existing_rules', 'mixed', 'pending'], inst)
    v7_meta('v7-repair-log-by-instrument', 'repair log of 64 dated rule changes, counted by how each was made', 'repairLog.rows, grouped',
            'August 6, 1965 to the November 3, 2026 ballot', 'United States: federal, state and local', 'Dated changes to the rules that decide who officials answer to',
            'Rule changes', 'Directions are the atlas’s own codes, set out in its coding note; each row cites its own source.',
            {'instrument_group': col('category', 'how the change was made; five instruments with one row each are grouped (D2-102)'),
             'total': col('integer', 'rule changes made this way'), 'toward_voters': col('integer', 'coded toward voters'),
             'away_from_voters': col('integer', 'coded away from voters'), 'voters_kept_existing_rules': col('integer', 'coded voters kept existing rules'),
             'mixed': col('integer', 'coded mixed'), 'pending': col('integer', 'coded pending')},
            rl_line, 'D02', ['S03'], kind='derived', derived_from=['v7-repair-log.json'],
            derivation=('Counts of v7-repair-log rows by instrument_group and direction. Agency rule, executive action and executive order group as '
                        '"Executive or agency action"; municipal ordinance and council funding vote as "Local law or funding vote". The grouping is the studio’s; the instruments are V7’s.'),
            domain_note='53 of the 64 rows change election, ballot, district or campaign rules, V7 domain D02')

    # S06: eight scenarios and four outcome families, V7's words with the studio's coarse class beside each
    srows = []
    for s in V7['scenarios']['items']:
        row = {'id': s['id'], 'name': s['name'], 'assumptions': '; '.join(s['assumptions'])}
        for f in FAM:
            row[f.lower()] = s[f]['dir']
            row[f.lower() + '_class'] = dclass(s[f]['dir'])
            row[f.lower() + '_why'] = s[f]['why']
        srows.append(row)
    scols = ['id', 'name', 'assumptions'] + [x for f in FAM for x in (f.lower(), f.lower() + '_class', f.lower() + '_why')]
    write_v7('v7-scenarios-2030', scols, srows)
    cdesc = {}
    for f, label in FAM.items():
        cdesc[f.lower()] = col('text', f'V7’s direction words for {label}')
        cdesc[f.lower() + '_class'] = col('category', f'the studio’s coarse reading of those words, for a glyph or tint only: up, slightly up, flat, flat or down, down, mixed, same as ii')
        cdesc[f.lower() + '_why'] = col('text', f'V7’s reason for the {label} direction')
    v7_meta('v7-scenarios-2030', 'reform outcomes, eight scenarios and the direction each would move four outcome families', 'scenarios.items',
            'Conditional directions to 2036 from a 2026 baseline', 'United States', 'Eight scenarios', 'Direction words, no numbers',
            'Each scenario gives a direction only if its assumptions hold. It is no forecast, gives no odds, and the four families are never added together.',
            {'id': col('id', 'V7 scenario ID, i to viii'), 'name': col('text', 'scenario name, V7’s words'),
             'assumptions': col('text', 'V7’s assumptions, joined with "; "'), **cdesc},
            (f'{ATLAS_LINE}, reform outcomes, eight scenarios, conditional directions to 2036 from a 2026 baseline, United States. Snapshot of {SNAP_WORDS}. '
             'Each scenario gives a direction only if its assumptions hold. It is no forecast, gives no odds, and the four families are never added together.'),
            'all', ['S06'], intro=V7['scenarios']['intro'],
            # the editor's wording for the line's close (DR-191 read, E8), as a variant S06 can print
            source_line_variants={'directions_wording': (
                f'{ATLAS_LINE}, reform outcomes, eight scenarios, conditional directions to 2036 from a 2026 baseline, United States. Snapshot of {SNAP_WORDS}. '
                'Each scenario gives a direction, with no odds, that holds only if its assumptions do, and the atlas keeps the four families apart.')},
            domain_note='The scenarios cover four outcome families across every domain of the atlas',
            class_method=("The studio’s coarse reading of V7’s direction words, for a glyph or tint only. The words are V7’s and always print beside any glyph. "
                          "Words that start ‘up’ read up, except ‘up modestly’; ‘slightly up’, ‘up modestly’ and ‘small and slow’ read slightly up; "
                          "‘flat’, ‘near trend’ and ‘flat through 2036’ read flat; ‘down or flat’ and ‘flat, or down if ...’ read flat or down; "
                          "‘down’ reads down; ‘mixed’ and ‘prices down ...; employment effects mixed’ read mixed; ‘same as scenario ii’ points to scenario ii."),
            class_rules=['A glyph or tint is a reading aid only; the four families are never added or tallied, so no badge, count or title may say "all four up".',
                         '"same as ii" points to scenario ii and must print as words; it is no direction of its own.'],
            families=FAM)

    # S09: history events on four threads
    TH = {t['id']: t for t in V7['history']['threads']}
    ev = sorted(V7['history']['events'], key=lambda e: e['date'])
    erows = [{'key': f'E{i + 1:02d}', 'date': e['date'], 'year': int(e['date'][:4]), 'thread': e['thread'], 'thread_label': TH[e['thread']]['label'],
              'title': e['title'], 'mechanism': e['mechanism'], 'loop': e.get('loop'), 'source_text': e['source_text'], 'grade': e['quality']}
             for i, e in enumerate(ev)]
    write_v7('v7-history-events', ['key', 'date', 'year', 'thread', 'thread_label', 'title', 'mechanism', 'loop', 'source_text', 'grade'], erows)
    v7_meta('v7-history-events', 'history, 24 events on four threads', 'history.events', 'February 3, 1870 to June 29, 2026', 'United States',
            'Changes in the rules that decided who counts, who governs, who owns and who checks', 'One row per event',
            'Each event rests on a statute, ruling, constitutional text or official record, cited in its own row; the size of any effect comes from the source named beside it.',
            {'key': col('id', 'the studio’s key, E01 to E24 in date order; V7 events carry no IDs'), 'date': col('date', 'date of the event'),
             'year': col('year', 'its year'), 'thread': col('category', 'V7 thread ID'), 'thread_label': col('category', 'V7 thread label'),
             'title': col('text', 'V7’s title'), 'mechanism': col('text', 'V7’s mechanism'), 'loop': col('text', 'the loop V7 ties it to'),
             'source_text': col('text', 'V7’s source'), 'grade': col('category', 'V7’s quality word')},
            (f'{ATLAS_LINE}, history, 24 events, February 3, 1870 to June 29, 2026, United States. Snapshot of {SNAP_WORDS}. '
             'Each event rests on a statute, ruling, constitutional text or official record, cited in its own row; the size of any effect comes from the source named beside it.'),
            'all', ['S09'], threads=[{'id': t['id'], 'label': t['label'], 'question': t['question']} for t in V7['history']['threads']],
            events_note=V7['history']['events_note'],
            domain_note='The four threads run across domains D02, D05, D06 and D08 alike')

    # S10: claims by grade for each of the 16 everyday questions
    GR = ['documented', 'well-supported', 'plausible', 'contested']
    HUB = {h['id']: (h.get('title') or h.get('name')) for h in V7['hubs']}
    cnt = collections.defaultdict(collections.Counter)
    for c in V7['claims'].values():
        cnt[c['pathway']][c['confidence']] += 1
    crow = []
    for p in V7['pathways']:
        k = cnt[p['id']]
        crow.append({'id': p['id'], 'title': p['title'], 'question': p['question'], 'hub': p['hub'], 'hub_title': HUB[p['hub']],
                     'documented': k['documented'], 'well_supported': k['well-supported'], 'plausible': k['plausible'], 'contested': k['contested'],
                     'total': sum(k.values()), 'documented_share': round(100 * k['documented'] / sum(k.values()), 1) if sum(k.values()) else None})
    if sum(r['total'] for r in crow) != len(V7['claims']):
        raise SystemExit('S10: claims by pathway do not add to the register')
    write_v7('v7-claims-by-grade', ['id', 'title', 'question', 'hub', 'hub_title', 'documented', 'well_supported', 'plausible', 'contested', 'total', 'documented_share'], crow)
    # ST S6 (D3-519): 432 of the 433 claims carry the October 15, 2026 check date and one carries none, so the line counts them
    claims = list(V7['claims'].values()) if isinstance(V7['claims'], dict) else list(V7['claims'])
    on_snap = sum(1 for x in claims if x.get('verified_on') == SNAP)
    checked = (f'{on_snap} of the {len(claims)} claims checked on {SNAP_WORDS}' if on_snap < len(claims)
               else f'claims checked on {SNAP_WORDS}')
    v7_meta('v7-claims-by-grade', 'claims register, 433 claims across 16 everyday questions, by evidence grade', 'claims, counted by pathway and confidence',
            checked[0].upper() + checked[1:], 'United States', 'The 433 claims behind the atlas’s 16 everyday answers', 'Claims',
            'Grades are the atlas’s own, defined on its evidence page; a claim’s grade covers that claim alone.',
            {'id': col('id', 'V7 pathway ID, PW01 to PW16'), 'title': col('text', 'pathway title'), 'question': col('text', 'its everyday question'),
             'hub': col('id', 'V7 hub ID'), 'hub_title': col('category', 'hub title'), 'documented': col('integer', 'claims graded documented'),
             'well_supported': col('integer', 'claims graded well-supported'), 'plausible': col('integer', 'claims graded plausible'),
             'contested': col('integer', 'claims graded contested'), 'total': col('integer', 'all claims on the pathway'),
             'documented_share': col('number', 'documented claims as a share of all claims on the pathway, one decimal; the studio\u2019s arithmetic on V7\u2019s counts (request E4)', 'percent')},
            (f'{ATLAS_LINE}, claims register, 433 claims across 16 everyday questions, {checked}, United States. '
             f'Snapshot of {SNAP_WORDS}. Grades are the atlas’s own, defined on its evidence page; a claim’s grade covers that claim alone.'),
            'all', ['S10'], grade_meaning={'documented': 'on the public record', 'well-supported': 'strong research evidence', 'plausible': 'some evidence', 'contested': 'evidence disputed'},
            domain_note='The 16 everyday questions span the atlas’s five hubs and every domain')
    # maker A's A4 (round 1, S23): the same claims grouped by the atlas's five hubs, one row per hub and grade (C1, derived)
    hubs = []
    for r in crow:
        if r['hub'] not in hubs:
            hubs.append(r['hub'])
    hrow = []
    for h in hubs:
        rs = [r for r in crow if r['hub'] == h]
        hub_claims = sum(r['total'] for r in rs)
        for g in ('documented', 'well_supported', 'plausible', 'contested'):
            n = sum(r[g] for r in rs)
            hrow.append({'hub': h, 'hub_title': HUB[h], 'grade': g, 'claims': n, 'hub_claims': hub_claims,
                         'share_pct': round(100 * n / hub_claims, 1) if hub_claims else None, 'answers': len(rs)})
    if sum(r['claims'] for r in hrow) != len(V7['claims']) or len(hrow) != 4 * len(hubs):
        raise SystemExit('A4: claims by hub and grade do not add to the register')
    write_v7('v7-claims-by-hub-and-grade', ['hub', 'hub_title', 'grade', 'claims', 'hub_claims', 'share_pct', 'answers'], hrow)
    v7_meta('v7-claims-by-hub-and-grade', 'claims register, 433 claims across 16 everyday questions, grouped by its five topic hubs, by evidence grade',
            'claims, counted by pathway and confidence, summed by hub',
            checked[0].upper() + checked[1:], 'United States', 'The 433 claims behind the atlas’s 16 everyday answers', 'Claims',
            'Grades are the atlas’s own, defined on its evidence page; a claim’s grade covers that claim alone.',
            {'hub': col('id', 'V7 hub ID'), 'hub_title': col('category', 'hub title'),
             'grade': col('category', 'evidence grade: documented, well_supported, plausible or contested'),
             'claims': col('integer', 'claims of this grade on the hub’s pathways'), 'hub_claims': col('integer', 'all claims on the hub’s pathways'),
             'share_pct': col('number', 'claims of this grade as a share of the hub’s claims, one decimal; the studio’s arithmetic on V7’s counts', 'percent'),
             'answers': col('integer', 'everyday questions (pathways) in the hub')},
            (f'{ATLAS_LINE}, claims register, 433 claims across 16 everyday questions grouped by its five topic hubs, {checked}, '
             f'United States. Snapshot of {SNAP_WORDS}. Grades are the atlas’s own, defined on its evidence page; a claim’s grade covers that claim alone.'),
            'all', ['S23'], kind='derived', derived_from=['v7-claims-by-grade.json'],
            derivation='The rows of v7-claims-by-grade summed by hub, in that file’s hub order, grades in the order documented, well-supported, plausible, contested; share_pct is claims over hub_claims (request A4).',
            grade_meaning={'documented': 'on the public record', 'well-supported': 'strong research evidence', 'plausible': 'some evidence', 'contested': 'evidence disputed'},
            domain_note='The five hubs span every domain, as the 16 everyday questions do')


# ---------------------------------------------------------------------------------------------------------------
# The check: every file in the folder against the contract
# ---------------------------------------------------------------------------------------------------------------
# R1-C7 (round 1) and R3-2 (round 3): a boundary file's sidecar names these beside C1's fields, and its features carry
# exactly the properties its columns list, geoid first
GEO_REQUIRED = ('geometry_type', 'source_resolution', 'raw_file', 'raw_file_sha256', 'feature_count', 'coordinates')
GEOID_DIGITS = {2, 4, 5, 7}


def check_geojson(dp, m):
    """A boundary file under R1-C7: an RFC 7946 FeatureCollection in UTF-8 with no byte-order mark; one Feature per
    place, sorted by geoid, a Polygon or MultiPolygon; properties exactly the sidecar's columns (geoid, code, name, and
    district on districts); longitude and latitude in range with at most six decimals; every ring closed, of four points
    or more; no bbox and no id outside properties; the count the sidecar gives. Returns faults."""
    faults = []
    raw = dp.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        faults.append(f'{dp.name}: starts with a byte-order mark')
    try:
        gj = json.loads(raw.decode('utf-8'))
    except Exception as ex:
        return [f'{dp.name}: does not parse as UTF-8 JSON ({ex})']
    for k in GEO_REQUIRED:
        if k not in m or m[k] in (None, ''):
            faults.append(f'{dp.name}: its sidecar lacks {k} (R1-C7)')
    if gj.get('type') != 'FeatureCollection' or not isinstance(gj.get('features'), list):
        return faults + [f'{dp.name}: not a FeatureCollection']
    if 'bbox' in gj:
        faults.append(f'{dp.name}: carries a bbox (R1-C7 leaves it out)')
    feats = gj['features']
    if m.get('feature_count') != len(feats):
        faults.append(f'{dp.name}: {len(feats)} features, but the sidecar says {m.get("feature_count")}')
    cols = list((m.get('columns') or {}).keys())
    if cols[:1] != ['geoid']:
        faults.append(f'{dp.name}: the sidecar\'s first column is not geoid')
    ids, bad = [], 0
    dec6 = re.compile(r'^-?\d+(?:\.\d{1,6})?$')
    for i, f in enumerate(feats):
        where = f'{dp.name}: feature {i + 1}'
        if f.get('type') != 'Feature' or 'id' in f or 'bbox' in f:
            faults.append(f'{where} is not a plain Feature (no id or bbox outside properties)')
        pr = f.get('properties') or {}
        if list(pr.keys()) != cols:
            faults.append(f'{where}: properties {list(pr.keys())} differ from the sidecar\'s columns {cols}')
        gid = str(pr.get('geoid', ''))
        if not (gid.isdigit() and len(gid) in GEOID_DIGITS) and gid != 'US':
            faults.append(f'{where}: geoid {gid!r} is not the Bureau\'s digits')
        if 'code' in pr and not re.fullmatch(r'[A-Z]{2}', str(pr['code'])):
            faults.append(f'{where}: code {pr["code"]!r} is not a USPS code')
        ids.append(gid)
        g = f.get('geometry') or {}
        if g.get('type') not in ('Polygon', 'MultiPolygon'):
            faults.append(f'{where}: geometry {g.get("type")!r} is not a Polygon or MultiPolygon')
            continue
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            for ring in poly:
                if len(ring) < 4 or ring[0] != ring[-1]:
                    bad += 1
                    if bad <= 3:
                        faults.append(f'{where}: a ring is open or has under four points')
                for pt in ring:
                    if len(pt) != 2 or not (-180 <= pt[0] <= 180 and -90 <= pt[1] <= 90):
                        bad += 1
                        if bad <= 3:
                            faults.append(f'{where}: a point {pt} is not a longitude and latitude')
                        break
        if i < 40 or i % 97 == 0:
            # the six-decimal rule, read from the file's own text for a sample of features (json.loads drops the text)
            txt = json.dumps(g['coordinates'][:1])
            for num in re.findall(r'-?\d+\.\d+(?:e-?\d+)?', txt):
                if not dec6.match(num):
                    faults.append(f'{where}: a coordinate {num} carries more than six decimals')
                    break
    if ids != sorted(ids):
        faults.append(f'{dp.name}: features are not sorted by geoid')
    if len(set(ids)) != len(ids):
        faults.append(f'{dp.name}: a geoid appears twice')
    return faults


def load_rows(p):
    if p.suffix == '.csv':
        return read_csv(p), None
    d = json.loads(p.read_text())
    return d.get('rows'), d


def check_derived(out=OUT):
    """D3-95: every derived value equals the value computed from the publisher's counts or levels, to six decimals, so the
    kit rounds once. Returns faults."""
    faults = []
    res = {(r['code'], int(float(r['year']))): r for r in read_csv(out / 'fec-presidential-results-by-state.csv')}
    for r in read_csv(out / 'fec-presidential-shift-by-state.csv'):
        if r['code'] == 'US':
            continue
        for y in (2020, 2024):
            src = res[(r['code'], y)]
            want = 100 * (num(src['rep_votes']) - num(src['dem_votes'])) / num(src['total_votes'])
            if abs(num(r[f'margin_{y}']) - want) > 1e-5:
                faults.append(f"fec-presidential-shift-by-state: {r['code']} margin_{y} reads {r[f'margin_{y}']}, the counts give {want:.6f}")
    lev = {}
    for r in read_csv(out / 'fred-payrolls-by-sector-change.csv'):
        lev.setdefault(r['series_id'], []).append(r)
    for sid, rs in lev.items():
        base = num(rs[0]['employees_thousands'])
        for r in rs:
            v = num(r['employees_thousands'])
            if v is None or r['pct_change_since_2022_01'] in ('', None):
                continue
            want = (v / base - 1) * 100
            if abs(num(r['pct_change_since_2022_01']) - want) > 1e-5:
                faults.append(f"fred-payrolls-by-sector-change: {sid} {r['month']} reads {r['pct_change_since_2022_01']}, the levels give {want:.6f}")
    return faults


def check_folder(out=OUT):
    faults = check_derived(out)
    metas = sorted(out.glob('*.meta.json'))
    datas = sorted(p for p in out.iterdir() if p.suffix in ('.csv', '.json', '.geojson') and not p.name.endswith('.meta.json'))
    for p in out.iterdir():
        if p.is_dir():
            faults.append(f'{p.name}: the folder is flat; no subfolders')
        elif not (p.suffix in ('.csv', '.json', '.geojson')):
            faults.append(f'{p.name}: only .csv, .json, .geojson and .meta.json files belong here')
    named = set()
    for mp in metas:
        name = mp.name[:-len('.meta.json')]
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            faults.append(f'{mp.name}: name is not lowercase kebab-case')
        try:
            m = json.loads(mp.read_text())
        except Exception as ex:
            faults.append(f'{mp.name}: does not parse ({ex})')
            continue
        for k in REQUIRED:
            if k not in m or m[k] in (None, ''):
                faults.append(f'{mp.name}: missing {k}')
        if DISCLOSURE_RE.search(json.dumps(m, ensure_ascii=False)) or 'required_text' in m:
            faults.append(f'{mp.name}: carries the retired disclosure or a required_text (DR-100, D2-1756)')
        if m.get('kind') not in KINDS:
            faults.append(f'{mp.name}: kind {m.get("kind")!r} is not one of {sorted(KINDS)}')
        if m.get('domain') not in DOMAINS:
            faults.append(f'{mp.name}: domain {m.get("domain")!r} is not D01 to D10 or all')
        if not isinstance(m.get('states'), list) or any(not re.fullmatch(r'[A-Z]{2}', s) for s in m.get('states') or []):
            faults.append(f'{mp.name}: states must be a list of USPS codes')
        line = m.get('printed_source_line') or ''
        if not line.startswith('Source: '):
            faults.append(f'{mp.name}: printed_source_line must start "Source: "')
        # access S1 (round 1 fix pass): a template the kit fills with the years a chart draws
        tpl = m.get('source_line_templates')
        if tpl is not None and (not isinstance(tpl, dict) or any(not isinstance(t, str) or not t.startswith('Source: ') or '{from}' not in t or '{to}' not in t for t in tpl.values())):
            faults.append(f'{mp.name}: source_line_templates is an object of lines that start "Source: " and hold {{from}} and {{to}}')
        if '—' in json.dumps(m, ensure_ascii=False) or '‑' in json.dumps(m, ensure_ascii=False):
            faults.append(f'{mp.name}: an em dash or U+2011 in the sidecar')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(m.get('date_retrieved', ''))):
            faults.append(f'{mp.name}: date_retrieved is not YYYY-MM-DD')
        if m.get('kind') == 'derived' and not (m.get('derived_from') and m.get('derivation')):
            faults.append(f'{mp.name}: a derived table names derived_from and derivation')
        if m.get('kind') == 'v7' and m.get('snapshot') != SNAP:
            faults.append(f'{mp.name}: a V7 table names the snapshot {SNAP}')
        dp = out / m.get('file', '')
        if not dp.is_file():
            faults.append(f'{mp.name}: its data file {m.get("file")} is missing')
            continue
        if dp.suffix == '.geojson':
            # R1-C7: a boundary file, public, named census-cb-<year>-..., read as shapes rather than rows
            named.add(dp.name)
            if m.get('kind') != 'public' or not name.startswith('census-cb-'):
                faults.append(f'{mp.name}: a boundary file is kind public and named census-cb-<year>-<set>')
            faults.extend(check_geojson(dp, m))
            continue
        if (dp.suffix == '.json') != name.startswith('v7-'):
            faults.append(f'{mp.name}: V7 tables are v7-*.json and only they are JSON')
        named.add(dp.name)
        rows, _ = load_rows(dp)
        cols = m.get('columns') or {}
        if not rows:
            faults.append(f'{dp.name}: no rows')
            continue
        keys = list(rows[0].keys())
        if keys != list(cols.keys()):
            faults.append(f'{dp.name}: columns {keys} differ from the sidecar’s {list(cols.keys())}')
        for c, spec in cols.items():
            if not isinstance(spec, dict) or spec.get('type') not in TYPES or not spec.get('description'):
                faults.append(f'{mp.name}: column {c} needs a type from {sorted(TYPES)} and a description')
                continue
            t = spec['type']
            for i, r in enumerate(rows):
                v = r.get(c)
                if v in ('', None):
                    continue
                v = str(v)
                bad = ((t in ('number',) and num(v) is None) or (t == 'integer' and not re.fullmatch(r'-?\d+', v)) or
                       (t == 'date' and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', v)) or (t == 'month' and not re.fullmatch(r'\d{4}-\d{2}', v)) or
                       (t == 'year' and not re.fullmatch(r'\d{4}', v)) or (t == 'boolean' and v.lower() not in ('true', 'false', '0', '1')))
                if bad:
                    faults.append(f'{dp.name}: row {i + 1} column {c} = {v!r} is not a {t}')
                    break
                if v.strip().upper() in ('NA', 'N/A', '-'):
                    faults.append(f'{dp.name}: row {i + 1} column {c} uses {v!r} for missing; leave it empty')
                    break
        if dp.suffix == '.json':
            for r in rows:
                if any(isinstance(v, (dict, list)) for v in r.values()):
                    faults.append(f'{dp.name}: a V7 row holds a list or object; join lists with "; "')
                    break
    for dp in datas:
        if dp.name not in named:
            faults.append(f'{dp.name}: has no sidecar')
    return faults


def main():
    if '--check' not in sys.argv:
        OUT.mkdir(parents=True, exist_ok=True)
        copy_public()
        derive_fec_shift()
        derive_fred()
        v7_tables()
    faults = check_folder()
    n = len(list(OUT.glob('*.meta.json')))
    for f in faults:
        print('FAULT', f)
    print(f'{OUT.relative_to(ROOT)}: {n} tables, {len(faults)} faults')
    return 1 if faults else 0


if __name__ == '__main__':
    sys.exit(main())
