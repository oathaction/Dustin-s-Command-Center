"""Build the shared chart dataset for the data visualization round (November 6, 2026; DR-44 to DR-51).

Usage:
    python3 -I work/build/scripts/phase-2/dataviz_shared_data.py

Reads Atlas V7 (work/extract/atlas-v7-data.json, D2-90) and the research lead's public series
(work/boards/phase-2/data-viz/shared/public/*.csv with *.meta.json sidecars), and writes
work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json: one record per dataset with its rows, fields,
evidence kind and a source line in Master Brief section 15 order, plus the ten like-for-like specimens.
Every chart value the makers draw comes from this file, and the verifier checks marks against it.
"""
import csv
import json
import pathlib
import collections

ROOT = pathlib.Path(__file__).resolve().parents[4]
V7 = json.loads((ROOT / 'work/extract/atlas-v7-data.json').read_text())
SHARED = ROOT / 'work/boards/phase-2/data-viz/shared'
PUBLIC = SHARED / 'public'
OUT = SHARED / '20261106_Chart-Data.json'
SNAP = V7['meta']['snapshot']  # 2026-10-15
ATLAS = 'Oath & Action, Who Do They Answer To? Systems Atlas V7'


def src(ids):
    out = []
    for i in ids:
        s = V7['sources'].get(i)
        if not s:
            raise SystemExit(f'unknown V7 source {i}')
        out.append({k: s.get(k) for k in ('id', 'publisher', 'title', 'year', 'url', 'type', 'note', 'accessed')})
    return out


def atlas_line(table, period, geography, qualification):
    return f'{ATLAS}, {table}. {period}. {geography}. Snapshot of {SNAP}. {qualification}'


datasets = {}

# S01 Big number in context: the shared view on a stock trading ban (V7 headline figure 7)
n7 = next(n for n in V7['numbers'] if n['figure'].startswith('87%'))
datasets['stock-trading-ban'] = {
    'spec': 'S01', 'kind': 'v7', 'title': 'Support for banning stock trading by members of Congress, and the votes that followed',
    'evidence': 'Finding', 'grade': 'documented',
    'key': 'key',
    'fields': [{'name': 'key', 'type': 'id'}, {'name': 'group', 'type': 'label'}, {'name': 'value', 'type': 'number', 'unit': 'percent or votes'},
               {'name': 'measure', 'type': 'label'}],
    'rows': [
        {'key': 'support-all', 'group': 'All registered voters', 'value': 86, 'measure': 'percent who favor a ban'},
        {'key': 'support-republicans', 'group': 'Republicans', 'value': 87, 'measure': 'percent who favor a ban'},
        {'key': 'support-democrats', 'group': 'Democrats', 'value': 88, 'measure': 'percent who favor a ban'},
        {'key': 'house-yes', 'group': 'House, passage of H.R. 7008, July 22, 2026', 'value': 232, 'measure': 'votes for'},
        {'key': 'house-no', 'group': 'House, passage of H.R. 7008, July 22, 2026', 'value': 198, 'measure': 'votes against'},
        {'key': 'senate-yes', 'group': 'Senate, cloture on the motion to proceed, September 30, 2026', 'value': 53, 'measure': 'votes for'},
        {'key': 'senate-no', 'group': 'Senate, cloture on the motion to proceed, September 30, 2026', 'value': 47, 'measure': 'votes against'},
        {'key': 'senate-needed', 'group': 'Senate, cloture on the motion to proceed, September 30, 2026', 'value': 60, 'measure': 'votes needed (three-fifths)'},
    ],
    'v7_figure': n7,
    'sources': src(n7['sources']),
    'source_line': ('Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, '
                    'United States; U.S. House of Representatives, Roll Call 280, July 22, 2026; U.S. Senate, Vote 253, September 30, 2026; '
                    f'as recorded in {ATLAS}, snapshot of {SNAP}. The survey predates both votes by three years.'),
    'notes': ['Party marks take neutral inks with the party name printed on them (DR-48).',
              'The 86 percent overall figure is in the survey source note (N40), not in the headline figure caption.'],
}

