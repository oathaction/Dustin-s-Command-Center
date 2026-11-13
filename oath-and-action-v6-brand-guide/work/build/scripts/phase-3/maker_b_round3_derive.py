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
    src = 'fec-jfc-transfers-2024'
    m = meta(src)
    rows = read(src)
    states = [r for r in rows if r['jfc_name'] == 'HARRIS VICTORY FUND' and r['amount_lines'] == '22' and r['recipient_type'] == 'Party - Qualified' and r['recipient_id'] != 'C00010603']
    named = {'C00703975': (1, 'Harris for President, the campaign'), 'C00010603': (2, 'Democratic National Committee'),
             'C00828541': (4, 'Donald J. Trump for President 2024, the campaign'), 'C00003418': (5, 'Republican National Committee')}
    out = []
    for r in rows:
        if r['amount_lines'] == '28C':
            o, nd = 6, r['recipient_name_2024_election'] + ', a refund of its own contribution, not drawn'
        elif r['recipient_id'] in named:
            o, nd = named[r['recipient_id']]
        elif r in states:
            o, nd = 3, '%d state party committees, the District of Columbia’s included' % len(states)
        else:
            FAULTS.append('S73: a line 22 row the drawing does not fold: ' + r['recipient_id'])
            continue
        out.append(dict(r, node_order=str(o), node=nd))
    out.sort(key=lambda r: (int(r['node_order']), -float(r['amount'])))
    cols = list(rows[0].keys()) + ['node_order', 'node']
    side = dict(m)
    side.pop('source_line_variants', None)
    side.update({
        'file': 'fec-jfc-transfers-2024-by-node.csv',
        'kind': 'derived',
        'title_or_table': m['title_or_table'] + ', each payment with the node the network diagram draws it in',
        'columns': dict(m['columns'], node_order={'type': 'integer', 'description': 'the order of the node in the drawing; 6 for a refund, which does not draw'},
                        node={'type': 'text', 'description': 'the node the drawing folds the payment into, or the refund it is, in words'}),
        'printed_source_line': m['source_line_variants']['transfers_and_refunds'],
        'derived_from': [src + '.csv'],
        'derivation': 'The rows of ' + src + ' unchanged, with two columns added: node names the node the network diagram draws each line 22 payment in (each nominee’s campaign and national party committee alone, and the Harris Victory Fund’s 51 state party committees, DC’s included, as one node), or marks a line 28C refund, which does not draw; node_order orders the nodes. Rows sorted by node, then by amount, largest first.',
    })
    write('fec-jfc-transfers-2024-by-node', cols, out, side)


