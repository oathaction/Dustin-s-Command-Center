"""Chapter 08 The Signal Grid: specimens, the composer demo and the rasterized kicker for its failure case.

Fix pass, November 6, 2026: the nine stages take plain names, and each is explained once per tracker page and in the
stages sheet (CP-M9, RP-S8); the tracker list shows a phone column first and a 600 px page under it (CP-S19); every
kicker follows Rule 01.21 (D2-250, RP-M1); the codes table and the stages sheet are readable to assistive technology
(AX-S9, AX-S2); the composer fills its column and ties its disabled option to its reason (AX-S5, AX-S15); sheets flow."""
import json

from stage_a_identity_lib import (E, ID_DIR, LOCK, SERIES, STAGES, GLOSS, PILLAR_CORNER, POS, NAMES, fragment, mark, lockmark,
                                  sgrid, progress, corner, icon, illus, head_label, tag, ink, ink2, hair, pal, tv, sig, ground,
                                  g_ess, g_sub, svg_file, ty, raster_png)
from stage_a_identity_s03 import rec as _rec

S = []
PHONE = 358


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "08")
    return _rec(*a, **k)


def key_text(nodes):
    """The words a progress grid stands for."""
    stage = max((i + 1 for i, n in enumerate(nodes) if n in ("done", "now", "step")), default=0)
    if stage == 0:
        return "Nothing filed yet"
    st = nodes[stage - 1]
    t = f"Stage {stage} of 9: {STAGES[stage - 1]}"
    if st in ("now", "step"):
        t += ", under way"
    gaps = [STAGES[i] for i, n in enumerate(nodes) if n == "gap"]
    if gaps:
        t += ". No hearing was held" if gaps[0] == "Hearing" else f". {gaps[0]} never happened"
    return t


LEGEND_CSS = (".oai-lg{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:14px;line-height:1.5}"
              ".oai-lg span{display:inline-flex;align-items:center;gap:6px}"
              ".oai-gl{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr));gap:4px 24px;margin:0;padding:0;list-style:none;font-size:14px;line-height:1.45}"
              ".oai-gl b{font-weight:600}")


def legend(surface="newsprint", step=True):
    e, sb = g_ess(surface), g_sub(surface)

    def sh(inner):
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" width="12" height="12" aria-hidden="true" class="oai-svg">{inner}</svg>'
    items = [
        (sh(f'<circle cx="6" cy="6" r="3.5" fill="{e}"/>'), "Done"),
        (sh(f'<circle cx="6" cy="6" r="3" fill="none" stroke="{e}" stroke-width="1"/>'), "Under way"),
        (sh(f'<rect x="0" y="5.5" width="2" height="1" fill="{sb}"/><rect x="10" y="5.5" width="2" height="1" fill="{sb}"/>'), "Never happened"),
        (sh(f'<circle cx="6" cy="6" r="1.5" fill="{sb}"/>'), "Not yet reached"),
    ]
    if step:
        kl = f' stroke="{tv("color-border-strong-on-" + surface)}" stroke-width="1"' if surface in ("newsprint", "white") else ""
        items.append((f'<span class="oai-red" data-red="working" data-red-job="the step a reader can take now">'
                      + sh(f'<circle cx="6" cy="6" r="3" fill="{tv("color-palette-pillar-red")}"{kl}/>') + '</span>', "You can take part now"))
    return '<p class="oai-lg">' + "".join(f'<span>{s}{E(t)}</span>' for s, t in items) + '</p>'


def glossary(which=range(9)):
    """What the stages mean, once per tracker page (CP-M9)."""
    return ('<ol class="oai-gl">' + "".join(f'<li><b>{i + 1} {E(STAGES[i])}.</b> {E(GLOSS[i])}</li>' for i in which) + '</ol>')


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
            + it("96 px, display master", lockmark(96, label="Lockmark at 96 px"))
            + it("48 px, display master", lockmark(48, label="Lockmark at 48 px"))
            + it("24 px master", lockmark(24, label="Lockmark, 24 px master"))
            + it("16 px master", lockmark(16, label="Lockmark, 16 px master"))
            + f'<div class="oai-cell"><div class="oai-s-charcoal" style="padding:12px">{lockmark(48, surface="charcoal", label="Lockmark at 48 px on Charcoal")}</div><span class="oai-tag">On Charcoal</span></div>'
            + f'<div class="oai-cell"><div class="oai-s-prussian" style="padding:12px">{lockmark(48, surface="prussian", label="Lockmark at 48 px on Prussian, all White")}</div><span class="oai-tag">On Prussian, all White</span></div>'
            + '</div></div></div>')
    alt = ("The lockmark: nine nodes on a three by three grid joined by thin links around the edge and through the center, with "
           "a larger red node, the lever, at bottom right. Its construction at 240 pixels with the node centers and radii, then "
           "true-size versions at 96, 48, 24 and 16 pixels, and at 48 pixels on Charcoal and on Prussian, where it is all White.")
    return rec("s-08-1-correct", "08.1", 700, alt, body)


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
@spec
def s_08_2_correct():
    corner_ = (f'<div class="oai-s-newsprint" style="position:relative;width:360px;height:240px;border:1px solid {hair("newsprint")};overflow:hidden">'
               f'<p class="oai-tag" style="position:absolute;left:24px;top:20px">Bottom-right corner of a report cover, 0.5 in margin</p>'
               f'<span style="position:absolute;right:48px;bottom:48px">{lockmark(40, label="Lockmark anchored at bottom right, 40 px")}</span></div>')
    header = (f'<div class="oai-s-white" style="width:{PHONE}px;display:flex;align-items:center;gap:12px;padding:16px 20px;border:1px solid {hair("white")}">'
              f'{lockmark(24, surface="white", label="Lockmark as a section marker, 24 px")}'
              f'<span class="oai-label">03 · Who writes the budget</span></div>')
    body = ('<div class="oai-stack" style="gap:28px">'
            f'<div class="oai-cell">{corner_}<span class="oai-tag">Anchor, 40 px, inside the margin</span></div>'
            f'<div class="oai-cell">{header}<span class="oai-tag">{illus()}Section marker, 24 px, beside an invented section label</span></div></div>')
    alt = ("Two fixed places at true size: the lockmark at 40 pixels in the bottom-right corner of a report cover, half an "
           "inch in from both edges; and the lockmark at 24 pixels beside the section label 03 Who writes the budget at the "
           "top of a report page. The section label is Illustrative.")
    return rec("s-08-2-correct", "08.2", 360, alt, body, illustrative=True)