# S03 Ranked bar and S08 Unit chart: the repair log
RL = V7['repairLog']
GROUP = {
    'ballot initiative': 'Ballot initiative', 'court ruling': 'Court ruling', 'state statute': 'State statute',
    'referendum': 'Referendum', 'federal statute': 'Federal statute',
    'agency rule': 'Executive or agency action', 'executive action': 'Executive or agency action', 'executive order': 'Executive or agency action',
    'municipal ordinance (local law)': 'Local law or funding vote', 'council funding vote': 'Local law or funding vote',
}
DIRS = ['toward voters', 'away from voters', 'voters kept existing rules', 'mixed', 'pending']
rows = []
for r in RL['rows']:
    rows.append({'key': r['id'], 'date': r['date'], 'year': int(r['date'][:4]), 'jurisdiction': r['jurisdiction'],
                 'direction': r['direction'], 'instrument': r['instrument'], 'instrument_group': GROUP[r['instrument']],
                 'rule': r['rule'], 'margin': r['margin'], 'reversed_by': r.get('reversed_by'),
                 'source_title': r['source_title'], 'source_url': r['source_url'], 'verified': r['verified']})
rows.sort(key=lambda x: (x['date'], x['key']))
rl_line = atlas_line('repair log of 64 dated rule changes', 'August 6, 1965 to the November 3, 2026 ballot',
                     'United States: federal, state and local', 'Directions are the atlas\'s own codes, set out in its coding note; each row cites its own source. One row (RL02) rests on a source the atlas did not check.')
datasets['rule-changes'] = {
    'spec': 'S08', 'kind': 'v7', 'title': 'The repair log: 64 dated changes to the rules that decide who officials answer to',
    'evidence': 'Finding', 'grade': 'documented', 'key': 'key',
    'fields': [{'name': 'key', 'type': 'id'}, {'name': 'date', 'type': 'date'}, {'name': 'direction', 'type': 'category', 'values': DIRS},
               {'name': 'instrument_group', 'type': 'category'}, {'name': 'jurisdiction', 'type': 'label'}],
    'rows': rows, 'intro': RL['intro'], 'coding_note': RL['coding_note'],
    'counts': dict(collections.Counter(r['direction'] for r in rows)),
    'source_line': rl_line,
    'notes': ['Unit charts draw one mark per row, keyed by its RL id, so every mark traces to one record.'],
}
by = collections.OrderedDict()
for r in rows:
    g = by.setdefault(r['instrument_group'], {'key': r['instrument_group'], 'value': 0, **{d: 0 for d in DIRS}})
    g['value'] += 1
    g[r['direction']] += 1
inst = sorted(by.values(), key=lambda x: (-x['value'], x['key']))
datasets['rule-changes-by-instrument'] = {
    'spec': 'S03', 'kind': 'v7', 'title': 'How the 64 rule changes in the repair log were made',
    'evidence': 'Finding', 'grade': 'documented', 'key': 'key',
    'fields': [{'name': 'key', 'type': 'category'}, {'name': 'value', 'type': 'number', 'unit': 'rule changes'}] +
              [{'name': d, 'type': 'number', 'unit': 'rule changes'} for d in DIRS],
    'rows': inst,
    'grouping': {k: v for k, v in GROUP.items()},
    'source_line': rl_line,
    'notes': ['Five instruments with one row each are grouped: agency rule, executive action and executive order as "Executive or agency action"; '
              'municipal ordinance and council funding vote as "Local law or funding vote". The grouping is the studio\'s; the instruments are V7\'s.'],
}

# S06 Comparison table: eight scenarios for 2030 and the four outcome families
FAM = {'DQ': 'Quality of democracy', 'GE': 'Government efficacy', 'EP': 'Economic performance', 'EQ': 'Income and wealth equality'}


def dclass(w):
    w = w.lower()
    if w.startswith('same as scenario'):
        return 'same as ii'
    if w.startswith('down or flat') or w.startswith('flat, or down'):
        return 'flat or down'
    if w.startswith('down'):
        return 'down'
    if w.startswith('mixed') or 'mixed' in w and w.startswith('prices'):
        return 'mixed'
    if w.startswith('slightly up') or w.startswith('small') or w.startswith('up modestly'):
        return 'slightly up'
    if w.startswith('up'):
        return 'up'
    if w.startswith('flat') or w.startswith('near trend'):
        return 'flat'
    raise SystemExit(f'unclassed scenario word: {w}')


