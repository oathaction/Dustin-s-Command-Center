"""Build stage board A (November 6, 2026): chapters 01 to 08 and the wordmark proofs, for Dustin's review and answers.

Usage:
    python3 -I work/build/scripts/phase-2/stage_a_board_build.py [--strict] [--no-capture]
        [--content PATH] [--record PATH] [--page PATH] [--out PATH] [--captures DIR] [--publish DIR]

Reads, from work/boards/phase-2/stage-a/board-a/:
    20261106_Stage-A-Board-Content.json        the creative director's content (verdict, scores, notes, decisions)
    20261106_Stage-A-Board-Studio-Record.json  the main session's record (what was asked, process, checks, change log,
                                               and the chapters page's published address or its placeholder)
Their schema is in work/handoffs/phase-2/20261106_Stage-A-Board-Builder-Notes.md.

On every run it reads the chapters page, work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html, as it is then:
stage_a_board_capture.js captures each chosen view at 1440 and 390 px and each comparison plate of the wordmark
proofs, all at device scale 2, and reads the page's titles, instruction lines, rules, proof notes and letter spacing.
Writes:
    work/boards/20261106_Stage-A-Foundations-Board.html                 the board (images by relative path)
    work/boards/phase-2/stage-a/board-a/captures/                       the captures and the facts read from the page
    <scratchpad>/publish-board-a/20261106_Stage-A-Foundations-Board.html the publish copy, with captures/ beside it
    <scratchpad>/publish-board-a/files.json                             published path to source file, for the publish call

Captures are shown at their CSS size, never scaled. Colors and type come from work/build/tokens/tokens.css, inlined.
The page carries no red of its own; red appears only inside captures of the guide.
--no-capture reuses the last captures (for layout work only; the board then says so in its builder checks).
--strict exits 1 on any warning (flagged words, an en dash, a decision that touches no rule, reused captures).
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
DATE = '20261106'
BOARD_DIR = ROOT / 'work/boards/phase-2/stage-a/board-a'
DEF = {
    'content': BOARD_DIR / f'{DATE}_Stage-A-Board-Content.json',
    'record': BOARD_DIR / f'{DATE}_Stage-A-Board-Studio-Record.json',
    'page': ROOT / f'work/boards/phase-2/stage-a/{DATE}_Stage-A-Chapters.html',
    'out': ROOT / f'work/boards/{DATE}_Stage-A-Foundations-Board.html',
    'captures': BOARD_DIR / 'captures',
    'publish': pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad/publish-board-a'),
}
CAPTURE_JS = ROOT / 'work/build/scripts/phase-2/stage_a_board_capture.js'
TOKENS = ROOT / 'work/build/tokens/tokens.css'
AMP = ROOT / 'work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg'
TITLE = 'Stage A Foundations Board'
STEM = f'{DATE}_Board-A-'
RUBRIC = ['Craft', 'Clarity', 'Brand fidelity', 'Usefulness', 'Evidence honesty', 'Accessibility']
RUBRIC_SHORT = {'Brand fidelity': 'Brand', 'Evidence honesty': 'Evidence'}
CHAPTERS = ['01', '02', '03', '04', '05', '06', '07', '08']
TAGLINE = 'A country that answers to its people.'
LOCKED = {
    'tagline': (TAGLINE, ['answers to its people']),
    'mission': ('Help people understand and improve the rules that shape their lives.', ['rules that shape their lives']),
    'promise': ('We explain how a decision is made and give you a practical way to take part.', ['how a decision is made and give']),
    'commitment': ('Clarity is our duty. Action is our promise.', ['Clarity is our duty', 'Action is our promise']),
}
# DR-95: the old display tracking, and the new values the decision set (the tokens should carry them)
OLD_TRACKING = {'title': -4.5, 'section': -4.0, 'h3': -3.0}
NEW_TRACKING = {'title': -3.0, 'section': -2.5, 'h3': -1.0}
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless']
PROCESS_STAGES = [('makers', 'maker'), ('red team', 'red team'), ('fix pass', 'fix pass'), ('creative director', 'creative director')]

WARN = []


class BoardError(Exception):
    pass


def warn(msg):
    WARN.append(msg)
    print('warning', msg)


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


class Linker:
    """Links to the live chapters page, and the words each anchor carries."""

    def __init__(self, base, anchors):
        self.base = base
        self.anchors = anchors

    def href(self, anchor):
        return f'{self.base}#{anchor}'

    def resolve(self, ref):
        """'05.3', 'Rule 05.3', 'rule-05-3', '05', 'color', 'proofs-avatar' to an anchor on the page, or None."""
        r = str(ref).strip()
        m = re.fullmatch(r'(?:Rule\s+)?(\d\d)\.(\d+)', r, flags=re.I)
        if m:
            r = f'rule-{m.group(1)}-{m.group(2)}'
        elif re.fullmatch(r'\d\d', r):
            r = next((a for a, v in self.anchors.items() if v['kind'] == 'chapter' and v['chapter'] == r), r)
        return r if r in self.anchors else None

    def label(self, anchor):
        return self.anchors[anchor]['label']


LINK = None   # set in main()
N_DEC = 0     # decisions on the board; A1 to A{N_DEC} in body text link to their cards


def md(s, links=True):
    """Escaped text with `code`, **bold**, and each Rule NN.N found on the page linked to its live anchor."""
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f'\x00{len(codes) - 1}\x00'
    t = re.sub(r'`([^`]+)`', keep, str(s))
    t = html.escape(copy(t), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    if links and LINK:
        def rl(m):
            a = f'rule-{m.group(1)}-{m.group(2)}'
            return f'<a href="{attr(LINK.href(a))}">{m.group(0)}</a>' if a in LINK.anchors else m.group(0)
        t = re.sub(r'(?<![\w/#.-])A([1-9]\d?)\b', lambda m: f'<a href="#a{m.group(1)}">{m.group(0)}</a>' if int(m.group(1)) <= N_DEC else m.group(0), t)
        t = re.sub(r'\bRule (\d\d)\.(\d+)\b', rl, t)
    t = t.replace('{{illus}}', '<span class="chip chip--ill">Illustrative</span>')
    return re.sub(r'\x00(\d+)\x00', lambda m: f'<code>{html.escape(codes[int(m.group(1))])}</code>', t)


def words_date(d):
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def words_time(d):
    h = d.hour % 12 or 12
    return f'{h}:{d.minute:02d} {"a.m." if d.hour < 12 else "p.m."}'


def num_words(n):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][n] if 0 <= n < 10 else f'{n:,}'


# ------------------------------------------------------------------------------------------------ inputs
def need(cond, msg):
    if not cond:
        raise BoardError(msg)


def strings(obj, path=''):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from strings(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from strings(v, f'{path}[{i}]')


def lint(obj, name, skip=('url', 'placeholder', 'command')):
    """Chapter 02's marks and locked lines on every string an input holds. Em dashes fail; flagged words warn."""
    for path, s in strings(obj):
        if path.split('.')[-1] in skip or re.search(r'changelog', path):
            continue
        need('—' not in s, f'{name} {path}: an em dash (W21). Join the parts with a comma and a word, or end the sentence.')
        if '–' in s or ' -- ' in s:
            warn(f'{name} {path}: an en dash or double hyphen; write "to" for a range')
        for w in FLAGGED:
            if re.search(rf'\b{w}\b', s, flags=re.I):
                warn(f'{name} {path}: "{w}" is on the writing rules\' list (W17, W18, W20)')
        for key, (line, frags) in LOCKED.items():
            for f in frags:
                if f.lower() in s.lower() and line not in copy(s).replace('’', "'") and line not in s:
                    raise BoardError(f'{name} {path}: quotes the {key} inexactly. It reads "{line}" (H01).')