@spec
def s_08_2_failure():
    items = ["Read the agenda a week ahead", "Sign up with the clerk to speak", "Bring two printed copies of your comment"]
    li = "".join(f'<li style="display:flex;gap:12px;align-items:center;margin:10px 0"><span class="oai-red" data-red="signature" data-failure="true">{lockmark(16, decorative=True)}</span><span>{E(t)}</span></li>' for t in items)
    flyer = (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:20px;border:1px solid {hair("newsprint")}">'
             f'{head_label()}<p style="{ty("h3")}">How to speak at a council meeting</p>'
             f'<ul style="list-style:none;padding:0;margin:12px 0 0;{ty("body")}">{li}</ul></div>')
    body = f'<div>{flyer}</div>'
    alt = "Failure case: a flyer, How to speak at a council meeting, whose three list items each start with a 16 pixel lockmark used as a bullet. Illustrative."
    return rec("s-08-2-failure", "08.2", PHONE, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 08.3
def _row(bill, topic, nodes, keyed=True, surface="newsprint", extra=""):
    g = sgrid(40, nodes=nodes, surface=surface, decorative=keyed, label=key_text(nodes))
    k = (f'<span style="{ty("body-small")};color:{ink2(surface)}">{E(key_text(nodes))}{E(extra)}</span>' if keyed else "")
    return (f'<div style="display:flex;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid {hair(surface)}">'
            f'{g}<div style="display:flex;flex-direction:column;gap:2px"><span style="{ty("body")};font-weight:600">{E(bill)}, {E(topic)}</span>{k}</div></div>')


@spec
def s_08_3_correct():
    box = (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:8px 20px;border:1px solid {hair("newsprint")}">'
           f'{_row("Bill S.0876", "School bus contracts", progress(4))}</div>')
    body = f'<div>{head_label()}{box}</div>'
    alt = ("A tracker row at true size: a 40 pixel Signal Grid with its first four nodes filled, beside Bill S.0876, School bus "
           "contracts, and its key, Stage 4 of 9: Out of committee. Illustrative.")
    return rec("s-08-3-correct", "08.3", PHONE, alt, body, illustrative=True)


@spec
def s_08_3_failure():
    box = (f'<div class="oai-s-newsprint" style="width:{PHONE}px;padding:8px 20px;border:1px solid {hair("newsprint")}">'
           f'{_row("Bill S.0876", "School bus contracts", progress(4), keyed=False)}</div>')
    body = f'<div>{head_label()}{box}</div>'
    alt = "Failure case: the same tracker row with the grid and no key. Four filled nodes sit beside the bill name with nothing to say what they count. Illustrative."
    return rec("s-08-3-failure", "08.3", PHONE, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 08.4
@spec
def s_08_4_correct():
    def it(g, k):
        return f'<div class="oai-cell" style="max-width:200px">{g}<span style="{ty("body-small")}">{k}</span></div>'
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row top" style="gap:40px">'
            + it(sgrid(40, nodes=progress(5, now=True), decorative=True), "<b>Tracker progress.</b> Stage 5 of 9: Passed one chamber, under way")
            + it(sgrid(40, route=SERIES[2][2], decorative=True), "<b>Series route.</b> Dispatch, a Track series, ending top right")
            + it(sgrid(40, nodes=corner("Connect"), decorative=True), "<b>Pillar corner.</b> Connect, bottom left. It shares its grid with nothing else.")
            + '</div></div>')
    alt = ("The three codes at 40 pixels, each with its key: a tracker grid with four filled nodes and a ring on the fifth, "
           "Stage 5 of 9, Passed one chamber, under way; the Dispatch series route, a heavy line from the middle left through "
           "the center and up to the top right corner; and a pillar corner with only the bottom-left node lit, for Connect, "
           "which shares its grid with nothing else.")
    return rec("s-08-4-correct", "08.4", None, alt, body, notes="A sheet that flows; each grid keeps its 40 px.")


@spec
def s_08_4_failure():
    colors = [("Explainer, Prussian", pal("prussian")), ("Tracker, Verdigris", pal("verdigris")), ("Analysis, Charcoal", pal("charcoal")),
              ("A step to take now, red", tv("color-palette-pillar-red"))]

    def v5grid(c, red):
        nodes = "".join(f'<circle cx="{x}" cy="{y}" r="1.5" fill="{pal("stone")}"/>' for y in (3.5, 11.5, 19.5) for x in (3.5, 11.5, 19.5) if not (x == 11.5 and y == 11.5))
        lit = f'<circle cx="11.5" cy="11.5" r="2.5" fill="{c}"/>'
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 23 23" width="24" height="24" aria-hidden="true" class="oai-svg">'
               f'<g fill="{pal("stone")}"><rect x="3.5" y="3" width="16" height="1"/><rect x="3.5" y="11" width="16" height="1"/><rect x="3.5" y="19" width="16" height="1"/>'
               f'<rect x="3" y="3.5" width="1" height="16"/><rect x="11" y="3.5" width="1" height="16"/><rect x="19" y="3.5" width="1" height="16"/></g>{nodes}{lit}</svg>')
        return f'<span class="oai-red" data-red="working" data-red-job="failure case" data-failure="true">{svg}</span>' if red else svg

    def row(gray):
        st = ' style="filter:grayscale(1)"' if gray else ""
        return (f'<div class="oai-row"{st}>' + "".join(f'<div class="oai-cell">{v5grid(c, i == 3)}<span class="oai-tag" style="filter:none">{E(n)}</span></div>' for i, (n, c) in enumerate(colors)) + '</div>')
    body = (f'<div class="oai-panel oai-s-newsprint">'
            f'<div class="oai-stack"><p class="oai-tag">In color</p>{row(False)}<p class="oai-tag">In grayscale</p>{row(True)}</div></div>')
    alt = ("Failure case: our fifth edition's four content-type grids at 24 pixels, each lighting its center node in a "
           "different color: Prussian, Verdigris, Charcoal and red. Converted to grayscale, the four lit nodes turn into "
           "near-identical dark grays.")
    return rec("s-08-4-failure", "08.4", 520, alt, body, check_exempt=["red"],
               notes="Redrawn from V5's rule B captions at its 24 px kicker size. A labeled failure that shows V5's red content-type node, so check_exempt red.")


