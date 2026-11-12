"""The research lead's review fix pass for Phase 3, round 1 (fix brief 20261112_Round-1-Fix-Brief.md, calls D3-476 to D3-488).

Usage:
    python3 -I work/build/scripts/phase-3/research_review_fix_round1.py <item> [<item> ...] [--dl <folder>]

Items, in the order the brief sets:
    s24      ST M1: the frozen Business Formation Statistics files print their release (D3-476); figures unchanged
    s34      ST M3: the 119th Congress row of the cloture counts, recounted from the Senate's vote menus (needs --dl)
    s31      ST S1 and ST S3: the unemployment file prints its vintage and gains the with_margin variant
    s27      ST S2 and ST S3: the FHFA file prints its release; the United States purchase-only series (needs --dl)
    vintages ST S3: OPM (S25) and FEC (S36) print their vintages
    s11      ST S11: S20's two-file line as a variant
    ax_s1    AX S1: span templates for multi-year files
    bc_m3    BC M3: the FEC's party for the three party committees (needs --dl)
    bc_s20   BC S20: OPM's January 2025 count for S25's agencies (needs --dl)

Each item sets values (it never appends twice), so a rerun writes the same files. Sidecars keep their format: JSON with a
one-space indent, characters as written, and the trailing newline the file had. Frozen figures never change under D3-476;
only S34's 119th row, a count the Senate's own record does not support, is corrected (ST M3). Downloads are read from the
folder given with --dl, never from this script's folder.
"""
import csv
import hashlib
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATA = ROOT / 'work/build/data'


def load(name):
    p = DATA / f'{name}.meta.json'
    raw = p.read_text(encoding='utf-8')
    return json.loads(raw), raw.endswith('\n')


def save(name, meta, newline):
    p = DATA / f'{name}.meta.json'
    text = json.dumps(meta, indent=1, ensure_ascii=False) + ('\n' if newline else '')
    if p.read_text(encoding='utf-8') != text:
        p.write_text(text, encoding='utf-8')
        print(f'wrote {p.relative_to(ROOT)}')
    else:
        print(f'unchanged {p.relative_to(ROOT)}')


def set_note(meta, key, text):
    """Keep one note per key: a note starting with the key's words is replaced, else added."""
    notes = [n for n in meta.get('notes', []) if not n.startswith(key)]
    notes.append(text)
    meta['notes'] = notes


def sha_prefix(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]


# ---------------------------------------------------------------------------------------------------------------
# s24: ST M1. The frozen BFS files name their release. The figures stay (D3-476); the November 12 release goes to
# the Phase 5 refresh list in the research ledger's Part 7.
# ---------------------------------------------------------------------------------------------------------------
BFS_RELEASE = 'September 2026 monthly release (October 14, 2026)'
BFS_VINTAGE = ('Business Formation Statistics, September 2026 monthly release, posted October 14, 2026 and retrieved November 11, 2026. '
               'The October 2026 monthly release of November 12, 2026 applied the Bureau’s annual update and revised 2022 to 2025; '
               'this file keeps the September release until the Phase 5 refresh')
BFS_NOTE_KEY = 'Release confirmed November 12, 2026'
BFS_NOTE = (f'{BFS_NOTE_KEY} from the Bureau’s own pages: the BFS release schedule (https://www.census.gov/econ/bfs/release_schedule.html) '
            'lists the September 2026 report on Wednesday, October 14, 2026 and the October 2026 report on Thursday, November 12, 2026, '
            'and the BFS page (https://www.census.gov/econ/bfs/index.html) reads "The latest annual update was applied during the October 2026 '
            'monthly release on November 12, 2026." The file this one was summed from was retrieved November 11, between the two. '
            'The November 12 file (last-modified Thu, 12 Nov 2026 15:00:14 GMT; SHA-256 prefix 47975a1c7bca0aad), summed the same way, '
            'matches this file in every row for 2005 to 2021 and differs for 2022 to 2025: the 2025 United States total is 5,696,742 there '
            'against 5,671,836 here, a rise from 2019 of 62.8 percent against 62.1, and Wyoming has 81,688 against 79,023. '
            'The frozen figures stay until the Phase 5 refresh (research ledger, Part 7, "Phase 5 refresh list").')
BFS_TAIL = ('business applications, {span}, 50 states and DC. Retrieved November 11, 2026. Applications for a tax ID that signal a new business; '
            'many never hire; annual totals summed by Oath & Action.')


def bfs_line(span):
    return f'Source: U.S. Census Bureau, Business Formation Statistics, {BFS_RELEASE}, ' + BFS_TAIL.format(span=span)


def item_s24(dl):
    for name in ('census-bfs-business-applications-by-state', 'census-bfs-business-applications-change-by-state'):
        meta, nl = load(name)
        meta['vintage'] = BFS_VINTAGE
        meta['printed_source_line'] = bfs_line('2019 and 2025')
        if name == 'census-bfs-business-applications-by-state':
            meta.setdefault('source_line_variants', {})['all_years'] = bfs_line('2005 to 2025')
        set_note(meta, BFS_NOTE_KEY, BFS_NOTE)
        save(name, meta, nl)


