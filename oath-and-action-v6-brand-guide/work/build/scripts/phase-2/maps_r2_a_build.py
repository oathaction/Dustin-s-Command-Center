#!/usr/bin/env python3
"""Build Direction A, Field Guide: five specimen pages and the board that shows them.

Run:  python3 -I work/build/scripts/phase-2/maps_r2_a_build.py
Then: python3 -I work/build/scripts/phase-2/maps_r2_a_verify.py
      node work/build/scripts/phase-2/maps_r2_a_check.js        (captures the 390 px and grayscale proofs, then audits)
      python3 -I work/build/scripts/phase-2/maps_r2_a_build.py   (again, so the board prints the results)
Reads  work/extract/atlas-v7-data.json through maps_model.py (no V7 value is typed by hand)
Writes work/boards/20261028_Map-Direction-A-Field-Guide.html
       work/boards/phase-2/maps-r2/a/: the drawings (SVG), the five standalone pages (HTML), check data (JSON)
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import maps_draw as D  # noqa: E402
import maps_model as MM  # noqa: E402
import maps_r2_a_circuit as C  # noqa: E402
import maps_r2_a_fg as FG  # noqa: E402
import maps_r2_a_text as TX  # noqa: E402

ROOT = HERE.parents[3]
ASSETS = ROOT / "work/boards/phase-2/maps-r2/a"
BOARD = ROOT / "work/boards/20261028_Map-Direction-A-Field-Guide.html"
REL = "phase-2/maps-r2/a/"
VERIFY = ASSETS / "20261028_A-Verify-Results.json"
CHECK = ASSETS / "20261028_A-Check-Results.json"
V7 = json.loads((ROOT / "work/extract/atlas-v7-data.json").read_text(encoding="utf-8"))
def esc(text, quote=True):
    """Escape for HTML and set apostrophes as typographic ones (owners' becomes owners’). Display only."""
    t = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)]|$)", "\u2019", str(text))
    return html.escape(t, quote=quote)
M = MM.build_model()
LP = M["loops"]
SRC = "Source: Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026."
WRITTEN = []
DOT = "·"

# Headlines written by the studio from V7's how_to_read, for the editor's review (CD brief: the editor writes them).
# Each verb matches the loop's least certain grade (Master Brief section 15): a plausible step takes "can" or "may".
HEADLINES = {
    "R8": "Scarce homes build owners’ equity, which keeps homes scarce",
    "R10": "Safe seats can let officeholders write the rules that keep seats safe",
    "R-01": "Where all-party primaries with ranked general elections may act",
}
LEADS = {}  # filled by plate_order


def save(name, svg):
    path = ASSETS / f"20261028_A-{name}.svg"
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg, encoding="utf-8")
    WRITTEN.append(path)
    return svg


def inner(svg):
    body = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]
    return body.split("</title>", 1)[1] if "</title>" in body else body


def nbh(text):
    """Keep reform IDs such as R-06 on one line."""
    return re.sub(r"\bR-(\d\d)\b", "R\u2011\\1", text)


def chip(kind, code):
    return f'<span class="chip"><span class="k">{esc(kind)}</span><span class="c">{esc(code)}</span></span>'


def gw(g):
    return D.GRADE_WORD[g].lower()


def least_certain(lp, short=True):
    if lp["conceptual"]:
        return "Sketched in V7: no numbered steps, so no step carries its own grade."
    if lp["weakest"]:
        ws = [s for s in lp["steps"] if s["id"] in lp["weakest"]]
        ids = [s["id"] for s in ws]
        grades = {gw(s["evidence"]) for s in ws}
        if len(ws) == 1:
            return f"Least certain: {ids[0]}, {gw(ws[0]['evidence'])}."
        joined = ", ".join(ids[:-1]) + " and " + ids[-1]
        if len(grades) == 1:
            return f"Least certain: {joined}, {'both' if len(ws) == 2 else 'all'} {grades.pop()}."
        return "Least certain: " + " and ".join(f'{s["id"]} ({gw(s["evidence"])})' for s in ws) + "."
    grades = sorted({gw(s["evidence"]) for s in lp["steps"]})
    if len(grades) == 1:
        g = "a hypothesis" if grades[0] == "hypothesis" else grades[0]
        return f"Least certain: no single step; every step is {g}."
    return f"Least certain: no single step; its steps are {' and '.join(grades)}, which V7 ranks equal."


def caption(lp):
    kind = "Feeds itself." if lp["type"] == "R" else "Pushes back."
    hyp = " Closes through a hypothesized step." if lp["hypothesized"] else ""
    return f'{kind} One turn: {lp["delay_word"]}. {least_certain(lp)}{hyp}'


def v7_sentence(text, word):
    """The clause of V7's evidence summary that names the weak step, with the step it is about."""
    for snt in re.split(r"(?<=\.)\s+", text):
        if word not in snt.lower():
            continue
        for c in [c.strip() for c in snt.split(";")]:
            if word in c.lower():
                ids = re.findall(r"\b(L\d\d|LE\d\d|LT\d\d|LX\d|T\d\d)\b", snt)
                quote = "\u201c" + c.rstrip(".") + ".\u201d"
                if c[0].islower() and ids:
                    return f"on {ids[0]}, {quote}"
                return quote
    return None


# ------------------------------------------------------------------ the catalog page

def plate_order():
    plates = []
    for g in M["groups"]:
        ids = g["loops"]
        if g["id"] == "A":
            lead = "R8"
        elif g["id"] == "SK":
            lead = None
        else:
            # the loop with the most live reforms V7 lists; ties go to the loop first in V7's order
            lead = max(ids, key=lambda k: (len(LP[k]["reforms"]), -M["loop_order"].index(k)))
        rest = [k for k in ids if k != lead]
        span = None
        if lead:
            span = "lead3" if len(rest) % 3 == 0 else "lead2"
        plates.append({"id": g["id"], "title": g["title"], "lead": lead, "rest": rest, "span": span})
        LEADS[g["id"]] = lead
    return plates


def tile(lid, kind="single"):
    lp = LP[lid]
    if kind == "single":
        d_svg, _ = FG.drawing(lp, M, "mini")
        save(f"Mini-{lid}", d_svg)
    else:
        d_svg, _ = FG.drawing(lp, M, "lead")
        save(f"Lead-{lid}", d_svg)
    p_svg = save(f"Mini-Phone-{lid}", FG.phone_mini(lp, M))
    kind_word = lp["kind_word"]
    read = f'<p class="fga-read">“{esc(lp["how_to_read"])}”</p>' if kind != "single" else ""
    cls = {"single": "fga-tile", "lead2": "fga-tile lead lead2", "lead3": "fga-tile lead lead3"}[kind]
    return (f'<article class="{cls}" data-loop="{lid}"><div class="fga-tt">'
            f'<div class="fga-th">{chip("Loop", lid)}<span class="fga-kind">{esc(kind_word)}</span></div>'
            f'<h4>{esc(lp["title"])}</h4>{read}<p class="fga-cap">{esc(caption(lp))}</p></div>'
            f'<div class="fga-fig"><div class="dsk">{d_svg}</div><div class="phn">{p_svg}</div></div></article>')


