"""research_atlas_recheck.py: Phase 0's 2,644 atlas comparisons rerun against today's Atlas V7, as data only (DR-250).

Run:  python3 -I work/build/scripts/phase-3/research_atlas_recheck.py [--write]

Reads, never writes:
  work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json   (what each page showed, as Phase 0 recorded it)
  work/build/scripts/phase-0/atlas_reconcile_extract.py           (Phase 0's own V7 helpers: its header only, which
                                                                   reads no source file)
  work/extract/atlas-v7-data.json, checked equal to work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json
Writes, with --write, new files only:
  work/research/20261113_Atlas-Recheck-Data.json
  work/research/20261113_Atlas-Recheck-Table.md

Phase 0 read three supplied documents that are not in the repository (V5 Polished, the Atlas Visual System and Concepts
V2 stay out of git), so this rerun takes each page's side of a comparison from Phase 0's recorded data and recomputes
the V7 side from today's model with Phase 0's own rules. A comparison can change only if the V7 side changed. Families
whose page side Phase 0 did not record are tested through every V7-side value Phase 0 did record, and otherwise rest on
the model's provenance, which the output states family by family.
"""
import collections
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P0 = ROOT / 'work/handoffs/phase-0'
P0_SCRIPT = ROOT / 'work/build/scripts/phase-0/atlas_reconcile_extract.py'
V7_EXTRACT = ROOT / 'work/extract/atlas-v7-data.json'
V7_MODEL = ROOT / 'work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json'
OUT_JSON = ROOT / 'work/research/20261113_Atlas-Recheck-Data.json'
OUT_MD = ROOT / 'work/research/20261113_Atlas-Recheck-Table.md'
MODEL_SHA = 'ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


# Phase 0's header: the V7 model, norm, grade_of, delay_of, kinds_of and ID_RE, exactly as Phase 0 ran them
src = P0_SCRIPT.read_text(encoding='utf-8')
cut = src.index('# ------------------------------------------------------------ HTML to lines')
G = {'__file__': str(P0_SCRIPT), '__name__': 'phase0_header'}
exec(compile(src[:cut], str(P0_SCRIPT), 'exec'), G)
V7, NODES, LINKS, LOOPS, REFORMS, DOMAINS = G['V7'], G['NODES'], G['LINKS'], G['LOOPS'], G['REFORMS'], G['DOMAINS']
ISSUES = G['ISSUES']
norm, grade_of, delay_of, kinds_of = G['norm'], G['grade_of'], G['delay_of'], G['kinds_of']

D0 = json.loads((P0 / '20261020_Atlas-Reconciliation-Data.json').read_text(encoding='utf-8'))

# Phase 0's derived maps, copied from its script (lines 568 to 575, 724 to 760, 973 to 1016)
DOM_SHEET = {k: (n['domain'].split('/')[0] if n['domain'] else n['cluster']) for k, n in NODES.items()}
TEX = {'documented': 'solid', 'well-supported': 'solid', 'plausible': 'dashed', 'plausible_contested': 'dash-dot',
       'hypothesis': 'dotted'}
SIGN = {'+': 'arrowhead (raises)', '-': 'bar (lowers)', None: 'open diamond (decides)'}
EV_WORD = {'documented': 'on the record', 'well-supported': 'strong evidence', 'plausible': 'some evidence',
           'plausible_contested': 'disputed', 'hypothesis': 'untested'}


def lead_code(c):  # Phase 0's second lead_code (line 905), the one in force when its comparisons ran
    c = (c or '').replace('−', '-').strip()
    m = re.match(r'^([+\-]?[LMS]|0|\?)', c)
    return m.group(1) if m else c


vars_on = collections.defaultdict(list)
for k in NODES:
    vars_on[DOM_SHEET[k]].append(k)
filed = collections.defaultdict(list)
for k, L in LINKS.items():
    filed[DOM_SHEET[L['to']]].append(k)