srows = []
for s in V7['scenarios']['items']:
    row = {'key': s['id'], 'name': s['name'], 'assumptions': s['assumptions'], 'watch': s.get('watch', []), 'sources': s.get('sources', [])}
    for f in FAM:
        row[f] = s[f]['dir']
        row[f + '_class'] = dclass(s[f]['dir'])
        row[f + '_why'] = s[f]['why']
    srows.append(row)
datasets['scenarios-2030'] = {
    'spec': 'S06', 'kind': 'v7', 'title': 'Eight scenarios and the direction each would move four outcome families',
    'evidence': 'Estimate', 'grade': 'conditional directions, no forecast',
    'key': 'key', 'families': FAM,
    'fields': [{'name': 'key', 'type': 'id'}, {'name': 'name', 'type': 'label'}] +
              [{'name': f, 'type': 'words', 'label': FAM[f]} for f in FAM] + [{'name': f + '_class', 'type': 'category'} for f in FAM],
    'class_values': ['up', 'slightly up', 'flat', 'flat or down', 'down', 'mixed', 'same as ii'],
    'class_rules': ['A glyph or tint is a reading aid only; the four families are never added or tallied, so no badge, count or title may say "all four up".',
                    '"same as ii" points to scenario ii and must print as words; it is no direction of its own.'],
    'class_method': ("The studio's coarse reading of V7's direction words, for a glyph or tint only. The words are V7's and always print beside any glyph. "
                     "Words that start 'up' read up, except 'up modestly'; 'slightly up', 'up modestly' and 'small and slow' read slightly up; 'flat', 'near trend' and 'flat through 2036' read flat; "
                     "'down or flat' and 'flat, or down if ...' read flat or down; 'down' reads down; 'mixed' and 'prices down ...; employment effects mixed' read mixed; "
                     "'same as scenario ii' points to scenario ii."),
    'rows': srows, 'intro': V7['scenarios']['intro'],
    'source_line': atlas_line('reform outcomes, eight scenarios', 'Conditional directions to 2036 from a 2026 baseline', 'United States',
                              'Each scenario gives a direction only if its assumptions hold. It is no forecast, gives no odds, and the four families are never added together.'),
    'notes': ['DQ prints as "Quality of democracy" (DR-39).', 'Title verbs take "would" or "may": these are conditional estimates (section 15).'],
}

# S09 Timeline: history events on four threads
TH = {t['id']: t for t in V7['history']['threads']}
ev = sorted(V7['history']['events'], key=lambda e: e['date'])
erows = [{'key': f'E{i + 1:02d}', 'date': e['date'], 'year': int(e['date'][:4]), 'thread': e['thread'], 'thread_label': TH[e['thread']]['label'],
          'title': e['title'], 'mechanism': e['mechanism'], 'loop': e.get('loop'), 'source_text': e['source_text'], 'grade': e['quality']}
         for i, e in enumerate(ev)]
datasets['history-events'] = {
    'spec': 'S09', 'kind': 'v7', 'title': 'Twenty-four changes in the rules, 1870 to 2026, on four threads',
    'evidence': 'Finding', 'grade': 'documented', 'key': 'key',
    'threads': [{'id': t['id'], 'label': t['label'], 'question': t['question']} for t in V7['history']['threads']],
    'fields': [{'name': 'key', 'type': 'id'}, {'name': 'date', 'type': 'date'}, {'name': 'thread', 'type': 'category'}, {'name': 'title', 'type': 'label'}],
    'rows': erows, 'events_note': V7['history']['events_note'],
    'source_line': atlas_line('history, 24 events', 'February 3, 1870 to June 29, 2026', 'United States',
                              'Each event rests on a statute, ruling, constitutional text or official record, cited in its own row; the size of any effect comes from the source named beside it.'),
    'notes': ['Event keys E01 to E24 are the studio\'s, in date order; V7 events carry no IDs.'],
}

# S10 Evidence mix: 433 claims by confidence across the 16 everyday questions
GR = ['documented', 'well-supported', 'plausible', 'contested']
HUB = {h['id']: (h.get('title') or h.get('name')) for h in V7['hubs']}
cnt = collections.defaultdict(collections.Counter)
for c in V7['claims'].values():
    cnt[c['pathway']][c['confidence']] += 1
crow = []
for p in V7['pathways']:
    k = cnt[p['id']]
    crow.append({'key': p['id'], 'title': p['title'], 'question': p['question'], 'hub': p['hub'], 'hub_title': HUB[p['hub']],
                 **{g: k[g] for g in GR}, 'value': sum(k.values())})
