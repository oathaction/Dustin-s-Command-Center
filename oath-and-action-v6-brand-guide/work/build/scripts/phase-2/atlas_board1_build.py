"""Build Board 1 of the atlas concepts (October 30, 2026): the shared frame, the twelve-concept roster, the ten
from-scratch directions and the data visualization research, with the decisions for Dustin.

Usage:
    node work/build/scripts/phase-2/atlas_board1_capture.js      # element captures from the Stage 1 pages
    python3 -I work/build/scripts/phase-2/atlas_board1_build.py  # writes the board, images embedded

Writes work/boards/20261030_Atlas-Concepts-Ideas-Board.html, self-contained so it can publish as a private page.
Every count it prints is read from the model export or from the Stage 1 files named beside it.
"""
import base64
import html
import io
import json
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[4]
AC = ROOT / 'work/boards/phase-2/atlas-concepts'
IMG = AC / 'board-1/img'
REF = ROOT / 'work/research/chat-references/atlas-concepts'
DVR = ROOT / 'work/research/data-viz-references'
OUT = ROOT / 'work/boards/20261030_Atlas-Concepts-Ideas-Board.html'
PUB = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/116edc6c-f1d0-50f6-9263-c43fde110995/scratchpad/publish/20261030_Atlas-Concepts-Ideas-Board.html')
M = json.loads((ROOT / 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json').read_text())
GEO = json.loads((AC / 'shared/20261030_Loop-Route-Geometry.json').read_text())
E = lambda s: html.escape(str(s), quote=True)
C = M['generated']['counts']


def img(path, width=1000, alt='', cls='', quality=80):
    im = Image.open(path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    data = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/jpeg;base64,{data}" width="{im.width}" height="{im.height}" alt="{E(alt)}" class="{cls}">'


FIXED = [
    ('01', 'The Circuit, refined', 'Newsprint', 'Your Concept 09',
     'Five area cards wired left to right, with the household economy and technology layers below. The studio keeps the wiring, calms the lower channel and the crossing between D and E that the creative director flagged on October 28, and lets a reader isolate one wire.',
     REF / '20261030_Ref-Atlas-Concept-09-The-Circuit.png', 'Your Concept 09, The Circuit'),
    ('02', 'The Stack', 'White', 'Your Civic Architecture and Decision Grid boards',
     'The areas as stacked floors, each variable with its Civic Line icon, and a panel for the selected item. Built with V7\'s own variables in place of the invented groups on the reference boards.',
     REF / '20261030_Ref-Atlas-Civic-Architecture-Layers.webp', 'Your Civic Architecture layers board'),
    ('03', 'Night Schematic', 'Charcoal', 'Your Fine Structure and grouped overview boards',
     'A dark schematic: each area a bracket tree of its variables, the flows between areas as quiet lines, and one route lit at a time.',
     REF / '20261030_Ref-Atlas-Civic-Circuit-Grouped-Overview.webp', 'Your grouped overview board on a dark ground'),
    ('04', 'Civic Landscape', 'Newsprint', 'Your Civic Landscape board',
     'The areas as territories on one map, with routes between them and a clear place to start.',
     REF / '20261030_Ref-Atlas-Civic-Landscape.webp', 'Your Civic Landscape board'),
    ('05', 'Loop Card as the unit', 'Newsprint', 'Your Concept 07 Loop Card and the Civic Architecture loop page',
     'Every loop as a card that reads aloud, step by step, with the reform marked where it acts. The overview is a field of those cards, arranged by area.',
     REF / '20261030_Ref-Atlas-Concept-07-Loop-Card-R10.png', 'Your Concept 07 Loop Card for R10'),
    ('06', 'Loop Lines with the Field Guide', 'Prussian poster, Newsprint cards', 'The studio pick of October 28',
     'The transit-style poster of the 20 numbered loops on Prussian, with field-guide cards for each loop, now drawn with loop-route thumbnails.',
     ROOT / 'work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Poster-Capture.png', 'The Loop Lines poster from October 28'),
]

SCRATCH = [
    ('07', 'great-circle', 'Great Circle', 'Newsprint', 1),
    ('08', 'star-atlas', 'Star Atlas', 'Charcoal', 2),
    ('09', 'open-atlas', 'Open Atlas', 'Newsprint with White pages', 3),
    ('10', 'kitchen-table', 'Kitchen Table', 'White', 4),
    ('11', 'flywheels', 'Flywheels and Governors', 'Charcoal (sketched on Newsprint; moved for DR-17)', 5),
]
IDEAS = {
    'great-circle': ('Great Circle', 'The five core areas drawn as one ring, because influence in the model travels around a circle.', 'It shows the circle the core areas form in one shape, and every loop thumbnail is that loop drawn on the same ring.'),
    'star-atlas': ('Star Atlas', 'Variables as stars and loops as named constellations, on a dark sky divided into regions.', 'The most beautiful of the ten, and the loop page becomes a page of distinct, named figures.'),
    'open-atlas': ('Open Atlas', 'The system as a two-page spread: the economy on the left, democracy on the right, technology in the fold.', "It puts the publication's own argument, that democracy and the economy form one system, in the middle of the page."),
    'kitchen-table': ('Kitchen Table', 'The household at the center, with every other variable placed by how many steps it takes to reach it.', 'The best first door for a member of the public: it starts at the household and measures everything from there.'),
    'flywheels': ('Flywheels and Governors', 'Loops as machines: reinforcing loops are flywheels, balancing loops are governors.', 'It teaches the difference between feeding itself and pushing back through objects people already know.'),
    'honeycomb': ('Honeycomb', 'Fifty-one equal tiles in territories, the way newsrooms draw states on election night.', 'The most phone-ready overview, in a form the public already knows from election coverage.'),
    'crossroads': ('Crossroads', 'Loops as petals growing from the variables they share, printed like a cyanotype.', 'Striking and true to where loops meet, but showing one variable in two places will trip up new readers.'),
    'spine': ('The Spine', 'All 51 variables on one line, with each connection as an arc; feedback shows as arcs that run back.', 'Exact and easy to scroll, held back by abstraction and by its dependence on one chosen order.'),
    'ledger-grid': ('Ledger Grid', 'Every connection as a cell in a table of causes and effects; loops become staircases.', 'The most exact drawing of the model, best kept as an expert view because its first screen asks a lot of a new reader.'),
    'tabletop': ('Tabletop Model', "An architect's model of the system, each variable a block whose height counts the loops through it.", 'An appealing skyline, but height will be read as amount, and it costs the most to build.'),
}
RANK = ['great-circle', 'star-atlas', 'open-atlas', 'kitchen-table', 'flywheels', 'honeycomb', 'crossroads', 'spine', 'ledger-grid', 'tabletop']


def card_fixed(n, name, ground, src, idea, path, alt):
    return f'''<article class="card">
  <figure class="shot">{img(path, 900, alt)}</figure>
  <div class="card-b"><p class="num">{n}</p><h3>{E(name)}</h3>
  <p class="meta"><span class="chip">{E(ground)}</span></p>
  <p class="from">Grown from: {E(src)}</p><p>{E(idea)}</p></div></article>'''


def card_scratch(n, key, name, ground, rank):
    t, idea, why = IDEAS[key]
    return f'''<article class="card">
  <figure class="shot">{img(IMG / f"sketch-{key}.jpg", 900, f"Sketch of {name}")}</figure>
  <div class="card-b"><p class="num">{n}</p><h3>{E(name)}</h3>
  <p class="meta"><span class="chip">{E(ground)}</span> <span class="chip ghost">Rank {rank} of 10</span></p>
  <p>{E(idea)}</p><p class="why">{E(why)}</p></div></article>'''


def table_levels():
    rows = [
        ('The system', 'What shapes who officials answer to?', 'Conditions push on one another, and 23 chains of cause return to where they started.'),
        ('Area C', 'Can officials here lose their seats, and who controls election rules?', 'Electoral pressure (C3) is where R10 and B4 meet. B4 works only where seats are competitive, and R10 makes seats safe.'),
        ('Loop R10', 'Why does a safe-seat official answer to a small primary electorate, and why does that last?', 'Each turn feeds the next, and the weakest step, L53, is plausible.'),
        ('Reform R-01', 'What would R-01 change, and who could adopt it?', 'It acts on three named points, L08, L25 and C2, and each outcome family is rated on its own, never totaled.'),
    ]
    body = ''.join(f'<tr><th scope="row">{a}</th><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in rows)
    return f'<div class="tw" role="region" tabindex="0" aria-label="The four levels"><table><thead><tr><th scope="col">Level</th><th scope="col">The one question it answers</th><th scope="col">What a reader leaves with</th></tr></thead><tbody>{body}</tbody></table></div>'


def table_ten():
    rows = []
    for i, key in enumerate(RANK, 1):
        name, idea, why = IDEAS[key]
        if key in ('great-circle', 'star-atlas', 'open-atlas', 'kitchen-table', 'flywheels'):
            st = '<span class="chip solid">Build</span>'
        elif key == 'honeycomb':
            st = '<span class="chip">Your call: build, or swap for Editorial Desk</span>'
        else:
            st = '<span class="chip ghost">Hold</span>'
        rows.append(f'<tr><td class="r">{i}</td><th scope="row">{E(name)}</th><td>{E(idea)}</td><td>{E(why)}</td><td>{st}</td></tr>')
    return f'<div class="tw" role="region" tabindex="0" aria-label="Ten directions, ranked"><table><thead><tr><th scope="col">Rank</th><th scope="col">Direction</th><th scope="col">The idea</th><th scope="col">The ideation agent\'s reason</th><th scope="col">Status</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


sim = GEO.get('similarity', {}) if isinstance(GEO, dict) else {}

CSS = '''
/* Layout: one 1280 px reading column; cards in an auto-fill grid; Prussian decision band. Single light theme by choice: the board shows the brand on its Newsprint ground. */
:root{color-scheme:light;--bg:#DCD9D2;--surface:#E6E3DD;--white:#FFFFFF;--fg:#121212;--muted:#45494F;--rule:#5D636D;--prussian:#1F2D5A;--newsprint:#DCD9D2;
--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1rem/1.6 var(--body)}
a{color:inherit;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.board{max-width:1280px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--fg);padding-bottom:14px;flex-wrap:wrap}
.mast b{font:800 1.25rem/1 var(--display);letter-spacing:-.02em}.mast span{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.eyebrow{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:28px 0 0}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.025em;text-wrap:balance;margin:0}
h1{font-size:clamp(2.25rem,6vw,4.25rem);line-height:1.02;margin-top:10px;max-width:16ch}
h2{font-size:clamp(1.5rem,3vw,2.25rem);line-height:1.08;margin:0 0 12px}
h3{font-size:1.25rem;line-height:1.2;letter-spacing:-.015em}
h4{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px}
p{margin:0 0 12px;max-width:72ch}.deck{font-size:1.1875rem;line-height:1.5;max-width:62ch;margin-top:16px}
section{border-top:1px solid var(--rule);margin-top:48px;padding-top:32px}
.secnum{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.ask{background:var(--white);border:1px solid var(--rule);padding:22px 24px;margin-top:28px;display:grid;gap:8px}
.ask ol{margin:0;padding-left:1.3em}.ask li{margin:0 0 6px;max-width:80ch}.ask .reply{font:italic 400 1.0625rem/1.5 var(--quote);margin:6px 0 0}
.grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fill,minmax(min(100%,370px),1fr))}
.card{background:var(--white);border:1px solid var(--rule);display:flex;flex-direction:column;min-width:0}
.shot{margin:0;background:var(--surface);border-bottom:1px solid var(--rule);aspect-ratio:16/10;overflow:hidden;display:flex;align-items:center;justify-content:center}
.shot img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block}
.card-b{padding:16px 18px 18px}.card-b p{font-size:.9375rem;line-height:1.55;margin-bottom:8px}
.num{font:800 .9375rem/1 var(--display);color:var(--muted);margin:0 0 6px!important}
.meta{margin:8px 0 10px!important}.from{color:var(--muted)}.why{color:var(--muted);font-size:.875rem!important}
.chip{display:inline-block;font:600 .8125rem/1.3 var(--body);border:1px solid var(--fg);padding:2px 7px;margin:0 4px 4px 0}
.chip.ghost{border-color:var(--rule);color:var(--muted)}.chip.solid{background:var(--fg);color:var(--white)}
.alt{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,370px),1fr));gap:20px}
.altbox{background:var(--white);border:2px solid var(--fg);padding:18px 20px;display:flex;flex-direction:column;justify-content:flex-start}
.altbox .tag{font:700 .8125rem/1.3 var(--body);letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
.two{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:32px;align-items:start}
.two figure,.wide{margin:0}.two img,.wide img{width:100%;height:auto;display:block;border:1px solid var(--rule)}
figcaption{font-size:.875rem;line-height:1.45;color:var(--muted);margin-top:8px}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:70ch}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));border-top:2px solid var(--fg);margin:18px 0 20px}
.stats div{padding:12px 14px 12px 0}.stats b{display:block;font:800 2.25rem/1 var(--display);letter-spacing:-.03em}.stats span{font-size:.875rem;color:var(--muted);line-height:1.4;display:block;margin-top:6px}
.quote{border-left:3px solid var(--fg);padding:2px 0 2px 16px;margin:12px 0}.quote p{font:italic 400 1.0625rem/1.5 var(--quote);margin:0 0 6px}
.draft{font-size:.8125rem;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:var(--muted)}
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--white)}
table{border-collapse:collapse;width:100%;font-size:.9375rem;min-width:640px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #C9C6BF}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.05em;text-transform:uppercase;color:var(--muted);background:var(--surface)}
tbody th{font-weight:700}td.r{font:800 1rem/1.3 var(--display)}
.thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));gap:14px}
.thumbs.strips{grid-template-columns:1fr}
.thumbs figure{margin:0;background:var(--white);border:1px solid var(--rule);padding:10px}.thumbs img{width:100%;height:auto;display:block}
.decision{background:var(--prussian);color:var(--newsprint);padding:28px max(20px,3vw);margin-top:48px}
.decision *{color:inherit}.decision h2{color:#FFFFFF}.decision ol{padding-left:1.3em;margin:0}.decision li{margin:0 0 16px;max-width:86ch}
.decision .rec{display:block;margin-top:4px;font-weight:700}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:28px}
.small{font-size:.875rem;color:var(--muted)}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.toc{display:flex;flex-wrap:wrap;gap:6px 22px;margin:22px 0 0;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none}.toc a:hover{text-decoration:underline}
@media (max-width:820px){.two{grid-template-columns:1fr}}
'''


def build():
    fixed = ''.join(card_fixed(*f) for f in FIXED)
    scratch = ''.join(card_scratch(*s) for s in SCRATCH)
    held = ''.join(f'<figure>{img(IMG / f"sketch-{k}.jpg", 700, "Sketch of " + IDEAS[k][0])}<figcaption>{E(IDEAS[k][0])}, rank {RANK.index(k) + 1}</figcaption></figure>' for k in ('crossroads', 'spine', 'ledger-grid', 'tabletop'))
    strips = ''.join(f'<figure>{img(IMG / f"strip-{k}.jpg", 1600, "All 23 loops drawn in " + IDEAS[k][0])}<figcaption>{E(IDEAS[k][0])}: all 23 loops</figcaption></figure>' for k in ('great-circle', 'star-atlas', 'honeycomb', 'flywheels'))
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="atlas-views" content="overview">
<title>Atlas Concepts Board One</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="board" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Brand Guide, Edition 06 · Phase 2 · Atlas visual system</span></div>
<p class="eyebrow">Board 1 of the atlas concepts · October 30, 2026</p>
<h1>The frame and the ideas</h1>
<p class="deck">Four specialists set the rules every concept will share, and a designer who saw none of the earlier work pitched ten ways to draw the system from scratch. This board shows both, with the data visualization research you asked for. The twelve concepts get built after your answers.</p>
<div class="ask" aria-labelledby="h-ask"><h3 id="h-ask">What you are asked</h3>
<ol>
<li><b>Pick the six concepts from scratch</b> (sections 1 and 3). The studio recommends the ideation agent's six with one swap: Editorial Desk, a newspaper-graphics treatment shaped by your note on the Times, in place of Honeycomb.</li>
<li><b>Approve the shared frame as a set</b> (section 2): the four levels and their reading rules, loops drawn as routes, the navigation model, and the type and line scale.</li>
<li><b>Say when the data visualization system starts</b> (section 4). Recommended: right after you pick an atlas direction, so charts and maps share one visual language with the atlas.</li>
</ol>
<p class="reply">A reply can be this short: "Six: as recommended. Frame: approved. Data viz: after the atlas pick."</p></div>
<nav class="toc" aria-label="On this board"><a href="#s1">1 The twelve concepts</a><a href="#s2">2 The shared frame</a><a href="#s3">3 Ten directions from scratch</a><a href="#s4">4 Data visualization research</a><a href="#s5">5 Decisions</a><a href="#s6">6 Checks</a><a href="#s7">7 Change log</a></nav>
</header>

<section id="s1" aria-labelledby="h1s">
<p class="secnum">01</p><h2 id="h1s">The twelve concepts</h2>
<p>Each concept will be an overview of the whole system, a close-up of area C and loop R10, and a strip of all 23 loops drawn as routes, at 1440 and 390 px (DR-12, DR-13). Six grow from the boards you sent. Six come from scratch. Four sit on dark grounds (03, 06, 08, 11) and eight on light (DR-17).</p>
<h4>Grown from your references</h4>
<div class="grid">{fixed}</div>
<h4>From scratch</h4>
<div class="grid">{scratch}</div>
<h4>Concept 12: your call</h4>
<div class="alt">
<article class="card"><figure class="shot">{img(IMG / "sketch-honeycomb.jpg", 900, "Sketch of Honeycomb")}</figure>
<div class="card-b"><p class="num">12, option A</p><h3>Honeycomb</h3><p class="meta"><span class="chip">Newsprint</span> <span class="chip ghost">Rank 6 of 10</span></p>
<p>{E(IDEAS["honeycomb"][1])}</p><p class="why">{E(IDEAS["honeycomb"][2])} It overlaps concept 04, since both draw the areas as territories on a map.</p></div></article>
<div class="altbox"><p class="tag">12, option B · Recommended</p><h3>Editorial Desk</h3><p class="meta"><span class="chip">White</span> <span class="chip ghost">No sketch yet</span></p>
<p>The system drawn the way a newspaper graphics desk would draw it. The route the headline names runs in Charcoal and everything else sits back in Stone. Notes are set inside the drawing on fine leaders, the title is a sentence that states the finding, and the steps of R10 are told in order as the reader scrolls.</p>
<p class="why">Its structure is the data visualization lead's plan: the core areas as a ring with printed counts, and the 23 loops as the way in. Its look comes from the research in section 4, direction A, Annotated Newsprint. No other concept takes on the style you named.</p></div>
</div>
</section>

<section id="s2" aria-labelledby="h2s">
<p class="secnum">02</p><h2 id="h2s">The shared frame</h2>
<p>Every concept follows these rules, so the twelve differ in their big idea and meet one standard of finish. Each part comes from a specialist's memo in <code>work/handoffs/phase-2/</code>.</p>

<h3>The reader and the four levels</h3>
<p class="small">Civic education expert · <code>20261030_Atlas-Civic-Education-Memo.md</code></p>
{table_levels()}
<h4>Three rules the expert ranks first</h4>
<ul class="facts">
<li>Print "raises" or "lowers" on every connection a first-time reader meets, and keep the plus and minus signs beside the words. A newcomer reads the plus between housing scarcity and owner home equity (L38) as "scarcity is good."</li>
<li>Build each loop's read-aloud line from its signs by script. For R10: "More safe seats, more primary decisiveness, less electoral pressure, more incumbent control of election rules, and back to more safe seats."</li>
<li>Show each loop's weakest step and its reforms on the loop's own view, so a loop never reads as fate. 22 of the 23 loops have at least one reform (B5 has none).</li>
</ul>
<h4>Draft overview lines, written by the studio</h4>
<div class="cols">
<div class="quote"><p>Who do officials answer to?</p><p>This map links 51 conditions, from household wealth to court rulings, through 118 connections. Each connection carries a grade for the strength of its evidence.</p></div>
<div class="quote"><p>Can your representative lose their seat?</p><p>"In a safe seat, the primary decides who wins, and few people vote in it." That pattern is one of 23 loops on this map of 51 conditions and the connections between them.</p></div>
<div class="quote"><p>Where economic power meets public office.</p><p>The map follows 118 connections among 51 conditions, from household wealth to the risk of losing office. In 23 places, a chain of causes returns to where it started.</p></div>
</div>
<p class="small">How to read the map, in 23 words: "Each name is a condition that can rise or fall; an arrow shows one raising or lowering another. Broken lines mark weaker evidence."</p>

<h3 style="margin-top:36px">Loops drawn as their own routes</h3>
<p class="small">Data visualization lead · <code>20261030_Atlas-Dataviz-Memo.md</code>, <code>shared/20261030_Loop-Route-Thumbnails-Study.html</code></p>
<div class="two"><figure>{img(IMG / "routes-newsprint.jpg", 1400, "The loop-route study: loop thumbnails on one shared plan of the system")}<figcaption>The study sheet. Every loop is drawn as the path it takes across one plan of the system, so each thumbnail also shows where its loop lives.</figcaption></figure>
<div><div class="stats"><div><b>{C["loops"]}</b><span>loops, {C["loops_numbered"]} with a complete numbered chain</span></div><div><b>0.57</b><span>highest similarity of any two thumbnails, under the 0.60 limit (R1 and R6)</span></div><div><b>310</b><span>pixels wide for the full form; below 256 px a thumbnail is a locator only</span></div></div>
<ul class="facts">
<li>The plan puts the outside drivers on top, the economy and technology layers below, and the five core areas in a ring between them. The core's 38 connections between areas join only seven pairs, so in the ring every one joins two neighbors.</li>
<li>Each step carries its evidence texture, a pointing tag for sign and direction, and a bar on the step that closes the loop. Sketched loops (B2, B3, R9) sit off the map and say so.</li>
<li>Its overview advice: draw all 118 connections and you get 339 crossings. Draw the ring with the seven core counts printed as numbers and you get none, with the 23 loops as the way in and every connection one click down.</li>
<li>Each concept may draw its thumbnails in its own style, as the ten sketches do, as long as each one is the loop's real route (DR-15).</li>
</ul></div></div>

<h3 style="margin-top:36px">Moving between levels</h3>
<p class="small">UX and accessibility lead · <code>20261030_Atlas-Interaction-Memo.md</code>, <code>shared/atlas-kit.js</code>, <code>shared/20261030_Atlas-Kit-Demo.html</code></p>
<div class="two"><figure>{img(IMG / "kit-overview.jpg", 1400, "The interaction kit demo, overview view")}<figcaption>The kit demo built from the model. It is a test bed for behavior, not a visual concept.</figcaption></figure>
<div><ul class="facts">
<li><b>Views with a panel.</b> Each level has its own address (overview, area C, loop R10), so the Back button always moves up a level. An area or loop opens with a short zoom from the item clicked. A variable, connection or reform opens in a side panel, which becomes a bottom sheet on a phone.</li>
<li>Hover never carries anything that focus and tap do not also give. Arrow keys move along the drawing, and every drawing has its lines in words.</li>
<li>A loop can be stepped through one link at a time, with play, pause and reset, and a still sequence for readers who turn motion off.</li>
<li>Tested: 76 scripted checks pass, and axe-core finds 0 violations in nine states.</li>
</ul>
<figure style="max-width:260px;margin-top:14px">{img(IMG / "kit-loop-r10-phone.jpg", 520, "The demo's R10 view at 390 px")}<figcaption>R10 at 390 px.</figcaption></figure></div></div>

<h3 style="margin-top:36px">Type, lines and grounds</h3>
<p class="small">Design director · <code>20261030_Atlas-Design-Frame-Memo.md</code>, <code>shared/20261030_Atlas-Type-And-Line-Specimen.html</code></p>
<div class="two"><figure>{img(IMG / "specimen-lines.jpg", 1400, "The V7 evidence line code at three weights")}<figcaption>V7's evidence code at the three weights the concepts use: context lines, a step in a close-up, and the lit route.</figcaption></figure>
<div><ul class="facts">
<li><b>Type scale.</b> Display in Inter Tight 800 at 56 px, headline 40, panel head 22; deck in Inter at 19, body 17; station labels in Inter Tight 700 at 20, map labels in Inter 600 at 15; notes, legends and source lines at 13; quotes in Lora Italic at 22; and the two-part ID chip.</li>
<li><b>One stroke family</b> of 1, 1.5, 2, 3 and 6 px, with each evidence pattern drawn in multiples of its line width so a texture keeps its shape from the overview to the lit route.</li>
<li><b>One arrowhead</b> sized by weight. Labels stay 4 px clear of every stroke.</li>
<li><b>One working red per view.</b> Red never marks a sign, a hover state or navigation, and never sits on Prussian.</li>
<li>Faults on the generated boards that no concept copies: redrawn wordmarks, five to ten reds in a view, renamed variables and reforms, steps without signs, tints outside the palette.</li>
</ul></div></div>
<h4>Calls the studio made today</h4>
<ul class="facts">
<li>D2-56: the pointing tag is the default sign mark in every concept. Choice 3 of the direction review stays open for you.</li>
<li>D2-57: inside a dense map, a node may print its bare code (C1) when the key names the type.</li>
<li>D2-58: until you decide P3, the current icon in a row keeps its red as the view's working red.</li>
<li>D2-59: Dim Newsprint, adopted at Gate 1, joins the atlas palette for secondary text on dark grounds.</li>
<li>D2-60: one stroke family for every atlas drawing.</li>
</ul>
</section>

<section id="s3" aria-labelledby="h3s">
<p class="secnum">03</p><h2 id="h3s">Ten directions from scratch</h2>
<p>A designer briefed only with the model, the palette, the type, the red rule and your words pitched ten directions, each with a sketch drawn from the model and all 23 loops in its own drawing. The full sheet is <code>work/boards/phase-2/atlas-concepts/ideas/20261030_From-Scratch-Directions-Sketches.html</code>. The designer and the data visualization lead each arrived at a ring of the core areas without seeing the other's work: 20 connections run forward around A, B, C, D, E and back to A, and 11 run the other way.</p>
{table_ten()}
<h4>Loop strips from four directions</h4>
<p>Your note on the loop catalog, answered four ways. Each strip shows all 23 loops, and no two look alike.</p>
<div class="thumbs strips">{strips}</div>
<h4>The four directions on hold</h4>
<div class="thumbs">{held}</div>
<p class="small">The main session made the recommendation on concept 12. No creative director reviewed the ten before this board; the creative director reviews all twelve built concepts at the next stage.</p>
</section>

<section id="s4" aria-labelledby="h4s">
<p class="secnum">04</p><h2 id="h4s">Data visualization research</h2>
<p>You asked for an Oath &amp; Action system for charts, graphs, maps and tables, with the Times as the style you like most. The research lead read the four sites you sent, plus Our World in Data, which the brief requires. The full brief is <code>work/research/20261030_Data-Viz-System-References.md</code>, with 28 rules and 13 study captures.</p>
<div class="cols">
<div><h4>Read</h4><ul class="facts">
<li>The Gagnier case study, including four Times brand principles</li>
<li>The Times's open-source ai2html tool and a 2016 talk by Archie Tse, then a Times graphics director</li>
<li>Public writing by three Times graphics editors, and five Times charts reproduced on Datawrapper's blog</li>
<li>Ten Carbon data visualization pages</li>
<li>BBC GEL's infographic and chart description guidance, and the BBC's bbplot package and its R cookbook</li>
<li>Our World in Data's redesign article and a live chart, map and table</li>
<li>The Economist's 2017 map style guide</li>
</ul></div>
<div><h4>Not read</h4><ul class="facts">
<li>Any nytimes.com page. The site refuses automated requests, and the studio respects that. How Times charts behave on phones, and its small multiples, tables and source lines, stay unverified.</li>
<li>The Economist's 2017 chart guide, which is no longer online, and one article that refused the connection</li>
<li>Carbon's chart accessibility page, which returns an error</li>
</ul>
<p class="small">If you save a few Times graphics pages as PDFs or screenshots, the studio can study the Times first hand.</p></div>
</div>
<h4>Five rules the research lead ranks first</h4>
<ul class="facts">
<li>The title is a sentence that states the finding, with its evidence kind (finding, association, estimate, illustration) as a label above it.</li>
<li>Annotation goes inside the chart, on fine leader lines.</li>
<li>Context data in Stone, the series the title names in Charcoal.</li>
<li>Red marks only the one point the headline names, and never a series or a scale.</li>
<li>Diverging scales never pair red with blue. Two candidates to test at Gate 2: Stone to Verdigris, and Prussian through Newsprint to Verdigris.</li>
</ul>
<h4>Three candidate directions</h4>
<div class="cols">
<div><h3>A. Annotated Newsprint</h3><p>Times-style sentence titles and annotation on Newsprint, with our evidence labels and grade-matched verbs.</p></div>
<div><h3>B. Field Instrument</h3><p>Hairline technical charts on the Signal Grid, labeled with real Atlas V7 IDs.</p></div>
<div><h3>C. Two-Ink Register</h3><p>Prussian and Verdigris only, with tables as first-class views and chart, table and map tabs.</p></div>
</div>
<div class="thumbs" style="margin-top:12px">
<figure>{img(DVR / "20261030_Capture-Gagnier-NYT-Case-Study.jpg", 800, "Study capture of the Gagnier case study")}<figcaption>Gagnier case study. Study only.</figcaption></figure>
<figure>{img(DVR / "20261030_Capture-Carbon-Color-Palettes.jpg", 800, "Study capture of Carbon color palettes")}<figcaption>Carbon color palettes. Study only.</figcaption></figure>
<figure>{img(DVR / "20261030_Capture-OWID-Grapher-Table.jpg", 800, "Study capture of an Our World in Data table view")}<figcaption>Our World in Data table view. Study only.</figcaption></figure>
</div>
</section>

<div class="decision" id="s5" role="region" aria-labelledby="h5s">
<h2 id="h5s">Decisions</h2>
<ol>
<li><b>The six concepts from scratch.</b> Options: the ideation agent's six (Great Circle, Star Atlas, Open Atlas, Kitchen Table, Flywheels and Governors, Honeycomb); the same with Editorial Desk in place of Honeycomb; or your own picks from the ten.<span class="rec">Recommended: Editorial Desk in place of Honeycomb. It tests the newspaper style you named, and Honeycomb overlaps concept 04.</span></li>
<li><b>The shared frame, as a set.</b> The four levels and the reading rules, loops drawn as routes, views with a panel, and the type, line and ground rules, with the calls D2-56 to D2-60.<span class="rec">Recommended: approve as a set.</span></li>
<li><b>When the data visualization system starts.</b> Options: (a) in Phase 3 order, after the atlas, the open direction review items and Gate 2; (b) right after you pick an atlas direction.<span class="rec">Recommended: (b). Charts, maps and the atlas share type, lines and color, so building them together keeps one language.</span></li>
</ol>
<p>After your answers, twelve makers build in parallel, each concept passes the shared checks, the creative director scores all twelve, and Board 2 shows them at true size with a recommendation of two or three.</p>
</div>

<section id="s6" aria-labelledby="h6s">
<p class="secnum">06</p><h2 id="h6s">Checks</h2>
<div class="cols"><div><h4>Tested</h4><ul class="facts">
<li>The shared data verifier caught all six errors planted in a test page, and the shared rendered check caught a planted unmarked red and a contrast failure.</li>
<li>The loop-route study: all 23 thumbnails drawn from the model; no pair reaches the 0.60 similarity limit at 256, 310 or 318 px.</li>
<li>The interaction kit: 76 scripted checks and 0 axe-core violations in nine states.</li>
<li>The type and line specimen: no sideways scroll, no text under 13 px and 0 axe-core violations at 1440 and 390 px.</li>
<li>The civic education memo's quoted strings match the model.</li>
<li>This board: rendered at 1440 and 390 px with the shared check script.</li>
</ul></div>
<div><h4>Not tested</h4><ul class="facts">
<li>Readers. No person has seen any concept, thumbnail or sketch.</li>
<li>Screen readers, Firefox, Safari and real phones.</li>
<li>Any nytimes.com page, by rule.</li>
<li>The raw Atlas V7 file, which stays on your machine. Every figure comes from the October 28 model export (DR-20).</li>
</ul></div></div>
</section>

<section id="s7" aria-labelledby="h7s">
<p class="secnum">07</p><h2 id="h7s">Change log</h2>
<p class="small">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>. Nothing in <code>source/</code>, the Civic Line icons or the identity masters changed.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts">
<li><code>work/handoffs/phase-2/</code>: the concepts brief and four memos (civic education, data visualization, interaction, design frame) and the ten directions from scratch</li>
<li><code>work/boards/phase-2/atlas-concepts/shared/</code>: the variable-to-icon map, loop-route study and geometry, interaction kit and demo, type and line specimen</li>
<li><code>work/boards/phase-2/atlas-concepts/ideas/</code>: the ten sketches page and its build script</li>
<li><code>work/boards/phase-2/atlas-concepts/board-1/img/</code>: this board's captures</li>
<li><code>work/research/20261030_Data-Viz-System-References.md</code> and <code>work/research/data-viz-references/</code></li>
<li><code>work/research/chat-references/atlas-concepts/</code> and <code>data-viz/</code>: your twelve reference images</li>
<li><code>work/build/scripts/phase-2/</code>: shared check, verify and common scripts, the loop-route and kit scripts, and this board's capture and build scripts</li>
<li><code>work/boards/20261030_Atlas-Concepts-Ideas-Board.html</code>: this board</li>
</ul></div>
<div><h4>Modified</h4><ul class="facts">
<li><code>work/ledger/20261020_Decision-Log.md</code>: DR-12 to DR-22, D2-47 to D2-62</li>
<li><code>work/research/20261020_Rights-Ledger.md</code>: the October 30 references and research sources</li>
</ul></div></div>
</section>
<p class="small" style="margin-top:40px">Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026: {C["variables"]} variables, {C["connections"]} connections, {C["loops"]} loops, {C["reforms"]} reforms. Sketches and studies are for direction only.</p>
</main></body></html>'''
    OUT.write_text(page)
    PUB.parent.mkdir(parents=True, exist_ok=True)
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1e6:.1f} MB')
    # the publish copy: the artifact host wraps the page in its own document skeleton
    import re
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1].replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    title = '<title>Atlas Concepts Board One</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
    head = head.replace('<title>Atlas Concepts Board One</title>\n', '')
    frag = title + head + re.sub(r'</body>\s*</html>\s*$', '', body)
    PUB.write_text(frag)
    print('wrote publish copy', PUB)


if __name__ == '__main__':
    build()
