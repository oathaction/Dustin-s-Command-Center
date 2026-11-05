"""Build Board 2 of the editorial atlas round (November 5, 2026): the five systems side by side for Dustin's pick.

Usage:
    python3 -I work/build/scripts/phase-2/atlas_board2_build.py

Reads each system's captures, the published page links (board-2/20261105_Published-Pages.json), the review
content (board-2/20261105_Board-2-Content.json, written from the creative director's review and the four red
team reports), and writes:
    work/boards/20261105_Atlas-Editorial-Systems-Board.html   (the studio record, a full document)
    <scratchpad>/publish/20261105_Atlas-Editorial-Systems-Board.html   (the publish copy for the private page)
"""
import base64
import html
import io
import json
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[4]
ED = ROOT / 'work/boards/phase-2/atlas-editorial'
B2 = ED / 'board-2'
OUT = ROOT / 'work/boards/20261105_Atlas-Editorial-Systems-Board.html'
PUB = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/116edc6c-f1d0-50f6-9263-c43fde110995/scratchpad/publish/20261105_Atlas-Editorial-Systems-Board.html')
PAGES = json.loads((B2 / '20261105_Published-Pages.json').read_text())
C = json.loads((B2 / '20261105_Board-2-Content.json').read_text())
SLUG = {'01': '01-times-explainer', '02': '02-economist-register', '03': '03-reference-sheets',
        '04': '04-night-edition', '05': '05-architecture'}
STEM = {'01': 'Times-Explainer', '02': 'Economist-Register', '03': 'Reference-Sheets', '04': 'Night-Edition',
        '05': 'Architecture'}
E = lambda s: html.escape(str(s), quote=True)
RUBRIC = ['Craft', 'Clarity', 'Brand fidelity', 'Usefulness', 'Evidence honesty', 'Accessibility', 'Beauty']


