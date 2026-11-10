"""Chapter 08 The lockmark: specimens.

Apply pass, November 7, 2026 (DR-110, D2-325 to D2-327): the lockmark keeps four fixed places and codes nothing. Rule
08.1 keeps its plates. Rule 08.2 draws the four places at true size: the masthead (L3 from 768 px), the page header
(24 px beside the section label), the footer (24 px beside the tagline, 16 px in a chart's footer) and the sign-off
(48 px from the display master). Rule 08.3 shows a bill as chapter 11 draws it, and the same bill drawn on the grid as a
labeled failure. The old Rules 08.3 to 08.9, the codes table, the stages sheet and the composer leave the chapter.

Q1 to Q4 pass, November 8, 2026 (DR-131, CD-N9): the masthead (L3's masthead master) and the sign-off draw the 48 px
master at 48 px; Rule 08.1's plate shows the four masters; Rule 08.2's places stand 16 px in from the frame.

Promotion, November 10, 2026 (DR-181): the 24 and 48 px masters are the rebuilt files, each node and the lever one
outline, through stage_a_identity_lib.LOCK; the drawings on the plates keep the same pixels."""
from stage_a_identity_lib import (E, LOCK, fragment, mark, lockmark, sgrid, progress, illus, head_label, dnp, steps, ink, ink2,
                                  hair, pal, ground, ty, tv)
from stage_a_identity_s03 import rec as _rec, l3_small

S = []
PHONE = 358
TAGLINE = "A country that answers to its people."


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "08")
    return _rec(*a, **k)


# ------------------------------------------------------------------------------------------- 08.1
@spec
def s_08_1_correct():
    k = 240 / 123.5
    a = ink("newsprint")
    lines = []
    for c in (11.75, 61.75, 111.75):
        X = 64 + c * k
        lines.append(f'<line x1="{X:.1f}" x2="{X:.1f}" y1="24" y2="36" stroke="{a}" stroke-width="1"/>')
        lines.append(f'<text x="{X:.1f}" y="18" text-anchor="middle" font-size="13" fill="{a}">{c:g}</text>')
    lines.append(f'<text x="{64 + 240 + 16}" y="{40 + 111.75 * k + 5:.1f}" font-size="13" fill="{a}">Lever, radius 4.75, Pillar Red</text>')
    lines.append(f'<text x="{64 + 240 + 16}" y="{40 + 61.75 * k + 5:.1f}" font-size="13" fill="{a}">Node, radius 3.8</text>')
    lines.append(f'<text x="{64 + 240 + 16}" y="{40 + 11.75 * k + 5:.1f}" font-size="13" fill="{a}">Links, 1 px Stone</text>')
    lines.append(f'<text x="64" y="{40 + 240 + 24}" font-size="13" fill="{a}">Field 123.5 units; node centers 11.75, 61.75 and 111.75 on each axis</text>')
    over = (f'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="320" viewBox="0 0 560 320" aria-hidden="true" class="oai-svg" '
            f'style="position:absolute;left:0;top:0;font-family:var(--oa-font-family-reading)">{"".join(lines)}</svg>')
    cons = (f'<div style="position:relative;width:560px;height:320px">{over}'
            f'<div style="position:absolute;left:64px;top:40px">{mark(LOCK["display"], h=240, label="Lockmark construction, display master at 240 px")}</div></div>')

    def it(lbl, inner):
        return f'<div class="oai-cell">{inner}<span class="oai-tag">{E(lbl)}</span></div>'
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:24px">' + cons
            + '<div class="oai-row">'
            + it("Display master, 96 px", lockmark(96, label="Lockmark, display master, at 96 px"))
            + it("48 px master", lockmark(48, label="Lockmark, 48 px master"))
            + it("24 px master", lockmark(24, label="Lockmark, 24 px master"))
            + it("16 px master", lockmark(16, label="Lockmark, 16 px master"))
            + f'<div class="oai-cell"><div class="oai-s-charcoal" style="padding:12px">{lockmark(48, surface="charcoal", label="Lockmark at 48 px on Charcoal")}</div><span class="oai-tag">On Charcoal</span></div>'
            + f'<div class="oai-cell"><div class="oai-s-prussian" style="padding:12px">{lockmark(48, surface="prussian", label="Lockmark at 48 px on Prussian, all White")}</div><span class="oai-tag">On Prussian, all White</span></div>'
            + '</div></div></div>')
    alt = ("The lockmark: nine nodes on a three by three grid joined by thin links around the edge and through the center, with "
           "a larger red node, the lever, at bottom right. Its construction at 240 pixels with the node centers and radii, then "
           "its four masters at true size: the display master at 96 pixels with fine links and small nodes, and the 48, 24 and "
           "16 pixel masters, each heavier, with the same nine nodes, links and lever. Last, the 48 pixel master on Charcoal, "
           "in Newsprint with its red lever, and on Prussian, all in White.")
    return rec("s-08-1-correct", "08.1", 700, alt, body, fit_switch=True,
               notes="Construction from the display master at 240 px. The four masters each at their own size (DR-131): the display "
                     "master at 96 px, then the 48, 24 and 16 px masters on whole pixels. The 48 and 24 px masters are the rebuilt "
                     "files in use since November 10, 2026, each node and the lever one outline (DR-181): "
                     "lockmark/20261109_Lockmark-48px-Master-Outline.svg and lockmark/20261109_Lockmark-24px-Master-Outline.svg, the "
                     "same pixels as the earlier files at these sizes (DR-145). The 16 px master is unchanged. On Prussian, the rebuilt "
                     "48 px master's White file.")


