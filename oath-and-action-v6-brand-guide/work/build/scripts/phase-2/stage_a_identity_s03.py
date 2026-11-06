"""Chapter 03 Identity: specimens. Each function returns one specimen record (see stage_a_identity_build.py)."""
import json
from stage_a_identity_lib import (E, ID_DIR, WM, WMC, L2, L3, L8, LOCK, AMP, BADGE, HINGE, TL1, TL2A, TL2B, fragment, mark,
                                  wordmark, lockmark, amp, illus, tag, svg_file, mark_style, ink, ink2, hair, pal, tv, sig)

S = []


def spec(fn):
    S.append(fn)
    return fn


def rec(sid, rule, width, alt, body, *, illustrative=False, notes="", cls="", css="", role_img=None, chapter="03"):
    return {"id": sid, "chapter": chapter, "rule": rule, "width_px": width, "alt": alt, "illustrative": illustrative,
            "notes": notes, "html": fragment(sid, body, cls=cls, extra_css=css, role_img=role_img)}


def scroll(inner, label):
    return f'<div class="oai-scroll" role="region" tabindex="0" aria-label="{E(label)}">{inner}</div>'


# ------------------------------------------------------------------------------------------- lockup assembly
def l3_small(master16or24=24, width="today", surface="newsprint", label="Oath & Action, L3 horizontal lockup"):
    """L3 as I8 composes it at small sizes: the wordmark's small master, 0.6x of space, the lockmark at 2.4 cap heights,
    centered on the wordmark's box. 24: 221 or 181 px wordmark (22 px capitals), 13 px gap, 52 px lockmark (V5 master).
    16: 152 or 120 px wordmark (14 px capitals), 8 px gap, 34 px lockmark from its 24 px master."""
    files = WM if width == "today" else WMC
    if master16or24 == 24:
        wm = mark(files[24], h=24, surface=surface, decorative=True)
        lk = mark(LOCK["display"], h=52, surface=surface, decorative=True)
        gap, top = 13, -14
    else:
        wm = mark(files[16], h=16, surface=surface, decorative=True)
        lk = mark(LOCK[24], h=34, surface=surface, decorative=True)
        gap, top = 8, -9
    return (f'<span class="oai-l3" role="img" aria-label="{E(label)}" style="display:inline-flex;align-items:flex-start;gap:{gap}px;'
            f'padding:{-top}px 0">{wm}<span style="margin-top:{top}px">{lk}</span></span>')


def l4(width_px, surface="newsprint"):
    """L4 on V5's layout (I8 note): L8 at left, a hairline, the two-line tagline (re-exported outlines, I1).
    Units: L8 box 299.67 by 108; hairline at 334; tl-2a at x 368.65, y 25.12, cap 0.22x; tl-2b at y 60.95."""
    U = 706.7
    k = width_px / U
    h = 108 * k
    st = mark_style(surface)
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
    """L5 on V5's layout: the wordmark, then tl-1 at x 0, y 142.86 (re-exported), 581.35 units wide, cap 0.24x."""
    k = width_px / 978.31
    h = 175.5 * k
    wm = mark(WM["display"] if 108 * k >= 40 else WM[24], h=108 * k, surface=surface, decorative=True)
    t1 = svg_file(ID_DIR / TL1, w=581.35 * k, style=f"color:{ink(surface)}", decorative=True)
    return (f'<span role="img" aria-label="Oath &amp; Action, L5: wordmark and tagline, A country that answers to its people." '
            f'style="position:relative;display:inline-block;width:{width_px:.1f}px;height:{h:.1f}px">'
            f'<span style="position:absolute;left:0;top:0">{wm}</span>'
            f'<span style="position:absolute;left:0;top:{142.86 * k:.1f}px">{t1}</span></span>')


