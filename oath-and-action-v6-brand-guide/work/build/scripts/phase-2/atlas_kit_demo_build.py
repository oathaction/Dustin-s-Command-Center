"""Build the atlas kit demo page from the model export. Every label, sign, grade, delay and count comes from the
model; nothing is typed by hand. Usage: python3 -I build_kit_demo.py <project root>"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
M = json.loads((ROOT / 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json').read_text())
OUT = ROOT / 'work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Kit-Demo.html'
N, L, LO, RF = M['nodes'], M['links'], M['loops'], M['reforms']
AREAS = {a['id']: a for a in M['areas']}
G = M['glossary']
E = lambda s: html.escape(str(s), quote=True)
GRADE = {'documented': 'documented', 'well-supported': 'well supported', 'plausible': 'plausible',
         'plausible_contested': 'contested', 'hypothesis': 'hypothesis'}
GLOSS = {'documented': 'Documented', 'well-supported': 'Well-supported', 'plausible': 'Plausible',
         'plausible_contested': 'Contested', 'hypothesis': 'Hypothesis'}
DASH = {'documented': None, 'well-supported': None, 'plausible': '9 6', 'plausible_contested': '9 4 2 4', 'hypothesis': '2 4'}
DELAY = {'S': 'under 2 years', 'M': '2 to 10 years', 'L': 'over 10 years'}
SIGN = {'+': ('+', 'same way'), '-': ('−', 'opposite way'), None: ('', 'no direction')}
SNAP = M['generated']['snapshot']


def low(s):
    return s[0].lower() + s[1:] if len(s) > 1 and s[1].islower() else s


def key(kind, i):
    return f'{kind}-{i.lower()}'


def link_words(l):
    s, w = SIGN.get(l['polarity'], ('', 'no direction'))
    return (f"{l['id']}: {l['name']}. From {l['from']} {N[l['from']]['label']} to {l['to']} {N[l['to']]['label']}. "
            f"Sign {s}, {w}. Evidence {GRADE[l['evidence']]}. Delay {DELAY[l['delay']]}.")


# ---------- drawing helpers ----------
def wrap(text, n):
    out, line = [], ''
    for w in text.split():
        if line and len(line) + 1 + len(w) > n:
            out.append(line); line = w
        else:
            line = (line + ' ' + w).strip()
    return out + [line]


def node_svg(nid, x, y, w=280, h=110, extra=''):
    n = N[nid]
    lines = wrap(n['label'], 24)
    ts = ''.join(f'<tspan x="{x + 16}" dy="{0 if i == 0 else 22}">{E(t)}</tspan>' for i, t in enumerate(lines))
    rel = ' '.join([key('link', l['id']) for l in L.values() if nid in (l['from'], l['to']) and l['from'] in DRAWN and l['to'] in DRAWN]
                   + [key('var', o) for l in L.values() if nid in (l['from'], l['to']) for o in (l['from'], l['to']) if o != nid and o in DRAWN])
    say = f"{nid} {n['label']}. {n['increase_means']}"
    return (f'<g class="node" role="button" data-select="{key("var", nid)}" data-node="{nid}" data-rel="{rel}" '
            f'aria-label="{E(say)}" data-say="{E(say)}"{extra}>'
            f'<rect class="ak-mark" x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke-width="1.5"/>'
            f'<text class="nid" x="{x + 16}" y="{y + 28}">{nid}</text>'
            f'<text class="ak-label" data-node="{nid}" data-name="{E(n["label"])}" x="{x + 16}" y="{y + 58}">{ts}</text></g>')


def chevron(x2, y2, dx, dy):
    px, py = -dy, dx
    a = (x2 - dx * 12 + px * 7, y2 - dy * 12 + py * 7)
    b = (x2 - dx * 12 - px * 7, y2 - dy * 12 - py * 7)
    return f'M {a[0]:.0f} {a[1]:.0f} L {x2} {y2} L {b[0]:.0f} {b[1]:.0f}'


def wire_svg(lid, x1, y1, x2, y2, lx, ly, anchor='middle', num=None):
    l = L[lid]
    d = f'M {x1} {y1} L {x2} {y2}'
    dx, dy = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)
    dash = f' stroke-dasharray="{DASH[l["evidence"]]}"' if DASH[l['evidence']] else ''
    s, w = SIGN.get(l['polarity'])
    label = (f'{num} · ' if num else '') + f'{lid} {s}'
    rel = f'{key("var", l["from"])} {key("var", l["to"])}'
    return (f'<g class="wire" role="button" data-select="{key("link", lid)}" data-link="{lid}" data-sign="{l["polarity"] or "none"}" '
            f'data-grade="{l["evidence"]}" data-delay="{l["delay"]}" data-from="{l["from"]}" data-to="{l["to"]}" data-rel="{rel}" '
            f'aria-label="{E(link_words(l))}" data-say="{E(link_words(l))}">'
            f'<path class="ak-case" d="{d}" fill="none"{dash}/>'
            f'<path class="ak-mark" d="{d}" fill="none" stroke-width="2"{dash}/>'
            f'<path class="ak-mark" d="{chevron(x2, y2, dx, dy)}" fill="none" stroke-width="2"/>'
            f'<path class="ak-hit" d="{d}"/>'
            f'<text class="ak-label wl" x="{lx}" y="{ly}" text-anchor="{anchor}">{E(label)}</text></g>')


# ---------- panel templates ----------
def pick(k, text):
    return f'<button type="button" class="ak-btn pick" data-ak-pick="{k}">{E(text)}</button>'


def src():
    return f'<p class="src">Atlas V7, snapshot {SNAP}. Read from the model export of October 28.</p>'


def tpl_var(nid):
    n = N[nid]
    outs = [l for l in L.values() if l['from'] == nid]
    ins = [l for l in L.values() if l['to'] == nid]
    def li(l, other):
        return f'<li>{pick(key("link", l["id"]), l["id"] + " " + l["name"])}<br>{E(other)} {E(N[other]["label"])}, sign {SIGN[l["polarity"]][0]}, {GRADE[l["evidence"]]}</li>'
    loops = ''.join((f'<li><a href="#loop-r10">{lp} {E(LO[lp]["title"])}. Open the loop</a></li>' if lp == 'R10' else f'<li>{lp} {E(LO[lp]["title"])}</li>') for lp in n['loops'])
    refs = [r for r in RF.values() if nid in r['targets']]
    return (f'<template data-detail="{key("var", nid)}" data-kind="Variable {nid}" data-title="{E(n["label"])}">'
            f'<p>{E(n["title"])}. {E(n["increase_means"])}</p>'
            f'<h3>Where it sits</h3><p>Area {n["area"]}, {E(AREAS[n["area"]]["title"])}. Type: {n["type"]}.</p>'
            f'<h3>Pushes ({len(outs)})</h3><ul>{"".join(li(l, l["to"]) for l in outs)}</ul>'
            f'<h3>Pushed by ({len(ins)})</h3><ul>{"".join(li(l, l["from"]) for l in ins)}</ul>'
            f'<h3>Loops it belongs to</h3><ul>{loops}</ul>'
            f'<h3>Reforms that act on it</h3><ul>{"".join(f"<li>{r["id"]} {E(r["title"])}</li>" for r in refs) or "<li>None in the model</li>"}</ul>'
            f'{src()}</template>')


def tpl_link(lid):
    l = L[lid]
    s, w = SIGN[l['polarity']]
    refs = [r for r in RF.values() if lid in r['targets']]
    return (f'<template data-detail="{key("link", lid)}" data-kind="Connection {lid}" data-title="{E(l["name"])}">'
            f'<dl><dt>From</dt><dd>{pick(key("var", l["from"]), l["from"] + " " + N[l["from"]]["label"])}</dd>'
            f'<dt>To</dt><dd>{pick(key("var", l["to"]), l["to"] + " " + N[l["to"]]["label"])}</dd>'
            f'<dt>Sign</dt><dd>{s}, the two move the {w}. A plus sign does not mean a benefit.</dd>'
            f'<dt>Type</dt><dd>{l["type"]}</dd><dt>Delay</dt><dd>{DELAY[l["delay"]]}</dd>'
            f'<dt>Evidence</dt><dd>{GRADE[l["evidence"]]}: {E(G.get(GLOSS[l["evidence"]], ""))}</dd></dl>'
            f'<h3>Loops it closes</h3><ul>{"".join(f"<li>{x} {E(LO[x]["title"])}</li>" for x in l["loops"]) or "<li>None</li>"}</ul>'
            f'<h3>Reforms that act on it</h3><ul>{"".join(f"<li>{r["id"]} {E(r["title"])}</li>" for r in refs) or "<li>None in the model</li>"}</ul>'
            f'{src()}</template>')


def tpl_loop(lp):
    o = LO[lp]
    steps = ''.join(f'<li>{s["id"]}: {E(s["name"])}, sign {SIGN[s["polarity"]][0]}, {GRADE[s["evidence"]]}</li>' for s in o['steps'])
    return (f'<template data-detail="{key("loop", lp)}" data-kind="Loop {lp}" data-title="{E(o["title"])}">'
            f'<p>{E(o["summary"])}</p><dl><dt>Kind</dt><dd>{o["kind_word"]}, {o["kind_gloss"]}</dd>'
            f'<dt>Closure</dt><dd>{E(o["closure"])}</dd><dt>One turn</dt><dd>{o["delay_word"]}</dd>'
            f'<dt>Now</dt><dd>{o["direction_word"]}</dd><dt>Weakest step</dt><dd>{", ".join(o["weakest"]) or "none named"}</dd></dl>'
            f'<h3>Steps</h3><ol>{steps}</ol><h3>Keep in mind</h3><p>{E(o["qualification"])}</p>'
            f'<p class="note">This demo draws R10 up close. The other loops open here.</p>{src()}</template>')


def tpl_reform(rid):
    r = RF[rid]
    eff = ''.join(f'<dt>{E(M["families"][f])}</dt><dd>{E(c)}, {E(M["effect_codes"].get(c, c))}</dd>' for f, c in r['effects'].items())
    routes = ''.join(f'<li>{E(M["route_names"][x["route"]])} ({x["route"]}): {E(x["who"])}. Feasibility {x["feasibility"]}. '
                     f'{"Checked " + x["checked"] if x["checked"] else "Not checked"}.</li>' for x in r['routes'])
    tg = ', '.join(r['targets'])
    return (f'<template data-detail="{key("reform", rid)}" data-kind="Reform {rid}" data-title="{E(r["title"])}">'
            f'<p>{E(r["summary"])}</p><h3>Where it acts</h3><p>Targets {tg}. Their marks in the drawing take the red while this reform is selected.</p>'
            f'<h3>Expected effects</h3><dl>{eff}</dl><p>The four effects are separate judgments and are never added together.</p>'
            f'<dl><dt>Problem evidence</dt><dd>{GRADE.get(r["problem_grade"], r["problem_grade"])}</dd>'
            f'<dt>Remedy evidence</dt><dd>{GRADE.get(r["remedy_grade"], r["remedy_grade"])}</dd></dl>'
            f'<h3>Routes</h3><ul>{routes}</ul>{src()}</template>')


def tpl_area(aid):
    a = AREAS[aid]
    vs = ''.join(f'<li>{v} {E(N[v]["label"])}</li>' for v in a['nodes'])
    grp = next((g for g in M['groups'] if g['id'] == aid), None)
    lps = ', '.join(grp['loops']) if grp else 'none grouped here'
    return (f'<template data-detail="{key("area", aid)}" data-kind="Area {aid}" data-title="{E(a["title"])}">'
            f'<p>{E(a["text"])}</p><h3>Variables ({len(a["nodes"])})</h3><ul>{vs}</ul><h3>Loops grouped here</h3><p>{lps}</p>'
            f'<p class="note">This demo draws area C up close. In a concept, every area opens its own close-up.</p>{src()}</template>')


# ---------- views ----------
DRAWN = set(AREAS['C']['nodes'])
order = [a['id'] for a in M['areas']]
cells = []
for i, aid in enumerate(order):
    a = AREAS[aid]; col, row = i % 5, i // 5
    x, y = 10 + col * 186, 10 + row * 186
    nv = len(a['nodes'])
    lines = wrap(a['title'], 14)
    ts = ''.join(f'<tspan x="{x + 14}" dy="{0 if k == 0 else 21}">{E(t)}</tspan>' for k, t in enumerate(lines))
    letter = aid if len(aid) <= 2 else ''
    inner = (f'<rect class="ak-mark" x="{x}" y="{y}" width="172" height="172" fill="#FFFFFF" stroke-width="1.5"/>'
             f'<text class="big" x="{x + 14}" y="{y + 40}">{E(letter or a["layer"].title())}</text>'
             f'<text class="ak-label ol" x="{x + 14}" y="{y + 76}">{ts}</text>'
             f'<text class="nid" x="{x + 14}" y="{y + 156}">{nv} variables</text>')
    name = f'Area {aid}, {a["title"]}, {nv} variables.'
    if aid == 'C':
        cells.append(f'<a href="#area-c" data-area="C" aria-label="{E(name)} Opens the close-up." data-say="{E(name)} Opens the close-up.">{inner}</a>')
    else:
        cells.append(f'<g role="button" data-select="area-{aid.lower()}" data-area="{aid}" aria-label="{E(name)} Opens a summary." data-say="{E(name)} Opens a summary.">{inner}</g>')
overview_svg = (f'<svg data-view="overview" viewBox="0 0 940 380" role="group" aria-labelledby="h-overview" data-ak-roving data-ak-nav="spatial">'
                + ''.join(cells) + '</svg>')
overview_words = ''.join(
    f'<li><strong>{aid}, {E(AREAS[aid]["title"])}.</strong> {E(AREAS[aid]["text"])} {len(AREAS[aid]["nodes"])} variables.</li>' for aid in order)

# Area C: R10's ring plus C5
P = {'C1': (30, 40), 'C2': (630, 40), 'C3': (630, 250), 'C4': (30, 250), 'C5': (630, 440)}
area_nodes = ''.join(node_svg(n, *P[n]) for n in ['C1', 'C2', 'C3', 'C4', 'C5'])
area_wires = (wire_svg('L08', 310, 95, 630, 95, 470, 82) + wire_svg('L25', 770, 150, 770, 250, 786, 206, 'start')
              + wire_svg('L53', 630, 305, 310, 305, 470, 292) + wire_svg('L42', 170, 250, 170, 150, 186, 206, 'start')
              + wire_svg('L24', 770, 360, 770, 440, 786, 406, 'start'))
area_svg = (f'<svg data-view="area-c" viewBox="0 0 940 560" role="group" aria-labelledby="h-area-c" data-ak-roving data-ak-nav="spatial">'
            + area_wires + area_nodes + '</svg>')
inside = [l for l in L.values() if l['from'] in DRAWN and l['to'] in DRAWN]
crossing = [l for l in L.values() if (l['from'] in DRAWN) != (l['to'] in DRAWN)]
area_words = ''.join(f'<li>{E(link_words(l))}</li>' for l in sorted(inside, key=lambda l: l['id']))
grpC = next(g for g in M['groups'] if g['id'] == 'C')
chips = []
for lp in grpC['loops']:
    o = LO[lp]; steps = ' '.join(s['id'] for s in o['steps'])
    if lp == 'R10':
        chips.append(f'<li><a class="chip ak-mark" href="#loop-r10" data-loop="R10" data-steps="{steps}">R10 {E(o["title"])}. Open the loop</a></li>')
    else:
        chips.append(f'<li><button type="button" class="chip ak-mark" data-select="{key("loop", lp)}" data-loop="{lp}" data-steps="{steps}" aria-pressed="false">{lp} {E(o["title"])}</button></li>')

# Loop R10
R = LO['R10']
ring = {'C1': (30, 60), 'C2': (630, 60), 'C3': (630, 300), 'C4': (30, 300)}
geo = {'L08': (310, 115, 630, 115, 470, 102, 'middle'), 'L25': (770, 170, 770, 300, 786, 241, 'start'),
       'L53': (630, 355, 310, 355, 470, 342, 'middle'), 'L42': (170, 300, 170, 170, 186, 241, 'start')}
seq = []
for st in R['steps']:
    seq.append(st['from'])
    seq.append(st['id'])
# DOM order is the sequence order, so arrow keys walk the loop: C1, L08, C2, L25, C3, L53, C4, L42.
dirs, d = {}, 1
markers = []
mpos = {'C2': (630, 48), 'C3': (630, 288), 'C4': (30, 288)}
start = R['steps'][0]['from']
markers.append(f'<text class="mk" data-ak-at="0" x="30" y="48">Start: more {E(low(N[start]["label"]))}</text>')
loop_items = []
for k, st in enumerate(R['steps'], 1):
    d = d * (1 if st['polarity'] == '+' else -1)
    dirs[k] = d
    word = 'more' if d > 0 else 'less'
    if st['to'] == start:
        markers.append(f'<text class="mk" data-ak-at="{k}" x="186" y="196">Back here: {word} again</text>')
    else:
        x, y = mpos[st['to']]
        markers.append(f'<text class="mk" data-ak-at="{k}" x="{x}" y="{y}">Step {k}: {word}</text>')
for n_ in ['C1', 'C2', 'C3', 'C4']:
    pass
parts = []
for st in R['steps']:
    parts.append(node_svg(st['from'], *ring[st['from']]))
    g = geo[st['id']]
    parts.append(wire_svg(st['id'], *g[:6], anchor=g[6], num=st['index']))
loop_svg = (f'<svg data-view="loop-r10" viewBox="0 0 940 420" role="group" aria-labelledby="h-loop-r10" data-ak-roving data-ak-nav="sequence" data-ak-wrap>'
            + ''.join(parts) + ''.join(markers) + '</svg>')
d = 1
step_lis = []
for k, st in enumerate(R['steps'], 1):
    a = 'More' if d > 0 else 'Less'
    d2 = d * (1 if st['polarity'] == '+' else -1)
    b = 'more' if d2 > 0 else 'less'
    s, w = SIGN[st['polarity']]
    keys = f'{key("link", st["id"])} {key("var", st["to"])}'
    txt = (f'{st["id"]}, {st["name"]}. {a} {low(st["from_label"])} means {b} {low(st["to_label"])}. '
           f'Sign {s}, {w}; {GRADE[st["evidence"]]}; {DELAY[st["delay"]]}.')
    step_lis.append(f'<li data-ak-step-keys="{keys}">{E(txt)}</li>')
    d = d2
minus = sum(1 for st in R['steps'] if st['polarity'] == '-')
end = (f'The loop is back where it started, so it {R["kind_gloss"]}: {R["kind_word"].lower()}. '
       f'Its weakest step is {", ".join(R["weakest"])}, graded {GRADE[L[R["weakest"][0]]["evidence"]]}.')
idle = f'Start at {start}, {N[start]["label"]}, and suppose it rises. Press Play, or Next step to follow one numbered link at a time.'
reform_btns = ''.join(
    f'<li><button type="button" class="chip ak-mark" data-select="{key("reform", r)}" data-reform="{r}" data-targets="{" ".join(RF[r]["targets"])}" '
    f'aria-pressed="false">{r} {E(RF[r]["title"])}</button></li>' for r in R['reforms'])

templates = (''.join(tpl_area(a) for a in order if a != 'C') + ''.join(tpl_var(n) for n in AREAS['C']['nodes'])
             + ''.join(tpl_link(l['id']) for l in sorted(inside, key=lambda l: l['id']))
             + ''.join(tpl_loop(lp) for lp in grpC['loops'] if lp != 'R10') + ''.join(tpl_reform(r) for r in R['reforms']))

legend = ''.join(
    f'<li><svg viewBox="0 0 60 12" width="60" height="12" aria-hidden="true"><path d="M 2 6 L 58 6" stroke="currentColor" stroke-width="2"'
    f'{" stroke-dasharray=" + chr(34) + DASH[g] + chr(34) if DASH[g] else ""}/></svg> {GRADE[g]}</li>'
    for g in ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis'])

PAGE = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="atlas-views" content="overview area-c loop-r10">
<title>Atlas Kit Demo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="atlas-kit.css">
<style>
  body {{ margin: 0; font: 400 16px/1.5 Inter, system-ui, sans-serif; }}
  .top {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px 24px; padding: 14px 32px; border-bottom: 1px solid var(--ak-ink); }}
  .top .eyebrow {{ margin: 0; font: 600 13px/1.4 Inter, sans-serif; letter-spacing: .06em; text-transform: uppercase; }}
  .top .ak-crumbs {{ flex: 1; }}
  .locator {{ display: inline-flex; align-items: center; gap: 8px; color: inherit; font: 500 14px/1.4 Inter, sans-serif; }}
  .locator svg {{ width: 70px; height: 28px; }}
  .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) var(--ak-panel-w); gap: 32px; padding: 24px 32px 48px; }}
  h1 {{ margin: 0 0 8px; font: 700 32px/1.15 Inter, sans-serif; letter-spacing: -.01em; }}
  h2 {{ margin: 28px 0 8px; font: 700 20px/1.25 Inter, sans-serif; }}
  p, li {{ max-width: 68ch; }}
  svg text {{ fill: currentColor; font-family: Inter, sans-serif; }}
  svg .big {{ font-size: 30px; font-weight: 700; }}
  svg .ak-label {{ font-size: 17px; font-weight: 600; }}
  svg .ak-label.ol {{ font-size: 16px; }}
  svg .nid {{ font-size: 15px; }}
  svg .wl {{ font-size: 15px; font-weight: 600; }}
  svg .mk {{ font-size: 15px; font-weight: 700; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 0; padding: 0; list-style: none; }}
  .chip {{ display: inline-block; padding: 8px 12px; background: var(--ak-white); color: var(--ak-ink); font: 500 15px/1.35 Inter, sans-serif;
          text-align: left; cursor: pointer; text-decoration: none; }}
  .chip:hover {{ text-decoration: underline; text-underline-offset: 3px; }}
  .stepper .controls {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 8px; }}
  .stepper ol {{ margin: 8px 0 0; padding-left: 28px; }}
  .status {{ min-height: 1.5em; font-weight: 600; }}
  .key ul {{ margin: 0; padding: 0; list-style: none; }}
  .key li {{ display: flex; align-items: center; gap: 10px; padding: 2px 0; }}
  .pick {{ min-height: 28px; padding: 2px 8px; text-align: left; font-weight: 500; }}
  .ak-panel ul {{ padding: 0; list-style: none; }}
  .ak-panel ul li {{ margin-bottom: 8px; }}
  .src, .note {{ margin-top: 16px; font-size: 14px; }}
  .full-btn {{ margin-top: 8px; }}
  @media (min-width: 900px) {{ .full-btn {{ display: none; }} }}
  @media (max-width: 899.98px) {{
    .top {{ padding: 12px 16px; }}
    .top .ak-crumbs {{ order: 3; flex-basis: 100%; }}
    .layout {{ grid-template-columns: minmax(0, 1fr); padding: 16px; }}
    h1 {{ font-size: 26px; }}
  }}
</style>
</head>
<body data-surface="newsprint">
<header class="top">
  <p class="eyebrow">Atlas kit demo</p>
  <nav class="ak-crumbs" aria-label="Breadcrumb" data-ak-crumbs></nav>
  <a class="locator" href="#overview"><svg viewBox="0 0 70 28" aria-hidden="true">{"".join(f'<rect data-locate="area-{a.lower()}" class="ak-mark" x="{1 + (i % 5) * 14}" y="{1 + (i // 5) * 14}" width="12" height="12" fill="none" stroke-width="1.5"/>' for i, a in enumerate(order))}</svg>Overview</a>
</header>
<p class="ak-vh" role="status" data-ak-status></p>
<div class="layout">
<main class="ak-stage" id="main">

<section data-view-root="overview" data-crumb="Overview" aria-labelledby="h-overview">
  <h1 id="h-overview" data-ak-heading>The system in <span data-count="areas">{len(order)}</span> areas</h1>
  <p>Select an area to read about it. Area C opens its close-up, and the other nine open a summary beside the map. The model holds <span data-count="variables">{M["generated"]["counts"]["variables"]}</span> variables and <span data-count="connections">{M["generated"]["counts"]["connections"]}</span> connections.</p>
  <div class="ak-scroll" id="map-overview" role="region" tabindex="0" aria-label="Map of the ten areas" style="--ak-min: 940px; --ak-full-w: 1200px">{overview_svg}</div>
  <p class="ak-readout" data-ak-readout>Point at or tab to an area to read its name here.</p>
  <button type="button" class="ak-btn full-btn" data-ak-full="map-overview">View the map full size</button>
  <h2>The areas in words</h2>
  <ol>{overview_words}</ol>
</section>

<section data-view-root="area-c" data-crumb="Area C, {E(AREAS["C"]["title"])}" data-parent="overview" aria-labelledby="h-area-c" hidden>
  <h1 id="h-area-c" data-ak-heading>Area C: {E(AREAS["C"]["title"])}</h1>
  <p>{E(AREAS["C"]["text"])} The drawing shows its {len(DRAWN)} variables and the {len(inside)} connections inside it; {len(crossing)} more cross its edge.</p>
  <div class="ak-scroll" id="map-area-c" role="region" tabindex="0" aria-label="Area C drawing" style="--ak-min: 940px">{area_svg}</div>
  <p class="ak-readout" data-ak-readout>Point at or tab to a variable or a connection to read it here.</p>
  <button type="button" class="ak-btn full-btn" data-ak-full="map-area-c">View the drawing full size</button>
  <h2>Loops in this area</h2>
  <ul class="chips" data-ak-roving data-ak-nav="sequence">{"".join(chips)}</ul>
  <h2>The lines in words</h2>
  <ol>{area_words}</ol>
</section>

<section data-view-root="loop-r10" data-crumb="Loop R10" data-parent="area-c" aria-labelledby="h-loop-r10" hidden>
  <h1 id="h-loop-r10" data-ak-heading>R10: {E(R["title"])}</h1>
  <p>{E(R["summary"])}</p>
  <div class="ak-scroll" id="map-loop-r10" role="region" tabindex="0" aria-label="Loop R10 drawing" style="--ak-min: 940px">{loop_svg}</div>
  <p class="ak-readout" data-ak-readout>Use the arrow keys to walk the loop one link at a time.</p>
  <button type="button" class="ak-btn full-btn" data-ak-full="map-loop-r10">View the loop full size</button>
  <section class="stepper" data-ak-stepper data-ak-hold="3200" data-ak-end="{E(end)}" aria-labelledby="h-steps">
    <h2 id="h-steps">Follow the loop</h2>
    <div class="controls"><button type="button" class="ak-btn" data-ak-step="play">Play</button><button type="button" class="ak-btn" data-ak-step="prev">Previous step</button><button type="button" class="ak-btn" data-ak-step="next">Next step</button><button type="button" class="ak-btn" data-ak-step="reset">Reset</button></div>
    <p class="status" data-ak-step-status aria-live="polite">{E(idle)}</p>
    <ol data-ak-step-list>{"".join(step_lis)}</ol>
  </section>
  <h2>Where reforms enter</h2>
  <ul class="chips" data-ak-roving data-ak-nav="sequence">{reform_btns}</ul>
</section>

</main>
<div class="side">
  <aside class="ak-panel" data-ak-panel aria-labelledby="ak-panel-title" hidden>
    <div class="ak-panel-bar"><p data-ak-panel-kind></p><button type="button" class="ak-btn" data-ak-sheet-toggle aria-expanded="false">More</button><button type="button" class="ak-btn" data-ak-close>Close</button></div>
    <h2 id="ak-panel-title" data-ak-panel-title tabindex="-1"></h2>
    <div data-ak-panel-body></div>
  </aside>
  <section class="key" aria-labelledby="h-key">
    <h2 id="h-key">How to read a wire</h2>
    <p>The line's texture gives its evidence grade. A plus sign means the two variables move the same way; a minus sign means they move opposite ways. Neither means good or bad.</p>
    <ul>{legend}</ul>
  </section>
</div>
</div>
{templates}
<script src="atlas-kit.js"></script>
<script>AtlasKit.init();</script>
</body>
</html>
'''
assert '—' not in PAGE, 'em dash in page'
OUT.write_text(PAGE)
print('wrote', OUT, len(PAGE), 'bytes')
