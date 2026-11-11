"""Chapter 12 Graphic devices and patterns: the identity designer's Rules 12.1 to 12.4 (stage B round 2, November 10,
2026), under work/handoffs/phase-2/20261110_Stage-B-Round-2-Brief.md, "Chapter 12", identity designer.

  12.1  dividers: the Stone hairline, with the hinge divider indexed from Rule 04.4, and an index of every device
  12.2  watermarks: ampersand B from its display master at the token opacities 0.08 and 0.10, in an open margin
  12.3  L8, the monogram, as a small signature: opaque, for small headers and video corners
  12.4  one restrained pattern built from the hinge devices, the hinge arcs, after icon study 07's ring rhythm (round 3
        dropped the hinge rules, CA-S11)

The chapter file is shared (D2-829, D2-830): the systems designer's stage_b_ch12_systems_build.py writes Rules 12.5 to
12.9. write_chapter() replaces only Rules 12.1 to 12.4 and this maker's extras, keeps every other rule, extra and the
opener, and adds one sentence to the intro for Rules 12.1 to 12.4. Specimens are named by device (D2-829):
s-12-divider-*, s-12-index, s-12-watermark-*, s-12-signature-*, s-12-pattern-*, in manifest-identity.json.

Run through the identity build: python3 -I work/build/scripts/phase-2/promotion_identity.py specimens
"""
import base64
import io
import json
import re

from stage_a_identity_lib import (E, ROOT, ID_DIR, AMP, L8, fragment, svg_file, mark, illus, head_label, dnp, ty, tv, ink, ink2,
                                  hair, pal, raster_png, steps, CHAP_DIR)
import stage_a_identity_lib as LIB
from stage_a_identity_s03 import rec as _rec
from stage_a_identity_s04 import divider

S = []
CH = "12"
MINE = ("12.1", "12.2", "12.3", "12.4")
DEVICES = ("divider", "index", "watermark", "signature", "pattern")
PREFIXES = tuple(f"s-12-{d}" for d in DEVICES)
W = 600                                                    # every plate fits a chapter column (D2-424)
PHONE_W = 360                                              # a plate that is one phone-size piece fits a 360 px screen (CA-S5)
# Where the page's right edge cuts B, in units of the display master (93.29 wide): through the upper loop, the crossing
# stroke and the lower bowl's counter, left of the arm (64.71 to 84.14) and of the loop's outer edge (63.86), so no piece
# of B stands alone at the edge and no curve grazes it (round 3, CD-S10, CA-S10; Rule 04.8's crop rule)
WM_CUT, WM_TOP, WM_H, PAGE_H = 50.0, 20, 320, 360
B_W, B_H = 93.29, 102.69


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", CH)
    return _rec(*a, **k)


def hl(surface):
    return tv(f"color-border-hairline-on-{surface}")


# ============================================================================================ 12.1 dividers
def section(head, text, surface="newsprint"):
    return (f'<p style="{ty("h4")};margin:0 0 8px;color:{ink(surface)}">{E(head)}</p>'
            f'<p style="{ty("body")};margin:0;color:{ink(surface)};max-width:34em">{E(text)}</p>')


def rule_line(surface="newsprint", dashed=False):
    style = f"border-top:1px {'dashed' if dashed else 'solid'} {hl(surface)};margin:24px 0"
    return f'<div aria-hidden="true" style="{style}"></div>'


ARTICLE = [("Who writes the budget", "The town manager drafts it each winter from the requests every department sends in."),
           ("Who changes it", "The finance committee holds two public hearings, then sends its changes to the town council."),
           ("What you can do", "Speak at the second hearing, or send written comments to the committee clerk by March 3.")]


def article(dashed=False):
    a, b, c = ARTICLE
    return (f'<div class="oai-s-newsprint" style="padding:24px;border:1px solid {hair("newsprint")}">{head_label()}'
            f'{section(*a)}{rule_line(dashed=dashed)}{section(*b)}{divider() if not dashed else rule_line(dashed=True)}{section(*c)}</div>')


@spec
def s_12_divider_correct():
    sw = "".join(f'<div class="oai-cell" style="flex:1 1 120px;align-items:stretch"><div class="oai-s-{s}" style="height:56px;display:flex;align-items:center;'
                 f'padding:0 12px"><div aria-hidden="true" style="flex:1;border-top:1px solid {hl(s)}"></div></div>'
                 f'<span class="oai-tag">{E(n)}</span></div>'
                 for s, n in (("newsprint", "Newsprint, Stone"), ("white", "White, Stone"), ("charcoal", "Charcoal, Stone"),
                              ("prussian", "Prussian, White")))
    body = f'<div class="oai-pad">{article()}<div class="oai-row" style="gap:12px;margin-top:20px;flex-wrap:nowrap">{sw}</div></div>'
    alt = ("An Illustrative article on a town budget at true size, in three sections: Who writes the budget, then a 1 pixel "
           "Stone hairline, Who changes it, then the hinge divider, a line broken by a small Charcoal ampersand, and What you "
           "can do. Below, the hairline on Newsprint, White and Charcoal in Stone, and on Prussian in White.")
    return rec("s-12-divider-correct", "12.1", W, alt, body, illustrative=True,
               notes="The hairline is a 1 px top border in oa.color.border.hairline on each surface (Stone; White on Prussian), "
                     "with 24 px (oa.space.300) above and below. The hinge divider is chapter 04's, drawn by "
                     "stage_a_identity_s04.divider (Rule 04.4, DR-96). The article is invented. From our fifth edition's "
                     "Stone hairline dividers and its standard Hairlines, not boxes.")


