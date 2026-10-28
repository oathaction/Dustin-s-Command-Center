"""Specimen pages for Direction B, Snowball and Thermostat: the loop catalog, the loop cards (R8, R10, B4) and the
R-01 reform view. Each page is one responsive HTML file, rendered and checked at 1440 and 390 px.

Every value printed here comes from the loop model (maps_model.py, Atlas V7 read once). Copy that is not a V7 field
is studio copy: the card headlines are drafts for the editor and say so in the page foot.
"""
import html
import re
from pathlib import Path

import maps_r2_b_draw as D

esc = html.escape
ROOT = Path(__file__).resolve().parents[4]
SNAP = "October 15, 2026"
SRC = f"Source: Who Do They Answer To? Systems Atlas V7, snapshot {SNAP}."
HONEST = "Every snowball is drawn the same. The shape shows the kind of loop and never its speed or strength."
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@600;800'
         '&family=Lora:ital,wght@1,400&display=swap">')


def wordmark(color="#121212", height=20, label="Oath & Action"):
    """The wordmark from the V5 Polished sprite master (Master Brief section 3), inlined. The ampersand keeps
    signature red, which Rule 05.3 does not count."""
    raw = (ROOT / "work/extract/v5-polished/sprite/wordmark.svg").read_text(encoding="utf-8")
    raw = re.sub(r"<title>.*?</title>", "", raw)
    w = round(970.71 / 108 * height, 1)
    raw = raw.replace('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 970.71 108" style="color:#121212">',
                      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 970.71 108" width="{w}" height="{height}" role="img" '
                      f'aria-label="{esc(label)}" style="color:{color};display:block" class="wm">')
    return raw


def chip(kind, code):
    return f'<span class="chip"><span class="k">{esc(kind)}</span><span class="c">{esc(code)}</span></span>'


def cap1(s):
    return s[:1].upper() + s[1:]


def direction_text(lp):
    return cap1(lp["direction_word"])


def _join_ids(ids):
    return ids[0] if len(ids) == 1 else ", ".join(ids[:-1]) + " and " + ids[-1]


def weakest_text(lp):
    if lp["conceptual"]:
        return None
    steps = lp["steps"]
    if lp["weakest"]:
        ws = [s for s in steps if s["id"] in lp["weakest"]]
        grades = []
        for s in ws:
            g = D.GRADE_WORD[s["evidence"]].lower()
            if g not in grades:
                grades.append(g)
        if len(grades) == 1:
            return f"Least certain: {_join_ids([s['id'] for s in ws])},\u00a0{grades[0].replace(' ', chr(160))}"
        return "Least certain: " + ", ".join(f'{s["id"]},\u00a0{D.GRADE_WORD[s["evidence"]].lower()}' for s in ws)
    grades = sorted({D.GRADE_WORD[s["evidence"]] for s in steps})
    if len(grades) == 1:
        return f"Every step graded {grades[0].lower()}"
    return "Steps tie at V7's rank: " + " and ".join(g.lower() for g in grades)


def turn_text(lp):
    if lp["conceptual"]:
        return "no complete numbered chain"
    return f'{lp["delay_word"]} a turn'.replace("10 years", "10\u00a0years").replace(" a turn", "\u00a0a\u00a0turn")


def kind_word(lp):
    return "Feeds itself" if lp["type"] == "R" else "Pushes back"


def tm(s):
    return re.sub(r"(?<![\w])-(?=[SML0])", D.MINUS, s)


# ------------------------------------------------------------------ effect pips (M4), copied from round one's rule

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
    """Filled pips for a stated code, open pips for the far end of a range, costs left of the zero line, never summed."""
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
    return (f'<svg class="pips" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Effect {esc(tm(v))}" data-effect="{esc(v)}">'
            f'{D.STYLE}{"".join(out)}</svg>')


