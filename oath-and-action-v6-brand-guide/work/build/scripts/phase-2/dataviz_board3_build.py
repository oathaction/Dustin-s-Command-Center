"""Build Board 3 of the data visualization round (November 6, 2026): three chart systems side by side for Dustin's pick.

Usage:
    python3 -I work/build/scripts/phase-2/dataviz_board3_build.py

Reads the creative director's board content (board-3/20261106_Board-3-Content.json), the published page links
(board-3/20261106_Published-Pages.json, optional), and the captures written by dataviz_board3_capture.js, and writes:
    work/boards/20261106_Data-Viz-Systems-Board.html            (the studio record, a full document)
    <scratchpad>/publish/20261106_Data-Viz-Systems-Board.html  (the publish copy for the private page)
"""
import base64
import html
import io
import json
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[4]
DV = ROOT / 'work/boards/phase-2/data-viz'
B3 = DV / 'board-3'
CAP = B3 / 'captures'
OUT = ROOT / 'work/boards/20261106_Data-Viz-Systems-Board.html'
PUB = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/bce9c31a-68c6-5654-913f-e031125afc9e/scratchpad/publish/20261106_Data-Viz-Systems-Board.html')
C = json.loads((B3 / '20261106_Board-3-Content.json').read_text())
PP = B3 / '20261106_Published-Pages.json'
PAGES = json.loads(PP.read_text()) if PP.exists() else {}
NAME = {'01': 'Explainer', '02': 'Register', '03': 'Instrument'}
ORDER = ['01', '02', '03']
E = lambda s: html.escape(str(s), quote=True)
RUBRIC = ['Craft', 'Clarity', 'Brand', 'Usefulness', 'Evidence', 'Access', 'Beauty']
LENSES = [('statistics', 'Statistics'), ('civic', 'Teaches'), ('interface', 'Works'), ('brand', 'Brand, both sides'),
          ('craft', 'Craft at 2x'), ('production', 'Builds')]


