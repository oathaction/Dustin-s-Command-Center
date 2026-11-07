"""Build the Board 6 hub (November 7, 2026): the page Dustin opens first for the four explorations after stage board A.

Usage:
    python3 -I work/build/scripts/phase-2/board6_hub_build.py [--strict] [--no-capture]
        [--board-dir DIR] [--content PATH] [--record PATH] [--out PATH] [--captures DIR] [--publish DIR]

Reads, from work/boards/phase-2/board-6/ (the board dir):
    20261107_Board-6-Content.json        the creative director's content (verdict, one entry per section, decisions)
    20261107_Board-6-Studio-Record.json  the main session's record (what was asked, process, checks, change log)
    tracker/ pillar-icons/ stacked/ color-sheets/   one finished section page in each, found as the folder's one .html
Their schema is in work/handoffs/phase-2/20261107_Board-6-Builder-Notes.md.

On every run board6_hub_capture.js opens each section page as it stands then, in a 1440 by 900 window at device
scale 2, and captures its lead comparison at true size. A section folder with no page yet gets a placeholder band and
a warning, so the hub builds while the color sheets are made and fills in on the first run after they land.
Writes:
    work/boards/20261107_Board-6-Explorations.html              the hub (captures and section pages by relative path)
    work/boards/phase-2/board-6/captures/                        the captures and the facts read from each page
    <scratchpad>/publish-board-6/index.html                      the publish copy of the hub, without its skeleton
    <scratchpad>/publish-board-6/<section>.html                  each section page, with a "Back to Board 6" link added
    <scratchpad>/publish-board-6/captures/, <section>/           the captures, and any file a section page references
    <scratchpad>/publish-board-6/files.json                      served path to source file, for every file but the page

Captures are shown at their CSS size, never scaled. Colors and type come from work/build/tokens/tokens.css, inlined.
The hub's own styles carry no red; the one red it draws is the wordmark's ampersand, marked as the signature.
--no-capture reuses the last captures (layout work only; the hub then says so). --strict exits 1 on any warning.
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261107'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad')
BOARD_DIR = ROOT / 'work/boards/phase-2/board-6'
OUT = ROOT / f'work/boards/{DATE}_Board-6-Explorations.html'
PUBLISH = SCRATCH / 'publish-board-6'
CAPTURE_JS = ROOT / 'work/build/scripts/phase-2/board6_hub_capture.js'
TOKENS = ROOT / 'work/build/tokens/tokens.css'
WORDMARK = ROOT / 'work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg'
TITLE = 'Board 6 Explorations'
STEM = f'{DATE}_Board-6-Hub-'
CAPTURE_W = 1440
MAX_PNG = 4_000_000
TALL = 1800        # a lead taller than this, in CSS px, warns: name a smaller element
MEASURE = 1312     # the hub's column at 1,440 px (82rem); a wider lead scrolls even on a desktop

# The four sections, in the brief's order. Dustin's words are quoted from the brief (DR-104 to DR-107).
SECTIONS = [
    {'key': 'tracker', 'short': 'Bill tracker', 'title': 'The grid keeps one job, and a simpler bill tracker',
     'defaults': ['#compare table.mx:not(.mx-c)', '#compare'],
     'caption': 'The four options side by side: your four bills as rows, each option drawn at 240 px, the width of a story card.',
     'asked': 'a bill tracker should be much simpler, like a line with dots or a 1, 2, 3, 4, 5, 6 step process. '
              'That grid system\'s not clear. I want everything to be clear.'},
    {'key': 'pillar-icons', 'short': 'Pillar icons', 'title': 'Four pillar icons from the Civic Line set',
     'defaults': ['#compare .cmp', '#compare'],
     'caption': 'The three sets in the pillar row at 48 px in one color, with each word and icon ID beside its icon.',
     'asked': 'revisit the civic icons. I\'d like to use those and maybe see just a few thoughts on the four icons for the four pillars.'},
    {'key': 'stacked', 'short': 'Stacked lockups', 'title': 'More stacked lockups',
     'defaults': ['.lead .cmp-grid', 'section.lead'],
     'caption': 'All six stacks beside today\'s L2, every one with capitals 33 px tall.',
     'asked': 'I don\'t know that I like that. Can you give me a few more variations of stacked?'},
    {'key': 'color-sheets', 'short': 'Color sheets', 'title': 'Six identity sheets in six color schemes',
     'defaults': ['#all-seven .thumbs-w', '#all-seven', '#compare'],
     'caption': 'All seven at once: the six new sheets and today\'s palette, side by side.',
     'asked': 'I want to see, if red wasn\'t at the forefront, what other colors would work.'},
]
KEYS = [s['key'] for s in SECTIONS]
SEC = {s['key']: s for s in SECTIONS}
RUBRIC = ['Craft', 'Clarity', 'Brand fidelity', 'Usefulness', 'Evidence honesty', 'Accessibility']
LOCKED = {
    'tagline': ('A country that answers to its people.', ['answers to its people']),
    'mission': ('Help people understand and improve the rules that shape their lives.', ['rules that shape their lives']),
    'promise': ('We explain how a decision is made and give you a practical way to take part.', ['how a decision is made and give']),
    'commitment': ('Clarity is our duty. Action is our promise.', ['Clarity is our duty', 'Action is our promise']),
}
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless']
SKIP_REF = re.compile(r'^(?:#|data:|https?:|//|mailto:|javascript:|about:|blob:|tel:)', re.I)

WARN = []
BUILDER_CHECKS = []


class BoardError(Exception):
    pass


def warn(msg):
    WARN.append(msg)
    print('warning', msg)


def need(cond, msg):
    if not cond:
        raise BoardError(msg)


# ------------------------------------------------------------------------------------------------ text
def copy(s):
    """Curly quotes and apostrophes, and the true minus before a figure (H07)."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    s = re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", '‘\\1’', s)
    return re.sub(r'(?<![\w.\-/])-(?=\d)', '−', s)


def esc(s):
    return html.escape(copy(s), quote=True)


def attr(s):
    return html.escape(str(s), quote=True)


N_DEC = 0   # decisions on the hub; B6-1 to B6-{N_DEC} in body text link to their cards


def md(s, links=True):
    """Escaped text with `code`, **bold**, {{illus}}, and each B6-n linked to its decision card."""
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f'\x00{len(codes) - 1}\x00'
    t = re.sub(r'`([^`]+)`', keep, str(s))
    t = html.escape(copy(t), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    if links:
        t = re.sub(r'(?<![\w/#.-])B6-([1-9]\d?)\b',
                   lambda m: f'<a href="#b6-{m.group(1)}">{m.group(0)}</a>' if int(m.group(1)) <= N_DEC else m.group(0), t)
    t = t.replace('{{illus}}', '<span class="chip chip--ill">Illustrative</span>')
    return re.sub(r'\x00(\d+)\x00', lambda m: f'<code>{html.escape(codes[int(m.group(1))])}</code>', t)


def paras(x, cls=''):
    items = x if isinstance(x, list) else [x] if x else []
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<p{c}>{md(p)}</p>' for p in items)


def words_date(d):
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def words_time(d):
    h = d.hour % 12 or 12
    return f'{h}:{d.minute:02d} {"a.m." if d.hour < 12 else "p.m."}'


def iso(s):
    return datetime.datetime.fromisoformat(str(s).replace('Z', '+00:00'))


def num_words(n):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][n] if 0 <= n < 10 else f'{n:,}'


def px(n):
    return f'{n:,}'