def l6(width_px):
    """L6, the editorial signature strip, on V5's layout (1400 by 300 units, measured from the Gate 0 capture), on Prussian
    in treatment D: every part White. The web address waits for the site (DR-55)."""
    k = width_px / 1400
    wh = pal("white")
    wm = mark(WM["display"], h=50.8 * k, surface="prussian", decorative=True)
    t1 = svg_file(ID_DIR / TL1, w=363.34 * k, style=f"color:{wh}", decorative=True)
    lk = mark(LOCK["display"], h=148 * k, surface="prussian", decorative=True)
    dots = "".join(f'<span style="position:absolute;left:{(x - 6) * k:.1f}px;top:{(227.8 - 6) * k:.1f}px;width:{12 * k:.1f}px;height:{12 * k:.1f}px;border-radius:50%;background:{wh}"></span>'
                   for x in (85.6, 110.0, 134.4, 158.8))
    return (f'<span role="img" aria-label="Oath &amp; Action, L6 editorial signature on Prussian, all in White: the wordmark, the tagline, four pillar dots and the lockmark." '
            f'style="position:relative;display:block;width:{width_px:.1f}px;height:{300 * k:.1f}px;background:{tv("color-surface-prussian")}">'
            f'<span style="position:absolute;left:{80 * k:.1f}px;top:{82.5 * k:.1f}px">{wm}</span>'
            f'<span style="position:absolute;left:{80 * k:.1f}px;top:{170.46 * k:.1f}px">{t1}</span>{dots}'
            f'<span style="position:absolute;left:{1170.5 * k:.1f}px;top:{74.9 * k:.1f}px">{lk}</span></span>')


def l7(width_px, word="TRACK", surface="newsprint"):
    """L7, section masthead: the wordmark, 0.6x of space, a 1 px hairline over the cap band, 0.6x, then the pillar word
    in Inter 600 capitals at a cap height of 0.6x, tracked 0.08 em, in the surface's ink (Rule 05.3 retires V5's red Act)."""
    F = 82.8                      # font size in units: cap height 0.7275 em = 60 units
    est = {"EXPLAIN": 5.55, "TRACK": 4.02, "CONNECT": 5.86, "ACT": 2.41}[word]
    U = 1098.31 + est * F
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
    W = 480
    k = W / 978.31          # px per unit; x = 100 units
    x = 100 * k
    pad = x                 # clear space 1.0x
    wm = mark(WM["display"], w=W, decorative=True)
    left = 96               # room for labels
    ink_top, ink_bot = 2.66 * k, 105.34 * k
    H = ink_bot - ink_top + 2 * pad + 40
    Wt = left + W + 2 * pad + 24
    ox, oy = left + pad, pad + 32 - ink_top     # wordmark origin
    st = pal("stone")
    a = ink("newsprint")
    lines = []
    # clear-space box from the ink edges
    bx0, by0, bx1, by1 = ox - pad, oy + ink_top - pad, ox + W + pad, oy + ink_bot + pad
    lines.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}" fill="none" stroke="{st}" stroke-width="1"/>')
    # cap line and baseline
    for yu, name in ((4, "Cap line"), (104, "Baseline")):
        y = oy + yu * k
        lines.append(f'<line x1="{bx0 - 8:.1f}" x2="{bx1:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{st}" stroke-width="1"/>')
        lines.append(f'<text x="{bx0 - 12:.1f}" y="{y + 4.5:.1f}" text-anchor="end" font-size="13" fill="{a}">{name}</text>')
    # x bracket inside the clear space, left of the O
    xb = ox - 16
    lines.append(f'<line x1="{xb:.1f}" x2="{xb:.1f}" y1="{oy + 4 * k:.1f}" y2="{oy + 104 * k:.1f}" stroke="{a}" stroke-width="1.5"/>')
    lines.append(f'<text x="{xb - 6:.1f}" y="{oy + 54 * k + 5:.1f}" text-anchor="end" font-size="15" font-style="italic" font-weight="700" fill="{a}">x</text>')
    # clear space measure at the top: 1.0x
    lines.append(f'<line x1="{ox + W / 2:.1f}" x2="{ox + W / 2:.1f}" y1="{by0:.1f}" y2="{oy + ink_top:.1f}" stroke="{a}" stroke-width="1"/>')
    lines.append(f'<text x="{ox + W / 2 + 6:.1f}" y="{by0 + pad / 2 + 5:.1f}" font-size="13" fill="{a}">1.0x clear space</text>')
    # hinge white: ticks at H's right edge, B's ink and A's left edge
    for u in (360.07, 369.4, 462.69, 469.68):
        X = ox + u * k
        lines.append(f'<line x1="{X:.1f}" x2="{X:.1f}" y1="{oy + ink_bot + 4:.1f}" y2="{oy + ink_bot + 12:.1f}" stroke="{a}" stroke-width="1"/>')
    yb = oy + ink_bot + 12 + 16
    lines.append(f'<text x="{ox + 415 * k:.1f}" y="{yb:.1f}" text-anchor="middle" font-size="13" fill="{a}">0.203x of white on each side of B</text>')
    overlay = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt:.0f}" height="{H:.0f}" viewBox="0 0 {Wt:.0f} {H:.0f}" '
               f'style="position:absolute;left:0;top:0;font-family:var(--oa-font-family-reading)" aria-hidden="true" class="oai-svg">{"".join(lines)}</svg>')
    body = (f'<div class="oai-panel oai-s-newsprint">' + scroll(
        f'<div style="position:relative;width:{Wt:.0f}px;height:{H:.0f}px">{overlay}'
        f'<div style="position:absolute;left:{ox:.1f}px;top:{oy:.1f}px">{wm}</div></div>',
        "Wordmark construction at true size; scroll sideways on a narrow screen") + '</div>')
    alt = ("The Oath & Action wordmark at 480 pixels wide on Newsprint: OATH and ACTION in black capitals with a red "
           "ampersand between them. Guides mark the cap line and baseline, the cap height x, a clear-space box one cap height "
           "out from the letters on every side, and the equal white on each side of the ampersand, 0.203x.")
    return rec("s-03-1-correct", "03.1", int(Wt + 50), alt, body, role_img=alt,
               notes="Display master placed at 480 px wide (49.06 px capitals). Annotations are a guide overlay, not part of the mark.")


