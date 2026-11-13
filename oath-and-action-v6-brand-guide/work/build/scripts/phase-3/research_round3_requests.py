"""research_round3_requests.py: the data lead's round 3 requests RL-1 to RL-3 on three frozen files (research ledger
P7-211, P7-212 and P7-216), November 13, 2026.

Run, with the downloads in folders of their own:

    python3 -I work/build/scripts/phase-3/research_round3_requests.py rl1 --dl <folder with us.json, county.json>
    python3 -I work/build/scripts/phase-3/research_round3_requests.py rl2 --dl <folder with cbp23co.zip, cbp23st.zip, cbp23us.zip>
    python3 -I work/build/scripts/phase-3/research_round3_requests.py rl3 --dl <folder with sbr-*.json and agg-*.json>

Each item reads its downloads, asserts every frozen field unchanged (D3-476, D3-1052), adds what the request asks after
the frozen columns or as a new row, and sets values rather than appending, so a rerun writes nothing. It refuses to
write when a check fails.

- RL-1: the nation's row in census-acs5-county-median-household-income (B19013, 5-year 2020 to 2024, us:1), first,
  code US, as the broadband and business formation files carry the nation; the county rows are re-read and must equal.
- RL-2: census-cbp-county-employment gains each county's noise flag from the Bureau's 2023 county file (G, H or J, the
  record layout's letters), and the sidecar traces the gap between the counties' sum and the national total.
- RL-3: fec-jfc-transfers-2024 gains each recipient's name as its joint fundraising committee wrote it on the itemized
  payments, the line 21B payments the FEC's aggregate leaves out, and the lines its amount sums.
- judges (the brief's third research item, ledger claim 28): the courts' 677 district positions traced to 28 U.S.C.
  133's 673 and the territorial courts' 4; uscode-federal-trial-judges and uscode-federal-courts-circuits-districts
  print the same account. Run with any --dl; it reads only the frozen files.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'work/build/data'
ELECTION = '2024-11-05'


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def read_csv_raw(p):
    b = p.read_bytes()
    rows = list(csv.reader(io.StringIO(b.decode('utf-8'))))
    s = io.StringIO()
    csv.writer(s, lineterminator='\n').writerows(rows)
    assert s.getvalue().encode('utf-8') == b, f'{p.name} does not round-trip; stop'
    return rows


def write_csv(rows):
    s = io.StringIO()
    csv.writer(s, lineterminator='\n').writerows(rows)
    return s.getvalue()


def read_meta(p):
    t = p.read_text(encoding='utf-8')
    m = json.loads(t)
    assert json.dumps(m, indent=1, ensure_ascii=False) == t, f'{p.name} is not in its writer format; stop'
    return m


def dump_meta(m):
    t = json.dumps(m, indent=1, ensure_ascii=False)
    assert '—' not in t and '‑' not in t, 'an em dash or U+2011'
    return t


def put(path, text, write):
    if path.read_text(encoding='utf-8') == text:
        return 'unchanged'
    if write:
        path.write_text(text, encoding='utf-8')
        return 'written'
    return 'would write'


def set_note(notes, startswith, new):
    """Replace the note that starts with `startswith` (or a note already equal to `new`); else add `new`."""
    for i, n in enumerate(notes):
        if n == new or n.startswith(startswith):
            notes[i] = new
            return notes
    notes.append(new)
    return notes


# ------------------------------------------------------------------------------------------------------------------
def rl1(dl, write):
    name = 'census-acs5-county-median-household-income'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    rows, m = read_csv_raw(cp), read_meta(mp)
    head, body = rows[0], [r for r in rows[1:] if r[0] != 'US']
    assert head == ['geoid', 'name', 'state', 'median_household_income', 'moe']
    assert len(body) == 3144
    us = json.loads((dl / 'us.json').read_text())
    co = json.loads((dl / 'county.json').read_text())
    assert us[0] == ['NAME', 'B19013_001E', 'B19013_001M', 'us'] and len(us) == 2 and us[1][0] == 'United States'
    api = {r[3] + r[4]: r for r in co[1:]}
    for r in body:  # every frozen county equals today's API (a negative value is the API's code for no estimate)
        a = api[r[0]]
        val = '' if int(a[1]) < 0 else a[1]
        moe = '' if int(a[2]) < 0 else a[2]
        assert (r[3], r[4]) == (val, moe), (r, a)
    nat = ['US', 'United States', 'US', us[1][1], us[1][2]]
    out = [head, nat] + body
    m['geography'] = ('Every county and county equivalent in the 50 states and DC (3144), Puerto Rico left out; Connecticut '
                      'by its nine planning regions; and the United States as the first row (code US)')
    url_us = 'https://api.census.gov/data/2024/acs/acs5?get=NAME,B19013_001E,B19013_001M&for=us:1'
    if url_us not in m['url']:
        m['url'].append(url_us)
    m['columns']['geoid']['description'] = 'county FIPS code, state and county; US for the nation'
    m['columns']['state']['description'] = 'USPS state code; US for the nation'
    v = m.get('source_line_variants') or {}
    v['with_united_states'] = ('Source: U.S. Census Bureau, American Community Survey 5-year estimates, Table B19013, median '
                               'household income, 2020 to 2024, every county in the 50 states and DC, and the United States. '
                               'Retrieved November 12 and 13, 2026. Survey estimates in 2024 dollars; margins are wide in '
                               'small counties.')
    m['source_line_variants'] = v
    m['notes'] = set_note(list(m.get('notes') or []), 'The United States row',
                          f'The United States row (RL-1), first in the file: ${int(us[1][1]):,} with a 90 percent margin '
                          f'of ${int(us[1][2]):,}, from the same table and release (for=us:1), read November 13, 2026. '
                          'The same call for every county returned all 3,144 frozen values unchanged. A map sets the '
                          'nation apart beside it, never as a region.')
    m['raw_files_sha256_prefix'] = dict(m.get('raw_files_sha256_prefix') or {}, **{
        'us.json (2026-11-13)': sha16(dl / 'us.json'), 'county.json (2026-11-13)': sha16(dl / 'county.json')})
    return [(cp, write_csv(out)), (mp, dump_meta(m))], f'nation ${int(us[1][1]):,} ± ${int(us[1][2]):,}; 3,144 counties equal'


# ------------------------------------------------------------------------------------------------------------------
FLAG_WORDS = {'G': 'low noise: changed by less than 2 percent', 'H': 'medium noise: changed by 2 to under 5 percent',
              'J': 'high noise: changed by 5 percent or more'}


def cbp_rows(zpath):
    z = zipfile.ZipFile(zpath)
    n = [i for i in z.namelist() if i.lower().endswith('.txt')]
    assert len(n) == 1
    with z.open(n[0]) as f:
        r = csv.DictReader(io.TextIOWrapper(f, encoding='latin-1'))
        r.fieldnames = [x.strip().lower() for x in r.fieldnames]
        for row in r:
            if row['naics'].strip() == '------':
                yield {k: (v or '').strip() for k, v in row.items()}


def rl2(dl, write):
    name = 'census-cbp-county-employment'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    rows, m = read_csv_raw(cp), read_meta(mp)
    frozen_head = ['geoid', 'name', 'state', 'paid_employees', 'establishments']
    assert rows[0][:5] == frozen_head
    co = {r['fipstate'] + r['fipscty']: r for r in cbp_rows(dl / 'cbp23co.zip')}
    total = lambda r: r.get('lfo', '-') == '-' and r.get('empszes', '001') == '001'
    st = {r['fipstate']: int(r['emp']) for r in cbp_rows(dl / 'cbp23st.zip') if total(r)}
    us = [int(r['emp']) for r in cbp_rows(dl / 'cbp23us.zip') if total(r)]
    assert us == [139831742] and sum(st.values()) == us[0] and len(st) == 51
    head = frozen_head + ['emp_noise_flag', 'emp_noise_words']
    out = [head]
    for r in rows[1:]:
        f = co[r[0]]
        assert (int(f['emp']), int(f['est'])) == (int(r[3]), int(r[4])), r  # the file's counts equal the frozen API counts
        assert f['emp_nf'] in FLAG_WORDS, f
        out.append(r[:5] + [f['emp_nf'], FLAG_WORDS[f['emp_nf']]])
    assert len(out) == 3143
    flags = collections.Counter(r[5] for r in out[1:])
    sw = {k: int(v['emp']) for k, v in co.items() if k.endswith('999')}
    counties = sum(int(r[3]) for r in out[1:])
    assert counties == 132151802 and len(sw) == 50
    resid = {}
    for s, t in st.items():
        c = sum(int(r[3]) for r in out[1:] if r[0][:2] == s) + sum(v for k, v in sw.items() if k[:2] == s)
        if c != t:
            resid[s] = t - c
    assert resid == {'15': 3, '48': 2}, resid  # Hawaii and Texas, the two states with a county the file leaves out
    top = sorted(((v, k) for k, v in sw.items()), reverse=True)[:3]
    names = {'12': 'Florida', '06': 'California', '48': 'Texas'}
    m['columns']['emp_noise_flag'] = {'type': 'category', 'description': 'the Bureau’s noise flag for paid_employees, '
                                      'from its 2023 county file: G low, H medium, J high'}
    m['columns']['emp_noise_words'] = {'type': 'text', 'description': 'the flag’s meaning, in the record layout’s words'}
    m['qualification'] = (
        'Counts private-sector paid employees where they work, not where they live. The Bureau adds noise to each '
        'establishment’s figures to protect employers, and flags each published count by how much noise changed it: '
        f'G, less than 2 percent ({flags["G"]:,} counties); H, 2 to under 5 percent ({flags["H"]:,}); J, 5 percent or '
        f'more ({flags["J"]:,}). The flags come from the Bureau’s downloadable 2023 county file, whose counts equal the '
        'data API’s in every row; the API’s own noise range code returned 0 for every county, and its variable list '
        'defines no values for it. Kalawao County, Hawaii, and King County, Texas, are not in the file.')
    for u in ('https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23co.zip',
              'https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23st.zip',
              'https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23us.zip',
              'https://www2.census.gov/programs-surveys/cbp/technical-documentation/records-layouts/2020_record_layouts/county-layout-2020.txt',
              'https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html'):
        if u not in m['url']:
            m['url'].append(u)
    gap = us[0] - counties
    notes = list(m.get('notes') or [])
    notes = set_note(notes, 'The counties sum to 132,151,802',
                     f'The counties sum to {counties:,} paid employees; the national row, all sectors, gives {us[0]:,}, '
                     f'{gap:,} more (RL-2). The Bureau’s 2023 county file holds 50 "statewide" records (county code '
                     f'999), {sum(sw.values()):,} employees in all; the methodology page says "Employers without a fixed '
                     'location within a state (or of unknown county location) are included under a “statewide” '
                     'classification. This incomplete detail causes only slight understatement of county employment," '
                     'and that employee-leasing establishments may be published statewide. The largest are '
                     + ', '.join(f'{names[k[:2]]} {v:,}' for v, k in top) +
                     f'. The last {gap - sum(sw.values())} are in the state totals of Hawaii ({resid["15"]}) and Texas '
                     f'({resid["48"]}) beyond their counties and statewide records: the two states whose one county the '
                     'file leaves out (Kalawao County and King County). Counties, statewide records and those 5 sum to '
                     'the national total, and the 51 state totals sum to it exactly. Read November 13, 2026.')
    notes = set_note(notes, 'Noise flags (RL-2)',
                     'Noise flags (RL-2): the record layout for 2020 to 2023 defines "G 0 to < 2% noise (low noise)", '
                     '"H 2 to < 5% noise (medium noise)" and "J >= 5% noise (high noise)". A table marks the J counties '
                     'at least; a count flagged H or J differs from the unperturbed figure by the share its flag gives.')
    m['notes'] = notes
    v = m.get('source_line_variants') or {}
    v['with_noise_flags'] = ('Source: U.S. Census Bureau, County Business Patterns, paid employees by county, 2023, '
                             'counties of the 50 states and DC, with the Bureau’s noise flags. Retrieved November 12 and '
                             '13, 2026. Private-sector paid employees only, counted where they work.')
    m['source_line_variants'] = v
    m['raw_files_sha256_prefix'] = dict(m.get('raw_files_sha256_prefix') or {}, **{
        f'{z} (2026-11-13)': sha16(dl / z) for z in ('cbp23co.zip', 'cbp23st.zip', 'cbp23us.zip')})
    return [(cp, write_csv(out)), (mp, dump_meta(m))], (f'flags G {flags["G"]}, H {flags["H"]}, J {flags["J"]}; gap '
                                                        f'{gap:,} = statewide {sum(sw.values()):,} + 5')


# ------------------------------------------------------------------------------------------------------------------
def rl3(dl, write):
    name = 'fec-jfc-transfers-2024'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    rows, m = read_csv_raw(cp), read_meta(mp)
    frozen_head = ['nominee', 'jfc_id', 'jfc_name', 'recipient_id', 'recipient_name', 'recipient_type', 'recipient_state',
                   'amount', 'transactions', 'schedule_b_lines', 'is_nominee_campaign']
    assert rows[0][:11] == frozen_head and len(rows) == 58
    new_cols = ['recipient_name_2024_election', 'recipient_names_itemized', 'amount_lines', 'line_21b_amount',
                'line_21b_transactions']
    agg = {}
    for j in ('C00744946', 'C00873893'):
        for a in json.loads((dl / f'agg-{j}.json').read_text())['results']:
            agg[(j, a['recipient_id'])] = a
    out = [frozen_head + new_cols]
    found = collections.Counter()
    for r in rows[1:]:
        r = r[:11]
        a = agg[(r[1], r[3])]  # the FEC's aggregate today equals the frozen amount and count
        assert abs(a['total'] - float(r[7])) < 0.005 and a['count'] == int(r[8]), (r, a)
        d = json.loads((dl / f'sbr-{r[1]}-{r[3]}.json').read_text())
        res = d['results']
        assert d['pagination']['count'] == len(res) and all(x['memo_code'] is None for x in res)
        assert len({x['transaction_id'] for x in res}) == len(res)
        res.sort(key=lambda x: (x['disbursement_date'], x['transaction_id']))
        lines = collections.defaultdict(list)
        for x in res:
            lines[x['line_number']].append(x)
        counted = [ln for ln in ('22', '28C') if ln in lines]
        assert len(counted) == 1 and set(lines) <= {'22', '28C', '21B'}, (r, set(lines))
        c = lines[counted[0]]
        assert len(c) == int(r[8]) and abs(sum(x['disbursement_amount'] for x in c) - float(r[7])) < 0.005, r
        found[counted[0]] += 1
        before = [x for x in res if x['disbursement_date'][:10] <= ELECTION]
        pick = before[-1] if before else res[0]
        same_day = {x['recipient_name'] for x in res if x['disbursement_date'] == pick['disbursement_date']}
        assert len(same_day) == 1, (r, same_day)
        spans = collections.OrderedDict()
        for x in res:
            s = spans.setdefault(x['recipient_name'], [0, x['disbursement_date'][:10], x['disbursement_date'][:10]])
            s[0] += 1
            s[2] = x['disbursement_date'][:10]
        names = '; '.join(f'{k} ({v[0]} {"row" if v[0] == 1 else "rows"}, {v[1]} to {v[2]})' for k, v in spans.items())
        b = lines.get('21B', [])
        out.append(r + [pick['recipient_name'], names, counted[0], f'{sum(x["disbursement_amount"] for x in b):.2f}', str(len(b))])
    assert found == {'22': 55, '28C': 2}, found
    by = {row[3]: row for row in out[1:]}
    assert by['C00703975'][11] == 'HARRIS FOR PRESIDENT' and by['C00828541'][11] == 'DONALD J. TRUMP FOR PRESIDENT 2024, INC.'
    cols = m['columns']
    cols['recipient_name']['description'] = ('its name as the FEC’s aggregate by recipient gave it on November 12, 2026: '
                                             'mostly the committee’s name today, but Harris’s campaign under its 2024 name '
                                             'and Trump’s under its name today; print recipient_name_2024_election')
    cols['recipient_type']['description'] = ('committee type as the FEC lists it today; both campaign committees have since '
                                             'become PACs, and is_nominee_campaign marks them')
    cols['schedule_b_lines']['description'] = ('every Schedule B line the itemized payments to this committee use, line '
                                               '21B included; amount sums only the line in amount_lines')
    cols['recipient_name_2024_election'] = {'type': 'text', 'description': (
        'the name the joint fundraising committee wrote for this recipient on its last itemized payment dated on or before '
        'November 5, 2024 (its first payment, where none came before), read the same way for every recipient')}
    cols['recipient_names_itemized'] = {'type': 'text', 'description': (
        'every name the itemized payments give this recipient, each with its row count and first and last date')}
    cols['amount_lines'] = {'type': 'category', 'description': (
        'the Schedule B line amount and transactions sum: 22, transfers to other committees, or 28C, a refund of a '
        'committee’s contribution')}
    cols['line_21b_amount'] = {'type': 'number', 'unit': 'dollars', 'description': (
        'line 21B operating expenditures paid to the same committee in the cycle, not in amount')}
    cols['line_21b_transactions'] = {'type': 'integer', 'description': 'itemized line 21B payments, not in transactions'}
    m['qualification'] = (
        'Amounts and transactions are the FEC’s aggregate of Schedule B by recipient for the cycle, which sums line 22 '
        'transfers to other committees (55 rows) and, for two committees, a line 28C refund of their own contribution '
        '(Progressive Turnout Project, $80,000; Operating Engineers Local 478, $1,000). It leaves out line 21B operating '
        'expenditures paid to three of the same committees, which line_21b_amount gives: $11,993,565.82 to Harris’s '
        'campaign, $15,146,635.19 to the DNC and $1,501.00 to Kentucky’s party. A joint fundraising committee splits '
        'contributions among its participants under its agreement, so a transfer is not a gift from the committee’s own '
        'funds. Each nominee had more than one joint fundraising committee; the rule above picks one for each, read the '
        'same way. Names: recipient_name_2024_election gives each committee the name its payer wrote just before the '
        'election, "HARRIS FOR PRESIDENT" (called "BIDEN FOR PRESIDENT" on its 14 payments to July 2024) and "DONALD J. '
        'TRUMP FOR PRESIDENT 2024, INC."; both have since become PACs.')
    old_u = ('For each major-party nominee, the joint fundraising committee that transferred the most to the nominee’s '
             'principal campaign committee in the 2024 cycle, and every committee it paid')
    assert m['universe_or_base'] in (old_u, old_u + ' on line 22 (transfers) or line 28C (refunds)')  # RL-3a
    m['universe_or_base'] = old_u + ' on line 22 (transfers) or line 28C (refunds)'
    u = 'https://api.open.fec.gov/v1/schedules/schedule_b/?committee_id={jfc}&recipient_committee_id={recipient}&two_year_transaction_period=2024'
    if u not in m['url']:
        m['url'].append(u)
    notes = list(m.get('notes') or [])
    notes = set_note(notes, 'Schedule B lines used:', 'Schedule B lines in the itemized payments: 22 (629 rows), 21B (40) '
                     'and 28C (2); amount and transactions sum line 22, or 28C for the two refunds (RL-3, read November '
                     '13, 2026: the aggregate today equals all 57 frozen rows, and each row’s line 22 or 28C payments '
                     'sum to it).')
    notes = set_note(notes, 'The principal campaign committees have since changed',
                     'The principal campaign committees have since changed name and type, as the FEC lists them today '
                     '(principal_name_now in the note above). The FEC’s committee history for the 2024 cycle already '
                     'lists Trump’s as "NEVER SURRENDER, INC.", a leadership PAC, since it changed before the cycle '
                     'ended, so the names in the cycle come from the itemized payments instead (RL-3).')
    m['notes'] = notes
    v = m.get('source_line_variants') or {}
    v['transfers_and_refunds'] = (
        'Source: Federal Election Commission, Schedule B transfers and refunds to other committees (lines 22 and 28C) of '
        'the Harris Victory Fund and the Trump National Committee JFC, 2023 to 2024 cycle, United States. Retrieved '
        'November 12 and 13, 2026. Each is the nominee’s joint fundraising committee that sent the most to the campaign; '
        'committees named as their payer wrote them before the November 5, 2024 election.')
    m['source_line_variants'] = v
    return [(cp, write_csv(out)), (mp, dump_meta(m))], (
        f'Harris {by["C00703975"][11]}, Trump {by["C00828541"][11]}; lines {dict(found)}')


# ------------------------------------------------------------------------------------------------------------------
def read_meta_any(p):
    t = p.read_text(encoding='utf-8')
    m = json.loads(t)
    end = '\n' if t.endswith('\n') else ''
    assert json.dumps(m, indent=1, ensure_ascii=False) + end == t, f'{p.name} is not in its writer format; stop'
    return m, end


def judges(dl, write):
    """The judge counts (ledger claim 28): the courts' 677 district positions are 28 U.S.C. 133's 673 and the 4
    judgeships of the three territorial district courts. Asserted from the frozen files themselves; the Administrative
    Office's table of authorized district judgeships (January 2025), read court by court, agrees (research notes)."""
    tp, tm = OUT / 'uscode-federal-trial-judges.csv', OUT / 'uscode-federal-trial-judges.meta.json'
    cp, cm = OUT / 'uscode-federal-courts-circuits-districts.csv', OUT / 'uscode-federal-courts-circuits-districts.meta.json'
    courts = list(csv.DictReader(io.StringIO(cp.read_text(encoding='utf-8'))))
    stat = sum(int(r['judgeships']) for r in courts if r['level'] in ('district', 'district-shared'))
    terr = {r['code']: int(r['judgeships']) for r in courts if r['level'] == 'district-territorial'}
    assert stat == 673 and terr == {'GU': 1, 'MP': 1, 'VI': 2}, (stat, terr)
    rows = read_csv_raw(tp)
    frozen_head = ['order', 'kind', 'appointed_by', 'consent', 'term', 'cases_heard', 'seats', 'seats_as_of',
                   'seats_in_statute_table', 'number_set_by', 'legal_basis', 'source_words']
    assert rows[0][:12] == frozen_head and len(rows) == 4
    dist = rows[1]
    assert dist[1] == 'District judge' and int(dist[6]) == 677 and int(dist[8]) == 673 == stat
    assert int(dist[6]) == stat + sum(terr.values())
    out = [frozen_head + ['seats_in_territorial_courts']]
    for r in rows[1:]:
        out.append(r[:12] + ([str(sum(terr.values()))] if r[1] == 'District judge' else ['']))
    m, end = read_meta_any(tm)
    m['columns']['seats_in_territorial_courts'] = {'type': 'integer', 'description': (
        'of seats, the judgeships of the three territorial district courts (Guam 1, the Northern Mariana Islands 1, the '
        'Virgin Islands 2), set by Title 48, whose judges serve ten-year terms; district row only')}
    m['qualification'] = (
        'Seats are positions authorized, filled or vacant: 677 district positions (48 vacant), 345 bankruptcy '
        'judgeships authorized and funded (63 vacant), and 593 magistrate judge positions (567 full time, 24 part time, '
        '2 combined with a clerk’s post), all as of September 30, 2025. The courts’ 677 district positions are the 673 '
        'judgeships of 28 U.S.C. 133’s table and the 4 of the three territorial district courts (Guam 1, the Northern '
        'Mariana Islands 1, the Virgin Islands 2), which Title 48 sets and whose judges serve ten-year terms, not for '
        'life; the Administrative Office’s table of authorized district judgeships agrees court by court. No temporary '
        'district judgeship remains: Pub. L. 118-203 of December 23, 2024 made the last ten permanent, and the courts '
        'counted 677 in every year from 2021 to 2025. The statute table lists 316 bankruptcy judgeships; the 29 more the '
        'courts count were not traced. No appointing president or party is recorded.')
    # Round 4 (the editor's ED4-5, November 13, 2026): the line ends in words, and S91's variant leaves out the seats'
    # date its grade line prints (IM-2), so a rerun writes both as they stand.
    m['printed_source_line'] = (
        'Source: U.S. Code, 2024 edition, 28 U.S.C. 133, 134, 152, 631 and 633; Administrative Office of the U.S. Courts, '
        'Judicial Business 2025, seats as of September 30, 2025, United States. Retrieved November 12, 2026. Seats include '
        'vacant ones; the 677 district positions include four in the territorial courts.')
    m.setdefault('source_line_variants', {})['seats_date_in_grade'] = m['printed_source_line'].replace(
        ', seats as of September 30, 2025', '')
    for u in ('https://www.uscourts.gov/sites/default/files/2025-01/districtauth-with-endnotes.pdf',
              'https://www.uscourts.gov/sites/default/files/2025-01/districttemp.pdf'):
        if u not in m['url']:
            m['url'].append(u)
    note = ('Traced November 13, 2026 (ledger claim 28): 677 = 673 + 4. The Administrative Office’s "Additional Authorized '
            'Judgeships" table (January 2025) lists 104 district rows summing to 677; its 97 rows with seats equal, court '
            'by court, the 94 statute rows and 3 territorial rows of uscode-federal-courts-circuits-districts. Its '
            '"Authorized Temporary Judgeships" list shows the last ten temporary district judgeships (Alabama Northern, '
            'Arizona, California Central, Florida Southern, Hawaii, Kansas, Missouri Eastern, New Mexico, North Carolina '
            'Western, Texas Eastern) made permanent by Pub. L. 118-203, December 23, 2024. Judicial Business 2025, Table 10, '
            'gives 677 district positions for 2021 to 2025.')
    notes = [n for n in (m.get('notes') or []) if not n.startswith('The courts’ 677 district positions against')]
    m['notes'] = set_note(notes, 'Traced November 13, 2026 (ledger claim 28)', note)
    m2, end2 = read_meta_any(cm)
    m2['notes'] = set_note(list(m2.get('notes') or []), 'The courts count 677 district positions',
                           'The courts count 677 district positions on September 30, 2025 (Judicial Business 2025, Table '
                           '10): this file’s 673 statute judgeships and its 4 territorial ones, court by court as the '
                           'Administrative Office’s table of authorized district judgeships lists them (read November 13, '
                           '2026). uscode-federal-trial-judges prints the same account.')
    return [(tp, write_csv(out)), (tm, json.dumps(m, indent=1, ensure_ascii=False) + end),
            (cm, json.dumps(m2, indent=1, ensure_ascii=False) + end2)], '677 = 673 + 4 (GU 1, MP 1, VI 2)'


