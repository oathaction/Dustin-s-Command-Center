"""Parity test: tokens.json and tokens.css say the same thing.

Run:  python3 -I work/build/tests/tokens/test_token_parity.py [--json PATH] [--css PATH] [--quiet]
Default inputs: work/build/tokens/tokens.json and work/build/tokens/tokens.css. Exit code 1 on any failure.

Checks, all against rules written here, not read from the generator:
  1. Every JSON token has its custom property in :root, and :root has no property the JSON lacks.
     A typography token has its shorthand and eight part properties.
  2. Where the JSON aliases a token, the CSS points at that token's property with var(); every property
     resolves through its var() chain to the same value the JSON resolves to.
  3. Values DTCG cannot hold match their JSON record: clamp() sizes hit the minimum at 390 px and the
     maximum at 1440 px, em tracking times the size gives the stored rem, 50% is the stored fraction.
  4. Each surface class sets exactly the short names the JSON's surface tokens imply, each pointing at its
     own surface's token or set to initial where that surface has no token, plus its background, ink and
     color scheme. No other selector exists.
  5. The reduced-motion block sets every duration, and only durations, to its reducedMotionValue.
  6. The stylesheet's header carries the JSON's version.
"""

import argparse
import importlib.util
import pathlib
import re
import sys

sys.dont_write_bytecode = True       # loading the sibling modules leaves no cache folder
HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('token_test_lib', HERE / 'token_test_lib.py')
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

GENERIC = {'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui'}
TYPE_PARTS = ['font-family', 'font-style', 'font-weight', 'font-size', 'line-height', 'letter-spacing',
              'text-transform', 'font-variant-numeric']
SCHEME = {'newsprint': 'light', 'white': 'light', 'charcoal': 'dark', 'prussian': 'dark'}


def num(x):
    s = f'{round(float(x), 6):.6f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def literal_css(t, e):
    """The CSS a literal DTCG value becomes, by the rules of Token Architecture section 7."""
    v, typ = t['$value'], t['$type']
    if typ == 'color':
        return v['hex']
    if typ in ('dimension', 'duration'):
        return f"{num(v['value'])}{v['unit']}"
    if typ == 'number':
        return e.get('css', num(v))
    if typ == 'fontWeight':
        return num(v)
    if typ == 'fontFamily':
        names = v if isinstance(v, list) else [v]
        return ', '.join(n if n in GENERIC else f'"{n}"' for n in names)
    if typ == 'cubicBezier':
        return 'cubic-bezier(' + ', '.join(num(x) for x in v) + ')'
    raise ValueError(f'no CSS rule for type {typ}')


def expected_props(toks):
    """name -> (expected raw CSS, origin path). Raw means before var() resolution."""
    exp = {}
    for p, t in toks.items():
        n = L.css_name(p)
        tgt = L.alias_target(t['$value'])
        typ = L.resolved_type(p, toks)
        if typ == 'typography':
            if tgt:
                tn = L.css_name(tgt)
                for part in TYPE_PARTS:
                    exp[f'{n}-{part}'] = (f'var({tn}-{part})', p)
                exp[n] = (f'var({tn})', p)
                continue
            v, e = t['$value'], L.ext(t)

            def sub(x, render):
                a = L.alias_target(x) if isinstance(x, str) else None
                return f'var({L.css_name(a)})' if a else render(x)
            exp[f'{n}-font-family'] = (sub(v['fontFamily'], lambda x: literal_css({'$type': 'fontFamily', '$value': x}, {})), p)
            exp[f'{n}-font-style'] = (e.get('fontStyle', 'normal'), p)
            exp[f'{n}-font-weight'] = (sub(v['fontWeight'], num), p)
            exp[f'{n}-font-size'] = (e.get('cssFontSize') or f"{num(v['fontSize']['value'])}{v['fontSize']['unit']}", p)
            exp[f'{n}-line-height'] = (num(v['lineHeight']), p)
            exp[f'{n}-letter-spacing'] = (f"{num(e.get('trackingEm', 0))}em", p)
            exp[f'{n}-text-transform'] = ('uppercase' if e.get('textTransform') == 'uppercase' else 'none', p)
            exp[f'{n}-font-variant-numeric'] = (e.get('numeric', 'normal'), p)
            exp[n] = (f'var({n}-font-style) var({n}-font-weight) var({n}-font-size)/var({n}-line-height) var({n}-font-family)', p)
            continue
        exp[n] = (f'var({L.css_name(tgt)})' if tgt else literal_css(t, L.ext(t)), p)
    return exp