# ---------------------------------------------------------------------------------------------------------------
# s34: ST M3. The 119th Congress row. The frozen row (294 motions, 294 votes, 247 invoked) does not match the Senate's
# roll call record. Recount: every vote in vote_menu_119_1.xml and _2.xml whose question names cloture, plus the votes
# the menus list with an empty question, each read from its own record (vote_119_<s>_<n>.xml) and counted when its
# question is "On the Cloture Motion". The recount must equal the cloture counts page's row, or nothing is written.
# --dl holds vote_menu_119_1.xml, vote_menu_119_2.xml, clotureCounts.htm and votes/vote_119_*.xml.
# ---------------------------------------------------------------------------------------------------------------
CLOTURE = 'senate-cloture-motions-by-congress'
CLOTURE_NOTE_KEY = 'The 119th Congress row, corrected November 12, 2026'


def recount_119(dl):
    import xml.etree.ElementTree as ET
    votes, invoked, empty, last = 0, 0, [], None
    for s in (1, 2):
        root = ET.parse(dl / f'vote_menu_119_{s}.xml').getroot()
        for v in root.iter('vote'):
            q = (v.findtext('question') or '').strip()
            n = int((v.findtext('vote_number') or '0').strip())
            if last is None or (s, n) > last[:2]:
                last = (s, n, (v.findtext('vote_date') or '').strip())
            if not q:
                empty.append((s, n))
            elif 'cloture' in q.lower():
                votes += 1
                invoked += (v.findtext('result') or '').strip().lower() == 'agreed to'
    found = []
    for s, n in empty:
        r = ET.parse(dl / 'votes' / f'vote_119_{s}_{n:05d}.xml').getroot()
        q = (r.findtext('question') or '').strip()
        res = (r.findtext('vote_result') or '').strip()
        if q == 'On the Cloture Motion':
            votes += 1
            invoked += res == 'Cloture Motion Agreed to'
            found.append(f'{s}-{n} {res.lower()}')
    return votes, invoked, empty, found, last


def page_row(dl, congress):
    import html
    import re
    t = (dl / 'clotureCounts.htm').read_text(encoding='utf-8', errors='replace')
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        c = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip() for x in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)]
        if c and c[0] == str(congress):
            return int(c[2].replace(',', '')), int(c[3].replace(',', '')), int(c[4].replace(',', ''))
    raise SystemExit(f'no row for the {congress}th Congress on the page')


def item_s34(dl):
    if dl is None:
        raise SystemExit('s34 needs --dl <folder with the vote menus, vote records and clotureCounts.htm>')
    votes, invoked, empty, found, last = recount_119(dl)
    motions, p_votes, p_invoked = page_row(dl, 119)
    print(f'recount: {votes} votes, {invoked} invoked; page: {motions} motions, {p_votes} votes, {p_invoked} invoked; '
          f'{len(empty)} menu votes with no question, cloture among them: {", ".join(found)}; latest vote {last}')
    if (votes, invoked) != (p_votes, p_invoked):
        raise SystemExit('the recount and the page differ; nothing written')
    p = DATA / f'{CLOTURE}.csv'
    raw = p.read_text(encoding='utf-8')
    rows = list(csv.reader(io.StringIO(raw)))
    head = rows[0]
    for r in rows[1:]:
        if r[0] == '119':
            r[head.index('motions_filed')] = str(motions)
            r[head.index('votes_on_cloture')] = str(votes)
            r[head.index('cloture_invoked')] = str(invoked)
    out = io.StringIO()
    csv.writer(out, lineterminator='\n').writerows(rows)
    if out.getvalue() != raw:
        p.write_text(out.getvalue(), encoding='utf-8')
        print(f'wrote {p.relative_to(ROOT)}')
    meta, nl = load(CLOTURE)
    meta['observation_period'] = ('65th Congress (1917 to 1918) to the 119th Congress (2025 to 2026), through November 10, 2026, '
                                  'the date of the Senate’s latest roll call vote when the page was read')
    meta['date_retrieved'] = '2026-11-12'
    meta['vintage'] = ('Page as read on November 12, 2026, every row; first read November 11, 2026, when the 119th Congress row was '
                       'frozen as 294 motions, 294 votes and 247 invoked')
    meta['qualification'] = ('Counts mix bills and nominations, and the vote needed changed over time (two-thirds of those voting until 1975, '
                             'then three-fifths of senators for most matters; a simple majority for nominations since 2013 and 2017). '
                             'The 119th Congress is still in session; its row counts votes through November 10, 2026')
    meta['printed_source_line'] = ('Source: United States Senate, Senate Action on Cloture Motions, 65th Congress (1917) to the 119th Congress '
                                   'through November 10, 2026, United States Senate. Retrieved November 12, 2026. Counts include bills and '
                                   'nominations; the votes needed changed in 1975, 2013 and 2017.')
    meta['url'] = ['https://www.senate.gov/legislative/cloture/clotureCounts.htm',
                   'https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_119_1.xml',
                   'https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_119_2.xml']
    set_note(meta, CLOTURE_NOTE_KEY,
             f'{CLOTURE_NOTE_KEY} (statistics review M3). The page read that day gives the 119th Congress {motions} motions filed, '
             f'{votes} votes on cloture and {invoked} times invoked, and every other row equals the file. The Senate’s own vote lists give '
             f'the same {votes} and {invoked}: {votes - len(found)} votes whose question names cloture in vote_menu_119_1.xml and '
             f'vote_menu_119_2.xml, plus {len(found)} the lists show with no question, each read from its own record as "On the Cloture '
             f'Motion" (session and vote: {", ".join(found)}). The latest roll call vote was number {last[1]} of the second session, '
             f'November 10, 2026. The row frozen November 11 (294, 294 and 247) matched neither; the round 0 download is gone, so the '
             'cause was not found. Motions filed come from the page only; the vote lists do not record a motion until it is voted on.')
    set_note(meta, 'On September 17, 2025',
             'On September 17, 2025, cloture on a group of nominations considered together failed 51 to 48 under a three-fifths requirement '
             '(vote 522 of the first session); the Senate then voted 47 to 52 not to sustain the chair (vote 524) and invoked cloture on the '
             'same group 52 to 47 with a majority requirement of one-half (vote 525). Read from each vote’s record on senate.gov, '
             'November 12, 2026. A chart that names the changes in the votes needed may add this one.')
    save(CLOTURE, meta, nl)


