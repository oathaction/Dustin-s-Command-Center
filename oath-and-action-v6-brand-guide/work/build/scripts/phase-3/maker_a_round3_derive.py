"""Maker A, Phase 3 round 3: R2-2's derived table for S71, and the figure checks for S66 to S72 (contract C1).

    python3 -I work/build/scripts/phase-3/maker_a_round3_derive.py [--check] [--figures]

Writes one derived table with its sidecar in work/build/data/:

- usgov-v7-route-grid: the atlas's eleven routes to change (v7-routes: name, who acts, instrument and the count of
  reform profiles that list each route), joined by route code to what the official texts require of each route
  (usgov-route-requirements: who decides, what it takes, how it can be undone, the texts and one address), with the
  date each route's texts were read, from the workflow sources file (FS, SS, BI and LOC on November 11, 2026; the
  other seven on November 12, 2026, as its sections say). Rows keep the atlas's order. No value is changed.

--check writes nothing and fails when a written file differs from what the script computes now. --figures writes
nothing and checks every figure in the titles, notes, alts and labels of specs S66 to S72 against the data files,
each check named in the spec's notes_internal (check S66 to check S72). Standard library only.
"""
import csv
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
BASE = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data'))
SPECS = os.path.normpath(os.path.join(HERE, '..', '..', 'chart-kit', 'specs'))
WORKFLOW = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'research', '20261111_Policy-Workflow-Sources.md'))
CHECK = '--check' in sys.argv
FIGS = '--figures' in sys.argv
FAULTS = []


