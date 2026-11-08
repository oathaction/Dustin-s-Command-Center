"""Build the apply pass changes board (November 7, 2026): what the apply pass changed after Dustin's board A and
Board 6 answers, the creative director's scores after the recheck, the review and its fixes, the decisions still open
and the questions for stage B.

Usage:
    python3 -I work/build/scripts/phase-2/apply_pass_board_build.py [--strict] [--no-capture]
        [--content PATH] [--scores PATH] [--before PATH] [--after PATH] [--out PATH] [--captures DIR] [--publish DIR]

Reads:
    work/boards/phase-2/apply-pass/20261107_Apply-Pass-Board-Content.json   the board's words, cards, views and questions
    work/boards/phase-2/apply-pass/20261107_CD-Scores.json                  the creative director's scores after the recheck
    --before  the chapters page before the pass: `git show 3130c5b:oath-and-action-v6-brand-guide/work/boards/phase-2/
              stage-a/20261106_Stage-A-Chapters.html`, saved outside the repository (required, no default)
    --after   work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html as it stands (never rebuilt here)
    the identity designer's plate pages in work/boards/phase-2/apply-pass/{l6,end-mark,lockmark}/
On every run apply_pass_board_capture.js captures each view of both pages at device scale 2 as JPEG (quality 80), each
plate at true size as PNG, and reads the after page's anchors, so every "where in the guide" link is checked.
Writes:
    work/boards/phase-2/apply-pass/20261107_Apply-Pass-Changes-Board.html   the board (images by relative path)
    work/boards/phase-2/apply-pass/captures/                                the captures and the facts read from the pages
    <publish>/20261107_Apply-Pass-Changes-Board.html and <publish>/captures/ the publish copy, and <publish>/files.json

Captures are shown at their CSS size, never scaled. Colors and type come from work/build/tokens/tokens.css, inlined
(D2-313). Red appears only inside captures and plates. --no-capture reuses the last captures (layout work only).
--strict exits 1 on any warning (a flagged word, an en dash, reused captures, a page over 15 MB).
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
import struct
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261107'
BOARD_DIR = ROOT / 'work/boards/phase-2/apply-pass'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/ab3d43b8-cc87-5ece-933a-c4123e99234a/scratchpad')
DEF = {
    'content': BOARD_DIR / f'{DATE}_Apply-Pass-Board-Content.json',
    'scores': BOARD_DIR / f'{DATE}_CD-Scores.json',
    'before': None,
    'after': ROOT / 'work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html',
    'out': BOARD_DIR / f'{DATE}_Apply-Pass-Changes-Board.html',
    'captures': BOARD_DIR / 'captures',
    'publish': SCRATCH / 'publish-apply-pass-board',
}
CAPTURE_JS = ROOT / 'work/build/scripts/phase-2/apply_pass_board_capture.js'
TOKENS = ROOT / 'work/build/tokens/tokens.css'
AMP = ROOT / 'work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg'
TITLE = 'Apply Pass Changes Board'
STEM = f'{DATE}_Apply-Board-'
RUBRIC = ['Craft', 'Clarity', 'Brand fidelity', 'Usefulness', 'Evidence honesty', 'Accessibility']
RUBRIC_SHORT = {'Brand fidelity': 'Brand', 'Evidence honesty': 'Evidence'}
COLUMN_W = 918          # a 1,440 px view: the chapter column and 24 px either side, 914 to 916 px, inside a 1 px frame
TAGLINE = 'A country that answers to its people.'
LOCKED = {
    'tagline': (TAGLINE, ['answers to its people']),
    'mission': ('Help people understand and improve the rules that shape their lives.', ['rules that shape their lives']),
    'promise': ('We explain how a decision is made and give you a practical way to take part.', ['how a decision is made and give']),
    'commitment': ('Clarity is our duty. Action is our promise.', ['Clarity is our duty', 'Action is our promise']),
}
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat']
LIMIT = 16_000_000
WARN = []


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


URL = ''        # the published chapters page
ANCHORS = {}    # the after page's anchors, from the capture facts
N_Q = 0         # questions on the board, Q1 to Q{N_Q}


def href(anchor):
    return f'{URL}#{anchor}'


def md(s, links=True):
    """Escaped text with `code`, **bold**, each Rule NN.N on the after page linked to the published copy, Qn to its card."""
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f'\x00{len(codes) - 1}\x00'
    t = re.sub(r'`([^`]+)`', keep, str(s))
    t = html.escape(copy(t), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    if links:
        def rl(m):
            a = f'rule-{m.group(1)}-{m.group(2)}'
            return f'<a href="{attr(href(a))}">{m.group(0)}</a>' if a in ANCHORS else m.group(0)
        t = re.sub(r'(?<![\w/#.-])Q([1-9]\d?)\b', lambda m: f'<a href="#q{m.group(1)}">{m.group(0)}</a>' if int(m.group(1)) <= N_Q else m.group(0), t)
        t = re.sub(r'\bRule (\d\d)\.(\d+)\b', rl, t)
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


def num_words(n):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][n] if 0 <= n < 10 else f'{n:,}'


def word_count(s):
    return len(re.findall(r"[\w’'.,-]+", s.replace('“', '').replace('”', '')))


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


def lint(obj, name, skip=('anchor', 'find', 'page', 'selector', 'file', 'stem', 'url')):
    """Chapter 02's marks and locked lines on every string an input holds. Em dashes fail; flagged words warn."""
    for path, s in strings(obj):
        if path.split('.')[-1].split('[')[0] in skip:
            continue
        need('—' not in s, f'{name} {path}: an em dash (W21). Join the parts with a comma and a word, or end the sentence.')
        if '–' in s or ' -- ' in s:
            warn(f'{name} {path}: an en dash or double hyphen; write "to" for a range')
        for w in FLAGGED:
            if re.search(rf'\b{w}\b', s, flags=re.I):
                warn(f'{name} {path}: "{w}" is on the writing rules\' list (W16 to W18, W20)')
        for key, (line, frags) in LOCKED.items():
            for f in frags:
                if f.lower() in s.lower() and line not in copy(s).replace('’', "'") and line not in s:
                    raise BoardError(f'{name} {path}: quotes the {key} inexactly. It reads "{line}" (H01).')


def option_index(r, n):
    if isinstance(r, int) and 1 <= r <= n:
        return r - 1
    if isinstance(r, str) and re.fullmatch(r'[a-h]', r.strip().lower()) and ord(r.strip().lower()) - 97 < n:
        return ord(r.strip().lower()) - 97
    return None


