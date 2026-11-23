"""Chat 11c's progress board (DR-322): chapter 21, the atlas, as the application kit drew it. The four views at 1440 and
390 px in the light and dark themes, the loop index and How to read, Rule 05.1 by screen (contract C5), the atlas test's
report, the answers applied this chat, the page's weight and what was and was not tested. It asks Dustin for no decision.
Built by the main session from the kit's exports, with no extra agent (DR-322).

Usage, from the project folder:
  python3 -I work/build/scripts/phase-4/chat_11c_progress_build.py --report <strict build report JSON>
      [--quick-check TEXT] [--guide-url URL]

Reads the atlas exports in work/build/exports/phase-4/ (20261122_Atlas-*), the kit's plates
work/build/app-kit/plates/a11.json to a20.json (each view's `screens`, contract C5) and atlas-test.json, chapter 21's
JSON for its rule and specimen counts, and the strict build's report for the bytes. Writes
work/boards/phase-4/chat-11c/20261123_Chat-11c-Progress.html and its img/ folder (WebP: each view's first screen and
whole page).
"""
import html
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = Path.cwd()
OUT = ROOT / 'work/boards/phase-4/chat-11c'
IMG = OUT / 'img'
PAGE = OUT / '20261123_Chat-11c-Progress.html'
EXP = ROOT / 'work/build/exports/phase-4'
PLATES = ROOT / 'work/build/app-kit/plates'
CH21 = json.loads((ROOT / 'work/build/guide/chapters/21-atlas.json').read_text())


def arg(name, default=''):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


REPORT = json.loads(Path(arg('--report')).read_text())
QUICK = arg('--quick-check', 'Quick guide check at 1440 and 390 px: result to come.')
GUIDE_URL = arg('--guide-url')
VH = {1440: 900, 390: 844}
Q_FIRST, Q_FULL = 90, 82
e = html.escape
WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def n(x):
    return WORDS[x] if 0 <= x < 10 else f'{x:,}'


VIEWS = [
    ('home', 'A11', 'Atlas-Home-Page', 'The atlas home',
     'The whole system drawn as eight parts with a count on every flow, and the question “Why can the same care '
     'produce different bills?” pressed, which lights the three parts it reaches.'),
    ('reform', 'A12', 'Atlas-Reform-R-23-Page', 'Reform R-23',
     'A minimum wage that rises with an index: its two targets in red, the other reforms at the same mark in ink, its '
     'two grades apart, its four effects one to a row, and its routes with their check dates.'),
    ('register', 'A13', 'Atlas-Register-D04-Page', 'The Register, sheet D04',
     'The index of twelve sheets with each grade counted in words, then sheet D04 open: its ten connections one to a '
     'row, the rejected option, and its issue records filtered to Variable D4.'),
    ('loop', 'A14', 'Atlas-Loop-R18-Page', 'Loop R18',
     'Weakening watchdogs: the grade line, the signs read aloud, the two-step drawing with its weakest step, the '
     'stepper, and Reform R-11 chosen, with its three targets in red.'),
]
EXTRAS = [
    ('index', 'A15', 'Atlas-Loop-Index-Page', 'The loop index',
     'All 23 loops by kind, closure and grade, titles as the atlas stores them, with DR-321’s note under the index.'),
    ('read', 'A16', 'Atlas-How-To-Read-Page', 'How to read',
     'Every mark the atlas’s pages use, each with its words.'),
]


