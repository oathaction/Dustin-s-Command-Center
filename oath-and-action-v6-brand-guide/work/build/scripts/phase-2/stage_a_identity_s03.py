"""Chapter 03 Identity: specimens. Each function returns one specimen record (see stage_a_identity_build.py).

Fix pass, November 6, 2026: codes and internal names leave the plates and alt text (D2-253); the lockup sheet runs as
two columns at 712 px with L6 in its own plate (C-S7); the minimum-size table is readable to assistive technology and
shows today's width only (AX-M1, BE-S11); marks in the minimum sheet share one bottom line (C-S13); the masthead's
navigation is a div (AX-S8); the partnership lockup shows both orders (RP-S3, DR-102); type on fixed artboards follows
D2-254, and labeled failures that must sit off the scale carry check_exempt "scale".

Apply pass, November 7, 2026: S1 replaces L2 in the lockup sheet, the minimum sheet and table, and the surfaces sheet
(DR-113); the badge shows at its new 48 px minimum (DR-118); the minimum table leaves out retired rows and condensed
figures (DR-115, D2-328).

Q1 to Q4 pass, November 8, 2026: L3's masthead form places its new master, the lockmark at 48 px from its 48 px master
on whole pixels (DR-131); L6 draws without its four pillar dots (DR-129).

Promotion, November 10, 2026: L6 draws its wordmark and tagline centered on the strip (DR-182); L3 places the masthead
master that carries the rebuilt 48 px lockmark, and the minimum form draws the rebuilt 24 px master (DR-181)."""
import json
import re
import stage_a_identity_lib as LIB
from stage_a_identity_lib import (E, ID_DIR, WM, WMC, L2, L3, L8, LOCK, AMP, BADGE, HINGE, TL1, TL2A, TL2B, fragment, mark, s1, s1_width,
                                  wordmark, lockmark, amp, illus, head_label, tag, svg_file, mark_style, ink, ink2, hair, pal,
                                  tv, sig, ty, curl)

S = []


def spec(fn):
    S.append(fn)
    return fn


def rec(sid, rule, width, alt, body, *, illustrative=False, notes="", cls="", css="", role_img=None, chapter="03", **meta):
    """One specimen record. width None lets the shell flow the stage (a sheet whose marks carry their own sizes, or a
    table). meta carries the shell's newer manifest keys: readable, interactive, scale, fit_switch, check_exempt."""
    return {"id": sid, "chapter": chapter, "rule": rule, "width_px": width, "alt": curl(" ".join(alt.split())),
            "illustrative": illustrative, "notes": notes, "meta": meta,
            "html": fragment(sid, body, cls=cls, extra_css=css, role_img=role_img)}


def scroll(inner, label=""):
    """A wide part of a specimen. The shell's mat scrolls the whole plate sideways when it is wider than the screen,
    so the specimen itself holds no scrolling region (a focusable region inside an image would trap keyboard users)."""
    return f'<div class="oai-wide">{inner}</div>'


def markrow(items, height, gap=32):
    """A row of marks that share one bottom line, each with its tags under it (C-S13). items: (mark html, tags)."""
    cells = "".join(f'<div class="oai-mr-cell"><div class="oai-mr-box" style="height:{height}px">{m}</div>'
                    + "".join(f'<span class="oai-tag">{E(t)}</span>' for t in tags) + '</div>' for m, tags in items)
    return f'<div class="oai-mr" style="gap:24px {gap}px">{cells}</div>'


MARKROW_CSS = (".oai-mr{display:flex;flex-wrap:wrap;align-items:flex-start}"
               ".oai-mr-cell{display:flex;flex-direction:column;gap:6px;align-items:flex-start}"
               ".oai-mr-box{display:flex;align-items:flex-end}")


# ------------------------------------------------------------------------------------------- lockup assembly
def l3_small(master16or24=24, width="today", surface="newsprint", label="Oath & Action, L3 horizontal lockup", hang=False):
    """L3 at small sizes. 24: the masthead form, placed from L3's masthead master (DR-131): the 24 px wordmark master
    (221 px, 22 px capitals), 13 px and the lockmark's 48 px master at 48 px, centered on the wordmark's box, 282 by
    48 px on whole pixels. 16: the minimum form, built here: the 16 px wordmark master (152 px, 14 px capitals), 8 px and
    the lockmark at 34 px from its 24 px master. hang=True lets the lockmark hang above and below the wordmark's box, so
    the lockup's box is the wordmark's and its baseline lines up with other marks."""
    files = WM if width == "today" else WMC
    if master16or24 == 24 and width == "today":
        m = mark(L3["masthead"], h=48, surface=surface, decorative=True)
        pad = "-12px 0" if hang else "0"
        return (f'<span class="oai-l3" role="img" aria-label="{E(label)}" style="display:inline-flex;line-height:0;margin:{pad}">{m}</span>')
    if master16or24 == 24:
        wm = mark(files[24], h=24, surface=surface, decorative=True)
        lk = mark(LOCK["display"], h=52, surface=surface, decorative=True)
        gap, top = 13, -14
    else:
        wm = mark(files[16], h=16, surface=surface, decorative=True)
        lk = mark(LOCK[24], h=34, surface=surface, decorative=True)
        gap, top = 8, -9
    pad = "0" if hang else f"{-top}px 0"
    lk_style = f"display:block;line-height:0;margin-top:{top}px;margin-bottom:{top}px"   # centered on the wordmark's box, hanging equally above and below
    return (f'<span class="oai-l3" role="img" aria-label="{E(label)}" style="display:inline-flex;align-items:flex-start;gap:{gap}px;'
            f'padding:{pad}">{wm}<span style="{lk_style}">{lk}</span></span>')