def texture_svg(grade, conceptual=False, w=64, ink=D.INK, ground=D.WHITE, label=None):
    d = f"M2 9 L{w - 2} 9"
    if conceptual:
        body = (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="5"/><path d="{d}" fill="none" stroke="{ground}" stroke-width="1.5"/>')
    else:
        dash = D.DASH.get(grade)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        body = f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="2"{da}/>'
    lab = label or ("Sketched step: hollow line" if conceptual else f"{D.GRADE_WORD[grade]} line")
    return f'<svg class="tex" width="{w}" height="18" viewBox="0 0 {w} 18" role="img" aria-label="{esc(lab)}">{body}</svg>'


# ------------------------------------------------------------------ shared CSS

BASE_CSS = """
:root{--news:#DCD9D2;--ink:#121212;--white:#FFFFFF;--deep:#4E535B;--stone:#5D636D;--red:#E63946;--prussian:#1F2D5A;
--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;color:var(--ink);font:400 16px/1.5 var(--body)}
.wrap{max-width:1440px;margin:0 auto;padding:0 48px}
.chip{display:inline-flex;align-items:stretch;height:26px;font:600 13px/1 var(--body);vertical-align:middle;flex:none}
.chip .k{background:var(--ink);color:var(--news);padding:7px 7px 0;letter-spacing:.02em}
.chip .c{border:1.5px solid var(--ink);padding:5px 7px 0;font-size:14px;font-weight:700}
.on-ink .chip .k{background:var(--news);color:var(--ink)} .on-ink .chip .c{border-color:var(--news)}
h1,h2,h3{text-wrap:balance}
p{text-wrap:pretty}
.mast{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 0 18px}
.mast .where{font:700 13px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase}
.src{font:400 13px/1.5 var(--body);color:var(--deep);margin:0}
@media (max-width:760px){.wrap{padding:0 16px}.mast .where{font-size:13px;letter-spacing:.04em;text-align:right}}
"""


def page(title, body_class, css, body, desc):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{FONTS}<style>{BASE_CSS}{css}</style></head>'
            f'<body class="{body_class}">{body}</body></html>')


# ------------------------------------------------------------------ catalog page

