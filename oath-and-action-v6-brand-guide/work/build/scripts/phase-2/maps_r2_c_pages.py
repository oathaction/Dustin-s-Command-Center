"""Direction C, Loop Lines: real pages built around the drawings. Catalog page at 1440 and 390 px, loop card pages
at 1440 and 390 px, the poster page and its 24 by 36 inch print page, the working map page and the reform view page.
Every page is standalone HTML in work/boards/phase-2/maps-r2/c/ and inlines the drawings it shows."""
import html
import math
import re

import maps_r2_c_cards as C
import maps_r2_c_draw as D
import maps_r2_c_geom as G
import maps_r2_c_views as V

esc = html.escape
M, LOOPS = G.M, G.LOOPS
SNAP = "October 15, 2026"
SRC = f"Source: Who Do They Answer To? Systems Atlas V7, snapshot {SNAP}. Drawn by script from the V7 model; every mark is checked against V7."
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:ital,wght@0,400;0,600;0,700;1,400&family=Lora:ital@1&display=swap">')
AREA_ORDER = "ABCDE"
EDITORIAL = {"R8": "How housing scarcity sustains itself", "R10": "How safe seats make more safe seats"}

BASE_CSS = """
:root{--charcoal:#121212;--newsprint:#DCD9D2;--white:#FFFFFF;--red:#E63946;--prussian:#1F2D5A;--stone:#5D636D;--deep:#4E535B;
--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;--body:Inter,"Helvetica Neue",Arial,sans-serif;--quote:Lora,Georgia,serif}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--newsprint);color:var(--charcoal);font:400 16px/1.55 var(--body)}
svg{display:block;max-width:none}
a{color:inherit}
a:focus-visible,.wrap:focus-visible{outline:3px solid var(--prussian);outline-offset:2px}
.chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 var(--body);vertical-align:middle}
.chip .k{background:var(--charcoal);color:var(--newsprint);padding:6px 7px 0;letter-spacing:.02em}
.chip .c{border:1.5px solid var(--charcoal);padding:5px 7px 0;font-size:14px;font-weight:700}
.kind{display:inline-flex;align-items:center;gap:6px;font:600 14px/1.3 var(--body)}
.src{font-size:13px;color:var(--deep);margin:24px 0 0}
"""


def chip(kind, code):
    return f'<span class="chip"><span class="k">{esc(kind)}</span><span class="c">{esc(code)}</span></span>'


def kind_svg(kind, size=24, ink=D.CHARCOAL):
    """The kind glyph, kept only where it draws at 24 px or more (round-two review, fix 2)."""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false">'
            f'{D.kind_glyph(size / 2, size / 2, kind, size, ink, 1.9)}</svg>')


def page(title, css, body, lang="en", desc=""):
    return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{FONTS}<style>{BASE_CSS}{css}</style></head>'
            f'<body>{body}</body></html>\n')


# ------------------------------------------------------------------ words for one loop

def areas_of(lid):
    return sorted({M["nodes"][s["code"]]["area"] for s in LOOPS[lid]["stations"] if s["code"]}, key=AREA_ORDER.index)


def words_list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def weakest_text(lp):
    steps = lp["steps"]
    if lp["weakest"]:
        ws = [s for s in steps if s["id"] in lp["weakest"]]
        return "Least certain: " + words_list([f'{s["id"]}, {D.GRADE_WORD[s["evidence"]].lower()}' for s in ws]) + "."
    grades = sorted({D.GRADE_WORD[s["evidence"]].lower() for s in steps})
    if len(grades) == 1:
        return f"No step is less certain than another: every step is {grades[0]}."
    return "Steps tie at V7's grade rank: " + " and ".join(grades) + "."


def turn_text(lp):
    t = f"{lp['kind_gloss'].capitalize()}. A turn takes {lp['delay_word']}."
    if lp["hypothesized"]:
        t += " It closes through a hypothesized step."
    return t


def catalog_order():
    """District order: A's lines first, then B, C, D and E; a line that crosses areas follows the last area it reaches."""
    groups = {a: [] for a in AREA_ORDER}
    for lid in G.NUMBERED:
        last = max(areas_of(lid), key=AREA_ORDER.index)
        groups[last].append(lid)
    return groups


def span_of(lid):
    return 2 if len(areas_of(lid)) >= 3 else 1


