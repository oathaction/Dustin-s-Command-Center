"""Build Board 4 of the data visualization round (November 6, 2026): the chapter 14 coverage plan and the six
stretch charts, for Dustin's review.

Usage:
    python3 -I work/build/scripts/phase-2/dataviz_board4_build.py

Reads the coverage plan (work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md, parsed from its tables), the
board content (board-4/20261106_Board-4-Content.json: the creative director's verdicts and scores, then the main
session's process, checks and change log), the published page links (board-4/20261106_Published-Pages.json,
optional), and the captures written by dataviz_board4_capture.js. Writes:
    work/boards/20261106_Data-Viz-Coverage-Board.html          (the studio record, a full document)
    <scratchpad>/publish/20261106_Data-Viz-Coverage-Board.html (the publish copy for the private page)
"""
import base64
import collections
import html
import io
import json
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[4]
DV = ROOT / 'work/boards/phase-2/data-viz'
B4 = DV / 'board-4'
CAP = B4 / 'captures'
PLAN = ROOT / 'work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md'
OUT = ROOT / 'work/boards/20261106_Data-Viz-Coverage-Board.html'
PUB = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/72a6dd5d-b3ac-5a79-9ac0-32d5f5fbde66/scratchpad/publish/20261106_Data-Viz-Coverage-Board.html')
C = json.loads((B4 / '20261106_Board-4-Content.json').read_text())       # the creative director's content
REC = B4 / '20261106_Board-4-Studio-Record.json'                         # the main session's: process, checks, files, next stage
C.update(json.loads(REC.read_text()) if REC.exists() else {})
PP = B4 / '20261106_Published-Pages.json'
PAGES = json.loads(PP.read_text()) if PP.exists() else {}
SPECS = ['S11', 'S12', 'S13', 'S14', 'S15', 'S16']
TIERS = ['Core', 'Extended', 'Reference', 'Avoid']
RUBRIC = ['Craft', 'Clarity', 'Brand', 'Usefulness', 'Evidence', 'Access', 'Beauty']
REFS = {'NYT1': 'your election shift charts', 'NYT2': 'your results tables', 'NYT3': 'your election maps',
        'NYT4': 'your jobs report charts', 'NYT5': 'your House tile maps', 'ECO': 'the chart montage',
        'COL': 'the navy and teal collage', 'P14': 'page 14 of your saved pictures'}


def copy(s):
    """Curly quotes and apostrophes, and the true minus before a figure, as on the chart pages."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '\u201c\\1\u201d', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '\u2019', s)
    s = re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", '\u2018\\1\u2019', s)
    return re.sub(r'(?<![\w.\-])-(?=\d)', '\u2212', s)


E = lambda s: html.escape(copy(s), quote=True)


def md(s):
    """The plan's light markdown (backticks and bold) as escaped HTML."""
    s = E(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)


# ------------------------------------------------------------------------------------------------ the plan
def parse_plan():
    t = PLAN.read_text()
    rules = re.findall(r'^- (.+)$', t.split('Rules that hold across every form:')[1].split('## 2.')[0], flags=re.M)
    tier_rows = [r for r in t.split('## 2. Tiers')[1].split('## 3.')[0].splitlines() if r.startswith('| ') and not r.startswith('| Tier')]
    tier_text = {}
    for r in tier_rows:
        cells = [x.strip() for x in r.strip('|').split('|')]
        tier_text[cells[0]] = (cells[1], int(cells[2]))
    fams = []
    for block in re.split(r'\n### ', t.split('## 3. The families')[1].split('## 4.')[0])[1:]:
        head = block.split('\n')[0]
        num, rest = head.split(' ', 1)
        name, question = rest.split(': ', 1)
        rows = []
        for line in block.splitlines():
            if not line.startswith('| ') or line.startswith('| Form') or line.startswith('|---'):
                continue
            form, tier, use, data, status = [x.strip() for x in line.strip('|').split('|')]
            rows.append(row_of(form, tier, use, data, status))
        note = re.findall(r'^Every .+$', block, flags=re.M)
        fams.append({'num': num, 'id': 'f' + num.replace('.', '-'), 'name': name, 'question': question,
                     'rows': rows, 'note': note[0] if note else ''})
    order = []
    for r in t.split('## 4. Phase 3 build order')[1].split('A balance check')[0].splitlines():
        if r.startswith('| ') and not r.startswith('| Round'):
            order.append([x.strip() for x in r.strip('|').split('|')])
    balance = re.search(r'^A balance check.+$', t, flags=re.M).group(0)
    return rules, tier_text, fams, order, balance


