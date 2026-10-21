"""Build work/boards/20261021_Symbol-Family-Board.html (Phase 1, design director).

Run after symbols_measure.py:  python3 -I symbols_board_build.py
Optional: symbols_board_check.js writes a layout and type check that a second run of
this script folds into the board.
"""
import html
import json
import math
import random
import re
import subprocess
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import symbols_family as F  # noqa: E402
import symbols_measure as M  # noqa: E402
from symbols_geom import circle, d_of, flatten_segments, minus, rect, transform, union  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = HERE.parents[3]
BOARD = ROOT / "work/boards/20261021_Symbol-Family-Board.html"
ASSETS = "phase-1/symbols"
MEAS = json.loads((ROOT / "work/boards/phase-1/symbols/20261021_Symbol-Family-Measurements.json").read_text())
CHECK = ROOT / "work/boards/phase-1/symbols/20261021_Symbol-Family-Board-Check.json"
SCRATCH = M.SCRATCH
NEWS, CHAR, WHITE, PRUS, RED, STONE, VERD = M.NEWS, M.CHAR, M.WHITE, M.PRUS, M.RED, M.STONE, M.VERD
RED_RULE = "The wordmark's ampersand and the lockmark's lever are signature red and do not count. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand is Charcoal. The Act handle is red only when the Act mark is itself the call to act, as on a social tile. Red never sits on Prussian."
PL = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act"}
TL = {"filled": "Filled", "line": "Line", "tile": "Tile"}
DL = {"A": "A, geometric solid", "B": "B, line with one accent"}
SURF = [("newsprint", "Newsprint"), ("white", "White"), ("charcoal", "Charcoal"), ("prussian", "Prussian")]
SIM_PASS = 0.60
CROSS_PASS = 0.70


def e(s):
    return html.escape(str(s), quote=True)


def num(v, nd=2):
    """Format a number with a true minus sign."""
    if abs(v) < 0.5 * 10 ** -nd:
        v = 0.0
    s = f"{v:.{nd}f}"
    return s.replace("-", "\u2212")


# ------------------------------------------------------------------ sprite

def sym_mark(sid, lay, vb):
    return (f'<symbol id="{sid}" viewBox="0 0 {vb} {vb}">'
            f'<path d="{d_of(lay["body"])}" fill="currentColor"/>'
            f'<path d="{d_of(lay["seat"])}" style="fill:var(--seat,none)"/>'
            f'<path d="{d_of(lay["node"])}" style="fill:var(--node,currentColor)"/></symbol>')


def sym_tile(sid, lay, vb):
    node_fill = "var(--node,currentColor)" if lay.get("hole") else "var(--node,var(--knock,#DCD9D2))"
    return (f'<symbol id="{sid}" viewBox="0 0 {vb} {vb}">'
            f'<path d="{d_of(lay["plate"])}" fill="currentColor"/>'
            f'<path d="{d_of(lay["body"])}" style="fill:var(--knock,#DCD9D2)"/>'
            f'<path d="{d_of(lay["seat"])}" style="fill:var(--tseat,none)"/>'
            f'<path d="{d_of(lay["node"])}" style="fill:{node_fill}"/></symbol>')


def v5_symbol(name):
    s = (M.SPRITE / f"{name}.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>", "", s, flags=re.S)
    inner = re.sub(r"</svg>\s*$", "", inner)
    inner = re.sub(r"<title>.*?</title>", "", inner)
    return f'<symbol id="v5-{name}" viewBox="{vb}">{inner}</symbol>'


def sprite():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">']
    for d in F.DIRECTIONS:
        for t in ("filled", "line"):
            for p in F.PILLARS:
                for m in (16, 24):
                    out.append(sym_mark(f"p-{d}-{t}-{p}-{m}", F.draw(p, d, t, m), m))
        for p in F.PILLARS:
            for m in (16, 24, 48):
                out.append(sym_tile(f"tile-{d}-{p}-{m}", F.draw(p, d, "tile", m), m))
    for n in F.TOPICS:
        for m in (16, 24):
            out.append(sym_mark(f"tp-{n}-{m}", F.topic(n, m), m))
    for p in F.PILLARS:
        out.append(v5_symbol(f"pm-{p}"))
        out.append(v5_symbol(f"pm-{p}-s"))
    for n in F.TOPICS:
        for m in (16, 24, 48):
            out.append(v5_symbol(f"ic-{n}-{m}"))
    out.append("</svg>")
    return "".join(out)


def use(sid, size, vb, cls="", label=None):
    aria = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true"'
    return f'<svg class="mk {cls}" width="{size}" height="{size}" viewBox="0 0 {vb} {vb}" {aria} focusable="false"><use href="#{sid}" width="{vb}" height="{vb}"/></svg>'


def mark(d, t, p, size, cls="", label=None):
    if t == "tile":
        m = 48 if size >= 48 else size
        return use(f"tile-{d}-{p}-{m}", size, m, ("tile " + cls).strip(), label)
    m = 16 if size == 16 else 24
    return use(f"p-{d}-{t}-{p}-{m}", size, m, cls, label)


def v5(name, size, mono=True, label=None):
    style = ' style="--pc:currentColor;--dot:currentColor"' if mono else ""
    aria = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true"'
    vb = re.search(r'viewBox="([^"]+)"', (M.SPRITE / f"{name}.svg").read_text()).group(1)
    return f'<svg class="mk" width="{size}" height="{size}" viewBox="{vb}" {aria}{style} focusable="false"><use href="#v5-{name}"/></svg>'


def zoom(file, px, scale, alt):
    w = px * scale
    return f'<span class="gw" style="--g:{scale}px"><img class="pix" src="{ASSETS}/px/{file}" width="{w}" height="{w}" alt="{e(alt)}"></span>'


# ------------------------------------------------------------------ data helpers

def mk(d, t, p, sz):
    return MEAS["marks"][f"{d}|{t}|{p}|{sz}"]


def pair(d, t, a, b, sz):
    k = f"{d}|{t}|{a}|{b}|{sz}"
    if k not in MEAS["pairs"]:
        k = f"{d}|{t}|{b}|{a}|{sz}"
    return MEAS["pairs"][k]


WATCH = {"track": ["status light", "Signal Grid lockmark"], "act": ["letter D", "play button", "outbound arrow (ui-external)", "V5 outbound arrow (pm-act)"],
         "explain": ["copyright sign", "letter C", "letter L"], "connect": ["V5 chain link (pm-connect)", "copyright sign"]}


def checks(d, t, p):
    """The nine craft checks for one drawing (both masters). Returns list of (status, detail)."""
    m16, m24, m96 = mk(d, t, p, 16), mk(d, t, p, 24), mk(d, t, p, 96)
    out = []
    # 1 silhouette
    if t == "tile":
        ok = m16["crisp"] >= 0.60
        out.append((ok, f"Plate gives the silhouette; mark crisp share {num(m16['crisp'])}"))
    else:
        ok = m16["crisp"] >= 0.60 and m16["density"] >= 0.25
        out.append((ok, f"Crisp share {num(m16['crisp'])}, ink {num(m16['density'])}"))
    # 2 pixel fit
    s16, s24 = m16["pixel_fit"]["share"], m24["pixel_fit"]["share"]
    ok = s16 == 1.0 and s24 == 1.0
    out.append((ok, f"16 px {m16['pixel_fit']['on_grid']} of {m16['pixel_fit']['checked']}; 24 px {m24['pixel_fit']['on_grid']} of {m24['pixel_fit']['checked']}"))
    # 3 consistency
    exc = m16.get("exception") or m24.get("exception")
    ok = bool(m16["consistent"] and m24["consistent"])
    out.append((ok, exc or f"Node {num(m16['node_r'] * 2, 0)} px at 16, {num(m24['node_r'] * 2, 0)} px at 24; ring 1 px"))
    # 4 optical balance
    dens = [mk(d, t, q, 96)["density"] for q in F.PILLARS]
    med = sorted(dens)[1:3]
    med = sum(med) / 2
    dev = m96["density"] / med - 1
    cx, cy = m96["centroid"]
    ok = abs(dev) <= 0.20 and abs(cx) <= 0.12 and abs(cy) <= 0.12
    out.append((ok, f"Ink {num(dev * 100, 0)}% from set median; center offset {num(cx)}, {num(cy)}"))
    # 5 similarity
    worst = max(((pair(d, t, p, q, sz)["score"], q, sz) for q in F.PILLARS if q != p for sz in (16, 24)))
    if t == "tile":
        ok = worst[0] < SIM_PASS
        out.append((ok, f"Nearest pillar {PL[worst[1]]} {num(worst[0])} at {worst[2]} px, inside the plate; watch items as for the drawing it holds"))
    else:
        wwatch = max(((MEAS["watch"][f"{d}|{t}|{p}|{nm}|{sz}"]["score"], nm, sz) for nm in WATCH[p] for sz in (16, 24)))
        ok = worst[0] < SIM_PASS and wwatch[0] < SIM_PASS
        out.append((ok, f"Nearest pillar {PL[worst[1]]} {num(worst[0])} at {worst[2]} px; nearest watch item {wwatch[1]} {num(wwatch[0])}"))
    # 6 monochrome
    ok = all(m16["node_separate"].values()) and all(m24["node_separate"].values())
    out.append((ok, "Node stays separate in Charcoal on Newsprint and Newsprint on Charcoal, 16 and 24 px" if ok else "Node merges with the body in one color"))
    # 7 red discipline
    if p == "act":
        out.append((True, "Red only on the handle, and only where the Act mark is the call to act"))
    else:
        out.append((True, "No red"))
    # 8 contrast
    if p == "act" and t != "tile":
        ring = min(MEAS["red"][f"{d}|{t}|24|{s}"]["ring_vs_red"] for s in ("newsprint", "white", "charcoal"))
        out.append((ring >= 3.0, f"Ink 9.42 to 18.73; red to its ring {num(ring)} at 24 px, 4.49 at 48 px; no red on Prussian"))
    else:
        out.append((True, "Ink 9.42 to 18.73 on all four surfaces"))
    # 9 type
    out.append((None, "No type in the mark"))
    return out