def l4(width_px, surface="newsprint"):
    """L4 on the fifth edition's layout: L8 at left, a hairline, the two-line tagline (re-exported outlines).
    Units: L8 box 299.67 by 108; hairline at 334; tl-2a at x 368.65, y 25.12, cap 0.22x; tl-2b at y 60.95."""
    U = 706.7
    k = width_px / U
    h = 108 * k
    l8 = mark(L8["today"], h=h, surface=surface, decorative=True)
    t2a = svg_file(ID_DIR / TL2A, w=338.05 * k, style=f"color:{ink(surface)}", decorative=True)
    t2b = svg_file(ID_DIR / TL2B, w=185.70 * k, style=f"color:{ink(surface)}", decorative=True)
    return (f'<span role="img" aria-label="Oath &amp; Action, L4: monogram and tagline, A country that answers to its people." '
            f'style="position:relative;display:inline-block;width:{width_px:.1f}px;height:{h:.1f}px">'
            f'<span style="position:absolute;left:0;top:0">{l8}</span>'
            f'<span style="position:absolute;left:{334 * k:.1f}px;top:{4 * k:.1f}px;width:1px;height:{100 * k:.1f}px;background:{hair(surface)}"></span>'
            f'<span style="position:absolute;left:{368.65 * k:.1f}px;top:{25.12 * k:.1f}px">{t2a}</span>'
            f'<span style="position:absolute;left:{368.65 * k:.1f}px;top:{60.95 * k:.1f}px">{t2b}</span></span>')


def l5(width_px, surface="newsprint"):
    """L5 on the fifth edition's layout: the wordmark, then tl-1 at x 0, y 142.86 (re-exported), 581.35 units wide."""
    k = width_px / 978.31
    h = 175.5 * k
    wm = mark(WM["display"] if 108 * k >= 40 else WM[24], h=108 * k, surface=surface, decorative=True)
    t1 = svg_file(ID_DIR / TL1, w=581.35 * k, style=f"color:{ink(surface)}", decorative=True)
    return (f'<span role="img" aria-label="Oath &amp; Action, L5: wordmark and tagline, A country that answers to its people." '
            f'style="position:relative;display:inline-block;width:{width_px:.1f}px;height:{h:.1f}px">'
            f'<span style="position:absolute;left:0;top:0">{wm}</span>'
            f'<span style="position:absolute;left:0;top:{142.86 * k:.1f}px">{t1}</span></span>')


# L6 centered (DR-182, November 10, 2026): the wordmark and the tagline move down 14.72 units of L6's 300, 9.3 px at 884 px,
# so the span from the wordmark's cap line (84.38 units) to the tagline's baseline (186.18) has its middle on the strip's
# middle (150), where the lockmark's middle already sits (149.47). The figure the identity designer's stage B proposal
# drew it with (work/boards/phase-2/stage-b/drawings/identity/20261109_Identity-Figures.json, key l6). Nothing else moves.
L6_SHIFT = 14.72


def l6(width_px, dots=False, centered=None):
    """L6, the editorial signature strip, on the fifth edition's layout (1400 by 300 units), on Prussian in White.
    The web address waits until it is settled. L6 draws without the four pillar dots since November 8, 2026 (DR-129);
    dots=True draws them only for the changes board's record (stage_a_identity_fix_boards.py). The lockmark keeps L6's
    own proportion, 148 units, from the master whose range holds that height: the display master at 884 px.
    centered (the default without dots, DR-182) moves the wordmark and the tagline down L6_SHIFT units; centered=False
    draws L6 as it stood before, for the boards that keep that record."""
    if centered is None:
        centered = not dots
    k = width_px / 1400
    dy = L6_SHIFT if centered else 0
    wh = pal("white")
    wm = mark(WM["display"], h=50.8 * k, surface="prussian", decorative=True)
    t1 = svg_file(ID_DIR / TL1, w=363.34 * k, style=f"color:{wh}", decorative=True)
    lk = lockmark(148 * k, surface="prussian", decorative=True)
    dots = "".join(f'<span style="position:absolute;left:{(x - 6) * k:.1f}px;top:{(227.8 - 6) * k:.1f}px;width:{12 * k:.1f}px;height:{12 * k:.1f}px;border-radius:50%;background:{wh}"></span>'
                   for x in (85.6, 110.0, 134.4, 158.8)) if dots else ""
    what = "the wordmark, the tagline, four pillar dots and the lockmark" if dots else "the wordmark, the tagline and the lockmark"
    return (f'<span role="img" aria-label="Oath &amp; Action, L6 editorial signature on Prussian, all in White: {what}." '
            f'style="position:relative;display:block;width:{width_px:.1f}px;height:{300 * k:.1f}px;background:{tv("color-surface-prussian")}">'
            f'<span style="position:absolute;left:{80 * k:.1f}px;top:{(82.5 + dy) * k:.1f}px">{wm}</span>'
            f'<span style="position:absolute;left:{80 * k:.1f}px;top:{(170.46 + dy) * k:.1f}px">{t1}</span>{dots}'
            f'<span style="position:absolute;left:{1170.5 * k:.1f}px;top:{74.9 * k:.1f}px">{lk}</span></span>')


L7_EST = {"EXPLAIN": 5.55, "TRACK": 4.02, "CONNECT": 5.86, "ACT": 2.41}


def l7_width(word_px, word="TRACK"):
    """L7's width when its pillar word sets at a given size: the word is 0.6x tall, so its size fixes the lockup's."""
    return word_px / 82.8 * (1098.31 + L7_EST[word] * 82.8)


def l7(width_px, word="TRACK", surface="newsprint"):
    """L7, section masthead: the wordmark, 0.6x of space, a 1 px hairline over the cap band, 0.6x, then the pillar word
    in Inter 600 capitals at a cap height of 0.6x, tracked 0.08 em, in the surface's ink."""
    F = 82.8                      # font size in units: cap height 0.7275 em = 60 units
    U = 1098.31 + L7_EST[word] * F
    k = width_px / U
    wm = mark(WM["display"] if 108 * k >= 40 else WM[24], h=108 * k, surface=surface, decorative=True)
    return (f'<span role="img" aria-label="Oath &amp; Action, L7 section masthead: {word.title()}" '
            f'style="position:relative;display:inline-flex;align-items:center;height:{108 * k:.1f}px;width:{width_px:.1f}px">'
            f'{wm}<span style="width:{60 * k:.1f}px"></span><span style="width:1px;height:{100 * k:.1f}px;background:{hair(surface)}"></span>'
            f'<span style="width:{60 * k:.1f}px"></span><span aria-hidden="true" style="font:600 {F * k:.2f}px/1 var(--oa-font-family-reading);letter-spacing:.08em;'
            f'color:{ink(surface)};white-space:nowrap">{word}</span></span>')