CAT_CSS = """
body{background:var(--news)}
.head{background:var(--ink);color:var(--news)}
.head .mast{border-bottom:1px solid #4E535B}
.hero{display:grid;grid-template-columns:240px minmax(0,1fr);column-gap:48px;row-gap:28px;align-items:center;padding:56px 0 8px}
.hero svg{display:block}
.count{font:800 96px/.92 var(--display);letter-spacing:-.035em;margin:0}
.count-gloss{font:400 20px/1.4 var(--body);margin:14px 0 0;max-width:46ch}
.deckrow{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;padding:40px 0 48px;align-items:start}
.deck{font:400 18px/1.55 var(--body);margin:0;max-width:62ch}
.honest{margin:0;border:2px solid var(--news);padding:18px 20px;font:600 18px/1.45 var(--body)}
.howto{border-top:1px solid #4E535B;padding:32px 0 48px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px}
.howto h2{font:800 22px/1.15 var(--display);margin:0 0 8px;letter-spacing:-.01em}
.howto p{margin:0;font-size:15px;line-height:1.5}
.howto .key{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:6px;font-size:14px;line-height:1.35}
.howto .key li{display:grid;grid-template-columns:64px 1fr;gap:10px;align-items:center}
.howto .demo{margin-bottom:12px}
.area{padding:64px 0 0}
.band{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:28px;align-items:end;border-top:3px solid var(--ink);padding-top:18px;margin-bottom:24px}
.letter{font:800 96px/.78 var(--display);letter-spacing:-.04em}
.band h2{font:800 34px/1.05 var(--display);letter-spacing:-.02em;margin:0}
.band p{margin:8px 0 0;max-width:64ch;color:var(--deep);font-size:16px}
.band .cnt{font:600 15px/1.4 var(--body);margin:0;text-align:right;white-space:nowrap;color:var(--ink)}
.row{display:grid;gap:16px;list-style:none;margin:0;padding:0}
.n6{grid-template-columns:repeat(6,minmax(0,1fr))}.n4{grid-template-columns:repeat(4,minmax(0,1fr))}
.tile{background:var(--white);padding:18px 18px 22px;display:flex;flex-direction:column;min-width:0}
.tt{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:14px}
.tt .kw{font:600 13px/1.2 var(--body)}
.shape svg{display:block;width:150px;height:auto;margin:0 auto}
.tile h3{font:600 17px/1.25 var(--display);letter-spacing:-.005em;margin:14px 0 10px}
.st{list-style:none;margin:0 0 10px;padding:0;font-size:13px;line-height:1.4}
.st li{display:grid;grid-template-columns:26px 1fr;gap:4px}
.st b{font-weight:700}
.fx{margin:auto 0 0;padding-top:10px;border-top:1px solid #C9C6BF;font-size:13px;line-height:1.45;color:var(--deep);text-wrap:pretty}
.note{background:var(--white);padding:18px 18px 22px;border-left:6px solid var(--ink)}
.note h3{font:800 20px/1.15 var(--display);margin:0 0 8px}
.note p{margin:0 0 10px;font-size:14px;line-height:1.5}
.nkey{list-style:none;margin:6px 0 14px;padding:0;display:grid;gap:10px;font-size:14px;line-height:1.4}
.nkey li{display:grid;grid-template-columns:64px 1fr;gap:10px;align-items:center}
.band.noletter{grid-template-columns:minmax(0,1fr) auto}
.foot{padding:56px 0 48px}
.foot p{max-width:90ch}
@media (max-width:760px){
.hero{grid-template-columns:1fr;row-gap:12px;padding:32px 0 0}
.hero .em{width:150px}.hero .em svg{width:150px;height:auto}
.hero .em + div{margin-bottom:24px}
.count{font-size:56px;line-height:.95}
.count-gloss{font-size:17px}
.deckrow{grid-template-columns:1fr;gap:20px;padding:12px 0 32px}
.deck{font-size:16px}.honest{font-size:16px;padding:14px 16px}
.howto{grid-template-columns:1fr;gap:24px}
.area{padding-top:44px}
.band{grid-template-columns:auto minmax(0,1fr);gap:14px}
.band .cnt{grid-column:1 / -1;text-align:left;white-space:normal}
.band.noletter{grid-template-columns:1fr}
.letter{font-size:64px}
.band h2{font-size:24px}
.band p{font-size:15px}
.n6,.n4{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.tile{padding:12px 11px 16px}
.tt{flex-wrap:wrap;margin-bottom:10px}
.tile h3{font-size:16px}
.note{grid-column:1 / -1;padding:14px 14px 16px}
}
"""


def mini_tile(lp, svg):
    names = "".join(f'<li><b>{esc(s["code"] or "")}</b><span>{esc(s["label"])}</span></li>' for s in lp["stations"])
    lines = [f'{esc(direction_text(lp))} \u00b7 {esc(turn_text(lp))}']
    w = weakest_text(lp)
    if w:
        lines.append(esc(w))
    if lp["hypothesized"]:
        lines.append("Closes only through a hypothesized step")
    return (f'<li class="tile" data-loop="{esc(lp["id"])}" data-kind="{lp["type"]}"><div class="tt">{chip("Loop", lp["id"])}'
            f'<span class="kw">{kind_word(lp)}</span></div><div class="shape">{svg}</div><h3>{esc(lp["title"])}</h3>'
            f'<ol class="st" aria-label="Stations, clockwise from twelve o\'clock">{names}</ol>'
            f'<p class="fx" data-direction="{esc(lp["direction"])}" data-delay="{esc(lp["delay"])}">{"<br>".join(lines)}</p></li>')


def howto_strip(model, demo_svg):
    key = [("documented", False, "Documented or well supported: on the public record, or strong studies agree on the direction"),
           ("plausible", False, "Plausible: a coherent mechanism with some evidence"), ("plausible_contested", False, "Contested: credible studies disagree"),
           ("hypothesis", False, "Hypothesis: proposed, not yet supported"), (None, True, "Sketched: V7 names no numbered step")]
    rows = "".join(f'<li>{texture_svg(g, c, ink=D.NEWS, ground=D.INK, label=t)}<span>{esc(t)}</span></li>' for g, c, t in key)
    return f'''<div class="howto" aria-label="How to read the shapes">
<div><div class="demo">{demo_svg}</div><h2>Start at twelve o'clock</h2><p>Follow the line clockwise. Each disc is a variable, shown by its ID; the list under each shape gives its name.</p></div>
<div><h2>Each segment is one step</h2><p>One variable moves the next. The line's texture shows how strong the evidence is for that step.</p><ul class="key">{rows}</ul></div>
<div><h2>A snowball comes back further out</h2><p>The outlined disc repeats the first ID one lap out: the loop has returned to where it started, one turn later, and each turn builds on the last. The outward step means one more turn and never an amount.</p></div>
<div><h2>A thermostat closes on its start</h2><p>A change sets off a push back toward where it began. Under each shape, a line in words says which way the loop is running now, how long one turn takes and which step is least certain.</p></div>
</div>'''