@spec
def s_08_1_failure():
    v = mark(LOCK["display"], h=16, decorative=True)
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row mid">'
            f'<span class="oai-red" data-red="signature" data-failure="true">{v}</span>'
            f'<span class="oai-tag">The fifth edition\'s master scaled to 16 px</span>'
            f'<span style="width:24px"></span>{lockmark(16, label="The 16 px master, for comparison")}<span class="oai-tag">The 16 px master</span></div></div>')
    alt = ("Failure case: the lockmark master from our brand guide's fifth edition scaled to 16 pixels, its nodes no wider "
           "than its links and the lever a single pink pixel, beside the 16 pixel master for comparison.")
    return rec("s-08-1-failure", "08.1", 420, alt, body)


# ------------------------------------------------------------------------------------------- 08.2
PLACE_CSS = (".oai-pl8{display:flex;flex-direction:column;gap:28px;padding:12px 16px 16px}"
             ".oai-pl8 .oai-pl8-h{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;margin:0 0 8px}"
             ".oai-pl8 .oai-pl8-n{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}"
             ".oai-pl8-row{display:flex;flex-wrap:wrap;gap:16px 24px;align-items:flex-start}")


def _place(name, where, inner, scope=""):
    lab = f'{illus()}<span class="oai-tag">{E(scope)}</span>' if scope else ""
    return (f'<div><p class="oai-pl8-h"><span class="oai-pl8-n">{E(name)}</span><span class="oai-tag">{E(where)}</span>{lab}</p>'
            f'{inner}</div>')


def _masthead():
    nav = "".join(f'<span style="{ty("ui")};white-space:nowrap">{t}</span>' for t in ("Explain", "Track", "Connect", "Act"))
    return (f'<div class="oai-s-newsprint" style="width:768px;height:80px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 32px;border:1px solid {hair("newsprint")}">{l3_small(24, label="Oath & Action, L3: the wordmark with the lockmark at 48 px")}'
            f'<div style="display:flex;gap:24px">{nav}</div></div>')


def _page_header():
    return (f'<div class="oai-s-white" style="width:600px;display:flex;align-items:center;gap:12px;padding:16px 24px;border:1px solid {hair("white")}">'
            f'{lockmark(24, surface="white", label="Lockmark, 24 px, in a page header")}'
            f'<span class="oai-label" style="color:{ink("white")}">03 · Who writes the budget</span>'
            f'<span style="margin-left:auto;{ty("caption")};color:{ink2("white")}" class="oai-num">7</span></div>')


def _footer():
    return (f'<div class="oai-s-charcoal" style="width:600px;display:flex;align-items:center;gap:12px;padding:16px 24px">'
            f'{lockmark(24, surface="charcoal", label="Lockmark, 24 px, in a footer on Charcoal")}'
            f'<span style="{ty("body-small")};color:{ink("charcoal")}">{E(TAGLINE)}</span></div>')


CHART_SOURCE = ("Source: U.S. Bureau of Labor Statistics, Current Employment Statistics, all nonfarm employees, monthly change, "
                "seasonally adjusted, January 2022 to September 2026, United States, via FRED, Federal Reserve Bank of St. Louis. "
                "Retrieved November 6, 2026.")


