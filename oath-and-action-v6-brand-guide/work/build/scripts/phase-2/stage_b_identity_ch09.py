"""Chapter 09 Pillar icons: the chapter text and its specimens (stage B round 2, November 10, 2026).

Under work/handoffs/phase-2/20261110_Stage-B-Round-2-Brief.md, "Chapter 09, Pillar icons". The identity designer owns
the drawings and the specimens; the editor owns every word and copy edits them.

Every pillar icon on a page is drawn from the guide's sprite with <use>, never inlined (D2-590), with data-icon and
data-icon-family="pillar" on its <svg> (D2-517), hidden from assistive technology beside its visible word (R9):
  48 px and up   the Civic Line master, oa-sym-cl-0xx, in the surface's icon ink; its red only as the current pillar's
                 second sign or on a standalone icon (DR-66, DR-111, R11)
  24 px          the pixel fit under 2x and the master from 2x, two <use> in one <svg> (DR-179, D2-783)
  16 px          the 16 px pixel fit on every screen (D2-634)
Under 48 px every pillar icon is one color (R10, D2-497). Words and arrows are spaced from each icon's ink, never its box
(D2-439): the masters' ink from guide_editor_common.INK, the fits' from their pixel maps in the pillar icons manifest.

Run through the identity build: python3 -I work/build/scripts/phase-2/stage_a_identity_build.py
(or promotion_identity.py specimens, which skips the letterhead print).
"""
import json

from stage_a_identity_lib import (E, ROOT, ID_DIR, fragment, svg_file, illus, head_label, dnp, ty, tv, ink, ink2, hair, raster_png,
                                  INLINE_ALL)
from stage_a_identity_s03 import rec as _rec
import stage_a_identity_lib as LIB

S = []
CH = "09"
PILLARS = [("CL-019", "Explain"), ("CL-020", "Track"), ("CL-021", "Connect"), ("CL-022", "Act")]
JOBS = {"Explain": "Make the rules and their effects understandable.",
        "Track": "Follow the decision and keep its record within reach.",
        "Connect": "Help people reach the office that decides and the evidence it decides on.",
        "Act": "Give the reader a useful next step."}          # chapter 01's job lines, word for word
PI_DIR = ROOT / "work/build/assets/pillar-icons"
CL6 = ROOT / "work/build/assets/civic-line-v6/black"
TILE_DIR = ROOT / "work/build/assets/civic-line/tiles/rounded-charcoal/svg"
MANIFEST = json.loads((PI_DIR / "20261110_Pillar-Icons-Manifest.json").read_text())

# Each master's ink in its 128-unit field (left, top, right, bottom), measured in Chromium with half the stroke added
# (guide_editor_common.INK, November 7, 2026), so chapter 01's row and this chapter's space alike.
try:
    from guide_editor_common import INK as MASTER_INK
except Exception:                                        # the editor's module is being rewritten; the same figures
    MASTER_INK = {"CL-019": (12.85, 25.28, 115.15, 103.2), "CL-020": (10.34, 24.45, 118.19, 104.36),
                  "CL-021": (10.37, 32.2, 117.94, 96.03), "CL-022": (34.48, 22.92, 93.7, 105.36)}


def _fit_ink():
    """Each fit's inked columns and rows, inclusive, from its pixel map: {(id, size): (x0, y0, x1, y1)}."""
    out = {}
    for ic in MANIFEST["icons"]:
        if ic["edition"] != "black":
            continue
        m = ic["map"]
        xs = [x for row in m for x, c in enumerate(row) if c != "."]
        ys = [y for y, row in enumerate(m) if any(c != "." for c in row)]
        out[(ic["id"], ic["size_px"])] = (min(xs), min(ys), max(xs), max(ys))
    return out


FIT_INK = _fit_ink()


def fit_file(cid, size):
    return next(PI_DIR / ic["svg"] for ic in MANIFEST["icons"] if ic["id"] == cid and ic["size_px"] == size and ic["edition"] == "black")


def master_file(cid):
    return next(CL6.glob(f"*-{cid}-*-Black.svg"))


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", CH)
    return _rec(*a, **k)