def teach(view_suffix=""):
    """The catalog head: R8 at full card size with five numbered callouts."""
    lp = LP["R8"]
    svg, meta = FG.drawing(lp, M, "card", reform_id=None, view="fg-head")
    boxes, routes = meta["boxes"], meta["routes"]
    a5, a6 = boxes[0], boxes[1]
    (fx1, fy), (fx2, _) = routes[0][0], routes[0][-1]
    under = routes[1]
    dx, dy, _ = meta["marks"]["L38"]
    pts = {
        1: (a6[0] + a6[2] - 18, a6[1] + 18),
        2: (fx1 + 0.82 * (fx2 - fx1), fy),
        3: (under[2][0] + 0.18 * (under[1][0] - under[2][0]), under[1][1]),
        4: (dx + 24, dy + 24),
        5: (fx1 + 0.28 * (fx2 - fx1), fy),
    }
    marker = "".join(
        f'<g class="mk"><circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{D.INK}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="none" stroke="{D.INK}" stroke-width="1"/>'
        + FG.T(x, y + 5, str(n), 14, 700, D.WHITE, "middle") + "</g>" for n, (x, y) in pts.items())
    body = inner(svg).replace("</svg>", "")
    w, h = meta["w"], meta["h"]
    full = FG.svg_doc(w, h, body + marker, "Loop R8 at full card size with five numbered callouts", "fg-head",
                      ' data-loop="R8" data-direction="field-guide"')
    save("Catalog-Head-R8", full)
    # the phone head: the stacked card with the same five markers
    def ph_markers(g):
        bx = g["boxes"]
        xl = g["xl"]
        a5, a6 = bx[0], bx[1]
        mid = (a5[1] + a5[3] + a6[1]) / 2
        return [f'<g class="mk"><circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{D.INK}"/>' + FG.T(x, y + 4.6, str(n), 13, 700, D.WHITE, "middle") + "</g>"
                for n, (x, y) in {1: (a5[0] + a5[2] - 16, a5[1] + 16), 2: (xl, a6[1] - 22), 3: (10, a6[1] + a6[3] / 2 - 34),
                                  4: (xl - 24, mid), 5: (xl, a5[1] + a5[3] + 30)}.items()]
    ph = FG.phone_drawing(lp, M, None, view="fg-head-phone", markers=ph_markers)
    save("Catalog-Head-R8-Phone", ph)
    items = [
        ("A box is something that can rise or fall", "Its name is V7's. On a card, a line under it says what a higher value means."),
        ("The top line runs forward", "A change in one box changes the next box along the arrow."),
        ("The line underneath comes back", "It carries the last change back to the first box. That return is what makes a loop."),
        ("The sign says which way", "+ means the two move the same way; − means they move opposite ways. A plus is not good news."),
        ("The texture says how sure", "Solid: documented or well supported. Dashed: plausible. Dash-dot: contested. Dotted: a hypothesis."),
    ]

    def samples():
        out = []
        for i, g in enumerate(["well-supported", "plausible", "plausible_contested", "hypothesis"]):
            dash = D.DASH.get(g)
            da = f' stroke-dasharray="{dash}"' if dash else ""
            out.append(f'<svg width="54" height="14" viewBox="0 0 54 14" aria-hidden="true"><path d="M2 7 L52 7" stroke="#DCD9D2" stroke-width="2.5"{da}/></svg>')
        return "".join(out)
    key = "".join(f'<li><span class="n">{n}</span><span><b>{esc(t)}</b> {esc(x)}' + (f'<span class="smp">{samples()}</span>' if n == 5 else "") + "</span></li>"
                  for n, (t, x) in enumerate(items, start=1))
    return (f'<div class="fga-teach"><div class="fga-panel"><div class="dsk">{full}</div><div class="phn">{ph}</div></div>'
            f'<ol class="fga-key" aria-label="How to read a loop card">{key}</ol></div>')


def catalog_page(hl="h2"):
    plates = plate_order()
    n_numbered = sum(1 for l in LP.values() if not l["conceptual"])
    head = (f'<header class="fga-head"><div class="wrapc"><p class="fga-eyebrow">Who Do They Answer To? {DOT} Systems Atlas {DOT} Loop guide</p>'
            f'<{hl} class="fga-display">Twenty-three loops</{hl}>'
            f'<p class="fga-deck">Every loop in the atlas, drawn one way. Learn this card, and you can read the other twenty-two.</p>'
            f'{teach()}</div></header>')
    out = [head]
    for pl in plates:
        if pl["id"] == "SK":
            letter, name = "", "Sketched loops"
            deck = "Three loops V7 describes without a complete numbered chain. Their steps take the hollow line."
        else:
            letter, name = pl["id"], pl["title"]
            deck = next(a["text"] for a in M["areas"] if a["id"] == pl["id"])
        count = len(pl["rest"]) + (1 if pl["lead"] else 0)
        lead_note = f'Lead specimen: Loop {pl["lead"]}' if pl["lead"] else "No lead specimen"
        band = (f'<div class="fga-band"><div class="wrapc fga-bandin">' + (f'<span class="fga-letter" aria-hidden="true">{letter}</span>' if letter else '<span class="fga-letter sk" aria-hidden="true"><svg width="96" height="96" viewBox="0 0 96 96"><circle cx="48" cy="48" r="38" fill="none" stroke="#DCD9D2" stroke-width="12"/><circle cx="48" cy="48" r="38" fill="none" stroke="#121212" stroke-width="5"/></svg></span>')
                + f'<div><h3>{esc(("Area " + letter + ": ") if letter else "")}{esc(name)}</h3><p>{esc(deck)}</p></div>'
                + f'<p class="fga-count"><b>{count}</b> loops<br><span>{esc(lead_note)}</span></p></div></div>')
        tiles = []
        if pl["lead"]:
            tiles.append(tile(pl["lead"], pl["span"]))
        tiles += [tile(k) for k in pl["rest"]]
        out.append(f'<section class="fga-plate" aria-label="{esc(name)}">{band}<div class="wrapc"><div class="fga-grid">{"".join(tiles)}</div></div></section>')
    foot = (f'<div class="wrapc fga-foot"><p>{esc(SRC)} {n_numbered} loops have numbered chains: 11 of two steps, 5 of three and 4 of four; 3 are sketched. '
            f'Names in the boxes are V7’s own chain labels. Plates follow the area holding most of a loop’s variables; each plate’s lead is R8 for area A '
            f'and otherwise the loop with the most live reforms V7 lists.</p></div>')
    return f'<section class="fga fga-catalog">{"".join(out)}{foot}</section>'


# ------------------------------------------------------------------ cards

def rail(lp, rid=None):
    closing = lp["steps"][-1]
    ret_plain = V7["links"][closing["id"]]["plain"] if closing["id"] else None
    kind_h = "Feeds itself" if lp["type"] == "R" else "Pushes back"
    gl = M["glossary"]["Reinforcing loop (R)" if lp["type"] == "R" else "Balancing loop (B)"]
    weak_v7 = v7_sentence(lp["evidence_summary"], "weak")
    w_lead = least_certain(lp).replace("Least certain: ", "")
    w = w_lead[0].upper() + w_lead[1:]
    if weak_v7:
        w += (" V7, " + weak_v7) if weak_v7.startswith("on ") else (" V7: " + weak_v7)
    rows = [
        (kind_h, f"{'Reinforcing' if lp['type'] == 'R' else 'Balancing'} loop. V7: “{gl}”"),
        ("What the return line means", f"{closing['id']}, {closing['name']}. {ret_plain}" if ret_plain else ""),
        ("Least certain step", w),
        ("One turn", f"{lp['delay_word'].capitalize()}. V7 gives a loop the delay of its slowest step."),
        ("Now", f"{lp['direction_word'].capitalize()}. V7 tracks it by “{lp['reference_mode']}”."),
    ]
    return "".join(f'<div class="fga-railsec"><h4>{esc(h)}</h4><p>{esc(t)}</p></div>' for h, t in rows)


def pips(v):
    import build_maps_board
    return build_maps_board.pips_svg(v)


def route_rows(r):
    out = []
    for x in r["routes"]:
        chk = D_long(x["checked"]) if x["checked"] else "no check date in V7"
        out.append(f'<tr><td>{chip("Route", x["route"])}</td><td>{esc(M["route_names"][x["route"]])}: {esc(x["who"])}</td><td>{esc(x["feasibility"])}</td><td>{esc(chk)}</td></tr>')
    return "".join(out)