def catalog_page(model, minis, emblems, demo_svg):
    LP = model["loops"]
    nR = sum(1 for lp in LP.values() if lp["type"] == "R")
    nB = sum(1 for lp in LP.values() if lp["type"] == "B")
    head = f'''<header class="head on-ink"><div class="wrap">
<div class="mast">{wordmark("#DCD9D2", 20)}<span class="where">Systems Atlas · Loop catalog</span></div>
<div class="hero">
<div class="em">{emblems["R"]}</div><div><p class="count" data-count="R">{nR} feed themselves</p><p class="count-gloss">Snowball loops. A change comes back around and builds on itself, turn after turn.</p></div>
<div class="em">{emblems["B"]}</div><div><p class="count" data-count="B">{nB} push back</p><p class="count-gloss">Thermostat loops. A change sets off a correction that pulls the system back.</p></div>
</div>
<div class="deckrow"><p class="deck">Atlas V7 names {nR + nB} feedback loops: chains of cause that come back to where they began. Each one is drawn by the same rule. A loop that feeds itself is one turn of a spiral that returns to its first variable one lap further out. A loop that pushes back is a ring that closes on its start.</p>
<p class="honest" data-honest="1">{esc(HONEST)}</p></div>
{howto_strip(model, demo_svg)}
</div></header>'''
    areas = []
    for g in model["groups"]:
        ids = g["loops"]
        if g["id"] == "SK":
            letter = ""
            deck = ("Atlas V7 names three loops without a complete numbered chain. They keep their shape, drawn in the hollow line, "
                    "and stations that are not variables are open circles.")
        else:
            reg = next(a for a in model["areas"] if a["id"] == g["id"])
            letter = g["id"]
            deck = reg["text"]
        nr = sum(1 for i in ids if LP[i]["type"] == "R")
        nb = len(ids) - nr
        parts = []
        if nr:
            parts.append(f"{nr} feed{'s' if nr == 1 else ''} {'itself' if nr == 1 else 'themselves'}")
        if nb:
            parts.append(f"{nb} push{'es' if nb == 1 else ''} back")
        cnt = f'{len(ids)} loops · ' + ", ".join(parts)
        tiles = [mini_tile(LP[i], minis[i]) for i in ids]
        if g["id"] == "SK":
            open_disc = ('<svg class="tex" width="64" height="18" viewBox="0 0 64 18" role="img" aria-label="Open station">'
                         '<circle cx="32" cy="9" r="7" fill="#FFFFFF" stroke="#121212" stroke-width="2"/></svg>')
            tiles.insert(0, '<li class="note"><h3>Read a sketch</h3><p>B2 and B3 push back and R9 feeds itself, so they keep the ring and the spiral.</p>'
                            f'<ul class="nkey"><li>{texture_svg(None, True)}<span>A step V7 describes without a numbered connection</span></li>'
                            f'<li>{open_disc}<span>A station that is not one of V7\'s variables</span></li></ul>'
                            '<p>R9 is a design target: a loop V7 would like to see built.</p></li>')
        ncls = "n6" if len(tiles) == 6 else "n4"
        title = g["title"] if g["id"] != "SK" else "Sketched loops"
        let = f'<span class="letter" aria-hidden="true">{letter}</span>' if letter else ''
        areas.append(f'<section class="area" id="area-{g["id"]}" data-group="{g["id"]}"><div class="band{" noletter" if not letter else ""}">{let}<div><h2>{"Area " + letter + ", " if letter else ""}{esc(title)}</h2>'
                     f'<p>{esc(deck)}</p></div><p class="cnt">{esc(cnt)}</p></div><ul class="row {ncls}">{"".join(tiles)}</ul></section>')
    foot = (f'<footer class="foot"><p class="src">{esc(SRC)} Loop types, chains, grades, delays and directions come from V7. '
            f'The five thermostats stand out by shape inside their area rows; the live atlas can sort the wall by kind. '
            f'Specimen for Direction B, Snowball and Thermostat. Shapes are drawn by script from V7 and checked against it.</p></footer>')
    body = head + f'<main class="wrap">{"".join(areas)}{foot}</main>'
    return page("Loop Catalog, Direction B", "cat", CAT_CSS, body,
                "Direction B specimen: the 23 Atlas V7 loops as spirals and rings, by area.")


