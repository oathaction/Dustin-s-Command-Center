"""Palette proofs for Phase 3, round 0 (November 11, 2026).

Usage:
    python3 -I work/boards/phase-3/round-0/palettes/build_palette_proofs.py
    node work/boards/phase-3/round-0/palettes/capture_palette_proofs.js
    python3 -I work/boards/phase-3/round-0/palettes/build_palette_proofs.py --verify

The first command reads the token release (work/build/tokens/tokens.json), the palette rules and two public datasets
already in the repository, and writes:
    work/handoffs/phase-3/20261111_Palette-Proposal.json           every proposed token, with values and ratios
    work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs.html          the proof sheet
    work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs-Measures.json every measured ratio on the sheet
The capture script writes the PNG captures beside the sheet and a probe file; --verify then samples the captures and
checks that the page drew each swatch in its token's color and that the browser's simulation filters match this
script's simulation.

Method. Colors mix in OKLab (D1-04). Contrast is WCAG 2.2's ratio from relative luminance. Grayscale chips take the
neutral gray with the same relative luminance, so a chip keeps its contrast. Color-vision simulations follow
Machado, Oliveira and Fernandes (2009) at severity 1.0, applied in linear sRGB, as the Phase 2 palette lab did; the
captures apply the same matrices through SVG feColorMatrix filters, which work in linear RGB by default.
"""
import ast
import csv
import html
import importlib.util
import itertools
import json
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATE = '20261111'
SHEET = HERE / f'{DATE}_Palette-Proofs.html'
MEASURES = HERE / f'{DATE}_Palette-Proofs-Measures.json'
PROPOSAL = ROOT / 'work/handoffs/phase-3' / f'{DATE}_Palette-Proposal.json'
PROBES = HERE / f'{DATE}_Palette-Proofs-Capture-Log.json'
TOKENS_JSON = ROOT / 'work/build/tokens/tokens.json'
TOKENS_CSS = ROOT / 'work/build/tokens/tokens.css'
PUBLIC = ROOT / 'work/build/data'          # the kit's data folder (contract C1); the Phase 2 copies stay as records
TILES = ROOT / 'work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json'
WORDMARK = ROOT / 'work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg'