def phone_lists(r, eff_cap, route_cap):
    """The same rows as the two tables, as lists that read top to bottom on a phone."""
    eff = "".join(f'<li><b>{esc(M["families"][k])}</b><span class="pv">{pips(v)}<span>{esc(tm(v))}'
                  f'{(" (" + esc(M["effect_codes"][v]) + ")") if v in M["effect_codes"] else ""}</span></span></li>' for k, v in r["effects"].items())
    rts = []
    for x in r["routes"]:
        chk = D_long(x["checked"]) if x["checked"] else "no check date in V7"
        rts.append(f'<li>{chip("Route", x["route"])}<b>{esc(M["route_names"][x["route"]])}: {esc(x["who"])}</b>'
                   f'<span>Feasibility, 2026 to 2030: {esc(x["feasibility"])}. Checked: {esc(chk)}.</span></li>')
    return (f'<div class="phn fga-plist"><p class="cap">{eff_cap}</p><ul>{eff}</ul>'
            f'<p class="cap">{route_cap}</p><ul>{"".join(rts)}</ul></div>')


def D_long(iso):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    y, m, d = iso.split("-")
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def tm(s):
    return re.sub(r"(?<![\w])-(?=[SML0])", "−", s)


def reform_block(rid, loop_id):
    r = M["reforms"][rid]
    lp = LP[loop_id]
    els = {s["id"] for s in lp["steps"]} | {s["code"] for s in lp["stations"]}
    inside = [t for t in r["targets"] if t in els]
    outside = [t for t in r["targets"] if t not in els]

    def nm(t):
        return f'{t}, {M["links"][t]["name"]}' if t in M["links"] else f'{t}, {M["nodes"][t]["title"]}'
    others = sorted({o for o, rr in M["reforms"].items() if o != rid and not rr["rejected"] and set(rr["targets"]) & set(inside)})
    also = ""
    if others:
        shared = sorted({t for t in inside for o in others if t in M["reforms"][o]["targets"]})
        also = f' Reform {", ".join(others)} also acts on {", ".join(shared)}; V7 does not list {"it" if len(others) == 1 else "them"} on this loop.'
    eff = "".join(f'<tr><th scope="row">{esc(M["families"][k])}</th><td>{pips(v)}</td><td>{esc(tm(v))}'
                  f'{(" (" + esc(M["effect_codes"][v]) + ")") if v in M["effect_codes"] else ""}</td></tr>' for k, v in r["effects"].items())
    return f'''<section class="fga-reform" aria-label="Where reform {rid} acts">
<p class="fga-eyebrow ink">Where a reform acts</p>
<h3>{chip("Reform", rid)} {esc(r["title"])}</h3>
<p><span class="fga-redkey" aria-hidden="true"></span>{nbh(f"Red marks where {rid} acts in this loop: ")}{esc("; ".join(nm(t) for t in inside))}.{(" It also acts outside this loop on " + esc("; ".join(nm(t) for t in outside)) + ".") if outside else ""}{nbh(esc(also))}</p>
<p>Evidence that the problem exists: <b>{esc(D.GRADE_WORD[r["problem_grade"]])}</b>. Evidence that the remedy works: <b>{esc(D.GRADE_WORD[r["remedy_grade"]])}</b>. Confidence in the effects, in V7’s words: “{esc(r["effects_confidence"])}”.</p>
<div class="dsk"><div class="fga-tables"><div class="fga-tw" tabindex="0" role="region" aria-label="Expected effects of {rid}"><table><caption>Expected effect by outcome family. Ordinal marks, never added up.</caption>
<thead><tr><th scope="col">Outcome family</th><th scope="col">Mark</th><th scope="col">V7 value</th></tr></thead><tbody>{eff}</tbody></table></div>
<div class="fga-tw" tabindex="0" role="region" aria-label="Routes for {rid}"><table><caption>Routes to change, with V7’s check dates</caption>
<thead><tr><th scope="col">Route</th><th scope="col">Who acts</th><th scope="col">Feasibility, 2026 to 2030</th><th scope="col">Checked</th></tr></thead><tbody>{route_rows(r)}</tbody></table></div></div></div>
{phone_lists(r, "Expected effect by outcome family. Ordinal marks, never added up.", "Routes to change, with V7’s check dates")}
</section>'''


def card_page(lid, rid, hl="h2", name=None):
    lp = LP[lid]
    d_svg, meta = FG.drawing(lp, M, "card", reform_id=rid)
    save(f"Card-{lid}", d_svg)
    p_svg = save(f"Card-{lid}-Phone", FG.phone_drawing(lp, M, rid))
    layout = "side" if lp["n"] == 2 else "below"
    return f'''<section class="fga fga-cardpage"><div class="wrapc"><article class="fga-card" aria-labelledby="fga-{lid}-h">
<div class="fga-mast"><span>Who Do They Answer To? {DOT} Systems Atlas</span><span>Loop card {DOT} {esc(lid)}</span></div>
<{hl} class="fga-hl" id="fga-{lid}-h">{esc(HEADLINES[lid])}</{hl}>
<p class="fga-title">{chip("Loop", lid)}<span>{esc(lp["title"])}</span></p>
<p class="fga-say"><span class="lab">Read it aloud</span><span class="q">“{esc(lp["how_to_read"])}”</span></p>
<div class="fga-body {layout}"><figure class="fga-cfig"><div class="dsk">{d_svg}</div><div class="phn">{p_svg}</div>
<figcaption class="vh">Loop {esc(lid)} drawing. {esc(lp["how_to_read"])}</figcaption></figure>
<aside class="fga-rail" aria-label="How loop {esc(lid)} behaves">{rail(lp, rid)}</aside></div>
{reform_block(rid, lid)}
<p class="fga-src">{esc(SRC)} Loop {esc(lid)}, connections {", ".join(s["id"] for s in lp["steps"])}; reform {esc(rid)}. The headline is studio-written from V7’s how_to_read for the editor’s review; every other word on the card is V7’s or names a V7 field.</p>
</article></div></section>'''


# ------------------------------------------------------------------ the circuit

def legend():
    def smp(g, w=56):
        dash = D.DASH.get(g)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<svg width="{w}" height="14" viewBox="0 0 {w} 14" aria-hidden="true"><path d="M2 7 L{w - 2} 7" stroke="#121212" stroke-width="2"{da}/></svg>'
    items = [(smp("documented"), "Documented or well supported"), (smp("plausible"), "Plausible"), (smp("plausible_contested"), "Contested"),
             (smp("hypothesis"), "Hypothesis"),
             ('<svg width="22" height="18" viewBox="0 0 22 18" aria-hidden="true"><rect x="3.5" y="1.5" width="15" height="15" rx="7.5" fill="#DCD9D2" stroke="#121212" stroke-width="1.25"/><text x="11" y="13.2" text-anchor="middle" font-size="13" font-weight="700" font-family="Inter" fill="#121212">+</text></svg>',
              "Sign: + same direction, − opposite"),
             ('<svg width="30" height="20" viewBox="0 0 30 20" aria-hidden="true"><rect x="2" y="1" width="26" height="18" rx="9" fill="#DCD9D2" stroke="#5D636D" stroke-width="1.5"/><text x="15" y="14.5" text-anchor="middle" font-size="13" font-weight="700" font-family="Inter" fill="#121212">4</text></svg>',
              "A Stone bundle counts connections on no loop")]
    return '<ul class="fga-legend">' + "".join(f"<li>{a}<span>{esc(b)}</span></li>" for a, b in items) + "</ul>"


def circuit_page(hl="h2", reform=None, bg=D.NEWS, name="Circuit"):
    svg, st = C.build(M, bg=bg, reform_id=reform)
    save(name, svg)
    png = f"20261028_A-{name}-Reduced.png"
    return svg, st, png


