"""Write the Atlas V7 tables that rounds 1 and 2 draw, under the round 0 data contract (engineer notes, C1).

Research lead's script, Phase 3 round 0. It imports nothing of the engineer's and writes only these files in
work/build/data/, each with its sidecar:

  v7-reform-routes.json                  heat table (plan row 36): every reform's routes, feasibility and check date
  v7-issues.json                         filterable lookup table (row 37): every issue record, flattened
  v7-claims-drug-prices.json             evidence table (row 38): the drug-price claims on pathway PW06
  v7-numbers.json                        indicator row (row 76): V7's eight headline figures
  v7-issue-status-checks-on-power.json   status chips (row 79): dated statuses of six checks-on-power issues

Usage:
    python3 -I work/build/scripts/phase-3/research_v7_extract.py

Reads work/extract/atlas-v7-data.json (Atlas V7, snapshot of October 15, 2026). Values are copied, never typed.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
V7P = ROOT / 'work/extract/atlas-v7-data.json'
OUT = ROOT / 'work/build/data'
SNAP = '2026-10-15'
PUB = 'Oath & Action’s systems atlas, Who Do They Answer To?'
LEDGER = 'not needed: Atlas V7, read by script'

V7 = json.loads(V7P.read_text(encoding='utf-8'))
DOMAIN_TITLE = {d['id']: d['title'] for d in V7['domains']}


def flat(v):
    if isinstance(v, list):
        return '; '.join(flat(x) for x in v)
    if isinstance(v, dict):
        return '; '.join(f'{k}: {flat(x)}' for k, x in v.items())
    return v


def col(t, d, unit=None):
    o = {'type': t, 'description': d}
    if unit:
        o['unit'] = unit
    return o


def write(name, rows, columns, meta):
    for r in rows:
        assert list(r.keys()) == list(columns.keys()), (name, list(r.keys()))
    body = json.dumps({'rows': rows}, ensure_ascii=False, indent=1)
    for bad in ('—', '‑'):
        assert bad not in body, (name, bad)
    (OUT / f'{name}.json').write_text(body + '\n', encoding='utf-8')
    base = {'file': f'{name}.json', 'kind': 'v7', 'publisher': PUB, 'url': 'work/extract/atlas-v7-data.json',
            'geography': 'United States', 'date_retrieved': SNAP, 'vintage': 'Atlas V7 snapshot of October 15, 2026',
            'snapshot': SNAP, 'ledger_row': LEDGER, 'columns': columns}
    base.update(meta)
    txt = json.dumps(base, ensure_ascii=False, indent=1)
    assert '—' not in txt and 'isclos' not in txt, name
    (OUT / f'{name}.meta.json').write_text(txt + '\n', encoding='utf-8')
    print(name, len(rows))


# 1. Reform routes (heat table)
ROUTE_NAME = {r['code']: r['name'] for r in V7['routes']['items']}
GROUP = {rid: g['title'] for g in V7['reformGroups'] for rid in g['reforms']}
rows = []
for rid in sorted(V7['reforms'], key=lambda x: int(x.split('-')[1])):
    rf = V7['reforms'][rid]
    for rt in rf['routes']:
        rows.append({'reform_id': rid, 'reform_title': rf['title'], 'reform_group': GROUP.get(rid), 'route': rt['route'],
                     'route_name': ROUTE_NAME.get(rt['route']), 'who': rt.get('who'), 'feasibility': rt.get('feasibility'),
                     'note': rt.get('note'), 'checked': rt.get('checked')})
cols = {'reform_id': col('id', 'V7 reform ID'), 'reform_title': col('text', 'reform title'), 'reform_group': col('category', 'V7 reform group'),
        'route': col('code', 'V7 route code'), 'route_name': col('category', 'route name'), 'who': col('text', 'who acts on this route'),
        'feasibility': col('category', 'high, medium, low or very low, on V7\'s scale for 2026 to 2030'), 'note': col('text', 'V7\'s note on the route'),
        'checked': col('date', 'date V7 checked the route; empty means not checked')}
n_checked = sum(1 for r in rows if r['checked'])
write('v7-reform-routes', rows, cols, {
    'title_or_table': f'reform profiles, routes to change: {len(rows)} route entries for {len(V7["reforms"])} reforms', 'table_id': 'reforms[].routes; routes.items; reformGroups',
    'observation_period': 'Feasibility for 2026 to 2030, as of October 15, 2026',
    'universe_or_base': 'Every route entry in every reform profile',
    'unit': 'route entries; feasibility is an ordinal category, never a number',
    'qualification': f'{n_checked} of {len(rows)} route entries carry a check date (October 15, 2026); a route with no date prints as not checked. Feasibility is the atlas\'s own judgment on its four-step scale, and a heat table shows each cell\'s word, never a score or a total',
    'printed_source_line': f'Source: {PUB}, reform profiles, routes to change, {len(rows)} route entries for {len(V7["reforms"])} reforms, feasibility for 2026 to 2030, United States. Snapshot of October 15, 2026. {n_checked} routes carry a check date; the rest are not checked.',
    'domain': 'all', 'domain_note': 'The 50 reforms span every atlas domain', 'states': []})

# 2. Issues (lookup table)
rows = []
for iid in sorted(V7['issues'], key=lambda x: (x[0], int(re.sub(r'\D', '', x)))):
    i = V7['issues'][iid]
    st = i.get('status') or {}
    rows.append({'id': iid, 'domain': i['domain'], 'domain_title': DOMAIN_TITLE.get(i['domain']), 'subsystem': i.get('subsystem'),
                 'title': i['title'], 'grade': i.get('grade'), 'jurisdiction': flat(i.get('jurisdiction')), 'observed': None if i.get('observed') in (None, '', 'n/a') else i.get('observed'),
                 'actor': flat(i.get('actor')), 'loops': flat(i.get('loops') or []), 'aimed_reforms': flat(i.get('aimed_reforms') or []),
                 'retired': bool(i.get('retired')), 'status_checked': st.get('checked')})
cols = {'id': col('id', 'V7 issue ID'), 'domain': col('code', 'V7 domain ID'), 'domain_title': col('category', 'domain title'), 'subsystem': col('category', 'subsystem'),
        'title': col('text', 'issue title'), 'grade': col('category', 'V7 grade word as stored'), 'jurisdiction': col('category', 'level V7 records'),
        'observed': col('text', 'when V7 observed it, as stored (a year or a year and month)'), 'actor': col('text', 'who can act, as V7 states it'), 'loops': col('text', 'V7 loop IDs, joined by "; "'),
        'aimed_reforms': col('text', 'V7 reform IDs aimed at the issue, joined by "; "'), 'retired': col('boolean', 'V7 marks the record retired'),
        'status_checked': col('date', 'date of the status check, where V7 gives one')}
write('v7-issues', rows, cols, {
    'title_or_table': f'issue records, {len(rows)} issues', 'table_id': 'issues',
    'observation_period': 'Issues as recorded at the October 15, 2026 snapshot',
    'universe_or_base': f'Every issue record, {sum(1 for r in rows if not r["retired"])} active and {sum(1 for r in rows if r["retired"])} retired',
    'unit': 'issue records',
    'qualification': 'Grade words are V7\'s stored values (for example well_supported and retired) and print through chapter 13\'s mapping table, never raw; the observed field is V7\'s own, and where V7 stores "n/a" the cell is left empty',
    'printed_source_line': f'Source: {PUB}, issue records, {len(rows)} issues across ten domains, as of October 15, 2026, United States. Snapshot of October 15, 2026. Grades are the atlas\'s own; retired records are marked.',
    'domain': 'all', 'domain_note': 'The issue register spans all ten domains', 'states': []})

# 3. Drug-price claims on pathway PW06 (evidence table)
pat = re.compile(r'drug|insulin|pharmac|PBM|rebate|patent|generic|prescription', re.I)
rows = []
for cid, c in sorted(V7['claims'].items()):
    if c.get('pathway') == 'PW06' and pat.search(c['claim']):
        rows.append({'id': cid, 'claim': c['claim'], 'confidence': c['confidence'], 'population': c.get('population'), 'jurisdiction': c.get('jurisdiction'),
                     'period': c.get('period'), 'limitation': c.get('limitation'), 'sources': flat(c.get('sources') or []), 'verified_on': c.get('verified_on')})
cols = {'id': col('id', 'V7 claim ID'), 'claim': col('text', 'the claim as V7 words it'), 'confidence': col('category', 'V7 grade word as stored'),
        'population': col('text', 'who the claim covers'), 'jurisdiction': col('text', 'where'), 'period': col('text', 'when'), 'limitation': col('text', 'V7\'s stated limitation'),
        'sources': col('text', 'V7 source IDs, joined by "; "'), 'verified_on': col('text', 'V7\'s verification date as stored')}
write('v7-claims-drug-prices', rows, cols, {
    'title_or_table': f'claims register, pathway PW06 (Medical bills and drug prices), the {len(rows)} claims about drug prices', 'table_id': 'claims, pathway PW06, filtered by the studio on drug, insulin, pharmacy, PBM, rebate, patent, generic or prescription in the claim text',
    'observation_period': 'Claims as verified through October 15, 2026; each claim states its own period',
    'universe_or_base': f'The {len(rows)} of pathway PW06\'s claims whose text is about drug prices',
    'unit': 'claims',
    'qualification': 'Each claim carries its own population, place, period and limitation, and its grade covers that claim alone. The filter is the studio\'s, so the table is a selection from the pathway, which also holds claims on medical bills',
    'printed_source_line': f'Source: {PUB}, claims register, pathway PW06, {len(rows)} claims about drug prices, verified through October 15, 2026, United States. Snapshot of October 15, 2026. Each claim states its own period and limitation; grades are the atlas\'s own.',
    'domain': 'D06', 'domain_note': 'V7\'s competition domain asks why prescriptions cost so much, and the claims are about drug-benefit middlemen, patents and generic competition', 'states': []})

# 4. Headline figures (indicator row)
rows = []
for n, x in enumerate(V7['numbers'], 1):
    rows.append({'order': n, 'figure': x['figure'], 'caption': x['caption'], 'qualification': x.get('qualification'), 'kind': x.get('kind'),
                 'sources': flat(x.get('sources') or []), 'verified_status': x.get('verified_status')})
cols = {'order': col('integer', 'order in V7'), 'figure': col('text', 'the figure as V7 prints it'), 'caption': col('text', 'V7\'s caption'), 'qualification': col('text', 'V7\'s qualification'),
        'kind': col('category', 'kind of figure, as V7 labels it'), 'sources': col('text', 'V7 source IDs, joined by "; "'), 'verified_status': col('text', 'V7\'s check note')}
write('v7-numbers', rows, cols, {
    'title_or_table': f'headline figures, {len(rows)} numbers with captions, qualifications and sources', 'table_id': 'numbers',
    'observation_period': 'Each figure states its own period; all checked October 15, 2026',
    'universe_or_base': 'The atlas\'s headline figures', 'unit': 'figures, each in its own unit',
    'qualification': 'Each figure carries its own qualification, printed with it; several describe events that may have moved since the snapshot, such as Alaska\'s Ballot Measure 2, decided on November 3, 2026',
    'printed_source_line': f'Source: {PUB}, headline figures, {len(rows)} numbers, checked October 15, 2026, United States. Snapshot of October 15, 2026. Each figure carries its own source and qualification.',
    'domain': 'all', 'domain_note': 'The eight figures come from several domains', 'states': []})

# 5. Status of six checks-on-power issues (status chips)
PICK = ['I068', 'I070', 'I163', 'X05', 'X06', 'X18']
rows = []
for iid in PICK:
    i = V7['issues'][iid]
    st = i['status']
    rows.append({'id': iid, 'title': i['title'], 'domain': i['domain'], 'status_text': st['text'], 'status_result': st.get('result'), 'checked': st.get('checked')})
cols = {'id': col('id', 'V7 issue ID'), 'title': col('text', 'issue title'), 'domain': col('code', 'V7 domain ID'), 'status_text': col('text', 'V7\'s status text, verbatim'),
        'status_result': col('category', 'V7\'s check result word'), 'checked': col('date', 'date V7 checked the status')}
write('v7-issue-status-checks-on-power', rows, cols, {
    'title_or_table': 'issue records, status of six issues in Checks on power and equal justice (I068, I070, I163, X05, X06, X18)', 'table_id': 'issues[].status',
    'observation_period': 'Statuses as checked on October 15, 2026',
    'universe_or_base': 'Six issues the studio chose because each status names a court case, a ruling or a watchdog finding',
    'unit': 'issue statuses',
    'qualification': 'Statuses can have moved since October 15, 2026; a chip prints V7\'s date beside it. The chip words (decided, pending, in court) are the studio\'s reading of V7\'s text and must quote the case and date the text gives',
    'printed_source_line': f'Source: {PUB}, issue records, status of six issues on checks on power, as of October 15, 2026, United States. Snapshot of October 15, 2026. Statuses may have changed since that date.',
    'domain': 'D05', 'states': ['IL'], 'domain_note': 'Issue X05 names Trump v. Illinois, so Illinois counts once under Rule 01.9'})