# ------------------------------------------------------------------ card page

CARD_CSS = """
body{background:var(--white)}
.mast{border-bottom:1px solid #C9C6BF}
.kicker{display:flex;align-items:center;flex-wrap:wrap;gap:10px;font:600 15px/1.3 var(--body);margin:36px 0 0}
.kicker svg{display:block}
h1{font:800 44px/1.04 var(--display);letter-spacing:-.025em;margin:16px 0 14px;max-width:24ch}
.v7{font:600 17px/1.4 var(--body);margin:0 0 10px;max-width:70ch}
.v7 span{color:var(--deep);font-weight:400}
.read{font:italic 400 20px/1.45 var(--quote);margin:0;max-width:62ch}
.main{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:32px;margin-top:28px;align-items:start}
.fig{margin:0}
.fig .desk{display:block;margin:0 auto;max-width:100%;height:auto}
.fig .phone,.strip{display:none}
.rail .blk{border-top:2px solid var(--ink);padding:12px 0 22px}
.rail .lab{font:700 13px/1.3 var(--body);letter-spacing:.06em;text-transform:uppercase;margin:0 0 6px}
.rail .big{font:800 28px/1.08 var(--display);letter-spacing:-.015em;margin:0 0 8px}
.rail p{margin:0 0 8px;font-size:15px;line-height:1.5}
.rail .honest{font-weight:600;border-left:4px solid var(--ink);padding-left:12px}
.tbl{width:100%;border-collapse:collapse;font-size:15px;line-height:1.4;font-variant-numeric:tabular-nums}
.tbl caption{text-align:left;font:700 13px/1.3 var(--body);letter-spacing:.06em;text-transform:uppercase;padding:0 0 10px}
.tbl th,.tbl td{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-bottom:1px solid #C9C6BF}
.tbl thead th{font:700 13px/1.3 var(--body);color:var(--deep);border-bottom:2px solid var(--ink)}
.tbl .tex{display:block;margin-top:4px}
section.sec{margin-top:44px}
.left .steps{margin-top:8px}
section.sec > h2{font:800 30px/1.1 var(--display);letter-spacing:-.02em;margin:0 0 16px}
.reform{border-top:3px solid var(--ink);padding-top:20px}
.reform h2{display:flex;flex-wrap:wrap;align-items:center;gap:12px}
.rgrid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:40px;margin-top:8px}
.rgrid p{margin:0 0 10px;max-width:66ch}
.redkey{display:inline-block;width:22px;height:4px;background:var(--red);vertical-align:middle;margin-right:8px}
.also{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:12px}
.also figure{margin:0;display:grid;grid-template-columns:150px minmax(0,1fr);gap:18px;align-items:start;border-top:2px solid var(--ink);padding-top:14px}
.also figcaption{font-size:15px;line-height:1.5}
.also h3{font:600 18px/1.25 var(--display);margin:6px 0 6px}
.foot{margin:48px 0 40px;padding-top:14px;border-top:1px solid #C9C6BF}
@media (max-width:1000px){
.main{grid-template-columns:1fr}
.fig .desk{display:none}.fig .phone{display:block;margin:0 auto}.strip{display:block}
.rgrid{grid-template-columns:1fr;gap:12px}
}
@media (max-width:760px){
.kicker{margin-top:24px;font-size:14px}
h1{font-size:30px;line-height:1.08}
.v7{font-size:16px}.read{font-size:19px}
.main{margin-top:20px;gap:8px}
.strip{list-style:none;margin:6px 0 0;padding:0;font-size:15px;line-height:1.4}
.strip li{display:grid;grid-template-columns:40px 1fr;gap:8px;padding:8px 0;border-bottom:1px solid #C9C6BF}
.strip li.s{padding-left:0;color:var(--deep);font-size:14px}
.strip b{font-weight:700}
.strip li.back svg{display:block;margin-top:1px}
.tbl tr[data-effect] td{display:inline-block;vertical-align:middle;margin-right:14px}
.left .steps{margin-top:28px}
.tbl thead{display:none}
.tbl tr{display:block;padding:10px 0;border-bottom:1px solid #C9C6BF}
.tbl td,.tbl th{display:block;border:0;padding:2px 0}
section.sec > h2{font-size:24px}
.also{grid-template-columns:1fr}
.also figure{grid-template-columns:150px minmax(0,1fr);gap:12px}
}
"""


