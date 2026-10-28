"""Direction C, Loop Lines: the review board. Shows each page as a page first (captures of the real pages, linked),
then the spec, the tests, the checks, the rubric and the decisions. Reads the verify and check results when present."""
import html
import json

import maps_r2_c_cards as C
import maps_r2_c_draw as D
import maps_r2_c_geom as G
import maps_r2_c_pages as P
import maps_r2_c_views as V

esc = html.escape
M, LOOPS = G.M, G.LOOPS
ROOT, A = G.ROOT, G.ASSETS
BOARD = ROOT / "work/boards/20261028_Map-Direction-C-Loop-Lines.html"
REL = "phase-2/maps-r2/c/"
VERIFY = A / "20261028_Loop-Lines-Verify-Results.json"
CHECK = A / "20261028_Loop-Lines-Check-Results.json"

CSS = """
.board{max-width:1312px}
.lede{font-size:1.125rem;max-width:74ch}
.sumbox{background:var(--charcoal);color:var(--newsprint);padding:18px 20px;margin-top:20px}
.sumbox p{max-width:96ch;margin:0 0 8px}.sumbox b{color:var(--white)}
.toc{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:16px;font-size:.9375rem}
.toc a{color:var(--fg)}
figure{margin:16px 0 0}
figure img{display:block;max-width:100%;height:auto;border:1px solid var(--charcoal)}
figcaption{font-size:.875rem;color:var(--muted);margin-top:8px;max-width:96ch}
.pair{display:grid;grid-template-columns:minmax(0,1fr) 390px;gap:28px;align-items:start}
.pair .phone img{width:390px}
@media (max-width:1100px){.pair{grid-template-columns:1fr}}
.tall{max-height:1500px;overflow-y:auto;border:1px solid var(--charcoal)}
.tall img{border:0}
.tints{display:flex;flex-wrap:wrap;gap:16px}.tints figure{margin:0}
.phones{display:flex;flex-wrap:wrap;gap:24px}.phones figure{width:390px;max-width:100%;margin:0}.phones img{width:390px;max-width:100%}
.grays{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:16px}
.grays figure{margin:0}.grays img{width:100%;height:auto}
.spec{display:grid;grid-template-columns:minmax(150px,220px) 1fr;gap:8px 22px;margin:12px 0 0}
.spec dt{font-weight:700;font-size:.9375rem}.spec dd{margin:0;font-size:.9375rem;max-width:96ch}
@media (max-width:700px){.spec{grid-template-columns:1fr}.spec dd{margin-bottom:10px}}
.wrap{overflow-x:auto;max-width:100%}
.wrap:focus-visible,a:focus-visible{outline:3px solid var(--prussian);outline-offset:2px}
table.t td,table.t th{font-size:.875rem}
.rubric td:not(:last-child):not(:first-child){text-align:center;font-variant-numeric:tabular-nums;font-weight:700}
.chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 var(--body);vertical-align:middle}
.chip .k{background:var(--charcoal);color:var(--newsprint);padding:6px 7px 0;letter-spacing:.02em}
.chip .c{border:1.5px solid var(--charcoal);padding:5px 7px 0;font-size:14px;font-weight:700}
.tv td,.tv th{font-size:.875rem}
.note{background:var(--surface);border:1px solid var(--rule);padding:14px 16px;margin-top:14px}
ul.tight li{margin-bottom:6px;max-width:96ch}
.decision a{color:inherit}
.decision table th,.decision table td{border-bottom-color:#A3A19C}
.decision th{color:var(--newsprint)}
"""


def img(name, alt, w=None, h=None, cls=""):
    size = f' width="{w}" height="{h}"' if w else ""
    return f'<img src="{REL}20261028_Loop-Lines-{name}.png" alt="{esc(alt)}"{size} loading="eager"{cls}>'


