"""Chat 10's progress page (DR-303): the platform specifications, the application kit's three studio samples and the
re-sized Phase 4 allocations, with chapter 16's rule list. It asks Dustin for no decision.

Usage, from the project folder:
  python3 -I work/build/scripts/phase-4/chat_10_progress_build.py [--guide-url URL]

Reads work/research/20261121_Platform-Specifications.json, work/build/scripts/phase-3/guide_charts.py's allocations,
work/build/guide/chapters/16-photography.json and the exports in work/build/exports/phase-4/. Writes
work/boards/phase-4/chat-10/20261121_Chat-10-Progress.html and its img/ folder.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / 'work/boards/phase-4/chat-10'
IMG = OUT / 'img'
EXP = ROOT / 'work/build/exports/phase-4'
SPECS = json.loads((ROOT / 'work/research/20261121_Platform-Specifications.json').read_text())
CH16 = json.loads((ROOT / 'work/build/guide/chapters/16-photography.json').read_text())
CHARTS = (ROOT / 'work/build/scripts/phase-3/guide_charts.py').read_text()
GUIDE_URL = sys.argv[sys.argv.index('--guide-url') + 1] if '--guide-url' in sys.argv else 'https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF'

e = html.escape


def alloc(name):
    m = re.search(name + r'\s*=\s*\{(.*?)\}', CHARTS, re.S)
    return {k: int(v.replace('_', '')) for k, v in re.findall(r'"(\d\d)":\s*([\d_]+)', m.group(1))}


NEW, OLD = alloc('PHASE_4_ALLOCATION'), alloc('PHASE_4_GATE_3')
CHAPTERS = {'16': 'Photography, illustration and video', '20': 'Web', '21': 'The atlas', '22': 'Newsletter and email',
            '23': 'Social and video', '24': 'Reports', '25': 'Print and presentation'}
CHANNELS = [('website', 'Oath & Action website'), ('substack', 'Substack'), ('email', 'Email'), ('x', 'X (Twitter)'),
            ('threads', 'Threads'), ('instagram', 'Instagram'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'),
            ('linkedin', 'LinkedIn'), ('video', 'Video frames'), ('print', 'Print'), ('slides', 'Slides')]
STATUS = {'read': ('Read', 'st-read'), 'search-result': ('Search result', 'st-search'),
          'not-found': ('No official source', 'st-none')}

PICS = {
    'post': '20261121_Studio-Sample-Instagram-Portrait-1080x1350.png',
    'report': '20261121_Studio-Sample-Report-Page-03-Letter-Proof-96ppi.png',
    'a1440l': '20261121_Studio-Sample-Article-1440-Light.png',
    'a1440d': '20261121_Studio-Sample-Article-1440-Dark.png',
    'a390l': '20261121_Studio-Sample-Article-390-Light.png',
    'a390d': '20261121_Studio-Sample-Article-390-Dark.png',
}


def size(r):
    if r.get('width') and r.get('height'):
        u = ' in' if r.get('unit') == 'in' else ' px'
        w, h = r['width'], r['height']
        fmt = (lambda v: f'{v:g}') if r.get('unit') == 'in' else (lambda v: f'{v:,}')
        return f'{fmt(w)} x {fmt(h)}{u}'
    return r.get('aspect') or 'Not stated'


def spec_tables():
    out = []
    rows = SPECS['rows']
    seen = set()
    groups = []
    for key, name in CHANNELS:
        rs = [r for r in rows if r['channel'] == key]
        if rs:
            groups.append((name, rs))
            seen.update(id(r) for r in rs)
    rest = [r for r in rows if id(r) not in seen]
    if rest:
        groups.append(('Other', rest))
    for name, rs in groups:
        body = ''.join(
            f'<tr><td>{e(re.sub(r"`", "", r["application"]))}</td><td class="num">{e(size(r))}</td>'
            f'<td><span class="st {STATUS.get(r["status"], ("?", ""))[1]}">{STATUS.get(r["status"], (r["status"], ""))[0]}</span></td></tr>'
            for r in rs)
        out.append(f'<details class="spec"><summary><span>{e(name)}</span><span class="count">{len(rs)} rows</span></summary>'
                   f'<div class="tablewrap"><table><thead><tr><th scope="col">Application</th><th scope="col">Size</th>'
                   f'<th scope="col">Source</th></tr></thead><tbody>{body}</tbody></table></div></details>')
    return '\n'.join(out)


def counts():
    c = {}
    for r in SPECS['rows']:
        c[r['status']] = c.get(r['status'], 0) + 1
    return c


def alloc_table():
    body = ''
    for n, name in CHAPTERS.items():
        d = NEW[n] - OLD[n]
        ch = '0' if d == 0 else (f'+{d:,}' if d > 0 else f'minus {abs(d):,}')
        body += f'<tr><th scope="row">{n} {e(name)}</th><td class="num">{OLD[n]:,}</td><td class="num">{NEW[n]:,}</td><td class="num">{ch}</td></tr>'
    t_old, t_new = sum(OLD.values()), sum(NEW.values())
    body += (f'<tr class="total"><th scope="row">All seven</th><td class="num">{t_old:,}</td><td class="num">{t_new:,}</td>'
             f'<td class="num">+{t_new - t_old:,}</td></tr>')
    return body


def rules16():
    items = ''
    order = [r['id'] for r in CH16['rules']]
    groups = CH16.get('groups', [])
    starts = [order.index(g['before_rule']) for g in groups if g.get('before_rule') in order]
    for i, g in enumerate(groups):
        if g.get('before_rule') not in order:
            continue
        a = starts[i]
        b = starts[i + 1] if i + 1 < len(starts) else len(order)
        title = g.get('title') or ''
        rs = CH16['rules'][a:b]
        if not rs:
            continue
        lis = ''.join(f'<li><span class="rid">{e(r["id"])}</span> {e(r["title"])}</li>' for r in rs)
        items += f'<div class="rgroup"><h4>{e(title)}</h4><ol>{lis}</ol></div>'
    if not items:
        lis = ''.join(f'<li><span class="rid">{e(r["id"])}</span> {e(r["title"])}</li>' for r in CH16['rules'])
        items = f'<div class="rgroup"><ol>{lis}</ol></div>'
    return items


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if IMG.exists():
        shutil.rmtree(IMG)
    IMG.mkdir()
    for k, f in PICS.items():
        shutil.copyfile(EXP / f, IMG / f)
    c = counts()
    total = len(SPECS['rows'])
    page = TEMPLATE
    rep = {
        '{{GUIDE_URL}}': GUIDE_URL,
        '{{SPEC_TABLES}}': spec_tables(),
        '{{N_TOTAL}}': str(total), '{{N_READ}}': str(c.get('read', 0)),
        '{{N_SEARCH}}': str(c.get('search-result', 0)), '{{N_NONE}}': str(c.get('not-found', 0)),
        '{{ALLOC_ROWS}}': alloc_table(),
        '{{RULES16}}': rules16(), '{{N16}}': str(len(CH16['rules'])),
    }
    for k, v in PICS.items():
        rep['{{IMG_' + k + '}}'] = 'img/' + v
    for k, v in rep.items():
        page = page.replace(k, v)
    left = re.findall(r'\{\{[A-Z0-9_a-z]+\}\}', page)
    if left:
        sys.exit(f'unfilled: {left}')
    if '—' in page or '–' in page:
        sys.exit('an em or en dash is on the page')
    (OUT / '20261121_Chat-10-Progress.html').write_text(page)
    print('wrote', OUT / '20261121_Chat-10-Progress.html', len(page.encode()), 'bytes;', len(PICS), 'pictures')


TEMPLATE = r'''<title>Phase 4, Chat 10</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap">
<style>
/* Layout: one reading column on the brand's Newsprint, wide plates break out for the samples. Tokens are the guide's own. */
:root {
  --ground: #DCD9D2;      /* oa.color.palette.newsprint */
  --ink: #121212;         /* oa.color.palette.charcoal */
  --quiet: #4E535B;       /* oa.color.derived.deep-stone */
  --rule: #5D636D;        /* oa.color.palette.stone */
  --panel: #1F2D5A;       /* oa.color.palette.prussian */
  --on-panel: #FFFFFF;
  --red: #E63946;         /* oa.color.palette.pillar-red, the ampersand only */
  --good: #4A7C74;        /* oa.color.palette.verdigris */
  --card: #E7E5E0;
  --focus: #4A7C74;
  --display: "Inter Tight", "Inter", system-ui, sans-serif;
  --text: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --ground: #121212; --ink: #DCD9D2; --quiet: #A3A19C; --rule: #828A9D; --panel: #1F2D5A; --on-panel: #FFFFFF;
  --red: #E63946; --good: #7FB3A9; --card: #232426; --focus: #7FB3A9; color-scheme: dark } }
:root[data-theme="dark"] {
  --ground: #121212; --ink: #DCD9D2; --quiet: #A3A19C; --rule: #828A9D; --panel: #1F2D5A; --on-panel: #FFFFFF;
  --red: #E63946; --good: #7FB3A9; --card: #232426; --focus: #7FB3A9; color-scheme: dark }
body { background: var(--ground); color: var(--ink); font: 400 16px/1.55 var(--text); }
.wrap { max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 40px 80px; }
.col { max-width: 44rem; }
a { color: inherit; text-underline-offset: 3px; }
a:focus-visible, summary:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.mast { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 24px;
  border-bottom: 1px solid var(--rule); padding-bottom: 12px; }
.word { font: 800 22px/1 var(--display); letter-spacing: -0.01em; }
.word .amp { color: var(--red); }
.kick { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); }
h1 { font: 800 clamp(34px, 6vw, 56px)/1.04 var(--display); letter-spacing: -0.02em; margin: 40px 0 16px; text-wrap: balance; }
h2 { font: 800 clamp(24px, 3.4vw, 32px)/1.1 var(--display); letter-spacing: -0.01em; margin: 64px 0 12px; text-wrap: balance; }
h3 { font: 700 18px/1.3 var(--text); margin: 28px 0 8px; }
h4 { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin: 0 0 8px; }
p { margin: 0 0 12px; }
.lede { font-size: 19px; line-height: 1.5; }
.note { font-size: 14px; color: var(--quiet); }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 24px 0; }
.fact { border-top: 3px solid var(--ink); padding-top: 10px; min-width: 0; }
.fact b { display: block; font: 800 32px/1.05 var(--display); font-variant-numeric: tabular-nums; }
.fact span { font-size: 14px; color: var(--quiet); }
.samples { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; align-items: start; margin-top: 24px; }
figure { margin: 0; min-width: 0; }
figure img { display: block; width: 100%; height: auto; border: 1px solid var(--rule); background: #DCD9D2; }
figcaption { font-size: 14px; color: var(--quiet); margin-top: 8px; }
.label { display: inline-block; font: 700 12px/1 var(--text); letter-spacing: 0.06em; text-transform: uppercase;
  border: 1px solid currentColor; padding: 3px 6px; margin-right: 6px; color: var(--ink); }
.phones { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.scroll { max-height: 720px; overflow-y: auto; border: 1px solid var(--rule); }
.scroll img { border: 0; }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
th, td { text-align: left; padding: 8px 12px 8px 0; border-bottom: 1px solid color-mix(in srgb, var(--rule) 45%, transparent); vertical-align: top; }
thead th { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); border-bottom: 1px solid var(--rule); }
td.num, th.num { font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }
.alloc td.num { padding-right: 0; padding-left: 16px; }
.alloc tbody th { font-weight: 600; }
tr.total th, tr.total td { font-weight: 700; border-top: 2px solid var(--ink); }
details.spec { border-top: 1px solid var(--rule); }
details.spec:last-of-type { border-bottom: 1px solid var(--rule); }
details.spec summary { cursor: pointer; display: flex; justify-content: space-between; gap: 16px; padding: 12px 0; font-weight: 700; }
details.spec summary .count { font-weight: 400; color: var(--quiet); font-size: 14px; }
details.spec table { margin-bottom: 16px; }
.st { font: 600 12px/1 var(--text); padding: 3px 6px; border: 1px solid currentColor; white-space: nowrap; }
.st-read { color: var(--good); }
.st-search { color: var(--ink); border-style: dashed; }
.st-none { color: var(--quiet); border-style: dotted; }
.panel { background: var(--panel); color: var(--on-panel); padding: 24px; margin-top: 24px; }
.panel h3 { margin-top: 0; }
.panel a { color: var(--on-panel); }
.rules16 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; margin-top: 16px; }
.rgroup ol { list-style: none; padding: 0; margin: 0; display: grid; gap: 6px; }
.rid { font-weight: 700; font-variant-numeric: tabular-nums; margin-right: 4px; }
ul.plain { padding-left: 20px; margin: 0 0 12px; }
ul.plain li { margin-bottom: 6px; }
.twocol { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }
</style>
<div class="wrap">
  <header class="mast">
    <span class="word" aria-label="Oath &amp; Action">OATH<span class="amp">&amp;</span>ACTION</span>
    <span class="kick">Edition 06, Phase 4 progress, November 21, 2026</span>
  </header>

  <main>
  <div class="col">
    <p class="kick" style="margin-top:40px">Chat 10 of Phase 4</p>
    <h1>Specifications read, the application kit drawing, chapter 16 built</h1>
    <p class="lede">This page shows what Phase 4's first chat made. It asks you for no decision. The two items that need your word are in the chat, and the items held for Phase 4 board 1 are listed at the end.</p>
  </div>

  <div class="facts" role="list">
    <div class="fact" role="listitem"><b>{{N_TOTAL}}</b><span>platform specification rows, {{N_READ}} read on the platforms&#8217; own pages</span></div>
    <div class="fact" role="listitem"><b>11 of 11</b><span>kit exports at their exact sizes, by the size check</span></div>
    <div class="fact" role="listitem"><b>{{N16}}</b><span>rules in chapter 16, with 28 plates</span></div>
    <div class="fact" role="listitem"><b>265,941</b><span>bytes of reserve under the page&#8217;s 16 MB, projected</span></div>
  </div>

  <section aria-labelledby="h-samples">
    <h2 id="h-samples">The application kit&#8217;s three studio samples</h2>
    <div class="col">
      <p>The application kit draws each Phase 4 application from a small content file, at build time, in the guide&#8217;s own fonts and tokens. These three samples measure what an application costs the page, and they set the kit&#8217;s first patterns. Each is labeled a studio sample. The website&#8217;s own masthead is chapter 20&#8217;s work in chat 11, so the article carries a provisional header.</p>
    </div>
    <div class="samples">
      <figure>
        <img src="{{IMG_post}}" width="1080" height="1350" loading="lazy" alt="Studio sample, Instagram portrait post. An Explainer card on public records. Headline: The records law and your answer, with the red ampersand. The figure 20, working days for a federal agency to decide on your records request under the Freedom of Information Act; unusual circumstances can add up to 10 more. A Charcoal band at the foot holds the source line, the Freedom of Information Act, 5 U.S.C. 552(a)(6), retrieved November 12, 2026, and the lockmark sign-off.">
        <figcaption><span class="label">Studio sample</span>Instagram portrait, 1080 x 1350 px, shown here at about a third of its size. The source line and the 96 px sign-off sit on a Charcoal band.</figcaption>
      </figure>
      <figure>
        <img src="{{IMG_report}}" width="840" height="1080" loading="lazy" alt="Studio sample, report page 3, the executive summary, on US Letter with bleed. Headline: A useful question has a clear address. Three figures down the right, 100 units allocated, 40 units for public hours and 4 handoffs to a published answer, each labeled Illustrative. Sections: The allocation, The decision, The household perspective. A source line at the foot, labeled Illustrative.">
        <figcaption><span class="label">Studio sample</span>Report page 3, US Letter with 0.125 in bleed, at 96 pixels to the inch. Its figures are Illustrative until chat 15 checks each one (P4-4); four of its paragraphs are the studio&#8217;s, to be replaced with V5&#8217;s own words in chat 15.</figcaption>
      </figure>
    </div>

    <h3>The article page, at 1440 px and at 390 px, light and dark</h3>
    <div class="col"><p>An Explainer on special districts with chart S86, built from the tokens, chapter 07&#8217;s grid and chapter 18&#8217;s components, with the theme switch you approved (DR-204). The definition was checked against the Census Bureau&#8217;s glossary today. Scroll inside each frame to read the page.</p></div>
    <div class="samples">
      <figure>
        <div class="scroll" tabindex="0" role="region" aria-label="Article sample at 1440 px, light"><img src="{{IMG_a1440l}}" width="1440" height="2573" loading="lazy" alt="Studio sample, the article page at 1440 px on Newsprint: a provisional header with the wordmark and the theme switch, the kicker Explainer, Local government, the headline What a special district does, a standfirst defining a special district, the byline Dustin Cathcart, Founder and Editor, November 21, 2026, a section on how the Census Bureau counts them, and chart S86, special districts as the most common kind of government in 2022, 39,555 of 90,888."></div>
        <figcaption>1440 px, Newsprint.</figcaption>
      </figure>
      <figure>
        <div class="scroll" tabindex="0" role="region" aria-label="Article sample at 1440 px, dark"><img src="{{IMG_a1440d}}" width="1440" height="2573" loading="lazy" alt="Studio sample, the same article page at 1440 px in the dark mode, on Charcoal, with the switch set to Dark."></div>
        <figcaption>1440 px, the dark mode.</figcaption>
      </figure>
    </div>
    <div class="phones" style="margin-top:24px">
      <figure>
        <div class="scroll" tabindex="0" role="region" aria-label="Article sample at 390 px, light"><img src="{{IMG_a390l}}" width="390" height="3394" loading="lazy" alt="Studio sample, the article page at 390 px on Newsprint, the same content in one column."></div>
        <figcaption>390 px, Newsprint.</figcaption>
      </figure>
      <figure>
        <div class="scroll" tabindex="0" role="region" aria-label="Article sample at 390 px, dark"><img src="{{IMG_a390d}}" width="390" height="3394" loading="lazy" alt="Studio sample, the article page at 390 px in the dark mode."></div>
        <figcaption>390 px, the dark mode.</figcaption>
      </figure>
    </div>

    <div class="twocol" style="margin-top:32px">
      <div>
        <h3>What the checks found</h3>
        <ul class="plain">
          <li>Every export matches its size in the specifications table, 11 of 11.</li>
          <li>The article passes axe with 0 violations at 1440, 1024, 390 and 360 px in both themes; the theme holds after a reload and the page reflows at 320 px and at 200 percent text.</li>
          <li>Text pairs measure 13.29, 7.26 and 5.49 to 1 on the pixels. The red ampersand measures 2.96 to 1 on Newsprint; chat 12&#8217;s accessibility review rules whether the logo exception covers it.</li>
          <li>The post passes the feed test at 432 and 360 px.</li>
        </ul>
      </div>
      <div>
        <h3>What still fails</h3>
        <ul class="plain">
          <li>The article&#8217;s light captures are 88.2 percent Newsprint at 1440 px and 85.9 at 1024, past Rule 05.1&#8217;s 85. The open margins of a wide reading page drive it. How Rule 05.1 reads on a long page goes to chapter 20 in chat 11.</li>
          <li>The report page&#8217;s PDF carries Inter as Type 3 fonts, which some print shops refuse. Chapter 25&#8217;s print preflight settles the fonts in chat 15.</li>
        </ul>
      </div>
    </div>
  </section>

  <section aria-labelledby="h-bytes">
    <h2 id="h-bytes">Measured bytes and the re-sized allocations</h2>
    <div class="col">
      <p>Placed in the guide with their frames, the post weighs 11,696 bytes, the article at four widths in two themes 187,145, and the report page 11,355. Counting what each chapter will draw at those prices re-sizes the seven Phase 4 chapters. Chapters 20 and 21 grow, since a whole web page costs about 21,500 bytes a frame; chapters 24 and 25 shrink.</p>
    </div>
    <div class="tablewrap">
      <table class="alloc">
        <thead><tr><th scope="col">Chapter</th><th scope="col" class="num">Gate 3, bytes</th><th scope="col" class="num">Re-sized, bytes</th><th scope="col" class="num">Change</th></tr></thead>
        <tbody>{{ALLOC_ROWS}}</tbody>
      </table>
    </div>
    <p class="note" style="margin-top:12px">The page projects to 15,734,059 bytes with every chapter at its figure: 265,941 under 16 MB and 234,059 past the 15.5 MB line, which the build prints as an early warning and does not stop on, as the Gate 3 report has it (DR-271). Each allocation moves as its content needs. The report reader&#8217;s controls are counted at 10,000 bytes, assumed and not yet measured.</p>
  </section>

  <section aria-labelledby="h-specs">
    <h2 id="h-specs">Platform specifications for the eight channels</h2>
    <div class="col">
      <p>The research lead read each platform&#8217;s official help page today and recorded each size with its page and the date: {{N_READ}} rows read on the page, {{N_SEARCH}} from the official domain&#8217;s search result where the page refuses an automated reader (X and Instagram), and {{N_NONE}} with no official source, most of them sizes the studio sets itself. Before chat 13 builds X and Instagram, a person in a browser confirms the search-result rows.</p>
      <h3>Changes from the Gate 3 report&#8217;s starting sizes</h3>
      <ul class="plain">
        <li>YouTube now recommends thumbnails at 3840 x 2160, with 640 px the narrowest it takes; its banner&#8217;s safe area is 1235 x 338 at 2048 x 1152.</li>
        <li>LinkedIn&#8217;s company page cover reads 1512 x 256 on LinkedIn&#8217;s page today, and 400 x 400 is the avatar&#8217;s smallest.</li>
        <li>Instagram&#8217;s two help texts disagree on 3:4 posts at 1080 x 1440, so posts stay 1080 x 1350 with their words inside a centered 3:4 crop.</li>
        <li>X shows one image whole from 2:1 to 3:4, and its ordinary link card is 2:1; the 1200 x 628 figure comes from its ads pages.</li>
      </ul>
    </div>
    {{SPEC_TABLES}}
  </section>

  <section aria-labelledby="h-ch16">
    <h2 id="h-ch16">Chapter 16, photography, illustration and video</h2>
    <div class="col">
      <p>Chapter 16 teaches on the two federal photographs chapter 01 already shows, the Capitol Rotunda and the public meeting at Lake Isabella, drawn from one copy the page now embeds once (P4-5). That freed 190,804 bytes, and chapter 01&#8217;s plates match their earlier captures pixel for pixel at four widths. Placeholders announce themselves as placeholders, and the rule on generated images shows its label on a placeholder, with no generated image. The four video rules meet WCAG&#8217;s media criteria 1.2.1 to 1.2.5. You will see the chapter whole on the chapters page and review it on Phase 4 board 1.</p>
    </div>
    <div class="rules16">{{RULES16}}</div>
    <div class="panel">
      <h3>Read it on the chapters page</h3>
      <p>The chapters page carries chapter 16 and Gate 3&#8217;s word changes: <a href="{{GUIDE_URL}}">open the chapters page</a>.</p>
    </div>
  </section>

  <section aria-labelledby="h-also">
    <h2 id="h-also">Also done, and what waits</h2>
    <div class="twocol">
      <div>
        <h3>Done this chat</h3>
        <ul class="plain">
          <li>Gate 3&#8217;s word changes (a) and (b), built as approved. Change (c) is built as approved, and its fix waits for your answer in the chat.</li>
          <li>The label clearance check is on for every chart (G3-05). All 376 chart drawings hash the same as before, by the engineer&#8217;s comparison.</li>
          <li>Each Phase 4 chapter now reports its bytes against its own allocation in every build.</li>
        </ul>
      </div>
      <div>
        <h3>Held for Phase 4 board 1</h3>
        <ul class="plain">
          <li>Chapter 01&#8217;s photograph plates show color, while Gate 1 set black and white as the default with color where color is evidence (S10). The creative director recommends the same grayscale there, at no byte cost.</li>
          <li>How Rule 05.1&#8217;s color share applies to a long reading page.</li>
          <li>Whether to commission photographs stays your open question (Q-04).</li>
        </ul>
      </div>
    </div>
    <p class="note">Tested in Chromium only. Not tested: Safari, Firefox, a screen reader, and print shops&#8217; preflight of the PDF.</p>
  </section>
  </main>
</div>
'''

if __name__ == '__main__':
    main()