def pack(items, cols):
    """Rows that always fill. Items keep their order; when a wide card would overhang, the next narrow card in the
    queue moves up to fill the row. Returns rows of (item, span)."""
    queue = list(items)
    rows, cur, used = [], [], 0
    while queue:
        it, sp = queue[0]
        if used + sp <= cols:
            cur.append(queue.pop(0))
            used += sp
        else:
            j = next((k for k, (_, s2) in enumerate(queue) if used + s2 <= cols), None)
            if j is None:
                rows.append(cur)
                cur, used = [], 0
                continue
            cur.append(queue.pop(j))
            used += cur[-1][1]
        if used == cols:
            rows.append(cur)
            cur, used = [], 0
    if cur:
        rows.append(cur)
    return rows


# ------------------------------------------------------------------ effect pips (Gate 1 mark M4)

SIZE = {"S": 1, "M": 2, "L": 3}


def parse_effect(v):
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


def pips_svg(v, w=150, h=24):
    """One to three pips with a sign; costs sit left of the zero line; an open pip is the far end of a range; a
    question mark is an unknown. Never summed."""
    p = parse_effect(v)
    cx = w / 2
    out = [f'<line x1="{cx}" y1="2" x2="{cx}" y2="{h - 2}" stroke="{D.CHARCOAL}" stroke-width="1"/>']
    for side, firm, open_ in ((1, p["gain"], p["gain_open"]), (-1, p["cost"], p["cost_open"])):
        for i in range(max(firm, open_)):
            x = cx + side * (12 + i * 12)
            if i < firm:
                out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="4.5" fill="{D.CHARCOAL}"/>')
            else:
                out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="3.75" fill="none" stroke="{D.CHARCOAL}" stroke-width="1.5"/>')
        if max(firm, open_):
            gx = cx + side * (12 + max(firm, open_) * 12)
            out.append(D.T(gx - (3 if side > 0 else -3), h / 2 + 4.5, "+" if side > 0 else D.MINUS, 13, 700, D.CHARCOAL, "start" if side > 0 else "end"))
    if p["zero"]:
        out.append(f'<rect x="{cx - 2:.1f}" y="{h / 2 - 7:.1f}" width="4" height="14" fill="{D.CHARCOAL}"/>')
    if p["uncertain"]:
        out.append(f'<circle cx="{cx}" cy="{h / 2}" r="8" fill="{D.WHITE}" stroke="{D.CHARCOAL}" stroke-width="1.5"/>' + D.T(cx, h / 2 + 4.5, "?", 13, 700, D.CHARCOAL, "middle"))
    return (f'<svg class="pips" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Effect {esc(v)}" data-effect="{esc(v)}">'
            f'{D.STYLE}{"".join(out)}</svg>')


def tm(s):
    return re.sub(r"(?<![\w])-(?=[SML0])", D.MINUS, s)