def check_content(C):
    need(isinstance(C, dict), 'the content file must hold one JSON object')
    need(isinstance(C.get('deck'), str) and C['deck'].strip(), 'content.deck: one or two sentences under the title')
    v = C.get('verdict')
    need(isinstance(v, dict) and isinstance(v.get('headline'), str) and v['headline'].strip(), 'content.verdict.headline: the verdict in one sentence')
    sc = C.get('scores')
    need(isinstance(sc, list) and len(sc) == len(RUBRIC), f'content.scores: six entries, one per criterion, in this order: {", ".join(RUBRIC)}')
    for i, (s, crit) in enumerate(zip(sc, RUBRIC)):
        need(isinstance(s, dict) and s.get('criterion') == crit, f'content.scores[{i}].criterion must be "{crit}"')
        need(isinstance(s.get('score'), int) and 1 <= s['score'] <= 5, f'content.scores[{i}].score: a whole number from 1 to 5')
        need(isinstance(s.get('line'), str) and s['line'].strip(), f'content.scores[{i}].line: the reason, one line')
    ch = C.get('chapters')
    need(isinstance(ch, dict) and sorted(ch) == CHAPTERS, 'content.chapters: one entry for each of "01" to "08"')
    for n in CHAPTERS:
        c = ch[n]
        need(isinstance(c, dict) and isinstance(c.get('note'), str) and c['note'].strip(), f'content.chapters["{n}"].note: the creative director\'s note')
        vw = c.get('views')
        need(isinstance(vw, list) and 2 <= len(vw) <= 3, f'content.chapters["{n}"].views: two or three views, "opening" or a rule ID such as "{n}.1"')
        if 'scores' in c:
            need(isinstance(c['scores'], list) and len(c['scores']) == 6 and all(isinstance(x, int) and 1 <= x <= 5 for x in c['scores']),
                 f'content.chapters["{n}"].scores: six whole numbers from 1 to 5, in rubric order')
    for k in ('needs_work', 'risks'):
        need(isinstance(C.get(k), list), f'content.{k}: a list (it may be empty)')
        for i, x in enumerate(C[k]):
            need(isinstance(x, str) or (isinstance(x, dict) and isinstance(x.get('text'), str)), f'content.{k}[{i}]: a string, or {{"text": ..., "where": ...}}')
    d = C.get('decisions')
    need(isinstance(d, list) and d, 'content.decisions: at least one decision')
    for i, x in enumerate(d):
        tag = f'content.decisions[{i}]'
        need(isinstance(x, dict), f'{tag}: an object')
        if 'id' in x:
            need(x['id'] == f'A{i + 1}', f'{tag}.id: decisions are numbered in order, so this one is A{i + 1}')
        need(isinstance(x.get('question'), str) and x['question'].strip(), f'{tag}.question: the question for Dustin')
        o = x.get('options')
        need(isinstance(o, list) and 2 <= len(o) <= 8, f'{tag}.options: two to eight options')
        for j, op in enumerate(o):
            need(isinstance(op, str) or (isinstance(op, dict) and isinstance(op.get('text'), str)), f'{tag}.options[{j}]: a string, or {{"text": ..., "short": ...}}')
        r = x.get('recommended')
        need(r is not None, f'{tag}.recommended: the recommended option, as its letter ("b") or its number (2)')
        idx = option_index(r, len(o))
        need(idx is not None, f'{tag}.recommended: "{r}" names no option; use a letter from a to {chr(96 + len(o))}')
        need(isinstance(x.get('why'), str) and x['why'].strip(), f'{tag}.why: the reason for the recommendation')
        need(isinstance(x.get('touches', []), list), f'{tag}.touches: a list of rule IDs or anchors')
        if not x.get('touches'):
            warn(f'{tag} names no rule it touches')
    t = C.get('tracking', {})
    need(isinstance(t, dict), 'content.tracking: an object')
    lint(C, 'content')


def option_index(r, n):
    if isinstance(r, int) and 1 <= r <= n:
        return r - 1
    if isinstance(r, str) and re.fullmatch(r'[a-h]', r.strip().lower()) and ord(r.strip().lower()) - 97 < n:
        return ord(r.strip().lower()) - 97
    return None


def check_record(R):
    need(isinstance(R, dict), 'the studio record must hold one JSON object')
    cp = R.get('chapters_page')
    need(isinstance(cp, dict) and ('url' in cp or 'placeholder' in cp), 'record.chapters_page: {"url": "", "placeholder": "..."}')
    need((cp.get('url') or '').strip() or (cp.get('placeholder') or '').strip(), 'record.chapters_page: set the published url, or a placeholder until it exists')
    need(isinstance(R.get('asked'), list) and R['asked'], 'record.asked: what was asked, at least one line')
    pr = R.get('process')
    need(isinstance(pr, list) and all(isinstance(p, dict) and p.get('stage') and p.get('text') for p in pr), 'record.process: a list of {"stage": ..., "text": ...}')
    names = ' | '.join(p['stage'].lower() for p in pr)
    for label, key in PROCESS_STAGES:
        need(key in names, f'record.process: no stage for the {label}; the record names makers, red team, fix pass and creative director')
    for i, r in enumerate(R.get('red_team', [])):
        need(isinstance(r, dict) and r.get('lens'), f'record.red_team[{i}]: {{"lens": ..., "score": ..., "must_fix": ..., "should_fix": ...}}')
    ck = R.get('checks')
    need(isinstance(ck, list) and ck and all(isinstance(c, dict) and c.get('name') and c.get('result') for c in ck), 'record.checks: a list of {"name": ..., "result": ...}')
    need(isinstance(R.get('not_tested'), list) and R['not_tested'], 'record.not_tested: at least one line')
    cl = R.get('changelog')
    need(isinstance(cl, dict) and isinstance(cl.get('created'), list) and isinstance(cl.get('modified'), list), 'record.changelog: {"created": [...], "modified": [...]}')
    lint(R, 'record')


# ------------------------------------------------------------------------------------------------ captures
def view_anchor(chapter, ref, facts_by_num):
    """A view as the content names it, to (anchor, label kind)."""
    label = None
    if isinstance(ref, dict):
        label = ref.get('label')
        ref = ref.get('anchor', '')
    r = str(ref).strip()
    if r.lower() == 'opening':
        return facts_by_num[chapter]['anchor'] if chapter in facts_by_num else None, 'opening', label
    m = re.fullmatch(r'(?:Rule\s+)?(\d\d)\.(\d+)', r, flags=re.I)
    if m:
        return f'rule-{m.group(1)}-{m.group(2)}', 'rule', label
    return r, 'rule' if r.startswith('rule-') else 'other', label


def slug(anchor):
    return '-'.join(w[:1].upper() + w[1:] for w in anchor.split('-'))


