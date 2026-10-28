#!/usr/bin/env python3
"""Build the Systems Map Directions Board, its drawings and the two phone pages, all from Atlas V7.

Run:  python3 -I work/build/scripts/phase-2/build_maps_board.py
Then: python3 -I work/build/scripts/phase-2/verify_maps_data.py
      node work/build/scripts/phase-2/check_maps_board.js
      python3 -I work/build/scripts/phase-2/build_maps_board.py   (again, to print the check results on the board)
Reads  work/extract/atlas-v7-data.json through maps_model.py
       work/boards/phase-2/maps/20261028_Maps-Verify-Results.json and 20261028_Maps-Check-Results.json (when present)
Writes work/boards/20261028_Systems-Map-Directions-Board.html
       work/boards/phase-2/maps/*.svg, the phone pages *.html, and the model data JSON
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import maps_draw as D  # noqa: E402
import maps_explore as X  # noqa: E402
import maps_line  # noqa: E402
import maps_model as MM  # noqa: E402
import maps_orbit  # noqa: E402
import maps_weave  # noqa: E402

ROOT = HERE.parents[3]
ASSETS = ROOT / "work/boards/phase-2/maps"
BOARD = ROOT / "work/boards/20261028_Systems-Map-Directions-Board.html"
REL = "phase-2/maps/"
VERIFY = ASSETS / "20261028_Maps-Verify-Results.json"
CHECK = ASSETS / "20261028_Maps-Check-Results.json"
esc = html.escape
M = MM.build_model()
LP = M["loops"]
SNAP = "October 15, 2026"
SRC = f"Source: Who Do They Answer To? Systems Atlas V7, snapshot {SNAP}."
WRITTEN = []
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


def save_svg(name, svg):
    """Write one drawing as a standalone SVG file and return it for inlining."""
    path = ASSETS / f"20261028_{name}.svg"
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg, encoding="utf-8")
    WRITTEN.append(path)
    return svg


def chip(kind, code):
    return f'<span class="chip"><span class="k">{esc(kind)}</span><span class="c">{esc(code)}</span></span>'


def kind_badge(t, size=26):
    body = D.kind_mark(size / 2, size / 2, t, r=size / 2 - 3.5)
    return (f'<svg class="kb" width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false">'
            f'{D.STYLE}{body}</svg>')


def grade_word(g):
    return D.GRADE_WORD[g]


# ------------------------------------------------------------------ effect pips (Mark 4)

SIZE = {"S": 1, "M": 2, "L": 3}


def parse_effect(v):
    """V7 effect string to marks: the first code is firm; a code after 'to' is the open end of a range."""
    v = v.replace("−", "-")
    out = {"gain": 0, "gain_open": 0, "cost": 0, "cost_open": 0, "zero": False, "uncertain": "?" in v}
    parts = re.split(r"\bto\b", v)
    for i, part in enumerate(parts):
        for sign, size in re.findall(r"([+-])([SML])\b", part):
            key = ("gain" if sign == "+" else "cost") + ("_open" if i > 0 else "")
            out[key] = max(out[key], SIZE[size])
        if re.search(r"(^|\s)0(\s|$)", part):
            out["zero"] = True
    return out


def pips_svg(v, w=160, h=24):
    p = parse_effect(v)
    cx = w / 2
    out = [f'<line x1="{cx}" y1="2" x2="{cx}" y2="{h - 2}" stroke="{D.INK}" stroke-width="1"/>']
    for side, firm, open_ in ((1, p["gain"], p["gain_open"]), (-1, p["cost"], p["cost_open"])):
        for i in range(max(firm, open_)):
            x = cx + side * (12 + i * 12)
            if i < firm:
                out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="4.5" fill="{D.INK}"/>')
            else:
                out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="3.75" fill="none" stroke="{D.INK}" stroke-width="1.5"/>')
        if max(firm, open_):
            gx = cx + side * (12 + max(firm, open_) * 12)
            out.append(D.T(gx - (3 if side > 0 else -3), h / 2 + 4.5, "+" if side > 0 else D.MINUS, 13, 700, D.INK, "start" if side > 0 else "end"))
    if p["zero"]:
        out.append(f'<rect x="{cx - 2:.1f}" y="{h / 2 - 7:.1f}" width="4" height="14" fill="{D.INK}"/>')
    if p["uncertain"]:
        out.append(f'<circle cx="{cx}" cy="{h / 2}" r="8" fill="{D.WHITE}" stroke="{D.INK}" stroke-width="1.5"/>' + D.T(cx, h / 2 + 4.5, "?", 13, 700, D.INK, "middle"))
    return (f'<svg class="pips" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Effect {esc(v)}" data-effect="{esc(v)}">'
            f'{D.STYLE}{"".join(out)}</svg>')


def tm(s):
    return re.sub(r"(?<![\w])-(?=[SML0])", D.MINUS, s)


# ------------------------------------------------------------------ text for one loop

def weakest_text(lp):
    if lp["conceptual"]:
        return "No numbered steps, so no step can be graded on its own"
    steps = lp["steps"]
    if lp["weakest"]:
        ws = [s for s in steps if s["id"] in lp["weakest"]]
        return "Weakest: " + ", ".join(f'{s["id"]} {grade_word(s["evidence"]).lower()}' for s in ws)
    grades = sorted({grade_word(s["evidence"]) for s in steps})
    if len(grades) == 1:
        return f"Every step {grades[0].lower()}"
    return "Steps tie at V7's rank: " + " and ".join(g.lower() for g in grades)


def targets_text(lp):
    if not lp["targets"]:
        if lp["reforms"]:
            return "Its reforms (" + ", ".join(lp["reforms"]) + ") act outside the drawn steps"
        return "No reform listed on this loop"
    rs = sorted({r for v in lp["targets"].values() for r in v})
    return "Reforms acting here: " + ", ".join(rs)


def mini_card(direction, lp, svg):
    kind = f'{lp["kind_word"]}, {lp["kind_gloss"]}'
    closure = "" if lp["closure"].startswith("closed: every") else (
        '<p class="mcflag">Closes through a hypothesized step</p>' if lp["hypothesized"] else '<p class="mcflag">Sketched: no complete numbered chain</p>')
    return (f'<article class="mc" data-loop="{lp["id"]}"><div class="mchead">{chip("Loop", lp["id"])}{kind_badge(lp["type"])}'
            f'<span class="mck">{esc(kind)}</span></div><h4>{esc(lp["title"])}</h4>{closure}'
            f'<div class="mcfig">{svg}</div>'
            f'<p class="mcf">One turn: {esc(lp["delay_word"])}. {esc(weakest_text(lp))}. {esc(targets_text(lp))}.</p></article>')


def catalog(direction):
    out = []
    for g in M["groups"]:
        cards = []
        for lid in g["loops"]:
            lp = LP[lid]
            if direction == "orbit":
                svg = maps_orbit.mini(lp)
            elif direction == "line":
                svg = maps_line.mini(lp)
            else:
                svg = maps_weave.mini(lp, M)
            save_svg(f"{direction.title()}-Mini-{lid}", svg)
            cards.append(mini_card(direction, lp, svg))
        title = g["title"] if g["id"] == "SK" else f'{g["id"]}  {g["title"]}'
        out.append(f'<div class="cgroup"><h4 class="cgh">{esc(title)} <span class="cn">{len(g["loops"])} loops</span></h4>'
                   f'<div class="cgrid c-{direction}">{"".join(cards)}</div></div>')
    return "".join(out)


# ------------------------------------------------------------------ the R8 card

def facts_r8(lp, compact=False):
    w = (f'No single step. Both steps are graded well supported. V7\'s summary still calls L39 "the weaker step because equity is '
         f'one motive among several for opposing construction."')
    return [
        ("One turn takes", f'{lp["delay_word"].capitalize()}. V7 gives a loop the delay of its slowest step, and both steps here take over 10 years.'),
        ("Weakest step", w),
        ("Now", f'{lp["direction_word"].capitalize()}. V7 tracks it by "{lp["reference_mode"]}".'),
        ("Revised in V7", f'The loop grade note reads "{lp["evidence_text"]}". {lp["qualification"]}'),
    ]


def reform_block(rid, loop_id, compact=False):
    r = M["reforms"][rid]
    lp = LP[loop_id]
    inside = [t for t in r["targets"] if t in {s["id"] for s in lp["steps"]} | {s["code"] for s in lp["stations"]}]
    outside = [t for t in r["targets"] if t not in inside]

    def name_of(t):
        if t in M["links"]:
            return f'{t}, {M["links"][t]["name"]}'
        return f'{t}, {M["nodes"][t]["title"]}'
    others = sorted({o for o, rr in M["reforms"].items() if o != rid and not rr["rejected"] and set(rr["targets"]) & set(inside)})
    eff_rows = "".join(
        f'<tr><th scope="row">{esc(M["families"][k])}</th><td>{pips_svg(v)}</td><td>{esc(tm(v))}'
        f'{" (" + esc(M["effect_codes"][v]) + ")" if v in M["effect_codes"] else ""}</td></tr>' for k, v in r["effects"].items())
    route_rows = "".join(
        f'<tr><td>{chip("Route", x["route"])}</td><td>{esc(M["route_names"][x["route"]])}: {esc(x["who"])}</td><td>{esc(x["feasibility"])}</td>'
        f'<td>{esc(D_long(x["checked"])) if x["checked"] else "no check date in V7"}</td></tr>' for x in r["routes"])
    also = (f' Reform {", ".join(others)} also acts on {", ".join(t for t in inside if any(t in M["reforms"][o]["targets"] for o in others))}; '
            f'V7 does not list it on this loop.' if others else "")
    return f'''<section class="rblock" aria-label="Where reform {rid} acts">
  <p class="eyebrow">Where a reform acts</p>
  <h4>{chip("Reform", rid)} {esc(r["title"])}</h4>
  <p><span class="redkey" aria-hidden="true"></span> Red marks where {rid} acts in this loop: {"; ".join(esc(name_of(t)) for t in inside)}.
  {("It also acts outside this loop on " + "; ".join(esc(name_of(t)) for t in outside) + ".") if outside else ""}{esc(also)}</p>
  <p>Evidence that the problem exists: <b>{grade_word(r["problem_grade"])}</b>. Evidence that the remedy works: <b>{grade_word(r["remedy_grade"])}</b>.
  Confidence in the effects, in V7's words: "{esc(r["effects_confidence"])}".</p>
  <div class="wrap" tabindex="0" role="region" aria-label="Expected effects of {rid}"><table class="eff"><caption>Expected effect by outcome family, ordinal and never added up</caption>
  <thead><tr><th scope="col">Outcome family</th><th scope="col">Mark</th><th scope="col">V7 value</th></tr></thead><tbody>{eff_rows}</tbody></table></div>
  <div class="wrap" tabindex="0" role="region" aria-label="Routes for {rid}"><table class="eff"><caption>Routes to change</caption>
  <thead><tr><th scope="col">Route</th><th scope="col">Who acts</th><th scope="col">Feasibility, 2026 to 2030</th><th scope="col">Checked</th></tr></thead><tbody>{route_rows}</tbody></table></div>
</section>'''


def D_long(iso):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    y, m, d = iso.split("-")
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def step_table(lp):
    rows = "".join(
        f'<tr><td>{chip("Connection", s["id"])}</td><td>{esc(s["from"])} to {esc(s["to"])}</td><td>{D.sign_glyph(s["polarity"])}</td>'
        f'<td>{esc(s["type"])}</td><td>{esc(grade_word(s["evidence"]))}</td><td>{esc(D.DELAY_WORD[s["delay"]])}</td><td>{esc(s["name"])}</td></tr>'
        for s in lp["steps"])
    return ('<details class="eqv"><summary>Table equivalent of the drawing</summary><div class="wrap" tabindex="0" role="region" aria-label="Steps of loop '
            + lp["id"] + '"><table><thead><tr><th scope="col">Connection</th><th scope="col">From, to</th><th scope="col">Sign</th><th scope="col">Type</th>'
            '<th scope="col">Grade</th><th scope="col">Delay</th><th scope="col">V7 name</th></tr></thead><tbody>' + rows + "</tbody></table></div></details>")


def r8_card(direction):
    lp = LP["R8"]
    if direction == "orbit":
        fig = save_svg("Orbit-Card-R8", maps_orbit.card_figure(lp, M, "R-30"))
        layout = "side"
    elif direction == "line":
        fig = save_svg("Line-Card-R8", maps_line.card_figure(lp, M, "R-30"))
        layout = "wide"
    else:
        fig = save_svg("Weave-Card-R8", maps_weave.card_figure(lp, M, "R-30"))
        layout = "wide"
    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts_r8(lp))
    return f'''<article class="card {layout}" aria-labelledby="card-{direction}-h">
  <div class="cardhead"><p class="eyebrow">Loop card, full size</p>
    <div class="chiprow">{chip("Loop", "R8")}{kind_badge("R", 30)}<span>Reinforcing loop: feeds itself. Closed: every step is a numbered connection.</span></div>
    <h3 id="card-{direction}-h">{esc(lp["title"])}</h3>
    <p class="deck">Read it aloud: {esc(lp["how_to_read"])}</p></div>
  <div class="cardbody"><div class="cardfig wrap" tabindex="0" role="region" aria-label="Loop R8 drawing, scrolls sideways on a narrow screen">{fig}</div>
    <dl class="facts">{facts}</dl></div>
  {reform_block("R-30", "R8")}
  {step_table(lp)}
  <p class="src">{esc(SRC)} Loop R8, connections L38 and L39; reform R-30. Variable names on the drawing are V7's own chain labels.</p>
</article>'''


# ------------------------------------------------------------------ keys and specs

def key_panel():
    def line(grade, conceptual=False, w=86):
        st = {"evidence": grade, "conceptual": conceptual, "delay": None, "type": "causal"}
        return (f'<svg width="{w}" height="18" viewBox="0 0 {w} 18" aria-hidden="true">'
                + D.connection([(3, 9), (w - 3, 9)], st, ticks=False) + "</svg>")

    def tick(dl, w=86):
        st = {"evidence": "documented", "delay": dl, "type": "causal"}
        return f'<svg width="{w}" height="18" viewBox="0 0 {w} 18" aria-hidden="true">' + D.connection([(3, 9), (w - 3, 9)], st) + "</svg>"

    def pill(sign, doc=False):
        p, w = D.sign_pill(22, 12, {"polarity": sign, "evidence": "documented" if doc else "plausible", "type": "causal"})
        return f'<svg width="44" height="24" viewBox="0 0 44 24" aria-hidden="true">{D.STYLE}{p}</svg>'

    def ptr(red=False):
        return (f'<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">'
                + D.pointer(12, 18, 0, -1, red=red) + "</svg>")
    rows = [
        (line("documented"), "Documented or well supported: a solid line (V7). Documented adds the record square to the label, Mark 1."),
        (line("plausible"), "Plausible: dashed, V7's 9 4."),
        (line("plausible_contested"), "Contested: dash-dot, V7's 9 3 2 3. Credible studies disagree."),
        (line("hypothesis"), "Hypothesis: dotted, V7's 2 4. Proposed, not yet supported."),
        (line(None, True), "A step in a sketched loop, which has no numbered connection: the hollow line, Mark 1."),
        (tick("S") + tick("L"), "Delay ticks at the start of a step: one under 2 years, two 2 to 10 years, three over 10 years, Mark 4."),
        (pill("+", True) + pill("-"), "The step's label at its smallest: its sign, with the record square when documented. A plus means the two move the same way, not that the change is good."),
        (ptr() + "<span class='ks'>on the catalog</span>" + ptr(True) + "<span class='ks'>on a card that names one reform</span>",
         "A reform acts here. Ink on the catalog, which names no single reform; Pillar Red on White where the view names one reform (Rule 05.3)."),
        (kind_badge("R", 30) + kind_badge("B", 30), "Loop kind, in the causal loop diagram convention: R feeds itself, B pushes back. Always printed with the words."),
    ]
    body = "".join(f'<div class="krow"><div class="kmark">{a}</div><p>{b}</p></div>' for a, b in rows)
    return f'<div class="keygrid s-newsprint">{body}</div>'


SPECS = {
    "orbit": [
        ("Idea", "A loop is a closed figure. A slow step takes the long way round, so every loop draws its own shape."),
        ("Grid and scale", "Stations on a base circle, step 1 at twelve o'clock, clockwise, evenly spaced. Each step is a circular arc whose bow is a share of its chord: 0.14 under 2 years, 0.27 for 2 to 10 years, 0.42 over 10 years. The catalog uses a 58 to 62 px radius in a 236 by 206 cell; the card uses 178 px; the phone card 104 px. Only geometry scales."),
        ("Nodes and lines", "Variables are Charcoal discs with the ID in Newsprint, 13 px (catalog) and 18 px (card). Lines 2 px (catalog), 2.5 px (card), in V7's texture; arrowheads 9 by 4.5; ticks 1.5 by 10 px. A sketched loop sits on the plain base circle in the hollow line."),
        ("Type", "Inter 13 px bold for IDs and labels in the catalog, Inter 15 px semibold for step names on the card, Inter Tight 800 for card IDs and headlines. Nothing under 13 px."),
        ("Color", "Charcoal for every data mark on Newsprint. Stone for context only. Red on the card and reform views only, on White, at the targets of the one reform the headline names."),
        ("Labels", "Catalog: IDs, sign labels, the word 'weakest', pointers. Card: each step's ID, V7 name, grade and delay outside its arc, away from the center; station names outside the disc."),
        ("Scale", "Miniature, card and phone card call one geometry function at three radii. The whole map keeps the rule (bend left, slower bends more) on one ring of all 51 variables."),
        ("Phone", "Catalog as a list, miniature at 132 px beside its title. Card stacks: drawing at 326 px with IDs only, then the steps as a numbered list."),
    ],
    "line": [
        ("Idea", "A loop is a line you ride out and back: stations in V7's chain order, the closing step on a return line underneath."),
        ("Grid and scale", "Stations at a fixed pitch, 82 px in the catalog and 596 px between box centers on a two-step card, so a longer strip means more steps and nothing else. The return line drops 40 px (catalog) or 96 px (card) and runs back with 10 or 16 px corners."),
        ("Nodes and lines", "Catalog stations are 30 by 22 Charcoal tiles with the ID. Card stations are boxes with a 6 px Charcoal spine, the ID, V7's chain label and its reading rule ('Higher: ...'). Lines and marks as Orbit."),
        ("Type", "Inter 13 px in the catalog; 15 px semibold step names and 16 px bold station names on the card."),
        ("Color", "As Orbit. Red marks the targeted step's whole line and the targeted station's outline."),
        ("Labels", "Step names above each forward step, grade and delay below. The return step is labeled under the return line."),
        ("Scale", "One function draws the strip at two pitches. The whole map lays all 51 variables on one line, drivers and the two lower layers first, then A to E; links that run right arc over, links that run back arc under."),
        ("Phone", "The strip turns vertical: stations stacked, steps running down, the return line up the left side."),
    ],
    "weave": [
        ("Idea", "A loop is a stitch in the fabric of the system: rows are variables, vertical threads are connections."),
        ("Grid and scale", "Rows in V7's system order, 44 px apart in the catalog and 86 px on the card, with an 18 or 34 px gap where the loop crosses into another area. One thread per step, in chain order, 60 or 150 px apart."),
        ("Nodes and lines", "A dot where a thread leaves its row, an arrowhead where it lands. Row IDs in Charcoal tiles. Labels sit beside each thread so the texture stays visible."),
        ("Type", "Inter 13 px for IDs and labels; card row names 16 px bold with the reading rule in 13 px."),
        ("Color", "As Orbit. On the card, the loop's other connections to the rest of the system are Stone."),
        ("Labels", "Card: each thread's ID, V7 name, grade and delay beside it; 'Its other connections' names the far variable at each stub."),
        ("Scale", "The miniature is the card's rows and threads without names. The whole map is the full fabric: 51 rows, one band per numbered loop, then the connections on no loop."),
        ("Phone", "Rows keep their names on the left; threads stay vertical, so the fabric scrolls down the screen."),
    ],
}


def spec_panel(d):
    rows = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in SPECS[d])
    return f'<div class="spec"><p class="eyebrow">Spec</p><dl>{rows}</dl></div>'


def map_block(d, title, caption):
    if d == "orbit":
        svg = maps_orbit.whole_map(M)
    elif d == "line":
        svg = maps_line.whole_map(M)
    else:
        svg = maps_weave.whole_map(M)
    save_svg(f"{d.title()}-Whole-System-Map", svg)
    return (f'<figure class="mapfig"><figcaption><h4>{esc(title)}</h4><p>{esc(caption)}</p></figcaption>'
            f'<div class="wrap mapwrap" tabindex="0" role="region" aria-label="{esc(title)}, scrolls sideways on a narrow screen">{svg}</div>'
            f'<p class="src">{esc(SRC)} All 51 variables and 118 connections, read by script. Charcoal: connections on a named loop; Stone: the rest.</p></figure>')


# ------------------------------------------------------------------ sections

def baseline():
    return f'''<section id="baseline"><p class="eyebrow">Baseline</p><h2>The current system</h2>
<p>Concepts V2 is the system Dustin likes and the fallback if no direction gets there (G1-11). Its loop catalog draws all 23 loops on one ring, so a two-step loop and a four-step loop look alike and the plate reads as one ring repeated. Its R8 card is the drawing Dustin singled out: two boxes, a step named in words, a return line underneath. Both came before Gate 1, so they still use board-written short names and the plain grade words ("some evidence") that Gate 1 replaced with V7's words (M2).</p>
<div class="basegrid">
 <figure><img src="../research/chat-references/20261028_Ref-Atlas-Loop-Catalog-Current.png" width="1579" height="1587" alt="The current loop catalog from Concepts V2: 23 loops, each drawn on the same ring with ID circles, grouped by area A to D"><figcaption>Current loop catalog, Concepts V2 (Dustin's reference image, October 28). The same ring 20 times; three sketched loops left out.</figcaption></figure>
 <figure><img src="../research/chat-references/20261028_Ref-Atlas-Loop-R8-Concept-08.webp" width="2000" height="1333" alt="Concept 08 loop card for R8: Housing scarcity and Owner home equity as boxes, a forward arrow, and a red return line marking where reform R-30 enters"><figcaption>The R8 card Dustin likes, Concept 08. Built on an earlier model: its remedy grade reads "Well supported", where V7 grades R-30's remedy plausible.</figcaption></figure>
 <figure><img src="phase-1/systems/20261021_Concept-07-Loop-Card.jpg" width="720" height="489" alt="Concept 07 loop card for R10 with four boxes in a row and a return line"><figcaption>Concept 07 Loop Card, the Gate 1 base (M5).</figcaption></figure>
 <figure><img src="phase-1/systems/20261021_Concept-09-Circuit.jpg" width="720" height="563" alt="Concept 09 Circuit: five area cards wired together left to right"><figcaption>Concept 09 Circuit, the current whole-system view (M5).</figcaption></figure>
</div>
<div class="twocol"><div class="panel s-newsprint"><h3>What it does well</h3><p>One quiet vocabulary across every view. The read-aloud sentence. The return line, which shows in one glance that a loop comes back. Area cards on the circuit that a newcomer can name.</p></div>
<div class="panel s-newsprint"><h3>What this pass has to beat</h3><p>A catalog where every loop looks the same, so the page cannot show which loops are long, slow or uncertain. A whole-system map that groups wires by area, so no single connection can be followed. Grade words and short names that predate Gate 1.</p></div></div>
</section>'''


def brief():
    c = M["generated"]["counts"]
    nloop = sum(1 for k, l in M["links"].items() if l["loops"])
    return f'''<section id="brief"><p class="eyebrow">First principles</p><h2>Who reads a systems map, and what they need in ten seconds</h2>
<div class="twocol">
<div><h3>The reader</h3><p>A first-time reader anywhere in the country, of any party, who came for one rule that touches their week: a rent notice, a primary ballot, a power bill. They have never seen a causal loop diagram. They will give a figure ten seconds before deciding whether it is for them.</p>
<h3>What each view must show in ten seconds</h3><ol>
<li>Whether the loop feeds itself or pushes back.</li><li>Which step is weakest, meaning the least certain.</li><li>Where a reform can act.</li><li>How slowly it turns.</li></ol>
<p>The model never adds reform effects into a score or estimates how strong a whole loop is, so no view may suggest either.</p></div>
<div><h3>The four views</h3><ol>
<li><b>Loop catalog:</b> all 23 loops at once, each a miniature of its own card.</li>
<li><b>Loop card:</b> one loop in full. R8 is the worked example.</li>
<li><b>Whole-system map:</b> {c["variables"]} variables and {c["connections"]} connections, for orientation.</li>
<li><b>Reform view:</b> one reform's targets, red where it acts.</li></ol>
<h3>What the data holds</h3><p>{len(LP)} loops: {sum(1 for l in LP.values() if l["n"] == 2)} of two steps, {sum(1 for l in LP.values() if l["n"] == 3)} of three, {sum(1 for l in LP.values() if l["n"] == 4)} of four. {sum(1 for l in LP.values() if l["type"] == "R")} reinforcing, {sum(1 for l in LP.values() if l["type"] == "B")} balancing. Every step carries a sign, a type, a delay class and an evidence grade. {nloop} of the 118 connections sit on a named loop.</p>
<h3>Quirks the drawings work around</h3><ul>
<li>Three loops (B2, B3, R9) have no numbered chain, and two (R2, R16) close through a hypothesized step. Each says so in words, and sketched steps take the hollow line.</li>
<li>B2 to B5 name both a variable and a loop, so every loop ID sits in a typed chip (M3) and variables never do.</li>
<li>Grades are spelled several ways (V7.1 issue 1). The drawings read <span class="code">links[].evidence</span> only and print V7's words.</li>
<li>Delay and effect codes share S, M and L (issue 22), so no bare letter appears outside a data table.</li>
<li>V7 never defines its <span class="code">spine</span> flag, so no drawing encodes it.</li>
<li>Loops share connections: L42 sits on three. The fabric weaves a shared connection into each loop's band and marks the copies.</li></ul></div></div>
</section>'''


def explorations():
    cards = []
    for fam, title, fn, verdict, why in X.FAMILIES:
        svg = save_svg(f"Exploration-{title.replace(' and ', ' ').replace(',', '').title().replace(' ', '-')}", fn(M))
        tagc = "best" if verdict == "kept" else "orig"
        cards.append(f'<figure class="exp"><div class="expfig wrap" tabindex="0" role="region" aria-label="{esc(title)} sketch">{svg}</div><figcaption><p class="exph"><span class="tag {tagc}">{"Kept" if verdict == "kept" else "Fell away"}</span> {esc(title)}</p><p>{esc(why)}</p></figcaption></figure>')
    return f'''<section id="explore"><p class="eyebrow">Explore widely, then choose</p><h2>Seven form families on real loops</h2>
<p>Each sketch is drawn by script from V7, mostly on Loop R8 (two slow, well-supported steps) and Loop R10 (four steps, from documented to plausible). The research brief (<span class="code">work/research/20261028_Systems-Map-References.md</span>) shaped the choice: fixed positions and focus with context beat force layouts, a Sankey cannot carry a cycle, and bundles hide which line goes where.</p>
<div class="expgrid">{"".join(cards)}</div></section>'''


def direction_section(d, num, name, why, map_title, map_caption):
    return f'''<section id="dir-{d}"><p class="eyebrow">Direction {num}</p><h2>{esc(name)}</h2>
<p class="lede">{esc(why)}</p>
{spec_panel(d)}
<h3 class="vh">Loop catalog: all 23 loops, each drawn from its own steps</h3>
<p class="cap">Catalog view, Newsprint, ink only. The catalog names no single reform, so it carries no working red (Rule 05.3); ink pointers show where each loop's own reforms act. Groups follow the area holding most of a loop's variables, with ties going to the area first in V7's order.</p>
{catalog(d)}
<h3 class="vh">Loop card: R8 at full size</h3>
<p class="cap">The R8 miniature above is this drawing at a smaller {"radius" if d == "orbit" else "pitch"}. The card sits on White: Pillar Red on White measures 3.99:1, above the 3:1 floor for informative graphics, while on Newsprint it measures 2.96:1.</p>
{r8_card(d)}
<h3 class="vh">Whole-system map</h3>
{map_block(d, map_title, map_caption)}
</section>'''


def reform_view():
    rid = "R-01"
    r = M["reforms"][rid]
    fab = save_svg("Recommended-Reform-View-R-01-Fabric", maps_weave.whole_map(M, highlight_reform=rid, bg=D.WHITE))
    minis = []
    for lid in r["loops"]:
        lp = LP[lid]
        inside = {t for t in r["targets"] if t in ({s["id"] for s in lp["steps"]} | {s["code"] for s in lp["stations"]})}
        svg = save_svg(f"Recommended-Reform-View-R-01-Loop-{lid}", maps_orbit.mini(lp, red_targets=inside, bg=D.WHITE, only_reform=rid).replace(
            'data-view="orbit-mini"', f'data-view="orbit-mini" data-reform="{rid}"', 1))
        note = (f"{rid} acts on " + ", ".join(sorted(inside)) + " in this loop.") if inside else (
            f"V7 lists this loop as touched by {rid}, and none of {rid}'s targets sits on it. It shares C3 with Loop R10, where {rid} acts on L25, the step into C3.")
        minis.append(f'<article class="mc white" data-loop="{lid}"><div class="mchead">{chip("Loop", lid)}{kind_badge(lp["type"])}<span class="mck">{esc(lp["kind_word"])}</span></div>'
                     f'<h4>{esc(lp["title"])}</h4><div class="mcfig">{svg}</div><p class="mcf">{esc(note)}</p></article>')
    eff_rows = "".join(f'<tr><th scope="row">{esc(M["families"][k])}</th><td>{pips_svg(v)}</td><td>{esc(tm(v))} ({esc(M["effect_codes"].get(v, v))})</td></tr>' for k, v in r["effects"].items())
    route_rows = "".join(
        f'<tr><td>{chip("Route", x["route"])}</td><td>{esc(M["route_names"][x["route"]])}: {esc(x["who"])}</td><td>{esc(x["feasibility"])}</td>'
        f'<td>{esc(D_long(x["checked"])) if x["checked"] else "no check date in V7"}</td></tr>' for x in r["routes"])
    targets = "; ".join(f'{t}, {M["links"][t]["name"] if t in M["links"] else M["nodes"][t]["title"]}' for t in r["targets"])
    return f'''<div class="reformview" id="reform-view"><p class="eyebrow">Reform view, recommended direction</p>
<h3>{chip("Reform", rid)} {esc(r["title"])}</h3>
<p class="deck">Where it acts: {esc(targets)}. Red marks these three targets and nothing else (Rule 05.3: one job, several marks). The headline names no total, because V7 never adds effects into one score.</p>
<div class="rvgrid">{"".join(minis)}</div>
<div class="twocol"><div class="wrap" tabindex="0" role="region" aria-label="Expected effects of {rid}"><table class="eff"><caption>Expected effect by outcome family. Confidence, in V7's words: "{esc(r["effects_confidence"])}"</caption><thead><tr><th scope="col">Outcome family</th><th scope="col">Mark</th><th scope="col">V7 value</th></tr></thead><tbody>{eff_rows}</tbody></table></div>
<div class="wrap" tabindex="0" role="region" aria-label="Routes for {rid}"><table class="eff"><caption>Routes to change. Remedy evidence: {grade_word(r["remedy_grade"])}; problem evidence: {grade_word(r["problem_grade"])}</caption><thead><tr><th scope="col">Route</th><th scope="col">Who acts</th><th scope="col">Feasibility</th><th scope="col">Checked</th></tr></thead><tbody>{route_rows}</tbody></table></div></div>
<figure class="mapfig"><figcaption><h4>{rid} on the whole system</h4><p>The fabric on White with {rid}'s three targets in red: the C2 row and the L08 and L25 threads in Loop R10's band. Every other mark keeps its ink.</p></figcaption>
<div class="wrap mapwrap" tabindex="0" role="region" aria-label="Reform R-01 on the fabric, scrolls sideways on a narrow screen">{fab}</div>
<p class="src">{esc(SRC)} Reform R-01 targets, loops, effects and routes read by script.</p></figure></div>'''


RUBRIC = [
    ("Current system (Concepts V2)", [4, 4, 4, 3, 3, 3], "Fine drawing and one calm vocabulary. The uniform catalog hides structure; pre-Gate 1 grade words and board-written short names; not rechecked at 390 px in this pass."),
    ("Direction 1, Orbit, as built", [4, 3, 4, 4, 5, 4], "The strongest catalog and an elegant card. The ring map shows the story (returns cross the middle) and stays busy along the rim: Clarity 3."),
    ("Direction 2, Line", [4, 4, 4, 4, 5, 4], "The most readable strip and card, closest to the R8 card Dustin likes. Least distinct from the current system, and its arc map fans out at the hub variables."),
    ("Direction 3, Weave", [4, 3, 3, 4, 5, 4], "The calmest, most legible whole map, and the only one with no crossings at all. Its miniatures read as notation before they read as loops."),
    ("Recommended: Orbit loops with the fabric map", [4, 4, 4, 4, 5, 4], "Orbit's catalog and cards with Weave's fabric as the whole-system map. Every criterion at 4 or above; the fabric needs a one-line reading guide and a guided first loop."),
]
CRIT = ["Craft", "Clarity", "Brand fidelity", "Usefulness", "Evidence honesty", "Accessibility"]


def recommendation():
    head = "".join(f'<th scope="col">{c}</th>' for c in CRIT)
    rows = "".join(f'<tr><th scope="row">{esc(n)}</th>' + "".join(f"<td>{v}</td>" for v in s) + f"<td>{esc(why)}</td></tr>" for n, s, why in RUBRIC)
    phone_cat = "20261028_Phone-Loop-Catalog"
    phone_card = "20261028_Phone-R8-Loop-Card"
    return f'''<section id="recommend"><p class="eyebrow">Recommendation</p><h2>Orbit for the loops, the fabric for the whole system</h2>
<p class="lede">Orbit is the direction that gets there. It answers the ask exactly: on the catalog, R8 is a small copy of the R8 card, and the page holds 23 loops that each look like themselves, with the slow ones round and the fast ones thin. Its ring map is the one weak view, so the recommendation takes the fabric from Direction 3 as the whole-system map. Both use the same Gate 1 marks, so the reader learns one vocabulary.</p>
<div class="wrap" tabindex="0" role="region" aria-label="Rubric scores"><table class="rubric"><caption>Rubric, Master Brief V2 section 6, scored 1 to 5 by the studio (a design judgment); ship threshold 4 on every criterion</caption><thead><tr><th scope="col">Option</th>{head}<th scope="col">Reason</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="twocol"><div class="panel s-newsprint"><h3>What it costs</h3><ul>
<li>Four new marks need Dustin's approval beside M1 to M4, which stay as approved: the delay bow, the sign label at its smallest, the reform pointer and the loop-kind arrow.</li>
<li>Readers learn one new sentence: "the slower the step, the wider it bows." The ticks still carry delay, so the bow adds a second channel and replaces none.</li>
<li>It gives up the research brief's first idea, one identical ring for every loop, in favor of Dustin's ask for loops that look different.</li>
<li>The fabric reads as notation at first sight. It needs its reading line, a guided first loop (R8), and focus with context in the live atlas.</li>
<li>Build: the atlas renderer needs two computed layouts (orbit geometry and the fabric order), both generated from V7 with no hand placement, so upkeep stays low.</li></ul></div>
<div class="panel s-newsprint"><h3>What it keeps from the current system</h3><ul><li>The read-aloud sentence on every card.</li><li>The return idea: on the fabric, a loop's band shows it leaving a row and coming back.</li><li>V7's line code, the record square, the hollow line, the ticks, the typed chips and the effect pips, unchanged.</li><li>Red only where one reform acts, on White.</li></ul></div></div>
{reform_view()}
<div class="phones" id="phone"><p class="eyebrow">Phone layouts at 390 px</p><h3>The catalog and the R8 card on a phone</h3>
<p>Each page is a real 390 px layout, captured at that width. Open the pages themselves to scroll them.</p>
<div class="phonegrid">
<figure><div class="wrap phonewrap" tabindex="0" role="region" aria-label="Phone catalog capture"><img src="{REL}{phone_cat}.png" width="390" height="1700" alt="Phone layout of the loop catalog at 390 px: one loop per row, the orbit miniature beside the loop's chip, title and facts"></div><figcaption><a href="{REL}{phone_cat}.html">Open the phone catalog page</a>. First screens shown.</figcaption></figure>
<figure><div class="wrap phonewrap" tabindex="0" role="region" aria-label="Phone R8 card capture"><img src="{REL}{phone_card}.png" width="390" height="1700" alt="Phone layout of the R8 loop card at 390 px: chip and title, the orbit drawing with red at L39 and A5, then the two steps as a numbered list"></div><figcaption><a href="{REL}{phone_card}.html">Open the phone R8 card page</a>. First screens shown.</figcaption></figure>
</div></div>
</section>'''


def checks():
    v = json.loads(VERIFY.read_text()) if VERIFY.exists() else None
    c = json.loads(CHECK.read_text()) if CHECK.exists() else None
    items = []
    if v:
        items += [f"<li>{esc(s)}</li>" for s in v["summary"]]
    else:
        items.append("<li>Data verification has not run yet for this build.</li>")
    if c:
        items += [f"<li>{esc(s)}</li>" for s in c["summary"]]
    else:
        items.append("<li>Rendered checks have not run yet for this build.</li>")
    nt = "".join(f"<li>{esc(s)}</li>" for s in (c or {}).get("not_checked", []))
    return f'''<section id="checks"><p class="eyebrow">How this board was checked</p><h2>Checks</h2>
<div class="twocol"><div><h3>Tested</h3><ul>{"".join(items)}</ul></div><div><h3>Not tested</h3><ul>{nt or "<li>See the notes file.</li>"}
<li>Whether first-time readers decode the bow, the pointer and the fabric as intended. That needs reader tests.</li></ul></div></div></section>'''


DECISIONS = [
    ("Which direction", "Orbit loops with the fabric map; Orbit with its own ring map; Line; Weave; the current system (G1-11 fallback)",
     "Orbit loops with the fabric map", "It answers the catalog ask, scores 4 or above on every criterion, and keeps M1 to M4 as approved."),
    ("The delay bow, a second delay channel beside the ticks", "Adopt; ticks only",
     "Adopt", "It is what makes the 23 miniatures differ, and it says 'slow' without a number."),
    ("Three new marks: the sign label at its smallest, the reform pointer, the loop-kind arrow", "Adopt all three; adopt some; keep the Gate 1 set only",
     "Adopt all three", "Each solves a ten-second task at catalog size where the Gate 1 labels do not fit."),
    ("Red on the catalog", "None, ink pointers only; a reform filter that turns one reform's targets red",
     "None by default, the filter in the live atlas", "The catalog names no single reform, so under Rule 05.3 it carries no working red until a reader picks one."),
    ("The surface for views that carry red", "White; Newsprint with a Charcoal edge on red",
     "White", "Pillar Red on Newsprint measures 2.96:1, and an edged red line looks like the hollow line for sketched steps."),
    ("The weakest-step rule", "Lowest V7 rank, ties shown as ties, V7's prose quoted on the card; V7's prose only",
     "Lowest V7 rank, with the prose", "It is computable for every loop, and the card still carries V7's reasons, as for R8's L39."),
]


def decisions():
    rows = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td><b>{esc(c)}</b></td><td>{esc(d)}</td></tr>" for a, b, c, d in DECISIONS)
    return f'''<section id="decide" class="decision"><p class="eyebrow">Decisions for Dustin</p><h2>What you decide</h2>
<div class="wrap" tabindex="0" role="region" aria-label="Decisions for Dustin"><table><thead><tr><th scope="col">Decision</th><th scope="col">Options</th><th scope="col">Studio recommendation</th><th scope="col">Why</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Red on this board follows Rule 05.3, quoted here word for word from D2-01: "{esc(RED_RULE)}" The specimens on this board are specimens, so the board as a whole is not one view; inside each specimen, only one reform's targets take red.</p></section>'''


CSS = """
.board{max-width:1280px}
.lede{font-size:1.125rem;max-width:72ch}
.code{font-family:ui-monospace,Menlo,monospace;font-size:.875rem}
.twocol{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px;margin-top:16px}
.chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 var(--body);vertical-align:middle;margin-right:6px}
.chip .k{background:var(--charcoal);color:var(--newsprint);padding:6px 7px 0;letter-spacing:.02em}
.chip .c{border:1.5px solid var(--charcoal);padding:5px 7px 0;font-size:14px;font-weight:700;background:transparent}
.kb{vertical-align:middle;margin-right:6px}
.tag.best{background:var(--charcoal);color:var(--newsprint)} .tag.orig{background:transparent}
svg{max-width:none}
.wrap{overflow-x:auto;max-width:100%}
.wrap:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--verdigris);outline-offset:2px}
.cgroup{margin-top:20px}
.cgh{font:800 1.0625rem/1.3 var(--display);border-bottom:2px solid var(--charcoal);padding-bottom:6px;margin:0 0 12px}
.cn{font:400 .875rem var(--body);color:var(--muted)}
.cgrid{display:grid;gap:16px 16px}
.c-orbit{grid-template-columns:repeat(auto-fill,minmax(236px,1fr))}
.c-line,.c-weave{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.mc{border-top:1px solid var(--charcoal);padding-top:8px;min-width:0}
.mc.white{background:var(--white);padding:10px;border:1px solid var(--rule)}
.mchead{display:flex;align-items:center;flex-wrap:wrap;gap:2px}
.mck{font:600 .8125rem/1.3 var(--body)}
.mc h4{font:600 .9375rem/1.35 var(--body);margin:6px 0 2px;letter-spacing:0}
.mcflag{font:italic 400 .8125rem/1.35 var(--body);color:var(--muted);margin:0}
.mcfig svg{display:block;margin:0 auto}
.mcf{font-size:.8125rem;line-height:1.45;color:var(--muted);margin:2px 0 0}
.vh{margin:36px 0 6px;font-size:1.25rem}
.spec{background:var(--surface);border:1px solid var(--rule);padding:16px 18px;margin-top:16px}
.spec dl{display:grid;grid-template-columns:minmax(120px,170px) 1fr;gap:6px 18px;margin:8px 0 0}
.spec dt{font-weight:700;font-size:.875rem} .spec dd{margin:0;font-size:.9375rem;max-width:90ch}
@media (max-width:640px){.spec dl{grid-template-columns:1fr}.spec dd{margin-bottom:8px}}
.card{background:var(--white);border:1px solid var(--charcoal);padding:22px;margin-top:10px}
.cardhead h3{font:800 clamp(1.5rem,3vw,2.125rem)/1.1 var(--display);margin:10px 0 8px;letter-spacing:-.02em}
.chiprow{display:flex;align-items:center;flex-wrap:wrap;gap:4px;font:600 .875rem/1.4 var(--body)}
.deck{font-size:1.0625rem;max-width:70ch}
.cardbody{display:grid;gap:20px;margin-top:12px}
.card.side .cardbody{grid-template-columns:minmax(0,760px) minmax(260px,1fr)}
@media (max-width:1100px){.card.side .cardbody{grid-template-columns:1fr}}
.cardfig svg{display:block}
.facts{margin:0}.facts dt{font-weight:700;font-size:.875rem;margin-top:12px}.facts dd{margin:2px 0 0;font-size:.9375rem}
.card.wide .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:4px 24px}
.rblock{border-top:1px solid var(--charcoal);margin-top:18px;padding-top:12px}
.rblock h4{font:800 1.25rem/1.25 var(--display);margin:4px 0 8px}
.redkey{display:inline-block;width:22px;height:4px;background:var(--red);vertical-align:middle}
table.eff{width:auto;min-width:min(100%,520px);margin-top:10px}
table.eff caption,table caption{caption-side:top;text-align:left;font-size:.8125rem;color:var(--muted);padding:4px 0}
.eff td,.eff th{vertical-align:middle}
.pips{display:block}
.eqv{margin-top:12px}.eqv summary{cursor:pointer;font-weight:600}
.src{font-size:.8125rem;color:var(--muted);margin-top:10px}
.mapfig{margin:10px 0 0}.mapfig figcaption h4{font:800 1.0625rem var(--display);margin:0 0 4px}
.mapwrap svg{display:block}
.keygrid{padding:16px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,540px),1fr));gap:14px 32px;border:1px solid var(--rule)}
.krow{display:grid;grid-template-columns:210px 1fr;gap:14px;align-items:center}
.krow p{margin:0;font-size:.875rem}
.kmark{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.ks{font-size:.8125rem;color:var(--muted);margin-right:6px}
@media (max-width:640px){.krow{grid-template-columns:1fr}}
.basegrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:20px;margin-top:16px}
.basegrid figure{margin:0}.basegrid img{width:100%;height:auto;display:block;border:1px solid var(--rule)}
.basegrid figcaption{font-size:.8125rem;color:var(--muted);margin-top:6px}
.expgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,560px),1fr));gap:20px;margin-top:16px}
.exp{margin:0;border-top:1px solid var(--charcoal);padding-top:8px}
.expfig{overflow-x:auto}.expfig svg{display:block}
.exph{font-weight:700;margin:6px 0 4px}
.exp figcaption p{font-size:.9375rem}
.rubric td,.rubric th{font-size:.875rem}
.rubric td:not(:last-child){text-align:center;font-variant-numeric:tabular-nums;font-weight:700}
.reformview{background:var(--white);border:1px solid var(--charcoal);padding:22px;margin-top:28px}
.reformview h3{font:800 1.5rem/1.2 var(--display);margin:6px 0 8px}
.rvgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(256px,1fr));gap:16px;margin:12px 0}
.phones{margin-top:32px}
.phonegrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,390px),1fr));gap:24px;margin-top:12px}
.phonegrid figure{margin:0;min-width:0}
.phonewrap{max-height:1100px;overflow-y:auto;border:1px solid var(--charcoal);width:fit-content;max-width:100%}
.phonewrap img{display:block}
.decision a{color:inherit}
.decision table th,.decision table td{border-bottom-color:var(--dimnews,#A3A19C)}
.decision th{color:var(--newsprint)}
.toc{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:16px;font-size:.9375rem}
.toc a{color:var(--fg)}
.sumbox{background:var(--surface);border:1px solid var(--rule);padding:16px 18px;margin-top:20px}
"""


def board():
    sections = [
        ("baseline", "Current system"), ("brief", "First principles"), ("explore", "Explorations"), ("key", "Shared marks"),
        ("dir-orbit", "1 Orbit"), ("dir-line", "2 Line"), ("dir-weave", "3 Weave"), ("recommend", "Recommendation"),
        ("reform-view", "Reform view"), ("phone", "Phone"), ("checks", "Checks"), ("decide", "Decisions")]
    toc = "".join(f'<a href="#{a}">{esc(b)}</a>' for a, b in sections)
    key = f'''<section id="key"><p class="eyebrow">Shared marks</p><h2>One vocabulary under all three directions</h2>
<p>Every direction draws with the Gate 1 marks (M1 to M4) exactly as approved: V7's line code with the record square and the hollow line, V7's grade words with their glosses, typed chips, the effect pips and the delay ticks. Four studio additions appear below them, each flagged in the decisions: the delay bow (Orbit only), the sign label at its smallest, the reform pointer and the loop-kind arrow. No drawing contains the ampersand or calls a shared variable a hinge, so the five separation rules hold.</p>
{key_panel()}</section>'''
    dirs = [
        direction_section("orbit", 1, "Orbit: each loop draws its own shape",
                          "A loop is a closed figure that comes back around. Each step bows outward by its delay, so a slow loop is round and a fast one is thin, and the catalog becomes 23 different drawings that a reader can tell apart at a glance.",
                          "The whole system on one turning ring",
                          "All 51 variables on one ring, grouped by area clockwise in the order effects mostly travel (A to E), with technology and the economy closing the circle and the drivers at the top. Each connection bends to its left, more when slower: the orbit rule at system scale. Forward links hug the rim; the steps that come back cross the middle."),
        direction_section("line", 2, "Line: ride each loop out and back",
                          "A loop is a line with stations in V7's chain order and a return line underneath, the strip map above a train door. It reads left to right like the loop's own sentence, and it grows from the R8 card Dustin singled out.",
                          "The whole system on one line",
                          "All 51 variables on one line: outside drivers, technology and the economy on the left, then the core areas A to E. A connection that runs to the right arcs over the line; one that runs back arcs under it, so most steps that close a loop sit below."),
        direction_section("weave", 3, "Weave: each loop is a stitch in the fabric",
                          "Rows are variables and vertical threads are connections, after BioFabric. A loop is a run of threads that leaves a row and comes back to it, so every loop is a small stitch, and the whole system becomes a fabric with no crossing lines at all.",
                          "The whole system as a fabric",
                          "All 51 variables as rows in V7's system order and all 118 connections as vertical threads. Loops sit side by side on the left, one band per numbered loop; a connection on more than one loop is woven into each band. The connections on no loop follow by layer."),
    ]
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Systems Map Directions</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:ital,wght@0,400;0,600;0,700;1,400&family=Lora:ital@1&display=swap">
<link rel="stylesheet" href="board-base.css"><style>{CSS}</style></head>
<body><main class="board">
<p class="eyebrow">Phase 2 · Systems maps · October 28, 2026 · Data visualization and systems lead</p>
<h1>Systems map directions</h1>
<p class="lede">Dustin asked whether the studio can make a systems map that is distinct, visual, intuitive and beautiful, starting from scratch, with the current system kept if nothing gets there (G1-11). He asked one thing in particular: on the loop catalog, each loop should be a small copy of its own card, so R8 there is a miniature of the R8 card. This board shows the current system, seven explorations, three directions built from Atlas V7 by script, and a recommendation. Scope is a spec and specimens (G1-08); the working atlas file is untouched.</p>
<div class="sumbox"><p><b>Recommendation:</b> Orbit for the catalog and the loop cards, with Direction 3's fabric as the whole-system map. Every drawn ID, sign, grade, delay and reform target was checked against V7 by script.</p></div>
<nav class="toc" aria-label="Board sections">{toc}</nav>
{baseline()}{brief()}{explorations()}{key}{"".join(dirs)}{recommendation()}{checks()}{decisions()}
<p class="src">{esc(SRC)} Built by work/build/scripts/phase-2/build_maps_board.py. Drawings in work/boards/phase-2/maps/. Concept and reference images are Dustin's and the studio's earlier boards, shown for comparison.</p>
</main></body></html>'''


# ------------------------------------------------------------------ phone pages

PHONE_CSS = """
:root{--bg:#DCD9D2;--fg:#121212;--muted:#45494F;--rule:#5D636D;--white:#FFFFFF;--red:#E63946;--charcoal:#121212;--newsprint:#DCD9D2;--verdigris:#4A7C74}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:400 15px/1.5 Inter,Arial,sans-serif}
main{padding:20px 16px 48px;max-width:430px;margin:0 auto}
h1{font:800 28px/1.08 'Inter Tight',Arial,sans-serif;letter-spacing:-.02em;margin:6px 0 8px}
.eyebrow{font:700 13px/1.4 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.chip{display:inline-flex;height:26px;font:600 13px/1 Inter;vertical-align:middle;margin-right:6px}
.chip .k{background:var(--charcoal);color:var(--newsprint);padding:6px 7px 0}.chip .c{border:1.5px solid var(--charcoal);padding:5px 7px 0;font-size:14px;font-weight:700}
.kb{vertical-align:middle}
h2{font:800 17px/1.3 'Inter Tight';border-bottom:2px solid var(--charcoal);padding-bottom:6px;margin:26px 0 4px}
.row{display:grid;grid-template-columns:132px 1fr;gap:10px;border-top:1px solid var(--charcoal);padding:10px 0}
.row svg{display:block}
.row h3{font:600 14px/1.35 Inter;margin:4px 0}
.row p{font-size:13px;line-height:1.45;color:var(--muted);margin:2px 0 0}
.top{display:flex;align-items:center;flex-wrap:wrap;gap:2px;font:600 13px Inter}
.card{background:var(--white);border:1px solid var(--charcoal);padding:12px;margin-top:10px}
.card h1{font-size:25px}
.deck{font-size:15px}
.fig svg{display:block;margin:0 auto;max-width:100%;height:auto}
ol.steps{padding-left:0;list-style:none;margin:8px 0}
ol.steps li{border-top:1px solid var(--rule);padding:8px 0}
.red{display:inline-block;width:18px;height:4px;background:var(--red);vertical-align:middle;margin-right:4px}
dl dt{font-weight:700;font-size:13px;margin-top:10px}dl dd{margin:2px 0 0;font-size:14px}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:6px 4px;border-bottom:1px solid var(--rule);vertical-align:middle}
caption{caption-side:top;text-align:left;font-size:13px;color:var(--muted);padding:4px 0}
.src{font-size:13px;color:var(--muted)}
a{color:var(--fg)}
"""


def phone_head(title):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:ital,wght@0,400;0,600;0,700;1,400&display=swap">'
            f'<style>{PHONE_CSS}</style></head><body><main>')


def phone_catalog():
    out = [phone_head("Phone Loop Catalog"), '<p class="eyebrow">Orbit · loop catalog · 390 px</p><h1>Twenty-three loops</h1>',
           '<p>Each drawing is the loop itself. The slower a step, the wider it bows. A pointer marks where a reform listed on the loop acts, and a dark sign label marks the weakest step.</p>']
    for g in M["groups"]:
        title = g["title"] if g["id"] == "SK" else f'{g["id"]}  {g["title"]}'
        out.append(f'<h2>{esc(title)}</h2>')
        for lid in g["loops"]:
            lp = LP[lid]
            r0 = {2: 40, 3: 41, 4: 42}[lp["n"]]
            svg = maps_orbit.mini(lp, w=132, h=150, r0=r0, weakest_style="pill").replace('data-view="orbit-mini"', 'data-view="orbit-mini-phone"', 1)
            save_svg(f"Phone-Orbit-Mini-{lid}", svg)
            out.append(f'<article class="row" data-loop="{lid}"><div>{svg}</div><div><div class="top">{chip("Loop", lid)}{kind_badge(lp["type"], 24)}{esc(lp["kind_word"])}</div>'
                       f'<h3>{esc(lp["title"])}</h3><p>One turn: {esc(lp["delay_word"])}. {esc(weakest_text(lp))}. {esc(targets_text(lp))}.</p></div></article>')
    out.append(f'<p class="src">{esc(SRC)}</p></main></body></html>')
    path = ASSETS / "20261028_Phone-Loop-Catalog.html"
    path.write_text("".join(out), encoding="utf-8")
    WRITTEN.append(path)


def phone_card():
    lp = LP["R8"]
    r = M["reforms"]["R-30"]
    svg = save_svg("Phone-Orbit-Card-R8", maps_orbit.mini(lp, w=326, h=310, r0=104, red_targets={"L39", "A5"}, bg=D.WHITE, only_reform="R-30").replace(
        'data-view="orbit-mini"', 'data-view="orbit-card-phone" data-reform="R-30"', 1))
    steps = "".join(
        f'<li>{chip("Connection", s["id"])}{("<span class=red aria-hidden=true></span><b>R-30 acts here.</b> ") if s["id"] in r["targets"] else ""}'
        f'<b>{esc(s["name"])}.</b> {esc(s["from"])} to {esc(s["to"])}, sign {D.sign_glyph(s["polarity"])}. {esc(grade_word(s["evidence"]))}, {esc(D.DELAY_WORD[s["delay"]])}.</li>'
        for s in lp["steps"])
    facts = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in facts_r8(lp))
    eff = "".join(f'<tr><th scope="row">{esc(M["families"][k])}</th><td>{pips_svg(v, 120, 24)}</td><td>{esc(tm(v))}</td></tr>' for k, v in r["effects"].items())
    routes = "".join(f'<tr><td>{esc(x["route"])}</td><td>{esc(x["who"])}</td><td>{esc(x["feasibility"])}</td></tr>' for x in r["routes"])
    html_ = (phone_head("Phone R8 Loop Card") + f'''<p class="eyebrow">Orbit · loop card · 390 px</p>
<article class="card"><div class="top">{chip("Loop", "R8")}{kind_badge("R", 24)}Reinforcing: feeds itself</div>
<h1>{esc(lp["title"])}</h1><p class="deck">Read it aloud: {esc(lp["how_to_read"])}</p>
<div class="fig">{svg}</div>
<p><span class="red" aria-hidden="true"></span>Red marks where reform R-30 acts: the step L39 and the variable A5, Housing scarcity.</p>
<ol class="steps">{steps}</ol>
<dl>{facts}</dl>
<h2>{chip("Reform", "R-30")} {esc(r["title"])}</h2>
<p>It also acts outside this loop on LE17, {esc(M["links"]["LE17"]["name"])}. Remedy evidence: {grade_word(r["remedy_grade"])}.</p>
<table><caption>Expected effect, ordinal, never added up</caption><tbody>{eff}</tbody></table>
<table><caption>Routes to change; V7 gives these routes no check date</caption><thead><tr><th scope="col">Route</th><th scope="col">Who</th><th scope="col">Feasibility</th></tr></thead><tbody>{routes}</tbody></table>
<p class="src">{esc(SRC)} Loop R8; reform R-30.</p></article></main></body></html>''')
    path = ASSETS / "20261028_Phone-R8-Loop-Card.html"
    path.write_text(html_, encoding="utf-8")
    WRITTEN.append(path)


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "20261028_Maps-Model-Data.json").write_text(json.dumps(M, indent=1, ensure_ascii=False), encoding="utf-8")
    page = board()
    phone_catalog()
    phone_card()
    BOARD.write_text(page, encoding="utf-8")
    print("board", BOARD.relative_to(ROOT), f"{len(page) / 1e6:.2f} MB;", len(WRITTEN), "asset files")