def map_section(hl="h2"):
    svg, st, png = circuit_page(hl)
    iw, ih = int(st["W"]), int(st["H"])
    return f'''<section class="fga fga-mappage"><div class="wrapw">
<p class="fga-eyebrow ink">Who Do They Answer To? {DOT} Systems Atlas {DOT} The whole system</p>
<{hl} class="fga-hl">The circuit: 51 variables and 118 connections</{hl}>
<p class="fga-deckd">Read the five areas from left to right, in the order effects mostly travel. The 46 connections that sit on a named loop are drawn as wires you can follow from box to box; the other 72 are counted in Stone bundles. Steps that skip an area run over the top, and steps that come back run under the cards along the return line.</p>
{legend()}
<figure class="fga-map"><div class="dsk">{svg}</div><div class="phn"><img src="{png}" width="{iw}" height="{ih}" alt="The circuit map reduced to fit a phone screen. Open the page on a screen 1440 px wide to read it."><p>The circuit is drawn for a screen 1440 px wide or a printed page. On a phone this reduced copy shows its shape, and the loop cards carry each loop in full.</p></div></figure>
<p class="fga-src">{esc(SRC)} All 51 variables and 118 connections read by script: 46 wires, 72 counted in bundles, each listed on the bundle that counts it.</p>
</div></section>'''


# ------------------------------------------------------------------ the reform view

def reform_page(hl="h2"):
    rid = "R-01"
    r = M["reforms"][rid]
    lp = LP["R10"]
    d_svg, _ = FG.drawing(lp, M, "card", reform_id=rid, view="fg-card")
    save("Reform-R-01-Loop-R10", d_svg)
    p_svg = save("Reform-R-01-Loop-R10-Phone", FG.phone_drawing(lp, M, rid))
    touched = []
    for lid in r["loops"]:
        if lid == "R10":
            continue
        m_svg, _ = FG.drawing(LP[lid], M, "mini")
        save(f"Reform-R-01-Touches-{lid}", m_svg)
        ph = save(f"Reform-R-01-Touches-{lid}-Phone", FG.phone_mini(LP[lid], M))
        touched.append(f'<article class="fga-tile" data-loop="{lid}"><div class="fga-tt"><div class="fga-th">{chip("Loop", lid)}<span class="fga-kind">{esc(LP[lid]["kind_word"])}</span></div>'
                       f'<h4>{esc(LP[lid]["title"])}</h4><p class="fga-cap">V7 lists this loop as touched by {rid}, and none of {rid}’s targets sits on it. It shares C3 with Loop R10, where {rid} acts on L25, the step into C3.</p></div>'
                       f'<div class="fga-fig"><div class="dsk">{m_svg}</div><div class="phn">{ph}</div></div></article>')
    map_svg, st = C.build(M, bg=D.WHITE, reform_id=rid)
    save("Reform-R-01-Circuit", map_svg)
    iw, ih = int(st["W"]), int(st["H"])
    targets = "; ".join(f'{t}, {M["links"][t]["name"] if t in M["links"] else M["nodes"][t]["title"]}' for t in r["targets"])
    eff = "".join(f'<tr><th scope="row">{esc(M["families"][k])}</th><td>{pips(v)}</td><td>{esc(tm(v))} ({esc(M["effect_codes"].get(v, v))})</td></tr>' for k, v in r["effects"].items())
    return f'''<section class="fga fga-reformpage"><div class="wrapw"><article class="fga-rvpage" aria-labelledby="fga-r01-h">
<div class="fga-mast"><span>Who Do They Answer To? {DOT} Systems Atlas</span><span>Reform view {DOT} {rid}</span></div>
<{hl} class="fga-hl" id="fga-r01-h">{esc(HEADLINES["R-01"])}</{hl}>
<p class="fga-title">{chip("Reform", rid)}<span>{esc(r["title"])}</span></p>
<p class="fga-deckd">Red marks its three targets and nothing else: {esc(targets)}. All three sit on Loop R10. V7 also lists Loops B4 and R11 as touched by it. V7 never adds a reform’s effects into one score, so this view gives none.</p>
<div class="fga-rv"><figure class="fga-cfig"><div class="dsk">{d_svg}</div><div class="phn">{p_svg}</div><figcaption class="cap">Loop R10, {esc(lp["title"])}. The red line is L25 and L08; the red keyline is C2.</figcaption></figure>
<div class="fga-touch">{"".join(touched)}</div></div>
<div class="dsk"><div class="fga-tables"><div class="fga-tw" tabindex="0" role="region" aria-label="Expected effects of {rid}"><table><caption>Expected effect by outcome family. Confidence, in V7’s words: “{esc(r["effects_confidence"])}”</caption><thead><tr><th scope="col">Outcome family</th><th scope="col">Mark</th><th scope="col">V7 value</th></tr></thead><tbody>{eff}</tbody></table></div>
<div class="fga-tw" tabindex="0" role="region" aria-label="Routes for {rid}"><table><caption>Routes to change. Remedy evidence: {esc(D.GRADE_WORD[r["remedy_grade"]])}; problem evidence: {esc(D.GRADE_WORD[r["problem_grade"]])}</caption><thead><tr><th scope="col">Route</th><th scope="col">Who acts</th><th scope="col">Feasibility</th><th scope="col">Checked</th></tr></thead><tbody>{route_rows(r)}</tbody></table></div></div></div>
{phone_lists(r, "Expected effect by outcome family. Confidence, in V7’s words: “" + esc(r["effects_confidence"]) + "”", "Routes to change. Remedy evidence: " + esc(D.GRADE_WORD[r["remedy_grade"]]) + "; problem evidence: " + esc(D.GRADE_WORD[r["problem_grade"]]))}
<h3 class="fga-sub">{rid} on the whole system</h3>
<figure class="fga-map"><div class="dsk">{map_svg}</div><div class="phn"><img src="20261028_A-Reform-R-01-Circuit-Reduced.png" width="{iw}" height="{ih}" alt="The circuit on White, reduced to fit a phone, with L25, L08 and C2 in red"><p>Reduced to fit. Open the page on a wide screen to read the circuit.</p></div></figure>
<p class="fga-src">{esc(SRC)} Reform R-01 targets, loops, effects and routes read by script.</p>
</article></div></section>'''


# ------------------------------------------------------------------ styles

