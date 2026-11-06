"""Run every token test with one command.

Run from the project folder (oath-and-action-v6-brand-guide/):
    python3 -I work/build/tests/tokens/run_token_tests.py

Steps, in order; the run fails if any step fails:
  1. build check   node tokens_build.mjs --check: the files on disk are what the source builds
  2. parity        tokens.json and tokens.css agree, both ways, surface classes and reduced motion included
  3. rules         contrast on every surface, Rule 05.3, chart rules, type, opacity, motion, tiers, DTCG shape
  4. self-test     every planted break is caught by the test aimed at it
  5. cross-check   Style Dictionary reads tokens.json and agrees with tokens.css, and it reports a planted
                   change; skipped, and said so, when Style Dictionary is not installed in work/build
  6. rendered      Chromium (Playwright) resolves every token, paints each color-mix() derivation, nests
                   each surface in another and sets each type style at 390 and 1440 px; it must also report
                   a planted red leak onto Prussian; skipped, and said so, when Playwright is missing

Writes work/build/tests/tokens/20261106_Token-Test-Results.json with each step's result, the token counts
by group and tier, every plant and the role table by surface.
"""

import datetime
import importlib.util
import json
import pathlib
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
SELF = _load('test_token_selftest')
JSON_PATH = L.TOKENS_DIR / 'tokens.json'
CSS_PATH = L.TOKENS_DIR / 'tokens.css'
BUILD = L.ROOT / 'work/build/scripts/phase-2/tokens_build.mjs'
SD = HERE / 'sd_crosscheck.mjs'
RENDER = HERE / 'test_token_render.mjs'
RESULTS = HERE / '20261106_Token-Test-Results.json'


def counts(tree):
    toks = L.flatten(tree)
    out = {}
    for p, t in toks.items():
        segs = p.split('.')
        if segs[1] == 'color':
            group = f'color.{segs[2]}' if segs[2] in ('palette', 'derived', 'tint') else 'color (roles)'
        elif segs[1] == 'chart':
            group = 'chart.color' if segs[2] == 'color' else 'chart (sizes)'
        else:
            group = segs[1]
        tier = L.ext(t).get('tier', 'untiered')
        out.setdefault(group, {}).setdefault(tier, 0)
        out[group][tier] += 1
    return out


def main():
    steps = []
    ok = True

    def step(name, passed, detail):
        nonlocal ok
        ok = ok and passed is not False
        steps.append({'step': name, 'result': {True: 'pass', False: 'FAIL', None: 'skipped'}[passed], 'detail': detail})
        print(f'[{steps[-1]["result"]}] {name}: {detail if isinstance(detail, str) else ""}')

    res = subprocess.run(['node', str(BUILD), '--check'], capture_output=True, text=True)
    step('build check', res.returncode == 0, (res.stdout + res.stderr).strip())

    pf, ps = PARITY.check(JSON_PATH, CSS_PATH)
    step('parity', not pf, f'{ps.get("tokens")} tokens, {ps.get("rootProperties")} :root properties, '
                            f'{ps.get("shortNames")} short names in each of 4 surface classes, {len(pf)} failures')
    for f in pf[:20]:
        print('   FAIL', f)

    rf, rr = RULES.check(JSON_PATH, CSS_PATH)
    cells = sum(len(v) for v in rr.get('table', {}).values())
    step('rules', not rf, f'{rr.get("tokens")} tokens, {rr.get("derived")} derived colors and tints, {cells} semantic color cells measured, {len(rf)} failures')
    for f in rf[:20]:
        print('   FAIL', f)

    base_ok, plants = SELF.selftest(JSON_PATH, CSS_PATH, verbose=False)
    caught = sum(p['caught'] for p in plants)
    step('self-test', base_ok and caught == len(plants), f'clean files {"pass" if base_ok else "FAIL"}; plants caught {caught} of {len(plants)}')
    for p in plants:
        if not p['caught']:
            print('   MISSED', p['plant'], '->', p.get('failure') or p.get('note'))

    sd = subprocess.run(['node', str(SD)], capture_output=True, text=True)
    if sd.returncode == 2:
        step('cross-check', None, sd.stdout.strip())
    else:
        detail = sd.stdout.strip().splitlines()[0] if sd.stdout.strip() else sd.stderr.strip()
        planted = None
        if sd.returncode == 0:
            with tempfile.TemporaryDirectory(prefix='oa-sd-plant-') as tmp:
                bad = pathlib.Path(tmp) / 'tokens.css'
                bad.write_text(CSS_PATH.read_text(encoding='utf-8').replace('--oa-color-palette-stone: #5D636D;', '--oa-color-palette-stone: #5D636E;'), encoding='utf-8')
                pr = subprocess.run(['node', str(SD), '--css', str(bad)], capture_output=True, text=True)
                planted = pr.returncode == 1 and 'oa.color.palette.stone' in pr.stdout
            detail += f'; planted Stone change {"reported" if planted else "NOT reported"}'
        step('cross-check', sd.returncode == 0 and planted, detail)

    rd = subprocess.run(['node', str(RENDER)], capture_output=True, text=True)
    if rd.returncode == 2:
        step('rendered', None, rd.stdout.strip())
    else:
        detail = rd.stdout.strip().splitlines()[0] if rd.stdout.strip() else rd.stderr.strip()
        for line in rd.stdout.strip().splitlines()[1:21]:
            print('  ', line)
        planted = None
        if rd.returncode == 0:
            with tempfile.TemporaryDirectory(prefix='oa-render-plant-') as tmp:
                bad = pathlib.Path(tmp) / 'tokens.css'
                text = CSS_PATH.read_text(encoding='utf-8')
                i = text.index('.oa-surface-prussian {')
                j = text.index('  --oa-color-data-emphasis-red: initial;', i)
                bad.write_text(text[:j] + '  --oa-color-data-emphasis-red: var(--oa-color-data-emphasis-red-on-white);'
                               + text[j + len('  --oa-color-data-emphasis-red: initial;'):], encoding='utf-8')
                pr = subprocess.run(['node', str(RENDER), '--css', str(bad)], capture_output=True, text=True)
                planted = pr.returncode == 1 and 'oa.color.data.emphasisRed' in pr.stdout
            detail += f'; planted red leak onto Prussian {"reported" if planted else "NOT reported"}'
        step('rendered', rd.returncode == 0 and planted, detail)

    tree = L.load_json(JSON_PATH)
    meta = L.root_meta(tree)
    record = {
        'run': datetime.date.today().isoformat(),
        'command': 'python3 -I work/build/tests/tokens/run_token_tests.py',
        'tokenSetVersion': meta.get('tokenSetVersion'),
        'status': meta.get('status'),
        'passed': ok,
        'steps': steps,
        'counts': counts(tree),
        'plants': plants,
        'roleTable': RULES.table_md(rr.get('table', {})),
    }
    RESULTS.write_text(json.dumps(record, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'{"ALL TOKEN TESTS PASS" if ok else "TOKEN TESTS FAIL"}; results in {RESULTS.relative_to(L.ROOT)}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