def img(n, part, alt, out_w=1100, q=74, crop_h=None):
    p = CAP / f'{n}-{NAME[n]}-{part}.jpg'
    im = Image.open(p).convert('RGB')
    if crop_h and im.height > crop_h:
        im = im.crop((0, 0, im.width, crop_h))
    if im.width > out_w:
        im = im.resize((out_w, round(im.height * out_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return (f'<img src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}" width="{im.width}" '
            f'height="{im.height}" alt="{E(alt)}" loading="lazy">')


CSS = '''
/* Board 3: one 1280 px reading column on Newsprint, the work first, a Prussian decision band. */
:root{color-scheme:light;--bg:#DCD9D2;--surface:#E6E3DD;--white:#FFFFFF;--fg:#121212;--muted:#45494F;--rule:#5D636D;
--prussian:#1F2D5A;--newsprint:#DCD9D2;--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;
--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1rem/1.6 var(--body)}
a{color:inherit;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.board{max-width:1280px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--fg);padding-bottom:14px;flex-wrap:wrap}
.mast b{font:800 1.25rem/1 var(--display);letter-spacing:-.02em}.mast span{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.eyebrow{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:28px 0 0}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.025em;text-wrap:balance;margin:0}
h1{font-size:clamp(2.25rem,6vw,4.25rem);line-height:1.02;margin-top:10px;max-width:18ch}
h2{font-size:clamp(1.5rem,3vw,2.25rem);line-height:1.08;margin:0 0 12px}
h3{font-size:1.25rem;line-height:1.2;letter-spacing:-.015em}
h4{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px}
p{margin:0 0 12px;max-width:72ch}.deck{font-size:1.1875rem;line-height:1.5;max-width:64ch;margin-top:16px}
section{border-top:1px solid var(--rule);margin-top:48px;padding-top:32px}
.secnum{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.ask{background:var(--white);border:1px solid var(--rule);padding:22px 24px;margin-top:28px}
.ask ol{margin:0;padding-left:1.3em}.ask li{margin:0 0 8px;max-width:84ch}.reply{font:italic 400 1.0625rem/1.5 var(--quote);margin:10px 0 0}
.toc{display:flex;flex-wrap:wrap;gap:6px 22px;margin:22px 0 0;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}.toc a:hover{text-decoration:underline}
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--white)}
table{border-collapse:collapse;width:100%;font-size:.9375rem;min-width:860px;font-variant-numeric:tabular-nums}
th,td{text-align:left;vertical-align:top;padding:10px 7px;border-bottom:1px solid #C9C6BF}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.02em;text-transform:uppercase;color:var(--muted);background:var(--surface)}
td.n{text-align:center}tr.pick td,tr.pick th{background:#F1F0EC}th.grp{border-left:2px solid var(--rule)}td.grp{border-left:2px solid var(--rule)}
.sys{margin-top:40px;border-top:2px solid var(--fg);padding-top:20px}
.sys-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap}
.chip{display:inline-block;font:600 .8125rem/1.3 var(--body);border:1px solid var(--fg);padding:2px 7px;margin:0 6px 6px 0}
.chip.solid{background:var(--fg);color:var(--white)}
.open{font:700 1rem/1.3 var(--body);display:inline-flex;align-items:center;min-height:44px}
.two{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:28px;align-items:start;margin-top:14px}
.shot{margin:0}.shot img{width:100%;height:auto;display:block;border:1px solid var(--rule);background:var(--white)}
figcaption{font-size:.875rem;line-height:1.45;color:var(--muted);margin-top:6px}
.trio{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:16px;align-items:start}
.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px;align-items:start}
.phone{max-width:260px}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:70ch}
.decision{background:var(--prussian);color:var(--newsprint);padding:28px max(20px,3vw);margin-top:48px}
.decision *{color:inherit}.decision h2{color:#FFFFFF}.decision ol{padding-left:1.3em;margin:0}.decision li{margin:0 0 16px;max-width:88ch}
.decision .rec{display:block;margin-top:4px;font-weight:700}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:28px}
.small{font-size:.875rem;color:var(--muted)}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
@media (max-width:900px){.two,.trio,.pair{grid-template-columns:1fr}.phone{max-width:300px}}
'''


def scores_table():
    rows = []
    for n in ORDER:
        s = C['concepts'][n]
        cls = ' class="pick"' if n == C['pick'] else ''
        cd = ''.join(f'<td class="n{" grp" if i == 0 else ""}">{v}</td>' for i, v in enumerate(s['cd_scores']))
        rt = ''.join(f'<td class="n{" grp" if i == 0 else ""}">{s["red_team"].get(k, "")}</td>' for i, (k, _) in enumerate(LENSES))
        rows.append(f'<tr{cls}><th scope="row">{n} {E(s["name"])}</th>{cd}{rt}<td class="n grp">{s["readers_first"]} of 6</td></tr>')
    h1 = ''.join(f'<th scope="col"{" class=\"grp\"" if i == 0 else ""}>{h}</th>' for i, h in enumerate(RUBRIC))
    h2 = ''.join(f'<th scope="col"{" class=\"grp\"" if i == 0 else ""}>{h}</th>' for i, (_, h) in enumerate(LENSES))
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Scores for the three chart systems"><table>'
            f'<caption class="small" style="caption-side:bottom;text-align:left;padding:8px 12px">Left: the creative director after the fix pass, 1 to 5, ship line 4 on every line. '
            f'Middle: the six red team lenses before the fix pass. Right: first places among six simulated readers.</caption>'
            f'<thead><tr><th scope="col">System</th>{h1}{h2}<th scope="col" class="grp">Readers first</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def side_by_side(spec, label, caption):
    figs = ''.join(f'<figure class="shot">{img(n, f"white-{spec}", f"{NAME[n]}, chart {spec} on White", 760)}'
                   f'<figcaption>{n} {E(NAME[n])}</figcaption></figure>' for n in ORDER)
    return f'<h3 style="margin-top:28px">{E(label)}</h3><p>{E(caption)}</p><div class="trio">{figs}</div>'


def concept_band(n):
    s = C['concepts'][n]
    tag = '<span class="chip solid">Studio pick</span>' if n == C['pick'] else ('<span class="chip">Runner-up</span>' if n == C.get('runner_up') else '')
    link = f'<a class="open" href="{E(PAGES[n]["url"])}">Open the live page</a>' if n in PAGES else ''
    best = ''.join(f'<li>{E(x)}</li>' for x in s['best'])
    holds = ''.join(f'<li>{E(x)}</li>' for x in s['holds_back'])
    return f'''<article class="sys" id="c{n}" aria-labelledby="h{n}">
<div class="sys-head"><div><p class="secnum">CHART SYSTEM {n}</p><h2 id="h{n}">{E(s["name"])}</h2></div><div>{tag}{link}</div></div>
<p class="deck">{E(s["idea"])}</p>
<p><b>Pick this if</b> {E(s["pick_if"])}</p>
<div class="two"><figure class="shot">{img(n, "white-first-screen", f"{s['name']}, the White view's first screen at 1440 by 900")}<figcaption>The first screen of the White view at 1440 by 900.</figcaption></figure>
<div><h4>At its best</h4><ul class="facts">{best}</ul><h4>What still holds it back</h4><ul class="facts">{holds}</ul>
<figure class="shot phone">{img(n, "white-390-screen-1", f"{s['name']}, the first phone screen at 390 px", 390)}<figcaption>The first phone screen at 390 px.</figcaption></figure></div></div>
<div class="trio">
<figure class="shot">{img(n, "white-S01", "Chart S01, big number in context", 760)}<figcaption>S01, big number in context.</figcaption></figure>
<figure class="shot">{img(n, "white-S03", "Chart S03, ranked bar", 760, crop_h=1500)}<figcaption>S03, ranked bar (top of the figure).</figcaption></figure>
<figure class="shot">{img(n, "white-S10", "Chart S10, evidence mix", 760, crop_h=1500)}<figcaption>S10, evidence mix (top of the figure).</figcaption></figure>
</div>
<div class="pair">
<figure class="shot">{img(n, "dark-first-screen", f"{s['name']}, the Charcoal view's first screen", 760)}<figcaption>The Charcoal view, the dark palette.</figcaption></figure>
<figure class="shot">{img(n, "social-card", f"{s['name']}, the social card at 1080 by 1350", 620)}<figcaption>The social card, 1080 by 1350.</figcaption></figure>
</div></article>'''


def ground_section():
    n = C['pick']
    g = C['ground']
    return f'''<section id="ground" aria-labelledby="h-ground"><p class="secnum">PAGE COLOR</p><h2 id="h-ground">White or Newsprint, for charts and the atlas together</h2>
<p class="deck">{E(g["text"])} The studio recommends {E(g["rec"])}.</p>
<div class="pair"><figure class="shot">{img(n, "white-S02", "Chart S02 on White", 760)}<figcaption>{E(NAME[n])}, S02 on White.</figcaption></figure>
<figure class="shot">{img(n, "newsprint-S02", "Chart S02 on Newsprint", 760)}<figcaption>{E(NAME[n])}, S02 on Newsprint.</figcaption></figure></div></section>'''


def diverging_section():
    d = C['diverging']
    figs = ''.join(f'<figure class="shot">{img(n, "white-S06", f"{NAME[n]}, chart S06 on White", 760, crop_h=1300)}<figcaption>{n} {E(NAME[n])}, S06 (top of the figure).</figcaption></figure>' for n in ORDER)
    return f'''<section id="diverging" aria-labelledby="h-div"><p class="secnum">DIVERGING PAIR</p><h2 id="h-div">Up and down without red and blue</h2>
<p class="deck">{E(d["text"])} The studio recommends {E(d["rec"])}.</p><div class="trio">{figs}</div></section>'''


def build():
    bands = ''.join(concept_band(n) for n in ORDER)
    finishing = ''.join(f'<li>{E(x)}</li>' for x in C['finishing'])
    decisions = ''.join(f'<li><b>{E(d["q"])}</b> {E(d["text"])}<span class="rec">Recommended: {E(d["rec"])}</span></li>' for d in C['decisions'])
    risks = ''.join(f'<li>{E(x)}</li>' for x in C.get('risks', []))
    L = lambda k: ''.join(f'<li>{x}</li>' for x in C.get(k, []))
    pick = C['concepts'][C['pick']]['name']
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>Chart Systems Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="board" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Brand Guide, Edition 06 · Phase 2 · Data visualization</span></div>
<p class="eyebrow">Board 3 · November 6, 2026</p>
<h1>Three chart systems for Oath &amp; Action</h1>
<p class="deck">{E(C["deck"])}</p>
<div class="ask"><h3>What you are asked</h3><ol>
<li><b>Pick one chart system</b> to finish as chapter 14 and the chart kit. The studio recommends {E(pick)}.</li>
<li><b>Choose the page color</b> for charts and the atlas, and the diverging pair.</li>
<li><b>Answer the other calls</b> in the decisions band. Each has a recommendation.</li></ol>
<p class="reply">{E(C.get("sample_reply", "Pick: " + pick + ". Decisions: as recommended."))}</p></div>
<nav class="toc" aria-label="On this board"><a href="#scores">Scores</a><a href="#same">Same chart, three systems</a>{"".join(f'<a href="#c{n}">{n} {E(NAME[n])}</a>' for n in ORDER)}<a href="#ground">Page color</a><a href="#diverging">Diverging pair</a><a href="#rec">Recommendation</a><a href="#decisions">Decisions</a><a href="#checks">Checks</a></nav>
</header>
<section id="scores" aria-labelledby="h-scores"><p class="secnum">SCORES</p><h2 id="h-scores">How the three compare</h2>
{scores_table()}
<p class="small" style="margin-top:12px">The six readers were simulated by one model. No real reader has seen these charts (DR-51).</p></section>
<section id="same" aria-labelledby="h-same"><p class="secnum">LIKE FOR LIKE</p><h2 id="h-same">The same chart in each system</h2>
<p>Every system drew the same ten charts from the same data. Two of them side by side show how the systems differ.</p>
{side_by_side("S02", "S02, child poverty, 2009 to 2025", "A line with event notes, from the Census Bureau's current table.")}
{side_by_side("S08", "S08, the repair log's 64 rule changes", "A unit chart, one mark per entry, with the atlas's coding rule and the editor's disclosure.")}
</section>
{bands}
{ground_section()}
{diverging_section()}
<section id="rec" aria-labelledby="h-rec"><p class="secnum">RECOMMENDATION</p><h2 id="h-rec">The studio recommends {E(pick)}</h2>
<p class="deck">{E(C["rec_text"])}</p><p><b>Runner-up: {E(C["concepts"][C["runner_up"]]["name"])}.</b> {E(C["runner_text"])}</p>
<h4>Finishing work if you pick {E(pick)}</h4><ol>{finishing}</ol>
<h4>Risks to weigh</h4><ul class="facts">{risks}</ul></section>
<div class="decision" id="decisions" role="region" aria-labelledby="h-dec"><h2 id="h-dec">Decisions</h2><ol>{decisions}</ol></div>
<section id="process" aria-labelledby="h-proc"><p class="secnum">HOW THIS WAS MADE</p><h2 id="h-proc">Three makers, six reviewers, a reader panel, one fix pass</h2><ol>{L("process")}</ol>
<h4>What the round found in the atlas data</h4><ul class="facts">{L("v7_findings")}</ul></section>
<section id="checks" aria-labelledby="h-checks"><p class="secnum">CHECKS</p><h2 id="h-checks">What was tested</h2>
<div class="cols"><div><h4>Tested</h4><ul class="facts">{L("tested")}</ul></div><div><h4>Not tested</h4><ul class="facts">{L("not_tested")}</ul></div></div></section>
<section id="changes" aria-labelledby="h-ch"><p class="secnum">CHANGE LOG</p><h2 id="h-ch">Files</h2>
<p class="small">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>. Nothing in <code>source/</code>, the Civic Line icons, the identity masters or the atlas pick changed.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts">{L("changelog_created")}</ul></div><div><h4>Modified</h4><ul class="facts">{L("changelog_modified")}</ul></div></div></section>
<p class="small" style="margin-top:40px">Data: Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026; U.S. Census Bureau tables retrieved November 6, 2026; Ballotpedia (secondary), retrieved November 6, 2026. Chart titles on the three pages are studio drafts.</p>
</main></body></html>'''
    OUT.write_text(page)
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace('<title>Chart Systems Board</title>\n', '')
    PUB.parent.mkdir(parents=True, exist_ok=True)
    PUB.write_text('<title>Chart Systems Board</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + re.sub(r'</body>\s*</html>\s*$', '', body))
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1e6:.1f} MB', 'and', PUB)


if __name__ == '__main__':
    build()