@spec
def s_08_combinations():
    rows = [
        ("1", "Tracker progress", "Which stages a bill or record has passed, which one is under way, and which never happened", "40 px", "One red node for the stage where a reader can take part now, when no error holds the view's red; never on Prussian"),
        ("2", "Series route", "Which recurring series a piece belongs to", "24 px", "Its pillar's corner, where every route ends"),
        ("3", "Pillar corner", "Which pillar a piece serves, when it belongs to no series", "24 px", "Nothing else"),
        ("None", "Content type", "Retired from the grid. Name it in words in the kicker, such as Explainer or Tracker", "None", "Not a code"),
    ]
    tr = "".join(f'<tr><td class="oai-num" data-k="Order">{E(a)}</td><th scope="row">{E(b)}</th><td data-k="What it tells a reader">{E(c)}</td>'
                 f'<td data-k="Smallest size">{E(d)}</td><td data-k="May share a grid with">{E(e)}</td></tr>' for a, b, c, d, e in rows)
    table = ('<table class="stack"><caption class="oai-note" style="text-align:left;caption-side:top;padding-bottom:8px">When a piece could carry more than one code, its grid shows the first that applies.</caption>'
             '<thead><tr><th scope="col">Order</th><th scope="col">Code</th><th scope="col">What it tells a reader</th><th scope="col">Smallest size</th><th scope="col">May share a grid with</th></tr></thead>'
             f'<tbody>{tr}</tbody></table>')
    body = f'<div class="oai-panel oai-s-newsprint">{table}</div>'
    alt = "The Signal Grid's codes in order of precedence, with what each tells a reader, its smallest size and what it may share a grid with."
    return rec("s-08-combinations", "08.4", None, alt, body, readable=True,
               notes="readable: the table reaches assistive technology (AX-S9). Stacks under 568 px with each cell's column named.")


# ------------------------------------------------------------------------------------------- 08.5
BILLS = [("Bill H.4212", "Public meeting notice", progress(3, now=True, step=3), ". Testimony is open until March 3"),
         ("Bill S.0876", "School bus contracts", progress(4), ""),
         ("Bill H.1180", "Library hours", progress(6), ""),
         ("Bill H.3301", "Records request fees", progress(4, gap=3), "")]


def _tracker(width, pad):
    rows = "".join(_row(b, t, n, extra=x) for b, t, n, x in BILLS)
    return (f'<div class="oai-s-newsprint" style="width:{width}px;padding:16px {pad}px;border:1px solid {hair("newsprint")}">'
            f'{head_label()}<p style="{ty("h3")}">Where four state bills stand this week</p>{rows}'
            f'<div style="margin-top:14px">{legend()}</div>'
            f'<p class="oai-tag" style="margin:10px 0 6px">Nine stages, read left to right and top to bottom:</p>{glossary()}</div>')


@spec
def s_08_5_correct():
    body = (f'<div class="oai-stack" style="gap:28px">'
            f'<div class="oai-cell">{_tracker(PHONE, 20)}<span class="oai-tag">On a phone, 358 px</span></div>'
            f'<div class="oai-cell">{_tracker(600, 24)}<span class="oai-tag">On a wider page, 600 px</span></div></div>')
    alt = ("A tracker list at true size, Where four state bills stand this week, shown first at a phone's 358 pixels and "
           "then at 600, with a 40 pixel grid and a key per bill: Bill H.4212, Public meeting notice, stage 3 of 9, Hearing, "
           "under way, its third node red because testimony is open until March 3; Bill S.0876, stage 4, Out of committee; "
           "Bill H.1180, stage 6, Passed both chambers; and Bill H.3301, stage 4, Out of committee, with a gap where its "
           "hearing should be because no hearing was held. A legend names each shape, and a list says what each of the nine "
           "stages means. Illustrative.")
    return rec("s-08-5-correct", "08.5", 600, alt, body, illustrative=True, css=LEGEND_CSS,
               notes="Phone column first, so a phone reader sees the whole list with its step without scrolling sideways (CP-S19). "
                     "Bill numbers are V5's invented examples (Q-01) on neutral topics. One working red in each view: the open testimony.")