def strip_list(lp, reform_id=None, targets=()):
    """The phone's strip: every station and step in order, from twelve o'clock round to the return."""
    out = []
    n = lp["n"]
    for i, s in enumerate(lp["stations"]):
        red = " · reform acts here" if s["code"] in targets else ""
        out.append(f'<li><b>{esc(s["code"] or "")}</b><span>{esc(s["label"])}{esc(red)}</span></li>')
        st = lp["steps"][i]
        if st["id"]:
            sg = "same direction" if st["polarity"] == "+" else "opposite direction"
            red = f" · {reform_id} acts here" if st["id"] in targets else ""
            out.append(f'<li class="s"><b>{esc(st["id"])}</b><span>{D.sign_glyph(st["polarity"])} {sg}, {esc(D.GRADE_WORD[st["evidence"]].lower())}{esc(red)}</span></li>')
    first = lp["stations"][0]
    back = f'Back to {first["code"]}, one turn later' if lp["type"] == "R" else f'Back to {first["code"]}'
    out.append(f'<li><b aria-hidden="true">↺</b><span>{esc(back)}</span></li>')
    return f'<ol class="strip" aria-label="The loop in order">{"".join(out)}</ol>'


def steps_table(model, lp, targets=()):
    N = model["nodes"]
    rows = []
    for s in lp["steps"]:
        sg = ("+ same direction" if s["polarity"] == "+" else f"{D.MINUS} opposite direction")
        weak = "<br><b>Least certain step</b>" if s["id"] in lp["weakest"] else ""
        red = f'<br><span class="redkey" aria-hidden="true"></span><b>Reform acts here</b>' if s["id"] in targets else ""
        rows.append(f'<tr data-link="{esc(s["id"])}" data-from="{esc(s["from"])}" data-to="{esc(s["to"])}" data-sign="{esc(s["polarity"])}" '
                    f'data-grade="{esc(s["evidence"])}" data-delay="{esc(s["delay"])}"><th scope="row">{chip("Connection", s["id"])}</th>'
                    f'<td><b>{esc(s["name"])}</b><br>{esc(s["from"])} {esc(N[s["from"]]["label"])} to {esc(s["to"])} {esc(N[s["to"]]["label"])}{red}</td>'
                    f'<td>{sg}</td><td>{esc(D.GRADE_WORD[s["evidence"]])}: {esc(D.GRADE_GLOSS[s["evidence"]])}{texture_svg(s["evidence"])}{weak}</td>'
                    f'<td>{esc(D.DELAY_WORD[s["delay"]])}</td></tr>')
    return (f'<table class="tbl"><caption>The steps, in order from twelve o\'clock</caption><thead><tr><th scope="col">Step</th><th scope="col">What it says</th>'
            f'<th scope="col">Sign</th><th scope="col">Evidence</th><th scope="col">Delay</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')


