"""research_review_fix_round3.py: the research lead's items in Phase 3 round 3's review fix pass, November 13, 2026
(brief: work/handoffs/phase-3/20261113_Round-3-Fix-Brief.md; rulings: the data lead's "Review fix pass").

Run, with the downloads in folders of their own:

    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s8 --dl <folder with roll285.xml, senate-618.xml>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s11 --dl <folder with meta-e6205a51.json, renewals.csv>

Add --write to write. Each item reads its downloads, checks them against the hashes the sidecars record, asserts every
frozen field it does not mean to change, and sets values rather than appending, so a rerun writes nothing. It refuses
to write when a check fails.

- st_s8 (ST-S8): congress-hr5371-roll-calls-by-member prints each House member's name as the Clerk's roll call 285
  prints it (the element's text, accents kept), not the record's unaccented-name attribute the freeze read. Four names
  change: Barragán, García (IL), Sánchez, Velázquez. The Senate's names are checked against vote 618; three lose the
  doubled space the freeze made where the record ends a first name with a space (Curtis, Risch, Schmitt).
- st_s11 (ST-S11): S65's source line can name CMS's release. A variant on cms-medicaid-chip-renewal-funnel (S65's first
  dataset) and one on cms-medicaid-chip-renewal-outcomes, each the printed line with "October 2024 final release" after
  the title, from the metastore record and the file, both read today and equal to the frozen file's hash.
"""
import argparse
import csv
import hashlib
import io
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'work/build/data'


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
    end = '\n' if t.endswith('\n') else ''
    assert json.dumps(m, indent=1, ensure_ascii=False) + end == t, f'{p.name} is not in its writer format; stop'
    return m, end


def dump_meta(m, end):
    t = json.dumps(m, indent=1, ensure_ascii=False) + end
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
def st_s8(dl, write):
    name = 'congress-hr5371-roll-calls-by-member'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    rows, (m, end) = read_csv_raw(cp), read_meta(mp)
    raw = m['raw_files_sha256_prefix']
    assert sha16(dl / 'roll285.xml') == raw['house-285.xml'], 'the Clerk file is not the frozen raw; stop'
    assert sha16(dl / 'senate-618.xml') == raw['senate-618.xml'], 'the Senate file is not the frozen raw; stop'
    head = rows[0]
    assert head == ['chamber', 'vote', 'vote_date', 'question', 'result', 'member_id', 'member', 'party', 'state', 'vote_cast']
    ix = {c: i for i, c in enumerate(head)}

    house = {}
    for rv in ET.parse(dl / 'roll285.xml').getroot().iter('recorded-vote'):
        leg = rv.find('legislator')
        house[leg.get('name-id')] = (leg.text, leg.get('unaccented-name'), leg.get('party'), leg.get('state'), rv.find('vote').text)
    senate = {}
    for mem in ET.parse(dl / 'senate-618.xml').getroot().iter('member'):
        t = lambda k: mem.find(k).text or ''
        g = lambda k: t(k).strip()
        # the record's first_name ends in a space for three senators; the freeze's join kept it ("John  Curtis")
        senate[g('lis_member_id')] = (g('first_name') + ' ' + g('last_name'), g('party'), g('state'), g('vote_cast'),
                                      t('first_name') + ' ' + t('last_name'))

    out, changed = [head], []
    n_house = n_senate = 0
    for r in rows[1:]:
        r = list(r)
        if r[ix['chamber']] == 'House':
            n_house += 1
            text, unacc, party, state, vote = house[r[ix['member_id']]]
            # the freeze read the unaccented attribute; every other field equals the record
            assert r[ix['member']] in (unacc, text), (r, unacc, text)
            assert (r[ix['party']], r[ix['state']], r[ix['vote_cast']]) == (party, state, vote), r
            if r[ix['member']] != text:
                changed.append((r[ix['member_id']], r[ix['member']], text))
                r[ix['member']] = text
        else:
            n_senate += 1
            full, party, state, vote, joined_raw = senate[r[ix['member_id']]]
            assert r[ix['member']] in (full, joined_raw), r
            assert (r[ix['party']], r[ix['state']], r[ix['vote_cast']]) == (party, state, vote), r
            if r[ix['member']] != full:
                changed.append((r[ix['member_id']], r[ix['member']], full))
                r[ix['member']] = full
        out.append(r)
    assert (n_house, n_senate) == (len(house), len(senate)) == (433, 100), (n_house, n_senate, len(house), len(senate))
    want = {('B001300', 'Barragan', 'Barragán'), ('G000586', 'Garcia (IL)', 'García (IL)'),
            ('S001156', 'Sanchez', 'Sánchez'), ('V000081', 'Velazquez', 'Velázquez'),
            ('S431', 'John  Curtis', 'John Curtis'), ('S323', 'James  Risch', 'James Risch'),
            ('S420', 'Eric  Schmitt', 'Eric Schmitt')}
    assert not changed or set(changed) == want, changed
    assert all(r[ix['member']] == senate[r[ix['member_id']]][0] for r in out[1:] if r[ix['chamber']] == 'Senate')
    assert not any('  ' in r[ix['member']] or r[ix['member']] != r[ix['member']].strip() for r in out[1:])
    # after the change every House name is the record's printed text
    assert all(r[ix['member']] == house[r[ix['member_id']]][0] for r in out[1:] if r[ix['chamber']] == 'House')
    note = ('Names as each record prints them (ST-S8, November 13, 2026): a House member’s name is the text of the Clerk’s '
            'legislator element, accents kept (Barragán, García (IL), Sánchez, Velázquez), re-read from the same file '
            '(SHA-256 prefix dfbc7b2e76b87b86); the freeze of November 12 had read the record’s unaccented-name attribute. '
            'A senator’s name is the Senate record’s first_name and last_name joined by one space, checked against vote 618 '
            '(SHA-256 prefix ab81bac6e53d98c8); the record carries no accents (Ben Lujan as printed), and the space the '
            'record leaves after three first names (Curtis, Risch, Schmitt) is not doubled.')
    m['notes'] = set_note(list(m.get('notes') or []), 'Names as each record prints them', note)
    return [(cp, write_csv(out)), (mp, dump_meta(m, end))], (
        '4 House names take the record’s accents and 3 Senate names lose a doubled space; '
        f'{n_house} House and {n_senate} Senate rows checked against the records')