@spec
def s_12_divider_failure():
    body = f'<div class="oai-pad">{dnp()}<div style="margin-top:12px">{article(dashed=True)}</div></div>'
    alt = ("Failure case: do not publish. The same Illustrative article with dashed lines between its sections, and no "
           "hinge divider before What you can do.")
    return rec("s-12-divider-failure", "12.1", W, alt, body, illustrative=True,
               notes="D1-21: no brand graphic uses a dotted or dashed line, since the atlas's key gives them to evidence grades. "
                     "Failure band per D2-308.")


INDEX = [("Stone hairline", "Separates sections and modules", "12.1"),
         ("Hinge divider", "Marks the turn from how a decision is made to what a reader can do", "04.4"),
         ("Hinge diagram", "Shows our idea whole: understand, then impact", "04.5"),
         ("End mark", "Closes an article", "04.6"),
         ("Large crop of B", "Frames a cover", "04.8"),
         ("Lockmark", "Signs four fixed places", "08.2"),
         ("Watermark", "Signs an open margin", "12.2"),
         ("L8, the monogram", "Signs a small header or a video corner", "12.3"),
         ("Hinge arcs", "Gives an open area texture", "12.4"),
         ("Intervention marker", "Shows where a reform acts", "12.5"),
         ("Chart key", "Names what a chart's labels cannot carry", "12.6"),
         ("Locator", "Shows where a view sits in the whole", "12.7"),
         ("Layer diagram", "Stacks the atlas's three layers", "12.8"),
         ("Owner frame", "Names who owns each step of a process", "12.9")]


@spec
def s_12_index():
    rows = "".join(f'<tr><th scope="row">{E(d)}</th><td data-k="Job">{E(j)}</td><td data-k="Rule" style="white-space:nowrap">'
                   f'<a href="#rule-{r.replace(".", "-")}">Rule {r}</a></td></tr>' for d, j, r in INDEX)
    table = ('<table class="stack"><thead><tr><th scope="col">Device</th><th scope="col">Its job</th><th scope="col">Rule</th>'
             f'</tr></thead><tbody>{rows}</tbody></table>')
    body = f'<div class="oai-panel oai-s-newsprint">{table}</div>'
    alt = "Every graphic device in this guide, the job it does and the rule that sets it."
    return rec("s-12-index", "12.1", None, alt, body, readable=True,
               notes="The device index the architecture map asks for (the hinge divider is listed here and set in Rule 04.4). "
                     "readable: the table and its links reach assistive technology. Rules 12.5 to 12.9 are the systems "
                     "designer's (D2-829).")


# ============================================================================================ 12.2 watermarks
def watermark_b(height, surface):
    """Ampersand B from its display master as a watermark: Charcoal at the light token's opacity on Newsprint and White,
    Newsprint at the dark token's on Charcoal and Prussian. Decorative."""
    light = surface in ("newsprint", "white")
    color = pal("charcoal") if light else pal("newsprint")
    op = tv("opacity-watermark-on-light" if light else "opacity-watermark-on-dark")
    return svg_file(ID_DIR / AMP["display"], h=height, decorative=True, style=f"color:{color};opacity:{op}")


def _page(surface, eyebrow, title, text, wm, behind=False, h=PAGE_H):
    """A page at true size: the text column at left, the watermark in the open margin at right and running off the
    page's edge, or behind the text when behind=True (the failure)."""
    # behind the text for the failure, at the same height, so its only fault is where it stands (its foot no longer
    # grazes the page's bottom edge, round 3)
    pos = f"left:-24px;top:{WM_TOP}px" if behind else f"right:{-(B_W - WM_CUT) * WM_H / B_H:.1f}px;top:{WM_TOP}px"
    return (f'<div class="oai-s-{surface}" style="position:relative;width:552px;height:{h}px;overflow:hidden;'
            f'border:1px solid {hair(surface)}">'
            f'<div aria-hidden="true" style="position:absolute;{pos};line-height:0">{wm}</div>'
            f'<div style="position:relative;padding:40px;width:{"440px" if behind else "330px"}">'
            f'<p style="{ty("label")};color:{ink2(surface)};margin:0 0 12px">{E(eyebrow)}</p>'
            f'<p style="{ty("h3")};color:{ink(surface)};margin:0 0 12px">{E(title)}</p>'
            f'<p style="{ty("body")};color:{ink(surface)};margin:0">{E(text)}</p></div></div>')