def row_of(form, tier, use, data, status):
    t = tier.split(',')[0]
    parts = [p.strip() for p in status.split(',')]
    refs = [REFS[p] for p in parts if p in REFS]
    rest = [p for p in parts if p not in REFS]
    st = rest[0] if rest else ''
    spec = re.findall(r'S\d\d', st)
    if st.startswith('Built in each system'):
        kind, label = 'built', 'Built in all three systems'
    elif st.startswith('Built'):
        kind, label = 'built', 'Built, ' + ' and '.join(spec) + (' (panels)' if 'panels' in st else '')
    elif st.startswith('Stretch'):
        kind, label = 'stretch', 'Stretch test, ' + ' and '.join(spec)
    elif st.startswith('Register'):
        kind, label = 'register', 'Built in Register; folds into Explainer'
    elif st.startswith('Rule only'):
        kind, label = 'rule', 'Rule only'
    elif st.startswith('Sketch'):
        kind, label = 'sketch', 'Sketch and rule'
    else:
        kind, label = 'phase3', st or 'Phase 3'
    extra = [p for p in rest[1:]]
    if 'interactive' in tier:
        extra.append('interactive')
    return {'form': form, 'tier': t, 'tier_full': tier, 'use': use, 'data': data, 'kind': kind, 'label': label,
            'extra': extra, 'refs': refs, 'drawn': kind in ('built', 'stretch')}


RULES, TIER_TEXT, FAMS, ORDER, BALANCE = parse_plan()
ALL = [r for f in FAMS for r in f['rows']]
COUNT = collections.Counter(r['tier'] for r in ALL)
TOTAL = len(ALL)
assert all(TIER_TEXT[t][1] == COUNT[t] for t in TIERS), (COUNT, TIER_TEXT)   # the family tables agree with the tier table (D2-125, D2-127)
assert str(TOTAL) in PLAN.read_text().split('## 3.')[0], 'the plan states its own entry count'
DRAWN = sum(r['drawn'] for r in ALL)


def unit_map():
    rows = []
    for f in FAMS:
        key = {'Core': 0, 'Extended': 1, 'Reference': 2, 'Avoid': 3}
        units = sorted(f['rows'], key=lambda r: (key[r['tier']], not r['drawn']))
        c = collections.Counter(r['tier'] for r in f['rows'])
        d = sum(r['drawn'] for r in f['rows'])
        words = ', '.join(f'{c[t]} {t.lower()}' for t in TIERS if c[t])
        aria = f"{f['name']}: {len(f['rows'])} forms, {words}; {d} drawn so far."
        sq = ''.join(f'<span class="u u-{r["tier"].lower()}{" drawn" if r["drawn"] else ""}" title="{E(r["form"])}, {E(r["tier"].lower())}"></span>' for r in units)
        rows.append(f'<li><a href="#{f["id"]}"><span class="un">{E(f["name"])}</span><span class="uc">{len(f["rows"])}</span></a>'
                    f'<span class="us" role="img" aria-label="{E(aria)}">{sq}</span></li>')
    legend = ''.join(f'<li><span class="u u-{t.lower()}"></span>{t}, {COUNT[t]}</li>' for t in TIERS)
    return (f'<figure class="umap"><figcaption class="umap-h"><b>All {TOTAL} forms, one square each, by family and tier.</b> '
            f'A dot marks a form already drawn in the Explainer system: {DRAWN} so far, from the ten specimens and the six in this test. '
            f'Each family name links to its table.</figcaption>'
            f'<ul class="ulegend" aria-label="Key">{legend}<li><span class="u u-core drawn"></span>Drawn so far, {DRAWN}</li></ul>'
            f'<ol class="urows">{"".join(rows)}</ol></figure>')