# ============================================================================================ the glyph and the row
def glyph(cid, size, surface="newsprint", red=False, trim=False, cls="p9-ic", extra=""):
    """One pillar icon from the sprite at a size, in the surface's icon ink. red keeps its accent (48 px and up only,
    never on Prussian). trim pulls the box in to the ink with negative margins (D2-439); at 16 and 24 px the margins
    are whole pixels, so the fit keeps its pixel grid."""
    if red and (size < 48 or surface == "prussian"):
        raise ValueError("a pillar icon keeps its red only from 48 px and never on Prussian (R10, D2-497, Rule 05.3)")
    st = [f"color:{tv(f'component-icon-ink-on-{surface}')}"]
    if red:
        st.append(f"--oa-icon-accent:{tv(f'component-icon-accent-on-{surface}')}")
    if trim:
        if size >= 48:
            x0, _, x1, _ = MASTER_INK[cid]
            st.append(f"margin:0 {-(128 - x1) * size / 128:.2f}px 0 {-x0 * size / 128:.2f}px")
        else:
            x0, _, x1, _ = FIT_INK[(cid, size)]
            st.append(f"margin:0 {-(size - 1 - x1)}px 0 {-x0}px")
    sid = cid.lower()
    if size >= 48:
        vb, uses = "0 0 128 128", f'<use href="#oa-sym-{sid}"/>'
    elif size == 24:
        vb, uses = "0 0 24 24", f'<use class="oa-at-1x" href="#oa-sym-{sid}-24px"/><use class="oa-at-2x" href="#oa-sym-{sid}"/>'
    elif size == 16:
        vb, uses = "0 0 16 16", f'<use href="#oa-sym-{sid}-16px"/>'
    else:
        raise ValueError(f"no pillar icon at {size} px: 16, 24, or 48 and up (Rule 09.3)")
    red_attr = ' data-red="signature"' if red else ""
    return (f'<svg viewBox="{vb}" width="{size}" height="{size}" class="{cls}" aria-hidden="true" focusable="false" '
            f'data-icon="{cid}" data-icon-family="pillar"{red_attr} style="{";".join(st)}"{extra}>{uses}</svg>')


def master_at(cid, size, surface="newsprint"):
    """The master drawn at any size, for a failure case: the misuse Rule 09.3 forbids."""
    return (f'<svg viewBox="0 0 128 128" width="{size}" height="{size}" class="p9-ic" aria-hidden="true" focusable="false" '
            f'data-icon="{cid}" data-icon-family="pillar" style="color:{tv(f"component-icon-ink-on-{surface}")}"><use href="#oa-sym-{cid.lower()}"/></svg>')


def row(size, surface="newsprint", current=None, words=True, red_only=False, stack=False, label=None):
    """The pillar row (Rule 09.1): an ordered list, each icon beside its word, an arrow between each pair drawn by CSS
    and skipped by screen readers. current underlines that word (Rule 09.2) and, from 48 px, keeps its icon's red.
    red_only is the failure case: the current icon red and no underline. stack forces the phone column (D2-376)."""
    lis = []
    for cid, word in PILLARS:
        cur = word == current
        red = cur and size >= 48 and surface != "prussian"
        c = "p9-pi" + (" p9-cur" if cur and not red_only else "")
        a = ' aria-current="true"' if cur and not red_only else ""
        w = f'<span class="p9-w">{E(word)}</span>' if words else ""
        lis.append(f'<li class="{c}"{a}>{glyph(cid, size, surface, red=red, trim=words)}{w}</li>')
    cls = f"p9-row p9-{size}" + (" p9-stack" if stack else "") + ("" if words else " p9-bare")
    lab = label or ("The four pillars, in order" + (f", with {current} as the current pillar" if current and not red_only else ""))
    return f'<ol class="{cls}" aria-label="{E(lab)}">{"".join(lis)}</ol>'


ROW_CSS = (
    ".oai .p9-row{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;row-gap:12px}"
    ".oai .p9-pi{display:flex;align-items:center;gap:12px}"
    ".oai .p9-24 .p9-pi{gap:8px}.oai .p9-16 .p9-pi{gap:6px}"
    ".oai .p9-ic{display:block;flex:none;overflow:visible}"
    f".oai .p9-pi:not(:last-child)::after{{content:\"\\2192\" / \"\";margin:0 14px 0 2px;{ty('body')};color:{ink2('newsprint')}}}"
    f".oai .oai-s-charcoal .p9-pi:not(:last-child)::after{{color:{ink2('charcoal')}}}"
    f".oai .p9-48 .p9-w{{{ty('intro', size=19)};font-weight:700}}"
    "@media (min-width:48em){.oai .p9-48:not(.p9-stack) .p9-w{font-size:22px}}"
    f".oai .p9-24 .p9-w{{{ty('body')}}}"
    f".oai .p9-16 .p9-w{{{ty('body-small')}}}"
    ".oai .p9-cur .p9-w{text-decoration:underline solid 2px;text-underline-offset:5px;text-decoration-skip-ink:none}"
    ".oai .p9-24 .p9-cur .p9-w,.oai .p9-16 .p9-cur .p9-w{font-weight:700}"
    # a stacked column keeps each icon's whole box, so the four words share one left edge
    ".oai .p9-stack{flex-direction:column;align-items:flex-start}.oai .p9-stack .p9-ic{margin:0!important}"
    ".oai .p9-stack .p9-pi:not(:last-child)::after{content:\"\\2193\" / \"\";margin:0 0 0 4px}"
    "@media (max-width:47.99em){.oai .p9-48{flex-direction:column;align-items:flex-start}.oai .p9-48 .p9-ic{margin:0!important}"
    ".oai .p9-48 .p9-pi:not(:last-child)::after{content:\"\\2193\" / \"\";margin:0 0 0 4px}}"
    ".oai .p9-bare{gap:16px}.oai .p9-bare .p9-pi::after{content:none!important}"
    ".oai .p9-box+.p9-box{margin-top:20px}.oai .p9-box .oai-tag{display:block;margin:0 0 10px}"
    ".oai .oai-s-charcoal .oai-tag{color:var(--oa-color-text-secondary-on-charcoal)}"
)