# ---------------------------------------------------------------------------------------------------------------
# s31: ST S1 and ST S3. The unemployment file names its releases, and gains with_margin from the Bureau's technical
# note (read through the session's web-fetch tool, as P7-042 was, since bls.gov refuses this container's reader).
# The unemployment_rate_only variant S31 prints now carries the release too, so no line without it stays valid.
# ---------------------------------------------------------------------------------------------------------------
UNEMP = 'fred-unemployment-and-job-openings'
ES_REL = 'Employment Situation for October 2026 (November 6, 2026)'
UNEMP_ONLY = (f'Source: U.S. Bureau of Labor Statistics, Current Population Survey, {ES_REL}, unemployment rate, seasonally adjusted, '
              'January 2022 to October 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 11, 2026. '
              'No rate was published for October 2025.')
UNEMP_MARGIN = (UNEMP_ONLY + ' The margin of error is the Bureau’s 90 percent interval for a month’s change in the rate, plus or minus '
                '0.3 point at a rate near 6 percent, from the same release’s technical note.')
BOTH_REL = 'releases for October 2026 (November 6, 2026) and September 2026 (November 3, 2026)'


def both_line(span):
    return ('Source: U.S. Bureau of Labor Statistics, Current Population Survey and Job Openings and Labor Turnover Survey, '
            f'{BOTH_REL}, unemployment rate and job openings, seasonally adjusted, {span}, United States, via FRED, Federal Reserve Bank '
            'of St. Louis. Retrieved November 11, 2026. No unemployment rate was published for October 2025; recent months are preliminary '
            'and will be revised.')


def item_s31(dl):
    meta, nl = load(UNEMP)
    base = meta['vintage'].split('. The unemployment rate comes from')[0]
    meta['vintage'] = (base + '. The unemployment rate comes from the Bureau’s Employment Situation for October 2026, released November 6, '
                       '2026, and job openings from its Job Openings and Labor Turnover Survey for September 2026, released November 3, 2026')
    meta['printed_source_line'] = both_line('January 2022 to October 2026')
    v = meta.setdefault('source_line_variants', {})
    v['connected_scatter'] = both_line('December 2000 to September 2026')
    v['unemployment_rate_only'] = UNEMP_ONLY
    v['with_margin'] = UNEMP_MARGIN
    set_note(meta, 'Margin of error, read November 12, 2026',
             'Margin of error, read November 12, 2026 from the Bureau’s "Employment Situation Technical Note - 2026 M10 Results" '
             '(https://www.bls.gov/news.release/empsit.tn.htm, "Last Modified Date: November 06, 2026") through the session’s web-fetch tool, '
             'which returns quotes of at most 125 characters; two reads gave the same words: "At an unemployment rate of around 6.0 percent, '
             'the 90-percent confidence interval for the monthly change in unemployment" "as measured by the household survey is about '
             '+/- 425,000," "and for the monthly change in the unemployment rate it is about +/- 0.3 percentage point." The note gives no '
             'interval for a change over more than one month and none for a level. The rise from 3.4 percent in April 2023 to 4.5 percent '
             'in November 2025 is 1.1 points, more than three times the monthly interval; the Bureau publishes no interval for a 31-month '
             'change to test it against directly.')
    set_note(meta, 'Releases confirmed November 12, 2026',
             'Releases confirmed November 12, 2026: the technical note above is titled "2026 M10 Results", last modified November 6, 2026; '
             'the JOLTS news release (https://www.bls.gov/news.release/jolts.nr0.htm) reads "For release 10:00 a.m. (ET) Tuesday, November 3, '
             '2026" and covers September 2026, with "The number of job openings was little changed at 7.5 million in September"; this file '
             'holds 7,523 thousand for September 2026 and 4.1 percent for October 2026.')
    save(UNEMP, meta, nl)


