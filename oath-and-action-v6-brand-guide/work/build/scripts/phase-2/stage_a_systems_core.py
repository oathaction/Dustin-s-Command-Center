"""Shared measurement and markup helpers for the systems designer's chapters (05 Color, 06 Type, 07 Layout and
spacing) on stage board A, November 6, 2026.

Every figure a chapter prints comes from these functions, run on the token values in
work/build/tokens/tokens.json (the engineer's generated file, read and never edited). Until that file exists, pass
--tokens <path> to read a copy written by the engineer's own builder.

Color math: WCAG 2.x relative luminance and contrast; OKLab per Ottosson (CSS Color 4); color-vision simulation per
Machado, Oliveira and Fernandes 2009 at severity 1.0 in linear sRGB, the palette lab's method (D2-95).
"""
import html
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
TOKENS_JSON = ROOT / 'work/build/tokens/tokens.json'
TOKENS_CSS = ROOT / 'work/build/tokens/tokens.css'

MINUS = '−'
NBSP = ' '


# ------------------------------------------------------------------------------------------------ tokens
class Tokens:
    def __init__(self, json_path, css_path):
        self.json_path = pathlib.Path(json_path)
        self.css_path = pathlib.Path(css_path)
        self.data = json.loads(self.json_path.read_text())
        self.css = self.css_path.read_text()
        self.css_names = set(re.findall(r'(--oa-[a-z0-9-]+)\s*:', self.css))
        self.used = set()

    def node(self, path):
        n = self.data
        for k in path.split('.'):
            n = n[k]
        return n

    def value(self, path):
        v = self.node(path)['$value']
        if isinstance(v, str) and v.startswith('{') and v.endswith('}'):
            return self.value(v[1:-1])
        return v

    def hex(self, path):
        v = self.value(path)
        if isinstance(v, dict) and 'hex' in v:
            return v['hex'].upper()
        raise ValueError(f'{path} is not a color: {v!r}')

    def alias(self, path):
        """The token a semantic token points at, one step down, as a dot path (or None)."""
        v = self.node(path)['$value']
        if isinstance(v, str) and v.startswith('{'):
            return v[1:-1]
        return None

    def ext(self, path):
        return self.node(path).get('$extensions', {}).get('org.oathandaction', {})

    def dim(self, path):
        v = self.value(path)
        return v['value'], v['unit']

    def px(self, path, root=16):
        val, unit = self.dim(path)
        return val * root if unit == 'rem' else val

    def var(self, path):
        """CSS custom property for a token path, checked against tokens.css."""
        name = css_name(path)
        if name not in self.css_names:
            raise KeyError(f'{name} (from {path}) is not in {self.css_path}')
        self.used.add(path)
        return f'var({name})'

    def exists(self, path):
        try:
            self.node(path)
            return True
        except KeyError:
            return False


def css_name(path):
    segs = path.split('.')
    out = []
    for s in segs:
        s = re.sub(r'(?<=[a-z0-9])([A-Z])', r'-\1', s).lower()
        out.append(s)
    return '--' + '-'.join(out)


# ------------------------------------------------------------------------------------------------ color math
def rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def to_hex(c):
    return '#' + ''.join(f'{max(0, min(255, round(v))):02X}' for v in c)


def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def delin(c):
    c = max(0.0, min(1.0, c))
    return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def luminance(h):
    r, g, b = (lin(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = sorted([luminance(a), luminance(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


def ratio_txt(a, b):
    """A ratio as the guide prints it, two decimals, rounded half up from the unrounded value."""
    return f'{math.floor(contrast(a, b) * 100 + 0.5) / 100:.2f}'


def passes(a, b, need):
    return contrast(a, b) >= need


def oklab(h):
    r, g, b = (lin(c) for c in rgb(h))
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l_, m_, s_))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def from_oklab(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bb = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return to_hex([delin(r), delin(g), delin(bb)])


def mix_oklab(a, b, t):
    A, B = oklab(a), oklab(b)
    return from_oklab(*[x + (y - x) * t for x, y in zip(A, B)])


def delta_ok(a, b):
    return math.dist(oklab(a), oklab(b))


def composite(fg, bg, alpha):
    """fg at alpha over bg, composited in sRGB as browsers paint it."""
    return to_hex([alpha * f + (1 - alpha) * g for f, g in zip(rgb(fg), rgb(bg))])


def css_gray(h):
    """What CSS filter: grayscale(1) paints: luminance weights on the encoded values."""
    r, g, b = rgb(h)
    v = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return to_hex([v, v, v])


CVD = {
    'protanopia': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    'deuteranopia': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    'tritanopia': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simulate(h, kind):
    r, g, b = (lin(c) for c in rgb(h))
    m = CVD[kind]
    return to_hex([delin(m[i][0] * r + m[i][1] * g + m[i][2] * b) for i in range(3)])


# ------------------------------------------------------------------------------------------------ copy
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']
WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def num(n):
    """Numbers under ten in words, in prose (H06)."""
    return WORDS[n] if 0 <= n < 10 else f'{n:,}'


def signed(v, decimals=0, thousands=True):
    s = f'{abs(v):,.{decimals}f}' if thousands else f'{abs(v):.{decimals}f}'
    if v < 0:
        return MINUS + s
    return s


def esc(s):
    return html.escape(str(s), quote=True)


EM_DASH = '—'
EN_DASH = '–'


def check_copy(s, where):
    """Fail on marks the house rules forbid in every word we write here."""
    bad = []
    s_full = s
    s = re.sub(r'<code>.*?</code>', '', s, flags=re.S)
    if EM_DASH in s:
        bad.append('em dash')
    if EN_DASH in s:
        bad.append('en dash')
    if re.search(r"(?<![=\w])'(?=[A-Za-z])|(?<=[a-z])'(?=[a-z])", re.sub(r'<[^>]+>', '', s)):
        bad.append('straight apostrophe or quote')
    if re.search(r'"[A-Za-z]', re.sub(r'<[^>]+>', '', s)):
        bad.append('straight double quote')
    for w in ('genuinely', 'really', 'truly', 'actually', 'leverage', 'underscore', 'simply', 'just '):
        if re.search(r'\b' + w.strip() + r'\b', re.sub(r'<[^>]+>', '', s), re.I) and w != 'just ':
            bad.append(f'"{w}"')
    if bad:
        raise ValueError(f'{where}: {", ".join(bad)} in: {s[:160]}')
    return s_full