datasets['claims-by-grade'] = {
    'spec': 'S10', 'kind': 'v7', 'title': 'How sure each everyday answer is: 433 claims by evidence grade',
    'evidence': 'Finding', 'grade': 'documented', 'key': 'key', 'grades': GR,
    'grade_meaning': {'documented': 'on the public record', 'well-supported': 'strong research evidence', 'plausible': 'some evidence', 'contested': 'evidence disputed'},
    'fields': [{'name': 'key', 'type': 'id'}, {'name': 'title', 'type': 'label'}, {'name': 'value', 'type': 'number', 'unit': 'claims'}] +
              [{'name': g, 'type': 'number', 'unit': 'claims'} for g in GR],
    'rows': crow, 'totals': {g: sum(r[g] for r in crow) for g in GR},
    'source_line': atlas_line('claims register, 433 claims across 16 everyday questions', 'Claims checked through October 15, 2026', 'United States',
                              'Grades are the atlas\'s own, defined on its evidence page; a claim\'s grade covers that claim alone.'),
    'notes': ['Grades never take Pillar Red (R10 of the research brief); the atlas draws grades as line textures, so a fill needs a texture or tint step that survives grayscale.'],
}

# Public series from the research lead (DR-46). Each CSV has a sidecar meta.json with a ready source line.
PUBLIC_SPECS = {
    'census-spm-child-poverty': ('S02', 'child-poverty-spm', 'Line with event notes'),
    'census-cps-reported-voting': ('S04', 'turnout-by-age', 'Dumbbell'),
    'census-hvs-homeownership-by-race-annual': ('S05', 'homeownership-by-race', 'Small multiples'),
    'ballotpedia-rcv-prohibitions-by-state': ('S07', 'rcv-bans', 'Map'),
}
public_found = {}
if PUBLIC.exists():
    for p in sorted(PUBLIC.glob('*.csv')):
        meta_p = p.with_suffix('.meta.json')
        meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
        with p.open(newline='') as fh:
            prow = list(csv.DictReader(fh))
        for r in prow:
            for k, v in list(r.items()):
                try:
                    r[k] = float(v) if v not in ('', None) and any(ch.isdigit() for ch in v) and v.replace('.', '', 1).replace('-', '', 1).isdigit() else v
                except (TypeError, ValueError):
                    pass
                if isinstance(r[k], float) and r[k].is_integer() and k in ('year',):
                    r[k] = int(r[k])
        public_found[p.stem] = {'file': str(p.relative_to(ROOT)), 'meta': meta, 'rows': prow, 'columns': list(prow[0].keys()) if prow else []}

