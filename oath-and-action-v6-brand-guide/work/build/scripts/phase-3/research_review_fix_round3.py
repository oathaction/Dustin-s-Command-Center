"""research_review_fix_round3.py: the research lead's items in Phase 3 round 3's review fix pass, November 13, 2026
(brief: work/handoffs/phase-3/20261113_Round-3-Fix-Brief.md; rulings: the data lead's "Review fix pass").

Run, with the downloads in folders of their own:

    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s8 --dl <folder with roll285.xml, senate-618.xml>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s11 --dl <folder with meta-e6205a51.json, renewals.csv>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s2 --dl <any folder; reads only frozen files>

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
- st_s2 (ST-S2, S76): fec-house-campaigns-2024-money-in-out nets transfers between a candidate's own committees
  candidate by candidate (the data lead's ruling), so an out line appears; its sidecar gives the remainder by campaign.
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


def st_s2(dl, write):
    """ST-S2 (S76): fec-house-campaigns-2024-money-in-out nets transfers between a candidate's own committees candidate
    by candidate, as S76's note says, instead of across all 1,926 candidates at once; and its sidecar says what the
    file shows of the remainder, with no cause. Reads only the frozen by-candidate file; dl is not read."""
    from decimal import Decimal
    src = read_csv_raw(OUT / 'fec-house-campaigns-2024-by-candidate.csv')
    head, body = src[0], src[1:]
    cand = [dict(zip(head, r)) for r in body]
    assert len(cand) == 1926
    cents = lambda r, k: int((Decimal(r[k] or '0') * 100).to_integral_value())
    tot = lambda k: sum(cents(r, k) for r in cand)
    frm, to = tot('trans_from_auth'), tot('trans_to_auth')
    net_in = sum(max(0, cents(r, 'trans_from_auth') - cents(r, 'trans_to_auth')) for r in cand)
    net_out = sum(max(0, cents(r, 'trans_to_auth') - cents(r, 'trans_from_auth')) for r in cand)
    n_in = sum(1 for r in cand if cents(r, 'trans_from_auth') > cents(r, 'trans_to_auth'))
    n_out = sum(1 for r in cand if cents(r, 'trans_to_auth') > cents(r, 'trans_from_auth'))
    named_in = ['ttl_indiv_contrib', 'other_pol_cmte_contrib', 'pol_pty_contrib', 'cand_contrib', 'cand_loans', 'other_loans']
    named_out = ['indiv_refunds', 'cmte_refunds', 'cand_loan_repay', 'other_loan_repay']
    want = {
        'cash_start': tot('coh_bop'), 'individuals': tot('ttl_indiv_contrib'), 'other_committees': tot('other_pol_cmte_contrib'),
        'party': tot('pol_pty_contrib'), 'candidate_contributions': tot('cand_contrib'), 'candidate_loans': tot('cand_loans'),
        'other_loans': tot('other_loans'), 'transfers_in_net': net_in,
        'other_receipts': tot('ttl_receipts') - sum(tot(k) for k in named_in) - frm,
        'spending': tot('ttl_disb') - sum(tot(k) for k in named_out) - to,
        'refunds_individuals': tot('indiv_refunds'), 'refunds_committees': tot('cmte_refunds'),
        'candidate_loan_repayments': tot('cand_loan_repay'), 'other_loan_repayments': tot('other_loan_repay'),
        'transfers_out_net': net_out, 'cash_end': tot('coh_cop')}
    name = 'fec-house-campaigns-2024-money-in-out'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    rows, (m, end) = read_csv_raw(cp), read_meta(mp)
    assert rows[0] == ['order', 'side', 'line_id', 'line', 'dollars']
    words = {'transfers_in_net': 'Transfers from other committees of the same candidates, net of transfers out, candidate by candidate',
             'transfers_out_net': 'Transfers to other committees of the same candidates, net of transfers in, candidate by candidate'}
    old_words = {'transfers_in_net': 'Transfers from other committees of the same candidates, net of transfers out',
                 'transfers_out_net': 'Transfers to other committees of the same candidates, net of transfers in'}
    out = [rows[0]]
    for r in rows[1:]:
        r = list(r)
        lid = r[2]
        v = want[lid]
        if lid in words:
            assert r[3] in (old_words[lid], words[lid]), r
            r[3] = words[lid]
            r[4] = f'{v // 100}.{v % 100:02d}'
        else:  # every other line is the frozen value, recomputed to the cent
            assert int((Decimal(r[4]) * 100).to_integral_value()) == v, (lid, r[4], v)
        out.append(r)
    assert [r[2] for r in out[1:]] == list(want)
    ins = sum(want[r[2]] for r in out[1:] if r[1] == 'in')
    outs = sum(want[r[2]] for r in out[1:] if r[1] == 'out')
    rem_c = {r['cand_id']: cents(r, 'coh_bop') + cents(r, 'ttl_receipts') - cents(r, 'ttl_disb') - cents(r, 'coh_cop') for r in cand}
    nz = {k: v for k, v in rem_c.items() if v}
    pos, neg = sum(v for v in nz.values() if v > 0), -sum(v for v in nz.values() if v < 0)
    big_id, big = max(nz.items(), key=lambda kv: abs(kv[1]))
    big_row = next(r for r in cand if r['cand_id'] == big_id)
    rem = ins - outs
    assert rem == sum(nz.values()) == 153315803, rem          # the remainder does not move
    assert (net_in, net_out, n_in, n_out, len(nz)) == (17510377247, 1831324858, 436, 84, 297)
    assert (big_id, big, big_row['coverage_end']) == ('H4IN05195', 150000000, '04/30/2024')
    assert (ins, outs) == (262648161775, 262494845972)
    took = ins - want['cash_start']
    usd = lambda c: f'${c // 100:,}.{c % 100:02d}'
    pct = lambda a, b, d: f'{100 * a / b:.{d}f}'
    others = sum(v for k, v in nz.items() if k != big_id)
    m['qualification'] = (
        'No dollar received is traced to a dollar spent: the node is all House campaigns together. Loans and their '
        'repayments are their own lines, so a loan is not read as a gift. Transfers between a candidate’s own committees '
        f'are netted candidate by candidate: {n_in} candidates took in more from their other committees than they sent '
        f'them ({usd(net_in)} net, on the in side) and {n_out} sent more than they took ({usd(net_out)} net, on the out '
        f'side). Cash at the start plus receipts comes to {usd(ins)}; spending, refunds, repayments, transfers and cash '
        f'at the end come to {usd(outs)}; the remainder, {usd(rem)}, is the figures of {len(nz)} of the 1,926 campaigns '
        'that do not balance in the file (cash at the start plus receipts, less disbursements and cash at the end), '
        f'{usd(big)} of it from one campaign. The file gives no cause.')
    m['derivation'] = (
        'Sums of the file’s columns over every House candidate; other receipts and spending are totals less the named '
        'lines; transfers between a candidate’s own committees are netted candidate by candidate, each candidate’s net '
        'transfers in summed on the in side and net transfers out on the out side.')
    notes = [n for n in (m.get('notes') or []) if not n.startswith('In: ')]
    notes.insert(0, f'In: {usd(ins)[1:]}; out: {usd(outs)[1:]}; remainder: {usd(rem)[1:]} ({pct(rem, ins, 3)} percent of '
                    f'the in side). Receipts with cash at the start left out: {usd(took)[1:]}; individuals '
                    f'{usd(want["individuals"])[1:]}, {pct(want["individuals"], took, 1)} percent of them.')
    notes = set_note(notes, 'The remainder, by campaign', (
        f'The remainder, by campaign (ST-S2, November 13, 2026): {len(nz)} of the 1,926 campaigns do not balance, '
        f'{sum(1 for v in nz.values() if v > 0)} leaving more in than out ({usd(pos)}) and '
        f'{sum(1 for v in nz.values() if v < 0)} less ({usd(neg)}). One campaign, {big_id}, whose last report in the '
        f'file covers through April 30, 2024, leaves {usd(big)}, {pct(big, rem, 1)} percent of the net remainder; the '
        f'other {len(nz) - 1} leave {usd(others)} net, from {usd(pos - big)} over and {usd(neg)} under. The chart names '
        'no candidate.'))
    notes = set_note(notes, 'Transfers netted candidate by candidate since', (
        'Transfers netted candidate by candidate since November 13, 2026 (ST-S2): before, the file netted them across all '
        f'1,926 campaigns at once ({usd(frm - to)} in, $0.00 out), which set one campaign’s transfers out against '
        f'another’s transfers in. Money in and out each grow by {usd(net_out)}; the remainder does not move.'))
    m['notes'] = notes
    return [(cp, write_csv(out)), (mp, dump_meta(m, end))], (
        f'net in {usd(net_in)} ({n_in} candidates), net out {usd(net_out)} ({n_out}); in {usd(ins)}, out {usd(outs)}, '
        f'remainder {usd(rem)} ({pct(rem, ins, 3)} percent); individuals {pct(want["individuals"], took, 1)} percent of '
        f'{usd(took)}; {len(nz)} campaigns unbalanced, {big_id} {usd(big)}')


ITEMS = {'st_s8': st_s8, 'st_s11': st_s11, 'st_s2': st_s2}


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