def topic_checks(n):
    t16, t24, t48 = (MEAS["topics"][f"metrics|{n}|{s}"] for s in (16, 24, 48))
    out = []
    out.append((t16["crisp"] >= 0.60 and t16["density"] >= 0.25, f"Crisp share {num(t16['crisp'])}, ink {num(t16['density'])}"))
    ok = t16["pixel_fit"]["share"] == 1.0 and t24["pixel_fit"]["share"] == 1.0
    out.append((ok, f"16 px {t16['pixel_fit']['on_grid']} of {t16['pixel_fit']['checked']}; 24 px {t24['pixel_fit']['on_grid']} of {t24['pixel_fit']['checked']}"))
    ok = abs(t16["node_r"] - 1.5) < 0.06 and abs(t24["node_r"] - 2.0) < 0.06
    out.append((ok, f"Node {num(t16['node_r'] * 2, 0)} px at 16, {num(t24['node_r'] * 2, 0)} px at 24; ring 1 px"))
    dens = sorted(MEAS["topics"][f"metrics|{q}|48"]["density"] for q in F.TOPICS)
    med = (dens[1] + dens[2]) / 2
    dev = t48["density"] / med - 1
    out.append((abs(dev) <= 0.20, f"Ink {num(dev * 100, 0)}% from set median"))
    worst = max(((MEAS["topics"][key]["score"], q, sz) for q in F.TOPICS if q != n for sz in (16, 24)
                 for key in (f"new|{n}|{q}|{sz}", f"new|{q}|{n}|{sz}") if key in MEAS["topics"]))
    cross = max(((MEAS["topics"][f"vspillar|{n}|{p}|{sz}"]["score"], p, sz) for p in F.PILLARS for sz in (16, 24)))
    ok = worst[0] < SIM_PASS and cross[0] < CROSS_PASS
    out.append((ok, f"Nearest topic {F.TOPIC_LABELS[worst[1]]} {num(worst[0])} at {worst[2]} px; nearest pillar {PL[cross[1]]} {num(cross[0])}"))
    ok = all(t16["node_separate"].values()) and all(t24["node_separate"].values())
    out.append((ok, "Node stays separate in both polarities, 16 and 24 px"))
    out.append((True, "No red; in an Act module the node may turn red"))
    out.append((True, "Ink 9.42 to 18.73 on all four surfaces"))
    out.append((None, "No type in the mark"))
    return out


def status_cell(st, detail):
    if st is None:
        return f'<td class="ck na"><span class="st">Not applicable</span><span class="dt">{e(detail)}</span></td>'
    return f'<td class="ck {"ok" if st else "no"}"><span class="st">{"Pass" if st else "Fail"}</span><span class="dt">{e(detail)}</span></td>'


# ------------------------------------------------------------------ sections

CHECK_NAMES = ["Silhouette", "Pixel fit", "Consistency", "Optical balance", "Similarity", "Monochrome", "Red discipline", "Contrast", "Type"]


def matrix(d, t):
    rows = []
    for sid, sname in SURF:
        cells = [f'<div class="s-{sid} mx"><p class="sname">{sname}</p><div class="mgrid" aria-hidden="true"><span></span><span class="sz">16</span><span class="sz">24</span><span class="sz">48</span><span class="sz">96</span></div>']
        for p in F.PILLARS:
            marks = "".join(f'<span class="mc">{mark(d, t, p, s)}</span>' for s in (16, 24, 48, 96))
            cells.append(f'<div class="mgrid" role="group" aria-label="{PL[p]}, {TL[t].lower()}, Direction {d}, on {sname}, at 16, 24, 48 and 96 px"><span class="pl">{PL[p]}</span>{marks}</div>')
        cells.append("</div>")
        rows.append("".join(cells))
    return f'<div class="surfaces matrix">{"".join(rows)}</div>'


def zooms(d, t):
    items = []
    for p in F.PILLARS:
        f16 = f"n-{d}-{t}-{p}-16.png"
        f24 = f"n-{d}-{t}-{p}-24.png"
        items.append(f'<figure class="zf">{zoom(f16, 16, 8, f"{PL[p]} {t} 16 px at 8 times")}<figcaption>{PL[p]}, 16 px at 8x</figcaption></figure>')
        items.append(f'<figure class="zf">{zoom(f24, 24, 6, f"{PL[p]} {t} 24 px at 6 times")}<figcaption>{PL[p]}, 24 px at 6x</figcaption></figure>')
    return f'<div class="zrow">{"".join(items)}</div>'


def accent_panel(d):
    out = ['<div class="surfaces matrix">']
    for sid, sname in SURF:
        cls = "accent" if sid != "prussian" else ""
        out.append(f'<div class="s-{sid} mx"><p class="sname">{sname}</p>')
        for t in F.TREATMENTS:
            marks = "".join(f'<span class="mc">{mark(d, t, "act", s, cls)}</span>' for s in (24, 48, 96))
            out.append(f'<div class="arow" role="group" aria-label="Act {t} on {sname}"><span class="pl">{TL[t]}</span>{marks}</div>')
        note = "One color only. Red never sits on Prussian." if sid == "prussian" else ("Red handle inside a Charcoal ring" if sid != "charcoal" else "Red handle in a knocked-out seat, against Charcoal")
        out.append(f'<p class="cap">{note}</p></div>')
    out.append("</div>")
    return "".join(out)


def composition(d):
    t_social = "filled" if d == "A" else "line"
    t_kick = "filled" if d == "A" else "line"
    social = f'''<figure class="comp">
<div class="social s-newsprint" role="img" aria-label="Square social post for an Act piece, with the Act mark and a headline"><div class="so-in">
  <div class="so-top">{mark(d, t_social, "act", 96, "accent so-mark")}<p class="so-kicker">Act</p></div>
  <p class="so-head">How to speak at a public hearing in your state</p>
  <p class="so-dek">Find the hearing, sign up, then say who you are and what the rule changes for you.</p>
  <p class="so-foot"><span class="so-sig">Oath &amp; Action</span><span class="so-series">{mark(d, "tile", "act", 24)}<span>Act series</span></span></p>
</div></div>
<figcaption><span class="tag">Illustrative</span> 1080 by 1080 post shown at one third. Headline and steps are example copy, labeled here as illustrative. The signature is set in type as a stand-in; the identity board owns the wordmark. One working red: the Act handle, because the mark is the call to act.</figcaption>
</figure>'''
    stories = []
    heads = {"explain": "What a primary election decides, and who can vote in one",
             "track": "Where the state budget bill stands this week",
             "connect": "Three groups on opposite sides agreed on one change to the ballot",
             "act": "Ask for a hearing date before the committee votes"}
    topics = {"explain": "Elections", "track": "Budget", "connect": "Ballot access", "act": "Hearings"}
    for p in F.PILLARS:
        stories.append(f'<li><p class="ki">{mark(d, t_kick, p, 24)}<span class="kp">{PL[p]}</span><span class="kt">{topics[p]}</span><span class="tag ki-il">Illustrative</span></p><p class="kh">{heads[p]}</p></li>')
    kicker = f'''<figure class="comp">
<div class="article s-white">
  <p class="ki">{mark(d, t_kick, "explain", 24)}<span class="kp">Explain</span><span class="kt">Elections</span></p>
  <p class="ah">What a primary election decides, and who can vote in one</p>
  <p class="cap" style="margin:0 0 8px"><span class="tag">Illustrative</span> Headline and dek are example copy.</p>
  <p class="ad">The rules differ by state. Four questions tell you which kind your state runs and whether you can take part.</p>
  <ul class="stories" aria-label="Story list with pillar kickers">{"".join(stories)}</ul>
</div>
<figcaption><span class="tag">Illustrative</span> Article kicker and a story list at 1:1, 24 px marks. Each story carries its pillar in Charcoal. No mark here is a call to act, so the view spends no working red.</figcaption>
</figure>'''
    return f'<div class="comps">{social}{kicker}</div>'


def skeleton_card(p):
    """Construction drawing on the 24-unit grid at 10x, beside the V5 original and both derived marks."""
    S = 10
    g = []
    g.append(f'<svg class="cons" viewBox="-8 -8 256 256" width="256" height="256" role="img" aria-label="{PL[p]} skeleton on the 24-unit grid">')
    g.append('<rect x="0" y="0" width="240" height="240" fill="#F4F2EE"/>')
    for i in range(25):
        w = 0.6 if i % 2 else 0.9
        g.append(f'<line x1="{i * S}" y1="0" x2="{i * S}" y2="240" stroke="#9EA2A8" stroke-width="{w}"/>')
        g.append(f'<line x1="0" y1="{i * S}" x2="240" y2="{i * S}" stroke="#9EA2A8" stroke-width="{w}"/>')
    g.append(f'<rect x="20" y="20" width="200" height="200" fill="none" stroke="{VERD}" stroke-width="1.5"/>')
    g.append(f'<line x1="0" y1="120" x2="240" y2="120" stroke="{PRUS}" stroke-width="1"/>')
    g.append(f'<line x1="120" y1="0" x2="120" y2="240" stroke="{PRUS}" stroke-width="1"/>')
    sk = F.SKELETON_24[p]
    st = f'fill="none" stroke="{CHAR}" stroke-width="2"'
    if p == "explain":
        x, y, w, h = sk["square"]
        nxs, nys, nw, nh = sk["notch"]
        g.append(f'<path d="M{x*S} {y*S}H{nxs*S}V{(nys+nh)*S}H{(x+w)*S}V{(y+h)*S}H{x*S}Z" {st}/>')
        g.append(f'<rect x="{nxs*S}" y="{nys*S}" width="{nw*S}" height="{nh*S}" fill="none" stroke="{STONE}" stroke-width="1.5"/>')
        qx, qy, qw, qh = sk["quarter"]
        g.append(f'<rect x="{qx*S}" y="{qy*S}" width="{qw*S}" height="{qh*S}" {st}/>')
        g.append(f'<line x1="{nxs*S}" y1="{(nys+nh)*S}" x2="{qx*S}" y2="{(qy+qh)*S}" stroke="{PRUS}" stroke-width="1.5"/>')
    elif p == "track":
        pts = "M20 220V170H80V120H160V70H220V220Z"
        g.append(f'<path d="{pts}" {st}/>')
        g.append(f'<path d="M20 170H80V120H160V70H220" fill="none" stroke="{PRUS}" stroke-width="1.5"/>')
    elif p == "connect":
        g.append(f'<circle cx="120" cy="120" r="100" {st}/>')
        g.append(f'<rect x="80" y="20" width="80" height="200" fill="#F4F2EE" stroke="{STONE}" stroke-width="1.5"/>')
    elif p == "act":
        g.append(f'<path d="M30 20L110 50V220H30Z" {st}/>')
        g.append(f'<path d="M120 20H210V220H180V50H120Z" {st}/>')
        g.append(f'<line x1="110" y1="50" x2="110" y2="220" stroke="{PRUS}" stroke-width="1.5"/>')
    nx, ny = sk["node"]
    g.append(f'<circle cx="{nx*S}" cy="{ny*S}" r="30" fill="none" stroke="{STONE}" stroke-width="1.5"/>')
    g.append(f'<circle cx="{nx*S}" cy="{ny*S}" r="20" fill="{CHAR}"/>')
    g.append("</svg>")
    v5name = f"pm-{p}"
    derived = (f'<div class="der"><span>{mark("A", "filled", p, 48, label=f"{PL[p]}, Direction A")}<small>A</small></span>'
               f'<span>{mark("B", "line", p, 48, label=f"{PL[p]}, Direction B")}<small>B</small></span></div>')
    watch = {"explain": "No letter C, no copyright sign: square primitives only, and the node sits between two pieces.",
             "track": "No status light: one node, no row of colored circles. No tree, so it stays apart from the Signal Grid.",
             "connect": "No chain link: the halves never interlock. Same size and color on both sides, so neither side leads.",
             "act": "No letter D, no play button, no outbound arrow: straight edges, a frame and a leaf, no arrowhead."}[p]
    return f'''<article class="sk panel">
<h3>{PL[p]}</h3>
<div class="sk-row">
  <figure class="orig"><div class="s-newsprint pad">{v5(v5name, 96, mono=False, label=f"V5 {PL[p]} mark")}</div><figcaption><span class="tag">Original</span> V5 <code>{v5name}</code></figcaption></figure>
  <figure class="cons-f">{"".join(g)}<figcaption><span class="tag">Option</span> Skeleton, 24-unit grid at 10x. Green: live area 2 to 22. Blue: center lines. Gray: the part removed or held apart, and the node's clear seat.</figcaption></figure>
  <figure class="derf">{derived}<figcaption>Derived at 48 px</figcaption></figure>
</div>
<p>{e(sk["note"])}</p>
<p class="cap">{e(watch)}</p>
</article>'''