def reform_panel(rid, lid=None, compact=False, responsive=False):
    """Where a reform acts, its effects by outcome family and its routes. compact is the phone card's form: the
    routes as a list, so no cell runs past the card. responsive carries both forms and lets the width choose."""
    r = M["reforms"][rid]
    fam = M["families"]
    pw = 124 if (compact or responsive) else 150
    rows = "".join(f'<tr><th scope="row">{esc(fam[k])}</th><td>{pips_svg(v, w=pw)}</td><td>{esc(tm(v))}</td></tr>' for k, v in r["effects"].items())
    routes = "".join(
        f'<tr><td>{chip("Route", x["route"])}</td><td>{esc(M["route_names"][x["route"]])}</td><td>{esc(x["feasibility"].capitalize())}</td>'
        f'<td>{esc(datefmt(x["checked"]) if x["checked"] else "no check date in V7")}</td></tr>' for x in r["routes"])
    route_items = "".join(
        f'<li>{chip("Route", x["route"])} <b>{esc(M["route_names"][x["route"]])}</b><br>'
        f'<span class="small">Feasibility {esc(x["feasibility"])}. Checked: {esc(datefmt(x["checked"]) if x["checked"] else "no check date in V7")}.</span></li>'
        for x in r["routes"])
    route_table = (f'<div class="wrap rt-wide" tabindex="0" role="region" aria-label="Routes for {rid}"><table class="eff"><caption>Routes to change, with V7\'s feasibility and the date each was checked</caption>'
                   f'<thead><tr><th scope="col">Route</th><th scope="col">Who</th><th scope="col">Feasibility</th><th scope="col">Checked</th></tr></thead><tbody>{routes}</tbody></table></div>')
    route_list = (f'<div class="rt-narrow"><p class="small rcap">Routes to change, with V7\'s feasibility and the date each was checked</p>'
                  f'<ul class="routes">{route_items}</ul></div>')
    route_html = route_list if compact else (route_table + route_list if responsive else route_table)
    tg = r["targets"]
    drawn = set()
    if lid:
        drawn = {s["id"] for s in LOOPS[lid]["steps"]} | {s["code"] for s in LOOPS[lid]["stations"]}
    here = [t for t in tg if t in drawn] if lid else tg
    away = [t for t in tg if t not in drawn] if lid else []
    away_txt = ""
    for t in away:
        if t in M["links"]:
            l = M["links"][t]
            away_txt += (f" It also acts on {t}, {l['name'][0].lower() + l['name'][1:]}, which runs from {M['nodes'][l['from']]['label']} to "
                         f"{M['nodes'][l['to']]['label'].lower()} in the {M['nodes'][l['to']]['layer']} layer, outside this loop.")
        elif t in M["nodes"]:
            away_txt += f" It also acts on {t}, {M['nodes'][t]['label']}, outside this loop."
    return f'''<section class="reform" aria-labelledby="rf-{rid}">
<p class="eyebrow">Where a reform acts</p>
<h2 id="rf-{rid}">{chip("Reform", rid)} {esc(r["title"])}</h2>
<p><span class="redkey" aria-hidden="true"></span> Red marks where {rid} acts on this view: {esc(words_list(here))}.{esc(away_txt)}</p>
<p>{esc(r["what_it_changes"]) if r.get("what_it_changes") else ""}</p>
<div class="rfgrid"><div class="wrap" tabindex="0" role="region" aria-label="Effects of {rid}"><table class="eff"><caption>Effects by outcome family, as V7's ordinal codes. The atlas never adds them into one score.</caption>
<thead><tr><th scope="col">Family</th><th scope="col">Mark</th><th scope="col">V7 code</th></tr></thead><tbody>{rows}</tbody></table></div>
{route_html}</div>
<p class="small">Problem evidence: {esc(D.GRADE_WORD.get(r["problem_grade"], r["problem_grade"]))}. Remedy evidence: {esc(D.GRADE_WORD.get(r["remedy_grade"], r["remedy_grade"]))}. Confidence in the effects: {esc(r["effects_confidence"])}.</p>
</section>'''


def datefmt(s):
    y, m, d = s.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[int(m) - 1]} {int(d)}, {y}"


# ------------------------------------------------------------------ catalog

CAT_CSS = """
.band{background:var(--prussian);color:var(--white)}
.band svg{width:100%;height:auto}
.pw{max-width:1440px;margin:0 auto;padding:0 64px}
.read{background:var(--charcoal);color:var(--newsprint);padding:22px 0}
.read .pw{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px 32px;align-items:start}
.read h2{font:800 22px/1.2 var(--display);margin:0;grid-column:1/-1;color:var(--newsprint)}
.read p{margin:0;font-size:14px;line-height:1.45}
.read svg{display:inline-block;vertical-align:middle;margin-right:6px}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;padding:36px 0 8px}
.card{background:var(--white);padding:16px 16px 14px;display:flex;flex-direction:column;min-width:0}
.card.w2{grid-column:span 2}
.card .top{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.card .areas{font:600 13px/1.3 var(--body);color:var(--deep)}
.card .kindw{display:inline-flex;align-items:center;gap:6px}
.card h3{font:600 16px/1.3 var(--body);margin:10px 0 8px;text-wrap:balance}
.card figure{margin:4px 0 8px;display:flex;justify-content:center;align-items:center;flex:1;min-height:90px}
.card figure svg{flex:none}
.card.w2 .inner{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:20px;align-items:center;flex:1}
.card.w2 figure{justify-content:flex-start}
.card p{margin:0;font-size:13px;line-height:1.45;color:var(--deep)}
.card p.k{color:var(--charcoal);font-weight:600}
.card.sk h3{margin-top:4px}
.secthead{font:800 13px/1 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--deep);margin:28px 0 -14px}
.foot{padding:8px 0 56px}
"""

CAT_CSS_PHONE = """
.pw{padding:0 16px}
.read .pw{grid-template-columns:1fr}
.cards{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:20px 0 8px}
.card{padding:12px 12px 12px}
.card h3{font-size:15px}
.card.w2 .inner{display:block}
.card .stations{font-size:13px;color:var(--charcoal);margin:6px 0}
.card figure svg{max-width:100%;height:auto}
"""