spec = importlib.util.spec_from_file_location('oa_color', ROOT / 'work/build/scripts/phase-1/oa_color.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
P = C.PALETTE
MINUS = '−'
NBSP = ' '

# ------------------------------------------------------------------------------------------------ color math
CVD = {  # Machado, Oliveira and Fernandes 2009, severity 1.0, linear sRGB
    'protanopia': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    'deuteranopia': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    'tritanopia': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}
SIMS = ['grayscale', 'protanopia', 'deuteranopia', 'tritanopia']
SIM_WORD = {'grayscale': 'Grayscale', 'protanopia': 'Protanopia', 'deuteranopia': 'Deuteranopia', 'tritanopia': 'Tritanopia'}


def simulate(h, kind):
    if kind == 'grayscale':
        return gray_of(h)
    r, g, b = (C.lin(c) for c in C.hex_to_rgb(h))
    m = CVD[kind]
    return C.rgb_to_hex(tuple(C.delin(min(1, max(0, m[i][0] * r + m[i][1] * g + m[i][2] * b))) for i in range(3)))


def gray_of(h):
    """The neutral gray with the same WCAG relative luminance."""
    v = C.delin(C.luminance(h))
    return C.rgb_to_hex((v, v, v))


def mix(base, toward, t):
    return C.mix_oklab(P.get(base, base), P.get(toward, toward), t)[0]


def L(h):
    return round(C.to_oklab(h)[0], 3)


def cr(a, b):
    return round(C.contrast(a, b), 2)


def dE(a, b):
    return round(C.delta_e_ok(a, b), 3)


def luma(h):
    """The gray level CSS filter grayscale(1) gives: Rec. 709 weights on the encoded components."""
    r, g, b = C.hex_to_rgb(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def screen_pct(h):
    """Black ink coverage on White paper that matches the color's luminance (dot gain ignored)."""
    return round(100 * (1 - C.luminance(h)))


# ------------------------------------------------------------------------------------------------ tokens
TOK = json.loads(TOKENS_JSON.read_text())
RELEASE = TOK['$extensions']['org.oathandaction']['version']


def node(path):
    n = TOK
    for k in path.split('.'):
        n = n[k]
    return n


def hex_of(path, proposed=None):
    proposed = proposed or {}
    if path in proposed:
        v = proposed[path]
        return hex_of(v[1:-1], proposed) if isinstance(v, str) and v.startswith('{') else v
    n = node(path)
    v = n['$value']
    if isinstance(v, str) and v.startswith('{'):
        return hex_of(v[1:-1], proposed)
    return v['hex'].upper()


def css_name(path):
    out = path.replace('.', '-')
    out = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', out).lower()
    return '--' + out


GROUND_HEX = {'newsprint': P['newsprint'], 'white': P['white'], 'charcoal': P['charcoal'], 'prussian': P['prussian']}
GROUND_WORD = {'newsprint': 'Newsprint', 'white': 'White', 'charcoal': 'Charcoal', 'prussian': 'Prussian'}
SURF = {'newsprint': 'onNewsprint', 'white': 'onWhite', 'charcoal': 'onCharcoal', 'prussian': 'onPrussian'}

# ------------------------------------------------------------------------------------------------ the proposal
# New primitives: the two Prussian steps the diverging scale lacks on Charcoal (N-10). Everything else reuses a value.
NEW_TINTS = {
    'prussianN56': ('prussian', 'newsprint', 0.56, 'Strong Prussian end of the diverging scale on Charcoal'),
    'prussianN29': ('prussian', 'newsprint', 0.29, 'Near Prussian step of the diverging scale on Charcoal'),
}
NEW_TINT_HEX = {k: mix(b, t, a) for k, (b, t, a, _) in NEW_TINTS.items()}
# Existing primitives that take a second job (their job sentence widens; no value changes).
WIDENED = {
    'oa.color.tint.stoneC72': 'Band on Charcoal, and the midpoint of the diverging scale on Charcoal',
    'oa.color.tint.verdigrisC20': 'Third sequential Verdigris step on Charcoal, and the near Verdigris step of the diverging scale on Charcoal',
    'oa.color.tint.verdigrisN25': 'Fourth sequential Verdigris step on Charcoal, and the strong Verdigris end of the diverging scale on Charcoal',
    'oa.color.tint.prussianN62': 'Light Prussian step of the diverging scale on Newsprint, and the Prussian group of the categorical set on Charcoal',
    'oa.color.tint.stoneN55': 'Light Stone fill for a category under the subject, and the ghost lines of the other groups in small multiples on Newsprint',
    'oa.color.tint.stoneC40': 'Second gray step of a phone tile map on Charcoal, and the ghost lines of the other groups in small multiples on Charcoal',
}

DIV_C = ['{oa.color.tint.prussianN56}', '{oa.color.tint.prussianN29}', '{oa.color.tint.stoneC72}',
         '{oa.color.tint.verdigrisC20}', '{oa.color.tint.verdigrisN25}']
DIV_LABEL_C = ['charcoal', 'newsprint', 'newsprint', 'newsprint', 'charcoal']
DIV_WORDS = ['strong Prussian end', 'near Prussian step', 'midpoint, tinted toward the ground',
             'near Verdigris step', 'strong Verdigris end']
CAT = {
    'newsprint': ['{oa.color.palette.charcoal}', '{oa.color.palette.verdigris}', '{oa.color.palette.prussian}', '{oa.color.palette.stone}'],
    'charcoal': ['{oa.color.palette.newsprint}', '{oa.color.palette.verdigris}', '{oa.color.tint.prussianN62}', '{oa.color.palette.stone}'],
}
CAT_LABEL = {'newsprint': ['white', 'white', 'white', 'charcoal'], 'charcoal': ['charcoal', 'white', 'charcoal', 'newsprint']}
CAT_NAMES = ['Charcoal group', 'Verdigris group', 'Prussian group', 'Stone group']
CAT_INK_WORD = {'newsprint': ['Charcoal', 'Verdigris', 'Prussian', 'Stone, hatched'],
                'charcoal': ['Newsprint', 'Verdigris', 'Prussian lifted 62%', 'Stone, hatched']}


def cat_label_path(i, surface_key):
    """Groups 1 to 3 set their labels on the fill; group 4's label sits beside the hatch or on a halo, and says so."""
    return (f'oa.chart.color.categorical.labelBeside.group{i}.{surface_key}' if i == 4
            else f'oa.chart.color.categorical.label.group{i}.{surface_key}')
CAT_MARKER = ['circle', 'square', 'triangle', 'diamond']
CAT_PATTERN = ['solid', 'solid', 'solid', 'hatch']
GHOST = {'newsprint': '{oa.color.tint.stoneN55}', 'charcoal': '{oa.color.tint.stoneC40}'}

ATLAS_BUILD = ROOT / 'work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py'
ATLAS_COMMON = ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py'


def atlas_line_code():
    """D3-84: read the line code from the atlas build itself (wire_marks, pattern, fitted and their constants), so the
    tokens, Rule 10.10 and Rule 13.4 state one set of numbers. Only the function `pattern` is run; everything else is read
    from the source text, with the line it sits on."""
    src = ATLAS_BUILD.read_text()
    tree = ast.parse(src)
    fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    asg = {n.targets[0].id: n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    ns = {}
    exec(compile(ast.Module(body=[fn['pattern']], type_ignores=[]), str(ATLAS_BUILD), 'exec'), ns)
    tex = {t: ns['pattern'](t, 1) for t in ('solid', 'dashed', 'dash-dot', 'dotted')}
    wm = ast.get_source_segment(src, fn['wire_marks'])
    off = re.search(r'off = w / 2 \+ ([\d.]+)', wm)
    rail = re.search(r'class="rail"[^\n]*?stroke-width="([\d.]+)"', wm)
    clear = re.search(r"if tex == 'dotted':\s*body\[-1\] = \(body\[-1\]\[0\] - ux \* ([\d.]+) \* w", wm)
    assert off and rail and clear, 'wire_marks changed shape; read it again by hand'
    rail_w, off_k = float(rail.group(1)), float(off.group(1))
    key_call = re.search(r'grade_glyph\(g, (\d+)\)', ast.get_source_segment(src, fn['evidence_key']))
    common = ast.parse(ATLAS_COMMON.read_text())
    grades = next(ast.literal_eval(n.value) for n in common.body if isinstance(n, ast.Assign)
                  and getattr(n.targets[0], 'id', '') == 'GRADES')
    widths = sorted(ast.literal_eval(asg['ARROW'].value))
    return {
        'source': str(ATLAS_BUILD.relative_to(ROOT)),
        'patterns_per_width': {k: (None if v[0] is None else v[0]) for k, v in tex.items()},
        'caps': {k: v[1] for k, v in tex.items()},
        'pattern_line': fn['pattern'].lineno, 'wire_marks_line': fn['wire_marks'].lineno,
        'fitting': ast.get_docstring(fn['fitted']), 'fitted_line': fn['fitted'].lineno,
        'line_widths': widths, 'line_widths_from': f'ARROW, line {asg["ARROW"].lineno}',
        'hollow_rail_px': rail_w, 'hollow_rail_offset': f'w / 2 + {off_k:g}',
        'hollow_inner_gap': f'one line width plus {2 * off_k - rail_w:g} px',
        'dotted_head_clearance_widths': float(clear.group(1)),
        'key_glyph_px_at_2px': {'grade_glyph default': fn['grade_glyph'].args.defaults[0].value,
                                'evidence_key': int(key_call.group(1)) if key_call else None},
        'grades': grades,
        'defines_shortest_line': bool(re.search(r'min_?run|shortest', src, re.I)),
        'defines_record_square': bool(re.search(r'record.?square', src, re.I)),
    }


ALC = atlas_line_code()
# The hollow line: rails of ALC['hollow_rail_px'] centered at w/2 + 0.5 either side, so the ground between them is one line
# width at every width (2 x (w/2 + 0.5) - 1 = w).
assert ALC['hollow_rail_px'] == 1 and ALC['hollow_inner_gap'] == 'one line width plus 0 px'
# Display words and glosses: Rule 13.3's table, as Rule 12.6's key prints them (D3-84 names the hypothesis gloss).
GLOSS = {'documented': 'on the public record', 'well-supported': 'strong research evidence', 'plausible': 'some evidence',
         'plausible_contested': 'evidence disputed', 'hypothesis': 'not yet tested'}
TEX_KEY = {'documented': 'documented', 'wellSupported': 'well-supported', 'plausible': 'plausible',
           'contested': 'plausible_contested', 'hypothesis': 'hypothesis'}
GRADES = [  # (key, V7 value, word, gloss, texture, pattern per 1 px of line width, cap), patterns read from the atlas build
    *[(k, v, ALC['grades'][v][0], GLOSS[v], ALC['grades'][v][2], ALC['patterns_per_width'][ALC['grades'][v][2]],
       ALC['caps'][ALC['grades'][v][2]]) for k, v in TEX_KEY.items()],
    ('conceptual', None, 'Conceptual step', 'no complete numbered chain, as in Loops B2, B3 and R9', 'hollow', None, 'butt'),
]
MIN_RUN = 20            # line widths; set here, since the atlas build defines none (see the proposal's line_code_source)
RECORD_SQUARE = 7       # px; set here from the Phase 2 atlas design frame memo, since the atlas build draws none
V7_RENDERER = {'plausible': '9 4', 'contested': '9 3 2 3', 'hypothesis': '2 4'}
LINE_WIDTHS = ALC['line_widths']

PROPOSED = {}   # token path -> value reference or hex, for hex_of()
for k, h in NEW_TINT_HEX.items():
    PROPOSED[f'oa.color.tint.{k}'] = h
for i in range(5):
    PROPOSED[f'oa.chart.color.diverging.fill.step{i + 1}.onCharcoal'] = DIV_C[i]
    PROPOSED[f'oa.chart.color.diverging.label.step{i + 1}.onCharcoal'] = f'{{oa.color.palette.{DIV_LABEL_C[i]}}}'
for g in ('newsprint', 'charcoal'):
    for i in range(4):
        PROPOSED[f'oa.chart.color.categorical.fill.group{i + 1}.{SURF[g]}'] = CAT[g][i]
        PROPOSED[cat_label_path(i + 1, SURF[g])] = f'{{oa.color.palette.{CAT_LABEL[g][i]}}}'
    PROPOSED[f'oa.chart.color.ghost.{SURF[g]}'] = GHOST[g]


def hx(path):
    return hex_of(path, PROPOSED)


def is_proposed(path):
    return path in PROPOSED


# ------------------------------------------------------------------------------------------------ palette sets
def seq_paths(g):
    return [f'oa.chart.color.sequential.fill.step{i}.{SURF[g]}' for i in range(1, 6)], \
           [f'oa.chart.color.sequential.label.step{i}.{SURF[g]}' for i in range(1, 6)]


def div_paths(g):
    return [f'oa.chart.color.diverging.fill.step{i}.{SURF[g]}' for i in range(1, 6)], \
           [f'oa.chart.color.diverging.label.step{i}.{SURF[g]}' for i in range(1, 6)]


def mag_paths(g):
    return [f'oa.chart.color.magnitude.fill.step{i}.{SURF[g]}' for i in range(1, 5)], \
           [f'oa.chart.color.magnitude.label.step{i}.{SURF[g]}' for i in range(1, 5)]


VS_PAIR = {'Group 2', 'Group 4'}    # Verdigris and Stone, 0.05 apart in lightness (D2-95)


def cat_paths(g):
    return [f'oa.chart.color.categorical.fill.group{i}.{SURF[g]}' for i in range(1, 5)], \
           [cat_label_path(i, SURF[g]) for i in range(1, 5)]


PALETTES = {
    'sequential': {'name': 'Sequential Verdigris', 'kind': 'ordered', 'paths': seq_paths,
                   'step_names': [f'Step {i}' for i in range(1, 6)], 'sample': ['48.2', '57.9', '63.4', '67.1', '74.0']},
    'diverging': {'name': 'Diverging pair B', 'kind': 'diverging', 'paths': div_paths,
                  'step_names': ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5'],
                  'sample': [f'{MINUS}3.9', f'{MINUS}0.9', '+0.2', '+1.3', '+4.8']},
    'categorical': {'name': 'Categorical, four inks', 'kind': 'categorical', 'paths': cat_paths,
                    'step_names': ['Group 1', 'Group 2', 'Group 3', 'Group 4'], 'sample': ['24.0', '23.3', '12.7', '2.7']},
    'magnitude': {'name': 'Magnitude, Stone steps', 'kind': 'ordered', 'paths': mag_paths,
                  'step_names': [f'Step {i}' for i in range(1, 5)], 'sample': ['0.4', '2.1', '4.8', '9.6']},
}
# Grounds each palette is measured on. White prints the Newsprint values, as charts in a printed report sit on the
# paper (DR-53); charts never sit on Prussian, which the Prussian panel measures.
PLATES = {'sequential': ['newsprint', 'charcoal', 'white'], 'diverging': ['newsprint', 'charcoal', 'white'],
          'categorical': ['newsprint', 'charcoal', 'white'], 'magnitude': ['newsprint', 'charcoal', 'white']}
TOKEN_GROUND = {'newsprint': 'newsprint', 'white': 'newsprint', 'charcoal': 'charcoal'}


def measure_set(pid, ground):
    pal = PALETTES[pid]
    fills, labels = pal['paths'](TOKEN_GROUND[ground])
    gh = GROUND_HEX[ground]
    rows = []
    for i, (fp, lp) in enumerate(zip(fills, labels)):
        f, lab = hx(fp), hx(lp)
        label_ground = f
        if pid == 'categorical' and i == 3:
            label_ground = gh      # the hatched group's label sits on a halo of the ground
        rows.append({
            'name': pal['step_names'][i], 'fill_token': fp, 'fill_css': css_name(fp), 'fill_hex': f,
            'fill_status': 'proposed' if is_proposed(fp) else 'in tokens', 'fill_on_ground': cr(f, gh),
            'label_token': lp, 'label_css': css_name(lp), 'label_hex': lab,
            'label_status': 'proposed' if is_proposed(lp) else 'in tokens',
            'label_on_fill': cr(lab, label_ground), 'label_ground': 'halo of the ground' if label_ground == gh and pid == 'categorical' else 'the fill',
            'oklab_L': L(f), 'luminance_gray': gray_of(f), 'black_screen_pct': screen_pct(f),
            **{f'sim_{k}': simulate(f, k) for k in CVD},
        })
    hs = [r['fill_hex'] for r in rows]
    pairs = list(zip(range(len(hs)), range(1, len(hs)))) if pal['kind'] != 'categorical' else list(itertools.combinations(range(len(hs)), 2))
    closest = {}
    for k in ['normal'] + list(CVD):
        f = (lambda x: x) if k == 'normal' else (lambda x, k=k: simulate(x, k))
        ds = [(dE(f(hs[a]), f(hs[b])), rows[a]['name'], rows[b]['name']) for a, b in pairs]
        m = min(ds)
        closest[k] = {'delta_e_ok': m[0], 'between': [m[1], m[2]]}
    dl = [(round(abs(rows[a]['oklab_L'] - rows[b]['oklab_L']), 3), rows[a]['name'], rows[b]['name']) for a, b in pairs]
    out = {'palette': pid, 'ground': ground, 'ground_hex': gh, 'tokens_from': TOKEN_GROUND[ground], 'rows': rows,
           'pairs_measured': 'neighbors' if pal['kind'] != 'categorical' else 'every pair', 'closest': closest,
           'lightness_gaps': [{'delta_L': d, 'between': [a, b]} for d, a, b in dl],
           'smallest_lightness_gap': min(dl)[0]}
    Ls = [r['oklab_L'] for r in rows]
    if pal['kind'] == 'ordered':
        out['grayscale_order_holds'] = all(a > b for a, b in zip(Ls, Ls[1:])) or all(a < b for a, b in zip(Ls, Ls[1:]))
    if pal['kind'] == 'diverging':
        out['grayscale_order_holds'] = (Ls[0] != Ls[2]) and ((Ls[1] - Ls[2]) * (Ls[3] - Ls[2]) > 0)
        out['end_pair'] = {'delta_L': round(abs(Ls[0] - Ls[4]), 3), 'delta_e_ok': dE(hs[0], hs[4]),
                           **{f'delta_e_{k}': dE(simulate(hs[0], k), simulate(hs[4], k)) for k in CVD},
                           'note': 'The two ends are meant to match in lightness; a boxed arrow or a printed sign carries the direction'}
    if pal['kind'] == 'categorical':
        out['pairs_under_margin'] = [{'between': [a, b], 'delta_L': d,
                                      'separated_by': 'the hatch on the Stone group and a direct label' if 'Group 4' in (a, b) else 'a direct label'}
                                     for d, a, b in dl if d < 0.10]
    return out


# ------------------------------------------------------------------------------------------------ data
def read_csv(name):
    with open(PUBLIC / name, newline='') as fh:
        return list(csv.DictReader(fh))


def meta(name):
    return json.loads((PUBLIC / name).read_text())


TURNOUT_META = meta('census-cps-2024-turnout-by-state.meta.json')
_turnout_rows = [r for r in read_csv('census-cps-2024-turnout-by-state.csv') if r['year'] == '2024']
TURNOUT = {r['code']: {'name': r['name'], 'pct': float(r['voted_pct']), 'moe': float(r['moe_pct'])}
           for r in _turnout_rows if r['code'] != 'US'}
_US_ROW = next((r for r in _turnout_rows if r['code'] == 'US'), None)   # the engineer's ENG-7 adds it; until then, the sidecar's note
TILE = json.loads(TILES.read_text())
TURNOUT_SOURCE = TURNOUT_META['source_line_variants']['source_line_2024_only']   # the sidecar's own line for 2024
TURNOUT_BREAKS = [58, 62, 66, 70]
_us = re.search(r'National rate, not in the CSV: ([\d.]+)% .*?\(margin ([\d.]+)\)', ' '.join(TURNOUT_META['notes']))
US_TURNOUT, US_TURNOUT_MOE = ((float(_US_ROW['voted_pct']), float(_US_ROW['moe_pct'])) if _US_ROW
                              else (float(_us.group(1)), float(_us.group(2))))
MOE_RANGE = re.search(r'margins of error run from ([\d.]+) to ([\d.]+) points in 2024', TURNOUT_META['qualification']).groups()

JOBS_META = meta('fred-payrolls-by-sector.meta.json')
_jobs = {}
for r in read_csv('fred-payrolls-by-sector.csv'):
    _jobs.setdefault(r['sector'], {})[r['date'][:7]] = float(r['employees_thousands'])
SECTORS = ['Mining and logging', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade',
           'Transportation and warehousing', 'Utilities', 'Information', 'Financial activities',
           'Professional and business services', 'Private educational services', 'Health care and social assistance',
           'Leisure and hospitality', 'Other services', 'Government']
MONTHS = [f'{y}-{m:02d}' for y in range(2022, 2027) for m in range(1, 13) if '2022-01' <= f'{y}-{m:02d}' <= '2026-09']
assert abs(sum(_jobs[s]['2026-09'] for s in SECTORS) - _jobs['Total nonfarm']['2026-09']) < 2, 'sectors must sum to total'
INDEX = {s: [100 * _jobs[s][m] / _jobs[s]['2022-01'] for m in MONTHS] for s in SECTORS}
CHANGE4 = {s: 100 * (_jobs[s]['2026-09'] / _jobs[s]['2022-01'] - 1) for s in SECTORS}
PERIODS = ['2023-09', '2024-09', '2025-09', '2026-09']
PERIOD_WORD = {'2023-09': 'Year to Sep. 2023', '2024-09': 'Year to Sep. 2024', '2025-09': 'Year to Sep. 2025', '2026-09': 'Year to Sep. 2026'}
YOY = {s: {p: 100 * (_jobs[s][p] / _jobs[s][f'{int(p[:4]) - 1}-09'] - 1) for p in PERIODS} for s in SECTORS}
DIV_BREAKS = [-2.0, -0.5, 0.5, 2.0]
# The same printed line S13 carries for these series and this window (the derived file's sidecar)
JOBS_SOURCE = meta('fred-payrolls-by-sector-change.meta.json')['printed_source_line']
assert 'January 2022 to September 2026' in JOBS_SOURCE and 'preliminary' in JOBS_SOURCE
WINDOW_REASON = ('Every jobs chart on this sheet runs from January 2022 to September 2026, the window S13 and S14 use: three '
                 'full years before the January 2025 inauguration and every month since. The 12-month periods end each '
                 'September, so none splits at the inauguration.')
LEAD = max(SECTORS, key=lambda s: CHANGE4[s])
LEAD_TITLE = (f'{LEAD} grew {CHANGE4[LEAD]:.1f} percent from January 2022 to September 2026, a '
              'preliminary figure, the most of 15 sectors.')
FOUR = ['Health care and social assistance', 'Government', 'Manufacturing', 'Information']


def fmt_signed(v, d=1):
    s = f'{abs(v):.{d}f}'
    if round(v, d) == 0:
        return f'{0:.{d}f}'
    return ('+' if v > 0 else MINUS) + s


def div_step(v):
    return 1 + sum(v >= b for b in DIV_BREAKS)


def seq_step(v):
    return 1 + sum(v >= b for b in TURNOUT_BREAKS)


# ------------------------------------------------------------------------------------------------ text helpers
def e(s):
    return html.escape(str(s), quote=True)


_NARROW = set("ijlt.,:;'!|() ")
_WIDE = set('mwMW')


def tw(s, size, weight=400):
    """Approximate advance width of Inter, enough to place labels; the browser draws the type."""
    w = 0.0
    for ch in s:
        if ch in _NARROW:
            w += 0.30
        elif ch in _WIDE:
            w += 0.86
        elif ch.isdigit():
            w += 0.60
        elif ch.isupper():
            w += 0.68
        elif ch in '+−%':
            w += 0.62
        else:
            w += 0.55
    return w * size * (1.05 if weight >= 600 else 1.0)


def f2(x):
    return f'{x:.2f}'.rstrip('0').rstrip('.')


def spread(ys, gap, lo, hi):
    """Push label centers apart by at least gap, keeping their order, inside lo..hi."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    pos = [ys[i] for i in order]
    for _ in range(200):
        moved = False
        for j in range(1, len(pos)):
            if pos[j] - pos[j - 1] < gap:
                mid = (pos[j] + pos[j - 1]) / 2
                pos[j - 1], pos[j] = mid - gap / 2, mid + gap / 2
                moved = True
        if pos[0] < lo:
            shift = lo - pos[0]
            pos = [p + shift for p in pos]
        if pos[-1] > hi:
            shift = pos[-1] - hi
            pos = [p - shift for p in pos]
        if not moved:
            break
    out = [0] * len(ys)
    for j, i in enumerate(order):
        out[i] = pos[j]
    return out


# ------------------------------------------------------------------------------------------------ proposal JSON
def tint_token(name):
    base, toward, amount, job = NEW_TINTS[name]
    h = NEW_TINT_HEX[name]
    return {
        'path': f'oa.color.tint.{name}', 'css': css_name(f'oa.color.tint.{name}'), 'tier': 'primitive', 'type': 'color',
        'value': h, 'derivation': {'method': 'color-mix', 'space': 'oklab', 'base': f'{{oa.color.palette.{base}}}',
                                   'toward': f'{{oa.color.palette.{toward}}}', 'amount': amount,
                                   'css': f'color-mix(in oklab, {P[base]}, {P[toward]} {round(amount * 100)}%)'},
        'surfaces': ['charcoal'], 'kind': 'dataFill', 'job': job, 'need': 'N-10',
        'ratios': {'on Charcoal': cr(h, P['charcoal']), 'Charcoal text on it': cr(P['charcoal'], h),
                   'Newsprint text on it': cr(P['newsprint'], h)},
        'oklab_L': L(h),
        'description': f'{job}. Prussian mixed {round(amount * 100)}% toward Newsprint in OKLab. Proposed until board 1.',
        'reason': ('The diverging scale has no Charcoal steps (its description says "Newsprint only until a Charcoal ramp is '
                   'measured"), and the dark theme (DR-204) sets every role with no Charcoal token to initial. The Verdigris half '
                   'reuses the sequential scale\'s Charcoal steps 3 and 4; no existing value sits at the matching lightness on '
                   'the Prussian side, so these two are the only new colors.'),
    }


def ref_hex(ref):
    return hx(ref[1:-1]) if ref.startswith('{') else ref


def semantic_token(path, ref, job, kind, ground, extra=None, label_ground_ref=None):
    h = ref_hex(ref)
    gh = GROUND_HEX[ground]
    rec = {'path': path, 'css': css_name(path), 'tier': 'semantic', 'type': 'color', 'value': ref, 'resolves_to': h,
           'surface': ground, 'kind': kind, 'job': job}
    if kind == 'text':
        lg = ref_hex(label_ground_ref) if label_ground_ref else gh
        rec['ground'] = label_ground_ref or f'{{oa.color.surface.{ground}}}'
        rec['ratios'] = {'on its ground': cr(h, lg)}
        rec['threshold'] = 4.5
        rec['passes'] = C.contrast(h, lg) >= 4.5
    else:
        rec['ratios'] = {f'on {GROUND_WORD[ground]}': cr(h, gh)}
        rec['threshold'] = 3.0 if kind == 'graphic' else None
        if kind == 'dataFill':
            rec['valuesPrinted'] = True
            rec['threshold_note'] = ('A data fill under 3 to 1 is allowed only with its value printed on or beside it, or a '
                                     'direct label; the 3 to 1 test applies to the marks a reader needs (Rule 05.5)')
    if extra:
        rec.update(extra)
    rec['description'] = job + ' Proposed until board 1.'
    return rec


def build_proposal():
    toks = [tint_token(k) for k in NEW_TINTS]
    # diverging on Charcoal
    for i in range(5):
        fp = f'oa.chart.color.diverging.fill.step{i + 1}.onCharcoal'
        toks.append(semantic_token(fp, DIV_C[i], f'The diverging scale on Charcoal, step {i + 1} of 5: the {DIV_WORDS[i]}.',
                                   'dataFill', 'charcoal', {'scale': 'diverging', 'step': i + 1, 'need': 'N-10',
                                                            'reason': 'Dark mode (DR-204) needs the diverging scale on Charcoal; '
                                                                      'the two ends match in lightness, as on any diverging scale, '
                                                                      'and the boxed arrow or printed sign carries direction (DR-54).'}))
        lp = f'oa.chart.color.diverging.label.step{i + 1}.onCharcoal'
        toks.append(semantic_token(lp, f'{{oa.color.palette.{DIV_LABEL_C[i]}}}', f'Text on diverging step {i + 1} on Charcoal.',
                                   'text', 'charcoal', {'need': 'N-10'}, label_ground_ref='{' + fp + '}'))
    # categorical
    for g in ('newsprint', 'charcoal'):
        for i in range(4):
            fp = f'oa.chart.color.categorical.fill.group{i + 1}.{SURF[g]}'
            extra = {'group': i + 1, 'pattern': CAT_PATTERN[i], 'marker': CAT_MARKER[i], 'need': 'N-11',
                     'never': 'A party, a side or a person (DR-48, DR-58, Rule 01.1); party data takes oa.chart.color.party.mark'}
            if i == 3:
                extra['pattern_spec'] = {'pattern': 'hatch', 'angle_degrees': 45, 'pitch': '{oa.chart.hatch.pitch}',
                                         'weight': '{oa.chart.hatch.weight}', 'edge': '1 px in the same ink',
                                         'why': 'Verdigris and Stone sit 0.05 apart in OKLab lightness (D2-95), so the Stone group always carries the hatch, on both grounds'}
            extra['marker_spec'] = ('On a line, the group\'s marker sits at the line\'s end beside its label, drawn with the '
                                    'area of a circle of oa.chart.dot.openRadius; markers at data points follow the form')
            job = (f'The categorical set, group {i + 1} of 4, on {GROUND_WORD[g]}: {CAT_INK_WORD[g][i]}'
                   f'{", with the hatch" if i == 3 else ""} and a {CAT_MARKER[i]} marker. Every group carries a direct label; '
                   f'past four groups, use small multiples or one group in ink against gray (DR-234).')
            toks.append(semantic_token(fp, CAT[g][i], job, 'graphic', g, extra))
            lp = cat_label_path(i + 1, SURF[g])
            if i == 3:
                toks.append(semantic_token(lp, f'{{oa.color.palette.{CAT_LABEL[g][i]}}}',
                                           f'Label of categorical group 4 on {GROUND_WORD[g]}: set beside the hatch, or on a '
                                           'halo of the ground (oa.chart.halo), never on the hatch itself.',
                                           'text', g, {'need': 'N-11'}))
            else:
                toks.append(semantic_token(lp, f'{{oa.color.palette.{CAT_LABEL[g][i]}}}',
                                           f'Text set on categorical group {i + 1} on {GROUND_WORD[g]}.', 'text', g,
                                           {'need': 'N-11'}, label_ground_ref='{' + fp + '}'))
        toks.append(semantic_token(f'oa.chart.color.ghost.{SURF[g]}', GHOST[g],
                                   f'Ghost: the other groups drawn faint behind each panel of small multiples on {GROUND_WORD[g]}, '
                                   '1 px. They repeat lines drawn in full in their own panels, so they carry no new information '
                                   'and need no 3 to 1 ratio.',
                                   'decorative', g, {'need': 'N-13', 'width': '{oa.chart.line.hairline}'}))
    # grade line code (D3-84): every value read from the atlas build, or set here where the build defines none
    src_ref = f'{ALC["source"]}, pattern() line {ALC["pattern_line"]}, wire_marks() line {ALC["wire_marks_line"]}'
    for key, v7, word, gloss, tex, pat, cap in GRADES:
        path = f'oa.chart.grade.{key}'
        if key == 'conceptual':
            toks.append({'path': f'{path}.rail', 'css': css_name(f'{path}.rail'), 'tier': 'semantic', 'type': 'dimension',
                         'value': f'{ALC["hollow_rail_px"]:g}px', 'need': 'N-12', 'source': src_ref,
                         'job': 'Each of the two rails of a hollow line, at every line width.',
                         'description': ('Rail of the hollow line for a conceptual step (Gate 1, M1): 1 px at every line '
                                         'width, centered half a width plus 0.5 px either side of the line. Proposed until board 1.')})
            toks.append({'path': f'{path}.gap', 'css': css_name(f'{path}.gap'), 'tier': 'semantic', 'type': 'number',
                         'value': 1, 'unit': 'line widths', 'need': 'N-12', 'source': src_ref,
                         'job': 'The ground between the two rails: one line width, so the hollow line is two widths plus 2 px across.',
                         'at_widths': {f'{w} px': f'{w} px of ground, {w + 2} px across' for w in LINE_WIDTHS},
                         'description': 'Ground between the rails of a hollow line, in line widths. Proposed until board 1.'})
            continue
        value = 'solid' if pat is None else {'dashArray': [f'{f2(x)}px' for x in pat], 'lineCap': cap}
        rec = {'path': path, 'css': css_name(path), 'tier': 'semantic', 'type': 'strokeStyle', 'value': value,
               'per_line_width': pat is not None, 'v7_value': v7, 'word': word, 'gloss': gloss, 'texture': tex,
               'need': 'N-12', 'source': src_ref,
               'at_widths': {f'{w} px': ('none' if pat is None else ' '.join(f2(x * w) for x in pat)) for w in LINE_WIDTHS},
               'job': f'{word} ({gloss}): {tex}' + ('' if pat is None else f', {" ".join(f2(x) for x in pat)} line widths, {cap} caps') + '.',
               'description': (f'Evidence grade {word}, {gloss}: drawn {tex}' +
                               ('' if pat is None else f'; the dash array is per 1 px of line width, so multiply by the width '
                                                       f'(2, 3 or 6 px) and stretch it to start and end on ink') +
                               '. Proposed until board 1.')}
        if key in V7_RENDERER:
            rec['v7_renderer_dasharray'] = V7_RENDERER[key]
        if key == 'documented':
            rec['record_square'] = '{oa.chart.grade.recordSquare}'
        toks.append(rec)
    toks.append({'path': 'oa.chart.grade.headClearance', 'css': css_name('oa.chart.grade.headClearance'), 'tier': 'semantic',
                 'type': 'number', 'value': ALC['dotted_head_clearance_widths'], 'unit': 'line widths', 'need': 'N-12',
                 'source': src_ref,
                 'job': 'A dotted line stops 1.5 line widths short of its arrowhead, so its last dot stays clear of the head.',
                 'description': 'Gap between a dotted line\'s last dot and its arrowhead, in line widths. Proposed until board 1.'})
    toks.append({'path': 'oa.chart.grade.recordSquare', 'css': css_name('oa.chart.grade.recordSquare'), 'tier': 'semantic',
                 'type': 'dimension', 'value': f'{RECORD_SQUARE}px', 'need': 'N-12',
                 'source': 'set by the data lead: the atlas build draws no record square (D3-84 log)',
                 'job': 'The filled square set before the word Documented in labels and keys (Gate 1, M1).',
                 'description': 'Record square before the word Documented, 7 px, in the label\'s ink, set inline before the word only. Proposed until board 1.'})
    toks.append({'path': 'oa.chart.grade.minRun', 'css': css_name('oa.chart.grade.minRun'), 'tier': 'semantic',
                 'type': 'number', 'value': MIN_RUN, 'unit': 'line widths', 'need': 'N-12',
                 'source': 'set by the data lead: the atlas build defines no shortest line (D3-84 log)',
                 'at_widths': {f'{w} px': f'{MIN_RUN * w} px' for w in LINE_WIDTHS},
                 'job': (f'The shortest run that may carry a texture, key samples included: {MIN_RUN} line widths, '
                         f'{MIN_RUN * 2} px on a 2 px line, which holds two full dash-dot periods and the closing dash. '
                         'A shorter step prints its grade in words beside it.'),
                 'description': 'Shortest textured run, key samples included, in line widths. Proposed until board 1.'})

    new_colors = [t for t in toks if t['tier'] == 'primitive']
    descr = [
        {'path': 'oa.chart.color.diverging', 'field': '$description',
         'now': node('oa.chart.color.diverging')['$description'],
         'proposed': ('The diverging scale, Prussian through a midpoint tinted toward the ground to Verdigris, on Newsprint and '
                      'Charcoal. Neither end keeps its order in grayscale, so a boxed arrow or a printed sign carries direction.')},
        {'path': 'oa.chart.hatch.pitch', 'field': '$description', 'now': node('oa.chart.hatch.pitch')['$description'],
         'proposed': 'Spacing of the hatch, the pattern a key names: contested evidence in a grade chart, or the Stone group of the categorical set.'},
        {'path': 'oa.chart.hatch.weight', 'field': '$description', 'now': node('oa.chart.hatch.weight')['$description'],
         'proposed': 'Stroke of the hatch, in the ink of the mark it fills.'},
        {'path': 'oa.chart.color.point', 'field': '$description', 'now': node('oa.chart.color.point.onNewsprint')['$description'],
         'proposed': (node('oa.chart.color.point.onNewsprint')['$description'] + ' When an error or an ask holds the view\'s red, '
                      'the point yields to the subject ink and keeps its label and its place (Rule 11.16).')},
        {'path': 'oa.chart.color.context', 'field': '$description', 'now': node('oa.chart.color.context.onNewsprint')['$description'],
         'proposed': (node('oa.chart.color.context.onNewsprint')['$description'] + ' Past four groups, every group but the one '
                      'the title names takes this ink, each with its label (DR-234).')},
    ] + [{'path': p, 'field': 'job and surfaces', 'now': node(p)['$extensions']['org.oathandaction']['job'], 'proposed': j,
          'surfaces_now': node(p)['$extensions']['org.oathandaction']['surfaces'],
          'surfaces_proposed': sorted(set(node(p)['$extensions']['org.oathandaction']['surfaces']) | {'newsprint' if 'Newsprint' in j.split(', and')[-1] else 'charcoal'}),
          'contrast_proposed': {s: cr(node(p)['$value']['hex'], P[s]) for s in sorted(set(node(p)['$extensions']['org.oathandaction']['surfaces']) | {'newsprint' if 'Newsprint' in j.split(', and')[-1] else 'charcoal'})}}
         for p, j in WIDENED.items()]
    needs = {
        'N-10': ('Diverging pair B on Charcoal for the dark theme (DR-204): the scale has Newsprint tokens only, and the dark '
                 'theme sets it to initial. Measured on this sheet'),
        'N-11': ('A categorical set of up to four groups (DR-234): no token names the four brand inks as groups, with a '
                 'label ink for each and the hatch that keeps Verdigris and Stone apart (D2-95)'),
        'N-12': ('The evidence line code (Gate 1, M1; Rule 10.10) as tokens, so the chart kit, chapter 13 and chapter 15 draw '
                 'one set of patterns: today the patterns live in three build scripts'),
        'N-13': ('Small multiples past four groups (DR-234) draw the other groups faint behind each panel; no token names that role'),
    }
    return {
        'title': 'Palette proposal: the chart tokens for Phase 3, round 0',
        'date': '2026-11-11',
        'author': 'Data visualization and systems lead, with the design director\'s eye',
        'status': ('Proposed. Every token here is marked "Proposed until board 1" in its description; Dustin approves the new '
                   'colors on board 1. The engineer adds them as one pre-release under Rule 26.8.'),
        'built_from': {'tokens': f'work/build/tokens/tokens.json, release {RELEASE}',
                       'script': 'work/boards/phase-3/round-0/palettes/build_palette_proofs.py',
                       'proofs': 'work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs.html',
                       'measures': 'work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs-Measures.json'},
        'release_suggestion': {
            'version': '6.0.0-gate3.1',
            'why': ('Rule 26.8: before 6.0.0, every change raises the number after the hyphen. The Gate 2 drafts ran gate2.1 '
                    'to gate2.9; this is the first draft on the way to Gate 3. The engineer names the release'),
            'change_note': {
                'tokens': ('oa.color.tint.prussianN56 and prussianN29 (new); oa.chart.color.diverging on Charcoal; '
                           'oa.chart.color.categorical; oa.chart.color.ghost; oa.chart.grade; the descriptions listed under '
                           'description_changes'),
                'change': ('Two new colors, both Prussian mixed toward Newsprint, so the diverging scale works on Charcoal. '
                           'New roles with no new value: the four-ink categorical set with its label inks, the ghost lines of '
                           'small multiples, and the evidence line code as stroke styles. Every new token is marked proposed '
                           'until board 1.'),
                'reason': ('Dark mode needs the diverging scale on Charcoal (DR-204); the categorical set stays with the four '
                           'brand inks and no new hue (DR-234); the line code moves out of three build scripts into the tokens '
                           '(Gate 1, M1; Rule 10.10).'),
                'record': 'DR-204, DR-234, D2-95, Gate 1 M1, Rule 10.10; the palette notes\' D3 calls', 'gate': 'Board 1, then Gate 3'},
        },
        'summary': {
            'new_colors': len(new_colors),
            'new_color_tokens': [t['path'] for t in new_colors],
            'new_tokens_total': len(toks),
            'by_group': {
                'oa.color.tint (new primitives)': len(new_colors),
                'oa.chart.color.diverging, on Charcoal': sum(t['path'].startswith('oa.chart.color.diverging') for t in toks),
                'oa.chart.color.categorical': sum(t['path'].startswith('oa.chart.color.categorical') for t in toks),
                'oa.chart.color.ghost': sum(t['path'].startswith('oa.chart.color.ghost') for t in toks),
                'oa.chart.grade': sum(t['path'].startswith('oa.chart.grade') for t in toks),
            },
            'existing_values_reused': sorted(set(t['value'] for t in toks if isinstance(t.get('value'), str)
                                                 and t['value'].startswith('{oa.color')
                                                 and t['value'][1:-1] not in {n['path'] for n in new_colors})),
            'not_added': [
                'A Prussian sequential scale: no chart in S01 to S16 or in rounds 1 and 2\'s plan as read today needs a second measure in sequence (proposal section 1.6 adds it only on need)',
                'Chart tokens on White: a printed report prints the Newsprint values on the paper (DR-53); this sheet measures them on White and they hold',
                'Chart tokens on Prussian: Prussian is a data ink in two palettes, and red never sits on it (Rule 05.3); a chart in a Prussian panel sits on its own Newsprint or Charcoal plate',
                'A new red or a red tint: the red-on-red specimen resolves by Rule 05.3\'s order, with the point yielding to ink (Rule 11.16)',
            ],
        },
        'needs': needs,
        'line_code_source': {
            'decision': 'D3-84: the atlas build\'s own constants are the one source of the line code; Rule 10.10\'s builders line names them, the tokens take them, and Rule 13.4 states the same numbers and cites the tokens',
            'read_by_script_from': ALC['source'],
            'read': {
                'patterns_per_line_width': {g[2]: g[5] for g in GRADES if g[0] != 'conceptual'},
                'caps': {g[2]: g[6] for g in GRADES if g[0] != 'conceptual'},
                'pattern_function_line': ALC['pattern_line'],
                'fitting': ALC['fitting'] + f' (fitted(), line {ALC["fitted_line"]})',
                'line_widths_px': ALC['line_widths'], 'line_widths_from': ALC['line_widths_from'],
                'hollow_line': (f'two rails of {ALC["hollow_rail_px"]:g} px at {ALC["hollow_rail_offset"]} either side of the '
                                f'line, at every width, so the ground between them is {ALC["hollow_inner_gap"]} '
                                f'(wire_marks(), line {ALC["wire_marks_line"]})'),
                'dotted_head_clearance_line_widths': ALC['dotted_head_clearance_widths'],
                'grade_words_and_build_glosses': {k: list(v[:2]) for k, v in ALC['grades'].items()},
                'key_glyph_lengths_px_on_a_2px_line': ALC['key_glyph_px_at_2px'],
            },
            'set_here_because_the_build_defines_none': [
                {'value': f'oa.chart.grade.minRun = {MIN_RUN} line widths',
                 'why': (f'The build has no shortest-line constant. Its keys draw 32 and 36 px samples on a 2 px line (16 and 18 '
                         f'widths), which squeeze a dash-dot sample by up to a fifth to fit it. {MIN_RUN} widths holds two full '
                         'dash-dot periods (8 widths each) and the closing dash at every width, which is what Rule 13.4\'s "long '
                         'enough to show its pattern twice" asks: 40 px at 2 px, 60 px at 3 px, 120 px at 6 px. It replaces '
                         'both the 28 widths of the Phase 2 frame memo, which the build never coded, and Rule 13.4\'s 48 px')},
                {'value': f'oa.chart.grade.recordSquare = {RECORD_SQUARE} px',
                 'why': ('The build draws no record square. Gate 1 M1 added it; the Phase 2 atlas design frame memo and Rule 13.4 '
                         'both set 7 px, so the value stays, set inline before the word Documented only')},
                {'value': 'Hypothesis gloss "not yet tested"',
                 'why': ('The build\'s shared table glosses Hypothesis "untested"; D3-84 names Rule 13.3\'s table, which prints '
                         '"not yet tested" as Rule 12.6\'s key does, so the tokens and the sheet take it. The Phase 2 build stays as a record')},
            ],
            'changed_from_the_first_proposal': [
                'oa.chart.grade.conceptual.railSelected (2 px on the 6 px route) is withdrawn: the build draws 1 px rails at every width',
                f'oa.chart.grade.minRun goes from 28 to {MIN_RUN} line widths',
                'oa.chart.grade.headClearance is new: 1.5 line widths, read from wire_marks()',
                'The hypothesis gloss reads "not yet tested"',
                'The source of every grade token is the atlas build, in place of "Atlas V7 renderer"',
            ],
        },
        'tokens': toks,
        'description_changes': descr,
        'kit_roles': {
            'note': 'The engineer\'s kit roles (Contracts, C4) that map to these tokens in kit.css',
            'div-1 to div-5': 'oa.chart.color.diverging.fill.stepN, now on both grounds',
            'cat-1 to cat-4': 'oa.chart.color.categorical.fill.groupN; cat-4 also takes the hatch',
            'ghost': 'oa.chart.color.ghost (a new role the kit needs for small multiples)',
            'grade-documented to grade-conceptual': 'oa.chart.grade.*, for chapter 13 and 15 diagrams and any chart that draws a connection',
        },
        'rules_with_the_palettes': [
            'Sequential: five Verdigris steps per ground, light to strong on Newsprint and dark to light on Charcoal, so the most always reads strongest. Print the value on or beside every step 1 to 3 fill.',
            'Diverging: pair B only, Prussian for one side and Verdigris for the other, with a boxed arrow or a printed sign in every cell. Say in the key which side is which. Never red with blue.',
            'Categorical: at most four groups, in the order Charcoal (Newsprint on Charcoal), Verdigris, Prussian, Stone, so neither close pair ever touches in a stack. The Stone group always carries the hatch; every group carries a direct label on the chart and, on a line, its end marker. Never for parties.',
            'Past four groups: small multiples with the other groups as ghosts, or one group in ink and every other in the context gray, every group labeled (DR-234).',
            'Magnitude: gray Stone steps with no direction; the figure prints in every tile.',
            f'Grade line code: the line\'s width sets its pattern; no coded line drops under 2 px; a run under {MIN_RUN} widths, key samples included, prints its grade in words.',
            'Red: one working red per view (Rule 05.3). A chart\'s red point yields to the subject ink when an error or an ask is in the view, and keeps its label and place.',
        ],
    }


PROPOSAL_DATA = build_proposal()


# ------------------------------------------------------------------------------------------------ CSS
def token_css():
    """The color and chart tokens from tokens.css's first :root block, then the proposed ones."""
    src = TOKENS_CSS.read_text()
    root = src[src.index(':root {'):]
    root = root[:root.index('\n}')]
    keep = [ln.strip() for ln in root.splitlines()
            if re.match(r'\s*--oa-(color|chart)-', ln) and 'deprecated' not in ln]
    prop = []
    for name, h in NEW_TINT_HEX.items():
        prop.append(f'{css_name("oa.color.tint." + name)}: {h};')
    for path, v in PROPOSED.items():
        if path.startswith('oa.color.tint.'):
            continue
        prop.append(f'{css_name(path)}: var({css_name(v[1:-1])});')
    return (f'/* tokens.css {RELEASE}: color and chart tokens */\n:root{{{"".join(keep)}}}\n'
            '/* Proposed in work/handoffs/phase-3/20261111_Palette-Proposal.json, not yet in tokens.css */\n'
            f':root{{{"".join(prop)}}}')


def ground_vars():
    out = []
    for g in ('newsprint', 'white', 'charcoal', 'prussian'):
        tg = TOKEN_GROUND.get(g, g)
        v = {'--gr': f'var(--oa-color-palette-{g})',
             '--ink': f'var(--oa-color-text-primary-on-{g})',
             '--sec': f'var(--oa-color-text-secondary-on-{g})',
             '--rule': f'var(--oa-color-border-hairline-on-{g})',
             '--strong': f'var(--oa-color-border-strong-on-{g})'}
        if g in ('newsprint', 'white', 'charcoal'):
            c = f'on-{tg}'
            v.update({'--sub': f'var(--oa-chart-color-subject-{c})', '--ctx': f'var(--oa-chart-color-context-{c})',
                      '--lab': f'var(--oa-chart-color-label-{c})', '--csec': f'var(--oa-chart-color-secondary-{c})',
                      '--base': f'var(--oa-chart-color-baseline-{c})', '--grid': f'var(--oa-chart-color-gridline-{c})',
                      '--point': f'var(--oa-chart-color-point-{c})', '--ghost': f'var(--oa-chart-color-ghost-{c})',
                      '--land': f'var(--oa-chart-color-land-{c})', '--track': f'var(--oa-chart-color-track-{c})'})
            if tg == 'newsprint':
                v['--keyline'] = 'var(--oa-chart-color-point-keyline-on-newsprint)'
            v['--lfill'] = f'var(--oa-chart-color-light-fill-{c})'
            for i in range(1, 6):
                v[f'--seq{i}'] = f'var(--oa-chart-color-sequential-fill-step{i}-{c})'
                v[f'--seql{i}'] = f'var(--oa-chart-color-sequential-label-step{i}-{c})'
                v[f'--div{i}'] = f'var(--oa-chart-color-diverging-fill-step{i}-{c})'
                v[f'--divl{i}'] = f'var(--oa-chart-color-diverging-label-step{i}-{c})'
            for i in range(1, 5):
                v[f'--mag{i}'] = f'var(--oa-chart-color-magnitude-fill-step{i}-{c})'
                v[f'--magl{i}'] = f'var(--oa-chart-color-magnitude-label-step{i}-{c})'
                v[f'--cat{i}'] = f'var(--oa-chart-color-categorical-fill-group{i}-{c})'
                v[f'--catl{i}'] = f'var({css_name(cat_label_path(i, SURF[tg]))})'
        out.append(f'.g-{g}{{{";".join(f"{k}:{val}" for k, val in v.items())};background:var(--gr);color:var(--ink)}}')
    return '\n'.join(out)


PAGE_CSS = r'''
html{-webkit-text-size-adjust:100%;background:var(--oa-color-palette-newsprint)}
body{margin:0;background:var(--oa-color-palette-newsprint);color:var(--oa-color-palette-charcoal);font:400 17px/27px Inter,system-ui,sans-serif}
*,*::before,*::after{box-sizing:border-box}
html[data-sim="grayscale"] body{filter:grayscale(1)}
html[data-sim="protanopia"] body{filter:url(#f-protanopia)}
html[data-sim="deuteranopia"] body{filter:url(#f-deuteranopia)}
html[data-sim="tritanopia"] body{filter:url(#f-tritanopia)}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
:focus-visible{outline:3px solid var(--oa-color-palette-charcoal);outline-offset:2px}
.wrap{max-width:1440px;margin:0 auto;padding:0 64px}
.mast{border-bottom:1px solid var(--oa-color-palette-stone)}
.mrow{display:flex;align-items:center;gap:48px;min-height:72px}
.wm{display:inline-flex;color:var(--oa-color-palette-charcoal)}
.run{margin:0;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone)}
.top{padding:40px 0 32px;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:24px 64px;align-items:end;border-bottom:2px solid var(--oa-color-palette-charcoal)}
.eyebrow{margin:0 0 8px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
.display{margin:0;font:800 56px/60px "Inter Tight",Inter,sans-serif;letter-spacing:-.035em;margin-left:-.04em}
.deck p{margin:16px 0 0;font:400 19px/28px Inter,sans-serif;max-width:40em;text-wrap:pretty}
.deck p+p{font-size:17px;line-height:27px;color:var(--oa-color-derived-deep-stone)}
.facts{margin:0;padding:0;list-style:none;border-top:1px solid var(--oa-color-palette-charcoal)}
.facts li{display:grid;grid-template-columns:64px 1fr;gap:12px;padding:10px 0;border-bottom:1px solid var(--oa-chart-color-gridline-on-newsprint);font:400 15px/22px Inter,sans-serif}
.facts b{font:800 28px/28px "Inter Tight",sans-serif;font-variant-numeric:tabular-nums}
.tools{display:flex;flex-wrap:wrap;gap:12px 40px;align-items:center;padding:20px 0;border-bottom:1px solid var(--oa-chart-color-gridline-on-newsprint)}
.tools fieldset{display:flex;flex-wrap:wrap;gap:4px 18px;border:0;margin:0;padding:0;align-items:center}
.tools legend{float:left;margin-right:14px;font:600 15px/44px Inter,sans-serif}
.tools label{display:inline-flex;align-items:center;gap:6px;min-height:44px;font:400 15px/20px Inter,sans-serif;cursor:pointer}
.tools input{width:18px;height:18px;margin:0;accent-color:var(--oa-color-palette-charcoal)}
.toc{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:0 24px}
.toc a{display:inline-flex;min-height:44px;align-items:center;font:600 15px/20px Inter,sans-serif}
.sec{padding:56px 0 72px;border-top:2px solid var(--oa-color-palette-charcoal)}
.sec:first-of-type{border-top:0}
.sh{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:12px 64px;align-items:start;margin-bottom:28px}
.sh h2{margin:0;font:800 40px/44px "Inter Tight",Inter,sans-serif;letter-spacing:-.03em;text-wrap:balance}
.lede{margin:12px 0 0;font:400 17px/27px Inter,sans-serif;max-width:44em;text-wrap:pretty}
.side{margin:0;font:400 15px/23px Inter,sans-serif;color:var(--oa-color-derived-deep-stone)}
.side p{margin:0 0 10px}
.tag{display:inline-block;padding:3px 7px;font:700 13px/16px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;border:1.5px solid currentColor;vertical-align:2px}
.tag.new{background:var(--oa-color-palette-charcoal);border-color:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint)}
.g-charcoal .tag.new{background:var(--oa-color-palette-newsprint);border-color:var(--oa-color-palette-newsprint);color:var(--oa-color-palette-charcoal)}
.plate{padding:24px 24px 20px;border:1px solid var(--rule);margin-top:20px}
.g-newsprint.plate{border-color:var(--oa-color-palette-stone)}
.ph{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 16px;margin-bottom:16px}
.ph h3{margin:0;font:800 22px/26px "Inter Tight",sans-serif;letter-spacing:-.02em}
.ph p{margin:0;font:400 15px/22px Inter,sans-serif;color:var(--sec)}
.scroll{overflow-x:auto;position:relative}
table caption.vh,.lc caption.vh{left:0;top:0}
.rg{display:grid;grid-template-columns:112px repeat(var(--n),152px) minmax(150px,1fr);gap:8px 10px;align-items:start;min-width:max-content}
.rh{font:600 13px/18px Inter,sans-serif;color:var(--ink);padding-top:2px}
.nm{display:flex;gap:6px;align-items:center;justify-content:space-between;font:700 13px/18px Inter,sans-serif;margin-bottom:6px}
.nm .tag{padding:1px 5px;font-size:13px;line-height:15px;border-width:1px}
.chip{height:72px;display:flex;align-items:flex-end;padding:8px 10px;font:600 15px/1 Inter,sans-serif;font-variant-numeric:tabular-nums}
.chip.hatch{box-shadow:inset 0 0 0 1px var(--hc)}
.halo{background:var(--gr);color:var(--ink);padding:2px 4px;margin-left:-4px}
.mk{margin-left:auto;align-self:flex-start}
.dl{margin:8px 0 0;font:400 13px/18px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.dl div{display:flex;justify-content:space-between;gap:6px;border-bottom:1px solid var(--rule);padding:2px 0}
.dl dt{margin:0}.dl dd{margin:0;color:var(--ink);font-weight:600}
.dl .src{display:block;border:0;padding-top:4px}
.sim{height:22px}
.simv{font:400 13px/22px Inter,sans-serif;color:var(--sec);font-variant-numeric:tabular-nums}
.simv b{color:var(--ink);font-weight:600}
.bo{height:22px;display:flex;align-items:center;padding-left:6px;font:600 13px/1 Inter,sans-serif}
.pn{margin:16px 0 0;font:400 15px/23px Inter,sans-serif;color:var(--sec);max-width:62em;text-wrap:pretty}
.pn b{color:var(--ink);font-weight:600}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.two>.plate{margin-top:20px}
figure{margin:0}
.fh{margin:0 0 4px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--sec)}
.ft{margin:0;font:800 24px/28px "Inter Tight",sans-serif;letter-spacing:-.02em;max-width:30em;text-wrap:balance}
.fm{margin:6px 0 14px;font:400 15px/23px Inter,sans-serif;color:var(--sec);max-width:44em;text-wrap:pretty}
.fs{margin:12px 0 0;font:400 13px/19px Inter,sans-serif;color:var(--sec);max-width:56em}
.fn{margin:10px 0 0;font:400 14px/21px Inter,sans-serif;color:var(--sec);max-width:56em}
svg text{font-family:Inter,system-ui,sans-serif;font-variant-numeric:tabular-nums}
svg .t13{font-size:13px}svg .t14{font-size:14px}svg .t15{font-size:15px}
svg .b{font-weight:600}svg .bb{font-weight:700}
.key{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 12px;padding:0;list-style:none;font:400 14px/20px Inter,sans-serif}
.key li{display:flex;align-items:center;gap:8px}
.key .sw{width:28px;height:18px;flex:none}
details.mt{margin-top:24px;border-top:1px solid var(--oa-color-palette-charcoal)}
details.mt>summary{display:flex;align-items:center;min-height:44px;font:600 15px/20px Inter,sans-serif;cursor:pointer;list-style:none}
details.mt>summary::-webkit-details-marker{display:none}
details.mt>summary::before{content:"+";display:inline-block;width:18px;font:700 18px/1 Inter,sans-serif}
details.mt[open]>summary::before{content:"\2212"}
table.m{border-collapse:collapse;font:400 13px/18px Inter,sans-serif;font-variant-numeric:tabular-nums;min-width:100%}
table.m th,table.m td{text-align:left;padding:6px 10px 6px 0;border-bottom:1px solid var(--oa-chart-color-gridline-on-newsprint);vertical-align:top;white-space:nowrap}
table.m thead th{border-bottom:1.5px solid var(--oa-color-palette-charcoal);font-weight:600}
table.m td.n{text-align:right}
.sq{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin-right:6px;box-shadow:inset 0 0 0 1px rgba(18,18,18,.25)}
.lc{border-collapse:collapse;font:400 14px/20px Inter,sans-serif}
.lc th,.lc td{padding:10px 18px 10px 0;border-bottom:1px solid var(--oa-chart-color-gridline-on-newsprint);vertical-align:middle;text-align:left}
.lc thead th{font:600 13px/18px Inter,sans-serif;border-bottom:1.5px solid var(--oa-color-palette-charcoal)}
.lc td.cell{padding:8px 10px}
.lc th[scope="row"]{font-weight:400}.lc .gw{display:block;font-weight:600}.lc .gg{display:block;color:var(--oa-color-derived-deep-stone);font-size:13px;line-height:18px}
.views{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:20px}
.view{border:1px solid var(--oa-color-palette-stone);padding:0}
.vlab{margin:0;padding:10px 16px;font:700 13px/18px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid var(--oa-color-palette-stone);background:var(--oa-color-palette-newsprint);color:var(--oa-color-palette-charcoal)}
.vlab.fail{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint)}
.vbody{padding:20px 20px 22px}
.cap{margin:0;padding:12px 16px 14px;font:400 15px/23px Inter,sans-serif;border-top:1px solid var(--oa-color-palette-stone);background:var(--oa-color-palette-newsprint);color:var(--oa-color-palette-charcoal)}
.cap b{font-weight:700}
.form{margin-top:18px;padding-top:16px;border-top:1px solid var(--rule)}
.form .fl{display:block;font:600 15px/22px Inter,sans-serif;margin-bottom:6px}
.field{position:relative;display:flex;align-items:center;height:44px;padding:0 12px;font:400 17px/1 Inter,sans-serif;border:1px solid var(--strong)}
.g-newsprint .field{background:var(--oa-color-field-ground-on-newsprint)}
.g-charcoal .field{background:var(--oa-color-field-ground-on-charcoal)}
.field.err::before{content:"";position:absolute;left:-1px;top:-1px;bottom:-1px;width:4px;background:var(--oa-color-state-error-bar-on-newsprint)}
.msg{display:flex;gap:10px;align-items:flex-start;margin-top:8px;padding:8px 12px 8px 16px;position:relative;font:400 15px/22px Inter,sans-serif}
.g-newsprint .msg{background:var(--oa-color-state-error-band-on-newsprint)}
.msg::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--oa-color-state-error-bar-on-newsprint)}
.msg svg{flex:none;margin-top:2px}
.ask{display:inline-flex;align-items:center;min-height:48px;margin-top:14px;padding:0 20px;font:700 19px/1 Inter,sans-serif;border:0}
.ask.red{background:var(--oa-color-action-ask-fill-on-newsprint);color:var(--oa-color-action-ask-label-on-newsprint);box-shadow:inset 0 0 0 1px var(--oa-color-palette-charcoal)}
.g-charcoal .ask.red{box-shadow:none}
.ask.ink{background:var(--oa-color-action-primary-fill-on-newsprint);color:var(--oa-color-action-primary-label-on-newsprint)}
.g-charcoal .ask.ink{background:var(--oa-color-action-primary-fill-on-charcoal);color:var(--oa-color-action-primary-label-on-charcoal)}
.ex{margin:4px 0 0;font:400 13px/18px Inter,sans-serif;color:var(--sec)}
.phn{display:none}
.fh .ek{display:inline-block;margin-right:8px;padding:2px 7px;background:var(--ink);color:var(--gr);letter-spacing:.06em}
.fh .gl{text-transform:none;letter-spacing:0;font-weight:600;font-size:14px;color:var(--sec)}
.foot{padding:32px 0 64px;border-top:2px solid var(--oa-color-palette-charcoal);font:400 14px/21px Inter,sans-serif;color:var(--oa-color-derived-deep-stone)}
.foot p{margin:0 0 8px;max-width:72em}
@media (max-width:1100px){.top,.sh{grid-template-columns:minmax(0,1fr)}.two,.views{grid-template-columns:minmax(0,1fr)}}
.view,.vbody,.plate,figure{min-width:0}
@media (max-width:767.98px){.dsk{display:none}.phn{display:block}.wrap{padding:0 16px}.display{font-size:40px;line-height:44px}.sh h2{font-size:30px;line-height:34px}.mrow{gap:4px 20px;flex-wrap:wrap;padding:10px 16px}.plate{padding:16px 12px}.vbody{padding:16px 12px}}
'''

SIM_FILTERS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>' + ''.join(
    f'<filter id="f-{k}" color-interpolation-filters="linearRGB"><feColorMatrix type="matrix" values="'
    + ' '.join(f'{m[i][0]} {m[i][1]} {m[i][2]} 0 0' for i in range(3)) + ' 0 0 0 1 0"/></filter>'
    for k, m in CVD.items()) + '</defs></svg>')


# ------------------------------------------------------------------------------------------------ swatch plates
def mix_words(path):
    """Plain words for where a token's value comes from."""
    n = node(path) if path not in PROPOSED else None
    ref = PROPOSED.get(path) if n is None else n['$value']
    while isinstance(ref, str) and ref.startswith('{'):
        p = ref[1:-1]
        if p in PROPOSED and p.startswith('oa.color.tint.'):
            b, t, a, _ = NEW_TINTS[p.split('.')[-1]]
            return f'{b.capitalize()} {round(a * 100)}% toward {t.capitalize()}'
        if p.startswith('oa.color.palette.'):
            nm = node(p)['$description'].split(',')[0]
            return nm
        if p.startswith('oa.color.tint.') or p.startswith('oa.color.derived.'):
            d = node(p)['$extensions']['org.oathandaction']['derivation']
            pct = round(d['amount'] * 100, 2)
            pct = int(pct) if pct == int(pct) else pct
            return f'{d["base"].split(".")[-1][:-1].replace("pillarRed", "Pillar Red").capitalize()} {pct}% toward {d["toward"].split(".")[-1][:-1].capitalize()}'
        ref = PROPOSED[p] if p in PROPOSED else node(p)['$value']
    return ''


def marker_svg(kind, color, size=12):
    s = size
    c = s / 2
    if kind == 'circle':
        sh = f'<circle cx="{c}" cy="{c}" r="{f2(s * 0.42)}"/>'
    elif kind == 'square':
        a = s * 0.74
        sh = f'<rect x="{f2(c - a / 2)}" y="{f2(c - a / 2)}" width="{f2(a)}" height="{f2(a)}"/>'
    elif kind == 'triangle':
        sh = f'<path d="M{f2(c)} {f2(s * 0.06)}L{f2(s * 0.97)} {f2(s * 0.9)}H{f2(s * 0.03)}Z"/>'
    else:
        sh = f'<path d="M{f2(c)} 0L{s} {f2(c)}L{f2(c)} {s}L0 {f2(c)}Z"/>'
    return f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" aria-hidden="true" focusable="false" style="fill:{color};flex:none">{sh}</svg>'


def hatch_bg(color, ground):
    return f'repeating-linear-gradient(45deg,{color} 0 1.5px,{ground} 1.5px 5px)'


def ramp_plate(pid, ground, m):
    pal = PALETTES[pid]
    n = len(m['rows'])
    cat = pid == 'categorical'
    cells = ['<div class="rh">Fill, with its label ink</div>']
    for i, r in enumerate(m['rows']):
        tag = '<span class="tag new">Proposed</span>' if 'proposed' in (r['fill_status'], r['label_status']) else ''
        hatch = cat and i == 3
        fill_var, label_var = f'var({r["fill_css"]})', f'var({r["label_css"]})'
        if hatch:
            sw = (f'<div class="chip hatch" style="background:{hatch_bg(fill_var, "var(--gr)")};--hc:{fill_var}">'
                  f'<span class="halo" style="color:var({r["label_css"]})">{e(pal["sample"][i])}</span>'
                  f'<span class="mk halo" style="padding:3px;line-height:0">{marker_svg(CAT_MARKER[i], fill_var)}</span></div>')
        else:
            mk = f'<span class="mk">{marker_svg(CAT_MARKER[i], label_var)}</span>' if cat else ''
            sw = (f'<div class="chip" style="background:var({r["fill_css"]});color:var({r["label_css"]})" '
                  f'data-probe="fill" data-hex="{r["fill_hex"]}" data-ground="{ground}">{e(pal["sample"][i])}{mk}</div>')
        lab_note = 'Label on halo' if hatch else 'Label on fill'
        cells.append(f'<div><div class="nm"><span>{e(r["name"])}</span>{tag}</div>{sw}'
                     f'<dl class="dl"><div><dt>Fill on {GROUND_WORD[ground]}</dt><dd>{r["fill_on_ground"]:.2f}</dd></div>'
                     f'<div><dt>{lab_note}</dt><dd>{r["label_on_fill"]:.2f}</dd></div>'
                     f'<div><dt>Lightness</dt><dd>{r["oklab_L"]:.3f}</dd></div>'
                     f'<div class="src"><dt class="vh">Value</dt><dd style="font-weight:400;color:var(--sec)">{r["fill_hex"]}, {e(mix_words(r["fill_token"]))}</dd></div></dl></div>')
    cells.append('<div></div>')
    sims = []
    for k in SIMS:
        sims.append(f'<div class="rh" style="padding-top:2px">{SIM_WORD[k]}</div>')
        for i, r in enumerate(m['rows']):
            h = r['luminance_gray'] if k == 'grayscale' else r[f'sim_{k}']
            if cat and i == 3:
                sims.append(f'<div class="sim" style="background:{hatch_bg(h, simulate(GROUND_HEX[ground], k))};box-shadow:inset 0 0 0 1px {h}"></div>')
            else:
                sims.append(f'<div class="sim" style="background:{h}" data-probe="sim-{k}" data-hex="{h}"></div>')
        if k == 'grayscale':
            gap = m['smallest_lightness_gap']
            if cat:
                rest = min(p['delta_L'] for p in m['lightness_gaps'] if set(p['between']) != VS_PAIR)
                sims.append(f'<div class="simv">Groups 2 and 4: <b>{gap:.3f}</b>, kept apart by the hatch; every other pair <b>{rest:.3f}</b> or more</div>')
            else:
                sims.append(f'<div class="simv">Smallest lightness gap between neighbors: <b>{gap:.3f}</b></div>')
        else:
            c = m['closest'][k]
            if cat:
                sims.append(f'<div class="simv">Closest pair, {e(c["between"][0])} and {e(c["between"][1])[-1]}: <b>{c["delta_e_ok"]:.3f}</b></div>')
            else:
                sims.append(f'<div class="simv">Closest neighbors: <b>{c["delta_e_ok"]:.3f}</b></div>')
    extra = []
    if cat and ground != 'charcoal':
        extra.append('<div class="rh" style="padding-top:2px">Black only</div>')
        for i, r in enumerate(m['rows']):
            g = r['luminance_gray']
            fg = '#FFFFFF' if C.luminance(g) < 0.18 else '#000000'
            if i == 3:
                extra.append(f'<div class="bo" style="background:{hatch_bg(g, "#FFFFFF")};box-shadow:inset 0 0 0 1px {g}"><span style="background:#FFFFFF;color:#000000;padding:2px 4px">Lines at {r["black_screen_pct"]}%</span></div>')
            else:
                extra.append(f'<div class="bo" style="background:{g};color:{fg}">{r["black_screen_pct"]}% screen</div>')
        extra.append('<div class="simv">Black ink on White paper, at the screen that matches each ink\'s luminance</div>')
    tok_note = ' The fills and labels come from the Newsprint tokens, as a printed report puts them on the paper (DR-53).' if ground == 'white' else ''
    return (f'<div class="plate g-{ground}" id="{pid}-{ground}" data-plate="{pid}-{ground}">'
            f'<div class="ph"><h3>On {GROUND_WORD[ground]}</h3><p>{e(plate_note(pid, ground, m))}{e(tok_note)}</p></div>'
            f'<div class="scroll"><div class="rg" style="--n:{n}">{"".join(cells)}{"".join(sims)}{"".join(extra)}</div></div></div>')


def plate_note(pid, ground, m):
    rows = m['rows']
    under = [r['name'] for r in rows if r['fill_on_ground'] < 3]
    lab_min = min(r['label_on_fill'] for r in rows)
    if pid == 'categorical':
        return (f'Every ink measures 3 to 1 or more on {GROUND_WORD[ground]} ({min(r["fill_on_ground"] for r in rows):.2f} at the least), '
                f'and every label {lab_min:.2f} to 1 or more.')
    s = ''
    if under:
        nums = [int(n.split()[-1]) for n in under]
        if len(nums) == 1:
            who = f'Step {nums[0]} measures'
        elif nums == list(range(nums[0], nums[-1] + 1)) and len(nums) > 2:
            who = f'Steps {nums[0]} to {nums[-1]} measure'
        else:
            who = 'Steps ' + ', '.join(str(n) for n in nums[:-1]) + f' and {nums[-1]} measure'
        s = f'{who} under 3 to 1 on {GROUND_WORD[ground]}, so a chart prints the value on or beside each. '
    s += f'Every label measures {lab_min:.2f} to 1 or more on its fill.'
    return s


# ------------------------------------------------------------------------------------------------ SVG helpers
def wrap(s, width, size, weight=400):
    words, lines, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if tw(t, size, weight) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def svg(w, h, body, label):
    return (f'<svg width="{f2(w)}" height="{f2(h)}" viewBox="0 0 {f2(w)} {f2(h)}" role="img" aria-label="{e(label)}" '
            f'style="display:block;overflow:visible">{body}</svg>')


def text(x, y, s, cls='t14', fill='var(--ink)', anchor='start', extra=''):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{f2(x)}" y="{f2(y)}" class="{cls}" style="fill:{fill}"{a}{extra}>{e(s)}</text>'


def tspan_lines(x, y, lines, lh, cls, fill, anchor='start'):
    return ''.join(text(x, y + i * lh, ln, cls, fill, anchor) for i, ln in enumerate(lines))


def marker(kind, cx, cy, color, area_r=5.5):
    a = math.pi * area_r ** 2
    if kind == 'circle':
        return f'<circle cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(area_r)}" style="fill:{color}"/>'
    if kind == 'square':
        s = math.sqrt(a)
        return f'<rect x="{f2(cx - s / 2)}" y="{f2(cy - s / 2)}" width="{f2(s)}" height="{f2(s)}" style="fill:{color}"/>'
    if kind == 'triangle':
        s = math.sqrt(4 * a / math.sqrt(3))
        h = s * math.sqrt(3) / 2
        return (f'<path d="M{f2(cx)} {f2(cy - h * 2 / 3)}L{f2(cx + s / 2)} {f2(cy + h / 3)}L{f2(cx - s / 2)} {f2(cy + h / 3)}Z" '
                f'style="fill:{color}"/>')
    d = math.sqrt(2 * a) / 2 * 1.0
    return f'<path d="M{f2(cx)} {f2(cy - d)}L{f2(cx + d)} {f2(cy)}L{f2(cx)} {f2(cy + d)}L{f2(cx - d)} {f2(cy)}Z" style="fill:{color}"/>'


def hatch_def(pid, color):
    return (f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="5" height="5" patternTransform="rotate(45)">'
            f'<rect width="1.5" height="5" style="fill:{color}"/></pattern>')


JOBS_GRADE = 'Documented: a Bureau of Labor Statistics survey of employers, as copied by FRED'   # D3-83
PHONE_W = 320   # the widest drawing a 390 px screen holds inside a plate


def dual(desktop, phone):
    """The desktop drawing and the phone drawing the kit would use (DR-64); CSS shows one by the screen's width."""
    return f'<div class="dsk">{desktop}</div><div class="phn">{phone}</div>'


def figure(eyebrow, heading, measure, body, source, notes='', grade=None):
    kick = (f'<p class="fh"><span class="ek">Finding</span><span class="gl">{e(grade)}</span></p>' if grade else f'<p class="fh">{e(eyebrow)}</p>')
    return (f'<figure>{kick}<p class="ft">{e(heading)}</p><p class="fm">{e(measure)}</p>'
            f'<div class="scroll">{body}</div>{notes}<p class="fs">{e(source)}</p></figure>')


# ------------------------------------------------------------------------------------------------ sequential: tile map
SEQ_RANGES = ['Under 58', '58 to 61.9', '62 to 65.9', '66 to 69.9', '70 or more']


def tile_map(ground):
    ts, gap = 44, 4
    cols = max(t['col'] for t in TILE) + 1
    rows = max(t['row'] for t in TILE) + 1
    top = 70
    body = []
    for i, rng in enumerate(SEQ_RANGES):
        x = i * 76
        body.append(f'<rect x="{x}" y="0" width="68" height="18" style="fill:var(--seq{i + 1})"/>')
        body.append(text(x, 36, rng, 't13', 'var(--csec)'))
    us = US_TURNOUT
    k = seq_step(us)
    ux = 5 * 76 + 28
    body.append(f'<rect x="{ux}" y="0" width="{ts}" height="{ts}" style="fill:var(--seq{k})"/>')
    body.append(text(ux + 5, 16, 'U.S.', 't13 b', f'var(--seql{k})'))
    body.append(text(ux + 5, 38, f'{us:.1f}', 't13', f'var(--seql{k})'))
    body.append(tspan_lines(ux + ts + 10, 16, ['United States,', f'margin {US_TURNOUT_MOE:g}'], 17, 't13', 'var(--csec)'))
    for t in TILE:
        v = TURNOUT[t['code']]['pct']
        s = seq_step(v)
        x, y = t['col'] * (ts + gap), top + t['row'] * (ts + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{ts}" height="{ts}" style="fill:var(--seq{s})" data-key="{t["code"]}" data-value="{v}"/>')
        body.append(text(x + 5, y + 16, t['code'], 't13 b', f'var(--seql{s})'))
        body.append(text(x + 5, y + 38, f'{v:.1f}', 't13', f'var(--seql{s})'))
    w = cols * (ts + gap) - gap
    h = top + rows * (ts + gap)
    return svg(w, h, ''.join(body), 'Tile map of the 50 states and DC: reported turnout among citizens 18 and over, '
                                     'November 2024, in five sequential Verdigris steps, each tile printing its value; the '
                                     'United States, 65.3 percent, is set apart beside the key.')


# ------------------------------------------------------------------------------------------------ diverging: heat table
DIV_RANGES = [f'Fell 2 percent or more', 'Fell 0.5 to 2 percent', 'Within 0.5 percent', 'Rose 0.5 to 2 percent', 'Rose 2 percent or more']


def glyph(step, x, y, color, size=18):
    s = size
    inner = {1: f'M{s / 2} {s - 3.5}L{s - 4} {4}H4Z', 2: f'M{s / 2} {s - 5.5}L{s - 6} {6.5}H6Z',
             3: None, 4: f'M{s / 2} 5.5L{s - 6} {s - 6.5}H6Z', 5: f'M{s / 2} 3.5L{s - 4} {s - 4}H4Z'}[step]
    shape = (f'<rect x="4" y="{s / 2 - 1.25}" width="{s - 8}" height="2.5" style="fill:{color}"/>' if inner is None
             else f'<path d="{inner}" style="fill:{color}"/>')
    return (f'<g transform="translate({f2(x)} {f2(y)})"><rect x="0.75" y="0.75" width="{s - 1.5}" height="{s - 1.5}" '
            f'style="fill:none;stroke:{color};stroke-width:1.5"/>{shape}</g>')


def div_table(ground):
    rows = sorted(SECTORS, key=lambda s: -YOY[s]['2026-09'])
    name_w, cw, ch, gx = 222, 88, 34, 3
    x0 = name_w + 8
    body = []
    for i, rng in enumerate(DIV_RANGES):
        xx = (i % 3) * 200
        yy = (i // 3) * 30
        body.append(f'<rect x="{xx}" y="{yy}" width="30" height="24" style="fill:var(--div{i + 1})"/>')
        body.append(glyph(i + 1, xx + 6, yy + 3, f'var(--divl{i + 1})'))
        body.append(text(xx + 38, yy + 17, rng, 't13', 'var(--csec)'))
    heads = [wrap(PERIOD_WORD[p] + (', preliminary' if p == '2026-09' else ''), cw, 13, 600) for p in PERIODS]
    top = 76
    hmax = max(len(h) for h in heads)
    for j, lines in enumerate(heads):
        body.append(tspan_lines(x0 + j * (cw + gx), top + 13 + 16 * (hmax - len(lines)), lines, 16, 't13 b', 'var(--ink)'))
    y = top + 16 * hmax + 8
    for s in rows + ['Total nonfarm']:
        tot = s == 'Total nonfarm'
        if tot:
            y += 10
        nm = wrap('All sectors' if tot else s, name_w, 13, 600 if tot else 400)
        rh = ch if len(nm) == 1 else ch + 2
        body.append(tspan_lines(0, y + rh / 2 + 5 - 8 * (len(nm) - 1), nm, 16, 't13' + (' b' if tot else ''), 'var(--ink)'))
        for j, p in enumerate(PERIODS):
            v = 100 * (_jobs[s][p] / _jobs[s][f'{int(p[:4]) - 1}-09'] - 1)
            k = div_step(v)
            cx = x0 + j * (cw + gx)
            body.append(f'<rect x="{cx}" y="{y}" width="{cw}" height="{rh - 3}" style="fill:var(--div{k})" data-key="{e(s)}" data-value="{v:.2f}"/>')
            body.append(glyph(k, cx + 7, y + (rh - 3) / 2 - 9, f'var(--divl{k})'))
            body.append(text(cx + cw - 8, y + (rh - 3) / 2 + 5, fmt_signed(v), 't14 b', f'var(--divl{k})', 'end'))
        y += rh
    w = x0 + 4 * (cw + gx)
    return svg(w, y, ''.join(body), 'Heat table: 12-month percent change in jobs for 15 sectors and all sectors, in the four '
                                    'years to September 2026, each cell colored by diverging pair B with a boxed arrow and its value.')


# ------------------------------------------------------------------------------------------------ categorical
def line_path(xs, ys):
    return 'M' + 'L'.join(f'{f2(x)} {f2(y)}' for x, y in zip(xs, ys))


def scale(d0, d1, r0, r1):
    return lambda v: r0 + (v - d0) * (r1 - r0) / (d1 - d0)


def x_ticks(X, y, color, every=1):
    out = []
    for m in ['2022-01', '2023-01', '2024-01', '2025-01', '2026-01'][::every]:
        i = MONTHS.index(m)
        out.append(f'<line x1="{f2(X(i))}" y1="{y}" x2="{f2(X(i))}" y2="{y + 5}" style="stroke:{color};stroke-width:1"/>')
        out.append(text(X(i), y + 20, m[:4], 't13', 'var(--csec)', 'middle'))   # ticks sit at each January
    return ''.join(out)


def y_grid(Y, lo, hi, step, x0, x1, fmt=lambda v: f'{v:g}'):
    out = []
    v = math.ceil(lo / step) * step
    while v <= hi + 1e-9:
        out.append(f'<line x1="{x0}" y1="{f2(Y(v))}" x2="{x1}" y2="{f2(Y(v))}" style="stroke:var(--grid);stroke-width:1"/>')
        out.append(text(x0 - 6, Y(v) + 4.5, fmt(v), 't13', 'var(--csec)', 'end'))
        v += step
    return ''.join(out)


def cat_lines(ground, phone=False):
    pw, ph = (156, 230) if phone else (300, 250)
    lab_w = 120 if phone else 220
    x0, y0 = 30 if phone else 36, 10
    lo = math.floor(min(min(INDEX[s]) for s in FOUR) / 5) * 5
    hi = math.ceil(max(max(INDEX[s]) for s in FOUR) / 5) * 5
    X = scale(0, len(MONTHS) - 1, x0, x0 + pw)
    Y = scale(lo, hi, y0 + ph, y0)
    body = [y_grid(Y, lo, hi, 5, x0, x0 + pw)]
    body.append(f'<line x1="{x0}" y1="{f2(Y(100))}" x2="{x0 + pw}" y2="{f2(Y(100))}" style="stroke:var(--base);stroke-width:1.5"/>')
    ends = []
    for i, s in enumerate(FOUR):
        ys = [Y(v) for v in INDEX[s]]
        body.append(f'<path d="{line_path([X(j) for j in range(len(MONTHS))], ys)}" style="fill:none;stroke:var(--cat{i + 1});'
                    f'stroke-width:2;stroke-linejoin:round"/>')
        ends.append(ys[-1])
    lab_x = x0 + pw + (16 if phone else 22)
    pos = spread(ends, 58 if phone else 44, y0 + 8, y0 + ph + 10)
    for i, s in enumerate(FOUR):
        body.append(marker(CAT_MARKER[i], x0 + pw, ends[i], f'var(--cat{i + 1})'))
        lines = wrap(s, lab_w, 14, 600)
        ly = pos[i] - (len(lines) * 17) / 2 + 12
        if abs(pos[i] - ends[i]) > 3:
            body.append(f'<path d="M{x0 + pw + 8} {f2(ends[i])}L{lab_x - 4} {f2(pos[i])}" style="fill:none;stroke:var(--ctx);stroke-width:1"/>')
        body.append(tspan_lines(lab_x, ly, lines, 17, 't14 b', 'var(--lab)'))
        body.append(text(lab_x, ly + len(lines) * 17, f'{fmt_signed(CHANGE4[s])} percent', 't14', 'var(--csec)'))
    body.append(x_ticks(X, y0 + ph, 'var(--csec)', every=2 if phone else 1))
    return svg(lab_x + lab_w + 4, y0 + ph + 30, ''.join(body),
               'Line chart: jobs in four sectors indexed to January 2022, to September 2026, one line each in the four '
               'categorical inks with an end marker and a direct label.')


def cat_stack(ground, W=560):
    """The same four groups as the line chart above it, in one bar of their September 2026 jobs, each segment named on the
    bar (CD M5, brand P1 and P2). The last segment's name sits at the bar's end; the others hang from leaders in rows
    ordered right to left, each name to the right of its own leader, so no leader crosses a name."""
    size = 13 if W < 400 else 14
    parts = [(s, _jobs[s]['2026-09']) for s in FOUR]
    tot = sum(v for _, v in parts)
    last = f'{parts[-1][0]}, {parts[-1][1] / 1000:.1f}'
    BW = W - tw(last, size, 600) - 22
    body = [f'<defs>{hatch_def(f"h4-{ground}-{W}", "var(--cat4)")}</defs>']
    x, bh = 0, 36
    segs = []
    for i, (s, v) in enumerate(parts):
        w = BW * v / tot
        val = f'{v / 1000:.1f}'
        fits = w - 16 >= tw(val, 15, 600)
        if i == 3:
            body.append(f'<rect x="{f2(x + 0.5)}" y="0.5" width="{f2(max(w - 1, 1))}" height="{bh - 1}" '
                        f'style="fill:url(#h4-{ground}-{W});stroke:var(--cat4);stroke-width:1"/>')
        else:
            body.append(f'<rect x="{f2(x)}" y="0" width="{f2(w - 1)}" height="{bh}" style="fill:var(--cat{i + 1})"/>')
            if fits:
                body.append(text(x + 8, 23, val, 't15 b', f'var(--catl{i + 1})'))
        segs.append((x, w, s, val, fits, i))
        x += w
    # the last, narrow segment: its name at the bar's end, with its marker
    body.append(marker(CAT_MARKER[3], x + 9, bh / 2, 'var(--cat4)', 4.5))
    body.append(text(x + 18, bh / 2 + 5, last, f't{size} b', 'var(--lab)'))
    y = bh + 8
    for x0, w, s, val, fits, i in reversed(segs[:3]):
        cx = x0 + min(w / 2, 14)
        words = s + ('' if fits else f', {val}')
        lines = wrap(words, W - cx - 12, size, 600)
        y += size + 6
        body.append(f'<path d="M{f2(cx)} {bh + 2}V{f2(y - 5)}" style="fill:none;stroke:var(--ctx);stroke-width:1"/>')
        body.append(marker(CAT_MARKER[i], cx, y - 5, f'var(--cat{i + 1})', 4.5))
        body.append(tspan_lines(cx + 10, y, lines, size + 4, f't{size} b', 'var(--lab)'))
        y += (len(lines) - 1) * (size + 4)
    return svg(W, y + 6, ''.join(body),
               'One bar of the same four sectors\' jobs in September 2026, millions, in the categorical inks with the fourth '
               'hatched, each segment named on the chart: health care and social assistance, government, manufacturing and information.')


# ------------------------------------------------------------------------------------------------ past four groups
def small_multiples(ground, phone=False):
    cols, pw, ph, gx, gy = (2, 150, 90, 20, 22) if phone else (5, 236, 112, 21, 26)
    order = sorted(SECTORS, key=lambda s: -CHANGE4[s])
    lo = math.floor(min(min(INDEX[s]) for s in SECTORS) / 5) * 5
    hi = math.ceil(max(max(INDEX[s]) for s in SECTORS) / 5) * 5
    head = 44
    body = []
    for n, s in enumerate(order):
        cx = (n % cols) * (pw + gx)
        cy = (n // cols) * (head + ph + gy + 18)
        X = scale(0, len(MONTHS) - 1, cx, cx + pw)
        Y = scale(lo, hi, cy + head + ph, cy + head)
        lines = wrap(s, pw - (58 if phone else 70), 13 if phone else 14, 600)
        body.append(tspan_lines(cx, cy + 15, lines, 16 if phone else 17, ('t13' if phone else 't14') + ' b', 'var(--lab)'))
        body.append(text(cx + pw, cy + 15, f'{fmt_signed(CHANGE4[s])}%', ('t13' if phone else 't14') + ' b', 'var(--lab)', 'end'))
        body.append(f'<line x1="{cx}" y1="{f2(Y(100))}" x2="{cx + pw}" y2="{f2(Y(100))}" style="stroke:var(--base);stroke-width:1.5"/>')
        xs = [X(j) for j in range(len(MONTHS))]
        for o in SECTORS:
            if o != s:
                body.append(f'<path d="{line_path(xs, [Y(v) for v in INDEX[o]])}" style="fill:none;stroke:var(--ghost);stroke-width:1"/>')
        body.append(f'<path d="{line_path(xs, [Y(v) for v in INDEX[s]])}" style="fill:none;stroke:var(--sub);stroke-width:3;stroke-linejoin:round"/>')
        if n >= len(order) - (len(order) % cols or cols):
            body.append(text(cx, cy + head + ph + 17, 'Jan. 2022', 't13', 'var(--csec)'))
            body.append(text(cx + pw, cy + head + ph + 17, 'Sep. 2026', 't13', 'var(--csec)', 'end'))
    rows = math.ceil(len(order) / cols)
    return svg(cols * pw + (cols - 1) * gx, rows * (head + ph + gy + 18) - gy, ''.join(body),
               'Small multiples: 15 panels, one per sector, each drawing its own jobs line in ink, indexed to January 2022, '
               'over the other 14 sectors drawn as faint ghost lines on one shared scale.')


def one_in_ink(ground):
    pw, ph = 228, 420
    x0, y0 = 36, 10
    lo = math.floor(min(min(INDEX[s]) for s in SECTORS) / 5) * 5
    hi = math.ceil(max(max(INDEX[s]) for s in SECTORS) / 5) * 5
    X = scale(0, len(MONTHS) - 1, x0, x0 + pw)
    Y = scale(lo, hi, y0 + ph, y0)
    xs = [X(j) for j in range(len(MONTHS))]
    body = [y_grid(Y, lo, hi, 5, x0, x0 + pw)]
    body.append(f'<line x1="{x0}" y1="{f2(Y(100))}" x2="{x0 + pw}" y2="{f2(Y(100))}" style="stroke:var(--base);stroke-width:1.5"/>')
    others = [s for s in SECTORS if s != LEAD]
    for s in others:
        body.append(f'<path d="{line_path(xs, [Y(v) for v in INDEX[s]])}" style="fill:none;stroke:var(--ctx);stroke-width:2;stroke-linejoin:round"/>')
    body.append(f'<path d="{line_path(xs, [Y(v) for v in INDEX[LEAD]])}" style="fill:none;stroke:var(--sub);stroke-width:3;stroke-linejoin:round"/>')
    ends = [Y(INDEX[s][-1]) for s in SECTORS]
    pos = spread(ends, 19, y0 + 4, y0 + ph + 4)
    lab_x = x0 + pw + 30
    for s, ey, py in zip(SECTORS, ends, pos):
        lead = s == LEAD
        cls = 't13' + (' bb' if lead else '')
        col = 'var(--lab)' if lead else 'var(--csec)'
        body.append(f'<path d="M{x0 + pw + 4} {f2(ey)}L{x0 + pw + 10} {f2(ey)}L{lab_x - 4} {f2(py)}" '
                    f'style="fill:none;stroke:var(--ctx);stroke-width:1"/>')
        body.append(text(lab_x + 46, py + 4.5, f'{fmt_signed(CHANGE4[s])}%', cls, col, 'end'))
        body.append(text(lab_x + 54, py + 4.5, s, cls, col))
    body.append(x_ticks(X, y0 + ph, 'var(--csec)'))
    return svg(lab_x + 54 + 248, y0 + ph + 30, ''.join(body),
               f'Line chart: jobs in 15 sectors indexed to January 2022; {LEAD} in ink, the other 14 in gray, every line '
               'labeled at its end with its change since January 2022.')


# ------------------------------------------------------------------------------------------------ the grade line code
def fitted(pat, w, length):
    """Stretch a pattern so the line starts and ends on ink (System 1's fitted(), design frame memo rule 2)."""
    if pat is None:
        return None
    arr = [x * w for x in pat]
    if arr[0] == 0:                       # dotted
        n = max(1, round(length / arr[1]))
        return [0, length / n]
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return [x * k for x in arr]


def grade_line(key, w, length, color, x=0, y=0, case=None):
    g = next(r for r in GRADES if r[0] == key)
    pat, cap = g[5], g[6]
    if key == 'conceptual':
        rail = ALC['hollow_rail_px']
        off = w / 2 + rail / 2
        return ''.join(f'<line x1="{f2(x)}" y1="{f2(y + d)}" x2="{f2(x + length)}" y2="{f2(y + d)}" '
                       f'style="stroke:{color};stroke-width:{rail}"/>' for d in (-off, off))
    if cap == 'round':                    # a round cap reaches w/2 past each end, so the run starts and ends w/2 inside
        x, length = x + w / 2, length - w
    da = fitted(pat, w, length)
    dash = f';stroke-dasharray:{" ".join(f2(v) for v in da)}' if da else ''
    out = ''
    if case:
        out += (f'<line x1="{f2(x)}" y1="{f2(y)}" x2="{f2(x + length)}" y2="{f2(y)}" style="stroke:{case};'
                f'stroke-width:{w + 2};stroke-linecap:{cap}{dash}"/>')
    out += (f'<line x1="{f2(x)}" y1="{f2(y)}" x2="{f2(x + length)}" y2="{f2(y)}" style="stroke:{color};'
            f'stroke-width:{w};stroke-linecap:{cap}{dash}"/>')
    return out


LC_VARIANTS = [
    ('ink-newsprint', 'Ink on Newsprint', 'newsprint', 'var(--oa-color-graphic-essential-on-newsprint)', None),
    ('ink-charcoal', 'Ink on Charcoal', 'charcoal', 'var(--oa-color-graphic-essential-on-charcoal)', None),
    ('context', 'Context, Stone on Newsprint', 'newsprint', 'var(--oa-chart-color-context-on-newsprint)', None),
    ('red', 'Red target, with its Charcoal case', 'newsprint', 'var(--oa-chart-color-point-on-newsprint)', 'var(--oa-chart-color-point-keyline-on-newsprint)'),
    ('black', 'Black only, on White paper', 'white', '#000000', None),
]


def lc_cell(key, variant, scale_k=1, widths=LINE_WIDTHS, length=168):
    vid, _, ground, color, case = variant
    rows = []
    h = 0
    for w in widths:
        h += max(w + 4, 12) + 8
    y = 0
    for w in widths:
        rh = max(w + 4, 12) + 8
        rows.append(grade_line(key, w, length, color, 0, y + rh / 2, case if key != 'conceptual' else None))
        y += rh
    W, H = length, h
    return (f'<svg width="{f2(W * scale_k)}" height="{f2(H * scale_k)}" viewBox="0 -1 {W} {H + 2}" aria-hidden="true" '
            f'focusable="false" style="display:block">{"".join(rows)}</svg>')


def grade_label(key):
    g = next(r for r in GRADES if r[0] == key)
    sq = ('<svg width="7" height="7" viewBox="0 0 7 7" aria-hidden="true" style="display:inline-block;margin-right:6px;'
          'vertical-align:0"><rect width="7" height="7" style="fill:currentColor"/></svg>') if key == 'documented' else ''
    v7 = f'V7 value {g[1]}' if g[1] else 'V7 closure: conceptual'
    if key == 'conceptual':
        pat = 'two rails, the gap one line width'
    elif g[5] is None:
        pat = 'one unbroken line'
    else:
        nums = [f2(x) for x in g[5]]
        pat = (', '.join(nums[:-1]) + ' and ' + nums[-1]) + f' line widths, {g[6]} caps'
    return (f'<span class="gw">{sq}{e(g[2])}</span><span class="gg">{e(g[3])}</span>'
            f'<span class="gg">{e(g[4].capitalize())}: {e(pat)}</span><span class="gg">{e(v7)}</span>')


def line_code_table(scale_k=1, variants=LC_VARIANTS, widths=LINE_WIDTHS, length=168, caption=''):
    head = ''.join(f'<th scope="col">{e(v[1])}</th>' for v in variants)
    body = []
    for g in GRADES:
        cells = ''.join(
            (f'<td class="cell g-{v[2]}" style="background:var(--gr);max-width:{length * scale_k + 20}px;white-space:normal">'
             '<span class="gg" style="color:var(--sec)">No red. A reform targets numbered connections and variables, and a '
             'conceptual step is neither.</span></td>') if (v[0] == 'red' and g[0] == 'conceptual') else
            f'<td class="cell g-{v[2]}" style="background:var(--gr)">{lc_cell(g[0], v, scale_k, widths, length)}</td>' for v in variants)
        body.append(f'<tr><th scope="row" style="min-width:190px">{grade_label(g[0])}</th>{cells}</tr>')
    return (f'<div class="scroll"><table class="lc"><caption class="vh">{e(caption)}</caption><thead><tr><th scope="col">Grade</th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


def v7_compare():
    rows = []
    for key in ('plausible', 'contested', 'hypothesis'):
        g = next(r for r in GRADES if r[0] == key)
        arr = [float(x) for x in V7_RENDERER[key].split()]
        length = 168
        v7 = (f'<line x1="0" y1="8" x2="{length}" y2="8" style="stroke:var(--oa-color-palette-charcoal);stroke-width:2;'
              f'stroke-dasharray:{V7_RENDERER[key]}"/>')
        ours = grade_line(key, 2, length, 'var(--oa-color-palette-charcoal)', 0, 8)
        rows.append(f'<tr><th scope="row"><span class="gw">{e(g[2])}</span></th>'
                    f'<td class="cell g-newsprint" style="background:var(--gr)"><svg width="{length * 2}" height="32" viewBox="0 0 {length} 16" aria-hidden="true">{v7}</svg>'
                    f'<span class="gg">{e(V7_RENDERER[key])}, as Phase 0 read V7\'s renderer</span></td>'
                    f'<td class="cell g-newsprint" style="background:var(--gr)"><svg width="{length * 2}" height="32" viewBox="0 0 {length} 16" aria-hidden="true">{ours}</svg>'
                    f'<span class="gg">{" ".join(f2(x * 2) for x in g[5])} at 2 px, fitted to the run</span></td></tr>')
    return ('<div class="scroll"><table class="lc"><caption class="vh">V7\'s renderer beside the proposed tokens, both on a 2 px line at twice size</caption>'
            '<thead><tr><th scope="col">Grade</th><th scope="col">V7\'s renderer, 2 px line, at 2x</th><th scope="col">Proposed token, 2 px line, at 2x</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


# ------------------------------------------------------------------------------------------------ red: point and red on red
def ranked_bars_phone(ground, mode, ctx='ctx', W=PHONE_W):
    """The phone form of the ranked bars (DR-64): each name above its bar, so no name runs off a 390 px screen."""
    order = sorted(SECTORS, key=lambda s: -CHANGE4[s])
    X = scale(-15, 20, 0, W - 56)
    body, y = [], 0
    for s in order:
        v, lead = CHANGE4[s], s == LEAD
        cls, col = ('t13 bb', 'var(--lab)') if lead else ('t13', 'var(--csec)')
        body.append(text(0, y + 13, s, cls, col))
        x1, x2 = sorted([X(0), X(v)])
        if lead and mode == 'red':
            kl = 'var(--keyline)' if ground == 'newsprint' else 'none'
            body.append(f'<rect x="{f2(x1 + 0.5)}" y="{y + 19.5}" width="{f2(x2 - x1 - 1)}" height="11" '
                        f'style="fill:var(--point);stroke:{kl};stroke-width:1" data-red="working" data-red-job="the point the title names"/>')
        else:
            body.append(f'<rect x="{f2(x1)}" y="{y + 19}" width="{f2(x2 - x1)}" height="12" '
                        f'style="fill:var(--{"sub" if lead else ctx})"/>')
        body.append(text((X(v) if v >= 0 else X(0)) + 5, y + 29, f'{fmt_signed(v)}%', cls, col))
        body.append(f'<line x1="{f2(X(0))}" y1="{y + 17}" x2="{f2(X(0))}" y2="{y + 33}" style="stroke:var(--base);stroke-width:1.5"/>')
        y += 40
    return svg(W, y - 4, ''.join(body), f'Ranked bars, phone form: change in jobs for 15 sectors, January 2022 to '
                                        f'September 2026, each name above its bar; {LEAD} named in the title.')


def ranked_bars(ground, mode, ctx='ctx'):
    """Ranked bars of the change since January 2022; mode 'red' gives the named bar the working red, 'ink' yields it to
    the subject ink. ctx='lfill' draws the other bars in the light fill (brand P5's variant)."""
    order = sorted(SECTORS, key=lambda s: -CHANGE4[s])
    name_w, bar_w, pitch, bh = 232, 196, 22, 14
    lo, hi = -15, 20
    X = scale(lo, hi, name_w + 8, name_w + 8 + bar_w)
    body = []
    y = 4
    for s in order:
        v = CHANGE4[s]
        lead = s == LEAD
        x1, x2 = sorted([X(0), X(v)])
        if lead and mode == 'red':
            kl = 'var(--keyline)' if ground == 'newsprint' else 'none'
            body.append(f'<rect x="{f2(x1 + 0.5)}" y="{f2(y + 0.5)}" width="{f2(x2 - x1 - 1)}" height="{bh - 1}" '
                        f'style="fill:var(--point);stroke:{kl};stroke-width:1" data-red="working" data-red-job="the point the title names"/>')
        elif lead:
            body.append(f'<rect x="{f2(x1)}" y="{y}" width="{f2(x2 - x1)}" height="{bh}" style="fill:var(--sub)"/>')
        else:
            body.append(f'<rect x="{f2(x1)}" y="{y}" width="{f2(x2 - x1)}" height="{bh}" style="fill:var(--{ctx})"/>')
        cls = 't13 bb' if lead else 't13'
        col = 'var(--lab)' if lead else 'var(--csec)'
        body.append(text(name_w, y + 11, s, cls, col, 'end'))
        tx = X(v) + 5 if v >= 0 else X(0) + 5
        body.append(text(tx, y + 11, f'{fmt_signed(v)}%', cls, col))
        y += pitch
    body.append(f'<line x1="{f2(X(0))}" y1="0" x2="{f2(X(0))}" y2="{y - 4}" style="stroke:var(--base);stroke-width:1.5"/>')
    return svg(name_w + 8 + bar_w + 50, y, ''.join(body),
               f'Ranked bars: change in jobs for 15 sectors, January 2022 to September 2026; {LEAD} '
               + ('in the working red with its keyline.' if mode == 'red' else 'in the subject ink, its label bold.'))


def error_mark(color):
    return (f'<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true" focusable="false">'
            f'<circle cx="9" cy="9" r="8" style="fill:none;stroke:{color};stroke-width:1.5"/>'
            f'<rect x="8.1" y="4.2" width="1.8" height="6.4" style="fill:{color}"/><rect x="8.1" y="12" width="1.8" height="1.8" style="fill:{color}"/></svg>')


def view_card(label, ground, chart_mode, form, ask_mode, caption, fail=False, ctx='ctx'):
    chart = (f'<p class="fh"><span class="ek">Finding</span><span class="gl">{e(JOBS_GRADE)}</span></p>'
             f'<p class="ft" style="font-size:22px;line-height:26px">{e(LEAD_TITLE)}</p>'
             f'<p class="fm" style="font-size:14px;line-height:21px">Change in jobs, percent, January 2022 to September 2026, '
             f'United States; August and September 2026 are preliminary.</p>'
             f'<div class="scroll">{dual(ranked_bars(ground, chart_mode, ctx), ranked_bars_phone(ground, chart_mode, ctx))}</div>')
    f = ''
    if form:
        err = form == 'error'
        ink = 'var(--ink)'
        msg = (f'<div class="msg">{error_mark(ink)}<span><b>Error:</b> Enter an email address with an @, such as '
               f'name@example.com.</span></div>') if err else ''
        val = 'name.example.com' if err else 'name@example.com'
        ask_cls = 'red' if ask_mode == 'red' else 'ink'
        f = (f'<div class="form"><span class="fl">Email me the next jobs chart</span>'
             f'<div class="field{" err" if err else ""}">{val}</div>{msg}'
             f'<button class="ask {ask_cls}" type="button" tabindex="-1">Send me the chart</button>'
             f'<p class="ex">The form and its address are Illustrative.</p></div>')
    lab_cls = 'vlab fail' if fail else 'vlab'
    return (f'<div class="view"><p class="{lab_cls}">{e(label)}</p><div class="vbody g-{ground}">{chart}{f}</div>'
            f'<p class="cap">{caption}</p></div>')


def red_views():
    src = f'<p class="fs" style="margin-top:18px">{e(JOBS_SOURCE)}</p>'
    cards = [
        view_card('1. The chart in a view of its own', 'newsprint', 'red', None, None,
                  'Correct. With no error and no step to take in the view, the bar the title names takes the working red, '
                  'with its 1 px Charcoal keyline, since Pillar Red measures 2.96 to 1 on Newsprint.'),
        view_card('2. Fails Rule 05.3', 'newsprint', 'red', 'error', 'red',
                  '<b>Fails Rule 05.3.</b> The same chart meets a form with an error, and three reds compete: the error, '
                  'the ask and the chart\'s point. A reader cannot tell which one to act on first.', fail=True),
        view_card('3. Resolved: the error keeps the red', 'newsprint', 'ink', 'error', 'ink',
                  'Correct. The error keeps the red, on its bar and the field\'s edge. The ask steps down to Charcoal, '
                  'and the chart\'s point yields to the subject ink, keeping its bold label and its place (Rule 11.16).'),
        view_card('4. After the reader fixes the address', 'newsprint', 'ink', 'fixed', 'red',
                  'Correct. The red goes to the ask, the step the reader can take now. The point stays in ink, since a '
                  'step outranks the point a title names. It takes the red again only in a view with no ask.'),
        view_card('5. Resolved, on Charcoal', 'charcoal', 'ink', 'error', 'ink',
                  'Correct, in the dark theme. Pillar Red measures 4.49 to 1 on Charcoal, so the error bar needs no edge; '
                  'the point yields to Newsprint, the subject ink on Charcoal.'),
        view_card('6. The point in red, on Charcoal', 'charcoal', 'red', None, None,
                  'Correct. In a view of its own on Charcoal, the named bar takes the working red with no keyline.'),
        view_card('7. A variant to weigh: the other bars in the light fill', 'newsprint', 'red', None, None,
                  f'Correct, and a choice for the creative director. With the other bars in the light fill, which prints '
                  f'each value beside its bar, the red bar prints darker than its neighbors in gray: Chromium\'s filter gives '
                  f'{luma(P["pillarRed"]):.3f} against {luma(hx("oa.chart.color.lightFill.onNewsprint")):.3f}, where view 1 '
                  f'gives {luma(P["pillarRed"]):.3f} against {luma(P["stone"]):.3f}. The grayscale capture shows both.',
                  ctx='lfill'),
        view_card('8. The same variant, resolved', 'newsprint', 'ink', 'error', 'ink',
                  'Correct. When an error holds the red, the named bar yields to the subject ink, which stands out against '
                  'the light fill in color and in gray.', ctx='lfill'),
    ]
    return f'<div class="views">{"".join(cards)}</div>{src}'


def red_chips():
    out = []
    for g in ('newsprint', 'white', 'charcoal', 'prussian'):
        r = cr(P['pillarRed'], P[g])
        if g == 'prussian':
            body = ('<div style="height:72px;display:flex;align-items:center;font:600 15px/20px Inter,sans-serif">'
                    'No red here. Red never sits on Prussian (Rule 05.3).</div>')
            note = f'Measured {r:.2f} to 1, and red with Prussian reads as a party pair'
        else:
            kl = g == 'newsprint'
            body = (f'<svg width="200" height="72" viewBox="0 0 200 72" role="img" aria-label="Red point on {GROUND_WORD[g]}">'
                    f'<rect x="{0.5 if kl else 0}" y="{20.5 if kl else 20}" width="{109 if kl else 110}" height="{19 if kl else 20}" '
                    f'style="fill:var(--oa-color-palette-pillar-red);{"stroke:var(--oa-color-palette-charcoal);stroke-width:1" if kl else ""}"/>'
                    f'<circle cx="160" cy="30" r="6.5" style="fill:var(--oa-color-palette-pillar-red);{"stroke:var(--oa-color-palette-charcoal);stroke-width:1" if kl else ""}"/></svg>')
            note = (f'{r:.2f} to 1 on the ground, so the mark takes a 1 px Charcoal keyline at {cr(P["charcoal"], P["newsprint"]):.2f}' if kl
                    else f'{r:.2f} to 1 on the ground, so the mark needs no keyline')
        out.append(f'<div class="plate g-{g}" style="margin-top:0"><div class="ph"><h3>On {GROUND_WORD[g]}</h3></div>{body}'
                   f'<p class="pn" style="margin-top:8px">{e(note)}.</p></div>')
    return f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px">{"".join(out)}</div>'


# ------------------------------------------------------------------------------------------------ Prussian
def prussian_rows():
    inks = [('Charcoal', P['charcoal'], 'Categorical group 1'), ('Prussian', P['prussian'], 'Categorical group 2; diverging step 1'),
            ('Verdigris', P['verdigris'], 'Categorical group 3; sequential base'), ('Stone', P['stone'], 'Categorical group 4; context'),
            ('Pillar Red', P['pillarRed'], 'The working red'), ('Newsprint', P['newsprint'], 'Subject ink on dark grounds')]
    rows = []
    for name, h, job in inks:
        r = cr(h, P['prussian'])
        rows.append({'ink': name, 'hex': h, 'job_in_charts': job, 'on_prussian': r, 'passes_3_to_1': r >= 3})
    return rows


def prussian_panel(rows):
    chips = []
    for r in rows:
        verdict = 'passes 3 to 1' if r['passes_3_to_1'] else 'under 3 to 1'
        if r['ink'] == 'Pillar Red':
            verdict = 'never used: Rule 05.3'
        sw = (f'<div class="chip" style="background:{r["hex"]};box-shadow:inset 0 0 0 1px var(--oa-color-palette-newsprint)"></div>'
              if r['ink'] != 'Pillar Red' else '<div class="chip" style="border:1px solid var(--oa-color-derived-dim-newsprint);height:72px"></div>')
        chips.append(f'<div><div class="nm"><span>{e(r["ink"])}</span></div>{sw}<dl class="dl"><div><dt>On Prussian</dt><dd>{r["on_prussian"]:.2f}</dd></div>'
                     f'<div><dt>Verdict</dt><dd>{e(verdict)}</dd></div></dl></div>')
    return (f'<div class="plate g-prussian"><div class="ph"><h3>Each data ink, measured on Prussian</h3>'
            f'<p>Prussian is itself a data ink, and {sum(1 for r in rows[:4] if not r["passes_3_to_1"])} of the four categorical inks fall under 3 to 1 on it. Only Newsprint passes.</p></div>'
            f'<div class="scroll"><div class="rg" style="--n:6;grid-template-columns:repeat(6,152px)">{"".join(chips)}</div></div></div>')


# ------------------------------------------------------------------------------------------------ measures and checks
def all_measures():
    out = {pid: {g: measure_set(pid, g) for g in PLATES[pid]} for pid in PALETTES}
    return out


def checks(M):
    res = []

    def add(name, ok, detail):
        res.append({'check': name, 'passes': bool(ok), 'detail': detail})

    for pid, by in M.items():
        for g, m in by.items():
            low = min(r['label_on_fill'] for r in m['rows'])
            add(f'{pid} on {g}: every label 4.5 to 1 or more on its fill', low >= 4.5, f'lowest {low:.2f}')
            if pid == 'categorical':
                lowf = min(r['fill_on_ground'] for r in m['rows'])
                add(f'categorical on {g}: every ink 3 to 1 or more on the ground', lowf >= 3, f'lowest {lowf:.2f}')
                bad = [p for p in m['pairs_under_margin'] if 'Group 4' not in p['between']]
                add(f'categorical on {g}: only pairs with the hatched Stone group sit under 0.10 lightness', not bad,
                    f'{len(m["pairs_under_margin"])} pairs under 0.10, each with Group 4')
            if pid == 'categorical':
                rows = m['rows']
                nb = [(rows[i]['name'], rows[i + 1]['name'], round(abs(rows[i]['oklab_L'] - rows[i + 1]['oklab_L']), 3),
                       abs(rows[i]['black_screen_pct'] - rows[i + 1]['black_screen_pct'])) for i in range(3)]
                ok = all(d >= 0.10 or b == 'Group 4' for a, b, d, s in nb)
                add(f'categorical on {g}: neighbors in a stack stand 0.10 apart in lightness, or the second is the hatched group',
                    ok, '; '.join(f'{a} and {b}: {d:.3f}' for a, b, d, s in nb))
                if g != 'charcoal':
                    ok2 = all(s >= 10 or b == 'Group 4' for a, b, d, s in nb)
                    add(f'categorical on {g}: neighbors in a stack differ by 10 points of black or more in one-ink print',
                        ok2, '; '.join(f'{a} and {b}: {s} points' for a, b, d, s in nb))
            if 'grayscale_order_holds' in m:
                add(f'{pid} on {g}: grayscale order holds', m['grayscale_order_holds'],
                    f'smallest lightness gap {m["smallest_lightness_gap"]:.3f}')
            worst = min(v['delta_e_ok'] for k, v in m['closest'].items() if k != 'normal')
            if pid != 'categorical':
                add(f'{pid} on {g}: neighbors stay 0.05 or more apart (OKLab) under every simulation', worst >= 0.05, f'closest {worst:.3f}')
    dc = M['diverging']['charcoal']['rows']
    add('diverging on Charcoal: ends and near steps match in lightness within 0.01',
        abs(dc[0]['oklab_L'] - dc[4]['oklab_L']) <= 0.01 and abs(dc[1]['oklab_L'] - dc[3]['oklab_L']) <= 0.01,
        f'ends {dc[0]["oklab_L"]:.3f} and {dc[4]["oklab_L"]:.3f}; near steps {dc[1]["oklab_L"]:.3f} and {dc[3]["oklab_L"]:.3f}')
    add('every new color is one palette color mixed in OKLab toward Newsprint or Charcoal',
        all(NEW_TINTS[k][1] in ('newsprint', 'charcoal') for k in NEW_TINTS), ', '.join(f'{k} {NEW_TINT_HEX[k]}' for k in NEW_TINTS))
    for w in LINE_WIDTHS:
        add(f'grade line code at {w} px: the {MIN_RUN}-width shortest run holds two full dash-dot periods and the closing dash',
            MIN_RUN * w >= 2 * sum(x * w for x in GRADES[3][5]) + GRADES[3][5][0] * w,
            f'run {MIN_RUN * w} px, period {f2(sum(x * w for x in GRADES[3][5]))} px')
    return res


def line_code_values():
    """One table of every line code value, with where it comes from (D3-84)."""
    src = f'Atlas build, <code>pattern()</code>, line {ALC["pattern_line"]}'
    rows = []
    for g in GRADES:
        if g[0] == 'conceptual':
            continue
        nums = 'one unbroken line' if g[5] is None else ', '.join(f2(x) for x in g[5]) + f' line widths, {g[6]} caps'
        at2 = 'solid' if g[5] is None else ' '.join(f2(x * 2) for x in g[5])
        rows.append((f'{g[2]}: {g[3]}', nums, at2, src))
    rows += [
        ('Conceptual step: the hollow line', f'two {ALC["hollow_rail_px"]:g} px rails, one line width of ground between them',
         '1, 2, 1 (4 px across)', f'Atlas build, <code>wire_marks()</code>, line {ALC["wire_marks_line"]}'),
        ('Line widths', ', '.join(f'{w} px' for w in LINE_WIDTHS) + ', no others', '2 px', f'Atlas build, <code>{ALC["line_widths_from"].split(",")[0]}</code>,{ALC["line_widths_from"].split(",")[1]}'),
        ('Fitting', 'stretched so each line starts and ends on ink', 'per run', f'Atlas build, <code>fitted()</code>, line {ALC["fitted_line"]}'),
        ('Dotted line before an arrowhead', f'stops {f2(ALC["dotted_head_clearance_widths"])} line widths short', '3 px',
         f'Atlas build, <code>wire_marks()</code>, line {ALC["wire_marks_line"]}'),
        ('Shortest textured run', f'{MIN_RUN} line widths, key samples included', f'{MIN_RUN * 2} px',
         'Set here: the build defines none; two full dash-dot periods and the closing dash'),
        ('Record square', f'{RECORD_SQUARE} px, filled, inline before the word Documented', f'{RECORD_SQUARE} px',
         'Set here: the build draws none; Gate 1, M1, at the frame memo\'s size'),
        ('Hypothesis gloss', 'not yet tested', '', 'Rule 13.3\'s table; the build\'s shared table says untested'),
    ]
    body = ''.join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    return ('<div class="plate g-newsprint"><div class="ph"><h3>Every value, and where it comes from</h3>'
            '<p>The tokens in <code>oa.chart.grade</code> take these numbers, and Rule 13.4 states the same ones.</p></div>'
            '<div class="scroll"><table class="m"><caption class="vh">The line code\'s values and their sources</caption>'
            '<thead><tr><th>Item</th><th>Value</th><th>On a 2 px line</th><th>Source</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div></div>')


def section(sid, num, status, title, lede, side, body):
    st = ''.join(f'<span class="tag{" new" if "Proposed" in s else ""}" style="margin-right:8px">{e(s)}</span>' for s in status)
    return (f'<section class="sec" id="{sid}" aria-labelledby="{sid}-h" data-section="{sid}"><div class="sh"><div>'
            f'<p class="eyebrow">{num} &nbsp;{st}</p><h2 id="{sid}-h">{e(title)}</h2><p class="lede">{lede}</p></div>'
            f'<div class="side">{side}</div></div>{body}</section>')


def measure_table(M, pids):
    head = ('<tr><th>Palette</th><th>Ground</th><th>Step</th><th>Fill token</th><th>Status</th><th>Hex</th><th class="n">Fill on ground</th>'
            '<th>Label token</th><th class="n">Label</th><th class="n">Lightness</th><th>Gray</th><th>Protanopia</th>'
            '<th>Deuteranopia</th><th>Tritanopia</th></tr>')
    rows = []
    for pid in pids:
        for g, m in M[pid].items():
            for r in m['rows']:
                sw = lambda h: f'<span class="sq" style="background:{h}"></span>{h}'
                rows.append(f'<tr><td>{e(PALETTES[pid]["name"])}</td><td>{GROUND_WORD[g]}</td><td>{e(r["name"])}</td>'
                            f'<td><code>{e(r["fill_css"])}</code></td><td>{e(r["fill_status"])}</td><td>{sw(r["fill_hex"])}</td>'
                            f'<td class="n">{r["fill_on_ground"]:.2f}</td><td><code>{e(r["label_css"])}</code></td>'
                            f'<td class="n">{r["label_on_fill"]:.2f}</td><td class="n">{r["oklab_L"]:.3f}</td>'
                            f'<td>{sw(r["luminance_gray"])}</td><td>{sw(r["sim_protanopia"])}</td><td>{sw(r["sim_deuteranopia"])}</td>'
                            f'<td>{sw(r["sim_tritanopia"])}</td></tr>')
    return (f'<details class="mt"><summary>Every measured value in this section</summary><div class="scroll">'
            f'<table class="m"><caption class="vh">Measured values</caption><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div></details>')


def plates(pid, M):
    return ''.join(ramp_plate(pid, g, M[pid][g]) for g in PLATES[pid])


def two(*items):
    return f'<div class="two">{"".join(items)}</div>'


def applied(ground, fig, sid=''):
    return f'<div class="plate g-{ground}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}>{fig}</div>'


def build_page(M, CK):
    wm = WORDMARK.read_text()
    wm = re.sub(r'<title>.*?</title>', '', wm, flags=re.S)
    vb = re.search(r'viewBox="([^"]+)"', wm).group(1).split()
    wmw = float(vb[2]) * 24 / float(vb[3])
    wm = wm.replace('<svg ', f'<svg width="{wmw:.0f}" height="24" role="img" aria-label="Oath &amp; Action" focusable="false" ', 1)
    sq, dv, ct, mg = M['sequential'], M['diverging'], M['categorical'], M['magnitude']
    dvc = dv['charcoal']['rows']
    ctn = ct['newsprint']
    other_pairs = [p['delta_L'] for p in ctn['lightness_gaps'] if set(p['between']) != VS_PAIR]
    ctc_pairs = [p['delta_L'] for p in ct['charcoal']['lightness_gaps'] if set(p['between']) != VS_PAIR]
    seq_gaps_n = [p['delta_L'] for p in sq['newsprint']['lightness_gaps']]
    n_tokens = PROPOSAL_DATA['summary']['new_tokens_total']
    n_colors = PROPOSAL_DATA['summary']['new_colors']
    n_roles = sum(1 for tk in PROPOSAL_DATA['tokens'] if tk['tier'] == 'semantic' and tk['type'] == 'color')

    top = (f'<header class="mast"><div class="wrap mrow"><span class="wm">{wm}</span>'
           '<p class="run">Phase 3 · Round 0 · Palette proofs</p></div></header>'
           '<div class="wrap"><div class="top"><div><p class="eyebrow">Board 1 proof sheet · November 11, 2026</p>'
           '<h1 class="display">Data palettes, measured</h1><div class="deck">'
           '<p>Every data palette our charts use, drawn on each ground it may sit on, with its contrast, its grayscale and '
           'three simulations of color-vision deficiency. Two colors are new: the Prussian steps that let the diverging '
           'scale work in the dark theme. Every other proposed token reuses a value the tokens already hold.</p>'
           f'<p>Swatches marked In tokens come from release {e(RELEASE)}. Swatches marked Proposed come from the palette '
           'proposal and wait for board 1. The charts on this sheet draw real data, each with its source line, and every '
           'number on the sheet comes from its build script.</p></div></div>'
           f'<ul class="facts"><li><b>{n_colors}</b><span>new colors, both Prussian mixed toward Newsprint in OKLab</span></li>'
           f'<li><b>{n_tokens}</b><span>proposed tokens: the {n_colors} new colors, {n_roles} color roles that point at values the release already holds, and {n_tokens - n_colors - n_roles} for the grade line code</span></li>'
           '<li><b>0</b><span>new hues. The categorical set stays with the four brand inks (DR-234)</span></li>'
           f'<li><b>{sum(1 for c in CK if c["passes"])}</b><span>of {len(CK)} scripted checks pass on this sheet</span></li></ul></div>'
           '<div class="tools"><fieldset><legend>View this sheet as</legend>'
           + ''.join(f'<label><input type="radio" name="sim" value="{v}"{" checked" if v == "normal" else ""}>{w}</label>'
                     for v, w in [('normal', 'Normal'), ('grayscale', 'Grayscale'), ('protanopia', 'Protanopia'),
                                  ('deuteranopia', 'Deuteranopia'), ('tritanopia', 'Tritanopia')]) +
           '</fieldset><p class="side" style="max-width:46em">Grayscale is Chromium\'s grayscale filter. The three simulations '
           'apply the matrices of Machado, Oliveira and Fernandes (2009) at full severity in linear RGB; the strips under each '
           'swatch use the same matrices, computed by the build script.</p></div>'
           '<nav aria-label="Sections"><ul class="toc">'
           + ''.join(f'<li><a href="#{a}">{w}</a></li>' for a, w in [
               ('sequential', 'Sequential'), ('diverging', 'Diverging'), ('categorical', 'Categorical'),
               ('past-four', 'Past four groups'), ('magnitude', 'Magnitude'), ('line-code', 'Grade line code'),
               ('red', 'Red on red'), ('prussian', 'Prussian')]) + '</ul></nav></div>')

    s_seq = section(
        'sequential', '01', ['In tokens'], 'Sequential Verdigris',
        'One measure from low to high, in five Verdigris steps on each ground. The steps run light to strong on Newsprint '
        'and dark to light on Charcoal, so the largest value always reads strongest.',
        f'<p>Nothing changes here, and the proofs confirm the release. On Newsprint the lightness changes by '
        f'{min(seq_gaps_n):.3f} to {max(seq_gaps_n):.3f} at each step, so the order holds in gray, and neighbors stay at '
        f'least {min(v["delta_e_ok"] for k, v in sq["newsprint"]["closest"].items()):.3f} apart under all three simulations.</p>'
        '<p>Steps 1 to 3 measure under 3 to 1 on Newsprint, so a chart prints the value on or beside them, as the tile map does.</p>',
        plates('sequential', M) +
        two(applied('newsprint', figure('Proof on real data, Newsprint', 'Sequential Verdigris on a state tile map',
                                        'Reported voting among citizens 18 and over, percent, November 2024, 50 states and DC, '
                                        'in five steps. Every tile prints its value, so no reader has to match a shade.',
                                        tile_map('newsprint'), TURNOUT_SOURCE,
                                        f'<p class="fn">The United States stood at {US_TURNOUT:g} percent, margin {US_TURNOUT_MOE:g} '
                                        f'points, set apart beside the key (DR-64). State margins of error run from '
                                        f'{MOE_RANGE[0]} to {MOE_RANGE[1]} points, so a state near a step\'s edge may belong '
                                        'in the next step; every tile prints its value, and no tile is ranked.</p>'), 'tile-newsprint'),
            applied('charcoal', figure('Proof on real data, Charcoal', 'The same map in the dark theme',
                                       'The same data and steps on Charcoal, where the strongest step is the lightest.',
                                       tile_map('charcoal'), TURNOUT_SOURCE), 'tile-charcoal')) +
        measure_table(M, ['sequential']))

    s_div = section(
        'diverging', '02', ['Newsprint in tokens', 'Charcoal Proposed'], 'Diverging pair B',
        'Values above and below a midpoint: Prussian on one side and Verdigris on the other, through a midpoint tinted toward '
        'the ground (DR-54). The dark theme needs the scale on Charcoal (DR-204), and the release holds Newsprint steps only.',
        f'<p>On Charcoal the Verdigris half reuses the sequential scale\'s steps 3 and 4. The Prussian half takes two new mixes, '
        f'Prussian 56 and 29 percent toward Newsprint, picked so each Prussian step matches its Verdigris partner in '
        f'lightness ({dvc[0]["oklab_L"]:.3f} with {dvc[4]["oklab_L"]:.3f}, and {dvc[1]["oklab_L"]:.3f} with {dvc[3]["oklab_L"]:.3f}). '
        'The midpoint reuses the Charcoal band tint.</p><p>Matched ends look alike in gray and to a reader with '
        f'deuteranopia (the ends sit {dv["charcoal"]["end_pair"]["delta_e_deuteranopia"]:.3f} apart there), which is why the '
        'boxed arrow or a printed sign carries the direction in every cell, on both grounds.</p>',
        plates('diverging', M) +
        two(applied('newsprint', figure('Proof on real data, Newsprint', 'Diverging pair B in a heat table',
                                        'Change in jobs over 12 months, percent, for each of the four years to September 2026, '
                                        'by sector, United States. The boxed arrow in each cell carries the direction in any print.',
                                        div_table('newsprint'), JOBS_SOURCE,
                                        f'<p class="fn">{e(WINDOW_REASON)}</p>'), 'div-newsprint'),
            applied('charcoal', figure('Proof on real data, Charcoal', 'The same table in the dark theme',
                                       'The proposed Charcoal steps, with Charcoal labels on the two ends and Newsprint labels '
                                       'on the three middle steps.', div_table('charcoal'), JOBS_SOURCE), 'div-charcoal')) +
        measure_table(M, ['diverging']))

    s_cat = section(
        'categorical', '03', ['Proposed, no new value'], 'Categorical: four inks, four groups',
        'Up to four named groups, in the four brand inks and no added hue (DR-234): Charcoal, Verdigris, Prussian and Stone, '
        'in that order. On Charcoal, Newsprint takes Charcoal\'s place and Prussian lifts 62 percent toward Newsprint, a '
        'value the tokens already hold.',
        f'<p>The order is Charcoal, Verdigris, Prussian, Stone, so neither close pair ever touches in a stack: Charcoal and '
        f'Prussian print at {ctn["rows"][0]["black_screen_pct"]} and {ctn["rows"][2]["black_screen_pct"]} percent black in '
        f'one-ink print, and Verdigris and Stone sit {ctn["rows"][1]["oklab_L"] - ctn["rows"][3]["oklab_L"]:.2f} apart in '
        'lightness (D2-95). The Stone group always carries the hatch, and every group carries a direct label; on a line, '
        'each group ends on its own marker: circle, square, triangle and diamond.</p>'
        f'<p>Every other pair stands at least {min(other_pairs):.3f} apart in lightness on Newsprint and '
        f'{min(ctc_pairs):.3f} on Charcoal. The set never marks a party (DR-48).</p>',
        plates('categorical', M) +
        two(applied('newsprint', figure('Proof on real data, Newsprint', 'Four groups on a line chart, and in one bar',
                                        'Jobs in four sectors, indexed to January 2022 = 100, January 2022 to September 2026, '
                                        'United States. Below, the same four sectors\' jobs in September 2026, millions, a '
                                        'preliminary month.',
                                        dual(cat_lines('newsprint') + '<div style="height:28px"></div>' + cat_stack('newsprint'),
                                             cat_lines('newsprint', phone=True) + '<div style="height:24px"></div>' + cat_stack('newsprint', PHONE_W)),
                                        JOBS_SOURCE), 'cat-newsprint'),
            applied('charcoal', figure('Proof on real data, Charcoal', 'The same two charts in the dark theme',
                                       'The same data on Charcoal, in Newsprint, Verdigris, Prussian lifted 62 percent and '
                                       'hatched Stone.', dual(cat_lines('charcoal') + '<div style="height:28px"></div>' + cat_stack('charcoal'),
                                                              cat_lines('charcoal', phone=True) + '<div style="height:24px"></div>' + cat_stack('charcoal', PHONE_W)),
                                       JOBS_SOURCE), 'cat-charcoal')) +
        measure_table(M, ['categorical']))

    lead_title = LEAD_TITLE
    s_past = section(
        'past-four', '04', ['Proposed, no new value'], 'Past four groups',
        'Past four groups a chart takes one of two forms, with every group labeled on the chart (DR-234). Small multiples give '
        'each group a panel of its own, with the other groups faint behind it. One group in ink against gray keeps a single '
        'panel, and the title names the group in ink.',
        '<p>Neither form adds a color. The ghost lines reuse the light Stone fill on Newsprint and a dark Stone step on '
        'Charcoal, at 1 px, and repeat lines drawn in full in their own panels. The gray lines of the second form take the '
        'context ink the release already holds.</p>',
        applied('newsprint', figure('Proof on real data, Newsprint', 'Small multiples: 15 sectors, one panel each',
                                    'Jobs indexed to January 2022 = 100, January 2022 to September 2026, United States, '
                                    'on one shared scale, sorted by the change since January 2022.',
                                    dual(small_multiples('newsprint'), small_multiples('newsprint', phone=True)),
                                    JOBS_SOURCE, f'<p class="fn">{e(WINDOW_REASON)}</p>'), 'sm-newsprint') +
        applied('charcoal', figure('Proof on real data, Charcoal', 'The same small multiples in the dark theme',
                                   'The same panels on Charcoal, with the ghost lines in the dark Stone step.',
                                   dual(small_multiples('charcoal'), small_multiples('charcoal', phone=True)), JOBS_SOURCE), 'sm-charcoal') +
        two(applied('newsprint', figure('Finding, Newsprint', lead_title,
                                        'Jobs indexed to January 2022 = 100, January 2022 to September 2026, United States. '
                                        'One sector in ink, 14 in gray, each labeled with its change since January 2022. On a '
                                        'phone the chart becomes ranked bars, each name above its bar (DR-64).',
                                        dual(one_in_ink('newsprint'), ranked_bars_phone('newsprint', 'ink')), JOBS_SOURCE,
                                        grade=JOBS_GRADE), 'ink-newsprint'),
            applied('charcoal', figure('Finding, Charcoal', lead_title, 'The same chart in the dark theme.',
                                       dual(one_in_ink('charcoal'), ranked_bars_phone('charcoal', 'ink')), JOBS_SOURCE,
                                       grade=JOBS_GRADE), 'ink-charcoal')))

    s_mag = section(
        'magnitude', '05', ['In tokens'], 'Magnitude: Stone steps',
        'Gray steps by size, with no direction, for phone tile maps of shifts (DR-64). Arrows and words carry the direction, '
        'and the figure prints in every tile.',
        f'<p>Nothing changes here. The steps hold their order in gray on both grounds, at least '
        f'{min(mg["newsprint"]["smallest_lightness_gap"], mg["charcoal"]["smallest_lightness_gap"]):.3f} apart in lightness, '
        'and every label measures 4.5 to 1 or more on its fill.</p>',
        plates('magnitude', M) + measure_table(M, ['magnitude']))

    s_lc = section(
        'line-code', '06', ['Proposed, read from the atlas build'], 'The grade line code',
        'V7\'s line code for the evidence grade of a connection: solid for documented and well supported, dashed for '
        'plausible, dash-dot for contested and dotted for hypothesis, with the record square and the hollow line Gate 1 '
        'added (M1). Each pattern is a multiple of the line\'s width, as Rule 10.10 sets it, so the 6 px lit route keeps its texture.',
        '<p>Every value comes from one source, the atlas build\'s own <code>wire_marks</code> and its constants, read by '
        'script (D3-84). The tokens carry each pattern per 1 px of width, and the kit stretches it so a line starts and ends '
        'on ink. Phase 0 read V7\'s renderer\'s dash arrays as 9 and 4 for plausible, 9, 3, 2 and 3 for contested, and 2 '
        'and 4 for hypothesis; on a 2 px line the build draws 8 and 4, then 8, 3, 2 and 3, then round dots 5 px apart.</p>'
        f'<p>No coded line drops under 2 px. A run shorter than {MIN_RUN} widths, key samples included, prints its grade in '
        f'words beside it: {MIN_RUN * 2} px on a 2 px line.</p>',
        line_code_values() +
        '<div class="plate g-newsprint"><div class="ph"><h3>At true size</h3><p>Each grade at 2, 3 and 6 px, in color and in black, 168 px long.</p></div>'
        + line_code_table(1, caption='The grade line code at true size, in five treatments') +
        '<p class="pn">On a 2 px dotted line the Charcoal case swallows most of the red, so the dots read dark. The atlas '
        'already draws a reform\'s targets heavier, at 4 px and up (Rule 12.5), where the red holds; a red target never '
        'drops to 2 px.</p></div>'
        '<div class="plate g-newsprint" id="line-code-2x"><div class="ph"><h3>At twice size</h3><p>The 2 and 3 px lines at 2x, '
        'where a dot that clips or a dash that runs short would show.</p></div>'
        + line_code_table(2, [LC_VARIANTS[0], LC_VARIANTS[3], LC_VARIANTS[4]], [2, 3], 120, 'The grade line code at twice size') + '</div>'
        '<div class="plate g-newsprint"><div class="ph"><h3>V7\'s renderer beside the tokens</h3><p>Both on a 2 px line, drawn at twice size.</p></div>'
        + v7_compare() + '</div>')

    s_red = section(
        'red', '07', ['In tokens', 'Specimen for tension 14'], 'Red on red',
        'Each view carries one working red (Rule 05.3). A chart\'s red goes to the one point its title names, third in line '
        'after an error the reader must fix and a step the reader can take now. Master Brief tension 14 asks what happens '
        'when a chart\'s red meets a red the view already holds.',
        '<p>The answer needs no new token. The chart\'s point yields to the subject ink and keeps its bold label and its '
        'place, as the take-part mark and the intervention marker yield in Rule 11.16. The title still names it, so the '
        'reader loses nothing.</p><p>In the grayscale capture the red bar and the Stone bars print almost the same gray '
        f'(Chromium\'s filter gives {luma(P["pillarRed"]):.3f} and {luma(P["stone"]):.3f}), so the keyline, the bold label and '
        'the title carry the point in black-and-white print.</p>',
        red_chips() + red_views())

    s_pr = section(
        'prussian', '08', ['No chart tokens'], 'Prussian',
        'Charts stay off Prussian. Prussian is the strong end of the diverging scale and the second categorical ink, so a '
        'Prussian ground would hide them, and red never sits on it (Rule 05.3). A chart in a Prussian panel sits on its own '
        'Newsprint or Charcoal plate.',
        '<p>The release already keeps chart tokens to Newsprint and Charcoal. This panel shows the measurement behind that '
        'rule.</p>',
        prussian_panel(prussian_rows()))

    foot = ('<footer class="foot"><div class="wrap">'
            f'<p>Built by <code>work/boards/phase-3/round-0/palettes/build_palette_proofs.py</code> from <code>tokens.json</code> '
            f'release {e(RELEASE)} and the palette proposal, <code>work/handoffs/phase-3/20261111_Palette-Proposal.json</code>. '
            'Every ratio here is in <code>20261111_Palette-Proofs-Measures.json</code> beside this page.</p>'
            '<p>Contrast follows WCAG 2.2: 4.5 to 1 for text, 3 to 1 for marks a reader needs. Lightness is OKLab L. Gray '
            'swatches take the neutral gray with the same luminance, so they keep their contrast. Simulations follow Machado, '
            'Oliveira and Fernandes (2009), severity 1.0, in linear RGB.</p></div></footer>')
    script = ('<script>document.querySelectorAll(\'input[name="sim"]\').forEach(function(r){r.addEventListener("change",'
              'function(){if(r.checked){if(r.value==="normal"){document.documentElement.removeAttribute("data-sim")}'
              'else{document.documentElement.setAttribute("data-sim",r.value)}}})});</script>')
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Data Palettes, Measured</title>'
            '<meta name="description" content="Phase 3 round 0 palette proofs for the Oath &amp; Action brand guide: every data palette on each ground, with contrast, grayscale and color-vision simulations, the grade line code and the red-on-red specimen.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{token_css()}\n{ground_vars()}\n{PAGE_CSS}</style></head><body>')
    page = (head + SIM_FILTERS + top + '<main class="wrap">' + s_seq + s_div + s_cat + s_past + s_mag + s_lc + s_red + s_pr
            + '</main>' + foot + script + '</body></html>')
    return page


def main():
    M = all_measures()
    CK = checks(M)
    page = build_page(M, CK)
    assert '—' not in page and '‑' not in page, 'em dash or U+2011 in the page'
    used = set(re.findall(r'var\((--oa-[a-z0-9-]+)\)', page))
    defined = set(re.findall(r'(--oa-[a-z0-9-]+):', page))
    missing = sorted(used - defined)
    assert not missing, f'undefined tokens: {missing}'
    SHEET.write_text(page)
    PROPOSAL.write_text(json.dumps(PROPOSAL_DATA, indent=1, ensure_ascii=False) + '\n')
    measures = {
        'title': 'Palette proofs: every measured value', 'date': '2026-11-11', 'tokens_release': RELEASE,
        'proposal': 'work/handoffs/phase-3/20261111_Palette-Proposal.json',
        'method': {
            'contrast': 'WCAG 2.2 ratio from relative luminance; pass or fail on the unrounded ratio; printed to two decimals',
            'lightness': 'OKLab L (Ottosson), the grayscale proof the Phase 2 palette lab used',
            'grayscale_swatch': 'The neutral gray with the same relative luminance, so a gray swatch keeps the color\'s contrast',
            'grayscale_capture': 'Chromium\'s CSS filter grayscale(1)',
            'simulation': 'Machado, Oliveira and Fernandes (2009), severity 1.0, applied in linear sRGB; captures apply the same matrices through SVG feColorMatrix, which works in linear RGB',
            'distance': 'OKLab Euclidean distance (delta E OK)',
            'black_only': 'Black ink coverage on White paper that gives the same luminance, dot gain ignored',
            'thresholds': {'text': 4.5, 'graphic': 3.0, 'lightness_margin_categorical': 0.10,
                           'note': 'Fills inside a scale may sit under 3 to 1 when every value prints on or beside them (Rule 05.5, Gate 2 contrast table)'},
        },
        'checks': CK,
        'palettes': M,
        'prussian': prussian_rows(),
        'red_point': {g: {'pillar_red_on_ground': cr(P['pillarRed'], P[g]), 'keyline_needed': C.contrast(P['pillarRed'], P[g]) < 3,
                          'allowed': g != 'prussian'} for g in GROUND_HEX},
        'grade_line_code': {g[0]: {'v7_value': g[1], 'word': g[2], 'texture': g[4], 'per_line_width': g[5], 'cap': g[6],
                                   'at_widths': {w: (None if g[5] is None else [round(x * w, 2) for x in g[5]]) for w in LINE_WIDTHS},
                                   'fitted_on_168_px': {w: (None if g[5] is None else [round(x, 2) for x in fitted(g[5], w, 168 - (w if g[6] == 'round' else 0))]) for w in LINE_WIDTHS},
                                   'v7_renderer': V7_RENDERER.get(g[0])} for g in GRADES},
        'data_drawn': {
            'turnout_2024': {'breaks': TURNOUT_BREAKS, 'states': {k: {**v, 'step': seq_step(v['pct'])} for k, v in sorted(TURNOUT.items())},
                             'united_states': 65.3, 'source_line': TURNOUT_SOURCE},
            'jobs': {'window': 'January 2022 to September 2026', 'window_reason': WINDOW_REASON, 'source_line': JOBS_SOURCE,
                     'change_since_january_2022_pct': {s: round(v, 2) for s, v in CHANGE4.items()}, 'lead': LEAD,
                     'twelve_month_change_pct': {s: {p: round(v, 2) for p, v in YOY[s].items()} for s in SECTORS},
                     'diverging_breaks': DIV_BREAKS,
                     'diverging_steps': {s: {p: div_step(v) for p, v in YOY[s].items()} for s in SECTORS},
                     'categorical_four': FOUR, 'stack_groups': FOUR},
        },
    }
    MEASURES.write_text(json.dumps(measures, indent=1, ensure_ascii=False) + '\n')
    fails = [c for c in CK if not c['passes']]
    print(f'wrote {SHEET.relative_to(ROOT)} ({len(page):,} bytes), {MEASURES.relative_to(ROOT)}, {PROPOSAL.relative_to(ROOT)}')
    print(f'{len(CK) - len(fails)} of {len(CK)} checks pass')
    for c in fails:
        print('FAIL', c)


def verify():
    """Sample the captures: the page drew each swatch in its token's color, and the browser's filters match the script."""
    from PIL import Image
    log = json.loads(PROBES.read_text())

    def srgb_gray_css(h):
        # CSS grayscale(1): the luma matrix applied to the color's components
        r, g, b = C.hex_to_rgb(h)
        v = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return C.rgb_to_hex((v, v, v))

    def lin_gray_css(h):
        r, g, b = (C.lin(c) for c in C.hex_to_rgb(h))
        v = C.delin(0.2126 * r + 0.7152 * g + 0.0722 * b)
        return C.rgb_to_hex((v, v, v))

    out = {'date': '2026-11-11', 'tolerance_delta_e_ok': 0.01, 'by_mode': {}, 'worst': {}}
    for cap in log['captures']:
        if not cap['probes']:
            continue
        im = Image.open(HERE / cap['file']).convert('RGB')
        mode = cap['mode']
        rows = []
        for pr in cap['probes']:
            if pr['kind'] != 'fill' and not (mode == 'normal' and pr['kind'].startswith('sim-')):
                continue
            x, y = int(pr['x'] + pr['w'] * 0.15), int(pr['y'] + pr['h'] * 0.25)
            got = '#%02X%02X%02X' % im.getpixel((x, y))
            if mode == 'normal':
                want = pr['hex']
            elif mode == 'grayscale':
                want = srgb_gray_css(pr['hex'])
            else:
                want = simulate(pr['hex'], mode)
            rec = {'section': cap['section'], 'kind': pr['kind'], 'token_hex': pr['hex'], 'expected': want, 'sampled': got,
                   'delta_e_ok': dE(want, got)}
            if mode == 'grayscale':
                rec['if_linear_light'] = lin_gray_css(pr['hex'])
                rec['delta_e_linear'] = dE(rec['if_linear_light'], got)
            rows.append(rec)
        out['by_mode'].setdefault(mode, []).extend(rows)
    for mode, rows in out['by_mode'].items():
        w = max(rows, key=lambda r: r['delta_e_ok'])
        out['worst'][mode] = {'samples': len(rows), 'largest_delta_e_ok': w['delta_e_ok'], 'at': w,
                              'all_within_tolerance': all(r['delta_e_ok'] <= 0.01 for r in rows)}
        print(f"{mode:13s} {len(rows):4d} samples, largest delta E OK {w['delta_e_ok']:.4f}")
    m = json.loads(MEASURES.read_text())
    m['capture_verification'] = {k: v for k, v in out.items() if k != 'by_mode'}
    m['capture_verification']['samples'] = sum(len(v) for v in out['by_mode'].values())
    m['capture_verification']['method'] = ('Each probed swatch is sampled in its capture, 15 percent in from its left edge '
                                           'and a quarter down, and compared with the token color (normal), the luma '
                                           'grayscale of CSS filter grayscale(1) (grayscale), or this script\'s Machado '
                                           'simulation (the three color-vision captures)')
    MEASURES.write_text(json.dumps(m, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    if '--verify' in sys.argv:
        verify()
    else:
        main()