# ---------------------------------------------------------------------------------------------------------------
# Figure checks
# ---------------------------------------------------------------------------------------------------------------
def spec(sid):
    with open(os.path.join(SPECS, sid + '.json'), encoding='utf-8') as fh:
        sp = json.load(fh)
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
    want('S65', sp['title'], 'Of %s million Medicaid and CHIP renewals due from April 2023 to March 2024, %s million ended for a procedural reason, more than twice the %s million found ineligible' % (mil(fu['due']), mil(fu['ended_procedural']), mil(fu['ended_ineligible'])), 'title (MB-1)')
    same('S65', 2 < fu['ended_procedural'] / fu['ended_ineligible'] < 3, True, 'more than twice (2.30)')
    want('S65', sp['measure_line'], 'shares are of renewals due', 'MB-2')
    same('S65', sp['labels']['named'], ['ended_procedural'], 'the named loss')

    # S73: both joint fundraising committees, line 22 alone drawn (ruling RL-3a), folded as the drawing folds them
    sp, t = spec('s73')
    rows = read('fec-jfc-transfers-2024')
    nodes = read('fec-jfc-transfers-2024-by-node')
    same('S73', sorted((r['recipient_id'], r['amount']) for r in nodes), sorted((r['recipient_id'], r['amount']) for r in rows), 'the node file keeps every row')
    same('S73', sorted(set(r['node'] for r in nodes if r['amount_lines'] == '22')), sorted(['Harris for President, the campaign', 'Democratic National Committee', '51 state party committees, the District of Columbia’s included', 'Donald J. Trump for President 2024, the campaign', 'Republican National Committee']), 'the table groups as the drawing folds')
    hv = [r for r in rows if r['jfc_name'] == 'HARRIS VICTORY FUND' and r['amount_lines'] == '22']
    tn = [r for r in rows if r['jfc_name'] == 'TRUMP NATIONAL COMMITTEE JFC, INC.' and r['amount_lines'] == '22']
    refunds = [r for r in rows if r['amount_lines'] == '28C']
    same('S73', len(hv) + len(tn) + len(refunds), len(rows), 'every row is line 22 or a line 28C refund')
    tot = lambda rs: round(sum(float(r['amount']) for r in rs), 2)
    same('S73', (len(hv), tot(hv), len(tn), tot(tn)), (53, 899402049.70, 2, 273762296.73), 'line 22 sums')
    same('S73', (len(refunds), tot(refunds), {r['jfc_name'] for r in refunds}), (2, 81000.0, {'HARRIS VICTORY FUND'}), 'refunds')
    want('S73', sp['title'], 'The Harris Victory Fund sent $%s million to %d committees in the 2024 cycle, and the Trump National Committee JFC sent $%s million to two' % (mil(tot(hv)), len(hv), mil(tot(tn))), 'title')
    camp = [r for r in hv if r['recipient_id'] == 'C00703975']
    dnc = [r for r in hv if r['recipient_id'] == 'C00010603']
    states = [r for r in hv if r['recipient_type'] == 'Party - Qualified' and r['recipient_id'] != 'C00010603']
    same('S73', (len(camp), len(dnc), len(states), len(hv) - len(camp) - len(dnc) - len(states)), (1, 1, 51, 0), 'Harris folds')
    same('S73', 'DC' in [r['recipient_state'] for r in states], True, 'the District of Columbia among the 51')
    want('S73', t, '$%s million to the Harris campaign, $%s million to the Democratic National Committee and $%s million to 51 state party committees, $%s million in all' % (mil(tot(camp)), mil(tot(dnc)), mil(tot(states)), mil(tot(hv))), 'alt, Harris')
    tc = [r for r in tn if r['recipient_id'] == 'C00828541']
    rnc = [r for r in tn if r['recipient_id'] == 'C00003418']
    want('S73', t, '$%s million to the Trump campaign and $%s million to the Republican National Committee' % (mil(tot(tc)), mil(tot(rnc))), 'alt, Trump')
    b21 = [r for r in rows if float(r['line_21b_amount'] or 0) > 0]
    same('S73', (len(b21), round(sum(float(r['line_21b_amount']) for r in b21), 2), {r['jfc_name'] for r in b21}), (3, 27141702.01, {'HARRIS VICTORY FUND'}), 'line 21B')
    same('S73', all(r in hv for r in b21), True, 'line 21B only to drawn committees')
    want('S73', t, 'paid three of the committees drawn $%s million for operating expenses (line 21B), $%s million of it to the campaign and $%s million to the Democratic National Committee, and refunded $%s to two committees' % (mil(sum(float(r['line_21b_amount']) for r in b21)), mil(float(camp[0]['line_21b_amount'])), mil(float(dnc[0]['line_21b_amount'])), '{:,.0f}'.format(tot(refunds))), 'note 3')
    note = json.loads(meta('fec-jfc-transfers-2024')['notes'][0])
    for nominee, campaign_words, drawn in (('Kamala D. Harris', 'Harris', camp), ('Donald J. Trump', 'Trump', tc)):
        nt = note[nominee]
        same('S73', round(nt['to_campaign'], 2), tot(drawn), nominee + ': the committee drawn sent the most')
        same('S73', all(o[1] < nt['to_campaign'] for o in nt['other_jfcs']), True, nominee + ': the rule picks the largest')
        want('S73', t, 'the %s campaign $%s million' % (campaign_words, mil(sum(o[1] for o in nt['other_jfcs']))), nominee + ': other committees')
    same('S73', sp['labels']['unit'], 4000000, 'unit')
    same('S73', min(tot(rnc), tot(states), tot(dnc)) > sp['labels']['unit'], True, 'every drawn link is wider than a pixel')

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
    same('S76', round(took, 2), 2252865112.88, 'receipts, cash at the start left out')
    want('S76', sp['title'], 'Individuals gave 2024 House campaigns $%s million, more than any other source and %d percent of all they took in' % (mil(ins['individuals']), round(100 * ins['individuals'] / took)), 'title (MB-4)')
    rem = round(sum(ins.values()) - sum(outs.values()), 2)
    same('S76', rem, 1533158.03, 'remainder')
    want('S76', t, 'The reports leave $%s million unaccounted for, %s percent of the money in' % (mil(rem), '{:.3f}'.format(100 * rem / sum(ins.values()))), 'note 2')
    same('S76', outs['transfers_out_net'], 0.0, 'transfers out')
    cands = read('fec-house-campaigns-2024-by-candidate')
    want('S76', t, 'all {:,} House candidates'.format(len(cands)), 'candidates')
    for k in ('cash_start', 'individuals', 'other_committees', 'candidate_loans', 'cash_end'):
        want('S76', sp['alt'], '$%s million' % mil(ins.get(k, outs.get(k))), 'alt ' + k)
    same('S76', sp['labels']['named'], ['individuals'], 'named flow')

    # S77: the rule's limits
    sp, t = spec('s77')
    st = {r['order']: r for r in read('govinfo-snap-application-path')}
    same('S77', (st['4']['time_limit'], st['5']['time_limit'], st['3']['time_limit'], st['1']['time_limit'], st['2']['time_limit']), ('30 calendar days', '7 calendar days', 'At least 10 days', 'Same day', ''), 'limits as the file holds them')
    want('S77', sp['title'], 'at most 30 days from an application to a decision, and at most seven days for a household with very little income or cash', 'title')
    want('S77', t, 'at least 10 days', 'proof')
    lim = sp['labels']['limits']
    same('S77', (lim['4'], lim['5'], lim['3'], lim['1']), ('within 30 days of filing, the rule’s limit', 'interview and benefits within 7 days of filing, the rule’s limit', 'at least 10 days to send it', 'taken the same day'), 'step words against the limits')
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
