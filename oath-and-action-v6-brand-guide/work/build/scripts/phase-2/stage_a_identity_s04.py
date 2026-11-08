"""Chapter 04 The Ampersand and the hinge: specimens.

Apply pass, November 7, 2026: an article ends with B alone in the text's ink, and the badge keeps sizes from 48 px for
back covers and events (DR-118); Rule 04.6's failure shows the badge at 16 px read as the registered trademark sign.

Q1 to Q4 pass, November 8, 2026 (DR-130, CD-N8): the end mark stands at the text's cap height at every size, B's band
on the capitals, as plate (a) on the changes board drew it, under B's 16 px minimum in body text by exception.

Fix pass, November 6, 2026: hinge headlines come from Rule 02.27's correct list and set in the scale's styles at their
fixed sizes (BE-M6, CP-M4, C-M7, D2-254); the Act card reads "The route plan & your commute." with the kicker
"Act · How to take part" (D2-250); cards are drawn at a phone column's 358 px, so they fit a phone at true size (C-S7);
B's sizes share one baseline and the 16 px master shows as pixels at four times (C-S13); the divider centers B on a line
as wide as the text it divides (DR-96, C-M2); "reports the bill out" is glossed (CP-M9)."""
from stage_a_identity_lib import (E, ID_DIR, AMP, BADGE, HINGE, LORA, WM, fragment, mark, wordmark, amp, illus, head_label,
                                  tag, svg_file, ink, ink2, hair, pal, tv, sig, strong, ground, ty, raster_png, inline_master, dnp,
                                  figures)
from stage_a_identity_s03 import rec as _rec, markrow, MARKROW_CSS

S = []


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "04")
    return _rec(*a, **k)


CAP = 0.7275   # Inter Tight cap height, in em
PHONE = 358    # a 390 px phone's column after 16 px margins: the width a phone shows a card or a feed preview


def hinge_amp(font_px, surface="newsprint", red=True, job="the one point the headline names"):
    """B set inside a line of Inter Tight 800 at a font size: its cap band on the text's cap band, its baseline on the
    baseline. The 16 and 24 px masters fill their box with 1 px of overshoot top and bottom (14 and 22 px capitals);
    the display master's box runs 1.34 units above the cap line and 1.35 below the baseline (cap height 100)."""
    cap = font_px * CAP
    if cap < 24:                 # Rule 04.1's ranges: 16 px master to 23 px, 24 px master to 47 px, display from 48 px
        f, h, below = AMP[16], cap * 16 / 14, cap / 14
    elif cap < 48:
        f, h, below = AMP[24], cap * 24 / 22, cap / 22
    else:
        f, h, below = AMP["display"], cap * 1.0269, cap * 0.0135
    color = (tv("color-palette-pillar-red") if red else ink(surface))
    svg = svg_file(ID_DIR / f, h=h, decorative=True, style=f"color:{color};display:inline-block;vertical-align:{-below:.2f}px")
    if red:
        return f'<span class="oai-red" data-red="working" data-red-job="{E(job)}" style="line-height:0">{svg}</span>'
    return svg


def headline(text_a, text_b, style="h3", board=600, surface="newsprint", red=True, extra_style="", br=True):
    """A hinge headline in a style of the type scale at its fixed size on a board of a given width (D2-254). It breaks
    at the hinge, so B leads the second line and a line break never splits a noun phrase (C-S14)."""
    from stage_a_identity_lib import FLOOR, CEIL
    px = (CEIL if board >= 1200 else FLOOR)[style]
    a = hinge_amp(px, surface, red)
    first = E(text_a).replace(" ", "&nbsp;") if br else E(text_a)
    b = E(text_b).replace(" ", "&nbsp;")
    return (f'<p style="{ty(style, board)};{extra_style}">'
            f'{first}{"<br>" if br else " "}<span style="white-space:nowrap"><span role="img" aria-label="and" style="display:inline-block">{a}</span>&nbsp;{b}</span></p>')