def check_content(C):
    need(isinstance(C, dict), 'the content file must hold one JSON object')
    for k in ('title', 'deck', 'sample_reply', 'url'):
        need(isinstance(C.get(k), str) and C[k].strip(), f'content.{k}: a string')
    need(isinstance(C.get('ask'), list) and C['ask'], 'content.ask: what Dustin is asked, at least one line')
    ch = C.get('changes')
    need(isinstance(ch, dict) and isinstance(ch.get('groups'), list) and ch['groups'], 'content.changes.groups: a list')
    ids = set()
    for g in ch['groups']:
        need(isinstance(g.get('cards'), list) and g['cards'], f'group {g.get("id")}: cards')
        for c in g['cards']:
            cid = c.get('id')
            need(isinstance(cid, str) and re.fullmatch(r'[a-z0-9-]+', cid) and cid not in ids, f'card id {cid!r}: unique, lowercase')
            ids.add(cid)
            need(isinstance(c.get('decision'), str) and c['decision'].strip(), f'card {cid}: the decision in one sentence')
            need(not re.search(r'[a-z)][.?!]\s+[A-Z“"]', c['decision']), f'card {cid}: the decision should be one sentence')
            need(isinstance(c.get('short'), str), f'card {cid}: a short name for the index')
            if c.get('line_only'):
                continue
            need(isinstance(c.get('views'), list) and c['views'], f'card {cid}: views')
            sides = {v.get('side') for v in c['views']}
            need('after' in sides, f'card {cid}: at least one after view')
            if 'before' not in sides:
                need(c.get('same_before'), f'card {cid}: a before view, or "same_before" saying why none is shown')
            for v in c['views']:
                need(v.get('side') in ('before', 'after'), f'card {cid}: each view names its side, before or after')
                need(v.get('stage') or v.get('width') in (1440, 390), f'card {cid}: a view is 1440 or 390 px wide, or a plate stage')
                need(isinstance(v.get('anchor'), str), f'card {cid}: each view names an anchor')
            need(isinstance(c.get('where'), list) and c['where'], f'card {cid}: where it lives in the guide')
    for sec in ('decisions', 'stage_b'):
        need(sec in C, f'content.{sec}')
    qs = C['decisions']['cards'] + C['stage_b']['questions']
    for i, q in enumerate(qs):
        tag = f'question Q{i + 1}'
        need(q.get('id') == f'Q{i + 1}', f'{tag}: ids run Q1, Q2 and on, in order (found {q.get("id")})')
        need(isinstance(q.get('question'), str) and q['question'].strip().endswith('?'), f'{tag}: the question, ending in a question mark')
        o = q.get('options')
        need(isinstance(o, list) and 2 <= len(o) <= 6, f'{tag}: two to six options')
        need(option_index(q.get('recommended'), len(o)) is not None, f'{tag}: the recommended option, as a letter')
        need(isinstance(q.get('why'), str) and q['why'].strip(), f'{tag}: the reason')
        need(isinstance(q.get('named'), bool), f'{tag}: "named": true or false (gate rule 4)')
        need(isinstance(q.get('named_note'), str) and q['named_note'].strip(), f'{tag}: "named_note" says why it does or does not need approval by name')
    lint(C, 'content')


def check_scores(S):
    need(isinstance(S, dict), 'the scores file must hold one JSON object')
    cr = S.get('criteria')
    need(isinstance(cr, list) and [c.get('name') for c in cr] == RUBRIC, f'scores.criteria: six entries in this order: {", ".join(RUBRIC)}')
    for c in cr:
        need(isinstance(c.get('lowest'), int) and 1 <= c['lowest'] <= 5, f'scores.criteria {c["name"]}: "lowest", 1 to 5')
        need(isinstance(c.get('reason'), str) and c['reason'].strip(), f'scores.criteria {c["name"]}: the reason for the lowest score')
    ch = S.get('chapters')
    need(isinstance(ch, dict) and ch, 'scores.chapters')
    for k, v in ch.items():
        need(isinstance(v.get('scores'), dict) and list(v['scores']) == RUBRIC, f'scores.chapters[{k}]: six scores in rubric order')
        for crit, x in v['scores'].items():
            need(isinstance(x.get('score'), int) and 1 <= x['score'] <= 5, f'scores.chapters[{k}].{crit}: a score from 1 to 5')
    # the lowest the file states must be the lowest its chapters give
    for c in cr:
        low = min(v['scores'][c['name']]['score'] for v in ch.values())
        need(low == c['lowest'], f'scores: {c["name"]} lowest is {c["lowest"]}, but the chapters give {low}')
    need(isinstance(S.get('signed_off'), bool), 'scores.signed_off: true or false')
    need('—' not in json.dumps(S, ensure_ascii=False), 'scores: an em dash')


# ------------------------------------------------------------------------------------------------ capture
def png_size(p):
    with open(p, 'rb') as f:
        d = f.read(24)
    return struct.unpack('>II', d[16:24])


def card_views(C):
    """Every view each card names, as a capture job entry."""
    out = []
    for g in C['changes']['groups']:
        for c in g['cards']:
            n = {}
            for v in c.get('views', []):
                w = 'Plate' if v.get('stage') else str(v['width'])
                n[(v['side'], w)] = n.get((v['side'], w), 0) + 1
                cid = '-'.join(x.upper() if i == 0 and len(x) <= 3 else x[:1].upper() + x[1:] for i, x in enumerate(c['id'].split('-')))
                stem = f'{STEM}{cid}-{v["side"].capitalize()}-{n[(v["side"], w)]}-{w}'
                v['key'] = stem[len(STEM):]
                v['stem'] = stem
                out.append({'key': v['key'], 'stem': stem, 'page': v['side'], 'width': v.get('width'), 'stage': bool(v.get('stage')),
                            'anchor': v['anchor'], 'find': v.get('find'), 'until': v.get('until'), 'offset': v.get('offset', 0), 'height': v.get('height')})
    return out


def plate_jobs(C):
    out = []
    for q in C['decisions']['cards']:
        for p in q.get('plates', []):
            if p.get('page'):
                p['stem'] = f'{STEM}{q["id"]}-{p["key"]}'
                out.append({'key': p['key'], 'stem': p['stem'], 'page': str(BOARD_DIR / p['page']), 'selector': p['selector'], 'viewport': p.get('viewport', 1960)})
    return out


def compare_job(C):
    for q in C['decisions']['cards']:
        for p in q.get('plates', []):
            if p.get('compare'):
                p['stem'] = f'{STEM}{q["id"]}-{p["key"]}'
                cmp = p['compare']
                return {'key': p['key'], 'stem': p['stem'], 'tokens': str(TOKENS), 'sizes': cmp['sizes'],
                        'rows': [{'label': r['label'], 'file': str(ROOT / r['file'])} for r in cmp['rows']]}
    return None


def run_capture(pages, cap_dir, views, plates, compare, no_capture):
    facts_path = cap_dir / f'{DATE}_Apply-Board-Capture-Facts.json'
    if no_capture:
        need(facts_path.exists(), f'--no-capture: no earlier captures in {cap_dir}')
        warn('captures reused from an earlier run (--no-capture)')
        return json.loads(facts_path.read_text()), True
    cap_dir.mkdir(parents=True, exist_ok=True)
    for old in list(cap_dir.glob(f'{STEM}*.jpg')) + list(cap_dir.glob(f'{STEM}*.png')):
        old.unlink()
    job = {'pages': {k: str(v) for k, v in pages.items()}, 'out': str(cap_dir), 'facts': str(facts_path), 'quality': 80,
           'views': views, 'plates': plates, 'compare': compare}
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(job, f)
        jp = f.name
    try:
        r = subprocess.run(['node', str(CAPTURE_JS), jp], cwd=ROOT, capture_output=True, text=True, timeout=2400)
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