BRIEF = ("Research brief", "The decision behind the service.",
         "Every five years the town puts its trash pickup out to bid. This brief traces who wrote the last contract, who "
         "voted on it and what the record shows.")
OPENER = ("Track", "Follow the decision and keep its record within reach.",
          "Every vote, hearing and filing on the bills we follow, dated and linked to its source.")


@spec
def s_12_watermark_correct():
    body = (f'<div class="oai-pad">{head_label()}<div class="oai-stack" style="gap:16px">'
            f'<div class="oai-cell">{_page("newsprint", *BRIEF, watermark_b(320, "newsprint"))}'
            f'<span class="oai-tag">A report page on Newsprint: Charcoal at 8 percent</span></div>'
            f'<div class="oai-cell">{_page("charcoal", *OPENER, watermark_b(320, "charcoal"))}'
            f'<span class="oai-tag">A section opener on Charcoal: Newsprint at 10 percent</span></div></div></div>')
    alt = ("Two Illustrative pages at true size. A report page on Newsprint headed Research brief, The decision behind the "
           "service., with a paragraph at left, and a very large ampersand B in Charcoal at 8 percent in the open right "
           "margin, running off the page's right edge, which cuts through its loop and its crossing stroke. A section opener "
           "on Charcoal headed Track, Follow the decision and keep its record within reach., with the same B in Newsprint at "
           "10 percent in its right margin. Neither watermark sits behind any words.")
    return rec("s-12-watermark-correct", "12.2", W, alt, body, illustrative=True,
               notes="B's display master (ampersand/20261028_Amp-B-Display-Master.svg) at 320 px tall, in Charcoal with "
                     "opacity oa.opacity.watermarkOnLight (0.08, 1.17 to 1) and in Newsprint with oa.opacity.watermarkOnDark "
                     "(0.10, 1.24 to 1), the two opacities our fifth edition's quiet signatures used, now tokens (Rule 05.6). "
                     "B's top 20 px under the page's top, and the page's right edge cutting B at 50 of its 93.29 units: through "
                     "the loop, the crossing stroke and the lower counter, left of the arm, so no piece of B stands alone at the "
                     "edge (round 3, CD-S10, CA-S10). The report page's heading is our fifth edition's watermark mockup's "
                     "(architecture map, V5 03); the opener's line is Track's job line, as chapter 01 and Rule 09.4 print it; "
                     "the paragraphs are invented.")


@spec
def s_12_watermark_failure():
    body = (f'<div class="oai-pad">{dnp()}<div style="margin-top:12px">{head_label()}'
            f'{_page("newsprint", *BRIEF, watermark_b(320, "newsprint"), behind=True)}</div></div>')
    alt = ("Failure case: do not publish. The Illustrative report page with the large Charcoal B at 8 percent moved behind "
           "its heading and paragraph, so its edges cross the letters.")
    return rec("s-12-watermark-failure", "12.2", W, alt, body, illustrative=True,
               notes="Our fifth edition's rule: a watermark belongs in an open margin, never behind text. Failure band per D2-308.")


# ============================================================================================ 12.3 the compact signature
def running_head(l8):
    return (f'<div class="oai-s-white" style="width:552px;display:flex;align-items:center;gap:16px;padding:16px 24px;'
            f'border:1px solid {hair("white")};border-bottom:1px solid {hl("white")}">{l8}'
            f'<span style="{ty("caption")};color:{ink2("white")}">Report 3 · How state committees record their votes</span>'
            f'<span class="oai-num" style="margin-left:auto;{ty("caption")};color:{ink2("white")}">7</span></div>')


def video_frame(sig):
    """A still from an explainer video, 480 by 270 px, on Charcoal: a bill's six steps with the step in words, and the
    signature in the top right corner, 24 px in from each edge."""
    trk = steps(["done", "done", "done", "now", "notyet", "notyet"], 328, 26, surface="charcoal", flush=True, tag=True)
    return (f'<div class="oai-s-charcoal" style="position:relative;width:480px;height:270px;display:flex;flex-direction:column;'
            f'justify-content:center;align-items:center;gap:16px">{trk}'
            f'<p style="{ty("body", size=17)};color:{ink("charcoal")};margin:0"><b>Step 4 of 6: First chamber.</b></p>'
            f'<span style="position:absolute;right:24px;top:24px;line-height:0">{sig}</span></div>')


