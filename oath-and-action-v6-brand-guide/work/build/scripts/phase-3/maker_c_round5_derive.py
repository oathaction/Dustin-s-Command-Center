"""The complex examples maker, Phase 3 round 5: the figure checks for Rules 14.142 to 14.144, the three charts in full
(contract R5-4; work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md).

    python3 -I work/build/scripts/phase-3/maker_c_round5_derive.py [--figures] [--json]

Round 5 needs no derived table. Example 1 draws S14's frozen file, fred-payrolls-monthly-change, as it stands (D3-1873);
examples 2 and 3 read the atlas model, work/extract/atlas-v7-data.json, snapshot of October 15, 2026.

facts() reads every figure the three examples print, by script, and stops on any value that has moved since the plan:
  example 1  the 57 months, the two preliminary months, each three-month average recomputed from the changes, the seven
             losses, the survey's margin (plus or minus 122,000, from the sidecar's with_margin source line) and the two
             drops past it (DR-239), the latest month and its average;
  example 2  Loops B4 and R10, the one variable they share (Variable C3), each step's sign, grade, delay and type, and
             the order the stepper takes through Variable C3;
  example 3  Reforms R-06, R-30 and R-38 on Loop R8: targets, band, the four effects with their qualifiers whole, the
             confidence line, the two grades, every route with its check date or none, and the drawing that holds every
             target.

--figures also checks every figure in the words of the three examples' files, once they exist, against facts(): the new
kit spec (title, measure line, notes, chart notes, alt, labels, annotations) and the three entry files and their plates
(every number and date the reader sees). Each check is named in the spec's notes_internal. --json prints facts().
Standard library only. Exits 1 on any failed check.
"""
import csv
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
DATA = os.path.join(GUIDE, 'work', 'build', 'data')
SPECS = os.path.join(GUIDE, 'work', 'build', 'chart-kit', 'specs')
ENTRIES = os.path.join(GUIDE, 'work', 'build', 'guide', 'entries')
SPECIMENS = os.path.join(GUIDE, 'work', 'build', 'guide', 'specimens')
ATLAS = os.path.join(GUIDE, 'work', 'extract', 'atlas-v7-data.json')
PLAN = os.path.join(GUIDE, 'work', 'handoffs', 'phase-3', '20261112_Chapter-14-Plan.json')
DATASET = 'fred-payrolls-monthly-change'
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
FAULTS = []
COUNT = [0]


def check(where, ok, what):
    COUNT[0] += 1
    if not ok:
        FAULTS.append(f'{where}: {what}')
    return ok


def need(ok, what):
    if not ok:
        raise SystemExit(f'maker_c_round5_derive: {what}')


def month_words(m):
    y, mo = m.split('-')
    return f'{MONTHS[int(mo) - 1]} {y}'