def join_words(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


# ------------------------------------------------------------------------------------------------ inputs
def strings(obj, path=''):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from strings(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from strings(v, f'{path}[{i}]')


def lint(obj, name, skip=('selector', 'page', 'command', 'url')):
    """Chapter 02's marks and locked lines on every string an input holds. Em dashes fail; flagged words warn."""
    for path, s in strings(obj):
        if path.split('.')[-1].split('[')[0] in skip or 'changelog' in path:
            continue
        need('\u2014' not in s, f'{name} {path}: an em dash (W21). Join the parts with a comma and a word, or end the sentence.')
        if '\u2013' in s or ' -- ' in s:
            warn(f'{name} {path}: an en dash or double hyphen; write "to" for a range')
        for w in FLAGGED:
            if re.search(rf'\b{w}\b', s, flags=re.I):
                warn(f'{name} {path}: "{w}" is on the writing rules\' list (W17, W18, W20)')
        for key, (line, frags) in LOCKED.items():
            for f in frags:
                if f.lower() in s.lower() and line not in copy(s).replace('’', "'") and line not in s:
                    raise BoardError(f'{name} {path}: quotes the {key} inexactly. It reads "{line}" (H01).')


def text_or_list(x):
    return (isinstance(x, str) and x.strip()) or (isinstance(x, list) and x and all(isinstance(p, str) and p.strip() for p in x))


def option_index(r, n):
    if isinstance(r, int) and not isinstance(r, bool) and 1 <= r <= n:
        return r - 1
    if isinstance(r, str) and re.fullmatch(r'[a-h]', r.strip().lower()) and ord(r.strip().lower()) - 97 < n:
        return ord(r.strip().lower()) - 97
    return None


def parse_touch(ref):
    """'tracker', 'tracker#option-b' or {"section": ..., "anchor": ...} to (key, anchor or None)."""
    if isinstance(ref, dict):
        return str(ref.get('section', '')).strip(), (str(ref['anchor']).strip().lstrip('#') if ref.get('anchor') else None)
    k, _, a = str(ref).strip().partition('#')
    return k.strip(), (a.strip() or None)


def check_content(C):
    need(isinstance(C, dict), 'the content file must hold one JSON object')
    need(isinstance(C.get('deck'), str) and C['deck'].strip(), 'content.deck: one or two sentences under the title')
    v = C.get('verdict')
    need(isinstance(v, dict) and isinstance(v.get('headline'), str) and v['headline'].strip(), 'content.verdict.headline: the verdict in one sentence')
    need(v.get('text') is None or text_or_list(v['text']), 'content.verdict.text: a string or a list of paragraphs')
    if 'scores' in C:
        sc = C['scores']
        need(isinstance(sc, list) and len(sc) == len(RUBRIC), f'content.scores: six entries in this order: {", ".join(RUBRIC)}')
        for i, (s, crit) in enumerate(zip(sc, RUBRIC)):
            need(isinstance(s, dict) and s.get('criterion') == crit, f'content.scores[{i}].criterion must be "{crit}"')
            need(isinstance(s.get('score'), int) and 1 <= s['score'] <= 5, f'content.scores[{i}].score: a whole number from 1 to 5')
            need(isinstance(s.get('line'), str) and s['line'].strip(), f'content.scores[{i}].line: the reason, one line')
    S = C.get('sections')
    need(isinstance(S, dict) and S, f'content.sections: an object with an entry for each section, keyed {", ".join(KEYS)}')
    for k in S:
        need(k in KEYS, f'content.sections["{k}"]: not a section of Board 6; the keys are {", ".join(KEYS)}')
    for k, e in S.items():
        tag = f'content.sections["{k}"]'
        need(isinstance(e, dict), f'{tag}: an object')
        need(text_or_list(e.get('summary')), f'{tag}.summary: what the section made, a string or a list of paragraphs')
        need(e.get('recommendation') is None or (isinstance(e['recommendation'], str) and e['recommendation'].strip()),
             f'{tag}.recommendation: the recommendation, one or two sentences')
        for f in ('pick', 'title', 'short', 'page'):
            need(e.get(f) is None or (isinstance(e[f], str) and e[f].strip()), f'{tag}.{f}: a non-empty string when given')
        for f in ('why', 'note'):
            need(e.get(f) is None or text_or_list(e[f]), f'{tag}.{f}: a string or a list of paragraphs when given')
        need(e.get('asked') is None or e['asked'] is False or (isinstance(e['asked'], str) and e['asked'].strip()),
             f'{tag}.asked: Dustin\'s words as a string, or false to leave the quote out')
        ld = e.get('lead')
        if ld is not None:
            need(isinstance(ld, dict), f'{tag}.lead: {{"selector": ..., "caption": ..., "alt": ...}}')
            for f in ('selector', 'caption', 'alt'):
                need(ld.get(f) is None or (isinstance(ld[f], str) and ld[f].strip()), f'{tag}.lead.{f}: a non-empty string when given')
            if ld.get('selector') and not ld.get('caption'):
                warn(f'{tag}.lead names its own selector but no caption; the band would print the default caption for another element')
    d = C.get('decisions')
    need(isinstance(d, list) and d, 'content.decisions: at least one decision')
    for i, x in enumerate(d):
        tag = f'content.decisions[{i}]'
        need(isinstance(x, dict), f'{tag}: an object')
        if 'id' in x:
            need(x['id'] == f'B6-{i + 1}', f'{tag}.id: decisions are numbered in order, so this one is B6-{i + 1}')
        need(isinstance(x.get('question'), str) and x['question'].strip(), f'{tag}.question: the question for Dustin')
        o = x.get('options')
        need(isinstance(o, list) and 2 <= len(o) <= 8, f'{tag}.options: two to eight options')
        for j, op in enumerate(o):
            need((isinstance(op, str) and op.strip()) or (isinstance(op, dict) and isinstance(op.get('text'), str) and op['text'].strip()),
                 f'{tag}.options[{j}]: a string, or {{"text": ..., "short": ...}}')
        r = x.get('recommended')
        need(r is not None, f'{tag}.recommended: the recommended option, as its letter ("b") or its number (2)')
        need(option_index(r, len(o)) is not None, f'{tag}.recommended: "{r}" names no option; use a letter from a to {chr(96 + len(o))}')
        need(isinstance(x.get('why'), str) and x['why'].strip(), f'{tag}.why: the reason for the recommendation')
        need(x.get('context') is None or text_or_list(x['context']), f'{tag}.context: a string or a list of paragraphs when given')
        if x.get('section') is not None:
            need(x['section'] in KEYS, f'{tag}.section: "{x["section"]}" is not a section; use one of {", ".join(KEYS)}')
        need(isinstance(x.get('touches', []), list), f'{tag}.touches: a list such as ["tracker#option-b"]')
        for ref in x.get('touches', []):
            k, _ = parse_touch(ref)
            need(k in KEYS, f'{tag}.touches: "{ref}" names no section; write "tracker#option-b" or {{"section": "tracker", "anchor": "option-b"}}')
        if not x.get('section') and not x.get('touches'):
            warn(f'{tag} names no section and no place on a section page')
    need(C.get('ask') is None or (isinstance(C['ask'], list) and all(isinstance(a, str) and a.strip() for a in C['ask'])), 'content.ask: a list of lines')
    lint(C, 'content')


def check_record(R):
    need(isinstance(R, dict), 'the studio record must hold one JSON object')
    need(isinstance(R.get('asked'), list) and R['asked'] and all(isinstance(a, str) and a.strip() for a in R['asked']), 'record.asked: what was asked, at least one line')
    pr = R.get('process', [])
    need(isinstance(pr, list) and all(isinstance(p, dict) and isinstance(p.get('stage'), str) and p['stage'].strip() and text_or_list(p.get('text')) for p in pr),
         'record.process: a list of {"stage": ..., "text": ...}')
    ck = R.get('checks')
    need(isinstance(ck, list) and ck and all(isinstance(c, dict) and c.get('name') and c.get('result') for c in ck), 'record.checks: a list of {"name": ..., "result": ...}')
    for i, c in enumerate(ck):
        need(c.get('pass') in (None, True, False), f'record.checks[{i}].pass: true, false or left out')
    need(isinstance(R.get('not_tested'), list) and R['not_tested'], 'record.not_tested: at least one line')
    cl = R.get('changelog')
    need(isinstance(cl, dict) and isinstance(cl.get('created'), list) and isinstance(cl.get('modified'), list), 'record.changelog: {"created": [...], "modified": [...]}')
    lint(R, 'record')


# ------------------------------------------------------------------------------------------------ section pages
def find_page(board_dir, key, entry):
    folder = board_dir / key
    if entry and entry.get('page'):
        p = folder / entry['page']
        need(p.is_file(), f'content.sections["{key}"].page: no file {p}')
        return p
    if not folder.is_dir():
        return None
    pages = sorted(p for p in folder.glob('*.html') if p.is_file())
    need(len(pages) <= 1, f'{folder} holds {len(pages)} pages ({", ".join(p.name for p in pages)}); name the one to use in content.sections["{key}"].page')
    return pages[0] if pages else None


def page_check(page):
    """The section page's own dataviz_check result, read from the JSON its check wrote beside it."""
    res = page.with_name(page.stem + '-Check-Results.json')
    if not res.exists():
        return None
    try:
        r = json.loads(res.read_text())
    except ValueError:
        return {'file': res, 'error': 'unreadable'}
    widths = sorted({run.get('width') for run in r.get('runs', []) if run.get('width')}, reverse=True)
    checked = iso(r['checked']) if r.get('checked') else None
    mtime = datetime.datetime.fromtimestamp(page.stat().st_mtime, datetime.timezone.utc)
    return {'file': res, 'pass': r.get('pass'), 'failures': len(r.get('failures', [])), 'widths': widths, 'checked': checked,
            'stale': bool(checked and mtime > checked + datetime.timedelta(seconds=2))}


def run_capture(jobs, cap_dir, no_capture):
    facts_path = cap_dir / f'{STEM}Capture-Facts.json'
    if no_capture:
        need(facts_path.exists(), f'--no-capture: no earlier captures in {cap_dir}')
        warn('captures reused from an earlier run (--no-capture)')
        facts = json.loads(facts_path.read_text())
        for j in jobs:
            need(j['key'] in facts['sections'], f'--no-capture: the earlier run captured no {j["key"]} page')
        return facts, True
    cap_dir.mkdir(parents=True, exist_ok=True)
    for old in list(cap_dir.glob(f'{STEM}*.png')) + list(cap_dir.glob(f'{STEM}*.jpg')):
        old.unlink()
    job = {'out': str(cap_dir), 'facts': str(facts_path), 'width': CAPTURE_W, 'height': 900, 'scale': 2, 'max_png_bytes': MAX_PNG, 'sections': jobs}
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(job, f)
        jp = f.name
    try:
        r = subprocess.run(['node', str(CAPTURE_JS), jp], cwd=ROOT, capture_output=True, text=True, timeout=900)
    finally:
        os.unlink(jp)
    print(r.stdout.strip())
    if not facts_path.exists():
        raise BoardError(f'the capture script wrote no facts: {r.stderr.strip()[-600:]}')
    facts = json.loads(facts_path.read_text())
    if r.returncode != 0:
        lines = [f'{k}: {e}' for k, s in facts['sections'].items() for e in s.get('errors', [])]
        hint = []
        for k, s in facts['sections'].items():
            if not s.get('lead'):
                ids = [i for i, v in s.get('ids', {}).items() if v['tag'] in ('section', 'figure', 'div', 'table', 'article')][:24]
                hint.append(f'{k}: name the lead in content.sections["{k}"].lead.selector, or mark it on the page with data-board-lead. '
                            f'Ids on the page: {", ".join(ids) or "none"}')
        raise BoardError('the capture script failed:\n  ' + '\n  '.join(lines + hint or [r.stderr.strip()[-600:]]))
    return facts, False


# ------------------------------------------------------------------------------------------------ publish copies
def back_link(colors):
    css = (f'<style id="b6-back-style">.b6-back{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 24px;margin:0 0 16px;padding:0;background:transparent}}'
           f'.b6-back a{{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 8px 0 0;background:{colors["newsprint"]};'
           f'color:{colors["ink"]};font:600 15px/1.2 Inter,Arial,sans-serif;letter-spacing:0;text-decoration:none}}'
           f'.b6-back .t{{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.2em}}'
           f'.b6-back a:hover .t{{text-decoration-thickness:2px}}'
           f'.b6-back a:focus-visible{{outline:2px solid {colors["ring"]};outline-offset:2px}}'
           f'@media print{{.b6-back{{display:none}}}}</style>')
    nav = ('<nav class="b6-back" aria-label="Board 6"><a href="index.html"><span aria-hidden="true">←</span>'
           '<span class="t">Back to Board 6</span></a></nav>')
    return css, nav


REF_ATTR = re.compile(r'(\s(?:src|href|xlink:href|poster)\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
REF_SRCSET = re.compile(r'(\ssrcset\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
REF_URL = re.compile(r'url\(\s*(["\']?)([^"\')]*)\1\s*\)', re.I)


def publish_section(key, page, pub_dir, section_pages, colors):
    """Copy a section page to <key>.html with the back link, and every local file it references to <key>/..."""
    text = page.read_text()
    files = {}
    missing = []

    def remap(val):
        raw = html.unescape(val).strip()
        if not raw or SKIP_REF.match(raw):
            return val
        base, frag = (raw.split('#', 1) + [''])[:2]
        base = base.split('?', 1)[0]
        if not base:
            return val
        src = (page.parent / base).resolve()
        for k, p in section_pages.items():
            if p and src == p.resolve():
                return attr(f'{k}.html' + (f'#{frag}' if frag else ''))
        if not src.is_file():
            missing.append(raw)
            return val
        try:
            rel = src.relative_to(page.parent.resolve()).as_posix()
        except ValueError:
            rel = f'linked/{src.name}'
        served = f'{key}/{rel}'
        if served in files and files[served] != src:
            served = f'{key}/linked/{hashlib.sha1(str(src).encode()).hexdigest()[:8]}-{src.name}'
        files[served] = src
        return attr(served + (f'#{frag}' if frag else ''))

    text = REF_ATTR.sub(lambda m: m.group(1) + m.group(2) + remap(m.group(3)) + m.group(2), text)
    text = REF_SRCSET.sub(lambda m: m.group(1) + m.group(2) + ', '.join(
        ' '.join([remap(part.strip().split()[0])] + part.strip().split()[1:]) for part in m.group(3).split(',') if part.strip()) + m.group(2), text)
    text = REF_URL.sub(lambda m: f'url({m.group(1)}{remap(m.group(2))}{m.group(1)})', text)
    css, nav = back_link(colors)
    need(re.search(r'</head>', text, flags=re.I), f'{page.name}: no </head> to add the back link\'s style to')
    text = re.sub(r'</head>', lambda m: css + m.group(0), text, count=1, flags=re.I)
    m = re.search(r'<main\b[^>]*>', text, flags=re.I) or re.search(r'<body\b[^>]*>', text, flags=re.I)
    need(m, f'{page.name}: no <main> or <body> to put the back link in')
    text = text[:m.end()] + nav + text[m.end():]
    out = pub_dir / f'{key}.html'
    out.write_text(text)
    for served, src in files.items():
        dst = pub_dir / served
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for x in missing:
        warn(f'the {key} page references "{x}", which does not exist beside it, so the published copy cannot load it')
    return out, files


def token_colors(tokens_css):
    vals = dict(re.findall(r'(--oa-[\w-]+):\s*([^;]+);', tokens_css))

    def res(name, depth=0):
        v = vals.get(name, '').strip()
        m = re.fullmatch(r'var\((--oa-[\w-]+)\)', v)
        return res(m.group(1), depth + 1) if m and depth < 8 else v
    return {'newsprint': res('--oa-color-surface-newsprint'), 'ink': res('--oa-color-text-primary-on-newsprint'),
            'ring': res('--oa-color-focus-ring-on-newsprint')}


# ------------------------------------------------------------------------------------------------ page parts
HREF = {}       # section key to the page's address in this render ('' when the page is missing)
CAP_PREFIX = ''


def sec_href(key, anchor=None):
    base = HREF.get(key)
    return f'{base}#{anchor}' if base and anchor else base


def wordmark():
    svg = WORDMARK.read_text().strip()
    svg = re.sub(r'<title>.*?</title>', '', svg)
    svg = svg.replace('<svg ', '<svg class="wm" role="img" aria-label="Oath &amp; Action" focusable="false" width="221" height="24" ', 1)
    return f'<span class="wm-wrap" data-red="signature">{svg}</span>'


def frame(inner, name, pad=24):
    """A frame that holds a capture at true size, on a Newsprint mat, and scrolls sideways when the window is narrower."""
    return (f'<p class="hint caption" hidden>Wider than this window. Scroll inside the frame to see all of it.</p>'
            f'<div class="frame" role="region" tabindex="0" aria-label="{attr(name)}" style="--pad:{pad}px">{inner}</div>')


def section(sid, title, body, num=None, kicker=None, extra=''):
    n = f'<span class="n">{num}</span> ' if num else ''
    k = f'<p class="label kick">{esc(kicker)}</p>' if kicker else ''
    return (f'<section class="sec{extra}" id="{sid}" aria-labelledby="{sid}-h">{k}<h2 class="sec-h" id="{sid}-h">{n}'
            f'<span class="t">{esc(title)}</span></h2>{body}</section>')


def note_block(text, who='Creative director'):
    items = text if isinstance(text, list) else [text]
    return (f'<figure class="note"><blockquote>{"".join(f"<p>{md(p)}</p>" for p in items)}</blockquote>'
            f'<figcaption class="caption">{esc(who)}</figcaption></figure>')


def pips(score):
    cells = ''.join(f'<i class="{"on" if k < score else ""}"></i>' + ('<b></b>' if k == 2 else '') for k in range(5))
    return f'<span class="pips" aria-hidden="true">{cells}</span>'


def sec_info(C, key):
    e = (C.get('sections') or {}).get(key) or {}
    s = SEC[key]
    return e, e.get('short') or s['short'], e.get('title') or s['title']


def verdict_section(C, present):
    v = C['verdict']
    body = f'<p class="v-head">{md(v["headline"])}</p>{paras(v.get("text"))}'
    if C.get('scores'):
        sc = C['scores']
        rows = ''.join(
            f'<li><span class="sc-k">{esc(s["criterion"])}</span><span class="sc-v"><span class="sc-n">{s["score"]}</span>'
            f'<span class="caption">of 5</span>{pips(s["score"])}</span><span class="sc-line">{md(s["line"])}</span></li>' for s in sc)
        body += (f'<h3 class="sub">The six criteria</h3><p class="caption legend">The creative director scores each criterion from 1 to 5 on the brief’s rubric. '
                 f'In each row of squares, the upright rule after the third square marks the ship line of 4.</p><ol class="scores">{rows}</ol>')
    cells = ''
    for i, key in enumerate(KEYS, 1):
        e, short, title = sec_info(C, key)
        if key in present and e:
            pick = md(e.get('pick') or e['recommendation'])
            state = f'<p class="gl-p">{pick}</p>'
        else:
            state = '<p class="gl-p gl-wait">The page is still being made.</p>'
        cells += (f'<li><p class="gl-n" aria-hidden="true">{i}</p><h3 class="gl-t"><a href="#{key}"><span class="vh">Section {i}, </span>{esc(short)}</a></h3>'
                  f'<p class="label gl-k">We recommend</p>{state}</li>')
    body += f'<h3 class="sub">The four recommendations</h3><ol class="glance">{cells}</ol>'
    return section('verdict', 'Verdict', body)


def lead_figure(key, short, e, lead, captured):
    ld = e.get('lead') or {}
    cap = ld.get('caption') or SEC[key]['caption']
    w, h = lead['css_w'], lead['css_h']
    alt = ld.get('alt') or (f'Capture of the {short.lower()} page at a 1,440 px window, shown at true size. {copy(cap)} '
                            f'The full section page holds every option.')
    img = (f'<img src="{attr(CAP_PREFIX + lead["file"])}" width="{w}" height="{h}" alt="{attr(copy(alt))}" loading="lazy" decoding="async">')
    when = f'{words_date(captured)} at {words_time(captured)} UTC'
    return (f'<figure class="lead"><figcaption class="vcap"><span class="vk">Lead comparison</span><span class="vt">{md(cap)}</span>'
            f'<span class="vs caption">{px(w)} by {px(h)} px, true size</span></figcaption>'
            f'{frame(img, f"{short}, lead comparison at true size", mat(w))}'
            f'<p class="caption cap-note">Captured from the section page in a 1,440 px window on {when}. '
            f'<a href="{attr(sec_href(key))}">Open the full {esc(short.lower())} page</a> to see every option and its sizes.</p></figure>')


def mat(w):
    """The mat around a capture: 24 px, or less so a capture that fits the 1,440 px column still fits with its mat."""
    return max(8, min(24, (MEASURE - 2 - w) // 2)) if w <= MEASURE - 2 - 16 else 8


def check_line(chk):
    if not chk:
        return '<p class="caption chk">No check result sits beside the section page, so the hub cannot say whether it passed.</p>'
    if chk.get('error'):
        return '<p class="caption chk">The section page’s check result could not be read.</p>'
    ws = join_words([px(w) for w in chk['widths']]) + ' px' if chk['widths'] else 'its widths'
    when = f'{words_date(chk["checked"])} at {words_time(chk["checked"])} UTC' if chk['checked'] else 'an unknown time'
    if chk['pass']:
        s = f'The section page’s own check, run on {when}, passed at {ws}.'
    else:
        s = f'The section page’s own check, run on {when}, found {num_words(chk["failures"])} failure{"s" if chk["failures"] != 1 else ""}.'
    if chk['stale']:
        s += ' The page changed after that check ran.'
    return f'<p class="caption chk">{s}</p>'


def band(C, i, key, present, facts, checks, dec_by_sec):
    e, short, title = sec_info(C, key)
    asked = e.get('asked') if e.get('asked') is not None else SEC[key]['asked']
    quote = ''
    if asked:
        quote = (f'<figure class="asked"><blockquote><p>“{esc(asked)}”</p></blockquote>'
                 f'<figcaption class="caption">Your words, November 7, 2026</figcaption></figure>')
    kicker = f'Section {i} of 4'
    if key not in present:
        summ = f'<p class="label">What we are making</p>{paras(e.get("summary"))}' if e.get('summary') else ''
        body = (f'<div class="band-top">{quote}<div class="band-sum">{summ}'
                f'<div class="wait" role="note"><p>The {esc(short.lower())} page is still being made. When it lands, the next build of this hub adds '
                f'its lead comparison at true size and a link to the full page, with our recommendation.</p></div></div></div>')
        return section(key, title, body, num=str(i), kicker=kicker, extra=' band band--wait')
    f = facts['sections'][key]
    captured = iso(facts['captured'])
    note = note_block(e['note']) if e.get('note') else ''
    top = (f'<div class="band-top">{quote}<div class="band-sum"><p class="label">What we made</p>'
           f'{paras(e["summary"], "lede")}{note}</div></div>')
    fig = lead_figure(key, short, e, f['lead'], captured)
    decs = dec_by_sec.get(key, [])
    dl = ''
    if decs:
        dl = (f'<p class="label">Decisions for you</p><ul class="declinks">'
              + ''.join(f'<li><a href="#b6-{n}"><b>B6-{n}</b> {md(q, links=False)}</a></li>' for n, q in decs) + '</ul>')
    why = f'<p class="label">Why</p>{paras(e["why"])}' if e.get('why') else ''
    rec = (f'<div class="pick"><div class="pick-main"><p class="label">We recommend</p><p class="pick-h">{md(e["recommendation"])}</p></div>'
           f'<div class="pick-side">{why}{dl}<p class="go-row"><a class="go" href="{attr(sec_href(key))}">Open the full {esc(short.lower())} page'
           f'<span aria-hidden="true"> →</span></a></p><p class="caption page-name">The page: {esc(f.get("h1") or f.get("title") or short)}</p></div></div>')
    return section(key, title, top + fig + rec + check_line(checks.get(key)), num=str(i), kicker=kicker, extra=' band')


def touch_link(ref, facts, present):
    k, a = parse_touch(ref)
    short = sec_info(CONTENT, k)[1]
    if k not in present:
        return f'<li><span>The {esc(short.lower())} page, still being made</span></li>'
    if not a:
        return f'<li><a href="{attr(sec_href(k))}">The full {esc(short.lower())} page</a></li>'
    label = facts['sections'][k]['ids'][a]['label'] or a
    return f'<li><a href="{attr(sec_href(k, a))}">{esc(label)}, on the {esc(short.lower())} page</a></li>'


def decisions_section(C, sample, facts, present):
    decs = C['decisions']
    n = len(decs)
    cards = []
    for i, d in enumerate(decs):
        did = f'B6-{i + 1}'
        rec = option_index(d['recommended'], len(d['options']))
        opts, radios = '', ''
        for j, op in enumerate(d['options']):
            text = op if isinstance(op, str) else op['text']
            short = (op.get('short') if isinstance(op, dict) else None) or text
            letter = chr(97 + j)
            chip = ' <span class="chip">Recommended</span>' if j == rec else ''
            opts += f'<li><span class="ol">({letter})</span><span>{md(text)}{chip}</span></li>'
            radios += (f'<label class="rad"><input type="radio" name="ans-{did}" value="{letter}" data-short="{attr(copy(short))}">'
                       f'<span>({letter}) {esc(short if len(short) <= 90 else short[:87].rsplit(" ", 1)[0] + "…")}{" · recommended" if j == rec else ""}</span></label>')
        where = []
        if d.get('section'):
            k = d['section']
            where.append(f'<li><a href="#{k}">Section {KEYS.index(k) + 1}, {esc(sec_info(C, k)[1])}, on this hub</a></li>')
        where += [touch_link(ref, facts, present) for ref in d.get('touches', [])]
        ctx = paras(d.get('context'))
        rop = d['options'][rec]
        recline = md(d['recommendation']) if d.get('recommendation') else f'({chr(97 + rec)}) ' + md(rop if isinstance(rop, str) else rop['text'])
        src = f'<p class="caption">{md(d["source"])}</p>' if d.get('source') else ''
        cards.append(f'''<li class="dec" id="b6-{i + 1}" data-dec="{did}" data-rec="{chr(97 + rec)}">
<div class="dec-n" aria-hidden="true">{did}</div><div class="dec-b">
<div class="dec-main"><h3 class="dec-q"><span class="vh">{did}. </span>{md(d["question"], links=False)}</h3>{ctx}
<p class="label">Options</p><ol class="opts">{opts}</ol>
<div class="rec"><p><span class="label">We recommend</span> {recline}</p><p><span class="label">Why</span> {md(d["why"])}</p></div>
{f'<p class="label">Where to look</p><ul class="touch">{"".join(where)}</ul>' if where else ''}{src}</div>
<fieldset class="ans"><legend>Your answer to {did}</legend><div class="rads">{radios}</div>
<label class="nl" for="note-{did}">A note, or an answer of your own</label><textarea id="note-{did}" rows="2" data-note="{did}"></textarea></fieldset></div></li>''')
    reply = f'''<div class="reply oa-surface-prussian" id="reply" role="region" aria-labelledby="reply-h">
<h3 id="reply-h">Your reply</h3>
<p>The answers you mark above collect here, ready to paste into our chat. Your marks stay in this browser only. Until you mark one, the box holds a sample reply.</p>
<label class="label" for="reply-text">Reply</label>
<textarea id="reply-text" rows="{min(max(n, 3), 14)}" readonly data-sample="{attr(copy(sample))}">{esc(sample)}</textarea>
<div class="reply-row"><button type="button" id="copy-reply">Copy the reply</button><span id="copy-status" role="status" aria-live="polite"></span></div></div>'''
    count = num_words(n).capitalize() if n < 10 else str(n)
    intro = (f'<p class="intro">{count} decision{"s wait" if n != 1 else " waits"} for you, numbered B6-1{f" to B6-{n}" if n > 1 else ""}. '
             f'Each card gives the question, the options and our recommendation with its reason, and links to the place on a section page '
             f'where you can see what it changes. Mark an answer on a card and it joins your reply at the end of this section.</p>')
    return section('decisions', 'Decisions', f'{intro}<ol class="decs">{"".join(cards)}</ol>{reply}')


def record_section(R):
    asked = ''.join(f'<li>{md(x)}</li>' for x in R['asked'])
    proc = ''.join(f'<li><span class="label">{esc(p["stage"])}</span><div>{paras(p["text"])}</div></li>' for p in R.get('process', []))
    proc_block = f'<div><h3 class="sub">How the work was done</h3><ol class="process">{proc}</ol></div>' if proc else ''
    checks = ''.join(f'<tr><th scope="row">{md(c["name"])}{"<br><code>" + html.escape(c["command"]) + "</code>" if c.get("command") else ""}</th>'
                     f'<td>{"<b>Pass.</b> " if c.get("pass") is True else "<b>Fail.</b> " if c.get("pass") is False else ""}{md(c["result"])}</td></tr>' for c in R['checks'])
    bchecks = ''.join(f'<li>{esc(x)}</li>' for x in BUILDER_CHECKS)
    nt = ''.join(f'<li>{md(x)}</li>' for x in R['not_tested'])
    cl = R['changelog']
    path = lambda x: f'<li><code>{html.escape(str(x))}</code></li>' if re.fullmatch(r'[\w./ -]+', str(x)) and '/' in str(x) else f'<li>{md(x)}</li>'
    created = ''.join(path(x) for x in cl['created']) or '<li>None</li>'
    modified = ''.join(path(x) for x in cl['modified']) or '<li>None</li>'
    body = f'''<div class="rec-grid"><div><h3 class="sub">What was asked</h3><ul class="facts">{asked}</ul></div>{proc_block}</div>
<h3 class="sub">Checks run</h3><div class="tw" role="region" tabindex="0" aria-label="Checks run"><table class="ck-t"><thead><tr><th scope="col">Check</th><th scope="col">Result</th></tr></thead><tbody>{checks}</tbody></table></div>
<div class="cols"><div><h3 class="sub">Checks the hub builder ran</h3><ul class="facts">{bchecks}</ul></div><div><h3 class="sub">Not tested</h3><ul class="facts">{nt}</ul></div></div>
<h3 class="sub">Change log</h3><p class="caption">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts files">{created}</ul></div><div><h4>Modified</h4><ul class="facts files">{modified}</ul></div></div>'''
    return section('record', 'Studio record', body)


CSS = r'''
/* Board 6 hub. Stage board A's frame on Newsprint: the grid margins of tokens.css, the title, section, H3 and H4
   styles, Lora Italic only for quoted words, hairlines in Stone, White for cards, and one Prussian panel for the reply.
   Captures sit at true size in frames that scroll sideways on narrow windows. The only red is the wordmark's ampersand. */
:root{--m:var(--oa-layout-grid-phone-small-margin);--g:var(--oa-layout-grid-phone-small-gutter);--max:82rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace}
@media (min-width:24.375em){:root{--m:var(--oa-layout-grid-phone-margin);--g:var(--oa-layout-grid-phone-gutter)}}
@media (min-width:48em){:root{--m:var(--oa-layout-grid-tablet-margin);--g:var(--oa-layout-grid-tablet-gutter)}}
@media (min-width:64em){:root{--m:var(--oa-layout-grid-desktop-margin);--g:var(--oa-layout-grid-desktop-gutter)}}
@media (min-width:90em){:root{--m:var(--oa-layout-grid-wide-margin);--g:var(--oa-layout-grid-wide-gutter)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--oa-color-surface-newsprint)}
body{margin:0;background:var(--oa-color-surface-newsprint);color:var(--ink);font:var(--oa-type-body);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration-thickness:var(--oa-border-width-underline);text-underline-offset:.2em}
a:hover{text-decoration-thickness:var(--oa-border-width-underline-hover)}
:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring-on-newsprint);outline-offset:var(--oa-border-focus-offset)}
.oa-surface-prussian :focus-visible{outline-color:var(--oa-color-focus-ring-on-prussian)}
.dec :focus-visible,.pick :focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
p{margin:0 0 var(--oa-space-200);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
code{font:500 .875rem/1.4 var(--mono);overflow-wrap:anywhere}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
[hidden]{display:none!important}
.board{max-width:calc(var(--max) + 2 * var(--m));margin:0 auto;padding:0 var(--m) var(--oa-space-1300)}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2)}
.caption{font:var(--oa-type-caption);color:var(--ink-2)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.n{color:var(--ink-2);font-variant-numeric:tabular-nums}
/* masthead and cover */
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-150) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong);margin:0}
.wm-wrap{display:inline-flex;color:var(--ink);--amp:var(--oa-color-identity-signature-on-newsprint)}
.wm{display:block;width:221px;height:24px}
.cover{padding:var(--oa-space-800) 0 0}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-400);max-width:13ch;text-wrap:balance}
.cover .intro{margin-bottom:var(--oa-space-200)}
.sample{border:var(--oa-border-width-rule) solid var(--strong);padding:var(--oa-space-200) var(--oa-space-300);margin:var(--oa-space-400) 0 0;background:var(--white)}
.sample p{margin:0}
.ask{background:var(--white);border:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-300) var(--oa-space-400);margin:var(--oa-space-500) 0 0;max-width:52rem}
.ask h2{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-200)}
.ask ol{margin:0 0 var(--oa-space-200);padding-left:1.4em}.ask li{margin:0 0 var(--oa-space-100);max-width:var(--oa-layout-measure-intro-max)}
.ask .q{font:italic 400 1.125rem/1.5 var(--oa-font-family-quote);margin:0}
.toc{margin:var(--oa-space-500) 0 0;border-top:var(--oa-border-width-hairline) solid var(--hair);border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.toc ol{list-style:none;margin:0;padding:var(--oa-space-100) 0;display:flex;flex-wrap:wrap;gap:0 var(--oa-space-400)}
.toc a{display:inline-flex;align-items:center;gap:.5em;min-height:var(--oa-size-target-touch);font:var(--oa-type-ui);text-decoration:none}
.toc a:hover{text-decoration:underline}
/* sections, in the guide's chapter rhythm */
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-400)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:0 0 var(--oa-space-500);text-wrap:balance;max-width:20ch}
.kick{margin:0 0 var(--oa-space-200)}
h3,.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;text-wrap:balance}
.sub{margin:var(--oa-space-800) 0 var(--oa-space-300)}
.sec-h + .cols > div:first-child > .sub:first-child,.sec-h + .rec-grid > div:first-child > .sub:first-child{margin-top:0}
@media (min-width:64em){.sec-h + .cols > div > .sub:first-child,.sec-h + .rec-grid > div > .sub:first-child{margin-top:0}}
h4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-300) 0 var(--oa-space-150)}
.cols{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-800)}
@media (min-width:64em){.cols{grid-template-columns:repeat(2,minmax(0,1fr))}}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 var(--oa-space-150);max-width:var(--oa-layout-measure-body-max)}
ul.files li{list-style:none;margin-left:-1.1em}
.note{margin:var(--oa-space-400) 0 0;padding-left:var(--oa-space-300);border-left:var(--oa-border-width-rule) solid var(--strong);max-width:var(--oa-layout-measure-intro-max)}
.note blockquote{margin:0}.note blockquote p{font:italic 400 clamp(1.1875rem,1.12rem + .3vw,1.375rem)/1.5 var(--oa-font-family-quote);margin:0 0 var(--oa-space-150)}
.note figcaption{margin:0}
/* verdict */
.v-head{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);max-width:30ch;text-wrap:balance}
.legend{margin:0 0 var(--oa-space-200)}
ol.scores{list-style:none;margin:0;padding:0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
ol.scores li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:var(--oa-space-100) var(--oa-space-300);padding:var(--oa-space-200) 0;border-top:var(--oa-border-width-hairline) solid var(--hair);align-items:baseline}
.sc-k{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing)}
.sc-v{display:inline-flex;align-items:baseline;gap:var(--oa-space-100)}
.sc-n{font:var(--oa-type-h3);letter-spacing:0;font-variant-numeric:tabular-nums}
.sc-line{grid-column:1/-1;max-width:var(--oa-layout-measure-intro-max)}
.pips{display:inline-flex;gap:3px;align-items:center;margin-left:var(--oa-space-150);align-self:center}
.pips i{width:12px;height:12px;box-shadow:inset 0 0 0 1px var(--oa-color-graphic-subtle-on-newsprint)}
.pips i.on{background:var(--oa-color-graphic-essential-on-newsprint);box-shadow:none}
.pips b{width:2px;height:20px;background:var(--oa-color-graphic-essential-on-newsprint);margin:0 3px}
@media (min-width:48em){ol.scores li{grid-template-columns:13rem 11rem minmax(0,1fr)}.sc-line{grid-column:auto}}
ol.glance{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);border-top:var(--oa-border-width-rule) solid var(--strong)}
.glance li{padding:var(--oa-space-300) 0 var(--oa-space-400);border-bottom:var(--oa-border-width-hairline) solid var(--hair);display:grid;grid-template-columns:3.25rem minmax(0,1fr);align-content:start}
.glance li > *{grid-column:2}
.gl-n{grid-column:1!important;grid-row:1 / span 3;margin:0;font:var(--oa-type-h3);letter-spacing:0;color:var(--ink-2);font-variant-numeric:tabular-nums}
.gl-t{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-150)}
.gl-t a{text-decoration:none;display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);margin:-10px 0}
.gl-t a:hover{text-decoration:underline}
.gl-k{margin:0 0 var(--oa-space-050)}
.gl-p{margin:0;max-width:34ch}
.gl-wait{color:var(--ink-2)}
@media (min-width:48em){ol.glance{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:var(--oa-space-400)}}
@media (min-width:80em){ol.glance{grid-template-columns:repeat(4,minmax(0,1fr));column-gap:0}
  .glance li{border-bottom:0;grid-template-columns:minmax(0,1fr);padding:var(--oa-space-300) var(--oa-space-300) var(--oa-space-200)}
  .glance li > *{grid-column:1}.gl-n{grid-row:auto;margin:0 0 var(--oa-space-100)}
  .glance li + li{border-left:var(--oa-border-width-hairline) solid var(--hair)}.glance li:first-child{padding-left:0}}
/* bands */
.band .sec-h .n{margin-right:.08em}
.band-top{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-800);align-items:start}
@media (min-width:64em){.band-top{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}}
.asked{margin:0}
.asked blockquote{margin:0}
.asked blockquote p{font:italic 400 clamp(1.25rem,1.15rem + .45vw,1.625rem)/1.42 var(--oa-font-family-quote);margin:0 0 var(--oa-space-150);max-width:26ch;text-wrap:pretty}
.asked figcaption{margin:0}
.band-sum > .label{margin:0 0 var(--oa-space-100)}
.lede{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.lead{margin:var(--oa-space-800) 0 0;min-width:0}
.vcap{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--oa-space-050) var(--oa-space-200);margin:0 0 var(--oa-space-200);max-width:none}
.vk{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}
.vt{font:var(--oa-type-ui);font-weight:600;max-width:var(--oa-layout-measure-intro-max)}
.frame{overflow-x:auto;overflow-y:hidden;max-width:100%;width:max-content;padding:min(var(--pad,24px),var(--m));border:var(--oa-border-width-hairline) solid var(--hair);background:var(--oa-color-surface-newsprint)}
.frame img{display:block;max-width:none;height:auto}
.hint{margin:0 0 var(--oa-space-100)}
.cap-note{margin:var(--oa-space-150) 0 0;max-width:var(--oa-layout-measure-intro-max)}
.pick{margin:var(--oa-space-600) 0 0;background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);
  border-top:var(--oa-border-width-bar) solid var(--oa-color-border-strong-on-white);padding:var(--oa-space-300);display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-800)}
@media (min-width:48em){.pick{padding:var(--oa-space-400) var(--oa-space-500)}}
@media (min-width:64em){.pick{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}}
.pick .label{color:var(--oa-color-text-secondary-on-white);margin:0 0 var(--oa-space-100)}
.pick-h{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;max-width:24ch;text-wrap:balance}
.pick-side p{max-width:none}
.pick-side .label{margin-top:var(--oa-space-200)}.pick-side > .label:first-child{margin-top:0}
ul.declinks{list-style:none;margin:0 0 var(--oa-space-200);padding:0}
ul.declinks a{display:flex;gap:.6em;align-items:baseline;padding:var(--oa-space-100) 0;min-height:var(--oa-size-target-touch);font:var(--oa-type-body-small);text-decoration:none;border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
ul.declinks a b{flex:none;font-variant-numeric:tabular-nums}
ul.declinks a:hover{text-decoration:underline}
.go-row{margin:var(--oa-space-300) 0 var(--oa-space-100)}
.go{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);padding:var(--oa-space-100) var(--oa-space-300);font:var(--oa-type-ui);font-weight:600;
  text-decoration:none;border:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);color:var(--oa-color-text-primary-on-white)}
.go:hover{text-decoration:underline}
.page-name{margin:0}
.chk{margin:var(--oa-space-200) 0 0;max-width:var(--oa-layout-measure-intro-max)}
.wait{margin:var(--oa-space-300) 0 0;padding:var(--oa-space-300);border:var(--oa-border-width-rule) solid var(--strong);max-width:var(--oa-layout-measure-intro-max)}
.wait p{margin:0}
/* decisions */
.tw{overflow-x:auto;border:var(--oa-border-width-hairline) solid var(--hair);background:var(--white)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-150) var(--oa-space-200);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary-on-white);background:var(--oa-color-tint-white-n55)}
table.ck-t th{width:40%;font-weight:600}
@media (max-width:40em){table.ck-t,table.ck-t tbody,table.ck-t tr,table.ck-t th,table.ck-t td{display:block;width:auto}.ck-t thead{display:none}
  .ck-t tr{border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);padding:var(--oa-space-100) 0}.ck-t th,.ck-t td{border:0;padding:var(--oa-space-050) var(--oa-space-200)}}
ol.decs{list-style:none;margin:var(--oa-space-500) 0 0;padding:0;display:grid;gap:var(--oa-space-400)}
.dec{background:var(--white);border:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-300);display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200)}
@media (min-width:48em){.dec{grid-template-columns:6rem minmax(0,1fr);padding:var(--oa-space-400) var(--oa-space-500) var(--oa-space-400) var(--oa-space-400)}}
.dec-b{min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-600);align-items:start}
@media (min-width:80em){.dec-b{grid-template-columns:minmax(0,1fr) minmax(17rem,24rem)}
  .dec-b .ans{margin-top:0;border-top:0;border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:0 0 0 var(--oa-space-400)}}
.dec-n{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);font-variant-numeric:tabular-nums;white-space:nowrap}
.dec-q{margin:0 0 var(--oa-space-200);max-width:30ch}
.dec .label{margin:var(--oa-space-300) 0 var(--oa-space-100);color:var(--oa-color-text-secondary-on-white)}
ol.opts{list-style:none;margin:0;padding:0;max-width:var(--oa-layout-measure-intro-max)}
ol.opts li{display:grid;grid-template-columns:2.2em minmax(0,1fr);padding:var(--oa-space-100) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
.ol{font-weight:600;font-variant-numeric:tabular-nums}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);padding:1px 6px;margin-left:.4em;white-space:nowrap}
.chip--ill{margin:0 .4em 0 0}
.rec{border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);margin-top:var(--oa-space-300);padding-top:var(--oa-space-100);max-width:var(--oa-layout-measure-intro-max)}
.rec p{margin:var(--oa-space-150) 0 0;max-width:none}.rec .label{display:block;margin:0 0 2px}
ul.touch{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:var(--oa-space-050) var(--oa-space-300)}
ul.touch a{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);padding:var(--oa-space-050) 0;font:var(--oa-type-ui)}
ul.touch span{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);font:var(--oa-type-ui);color:var(--oa-color-text-secondary-on-white)}
.ans{margin:var(--oa-space-400) 0 0;padding:var(--oa-space-200) 0 0;border:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);min-width:0}
.ans legend{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;padding:0;float:left;width:100%;margin-bottom:var(--oa-space-100)}
.rads{display:grid;gap:0;clear:both}
.rad{display:flex;gap:var(--oa-space-150);align-items:center;min-height:var(--oa-size-target-touch);cursor:pointer;max-width:var(--oa-layout-measure-intro-max)}
.rad input{width:20px;height:20px;margin:0;flex:none;accent-color:var(--oa-color-palette-charcoal)}
.nl{display:block;font:var(--oa-type-body-small);color:var(--oa-color-text-secondary-on-white);margin:var(--oa-space-200) 0 var(--oa-space-100)}
textarea{display:block;width:100%;max-width:var(--oa-layout-measure-intro-max);font:var(--oa-type-body);color:var(--oa-color-text-primary-on-white);background:var(--white);
  border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);border-radius:0;padding:var(--oa-space-150);resize:vertical}
.reply{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);margin:var(--oa-space-800) 0 0;padding:var(--oa-space-400) var(--oa-space-300)}
@media (min-width:48em){.reply{padding:var(--oa-space-500)}}
.reply h3{color:inherit;margin:0 0 var(--oa-space-200)}
.reply p{color:var(--oa-color-text-primary-on-prussian)}
.reply .label{color:var(--oa-color-text-secondary-on-prussian);display:block;margin:var(--oa-space-300) 0 var(--oa-space-100)}
.reply textarea{background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);border-color:var(--oa-color-surface-newsprint);font:500 1rem/1.55 var(--mono)}
.reply-row{display:flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-200);margin-top:var(--oa-space-200)}
.reply button{font:var(--oa-type-ui);min-height:var(--oa-size-target-touch);padding:0 var(--oa-space-300);border:0;border-radius:0;cursor:pointer;
  background:var(--oa-color-action-primary-fill-on-prussian);color:var(--oa-color-action-primary-label-on-prussian)}
.reply button:hover{background:var(--oa-color-action-primary-fill-hover-on-prussian)}
#copy-status{font:var(--oa-type-body-small);color:var(--oa-color-text-primary-on-prussian)}
/* record */
.rec-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-800)}
@media (min-width:64em){.rec-grid{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}}
ol.process{list-style:none;margin:0 0 var(--oa-space-300);padding:0;border-top:var(--oa-border-width-hairline) solid var(--hair)}
ol.process li{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-050);padding:var(--oa-space-200) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
ol.process li p{margin:0 0 var(--oa-space-100)}ol.process .label{color:var(--ink)}
@media (min-width:48em){ol.process li{grid-template-columns:10rem minmax(0,1fr);gap:var(--oa-space-300)}}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media print{.toc,.ans,.reply,.hint{display:none!important}.frame{overflow:visible;border:0}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''

JS = r'''
(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  // A frame takes keyboard focus only while it is wider than the window and so needs scrolling.
  function frames() {
    $$('.frame').forEach(function (f) {
      var over = f.scrollWidth > f.clientWidth + 1;
      if (over) f.setAttribute('tabindex', '0'); else f.removeAttribute('tabindex');
      var h = f.previousElementSibling; if (h && h.classList.contains('hint')) h.hidden = !over;
    });
  }
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(frames, 120); });
  $$('.frame img').forEach(function (i) { if (!i.complete) i.addEventListener('load', frames); });
  frames();
  // Answers: each card's marks join the reply. Saved in this browser only, keyed to this version of the decisions.
  var out = document.getElementById('reply-text');
  if (!out) return;
  var KEY = 'oa-board-6-answers:' + (document.querySelector('.board') || document.body).getAttribute('data-decisions');
  var store = {};
  try { store = JSON.parse(window.localStorage.getItem(KEY) || '{}') || {}; } catch (e) { store = {}; }
  function save() { try { window.localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }
  var cards = $$('.dec[data-dec]');
  function compose() {
    var lines = [];
    cards.forEach(function (c) {
      var id = c.getAttribute('data-dec'), s = store[id] || {};
      var note = (s.note || '').trim(), part = '';
      if (s.opt) {
        var r = c.querySelector('input[value="' + s.opt + '"]');
        part = s.opt === c.getAttribute('data-rec') ? 'as recommended (' + s.opt + ').' : '(' + s.opt + ') ' + (r ? r.getAttribute('data-short') : '') + '.';
      }
      if (note) part = part ? part + ' ' + note : note;
      if (part) lines.push(id + ': ' + part.replace(/\.\.$/, '.'));
    });
    out.value = lines.length ? lines.join('\n') : out.getAttribute('data-sample');
  }
  cards.forEach(function (c) {
    var id = c.getAttribute('data-dec'), s = store[id] || {};
    $$('input[type=radio]', c).forEach(function (r) {
      if (s.opt === r.value) r.checked = true;
      r.addEventListener('change', function () { store[id] = store[id] || {}; store[id].opt = r.value; save(); compose(); });
    });
    var t = c.querySelector('textarea[data-note]');
    if (t) { if (s.note) t.value = s.note; t.addEventListener('input', function () { store[id] = store[id] || {}; store[id].note = t.value; save(); compose(); }); }
  });
  compose();
  var btn = document.getElementById('copy-reply'), st = document.getElementById('copy-status');
  btn.addEventListener('click', function () {
    var done = function () { st.textContent = 'Copied. Paste it into our chat.'; };
    var fall = function () { out.focus(); out.select(); try { document.execCommand('copy') ? done() : (st.textContent = 'Press Ctrl or Command and C to copy the selected reply.'); } catch (e) { st.textContent = 'Press Ctrl or Command and C to copy the selected reply.'; } };
    try { navigator.clipboard.writeText(out.value).then(done, fall); } catch (e) { fall(); }
  });
})();
'''

CONTENT = {}


def build_page(C, R, facts, checks, present, tokens_css, reused):
    n_dec = len(C['decisions'])
    ask = C.get('ask') or [
        'Read the verdict, then the four sections. Each one sets its lead comparison at true size above our recommendation.',
        'Open a section’s full page to see every option at every size. A link at the top of each page brings you back here.',
        f'Answer B6-1{f" to B6-{n_dec}" if n_dec > 1 else ""} on the cards, or send the sample reply if every recommendation suits you.',
    ]
    sample = C.get('sample_reply') or (f'B6-1 to B6-{n_dec}: as recommended.' if n_dec > 1 else 'B6-1: as recommended.')
    toc = [('verdict', '', 'Verdict')] + [(k, str(i), sec_info(C, k)[1]) for i, k in enumerate(KEYS, 1)] + [('decisions', '', 'Decisions'), ('record', '', 'Studio record')]
    num = lambda n: f'<span class="n">{n}</span> ' if n else ''
    nav = ''.join(f'<li><a href="#{a}">{num(n)}{esc(t)}</a></li>' for a, n, t in toc)
    sample_band = ('<div class="sample" role="note"><p><b>Sample content.</b> This hub was built from sample files to test the builder. '
                   'The creative director’s content and the studio record replace them.</p></div>') if (C.get('sample') or R.get('sample')) else ''
    built = datetime.datetime.now(datetime.timezone.utc)
    decision_key = hashlib.sha1(json.dumps(C['decisions'], sort_keys=True).encode()).hexdigest()[:12]
    title = md(C.get('title') or 'Four explorations, for your pick', links=False)
    dec_by_sec = {}
    for i, d in enumerate(C['decisions'], 1):
        ks = {d['section']} if d.get('section') else set()
        ks |= {parse_touch(r)[0] for r in d.get('touches', [])}
        for k in ks:
            dec_by_sec.setdefault(k, []).append((i, d['question']))
    bands = ''.join(band(C, i, k, present, facts, checks, dec_by_sec) for i, k in enumerate(KEYS, 1))
    pages = 'four section pages' if len(present) == 4 else 'section pages'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{tokens_css}
{CSS}</style></head>
<body><main class="board" data-view-root="overview" data-decisions="{decision_key}">
<header class="cover">
<div class="mast">{wordmark()}<span class="label">Brand Guide, Edition 06 · Board 6</span></div>
{sample_band}
<p class="label" style="margin-top:var(--oa-space-800)">For Dustin Cathcart · {words_date(built)}</p>
<h1>{title}</h1>
<p class="intro">{md(C["deck"])}</p>
<div class="ask"><h2>What you are asked</h2><ol>{"".join(f"<li>{md(x)}</li>" for x in ask)}</ol>
<p class="caption" style="margin:0 0 var(--oa-space-050)">A reply can be this short:</p><p class="q">{esc(sample)}</p></div>
<nav class="toc" aria-label="On this board"><ol>{nav}</ol></nav>
</header>
{verdict_section(C, present)}
{bands}
{decisions_section(C, sample, facts, present)}
{record_section(R)}
<p class="foot caption">Built {words_date(built)} at {words_time(built)} UTC by <code>work/build/scripts/phase-2/board6_hub_build.py</code>, from the creative director’s content, the studio record and the {pages} as they stood then.{" These captures came from an earlier run." if reused else ""}</p>
</main>
<script>{JS}</script></body></html>'''


def main():
    global N_DEC, CONTENT, CAP_PREFIX
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--board-dir', type=pathlib.Path, default=BOARD_DIR)
    for k in ('content', 'record', 'out', 'captures', 'publish'):
        ap.add_argument(f'--{k}', type=pathlib.Path, default=None)
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--no-capture', action='store_true')
    a = ap.parse_args()
    bd = a.board_dir.resolve()
    a.content = (a.content or bd / f'{DATE}_Board-6-Content.json').resolve()
    a.record = (a.record or bd / f'{DATE}_Board-6-Studio-Record.json').resolve()
    a.captures = (a.captures or bd / 'captures').resolve()
    a.out = (a.out or OUT).resolve()
    a.publish = (a.publish or PUBLISH).resolve()
    for k in ('content', 'record'):
        need(getattr(a, k).exists(), f'{k} file not found: {getattr(a, k)}')
    if a.publish.exists():   # checked before anything is written: the publish folder is wiped on every run
        need((a.publish / 'files.json').exists() or (a.publish / 'index.html').exists() or not any(a.publish.iterdir()),
             f'{a.publish} holds files this builder did not write; choose another --publish folder')
    C = json.loads(a.content.read_text())
    R = json.loads(a.record.read_text())
    check_content(C)
    check_record(R)
    CONTENT = C
    N_DEC = len(C['decisions'])

    # the section pages as they stand now
    pages, checks, present = {}, {}, []
    for s in SECTIONS:
        k = s['key']
        entry = (C.get('sections') or {}).get(k)
        p = find_page(bd, k, entry)
        pages[k] = p
        if not p:
            warn(f'section {KEYS.index(k) + 1}, {s["short"].lower()}: no page in {bd / k} yet, so its band is a placeholder')
            continue
        need(entry and entry.get('recommendation'), f'content.sections["{k}"]: the {s["short"].lower()} page exists ({p.name}), '
             f'so the band needs its summary and recommendation')
        present.append(k)
        chk = page_check(p)
        checks[k] = chk
        if not chk:
            warn(f'the {k} page has no check result beside it ({p.stem}-Check-Results.json)')
        elif chk.get('error'):
            warn(f'the {k} page\'s check result cannot be read')
        else:
            if not chk['pass']:
                warn(f'the {k} page failed its own check ({chk["failures"]} failures)')
            if chk['stale']:
                warn(f'the {k} page changed after its own check ran; run dataviz_check.js on it again')
    jobs = []
    for k in present:
        ld = (C['sections'][k].get('lead') or {})
        jobs.append({'key': k, 'page': str(pages[k]), 'selector': ld.get('selector'), 'defaults': SEC[k]['defaults'],
                     'stem': f'{STEM}{"-".join(w.capitalize() for w in k.split("-"))}-Lead'})
    if jobs:
        facts, reused = run_capture(jobs, a.captures, a.no_capture)
    else:
        facts, reused = {'captured': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'sections': {}}, False
    for k in present:
        f = facts['sections'][k]
        need(f.get('lead'), f'no lead comparison captured for the {k} page')
        L = f['lead']
        need((a.captures / L['file']).exists(), f'the capture {L["file"]} is missing from {a.captures}')
        if L['from'] == 'default' and SEC[k]['defaults'] and L['selector'] != SEC[k]['defaults'][0]:
            warn(f'the {k} page\'s lead fell back to "{L["selector"]}"; name the element in content.sections["{k}"].lead.selector')
        if L['css_h'] > TALL:
            warn(f'the {k} lead is {px(L["css_h"])} px tall; name a smaller element so the band stays one comparison')
        if L['css_w'] > MEASURE:
            warn(f'the {k} lead is {px(L["css_w"])} px wide, wider than the hub\'s {px(MEASURE)} px column, so it scrolls even at 1,440 px')
        for e in f.get('errors', []):
            if e.startswith('page error'):
                warn(f'the {k} page threw an error while it was captured: {e}')
    # every place a decision points at must exist on its section page
    for i, d in enumerate(C['decisions']):
        for ref in d.get('touches', []):
            k, anc = parse_touch(ref)
            if k not in present:
                warn(f'content.decisions[{i}].touches: "{ref}" points at the {k} page, which does not exist yet')
            elif anc:
                need(anc in facts['sections'][k]['ids'], f'content.decisions[{i}].touches: "{ref}": no #{anc} on the {k} page. '
                     f'Ids there include {", ".join(list(facts["sections"][k]["ids"])[:20])}')
        if d.get('section') and d['section'] not in present:
            warn(f'content.decisions[{i}].section: the {d["section"]} page does not exist yet')

    tokens_css = TOKENS.read_text()
    colors = token_colors(tokens_css)

    # the builder's own checks, printed on the hub as run
    if present:
        cap_t = iso(facts['captured'])
        leads = [facts['sections'][k]['lead'] for k in present]
        BUILDER_CHECKS.append(
            f'The builder captured {num_words(len(present))} lead comparison{"s" if len(present) != 1 else ""} on {words_date(cap_t)} at {words_time(cap_t)} UTC, '
            f'each from its section page in a 1,440 px window at device scale 2, and shows each at its CSS size: '
            + '; '.join(f'{sec_info(C, k)[1].lower()}, {px(L["css_w"])} by {px(L["css_h"])} px' for k, L in zip(present, leads)) + '.'
            + (' These captures came from an earlier run.' if reused else ''))
        ok = [k for k in present if checks.get(k) and checks[k].get('pass') and not checks[k].get('stale')]
        BUILDER_CHECKS.append(f'It read each section page’s own check result: '
                              + (f'all {num_words(len(present))} passed, each run on the page as it stands.' if len(ok) == len(present) > 1 else
                                 'it passed, run on the page as it stands.' if len(ok) == len(present) else
                                 f'{num_words(len(ok))} of {num_words(len(present))} passed on the page as it stands.'))
    missing = [SEC[k]['short'].lower() for k in KEYS if k not in present]
    if missing:
        BUILDER_CHECKS.append(f'It found no page yet for {join_words(missing)}, so {"that band holds" if len(missing) == 1 else "those bands hold"} a placeholder.')
    if any(d.get('touches') for d in C['decisions']):
        BUILDER_CHECKS.append('Each place a decision points at exists on its section page.')

    def render(cap_prefix, hrefs):
        global CAP_PREFIX
        CAP_PREFIX = cap_prefix
        HREF.clear()
        HREF.update(hrefs)
        return build_page(C, R, facts, checks, present, tokens_css, reused)

    repo_hrefs = {k: os.path.relpath(pages[k], a.out.parent).replace(os.sep, '/') for k in present}
    pub_hrefs = {k: f'{k}.html' for k in present}
    rel = os.path.relpath(a.captures, a.out.parent).replace(os.sep, '/') + '/'
    page = render(rel, repo_hrefs)
    # the hub's own words: no em dash anywhere, the word check on everything it prints, and no red of its own
    text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)))
    need('\u2014' not in text, 'em dash on the hub')
    if '\u2013' in text:
        warn('an en dash on the hub')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text, flags=re.I)})
    if flagged:
        warn(f'the hub prints words the writing rules flag: {", ".join(flagged)}')
    own = CSS + re.sub(r'<style>.*?</style>|<span class="wm-wrap" data-red="signature">.*?</svg>\s*</span>', '', page, flags=re.S)
    need(not re.search(r'pillar-red|#E63946|data-red="working"', own, flags=re.I), 'the hub\'s own styles or markup carry a red')
    BUILDER_CHECKS.append('The hub prints no em dash' + (f', and the word check flags {", ".join(flagged)}.' if flagged else ' and none of the words the writing rules flag.'))
    BUILDER_CHECKS.append('Its own styles use no red. The one red it draws is the wordmark’s ampersand in the masthead, marked as the signature; '
                          'every other red sits inside a capture of a section page.')
    BUILDER_CHECKS.append('Each section page is published as a copy with a link back to this hub added at its top. The pages in the repository are left as they are.')
    page = render(rel, repo_hrefs)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)

    # the publish folder: the hub without its document skeleton, the section pages, their files and the captures
    if a.publish.exists():
        shutil.rmtree(a.publish)
    a.publish.mkdir(parents=True)
    pub = render('captures/', pub_hrefs)
    head, body = re.split(r'</head>\s*<body>', pub, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace(f'<title>{TITLE}</title>\n', '')
    body = re.sub(r'</body>\s*</html>\s*$', '', body)
    setup = '<script>document.documentElement.lang="en";</script>'   # the publish skeleton's html element carries no lang
    (a.publish / 'index.html').write_text(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + setup + body)
    files = {}
    (a.publish / 'captures').mkdir()
    for k in present:
        L = facts['sections'][k]['lead']
        shutil.copy2(a.captures / L['file'], a.publish / 'captures' / L['file'])
        files[f'captures/{L["file"]}'] = str(a.publish / 'captures' / L['file'])
    for k in present:
        out, refs = publish_section(k, pages[k], a.publish, pages, colors)
        files[f'{k}.html'] = str(out)
        for served in refs:
            files[served] = str(a.publish / served)
    (a.publish / 'files.json').write_text(json.dumps(files, indent=1))
    size = sum(os.path.getsize(p) for p in files.values()) + os.path.getsize(a.publish / 'index.html')
    big = [s for s, p in files.items() if os.path.getsize(p) > 15_000_000]
    need(not big, f'files over the 15 MB publish limit: {", ".join(big)}')
    print(f'wrote {a.out} ({len(page) / 1e3:.0f} kB) with {len(present)} captures in {a.captures}')
    print(f'wrote {a.publish / "index.html"} and {len(files)} files ({size / 1e6:.1f} MB with the page); publish map in {a.publish / "files.json"}')
    if WARN:
        print(f'{len(WARN)} warnings')
        if a.strict:
            sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