@spec
def s_12_signature_correct():
    l8w = mark(L8["today"], w=48, surface="white", label="Oath & Action, L8 monogram")
    l8c = mark(L8["today"], w=48, surface="charcoal", decorative=True)
    body = (f'<div class="oai-pad">{head_label()}<div class="oai-stack" style="gap:20px">'
            f'<div class="oai-cell">{running_head(l8w)}<span class="oai-tag">A report’s running head on White: L8 at 48 px wide, opaque</span></div>'
            f'<div class="oai-cell">{video_frame(l8c)}<span class="oai-tag">A frame from an explainer video: L8 at 48 px wide in the top right corner</span></div>'
            '</div></div>')
    alt = ("Two Illustrative pieces at true size. A report's running head on White: the L8 monogram, O & A with a red "
           "ampersand, 48 pixels wide and opaque, then Report 3, How state committees record their votes, and the page "
           "number 7. Then a still from an explainer video, 480 by 270 pixels on Charcoal: a bill's six numbered steps with "
           "the fourth current, the words Step 4 of 6: First chamber, and L8 in Newsprint with its red ampersand, 48 pixels "
           "wide, in the top right corner.")
    return rec("s-12-signature-correct", "12.3", W, alt, body, illustrative=True,
               notes="L8 (lockups/20261028_L8-Monogram-Master.svg) at its 48 px minimum (Rule 03.4), in Rule 03.5's colors: "
                     "Charcoal with signature red on White, Newsprint with signature red on Charcoal. Our fifth edition's quiet "
                     "signatures sent small headers and video corners to an opaque compact signature; L8 is the one monogram "
                     "(D2-193). The steps are chapter 11's at 360 px (S.99002's states), on Charcoal. The report title is "
                     "chapter 01's invented Report example.")


@spec
def s_12_signature_failure():
    faint = svg_file(ID_DIR / L8["today"], w=48, decorative=True,
                     style=f"color:{pal('newsprint')};--amp:{pal('newsprint')};opacity:{tv('opacity-watermark-on-dark')}")
    body = f'<div class="oai-pad">{dnp()}<div style="margin-top:12px">{head_label()}{video_frame(faint)}</div></div>'
    alt = ("Failure case: do not publish. The same Illustrative video still with L8 in the corner at 10 percent opacity, "
           "as a watermark would be, so the mark almost vanishes.")
    return rec("s-12-signature-failure", "12.3", W, alt, body, illustrative=True,
               notes="A watermark shrunk to a corner: L8 at 48 px in Newsprint at oa.opacity.watermarkOnDark. Failure band per D2-308.")


# ============================================================================================ 12.4 patterns
STEP = 16          # the arcs' step in px: half the hinge diagram's ring radius (110 units), whose arcs sit at 165, a 2 to 3 ratio
ARCS_H = 220       # the open area the arcs fill on a cover, from its foot: it starts at least 24 px under the paragraph


def hinge_arcs(w, h, surface, corner="br", fill=False):
    """Concentric arcs from a corner, at radii 2, 3, 4 and more times STEP: the hinge diagram's ring and arcs (110 and 165
    units, a 2 to 3 ratio) carried on in equal steps, 1 px, in the surface's hairline color. The arcs end inside a
    quarter circle as wide as the area's shorter side, so none is cut off flat; fill=True runs them to the far corner
    (a swatch, or the failure). Clipped to its box, whatever the page's CSS says about overflow."""
    cx, cy = (w, h) if corner == "br" else (w, 0)
    rmax = (w * w + h * h) ** 0.5 if fill else min(w, h) - 1
    circles = "".join(f'<circle cx="{cx}" cy="{cy}" r="{k * STEP}"/>' for k in range(2, int(rmax / STEP) + (2 if fill else 1)))
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false" class="oai-svg" '
            f'style="display:block;overflow:hidden" fill="none" stroke="{hl(surface)}" stroke-width="1">{circles}</svg>')


def coverage():
    """Ink coverage of the hinge arcs on a 1x Chromium render, as Phase 1 measured its swatches: the mean of each pixel's
    distance from the ground over the distance from ground to Stone, on Newsprint."""
    from PIL import Image
    swatch = hinge_arcs(240, 240, "newsprint", fill=True)
    uri = raster_png(f'<div style="line-height:0">{swatch}</div>', 240, 240, "p12-hinge_arcs", scale=1)
    im = Image.open(io.BytesIO(base64.b64decode(uri.split(",", 1)[1]))).convert("RGB")
    g, s = (0xDC, 0xD9, 0xD2), (0x5D, 0x63, 0x6D)
    span = max(abs(a - b) for a, b in zip(g, s))
    px = list(im.getdata())
    return {"hinge_arcs": round(sum(min(1, max(abs(a - b) for a, b in zip(p, g)) / span) for p in px) / len(px), 3)}


COVER = None


def _coverage():
    global COVER
    if COVER is None:
        COVER = coverage()
    return COVER