# ---------------------------------------------------------------------------------------------------------------
# s27: ST S2 and ST S3, with the data lead's ruling (d). The nation's purchase-only index, quarterly, seasonally adjusted
# and not, first quarter 1991 = 100, from the release the state rows come from (August 25, 2026, through 2026Q2), joins
# the state file as code US, first, as the BFS files carry the nation. The state rows do not change. --dl holds
# hpi_po_us_and_census.txt and hpi_po_state.txt as fetched November 12, 2026; the state file must equal the frozen
# rows in every value, or nothing is written.
# ---------------------------------------------------------------------------------------------------------------
FHFA = 'fhfa-house-price-index-by-state'
FHFA_REL = 'quarterly release of August 25, 2026'


def fhfa_num(x):
    return ('%.2f' % float(x)).rstrip('0').rstrip('.')


def fhfa_line(geo, retrieved):
    return (f'Source: Federal Housing Finance Agency, House Price Index, purchase-only, {FHFA_REL}, seasonally adjusted, first quarter 1991 '
            f'to second quarter 2026, {geo}. Retrieved {retrieved}. Repeat sales of homes with Fannie Mae or Freddie Mac mortgages; '
            'an index of change since 1991, not a price.')


def item_s27(dl):
    if dl is None:
        raise SystemExit('s27 needs --dl <folder with hpi_po_us_and_census.txt and hpi_po_state.txt>')
    p = DATA / f'{FHFA}.csv'
    raw = p.read_text(encoding='utf-8')
    rows = list(csv.DictReader(io.StringIO(raw)))
    head = list(rows[0].keys())
    states = [r for r in rows if r['code'] != 'US']
    # the state file today equals the frozen rows: the same release
    today = {}
    for line in (dl / 'hpi_po_state.txt').read_text(encoding='utf-8').splitlines()[1:]:
        c = line.split('\t')
        if len(c) >= 5:
            today[(c[0], c[1], c[2])] = (fhfa_num(c[4]), fhfa_num(c[3]))
    same = sum(today.get((r['code'], r['year'], r['quarter'])) == (r['index_sa'], r['index_nsa']) for r in states)
    if same != len(states) or len(today) != len(states):
        raise SystemExit(f'the state file differs from the frozen rows ({same} of {len(states)} equal); nothing written')
    us = []
    lines = (dl / 'hpi_po_us_and_census.txt').read_text(encoding='utf-8').splitlines()
    if lines[0].split('\t') != ['division', 'year', 'qtr', 'index_po_not_seasonally_adjusted', 'index_po_seasonally_adjusted']:
        raise SystemExit('the national file has other columns; nothing written')
    for line in lines[1:]:
        c = line.split('\t')
        if c[0] == 'USA':
            us.append({'code': 'US', 'name': 'United States', 'year': c[1], 'quarter': c[2], 'index_sa': fhfa_num(c[4]),
                       'index_nsa': fhfa_num(c[3]), 'small_sample': 'false'})
    by_q = {(r['year'], r['quarter']): float(r['index_sa']) for r in us}
    assert by_q[('1991', '1')] == 100 and len(us) == 142 and ('2026', '2') in by_q and ('2026', '3') not in by_q
    qoq = 100 * (by_q[('2026', '2')] / by_q[('2026', '1')] - 1)
    yoy = 100 * (by_q[('2026', '2')] / by_q[('2025', '2')] - 1)
    print(f'United States, seasonally adjusted: 2026Q2 {by_q[("2026", "2")]}, {qoq:.2f} percent on the quarter, {yoy:.2f} on the year')
    assert round(qoq, 1) == 0.3 and round(yoy, 1) == 2.1, 'the release of August 25, 2026 reads up 0.3 on the quarter and 2.1 on the year'
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=head, lineterminator='\n')
    w.writeheader()
    w.writerows(us + states)
    if out.getvalue() != raw:
        p.write_text(out.getvalue(), encoding='utf-8')
        print(f'wrote {p.relative_to(ROOT)}')
    meta, nl = load(FHFA)
    meta['title_or_table'] = ('FHFA House Price Index, purchase-only indexes, quarterly: states (hpi_po_state) and the United States '
                              '(hpi_po_us_and_census, division USA)')
    meta['table_id'] = 'HPI purchase-only, state and U.S., quarterly'
    meta['url'] = ['https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_state.csv',
                   'https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_us_and_census.txt',
                   'https://www.fhfa.gov/data/hpi/datasets']
    meta['geography'] = '50 states and DC, with a United States row (code US)'
    meta['vintage'] = ('FHFA’s quarterly release of August 25, 2026, through the second quarter of 2026: the state rows as retrieved November 11, '
                       '2026, and the United States rows from the same release’s U.S. and census division file, retrieved November 12, 2026, '
                       'when the state file still equaled the frozen rows in all 7,242 values. FHFA revises earlier quarters each release; '
                       'its next quarterly release is due Tuesday, November 24, 2026')
    cols = meta['columns']
    cols['code']['description'] = 'USPS state code, or US for the nation'
    cols['name']['description'] = 'state name, or United States'
    cols['small_sample']['description'] = 'FHFA note: fewer than 15,000 transactions in ten years; false for the nation'
    meta['printed_source_line'] = fhfa_line('50 states, DC and the United States', 'November 11 and 12, 2026')
    meta.setdefault('source_line_variants', {})['states_and_dc'] = fhfa_line('50 states and DC', 'November 11, 2026')
    set_note(meta, 'The United States rows (code US)',
             'The United States rows (code US) were added November 12, 2026 for S27’s national line (statistics review S2, the data '
             'lead’s ruling (d)): division USA of hpi_po_us_and_census.txt (SHA-256 prefix 4776cd3261d1a5ba), the same purchase-only index, '
             'quarterly, first quarter 1991 = 100, seasonally adjusted and not, 142 quarters. FHFA’s news release of August 25, 2026, '
             '"U.S. House Prices Rise 2.1 Percent Year over Year; Up 0.3 percent Quarter over Quarter" (read through the session’s '
             f'web-fetch tool), matches these rows: {qoq:.2f} percent on the quarter and {yoy:.2f} on the year, seasonally adjusted. '
             'The state rows are unchanged. A chart of the states alone filters code US out and prints the states_and_dc line.')
    save(FHFA, meta, nl)


