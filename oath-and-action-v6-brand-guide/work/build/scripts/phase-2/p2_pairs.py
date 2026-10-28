"""Every V5-and-new pair on the Identity Masters Board.

A variant maps a size key (16, 24, 48, 96 or 'display') to (inner SVG markup, viewBox). Sizes are
heights in CSS px. Each new variant uses the master that serves that size under the I8 rule.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402

SIZES = [16, 24, 48, 96]
A = P.ASSETS


def sp(name):
    return o.SPRITE / f"{name}.svg"


def same(path):
    v = P.svg_parts(path)
    return {k: v for k in SIZES + ["display"]}


def by_size(m):
    return {k: P.svg_parts(p) for k, p in m.items()}


def masters(m16, m24, disp):
    return by_size({16: m16, 24: m24, 48: disp, 96: disp, "display": disp})


WM = masters(A / "wordmark/20261028_Wordmark-16px-Master.svg", A / "wordmark/20261028_Wordmark-24px-Master.svg", A / "wordmark/20261028_Wordmark-Display-Master.svg")
WMC = masters(A / "wordmark-condensed/20261028_Wordmark-Condensed-16px-Master.svg", A / "wordmark-condensed/20261028_Wordmark-Condensed-24px-Master.svg",
              A / "wordmark-condensed/20261028_Wordmark-Condensed-Display-Master.svg")
AMPB = masters(A / "ampersand/20261028_Amp-B-16px-Master.svg", A / "ampersand/20261028_Amp-B-24px-Master.svg", A / "ampersand/20261028_Amp-B-Display-Master.svg")
AMPN = masters(A / "ampersand/20261028_Amp-B-Narrow-16px-Master.svg", A / "ampersand/20261028_Amp-B-Narrow-24px-Master.svg", A / "ampersand/20261028_Amp-B-Narrow-Display-Master.svg")
V5AMP = by_size({16: sp("amp-16"), 24: sp("amp"), 48: sp("amp"), 96: sp("amp"), "display": sp("amp")})
P1B = o.OUT / "05-amp-b"
P1AMPB = by_size({16: P1B / "20261021_Amp-B-Small-Master-16px.svg", 24: P1B / "20261021_Amp-B-Drawn-Master.svg", 48: P1B / "20261021_Amp-B-Drawn-Master.svg",
                  96: P1B / "20261021_Amp-B-Drawn-Master.svg", "display": P1B / "20261021_Amp-B-Drawn-Master.svg"})
P1C = o.OUT / "06-condensed"
P1COND = by_size({16: P1C / "20261021_Wordmark-Condensed-7-5-To-1-16px.svg", 24: P1C / "20261021_Wordmark-Condensed-7-5-To-1-24px.svg",
                  48: P1C / "20261021_Wordmark-Condensed-7-5-To-1-Display.svg", 96: P1C / "20261021_Wordmark-Condensed-7-5-To-1-Display.svg",
                  "display": P1C / "20261021_Wordmark-Condensed-7-5-To-1-Display.svg"})
LK = A / "lockups"
HG = A / "hinge"
BADGE = masters(A / "badge/20261028_Hinge-Badge-16px-Master.svg", A / "badge/20261028_Hinge-Badge-24px-Master.svg", A / "badge/20261028_Hinge-Badge-Display-Master.svg")
P1BADGE = o.ROOT / "work/boards/phase-1/symbols/badge"
P1BADGES = masters(P1BADGE / "20261021_Hinge-Badge-16px-Master.svg", P1BADGE / "20261021_Hinge-Badge-24px-Master.svg", P1BADGE / "20261021_Hinge-Badge-Display-Master.svg")


def pairs():
    Q = []
    R = A / "reexport"
    Q.append({"item": "I1", "id": "i1-amp", "label": "Master ampersand, #amp (V5's Lora glyph, kept for the A fallback)", "display": 200, "overlay": "common",
              "orig": same(sp("amp")), "prop": same(R / "20261028_Amp-V5-Lora-Master-Reexported.svg"), "glyph": "amp", "olab": "V5 as shipped", "plab": "Re-exported"})
    Q.append({"item": "I1", "id": "i1-stacked", "label": "Stacked lockup L2, #stacked (V5 geometry)", "display": 160, "overlay": "common",
              "orig": same(sp("stacked")), "prop": same(R / "20261028_Stacked-L2-V5-Reexported.svg"), "olab": "V5 as shipped", "plab": "Re-exported"})
    for n, f, lab in (("tl-1", "Tagline-1-Line", "Tagline, one line, #tl-1"), ("tl-2a", "Tagline-2-Line-A", "Tagline, first of two lines, #tl-2a"),
                      ("tl-2b", "Tagline-2-Line-B", "Tagline, second of two lines, #tl-2b"), ("url-1", "Url-1", "Web address, #url-1")):
        Q.append({"item": "I1", "id": f"i1-{n}", "label": lab, "display": 40, "overlay": "common", "modes": ["mono"],
                  "orig": same(sp(n)), "prop": same(R / f"20261028_{f}-Reexported.svg"), "olab": "V5 as shipped", "plab": "Re-exported"})
    Q.append({"item": "I2", "id": "i2-hinge", "label": "Hinge gaps by equal white area, display master", "display": 120, "overlay": "left",
              "orig": same(sp("wordmark")), "prop": same(A / "wordmark/20261028_Wordmark-Display-Master.svg"), "olab": "V5", "plab": "Phase 2"})
    Q.append({"item": "I4", "id": "i4-amp", "label": "Ampersand B: 16 px master at 16, 24 px master at 24, display master from 48", "display": 280, "overlay": "left",
              "orig": V5AMP, "prop": AMPB, "glyph": "amp", "olab": "V5", "plab": "B, refined"})
    Q.append({"item": "I4", "id": "i4-p1", "label": "Ampersand B, Phase 1 drawing against the refinement", "display": 280, "overlay": "left",
              "orig": P1AMPB, "prop": AMPB, "glyph": "amp", "olab": "B, Phase 1", "plab": "B, refined", "surfaces": ["newsprint", "charcoal"]})
    Q.append({"item": "I4", "id": "i4-narrow", "label": "Narrow B for the condensed wordmark: its own 16 and 24 px masters", "display": 280, "overlay": "left",
              "orig": V5AMP, "prop": AMPN, "glyph": "amp", "olab": "V5", "plab": "Narrow B"})
    Q.append({"item": "I3", "id": "i3-wordmark", "label": "Wordmark: 16 px master at 16, 24 px master at 24, display master from 48", "display": 120, "overlay": "left",
              "orig": same(sp("wordmark")), "prop": WM, "olab": "V5", "plab": "Phase 2"})
    Q.append({"item": "I5", "id": "i5-l1", "label": "L1 wordmark: today's width against the condensed drawing at 7.5 to 1", "display": 120, "overlay": None,
              "orig": WM, "prop": WMC, "olab": "Today's width", "plab": "Condensed"})
    Q.append({"item": "I5", "id": "i5-p1", "label": "Condensed: the Phase 1 exploration against the drawing pass", "display": 120, "overlay": "left",
              "orig": P1COND, "prop": WMC, "olab": "Phase 1", "plab": "Phase 2", "surfaces": ["newsprint", "charcoal"]})
    for lk, nm, disp in (("L2", "Stacked", 160), ("L3", "Horizontal", 120), ("L8", "Monogram", 120)):
        Q.append({"item": "I5", "id": f"i5-{lk.lower()}", "label": f"{lk} {nm.lower()}: today's width against the condensed drawing", "display": disp, "overlay": None,
                  "orig": same(LK / f"20261028_{lk}-{nm}-Master.svg"), "prop": same(LK / f"20261028_{lk}-{nm}-Condensed-Master.svg"), "olab": "Today's width", "plab": "Condensed"})
    for lk, sym, nm in (("L2", "stacked", "Stacked"), ("L3", "l3", "Horizontal"), ("L8", "monogram", "Monogram")):
        Q.append({"item": "I5", "id": f"i5-v5{lk.lower()}", "label": f"{lk} {nm.lower()}: V5 against Phase 2 at today's width", "display": 120 if lk != "L2" else 160, "overlay": None,
                  "orig": same(sp(sym)), "prop": same(LK / f"20261028_{lk}-{nm}-Master.svg"), "olab": "V5", "plab": "Phase 2"})
    comp = HG / "20261028_Hinge-Diagram-V2-Compact-Master.svg"
    Q.append({"item": "I6", "id": "i6-hinge", "label": "Hinge diagram V2: compact master below 533 px wide, display master above", "display": 200, "overlay": None,
              "orig": same(sp("hinge")), "prop": by_size({16: comp, 24: comp, 48: comp, 96: comp, "display": HG / "20261028_Hinge-Diagram-V2-Display-Master.svg"}),
              "olab": "V5", "plab": "V2, today's width"})
    compc = HG / "20261028_Hinge-Diagram-V2-Compact-Condensed-Master.svg"
    Q.append({"item": "I6", "id": "i6-cond", "label": "Hinge diagram V2 with the condensed OATH and ACTION", "display": 200, "overlay": None,
              "orig": by_size({16: comp, 24: comp, 48: comp, 96: comp, "display": HG / "20261028_Hinge-Diagram-V2-Display-Master.svg"}),
              "prop": by_size({16: compc, 24: compc, 48: compc, 96: compc, "display": HG / "20261028_Hinge-Diagram-V2-Display-Condensed-Master.svg"}),
              "olab": "Today's width", "plab": "Condensed"})
    L = A / "lockmark"
    Q.append({"item": "I7", "id": "i7-lockmark", "label": "Lockmark: 16 and 24 px masters, V5's master from 48", "display": 200, "overlay": "left",
              "orig": same(sp("lockmark")), "prop": masters(L / "20261028_Lockmark-16px-Master.svg", L / "20261028_Lockmark-24px-Master.svg", L / "20261028_Lockmark-Master-V5.svg"),
              "olab": "V5", "plab": "Phase 2"})
    Q.append({"item": "S9", "id": "s9-badge", "label": "Hinge-circle badge: the Phase 1 drawing against the Phase 2 masters", "display": 200, "overlay": "left",
              "orig": P1BADGES, "prop": BADGE, "glyph": "amp", "olab": "Phase 1 (no V5 mark)", "plab": "Phase 2"})
    return Q