def _chart_foot():
    return (f'<div class="oai-s-newsprint" style="width:600px;display:flex;align-items:flex-end;gap:16px;padding:12px 24px 16px;'
            f'border:1px solid {hair("newsprint")};border-top:2px solid {tv("color-border-strong-on-newsprint")}">'
            f'<span style="flex:1;{ty("caption")};color:{ink2("newsprint")}">{E(CHART_SOURCE)}</span>'
            f'{lockmark(16, label="Lockmark, 16 px, in a chart footer")}</div>')


def _signoff():
    """The bottom-right corner of a 1080 px social card at true size: its right and bottom edges, the lockmark at 48 px
    from its 48 px master 72 px in from each, and two dimension lines that measure the margin."""
    W, H, M, L = 360, 216, 72, 48
    st = pal("stone")
    cx, cy = W - M - L / 2, H - M - L / 2          # the lockmark's center
    dims = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true" class="oai-svg" '
            f'style="position:absolute;left:0;top:0" stroke="{st}" stroke-width="1" fill="none">'
            f'<path d="M{W - M + 6} {cy + 0.5}H{W - 1}M{W - M + 6} {cy - 3.5}v8"/>'
            f'<path d="M{cx + 0.5} {H - M + 6}V{H - 1}M{cx - 3.5} {H - M + 6}h8"/></svg>')
    labels = (f'<span class="oai-tag" style="position:absolute;left:16px;top:14px">Corner of a 1080 px card</span>'
              f'<span class="oai-tag" style="position:absolute;right:8px;top:{cy - 26:.0f}px">72 px</span>'
              f'<span class="oai-tag" style="position:absolute;right:{M + L / 2 + 8:.0f}px;bottom:28px">72 px</span>')
    return (f'<div class="oai-s-newsprint" style="position:relative;width:{W}px;height:{H}px;border-right:1px solid {ink("newsprint")};'
            f'border-bottom:1px solid {ink("newsprint")};overflow:hidden">{dims}{labels}'
            f'<span style="position:absolute;right:{M}px;bottom:{M}px;line-height:0">{lockmark(L, label="Lockmark, 48 px, the sign-off")}</span></div>')


@spec
def s_08_2_correct():
    body = ('<div class="oai-pl8">'
            + _place("Masthead", "L3 on screens from 48em, 768 px at the default text size; the lockmark at 48 px", _masthead())
            + _place("Page header", "24 px, beside the section label on a report page", _page_header(), "The section title is invented.")
            + _place("Footer", "24 px beside the tagline; 16 px beside the source line in a chart's footer",
                     f'<div class="oai-stack" style="gap:12px">{_footer()}{_chart_foot()}</div>')
            + _place("Sign-off", "48 px, bottom right of a social card, cover or poster", _signoff())
            + '</div>')
    alt = ("The lockmark's four places at true size, one under another. Masthead: a 768 pixel Newsprint bar with the wordmark "
           "and the lockmark at 48 pixels at left and four navigation words at right. Page header: a white report header with the lockmark "
           "at 24 pixels beside the section label 03 Who writes the budget and the page number 7; the section title is "
           "Illustrative. Footer: a Charcoal footer with the lockmark at 24 pixels beside the tagline, A country that answers "
           "to its people., and a chart's footer with its source line and the lockmark at 16 pixels at right. Sign-off: the "
           "bottom-right corner of a 1080 pixel social card with the lockmark at 48 pixels inside its 72 pixel margin.")
    return rec("s-08-2-correct", "08.2", 802, alt, body, css=PLACE_CSS, fit_switch=True,
               notes="DR-110 and DR-131. Footer place: the lockmark, 12 px, then the tagline, at the footer's left edge, as the "
                     "letterhead proof draws it too (CA-S10). Masthead: L3's masthead master, the 24 px wordmark master with the "
                     "lockmark at 48 px from its 48 px master, in a 768 px bar (Rule 03.6's breakpoint). Page header and footer: the "
                     "24 px master on whole pixels. Chart footer: the 16 px master beside chapter 02's jobs chart source line, word "
                     "for word. Sign-off: the 48 px master at 48 px, 72 px from the card's right and bottom edges (D2-295's card "
                     "margin). The places and their labels stand 16 px in from the frame (CD-N9), so the plate is 802 px wide. Type "
                     "takes sizes common to both columns of the scale (13 to 17 px). Since November 10, 2026 the 48 and 24 px masters "
                     "are the rebuilt files, each node and the lever one outline, and L3's masthead master is "
                     "lockups/20261110_L3-Horizontal-Master.svg, which carries the rebuilt 48 px master; each draws the same pixels "
                     "as before (DR-145, DR-181). The 16 px master is unchanged.")