def cover(behind=False):
    """A report's first screen at true size, 360 by 466 px, on Newsprint, the whole plate (round 3, CA-S11): the
    Illustrative label at its head, the title at top left and the hinge arcs in the open lower right. behind=True runs
    the arcs under the cover's title and paragraph (the failure)."""
    pat = hinge_arcs(PHONE_W, 466, "newsprint", fill=True) if behind else hinge_arcs(PHONE_W, ARCS_H, "newsprint")
    pos = "left:0;top:0" if behind else "left:0;bottom:0"
    return (f'<div class="oai-s-newsprint" style="position:relative;width:{PHONE_W}px;height:466px;overflow:hidden">'
            f'<div aria-hidden="true" style="position:absolute;{pos};line-height:0">{pat}</div>'
            f'<div style="position:relative;padding:32px 32px 0">{head_label()}'
            f'<p style="{ty("label")};color:{ink2("newsprint")};margin:0 0 10px">Report 3</p>'
            f'<p style="{ty("h3")};color:{ink("newsprint")};margin:0 0 12px">How state committees record their votes</p>'
            f'<p class="p12-par" style="{ty("body")};color:{ink("newsprint")};margin:0">We read every committee rule in the fifty '
            f'states and checked which ones post a vote within two days.</p></div></div>')


@spec
def s_12_pattern_correct():
    c = _coverage()
    alt = ("An Illustrative report cover at true size on Newsprint, 360 by 466 pixels, with the kicker Report 3, the title How "
           "state committees record their votes and a short paragraph at the top. Stone arcs 1 pixel wide spread from the "
           "bottom right corner across the open lower part of the cover, and stop well short of the words.")
    return rec("s-12-pattern-correct", "12.4", PHONE_W, alt, cover(), illustrative=True,
               notes=f"Built from the hinge devices, after icon study 07's ring rhythm. Hinge arcs: circles from the corner at "
                     f"radii 2, 3, 4 and more times {STEP} px, continuing the hinge diagram's ring and arcs (radii 110 and 165 "
                     f"units, 2 to 3), ending inside a quarter circle {ARCS_H - 1} px wide, 1 px in oa.color.border.hairline "
                     f"(Stone). Ink coverage measured on a 240 px swatch rendered at 1x in Chromium, as Phase 1 measured its "
                     f"patterns: {c['hinge_arcs'] * 100:.1f} percent, under the 12 percent ceiling (D1-18). Round 3 (CA-S11): "
                     f"the hinge rules leave the rule, since sixteen even lines read as lines to write on, and the plate is the "
                     f"cover alone at 360 px, so no part of the frame stands empty and a phone shows it whole. The cover is a "
                     f"report's first screen, with type at the phone floor (D2-254).")


@spec
def s_12_pattern_failure():
    body = f'{dnp()}{cover(behind=True)}'
    alt = ("Failure case: do not publish. The same Illustrative cover with the arcs spread over the whole of it, so the "
           "fine lines run behind the title and the paragraph.")
    return rec("s-12-pattern-failure", "12.4", PHONE_W, alt, body, illustrative=True,
               notes="The arcs under body text, the failure the brief names. The band runs the plate's width, as chapter 11's "
                     "360 px plates set it, and the Illustrative label opens the cover under it (CD-S11). Failure band per D2-308.")


# ============================================================================================ 12.4 rewritten, for board C
# Stage C round 1 (November 11, 2026): the creative director's review of Rule 12.4 (20261111_CD-Review-Of-Rule-12-4.md)
# recommends retiring the hinge arcs and rewriting the rule for open areas: leave them plain, or sign them with the large
# crop of B (Rule 04.8) or a watermark (Rule 12.2). Dustin decides on board C. This is the rewrite as a variant beside
# the current rule: its words (REWRITE_12_4, a draft for the editor) and its two plates (rewrite_plates), which
# stage_c_identity_round1.py sets beside today's rule on a comparison page. Nothing here is a specimen: S does not hold
# these functions, so chapter 12 and its plates stay as they are until Dustin chooses.
#
# The crop on the Report 3 cover keeps Rule 04.8's proportions as s-04-8-correct sets them: B's display master in the
# surface's ink, its right edge 142/400 of its width past the cover's right edge and its foot 30/440 of its height past
# the cover's foot. Its height on this cover, CROP_B_H, is the largest that keeps Rule 04.8's measures, chosen on a
# render by stage_c_identity_round1.py (20261111_Stage-C-Round-1-Identity-Figures.json, key rule_12_4).
CROP_B_H = 236
CROP_RIGHT, CROP_FOOT = 142 / 400, 30 / 440          # s-04-8-correct: 142 of B's 400 px width, 30 of its 440 px height


def crop_b(b_h=None):
    """The large crop of B for the 360 px cover, at Rule 04.8's proportions, in the surface's ink, behind the words."""
    b_h = b_h or CROP_B_H
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', (ID_DIR / AMP["display"]).read_text()).group(1).split()]
    b_w = b_h * vb[2] / vb[3]
    return (f'<span aria-hidden="true" style="position:absolute;right:{-CROP_RIGHT * b_w:.2f}px;bottom:{-CROP_FOOT * b_h:.2f}px;'
            f'line-height:0">{mark(AMP["display"], h=b_h, mode="ink", decorative=True)}</span>')