def hinge_row():
    items = []
    for i, p in enumerate(F.PILLARS):
        items.append(f'<div class="hr-m">{mark("A", "filled", p, 48, label=f"{PL[p]}, Direction A")}<span>{PL[p]}</span></div>')
        if i < 3:
            items.append('<div class="hr-l" aria-hidden="true"></div>')
    return f'<div class="hrow s-newsprint" role="group" aria-label="The four Direction A pillar marks in order, joined by one line through their nodes">{"".join(items)}</div>'


def hinge_schematic():
    amp = re.search(r' d="([^"]+)"', (M.SPRITE / "amp.svg").read_text()).group(1)
    return (f'<svg viewBox="0 0 470 110" width="470" height="110" class="hsch" role="img" aria-label="Schematic of the hinge: Oath, a node, the ampersand in a ring, a node, Action">'
            f'<text x="10" y="64" font-family="Inter Tight, sans-serif" font-weight="800" font-size="30" fill="{CHAR}">OATH</text>'
            f'<line x1="104" y1="54" x2="178" y2="54" stroke="{CHAR}" stroke-width="2"/><circle cx="104" cy="54" r="5" fill="{CHAR}"/><circle cx="178" cy="54" r="5" fill="{CHAR}"/>'
            f'<circle cx="210" cy="54" r="32" fill="none" stroke="{CHAR}" stroke-width="1.5"/>'
            f'<path d="{amp}" transform="translate(186 78) scale(0.07 -0.07)" fill="{CHAR}"/>'
            f'<line x1="242" y1="54" x2="316" y2="54" stroke="{CHAR}" stroke-width="2"/><circle cx="242" cy="54" r="5" fill="{CHAR}"/><circle cx="316" cy="54" r="5" fill="{CHAR}"/>'
            f'<text x="324" y="64" font-family="Inter Tight, sans-serif" font-weight="800" font-size="30" fill="{CHAR}">ACTION</text></svg>')


def alternatives():
    a = union(transform(F.stroke_path([("M", 6, 6), ("L", 18, 18)], 4, "butt", "miter"), 1), F.stroke_path([("M", 18, 6), ("L", 6, 18)], 4, "butt", "miter"))
    a = union(minus(a, circle(12, 12, 4)), circle(12, 12, 2.5))
    lay = F.draw("explain", "A", "filled", 24)
    ring = minus(circle(12, 12, 11.5), circle(12, 12, 10))
    inner = transform(union(lay["body"], lay["node"]), 0.66, 4.08, 4.08)
    b = union(ring, inner)
    t = F.draw("track", "A", "filled", 24)
    c = union(transform(union(t["body"], t["node"]), 0.8, 2.4, 0), rect(2, 21, 20, 2))
    def s(path):
        return f'<svg width="48" height="48" viewBox="0 0 24 24" aria-hidden="true"><path d="{d_of(path)}" fill="currentColor"/></svg>'
    items = [(a, "The ampersand's crossing", "At 16 px the crossing becomes an X, which readers know as close or wrong. It also borrows the master ampersand, which the identity board is refining."),
             (b, "A ring around every mark", "Four rings make four badges of the same shape, and a ring with a center point drifts toward the copyright sign."),
             (c, "A shared baseline bar", "A bar under every mark adds the same shape to all four, which pulls them together at small sizes, the opposite of what Track and Act need.")]
    return "".join(f'<figure class="alt panel"><div class="s-newsprint pad">{s(pth)}</div><figcaption><strong>{e(h)}</strong> <span class="tag">Not chosen</span><br>{e(t)}</figcaption></figure>' for pth, h, t in items)


# ------------------------------------------------------------------ sanctioned treatment sketches

def iso_diagram():
    W, H = 300, 300
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">']
    cx, w, h, th = 150, 250, 125, 12
    for i in range(3):
        cy = 64 + i * 86
        top = f"M{cx} {cy - h / 2}L{cx + w / 2} {cy}L{cx} {cy + h / 2}L{cx - w / 2} {cy}Z"
        left = f"M{cx - w / 2} {cy}L{cx} {cy + h / 2}L{cx} {cy + h / 2 + th}L{cx - w / 2} {cy + th}Z"
        right = f"M{cx + w / 2} {cy}L{cx} {cy + h / 2}L{cx} {cy + h / 2 + th}L{cx + w / 2} {cy + th}Z"
        out.append(f'<path d="{left}" fill="#C9C6BE" stroke="{CHAR}" stroke-width="1.2"/><path d="{right}" fill="#B3B0A8" stroke="{CHAR}" stroke-width="1.2"/><path d="{top}" fill="#EEECE7" stroke="{CHAR}" stroke-width="1.5"/>')
        for j in range(3):
            out.append(f'<circle cx="{cx - 52 + j * 52}" cy="{cy - 8 + (j % 2) * 16}" r="4.5" fill="{CHAR}"/>')
        out.append(f'<circle cx="{cx + w / 2 - 24}" cy="{cy}" r="11" fill="{CHAR}"/><text x="{cx + w / 2 - 24}" y="{cy + 5}" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#DCD9D2">{i + 1}</text>')
    out.append(f'<line x1="{cx + 52}" y1="{64 + 8}" x2="{cx + 52}" y2="{64 + 2 * 86 + 8}" stroke="{CHAR}" stroke-width="1.5"/>')
    out.append("</svg>")
    labels = ["Technology and its effects", "Power and accountability", "How the economy reaches a household"]
    ol = "".join(f"<li>{e(x)}</li>" for x in labels)
    return f'<div class="iso" role="img" aria-label="Sketch of an exploded layer diagram: three isometric slabs, numbered 1 to 3, with flat labels">{"".join(out)}<ol class="isol">{ol}</ol></div>'


def hand_drawn():
    """Texture study: the Ballot topic drawing traced with jittered double strokes (seeded)."""
    rnd = random.Random(20261021)
    lay = F.topic("ballot", 24)
    S = 7
    paths = []
    for key in ("body", "node"):
        for seg in flatten_segments(lay[key]):
            if seg[0] == "L":
                pts = [seg[1], seg[2]]
            elif seg[0] in ("C", "Q"):
                q = seg[1:]
                pts = [M._bez(q, k / 8)[:2] for k in range(9)]
            else:
                continue
            for rep in range(2):
                dense = []
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    L = math.hypot(x1 - x0, y1 - y0) * S
                    n = max(2, int(L / 6))
                    for k in range(n):
                        tt = k / n
                        dense.append((x0 + (x1 - x0) * tt, y0 + (y1 - y0) * tt))
                dense.append(pts[-1])
                dd = "M" + " L".join(f"{x * S + rnd.uniform(-0.9, 0.9) + 8:.1f} {y * S + rnd.uniform(-0.9, 0.9) + 8:.1f}" for x, y in dense)
                paths.append(f'<path d="{dd}" fill="none" stroke="{CHAR}" stroke-width="{1.6 if rep == 0 else 1.0}" stroke-linecap="round" stroke-linejoin="round"/>')
    hatch = []
    for k in range(0, 200, 7):
        hatch.append(f'<line x1="{k - 60}" y1="{175}" x2="{k + 10}" y2="{100}" stroke="{CHAR}" stroke-width="0.9"/>')
    clip = d_of(transform(lay["body"], S, 8, 8))
    return (f'<svg viewBox="0 0 184 184" width="184" height="184" role="img" aria-label="Texture study of the Ballot drawing with hand-drawn line quality, at 184 px">'
            f'<defs><clipPath id="hdclip"><path d="{clip}"/></clipPath></defs><g clip-path="url(#hdclip)" opacity="0.9">{"".join(hatch)}</g>{"".join(paths)}</svg>')


def patterns():
    """Pattern swatches in one ink, built from the node and line. Returns list of (name, svg, rule)."""
    W, H = 240, 120
    out = []
    # node rhythm
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    rnd = random.Random(7)
    for row in range(5):
        y = 12 + row * 24
        for col in range(10):
            x = 12 + col * 24
            p.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{CHAR}"/>')
            if rnd.random() < 0.18 and col < 9:
                p.append(f'<line x1="{x + 4}" y1="{y}" x2="{x + 20}" y2="{y}" stroke="{CHAR}" stroke-width="1"/>')
    p.append("</svg>")
    out.append(("Node rhythm", "".join(p), "From the pillar marks' node and the Signal Grid pitch. Dividers, section openers, social backgrounds."))
    # halftone nodes
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    for row in range(10):
        for col in range(20):
            r = 0.4 + 2.6 * (col / 19) ** 1.6
            p.append(f'<circle cx="{6 + col * 12}" cy="{6 + row * 12}" r="{r:.2f}" fill="{CHAR}"/>')
    p.append("</svg>")
    out.append(("Halftone nodes", "".join(p), "From the pattern collage. Edges of photographs and covers; it fades out before any text."))
    # rule rhythm
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    y = 8
    gaps = [6, 6, 10, 6, 16, 6, 6, 10, 24, 6, 10]
    for gp in gaps:
        p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{CHAR}" stroke-width="1"/>')
        y += gp
    p.append("</svg>")
    out.append(("Rule rhythm", "".join(p), "From study 07. Dividers and the edge of report covers."))
    return out


