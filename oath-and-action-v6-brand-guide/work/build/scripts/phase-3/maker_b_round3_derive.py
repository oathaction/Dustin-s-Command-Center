"""Maker B, Phase 3 round 3: R2-2's derived table for S77, and the figure checks for S65 and S73 to S77.

    python3 -I work/build/scripts/phase-3/maker_b_round3_derive.py [--check] [--figures]

Reads frozen files in work/build/data/ and writes two derived tables with their sidecars (contract C1, R2-2):

- fec-jfc-transfers-2024-by-node: every payment row of fec-jfc-transfers-2024 (P7-216, RL-3) with the node S73
  draws it in, so the page's table prints one row a node and the CSV export every row (D3-1097)
- govinfo-snap-application-path: the steps of 7 CFR 273.2 in the order a screen reader takes them, each with the step
  that follows it named (contract R3-6: a journey map's table lists its steps in reading order with each link named),
  from govinfo-snap-application-steps (P7-208). The main path's steps run in their order and the last says the path
  ends; the branch follows them, names the step it leaves, and names its own next step, the postponed proof (273.2(i)).

--check writes nothing and fails when a written file differs from what the script computes now. --figures writes
nothing and checks every figure in the titles, notes, alts, chart notes and labels of specs S65 and S73 to S77 against
the data files, each check named in the spec's notes_internal (check S65, check S73 to check S77). Standard library only.
"""
import csv
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data'))
SPECS = os.path.normpath(os.path.join(HERE, '..', '..', 'chart-kit', 'specs'))
CHECK = '--check' in sys.argv
FAULTS = []