def divider(surface="newsprint", red=False):
    """The hinge divider (DR-96): B's 24 px master at 24 px, centered on a 1 px line that runs the full width of the
    text block it divides, with 12 px of clear line on each side of B, line and B in the surface's ink. red=True draws
    our fifth edition's red version for a failure case."""
    if red:
        b = (f'<span class="oai-red" data-red="working" data-red-job="divider" data-failure="true" style="line-height:0">'
             f'{svg_file(ID_DIR / AMP[24], h=24, decorative=True, style="color:" + tv("color-palette-pillar-red"))}</span>')
    else:
        b = svg_file(ID_DIR / AMP[24], h=24, decorative=True, style=f"color:{tv('color-identity-hinge-divider-on-' + surface)}")
    line = f'<span aria-hidden="true" style="flex:1;height:1px;background:{tv("color-identity-hinge-divider-on-" + surface) if not red else hair(surface)}"></span>'
    return f'<div aria-hidden="true" style="display:flex;align-items:center;gap:12px;margin:24px 0">{line}{b}{line}</div>'


def ask(label, surface="newsprint", red=True):
    if red:
        kl = f"box-shadow:0 0 0 1px {strong(surface)};" if surface in ("newsprint", "white") else ""
        return (f'<span class="oai-red" data-red="working" data-red-job="the step a reader can take now" style="display:inline-block;line-height:1.2">'
                f'<span style="display:inline-block;padding:12px 20px;background:{tv("color-action-ask-fill-on-" + surface)};color:{tv("color-action-ask-label-on-" + surface)};'
                f'{ty("ask")};{kl}">{E(label)}</span></span>')
    return (f'<span style="display:inline-block;padding:12px 20px;background:{tv("color-action-primary-fill-on-" + surface)};color:{tv("color-action-primary-label-on-" + surface)};'
            f'{ty("ask")}">{E(label)}</span>')


def kicker(text, surface="newsprint"):
    return f'<p style="{ty("label")};color:{ink2(surface)}">{E(text)}</p>'


# ------------------------------------------------------------------------------------------- 04.1
def _px16():
    """The 16 px master rendered by Chromium at 1x on Newsprint, then shown at four times with nearest-neighbor scaling,
    so each screen pixel reads as a square (C-S13)."""
    svg = inline_master(AMP[16], 16, style="color:var(--oa-color-identity-signature-on-newsprint)")
    w = round(16 * 14 / 16)
    uri = raster_png(svg, w, 16, "amp16", scale=1)
    return (f'<img src="{uri}" width="{w * 4}" height="64" alt="" style="display:block;image-rendering:pixelated;'
            f'image-rendering:crisp-edges">')


@spec
def s_04_1_correct():
    grid = "".join(f'<line x1="{i}" x2="{i}" y1="0" y2="16" />' for i in range(15)) + "".join(f'<line x1="0" x2="14" y1="{j}" y2="{j}" />' for j in range(17))
    outline = (f'<span style="position:relative;display:inline-block;width:56px;height:64px">'
               f'{mark(AMP[16], h=64, decorative=True)}'
               f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 16" width="56" height="64" aria-hidden="true" class="oai-svg" '
               f'style="position:absolute;left:0;top:0" stroke="{pal("stone")}" stroke-width="0.04">{grid}</svg></span>')

    def down(h):            # how far the display master's box runs below the baseline, at a height
        return h * 1.35 / 102.69

    def sit(m, off):
        return f'<span style="position:relative;top:{off:.2f}px">{m}</span>'
    row = markrow([
        (sit(mark(AMP["display"], h=160, label="Ampersand B, display master, 160 px tall"), down(160)), ["Display master, 160 px"]),
        (sit(mark(AMP["display"], h=48, label="Ampersand B at 48 px"), down(48)), ["48 px, display master"]),
        (sit(mark(AMP[24], h=24, label="Ampersand B, 24 px master"), 1), ["24 px master"]),
        (sit(mark(AMP[16], h=16, label="Ampersand B, 16 px master"), 1), ["16 px master"]),
    ], 162)
    enlarged = markrow([
        (_px16(), ["16 px master as Chromium draws it,", "enlarged four times"]),
        (outline, ["Its outline on the pixel grid,", "enlarged four times"]),
    ], 64)
    body = (f'<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:32px">{row}'
            f'<div style="border-top:1px solid {hair("newsprint")};padding-top:24px">{enlarged}</div></div></div>')
    alt = ("Ampersand B in Pillar Red at true size, every size on one baseline: the display master 160 pixels tall, then at "
           "48, 24 and 16 pixels. Below, enlarged four times, the 16 pixel master as the browser draws it in square pixels, "
           "and its outline over the pixel grid, with its two open counters.")
    return rec("s-04-1-correct", "04.1", None, alt, body, css=MARKROW_CSS,
               notes="A sheet that flows. Each B sits on one baseline: the display master's box runs 1.35 units below it, the small "
                     "masters' 1 px. The pixel view is a PNG Chromium rendered at 1x, scaled four times with image-rendering pixelated.")