def sheet_computed(code):
    vs = set(vars_on[code])
    lk = filed[code]
    loops_through = {lp for lp, Lp in LOOPS.items() if Lp['links'] and
                     any(LINKS[l]['from'] in vs or LINKS[l]['to'] in vs for l in Lp['links'])}
    ra = {r for r, R in REFORMS.items() if not R['rejected'] and
          any((t in vs) or (t in LINKS and LINKS[t]['to'] in vs) for t in R['targets'])}
    ra2 = {r for r, R in REFORMS.items() if not R['rejected'] and
           any((t in vs) or (t in LINKS and (LINKS[t]['to'] in vs or LINKS[t]['from'] in vs)) for t in R['targets'])}
    evc = collections.Counter(LINKS[l]['evidence'] for l in lk)
    return {'variables': len(vs), 'connections': len(lk), 'loops': len(loops_through),
            'reforms (targets into sheet)': len(ra), 'reforms (targets touching sheet)': len(ra2),
            'issues': len(DOMAINS[code]['issues']) if code in DOMAINS else None, 'evidence': dict(evc),
            'leave': sum(1 for k, L in LINKS.items() if L['from'] in vs and DOM_SHEET[L['to']] != code),
            'reform_ids': sorted(ra2), 'loop_ids': sorted(loops_through)}


FAM = collections.OrderedDict()  # family -> {'n': comparisons, 'conflicts': [...], 'method': ..., 'p0': (n, conflicts)}


def fam(name, p0n, p0c, method):
    FAM[name] = {'n': 0, 'conflicts': [], 'method': method, 'p0_comparisons': p0n, 'p0_conflicts': p0c}
    return FAM[name]


def cmp(f, item, shown, v7, typ):
    f['n'] += 1
    if shown != v7:
        f['conflicts'].append({'item': item, 'shown': str(shown), 'v7_today': str(v7), 'type': typ})


# 1. Register connection rows: 7 per row plus each from-sheet tag (Phase 0: reg_rows * 7 + tags)
f = fam('Concepts V2 Register connection rows', 908, 0, 'recomputed from the recorded rows')
for r in D0['register_rows']:
    L = LINKS[r['id']]
    cmp(f, r['id'] + ' from and to', '%s to %s' % (r['from'], r['to']), '%s to %s' % (L['from'], L['to']), 'structure')
    cmp(f, r['id'] + ' sign glyph', r['glyph'], SIGN[L['polarity']], 'sign')
    cmp(f, r['id'] + ' texture', r['texture'], TEX[L['evidence']], 'encoding')
    cmp(f, r['id'] + ' grade', grade_of(r['grade']), L['evidence'], 'grade')
    cmp(f, r['id'] + ' delay', delay_of(r['delay']), L['delay'], 'delay')
    cmp(f, r['id'] + ' name', norm(r['name']), norm(L['name']), 'label')
    cmp(f, r['id'] + ' filing sheet', r['code'], DOM_SHEET[L['to']], 'structure')
    if r['from_sheet_shown']:
        cmp(f, r['id'] + ' from-sheet tag', r['from_sheet_shown'], DOM_SHEET[r['from']], 'label')

# 2. Register variable cards: title, type, loops, higher-means, plus each secondary domain
f = fam('Concepts V2 Register variable cards', 213, 0, 'recomputed from the recorded cards')
KIND = {'stock': 'Stock', 'flow': 'Flow', 'auxiliary': 'Condition', 'driver': 'Outside driver'}
for v in D0['register_vars']:
    N = NODES[v['id']]
    cmp(f, v['id'] + ' title', norm(v['title']), norm(N['title']), 'label')
    cmp(f, v['id'] + ' type', v['kind'].startswith(KIND[N['type']]), True, 'label')
    lp = re.search(r'Loops ([A-Za-z0-9, ]+?)(?: ·|$)', v['kind'])
    shown_loops = set(x.strip() for x in lp.group(1).split(',')) if lp else set()
    v7_loops = {k for k, Lp in LOOPS.items() if v['id'] in [c[0] for c in Lp['chain']] or
                any(v['id'] in (LINKS[l]['from'], LINKS[l]['to']) for l in Lp['links'])}
    cmp(f, v['id'] + ' loops', sorted(shown_loops), sorted(k for k in v7_loops if LOOPS[k]['links']), 'structure')
    hm = norm(v['higher'])
    ok = hm.replace('higher means', 'a higher value means') in norm(N['increase_means']) or hm[12:40] in norm(N['increase_means'])
    cmp(f, v['id'] + ' higher means', ok, True, 'label')
    also = re.search(r'Also under (D\d\d)', v['kind'])
    if also:
        doms = (N['domain'] or '').split('/')
        cmp(f, v['id'] + ' secondary domain', also.group(1), doms[1] if len(doms) > 1 else None, 'structure')