def parse_clamp(s):
    m = re.fullmatch(r'clamp\(\s*([\d.]+)rem,\s*(-?[\d.]+)rem \+ ([\d.]+)vw,\s*([\d.]+)rem\s*\)', s)
    return tuple(float(x) for x in m.groups()) if m else None


def check(json_path, css_path):
    fails = []
    tree = L.load_json(json_path)
    toks = L.flatten(tree)
    meta = L.root_meta(tree)
    sheet = L.parse_css(pathlib.Path(css_path).read_text(encoding='utf-8'))
    stats = {'tokens': len(toks)}

    roots = [d for sel, d in sheet['blocks'] if sel == ':root']
    if len(roots) != 1:
        fails.append(f'stylesheet: expected one :root block, found {len(roots)}')
        return fails, stats
    root = {}
    for name, value in roots[0]:
        if name in root:
            fails.append(f':root declares {name} twice')
        root[name] = value
    stats['rootProperties'] = len(root)

    # 1. presence, both ways
    try:
        exp = expected_props(toks)
    except (KeyError, ValueError) as err:
        fails.append(f'tokens.json: {err}')
        return fails, stats
    for n, (_, p) in exp.items():
        if n not in root:
            fails.append(f'{p}: tokens.json has it, tokens.css has no {n}')
    for n in root:
        if n not in exp:
            fails.append(f'{n}: tokens.css declares it, tokens.json has no token for it')
    stats['expectedProperties'] = len(exp)

    # 2. aliases mirrored, values equal after resolution
    for n, (raw, p) in exp.items():
        if n not in root:
            continue
        got = root[n]
        if raw.startswith('var(') and ' '.join(got.split()) != ' '.join(raw.split()):
            fails.append(f'{p}: {n} should read {raw}, as the JSON aliases it; it reads {got}')
            continue
        try:
            want = L.resolve_css(raw, {k: v for k, (v, _) in exp.items()})
        except (KeyError, ValueError) as err:
            fails.append(f'{p}: the JSON side does not resolve ({err})')
            continue
        try:
            have = L.resolve_css(got, root)
        except (KeyError, ValueError) as err:
            fails.append(f'{p}: {n} does not resolve in tokens.css ({err})')
            continue
        if L.norm(want) != L.norm(have):
            fails.append(f'{p}: {n} resolves to {have} in tokens.css and to {want} in tokens.json')

    # 3. values DTCG cannot hold
    rng = meta.get('fluidRange', {'minViewportPx': 390, 'maxViewportPx': 1440})
    base = meta.get('remBasePx', 16)
    for p, t in toks.items():
        e = L.ext(t)
        v = t['$value']
        if t.get('$type') == 'typography' and isinstance(v, dict):
            size = v['fontSize']['value']
            css = e.get('cssFontSize', '')
            mn = (e.get('minFontSize') or v['fontSize'])['value']
            c = parse_clamp(css)
            if c:
                lo, icpt, slope, hi = c
                at = lambda vw: icpt * base + slope * vw / 100
                if abs(lo - mn) > 1e-6 or abs(hi - size) > 1e-6:
                    fails.append(f'{p}: clamp() runs {lo:g} to {hi:g} rem; the JSON says {mn:g} to {size:g} rem')
                if abs(at(rng['minViewportPx']) - mn * base) > 0.05 or abs(at(rng['maxViewportPx']) - size * base) > 0.05:
                    fails.append(f'{p}: clamp() gives {at(rng["minViewportPx"]):.2f} px at {rng["minViewportPx"]} and '
                                 f'{at(rng["maxViewportPx"]):.2f} px at {rng["maxViewportPx"]}; the JSON says {mn * base:g} and {size * base:g}')
            elif css != f'{num(size)}rem' or abs(mn - size) > 1e-9:
                fails.append(f'{p}: fixed size {css} does not match the JSON size {size:g} rem (minimum {mn:g})')
            ls = v['letterSpacing']['value']
            if abs(e.get('trackingEm', 0) * size - ls) > 1e-4:
                fails.append(f'{p}: {e.get("trackingEm")}em at {size:g} rem is {e.get("trackingEm", 0) * size:.5f} rem; the JSON stores {ls} rem')
        if t.get('$type') == 'number' and 'css' in e:
            m = re.fullmatch(r'(-?[\d.]+)%', e['css'])
            if not m or abs(float(m.group(1)) / 100 - v) > 1e-9:
                fails.append(f'{p}: CSS value {e["css"]} does not equal the stored fraction {v}')

    # 4. surface classes
    bases = []
    for p in toks:
        segs = p.split('.')
        if segs[-1] in L.SURFACE_KEYS:
            b = '.'.join(segs[:-1])
            if b not in bases:
                bases.append(b)
    stats['shortNames'] = len(bases)
    seen_sel = set()
    for sel, decls in sheet['blocks']:
        if sel == ':root':
            continue
        m = re.fullmatch(r'\.oa-surface-([a-z]+)', sel)
        if not m or m.group(1) not in L.SURFACES:
            fails.append(f'stylesheet: unexpected selector "{sel}"')
            continue
        s = m.group(1)
        seen_sel.add(s)
        key = L.KEY_OF[s]
        got = {}
        for name, value in decls or []:
            if name in got:
                fails.append(f'.oa-surface-{s} declares {name} twice')
            got[name] = value
        want = {'background-color': f'var({L.css_name("oa.color.surface." + s)})',
                'color': f'var({L.css_name("oa.color.text.primary." + key)})',
                'color-scheme': SCHEME[s]}
        for b in bases:
            want[L.css_name(b)] = f'var({L.css_name(b + "." + key)})' if f'{b}.{key}' in toks else 'initial'
        for name, value in want.items():
            if name not in got:
                fails.append(f'.oa-surface-{s}: missing {name}')
            elif ' '.join(got[name].split()) != value:
                fails.append(f'.oa-surface-{s}: {name} reads {got[name]}; the JSON implies {value}')
        for name in got:
            if name not in want:
                fails.append(f'.oa-surface-{s}: {name} has no token behind it')
        for name, value in got.items():
            if name.startswith('--') and value != 'initial':
                try:
                    L.resolve_css(value, root)
                except (KeyError, ValueError) as err:
                    fails.append(f'.oa-surface-{s}: {name} does not resolve ({err})')
    for s in L.SURFACES:
        if s not in seen_sel:
            fails.append(f'stylesheet: no .oa-surface-{s} class')

    # 5. reduced motion
    durations = {L.css_name(p): L.ext(t).get('reducedMotionValue') for p, t in toks.items() if t.get('$type') == 'duration'}
    rm = [(q, inner) for q, inner in sheet['media'] if q.replace(' ', '') == '(prefers-reduced-motion:reduce)']
    others = [q for q, _ in sheet['media'] if q.replace(' ', '') != '(prefers-reduced-motion:reduce)']
    for q in others:
        fails.append(f'stylesheet: unexpected @media {q}')
    if len(rm) != 1:
        fails.append(f'stylesheet: expected one reduced-motion block, found {len(rm)}')
    else:
        inner = rm[0][1]
        if len(inner) != 1 or inner[0][0] != ':root':
            fails.append('reduced-motion block: expected a single :root rule')
        decls = dict(inner[0][1]) if inner else {}
        for n, rv in durations.items():
            if rv is None:
                fails.append(f'{n}: the duration token has no reducedMotionValue')
            elif n not in decls:
                fails.append(f'reduced-motion block: {n} is missing')
            elif L.norm(decls[n]) != L.norm(f"{num(rv['value'])}{rv['unit']}"):
                fails.append(f'reduced-motion block: {n} reads {decls[n]}; the JSON says {rv["value"]}{rv["unit"]}')
        for n in decls:
            if n not in durations:
                fails.append(f'reduced-motion block: {n} is not a duration token')

    # 6. version
    version = meta.get('tokenSetVersion')
    if not version or f'Version {version} ' not in sheet['header']:
        fails.append(f'stylesheet header does not carry the JSON version {version}')
    stats['version'] = version
    return fails, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=str(L.TOKENS_DIR / 'tokens.json'))
    ap.add_argument('--css', default=str(L.TOKENS_DIR / 'tokens.css'))
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    fails, stats = check(a.json, a.css)
    print(f'parity: {stats.get("tokens")} tokens, {stats.get("rootProperties")} :root properties, '
          f'{stats.get("shortNames")} short names per surface class, {len(fails)} failures')
    for f in fails if not a.quiet else fails[:20]:
        print('  FAIL', f)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