CSS = """
.fga{--news:#DCD9D2;--ink:#121212;--white:#FFFFFF;--stone:#5D636D;--deep:#4E535B;--dim:#A3A19C;--red:#E63946;color:var(--ink);font-family:Inter,'Helvetica Neue',Arial,sans-serif}
.fga *{box-sizing:border-box}
.fga svg{display:block;max-width:none}
.fga .wrapc{max-width:1280px;margin:0 auto;padding:0 16px}
.fga .wrapw{max-width:1424px;margin:0 auto;padding:0 16px}
.fga .chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 Inter,Arial,sans-serif;vertical-align:middle;margin-right:8px;flex:none}
.fga .chip .k{background:var(--ink);color:var(--news);padding:6px 7px 0}
.fga .chip .c{border:1.5px solid var(--ink);padding:5px 7px 0;font-size:14px;font-weight:700;background:var(--white);color:var(--ink)}
.fga .dsk{display:block}.fga .phn{display:none}
@media (max-width:1099px){.fga .dsk{display:none}.fga .phn{display:block}}
.fga-eyebrow{font:700 13px/1.4 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0}
.fga-eyebrow.ink{color:var(--deep)}
/* catalog head */
.fga-head{background:var(--ink);color:var(--news);padding:64px 0 72px}
.fga-display{font:800 96px/0.98 'Inter Tight',Inter,Arial,sans-serif;letter-spacing:-0.035em;margin:14px 0 18px;color:var(--news)}
.fga-deck{font:400 22px/1.4 Inter;margin:0 0 40px;max-width:44ch;color:var(--news)}
.fga-teach{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:32px;align-items:start}
.fga-panel{background:var(--white);padding:20px 28px;border-radius:2px;overflow:hidden}
.fga-panel svg{margin:0 auto}
.fga-key{list-style:none;margin:0;padding:0;display:grid;gap:20px;counter-reset:k}
.fga-key li{display:grid;grid-template-columns:34px 1fr;gap:12px;font:400 16px/1.45 Inter;color:var(--news)}
.fga-key b{display:block;font:700 17px/1.3 Inter;color:var(--news);margin-bottom:2px}
.fga-key .n{width:28px;height:28px;border-radius:50%;border:1.5px solid var(--news);display:grid;place-items:center;font:700 14px Inter}
.fga-key .smp{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
/* plates */
.fga-plate{margin-top:56px}
.fga-band{background:var(--ink);color:var(--news)}
.fga-bandin{display:grid;grid-template-columns:140px 1fr auto;gap:28px;align-items:end}
.fga .fga-bandin{padding-top:30px;padding-bottom:26px}
.fga-letter{font:800 120px/0.8 'Inter Tight',Arial,sans-serif;letter-spacing:-0.04em;color:var(--news)}
.fga-letter.sk{font-size:96px}
.fga-band h3{font:800 34px/1.05 'Inter Tight',Arial,sans-serif;letter-spacing:-0.02em;margin:0 0 8px;color:var(--news)}
.fga-band p{margin:0;font:400 17px/1.45 Inter;max-width:60ch;color:var(--news)}
.fga-count{text-align:right;font:400 15px/1.35 Inter !important}
.fga-count b{font:800 44px/1 'Inter Tight',Arial,sans-serif}
.fga-count span{color:var(--dim)}
.fga-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:24px}
.fga-tile{background:var(--white);padding:18px 12px 16px;display:flex;flex-direction:column;gap:12px;min-width:0}
.fga-tile .fga-tt{padding:0 8px}
.fga-th{display:flex;align-items:center;gap:2px}
.fga-kind{font:600 13px Inter;color:var(--deep)}
.fga-tile h4{font:700 16px/1.3 Inter;margin:8px 0 0;text-wrap:balance}
.fga-cap{font:400 14px/1.45 Inter;color:var(--deep);margin:6px 0 0}
.fga-read{font:italic 400 18px/1.45 Lora,Georgia,serif;margin:10px 0 0;color:var(--ink)}
.fga-fig{margin-top:auto;display:flex;justify-content:center;align-items:center;min-height:176px}
.fga-tile.lead2 .fga-fig{flex:1;margin-top:0}
.fga-tile.lead{padding:24px 20px}
.fga-tile.lead h4{font:800 26px/1.15 'Inter Tight',Arial,sans-serif;letter-spacing:-0.01em}
.fga-tile.lead2{grid-column:span 2;grid-row:span 2}
.fga-tile.lead3{grid-column:span 3;display:grid;grid-template-columns:minmax(0,1fr) 380px;align-items:center}
.fga-tile.lead3 .fga-tt{order:2}
.fga-tile.lead3 .fga-fig{order:1}
.fga-foot{margin:28px auto 0;font:400 14px/1.5 Inter;color:var(--deep)}
.fga-foot p{max-width:100ch}
@media (max-width:1099px){
 .fga-head{padding:36px 0 40px}
 .fga-display{font-size:56px;line-height:1;margin:10px 0 14px}
 .fga-deck{font-size:18px;margin-bottom:24px}
 .fga-teach{grid-template-columns:1fr}
 .fga-panel{padding:16px}
 .fga-bandin{grid-template-columns:1fr;gap:10px}
 .fga-letter{font-size:72px}
 .fga-band h3{font-size:26px}
 .fga-count{text-align:left}
 .fga-grid{grid-template-columns:1fr;gap:16px}
 .fga-tile.lead2,.fga-tile.lead3{grid-column:auto;grid-row:auto;display:flex}
 .fga-tile.lead3 .fga-tt,.fga-tile.lead3 .fga-fig{order:initial}
 .fga-fig{min-height:0}
}
/* cards */
.fga-cardpage,.fga-reformpage{padding:40px 0}
.fga-card{background:var(--white);padding:40px 48px 36px}
.fga-mast{display:flex;justify-content:space-between;gap:16px;font:700 13px/1.4 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--deep);border-bottom:1px solid var(--ink);padding-bottom:12px}
.fga-hl{font:800 44px/1.06 'Inter Tight',Arial,sans-serif;letter-spacing:-0.025em;margin:26px 0 14px;max-width:24ch;text-wrap:balance}
.fga-title{display:flex;align-items:center;flex-wrap:wrap;gap:4px;font:600 18px/1.35 Inter;margin:0 0 16px}
.fga-say{margin:0 0 8px;max-width:62ch}
.fga-say .lab{display:block;font:700 13px/1.4 Inter;letter-spacing:.08em;text-transform:uppercase;color:var(--deep);margin-bottom:4px}
.fga-say .q{font:italic 400 20px/1.5 Lora,Georgia,serif}
.fga-body{display:grid;gap:32px;margin-top:16px}
.fga-body.side{grid-template-columns:minmax(0,1fr) 340px}
.fga-body.below .fga-rail{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px;border-top:1px solid var(--ink);padding-top:18px}
.fga-cfig{margin:0}
.fga-cfig svg{margin:0 auto}
.fga-rail{border-left:1px solid var(--ink);padding-left:24px}
.fga-body.below .fga-rail{border-left:0;padding-left:0}
.fga-railsec h4{font:800 20px/1.2 'Inter Tight',Arial,sans-serif;margin:0 0 6px}
.fga-railsec:first-child h4{font-size:28px;text-transform:uppercase;letter-spacing:-0.01em}
.fga-railsec p{font:400 15px/1.5 Inter;margin:0 0 20px;color:var(--ink)}
.fga-reform{border-top:1px solid var(--ink);margin-top:24px;padding-top:18px}
.fga-reform h3{display:flex;align-items:center;flex-wrap:wrap;gap:4px;font:800 26px/1.2 'Inter Tight',Arial,sans-serif;margin:8px 0 10px}
.fga-reform p{font:400 16px/1.5 Inter;max-width:80ch}
.fga .fga-reform p.fga-eyebrow{font:700 13px/1.4 Inter;letter-spacing:.08em;color:var(--deep)}
.fga p,.fga li{text-wrap:pretty}
.fga h1,.fga h2,.fga h3,.fga h4,.fga-key b{text-wrap:balance}
.fga-redkey{display:inline-block;width:26px;height:4px;background:var(--red);vertical-align:middle;margin-right:8px}
.fga-tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:24px;margin-top:12px}
.fga-tw{overflow-x:auto;max-width:100%}
.fga-plist .cap{font:400 14px/1.45 Inter;color:var(--deep);margin:16px 0 6px}
.fga-plist ul{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink)}
.fga-plist li{padding:12px 0;border-bottom:1px solid var(--news);font:400 15px/1.45 Inter}
.fga-plist li b{display:block;font-weight:700;margin:2px 0}
.fga-plist li .chip{margin-bottom:6px}
.fga-plist .pv{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.fga-tw:focus-visible{outline:3px solid #4A7C74;outline-offset:2px}
.fga table{border-collapse:collapse;width:100%;font:400 14px/1.45 Inter}
.fga caption{caption-side:top;text-align:left;font:400 13px/1.4 Inter;color:var(--deep);padding:4px 0}
.fga th,.fga td{text-align:left;vertical-align:middle;padding:8px 10px;border-bottom:1px solid var(--stone)}
.fga thead th{font:700 13px/1.3 Inter;letter-spacing:.04em;text-transform:uppercase;color:var(--deep)}
.fga .pips{display:block}
.fga-src{font:400 13px/1.5 Inter;color:var(--deep);margin-top:20px;max-width:110ch}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (max-width:1099px){
 .fga-cardpage,.fga-reformpage{padding:16px 0}
 .fga-card{padding:20px 16px 20px}
 .fga-mast{flex-direction:column;gap:2px}
 .fga-hl{font-size:30px;margin:16px 0 10px}
 .fga-title{font-size:16px}
 .fga-say .q{font-size:18px}
 .fga-body.side,.fga-body.below .fga-rail{grid-template-columns:1fr}
 .fga-rail{border-left:0;padding-left:0;border-top:1px solid var(--ink);padding-top:16px}
 .fga-reform h3{font-size:22px}
}
/* map */
.fga-mappage{padding:40px 0}
.fga-mappage .fga-hl{max-width:none}
.fga-deckd{font:400 17px/1.5 Inter;max-width:80ch;margin:0 0 16px}
.fga-legend{list-style:none;display:flex;flex-wrap:wrap;gap:10px 26px;padding:0;margin:0 0 18px;font:400 14px Inter}
.fga-legend li{display:flex;align-items:center;gap:8px}
.fga-map{margin:0}
.fga-map .phn img{width:100%;height:auto;border:1px solid var(--stone)}
.fga-map .phn p{font:400 14px/1.5 Inter;color:var(--deep)}
.fga-reformpage{background:var(--white)}
.fga-rvpage{padding:40px 0 24px}
.fga-rv{display:grid;grid-template-columns:1fr;gap:24px;align-items:start;margin:18px 0}
.fga-touch{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.fga-touch .fga-tile{border:1px solid var(--stone)}
.fga-sub{font:800 24px/1.2 'Inter Tight',Arial,sans-serif;margin:28px 0 12px}
.fga .cap{font:400 14px/1.45 Inter;color:var(--deep)}
@media (max-width:1099px){.fga-rv{grid-template-columns:1fr}.fga-touch{grid-template-columns:1fr}.fga-mappage{padding:16px 0}.fga-rvpage{padding:16px 0}}
"""