# ---------------------------------------------------------------------------------------------------------------
# bc_m3: BC M3, with ST S3 for S36. Each committee's party as its FEC committee record lists it (api.open.fec.gov
# /v1/committee/<id>/, read November 12, 2026), for all 25 rows: the three party committees and one hybrid PAC carry
# one. The totals do not change. The printed line names the processing date the totals stand on (the vintage) and the
# committee records. --dl holds committee-<id>.json for each row.
# ---------------------------------------------------------------------------------------------------------------
FEC_IE = 'fec-independent-expenditures-2024'
PARTY_WORDS = {'DEMOCRATIC PARTY': 'Democratic', 'REPUBLICAN PARTY': 'Republican'}


def item_bc_m3(dl):
    if dl is None:
        raise SystemExit('bc_m3 needs --dl <folder with committee-<id>.json>')
    p = DATA / f'{FEC_IE}.csv'
    raw = p.read_text(encoding='utf-8')
    rows = list(csv.DictReader(io.StringIO(raw)))
    head = [h for h in rows[0].keys() if h not in ('party', 'party_full', 'party_words')]
    i = head.index('committee_type_words') + 1
    head = head[:i] + ['party', 'party_full', 'party_words'] + head[i:]
    named, renamed = [], []
    for r in rows:
        rec = json.loads((dl / f'committee-{r["committee_id"]}.json').read_text(encoding='utf-8'))['results'][0]
        if rec['committee_id'] != r['committee_id']:
            raise SystemExit(f'{r["committee_id"]}: the record is {rec["committee_id"]}; nothing written')
        if rec['name'] != r['committee_name']:
            renamed.append(f'{r["committee_name"]} ({r["committee_id"]}) now reads {rec["name"]}')
        full = rec.get('party_full') or ''
        if full and full not in PARTY_WORDS:
            raise SystemExit(f'{r["committee_id"]}: party {full} has no reader word; nothing written')
        r['party'], r['party_full'], r['party_words'] = rec.get('party') or '', full, PARTY_WORDS.get(full, '')
        if full:
            named.append(f'{r["committee_name"]} ({r["committee_type_words"]}, {PARTY_WORDS[full]})')
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=head, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    if out.getvalue() != raw:
        p.write_text(out.getvalue(), encoding='utf-8')
        print(f'wrote {p.relative_to(ROOT)}')
    print('party listed:', '; '.join(named))
    meta, nl = load(FEC_IE)
    cols = meta['columns']
    new_cols = {}
    for k, v in cols.items():
        if k in ('party', 'party_full', 'party_words'):
            continue
        new_cols[k] = v
        if k == 'committee_type_words':
            new_cols['party'] = {'type': 'category', 'description': 'the party affiliation the FEC records for the committee, as its code (DEM, REP); empty where the record names none, as for most PACs'}
            new_cols['party_full'] = {'type': 'text', 'description': 'the party affiliation the FEC records for the committee, as the record spells it'}
            new_cols['party_words'] = {'type': 'category', 'description': 'the recorded party affiliation in a reader’s word (Democratic, Republican); empty where the record names none'}
    meta['columns'] = new_cols
    meta['url'] = ['https://api.open.fec.gov/v1/totals/pac-party/?cycle=2024&sort=-independent_expenditures&per_page=40',
                   'https://api.open.fec.gov/v1/committee/<committee_id>/']
    meta['vintage'] = ('FEC processed data as served on November 11, 2026: the totals stand on the reports and amendments the commission had '
                       'processed by then, every committee’s covering through December 31, 2024; a later amendment can change a total. '
                       'Parties from the committee records as served November 12, 2026')
    meta['qualification'] = ('Independent expenditures are spending for or against candidates made without coordinating with them; the totals '
                             'count spending for and against together and leave out groups that are not political committees (filers of Form 5, '
                             'such as some nonprofits). Money moved between committees is counted where it was spent. The party columns hold the '
                             'party affiliation the commission records for each committee, filled wherever its record names one: the three '
                             'party committees and one hybrid PAC, SFA Fund, Inc.; most PACs record none, and 21 of the 22 here record none')
    meta['printed_source_line'] = ('Source: Federal Election Commission, financial totals for PACs and party committees, independent expenditures, '
                                   '2023 to 2024 cycle, from reports the commission had processed by November 11, 2026, with each party committee’s '
                                   'party from its committee record, United States. Retrieved November 11 and 12, 2026. Spending for and against '
                                   'candidates together; groups that are not political committees are not included.')
    set_note(meta, 'Parties read November 12, 2026',
             'Parties read November 12, 2026 from each of the 25 committees’ records (api.open.fec.gov/v1/committee/<id>/, key injected by the '
             f'network proxy; fetch log in the research lead’s scratch folder). Records that list a party: {"; ".join(named)}. The three party '
             'committees’ records also give party type NATIONAL. SFA Fund, Inc. (C00828061) is a hybrid PAC whose record lists '
             '"REPUBLICAN PARTY" with no party type; its filing frequency reads T. A chart that says the commission records no party for a PAC '
             'is wrong for this one. The file keeps each name as the 2024 totals list it; four records carry a newer name: '
             f'{"; ".join(renamed)}.')
    save(FEC_IE, meta, nl)