def img_tag(file, w, h, alt, eager=False):
    return (f'<img src="{attr(PREFIX + file)}" width="{w}" height="{h}" alt="{attr(copy(alt))}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')


def frame(inner, name, phone=False):
    """A frame that holds a capture at true size and scrolls sideways when the window is narrower."""
    return (f'<div class="frame{" frame--phone" if phone else ""}" role="region" tabindex="0" aria-label="{attr(copy(name))}">{inner}</div>'
            f'<p class="hint caption" hidden>Wider than this column. Scroll inside the frame to see all of it.</p>')


def pips(score):
    cells = ''.join(f'<i class="{"on" if k < score else ""}"></i>' + ('<b></b>' if k == 3 else '') for k in range(5))
    return f'<span class="pips" aria-hidden="true">{cells}</span>'


def section(num, sid, title, body):
    return (f'<section class="sec" id="{sid}" aria-labelledby="{sid}-h"><h2 class="sec-h" id="{sid}-h">'
            f'<span class="n">{num}</span> {title}</h2>{body}</section>')


def anchor_label(a):
    info = ANCHORS[a]
    lab = info['label']
    if info['kind'] == 'chapter' and info.get('chapter'):
        lab = f'Chapter {lab}' if re.match(r'\d\d ', lab) else lab
    return lab


# ---- 01 scores
def scores_section(C, S):
    cr = S['criteria']
    at = sum(1 for c in cr if c['lowest'] >= 4)
    signed = S['signed_off']
    rows = ''.join(
        f'<li><span class="sc-k">{esc(c["name"])}</span><span class="sc-v"><span class="sc-n">{c["lowest"]}</span>'
        f'<span class="caption">of 5</span>{pips(c["lowest"])}</span><span class="sc-line">{md(c["reason"])}</span></li>' for c in cr)
    keys = list(S['chapters'])
    head = ''.join(f'<th scope="col">{esc(RUBRIC_SHORT.get(r, r))}</th>' for r in RUBRIC)
    body = ''
    for k in keys:
        v = S['chapters'][k]
        name = f'{k} {v["title"]}' if re.fullmatch(r'\d\d', k) else v['title']
        cells = ''.join(f'<td class="num{" low" if v["scores"][r]["score"] == min(S["chapters"][x]["scores"][r]["score"] for x in keys) and v["scores"][r]["score"] < 5 else ""}">'
                        f'<span>{v["scores"][r]["score"]}</span></td>' for r in RUBRIC)
        body += f'<tr><th scope="row">{esc(name)}</th>{cells}</tr>'
    reasons = ''
    for k in keys:
        v = S['chapters'][k]
        name = f'{k} {v["title"]}' if re.fullmatch(r'\d\d', k) else v['title']
        li = ''.join(f'<li><span class="rk">{esc(r)} {v["scores"][r]["score"]}</span> {md(v["scores"][r]["reason"])}</li>' for r in RUBRIC)
        reasons += f'<details class="why-d"><summary>{esc(name)}</summary><ul>{li}</ul></details>'
    ship = ('The guide ships at 4 on every criterion, and every chapter now scores 4 or above on all six.' if at == 6 else
            f'{num_words(at).capitalize()} of the six criteria reach 4 in every chapter. The guide ships at 4 on every one.')
    so = (f'<p class="signed"><span class="label">Sign-off</span> {esc(C["scores"]["signed"] if signed else C["scores"]["not_signed"])}</p>')
    opens = ''.join(f'<li>{md(x)}</li>' for x in C['scores'].get('open', []))
    out = (f'{paras(C["scores"]["intro"], "intro")}{so}<p class="ship">{esc(ship)}</p>'
           f'<h3 class="sub">Lowest score on each criterion</h3><p class="caption legend">{md(C["scores"]["legend"])}</p><ol class="scores">{rows}</ol>'
           f'<h3 class="sub">By chapter</h3><div class="tw" role="region" tabindex="0" aria-label="Scores by chapter"><table class="scores-t">'
           f'<caption class="caption">{esc(C["scores"]["table_caption"])}</caption>'
           f'<thead><tr><th scope="col">Chapter</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'
           f'<p class="caption reasons-h">Every score with its reason, by chapter</p><div class="reasons">{reasons}</div>'
           f'<h3 class="sub">Left open after the recheck</h3><ul class="facts open">{opens}</ul>')
    return section('01', 'scores', 'Scores', out)


# ---- 02 what changed
def view_figure(v, fv):
    side = 'Before' if v['side'] == 'before' else 'After'
    a = fv.get('about') or {}
    if v.get('label'):
        lab = v['label']
    elif a.get('kind') == 'chapter':
        lab = f'Chapter {a["chapter"]} {a["chapter_title"]}, opening' if a.get('chapter') else a.get('chapter_title', '')
    elif a.get('proof'):
        lab = f'Identity proofs, {a["proof"]}' if v['side'] == 'after' else f'Wordmark width proofs, {a["proof"]}'
    elif a.get('rule'):
        lab = f'Rule {a["rule"]}' + (f', {a["figure"]}' if a.get('figure') else f', {a["rule_title"]}')
    else:
        lab = (a.get('figure') or v['anchor']) + (f', chapter {a["chapter"]}' if a.get('chapter') else '')
    w, h = fv['css_w'], fv['css_h']
    phone = fv['width'] == 390
    where = ('the phone screen under the masthead' if phone else
             'the plate alone, at true size' if fv['width'] == 'stage' else 'the chapter column under the masthead')
    when = 'before the apply pass' if v['side'] == 'before' else 'as it stands now'
    wtxt = '390 px' if phone else '1,440 px' if fv['width'] == 1440 else 'true size'
    alt = v.get('alt') or f'{side}: the chapters page {when}, {lab}, at a {wtxt} window: {where}.'
    if fv['width'] == 'stage':
        alt = v.get('alt') or f'{side}: the chapters page {when}, {lab}, the plate alone at true size.'
    name = f'{side}, {lab}, {w:,} by {h:,} px'
    link = ''
    if v['side'] == 'after' and v['anchor'] in ANCHORS:
        link = f'<a class="vlink" href="{attr(href(v["anchor"]))}">Open in the published page</a>'
    return (f'<figure class="view view--{v["side"]}{" view--phone" if phone else ""}">'
            f'<figcaption class="vcap"><span class="tag tag--{v["side"]}">{side}</span><span class="vt">{esc(lab)}</span>'
            f'<span class="vs caption">{w:,} by {h:,} px</span>{link}</figcaption>'
            f'{frame(img_tag(fv["file"], w, h, alt), name, phone=phone)}</figure>')