BOARD_CSS = """
body{margin:0;background:#DCD9D2}
.bd{max-width:1280px;margin:0 auto;padding:40px 16px}
.bd h1{font:800 clamp(40px,6vw,72px)/1.02 'Inter Tight',Arial,sans-serif;letter-spacing:-0.03em;margin:10px 0 14px}
.bd h2{font:800 clamp(28px,3.4vw,40px)/1.08 'Inter Tight',Arial,sans-serif;letter-spacing:-0.02em;margin:6px 0 12px}
.bd h3{font:800 20px/1.2 'Inter Tight',Arial,sans-serif;margin:20px 0 8px}
.bd p,.bd li{font:400 16px/1.6 Inter;max-width:78ch}
.bd .lede{font-size:19px}
.bd-spec{border-top:2px solid #121212;margin-top:56px;padding-top:28px}
.bd-proofs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px;margin:28px 0}
.bd-proofs figure{margin:0;min-width:0}
.bd-proofs figcaption{font:400 13px/1.45 Inter;color:#4E535B;margin-top:6px}
.bd-frame{overflow:auto;max-height:900px;border:1px solid #121212;background:#fff;width:fit-content;max-width:100%}
.bd-frame:focus-visible{outline:3px solid #4A7C74;outline-offset:2px}
.bd-frame img{display:block}
.bd-gray img{width:100%;height:auto;display:block;border:1px solid #5D636D}
.bd-specpanel{background:#FFFFFF;border:1px solid #5D636D;padding:18px 20px;margin-top:20px}
.bd-specpanel dl{display:grid;grid-template-columns:minmax(120px,190px) 1fr;gap:8px 20px;margin:8px 0 0}
.bd-specpanel dt{font:700 14px/1.5 Inter}.bd-specpanel dd{margin:0;font:400 15px/1.55 Inter}
@media (max-width:640px){.bd-specpanel dl{grid-template-columns:1fr}.bd-specpanel dd{margin-bottom:8px}}
.bd-tests{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:20px;margin-top:20px}
.bd-tests div{border-top:1px solid #121212;padding-top:10px}
.bd-dec{background:#1F2D5A;color:#DCD9D2;padding:24px;margin-top:40px}
.bd-dec *{color:#DCD9D2}
.bd-dec table{border-collapse:collapse;width:100%;font:400 15px/1.5 Inter}
.bd-dec th,.bd-dec td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid #A3A19C}
.bd-dec thead th{font:700 13px Inter;letter-spacing:.04em;text-transform:uppercase}
.bd-wrapt{overflow-x:auto}
.bd-wrapt:focus-visible{outline:3px solid #DCD9D2;outline-offset:2px}
.bd .eyebrow{font:700 13px/1.4 Inter;letter-spacing:.08em;text-transform:uppercase;color:#4E535B;margin:0}
.bd-toc{display:flex;flex-wrap:wrap;gap:6px 20px;font:400 15px Inter;margin-top:12px}
.bd-toc a{color:#121212}
.bd-sum{background:#FFFFFF;border:1px solid #5D636D;padding:16px 18px;margin-top:20px}
.bd-index{list-style:none;margin:20px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:16px}
.bd-index li{background:#FFFFFF;padding:16px;display:flex;flex-direction:column;gap:6px;font:400 15px/1.45 Inter}
.bd-index .n{font:800 28px/1 'Inter Tight',Arial,sans-serif}
.bd-index b{font:700 17px/1.3 Inter}
.bd-index a{margin-top:auto;color:#121212;font-weight:600}
.bd a{color:#121212}
.bd-tests h4,.bd-tests .h4{font:700 17px/1.3 Inter,Arial,sans-serif;margin:16px 0 6px}
"""


def head(title, extra_css=""):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:ital,wght@0,400;0,600;0,700;1,400&family=Lora:ital@1&display=swap">'
            f'<style>body{{margin:0;background:#DCD9D2}}{CSS}{extra_css}</style></head><body><main>')


def typo_html(page):
    """Typographic apostrophes, and reform IDs such as R-30 kept on one line, in the text between tags. Tags,
    styles, scripts and drawings stay as written, so every drawing on a page matches its file byte for byte."""
    parts = re.split(r"(<style.*?</style>|<script.*?</script>|<svg.*?</svg>|<[^>]+>)", page, flags=re.S)
    return "".join(x if x.startswith("<") else nbh(re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)]|$)", "\u2019", x)) for x in parts)


def standalone(name, title, fragment):
    path = ASSETS / f"20261028_A-{name}.html"
    path.write_text(typo_html(head(title) + fragment + "</main></body></html>"), encoding="utf-8")
    WRITTEN.append(path)
    return path


# ------------------------------------------------------------------ the board