def rl4(dl, write):
    """RL-4: every line 21B row of both joint fundraising committees in the 2024 cycle, read for payees that are
    committees outside the file. dl holds the keyset pages, <committee>-NNNN.json, as the FEC API served them."""
    name = 'fec-jfc-transfers-2024'
    mp = OUT / f'{name}.meta.json'
    m = read_meta(mp)
    inside = {(r['jfc_id'], r['recipient_id']) for r in csv.DictReader(io.StringIO((OUT / f'{name}.csv').read_text(encoding='utf-8')))}
    found, total_rows = {}, {}
    for cid, want in (('C00873893', 6580), ('C00744946', 16472)):
        res, counts = [], set()
        for p in sorted(dl.glob(f'{cid}-*.json')):
            d = json.loads(p.read_text())
            res += d['results']
            counts.add(d['pagination']['count'])
        assert counts == {want} and len(res) == want and len({x['sub_id'] for x in res}) == want, (cid, len(res), counts)
        assert all(x['line_number'] == '21B' for x in res)
        total_rows[cid] = want
        com = [x for x in res if not x.get('memo_code') and (x.get('recipient_committee_id') or x.get('entity_type') in ('COM', 'PAC', 'PTY', 'CCM'))]
        assert all(x.get('recipient_committee_id') for x in com)
        by = collections.defaultdict(lambda: [0, 0.0, ''])
        for x in com:
            if (cid, x['recipient_committee_id']) in inside:
                continue
            b = by[x['recipient_committee_id']]
            b[0] += 1
            b[1] += x['disbursement_amount']
            b[2] = x['recipient_name']
        found[cid] = sorted(by.items(), key=lambda kv: -kv[1][1])
    assert not found['C00873893'] and len(found['C00744946']) == 7, found
    out = found['C00744946']
    tot = sum(v[1] for _, v in out)
    lst = '; '.join(f'{v[2]} ({k}), ${v[1]:,.2f} in {v[0]} {"payment" if v[0] == 1 else "payments"}' for k, v in out)
    note = (f'Line 21B to committees outside the file (RL-4, read November 13, 2026, every line 21B row of the cycle: '
            f'{total_rows["C00744946"]:,} for the Harris Victory Fund and {total_rows["C00873893"]:,} for the Trump National '
            f'Committee JFC). The Trump National Committee JFC paid no committee on line 21B. The Harris Victory Fund paid '
            f'seven committees outside the file ${tot:,.2f} on line 21B: {lst}. Two memo entries name the Biden Victory Fund '
            'and the Harris Victory Fund with no committee ID; memo entries are not payments. None of these committees is '
            'drawn, and none is in amount.')
    m['notes'] = set_note(list(m.get('notes') or []), 'Line 21B to committees outside the file', note)
    return [(mp, dump_meta(m))], f'Harris Victory Fund: 7 committees outside the file, ${tot:,.2f}; Trump JFC: none'


