"""Write the Atlas V7 tables that rounds 1 to 3 draw, under the round 0 data contract (engineer notes, C1).

Research lead's script, Phase 3 round 0. It imports nothing of the engineer's and writes only these files in
work/build/data/, each with its sidecar:

  v7-reform-routes.json                  heat table (plan row 36): every reform's routes, feasibility and check date
  v7-issues.json                         filterable lookup table (row 37): every issue record, flattened
  v7-claims-drug-prices.json             evidence table (row 38): the drug-price claims on pathway PW06
  v7-numbers.json                        indicator row (row 76): V7's eight headline figures
  v7-issue-status-checks-on-power.json   status chips (row 79): dated statuses of six checks-on-power issues

Round 3 tables, added November 12, 2026 (round 3 data plan):

  v7-rcv-local-routes.json                  decision tree (row 87): route LOC on reforms R-01 and R-02
  v7-pathway-electric-decision-makers.json  who-decides diagram (row 88): pathway PW03's decision makers
  v7-routes.json                            comparison grid (row 91): the eleven routes, with route entries counted
  v7-links-with-regions.json                adjacency matrix (row 95): every connection with the region of each end
  v7-region-connection-matrix.json          adjacency matrix (row 95): connections counted by region pair (derived)

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


def curl(line):
    """Set a printed line's apostrophes and double quotes curly (D3-175, extended in fix pass 4 to double quotes)."""
    line = line.replace("'", '\u2019')
    line = re.sub(r'(^|[\s(\[])"', '\\1\u201c', line)
    return line.replace('"', '\u201d')


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
    base['printed_source_line'] = curl(base['printed_source_line'])
    if 'source_line_variants' in base:
        base['source_line_variants'] = {k: curl(v) for k, v in base['source_line_variants'].items()}
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
    # Fix pass 3 (DL-R5): one variant per domain, so a table that draws one domain names the rows it draws (Rule 13.6); S38 takes domain_d01
    'source_line_variants': {f'domain_{d.lower()}': (f'Source: {PUB}, issue records in the domain of {DOMAIN_TITLE[d][0].lower() + DOMAIN_TITLE[d][1:]}, '
                                                     f'{sum(1 for r in rows if r["domain"] == d)} of {len(rows)} issues, as of October 15, 2026, United States. '
                                                     'Snapshot of October 15, 2026. Grades are the atlas\u2019s own'
                                                     + ('; retired records are marked.' if any(r['retired'] for r in rows if r['domain'] == d) else '.'))
                             for d in sorted(DOMAIN_TITLE)},
    'domain': 'all', 'domain_note': 'The issue register spans all ten domains', 'states': []})

# 3. Drug-price claims on pathway PW06 (evidence table)
pat = re.compile(r'drug|insulin|pharmac|PBM|rebate|patent|generic|prescription', re.I)
rows = []
for cid, c in sorted(V7['claims'].items()):
    if c.get('pathway') == 'PW06' and pat.search(c['claim']):
        rows.append({'id': cid, 'claim': c['claim'], 'confidence': c['confidence'], 'population': c.get('population'), 'jurisdiction': c.get('jurisdiction'),
                     'period': c.get('period'), 'limitation': c.get('limitation'), 'sources': flat(c.get('sources') or []),
                     'source_words': '; '.join(', '.join(x for x in (V7['sources'][sid].get('publisher'), V7['sources'][sid].get('title')) if x)
                                               for sid in (c.get('sources') or []) if sid in V7['sources']),
                     'verified_on': c.get('verified_on')})