# ------------------------------------------------------------------------------------------- 03.1
@spec
def s_03_1_correct():
    W = 440
    k = W / 978.31          # px per unit; x = 100 units
    x = 100 * k
    pad = x                 # clear space 1.0x
    wm = mark(WM["display"], w=W, decorative=True)
    left = 80               # room for labels
    ink_top, ink_bot = 2.66 * k, 105.34 * k
    H = ink_bot - ink_top + 2 * pad + 40
    Wt = left + W + 2 * pad + 24
    ox, oy = left + pad, pad + 32 - ink_top     # wordmark origin
    st = pal("stone")
    a = ink("newsprint")
    lines = []
    bx0, by0, bx1, by1 = ox - pad, oy + ink_top - pad, ox + W + pad, oy + ink_bot + pad
    lines.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}" fill="none" stroke="{st}" stroke-width="1"/>')
    for yu, name in ((4, "Cap line"), (104, "Baseline")):
        y = oy + yu * k
        lines.append(f'<line x1="{bx0 - 8:.1f}" x2="{bx1:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{st}" stroke-width="1"/>')
        lines.append(f'<text x="{bx0 - 12:.1f}" y="{y + 4.5:.1f}" text-anchor="end" font-size="13" fill="{a}">{name}</text>')
    xb = ox - 16
    lines.append(f'<line x1="{xb:.1f}" x2="{xb:.1f}" y1="{oy + 4 * k:.1f}" y2="{oy + 104 * k:.1f}" stroke="{a}" stroke-width="1.5"/>')
    lines.append(f'<text x="{xb - 6:.1f}" y="{oy + 54 * k + 5:.1f}" text-anchor="end" font-size="15" font-weight="400" fill="{a}">x</text>')
    lines.append(f'<line x1="{ox + W / 2:.1f}" x2="{ox + W / 2:.1f}" y1="{by0:.1f}" y2="{oy + ink_top:.1f}" stroke="{a}" stroke-width="1"/>')
    lines.append(f'<text x="{ox + W / 2 + 6:.1f}" y="{by0 + pad / 2 + 5:.1f}" font-size="13" fill="{a}">1.0x clear space</text>')
    for u in (360.07, 369.4, 462.69, 469.68):
        X = ox + u * k
        lines.append(f'<line x1="{X:.1f}" x2="{X:.1f}" y1="{oy + ink_bot + 4:.1f}" y2="{oy + ink_bot + 12:.1f}" stroke="{a}" stroke-width="1"/>')
    yb = oy + ink_bot + 12 + 16
    lines.append(f'<text x="{ox + 415 * k:.1f}" y="{yb:.1f}" text-anchor="middle" font-size="13" fill="{a}">0.203x of white on each side of B</text>')
    overlay = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt:.0f}" height="{H:.0f}" viewBox="0 0 {Wt:.0f} {H:.0f}" '
               f'style="position:absolute;left:0;top:0;font-family:var(--oa-font-family-reading)" aria-hidden="true" class="oai-svg">{"".join(lines)}</svg>')
    body = (f'<div class="oai-panel oai-s-newsprint">'
            f'<div style="position:relative;width:{Wt:.0f}px;height:{H:.0f}px">{overlay}'
            f'<div style="position:absolute;left:{ox:.1f}px;top:{oy:.1f}px">{wm}</div></div></div>')
    alt = ("The Oath & Action wordmark at 440 pixels wide on Newsprint: OATH and ACTION in black capitals with a red "
           "ampersand between them. Guides mark the cap line and baseline, the cap height x, a clear-space box one cap height "
           "out from the letters on every side, and the equal white on each side of the ampersand, 0.203x.")
    return rec("s-03-1-correct", "03.1", int(Wt + 50), alt, body,
               notes="Display master placed at 440 px wide (44.98 px capitals). Annotations are a guide overlay, not part of the mark.")


@spec
def s_03_1_failure():
    cap = 44.98
    fs = cap / 0.7275
    w = 560
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="96" viewBox="0 0 {w} 96" class="oai-svg" aria-hidden="true">'
           f'<text x="0" y="{24 + cap:.1f}" font-family="Inter Tight, Arial, sans-serif" font-weight="800" font-size="{fs:.1f}" fill="{ink("newsprint")}">'
           f'OATH <tspan fill="{sig("newsprint")}">&amp;</tspan> ACTION</text></svg>')
    body = f'<div class="oai-panel oai-s-newsprint"><span class="oai-red" data-red="signature" data-failure="true">{svg}</span></div>'
    alt = ("Failure case: OATH & ACTION typed in Inter Tight 800 with the font's own sans-serif ampersand colored red and "
           "ordinary word spaces, so the ampersand is a different shape and the gaps around it are wide and uneven.")
    return rec("s-03-1-failure", "03.1", 610, alt, body, check_exempt=["contrast", "scale"],
               notes="Drawn as live SVG text inside a labeled image, at the correct case's cap height (44.98 px capitals, so 61.8 px type): "
                     "a labeled failure, so it takes check_exempt scale and contrast (the font's red ampersand measures 2.96:1).")


# ------------------------------------------------------------------------------------------- 03.2
def _tile(inner, size=120, label=""):
    return (f'<div class="oai-cell"><div style="width:{size}px;height:{size}px;display:flex;align-items:center;justify-content:center;'
            f'background:{tv("color-surface-white")};border:1px solid {hair("white")}">{inner}</div>{tag(label) if label else ""}</div>')


@spec
def s_03_2_correct():
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row">'
            + _tile(mark(L8["today"], w=74, surface="white", label="Oath & Action, L8 monogram"), 120, "Partner tile, 120 px, L8 at 74 px wide")
            + '</div></div>')
    alt = "A 120 pixel white square tile from a partner directory carrying the L8 monogram, O & A, 74 pixels wide with 25 pixel capitals."
    return rec("s-03-2-correct", "03.2", 200, alt, body, notes="L8 cap height 24.7 px.")