def band_svg(L0, width, height, cell, ox, oy, head_size, head_lines, deck, phone=False):
    L = L0.scaled(cell, ox, oy)
    th = D.Theme("prussian")
    net, _ = D.network(L, th, show_labels=False, show_signs=False, show_bullets=False, line_w=2.0 if not phone else 1.4,
                       show_ids=False, station_scale=0.36 if not phone else 0.26, hub_names=False)
    body = [net]
    x = 64 if not phone else 16
    y = 130 if not phone else 70
    # the headline is one text of two lines (tspans), so its tight display leading reads as one label
    spans = "".join(f'<tspan x="{x:.1f}" y="{y + i * head_size * 0.98:.1f}">{esc(ln)}</tspan>' for i, ln in enumerate(head_lines))
    body.append(f'<text class="d" font-size="{head_size}" fill="{D.WHITE}">{spans}</text>')
    yy = y + (len(head_lines) - 1) * head_size * 0.98 + (44 if not phone else 34)
    for ln in deck:
        body.append(D.T(x, yy, ln, 18 if not phone else 15, 400, D.NEWS, "start"))
        yy += 26 if not phone else 21
    lab = "Catalog head: the Loop Lines poster as a band, with the headline Twenty loop lines"
    return D.svg_doc(width, height, "".join(body), lab, "c-band" if not phone else "c-band-phone", D.PRUSSIAN,
                     extra=f' data-cell="{L.cell}" data-ox="{L.ox}" data-oy="{L.oy}"')


def read_strip(phone=False):
    ink = D.NEWS
    sw = lambda g: (f'<svg width="44" height="10" viewBox="0 0 44 10" aria-hidden="true" focusable="false">'
                    f'{V.legend_line(2, 5, g, 40, ink, 3.0)}</svg>')
    cells = [
        f"<p>{sw('documented')}Documented or well supported. {sw('plausible')}Plausible.</p>",
        f"<p>{sw('plausible_contested')}Contested. {sw('hypothesis')}Hypothesis. A hollow line is a sketched step.</p>",
        f"<p>{kind_svg('R', 24, ink)}A loop that feeds itself. {kind_svg('B', 24, ink)}One that pushes back.</p>",
        "<p>Each card is the loop's own line lifted from the map at one shared scale. A wide card is a loop that crosses three areas.</p>",
    ]
    return f'<section class="read" aria-labelledby="howto"><div class="pw"><h2 id="howto">How to read a line</h2>{"".join(cells)}</div></section>'


def catalog_card(L, lid, sp, phone=False, written=None):
    lp = LOOPS[lid]
    ar = areas_of(lid)
    if phone:
        svg, w, h = C.miniature(L, lid, scale=0.24, names=False, view="c-mini-phone")
    else:
        svg, w, h = C.miniature(L, lid)
    if written is not None:
        written.append((f"Mini{'-Phone' if phone else ''}-{lid}", svg))
    bullet = (f'<svg width="{D.bullet_size(lid)[0]:.0f}" height="22" viewBox="0 0 {D.bullet_size(lid)[0]:.0f} 22" aria-hidden="true" focusable="false">'
              f'{D.bullet_svg(D.bullet_size(lid)[0] / 2, 11, lid, D.CHARCOAL, D.WHITE)}</svg>')
    stations = ""
    if phone:
        stations = f'<p class="stations">{esc(" to ".join(s["label"] for s in lp["stations"]))}, then back to {esc(lp["stations"][0]["label"])}.</p>'
    cls = "card w2" if sp == 2 else "card"
    cap = (f'<p class="k">{esc(turn_text(lp))}</p><p>{esc(weakest_text(lp))}</p>'
           f'<p>Crosses {esc(words_list(ar))}.</p>')
    head = (f'<div class="top">{bullet}<span class="sr">Loop {lid}.</span><span class="areas kindw">{kind_svg(lp["type"], 24, D.DEEP)}'
            f'{esc(lp["kind_word"])}</span></div>')
    fig = f'<figure>{svg}</figure>'
    if sp == 2 and not phone:
        inner = f'<div class="inner">{fig}<div><h3>{esc(lp["title"])}</h3>{cap}</div></div>'
        return f'<article class="{cls}" data-loop="{lid}" data-span="{sp}" data-areas="{"".join(ar)}">{head}{inner}</article>'
    return f'<article class="{cls}" data-loop="{lid}" data-span="{sp}" data-areas="{"".join(ar)}">{head}<h3>{esc(lp["title"])}</h3>{fig}{stations}{cap}</article>'