# 3. Register reform rows: title and route list
f = fam('Concepts V2 Register reform rows', 172, 0, 'recomputed from the recorded rows')
for r in D0['register_reforms']:
    R = REFORMS[r['id']]
    cmp(f, r['id'] + ' title', norm(r['title']), norm(R['title']), 'label')
    cmp(f, r['id'] + ' routes', r['routes'] if r['routes'] else [x['route'] for x in R['routes']],
        [x['route'] for x in R['routes']], 'structure')

# 4. Effect cells: the page side was not recorded
f = fam('Concepts V2 Register effect cells', 344, 0, 'not recomputed: the cells were read from the SVG and not recorded')

# 5. Sheet figures and index table
f = fam('Concepts V2 Register sheet figures and index table', 146, 0,
        'recomputed from the recorded sheet and index figures; busiest crossings by Phase 0’s recorded counts')
for code, nums in D0['sheet_stats_shown'].items():
    c = sheet_computed(code)
    for key in ('variables', 'connections', 'loops', 'issues', 'leave'):
        if nums[key] is not None and c[key] is not None:
            cmp(f, code + ' ' + key, nums[key], c[key], 'structure')
    if nums['reforms'] is not None:
        cmp(f, code + ' reforms', nums['reforms'] in (c['reforms (targets into sheet)'], c['reforms (targets touching sheet)']),
            True, 'structure')
    if nums['evidence']:
        shown = {w.strip(): int(n) for n, w in re.findall(r'(\d+) ([a-z ]+?)(?: ·|$)', nums['evidence'])}
        cmp(f, code + ' evidence mix', shown, {EV_WORD[g]: n for g, n in c['evidence'].items()}, 'grade')
for code, nums in D0['index_rows_shown'].items():
    c = sheet_computed(code)
    exp = [str(c['variables']), str(c['connections']), str(c['loops']), None, str(c['issues']) if c['issues'] else '–']
    for k, lab in ((0, 'variables'), (1, 'connections'), (2, 'loops'), (4, 'issues')):
        cmp(f, code + ' index ' + lab, nums[k], exp[k], 'structure')
    cmp(f, code + ' index reforms', nums[3], str(D0['sheet_stats_shown'][code]['reforms']), 'structure')
cross = collections.Counter()
for k, L in LINKS.items():
    a, b = DOM_SHEET[L['from']], DOM_SHEET[L['to']]
    if a != b:
        cross[(a, b)] += 1
for (pair, n) in D0['busiest_crossings_computed'][:4]:
    a, b = pair.split(' to ')
    cmp(f, 'busiest crossing ' + pair, n, cross[(a, b)], 'structure')

# 6. Field Guide specimens: six word checks and two glyph checks each
f = fam('Concepts V2 Field Guide specimens', 160, 0, 'recomputed from the recorded specimens and glyph counts')
RANK = ['hypothesis', 'plausible_contested', 'plausible', 'well-supported', 'documented']
DIRMAP = {'running_up': 'running and building', 'running_down': 'running and wearing down', 'running': 'working',
          'unclear': 'direction unclear', 'dormant': 'switched off in practice'}
