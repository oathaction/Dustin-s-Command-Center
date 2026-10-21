"""Color math for the Oath & Action V6 token work (Phase 1).

Self-contained, standard library only, so it runs with `python3 -I`.
Imported by nothing: other Phase 1 scripts copy what they need, because
`-I` drops the script folder from sys.path.

WCAG 2.x relative luminance and contrast ratio, and OKLab / OKLCH
conversion (Bjorn Ottosson's matrices, as used by CSS Color 4).
"""

import math

PALETTE = {
    "newsprint": "#DCD9D2",
    "charcoal": "#121212",
    "pillarRed": "#E63946",
    "prussian": "#1F2D5A",
    "stone": "#5D636D",
    "verdigris": "#4A7C74",
    "white": "#FFFFFF",
}
SURFACES = ["newsprint", "white", "charcoal", "prussian"]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(min(1, max(0, c)) * 255):02X}" for c in rgb)


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def delin(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(h):
    r, g, b = (lin(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def to_oklab(h):
    r, g, b = (lin(c) for c in hex_to_rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def oklab_to_linear(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklab_to_hex(L, a, b):
    rl = oklab_to_linear(L, a, b)
    in_gamut = all(-1e-6 <= c <= 1 + 1e-6 for c in rl)
    return rgb_to_hex(tuple(delin(min(1, max(0, c))) for c in rl)), in_gamut


ACHROMATIC = 1e-4  # chroma below this makes hue powerless (CSS Color 4)


def to_oklch(h):
    L, a, b = to_oklab(h)
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360 if C >= ACHROMATIC else None
    return L, C, H


def mix_oklch(base, toward, t):
    """CSS color-mix(in oklch, base (1-t), toward t), shorter hue arc."""
    L1, C1, H1 = to_oklch(base)
    L2, C2, H2 = to_oklch(toward)
    L = L1 + (L2 - L1) * t
    C = C1 + (C2 - C1) * t
    if H1 is None and H2 is None:
        H = 0.0
    elif H1 is None:
        H = H2
    elif H2 is None:
        H = H1
    else:
        d = (H2 - H1) % 360
        if d > 180:
            d -= 360
        H = (H1 + d * t) % 360
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    return oklab_to_hex(L, a, b)


def mix_oklab(base, toward, t):
    """CSS color-mix(in oklab, base (1-t), toward t)."""
    p, q = to_oklab(base), to_oklab(toward)
    return oklab_to_hex(*(x + (y - x) * t for x, y in zip(p, q)))


def over(fg, bg, alpha):
    """Composite fg at alpha over bg in sRGB (how browsers blend opacity)."""
    f, b = hex_to_rgb(fg), hex_to_rgb(bg)
    return rgb_to_hex(tuple(fc * alpha + bc * (1 - alpha) for fc, bc in zip(f, b)))


def delta_e_ok(a, b):
    return math.dist(to_oklab(a), to_oklab(b))