# How each public series becomes chart rows: which rows, which fields make the key, which field holds the value
PUBLIC_RULES = {
    'child-poverty-spm': {
        'title': 'Children in poverty, Supplemental Poverty Measure and official measure, 2009 to 2025',
        'filter': lambda r: r['vintage'] == 'p60-290' and r['age_group'] == 'under_18',
        'key_fields': ['measure', 'year', 'series_variant'], 'value_field': 'percent',
        'required': lambda r: r['measure'] == 'spm',
        'source_tokens': ['Census Bureau', 'P60-290'],
        'notes': ['Use the current P60-290 table (D2-98). V7 prints the first-published 9.7 (2020), 5.2 (2021) and 13.4 (2024) percent; '
                  'the current table reads 9.6, 5.1 and 13.5 after the August 2026 revision and the 2024 reweighting.',
                  'Break years carry two rows (series_variant "earlier" and "later" method, for 2013, 2017 and 2019). Draw the break; never bridge it (R16).',
                  'Census: a change between two years is a descriptive change, not the effect of one policy.'],
    },
    'turnout-by-age': {
        'title': 'Reported voting rate by age group, November elections, 1964 to 2024',
        'filter': lambda r: True,
        'key_fields': ['age_group', 'year', 'base'], 'value_field': 'voted_pct',
        'required': lambda r: r['base'] == 'citizen_voting_age_population' and r['age_group'] != 'all' and int(float(r['year'])) in (2020, 2024),
        'source_tokens': ['Census Bureau', 'Table A-1'],
        'notes': ['S04 compares 2020 and 2024 for the four age groups, citizens 18 and over (the required rows). Other rows are context.',
                  'Rates are what respondents reported, which runs higher than counted ballots; say so in the chart.'],
    },
    'homeownership-by-race': {
        'title': 'Homeownership rate by race and ethnicity of householder, 1994 to 2025',
        'filter': lambda r: True,
        'key_fields': ['group', 'year', 'race_definition', 'series_variant'], 'value_field': 'rate_pct',
        'required': lambda r: r['series_variant'] == 'standard',
        'source_tokens': ['Census Bureau', 'Table 22'],
        'notes': ['Race categories changed in 2003, so the Black and non-Hispanic White lines break there. Draw the break.',
                  'The 2025 annual figure leaves out October 2025, when no data were collected. The latest quarter (third quarter of 2026) is in the dataset homeownership-by-race-quarterly.'],
    },
    'rcv-bans': {
        'title': 'States that prohibit ranked-choice voting, as of November 2026',
        'filter': lambda r: True,
        'key_fields': ['code'], 'value_field': None,
        'required': lambda r: True,
        'source_tokens': ['Ballotpedia'],
        'notes': ['Ballotpedia is a secondary source; V7 cites the National Conference of State Legislatures (W049), whose page refused automated reading. '
                  'Both give 19 states, matching V7 repair log row RL47.',
                  'Mark each state with data-key="<code>" data-category="<status>" data-field="status". Every state and DC must be drawn.'],
    },
}
for stem, (spec, did, form) in PUBLIC_SPECS.items():
    hit = public_found.get(stem)
    if not hit:
        datasets[did] = {'spec': spec, 'kind': 'public', 'pending': True, 'title': f'{form}: waiting for the research lead ({stem})'}
        continue
    m, rule = hit['meta'], PUBLIC_RULES[did]
    prow = [dict(r) for r in hit['rows'] if rule['filter'](r)]
    for r in prow:
        for k in ('year', 'quarter', 'enacted_year'):
            if isinstance(r.get(k), float):
                r[k] = int(r[k])
        if did == 'rcv-bans':
            r['status'] = {'all': 'bans in all elections', 'some': 'bans in some elections'}.get(r.get('scope') or '', 'no ban')
        r['key'] = '|'.join(str(r[f]) for f in rule['key_fields'])
    keys = [r['key'] for r in prow]
    if len(keys) != len(set(keys)):
        raise SystemExit(f'{did}: key fields {rule["key_fields"]} do not make unique keys')
    datasets[did] = {
        'spec': spec, 'kind': 'public', 'title': rule['title'], 'evidence': 'Finding', 'grade': 'official statistic' if 'census' in stem else 'secondary compilation',
        'file': hit['file'], 'key': 'key', 'key_fields': rule['key_fields'], 'value_field': rule['value_field'],
        'columns': hit['columns'] + (['status'] if did == 'rcv-bans' else []) + ['key'],
        'rows': prow, 'required_keys': [r['key'] for r in prow if rule['required'](r)],
        'source_line': m.get('source_line'), 'source_tokens': rule['source_tokens'], 'meta': m, 'notes': rule['notes'],
    }
# Extra public tables beside the ten (not specimen datasets): latest quarter and initiative states
for stem, did in (('census-hvs-homeownership-by-race-quarterly', 'homeownership-by-race-quarterly'), ('ballotpedia-citizen-initiative-states', 'initiative-states')):
    hit = public_found.get(stem)
    if hit:
        datasets[did] = {'spec': None, 'kind': 'public', 'title': hit['meta'].get('title_or_table'), 'file': hit['file'], 'rows': hit['rows'],
                         'source_line': hit['meta'].get('source_line'), 'meta': hit['meta']}

# Verifier hooks: which keys a figure must draw, and which words its source line must carry
for did, ds in datasets.items():
    if ds.get('kind') == 'v7':
        ds['source_tokens'] = ['Atlas V7']
        ds['required_keys'] = [r['key'] for r in ds['rows']]
datasets['stock-trading-ban']['source_tokens'] = ['Atlas V7', 'Program for Public Consultation']
datasets['stock-trading-ban']['required_keys'] = ['support-republicans', 'support-democrats']

