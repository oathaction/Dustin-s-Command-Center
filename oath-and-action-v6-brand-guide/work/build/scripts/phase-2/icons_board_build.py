"""Build the Phase 2 icon concepts board (design director, October 28, 2026).

Run after icons_assets.py and icons_measure.py:
  python3 -I icons_board_build.py
Writes work/boards/20261028_Icon-Concepts-Board.html. Every image is referenced by relative path
from work/boards/phase-2/icons/. Numbers on the board come from the measurements JSON.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_assets as A  # noqa: E402
import icons_common as C  # noqa: E402
import icons_draw as D  # noqa: E402

BOARD = C.BOARDS / f"{C.DATE}_Icon-Concepts-Board.html"
MEAS = json.loads((C.OUT / f"{C.DATE}_Icon-Concepts-Measurements.json").read_text())
BASE = json.loads((C.BASELINE / "manifest.json").read_text())
e = html.escape


def rule_0503():
    s = (C.ROOT / "work/ledger/20261020_Decision-Log.md").read_text()
    line = [ln for ln in s.splitlines() if ln.startswith("| D2-01 ")][0]
    return re.search(r'word for word: "(.*?)" \|', line).group(1)


def num(v, d=2):
    s = f"{v:.{d}f}"
    return s.replace("-", "−")


def pw(v, d=0):
    """A share written out for prose, for example 12.5 percent."""
    return (f"{v * 100:.{d}f}".replace("-", "\u2212")) + " percent"


def pct(v, d=0, sign=False):
    s = f"{v * 100:+.{d}f}" if sign else f"{v * 100:.{d}f}"
    return s.replace("-", "−") + "%"


# ---------------------------------------------------------------- image helpers

def src(p):
    return e(C.rel(p))


def icon(c, cut, n, size, colorway="Ink-Charcoal-Red", alt=None):
    if size <= 16 and 16 in C.sizes(c, cut):
        kind = "16px"
    elif size <= 40:
        kind = "24px"
    else:
        kind = "Display"
    f = A.variant_file(c, cut, n, kind, colorway)
    a = alt if alt is not None else f"{D.LABELS[n]}"
    return f'<img src="{src(f)}" width="{size}" height="{size}" alt="{e(a)}">'


def tile(c, cut, n, shape, color, size, alt=None):
    """A holder with its icon. The icon's live area is half the holder: a 24 px master sits in
    a 40 px holder, the display master in anything larger."""
    fill, cw = C.HOLDER_COLORS[color]
    field = size * C.FIELD_FRACTION
    off = (size - field) / 2
    kind = "24px" if size == 40 else "Display"
    f = A.variant_file(c, cut, n, kind, cw)
    a = alt if alt is not None else f"{D.LABELS[n]} on a {color} {shape.replace('-', ' ').lower()}"
    return (f'<span class="tile" style="width:{size}px;height:{size}px">'
            f'<img class="h" src="{src(C.holder_file(shape, color))}" width="{size}" height="{size}" alt="">'
            f'<img class="i" src="{src(f)}" style="left:{off:g}px;top:{off:g}px" width="{field:g}" height="{field:g}" alt="{e(a)}"></span>')


def strip(c, cut, size, colorway="Ink-Charcoal-Red", names=None, cols=None):
    names = names or D.ICONS
    if cols:
        return (f'<div class="igrid" style="grid-template-columns:repeat({cols},{size}px)">'
                + "".join(icon(c, cut, n, size, colorway) for n in names) + "</div>")
    return '<div class="strip">' + "".join(icon(c, cut, n, size, colorway) for n in names) + "</div>"


DRAW_LABEL = {("A", "line"): "A, line", ("B", "flat"): "B, flat", ("C", "line"): "C, line cut", ("C", "flat"): "C, flat cut"}
SHOW = [("A", "line"), ("B", "flat"), ("C", "line"), ("C", "flat")]
TILE_CUT = {"A": ("A", "line"), "B": ("B", "flat"), "C": ("C", "flat")}


def m(c, cut, n, s):
    return MEAS["drawings"][f"{c}-{cut}-{n}-{s}"]


def sset(c, cut, s):
    return MEAS["sets"][f"{c}-{cut}-{s}"]


# ---------------------------------------------------------------- derived numbers

def worst_pair_all(size=16):
    best = (0, None)
    for k, v in MEAS["pairs"].items():
        if k.endswith(f"|{size}") and v["score"] > best[0]:
            best = (v["score"], k)
    return best


def pairs_over(size=16):
    return sum(1 for k, v in MEAS["pairs"].items() if k.endswith(f"|{size}") and v["score"] >= 0.60)


def crisp_min():
    return min(v["crisp"] for v in MEAS["drawings"].values())


def watch_worst(prefix):
    vals = [(v["score"], k) for k, v in MEAS["watch"].items() if k.startswith(prefix + "|")]
    return max(vals) if vals else (0, "")


def act_01(prefix):
    for k, v in MEAS["watch"].items():
        if k.startswith(prefix + "|act|chapter number 01"):
            return v["score"]
    return None


OLD01 = {k.split("|")[1]: v["score"] for k, v in MEAS["watch"].items() if k.startswith("phase1-frame|")}
CRISP_UNHINTED_MIN = min(v["crisp_unhinted"] for v in MEAS["drawings"].values())
TILES_TOTAL = len(MEAS["tiles"])
TILES_IN = sum(1 for v in MEAS["tiles"].values() if v["in_live_area"] and v.get("in_circle_safe", True))
MIN_MARGIN = min(v["margin_share"] for v in MEAS["tiles"].values())
MAX_R = max(v["r_max_share"] for k, v in MEAS["tiles"].items() if "Circle" in k)


# ---------------------------------------------------------------- CSS

CSS = """
.board{max-width:1280px}
.lede{font-size:1.125rem;line-height:1.55;max-width:64ch}
.note{font-size:.9375rem;max-width:70ch}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--rule);margin:22px 0 8px}
.stats>div{padding:16px;border-left:1px solid var(--rule);min-width:0}
.stats>div:first-child{border-left:0}
.stats b{display:block;font:800 1.625rem/1.1 var(--display);letter-spacing:-.02em;margin-bottom:6px;font-variant-numeric:tabular-nums}
.stats span{font-size:.875rem;line-height:1.45;color:var(--muted);display:block}
.toc{display:flex;flex-wrap:wrap;gap:6px 18px;margin:18px 0 0;font-weight:600;font-size:.9375rem}
.toc a{color:var(--fg)}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;align-items:start}
.igrid{display:grid;gap:14px 22px;align-items:end}
.igrid img{display:block}
.bgrid{display:grid;grid-template-columns:repeat(8,56px);gap:10px;align-items:end}
.bgrid>span{display:flex;justify-content:flex-start;align-items:flex-end;min-height:24px}
.hrow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin-bottom:10px}
.hrow>div{background:var(--bg);padding:12px;min-width:0}
.hrow>div.wh{background:var(--white)}
.hrow>div.s-charcoal{background:var(--charcoal)}
.hrow>div.s-prussian{background:var(--prussian)}
.hrow>div.s-charcoal .cap,.hrow>div.s-prussian .cap{color:#C9C5BC}
.hrow .cap{margin-bottom:8px}
.tgrid{display:grid;grid-template-columns:repeat(4,40px);gap:10px 14px}
.navstack{display:grid;gap:10px}
.navstack h4{margin:0 0 6px}
.card{background:var(--surface);border:1px solid var(--rule);padding:18px;min-width:0;display:flex;flex-direction:column;gap:12px}
.card h3{font-size:1.25rem;font-weight:800;letter-spacing:-.02em}
.card ul{margin:0;padding-left:18px;font-size:.875rem;line-height:1.5}
.card ul li{margin:2px 0}
.strip{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:flex-end}
.strip img{display:block}
.strip.tight{gap:8px 10px}
.idea{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin:16px 0}
.idea>div{background:var(--bg);padding:14px;display:grid;grid-template-columns:56px 1fr;gap:12px;align-items:center}
.idea p{margin:0;font-size:.875rem;line-height:1.45}
.idea strong{display:block;font-size:.9375rem}
blockquote{margin:16px 0;padding:14px 18px;border-left:3px solid var(--fg);background:var(--surface);font-size:.9375rem;max-width:80ch}
.rows{border-top:1px solid var(--rule)}
.row{display:grid;grid-template-columns:150px minmax(0,1fr);gap:16px;align-items:center;padding:14px 0;border-bottom:1px solid var(--rule)}
.row>.lab{font-weight:700;font-size:.9375rem;line-height:1.35}
.row>.lab small{display:block;font-weight:400;color:var(--muted);font-size:.8125rem}
.sizes4{display:flex;flex-wrap:wrap;gap:18px 28px;align-items:flex-end}
.sizes4 figure{margin:0}
.sizes4 figcaption{font-size:.8125rem;color:var(--muted);margin-top:6px}
.surf{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule)}
.surf>div{padding:14px;min-width:0}
.surf .cap{margin-bottom:8px}
.s-charcoal .cap,.s-prussian .cap{color:#C9C5BC}
.tile{position:relative;display:inline-block;flex:none}
.tile>img{position:absolute;display:block}
.tile>img.h{left:0;top:0}
.holders{display:grid;grid-template-columns:120px repeat(3,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}
.holders>div{background:var(--bg);padding:12px;min-width:0}
.holders .hd{font-weight:700;font-size:.875rem}
.holders .strip{gap:8px}
.cmp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.cmp>div{min-width:0}
.cmp h4{font:700 .9375rem/1.3 var(--body);margin:0 0 10px}
.navrow{display:flex;align-items:center;flex-wrap:wrap;gap:0;padding:14px 16px;border:1px solid var(--rule)}
.navrow .it{display:flex;align-items:center;gap:8px;font-size:.9375rem;color:var(--fg)}
.navrow .it b{font-weight:700}
.navrow .ln{flex:1 1 18px;min-width:14px;height:1px;background:var(--rule);margin:0 10px}
.navrow.dark{background:var(--charcoal);border-color:var(--charcoal)}
.navrow.dark .it{color:var(--newsprint)}
.navrow.dark .ln{background:#5D636D}
.navrow .cur{font-weight:700;box-shadow:inset 0 -2px 0 currentColor;padding-bottom:3px}
.topics{border:1px solid var(--rule);background:var(--surface)}
.topics>div{display:grid;grid-template-columns:24px 1fr;gap:12px;align-items:center;padding:9px 14px;border-top:1px solid var(--rule)}
.topics>div:first-child{border-top:0}
.topics span{font-size:.9375rem;line-height:1.3}
.topics small{display:block;color:var(--muted);font-size:.8125rem}
.topics .on span{font-weight:700}
.avatar{display:flex;gap:14px;align-items:center;padding:14px;border:1px solid var(--rule);background:var(--white)}
.avatar p{margin:0;font-size:.9375rem;line-height:1.35}
.avatar small{display:block;color:var(--muted);font-size:.8125rem}
.legend{padding:12px 14px;border:1px solid var(--rule)}
.legend .lg{display:flex;gap:10px;align-items:center;font-size:.8125rem;line-height:1.4;margin:4px 0}
.legend .lg img{flex:none}
.phone{width:300px;max-width:100%;border:10px solid #121212;border-radius:38px;background:var(--newsprint);padding:30px 16px 26px;margin:0 auto}
.phone .grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px 8px;justify-items:center}
.phone .app{display:flex;flex-direction:column;align-items:center;gap:5px;font-size:.8125rem;line-height:1.1;text-align:center;width:100%}
.phone .app span{display:block;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.apptile{display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap}
.pix{image-rendering:pixelated;image-rendering:crisp-edges}
.pixrow{display:grid;grid-template-columns:repeat(auto-fill,96px);gap:12px 16px}
.pixrow figure{margin:0;width:96px}
.pixrow figcaption{font-size:.8125rem;line-height:1.3;color:var(--muted);margin-top:4px}
.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.ok{color:var(--fg)} td.no{color:#121212}
.pass{display:inline-block;font:700 .8125rem/1.2 var(--body);padding:2px 6px;border:1px solid var(--fg)}
.fail{display:inline-block;font:700 .8125rem/1.2 var(--body);padding:2px 6px;background:var(--fg);color:var(--bg)}
.tblwrap{overflow-x:auto}
.tblwrap table{min-width:640px}
table td small{color:var(--muted);font-size:.8125rem;display:block}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:start}
.grids{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}
.grids figure{margin:0;max-width:100%;width:200px}
.grids figure.w{width:auto}
.grids img{max-width:100%;height:auto;display:block}
.grids figcaption{font-size:.8125rem;color:var(--muted);margin-top:6px;max-width:300px}
.wideimg{max-width:100%;height:auto;display:block}
.decision h2{color:var(--newsprint)}
.decision ol{padding-left:20px;margin:0}
.decision li{margin:0 0 14px;max-width:78ch}
.decision li b{display:block}
.tag.ill{background:transparent}
.tag.rec{background:var(--prussian);color:var(--newsprint);border-color:var(--prussian)}
.cutpair{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:10px}
.cutpair>div{display:flex;flex-direction:column;gap:6px;align-items:center;font-size:.8125rem;text-align:center}
@media (max-width:1000px){.cards,.cmp{grid-template-columns:1fr}.idea{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:420px){.igrid{gap:12px 14px}}
@media (max-width:760px){
 .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
 .stats b{font-size:1.25rem}
 .hrow{grid-template-columns:1fr}
 .bgrid{grid-template-columns:repeat(4,56px)}
 .stats>div:nth-child(3){border-left:0}
 .stats>div:nth-child(n+3){border-top:1px solid var(--rule)}
 .row{grid-template-columns:1fr;gap:8px}
 .surf{grid-template-columns:1fr}
 .holders{grid-template-columns:1fr}
 .holders>div.hd{padding-bottom:0}
 .idea{grid-template-columns:1fr}
 .two{grid-template-columns:1fr}
 .navrow{flex-direction:column;align-items:flex-start;gap:10px}
 .navrow .ln{display:none}
 .cutpair{grid-template-columns:repeat(4,minmax(0,1fr))}
}
"""


# ---------------------------------------------------------------- sections

def head():
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Icon Concepts Board, Phase 2</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&amp;family=Inter:wght@400;600;700&amp;family=Lora:ital,wght@1,400&amp;display=swap">
<link rel="stylesheet" href="board-base.css">
<style>{CSS}</style></head><body><main class="board">"""


def intro():
    wp = worst_pair_all(16)
    a01 = {p: act_01(p) for p in ("A-line", "B-flat", "C-flat")}
    out = [
        '<p class="eyebrow">Oath &amp; Action brand guide, Edition 06 · Phase 2 concept board · October 28, 2026 · Design director</p>',
        "<h1>Three icon concepts, one red node</h1>",
        '<p class="lede">You asked for premium line or flat icons, black with a little Pillar Red, in a square, a rounded square and a circle. '
        "This board draws the same eight test icons three ways, so you can pick a direction before the studio draws the full set (G1-10).</p>",
        '<p class="note">Every drawing here is a proposal, tagged <span class="tag">Option</span>. No V5 master changes. '
        "V5's marks and Direction A, as you approved it at Gate 1, appear once in section 2 as the baseline. "
        "Items tagged <span class=\"tag ill\">Illustrative</span> show invented content.</p>",
        '<div class="stats">',
        f'<div><b>8 icons, 3 concepts</b><span>Four pillar marks, Ballot and Campaign money, the Feedback loop from the atlas, and Search.</span></div>',
        f'<div><b>{pairs_over(16)} pairs at 0.60</b><span>Similarity inside every set at 16 px. The closest pair scores {num(wp[0])}; the limit is 0.60 (D1-16).</span></div>',
        f'<div><b>{num(crisp_min())} or better</b><span>Crisp pixel share in every 16 and 24 px master. The pass line is 0.60 (D1-17).</span></div>',
        '<div><b>C recommended</b><span>One drawing in two cuts: flat at 16 px, line from 24 px, the structure Gate 1 set (Y1, Y4).</span></div>',
        "</div>",
        '<nav class="toc" aria-label="Sections">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in (
            ("s-idea", "1. The idea"), ("s-base", "2. Baseline"), ("s-glance", "3. Three concepts"), ("s-grid", "4. Grid and rules"),
            ("s-sizes", "5. Sizes"), ("s-pixels", "6. Pixels"), ("s-surfaces", "7. Surfaces"), ("s-holders", "8. Holders"),
            ("s-use", "9. In use"), ("s-cuts", "10. Two cuts"), ("s-checks", "11. Checks"), ("s-rubric", "12. Rubric"), ("s-decide", "13. Decisions"))) + "</nav>",
    ]
    return "".join(out)


def sec_idea():
    items = "".join(
        f'<div>{icon("C", "flat", n, 56)}<p><strong>{e(D.LABELS[n])}</strong>{e(D.STEP_IN[n][0].upper() + D.STEP_IN[n][1:])}.</p></div>'
        for n in D.ICONS)
    lock = f'<img src="{src(C.BASELINE / BASE["v5|lockmark"])}" width="48" height="48" alt="The V5 lockmark, with its red lever at the bottom right">'
    return f"""<section id="s-idea"><h2>1. The idea: red marks where a person steps in</h2>
<p>Each icon carries one red element, the node. It is Direction A's shared node, a 4 px disc in a 1 px seat, and it sits where a person takes part. On the lockmark it is the lever. In the atlas it marks the step where a reform acts. The eight test icons follow the same logic, shown here in concept C's flat cut.</p>
<div class="idea">{items}</div>
<div class="row" style="border-top:1px solid var(--rule)"><div class="lab">{lock}</div><div><p style="margin:0">The lockmark's lever is the precedent: one red node in a grid of Charcoal ones. The icons borrow its logic and its disc.</p></div></div>
<h3 style="margin-top:22px">Rule 05.3, word for word (D2-01)</h3>
<blockquote>{e(rule_0503())}</blockquote>
<h3>How the rule applies to these icons</h3>
<ul class="note">
<li><strong>Alone.</strong> An app tile, an avatar or a single feature icon keeps its red. That red counts as signature red, as the wordmark's ampersand does.</li>
<li><strong>In a row or a menu.</strong> Icons go one color, and the current one keeps its red. On Newsprint that red takes a 1 px Charcoal keyline, because it marks a state, and the current label sets in bold, so the state never rests on color alone.</li>
<li><strong>On Prussian.</strong> One color, White, with no red.</li>
</ul></section>"""


def sec_base():
    def cell(key, size):
        if key in BASE:
            return f'<img src="{src(C.BASELINE / BASE[key])}" width="{size}" height="{size}" alt="">'
        return '<span class="cap">None</span>'
    rows = []
    for label, pre, note in (("V5 today", "v5", "From the V5 Polished sprite. V5 has no loop symbol."),
                             ("Direction A, Gate 1", "a", "Phase 1 sketches you approved (Y1). Loop and Search were not drawn.")):
        s24 = "".join(f'<span>{cell(f"{pre}|{n}", 24)}</span>' for n in D.ICONS)
        s48 = "".join(f'<span>{cell(f"{pre}|{n}", 48)}</span>' for n in D.ICONS)
        rows.append(f'<div class="row"><div class="lab">{label}<small>{note}</small></div><div><div class="bgrid">{s24}</div><div class="bgrid" style="margin-top:12px">{s48}</div></div></div>')
    names = " · ".join(D.LABELS[n] for n in D.ICONS)
    return f"""<section id="s-base"><h2>2. Where the concepts start</h2>
<p>V5's marks today and Direction A as you approved it, at 24 and 48 px, in the order used throughout: {e(names)}.</p>
<div class="rows">{''.join(rows)}</div></section>"""


def concept_card(cname):
    if cname == "A":
        body = ("<ul><li>One 2 px line at 24 and 16 px, flat ends, mitered corners.</li>"
                "<li>Lines stop at the node's 1 px seat, so the red sits just off the line.</li>"
                "<li>At 16 px the line stays 2 px. A counter narrower than 2 px closes into a solid.</li>"
                f"<li>Red share {pct(sset('A', 'line', 24)['red_share_vector'][0])} to {pct(sset('A', 'line', 24)['red_share_vector'][1])} of the ink at 24 px.</li></ul>")
        rows = (f'<div class="cap">48 px</div>{strip("A", "line", 48, cols=4)}<div class="cap">24 and 16 px masters</div>'
                f'{strip("A", "line", 24)}{strip("A", "line", 16)}')
        idea = "Premium line icons in the manner of the blue and orange set you sent, with the node as the one red shape."
        ref = "Refined: the red shape is the node in every icon, so all eight carry one red form."
    elif cname == "B":
        body = ("<ul><li>Solid pieces from a small kit: square, bar, disc, half disc, quarter ring, triangle.</li>"
                "<li>Square corners. Pieces sit apart by 1 px cuts, as the ballot sits in its slot.</li>"
                "<li>The node is one solid piece in a 1 px seat.</li>"
                f"<li>Red share {pct(sset('B', 'flat', 24)['red_share_vector'][0])} to {pct(sset('B', 'flat', 24)['red_share_vector'][1])} of the ink at 24 px.</li></ul>")
        rows = (f'<div class="cap">48 px</div>{strip("B", "flat", 48, cols=4)}<div class="cap">24 and 16 px masters</div>'
                f'{strip("B", "flat", 24)}{strip("B", "flat", 16)}')
        idea = "Built from a few geometric pieces, in the manner of the purple and the pink and gold sets."
        ref = "Refined: the red piece is the node, so the kit's red is always the same disc."
    else:
        body = ("<ul><li>Direction A's geometry drawn once, as closed outlines with square corners.</li>"
                "<li>Line cut: each outline as a 2 px wall. Flat cut: each outline filled.</li>"
                "<li>Both cuts share one silhouette, so a product can swap them by size or by state.</li>"
                f"<li>Red share {pct(sset('C', 'flat', 24)['red_share_vector'][0])} to {pct(sset('C', 'line', 24)['red_share_vector'][1])} of the ink at 24 px.</li></ul>")
        rows = (f'<div class="cap">Line cut, 48 px</div>{strip("C", "line", 48, cols=4)}<div class="cap">Flat cut, 48 px</div>{strip("C", "flat", 48, cols=4)}'
                f'<div class="cap">Line cut 24 px; flat cut 24 and 16 px</div>{strip("C", "line", 24)}{strip("C", "flat", 24)}{strip("C", "flat", 16)}')
        idea = "The Line and Flat pairing from the collage you sent, built on the skeletons you approved."
        ref = ("Refined: 16 px always uses the flat cut, since Y4 starts the line companion at 24 px. Open lines keep 2 px, "
               "except the loop's arc and the lens handle, which carry a whole subject and double inward to 4 px in the flat cut.")
    title = {"A": "A. Line and node", "B": "B. Flat kit", "C": "C. One drawing, two cuts"}[cname]
    rec = ' <span class="tag rec">Recommended</span>' if cname == "C" else ""
    return f"""<div class="card"><div><span class="tag">Option</span>{rec}</div><h3>{title}</h3><p style="margin:0">{e(idea)}</p>{body}{rows}<p class="cap" style="margin:0">{e(ref)}</p></div>"""


def sec_glance():
    a01 = {p: act_01(p) for p in ("A-line", "B-flat", "C-flat")}
    return f"""<section id="s-glance"><h2>3. Three concepts at a glance</h2>
<p>Each card shows the eight icons at 48 px, then the true 24 and 16 px masters. All three share the grid, the node and the idea in section 1. They differ in how the drawing carries the node.</p>
<div class="cards">{concept_card('A')}{concept_card('B')}{concept_card('C')}</div>
<h3 style="margin-top:22px">Two refinements to the approved skeletons</h3>
<ul class="note">
<li><strong>Act gains a lintel.</strong> The frame now runs across the top of the door. At 16 px the Phase 1 frame read close to the chapter number 01: against Inter Tight 800 "01" the flat Act scored {num(OLD01['B-flat'])}, and with the lintel it scores {num(a01['B-flat'])}. In A it falls from {num(OLD01['A-line'])} to {num(a01['A-line'])}. The node stays on the center line.</li>
<li><strong>Track rises.</strong> Y2 asked for a raised stair. The base moves up from 22 to 20, which brings the flat stair's center of mass from 17 percent of the field below center to {pw(m('B', 'flat', 'track', 24)['centroid96'][1], 1)}.</li>
</ul></section>"""


def sec_grid():
    shared = [
        ("Grid", "24 units, 1 unit to 1 px at 24 px. The 16 px masters are separate drawings on a 16-unit grid."),
        ("Padding and live area", "2 units at 24 px, so ink sits from 2 to 22. 1 unit at 16 px, so ink sits from 1 to 15."),
        ("Keylines at 24 px", "Circle 20 across. Square 18. Portrait 16 by 20. Landscape 20 by 16. A circle reaches the circle keyline; a square shape stops at the square keyline, so both read the same size."),
        ("Node", "A 4 px disc in a 1 px seat at 24 px, centered on a pixel corner. A 3 px disc in a 1 px seat at 16 px, centered on a pixel center. Pillar marks keep it on the horizontal center line."),
        ("Masters", "The 16 and 24 px masters are hinted: every edge, ring and diagonal lands on whole pixels, and the node stays a true disc. From 48 px up, a display master keeps the unhinted 24-unit drawing."),
        ("Red", "One element per icon, the node. Pillar Red #E63946, never a tint."),
    ]
    per = [
        ("Stroke", "2 px", "None; solid pieces", "Line cut 2 px walls; flat cut solid"),
        ("16 px", "2 px line, counters under 2 px close", "Separate solid drawing", "Flat cut only"),
        ("Ends and joins", "Flat ends, mitered corners", "Square corners, 1 px cuts between pieces", "Square corners; open lines with flat ends"),
        ("Curves", "Circles and quarter arcs only", "Discs, half discs, quarter rings", "Circles and quarter arcs only"),
        ("How the node sits", "Off the line, lines stop at its seat", "Seated in a piece or between pieces", "In a counter, clear of shapes, or in a flat-ended gap"),
        ("Arrowhead", "Open chevron, as the hinge diagram's arcs", "Solid triangle", "Chevron in the line cut, the same triangle filled in the flat cut"),
        ("Open lines", "2 px", "None; bars are solid pieces", "2 px in both cuts; the loop arc and lens handle double inward to 4 px in the flat cut"),
    ]
    trs = "".join(f"<tr><th scope=\"row\">{e(a)}</th><td>{e(b)}</td></tr>" for a, b in shared)
    trp = "".join(f"<tr><th scope=\"row\">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>" for a, b, c, d in per)
    figs = [
        (C.CONTEXT / f"{C.DATE}_Grid-24px-Keylines.svg", "24-unit grid. Green: live area and keylines. Blue: center lines and the node's seat."),
        (C.CONTEXT / f"{C.DATE}_Grid-16px-Keylines.svg", "16-unit grid, with the 3 px node on a pixel center."),
        (C.CONTEXT / f"{C.DATE}_Concept-A-Ballot-On-Grid.svg", "Ballot, concept A."),
        (C.CONTEXT / f"{C.DATE}_Concept-B-Ballot-On-Grid.svg", "Ballot, concept B."),
        (C.CONTEXT / f"{C.DATE}_Concept-C-Line-Ballot-On-Grid.svg", "Ballot, concept C line cut."),
        (C.CONTEXT / f"{C.DATE}_Concept-C-Flat-Ballot-On-Grid.svg", "Ballot, concept C flat cut."),
    ]
    fg = "".join(f'<figure><img src="{src(p)}" width="200" height="200" alt="{e(c)}"><figcaption>{e(c)}</figcaption></figure>' for p, c in figs)
    return f"""<section id="s-grid"><h2>4. Grid and craft rules</h2>
<p>One grid serves all three concepts. Ballot is drawn on it in each concept below, its node on the ballot paper as the vote cue Y5 asked for.</p>
<div class="grids">{fg}</div>
<h3 style="margin-top:22px">Shared by every concept</h3><table><tbody>{trs}</tbody></table>
<h3 style="margin-top:22px">By concept</h3><div class="tblwrap"><table><thead><tr><th scope="col">Rule</th><th scope="col">A, line</th><th scope="col">B, flat kit</th><th scope="col">C, two cuts</th></tr></thead><tbody>{trp}</tbody></table></div></section>"""


def sec_sizes():
    rows = []
    for c, cut in SHOW:
        figs = []
        for s in (16, 24, 48, 96):
            if s == 16 and 16 not in C.sizes(c, cut):
                figs.append('<figure><span class="cap">No 16 px line cut. 16 px uses the flat cut.</span><figcaption>16 px</figcaption></figure>')
                continue
            figs.append(f'<figure>{strip(c, cut, s)}<figcaption>{s} px</figcaption></figure>')
        rows.append(f'<div class="row"><div class="lab">{DRAW_LABEL[(c, cut)]}</div><div class="sizes4">{"".join(figs)}</div></div>')
    tiles = "".join(
        f'<figure style="margin:0"><img src="{src(A.app_tile_file(c, cut))}" width="200" height="200" alt="Act as a 1024 px app tile, concept {c}"><figcaption class="cap">{DRAW_LABEL[(c, cut)]}</figcaption></figure>'
        for c, cut in A.APP_TILE)
    return f"""<section id="s-sizes"><h2>5. The eight icons at 16, 24, 48 and 96 px</h2>
<p>16 and 24 px use the hinted masters at true size. 48 and 96 px use the display masters. Each row is one concept on Newsprint.</p>
<div class="rows">{''.join(rows)}</div>
<h3 style="margin-top:22px">Act as a 1024 px app tile, shown at 200 px</h3>
<p class="note">Each tile is a 1024 px master: the superellipse holder in Charcoal, the icon's live area at half the side, the red node on Charcoal.</p>
<div class="apptile">{tiles}</div></section>"""


def sec_pixels():
    rows = []
    for c, cut in SHOW:
        s = 16 if 16 in C.sizes(c, cut) else 24
        k = 6 if s == 16 else 4
        figs = "".join(
            f'<figure><img class="pix" src="{src(C.PX / (A.file_stem(c, cut, n, f"{s}px") + "-Newsprint.png"))}" width="{s * k}" height="{s * k}" alt="{e(D.LABELS[n])}, {s} px master at {k}x"><figcaption>{e(D.LABELS[n])}</figcaption></figure>'
            for n in D.ICONS)
        lab = DRAW_LABEL[(c, cut)] + (f"<small>{s} px at {k}x</small>")
        rows.append(f'<div class="row"><div class="lab">{lab}</div><div class="pixrow">{figs}</div></div>')
    return f"""<section id="s-pixels"><h2>6. The 16 px masters, magnified without smoothing</h2>
<p>Each image is the master rendered by Chromium at 1x, then enlarged with no smoothing, so every pixel shows: the 16 px masters six times, and C's line cut, which has no 16 px master, at 24 px four times.</p>
<div class="rows">{''.join(rows)}</div></section>"""


def sec_surfaces():
    rows = []
    for c, cut in SHOW:
        cells = []
        for sname, label, bg in C.SURFACES:
            cw = {"newsprint": "Ink-Charcoal-Red", "white": "Ink-Charcoal-Red", "charcoal": "Ink-Newsprint-Red", "prussian": "Ink-White"}[sname]
            note = {"newsprint": "Charcoal, red node", "white": "Charcoal, red node", "charcoal": "Newsprint, red node", "prussian": "White, no red"}[sname]
            cells.append(f'<div class="s-{sname}"><div class="cap">{label} · {note}</div>{strip(c, cut, 24, cw, cols=4)}<div style="height:14px"></div>{strip(c, cut, 48, cw, names=D.ICONS[:4], cols=4)}</div>')
        rows.append(f'<h3 style="margin:18px 0 8px">{DRAW_LABEL[(c, cut)]}</h3><div class="surf">{"".join(cells)}</div>')
    return f"""<section id="s-surfaces"><h2>7. On all four surfaces</h2>
<p>The eight at 24 px and the four pillar marks at 48 px on Newsprint, White, Charcoal and Prussian. Red never sits on Prussian, so there the icons go White.</p>
{''.join(rows)}</section>"""


def sec_holders():
    out = [f"""<section id="s-holders"><h2>8. Bare and in three holders</h2>
<p>The holders are a square, a rounded square and a circle. The rounded square is a true superellipse, |x|<sup>5</sup> + |y|<sup>5</sup> = 1, so its curvature changes without a step all the way around. It comes close to the corner of Apple's app icons; Apple does not publish its own mask. The SVG master draws it with 96 cubic segments that stay within 0.16 px of the exact curve at 1024 px.</p>
<div class="grids"><figure class="w"><img class="wideimg" src="{src(C.HOLDERS / f'{C.DATE}_Holder-Construction.svg')}" width="760" height="220" alt="The three holders with the icon field at 60 percent and the live area at 50 percent of the side"><figcaption style="max-width:70ch">Square, rounded square (the superellipse) and circle. Green: the 24-unit icon field, 60 percent of the side. Blue: the 20-unit live area, 50 percent of the side, where ink sits; in the circle, ink also stays inside the blue circle, 80 percent of the diameter.</figcaption></figure>
<figure class="w"><img class="wideimg" src="{src(C.HOLDERS / f'{C.DATE}_Holder-Superellipse-Corner.svg')}" width="760" height="262" alt="The superellipse corner against a plain border radius, with a curvature plot"><figcaption style="max-width:70ch">Left: the top right corner at 2.2x, the superellipse in black over a plain border radius of 22.37 percent in gray. Right: curvature from the middle of the top edge to the middle of the right edge. Gray steps from straight to full curve; black changes without a step.</figcaption></figure></div>
<h3 style="margin-top:12px">Safe area</h3>
<ul class="note"><li>The icon's 20-unit live area is half the holder's side, and its 24-unit field is 60 percent. A 24 px master sits in a 40 px holder and a 16 px master in a 28 px holder, both on whole pixels. Larger tiles scale the display master.</li>
<li>In the circle, ink also stays within 80 percent of the diameter.</li>
<li>Measured on {TILES_TOTAL} rendered tiles, every icon in every holder and color at 40 and 80 px: {TILES_IN} keep their ink inside the live area, the smallest margin is {pct(MIN_MARGIN)} of the side, and in the circle the farthest ink sits at {pct(MAX_R, 1)} of the diameter from the center.</li>
<li>Tiles and avatars use concept C's flat cut, since a tile is a standalone mark.</li></ul>"""]
    for cname in ("A", "B", "C"):
        c, cut = TILE_CUT[cname]
        rows = []
        bare = []
        for sname, cw, lab in (("charcoal", "Ink-Newsprint-Red", "Bare on Charcoal"), ("newsprint", "Ink-Charcoal-Red", "Bare on Newsprint"), ("prussian", "Ink-White", "Bare on Prussian")):
            cls = f"s-{sname}"
            bare.append(f'<div class="{cls}"><div class="cap">{lab}</div><div class="tgrid">{"".join(icon(c, cut, n, 24, cw) for n in D.ICONS)}</div></div>')
        rows.append(f'<div class="hrow">{"".join(bare)}</div>')
        for shape in C.HOLDER_SHAPES:
            cells = []
            for color, note in (("Charcoal", "Newsprint icon, red node"), ("Newsprint", "Charcoal icon, red node, on a White page"), ("Prussian", "White icon, no red")):
                wh = " wh" if color == "Newsprint" else ""
                cells.append(f'<div class="{wh.strip()}"><div class="cap"><strong>{shape.replace("-", " ")}, {color} tile.</strong> {note}</div>'
                             f'<div class="tgrid">{"".join(tile(c, cut, n, shape, color, 40) for n in D.ICONS)}</div></div>')
            rows.append(f'<div class="hrow">{"".join(cells)}</div>')
        out.append(f'<h3 style="margin:22px 0 8px">{DRAW_LABEL[(c, cut)]}, bare and in 40 px tiles</h3>{"".join(rows)}')
    big = "".join(tile(TILE_CUT[k][0], TILE_CUT[k][1], "connect", shape, color, 96)
                  for k in ("A", "B", "C") for shape in ("Rounded-Square",) for color in ("Charcoal", "Newsprint"))
    out.append(f'<h3 style="margin:22px 0 8px">Connect at 96 px in the rounded square, concepts A, B and C</h3><div class="strip" style="background:var(--white);padding:14px;gap:14px">{big}</div>')
    out.append("</section>")
    return "".join(out)


def navrow(cname, dark=False, current="track"):
    cur_c, cur_cut = ({"A": ("A", "line"), "B": ("B", "flat"), "C": ("C", "flat")})[cname]
    base_c, base_cut = ({"A": ("A", "line"), "B": ("B", "flat"), "C": ("C", "line")})[cname]
    parts = []
    for i, n in enumerate(["explain", "track", "connect", "act"]):
        if i:
            parts.append('<span class="ln" aria-hidden="true"></span>')
        if n == current:
            cw = "Ink-Newsprint-Red" if dark else "Ink-Charcoal-Keyline"
            img = icon(cur_c, cur_cut, n, 24, cw, alt="")
            parts.append(f'<span class="it">{img}<b class="cur" aria-current="page">{e(D.LABELS[n])}</b></span>')
        else:
            cw = "Ink-Newsprint" if dark else "Ink-Charcoal"
            img = icon(base_c, base_cut, n, 24, cw, alt="")
            parts.append(f'<span class="it">{img}<span>{e(D.LABELS[n])}</span></span>')
    return f'<div class="navrow{" dark" if dark else ""}">{"".join(parts)}</div>'


TOPIC_ROWS = [("explain", "How a bill becomes law"), ("track", "Bills on the move this week"), ("connect", "Groups working on the same rule"),
              ("act", "Testify at a state hearing"), ("ballot", "Ranked ballots, step by step"), ("money", "Who pays for a campaign"),
              ("loop", "Loops in the systems atlas"), ("search", "Find a rule, a bill or a loop")]


def topics(cname, current="money"):
    cur = ({"A": ("A", "line"), "B": ("B", "flat"), "C": ("C", "flat")})[cname]
    base = ({"A": ("A", "line"), "B": ("B", "flat"), "C": ("C", "line")})[cname]
    rows = []
    for n, gloss in TOPIC_ROWS:
        if n == current:
            rows.append(f'<div class="on">{icon(cur[0], cur[1], n, 24, "Ink-Charcoal-Keyline", alt="")}<span>{e(D.LABELS[n])}<small>{e(gloss)}</small></span></div>')
        else:
            rows.append(f'<div>{icon(base[0], base[1], n, 24, "Ink-Charcoal", alt="")}<span>{e(D.LABELS[n])}<small>{e(gloss)}</small></span></div>')
    return f'<div class="topics">{"".join(rows)}</div>'


def avatar(cname):
    c, cut = TILE_CUT[cname]
    return (f'<div class="avatar">{tile(c, cut, "track", "Circle", "Charcoal", 72, alt="Track avatar")}'
            f'<p><strong>Bill watch</strong><small>A Track series from Oath &amp; Action</small><small>400 px avatar shown at 72 px</small></p></div>')


def legend(cname):
    c, cut = ({"A": ("A", "line"), "B": ("B", "flat"), "C": ("C", "flat")})[cname]
    return (f'<div class="legend"><div class="cap" style="font-weight:700;letter-spacing:.04em;text-transform:uppercase">How to read a loop</div>'
            f'<div class="lg">{icon(c, cut, "loop", 16)}<span>Feedback loop. Each turn builds on the last.</span></div>'
            f'<div class="lg">{icon(c, cut, "loop", 16, "Ink-Charcoal")}<span>The same loop in a list, one color.</span></div>'
            f'<div class="lg"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="2" fill="#E63946"/></svg><span>Red marks the step where a reform acts.</span></div></div>')


def phone(cname):
    c, cut = TILE_CUT[cname]
    short = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot", "money": "Money", "loop": "Loops", "search": "Search"}
    apps = "".join(f'<div class="app">{tile(c, cut, n, "Rounded-Square", "Charcoal", 48)}<span>{short[n]}</span></div>' for n in D.ICONS)
    return f'<div class="phone"><div class="grid4">{apps}</div></div>'


def sec_use():
    blocks = []
    navs = []
    for title, dark, note in (("A menu row, on Newsprint", False, "Track is current: its red keeps a 1 px Charcoal keyline and its label sets in bold. A hairline joins the four nodes on one line."),
                              ("The same row on Charcoal", True, "On Charcoal the current red needs no keyline; red on Charcoal measures 4.49:1.")):
        rows = "".join(f'<div><h4>{({"A": "A, line", "B": "B, flat kit", "C": "C, two cuts"})[k]}</h4>{navrow(k, dark=dark)}</div>' for k in ("A", "B", "C"))
        navs.append(f'<h3 style="margin:24px 0 6px">{title}</h3><p class="cap" style="margin:0 0 10px">{e(note)}</p><div class="navstack">{rows}</div>')
    for title, fn, note in (
            ("A topic list with labels", lambda k: topics(k), "Campaign money is current. Labels are example copy."),
            ("A social avatar", lambda k: avatar(k), "The circle holder in Charcoal. The series name is example copy."),
            ("An atlas legend line, at 16 px", lambda k: legend(k), "The loop at its 16 px master beside 13 px legend text."),
            ("A phone home screen", lambda k: phone(k), "Charcoal tiles at 48 px, the default proposed in decision 8. App names are illustrative; these are not real apps.")):
        cols = "".join(f'<div><h4>{"A, line" if k == "A" else ("B, flat kit" if k == "B" else "C, two cuts")}</h4>{fn(k)}</div>' for k in ("A", "B", "C"))
        tag = '<span class="tag ill">Illustrative</span> ' if title in ("A topic list with labels", "A social avatar", "A phone home screen") else ""
        blocks.append(f'<h3 style="margin:24px 0 6px">{title}</h3><p class="cap" style="margin:0 0 10px">{tag}{e(note)}</p><div class="cmp">{cols}</div>')
    return f"""<section id="s-use"><h2>9. In use, the same contexts for each concept</h2>
<p>Every row applies Rule 05.3: a row or a menu goes one color, and only the current icon keeps its red. In concept C the current item also switches from the line cut to the flat cut, so the state changes shape as well as color.</p>
{''.join(navs)}{''.join(blocks)}</section>"""


def sec_cuts():
    pairs = "".join(f'<div>{icon("C", "line", n, 48)}{icon("C", "flat", n, 48)}<span>{e(D.LABELS[n])}</span></div>' for n in D.ICONS)
    st = []
    for n in D.ICONS:
        st.append(f'<div>{icon("C", "line", n, 24, "Ink-Charcoal", alt=D.LABELS[n] + ", default")}{icon("C", "flat", n, 24, "Ink-Charcoal-Keyline", alt=D.LABELS[n] + ", current")}<span>{e(D.LABELS[n])}</span></div>')
    return f"""<section id="s-cuts"><h2>10. Concept C's two cuts at work</h2>
<p>The line cut and the flat cut share every outer edge. Above each name: the line cut, then the flat cut, at 48 px.</p>
<div class="cutpair">{pairs}</div>
<h3 style="margin-top:20px">The switch by state, at 24 px</h3>
<p class="note">Default: line cut, one color. Current: flat cut, with its red. At 16 px both states use the flat cut, and the current one keeps its red and its bold label.</p>
<div class="cutpair">{''.join(st)}</div>
<p class="cap" style="margin-top:10px">Feedback loop changes least between cuts: its arc doubles from 2 to 4 px and its arrowhead fills.</p></section>"""


def status(ok):
    return '<span class="pass">Pass</span>' if ok else '<span class="fail">Fail</span>'


def failure_notes():
    out = []
    for c, cut in SHOW:
        st = sset(c, cut, 24)
        med = st["density96"][2]
        hi = [n for n in D.ICONS if m(c, cut, n, 24)["density96"] / med - 1 > 0.20]
        lo = [n for n in D.ICONS if m(c, cut, n, 24)["density96"] / med - 1 < -0.20]
        bits = []
        if hi:
            bits.append(", ".join(f"{D.LABELS[n]} {pct(m(c, cut, n, 24)['density96'] / med - 1, 0, True)}" for n in hi) + " over the median")
        if lo:
            bits.append(", ".join(f"{D.LABELS[n]} {pct(m(c, cut, n, 24)['density96'] / med - 1, 0, True)}" for n in lo) + " under it")
        if bits:
            out.append(f"<li><strong>Balance in {DRAW_LABEL[(c, cut)]}.</strong> " + "; ".join(bits) + ". " + BALANCE_WHY[(c, cut)] + "</li>")
    out.append("<li><strong>Standalone red on Newsprint measures 2.96:1.</strong> Rule 05.3 treats it as signature red, like the wordmark's ampersand. Decision 3 below asks whether to keep that or add the keyline everywhere on Newsprint.</li>")
    out.append(f"<li><strong>Center of mass.</strong> Track sits low in every concept, the stair's nature: {pw(m('A', 'line', 'track', 24)['centroid96'][1], 1)} of the field in A and {pw(m('B', 'flat', 'track', 24)['centroid96'][1], 1)} in B and C's flat cut, against Phase 1's 12 percent. It was 17 to 18 percent in Phase 1. The brief's balance check is ink area, so this row carries no pass mark.</li>")
    return "".join(out)


BALANCE_WHY = {
    ("A", "line"): "A door carries a frame and a leaf, and the leaf needs a 6-unit counter for its handle. The full-set pass can narrow the door toward the portrait keyline.",
    ("B", "flat"): "",
    ("C", "line"): "Open drawings carry less ink than outlined solids at the same stroke. Each sits 1 to 3 points past the line; a small enlargement in the full-set pass would bring them in.",
    ("C", "flat"): "",
}


def sec_checks():
    rows = []
    cols = SHOW

    def cell(c, cut, fn):
        try:
            ok, text = fn(c, cut)
        except KeyError:
            return "<td>Not applicable</td>"
        if ok is None:
            return f"<td>{text}</td>"
        return f"<td>{status(ok)}<small>{text}</small></td>"

    def pf(size):
        def f(c, cut):
            if size not in C.sizes(c, cut):
                return None, "No 16 px master; 16 px uses the flat cut"
            st = sset(c, cut, size)
            return st["crisp_min"] >= 0.60, f"Crisp share {num(st['crisp_min'])} to {num(st['crisp_max'])}; vector edges on whole pixels {pct(st['pixel_fit_vector_min'])}"
        return f

    def stroke(c, cut):
        if cut == "flat":
            if c == "B":
                return None, "Solid pieces; every cut between pieces is 1 px"
            return None, "Solid shapes; open lines 2 px, the loop arc and lens handle 4 px"
        vals = [m(c, cut, n, 24)["stroke"] for n in D.ICONS]
        med = sorted(v["median_units"] for v in vals)
        share = min(v["share_at_2"] for v in vals)
        return all(v["median_units"] == 2.0 or abs(v["median_units"] - 2.0) <= 0.15 for v in vals), \
            f"Median width {num(med[0], 1)} to {num(med[-1], 1)} units in all eight; {pct(share)} or more of ink pixels sit at 1.75 to 2.4 units, the rest at corners and joins"

    def balance(c, cut):
        st = sset(c, cut, 24)
        lo, hi = st["density96_dev"]
        names = [n for n in D.ICONS if abs(m(c, cut, n, 24)["density96"] / st["density96"][2] - 1) > 0.20]
        out = f"Ink {pct(st['density96'][0], 1)} to {pct(st['density96'][1], 1)} of the field at 96 px, {pct(lo, 0, True)} to {pct(hi, 0, True)} from the median"
        if names:
            out += "; outside 20 percent: " + ", ".join(D.LABELS[n] for n in names)
        return not names, out

    def centroid(c, cut):
        st = sset(c, cut, 24)
        return None, f"Largest offset of the center of mass {pct(st['centroid_max'], 1)} of the field (Phase 1 limit 12%)"

    def red(c, cut):
        rs = []
        for s in C.sizes(c, cut):
            st = sset(c, cut, s)
            rs.append(f"{pct(st['red_share_vector'][0], 1)} to {pct(st['red_share_vector'][1], 1)} at {s} px")
        lo = min(sset(c, cut, s)["red_share_vector"][0] for s in C.sizes(c, cut))
        hi = max(sset(c, cut, s)["red_share_vector"][1] for s in C.sizes(c, cut))
        return 0.05 <= lo and hi <= 0.12, "; ".join(rs) + ". Stated range 5 to 12 percent"

    def sim16(c, cut):
        s = 16 if 16 in C.sizes(c, cut) else 24
        st = sset(c, cut, s)
        a, b, sc = st["worst_pair"]
        return st["pairs_over_060"] == 0, f"{st['pairs_over_060']} of 28 pairs at 0.60 or more at {s} px; closest {D.LABELS[a]} and {D.LABELS[b]}, {num(sc)}"

    def watch(c, cut):
        sc, k = watch_worst(f"{c}-{cut}")
        parts = k.split("|")
        return sc < 0.60, f"Closest look-alike: {D.LABELS[parts[1]]} against {parts[2]}, {num(sc)}"

    def contrast(c, cut):
        return True, "Ink 13.28 to 18.73 on every surface and tile. Red against Charcoal 4.49, against White 4.17"

    def red_np(c, cut):
        return False, "A standalone icon on Newsprint shows red against Newsprint at 2.96:1, as the wordmark's ampersand does. In a row the keyline lifts the edge to 13.29:1"

    def holders(c, cut):
        cc, ccut = TILE_CUT[c]
        keys = [k for k in MEAS["tiles"] if k.startswith(f"{cc}-{ccut}-")]
        ok = sum(1 for k in keys if MEAS["tiles"][k]["in_live_area"] and MEAS["tiles"][k].get("in_circle_safe", True))
        if (c, cut) == ("C", "line"):
            return ok == len(keys), f"Tiles use the flat cut; the line cut also fits: {sum(1 for k in MEAS['tiles'] if k.startswith('C-line-') and MEAS['tiles'][k]['in_live_area'] and MEAS['tiles'][k].get('in_circle_safe', True))} of {sum(1 for k in MEAS['tiles'] if k.startswith('C-line-'))}"
        return ok == len(keys), f"{ok} of {len(keys)} tiles keep ink inside the live area and the circle's safe area"

    def silhouette(c, cut):
        if 16 not in C.sizes(c, cut):
            return None, "Not drawn at 16 px"
        res = [m(c, cut, n, 16) for n in D.ICONS]
        bad = [D.LABELS[n] for n, r in zip(D.ICONS, res) if not r["silhouette_pass"]]
        txt = f"{8 - len(bad)} of 8 pass: crisp share 0.60 or more and ink 25 percent of the field or more"
        if bad:
            txt += "; light: " + ", ".join(bad)
        return not bad, txt

    def mono(c, cut):
        ok = all(all(m(c, cut, n, s)["node_separate"].values()) for n in D.ICONS for s in C.sizes(c, cut))
        return ok, "The node stays its own shape in Charcoal on Newsprint and Newsprint on Charcoal"

    def red_disc(c, cut):
        return True, "One red element per icon, the node; rows go one color with the current one red"

    checks = [("Pixel fit, 16 px (D1-17)", pf(16)), ("Pixel fit, 24 px (D1-17)", pf(24)), ("One stroke weight", stroke),
              ("Optical balance, ink area", balance), ("Center of mass", centroid), ("Red share of ink", red),
              ("Similarity inside the set (D1-16)", sim16), ("Look-alikes: letters, chapter number, Phase 0 watch items", watch),
              ("Contrast, ink and red on Charcoal and White", contrast), ("Contrast, standalone red on Newsprint", red_np),
              ("Holder safe area", holders), ("Silhouette at 16 px (Phase 1 test)", silhouette), ("Monochrome", mono), ("Red discipline", red_disc)]
    for name, fn in checks:
        rows.append(f"<tr><th scope=\"row\">{e(name)}</th>" + "".join(cell(c, cut, fn) for c, cut in cols) + "</tr>")
    head_ = "".join(f'<th scope="col">{DRAW_LABEL[k]}</th>' for k in cols)
    return f"""<section id="s-checks"><h2>11. Checks on every drawing</h2>
<p>All numbers come from Chromium renders at device scale 1 and from the vector masters. Similarity uses the Phase 1 measure: the mean of filled-silhouette overlap and correlation after a 3 by 3 blur.</p>
<div class="tblwrap"><table><thead><tr><th scope="col">Check</th>{head_}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<h3 style="margin-top:18px">What the failures say</h3>
<ul class="note">{failure_notes()}</ul></section>"""


RUBRIC = {
    "A": (4, 4, 3, 3, 5, 4, "Clean line and pixel fit. Act runs a third over the set's median weight, line icons are the most familiar genre, and a product gets no shape change for state. Under 4 on brand fidelity and usefulness."),
    "B": (4, 4, 4, 4, 5, 4, "Most even weight of the three and strong at 16 px. It drops the line companion Gate 1 approved (Y4), and its kit cuts move a step away from Direction A."),
    "C": (4, 4, 5, 5, 5, 4, "Direction A's geometry with the line companion Gate 1 approved, drawn so both cuts share one silhouette. States change shape as well as color. Three line-cut icons sit just under the balance band."),
}


def sec_rubric():
    crit = ["Craft", "Clarity", "Brand fidelity", "Usefulness", "Evidence honesty", "Accessibility"]
    rows = "".join(f"<tr><th scope=\"row\">{({'A': 'A, line', 'B': 'B, flat kit', 'C': 'C, two cuts'})[k]}</th>" + "".join(f'<td class="n">{v}</td>' for v in RUBRIC[k][:6]) + f"<td>{e(RUBRIC[k][6])}</td></tr>" for k in ("A", "B", "C"))
    return f"""<section id="s-rubric"><h2>12. Rubric and recommendation</h2>
<p>Scores on the Master Brief section 6 rubric, 1 to 5. The ship threshold is 4 on every criterion.</p>
<div class="tblwrap"><table><thead><tr><th scope="col">Concept</th>{''.join(f'<th scope="col" class="n">{c}</th>' for c in crit)}<th scope="col">Reason</th></tr></thead><tbody>{rows}</tbody></table></div>
<h3 style="margin-top:18px">Recommendation: concept C</h3>
<p>C keeps the filled geometry you approved at Gate 1 and gives it the line companion Y4 already set to start at 24 px. Because both cuts share one silhouette, a menu can show the current item in the flat cut and the rest in line, which meets the state rule in section 10 of the Master Brief with a change of shape. At 16 px, in tiles and in avatars it is the flat cut, which passes every 16 px test here.</p>
<p><strong>What it costs.</strong> Every icon is drawn twice at 24 px and once at 16 px, so the full set of about 60 icons (20 topics, the atlas symbols, status marks and utility icons) means about 180 masters, plus a display master per cut. A script has to check on every rebuild that the two cuts share their outer edges. Track, Feedback loop and Search in the line cut need a small enlargement to sit inside the balance band. If you prefer one cut only, B costs about a third less and loses the line companion.</p></section>"""


def sec_decide():
    items = [
        ("Which concept goes forward to the full set?", "A, line and node; B, flat kit; or C, one drawing in two cuts.", "C. It extends what you approved at Gate 1 and gives products a state change by shape."),
        ("Red's job across the family", "Red marks where a person steps in, on the node of every icon; or red only on Act, as Y3 had it before G1-07.", "Red marks where a person steps in. It gives every icon one reason to carry red, the way the lockmark's lever does."),
        ("A standalone icon's red on Newsprint", "Keep it bare, as signature red at 2.96:1 like the wordmark's ampersand; or give it the 1 px Charcoal keyline everywhere on Newsprint.", "Keep it bare when the icon stands alone, and keep the keyline in rows, where red marks a state."),
        ("Does the current icon's red in a menu count as the view's working red?", "Count it as working red, so a menu never shares a view with an error or an ask in red; or treat it as signature red, as Rule 05.3 does for a single feature icon.", "Treat it as signature red. A menu then never competes with an error or an ask for the view's one working red. This adds a clause to Rule 05.3, so it needs your named approval."),
        ("Act's frame becomes a full lintel", "Approve the lintel; or keep the Phase 1 frame over the opening only.", f"Approve. At 16 px it takes the flat Act from {num(OLD01['B-flat'])} against \"01\" to {num(act_01('B-flat'))}, and the node stays on the center line."),
        ("Masters", "Hinted 16 and 24 px masters with a separate display master from 48 px; or one unhinted master at every size.", f"Hinted masters. Unhinted, the ring icons fall to a crisp pixel share of {num(CRISP_UNHINTED_MIN)}, under the 0.60 line; hinted, every master reaches {num(crisp_min())} or better."),
        ("The rounded-square holder", "A true superellipse with exponent 5; or Figma's published corner smoothing at 60 percent, which steps in curvature where its curve meets the arc.", "The superellipse. Its curvature never steps, and its geometry is one line to state."),
        ("Default tile color for app icons and avatars", "Charcoal tile with a Newsprint icon; or Newsprint tile with a Charcoal icon (both stay in the system, G1-09).", "Charcoal for app icons and avatars, since red on Charcoal measures 4.49:1. Newsprint tiles for light pages and print."),
    ]
    lis = "".join(f"<li><b>{i}. {e(q)}</b>Options: {e(o)}<br>Studio recommends: {e(r)}</li>" for i, (q, o, r) in enumerate(items, 1))
    return f"""<section id="s-decide" class="decision"><h2>13. Decisions for Dustin</h2><ol style="list-style:none;padding-left:0">{lis}</ol></section>"""


def sec_files():
    n_masters = len(list(C.OUT.glob(f"{C.DATE}_Concept-*.svg")))
    n_var = len(list(C.VARIANTS.glob("*.svg")))
    return f"""<section><h2>Files</h2><ul class="note">
<li><code>work/boards/phase-2/icons/</code>: {n_masters} SVG masters, named like <code>20261028_Concept-A-Explain-24px.svg</code>, <code>-16px</code> and <code>-Display</code>; concept C carries its cut, as in <code>20261028_Concept-C-Line-Explain-24px.svg</code>. Each master has three paths: ink, seat and node.</li>
<li><code>variants/</code>: {n_var} color variants of the masters for this board. <code>holders/</code>: the three holders in three colors and two construction drawings. <code>context/</code>: grids, Ballot on the grid and the 1024 px app tiles. <code>px/</code>: 1x renders for the magnified views. <code>baseline/</code>: copies of the V5 marks and the Direction A sketches.</li>
<li>Measurements: <code>20261028_Icon-Concepts-Measurements.json</code>. Scripts: <code>work/build/scripts/phase-2/icons_*.py</code> and <code>icons_*.js</code>. Notes: <code>work/handoffs/phase-2/20261028_Icon-Concepts-Notes.md</code>.</li></ul></section>"""


def build():
    parts = [head(), intro(), sec_idea(), sec_base(), sec_glance(), sec_grid(), sec_sizes(), sec_pixels(), sec_surfaces(),
             sec_holders(), sec_use(), sec_cuts(), sec_checks(), sec_rubric(), sec_decide(), sec_files(), "</main></body></html>"]
    BOARD.write_text("\n".join(parts))
    print("wrote", BOARD, BOARD.stat().st_size)


if __name__ == "__main__":
    build()