def run_capture(page, cap_dir, views, no_capture):
    facts_path = cap_dir / f'{DATE}_Board-A-Capture-Facts.json'
    if no_capture:
        need(facts_path.exists(), f'--no-capture: no earlier captures in {cap_dir}')
        warn('captures reused from an earlier run (--no-capture)')
        return json.loads(facts_path.read_text()), True
    cap_dir.mkdir(parents=True, exist_ok=True)
    for old in cap_dir.glob(f'{STEM}*.jpg'):
        old.unlink()
    job = {'page': str(page), 'out': str(cap_dir), 'facts': str(facts_path), 'quality': 80, 'widths': [1440, 390],
           'proofs': True, 'proof_prefix': f'{STEM}Proof-', 'views': views}
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(job, f)
        jp = f.name
    try:
        r = subprocess.run(['node', str(CAPTURE_JS), jp], cwd=ROOT, capture_output=True, text=True, timeout=1800)
    finally:
        os.unlink(jp)
    print(r.stdout.strip())
    if not facts_path.exists():
        raise BoardError(f'the capture script wrote no facts: {r.stderr.strip()[-600:]}')
    facts = json.loads(facts_path.read_text())
    if r.returncode != 0:
        raise BoardError('the capture script failed:\n  ' + '\n  '.join(facts.get('errors') or [r.stderr.strip()[-600:]]))
    return facts, False


# ------------------------------------------------------------------------------------------------ page parts
def hinge():
    svg = AMP.read_text()
    svg = re.sub(r'<title>.*?</title>', '', svg).replace('<svg ', '<svg class="hamp" width="21" height="24" aria-hidden="true" focusable="false" ', 1)
    return f'<div class="hinge" aria-hidden="true">{svg}</div>'


def img_tag(prefix, file, w, h, alt, cls=''):
    return (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{attr(prefix + file)}" width="{w}" height="{h}" '
            f'alt="{attr(alt)}" loading="lazy" decoding="async">')


def frame(inner, name, wide=False):
    """A frame that holds a capture at true size and scrolls sideways when the window is narrower."""
    return (f'<div class="frame{" frame--phone" if wide else ""}" role="region" tabindex="0" aria-label="{attr(name)}">{inner}</div>'
            f'<p class="hint caption" hidden>Wider than this window. Scroll inside the frame to see all of it.</p>')


def pips(score):
    cells = ''.join(f'<i class="{"on" if k < score else ""}"></i>' + ('<b></b>' if k == 2 else '') for k in range(5))
    return f'<span class="pips" aria-hidden="true">{cells}</span>'


def section(num, sid, title, body, extra_cls=''):
    return (f'<section class="sec{extra_cls}" id="{sid}" aria-labelledby="{sid}-h"><h2 class="sec-h" id="{sid}-h">'
            f'<span class="n">{num}</span> {title}</h2>{body}</section>')


def note_block(text, who='Creative director'):
    paras = text if isinstance(text, list) else [text]
    return (f'<figure class="note"><blockquote>{"".join(f"<p>{md(p)}</p>" for p in paras)}</blockquote>'
            f'<figcaption class="caption">{esc(who)}</figcaption></figure>')


def verdict_section(C):
    v = C['verdict']
    sc = C['scores']
    at = sum(1 for s in sc if s['score'] >= 4)
    ship = ('It scores 4 or above on all six criteria, the line the guide must reach to ship.' if at == 6 else
            f'It scores 4 or above on {num_words(at)} of the six criteria. The guide ships at 4 on every one.')
    rows = ''.join(
        f'<li><span class="sc-k">{esc(s["criterion"])}</span><span class="sc-v"><span class="sc-n">{s["score"]}</span>'
        f'<span class="caption">of 5</span>{pips(s["score"])}</span><span class="sc-line">{md(s["line"])}</span></li>' for s in sc)
    text = ''.join(f'<p>{md(p)}</p>' for p in (v.get('text') if isinstance(v.get('text'), list) else [v['text']] if v.get('text') else []))
    table = ''
    if any('scores' in C['chapters'][n] for n in CHAPTERS):
        head = ''.join(f'<th scope="col">{esc(RUBRIC_SHORT.get(r, r))}</th>' for r in RUBRIC)
        body = ''
        for n in CHAPTERS:
            s = C['chapters'][n].get('scores')
            cells = ''.join(f'<td class="num{" low" if x < 4 else ""}"><span>{x}</span></td>' for x in s) if s else '<td colspan="6" class="caption">Not scored</td>'
            body += f'<tr><th scope="row"><a href="#ch-{n}">{n} {esc(FACTS_BY_NUM[n]["title"])}</a></th>{cells}</tr>'
        table = (f'<h3 class="sub">By chapter</h3><div class="tw" role="region" tabindex="0" aria-label="Scores by chapter"><table class="scores-t">'
                 f'<caption class="caption">The creative director’s scores for each chapter, 1 to 5. A boxed score sits under the ship line of 4.</caption>'
                 f'<thead><tr><th scope="col">Chapter</th>{head}</tr></thead><tbody>{body}</tbody></table></div>')
    body = (f'<p class="v-head">{md(v["headline"])}</p>{text}<p class="ship">{esc(ship)}</p>'
            f'<h3 class="sub">The six criteria</h3><p class="caption legend">The creative director scores each criterion from 1 to 5 on the brief’s rubric. '
            f'In each row of squares, the upright rule after the third square marks the ship line.</p><ol class="scores">{rows}</ol>{table}')
    return section('01', 'verdict', 'Verdict', body)


def view_figure(fv, label_kind, label, anchor, chapter):
    w, h = fv['css_w'], fv['css_h']
    if label_kind == 'opening':
        k, t = 'Chapter opening', label or f'{chapter} {FACTS_BY_NUM[chapter]["title"]}'
    elif LINK.anchors.get(anchor, {}).get('kind') == 'rule':
        rid = anchor[5:].replace('-', '.')
        k, t = f'Rule {rid}', label or next((r['title'] for r in FACTS_BY_NUM[chapter]['rules'] if r['anchor'] == anchor), '')
    else:
        k, t = 'View', label or LINK.label(anchor)
    where = 'the chapter column under the masthead' if fv['width'] >= 1024 else 'the phone screen under the masthead'
    name = f'Chapter {chapter} {FACTS_BY_NUM[chapter]["title"]}, {k.lower() if k == "Chapter opening" else k} at {fv["width"]} px, true size'
    alt = (f'Capture of chapter {chapter}, {FACTS_BY_NUM[chapter]["title"]}, at a {fv["width"]} px window: {where}, '
           f'at {"the chapter opening" if label_kind == "opening" else k + ", " + t}. The same place is live in the chapters page.')
    phone = fv['width'] < 1024
    return (f'<figure class="view{" view--phone" if phone else ""}"><figcaption class="vcap"><span class="vk">{esc(k)}</span>'
            f'<a class="vt" href="{attr(LINK.href(anchor))}">{esc(t)}</a><span class="vs caption">{w:,} by {h:,} px</span></figcaption>'
            f'{frame(img_tag(PREFIX, fv["file"], w, h, alt), name, wide=phone)}</figure>')