cols = {'id': col('id', 'V7 claim ID'), 'claim': col('text', 'the claim as V7 words it'), 'confidence': col('category', 'V7 grade word as stored'),
        'population': col('text', 'who the claim covers'), 'jurisdiction': col('text', 'where'), 'period': col('text', 'when'), 'limitation': col('text', 'V7\'s stated limitation'),
        'sources': col('text', 'V7 source IDs, joined by "; "'), 'source_words': col('text', 'each source as V7\'s sources record names it, publisher and title, joined by "; " (fix pass 2, A7)'),
        'verified_on': col('text', 'V7\'s verification date as stored')}
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
    'title_or_table': 'headline figures, eight figures with captions, qualifications and sources', 'table_id': 'numbers',
    'observation_period': 'Each figure states its own period; all checked October 15, 2026',
    'universe_or_base': 'The atlas\'s headline figures', 'unit': 'figures, each in its own unit',
    # D3-835's wording ("on the ballot") and the data lead's RF-4 note on figures 5 and 7 (round 2 review fix pass, D3-910)
    'qualification': ('Each figure carries its own qualification, printed with it; several describe events that may have moved since the snapshot, such as Alaska\'s Ballot Measure 2, on the ballot on November 3, 2026.'
                      ' V7 stores figure 4’s sentence on the inspectors general under figure 5 as well, with a different docket clause ("a July 20, 2026 minute order" against "dated July 22, 2026"), where it does not apply to figure 5.'
                      ' Figure 7’s qualification calls H.R. 7008 "a ban" by its stock provision alone; the bill as the House passed it (engrossed text of July 22, 2026, read on govinfo.gov November 12, 2026) has two parts,'
                      ' section 2, "Restrictions on covered investments", and section 3, "Requiring voters to provide photo identification" to vote in person in an election for federal office.'
                      ' The table keeps V7’s words as stored (data lead ruling RF-4)'),
    'printed_source_line': f'Source: {PUB}, headline figures, eight figures, checked October 15, 2026, United States. Snapshot of October 15, 2026. Each figure carries its own source and qualification.',
    'domain': 'all', 'domain_note': 'The eight figures come from several domains', 'states': []})
assert len(rows) == 8

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


# ---- Round 3 tables, added November 12, 2026 (round 3 data plan rows 87, 88, 91 and 95) -----------------------------
# 6. Route LOC on the two ranked-choice reforms (decision tree, row 87)
rows = []
for rid in ('R-01', 'R-02'):
    rf = V7['reforms'][rid]
    for rt in rf['routes']:
        if rt['route'] == 'LOC':
            rows.append({'reform_id': rid, 'reform_title': rf['title'], 'route': rt['route'], 'who': rt.get('who'), 'feasibility': rt.get('feasibility'),
                         'note': rt.get('note'), 'checked': rt.get('checked')})
loc = next(r for r in V7['routes']['items'] if r['code'] == 'LOC')
cols = {'reform_id': col('id', 'V7 reform ID'), 'reform_title': col('text', 'reform title'), 'route': col('code', 'V7 route code'), 'who': col('text', 'who acts, as V7 states it'),
        'feasibility': col('category', 'V7 feasibility word'), 'note': col('text', 'V7\'s note, verbatim'), 'checked': col('date', 'date V7 checked the route; empty means not checked')}
write('v7-rcv-local-routes', rows, cols, {
    'title_or_table': 'reform profiles R-01 and R-02, the local route (LOC)', 'table_id': 'reforms[R-01, R-02].routes (route LOC); routes.items (LOC)',
    'observation_period': 'As of October 15, 2026', 'universe_or_base': 'The local route on the two reforms that adopt ranked-choice voting',
    'unit': 'route entries', 'qualification': 'V7\'s route definition for LOC: ' + loc['depends'],
    'printed_source_line': f'Source: {PUB}, reform profiles R-01 and R-02, the local route, as of October 15, 2026, United States. Snapshot of October 15, 2026. Bans by state come from Ballotpedia, a secondary source.',
    'domain': 'D02', 'states': []})

