"""research_review_fix_round3.py: the research lead's items in Phase 3 round 3's review fix pass, November 13, 2026
(brief: work/handoffs/phase-3/20261113_Round-3-Fix-Brief.md; rulings: the data lead's "Review fix pass").

Run, with the downloads in folders of their own:

    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s8 --dl <folder with roll285.xml, senate-618.xml>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s11 --dl <folder with meta-e6205a51.json, renewals.csv>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s2 --dl <any folder; reads only frozen files>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py bc_m1 --dl <folder with the FEC downloads below>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st_s4 --dl <folder with the Census API reads for state 72>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py bc_s9 --dl <folder with ecfr-435-916-20231001.xml, fr-2024-06566.htm, gi-1396a.htm>
    python3 -I work/build/scripts/phase-3/research_review_fix_round3.py st2_m1 --dl <download root holding bcm1/ and st2m1/>

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
- bc_m1 (BC-M1 with ST-S6, S73): fec-jfc-transfers-2024-all-committees, a new public file (P7-226). Every committee
  the FEC designates a joint fundraising committee (J) that paid either nominee's principal campaign committee in the
  2024 cycle (three for Harris, four for Trump), and every committee each paid on line 22 or line 28C, from the same
  aggregate by recipient and itemized Schedule B reads as RL-3. The two funds fec-jfc-transfers-2024 holds keep its 57
  rows unchanged (asserted equal to today's aggregate and committee records). Each recipient carries its kind by one
  rule (nominee campaign, national party committee, state party committee, other committee), stated in the sidecar.
  dl holds agg-to-<campaign>.json (2), committees-payers.json, agg-<jfc>.json (7), sbr-<jfc>-<recipient>.json for the
  five new funds' pairs, committees-recipients.json and detail-<recipient>.json (the FEC's Form 1 party type).
- st_s4 (ST-S4): the geography line of each public file behind S78, S81 and S83 says whether the publisher's table
  covers Puerto Rico; all three do (the Census API returns state 72 for B28002 and S2801, B19013 by municipio and County
  Business Patterns 2023 by municipio), so each says the file leaves Puerto Rico out. The Department of Labor's history
  file already holds it (S84).
- bc_s9 (BC-S9): the CMS sidecars' note on the procedural reason adds the regulation's words (42 CFR 435.916(a)(3)(iii)
  as in force in 2023) and CMS's own gloss in its 2024 rule (89 FR 22780, at 22800 and 22781), so a note can say what a
  procedural ending is from a primary source.
- st2_m1 (ST2-M1, S73): fec-jfc-transfers-2024-all-committees gains each line 22 amount's part paid before July 21, 2024,
  the day Harris's principal campaign committee and her three funds filed their new names (each had carried Joe
  Biden's), read the same way for all seven funds; the sidecar gives the sums by fund and kind on each side of the date
  and every fund's and principal committee's names in the cycle, as their statements of organization (Form 1) filed them.
  dl/st2m1 holds the two original funds' line 22 rows (hvf-22.json, tnc-22.json), the committees' Form 1 lists
  (f1-<id>.json, with f1-list.tsv) and the Form 1 files themselves (f1fec/<file>.fec); dl/bcm1 the five others' rows.
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
    if path.exists() and path.read_text(encoding='utf-8') == text:
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

def bc_m1(dl, write):
    import collections
    NOM = {'Kamala D. Harris': 'C00703975', 'Donald J. Trump': 'C00828541'}
    ELECTION = '2024-11-05'
    payers = {r['committee_id']: r for r in json.loads((dl / 'committees-payers.json').read_text())['results']}
    funds = {}
    for nom, camp in NOM.items():
        agg = json.loads((dl / f'agg-to-{camp}.json').read_text())
        assert agg['pagination']['count'] == len(agg['results'])
        js = [a for a in agg['results'] if payers[a['committee_id']]['designation'] == 'J']
        js.sort(key=lambda a: -a['total'])
        funds[nom] = [(a['committee_id'], payers[a['committee_id']]['name'], round(a['total'] * 100), a['count']) for a in js]
    assert [f[0] for f in funds['Kamala D. Harris']] == ['C00744946', 'C00838912', 'C00849281'], funds
    assert [f[0] for f in funds['Donald J. Trump']] == ['C00873893', 'C00770941', 'C00867937', 'C00855114'], funds
    cm = {r['committee_id']: r for r in json.loads((dl / 'committees-recipients.json').read_text())['results']}
    detail = {}
    for c in cm:
        d = json.loads((dl / f'detail-{c}.json').read_text())['results'][0]
        assert d['committee_id'] == c and d['committee_type'] == cm[c]['committee_type']
        detail[c] = d

    def kind(nom, rid):
        x = detail[rid]
        if rid == NOM[nom]:
            return 'nominee campaign'
        if x['committee_type'] in ('X', 'Y'):
            pt = x.get('party_type')
            if pt == 'NAT':
                return 'national party committee'
            if pt == 'STA':
                return 'state party committee'
            # one party committee's record gives no party type; its own name says state (Missouri)
            assert pt is None and rid == 'C00008664' and 'STATE COMMITTEE' in x['name'], (rid, x['name'], pt)
            return 'state party committee'
        return 'other committee'

    old = read_csv_raw(OUT / 'fec-jfc-transfers-2024.csv')
    head = old[0]
    assert len(head) == 16 and len(old) == 58
    ix = {c: i for i, c in enumerate(head)}
    new_cols = ['recipient_designation', 'recipient_party_type', 'recipient_kind']
    out_rows = {}
    for r in old[1:]:  # the two funds already frozen: rows unchanged, checked against today's reads
        jfc, rid = r[ix['jfc_id']], r[ix['recipient_id']]
        a = [x for x in json.loads((dl / f'agg-{jfc}.json').read_text())['results'] if x['recipient_id'] == rid][0]
        assert round(a['total'] * 100) == round(float(r[ix['amount']]) * 100) and a['count'] == int(r[ix['transactions']]), r
        assert a['recipient_name'] == r[ix['recipient_name']], (a['recipient_name'], r)
        x = cm[rid]
        assert (x['committee_type_full'], x['state'] or '') == (r[ix['recipient_type']], r[ix['recipient_state']]), (x, r)
        nom = r[ix['nominee']]
        out_rows.setdefault((nom, jfc), []).append(list(r) + [x['designation_full'], detail[rid].get('party_type_full') or '', kind(nom, rid)])
    for nom, fl in funds.items():
        for jfc, jname, to_camp, _ in fl:
            agg = json.loads((dl / f'agg-{jfc}.json').read_text())
            assert agg['pagination']['count'] == len(agg['results'])
            if (nom, jfc) in out_rows:
                assert len(out_rows[(nom, jfc)]) == len(agg['results']), jfc
                continue
            rows = []
            for a in sorted(agg['results'], key=lambda a: (-a['total'], a['recipient_id'])):
                rid = a['recipient_id']
                d = json.loads((dl / f'sbr-{jfc}-{rid}.json').read_text())
                res = d['results']
                assert d['pagination']['count'] == len(res) and all(e['memo_code'] is None for e in res), (jfc, rid)
                assert len({e['transaction_id'] for e in res}) == len(res) and len({e['sub_id'] for e in res}) == len(res)
                assert all(e['committee_id'] == jfc and e['recipient_committee_id'] == rid for e in res)
                res.sort(key=lambda e: (e['disbursement_date'], e['transaction_id']))
                lines = collections.defaultdict(list)
                for e in res:
                    lines[e['line_number']].append(e)
                counted = [ln for ln in ('22', '28C') if ln in lines]
                assert len(counted) == 1 and set(lines) <= {'22', '28C', '21B'}, (jfc, rid, set(lines))
                c = lines[counted[0]]
                amt = sum(round(e['disbursement_amount'] * 100) for e in c)
                assert amt == round(a['total'] * 100) and len(c) == a['count'], (jfc, rid)
                before = [e for e in res if e['disbursement_date'][:10] <= ELECTION]
                pick = before[-1] if before else res[0]
                assert len({e['recipient_name'] for e in res if e['disbursement_date'] == pick['disbursement_date']}) == 1
                spans = collections.OrderedDict()
                for e in res:
                    s = spans.setdefault(e['recipient_name'], [0, e['disbursement_date'][:10], e['disbursement_date'][:10]])
                    s[0] += 1
                    s[2] = e['disbursement_date'][:10]
                names = '; '.join(f'{k} ({v[0]} {"row" if v[0] == 1 else "rows"}, {v[1]} to {v[2]})' for k, v in spans.items())
                b = lines.get('21B', [])
                b_amt = sum(round(e['disbursement_amount'] * 100) for e in b)
                x = cm[rid]
                rows.append([nom, jfc, jname, rid, a['recipient_name'], x['committee_type_full'], x['state'] or '',
                             f'{amt // 100}.{amt % 100:02d}', str(len(c)), '; '.join(sorted(lines)),
                             'yes' if rid == NOM[nom] else '', pick['recipient_name'], names, counted[0],
                             f'{b_amt // 100}.{b_amt % 100:02d}', str(len(b)),
                             x['designation_full'], detail[rid].get('party_type_full') or '', kind(nom, rid)])
            out_rows[(nom, jfc)] = rows
    out = [head + new_cols]
    for nom, fl in funds.items():
        for jfc, *_ in fl:
            out.extend(out_rows[(nom, jfc)])
    body = out[1:]
    jx = {c: i for i, c in enumerate(out[0])}
    ids = set(f[0] for fl in funds.values() for f in fl)
    assert not any(r[jx['recipient_id']] in ids for r in body), 'a fund paid another fund'
    # each fund's line 22 or 28C row to its nominee's campaign equals what the campaign's aggregate shows it received
    for nom, fl in funds.items():
        for jfc, jname, to_camp, n in fl:
            cr = [r for r in body if r[jx['jfc_id']] == jfc and r[jx['is_nominee_campaign']] == 'yes']
            assert len(cr) == 1 and round(float(cr[0][jx['amount']]) * 100) == to_camp and int(cr[0][jx['transactions']]) == n, jfc
            assert cr[0][jx['amount_lines']] == '22'

    # sums by nominee and kind, line 22 only, for the sidecar and the report
    cents = lambda r: round(float(r[jx['amount']]) * 100)
    usd = lambda c: f'${c // 100:,}.{c % 100:02d}'
    summ = {}
    for nom in NOM:
        k22 = collections.OrderedDict((k, [0, set()]) for k in ('nominee campaign', 'national party committee', 'state party committee', 'other committee'))
        refunds = []
        for r in body:
            if r[jx['nominee']] != nom:
                continue
            if r[jx['amount_lines']] == '28C':
                refunds.append(r)
                continue
            s = k22[r[jx['recipient_kind']]]
            s[0] += cents(r)
            s[1].add(r[jx['recipient_id']])
        summ[nom] = (k22, refunds)
    hk, hr = summ['Kamala D. Harris']
    tk, tr = summ['Donald J. Trump']
    h22, t22 = sum(v[0] for v in hk.values()), sum(v[0] for v in tk.values())
    hn = len(set().union(*[v[1] for v in hk.values()]))
    tn = len(set().union(*[v[1] for v in tk.values()]))

    def kinds_words(k):
        return '; '.join(f'{kk} {usd(v[0])} to {len(v[1])}' for kk, v in k.items())

    name = 'fec-jfc-transfers-2024-all-committees'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    old_m, _ = read_meta(OUT / 'fec-jfc-transfers-2024.meta.json')
    cols = json.loads(json.dumps(old_m['columns']))
    cols['jfc_id']['description'] = 'FEC committee ID of the joint fundraising committee that paid'
    cols['jfc_name']['description'] = 'the joint fundraising committee’s name in the FEC’s committee record'
    cols['recipient_designation'] = {'type': 'category', 'description': (
        'the recipient committee’s designation in the FEC’s committee record today (for example principal campaign '
        'committee, leadership PAC, unauthorized)')}
    cols['recipient_party_type'] = {'type': 'category', 'description': (
        'for a party committee, the party type its statement of organization (Form 1) gives in the FEC’s committee record: '
        'NATIONAL or STATE; empty for any other committee, and for one party committee whose record gives none')}
    cols['recipient_kind'] = {'type': 'category', 'description': (
        'the receiver’s kind by the rule in the qualification: nominee campaign, national party committee, state party '
        'committee or other committee')}
    fund_words = {nom: ', '.join(f'{jn} ({j}, {usd(tc)} to the campaign in {n} {"payment" if n == 1 else "payments"})'
                                 for j, jn, tc, n in fl) for nom, fl in funds.items()}
    m = collections.OrderedDict()
    m['file'] = f'{name}.csv'
    m['kind'] = 'public'
    m['publisher'] = 'Federal Election Commission'
    m['title_or_table'] = ('Schedule B transfers and refunds to other committees of every joint fundraising committee '
                           'that paid a 2024 major-party nominee’s campaign, aggregated by recipient')
    m['table_id'] = ('OpenFEC /schedules/schedule_b/by_recipient_id/, /schedules/schedule_b/, /committees/ and '
                     '/committee/{id}/, 2024 cycle')
    m['url'] = ['https://api.open.fec.gov/v1/schedules/schedule_b/by_recipient_id/?recipient_id=C00703975&cycle=2024',
                'https://api.open.fec.gov/v1/schedules/schedule_b/by_recipient_id/?recipient_id=C00828541&cycle=2024',
                'https://api.open.fec.gov/v1/committees/?committee_id={payer}',
                'https://api.open.fec.gov/v1/schedules/schedule_b/by_recipient_id/?committee_id={jfc}&cycle=2024',
                'https://api.open.fec.gov/v1/schedules/schedule_b/?committee_id={jfc}&recipient_committee_id={recipient}&two_year_transaction_period=2024',
                'https://api.open.fec.gov/v1/committee/{recipient}/']
    m['observation_period'] = '2023 to 2024 election cycle'
    m['geography'] = 'United States'
    m['universe_or_base'] = (
        'For each 2024 major-party nominee, every committee the FEC designates a joint fundraising committee (designation '
        'J) that paid the nominee’s principal campaign committee in the 2024 cycle, three for Kamala Harris and four for '
        'Donald Trump, and every committee each paid on line 22 (transfers) or line 28C (refunds)')
    m['unit'] = 'dollars; transactions'
    m['date_retrieved'] = '2026-11-13'
    m['vintage'] = ('FEC processed filings as the API served them on November 12 and 13, 2026 (the Harris Victory Fund’s '
                    'and the Trump National Committee JFC’s rows as frozen in fec-jfc-transfers-2024, checked equal on '
                    'November 13)')
    m['qualification'] = (
        'The rule picks the senders: of the 92 committees that paid Harris’s campaign in the cycle, the FEC designates 3 '
        'joint fundraising committees, and of the 64 that paid Trump’s, 4; a committee that paid a campaign but is not '
        'designated J stays out for both (for example the Donald J. Trump Republican Nominee Fund 2024, an authorized '
        'committee). Amounts and transactions are the FEC’s aggregate by recipient for the cycle, which equals, for every '
        'row, the itemized payments on one line: line 22, transfers to other committees, or line 28C, a refund of a '
        'committee’s own contribution (amount_lines). Line 21B operating expenditures to the same committees are left out '
        'of amount and given in line_21b_amount. A joint fundraising committee splits contributions among its '
        'participants under its agreement, so a transfer is not a gift from the committee’s own funds. Receivers fold '
        'by kind, read the same way for both nominees: the nominee’s principal campaign committee is the nominee campaign; '
        'any other committee the FEC lists as a party committee (committee type X or Y) is a national party committee '
        'where its statement of organization gives the party type NATIONAL (the DNC and the RNC; no party’s House or '
        'Senate committee appears) and a state party committee where it gives STATE (the parties of states, DC and '
        'Guam, whatever their names, such as the Oklahoma Leadership Council, the Oklahoma Republican Party’s federal '
        'committee); the Missouri Republican State Committee-Federal’s record gives no party type and its own name '
        'makes it a state party committee; every other committee (campaigns of other candidates, leadership PACs, '
        'other PACs, and the Trump nominee fund) is an other committee. No fund paid another of the seven.')
    m['columns'] = cols
    m['printed_source_line'] = (
        'Source: Federal Election Commission, Schedule B transfers and refunds to other committees (lines 22 and 28C) of '
        'the seven committees the FEC designates joint fundraising committees that paid Kamala Harris’s or Donald '
        'Trump’s campaign, 2023 to 2024 cycle, United States. Retrieved November 12 and 13, 2026. Committees named as '
        'their payer wrote them before the November 5, 2024 election.')
    m['ledger_row'] = 'P7-226'
    m['domain'] = 'D03'
    m['states'] = []
    m['raw_files_sha256_prefix'] = {'fetch-log.tsv': 'see the download folder; every response logged with its SHA-256'}
    notes = []
    for nom in NOM:
        notes.append(f'{nom}’s joint fundraising committees, by what each sent the campaign: {fund_words[nom]}.')
    for nom, (k, rf) in summ.items():
        tot = sum(v[0] for v in k.values())
        n = len(set().union(*[v[1] for v in k.values()]))
        notes.append(
            f'Line 22 for {nom}, all funds together (BC-M1, read by script): {usd(tot)} to {n} committees; by kind, '
            f'{kinds_words(k)}. Line 28C refunds apart: '
            + ('; '.join(f'{r[jx["recipient_name_2024_election"]]} {usd(cents(r))} from {r[jx["jfc_name"]]}' for r in rf) or 'none') + '.')
    per_fund = []
    for nom, fl in funds.items():
        for j, jn, *_ in fl:
            rs = [r for r in body if r[jx['jfc_id']] == j and r[jx['amount_lines']] == '22']
            per_fund.append(f'{jn} {usd(sum(cents(r) for r in rs))} to {len(rs)}')
    notes.append('Line 22 by fund: ' + '; '.join(per_fund) + '.')
    b21 = [r for r in body if r[jx['line_21b_amount']] not in ('', '0.00')]
    notes.append('Line 21B to committees in the file, not in amount: ' + '; '.join(
        f'{r[jx["jfc_name"]]} to {r[jx["recipient_name_2024_election"]]}, {usd(round(float(r[jx["line_21b_amount"]]) * 100))} in {r[jx["line_21b_transactions"]]}'
        for r in b21) + '. Line 21B paid to committees outside the file was read for the Harris Victory Fund and the '
        'Trump National Committee JFC only (RL-4, in fec-jfc-transfers-2024’s notes), not for the other five.')
    st = lambda j: sorted(r[jx['recipient_state']] for r in body if r[jx['jfc_id']] == j and r[jx['recipient_kind']] == 'state party committee')
    fifty = set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH '
                'OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split())
    assert st('C00744946') == sorted(fifty | {'DC'})
    assert st('C00867937') == sorted((fifty - {'HI', 'VT'}) | {'DC', 'GU'})
    assert st('C00849281') == ['WI'] and not st('C00838912') and not st('C00873893') and not st('C00770941') and not st('C00855114')
    notes.append('Trump 47 Committee’s 50 state party committees are those of 48 states, DC and Guam (none for Hawaii or '
                 'Vermont); the Harris Victory Fund’s 51 are those of the 50 states and DC, and the Harris Baldwin Victory '
                 'Fund’s one, Wisconsin’s, is among them. The principal campaign committees’ names: see '
                 'fec-jfc-transfers-2024’s notes (both have since become PACs).')
    m['notes'] = notes
    text = dump_meta(m, '')
    return [(cp, write_csv(out)), (mp, text)], (
        f'{len(body)} rows; Harris {usd(h22)} on line 22 to {hn}, Trump {usd(t22)} to {tn}; '
        + ' | '.join(f'{nom}: {kinds_words(k)}' for nom, (k, _) in summ.items()))

def st_s4(dl, write):
    rd = lambda f: json.loads((dl / f).read_text(encoding='utf-8'))
    b28 = rd('b28002-acs1-2025-pr.json')
    s28 = rd('s2801-acs1-2025-pr-full.json')
    inc = rd('b19013-acs5-2024-pr.json')
    cbp = rd('cbp-2023-pr.json')
    cbs = rd('cbp-2023-pr-state.json')
    assert b28[1][0] == 'Puerto Rico' and b28[1][-1] == '72' and int(b28[1][1]) > 0
    assert s28[1][0] == 'Puerto Rico' and s28[1][-1] == '72' and float(s28[1][1]) > 0
    assert len(inc) - 1 == 78 and all(r[3] == '72' for r in inc[1:])
    assert len(cbp) - 1 == 78 and all(r[4] == '72' for r in cbp[1:])
    assert cbs[1][0] == 'Puerto Rico'
    files = []
    words = {
        'census-acs-broadband-by-state': (
            '50 states and DC, with a United States row (code US) to set apart',
            '50 states and DC, with a United States row (code US) to set apart; Puerto Rico left out, though the Bureau '
            'publishes B28002 and S2801 for it (state 72, read November 13, 2026)'),
        'census-acs5-county-median-household-income': (
            'Every county and county equivalent in the 50 states and DC (3144), Puerto Rico left out; Connecticut by its '
            'nine planning regions; and the United States as the first row (code US)',
            'Every county and county equivalent in the 50 states and DC (3144), Puerto Rico left out, though the Bureau '
            'publishes B19013 for its 78 municipios (read November 13, 2026); Connecticut by its nine planning regions; '
            'and the United States as the first row (code US)'),
        'census-cbp-county-employment': (
            'Every county in the 50 states and DC that the file lists (3142); Puerto Rico and the island areas left out',
            'Every county in the 50 states and DC that the file lists (3142); Puerto Rico left out, though County Business '
            'Patterns 2023 covers its 78 municipios (read November 13, 2026); the island areas are not in the file'),
    }
    for name, (old, new) in words.items():
        mp = OUT / f'{name}.meta.json'
        m, end = read_meta(mp)
        assert m['geography'] in (old, new), (name, m['geography'])
        m['geography'] = new
        files.append((mp, dump_meta(m, end)))
    return files, ('Puerto Rico published in all three: B28002 and S2801 (state 72), B19013 (78 municipios), CBP 2023 '
                   '(78 municipios); DOL history already holds PR, GU, VI; geography lines say each file leaves it out')


def bc_s9(dl, write):
    import html as _html
    import re as _re
    norm = lambda s: _re.sub(r'\s+', ' ', _html.unescape(_re.sub(r'<[^>]+>', ' ', s))).strip()
    ecfr = norm((dl / 'ecfr-435-916-20231001.xml').read_text(encoding='utf-8'))
    fr = norm((dl / 'fr-2024-06566.htm').read_text(encoding='utf-8', errors='replace'))
    q1 = ('Reconsider in a timely manner the eligibility of an individual who is terminated for failure to submit the '
          'renewal form or necessary information, if the individual subsequently submits the renewal form within 90 days '
          'after the date of termination, or a longer period elected by the State, without requiring a new application')
    q2 = ('individuals who are terminated for procedural reasons (that is, because they did not respond to the State\'s '
          'request for additional information)')
    q3 = 'losing coverage due to procedural reasons, including, for example, failure to return paperwork'
    assert q1 in ecfr and '[77 FR 17210, Mar. 23, 2012]' in ecfr
    page = lambda q: [g for g in _re.findall(r'\[\[Page (\d+)\]\]', fr[:fr.index(q)])][-1]
    assert q2 in fr and q3 in fr and page(q2) == '22800' and page(q3) == '22781'
    usc = norm((dl / 'gi-1396a.htm').read_text(encoding='utf-8', errors='replace'))
    assert ('(B) The number of individuals whose coverage for medical assistance, child health assistance, or '
            'pregnancy-related assistance was so terminated for procedural reasons.') in usc
    note = (
        'What a procedural ending is, in the rules’ words (BC-S9, read November 13, 2026). The renewal rule in force '
        'through the file’s period, 42 CFR 435.916(a)(3)(iii) (77 FR 17210, March 23, 2012; eCFR as of October 1, 2023), '
        'tells the state to “Reconsider in a timely manner the eligibility of an individual who is terminated for failure '
        'to submit the renewal form or necessary information, if the individual subsequently submits the renewal form '
        'within 90 days after the date of termination”. CMS’s 2024 eligibility rule (89 FR 22780, April 2, 2024) speaks '
        'of “individuals who are terminated for procedural reasons (that is, because they did not respond to the State’s '
        'request for additional information)” (at 22800) and of “losing coverage due to procedural reasons, including, '
        'for example, failure to return paperwork” (at 22781). Section 1902(tt)(1) of the Social Security Act, under '
        'which states reported these counts, names the two kinds apart: those terminated and, of them, those terminated '
        '“for procedural reasons”. No record read says how many people ended for a procedural reason were still '
        'eligible, or which reason was most common.')
    files = []
    for name in ('cms-medicaid-chip-renewal-outcomes', 'cms-medicaid-chip-renewal-funnel'):
        mp = OUT / f'{name}.meta.json'
        m, end = read_meta(mp)
        m['notes'] = set_note(list(m.get('notes') or []), 'What a procedural ending is, in the rules’ words', note)
        for u in ('https://www.ecfr.gov/api/versioner/v1/full/2023-10-01/title-42.xml?part=435&section=435.916',
                  'https://www.govinfo.gov/content/pkg/FR-2024-04-02/html/2024-06566.htm',
                  'https://www.govinfo.gov/content/pkg/USCODE-2024-title42/html/USCODE-2024-title42-chap7-subchapXIX-sec1396a.htm'):
            if u not in m['url']:
                m['url'].append(u)
        files.append((mp, dump_meta(m, end)))
    return files, 'note added to both CMS sidecars: 42 CFR 435.916(a)(3)(iii) and 89 FR 22800, 22781'

def st2_m1(dl, write):
    import collections
    import glob as _glob
    from decimal import Decimal
    CUT = '2024-07-21'
    name = 'fec-jfc-transfers-2024-all-committees'
    cp, mp = OUT / f'{name}.csv', OUT / f'{name}.meta.json'
    rows, (m, end) = read_csv_raw(cp), read_meta(mp)
    head = rows[0]
    new_cols = ['amount_before_2024_07_21', 'transactions_before_2024_07_21']
    base = head[:-2] if head[-2:] == new_cols else head
    assert base[-3:] == ['recipient_designation', 'recipient_party_type', 'recipient_kind'] and len(base) == 19, base
    ix = {c: i for i, c in enumerate(base)}
    items = []
    for f in ('hvf-22.json', 'tnc-22.json'):
        d = json.loads((dl / 'st2m1' / f).read_text())
        assert d['pagination']['count'] == len(d['results'])
        items += d['results']
    for f in sorted(_glob.glob(str(dl / 'bcm1' / 'sbr-*.json'))):
        items += [e for e in json.loads(Path(f).read_text())['results'] if e['line_number'] == '22']
    assert all(e['line_number'] == '22' and e['memo_code'] is None for e in items)
    assert len({e['sub_id'] for e in items}) == len(items) == 1030
    by = collections.defaultdict(lambda: [0, 0, 0, 0])   # cents before, count before, cents all, count all
    for e in items:
        k = (e['committee_id'], e['recipient_committee_id'])
        c = round(e['disbursement_amount'] * 100)
        by[k][2] += c
        by[k][3] += 1
        if e['disbursement_date'][:10] < CUT:
            by[k][0] += c
            by[k][1] += 1
    cents = lambda v: int((Decimal(v) * 100).to_integral_value())
    usd = lambda c: f'${c // 100:,}.{c % 100:02d}'
    out = [base + new_cols]
    n22 = 0
    for r in rows[1:]:
        r = list(r[:len(base)])
        k = (r[ix['jfc_id']], r[ix['recipient_id']])
        if r[ix['amount_lines']] == '22':
            n22 += 1
            b = by[k]
            assert (b[2], b[3]) == (cents(r[ix['amount']]), int(r[ix['transactions']])), (k, b, r[ix['amount']])
            r += [f'{b[0] // 100}.{b[0] % 100:02d}', str(b[1])]
        else:
            assert k not in by
            r += ['', '']
        out.append(r)
    assert n22 == len(by) == 119
    jx = {c: i for i, c in enumerate(out[0])}
    body = out[1:]
    # sums by fund and kind, and by nominee and kind, before and on or after the date
    S = collections.OrderedDict()
    for r in body:
        if r[jx['amount_lines']] != '22':
            continue
        for key in ((r[jx['nominee']], r[jx['jfc_name']], r[jx['recipient_kind']]), (r[jx['nominee']], 'all funds', r[jx['recipient_kind']]),
                    (r[jx['nominee']], r[jx['jfc_name']], 'all kinds'), (r[jx['nominee']], 'all funds', 'all kinds')):
            s = S.setdefault(key, [0, 0, 0, 0, set(), set()])
            bc, bn = cents(r[jx['amount_before_2024_07_21']]), int(r[jx['transactions_before_2024_07_21']])
            ac, an = cents(r[jx['amount']]), int(r[jx['transactions']])
            s[0] += bc; s[1] += bn; s[2] += ac - bc; s[3] += an - bn
            if bn:
                s[4].add(r[jx['recipient_id']])
            if an - bn:
                s[5].add(r[jx['recipient_id']])
    def side(c, n, who, when):
        if not n:
            return f'none {when}'
        return f'{usd(c)} to {len(who)} {when} ({n} {"payment" if n == 1 else "payments"})'

    def words(key):
        s = S[key]
        return side(s[0], s[1], s[4], 'before') + ', ' + side(s[2], s[3], s[5], 'on or after')
    lines = []
    for nom in ('Kamala D. Harris', 'Donald J. Trump'):
        lines.append(f'{nom}, all funds: ' + words((nom, 'all funds', 'all kinds')) + '; by kind: ' + '; '.join(
            f'{k} {words((nom, "all funds", k))}' for k in ('nominee campaign', 'national party committee', 'state party committee', 'other committee')
            if (nom, 'all funds', k) in S))
        for fund in dict.fromkeys(r[jx['jfc_name']] for r in body if r[jx['nominee']] == nom):
            if (nom, fund, 'all kinds') not in S:
                continue
            lines.append(f'{fund}: ' + words((nom, fund, 'all kinds')) + '; by kind: ' + '; '.join(
                f'{k} {words((nom, fund, k))}' for k in ('nominee campaign', 'national party committee', 'state party committee', 'other committee')
                if (nom, fund, k) in S))
    # names in the cycle, as each statement of organization (Form 1) filed them
    flist = [l.split('\t') for l in (dl / 'st2m1' / 'f1-list.tsv').read_text().strip().split('\n')]
    names = collections.OrderedDict()
    for cid, date, num, url in flist:
        txt = (dl / 'st2m1' / 'f1fec' / f'{num}.fec').read_bytes().decode('latin-1').replace('\r', '')
        rec = [l.split('\x1c') for l in txt.split('\n') if l.startswith('F1')][0]
        assert rec[1] == cid, (cid, num)
        names.setdefault(cid, []).append((date, rec[3], rec[2] == 'X', rec[0]))
    order = ['C00703975', 'C00744946', 'C00838912', 'C00849281', 'C00828541', 'C00873893', 'C00770941', 'C00867937', 'C00855114']
    assert list(names) == ['C00744946', 'C00703975', 'C00838912', 'C00849281', 'C00873893', 'C00828541', 'C00770941', 'C00867937', 'C00855114']
    def history(cid):
        seq, last = [], None
        for date, nm, flag, form in names[cid]:
            if nm != last:
                seq.append(f'“{nm}” ({"first filed" if form == "F1N" else ("filed as a new name" if flag else "on file")} {date})')
                last = nm
        return ' then '.join(seq)
    want = {'C00744946': ['Biden Victory Fund', 'Harris Victory Fund'], 'C00703975': ['Biden for President', 'Harris for President'],
            'C00838912': ['Biden Action Fund', 'Harris Action Fund'], 'C00849281': ['Biden Baldwin Victory Fund', 'Harris Baldwin Victory Fund'],
            'C00828541': ['DONALD J. TRUMP FOR PRESIDENT 2024, INC.', 'NEVER SURRENDER, INC.'],
            'C00873893': ['TRUMP NATIONAL COMMITTEE JFC', 'TRUMP NATIONAL COMMITTEE JFC, INC.'],
            'C00770941': ['TRUMP SAVE AMERICA JOINT FUNDRAISING COMMITTEE'],
            'C00867937': ['2024 RNC VICTORY', 'TRUMP 47 COMMITTEE', 'TRUMP 47 COMMITTEE, INC.'],
            'C00855114': ['TRUMP BILIRAKIS VICTORY FUND']}
    for cid, w in want.items():
        assert list(dict.fromkeys(n for _, n, _, _ in names[cid])) == w, (cid, names[cid])
    for cid in ('C00744946', 'C00703975', 'C00838912', 'C00849281'):
        assert [d for d, n, flag, _ in names[cid] if flag] == [CUT], cid   # the new name filed July 21, 2024
    assert [d for d, n, flag, _ in names['C00828541'] if n == 'NEVER SURRENDER, INC.'] == ['2024-11-12']
    cols = m['columns']
    cols['nominee']['description'] = (
        'the 2024 major-party nominee whose principal campaign committee the fund paid; Kamala D. Harris’s committee and her '
        'three funds carried Joe Biden’s name until July 21, 2024 (see amount_before_2024_07_21 and the notes)')
    cols['amount_before_2024_07_21'] = {'type': 'number', 'unit': 'dollars', 'description': (
        'of amount, the line 22 payments dated before July 21, 2024, the day Harris’s principal campaign committee and her '
        'three funds filed their new names; the same date test for all seven funds; empty for a line 28C row')}
    cols['transactions_before_2024_07_21'] = {'type': 'integer', 'description': (
        'of transactions, the line 22 payments dated before July 21, 2024; empty for a line 28C row')}
    q = m['qualification']
    add = (' Before July 21, 2024, the Democratic principal campaign committee and its three funds carried Joe Biden’s name '
           '(Biden for President, Biden Victory Fund, Biden Action Fund, Biden Baldwin Victory Fund); each filed its new name '
           'on a statement of organization received July 21, 2024. amount_before_2024_07_21 splits each line 22 amount by '
           'payment date at that day, read the same way for both sides.')
    if add not in q:
        q = q + add
    m['qualification'] = q
    notes = list(m.get('notes') or [])
    notes = set_note(notes, 'Names in the cycle, as each committee’s statements of organization', (
        'Names in the cycle, as each committee’s statements of organization (Form 1) filed them (ST2-M1, read November 13, '
        '2026 from the FEC’s filings list and the filed Form 1 files; the FEC’s committee history gives one name a two-year '
        'cycle, the latest): ' + '; '.join(f'{cid}, {history(cid)}' for cid in order) + '.'))
    notes = set_note(notes, 'Line 22 before July 21, 2024 and on or after', (
        'Line 22 before July 21, 2024 and on or after, by payment date, read the same way for all seven funds (ST2-M1; '
        'the 1,030 itemized payments sum to amount in all 119 line 22 rows): ' + ' | '.join(lines) + '.'))
    # the Republican campaign committee filed "NEVER SURRENDER, INC." on November 12, 2024: any line 22 payment after it
    camp = [e for e in items if e['recipient_committee_id'] == 'C00828541']
    late = sorted((e for e in camp if e['disbursement_date'][:10] >= '2024-11-12'), key=lambda e: (e['disbursement_date'], -e['disbursement_amount']))
    assert [(e['committee_id'], e['disbursement_date'][:10], round(e['disbursement_amount'] * 100), e['recipient_name']) for e in late] == [
        ('C00873893', '2024-12-11', 1518774435, 'DONALD J. TRUMP FOR PRESIDENT 2024, INC.'),
        ('C00873893', '2024-12-11', 394106284, 'NEVER SURRENDER, INC.')], late
    last_other = max(e['disbursement_date'][:10] for e in camp if e['committee_id'] != 'C00873893')
    assert last_other == '2024-10-30'
    lc = sum(round(e['disbursement_amount'] * 100) for e in late)
    notes = set_note(notes, 'Line 22 payments to the Republican principal campaign committee on or after November 12, 2024', (
        'Line 22 payments to the Republican principal campaign committee on or after November 12, 2024, the day it filed '
        'the name “NEVER SURRENDER, INC.” (ST2-M1, read by script from the itemized payments): two, both from the Trump '
        f'National Committee JFC on December 11, 2024, {usd(round(late[0]["disbursement_amount"] * 100))} with the payee '
        f'written “{late[0]["recipient_name"]}” and {usd(round(late[1]["disbursement_amount"] * 100))} written '
        f'“{late[1]["recipient_name"]}”, {usd(lc)} in all, inside the drawn amount; no other fund paid it on line 22 '
        'after October 30, 2024.'))
    m['notes'] = notes
    v = dict(m.get('source_line_variants') or {})
    v['with_form_1'] = (
        'Source: Federal Election Commission, itemized Schedule B transfers and refunds to other committees (lines 22 and '
        '28C) of the seven committees the FEC designates joint fundraising committees that paid the Democratic or the '
        'Republican presidential campaign committee, and those committees’ Statements of Organization (Form 1), 2023 to '
        '2024 cycle, United States. Retrieved November 12 and 13, 2026. Names and the dates they changed from Form 1; '
        'committees named as their payer wrote them before the November 5, 2024 election.')
    m['source_line_variants'] = v
    return [(cp, write_csv(out)), (mp, dump_meta(m, end))], '\n'.join(lines)


ITEMS = {'st_s8': st_s8, 'st_s11': st_s11, 'st_s2': st_s2, 'bc_m1': bc_m1, 'st_s4': st_s4, 'bc_s9': bc_s9, 'st2_m1': st2_m1}


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