def chapters_section(C, facts, link_note):
    views = {(v['key'], v['width']): v for v in facts['views']}
    nav = ''.join(f'<li><a href="#ch-{n}"><span class="n">{n}</span> {esc(FACTS_BY_NUM[n]["title"])}</a></li>' for n in CHAPTERS)
    bands = []
    for n in CHAPTERS:
        c, f = C['chapters'][n], FACTS_BY_NUM[n]
        wide, phone = [], []
        for ref in c['views']:
            a, kind, label = view_anchor(n, ref, FACTS_BY_NUM)
            key = f'{n}-{"opening" if kind == "opening" else a}'
            for wdt, bucket in ((1440, wide), (390, phone)):
                fv = views.get((key, wdt))
                need(fv, f'no capture for chapter {n} view {ref!r} at {wdt} px')
                bucket.append(view_figure(fv, kind, label, a, n))
        scores = ''
        if c.get('scores'):
            scores = ('<p class="ch-scores caption">' + ' · '.join(f'{esc(RUBRIC_SHORT.get(r, r))} {x}' for r, x in zip(RUBRIC, c['scores']))
                      + '</p>')
        nr = len(f['rules'])
        bands.append(f'''<article class="chap" id="ch-{n}" aria-labelledby="ch-{n}-h">
<div class="chap-head"><h3 class="chap-h" id="ch-{n}-h"><span class="n">{n}</span> {esc(f["title"])}</h3>
<p class="chap-meta caption">{num_words(nr).capitalize() if nr < 10 else nr} rules · <a href="{attr(LINK.href(f["anchor"]))}">Open chapter {n} in the chapters page</a></p>
<p class="instr">{esc(f["instruction"])}</p>{note_block(c["note"])}{scores}</div>
<div class="views"><p class="label vw-h">At 1,440 px</p>{"".join(wide)}
<p class="label vw-h">At 390 px</p><div class="phones">{"".join(phone)}</div></div></article>''')
    built = datetime.datetime.fromisoformat(facts['page_mtime'].replace('Z', '+00:00'))
    intro = (f'<p class="intro">Each chapter gives its instruction line, a note from the creative director and two or three key views. '
             f'Every view is a capture of the chapters page as it was built on {words_date(built)} at {words_time(built)} UTC, shown at true size. '
             f'A capture made at 1,440 px holds the chapter column under the masthead and leaves out the rail, while a 390 px capture holds the whole phone screen below it. '
             f'Each view’s title opens the same place in the live chapters page.</p>{link_note}')
    return section('02', 'chapters', 'Chapters', f'{intro}<nav class="chnav" aria-label="Chapters on this board"><ol>{nav}</ol></nav>{"".join(bands)}')


def clamp_px(tokens_css, style):
    m = re.search(rf'--oa-type-{style}-font-size:\s*clamp\(([\d.]+)rem,[^,]+,\s*([\d.]+)rem\)', tokens_css)
    return (round(float(m.group(1)) * 16), round(float(m.group(2)) * 16)) if m else None


def token_tracking(tokens_css, style):
    m = re.search(rf'--oa-type-{style}-letter-spacing:\s*(-?[\d.]+)em', tokens_css)
    return round(float(m.group(1)) * 100, 2) if m else None


def pct(x):
    s = f'{x:.1f}'.rstrip('0').rstrip('.') if x % 1 else f'{x:.0f}'
    return s.replace('-', '−') + ' percent'


def tracking_section(C, facts, tokens_css):
    t = C.get('tracking', {})
    ch_ref = str(t.get('chapter', '04'))
    ch_anchor = LINK.resolve(ch_ref)
    need(ch_anchor and LINK.anchors[ch_anchor]['kind'] == 'chapter', f'content.tracking.chapter: "{ch_ref}" names no chapter on the page')
    num = LINK.anchors[ch_anchor]['chapter']
    rule_anchor = LINK.resolve(t.get('rule', '05.3'))
    need(rule_anchor and LINK.anchors[rule_anchor]['kind'] == 'rule', f'content.tracking.rule: "{t.get("rule")}" names no rule on the page')
    rnum = LINK.anchors[rule_anchor]['chapter']
    rid = rule_anchor[5:].replace('-', '.')
    rtitle = next(r['title'] for r in FACTS_BY_NUM[rnum]['rules'] if r['anchor'] == rule_anchor)
    specs = [
        ('title', 'The tagline', 'Title style', f'<span>{html.escape(TAGLINE)}</span>', 'top' if 'top' in LINK.anchors else None),
        ('section', f'Chapter title, chapter {num}', 'Section style',
         f'<span class="n">{num}</span> <span>{esc(FACTS_BY_NUM[num]["title"])}</span>', ch_anchor),
        ('h3', f'Rule title, Rule {rid}', 'H3 style', f'<span>{esc(rtitle)}</span>', rule_anchor),
    ]
    blocks = []
    for style, what, sname, words, anchor in specs:
        tok = token_tracking(tokens_css, style)
        if tok != NEW_TRACKING[style]:
            warn(f'tokens.css sets the {style} style at {tok} percent, where the approved value is {NEW_TRACKING[style]}')
        rng = clamp_px(tokens_css, style)
        size = f'Inter Tight 800, {rng[0]} to {rng[1]} px as the window widens' if rng else 'Inter Tight 800'
        link = f' · <a href="{attr(LINK.href(anchor))}">See it in the chapters page</a>' if anchor else ''
        blocks.append(f'''<div class="trk trk--{style}"><p class="trk-h"><span class="label">{esc(what)}</span>
<span class="caption">{esc(sname)}, {esc(size)}{link}</span></p><div class="trk-pair">
<p class="trk-k label">Before · {esc(pct(OLD_TRACKING[style]))}</p>
<p class="trk-line trk-{style}" style="letter-spacing:{OLD_TRACKING[style] / 100:.3f}em">{words}</p>
{hinge()}
<p class="trk-k label">Now · {esc(pct(tok if tok is not None else NEW_TRACKING[style]))}</p>
<p class="trk-line trk-{style}">{words}</p></div></div>''')
    m = facts.get('tracking') or {}
    meas = ''
    if all(m.get(k) for k in ('title', 'section', 'h3')):
        same = all(abs(m[k]['percent'] - NEW_TRACKING[k]) < 0.06 for k in ('title', 'section', 'h3'))
        meas = (f'<p class="caption">Measured on the chapters page at {m.get("width", 1440):,} px: the tagline renders at {esc(pct(m["title"]["percent"]))}, '
                f'chapter titles at {esc(pct(m["section"]["percent"]))} and rule titles at {esc(pct(m["h3"]["percent"]))}'
                f'{", the values you approved." if same else ". These differ from the values you approved, so the chapters page needs a rebuild."}</p>')
        if not same:
            warn('the chapters page renders display tracking that differs from the approved values')
    note = note_block(t['note']) if t.get('note') else ''
    intro = ('<p class="intro">You approved looser letter spacing for display type on November 6. At the old values, the letters of the heaviest lines touched. '
             'Each pair below sets the same words in the same face and size twice, at the old spacing and then at the new one the tokens now carry. '
             'The text is live, so it takes the size the guide gives it at this window width.</p>')
    return section('03', 'tracking', 'Letter spacing', f'{intro}{note}<div class="trks">{"".join(blocks)}</div>{meas}')