def read_csv(name):
    with open(os.path.join(DATA, name + '.csv'), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def read_json(name):
    with open(os.path.join(DATA, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)['rows']


def meta(name):
    with open(os.path.join(DATA, name + '.meta.json'), encoding='utf-8') as fh:
        return json.load(fh)


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
        elif not FIGS:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(body)


# ---- the route grid ------------------------------------------------------------------------------------------------
def route_dates():
    """Each route's reading date, from the workflow sources file: the date a section's rows give, else its intro's."""
    text = open(WORKFLOW, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'^## ([A-Z]{2,3})\. [^\n]*\n(.*?)(?=^## |\Z)', text, re.S | re.M):
        dates = sorted(set(re.findall(r'\|\s*(2026-11-\d\d)\s*\|', m.group(2))))
        out[m.group(1)] = dates
    return out


def grid():
    v7 = read_json('v7-routes')
    req = {r['route']: r for r in read_csv('usgov-route-requirements')}
    dates = route_dates()
    words = {'2026-11-11': 'November 11, 2026', '2026-11-12': 'November 12, 2026'}
    rows = []
    for r in v7:
        q = req[r['route']]
        if q['name'] != r['name']:
            FAULTS.append('route %s: names differ (%s, %s)' % (r['route'], r['name'], q['name']))
        ds = dates.get(r['route']) or []
        if not ds:
            FAULTS.append('route %s: no reading date in the workflow sources file' % r['route'])
        rows.append({
            'route': r['route'], 'name': r['name'], 'v7_who': r['who'], 'v7_instrument': r['instrument'],
            'route_entries': str(r['route_entries']), 'who_decides': q['who_decides'], 'what_it_takes': q['what_it_takes'],
            'how_it_can_be_undone': q['how_it_can_be_undone'], 'sources': q['sources'], 'url': q['url'],
            'date_read': ds[-1] if ds else '', 'date_read_words': ' and '.join(words[d] for d in ds),
        })
    cols = ['route', 'name', 'v7_who', 'v7_instrument', 'route_entries', 'who_decides', 'what_it_takes',
            'how_it_can_be_undone', 'sources', 'url', 'date_read', 'date_read_words']
    mu, mv = meta('usgov-route-requirements'), meta('v7-routes')
    line = ('Source: U.S. National Archives (the Constitution); U.S. Government Publishing Office (U.S. Code, CFR, Senate '
            'rules); U.S. Senate; state constitutions and election offices; Internal Revenue Service; requirements for '
            'each route as of November 12, 2026, retrieved November 11 and 12, 2026. Oath & Action’s systems atlas, Who Do '
            'They Answer To?, routes to change, as of October 15, 2026. Formal requirements only; state rows name examples.')
    side = {
        'file': 'usgov-v7-route-grid.csv',
        'kind': 'derived',
        'publisher': mu['publisher'] + '; ' + mv['publisher'],
        'title_or_table': 'The atlas’s eleven routes to change, each with what the official texts require of it',
        'table_id': 'v7-routes joined to usgov-route-requirements by route code',
        'url': mu['url'] + [mv['url']],
        'observation_period': 'Routes as of October 15, 2026 (Atlas V7 snapshot); law and rules as read November 11 and 12, 2026',
        'geography': 'United States, with state examples named in each row',
        'universe_or_base': 'V7’s eleven routes, each with its count of reform profiles and what the official texts require',
        'unit': 'routes; route entries (reform profiles that list a route)',
        'date_retrieved': '2026-11-12',
        'vintage': 'Atlas V7 snapshot of October 15, 2026; official pages read November 11 and 12, 2026',
        'qualification': mu['qualification'] + ' ' + mv['qualification'] + '.',
        'columns': {
            'route': {'type': 'code', 'description': 'V7 route code'},
            'name': {'type': 'text', 'description': 'V7 route name, verbatim'},
            'v7_who': {'type': 'text', 'description': 'who acts, as V7 states it, verbatim'},
            'v7_instrument': {'type': 'text', 'description': 'the route’s instrument, as V7 states it, verbatim'},
            'route_entries': {'type': 'integer', 'description': 'reform profiles in V7 that list this route', 'unit': 'route entries'},
            'who_decides': {'type': 'text', 'description': 'who decides, from the official texts (usgov-route-requirements)'},
            'what_it_takes': {'type': 'text', 'description': 'the votes or approvals the official texts require'},
            'how_it_can_be_undone': {'type': 'text', 'description': 'how a change made this way can be undone'},
            'sources': {'type': 'text', 'description': 'the official texts behind the row'},
            'url': {'type': 'text', 'description': 'one address per row; the workflow sources file lists every page'},
            'date_read': {'type': 'date', 'description': 'the last date the route’s texts were read'},
            'date_read_words': {'type': 'text', 'description': 'the date or dates the route’s texts were read, in words'},
        },
        'printed_source_line': line,
        'ledger_row': 'pending: the research lead’s data check (R2-2)',
        'domain': 'all',
        'domain_note': mu.get('domain_note', ''),
        'states': mu.get('states', []),
        'derived_from': ['v7-routes.json', 'usgov-route-requirements.csv'],
        'derivation': ('Each of V7’s eleven routes, in V7’s order, joined by route code to the row of usgov-route-requirements '
                       'with the same code, every value copied as stored; date_read and date_read_words give the dates the '
                       'workflow sources file records for the route’s texts (the dates in its section’s rows). Script: '
                       'work/build/scripts/phase-3/maker_a_round3_derive.py.'),
    }
    write('usgov-v7-route-grid', cols, rows, side)
    return rows


# ---- figure checks ---------------------------------------------------------------------------------------------------
def spec(sid):
    with open(os.path.join(SPECS, sid + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def words_of(s):
    out = [s.get('title', ''), s.get('measure_line', ''), s.get('alt', ''), s.get('grade_line', '')]
    out += s.get('notes', []) + s.get('chart_notes', [])
    return ' '.join(out)


CHECKS = []


def check(name, ok, what):
    CHECKS.append((name, bool(ok), what))


def figures():
    # S66: the steps and branches, the 90 days, 60 days and 30 days in the law's text
    s, rows = spec('s66'), read_csv('govinfo-federal-rulemaking-steps')
    main = [r for r in rows if r['path'] == 'main']
    check('S66', len(main) == 5 and 'five steps' in s['title'], 'five main steps (title)')
    by = {r['order']: r for r in rows}
    check('S66', '90 calendar days' in by['2']['time_limit'] and '90 days' in s['alt'], 'White House review, 90 days')
    check('S66', '30 days' in by['5']['time_limit'] and 'at least 30 days' in s['alt'], 'final rule 30 days before effect')
    check('S66', 'February 18, 2025' in s['notes'][0] and 'February 18, 2025' in meta('govinfo-federal-rulemaking-steps')['vintage'], 'EO 14215 date')
    check('S66', 'November 12, 2026' in s['measure_line'] and meta('govinfo-federal-rulemaking-steps')['date_retrieved'] == '2026-11-12', 'law as of the retrieval date')
    # S67: 18, Ohio, 31 states and DC
    s, rows = spec('s67'), read_csv('ballotpedia-rcv-prohibitions-by-state')
    yes = [r for r in rows if r['reaches_city_elections'] == 'yes']
    part = [r for r in rows if r['reaches_city_elections'] == 'partly']
    none = [r for r in rows if not r['reaches_city_elections']]
    check('S67', len(yes) == 18 and '18 states' in s['title'] and 'TN' in [r['code'] for r in yes], '18 states, Tennessee among them')
    check('S67', [r['code'] for r in part] == ['OH'], 'Ohio alone partly')
    check('S67', len(none) == 32 and 'DC' in [r['code'] for r in none] and '31 states and the District of Columbia' in s['alt'], '31 states and DC with no ban')
    check('S67', sum(1 for r in yes if r['scope'] == 'all') == 17, '17 full bans in the first answer')
    check('S67', 'Public Chapter 621' in s['notes'][1] and 'Public Chapter 621' in part[0]['city_reach_note'] + ''.join(r['city_reach_note'] for r in yes), 'Public Chapter 621')
    # S68: six can change, two apply
    s, rows = spec('s68'), read_json('v7-pathway-electric-decision-makers')
    ch = [r for r in rows if r['can_change_rule']]
    check('S68', len(rows) == 8 and len(ch) == 6 and 'Six of the eight' in s['title'], 'six of eight can change')
    check('S68', sorted(r['order'] for r in rows if not r['can_change_rule']) == [6, 8], 'the two who apply: grid operators and the investor-owned utility')
    # S69: 20 standing, 3 select, 109 subcommittees, Appropriations 12, Budget and Ethics none
    s, rows = spec('s69'), read_csv('clerk-house-committees-119')
    com = {}
    for r in rows:
        com.setdefault(r['committee_code'], [r['committee'], r['committee_type'], 0])
        if r['subcommittee_code']:
            com[r['committee_code']][2] += 1
    ty = [v[1] for v in com.values()]
    check('S69', ty.count('standing') == 20 and ty.count('select') == 3 and ty.count('joint') == 4, '20 standing, 3 select, 4 joint')
    check('S69', sum(v[2] for v in com.values()) == 109 and '109 subcommittees' in s['title'] and '20 standing committees and three select' in s['title'], '20 standing, three select, 109 subcommittees (title)')
    check('S69', com['AP00'][2] == 12 and max(v[2] for v in com.values()) == 12, 'Appropriations has the most, 12')
    check('S69', com['BU00'][2] == 0 and com['SO00'][2] == 0 and [v[0] for v in com.values() if v[1] == 'standing' and v[2] == 0] == ['Committee on the Budget', 'Committee on Ethics'], 'Budget and Ethics have none')
    # S70: 94 districts, 13 appeals, 179, 673, 4, 9, the circuits' figures in the alt
    s, rows = spec('s70'), read_csv('uscode-federal-courts-circuits-districts')
    app = [r for r in rows if r['level'] == 'appeals']
    dist = [r for r in rows if r['level'] in ('district', 'district-territorial')]
    check('S70', len(app) == 13 and len(dist) == 94 and '94 district courts' in s['title'] and '13 courts of appeals' in s['title'], '94 district courts, 13 courts of appeals')
    check('S70', sum(int(r['judgeships']) for r in app) == 179 and '179' in s['notes'][0], '179 appeals judgeships')
    check('S70', sum(int(r['judgeships']) for r in rows if r['level'] in ('district', 'district-shared')) == 673 and '673' in s['notes'][0], '673 district judgeships with shared seats')
    check('S70', sum(int(r['judgeships']) for r in rows if r['level'] == 'district-territorial') == 4, 'four territorial judgeships')
    nine = [r for r in app if 'Ninth' in r['court']][0]
    check('S70', nine['judgeships'] == '29' and sum(int(r['judgeships']) for r in rows if r['parent'] == nine['court']) == 112, 'Ninth Circuit 29 and 112 in its districts')
    dcc = [r for r in app if 'District of Columbia' in r['court']][0]
    fed = [r for r in app if 'Federal' in r['court']][0]
    check('S70', dcc['judgeships'] == '11' and fed['judgeships'] == '12' and rows[0]['judgeships'] == '9', 'DC Circuit 11, Federal Circuit 12, nine justices')
    check('S70', '10-year terms' in s['notes'][0], 'territorial judges serve ten-year terms (sidecar note)')
    # S71: the counts of reforms per route, the 60 senators
    s, rows = spec('s71'), read_csv('usgov-v7-route-grid')
    n = {r['route']: int(r['route_entries']) for r in rows}
    check('S71', len(rows) == 11 and n['FS'] == 38 and max(n.values()) == 38 and '38' in s['title'], 'federal statute listed most, 38')
    check('S71', '60 senators to end debate on most bills' in [r for r in rows if r['route'] == 'FS'][0]['what_it_takes'] and '60 senators' in s['title'], '60 senators to end debate')
    want = {'SS': 29, 'LOC': 15, 'BI': 11, 'FA': 7, 'CRT': 7, 'FR': 6, 'ENF': 5, 'CIV': 4, 'AV': 3, 'IC': 1}
    check('S71', all(n[k] == v for k, v in want.items()), 'every route count in the alt')
    check('S71', '546,651' in [r for r in rows if r['route'] == 'BI'][0]['what_it_takes'], "California's signature count behind note 2")
    # S72: both votes by party
    s, rows = spec('s72'), read_csv('congress-hr5371-roll-calls-by-member')
    def cnt(ch, party=None, vote=None):
        return sum(1 for r in rows if r['chamber'] == ch and (party is None or r['party'] == party) and (vote is None or r['vote_cast'] == vote))
    check('S72', cnt('Senate', vote='Yea') == 60 and cnt('Senate', vote='Nay') == 40 and '60 to 40' in s['title'], 'Senate 60 to 40')
    check('S72', cnt('Senate', 'D', 'Yea') == 7 and cnt('Senate', 'I', 'Yea') == 1 and cnt('Senate', 'R', 'Yea') == 52 and 'seven Democrats and one independent joining 52 Republicans' in s['title'], 'Senate yes: 7 D, 1 I, 52 R (title)')
    check('S72', cnt('Senate', 'R', 'Nay') == 1 and cnt('Senate', 'I', 'Nay') == 1 and cnt('Senate', 'D', 'Nay') == 38, 'Senate no: 1 R, 1 I, 38 D')
    check('S72', cnt('House', vote='Yea') == 222 and cnt('House', vote='Nay') == 209 and '222 to 209' in s['title'], 'House 222 to 209')
    check('S72', cnt('House') == 433 and 435 - cnt('House') == 2, 'House 433 members recorded, 2 of 435 seats vacant')
    check('S72', cnt('House', 'D', 'Yea') == 6 and cnt('House', 'R', 'Nay') == 2 and cnt('House', 'D', 'Not Voting') == 1 and cnt('House', 'R', 'Not Voting') == 1, 'House: 6 D yes, 2 R no, 1 of each not voting')
    check('S72', cnt('House', 'D') == 214 and cnt('House', 'R') == 219 and cnt('Senate', 'D') == 45 and cnt('Senate', 'R') == 53 and cnt('Senate', 'I') == 2, 'party sizes in the alt')
    dates = {(r['chamber'], r['vote_date']) for r in rows}
    check('S72', dates == {('Senate', '2025-11-10'), ('House', '2025-11-12')} and 'November 10, 2025' in s['title'] and 'two days later' in s['title'], 'vote dates, two days apart')
    for name, ok, what in CHECKS:
        print(('ok    ' if ok else 'FAIL  ') + name + ': ' + what)
        if not ok:
            FAULTS.append(name + ': ' + what)
    print('%d checks, %d failed' % (len(CHECKS), sum(1 for c in CHECKS if not c[1])))


if __name__ == '__main__':
    g = grid()
    if FIGS:
        figures()
    else:
        for r in g:
            print(r['route'], r['route_entries'], r['date_read_words'])
    if FAULTS:
        print('\n'.join('FAULT ' + f for f in FAULTS))
        sys.exit(1)