def pattern_coverage(pats):
    jobs = [{"id": f"pat-{i}", "w": 240, "h": 120, "bg": NEWS, "html": svg} for i, (_, svg, _) in enumerate(pats)]
    jp = SCRATCH / "pat_jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(M.RENDER), str(jp), str(SCRATCH / "pat")], check=True)
    cov = []
    for i in range(len(pats)):
        c = M.load_cov(SCRATCH / "pat" / f"pat-{i}.png", NEWS, CHAR)
        cov.append(sum(map(sum, c)) / (240 * 120))
    return cov


# ------------------------------------------------------------------ page

CSS = """
.toc{display:flex;flex-wrap:wrap;gap:8px 18px;margin:18px 0 0;padding:0;list-style:none}
.toc a{color:var(--fg);font-weight:600}
.lede{font-size:1.125rem;max-width:68ch}
.keyfacts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin:20px 0}
.keyfacts div{background:var(--surface);padding:14px}
.keyfacts b{display:block;font:800 1.5rem/1.1 var(--display);font-variant-numeric:tabular-nums}
.keyfacts span{font-size:.875rem;color:var(--muted)}
code{font:.8125rem/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;background:#E9E6E0;padding:1px 4px}
figure{margin:0}
figcaption{font-size:.8125rem;line-height:1.45;color:var(--muted);margin-top:6px;max-width:60ch}
.pad{padding:12px;display:inline-block;line-height:0}
.mk{display:block}
.s-newsprint{--knock:#DCD9D2}.s-white{--knock:#FFFFFF}.s-charcoal{--knock:#121212}.s-prussian{--knock:#1F2D5A;color:var(--newsprint)}
.s-newsprint .accent,.s-white .accent{--node:#E63946;--seat:currentColor;--tseat:currentColor}
.s-charcoal .accent{--node:#E63946;--seat:none;--tseat:var(--knock)}
.matrix{grid-template-columns:repeat(4,minmax(0,1fr))}
.mx{gap:10px}
.sname{font:700 .8125rem/1.3 var(--body);letter-spacing:.06em;text-transform:uppercase;margin:0}
.mgrid{display:grid;grid-template-columns:62px 16px 24px 48px 96px;gap:10px;align-items:end}
.mgrid .sz{font-size:.8125rem;line-height:1;text-align:left;opacity:.85}
.mgrid .pl,.arow .pl{font-size:.8125rem;font-weight:600;align-self:center}
.arow{display:grid;grid-template-columns:62px 24px 48px 96px;gap:10px;align-items:end}
.mc{display:block;line-height:0}
.zrow{display:flex;flex-wrap:wrap;gap:16px 20px;margin:16px 0 4px}
.zf figcaption{margin-top:4px}
.gw{position:relative;display:inline-block;line-height:0;border:1px solid var(--rule)}
.gw::after{content:"";position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(to right,rgba(31,45,90,.22) 1px,transparent 1px),linear-gradient(to bottom,rgba(31,45,90,.22) 1px,transparent 1px);background-size:var(--g) var(--g)}
.sk-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.sk h3{margin-bottom:10px}
.sk-row{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start;margin-bottom:10px}
.cons{display:block;max-width:100%;height:auto}
.der{display:flex;gap:12px;background:var(--newsprint);padding:12px;border:1px solid var(--rule)}
.der span{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:.8125rem;color:var(--fg)}
.der small{font-size:.8125rem}
.spec td:first-child{font-weight:600;white-space:nowrap}
.hingebox{display:flex;flex-wrap:wrap;gap:28px;align-items:center;margin:18px 0}
.hsch{max-width:100%;height:auto}
.hrow{display:flex;align-items:flex-start;padding:16px;border:1px solid var(--rule);max-width:560px}
.hr-m{display:flex;flex-direction:column;align-items:center;gap:8px;font-weight:700;font-size:.875rem}
.hr-l{flex:1 1 24px;min-width:14px;height:2px;background:var(--charcoal);margin-top:23px}
.alts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:14px}
.alt .pad{margin-bottom:6px}
.dirhead{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:8px}
h4{font:600 1rem/1.3 var(--display);margin:26px 0 10px}
.comps{display:grid;grid-template-columns:360px minmax(0,1fr);gap:24px;align-items:start;margin-top:12px}
.social{width:100%;max-width:360px;aspect-ratio:1/1;container-type:inline-size;border:1px solid var(--rule)}
.so-in{height:100%;padding:7cqw;display:flex;flex-direction:column}
.so-top{display:flex;align-items:center;gap:4cqw}
.so-mark{width:26.7cqw;height:26.7cqw}
.so-kicker{font:700 4.4cqw/1 var(--body);letter-spacing:.1em;text-transform:uppercase;margin:0}
.so-head{font:800 9cqw/1.05 var(--display);letter-spacing:-.02em;margin:7cqw 0 3cqw;text-wrap:balance}
.so-dek{font:400 4.2cqw/1.4 var(--body);margin:0;text-wrap:pretty}
.so-foot{margin:auto 0 0;display:flex;justify-content:space-between;align-items:center;font:800 4.2cqw/1 var(--display)}
.so-series{display:flex;align-items:center;gap:2cqw;font:600 4.2cqw/1 var(--body)}
.so-series svg{width:6.7cqw;height:6.7cqw}
.article{padding:22px 24px;border:1px solid var(--rule);max-width:640px}
.ki{display:flex;align-items:center;gap:8px;margin:0;font-size:.8125rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.ki .kt{font-weight:600;letter-spacing:.04em;color:#45494F}
.ki .ki-il{margin-left:auto;letter-spacing:.04em}
.ki .kt::before{content:"\\00B7";margin-right:8px}
.ah{font:800 2rem/1.08 var(--display);letter-spacing:-.02em;margin:12px 0 10px;text-wrap:balance;max-width:24ch}
.ad{font-size:1.0625rem;margin:0 0 18px;max-width:58ch}
.stories{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.stories li{padding:12px 0;border-bottom:1px solid var(--rule)}
.kh{font:600 1.0625rem/1.3 var(--display);margin:6px 0 0;text-wrap:balance}
table{font-variant-numeric:tabular-nums}
td.n,th.n{text-align:right}
.s-charcoal .cap,.s-prussian .cap{color:var(--newsprint)}
.ck .st{display:block;font-weight:700;font-size:.8125rem;letter-spacing:.04em;text-transform:uppercase}
.ck .dt{display:block;font-size:.8125rem;line-height:1.35;color:var(--muted)}
.ck.no{background:#EBD9D5}
.ck.no .st{color:#8E1B23}
.ck.ok .st{color:#24473F}
.ck.na .st{color:var(--muted)}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--rule);background:var(--surface)}
.scroll:focus-visible{outline:3px solid var(--prussian);outline-offset:2px}
.scroll{max-width:100%}
.scroll table.checks{min-width:1180px}
.scroll table.tt,.scroll table.spec{min-width:520px}
.two>*,.comps>*,.trt>*,.sk-grid>*,.matrix>*{min-width:0}
.tag{font-size:.8125rem;line-height:1.2}
.checks th:first-child,.checks td:first-child{position:sticky;left:0;background:var(--surface);z-index:1;min-width:150px}
.tt td,.tt th{white-space:nowrap}
.trt{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.topicrow{display:grid;grid-template-columns:150px repeat(2,minmax(0,1fr));gap:14px;align-items:center;padding:12px 0;border-bottom:1px solid var(--rule)}
.tset{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end}
.tlab{font-weight:600}
.iso{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.iso svg{flex:0 0 auto}
.isol{margin:0;padding-left:1.4em;font-weight:600;font-size:.9375rem}
.isol li{margin:0 0 8px}
.pats{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.pat .sw{background:var(--newsprint);border:1px solid var(--rule);line-height:0}
.pat svg{display:block;width:100%;height:auto}
.avatars{display:flex;flex-wrap:wrap;gap:20px;align-items:center}
.av{position:relative;width:100px;height:100px}
.av .ring{position:absolute;inset:0;border-radius:50%;border:1.5px solid #5D636D;pointer-events:none}
.series{display:flex;flex-direction:column;gap:10px}
.chip{display:inline-flex;align-items:center;gap:10px;font-weight:600;font-size:.9375rem}
.tag.rec{background:var(--prussian);color:var(--newsprint);border-color:var(--prussian)}
.decision h2{color:var(--newsprint)}
.posts{display:grid;grid-template-columns:repeat(3,minmax(0,360px));gap:24px;margin:14px 0 8px}
.post{width:100%;max-width:360px;aspect-ratio:4/5;container-type:inline-size;border:1px solid var(--rule)}
.po-in{height:100%;padding:6cqw 7cqw;display:flex;flex-direction:column}
.po-wm{height:11cqw;display:flex;align-items:center}
.po-hd{margin:0 0 3cqw}
.po-hinge{display:block;width:72cqw;height:auto;color:var(--charcoal)}
.po-wmsvg{display:block;width:76cqw;height:auto;color:var(--charcoal)}
.po-cover{width:76cqw;height:11cqw;background:#B3B0A8;display:flex;align-items:center;justify-content:center}
.po-cover span{font:600 3.8cqw/1 var(--body);color:var(--charcoal)}
.po-act{display:flex;align-items:center;gap:4cqw;margin-top:4cqw}
.po-mark{width:17cqw;height:17cqw}
.po-k{font:700 4.4cqw/1 var(--body);letter-spacing:.1em;text-transform:uppercase;margin:0}
.po-head{font:800 7.4cqw/1.05 var(--display);letter-spacing:-.02em;margin:4cqw 0 3cqw;text-wrap:balance}
.po-steps{margin:0;padding-left:5.5cqw;font:400 3.9cqw/1.4 var(--body)}
.po-steps li{margin:0 0 1.2cqw}
.po-row{margin-top:auto;display:flex;justify-content:space-between;border-top:1px solid var(--rule);padding-top:3.5cqw}
.po-row span{display:flex;flex-direction:column;align-items:center;gap:1.5cqw}
.po-row svg{width:6.7cqw;height:6.7cqw}
.po-row em{font:600 3.7cqw/1 var(--body);font-style:normal}
.decision ol{padding-left:1.2em;margin:0}
.decision li{margin:0 0 14px;max-width:80ch}
.decision .rec{display:block;margin-top:4px}
.fail-list li{margin-bottom:6px}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
@media (max-width:1100px){.matrix{grid-template-columns:repeat(2,minmax(0,1fr))}.sk-grid{grid-template-columns:1fr}}
@media (max-width:1100px){.posts{grid-template-columns:repeat(2,minmax(0,360px))}}
@media (max-width:760px){.posts{grid-template-columns:minmax(0,360px)}.comps{grid-template-columns:1fr}.two{grid-template-columns:1fr}.topicrow{grid-template-columns:1fr}}
@media (max-width:560px){.matrix{grid-template-columns:1fr}.mgrid{grid-template-columns:58px 16px 24px 48px 96px;gap:8px}.ah{font-size:1.625rem}}
"""