@spec
def s_08_2_failure():
    items = ["Read the agenda a week ahead", "Sign up with the clerk to speak", "Bring two printed copies of your comment"]
    li = "".join(f'<li style="display:flex;gap:12px;align-items:center;margin:10px 0"><span class="oai-red" data-red="signature" data-failure="true">{lockmark(16, decorative=True)}</span><span>{E(t)}</span></li>' for t in items)
    flyer = (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:20px;border:1px solid {hair("newsprint")}">'
             f'{head_label()}<p style="{ty("h3")}">How to speak at a council meeting</p>'
             f'<ul style="list-style:none;padding:0;margin:12px 0 0;{ty("body")}">{li}</ul></div>')
    body = f'<div style="width:{PHONE}px">{dnp()}{flyer}</div>'
    alt = ("Failure case: do not publish. A flyer, How to speak at a council meeting, whose three list items each start with a "
           "16 pixel lockmark used as a bullet. Illustrative.")
    return rec("s-08-2-failure", "08.2", PHONE, alt, body, illustrative=True,
               notes="The flyer could pass for our work, so it carries the Charcoal failure band (D2-308; CD-N5, CA-S6).")


# ------------------------------------------------------------------------------------------- 08.3
BILL = ("Bill S.0876", "School bus contracts")
BILL_STATES = ["done", "done", "done", "now", "notyet", "notyet"]          # Board 6's S.0876, at step 4 of 6
BILL_WORDS = ("Step 4 of 6: First chamber.", "The committee sent it on, and the Senate votes next.")


def _bill_card(mark_html, gap=12):
    return (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:16px 16px 18px;border:1px solid {hair("newsprint")}">'
            f'{head_label()}<p style="{ty("body")};margin:0 0 {gap}px"><b>{E(BILL[0])}</b>, {E(BILL[1])}</p>{mark_html}'
            f'<p style="{ty("body-small")};margin-top:10px"><b>{E(BILL_WORDS[0])}</b> {E(BILL_WORDS[1])}</p></div>')


@spec
def s_08_3_correct():
    body = f'<div>{_bill_card(steps(BILL_STATES, 324, 26))}</div>'
    alt = ("A bill in a tracker list at true size on a 358 pixel phone column: Bill S.0876, School bus contracts, with six "
           "numbered steps on a line. Steps 1 to 3 are filled circles, step 4 is a heavy ring marking the step the bill is at, "
           "and steps 5 and 6 are fine rings ahead. Under them: Step 4 of 6: First chamber. The committee sent it on, and the "
           "Senate votes next. No lockmark sits in the row. Illustrative.")
    return rec("s-08-3-correct", "08.3", PHONE, alt, body, illustrative=True,
               notes="Chapter 11 owns these marks (DR-108, DR-109, D2-324); checked against s-11-list-360-charcoal, same geometry. Drawn with the geometry of Board 6's Option B at its 360 px "
                     "list size (324 px wide, 26 px circles, Inter 13 px numbers), from board6_tracker_build.py's b_node and mk_steps, "
                     "colored with tokens. S.0876 and its states are Board 6's, invented (DR-97). If chapter 11 changes the marks, this "
                     "plate follows them.")


@spec
def s_08_3_failure():
    g = sgrid(40, nodes=progress(4), decorative=True)
    body = f'<div style="width:{PHONE}px">{dnp()}{_bill_card(g)}</div>'
    alt = ("Failure case: do not publish. The same bill, S.0876, School bus contracts, drawn on the lockmark's nine nodes at 40 "
           "pixels with four nodes filled to show progress, beside the same words, Step 4 of 6: First chamber. Nine nodes cannot "
           "count six steps, and the mark that signs our pages changes from bill to bill. Illustrative.")
    return rec("s-08-3-failure", "08.3", PHONE, alt, body, illustrative=True,
               notes="One retired use (DR-110): tracker progress on the grid, drawn as the stage A Rule 08.5 drew it (40 px lattice on "
                     "whole pixels, filled 7 px discs for done, 3 px Stone nodes ahead), under the Charcoal failure band (D2-308).")