# 7. Pathway PW03's decision makers (who-decides diagram, row 88)
pw = next(p for p in V7['pathways'] if p['id'] == 'PW03')
rows = [{'order': n, 'who': x['who'], 'jurisdiction': x.get('jurisdiction'), 'controls': x.get('controls'), 'can_change_rule': bool(x.get('can_change_rule')),
         'how_to_reach': x.get('how_to_reach')} for n, x in enumerate(pw['decision_makers'], 1)]
cols = {'order': col('integer', 'order in V7'), 'who': col('text', 'decision maker, as V7 names it'), 'jurisdiction': col('category', 'federal, regional, state, local or private, as stored'),
        'controls': col('text', 'what it controls, verbatim'), 'can_change_rule': col('boolean', 'V7: whether it can change the rule, or only apply it'),
        'how_to_reach': col('text', 'how a reader reaches it, verbatim')}
write('v7-pathway-electric-decision-makers', rows, cols, {
    'title_or_table': f'everyday answer PW03, "{pw["title"]}", its decision makers', 'table_id': 'pathways[PW03].decision_makers; who_can_change_the_rules',
    'observation_period': 'As of October 15, 2026', 'universe_or_base': f'The {len(rows)} decision makers V7 lists for "{pw["question"]}"',
    'unit': 'decision makers', 'qualification': 'Who can change a rule is V7\'s own field; lines of authority between them take no sign. V7\'s summary: ' + pw['who_can_change_the_rules'][:600],
    'printed_source_line': f'Source: {PUB}, everyday answer "{pw["title"]}", decision makers, as of October 15, 2026, United States. Snapshot of October 15, 2026. Roles as the atlas states them.',
    'domain': 'D06', 'domain_note': 'V7 I093, utility networks, sits in competition and market power (Sector bottlenecks)', 'states': []})

# 8. The eleven routes (comparison grid, row 91)
counts = {}
for rf in V7['reforms'].values():
    for rt in rf['routes']:
        counts[rt['route']] = counts.get(rt['route'], 0) + 1
rows = [{'route': r['code'], 'name': r['name'], 'instrument': r['instrument'], 'who': r['who'], 'depends': r['depends'], 'route_entries': counts.get(r['code'], 0)}
        for r in V7['routes']['items']]
cols = {'route': col('code', 'V7 route code'), 'name': col('text', 'route name'), 'instrument': col('text', 'instrument, verbatim'), 'who': col('text', 'who acts, verbatim'),
        'depends': col('text', 'what a change on the route depends on, verbatim'), 'route_entries': col('integer', 'reform profiles that list this route', 'route entries')}
write('v7-routes', rows, cols, {
    'title_or_table': 'routes to change, the eleven routes', 'table_id': 'routes.items; reforms[].routes (counted)', 'observation_period': 'As of October 15, 2026',
    'universe_or_base': 'Every route V7 defines, with how many reform profiles list it', 'unit': 'routes; route entries',
    'qualification': 'Route entries count reforms that list a route, not how likely a change is; V7 rates feasibility per reform',
    'printed_source_line': f'Source: {PUB}, routes to change, eleven routes, as of October 15, 2026, United States. Snapshot of October 15, 2026.',
    'domain': 'all', 'domain_note': 'The routes serve reforms in every domain', 'states': []})

# 9. Connections with the region of each end, and the region matrix (adjacency matrix, row 95; data lead change 1)
REGION, RTITLE, RLAYER = {}, {}, {}
for lay, v in V7['layers'].items():
    for r in v['regions']:
        RTITLE[r['id']] = r['title']
        RLAYER[r['id']] = lay
        for n in r['nodes']:
            assert n not in REGION, n
            REGION[n] = r['id']
nodes = V7['nodes'] if isinstance(V7['nodes'], list) else list(V7['nodes'].values())
assert all(n['id'] in REGION for n in nodes) and len(REGION) == len(nodes) == 51
links = V7['links'] if isinstance(V7['links'], list) else list(V7['links'].values())
rows = [{'id': l['id'], 'from': l['from'], 'to': l['to'], 'from_region': REGION[l['from']], 'to_region': REGION[l['to']], 'type': l['type'],
         'polarity': {'+': 'positive', '-': 'negative'}.get(l['polarity'], 'none'), 'evidence': l['evidence'], 'delay': l.get('delay'), 'name': l.get('name')} for l in links]