def webp(src, dst, crop_h=None, q=Q_FULL, scale=None):
    im = Image.open(src).convert('RGB')
    if crop_h:
        im = im.crop((0, 0, im.width, min(crop_h, im.height)))
    if scale and im.width > scale:
        im = im.resize((scale, round(im.height * scale / im.width)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=q, method=6)
    return im.size


def screens(aid):
    p = PLATES / f'{aid.lower()}.json'
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    out = {}
    for v in d.get('views', []):
        if v.get('screens') and v.get('theme') == 'light' and '-' in v.get('key', '') and v['key'].count('-') == 1:
            out[v['key']] = v['screens']
    return out


def test_table():
    t = json.loads((PLATES / 'atlas-test.json').read_text())
    by = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    names = {}
    for line in t['lines']:
        m = re.match(r'(PASS|FAIL) (T\d+) (A\d+) [^:]+: ([^,]+)', line)
        if not m:
            continue
        ok, check, aid, name = m.groups()
        names[check] = name
        by[check][aid][0 if ok == 'PASS' else 1] += 1
    return t, by, names


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    IMG.mkdir(parents=True)
    w = REPORT['weight']
    ch = w['chapters']
    c21 = ch.get('21', {}).get('bytes', 0)
    proj = w['projection']['projected_bytes']
    page = REPORT['bytes']
    limit = w['limit']
    rules = sum(len(g.get('rules', [])) for g in CH21.get('groups', [])) if CH21.get('groups') else None

    parts = []
    P = parts.append
    P('<title>Phase 4, Chat 11c</title>\n<meta name="claude:viewport-fit-sides" content="cover">')
    P('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    P('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@700;800&display=swap">')
    P(STYLE)
    P('<div class="wrap">')
    P('<header class="mast"><span class="word">OATH <span class="amp">&amp;</span> ACTION</span>'
      '<span class="kick">Edition 06 · Phase 4 · Chat 11c · November 23, 2026</span></header>')
    P('<main>')
    P('<h1>Chapter 21, the atlas, as built</h1>')
    P('<div class="col"><p class="lede">Our systems atlas, Who Do They Answer To?, now sits inside our website, under the '
      'site’s masthead with a title bar of its own. The application kit draws its four kinds of page from the atlas model '
      'alone, and the atlas test holds every page to the model before it ships. Nothing here asks you for a decision. The '
      'review, the creative director’s wall test and the keyboard walks come in chat 12, and the choices go to Phase 4 '
      'board 1.</p></div>')
    t, by, names = test_table()
    total_pass = sum(v[0] for c in by.values() for v in c.values())
    total_fail = sum(v[1] for c in by.values() for v in c.values())
    P('<div class="facts">')
    P(f'<div class="fact"><b>{len(VIEWS) * 4}</b><span>frames: {n(len(VIEWS))} views, each at 1440 and 390 px, light and dark</span></div>')
    P(f'<div class="fact"><b>{total_pass:,}</b><span>atlas test checks passed, {total_fail:,} failed; self-test {e(t["self_test"])}</span></div>')
    P(f'<div class="fact"><b>{c21:,}</b><span>bytes for chapter 21, against its 655,000</span></div>')
    P(f'<div class="fact"><b>{proj / 1e6:.2f} MB</b><span>the page projected with every chapter still to come; the limit is 16 MB</span></div>')
    P('</div>')
    if GUIDE_URL:
        P(f'<p class="note">The chapters page: <a href="{e(GUIDE_URL)}">{e(GUIDE_URL)}</a></p>')

    for key, aid, stem, title, desc in VIEWS:
        P(f'<h2 id="{key}">{e(title)}</h2><div class="col"><p>{e(desc)}</p></div>')
        shares = screens(aid)
        for wd in (1440, 390):
            figs = []
            for theme in ('Light', 'Dark'):
                src = EXP / f'20261122_{stem}-{wd}-{theme}.png'
                if not src.exists():
                    continue
                first = IMG / f'{key}-{wd}-{theme.lower()}-first.webp'
                full = IMG / f'{key}-{wd}-{theme.lower()}.webp'
                webp(src, first, crop_h=VH[wd], q=Q_FIRST)
                fw, fh = webp(src, full, q=Q_FULL)
                figs.append((theme, first, full, fh))
            cls = 'pair' if wd == 1440 else 'phones'
            P(f'<div class="{cls}">')
            for theme, first, full, fh in figs:
                alt = f'{title}, first screen at {wd} px, {theme.lower()} theme.'
                P(f'<figure class="shot"><a href="img/{full.name}"><img src="img/{first.name}" alt="{e(alt)}" '
                  f'loading="lazy"></a><figcaption>{wd} px, {theme.lower()}. First screen; the picture opens the whole '
                  f'page, {fh:,} px tall.</figcaption></figure>')
            P('</div>')
        rows = []
        for vk, scr in sorted(shares.items(), key=lambda kv: -int(kv[0].split('-')[0])):
            for s in scr:
                rows.append((vk.split('-')[0], s['name'], s['newsprint'], s.get('red', 0), s.get('faults', [])))
        if rows:
            P('<details><summary>Rule 05.1 by screen, light theme (contract C5)</summary><div class="tbl"><table>'
              '<thead><tr><th>Width</th><th>Screen</th><th>Newsprint</th><th>Red</th><th>Inside the limits</th></tr></thead><tbody>')
            for wd, name, nw, red, faults in rows:
                P(f'<tr><td>{wd} px</td><td>{e(name)}</td><td class="num">{nw:.1f}</td><td class="num">{red:.1f}</td>'
                  f'<td>{"Yes" if not faults else e("; ".join(faults))}</td></tr>')
            P('</tbody></table></div></details>')

    P('<h2 id="more">The loop index and How to read</h2>')
    P('<div class="pair">')
    for key, aid, stem, title, desc in EXTRAS:
        src = EXP / f'20261122_{stem}-1440-Light.png'
        if not src.exists():
            continue
        first = IMG / f'{key}-1440-light-first.webp'
        full = IMG / f'{key}-1440-light.webp'
        webp(src, first, crop_h=VH[1440], q=Q_FIRST)
        fw, fh = webp(src, full, q=Q_FULL)
        P(f'<figure class="shot"><a href="img/{full.name}"><img src="img/{first.name}" alt="{e(title)}, first screen at '
          f'1440 px, light theme." loading="lazy"></a><figcaption><strong>{e(title)}.</strong> {e(desc)} The picture '
          f'opens the whole page, {fh:,} px tall.</figcaption></figure>')
    P('</div>')

    P('<h2 id="test">The atlas test</h2>')
    P('<div class="col"><p>One script reads every atlas page the kit draws, as its standalone page and as each plate’s '
      'frames, together with the model, and checks that each page says what the model holds. Any failure stops the kit’s '
      'build and the strict guide build. Its self-test plants one fault for each check in a copy of a page, never in the '
      f'model, and passes only when every plant is caught. Run {e(t["ran"][:16].replace("T", " "))} UTC.</p></div>')
    ids = t['ids']
    P('<div class="tbl"><table class="test"><thead><tr><th>Check</th>' + ''.join(f'<th class="num">{a}</th>' for a in ids)
      + '</tr></thead><tbody>')
    for check in sorted(by, key=lambda c: int(c[1:])):
        cells = []
        for a in ids:
            p_, f_ = by[check].get(a, [0, 0])
            cells.append(f'<td class="num">{"none" if not (p_ or f_) else (str(p_) if not f_ else f"{p_} / {f_} failed")}</td>')
        P(f'<tr><th scope="row">{check} {e(names.get(check, ""))}</th>{"".join(cells)}</tr>')
    P('</tbody></table></div>')
    P('<p class="note">Each cell counts the frames and pages that passed the check for that application. A dash means the '
      'application holds nothing that check reads. A11 to A16 are the six pages; A17 to A20 are the states the rule plates '
      'show (every variable open, sheet D10 open, Loop R18 on its second step, and the claim open).</p>')

    P('<h2 id="answers">Your answers, applied</h2><div class="tbl"><table><thead><tr><th>Answer</th><th>What it set</th>'
      '<th>Where it landed</th></tr></thead><tbody>')
    for a, what, where in ANSWERS:
        P(f'<tr><td>{a}</td><td>{e(what)}</td><td>{e(where)}</td></tr>')
    P('</tbody></table></div>')

    P('<h2 id="calls">Calls the studio made inside the plan</h2><div class="col"><ul>')
    for c in CALLS:
        P(f'<li>{e(c)}</li>')
    P('</ul></div>')

    P('<h2 id="weight">Weight</h2><div class="col">')
    P(f'<p>The page weighs {page:,} bytes today. Chapter 21 weighs {c21:,} bytes against its allocation of 655,000. '
      f'With every chapter still to come counted at its own allocation, the page projects to {proj:,} bytes, '
      f'{abs(limit - proj):,} bytes {"over" if proj > limit else "under"} the 16 MB limit. Nothing stops a build today, '
      'since only the page itself past 16 MB does (DR-271).</p>')
    P(f'<p>The first placement weighed 1,539,423 bytes. The engineer took {1539423 - c21:,} bytes off with no word, frame '
      'or picture lost: every cropped plate now draws its own part alone, where it had carried the whole page clipped; the '
      'atlas style keeps only the rules a frame uses; and the marks that repeat in every row are drawn once and reused, '
      'proved pixel for pixel on every frame.</p>')
    P('<p>The options that keep content, and what each costs, come to Phase 4 board 1 for your decision. Nothing is cut '
      'before you answer.</p></div>')

    P('<h2 id="tested">Tested and not tested</h2><div class="pair"><div><h4>Tested</h4><ul>')
    for x in TESTED + [QUICK]:
        P(f'<li>{e(x)}</li>')
    P('</ul></div><div><h4>Not tested</h4><ul>')
    for x in NOT_TESTED:
        P(f'<li>{e(x)}</li>')
    P('</ul></div></div>')
    P('<p class="note">Built by the main session from the kit’s exports (DR-322). Every picture on this page is a capture '
      'of a working page the kit exported.</p>')
    P('</main></div>')
    PAGE.write_text('\n'.join(parts))
    size = sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
    print(f'wrote {PAGE} and {len(list(IMG.iterdir()))} pictures, {size:,} bytes in all')


ANSWERS = [
    ('DR-319', 'The atlas pages share chapter 20’s website style wherever the rules match, and How to read drops its dark frame',
     'The atlas adds only its own small style; chapter 20’s plates and exports did not move by a byte'),
    ('DR-320', 'The keyboard walks move to chat 12; the atlas test and axe cover order, names, colors and pace by script',
     'axe at 0 on all 20 working views; the test checks the stepper’s order and pace'),
    ('DR-321', 'The loop index prints all 23 titles as stored, with a note that the atlas’s next version reviews them',
     'Rule 21.14 and the loop index page'),
    ('DR-322', 'This board, built by the main session, asking nothing', 'This page'),
    ('DR-323', 'Rule 13.12: “sets out what the record shows from each side, at the length the record holds”',
     'Chapter 13, word for word; chapter 14’s check 99 of 99'),
    ('DR-324', 'Rule 03.6: L1 from the 16 px master under 24.375em, and the row “Site, from 24.375em to 48em”',
     'Chapter 03, word for word'),
    ('DR-325', 'Rule 03.6’s file list adds the 16 px wordmark master', 'Chapter 03'),
]
CALLS = [
    'The atlas’s title bar is a Charcoal band in both themes, as chapter 20’s home page already draws it; the plan had set it '
    'on the page’s own ground. The data lead ruled that it stands (R17): each page still has one header and one navigation '
    'named “Atlas views”. Chat 12’s accessibility lead checks it.',
    'A contested remedy prints the atlas’s stored text whole, split at one sentence, side by side. The plan had asked the two '
    'readings to match in length, which only an edit of the atlas’s text could promise; the test now prints each block’s '
    'length and never fails on it (R15), in line with your answers DR-314 and DR-323.',
    'Connection L15 on Loop R18 is plausible, so it is dashed, and Reform R-11 targets it, so it is red. Its Charcoal edge '
    'follows the dashes, so in gray it still reads as plausible (R14).',
    'Sections whose opening screens ran past 85 percent Newsprint open on a compact Charcoal band (Rule 05.1 by screen, DR-310).',
    'Page titles name the record: “Reform R-23, Minimum wage that rises with an index | Who Do They Answer To? | Oath & Action”.',
]
TESTED = [
    'The strict build, November 23, 00:46 UTC: exit 0, 0 warnings, 0 stale plates, 14,189,330 bytes, 409 rules, 765 specimens',
    'The atlas test on the final drawing, 00:30 to 00:33 UTC (the engineer’s run): 1,264 checks passed, 0 failed; its self-test '
    'caught all 27 planted faults, on the working pages and on the plates alone',
    'The data visualization lead’s own check of every export and plate frame against the model, in three batches: 0 data '
    'faults, every view signed off whole',
    'Every export at its size: 67 of 67',
    'Rule 05.1 by screen: all 57 light screens between 60 and 85 percent Newsprint',
    'axe at 0 on all 20 working views; the working pages’ scripts clicked through in Chromium at 1440 and 390 px',
    'Chapter 20 unchanged: its 42 frames and 41 exports byte for byte',
    'The chart kit, 96 of 96 charts, 0 faults; chapter 14’s check, 99 of 99',
    'The guide check’s self-test: 163 of 163 planted faults caught, 59 of 59 allowed cases left alone',
]
NOT_TESTED = [
    'Keyboard and screen reader walks of the atlas pages by the accessibility lead (chat 12, DR-320)',
    'The creative director’s wall test and scores (chat 12, DR-315)',
    'Safari, Firefox, real screen readers and real phones (listed at Gate 4, DR-279)',
]

STYLE = '''<style>
/* Layout: one reading column on the brand's Newsprint; the atlas captures run to the full width. Tokens are the guide's own. */
:root {
  --ground: #DCD9D2;      /* oa.color.palette.newsprint */
  --ink: #121212;         /* oa.color.palette.charcoal */
  --quiet: #4E535B;       /* oa.color.derived.deep-stone */
  --rule: #5D636D;        /* oa.color.palette.stone */
  --red: #E63946;         /* oa.color.palette.pillar-red, the ampersand only */
  --card: #E7E5E0;
  --focus: #4A7C74;       /* oa.color.palette.verdigris */
  --display: "Inter Tight", "Inter", system-ui, sans-serif;
  --text: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --ground: #121212; --ink: #DCD9D2; --quiet: #A3A19C; --rule: #828A9D; --red: #E63946; --card: #232426; --focus: #7FB3A9;
  color-scheme: dark } }
:root[data-theme="dark"] {
  --ground: #121212; --ink: #DCD9D2; --quiet: #A3A19C; --rule: #828A9D; --red: #E63946; --card: #232426; --focus: #7FB3A9;
  color-scheme: dark }
body { background: var(--ground); color: var(--ink); font: 400 16px/1.55 var(--text); overflow-wrap: break-word; }
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
h4 { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin: 0 0 8px; }
p { margin: 0 0 12px; }
ul { padding-left: 1.2em; margin: 0 0 12px; } li { margin-bottom: 6px; }
.lede { font-size: 19px; line-height: 1.5; }
.note { font-size: 14px; color: var(--quiet); }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr)); gap: 16px; margin: 24px 0; }
.fact { border-top: 3px solid var(--ink); padding-top: 10px; min-width: 0; }
.fact b { display: block; font: 800 32px/1.05 var(--display); font-variant-numeric: tabular-nums; }
.fact span { font-size: 14px; color: var(--quiet); }
figure { margin: 0; min-width: 0; }
.shot img { display: block; width: 100%; height: auto; border: 1px solid var(--rule); background: #DCD9D2; }
figcaption { font-size: 14px; color: var(--quiet); margin-top: 8px; }
.pair { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 24px; margin-top: 24px; align-items: start; }
.phones { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 300px)); gap: 24px; margin-top: 24px; align-items: start; }
details { margin-top: 20px; } summary { cursor: pointer; font-weight: 600; }
.tbl { overflow-x: auto; margin-top: 16px; }
table { border-collapse: collapse; font-size: 14px; min-width: 100%; }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; }
thead th { font-weight: 700; border-bottom: 2px solid var(--ink); }
.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
table.test th[scope="row"] { font-weight: 600; white-space: nowrap; }
</style>'''

if __name__ == '__main__':
    build()