def cap(n, view, width=1440, crop_h=None, out_w=1100, q=78):
    p = ED / SLUG[n] / 'captures' / f'20261105_Editorial-{n}-{STEM[n]}-{view}-{width}.jpg'
    im = Image.open(p).convert('RGB')
    if crop_h:
        im = im.crop((0, 0, im.width, min(im.height, crop_h)))
    if im.width > out_w:
        im = im.resize((out_w, round(im.height * out_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    alt = f"{PAGES[n]['name']}, {view.replace('-', ' ')} at {width} px"
    return f'<img src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}" width="{im.width}" height="{im.height}" alt="{E(alt)}">'


CSS = '''
/* Layout: one 1280 px reading column; one band per system; a Prussian decision band. Single light theme by
   choice: the board shows the brand on its Newsprint ground. */
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
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none}.toc a:hover{text-decoration:underline}
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--white)}
table{border-collapse:collapse;width:100%;font-size:.9375rem;min-width:760px;font-variant-numeric:tabular-nums}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #C9C6BF}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.05em;text-transform:uppercase;color:var(--muted);background:var(--surface)}
td.n{text-align:center}tr.pick td,tr.pick th{background:#F1F0EC}
.sys{margin-top:40px;border-top:2px solid var(--fg);padding-top:20px}
.sys-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap}
.chip{display:inline-block;font:600 .8125rem/1.3 var(--body);border:1px solid var(--fg);padding:2px 7px;margin:0 6px 6px 0}
.chip.solid{background:var(--fg);color:var(--white)}
.open{font:700 1rem/1.3 var(--body)}
.two{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:28px;align-items:start;margin-top:14px}
.shot{margin:0}.shot img{width:100%;height:auto;display:block;border:1px solid var(--rule);background:var(--white)}
figcaption{font-size:.875rem;line-height:1.45;color:var(--muted);margin-top:6px}
.trio{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:16px}
.phone{max-width:240px}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:70ch}
.quote{border-left:3px solid var(--fg);padding:2px 0 2px 16px;margin:12px 0}
.decision{background:var(--prussian);color:var(--newsprint);padding:28px max(20px,3vw);margin-top:48px}
.decision *{color:inherit}.decision h2{color:#FFFFFF}.decision ol{padding-left:1.3em;margin:0}.decision li{margin:0 0 16px;max-width:88ch}
.decision .rec{display:block;margin-top:4px;font-weight:700}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:28px}
.small{font-size:.875rem;color:var(--muted)}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
@media (max-width:900px){.two{grid-template-columns:1fr}.trio{grid-template-columns:1fr}.phone{max-width:300px}}
'''


def scores_table():
    rows = []
    for n in ['01', '02', '03', '04', '05']:
        s = C['systems'][n]
        cd = s['cd_scores']
        cls = ' class="pick"' if n == C['pick'] else ''
        cells = ''.join(f'<td class="n">{v}</td>' for v in cd)
        rt = s['red_team']
        rows.append(f'<tr{cls}><th scope="row">{n} {E(PAGES[n]["name"])}</th>{cells}<td class="n">{rt["civic"]}</td><td class="n">{rt["interface"]}</td><td class="n">{rt["evidence"]}</td><td class="n">{rt["readers"]}</td></tr>')
    head = ''.join(f'<th scope="col">{h}</th>' for h in RUBRIC)
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Scores for the five systems"><table><thead><tr><th scope="col">System</th>{head}'
            '<th scope="col">Teaches</th><th scope="col">Works</th><th scope="col">True and on brand</th><th scope="col">Readers right</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def system_band(n):
    s = C['systems'][n]
    pg = PAGES[n]
    tag = '<span class="chip solid">Studio pick</span>' if n == C['pick'] else ('<span class="chip">Runner-up</span>' if n == C['runner_up'] else '')
    best = ''.join(f'<li>{E(x)}</li>' for x in s['best'])
    holds = ''.join(f'<li>{E(x)}</li>' for x in s['holds_back'])
    return f'''<article class="sys" id="s{n}" aria-labelledby="h{n}">
<div class="sys-head"><div><p class="secnum">SYSTEM {n} · {E(pg["ground"]).upper()}</p><h2 id="h{n}">{E(pg["name"])}</h2></div>
<div>{tag}<a class="open" href="{E(pg["url"])}">Open the live page</a></div></div>
<p class="deck">{E(s["idea"])}</p>
<p><b>Pick this if</b> {E(s["pick_if"])}</p>
<div class="two"><figure class="shot">{cap(n, "overview", 1440, 900)}<figcaption>The first screen of the overview at 1440 by 900.</figcaption></figure>
<div><h4>At its best</h4><ul class="facts">{best}</ul><h4>What still holds it back</h4><ul class="facts">{holds}</ul>
<figure class="shot phone">{cap(n, "overview", 390, 844 * 2, 390)}<figcaption>The first two phone screens at 390 px.</figcaption></figure></div></div>
<div class="trio">
<figure class="shot">{cap(n, "loop-r10", 1440, 1100, 760)}<figcaption>Loop R10, the safe-seat loop.</figcaption></figure>
<figure class="shot">{cap(n, "area-c", 1440, 1100, 760)}<figcaption>Elections, the area page.</figcaption></figure>
<figure class="shot">{cap(n, "loops", 1440, 1100, 760)}<figcaption>The loop catalog.</figcaption></figure>
</div></article>'''


def build():
    bands = ''.join(system_band(n) for n in ['01', '02', '03', '04', '05'])
    finishing = ''.join(f'<li>{E(x)}</li>' for x in C['finishing'])
    decisions = ''.join(f'<li><b>{E(d["q"])}</b> {E(d["text"])}<span class="rec">Recommended: {E(d["rec"])}</span></li>' for d in C['decisions'])
    tested = ''.join(f'<li>{E(x)}</li>' for x in C['tested'])
    untested = ''.join(f'<li>{E(x)}</li>' for x in C['not_tested'])
    process = ''.join(f'<li>{E(x)}</li>' for x in C['process'])
    created = ''.join(f'<li>{x}</li>' for x in C['changelog_created'])
    modified = ''.join(f'<li>{x}</li>' for x in C['changelog_modified'])
    pick = PAGES[C['pick']]['name']
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="atlas-views" content="overview">
<title>Atlas Editorial Systems Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="board" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Brand Guide, Edition 06 · Phase 2 · Atlas visual system</span></div>
<p class="eyebrow">Board 2 of the atlas systems · November 5, 2026</p>
<h1>Five editorial systems for the atlas</h1>
<p class="deck">{E(C["deck"])}</p>
<div class="ask"><h3>What you are asked</h3><ol>
<li><b>Pick one system</b> to finalize as the atlas's visual language and the pattern for your future systems maps. The studio recommends {E(pick)}.</li>
<li><b>Answer the wording and mark calls</b> in the decisions section. Each has a recommendation.</li></ol>
<p class="reply">{E(C["sample_reply"])}</p></div>
<nav class="toc" aria-label="On this board"><a href="#scores">Scores</a>{"".join(f'<a href="#s{n}">{n} {E(PAGES[n]["name"])}</a>' for n in ["01","02","03","04","05"])}<a href="#rec">Recommendation</a><a href="#decisions">Decisions</a><a href="#process">How this was made</a><a href="#checks">Checks</a><a href="#changes">Change log</a></nav>
</header>
<section id="scores" aria-labelledby="h-scores"><p class="secnum">SCORES</p><h2 id="h-scores">How the five compare</h2>
<p>The creative director scored each system after the fix pass, 1 to 5 on the seven lines of the rubric, with 4 as the ship line on each. The four columns on the right are from the red team before the fix pass: the civic educator, the interface and accessibility lead, the evidence and brand auditor (each 1 to 5), and how many of 35 comprehension answers the simulated readers got fully right.</p>
{scores_table()}
<p class="small">The readers were simulated by one model, never people. No real reader has seen any of the five.</p></section>
{bands}
<section id="rec" aria-labelledby="h-rec"><p class="secnum">RECOMMENDATION</p><h2 id="h-rec">The studio recommends {E(pick)}</h2>
<p class="deck">{E(C["rec_text"])}</p><p><b>Runner-up: {E(PAGES[C["runner_up"]]["name"])}.</b> {E(C["runner_text"])}</p>
<h4>Finishing work if you pick {E(pick)}</h4><ol>{finishing}</ol></section>
<div class="decision" id="decisions" role="region" aria-labelledby="h-dec"><h2 id="h-dec">Decisions</h2><ol>{decisions}</ol></div>
<section id="process" aria-labelledby="h-proc"><p class="secnum">HOW THIS WAS MADE</p><h2 id="h-proc">Five makers, four reviewers, one fix pass</h2><ol>{process}</ol></section>
<section id="checks" aria-labelledby="h-checks"><p class="secnum">CHECKS</p><h2 id="h-checks">What was tested</h2>
<div class="cols"><div><h4>Tested</h4><ul class="facts">{tested}</ul></div><div><h4>Not tested</h4><ul class="facts">{untested}</ul></div></div></section>
<section id="changes" aria-labelledby="h-ch"><p class="secnum">CHANGE LOG</p><h2 id="h-ch">Files</h2>
<p class="small">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>. Nothing in <code>source/</code>, the Civic Line icons or the identity masters changed.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts">{created}</ul></div><div><h4>Modified</h4><ul class="facts">{modified}</ul></div></div></section>
<p class="small" style="margin-top:40px">Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026: 51 variables, 118 connections, 23 loops, 194 issue records, 50 reforms. Headlines on the five pages are studio drafts.</p>
</main></body></html>'''
    OUT.write_text(page)
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace('<title>Atlas Editorial Systems Board</title>\n', '')
    PUB.parent.mkdir(parents=True, exist_ok=True)
    PUB.write_text('<title>Atlas Editorial Systems Board</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + re.sub(r'</body>\s*</html>\s*$', '', body))
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1e6:.1f} MB', 'and', PUB)


if __name__ == '__main__':
    build()