IDENT = ROOT / "work/boards/phase-1/identity"
WM_FILES = {"current": IDENT / "03-wordmark-masters/20261021_Wordmark-Display-Amp-B.svg",
            "condensed": IDENT / "06-condensed/20261021_Wordmark-Condensed-7-5-To-1-Display.svg"}
HINGE_V2 = ROOT / "work/handoffs/phase-1/20261021_Hinge-V2-Ready.md"


def wordmark_inline(kind, label):
    s = WM_FILES[kind].read_text()
    s = re.sub(r"<title>.*?</title>", "", s)
    return s.replace("<svg ", f'<svg class="po-wmsvg" role="img" aria-label="{e(label)}" ', 1)


HINGE_FILE = IDENT / "07-hinge/20261021_Hinge-Compact-Master_V2.svg"


def hinge_divider(covered=False):
    """The V2 compact hinge diagram, used as a divider: ampersand Charcoal, lines Stone (red rule)."""
    h = HINGE_FILE.read_text()
    h = re.sub(r"<title>.*?</title>", "", h)
    if covered:
        cover = '<rect x="-12" y="-14" width="394" height="134" fill="#B3B0A8"/><rect x="922" y="-14" width="511" height="134" fill="#B3B0A8"/>'
        h = re.sub(r"</svg>\s*$", cover + "</svg>", h)
    lab = "Hinge diagram V2 used as a divider" + (", with its words covered" if covered else "")
    return h.replace("<svg ", f'<svg class="po-hinge" role="img" aria-label="{e(lab)}" style="--amp:#121212;--line:#5D636D" ', 1)


def post(kind, covered=False):
    if covered:
        wm = '<div class="po-cover"><span>Wordmark covered</span></div>'
        lab = "Portrait post with the wordmark covered"
    else:
        wm = wordmark_inline(kind, "Oath & Action wordmark with ampersand B" + (", condensed 7.5 to 1" if kind == "condensed" else ""))
        lab = "Portrait Act post with the wordmark" + (" at the condensed width" if kind == "condensed" else " at today's width")
    row = "".join(f'<span>{mark("A", "filled", p, 24)}<em>{PL[p]}</em></span>' for p in F.PILLARS)
    hinge = f'<div class="po-hd">{hinge_divider(covered)}</div>' if HINGE_V2.exists() else ""
    return f'''<div class="post s-newsprint" role="group" aria-label="{e(lab)}"><div class="po-in">
  <div class="po-wm">{wm}</div>
  <div class="po-act">{mark("A", "filled", "act", 96, "accent po-mark", label="Act mark, the call to act")}<p class="po-k">Act</p></div>
  <p class="po-head">How to speak at a public hearing in your state</p>
  {hinge}
  <ol class="po-steps"><li>Find the hearing date.</li><li>Sign up to speak.</li><li>Say what the rule changes for you.</li></ol>
  <div class="po-row">{row}</div>
</div></div>'''


def composite():
    hinge_note = ("The identity board's V2 hinge diagram, with solid arcs, sits between the headline and the steps as a divider, so its ampersand is Charcoal. In the covered post its words are covered too, and its ring, nodes, arcs and ampersand stay visible." if HINGE_V2.exists() else
                  "The hinge diagram is left out: its revised solid drawing (V2) was not ready when this board was built.")
    figs = [(post("current"), "As designed. Wordmark with ampersand B at today's width (identity board items 3 and 5)."),
            (post("condensed"), "As designed. Wordmark at the condensed 7.5 to 1 width (identity board item 6)."),
            (post("current", covered=True), "Wordmark covered, with the hinge diagram's words. Judge whether the post still reads as Oath & Action.")]
    cells = "".join(f'<figure class="comp">{p_}<figcaption>{e(c)}</figcaption></figure>' for p_, c in figs)
    return (f'<section id="composite" aria-labelledby="h-co"><h2 id="h-co">11. The whole recommended set in one post</h2>'
            "<p>The Act post from section 3, rebuilt at 1080 by 1350, the portrait size, with the set the studio recommends: the identity board's wordmark with ampersand B, Direction A's marks and the red rule. The first post sets the wordmark at today's width and the second at the condensed 7.5 to 1 width. The third covers the wordmark, so you can judge whether the system still reads as Oath &amp; Action without it. " + e(hinge_note) + "</p>"
            f'<div class="posts">{cells}</div>'
            '<p class="cap"><span class="tag">Illustrative</span> Headline and steps are example copy. Posts are shown at one third. Red: the wordmark\'s ampersand is signature red and does not count. The one working red is the Act handle, because the Act mark is the call to act. The pillar row and the hinge divider stay Charcoal. The wordmark and hinge files are identity board proposals, inlined unchanged apart from the divider colors the red rule sets.</p></section>')