CMS_5C = 'Total beneficiaries whose coverage was terminated for a procedural or administrative reason'
CMS_5B = 'Total beneficiaries determined ineligible for Medicaid and CHIP based on the return of a renewal form'
CMS_HELD = ('States that held procedural terminations reflect these data in metric 5d as pending renewals along with '
            'renewals that were due but not completed by the end of the reporting period.')


def cms_proc(dl, write):
    """Maker B's RB3-R2: CMS's own words for a procedural termination (metric 5c), quoted into both renewal sidecars.
    dl holds updated.csv (CMS's file as published) and orig-meta.json (the CAA Reporting Metrics dataset's metadata)."""
    names = set()
    with open(dl / 'updated.csv', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            names.add(' '.join(r['Metric name '].split()))
    assert CMS_5C + ' (Metric 5c)' in names and CMS_5B + ' (Metric 5b)' in names, sorted(names)[:3]
    import re as _re
    desc = ' '.join(_re.sub(r'<[^>]+>', ' ', json.loads((dl / 'orig-meta.json').read_text())['description']).split())
    assert CMS_HELD in desc
    note = (f'Procedural reason, in CMS’s words (read November 13, 2026): its file names metric 5c “{CMS_5C}”, beside '
            f'metric 5b, “{CMS_5B}”. The description of CMS’s original renewal data (Medicaid and CHIP CAA Reporting '
            f'Metrics, data.medicaid.gov) adds: “{CMS_HELD}” The file, its data dictionary and both datasets’ '
            'descriptions give no examples of a procedural reason; CMS’s Data Sources and Metrics Definitions Overview, '
            'on medicaid.gov, refused this container (HTTP 403) and was not read.')
    out = []
    for n in ('cms-medicaid-chip-renewal-outcomes', 'cms-medicaid-chip-renewal-funnel'):
        mp = OUT / f'{n}.meta.json'
        m, end = read_meta_any(mp)
        m['notes'] = set_note(list(m.get('notes') or []), 'Procedural reason, in CMS’s words', note)
        u = 'https://data.medicaid.gov/api/1/metastore/schemas/dataset/items/ebcfc16f-8291-4c61-82a4-055846d72f3a'
        if u not in m['url']:
            m['url'].append(u)
        t = json.dumps(m, indent=1, ensure_ascii=False) + end
        assert '—' not in t and '‑' not in t
        out.append((mp, t))
    return out, 'metric 5c quoted in both sidecars'


def snap_expedited(dl, write):
    """RL-5 (for maker B's MB-7): who qualifies for expedited service, 7 CFR 273.2(i)(1), in the regulation's words.
    dl holds govinfo-2025.xml (the 2025 annual edition), ecfr-273-2.html (eCFR's renderer, current) and versions.json
    and titles.json (eCFR's versioner). The words come from govinfo and must equal eCFR's, word for word."""
    import html as _html
    import re as _re
    import xml.etree.ElementTree as _ET
    norm = lambda s: _re.sub(r'\s+', ' ', _re.sub(r'§\s*', '§ ', s)).strip()
    root = _ET.parse(dl / 'govinfo-2025.xml').getroot()
    paras = [' '.join(' '.join(p.itertext()).split()) for p in root.iter() if p.tag in ('P', 'FP')]
    j = next(k for k, p in enumerate(paras) if 'Entitlement to expedited service' in p)
    words = paras[j:j + 4]
    words[0] = words[0].split('—', 1)[1].strip()
    assert words[0].startswith('(1) Entitlement to expedited service.') and words[3].startswith('(iii) Households whose')
    ecfr = norm(_html.unescape(_re.sub(r'<[^>]+>', ' ', (dl / 'ecfr-273-2.html').read_text(encoding='utf-8'))))
    squeeze = lambda s: _re.sub(r'\s+', '', s)
    assert all(squeeze(w) in squeeze(ecfr) for w in words), 'eCFR and govinfo differ'  # word for word, spacing aside
    last = max(v['date'] for v in json.loads((dl / 'versions.json').read_text())['content_versions'])
    t7 = [t for t in json.loads((dl / 'titles.json').read_text())['titles'] if t['number'] == 7][0]
    assert last == '2020-07-14' and t7['up_to_date_as_of'] == '2026-11-10', (last, t7['up_to_date_as_of'])
    quote = ' '.join(norm(w) for w in words)
    note = ('Who qualifies for expedited service, 7 CFR 273.2(i)(1), in the regulation’s words (RL-5; read November 13, '
            '2026 on eCFR, title 7 up to date as of November 10, 2026, and in the 2025 annual edition on govinfo, the same '
            'word for word; the section was last amended July 14, 2020, so the November 9 reading this file froze holds): '
            f'“{quote}”')
    mp = OUT / 'govinfo-snap-application-steps.meta.json'
    m, end = read_meta_any(mp)
    m['notes'] = set_note(list(m.get('notes') or []), 'Who qualifies for expedited service, 7 CFR 273.2(i)(1)', note)
    for u in ('https://www.ecfr.gov/api/versioner/v1/versions/title-7.json?part=273&section=273.2',):
        if u not in m['url']:
            m['url'].append(u)
    t = json.dumps(m, indent=1, ensure_ascii=False) + end
    assert '—' not in t and '‑' not in t
    return [(mp, t)], 'three tests quoted: under $150 income with $100 or less in liquid resources; destitute farmworkers with $100 or less; income and resources below rent or mortgage and utilities'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('item', choices=['rl1', 'rl2', 'rl3', 'judges', 'rl4', 'cms_proc', 'snap_expedited'])
    ap.add_argument('--dl', required=True)
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    files, summary = {'rl1': rl1, 'rl2': rl2, 'rl3': rl3, 'judges': judges, 'rl4': rl4,
                      'cms_proc': cms_proc, 'snap_expedited': snap_expedited}[a.item](Path(a.dl), a.write)
    for p, text in files:
        print(f'{p.name}: {put(p, text, a.write)}')
    print(f'{a.item}: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