@spec
def s_03_2_failure():
    wm = mark(WM["display"], w=100, surface="white", decorative=True)
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row">'
            + _tile(wm, 120, "Same tile, full wordmark at 100 px wide")
            + '</div></div>')
    alt = "Failure case: the same 120 pixel tile with the full OATH & ACTION wordmark squeezed to 100 pixels wide; its capitals are 10 pixels tall and blur."
    return rec("s-03-2-failure", "03.2", 200, alt, body, notes="Display master scaled to 100 px wide (10.2 px capitals), as a producer would drag it.")


MIN = {  # each lockup's minimum, from the identity masters' table at today's width
    "L1": ("16 px tall, 152 px wide", "1.20 in wide"), "L2": ("90 px wide", "0.80 in"), "L3": ("196 px wide", "1.55 in"),
    "S1": ("79 px wide", "0.65 in"),
    "L4": ("304 px wide", "2.30 in"), "L5": ("388 px wide", "2.90 in"), "L6": ("884 px wide", "6.60 in"),
    "L7": ("250 px wide", "1.90 in"), "L8": ("48 px wide", "0.50 in"),
}


def _lock_item(code, name, job, inner, span=False):
    scr, prt = MIN[code]
    return (f'<div class="oai-panel oai-s-newsprint oai-lk{" oai-lk--span" if span else ""}">'
            f'<div class="oai-lk-mark">{inner}</div>'
            f'<p class="oai-lk-name">{E(code)} {E(name)}</p><p class="oai-lk-job">{E(job)}</p>'
            f'<p class="oai-tag">Minimum: {E(_nb(scr))} on screen, {E(_nb(prt))} in print</p></div>')


def _nb(t):
    """A number keeps its unit on its line (CA-N4)."""
    return re.sub(r"(\d) (px|pt|in|mm)\b", "\\1\u00a0\\2", t)


LOCK_CSS = (".oai-lockgrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}"
            ".oai-lk{padding:20px;display:flex;flex-direction:column;gap:6px;align-items:flex-start}"
            ".oai-lk--span{grid-column:1/-1}"
            ".oai-lk-mark{min-height:88px;display:flex;align-items:flex-end;margin-bottom:10px}"
            ".oai-lk-name{font-weight:700;font-size:17px}"
            ".oai-lk-job{font-size:15px;color:var(--oa-color-text-secondary-on-newsprint)}")


# Gate 2's fix pass (CD-S1): the plate carries each master once with an id, and chapter 03's opener draws the same
# masters by <use> (stage_a_identity_lib.SHARE and REF), so the page holds each drawing once.
@spec
def s_03_lockups():
    LIB.SHARE[0], LIB.SHARE[1] = "s-03-lockups", set()
    try:
        return _lockups()
    finally:
        LIB.SHARE[0] = None


def _lockups():
    parts = [
        _lock_item("L1", "Wordmark", "Most uses: page heads, documents, slides and signs.", wordmark(32, label="Oath & Action, L1 wordmark")),
        _lock_item("L8", "Monogram", "Squares where the name must show, such as a tile in a partner's directory. Never an avatar or a favicon.", mark(L8["today"], w=120, label="Oath & Action, L8 monogram")),
        _lock_item("S1", "Stacked", "OATH & over ACTION, flush left, for square formats and posters.", s1(40, label="Oath & Action, S1 stacked lockup")),
        _lock_item("L4", "Monogram and tagline", "Document footers and small print.", l4(304)),
        _lock_item("L3", "Horizontal with the lockmark", "The site and email masthead.", l3_small(24)),
        _lock_item("L7", "Section masthead", "Names the pillar a piece serves, in the surface's ink.", l7(l7_width(17, "TRACK"), "TRACK")),
        _lock_item("L5", "Wordmark and tagline", "Covers, banners and partner placements where the tagline travels with the mark.", l5(400), span=True),
    ]
    body = f'<div class="oai-lockgrid">{"".join(parts)}</div>'
    alt = ("Seven lockups at true size on Newsprint, two to a row, each with its job and its minimum on screen and in print: "
           "L1 the wordmark, 16 pixels tall or 152 wide, 1.20 inches, beside L8 the O & A monogram, 48 pixels, 0.50 inches; "
           "S1 stacked, OATH & over ACTION on two flush-left lines, 79 pixels, 0.65 inches, beside L4 the monogram, a hairline "
           "and the tagline on two lines, 304 pixels, 2.30 inches; L3 the wordmark with the lockmark at its right, 196 pixels, "
           "1.55 inches, beside L7 the wordmark, a hairline and the word TRACK, 250 pixels, 1.90 inches; and L5 the wordmark "
           "over the tagline, 388 pixels, 2.90 inches. L6 follows in its own plate.")
    return rec("s-03-lockups", "03.2", 712, alt, body, css=LOCK_CSS,
               notes="Two columns at 712 px (C-S7), with L1, S1 and L3 in the left column, so a phone shows them first in the scrolling frame (CD-S7); every mark sits on the bottom of an 88 px box, so each row's names share one line (CA-S11). L1, S1, L3 and L8 are masters; S1 at 40 px capitals from its display master (DR-113). L4, L5 and L7 are assembled from the approved "
                     "masters and re-exported taglines on V5's layouts (I8 note). L6 has its own plate, s-03-l6, since its 884 px "
                     "minimum is wider than the column. L7's pillar word is live text at 17 px, a size on the scale, which sets L7 at 294 px. "
                     "L3 from its masthead master in use since November 10, 2026, lockups/20261110_L3-Horizontal-Master.svg, which "
                     "carries the rebuilt 48 px lockmark master and draws the same pixels as the November 8 file (DR-181).")