@spec
def s_03_1_failure():
    cap = 49.06
    fs = cap / 0.7275
    w = 600
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="96" viewBox="0 0 {w} 96" class="oai-svg" aria-hidden="true">'
           f'<text x="0" y="{24 + cap:.1f}" font-family="Inter Tight, Arial, sans-serif" font-weight="800" font-size="{fs:.1f}" fill="{ink("newsprint")}">'
           f'OATH <tspan fill="{sig("newsprint")}">&amp;</tspan> ACTION</text></svg>')
    body = ('<div class="oai-panel oai-s-newsprint">' + scroll(
        f'<span class="oai-red" data-red="signature" data-failure="true">{svg}</span>', "Failure case; scroll sideways on a narrow screen") + '</div>')
    alt = ("Failure case: OATH & ACTION typed in Inter Tight 800 with the font's own sans-serif ampersand colored red and "
           "ordinary word spaces, so the ampersand is a different shape and the gaps around it are wide and uneven.")
    return rec("s-03-1-failure", "03.1", 650, alt, body, role_img=alt,
               notes="Drawn as live SVG text inside a labeled image (D1-09), in the same cap height as the correct case.")


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
            + _tile(f'<span role="img" aria-label="Failure case: the full wordmark squeezed to 100 pixels wide">{wm}</span>', 120,
                    "Same tile, full wordmark at 100 px wide")
            + '</div></div>')
    alt = "Failure case: the same 120 pixel tile with the full OATH & ACTION wordmark squeezed to 100 pixels wide; its capitals are 10 pixels tall and blur."
    return rec("s-03-2-failure", "03.2", 200, alt, body, notes="Display master scaled to 100 px wide (10.2 px capitals), as a producer would drag it.")