@spec
def s_08_5_failure():
    def v5(lever, h):
        st = f"color:{ink('newsprint')};--link:{pal('stone')};--lever:{lever}"
        return svg_file(ID_DIR / LOCK["display"], h=h, decorative=True, style=st)
    cells = []
    for gray in (False, True):
        f = ' style="filter:grayscale(1)"' if gray else ""
        cells.append(f'<div class="oai-row"{f}>'
                     f'<div class="oai-cell"><span class="oai-red" data-red="signature" data-failure="true">{v5(pal("verdigris"), 28)}</span><span class="oai-tag">Active: lever in Verdigris, 28 px</span></div>'
                     f'<div class="oai-cell"><span class="oai-red" data-red="signature" data-failure="true">{v5(tv("color-palette-pillar-red"), 28)}</span><span class="oai-tag">Ready: lever in red, 28 px</span></div>'
                     f'<div class="oai-cell"><span class="oai-red" data-red="signature" data-failure="true">{v5(pal("verdigris"), 112)}</span><span class="oai-tag">Active, enlarged four times</span></div>'
                     f'<div class="oai-cell"><span class="oai-red" data-red="signature" data-failure="true">{v5(tv("color-palette-pillar-red"), 112)}</span><span class="oai-tag">Ready, enlarged four times</span></div></div>')
    body = (f'<div class="oai-panel oai-s-newsprint">'
            f'<div class="oai-stack"><p class="oai-tag">In color</p>{cells[0]}<p class="oai-tag">In grayscale</p>{cells[1]}</div></div>')
    alt = ("Failure case: our fifth edition's Active and Ready states at 28 pixels, the same grid with the lever in Verdigris "
           "or in red. In grayscale the two are the same picture; the colors differ at 1.14 to 1.")
    return rec("s-08-5-failure", "08.5", 700, alt, body,
               notes="V5's lockmark master at 28 px, V5's tracker size, with its lever hook set to Verdigris or red, as V5 described the two states.")


@spec
def s_08_stages():
    names = "".join(f'<li><span class="oai-num" style="font-weight:700">{i}</span> {E(s)}<span class="oai-gl-d">{E(GLOSS[i - 1])}</span></li>'
                    for i, s in enumerate(STAGES, 1))
    ex = [("Under way at stage 3", progress(3, now=True)), ("Stage 3 never happened; now at stage 5", progress(5, gap=3)),
          ("Taking part is open at stage 3", progress(3, now=True, step=3)), ("In effect", progress(9, final=True))]
    cells = "".join(f'<div class="oai-cell">{sgrid(80, nodes=n, label=t)}<span style="{ty("caption")};max-width:150px">{E(t)}</span></div>' for t, n in ex)
    a, sb = ink("newsprint"), g_sub("newsprint")
    C = (6, 26, 46)
    links = "".join(f'<line x1="{C[0]}" x2="{C[2]}" y1="{c}" y2="{c}"/><line y1="{C[0]}" y2="{C[2]}" x1="{c}" x2="{c}"/>' for c in C)
    nums = "".join(f'<circle cx="{C[i % 3]}" cy="{C[i // 3]}" r="5.5" fill="{ground("newsprint")}" stroke="{a}" stroke-width="0.6"/>'
                   f'<text x="{C[i % 3]}" y="{C[i // 3] + 2.15}" text-anchor="middle" font-size="6" font-family="Inter, Arial, sans-serif" font-weight="700" fill="{a}">{i + 1}</text>' for i in range(9))
    order = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" width="208" height="208" class="oai-svg" role="img" '
             f'aria-label="The nine stages in reading order, numbered 1 to 9, left to right and top to bottom">'
             f'<g stroke="{sb}" stroke-width="0.5">{links}</g>{nums}</svg>')
    css = (LEGEND_CSS + ".oai-st{display:flex;flex-wrap:wrap;gap:32px 40px;align-items:flex-start}"
           ".oai-st ol{margin:0;padding:0;list-style:none;font-size:15px;line-height:1.4;max-width:34ch}"
           ".oai-st li{padding:5px 0;border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}"
           ".oai-gl-d{display:block;font-size:14px;color:var(--oa-color-text-secondary-on-newsprint)}")
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-st">'
            f'<div class="oai-cell">{order}<ol>{names}</ol></div>'
            f'<div class="oai-stack" style="flex:1 1 320px"><div class="oai-row top">{cells}</div>{legend()}'
            '<p class="oai-note">The grids are the 40 px drawing at twice size. These nine stages follow a state bill; chapter 15 sets the stages for other routes, such as a ballot measure or an agency rule.</p></div>'
            '</div></div>')
    alt = ("The nine stages of a state bill in reading order, numbered on the grid, each with what it means: 1 Filed, a "
           "legislator introduced the bill; 2 Sent to committee; 3 Hearing, the committee heard from the public; 4 Out of "
           "committee, the committee voted to send it to the full chamber, the House or the Senate; 5 Passed one chamber; "
           "6 Passed both chambers; 7 Final text agreed, both chambers agreed on one text; 8 Signed by the governor; 9 In "
           "effect. Four grids at 80 pixels show a stage under way as a ring, a stage that never happened as a gap with its "
           "links cut, a red node where taking part is open, and all nine filled for a law in effect, with a legend of the shapes.")
    return rec("s-08-stages", "08.5", None, alt, body, css=css, readable=True,
               notes="readable: the stage list and its meanings reach assistive technology (CP-M9, AX-S2). The numbered order grid "
                     "is a diagram at 208 px with 24 px numbers; the four grids are the 40 px drawing at twice size. A sheet that flows.")