def link(name, text):
    return f'<a href="{REL}20261028_Loop-Lines-{name}">{esc(text)}</a>'


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def station_table_html(L):
    rows = []
    for sid in G.STATIONS:
        t = L.table[sid]
        rows.append(f'<tr><td>{sid}</td><td>{esc(M["nodes"][sid]["short"])}</td><td>{t["district"]}</td><td>{t["col"]}</td>'
                    f'<td>{t["row"]}</td><td>{esc(t["label"])}</td><td>{esc(" ".join(G.station_loops(sid)))}</td><td>{esc(t["why"])}</td></tr>')
    return ('<div class="wrap" tabindex="0" role="region" aria-label="Station table"><table class="t"><caption>The 25-row station table '
            '(20261028_Loop-Lines-Station-Table.csv). Columns and rows are grid cells of 36 px on the 1440 poster, counted from the hub; '
            'the verifier reads this file and checks every drawn station against it.</caption><thead><tr><th scope="col">ID</th>'
            '<th scope="col">Station name (V7)</th><th scope="col">District</th><th scope="col">Column</th><th scope="col">Row</th>'
            '<th scope="col">Name side</th><th scope="col">Loops</th><th scope="col">Why it sits there</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def checks_html():
    v, c = load(VERIFY), load(CHECK)
    out = []
    if v:
        out.append("<h3>Data check against V7</h3><ul class=\"tight\">" + "".join(f"<li>{esc(x)}</li>" for x in v["summary"]) + "</ul>")
        if v.get("mutation_test"):
            out.append("<p>Mutation test: I planted one error of each kind in copies of the files and ran the verifier on each copy.</p><ul class=\"tight\">"
                       + "".join(f"<li>{esc(r['planted'].capitalize())} in {esc(r['file'])}: caught ({r['caught']} flag{'s' if r['caught'] != 1 else ''}). "
                                 f"First flag: {esc(r['first'][0] if r['first'] else '')}</li>" for r in v["mutation_test"]) + "</ul>")
    else:
        out.append("<p>The data check has not run yet.</p>")
    if c:
        out.append("<h3>Rendered checks</h3><ul class=\"tight\">" + "".join(f"<li>{esc(x)}</li>" for x in c["summary"]) + "</ul>")
        out.append("<p>Not checked by script: " + esc(" ".join(c.get("not_checked", []))) + "</p>")
    else:
        out.append("<p>The rendered checks have not run yet.</p>")
    return "".join(out)


RUBRIC = [
    ("Craft", 4, "Octilinear routes on one 36 px grid, one corner radius with concentric parallel tracks, zero crossings, no truncated name, "
              "every label, tag and bullet placed by a collision score and reviewed at 2x; the rendered label audit ported from Direction A finds no collision."),
    ("Clarity", 4, "Each loop reads as a closed line with its stations on it, and the legend teaches the rest. With one ink, a reader cannot "
                   "follow a line through the E1 hub on the poster alone; the working map lights one line to answer that."),
    ("Brand fidelity", 4, "Locked palette and faces only. Prussian carries no red; red appears on White at one reform's targets. "
                          "With the wordmark covered, the Prussian ground, Inter Tight districts and the red discipline still read as Oath & Action."),
    ("Usefulness", 4, "Every position, route, offset, size and color comes from two small tables and five scripts. A producer can move a station in "
                      "the table, rebuild and rerun the checks."),
    ("Evidence honesty", 4, "Every drawn ID, sign, grade, delay and target matches V7 (0 mismatches, mutation test passed). The poster states that "
                            "spacing carries no meaning and points to the register. Two two-step loops ride long routes, which a reader could misread as weight."),
    ("Accessibility", 4, "No text under 13 px, no contrast failures and no axe-core violations on any page at its width; a text version of the "
                         "poster and of each card; no meaning carried by color alone. Screen readers and keyboard order were not tested."),
    ("Beauty and distinctiveness", 4, "A signature image: the eight-spoke hub at the center, the octagon of the two long shuttles, double tracks for every "
                                      "two-step loop, all on Prussian. The east cluster is dense, and the sign tags still add texture a world-class transit diagram would not carry."),
]

DECISIONS = [
    ("E1 is the center: an eight-spoke hub, with A west, B north, C east and D south and east, clockwise in the order effects mostly travel", "Seven loops meet at E1, and its eight connections fill the eight directions exactly"),
    ("Station positions live in the 25-row station table as whole grid cells; corridors are routed by script", "One file to review when V7.1 changes a loop, and the verifier reads it"),
    ("Corridors run straight where stations align; otherwise an octilinear A* path that stays one cell from every other station and clear of every station name", "Calm routes with no crossing, and labels never sit on a line"),
    ("Each loop rides the side of a shared corridor that faces its own inside, nested loops innermost", "Parallel lines never swap places, so no route hides another"),
    ("Two-step loops run clockwise, so the first step rides the upper or left track", "It matches reading order and the review's R8 card: L38 above, L39 below"),
    ("A station on one loop is a ring, on several a capsule, on five or more a capsule that holds its name", "Only E1 qualifies; its eight spokes leave no free side for a label"),
    ("Every station prints its V7 ID in its ring", "The ID tells the district at once, which matters for B1 and E2, which sit away from their fields"),
    ("The sign tag points the way its step runs", "A loop has an order; one mark carries the sign and the direction"),
    ("M1 dash lengths scale with line weight: the code is written for a 2 px line, doubled on the 4 px poster line and tripled on the 6 px card line", "The texture looks the same at every scale"),
    ("Line bullets are the M3 chip in a bullet form, set on a stretch only their loop rides or on a 1 px leader from it; the code alone on screen, the kind glyph added in print", "The review: a bullet must belong to its line, and a 12 px glyph reads as a numeral"),
    ("The kind glyphs are Direction B's spiral and ring, drawn only where they reach 24 px: the print poster, the card head, the catalog chips", "The winner and B then share one loop-kind mark at a size that reads"),
    ("District fields are drawn on the grid from a field table; B1 and E2 sit in their own patches, each lettered", "R1, R6 and R7 put B1 and E2 there; the patch is honest about it"),
    ("Field tint: Prussian mixed 16 percent toward Newsprint in OKLab (#39476D), proposed as a token", "At 25 percent in grayscale the five areas read only at this step; White names on it measure above 9:1"),
    ("The frame says its counts in words, one horizontal line per band", "The review found the ticks and side text hard to read; words carry the same counts"),
    ("Lit views draw the lit loops at 6 px Charcoal and the rest at 2 px Stone, with Charcoal stations", "The lit line has to win by weight as well as color, so it holds in grayscale"),
    ("Sign tags are placed after stations and names, by a collision score", "Tags at the middle of a short run fell under the hub and beside names"),
    ("Miniatures share one scale, 0.38 of the poster cell; names take the clearest of eight sides", "R4b and R1b set the scale; every other difference comes from the data"),
    ("Catalog cards span two columns when a loop crosses three areas; the sketched loops close the page in the same grid", "Width means reach, and every row fills"),
    ("R8 is drawn horizontally on the map", "Its card then reads like the line map inside a train car"),
    ("Card headlines: R8 reuses Concept 08's; R10's is the studio's, written from V7's how_to_read; both are labeled", "Dustin already approved the R8 wording in his reference"),
    ("The R10 card names R-01; the reform view keeps R-01's three loops in Charcoal and drops the rest to Stone", "Both views mark one reform, and the targets read in their context"),
    ("Phone cards draw IDs only and list the steps and stations as text", "Names cannot fit around a 358 px drawing without overlap"),
    ("The card's locator inset is the Newsprint working map with the loop lit", "A lit line on Prussian would need a new dim tone; Newsprint already has Stone"),
    ("The view pages carry the lines in words, as a table at 1440 and a list on a phone, and fit the drawing to a phone screen", "The diagram needs a text equivalent, and a 1440 px page should not scroll sideways"),
]

FOR_DUSTIN = [
    ("Direction C as the systems map direction", "Adopt C; keep A's Circuit as the whole-system fallback", "Adopt C", "Twenty closed lines hold at 1440 px with zero crossings, so the fallback the review set is not needed."),
    ("The pointing sign tag", "Adopt; signs without direction", "Adopt", "A loop has an order; the review's notation budget gives the map a sign glyph and no direction mark."),
    ("The M3 bullet form and the shared spiral and ring", "Adopt both; the full chip with the word Loop", "Adopt both", "Twenty full chips crowd the poster; the glyph prints where it reaches 24 px."),
    ("The field tint token", "Register #39476D; keep #2C3B64; draw fields as outlines", "Register #39476D", "Only the stronger step reads as five areas at 25 percent in grayscale."),
    ("The two long shuttles, R4b and R1b", "Keep the octagon; allow one clean crossing to shorten them", "Keep the octagon", "The topology forces them around the C and D cluster; a crossing would shorten one and add an exception."),
    ("Reader check", "Run it with five readers on R8, R10 and the poster", "Run it", "Every claim here about what a first-time reader sees is studio judgment."),
]


def contrast(a, b):
    def lum(h):
        def lin(c):
            c = c / 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        r, g, bb = (int(h[i:i + 2], 16) for i in (1, 3, 5))
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(bb)
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def layout_facts(L):
    import math
    straight = sum(1 for cells in L.routes_cells.values() if len(G.simplify(cells)) == 2)
    lens = []
    for (a, b), cells in L.routes_cells.items():
        if len(G.simplify(cells)) == 2:
            p, q = cells[0], cells[-1]
            lens.append(max(abs(q[0] - p[0]), abs(q[1] - p[1])))
    return {"corridors": len(L.routes_cells), "straight": straight, "routed": len(L.routes_cells) - straight,
            "min": min(lens), "max": max(lens)}


def label_audit_line():
    c = load(CHECK)
    if not c or "selfTest" not in c:
        return "The label audit has not run yet."
    runs = [(k, a["labels"]) for k, a in c["pages"].items() if a.get("labels") and a["labels"]["drawings"]]
    hits = sum(t["total"] for _, t in runs) + (c["printLabels"]["total"] if c.get("printLabels") else 0)
    n_lab = sum(t["labels"] for _, t in runs)
    st = c["selfTest"]
    return (f"Label audit, ported from Direction A's check: {hits} collisions across {len(runs)} page renders and the print drawing "
            f"({n_lab} labels on screen: text past the drawing, label on label, label on a sign tag, bullet or station, label on a line). "
            f"Its self-test caught {sum(1 for v in st.values() if v)} of {len(st)} planted faults.")


def fixpass_html(L):
    cr = lambda a, b: f"{contrast(a, b):.2f}:1"
    old, new = V.FIELD_TINT_ROUND_TWO, V.FIELD_ON_PRUSSIAN
    items = [
        ("1. Every bullet on its own line", "Each line bullet now sits on a stretch that only its loop rides, centered on its track, "
         "or beside that stretch on a 1 px leader where the stretch has no room (nine of the twenty, all two-step shuttles whose short stretch also holds two tags). "
         "Sign tags are placed after the stations and names, by the same kind of collision score, so they slide clear. R4a's bullet sits on "
         "L56 between its tag and D7, and the plus tag on the C1 to D7 pair moved up toward C1. The verifier now checks that every bullet's "
         "stretch carries no other loop and that the bullet or its leader touches the loop's own drawn track."),
        ("2. Kind glyph off the screen bullets", "On screen the bullet is the outlined code alone, and the legend reads "
         "\u201cR: feeds itself. B: pushes back.\u201d The print poster (its own drawing, 20261028_Loop-Lines-Poster-Print.svg) keeps the glyph "
         "cell, where the glyph prints at about 30 px. The card head and catalog chips draw the glyph at 24 px."),
        ("3. The lit line reads", "On the working map, the reform view and the locator the lit loops draw at 6 px Charcoal "
         "(red at the reform's targets), every other line at 2 px Stone, and stations on a lit loop fill Charcoal with Newsprint IDs. "
         "The grayscale proofs below show the lit loops by weight alone."),
        ("4. The frame in words", "The ticks and the side text are gone. Each band is one horizontal line, for example "
         "\u201cOutside drivers, 5 variables. 12 connections reach areas A to E: 5 into area A, 4 into area B and 1 each into areas C, D and E.\u201d "
         "The economy and technology lines share the bottom band. The text says areas A to E because two of those connections reach A3, "
         "which sits in area A on no loop."),
        ("5. The areas read as territories", f"The tint moves one step, from {old} ({cr(old, D.PRUSSIAN)} against Prussian) to {new} "
         f"({cr(new, D.PRUSSIAN)}). In the grayscale proofs at 25 percent size below, the five areas read only at the stronger step. "
         f"White names on the new tint measure {cr(D.WHITE, new)}. B's patch under the hub and E's hub strip carry their letters, "
         "and the E2 island grew to hold its full name."),
        ("6. A 390 px form for the three views", "Below 1200 px the poster, working map and reform view show the drawing fit to the "
         "screen width in a focusable region, a link to the full-size image, the reform panel where there is one, then the lines in words as a list."),
        ("10. A's label audit in C's check", label_audit_line() + " The two-line C and D district names, which A's audit flagged on the "
         "reform view, now sit 24 px apart."),
        ("Appendix items", "Miniature names are placed by a search over every name's eight sides, so R10's and R12's tiles no longer collide. "
         "The R10 card's step labels step away from their own line, so \u201cLeast certain step\u201d clears L53. The phone card lists its routes "
         "in place of the four-column table, so nothing runs past the card. The phone step list no longer repeats \u201cDocumented on the public record\u201d."),
    ]
    lis = "".join(f"<li><b>{esc(a)}.</b> {esc(b)}</li>" for a, b in items)
    phones = "".join(
        f'<figure class="phone"><div class="tall wrap" tabindex="0" role="region" aria-label="{esc(t)} at 390 px">'
        f'{img(n + "-Phone-Capture", t + " at 390 px: the drawing fit to the screen, the link to full size, then the lines in words")}</div>'
        f'<figcaption>{link(n + ".html", "Open the page")} and narrow the window below 1200 px.</figcaption></figure>'
        for n, t in (("Poster", "Poster"), ("Working-Map", "Working map"), ("Reform-View-R-01", "Reform view")))
    return f'''<section id="fixes"><p class="eyebrow">Fix pass, after the creative director's round-two review</p><h2>What changed in this pass</h2>
<p>The studio picked this poster as the whole-system map, with the working map and the reform view. This pass makes the review's fixes 1 to 6 and 10 and the appendix items. No station moved: the 25-row station table is unchanged.</p>
<ul class="tight">{lis}</ul>
<h3>Field tint proof, grayscale at 25 percent size</h3>
<div class="tints"><figure>{img("Field-Tint-Current-Gray-25", "The poster in grayscale at 25 percent with round two's field tint: the fields barely separate from the ground", 360, 240)}<figcaption>Round two, {old}.</figcaption></figure>
<figure>{img("Field-Tint-Stronger-Gray-25", "The poster in grayscale at 25 percent with the stronger field tint: the five areas read as blocks", 360, 240)}<figcaption>This pass, {new}.</figcaption></figure></div>
<h3>The three views at 390 px</h3>
<div class="phones">{phones}</div>
</section>

'''


def board_html(L, order):
    v = load(VERIFY)
    lf = layout_facts(L)
    cr = lambda a, b: f"{contrast(a, b):.2f}:1"
    mism = v["mismatches"] if v else "not run"
    sections = [("fixes", "Fix pass"), ("poster", "Poster"), ("working", "Working map"), ("catalog", "Catalog page"), ("r8", "R8 card"), ("r10", "R10 card"),
                ("reform", "Reform view"), ("gray", "Grayscale"), ("spec", "Spec"), ("table", "Station table"), ("tests", "Tests"),
                ("checks", "Checks"), ("rubric", "Rubric"), ("decide", "Decisions")]
    toc = "".join(f'<a href="#{a}">{esc(b)}</a>' for a, b in sections)
    rub = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{b}</td><td>{esc(c)}</td></tr>" for a, b, c in RUBRIC)
    dec = "".join(f"<tr><td>{i + 1}</td><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for i, (a, b) in enumerate(DECISIONS))
    fd = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td><b>{esc(c)}</b></td><td>{esc(d)}</td></tr>" for a, b, c, d in FOR_DUSTIN)
    grays = "".join(
        f'<figure><a href="{REL}20261028_Loop-Lines-{n}-Grayscale.png">{img(n + "-Grayscale", "Grayscale proof of the " + t)}</a><figcaption>{esc(t)}</figcaption></figure>'
        for n, t in (("Poster", "poster"), ("Working-Map", "working map"), ("Reform-View-R-01", "reform view"), ("Catalog", "catalog page at 1440 px"),
                     ("Catalog-Phone", "catalog page at 390 px"), ("Card-R8", "R8 card at 1440 px"), ("Card-R8-Phone", "R8 card at 390 px"),
                     ("Card-R10", "R10 card at 1440 px"), ("Card-R10-Phone", "R10 card at 390 px"),
                     ("Poster-Phone", "poster page at 390 px"), ("Working-Map-Phone", "working map page at 390 px"),
                     ("Reform-View-R-01-Phone", "reform view page at 390 px")))
    nb = [("Line texture for the grade (M1)", "Yes, dash code scaled by weight", "Yes", "Yes"),
          ("Hollow line for sketched steps (M1)", "Yes, on the three sketched tiles", "Not drawn: R8 and R10 have none", "Listed in words in the frame"),
          ("Record square on documented labels (M1)", "No", "Yes", "No"),
          ("Grade words with glosses (M2)", "Caption only", "Yes, with the gloss in the phone list", "Legend only"),
          ("Typed chips (M3)", "Line bullet", "Full chips for loop, reform and route", "Line bullets"),
          ("Signs", "No", "Yes, a pointing tag", "Yes, one pointing tag per connection"),
          ("Delay ticks (M4)", "No; delay in words in the caption", "Yes", "No"),
          ("Effect pips, routes (M4)", "No", "Yes, never summed", "No; on the reform page below the map"),
          ("Weakest step", "Its texture, named in the caption", "Named and explained", "No"),
          ("Pillar Red", "Never", "Targets of the named reform", "Reform view on White only")]
    nbh = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td></tr>" for a, b, c, d in nb)
    field = V.FIELD_ON_PRUSSIAN
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Map Direction C Loop Lines</title>
{P.FONTS}
<link rel="stylesheet" href="board-base.css"><style>{CSS}</style></head>
<body><main class="board">
<p class="eyebrow">Phase 2 · Systems maps, round two · Direction C · October 28, 2026 · Data visualization and systems lead</p>
<h1>Loop Lines</h1>
<p class="lede">The loop network drawn as a transit map. Each of Atlas V7's 20 numbered loops is a closed line, each of the 25 variables those loops run through is a station, and a variable several loops share is an interchange. The catalog miniature is each loop's own line lifted from the map, the R8 card is that line at full size, and the whole-system map is a poster on Prussian. Scope is a spec and specimens (G1-08); V7, the atlas file and the ledgers are untouched.</p>
<div class="sumbox"><p><b>Where it landed.</b> The studio picked this poster as the whole-system map, with the Newsprint working map and the R-01 reform view; Direction A's catalog and cards carry the loops, joined by this map's locator inset. This board now shows the fix pass on those three views.</p>
<p><b>Checked.</b> Data check against V7: {mism} mismatches across every drawing; a mutation test caught each of eight planted errors. Every page passes the rendered checks at 1440 and 390 px, and the label audit ported from Direction A finds no collision.</p>
<p><b>Open first.</b> The fix pass, then the poster, the working map and the reform view. Each is a real page, linked under its capture.</p></div>
<nav class="toc" aria-label="Board sections">{toc}</nav>
{fixpass_html(L)}
<section id="poster"><p class="eyebrow">Specimen 1</p><h2>The poster on Prussian, 1440 by 960 px and 24 by 36 inches</h2>
<figure>{img("Poster-Capture", "The Loop Lines poster: twenty closed lines in Newsprint on Prussian, the E1 hub at the center with eight spokes, the west fan of two squares, the C and D cluster framed by the octagon of R4b and R1b, district fields A to E, the frame bands in words and the legend", 1440, 960)}
<figcaption>{link("Poster.html", "Open the poster page")}, with the lines in words below it. {link("Poster-24x36.pdf", "Open the 24 by 36 inch PDF")} (one landscape page, 36 by 24 inches, the print drawing scaled 2.4 times; its bullets carry the kind glyph). The note in the frame reads: "This map draws the 20 numbered loops: 25 variables and 46 connections. The register lists all 51 variables and 118 connections."</figcaption></figure>
<details class="note"><summary>The lines in words</summary>{P.text_version()}</details>
</section>

<section id="working"><p class="eyebrow">Specimen 2</p><h2>The working map on Newsprint, with one line lit</h2>
<figure>{img("Working-Map-Capture", "The working map on Newsprint: Loop R10 lit at 6 px in Charcoal through C1, C2, C3 and C4, its stations filled Charcoal, every other line at 2 px in Stone", 1440, 960)}
<figcaption>{link("Working-Map.html", "Open the working map")}. The live atlas would light any line on request; this specimen lights R10 at 6 px Charcoal, every other line at 2 px Stone. Stone measures {cr(D.STONE, D.NEWS)} on Newsprint, above the 3:1 floor for lines; any text on an unlit line uses deep Stone (#4E535B, {cr(D.DEEP, D.NEWS)}).</figcaption></figure></section>

<section id="catalog"><p class="eyebrow">Specimen 3</p><h2>The catalog page, a line guide, at 1440 and 390 px</h2>
<div class="pair"><figure><div class="tall wrap" tabindex="0" role="region" aria-label="Catalog page capture at 1440 px">{img("Catalog-Capture", "Catalog page at 1440 px: the poster as a Prussian band with the headline Twenty loop lines, a Charcoal how-to-read strip, then 23 White cards on Newsprint in district order, two columns wide for loops that cross three areas")}</div>
<figcaption>{link("Catalog.html", "Open the catalog page at 1440 px")}. Cards in district order: {esc(", ".join(lid for lid, _ in order))}. Every row fills.</figcaption></figure>
<figure class="phone"><div class="tall wrap" tabindex="0" role="region" aria-label="Catalog page capture at 390 px">{img("Catalog-Phone-Capture", "Catalog page at 390 px: the band, the strip and the cards two to a row, with each loop's stations listed in words")}</div>
<figcaption>{link("Catalog-Phone.html", "Open it at 390 px")}.</figcaption></figure></div></section>

<section id="r8"><p class="eyebrow">Specimen 4</p><h2>The R8 card, at 1440 and 390 px, with the locator inset</h2>
<div class="pair"><figure>{img("Card-R8-Capture", "R8 card at 1440 px: a closed shuttle on White between Housing scarcity and Owner home equity; L38 on the upper track, L39 on the lower in red with A5's ring, because R-30 acts there; the locator inset; the R-30 panel with effect pips and routes")}
<figcaption>{link("Card-R8.html", "Open the R8 card at 1440 px")}.</figcaption></figure>
<figure class="phone"><div class="tall wrap" tabindex="0" role="region" aria-label="R8 card capture at 390 px">{img("Card-R8-Phone-Capture", "R8 card at 390 px: the shuttle with IDs, the steps and stations listed below, the locator and the R-30 panel")}</div>
<figcaption>{link("Card-R8-Phone.html", "Open it at 390 px")}.</figcaption></figure></div></section>

<section id="r10"><p class="eyebrow">Specimen 5</p><h2>The R10 card, the stress test</h2>
<div class="pair"><figure>{img("Card-R10-Capture", "R10 card at 1440 px: the four-station line from the map at full size, from documented L08 and L42 to plausible L53, with R-01's targets L25, L08 and C2 in red")}
<figcaption>{link("Card-R10.html", "Open the R10 card at 1440 px")}. Four steps from documented to plausible; L53 is named as the least certain step.</figcaption></figure>
<figure class="phone"><div class="tall wrap" tabindex="0" role="region" aria-label="R10 card capture at 390 px">{img("Card-R10-Phone-Capture", "R10 card at 390 px")}</div>
<figcaption>{link("Card-R10-Phone.html", "Open it at 390 px")}.</figcaption></figure></div></section>

<section id="reform"><p class="eyebrow">Specimen 6</p><h2>The R-01 reform view on White</h2>
<figure>{img("Reform-View-R-01-Capture", "Reform view on White: the whole map with L25, L08 and C2 in Pillar Red, R10, B4 and R11 at 6 px in Charcoal with Charcoal stations, every other line at 2 px in Stone")}
<figcaption>{link("Reform-View-R-01.html", "Open the reform view")}, with R-01's effects and routes below the map. Red never sits on Prussian, so a reform view of the poster moves to White, where Pillar Red measures {cr(D.RED, D.WHITE)}.</figcaption></figure></section>

<section id="gray"><p class="eyebrow">Proofs</p><h2>Grayscale proof of each page</h2>
<p>Lines, textures, tags, rings and capsules carry every distinction in gray. On White, red turns mid gray; the thicker red ring at C2 and A5 and the panel text still name the targets.</p>
<div class="grays">{grays}</div></section>

<section id="spec"><p class="eyebrow">The spec</p><h2>How the drawing is built</h2>
<dl class="spec">
<dt>Grid</dt><dd>One square grid, 36 px a cell on the 1440 poster and 2.4 times that in the PDF. Stations sit on whole cells. Routes use 0, 45 and 90 degrees only. The grid is even and the spacing is close to even: a straight corridor runs {lf['min']} to {lf['max']} cells, most of them 3 to 6, because a 45 degree triangle cannot keep all three sides equal. V7 holds no distances, and the legend says that distance and line length carry no meaning.</dd>
<dt>Routes</dt><dd>A corridor is a pair of stations joined by one or more numbered-loop connections; there are {lf['corridors']}. A corridor runs straight when its stations already align on the grid ({lf['straight']} do). The other {lf['routed']}, R4b and R1b, are routed by an A* search on the grid that keeps one cell from every other station, stays off every station name, never shares a cell with another corridor and never leaves a station in a direction already taken. The result has no crossing.</dd>
<dt>Tracks</dt><dd>A loop rides each of its corridors as one 4 px track, 9 px apart from its neighbors. A loop keeps to the side of a shared corridor that faces its own inside, nested loops innermost; a two-step loop runs clockwise. One corner radius, 22 px on the corridor's center line; parallel tracks turn on concentric arcs, 22 px plus or minus their offset.</dd>
<dt>Stations</dt><dd>An open ring 24 px across for a variable on one loop; an open capsule 42 by 24 px for a variable several loops share; the hub capsule, which holds its name, for a variable on five or more loops (E1 only). White 2.5 px edge, Prussian fill, the V7 ID inside in Inter 13 bold. Names beside them in White Inter 15 semibold, V7's chain labels, one or two lines, never truncated. On a lit view a station on a lit loop fills Charcoal with its ID in Newsprint; the rest keep a Stone ring.</dd>
<dt>Signs</dt><dd>One tag per connection, across its bundle when several loops ride it, at the middle of its longest straight run or slid along it by the least distance that clears every station and name. Newsprint fill, the sign in Prussian Inter 13 bold, the tag's point toward the way the step runs. The two directions of a two-step loop carry their tags together, up to 48 px apart. On a lit view a lit tag turns Charcoal with a Newsprint sign.</dd>
<dt>Textures</dt><dd>Gate 1 mark M1, V7's code: documented and well supported solid, plausible 9 4, contested 9 3 2 3, hypothesis 2 4, written for a 2 px line and scaled with weight (18 8, 18 6 4 6 and 4 8 on the poster).</dd>
<dt>Line bullets</dt><dd>M3 in a bullet form, 22 px tall: the code outlined in Inter 14 bold, set on a stretch that only its loop rides, centered on its track, or beside that stretch on a 1 px leader when the stretch has no room. Placed by a collision score, the loops with the fewest clear places first. On screen the loop's R or B carries its kind; the print drawing adds a 20 px ink cell with the kind glyph (spiral for a loop that feeds itself, ring for one that pushes back), which prints at about 30 px.</dd>
<dt>Districts</dt><dd>Fields A to E drawn on the grid from the field table (20261028_Loop-Lines-District-Fields.csv), 8 px apart, corners rounded at 14 px, tinted {field} (Prussian mixed 16 percent toward Newsprint in OKLab, one step stronger than round two's 8.5 percent). B1 sits in its own B patch south of the hub and E2 in an E island inside D, because R1, R6 and R7 put them there; the B patch and E's hub strip carry their letters, and the E island holds the E name. District names in Newsprint Inter Tight 800, the letter at 40 px, two-line names at 24 px leading.</dd>
<dt>Frame</dt><dd>Outside drivers along the top, the economy and technology layers along the bottom, each as one horizontal line in Inter 13: the group's name in capitals, its variable count, and how many of its connections reach each area (12, 15 and 8 in all), counted from V7 and checked by the verifier.</dd>
<dt>Lit views</dt><dd>Working map, reform view and locator: the lit loops at 6 px Charcoal (red at the targets of the named reform), every other loop at 2 px Stone, dash lengths scaled with each weight. The locator keeps the same three-to-one ratio at its scale.</dd>
<dt>Phone form</dt><dd>Below 1200 px a view page shows its capture fit to the screen width in a focusable region, a link to the full-size image, the reform panel where there is one (routes as a list), then the lines in words as a list.</dd>
<dt>Surfaces</dt><dd>Poster: Prussian with Newsprint lines ({cr(D.NEWS, D.PRUSSIAN)}) and White names ({cr(D.WHITE, D.PRUSSIAN)}), no red; White on the field tint measures {cr(D.WHITE, V.FIELD_ON_PRUSSIAN)}. Working map: Newsprint, one line in Charcoal, the rest in Stone. Catalog: Newsprint with White cards, a Prussian band head and a Charcoal how-to-read strip. Card and reform view: White, red only at the targets of the one reform the view names ({cr(D.RED, D.WHITE)}).</dd>
<dt>Miniature</dt><dd>The loop's own tracks lifted from the poster at one shared scale, 0.38 of the poster cell: 3 px lines, 6 px rings, names in Inter 13 semibold, placed by a search over each name's eight sides that keeps them off one another, the stations and the line, Stone ghost stubs 0.85 cell long for the other corridors at each shared station. No signs, ticks or red. The caption names the kind, the turn in words, the least certain step with its grade, and the areas it crosses.</dd>
<dt>Card</dt><dd>The loop's line at full size, the shape it has on the map: 6 px line, 22 px rings, station names in Inter Tight 700 22 px with V7's reading rule for a higher value in Inter 15, each step with its ID and V7 name, sign tag, grade word, record square when documented, and one to three delay ticks. Labels are placed by a collision score over 96 trial scales and offsets. V7's how_to_read in Lora Italic 20 px. At 390 px the drawing keeps IDs only and the words follow as lists.</dd>
<dt>Catalog</dt><dd>Band head 1440 by 560 px. Four columns, 24 px gutters. Cards in district order: A's lines first, then B, C, D and E, a line placed after the last area it reaches. A card spans two columns when its loop crosses three areas. Rows always fill; the three sketched loops close the page in the same grid.</dd>
</dl>
<h3 style="margin-top:22px">Notation budget, as built</h3>
<div class="wrap" tabindex="0" role="region" aria-label="Notation budget"><table class="t"><thead><tr><th scope="col">Mark</th><th scope="col">Miniature</th><th scope="col">Loop card</th><th scope="col">Whole-system map</th></tr></thead><tbody>{nbh}</tbody></table></div>
</section>

<section id="table"><p class="eyebrow">Layout data</p><h2>The station table</h2>
{station_table_html(L)}
</section>

<section id="tests"><p class="eyebrow">The review's tests</p><h2>Wall test, 2x test and the other two</h2>
<h3>Wall test, applied on screen</h3>
<p>I viewed the poster at 100 percent and the PDF at print scale beside the review's benchmarks as I know them; I could not print or pin anything. What I changed because of it:</p>
<ul class="tight">
<li>The first Voronoi district fields drew faint diagonal seams across the map. I replaced them with fields drawn on the same grid as the stations.</li>
<li>The first chips used the full M3 chip with the word Loop twenty times and outweighed the stations. I moved to the bullet form and placed each bullet inside its own ring.</li>
<li>The sign tags read as a swarm of arrows at a distance. I cut them to 18 by 14 px with a 13 px glyph.</li>
<li>The note box sat on the R4b arch. I moved it into the clear corner beside the arch.</li>
<li>Making R8 horizontal turned a lost vertical stub into a small shuttle a reader finds at once.</li>
</ul>
<h3>2x test</h3>
<p>I reviewed 2x crops of nine tiles of the poster and of the catalog and both cards. What I changed because of it:</p>
<ul class="tight">
<li>The router once sent R4b through the names of B6 and B4; corridors now treat station names as obstacles.</li>
<li>B2's name was boxed in by the arch; B2 moved one cell closer to C3.</li>
<li>The B4 triangle was too small for its bullet; C5 and D5 moved one cell west.</li>
<li>R8's two tags overlapped; the two directions of a two-step loop now carry their tags 48 px apart.</li>
<li>R12's bullet clipped R4a's diagonal; bullets may now sit beside one of their own edges.</li>
<li>Miniature names were squeezed under 13 px where a drawing outgrew its card; the shared scale dropped to 0.38 and end names move above and below.</li>
<li>The R10 card's names collided with its step labels; the card now tries 96 scales and offsets and keeps the clearest.</li>
<li>The B2 sketched tile printed its two names on top of each other; they now sit outside each end.</li>
</ul>
<p>Fix pass, at 2x: every bullet now sits on its own stretch or its leader, R4a clears the C1 to D7 tag, the tags at the hub clear E1, and the R10 card's labels clear their lines. The rendered label audit finds no collision on any page.</p>
<h3>Distinctiveness test</h3>
<p>With the wordmark covered, the Prussian ground, the Newsprint lines, Inter Tight district names and red only on White still read as Oath & Action. Nothing borrows the roundel, the Johnston face, TfL's colors or the MTA's bullets.</p>
<h3>Ten-second test</h3>
<p>Not run. It needs five readers and Dustin's go.</p>
</section>

<section id="checks"><p class="eyebrow">Checks</p><h2>What the scripts checked</h2>{checks_html()}</section>

<section id="rubric"><p class="eyebrow">Rubric</p><h2>Scores, studio judgment, threshold 4</h2>
<div class="wrap" tabindex="0" role="region" aria-label="Rubric"><table class="t rubric"><thead><tr><th scope="col">Criterion</th><th scope="col">Score</th><th scope="col">Reason</th></tr></thead><tbody>{rub}</tbody></table></div></section>

<section id="decide-studio"><p class="eyebrow">Decisions I made</p><h2>Routine decisions, one line each</h2>
<div class="wrap" tabindex="0" role="region" aria-label="Decisions"><table class="t"><thead><tr><th scope="col">#</th><th scope="col">Decision</th><th scope="col">Reason</th></tr></thead><tbody>{dec}</tbody></table></div></section>

<section id="decide" class="decision"><p class="eyebrow">Decisions for Dustin</p><h2>What you decide</h2>
<div class="wrap" tabindex="0" role="region" aria-label="Decisions for Dustin"><table><thead><tr><th scope="col">Decision</th><th scope="col">Options</th><th scope="col">Studio recommendation</th><th scope="col">Why</th></tr></thead><tbody>{fd}</tbody></table></div>
<p>Red on these specimens follows Rule 05.3 as worded in D2-01. Each view carries one working red, the point the headline names, which in a systems figure is where a reform acts. Red never sits on Prussian.</p></section>
<p class="src" style="margin-top:28px">{esc(P.SRC)} Built by work/build/scripts/phase-2/maps_r2_c_build.py. Notes: work/handoffs/phase-2/20261028_Map-Direction-C-Notes.md.</p>
</main></body></html>'''


def build(L, order):
    BOARD.write_text(board_html(L, order), encoding="utf-8")