def read_csv(name):
    with open(os.path.join(DATA, name + '.csv'), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def read_json(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------------------------------------------------
# Example 1: S14 in full
# ---------------------------------------------------------------------------------------------------------------------
def example_1():
    rows = read_csv(DATASET)
    side = read_json(os.path.join(DATA, DATASET + '.meta.json'))
    months = [r['month'] for r in rows]
    ch = [float(r['change_thousands']) for r in rows]
    av = [float(r['avg3_thousands']) for r in rows]
    need(months[0] == '2022-01' and months[-1] == '2026-09' and len(rows) == 57, 'S14\'s window moved')
    need(all(r['status'] in ('final', 'preliminary') for r in rows), 'a status other than final or preliminary')
    pre = [r['month'] for r in rows if r['status'] == 'preliminary']
    need(pre == ['2026-08', '2026-09'], f'the preliminary months moved: {pre}')
    # each three-month average from the changes; January and February 2022 draw on two months before the window, which
    # the file does not hold (the spec's first note says so)
    for i in range(2, len(rows)):
        need(abs((ch[i] + ch[i - 1] + ch[i - 2]) / 3 - av[i]) < 1e-4, f'the average for {months[i]} is not its three months\' mean')
    losses = [m for m, v in zip(months, ch) if v < 0]
    need(losses == ['2025-01', '2025-06', '2025-08', '2025-10', '2025-12', '2026-02', '2026-07'], f'the losses moved: {losses}')
    # the margin: the Bureau's 90 percent interval for one month's change, as the sidecar's with_margin line prints it
    wm = side['source_line_variants']['with_margin']
    m_ = re.search(r'plus or minus ([\d,]+), from its Employment Situation technical note, October 2026 release', wm)
    need(m_ is not None, 'the sidecar\'s with_margin line no longer names the margin')
    margin = int(m_.group(1).replace(',', '')) / 1000
    need(margin == 122, f'the margin moved: {margin}')
    past = [m for m, v in zip(months, ch) if v < 0 and abs(v) > margin]
    need(past == ['2025-10', '2026-02'], f'DR-239\'s two drops past the margin moved: {past}')
    inside = [m for m, v in zip(months, ch) if v < 0 and abs(v) <= margin]
    gains_past = [m for m, v in zip(months, ch) if v > margin]
    in_band = [m for m, v in zip(months, ch) if abs(v) <= margin]
    since = [i for i, m in enumerate(months) if m >= '2025-01']
    return {
        'dataset': DATASET,
        'first': months[0], 'last': months[-1], 'n': len(rows),
        'window_words': f'{month_words(months[0])} to {month_words(months[-1])}',
        'preliminary': pre, 'preliminary_words': ' and '.join(MONTHS[int(m[5:]) - 1] for m in pre) + ' ' + pre[-1][:4],
        'losses': losses, 'n_losses': len(losses),
        'margin_thousands': margin, 'margin_words': f'plus or minus {int(margin * 1000):,}',
        'margin_level': '90 percent',
        'past_margin': past, 'past_margin_values': [ch[months.index(m)] for m in past],
        'losses_inside_margin': inside,
        'gains_past_margin': len(gains_past),
        'months_inside_margin': len(in_band),
        'since_2025': {'n': len(since), 'inside_margin': sum(1 for i in since if abs(ch[i]) <= margin),
                       'gains_past_margin': [months[i] for i in since if ch[i] > margin],
                       'losses_past_margin': [months[i] for i in since if ch[i] < -margin]},
        'latest': {'month': months[-1], 'change': ch[-1], 'avg3': av[-1], 'avg3_rounded': round(av[-1]),
                   'status': rows[-1]['status']},
        'largest': {'month': months[ch.index(max(ch))], 'change': max(ch)},
        'largest_loss': {'month': months[ch.index(min(ch))], 'change': min(ch)},
        'avg3_low': {'month': months[av.index(min(av))], 'avg3': min(av)},
        'source_line': wm,
        'retrieved': side['date_retrieved'],
    }


# ---------------------------------------------------------------------------------------------------------------------
# The atlas
# ---------------------------------------------------------------------------------------------------------------------
V7 = read_json(ATLAS)
SNAP = '2026-10-15'
need(V7['meta']['snapshot'] == SNAP, 'the atlas snapshot moved; reread every value before printing')
LINK, NODE, LOOP, REFORM = V7['links'], V7['nodes'], V7['loops'], V7['reforms']


def step_facts(lid):
    l_ = LINK[lid]
    return {'id': lid, 'from': l_['from'], 'to': l_['to'], 'sign': l_['polarity'], 'type': l_['type'],
            'grade': l_['evidence'], 'delay': l_['delay'], 'name': l_['name'], 'sign_meaning': l_['sign_meaning']}


def example_2():
    """Loops B4 and R10 through Variable C3, the one variable they share."""
    b4, r10 = LOOP['B4'], LOOP['R10']
    need([c for c, _ in b4['chain']] == ['D5', 'C3', 'C5'] and b4['links'] == ['L23', 'L24', 'L54'] and b4['type'] == 'B',
         'Loop B4 changed')
    need([c for c, _ in r10['chain']] == ['C1', 'C2', 'C3', 'C4'] and r10['links'] == ['L08', 'L25', 'L53', 'L42']
         and r10['type'] == 'R', 'Loop R10 changed')
    shared = sorted(set(c for c, _ in b4['chain']) & set(c for c, _ in r10['chain']))
    need(shared == ['C3'], f'Loops B4 and R10 share {shared}; the example follows Variable C3 alone')
    loops = {}
    for k, lp in (('B4', b4), ('R10', r10)):
        codes = [c for c, _ in lp['chain']]
        steps = [step_facts(x) for x in lp['links']]
        for i, s in enumerate(steps):
            need((s['from'], s['to']) == (codes[i], codes[(i + 1) % len(codes)]), f'Loop {k}\'s step {i + 1} changed')
        minus = sum(1 for s in steps if s['sign'] == '-')
        need(('R' if minus % 2 == 0 else 'B') == lp['type'], f'Loop {k}\'s kind disagrees with its signs')
        loops[k] = {'title': lp['title'], 'type': lp['type'], 'codes': codes,
                    'titles': {c: NODE[c]['title'] for c in codes}, 'steps': steps, 'minus': minus,
                    'into_C3': next(s['id'] for s in steps if s['to'] == 'C3'),
                    'out_of_C3': next(s['id'] for s in steps if s['from'] == 'C3'),
                    'qualification': lp['qualification'], 'evidence': lp['evidence'],
                    'evidence_summary': lp['evidence_summary'], 'delay': lp['delay']}
    need([s['grade'] for s in loops['B4']['steps']] == ['well-supported'] * 3, 'Loop B4\'s grades changed')
    need([s['grade'] for s in loops['R10']['steps']] == ['documented', 'well-supported', 'plausible', 'documented'],
         'Loop R10\'s grades changed')
    need(b4['evidence_summary'].endswith('For U.S. services the weakest is L54, since its main study covers Brazilian mayors.'),
         'Loop B4\'s weakest step changed')
    need(r10['evidence'].endswith('plausible for C3 to C4 (the weakest link)'), 'Loop R10\'s weakest step changed')
    need(NODE['C3']['title'] == 'Risk of losing office', 'Variable C3\'s title changed')
    return {'shared': 'C3', 'shared_title': NODE['C3']['title'], 'loops': loops,
            'weakest': {'B4': 'L54', 'R10': 'L53'}}


def example_3():
    """Reforms R-06, R-30 and R-38 on Loop R8, compared by target, band, effects, grades and routes, never added."""
    rids = ['R-06', 'R-30', 'R-38']
    r8 = LOOP['R8']
    need([c for c, _ in r8['chain']] == ['A5', 'A6'] and r8['links'] == ['L38', 'L39'] and r8['type'] == 'R', 'Loop R8 changed')
    out = {}
    want = {'R-06': (['B5', 'L39'], 'rules', {'DQ': '+L local', 'GE': '+S', 'EP': '0', 'EQ': '+S'}),
            'R-30': (['L39', 'A5', 'LE17'], 'rules', {'DQ': '+S delayed', 'GE': '0', 'EP': '+M', 'EQ': '+M renter-owner'}),
            'R-38': (['LT12', 'TC7'], 'rules', {'DQ': '0', 'GE': '0', 'EP': '+S sector', 'EQ': '+S renters'})}
    drawn = set()
    for rid in rids:
        r = REFORM[rid]
        t, band, eff = want[rid]
        need(r['targets'] == t and r['band'] == band and r['effects'] == eff and 'R8' in r['loops'] and not r.get('rejected'),
             f'reform {rid}\'s targets, band, effects or loops changed')
        routes = [{'route': x['route'], 'who': x['who'], 'feasibility': x['feasibility'], 'note': x['note'],
                   'checked': x['checked']} for x in r['routes']]
        out[rid] = {'title': r['title'], 'targets': r['targets'], 'loops': r['loops'], 'band': r['band'],
                    'effects': r['effects'], 'effects_confidence': r['effects_confidence'],
                    'problem': r['problem_evidence']['grade'], 'remedy': r['remedy_evidence']['grade'],
                    'routes': routes, 'status_checked': r['status']['checked'], 'tradeoffs': r['tradeoffs']}
        drawn |= set(r['targets'])
    # the qualifiers Gate 2 named, each kept whole after its code
    quals = sorted(v for rid in rids for v in REFORM[rid]['effects'].values() if ' ' in v)
    need(quals == ['+L local', '+M renter-owner', '+S delayed', '+S renters', '+S sector'], f'the qualifiers moved: {quals}')
    dated = [(rid, x['route']) for rid in rids for x in REFORM[rid]['routes'] if x['checked']]
    need(dated == [('R-38', 'SS')], f'the dated routes moved: {dated}')
    need(all(x['checked'] in (None, SNAP) for rid in rids for x in REFORM[rid]['routes']), 'a route carries another date')
    # what the drawing must hold so every offered reform's every target sits on it (Rule 15.20)
    need(drawn == {'B5', 'L39', 'A5', 'LE17', 'LT12', 'TC7'}, f'the targets moved: {sorted(drawn)}')
    off = {x: step_facts(x) for x in ('LE17', 'LT12')}
    need((off['LE17']['from'], off['LE17']['to']) == ('A5', 'EC9') and (off['LT12']['from'], off['LT12']['to']) == ('TC7', 'EC9'),
         'connections LE17 or LT12 changed')
    return {'loop': {'id': 'R8', 'title': r8['title'], 'codes': ['A5', 'A6'], 'steps': [step_facts(x) for x in r8['links']],
                     'reforms_listed': r8['reforms'], 'evidence': r8['evidence']},
            'reforms': out, 'order': rids, 'qualifiers': quals, 'dated_routes': dated,
            'targets_all': sorted(drawn), 'off_loop': off,
            'variables_drawn': {c: NODE[c]['title'] for c in ('A5', 'A6', 'EC9', 'TC7', 'B5')},
            'effect_codes': V7['outcomes']['effect_codes']}


def facts():
    return {'snapshot': SNAP, 'example_1': example_1(), 'example_2': example_2(), 'example_3': example_3()}


# ---------------------------------------------------------------------------------------------------------------------
# --figures: the words of the three examples' files against facts()
# ---------------------------------------------------------------------------------------------------------------------
def plan_rows():
    plan = read_json(PLAN)
    rows = [r for r in plan.get('chapter_rules', []) + plan.get('forms', []) + plan.get('complex', [])
            if str(r.get('rule')) in ('14.142', '14.143', '14.144')]
    for k, v in plan.items():
        if isinstance(v, list) and k not in ('chapter_rules', 'forms', 'complex', 'groups'):
            rows += [r for r in v if isinstance(r, dict) and str(r.get('rule')) in ('14.142', '14.143', '14.144')]
    return rows


def reader_text(s):
    """Every reader word in a string of markup or plain text, entities read, tags and comments out."""
    s = re.sub(r'<!--.*?-->|<style\b.*?</style>|<script\b.*?</script>', ' ', str(s), flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace(' ', ' ')


def figures(f):
    e1, e2, e3 = f['example_1'], f['example_2'], f['example_3']
    rows = plan_rows()
    if not rows:
        print('  note: the plan file holds no row for Rules 14.142 to 14.144 yet; the word checks wait for it')
        return
    for r in rows:
        rid = str(r['rule'])
        ef = os.path.join(GUIDE, r['entry_file']) if r.get('entry_file') else None
        texts = []
        if ef and os.path.exists(ef):
            texts.append(json.dumps(read_json(ef), ensure_ascii=False))
        sid = r.get('spec_id')
        if sid and os.path.exists(os.path.join(SPECS, sid.lower() + '.json')):
            texts.append(json.dumps(read_json(os.path.join(SPECS, sid.lower() + '.json')), ensure_ascii=False))
        for plate in [x for x in (r.get('correct'), r.get('failure')) if x]:
            p = os.path.join(SPECIMENS, plate + '.html')
            if os.path.exists(p):
                with open(p, encoding='utf-8') as fh:
                    texts.append(fh.read())
        if not texts:
            print(f'  note: Rule {rid}: no file written yet')
            continue
        t = reader_text(' '.join(texts)).replace('\\u2019', '’')
        where = f'Rule {rid}'
        # no em dash, no U+2011, anywhere in the examples' words
        check(where, '—' not in t and '‑' not in t, 'an em dash or U+2011 in the words')
        if rid == '14.142':
            check(where, e1['window_words'] in t, f'the window "{e1["window_words"]}" is not stated')
            check(where, 'preliminary' in t.lower(), 'the preliminary months are not named')
            check(where, '122,000' in t, 'the margin, plus or minus 122,000, is not printed')
            for m in e1['past_margin']:
                check(where, month_words(m) in t or (MONTHS[int(m[5:]) - 1] + ' ' + m[:4]) in t,
                      f'the drop past the margin in {month_words(m)} is not named')
            # every count of months or drops the words print is one the data holds
            counts = {'seven': e1['n_losses'], 'two': len(e1['past_margin']), 'five': len(e1['losses_inside_margin'])}
            for w_, n_ in counts.items():
                check(where, n_ == {'seven': 7, 'two': 2, 'five': 5}[w_], f'the count "{w_}" no longer matches the data ({n_})')
            check(where, f'{e1["n"]} months' in t, f'the window\'s {e1["n"]} months are not counted')
            for m, v in zip(e1['past_margin'], e1['past_margin_values']):
                check(where, f'\u2212{abs(int(v * 1000)):,}' in t or f'minus {abs(int(v * 1000)):,}' in t,
                      f'the value of the {month_words(m)} drop, {v:+.0f} thousand, is not printed')
            check(where, '51,000' in t or '+51,000' in t, 'the latest average, 51,000, is not printed')
        if rid == '14.143':
            for k in ('B4', 'R10'):
                check(where, e2['loops'][k]['title'] in t, f'Loop {k}\'s title is not printed')
                for c, title in e2['loops'][k]['titles'].items():
                    check(where, title.replace("'", '\u2019').lower() in t.lower(), f'Variable {c}\'s title, "{title}", is not printed')
            check(where, 'October 15, 2026' in t, 'the snapshot date is not printed')
        if rid == '14.144':
            for rid_, r_ in e3['reforms'].items():
                check(where, r_['title'] in t or r_['title'].replace("'", '’') in t, f'Reform {rid_}\'s title is not printed')
                for v in r_['effects'].values():
                    if ' ' in v:
                        check(where, v.replace('-', '−', 1) in t or v in t, f'the qualifier "{v}" is not kept whole')
            check(where, 'October 15, 2026' in t, 'the snapshot date is not printed beside the routes')
            check(where, not re.search(r'(?i)\b(total|combined|sum|overall score|net effect)\b', t)
                  or 'never add' in t.lower() or 'no total' in t.lower(),
                  'a word that totals effects appears without the rule against it')


def main():
    f = facts()
    if '--json' in sys.argv:
        print(json.dumps(f, indent=1, ensure_ascii=False))
    if '--figures' in sys.argv:
        figures(f)
    e1 = f['example_1']
    print(f'maker_c_round5_derive: example 1: {e1["n"]} months, {e1["window_words"]}; preliminary {e1["preliminary_words"]}; '
          f'{e1["n_losses"]} losses, {len(e1["past_margin"])} past the margin of {e1["margin_words"]} '
          f'({", ".join(month_words(m) for m in e1["past_margin"])}); latest {e1["latest"]["change"]:+.0f} thousand, '
          f'average {e1["latest"]["avg3"]:.2f} thousand')
    e2 = f['example_2']
    print(f'maker_c_round5_derive: example 2: Loops B4 and R10 share Variable {e2["shared"]}, "{e2["shared_title"]}"; '
          f'into it {e2["loops"]["B4"]["into_C3"]} and {e2["loops"]["R10"]["into_C3"]}, out of it '
          f'{e2["loops"]["B4"]["out_of_C3"]} and {e2["loops"]["R10"]["out_of_C3"]}')
    e3 = f['example_3']
    print(f'maker_c_round5_derive: example 3: {", ".join(e3["order"])} on Loop R8; targets {", ".join(e3["targets_all"])}; '
          f'qualifiers {", ".join(e3["qualifiers"])}; dated routes {e3["dated_routes"]}')
    print(f'maker_c_round5_derive: {COUNT[0]} word checks, {len(FAULTS)} fault(s)')
    for x in FAULTS:
        print('  FAIL ' + x)
    return 1 if FAULTS else 0


if __name__ == '__main__':
    sys.exit(main())