def change_card(c, g, views_by_key):
    if c.get('line_only'):
        return (f'<li class="chg chg--line" id="c-{c["id"]}"><p class="chg-id label">{esc(c["label"])}</p>'
                f'<div><h4 class="chg-h4">{md(c["decision"])}</h4>{paras(c.get("text"))}</div></li>')
    vs = [(v, views_by_key[v['key']]) for v in c['views']]
    wide = any(fv['css_w'] > COLUMN_W for _, fv in vs)
    desk = [x for x in vs if x[1]['width'] != 390]
    phone = [x for x in vs if x[1]['width'] == 390]
    blocks = ''
    if desk:
        bef = ''.join(view_figure(v, fv) for v, fv in desk if v['side'] == 'before')
        aft = ''.join(view_figure(v, fv) for v, fv in desk if v['side'] == 'after')
        same = f'<p class="caption same">{md(c["same_before"])}</p>' if c.get('same_before') else ''
        lab = 'At 1,440 px' if all(fv['width'] == 1440 for _, fv in desk) else 'At 1,440 px and at true size' if any(fv['width'] == 1440 for _, fv in desk) else 'At true size'
        blocks += f'<p class="label vw-h">{lab}</p>{same}{bef}{hinge() if bef and aft else ""}{aft}'
    if phone:
        blocks += f'<p class="label vw-h">At 390 px</p><div class="phones">{"".join(view_figure(v, fv) for v, fv in phone)}</div>'
    where = ''.join(f'<li><a href="{attr(href(a))}">{esc(anchor_label(a))}</a></li>' for a in c['where'])
    return (f'<li class="chg{" chg--wide" if wide else ""}" id="c-{c["id"]}"><div class="chg-text">'
            f'<p class="chg-id label">{esc(c["label"])}</p><h4 class="chg-h4">{md(c["decision"])}</h4>{paras(c.get("text"))}'
            f'<p class="label wh">Where it lives in the guide</p><ul class="where-l">{where}</ul></div>'
            f'<div class="chg-views">{blocks}</div></li>')


def changes_section(C, views_by_key):
    ch = C['changes']
    groups = ''
    index = ''
    for g in ch['groups']:
        cards = ''.join(change_card(c, g, views_by_key) for c in g['cards'])
        groups += (f'<div class="grp" id="g-{g["id"]}"><h3 class="grp-h">{esc(g["title"])}</h3>{paras(g.get("intro"), "grp-intro")}'
                   f'<ol class="chgs">{cards}</ol></div>')
        items = ''.join(f'<li><a href="#c-{c["id"]}"><span class="n">{esc(c["label"].split(" · ")[0])}</span> {esc(c["short"])}</a></li>' for c in g['cards'])
        index += f'<div><p class="label">{esc(g["title"])}</p><ol>{items}</ol></div>'
    body = f'{paras(ch["intro"], "intro")}<nav class="cidx" aria-label="Changes on this board">{index}</nav>{groups}'
    return section('02', 'changes', 'What changed', body)