SPECS = {
    "catalog": [
        ("Grid", "Content 1248 px at 1440, three columns of 400 px tiles with 24 px gutters on a Newsprint ground. Every row fills: a plate whose other loops divide by three gets a lead three columns wide; otherwise the lead spans two columns and two rows. At 390 px one column of 358 px tiles."),
        ("Head", "Charcoal band. Eyebrow 13 px caps, Inter Tight 800 at 96 px (56 px at 390), deck Inter 22 px. R8 at full card size on a White panel with five numbered callouts; the key runs beside it at 1440 and under it at 390."),
        ("Plates", "One per area, in V7's order A to D, then the sketched loops. A Charcoal band holds the area letter in Inter Tight 800 at 120 px (72 at 390), the area's name at 34 px, V7's area text and the count. The lead is R8 for A and otherwise the loop with the most live reforms V7 lists."),
        ("Miniature", "The card's drawing at a little over half size: boxes 158 px wide in Newsprint with a 5 px Charcoal spine, V7's chain label in Inter 13 semibold wrapped to at most two balanced lines. Two steps side by side with the return underneath; three as two over one; four as two over two, clockwise from top left. Lines 2 px Charcoal in V7's texture, each with its sign in a 16 px disc. At 390 the boxes stack and the return runs up the left."),
        ("Caption", "Kind in words, one turn in words, least certain step by ID and V7's grade word. No ticks, record squares, pointers or red: they belong on the card (CD notation budget)."),
        ("Type", "Inter Tight 800 for display and area letters, Inter 13 to 22 px for text, Lora Italic 18 px for V7's read-aloud sentence on lead tiles. Nothing under 13 px."),
    ],
    "card": [
        ("Surface", "White card on Newsprint, 48 px padding at 1440 and 16 px at 390. Pillar Red marks the targets of the one reform the card names: the line and its disc outline for a step, a 3 px keyline for a box (4.17:1 on White)."),
        ("Headline", "Inter Tight 800 at 44 px (30 at 390), studio-written from V7's how_to_read for the editor, with the verb matched to the least certain grade. Then V7's title with the Loop chip, then the read-aloud sentence quoting how_to_read in Lora Italic 20 px."),
        ("Drawing", "The catalog geometry at full size: boxes 264 px wide with a 222 px gap for two steps, 280 px with a 200 px gap for three or four, with the ID in Inter Tight 800 16 px, V7's chain label in Inter 16 semibold and its “Higher:” rule from increase_means in Inter 16. Lines 2.5 px with V7's texture, delay ticks at the start, signs in 24 px discs with the record square on documented steps. Step labels give the ID, V7's name, the grade and the delay in words, set outside the line."),
        ("Rail", "Concept 08's order: feeds itself or pushes back with V7's glossary definition; what the return line means, from the closing connection's plain text; the least certain step, quoting V7's evidence summary; one turn; now, with V7's series. The rail sits beside a two-step drawing and under a three- or four-step one."),
        ("Foot", "The reform's chip and title, where it acts, problem and remedy grades, V7's confidence text, the effect pips with no total, and the routes with V7's check dates or “no check date in V7”."),
        ("Phone", "The boxes stack in chain order; forward steps run down a line at the left of the boxes; the return line runs up the left edge into the first box. Step labels sit beside the line."),
    ],
    "map": [
        ("Grid", "1392 px wide at 1440. Five White area cards on Newsprint, A to E left to right; the outside drivers as Charcoal tabs on the top edge; the economy and technology layers in a lower band."),
        ("Wires", "The 46 loop connections as individual 2 px Charcoal wires in V7's texture, one corner radius (5 px). Same-area wires hook in the card's left gutter; next-area wires take a lane in the channel; longer forward steps run over the top bus and longer return steps along the bottom bus. Lanes are 9 px apart and are shared only where two wires' runs never meet; box ports are 16 px apart and offset by 8 px across a channel, so no two stubs share a row."),
        ("Signs", "One 13 px glyph per wire in a 15 px capsule on its first stub."),
        ("Bundles", "The other 72 connections in Stone (4.29:1 on Newsprint) at the same 2 px weight, each bundle with a count capsule; counts inside an area sit in its card's footer, and counts inside the lower layers in their cards. Every bundle lists the connections it counts."),
        ("Boxes", "Each card's box width comes from its longest V7 chain label at 13 px semibold on two balanced lines; boxes grow with the number of wires they carry, so E1, on 11 loop wires, is the tallest."),
        ("Live atlas", "One loop lights in Charcoal and every other wire drops to Stone. A reform view moves to White, with red at that reform's targets."),
    ],
    "reform": [
        ("Surface", "White. Red marks R-01's three targets, L25, L08 and C2, on the R10 card drawing and on the circuit, and nothing else."),
        ("Order", "Headline, R-01's chip and V7 title, where it acts, the R10 drawing with the two loops V7 lists as touched beside it, the effects and routes, then the reform on the whole circuit."),
        ("Honesty", "No total and no ranking: V7 never adds effects into one score. B4 and R11 carry no red, because none of R-01's targets sits on them, and their captions say so."),
        ("Phone", "The R10 drawing stacks, the touched loops follow as tiles, the two tables become lists, and the circuit appears reduced with a note."),
    ],
}

TESTS = {
    "catalog": [
        ("Wall test", "Pinned beside a Tufte small-multiples plate, the first draft read as a grid of equal cells. Changes: plates with Charcoal bands and 120 px letters, a lead specimen at double size on every plate, and three columns, where four left orphan rows and could not hold V7's longest chain label on two lines."),
        ("2x test", "Checked every miniature at 2x for collisions and truncation. Changes: real font metrics for every wrap (round one estimated widths), balanced two-line labels so no word sits alone, box outlines removed in favor of the spine, and a stacked phone miniature, because the 376 px drawing cannot fit a 358 px phone tile without shrinking text under 13 px. A second pass at 2x found captions listing tied steps one by one and the band letters touching the band's top edge; tied steps now read “L02 and L31, both plausible”, and the bands gained 30 px of air above the letter."),
    ],
    "card": [
        ("Wall test", "Beside Concept 08, the round-one card had gained little. Changes: an editorial headline, the read-aloud sentence in Lora Italic, Concept 08's rail order restored, and the return line and A5's keyline carrying the one red."),
        ("2x test", "At 2x the first draft set R10's grade line for L08 into the C2 box. Changes: the grade and delay now join the label block above a top step and wrap within the gap; every step label is measured against the space it has. A second pass found “under 2 years” broken across lines and a line starting with its separator dot; no-break spaces now hold each phrase whole, and the R8 gap widened from 170 to 222 px so L38's name takes two lines. On a phone the effect and route tables became lists, since their columns clipped at 358 px."),
    ],
    "map": [
        ("Wall test", "Beside the Vignelli diagram, a first route put the top bus through the bundle tracks and set a bus label on the wires. Changes: drivers, bundles and the top bus each got their own band, and the three bus labels sit on a background halo where a wire crosses them."),
        ("2x test", "The lower band set two-line names on a one-line rhythm, so they overlapped, and a card footer ran past its card. Changes: a two-line rhythm for the lower band and footers that wrap inside their card. A later pass found A3's name running past card A and the economy layer listing EC5 after EC9; A3 now wraps inside its card and both layers list in number order."),
    ],
    "reform": [
        ("Wall test", "Round one's reform view ran the C2 row red across the full fabric. Here red touches only two wires and one box. The first draft also sat the view inside a card frame that ran 24 px past a 1440 px screen; the view is now a White page of its own."),
        ("2x test", "Checked the three loop drawings and the circuit on White at 2x; the touched-loop captions were rewritten to say exactly why they carry no red."),
    ],
}


def spec_html(key):
    rows = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in SPECS[key])
    tests = "".join(f'<div><h4 class="h4">{esc(a)}</h4><p>{esc(b)}</p></div>' for a, b in TESTS[key])
    return f'<div class="bd-specpanel"><p class="eyebrow">Spec</p><dl>{rows}</dl></div><div class="bd-tests">{tests}</div>'


def proofs(name, phone=True):
    figs = []
    if phone:
        figs.append(f'<figure><div class="bd-frame" tabindex="0" role="region" aria-label="{esc(name)} at 390 px, capture"><img src="{REL}20261028_A-{name}-390.png" width="390" height="1600" alt="{esc(name)} page at 390 px wide, first screens"></div>'
                    f'<figcaption>The page at 390 px, captured at that width. <a href="{REL}20261028_A-{name}.html">Open the page</a>.</figcaption></figure>')
    figs.append(f'<figure class="bd-gray"><img src="{REL}20261028_A-{name}-Grayscale.png" width="1440" height="900" alt="{esc(name)} page at 1440 px in grayscale, first screen"><figcaption>Grayscale proof at 1440 px, reduced to fit. Red turns mid gray; the keyline, the line and the words still name the target.</figcaption></figure>')
    return f'<div class="bd-proofs">{"".join(figs)}</div>'


def checks_html():
    v = json.loads(VERIFY.read_text()) if VERIFY.exists() else None
    c = json.loads(CHECK.read_text()) if CHECK.exists() else None
    items = [f"<li>{esc(s)}</li>" for s in (v["summary"] if v else ["Data verification has not run for this build."])]
    items += [f"<li>{esc(s)}</li>" for s in (c["summary"] if c else ["Rendered checks have not run for this build."])]
    nt = "".join(f"<li>{esc(s)}</li>" for s in (c or {}).get("not_checked", []))
    return f'''<section class="bd-spec" id="checks"><p class="eyebrow">Checks</p><h2>How this direction was checked</h2>
<h3>Tested</h3><ul>{"".join(items)}</ul><h3>Not tested</h3><ul>{nt}<li>The ten-second reader check (CD brief section 4). It needs Dustin's go and five readers new to the brand.</li><li>The distinctiveness test beyond the studio's own judgment.</li></ul></section>'''


