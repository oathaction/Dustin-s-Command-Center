"""Every original-and-proposal pair shown on the Identity Refinement Board.

A variant maps a size key (16, 24, 48, 96, 'display' or 'min') to (inner SVG markup, viewBox).
Size keys are heights in CSS pixels unless a pair sets 'size_by': 'width'.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402

SIZES = [16, 24, 48, 96]
I = o.OUT  # identity proposals folder


def svg_parts(path):
    s = Path(path).read_text()
    vb = o.viewbox(s)
    s = re.sub(r"<title>.*?</title>", "", s)
    inner = s[s.find(">") + 1: s.rfind("</svg>")]
    return inner, vb


def same(path, keys=None):
    v = svg_parts(path)
    return {k: v for k in (keys or SIZES + ["display"])}


def by_size(m):
    """m: dict size_key -> path"""
    return {k: svg_parts(p) for k, p in m.items()}


def sp(name):
    return o.SPRITE / f"{name}.svg"


WM = I / "03-wordmark-masters"


def wordmark_masters(suffix=""):
    disp = WM / (f"20261021_Wordmark-Display-Amp-{suffix}.svg" if suffix else "20261021_Wordmark-Display-Master.svg")
    m16 = WM / (f"20261021_Wordmark-16px-Amp-{suffix}.svg" if suffix else "20261021_Wordmark-16px-Master.svg")
    m24 = WM / (f"20261021_Wordmark-24px-Amp-{suffix}.svg" if suffix else "20261021_Wordmark-24px-Master.svg")
    return by_size({16: m16, 24: m24, 48: disp, 96: disp, "display": disp})


def prussian_variant(kind):
    """Wordmark on Prussian with one of four ampersand treatments, as markup with CSS hooks."""
    inner, vb = svg_parts(sp("wordmark"))
    if kind == "keyline":
        inner = inner.replace('<g fill="var(--amp,#E63946)">',
                              '<g fill="var(--amp,#E63946)" stroke="#DCD9D2" stroke-width="2" paint-order="stroke" stroke-linejoin="round">')
        inner = inner.replace('transform="translate(365.5 104) scale(0.14 -0.14)"', 'transform="translate(365.5 104) scale(0.14 -0.14)" vector-effect="non-scaling-stroke"')
    return {k: (inner, vb) for k in SIZES + ["display"]}


def pairs():
    P = []
    # ---- 1 re-exports
    P.append({"panel": 1, "id": "p01-amp", "label": "Master ampersand, #amp", "display": 240, "overlay": "common",
              "orig": same(sp("amp")), "prop": same(I / "01-reexport/20261021_Amp-Master-Reexported.svg"), "glyph": "amp"})
    P.append({"panel": 1, "id": "p01-stacked", "label": "Stacked lockup L2, #stacked", "display": 200, "overlay": "common",
              "orig": same(sp("stacked")), "prop": same(I / "01-reexport/20261021_Stacked-L2-Reexported.svg")})
    for n, f, lab in (("tl-1", "Tagline-1-Line", "Tagline, one line, #tl-1"), ("tl-2a", "Tagline-2-Line-A", "Tagline, first of two lines, #tl-2a"),
                      ("tl-2b", "Tagline-2-Line-B", "Tagline, second of two lines, #tl-2b"), ("url-1", "Url-1", "Web address, #url-1")):
        P.append({"panel": 1, "id": f"p01-{n}", "label": lab, "display": 40, "overlay": "common", "modes": ["mono"],
                  "orig": same(sp(n)), "prop": same(I / f"01-reexport/20261021_{f}-Reexported.svg")})
    # ---- 2 hinge gaps
    P.append({"panel": 2, "id": "p02-literal", "label": "Hinge gaps at the stated 0.10x, nearest ink", "display": 120, "overlay": "left",
              "orig": same(sp("wordmark")), "prop": same(I / "02-hinge-gaps/20261021_Wordmark-Hinge-Literal-0.10x.svg")})
    P.append({"panel": 2, "id": "p02-optical", "label": "Hinge gaps by equal white area (recommended)", "display": 120, "overlay": "left",
              "orig": same(sp("wordmark")), "prop": same(I / "02-hinge-gaps/20261021_Wordmark-Hinge-Optical.svg")})
    # ---- 3 wordmark masters
    P.append({"panel": 3, "id": "p03-masters", "label": "Wordmark: 16 px master at 16, 24 px master at 24, display master from 48 up", "display": 120,
              "overlay": "left", "orig": same(sp("wordmark")), "prop": wordmark_masters()})
    # ---- 4 ampersand A
    P.append({"panel": 4, "id": "p04-amp", "label": "Freestanding ampersand: 16 px master at 16, display tune from 24 up", "display": 280, "overlay": "left",
              "orig": same(sp("amp")), "prop": by_size({16: I / "04-amp-a/20261021_Amp-A-Small-Master-16px.svg", 24: I / "04-amp-a/20261021_Amp-A-Display-Tune.svg",
                                                         48: I / "04-amp-a/20261021_Amp-A-Display-Tune.svg", 96: I / "04-amp-a/20261021_Amp-A-Display-Tune.svg",
                                                         "display": I / "04-amp-a/20261021_Amp-A-Display-Tune.svg"}), "glyph": "amp"})
    P.append({"panel": 4, "id": "p04-wordmark", "label": "Wordmark carrying option A", "display": 120, "overlay": "left",
              "orig": same(sp("wordmark")), "prop": wordmark_masters("A")})
    # ---- 5 ampersand B
    P.append({"panel": 5, "id": "p05-amp", "label": "Freestanding ampersand: 16 px master at 16, drawn master from 24 up", "display": 280, "overlay": "left",
              "orig": same(sp("amp")), "prop": by_size({16: I / "05-amp-b/20261021_Amp-B-Small-Master-16px.svg", 24: I / "05-amp-b/20261021_Amp-B-Drawn-Master.svg",
                                                         48: I / "05-amp-b/20261021_Amp-B-Drawn-Master.svg", 96: I / "05-amp-b/20261021_Amp-B-Drawn-Master.svg",
                                                         "display": I / "05-amp-b/20261021_Amp-B-Drawn-Master.svg"}), "glyph": "amp"})
    P.append({"panel": 5, "id": "p05-wordmark", "label": "Wordmark carrying option B", "display": 120, "overlay": "left",
              "orig": same(sp("wordmark")), "prop": wordmark_masters("B")})
    # ---- 6 condensed
    C = I / "06-condensed"
    P.append({"panel": 6, "id": "p06-c75", "label": "Condensed, 7.5 to 1 (chosen by the 16 px test), against the current proportions at the same height", "display": 120,
              "overlay": "left", "orig": wordmark_masters(),
              "prop": by_size({16: C / "20261021_Wordmark-Condensed-7-5-To-1-16px.svg", 24: C / "20261021_Wordmark-Condensed-7-5-To-1-24px.svg",
                               48: C / "20261021_Wordmark-Condensed-7-5-To-1-Display.svg", 96: C / "20261021_Wordmark-Condensed-7-5-To-1-Display.svg",
                               "display": C / "20261021_Wordmark-Condensed-7-5-To-1-Display.svg"})})
    P.append({"panel": 6, "id": "p06-c60", "label": "Condensed, 6 to 1 (drawn for comparison, display master only)", "display": 120, "overlay": "left",
              "orig": wordmark_masters(), "prop": same(C / "20261021_Wordmark-Condensed-6-0-To-1-Display.svg")})
    # ---- 7 hinge
    H = I / "07-hinge"
    P.append({"panel": 7, "id": "p07-hinge", "label": "Hinge: compact master below 526 px wide, display master above", "display": 200, "overlay": "left",
              "orig": same(sp("hinge")), "prop": by_size({16: H / "20261021_Hinge-Compact-Master.svg", 24: H / "20261021_Hinge-Compact-Master.svg",
                                                           48: H / "20261021_Hinge-Compact-Master.svg", 96: H / "20261021_Hinge-Compact-Master.svg",
                                                           "display": H / "20261021_Hinge-Display-Master.svg"})})
    # ---- 8 lockmark
    L = I / "08-lockmark"
    P.append({"panel": 8, "id": "p08-lockmark", "label": "Lockmark: 16 and 24 px masters, V5 master from 48 up", "display": 240, "overlay": "left",
              "orig": same(sp("lockmark")), "prop": by_size({16: L / "20261021_Lockmark-16px-Master.svg", 24: L / "20261021_Lockmark-24px-Master.svg",
                                                              48: sp("lockmark"), 96: sp("lockmark"), "display": sp("lockmark")})})
    # ---- 10 Prussian
    for kind, lab, style in (("display-only", "A. Red at display size only: one colour below 48 px", "displayonly"),
                             ("newsprint", "B. Newsprint ampersand, White letters", "newsprint"),
                             ("keyline", "C. Red with a 1 px Newsprint keyline", "keyline"),
                             ("mono", "D. One colour, all White", "mono")):
        P.append({"panel": 10, "id": f"p10-{kind}", "label": lab, "display": 120, "overlay": None, "surfaces": ["prussian"],
                  "orig": same(sp("wordmark")), "prop": prussian_variant(kind), "prop_style": style})
    return P