def date_long(iso):
    import datetime
    if not iso:
        return None
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def reform_tables(model, rid):
    r = model["reforms"][rid]
    eff = "".join(f'<tr data-family="{k}" data-effect="{esc(v)}"><th scope="row">{esc(model["families"][k])}</th><td>{pips_svg(v)}</td><td>{esc(tm(v))}</td></tr>'
                  for k, v in r["effects"].items())
    routes = []
    for x in r["routes"]:
        chk = date_long(x["checked"])
        routes.append(f'<tr data-route="{esc(x["route"])}" data-checked="{esc(x["checked"] or "")}"><th scope="row">{chip("Route", x["route"])}</th>'
                      f'<td>{esc(model["route_names"][x["route"]])}: {esc(x["who"])}</td><td>{esc(cap1(x["feasibility"]))}</td>'
                      f'<td>{"Checked " + esc(chk) if chk else "Not checked: V7 gives no check date"}</td></tr>')
    t1 = (f'<table class="tbl"><caption>Expected effects, ordinal. The atlas never adds them up.</caption><thead><tr><th scope="col">Family</th>'
          f'<th scope="col">Effect</th><th scope="col">V7 code</th></tr></thead><tbody>{eff}</tbody></table>')
    t2 = (f'<table class="tbl"><caption>Routes to change</caption><thead><tr><th scope="col">Route</th><th scope="col">Who</th>'
          f'<th scope="col">Feasibility</th><th scope="col">Checked</th></tr></thead><tbody>{"".join(routes)}</tbody></table>')
    return t1, t2


def target_name(model, t):
    if t in model["links"]:
        return f'{t}, {model["links"][t]["name"]}'
    return f'{t}, {model["nodes"][t]["title"]}'


def reform_section(model, lp, rid):
    r = model["reforms"][rid]
    drawn = {s["id"] for s in lp["steps"]} | {s["code"] for s in lp["stations"]}
    here = [t for t in r["targets"] if t in drawn]
    away = [t for t in r["targets"] if t not in drawn]
    t1, t2 = reform_tables(model, rid)
    where = "On this loop it acts at " + " and ".join(esc(target_name(model, t)) for t in here) + ", marked in red."
    if away:
        where += " Outside this loop it also acts at " + " and ".join(esc(target_name(model, t)) for t in away) + "."
    others = [x for x in lp["reforms"] if x != rid]
    oth = ""
    if others:
        words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
        oth = (f'<p>Atlas V7 lists {words.get(len(others), len(others))} more reform{"s" if len(others) > 1 else ""} on this loop: '
               + ", ".join(f'{x}, {esc(model["reforms"][x]["title"])}' for x in others) + '. This card names one reform, so only its targets are red.</p>')
    return f'''<section class="sec reform" data-reform="{esc(rid)}"><h2>{chip("Reform", rid)}<span>{esc(r["title"])}</span></h2>
<div class="rgrid"><div><p><span class="redkey" aria-hidden="true"></span>{where}</p><p>{esc(r["summary"])}</p>{oth}
<p><b>Evidence for the problem:</b> {esc(D.GRADE_WORD[r["problem_grade"]])}. <b>Evidence for the remedy:</b> {esc(D.GRADE_WORD[r["remedy_grade"]])}, {esc(D.GRADE_GLOSS[r["remedy_grade"]])}.</p>
<p><b>Confidence in the effects (V7):</b> {esc(r["effects_confidence"])}.</p></div>
<div>{t1}{t2}</div></div></section>'''


