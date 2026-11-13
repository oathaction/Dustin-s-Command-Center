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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('item', choices=['rl1', 'rl2', 'rl3'])
    ap.add_argument('--dl', required=True)
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    files, summary = {'rl1': rl1, 'rl2': rl2, 'rl3': rl3}[a.item](Path(a.dl), a.write)
    for p, text in files:
        print(f'{p.name}: {put(p, text, a.write)}')
    print(f'{a.item}: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