def cover_signed(b_h=None):
    """The same Report 3 cover as cover(), signed with the large crop of B in place of the arcs."""
    base = cover()
    arcs = re.search(r'<div aria-hidden="true" style="position:absolute;left:0;bottom:0;line-height:0">.*?</svg></div>', base, flags=re.S)
    assert arcs, "the cover is not the one this variant was written for"
    return base.replace(arcs.group(0), crop_b(b_h), 1)


def rewrite_plates(b_h=None):
    """The rewrite's correct plate (the cover signed with the crop of B) and its failure plate (today's cover with the
    arcs, under the failure band), each Illustrative, as the creative director's instruction for board C sets them."""
    return cover_signed(b_h), f'{dnp()}{cover()}'


REWRITE_12_4 = {
    "id": "12.4",
    "title": "Leave an open area plain, or sign it with the large crop of B or a watermark.",
    "rule": ("We use no repeating pattern. A cover or a section opener may carry the large crop of B (Rule 04.8), and a "
             "report page or a section opener may carry a watermark in its open margin (Rule 12.2). A social card, and any "
             "view whose ampersand moment is a hinge headline, keeps its open area plain."),
    "why": ("Every shape we own already has a rule that a repeat would break: B appears once in a view (Rule 04.2), the "
            "lockmark stays whole (Rule 08.3), and a row of nodes reads as chapter 11's tracker. A pattern that avoids them "
            "belongs to no one, so a cover that carries one reads as anyone's report. The crop of B and the watermark sign "
            "an open area with the mark a reader already knows as ours."),
    "basis": "Design judgment, approved on board C",
    "correct": ("The Report 3 cover at true size, signed with the large crop of B off its bottom-right corner, clear of the "
                "words."),
    "failure": ("Nothing on this cover says Oath & Action, and the arcs take the corner the crop of B would sign."),
    "specs": [("Plain", "The first choice for an open area"),
              ("Crop of B", "A cover or a section opener, bottom right, at Rule 04.8's measures"),
              ("Watermark", "A report page or a section opener, in the open margin, at Rule 12.2's measures"),
              ("Kept plain", "A social card, and any view whose ampersand moment is a hinge headline (Rule 04.2)"),
              ("Never", "A repeating pattern of arcs, lines, dots, nodes or ampersands")],
    "builders": ("Leave the open area plain first. Sign it with the crop of B only on a cover or a section opener that holds "
                 "no hinge headline, and check Rule 04.8's measures on the cover at its true size."),
    "if_chosen": ["Remove the \"Hinge arcs\" row from s-12-index",
                  "Change the chapter intro's \"a pattern drawn from the hinge\" to \"the rule for open areas\"",
                  "Drop \"or a pattern\" from Rule 12.2's Never row",
                  "Remove hinge_arcs and its coverage figure from this generator, and set the rewrite's plates as "
                  "s-12-pattern-correct and s-12-pattern-failure"],
}


# ============================================================================================ the chapter's rules
A = "work/build/assets/identity/"
APPROVED = "Design judgment, approved by our founder and editor in November 2026"


DEVICE_OF = {"12.1": "divider", "12.2": "watermark", "12.3": "signature", "12.4": "pattern"}


def rules():
    """Rules 12.1 to 12.4, their specimens named by device (D2-829)."""
    out = _rules()
    for r in out:
        for k in ("correct", "failure", "corrective"):
            if r.get(k):
                r[k]["specimen"] = f"s-12-{DEVICE_OF[r['id']]}-{k}"
    return out