TEXNAME = {'solid': 'solid', '8 6': 'dashed', '0.1 5.2': 'dotted', '0.1 4.4': 'dotted', '10 4 2 4': 'dash-dot'}
for s, g in zip(D0['field_guide'], D0['field_guide_glyphs']):
    LP = LOOPS[s['loop']]
    cmp(f, s['loop'] + ' type', s['type'], LP['type'], 'structure')
    cmp(f, s['loop'] + ' turn time', s['delay'], LP['delay'], 'delay')
    cmp(f, s['loop'] + ' title', norm(s['title']), norm(LP['title']), 'label')
    cmp(f, s['loop'] + ' ring order', s['ring'], [c[0] for c in LP['chain']], 'structure')
    grades = [LINKS[l]['evidence'] for l in LP['links']]
    weak = s['weak']
    if weak.startswith('Every step'):
        cmp(f, s['loop'] + ' weakest step', len(set(grades)) == 1 and grade_of(weak) == grades[0], True, 'grade')
    else:
        cmp(f, s['loop'] + ' weakest step', grade_of(weak.split('Now:')[0]), min(grades, key=RANK.index), 'grade')
    now = re.search(r'Now: (.+)$', weak)
    cmp(f, s['loop'] + ' state', now.group(1) if now else DIRMAP.get(LP['direction'], LP['direction']),
        DIRMAP.get(LP['direction'], LP['direction']), 'label')
    shown_tex = collections.Counter()
    for k, n in g['textures'].items():
        shown_tex[TEXNAME.get(k, k)] += n
    cmp(f, s['loop'] + ' ring textures', dict(shown_tex), dict(collections.Counter(TEX[LINKS[l]['evidence']] for l in LP['links'])), 'encoding')
    pos = sum(1 for l in LP['links'] if LINKS[l]['polarity'] == '+')
    neg = sum(1 for l in LP['links'] if LINKS[l]['polarity'] == '-')
    cmp(f, s['loop'] + ' end marks', (g['arrowheads_or_triangles'] - 1, g['bars']), (pos, neg), 'sign')

# 7. Who Can Act: the page side was not recorded; Phase 0's recorded V7 tallies are compared with today's
f = fam('Concepts V2 Who Can Act', 94, 0, 'V7 side only: Phase 0’s recorded route and effect tallies against today’s')
live = {k: R for k, R in REFORMS.items() if not R['rejected']}
rc = collections.Counter(x['route'] for R in live.values() for x in R['routes'])
cmp(f, 'route counts (live reforms)', dict(rc), D0['who_can_act']['route_counts'], 'structure')
for fm in ('DQ', 'GE', 'EP', 'EQ'):
    codes = collections.Counter(lead_code(R['effects'][fm]) for R in live.values())
    cmp(f, fm + ' effect codes (live reforms)', dict(codes), D0['who_can_act']['families'][fm]['codes'], 'structure')
f['n'] = 0  # these are V7-side checks, not the page comparisons; counted apart below
f['v7_side_checks'] = 5

# 8. Ledger rows: variables, links, loops, reforms (Phase 0 found the D03 and D04 reform counts)
f = fam('Concepts V2 Ledger rows', 48, 2, 'recomputed from the recorded rows')
for code, row in D0['ledger_shown'].items():
    vs = set(vars_on[code])
    vs_any = {k for k, n in NODES.items() if code in (n['domain'] or n['cluster']).split('/')}
    touch = sum(1 for L in LINKS.values() if L['from'] in vs or L['to'] in vs)
    touch_any = sum(1 for L in LINKS.values() if L['from'] in vs_any or L['to'] in vs_any)
    l1 = len({lp for lp, Lp in LOOPS.items() if any(LINKS[l]['from'] in vs or LINKS[l]['to'] in vs for l in Lp['links'])
              or any(c[0] in vs for c in Lp['chain'])})
    l2 = len({lp for lp, Lp in LOOPS.items() if any(LINKS[l]['from'] in vs_any or LINKS[l]['to'] in vs_any for l in Lp['links'])})
    live_n = sum(1 for R in live.values() if any((t in vs) or (t in LINKS and (LINKS[t]['from'] in vs or LINKS[t]['to'] in vs)) for t in R['targets']))
    cmp(f, code + ' variables', set(row['vars']) <= set(vars_on[code]) if row['vars'] else True, True, 'structure')
    cmp(f, code + ' links', row['links'] in (touch, touch_any), True, 'structure')
    cmp(f, code + ' loops', row['loops'] in (l1, l2), True, 'structure')
    cmp(f, code + ' reforms', row['reforms'], live_n, 'structure')
    if D0['ledger_computed'].get(code):
        c0 = D0['ledger_computed'][code]
        f.setdefault('v7_side', []).append(c0 == {'links touching first-domain vars': touch, 'links touching any-domain vars': touch_any,
                                                   'loops (first-domain)': l1, 'loops (any domain)': l2,
                                                   'reforms touching': sheet_computed(code)['reforms (targets touching sheet)'] if code in D0['sheet_stats_shown'] else None})