def box(tag, inner):
    return f'<div class="p9-box"><span class="oai-tag">{E(tag)}</span>{inner}</div>'


# ============================================================================================ 09.1
@spec
def s_09_1_correct():
    body = ('<div class="oai-stack" style="gap:12px">'
            f'<div class="oai-panel oai-s-newsprint">{box("On Newsprint, 48 px", row(48))}{box("24 px", row(24))}</div>'
            f'<div class="oai-panel oai-s-charcoal">{box("On Charcoal, 48 px", row(48, "charcoal"))}{box("24 px", row(24, "charcoal"))}</div></div>')
    alt = ("The pillar row at true size, four times. On Newsprint at 48 pixels, then at 24 pixels; on Charcoal at 48 pixels, "
           "then at 24 pixels. Each row reads Explain, Track, Connect, Act, each icon beside its word, joined by arrows, every "
           "icon in one color: Explain, three short rays rising from an open book; Track, a route from a map pin to a magnifier; "
           "Connect, two overlapping rings; Act, a finger pressing a round control.")
    return rec("s-09-1-correct", "09.1", None, alt, body, css=ROW_CSS,
               notes="DR-111, R9, D2-439. Each icon from the sprite with data-icon-family pillar: the master at 48 px, and at 24 px "
                     "the pixel fit under 2x with the master from 2x (DR-179, D2-783). One color, in the surface's icon ink token, "
                     "since no pillar is current. Words in the intro style, bold, 19 px and 22 px from 48em, beside the 48 px icons, "
                     "as chapter 01's row sets them, and in body text beside the 24 px icons. Spaced from each icon's ink. A sheet "
                     "that flows: at 390 px the 48 px rows stack in one column (D2-376).")


@spec
def s_09_1_failure():
    body = (f'<div class="oai-pad">{dnp()}<div class="oai-panel oai-s-newsprint" style="margin-top:12px">'
            f'{row(24, words=False, label="Four pillar icons with no words")}</div></div>')
    alt = ("Failure case: do not publish. The four pillar icons at 24 pixels in a row with no words and no arrows: an open book "
           "with rays, a route to a magnifier, two overlapping rings and a finger pressing a round control.")
    return rec("s-09-1-failure", "09.1", 400, alt, body, css=ROW_CSS,
               notes="R9: under 48 px a pillar icon sits with its word. The row without its words, as a toolbar would set it. "
                     "Failure band per D2-308, since a bare row could pass for our work.")


@spec
def s_09_phone():
    phone = (f'<div class="oai-s-newsprint" style="width:358px;padding:16px;border:1px solid {hair("newsprint")}">'
             f'{box("The 48 px row stacks in one column", row(48, stack=True))}{box("The 24 px row wraps after an arrow", row(24))}</div>')
    body = f'<div class="oai-pad">{phone}</div>'
    alt = ("A phone column 358 pixels wide on Newsprint. The 48 pixel pillar row stands in one column, Explain, Track, Connect "
           "and Act one under another, each icon beside its word and a downward arrow after each word but the last. Under it, the "
           "24 pixel row runs across two lines, breaking after an arrow.")
    return rec("s-09-phone", "09.1", 406, alt, body, css=ROW_CSS,
               notes="D2-376: under 48em the 48 px row stacks in one column with downward arrows, after the creative director's "
                     "Board 6 review found the phone row dropping its arrow. Drawn at a phone's 358 px text column, so the plate "
                     "shows the column at every screen width; the rows in Rule 09.1's sheet take the same form at 390 px.")