def build():
    check = json.loads(CHECK.read_text()) if CHECK.exists() else None
    pats = patterns()
    cov = pattern_coverage(pats)
    H = []
    H.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    H.append("<title>Symbol Family Board</title>")
    H.append('<meta name="description" content="Phase 1 proposal for the Oath &amp; Action pillar marks: one skeleton per pillar, two directions, checks and the Gate 1 decisions.">')
    H.append('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    H.append('<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">')
    H.append('<link rel="stylesheet" href="board-base.css">')
    H.append(f"<style>{CSS}</style></head><body>")
    H.append(sprite())
    H.append('<main class="board" id="top">')

    # ---------------- header
    ta = {k: pair(*k) for k in [("A", "filled", "track", "act", 16), ("B", "line", "track", "act", 16), ("V5", "current", "track", "act", 16)]}
    cm_new = MEAS["topics"]["new|contact-an-official|campaign-money|16"]["score"]
    cm_old = MEAS["topics"]["v5|contact-an-official|campaign-money|16"]["score"]
    rows_all = [(d, t, p) for d in F.DIRECTIONS for t in F.TREATMENTS for p in F.PILLARS]
    res_all = {k: checks(*k) for k in rows_all}
    res_topics = {n: topic_checks(n) for n in F.TOPICS}

    def tally(d):
        ps = [s for k, v in res_all.items() if k[0] == d for s, _ in v if s is not None]
        return sum(ps), len(ps) - sum(ps)
    ta_pass, ta_fail = tally("A")
    tb_pass, tb_fail = tally("B")
    H.append('<p class="eyebrow">Oath &amp; Action Brand Guide, Edition 06 · Phase 1 proposal board · October 21, 2026 · Design director</p>')
    H.append("<h1>One skeleton per pillar, drawn two ways</h1>")
    H.append('<p class="lede">This board proposes new pillar marks for Explain, Track, Connect and Act. Each pillar starts as one skeleton on a shared 24-unit grid. Two directions grow from the same four skeletons: A, a geometric solid, and B, a line with one accent. Every mark carries one node, the point where its two parts meet. The studio recommends Direction A.</p>')
    H.append('<p>Everything here is a sketch for a decision at Gate 1. No master changes. Decision DC-02 allows the redraw; the drawings live in <code>work/boards/phase-1/symbols/</code>. Each proposal sits beside the V5 original it would replace. <span class="tag defect">Defect fix</span> marks a change that repairs a measured problem. <span class="tag">Option</span> marks a choice for you.</p>')
    H.append('<div class="keyfacts">')
    H.append(f'<div><b>{num(ta[("A", "filled", "track", "act", 16)]["blurred_corr"])}</b><span>Track against Act at 16 px, blurred correlation, Direction A filled. V5 measures {num(ta[("V5", "current", "track", "act", 16)]["blurred_corr"])}.</span></div>')
    H.append(f'<div><b>{num(cm_new)}</b><span>Contact an official against Campaign money at 16 px, similarity score. V5 measures {num(cm_old)}.</span></div>')
    n_masters = sum(1 for k in rows_all for sz in (16, 24) if mk(*k, sz)["pixel_fit"]["share"] == 1.0)
    H.append(f'<div><b>{n_masters} of {len(rows_all) * 2}</b><span>16 and 24 px pillar masters with every straight edge and curve extreme on a whole pixel.</span></div>')
    H.append(f'<div><b>{ta_pass} pass, {ta_fail} fail</b><span>Craft checks on Direction A drawings. Direction B: {tb_pass} pass, {tb_fail} fail.</span></div>')
    H.append("</div>")
    H.append('<nav aria-label="On this board"><ul class="toc">' + "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in [
        ("skeletons", "1. Skeletons"), ("hinge", "2. The shared node"), ("direction-a", "3. Direction A"), ("direction-b", "4. Direction B"),
        ("track-act", "5. Track and Act at 16 px"), ("topics", "6. Topic grammar"), ("treatments", "7. Sanctioned treatments"),
        ("checks", "8. Craft checks"), ("rubric", "9. Rubric"), ("tested", "10. Checked and not checked"), ("composite", "11. The whole set in one post"), ("decisions", "12. Decisions")]) + "</ul></nav>")

    # ---------------- 1 skeletons
    H.append('<section id="skeletons" aria-labelledby="h-sk"><h2 id="h-sk">1. Four skeletons on one grid</h2>')
    H.append("<p>Each skeleton is the drawing both directions share: the parts, their proportions and where the node sits. The grid is 24 units square, one unit to a pixel at 24 px, with a 2-unit margin. 48 and 96 px scale the 24 px master by 2 and 4. The 16 px masters are separate drawings of the same skeletons, fitted to whole pixels.</p>")
    H.append('<div class="sk-grid">' + "".join(skeleton_card(p) for p in F.PILLARS) + "</div>")
    H.append('<h3 style="margin-top:24px">Family specification</h3><div class="scroll" tabindex="0" role="region" aria-label="Family specification table"><table class="spec"><thead><tr><th scope="col">Item</th><th scope="col">Direction A, geometric solid</th><th scope="col">Direction B, line with one accent</th></tr></thead><tbody>')
    for row in [("Grid", "24 units, 2-unit margin, center lines at 12", "Same"),
                ("Keylines", "Square 2 to 22; circle radius 10 at the center; portrait door 3 to 21", "Same"),
                ("Node at 24 px", "4 px dot in a 1 px clear seat cut into the mass", "6 px dot held off the line by a 1 px gap"),
                ("Node at 16 px", "3 px dot on a pixel center in a 1 px seat (filled); 4 px dot with a 1 px gap (line)", "Same as A at this size"),
                ("Node position", "On the horizontal center line in all four marks", "Same"),
                ("Stroke, line treatment", "2 px at 16 and 24, 4 px at 48, 8 px at 96", "Same"),
                ("Terminals and joins", "Butt or square ends, mitered joins", "Round ends, round joins"),
                ("Corners", "Square", "2 px radius at 24, 1.5 px at 16"),
                ("Tiles", "Rounded square, radius one sixth of the side; mark at two thirds; 10 px micro drawing inside the 16 px tile", "Same plate; the line master sits inside from 24 px"),
                ("Color", "One color. The Act handle turns red only where the Act mark is the call to act (the red rule, section 12), inside a Charcoal ring on light surfaces and never on Prussian", "Same")]:
        H.append(f"<tr><td>{e(row[0])}</td><td>{e(row[1])}</td><td>{e(row[2])}</td></tr>")
    H.append("</tbody></table></div></section>")

    # ---------------- 2 hinge
    H.append('<section id="hinge" aria-labelledby="h-hi"><h2 id="h-hi">2. One node runs through all four</h2>')
    H.append("<p>Dustin described the hinge as a promise, then acting, and as the point where two sides meet. Each pillar mark is drawn as two parts and the point that joins them. In Explain the node sits where a quarter of the square lifts out. In Track it stands on the stage a decision has reached. In Connect it holds the space between two equal halves. In Act it is the handle of the open door.</p>")
    H.append("<p>The node always sits on the horizontal center line. When the four marks run in order, one line can pass through every node, so the row reads as a single path from Explain to Act. That is the same grammar as the hinge diagram and the Signal Grid: a node and a line. A reader who learns one mark learns where to look in the other three.</p>")
    H.append(f'<div class="hingebox"><figure>{hinge_row()}<figcaption><span class="tag">Option</span> The four Direction A marks at 48 px, joined through their nodes. All four stay Charcoal: the row names the pillars and asks nothing of the reader.</figcaption></figure>'
             f'<figure>{hinge_schematic()}<figcaption>Simplified schematic of the proposed hinge diagram (identity item 7), without its arcs, drawn with the V5 ampersand outline in one color. Not a master.</figcaption></figure></div>')
    H.append("<h3>Shared elements considered</h3>")
    H.append(f'<div class="alts">{alternatives()}</div>')
    H.append("<p style=\"margin-top:14px\">The node adds no new shape, because every mark already needs one point of focus. It sits in the same place every time, and it is the only place a pillar mark may ever carry red. It also keeps the ampersand out of the pillar marks, so the wordmark keeps sole use of it.</p></section>")

    # ---------------- 3 and 4 directions
    intro = {
        "A": ("Filled primitives: squares, a circle cut in two, a frame and a leaf. Corners stay square. The node is a dot set into a clear seat in the mass, which keeps it visible in one color. The geometry comes from study 06 and the filled silhouettes in the chat collages. It drops study 06's three colors, its concentric arcs and its quadrant.",
              "Its line treatment traces the same parts with a 2 px stroke and mitered corners."),
        "B": ("A 2 px monoline with round ends, and one solid accent: the node, larger than the line and held off it by a 1 px gap. The approach comes from study 08 and the offset-accent icons in chat collage 5. It drops study 08's tree and its letter-C Explain.",
              "Its filled treatment closes the same contours with 2 px rounded corners."),
    }
    for d in F.DIRECTIONS:
        did = "direction-a" if d == "A" else "direction-b"
        H.append(f'<section id="{did}" aria-labelledby="h-{did}"><div class="dirhead"><h2 id="h-{did}">{3 if d == "A" else 4}. Direction {DL[d]}</h2><span class="tag">Option</span>{"<span class=\"tag rec\">Recommended</span>" if d == "A" else ""}</div>')
        H.append(f"<p>{e(intro[d][0])} {e(intro[d][1])}</p>")
        for t in F.TREATMENTS:
            H.append(f"<h4>{d}. {TL[t]}, in one color, at 16, 24, 48 and 96 px</h4>")
            if t == "tile":
                H.append("<p class=\"cap\">The plate takes the ink color and the mark is cut out of it, so the surface shows through. At 16 px the plate holds a 10 px micro drawing shared by both directions.</p>")
            H.append(matrix(d, t))
            H.append(zooms(d, t))
        H.append(f"<h4>{d}. The red handle, where the Act mark is the call to act</h4>")
        H.append("<p>Under the red rule in section 12, the Act handle is red only when the Act mark is itself the call to act, as on a social tile, and the handle then spends the view's one working red. On Newsprint and White the handle sits inside a 1 px Charcoal ring, because red on Newsprint measures 2.96:1 and an informative mark needs 3:1. On Charcoal the seat is cut out and red meets Charcoal at 4.49:1. Red never sits on Prussian. At 16 px the handle is 2 px, too small to carry color, so Act stays one color there.</p>")
        r24 = min(MEAS["red"][f"{d}|{t}|24|{s}"]["ring_vs_red"] for t in ("filled", "line") for s in ("newsprint", "white", "charcoal"))
        H.append(accent_panel(d))
        H.append(f'<p class="cap">Measured on the rendered pixels: the ring around the red handle reads {num(r24)}:1 or better against the red at 24 px, where the 1 px ring is antialiased, and 4.49:1 at 48 px.</p>')
        H.append(f"<h4>{d}. In use: a social post and an article kicker</h4>")
        H.append(composition(d))
        H.append("</section>")

    # ---------------- 5 Track and Act
    H.append('<section id="track-act" aria-labelledby="h-ta"><h2 id="h-ta">5. Track and Act no longer look alike at 16 px</h2><span class="tag defect">Defect fix</span>')
    H.append("<p>In V5 both marks run from a node at the bottom left to an accent at the top right, and at 16 px they correlate at 0.81. The new Track is a stair, wide and low. The new Act is a door, tall and narrow. The measure is the one the Phase 0 audit used: overlap of the filled silhouettes, and correlation after a 3 by 3 blur, which stands in for a glance. A score is their mean.</p>")
    H.append('<div class="two"><div><div class="scroll" tabindex="0" role="region" aria-label="Track against Act scores"><table class="tt"><thead><tr><th scope="col">Set</th><th scope="col" class="n">Overlap 16</th><th scope="col" class="n">Blur corr. 16</th><th scope="col" class="n">Score 16</th><th scope="col" class="n">Score 24</th></tr></thead><tbody>')
    sets = [("V5", "current", "V5 current")] + [(d, t, f"{d} {t}") for d in F.DIRECTIONS for t in F.TREATMENTS]
    for d, t, lab in sets:
        p16, p24 = pair(d, t, "track", "act", 16), pair(d, t, "track", "act", 24)
        H.append(f'<tr><td>{e(lab)}</td><td class="n">{num(p16["silhouette_iou"])}</td><td class="n">{num(p16["blurred_corr"])}</td><td class="n">{num(p16["score"])}</td><td class="n">{num(p24["score"])}</td></tr>')
    H.append("</tbody></table></div></div><div>")
    H.append('<div class="zrow">')
    for f, alt in (("n-v5-track-16.png", "V5 Track 16 px"), ("n-v5-act-16.png", "V5 Act 16 px"), ("n-A-filled-track-16.png", "A Track 16 px"), ("n-A-filled-act-16.png", "A Act 16 px"),
                   ("n-B-line-track-16.png", "B Track 16 px"), ("n-B-line-act-16.png", "B Act 16 px")):
        H.append(f'<figure class="zf">{zoom(f, 16, 6, alt)}<figcaption>{e(alt)}</figcaption></figure>')
    H.append("</div></div></div>")
    H.append("<h3 style=\"margin-top:20px\">Every pillar pair, and the Phase 0 watch points</h3><p>Pass is a score under 0.60, a studio threshold set between V5's worst pillar pair (0.65) and its unrelated pairs. The watch items are drawn or set at the same size: Inter Tight capitals C, D and L, the Inter copyright sign fitted to the live area, a play triangle, a three-light status row, and V5's chain link, outbound arrows and Signal Grid lockmark.</p>")
    H.append('<div class="scroll" tabindex="0" role="region" aria-label="Pair and watch point scores"><table class="tt"><thead><tr><th scope="col">Set</th>' + "".join(f'<th scope="col" class="n">{PL[a]} / {PL[b]}</th>' for a, b in combinations(F.PILLARS, 2)) + "</tr></thead><tbody>")
    for d, t, lab in sets:
        H.append(f"<tr><td>{e(lab)}</td>" + "".join(f'<td class="n">{num(max(pair(d, t, a, b, 16)["score"], pair(d, t, a, b, 24)["score"]))}</td>' for a, b in combinations(F.PILLARS, 2)) + "</tr>")
    H.append("</tbody></table></div><p class=\"cap\">Each cell is the higher of the 16 and 24 px scores. Tiles are measured on the mark inside the plate.</p>")
    H.append('<div class="scroll" tabindex="0" role="region" aria-label="Watch point scores" style="margin-top:14px"><table class="tt"><thead><tr><th scope="col">Pillar</th><th scope="col">Watch item</th><th scope="col" class="n">V5</th><th scope="col" class="n">A filled</th><th scope="col" class="n">A line</th><th scope="col" class="n">B filled</th><th scope="col" class="n">B line</th></tr></thead><tbody>')
    for p, names in WATCH.items():
        for nm in names:
            def w(dd, tt):
                return max(MEAS["watch"][f"{dd}|{tt}|{p}|{nm}|{sz}"]["score"] for sz in (16, 24))
            H.append(f'<tr><td>{PL[p]}</td><td>{e(nm)}</td><td class="n">{num(w("V5", "current"))}</td><td class="n">{num(w("A", "filled"))}</td><td class="n">{num(w("A", "line"))}</td><td class="n">{num(w("B", "filled"))}</td><td class="n">{num(w("B", "line"))}</td></tr>')
    cc = max(MEAS["watch"][f"A|filled|connect|copyright sign|{sz}"]["score"] for sz in (16, 24))
    H.append(f"</tbody></table></div><p class=\"cap\">V5 scores 1.00 against its own chain link and arrow, the metaphors these sketches replace. Any round mark scores high on the silhouette half of the test against the copyright sign. An 8-unit divide between Connect's halves holds Direction A at {num(cc)}; a 2-unit divide scored 0.82 in an earlier sketch. Connect stays on the watch list for a reader test.</p></section>")

    # ---------------- 6 topics
    H.append('<section id="topics" aria-labelledby="h-tp"><h2 id="h-tp">6. Topic grammar proof in Direction A</h2><span class="tag">Option</span>')
    H.append("<p>Four V5 topics redrawn with Direction A's rules: filled primitives, square corners and one node with a real job. The node is the filled oval on the ballot, the seal at the foot of the bill, the seal on the envelope and the face of the coin. In V5, Contact an official and Campaign money shared one silhouette at 16 px, a landscape box with a mark in the middle. Campaign money is now a stack of coins with one coin standing, so the two subjects no longer share an outline.</p>")
    H.append('<p><span class="tag defect">Defect fix</span> applies to one change only: splitting Contact an official from Campaign money, which shared one silhouette in V5. The grammar itself, for all four topics and the sixteen still to draw, is an option for you.</p>')
    for n in F.TOPICS:
        old = "".join(f'<span class="mc">{v5(f"ic-{n}-{s}", s, label=f"V5 {F.TOPIC_LABELS[n]} {s} px")}</span>' for s in (16, 24, 48))
        new = "".join(f'<span class="mc">{use(f"tp-{n}-{16 if s == 16 else 24}", s, 16 if s == 16 else 24, label=f"Proposed {F.TOPIC_LABELS[n]} {s} px")}</span>' for s in (16, 24, 48))
        zo = zoom(f"n-v5topic-{n}-16.png", 16, 6, f"V5 {F.TOPIC_LABELS[n]} 16 px at 6x") + zoom(f"n-topic-{n}-16.png", 16, 6, f"Proposed {F.TOPIC_LABELS[n]} 16 px at 6x")
        H.append(f'<div class="topicrow"><span class="tlab">{F.TOPIC_LABELS[n]}</span><div class="s-newsprint pad"><div class="tset">{old}</div><p class="cap" style="margin:6px 0 0"><span class="tag">Original</span> V5 at 16, 24, 48</p></div>'
                 f'<div class="s-newsprint pad"><div class="tset">{new}{zo}</div><p class="cap" style="margin:6px 0 0"><span class="tag">Option</span> Proposed at 16, 24, 48; V5 and proposed 16 px at 6x</p></div></div>')
    H.append('<h3 style="margin-top:20px">Similarity against V5</h3><div class="scroll" tabindex="0" role="region" aria-label="Topic similarity table"><table class="tt"><thead><tr><th scope="col">Pair</th><th scope="col" class="n">V5, 16 px</th><th scope="col" class="n">Proposed, 16 px</th><th scope="col" class="n">V5, 24 px</th><th scope="col" class="n">Proposed, 24 px</th></tr></thead><tbody>')
    for a, b in combinations(F.TOPICS, 2):
        vals = [MEAS["topics"][f"{w}|{a}|{b}|{sz}"]["score"] for sz in (16, 24) for w in ("v5", "new")]
        H.append(f'<tr><td>{F.TOPIC_LABELS[a]} / {F.TOPIC_LABELS[b]}</td>' + "".join(f'<td class="n">{num(v)}</td>' for v in (vals[0], vals[1], vals[2], vals[3])) + "</tr>")
    H.append("</tbody></table></div>")
    bb16 = MEAS["topics"]["new|ballot|bill|16"]["score"]
    H.append(f"<p class=\"cap\">Contact an official against Campaign money falls from {num(cm_old)} to {num(cm_new)} at 16 px. Ballot against Bill falls from 0.71 to {num(bb16)}, still the closest pair, because both are sheets of paper. Three pairs score higher than in V5 and all stay under 0.60, because the four now share one grammar. The full set of twenty gets the same test in Phase 2.</p></section>")

    # ---------------- 7 treatments
    H.append('<section id="treatments" aria-labelledby="h-tr"><h2 id="h-tr">7. Where each sanctioned treatment belongs</h2>')
    H.append("<p>One master family, Direction A, and a short list of treatments with fixed jobs. Each treatment may appear only in the places named here.</p>")
    H.append('<div class="scroll" tabindex="0" role="region" aria-label="Sanctioned treatments map"><table><thead><tr><th scope="col">Treatment</th><th scope="col">Source</th><th scope="col">Job</th><th scope="col">Where it appears</th><th scope="col">Minimum</th><th scope="col">Never</th></tr></thead><tbody>')
    for row in [
        ("Filled mark", "Study 06; chat collages 1 to 3", "Pillar marks and topic symbols", "Navigation, kickers, chapter openers, report covers, the atlas", "16 px", "In more than one color"),
        ("Line companion", "Study 08; chat collage 5", "The same drawings at reading size", "Inline with text, interface buttons, large line art on covers", "24 px", "Below 24 px, or mixed with filled marks in one row"),
        ("Tile", "Study 04", "Avatars and series markers", "Social avatars, app tiles, series chips, newsletter sections", "16 px (micro drawing)", "An all-red tile; red on Prussian"),
        ("Isometric layers", "Study 03", "Exploded layer diagrams", "The three atlas layers; layer explainers in reports", "320 px wide", "Icons; tilted labels"),
        ("Hand-drawn spot illustration", "Study 05", "Human texture in editorial pieces", "Article openers, report spreads, event signs", "96 px", "Icons; red and blue pairs; a Capitol dome or scales"),
        ("Patterns", "Study 07; chat collage 4", "Rhythm and texture", "Dividers, section openers, social backgrounds, watermark fields", "Coverage limits below", "More than 12 percent ink behind text"),
        ("Orbit and ring motion", "Study 01", "Movement in Track, Connect and loop graphics", "Animated diagrams with a still frame", "Motion only", "A separate icon style"),
        ("Flat Geo", "Study 02", "Comparison only", "This board", "Not shipped", "Any product use")]:
        H.append("<tr>" + "".join(f"<td>{e(c)}</td>" for c in row) + "</tr>")
    H.append("</tbody></table></div>")
    H.append('<div class="trt" style="margin-top:22px">')
    H.append(f'<figure class="panel">{iso_diagram()}<figcaption><span class="tag">Sketch</span> Isometric is sanctioned for exploded layer diagrams only. The slabs tilt; the labels stay flat and horizontal. Layer names from Master Brief V2 section 11, in the order of the Concept 03 screenshot.</figcaption></figure>')
    H.append(f'<figure class="panel"><div class="s-newsprint pad">{hand_drawn()}</div><figcaption><span class="tag">Sketch</span> Texture study generated by script from the Ballot drawing, to show line quality at spot size. Final spot illustrations are drawn by a person at 96 px and larger, in Charcoal on Newsprint. Study 05 is likely generated, so it cannot ship.</figcaption></figure>')
    av = "".join(f'<div class="av s-charcoal" style="border-radius:50%;overflow:hidden">{mark("A", "tile", p, 96, label=f"{PL[p]} avatar")}<span class="ring"></span></div>' for p in ("explain", "track"))
    chips = "".join(f'<span class="chip">{mark("A", "tile", p, 24)}<span>{PL[p]} · {s}</span></span>' for p, s in (("track", "Bill watch"), ("explain", "How it works"), ("connect", "Common ground"), ("act", "How to take part")))
    H.append(f'<figure class="panel"><div class="avatars"><div class="s-newsprint pad" style="display:flex;gap:16px">{av}</div><div class="series">{chips}</div></div><figcaption><span class="tag">Sketch</span> Tiles for avatars and series markers. Avatars are 400 by 400 shown at one quarter; the gray ring is the circle-safe area, and the mark sits inside it. Series chips use the 24 px tile. Names are examples.</figcaption></figure>')
    H.append("</div>")
    H.append("<h3 style=\"margin-top:22px\">Patterns, with measured ink coverage</h3><div class=\"pats\">")
    for (nm, svg, rule), c in zip(pats, cov):
        H.append(f'<figure class="pat"><div class="sw">{svg}</div><figcaption><strong>{e(nm)}</strong>, {num(c * 100, 1)} percent ink. {e(rule)}</figcaption></figure>')
    H.append("</div><p class=\"cap\">Rule proposed for Gate 1: a pattern behind text stays at or under 12 percent ink in one palette color, and never runs under body copy. Standalone dividers may reach 25 percent. Coverage is measured on Chromium renders of the swatches above.</p></section>")

    # ---------------- 8 checks
    H.append('<section id="checks" aria-labelledby="h-ck"><h2 id="h-ck">8. Craft checks on every drawing</h2>')
    H.append("<p>The nine checks from the design director's role file, run on every pillar drawing and the four topics. Where a check needs a number, the test and its threshold are set out below the table. All rasters come from Chromium at device scale 1.</p>")
    H.append('<div class="scroll" tabindex="0" role="region" aria-label="Craft check results"><table class="checks"><thead><tr><th scope="col">Drawing</th>' + "".join(f'<th scope="col">{i + 1}. {n}</th>' for i, n in enumerate(CHECK_NAMES)) + "</tr></thead><tbody>")
    for (d, t, p), res in res_all.items():
        H.append(f"<tr><th scope=\"row\">{d} · {TL[t]} · {PL[p]}</th>" + "".join(status_cell(s, dt) for s, dt in res) + "</tr>")
    for n, res in res_topics.items():
        H.append(f"<tr><th scope=\"row\">Topic · {F.TOPIC_LABELS[n]}</th>" + "".join(status_cell(s, dt) for s, dt in res) + "</tr>")
    H.append("</tbody></table></div>")
    tests = [
        ("Silhouette", "At 16 px, at least 60 percent of inked pixels are solid (crisp share) and ink covers at least 25 percent of the field. V5's pillar masters score 0.30 to 0.57 crisp share."),
        ("Pixel fit", "In the 16 and 24 px masters, every horizontal and vertical straight edge, and every horizontal or vertical tangent of the node, seats, discs and arcs, lies within 0.06 px of a whole pixel. Round caps, round joins and corner fillets are exempt."),
        ("Consistency", "The node and its 1 px ring match the family specification at 16 and 24 px. A declared exception counts as a fail and is named in the cell."),
        ("Optical balance", "At 96 px, ink sits within 20 percent of the median of its set, and the center of mass sits within 12 percent of the field center on both axes."),
        ("Similarity", "Every score against another pillar in the same set, and against each Phase 0 watch item, is under 0.60. Tiles are compared inside the plate and inherit the watch-item results of the drawing they hold. Topic against pillar must be under 0.70, because the two never share a slot."),
        ("Monochrome", "Rendered in Charcoal on Newsprint and in Newsprint on Charcoal, the node is its own connected shape at 16 and 24 px."),
        ("Red discipline", "Red appears only on the Act handle, and only where the Act mark is the call to act, as the red rule in section 12 sets out. Checked in the drawings and in every composition on this board."),
        ("Contrast", "Ink against every surface (WCAG ratio), and the ring around the red handle against the red, measured on rendered pixels."),
        ("Type", "Applies to compositions. Results for the board's headings and the composition headlines are listed below.")]
    H.append("<h3 style=\"margin-top:18px\">How each check was run</h3><ul>" + "".join(f"<li><strong>{e(a)}.</strong> {e(b)}</li>" for a, b in tests) + "</ul>")
    fails = []
    for (d, t, p), res in res_all.items():
        for i, (s, dt) in enumerate(res):
            if s is False:
                fails.append(f"{d} {t} {PL[p]}: {CHECK_NAMES[i].lower()}. {dt}.")
    for n, res in res_topics.items():
        for i, (s, dt) in enumerate(res):
            if s is False:
                fails.append(f"Topic {F.TOPIC_LABELS[n]}: {CHECK_NAMES[i].lower()}. {dt}.")
    H.append(f"<h3>Failures, {len(fails)} in all</h3><ul class=\"fail-list\">" + "".join(f"<li>{e(f)}</li>" for f in fails) + "</ul>")
    sil_fail = [f"{d} {PL[p]}" for d in F.DIRECTIONS for p in F.PILLARS if res_all[(d, "line", p)][0][0] is False]
    tcy = [mk(d, t, "track", 96)["centroid"][1] for d, t in (("A", "filled"), ("A", "line"), ("B", "filled"))]
    H.append(f"<p><strong>What the failures say.</strong> At 16 px, the line masters of {', '.join(sil_fail)} fail the silhouette test, so the line companion should start at 24 px. Track's solid stair carries its weight low, {num(min(tcy) * 100, 0)} to {num(max(tcy) * 100, 0)} percent of the field below center in the filled and A line drawings, and fails optical balance; Phase 2 should test a raised stair. The Act handle at 16 px is a declared exception in both directions, because a 6 px leaf has no room for a 3 px dot and a ring. Direction B's Track line carries {num(mk('B', 'line', 'track', 96)['density'] * 100, 0)} percent ink at 96 px, far below its set.</p>")
    if check:
        H.append("<h3>Type and layout check</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in check.get("summary", [])) + "</ul>")
    H.append("</section>")

    # ---------------- 9 rubric
    H.append('<section id="rubric" aria-labelledby="h-ru"><h2 id="h-ru">9. Rubric scores</h2><p>Scored against Master Brief V2 section 6. The ship threshold is 4 on every criterion. These are Phase 1 sketches, so usefulness is scored on what a builder could take from the board today.</p>')
    rub = [
        ("Craft", 4, "Every filled master sits on whole pixels; nodes survive one color at 16 px. Track sits low and the 16 px handle is an exception.", 3, "Two of four line masters fail the 16 px silhouette test; the B Track line carries little ink; the large B handle crowds the Act leaf."),
        ("Clarity", 4, "Each skeleton names its idea in a sentence; one rule places the node in every mark.", 3, "The same skeletons. In the studio's judgment, Connect's two arcs and dot read close to a target or broadcast symbol."),
        ("Brand fidelity", 4, "One color, one red job, a node grammar shared with the hinge and the Signal Grid. In the studio's judgment it reads as Oath & Action without the wordmark.", 3, "Brand rules hold. In the studio's judgment a monoline set with round ends sits close to stock icon sets, the criticism Phase 0 made of V5's topics."),
        ("Usefulness", 3, "Specification, masters at 16 and 24, measured checks and a topic proof. Missing: exports, the other sixteen topics, tokens.", 3, "Same gaps."),
        ("Evidence honesty", 5, "Every number comes from a script run on rendered pixels; every example headline is labeled.", 5, "Same."),
        ("Accessibility", 4, "Ink on all surfaces 9.42:1 or better; red is never the only signal; marks carry text labels in use.", 3, "Contrast holds, but 2 px lines at 16 px lose shape, so the marks need their labels even more."),
    ]
    H.append('<div class="scroll" tabindex="0" role="region" aria-label="Rubric scores"><table><thead><tr><th scope="col">Criterion</th><th scope="col" class="n">A</th><th scope="col">Reason</th><th scope="col" class="n">B</th><th scope="col">Reason</th></tr></thead><tbody>')
    for c, a, ra, b, rb in rub:
        H.append(f'<tr><td>{c}</td><td class="n">{a}</td><td>{e(ra)}</td><td class="n">{b}</td><td>{e(rb)}</td></tr>')
    H.append("</tbody></table></div><p class=\"cap\">Neither direction reaches 4 on usefulness yet. That is expected at a proposal gate; Phase 2 closes it with exports, the full topic set and tokens.</p></section>")

    # ---------------- 10 tested
    H.append('<section id="tested" aria-labelledby="h-te"><h2 id="h-te">10. Checked and not checked</h2><div class="two"><div><h3>Checked</h3><ul>'
             "<li>Every drawing rendered by Chromium at device scale 1, at 16, 24, 48 and 96 px, in one color on all four surfaces.</li>"
             "<li>The nine craft checks on all 24 pillar drawings and four topics, with the tests listed in section 8.</li>"
             "<li>Similarity among the four pillars in every set, against V5, against the Phase 0 watch items, and among the four topics against V5.</li>"
             "<li>Red ring contrast on rendered pixels at 24 and 48 px, on Newsprint, White and Charcoal.</li>"
             "<li>Pattern ink coverage on rendered swatches.</li>"
             "<li>This board at 1440 and 390 px wide in Chromium: horizontal overflow, heading widows and tabular figures.</li>"
             "</ul></div><div><h3>Not checked</h3><ul>"
             "<li>Readers. Similarity comes from a model of a glance, not from people.</li>"
             "<li>Rendering outside Chromium on Linux, high-density screens, Windows and macOS font smoothing.</li>"
             "<li>Print. No inch or millimeter minimums yet.</li>"
             "<li>The other sixteen topics, the atlas symbols, status marks and utility icons.</li>"
             "<li>Screen reader output for this board beyond the labels written into it.</li>"
             "<li>Whether the example headlines describe real procedures in every state. They are labeled as illustrative.</li>"
             "</ul></div></div></section>")

    # ---------------- 11 decisions
    H.append(composite())
    H.append('<section id="decisions" aria-labelledby="h-de" class="decision"><h2 id="h-de">12. Decisions for Gate 1</h2><ol>')
    LINE16 = ", ".join(f"{d} {PL[p]}" for d in F.DIRECTIONS for p in F.PILLARS if res_all[(d, "line", p)][0][0] is False)
    LINE16 = LINE16[0].upper() + LINE16[1:] if LINE16 else "No line masters"
    decisions = [
        ("Symbol direction", "A, geometric solid; or B, line with one accent.", "A. It leads with the filled master, which passes the 16 px silhouette test for all four pillars. B leads with the line, which fails it for Track and Connect."),
        ("The four skeletons", "Approve the exploded square, the stair, the split circle and the open door, or ask for changes to any one.", "Approve, with one Phase 2 change: raise Track's stair so its mass sits nearer the center."),
        ("The shared element", "One node on the center line in every mark; the ampersand's crossing; a ring; a baseline bar.", "The node. It ties the marks to the hinge and the Signal Grid without adding a shape, and leaves the ampersand to the wordmark."),
        ("Red in the pillar marks", "Adopt the red rule, which also settles whether the Act handle counts; or red in all four marks, as in study 06.", "Adopt the red rule. " + RED_RULE),
        ("Line treatment at 16 px", "Allow line marks at 16 px; or start the line companion at 24 px.", f"Start at 24 px. {LINE16} fail the 16 px silhouette test, and filled masters pass it in both directions."),
        ("Topic grammar", "Redraw all twenty topics in Direction A's grammar, one node per subject; or keep V5's topic set.", "Redraw in Phase 2, starting with the four pairs Phase 0 named and Ballot against Bill."),
        ("Sanctioned treatments", "Approve the map in section 7, including hand-drawn at 96 px and up, isometric for layer diagrams only, tiles for avatars and series, and the 12 percent pattern limit behind text.", "Approve. Each treatment gets one job and a minimum size a builder can check."),
    ]
    for h, opts, rec in decisions:
        H.append(f"<li><strong>{e(h)}.</strong> Options: {e(opts)}<span class=\"rec\">Studio recommendation: {e(rec)}</span></li>")
    H.append("</ol><p><strong>Recommended direction: A, geometric solid.</strong> It holds at 16 px, puts red in one place and gives the topic and atlas symbols a grammar that survives small sizes.</p></section>")

    H.append('<section aria-labelledby="h-fi"><h2 id="h-fi">Files</h2><ul>'
             "<li>Sketch sprites: <code>work/boards/phase-1/symbols/20261021_Pillar-Sketches-Direction-A.svg</code>, <code>…-Direction-B.svg</code>, <code>20261021_Topic-Sketches-Direction-A.svg</code></li>"
             "<li>Measurements: <code>work/boards/phase-1/symbols/20261021_Symbol-Family-Measurements.json</code>; renders in <code>work/boards/phase-1/symbols/px/</code></li>"
             "<li>Scripts: <code>work/build/scripts/phase-1/symbols_geom.py</code>, <code>symbols_family.py</code>, <code>symbols_measure.py</code>, <code>symbols_board_build.py</code>, <code>symbols_board_check.js</code>, <code>symbols_render_cells.js</code></li>"
             "<li>Notes: <code>work/handoffs/phase-1/20261021_Symbol-Family-Notes.md</code></li></ul></section>")
    H.append("</main></body></html>")
    out = "".join(H)
    # red discipline in markup: red appears only through .accent on Act marks
    for m_ in re.finditer(r'class="mk ([^"]*accent[^"]*)"[^>]*><use href="#([^"]+)"', out):
        assert "-act-" in m_.group(2), m_.group(2)
    for m_ in re.finditer(r'<svg x="[^"]+" y="0" width="\d+" height="\d+" viewBox="0 0 24 24" class="accent"><use href="#([^"]+)"', out):
        assert "-act-" in m_.group(1)
    BOARD.write_text(out)
    print("board", BOARD, len(out) // 1024, "KB; fails", len(fails))


if __name__ == "__main__":
    build()
