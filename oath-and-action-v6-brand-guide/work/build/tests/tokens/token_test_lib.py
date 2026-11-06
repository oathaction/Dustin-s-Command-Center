"""Shared helpers for the Oath & Action token tests (parity, rules, self-test).

Standard library only, so every test runs with `python3 -I`. Nothing here is shared with the generator
(work/build/scripts/phase-2/tokens_build.mjs): the color math, the alias resolution, the CSS naming and
the CSS reading are written out again on purpose, so a mistake in the generator cannot hide itself.
The color math follows work/build/scripts/phase-1/token_rule_test.py (WCAG 2.x contrast; OKLab per
Ottosson, as CSS Color 4 uses it).
"""

import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
TOKENS_DIR = ROOT / 'work/build/tokens'
NS = 'org.oathandaction'
SURFACES = ['newsprint', 'white', 'charcoal', 'prussian']
SURFACE_KEYS = {'onNewsprint': 'newsprint', 'onWhite': 'white', 'onCharcoal': 'charcoal', 'onPrussian': 'prussian'}
KEY_OF = {v: k for k, v in SURFACE_KEYS.items()}
LOCKED = {'newsprint': '#DCD9D2', 'charcoal': '#121212', 'pillarRed': '#E63946', 'prussian': '#1F2D5A',
          'stone': '#5D636D', 'verdigris': '#4A7C74', 'white': '#FFFFFF'}
ALIAS = re.compile(r'^\{([^{}]+)\}$')