# ------------------------------------------------------------------------------------------- 08.6
@spec
def s_08_6_correct():
    cells = "".join(
        f'<div class="oai-cell" style="width:132px">{sgrid(40, route=r, decorative=True)}'
        f'<div style="display:flex;gap:10px;align-items:center">{sgrid(24, route=r, decorative=True)}<span style="{ty("ui")}">{E(n)}</span></div>'
        f'<span class="oai-tag">{E(p)} · {" to ".join(NAMES[x] for x in r)}</span></div>'
        for n, p, r in SERIES)
    body = f'<div class="oai-panel oai-s-newsprint"><div class="oai-row top" style="gap:24px">{cells}</div></div>'
    alt = ("Six series and their six routes at 40 and 24 pixels, each route a heavy line along the grid's links that ends on "
           "its pillar's corner: Reform 101 and The Oath end top left for Explain, Dispatch and The Public Record top right for "
           "Track, Field Notes bottom left for Connect, and Proof It Works bottom right for Act.")
    return rec("s-08-6-correct", "08.6", None, alt, body,
               notes="A sheet that flows. Routes from V5's table; Dispatch from the Front is renamed Dispatch (S2).")


@spec
def s_08_6_failure():
    e = g_ess("newsprint")
    g = sgrid(40, nodes=["off"] * 9, decorative=True)
    diag = (f'<line x1="19.5" y1="19.5" x2="35.5" y2="3.5" stroke="{e}" stroke-width="3" stroke-linecap="butt"/>'
            f'<circle cx="19.5" cy="19.5" r="2.5" fill="{e}"/><circle cx="35.5" cy="3.5" r="3.5" fill="{e}"/>'
            f'<rect x="3.5" y="18" width="16" height="3" fill="{e}"/><circle cx="3.5" cy="19.5" r="2.5" fill="{e}"/>')
    g = g.replace("</svg>", diag + "</svg>")
    body = (f'<div class="oai-panel oai-s-newsprint"><div class="oai-row mid">{g}'
            f'<span style="{ty("ui")}">A seventh series</span></div></div>')
    alt = "Failure case: a route for a new series that runs from the middle left to the center, then cuts diagonally to the top-right corner, across a link the grid does not have."
    return rec("s-08-6-failure", "08.6", 360, alt, body)


# ------------------------------------------------------------------------------------------- 08.7
@spec
def s_08_7_correct():
    cells = "".join(f'<div class="oai-cell" style="flex-direction:row;align-items:center;gap:10px">{sgrid(24, nodes=corner(p), decorative=True)}<span style="{ty("ui")}">{E(p)}</span></div>'
                    for p in ("Explain", "Track", "Connect", "Act"))
    body = f'<div class="oai-panel oai-s-newsprint"><div class="oai-row mid" style="gap:32px">{cells}</div></div>'
    alt = "Four pillar corners at 24 pixels, each beside its pillar's name: Explain lights the top-left node, Track the top right, Connect the bottom left and Act the bottom right."
    return rec("s-08-7-correct", "08.7", None, alt, body, notes="A sheet that flows.")


@spec
def s_08_7_failure():
    def g(size=16):
        n = "".join(f'<circle cx="{x}" cy="{y}" r="1.5" fill="{pal("verdigris") if (x, y) == (12.5, 2.5) else pal("charcoal")}"/>' for y in (2.5, 7.5, 12.5) for x in (2.5, 7.5, 12.5))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="{size}" height="{size}" aria-hidden="true" class="oai-svg">'
                f'<g fill="{pal("stone")}"><rect x="2.5" y="2" width="10" height="1"/><rect x="2.5" y="7" width="10" height="1"/><rect x="2.5" y="12" width="10" height="1"/>'
                f'<rect x="2" y="2.5" width="1" height="10"/><rect x="7" y="2.5" width="1" height="10"/><rect x="12" y="2.5" width="1" height="10"/></g>{n}</svg>')
    body = (f'<div class="oai-panel oai-s-newsprint">'
            f'<div class="oai-row"><div class="oai-cell">{g()}<span class="oai-tag">In color, 16 px</span></div>'
            f'<div class="oai-cell"><span style="filter:grayscale(1)">{g()}</span><span class="oai-tag">In grayscale, 16 px</span></div>'
            f'<div class="oai-cell">{g(64)}<span class="oai-tag">In color, enlarged four times</span></div>'
            f'<div class="oai-cell"><span style="filter:grayscale(1)">{g(64)}</span><span class="oai-tag">In grayscale, enlarged four times</span></div></div></div>')
    alt = "Failure case: a 16 pixel grid where every node is the same size and the top-right node is Verdigris to mean Track. In grayscale no node stands out."
    return rec("s-08-7-failure", "08.7", 300, alt, body)


# ------------------------------------------------------------------------------------------- 08.8
def kicker(surface="newsprint"):
    chip = (f'<span style="display:inline-flex;border:1px solid {ink(surface)};{ty("label")};text-transform:none;letter-spacing:0;line-height:1">'
            f'<span style="background:{ink(surface)};color:{ground(surface)};padding:5px 6px">Bill</span>'
            f'<span style="padding:5px 6px">H.4212</span></span>')
    return (f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">{sgrid(24, route=SERIES[2][2], decorative=True)}'
            f'{icon("CL-005", size=24, decorative=True)}'
            f'<span class="oai-label">Report · Dispatch</span>{chip}</div>')


@spec
def s_08_8_correct():
    art = (f'<div class="oai-s-newsprint" style="width:600px;padding:24px 28px;border:1px solid {hair("newsprint")}">'
           f'{head_label()}{kicker()}'
           f'<p style="{ty("h3")};margin-top:14px">The House takes up the meeting notice bill on Thursday</p>'
           f'<p style="margin-top:10px;{ty("body-small")};color:{ink2("newsprint")}">By the Oath &amp; Action desk</p></div>')
    body = f'<div>{art}</div>'
    alt = ("The top of a story card at true size. Its kicker runs left to right: a 24 pixel Signal Grid lighting the Dispatch "
           "route, a 24 pixel Civic Line icon for a public meeting, the words Report · Dispatch, and a chip reading Bill "
           "H.4212. Below sits the headline The House takes up the meeting notice bill on Thursday. Illustrative.")
    return rec("s-08-8-correct", "08.8", 600, alt, body, illustrative=True,
               notes="Kicker per Rule 01.21 and D2-250: the content label, then the series. Civic Line CL-005 Public Meeting, black "
                     "edition, placed by reference at 24 px (one color in a row, G1-07). H3 at 26 px on a 600 px card (D2-254).")


