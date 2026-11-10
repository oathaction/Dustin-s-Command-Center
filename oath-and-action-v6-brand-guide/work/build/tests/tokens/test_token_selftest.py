"""Self-test: plant broken copies of the token files and prove each test catches its plant.

Run:  python3 -I work/build/tests/tokens/test_token_selftest.py [--json PATH] [--css PATH]

The clean files must pass every check first. Then each plant changes one thing in a copy (in a temporary
folder; the real files are never touched), runs the parity test, the rule test and the generator's
--check, and counts the plant as caught only when the test it is aimed at reports a new failure that
names the planted thing. A check that passes everything therefore fails here.
"""

import argparse
import copy
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True       # loading the sibling modules leaves no cache folder
HERE = pathlib.Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L = _load('token_test_lib')
PARITY = _load('test_token_parity')
RULES = _load('test_token_rules')
BUILD = L.ROOT / 'work/build/scripts/phase-2/tokens_build.mjs'
NS = L.NS


# --- tools for writing plants ---------------------------------------------------------------------------
def node(tree, path):
    cur = tree
    for seg in path.split('.'):
        cur = cur[seg]
    return cur


def x(tree, path):
    return node(tree, path).setdefault('$extensions', {}).setdefault(NS, {})


def alias(path, target):
    def f(j, c):
        node(j, path)['$value'] = '{' + target + '}'
        return j, c
    return f


def css_replace(old, new, count=1):
    def f(j, c):
        if old not in c:
            raise AssertionError(f'plant could not find {old!r} in tokens.css')
        return j, c.replace(old, new, count)
    return f


def css_drop_line(prefix, within=None):
    def f(j, c):
        lines = c.split('\n')
        start = 0
        if within:
            start = next(i for i, ln in enumerate(lines) if ln.startswith(within))
        i = next(i for i, ln in enumerate(lines) if i >= start and ln.strip().startswith(prefix))
        del lines[i]
        return j, '\n'.join(lines)
    return f


def edit(fn):
    def f(j, c):
        fn(j)
        return j, c
    return f


def set_value(path, value):
    return edit(lambda j: node(j, path).__setitem__('$value', value))


def color(hexv, alpha=1):
    r = L.rgb(hexv)
    return {'colorSpace': 'srgb', 'components': [round(v, 4) for v in r], 'alpha': alpha, 'hex': hexv}


def add_token(group, name, token):
    return edit(lambda j: node(j, group).__setitem__(name, token))


def _prussian_leak(j, c):
    block = c[c.index('.oa-surface-prussian {'):]
    old = '  --oa-color-data-emphasis-red: initial;'
    if old not in block:
        raise AssertionError('plant could not find the Prussian emphasisRed line')
    i = c.index('.oa-surface-prussian {') + block.index(old)
    return j, c[:i] + '  --oa-color-data-emphasis-red: var(--oa-color-data-emphasis-red-on-white);' + c[i + len(old):]


def _white_leak(j, c):
    start = c.index('.oa-surface-white {')
    old = '  --oa-chart-color-subject: initial;'
    i = c.index(old, start)
    return j, c[:i] + '  --oa-chart-color-subject: var(--oa-chart-color-subject-on-newsprint);' + c[i + len(old):]


def _dark_theme_line(name, value):
    """Point one short name in the [data-oa-theme="dark"] block at another value."""
    def f(j, c):
        start = c.index('[data-oa-theme="dark"] {')
        i = c.index(f'  {name}:', start)
        k = c.index(';', i)
        return j, c[:i] + f'  {name}: {value}' + c[k:]
    return f