@spec
def s_04_1_failure():
    lora = mark(LORA, h=160, decorative=True)
    body = (f'<div class="oai-panel oai-s-newsprint"><div class="oai-row">{lora}'
            '<span class="oai-tag">Our fifth edition\'s ampersand, Lora Bold\'s glyph, 160 px</span></div></div>')
    alt = ("Failure case: the ampersand from our brand guide's fifth edition, the unmodified Lora Bold glyph that any Lora "
           "user can type, in red at 160 pixels tall. It has no beak, and its strokes are more even than B's.")
    return rec("s-04-1-failure", "04.1", 420, alt, body, notes="V5's glyph placed from the re-exported I1 record file, as an old Edition 05 file would place it.")


# ------------------------------------------------------------------------------------------- 04.2
def _card(extra_crop=False, extra_free=False):
    W, H = PHONE, 188
    crop = ""
    if extra_crop:
        crop = (f'<span aria-hidden="true" style="position:absolute;right:-44px;bottom:-56px">'
                f'{mark(AMP["display"], h=160, mode="ink", decorative=True)}</span>')
    free = f'<span style="margin-left:10px">{mark(AMP[16], h=16, decorative=True)}</span>' if extra_free else ""
    return (f'<div class="oai-s-newsprint" style="position:relative;overflow:hidden;width:{W}px;height:{H}px;padding:20px 20px;'
            f'border:1px solid {hair("newsprint")}">'
            f'{headline("The zoning code", "the rent.", "h3")}'
            f'<p style="margin-top:8px;{ty("body")};max-width:30ch">Who decides what can be built near you.</p>'
            f'<div style="position:absolute;left:20px;bottom:18px;display:flex;align-items:center">{wordmark(16, label="Oath & Action")}{free}</div>'
            f'{crop}</div>')


@spec
def s_04_2_correct():
    body = f'<div>{head_label()}{_card()}</div>'
    alt = ("A link card at 358 by 188 pixels, the size a phone feed shows it: the hinge headline The zoning code & the rent. "
           "with one red ampersand, a line under it, and the wordmark at the foot. Illustrative.")
    return rec("s-04-2-correct", "04.2", PHONE, alt, body, illustrative=True,
               notes="A 1200 by 630 link preview as a 390 px phone's feed draws it, 358 by 188 px, so it fits a phone at true size. "
                     "H3 at 26 px and body at 17 px, the phone floor (D2-254). The headline is chapter 02's hinge example.")


@spec
def s_04_2_failure():
    body = f'<div>{head_label()}{_card(extra_crop=True, extra_free=True)}</div>'
    alt = ("Failure case: the same card with a large cropped ampersand in the corner and a second small ampersand beside the "
           "wordmark, so three ampersands compete with the headline's. Illustrative.")
    return rec("s-04-2-failure", "04.2", PHONE, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 04.3
@spec
def s_04_3_correct():
    def lab(t):
        return f'<p class="oai-tag" style="margin-top:6px">{E(t)}</p>'
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:28px">'
            f'<div>{headline("The zoning code", "the rent.", "title")}{lab("Title style, 56 px")}</div>'
            f'<div>{headline("The filing deadline", "the ballot.", "section")}{lab("Section style, 44 px")}</div>'
            f'<div>{headline("The records law", "the answer.", "h3")}{lab("H3 style, 26 px")}</div>'
            '</div></div>')
    alt = ("Three hinge headlines at true size in heavy type, each naming a rule and then what it produces, joined by a red "
           "ampersand B that leads the second line: The zoning code & the rent. at 56 pixels, The filing deadline & the "
           "ballot. at 44, and The records law & the answer. at 26.")
    return rec("s-04-3-correct", "04.3", 600, alt, body,
               notes="Headlines from Rule 02.27's correct list (BE-M6, CP-M4), in the title, section and H3 styles at the phone floor "
                     "for a 600 px column (D2-254). B comes from the master whose range holds each cap height: the 24 px master at 56 "
                     "and 44 px type, the 16 px master at 26 px.")


def _act_card(red_amp):
    return (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:20px;border:1px solid {hair("newsprint")}">'
            f'{kicker("Act · How to take part")}'
            f'{headline("The route plan", "your commute.", "h3", red=red_amp, extra_style="margin-top:8px")}'
            f'<p style="margin-top:10px;{ty("body")}">The transit board votes on the new bus routes March 12. Comments close March 9.</p>'
            f'<div style="margin-top:18px">{ask("Send a comment")}</div></div>')