def proofs_section(C, facts):
    P = facts.get('proofs')
    need(P and P.get('groups'), 'the chapters page has no wordmark proofs appendix')
    pc = C.get('proofs', {}) or {}
    groups = []
    for g in P['groups']:
        need(g.get('file'), f'no capture for the proof {g["anchor"]}')
        notes = ''.join(f'<p>{md(x)}</p>' for x in g['notes'])
        cd = pc.get('notes', {}).get(g['anchor']) if isinstance(pc.get('notes'), dict) else None
        size = f'<span class="caption">{esc(g["size"])}</span>' if g.get('size') else f'<span class="caption">True size, {g["css_w"]:,} px wide</span>'
        alt = g['alt'] or f'{g["title"]}, both wordmark widths at true size.'
        groups.append(f'''<div class="proof" id="pf-{attr(g["anchor"])}"><h3 class="proof-h">{esc(g["title"])}</h3>{notes}{note_block(cd) if cd else ""}
<figure class="pfig"><figcaption class="pcap"><span class="label">{esc(g["plate_label"] or "Both widths")}</span>{size}
<a href="{attr(LINK.href(g["anchor"]))}">Open this proof in the chapters page</a></figcaption>
{frame(img_tag(PREFIX, g["file"], g["css_w"], g["css_h"], alt), f'{g["title"]}, both widths at true size')}
<p class="caption pnote">{md(g["caption"])}</p></figure></div>''')
    intro = ''.join(f'<p>{md(x)}</p>' for x in P['intro'])
    note = note_block(pc['note']) if pc.get('note') else ''
    body = (f'<p class="intro">{esc(P["instruction"])}</p><div class="from"><p class="label">From the chapters page</p>{intro}</div>{note}'
            f'<p class="caption">Each plate is the appendix’s own specimen, captured at true size. A plate wider than this window scrolls inside its frame.</p>'
            f'{"".join(groups)}')
    return section('04', 'proofs', 'Wordmark proofs', body)


def where_html(x):
    if isinstance(x, str):
        return '', md(x)
    w = x.get('where')
    tag = ''
    if w:
        a = LINK.resolve(w)
        if a:
            info = LINK.anchors[a]
            short = f'Rule {a[5:].replace("-", ".")}' if info['kind'] == 'rule' else info['label']
            tag = f'<a class="where" href="{attr(LINK.href(a))}" title="{attr(copy(info["label"]))}">{esc(short)}</a>'
        else:
            if re.fullmatch(r'(?:Rule\s+)?\d\d(?:\.\d+)?|rule-[\w-]+|proofs-[\w-]+', str(w).strip(), flags=re.I):
                warn(f'"where": "{w}" looks like an anchor but is not on the chapters page; it prints as plain text')
            tag = f'<span class="where">{esc(w)}</span>'
    return tag, md(x['text'])


def todo_section(C):
    def lst(items, empty):
        if not items:
            return f'<p>{esc(empty)}</p>'
        out = ''
        for x in items:
            tag, text = where_html(x)
            out += f'<li>{tag}<span>{text}</span></li>'
        return f'<ul class="todo">{out}</ul>'
    body = (f'<div class="cols"><div><h3 class="sub">What still needs work</h3>{lst(C["needs_work"], "The creative director lists nothing still to do.")}</div>'
            f'<div><h3 class="sub">Risks</h3>{lst(C["risks"], "The creative director names no risk.")}</div></div>')
    return section('05', 'todo', 'Still to do', body)


def decisions_section(C, sample):
    decs = C['decisions']
    n = len(decs)
    cards = []
    for i, d in enumerate(decs):
        did = f'A{i + 1}'
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
        touches = []
        for ref in d.get('touches', []):
            a = LINK.resolve(ref)
            need(a, f'content.decisions[{i}].touches: "{ref}" is not an anchor on the chapters page')
            touches.append(f'<li><a href="{attr(LINK.href(a))}">{esc(LINK.label(a))}</a></li>')
        ctx = ''.join(f'<p>{md(p)}</p>' for p in (d['context'] if isinstance(d.get('context'), list) else [d['context']] if d.get('context') else []))
        rop = d['options'][rec]
        recline = md(d['recommendation']) if d.get('recommendation') else f'({chr(97 + rec)}) ' + md(rop if isinstance(rop, str) else rop['text'])
        src = f'<p class="caption">{md(d["source"])}</p>' if d.get('source') else ''
        cards.append(f'''<li class="dec" id="{did.lower()}" data-dec="{did}" data-rec="{chr(97 + rec)}">
<div class="dec-n" aria-hidden="true">{did}</div><div class="dec-b">
<div class="dec-main"><h3 class="dec-q"><span class="vh">{did}. </span>{md(d["question"], links=False)}</h3>{ctx}
<p class="label">Options</p><ol class="opts">{opts}</ol>
<div class="rec"><p><span class="label">We recommend</span> {recline}</p><p><span class="label">Why</span> {md(d["why"])}</p></div>
{f'<p class="label">Rules it touches</p><ul class="touch">{"".join(touches)}</ul>' if touches else ''}{src}</div>
<fieldset class="ans"><legend>Your answer to {did}</legend><div class="rads">{radios}</div>
<label class="nl" for="note-{did}">A note, or an answer of your own</label><textarea id="note-{did}" rows="2" data-note="{did}"></textarea></fieldset></div></li>''')
    reply = f'''<div class="reply oa-surface-prussian" id="reply" role="region" aria-labelledby="reply-h">
<h3 id="reply-h">Your reply</h3>
<p>The answers you mark above collect here, ready to paste into our chat. Your marks stay in this browser only. Until you mark one, the box holds a sample reply.</p>
<label class="label" for="reply-text">Reply</label>
<textarea id="reply-text" rows="{min(max(n, 3), 14)}" readonly data-sample="{attr(copy(sample))}">{esc(sample)}</textarea>
<div class="reply-row"><button type="button" id="copy-reply">Copy the reply</button><span id="copy-status" role="status" aria-live="polite"></span></div></div>'''
    intro = (f'<p class="intro">{num_words(n).capitalize() if n < 10 else n} decisions wait for you, numbered A1 to A{n}. Each card gives the question, the options, '
             f'our recommendation with the reason for it, and links to the rules it touches in the live chapters page. Mark an answer on a card and it joins your reply at the end of this section.</p>')
    return section('06', 'decisions', 'Decisions', f'{intro}<ol class="decs">{"".join(cards)}</ol>{reply}')


