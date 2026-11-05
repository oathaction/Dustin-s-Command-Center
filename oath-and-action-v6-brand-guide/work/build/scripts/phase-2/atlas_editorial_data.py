"""Build the shared dataset for the editorial atlas systems of November 5, 2026 (DR-28 to DR-35, D2-71, D2-72).

Joins Atlas V7 (the master: model, issues, reforms, pathways, evidence) with the dark atlas's plain-language
layer (chapter stories, short labels, "why it matters" lines, plain loop names, real-world examples, mix-ups),
and adds the plain names Dustin's newest atlas leads with (DR-35).

Usage:
    python3 -I work/build/scripts/phase-2/atlas_editorial_data.py

Reads  work/extract/atlas-v7-data.json and work/extract/atlas-interactive-concept-v2-data.json
       (extract them from the supplied HTML files with the atlas-data script tag; see D2-69)
Writes work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
V7 = json.loads((ROOT / 'work/extract/atlas-v7-data.json').read_text())
IC = json.loads((ROOT / 'work/extract/atlas-interactive-concept-v2-data.json').read_text())
OLD = json.loads((ROOT / 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json').read_text())
OUT = ROOT / 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json'

# DR-35: the plain names lead, the formal titles sit beneath. Questions as Dustin's newest atlas shows them.
PLAIN = {
    'A': ('Wealth', 'Who holds the cards?'),
    'B': ('Voice', 'Who pays for influence?'),
    'C': ('Elections', 'Who picks them?'),
    'D': ('Checks', 'Who checks their work?'),
    'E': ('Policy', 'Whose side are the rules on?'),
    'EC': ('Your household', 'Who lives with the results?'),
    'TC': ('Technology', 'Who controls the machines?'),
    'X': ('Outside forces', None),
}
ORDER = ['X', 'A', 'B', 'C', 'D', 'E', 'EC', 'TC']


def pick(d, *keys):
    return {k: d.get(k) for k in keys if k in d}


def build():
    parts_ic = {p['id']: p for p in IC['parts']}
    stories = IC['story'].get('parts', {})
    old_areas = {a['id']: a for a in OLD['areas']}
    parts = []
    for pid in ORDER:
        p = parts_ic[pid]
        plain, q = PLAIN[pid]
        st = stories.get(pid, {}) if isinstance(stories, dict) else {}
        nodes = [n for n in V7['nodes'] if (V7['nodes'][n].get('cluster') == pid or (pid == 'EC' and V7['nodes'][n].get('layer') == 'economy') or (pid == 'TC' and V7['nodes'][n].get('layer') == 'technology'))]
        if pid == 'X':
            nodes = [n for n in V7['nodes'] if V7['nodes'][n].get('type') == 'driver']
        parts.append({
            'id': pid, 'plain_name': plain, 'plain_question': q, 'formal_title': p['title'],
            'chapter': st.get('chapter'), 'story': st.get('story'), 'text': p.get('text'),
            'nodes': nodes,
            'groups': [pick(old_areas[g], 'id', 'title', 'text', 'nodes') for g in ('production', 'household', 'money')] if pid == 'EC' else None,
        })

    nodes = {}
    for k, n in V7['nodes'].items():
        d = IC['nodes'][k]
        o = OLD['nodes'].get(k, {})
        nodes[k] = {
            'id': k, 'part': d.get('part') or n.get('cluster'), 'layer': n['layer'], 'type': n['type'],
            'title': n['title'], 'label': d.get('label') or o.get('label') or n['title'],
            'description': n.get('description'), 'increase_means': n.get('increase_means'),
            'why': d.get('why'), 'kind_plain': n.get('kind_plain'), 'indicator': n.get('indicator'),
            'domain': n.get('domain'), 'domains': d.get('domains'),
            'loops': sorted({lp for lp, L in V7['loops'].items() if k in {c[0] if isinstance(c, list) else c for c in (L.get('chain') or [])}}),
        }

    links = {}
    for k, l in V7['links'].items():
        links[k] = pick(l, 'id', 'layer', 'from', 'to', 'polarity', 'type', 'delay', 'evidence', 'contested', 'loops',
                        'name', 'plain', 'sign_meaning', 'qualification', 'mechanism', 'counterevidence')

    loops = {}
    for k, L in V7['loops'].items():
        d = IC['loops'][k]
        o = OLD['loops'][k]
        loops[k] = {
            **pick(L, 'id', 'type', 'title', 'summary', 'how_to_read', 'closure', 'evidence_summary', 'qualification',
                   'case', 'chain', 'chain_labels', 'links', 'delay', 'direction', 'reference_mode', 'nonlinearity',
                   'adaptation', 'fix', 'reforms'),
            'plain_name': d.get('name'), 'home': d.get('home'), 'read_aloud_source': d.get('read'),
            'kind_word': o.get('kind_word'), 'kind_gloss': o.get('kind_gloss'), 'closure_short': o.get('closure_short'),
            'conceptual': o.get('conceptual'), 'hypothesized': o.get('hypothesized'), 'weakest': o.get('weakest'),
            'steps': o.get('steps'), 'stations': o.get('stations'), 'delay_word': o.get('delay_word'),
        }

    # V7's renderer holds the editor's disclosures for eight reform profiles (INTERESTS and INTEREST_TEXT in the
    # V7 script); the profiles flag them with interest_note. Copied here word for word.
    interests = {'R-01': 'nomination', 'R-02': 'nomination', 'R-47': 'nomination', 'R-22': 'care', 'R-24': 'care',
                 'R-31': 'care', 'R-39': 'contracting', 'R-49': 'veteran'}
    interest_text = {
        'nomination': "Oath & Action's editor works with the Yes on 3 campaign for Massachusetts Question 3 and promotes it through Veterans for All Voters, where he is Massachusetts state lead. He also co-leads Ranked Choice Melrose, a local campaign.",
        'care': "Oath & Action's editor co-founded and led a home care company.",
        'contracting': "Oath & Action's editor worked as a manager at a large government contractor. This profile proposes building more capacity inside government.",
        'veteran': "Oath & Action's editor is an Army veteran.",
    }
    reforms = {}
    for k, r in V7['reforms'].items():
        d = IC['reforms'][k]
        reforms[k] = {**pick(r, 'id', 'title', 'summary', 'what_it_changes', 'who_decides', 'legal_authority',
                             'implementation', 'costs', 'failure_risks', 'problem_evidence', 'remedy_evidence',
                             'tradeoffs', 'success_measures', 'alternatives', 'status', 'rejected', 'interest_note',
                             'targets', 'loops', 'band', 'routes', 'effects', 'effects_confidence', 'complements'),
                      'short': d.get('short'), 'lead': d.get('lead'),
                      'disclosure': interest_text[interests[k]] if k in interests else None}

    issues = {}
    for k, i in V7['issues'].items():
        ex = IC['examples'].get(k, {})
        issues[k] = {**pick(i, 'id', 'domain', 'subsystem', 'title', 'summary', 'mechanism', 'grade', 'jurisdiction',
                            'observed', 'evidence_note', 'remedy_note', 'response', 'actor', 'tradeoff',
                            'success_measure', 'loops', 'nodes', 'aimed_reforms', 'shared_reforms', 'status',
                            'retired', 'sources'),
                     'problem_example': ex.get('problem_example'), 'fix_example': ex.get('fix_example')}

    sources = {k: pick(s, 'id', 'title', 'publisher', 'year', 'date', 'type', 'url', 'same_as')
               for k, s in V7['sources'].items()}

    data = {
        'built': '2026-11-05',
        'sources_of_this_file': ['Atlas V7 (20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html), the master',
                                 'Dark atlas (20261019_Oath-And-Action-Atlas-Interactive-Concept_V2.html), plain-language layer',
                                 'Plain names from Dustin\'s newest atlas (DR-35)'],
        'meta': V7['meta'],
        'questions': IC['story']['questions'],
        'opening': IC['story']['opening'],
        'parts': parts,
        'domains': V7['domains'],
        'hubs': V7['hubs'],
        'pathways': [pick(p, 'id', 'hub', 'title', 'question', 'short_answer', 'model_refs') for p in V7['pathways']],
        'nodes': nodes, 'links': links, 'loops': loops, 'loop_order': OLD['loop_order'], 'loop_groups': OLD['groups'],
        'reforms': reforms, 'issues': issues, 'sources': sources,
        'glossary': V7['glossary'], 'mixups': IC['mixups'], 'numbers': V7['numbers'],
        'families': OLD['families'], 'effect_codes': OLD['effect_codes'], 'route_names': OLD['route_names'],
        'feasibility_scale': OLD['feasibility_scale'], 'omissions': V7['omissions'],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print('wrote', OUT.relative_to(ROOT), f'{OUT.stat().st_size / 1e6:.2f} MB',
          {k: len(v) for k, v in data.items() if isinstance(v, (list, dict))})


if __name__ == '__main__':
    build()