def family_table(f):
    c = collections.Counter(r['tier'] for r in f['rows'])
    chips = ''.join(f'<span class="tc tc-{t.lower()}">{c[t]} {t.lower()}</span>' for t in TIERS if c[t])
    body = []
    for r in f['rows']:
        ex = ''.join(f'<span class="x">{E(x)}</span>' for x in r['extra'])
        refs = f'<span class="x">From {E(" and ".join(r["refs"]))}</span>' if r['refs'] else ''
        body.append(f'<tr class="k-{r["kind"]}"><th scope="row">{E(r["form"])}</th>'
                    f'<td><span class="tier t-{r["tier"].lower()}"><span class="u u-{r["tier"].lower()}" aria-hidden="true"></span>{E(r["tier"])}</span></td>'
                    f'<td>{E(r["use"])}</td><td>{E(r["data"])}</td>'
                    f'<td><span class="st st-{r["kind"]}">{E(r["label"])}</span>{ex}{refs}</td></tr>')
    note = f'<p class="fnote">{E(f["note"])}</p>' if f['note'] else ''
    return (f'<article class="fam" id="{f["id"]}" aria-labelledby="{f["id"]}-h">'
            f'<div class="fam-h"><p class="secnum">FAMILY {E(f["num"].split(".")[1])} OF 16</p>'
            f'<h3 id="{f["id"]}-h">{E(f["name"])}</h3><p class="fq">{E(f["question"][0].upper() + f["question"][1:])}</p>'
            f'<p class="chips">{chips}</p></div>'
            f'<div class="tw" role="region" tabindex="0" aria-label="{E(f["name"])}: the forms"><table class="ft">'
            f'<thead><tr><th scope="col">Form</th><th scope="col">Tier</th><th scope="col">What Oath &amp; Action uses it for</th>'
            f'<th scope="col">Specimen data</th><th scope="col">Status</th></tr></thead><tbody>{"".join(body)}</tbody></table></div>{note}</article>')