def card_page(model, lid, rid, headline, figs, rail_html, title):
    lp = model["loops"][lid]
    targets = set(model["reforms"][rid]["targets"]) if rid else set()
    glyph = D.glyph24(lp["type"])
    kw = "Snowball loop · feeds itself" if lp["type"] == "R" else "Thermostat loop · pushes back"
    body = f'''<div class="wrap"><header class="mast">{wordmark("#121212", 20)}<span class="where">Systems Atlas · Loop card</span></header>
<main><article data-loop="{esc(lid)}" data-reform="{esc(rid or "")}">
<p class="kicker">{chip("Loop", lid)}{glyph}<span>{kw}</span></p>
<h1>{esc(headline)}</h1>
<p class="v7"><span>Atlas V7 title:</span> {esc(lp["title"])}</p>
<p class="read">“{esc(lp["how_to_read"])}”</p>
<div class="main"><div class="left"><figure class="fig">{figs["desk"].replace("<svg ", '<svg class="desk" ', 1)}{figs["phone"].replace("<svg ", '<svg class="phone" ', 1)}{strip_list(lp, rid, targets)}</figure>
<section class="sec steps"><h2>The steps</h2>{steps_table(model, lp, targets)}</section></div>
<aside class="rail" aria-label="Reading the loop">{rail_html}</aside></div>
{reform_section(model, lp, rid) if rid else ""}
<footer class="foot"><p class="src">{esc(SRC)} Loop {esc(lid)}{"; reform " + esc(rid) if rid else ""}. The headline is a studio draft for the editor; every other line on this card is an Atlas V7 field or reads one. Red marks only where {esc(rid)} acts. Specimen for Direction B, Snowball and Thermostat.</p></footer>
</article></main></div>'''
    return page(title, "card", CARD_CSS, body, f"Direction B specimen: loop card for {lid}.")


def rail_block(label, big, *paras, cls=""):
    ps = "".join(f'<p{" class=" + chr(34) + c + chr(34) if c else ""}>{t}</p>' for t, c in paras)
    b = f'<p class="big">{esc(big)}</p>' if big else ""
    return f'<div class="blk {cls}"><p class="lab">{esc(label)}</p>{b}{ps}</div>'


def reform_page(model, rid, headline, fig, phone_fig, also, title):
    r = model["reforms"][rid]
    t1, t2 = reform_tables(model, rid)
    tg = "".join(f'<li>{esc(target_name(model, t))}</li>' for t in r["targets"])
    lp = model["loops"]["R10"]
    body = f'''<div class="wrap"><header class="mast">{wordmark("#121212", 20)}<span class="where">Systems Atlas · Reform view</span></header>
<main><article data-reform="{esc(rid)}">
<p class="kicker">{chip("Reform", rid)}<span>Reform view · acts on three loops</span></p>
<h1>{esc(headline)}</h1>
<p class="v7"><span>Atlas V7 title:</span> {esc(r["title"])}</p>
<p class="read" style="font-family:var(--body);font-style:normal;font-size:17px;line-height:1.55">{esc(r["summary"])}</p>
<div class="main"><figure class="fig">{fig.replace("<svg ", '<svg class="desk" ', 1)}{phone_fig.replace("<svg ", '<svg class="phone" ', 1)}{strip_list(lp, rid, set(r["targets"]))}</figure>
<aside class="rail" aria-label="Where the reform acts">
{rail_block("Where it acts", "Three targets", ("<span class='redkey' aria-hidden='true'></span>All three sit on loop R10, marked in red:", ""), (f"<ul style='margin:0;padding-left:18px'>{tg}</ul>", ""))}
{rail_block("What it changes", None, (esc(r["what_it_changes"]), ""))}
</aside></div>
<section class="sec"><h2>It also lists two more loops</h2><div class="also">{also}</div></section>
<section class="sec reform"><h2>{chip("Reform", rid)}<span>Effects and routes</span></h2><div class="rgrid"><div>{t1}
<p><b>Confidence in the effects (V7):</b> {esc(r["effects_confidence"])}.</p>
<p><b>Evidence for the problem:</b> {esc(D.GRADE_WORD[r["problem_grade"]])}, {esc(D.GRADE_GLOSS[r["problem_grade"]])}. <b>Evidence for the remedy:</b> {esc(D.GRADE_WORD[r["remedy_grade"]])}, {esc(D.GRADE_GLOSS[r["remedy_grade"]])}.</p>
<p>{esc(r["remedy_text"])}</p></div><div>{t2}</div></div></section>
<footer class="foot"><p class="src">{esc(SRC)} Reform {esc(rid)}; loops R10, B4 and R11. The headline is a studio draft for the editor. Red marks only where {esc(rid)} acts. Specimen for Direction B, Snowball and Thermostat.</p></footer>
</article></main></div>'''
    return page(title, "card reform-view", CARD_CSS, body, f"Direction B specimen: reform view for {rid}.")