def record_section(R, builder_checks):
    asked = ''.join(f'<li>{md(x)}</li>' for x in R['asked'])
    proc = ''.join(f'<li><span class="label">{esc(p["stage"])}</span><div>{"".join(f"<p>{md(t)}</p>" for t in (p["text"] if isinstance(p["text"], list) else [p["text"]]))}</div></li>' for p in R['process'])
    rt = ''
    if R.get('red_team'):
        rows = ''.join(f'<tr><th scope="row">{esc(r["lens"])}</th><td class="num">{esc(r.get("score", ""))}</td><td class="num">{esc(r.get("must_fix", ""))}</td>'
                       f'<td class="num">{esc(r.get("should_fix", ""))}</td></tr>' for r in R['red_team'])
        rt = (f'<div class="tw" role="region" tabindex="0" aria-label="Red team scores and findings"><table class="rt-t"><caption class="caption">Each red team lens scored the page 1 to 5 before the fix pass and listed what must and should be fixed.</caption>'
              f'<thead><tr><th scope="col">Lens</th><th scope="col">Score</th><th scope="col">Must fix</th><th scope="col">Should fix</th></tr></thead><tbody>{rows}</tbody></table></div>')
    checks = ''.join(f'<tr><th scope="row">{md(c["name"])}{"<br><code>" + html.escape(c["command"]) + "</code>" if c.get("command") else ""}</th>'
                     f'<td>{"<b>Pass.</b> " if c.get("pass") is True else "<b>Fail.</b> " if c.get("pass") is False else ""}{md(c["result"])}</td></tr>' for c in R['checks'])
    bchecks = ''.join(f'<li>{esc(x)}</li>' for x in builder_checks)
    nt = ''.join(f'<li>{md(x)}</li>' for x in R['not_tested'])
    cl = R['changelog']
    path = lambda x: f'<li><code>{html.escape(str(x))}</code></li>' if re.fullmatch(r'[\w./ -]+', str(x)) and '/' in str(x) else f'<li>{md(x)}</li>'
    created = ''.join(path(x) for x in cl['created']) or '<li>None</li>'
    modified = ''.join(path(x) for x in cl['modified']) or '<li>None</li>'
    body = f'''<div class="rec-grid"><div><h3 class="sub">What was asked</h3><ul class="facts">{asked}</ul></div>
<div><h3 class="sub">How the work was done</h3><ol class="process">{proc}</ol>{rt}</div></div>
<h3 class="sub">Checks run</h3><div class="tw" role="region" tabindex="0" aria-label="Checks run"><table class="ck-t"><thead><tr><th scope="col">Check</th><th scope="col">Result</th></tr></thead><tbody>{checks}</tbody></table></div>
<div class="cols"><div><h3 class="sub">Checks the board builder ran</h3><ul class="facts">{bchecks}</ul></div><div><h3 class="sub">Not tested</h3><ul class="facts">{nt}</ul></div></div>
<h3 class="sub">Change log</h3><p class="caption">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts files">{created}</ul></div><div><h4>Modified</h4><ul class="facts files">{modified}</ul></div></div>'''
    return section('07', 'record', 'Studio record', body)