@spec
def s_08_8_failure():
    st = pal("stone")
    grid16 = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 123.5 123.5" width="16" height="16">'
              f'<g stroke="{st}" stroke-width="1" vector-effect="non-scaling-stroke"><path d="M11.75 11.75H111.75M11.75 61.75H111.75M11.75 111.75H111.75M11.75 11.75V111.75M61.75 11.75V111.75M111.75 11.75V111.75" vector-effect="non-scaling-stroke"/></g>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="3.8" fill="{pal("verdigris")}"/>' for x, y in ((11.75, 61.75), (61.75, 61.75), (111.75, 61.75), (111.75, 11.75)))
              + '</svg>')
    raw = (f'<div style="padding:24px 28px;width:600px"><div style="display:flex;align-items:center;gap:10px">{grid16}'
           '<span style="font:700 11px/1 Inter;letter-spacing:.12em;text-transform:uppercase">Public meetings</span><span style="font-size:11px;color:var(--oa-color-text-secondary-on-newsprint)">/</span>'
           '<b style="font:700 11px/1 Inter;letter-spacing:.12em;text-transform:uppercase">Dispatch</b><span style="font-size:11px">H.4212</span></div>'
           '<p style="font:800 26px/1.08 Inter Tight;letter-spacing:-.035em;margin:14px 0 0">The House takes up the meeting notice bill on Thursday</p></div>')
    src = raster_png(raw, 664, 140, "kicker-v5")
    body = (f'<div class="oai-panel oai-s-newsprint" style="padding:0"><img src="{src}" width="664" height="140" alt="" style="display:block;max-width:none"></div>'
            f'<p style="margin-top:8px">{illus()}</p>')
    alt = ("Failure case: our fifth edition's kicker, with a 16 pixel grid whose nodes turn to specks and labels set at 11 "
           "pixels in tracked capitals, under the 13 pixel floor. Illustrative.")
    return rec("s-08-8-failure", "08.8", 680, alt, body, illustrative=True,
               notes="Rendered to a PNG at twice size and embedded, so the page's own 13 px check stays clean while the failure shows at true size (D1-09).")


# ------------------------------------------------------------------------------------------- 08.9
STATES = [("Empty", None, "Nothing filed yet"), ("Loading", "loading", "Loading tracker"), ("Ready", progress(2), "Stage 2 of 9: Sent to committee"),
          ("Under way", progress(3, now=True), "Stage 3 of 9: Hearing, under way"), ("Final", progress(9, final=True), "Stage 9 of 9: In effect")]


def _state(nodes, surface):
    if nodes == "loading":
        return sgrid(40, nodes=["none"] * 9, surface=surface, decorative=True)
    return sgrid(40, nodes=nodes or ["off"] * 9, surface=surface, decorative=True)


@spec
def s_08_9_correct():
    def row(surface, name):
        cells = "".join(f'<div class="oai-cell" style="width:116px">{_state(n, surface)}<span style="{ty("ui")}">{E(t)}</span>'
                        f'<span style="{ty("caption")};color:{ink2(surface)}">{E(w)}</span></div>' for t, n, w in STATES)
        return f'<div class="oai-panel oai-s-{surface}"><div class="oai-row top" style="gap:16px">{cells}</div><p class="oai-tag" style="margin-top:12px">{E(name)}</p></div>'
    body = f'<div class="oai-stack" style="gap:12px">{row("newsprint", "Newsprint")}{row("charcoal", "Charcoal")}{row("prussian", "Prussian")}</div>'
    alt = ("Five tracker states at 40 pixels on Newsprint, Charcoal and Prussian, each with its words: Empty, small nodes only, "
           "Nothing filed yet; Loading, the links with no nodes, Loading tracker; Ready, two filled nodes, Stage 2 of 9: Sent to "
           "committee; Under way, two filled and a ring on the third, Stage 3 of 9: Hearing, under way; Final, all nine filled, "
           "In effect.")
    return rec("s-08-9-correct", "08.9", None, alt, body,
               notes="A sheet that flows. Loading draws the links alone, so it differs in shape from Empty, which draws the nodes small. In a page, the words sit in a role=\"status\" region.")


@spec
def s_08_9_failure():
    def frame(op, h=28):
        g = mark(LOCK["display"], h=h, decorative=True)
        return f'<span class="oai-red" data-red="signature" data-failure="true" style="--o:{op}">{g}</span>'
    css = ".oai-pulse [fill^=\"var(--lever\"]{opacity:var(--o)}"
    body = (f'<div class="oai-panel oai-s-newsprint">'
            f'<div class="oai-row oai-pulse"><div class="oai-cell">{frame(0.2)}<span class="oai-tag">Frame at 20 percent, 1.27 to 1</span></div>'
            f'<div class="oai-cell">{frame(0.5)}<span class="oai-tag">Frame at 50 percent, 1.83 to 1</span></div>'
            f'<div class="oai-cell">{frame(0.2, 112)}<span class="oai-tag">20 percent, enlarged four times</span></div>'
            f'<div class="oai-cell">{frame(0.5, 112)}<span class="oai-tag">50 percent, enlarged four times</span></div></div></div>')
    alt = ("Failure case: two frames of our fifth edition's loading state, the lockmark's red lever faded to 20 and then 50 "
           "percent. It pulsed forever with no text, and neither frame reaches 3 to 1.")
    return rec("s-08-9-failure", "08.9", 700, alt, body, css=css,
               notes="V5's lockmark master at 28 px with its lever at V5's two opacities.")