# 9. Circuit: the tally and area cards through Phase 0's recorded counts; pass-on examples and bundles not recorded
f = fam('Concepts V2 Circuit', 27, 0, 'V7 side for the tally and the four area cards (9); the 5 pass-on examples and '
        '13 drawn bundle counts were not recorded')
region_of = {n: rg['id'] for lay in V7['layers'].values() for rg in lay['regions'] for n in rg['nodes']}


def area(n):
    return region_of[n] if NODES[n]['layer'] == 'core' else NODES[n]['layer']


inside_area, cat = collections.Counter(), collections.Counter()
for k, L in LINKS.items():
    a, b = area(L['from']), area(L['to'])
    if a == b:
        inside_area[a] += 1
    elif a == 'X':
        cat['from outside drivers'] += 1
    elif a in 'ABCDE' and b in 'ABCDE':
        cat['between the five areas'] += 1
    else:
        cat['to, from or within the two lower layers'] += 1
shown_tally = (81, 38, 28, 15, 37)  # the page's words, as Phase 0's script quotes them in its finding text
exp = (sum(cat.values()), cat['between the five areas'], cat['to, from or within the two lower layers'],
       cat['from outside drivers'], sum(inside_area.values()))
for i, lab in enumerate(('crossing', 'between the five areas', 'lower layers', 'outside drivers', 'inside')):
    cmp(f, 'tally ' + lab, shown_tally[i], exp[i], 'structure')
for a, n in (('A', 6), ('B', 5), ('C', 5), ('D', 7)):
    cmp(f, 'area card ' + a, n, inside_area[a], 'structure')
f['v7_side'] = [D0['circuit_computed'] == {'inside': dict(inside_area), 'categories': dict(cat), 'crossing_total': sum(cat.values())}]

# 10. Other numeric claims, recomputed by Phase 0's own expressions
f = fam('Other numeric claims', 21, 0, 'recomputed from the recorded claims')
lay_n = collections.Counter(n['layer'] for n in NODES.values())
band_label = {'parameter': 'Numbers', 'feedback': 'Feedback', 'information': 'Information', 'rules': 'Rules',
              'power to change the rules': 'Power over the rules', 'goals': 'Goals and mindsets'}
V7_CLAIM = {
    'connections that cross from one layer to another': sum(1 for L in LINKS.values() if NODES[L['from']]['layer'] != NODES[L['to']]['layer']),
    'Power and accountability variables': lay_n['core'], 'How the economy reaches a household variables': lay_n['economy'],
    'Technology and its effects variables': lay_n['technology'],
    'Outside drivers among the 31': sum(1 for n in NODES.values() if n['type'] == 'driver'),
    'closed loops': sum(1 for Lp in LOOPS.values() if Lp['links']),
    'snowball (R) closed loops': sum(1 for Lp in LOOPS.values() if Lp['links'] and Lp['type'] == 'R'),
    'thermostat (B) closed loops': sum(1 for Lp in LOOPS.values() if Lp['links'] and Lp['type'] == 'B'),
    'closed with an untested step': sum(1 for Lp in LOOPS.values() if Lp['closure'].startswith('closed with')),
    'live reforms': len(live), 'issues': len(ISSUES)}