@spec
def s_04_3_failure():
    body = f'<div>{head_label()}{_act_card(True)}</div>'
    alt = ("Failure case: an Act card whose hinge headline The route plan & your commute. has a red ampersand above a red "
           "Send a comment button, two working reds in one view. Illustrative.")
    return rec("s-04-3-failure", "04.3", PHONE, alt, body, illustrative=True, check_exempt=["red"],
               notes="The failure is two working reds in one view, so check_exempt red. Kicker per D2-250.")


@spec
def s_04_3_corrective():
    body = f'<div>{head_label()}{_act_card(False)}</div>'
    alt = ("The same Act card corrected: the headline's ampersand in Charcoal and the Send a comment button in red, so the "
           "step to take is the one red mark. Illustrative.")
    return rec("s-04-3-corrective", "04.3", PHONE, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 04.4
@spec
def s_04_4_correct():
    art = (f'<div class="oai-s-newsprint" style="max-width:560px;padding:24px 28px;border:1px solid {hair("newsprint")};{ty("body")}">'
           f'{head_label()}'
           f'<p>The committee votes on whether to report the bill out, which sends it to the full House. The House then has 30 days to take it up, or the bill waits for the next session.</p>'
           f'{divider("newsprint")}'
           f'<p><b>What you can do.</b> The committee takes written testimony until March 27. Send it to the committee clerk, and include your town.</p></div>')
    strips = "".join(
        f'<div class="oai-cell"><div class="oai-s-{s}" style="width:300px;max-width:100%;padding:0 20px;border:1px solid {hair(s)}">{divider(s)}</div><span class="oai-tag">{n}</span></div>'
        for s, n in (("newsprint", "Charcoal on Newsprint"), ("white", "Charcoal on White"), ("charcoal", "Newsprint on Charcoal"), ("prussian", "White on Prussian")))
    body = f'<div class="oai-pad"><div class="oai-stack" style="gap:24px">{art}<div class="oai-row top">{strips}</div></div></div>'
    alt = ("An article passage: a paragraph on how a bill leaves committee, then the hinge divider, a thin line as wide as the "
           "text with a small ampersand at its center, then What you can do. with the testimony deadline. The passage is "
           "Illustrative. Below, the divider on Newsprint, White, Charcoal and Prussian, its line and ampersand in each "
           "surface's ink.")
    return rec("s-04-4-correct", "04.4", None, alt, body, illustrative=True,
               notes="Page text that flows, so the passage reflows on a phone. Divider per DR-96: B's 24 px master at 24 px, centered "
                     "on a 1 px line as wide as the text block, 12 px of clear line each side, 24 px above and below.")


@spec
def s_04_4_failure():
    art = (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:20px;border:1px solid {hair("newsprint")};{ty("body")}">'
           f'{head_label()}<p>The committee votes on whether to report the bill out, which sends it to the full House.</p>{divider("newsprint", red=True)}'
           f'<p><b>What you can do.</b> Written testimony is open until March 27.</p><div style="margin-top:16px">{ask("Send testimony")}</div></div>')
    body = f'<div>{art}</div>'
    alt = ("Failure case: our fifth edition's hinge divider with a red ampersand, above a red Send testimony button, so two "
           "red marks compete for the step. Illustrative.")
    return rec("s-04-4-failure", "04.4", PHONE, alt, body, illustrative=True, check_exempt=["red"],
               notes="The failure is V5's red divider beside a red ask, so check_exempt red.")


# ------------------------------------------------------------------------------------------- 04.5
@spec
def s_04_5_correct():
    disp = mark(HINGE["display"], w=600, label="The hinge diagram, display master: OATH and ACTION on a line with four nodes, ampersand B in a ring, two solid clockwise arcs, UNDERSTAND and IMPACT beneath")
    comp = mark(HINGE["compact"], w=280, label="The hinge diagram, compact master")
    compc = mark(HINGE["compact"], w=280, surface="charcoal", label="The hinge diagram, compact master on Charcoal")
    body = ('<div class="oai-stack" style="gap:16px">'
            f'<div class="oai-panel oai-s-newsprint">{disp}<p class="oai-tag" style="margin-top:12px">Display master, 600 px</p></div>'
            f'<div class="oai-row top"><div class="oai-panel oai-s-newsprint">{comp}<p class="oai-tag" style="margin-top:12px">Compact master, 280 px</p></div>'
            f'<div class="oai-panel oai-s-charcoal">{compc}<p class="oai-tag" style="margin-top:12px">Compact master on Charcoal</p></div></div></div>')
    alt = ("The hinge diagram at true size: the display master 600 pixels wide on Newsprint, with OATH and ACTION on a line "
           "through four nodes, a red ampersand B in a ring between them, two solid arcs running clockwise and the words "
           "UNDERSTAND and IMPACT beneath; and the compact master at 280 pixels on Newsprint and on Charcoal.")
    return rec("s-04-5-correct", "04.5", 650, alt, body)


@spec
def s_04_5_failure():
    css = ".oai-dash path[stroke],.oai-dash circle[stroke]{stroke-dasharray:9 5}"
    d = mark(HINGE["display"], w=600, decorative=True, cls="oai-dash")
    body = f'<div class="oai-panel oai-s-newsprint">{d}</div>'
    alt = ("Failure case: the hinge diagram redrawn with dashed arcs and a dashed ring. In our systems atlas's key a dashed "
           "line means a plausible link, so the diagram reads as a guess.")
    return rec("s-04-5-failure", "04.5", 650, alt, body, css=css,
               notes="The master is placed unchanged; a dash pattern applied to its strokes at placement shows the failure.")


# ------------------------------------------------------------------------------------------- 04.6
END_TEXT = ("The board meets again on April 2, and the agenda posts a week before. We will add the vote to the tracker once "
            "the clerk publishes the minutes.")
CAP_EM = 0.7275          # Inter's cap height in em

# The registered trademark sign, U+00AE, from Liberation Sans Regular (SIL Open Font License), in font units (2048 to the
# em, y up), read with fontTools on November 7, 2026. Drawn as outlines, so the comparison never depends on a viewer's
# fonts. Advance 1509 units; ink from y -16 to 1430.
REG_PATH = ("M1477 707Q1477 514 1380.5 345.5Q1284 177 1115.5 80.5Q947 -16 754 -16Q557 -16 387.5 84.5Q218 185 124.5 351.5Q31 518 31 707Q31 900 128.0 1068.0Q225 1236 393.0 1333.0Q561 1430 754 1430Q948 1430 1116.5 1332.5Q1285 1235 1381.0 1068.0Q1477 901 1477 707ZM1385 707Q1385 876 1301.0 1020.5Q1217 1165 1070.5 1250.0Q924 1335 754 1335Q586 1335 440.0 1250.5Q294 1166 210.0 1020.0Q126 874 126 707Q126 538 210.5 392.0Q295 246 440.0 162.0Q585 78 754 78Q923 78 1070.0 162.0Q1217 246 1301.0 392.0Q1385 538 1385 707ZM955 289 756 625H595V289H468V1120H775Q917 1120 992.5 1057.0Q1068 994 1068 883Q1068 781 1016.0 719.5Q964 658 879 639L1100 289ZM941 881Q941 950 893.5 986.0Q846 1022 765 1022H595V721H777Q857 721 899.0 763.5Q941 806 941 881Z")


def end_b(font_px=17, surface="newsprint"):
    """B alone as an article's end mark at the text's cap height (DR-130): B's band, its master's capitals (the 16 px
    master's y 1 to 15), on the text's capitals at every size, with the master's lowest row under the baseline as the
    master draws it. B comes from the master whose range holds its height (Rule 04.1), and from the 16 px master under
    16 px, the end mark's one exception to B's minimum (Rule 03.4). In Inter that is 0.831 em tall with vertical-align
    -0.052 em. Half an em before it, inside the last word's no-wrap span (CA-S4)."""
    cap = font_px * CAP_EM
    if cap * 16 / 14 < 24:
        f, h, below = AMP[16], cap * 16 / 14, cap / 14
    elif cap * 24 / 22 < 48:
        f, h, below = AMP[24], cap * 24 / 22, cap / 22
    else:
        f, h, below = AMP["display"], cap * 1.0269, cap * 0.0135
    return svg_file(ID_DIR / f, h=h, decorative=True,
                    style=f"color:{ink(surface)};display:inline-block;vertical-align:{-below:.3f}px;margin-left:0.5em")


def end_figures(text_px):
    """The end mark's figures at a text size, as stage_a_identity_q_measure.py measured them in Chromium at eight times."""
    f = figures("endmark")
    return (f or {}).get("measured_at_8x", {}).get(str(text_px))


def end_badge():
    return (f'<span class="oai-red" data-red="signature" data-failure="true" style="display:inline-block;line-height:0;vertical-align:-3px">'
            f'{svg_file(ID_DIR / BADGE[16], h=16, decorative=True, style="color:" + tv("color-identity-signature-on-newsprint"))}</span>')


def registered(font_px=17, surface="newsprint"):
    """The registered sign drawn from Liberation Sans's outline at a font size, on the text's baseline."""
    k = font_px / 2048
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1430 1509 1446" width="{1509 * k:.2f}" height="{1446 * k:.2f}" '
            f'aria-hidden="true" focusable="false" class="oai-svg" style="display:inline-block;vertical-align:{-16 * k:.2f}px">'
            f'<path transform="scale(1,-1)" fill="{ink(surface)}" d="{REG_PATH}"/></svg>')