# ---------------------------------------------------------------------------------------------------------------
# bc_s20: BC S20, with ST S3 for S25. OPM's January 2025 status file (version 4, published October 3, 2026, the same
# round as January 2022's), summed by department code from the record-level count field, as the frozen columns were.
# The sums of the January 2022 and August 2026 files must reproduce the frozen columns in all 130 rows, or nothing is
# written. --dl holds employment_202201_4.parquet, employment_202501_4.parquet and employment_202608_1.parquet; reading
# them needs pyarrow, so this item runs under a Python that has it (the research lead's scratch environment).
# ---------------------------------------------------------------------------------------------------------------
OPM = 'opm-federal-employment-by-agency'
OPM_FILES = {'2022_01': 'employment_202201_4', '2025_01': 'employment_202501_4', '2026_08': 'employment_202608_1'}


def opm_sums(path):
    import collections
    import pyarrow.parquet as pq
    t = pq.read_table(path, columns=['department_code', 'count'])
    sums = collections.Counter()
    for c, k in zip(t.column('department_code').to_pylist(), t.column('count').to_pylist()):
        sums[c] += int(k)
    return sums


def opm_line(files, retrieved, days):
    return (f'Source: U.S. Office of Personnel Management, Federal Workforce Data, employment status files, {files}, federal civilian '
            f'workforce. Retrieved {retrieved}. People on the rolls on {days}; some agencies, including intelligence agencies and the '
            'Postal Service, are not in the files.')