for c in D0['claims']:
    m = re.match(r'(R-\d\d) leverage band$', c['text'])
    v = band_label[REFORMS[m.group(1)]['band']] if m else V7_CLAIM[c['text']]
    cmp(f, c['text'], str(c['shown']), str(v), 'structure')
    f.setdefault('v7_side', []).append(str(c['v7']) == str(v))

# 11. Direction-and-sign sentences, reparsed from the recorded lines (each holds a connection ID)
f = fam('Direction-and-sign sentences', 78, 0, 'reparsed from the lines Phase 0 recorded with each identifier')
VAR = r"\b([A-Z]{1,2}\d{1,2})(?: [a-z][a-z ,']*?)?"
PAIR1 = re.compile(VAR + r' to ' + VAR + r' through ([A-Z]{1,2}\d{2}|LX\d) (positive|negative)')
PAIR2 = re.compile(VAR + r' to ' + VAR + r' (positive|negative) through ([A-Z]{1,2}\d{2}|LX\d)')
seen_lines = []
for o in D0['occurrences']:
    key = (o['file'], o['location'], o['text'])
    if key not in seen_lines:
        seen_lines.append(key)
for (_fl, _lc, t) in seen_lines:
    t = html.unescape(t)
    hits = [(a, b, l, s) for a, b, l, s in PAIR1.findall(t)] + [(a, b, l, s) for a, b, s, l in PAIR2.findall(t)]
    for a, b, l, s in hits:
        if l not in LINKS:
            continue
        L = LINKS[l]
        cmp(f, l + ' direction', '%s to %s' % (a, b), '%s to %s' % (L['from'], L['to']), 'structure')
        cmp(f, l + ' sign', '+' if s == 'positive' else '-', L['polarity'], 'sign')

# 12, 13. Not recorded
fam('AVS production table rows', 48, 0, 'not recomputed: the rows were read from the lines after each ID, not recorded')
fam('Connection names shown without an ID', 127, 0, 'not recomputed: the lines were matched by name, not recorded')

# 14. Connection IDs with a grade, delay or glyph beside them: the recorded "shown" attributes
f = fam('Connection IDs with a grade, delay or glyph shown beside them', 179, 0, 'recomputed from the recorded attributes')
GL = {'arrowhead (raises)': '+', 'bar (lowers)': '-', 'open diamond (decides)': None}
for o in D0['occurrences']:
    if 'connection' not in o['kinds'] or not o['shown']:
        continue
    L = LINKS[o['id']]
    ok = True
    for part in o['shown'].split('; '):
        if part.startswith('grade '):
            g = part[6:]
            ok &= g == L['evidence'] or (g == 'contested' and bool(L['contested']))
        elif part.startswith('delay '):
            ok &= part[6:] == L['delay']
        elif part.startswith('glyph '):
            end, tex = part[6:].rsplit(', ', 1)
            ok &= GL.get(end) == L['polarity'] and tex == TEX[L['evidence']]
    f['n'] += 1
    if not ok:
        f['conflicts'].append({'item': o['id'], 'shown': o['shown'], 'v7_today': '%s %s %s' % (L['evidence'], L['delay'], L['polarity']),
                               'type': 'attribute', 'where': o['file'] + ', ' + o['location']})