@spec
def s_03_l6():
    body = (f'<div class="oai-pad">{l6(884)}<p class="oai-tag" style="margin-top:12px">L6 Editorial signature, at its minimum: 884 px wide on '
            f'screen, 6.60 in in print. The strip that closes a report or a long page, shown on Prussian, where every part is White.</p></div>')
    alt = ("L6, the editorial signature, at its 884 pixel minimum on a Prussian strip, all in White: the wordmark and the "
           "tagline at left, centered on the strip's height, and the lockmark at right. Its print minimum is 6.60 inches.")
    return rec("s-03-l6", "03.2", 932, alt, body, fit_switch=True,
               notes="L6 on V5's layout, measured from the Gate 0 capture: 1400 by 300 units, without the four pillar dots V5 drew "
                     "under the tagline (DR-129). In use since November 10, 2026: the wordmark and tagline centered on the strip "
                     "(DR-182), moved down 14.72 units, 9.3 px at 884 px, so the span from the wordmark's cap line to the tagline's "
                     "baseline has its middle on the strip's middle, as the identity designer's stage B proposal drew it. The strip, "
                     "the lockmark and every size stay as they were: the lockmark keeps L6's proportion, 93.5 px at 884 px, from the "
                     "display master. No web address until it is settled (DR-55).")


# ------------------------------------------------------------------------------------------- the opener
# Gate 2's fix pass (CD-S1, the creative director's list: "03 the eight lockups"). The lockups at the sizes Rule 03.2's
# plate sets them, built by the same functions and drawn by <use> of the masters that plate carries, so the opener adds
# about 6 KB and no drawing. Each fits a phone's column but L5, whose 388 px minimum is wider than it, so L5 shows from
# 48em. L6, at 884 px, keeps its own plate. Two to a row from 48em, one under 48em.
OPENER_CSS = (".oai-op3{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 32px;align-items:end}"
              ".oai-op3-c{display:flex;flex-direction:column;gap:10px;align-items:flex-start}"
              ".oai-op3-c--wide{grid-column:1/-1}"
              "@media (max-width:47.99em){.oai-op3{grid-template-columns:minmax(0,1fr);gap:24px}.oai-op3-c--wide{display:none}}")


@spec
def s_03_opener():
    LIB.REF[0] = "s-03-lockups"
    try:
        cells = [("L1", "Wordmark", wordmark(32, decorative=True)),
                 ("L8", "Monogram", mark(L8["today"], w=120, decorative=True)),
                 ("S1", "Stacked", s1(40, decorative=True)),
                 ("L4", "Monogram and tagline", l4(304)),
                 ("L3", "Horizontal with the lockmark", l3_small(24)),
                 ("L7", "Section masthead", l7(l7_width(17, "TRACK"), "TRACK")),
                 ("L5", "Wordmark and tagline", l5(400))]
    finally:
        LIB.REF[0] = None
    # the plate's stage gives the opener its 24 px inset (16 px on a phone), so the grid takes the whole width
    body = ('<div class="oai-op3">'
            + "".join(f'<div class="oai-op3-c{" oai-op3-c--wide" if code == "L5" else ""}">{m}<p class="oai-tag">{code} {E(name)}</p></div>'
                      for code, name, m in cells)
            + '</div>')
    alt = ("The lockups at true size on Newsprint, each with its name, two to a row: L1, the wordmark, beside L8, the O & A "
           "monogram; S1, OATH & over ACTION on two flush-left lines, beside L4, the monogram, a hairline and the tagline; L3, "
           "the wordmark with the lockmark at its right, beside L7, the wordmark, a hairline and the word TRACK. On screens "
           "48em wide and up, L5 follows across both columns: the wordmark over the tagline.")
    return rec("s-03-opener", None, None, alt, body, css=OPENER_CSS,
               notes="Gate 2's fix pass, CD-S1: chapter 03's opener. Each mark is an <svg> holding one <use> of the master "
                     "s-03-lockups carries with an id (stage_a_identity_lib.SHARE and REF), at the size that plate sets, from "
                     "the same lockup functions, so the opener draws no master of its own. L5 shows from 48em, since its 388 px "
                     "minimum is wider than a phone's column; L6 keeps its own plate, s-03-l6.")


# ------------------------------------------------------------------------------------------- 03.3
def _page_head(gap_px, failure=False):
    h = 32
    wm = wordmark(h, decorative=True)
    zone = ""
    if not failure:
        cs = 32   # 1.0x rounded up to oa.space.400
        zone = (f'<span aria-hidden="true" style="position:absolute;left:{-cs}px;top:{-cs}px;width:calc(100% + {2 * cs}px);'
                f'height:{h + 2 * cs}px;border:1px solid {pal("stone")}"></span>'
                f'<span class="oai-tag" style="position:absolute;left:calc(100% + {cs + 8}px);top:{-cs - 2}px;white-space:nowrap">1.0x</span>')
    head = f'<p style="{ty("h3", 520)};margin-top:{gap_px}px;max-width:22ch">What the county board decides on Tuesday</p>'
    return (f'<div style="padding:{40 if not failure else 24}px 56px 24px 56px">'
            f'<div style="position:relative;display:inline-block">{wm}{zone}</div>{head}'
            f'<p style="margin-top:8px">{illus()}<span class="oai-tag">The headline is invented.</span></p></div>')


@spec
def s_03_3_correct():
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:0">{_page_head(40)}</div>'
    alt = ("A page head at true size: the wordmark 32 pixels tall with a box one cap height out on every side, and the "
           "headline What the county board decides on Tuesday set below the box. The headline is Illustrative.")
    return rec("s-03-3-correct", "03.3", 520, alt, body, illustrative=True,
               notes="24 px master drawn at 32 px tall (29 px capitals); clear space rounded up to 32 px, oa.space.400. Headline in the H3 style at 26 px (D2-254).")


@spec
def s_03_3_failure():
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:0">{_page_head(9, failure=True)}</div>'
    alt = ("Failure case: the same page head with the headline moved up to 9 pixels below the wordmark, inside its clear "
           "space, so the headline's first words read as part of the name. The headline is Illustrative.")
    return rec("s-03-3-failure", "03.3", 520, alt, body, illustrative=True, notes="Headline 0.3x below the wordmark.")