def item_bc_s20(dl):
    if dl is None:
        raise SystemExit('bc_s20 needs --dl <folder with the three parquet files>')
    sums = {k: opm_sums(dl / f'{v}.parquet') for k, v in OPM_FILES.items()}
    shas = {f'{v}.parquet': sha_prefix(dl / f'{v}.parquet') for v in OPM_FILES.values()}
    p = DATA / f'{OPM}.csv'
    raw = p.read_text(encoding='utf-8')
    rows = list(csv.DictReader(io.StringIO(raw)))
    meta, nl = load(OPM)
    for name, prefix in meta['raw_files_sha256_prefix'].items():
        if shas.get(name) != prefix:
            raise SystemExit(f'{name} is not the frozen file; nothing written')
    for r in rows:
        for when, col in (('2022_01', 'employees_2022_01'), ('2026_08', 'employees_2026_08')):
            got = sum(sums[when].values()) if r['department_code'] == 'ALL' else sums[when].get(r['department_code'], 0)
            if got != int(r[col]):
                raise SystemExit(f'{r["department_code"]} {col}: {got} against {r[col]}; nothing written')
    known = {r['department_code'] for r in rows}
    unrowed = {k: v for k, v in sums['2025_01'].items() if k not in known}
    for r in rows:
        a = sum(sums['2025_01'].values()) if r['department_code'] == 'ALL' else sums['2025_01'].get(r['department_code'], 0)
        r['employees_2025_01'] = str(a)
        r['change_2022_01_to_2025_01'] = str(a - int(r['employees_2022_01']))
        r['change_2025_01_to_2026_08'] = str(int(r['employees_2026_08']) - a)
    old = [h for h in rows[0].keys() if h not in ('employees_2025_01', 'change_2022_01_to_2025_01', 'change_2025_01_to_2026_08')]
    i = old.index('employees_2022_01') + 1
    head = old[:i] + ['employees_2025_01'] + old[i:] + ['change_2022_01_to_2025_01', 'change_2025_01_to_2026_08']
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=head, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    if out.getvalue() != raw:
        p.write_text(out.getvalue(), encoding='utf-8')
        print(f'wrote {p.relative_to(ROOT)}')
    all_row = next(r for r in rows if r['department_code'] == 'ALL')
    print('all agencies:', all_row['employees_2022_01'], all_row['employees_2025_01'], all_row['employees_2026_08'], 'unrowed', unrowed)
    cols = {}
    for k, v in meta['columns'].items():
        if k in ('employees_2025_01', 'change_2022_01_to_2025_01', 'change_2025_01_to_2026_08'):
            continue
        cols[k] = v
        if k == 'employees_2022_01':
            cols['employees_2025_01'] = {'type': 'integer', 'description': 'employees, January 31, 2025', 'unit': 'people'}
    cols['change_2022_01_to_2025_01'] = {'type': 'integer', 'description': 'change from January 31, 2022 to January 31, 2025, computed', 'unit': 'people'}
    cols['change_2025_01_to_2026_08'] = {'type': 'integer', 'description': 'change from January 31, 2025 to August 31, 2026, computed', 'unit': 'people'}
    meta['columns'] = cols
    meta['title_or_table'] = ('Federal Workforce Data, Federal Employment Raw Data (EHRI status files), January 2022 (version 4), January 2025 '
                              '(version 4) and August 2026 (version 1), employees counted by department or independent agency')
    meta['table_id'] = 'data.opm.gov employment files employment_202201_4, employment_202501_4 and employment_202608_1'
    meta['url'] = ['https://data.opm.gov/api/v1/files/employment/2022/01/4/download', 'https://data.opm.gov/api/v1/files/employment/2025/01/4/download',
                   'https://data.opm.gov/api/v1/files/employment/2026/08/1/download', 'https://data.opm.gov/get-data/data-downloads']
    meta['vintage'] = ('January 2022 version 4 (published October 3, 2026), January 2025 version 4 (published October 3, 2026) and August 2026 '
                       'version 1 (published October 4, 2026), each the current version when read; OPM may publish later versions')
    meta['raw_files_sha256_prefix'] = shas
    meta['printed_source_line'] = opm_line('January 2022 (version 4, October 3, 2026) and August 2026 (version 1, October 4, 2026)',
                                           'November 11, 2026', 'one day')
    meta.setdefault('source_line_variants', {})['with_january_2025'] = opm_line(
        'January 2022 and January 2025 (version 4 of each, October 3, 2026) and August 2026 (version 1, October 4, 2026)',
        'November 11 and 12, 2026', 'the last day of each month')
    named = ', '.join(f'{k} ({v} employees)' for k, v in sorted(unrowed.items()))
    set_note(meta, 'January 2025 column (brand review S20)',
             'January 2025 column (brand review S20), added November 12, 2026 from employment_202501_4, version 4, published October 3, 2026 '
             '(OPM’s file list at https://data.opm.gov/api/v1/files/employment marks it current), summed by department code from the count '
             f'field, the method that reproduces the January 2022 and August 2026 columns in all 130 rows. All agencies: {int(all_row["employees_2022_01"]):,} '
             f'on January 31, 2022, {int(all_row["employees_2025_01"]):,} on January 31, 2025 and {int(all_row["employees_2026_08"]):,} on August 31, 2026. '
             f'The January 2025 total includes {sum(unrowed.values())} people under codes with no row here: {named}; '
             'OP is the Office of Pandemic Preparedness and Response Policy, as the file names it, and "No Data Reported" is OPM’s own code. January 31, 2025 is the file’s day, eleven days after the inauguration of January 20, 2025, '
             'so changes made in those eleven days fall in the first span. OPM also publishes December 2024 (version 4, October 3, 2026), '
             'not read here.')
    save(OPM, meta, nl)


# ---------------------------------------------------------------------------------------------------------------
# ed_r1: the editor's ED-R1 (BC M2, Rule 14.6's plate from the kit's ranked-bar). Active judges counted by court of
# appeals from the frozen FJC file, a derived table. Reads only work/build/data/.
# ---------------------------------------------------------------------------------------------------------------
FJC = 'fjc-article-iii-judges'
FJC_COA = 'fjc-active-judges-by-court-of-appeals'
CIRCUITS = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth', 'Eleventh']