DECISIONS = [
    ("Direction A as built", "Take A forward; keep it as the fallback behind C; return to the current system (G1-11)",
     "Hold A as the safe path while C reports", "It meets Dustin's literal ask and keeps Concept 08's card; its beauty depends on finish, as the brief warned."),
    ("Three columns on the catalog", "Three columns; four columns with three-line labels", "Three columns",
     "Four columns cannot hold V7's longest chain label on two lines without shrinking text, and three fill every row with no filler."),
    ("Editorial headlines", "Keep the studio's lines for the editor to revise; use V7's titles as headlines", "Keep them for the editor",
     "They name the mechanism the way Concept 08 did, with verbs matched to the least certain grade."),
    ("The circuit's 72 bundled connections", "Counted bundles; draw all 118 as wires", "Counted bundles",
     "All 118 as wires would bury the loops; the register keeps every connection one step away."),
]


def board():
    sections = [("idea", "The idea"), ("spec-catalog", "Catalog page"), ("spec-r8", "R8 card"), ("spec-r10", "R10 card"),
                ("spec-map", "Circuit"), ("spec-reform", "R-01 view"), ("checks", "Checks"), ("decide", "Decisions")]
    toc = "".join(f'<a href="#{a}">{esc(b)}</a>' for a, b in sections)
    index = "".join(f'<li><span class="n">{n}</span><b>{t}</b><span>{d}</span><a href="{REL}20261028_A-{f}.html">Open the {t.replace("Loop catalog", "catalog").replace("Circuit", "circuit")}</a></li>'
                    for n, (f, t, d) in enumerate((("Loop-Catalog", "Loop catalog", "All 23 loops, R8 taught at full size, one plate per area."),
                                                    ("R8-Loop-Card", "R8 card", "Two steps on White, with R-30's targets in red."),
                                                    ("R10-Loop-Card", "R10 card", "The stress test: four steps, R-01 in red."),
                                                    ("Circuit-Page", "Circuit", "51 variables and 118 connections, Concept 09 redrawn."),
                                                    ("R-01-Reform-View", "R-01 view", "One reform on its loop and on the whole system.")), 1))
    intro = f'''<div class="bd"><p class="eyebrow">Phase 2 {DOT} Systems maps, round two {DOT} October 28, 2026 {DOT} Direction A</p>
<h1>Field Guide</h1>
<p class="lede">Dustin's reference card came from Concept 08, the Loop Field Guide. This direction takes the name at its word: every loop is a specimen card drawn one way, and the catalog is a set of plates where each card is the R8 card at a smaller size. The head of the catalog teaches one card at full size, and a reader then reads all 23 the way a birder reads a guide.</p>
<div class="bd-sum"><p><b>What a first-time reader grasps without a key:</b> boxes are things that change; the line across the top runs forward; the line underneath, or up the left side, brings the last change back to the first box.</p>
<p><b>Built to the creative director's brief</b> (<span>work/handoffs/phase-2/20261028_CD-Review-Of-Map-Directions.md</span>, section 4): the notation budget by scale, Rule 05.3, the 13 px floor, Lora Italic only for V7's read-aloud sentence, constant stroke weight within a view, no truncated label and no row with one card alone. Every page below is shown first as a page at its true composition, then at 390 px and in grayscale, then its spec and what the wall and 2x tests changed.</p></div>
<nav class="bd-toc" aria-label="Board sections">{toc}</nav>
<section class="bd-spec" id="idea"><p class="eyebrow">Specimens</p><h2>Five pages</h2><p>Each is a real page. The board shows it at its true composition, then at 390 px and in grayscale, then its spec and what the wall and 2x tests changed. Open any page on its own here.</p>
<ol class="bd-index">{index}</ol></section></div>'''

    def spec_section(sid, num, title, lede, fragment, name, key, phone=True):
        return (f'<section id="{sid}" aria-label="{esc(title)}"><div class="bd"><div class="bd-spec"><p class="eyebrow">Specimen {num}</p><h2>{esc(title)}</h2><p>{esc(lede)}</p></div></div>'
                f'{fragment}<div class="bd">{proofs(name, phone)}{spec_html(key)}</div></section>')
    cat = catalog_page("h2")
    r8 = card_page("R8", "R-30", "h2")
    r10 = card_page("R10", "R-01", "h2")
    mp = map_section("h2")
    rv = reform_page("h2")
    for name, title, frag in (("Loop-Catalog", "Twenty-Three Loops", catalog_page("h1")), ("R8-Loop-Card", "Loop R8 Card", card_page("R8", "R-30", "h1")),
                              ("R10-Loop-Card", "Loop R10 Card", card_page("R10", "R-01", "h1")), ("Circuit-Page", "The Circuit", map_section("h1")),
                              ("R-01-Reform-View", "Reform R-01 View", reform_page("h1"))):
        standalone(name, title, frag)
    body = (intro
            + spec_section("spec-catalog", 1, "The loop catalog", "A Charcoal head that teaches R8 at full size, then one plate per area. Every miniature is drawn from its loop's own steps.", cat, "Loop-Catalog", "catalog")
            + spec_section("spec-r8", 2, "The R8 card", "The R8 card at full size on White, with R-30's targets in red: the return line L39 and A5's keyline.", r8, "R8-Loop-Card", "card")
            + spec_section("spec-r10", 3, "The R10 card, the stress test", "Four steps from documented to plausible, with R-01's targets in red. The rail moves under the drawing.", r10, "R10-Loop-Card", "card")
            + spec_section("spec-map", 4, "The whole system: the circuit", "Concept 09 redrawn: every loop connection a wire, every other connection counted.", mp.replace(f'src="{""}20261028_A-Circuit-Reduced.png"', f'src="{REL}20261028_A-Circuit-Reduced.png"'), "Circuit-Page", "map", phone=False)
            + spec_section("spec-reform", 5, "The R-01 reform view", "One reform's targets in red, on White, on the loop card and on the whole circuit.", rv.replace('src="20261028_A-Reform-R-01-Circuit-Reduced.png"', f'src="{REL}20261028_A-Reform-R-01-Circuit-Reduced.png"'), "R-01-Reform-View", "reform")
            + f'<div class="bd">{checks_html()}'
            + '<section class="bd-dec" id="decide"><p class="eyebrow" style="color:#DCD9D2">Decisions for Dustin</p><h2>What you decide for Direction A</h2>'
            + '<div class="bd-wrapt" tabindex="0" role="region" aria-label="Decisions for Dustin"><table><thead><tr><th scope="col">Decision</th><th scope="col">Options</th><th scope="col">Studio recommendation</th><th scope="col">Why</th></tr></thead><tbody>'
            + "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td><b>{esc(c)}</b></td><td>{esc(d)}</td></tr>" for a, b, c, d in DECISIONS)
            + f'</tbody></table></div><p>Red on every specimen follows Rule 05.3 as worded in D2-01: one working red per view, the point where the named reform acts, on White, never on Prussian. The catalog names no reform and carries none.</p></section>'
            + f'<p class="fga-src" style="font:400 13px/1.5 Inter;color:#4E535B">{esc(SRC)} Built by work/build/scripts/phase-2/maps_r2_a_build.py; drawings and pages in work/boards/phase-2/maps-r2/a/.</p></div>')
    return head("Map Direction A Field Guide", BOARD_CSS) + body + "</main></body></html>"


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    page = typo_html(board())
    BOARD.write_text(page, encoding="utf-8")
    print("board", BOARD.relative_to(ROOT), f"{len(page) / 1e6:.2f} MB;", len(WRITTEN), "files;", "leads", LEADS)