# Each plant: (label, function, test that must catch it, words its failure must contain)
PLANTS = [
    # the seven the brief names
    ('A changed value in tokens.css (Stone one step off)',
     css_replace('--oa-color-palette-stone: #5D636D;', '--oa-color-palette-stone: #5D636E;'), 'parity', 'oa.color.palette.stone'),
    ('A missing CSS property (secondary text on Newsprint)',
     css_drop_line('--oa-color-text-secondary-on-newsprint:'), 'parity', 'oa.color.text.secondary.onNewsprint'),
    ('An extra CSS property the JSON lacks',
     css_replace('  --oa-color-text-secondary-on-newsprint:', '  --oa-color-text-tertiary-on-newsprint: #777777;\n  --oa-color-text-secondary-on-newsprint:'),
     'parity', '--oa-color-text-tertiary-on-newsprint'),
    ('A red ask fill on Prussian',
     alias('oa.color.action.ask.fill.onPrussian', 'oa.color.palette.pillarRed'), 'rules', 'red never sits on Prussian'),
    ('A failing text contrast (Stone as secondary text on Newsprint, 4.29:1)',
     alias('oa.color.text.secondary.onNewsprint', 'oa.color.palette.stone'), 'rules', 'under 4.5:1'),
    ('A broken alias (a label pointing at a surface that does not exist)',
     alias('oa.component.button.primary.label.onWhite', 'oa.color.action.primary.label.onSnow'), 'rules', 'broken alias'),
    ('A party color set to Pillar Red',
     alias('oa.chart.color.party.mark.onNewsprint', 'oa.color.data.emphasisRed.onNewsprint'), 'rules', 'party mark resolves to Pillar Red'),
    # more ways the files can go wrong
    ('A changed value in tokens.json (space.200 from 1 rem to 1.25 rem)',
     set_value('oa.space.200', {'value': 1.25, 'unit': 'rem'}), 'parity', 'oa.space.200'),
    ('Red reaching Prussian through the stylesheet\'s surface class',
     _prussian_leak, 'rules', 'resolves to Pillar Red'),
    ('A chart role leaking onto White from an outer surface',
     _white_leak, 'parity', '.oa-surface-white: --oa-chart-color-subject'),
    ('A party color set to Prussian on Charcoal',
     alias('oa.chart.color.party.mark.onCharcoal', 'oa.color.state.selected.band.onCharcoal'), 'rules', 'party mark resolves to Prussian'),
    ('A party color pair (a second ink for one party)',
     add_token('oa.chart.color.party', 'markSecond', {'onNewsprint': {
         '$type': 'color', '$value': '{oa.color.data.context.onNewsprint}', '$description': 'Planted second party ink.',
         '$extensions': {NS: {'tier': 'component', 'partyMark': True}}}}), 'rules', 'no party color pair'),
    ('Working red on Newsprint without its keyline',
     edit(lambda j: x(j, 'oa.color.data.emphasisRed.onNewsprint').pop('keyline')), 'rules', 'keyline'),
    ('Red as text (an error message set in Pillar Red)',
     alias('oa.color.state.error.text.onWhite', 'oa.color.palette.pillarRed'), 'rules', 'red never sets text'),
    ('A red hinge divider',
     alias('oa.color.identity.hingeDivider.onWhite', 'oa.color.palette.pillarRed'), 'rules', 'hinge divider'),
    ('A diverging step set to red',
     alias('oa.chart.color.diverging.fill.step2.onNewsprint', 'oa.color.palette.pillarRed'), 'rules', 'diverging step is red'),
    ('A derived red ink (#AC3339, rejected at Gate 1)',
     add_token('oa.color.tint', 'redInk', {'$type': 'color', '$value': color('#AC3339'), '$description': 'Planted small red text.',
                                           '$extensions': {NS: {'tier': 'primitive', 'status': 'adopted', 'job': 'Small red text', 'kind': 'text',
                                                                'surfaces': ['newsprint'], 'need': 'N-01', 'contrast': {'newsprint': 4.53},
                                                                'derivation': {'method': 'color-mix', 'space': 'oklab', 'base': '{oa.color.palette.pillarRed}',
                                                                               'toward': '{oa.color.palette.charcoal}', 'amount': 0.25}}}}),
     'rules', 'derived red'),
    ('A tint whose hex its derivation does not produce',
     edit(lambda j: node(j, 'oa.color.tint.stoneN55')['$value'].update(hex='#A1A2A4', components=[round(v, 4) for v in L.rgb('#A1A2A4')])),
     'rules', 'condition 2'),
    ('A tint with no registered need',
     edit(lambda j: x(j, 'oa.color.tint.stoneN70').__setitem__('need', 'N-99')), 'rules', 'condition 1'),
    ('The locked Pillar Red changed to Atlas V7\'s #BD2C32',
     edit(lambda j: node(j, 'oa.color.palette.pillarRed').__setitem__('$value', color('#BD2C32'))), 'rules', 'locked value'),
    ('A stale stored contrast ratio',
     edit(lambda j: x(j, 'oa.color.text.primary.onNewsprint').__setitem__('contrast', 14.0)), 'rules', 'stale'),
    ('An 11 px label',
     edit(lambda j: node(j, 'oa.type.label')['$value'].__setitem__('fontSize', {'value': 0.6875, 'unit': 'rem'})), 'rules', 'under the 13 px floor'),
    ('The ask label at 15 px',
     edit(lambda j: (node(j, 'oa.type.ask')['$value'].__setitem__('fontSize', {'value': 0.9375, 'unit': 'rem'}),
                     x(j, 'oa.type.ask').__setitem__('minFontSize', {'value': 0.9375, 'unit': 'rem'}))), 'rules', 'large-text pass'),
    ('Chart type at 12 px',
     set_value('oa.chart.type.tick', {'value': 12, 'unit': 'px'}), 'rules', 'oa.chart.type.tick'),
    ('A third opacity job (a 40% disabled label)',
     add_token('oa.opacity', 'disabledLabel', {'$type': 'number', '$value': 0.4, '$description': 'Planted disabled label. Decoration only.'}),
     'rules', 'two decorative jobs'),
    ('A transparent color token',
     edit(lambda j: node(j, 'oa.color.tint.stoneN70')['$value'].__setitem__('alpha', 0.6)), 'rules', 'never transparent'),
    ('A duration off V5\'s timing',
     set_value('oa.motion.duration.fast', {'value': 150, 'unit': 'ms'}), 'rules', 'V5 sets 120 ms'),
    ('A duration missing from the reduced-motion block',
     css_drop_line('--oa-motion-duration-hinge: 0ms', within='@media'), 'parity', 'reduced-motion block'),
    ('A clamp() size that no longer reaches the JSON maximum',
     edit(lambda j: node(j, 'oa.type.title')['$value'].__setitem__('fontSize', {'value': 7, 'unit': 'rem'})), 'parity', 'clamp()'),
    ('A 16 px icon allowed a red accent',
     edit(lambda j: x(j, 'oa.component.icon.accent.onNewsprint').__setitem__('minSize', '{oa.size.icon.small}')), 'rules', 'R10'),
    ('The app icon tile moved to Newsprint',
     alias('oa.component.appIcon.tile', 'oa.color.surface.newsprint'), 'rules', 'R13'),
    ('An alias cycle',
     edit(lambda j: (node(j, 'oa.color.surface.white').__setitem__('$value', '{oa.color.surface.prussian}'),
                     node(j, 'oa.color.surface.prussian').__setitem__('$value', '{oa.color.surface.white}'))), 'rules', 'cycle'),
    ('A component token pointing straight at a primitive',
     alias('oa.component.button.disabled.label.onWhite', 'oa.color.palette.stone'), 'rules', 'must alias a semantic token'),
    ('Rule 05.3 reworded',
     edit(lambda j: j['$extensions'][NS].__setitem__('redRule', j['$extensions'][NS]['redRule'].replace('Red never sits on Prussian.', 'Red rarely sits on Prussian.'))),
     'rules', 'Rule 05.3'),
    ('A stylesheet edited by hand, so it no longer matches the source',
     css_replace('--oa-z-index-skip: 100;', '--oa-z-index-skip: 999;'), 'build', 'differ'),
    # stage C, round 0 (November 10, 2026): the themes (DR-204, D2-1133)
    ('The dark theme pointing secondary text at its Newsprint token',
     _dark_theme_line('--oa-color-text-secondary', 'var(--oa-color-text-secondary-on-newsprint)'), 'rules', 'another surface'),
    ('A dark theme role under its contrast (Stone as secondary text on Charcoal, 3.10:1)',
     alias('oa.color.text.secondary.onCharcoal', 'oa.color.palette.stone'), 'rules', 'dark theme'),
    ('The device\'s dark setting overriding data-oa-theme="light" on the root',
     css_replace('  :root:not([data-oa-theme="light"]) {', '  :root {'), 'parity', 'wins over the device'),
    ('A short name missing from the light theme (the focus ring)',
     css_drop_line('--oa-color-focus-ring:', within=':root:not([data-oa-theme="dark"]),'), 'parity', 'light theme'),
    ('The dark theme moved from Charcoal to Prussian',
     edit(lambda j: j['$extensions'][NS]['theme']['dark'].__setitem__('surface', 'prussian')), 'parity', 'DR-204'),
    ('A version rise with no change note',
     edit(lambda j: j['$extensions'][NS].__setitem__('tokenSetVersion', '6.0.0-gate2.8')), 'rules', 'change note'),
]