# ------------------------------------------------------------------------------------------------ captures
def img(name, alt, out_w=1440, q=80, cls=''):
    p = CAP / name
    if not p.exists():
        return f'<p class="missing">Capture {E(name)} not made yet.</p>'
    im = Image.open(p).convert('RGB')
    if im.width > out_w:
        im = im.resize((out_w, round(im.height * out_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    w, h = im.width // 2, im.height // 2      # captured at twice size; shown at true size
    return (f'<img{f" class={cls}" if cls else ""} src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}" '
            f'width="{w}" height="{h}" alt="{E(alt)}" loading="lazy">')


def stretch_scores():
    s = C['stretch']
    cd = ''.join(f'<td class="n">{v}</td>' for v in s['cd_scores'])
    first = ''.join(f'<td class="n">{v}</td>' for v in C.get('cd_first', []))
    head = ''.join(f'<th scope="col">{h}</th>' for h in RUBRIC)
    rv = C.get('reviewer', {})
    rvt = ''.join(f'<li><b>{E(k)}:</b> {E(v)}</li>' for k, v in rv.items())
    return (f'<div class="tw" role="region" tabindex="0" aria-label="Scores for the stretch test"><table class="sc">'
            f'<caption>The creative director’s scores, 1 to 5, ship line 4 on every line, after the fix pass and on the first build.</caption>'
            f'<thead><tr><th scope="col">Page</th>{head}<th scope="col">Ships</th></tr></thead>'
            f'<tbody><tr><th scope="row">After the fix pass</th>{cd}<td>{E(s["ships"])}</td></tr>'
            f'<tr><th scope="row">First build</th>{first}<td>No</td></tr></tbody></table></div>'
            + (f'<h4>The statistics and nonpartisanship review</h4><ul class="facts">{rvt}</ul>' if rvt else ''))


def chart_band(sid):
    ch = C['stretch']['charts'][sid]
    proves = ''.join(f'<li>{E(x)}</li>' for x in ch.get('proves', []))
    needs = ''.join(f'<li>{E(x)}</li>' for x in ch.get('needs', []))
    return f'''<article class="sb" id="{sid.lower()}" aria-labelledby="{sid.lower()}-h">
<div class="sb-h"><p class="secnum">{sid} · {E(ch["form"]).upper()}</p><h3 id="{sid.lower()}-h">{E(ch["question"])}</h3></div>
<div class="sb-g"><figure class="shot big">{img(f"newsprint-{sid}.jpg", f"{sid}, {ch['form']}, on Newsprint at 1440 px: {ch['title']}")}
<figcaption>Desktop, on Newsprint.</figcaption></figure>
<div class="sb-side"><figure class="shot ph">{img(f"phone-{sid}.jpg", f"{sid} on a phone at 390 px", 780)}<figcaption>Phone, 390 px.</figcaption></figure>
<h4>What it proves</h4><ul class="facts">{proves}</ul>{f'<h4>What still needs work</h4><ul class="facts">{needs}</ul>' if needs else ''}</div></div></article>'''


# ------------------------------------------------------------------------------------------------ page
CSS = '''
/* Board 4. The same frame as Board 3: one 1280 px column on Newsprint, the work first, a Prussian decision band.
   The coverage map is the board's one drawing: 122 squares in the tier code the tables repeat. */
:root{color-scheme:light;--bg:#DCD9D2;--surface:#E6E3DD;--white:#FFFFFF;--fg:#121212;--muted:#45494F;--rule:#5D636D;
--stone:#5D636D;--hair:#C9C6BF;--prussian:#1F2D5A;--newsprint:#DCD9D2;--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;
--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif;--u:15px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1rem/1.6 var(--body)}
a{color:inherit;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.board{max-width:1280px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--fg);padding-bottom:14px;flex-wrap:wrap}
.mast b{font:800 1.25rem/1 var(--display);letter-spacing:-.02em}.mast span{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.eyebrow{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:28px 0 0}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.025em;text-wrap:balance;margin:0}
h1{font-size:clamp(2.25rem,6vw,4.25rem);line-height:1.02;margin-top:10px;max-width:17ch}
h2{font-size:clamp(1.5rem,3vw,2.25rem);line-height:1.08;margin:0 0 12px}
h3{font-size:1.375rem;line-height:1.2;letter-spacing:-.015em}
h4{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px}
p{margin:0 0 12px;max-width:72ch}.deck{font-size:1.1875rem;line-height:1.5;max-width:64ch;margin-top:16px}
section{border-top:1px solid var(--rule);margin-top:48px;padding-top:32px}
.secnum{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.ask{background:var(--white);border:1px solid var(--rule);padding:22px 24px;margin-top:28px}
.ask ol{margin:0;padding-left:1.3em}.ask li{margin:0 0 8px;max-width:84ch}.reply{font:italic 400 1.0625rem/1.5 var(--quote);margin:10px 0 0}
.toc{display:flex;flex-wrap:wrap;gap:6px 22px;margin:22px 0 0;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}.toc a:hover{text-decoration:underline}
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--white)}
table{border-collapse:collapse;width:100%;font-size:.9375rem;font-variant-numeric:tabular-nums}
caption{caption-side:bottom;text-align:left;padding:8px 12px;font-size:.875rem;color:var(--muted)}
th,td{text-align:left;vertical-align:top;padding:10px 9px;border-bottom:1px solid var(--hair)}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.02em;text-transform:uppercase;color:var(--muted);background:var(--surface)}
table.sc{min-width:760px}td.n{text-align:center}
table.ft{min-width:900px}table.ft tbody th{font-weight:600;width:19%}table.ft td:nth-child(2){width:11%;white-space:nowrap}
table.ft td:nth-child(3){width:28%}table.ft td:nth-child(4){width:24%}
.shot{margin:0}.shot img{max-width:100%;height:auto;display:block;border:1px solid var(--rule);background:var(--bg)}
figcaption{font-size:.875rem;line-height:1.45;color:var(--muted);margin-top:6px}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:70ch}
.decision{background:var(--prussian);color:var(--newsprint);padding-block:28px;padding-left:max(20px,3vw);padding-right:max(20px,3vw);margin-top:48px}
.decision *{color:inherit}.decision h2,.decision h3{color:#FFFFFF}.decision ol{padding-left:1.3em;margin:0}.decision li{margin:0 0 16px;max-width:88ch}
.decision .rec{display:block;margin-top:4px;font-weight:700}.decision h3{margin:28px 0 12px;font-size:1.25rem}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:28px}
.small{font-size:.875rem;color:var(--muted)}
.open{font:700 1rem/1.3 var(--body);display:inline-flex;align-items:center;min-height:44px;margin:0 0 12px}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.missing{border:1px dashed var(--rule);padding:16px;color:var(--muted)}
/* stretch bands */
.sb{border-top:2px solid var(--fg);margin-top:40px;padding-top:18px}
.sb-h h3{max-width:40ch}
.sb-g{display:grid;grid-template-columns:minmax(0,760px) minmax(0,1fr);gap:32px;align-items:start;margin-top:16px}
.sb-side{min-width:0}.shot.ph{max-width:390px}
.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:16px;align-items:start}
/* coverage map: tier code. Core solid Charcoal; extended outlined; reference Stone; avoid outlined and struck.
   A Newsprint dot (Charcoal on light squares) marks a form already drawn. */
.u{display:inline-block;width:var(--u);height:var(--u);flex:none;position:relative;vertical-align:-2px}
.u-core{background:var(--fg)}
.u-extended{background:var(--bg);box-shadow:inset 0 0 0 2px var(--fg)}
.u-reference{background:var(--stone)}
.u-avoid{background:linear-gradient(to top right,transparent calc(50% - 1px),var(--fg) calc(50% - 1px),var(--fg) calc(50% + 1px),transparent calc(50% + 1px)),var(--bg);box-shadow:inset 0 0 0 2px var(--fg)}
.u.drawn::after{content:"";position:absolute;left:50%;top:50%;width:5px;height:5px;margin:-2.5px 0 0 -2.5px;border-radius:50%;background:var(--bg)}
.u-extended.drawn::after{background:var(--fg)}
.umap{margin:24px 0 0;background:var(--white);border:1px solid var(--rule);padding:22px 24px}
.umap-h{font-size:.9375rem;line-height:1.5;color:var(--fg);margin:0 0 12px;max-width:80ch}
.ulegend{display:flex;flex-wrap:wrap;gap:8px 22px;list-style:none;margin:0 0 16px;padding:0 0 14px;border-bottom:1px solid var(--hair);font-size:.875rem}
.ulegend li{display:flex;align-items:center;gap:8px}
.urows{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 40px}
.urows li{display:grid;grid-template-columns:minmax(0,15em) minmax(0,1fr);gap:12px;align-items:center;border-bottom:1px solid var(--hair);padding:6px 0;min-height:44px}
.urows a{display:flex;justify-content:space-between;gap:8px;text-decoration:none;font-weight:600;font-size:.9375rem;min-height:32px;align-items:center}
.urows a:hover .un{text-decoration:underline}.uc{color:var(--muted);font-weight:400;font-variant-numeric:tabular-nums}
.us{display:flex;flex-wrap:wrap;gap:3px}
.tiers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:20px}
.tiers div{border-top:2px solid var(--fg);padding-top:10px}.tiers b{display:flex;align-items:center;gap:8px;font:800 1.125rem/1.2 var(--display)}
.tiers p{font-size:.9375rem;margin:6px 0 0}
ul.rules{columns:2;column-gap:40px;padding-left:1.1em;margin:0}ul.rules li{break-inside:avoid;margin:0 0 10px}
.fam{border-top:2px solid var(--fg);margin-top:36px;padding-top:16px}
.fam-h{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 24px;align-items:end;margin-bottom:12px}
.fam-h .secnum{grid-column:1/-1}.fam-h h3{grid-column:1}.fam-h .fq{grid-column:1;margin:4px 0 0;font-size:1.0625rem}
.fam-h .chips{grid-column:2;grid-row:2/4;margin:0;display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.tc{font:600 .8125rem/1.3 var(--body);border:1px solid var(--fg);padding:3px 8px;white-space:nowrap}.tc-core{background:var(--fg);color:var(--white)}
.tier{display:inline-flex;align-items:center;gap:8px;font-weight:600}
.st{display:inline-block;font-weight:600}.st-built,.st-stretch{border-bottom:2px solid var(--fg)}.st-rule,.st-sketch{color:var(--muted)}
.x{display:block;font-size:.875rem;color:var(--muted);margin-top:2px}
tr.k-built,tr.k-stretch{background:#F4F3F0}
.fnote{font-size:.9375rem;margin-top:10px}
ol.rounds{list-style:none;margin:16px 0 0;padding:0;counter-reset:r;display:grid;gap:0}
ol.rounds li{display:grid;grid-template-columns:4.5em minmax(0,1fr) minmax(0,16em);gap:20px;padding:14px 0;border-bottom:1px solid var(--rule)}
ol.rounds .rn{font:800 1.75rem/1 var(--display);letter-spacing:-.02em}ol.rounds .rn small{display:block;font:700 .75rem/1.4 var(--body);letter-spacing:.08em;color:var(--muted);text-transform:uppercase}
ol.rounds .rw{color:var(--muted);font-size:.9375rem}
@media (max-width:1000px){.sb-g{grid-template-columns:minmax(0,1fr)}.urows{grid-template-columns:minmax(0,1fr)}}
@media (max-width:900px){.pair,.tiers{grid-template-columns:minmax(0,1fr)}ul.rules{columns:1}
.fam-h{grid-template-columns:minmax(0,1fr)}.fam-h .chips{grid-column:1;grid-row:auto;justify-content:flex-start;margin-top:8px}
ol.rounds li{grid-template-columns:3.5em minmax(0,1fr)}ol.rounds .rw{grid-column:2}}
@media (max-width:520px){.urows li{grid-template-columns:minmax(0,1fr)}.umap{padding:16px}.ask{padding:18px 16px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''


def build():
    L = lambda k: ''.join(f'<li>{x}</li>' for x in C.get(k, []))
    s = C['stretch']
    ask = ''.join(f'<li>{E(x)}</li>' for x in C['ask'])
    decisions = ''.join(f'<li><b>{E(d["q"])}</b> {E(d["text"])}<span class="rec">Recommended: {E(d["rec"])}</span></li>' for d in C['decisions'])
    nextq = ''.join(f'<li><b>{E(d["q"])}</b> {E(d["text"])}<span class="rec">Recommended: {E(d["rec"])}</span></li>' for d in C.get('next_questions', []))
    tiers = ''.join(f'<div><b><span class="u u-{t.lower()}" aria-hidden="true"></span>{t}, {COUNT[t]}</b><p>{md(TIER_TEXT[t][0])}</p></div>' for t in TIERS)
    rules = ''.join(f'<li>{md(r)}</li>' for r in RULES)
    rounds = ''.join(f'<li><span class="rn"><small>Round</small>{E(r[0])}</span><span>{md(r[1])}</span><span class="rw">{E(r[2])}</span></li>' for r in ORDER)
    fams = ''.join(family_table(f) for f in FAMS)
    link = f'<a class="open" href="{E(PAGES["stretch"]["url"])}">Open the live stretch page</a>' if 'stretch' in PAGES else ''
    corr = ''.join(f'<li>{E(x)}</li>' for x in C.get('coverage', {}).get('corrections', []))
    dark = C['stretch'].get('dark', {})
    dark_specs = dark.get('specs', [])
    dark_figs = ''.join(f'<figure class="shot">{img(f"dark-{d}.jpg", f"{d} on Charcoal", 1440)}<figcaption>{d} on Charcoal.</figcaption></figure>' for d in dark_specs)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>Chapter 14 Coverage Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="board" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Brand Guide, Edition 06 · Phase 2 · Data visualization</span></div>
<p class="eyebrow">Board 4 · November 6, 2026</p>
<h1>Chapter 14, planned in full, and six charts that test the system</h1>
<p class="deck">{E(C["deck"])}</p>
<div class="ask"><h3>What you are asked</h3><ol>{ask}</ol>
<p class="reply">{E(C["sample_reply"])}</p></div>
<nav class="toc" aria-label="On this board"><a href="#stretch">The six charts</a><a href="#coverage">Coverage plan</a><a href="#families">The 16 families</a><a href="#order">Phase 3 build order</a><a href="#decisions">Decisions</a><a href="#next">Next stage</a><a href="#checks">Checks</a></nav>
</header>
<section id="stretch" aria-labelledby="h-stretch"><p class="secnum">THE STRETCH TEST</p><h2 id="h-stretch">Six new forms in the Explainer system</h2>
<p class="deck">{E(s["verdict"])}</p>{link}
{stretch_scores()}
{"".join(chart_band(x) for x in SPECS)}
<h3 style="margin-top:40px">On Charcoal</h3><p>{E(dark.get("text", ""))}</p><div class="pair">{dark_figs}</div>
</section>
<section id="coverage" aria-labelledby="h-cov"><p class="secnum">COVERAGE PLAN</p><h2 id="h-cov">Every way Oath &amp; Action shows data</h2>
<p class="deck">The plan lists {TOTAL} forms in 16 families. Each one says what Oath &amp; Action uses it for, names real data for its specimen and sets a tier. Chapter 14 is built from it at the start of Phase 3.</p>
<div class="tiers">{tiers}</div>
{unit_map()}
<h4>Rules that hold across every form</h4><ul class="rules">{rules}</ul>
{f'<h4>What the creative director changed in the plan</h4><ul class="facts">{corr}</ul>' if corr else ''}
</section>
<section id="families" aria-labelledby="h-fam"><p class="secnum">THE 16 FAMILIES</p><h2 id="h-fam">Each family opens with the question it answers</h2>
<p>Rows already drawn in the Explainer system are shaded and underlined. “Rule only” forms are named with the reason and the form to use instead. “Sketch and rule” forms get a small drawing and a rule that says when they are the right choice.</p>
{fams}</section>
<section id="order" aria-labelledby="h-order"><p class="secnum">PHASE 3 BUILD ORDER</p><h2 id="h-order">Six rounds, the chart kit first</h2>
<ol class="rounds">{rounds}</ol>
<p style="margin-top:16px">Each round runs the red team (statistics, civic education, accessibility, nonpartisanship, craft and production), a reader panel, one fix pass and the creative director’s scores. {E(BALANCE)}</p></section>
<div class="decision" id="decisions" role="region" aria-labelledby="h-dec"><h2 id="h-dec">Decisions on this board</h2><ol>{decisions}</ol>
<h3 id="next">Before the next stage</h3><p>After this board, the plan moves to the direction review’s open items and the rest of Phase 2 through Gate 2. These questions shape that work.</p><ol>{nextq}</ol></div>
<section id="process" aria-labelledby="h-proc"><p class="secnum">HOW THIS WAS MADE</p><h2 id="h-proc">One maker, two reviewers, one fix pass</h2><ol>{L("process")}</ol></section>
<section id="checks" aria-labelledby="h-checks"><p class="secnum">CHECKS</p><h2 id="h-checks">What was tested</h2>
<div class="cols"><div><h4>Tested</h4><ul class="facts">{L("tested")}</ul></div><div><h4>Not tested</h4><ul class="facts">{L("not_tested")}</ul></div></div></section>
<section id="changes" aria-labelledby="h-ch"><p class="secnum">CHANGE LOG</p><h2 id="h-ch">Files</h2>
<p class="small">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>. Nothing in <code>source/</code>, the Civic Line icons, the identity masters, the atlas pick or the three concept pages changed.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts">{L("changelog_created")}</ul></div><div><h4>Modified</h4><ul class="facts">{L("changelog_modified")}</ul></div></div></section>
<p class="small" style="margin-top:40px">{E(C.get("data_line", ""))}</p>
</main></body></html>'''
    assert '—' not in re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S), 'em dash on the board'
    OUT.write_text(page)
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace('<title>Chapter 14 Coverage Board</title>\n', '')
    PUB.parent.mkdir(parents=True, exist_ok=True)
    PUB.write_text('<title>Chapter 14 Coverage Board</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + re.sub(r'</body>\s*</html>\s*$', '', body))
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1e6:.1f} MB', 'and', PUB)


if __name__ == '__main__':
    build()