@spec
def s_03_lockups():
    def item(name, job, minimum, inner, wide=False):
        cell = (f'<div class="oai-cell" style="gap:12px">'
                + scroll(f'<div style="min-height:24px;display:flex;align-items:flex-end;width:max-content">{inner}</div>', f"{name} at true size; scroll sideways on a narrow screen")
                + f'<p><b>{E(name)}</b></p><p class="oai-note">{E(job)}</p><p class="oai-tag">Minimum {E(minimum)}</p></div>')
        return f'<div class="oai-panel oai-s-newsprint" style="{"grid-column:1/-1" if wide else ""}">{cell}</div>'
    parts = [
        item("L1 Wordmark", "Most uses: page heads, documents, slides and signage.", "16 px tall (152 px wide); 1.20 in", wordmark(40, label="Oath & Action, L1 wordmark")),
        item("L2 Stacked", "Square formats and posters.", "90 px wide; 0.80 in", mark(L2["today"], w=200, label="Oath & Action, L2 stacked lockup")),
        item("L3 Horizontal with the lockmark", "The site and email masthead.", "196 px wide; 1.55 in", l3_small(24)),
        item("L4 Monogram and tagline", "Document footers and small print.", "304 px wide; 2.30 in", l4(330)),
        item("L5 Wordmark and tagline", "Covers, banners and partner placements where the tagline travels with the mark.", "388 px wide; 2.90 in", l5(400)),
        item("L7 Section masthead", "Names the pillar a piece serves, in the surface's ink.", "250 px wide with the longest pillar word; 1.90 in", l7(330, "TRACK")),
        item("L8 Monogram", "Small squares where the full name will not fit. Never a favicon.", "48 px wide; 0.50 in", mark(L8["today"], w=120, label="Oath & Action, L8 monogram")),
        item("L6 Editorial signature", "The sign-off strip at the foot of pages, emails and reports. Shown on Prussian, where every part is White.", "884 px wide; 6.60 in", l6(884), wide=True),
    ]
    css = (".oai-lockgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(420px,100%),1fr));gap:16px}"
           "@media (max-width:420px){.oai-lockgrid{grid-template-columns:1fr}}")
    body = f'<div class="oai-lockgrid">{"".join(parts)}</div>'
    alt = ("The eight lockups at true size on Newsprint, each with its job and minimum: L1 the wordmark; L2 stacked, OATH over ACTION "
           "with a large ampersand at right; L3 the wordmark with the lockmark grid at its right; L4 the O & A monogram, a hairline "
           "and the tagline on two lines; L5 the wordmark over the tagline; L7 the wordmark, a hairline and the word TRACK; L8 the "
           "monogram; and L6, a Prussian strip with the wordmark, tagline, four dots and lockmark all in White.")
    return rec("s-03-lockups", "03.2", 1000, alt, body, css=css,
               notes="L1, L2, L3 and L8 are masters. L4 to L7 are assembled here from the approved masters and re-exported taglines on V5's layouts (I8 note); their own masters are drawn after Gate 2. L6 leaves out the web address until the site is settled (DR-55). L7's pillar word is live text.")


# ------------------------------------------------------------------------------------------- 03.3
def _page_head(gap_px, failure=False):
    h = 32
    cap = 32 * 22 / 24
    wm = wordmark(h, decorative=True)
    zone = ""
    if not failure:
        cs = 32   # 1.0x rounded up to oa.space.400
        zone = (f'<span aria-hidden="true" style="position:absolute;left:{-cs}px;top:{-cs}px;width:calc(100% + {2 * cs}px);'
                f'height:{h + 2 * cs}px;border:1px solid {pal("stone")}"></span>'
                f'<span class="oai-tag" style="position:absolute;left:calc(100% + {cs + 8}px);top:{-cs - 2}px;white-space:nowrap">1.0x</span>')
    head = (f'<p class="oai-disp" style="font-size:28px;margin-top:{gap_px}px;max-width:22ch">What the county board decides on Tuesday</p>')
    return (f'<div style="padding:{40 if not failure else 24}px 48px 24px 40px">'
            f'<div style="position:relative;display:inline-block">{wm}{zone}</div>{head}'
            f'<p style="margin-top:8px">{illus()}</p></div>')


@spec
def s_03_3_correct():
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:0">{_page_head(40)}</div>'
    alt = ("A page head at true size: the wordmark 32 pixels tall with a box one cap height out on every side, and the "
           "headline What the county board decides on Tuesday set below the box. Illustrative.")
    return rec("s-03-3-correct", "03.3", 520, alt, body, illustrative=True,
               notes="24 px master drawn at 32 px tall (29 px capitals); clear space rounded up to 32 px, oa.space.400.")