def run_checks(jp, cp):
    out = {}
    try:
        out['parity'] = PARITY.check(jp, cp)[0]
    except Exception as err:          # a crash on broken input counts as a failure the test reported
        out['parity'] = [f'parity test stopped: {type(err).__name__}: {err}']
    try:
        out['rules'] = RULES.check(jp, cp)[0]
    except Exception as err:
        out['rules'] = [f'rule test stopped: {type(err).__name__}: {err}']
    res = subprocess.run(['node', str(BUILD), '--check', '--quiet', '--out-dir', str(pathlib.Path(jp).parent)],
                         capture_output=True, text=True)
    out['build'] = [] if res.returncode == 0 else [(res.stderr or res.stdout).strip() or f'exit {res.returncode}']
    return out


def selftest(json_path, css_path, verbose=True):
    clean_json = L.load_json(json_path)
    clean_css = pathlib.Path(css_path).read_text(encoding='utf-8')
    results = []
    with tempfile.TemporaryDirectory(prefix='oa-token-plants-') as tmp:
        tmp = pathlib.Path(tmp)
        jp, cp = tmp / 'tokens.json', tmp / 'tokens.css'
        # the clean copies are byte-identical to the real files, so the build check sees them as current
        clean_json_bytes = pathlib.Path(json_path).read_bytes()
        jp.write_bytes(clean_json_bytes)
        cp.write_text(clean_css, encoding='utf-8')
        base = run_checks(jp, cp)
        baseline_ok = not any(base.values())
        if verbose:
            print(f'self-test baseline: parity {len(base["parity"])}, rules {len(base["rules"])}, build {len(base["build"])} failures')
            for k, v in base.items():
                for f in v[:5]:
                    print(f'  BASELINE FAIL ({k})', f)
        for label, fn, target, words in PLANTS:
            j, c = copy.deepcopy(clean_json), clean_css
            try:
                j, c = fn(j, c)
            except Exception as err:
                results.append({'plant': label, 'test': target, 'caught': False, 'note': f'plant failed to apply: {err}'})
                continue
            # a file the plant left alone keeps its exact bytes, so only the planted change can trip the build check
            if j == clean_json:
                jp.write_bytes(clean_json_bytes)
            else:
                jp.write_text(json.dumps(j, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
            cp.write_text(c, encoding='utf-8')
            got = run_checks(jp, cp)
            new = [f for f in got[target] if f not in base[target]]
            hit = [f for f in new if words in f]
            others = sorted(k for k in got if k != target and [f for f in got[k] if f not in base[k]])
            results.append({'plant': label, 'test': target, 'caught': bool(hit), 'failure': (hit or new or [''])[0][:220],
                            'alsoCaughtBy': others})
    caught = sum(r['caught'] for r in results)
    if verbose:
        for r in results:
            mark = 'caught' if r['caught'] else 'MISSED'
            also = f" (also {', '.join(r['alsoCaughtBy'])})" if r.get('alsoCaughtBy') else ''
            print(f"  plant {mark} by {r['test']}{also}: {r['plant']}\n      -> {r.get('failure') or r.get('note')}")
        print(f'plants caught: {caught} of {len(results)}')
    return baseline_ok, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=str(L.TOKENS_DIR / 'tokens.json'))
    ap.add_argument('--css', default=str(L.TOKENS_DIR / 'tokens.css'))
    a = ap.parse_args()
    ok, results = selftest(a.json, a.css)
    sys.exit(0 if ok and all(r['caught'] for r in results) else 1)


if __name__ == '__main__':
    main()
