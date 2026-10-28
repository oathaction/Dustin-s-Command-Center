"""The review board for Direction B, Snowball and Thermostat. Called by maps_r2_b_build.py.

Each specimen page appears first as a page, captured at its true composition (1440 px, or 390 px on a phone), and
its spec follows. Check results are read from the verifier's and the rendered checker's JSON files.
"""
import html
import json
from pathlib import Path

import maps_draw as OD  # round one's drawing helpers, for the retired loop-kind arrow only
import maps_r2_b_draw as D
import maps_r2_b_geom as G
import maps_r2_b_pages as P

esc = html.escape
ROOT = Path(__file__).resolve().parents[4]
ASSETS = ROOT / "work/boards/phase-2/maps-r2/b"
REL = "phase-2/maps-r2/b/"
REVIEW = "work/handoffs/phase-2/20261028_CD-Review-Of-Map-Directions.md"
NOTES = "work/handoffs/phase-2/20261028_Map-Direction-B-Notes.md"


def svg_body(text):
    return text.split("?>", 1)[1].strip() if text.startswith("<?xml") else text


def load(name):
    p = ASSETS / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def img_size(name):
    p = ASSETS / name
    if not p.exists():
        return None
    from PIL import Image
    with Image.open(p) as im:
        return im.size


def pagecap(tag, title, alt, page_file):
    """A page as a page: the 1440 capture at 1:1, swapped for the 390 capture on a phone."""
    s14 = img_size(f"20261028_B-Page-{tag}-1440.png") or (1440, 2000)
    s39 = img_size(f"20261028_B-Page-{tag}-390.png") or (390, 2000)
    return f'''<figure class="pagecap" aria-labelledby="cap-{tag}">
<picture><source media="(max-width: 760px)" srcset="{REL}20261028_B-Page-{tag}-390.png" width="{s39[0]}" height="{s39[1]}">
<img src="{REL}20261028_B-Page-{tag}-1440.png" width="{s14[0]}" height="{s14[1]}" alt="{esc(alt)}"></picture>
<figcaption id="cap-{tag}"><div class="board-inner"><b>{esc(title)}</b>. Captured in Chromium at 1440 px; a phone shows the 390 px capture.
<a href="{REL}{page_file}">Open the page itself</a> to read it at any width.</div></figcaption></figure>'''