def _ending(mark_html, surface="newsprint", gap=True):
    """A paragraph whose last word and end mark never break apart. gap=False keeps the old word space (the failure)."""
    head, last = END_TEXT.rsplit(" ", 1)
    sep = "" if gap else "&nbsp;"
    return f'<p>{E(head)} <span style="white-space:nowrap">{E(last)}{sep}{mark_html}</span></p>'


def _article(mark_html, surface="newsprint", gap=True, label=True):
    return (f'<div class="oai-s-{surface}" style="width:100%;padding:24px 28px;border:1px solid {hair(surface)};{ty("body")}">'
            f'{head_label() if label else ""}{_ending(mark_html, surface, gap)}</div>')


@spec
def s_04_6_correct():
    card = (f'<div class="oai-s-charcoal" style="width:384px;height:576px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px">'
            f'{mark(BADGE["display"], h=96, surface="charcoal", label="Hinge-circle badge, 96 px, on the back of an event card")}</div>')
    body = (f'<div class="oai-pad"><div class="oai-stack" style="gap:32px">'
            f'<div class="oai-stack" style="gap:12px">{_article(end_b())}{_article(end_b(surface="charcoal"), "charcoal", label=False)}'
            f'<span class="oai-tag">The end mark: B alone at the text\'s cap height, in the text\'s ink, half an em after the period</span></div>'
            f'<div class="oai-cell">{card}<span class="oai-tag">The badge at 96 px on the back of a 4 by 6 in event card, true size</span></div></div></div>')
    m = end_figures(17) or {"capitals_px": 0, "b_px": 0, "top_over_cap_line_px": 0, "tail_under_baseline_px": 0}
    alt = ("At true size, the last lines of an article in 17 pixel body text, on Newsprint and again on Charcoal, each ending "
           "with ampersand B alone in the text's ink, half an em after the final period. B stands at the text's cap height: "
           f"{m['b_px']:.1f} pixels tall beside capitals {m['capitals_px']:.1f} pixels tall, its curves running "
           f"{m['top_over_cap_line_px']:.1f} pixels over the cap line and {m['tail_under_baseline_px']:.1f} under the baseline. "
           "Below, the hinge-circle badge, a red ampersand B inside a thin red ring, at 96 pixels centered on the Charcoal back "
           "of a 4 by 6 inch event card. The article text is Illustrative.")
    return rec("s-04-6-correct", "04.6", 560, alt, body, illustrative=True, fit_switch=True,
               notes="DR-130, CD-N8 and CA-S4. B at the text's cap height, as plate (a) on the changes board: its band, the 16 px "
                     "master's y 1 to 15, on the capitals, so B is 16/14 of the cap height tall with vertical-align at minus 1/14 of "
                     "the cap height, in the text's ink. Under B's 16 px minimum by the end mark's exception (Rule 03.4). Measured in "
                     f"Chromium at eight times beside a capital H of 17 px Inter: capitals {m['capitals_px']:.1f} px, B {m['b_px']:.1f} px, "
                     f"its top {m['top_over_cap_line_px']:.1f} px over the cap line, its tail {m['tail_under_baseline_px']:.1f} px under the "
                     "baseline (work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json). Half an em of margin before B, inside a "
                     "no-wrap span with the last word. The plate is padded 24 px, so its tags and the event card stand clear of the "
                     "frame (CD-S4, CA-S5).")


