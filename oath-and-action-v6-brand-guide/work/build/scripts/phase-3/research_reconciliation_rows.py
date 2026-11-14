"""Rule 15.25's reconciliation rows, for the systems designer (round 5, R5-6, the data lead's ruling (e) and request R-2).

Writes work/build/data/v7-reconciliation-rows.json and its sidecar v7-reconciliation-rows.meta.json:
  - Phase 0's 45 rows of conflicts and ambiguities, parsed from its table
    (work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md), each with the model's value read today by this script
    from work/extract/atlas-v7-data.json (never copied from Phase 0's table), the resolution the guide applies and the
    chapter and rules where it applies it;
  - the two value conflicts (row 42, the Ledger's reform counts for D03 and D04), checked against Phase 0's data file;
  - new rows from 46 for what Phase 2 and Phase 3 drew from V7 where the model holds an ambiguity the guide resolves,
    each tied to its item on the V7.1 issue list;
  - the November 13 rerun's counts, read from work/research/20261113_Atlas-Recheck-Full-Data.json.
Rows are in the print order ruling (e) sets: value, then sign, grade and delay, identifiers, structure, encoding, labels,
then the new rows in chapter order. Phase 0's numbers stay as row IDs.

Usage:
    python3 -I work/build/scripts/phase-3/research_reconciliation_rows.py           # write both files
    python3 -I work/build/scripts/phase-3/research_reconciliation_rows.py --check   # rebuild in memory, compare, write nothing
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MODEL = ROOT / 'work/extract/atlas-v7-data.json'
P0_TABLE = ROOT / 'work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md'
P0_DATA = ROOT / 'work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json'
RERUN = ROOT / 'work/research/20261113_Atlas-Recheck-Full-Data.json'
OUT = ROOT / 'work/build/data'
NAME = 'v7-reconciliation-rows'
MODEL_SHA = 'ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2'
SNAP = '2026-10-15'
ATLAS_PUB = 'Oath & Action’s systems atlas, Who Do They Answer To?'
READ_ON = '2026-11-14'

raw = MODEL.read_bytes()
assert hashlib.sha256(raw).hexdigest() == MODEL_SHA, 'the model is not the committed snapshot'
D = json.loads(raw)
assert D['meta']['snapshot'] == SNAP
N, L, LP, R = D['nodes'], D['links'], D['loops'], D['reforms']
DOM = {x['id']: x for x in D['domains']}
GL = {x['term']: x['definition'] for x in D['glossary']}
METH = D['methods']


def sentence(text, needle):
    """The one sentence of text that holds needle, as stored."""
    for s in re.split(r'(?<!U\.S\.)(?<=[.!?])\s+', text):
        if needle in s:
            return s
    raise AssertionError(f'{needle!r} not found')


def counts(values):
    c = collections.Counter(values)
    return ', '.join(f'{k} {v}' for k, v in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0]))))


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')
    elif isinstance(o, str):
        yield path, o


def find_text(needle):
    """The first field holding needle, and the sentence that holds it, as stored."""
    for path, s in walk(D):
        if needle in s:
            return path, sentence(s, needle)
    raise AssertionError(needle)


def title(kind, k):
    return {'node': N, 'loop': LP, 'reform': R}[kind][k]['title']


def sheet(k):
    n = N[k]
    return n['domain'].split('/')[0] if n['domain'] else n['cluster']


def reforms_touching(code, live_only=True):
    vs = {k for k in N if sheet(k) == code}
    out = set()
    for rid, r in R.items():
        if live_only and r.get('rejected'):
            continue
        if any(t in vs or (t in L and (L[t]['to'] in vs or L[t]['from'] in vs)) for t in r['targets']):
            out.add(rid)
    return out


SEVEN = {'+L', '+M', '+S', '0', '-S', '-M', '?'}


def effect_extras():
    vals = [(rid, fam, v) for rid, r in R.items() for fam, v in r['effects'].items()]
    extra = [(rid, fam, v) for rid, fam, v in vals if v not in SEVEN]
    return vals, extra


def loop_reform_pairs():
    pairs = []
    for rid, r in R.items():
        for lp in r.get('loops') or []:
            if rid not in (LP.get(lp, {}).get('reforms') or []):
                pairs.append((lp, rid))
    back = [(lp, rid) for lp, x in LP.items() for rid in (x.get('reforms') or []) if lp not in (R[rid].get('loops') or [])]
    return sorted(pairs), back


# ------------------------------------------------------------------ the model's value today, row by row (read here)
def mv(row):
    if row == 1:
        assert 'L##' not in L
        return f"No connection L## exists. Connection L01 has delay {L['L01']['delay']}; Connection L24 has delay {L['L24']['delay']}"
    if row == 2:
        rl = sorted(k for k in LP if k.startswith('R'))
        return f"{len(rl)} loops with R codes: {', '.join(rl)}. Loop R5: \"{title('loop', 'R5')}\""
    if row == 3:
        return f"Loop R1: \"{title('loop', 'R1')}\"; Reform R-01: \"{title('reform', 'R-01')}\""
    if row == 4:
        return (f"Variable B4: \"{title('node', 'B4')}\"; Loop B4: \"{title('loop', 'B4')}\"; Loop B2 closure "
                f"\"{LP['B2']['closure']}\"; Loop B3 closure \"{LP['B3']['closure']}\"")
    if row == 5:
        both = [k for k in ('B2', 'B3', 'B4', 'B5') if k in N and k in LP]
        dv = sorted(k for k in N if re.fullmatch(r'D\d', k))
        return f"Codes that are both a variable and a loop: {', '.join(both)}. Variables {dv[0]} to {dv[-1]} ({len(dv)}); domains {min(DOM)} to {max(DOM)} ({len(DOM)})"
    if row == 6:
        return '; '.join(f"Variable {k}: \"{title('node', k)}\"; Loop {k}: \"{title('loop', k)}\"" for k in ('B4', 'B5'))
    if row == 7:
        return f"Variable D1: \"{title('node', 'D1')}\"; Domain D04: \"{DOM['D04']['title']}\""
    if row == 8:
        rf = sorted(R)
        return '; '.join(f"Loop {k}: \"{title('loop', k)}\"" for k in ('R4a', 'R8', 'R10')) + f"; reforms {rf[0]} to {rf[-1]} ({len(rf)})"
    if row == 9:
        return f"Variable B1: \"{title('node', 'B1')}\"; Loop B1a: \"{title('loop', 'B1a')}\""
    if row == 10:
        return f"Glossary, Delay: \"{GL['Delay']}\" Glossary, Effect code: \"{GL['Effect code']}\""
    if row in (11, 17):
        s = sentence(METH['how_claims_are_assessed'], 'dotted line')
        ev = counts(x['evidence'] for x in L.values())
        return f"Methods: \"{s}\" Connection grades: {ev}. The dash patterns live in V7's renderer, not in the model file; Phase 0 read them there"
    if row == 12:
        return f"Connection T01: grade {L['T01']['evidence']}, \"{L['T01']['name']}\"; Loop R16 closure \"{LP['R16']['closure']}\""
    if row == 13:
        return '; '.join(f"Connection {k}: {L[k]['evidence']}" for k in ('L01', 'L02', 'L03'))
    if row == 14:
        return f"Connection LE26: {L['LE26']['evidence']}, \"{L['LE26']['name']}\""
    if row == 15:
        return f"Model conventions: \"{sentence(METH['model_conventions'], 'association records')}\" Glossary, Association: \"{GL['Association']}\""
    if row == 16:
        cross = [k for k, x in L.items() if x['from'] in N and x['to'] in N and N[x['from']]['layer'] != N[x['to']]['layer']]
        return f"{len(cross)} connections join variables in two layers; grades: {counts(L[k]['evidence'] for k in cross)}"
    if row == 18:
        txt = METH['how_claims_are_assessed']
        words = ['Documented means', 'Well supported means', 'Plausible means', 'Mixed means', 'Contested means', 'Hypothesis marks']
        order = sorted(words, key=txt.index)
        return (f"Glossary, Confidence label: \"{GL['Confidence label']}\" The methods define the grades in this order: "
                + ', '.join(w.split()[0] if not w.startswith('Well') else 'Well supported' for w in order))
    if row == 19:
        return f"Signs on 118 connections: {counts(str(x['polarity']) for x in L.values())}. Model conventions: \"{find_text('does not mean a benefit')[1]}\""
    if row == 20:
        au = sorted(k for k, x in L.items() if x['type'] == 'authority')
        assert all(L[k]['polarity'] is None and not L[k]['loops'] for k in au)
        return f"{len(au)} authority connections ({', '.join(au)}), every one with no sign and in no loop"
    if row == 21:
        return f"Connection types: {counts(x['type'] for x in L.values())}"
    if row == 22:
        ow = sorted(k for k, x in L.items() if x['type'] == 'ownership')
        return 'Ownership connections, each signed: ' + ', '.join(f"{k} {L[k]['polarity'].replace('-', '−')}" for k in ow)
    if row == 23:
        assert all(all(f in x for f in ('type', 'polarity', 'evidence', 'delay')) for x in L.values())
        return 'Every connection stores type, polarity, evidence and delay as four separate fields'
    if row == 24:
        deg = collections.Counter()
        for x in L.values():
            deg[x['from']] += 1
            deg[x['to']] += 1
        vals = [deg[k] for k in N]
        return f"Connections per variable range from {min(vals)} to {max(vals)}; the model stores no size for a variable"
    if row == 25:
        return f"Variables by layer: {counts(x['layer'] for x in N.values())}"
    if row == 26:
        path, s = find_text('codes for different families are never added together')
        return f"Glossary, Effect code: \"{GL['Effect code']}\" At {path.lstrip('.')}: \"{s}\""
    if row == 27:
        live = {k: r for k, r in R.items() if not r.get('rejected')}
        dq = sorted(k for k, r in live.items() if '+' in r['effects']['DQ'] and '-' in r['effects']['DQ'])
        ep = sorted(k for k, r in live.items() if '-' in r['effects']['EP'] and '+' not in r['effects']['EP'])
        return (f"DQ values with a gain and a possible cost: {', '.join(f'{k} ' + live[k]['effects']['DQ'] for k in dq)}. "
                f"EP values with a possible cost and no gain: {', '.join(f'{k} ' + live[k]['effects']['EP'] for k in ep)}")
    if row == 28:
        return f"Feasibility levels: {', '.join(D['routes']['feasibility_scale'])}"
    if row == 29:
        vals, extra = effect_extras()
        live_rf = sorted({rid for rid, _, _ in extra if not R[rid].get('rejected')})
        ex = '; '.join(f"{rid} {fam} \"{R[rid]['effects'][fam]}\"" for rid, fam in (('R-25', 'DQ'), ('R-24', 'EP'), ('R-12', 'DQ'), ('R-29', 'EQ')))
        return f"{len(extra)} of {len(vals)} effect values carry a qualifier or a range, in {len(live_rf)} live reforms; for example {ex}"
    if row == 30:
        return f"Connection grades: {counts(x['evidence'] for x in L.values())}. Glossary, Confidence label: \"{GL['Confidence label']}\""
    if row == 31:
        lab = {}
        for x in LP.values():
            for v, t in zip(x.get('chain') or [], x.get('chain_labels') or []):
                if isinstance(v, list) and v[0] in N:
                    lab.setdefault(v[0], t[0])
        return '; '.join(f"Variable {k}: title \"{title('node', k)}\", loop chain label \"{lab.get(k)}\"" for k in ('A1', 'B4', 'C3'))
    if row == 32:
        return f"Variable C2: \"{title('node', 'C2')}\""
    if row == 33:
        return f"Variable D4: \"{title('node', 'D4')}\"; Variable TC5: \"{title('node', 'TC5')}\""
    if row == 34:
        return f"Variable C5: \"{title('node', 'C5')}\""
    if row == 35:
        return '; '.join(f"Loop {k}: \"{title('loop', k)}\"" for k in ('R3', 'R1b', 'R2', 'R6'))
    if row == 36:
        return f"Loop closure: {counts(x['closure'] for x in LP.values())}"
    if row == 37:
        reg = {r['id']: r['title'] for r in D['layers']['core']['regions']}
        parts = [f"Connection {k}: {L[k]['from']} (area {N[L[k]['from']]['cluster']}) to {L[k]['to']} (area {N[L[k]['to']]['cluster']})" for k in ('L03', 'L31', 'L37')]
        return '; '.join(parts) + f". Area A: \"{reg['A']}\""
    if row == 38:
        return f"Reform R-01's summary: \"{sentence(R['R-01']['summary'], 'takes no position')}\""
    if row == 39:
        return f"Reform bands: {counts(r['band'] for r in R.values())}"
    if row == 40:
        steps = '; '.join(f"Connection {k} {L[k]['evidence']}" for k in LP['B4']['links'])
        return (f"Loop B4 steps: {steps}. Loop B4's evidence summary: \"{sentence(LP['B4']['evidence_summary'], 'weakest')}\" "
                f"Connection L54's qualification: \"{L['L54']['qualification']}\"")
    if row == 41:
        fs = [x for x in R['R-28']['routes'] if x['route'] == 'FS'][0]
        return f"Reform R-28, route FS: who \"{fs['who']}\", feasibility {fs['feasibility']}, checked {fs['checked'] or 'none (Not checked)'}"
    if row == 42:
        out = []
        for code in ('D03', 'D04'):
            live, alls = reforms_touching(code), reforms_touching(code, False)
            out.append(f"{code}: {len(live)} live reforms, {len(alls)} with the rejected R-35")
        r35 = R['R-35']
        return '; '.join(out) + f". Reform R-35 \"{r35['title']}\" is rejected ({r35['rejected']}) and targets {', '.join(r35['targets'])}"
    if row == 43:
        out = []
        for code in ('D02', 'D01'):
            vs = {k for k in N if sheet(k) == code}
            touch = sum(1 for x in L.values() if x['from'] in vs or x['to'] in vs)
            filed = sum(1 for x in L.values() if x['to'] in vs)
            out.append(f"{code}: {touch} connections touch its variables, {filed} end at them")
        return '; '.join(out)
    if row == 44:
        iss = D['issues']
        ret = sum(1 for x in iss.values() if x.get('retired') or x.get('grade') == 'retired')
        return f"{len(iss)} issue records, {ret} retired, {len(iss) - ret} active; meta.counts.issues {D['meta']['counts'].get('issues')}"
    if row == 45:
        im = sum(1 for x in N.values() if x.get('increase_means'))
        return f"Variable types: {counts(x['type'] for x in N.values())}; {im} of {len(N)} variables carry increase_means"
    # new rows
    if row == 46:
        claims = D['claims'].values() if isinstance(D['claims'], dict) else D['claims']
        flag = sorted(k for k, x in L.items() if x.get('contested'))
        pc = sorted(k for k, x in L.items() if x['evidence'] == 'plausible_contested')
        assert flag == pc
        return (f"Connections: {counts(x['evidence'] for x in L.values())}. Issues: {counts(x['grade'] for x in D['issues'].values())}. "
                f"Claims: {counts(x['confidence'] for x in claims)}. The contested flag sits on exactly the {len(flag)} plausible_contested connections")
    if row == 47:
        ev = collections.Counter(x['evidence'] for x in L.values())
        return f"Documented connections {ev['documented']}, well-supported {ev['well-supported']}. V7's renderer draws both solid (V7.1 item 24; the renderer is not in this container)"
    if row == 48:
        cl = [k for k, x in LP.items() if x['closure'].startswith('conceptual')]
        return f"Conceptual loops: {', '.join(sorted(cl))}. V7's renderer dashes their steps 5 4, near plausible's 9 4 (V7.1 item 25; the renderer is not in this container)"
    if row == 49:
        ent = [x for r in R.values() for x in r['routes']]
        dated = [x for x in ent if x['checked']]
        return f"{len(ent)} route entries, {len(dated)} with a check date (all {', '.join(sorted({x['checked'] for x in dated}))}), {len(ent) - len(dated)} with none"
    if row == 50:
        return f"Variable D6 type \"{N['D6']['type']}\"; kind_plain: \"{sentence(N['D6']['kind_plain'], 'Stock')}\""
    if row == 51:
        x = L['L23']
        return f"Connection L23 \"{x['name']}\", from {x['from']} to {x['to']}, sign {x['polarity'].replace('-', '−')}; sign_meaning: \"{x['sign_meaning']}\""
    if row == 52:
        au = [k for k, x in L.items() if x['type'] == 'authority']
        return f"{len(au)} authority connections, none signed. V7's renderer ends them in a filled arrowhead (V7.1 item 26; the renderer is not in this container)"
    if row == 53:
        cl = sorted(k for k, x in LP.items() if x['closure'].startswith('conceptual'))
        def step(s):
            return f"{s[0]} {s[1].replace('-', '−')}" if isinstance(s, list) else str(s)
        return '; '.join(f"Loop {k} grade \"{LP[k]['evidence']}\", chain: {', '.join(step(s) for s in LP[k]['chain'])}" for k in cl)
    if row == 54:
        pairs, back = loop_reform_pairs()
        r8 = LP['R8'].get('reforms') or []
        naming = sorted(rid for rid, r in R.items() if 'R8' in (r.get('loops') or []))
        return (f"{len(pairs)} reform-to-loop pairs not listed back ({len({p[1] for p in pairs})} reforms, {len({p[0] for p in pairs})} loops); "
                f"{len(back)} the other way. Loop R8 lists {', '.join(r8) or 'no reform'}; reforms naming R8: {', '.join(naming)}")
    if row == 55:
        q = LP['R4a']['qualification']
        b = [x for x in R['R-08']['routes'] if x['route'] == 'BI'][0]
        return (f"Reform R-01's status (checked {R['R-01']['status']['checked']}): \"{sentence(R['R-01']['status']['text'], 'November 3, 2026 ballot')}\" "
                f"Loop R4a's qualification: \"{sentence(q, 'Missouri')}\" Reform R-08, route BI note: \"{sentence(b['note'], 'November 3, 2026')}\"")
    if row == 56:
        ent = [x for r in R.values() for x in r['routes']]
        vals = collections.Counter(x['who'] for x in ent)
        verbs = sorted(f"{rid} {x['route']} \"{x['who']}\"" for rid, r in R.items() for x in r['routes']
                       if x['who'].split()[0] in ('Repeal', 'Restructure', 'Codify', 'Rescind', 'Legalize'))
        return f"{len(ent)} route entries hold {len(vals)} distinct who values; five open with a verb: {'; '.join(verbs)}"
    if row == 57:
        av = [x for x in D['routes']['items'] if x['code'] == 'AV'][0]
        return f"Route AV, who: \"{av['who']}\"; sources: {len(av.get('sources') or [])}"
    raise KeyError(row)


# ------------------------------------------------------------------ where the guide applies each resolution
# group, resolution as the guide applies it today, chapter, rules, status. Read from the rule texts in
# work/build/guide/chapters/*.json on November 14, 2026; "not printed" means no chapter or specimen file in
# work/build/guide/ holds the item, by search the same day.
APPLY = {
    1: ('identifier', 'Real IDs in typed chips; no placeholder ID prints', '13 Evidence and sourcing', '13.9; 18.24', 'applied'),
    2: ('identifier', 'The guide numbers its rules by chapter, such as Rule 13.9, so no rule takes an R code; every atlas ID sits in a typed chip', '13 Evidence and sourcing', '13.9; 18.24', 'applied'),
    3: ('identifier', 'Loop R1 and Reform R-01 always print with their type words', '13 Evidence and sourcing', '13.9; 18.24', 'applied'),
    4: ('identifier', 'A loop takes its typed chip beside the drawing, apart from the variables on its ring', '15 Systems graphics', '13.9; 15.6', 'applied'),
    5: ('identifier', 'Typed chips in every column: Variable, Loop, Domain', '13 Evidence and sourcing', '13.9; 10.8', 'applied'),
    6: ('identifier', 'Typed chips for Variables B4 and B5 and Loops B4 and B5 wherever both appear', '13 Evidence and sourcing', '13.9', 'applied'),
    7: ('identifier', 'A domain prints in words with its chip, such as Domain D04; a variable as Variable D1', '10 Symbols', '10.8; 13.9', 'applied'),
    8: ('identifier', 'Loop and Reform chips on every page that shows both', '13 Evidence and sourcing', '13.9; 18.24', 'applied'),
    9: ('identifier', 'Variable B1 and Loop B1a in typed chips; B1a never shortened', '13 Evidence and sourcing', '13.9', 'applied'),
    10: ('delay', 'Delay draws as one to three ticks with its words in the key; effect size prints as the atlas code with pips, never a bare letter beside a delay', '13 Evidence and sourcing', '13.5; 10.10', 'applied'),
    11: ('encoding', 'The atlas line code: solid for documented and well supported, dashed for plausible, dash and dot for contested, dots for a hypothesis, each with its grade word', '13 Evidence and sourcing', '13.4; 10.10', 'applied'),
    12: ('encoding', 'A hypothesized step draws in dots, with its grade word', '15 Systems graphics', '13.4; 15.7', 'applied'),
    13: ('encoding', 'Each step of Loop R1 in its own line, Connection L02 dashed, and the weakest step named in words', '15 Systems graphics', '13.4; 15.13; 15.19', 'applied'),
    14: ('encoding', 'Every connection takes its own grade line; LE26 dashed wherever drawn', '13 Evidence and sourcing', '13.4', 'applied'),
    15: ('encoding', 'No association line: dots mean a hypothesis only, and associations stay off the drawing', '13 Evidence and sourcing', '13.4; 15.4', 'applied'),
    16: ('encoding', 'Layers framed by a 1 px rule and named; every connection across them keeps its own grade line', '15 Systems graphics', '15.9; 13.4', 'applied'),
    17: ('encoding', 'Dashed means plausible, as the atlas draws it', '13 Evidence and sourcing', '13.4; 10.10', 'applied'),
    18: ('encoding', 'One table of display words in the atlas order, Documented, Well supported, Plausible, Contested, Hypothesis, each with a gloss; the grade draws as a line pattern, never a darkness', '13 Evidence and sourcing', '13.3; 13.4; 13.5', 'applied'),
    19: ('sign', 'Every causal connection carries its sign tag and the word raises or lowers, with the atlas sentence that a plus is not a benefit', '15 Systems graphics', '15.3; 10.10', 'applied'),
    20: ('encoding', 'Authority draws solid, ends in an open diamond, prints decides and carries no sign; it stays out of every loop', '15 Systems graphics', '15.5; 15.17; 10.10', 'applied'),
    21: ('encoding', 'The connection type prints in words, such as money, lowers; no pattern, width or color of its own', '15 Systems graphics', '15.4', 'applied'),
    22: ('structure', 'Ownership draws as a signed connection with its type in words; frames only group a layout', '15 Systems graphics', '15.4; 15.9', 'applied'),
    23: ('structure', 'The grammar is built on the atlas fields: type, sign, grade and delay, each with its own mark', '15 Systems graphics', '15.1 to 15.5; 13.4; 13.5', 'applied'),
    24: ('encoding', 'One pill size and one line width; size or width measures only with a defined measure and a key', '15 Systems graphics', '15.1', 'applied'),
    25: ('encoding', 'Layers are coded by a frame and a name, never by color; Verdigris’s jobs are set in chapters 05 and 14', '15 Systems graphics', '15.9; 05.4; 05.7; 14.5', 'applied'),
    26: ('encoding', 'Effect size as the atlas code with one to three pips and its words, one row per family, never a width and never a total', '15 Systems graphics', '13.5; 15.16; 15.20', 'applied'),
    27: ('structure', 'Every outcome family keeps its own row with the atlas code, so a possible cost prints beside a gain', '15 Systems graphics', '13.5; 15.16; 15.20', 'applied'),
    28: ('encoding', 'Each route prints its feasibility in the atlas word, one of four, with who acts and its check date', '15 Systems graphics', '15.16; 15.24', 'applied'),
    29: ('label', 'An effect prints its full atlas text, qualifier or range kept whole, beside its pips', '13 Evidence and sourcing', '13.5; 15.16; 15.20', 'applied'),
    30: ('label', 'One display word per grade from one table, Contested for both plausible_contested and contested', '13 Evidence and sourcing', '13.3', 'applied'),
    31: ('label', 'One name per variable, its own title, in every drawing, loop drawings included (DR-265, DR-267)', '15 Systems graphics', '15.2', 'applied'),
    32: ('label', 'Variable C2 prints its own title everywhere', '15 Systems graphics', '15.2', 'applied'),
    33: ('label', 'Variables D4 and TC5 print their own titles, which name the capacity', '15 Systems graphics', '15.2', 'applied'),
    34: ('label', 'Variable C5 prints its own title, retirement included', '15 Systems graphics', '15.2', 'applied'),
    35: ('label', 'A loop prints its own title beside its chip', '15 Systems graphics', '15.6', 'applied'),
    36: ('label', 'Closure prints in the atlas words beside the loop grade: 18 closed, 2 through a hypothesis, 3 conceptual', '15 Systems graphics', '15.7', 'applied'),
    37: ('label', 'If drawn, the return connections end in area A, named by its title, Economic structure; no chapter draws the Circuit', '15 Systems graphics', '15.9', 'not printed'),
    38: ('label', 'No plate quotes R-01’s position sentence; none prints a disclosure (DR-100). Were one to, it names both measures, as the atlas summary does, as of October 15, 2026', '15 Systems graphics', '15.16', 'not printed'),
    39: ('label', 'A reform’s band prints in the atlas word with its definition', '15 Systems graphics', '15.11', 'applied'),
    40: ('grade', 'All three steps print well supported; “weakest” appears only in the atlas’s own words, which name the limit for U.S. services (data lead, ruling (e))', '15 Systems graphics', '15.15; 14.143', 'applied'),
    41: ('label', 'A route prints its code, name, who acts and feasibility, and “Not checked” where the atlas gives no date', '15 Systems graphics', '13.10; 15.16; 15.24', 'applied'),
    42: ('value', 'The rejected option keeps the word Rejected wherever it appears; no chapter prints a reform count by domain', '10 Symbols', '10.6', 'applied where shown; no domain count printed'),
    43: ('structure', 'No chapter prints the Ledger or the Register counts; a count that the guide prints names its counting rule', '15 Systems graphics', 'none', 'not printed'),
    44: ('structure', 'No chapter prints the issue count; Retired stays a record status outside every grade key', '13 Evidence and sourcing', '13.3', 'not printed'),
    45: ('structure', 'Each variable prints its kind in words and the atlas sentence on what a higher value means at first use', '15 Systems graphics', '15.2', 'applied'),
    46: ('new', 'One display word per grade from one table, and the grade field read, never the contested flag', '13 Evidence and sourcing', '13.3', 'applied'),
    47: ('new', 'A documented connection’s label starts with the record square, so documented and well supported differ on the drawing', '13 Evidence and sourcing', '13.4; 13.11', 'applied'),
    48: ('new', 'A conceptual step draws as the hollow line between thin pills, apart from the plausible dash', '13 Evidence and sourcing', '13.4; 15.7; 15.18', 'applied'),
    49: ('new', 'A route with no date prints “Not checked”; no date is inferred from a reform’s status', '13 Evidence and sourcing', '13.10; 15.16; 15.24', 'applied'),
    50: ('new', 'Chapter 15 prints no kind for Variable D6 until V7.1 sets it (DR-264)', '15 Systems graphics', '15.2', 'applied'),
    51: ('new', 'The connection prints the atlas sentence on its sign beside its name, so the minus reads as the atlas means it', '15 Systems graphics', '15.3; 15.15; 14.143', 'applied'),
    52: ('new', 'Authority ends in the open diamond, never an arrowhead', '15 Systems graphics', '15.5; 10.10', 'applied'),
    53: ('new', 'Closure prints first and the grade text second; a conceptual loop prints “no numbered chain” after its grade, and its stations come from the chain labels', '15 Systems graphics', '15.7; 15.18', 'applied'),
    54: ('new', 'Open until V7.1 makes the lists agree: 15.20’s Loop R4a is one both lists agree on; the round 5 comparison on Loop R8 (14.144) needs words for R-06 and R-38, which name R8 while R8 lists only R-30', '15 Systems graphics', '15.11; 15.20; 14.144', 'open for 14.144 in round 5'),
    55: ('new', 'A status the November 3, 2026 vote may have changed prints under “As of October 15, 2026”, until each state certifies (DR-269)', '15 Systems graphics', '15.16; 15.20', 'applied'),
    56: ('new', 'A route prints the atlas words as stored under a label that fits actors, instruments and actions alike; proposed for V7.1 at board 3', '15 Systems graphics', '15.20; 15.24', 'proposed for board 3'),
    57: ('new', 'The Article V route prints its stages from Article V beside the atlas words as stored, with the source the studio read (V7.1 item 41)', '15 Systems graphics', '15.24', 'for 15.24 in round 5'),
}
NEW = {
    46: ('V7.1 items 1 and 2', 'Grade vocabulary across record types', 'Grade fields', 'links[].evidence; issues[].grade; claims[].confidence; links[].contested'),
    47: ('V7.1 item 24', 'Documented and well supported share one line', 'Renderer line code', 'links[].evidence'),
    48: ('V7.1 item 25', 'Conceptual steps near the plausible dash', 'Renderer conceptual steps', 'loops[].closure'),
    49: ('V7.1 item 9', 'Most route entries have no check date', 'Route check dates', 'reforms[].routes[].checked'),
    50: ('V7.1 item 8', 'Variable D6 typed flow, described as a stock', 'Variable D6', 'nodes.D6.type; nodes.D6.kind_plain'),
    51: ('V7.1 item 28', 'Connection L23’s name against its sign', 'Connection L23', 'links.L23'),
    52: ('V7.1 item 26', 'Authority connections end in an arrowhead', 'Renderer authority mark', 'links[].type; links[].polarity'),
    53: ('V7.1 items 16 and 17', 'Conceptual loops carry grades with no numbered steps', 'Loops B2, B3, R9', 'loops[].evidence; loops[].chain'),
    54: ('V7.1 item 29', 'A reform lists a loop that does not list it back', 'Loop and reform lists', 'reforms[].loops; loops[].reforms'),
    55: ('V7.1 item 39', 'Measures pending in the snapshot', 'Alaska, Massachusetts and Missouri measures', 'reforms.R-01.status; loops.R4a.qualification; reforms.R-08.routes'),
    56: ('Round 4 research notes, proposed for board 3', 'Route who mixes actors, instruments and actions', 'Route who field', 'reforms[].routes[].who'),
    57: ('V7.1 item 41', 'The Article V route reads as if a convention could amend alone', 'Route AV', 'routes.items[AV].who'),
}
ORDER = [42, 19, 40, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22, 23, 27, 43, 44, 45, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 24, 25, 26, 28,
         29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41] + list(range(46, 58))
GROUP_WORD = {'value': 'A value', 'sign': 'A sign', 'grade': 'A grade', 'delay': 'A delay', 'identifier': 'Identifiers',
              'structure': 'Structure', 'encoding': 'Encoding', 'label': 'Labels', 'new': 'Drawn in Phase 2 and Phase 3'}
P0_TYPE_TO_GROUP = {'ID': 'identifier', 'sign': 'sign', 'grade': 'grade', 'delay': 'delay', 'label': 'label',
                    'structure': 'structure', 'encoding': 'encoding'}


def pages(f):
    out = []
    if 'v5-polished' in f:
        out.append('V5 Polished')
    if 'atlas-visual-system' in f:
        out.append('Atlas Visual System')
    if 'Concepts_V2' in f:
        out.append('Concepts V2')
    return '; '.join(out)


def phase0_rows():
    rows = {}
    text = P0_TABLE.read_text()
    sect = text.split('## Reconciliation table', 1)[1].split('\n## ', 1)[0]
    for line in sect.splitlines():
        m = re.match(r'\| (\d+) \| (.*) \|$', line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split(' | ')]
        assert len(cells) == 7, (m.group(1), len(cells))
        rows[int(m.group(1))] = dict(zip(('file', 'location', 'item', 'shown', 'v7', 'type', 'resolution'), cells))
    assert sorted(rows) == list(range(1, 46)), sorted(rows)
    tc = collections.Counter(r['type'] for r in rows.values())
    assert tc == {'ID': 9, 'sign': 1, 'grade': 1, 'delay': 1, 'label': 12, 'structure': 7, 'encoding': 14}, tc
    return rows


def build():
    p0 = phase0_rows()
    p0d = json.loads(P0_DATA.read_text())
    rerun = json.loads(RERUN.read_text())
    # the two value conflicts: Phase 0's findings, and the rerun's, still the same two
    f0 = [(x['location'], x['shown'], x['v7']) for x in p0d['findings']]
    assert [x[0].split('row ')[-1] for x in f0] == ['D03', 'D04'] and [x[1] for x in f0] == ['10', '14'], f0
    rows = []
    for i, n in enumerate(ORDER, start=1):
        grp, res, chap, rules, status = APPLY[n]
        if n <= 45:
            r = p0[n]
            assert P0_TYPE_TO_GROUP[r['type']] == grp or (n == 42 and grp == 'value'), (n, r['type'], grp)
            base = {'row': n, 'print_order': i, 'group': GROUP_WORD[grp], 'origin': 'Phase 0 table, October 20, 2026',
                    'phase0_type': r['type'], 'pages': pages(r['file']), 'location': r['location'], 'item': r['item'],
                    'value_shown': r['shown'], 'phase0_v7_value': r['v7'], 'phase0_resolution': r['resolution']}
        else:
            origin, item, where, fields = NEW[n]
            base = {'row': n, 'print_order': i, 'group': GROUP_WORD[grp], 'origin': origin, 'phase0_type': '',
                    'pages': 'Atlas V7', 'location': fields, 'item': f'{where}: {item}', 'value_shown': '',
                    'phase0_v7_value': '', 'phase0_resolution': ''}
        base.update({'model_value': mv(n), 'resolution_in_guide': res, 'guide_chapter': chap, 'guide_rules': rules,
                     'status': status, 'value_conflict': n == 42})
        rows.append(base)
    # row 42's model value must equal Phase 0's finding: 9 and 13 live, 10 and 14 with R-35
    assert '9 live reforms, 10 with the rejected R-35' in rows[0]['model_value'] and '13 live reforms, 14 with' in rows[0]['model_value']
    assert [(c['location'], c['shown']) for c in rerun['conflicts']] == [(x[0], x[1]) for x in f0]
    return rows, rerun


COLUMNS = {
    'row': {'type': 'integer', 'description': 'Row ID: Phase 0’s number for rows 1 to 45; 46 on for rows added in round 5'},
    'print_order': {'type': 'integer', 'description': 'The order the plate prints, by the data lead’s ruling (e)'},
    'group': {'type': 'category', 'description': 'What a copied drawing could mislead a reader about: a value, a sign, a grade, a delay, identifiers, structure, encoding, labels, or drawn in Phase 2 and Phase 3'},
    'origin': {'type': 'text', 'description': 'Where the row comes from: Phase 0’s table, or the V7.1 issue list item it ties to'},
    'phase0_type': {'type': 'category', 'description': 'Phase 0’s type: ID, sign, grade, delay, label, structure or encoding; empty for new rows'},
    'pages': {'type': 'text', 'description': 'The earlier pages that show the item: V5 Polished, the Atlas Visual System, Concepts V2; Atlas V7 for new rows'},
    'location': {'type': 'text', 'description': 'Where on those pages, as Phase 0 wrote it; for new rows, the model fields'},
    'item': {'type': 'text', 'description': 'The item, as Phase 0 named it; for new rows, the subject and the issue'},
    'value_shown': {'type': 'text', 'description': 'What the earlier page shows, as Phase 0 recorded it; never evidence for a model value'},
    'phase0_v7_value': {'type': 'text', 'description': 'The model value as Phase 0 wrote it on October 20, 2026, kept for the record'},
    'phase0_resolution': {'type': 'text', 'description': 'Phase 0’s proposed resolution'},
    'model_value': {'type': 'text', 'description': 'The model’s value read today by script from the snapshot of October 15, 2026; quotes keep the atlas’s straight apostrophes'},
    'resolution_in_guide': {'type': 'text', 'description': 'The resolution as the guide applies it today'},
    'guide_chapter': {'type': 'text', 'description': 'The chapter that applies it'},
    'guide_rules': {'type': 'text', 'description': 'The rules that apply it, joined with semicolons; none where no rule needs to'},
    'status': {'type': 'category', 'description': 'applied; not printed (no chapter or specimen in work/build/guide/ shows the item); open or due in round 5; or proposed for board 3'},
    'value_conflict': {'type': 'boolean', 'description': 'True for row 42, which holds Phase 0’s two value conflicts, D03 and D04'},
}


def meta(rows, rerun):
    n_new = sum(1 for r in rows if r['row'] >= 46)
    return {
        'file': f'{NAME}.json',
        'kind': 'derived',
        'publisher': ATLAS_PUB,
        'title_or_table': 'Reconciliation of earlier atlas drawings to the model: Phase 0’s 45 rows and the rows added in Phase 3',
        'table_id': 'Phase 0 reconciliation table rows 1 to 45; V7.1 issue list items; nodes, links, loops, reforms, routes, issues, claims, glossary and methods',
        'url': 'work/extract/atlas-v7-data.json',
        'observation_period': 'Model snapshot of October 15, 2026; earlier pages as Phase 0 read them on October 20, 2026, rerun November 13, 2026',
        'geography': 'United States',
        'universe_or_base': f'Phase 0’s 45 rows of conflicts and ambiguities and {n_new} rows for what Phase 2 and Phase 3 drew from the model',
        'unit': 'rows; each model value is text read from the model',
        'date_retrieved': READ_ON,
        'vintage': 'Atlas V7 snapshot of October 15, 2026',
        'snapshot': SNAP,
        'qualification': ('No earlier drawing is evidence for a model value: the value_shown column records what a page showed, and every model_value is read from the model. '
                          'On November 13, 2026 all 2,644 of Phase 0’s comparisons were rerun from Dustin’s three uploads: 2,642 match and 2 conflict, both in row 42 (the Ledger’s reform counts for D03 and D04, which count the rejected R-35); '
                          'Phase 0’s 45 rows are 9 identifier, 1 sign, 1 grade, 1 delay, 12 label, 7 structure and 14 encoding; 8 flags were read in context and set aside. '
                          'Rows 11, 17, 47, 48 and 52 rest partly on V7’s renderer, which is not in this container; their renderer facts are Phase 0’s and the V7.1 list’s readings. '
                          'Row 40’s model value differs from Phase 0’s note: the model’s evidence summary for Loop B4 names L54 the weakest step for U.S. services. '
                          'Chapter and rule numbers are those of November 14, 2026; chapter 11’s numbers move under DR-274 and no row cites chapter 11.'),
        'columns': COLUMNS,
        'printed_source_line': ('Source: Oath & Action’s systems atlas, Who Do They Answer To?, compared with our three earlier atlas pages, '
                                '2,644 comparisons rerun November 13, 2026, United States. Snapshot of October 15, 2026.'),
        'ledger_row': 'not needed: Atlas V7 and the studio’s own Phase 0 files, read by script',
        'derived_from': ['work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md', 'work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json',
                         'work/research/20261113_Atlas-Recheck-Full-Data.json', 'work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md',
                         'work/extract/atlas-v7-data.json'],
        'derivation': ('work/build/scripts/phase-3/research_reconciliation_rows.py: parses Phase 0’s 45 rows, asserts its type counts and its two value conflicts, '
                       'reads each model value from the model (SHA-256 asserted), and maps each resolution to the rules that apply it, read from the chapter files on November 14, 2026'),
        'rerun': {'date': '2026-11-13', 'comparisons': rerun['totals']['rerun_comparisons'],
                  'match': rerun['totals']['rerun_comparisons'] - rerun['totals']['rerun_conflicts'],
                  'conflict': rerun['totals']['rerun_conflicts'], 'flags_set_aside': rerun['totals']['reviewed_false_positives_found_again'],
                  'phase0_rows': 45, 'phase0_rows_by_type': {'ID': 9, 'sign': 1, 'grade': 1, 'delay': 1, 'label': 12, 'structure': 7, 'encoding': 14},
                  'page_side': rerun['totals']['page_side_by_source'], 'differs_from_phase0': len(rerun['differs_from_phase0']),
                  'record': 'work/research/20261113_Atlas-Recheck-Full-Table.md'},
        'domain': 'all',
        'domain_note': 'The rows reach every part of the model',
        'states': [],
    }


def check_rerun(rerun):
    tt = rerun['totals']
    assert (tt['phase0_comparisons'], tt['rerun_comparisons'], tt['rerun_conflicts'], tt['reviewed_false_positives_found_again']) == (2644, 2644, 2, 8)
    assert rerun['v7_model']['sha256'] == MODEL_SHA and rerun['differs_from_phase0'] == []
    p0 = json.loads(P0_DATA.read_text())['summary']
    assert p0['auto_findings'] == 2 and p0['reviewed_false_positives'] == 8 and p0['documents_scanned'] == 121


def main():
    rows, rerun = build()
    check_rerun(rerun)
    data = json.dumps({'rows': rows}, indent=1, ensure_ascii=False) + '\n'
    side = json.dumps(meta(rows, rerun), indent=1, ensure_ascii=False) + '\n'
    for txt in (data, side):
        assert '—' not in txt and '‑' not in txt and 'Disclosure:' not in txt
    dp, mp = OUT / f'{NAME}.json', OUT / f'{NAME}.meta.json'
    if '--check' in sys.argv:
        same = dp.is_file() and mp.is_file() and dp.read_text() == data and mp.read_text() == side
        print(f'{NAME}: {"unchanged" if same else "WOULD CHANGE"} ({len(rows)} rows)')
        return 0 if same else 1
    dp.write_text(data)
    mp.write_text(side)
    print(f'{NAME}: wrote {len(rows)} rows ({sum(1 for r in rows if r["row"] <= 45)} from Phase 0, {sum(1 for r in rows if r["row"] >= 46)} new)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