# ------------------------------------------------------------------------------------------- 03.4
@spec
def s_03_4_correct():
    row1 = markrow([
        (wordmark(16, label="L1 at its minimum, 16 px tall"), ["L1, 16 px tall", "152 px wide"]),
        (s1(14, label="S1 at its minimum, 79 px wide"), ["S1, 79 px wide"]),
        (l3_small(16, label="L3 at its minimum, 196 px wide", hang=True), ["L3, 196 px wide"]),
        (mark(L8["today"], w=48, label="L8 at its minimum, 48 px wide"), ["L8, 48 px wide"]),
    ], 36)
    row2 = markrow([
        (amp(16, label="Ampersand B at its minimum, 16 px"), ["Ampersand B, 16 px"]),
        (lockmark(16, label="Lockmark at its minimum, 16 px"), ["Lockmark, 16 px"]),
        (mark(BADGE["display"], h=48, label="Hinge-circle badge at its minimum, 48 px"), ["Badge, 48 px"]),
        (mark(HINGE["compact"], w=245, label="Hinge diagram, compact master, at its minimum, 245 px wide"), ["Hinge diagram, compact, 245 px"]),
    ], 60)
    row3 = markrow([(l4(304), ["L4, 304 px wide"]), (l7(250, "CONNECT"), ["L7, 250 px wide with its longest word"])], 44)
    row4 = markrow([(l5(388), ["L5, 388 px wide"])], 70)
    row5 = markrow([(mark(HINGE["display"], w=533, label="Hinge diagram, display master, at its minimum, 533 px wide"), ["Hinge diagram, display, 533 px"])], 140)
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:36px">'
            f'{row1}{row2}{row3}{row4}{row5}'
            '<p class="oai-note">Each mark sits at its smallest allowed size, at true size, on one bottom line with the others in its row. '
            'These are graphics, so the 13 px floor for text does not apply to the letters drawn inside them. L6 appears at its 884 px minimum after Rule 03.2.</p>'
            '</div></div>')
    alt = ("Every identity mark at its screen minimum, at true size, each row on one bottom line: the wordmark 16 pixels tall, "
           "the S1 stacked lockup 79 wide, the horizontal lockup 196 wide, the monogram 48 wide; ampersand B and the lockmark at "
           "16 pixels, the badge at 48 and the compact hinge diagram at 245; L4 at 304 and L7 at 250; L5 at 388; and the display hinge "
           "diagram at 533.")
    return rec("s-03-4-correct", "03.4", 712, alt, body, css=MARKROW_CSS,
               notes="Marks at true size are graphics (Stage A brief: the 13 px floor exempts a mark shown at its minimum, and the note says so). "
                     "L3's lockmark hangs above and below the wordmark's box, so every row aligns on the marks' bottoms (C-S13). L3 at "
                     "196 px draws its lockmark at 34 px from the rebuilt 24 px master in use since November 10, 2026, each node and "
                     "the lever one outline, so its nodes stay whole at 34 px (DR-145, DR-181). The lockmark at 16 px is the 16 px "
                     "master, unchanged.")


@spec
def s_03_4_failure():
    wm = mark(WM["display"], h=12, surface="newsprint", decorative=True)
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row mid">'
            f'{wm}<span class="oai-tag">Display master at 12 px tall</span></div></div>')
    alt = "Failure case: the wordmark's display master scaled down to 12 pixels tall, its capitals 11 pixels, the gaps around the ampersand filling in."
    return rec("s-03-4-failure", "03.4", 360, alt, body, notes="Display master at 12 px tall (11.1 px capitals), as an email footer might place it.")


def _no_condensed(t):
    """Today's width only in chapter 03 (BE-S11): the condensed figures move to the proofs appendix."""
    t = re.sub(r";\s*condensed [^);]*", "", t)
    t = re.sub(r"\s*\(condensed [^)]*\)", "", t)
    t = t.replace("V5 master", "display master").replace("from V5's layout", "on our fifth edition's layout")
    return re.sub(r"(\d) (px|pt|in|mm)\b", "\\1\u00a0\\2", t)       # a number keeps its unit on its line (CA-N4)


MINIMUM_ROWS = json.loads((ID_DIR / "20261028_Identity-Minimum-Sizes.json").read_text())


def _mark_name(n):
    return n.replace("Hinge diagram V2", "Hinge diagram").replace("L1 wordmark", "L1 Wordmark")