CSS = r'''
/* Stage board A. The guide's own frame on Newsprint: the grid margins of tokens.css, the title, section, H3 and H4 styles
   at the tracking you approved, Lora Italic only for quoted words, hairlines in Stone, White for cards, and one Prussian
   panel for the reply. Captures sit at true size in frames that scroll sideways on narrow windows. No red on the page. */
:root{--m:var(--oa-layout-grid-phone-small-margin);--g:var(--oa-layout-grid-phone-small-gutter);--max:82rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--mat:var(--oa-color-tint-stone-n90);--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace}
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
.dec :focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
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
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.cover{padding:var(--oa-space-800) 0 0}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-400);max-width:12ch;text-wrap:balance}
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
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:0 0 var(--oa-space-500);text-wrap:balance}
h3,.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;text-wrap:balance}
.sub{margin:var(--oa-space-800) 0 var(--oa-space-300)}
.sec-h + .cols > div:first-child > .sub:first-child,.sec-h + .rec-grid > div:first-child > .sub:first-child{margin-top:0}
@media (min-width:64em){.sec-h + .cols > div > .sub:first-child,.sec-h + .rec-grid > div > .sub:first-child{margin-top:0}}
h4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-300) 0 var(--oa-space-150)}
.cols{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-800)}
@media (min-width:64em){.cols{grid-template-columns:repeat(2,minmax(0,1fr))}}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 var(--oa-space-150);max-width:var(--oa-layout-measure-body-max)}
ul.files li{list-style:none;margin-left:-1.1em}
.note{margin:var(--oa-space-400) 0;padding-left:var(--oa-space-300);border-left:var(--oa-border-width-rule) solid var(--strong);max-width:var(--oa-layout-measure-intro-max)}
.note blockquote{margin:0}.note blockquote p{font:italic 400 clamp(1.1875rem,1.12rem + .3vw,1.375rem)/1.5 var(--oa-font-family-quote);margin:0 0 var(--oa-space-150)}
.note figcaption{margin:0}
/* verdict */
.v-head{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);max-width:28ch;text-wrap:balance}
.ship{font:var(--oa-type-ui);display:inline-block;border:var(--oa-border-width-hairline) solid var(--strong);padding:var(--oa-space-100) var(--oa-space-200);margin-top:var(--oa-space-100)}
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
.tw{overflow-x:auto;border:var(--oa-border-width-hairline) solid var(--hair);background:var(--white)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
caption{caption-side:bottom;text-align:left;padding:var(--oa-space-150) var(--oa-space-200)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-150) var(--oa-space-200);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);background:var(--oa-color-tint-white-n55)}
td.num{text-align:center;font-variant-numeric:tabular-nums}
td.low span{display:inline-block;min-width:1.9em;border:var(--oa-border-width-rule) solid var(--strong);line-height:1.5}
table.scores-t{min-width:44rem}table.ck-t th{width:40%;font-weight:600}table.rt-t{min-width:30rem}
@media (max-width:40em){table.ck-t,table.ck-t tbody,table.ck-t tr,table.ck-t th,table.ck-t td{display:block;width:auto}.ck-t thead{display:none}
  .ck-t tr{border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);padding:var(--oa-space-100) 0}.ck-t th,.ck-t td{border:0;padding:var(--oa-space-050) var(--oa-space-200)}}
/* chapters */
.chnav ol{list-style:none;margin:var(--oa-space-300) 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,15rem),1fr));gap:0 var(--oa-space-400);border-top:var(--oa-border-width-hairline) solid var(--hair)}
.chnav li{border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.chnav a{display:flex;gap:.6em;align-items:center;min-height:var(--oa-size-target-touch);font:var(--oa-type-ui);text-decoration:none}.chnav a:hover{text-decoration:underline}
.chap{margin-top:var(--oa-space-1000);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-300)}
.chap-h{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing)}
.chap-meta{margin:var(--oa-space-100) 0 var(--oa-space-300)}
.instr{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max);margin:0}
.ch-scores{margin:0}
.views{margin-top:var(--oa-space-400)}
.vw-h{max-width:none;margin:var(--oa-space-400) 0 var(--oa-space-200);padding-top:var(--oa-space-150);border-top:var(--oa-border-width-hairline) solid var(--hair)}
.view{margin:0 0 var(--oa-space-500);min-width:0}
.vcap{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--oa-space-050) var(--oa-space-200);margin:0 0 var(--oa-space-150)}
.vk{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}
.vt{font:var(--oa-type-ui)}
.frame{overflow-x:auto;overflow-y:hidden;max-width:100%;width:max-content;border:var(--oa-border-width-hairline) solid var(--hair);background:var(--oa-color-surface-newsprint)}
.frame img{display:block;max-width:none;height:auto}
.hint{margin:var(--oa-space-100) 0 0}
.phones{display:flex;flex-wrap:wrap;gap:var(--oa-space-400) var(--g)}
.phones .view{width:min(100%,24.5rem);margin:0}
.view--phone .vcap{min-height:3.2em;align-content:flex-start}
@media (max-width:30em){.phones .view{width:100%}
  .frame--phone{width:calc(100% + 2 * var(--m));max-width:none;margin-inline:calc(-1 * var(--m));border-left:0;border-right:0}}
/* letter spacing */
.trks{display:grid;gap:var(--oa-space-1000);margin-top:var(--oa-space-500)}
.trk{border-top:var(--oa-border-width-hairline) solid var(--hair);padding-top:var(--oa-space-200)}
.trk-h{display:flex;flex-wrap:wrap;gap:var(--oa-space-050) var(--oa-space-200);align-items:baseline;max-width:none;margin-bottom:var(--oa-space-300)}
.trk-h .label{color:var(--ink)}
.trk-k{margin:0 0 var(--oa-space-100)}
.trk-pair{width:fit-content;max-width:100%}
.trks + .caption{margin-top:var(--oa-space-500)}
.trk-line{margin:0;max-width:none;text-wrap:balance;font-feature-settings:"ss01" 0}
.trk-title{font:var(--oa-type-title)}
.trk-section{font:var(--oa-type-section)}
.trk-h3{font:var(--oa-type-h3)}
.trk-line:not([style]).trk-title{letter-spacing:var(--oa-type-title-letter-spacing)}
.trk-line:not([style]).trk-section{letter-spacing:var(--oa-type-section-letter-spacing)}
.trk-line:not([style]).trk-h3{letter-spacing:var(--oa-type-h3-letter-spacing)}
.hinge{display:flex;align-items:center;gap:12px;margin:var(--oa-space-300) 0;color:var(--oa-color-identity-hinge-divider-on-newsprint)}
.hinge::before,.hinge::after{content:"";flex:1;height:1px;background:currentColor}
.hamp{flex:none;width:21px;height:24px}
/* proofs */
.from{margin:var(--oa-space-400) 0;padding:var(--oa-space-300);background:var(--oa-color-tint-white-n55);border:var(--oa-border-width-hairline) solid var(--hair);max-width:52rem}
.from p:last-child{margin-bottom:0}
.proof{margin-top:var(--oa-space-1000);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-300)}
.proof-h{margin-bottom:var(--oa-space-200)}
.pfig{margin:var(--oa-space-300) 0 0}
.pcap{display:flex;flex-wrap:wrap;gap:var(--oa-space-050) var(--oa-space-200);align-items:baseline;margin:0 0 var(--oa-space-150)}
.pcap a{font:var(--oa-type-ui)}
.pnote{margin-top:var(--oa-space-150);max-width:var(--oa-layout-measure-intro-max)}
/* still to do */
ul.todo{list-style:none;margin:0;padding:0;border-top:var(--oa-border-width-hairline) solid var(--hair)}
ul.todo li{padding:var(--oa-space-200) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair);display:grid;gap:var(--oa-space-050);max-width:var(--oa-layout-measure-intro-max)}
.where{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2)}
a.where{color:var(--ink-2)}
/* decisions */
ol.decs{list-style:none;margin:var(--oa-space-500) 0 0;padding:0;display:grid;gap:var(--oa-space-400)}
.dec{background:var(--white);border:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-300);display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200)}
@media (min-width:48em){.dec{grid-template-columns:6rem minmax(0,1fr);padding:var(--oa-space-400) var(--oa-space-500) var(--oa-space-400) var(--oa-space-400)}}
.dec-b{min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-600);align-items:start}
@media (min-width:80em){.dec-b{grid-template-columns:minmax(0,1fr) minmax(17rem,24rem)}
  .dec-b .ans{margin-top:0;border-top:0;border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:0 0 0 var(--oa-space-400)}}
.dec-n{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);font-variant-numeric:tabular-nums}
.dec-q{margin:0 0 var(--oa-space-200);max-width:30ch}
.dec .label{margin:var(--oa-space-300) 0 var(--oa-space-100);color:var(--oa-color-text-secondary-on-white)}
ol.opts{list-style:none;margin:0;padding:0;max-width:var(--oa-layout-measure-intro-max)}
ol.opts li{display:grid;grid-template-columns:2.2em minmax(0,1fr);padding:var(--oa-space-100) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
.ol{font-weight:600;font-variant-numeric:tabular-nums}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);padding:1px 6px;margin-left:.4em;white-space:nowrap}
.chip--ill{margin:0 .4em 0 0}
.rec{border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);margin-top:var(--oa-space-300);padding-top:var(--oa-space-100);max-width:var(--oa-layout-measure-intro-max)}
.rec p{margin:var(--oa-space-150) 0 0;max-width:none}.rec .label{display:block;margin:0 0 2px}
ul.touch{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:0 var(--oa-space-300)}
ul.touch a{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);font:var(--oa-type-ui)}
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
      var h = f.nextElementSibling; if (h && h.classList.contains('hint')) h.hidden = !over;
    });
  }
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(frames, 120); });
  $$('.frame img').forEach(function (i) { if (!i.complete) i.addEventListener('load', frames); });
  frames();
  // Answers: each card's marks join the reply. Saved in this browser only, keyed to this version of the decisions.
  var out = document.getElementById('reply-text');
  if (!out) return;
  var KEY = 'oa-board-a-answers:' + (document.querySelector('.board') || document.body).getAttribute('data-decisions');
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

FACTS_BY_NUM = {}
PREFIX = ''


def build_page(C, R, facts, tokens_css, cap_prefix, reused):
    global PREFIX
    PREFIX = cap_prefix
    url = (R['chapters_page'].get('url') or '').strip()
    link_note = '' if url else (
        '<p class="caption linknote">The chapters page is not published yet, so each link on this board points at a stand-in address until it is.</p>')
    n_dec = len(C['decisions'])
    ask = C.get('ask') or [
        'Read the verdict, then look through each chapter’s views. Every view’s title opens that place in the live chapters page.',
        'Compare the wordmark proofs at actual size before you answer the decision on width.',
        f'Answer decisions A1 to A{n_dec} on their cards. Your reply collects at the end of the decisions, ready to paste into our chat.',
    ]
    sample = C.get('sample_reply') or (f'A1 to A{n_dec}: as recommended.' if n_dec > 1 else 'A1: as recommended.')
    toc = [('verdict', '01', 'Verdict'), ('chapters', '02', 'Chapters'), ('tracking', '03', 'Letter spacing'), ('proofs', '04', 'Wordmark proofs'),
           ('todo', '05', 'Still to do'), ('decisions', '06', 'Decisions'), ('record', '07', 'Studio record')]
    nav = ''.join(f'<li><a href="#{a}"><span class="n">{n}</span> {t}</a></li>' for a, n, t in toc)
    sample_band = ('<div class="sample" role="note"><p><b>Sample content.</b> This board was built from sample files to test the builder. '
                   'The creative director’s content and the studio record replace them.</p></div>') if (C.get('sample') or R.get('sample')) else ''
    built = datetime.datetime.now(datetime.timezone.utc)
    decision_key = hashlib.sha1(json.dumps(C['decisions'], sort_keys=True).encode()).hexdigest()[:12]
    builder_checks = BUILDER_CHECKS
    title = md(C.get('title') or 'Chapters 01 to 08, for your review', links=False)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{tokens_css}
{CSS}</style></head>
<body><main class="board" data-view-root="overview" data-decisions="{decision_key}">
<header class="cover">
<p class="mast"><b>Oath &amp; Action</b><span class="label">Brand Guide, Edition 06 · Stage board A</span></p>
{sample_band}
<p class="label" style="margin-top:var(--oa-space-800)">For Dustin Cathcart · {words_date(built)}</p>
<h1>{title}</h1>
<p class="intro">{md(C["deck"])}</p>
<div class="ask"><h2>What you are asked</h2><ol>{"".join(f"<li>{md(x)}</li>" for x in ask)}</ol>
<p class="caption" style="margin:0 0 var(--oa-space-050)">A reply can be this short:</p><p class="q">{esc(sample)}</p></div>
<nav class="toc" aria-label="On this board"><ol>{nav}</ol></nav>
</header>
{verdict_section(C)}
{chapters_section(C, facts, link_note)}
{tracking_section(C, facts, tokens_css)}
{proofs_section(C, facts)}
{todo_section(C)}
{decisions_section(C, sample)}
{record_section(R, builder_checks)}
<p class="foot caption">Built {words_date(built)} at {words_time(built)} UTC by <code>work/build/scripts/phase-2/stage_a_board_build.py</code>, from the creative director’s content, the studio record and the chapters page as it stood then.{" These captures came from an earlier run." if reused else ""}</p>
</main>
<script>{JS}</script></body></html>'''
    return page