def st_s11(dl, write):
    meta = json.loads((dl / 'meta-e6205a51.json').read_text(encoding='utf-8'))
    dist = meta['distribution'][0]['data']
    assert meta['identifier'] == 'e6205a51-e6d7-4849-9882-4483b8a28c41'
    assert meta['title'] == 'Medicaid and CHIP Updated Renewal Outcomes', meta['title']
    assert meta['modified'] == '2024-11-01T00:05:00+00:00', meta['modified']
    assert dist['downloadURL'] == 'https://download.medicaid.gov/data/updated-renewal-outcomes-october-2024-releasefinal.csv'
    files = []
    for name in ('cms-medicaid-chip-renewal-funnel', 'cms-medicaid-chip-renewal-outcomes'):
        mp = OUT / f'{name}.meta.json'
        m, end = read_meta(mp)
        assert sha16(dl / 'renewals.csv') == m['raw_files_sha256_prefix']['renewals.csv'], 'not the frozen raw; stop'
        assert m['url'][0] == dist['downloadURL']
        assert m['vintage'] == 'Updated renewal outcomes, October 2024 final release (dataset modified November 1, 2024)'
        line = m['printed_source_line']
        title = 'Medicaid and CHIP Updated Renewal Outcomes, '
        assert line.count(title) == 1, line
        v = line.replace(title, title + 'October 2024 final release, ')
        variants = dict(m.get('source_line_variants') or {})
        variants['with_release'] = v
        m['source_line_variants'] = variants
        files.append((mp, dump_meta(m, end)))
    return files, 'variant with_release on both sidecars: "... Updated Renewal Outcomes, October 2024 final release, renewals due ..."'


ITEMS = {'st_s8': st_s8, 'st_s11': st_s11}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('item', choices=sorted(ITEMS))
    ap.add_argument('--dl', required=True)
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    files, summary = ITEMS[a.item](Path(a.dl), a.write)
    for p, text in files:
        print(f'{p.name}: {put(p, text, a.write)}')
    print(f'{a.item}: {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