@spec
def s_03_minimums():
    rows = "".join(f'<tr><th scope="row">{E(_mark_name(r["lockup"]))}</th><td data-k="Screen">{E(_no_condensed(r["screen"]))}</td>'
                   f'<td data-k="Print">{E(_no_condensed(r["print"]))}</td><td data-k="Below the minimum">{E(r["below"])}</td></tr>'
                   for r in MINIMUM_ROWS["rows"] if r.get("status") != "retired")
    table = (f'<table class="stack"><caption class="oai-note" style="text-align:left;caption-side:top;padding-bottom:8px">{E(MINIMUM_ROWS["rule"])}</caption>'
             '<thead><tr><th scope="col">Mark</th><th scope="col">Screen minimum</th><th scope="col">Print minimum</th><th scope="col">Below the minimum</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    body = f'<div class="oai-panel oai-s-newsprint">{table}</div>'
    alt = "Minimum sizes on screen and in print for every identity mark, with the mark to use below each minimum."
    return rec("s-03-minimums", "03.4", None, alt, body, readable=True,
               notes="Read from work/build/assets/identity/20261028_Identity-Minimum-Sizes.json (I8) with retired rows (L2, DR-113) and "
                     "the condensed figures left out (DR-115, D2-328) and V5 named in words. readable: the table reaches assistive "
                     "technology (AX-M1). Stacks under 568 px with each cell's column named.")


# ------------------------------------------------------------------------------------------- 03.5
@spec
def s_03_5_correct():
    cols = [("newsprint", "color", "Newsprint"), ("white", "color", "White"), ("charcoal", "color", "Charcoal"),
            ("prussian", "color", "Prussian, all White"), ("newsprint", "mono", "One color, Charcoal"), ("charcoal", "mono", "One color, Newsprint")]
    cells = []
    for s, m, name in cols:
        inner = (f'<div class="oai-stack" style="gap:20px;align-items:flex-start">'
                 f'{wordmark(22, surface=s, mode=m, label=f"L1 on {name}")}'
                 f'<div class="oai-row" style="gap:20px">{s1(22, surface=s, mode=m, label=f"S1 on {name}")}'
                 f'{mark(L8["today"], w=60, surface=s, mode=m, label=f"L8 on {name}")}</div></div>')
        cells.append(f'<div class="oai-panel oai-s-{s}">{inner}<p class="oai-tag" style="margin-top:16px">{E(name)}</p></div>')
    css = ".oai-matrix{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr));gap:12px}"
    body = f'<div class="oai-matrix">{"".join(cells)}</div>'
    alt = ("L1, S1 and L8 on six grounds at true size: Newsprint, White and Charcoal with the red ampersand; Prussian with "
           "every part White; and one-color versions in Charcoal on Newsprint and in Newsprint on Charcoal.")
    return rec("s-03-5-correct", "03.5", None, alt, body, css=css,
               notes="A sheet: the stage flows and each mark keeps its true size. Prussian cells place the explicit-White files from prussian/ (treatment D, I9), S1's included. L1 uses the 24 px master at 22 px tall; S1 its 24 px master at 22 px capitals.")


@spec
def s_03_5_failure():
    wm = mark(WM["display"], h=54, surface="newsprint", decorative=True)   # the Newsprint file, as dropped on Charcoal
    body = f'<div class="oai-panel oai-s-charcoal"><span class="oai-red" data-red="signature" data-failure="true">{wm}</span></div>'
    alt = "Failure case: the Newsprint version of the wordmark placed on a Charcoal slide. The black letters disappear into the black ground and only the red ampersand shows."
    return rec("s-03-5-failure", "03.5", 560, alt, body, notes="Charcoal letters on Charcoal, 1:1.")


# ------------------------------------------------------------------------------------------- 03.6
def _nav(items):
    return "".join(f'<span style="{ty("ui")};white-space:nowrap">{E(t)}</span>' for t in items)


def _burger(surface="newsprint"):
    return (f'<span aria-hidden="true" style="width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:center">'
            + "".join(f'<span style="width:20px;height:2px;background:{ink(surface)}"></span>' for _ in range(3)) + '</span>')


@spec
def s_03_6_correct():
    desk = (f'<div class="oai-s-newsprint" style="width:1440px;height:80px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 64px;border-bottom:1px solid {hair("newsprint")}">{l3_small(24, label="Oath & Action")}'
            f'<div style="display:flex;gap:32px">{_nav(["Explain", "Track", "Connect", "Act", "About"])}</div></div>')
    phone = (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
             f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}">{wordmark(24, label="Oath & Action")}{_burger()}</div>')
    email = (f'<div class="oai-s-white" style="width:600px;height:96px;display:flex;align-items:center;padding:0 24px;'
             f'border:1px solid {hair("white")}">{l3_small(24, surface="white", label="Oath & Action")}</div>')
    body = ('<div class="oai-stack" style="gap:24px">'
            f'<div class="oai-cell">{desk}<span class="oai-tag">Site from 48em, 768 px at the default text size; shown at 1440 px: L3 from its masthead master, the lockmark at 48 px</span></div>'
            f'<div class="oai-row top"><div class="oai-cell">{phone}<span class="oai-tag">Phone, 390 px: L1 from the 24 px master</span></div>'
            f'<div class="oai-cell">{email}<span class="oai-tag">Email, 600 px: L3, sent as a PNG at twice size</span></div></div></div>')
    alt = ("Three mastheads at true size: a 1440 pixel site bar with the wordmark and lockmark at left and five navigation words "
           "at right; a 390 pixel phone bar with the wordmark and a menu button; and a 600 pixel white email header with the "
           "wordmark and lockmark.")
    return rec("s-03-6-correct", "03.6", 1440, alt, body, fit_switch=True,
               notes="Navigation words are placeholders for chapter 20, drawn as div elements (AX-S8). The email header is drawn live here; in email it ships as a PNG. "
                     "Both L3s from the masthead master in use since November 10, 2026, lockups/20261110_L3-Horizontal-Master.svg, "
                     "which carries the rebuilt 48 px lockmark master and draws the same pixels as the November 8 file (DR-181).")


@spec
def s_03_6_failure():
    l3m = mark(L3["masthead"], w=150, surface="newsprint", decorative=True)
    phone = (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
             f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}">{l3m}{_burger()}</div>')
    body = f'<div>{phone}</div>'
    alt = ("Failure case: a 390 pixel phone bar with the L3 lockup squeezed to 150 pixels wide; its capitals are 12 pixels tall, "
           "under the 14 pixel floor, and the lockmark shrinks to 26 pixels.")
    return rec("s-03-6-failure", "03.6", 400, alt, body,
               notes="L3's masthead master at 150 px wide: 11.7 px capitals, a 25.5 px lockmark. Since November 10, 2026 the masthead "
                     "master carries the rebuilt 48 px lockmark master (DR-181), so the squeezed lockmark keeps whole nodes, where the "
                     "earlier file's pixel rows parted into stripes. The failure is the capitals under the 14 px floor and L3 under "
                     "its 196 px minimum (Rule 03.4).")


# ------------------------------------------------------------------------------------------- 03.7
@spec
def s_03_7_correct():
    ch = (f'<div class="oai-cell"><div class="oai-s-charcoal" style="padding:16px">{mark(L8["today"], w=120, surface="charcoal", label="L8 at 120 px wide on Charcoal")}</div>'
          '<span class="oai-tag">120 px on Charcoal</span></div>')
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row">'
            f'<div class="oai-cell">{mark(L8["today"], w=48, label="L8 at 48 px wide")}<span class="oai-tag">48 px, the minimum</span></div>'
            f'<div class="oai-cell">{mark(L8["today"], w=120, label="L8 at 120 px wide")}<span class="oai-tag">120 px</span></div>'
            f'{ch}</div></div>')
    alt = "The L8 monogram, O & A with ampersand B, at its 48 pixel minimum and at 120 pixels on Newsprint and on Charcoal, at true size."
    return rec("s-03-7-correct", "03.7", 420, alt, body)