# The editor's disclosure (D2-80, D2-106): V7's renderer prints it on the nomination reforms (R-01, R-02, R-47),
# word for word as here. Charts on nomination, ranked-ballot or election-rule data carry it too.
DISCLOSURE = ("Oath & Action's editor works with the Yes on 3 campaign for Massachusetts Question 3 and promotes it through "
              "Veterans for All Voters, where he is Massachusetts state lead. He also co-leads Ranked Choice Melrose, a local campaign.")
for did in ('rule-changes-by-instrument', 'scenarios-2030', 'rcv-bans', 'rule-changes'):
    datasets[did]['required_text'] = [DISCLOSURE]
    datasets[did].setdefault('notes', []).append('Print the editor\'s disclosure word for word, labeled "Disclosure:", where the reader sees it with the chart (D2-106).')

# Extra V7 material the makers may use beside the ten (big numbers, social card, captions)
extras = {
    'numbers': V7['numbers'],
    'link_grades': dict(collections.Counter((l.get('evidence') or l.get('grade')) for l in V7['links'].values())),
    'link_delays': dict(collections.Counter(l.get('delay') for l in V7['links'].values())),
    'homeownership_q2_2026_v7': next((m['how'] for o in V7['overlays'] if o['id'] == 'DV-RACE' for m in o['mechanisms'] if 'homes' in m['how']), None),
}

SPECIMENS = [
    ('S01', 'Big number in context', 'stock-trading-ban', 'Do Republicans and Democrats agree on anything about Congress?',
     'One figure set large, the two party figures beside it with names printed, and the House and Senate votes as context. Party marks in neutral inks (DR-48).'),
    ('S02', 'Line with event notes', 'child-poverty-spm', 'What happened to child poverty when the expanded child tax credit was paid, and after it lapsed?',
     'One series in Charcoal, events as notes inside the plot, the unit once, a true minus where needed, the Census revision stated. The title must not credit one policy alone.'),
    ('S03', 'Ranked bar', 'rule-changes-by-instrument', 'Who changed the rules: voters, courts or legislatures?',
     'Bars start at zero, direct labels, the grouping note printed. Optional: split each bar by direction without red.'),
    ('S04', 'Dot plot or dumbbell', 'turnout-by-age', 'Which age groups vote, and did that change between two elections?',
     'Two years per row, the change labeled in words and numbers, survey self-report qualified.'),
    ('S05', 'Small multiples', 'homeownership-by-race', 'How far apart are homeownership rates by race, and has the gap closed?',
     'One panel per group, one shared scale (or the subtitle says otherwise), each panel highlights its group over the others in Stone.'),
    ('S06', 'Comparison table', 'scenarios-2030', 'If a reform path were followed, which way would each outcome move?',
     "V7's words print in every cell; any glyph or tint follows the class method and is labeled as the studio's reading. Tests the diverging pair without red and blue."),
    ('S07', 'Map', 'rcv-bans', 'Where can a city adopt ranked-choice voting, and where has the state ruled it out?',
     'Categorical, with words in the key and on hover, a table equivalent listing every state, and the as-of date in the title or measure line.'),
    ('S08', 'Unit chart', 'rule-changes', 'Have the rules been moving toward voters or away from them?',
     'One mark per repair-log row, keyed by its RL id; direction by shape or position as well as tint; the coding note one click or one line away.'),
    ('S09', 'Timeline', 'history-events', 'Which rule changes since 1870 decided who counts, who governs, who owns and who checks?',
     'Four thread lanes, dates on a true time scale, event names printed, every event documented.'),
    ('S10', 'Evidence mix', 'claims-by-grade', 'How much of each everyday answer rests on documented fact?',
     'A share per question across four grades, sorted, with grades readable in grayscale and never in red.'),
]
specimens = [{'id': i, 'form': f, 'dataset': ds, 'reader_question': q, 'requirements': req,
              'evidence': datasets[ds].get('evidence')} for i, f, ds, q, req in SPECIMENS]

out = {
    'built': '2026-11-06', 'about': __doc__.strip().splitlines()[0],
    'atlas_snapshot': SNAP, 'source_line_order': 'publisher, title or table, observation period, geography, date retrieved, qualification',
    'specimens': specimens, 'datasets': datasets, 'extras': extras,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
pend = [k for k, v in datasets.items() if v.get('pending')]
print(f'wrote {OUT.relative_to(ROOT)}: {len(datasets)} datasets, {len(specimens)} specimens; pending: {pend or "none"}')