# ------------------------------------------------------------------------------------------- composer
@spec
def s_08_composer():
    lock80 = lockmark(80, decorative=True)
    lock40 = lockmark(40, decorative=True)
    stage_opts = "".join(f'<option value="{i}">{i}, {E(s)}</option>' for i, s in enumerate(STAGES, 1))
    series_opts = "".join(f'<option value="{i}">{E(n)}</option>' for i, (n, p, r) in enumerate(SERIES))
    pillar_opts = "".join(f'<option value="{p}">{p}</option>' for p in ("Explain", "Track", "Connect", "Act"))
    data = {"stages": STAGES, "series": [[n, p, r] for n, p, r in SERIES], "corner": PILLAR_CORNER, "pos": POS, "names": NAMES,
            "ink": g_ess("newsprint"), "sub": g_sub("newsprint"), "red": tv("color-palette-pillar-red"), "keyline": tv("color-border-strong-on-newsprint")}
    css = """
.oai-compwrap{container-type:inline-size}
.oai-comp{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px}
@container (max-width:560px){.oai-comp{grid-template-columns:1fr}}
.oai-comp fieldset{border:0;padding:0;margin:0 0 16px}
.oai-comp legend{font-weight:700;font-size:15px;margin-bottom:6px;padding:0}
.oai-comp label{display:flex;gap:8px;align-items:center;font-size:15px;min-height:32px}
.oai-comp select{font:15px/1.3 var(--oa-font-family-reading);padding:6px 8px;min-height:36px;border:1px solid var(--oa-color-border-strong-on-newsprint);background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white);max-width:100%}
.oai-comp input[type=checkbox],.oai-comp input[type=radio]{width:20px;height:20px;accent-color:var(--oa-color-palette-charcoal)}
.oai-comp :focus-visible{outline:2px solid var(--oa-color-focus-ring-on-newsprint);outline-offset:2px}
.oai-comp .why{font-size:14px;color:var(--oa-color-text-secondary-on-newsprint);margin:0 0 4px 28px}
.oai-comp button{font:600 15px/1 var(--oa-font-family-reading);padding:12px 18px;min-height:44px;background:transparent;color:var(--oa-color-text-primary-on-newsprint);border:1px solid var(--oa-color-border-strong-on-newsprint);cursor:pointer}
.oai-comp .out{display:flex;gap:24px;align-items:flex-end}
.oai-comp .status{margin-top:16px;padding:12px 14px;border-left:4px solid var(--oa-color-border-strong-on-newsprint);background:var(--oa-color-surface-white);font-size:17px;min-height:52px}
"""
    controls = (
        '<fieldset><legend>Code</legend>'
        '<label><input type="radio" name="oai-c-code" value="none" checked> Nothing: the lockmark</label>'
        '<label><input type="radio" name="oai-c-code" value="progress"> Tracker progress</label>'
        '<label><input type="radio" name="oai-c-code" value="series"> Series route</label>'
        '<label><input type="radio" name="oai-c-code" value="pillar"> Pillar corner</label></fieldset>'
        '<fieldset data-g="progress" hidden><legend>Progress</legend>'
        f'<label>Stage <select data-c="stage">{stage_opts}</select></label>'
        '<label><input type="checkbox" data-c="now"> The stage is under way</label>'
        '<label>A stage that never happened <select data-c="gap"><option value="0">None</option></select></label>'
        '<label><input type="checkbox" data-c="step" aria-describedby="oai-c-stepwhy"> Readers can take part at this stage now</label>'
        '<p class="why" data-c="stepwhy" id="oai-c-stepwhy">Mark the stage as under way first. A reader can take part only in a stage that is happening.</p></fieldset>'
        f'<fieldset data-g="series" hidden><legend>Series</legend><label>Series <select data-c="series">{series_opts}</select></label></fieldset>'
        f'<fieldset data-g="pillar" hidden><legend>Pillar</legend><label>Pillar <select data-c="pillar">{pillar_opts}</select></label></fieldset>'
        '<button type="button" data-c="reset">Reset</button>')
    out = (f'<div class="out"><div data-c="g80">{lock80}</div><div data-c="g40">{lock40}</div></div>'
           '<p class="oai-tag" style="margin-top:8px">80 px and 40 px</p>'
           '<p class="status" role="status" aria-live="polite" data-c="status">The lockmark. It codes nothing.</p>')
    script = """<script>(function(){
var root=document.currentScript.closest('[data-oai="s-08-composer"]');if(!root)return;
var D=JSON.parse(root.querySelector('script[type="application/json"]').textContent);
function q(s){return root.querySelector(s)}function c(n){return root.querySelector('[data-c="'+n+'"]')}
var L80=c('g80').innerHTML,L40=c('g40').innerHTML,C=[3.5,19.5,35.5];
function seg(a,b,col,t,gaps){var ax=a[0],ay=a[1],bx=b[0],by=b[1],x1=C[ax],y1=C[ay],x2=C[bx],y2=C[by],ia=ay*3+ax,ib=by*3+bx;
 var ca=gaps.indexOf(ia)>=0?5:0,cb=gaps.indexOf(ib)>=0?5:0;
 if(y1===y2){var xs=Math.min(x1,x2)+(x1<x2?ca:cb),xe=Math.max(x1,x2)-(x1<x2?cb:ca);return xe>xs?'<rect x="'+xs+'" y="'+(y1-t/2)+'" width="'+(xe-xs)+'" height="'+t+'" fill="'+col+'"/>':''}
 var ys=Math.min(y1,y2)+(y1<y2?ca:cb),ye=Math.max(y1,y2)-(y1<y2?cb:ca);return ye>ys?'<rect x="'+(x1-t/2)+'" y="'+ys+'" width="'+t+'" height="'+(ye-ys)+'" fill="'+col+'"/>':''}
function grid(nodes,route,size){var p=[],gaps=[];nodes=nodes.slice();nodes.forEach(function(n,i){if(n==='gap')gaps.push(i)});
 for(var r=0;r<3;r++)for(var k=0;k<2;k++){p.push(seg([k,r],[k+1,r],D.sub,1,gaps));p.push(seg([r,k],[r,k+1],D.sub,1,gaps))}
 if(route){for(var i=0;i<route.length-1;i++)p.push(seg(D.pos[route[i]],D.pos[route[i+1]],D.ink,3,[]));
  route.forEach(function(q,i){var pp=D.pos[q];nodes[pp[1]*3+pp[0]]=i===route.length-1?'lit':'route'})}
 nodes.forEach(function(n,i){var x=C[i%3],y=C[Math.floor(i/3)];
  if(n==='off')p.push('<circle cx="'+x+'" cy="'+y+'" r="1.5" fill="'+D.sub+'"/>');
  else if(n==='done'||n==='lit')p.push('<circle cx="'+x+'" cy="'+y+'" r="3.5" fill="'+D.ink+'"/>');
  else if(n==='route')p.push('<circle cx="'+x+'" cy="'+y+'" r="2.5" fill="'+D.ink+'"/>');
  else if(n==='now')p.push('<circle cx="'+x+'" cy="'+y+'" r="3" fill="none" stroke="'+D.ink+'" stroke-width="1"/>');
  else if(n==='step')p.push('<circle cx="'+x+'" cy="'+y+'" r="3" fill="'+D.red+'" stroke="'+D.keyline+'" stroke-width="1" data-red="working" data-red-job="the step a reader can take now"/>')});
 var s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="'+size+'" height="'+size+'" class="oai-svg" aria-hidden="true" focusable="false">'+p.join('')+'</svg>';
 return nodes.indexOf('step')>=0?'<span class="oai-red" data-red="working" data-red-job="the step a reader can take now">'+s+'</span>':s}
function codeVal(){return q('input[name="oai-c-code"]:checked').value}
function render(){var code=codeVal();
 root.querySelectorAll('fieldset[data-g]').forEach(function(f){f.hidden=f.getAttribute('data-g')!==code});
 var st=+c('stage').value,now=c('now').checked,gs=c('gap');
 var keep=+gs.value;gs.innerHTML='<option value="0">None</option>';for(var i=1;i<st;i++){var o=document.createElement('option');o.value=i;o.textContent=i+', '+D.stages[i-1];gs.appendChild(o)}
 gs.value=keep<st?keep:0;var gap=+gs.value;
 var step=c('step'),why=c('stepwhy');step.disabled=!now;why.hidden=now;if(!now){step.checked=false;step.setAttribute('aria-describedby',why.id)}else step.removeAttribute('aria-describedby');
 var nodes,route=null,msg;
 if(code==='none'){c('g80').innerHTML=L80;c('g40').innerHTML=L40;c('status').textContent='The lockmark. It codes nothing.';return}
 if(code==='progress'){nodes=[];for(var j=1;j<=9;j++)nodes.push(j<st?'done':(j===st?(now?'now':'done'):'off'));
  if(gap)nodes[gap-1]='gap';if(step.checked)nodes[st-1]='step';
  msg='Tracker progress: stage '+st+' of 9, '+D.stages[st-1]+(now?', under way':'')+'.';
  if(gap)msg+=' Stage '+gap+', '+D.stages[gap-1]+', never happened.';
  if(step.checked)msg+=' Readers can take part now, so this stage takes the view’s working red.'}
 else if(code==='series'){var s=D.series[+c('series').value];nodes=['off','off','off','off','off','off','off','off','off'];route=s[2];
  msg='Series route: '+s[0]+', a '+s[1]+' series. The route runs from '+route.map(function(r){return D.names[r]}).join(' to ')+' and ends on the '+s[1]+' corner.'}
 else{var pl=c('pillar').value,pp=D.pos[D.corner[pl]];nodes=['off','off','off','off','off','off','off','off','off'];nodes[pp[1]*3+pp[0]]='lit';
  msg='Pillar corner: '+pl+', the '+D.names[D.corner[pl]]+' node.'}
 c('g80').innerHTML=grid(nodes,route,80);c('g40').innerHTML=grid(nodes,route,40);c('status').textContent=msg}
root.addEventListener('change',render);
c('reset').addEventListener('click',function(){q('input[value="none"]').checked=true;c('stage').value='1';c('now').checked=false;c('gap').value='0';c('step').checked=false;c('series').value='0';c('pillar').value='Explain';render()});
render()})();</script>"""
    body = (f'<script type="application/json">{json.dumps(data)}</script>'
            f'<div class="oai-panel oai-s-newsprint oai-compwrap"><div class="oai-comp"><div>{controls}</div><div>{out}</div></div></div>{script}')
    alt = ("An interactive composer. Pick a code, nothing, tracker progress, a series route or a pillar corner, and its "
           "settings; the grid redraws at 80 and 40 pixels and a status line reads the grid in words, for example Tracker "
           "progress: stage 3 of 9, Hearing, under way.")
    return rec("s-08-composer", "08.9", None, alt, body, css=css, interactive=True,
               notes="Script scoped to its own root; the status line is a role=\"status\" region. The step option stays disabled, with its reason shown, until the stage is under way. Only valid combinations can be built. Fills its column (AX-S5); the disabled option is described by its reason (AX-S15).")