@spec
def s_03_3_failure():
    inner = _page_head(9, failure=True)
    body = (f'<div class="oai-panel oai-s-newsprint" style="padding:0"><div role="img" aria-label="Failure case: the headline set 9 pixels under the wordmark, inside its clear space. Illustrative.">'
            f'{inner}</div></div>')
    alt = "Failure case: the same page head with the headline moved up to 9 pixels below the wordmark, inside its clear space, so the headline's first words read as part of the name. Illustrative."
    return rec("s-03-3-failure", "03.3", 520, alt, body, illustrative=True, notes="Headline 0.3x below the wordmark.")


# ------------------------------------------------------------------------------------------- 03.4
@spec
def s_03_4_correct():
    def it(label, inner, sub=""):
        return f'<div class="oai-cell">{inner}<span class="oai-tag">{E(label)}</span>{f"<span class=oai-tag>{E(sub)}</span>" if sub else ""}</div>'
    row1 = "".join([
        it("L1, 16 px tall, 152 px wide", wordmark(16, label="L1 at its minimum, 16 px tall")),
        it("L2, 90 px wide", mark(L2["today"], w=90, label="L2 at its minimum, 90 px wide")),
        it("L3, 196 px wide", l3_small(16, label="L3 at its minimum, 196 px wide")),
        it("L8, 48 px wide", mark(L8["today"], w=48, label="L8 at its minimum, 48 px wide")),
    ])
    row2 = "".join([
        it("Ampersand B, 16 px", amp(16, label="Ampersand B at its minimum, 16 px")),
        it("Lockmark, 16 px", lockmark(16, label="Lockmark at its minimum, 16 px")),
        it("Hinge-circle badge, 16 px", mark(BADGE[16], h=16, label="Hinge-circle badge at its minimum, 16 px")),
        it("Hinge diagram, compact, 245 px", mark(HINGE["compact"], w=245, label="Hinge diagram, compact master, at its minimum, 245 px wide")),
    ])
    row3 = "".join([
        it("L4, 304 px wide", l4(304)),
        it("L5, 388 px wide", l5(388)),
        it("L7, 250 px wide", l7(250, "CONNECT")),
    ])
    wide = it("Hinge diagram, display, 533 px", mark(HINGE["display"], w=533, label="Hinge diagram, display master, at its minimum, 533 px wide"))
    wide6 = it("L6, 884 px wide", l6(884))
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:32px">'
            f'<div class="oai-row">{row1}</div><div class="oai-row">{row2}</div><div class="oai-row">{row3}</div>'
            + scroll(f'<div class="oai-row" style="flex-wrap:nowrap">{wide}</div>', "The hinge diagram's display minimum at true size; scroll sideways on a narrow screen")
            + scroll(f'<div class="oai-row" style="flex-wrap:nowrap">{wide6}</div>', "L6 at its minimum, true size; scroll sideways")
            + '<p class="oai-note">Every mark here sits at its smallest allowed size, at true size. These are graphics, so the 13 px floor for text does not apply to the letters drawn inside them.</p>'
            '</div></div>')
    alt = ("Every identity mark at its screen minimum, at true size: the wordmark 16 pixels tall, the stacked lockup 90 wide, "
           "the horizontal lockup 196 wide, the monogram 48 wide, ampersand B, the lockmark and the badge at 16 pixels, the "
           "compact hinge diagram at 245 and the display one at 533, L4 at 304, L5 at 388, L7 at 250 and the L6 strip at 884.")
    return rec("s-03-4-correct", "03.4", 1000, alt, body,
               notes="Marks at true size are graphics (Stage A brief: the 13 px floor exempts a mark shown at its minimum, and the note says so).")