def coa_short(name):
    tail = name.replace('U.S. Court of Appeals for the ', '')
    if tail == 'District of Columbia Circuit':
        return 'D.C. Circuit', 11
    if tail == 'Federal Circuit':
        return 'Federal Circuit', 12
    word = tail.replace(' Circuit', '')
    return f'{word} Circuit', CIRCUITS.index(word)


def item_ed_r1(dl):
    import collections
    rows = list(csv.DictReader(io.StringIO((DATA / f'{FJC}.csv').read_text(encoding='utf-8'))))
    n = collections.Counter(r['court_name'] for r in rows if r['court_type'] == 'U.S. Court of Appeals')
    assert len(n) == 13 and sum(n.values()) == 179 and n['U.S. Court of Appeals for the Ninth Circuit'] == 29
    out_rows = []
    for court, judges in n.items():
        short, order = coa_short(court)
        out_rows.append({'court': court, 'short_name': short, 'circuit_order': order + 1, 'judges': judges})
    out_rows.sort(key=lambda r: (-r['judges'], r['circuit_order']))
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=['court', 'short_name', 'circuit_order', 'judges'], lineterminator='\n')
    w.writeheader()
    w.writerows(out_rows)
    p = DATA / f'{FJC_COA}.csv'
    if not p.exists() or p.read_text(encoding='utf-8') != out.getvalue():
        p.write_text(out.getvalue(), encoding='utf-8')
        print(f'wrote {p.relative_to(ROOT)}')
    src, _ = load(FJC)
    meta = {
        'file': f'{FJC_COA}.csv',
        'kind': 'derived',
        'publisher': src['publisher'],
        'title_or_table': src['title_or_table'],
        'table_id': src['table_id'],
        'url': src['url'],
        'observation_period': 'Judges in active service on the export’s latest record (latest commission date 2026-10-22), as retrieved November 11, 2026',
        'geography': 'The 13 United States courts of appeals',
        'universe_or_base': 'The 179 Article III judges in active service on a court of appeals in the frozen export, with no senior-status or termination date',
        'unit': 'judges in active service, counted by Oath & Action',
        'date_retrieved': src['date_retrieved'],
        'vintage': src['vintage'],
        'qualification': ('A judge who takes senior status still hears cases but leaves this count, and vacant seats are not in the file, so a '
                          'court’s count is below its authorized judgeships when a seat is open'),
        'columns': {
            'court': {'type': 'text', 'description': 'the court as the directory names it'},
            'short_name': {'type': 'text', 'description': 'the court’s short name as a chart prints it (Ninth Circuit, D.C. Circuit, Federal Circuit), Oath & Action’s'},
            'circuit_order': {'type': 'integer', 'description': 'the courts’ customary order, First Circuit 1 to Eleventh 11, D.C. Circuit 12, Federal Circuit 13'},
            'judges': {'type': 'integer', 'description': 'judges in active service', 'unit': 'judges'},
        },
        'printed_source_line': ('Source: Federal Judicial Center, Biographical Directory of Article III Federal Judges, judges in active service on '
                                'the 13 courts of appeals, as of November 11, 2026, United States. Retrieved November 11, 2026. Judges on senior '
                                'status and vacant seats are not counted; judges counted by court by Oath & Action.'),
        'ledger_row': src['ledger_row'],
        'domain': src['domain'],
        'states': [],
        'derived_from': [f'{FJC}.csv'],
        'derivation': ('Rows of the frozen FJC file whose court_type is "U.S. Court of Appeals", counted by court_name; rows sorted by judges, '
                       'most first, then by circuit_order'),
        'notes': ['Made November 12, 2026 for Rule 14.6’s plate (the editor’s request ED-R1). The 13 counts sum to 179, the file’s court of appeals rows.'],
    }
    pm = DATA / f'{FJC_COA}.meta.json'
    text = json.dumps(meta, indent=1, ensure_ascii=False) + '\n'
    if not pm.exists() or pm.read_text(encoding='utf-8') != text:
        pm.write_text(text, encoding='utf-8')
        print(f'wrote {pm.relative_to(ROOT)}')
    print('; '.join(f'{r["short_name"]} {r["judges"]}' for r in out_rows))


ITEMS = {'s24': item_s24, 's34': item_s34, 's31': item_s31, 's27': item_s27, 'bc_m3': item_bc_m3, 'bc_s20': item_bc_s20,
         'ed_r1': item_ed_r1}


def main(argv):
    dl = None
    if '--dl' in argv:
        i = argv.index('--dl')
        dl = pathlib.Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if not argv or any(a not in ITEMS for a in argv):
        print(__doc__)
        print('items:', ', '.join(ITEMS))
        return 2
    for a in argv:
        print(f'== {a}')
        ITEMS[a](dl)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