# ---- 03 review
def review_section(C):
    R = C['review']
    musts = ''.join(f'''<li class="mf"><p class="label mf-id">{esc(m["id"])} · {esc(m["where"])}</p><h4 class="mf-h">{md(m["title"], links=False)}</h4>
<p><span class="label">Found</span> {md(m["found"])}</p><p><span class="label">Fixed</span> {md(m["fixed"])}</p></li>''' for m in R['must'])
    total = sum(r['count'] for r in R['should']['rows'])
    need(total == R['should']['total'], f'review.should: the rows add to {total}, not {R["should"]["total"]}')
    rows = ''.join(f'<tr><th scope="row">{md(r["state"])}</th><td class="num"><span>{r["count"]}</span></td><td>{md(r["items"])}</td></tr>' for r in R['should']['rows'])
    body = (f'{paras(R["intro"], "intro")}<h3 class="sub">The four Must fix items</h3><ol class="mfs">{musts}</ol>'
            f'<h3 class="sub">The {R["should"]["total"]} Should fix items</h3>{paras(R["should"]["intro"])}'
            f'<div class="tw" role="region" tabindex="0" aria-label="Should fix items by state"><table class="sf-t"><thead><tr>'
            f'<th scope="col">State</th><th scope="col">Items</th><th scope="col">Which</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'{paras(R.get("after"))}')
    return section('03', 'review', 'What the review found', body)


# ---- 04 and 05: questions
def plate_figure(p, facts_plates):
    if p.get('copy'):
        f = p['file']
        w, h = p['w'], p['h']
    else:
        fp = facts_plates[p['key']]
        f, w, h = fp['file'], fp['css_w'], fp['css_h']
    return (f'<figure class="pl{" pl--wide" if w > 760 else ""}"><figcaption class="pcap"><span class="label">{esc(p["label"])}</span>'
            f'<span class="caption">{w:,} by {h:,} px, true size</span></figcaption>'
            f'{frame(img_tag(f, w, h, p["alt"]), p["label"] + ", true size")}<p class="caption pnote">{md(p["caption"])}</p></figure>')


def versions_block(vs):
    cols = ''
    for v in vs:
        n = sum(word_count(s) for s in re.split(r'(?<=[.?])\s+', v['text']) if s)
        sents = [s for s in re.split(r'(?<=[.?])\s+', v['text']) if s.strip()]
        size = (f'One sentence of {n} words' if len(sents) == 1 else
                f'{num_words(len(sents)).capitalize()} sentences, of {" and ".join(str(word_count(s)) for s in sents)} words')
        cols += (f'<div class="ver"><p class="label">{esc(v["label"])}</p><blockquote><p>{esc(v["text"])}</p></blockquote>'
                 f'<p class="caption">{esc(v["source"])}. {size}.</p></div>')
    return f'<div class="vers">{cols}</div>'


def question_card(q, facts_plates):
    did = q['id']
    rec = option_index(q['recommended'], len(q['options']))
    opts, radios = '', ''
    for j, op in enumerate(q['options']):
        text = op if isinstance(op, str) else op['text']
        short = (op.get('short') if isinstance(op, dict) else None) or text
        letter = chr(97 + j)
        chip = ' <span class="chip">Recommended</span>' if j == rec else ''
        opts += f'<li><span class="ol">({letter})</span><span>{md(text)}{chip}</span></li>'
        radios += (f'<label class="rad"><input type="radio" name="ans-{did}" value="{letter}" data-short="{attr(copy(short))}">'
                   f'<span>({letter}) {esc(short)}{" · recommended" if j == rec else ""}</span></label>')
    named = ''
    if q['named']:
        radios += (f'<label class="rad chk"><input type="checkbox" data-named="{did}"><span>I approve {did} by name</span></label>')
        named = f'<p class="named"><span class="chip chip--named">Needs your approval by name</span></p>'
    plates = ''
    if q.get('plates'):
        plates = f'<div class="dec-plates">{"".join(plate_figure(p, facts_plates) for p in q["plates"])}</div>'
    if q.get('versions'):
        plates += versions_block(q['versions'])
    src = f'<p class="caption src">{md(q["source"])}</p>' if q.get('source') else ''
    return f'''<li class="dec" id="{did.lower()}" data-dec="{did}" data-rec="{chr(97 + rec)}"{' data-named-q="1"' if q['named'] else ''}>
<div class="dec-head"><div class="dec-n" aria-hidden="true">{did}</div><div class="dec-hb"><h3 class="dec-q"><span class="vh">{did}. </span>{md(q["question"], links=False)}</h3>{named}{paras(q.get("context"))}</div></div>
{plates}
<div class="dec-b"><div class="dec-main"><p class="label">Options</p><ol class="opts">{opts}</ol>
<div class="rec"><p><span class="label">We recommend</span> ({chr(97 + rec)}) {md(q.get("recommendation") or (q["options"][rec] if isinstance(q["options"][rec], str) else q["options"][rec]["text"]))}</p>
<p><span class="label">Why</span> {md(q["why"])}</p><p><span class="label">Approval</span> {md(q["named_note"])}</p></div>{src}</div>
<fieldset class="ans"><legend>Your answer to {did}</legend><div class="rads">{radios}</div>
<label class="nl" for="note-{did}">A note, or an answer of your own</label><textarea id="note-{did}" rows="2" data-note="{did}"></textarea></fieldset></div></li>'''


def decisions_section(C, facts_plates):
    D = C['decisions']
    cards = ''.join(question_card(q, facts_plates) for q in D['cards'])
    return section('04', 'decisions', 'Decisions for you', f'{paras(D["intro"], "intro")}<ol class="decs">{cards}</ol>')


def stage_b_section(C, facts_plates):
    B = C['stage_b']
    rows = ''.join(f'<tr><th scope="row"><span class="n">{esc(r["chapter"])}</span> {esc(r["title"])}</th><td>{md(r["holds"])}</td><td>{md(r["who"])}</td></tr>' for r in B['scope'])
    table = (f'<div class="tw" role="region" tabindex="0" aria-label="Proposed scope for chapters 09 to 12"><table class="scope-t">'
             f'<caption class="caption">{esc(B["scope_caption"])}</caption><thead><tr><th scope="col">Chapter</th><th scope="col">What it would hold</th>'
             f'<th scope="col">Who draws or writes it</th></tr></thead><tbody>{rows}</tbody></table></div>')
    cards = ''.join(question_card(q, facts_plates) for q in B['questions'])
    body = (f'{paras(B["intro"], "intro")}<h3 class="sub">Proposed scope</h3>{table}{paras(B.get("after_scope"))}'
            f'<h3 class="sub">Six questions before stage B starts</h3>{paras(B.get("questions_intro"))}<ol class="decs">{cards}</ol>')
    return section('05', 'stage-b', 'Stage B', body)


def reply_section(C, sample, n):
    box = f'''<div class="reply oa-surface-prussian" id="reply-box" role="region" aria-labelledby="reply-h">
<h3 id="reply-h">{esc(C["reply"]["title"])}</h3>
{paras(C["reply"]["text"])}
<label class="label" for="reply-text">Reply</label>
<textarea id="reply-text" rows="{min(max(n, 4), 14)}" readonly data-sample="{attr(copy(sample))}">{esc(sample)}</textarea>
<div class="reply-row"><button type="button" id="copy-reply">Copy the reply</button><span id="copy-status" role="status" aria-live="polite"></span></div></div>'''
    return section('06', 'reply', 'Your reply', box)


# ------------------------------------------------------------------------------------------------ style and script
CSS = r'''
/* The apply pass changes board. The guide's own frame on Newsprint: the grid margins of tokens.css, the title, section,
   H3 and H4 styles at the tracking Dustin approved, Lora Italic only for quoted words, hairlines in Stone, White for
   decision cards, and one Prussian panel for the reply. Captures sit at true size in frames that scroll sideways on
   narrow windows; before sits above after, joined by the hinge divider. No red of the board's own. */
:root{--m:var(--oa-layout-grid-phone-small-margin);--g:var(--oa-layout-grid-phone-small-gutter);--max:82rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace}
@media (min-width:24.375em){:root{--m:var(--oa-layout-grid-phone-margin);--g:var(--oa-layout-grid-phone-gutter)}}
@media (min-width:48em){:root{--m:var(--oa-layout-grid-tablet-margin);--g:var(--oa-layout-grid-tablet-gutter)}}
@media (min-width:64em){:root{--m:var(--oa-layout-grid-desktop-margin);--g:var(--oa-layout-grid-desktop-gutter)}}
@media (min-width:90em){:root{--m:var(--oa-layout-grid-wide-margin);--g:var(--oa-layout-grid-wide-gutter)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--oa-color-surface-newsprint);scroll-padding-top:var(--oa-space-300)}
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
/* cover */
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.cover{padding:var(--oa-space-800) 0 0}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-400);max-width:13ch;text-wrap:balance}
.cover-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500) var(--oa-space-800);align-items:start}
@media (min-width:64em){.cover-grid{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}}
.cover .intro{margin-bottom:var(--oa-space-200)}
.ask{background:var(--white);border:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-300) var(--oa-space-400)}
.ask h2{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-200)}
.ask ol{margin:0 0 var(--oa-space-300);padding-left:1.4em}.ask li{margin:0 0 var(--oa-space-100)}
.ask .q{font:italic 400 1.125rem/1.5 var(--oa-font-family-quote);margin:0}
.pages{margin-top:var(--oa-space-300)}.pages p{font:var(--oa-type-body-small);color:var(--ink-2)}
.toc{margin:var(--oa-space-600) 0 0;border-top:var(--oa-border-width-hairline) solid var(--hair);border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.toc ol{list-style:none;margin:0;padding:var(--oa-space-100) 0;display:flex;flex-wrap:wrap;gap:0 var(--oa-space-400)}
.toc a{display:inline-flex;align-items:center;gap:.5em;min-height:var(--oa-size-target-touch);font:var(--oa-type-ui);text-decoration:none}
.toc a:hover{text-decoration:underline}
/* sections */
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-400)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:0 0 var(--oa-space-500);text-wrap:balance}
h3,.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;text-wrap:balance}
.sub{margin:var(--oa-space-800) 0 var(--oa-space-300)}
h4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-150);text-wrap:balance}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 var(--oa-space-150);max-width:var(--oa-layout-measure-intro-max)}
/* scores */
.signed{font:var(--oa-type-ui);display:flex;flex-wrap:wrap;gap:var(--oa-space-100) var(--oa-space-200);align-items:baseline;margin:var(--oa-space-300) 0 var(--oa-space-100)}
.signed .label{color:var(--ink)}
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
@media (min-width:48em){ol.scores li{grid-template-columns:13rem 13rem minmax(0,1fr)}.sc-line{grid-column:auto}}
.tw{overflow-x:auto;border:var(--oa-border-width-hairline) solid var(--hair);background:var(--white)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
caption{caption-side:bottom;text-align:left;padding:var(--oa-space-150) var(--oa-space-200)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-150) var(--oa-space-200);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary-on-white);background:var(--oa-color-tint-white-n55)}
tbody th{font-weight:600}
td.num{text-align:center;font-variant-numeric:tabular-nums}
td.low span{display:inline-block;min-width:1.9em;border:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);line-height:1.5}
table.scores-t{min-width:46rem}table.sf-t{min-width:34rem;table-layout:fixed}table.sf-t thead th:first-child{width:30%}table.sf-t thead th:nth-child(2){width:6rem}
.tw + p,.tw + .caption{margin-top:var(--oa-space-300)}
table.scope-t{min-width:44rem}table.scope-t th{width:22%}table.scope-t td:last-child{width:28%}
.reasons-h{margin:var(--oa-space-300) 0 var(--oa-space-100)}
.reasons{border-top:var(--oa-border-width-hairline) solid var(--hair);display:grid;grid-template-columns:minmax(0,1fr);column-gap:var(--oa-space-500)}
@media (min-width:64em){.reasons{grid-template-columns:repeat(2,minmax(0,1fr))}}
.why-d{border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.why-d summary{cursor:pointer;min-height:var(--oa-size-target-touch);display:flex;align-items:center;font:var(--oa-type-ui)}
.why-d ul{margin:0 0 var(--oa-space-200);padding-left:1.1em;font:var(--oa-type-body-small)}.why-d li{margin:0 0 var(--oa-space-100)}
.rk{font-weight:600}
/* what changed */
.cidx{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-500);margin:var(--oa-space-400) 0 0;padding:var(--oa-space-300) 0;border-top:var(--oa-border-width-hairline) solid var(--hair);border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.cidx{grid-template-columns:repeat(2,minmax(0,1fr))}}
.cidx ol{list-style:none;margin:var(--oa-space-100) 0 0;padding:0}
.cidx a{display:flex;gap:.6em;align-items:baseline;padding:var(--oa-space-050) 0;min-height:2rem;font:var(--oa-type-body-small);text-decoration:none}
.cidx a:hover{text-decoration:underline}.cidx .n{flex:none;min-width:3.6em;font-weight:600}
.grp{margin-top:var(--oa-space-1000)}
.grp-h{border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-300);margin-bottom:var(--oa-space-200)}
.grp-intro{max-width:var(--oa-layout-measure-intro-max)}
ol.chgs{list-style:none;margin:var(--oa-space-400) 0 0;padding:0}
.chg{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-600);padding:var(--oa-space-500) 0 var(--oa-space-700);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:80em){.chg:not(.chg--wide):not(.chg--line){grid-template-columns:minmax(0,1fr) 57.5rem}
  .chg:not(.chg--wide) .chg-text{position:sticky;top:var(--oa-space-300);align-self:start}}
.chg-id{margin:0 0 var(--oa-space-150);color:var(--ink)}
.chg-h4{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0 0 var(--oa-space-200);max-width:24ch}
.chg--wide .chg-h4{max-width:32ch}
.chg-text > p{font:var(--oa-type-body-small);max-width:var(--oa-layout-measure-body-max)}
.chg--wide .chg-text > p{font:var(--oa-type-body)}
.wh{margin:var(--oa-space-300) 0 var(--oa-space-050)}
ul.where-l{list-style:none;margin:0;padding:0}
ul.where-l a{display:inline-flex;align-items:center;min-height:2.25rem;font:var(--oa-type-body-small);font-weight:600}
.chg--line{grid-template-columns:minmax(0,1fr);padding:var(--oa-space-300) 0}
@media (min-width:48em){.chg--line{grid-template-columns:9rem minmax(0,1fr)}}
.chg--line .chg-h4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);max-width:40ch}
.chg--line p{font:var(--oa-type-body-small)}
.chg-views{min-width:0}
.vw-h{max-width:none;margin:0 0 var(--oa-space-200);padding-top:var(--oa-space-150);border-top:var(--oa-border-width-hairline) solid var(--hair)}
.vw-h ~ .vw-h{margin-top:var(--oa-space-500)}
.same{margin:0 0 var(--oa-space-200)}
.view{margin:0 0 var(--oa-space-300);min-width:0;width:fit-content;max-width:100%}
.view + .view{margin-top:var(--oa-space-400)}
.vcap{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--oa-space-050) var(--oa-space-200);margin:0 0 var(--oa-space-150)}
.tag{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;padding:2px 7px;border:var(--oa-border-width-hairline) solid var(--strong)}
.tag--after{background:var(--oa-color-palette-charcoal);color:var(--oa-color-text-primary-on-charcoal);border-color:var(--oa-color-palette-charcoal)}
.vt{font:var(--oa-type-ui)}
.vlink{font:var(--oa-type-body-small);margin-left:auto}
.frame{overflow-x:auto;overflow-y:hidden;max-width:100%;width:max-content;border:var(--oa-border-width-hairline) solid var(--hair);background:var(--oa-color-surface-newsprint)}
.frame img{display:block;max-width:none;height:auto}
.hint{margin:var(--oa-space-100) 0 0}
.phones{display:flex;flex-wrap:wrap;gap:var(--oa-space-400) var(--oa-space-300)}
.phones .view{width:min(100%,24.5rem);margin:0}
.phones .view + .view{margin-top:0}
.view--phone .vcap{min-height:3.4em;align-content:flex-start}
@media (max-width:30em){.phones .view{width:100%}
  .frame--phone{width:calc(100% + 2 * var(--m));max-width:none;margin-inline:calc(-1 * var(--m));border-left:0;border-right:0}}
.hinge{display:flex;align-items:center;gap:12px;margin:var(--oa-space-400) 0;max-width:57.5rem;color:var(--oa-color-identity-hinge-divider-on-newsprint)}
.hinge::before,.hinge::after{content:"";flex:1;height:1px;background:currentColor}
.hamp{flex:none;width:21px;height:24px}
/* review */
ol.mfs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300)}
@media (min-width:64em){ol.mfs{grid-template-columns:repeat(2,minmax(0,1fr))}}
.mf{border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-200)}
.mf-id{margin:0 0 var(--oa-space-100);color:var(--ink)}
.mf p{font:var(--oa-type-body-small)}.mf .label{display:block;margin-bottom:2px}
/* decisions */
ol.decs{list-style:none;margin:var(--oa-space-500) 0 0;padding:0;display:grid;gap:var(--oa-space-500)}
.dec{background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-300);display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300);min-width:0}
@media (min-width:48em){.dec{padding:var(--oa-space-400) var(--oa-space-500)}}
.dec-head{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-100) var(--oa-space-300)}
@media (min-width:48em){.dec-head{grid-template-columns:5rem minmax(0,1fr)}}
.dec-n{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);font-variant-numeric:tabular-nums}
.dec-q{margin:0 0 var(--oa-space-200);max-width:30ch}
.dec-hb > p{max-width:var(--oa-layout-measure-intro-max)}
.named{margin:0 0 var(--oa-space-200)}
.dec .label{color:var(--oa-color-text-secondary-on-white)}
.dec .caption{color:var(--oa-color-text-secondary-on-white)}
.dec-plates{display:flex;flex-wrap:wrap;gap:var(--oa-space-400) var(--oa-space-500);min-width:0;padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white)}
.pl{margin:0;min-width:0;max-width:100%}.pl--wide{flex-basis:100%}
.pcap{display:flex;flex-wrap:wrap;gap:var(--oa-space-050) var(--oa-space-200);align-items:baseline;margin:0 0 var(--oa-space-150)}
.pcap .label{color:var(--oa-color-text-primary-on-white)}
.pnote{margin:var(--oa-space-150) 0 0;max-width:var(--oa-layout-measure-intro-max)}
.dec .frame{border-color:var(--oa-color-border-hairline-on-white)}
.vers{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300)}
@media (min-width:48em){.vers{padding-left:calc(5rem + var(--oa-space-300))}}
@media (min-width:64em){.vers{grid-template-columns:repeat(3,minmax(0,1fr))}}
.ver{border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);padding-top:var(--oa-space-150)}
.ver .label{color:var(--oa-color-text-primary-on-white);margin:0 0 var(--oa-space-100)}
.ver blockquote{margin:0}.ver blockquote p{font:italic 400 1.1875rem/1.5 var(--oa-font-family-quote);margin:0 0 var(--oa-space-150)}
.dec-b{min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-600);align-items:start}
@media (min-width:48em){.dec-b{padding-left:calc(5rem + var(--oa-space-300))}}
@media (min-width:80em){.dec-b{grid-template-columns:minmax(0,1fr) minmax(17rem,24rem)}
  .dec-b .ans{margin-top:0;border-top:0;border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:0 0 0 var(--oa-space-400)}}
.dec-main > .label:first-child{margin:0 0 var(--oa-space-100)}
ol.opts{list-style:none;margin:0;padding:0;max-width:var(--oa-layout-measure-intro-max)}
ol.opts li{display:grid;grid-template-columns:2.2em minmax(0,1fr);padding:var(--oa-space-100) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
.ol{font-weight:600;font-variant-numeric:tabular-nums}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);padding:1px 6px;margin-left:.4em;white-space:nowrap}
.chip--named{margin:0;background:var(--oa-color-palette-charcoal);color:var(--oa-color-text-primary-on-charcoal);border-color:var(--oa-color-palette-charcoal)}
.chip--ill{margin:0 .4em 0 0}
.rec{border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);margin-top:var(--oa-space-300);padding-top:var(--oa-space-100);max-width:var(--oa-layout-measure-intro-max)}
.rec p{margin:var(--oa-space-150) 0 0;max-width:none}.rec .label{display:block;margin:0 0 2px}
.src{margin-top:var(--oa-space-300)}
.ans{margin:var(--oa-space-400) 0 0;padding:var(--oa-space-200) 0 0;border:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);min-width:0}
.ans legend{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;padding:0;float:left;width:100%;margin-bottom:var(--oa-space-100)}
.rads{display:grid;gap:0;clear:both}
.rad{display:flex;gap:var(--oa-space-150);align-items:center;min-height:var(--oa-size-target-touch);cursor:pointer;max-width:var(--oa-layout-measure-intro-max)}
.rad input{width:20px;height:20px;margin:0;flex:none;accent-color:var(--oa-color-palette-charcoal)}
.chk{margin-top:var(--oa-space-100);border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);font-weight:600}
.nl{display:block;font:var(--oa-type-body-small);color:var(--oa-color-text-secondary-on-white);margin:var(--oa-space-200) 0 var(--oa-space-100)}
textarea{display:block;width:100%;max-width:var(--oa-layout-measure-intro-max);font:var(--oa-type-body);color:var(--oa-color-text-primary-on-white);background:var(--white);
  border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);border-radius:0;padding:var(--oa-space-150);resize:vertical}
/* reply */
.reply{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);padding:var(--oa-space-400) var(--oa-space-300)}
@media (min-width:48em){.reply{padding:var(--oa-space-500)}}
.reply h3{color:inherit;margin:0 0 var(--oa-space-200)}
.reply p{color:var(--oa-color-text-primary-on-prussian);max-width:var(--oa-layout-measure-intro-max)}
.reply .label{color:var(--oa-color-text-secondary-on-prussian);display:block;margin:var(--oa-space-300) 0 var(--oa-space-100)}
.reply textarea{max-width:52rem;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);border-color:var(--oa-color-surface-newsprint);font:500 1rem/1.55 var(--mono)}
.reply-row{display:flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-200);margin-top:var(--oa-space-200)}
.reply button{font:var(--oa-type-ui);min-height:var(--oa-size-target-touch);padding:0 var(--oa-space-300);border:0;border-radius:0;cursor:pointer;
  background:var(--oa-color-action-primary-fill-on-prussian);color:var(--oa-color-action-primary-label-on-prussian)}
.reply button:hover{background:var(--oa-color-action-primary-fill-hover-on-prussian)}
#copy-status{font:var(--oa-type-body-small);color:var(--oa-color-text-primary-on-prussian)}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media print{.toc,.ans,.reply,.hint{display:none!important}.frame{overflow:visible;border:0}.chg-text{position:static!important}}
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
  // Answers: each card's marks join the reply. Saved in this browser only, keyed to this version of the questions (D2-316).
  var out = document.getElementById('reply-text');
  if (!out) return;
  var KEY = 'oa-apply-pass-board-answers:' + (document.querySelector('.board') || document.body).getAttribute('data-questions');
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
        var r = c.querySelector('input[type=radio][value="' + s.opt + '"]');
        part = s.opt === c.getAttribute('data-rec') ? 'as recommended (' + s.opt + ').' : '(' + s.opt + ') ' + (r ? r.getAttribute('data-short') : '') + '.';
      }
      if (s.named) part = (part ? part + ' ' : '') + 'Approved by name.';
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
    var k = c.querySelector('input[type=checkbox][data-named]');
    if (k) { if (s.named) k.checked = true; k.addEventListener('change', function () { store[id] = store[id] || {}; store[id].named = k.checked; save(); compose(); }); }
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

PREFIX = ''


def build_page(C, S, facts, tokens_css, prefix, reused):
    global PREFIX
    PREFIX = prefix
    views_by_key = {v['key']: v for v in facts['views']}
    plates = {p['key']: p for p in facts['plates']}
    built = datetime.datetime.now(datetime.timezone.utc)
    qs = C['decisions']['cards'] + C['stage_b']['questions']
    qkey = hashlib.sha1(json.dumps([q['question'] for q in qs] + [q['options'] for q in qs], sort_keys=True).encode()).hexdigest()[:12]
    toc = [('scores', '01', 'Scores'), ('changes', '02', 'What changed'), ('review', '03', 'What the review found'),
           ('decisions', '04', 'Decisions for you'), ('stage-b', '05', 'Stage B'), ('reply', '06', 'Your reply')]
    nav = ''.join(f'<li><a href="#{a}"><span class="n">{n}</span> {t}</a></li>' for a, n, t in toc)
    pg = C['pages']
    pages = ''.join(f'<p>{md(x)}</p>' for x in pg)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{tokens_css}
{CSS}</style></head>
<body><main class="board" data-view-root="overview" data-questions="{qkey}">
<header class="cover">
<p class="mast"><b>Oath &amp; Action</b><span class="label">Brand Guide, Edition 06 · Apply pass board</span></p>
<p class="label" style="margin-top:var(--oa-space-800)">For Dustin Cathcart · {words_date(built)}</p>
<h1>{md(C["title"], links=False)}</h1>
<div class="cover-grid"><div><p class="intro">{md(C["deck"])}</p><div class="pages">{pages}</div></div>
<div class="ask"><h2>What we ask of you</h2><ol>{"".join(f"<li>{md(x)}</li>" for x in C["ask"])}</ol>
<p class="caption" style="margin:0 0 var(--oa-space-050)">A reply can be this short:</p><p class="q">{esc(C["sample_reply"])}</p></div></div>
<nav class="toc" aria-label="On this board"><ol>{nav}</ol></nav>
</header>
{scores_section(C, S)}
{changes_section(C, views_by_key)}
{review_section(C)}
{decisions_section(C, plates)}
{stage_b_section(C, plates)}
{reply_section(C, C["sample_reply"], len(qs))}
<p class="foot caption">Built {words_date(built)} at {words_time(built)} UTC by <code>work/build/scripts/phase-2/apply_pass_board_build.py</code>, from the board’s content file, the creative director’s scores and both copies of the chapters page.{" These captures came from an earlier run." if reused else ""}</p>
</main>
<script>{JS}</script></body></html>'''
    return page


def main():
    global URL, ANCHORS, N_Q
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    for k in ('content', 'scores', 'before', 'after', 'out', 'captures', 'publish'):
        ap.add_argument(f'--{k}', type=pathlib.Path, default=DEF[k])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--no-capture', action='store_true')
    a = ap.parse_args()
    need(a.before is not None, '--before: the chapters page at commit 3130c5b, saved outside the repository (see the usage)')
    for k in ('content', 'scores', 'before', 'after'):
        need(getattr(a, k).exists(), f'{k} file not found: {getattr(a, k)}')
    C = json.loads(a.content.read_text())
    S = json.loads(a.scores.read_text())
    check_content(C)
    check_scores(S)
    URL = C['url'].rstrip('/')
    N_Q = len(C['decisions']['cards']) + len(C['stage_b']['questions'])
    views = card_views(C)
    plates = plate_jobs(C)
    cmp = compare_job(C)
    facts, reused = run_capture({'before': a.before, 'after': a.after}, a.captures, views, plates, cmp, a.no_capture)
    ANCHORS = facts['anchors']
    got = {v['key'] for v in facts['views']}
    for v in views:
        need(v['key'] in got, f'no capture for view {v["key"]}')
    for g in C['changes']['groups']:
        for c in g['cards']:
            for w in c.get('where', []):
                need(w in ANCHORS, f'card {c["id"]}: "where" anchor #{w} is not on the after page')
    # the designer's own renders, copied beside the captures, with their true size read from the file (2x renders)
    for q in C['decisions']['cards']:
        for p in q.get('plates', []):
            if p.get('copy'):
                src = BOARD_DIR / p['copy']
                need(src.exists(), f'{q["id"]}: plate file {p["copy"]} not found')
                p['file'] = f'{STEM}{q["id"]}-{p["key"]}.png'
                if not a.no_capture or not (a.captures / p['file']).exists():
                    shutil.copy2(src, a.captures / p['file'])
                w, h = png_size(src)
                p['w'], p['h'] = round(w / 2), round(h / 2)
            elif p['key'] not in {x['key'] for x in facts['plates']}:
                raise BoardError(f'{q["id"]}: no capture for plate {p["key"]}')
    for p in facts['plates']:
        if p.get('fonts') is not None and not any(f.startswith('Inter ') for f in p['fonts']):
            warn(f'plate {p["key"]}: Inter did not load in its source page, so the plate may set a stand-in face')
    tokens_css = TOKENS.read_text()
    rel = os.path.relpath(a.captures, a.out.parent).replace(os.sep, '/') + '/'
    page = build_page(C, S, facts, tokens_css, rel, reused)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)))
    need('—' not in text, 'em dash on the board')
    if '–' in text:
        warn('an en dash on the board')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text, flags=re.I)})
    if flagged:
        warn('flagged words on the board: ' + ', '.join(flagged))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    # every image the board references, and the page's size with them
    refs = sorted(set(re.findall(r'src="' + re.escape(rel) + r'([^"]+)"', page)))
    for r in refs:
        need((a.captures / r).exists(), f'the board references {r}, which is not in {a.captures}')
    stale = [p.name for p in a.captures.glob(f'{STEM}*') if p.suffix in ('.jpg', '.png') and p.name not in refs]
    for s in stale:
        warn(f'unused capture {s}')
    img_bytes = sum((a.captures / r).stat().st_size for r in refs)
    total = len(page.encode()) + img_bytes
    if total > 15_000_000:
        warn(f'the board and its images come to {total / 1e6:.1f} MB, close to the 16 MB limit')
    need(total < LIMIT, f'the board and its images come to {total / 1e6:.1f} MB, over 16 MB')

    # the publish copy: the page without its document skeleton, images beside it under captures/ (D2-317)
    pub = build_page(C, S, facts, tokens_css, 'captures/', reused)
    head, body = re.split(r'</head>\s*<body>', pub, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace(f'<title>{TITLE}</title>\n', '')
    body = re.sub(r'</body>\s*</html>\s*$', '', body)
    setup = '<script>document.documentElement.lang="en";</script>'
    a.publish.mkdir(parents=True, exist_ok=True)
    pdir = a.publish / 'captures'
    if pdir.exists():
        shutil.rmtree(pdir)
    pdir.mkdir(parents=True)
    files = {}
    for r in refs:
        shutil.copy2(a.captures / r, pdir / r)
        files[f'captures/{r}'] = str(pdir / r)
    pub_html = a.publish / a.out.name
    pub_html.write_text(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + setup + body)
    (a.publish / 'files.json').write_text(json.dumps(files, indent=1))
    n_jpg = sum(1 for r in refs if r.endswith('.jpg'))
    print(f'wrote {a.out} ({len(page.encode()) / 1e3:.0f} kB) with {len(refs)} images ({n_jpg} captures, {len(refs) - n_jpg} plates, '
          f'{img_bytes / 1e6:.2f} MB): {total / 1e6:.2f} MB in all')
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