@spec
def s_04_6_failure():
    def pair():
        return (f'<div style="display:flex;gap:24px;align-items:baseline;white-space:nowrap;width:max-content;{ty("body")}">'
                f'<span>minutes.&nbsp;{end_badge()}</span><span>minutes.&nbsp;{registered()}</span></div>')
    twice = f'<div style="width:{2 * 196}px;height:52px"><div style="transform:scale(2);transform-origin:0 0;width:max-content">{pair()}</div></div>'
    frame = (f'<div style="border:1px solid {hair("newsprint")}">{_article(end_badge(), gap=False).replace("border:1px solid", "border:0 solid", 1)}'
             f'<div class="oai-s-newsprint" style="border-top:1px solid {hair("newsprint")};padding:20px 28px 24px">'
             f'<div class="oai-stack" style="gap:20px">'
             f'<div class="oai-cell">{pair()}<span class="oai-tag">The badge, then the registered trademark sign, true size</span></div>'
             f'<div class="oai-cell">{twice}<span class="oai-tag">The same, enlarged twice</span></div></div></div></div>')
    body = f'<div class="oai-pad">{dnp()}{frame}</div>'
    alt = ("Failure case: do not publish. The same article ending with the hinge-circle badge, a red B inside a red ring, at "
           "16 pixels after the final period. Below, the words minutes. followed by the badge, then minutes. followed by the "
           "registered trademark sign, at true size and enlarged twice: at this size the two read as the same kind of mark. Illustrative.")
    return rec("s-04-6-failure", "04.6", 560, alt, body, illustrative=True, fit_switch=True,
               notes="The badge's 16 px master after the last word with a word space, as the end mark stood before DR-118. The comparison "
                     "is live: 17 px Inter, the badge's master and the registered sign drawn from Liberation Sans's outline (SIL Open "
                     "Font License), the form most typefaces draw, so only the marks differ (CA-S5). The twice-size row is a CSS "
                     "transform of vector drawings, sharp on any screen. Failure band per D2-308 (CA-S6). Padded 24 px (CA-S5).")