def sketched_card(lid, phone=False, written=None):
    lp = LOOPS[lid]
    w, h = (260, 120) if not phone else (150, 96)
    body, pts, labels = C.sketched_tile(lid, w=w, h=h)
    names = []
    if not phone:
        for i, (p, lab) in enumerate(zip(pts, labels)):
            lines = D.wrap_to(lab, 110, 13, 600)
            lw = max(D.text_w(x, 13, 600) for x in lines)
            if len(pts) == 2:
                x = p[0] - (14 if i == 0 else -14)
                anchor = "end" if i == 0 else "start"
                x = max(x, lw + 6) if i == 0 else min(x, w - lw - 6)
                y0 = p[1] - 8 * (len(lines) - 1) + 4
            else:
                anchor = "middle"
                x = min(max(p[0], lw / 2 + 6), w - lw / 2 - 6)
                y0 = p[1] + 22 if p[1] > h / 2 else p[1] - 14 - 16 * (len(lines) - 1)
            for k, ln in enumerate(lines):
                names.append(D.T(x, y0 + 16 * k, ln, 13, 600, D.CHARCOAL, anchor))
    names = "".join(names)
    lab = f"Sketched loop {lid}: {lp['title']}. No numbered chain."
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h + (16 if not phone else 0)}" viewBox="0 {-8 if not phone else 0} {w} {h + (16 if not phone else 0)}" role="img" '
           f'aria-label="{esc(lab)}" data-view="c-sketched" data-loop="{lid}"><title>{esc(lab)}</title>{D.STYLE}'
           f'<rect x="0" y="{-8 if not phone else 0}" width="{w}" height="{h + 16}" fill="{D.WHITE}"/>{"".join(body)}{names}</svg>')
    if written is not None:
        written.append((f"Sketched{'-Phone' if phone else ''}-{lid}", svg))
    stations = f'<p class="stations">{esc(" to ".join(labels))}, then back.</p>' if phone else ""
    return (f'<article class="card sk" data-loop="{lid}" data-span="1" data-sketched="1"><div class="top">{chip("Loop", lid)}<span class="areas">Sketched</span></div>'
            f'<h3>{esc(lp["title"])}</h3><figure>{svg}</figure>{stations}<p class="k">{esc(lp["kind_gloss"].capitalize())}. No numbered chain yet, so it has no stations on the map.</p>'
            f'<p>The hollow line marks a sketched step.</p></article>')


def catalog_page(L, phone=False, written=None):
    groups = catalog_order()
    items = [(lid, span_of(lid)) for a in AREA_ORDER for lid in groups[a]]
    cols = 4 if not phone else 2
    # the sketched loops close the page in the same grid, so every row fills
    rows = pack(items + [(lid, 1) for lid in G.SKETCHED], cols)
    order = [it for row in rows for it in row]
    cards = "".join(sketched_card(lid, phone, written) if lid in G.SKETCHED else catalog_card(L, lid, sp, phone, written)
                    for lid, sp in order)
    n_num = len(G.NUMBERED)
    if not phone:
        band = band_svg(L, 1440, 560, 18, 1440 - 64 - 22 * 18 - 30, 300, 96, ["Twenty", "loop lines"],
                        [f"Atlas V7 draws {n_num} loops with numbered steps. Each is a line",
                         "that comes back to where it starts. They share 25 variables",
                         "and 46 connections. Three sketched loops close the page."])
    else:
        band = band_svg(L, 390, 560, 9.5, 16 + 12.6 * 9.5, 400, 56, ["Twenty", "loop lines"],
                        [f"Atlas V7 draws {n_num} loops with", "numbered steps. Each is a line that",
                         "comes back to where it starts."], phone=True)
    if written is not None:
        written.append(("Catalog-Band" + ("-Phone" if phone else ""), band))
    sk_html = ""
    body = (f'<header class="band" role="banner"><h1 class="sr">Twenty loop lines</h1>{band}</header>{read_strip(phone)}'
            f'<main class="pw"><p class="secthead">The {n_num} numbered loops in district order, then the three sketched loops</p><div class="cards">{cards}</div>{sk_html}'
            f'<p class="src foot">{esc(SRC)} Specimen page for Direction C; illustrative layout, real V7 content.</p></main>')
    css = CAT_CSS + (CAT_CSS_PHONE if phone else "") + ".sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"
    title = "Loop Lines Catalog" + (" Phone" if phone else "")
    return page(title, css, body, desc="The twenty numbered loops of Atlas V7 as loop lines, in district order"), order