cols = {'id': col('id', 'V7 connection ID'), 'from': col('id', 'V7 variable ID at the start'), 'to': col('id', 'V7 variable ID at the end'),
        'from_region': col('code', 'V7 region of the start variable'), 'to_region': col('code', 'V7 region of the end variable'),
        'type': col('category', 'causal, money, information, authority or ownership'), 'polarity': col('category', 'V7 sign in words: positive (+), negative (-) or none (authority connections carry no sign)'),
        'evidence': col('category', 'V7 grade word as stored'), 'delay': col('category', 'S, M or L'), 'name': col('text', 'connection name')}
write('v7-links-with-regions', rows, cols, {
    'title_or_table': f'connections, {len(rows)} links with the region of each end', 'table_id': 'links; layers[].regions[].nodes',
    'observation_period': 'As of October 15, 2026', 'universe_or_base': 'Every connection in the model; every variable sits in one of V7\'s ten regions',
    'unit': 'connections', 'qualification': 'Regions are V7\'s own; V7 gives no domain to 20 variables and two domains to nine, so the matrix groups by region (data lead change 1)',
    'printed_source_line': f'Source: {PUB}, model connections, {len(rows)} links by region, snapshot of October 15, 2026, United States.',
    'domain': 'all', 'domain_note': 'Every connection in the model', 'states': []})
ORDER = [r['id'] for lay in ('core', 'economy', 'technology') for r in V7['layers'][lay]['regions']]
cells = []
for a in ORDER:
    for b in ORDER:
        sel = [r for r in rows if r['from_region'] == a and r['to_region'] == b]
        cells.append({'from_region': a, 'from_title': RTITLE[a], 'to_region': b, 'to_title': RTITLE[b], 'links': len(sel),
                      'positive': sum(1 for r in sel if r['polarity'] == 'positive'), 'negative': sum(1 for r in sel if r['polarity'] == 'negative'),
                      'no_sign': sum(1 for r in sel if r['polarity'] == 'none'), 'link_ids': '; '.join(r['id'] for r in sel)})
filled = sum(1 for c in cells if c['links'])
assert sum(c['links'] for c in cells) == len(rows)
cols = {'from_region': col('code', 'region at the start'), 'from_title': col('text', 'its title'), 'to_region': col('code', 'region at the end'), 'to_title': col('text', 'its title'),
        'links': col('integer', 'connections from the one region to the other', 'connections'), 'positive': col('integer', 'with a plus sign'), 'negative': col('integer', 'with a minus sign'),
        'no_sign': col('integer', 'authority connections, which carry no sign'), 'link_ids': col('text', 'the connection IDs, joined by "; "')}
write('v7-region-connection-matrix', cells, cols, {
    'kind': 'derived', 'derived_from': ['v7-links-with-regions.json'],
    'derivation': 'Counts of connections by start and end region, all 100 pairs of V7\'s ten regions, split by sign',
    'title_or_table': f'connections counted by region, ten regions by ten ({filled} of 100 cells filled)', 'table_id': 'links grouped by layers[].regions',
    'observation_period': 'As of October 15, 2026', 'universe_or_base': f'All {len(rows)} connections, counted for every pair of regions',
    'unit': 'connections', 'qualification': 'A count says how many connections join two regions, not how strong they are; a plus sign means the two variables move together, not that the link is good',
    'printed_source_line': f'Source: {PUB}, model connections counted by region, snapshot of October 15, 2026, United States. Counted by Oath & Action.',
    'domain': 'all', 'domain_note': 'Every connection in the model', 'states': []})