def poster_mock(w, phone=False):
    """Where the loop-kind glyph would sit on Direction C's poster: a line bullet at the first station. Prussian
    ground, Newsprint line, White names, no red. An illustration of placement only."""
    h = 200 if not phone else 230
    y = 112 if not phone else 128
    x0, x1 = (40, w - 40)
    out = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="{D.PRUSSIAN}"/>']
    # the line, with two stations of R8 and a ring line's bullet below for B4
    xs = [x0 + 150, x1 - 60] if not phone else [x0 + 112, x1 - 26]
    out.append(f'<path d="M{x0 + 112 if not phone else x0 + 82} {y} L{x1 - 20} {y}" stroke="{D.NEWS}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    for i, x in enumerate(xs):
        out.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{D.PRUSSIAN}" stroke="{D.NEWS}" stroke-width="4"/>')
    names = ["Housing scarcity", "Owner home equity"]
    for x, nm in zip(xs, names):
        out.append(D.T(x, y - 22, nm, 15, 600, D.WHITE, "middle"))
    # line bullet: chip cells inverted for Prussian, then the kind glyph in Newsprint
    bx, by = x0, y - 15
    out.append(f'<rect x="{bx}" y="{by}" width="40" height="30" fill="{D.NEWS}"/>')
    out.append(D.T(bx + 20, by + 20, "R8", 15, 700, D.PRUSSIAN, "middle"))
    g = svg_body(D.glyph24("R", ink=D.NEWS, size=30))
    g = g.replace("<svg ", f'<svg x="{bx + 46}" y="{by}" ', 1)
    out.append(g)
    out.append(D.T(x0, h - 22, "Illustration of placement only. Direction C draws the poster and routes its lines.", 13, 400, D.WHITE)
               if not phone else D.T(x0 - 24, h - 40, "Illustration of placement only.", 13, 400, D.WHITE)
               + D.T(x0 - 24, h - 20, "Direction C draws the poster.", 13, 400, D.WHITE))
    lab = ("Placement mock on Prussian: a line labeled R8 starts with a bullet holding the loop ID and the spiral mark, "
           "then runs through Housing scarcity and Owner home equity. Illustration only.")
    return D.svg_doc(w, h, "".join(out), lab, "b-poster-mock")


def bullet_pair():
    out = []
    for k, lid in (("R", "R8"), ("B", "B4")):
        g = svg_body(D.glyph24(k, ink=D.NEWS, size=48))
        out.append(f'<div class="bul"><span class="bchip">{lid}</span>{g}<span>{"Snowball line bullet" if k == "R" else "Thermostat line bullet"}</span></div>')
    return "".join(out)


def glyph_sheet(meas):
    surfaces = [("Newsprint", D.NEWS, D.INK), ("White", D.WHITE, D.INK), ("Charcoal", D.INK, D.NEWS), ("Prussian", D.PRUSSIAN, D.WHITE)]
    rows = []
    for name, bg, ink in surfaces:
        cells = []
        for k in ("R", "B"):
            for sz in (16, 24, 48, 96):
                cells.append(f'<span class="gcell">{svg_body(D.glyph24(k, ink=ink, size=sz))}</span>')
            cells.append('<span class="gsep" aria-hidden="true"></span>')
        rows.append(f'<div class="grow" style="background:{bg};color:{ink}"><span class="gname">{name}</span>{"".join(cells)}</div>')
    m = meas or {}
    def mrow(k):
        v = (m.get("marks") or {}).get(k)
        return f'<td>{v["crisp"]:.2f}</td><td>{v["ink_share"]:.2f}</td>' if v else "<td>not run</td><td>not run</td>"
    pairs = (m.get("pairs") or {})
    p16, p24 = pairs.get("spiral vs ring 16"), pairs.get("spiral vs ring 24")
    tbl = (f'<div class="tscroll" tabindex="0" role="region" aria-label="Kind mark measures"><table><thead><tr><th scope="col">Mark</th><th scope="col">Crisp share (D1-17 needs 0.60)</th><th scope="col">Ink share</th></tr></thead><tbody>'
           f'<tr><th scope="row">Spiral, 24 px</th>{mrow("Snowball 24")}</tr><tr><th scope="row">Ring, 24 px</th>{mrow("Thermostat 24")}</tr>'
           f'<tr><th scope="row">Spiral, 16 px</th>{mrow("Snowball 16")}</tr><tr><th scope="row">Ring, 16 px</th>{mrow("Thermostat 16")}</tr></tbody></table></div>'
           f'<p>Similarity of spiral and ring (D1-16, distinct under 0.60): {p24["score"] if p24 else "not run"} at 24 px, '
           f'{p16["score"] if p16 else "not run"} at 16 px.</p>')
    old = (f'<svg width="26" height="26" viewBox="0 0 26 26" role="img" aria-label="Round one loop-kind arrow, retired">'
           f'{OD.STYLE}{OD.kind_mark(13, 13, "R", r=9.5)}</svg>')
    return "".join(rows), tbl, old


RED_RULE = ("The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands "
            "inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with "
            "the wordmark and never stands in for the hinge divider. An icon's red accent counts as signature red when the icon stands "
            "alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one "
            "keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: "
            "an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is "
            "where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the "
            "view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on "
            "Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never "
            "sits on Prussian.")

CSS = """
.board-inner{max-width:1280px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:16px}
.lede{font-size:1.125rem;max-width:68ch}
.verdict{background:var(--charcoal);color:var(--newsprint);padding:20px 22px;margin:24px 0 0}
.verdict h2{color:var(--newsprint);margin-bottom:8px}
.verdict p{max-width:78ch}
.verdict a{color:var(--newsprint)}
.open{display:flex;flex-wrap:wrap;gap:8px 18px;padding:0;margin:14px 0 0;list-style:none}
.open a{color:inherit;font-weight:600}
.pagecap{margin:28px 0 0;padding:0}
.pagecap img{display:block;width:100%;height:auto;max-width:1440px;margin:0 auto}
.pagecap figcaption{background:var(--surface);border-bottom:1px solid var(--rule);padding:12px 0;font-size:.9375rem}
.chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 var(--body);vertical-align:middle;margin-right:6px}
.chip .k{background:var(--charcoal);color:var(--newsprint);padding:7px 7px 0;letter-spacing:.02em}
.chip .c{border:1.5px solid var(--charcoal);padding:5px 7px 0;font-size:14px;font-weight:700}
.spec{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:20px}
.spec h3{margin:0 0 6px}
.spec ul{margin:0;padding-left:18px}
.spec li{margin:0 0 4px}
.testrow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:12px 0}
.testrow figure,.tcard figure{margin:0;background:#fff;padding:14px}
.testrow svg{display:block;margin:0 auto}
.testrow figcaption,.tcard figcaption{font-size:.875rem;margin-top:8px}
.tcard{display:grid;grid-template-columns:1fr;gap:16px;margin:12px 0}
.tcard svg.desk{display:block;margin:0 auto}
.tcard svg.phone{display:none}
.judge{width:100%}
.judge td,.judge th{font-size:.9375rem}
.tag.fail{background:var(--charcoal);color:var(--newsprint)}
.gray{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:14px}
.gray figure{margin:0}
.gray img{display:block;width:100%;height:auto;border:1px solid var(--rule)}
.gray figcaption{font-size:.875rem;margin-top:6px}
.grow{display:flex;flex-wrap:wrap;align-items:flex-end;gap:14px;padding:14px 16px}
.gname{font:700 .8125rem/1.2 var(--body);letter-spacing:.06em;text-transform:uppercase;width:92px}
.gcell svg{display:block}
.gsep{width:18px}
.mock > svg{display:block;width:100%;height:auto;max-width:720px}
.mock > svg.phone{display:none}
.buls{display:flex;flex-wrap:wrap;gap:18px;background:var(--prussian);padding:16px;margin-top:12px}
.bul{display:flex;align-items:center;gap:10px;color:var(--white);font:600 15px/1.3 var(--body)}
.bul svg{display:block}
.bchip{background:var(--newsprint);color:var(--prussian);font:700 18px/1 var(--body);padding:10px 10px}
.rub td:first-child,.rub th:first-child{white-space:nowrap}
.tscroll{overflow-x:auto}
.decision ol{margin:0;padding-left:20px}
.decision li{margin:0 0 8px;max-width:90ch}
.redrule{font-size:.9375rem;max-width:90ch}
.quote{border-left:4px solid var(--charcoal);padding:4px 0 4px 14px;font-weight:600}
@media (max-width:760px){
.testrow{grid-template-columns:1fr}
.tcard{grid-template-columns:1fr}
.tcard figure{padding:0}
.tcard figcaption{padding:0 4px 10px}
.tcard svg.desk{display:none}.tcard svg.phone{display:block;margin:0 auto}
.gray{grid-template-columns:repeat(2,minmax(0,1fr))}
.mock > svg.desk{display:none}.mock > svg.phone{display:block}
.rub thead{display:none}
.rub tr{display:block;border-bottom:1px solid var(--rule);padding:8px 0}
.rub td,.rub th{display:block;border:0;padding:2px 0;white-space:normal}
.rub td:first-child,.rub th:first-child{white-space:normal}
.rub td[data-label]::before{content:attr(data-label) ": ";font-weight:700}
.gname{width:100%}
}
"""


def checks_html(ver, chk):
    v = (ver or {}).get("summary") or ["The verifier has not run on this build."]
    c = (chk or {}).get("summary") or ["The rendered check has not run on this build."]
    return ("<h3>Data check against Atlas V7 (maps_r2_b_verify.py)</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in v) + "</ul>"
            "<h3>Rendered checks (maps_r2_b_check.js, Chromium through Playwright)</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in c) + "</ul>")


RUBRIC = [
    ("Craft", 4, "True Archimedean geometry, read back point by point; labels placed by measured type and tested against the curve, the discs and each other (0 collisions, nearest label 15.6 px from a line); one stroke per view. Below 5: the 24 px marks miss the 60 percent crisp-pixel bar, and six-wide tiles set titles in four lines."),
    ("Clarity", 4, "Shape gives the kind before any word, and the first station's echo says the loop came back. Studio judgment only: the reader check needs Dustin's go. The phone figure shows IDs, with the strip under it naming each station."),
    ("Brand fidelity", 4, "Charcoal head, Newsprint wall, White tiles and cards, locked faces, the V5 wordmark master, and red only at the named reform's targets on White. Cover the wordmark and the surfaces and type still read as Oath & Action; the spiral is a new device Dustin has not approved."),
    ("Usefulness", 4, "One constant k, one geometry per scale, a geometry data file with every station's angle and radius, and scripts that draw any V7 loop. A builder can draw a new loop from the spec."),
    ("Evidence honesty", 4, "The printed line on every catalog and card, direction in words only, valence unused, the weakest step named, ties stated as ties, undated routes shown as unchecked. Open risk: on six loops running down, an outward turn could still read as more."),
    ("Accessibility", 4, "No page scroll, nothing under 13 px, 0 axe violations at 1440 and 390 on all five pages and the board; grayscale proofs decode; every drawing has a text equivalent and the phone strip. Screen readers and zoom not tested."),
    ("Beauty and distinctiveness", 3, "The head and the three cards are the strongest images across both rounds: a red return sweeping out past its start is ownable and needs no key. The wall rows still read as small line drawings at 1x, so the catalog sits under the bar."),
]

DECISIONS = [
    "Spiral growth k is 1.8 for every reinforcing loop at every scale. The review's 1.3 puts the echo on top of the first station at the 26 px and 54 px disc sizes the review sets (OVERLAP px overlap at 150 px), and 1.8 is the smallest tenth that clears it by 5 px.",
    "Rings share the spiral's center and starting radius on every miniature, so every first station sits at the same point on the wall and a snowball visibly leaves the ring.",
    "Each miniature step keeps one small arrowhead at its arrival, so a reader can tell outward from inward; it is the only mark beyond the budget's shape, textures and IDs.",
    "When a reform targets the first variable, both the start disc and its echo take red: one job, two marks of the same variable (Rule 05.3).",
    "On cards the first station's name sits inside the turn, under its disc, because the echo sits outward of it.",
    "The phone card figure prints station IDs only, with a strip list under it naming every station and step in order; four-station loops leave no room for side labels at 358 px.",
    "The phone catalog keeps 150 px shapes in two columns. At the review's 120 px the shared k of 1.8 overlaps the echo by 3.1 px, and clearing it would take k 2.2, a second geometry for phones.",
    "Catalog rows fill by area: six loops sit six-wide, four sit four-wide, and the sketched plate takes a reading note as its fourth tile. Shapes stay 150 px in every tile, centered.",
    "The 240 px head emblems are drawn at a 5 px display stroke because they carry no data; every data drawing keeps one stroke per view (2.5 px).",
    "The loop-kind mark is proposed at 24 px only; at 16 px spiral and ring score 0.69 and are not distinct, so smaller sizes print the words.",
    "Card headlines are studio drafts for the editor, labeled in each card's foot.",
]


def board(model, dr, pages):
    LP = model["loops"]
    ver = load("20261028_B-Verify-Results.json")
    chk = load("20261028_B-Check-Results.json")
    meas = load("20261028_B-Kind-Mark-Measurements.json")
    t = dr["test"]
    geo = D.mini_geo()
    g13 = D.mini_geo(D.K_BRIEF)

    def tmini(lid, tag):
        return svg_body(t[(lid, tag, "mini")])
    test_rows = []
    for tag, kk, g in (("K13", D.K_BRIEF, g13), ("K18", D.K, geo)):
        cells = "".join(f'<figure>{tmini(lid, tag)}<figcaption>{P.chip("Loop", lid)} at k {kk}.</figcaption></figure>' for lid in ("R8", "R10", "B4"))
        test_rows.append(f'<h3>Miniature, 150 px, k {kk}{": the echo overlaps the first station by " + str(round(-g["clear"], 1)) + " px" if g["clear"] < 0 else ": the echo clears the first station by " + str(g["clear"]) + " px"}</h3>'
                         f'<div class="testrow">{cells}</div>')
    c13 = svg_body(t[("R8", "K13", "card")]).replace("<svg ", '<svg class="desk" ', 1)
    c18 = svg_body(t[("R8", "K18", "card")]).replace("<svg ", '<svg class="desk" ', 1)
    p13 = svg_body(t[("R8", "K13", "phone")]).replace("<svg ", '<svg class="phone" ', 1)
    p18 = svg_body(t[("R8", "K18", "phone")]).replace("<svg ", '<svg class="phone" ', 1)
    cg = D.card_geo()
    clear13 = round((D.K_BRIEF - 1) * cg["r"] - 2 * cg["disc"] - cg["stroke"], 1)
    clear18 = round((D.K - 1) * cg["r"] - 2 * cg["disc"] - cg["stroke"], 1)
    test_cards = (f'<h3>Card, r {cg["r"]:.0f} px with 54 px discs</h3><div class="tcard"><figure>{c13}{p13}<figcaption>R8 at k 1.3: the echo overlaps the first station by {-clear13} px at card size.</figcaption></figure>'
                  f'<figure>{c18}{p18}<figcaption>R8 at k 1.8: the echo clears by {clear18} px and the return sweeps out past its start.</figcaption></figure></div>')
    judge = f'''<div class="tscroll" tabindex="0" role="region" aria-label="Test judgment"><table class="judge rub"><thead><tr><th scope="col">Question</th><th scope="col">k 1.3, the review's start</th><th scope="col">k 1.8, chosen</th></tr></thead><tbody>
<tr><th scope="row">Can a reader see the echo?</th><td data-label="k 1.3"><span class="tag fail">Fails</span> The echo disc sits on the first station at 150 px, on the card and on the phone. The ID cannot be read.</td><td data-label="k 1.8">Yes. 5.5 px clear at 150 px, {clear18} px on the card.</td></tr>
<tr><th scope="row">Does it read as a drain?</th><td data-label="k 1.3">No. It reads as a ring with a smudge at the top.</td><td data-label="k 1.8">No. One turn, an empty center and arrowheads that run outward clockwise. A drain needs many turns closing on a point.</td></tr>
<tr><th scope="row">Does it read as a target?</th><td data-label="k 1.3">Partly: start and echo stack like two rings.</td><td data-label="k 1.8">No. Nothing sits in the center and no ring repeats.</td></tr>
<tr><th scope="row">Does it read as runaway growth?</th><td data-label="k 1.3">No.</td><td data-label="k 1.8">Some risk. One bounded turn reads as "comes back further out", which is the snowball. On the six loops running down, an outward turn could read as more; the card states the direction in words beside the shape.</td></tr>
<tr><th scope="row">Can a reader tell the kinds apart without a key?</th><td data-label="k 1.3">Barely. Spiral and ring look almost alike.</td><td data-label="k 1.8">Yes, in every row of the catalog. A thermostat closes and sits smaller, at the radius where every snowball starts.</td></tr>
</tbody></table></div>'''
    rows, tbl, old = glyph_sheet(meas)
    gray = "".join(f'<figure><a href="{REL}20261028_B-Page-{tag}-1440-Grayscale.png"><img src="{REL}20261028_B-Page-{tag}-1440-Grayscale.png" alt="Grayscale proof of the {esc(name)} at 1440 px"></a>'
                   f'<figcaption>{esc(name)}, 1440 px. <a href="{REL}20261028_B-Page-{tag}-390-Grayscale.png">390 px proof</a>.</figcaption></figure>'
                   for tag, name in (("Loop-Catalog", "Loop catalog"), ("Loop-Card-R8", "R8 card"), ("Loop-Card-R10", "R10 card"), ("Loop-Card-B4", "B4 card"), ("Reform-View-R-01", "R-01 reform view")))
    rub = "".join(f'<tr><th scope="row">{esc(n)}</th><td data-label="Score">{s}</td><td data-label="Reason">{esc(r)}</td></tr>' for n, s, r in RUBRIC)
    dec = "".join(f"<li>{esc(d.replace('OVERLAP', str(round(-g13['clear'], 1))))}</li>" for d in DECISIONS)
    mock_d = svg_body(poster_mock(720)).replace("<svg ", '<svg class="desk" ', 1)
    mock_p = svg_body(poster_mock(358, phone=True)).replace("<svg ", '<svg class="phone" ', 1)
    mg = D.mini_geo()
    cg_ = D.card_geo()
    pg_ = D.phone_geo()
    nR = sum(1 for lp in LP.values() if lp["type"] == "R")
    nB = len(LP) - nR
    body = f'''<div class="board-inner" style="padding-top:40px">
<p class="eyebrow">Phase 2 · Systems maps, round two · October 28, 2026</p>
<h1>Direction B: Snowball and Thermostat</h1>
<p class="lede">The shape tells the reader what a loop does before any word. A loop that feeds itself is one turn of an Archimedean spiral that comes back to its first variable one lap further out. A loop that pushes back is a ring that closes on its start. All {len(LP)} Atlas V7 loops are drawn by script from V7 and checked against it.</p>
<p class="quote">{esc(P.HONEST)}</p>
<div class="verdict"><h2>Test first: passed, with one change</h2>
<p>I drew R8, R10 and B4 at miniature and card size before the full set. At the review's growth of 1.3 the echo lands on top of the first station at every size the review sets, so the shape cannot be read. At 1.8 the echo clears, and in my judgment the spiral reads as one turn that comes back further out. It does not read as a drain or a target. Runaway growth is a small risk on loops running down, and the words beside each shape carry the direction. This is studio judgment. The five-person reader check needs Dustin's go and has not run. If two or more of five readers see a drain or runaway growth, the ring folds into Direction A.</p>
<ul class="open"><li><a href="{REL}{pages["catalog"].name}">Loop catalog</a></li><li><a href="{REL}{pages["R8"].name}">R8 card</a></li><li><a href="{REL}{pages["R10"].name}">R10 card</a></li><li><a href="{REL}{pages["B4"].name}">B4 card</a></li><li><a href="{REL}{pages["R-01"].name}">R-01 reform view</a></li><li>Notes: <code>{NOTES}</code></li></ul></div>
<p class="cap">Brief: <code>{REVIEW}</code>, section 4, Direction B. Direction B has no whole-system map of its own; it rides on Direction C's poster as a line bullet (section 9 below). Directions A and C are built in parallel by other makers.</p>

<section id="test"><h2>1. The test: R8, R10 and B4 before the full set</h2>
<p>Same three loops, same frame, two values of k. The geometry is one rule: radius r (1 + (k − 1) t / 360) at angle t, stations at equal angles clockwise from twelve o'clock, the echo at 360 degrees.</p>
{"".join(test_rows)}{test_cards}{judge}</section>
</div>

<section id="catalog" class="full"><div class="board-inner"><h2>2. The loop catalog, as a page</h2></div>
{pagecap("Loop-Catalog", "Loop catalog", "The loop catalog page: a Charcoal head with a 240 px spiral beside 18 feed themselves and a ring beside 5 push back, the printed line, a how-to-read strip, then five area plates of White tiles on Newsprint, each with a 150 px spiral or ring, chip, title, station list and facts line.", pages["catalog"].name)}
<div class="board-inner"><h3 style="margin-top:20px">Spec</h3><div class="spec">
<div class="panel"><h3>Head, Charcoal</h3><ul><li>Two emblems, 240 by 240 px, Newsprint on Charcoal, 5 px display stroke, 20 px discs.</li><li>Counts in Inter Tight 800 at 96 px, 56 px under 760 px; {nR} and {nB} counted from V7 types.</li><li>The printed line in a 2 px Newsprint frame. How-to-read strip: four steps and the M1 texture key with M2 words.</li></ul></div>
<div class="panel"><h3>Area plates, Newsprint</h3><ul><li>Band: letter in Inter Tight 800 at 96 px, name at 34 px, V7's region text, kind counts.</li><li>Rows fill: six-wide or four-wide by the area's count; 16 px gutters; two columns under 760 px.</li><li>Group rule: the area holding most of a loop's numbered variables.</li></ul></div>
<div class="panel"><h3>Tile, White</h3><ul><li>Loop chip (M3) and the kind in words; the 150 by {mg["h"]} px shape, centered; V7 title in Inter Tight 600 at 17 px.</li><li>Stations by ID and V7 chain label; facts line: direction, one turn in words, least certain step, closure.</li><li>No signs, ticks, pointers or red (notation budget).</li></ul></div>
<div class="panel"><h3>Miniature geometry</h3><ul><li>k {D.K}; r {mg["r"]} px; center ({mg["cx"]}, {mg["cy"]}) in a 150 by {mg["h"]} frame for every loop.</li><li>26 px Charcoal discs, IDs in Inter 700 at 13 px, Newsprint; the echo as a 2.5 px outlined disc with the same ID.</li><li>2.5 px stroke, M1 textures per segment; 9 by 4.5 px arrowheads; sketched steps in the hollow line, open stations 14 px.</li></ul></div>
</div></div></section>

<section id="r8" class="full"><div class="board-inner"><h2>3. The R8 card, as a page</h2></div>
{pagecap("Loop-Card-R8", "R8 loop card", "The R8 loop card page on White: kicker with the Loop R8 chip and spiral mark, headline Scarce housing builds the equity that keeps it scarce, V7 title, read-aloud sentence, the spiral with A5 at twelve, A6 at six and the A5 echo one turn later, the L39 return and A5 in red for R-30, a right rail with feeds itself, now running up, one turn, least certain step and revision, the steps table and the R-30 panel with effect pips and routes.", pages["R8"].name)}
<div class="board-inner"><h3 style="margin-top:20px">Spec</h3><div class="spec">
<div class="panel"><h3>Figure</h3><ul><li>k {D.K}, r {cg_["r"]:.0f} px, 54 px discs with IDs in Inter Tight 800 at 20 px, 2.5 px stroke, 11 by 5.5 px arrowheads, M4 ticks after each departure.</li><li>Station names in Inter 600 at 16 px with "Higher:" rules from V7's increase_means at 14 px; the first station's name inside the turn.</li><li>Step labels outside each segment: sign pill with the record square on documented steps, ID and reading, V7 name at 15 px, grade word and delay in words.</li></ul></div>
<div class="panel"><h3>Page</h3><ul><li>White; headline Inter Tight 800 at 44 px (30 px on a phone); V7 title; the read-aloud sentence in Lora Italic at 20 px.</li><li>Figure column and a 340 px rail: kind, Now with V7's series name, one turn, least certain step, revision.</li><li>No chart: the series waits for sourced values from the research lead.</li></ul></div>
<div class="panel"><h3>Red, Rule 05.3</h3><ul><li>R-30 is the one reform the card names: L39, the A5 disc and its echo in Pillar Red (4.17:1 on White; IDs at 20 px bold count as large text).</li><li>R-30's third target, LE17, sits outside the loop and is named in words.</li></ul></div>
<div class="panel"><h3>Phone, 390 px</h3><ul><li>Same k at r {pg_["r"]:.0f} px, 38 px discs, IDs at 19 px weight 800; step IDs with their sign pill.</li><li>A strip list under the figure names every station and step in order, then the return.</li></ul></div>
</div></div></section>

<section id="r10" class="full"><div class="board-inner"><h2>4. The R10 card, the stress test</h2><p>Four steps from documented to plausible. L53 is named as the least certain step on the drawing and in the rail; R-01's three targets take the red.</p></div>
{pagecap("Loop-Card-R10", "R10 loop card", "The R10 loop card: a four-station spiral from C1 Safe seats round C2, C3 and C4 back to C1 one turn later, with L08, L25 and C2 in red for R-01 and L53 dashed and labeled least certain step.", pages["R10"].name)}</section>

<section id="b4" class="full"><div class="board-inner"><h2>5. The B4 card, a thermostat</h2><p>The ring closes on D5. The rail reads in the order Reuters used for its famine work: how it should work, then what is happening now. R-07 is the reform the card names, at C3.</p></div>
{pagecap("Loop-Card-B4", "B4 loop card", "The B4 loop card: a ring from D5 Public service quality round C3 and C5 and back to D5, with C3 in red for R-07, and a rail reading pushes back, how it should work and what is happening now.", pages["B4"].name)}</section>

<section id="r01" class="full"><div class="board-inner"><h2>6. The R-01 reform view, on White</h2><p>R-01 lists three loops. All three of its targets sit on R10, so R10 carries the red; B4 and R11 appear as miniatures with the reason nothing on them is red.</p></div>
{pagecap("Reform-View-R-01", "R-01 reform view", "The R-01 reform view: the R10 spiral with L25, L08 and C2 in red, a rail listing the three targets, B4 and R11 as miniatures, then effect pips and routes with their check dates.", pages["R-01"].name)}</section>

<div class="board-inner">
<section id="gray"><h2>7. Grayscale proofs</h2><p>Each page with color removed. Pillar Red turns a mid-gray, a clear step lighter than the Charcoal lines, and every red target also carries words: "R-30 acts on this step" on the drawing and "Reform acts here" in the steps table. Textures carry every grade, and the shapes carry every kind.</p><div class="gray">{gray}</div></section>

<section id="mark"><h2>8. The spiral and the ring as a loop-kind mark, 24 px <span class="tag">Option, pending Dustin's approval</span></h2>
<p>The marks would replace round one's loop-kind arrow (shown at the end, retired). Each prints beside the words "feeds itself" or "pushes back". Shown at 16, 24, 48 and 96 px on the four surfaces.</p>
{rows}<p style="margin-top:12px">Round one's arrow mark, retired: {old}</p>{tbl}
<p>What these measures say: the pair is distinct at 24 px. At 16 px the spiral's opening closes and the two read alike, so the mark is proposed for 24 px and larger only. Neither mark reaches D1-17's 60 percent crisp share, a bar set for straight-edged icons; a round 2 px line reaches about half. A variant with its extremes snapped to whole pixels measured no crisper and less distinct, so I kept this drawing.</p></section>

<section id="poster"><h2>9. On Direction C's poster</h2>
<p>Direction B draws no whole-system map: a spiral cannot share a station with six other loops. The poster belongs to Direction C, built by another maker. B's contribution would be the line bullet: the loop ID and the kind mark at the first station of each line.</p>
<div class="mock">{mock_d}{mock_p}</div><div class="buls">{bullet_pair()}</div>
<p class="cap">Prussian ground, Newsprint line, White names, no red (Rule 05.3: red never sits on Prussian). The station names are R8's, used to show placement only.</p></section>

<section id="spec"><h2>10. Spec: geometry, honesty and the notation budget</h2><div class="spec">
<div class="panel"><h3>Geometry</h3><ul><li>Snowball: radius r (1 + (k − 1) t / 360), t from 0 to 360 degrees clockwise from twelve o'clock; k = {D.K} for every reinforcing loop at every scale.</li><li>Thermostat: a circle at r.</li><li>Stations at t = 360 i / n; the echo at 360. Curves as cubic Bézier pieces of 8 degrees or less with exact tangents.</li><li>Every station's angle and radius: <code>{REL}20261028_Direction-B-Geometry-Data.json</code>.</li></ul></div>
<div class="panel"><h3>Honesty rules</h3><ul><li>Shape comes from V7's loop type only. Delay, direction, grade and valence never set a shape, size or color; the verifier checks shape against type and color sets on every miniature.</li><li>The outward step means one more turn and never an amount. The printed line appears on the catalog and on both snowball cards.</li><li>V7's direction appears in words only: running up on 10 loops, running down on 6, and the cases V7 calls running, switched off, direction unknown or a design target.</li></ul></div>
<div class="panel"><h3>Notation budget, as built</h3><ul><li>Miniature: shape, M1 textures, hollow line, IDs, echo, one arrowhead per step. Kind, delay, direction and least certain step in words in the tile.</li><li>Card: plus sign pills with record squares, grade words with glosses in the steps table, M4 ticks, the weakest step named, red at the named reform's targets.</li><li>Catalog: no working red; the wordmark's ampersand is signature red.</li></ul></div>
<div class="panel"><h3>Red rule, word for word (D2-01)</h3><p class="redrule">{esc(RED_RULE)}</p></div>
</div></section>

<section id="checks"><h2>11. Checks</h2>{checks_html(ver, chk)}
<h3>Wall test and 2x test</h3><ul>
<li>Wall: I viewed the catalog whole at 42 percent. The four-wide rows set their shapes at the left of wide tiles and looked unfinished beside the six-wide rows; shapes are now centered in every tile. The sketched plate showed a stray dot where a letter would sit; it now has no letter column. The 240 px emblems looked thin beside 96 px type; they now take a 5 px display stroke.</li>
<li>2x: crops of R8, R10, B4, R15 and R9 tiles and of every card figure at device scale 2. Found and fixed: the how-to-read demo's "Start" label sat on the curve; the phone figure's first label slid past A6; Inter's tabular figures spread hyphens ("Owner - renter"), so tabular figures now apply to tables only; the phone strip used an anticlockwise arrow for a clockwise loop and now uses the drawn mark.</li>
<li>I could not pin the page beside the Vignelli diagram or a Tufte plate; the studio holds no rights to show them, and I judged against my memory of them.</li></ul></section>

<section id="rubric"><h2>12. Rubric</h2><p>Master Brief section 6, 1 to 5, ship threshold 4, with the review's seventh line.</p>
<div class="tscroll" tabindex="0" role="region" aria-label="Rubric"><table class="rub"><thead><tr><th scope="col">Criterion</th><th scope="col">Score</th><th scope="col">Reason</th></tr></thead><tbody>{rub}</tbody></table></div>
<p>Beauty sits under the threshold on the catalog wall. Instruction for the next pass: test 200 px shapes four to a row with a 3 px stroke, so the wall carries the shapes at poster weight, and keep every shape the same size so size never reads as strength.</p></section>

<section class="decision" id="decisions"><h2>Decisions made in this direction</h2><ol>{dec}</ol>
<p>For Dustin: approve or decline the spiral and ring as the loop-kind mark (section 8), and say whether to run the five-person reader check on R8 and R10.</p></section>
<p class="cap" style="margin-top:24px">Source for every drawn value: Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026, read through <code>work/build/scripts/phase-2/maps_model.py</code>. Scripts: <code>work/build/scripts/phase-2/maps_r2_b_*.py</code> and <code>maps_r2_b_check.js</code>.</p>
</div>'''
    head = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Map Direction B, Snowball and Thermostat</title>{P.FONTS}<link rel="stylesheet" href="board-base.css"><style>{CSS}</style></head><body>')
    return head + body + "</body></html>"