# ------------------------------------------------------------------ loop card page

CARD_CSS = """
.pw{max-width:1440px;margin:0 auto;padding:40px 64px 56px}
.wrap{overflow-x:auto;max-width:100%}
.cardpage{background:var(--white);padding:36px 40px 32px}
.top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
h1{font:800 44px/1.05 var(--display);letter-spacing:-.02em;margin:18px 0 10px;text-wrap:balance}
.v7title{font:600 17px/1.4 var(--body);margin:0 0 14px}
.readaloud{font:italic 400 20px/1.5 var(--quote);margin:0 0 20px;max-width:62ch}
.readaloud cite{display:block;font:400 13px/1.4 var(--body);color:var(--deep);margin-top:4px}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start}
.rail{border-left:1px solid var(--charcoal);padding-left:22px}
.rail h2{font:800 15px/1.3 var(--display);margin:14px 0 4px}
.rail p{margin:0 0 6px;font-size:14px;line-height:1.5}
.rail .loc{margin:0 0 6px}
.small{font-size:13px;color:var(--deep)}
.eyebrow{font:700 13px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--deep);margin:0 0 6px}
.reform{border-top:1px solid var(--charcoal);margin-top:24px;padding-top:18px}
.reform h2{font:800 24px/1.25 var(--display);margin:0 0 10px}
.redkey{display:inline-block;width:24px;height:6px;background:var(--red);vertical-align:middle;margin-right:4px}
.rfgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--stone);vertical-align:middle}
thead th{font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--deep)}
caption{caption-side:top;text-align:left;font-size:13px;color:var(--deep);padding:0 0 6px}
.pips{display:block}
.steps{list-style:none;padding:0;margin:12px 0 0}
.steps li{border-top:1px solid var(--stone);padding:10px 0}
.steps b{font-weight:700}
.stationlist{list-style:none;padding:0;margin:8px 0 0}
.stationlist li{padding:6px 0}
.stationlist .n{font:700 18px/1.25 var(--display)}
.rfgrid>*{min-width:0}
.grid>*{min-width:0}
.routes{list-style:none;padding:0;margin:0}
.routes li{border-bottom:1px solid var(--stone);padding:8px 0;font-size:14px;line-height:1.5}
.rcap{margin:0 0 6px}
.kind svg{flex:none}
"""

CARD_CSS_PHONE = """
.pw{padding:16px 16px 40px}
.cardpage{padding:20px 16px}
h1{font-size:30px}
.readaloud{font-size:18px}
.grid{grid-template-columns:1fr}
.rail{border-left:0;padding-left:0;border-top:1px solid var(--charcoal)}
.rfgrid{grid-template-columns:1fr}
"""


def facts(lid):
    lp = LOOPS[lid]
    out = []
    out.append(("Kind", f"{lp['kind_word']}: {lp['kind_gloss']}."))
    out.append(("One turn", f"Takes {lp['delay_word']}, the delay of its slowest step."))
    w = weakest_text(lp)
    if lid == "R8":
        w += (" V7's summary still names L39 as the weaker step, because equity is one motive among several for "
              "opposing construction.")
    out.append(("Least certain step", w))
    out.append(("Now", f"V7 reads the loop as {lp['direction_word']}. The record to watch: {lp['reference_mode']}. "
                       "No values are charted until the research lead supplies them with their source."))
    cl = "Closed: every step is a numbered connection." if lp["closure"] == "closed" else lp["closure"].capitalize() + "."
    out.append(("Closure", cl))
    return out