def _rules():
    from stage_a_identity_chapters import R, S as SP_, DJ
    c = _coverage()
    return [
        R("12.1", "Divide sections with a Stone hairline.",
          "Between the sections and modules of a page, draw a 1 px hairline in the surface's hairline color: Stone on "
          "Newsprint, White and Charcoal, and White on Prussian. Run it the width of the column it divides, with 24 px above "
          "and below. Where an article turns from how a decision is made to what a reader can do, the hinge divider takes the "
          "hairline's place (Rule 04.4). Draw every divider solid.",
          "A hairline separates two sections without weight, so the words carry the structure and the page stays calm. In "
          "our atlas a dashed line marks a connection graded plausible, so a dashed divider would read as a claim about the "
          "evidence. "
          "A hairline carries no meaning, so it needs no contrast ratio (Rule 05.5).",
          DJ + ", carried from our fifth edition's Stone hairlines",
          "An article on a town budget at true size: a Stone hairline between its first two sections, the hinge divider "
          "before What you can do, and below, the hairline on each of the four surfaces.",
          "The same article divided by dashed lines. The breaks now read as the atlas's mark for a plausible connection, and "
          "the turn to the reader's step loses its divider.",
          tokens=["oa.color.border.hairline.onNewsprint", "oa.color.border.hairline.onPrussian", "oa.border.width.hairline", "oa.space.300"],
          specs=[SP_("Line", "1 px, solid", "oa.border.width.hairline"),
                 SP_("Color", "Stone on Newsprint, White and Charcoal; White on Prussian", "oa.color.border.hairline.onNewsprint"),
                 SP_("Length", "The width of the column it divides"),
                 SP_("Space", "24 px above and below", "oa.space.300"),
                 SP_("The turn to a reader's step", "The hinge divider (Rule 04.4)"),
                 SP_("Never", "Dashed, dotted, doubled, red or shadowed")],
          related=["04", "05", "07"],
          builders="Draw the hairline as a 1 px top border on the section that follows, in the surface's hairline token, so "
                   "it follows the column's width with no image."),
        R("12.2", "Set a watermark in an open margin, at its token opacity.",
          "A watermark is ampersand B, drawn large from its display master and faint: Charcoal at 8 percent on Newsprint and "
          "White, and Newsprint at 10 percent on Charcoal and Prussian. It sits in an open margin of a report page or a dark "
          "section opener, and it may run off the page's edge. It never sits behind words, a figure or a control. It counts "
          "as the view's one ampersand moment (Rule 04.2), so a page with a hinge headline takes no watermark.",
          "At 8 and 10 percent the mark measures 1.17 and 1.24 to 1 against its page, too faint to carry meaning, so it "
          "signs the page and asks nothing of the reader. Kept to an open margin, it never lowers the contrast of anything a "
          "reader needs. These two opacities are the only ones a page may use (Rule 05.6).",
          DJ + ", carried from our fifth edition's quiet signatures; the opacities are tokens",
          "A report page on Newsprint and a section opener on Charcoal at true size, each with B in its open right margin, "
          "running off the right edge, which cuts through B's loop and crossing stroke.",
          "The report page with the watermark moved behind its heading and paragraph. Its edges cross the letters, and the "
          "words lose the clean ground they need.",
          tokens=["oa.opacity.watermarkOnLight", "oa.opacity.watermarkOnDark"],
          specs=[SP_("Mark", "Ampersand B, from its display master"),
                 SP_("On Newsprint and White", "Charcoal at 0.08, 1.17 to 1", "oa.opacity.watermarkOnLight"),
                 SP_("On Charcoal and Prussian", "Newsprint at 0.10, 1.24 to 1", "oa.opacity.watermarkOnDark"),
                 SP_("Size", "At least half the page's height; it may run off any edge"),
                 SP_("Crop", "Where an edge cuts B, it cuts through strokes the eye can follow, with no piece of B left alone "
                             "at the edge and no curve grazing it (Rule 04.8)"),
                 SP_("Place", "An open margin of a report page or a section opener"),
                 SP_("Never", "Behind words, a figure or a control; in red; beside a hinge headline, a crop of B or a pattern")],
          files=[A + AMP["display"]],
          related=["04", "05", "24"],
          builders="Set the opacity on the mark from its token, and place the mark in its own layer, outside the text "
                   "column and hidden from assistive technology. Move it until every part of B inside the page joins the "
                   "rest of the letter."),
        R("12.3", "Sign a small header or a video's corner with L8 at full strength.",
          "Where a page or a frame has room only for a small mark, such as a report's running head or the corner of a video, "
          "sign it with L8, the monogram, opaque, from its 48 px minimum, in its colors for the surface (Rule 03.5). In a "
          "video, set it 24 px in from the frame's edges.",
          "A watermark shrunk to a corner falls under what an eye, or a compressed video, can hold, and it stops signing "
          "anything. At full strength and at its minimum, L8 keeps every letter and the ampersand's two counters (Rule 03.4).",
          DJ + ", from our fifth edition's quiet signatures",
          "A report's running head on White with L8 at 48 px wide, and a still from an explainer video on Charcoal with L8 "
          "in its top right corner.",
          "The video still with L8 at a watermark's 10 percent. In the corner of a moving picture the mark all but vanishes.",
          tokens=["oa.color.identity.signature.onWhite", "oa.color.identity.signature.onCharcoal"],
          specs=[SP_("Mark", "L8, the monogram"),
                 SP_("Size", "From 48 px wide (Rule 03.4)"),
                 SP_("Color", "Rule 03.5: Charcoal with its red ampersand on Newsprint and White, Newsprint with it on "
                              "Charcoal, all White on Prussian"),
                 SP_("In a video", "24 px in from the frame's top and side edges"),
                 SP_("Never", "At a watermark's opacity, or as an avatar or a favicon")],
          files=[A + L8["today"], A + "prussian/20261028_L8-Monogram-Master-Prussian-White.svg"],
          related=["03", "23", "24"],
          builders="Export the video's signature as a PNG at twice its size from the L8 master, with its colors written in, "
                   "and keep it in the same corner for the whole video."),
        R("12.4", "Use the hinge arcs only in an open area, away from words.",
          "One pattern, the hinge arcs, may give texture to a cover, an opener or the background of a social card. Its arcs "
          "spread from a corner at the radii of the hinge diagram's ring and arcs, carried on in equal steps, and end inside "
          "a quarter circle, so none is cut off flat. They run 1 px in the surface's hairline color, cover no more than 12 "
          "percent of the area they fill, and stop at least 24 px short of any words, figure or control.",
          "A pattern gives an empty area texture without a picture, and drawn from the hinge it adds no new shape for a "
          "reader to learn. Behind words, even a faint pattern adds edges the eye has to sort from the letters, so it stays "
          f"where nothing is read. The arcs cover {c['hinge_arcs'] * 100:.1f} percent of the area they fill.",
          "Our measurements, October and November 2026, and design judgment, which sets the 12 percent ceiling",
          "A report cover at true size, the title at top left and the hinge arcs spreading from the bottom right corner, "
          "clear of the words.",
          "The same cover with the arcs behind the title and the paragraph. The lines cross the letters and the words lose "
          "their clean ground.",
          tokens=["oa.color.border.hairline.onNewsprint", "oa.border.width.hairline"],
          specs=[SP_("Hinge arcs", f"Circles from a corner at 2, 3, 4 and more steps of {STEP} px, 1 px wide, ending inside a "
                                   "quarter circle as wide as the area's shorter side"),
                 SP_("Color", "The surface's hairline color: Stone on Newsprint, White and Charcoal; never on Prussian",
                     "oa.color.border.hairline.onNewsprint"),
                 SP_("Coverage", "At most 12 percent of the area the arcs fill, measured on a render"),
                 SP_("Clearance", "At least 24 px from any words, figure or control"),
                 SP_("Never", "Behind words; in red; dotted or dashed; as evenly ruled lines, which read as a form to fill in; "
                              "with a watermark or a crop of B in the same view")],
          related=["04", "05", "07"],
          builders="Draw the arcs as an SVG in the hairline token, sized to the open area they fill, and keep it out of the "
                   "layer that holds the words."),
    ]


