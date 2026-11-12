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


ITEMS = {'s24': item_s24, 's34': item_s34, 's31': item_s31, 's27': item_s27}


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