# ============================================================================================ 09.2
@spec
def s_09_2_correct():
    body = ('<div class="oai-stack" style="gap:12px">'
            '<div class="oai-panel oai-s-newsprint">'
            f'{box("A section that serves Track, 48 px", row(48, current="Track"))}'
            f'{box("The compact row on a Track page, 24 px", row(24, current="Track"))}</div>'
            f'<div class="oai-panel oai-s-charcoal">{box("On Charcoal, 48 px", row(48, "charcoal", current="Track"))}</div></div>')
    alt = ("The pillar row with Track as the current pillar, three times at true size. On Newsprint at 48 pixels, the word Track "
           "is underlined and Track's icon keeps its red parts, the map pin and the magnifier's handle; the other icons are one "
           "color. At 24 pixels every icon is one color, and the word Track is bold and underlined. On Charcoal at 48 pixels, "
           "the word Track is underlined and its icon keeps its red.")
    return rec("s-09-2-correct", "09.2", None, alt, body, css=ROW_CSS,
               notes="DR-111, DR-66, R10, D2-497, WCAG 2.2 SC 1.4.1. The underline marks the current pillar at every size; from "
                     "48 px the current icon also sets --oa-icon-accent to the surface's icon accent token, signature red "
                     "(Rule 05.3), and carries data-red signature. The 24 px row sets no accent (D2-785). aria-current on the "
                     "current item.")


@spec
def s_09_2_failure():
    body = (f'<div class="oai-pad">{dnp()}<div class="oai-panel oai-s-newsprint" style="margin-top:12px">'
            f'{row(48, current="Track", red_only=True, label="The four pillars, in order")}</div></div>')
    alt = ("Failure case: do not publish. The 48 pixel pillar row on Newsprint with Track's icon in red and no word "
           "underlined, so only the red says which pillar is current.")
    return rec("s-09-2-failure", "09.2", None, alt, body, css=ROW_CSS,
               notes="Color alone marks the current pillar (WCAG 2.2 SC 1.4.1). Failure band per D2-308.")


# ============================================================================================ 09.3
def _raster(svg_html, size, k, name, label):
    """A 1x render of one drawing, enlarged k times in square pixels, as an image."""
    uri = raster_png(f'<div style="padding:4px;background:var(--oa-color-surface-newsprint);line-height:0">{svg_html}</div>',
                     size + 8, size + 8, name, scale=1)
    return (f'<img src="{uri}" alt="" width="{(size + 8) * k}" height="{(size + 8) * k}" '
            f'style="display:block;image-rendering:pixelated" data-label="{E(label)}">')


def _inline(path, size):
    INLINE_ALL[0] = True
    try:
        return svg_file(path, h=size, decorative=True, style="color:var(--oa-color-palette-charcoal)", by_ref=False)
    finally:
        INLINE_ALL[0] = False


LADDER_CSS = (".oai .p9-lad{display:grid;grid-template-columns:96px repeat(4,max-content);gap:16px 28px;align-items:center}"
              ".oai .p9-lad .h{align-self:end}"
              ".oai .p9-lad .h{font:600 13px/1.4 var(--oa-font-family-reading);color:var(--oa-color-text-secondary-on-newsprint)}"
              f".oai .p9-lad .w{{{ty('body')};font-weight:700}}"
              ".oai .p9-enl{display:flex;flex-wrap:wrap;gap:20px 32px;align-items:flex-end;margin-top:28px}"
              ".oai .p9-enl .oai-cell{gap:6px}")


@spec
def s_09_3_correct():
    head = '<span></span>' + "".join(f'<span class="h">{s} px</span>' for s in (16, 24, 48, 96))
    rows = "".join(f'<span class="w">{E(w)}</span>' + "".join(f'<span>{glyph(cid, s)}</span>' for s in (16, 24, 48, 96))
                   for cid, w in PILLARS)
    e16 = _raster(_inline(fit_file("CL-020", 16), 16), 16, 4, "p9-fit16", "Track's 16 px fit at 1x")
    e24 = _raster(_inline(fit_file("CL-020", 24), 24), 24, 4, "p9-fit24", "Track's 24 px fit at 1x")
    enl = (f'<div class="p9-enl"><div class="oai-cell">{e16}<span class="oai-tag">Track’s 16 px fit, enlarged four times</span></div>'
           f'<div class="oai-cell">{e24}<span class="oai-tag">Track’s 24 px fit, enlarged four times</span></div></div>')
    body = f'<div class="oai-panel oai-s-newsprint"><div class="p9-lad">{head}{rows}</div>{enl}</div>'
    alt = ("The four pillar icons at true size at 16, 24, 48 and 96 pixels, one row per pillar with its word first: Explain, "
           "Track, Connect and Act, every icon in one color. At 16 and 24 pixels each is a pixel fit, a 1 pixel line drawn on "
           "whole pixels. Below, Track's 16 and 24 pixel fits as a standard screen draws them, enlarged four times, every "
           "pixel full or empty.")
    return rec("s-09-3-correct", "09.3", 600, alt, body, css=LADDER_CSS,
               notes="DR-133, DR-179, D2-634, D2-808. From the sprite: the 16 px fit, the 24 px pattern (the fit under 2x, the "
                     "master from 2x) and the master at 48 and 96 px, one color. The enlarged views are PNG renders at 1x of the "
                     "fit files in pillar-icons/svg/, scaled four times in square pixels; each plate's word sits in the first "
                     "column, so every icon under 48 px keeps its word beside it (R9). Marks at true size are graphics, so the "
                     "13 px floor applies to the words only.")


