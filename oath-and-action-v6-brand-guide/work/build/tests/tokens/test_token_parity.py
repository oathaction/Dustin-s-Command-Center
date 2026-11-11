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
     own surface's token or set to initial where that surface has no token, plus its background, ink,
     color scheme and the ground's own short name (--oa-color-surface, DR-204). No other selector exists.
  5. The reduced-motion block sets every duration, and only durations, to its reducedMotionValue.
  6. The stylesheet's header carries the JSON's version.
  7. The themes (DR-204), as the JSON's root theme record names them: the light block on
     :root:not([data-oa-theme="dark"]) and [data-oa-theme="light"], the dark block inside
     (prefers-color-scheme: dark) on :root:not([data-oa-theme="light"]) only, so the attribute wins over the
     device, and the dark block again on [data-oa-theme="dark"]. Each sets exactly what its surface's class
     sets, pointing every short name at the theme surface's token.
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
    if typ == 'strokeStyle':   # Phase 3: the DTCG keyword; an object reads "dashed" (its companions carry the dashes)
        return v if isinstance(v, str) else 'dashed'
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
        if typ == 'strokeStyle' and not tgt:   # Phase 3: the dash array and line cap an SVG line takes
            v = t['$value']
            exp[f'{n}-dasharray'] = (('none' if v == 'solid' else v) if isinstance(v, str) else ' '.join(f"{num(d['value'])}{d['unit']}" for d in v['dashArray']), p)
            exp[f'{n}-line-cap'] = ('butt' if isinstance(v, str) else v['lineCap'], p)
    return exp


def parse_clamp(s):
    m = re.fullmatch(r'clamp\(\s*([\d.]+)rem,\s*(-?[\d.]+)rem \+ ([\d.]+)vw,\s*([\d.]+)rem\s*\)', s)
    return tuple(float(x) for x in m.groups()) if m else None


def surface_want(s, bases, toks, short_surface):
    """What a surface class, or a theme on that surface, must declare: its ground, ink, color scheme, the
    ground's short name and every short name, pointing at its own token or initial."""
    key = L.KEY_OF[s]
    want = {'background-color': f'var({L.css_name("oa.color.surface." + s)})',
            'color': f'var({L.css_name("oa.color.text.primary." + key)})',
            'color-scheme': SCHEME[s]}
    if short_surface:
        want[short_surface] = f'var({L.css_name("oa.color.surface." + s)})'
    for b in bases:
        want[L.css_name(b)] = f'var({L.css_name(b + "." + key)})' if f'{b}.{key}' in toks else 'initial'
    return want


def compare_block(label, decls, want, root, fails):
    got = {}
    for name, value in decls or []:
        if name in got:
            fails.append(f'{label} declares {name} twice')
        got[name] = value
    for name, value in want.items():
        if name not in got:
            fails.append(f'{label}: missing {name}')
        elif ' '.join(got[name].split()) != value:
            fails.append(f'{label}: {name} reads {got[name]}; the JSON implies {value}')
    for name in got:
        if name not in want:
            fails.append(f'{label}: {name} has no token behind it')
    for name, value in got.items():
        if name.startswith('--') and value != 'initial':
            try:
                L.resolve_css(value, root)
            except (KeyError, ValueError) as err:
                fails.append(f'{label}: {name} does not resolve ({err})')


def theme_selectors(theme):
    a = theme.get('attribute', 'data-oa-theme')
    return {'light': f':root:not([{a}="dark"]), [{a}="light"]',
            'mediaDark': f':root:not([{a}="light"])',
            'dark': f'[{a}="dark"]'}


def norm_sel(sel):
    return ', '.join(x.strip() for x in ' '.join(sel.split()).split(','))


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
    theme = meta.get('theme') or {}
    short_surface = theme.get('shortSurface')
    if not theme:
        fails.append('tokens.json: no root theme record (DR-204)')
    elif short_surface and (short_surface in root or short_surface in {L.css_name(b) for b in bases}):
        fails.append(f'{short_surface}: the ground\'s short name collides with a token or another short name')
    tsel = theme_selectors(theme) if theme else {}
    seen_sel = set()
    seen_theme = []
    for sel, decls in sheet['blocks']:
        if sel == ':root':
            continue
        if theme and norm_sel(sel) in (tsel['light'], tsel['dark']):
            which = 'light' if norm_sel(sel) == tsel['light'] else 'dark'
            seen_theme.append(which)
            s = (theme.get(which) or {}).get('surface')
            if s not in L.SURFACES:
                fails.append(f'theme record: the {which} theme names no known surface ({s})')
                continue
            compare_block(f'{which} theme ({norm_sel(sel)})', decls, surface_want(s, bases, toks, short_surface), root, fails)
            continue
        m = re.fullmatch(r'\.oa-surface-([a-z]+)', sel)
        if not m or m.group(1) not in L.SURFACES:
            fails.append(f'stylesheet: unexpected selector "{sel}"')
            continue
        s = m.group(1)
        seen_sel.add(s)
        compare_block(f'.oa-surface-{s}', decls, surface_want(s, bases, toks, short_surface), root, fails)
    for s in L.SURFACES:
        if s not in seen_sel:
            fails.append(f'stylesheet: no .oa-surface-{s} class')
    if theme:
        for which in ('light', 'dark'):
            if seen_theme.count(which) != 1:
                fails.append(f'stylesheet: expected one {which} theme block ({tsel[which]}), found {seen_theme.count(which)}')
        # the light theme is Newsprint and the dark theme Charcoal (DR-204, from Night Edition, DR-36)
        if (theme.get('light') or {}).get('surface') != 'newsprint' or (theme.get('dark') or {}).get('surface') != 'charcoal':
            fails.append('theme record: DR-204 sets the light theme on Newsprint and the dark theme on Charcoal')
        stats['themes'] = sorted(set(seen_theme))

    # 5. reduced motion
    durations = {L.css_name(p): L.ext(t).get('reducedMotionValue') for p, t in toks.items() if t.get('$type') == 'duration'}
    rm = [(q, inner) for q, inner in sheet['media'] if q.replace(' ', '') == '(prefers-reduced-motion:reduce)']
    dev = (theme.get('followsDevice') or '').replace(' ', '') if theme else ''
    dk = [(q, inner) for q, inner in sheet['media'] if dev and q.replace(' ', '') == dev]
    others = [q for q, _ in sheet['media'] if q.replace(' ', '') not in ('(prefers-reduced-motion:reduce)', dev)]
    if theme:
        # 7. the device's dark setting reaches the root only, and only where the root does not force light
        if len(dk) != 1:
            fails.append(f'stylesheet: expected one {theme.get("followsDevice")} block, found {len(dk)}')
        else:
            inner = dk[0][1]
            if len(inner) != 1 or norm_sel(inner[0][0]) != tsel['mediaDark']:
                fails.append(f'{theme.get("followsDevice")} block: expected a single {tsel["mediaDark"]} rule, so {theme.get("attribute")}="light" wins over the device; '
                             f'found {", ".join(norm_sel(x[0]) for x in inner)}')
            elif (theme.get('dark') or {}).get('surface') in L.SURFACES:
                compare_block(f'dark theme under {theme.get("followsDevice")}', inner[0][1],
                              surface_want(theme['dark']['surface'], bases, toks, short_surface), root, fails)
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
          f'{stats.get("shortNames")} short names per surface class and theme, {len(fails)} failures')
    for f in fails if not a.quiet else fails[:20]:
        print('  FAIL', f)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