def card_page(L, Ls, lid, reform, phone=False, written=None):
    lp = LOOPS[lid]
    if phone:
        # 390 less the page and card padding (16 px each side, twice): the drawing sits inside the White card
        drawing = C.card_drawing(L, lid, reform=reform, width=326, height=250 if lp["n"] == 2 else 400, phone=True)
    else:
        drawing = C.card_drawing(L, lid, reform=reform, width=860, height=440 if lp["n"] == 2 else 680)
    loc = C.locator(Ls, lid, 300, 196)
    if written is not None:
        written.append((f"Card-{lid}" + ("-Phone" if phone else ""), drawing))
        written.append((f"Locator-{lid}" + ("-Phone" if phone else ""), loc))
    head = (f'<div class="top">{chip("Loop", lid)}<span class="kind">{kind_svg(lp["type"])}{esc(lp["kind_word"])}: {esc(lp["kind_gloss"])}</span></div>'
            f'<h1>{esc(EDITORIAL.get(lid, lp["title"]))}</h1>'
            f'<p class="v7title">Loop {lid} in Atlas V7: {esc(lp["title"])}</p>'
            f'<p class="readaloud">“{esc(lp["how_to_read"])}”<cite>Atlas V7, how to read Loop {lid}. The headline above is the studio\'s, written from this sentence.</cite></p>')
    rail = "".join(f"<h2>{esc(k)}</h2><p>{esc(v)}</p>" for k, v in facts(lid))
    rail = (f'<figure class="loc">{loc}<figcaption class="small">Where Loop {lid} sits on the whole map: lit in Charcoal, every other line in Stone.</figcaption></figure>' + rail)
    steplist = ""
    if phone:
        items = []
        for st in lp["steps"]:
            l = M["links"][st["id"]]
            red = f" {reform} acts here." if st["id"] in M["reforms"][reform]["targets"] else ""
            items.append(f'<li><b>{st["id"]}</b> {esc(l["name"])}. {esc(st["from_label"])} to {esc(st["to_label"])}. '
                         f'Sign {esc(D.sign_glyph(st["polarity"]))}: {"both move the same way" if st["polarity"] == "+" else "they move opposite ways"}. '
                         f'{esc(D.GRADE_WORD[st["evidence"]])}: {esc(D.GRADE_GLOSS[st["evidence"]])}. {esc(D.DELAY_WORD[st["delay"]].capitalize())}.{esc(red)}</li>')
        sts = "".join(f'<li><span class="n">{esc(s["label"])}</span> <span class="small">{esc(s["code"])}</span><br>{esc(C.higher_rule(s["code"]))}</li>' for s in lp["stations"])
        steplist = f'<h2 class="eyebrow" style="margin-top:16px">Steps, in order</h2><ol class="steps">{"".join(items)}</ol><h2 class="eyebrow" style="margin-top:12px">Stations</h2><ul class="stationlist">{sts}</ul>'
    body = (f'<main class="pw"><article class="cardpage" data-loop="{lid}">{head}<div class="grid"><div><figure style="margin:0">{drawing}'
            f'<figcaption class="small">The loop\'s own line from the map at full size. Tags show each step\'s sign and the way it runs; '
            f'ticks count the delay; the small square marks a documented step.</figcaption></figure>{steplist}</div>'
            f'<aside class="rail" aria-label="Facts about Loop {lid}">{rail}</aside></div>{reform_panel(reform, lid, compact=phone)}'
            f'<p class="src">{esc(SRC)}</p></article></main>')
    css = CARD_CSS + (CARD_CSS_PHONE if phone else "")
    return page(f"Loop {lid} Card" + (" Phone" if phone else ""), css, body, desc=f"Loop card for {lid}, Direction C")


# ------------------------------------------------------------------ drawing pages

VIEW_CSS = """
body.prussian{background:var(--prussian)} body.white{background:var(--white)}
.frame{width:1440px;margin:0}
.fit,.full{display:none}
.fit img{display:block;width:100%;height:auto}
.full{margin:0;padding:10px 16px 18px;font-size:15px}
body.prussian .full{color:var(--newsprint)} body.prussian .full a{color:var(--white)}
.below{background:var(--white);padding:24px 64px 8px}
.tvsec{background:var(--newsprint);padding:32px 64px 48px}
.tvsec h2{font:800 24px/1.2 var(--display);margin:0 0 12px}
.wrap{overflow-x:auto;max-width:100%}
table.tv{border-collapse:collapse;width:100%;font-size:14px}
.tv th,.tv td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--stone);vertical-align:top}
.tv thead th{font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--deep)}
.tv caption{caption-side:top;text-align:left;font-size:14px;color:var(--deep);padding:0 0 8px}
.small{font-size:13px;color:var(--deep)}
.eyebrow{font:700 13px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--deep);margin:0 0 6px}
.reform h2{font:800 24px/1.25 var(--display);margin:0 0 10px}
.redkey{display:inline-block;width:24px;height:6px;background:var(--red);vertical-align:middle;margin-right:4px}
.rfgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.rfgrid>*{min-width:0}
table.eff{border-collapse:collapse;width:100%;font-size:14px}
.eff th,.eff td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--stone);vertical-align:middle}
.eff thead th{font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--deep)}
.eff caption{caption-side:top;text-align:left;font-size:13px;color:var(--deep);padding:0 0 6px}
.routes{list-style:none;padding:0;margin:0}
.routes li{border-bottom:1px solid var(--stone);padding:8px 0;font-size:14px;line-height:1.5}
.rcap{margin:0 0 6px}
.rt-narrow{display:none}
.tv-narrow{display:none}
.tvl{list-style:none;padding:0;margin:8px 0 0}
.tvl li{border-top:1px solid var(--stone);padding:10px 0}
.tvl p{margin:0 0 4px;font-size:15px;line-height:1.5}
.tvl .tvh{font-weight:600}
@media (max-width:1199px){
 .tv-wide{display:none} .tv-narrow{display:block}
 .frame{display:none}
 .fit,.full{display:block}
 .below{padding:20px 16px 8px}
 .tvsec{padding:24px 16px 40px}
 .rfgrid{grid-template-columns:1fr}
 .rt-wide{display:none} .rt-narrow{display:block}
}
"""


