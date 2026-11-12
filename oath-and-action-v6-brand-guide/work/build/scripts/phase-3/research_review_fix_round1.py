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


ITEMS = {'s24': item_s24, 's34': item_s34}


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