@spec
def s_09_3_failure():
    cid = "CL-020"
    em = _raster(_inline(master_file(cid), 16), 16, 4, "p9-master16", "Track's master at 16 px at 1x")
    ef = _raster(_inline(fit_file(cid, 16), 16), 16, 4, "p9-fit16b", "Track's 16 px fit at 1x")

    def col(icon, enlarged, tag):
        return (f'<div class="oai-cell" style="gap:12px;width:140px"><div class="oai-row mid" style="gap:6px">{icon}'
                f'<span style="{ty("body-small")}">Track</span></div>{enlarged}<span class="oai-tag">{E(tag)}</span></div>')
    body = (f'<div class="oai-panel oai-s-newsprint"><div class="oai-row top" style="gap:40px;flex-wrap:nowrap">'
            f'{col(master_at(cid, 16), em, "The master at 16 px, true size and enlarged four times")}'
            f'{col(glyph(cid, 16), ef, "The 16 px fit, true size and enlarged four times")}</div></div>')
    alt = ("Failure case: Track's master scaled to 16 pixels beside the word Track, next to the 16 pixel fit beside the same "
           "word, at true size and enlarged four times. Scaled down, the master's lines fall under a pixel and draw gray, and "
           "the magnifier's lens and the route's turns blur together; the fit draws each line as one full pixel.")
    return rec("s-09-3-failure", "09.3", 400, alt, body, css=LADDER_CSS,
               notes="The master (civic-line-v6/black) at 16 px from the sprite, as a producer would drag it into a menu, beside "
                     "the fit. The enlarged views are PNG renders at 1x, scaled four times in square pixels.")


# ============================================================================================ 09.4
OPEN_CSS = (".oai .p9-open{width:552px;padding:40px;display:flex;flex-direction:column;gap:20px;align-items:flex-start}"
            f".oai .p9-open .p9-lab{{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:{ink('charcoal')};margin:0}}"
            f".oai .p9-open .p9-big{{{ty('title')};color:{ink('charcoal')};margin:0}}"
            f".oai .p9-open .p9-job{{{ty('body')};color:{ink('charcoal')};margin:0;max-width:40ch;text-wrap:pretty}}"
            f".oai .p9-card{{width:552px;margin-top:24px;padding:20px;display:flex;gap:20px;align-items:center;border:1px solid {hair('newsprint')}}}"
            f".oai .p9-card .p9-cw{{{ty('h3')};margin:0 0 4px}}.oai .p9-card .p9-cj{{{ty('body')};margin:0;text-wrap:pretty}}"
            ".oai .p9-card img{display:block;flex:none}")


def tile(cid, word, px):
    f = next(TILE_DIR.glob(f"*-{cid}-{word}-Tile-Rounded-Charcoal-Two-Color.svg"))
    return (f'<span class="oai-red" data-red="signature"><img src="{LIB.rel(f)}" alt="" width="{px}" height="{px}" '
            f'data-icon="{cid}" data-icon-family="pillar"></span>')