EXTRAS = [{"after_rule": "12.1", "specimen": "s-12-index", "label": "Every graphic device and its rule",
           "caption": "The devices this guide sets, the job of each and the rule that sets it."}]
INTRO_ADD = ("Rules 12.1 to 12.4 cover the devices that divide and sign a page: hairlines, watermarks, the monogram as "
             "a small signature and a pattern drawn from the hinge.")
# earlier wordings of INTRO_ADD, replaced in place when the shared file still holds one (round 3, ED 4e, CA-S11)
OLD_INTRO_ADDS = ("Rules 12.1 to 12.4 cover the devices that divide and sign a page: hairlines, watermarks, the compact "
                  "signature and two patterns drawn from the hinge.",)
RELATED_ADD = [{"chapter": "04", "reason": "The hinge divider, the hinge diagram and the large crop of B."},
               {"chapter": "03", "reason": "L8, the monogram, and the colors of every mark."}]


def write_chapter():
    """Replace Rules 12.1 to 12.4 and this maker's extras in the shared chapter file; keep the rest (D2-829, D2-830)."""
    from stage_a_identity_chapters import _smarten
    f = CHAP_DIR / "12-graphic-devices.json"
    ch = json.loads(f.read_text()) if f.exists() else {
        "number": "12", "anchor": "graphic-devices", "title": "Graphic devices and patterns", "part": "Symbols and graphics",
        "instruction": "Add dividers, frames, markers and watermarks only where they help someone read.",
        "intro": ["A graphic device is a mark that helps a reader find their way: a divider between sections, a watermark, a "
                  "marker on the place a reform acts, a key, a locator, a frame around a process. Each one has a job, and "
                  "the page leaves it out where that job is already done."],
        "rules": [], "related_chapters": []}
    mine = _smarten({"rules": rules(), "extras": EXTRAS, "intro": [INTRO_ADD], "rel": RELATED_ADD})
    keep = [r for r in ch.get("rules", []) if r.get("id") not in MINE]
    ch["rules"] = sorted(keep + mine["rules"], key=lambda r: [int(x) for x in str(r["id"]).split(".")])
    ch["extras"] = [x for x in ch.get("extras", []) if not str(x.get("specimen", "")).startswith(PREFIXES)] + mine["extras"]
    intro = list(ch.get("intro", []))
    add = mine["intro"][0]
    for old in _smarten(list(OLD_INTRO_ADDS)):
        intro = [para.replace(old, add) for para in intro]
    if add not in " ".join(intro):
        if len(intro) >= 2:
            intro[1] = add + " " + intro[1]
        else:
            intro.append(add)
    ch["intro"] = intro
    rel = [r for r in ch.get("related_chapters", []) if r.get("chapter") not in ("03", "04")]
    ch["related_chapters"] = mine["rel"] + rel
    f.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + "\n")
    return ch


def specimens_used():
    out = []
    for r in rules():
        for k in ("correct", "failure", "corrective"):
            if r.get(k):
                out.append(r[k]["specimen"])
    return out + [x["specimen"] for x in EXTRAS]