# ------------------------------------------------------------------------------------------- 04.7
def _tile(size, shape="circle", surface="charcoal", keyline=False):
    b = 0.58 * size
    key = AMP["display"] if b >= 48 else (AMP[24] if b >= 24 else AMP[16])
    if surface == "charcoal":
        fill, mk = tv("component-avatar-tile"), mark(key, h=b, surface="charcoal", decorative=True)
    elif surface == "prussian":
        fill, mk = ground("prussian"), mark(key, h=b, surface="prussian", decorative=True)
    elif surface == "mono":
        fill, mk = ground("white"), mark(key, h=b, mode="mono", decorative=True)
    else:
        fill, mk = ground(surface), mark(key, h=b, surface=surface, decorative=True)
    rad = "50%" if shape == "circle" else f"{0.2237 * size:.1f}px"
    kl = f"box-shadow:inset 0 0 0 1px {pal('charcoal')};" if keyline else ""
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;border-radius:{rad};'
            f'background:{fill};{kl}flex:none">{mk}</span>')


@spec
def s_04_7_correct():
    row1 = markrow([(_tile(180), ["Avatar, 180 px"]), (_tile(64), ["64 px"]), (_tile(32), ["32 px"]),
                    (_tile(180, "square"), ["App icon, 180 px"]), (_tile(64, "square"), ["64 px"])], 180)
    fav = (f'<span style="display:inline-flex;gap:8px;align-items:center;padding:8px 12px;background:{ground("white")};border:1px solid {hair("white")}">'
           f'{mark(AMP[16], h=16, surface="white", label="Favicon: ampersand B, 16 px master")}<span style="{ty("caption")}">Oath &amp; Action</span></span>'
           f'<span style="display:inline-flex;gap:8px;align-items:center;padding:8px 12px;background:{ground("charcoal")};color:{ink("charcoal")}">'
           f'{mark(AMP[16], h=16, surface="charcoal", label="Favicon on a dark browser tab")}<span style="{ty("caption")}">Oath &amp; Action</span></span>')
    row2 = markrow([(_tile(64, surface="newsprint", keyline=True), ["Newsprint with a 1 px Charcoal keyline,", "for dark app themes"]),
                    (_tile(64, surface="prussian"), ["Prussian, B in White"]),
                    (_tile(64, surface="mono", keyline=True), ["One color, for one-color print"]),
                    (f'<div class="oai-row" style="gap:8px">{fav}</div>', ["Favicon, 16 px master, light and dark tabs"])], 64)
    body = f'<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:32px">{row1}{row2}</div></div>'
    alt = ("Avatars and app icons at true size: ampersand B in red on a Charcoal circle at 180, 64 and 32 pixels and on a "
           "Charcoal rounded square at 180 and 64; then a Newsprint circle with a thin Charcoal keyline, a Prussian circle with "
           "a White ampersand, a one-color circle, and the 16 pixel ampersand as a favicon on a light and a dark browser tab.")
    return rec("s-04-7-correct", "04.7", None, alt, body, css=MARKROW_CSS,
               notes="A sheet that flows. B at 58 percent of the tile (V5's container proportion). The rounded square's corner is a "
                     "placeholder radius; iOS and Android cut their own mask from a full-bleed square upload.")