@spec
def s_09_4_correct():
    opener = (f'<div class="oai-s-charcoal p9-open">{glyph("CL-020", 128, "charcoal", red=True, trim=True)}'
              f'<p class="p9-lab">Track</p><p class="p9-big">Watch the vote.</p><p class="p9-job">{E(JOBS["Track"])}</p></div>')
    card = (f'<div class="oai-s-newsprint p9-card">{tile("CL-020", "Track", 76)}'
            f'<div><p class="p9-cw">Track</p><p class="p9-cj">{E(JOBS["Track"])}</p></div></div>')
    body = f'<div class="oai-pad">{head_label()}{opener}{card}</div>'
    alt = ("Two pieces at true size, both Illustrative. First, Track's section opener: a Charcoal panel with Track's icon at "
           "128 pixels in Newsprint lines with its red map pin and magnifier handle, then the word Track, the line Watch the "
           "vote. in large heavy type, and Track's job: Follow the decision and keep its record within reach. Second, a card "
           "that leads to Track's section: Track's icon on a rounded Charcoal tile at 76 pixels, in Newsprint and red, beside "
           "the word Track and the same job line.")
    return rec("s-09-4-correct", "09.4", 600, alt, body, css=OPEN_CSS, illustrative=True,
               notes="DR-112, DR-138, R11, R13, D2-42. The opener follows Board 6's: a Charcoal panel, as the guide's part openers are, "
                     "with the master at 128 px from the sprite in the Newsprint ink and its accent token, standalone, so signature "
                     "red. Watch the vote. is the line our fifth edition set on its pillar plate. The tile is the Civic Line "
                     "package's rounded two-color Charcoal tile (civic-line/tiles/rounded-charcoal/svg, the file the set in use "
                     "points to, D2-716) at its 76 px minimum (D2-42), placed as an image. The job line is chapter 01's, word for word.")


@spec
def s_09_4_failure():
    kick = (f'<p class="p9-kick">{glyph("CL-020", 24)}<span class="lb">Report</span><span class="dt" aria-hidden="true">·</span>'
            f'<span class="sx">State legislatures</span></p>')
    card = (f'<div class="oai-s-newsprint" style="width:358px;padding:20px;border:1px solid {hair("newsprint")}">{head_label()}{kick}'
            f'<p style="{ty("h3", size=26)};margin:8px 0 0">How state committees record their votes</p></div>')
    body = f'<div class="oai-pad">{dnp()}<div style="margin-top:12px">{card}</div></div>'
    css = (".oai .p9-kick{display:flex;align-items:center;gap:8px;margin:0;font:var(--oa-type-label);"
           "letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}"
           ".oai .p9-kick .sx{color:var(--oa-color-text-secondary-on-newsprint);text-transform:none;letter-spacing:0;font-weight:400}"
           ".oai .p9-kick .dt{color:var(--oa-color-text-secondary-on-newsprint)}.oai .p9-ic{display:block;flex:none}")
    alt = ("Failure case: do not publish. An Illustrative report card whose kicker opens with Track's pillar icon at 24 pixels, "
           "then the label Report and the topic State legislatures, over the headline How state committees record their votes.")
    return rec("s-09-4-failure", "09.4", 406, alt, body, css=css, illustrative=True,
               notes="DR-112: a kicker keeps its content label and words, and a pillar icon never enters it (Rule 01.21). The "
                     "icon is drawn as a 24 px pillar icon should be, so the only fault is where it stands. The headline is "
                     "chapter 01's invented Report example. Failure band per D2-308.")


# ============================================================================================ the chapter
A = "work/build/assets/"


def _fits():
    return [A + "pillar-icons/" + ic["svg"] for ic in MANIFEST["icons"] if ic["edition"] == "black"]