BUILDER_CHECKS = []


def main():
    global LINK, FACTS_BY_NUM, N_DEC
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    for k in ('content', 'record', 'page', 'out', 'captures', 'publish'):
        ap.add_argument(f'--{k}', type=pathlib.Path, default=DEF[k])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--no-capture', action='store_true')
    a = ap.parse_args()
    for k in ('content', 'record', 'page'):
        need(getattr(a, k).exists(), f'{k} file not found: {getattr(a, k)}')
    C = json.loads(a.content.read_text())
    R = json.loads(a.record.read_text())
    check_content(C)
    check_record(R)
    N_DEC = len(C['decisions'])
    # the views the content names, as capture jobs; anchors are checked against the page once it is read
    views = []
    for n in CHAPTERS:
        for ref in C['chapters'][n]['views']:
            anchor, kind, _ = view_anchor(n, ref, {})
            if kind == 'opening':      # the capture script finds the chapter's own anchor on the page
                views.append({'chapter': n, 'opening': True, 'anchor': None, 'key': f'{n}-opening', 'stem': f'{STEM}{n}-Opening'})
            else:
                views.append({'chapter': n, 'anchor': anchor, 'key': f'{n}-{anchor}', 'stem': f'{STEM}{n}-{slug(anchor)}'})
    seen = set()
    views = [v for v in views if not (v['key'] in seen or seen.add(v['key']))]
    facts, reused = run_capture(a.page, a.captures, views, a.no_capture)
    FACTS_BY_NUM = {c['number']: c for c in facts['chapters']}
    need(sorted(FACTS_BY_NUM) == CHAPTERS, f'the chapters page holds chapters {sorted(FACTS_BY_NUM)}, not 01 to 08')
    for v in views:
        if v.get('opening'):
            v['anchor'] = FACTS_BY_NUM[v['chapter']]['anchor']
    base = (R['chapters_page'].get('url') or '').strip() or R['chapters_page']['placeholder'].strip()
    LINK = Linker(base, facts['anchors'])
    for v in views:
        info = facts['anchors'].get(v['anchor'])
        need(info, f'chapter {v["chapter"]}: no #{v["anchor"]} on the chapters page')
        need(info.get('chapter') == v['chapter'], f'chapter {v["chapter"]}: #{v["anchor"]} belongs to chapter {info.get("chapter")}')
    tagline_page = ((facts.get('tracking') or {}).get('title') or {}).get('text')
    need(tagline_page == TAGLINE, f'the cover tagline on the chapters page reads "{tagline_page}", not the locked line')
    tokens_css = TOKENS.read_text()

    # the builder's own checks, printed on the board as run
    nv = {w: sum(1 for v in facts['views'] if v['width'] == w) for w in (1440, 390)}
    cap_t = datetime.datetime.fromisoformat(facts['captured'].replace('Z', '+00:00'))
    BUILDER_CHECKS.extend([
        f'The builder captured {nv[1440] + nv[390]} views at device scale 2 on {words_date(cap_t)} at {words_time(cap_t)} UTC, {nv[1440]} at 1,440 px and {nv[390]} at 390 px, '
        f'and found each view’s anchor inside its own chapter.' + (' These captures came from an earlier run.' if reused else ''),
        f'From the wordmark proofs appendix it captured {len([g for g in facts["proofs"]["groups"] if g.get("file")])} comparison plates at true size.',
        'Chapter titles, instruction lines, rule titles and the proofs’ notes and captions come from the chapters page itself.',
        'The tagline on the chapters page cover matches the locked line character for character.',
    ])
    if all((facts.get('tracking') or {}).get(k) for k in ('title', 'section', 'h3')):
        t = facts['tracking']
        BUILDER_CHECKS.append(f'On the chapters page at 1,440 px, it measured the letter spacing at {pct(t["title"]["percent"])} for the tagline, '
                              f'{pct(t["section"]["percent"])} for chapter titles and {pct(t["h3"]["percent"])} for rule titles.')
    for d in C['decisions']:
        for ref in d.get('touches', []):
            need(LINK.resolve(ref), f'decision "{d["question"][:50]}": "{ref}" is not an anchor on the chapters page')
    BUILDER_CHECKS.append('Each link to the chapters page, from a view or from a decision, points at an anchor that exists there.')

    def render(prefix):
        return build_page(C, R, facts, tokens_css, prefix, reused)

    rel = os.path.relpath(a.captures, a.out.parent).replace(os.sep, '/') + '/'
    page = render(rel)
    # the board's own words: no em dash anywhere, and the word check on everything it prints
    text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)))
    need('—' not in text, 'em dash on the board')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text, flags=re.I)})
    BUILDER_CHECKS.append('The board prints no em dash' + (f', and the word check flags {", ".join(flagged)}.' if flagged else ' and none of the words the writing rules flag.'))
    page = render(rel)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)

    # the publish copy: the page without its document skeleton, images beside it under captures/
    pub = render('captures/')
    head, body = re.split(r'</head>\s*<body>', pub, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace(f'<title>{TITLE}</title>\n', '')
    body = re.sub(r'</body>\s*</html>\s*$', '', body)
    # the publish skeleton's html element carries no lang, so the page sets it (WCAG 3.1.1)
    setup = '<script>document.documentElement.lang="en";</script>'
    a.publish.mkdir(parents=True, exist_ok=True)
    pdir = a.publish / 'captures'
    if pdir.exists():
        shutil.rmtree(pdir)
    pdir.mkdir(parents=True)
    files = {}
    for f in sorted(a.captures.glob(f'{STEM}*.jpg')):
        shutil.copy2(f, pdir / f.name)
        files[f'captures/{f.name}'] = str(pdir / f.name)
    pub_html = a.publish / a.out.name
    pub_html.write_text(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + setup + body)
    (a.publish / 'files.json').write_text(json.dumps(files, indent=1))
    size = sum(os.path.getsize(p) for p in files.values())
    print(f'wrote {a.out} ({len(page) / 1e3:.0f} kB) with {len(files)} captures ({size / 1e6:.1f} MB) in {a.captures}')
    print(f'wrote {pub_html} and {len(files)} files in {pdir}; publish map in {a.publish / "files.json"}')
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