@spec
def s_03_4_failure():
    wm = mark(WM["display"], h=12, surface="newsprint", decorative=True)
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row mid">'
            f'<span role="img" aria-label="Failure case: the display wordmark scaled to 12 pixels tall">{wm}</span>'
            '<span class="oai-tag">Display master at 12 px tall</span></div></div>')
    alt = "Failure case: the wordmark's display master scaled down to 12 pixels tall, its capitals 11 pixels, the gaps around the ampersand filling in."
    return rec("s-03-4-failure", "03.4", 360, alt, body, notes="Display master at 12 px tall (11.1 px capitals), as an email footer might place it.")


@spec
def s_03_minimums():
    data = json.loads((ID_DIR / "20261028_Identity-Minimum-Sizes.json").read_text())
    rows = "".join(f'<tr><th scope="row">{E(r["lockup"])}</th><td>{E(r["screen"])}</td><td>{E(r["print"])}</td><td>{E(r["below"])}</td></tr>'
                   for r in data["rows"])
    table = (f'<table><caption class="oai-note" style="text-align:left;caption-side:top;padding-bottom:8px">{E(data["rule"])}</caption>'
             '<thead><tr><th scope="col">Mark</th><th scope="col">Screen minimum</th><th scope="col">Print minimum</th><th scope="col">Below the minimum</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    body = '<div class="oai-panel oai-s-newsprint">' + scroll(f'<div style="min-width:760px">{table}</div>', "Minimum sizes table; scroll sideways on a narrow screen") + '</div>'
    alt = "Table of minimum sizes on screen and in print for every identity mark, with the mark to use below each minimum."
    return rec("s-03-minimums", "03.4", 1000, alt, body,
               notes="Read word for word from work/build/assets/identity/20261028_Identity-Minimum-Sizes.json (I8).")


# ------------------------------------------------------------------------------------------- 03.5
@spec
def s_03_5_correct():
    cols = [("newsprint", "color", "Newsprint"), ("white", "color", "White"), ("charcoal", "color", "Charcoal"),
            ("prussian", "color", "Prussian, all White"), ("newsprint", "mono", "Mono, Charcoal"), ("charcoal", "mono", "Mono, Newsprint")]
    cells = []
    for s, m, name in cols:
        inner = (f'<div class="oai-stack" style="gap:20px;align-items:flex-start">'
                 f'{wordmark(22, surface=s, mode=m, label=f"L1 on {name}")}'
                 f'<div class="oai-row" style="gap:20px">{mark(L2["today"], w=110, surface=s, mode=m, label=f"L2 on {name}")}'
                 f'{mark(L8["today"], w=60, surface=s, mode=m, label=f"L8 on {name}")}</div></div>')
        cells.append(f'<div class="oai-panel oai-s-{s}">{inner}<p class="oai-tag" style="margin-top:16px">{E(name)}</p></div>')
    css = (".oai-matrix{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr));gap:12px}")
    body = f'<div class="oai-matrix">{"".join(cells)}</div>'
    alt = ("L1, L2 and L8 on six grounds at true size: Newsprint, White and Charcoal with the red ampersand; Prussian with "
           "every part White; and one-color versions in Charcoal on Newsprint and in Newsprint on Charcoal.")
    return rec("s-03-5-correct", "03.5", 1000, alt, body,
               notes="Prussian cells place the explicit-White files from prussian/ (treatment D, I9). L1 uses the 24 px master at 22 px tall.")


@spec
def s_03_5_failure():
    wm = mark(WM["display"], h=54, surface="newsprint", decorative=True)   # the Newsprint file, as dropped on Charcoal
    body = ('<div class="oai-panel oai-s-charcoal">'
            f'<span class="oai-red" data-red="signature" data-failure="true" role="img" aria-label="Failure case: the Newsprint wordmark file placed on Charcoal">{wm}</span></div>')
    alt = "Failure case: the Newsprint version of the wordmark placed on a Charcoal slide. The black letters disappear into the black ground and only the red ampersand shows."
    return rec("s-03-5-failure", "03.5", 560, alt, body, notes="Charcoal letters on Charcoal, 1:1.")


# ------------------------------------------------------------------------------------------- 03.6
def _nav(items, surface="newsprint"):
    return "".join(f'<span style="font:600 15px/1 var(--oa-font-family-reading);white-space:nowrap">{E(t)}</span>' for t in items)


@spec
def s_03_6_correct():
    desk = (f'<div class="oai-s-newsprint" style="width:1440px;height:80px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 64px;border-bottom:1px solid {hair("newsprint")}">{l3_small(24, label="Oath & Action")}'
            f'<nav aria-label="Specimen site navigation" style="display:flex;gap:32px">{_nav(["Explain", "Track", "Connect", "Act", "About"])}</nav></div>')
    burger = (f'<span aria-hidden="true" style="width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:center">'
              + "".join(f'<span style="width:20px;height:2px;background:{ink("newsprint")}"></span>' for _ in range(3)) + '</span>')
    phone = (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
             f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}">{wordmark(24, label="Oath & Action")}{burger}</div>')
    email = (f'<div class="oai-s-white" style="width:600px;height:96px;display:flex;align-items:center;padding:0 24px;'
             f'border:1px solid {hair("white")}">{l3_small(24, surface="white", label="Oath & Action")}</div>')
    body = ('<div class="oai-stack" style="gap:24px">'
            f'<div class="oai-cell">{scroll(desk, "Site masthead at 1440 px, true size; scroll sideways")}<span class="oai-tag">Site, 1440 px wide: L3 with the 24 px wordmark master and a 52 px lockmark</span></div>'
            f'<div class="oai-row top"><div class="oai-cell">{scroll(phone, "Phone masthead at 390 px, true size")}<span class="oai-tag">Phone, 390 px: L1 from the 24 px master</span></div>'
            f'<div class="oai-cell">{scroll(email, "Email header at 600 px, true size")}<span class="oai-tag">Email, 600 px: L3, sent as a PNG at twice size</span></div></div></div>')
    alt = ("Three mastheads at true size: a 1440 pixel site bar with the wordmark and lockmark at left and five navigation words "
           "at right; a 390 pixel phone bar with the wordmark and a menu button; and a 600 pixel white email header with the "
           "wordmark and lockmark.")
    return rec("s-03-6-correct", "03.6", 1440, alt, body,
               notes="Navigation words are placeholders for chapter 20. The email header is drawn live here; in email it ships as a PNG.")


@spec
def s_03_6_failure():
    l3m = mark(L3["today"], w=150, surface="newsprint", decorative=True)
    burger = (f'<span aria-hidden="true" style="width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:center">'
              + "".join(f'<span style="width:20px;height:2px;background:{ink("newsprint")}"></span>' for _ in range(3)) + '</span>')
    phone = (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
             f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}"><span role="img" aria-label="Failure case: L3 squeezed to 150 pixels wide">{l3m}</span>{burger}</div>')
    body = f'<div>{scroll(phone, "Failure case at true size")}</div>'
    alt = "Failure case: a 390 pixel phone bar with the L3 lockup squeezed to 150 pixels wide; its capitals are 12 pixels tall and the lockmark's nodes and links run together at 28 pixels."
    return rec("s-03-6-failure", "03.6", 400, alt, body, notes="L3 master at 150 px wide: 11.7 px capitals, 28 px lockmark.")


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
    body = (f'<div class="oai-panel oai-s-newsprint"><span class="oai-red" data-red="signature" data-failure="true" role="img" '
            f'aria-label="Failure case: O and A typed with word spaces around a font ampersand">{svg}</span></div>')
    alt = "Failure case: V4.2's compact signature, O & A typed in Inter Tight with word spaces and the font's sans-serif ampersand in red, at the same cap height as L8 at 120 pixels."
    return rec("s-03-7-failure", "03.7", 300, alt, body)


# ------------------------------------------------------------------------------------------- 03.8
def _partner(failure=False):
    h = 32
    cap = h * 22 / 24
    wm = wordmark(h, decorative=True)
    if not failure:
        g = round(0.6 * cap)
        inner = (f'<div style="display:flex;align-items:center;gap:{g}px">{wm}'
                 f'<span aria-hidden="true" style="width:1px;height:{round(cap + 6)}px;background:{hair("newsprint")}"></span>'
                 f'<span style="font:600 22px/1.15 var(--oa-font-family-reading);max-width:15ch">Merrimack Valley Civic Lab</span></div>')
        return (f'<div role="img" aria-label="Partnership lockup: the Oath &amp; Action wordmark, a vertical hairline, then the name Merrimack Valley Civic Lab. Illustrative partner.">'
                f'{inner}</div><p style="margin-top:12px">{illus("Illustrative partner")}</p>')
    a = amp(cap, decorative=True)
    inner = (f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">{wm}<span class="oai-red" data-red="signature" data-failure="true">{a}</span>'
             f'<span class="oai-disp" style="font-size:{cap / 0.7275:.1f}px;letter-spacing:-.02em;text-transform:uppercase">Merrimack Valley Civic Lab</span></div>'
             f'<p style="margin-top:16px;font-size:17px">present a workshop on public comment</p>')
    return (f'<div role="img" aria-label="Failure case: an event flyer joining Oath &amp; Action and Merrimack Valley Civic Lab with a second red ampersand. Illustrative.">'
            f'{inner}</div><p style="margin-top:12px">{illus()}</p>')


@spec
def s_03_8_correct():
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:32px">{_partner()}</div>'
    alt = "A partnership lockup at true size: the wordmark 32 pixels tall, a vertical hairline, then the partner name Merrimack Valley Civic Lab in semibold type. The partner is invented. Illustrative."
    return rec("s-03-8-correct", "03.8", 620, alt, body, illustrative=True,
               notes="Merrimack Valley Civic Lab is invented (Q-01) and labeled beside the item.")


@spec
def s_03_8_failure():
    body = f'<div class="oai-panel oai-s-newsprint" style="padding:32px">{_partner(True)}</div>'
    alt = "Failure case: an event flyer that reads OATH & ACTION & MERRIMACK VALLEY CIVIC LAB present a workshop on public comment, with a second red ampersand joining the two names. Illustrative."
    return rec("s-03-8-failure", "03.8", 900, alt, body, illustrative=True)


@spec
def s_03_misuse():
    def case(title, inner):
        return (f'<div class="oai-panel oai-s-newsprint oai-cell" style="gap:16px"><div style="min-height:70px;display:flex;align-items:center">{inner}</div>'
                f'<p class="oai-note" style="color:var(--oa-color-text-primary-on-newsprint)">{title}</p></div>')
    stretched = mark(WM["display"], w=330, h=(330 / 1.3) * 108 / 978.31, decorative=True, extra=' preserveAspectRatio="none"')
    shadow = f'<span style="display:inline-block;filter:drop-shadow(3px 4px 3px rgba(18,18,18,.55))">{mark(WM["display"], w=300, decorative=True)}</span>'
    recolor = svg_file(ID_DIR / WM["display"], w=300, decorative=True,
                       style=f"color:{ink('newsprint')};--amp:{pal('prussian')}")
    cases = [
        case("<b>Stretched to fill a banner.</b> A slide app's corner handle pulled the mark 30 percent wider; the round letters turn oval.",
             f'<span role="img" aria-label="Failure case: the wordmark stretched 30 percent wider">{stretched}</span>'),
        case("<b>A drop shadow from a design app's effects menu.</b> The edges blur and the mark looks pasted on.",
             f'<span class="oai-red" data-red="signature" data-failure="true" role="img" aria-label="Failure case: the wordmark with a drop shadow">{shadow}</span>'),
        case("<b>The ampersand recolored to match a partner's blue.</b> The red joint of the name is gone, and Prussian sits in a job it does not have.",
             f'<span role="img" aria-label="Failure case: the wordmark with its ampersand recolored Prussian">{recolor}</span>'),
    ]
    css = ".oai-mis{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:12px}"
    body = f'<div class="oai-mis">{"".join(cases)}</div>'
    alt = "Three more failure cases at true size: the wordmark stretched 30 percent wider, the wordmark with a drop shadow, and the wordmark with its ampersand recolored dark blue."
    return rec("s-03-misuse", "03.8", 1000, alt, body,
               notes="Extras: three failures producers make in slide and design apps. Placement attributes only; the master is unchanged.")