@spec
def s_03_7_failure():
    cap = 120 * 100 / 299.67
    fs = cap / 0.7275
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="260" height="80" viewBox="0 0 260 80" class="oai-svg" aria-hidden="true">'
           f'<text x="0" y="{20 + cap:.1f}" font-family="Inter Tight, Arial, sans-serif" font-weight="800" font-size="{fs:.1f}" fill="{ink("newsprint")}">'
           f'O <tspan fill="{sig("newsprint")}">&amp;</tspan> A</text></svg>')
    body = f'<div class="oai-panel oai-s-newsprint"><span class="oai-red" data-red="signature" data-failure="true">{svg}</span></div>'
    alt = ("Failure case: the compact signature from our brand guide's fourth edition, O & A typed in Inter Tight with word "
           "spaces and the font's sans-serif ampersand in red, at the same cap height as L8 at 120 pixels.")
    return rec("s-03-7-failure", "03.7", 300, alt, body, check_exempt=["contrast", "scale"],
               notes="V4.2's typed signature at L8's cap height (40 px capitals, so 55 px type): a labeled failure, so check_exempt scale and contrast.")


# ------------------------------------------------------------------------------------------- 03.8
X32 = 32 * 22 / 24       # capitals of the wordmark drawn 32 px tall from its 24 px master: x


def _hair(surface="newsprint"):
    return f'<span aria-hidden="true" style="flex:none;width:1px;height:{round(1.2 * X32)}px;background:{hair(surface)}"></span>'


def _partner_name():
    return f'<span style="font:600 24px/1.1 var(--oa-font-family-reading);white-space:nowrap">Merrimack Valley Civic Lab</span>'


def _plock(host="us"):
    g = round(0.6 * X32)
    wm = wordmark(32, decorative=True)
    parts = [wm, _hair(), _partner_name()] if host == "us" else [_partner_name(), _hair(), wm]
    return f'<div style="display:flex;align-items:center;gap:{g}px">{"".join(parts)}</div>'


@spec
def s_03_8_correct():
    rows = (f'<div class="oai-stack" style="gap:28px">'
            f'<div class="oai-cell" style="gap:10px">{_plock("us")}<p class="oai-tag">{illus()}On a piece we host, our name leads. The partner is invented.</p></div>'
            f'<div class="oai-cell" style="gap:10px">{_plock("partner")}<p class="oai-tag">{illus()}On a piece the partner hosts, its name leads. The partner is invented.</p></div></div>')
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:32px">{rows}</div>'
    alt = ("Two partnership lockups at true size. In the first, for a piece Oath & Action hosts, the wordmark 32 pixels tall "
           "leads, then a vertical hairline, then the partner name Merrimack Valley Civic Lab. In the second, for a piece the "
           "partner hosts, the partner name leads and the wordmark follows the hairline. The partner is invented, Illustrative.")
    return rec("s-03-8-correct", "03.8", 760, alt, body, illustrative=True,
               notes="Merrimack Valley Civic Lab is V5's invented partner (Q-01), labeled beside each lockup. Hairline 1.2x tall, "
                     "0.6x of space on each side (x = 29.3 px). The host's name leads (DR-102).")


@spec
def s_03_8_failure():
    a = amp(X32, decorative=True)
    inner = (f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">{wordmark(32, decorative=True)}'
             f'<span class="oai-red" data-red="signature" data-failure="true">{a}</span>'
             f'<span style="font-family:var(--oa-font-family-display);font-weight:800;font-size:{X32 / 0.7275:.1f}px;line-height:1;letter-spacing:-.02em;text-transform:uppercase">Merrimack Valley Civic Lab</span></div>'
             f'<p style="margin-top:16px;{ty("body")}">present a workshop on public comment</p>')
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:32px">{head_label()}{inner}</div>'
    alt = ("Failure case: an event flyer that reads OATH & ACTION & MERRIMACK VALLEY CIVIC LAB present a workshop on public "
           "comment, with a second red ampersand joining the two names. Illustrative.")
    return rec("s-03-8-failure", "03.8", 700, alt, body, illustrative=True, check_exempt=["scale"],
               notes="A labeled failure: the partner's name is typed in Inter Tight 800 capitals at our capitals' height (40.3 px type), "
                     "as a producer would fake a joint lockup, so check_exempt scale.")


@spec
def s_03_misuse():
    def case(title, inner):
        return (f'<div class="oai-panel oai-s-newsprint oai-cell" style="gap:16px"><div style="min-height:70px;display:flex;align-items:center">{inner}</div>'
                f'<p class="oai-note" style="color:var(--oa-color-text-primary-on-newsprint)">{title}</p></div>')
    stretched = (f'<span style="display:inline-block;width:330px;height:{254 * 108 / 978.31:.1f}px">'
                 f'<span style="display:inline-block;transform:scaleX(1.3);transform-origin:0 0">{mark(WM["display"], w=254, decorative=True)}</span></span>')
    shadow = f'<span style="display:inline-block;filter:drop-shadow(3px 4px 3px var(--oa-color-palette-stone))">{mark(WM["display"], w=300, decorative=True)}</span>'
    recolor = svg_file(ID_DIR / WM["display"], w=300, decorative=True, style=f"color:{ink('newsprint')};--amp:{pal('prussian')}")
    cases = [
        case("<b>Stretched to fill a banner.</b> A slide app's corner handle pulled the mark 30 percent wider; the round letters turn oval.", stretched),
        case("<b>A drop shadow from a design app's effects menu.</b> The edges blur and the mark looks pasted on.",
             f'<span class="oai-red" data-red="signature" data-failure="true">{shadow}</span>'),
        case("<b>The ampersand recolored to match a partner's blue.</b> The red joint of the name is gone, and Prussian sits in a job it does not have.", recolor),
    ]
    css = ".oai-mis{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(380px,100%),1fr));gap:12px}"
    body = f'<div class="oai-mis">{"".join(cases)}</div>'
    alt = "Three more failure cases at true size: the wordmark stretched 30 percent wider, the wordmark with a drop shadow, and the wordmark with its ampersand recolored dark blue."
    return rec("s-03-misuse", "03.8", None, alt, body, css=css,
               notes="Extras: three failures producers make in slide and design apps. A sheet, so the stage flows. Placement attributes only; the master is unchanged.")
