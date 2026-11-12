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


ITEMS = {'s24': item_s24}


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