def view_page(title, svg, cls, desc="", capture="", what="", panel=""):
    """A whole-system view as a page. At 1440 the drawing sits inline at full size. Below 1200 px the page shows
    the same drawing fit to the screen width, as its capture inside a focusable region, with a link to the full-size
    image; then the reform panel where the view has one; then the lines in words."""
    fit = (f'<div class="fit" role="region" tabindex="0" aria-label="{esc(title)}, fit to the screen width">'
           f'<img src="{esc(capture)}" width="1440" height="960" alt="{esc(what)} The lines in words, below, give every line and its stations."></div>'
           f'<p class="full"><a href="{esc(capture)}">Open the map at full size</a>, 1440 by 960 px, to zoom in.</p>')
    below = f'<div class="below">{panel}</div>' if panel else ""
    tv = (f'<section class="tvsec" aria-labelledby="tvh"><h2 id="tvh">The lines in words</h2>{text_version(narrow=True)}'
          f'<p class="src">{esc(SRC)}</p></section>')
    body = f'<main aria-label="{esc(title)}"><div class="frame">{svg}</div>{fit}{below}{tv}</main>'
    return page(title, VIEW_CSS, body, desc=desc).replace("<body>", f'<body class="{cls}">', 1)


def print_page(svg):
    css = "@page{size:36in 24in;margin:0} html,body{margin:0;background:#1F2D5A} svg{width:36in;height:24in;display:block}"
    return page("Loop Lines Poster Print", css, svg, desc="The Loop Lines poster at 24 by 36 inches")


def text_version(caption="Text version of the poster: every line, its stations in order and the sign of each step", narrow=False):
    """The poster as a table, for screen readers and for anyone who wants the lines in words. narrow adds the same
    content as a list, which the view pages show below 1200 px in place of the table."""
    rows, items = [], []
    for lid in G.NUMBERED:
        lp = LOOPS[lid]
        parts = []
        for st in lp["steps"]:
            parts.append(f'{st["from_label"]} ({st["from"]}) {D.sign_glyph(st["polarity"])}\u2192')
        seq = " ".join(parts) + f' {lp["steps"][0]["from_label"]} ({lp["steps"][0]["from"]})'
        rows.append(f'<tr><th scope="row">{chip("Loop", lid)}</th><td>{esc(lp["kind_word"])}: {esc(lp["kind_gloss"])}</td>'
                    f'<td>{esc(seq)}</td><td>{esc(words_list(areas_of(lid)))}</td></tr>')
        items.append(f'<li><p class="tvh">{chip("Loop", lid)} {esc(lp["kind_word"])}: {esc(lp["kind_gloss"])}. '
                     f'Areas {esc(words_list(areas_of(lid)))}.</p><p>{esc(seq)}</p></li>')
    key = "A plus means both variables move the same way; a minus means they move opposite ways."
    table = (f'<div class="wrap tv-wide" tabindex="0" role="region" aria-label="Text version of the poster"><table class="tv"><caption>{esc(caption)}. '
             f'{key}</caption>'
             f'<thead><tr><th scope="col">Line</th><th scope="col">Kind</th><th scope="col">Stations in order</th><th scope="col">Areas</th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div>')
    if not narrow:
        return table
    lst = f'<div class="tv-narrow"><p class="small">{esc(caption)}. {key}</p><ol class="tvl">{"".join(items)}</ol></div>'
    return table + lst