def chapter():
    from stage_a_identity_chapters import R, S as SP_, DJ
    masters = [LIB.rel(master_file(cid)) for cid, _ in PILLARS]
    tiles = [LIB.rel(next(TILE_DIR.glob(f"*-{cid}-{w}-Tile-Rounded-Charcoal-Two-Color.svg"))) for cid, w in PILLARS]
    APPROVED = "Design judgment, approved by our founder and editor in November 2026"
    return {
        "number": "09", "anchor": "pillar-icons", "title": "Pillar icons", "part": "Symbols and graphics",
        "instruction": "Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act.",
        "intro": [
            "Our four pillars name the jobs our work does: Explain, Track, Connect and Act, in that order (chapter 01). Each pillar "
            "has an icon from the Civic Line, the symbol set in chapter 10, and each icon stands beside its word.",
            "This chapter sets the row the four stand in, how a page marks the pillar it serves, the file to draw at each size, "
            "and the few places a pillar icon may appear.",
        ],
        "rules": [
            R("09.1", "Set the four pillar icons in order, each beside its word.",
              "Set the pillars in one row in the order Explain, Track, Connect and Act, with an arrow between each pair. Each icon "
              "stands beside its word at every size, so the word names the pillar and the icon shows it a second way. A row takes "
              "one icon size throughout, 48 px with the words in the intro style or 24 px with the words in body text. Every icon "
              "in it is one color, unless the row marks a current pillar (Rule 09.2).",
              "The order follows the work, from understanding a decision to taking part in it, so it never changes. A reader learns "
              "four drawings faster with their words beside them, and the word settles a drawing that could pass for another "
              "pillar: Track's magnifier can read as looking into a question, which is Explain's job.",
              APPROVED,
              "The pillar row at true size on Newsprint and on Charcoal, at 48 and 24 px: each icon beside its word, in order, one "
              "color, with an arrow between each pair.",
              "The four icons in a row with no words. A reader has to decode each drawing, and nothing tells Track's magnifier "
              "from a search button.",
              tokens=["oa.component.icon.ink.onNewsprint", "oa.size.icon.large", "oa.size.icon.medium"],
              specs=[SP_("Order", "Explain, Track, Connect, Act, with an arrow between each pair; the arrows are hidden from screen "
                                  "readers, since the list's order carries the sequence"),
                     SP_("48 px row", "Words in the intro style, bold, 19 px on a phone and 22 px from 48em; 12 px from each icon's ink to its word"),
                     SP_("24 px row", "Words in body text, 17 px; 8 px from each icon's ink to its word"),
                     SP_("Spacing", "Measured from each icon's ink, so Act's narrow hand sits as close to its word as Explain's book; in a stacked column, from each icon's whole box, so the four words share one left edge"),
                     SP_("Color", "One color in the surface's icon ink: Charcoal on Newsprint and White, Newsprint on Charcoal and Prussian",
                         "oa.component.icon.ink.onNewsprint"),
                     SP_("Under 48em", "The 48 px row stacks in one column with downward arrows; the 24 px row wraps after an arrow")],
              files=[A + m.split("work/build/assets/", 1)[1] for m in masters],
              related=["01", "10"],
              builders="Build the row as an ordered list whose text is the four words, and draw each icon from the sprite beside its "
                       "word, hidden from screen readers with <code>aria-hidden=\"true\"</code>. Draw the arrows in CSS as content a "
                       "screen reader skips, <code>content: \"→\" / \"\"</code>. Pull each icon's box in to its ink with negative "
                       "margins, whole pixels at 16 and 24 px."),
            R("09.2", "Underline the current pillar's word, and add its red only from 48 px.",
              "On a page or a section that serves one pillar, underline that pillar's word in the row, at every size, and set the "
              "word bold under 48 px. From 48 px the current icon also keeps its red, as a second sign, and the red counts as "
              "signature red (Rule 05.3). Under 48 px every icon stays one color, the current one included. On Prussian no icon "
              "takes red, so the underline marks the current pillar alone.",
              "An underline marks the current pillar in any color and in gray print, so the row never relies on red alone. Red "
              "works as a second sign once the icon's line reaches a full pixel at 48 px. Under 48 px the line is a pixel or "
              "thinner, and a red line that thin stops reading as Pillar Red.",
              "WCAG 2.2 SC 1.4.1; " + APPROVED[0].lower() + APPROVED[1:],
              "A section that serves Track: the 48 px row with Track's word underlined and its icon in red, on Newsprint and on "
              "Charcoal, and the 24 px row with the word Track bold and underlined and every icon one color.",
              "Track marked by its red icon alone, with no underline. A reader who cannot tell red from Charcoal, or who reads the "
              "page in gray print, sees no current pillar.",
              tokens=["oa.component.icon.accent.onNewsprint", "oa.component.icon.accent.onCharcoal"],
              specs=[SP_("Underline", "2 px, solid, 5 px under the baseline, at every size"),
                     SP_("Bold", "The current word, under 48 px"),
                     SP_("Red", "From 48 px, the current icon's accent, as signature red; never on Prussian",
                         "oa.component.icon.accent.onNewsprint"),
                     SP_("Screen readers", "The current item carries aria-current, so the reader hears which pillar the page serves")],
              related=["05", "19"],
              builders="Mark the current item with <code>aria-current=\"true\"</code> and style its word from that attribute, so the "
                       "underline and the announcement come from one source. Set <code>--oa-icon-accent</code> on the current "
                       "icon's svg only, and only at 48 px and up."),
            R("09.3", "Draw a pillar icon from the file made for its size.",
              "Each size has its own drawing. At 16 px, draw the 16 px pixel fit on every screen. At 24 px, draw the 24 px pixel "
              "fit on screens under 2x, which give each CSS pixel fewer than two device pixels, and the master on 2x screens and "
              "denser, with both in one svg that the guide's stylesheet switches. From 48 px, draw the master. Never scale a master "
              "to 16 px, and never draw a fit at any size but its own.",
              "The masters are drawn on a 128-unit box with a line about 3 units wide, so at 24 px the line falls to half a pixel, "
              "and at 16 px small gaps fill in. Each pixel fit redraws its icon on whole pixels with a 1 px line and keeps every "
              "feature. A 24 px icon keeps its fit up to 2x, since below 2x the master's line falls under one device pixel and "
              "its counters fill, and the fit keeps every counter and gap. From 2x the master's line clears a device pixel and "
              "draws smoother than the fit's steps.",
              "Our measurements, November 2026; the pixel fits approved by our founder and editor in November 2026",
              "Each pillar at 16, 24, 48 and 96 px at true size, one color, each from the file made for its size; below, Track's "
              "16 and 24 px fits as a standard screen draws them, enlarged four times.",
              "Track's master scaled to 16 px beside its 16 px fit, at true size and enlarged four times. The master's lines fall "
              "under a pixel and draw gray, and its magnifier blurs.",
              tokens=["oa.size.icon.small", "oa.size.icon.medium", "oa.size.icon.large"],
              specs=[SP_("16 px", "The 16 px pixel fit, on every screen", "oa.size.icon.small"),
                     SP_("24 px", "The 24 px pixel fit on screens under 2x; the master from 2x", "oa.size.icon.medium"),
                     SP_("48 px and up", "The master, at whole pixel sizes", "oa.size.icon.large"),
                     SP_("Line", "1 px in each fit; about 3 units of 128 in each master"),
                     SP_("Color", "One color under 48 px (Rule 09.2)"),
                     SP_("Never", "A master under 48 px, except as a 24 px icon on a 2x screen; a fit at any size but its own")],
              files=_fits() + [A + "pillar-icons/20261110_Pillar-Icons-Manifest.json"],
              related=["10", "19"],
              builders="Write a 24 px icon as one svg holding two uses: the fit with the class <code>oa-at-1x</code> and the master "
                       "with <code>oa-at-2x</code>, as in <code>&lt;use class=\"oa-at-1x\" href=\"#oa-sym-cl-020-24px\"/&gt;&lt;use "
                       "class=\"oa-at-2x\" href=\"#oa-sym-cl-020\"/&gt;</code>. The guide's stylesheet shows the master from 2 "
                       "device pixels per CSS pixel. A 16 px icon is one use of its fit. Give the svg whole-pixel coordinates, and "
                       "set no accent under 48 px."),
            R("09.4", "Put pillar icons only in the pillar row, on section openers and on tiles.",
              "A pillar icon appears in three places: the pillar row; the opener of a section that serves one pillar, where it "
              "stands at 128 px; and a tile that leads to a pillar's section, from 76 px. It never enters a kicker, which may carry "
              "a topic icon only (Rule 01.21), and it never sits on a part opener.",
              "Four icons that turn up only where a pillar is named stay easy to learn. In a kicker, a pillar icon would sit "
              "beside a label such as Report or Guide, which names no pillar, and leave the reader to decode the drawing.",
              APPROVED,
              "Track's section opener at true size, a Charcoal panel with the icon at 128 px in Newsprint and red above the "
              "section's line, and a card that leads to Track's section, with the icon on the rounded Charcoal tile at 76 px.",
              "A report's kicker with Track's icon before its label. The label says Report, the icon says Track, and no word "
              "beside the icon names the pillar.",
              tokens=["oa.component.icon.ink.onCharcoal", "oa.component.icon.accent.onCharcoal"],
              specs=[SP_("Pillar row", "48 or 24 px (Rules 09.1 and 09.2)"),
                     SP_("Section opener", "128 px on a Charcoal panel, in Newsprint with its red, with the pillar's word"),
                     SP_("Tile", "The rounded two-color tile on Charcoal, from 76 px (Rule 10.5); in a row of tiles, the one-color "
                                 "tiles, with only the current one in two colors"),
                     SP_("Never", "A kicker, a part opener, a button or a bullet")],
              files=[A + t.split("work/build/assets/", 1)[1] for t in tiles],
              related=["01", "10"],
              builders="Take a pillar's tile from the Civic Line package's rounded Charcoal tiles. A standalone icon on an opener "
                       "keeps its red as signature red; give it the word of its pillar nearby."),
        ],
        "extras": [{"after_rule": "09.1", "specimen": "s-09-phone", "label": "The row on a phone",
                    "caption": "On a phone the 48 px row stands in one column with downward arrows, and the 24 px row wraps after "
                               "an arrow."}],
        "related_chapters": [{"chapter": "01", "reason": "The four pillars, their jobs and their products."},
                             {"chapter": "10", "reason": "The Civic Line's construction, editions, tiles and sizes."},
                             {"chapter": "05", "reason": "Rule 05.3, the red rule the current pillar's icon follows."},
                             {"chapter": "11", "reason": "Status and utility icons, which name states and actions."}],
        "sources": [],
    }