# 15. Loop titles beside loop IDs, from the recorded lines
f = fam('Loop titles printed beside loop IDs', 42, 0, 'reparsed from the recorded lines')
ID_RE = G['ID_RE']
for o in D0['occurrences']:
    if 'loop' not in o['kinds'] or 'standards rule' in o['kinds']:
        continue
    t = html.unescape(o['text'])
    m = re.search(r'(?<![A-Za-z0-9-])' + re.escape(o['id']) + r'(?![A-Za-z0-9])', t)
    if not m:
        continue
    after = t[m.end():].strip(' :·,')
    if o['id'] in NODES and 'variable' in o['kinds'] and not re.match(r'^[A-Z][a-z]', after or ''):
        continue
    if re.match(r'^(Variables?|Links?|Loops?|Reforms?)\b', after):
        continue
    if after and len(after) > 25 and not ID_RE.match(after) and re.match(r'^[A-Z][a-z]', after):
        lt = LOOPS[o['id']]['title']
        ok = norm(after).startswith(norm(lt)) or norm(lt)[:20] in norm(after)
        if o['id'] in NODES and not ok and norm(NODES[o['id']]['title'])[:20] in norm(after):
            continue  # a colliding ID used as a variable here, which Phase 0 set aside by its meaning test
        cmp(f, o['id'] + ' title', ok, True, 'label')

fam('Reform effect words (Concepts V2 and AVS outcome figure)', 24, 0, 'not recomputed: read from the lines after each heading')
fam('AVS domain titles and layer rows', 13, 0, 'not recomputed: read from the lines after each code')

# Identifier resolution: every recorded identifier occurrence still resolves to the same record kinds
id_changed = []
for o in D0['occurrences']:
    if o['kinds'] in (['route'], ['effect code']) or 'standards rule' in o['kinds'] or 'placeholder' in o['kinds']:
        continue
    now = kinds_of(o['id'])
    if sorted(now) != sorted(o['kinds']):
        id_changed.append({'id': o['id'], 'then': o['kinds'], 'now': now, 'where': o['file']})


def main():
    write = '--write' in sys.argv
    model_ok = sha(V7_EXTRACT) == sha(V7_MODEL) == MODEL_SHA
    rows, tot_p0, tot_re, tot_conf = [], 0, 0, 0
    for name, f in FAM.items():
        tot_p0 += f['p0_comparisons']
        tot_re += f['n']
        tot_conf += len(f['conflicts'])
        rows.append((name, f['p0_comparisons'], f['p0_conflicts'], f['n'], len(f['conflicts']), f['method'],
                     all(f.get('v7_side', [True]))))
    changed = []
    for name, f in FAM.items():
        if len(f['conflicts']) != f['p0_conflicts'] and f['n']:
            changed.append(name)
    ledger_now = sorted(c['item'] for c in FAM['Concepts V2 Ledger rows']['conflicts'])
    data = {
        'run': 'November 13, 2026, research lead, Phase 3 round 3 (DR-250)',
        'v7_model': {'file': str(V7_MODEL.relative_to(ROOT)), 'sha256': MODEL_SHA, 'extract_equal': model_ok},
        'families': [{'family': r[0], 'phase0_comparisons': r[1], 'phase0_conflicts': r[2], 'rerun_comparisons': r[3],
                      'rerun_conflicts': r[4], 'method': r[5], 'v7_side_equal_to_phase0': r[6],
                      'conflicts': FAM[r[0]]['conflicts']} for r in rows],
        'totals': {'phase0': tot_p0, 'rerun': tot_re, 'rerun_conflicts': tot_conf},
        'families_whose_result_changed': changed,
        'identifier_occurrences_rechecked': sum(1 for o in D0['occurrences'] if o['kinds'] not in (['route'], ['effect code'])
                                                and 'standards rule' not in o['kinds'] and 'placeholder' not in o['kinds']),
        'identifier_kinds_changed': id_changed,
        'ledger_conflicts_now': ledger_now,
    }
    print(json.dumps({k: v for k, v in data.items() if k != 'families'}, indent=1, ensure_ascii=False))
    for r in rows:
        print('%-70s p0 %4d/%d  rerun %4d/%d  %s  v7-side-equal=%s' % (r[0][:70], r[1], r[2], r[3], r[4], r[5][:60], r[6]))
    if write:
        if OUT_JSON.exists() and json.loads(OUT_JSON.read_text(encoding='utf-8')) == data:
            print('data unchanged')
        else:
            OUT_JSON.write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
            print('wrote', OUT_JSON.relative_to(ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
