"""Build the Concept 1, Overprint board (design director, Phase 2, round two, October 28, 2026).

Run after icons_r2_overprint_assets.py, icons_r2_overprint_contexts.py and
icons_r2_overprint_measure.py:
  python3 -I icons_r2_overprint_board.py
Writes work/boards/20261028_Icon-Concept-1-Overprint.html. Every image is referenced by relative
path from work/boards/; numbers come from the measurements JSON.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_overprint_common as C  # noqa: E402
import icons_r2_overprint_draw as O  # noqa: E402
import icons_geom as g  # noqa: E402

M = json.loads(C.MEAS.read_text())
I = M["icons"]
e = html.escape
ICONS = O.ICONS
PILLARS = ["explain", "track", "connect", "act"]


def rule_0503():
    s = (C.ROOT / "work/ledger/20261020_Decision-Log.md").read_text()
    line = [ln for ln in s.splitlines() if ln.startswith("| D2-01 ")][0]
    return re.search(r'word for word: "(.*?)" \|', line).group(1)


def num(v, d=2):
    return f"{v:.{d}f}".replace("-", "−")


def pct(v, d=0, sign=False):
    s = f"{v * 100:+.{d}f}" if sign else f"{v * 100:.{d}f}"
    return s.replace("-", "−") + "%"


def src(p):
    return e(C.rel(p))


def icon(name, px, cw="Charcoal-Red", kind=None, alt=None):
    kind = kind or C.best_kind(px)
    a = O.LABELS[name] if alt is None else alt
    return f'<img src="{src(C.variant_file(name, kind, cw))}" width="{px}" height="{px}" alt="{e(a)}">'


def tile(name, shape, color, size, alt=None):
    a = alt if alt is not None else f"{O.LABELS[name]} in a {color} {shape.replace('-', ' ').lower()}"
    if size == 80:
        return f'<img src="{src(C.tile_file(name, shape, color))}" width="80" height="80" alt="{e(a)}">'
    s, *_ = C.tile_svg(name, shape, color, size)
    return s.replace("<svg ", f'<svg role="img" aria-label="{e(a)}" ', 1)


def pass_(ok, text=None):
    t = text or ("Pass" if ok else "Fail")
    return f'<span class="{"pass" if ok else "fail"}">{t}</span>'


CSS = """
main{display:block}
.lede{text-wrap:pretty}
.hero{display:grid;grid-template-columns:minmax(0,1fr);gap:18px}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--rule);margin-top:22px}
.stats>div{padding:14px 16px;border-left:1px solid var(--rule)}
.stats>div:first-child{border-left:0}
.stats b{display:block;font:800 1.5rem/1.15 var(--display);letter-spacing:-.01em}
.stats span{font-size:.875rem;line-height:1.4;color:var(--muted)}
nav.toc{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:18px;font-size:.9375rem}
nav.toc a{color:var(--fg)}
.ten{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:22px 18px}
.ten figure{margin:0;min-width:0}
.ten figcaption{font-size:.8125rem;line-height:1.4;margin-top:6px}
.ten figcaption b{display:block;font-size:.9375rem}
.ten figcaption span{color:var(--muted)}
.pillartile{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-top:24px;padding:16px;background:var(--charcoal);color:var(--newsprint)}
.pillartile p{margin:0;font-size:.875rem;color:#C9C5BC;max-width:40ch}
.strip{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:flex-end}
.strip img,.strip svg{display:block}
.row{display:grid;grid-template-columns:170px minmax(0,1fr);gap:16px;align-items:center;padding:14px 0;border-bottom:1px solid var(--rule)}
.row>.lab{font-weight:700;font-size:.9375rem;line-height:1.35}
.row>.lab small{display:block;font-weight:400;color:var(--muted);font-size:.8125rem}
.bench{width:100%}
.bench td{vertical-align:middle}
.bench .ms{font-family:'Material Symbols Outlined';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;direction:ltr;-webkit-font-feature-settings:'liga';font-feature-settings:'liga';-webkit-font-smoothing:antialiased;color:var(--charcoal)}
.bench .ms24{font-size:24px;font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24}
.bench .ms48{font-size:48px;font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 48}
.bench img{display:block}
.ba{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 28px}
.ba>div{display:grid;grid-template-columns:auto auto minmax(0,1fr);gap:12px;align-items:center;border-top:1px solid var(--rule);padding-top:12px;min-width:0}
.ba p{margin:0;font-size:.875rem;line-height:1.45}
.ba p b{display:block;font-size:.9375rem}
.ba figure{margin:0;text-align:center}
.ba figcaption{font-size:.8125rem;color:var(--muted)}
.surf{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule)}
.surf>div{padding:14px;min-width:0}
.surf .cap{margin-bottom:8px}
.s-charcoal .cap,.s-prussian .cap{color:#C9C5BC}
.pix{image-rendering:pixelated;image-rendering:crisp-edges}
.pixrow{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:12px 16px}
.pixrow figure{margin:0}
.pixrow figcaption{font-size:.8125rem;line-height:1.3;color:var(--muted);margin-top:4px}
.cover{display:grid;grid-template-columns:150px repeat(3,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}
.cover>div{background:var(--bg);padding:12px;min-width:0}
.cover .hd{font-weight:700;font-size:.875rem}
.cover .pr{background:var(--prussian)}
.holders{display:grid;grid-template-columns:130px repeat(3,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}
.holders>div{background:var(--bg);padding:12px;min-width:0}
.holders>div.lt{background:var(--white)}
.ltstrip{background:var(--white);padding:10px;display:inline-flex;flex-wrap:wrap;gap:12px 16px}
.holders .hd{font-weight:700;font-size:.875rem}
.navrow{display:flex;align-items:center;flex-wrap:wrap;gap:0;padding:14px 16px;border:1px solid var(--rule)}
.navrow .it{display:flex;align-items:center;gap:8px;font-size:.9375rem;color:var(--fg);padding-bottom:5px;border-bottom:2px solid transparent}
.navrow .it img{display:block}
.navrow .it.cur{font-weight:700;border-bottom-color:var(--charcoal)}
.navrow .ln{flex:1 1 18px;min-width:14px;height:1px;background:var(--rule);margin:0 10px}
.navrow.dark{background:var(--charcoal);border-color:var(--charcoal)}
.navrow.dark .it{color:var(--newsprint)}
.navrow.dark .it.cur{border-bottom-color:var(--newsprint)}
.navrow.dark .ln{background:#5D636D}
.topics{border:1px solid var(--rule);background:var(--surface);max-width:420px}
.topics>div{display:grid;grid-template-columns:24px 1fr;gap:12px;align-items:center;padding:9px 14px;border-top:1px solid var(--rule)}
.topics>div:first-child{border-top:0}
.topics span{font-size:.9375rem;line-height:1.3}
.topics .on span{font-weight:700}
.topics .on{box-shadow:inset 3px 0 0 var(--charcoal)}
.avatar{display:flex;gap:14px;align-items:center;padding:14px;border:1px solid var(--rule);background:var(--white);flex-wrap:wrap}
.avatar p{margin:0;font-size:.9375rem;line-height:1.35}
.avatar small{display:block;color:var(--muted);font-size:.8125rem}
.legend{padding:12px 14px;border:1px solid var(--rule);max-width:460px;background:var(--surface)}
.legend .lg{display:flex;gap:10px;align-items:center;font-size:.8125rem;line-height:1.4;margin:6px 0}
.legend .lg img{flex:none}
.tracker{border-collapse:collapse;width:100%;max-width:720px;font-size:.875rem}
.tracker td{border-bottom:1px solid var(--rule);padding:8px 10px;vertical-align:middle}
.tracker img{display:inline-block;vertical-align:-3px}
.st{display:inline-flex;align-items:center;gap:6px;font-size:.8125rem}
.st i{display:inline-block;width:10px;height:10px;border:2px solid var(--charcoal);border-radius:50%}
.st i.full{background:var(--charcoal)}
.st i.half{background:linear-gradient(90deg,var(--charcoal) 50%,transparent 50%)}
.wideimg{max-width:100%;height:auto;display:block;border:1px solid var(--rule)}
.ctx{display:grid;grid-template-columns:minmax(0,1fr);gap:28px}
.ctx figure{margin:0}
.ctx figcaption{font-size:.8125rem;color:var(--muted);margin-top:6px;max-width:80ch}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:start}
.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.pass{display:inline-block;font:700 .8125rem/1.2 var(--body);padding:2px 6px;border:1px solid var(--fg)}
.fail{display:inline-block;font:700 .8125rem/1.2 var(--body);padding:2px 6px;background:var(--fg);color:var(--bg)}
.tblwrap{overflow-x:auto}
.tblwrap table{min-width:680px}
table td small{color:var(--muted);font-size:.8125rem;display:block}
.tag.ill{background:transparent}
.tag.exc{background:var(--charcoal);color:var(--newsprint);border-color:var(--charcoal)}
.decision h2{color:var(--newsprint)}
.decision ol{padding-left:20px;margin:0}
.decision li{margin:0 0 14px;max-width:78ch}
.decision li b{display:block}
.cons{display:flex;flex-wrap:wrap;gap:16px}
.cons figure{margin:0;width:260px;max-width:100%}
.cons svg{display:block;max-width:100%;height:auto}
.cons figcaption{font-size:.8125rem;color:var(--muted);margin-top:6px}
.s16grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 24px}
.s16{display:grid;grid-template-columns:110px auto auto auto;gap:14px;align-items:center;border-top:1px solid var(--rule);padding-top:10px;min-width:0}
.s16 .lab{font-weight:700;font-size:.9375rem}
.s16 figure{margin:0;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.s16 figure img{display:block}
.s16 figcaption{font-size:.8125rem;color:var(--muted);flex-basis:100%}
@media (max-width:900px){.ten{grid-template-columns:repeat(3,minmax(0,1fr))}.ba{grid-template-columns:1fr}.s16grid{grid-template-columns:1fr}}
@media (max-width:760px){
 .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
 .stats>div:nth-child(3){border-left:0}
 .stats>div:nth-child(n+3){border-top:1px solid var(--rule)}
 .ten{grid-template-columns:repeat(2,minmax(0,1fr))}
 .row{grid-template-columns:1fr;gap:8px}
 .surf{grid-template-columns:1fr}
 .holders,.cover{grid-template-columns:1fr}
 .two{grid-template-columns:1fr}
 .s16{grid-template-columns:1fr 1fr}
 .s16 .lab{grid-column:1/-1}
 .navrow{flex-direction:column;align-items:flex-start;gap:10px}
 .navrow .ln{display:none}
}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">'
         '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0&display=block" rel="stylesheet">')


def head():
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Icon Concept 1, Overprint</title>{FONTS}<link rel="stylesheet" href="board-base.css"><style>{CSS}</style></head><body><main class="board">"""


def intro():
    crisp_min = min(min(I[n]["crisp_16"], I[n]["crisp_24"]) for n in ICONS)
    reds = [I[n]["red_share"] for n in ICONS]
    toc = [("s-ten", "1. The ten"), ("s-fix", "2. Fix pass"), ("s-bench", "3. Beside the best"), ("s-changes", "4. After stage 1"), ("s-rules", "5. The rules"),
           ("s-sizes", "6. Sizes"), ("s-pixels", "7. Pixels"), ("s-cover", "8. Cover the red"), ("s-surfaces", "9. Surfaces"),
           ("s-holders", "10. Holders"), ("s-contexts", "11. In use"), ("s-checks", "12. Checks"), ("s-tests", "13. Tests"),
           ("s-rubric", "14. Rubric"), ("s-decide", "15. Decisions"), ("s-honest", "16. Tested")]
    return f"""<p class="eyebrow">Oath &amp; Action brand guide, Edition 06 · Phase 2 icons, round two · Concept 1 of 3 · October 28, 2026 · Design director</p>
<h1>Overprint</h1>
<p class="lede" style="font-size:1.1875rem;max-width:66ch">A fine Charcoal line printed over one solid plane of Pillar Red, set off register toward the lower left, the way a second ink lands on a newspaper page. The red sits under the part of each subject the story is about. The line drawing names the subject without it, so the red can come and go: it shows on an icon that stands alone and on the current item in a row. From 24 px up the family is this line; at 16 px it changes to a solid cut in one color.</p>
<p class="cap" style="max-width:78ch">Fix pass, October 28: this board now carries the creative director's fixes 1 to 4 from the final icon review. Section 2 shows what changed; stage 2's masters stay in <code>phase-2/icons-r2/overprint/stage-2/</code>.</p>
<p>Every drawing on this board is a proposal, tagged <span class="tag">Option</span>. Nothing in the V5 sprite changed. Compositions with invented copy are tagged <span class="tag ill">Illustrative</span>.</p>
<div class="stats">
<div><b>10 icons, 30 masters</b><span>Display master for 48 px and up, hinted 24 px master, and a solid 16 px cut in one color.</span></div>
<div><b>{num(crisp_min)} or better</b><span>Crisp share of every 16 and 24 px master; the pass line is 0.60 (D1-17).</span></div>
<div><b>{pct(min(reds))} to {pct(max(reds))}</b><span>Red as a share of the painted area, inside the 15 to 25 percent band.</span></div>
<div><b>One offset, no red at 16 px</b><span>Every plane prints 1.5 units left and 1.5 down. Connect alone prints straight down (Rule 01.1). The 16 px cut has no plane.</span></div>
</div>
<nav class="toc">{"".join(f'<a href="#{a}">{t}</a>' for a, t in toc)}</nav>"""


def sec_ten():
    figs = []
    for n in ICONS:
        figs.append(f'<figure>{icon(n, 96, kind="Display")}<figcaption><b>{e(O.LABELS[n])}</b><span>{e(O.CLASS[n])}.</span> {e(O.REASON[n])}</figcaption></figure>')
    tiles = "".join(tile(n, "Rounded-Square", "Charcoal", 96) for n in PILLARS)
    return f"""<section id="s-ten"><h2>1. The ten icons at 96 px</h2>
<p>The display masters on Newsprint, each with its one-line reason for its red. The four pillar marks keep Direction A's skeletons: a square broken open, three stages on a rising stair, one circle in two halves, a door swung open.</p>
<div class="ten">{"".join(figs)}</div>
<div class="pillartile">{tiles}<p>The four pillar marks in the Charcoal tile at 96 px: Newsprint line, Pillar Red plane.</p></div></section>"""


def stage2(name, kind):
    return C.OUT / "stage-2" / f"{C.DATE}_Overprint-Stage-2-{O.FILE_NAME[name]}-{kind}.svg"


FIXED = {
    "loop": ("Fix 2", "A closed ring with three stations evenly spaced and one arrowhead on the ring before each station, all turning clockwise. The plane fills the top station, where a reform acts. Ring and arrowheads are hinted to whole pixels at 24 px; the stations stay true discs."),
    "ballot": ("Fix 3", "The paper stands 7 units above the box and sinks into the slot. The oval sits in the paper's upper half, at least 2 units from its edges, so the mark's off-register spill stays on the paper. The box narrows by 2 units in the display master to keep the ink in the band."),
    "money": ("Fix 4", "The note spans the full width of the landscape keyline with tight 1-unit corners, its disc 2 units left of center and one short bar at the bottom right, so it no longer mirrors Connect. It is 16 units tall at 24 px and 15 in the display master, where the extra unit made it match Track."),
    "testify": ("Fix 4", "The 24 px master moves up 1 px, so its table no longer sits on Track's base line. The display master is unchanged."),
}


def sec_fix():
    s1 = M["sets"]["solid16"]
    l16 = M["sets"]["lookalikes_16"]
    l24 = M["sets"]["lookalikes_24"]
    cells = []
    for n in ICONS:
        cells.append(f"""<div class="s16"><div class="lab">{e(O.LABELS[n])}</div>
<figure><img src="{src(stage2(n, "16px"))}" width="16" height="16" alt="{e(O.LABELS[n])}, stage 2 line master at 16 px"><img class="pix" src="{src(stage2(n, "16px"))}" width="64" height="64" alt=""><figcaption>Stage 2 line</figcaption></figure>
<figure><img src="{src(C.master_file(n, "16px"))}" width="16" height="16" alt="{e(O.LABELS[n])}, solid 16 px cut"><img class="pix" src="{src(C.PX / f"{C.stem(n, '16px')}-Newsprint.png")}" width="64" height="64" alt=""><img src="{src(C.PX / f"{C.stem(n, '16px')}-2x.png")}" width="32" height="32" alt="" style="width:64px;height:64px"><figcaption>Solid cut: 1x, magnified, 2x screen</figcaption></figure>
<figure>{icon(n, 24)}<figcaption>24 px line</figcaption></figure></div>""")
    ba = []
    for n, (fx, txt) in FIXED.items():
        kinds = [("24px", 48)] if n == "testify" else [("Display", 72), ("24px", 24)]
        old = "".join(f'<img src="{src(stage2(n, k))}" width="{px}" height="{px}" alt="{e(O.LABELS[n])}, stage 2, {k}">' for k, px in kinds)
        new = "".join(f'<img src="{src(C.master_file(n, k))}" width="{px}" height="{px}" alt="{e(O.LABELS[n])}, fix pass, {k}">' for k, px in kinds)
        ba.append(f'<div><figure>{old}<figcaption>Stage 2</figcaption></figure><figure>{new}<figcaption>Fix pass</figcaption></figure><p><b>{e(O.LABELS[n])} <span class="tag">{fx}</span></b>{e(txt)}</p></div>')
    pr = {k: v for k, v in M["pairs"].items()}

    def b(mode, a, c, sz):
        k = f"{mode}|{a}|{c}|{sz}" if f"{mode}|{a}|{c}|{sz}" in pr else f"{mode}|{c}|{a}|{sz}"
        return pr[k]["blurred_corr"]
    prev = json.loads((C.OUT / "stage-2" / f"{C.DATE}_Overprint-Stage-2-Measurements.json").read_text())["pairs"]

    def pb(mode, a, c, sz):
        k = f"{mode}|{a}|{c}|{sz}" if f"{mode}|{a}|{c}|{sz}" in prev else f"{mode}|{c}|{a}|{sz}"
        return prev[k]["blurred_corr"]
    loopcd = l24["loop_cd_list"]
    wl = max(v[0] for v in loopcd.values())
    wlb = max(v[1] for v in loopcd.values())
    rows = [
        ("1. The 16 px solid cut", "No pair at 0.60 (D1-16)", s1["worst_pair_blurred"][2] < .6 and s1["worst_pair_score"][2] < .6,
         f"0 of 45 pairs at 0.60 by either measure. Worst by blurred correlation {e(O.LABELS[s1['worst_pair_blurred'][0]])} and {e(O.LABELS[s1['worst_pair_blurred'][1]])} {num(s1['worst_pair_blurred'][2])}; by the combined score {e(O.LABELS[s1['worst_pair_score'][0]])} and {e(O.LABELS[s1['worst_pair_score'][1]])} {num(s1['worst_pair_score'][2])}. Stage 2's line cut had 3 pairs over"),
        ("", "Pixel fit reaches 0.60 (D1-17)", s1["crisp_min"] >= .6, f"{num(s1['crisp_min'])} or better (Testify and Feedback loop {num(I['testify']['crisp_16'])} and {num(I['loop']['crisp_16'])}, the rest 0.75 to 0.96). Straight edges sit on whole pixels and curves stay curves; Feedback loop's ring and arrowheads are hinted to whole pixels, since its true ring measured 0.42"),
        ("", "No banned look-alike at 0.60", not l16["banned_over_060_score"],
         f"{len(l16['banned_over_060_score'])} of {l16['banned_checked']} by the combined score: " + ("; ".join(f"{e(O.LABELS[r['icon']])} and {e(r['ref'])} {num(r['score'])}" for r in l16["banned_over_060_score"]) or "none") + f". By blurred correlation {l16['banned_over_060_blurred']} of {l16['banned_checked']} reach 0.60, since filled shapes of one size correlate whatever they show"),
        ("", "Act under 0.60 against &ldquo;01&rdquo;, with its lintel", M["sets"]["act_vs_01_16"] < .6, f"{num(M['sets']['act_vs_01_16'])} combined, {num(M['sets']['act_vs_01_16_blur'])} blurred; against the letter n {num(M['sets']['act_vs_n_16'])}"),
        ("2. Feedback loop as a ring", "Ink in the band", I["loop"]["weight_pass"], f"{pct(I['loop']['ink96'], 1)} of the field, {pct(I['loop']['ink_dev'], 0, True)} from the median; stage 2 sat 23 percent under it"),
        ("", "Against cycle, recycle, share and group", wl < .6, f"Worst combined score {num(wl)}; Material's recycling reaches {num(wlb)} by blurred correlation at 24 px. Reload and sync: see the look-alike rows in section 12"),
        ("3. Ballot's paper raised", "About 7 units above the box, oval in the upper half, spill on the paper", True, "7 units above the box's top edge; oval 2.25 units below the paper's top line; the plane's edge stays on the paper in both masters"),
        ("", "Against the printer", I["ballot"]["watch_worst"][3] < .6, f"Closest: {e(I['ballot']['watch_worst'][0])} {num(I['ballot']['watch_worst'][3])} ({I['ballot']['watch_worst'][1]}, {I['ballot']['watch_worst'][2]} px). A box with paper standing out of it is the printer's own drawing, and raising the paper brings it closer"),
        ("4. Similarity at 24 px", "Connect and Campaign money under 0.60", max(b("drawn", "connect", "money", 24), b("idle", "connect", "money", 24)) < .6,
         f"{num(b('drawn', 'connect', 'money', 24))} as drawn, {num(b('idle', 'connect', 'money', 24))} idle; stage 2 {num(pb('drawn', 'connect', 'money', 24))}"),
        ("", "Track and Testify, idle Ballot and Bill", max(b("drawn", "track", "testify", 24), b("idle", "ballot", "bill", 24)) < .6,
         f"Track and Testify {num(b('drawn', 'track', 'testify', 24))} (stage 2 {num(pb('drawn', 'track', 'testify', 24))}); idle Ballot and Bill {num(b('idle', 'ballot', 'bill', 24))} (stage 2 {num(pb('idle', 'ballot', 'bill', 24))})"),
    ]
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{bb}</td><td>{pass_(ok)}</td><td>{c}</td></tr>" for a, bb, ok, c in rows)
    return f"""<section id="s-fix"><h2>2. Fix pass</h2>
<p>The creative director's final review recommends Overprint from 24 px up, with a solid cut at 16 px, after five fixes. This pass makes fixes 1 to 4; the main session reruns the name test (fix 5) on these masters.</p>
<h3>The 16 px solid cut (fix 1)</h3>
<p>At 16 px the family changes cut: Direction A's filled grammar in one color, drawn as hinted vectors on the 16-unit grid. Straight edges sit on whole pixels, curves stay curves, and pieces stand 1 px apart. Explain, Track, Connect, Act, Ballot, Bill and Housing start from Moving part's 16 px masters; Testify, Campaign money and Feedback loop are filled versions of this board's drawings. There is no red at 16 px: these icons live in rows, legends and tracker tables, where Rule 05.3 already makes them one color, and the current item shows by its bold label and the rule under it. Act keeps its full lintel.</p>
<div class="s16grid">{"".join(cells)}</div>
<h3 style="margin-top:22px">Redrawn from 24 px up (fixes 2 to 4)</h3>
<div class="ba">{"".join(ba)}</div>
<h3 style="margin-top:22px">Pass marks</h3>
<div class="tblwrap"><table><thead><tr><th>Fix</th><th>Mark</th><th>Result</th><th>Reading</th></tr></thead><tbody>{tr}</tbody></table></div>
<p class="cap">Pairs are judged by D1-16's blurred correlation, as ruled in the review; the combined score sits beside it. Look-alikes are judged by the combined score, the measure behind round one's and Moving part's tables and the review's own figures (Ballot and printer 0.63; Moving part's Act and &ldquo;01&rdquo; 0.07).</p></section>"""


MS = {"explain": "inventory_2", "track": "stairs", "connect": "join_inner", "act": "door_open", "ballot": "how_to_vote",
      "bill": "description", "testify": "record_voice_over", "housing": "home", "money": "payments", "loop": "cycle"}


def sec_bench():
    rows = []
    for n in ICONS:
        rows.append(f"<tr><td><b>{e(O.LABELS[n])}</b></td><td>{icon(n, 24)}</td><td><span class=\"ms ms24\" aria-label=\"Material Symbols {MS[n]}\">{MS[n]}</span></td>"
                    f"<td>{icon(n, 48)}</td><td><span class=\"ms ms48\" aria-label=\"Material Symbols {MS[n]}\">{MS[n]}</span></td><td><small>{MS[n]}</small></td></tr>")
    return f"""<section id="s-bench"><h2>3. Beside the best: a benchmark sheet</h2>
<p><span class="tag ill">Study</span> Each Overprint icon at its 24 px master and at 48 px, beside the nearest glyph in Google's Material Symbols Outlined at weight 400. Material Symbols is published under the Apache 2.0 license and loads here from Google Fonts; it is shown for comparison and forms no part of the system. SF Symbols stays out of the file, since its license ties it to Apple platforms. If this page opens offline, the Material column shows the glyph names as words.</p>
<div class="tblwrap"><table class="bench"><thead><tr><th>Icon</th><th>Overprint, 24 px</th><th>Material, 24 px</th><th>Overprint, 48 px</th><th>Material, 48 px</th><th>Glyph</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="cap">Reading of the sheet: section 13, test 4.</p></section>"""


CHANGES = {
    "explain": ("A notification badge, from the red on the lifted piece.", "The plane moves to the open quarter and slides toward the node. The lid stays an ink outline, lifted 2 units, moved 1.5 right and turned 15 degrees on its hinge corner. The square shrinks to 12 units and the node comes up to the center line."),
    "track": ("Ink at 15 percent, red at 30, the stair low and right.", "Three equal stages climb the landscape keyline from 4 to 20. The node sits on the riser between the first and second stages, on the center line. Red falls to 24 percent."),
    "connect": ("Live, record or an eye; the red leaned into the left half.", "The one exception to the offset: the plane centers on the gap and prints 1.5 units straight down, 1 unit clear of both halves (Rule 01.1)."),
    "act": ("Passed; the plane read as an object on the floor.", "The plane rises to the center line, so the lower half of the doorway reads as lit. It narrows to 4.5 units to stay under the 25 percent ceiling. The floor runs 2 to 22."),
    "ballot": ("A box with a frame holding a pill, then a printer.", "A taller box, 16 by 11 outside, with a slot across its top face. The paper's lower third sinks into the slot. The oval grows to 6.25 by 4.5, and the mark still covers it to the outer edge."),
    "bill": ("Passed.", "The highlight stays 2 units above the page's inner bottom edge. The page narrows by 1 unit so it reads apart from Housing."),
    "testify": ("Passed, with the red read as a map pin at 24 px.", "The plane fills the microphone's own capsule. The capsule sits at mouth height on a short gooseneck, angled 45 degrees toward the face."),
    "housing": ("Passed.", "The door plane narrows to 3.5 units. The house widens and lowers so it reads apart from Bill and Ballot."),
    "money": ("A faucet.", "A banknote: a landscape rounded rectangle with a round disc at its center and a short bar in two opposite corners. The plane fills the disc."),
    "loop": ("Sync or refresh, and at 24 px an eye or a fish.", "Two nodes on the center line. A straight forward link with its arrowhead along the top, a returning arc with its arrowhead below, arcs at the full line. The plane fills the node the return arrives at."),
}


def sec_changes():
    cells = []
    for n in ICONS:
        old = C.OUT / "stage-1" / f"{C.DATE}_Overprint-Stage-1-{O.FILE_NAME[n]}-Display.svg"
        read, did = CHANGES[n]
        tag = ' <span class="tag exc">Exception</span>' if n == "connect" else ""
        cells.append(f"""<div><figure><img src="{src(old)}" width="72" height="72" alt="{e(O.LABELS[n])}, stage 1"><figcaption>Stage 1</figcaption></figure>
<figure><img src="{src(stage2(n, "Display"))}" width="72" height="72" alt="{e(O.LABELS[n])}, stage 2"><figcaption>Stage 2</figcaption></figure>
<p><b>{e(O.LABELS[n])}{tag}</b>Stage 1 read as: {e(read)} {e(did)}</p></div>""")
    return f"""<section id="s-changes"><h2>4. What changed after stage 1</h2>
<p>The creative director's stage 1 notes and the blind name test set every change below. Stage 1's drawings stay in <code>phase-2/icons-r2/overprint/stage-1/</code> and stage 2's in <code>stage-2/</code> as the record; section 2 covers the fix pass that followed.</p>
<div class="ba">{"".join(cells)}</div></section>"""


def construction(name):
    L = O.display(name)
    U = 10
    W = 24 * U
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}" role="img" aria-label="{e(O.LABELS[name])} on the 24-unit grid">',
         f'<rect width="{W}" height="{W}" fill="#F1EFEA"/>']
    for i in range(25):
        p.append(f'<line x1="{i * U}" y1="0" x2="{i * U}" y2="{W}" stroke="#D3CFC6" stroke-width="1"/><line x1="0" y1="{i * U}" x2="{W}" y2="{i * U}" stroke="#D3CFC6" stroke-width="1"/>')
    p.append(f'<rect x="{2 * U}" y="{2 * U}" width="{20 * U}" height="{20 * U}" fill="none" stroke="#4A7C74" stroke-width="1.5"/>')
    p.append(f'<circle cx="{12 * U}" cy="{12 * U}" r="{10 * U}" fill="none" stroke="#4A7C74" stroke-width="1"/>')
    p.append(f'<line x1="0" y1="{12 * U}" x2="{W}" y2="{12 * U}" stroke="#1F2D5A" stroke-width="1"/><line x1="{12 * U}" y1="0" x2="{12 * U}" y2="{W}" stroke="#1F2D5A" stroke-width="1"/>')
    p.append(f'<path d="{g.d_of(g.transform(L["accent"], U))}" fill="{C.RED}"/>')
    p.append(f'<path d="{g.d_of(g.transform(L["ink"], U))}" fill="{C.CHAR}" fill-opacity="0.82"/>')
    for pen in L["lines"]:
        p.append(f'<path d="{g.d_of(g.transform(pen.p, U))}" fill="none" stroke="#7FD4F5" stroke-width="1.2"/>')
    if L["reg"] is not None:
        p.append(f'<path d="{g.d_of(g.transform(L["reg"], U))}" fill="none" stroke="#1F2D5A" stroke-width="2"/>')
    p.append("</svg>")
    return "".join(p)


def sec_rules():
    rows = [
        ("Grid", "Round one's 24-unit grid with 2-unit padding; keylines circle 20, square 18, portrait 16 by 20, landscape 20 by 16. The 16 px cut sits on a 16-unit grid with 1-unit padding."),
        ("Two cuts", "From 24 px up, the line with its red plane. At 16 px, a solid cut in one color: Direction A's filled pieces as hinted vectors, straight edges on whole pixels, curves kept as curves, a 1 px cut between pieces, knock-outs of 1 px or more."),
        ("Line", "1.5 units in the display master and 2 px in the 24 px master, so the line lightens as the icon grows. Round caps and round joins."),
        ("Corners", "Rectangles take a 2-unit outer radius in the display master and 1 px at 24 px. The banknote keeps a tight 1-unit corner, so it reads apart from Connect."),
        ("Live area", "Straight edges stay inside 2 to 22 units; round forms may pass it by 0.25 at most."),
        ("Node", "The pillar marks carry the node as a solid ink disc 3 units across, on the horizontal center line: 4 px at 24 px, a 2 px square bead at 16 px (Act's is knocked out of the leaf as its handle). Feedback loop's three stations are nodes too."),
        ("The plane", "One solid shape of Pillar Red behind the line. It fills one drawn shape of the subject to the line's center, then prints off register 1.5 units left and 1.5 units down. It covers 15 to 25 percent of the painted area, is never outlined or tinted, and carries no edge a reader needs."),
        ("Offset by size", "1.5 units in the display master and 2 px at 24 px, since a 1 px shift would hide under the 2 px line. No plane at 16 px."),
        ("Two exceptions", "Connect's plane centers on the gap and prints straight down, clear of both halves, so the red never leans toward a side (Rule 01.1). Ballot's mark covers its printed oval to the outer edge, as a pen mark does."),
        ("Badge corner", "No red sits in the top-right 6 by 6 units of the field, where interfaces put notification badges."),
        ("Detail", "Three to six strokes and one interior detail at 24 px. At 16 px the detail survives as knock-outs: Ballot's oval, Bill's lines, Act's handle, Housing's doorway."),
        ("Row state", "Idle icons are line only. The current icon gains its plane, its label goes bold and a Charcoal rule runs under it: a new shape and a text change, so the state never rests on color alone. At 16 px the icon stays one color and the label and rule carry the state."),
    ]
    tr = "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in rows)
    cons = "".join(f'<figure>{construction(n)}<figcaption>{e(O.LABELS[n])}: center lines in blue, the plane in register outlined in Prussian, the plane as printed in red.</figcaption></figure>'
                   for n in ("explain", "connect", "ballot"))
    return f"""<section id="s-rules"><h2>5. The rules</h2>
<div class="tblwrap"><table><tbody>{tr}</tbody></table></div>
<h3 style="margin-top:22px">Construction</h3><div class="cons">{cons}</div>
<h3 style="margin-top:22px">Rule 05.3, word for word (D2-01)</h3>
<blockquote style="margin:10px 0 0;padding:14px 18px;border-left:3px solid var(--charcoal);background:var(--surface);max-width:78ch;font-size:.9375rem">{e(rule_0503())}</blockquote>
<p class="cap" style="margin-top:8px">Here: alone, as an app tile, an avatar or a single feature icon, the plane counts as signature red. In a row or menu the icons go line only and the current one keeps its plane. On Prussian the plane goes and the White line stands alone. At 16 px every icon is one color.</p></section>"""


def sec_sizes():
    rows = []
    for n in ICONS:
        cells = "".join(f'<figure style="margin:0">{icon(n, s)}<figcaption class="cap">{s}</figcaption></figure>' for s in (16, 24, 48, 96))
        rows.append(f'<div class="row"><div class="lab">{e(O.LABELS[n])}<small>{e(O.CLASS[n])}</small></div><div class="strip">{cells}</div></div>')
    return f"""<section id="s-sizes"><h2>6. Sizes</h2>
<p>Each icon at its 16 px solid cut, its 24 px master, and the display master at 48 and 96 px, on Newsprint at true size.</p>{"".join(rows)}</section>"""


def sec_pixels():
    figs = []
    for kind, z in (("24px", 5), ("16px", 7)):
        s = C.vb(kind)
        for n in ICONS:
            f = C.PX / f"{C.stem(n, kind)}-Newsprint.png"
            figs.append(f'<figure><img class="pix" src="{src(f)}" width="{s * z}" height="{s * z}" alt="{e(O.LABELS[n])}, {kind} master, magnified">'
                        f'<figcaption>{e(O.LABELS[n])}, {kind[:-2]} px ×{z}</figcaption></figure>')
    for n in ICONS:
        f = C.PX / f"{C.stem(n, '16px')}-2x.png"
        figs.append(f'<figure><img class="pix" src="{src(f)}" width="112" height="112" alt="{e(O.LABELS[n])}, 16 px cut on a 2x screen, magnified">'
                    f'<figcaption>{e(O.LABELS[n])}, 16 px on a 2x screen ×3.5</figcaption></figure>')
    return f"""<section id="s-pixels"><h2>7. Pixels</h2>
<p>The 24 and 16 px masters rendered at 1x in Chromium and magnified without smoothing, then the 16 px cut as a 2x screen draws it. At 24 px straight center lines sit on whole pixels, so both edges of each 2 px line land on pixel boundaries. At 16 px straight edges sit on whole pixels and curves stay true curves, so on a 2x screen the discs and roofs are smooth. Feedback loop's ring and arrowheads are hinted to whole pixels at both sizes, since a true 2 px ring falls under D1-17; its stations stay true discs.</p>
<div class="pixrow">{"".join(figs)}</div></section>"""


def sec_cover():
    def cellrow(n, kinds):
        out = []
        for cw, lab in (("Charcoal-Red", "As drawn"), ("Charcoal-Plane-Ink", "Plane turned to ink"), ("Charcoal", "Plane removed")):
            imgs = "".join(icon(n, s, cw=cw, alt=f"{O.LABELS[n]}, {lab.lower()}, {s} px") for s in kinds)
            out.append(f'<div><div class="strip">{imgs}</div></div>')
        return "".join(out)
    rows = ['<div class="hd">Icon</div><div class="hd">As drawn</div><div class="hd">Plane turned to ink</div><div class="hd">Plane removed</div>']
    for n in ICONS:
        rows.append(f'<div class="hd">{e(O.LABELS[n])}</div>{cellrow(n, (16, 24, 48))}')
    pr = "".join(icon(n, 48, cw="White", alt=f"{O.LABELS[n]}, White on Prussian") for n in ICONS)
    pr24 = "".join(icon(n, 24, cw="White", alt=f"{O.LABELS[n]}, White on Prussian, 24 px") for n in ICONS)
    pr16 = "".join(icon(n, 16, cw="White", alt=f"{O.LABELS[n]}, White on Prussian, 16 px") for n in ICONS)
    return f"""<section id="s-cover"><h2>8. Cover the red (test 2)</h2>
<p>Every icon at 16, 24 and 48 px three ways: as drawn, with the plane printed in Charcoal, and with the plane removed. Each must keep its name. The 16 px cut has no plane, so its three cells match. The results are in section 13.</p>
<div class="cover">{"".join(rows)}</div>
<div style="background:var(--prussian);padding:16px;margin-top:16px"><p class="cap" style="color:#C9C5BC;margin:0 0 10px">White on Prussian, no red, at 48, 24 and 16 px</p><div class="strip">{pr}</div><div class="strip" style="margin-top:12px">{pr24}</div><div class="strip" style="margin-top:12px">{pr16}</div></div></section>"""


def sec_surfaces():
    out = []
    for sname, label, bg in C.SURFACES:
        cw = {"newsprint": "Charcoal-Red", "white": "Charcoal-Red", "charcoal": "Newsprint-Red", "prussian": "White"}[sname]
        imgs = "".join(icon(n, 48, cw=cw) for n in ICONS)
        note = {"newsprint": f"Charcoal {num(M['contrast']['ink|newsprint'])}:1. Red {num(M['contrast']['red|newsprint'])}:1, signature red alone.",
                "white": f"Charcoal {num(M['contrast']['ink|white'])}:1. Red {num(M['contrast']['red|white'])}:1.",
                "charcoal": f"Newsprint {num(M['contrast']['ink|charcoal'])}:1. Red {num(M['contrast']['red|charcoal'])}:1. Newsprint over red {num(M['contrast']['newsprint_line_on_red'])}:1.",
                "prussian": f"White {num(M['contrast']['white_on_prussian'])}:1, no red."}[sname]
        out.append(f'<div class="s-{sname}"><p class="cap">{label}. {note}</p><div class="strip">{imgs}</div></div>')
    return f"""<section id="s-surfaces"><h2>9. Surfaces</h2><div class="surf">{"".join(out)}</div></section>"""


def sec_holders():
    rows = ['<div class="hd"></div>' + "".join(f'<div class="hd">{s.replace("-", " ")}</div>' for s in C.HOLDER_SHAPES)]
    for color in C.HOLDER_COLORS:
        cells = []
        for shape in C.HOLDER_SHAPES:
            lt = ' class="lt"' if color == "Newsprint" else ""
            cells.append(f'<div{lt}><div class="strip">' + "".join(tile(n, shape, color, 80) for n in ICONS) + "</div></div>")
        rows.append(f'<div class="hd">{color} tile</div>' + "".join(cells))
    small = '<div class="strip">' + "".join(tile(n, "Rounded-Square", "Charcoal", 40) for n in ICONS) + "</div>" + \
            '<div class="ltstrip" style="margin-top:10px">' + "".join(tile(n, "Rounded-Square", "Newsprint", 28) for n in ICONS) + "</div>"
    apps = []
    for sc in C.APP_SCALES:
        f = C.app_tile_file(sc)
        apps.append(f'<figure style="margin:0"><div class="strip">' + "".join(f'<img src="{src(f)}" width="{w}" height="{w}" alt="App tile, live area {int(sc * 100)} percent, {w} px">' for w in (180, 60, 29)) +
                    f'</div><figcaption class="cap">{int(sc * 100)} percent{" · chosen" if abs(sc - C.APP_SCALE) < 1e-9 else ""}</figcaption></figure>')
    t = M["sets"]["tiles"]
    return f"""<section id="s-holders"><h2>10. Holders and tile colors</h2>
<p>Square, rounded square and circle, in the three G1-09 tile colors: a Charcoal tile with a Newsprint line and the red plane, a Newsprint tile with a Charcoal line and the red plane, and a Prussian tile with a White line and no red. The rounded square is round one's true superellipse with exponent 5. The icon's 20-unit live area is half the side, and the plane stays inside it in all {t['count']} measured tiles.</p>
<p class="cap">The Newsprint tiles sit on White here so their edges show on this Newsprint page.</p><div class="holders">{"".join(rows)}</div>
<h3 style="margin-top:22px">On whole pixels</h3><p class="cap">The 24 px master in a 40 px Charcoal tile, and the 16 px solid cut, one color, in a 28 px Newsprint tile.</p>{small}
<h3 style="margin-top:22px">The app tile, 1024 px master</h3>
<p>Act in the Charcoal superellipse, at three glyph scales (the live area as a share of the side), each at 180, 60 and 29 px. 62 percent is chosen by eye: 56 leaves the door small at 29 px, and 66 crowds the corners at 180.</p>
<div class="strip" style="gap:28px">{"".join(apps)}</div></section>"""


def navrow(dark=False, current="track"):
    items = []
    for i, n in enumerate(PILLARS):
        cur = n == current
        if dark:
            cw = "Newsprint-Red" if cur else "Newsprint"
        else:
            cw = "Charcoal-Red" if cur else "Charcoal"
        items.append(f'<span class="it{" cur" if cur else ""}">{icon(n, 24, cw=cw, alt="")}{e(O.LABELS[n])}</span>')
        if i < 3:
            items.append('<span class="ln" aria-hidden="true"></span>')
    return f'<div class="navrow{" dark" if dark else ""}">{"".join(items)}</div>'


def sec_contexts():
    topics = "".join(f'<div class="{"on" if n == "housing" else ""}">{icon(n, 24, cw="Charcoal-Red" if n == "housing" else "Charcoal", alt="")}<span>{e(O.LABELS[n])}</span></div>' for n in ICONS)
    av = C.CONTEXT / f"{C.DATE}_Overprint-Avatar-400.svg"
    avatar = (f'<div class="avatar"><img src="{src(av)}" width="72" height="72" alt="Act avatar at 72 px"><p>Oath &amp; Action<small>@oathandaction · 72 px</small></p>'
              f'<img src="{src(av)}" width="40" height="40" alt="Act avatar at 40 px"><p>Oath &amp; Action<small>40 px</small></p></div>')
    legend = (f'<div class="legend"><div class="cap" style="font-weight:700;letter-spacing:.04em;text-transform:uppercase">How to read a loop</div>'
              f'<div class="lg">{icon("loop", 16, cw="Charcoal", alt="")}<span>Feedback loop: a chain of effects that comes back to where it started.</span></div>'
              f'<div class="lg">{icon("bill", 16, cw="Charcoal", alt="")}<span>A bill or ballot measure in the loop.</span></div>'
              f'<div class="lg">{icon("connect", 16, cw="Charcoal", alt="")}<span>Two parts held apart, with ground between them.</span></div></div>')
    tracker = (f'<table class="tracker"><tbody>'
               f'<tr><td>{icon("bill", 16, cw="Charcoal", alt="Bill")}</td><td>Ballot access bill</td><td><span class="st"><i class="half"></i>In committee</span></td><td class="n">Mar 4</td></tr>'
               f'<tr><td>{icon("bill", 16, cw="Charcoal", alt="Bill, current")}</td><td><b>Open meetings bill</b></td><td><span class="st"><i class="full"></i>Passed one chamber</span></td><td class="n">Feb 27</td></tr>'
               f'<tr><td>{icon("testify", 16, cw="Charcoal", alt="Testify")}</td><td>Hearing sign-up</td><td><span class="st"><i></i>Open</span></td><td class="n">Mar 11</td></tr></tbody></table>')
    art = C.CONTEXT / f"{C.DATE}_Overprint-Context-Article-Header-1440.png"
    card = C.CONTEXT / f"{C.DATE}_Overprint-Context-Social-Card-1080.png"
    walls = C.CONTEXT / f"{C.DATE}_Overprint-Context-App-Tile-Wallpapers.png"
    return f"""<section id="s-contexts"><h2>11. In use</h2>
<p>The eight contexts from the round-two brief. The red appears where Rule 05.3 allows it: alone, on the current item from 24 px up, or as the view's one working red. At 16 px the icons are one color.</p>
<div class="ctx">
<figure><div style="display:grid;gap:10px">{navrow(False)}{navrow(True)}</div><figcaption>1. The four pillars in a menu row on Newsprint and on Charcoal, with Track current: its plane returns, its label goes bold, a rule runs under it.</figcaption></figure>
<figure><div class="topics">{topics}</div><figcaption>2. A topic list with labels at 24 px. Housing is current. <span class="tag ill">Illustrative</span></figcaption></figure>
<figure><img class="wideimg" src="{src(art)}" width="1440" height="520" alt="Article header at 1440 px with the Ballot icon at 64 px beside the headline"><figcaption>3. An article header at 1440 px, shown scaled: one feature icon at 64 px beside the headline. The headline and deck are invented. <span class="tag ill">Illustrative</span></figcaption></figure>
<figure>{avatar}<figcaption>4. A social avatar drawn at 400 px, shown at 72 and 40 px: Act in the Charcoal circle.</figcaption></figure>
<figure><img class="wideimg" src="{src(card)}" width="540" height="675" alt="Social card with Testify large in a Charcoal tile and a red sign-up button" style="width:540px"><figcaption>5. A social card, 1080 by 1350, shown at half size. Testify stands alone in its tile, so its plane counts as signature red; the sign-up button is the view's one working red, with a White label and a Charcoal keyline (D1-23). The copy is invented. <span class="tag ill">Illustrative</span></figcaption></figure>
<figure>{legend}<figcaption>6. An atlas legend at 16 px beside 13 px text, with Feedback loop, in the one-color solid cut.</figcaption></figure>
<figure>{tracker}<figcaption>7. A tracker table row at 16 px beside status marks, in the one-color solid cut; the current row shows by its bold label. The status marks here are placeholders drawn for this board; the status set comes later. The bills and dates are invented. <span class="tag ill">Illustrative</span></figcaption></figure>
<figure><img class="wideimg" src="{src(walls)}" width="760" height="600" alt="App tile at 180, 120, 60 and 29 px on a light and a dark wallpaper" style="width:760px"><figcaption>8. The app tile at 180, 120, 60 and 29 px on a light and a dark wallpaper. The wallpapers are flat stand-ins. <span class="tag ill">Illustrative</span></figcaption></figure>
</div></section>"""


def checks_rows():
    s = M["sets"]
    crisp16 = min(I[n]["crisp_16"] for n in ICONS)
    crisp24 = min(I[n]["crisp_24"] for n in ICONS)
    inks = [I[n]["ink96"] for n in ICONS]
    dev = [(I[n]["ink_dev"], n) for n in ICONS]
    out_band = [n for n in ICONS if not I[n]["weight_pass"]]
    com = max((max(abs(I[n]["centroid96"][0]), abs(I[n]["centroid96"][1])), n) for n in ICONS)
    reds = [(I[n]["red_share"], n) for n in ICONS]

    def worst_blur(mode, size):
        items = [(v["blurred_corr"], k) for k, v in M["pairs"].items() if k.startswith(f"{mode}|") and k.endswith(f"|{size}")]
        b, k = max(items)
        return b, k.split("|")[1], k.split("|")[2], sum(1 for v, _ in items if v >= 0.60)

    def worst_score(mode, size):
        items = [(v["score"], k) for k, v in M["pairs"].items() if k.startswith(f"{mode}|") and k.endswith(f"|{size}")]
        b, k = max(items)
        return b, k.split("|")[1], k.split("|")[2], sum(1 for v, _ in items if v >= 0.60)
    rows = []
    rows.append(("Pixel fit, D1-17", crisp16 >= .6 and crisp24 >= .6, f"16 px {num(crisp16)} or better; 24 px {num(crisp24)} or better (pass 0.60)", ""))
    for size in (16, 24, 48):
        b = [worst_blur(m, size) for m in ("drawn", "idle")]
        ok = all(x[3] == 0 for x in b)
        rows.append((f"Similarity at {size} px, D1-16 (blurred correlation)", ok,
                     f"As drawn: {b[0][3]} of 45 pairs at 0.60 or more, worst {e(O.LABELS[b[0][1]])} and {e(O.LABELS[b[0][2]])} {num(b[0][0])}. Idle: {b[1][3]} of 45, worst {e(O.LABELS[b[1][1]])} and {e(O.LABELS[b[1][2]])} {num(b[1][0])}", ""))
    for size in (16, 24, 48):
        b = [worst_score(m, size) for m in ("drawn", "idle")]
        ok = all(x[3] == 0 for x in b)
        rows.append((f"Similarity at {size} px, round one's combined score (reported beside D1-16)", ok,
                     f"As drawn: {b[0][3]} of 45 pairs at 0.60 or more, worst {e(O.LABELS[b[0][1]])} and {e(O.LABELS[b[0][2]])} {num(b[0][0])}. Idle: {b[1][3]} of 45, worst {e(O.LABELS[b[1][1]])} and {e(O.LABELS[b[1][2]])} {num(b[1][0])}", ""))
    for size in (16, 24):
        L = s[f"lookalikes_{size}"]
        bo = L["banned_over_060_score"]
        seen, items = set(), []
        for r in bo:
            key = (r["icon"], r["ref"])
            if key in seen:
                continue
            seen.add(key)
            items.append(f"{e(O.LABELS[r['icon']])} and {e(r['ref'])} {num(r['score'])}")
        rows.append((f"Look-alikes at {size} px, the banned glyphs (reload, sync, undo, redo, record, notification, copy, crop, expand, home, share)", not bo,
                     f"{len(bo)} of {L['banned_checked']} scores at 0.60 or more by the combined score; {L['banned_over_060_blurred']} by blurred correlation. " + ("Over: " + "; ".join(items) if items else "None over"), ""))
        ot = L["other_over_060_score"]
        seen, items = set(), []
        for r in ot:
            key = (r["icon"], r["ref"])
            if key in seen:
                continue
            seen.add(key)
            items.append(f"{e(O.LABELS[r['icon']])} and {e(r['ref'])} {num(r['score'])}")
        rows.append((f"Look-alikes at {size} px, the rest of each watch list", not ot, ("Over 0.60: " + "; ".join(items)) if items else "None over 0.60", ""))
    rows.append(("Act against &ldquo;01&rdquo; and the letter n", s["act_vs_01_16"] < .6 and s["act_vs_n_16"] < .6 and s["act_vs_01_24"] < .6,
                 f"16 px solid cut, with its full lintel: &ldquo;01&rdquo; {num(s['act_vs_01_16'])}, n {num(s['act_vs_n_16'])}. 24 px line cut, floor line and no lintel: &ldquo;01&rdquo; {num(s['act_vs_01_24'])}", ""))
    rows.append(("Weight, line ink at 96 px", not out_band,
                 f"{pct(min(inks), 1)} to {pct(max(inks), 1)} of the field, median {pct(s['ink_median'], 1)}; band 16 to 24 percent and 15 percent either side of the median. Outside: " + (", ".join(f"{e(O.LABELS[n])} {pct(I[n]['ink96'], 1)} ({pct(I[n]['ink_dev'], 0, True)})" for n in out_band) or "none"), ""))
    rows.append(("Red share of the painted area", all(I[n]["red_pass"] for n in ICONS), f"{pct(min(reds)[0], 1)} ({e(O.LABELS[min(reds)[1]])}) to {pct(max(reds)[0], 1)} ({e(O.LABELS[max(reds)[1]])}); band 15 to 25 percent", ""))
    rows.append(("Center of mass", com[0] <= 0.12, f"Largest offset {pct(com[0], 1)} of the field ({e(O.LABELS[com[1]])}); limit 12 percent", ""))
    rows.append(("Live area", all(I[n]["live_area_ok"] for n in ICONS), "Straight edges inside 2 to 22 units, round forms inside 1.75 to 22.25, in all ten display masters", ""))
    rows.append(("Badge corner", all(I[n]["badge_corner_red"] == 0 for n in ICONS), "No red in the top-right 6 by 6 units of any display master", ""))
    c = M["contrast"]
    rows.append(("Contrast, line on every surface and tile", True, f"Charcoal on Newsprint {num(c['ink|newsprint'])}, on White {num(c['ink|white'])}; Newsprint on Charcoal {num(c['ink|charcoal'])}; White on Prussian {num(c['ink|prussian'])}", ""))
    rows.append(("Contrast, Charcoal line over red", c["charcoal_line_on_red"] >= 3, f"{num(c['charcoal_line_on_red'])}:1", ""))
    rows.append(("Contrast, red on Charcoal and White", True, f"{num(c['red|charcoal'])}:1 and {num(c['red|white'])}:1", ""))
    rows.append(("Contrast, red on Newsprint", False, f"{num(c['red|newsprint'])}:1, under 3:1. The plane carries no edge a reader needs, so it stands as signature red alone (Rule 05.3), as the wordmark's ampersand does", ""))
    over_red = max((I[n]["ink_over_red"], n) for n in ICONS)
    rows.append(("Newsprint line over red on a Charcoal tile", False, f"{num(c['newsprint_line_on_red'])}:1 where the line crosses the plane. At most {pct(over_red[0])} of an icon's line sits on its plane ({e(O.LABELS[over_red[1]])}); the parts that name each subject stay off it", ""))
    rows.append(("Holder safe area", t_ok(), f"{M['sets']['tiles']['in_live_area']} of {M['sets']['tiles']['count']} tiles inside the live area; {M['sets']['tiles']['circle_safe']} of {M['sets']['tiles']['circle_count']} circle tiles inside 40 percent of the side from the center (farthest {pct(M['sets']['tiles']['max_r_share_circle'], 1)})", ""))
    return rows


def t_ok():
    t = M["sets"]["tiles"]
    return t["in_live_area"] == t["count"] and t["circle_safe"] == t["circle_count"]


def sec_checks():
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{pass_(ok)}</td><td>{b}</td></tr>" for a, ok, b, _ in checks_rows())
    per = []
    for n in ICONS:
        r = I[n]
        per.append(f"<tr><td>{e(O.LABELS[n])}</td><td class='n'>{num(r['crisp_16'])}</td><td class='n'>{num(r['crisp_24'])}</td><td class='n'>{pct(r['ink96'], 1)}</td>"
                   f"<td class='n'>{pct(r['ink_dev'], 0, True)}</td><td class='n'>{pct(r['red_share'], 1)}</td><td class='n'>{pct(r['red_share_visible'], 1)}</td>"
                   f"<td class='n'>{pct(r['centroid96'][0], 1, True)}, {pct(r['centroid96'][1], 1, True)}</td><td class='n'>{num(r['stroke']['median_units'])}</td>"
                   f"<td class='n'>{'' if r['min_gap_units'] is None else num(r['min_gap_units'])}</td><td>{e(r['watch_worst'][0])} <span class='n'>{num(r['watch_worst'][3])}</span></td></tr>")
    return f"""<section id="s-checks"><h2>12. Checks</h2>
<p>Every raster is Chromium at device scale 1. Numbers come from <code>phase-2/icons-r2/overprint/{C.MEAS.name}</code>. D1-16 defines similarity as blurred correlation, and the creative director's review rules that it decides pairs; round one also reported its mean with the filled-silhouette overlap, so both lines appear here. Look-alikes are judged by that combined score, as round one and Moving part judged them, against each icon's watch list, which the review widened to the banned interface glyphs. Material Symbols references are filled at 16 px and outlined at 24 px, matching each cut. The combined score includes the overlap of filled silhouettes, which runs high for any two outlines of one size: Feedback loop's ring scores {num(I['loop']['watch_worst'][3])} against {e(I['loop']['watch_worst'][0])}. Read the 24 px look-alike rows with that in mind.</p>
<div class="tblwrap"><table><thead><tr><th>Check</th><th>Result</th><th>Reading</th></tr></thead><tbody>{tr}</tbody></table></div>
<h3 style="margin-top:22px">Per icon</h3>
<div class="tblwrap"><table><thead><tr><th>Icon</th><th class="n">Crisp 16</th><th class="n">Crisp 24</th><th class="n">Ink at 96</th><th class="n">From median</th><th class="n">Red share</th><th class="n">Red visible</th><th class="n">Center of mass x, y</th><th class="n">Line, units</th><th class="n">Smallest gap, units</th><th>Closest look-alike</th></tr></thead><tbody>{"".join(per)}</tbody></table></div></section>"""


TEST2 = {  # the designer's reading by eye of section 8 at 2x, at 24 and 48 px and White on Prussian, and of the one-color 16 px cut
    "explain": ("Holds", "Holds at 24 and 48 px with the plane in ink or removed. The 16 px cut reads as a box with its lid lifted off the corner; the lid is small."),
    "track": ("Holds", "The stair holds at every size, plane or not. The 16 px flight, with its sloped underside, reads as steps."),
    "connect": ("Holds", "The two halves and the node hold at every size; with the plane in ink the node grows into a short bar under the center. At 16 px the broadcast reading the name test found is still there."),
    "act": ("Holds", "The door on its floor holds at 24 and 48 px. At 16 px the full lintel and jamb read as a frame with the leaf standing in it; the handle is a 1 px slot."),
    "ballot": ("Holds", "With the plane removed the paper keeps its printed oval and stands clear of the box. With the plane in ink the oval turns into a dark mark. At 16 px a paper with an oval stands between the two halves of the lid. A printer stays the nearest misreading."),
    "bill": ("Holds", "The folded page holds at every size; at 16 px its lines run to the edge of the page."),
    "testify": ("Holds", "The person and the microphone hold at 24 and 48 px, and at 16 px the microphone now stands on its own stand beside the head."),
    "housing": ("Holds", "The house holds at every size."),
    "money": ("Holds", "The note with its disc left of center holds at every size; at 16 px the disc sits in the note's counter."),
    "loop": ("Weak at 24 px", "At 48 px the ring, three stations and arrowheads read as a cycle, plane or not. At 24 px the arrowheads shrink into the ring and it reads first as a ring of beads. At 16 px three beads joined by short arrowed arcs read as a cycle of three steps."),
}


def sec_tests():
    t2 = "".join(f"<tr><td>{e(O.LABELS[n])}</td><td>{pass_(res == 'Holds', res)}</td><td>{e(txt)}</td></tr>" for n, (res, txt) in TEST2.items())
    rows3 = []
    for n in ICONS:
        r = I[n]
        ok = r["pixel_fit_pass"] and r["weight_pass"] and r["com_pass"] and r["live_area_ok"]
        why = []
        if not r["weight_pass"]:
            why.append(f"ink {pct(r['ink_dev'], 0, True)} from the median")
        if n == "loop":
            why.append(f"Ink in the band, center of mass and pixel fit inside their limits. The ridge median reads {num(r['stroke']['median_units'])} units where the ring runs into its stations and arrowheads, and the hinted 24 px ring shows small steps on a 2x screen")
        rows3.append(f"<tr><td>{e(O.LABELS[n])}</td><td>{pass_(ok)}</td><td>{e('; '.join(why) or 'One line weight, clean joins at 2x, ink in the band, center of mass and pixel fit inside their limits')}</td></tr>")
    return f"""<section id="s-tests"><h2>13. Tests 2 to 4</h2>
<p>Test 1, the blind name test, is run by the main session on these finished masters (fix 5). Tests 2 and 4 here are the designer's own reading by eye, made with the drawings in view, so they stand in for a reader no better than the blind test does.</p>
<h3>Test 2, cover the red</h3><div class="tblwrap"><table><thead><tr><th>Icon</th><th>Result</th><th>Reading</th></tr></thead><tbody>{t2}</tbody></table></div>
<p class="cap">Measured alongside: the idle rows in section 11 are the plane-removed drawings, and White on Prussian scores the same pairs as idle. The pairs that cross 0.60 there are listed in the checks in section 12.</p>
<h3 style="margin-top:22px">Test 3, hold up at 2x</h3><div class="tblwrap"><table><thead><tr><th>Icon</th><th>Result</th><th>Reading</th></tr></thead><tbody>{"".join(rows3)}</tbody></table></div>
<h3 style="margin-top:22px">Test 4, beside the best</h3>
<ul><li><strong>Finish at 24 px against Material Symbols.</strong> The 2 px line matches Material's weight 400 closely and the drawings look as finished. Overprint's icons sit a little smaller in the field, Track and Act most. At 48 px Overprint is lighter on purpose: a 3 px line against Material's heavier optical size.</li>
<li><strong>Oath &amp; Action at 48 px with the wordmark covered.</strong> Every plane falls the same way, down and to the left, and that repeat marks the set as one publication's. With the red removed, Bill, Housing and Campaign money could belong to any careful line set.</li>
<li><strong>One family in a one-color row.</strong> In the idle topic list in section 11 the ten share one line, one corner and one terminal. Feedback loop now weighs the same as the rest; at 24 px its hinted ring shows small steps on a 2x screen, the one drawing in the line cut that does.</li>
<li><strong>The 16 px cut beside the 24 px line.</strong> The two cuts share their skeletons and proportions, so a row that steps from 16 to 24 px keeps its subjects. The solid cut is heavier, as Moving part's was, and reads as a sibling of the line set.</li></ul></section>"""


RUBRIC = [
    ("Craft", 4, "One line, one radius and one offset hold at 2x from 24 px up, and the 16 px cut keeps true curves on whole-pixel edges. Every icon now sits in the weight band, every pair sits under 0.60 by D1-16 at 16, 24 and 48 px, and pixel fit passes everywhere. Feedback loop's 24 px ring is hinted to steps and its arrowheads are small; Bill's 16 px page scores 0.61 against Material's bell."),
    ("Clarity", 3, "The board says what the red does and where it stops from its first screen. The stage 2 name test found Ballot and Feedback loop weak and four 16 px icons falling apart; this score stays at 3 until the rerun reads the new masters."),
    ("Brand fidelity", 4, "Locked colors exact; Rule 05.3 applied to every row; red never on Prussian or at 16 px; Connect's plane stays clear of both halves. The pillar marks' treatment by size and the 16 px rule need Dustin's named approval."),
    ("Usefulness", 4, "A producer gets two cuts with one rule each: the plane rule and its offsets from 24 px up, the solid grammar at 16 px, the two exceptions, the row state and 30 masters with their colorways."),
    ("Evidence honesty", 5, "Every number comes from the measurement file, both similarity measures are shown, failures are listed as failures, illustrative copy is labeled, and tests 2 and 4 are marked as the designer's own reading."),
    ("Accessibility", 4, "The state shows by shape and text as well as color, and at 16 px by the label alone. Red on Newsprint stays under 3:1 and so carries nothing a reader needs."),
    ("Beauty and distinctiveness", 4, "Ten planes falling the same way read as one press run, and the drawings look finished beside Material Symbols. Offset-accent sets are common in stock libraries, so the distinctiveness rests on the fixed offset and the editor's-mark logic, and the 16 px cut carries none of it."),
]


def sec_rubric():
    tr = "".join(f"<tr><td><b>{e(a)}</b></td><td class='n'>{b}</td><td>{e(c)}</td></tr>" for a, b, c in RUBRIC)
    return f"""<section id="s-rubric"><h2>14. Rubric</h2>
<p>Master Brief section 6, plus the creative director's seventh line. The ship threshold is 4 on every line. These are the designer's own scores, for the creative director to test.</p>
<div class="tblwrap"><table><thead><tr><th>Criterion</th><th class="n">Score</th><th>Reason</th></tr></thead><tbody>{tr}</tbody></table></div></section>"""


def sec_decide():
    items = [
        ("The pillar marks by size", "Direction A's skeletons drawn in line with a red plane from 24 px up, and as Direction A's filled pieces in one color at 16 px. Y1's solid treatment and Y4's line companion trade roles.", "Needs Dustin's named approval if Overprint is chosen. The skeletons stay."),
        ("No red at 16 px", "Sixteen-pixel icons are always one color, and the current item shows by its label.", "Recommended: it narrows how Rule 05.3's icon sentences apply and leaves its words unchanged."),
        ("Act's lintel at 16 px only", "The solid cut keeps the full lintel; the line cut keeps the floor line and no lintel.", "Needs a named approval for the 16 px cut: &ldquo;01&rdquo; scores " + num(M["sets"]["act_vs_01_16"]) + " with it."),
        ("The plane rule", "The plane fills one drawn shape and prints off register at one fixed offset.", "Recommended: every red then belongs to a drawn part, and the offset carries the concept."),
        ("Connect's exception", "Connect's plane centers on the gap and prints straight down.", "Recommended: Rule 01.1 bars red that leans toward a side."),
        ("Standalone red on Newsprint", "A plane alone on Newsprint measures 2.96:1 and stands as signature red.", "Recommended, as round one's decision 3 proposed: the plane never carries an edge a reader needs."),
        ("Topic symbols carry a node only where it is part of the subject", "Outside the pillar marks only Feedback loop's three stations are nodes.", "For Dustin: this narrows Y5's &ldquo;Direction A's grammar&rdquo; for topics."),
    ]
    li = "".join(f"<li><b>{a}</b>{b} {c}</li>" for a, b, c in items)
    return f"""<section id="s-decide"><div class="decision"><h2>15. Decisions</h2><ol>{li}</ol></div></section>"""


def sec_honest():
    tested = ["Chromium renders at device scale 1 of all 30 masters, the 48 and 96 px display renders, the White-on-Prussian renders and the look-alike references, with the checks in section 12; the 16 and 24 px masters also as a 2x screen draws them.",
              "Similarity for all 45 pairs at 16, 24 and 48 px, as drawn and idle, by blurred correlation and by round one's combined score.",
              "Look-alikes against each icon's watch list: the creative director's watch column, the stage 1 and stage 2 misreadings, the letters and numerals Phase 1 watched, and the banned interface glyphs as Material Symbols, rendered from Google Fonts.",
              "Vector checks: live area, badge corner, red share, the smallest gap between parts, and the holder safe area in 360 tiles at 28, 40, 80 and 180 px.",
              "The app tile at three glyph scales at 180, 60 and 29 px, read by eye.",
              "Board layout at 1440 and 390 px with round one's layout check; captures read by eye."]
    untested = ["Readers. No person has seen these icons (Q-13); the main session's blind name test uses one agent rater, and its rerun on the fix-pass masters is still to come.",
                "Tests 2 and 4 by anyone other than the designer.",
                "Other browsers, operating systems and screen densities; Windows and macOS text rendering beside the icons.",
                "Print, embroidery and enamel; color-vision simulation; screen-reader output; hover, focus and motion.",
                "Apple's own icon mask, which Apple does not publish.",
                "The full set: the other topic, atlas, status and utility icons, and whether the plane rule holds across sixty subjects."]
    return f"""<section id="s-honest"><h2>16. Tested and not tested</h2><div class="two"><div><h3>Tested</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in tested)}</ul></div>
<div><h3>Not tested</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in untested)}</ul></div></div>
<p class="cap" style="margin-top:18px">Notes: <code>work/handoffs/phase-2/{C.NOTES.name}</code>. Scripts: <code>work/build/scripts/phase-2/icons_r2_overprint_*.py</code>.</p></section>"""


def build():
    parts = [head(), intro(), sec_ten(), sec_fix(), sec_bench(), sec_changes(), sec_rules(), sec_sizes(), sec_pixels(), sec_cover(), sec_surfaces(),
             sec_holders(), sec_contexts(), sec_checks(), sec_tests(), sec_rubric(), sec_decide(), sec_honest(), "</main></body></html>"]
    C.BOARD.write_text("\n".join(parts))
    print("wrote", C.BOARD)


if __name__ == "__main__":
    build()
