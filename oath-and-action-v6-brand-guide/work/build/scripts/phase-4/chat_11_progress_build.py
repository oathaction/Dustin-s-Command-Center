"""Chat 11's progress page: chapter 20 and the website the application kit drew, Rule 05.1 by screen under DR-310,
what the closing checks found, chapter 21's plan in brief, and the items coming to Phase 4 board 1. It asks Dustin
for no decision.

Usage, from the project folder:
  python3 -I work/build/scripts/phase-4/chat_11_progress_build.py [--guide-url URL] [--quick-check TEXT]

--quick-check replaces the one row the main session fills ("Quick guide check at 1440 and 390 px: result to come.").
--guide-url adds a panel that opens the chapters page.

Reads the website exports in work/build/exports/phase-4/ (20261121_Web-*), the kit's page plates
work/build/app-kit/plates/a06.json to a08.json (their views' `screens`, contract C5), Rule 20.9's section words in
work/build/scripts/phase-4/phase4_ch20_build.py (read as text, never run), chapter 20's JSON for its rule and
specimen counts, and the chapter 21 plan for its groups, rule titles and byte estimate. Writes
work/boards/phase-4/chat-11/20261121_Chat-11-Progress.html and its img/ folder: each page's first screen and whole
page as WebP (high quality), the menus and the share preview as WebP, the icons as lossless WebP, and the SVG
favicon as the file the site serves.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path.cwd()
OUT = ROOT / 'work/boards/phase-4/chat-11'
IMG = OUT / 'img'
PAGE = OUT / '20261121_Chat-11-Progress.html'
EXP = ROOT / 'work/build/exports/phase-4'
PLATES = ROOT / 'work/build/app-kit/plates'
GEN20 = (ROOT / 'work/build/scripts/phase-4/phase4_ch20_build.py').read_text()
CH20 = json.loads((ROOT / 'work/build/guide/chapters/20-web.json').read_text())
PLAN21 = (ROOT / 'work/handoffs/phase-4/20261121_Chapter-21-Plan.md').read_text()
GUIDE_URL = sys.argv[sys.argv.index('--guide-url') + 1] if '--guide-url' in sys.argv else ''
QUICK = (sys.argv[sys.argv.index('--quick-check') + 1] if '--quick-check' in sys.argv
         else 'Quick guide check at 1440 and 390 px: result to come.')
LIMIT = 40 * 1024 * 1024          # the board folder stays under about 40 MB
Q_FIRST, Q_FULL, Q_STILL = 92, 88, 92   # WebP quality: first screens, whole pages, the menus and the share card

e = html.escape

# One window's height at each width, contract C5 (the engineer's notes): 900 at 1440, 768 at 1024, 844 at 390, 780 at 360
VH = {1440: 900, 1024: 768, 390: 844, 360: 780}
VIEWS = [(1440, 'Light'), (1024, 'Light'), (390, 'Light'), (360, 'Light'), (1440, 'Dark'), (390, 'Dark')]
PAGES = [
    ('home', 'A06', '20261121_Web-Home-Page', 'Home page'),
    ('article', 'A07', '20261121_Web-Article-Page-Special-Districts', 'Article page'),
    ('act', 'A08', '20261121_Web-Act-Page-Comment-On-A-Proposed-Rule', 'Act page'),
]
OWNER = {'home': 'the home page’s', 'article': 'the article’s', 'act': 'the Act page’s'}
WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']  # H06: one to nine in words

# Alt text for each first screen, written from the captures as drawn (looked at November 21, 2026)
HEAD_WIDE = ('the masthead with the wordmark and its lockmark, the seven parts, Explain, Track, Connect, Act, Who Do They '
             'Answer To?, About and Subscribe, and under them the theme switch, Light, Dark and Match my device')
HEAD_PHONE = 'the masthead with the wordmark alone and a Menu button'
ALT = {
    ('home', 1440, 'Light'): f'The home page’s first screen at 1440 px on Newsprint: {HEAD_WIDE}, with Light chosen. A '
        'Charcoal band holds the four pillar cells with their icons, Explain, Track, Connect and Act. Under each sits one '
        'piece: the explainer What a special district does; the tracker for H.R. 7008, the Stop Insider Trading Act, at step '
        '5 of 6, Second chamber; the guide Who sets your electric bill; and Comment on the FDA’s proposed rule on NAC, its '
        'step 3 marked with a red dot and the words You can take part now.',
    ('home', 1024, 'Light'): f'The home page’s first screen at 1024 px on Newsprint: {HEAD_WIDE}. The pillar band breaks '
        'after Track, so Explain and Track head two columns: the explainer What a special district does, and the tracker for '
        'H.R. 7008 at step 5 of 6 with its source line.',
    ('home', 390, 'Light'): f'The home page’s first screen at 390 px on Newsprint: {HEAD_PHONE}. Explain heads the page '
        'on its own Charcoal cell, then the explainer What a special district does, then the Track cell and the start of the '
        'H.R. 7008 tracker.',
    ('home', 360, 'Light'): f'The home page’s first screen at 360 px on Newsprint: {HEAD_PHONE}, the wordmark drawn from '
        'its smaller master. The Explain cell, the explainer, then the Track cell and the start of the H.R. 7008 tracker.',
    ('home', 1440, 'Dark'): 'The home page’s first screen at 1440 px in the dark theme, on Charcoal, with Dark chosen. The '
        'same masthead and pillar row, the row now edged by a thin rule along its top and foot, and the same four pieces '
        'with the red dot on the NAC rule’s step 3.',
    ('home', 390, 'Dark'): 'The home page’s first screen at 390 px in the dark theme: the masthead with Menu, then the '
        'Explain and Track cells, each edged by a thin rule, with the explainer and the start of the tracker.',
    ('article', 1440, 'Light'): f'The article’s first screen at 1440 px on Newsprint: {HEAD_WIDE}, with Explain underlined '
        'as the current part. The pillar row in small type with Explain current, the kicker Explainer, Local government, '
        'the headline What a special district does in very large type, the opening paragraph and the byline Dustin Cathcart, '
        'Founder and Editor, November 21, 2026. A Charcoal count panel to the right reads 39,555 special districts in 2022, '
        'the most common kind of government, of the 90,888 governments the Census Bureau counted, with its source line.',
    ('article', 1024, 'Light'): f'The article’s first screen at 1024 px on Newsprint: {HEAD_WIDE}, with Explain current. The '
        'headline What a special district does, the opening paragraph and the byline, and the Charcoal count panel at the '
        'right: 39,555 special districts in 2022, the most common kind of government, of the 90,888 governments the '
        'Census Bureau counted, with the start of its source line at the window’s foot.',
    ('article', 390, 'Light'): f'The article’s first screen at 390 px on Newsprint: {HEAD_PHONE}. The pillar row on two '
        'lines with Explain current, the kicker, the headline on three lines, the opening paragraph, and the top of the '
        'Charcoal count panel showing 39,555 special districts in 2022.',
    ('article', 360, 'Light'): f'The article’s first screen at 360 px on Newsprint: {HEAD_PHONE}, from the smaller '
        'master. The pillar row, the kicker, the headline on three lines, the opening paragraph and the top of the count '
        'panel.',
    ('article', 1440, 'Dark'): 'The article’s first screen at 1440 px in the dark theme, with Dark chosen: the same '
        'headline, paragraph and byline in light type on Charcoal, and the count panel, 39,555, edged by a thin rule.',
    ('article', 390, 'Dark'): 'The article’s first screen at 390 px in the dark theme: the headline, the opening paragraph '
        'and the top of the count panel, edged by a thin rule.',
    ('act', 1440, 'Light'): f'The Act page’s first screen at 1440 px on Newsprint: {HEAD_WIDE}, with Act underlined as '
        'the current part. The headline How to comment on the FDA’s proposed rule on NAC, a paragraph saying anyone may '
        'comment until January 19, 2027, the line Checked November 21, 2026, and the byline. A Charcoal panel at the right, '
        'Where the rule stands, lists six steps: Early notice, done, April 22, 2022; Proposed, done, November 17, 2026; '
        'Comments open, now, with a red dot; Comments closed, Final rule and In effect, not yet. Under them, You can take '
        'part now, the docket number FDA-2025-N-2699, and the top edge of the red ask at the window’s foot.',
    ('act', 1024, 'Light'): f'The Act page’s first screen at 1024 px on Newsprint: {HEAD_WIDE}, with Act current. The '
        'headline, the opening paragraph and the status panel Where the rule stands, its six steps running to the '
        'window’s foot.',
    ('act', 390, 'Light'): f'The Act page’s first screen at 390 px on Newsprint: {HEAD_PHONE}. The pillar row with Act '
        'current, the headline on four lines, the opening paragraph and the top of the status panel with step 1, Early '
        'notice, done, April 22, 2022.',
    ('act', 360, 'Light'): f'The Act page’s first screen at 360 px on Newsprint: {HEAD_PHONE}, from the smaller master. '
        'The headline on four lines, the opening paragraph and the top of the status panel.',
    ('act', 1440, 'Dark'): 'The Act page’s first screen at 1440 px in the dark theme, with Dark chosen: the headline and '
        'paragraph on Charcoal, and the status panel edged by a thin rule, its step 3 marked with a red dot.',
    ('act', 390, 'Dark'): 'The Act page’s first screen at 390 px in the dark theme: the headline, the opening paragraph '
        'and the top of the status panel, edged by a thin rule.',
}

# A fault seen in a picture while building this page, printed under it; clear the entry once the export is redrawn
CAPTION_NOTES = {}  # the 1024 px article's cut figure, noted here in the first draft, was fixed in the 21:18 exports

STILLS = {
    'menu390l': ('20261121_Web-Menu-Open-390-Light', 'Menu open, 390 px, light theme',
                 'The menu open at 390 px on Newsprint. A title row with Menu and Close the menu, then the theme switch, '
                 'Light chosen, Dark and Match my device, then the seven parts as rows: Explain on a white band with a dark '
                 'bar at its left as the current part, then Track, Connect, Act, Who Do They Answer To?, About and '
                 'Subscribe.'),
    'menu360l': ('20261121_Web-Menu-Open-360-Light', 'Menu open, 360 px, light theme',
                 'The menu open at 360 px on Newsprint. The same rows, with Match my device moved to a second line of the '
                 'theme switch.'),
    'menu390d': ('20261121_Web-Menu-Open-390-Dark', 'Menu open, 390 px, dark theme',
                 'The menu open at 390 px on Charcoal, Dark chosen, with Explain on a Prussian blue band as the current '
                 'part.'),
    'share': ('20261121_Web-Share-Preview-Special-Districts-1200x630', 'Share preview, 1200 by 630 px',
              'The share preview card. On Newsprint, the kicker Explainer, Local government, and the headline What a '
              'special district does on two lines. A Charcoal band across the foot holds the wordmark at the left and the '
              'lockmark at the right, its last dot red.'),
}

ICONS = [  # (published name, source, how to read it, label, alt)
    ('20261121_Web-Favicon-16.webp', ('ico', 16), '16 px', 'favicon.ico, its 16 px image',
     'Ampersand B in signature red at 16 px, on a clear ground.'),
    ('20261121_Web-Favicon-32.webp', ('ico', 32), '32 px', 'favicon.ico, its 32 px image',
     'Ampersand B in signature red at 32 px, on a clear ground.'),
    ('20261121_Web-Favicon-48.webp', ('ico', 48), '48 px', 'favicon.ico, its 48 px image',
     'Ampersand B in signature red at 48 px, on a clear ground.'),
    ('20261121_Web-Apple-Touch-Icon-180.webp', ('png', '20261121_Web-Apple-Touch-Icon-180.png'), '180 by 180 px',
     'Apple touch icon', 'Ampersand B in signature red on a Charcoal square, 180 by 180 px.'),
    ('20261121_Web-Manifest-Icon-192.webp', ('png', '20261121_Web-Manifest-Icon-192.png'), '192 by 192 px',
     'Web app manifest icon', 'Ampersand B in signature red on a Charcoal square, 192 by 192 px.'),
    ('20261121_Web-Manifest-Icon-512-Maskable.webp', ('png', '20261121_Web-Manifest-Icon-512-Maskable.png'),
     '512 by 512 px', 'Maskable manifest icon',
     'Ampersand B in signature red on a full-bleed Charcoal square, 512 by 512 px, kept inside the circle a phone may '
     'crop it to.'),
]
SVG_FAVICON = '20261121_Web-Favicon.svg'


def n(v):
    return f'{v:,}'


# ---------------------------------------------------------------- pictures

def save_webp(im, path, **kw):
    im.save(path, 'WEBP', method=6, **kw)
    return path.name


def pictures():
    """Every picture the page shows, with its sizes; returns {key: info}."""
    if IMG.exists():
        shutil.rmtree(IMG)
    IMG.mkdir(parents=True)
    pics = {}
    for key, aid, stem, _ in PAGES:
        for w, theme in VIEWS:
            src = EXP / f'{stem}-{w}-{theme}.png'
            im = Image.open(src).convert('RGB')
            if im.width != w:
                sys.exit(f'{src.name}: {im.width} px wide, expected {w}')
            h = VH[w]
            full = save_webp(im, IMG / f'{stem}-{w}-{theme}.webp', quality=Q_FULL)
            first = save_webp(im.crop((0, 0, w, h)), IMG / f'{stem}-{w}-{theme}-First-Screen.webp', quality=Q_FIRST)
            pics[(key, w, theme)] = {'full': full, 'first': first, 'w': w, 'h': h, 'full_h': im.height}
    for k, (stem, _, _) in STILLS.items():
        im = Image.open(EXP / f'{stem}.png').convert('RGB')
        pics[k] = {'file': save_webp(im, IMG / f'{stem}.webp', quality=Q_STILL), 'w': im.width, 'h': im.height}
    ico = Image.open(EXP / '20261121_Web-Favicon-16-32-48.ico')
    for name, (kind, ref), *_ in ICONS:
        im = ico.ico.getimage((ref, ref)) if kind == 'ico' else Image.open(EXP / ref)
        save_webp(im, IMG / name, lossless=True, quality=100, exact=True)
        pics[name] = {'w': im.width, 'h': im.height}
    shutil.copyfile(EXP / SVG_FAVICON, IMG / SVG_FAVICON)
    return pics


# ---------------------------------------------------------------- the website

def shot(pics, key, w, theme, label, eager=False):
    p = pics[(key, w, theme)]
    alt = ALT[(key, w, theme)]
    return (f'<figure class="shot"><img src="img/{p["first"]}" width="{p["w"]}" height="{p["h"]}" '
            f'{"" if eager else "loading=" + chr(34) + "lazy" + chr(34) + " "}decoding="async" alt="{e(alt)}">'
            f'<figcaption><span class="label">{e(label)}</span><span class="label">{w} px</span>'
            f'<span class="label">{theme}</span>'
            f'First screen, {n(p["w"])} by {n(p["h"])} px. <a href="img/{p["full"]}" target="_blank" rel="noopener">'
            f'Open the whole page, {n(p["w"])} by {n(p["full_h"])} px</a>.'
            + (f' <strong>{e(CAPTION_NOTES[(key, w, theme)])}</strong>' if (key, w, theme) in CAPTION_NOTES else '')
            + '</figcaption></figure>')


def page_shots(pics, key, label, eager=False):
    one = shot(pics, key, 1440, 'Light', label, eager)
    two = shot(pics, key, 1024, 'Light', label) + shot(pics, key, 1440, 'Dark', label)
    phones = ''.join(shot(pics, key, w, t, label) for w, t in [(390, 'Light'), (360, 'Light'), (390, 'Dark')])
    return f'<div class="wide">{one}</div><div class="pair">{two}</div><div class="phones">{phones}</div>'


def still(pics, k, width_css=None):
    stem, label, alt = STILLS[k]
    p = pics[k]
    return (f'<figure class="shot"><img src="img/{p["file"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" '
            f'decoding="async" alt="{e(alt)}"><figcaption><span class="label">{e(label)}</span></figcaption></figure>')


def icons(pics):
    true = ''
    big = ''
    for name, (kind, ref), size, label, alt in ICONS:
        p = pics[name]
        cls = 'ico-tile' if kind == 'png' else 'ico-clear'
        true += (f'<figure class="icon {cls}"><div class="ground"><img src="img/{name}" width="{p["w"]}" '
                 f'height="{p["h"]}" loading="lazy" alt="{e(alt)}"></div>'
                 f'<figcaption><span class="label">{e(label)}</span>{e(size)}, at its own pixels.</figcaption></figure>')
        if kind == 'ico':
            big += (f'<figure class="icon"><div class="ground"><img class="px" src="img/{name}" width="{p["w"] * 4}" '
                    f'height="{p["h"] * 4}" loading="lazy" alt="{e(alt[:-1])}, drawn at four times its size with each '
                    f'pixel kept square."></div><figcaption><span class="label">{e(label)}</span>{e(size)}, at four '
                    'times.</figcaption></figure>')
    svg = ''
    for ground, word in [('light', 'Newsprint'), ('dark', 'Charcoal')]:
        svg += (f'<figure class="icon"><div class="ground g-{ground}"><img src="img/{SVG_FAVICON}" width="16" height="16" '
                f'alt="Ampersand B in signature red at 16 px on {word}."><img src="img/{SVG_FAVICON}" width="64" '
                f'height="64" alt="The same favicon drawn at 64 px on {word}."></div>'
                f'<figcaption><span class="label">favicon.svg</span>On {word}, at 16 px and at four times.</figcaption>'
                '</figure>')
    return f'<div class="icons">{svg}{true}</div><div class="icons">{big}</div>'


# ---------------------------------------------------------------- Rule 05.1 by screen

def section_words():
    m = re.search(r"'section_words':\s*\{(.*?)\}", GEN20, re.S)
    if not m:
        sys.exit('Rule 20.9’s section words not found in phase4_ch20_build.py')
    return dict(re.findall(r"'([^']+)':\s*'([^']+)'", m.group(1)))


def screen_tables():
    words = section_words()
    out, total, light_max, red_max, faults = [], 0, (0, ''), (0, ''), 0
    for key, aid, stem, label in PAGES:
        plate = json.loads((PLATES / f'{aid.lower()}.json').read_text())
        views = {v['key']: v for v in plate['views'] if v.get('screens')}
        tables, count, lo, hi = '', 0, 100.0, 0.0
        for w, theme in VIEWS:
            v = views[f'{w}-{theme.lower()}']
            rows = ''
            for s in v['screens']:
                count += 1
                faults += len(s.get('faults') or [])
                name = 'First screen' if s['name'] == 'first' else words.get(s['name'], s['name'])
                if name == 'footer':
                    name = 'Footer'
                if theme == 'Light':
                    lo, hi = min(lo, s['newsprint']), max(hi, s['newsprint'])
                    if s['newsprint'] > light_max[0]:
                        light_max = (s['newsprint'], f'{OWNER[key]} “{name}” screen at {w} px')
                if s['red'] > red_max[0]:
                    red_max = (s['red'], f'{OWNER[key]} “{name}” screen at {w} px, {theme.lower()} theme')
                rows += (f'<tr><th scope="row">{e(name)}</th><td class="num">{s["newsprint"]:.1f}</td>'
                         f'<td class="num">{s["dark"]:.1f}</td><td class="num">{s["red"]:.1f}</td></tr>')
            judged = 'all three limits' if theme == 'Light' else 'red only'
            tables += (f'<div class="tablewrap"><table class="scr"><caption>{w} px, {theme.lower()} theme '
                       f'<span>judged on {judged}</span></caption><thead><tr><th scope="col">Screen</th>'
                       f'<th scope="col" class="num">Newsprint</th><th scope="col" class="num">Dark</th>'
                       f'<th scope="col" class="num">Red</th></tr></thead><tbody>{rows}</tbody></table></div>')
        total += count
        out.append(f'<details class="spec"><summary><span>{e(label)}</span><span class="count">{count} screens; '
                   f'Newsprint {lo:.1f} to {hi:.1f} percent on the light pages</span></summary>'
                   f'<div class="scrgrid">{tables}</div></details>')
    if faults:
        sys.exit(f'{faults} screen faults in the plates; the page says every screen passes')
    return '\n'.join(out), total, light_max, red_max


# ---------------------------------------------------------------- chapter 21's plan

def plan21():
    titles = re.findall(r'^#### (21\.\d+) (.+?)\s*$', PLAN21, re.M)
    groups = re.findall(r'^\| (\d) \| (21\.\d+) \| ([^|]+?) \| ([^|]+?) \|$', PLAN21, re.M)
    est = re.search(r'\*\*Chapter 21\*\* \| \| \| \*\*about ([\d,]+)\*\*', PLAN21)
    alloc = re.search(r'Allocation ([\d,]+) bytes', PLAN21)
    if not (titles and groups and est and alloc):
        sys.exit('chapter 21 plan: groups, rule titles or the byte estimate not found')
    order = [t[0] for t in titles]
    starts = [order.index(g[1]) for g in groups]
    html_ = ''
    for i, g in enumerate(groups):
        a, b = starts[i], (starts[i + 1] if i + 1 < len(starts) else len(order))
        lis = ''.join(f'<li><span class="rid">{e(r)}</span> {e(t.replace(chr(39), chr(8217)))}</li>' for r, t in titles[a:b])
        html_ += f'<div class="rgroup"><h4>{e(g[2])}</h4><ol>{lis}</ol></div>'
    return html_, len(titles), len(groups), est.group(1), alloc.group(1)


# ---------------------------------------------------------------- page

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pics = pictures()
    tables, n_screens, light_max, red_max = screen_tables()
    rules21, n21, g21, est21, alloc21 = plan21()
    est_n, alloc_n = int(est21.replace(',', '')), int(alloc21.replace(',', ''))
    panel = ('<div class="panel"><h3>Read it on the chapters page</h3><p>Chapter 20 sits on the chapters page with '
             f'every plate in place: <a href="{e(GUIDE_URL)}">open the chapters page</a>.</p></div>') if GUIDE_URL else ''
    rep = {
        '{{N20_RULES}}': str(len(CH20['rules'])),
        '{{N20_SPECS}}': str(len(list((ROOT / 'work/build/guide/specimens').glob('s-20-*')))),
        '{{SHOTS_home}}': page_shots(pics, 'home', 'Home page', eager=True),
        '{{SHOTS_article}}': page_shots(pics, 'article', 'Article page'),
        '{{SHOTS_act}}': page_shots(pics, 'act', 'Act page'),
        '{{MENUS}}': still(pics, 'menu390l') + still(pics, 'menu360l') + still(pics, 'menu390d'),
        '{{SHARE}}': still(pics, 'share'),
        '{{ICONS}}': icons(pics),
        '{{SCREEN_TABLES}}': tables,
        '{{N_SCREENS}}': str(n_screens),
        '{{LIGHT_MAX}}': f'{light_max[0]:.1f} percent, {light_max[1]}',
        '{{RED_MAX}}': f'{red_max[0]:.1f} percent, {red_max[1]}',
        '{{RULES21}}': rules21, '{{N21}}': str(n21), '{{G21}}': WORDS[g21] if g21 < 10 else str(g21),
        '{{EST21}}': est21, '{{ALLOC21}}': alloc21, '{{OVER21}}': n(est_n - alloc_n),
        '{{QUICK}}': e(QUICK),
        '{{GUIDE_PANEL}}': panel,
    }
    page = TEMPLATE
    for k, v in rep.items():
        page = page.replace(k, v)
    left = re.findall(r'\{\{[A-Za-z0-9_]+\}\}', page)
    if left:
        sys.exit(f'unfilled: {left}')
    if '—' in page or '–' in page:
        sys.exit('an em or en dash is on the page')
    text = re.sub(r'<style.*?</style>', ' ', page, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    banned = re.findall(r'\b(genuinely|really|truly|actually|simply|just|leverage[sd]?|underscores?|reflects?|'
                        r'very|extremely|incredibly)\b', text, re.I)
    if banned:
        sys.exit(f'filler or corporate words on the page: {sorted(set(banned))}')
    for m in re.finditer(r'<img\b[^>]*>', page):
        if not re.search(r'\balt="[^"]{12,}"', m.group(0)):
            sys.exit(f'an image without real alt text: {m.group(0)[:120]}')
    PAGE.write_text(page)
    files = [p for p in OUT.rglob('*') if p.is_file()]
    size = sum(p.stat().st_size for p in files)
    if size > LIMIT:
        sys.exit(f'the board folder weighs {size:,} bytes, past {LIMIT:,}')
    print('wrote', PAGE, f'{len(page.encode()):,} bytes;', len(list(IMG.iterdir())), 'pictures;',
          f'folder {len(files)} files, {size:,} bytes')


TEMPLATE = r'''<title>Phase 4, Chat 11</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap">
<style>
/* Layout: one reading column on the brand's Newsprint; the website's captures break out to the full width. Tokens are the guide's own. */
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
h3 { font: 700 18px/1.3 var(--text); margin: 40px 0 8px; }
h4 { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin: 0 0 8px; }
p { margin: 0 0 12px; }
.lede { font-size: 19px; line-height: 1.5; }
.note { font-size: 14px; color: var(--quiet); }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr)); gap: 16px; margin: 24px 0; }
.fact { border-top: 3px solid var(--ink); padding-top: 10px; min-width: 0; }
.fact b { display: block; font: 800 32px/1.05 var(--display); font-variant-numeric: tabular-nums; }
.fact span { font-size: 14px; color: var(--quiet); }
figure { margin: 0; min-width: 0; }
.shot img { display: block; width: 100%; height: auto; border: 1px solid var(--rule); background: #DCD9D2; }
figcaption { font-size: 14px; color: var(--quiet); margin-top: 8px; }
.label { display: inline-block; font: 700 12px/1 var(--text); letter-spacing: 0.06em; text-transform: uppercase;
  border: 1px solid currentColor; padding: 3px 6px; margin: 0 6px 4px 0; color: var(--ink); }
.wide { margin-top: 24px; }
.pair { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 24px; margin-top: 24px; align-items: start; }
.phones { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 24px; margin-top: 24px; align-items: start; }
.phones .shot { max-width: 390px; }
.icons { display: flex; flex-wrap: wrap; gap: 24px; margin-top: 24px; align-items: flex-end; }
.icon { max-width: 100%; min-width: 0; flex: 0 1 auto; }
.icon .ground { display: flex; align-items: center; gap: 16px; padding: 16px; border: 1px solid var(--rule); background: #DCD9D2; max-width: 100%; }
.icon .g-dark { background: #121212; border-color: #828A9D; }
.icon img { display: block; max-width: 100%; height: auto; min-width: 0; }
.icon img.px { image-rendering: pixelated; }
.icon figcaption { max-width: 16rem; }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
th, td { text-align: left; padding: 8px 12px 8px 0; border-bottom: 1px solid color-mix(in srgb, var(--rule) 45%, transparent); vertical-align: top; }
thead th { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); border-bottom: 1px solid var(--rule); }
td.num, th.num { font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }
table.scr td.num, table.scr th.num { padding-right: 0; padding-left: 12px; }
table.scr tbody th { font-weight: 600; }
table.scr caption { text-align: left; font-weight: 700; padding: 0 0 6px; }
table.scr caption span { display: block; font-weight: 400; font-size: 14px; color: var(--quiet); }
@media (max-width: 480px) { table { font-size: 14px; } th, td { padding-right: 6px; } table.scr td.num, table.scr th.num { padding-left: 6px; } }
.scrgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: 24px 32px; margin: 8px 0 24px; }
details.spec { border-top: 1px solid var(--rule); }
details.spec:last-of-type { border-bottom: 1px solid var(--rule); }
details.spec summary { cursor: pointer; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 16px; padding: 12px 0; font-weight: 700; }
details.spec summary .count { font-weight: 400; color: var(--quiet); font-size: 14px; }
.panel { background: var(--panel); color: var(--on-panel); padding: 24px; margin-top: 24px; }
.panel h3 { margin-top: 0; }
.panel a { color: var(--on-panel); }
.views { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(260px, 100%), 1fr)); gap: 24px; margin-top: 16px; }
.view { border-top: 3px solid var(--ink); padding-top: 10px; }
.view h3 { margin: 0 0 8px; }
.rules21 { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(260px, 100%), 1fr)); gap: 24px; margin-top: 16px; }
.rgroup ol { list-style: none; padding: 0; margin: 0; display: grid; gap: 6px; }
.rid { font-weight: 700; font-variant-numeric: tabular-nums; margin-right: 4px; }
ul.plain { padding-left: 20px; margin: 0 0 12px; }
ul.plain li { margin-bottom: 6px; }
li.tocome { font-weight: 700; }
.twocol { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: 24px; }
.items { display: grid; gap: 16px; margin-top: 16px; }
.item { background: var(--card); padding: 20px; border-left: 3px solid var(--ink); }
.item h3 { margin: 0 0 8px; }
.item .code { display: block; font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin-bottom: 4px; }
.item .rec { margin: 0; padding-top: 10px; border-top: 1px solid color-mix(in srgb, var(--rule) 45%, transparent); }
.source { font-size: 13px; color: var(--quiet); }
</style>
<div class="wrap">
  <header class="mast">
    <span class="word" aria-label="Oath &amp; Action">OATH<span class="amp">&amp;</span>ACTION</span>
    <span class="kick">Edition 06, Phase 4 progress, November 21, 2026</span>
  </header>

  <main>
  <div class="col">
    <p class="kick" style="margin-top:40px">Chat 11 of Phase 4</p>
    <h1>Chapter 20 and the website are built, and chapter 21 has its plan</h1>
    <p class="lede">Chat 11 built chapter 20, Web, and drew the website it teaches: a home page, an article and an Act page, the menu, the card a shared link shows, and the icons. It also wrote the plan for chapter 21, The atlas, whose build takes a chat of its own. This page asks you for no decision. Seven items wait for Phase 4 board 1, and the last section lists each with the studio&#8217;s recommendation.</p>
  </div>

  <div class="facts" role="list">
    <div class="fact" role="listitem"><b>{{N20_RULES}}</b><span>rules in chapter 20, shown on {{N20_SPECS}} plates</span></div>
    <div class="fact" role="listitem"><b>41 of 41</b><span>kit exports at their exact sizes, by the size check</span></div>
    <div class="fact" role="listitem"><b>{{N_SCREENS}} of {{N_SCREENS}}</b><span>measured screens inside Rule 05.1&#8217;s color limits</span></div>
    <div class="fact" role="listitem"><b>181,840</b><span>bytes of room under 16 MB for the projected page, with the chapters still to build</span></div>
  </div>

  <section aria-labelledby="h-site">
    <h2 id="h-site">The website</h2>
    <div class="col">
      <p>The application kit, the studio&#8217;s tool that draws each application from the guide&#8217;s tokens and components, drew every page below, and chapter 20&#8217;s plates show the same drawings. Each page comes in the light theme at 1440, 1024, 390 and 360 px and in the dark theme at 1440 and 390 px, as you set in DR-311. Each picture is a page&#8217;s first screen, the part a reader sees before scrolling: 900 px tall at 1440, 768 at 1024, 844 at 390 and 780 at 360. Its caption opens the whole page, which runs past 8,000 px on a phone.</p>
      <p>The footer prints the address oathandaction.org with an Illustrative label beside it until you confirm the address (DR-308).</p>
    </div>

    <h3>The home page</h3>
    <div class="col">
      <p>The home page opens on the pillar row: four Charcoal cells, Explain, Track, Connect and Act, each heading one piece. The first leads to our explainer on special districts. Track follows H.R.&#160;7008, the Stop Insider Trading Act, a bill that would limit stock purchases by members of Congress and require photo ID to vote in federal elections. Connect asks who sets an electric bill, and Act carries the FDA&#8217;s proposed rule on NAC, N-acetyl-L-cysteine, with the red take-part mark on its open comment period. Further down, the atlas&#8217;s section opens on its own title bar and shows chart S10, the atlas&#8217;s claims by evidence grade.</p>
    </div>
    {{SHOTS_home}}

    <h3>The article</h3>
    <div class="col">
      <p>The article finishes chat 10&#8217;s studio sample, What a special district does. Its first screen sets the count, 39,555 special districts in 2022 of the 90,888 governments the Census Bureau counted, on a Charcoal panel beside the opening paragraph. Chart S86, the count of governments by type, comes next, and the page ends on a step a reader in any state can take: read their state&#8217;s summary in the Census Bureau&#8217;s report on how each state organizes its governments.</p>
      <p class="source">Source: U.S. Census Bureau, 2022 Census of Governments: Organization, tables CG2200ORG01 and CG2200ORG02, released August 24, 2023, United States. Retrieved November 12, 2026. School districts run by a state, county, city or township count with that government.</p>
    </div>
    {{SHOTS_article}}

    <h3>The Act page</h3>
    <div class="col">
      <p>The Act page is a process piece, Rule 01.22&#8217;s form for a procedure any reader can follow. It shows how to comment on the FDA&#8217;s proposed rule on NAC, docket FDA-2025-N-2699, before comments close on January 19, 2027. Its status panel, Where the rule stands, sits beside the headline: step 3, Comments open, carries the take-part mark, and the red ask, &#8220;Comment at Regulations.gov&#8221;, stands under the steps. The section &#8220;What the record shows&#8221; quotes the rule with its page numbers. The rule records no objection to the change so far, so the section prints what the record holds and adds no opponents&#8217; paragraph to match the petitioners&#8217; length (D4-108). The four steps, the comment panel with the ask again, and the rule at a glance follow.</p>
    </div>
    {{SHOTS_act}}

    <h3>The menu open</h3>
    <div class="col">
      <p>On screens narrower than 1,024 px the parts move behind Menu, which opens chapter 18&#8217;s dialog over the page with the theme switch at its top. These captures open it over the article, so Explain shows as the current part.</p>
    </div>
    <div class="phones">{{MENUS}}</div>

    <h3>The share preview</h3>
    <div class="col">
      <p>When someone shares the article, a feed shows this 1200 by 630 px card: its kicker and headline on Newsprint over a Charcoal foot that holds the wordmark and the lockmark as a 96 px sign-off. It passes Rule 08.2&#8217;s feed test at 500 and 360 px wide, the check that the sign-off keeps its red dot when a feed shrinks the card.</p>
    </div>
    <div class="wide">{{SHARE}}</div>

    <h3>The icons</h3>
    <div class="col">
      <p>Every icon draws ampersand B, the brand&#8217;s own ampersand, from its masters (DR-116). The favicon in a browser tab uses B&#8217;s 16 px master in signature red with no tile, and the app icons set B at 58 percent of a Charcoal square. The ICO file holds three images, at 16, 32 and 48 px. The SVG favicon is shown as the file the site serves; every other icon is converted without loss.</p>
    </div>
    {{ICONS}}
  </section>

  <section aria-labelledby="h-screens">
    <h2 id="h-screens">Color by screen: Rule 05.1 under DR-310</h2>
    <div class="col">
      <p>Rule 05.1 sets how much of a view is Newsprint, the brand&#8217;s paper color, how much is dark and how much is red. You answered DR-310 so that a long page meets it screen by screen: &#8220;On a long page the limits hold for the first screen and for each section&#8217;s opening screen; screens of running text between them may hold more Newsprint.&#8221;</p>
      <p>The kit measures each page&#8217;s first screen and the screen where each section opens, one window tall, on its own captures. A light screen must hold 60 to 85 percent Newsprint, at most one dark panel a section and no more than 5 percent red. A dark screen is judged on red alone, since the Newsprint limit belongs to the light view and DR-204 sets the dark theme. All {{N_SCREENS}} screens pass. The highest Newsprint share is {{LIGHT_MAX}}; the most red is {{RED_MAX}}.</p>
      <p class="note">Figures are percent of the screen. Dark counts Charcoal and Prussian together. Read from the kit&#8217;s plates, <code>work/build/app-kit/plates/a06.json</code> to <code>a08.json</code>.</p>
    </div>
    {{SCREEN_TABLES}}
  </section>

  <section aria-labelledby="h-checks">
    <h2 id="h-checks">What was checked, and what was not</h2>
    <div class="twocol">
      <div>
        <h3>Checked</h3>
        <ul class="plain">
          <li>The closing strict build exits 0 with 0 warnings: 13,080,599 bytes, 393 rules and 731 specimens.</li>
          <li>Chapter 20 weighs 839,154 bytes against its 757,000 allocation, 111 percent. The build reports it and cuts nothing (DR-271).</li>
          <li>The page weighs 13.08 MB today. With the chapters still to build at their allocations, it projects to 15.82 MB, 181,840 bytes under 16 MB.</li>
          <li>The chart kit passes 96 of 96 charts, and chapter 14&#8217;s check finds 99 of 99 files current.</li>
          <li>All 41 kit exports match their sizes in the specifications table. Each page plate in the guide matches its export pixel for pixel, 18 of 18.</li>
          <li>On the working pages, axe finds 0 violations at all 18 views. Tab order, the theme kept after a reload, reflow at 320 px and text at 200 percent show 0 faults.</li>
          <li>The accessibility lead walked the pages by keyboard 12 times and the menu nine times, and measured 3,554 text boxes on pixels with none under its contrast need. The lowest pair is White on Pillar Red, 4.17 to 1, on the ask&#8217;s 19 px bold words, which count as large text.</li>
          <li>The accessibility lead&#8217;s walks found one WCAG fault, W1, a menu link that Shift+Tab could hide under the menu&#8217;s title row at 320 by 256 px. The engineer fixed it and four lesser findings in the application kit, and a rerun of the menu case found 0 hidden in 6 of 6 runs.</li>
          <li>Chapter 05 prints your DR-305 and DR-310 words once each, and the old words nowhere.</li>
          <li>Chapter 19&#8217;s map of WCAG criteria marks seven Met that chapters 16 and 20 owed: four on prerecorded video and sound (1.2.1, 1.2.2, 1.2.3 and 1.2.5) by Rules 16.11 and 16.12, page titles and page language (2.4.2 and 3.1.1) by Rule 20.4, and consistent help (3.2.6) by Rule 20.3. Language of parts (3.1.2) stays a gap that chapter 02 owes.</li>
          <li class="tocome">{{QUICK}}</li>
        </ul>
      </div>
      <div>
        <h3>Not checked</h3>
        <ul class="plain">
          <li>Safari, Firefox and Edge. Only Chromium is installed, so the fix that gives each chart table a keyboard stop for Safari&#8217;s readers is untested there.</li>
          <li>A screen reader. What a reader hears comes from Chromium&#8217;s accessibility tree.</li>
          <li>Real phones, touch, voice control and a 2x screen. Every capture ran at 1x.</li>
          <li>The favicon in a real browser tab, the ICO on Windows and the manifest icons on Android. No web app manifest file is exported yet.</li>
          <li>Print, and forced colors beyond the two emulated captures the accessibility lead looked at.</li>
          <li>The full guide check at four widths. The closing checks run the quick check at 1440 and 390 px.</li>
          <li>Chapter 21. Nothing is drawn yet, so every figure in its plan is an estimate.</li>
          <li>A reading aloud by a person.</li>
        </ul>
      </div>
    </div>
    <div class="col">
      <h3>Done after the board&#8217;s first draft</h3>
      <p>The engineer fixed three craft faults found in the pictures: the article&#8217;s 39,555, cut at the count panel&#8217;s edge at 1024 px; its heading &#8220;How the Census Bureau counts them&#8221;, set far from its paragraph; and the Act page&#8217;s &#8220;Who decides&#8221;, with no space above it. A sweep of every view then found 0 overflows and 0 headings out of rhythm. Every picture on this page comes from those final exports, and the figures above from the strict build that followed them.</p>
      <p>The first quick guide check on that build failed inside chapter 20&#8217;s page pictures: it measured the scaled-down pages&#8217; words and buttons as if they were live text on the guide. The engineer changed the check to read a page picture as a picture, with its words measured at the picture&#8217;s own width, and proved the change with planted faults, 163 of 163 caught. Two faults were real at that width, a chart drawn too wide on the home page and a tracker&#8217;s step words lost in a trimmed picture, and both are fixed. A second run then found one fault of its own kind: Rule 20.10&#8217;s failure plate, a drawing of a share card, set the card&#8217;s words at 7.8 px on a phone. That plate is now a picture whose description carries every word the card shows, as the guide&#8217;s other drawings of a fault are.</p>
    </div>
  </section>

  <section aria-labelledby="h-ch21">
    <h2 id="h-ch21">Chapter 21&#8217;s plan, in brief</h2>
    <div class="col">
      <p>Chapter 21 shows our systems atlas, Who Do They Answer To?, as a reader meets it inside the website. Every atlas page sits under the site&#8217;s masthead with the atlas&#8217;s own title bar beneath (DR-307). Every ID sits in a typed chip, the small label that names a record&#8217;s kind beside its ID (Rule 18.24), and every claim links to the record that grades it. The data visualization lead read every ID, sign, grade and count in the plan from the atlas model by script, and the build reads them again.</p>
      <p>The plan draws four views, each at 1440 and 390 px on Newsprint and in the dark theme. They rotate across health care, wages, Congress and the agencies, and presidential power over watchdogs, and each prints a finding the record holds that one side may want to skip (DR-55, DR-93).</p>
    </div>
    <div class="views">
      <div class="view"><h3>The atlas home</h3><p>The whole system drawn once, its eight parts as boxes with a count on every flow between them, from the model&#8217;s 51 variables and 118 connections. A reader has pressed the everyday question &#8220;Why can the same care produce different bills?&#8221;, which lights the three parts it reaches: Wealth, Checks and Your household.</p></div>
      <div class="view"><h3>A reform page</h3><p>Reform R-23, a minimum wage that rises with an index. Its two targets, household income and households&#8217; financial security, the other reforms aimed at the same mark, and its two grades kept apart. The evidence for the remedy is graded contested, so both readings print at the same length. Its four effects, its routes and its sources follow.</p></div>
      <div class="view"><h3>The Register</h3><p>The index of all 12 sheets, each grade counted in words, and sheet D04, Congress, agencies and public services, open on its 10 connections. It keeps its one rejected option, Reform R-35, term limits for legislators, and lists its 20 issue records filtered to Variable D4, the ability to investigate and enforce the rules, with nine showing.</p></div>
      <div class="view"><h3>A loop page</h3><p>Loop R18, weakening watchdogs lowers the cost of further unilateral action. Its two steps are Connection L14, documented, and Connection L15, plausible and marked as the weakest step. The page reads its two minus signs aloud as the reason the loop reinforces itself, runs the stepper in the guide&#8217;s order and pace, and opens on Reform R-11, a Federal Election Commission able to act, one of three reforms that name the loop.</p></div>
    </div>
    <div class="facts" role="list">
      <div class="fact" role="listitem"><b>{{N21}}</b><span>rules in {{G21}} groups, with a How to read sheet and a plate of the typed chips</span></div>
      <div class="fact" role="listitem"><b>{{EST21}}</b><span>bytes estimated, about {{OVER21}} past its {{ALLOC21}} allocation</span></div>
      <div class="fact" role="listitem"><b>16</b><span>checks in the atlas test every page passes before it ships</span></div>
    </div>
    <div class="col">
      <p>Most of the estimate&#8217;s excess sits in the four view plates&#8217; 16 whole-page frames, where the Register and the loop page carry tables and drawings. Nothing is cut to meet the figure (DR-271), and the plan names two savings for the design director to weigh. Each figure is an estimate until the build measures it.</p>
    </div>
    <details class="spec">
      <summary><span>The {{N21}} rules, by group</span><span class="count">titles as the plan drafts them</span></summary>
      <div class="rules21">{{RULES21}}</div>
    </details>
  </section>

  <section aria-labelledby="h-board">
    <h2 id="h-board">Coming to Phase 4 board 1</h2>
    <div class="col">
      <p>Each item below changes approved work or a rule you set, so it waits for your named answer at board 1.</p>
    </div>
    <div class="items">
      <article class="item">
        <span class="code">ED11-1</span>
        <h3>Rule 05.1&#8217;s specification row</h3>
        <p>DR-310 added its sentence to Rule 05.1&#8217;s text. The rule&#8217;s specification row, &#8220;Newsprint in each view&#8221;, still reads 60 to 85 percent for every view, so a builder who reads only the row holds every screen of a long page to 85.</p>
        <p class="rec"><strong>The studio recommends</strong> the change, in the editor&#8217;s words for the row: &#8220;60 to 85 percent; on a long page, screens of running text between the opening screens may hold more&#8221;.</p>
      </article>
      <article class="item">
        <span class="code">ED11-2</span>
        <h3>The wordmark at 360 px against Rule 03.6</h3>
        <p>Rule 03.6 sets L1, the wordmark alone, from its 24 px master on a site under 48em, 768 px. At 360 px that master clears Menu by 4 px, so chapter 20 draws L1 from the 16 px master on screens under 390 px. The two rules disagree at 360 px.</p>
        <p class="rec"><strong>The studio recommends</strong> keeping the 16 px master at 360 px, as the guide&#8217;s own masthead has done through 372 px since your reply 10 on board 3 (DR-291), and adding the exception to Rule 03.6 as a row: &#8220;Site, under 24.375em: L1 from the 16 px master, 152 px wide&#8221;.</p>
      </article>
      <article class="item">
        <span class="code">DD11-NF1</span>
        <h3>Rule 01.22&#8217;s &#8220;same length&#8221; where the record holds one side</h3>
        <p>Rule 01.22 asks a process piece to set out what supporters and opponents have said at the same length. The FDA&#8217;s rule on NAC records no objector, so equal length would mean writing an opponent the record lacks. The Act page follows DR-93, one standard of evidence with no invented counterweight, and prints the record at its own length (D4-108).</p>
        <p class="rec"><strong>The studio recommends</strong> that Rule 01.22 read &#8220;sets out what the record shows from each side, at the length the record holds&#8221;, the wording chapter 20&#8217;s Rule 20.8 already uses.</p>
      </article>
      <article class="item">
        <span class="code">ED-F1</span>
        <h3>A layer color in the atlas</h3>
        <p>The creative director&#8217;s finishing list for the atlas asks for a colored rule down each part box, Prussian, Verdigris or Stone by layer, to give the atlas a signature of its own. Rule 15.25&#8217;s approved resolution (G3-03) reads &#8220;Layers coded by a frame and a name, never a color&#8221;, so chapter 21&#8217;s plan frames the parts as Rule 15.9 does.</p>
        <p class="rec"><strong>The studio recommends</strong> running the wall test first. In chat 12 the creative director covers the wordmark on chapter 21&#8217;s built views and asks whether they still read as ours. The question comes to you only if that test fails, as a choice between reopening Rule 15.25&#8217;s row for color and keeping the frames.</p>
      </article>
      <article class="item">
        <span class="code">AL11-1</span>
        <h3>Chapter 18&#8217;s menu: the current-page mark</h3>
        <p>Rule 18.6 marks the part a reader is in with <code>aria-current="page"</code>, the code a screen reader announces as &#8220;current page&#8221;. On the article, which sits inside Explain, a screen reader calls the Explain link the current page, though it leads to Explain&#8217;s front page. The website follows Rule 18.6 as approved.</p>
        <p class="rec"><strong>The studio recommends</strong> the accessibility lead&#8217;s fix: &#8220;page&#8221; on a part&#8217;s own front page and &#8220;true&#8221;, announced as &#8220;current&#8221;, on the pages inside it. The bold words and the 2 px underline stay as they are.</p>
      </article>
      <article class="item">
        <span class="code">AL11-2</span>
        <h3>Chapter 18&#8217;s menu: the focus fix W1</h3>
        <p>The menu&#8217;s title row stays at the top while the menu scrolls, and the menu sets no scroll padding. At 320 by 256 px, the size a 1,280 px window reaches at 400 percent zoom, a part reached with Shift+Tab can sit hidden under the row, which fails WCAG 2.4.11, Focus Not Obscured. The website carries the fix in its own code, where a rerun found 0 hidden in 6 of 6 runs. Chapter 18&#8217;s own code is unchanged.</p>
        <p class="rec"><strong>The studio recommends</strong> the same scroll padding in chapter 18&#8217;s menu, so the guide&#8217;s component matches the website.</p>
      </article>
      <article class="item">
        <span class="code">C16-CD-01, held from chat 10</span>
        <h3>Chapter 01&#8217;s photographs in color</h3>
        <p>Rules 01.6 and 01.8 show their two federal photographs in color. Gate 1 set black and white by default, with color where color is evidence (S10), and chapter 16 follows S10, so the guide shows the same photographs two ways.</p>
        <p class="rec"><strong>The studio recommends</strong> the creative director&#8217;s grayscale on the three plates, a style change at no byte cost.</p>
      </article>
    </div>
    {{GUIDE_PANEL}}
  </section>
  </main>
</div>
'''

if __name__ == '__main__':
    main()