# --- color math -------------------------------------------------------------------------------------
def rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    r, g, b = map(_lin, rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = sorted((_lum(a), _lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def oklab(h):
    r, g, b = map(_lin, rgb(h))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s]


def oklch(h):
    L, a, b = oklab(h)
    C = math.hypot(a, b)
    return L, C, (math.degrees(math.atan2(b, a)) % 360)


def _hex(L, a, b):
    l, m, s = ((L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3,
               (L - 0.0894841775 * a - 1.2914855480 * b) ** 3)
    out = []
    for c in (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
              -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
              -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s):
        c = min(1, max(0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        out.append(f'{round(c * 255):02X}')
    return '#' + ''.join(out)


def mix_oklab(base, toward, t):
    p, q = oklab(base), oklab(toward)
    return _hex(*(x + (y - x) * t for x, y in zip(p, q)))


def hue_gap(h1, h2):
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


# --- the token tree -----------------------------------------------------------------------------------
def load_json(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def flatten(tree):
    """path -> token dict, in document order, with $type inherited from groups (DTCG 5.2.2)."""
    out = {}

    def walk(node, path, inherited):
        typ = node.get('$type', inherited)
        for k, v in node.items():
            if k.startswith('$') or not isinstance(v, dict):
                continue
            p = path + [k]
            if '$value' in v:
                t = dict(v)
                t.setdefault('$type', typ)
                if t['$type'] is None and isinstance(v['$value'], str):
                    t['$type'] = None
                out['.'.join(p)] = t
            else:
                walk(v, p, typ)
    walk(tree, [], None)
    return out


def ext(t):
    return ((t or {}).get('$extensions') or {}).get(NS, {})


def root_meta(tree):
    return ((tree.get('$extensions') or {}).get(NS)) or {}


def alias_target(v):
    m = ALIAS.match(v) if isinstance(v, str) else None
    return m.group(1) if m else None


def resolve(path, toks, seen=()):
    """Follow aliases to the token with an explicit value. Returns (path, value); raises on a break."""
    if path in seen:
        raise ValueError('alias cycle: ' + ' > '.join(seen + (path,)))
    if path not in toks:
        raise KeyError(f'{seen[-1] if seen else "?"} points to missing {path}')
    v = toks[path]['$value']
    tgt = alias_target(v)
    if tgt:
        return resolve(tgt, toks, seen + (path,))
    return path, v


def chain(path, toks):
    """Every path on the alias chain, starting with path itself."""
    out = [path]
    while True:
        tgt = alias_target(toks[out[-1]]['$value'])
        if not tgt or tgt not in toks or tgt in out:
            return out
        out.append(tgt)


def ref_hex(ref, toks):
    tgt = alias_target(ref)
    if not tgt:
        raise KeyError(f'"{ref}" is not a reference')
    return resolve(tgt, toks)[1]['hex']


def resolved_type(path, toks):
    t = toks[path]
    if t.get('$type'):
        return t['$type']
    tgt = alias_target(t['$value'])
    return resolved_type(tgt, toks) if tgt and tgt in toks else None


def css_name(path):
    return '--' + '-'.join(re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', seg).lower() for seg in path.split('.'))


def surface_of(path, t):
    return ext(t).get('surface') or SURFACE_KEYS.get(path.split('.')[-1])


# --- the stylesheet ------------------------------------------------------------------------------------
def _strip_comments(text):
    return re.sub(r'/\*.*?\*/', '', text, flags=re.S)


def _blocks(text):
    """Top-level (prelude, body) pairs, with nested braces kept in body."""
    out, i, n = [], 0, len(text)
    while i < n:
        j = text.find('{', i)
        if j < 0:
            if text[i:].strip():
                out.append((text[i:].strip(), None))
            break
        prelude = text[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {'{': 1, '}': -1}.get(text[k], 0)
            k += 1
        out.append((prelude, text[j + 1:k - 1]))
        i = k
    return out


def _decls(body):
    out = []
    for part in body.split(';'):
        if not part.strip():
            continue
        if ':' not in part:
            out.append((part.strip(), None))
            continue
        name, value = part.split(':', 1)
        out.append((name.strip(), ' '.join(value.split())))
    return out


def parse_css(text):
    """Read tokens.css into {'header', 'blocks': [(selector, [(prop, value)])], 'media': [(query, [(selector, decls)])]}."""
    m = re.match(r'\s*/\*(.*?)\*/', text, flags=re.S)
    header = m.group(1) if m else ''
    clean = _strip_comments(text)
    blocks, media = [], []
    for prelude, body in _blocks(clean):
        if body is None:
            blocks.append((prelude, None))
        elif prelude.startswith('@media'):
            media.append((prelude[len('@media'):].strip(), [(p, _decls(b)) for p, b in _blocks(body)]))
        else:
            blocks.append((prelude, _decls(body)))
    return {'header': header, 'blocks': blocks, 'media': media}


VAR = re.compile(r'var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,[^()]*)?\)')


def resolve_css(value, props, seen=()):
    """Substitute var() references from props until none remain. Raises on a missing name or a cycle."""
    def sub(m):
        name = m.group(1)
        if name in seen:
            raise ValueError('var() cycle: ' + ' > '.join(seen + (name,)))
        if name not in props:
            raise KeyError(f'var({name}) has no declaration')
        return resolve_css(props[name], props, seen + (name,))
    prev = None
    while prev != value:
        prev = value
        value = VAR.sub(sub, value)
    return value


NUM = re.compile(r'(?<![\w-])-?\d*\.?\d+')
HEX = re.compile(r'#[0-9a-f]{6}\b')


def norm(value):
    """Canonical form for comparing two resolved CSS values: lower case, single spaces, numbers to six
    places. Hex colors are kept whole."""
    v = ' '.join(str(value).lower().split())
    v = re.sub(r'\s*,\s*', ', ', v)
    v = re.sub(r'\s*/\s*', '/', v)

    def fix(m):
        x = float(m.group(0))
        s = f'{round(x, 6):.6f}'.rstrip('0').rstrip('.')
        return '0' if s in ('-0', '') else s
    parts = re.split(r'(#[0-9a-f]{6}\b)', v)
    return ''.join(p if HEX.fullmatch(p) else NUM.sub(fix, p) for p in parts)
