"""Shared helpers for the atlas concepts of October 30, 2026 (DR-12 to DR-21).

Every concept maker imports this file by path (D1-05), for example:

    import importlib.util, pathlib
    p = pathlib.Path('work/build/scripts/phase-2/atlas_concepts_common.py').resolve()
    spec = importlib.util.spec_from_file_location('acc', p); acc = importlib.util.module_from_spec(spec); spec.loader.exec_module(acc)

It gives one way to read the model, the palette, the evidence and sign vocabulary, the
Civic Line icon for each variable and reform, and an inliner that keeps icon ids unique (D2-43, D2-52).

Run it directly to write the shared variable-to-icon map:
    python3 -I work/build/scripts/phase-2/atlas_concepts_common.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
MODEL_PATH = ROOT / 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json'
ICONS = ROOT / 'work/build/assets/civic-line'
SHARED = ROOT / 'work/boards/phase-2/atlas-concepts/shared'

# Locked palette, Master Brief section 3, and the approved derived tints (T4, R4 pending)
PALETTE = {
    'newsprint': '#DCD9D2',
    'charcoal': '#121212',
    'pillar_red': '#E63946',
    'prussian': '#1F2D5A',
    'stone': '#5D636D',
    'verdigris': '#4A7C74',
    'white': '#FFFFFF',
    'deep_stone': '#4E535B',   # T4: 5.49:1 on Newsprint, for small secondary text
}

# V7 grade words (M2) with plain glosses, and the V7 line code (M1)
GRADES = {
    'documented': ('Documented', 'on the public record', 'solid'),
    'well-supported': ('Well supported', 'strong research evidence', 'solid'),
    'plausible': ('Plausible', 'some evidence', 'dashed'),
    'plausible_contested': ('Contested', 'evidence disputed', 'dash-dot'),
    'hypothesis': ('Hypothesis', 'untested', 'dotted'),
}
DELAYS = {'S': 'under 2 years', 'M': '2 to 10 years', 'L': 'over 10 years'}
SIGN_WORDS = {'+': 'raises', '-': 'lowers', None: 'decides'}   # authority links carry no sign
SIGN_RULE = 'A plus sign means the two variables move the same way. It does not mean the change is good.'

# Each V7 variable and its Civic Line icon. All 51 variables have one.
VARIABLE_ICON = {
    'A1': 'CL-049', 'A2': 'CL-050', 'A3': 'CL-051', 'A4': 'CL-052', 'A5': 'CL-053', 'A6': 'CL-054',
    'B1': 'CL-015', 'B2': 'CL-032', 'B3': 'CL-006', 'B4': 'CL-008', 'B5': 'CL-007', 'B6': 'CL-033',
    'C1': 'CL-009', 'C2': 'CL-010', 'C3': 'CL-011', 'C4': 'CL-012', 'C5': 'CL-013',
    'D1': 'CL-025', 'D2': 'CL-026', 'D3': 'CL-027', 'D4': 'CL-028', 'D5': 'CL-029', 'D6': 'CL-030', 'D7': 'CL-014',
    'E1': 'CL-017', 'E2': 'CL-018',
    'X1': 'CL-034', 'X2': 'CL-035', 'X3': 'CL-036', 'X4': 'CL-037', 'X5': 'CL-038',
    'EC1': 'CL-055', 'EC2': 'CL-056', 'EC3': 'CL-057', 'EC4': 'CL-058', 'EC5': 'CL-059', 'EC6': 'CL-060',
    'EC7': 'CL-061', 'EC8': 'CL-062', 'EC9': 'CL-063', 'EC10': 'CL-064', 'EC11': 'CL-065', 'EC12': 'CL-066',
    'TC1': 'CL-039', 'TC2': 'CL-040', 'TC3': 'CL-041', 'TC4': 'CL-042', 'TC5': 'CL-043', 'TC6': 'CL-044',
    'TC7': 'CL-045', 'TC8': 'CL-046',
}
# Other atlas ideas with an icon of their own
CONCEPT_ICON = {'feedback_loop': 'CL-024', 'evidence': 'CL-023', 'policy': 'CL-071', 'reform': 'CL-072',
                'explain': 'CL-019', 'track': 'CL-020', 'connect': 'CL-021', 'act': 'CL-022'}
EDITIONS = ('red-black', 'black', 'red-newsprint', 'newsprint')


def load_model():
    return json.loads(MODEL_PATH.read_text())


def reform_icon(reform_id):
    """Reforms R-01 to R-50 each have a Civic Line icon with the same ID."""
    return reform_id


def icon_path(icon_id, edition='black'):
    if edition not in EDITIONS:
        raise ValueError(edition)
    hits = sorted((ICONS / edition).glob(f'*-{icon_id}-*.svg'))
    if len(hits) != 1:
        raise FileNotFoundError(f'{icon_id} {edition}: {hits}')
    return hits[0]


def icon_svg(icon_id, edition='black', uid='', size=None, cls='cl-icon', title=None):
    """The approved drawing, unchanged, as inline SVG markup with every id prefixed by uid (D2-43).

    edition: 'red-black' or 'red-newsprint' carry the signature red accent; 'black' and 'newsprint' are one color.
    In a row or a menu, use the one-color edition, and only the current item keeps its red (Rule 05.3, G1-07).
    The red in a red edition counts as signature red: mark the wrapper data-red="signature".
    """
    src = icon_path(icon_id, edition).read_text()
    src = re.sub(r'<\?xml[^>]*\?>\s*', '', src)
    root = re.search(r'id="([^"]+)"', src).group(1)
    new_root = f'{uid}-{root}' if uid else root
    src = src.replace(root, new_root)
    if size:
        src = re.sub(r'width="128" height="128"', f'width="{size}" height="{size}"', src, count=1)
    src = src.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" focusable="false" ', 1)
    if title is None:
        src = re.sub(r'<title>.*?</title>\s*', '', src, flags=re.S)
    src = re.sub(r'<desc>.*?</desc>\s*', '', src, flags=re.S)
    return src


def loop_steps(model, loop_id):
    """The numbered steps of a loop in order, each a dict with id, from, to, polarity, type, delay, evidence, name."""
    return model['loops'][loop_id]['steps']


def write_shared():
    m = load_model()
    SHARED.mkdir(parents=True, exist_ok=True)
    inv = {r['id']: r['label'] for r in json.loads((ICONS / '20261029_Civic-Line-Inventory.json').read_text())['icons']}
    rows = []
    for vid in m['order']:
        n = m['nodes'][vid]
        ic = VARIABLE_ICON[vid]
        rows.append({'variable': vid, 'area': n['area'], 'v7_label': n['label'], 'v7_title': n['title'],
                     'icon': ic, 'icon_name': inv[ic], 'black': str(icon_path(ic, 'black').relative_to(ROOT)),
                     'red_black': str(icon_path(ic, 'red-black').relative_to(ROOT))})
    reforms = [{'reform': rid, 'title': m['reforms'][rid]['title'], 'icon': rid, 'icon_name': inv.get(rid)}
               for rid in sorted(m['reforms'])]
    out = {'date': '20261030', 'note': 'Every V7 variable and reform mapped to its Civic Line icon. Labels on the page use the V7 label or title, never the icon name.',
           'variables': rows, 'reforms': reforms, 'concepts': CONCEPT_ICON}
    assert len(rows) == 51 and all(r['icon_name'] for r in rows)
    (SHARED / '20261030_Variable-Icon-Map.json').write_text(json.dumps(out, indent=1))
    print('wrote', SHARED / '20261030_Variable-Icon-Map.json', len(rows), 'variables', len(reforms), 'reforms')


if __name__ == '__main__':
    write_shared()