@spec
def s_04_7_failure():
    feed = (f'<div class="oai-s-white" style="width:{PHONE}px;padding:16px;display:flex;gap:12px;align-items:center;border:1px solid {hair("white")}">'
            f'{_tile(48, surface="newsprint")}<div><p style="{ty("ui")}">Oath &amp; Action</p><p style="{ty("caption")};color:{ink2("white")}">Posted a link</p></div></div>')
    body = f'<div>{feed}</div>'
    alt = ("Failure case: a Newsprint circle avatar with no keyline in a white feed. The circle's edge measures 1.41 to 1 "
           "against the page and fades, so the ampersand floats without its tile.")
    return rec("s-04-7-failure", "04.7", PHONE, alt, body)


# ------------------------------------------------------------------------------------------- 04.8
def _cover(crop_ok=True):
    W, H = 528, 816
    if crop_ok:
        crop = (f'<span aria-hidden="true" style="position:absolute;right:-142px;bottom:-30px">'
                f'{mark(AMP["display"], h=440, mode="ink", decorative=True)}</span>')
    else:
        crop = (f'<span aria-hidden="true" style="position:absolute;left:-40px;top:70px">'
                f'{mark(AMP["display"], h=480, mode="ink", decorative=True)}</span>')
    return (f'<div class="oai-s-newsprint" style="position:relative;overflow:hidden;width:{W}px;height:{H}px;padding:48px">'
            f'{crop}<div style="position:relative">{wordmark(18, label="Oath & Action")}'
            f'<p style="margin-top:64px;font:700 10pt/1.4 var(--oa-font-family-reading);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:{ink2("newsprint")}">Report · Local budgets</p>'
            f'<p style="margin-top:12px;font:800 34pt/1.02 var(--oa-font-family-display);letter-spacing:var(--oa-type-section-letter-spacing);max-width:10ch;text-wrap:balance">How a county budget gets written</p>'
            f'<p style="margin-top:16px;font:400 12pt/1.45 var(--oa-font-family-reading);max-width:24ch">Who drafts it, who can change it and when the public can speak.</p></div></div>')


@spec
def s_04_8_correct():
    body = _cover(True)
    alt = ("A half-letter report cover at true size, 5.5 by 8.5 inches, on Newsprint: the wordmark and the title How a county "
           "budget gets written at top left, and a very large Charcoal ampersand B running off the bottom-right corner. Illustrative.")
    return rec("s-04-8-correct", "04.8", 528, alt, body, illustrative=True, check_exempt=["scale"],
               notes="A print piece set in points (D2-205): kicker 10 pt, title 34 pt, deck 12 pt, so check_exempt scale. "
                     "B display master at 440 px tall in the surface's ink, 142 px past the right edge and 30 px past the bottom: 30.5 percent of its ink "
                     "outside. The trim falls at 258 px of 400: it cuts a 116 px chord through the upper bowl (whose edge is at 273), leaves 14 px of ink beyond the lower counter's tip (244), and clears the beak (277 to 366), which sits wholly outside. The bottom trim falls 24 px below the lower counter, so no hairline of ink runs along the edge. What stays "
                     "inside is one piece at every offset within 4 px, and each stroke at the trim runs over 90 px across (measured on a 1x render). The stage is the cover, so the keyline is the trim; the Illustrative label sits in the caption (CD review B2).")


@spec
def s_04_8_failure():
    body = _cover(False)
    alt = "Failure case: the same cover with the large ampersand moved up behind the title, so the title's letters cross its strokes. Illustrative."
    return rec("s-04-8-failure", "04.8", 528, alt, body, illustrative=True, check_exempt=["scale"],
               notes="A print piece set in points (D2-205), so check_exempt scale.")