def read(name):
    with open(os.path.join(DATA, name + '.csv'), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def read_json(name):
    with open(os.path.join(DATA, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)['rows']


def meta(name):
    with open(os.path.join(DATA, name + '.meta.json'), encoding='utf-8') as fh:
        return json.load(fh)


def num(s):
    return float(s) if s not in (None, '') else None


def csv_text(columns, rows):
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n')
    w.writerow(columns)
    for r in rows:
        w.writerow([r[c] for c in columns])
    return out.getvalue()


def write(name, columns, rows, side):
    text = csv_text(columns, rows)
    side_text = json.dumps(side, ensure_ascii=False, indent=1) + '\n'
    for path, body in ((os.path.join(DATA, name + '.csv'), text), (os.path.join(DATA, name + '.meta.json'), side_text)):
        if CHECK:
            if not os.path.exists(path) or open(path, encoding='utf-8').read() != body:
                FAULTS.append('differs from what the script computes: ' + os.path.basename(path))
        else:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(body)
    print(('checked ' if CHECK else 'wrote ') + name + ' (%d rows)' % len(rows))


# ---------------------------------------------------------------------------------------------------------------
# S77: the SNAP application path in reading order, each step's next step named (R3-6)
# ---------------------------------------------------------------------------------------------------------------
def snap_path():
    src = 'govinfo-snap-application-steps'
    m = meta(src)
    rows = sorted(read(src), key=lambda r: int(r['order']))
    main = [r for r in rows if r['path'] == 'main']
    branch = [r for r in rows if r['path'] != 'main']
    if not main or len(branch) != 1:
        FAULTS.append('S77: expected one main path and one branch in ' + src)
        return
    br = branch[0]
    # the branch's condition, in the provision summary's own words: "A household with very little income or cash gets ..."
    mt = re.match(r'^A (household with [^,]+?) gets ', br['what_happens'])
    if not mt:
        FAULTS.append('S77: the branch summary no longer opens with its condition')
        return
    cond = 'a ' + mt.group(1)
    out = []
    for i, r in enumerate(main):
        if i + 1 < len(main):
            nxt = main[i + 1]['step']
            if i == 0:
                nxt += '; or ' + br['step'].lower() + ', with its own interview inside 7 days, for ' + cond
        else:
            nxt = 'None: the path ends with benefits or a denial notice'
        out.append(dict(r, next_step=nxt, path_words='Every application'))
    # 7 CFR 273.2(i)(3)(iii) and (i)(4)(iii)(A), as the research lead read them November 13, 2026: an expedited household is
    # still interviewed within the 7 days, and the proof the state postponed comes due by the second or third month of
    # benefits ("the household must reapply and satisfy all verification requirements which were postponed")
    out.append(dict(br, next_step='Postponed proof, due by the second or third month of benefits', path_words='Branch after “' + main[0]['step'] + '”, for ' + cond))
    cols = ['order', 'step', 'path', 'path_words', 'who_acts', 'time_limit', 'next_step', 'what_happens', 'legal_basis', 'source_words']
    side = {
        'file': 'govinfo-snap-application-path.csv',
        'kind': 'derived',
        'publisher': m['publisher'],
        'title_or_table': 'Supplemental Nutrition Assistance Program, application processing, 7 CFR 273.2: the steps in reading order, each with the step that follows it',
        'table_id': m['table_id'],
        'url': m['url'],
        'observation_period': m['observation_period'],
        'geography': m['geography'],
        'universe_or_base': m['universe_or_base'],
        'unit': 'steps; days',
        'date_retrieved': m['date_retrieved'],
        'vintage': m['vintage'],
        'qualification': m['qualification'],
        'columns': {
            'order': m['columns']['order'],
            'step': m['columns']['step'],
            'path': m['columns']['path'],
            'path_words': {'type': 'text', 'description': 'who takes the step, in words: every application, or the branch with its condition'},
            'who_acts': m['columns']['who_acts'],
            'time_limit': m['columns']['time_limit'],
            'next_step': {'type': 'text', 'description': 'the step that follows, named, in reading order (contract R3-6)'},
            'what_happens': m['columns']['what_happens'],
            'legal_basis': m['columns']['legal_basis'],
            'source_words': m['columns']['source_words'],
        },
        'printed_source_line': 'Source: Office of the Federal Register and U.S. Government Publishing Office, Electronic Code of Federal Regulations, 7 CFR 273.2, SNAP application processing, as in force November 9, 2026, United States. Retrieved November 12, 2026. Times are the regulation’s limits; each step’s next step named by Oath & Action.',
        # D3-1327 (B-S4): the rule's in-force date prints once, in the grade line; this variant leaves it out of the source line
        'source_line_variants': {'date_in_grade_line': 'Source: Office of the Federal Register and U.S. Government Publishing Office, Electronic Code of Federal Regulations, 7 CFR 273.2, SNAP application processing, United States. Retrieved November 12, 2026. Times are the regulation’s limits; each step’s next step named by Oath & Action.'},
        'ledger_row': m['ledger_row'],
        'domain': m['domain'],
        'domain_note': m.get('domain_note', ''),
        'states': [],
        'notes': m.get('notes', []),
        'derived_from': [src + '.csv'],
        'derivation': 'The rows of ' + src + ' in reading order: the main path by its order, then the branch. next_step names the main step that follows each step (the first also names the branch, with the condition the branch summary opens with); the last step of the path says it ends, and the branch’s next step is the postponed proof, due by the second or third month of benefits, with its interview inside the 7 days (7 CFR 273.2(i)(3)(iii) and (i)(4)(iii)(A), as the research lead read them November 13, 2026). path_words puts the path column in words. No other value changes.',
    }
    write('govinfo-snap-application-path', cols, out, side)


# ---------------------------------------------------------------------------------------------------------------
# S73: each payment row with the node the drawing folds it into, so the page's table prints one row a node and the CSV
# export every row (the main session's D3-1097 on weight; the data lead's ruling RL-3a on what draws)
# ---------------------------------------------------------------------------------------------------------------
def jfc_nodes():
    # BC-M1 with D3-1330 (the data lead's ruling and its sign-off of the seven): every committee the FEC designates a joint
    # fundraising committee that paid a nominee's campaign, three for Harris and four for Trump, from the research lead's
    # fec-jfc-transfers-2024-all-committees (P7-226). The drawing folds each nominee's funds into one sender and the
    # receivers by the sidecar's recipient_kind, read the same way for both; the table prints one row for each fund and
    # kind of receiver, its refunds last
    src = 'fec-jfc-transfers-2024-all-committees'
    m = meta(src)
    rows = read(src)
    nominees = ['Kamala D. Harris', 'Donald J. Trump']
    kinds = ['nominee campaign', 'national party committee', 'state party committee', 'other committee']
    campaign = {'Kamala D. Harris': 'Harris for President, the campaign', 'Donald J. Trump': 'Donald J. Trump for President 2024, the campaign'}
    national = {'Kamala D. Harris': 'Democratic National Committee', 'Donald J. Trump': 'Republican National Committee'}
    # each fund in the order the sidecar's notes list it, by what it sent the campaign
    funds = {}
    for nom in nominees:
        paid = {}
        for r in rows:
            if r['nominee'] == nom and r['recipient_kind'] == 'nominee campaign' and r['amount_lines'] == '22':
                paid[r['jfc_name']] = paid.get(r['jfc_name'], 0) + float(r['amount'])
        funds[nom] = sorted(paid, key=lambda f: -paid[f])
    if [len(funds[n]) for n in nominees] != [3, 4]:
        FAULTS.append('S73: expected three funds for Harris and four for Trump, found %r' % funds)
        return
    drawn = [r for r in rows if r['amount_lines'] == '22']
    bad = [r['recipient_id'] for r in rows if r['amount_lines'] not in ('22', '28C') or r['recipient_kind'] not in kinds or r['nominee'] not in nominees]
    if bad:
        FAULTS.append('S73: rows outside the rule: %r' % bad)
        return
    # a receiver paid by two funds counts once in its node's count
    distinct = {(n, k): len({r['recipient_id'] for r in drawn if r['nominee'] == n and r['recipient_kind'] == k}) for n in nominees for k in kinds}
    def node(r):
        n, k = r['nominee'], r['recipient_kind']
        if r['amount_lines'] == '28C':
            return 'Refunds, not drawn'
        if k == 'nominee campaign':
            return campaign[n]
        if k == 'national party committee':
            return national[n]
        c = distinct[(n, k)]
        return '%d state party committee%s' % (c, '' if c == 1 else 's') if k == 'state party committee' else '%d other committee%s' % (c, '' if c == 1 else 's')
    def table_to(r, grp):
        k = r['recipient_kind']
        if r['amount_lines'] == '28C':
            return 'Refunds of their own contributions (line 28C), not drawn: ' + '; '.join(x['recipient_name_2024_election'] for x in grp)
        if k in ('nominee campaign', 'national party committee'):
            return node(r)
        if k == 'state party committee':
            return 'State party committees'
        return 'Other committees: ' + '; '.join(x['recipient_name_2024_election'] for x in grp)
    out, order = [], 0
    for refund in (False, True):
        for n in nominees:
            for k in kinds:
                for f in funds[n]:
                    grp = [r for r in rows if r['nominee'] == n and r['recipient_kind'] == k and r['jfc_name'] == f and (r['amount_lines'] == '28C') == refund]
                    if not grp:
                        continue
                    order += 1
                    grp.sort(key=lambda r: -float(r['amount']))
                    tt = table_to(grp[0], grp)
                    for r in grp:
                        out.append(dict(r, link_id=str(len(out) + 1), node=node(r), table_row=str(order), table_to=tt))
    if len(out) != len(rows):
        FAULTS.append('S73: %d rows written of %d' % (len(out), len(rows)))
    cols = list(rows[0].keys()) + ['link_id', 'node', 'table_row', 'table_to']
    side = dict(m)
    side.update({
        'file': 'fec-jfc-transfers-2024-by-node.csv',
        'kind': 'derived',
        'title_or_table': m['title_or_table'] + ', each payment with the node the network diagram draws it in and the table row it prints in',
        'columns': dict(m['columns'],
                        link_id={'type': 'id', 'description': 'the row\'s own short ID, its place in this file\'s order: one paying fund, one committee paid, one report line'},
                        node={'type': 'text', 'description': 'the receiver the drawing folds the payment into, for its nominee: the campaign, the national party committee, the state party committees with their count, or the other committees with their count; a line 28C refund does not draw'},
                        table_row={'type': 'id', 'description': 'the page table\'s row: one for each fund and kind of receiver, then each fund\'s refunds, in the order the table prints them'},
                        table_to={'type': 'text', 'description': 'the words the page table prints for the row\'s receivers: the committee, its kind, or the other committees and refunds by name, as the payer wrote them'}),
        'printed_source_line': m['printed_source_line'],
        'derived_from': [src + '.csv'],
        'derivation': 'The rows of ' + src + ' unchanged, with four columns added, read the same way for both nominees: node names the receiver the network diagram draws each line 22 payment in, by recipient_kind (each nominee\'s campaign and national party committee alone; its state party committees and its other committees each as one node, counted once each, whichever fund paid them), and marks a line 28C refund, which does not draw; link_id numbers the rows in this order, one fund, committee and report line each; table_row and table_to give the page table one row for each fund and kind of receiver, in the order nominee, kind, then fund by what it sent the campaign, with each fund\'s refunds after every drawn row. Rows sorted in that order, then by amount, largest first.',
    })
    write('fec-jfc-transfers-2024-by-node', cols, out, side)


# ---------------------------------------------------------------------------------------------------------------
# Figure checks
# ---------------------------------------------------------------------------------------------------------------
def spec(sid):
    with open(os.path.join(SPECS, sid + '.json'), encoding='utf-8') as fh:
        sp = json.load(fh)
    # a no-break space (BC-S12) reads as a space in every check
    sp = json.loads(json.dumps(sp, ensure_ascii=False).replace('\u00a0', ' '))
    words = [sp.get('title', ''), sp.get('measure_line', ''), sp.get('reading_guide', ''), sp.get('alt', '')] + sp.get('notes', []) + sp.get('chart_notes', [])
    return sp, ' '.join(words)


def mil(v, nd=1):
    return ('{:,.%df}' % nd).format(round(v / 1e6 + 1e-12, nd))


def figures():
    bad = []

    def want(sid, text, piece, why):
        if piece not in text:
            bad.append('%s: "%s" missing (%s)' % (sid, piece, why))

    def same(sid, a, b, why):
        if a != b:
            bad.append('%s: %r is not %r (%s)' % (sid, a, b, why))

    # S65: the funnel's stages from one base, and the outcomes file's twelve months
    sp, t = spec('s65')
    fu = {r['stage_id']: int(r['people']) for r in read('cms-medicaid-chip-renewal-funnel')}
    oc = [r for r in read('cms-medicaid-chip-renewal-outcomes') if '2023-04' <= r['month'] <= '2024-03']
    same('S65', len(oc), 12, 'twelve months, April 2023 to March 2024')
    for k, col in (('due', 'due'), ('pending', 'pending'), ('ended_procedural', 'ended_procedural'), ('ended_ineligible', 'ended_ineligible'), ('kept', 'renewed')):
        same('S65', fu[k], sum(int(r[col]) for r in oc), 'stage %s against the months' % k)
    same('S65', fu['decided'], fu['due'] - fu['pending'], 'decided is due less pending')
    same('S65', fu['not_ended_procedural'], fu['decided'] - fu['ended_procedural'], 'nests')
    same('S65', fu['kept'], fu['not_ended_procedural'] - fu['ended_ineligible'], 'nests')
    for k in ('due', 'decided', 'not_ended_procedural', 'kept', 'ended_procedural', 'ended_ineligible', 'pending'):
        want('S65', t, mil(fu[k]) + ' million', k)
    want('S65', sp['title'], 'Of %s million Medicaid and CHIP renewals due April 2023 to March 2024, states ended %s million for a procedural reason, over twice the %s million they found ineligible' % (mil(fu['due']), mil(fu['ended_procedural']), mil(fu['ended_ineligible'])), 'title (MB-1, BC-S9, the editor\'s second pass)')
    for piece in ('terminated for a procedural or administrative reason', 'determined ineligible'):
        same('S65', piece in ' '.join(meta('cms-medicaid-chip-renewal-funnel')['notes'] + [meta('cms-medicaid-chip-renewal-funnel')['qualification']]), True, 'CMS term in the sidecar: ' + piece)
        want('S65', t, piece, 'note 1 quotes CMS (BC-S9)')
    sn = ' '.join(meta('cms-medicaid-chip-renewal-funnel')['notes'])
    for piece in ('terminated for failure to submit the renewal form or necessary information', 'did not respond to the State’s request for additional information', 'No record read says how many people ended for a procedural reason were still eligible'):
        same('S65', piece in sn, True, 'the sidecar quotes the rules (BC-S9): ' + piece)
    want('S65', t, 'a renewal form or the information it asked for does not come back, and the record does not say how many of those people were still eligible', 'note 1, the procedural reason in the rules\' terms (BC-S9)')
    same('S65', 2 < fu['ended_procedural'] / fu['ended_ineligible'] < 3, True, 'more than twice (2.30)')
    want('S65', sp['measure_line'], 'shares are of renewals due', 'MB-2')
    same('S65', sp['labels']['named'], ['ended_procedural'], 'the named loss')

    # S73: every joint fundraising committee of both nominees (BC-M1, D3-1330), line 22 alone drawn (RL-3a), folded by kind
    sp, t = spec('s73')
    rows = read('fec-jfc-transfers-2024-all-committees')
    nodes = read('fec-jfc-transfers-2024-by-node')
    key = lambda r: (r['jfc_id'], r['recipient_id'], r['amount_lines'], r['amount'])
    same('S73', sorted(key(r) for r in nodes), sorted(key(r) for r in rows), 'the node file keeps every row of the seven funds')
    same('S73', all(r[k] == n[k] for r, n in zip(sorted(rows, key=key), sorted(nodes, key=key)) for k in rows[0]), True, 'every carried column equal')
    tot = lambda rs: round(sum(float(r['amount']) for r in rs), 2)
    funds = {n: sorted({r['jfc_name'] for r in rows if r['nominee'] == n}) for n in ('Kamala D. Harris', 'Donald J. Trump')}
    same('S73', (len(funds['Kamala D. Harris']), len(funds['Donald J. Trump'])), (3, 4), 'three funds and four')
    words = sp['table']['group']['columns'][0]['words']
    same('S73', sorted(words), sorted(funds['Kamala D. Harris'] + funds['Donald J. Trump']), 'From names every fund')
    for f in words:
        want('S73', sp['notes'][0], words[f], 'note 1 names ' + f)
    l22 = [r for r in rows if r['amount_lines'] == '22']
    refunds = [r for r in rows if r['amount_lines'] == '28C']
    same('S73', len(l22) + len(refunds), len(rows), 'every row is line 22 or a line 28C refund')
    alt = {}
    for nom, short, camp, nat, nst, noth in (('Kamala D. Harris', 'Harris', 'the Harris campaign', 'the Democratic National Committee', 51, 1), ('Donald J. Trump', 'Trump', 'the Trump campaign', 'the Republican National Committee', 50, 4)):
        mine = [r for r in l22 if r['nominee'] == nom]
        n_all = len({r['recipient_id'] for r in mine})
        by = lambda k: [r for r in mine if r['recipient_kind'] == k]
        dist = lambda k: len({r['recipient_id'] for r in by(k)})
        same('S73', (dist('nominee campaign'), dist('national party committee'), dist('state party committee'), dist('other committee')), (1, 1, nst, noth), nom + ': committees by kind')
        # the title is the editor's (ST2-M1): it must give each side's sum and count of committees, and own no fund as a nominee's
        want('S73', sp['title'], '$%s million to %d' % (mil(tot(mine)), n_all), nom + ': title, sum and committees')
        party = 'Democratic' if short == 'Harris' else 'Republican'
        want('S73', sp['labels']['sources'][nom], '%s joint fundraising committees that paid the %s presidential campaign, {total} in all' % ('Three' if short == 'Harris' else 'Four', party), nom + ': bar head by the rule (ST2-M1)')
        oth = tot(by('other committee'))
        oth_words = '$%s' % '{:,.0f}'.format(oth) if oth < 1e6 else '$%s million' % mil(oth)
        want('S73', sp['alt'], 'The %s that paid the %s campaign, whose candidate was %s, sent $%s million to the campaign, $%s million to %s, $%s million to %d state party committees and %s to %s other committee%s, $%s million in all' % (
            'three' if short == 'Harris' else 'four', party, 'Joseph R. Biden Jr. until July 21, 2024, then Kamala D. Harris' if short == 'Harris' else 'Donald J. Trump', mil(tot(by('nominee campaign'))), mil(tot(by('national party committee'))), nat, mil(tot(by('state party committee'))), nst,
            oth_words, 'one' if noth == 1 else 'four', '' if noth == 1 else 's', mil(tot(mine))), nom + ': alt')
        b21 = [r for r in rows if r['nominee'] == nom and float(r['line_21b_amount'] or 0) > 0]
        same('S73', all(r['amount_lines'] == '22' for r in b21), True, nom + ': line 21B only to committees drawn')
        want('S73', t, ('the Democratic funds also paid committees drawn here $%s million for operating expenses (line 21B)' if short == 'Harris' else 'and the Republican funds $%s million, which the chart leaves out') % mil(sum(float(r['line_21b_amount']) for r in b21)), nom + ': line 21B')
        rf = [r for r in refunds if r['nominee'] == nom]
        alt[nom] = (len(rf), tot(rf))
        sts = {r['recipient_state'] for r in by('state party committee')}
        same('S73', ('DC' in sts, 'GU' in sts), (True, short == 'Trump'), nom + ': DC among the state parties, and Guam for Trump')
    same('S73', (alt['Kamala D. Harris'], alt['Donald J. Trump']), ((2, 81000.0), (4, 4000.0)), 'refunds')
    want('S73', t, 'The Democratic funds refunded $81,000 to two committees that had given to them, and the Republican funds $4,000 to four (line 28C)', 'note 4, refunds')
    same('S73', len({r['recipient_state'] for r in l22 if r['nominee'] == 'Donald J. Trump' and r['recipient_kind'] == 'state party committee'} - {'DC', 'GU'}), 48, 'Trump: 48 states')
    want('S73', t, 'The Democratic funds paid the state party committees of the 50 states and the District of Columbia, and the Republican funds those of 48 states, the District of Columbia and Guam', 'note 3')
    mine_words = ' '.join(sp['notes'] + sp.get('chart_notes', []) + [sp['alt'], sp['table']['caption']] + list(sp['labels']['sources'].values()))
    same('S73', [w for w in ('Harris’s', 'Trump’s', 'nominee’s') if w in mine_words], [], 'no nominee\'s possessive over the funds in the drawing, notes, alt and caption (ST2-M1)')
    same('S73', [w for w in ('Harris’s', 'Trump’s', 'nominee’s') if w in sp['title'] + ' ' + sp['measure_line']], [], 'no nominee\'s possessive over the funds in the title and measure line (ST2-M1, the editor\'s words)')
    same('S73', sp['labels']['sub'], {'Kamala D. Harris': 'Joseph R. Biden Jr. until July 21, 2024, then Kamala D. Harris', 'Donald J. Trump': 'Donald J. Trump'}, 'the campaigns\' candidates under each bar (ST2-M1)')
    names = sorted({r['recipient_name_2024_election'] for r in nodes if r['recipient_kind'] == 'other committee' or r['amount_lines'] == '28C'})
    tc = dict(sp['typography']['replace'])
    same('S73', sorted(tc), names, 'every capitals name the table prints has its title-case words (RS-3)')
    same('S73', all(tc[k].upper() == k for k in tc), True, 'the title-case words spell the stored names (RS-3)')
    same('S73', sp['labels']['unit'], 4000000, 'unit')
    want('S73', t, 'and the agreement that formed a fund sets how many committees it pays', 'note 2 (ST-S6)')
    # ST2-M1: the Democratic funds' line 22 before July 21, 2024 and from that day, by kind, from the research lead's split
    dem = [r for r in l22 if r['nominee'] == 'Kamala D. Harris']
    bef = lambda k: round(sum(float(r['amount_before_2024_07_21'] or 0) for r in dem if r['recipient_kind'] == k), 2)
    aft = lambda k: round(sum(float(r['amount']) - float(r['amount_before_2024_07_21'] or 0) for r in dem if r['recipient_kind'] == k), 2)
    cnt = lambda k, before: len({r['recipient_id'] for r in dem if r['recipient_kind'] == k and ((float(r['amount_before_2024_07_21'] or 0) > 0) if before else (float(r['amount']) - float(r['amount_before_2024_07_21'] or 0) > 0.004))})
    same('S73', (bef('nominee campaign'), bef('national party committee'), bef('state party committee'), bef('other committee')), (161426350.0, 85750000.0, 68058500.0, 29350.0), 'Democratic funds before July 21, 2024')
    same('S73', (aft('nominee campaign'), aft('national party committee'), aft('state party committee'), aft('other committee')), (372239915.32, 155095000.0, 113330624.21, 9290.21), 'Democratic funds from July 21, 2024')
    same('S73', (cnt('state party committee', True), cnt('state party committee', False), cnt('other committee', True), cnt('other committee', False)), (50, 51, 1, 1), 'state parties and other committee before and after')
    want('S73', t, 'Before that day the three funds sent the campaign $%s million, the Democratic National Committee $%s million, %d state party committees $%s million and one other committee $%s; from that day on, $%s million, $%s million, $%s million to %d and $%s' % (
        mil(bef('nominee campaign')), mil(bef('national party committee')), cnt('state party committee', True), mil(bef('state party committee')), '{:,.0f}'.format(bef('other committee')),
        mil(aft('nominee campaign')), mil(aft('national party committee')), mil(aft('state party committee')), cnt('state party committee', False), '{:,.0f}'.format(aft('other committee'))), 'the July 21 note (ST2-M1)')
    names = ' '.join(meta('fec-jfc-transfers-2024-all-committees')['notes'])
    for piece in ('“Biden for President” (on file 2022-08-30) then “Harris for President” (filed as a new name 2024-07-21)', '“Biden Victory Fund” (on file 2022-07-01) then “Harris Victory Fund” (filed as a new name 2024-07-21)', '“Biden Action Fund”', '“Biden Baldwin Victory Fund”'):
        same('S73', piece in names, True, 'the sidecar records the July 21, 2024 names: ' + piece[:40])
    want('S73', t, 'On July 21, 2024, the Democratic campaign committee and its three funds filed new names', 'the July 21 note, the names')
    for piece in ('C00867937, “2024 RNC VICTORY” (first filed 2024-01-31) then “TRUMP 47 COMMITTEE” (filed as a new name 2024-03-14) then “TRUMP 47 COMMITTEE, INC.”', 'C00873893, “TRUMP NATIONAL COMMITTEE JFC” (first filed 2024-03-20) then “TRUMP NATIONAL COMMITTEE JFC, INC.”', 'C00770941, “TRUMP SAVE AMERICA JOINT FUNDRAISING COMMITTEE” (on file 2022-12-05);', 'C00855114, “TRUMP BILIRAKIS VICTORY FUND” (first filed 2023-10-30)', 'C00828541, “DONALD J. TRUMP FOR PRESIDENT 2024, INC.” (filed as a new name 2022-12-05) then “NEVER SURRENDER, INC.” (filed as a new name 2024-11-12)'):
        same('S73', piece in names, True, 'the Republican names in the cycle: ' + piece[:30])
    want('S73', t, 'The Republican campaign kept one candidate through the cycle, so its funds are not split; the Trump 47 Committee was named 2024 RNC Victory until March 14, 2024', 'the Republican side, one test (ST2-M1 point 3)')
    same('S73', 'two, both from the Trump National Committee JFC on December 11, 2024' in names and '$19,128,807.19 in all, inside the drawn amount' in names, True, 'drawn payments after the November 12, 2024 rename (the research lead\'s check)')
    want('S73', t, 'and the campaign committee took the name Never Surrender, Inc. on November 12, 2024', 'the November 12 rename, named once (D3-1509)')
    same('S73', sp['source_line'], meta('fec-jfc-transfers-2024-all-committees')['source_line_variants']['with_form_1'], 'the source line is the with_form_1 variant, as stored')
    same('S73', any(w in sp['title'] for w in ('53', 'to two')), False, 'the title sets no one fund\'s reach against another\'s (BC-M1)')
    n22 = [r for r in nodes if r['amount_lines'] == '22']
    nk = lambda r: r['node'] + ' (' + r['nominee'] + ')'
    under = sorted(n for n in {nk(r) for r in n22} if sum(float(r['amount']) for r in n22 if nk(r) == n) < sp['labels']['unit'])
    same('S73', under, ['1 other committee (Kamala D. Harris)'], 'the one link under a pixel, keyed as a hairline')
    want('S73', t, 'a link under $4 million shows as a hairline', 'chart note, hairline')

    # S74: the region matrix against the 118 links
    sp, t = spec('s74')
    mx = read_json('v7-region-connection-matrix')
    lk = read_json('v7-links-with-regions')
    same('S74', len(lk), 118, 'connections')
    same('S74', sum(r['links'] for r in mx), 118, 'the matrix sums to the links')
    filled = [r for r in mx if r['links']]
    same('S74', (len(filled), len(mx)), (44, 100), 'cells filled')
    diag = sum(r['links'] for r in mx if r['from_region'] == r['to_region'])
    want('S74', sp['title'], '118 connections fill 44 of the 100 pairs of its ten regions, and %d of the connections stay within one region' % diag, 'title')
    out_d = {}
    in_d = {}
    for r in mx:
        out_d[r['from_region']] = out_d.get(r['from_region'], 0) + r['links']
        in_d[r['to_region']] = in_d.get(r['to_region'], 0) + r['links']
    top = max(out_d, key=out_d.get)
    same('S74', (top, out_d[top], sorted(out_d.values())[-2] < out_d[top]), ('D', 23, True), 'governing institutions starts the most')
    want('S74', t, 'Governing institutions starts 23, the most, among them all seven lines of authority', 'alt')
    auth = [r for r in lk if r['type'] == 'authority']
    same('S74', (len(auth), sorted(set(r['from_region'] for r in auth)), len([r for r in mx if r['no_sign']]), all(r['no_sign'] in (0, r['links']) for r in mx)), (7, ['D'], 3, True), 'authority: seven, all from D, three cells alone')
    same('S74', sum(r['no_sign'] for r in mx), 7, 'no-sign count in the matrix')
    same('S74', in_d.get('X', 0), 0, 'outside drivers receives none')
    same('S74', (min(r['links'] for r in filled), max(r['links'] for r in filled)), (1, 7), 'counts run 1 to 7')
    names = {r['id']: r['name'] for r in lk}
    same('S74', (names['LE02'], names['LE19']), ('Congress decides public investment levels', 'The executive sets tariff rates'), 'the two examples')
    same('S74', sp['v7']['ids'], [], 'no ID prints, so v7.ids is empty; the CSV export carries link_ids')
    same('S74', sorted(sum([r['link_ids'].split('; ') for r in filled], [])), sorted(r['id'] for r in lk), 'every connection ID in a cell of the export')
    steps = sp['labels']['steps']
    same('S74', [(s['min'], s['max'], s['fill']) for s in steps], [(1, 1, 'seq-1'), (2, 3, 'seq-3'), (4, 5, 'seq-4'), (6, 7, 'seq-5')], 'ruling (b) steps')

    # S75: the House bills and their shared backers
    sp, t = spec('s75')
    bills = read('congress-gov-pbm-bills-119')
    hr = sorted([b for b in bills if b['bill_type'] == 'HR'], key=lambda b: (b['introduced'], int(b['number'])))
    se = [b for b in bills if b['bill_type'] == 'S']
    same('S75', (len(hr), len(se)), (10, 8), 'chambers')
    want('S75', t, '10 House bills and eight Senate bills', 'note 1')
    want('S75', t, "The Senate’s eight are " + ', '.join(b['bill'] for b in se[:-1]) + ' and ' + se[-1]['bill'], 'note 2')
    same('S75', sp['labels']['order'], [b['bill'] for b in hr], 'the line in order of introduction')
    want('S75', sp['measure_line'], 'February 4, 2025 to September 14, 2026', 'span')
    same('S75', (hr[0]['introduced'], hr[-1]['introduced']), ('2025-02-04', '2026-09-14'), 'first and last introduced')
    pairs = read('congress-gov-pbm-bill-shared-backers-119')
    same('S75', len(pairs), 33, 'pairs')
    pairs.sort(key=lambda p: -int(p['shared_backers']))
    p0 = pairs[0]
    same('S75', (p0['bill_a'], p0['bill_b'], int(p0['shared_backers']), int(pairs[1]['shared_backers']) < int(p0['shared_backers'])), ('H.R. 6609', 'H.R. 6610', 34, True), 'the top pair')
    want('S75', sp['title'], 'Of 10 House bills whose titles name pharmacy benefit managers, H.R. 6609 and H.R. 6610 shared the most backers, 34 members', 'title')
    intro = {b['bill']: b['introduced'] for b in hr}
    same('S75', intro['H.R. 6609'] == intro['H.R. 6610'], True, 'introduced the same day')
    p4317 = {(p['bill_a'], p['bill_b']): int(p['shared_backers']) for p in pairs}
    same('S75', (p4317[('H.R. 4317', 'H.R. 6609')], p4317[('H.R. 4317', 'H.R. 6610')]), (19, 19), 'H.R. 4317 with each')
    others = [int(p['shared_backers']) for p in pairs[3:]]
    same('S75', (len(others), min(others), max(others)), (30, 1, 6), 'the other 30 pairs')
    same('S75', all(b['became_law'] == '' for b in bills), True, 'no bill in the file shows a public law')

    # S76: money in and out of one node
    sp, t = spec('s76')
    mo = {r['line_id']: (r['side'], float(r['dollars'])) for r in read('fec-house-campaigns-2024-money-in-out')}
    ins = {k: v for k, (s, v) in mo.items() if s == 'in'}
    outs = {k: v for k, (s, v) in mo.items() if s == 'out'}
    big = max((k for k in ins if k != 'cash_start'), key=ins.get)
    same('S76', big, 'individuals', 'the largest receipt line')
    took = sum(v for k, v in ins.items() if k != 'cash_start')
    same('S76', round(took, 2), 2271178361.46, 'receipts, cash at the start left out (transfers netted candidate by candidate, ST-S2)')
    same('S76', round(1000 * ins['individuals'] / took), 609, 'individuals, 60.9 percent of all they took in')
    want('S76', sp['title'], 'Individuals gave 2024 House campaigns $%s million, more than any other source and %d percent of all they took in' % (mil(ins['individuals']), round(100 * ins['individuals'] / took)), 'title (MB-4)')
    same('S76', (round(sum(ins.values()), 2), round(sum(outs.values()), 2)), (2626481617.75, 2624948459.72), 'money in and out (ST-S2)')
    rem = round(sum(ins.values()) - sum(outs.values()), 2)
    same('S76', rem, 1533158.03, 'remainder')
    want('S76', t, '$%s million unaccounted for, %s percent of the money in' % (mil(rem), '{:.3f}'.format(100 * rem / sum(ins.values()))), 'note 2')
    # ST-S2: transfers netted candidate by candidate, each candidate's net on its own side; the remainder by campaign
    cands = read('fec-house-campaigns-2024-by-candidate')
    want('S76', t, 'all {:,} House candidates'.format(len(cands)), 'candidates')
    z = lambda v: num(v) or 0.0
    nets = [z(r['trans_from_auth']) - z(r['trans_to_auth']) for r in cands]
    same('S76', (round(sum(x for x in nets if x > 0), 2), sum(1 for x in nets if x > 0)), (round(ins['transfers_in_net'], 2), 436), 'transfers in, net per candidate')
    same('S76', (round(-sum(x for x in nets if x < 0), 2), sum(1 for x in nets if x < 0)), (round(outs['transfers_out_net'], 2), 84), 'transfers out, net per candidate')
    gaps = [(r['cand_id'], round(z(r['coh_bop']) + z(r['ttl_receipts']) - z(r['ttl_disb']) - z(r['coh_cop']), 2)) for r in cands]
    gaps = [g for g in gaps if g[1] != 0]
    top = max(gaps, key=lambda g: abs(g[1]))
    same('S76', (len(gaps), round(sum(g[1] for g in gaps), 2), top), (297, 1533158.03, ('H4IN05195', 1500000.0)), 'campaigns that do not balance, and the one that leaves nearly all of it')
    same('S76', round(100 * top[1] / rem, 1), 97.8, 'one campaign\'s share of the remainder')
    same('S76', (round(ins['transfers_in_net'], 2), round(outs['transfers_out_net'], 2)), (175103772.47, 18313248.58), 'the derived file\'s transfer lines')
    rnote = ' '.join(meta('fec-house-campaigns-2024-money-in-out')['notes'])
    for piece in ('297 of the 1,926 campaigns do not balance', 'leaves $1,500,000.00, 97.8 percent of the net remainder'):
        same('S76', piece in rnote, True, 'the sidecar holds: ' + piece)
    want('S76', t, 'The figures for 297 of the {:,} campaigns do not balance'.format(len(cands)), 'note 2, campaigns that do not balance')
    want('S76', t, 'one campaign’s reports leave nearly all of it', 'note 2, $1,500,000.00 of $1,533,158.03 (97.8 percent)')
    same('S76', 'transfers_out_net' in sp['labels']['names'], True, 'the out line has a name')
    for k in ('cash_start', 'individuals', 'other_committees', 'candidate_loans', 'cash_end'):
        want('S76', sp['alt'], '$%s million' % mil(ins.get(k, outs.get(k))), 'alt ' + k)
    same('S76', sp['labels']['named'], ['individuals'], 'named flow')

    # S77: the rule's limits
    sp, t = spec('s77')
    st = {r['order']: r for r in read('govinfo-snap-application-path')}
    same('S77', (st['4']['time_limit'], st['5']['time_limit'], st['3']['time_limit'], st['1']['time_limit'], st['2']['time_limit']), ('30 calendar days', '7 calendar days', 'At least 10 days', 'Same day', ''), 'limits as the file holds them')
    want('S77', sp['title'], 'at most 30 days from an application to a decision, and seven for a household with very little income or cash', 'title (the editor\'s second pass)')
    want('S77', t, 'at least 10 days', 'proof')
    lim = sp['labels']['limits']
    same('S77', (lim['4'], lim['5'], lim['3'], lim['1']), ('Within 30 days of filing, the rule’s limit', 'Interview and benefits within 7 days of filing, the rule’s limit', 'At least 10 days to send it', 'Taken the same day'), 'step words against the limits')
    same('S77', 'miss the limits' in t, False, 'no claim on measured waits (BC-S13)')
    want('S77', sp['grade_line'], 'November 9, 2026', 'in force')
    same('S77', st['5']['next_step'], 'Postponed proof, due by the second or third month of benefits', 'the branch goes on (273.2(i)(4)(iii)(A))')
    want('S77', t, 'interviews a household on the expedited branch within the seven days', 'the expedited interview (273.2(i)(3)(iii))')
    want('S77', t, 'second or third month of benefits', 'postponed proof')
    rule = meta('govinfo-snap-application-path')['notes'][0]
    for piece in ('less than $150 in monthly gross income', 'do not exceed $100', 'Migrant or seasonal farmworker households who are destitute', 'combined monthly gross income and liquid resources are less than the household\'s monthly rent or mortgage, and utilities'):
        same('S77', piece in rule, True, 'the quoted rule holds: ' + piece)
    want('S77', t, 'under $150 in monthly gross income and no more than $100 in cash and other liquid resources', 'expedited test (i)')
    want('S77', t, 'a destitute migrant or seasonal farmworker household with no more than $100', 'expedited test (ii)')
    want('S77', t, 'monthly gross income and liquid resources together fall short of its monthly rent or mortgage and utilities', 'expedited test (iii)')

    for f in bad:
        print('FAULT ' + f)
    print('figures: %d faults' % len(bad))
    return len(bad)


if __name__ == '__main__':
    if '--figures' in sys.argv:
        sys.exit(1 if figures() else 0)
    snap_path()
    jfc_nodes()
    if FAULTS:
        print('\n'.join('FAULT ' + f for f in FAULTS))
        sys.exit(1)
    print('0 faults' if CHECK else 'done')
