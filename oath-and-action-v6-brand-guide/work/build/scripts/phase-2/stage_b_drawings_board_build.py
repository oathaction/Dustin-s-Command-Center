"""Build the stage B drawings board (November 9, 2026): every new or redrawn drawing at true size beside the drawing it
replaces, with the creative director's scores and pick, for Dustin's approval by name (DR-139, DR-146).

Usage:
    python3 -I work/build/scripts/phase-2/stage_b_drawings_board_build.py [--strict] [--reuse-checks]
        [--out PATH] [--publish DIR] [--scratch DIR]

Reads, on every run (nothing about the options is written into this script):
    work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Content.json   the board's own words
    work/boards/phase-2/stage-b/drawings/20261109_CD-Scores.json                         scores, picks, readings
    work/build/assets/civic-line-redraws/*Manifest.json, civic-line-new-topics/*Manifest.json,
    pillar-pixel-fit/*Manifest.json, utility-icons/*Manifest.json                          the options and their files
    work/build/assets/civic-line/20261029_Civic-Line-Inventory.json                        today's masters
    the three makers' notes in work/handoffs/phase-2/ (tables of readings; the fix round's reasons)
    the makers' plate pages in work/boards/phase-2/stage-b/drawings/<role>/ (the Civic Line plate's neighbours,
    the identity plate's lines of text) and work/boards/phase-2/stage-b/drawings/identity/20261109_Identity-Figures.json
Runs, on today's files (the figures on the board are this run's, not copied from the notes):
    work/build/scripts/phase-2/icon_likeness_check.js     every option against the 122 masters and each other
    work/build/scripts/phase-2/icon_pixel_fit_check.js    the utility masters and the pillar fits at their own sizes
Writes:
    work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html          the board (files by relative path)
    work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Figures.json  every figure the board prints
    <scratch>/check-copy/ the board with absolute file links, for dataviz_check.js with captures in the scratchpad
    <publish>/20261109_Stage-B-Drawings-Board.html, <publish>/img/ and <publish>/files.json, the publish copy

Drawings show at true size: Civic Line files as images of their own SVG (their ids would repeat inline, D2-617), the
utility glyphs, end marks and lockmarks inline so they draw in currentColor. A small script moves each drawing by under
one pixel onto whole CSS pixels (D2-565). Enlargements carry their magnification. --strict exits 1 on any warning.
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

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261109'
BOARD_DIR = ROOT / 'work/boards/phase-2/stage-b/drawings'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad')
ASSETS = ROOT / 'work/build/assets'
HANDOFFS = ROOT / 'work/handoffs/phase-2'
SCRIPTS = ROOT / 'work/build/scripts/phase-2'
DEF = {
    'content': BOARD_DIR / f'{DATE}_Stage-B-Drawings-Board-Content.json',
    'scores': BOARD_DIR / f'{DATE}_CD-Scores.json',
    'out': BOARD_DIR / f'{DATE}_Stage-B-Drawings-Board.html',
    'publish': SCRATCH / 'publish-drawings-board',
    'scratch': SCRATCH / 'drawings-board',
}
SRC = {
    'redraws': ASSETS / 'civic-line-redraws',
    'topics': ASSETS / 'civic-line-new-topics',
    'pillars': ASSETS / 'pillar-pixel-fit',
    'utility': ASSETS / 'utility-icons',
    'identity': ASSETS / 'identity',
    'inventory': ASSETS / 'civic-line/20261029_Civic-Line-Inventory.json',
    'cl_plate': BOARD_DIR / 'civic-line/20261109_Civic-Line-Drawings-Plates.html',
    'id_plate': BOARD_DIR / 'identity/20261109_Identity-Plates.html',
    'id_figs': BOARD_DIR / 'identity/20261109_Identity-Figures.json',
    'cl_notes': HANDOFFS / f'{DATE}_Stage-B-Civic-Line-Icons-Notes.md',
    'ut_notes': HANDOFFS / f'{DATE}_Stage-B-Utility-Icons-Notes.md',
    'id_notes': HANDOFFS / f'{DATE}_Stage-B-Identity-Notes.md',
    'audit': HANDOFFS / f'{DATE}_Stage-B-Accessibility-Audit.md',
    'screen2x': BOARD_DIR / 'civic-line/screen-2x',
}
TOKENS = ROOT / 'work/build/tokens/tokens.css'
LIKENESS_JS = SCRIPTS / 'icon_likeness_check.js'
PIXELFIT_JS = SCRIPTS / 'icon_pixel_fit_check.js'
TITLE = 'Stage B Drawings Board'
RUBRIC = [('craft', 'Craft'), ('clarity', 'Clarity'), ('brand_fidelity', 'Brand fidelity'), ('usefulness', 'Usefulness'),
          ('evidence_honesty', 'Evidence honesty'), ('accessibility', 'Accessibility')]
RUBRIC_SHORT = {'brand_fidelity': 'Brand', 'evidence_honesty': 'Evidence'}
# The card order the drawings brief and D2-621 set. Subjects name drawings; their options come from the manifests.
CIVIC = [
    ('congress', ['CL-025', 'CL-014', 'R-13', 'R-42']),
    ('redraw', ['CL-059']),
    ('redraw', ['R-48']),
    ('testify', ['Testify']),
    ('contact', ['Contact-An-Official']),
]
SCORE_IDS = {'Contact-An-Official': ['Contact', 'Contact-An-Official']}
# Sizes the drawings brief names. A topic symbol's floor is 48 px, so 24 px is a reference size (DR-136).
CL_SIZES = [128, 48, 24]
PILLAR_MASTER_SIZES = [96, 48, 24, 16]
LOCK_SIZES = [16, 24, 34, 40, 48]
UTILITY_LINE = {24: 2, 16: 1.5}           # the engineer's tokens (D2-564)
END_MAG = {'1x': 8, '2x': 4}              # the identity plate's enlargements (D2-550)
TAGLINE = 'A country that answers to its people.'
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat']
LIMIT = 16_000_000
WARN = []
OVERRIDES = []      # the editor's exact-text replacements: [old, new, times used]
# keys whose strings are file paths or the identifiers the build matches on; an override never touches them
ID_KEYS = {'files', 'svg_red_black', 'svg_black', 'stem', 'folder', 'file', 'prussian', 'today', 'map', 'paths', 'exports',
           '24', '16', 'id', 'key', 'word', 'option', 'rank', 'sheet_black', 'sheet_red', 'slug'}


def ov(s):
    """The editor's overrides applied to one string taken from another owner's file."""
    if not isinstance(s, str) or not OVERRIDES:
        return s
    for o in OVERRIDES:
        if o[0] in s:
            o[2] += s.count(o[0])
            s = s.replace(o[0], o[1])
    return s


def ov_deep(obj, key=None):
    if isinstance(obj, str):
        return obj if key in ID_KEYS or re.fullmatch(r'[\w./-]+\.(svg|png|json|html|md|csv)', obj) else ov(obj)
    if isinstance(obj, dict):
        return {k: (v if k in ID_KEYS and not isinstance(v, (dict, list)) else ov_deep(v, k)) if k not in ('files', 'exports', 'paths') else v
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [ov_deep(v, key) for v in obj]
    return obj


class BoardError(Exception):
    pass


def warn(msg):
    WARN.append(msg)
    print('warning', msg)


def need(cond, msg):
    if not cond:
        raise BoardError(msg)


def rel(p):
    return str(pathlib.Path(p).resolve().relative_to(ROOT))


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


def md(s):
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f'\x00{len(codes) - 1}\x00'
    t = re.sub(r'`([^`]+)`', keep, str(s))
    t = html.escape(copy(t), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w#-])card (\d{1,2})\b', lambda m: f'<a href="#card-{m.group(1)}">card {m.group(1)}</a>' if int(m.group(1)) <= N_CARDS else m.group(0), t)
    return re.sub(r'\x00(\d+)\x00', lambda m: f'<code>{html.escape(codes[int(m.group(1))])}</code>', t)


N_CARDS = 0
FILL = {}


def fill(s):
    """Content words with {n_cards} and the like filled in by the build."""
    try:
        return str(s).format_map(FILL)
    except (KeyError, IndexError, ValueError) as e:
        raise BoardError(f'content text names an unknown value {e}: {s[:80]}')


def paras(x, cls=''):
    items = x if isinstance(x, list) else [x] if x else []
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<p{c}>{md(fill(p))}</p>' for p in items)


def words_date(d):
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def words_time(d):
    h = d.hour % 12 or 12
    return f'{h}:{d.minute:02d} {"a.m." if d.hour < 12 else "p.m."}'


def num_words(n):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][n] if 0 <= n < 10 else f'{n:,}'


def join_words(items):
    items = list(items)
    if len(items) < 3:
        return ' and '.join(items)
    return ', '.join(items[:-1]) + ' and ' + items[-1]


def png_size(p):
    with open(p, 'rb') as f:
        d = f.read(24)
    return struct.unpack('>II', d[16:24])


# ------------------------------------------------------------------------------------------------ inputs
def load_json(p, what):
    need(pathlib.Path(p).exists(), f'{what} not found: {rel(p) if str(p).startswith(str(ROOT)) else p}')
    try:
        return json.loads(pathlib.Path(p).read_text())
    except json.JSONDecodeError as e:
        raise BoardError(f'{what} does not parse ({e}); a maker may be writing it, so rerun once it is saved')


def manifest(folder):
    found = sorted(folder.glob('*Manifest*.json'))
    need(found, f'no manifest in {rel(folder)}')
    if len(found) > 1:
        warn(f'{rel(folder)} holds {len(found)} manifests; reading the newest, {found[-1].name}')
    return load_json(found[-1], f'manifest {found[-1].name}'), found[-1]


def dropped(o):
    """An option the maker took off its card in the fix round, if the manifest marks it so."""
    st = str(o.get('status') or o.get('state') or '').lower()
    return bool(o.get('dropped') or o.get('withdrawn') or o.get('moved_to_family') or st in ('dropped', 'withdrawn', 'moved', 'replaced', 'family'))


def md_tables(text):
    """Every Markdown table in a notes file as a list of rows {header: cell}, in file order, with its section heading."""
    out, sec = [], ''
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('#'):
            sec = ln.lstrip('#').strip()
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|\s*$', lines[i + 1]):
            head = [h.strip() for h in ln.strip().strip('|').split('|')]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(dict(zip(head, cells)) | {'_section': sec})
                i += 1
            out.append({'head': head, 'rows': rows, 'section': sec})
            continue
        i += 1
    return out


def section_text(text, pattern):
    """The text of the notes' sections whose heading matches pattern (a fix round section, say), headings included."""
    out, keep, level = [], False, 0
    for ln in text.split('\n'):
        m = re.match(r'^(#+)\s+(.*)', ln)
        if m:
            if keep and len(m.group(1)) <= level:
                keep = False
            if re.search(pattern, m.group(2), flags=re.I):
                keep, level = True, len(m.group(1))
        if keep:
            out.append(ln)
    return '\n'.join(out)


def strip_md(s):
    s = re.sub(r'`([^`]*)`', r'\1', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    return s.strip()


def display_id(i):
    if re.match(r'(CL|R)-\d', i):
        return i
    t = i.replace('-', ' ')
    return t[:1] + t[1:].lower()


def letter_of(s):
    m = re.match(r'^\s*(?:Option\s+|Set\s+|Fit\s+)?([A-Z])\b', str(s))
    return m.group(1) if m else None


# ------------------------------------------------------------------------------------------------ the checks
def run_checks(files_like, pf_jobs, scratch, reuse):
    """The engineer's look-alike check on every option, and the pixel-fit check on the drawings meant for 16 and 24 px."""
    cdir = scratch / 'checks'
    cdir.mkdir(parents=True, exist_ok=True)
    lk_path = cdir / 'likeness.json'
    pf_paths = []
    if reuse:
        need(lk_path.exists(), '--reuse-checks: no earlier check results in the scratchpad')
        warn('check results reused from an earlier run (--reuse-checks)')
    else:
        r = subprocess.run(['node', str(LIKENESS_JS), *[str(f) for f in files_like], '--json', str(lk_path), '--quiet'],
                           cwd=ROOT, capture_output=True, text=True, timeout=900)
        need(r.returncode in (0, 1) and lk_path.exists(), f'the look-alike check failed: {(r.stderr or r.stdout)[-600:]}')
    lk = load_json(lk_path, 'look-alike results')
    pf = {}
    for k, (size, weight, files) in enumerate(pf_jobs):
        p = cdir / f'pixel-fit-{size}px-{str(weight).replace(".", "-")}px-{k}.json'
        pf_paths.append(p)
        if not reuse:
            if p.exists():
                p.unlink()
            r = subprocess.run(['node', str(PIXELFIT_JS), '--size', str(size), '--weight', str(weight), '--json', str(p),
                                *[str(f) for f in files]], cwd=ROOT, capture_output=True, text=True, timeout=1200)
            need(r.returncode in (0, 1) and p.exists(), f'the pixel-fit check failed at {size} px: {(r.stderr or r.stdout)[-600:]}')
        for res in load_json(p, 'pixel-fit results')['results']:
            pf[(pathlib.Path(res['file']).name, size)] = res
    return lk, pf, lk_path, pf_paths


class Like:
    """Look-alike figures for one drawing file, read from the check's JSON."""

    def __init__(self, lk):
        self.flag = lk['thresholds']['flag']['likeness']
        self.watch = lk['thresholds']['watch']['likeness']
        self.closest = {c['a']: c for c in lk.get('closest', [])}
        self.own = {c['a']: c for c in lk.get('own', [])}
        self.options = lk.get('options', [])
        self.new_pairs = [p for p in lk.get('flagged', []) + lk.get('watch', []) if p.get('against') == 'new']
        self.run = lk.get('run')

    def status(self, v):
        return 'flag' if v >= self.flag else 'watch' if v >= self.watch else ''

    def of(self, name, sibling_names, label_of):
        c = self.closest.get(name)
        out = {'file': name}
        if c:
            out['closest'] = {'name': c['b'], 'likeness': c['likeness'], 'percentile': c['percentile'], 'status': self.status(c['likeness'])}
        o = self.own.get(name)
        if o:
            out['own'] = {'name': o['b'], 'likeness': o['likeness']}
        best = None
        for p in self.options:
            if name in (p['a'], p['b']):
                other = p['b'] if p['a'] == name else p['a']
                if other in sibling_names and (best is None or p['likeness'] > best[1]):
                    best = (other, p['likeness'])
        if best:
            out['sibling'] = {'option': label_of(best[0]), 'likeness': best[1], 'status': self.status(best[1])}
        tw = None
        for p in self.new_pairs:
            if name in (p['a'], p['b']):
                other = p['b'] if p['a'] == name else p['a']
                if other in sibling_names:
                    continue
                if tw is None or p['likeness'] > tw[1]:
                    tw = (other, p['likeness'])
        if tw and self.status(tw[1]) == 'flag':
            out['twin'] = {'name': label_of(tw[0]) or tw[0], 'likeness': tw[1], 'status': 'flag'}
        return out


PF_WORDS = {'no ink': 'it draws no ink', 'width': 'a stroke is under one device pixel', 'soft': 'most of its pixels are soft',
            'straight': 'a straight stroke sits off the pixel grid', 'gap': 'a gap is under one device pixel',
            'counters': 'an enclosed space fills in', 'weight': 'its main width differs from the set\'s line'}


def pf_words(size, r):
    """The pixel-fit result at one size in words: 'passes at 24 px' or what fails, and at which densities."""
    if r is None:
        return f'not run at {size} px'
    if r['pass']:
        return f'passes at {size} px'
    by = {}
    for item in r['fails']:
        sc, _, codes = item.partition(': ')
        for c in codes.split('; '):
            by.setdefault(c, []).append(sc)
    if set(by) == {'weight'}:
        return f'passes every test at {size} px but line weight, at {join_words(by["weight"])}'
    parts = [f'{PF_WORDS.get(c, c)} at {join_words(scs)}' for c, scs in by.items()]
    return f'fails at {size} px: ' + '; '.join(parts)


def pf_sentence(r24, r16):
    """The pixel-fit results at 24 and 16 px as one sentence when both pass, or one sentence for each size."""
    if r24 and r16 and r24['pass'] and r16['pass']:
        return 'Passes at 24 px and at 16 px.'
    out = []
    for size, r in ((24, r24), (16, r16)):
        t = pf_words(size, r)
        out.append(t[:1].upper() + t[1:] + '.')
    return ' '.join(out)


def pf_summary(pf, fname, size):
    r = pf.get((fname, size))
    if not r:
        return None
    fails = []
    for sc in ('1x', '2x'):
        s = r['scales'].get(sc, {})
        if not s.get('pass', False):
            fails.append(f'{sc}: ' + '; '.join(str(x) for x in s.get('fails', [])))
    st = r['scales'].get('1x', {}).get('straight', {})
    return {'pass': bool(r.get('pass')), 'fails': fails, 'straight': f'{st.get("fit", 0)} of {st.get("total", 0)}',
            'soft': round(100 * r['scales'].get('1x', {}).get('soft_edges', {}).get('share', 0))}


# ------------------------------------------------------------------------------------------------ the model
class Option:
    def __init__(self, letter, **kw):
        self.letter = letter
        self.__dict__.update(kw)


def score_card(S, ids, title_words=None):
    want = {i.lower() for i in ids}
    for c in S['cards']:
        if str(c.get('id', '')).lower() in want:
            return c
    if title_words:
        for c in S['cards']:
            t = str(c.get('title', '')).lower()
            if all(w in t for w in title_words):
                return c
    return None


def cd_naming(sc, letter):
    for n in (sc or {}).get('naming_test', []) or []:
        if str(n.get('option')) == letter or letter_of(n.get('option')) == letter:
            return n
    return None


def cd_option(sc, letter):
    for o in (sc or {}).get('options', []) or []:
        if str(o.get('option')) == letter or letter_of(o.get('option')) == letter:
            return o
    return None


def accessibility_checks(text):
    """The accessibility lead's fix round check (the audit's "Fix round check" section): one bullet per drawing, its
    words and the option the lead recommends, keyed by the drawing's name."""
    out = {}
    sec = section_text(text, r'fix round check')
    for m in re.finditer(r'^- \*\*(.+?)\*\*\s*(.*)$', sec, flags=re.M):
        head, body = m.group(1).strip(), m.group(2).strip()
        nm = re.match(r'([A-Za-z][A-Za-z ]*?) ([A-C])\b', head)
        if not nm:
            continue
        txt = strip_md(f'{head} {body}')
        pk = re.search(r"\b([A-C])(?:['’]s [^.,]*?)?,? (?:remains my recommendation|stays my pick)", txt)
        out[nm.group(1).strip().lower()] = {'option': nm.group(2), 'text': txt, 'pick': pk.group(1) if pk else None}
    return out


def build_model(C, S, scratch, reuse):
    inv = ov_deep(load_json(SRC['inventory'], 'the Civic Line inventory'))
    masters = {r['id']: r for r in inv['icons']}
    m_red = ov_deep(manifest(SRC['redraws'])[0])
    m_top = ov_deep(manifest(SRC['topics'])[0])
    m_pil = ov_deep(manifest(SRC['pillars'])[0])
    m_ut, ut_path = manifest(SRC['utility'])
    m_ut = ov_deep(m_ut)
    figs = load_json(SRC['id_figs'], 'the identity figures')
    notes = {k: ov(SRC[k].read_text()) if SRC[k].exists() else '' for k in ('cl_notes', 'ut_notes', 'id_notes')}
    a11y = accessibility_checks(ov(SRC['audit'].read_text()) if SRC['audit'].exists() else '')
    for k, t in notes.items():
        if not t:
            warn(f'{k}: notes file missing')

    def master_svg(mid, ed='red-black'):
        r = masters[mid]
        name = r['exports']['svg_red_black' if ed == 'red-black' else 'svg_black']
        return ASSETS / 'civic-line' / ed / name

    # ---- Civic Line options, by drawing
    cl_opts = {}
    for o in m_red['options'] + m_top['options']:
        if dropped(o):
            continue
        cl_opts.setdefault(o['id'], []).append(o)
    for v in cl_opts.values():
        v.sort(key=lambda o: o['option'])
    used = {i for _, ids in CIVIC for i in ids}
    for i in cl_opts:
        if i not in used:
            warn(f'the Civic Line manifests hold drawing {i}, which no card shows')
    for i in used:
        need(i in cl_opts, f'no options for {i} in the Civic Line manifests')

    # ---- utility actions, grouped by the audit's rank (Play and Pause share one, D2-557)
    ut_entries = m_ut if isinstance(m_ut, list) else m_ut.get('cards') or m_ut.get('drawings') or m_ut.get('actions') or []
    need(isinstance(ut_entries, list) and ut_entries, f'{ut_path.name}: no drawings found')
    # the family card's ringed set (D2-621) and the status marks' solid partners, when the manifest carries them
    ut_family = None if isinstance(m_ut, list) else (m_ut.get('family_ringed') or m_ut.get('family') or m_ut.get('enclosure'))
    ut_partners = {} if isinstance(m_ut, list) else (m_ut.get('solid_partners') or {})
    actions = list(ut_entries)

    def rank_key(e):
        m = re.match(r'\d+', str(e.get('rank', '99')))
        return int(m.group(0)) if m else 99
    # one card per drawing, except drawings the audit makes one button (Play "one button with Pause", D2-557)
    groups, placed = {}, {}
    order = sorted(actions, key=rank_key)
    for k, e in enumerate(order):
        m = re.search(r'one button with ([\w-]+)', str(e.get('label', '')), flags=re.I)
        mate = next((x for x in order if m and str(x.get('word', '')).lower() == m.group(1).lower()), None)
        if mate is not None and mate['key'] in placed:
            groups[placed[mate['key']]].append(e)
            placed[e['key']] = placed[mate['key']]
        else:
            groups[k] = [e]
            placed[e['key']] = k

    # ---- files for the checks
    like_files, sib_sets, label_of = [], {}, {}

    def cl_black(o):
        p = ROOT / o['svg_black'] if o.get('svg_black') else SRC['redraws'] / 'svg' / f'{o["stem"]}-Black.svg'
        return p
    for i, opts in cl_opts.items():
        names = set()
        for o in opts:
            p = cl_black(o)
            if not p.exists():
                warn(f'{i} option {o["option"]}: {rel(p)} is missing')
                continue
            like_files.append(p)
            names.add(p.name)
            label_of[p.name] = f'{display_id(i)} {o["option"]}'
        sib_sets[i] = names
    for e in actions:
        names = set()
        for o in e['options']:
            if dropped(o):
                continue
            p = SRC['utility'] / o['files']['24']
            if p.exists():
                like_files.append(p)
                names.add(p.name)
                label_of[p.name] = f'{e["label"]} {o["option"]}'
            else:
                warn(f'utility {e["key"]} option {o["option"]}: {o["files"]["24"]} is missing')
        sib_sets[e['key']] = names
    fits = m_pil['fits']
    for f in fits:
        p = ROOT / f['svg_black']
        if p.exists():
            like_files.append(p)
            label_of[p.name] = f'{f["id"]} {f["size_px"]} px Fit {f["fit"]}'
    pf_jobs = []
    for size in (24, 16):
        files = []
        for e in actions:
            for o in e['options']:
                p = SRC['utility'] / o['files'][str(size)]
                if p.exists() and not dropped(o):
                    files.append(p)
        if files:
            pf_jobs.append((size, UTILITY_LINE[size], files))
    by_fit = {}
    for f in fits:
        for ed in ('svg_black', 'svg_red_black'):
            p = ROOT / f[ed]
            if p.exists():
                by_fit.setdefault((f['size_px'], f['line_px']), []).append(p)
    for (size, line), files in sorted(by_fit.items()):
        pf_jobs.append((size, line, files))
    lk_raw, pf, lk_path, pf_paths = run_checks(like_files, pf_jobs, scratch, reuse)
    LK = Like(lk_raw)

    # ---- the makers' readings from their notes, later tables overriding earlier ones (a fix round's table)
    maker_read = {}
    for t in md_tables(notes['cl_notes']):
        hn = next((h for h in t['head'] if h.lower().startswith('naming')), None)
        if not hn or 'Opt' not in t['head']:
            continue
        for r in t['rows']:
            maker_read[(r.get('Card', '').lower(), letter_of(r['Opt']))] = strip_md(r[hn])
    for t in md_tables(notes['ut_notes']):
        hn = next((h for h in t['head'] if h.lower().startswith('naming')), None)
        if not hn or 'Option' not in t['head']:
            continue
        for r in t['rows']:
            maker_read[(r.get('Drawing', '').lower(), letter_of(r['Option']))] = strip_md(r[hn])

    # ---- the Civic Line plate's neighbours: the settled drawings each card sets beside its options
    neighbors = {}
    if SRC['cl_plate'].exists():
        plate = SRC['cl_plate'].read_text()
        for m in re.finditer(r'<section class="card" id="card-\d+"><h3>(.*?)</h3>(.*?)</section>', plate, flags=re.S):
            title = re.sub(r'<[^>]+>', ' ', m.group(1))
            ids = re.findall(r'civic-line/red-black/20261029_Oath-And-Action-Civic-Line-((?:CL|R)-\d+)-', m.group(2))
            for i in list(cl_opts):
                key = i.replace('-An-', ' an ').replace('-', ' ').lower() if not re.match(r'(CL|R)-\d', i) else i.lower()
                if re.search(rf'\b{re.escape(key)}\b', title.lower()):
                    neighbors[i] = [x for x in dict.fromkeys(ids) if x != i]
    else:
        warn('the Civic Line plate page is missing; no neighbours shown')

    def cl_option_model(i, o, sc, siblings):
        bl = cl_black(o)
        n = cd_naming(sc, o['option'])
        mk = maker_read.get((i.lower(), o['option'])) or maker_read.get((i.replace('-', ' ').lower(), o['option'])) \
            or maker_read.get(('contact an official' if i.startswith('Contact') else i.lower(), o['option']))
        ch = cd_option(sc, o['option'])
        return Option(o['option'], change=o.get('change', ''), within=o.get('within_dr135'), stem=o['stem'],
                      red=ROOT / o['svg_red_black'], black=bl, cd=n, maker=mk, choice=ch,
                      like=LK.of(bl.name, siblings, lambda x: label_of.get(x, x).split(' ')[-1] if x in siblings else label_of.get(x)))

    # ---- cards
    cards = []
    for kind, ids in CIVIC:
        subs = []
        for i in ids:
            sc = score_card(S, SCORE_IDS.get(i, [i]))
            if not sc:
                warn(f'no scores for {i} in the scores file')
            subs.append({'id': i, 'name': masters[i]['label'] if i in masters else None, 'scores': sc,
                         'options': [cl_option_model(i, o, sc, sib_sets[i]) for o in cl_opts[i]],
                         'master': i if i in masters else None, 'neighbors': neighbors.get(i, [])})
        cards.append({'kind': kind, 'group': 'civic', 'subjects': subs})

    # the family card (D2-621), before the utility actions
    fam_sc = score_card(S, ['U-family', 'U-enclosure', 'Utility-family', 'Family', 'Enclosure'], ['family'])
    if not fam_sc:
        fam_sc = score_card(S, [], ['enclosure'])
    cards.append({'kind': 'utility-family', 'group': 'utility', 'scores': fam_sc, 'family': ut_family, 'subjects': []})
    for rk in sorted(groups):
        subs = []
        for e in groups[rk]:
            sc = score_card(S, ['U-' + str(e['word']).lower(), 'U-' + e['key']])
            if not sc:
                warn(f'no scores for utility {e["key"]}')
            opts = []
            for o in e['options']:
                if dropped(o):
                    continue
                f24 = SRC['utility'] / o['files']['24']
                f16 = SRC['utility'] / o['files']['16']
                mk = maker_read.get((str(e['word']).replace('-', ' ').lower(), o['option']))
                opts.append(Option(o['option'], shows=o.get('shows', ''), f24=f24, f16=f16, cd=cd_naming(sc, o['option']),
                                   maker=mk, choice=cd_option(sc, o['option']),
                                   reason=o.get('reason') or o.get('why') or '',
                                   like=LK.of(f24.name, sib_sets[e['key']], lambda x, k=e['key']: (label_of.get(x, x).split(' ')[-1] if x in sib_sets[k] else label_of.get(x))),
                                   pf24=pf_summary(pf, f24.name, 24), pf16=pf_summary(pf, f16.name, 16)))
            subs.append({'id': e['key'], 'word': e['word'], 'label': e['label'], 'asked': e.get('asked', ''), 'scores': sc,
                         'options': opts, 'entry': e,
                         'title': (sc or {}).get('title') or e['label']})
        reasons = list(dict.fromkeys(s['entry'].get('fewer_reason') for s in subs if s['entry'].get('fewer_reason')))
        cards.append({'kind': 'utility', 'group': 'utility', 'subjects': subs, 'fewer_reason': ' '.join(reasons) or None,
                      'partners': ut_partners})

    # pillar fits
    p_sc = score_card(S, ['Pillar-fits'], ['pillar'])
    pillars = {}
    for f in fits:
        pillars.setdefault(f['id'], {'id': f['id'], 'name': f['name'], 'fits': []})['fits'].append(f)
    for p in pillars.values():
        for f in p['fits']:
            bl = ROOT / f['svg_black']
            f['like'] = LK.of(bl.name, set(), lambda x: label_of.get(x, x))
            f['pf_black'] = pf_summary(pf, bl.name, f['size_px'])
            f['pf_red'] = pf_summary(pf, (ROOT / f['svg_red_black']).name, f['size_px'])
        p['fits'].sort(key=lambda f: (-f['size_px'], f['fit']))
    cards.append({'kind': 'pillars', 'group': 'pillars', 'scores': p_sc, 'pillars': list(pillars.values()),
                  'master_svg': master_svg})

    # identity
    for kind, sid, words in (('end-mark', ['End-mark'], ['end mark']), ('lockmark', ['Lockmark-masters'], ['lockmark']),
                             ('l6', ['L6-centered'], ['l6'])):
        sc = score_card(S, sid, words)
        if not sc:
            warn(f'no scores for {kind}')
        cards.append({'kind': kind, 'group': 'identity', 'scores': sc, 'figs': figs})

    model = {'cards': cards, 'like': LK, 'masters': masters, 'master_svg': master_svg, 'notes': notes, 'a11y': a11y, 'S': S,
             'checks': {'likeness': lk_path, 'pixel_fit': pf_paths, 'likeness_run': LK.run}}
    return model


# ------------------------------------------------------------------------------------------------ assets
ASSET_REFS = {}     # repo path -> True, every file the board shows
INLINE_N = [0]


def src(p):
    p = pathlib.Path(p).resolve()
    need(p.exists(), f'the board shows {p}, which does not exist')
    k = rel(p)
    ASSET_REFS[k] = True
    return f'@@A:{k}@@'


def inline_svg(p, w, h, cls='', style='', label=None):
    """An SVG file drawn inline at w by h px, so it takes currentColor from its stage. Ids are removed (none expected)."""
    t = pathlib.Path(p).read_text()
    t = re.sub(r'<\?xml[^>]*>|<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<title>.*?</title>|<desc>.*?</desc>', '', t, flags=re.S)
    ids = re.findall(r'\sid="([^"]+)"', t)
    if ids:
        # each inline copy gets its own ids, so a mask or gradient drawn many times on the page never collides
        INLINE_N[0] += 1
        for i in ids:
            j = f'{i}-i{INLINE_N[0]}'
            t = t.replace(f'id="{i}"', f'id="{j}"').replace(f'url(#{i})', f'url(#{j})').replace(f'href="#{i}"', f'href="#{j}"')
    m = re.search(r'<svg\b([^>]*)>', t)
    need(m, f'{p}: no <svg> element')
    a = m.group(1)
    a = re.sub(r'\s(width|height|class|style|aria-hidden|focusable|role)="[^"]*"', '', a)
    lab = f' role="img" aria-label="{attr(label)}"' if label else ' aria-hidden="true"'
    head = f'<svg{a} width="{w}" height="{h}" class="snap {cls}" focusable="false"{lab}{f" style={chr(34)}{style}{chr(34)}" if style else ""}>'
    return (t[:m.start()] + head + t[m.end():]).strip()


def img(p, w, h, alt, cls='', eager=False, srcset2x=None):
    ss = f' srcset="{src(p)} 1x, {src(srcset2x)} 2x"' if srcset2x else ''
    return (f'<img class="snap {cls}" src="{src(p)}"{ss} width="{w}" height="{h}" alt="{attr(copy(alt))}" '
            f'loading="eager" decoding="async">')


# ------------------------------------------------------------------------------------------------ page parts
def nx(h):
    """Keep "1x" and "2x" lowercase where a label sets its words in capitals."""
    return re.sub(r'\b([123])x\b', r'<span class="nc">\1x</span>', h)


def chip(t, cls=''):
    return f'<span class="chip{" " + cls if cls else ""}">{nx(esc(t))}</span>'


def fmt_like(v):
    return f'{v:.3f}' if v < 1 else '1'


def like_status_word(s):
    return {'flag': 'flagged', 'watch': 'to watch'}.get(s, '')


def like_lines(lk, own_label='today’s drawing', show_own=True):
    """The look-alike figures for one option, as definition-list rows."""
    out = []
    c = lk.get('closest')
    if c:
        st = like_status_word(c['status'])
        out.append(('Closest settled drawing', f'{esc(c["name"])}, <span class="num">{fmt_like(c["likeness"])}</span>'
                    f'{" " + chip(st, "chip--" + c["status"]) if st else ""}'))
    o = lk.get('own')
    if o and show_own:
        out.append((f'Against {own_label}', f'<span class="num">{fmt_like(o["likeness"])}</span>'))
    s = lk.get('sibling')
    if s:
        st = like_status_word(s['status'])
        out.append(('Closest other option', f'{esc(s["option"])}, <span class="num">{fmt_like(s["likeness"])}</span>'
                    f'{" " + chip(st, "chip--" + s["status"]) if st else ""}'))
    t = lk.get('twin')
    if t:
        out.append(('Closest other new drawing', f'{esc(t["name"])}, <span class="num">{fmt_like(t["likeness"])}</span> {chip("flagged", "chip--flag")}'))
    return out


def naming_lines(o, size):
    out = []
    if o.cd:
        r = o.cd.get('creative_director_reading') or ''
        v = o.cd.get('creative_director_verdict') or ''
        out.append((f'Naming test at {size} px', f'“{esc(r.rstrip("."))}.” {esc(v)}.'))
        mv = o.cd.get('maker_verdict')
        if mv:
            out.append(('The maker’s verdict', f'{esc(mv)}.'))
    elif o.maker:
        out.append((f'Naming test at {size} px', f'“{esc(o.maker.rstrip("."))}.” The maker’s reading; the creative director has not read this option yet.'))
        warn(f'option {getattr(o, "stem", "") or o.letter}: no naming test from the creative director; the maker\'s reading is shown')
    else:
        out.append((f'Naming test at {size} px', 'Not read yet.'))
        warn(f'option {getattr(o, "stem", "") or o.letter}: no naming test from either reader')
    return out


def dl(rows, cls='figs'):
    return f'<dl class="{cls}">' + ''.join(f'<div><dt>{nx(esc(k))}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


def choice_note(o):
    """The creative director's answer to "Is each option a real choice?" for this option."""
    ch = o.choice
    if not ch or ch.get('real_choice') is None:
        return ''
    note = str(ch.get('note') or '').strip()
    if ch.get('real_choice'):
        note = re.sub(r'^Real[.,:;]?\s*', '', note)
        txt = 'Yes.' + (f' {note[:1].upper()}{note[1:]}' if note else '')
    else:
        txt = 'No.' + (f' {note}' if note else '')
    return f'<p class="cd-note"><span class="label">A real choice, says the creative director</span> {esc(txt)}</p>'


def sizes_row(p, sizes, alt, ref24=True):
    figs = ''
    for s in sizes:
        figs += f'<figure class="sz">{img(p, s, s, f"{alt} at {s} px")}<figcaption>{s}</figcaption></figure>'
    ref = '<p class="ref caption">24 px: reference size only</p>' if (ref24 and 24 in sizes) else ''
    return f'<div class="sizes">{figs}</div>{ref}'


def rec_letter(sc):
    if not sc:
        return None
    return letter_of((sc.get('recommended') or {}).get('option', ''))


def scores_block(subjects):
    """The creative director's six scores for each scored subject on a card, any score under 4 flagged (D2-499)."""
    rows, reasons, lows = '', '', []
    for name, sc in subjects:
        if not sc:
            warn(f'{name}: not scored in the scores file')
            rows += f'<tr><th scope="row">{esc(name)}</th><td colspan="6">Not scored yet</td></tr>'
            continue
        cells = ''
        for k, lab in RUBRIC:
            x = (sc.get('scores') or {}).get(k) or {}
            v = x.get('score')
            low = isinstance(v, int) and v < 4
            if low:
                lows.append(f'{name}, {lab.lower()} {v}')
            cells += (f'<td class="num{" low" if low else ""}"><span>{v if v is not None else "–"}</span>'
                      f'{"<span class=vh> (under 4)</span>" if low else ""}</td>')
        rows += f'<tr><th scope="row">{esc(name)}</th>{cells}</tr>'
        li = ''.join(f'<li><span class="rk">{esc(lab)} {((sc.get("scores") or {}).get(k) or {}).get("score", "")}</span> '
                     f'{esc(((sc.get("scores") or {}).get(k) or {}).get("reason", ""))}</li>' for k, lab in RUBRIC)
        reasons += f'<p class="rs-h">{esc(name)}</p><ul>{li}</ul>'
    head = ''.join(f'<th scope="col">{esc(RUBRIC_SHORT.get(k, lab))}</th>' for k, lab in RUBRIC)
    flag = (f'<p class="lowflag"><span class="chip chip--low">Under 4</span> {esc(join_words(lows))}. '
            'The guide ships at 4 on every criterion.</p>') if lows else ''
    return (f'<div class="scores"><p class="label">The creative director’s scores, 1 to 5</p>{flag}'
            f'<div class="tw" role="region" tabindex="0" aria-label="Scores"><table class="sc-t"><thead><tr><th scope="col">Drawing</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<details class="why-d"><summary>Every score with its reason</summary>{reasons}</details></div>'), lows


def open_items(subjects):
    items = []
    for name, sc in subjects:
        for m in (sc or {}).get('must_fix') or []:
            items.append((name, m.get('owner', ''), m.get('fix', '')))
    if not items:
        return ''
    li = ''.join(f'<li><b>{esc(n)}</b> ({esc(o.lower())}): {esc(f)}</li>' for n, o, f in items)
    return (f'<details class="open-d"><summary>{num_words(len(items)).capitalize()} item{"s" if len(items) != 1 else ""} the creative director '
            f'still lists as Must fix</summary><ul>{li}</ul></details>')


def frame(inner, name, wide=True):
    """A plate that keeps true size: on a narrow window it scrolls sideways inside a labeled frame."""
    return (f'<div class="frame" role="region" tabindex="0" aria-label="{attr(copy(name))}, true size">{inner}</div>'
            f'<p class="hint caption" hidden>Wider than this window. Scroll sideways inside the frame to see all of it at true size.</p>')


# ---- the answer controls: one group per choice; the card and the reply panel's line share one store
def answer_block(card):
    n = card['n']
    groups = ''
    for g in card['groups']:
        opts = ''
        for v, lab, short in g['options']:
            rec = v == g['rec']
            opts += (f'<label class="rad"><input type="radio" name="c{n}-{g["name"]}" value="{attr(v)}" data-card="{n}" '
                     f'data-group="{g["name"]}" data-short="{attr(copy(short))}"><span>{esc(lab)}'
                     f'{" · recommended" if rec else ""}</span></label>')
        leg = f'<p class="glab">{esc(g["label"])}</p>' if g.get('label') else ''
        groups += f'<div class="grp-o" data-group="{g["name"]}" data-rec="{attr(g["rec"] or "")}">{leg}{opts}</div>'
    return (f'<fieldset class="ans"><legend>Your answer to card {n}</legend>{groups}'
            f'<label class="rad chk"><input type="checkbox" data-named="{n}"><span>I approve card {n} by name</span></label>'
            f'<label class="nl" for="note-{n}">A note, or an answer of your own</label>'
            f'<textarea id="note-{n}" rows="2" data-note="{n}"></textarea></fieldset>')


def card_shell(card, body, approve, scores_html, rec_html, extra=''):
    n = card['n']
    flags = ''
    if card.get('lows'):
        flags += chip('A score under 4', 'chip--low')
    if card.get('not_ready'):
        flags += chip('Not signed off by the creative director', 'chip--low')
    return f'''<article class="card" id="card-{n}" data-card="{n}" data-short="{attr(copy(card["short"]))}" aria-labelledby="card-{n}-h">
<header class="card-head"><p class="card-n" aria-hidden="true">{n}</p><div><h3 class="card-h" id="card-{n}-h"><span class="vh">Card {n}. </span>{esc(card["title"])}</h3>
<p class="chips">{chip("Needs your approval by name", "chip--named")}{flags}</p>{card.get("lede_html", "")}</div></header>
<div class="card-body">{body}</div>
<div class="card-foot"><div class="foot-main">{rec_html}<div class="approve"><p class="label">What you approve by name</p><p>{esc(approve)}</p></div>{extra}{scores_html}</div>
{answer_block(card)}</div></article>'''


def rec_block(sc, label_fn=None):
    if not sc:
        return '<div class="rec"><p class="label">The creative director recommends</p><p>Not scored yet.</p></div>'
    r = sc.get('recommended') or {}
    opt = r.get('option', '')
    lab = label_fn(opt) if label_fn else (f'Option {opt}' if re.fullmatch(r'[A-Z]', opt.strip()) else opt)
    return (f'<div class="rec"><p class="label">The creative director recommends</p>'
            f'<p class="rec-o">{esc(lab)}</p><p>{esc(r.get("reason", ""))}</p></div>')


# ---- Civic Line
def cl_option_col(o, sub, rec, size_naming=48, today=None):
    tags = ''
    if o.letter == rec:
        tags += chip('Recommended', 'chip--rec')
    if o.within is True:
        tags += chip('Within DR-135', 'chip--in')
    elif o.within is False:
        tags += chip('Outside DR-135', 'chip--out')
    rows = []
    if o.change:
        rows.append(('What it shows' if o.within is None else 'What changed', esc(o.change)))
    rows += naming_lines(o, size_naming)
    rows += like_lines(o.like, own_label=f'today’s {sub["id"]}')
    name = sub['name'] or display_id(sub['id'])
    return (f'<div class="col{" col--rec" if o.letter == rec else ""}"><p class="col-h">Option {esc(o.letter)}</p><p class="chips">{tags}</p>'
            f'<div class="stage">{sizes_row(o.red, CL_SIZES, f"{name}, option {o.letter}")}</div>'
            f'{dl(rows)}{choice_note(o)}</div>')


def cl_today_col(model, mid, label):
    m = model['masters'][mid]
    return (f'<div class="col col--today"><p class="col-h">{esc(label)}</p><p class="chips">{chip(mid)}</p>'
            f'<div class="stage">{sizes_row(model["master_svg"](mid), CL_SIZES, f"{mid} {m["label"]}, today")}</div>'
            f'<p class="caption">{esc(mid)} {esc(m["label"])}, the October 29 master.</p></div>')


def neighbor_col(model, ids, label):
    figs = ''
    for i in ids:
        m = model['masters'][i]
        figs += (f'<div class="nb"><div class="stage">{sizes_row(model["master_svg"](i), [128, 48], f"{i} {m["label"]}", ref24=False)}</div>'
                 f'<p class="caption">{esc(i)} {esc(m["label"])}</p></div>')
    return f'<div class="col col--today"><p class="col-h">{esc(label)}</p>{figs}</div>'


def fewer_note(card, n_opts, maker_key):
    """D2-622: a card with fewer than three options prints the maker's one-line reason."""
    if n_opts >= 3:
        return ''
    reason = card.get('fewer_reason')
    if not reason:
        warn(f'card {card["n"]} ({card["short"]}) shows {n_opts} option{"s" if n_opts != 1 else ""} and the {maker_key} gives no reason the build can find')
        return (f'<p class="fewer"><span class="label">Why {num_words(n_opts)} option{"s" if n_opts != 1 else ""}</span> '
                'The maker’s reason is not in the notes yet.</p>')
    return f'<p class="fewer"><span class="label">Why {num_words(n_opts)} option{"s" if n_opts != 1 else ""}</span> {esc(reason)}</p>'


def find_fewer_reason(notes_text, names):
    """The maker's one-line reason for showing fewer than three options, from a fix round section of its notes:
    a table row or a bullet that names the drawing and says why."""
    fix = section_text(notes_text, r'fix round')
    if not fix:
        return None
    pats = [re.escape(n.lower()) for n in names if n]
    for t in md_tables(fix):
        rh = next((h for h in t['head'] if re.search(r'reason|why|fewer', h, flags=re.I)), None)
        nh = t['head'][0]
        if not rh:
            continue
        for r in t['rows']:
            cell = strip_md(r.get(nh, '')).lower()
            if any(re.fullmatch(rf'{p}(\s*\(.*\))?', cell) or re.match(rf'{p}\b', cell) for p in pats) and r.get(rh):
                return strip_md(r[rh])
    for ln in fix.split('\n'):
        s = strip_md(ln.lstrip('-* ')).strip()
        low = s.lower()
        if any(re.match(rf'{p}\b', low) for p in pats) and re.search(r'fewer|one option|two options|alone|only|why', low):
            s = re.sub(rf'^({"|".join(pats)})\b[:.,]?\s*', '', s, flags=re.I)
            return s[:1].upper() + s[1:]
    return None


def congress_split(card):
    """The drawings that follow the set picked for CL-025, and those whose recommended letter differs, which get a pick
    of their own inside the card (CL-014 in the rescore)."""
    subs = card['subjects']
    rec = rec_letter(subs[0]['scores'])
    sets = [s for s in subs if s is subs[0] or rec_letter(s['scores']) in (rec, None)]
    return sets, [s for s in subs if s not in sets]


def congress_card(card, model, C):
    subs = card['subjects']
    W = C['cards']['congress']
    lead = subs[0]
    rec = rec_letter(lead['scores'])
    # A drawing whose recommended option differs from the set's letter gets its own pick inside the card (CL-014 in
    # the rescore); the others follow the set picked for CL-025.
    sets, own = congress_split(card)
    card['set_subjects'], card['own_subjects'] = sets, own
    letters = [o.letter for o in lead['options']]
    for s in sets[1:]:
        if [o.letter for o in s['options']] != letters:
            warn(f'Congress set: {s["id"]} has options {[o.letter for o in s["options"]]}, CL-025 has {letters}')
    head = ''.join(f'<p class="cg-colh">{esc(s["id"])} {esc(s["name"])}</p>' for s in sets)
    rows = f'<div class="cg-row cg-row--today"><div class="cg-rowh"><p class="col-h">{esc(W["today_label"])}</p></div>'
    for s in sets:
        rows += (f'<div class="cg-cell"><div class="stage">{sizes_row(model["master_svg"](s["id"]), CL_SIZES, f"{s["id"]} {s["name"]}, today")}</div>'
                 f'<p class="caption">{esc(s["id"])} {esc(s["name"])}, the October 29 master.</p></div>')
    rows += '</div>'
    for L in letters:
        lo = next(o for o in lead['options'] if o.letter == L)
        tags = (chip('Recommended', 'chip--rec') if L == rec else '') + (
            chip('Within DR-135', 'chip--in') if lo.within is True else chip('Outside DR-135', 'chip--out') if lo.within is False else '')
        rows += (f'<div class="cg-row{" cg-row--rec" if L == rec else ""}"><div class="cg-rowh"><p class="col-h">{esc(W["set_label"].format(letter=L))}</p>'
                 f'<p class="chips">{tags}</p><p class="cg-sign">{esc(lo.change)}</p></div>')
        for s in sets:
            o = next((x for x in s['options'] if x.letter == L), None)
            if not o:
                rows += '<div class="cg-cell"><p class="caption">No option in this set.</p></div>'
                continue
            fr = []
            if s is not lead and o.change:
                fr.append(('What changed', esc(o.change)))
            fr += naming_lines(o, 48)
            fr += like_lines(o.like, own_label=f'today’s {s["id"]}')
            rows += (f'<div class="cg-cell"><p class="cg-cellh">{esc(s["id"])} {esc(s["name"])}, set {esc(L)}</p>'
                     f'<div class="stage">{sizes_row(o.red, CL_SIZES, f"{s["id"]} {s["name"]}, set {L}")}</div>{dl(fr)}{choice_note(o)}</div>')
        rows += '</div>'
    followers = [f'{s["id"]}' for s in sets[1:]]
    follow = f'<p class="caption pnote">{esc(W["follows"].format(ids=join_words(followers), lead=lead["id"]))}</p>' if followers else ''
    grid = f'<div class="cg" style="--cgcols:{len(sets)}"><div class="cg-head">{head}</div>{rows}</div>'
    # a drawing with its own pick: today's drawing and its options, in the card's columns
    own_html = ''
    for s in own:
        orec = rec_letter(s['scores'])
        cols = cl_today_col(model, s['id'], W['today_label']) + ''.join(cl_option_col(o, s, orec) for o in s['options'])
        own_html += (f'<h4 class="sub4">{esc(W["own_title"].format(id=s["id"], name=s["name"]))}</h4>'
                     f'<p class="pnote">{esc(W["own_text"].format(id=s["id"]))}</p><div class="cols cols--cl">{cols}</div>')
    # the House drawings beside the chamber options (DR-152)
    nb = []
    for s in subs:
        for i in s['neighbors']:
            if i not in nb and i not in [x['id'] for x in subs]:
                nb.append(i)
    strip = ''
    if nb:
        cells = ''
        for o in lead['options']:
            if o.within is False:
                cells += (f'<div class="nb"><div class="stage">{sizes_row(o.red, [128, 48], f"CL-025 Congress, set {o.letter}", ref24=False)}</div>'
                          f'<p class="caption">CL-025, set {esc(o.letter)}</p></div>')
        for i in nb:
            m = model['masters'][i]
            cells += (f'<div class="nb nb--kept"><div class="stage">{sizes_row(model["master_svg"](i), [128, 48], f"{i} {m["label"]}", ref24=False)}</div>'
                      f'<p class="caption">{esc(i)} {esc(m["label"])}, as drawn</p></div>')
        names = join_words(f'{i} {model["masters"][i]["label"]}' for i in nb)
        strip = (f'<h4 class="sub4">{esc(W["neighbors_title"])}</h4><p>{esc(W["neighbors_text"].format(names=names))}</p>'
                 + frame(f'<div class="nbs">{cells}</div>', W['neighbors_title']))
    body = (f'<p class="honest">{esc(W["honest"])}</p>' + frame(grid, 'The Congress sets') + follow + own_html + strip)
    scored = [(f'{s["id"]} {s["name"]}', s['scores']) for s in subs]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = any(s['scores'] and not s['scores'].get('ready_for_board', True) for s in subs)
    card['groups'] = [{'name': 'set', 'label': W['set_group'] if own else None, 'rec': rec,
                       'options': [(L, f'Set {L}', f'set {L}') for L in letters]}]
    for s in own:
        card['groups'].append({'name': 'own-' + s['id'].lower(), 'label': s['id'], 'rec': rec_letter(s['scores']),
                               'options': [(o.letter, f'Option {o.letter}', f'{s["id"]} option {o.letter}') for o in s['options']]})
    rb = rec_block(lead['scores'], lambda x: f'Set {letter_of(x)}' + (x[1:] if letter_of(x) else ''))
    for s in own:
        rb += rec_block(s['scores'], lambda x, i=s['id']: f'{i}: option {letter_of(x)}' + (x[1:] if letter_of(x) else ''))
    ids = lambda xs: join_words(x['id'] for x in xs)
    approve = W['approve_own'].format(sets=ids(sets), own=ids(own)) if own else W['approve'].format(sets=ids(sets))
    return card_shell(card, body, approve, sh + open_items(scored), rb)


def single_cl_card(card, model, C):
    sub = card['subjects'][0]
    kind = card['kind']
    sc = sub['scores']
    rec = rec_letter(sc)
    cols = ''
    if sub['master']:
        W = C['cards']['redraw']
        cols += cl_today_col(model, sub['id'], W['today_label'])
    else:
        W = C['cards'][kind]
        if sub['neighbors']:
            cols += neighbor_col(model, sub['neighbors'], W['neighbors_label'])
    for o in sub['options']:
        cols += cl_option_col(o, sub, rec)
    body = f'<div class="cols cols--cl">{cols}</div>'
    if sub['master'] and any(o.within is True for o in sub['options']) and 'pediment' in ' '.join(o.change.lower() for o in sub['options']):
        body += f'<p class="caption pnote">{esc(C["cards"]["redraw"]["pediment"])}</p>'
    if len(sub['options']) < 3 and not card.get('fewer_reason'):
        card['fewer_reason'] = find_fewer_reason(model['notes']['cl_notes'], [card['title'], sub['id'], sub['name'] or ''])
    body += fewer_note(card, len(sub['options']), 'Civic Line designer')
    scored = [(card['title'], sc)]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = bool(sc and not sc.get('ready_for_board', True))
    card['groups'] = [{'name': 'option', 'label': None, 'rec': rec,
                       'options': [(o.letter, f'Option {o.letter}', f'option {o.letter}') for o in sub['options']]}]
    approve = (C['cards']['redraw']['approve'] if sub['master'] else C['cards'][kind]['approve']).format(title=card['title'])
    return card_shell(card, body, approve, sh + open_items(scored), rec_block(sc))


# ---- utility
def glyph_pair(o_list, stage, word=None):
    """The 24 and 16 px masters of one or more options, inline in currentColor on one stage."""
    g = ''
    for o in o_list:
        g += inline_svg(o.f24, 24, 24, 'g24') + inline_svg(o.f16, 16, 16, 'g16')
    return f'<span class="tile tile--{stage}">{g}</span>'


def utility_col(opts, subs, rec, word):
    o0 = opts[0]
    tags = chip('Recommended', 'chip--rec') if o0.letter == rec else ''
    tiles = glyph_pair(opts, 'np') + glyph_pair(opts, 'ch')
    spec = ''.join(f'<span class="btn">{inline_svg(o.f24, 24, 24)}<span>{esc(s["title"].split(" (")[0])}</span></span>' for o, s in zip(opts, subs))
    rows = []
    for o, s in zip(opts, subs):
        pre = f'{s["title"].split(" (")[0]}: ' if len(opts) > 1 else ''
        if o.shows:
            rows.append((f'{pre}What it shows', esc(o.shows)))
        for k, v in naming_lines(o, 24):
            rows.append((f'{pre}{k}', v))
        for k, v in like_lines(o.like, show_own=False):
            rows.append((f'{pre}{k}', v))
        rows.append((f'{pre}Pixel-fit check, 1x and 2x', esc(pf_sentence(o.pf24, o.pf16))))
    notes = ''.join(dict.fromkeys(choice_note(o) for o in opts))
    return (f'<div class="col{" col--rec" if o0.letter == rec else ""}"><p class="col-h">Option {esc(o0.letter)}</p><p class="chips">{tags}</p>'
            f'<div class="tiles">{tiles}</div><p class="caption tcap">True size: 24 and 16 px, on Newsprint and on Charcoal</p>'
            f'<div class="spec stage">{spec}</div><p class="caption tcap">At 24 px beside its word</p>{dl(rows)}{notes}</div>')


def utility_card(card, model, C):
    subs = card['subjects']
    W = C['cards']['utility']
    lead = subs[0]
    rec = rec_letter(lead['scores'])
    letters = [o.letter for o in lead['options']]
    for s in subs[1:]:
        if [o.letter for o in s['options']] != letters:
            warn(f'{card["title"]}: {s["id"]} has options {[o.letter for o in s["options"]]}, {lead["id"]} has {letters}')
    cols = ''
    for L in letters:
        opts = [next(o for o in s['options'] if o.letter == L) for s in subs if any(o.letter == L for o in s['options'])]
        cols += utility_col(opts, subs, rec, lead['word'])
    reasons = ''
    n_opts = len(letters)
    if n_opts < 3 and not card.get('fewer_reason'):
        names = [s['title'].split(' (')[0] for s in subs] + [s['label'] for s in subs] + [str(s['word']).replace('-', ' ') for s in subs]
        card['fewer_reason'] = find_fewer_reason(model['notes']['ut_notes'], names) or next((o.reason for o in lead['options'] if o.reason), None)
    body = f'<div class="cols cols--ut">{cols}</div>'
    solid = next((o for o in lead['options'] if re.search(r'\bsolid\b', o.shows, flags=re.I)), None)
    if solid and card.get('partners'):
        titles = {x['id']: x['title'].split(' (')[0] for c in model['cards'] if c['kind'] == 'utility' for x in c['subjects']}
        items = ''
        for key, f in card['partners'].items():
            f24, f16 = SRC['utility'] / f['24'], SRC['utility'] / f['16']
            if not (f24.exists() and f16.exists()):
                warn(f'solid partner {key}: files missing')
                continue
            items += (f'<span class="fam-i"><span class="fam-g">{inline_svg(f24, 24, 24)}{inline_svg(f16, 16, 16)}</span>'
                      f'<span class="fam-l">{esc(titles.get(key, key))}</span></span>')
        body += (f'<h4 class="sub4">{esc(W["partners_title"])}</h4><p class="pnote">{esc(W["partners_text"].format(letter=solid.letter))}</p>'
                 f'<div class="fams fams--short"><div class="fam tile--np">{items}</div><div class="fam tile--ch">{items}</div></div>')
    body += fewer_note(card, n_opts, 'utility designer')
    scored = [(s['title'], s['scores']) for s in subs]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = any(s['scores'] and not s['scores'].get('ready_for_board', True) for s in subs)
    card['groups'] = [{'name': 'option', 'label': None, 'rec': rec, 'options': [(L, f'Option {L}', f'option {L}') for L in letters]}]
    approve = W['pair_approve'] if len(subs) > 1 else W['approve'].format(title=card['title'])
    rb = rec_block(lead['scores'])
    for x in subs:
        names = {x['title'].split(' (')[0].lower(), str(x['word']).replace('-', ' ').lower(), x['label'].lower()}
        hit = next((v for k, v in model['a11y'].items() if k in names), None)
        if hit:
            card['a11y'] = hit
            pick = f'<p class="rec-o">Option {esc(hit["pick"])}</p>' if hit['pick'] else ''
            rb += (f'<div class="rec rec--a11y"><p class="label">{esc(W["a11y_label"])}</p>{pick}'
                   f'<p>“{esc(hit["text"])}”</p><p class="caption">{esc(W["a11y_source"])}</p></div>')
    return card_shell(card, body, approve, sh + open_items(scored), rb)


def family_card(card, model, C):
    W = C['cards']['utility-family']
    sc = card['scores']
    acts = [c for c in model['cards'] if c['kind'] == 'utility']
    # the bare row: each action's recommended option; the ringed row: each action's option drawn in a ring or circle
    bare, ringed = [], []
    fam = card.get('family')
    for c in acts:
        for s in c['subjects']:
            rl = rec_letter(s['scores']) or (s['options'][0].letter if s['options'] else None)
            o = next((x for x in s['options'] if x.letter == rl), None)
            if o:
                bare.append((s, o))
            ring = fam.get(s['id']) if isinstance(fam, dict) else None
            if ring and (SRC['utility'] / ring['24']).exists() and (SRC['utility'] / ring['16']).exists():
                ringed.append((s, Option('ringed', f24=SRC['utility'] / ring['24'], f16=SRC['utility'] / ring['16'])))
            elif o:
                if ring:
                    warn(f'family card: the ringed {s["id"]} files are missing')
                ringed.append((s, o))
    if not fam:
        warn('card %d: the utility manifest has no ringed family set yet; the ringed row repeats the bare one' % card['n'])

    def row(items, stage):
        g = ''
        for s, o in items:
            g += (f'<span class="fam-i"><span class="fam-g">{inline_svg(o.f24, 24, 24)}{inline_svg(o.f16, 16, 16)}</span>'
                  f'<span class="fam-l">{esc(s["title"].split(" (")[0])}</span></span>')
        return f'<div class="fam tile--{stage}">{g}</div>'
    body = ''
    for key, items in (('bare', bare), ('ringed', ringed)):
        body += (f'<h4 class="sub4">{esc(W["rows"][key])}</h4>' +
                 f'<div class="fams">{row(items, "np")}{row(items, "ch")}</div>')
    body += '<p class="caption pnote">Each icon at true size, 24 px then 16 px, on Newsprint and on Charcoal.</p>'
    scored = [(W['short'], sc)]
    # without a scored card, the creative director's answer to the family question is the recommendation (D2-621)
    fq = next((q for q in model['S'].get('family_questions', []) if re.search(r'\bbare\b', q.get('question', ''), flags=re.I)), None)
    if sc:
        sh, lows = scores_block(scored)
        rec_txt = ((sc.get('recommended') or {}).get('option', ''))
        rb = rec_block(sc)
    elif fq:
        sh, lows = f'<div class="scores"><p class="label">The creative director’s scores</p><p class="pnote">{esc(W["unscored"])}</p></div>', []
        ans = str(fq.get('answer', ''))
        rec_txt = 'bare' if re.match(r'\s*yes\b', ans, flags=re.I) else 'ringed'
        reason = re.split(r'(?<=[.])\s+', re.sub(r'^\s*(yes|no)\.\s*', '', ans, flags=re.I))[0]
        rb = (f'<div class="rec"><p class="label">The creative director recommends</p><p class="rec-o">{esc(W["options"][rec_txt])}</p>'
              f'<p>{esc(reason)}</p></div>')
    else:
        sh, lows = scores_block(scored)
        rec_txt, rb = '', rec_block(sc)
    card['lows'] = lows
    card['not_ready'] = bool(sc and not sc.get('ready_for_board', True)) or not (sc or fq)
    rec = 'ringed' if re.search(r'\bring', rec_txt, flags=re.I) and not re.search(r'bare', rec_txt, flags=re.I) else 'bare' if rec_txt else None
    card['groups'] = [{'name': 'family', 'label': None, 'rec': rec,
                       'options': [(k, W['options'][k], k) for k in ('bare', 'ringed')]}]
    return card_shell(card, body, W['approve'], sh + (open_items(scored) if sc else ''), rb)


# ---- pillar fits
def pillars_card(card, model, C):
    W = C['cards']['pillars']
    sc = card['scores']
    ps = card['pillars']
    fit_keys = []
    for p in ps:
        for f in p['fits']:
            k = (f['size_px'], f['fit'])
            if k not in fit_keys:
                fit_keys.append(k)
    fit_keys.sort(key=lambda k: (-k[0], k[1]))
    lines = {k: next((f['line_px'] for p in ps for f in p['fits'] if (f['size_px'], f['fit']) == k), None) for k in fit_keys}
    n_at = {sz: sum(1 for k in fit_keys if k[0] == sz) for sz, _ in fit_keys}
    head = '<p class="pg-h">Master, red-black above, black below</p>' + ''.join(
        (f'<p class="pg-h">{k[0]} px, Fit {k[1]}, {lines[k]} px line</p>' if n_at[k[0]] > 1 else
         f'<p class="pg-h">{k[0]} px, one fit, {lines[k]} px line</p>') for k in fit_keys)
    rows = ''
    for p in ps:
        mid = p['id']
        mrow = ''
        for ed in ('red-black', 'black'):
            mrow += sizes_row(card['master_svg'](mid, ed), PILLAR_MASTER_SIZES, f'{mid} {p["name"]} master, {ed}', ref24=False)
        cells = f'<div class="pg-c"><p class="pg-name">{esc(mid)} {esc(p["name"])}</p><div class="stage">{mrow}</div></div>'
        for k in fit_keys:
            f = next((x for x in p['fits'] if (x['size_px'], x['fit']) == k), None)
            if not f:
                cells += '<div class="pg-c"><p class="caption">No fit.</p></div>'
                continue
            s = f['size_px']
            red, black = ROOT / f['svg_red_black'], ROOT / f['svg_black']
            pf_ok = f['pf_black'] and f['pf_black']['pass'] and f['pf_red'] and f['pf_red']['pass']
            pft = ('Pixel-fit check: passes at 1x and 2x, both editions' if pf_ok else
                   'Pixel-fit check: ' + ('; '.join(sum(((r or {}).get('fails', []) for r in (f['pf_black'], f['pf_red'])), [])) or 'not run'))
            own = f['like'].get('own') or {}
            cells += (f'<div class="pg-c"><div class="stage pg-st">'
                      f'<figure class="sz">{img(red, s, s, f"{p["name"]}, {s} px fit {f["fit"]}, red-black")}<figcaption>Red-black</figcaption></figure>'
                      f'<figure class="sz">{img(black, s, s, f"{p["name"]}, {s} px fit {f["fit"]}, black")}<figcaption>Black</figcaption></figure>'
                      f'<figure class="sz">{img(black, s * 4, s * 4, f"{p["name"]}, {s} px fit {f["fit"]}, black, four times larger", cls="px")}<figcaption>Four times</figcaption></figure></div>'
                      f'<p class="inword">{img(black, s, s, "", cls="iw")}<span>{esc(p["name"])}</span></p>'
                      f'<p class="caption">{esc(pft)}.{" Look-alike figure against its master: " + fmt_like(own["likeness"]) + "." if own else ""}</p></div>')
        rows += f'<div class="pg-row">{cells}</div>'
    grid = f'<div class="pg" style="--cols:{len(fit_keys)}"><div class="pg-row pg-row--h">{head}</div>{rows}</div>'
    body = frame(grid, 'The pillar fits') + x2_grid(ps, W) + '<p class="caption pnote">The black edition is the one the guide sets under 48 px. The third view in each fit draws the black edition four times larger to show its pixels. Beside the word, each fit sits at true size next to 15 px Inter.</p>'
    naming = ''
    if sc and sc.get('naming_test'):
        li = ''.join(f'<li><b>{esc(n.get("option"))}</b>: “{esc(str(n.get("creative_director_reading", "")).rstrip("."))}.” {esc(n.get("creative_director_verdict", ""))}.</li>' for n in sc['naming_test'])
        naming = f'<div class="naming"><p class="label">Naming test, beside each pillar’s word</p><ul>{li}</ul></div>'
    body += naming
    scored = [(W['short'], sc)]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = bool(sc and not sc.get('ready_for_board', True))
    rec_txt = ((sc or {}).get('recommended') or {}).get('option', '')
    groups = []
    for size in sorted({k[0] for k in fit_keys}, reverse=True):
        ls = [k[1] for k in fit_keys if k[0] == size]
        if len(ls) < 2:
            continue
        m = re.search(rf'{size} px Fit ([A-Z])', rec_txt) or re.search(r'Fit ([A-Z])', rec_txt)
        groups.append({'name': f's{size}', 'label': f'{size} px', 'rec': m.group(1) if m else None,
                       'options': [(L, f'Fit {L}, {lines[(size, L)]} px line', f'{size} px Fit {L}') for L in ls]})
    if re.search(r'\b2x\b', rec_txt):
        x2 = 'master' if re.search(r'master on 2x', rec_txt) else 'fit'
        groups.append({'name': 'x2', 'label': W['x2_label'], 'rec': x2,
                       'options': [(k, W['x2_options'][k][0], W['x2_options'][k][1]) for k in ('master', 'fit')]})
    card['groups'] = groups
    return card_shell(card, body, W['approve'], sh + open_items(scored), rec_block(sc))


def x2_grid(ps, W):
    """The Civic Line designer's renders of each master and fit as a 2x screen draws them, enlarged (fix round, M11)."""
    d = SRC['screen2x']
    if not d.exists():
        warn('the pillar fits have no 2x screen renders')
        return ''
    found = {}
    for f in sorted(d.glob('*-On-2x-Screen-Enlarged.png')):
        m = re.search(r'_((?:CL|R)-\d+)-[\w-]+?-(\d+)px-(Master|Fit-[A-Z])-On-2x-Screen-Enlarged\.png$', f.name)
        if m:
            found[(m.group(1), int(m.group(2)), m.group(3))] = f
    cols = sorted({(k[1], k[2]) for k in found}, key=lambda c: (-c[0], c[1] != 'Master', c[1]))
    if not cols:
        return ''
    n_fit = {sz: sum(1 for x, k in cols if x == sz and k != 'Master') for sz, _ in cols}
    head = '<p class="pg-h"></p>' + ''.join(
        f'<p class="pg-h">{s} px, {"the master" if k == "Master" else ("Fit " + k[-1]) if n_fit[s] > 1 else "the fit"}</p>' for s, k in cols)
    rows, mag = '', None
    for p in ps:
        cells = f'<div class="x2-c"><p class="pg-name">{esc(p["id"])} {esc(p["name"])}</p></div>'
        for s, k in cols:
            f = found.get((p['id'], s, k))
            if not f:
                cells += '<div class="x2-c"></div>'
                continue
            w, h = png_size(f)
            mag = round(w / (s * 2))
            cells += f'<div class="x2-c">{img(f, w, h, f"{p["name"]}, {s} px, {"the master" if k == "Master" else "fit " + k[-1]}, as a 2x screen draws it, {num_words(mag)} times larger", cls="px")}</div>'
        rows += f'<div class="x2-row">{cells}</div>'
    grid = f'<div class="x2" style="--x2cols:{len(cols)}"><div class="x2-row x2-row--h">{head}</div>{rows}</div>'
    return (f'<h4 class="sub4">{esc(W["x2_title"])}</h4><p class="pnote">{esc(W["two_x"])}</p>'
            + frame(grid, W['x2_title']) + f'<p class="caption pnote">{esc(W["x2_caption"].format(mag=num_words(mag or 3)))}</p>')


# ---- identity
def identity_lines(plate):
    """Each end mark line of text from the identity plate's Newsprint cells: today's and the four fits."""
    out = {}
    for key in ('T17', '14A', '14B', 'T15', '12A', '12B'):
        m = re.search(rf'id="em-{key}">(.*?)</div>', plate, flags=re.S)
        need(m, f'identity plate: no line for {key}')
        p = re.search(r'<p style="[^"]*font-size[^"]*">.*?</p>', m.group(1), flags=re.S)
        need(p, f'identity plate: no paragraph in line {key}')
        t = p.group(0)
        t = re.sub(r'<title>.*?</title>', '', t, flags=re.S)
        t = re.sub(r'width:\d+px;', 'max-width:520px;', t, count=1)
        t = ov(t)
        t = t.replace('class="oai-svg ', 'class="snap ')
        out[key] = t
    return out


def end_mark_card(card, model, C):
    W = C['cards']['end-mark']
    figs = card['figs']
    sc = card['scores']
    plate = SRC['id_plate'].read_text()
    lines = identity_lines(plate)
    ef = figs['end_files']
    sizes = sorted({int(k[:-1]) for k in ef}, reverse=True)
    blocks = ''
    for surface in ('newsprint', 'charcoal'):
        cols = ''
        for s in sizes:
            text_px = ef[f'{s}A']['text_px']
            items = [('Today', lines[f'T{text_px}'])] + [(f'Fit {k[-1]}', lines[k]) for k in sorted(ef) if int(k[:-1]) == s]
            st = ''
            for lab, ln in items:
                if surface == 'charcoal':
                    ln = ln.replace('-on-newsprint', '-on-charcoal')
                st += f'<div class="em-l"><p class="em-lab">{esc(lab)}</p>{ln}</div>'
            cols += (f'<div class="em-col"><p class="col-h">B at {s} px, in {text_px} px text</p>'
                     f'<div class="stage{" stage--ch" if surface == "charcoal" else ""} em-st">{st}</div></div>')
        blocks += (f'<p class="label vw-h">{esc(W["stack_label"])}, on {surface.capitalize()}</p>'
                   f'<div class="em-cols">{cols}</div>')
    blocks += f'<p class="caption pnote">{chip("Illustrative", "chip--ill")} {esc(W["illustrative"])}</p>'
    # enlarged views, the identity designer's renders at their own size
    iddir = SRC['id_plate'].parent
    enl = ''
    for s in sizes:
        enl += '<div class="enl-col">'
        text_px = ef[f'{s}A']['text_px']
        for lab, stem in [('Today', f'Today-{text_px}')] + [(f'Fit {k[-1]}', f'Fit-{k[-1]}-{s}') for k in sorted(ef) if int(k[:-1]) == s]:
            cells = ''
            for sc_ in ('1x', '2x'):
                p = iddir / f'{DATE}_Identity-End-Mark-{stem}-{sc_}-Enlarged.png'
                if not p.exists():
                    warn(f'end mark: {p.name} missing')
                    continue
                w, h = png_size(p)
                cap = (f'As a 1x screen draws it, {num_words(END_MAG["1x"])} times larger' if sc_ == '1x'
                       else f'As a 2x screen draws it, {num_words(END_MAG["2x"])} times larger')
                cells += f'<figure class="enl">{img(p, w, h, f"{"Today’s end mark" if lab == "Today" else lab} at {s} px, {cap[:1].lower() + cap[1:]}", cls="px")}<figcaption class="caption">{esc(cap)}</figcaption></figure>'
            enl += f'<div class="enl-row"><p class="col-h">{esc(lab)}, B at {s} px in {text_px} px text</p><div class="enl-cells">{cells}</div></div>'
        enl += '</div>'
    body = blocks + '<h4 class="sub4">Enlarged, beside a capital H of the same text</h4>' + frame(f'<div class="enls enls--em">{enl}</div>', 'The end mark enlarged')
    if W.get('two_x'):
        body += f'<p class="pnote">{esc(W["two_x"])}</p>'
    # figures: rows at 1x with the line at four positions
    mrow = ''
    for key, lab in [('T17', 'Today, 17 px text'), ('14A', 'Fit A, 14 px'), ('14B', 'Fit B, 14 px'), ('T15', 'Today, 15 px text'), ('12A', 'Fit A, 12 px'), ('12B', 'Fit B, 12 px')]:
        m = figs['measure']['end_mark'].get(f'{key}-newsprint')
        if not m:
            continue
        full = round(100 * m.get('b_full_ink_share_at_1x', 0))
        tops = sorted({r['top_rows_over_h'] for r in m['rows_at_1x']})
        tails = sorted({r['tail_rows_under_h'] for r in m['rows_at_1x']})
        rng = lambda v: f'{int(v[0])}' if len(v) == 1 else f'{int(v[0])} to {int(v[-1])}'
        mrow += (f'<tr><th scope="row">{esc(lab)}</th><td class="num">{m["b_px"]:.1f}</td><td class="num">{rng(tops)}</td>'
                 f'<td class="num">{rng(tails)}</td><td class="num">{full}%</td></tr>')
    body += (f'<div class="tw" role="region" tabindex="0" aria-label="End mark figures"><table class="fig-t"><caption class="caption">'
             'Measured by the identity designer in Chromium on Newsprint, with the line at four positions between pixels. '
             'Rows over or under are rows of B above the capital H’s top row or below its last row.</caption>'
             '<thead><tr><th scope="col">Mark</th><th scope="col">B tall, px</th><th scope="col">Rows over the capitals</th>'
             f'<th scope="col">Rows under the baseline</th><th scope="col">Ink at full color, 1x</th></tr></thead><tbody>{mrow}</tbody></table></div>')
    scored = [(W['short'], sc)]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = bool(sc and not sc.get('ready_for_board', True))
    rec_txt = ((sc or {}).get('recommended') or {}).get('option', '')
    groups = []
    for s in sizes:
        ls = sorted(k[-1] for k in ef if int(k[:-1]) == s)
        m = re.search(rf'Fit ([A-Z]) at {s} px', rec_txt) or re.search(r'Fit ([A-Z])', rec_txt)
        groups.append({'name': f's{s}', 'label': f'B at {s} px', 'rec': m.group(1) if m else None,
                       'options': [(L, f'Fit {L}', f'Fit {L} at {s} px') for L in ls]})
    card['groups'] = groups
    return card_shell(card, body, W['approve'], sh + open_items(scored), rec_block(sc))


def lockmark_card(card, model, C):
    W = C['cards']['lockmark']
    figs = card['figs']
    sc = card['scores']
    lf = figs['lockmark_files']
    iddir = SRC['identity']
    today = {16: sorted((iddir / 'lockmark').glob('*_Lockmark-16px-Master.svg'))[-1]}
    new = {}
    for k, v in lf.items():
        today[int(k)] = iddir / v['today']
        new[int(k)] = ROOT / v['file']
    meas = figs['measure']['lockmark']['at_1x']

    def master_for(size):
        ms = [m for m in sorted(today) if f'today-{m}-at-{size}' in meas]
        return ms[0] if ms else max(m for m in today if m <= size)
    rows = ''
    for lab, which in (('Today', 'today'), ('Rebuilt', 'new')):
        cells = ''
        for s in LOCK_SIZES:
            m = master_for(s)
            f = (new.get(m) or today[m]) if which == 'new' else today[m]
            key = f'{which}-{m}-at-{s}'
            r = meas.get(key) or (meas.get(f'today-{m}-at-{s}') if which == 'new' and m not in new else None)
            whole = f'nodes whole {round(100 * r["node_core_full"])}%' if r else ''
            if m not in new:
                whole = 'one circle per node' + (', today’s file kept' if which == 'new' else '')
            cells += (f'<figure class="lk"><span class="lk-g">{inline_svg(f, s, s, style="color:var(--oa-color-graphic-essential-on-newsprint)")}</span>'
                      f'<figcaption class="caption">{s} px, from the {m} px master{"<br>" + esc(whole) if whole else ""}</figcaption></figure>')
        rows += f'<div class="lk-row"><p class="col-h">{esc(lab)}</p><div class="stage lk-st" data-red="identity">{cells}</div></div>'
    body = frame(f'<div class="lks">{rows}</div>', 'The lockmark at five sizes')
    body += ('<p class="caption pnote">“Nodes whole” is the share of a node’s core drawn at full color at 1x, measured by the identity designer (the range test of D2-465). '
             'Today’s nodes part into light stripes where it falls under 100%.</p>')
    enl = ''
    pd = SRC['id_plate'].parent
    for lab, stem in (('Today', 'Today'), ('Rebuilt', 'Rebuilt')):
        cells = ''
        for s in LOCK_SIZES:
            p = pd / f'{DATE}_Identity-Lockmark-{stem}-{s}px-1x-Enlarged.png'
            if p.exists():
                w, h = png_size(p)
                mag = round(w / s)
                cells += f'<figure class="enl">{img(p, w, h, f"{"Today’s lockmark" if lab == "Today" or s == min(LOCK_SIZES) else "The rebuilt lockmark"} at {s} px{", kept as it is" if lab != "Today" and s == min(LOCK_SIZES) else ""}, as a 1x screen draws it, {num_words(mag)} times larger", cls="px")}<figcaption class="caption">{s} px, {num_words(mag)} times</figcaption></figure>'
        enl += f'<div class="enl-row"><p class="col-h">{esc(lab)}, as a 1x screen draws it</p><div class="enl-cells">{cells}</div></div>'
    cells = ''
    for lab, stem in (('Today’s 48 px master', 'Today-48px'), ('Rebuilt 48 px master', 'Rebuilt-48px'), ('The display master, for comparison', 'Display-48px')):
        p = pd / f'{DATE}_Identity-Lockmark-{stem}-2x-Enlarged.png'
        if p.exists():
            w, h = png_size(p)
            mag = round(w / 96)
            cells += f'<figure class="enl">{img(p, w, h, f"{lab.split(",")[0]} at 48 px, as a 2x screen draws it, {num_words(mag)} times larger", cls="px")}<figcaption class="caption">{esc(lab)}, {num_words(mag)} times</figcaption></figure>'
    enl += f'<div class="enl-row"><p class="col-h">At 48 px, as a 2x screen draws it</p><div class="enl-cells">{cells}</div></div>'
    body += '<h4 class="sub4">Enlarged</h4>' + frame(f'<div class="enls">{enl}</div>', 'The lockmark enlarged')
    fd = figs.get('feed') or {}
    if fd:
        t, n = fd['today'], fd['new']
        body += (f'<p class="pnote">The feed test (D2-468): when a feed shrinks the 1,200 px share card to 360 px, the sign-off keeps '
                 f'{t["at_360"]["dark_nodes_kept"]} of 8 nodes and {t["at_360"]["lever_red_px"]} red pixels with today’s master and '
                 f'{n["at_360"]["dark_nodes_kept"]} of 8 and {n["at_360"]["lever_red_px"]} with the rebuilt one, against a floor of {fd["min_red_px"]}. '
                 f'At 500 px both keep {t["at_500"]["lever_red_px"]} red pixels.</p>')
    ident = figs['measure'].get('identical_at_own_size') or {}
    if ident:
        same = sum(1 for v in ident.values() if v)
        body += f'<p class="pnote">At 24 and 48 px the rebuilt files draw today’s pixels exactly: {same} of {len(ident)} comparisons match pixel for pixel, at 1x and 2x on Newsprint, Charcoal and Prussian.</p>'
    scored = [(W['short'], sc)]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = bool(sc and not sc.get('ready_for_board', True))
    card['groups'] = [{'name': 'lock', 'label': None, 'rec': 'approve' if sc and re.search(r'approve', str((sc.get('recommended') or {}).get('option', '')), flags=re.I) else None,
                       'options': [('approve', W['options']['approve'], 'the rebuilt files'), ('keep', W['options']['keep'], 'keep today’s files')]}]
    return card_shell(card, body, W['approve'], sh + open_items(scored), rec_block(sc))


def l6_card(card, model, C):
    W = C['cards']['l6']
    figs = card['figs']
    sc = card['scores']
    pd = SRC['id_plate'].parent
    l6 = figs['l6']
    strips = ''
    for lab, stem in (('Today, without its dots (DR-129)', 'L6-Today-No-Dots'), ('Proposal: centered', 'L6-Centered')):
        p1, p2 = pd / f'{DATE}_Identity-{stem}-1x.png', pd / f'{DATE}_Identity-{stem}-2x.png'
        need(p1.exists(), f'L6: {p1.name} missing')
        w, h = png_size(p1)
        strips += (f'<figure class="l6"><figcaption class="col-h">{esc(lab)}</figcaption>'
                   f'{img(p1, w, h, f"L6, {lab[:1].lower() + lab[1:]}, at {w} px", srcset2x=p2 if p2.exists() else None)}</figure>')
    body = frame(f'<div class="l6s">{strips}</div>', 'L6, today and centered')
    body += (f'<p class="pnote">Both strips at {w} px, L6’s smallest width on screen, on Prussian in White. '
             f'Centered, the wordmark and tagline move down {l6["shift_down_units"]:g} units of L6’s 1,400 by 300 layout, '
             f'{l6["shift_down_px_at_884"]:g} px at 884 px, so the span from the wordmark’s cap line to the tagline’s baseline has its middle on the strip’s middle. '
             f'The wordmark’s cap line then stands {l6["centered_cap_line"] - l6["lockmark_ink_top"]:.1f} units under the lockmark’s top nodes, '
             f'where today the two meet.</p>')
    scored = [(W['short'], sc)]
    sh, lows = scores_block(scored)
    card['lows'] = lows
    card['not_ready'] = bool(sc and not sc.get('ready_for_board', True))
    card['groups'] = [{'name': 'l6', 'label': None, 'rec': 'approve' if sc and re.search(r'approve', str((sc.get('recommended') or {}).get('option', '')), flags=re.I) else None,
                       'options': [('approve', W['options']['approve'], 'centered'), ('keep', W['options']['keep'], 'keep L6 as drawn today')]}]
    return card_shell(card, body, W['approve'], sh + open_items(scored), rec_block(sc))


# ------------------------------------------------------------------------------------------------ assemble
def number_cards(model, C):
    global N_CARDS
    cards = model['cards']
    for i, c in enumerate(cards, 1):
        c['n'] = i
        k = c['kind']
        if k == 'congress':
            c['title'], c['short'] = C['cards']['congress']['title'], C['cards']['congress']['short']
        elif k == 'redraw':
            s = c['subjects'][0]
            c['title'] = f'{s["id"]} {s["name"]}'
            c['short'] = c['title']
        elif k in ('testify', 'contact'):
            c['title'] = c['short'] = C['cards'][k]['short']
        elif k == 'utility':
            titles = [s['title'].split(' (')[0] for s in c['subjects']]
            c['title'] = join_words(titles) if len(titles) > 1 else c['subjects'][0]['title']
            c['short'] = join_words(titles)
        else:
            W = C['cards'][k]
            c['title'], c['short'] = W.get('title', W['short']), W['short']
    N_CARDS = len(cards)
    ut = [c['n'] for c in cards if c['kind'] == 'utility']
    ident = [c['n'] for c in cards if c['group'] == 'identity']
    FILL.update({
        'n_cards': len(cards), 'n_civic': sum(1 for c in cards if c['group'] == 'civic'),
        'family_n': next(c['n'] for c in cards if c['kind'] == 'utility-family'),
        'first_action': ut[0], 'last_action': ut[-1], 'n_utility': num_words(len(ut)),
        'pillars_n': next(c['n'] for c in cards if c['kind'] == 'pillars'),
        'first_identity': ident[0], 'flag': fmt_like(model['like'].flag), 'watch': fmt_like(model['like'].watch),
    })


def lede(card, C):
    k = card['kind']
    if k == 'congress':
        W = C['cards']['congress']
        sets, own = congress_split(card)
        own_line = W['own_line'].format(own=join_words(f'{x["id"]} {x["name"]}' for x in own)) if own else ''
        return ''.join(f'<p class="card-lede">{md(p.format(set_ids=join_words(x["id"] for x in sets), own_line=own_line))}</p>' for p in W['lede'])
    if k == 'redraw':
        s = card['subjects'][0]
        lost = 'columns' if any('column' in o.change.lower() for o in s['options']) else 'dome'
        return ''.join(f'<p class="card-lede">{md(p.format(title=card["title"], lost=lost))}</p>' for p in C['cards']['redraw']['lede'])
    if k == 'utility':
        s = card['subjects']
        W = C['cards']['utility']

        def asked(e):
            a = str(e.get('asked', '')).rstrip('.')
            return W['own_asked'] if a.lower().startswith('its own') else a[:1].lower() + a[1:]
        if len(s) > 1:
            line = W['pair_lede'].format(names=join_words(x['title'].split(' (')[0] for x in s),
                                         asked=join_words(asked(x['entry']) for x in s))
        else:
            e = s[0]['entry']
            line = W['lede'].format(label=e['label'], asked=asked(e))
        return f'<p class="card-lede">{esc(line)}</p>'
    return paras(C['cards'][k].get('lede'), 'card-lede')


RENDER = {'congress': congress_card, 'redraw': single_cl_card, 'testify': single_cl_card, 'contact': single_cl_card,
          'utility-family': family_card, 'utility': utility_card, 'pillars': pillars_card, 'end-mark': end_mark_card,
          'lockmark': lockmark_card, 'l6': l6_card}


def reply_section(model, C):
    W = C['reply']
    lines = ''
    for c in model['cards']:
        gs = ''
        for g in c['groups']:
            opts = ''.join(f'<label class="pill"><input type="radio" name="p{c["n"]}-{g["name"]}" value="{attr(v)}" data-card="{c["n"]}" '
                           f'data-group="{g["name"]}" aria-label="Card {c["n"]}, {attr(copy(g["label"] + ", " if g.get("label") else ""))}{attr(copy(lab))}"><span>{esc(short_label(lab))}'
                           f'{"<span class=star aria-hidden=true> ✓</span>" if False else ""}</span></label>' for v, lab, _ in g['options'])
            gl = f'<span class="pg-l">{esc(g["label"])}</span>' if g.get('label') else ''
            rl = next((short_label(lab) for v, lab, _ in g['options'] if v == g['rec']), None)
            rc = f'<span class="pg-l pg-rec">Recommended: {esc(rl)}</span>' if rl else ''
            gs += f'<span class="pgrp">{gl}{opts}{rc}</span>'
        lines += (f'<li class="bl" data-line="{c["n"]}"><a class="bl-n" href="#card-{c["n"]}"><span class="n">{c["n"]}</span> {esc(c["short"])}</a>'
                  f'<span class="bl-o">{gs}</span><label class="pill pill--named"><input type="checkbox" data-named="{c["n"]}" aria-label="I approve card {c["n"]} by name">'
                  f'<span>I approve by name</span></label></li>')
    box = f'''<div class="reply oa-surface-prussian" id="reply-box" role="region" aria-labelledby="reply-h">
<h3 id="reply-h">{esc(W["title"])}</h3>{paras(W["text"])}<p>{esc(W["storage"])}</p>
<ol class="ballot">{lines}</ol>
<label class="label" for="reply-text">Reply</label>
<textarea id="reply-text" rows="12" readonly data-sample="{attr(copy(C["sample_reply"]))}">{esc(C["sample_reply"])}</textarea>
<div class="reply-row"><button type="button" id="copy-reply">Copy the reply</button><span id="copy-status" role="status" aria-live="polite"></span></div></div>'''
    return f'<section class="sec" id="reply" aria-labelledby="reply-sh"><h2 class="sec-h" id="reply-sh">Your reply</h2>{box}</section>'


def short_label(lab):
    m = re.match(r'^(Option|Set|Fit) ([A-Z])\b', lab)
    return m.group(2) if m and m.group(1) in ('Option', 'Set') else lab.split(',')[0]


CSS = r'''
/* The stage B drawings board. The changes board's shell on Newsprint: the grid margins of tokens.css, the title, section,
   H3 and H4 styles, hairlines in Stone, White cards for words, Newsprint and Charcoal stages that hold the drawings at
   true size, and one Prussian panel for the reply. No red of the board's own: Pillar Red appears only inside drawings. */
:root{--m:var(--oa-layout-grid-phone-small-margin);--g:var(--oa-layout-grid-phone-small-gutter);--max:82rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--np:var(--oa-color-surface-newsprint);--ch:var(--oa-color-surface-charcoal);
--wink-2:var(--oa-color-text-secondary-on-white);--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace}
@media (min-width:24.375em){:root{--m:var(--oa-layout-grid-phone-margin);--g:var(--oa-layout-grid-phone-gutter)}}
@media (min-width:48em){:root{--m:var(--oa-layout-grid-tablet-margin);--g:var(--oa-layout-grid-tablet-gutter)}}
@media (min-width:64em){:root{--m:var(--oa-layout-grid-desktop-margin);--g:var(--oa-layout-grid-desktop-gutter)}}
@media (min-width:90em){:root{--m:var(--oa-layout-grid-wide-margin);--g:var(--oa-layout-grid-wide-gutter)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--np);scroll-padding-top:var(--oa-space-300)}
body{margin:0;background:var(--np);color:var(--ink);font:var(--oa-type-body);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration-thickness:var(--oa-border-width-underline);text-underline-offset:.2em}
a:hover{text-decoration-thickness:var(--oa-border-width-underline-hover)}
:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring-on-newsprint);outline-offset:var(--oa-border-focus-offset)}
.card :focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
.oa-surface-prussian :focus-visible{outline-color:var(--oa-color-focus-ring-on-prussian)}
p{margin:0 0 var(--oa-space-200);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
code{font:500 .875rem/1.4 var(--mono);overflow-wrap:anywhere}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
[hidden]{display:none!important}
.board{max-width:calc(var(--max) + 2 * var(--m));margin:0 auto;padding:0 var(--m) var(--oa-space-1300)}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2)}
.caption{font:var(--oa-type-caption);color:var(--ink-2)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.n{color:var(--ink-2);font-variant-numeric:tabular-nums}
.num{font-variant-numeric:tabular-nums}
.nc{text-transform:none}
/* cover */
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.cover{padding:var(--oa-space-800) 0 0}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-400);max-width:14ch;text-wrap:balance}
.cover-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500) var(--oa-space-800);align-items:start}
@media (min-width:64em){.cover-grid{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}}
.facts{margin-top:var(--oa-space-300)}.facts p{font:var(--oa-type-body-small);color:var(--ink-2)}
.ask{background:var(--white);border:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-300) var(--oa-space-400)}
.ask h2{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-200)}
.ask ol{margin:0 0 var(--oa-space-300);padding-left:1.4em}.ask li{margin:0 0 var(--oa-space-100)}
.ask .q{font:italic 400 1.125rem/1.5 var(--oa-font-family-quote);margin:0}
.legend{margin:var(--oa-space-600) 0 0;display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200) var(--oa-space-500);border-top:var(--oa-border-width-hairline) solid var(--hair);padding-top:var(--oa-space-300)}
@media (min-width:64em){.legend{grid-template-columns:repeat(2,minmax(0,1fr))}}
.legend h2{grid-column:1/-1;font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0}
.legend div p{font:var(--oa-type-body-small);margin:0}.legend b{display:block;font:var(--oa-type-ui);font-weight:600;margin-bottom:2px}
.toc{margin:var(--oa-space-600) 0 0;border-top:var(--oa-border-width-hairline) solid var(--hair);border-bottom:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-200) 0}
.toc ol{list-style:none;margin:0;padding:0;columns:1;column-gap:var(--oa-space-500)}
@media (min-width:48em){.toc ol{columns:2}}@media (min-width:80em){.toc ol{columns:3}}
.toc li{break-inside:avoid}
.toc a{display:flex;gap:.6em;align-items:baseline;min-height:2rem;padding:var(--oa-space-050) 0;font:var(--oa-type-body-small);text-decoration:none}
.toc a:hover{text-decoration:underline}.toc .n{flex:none;min-width:1.8em;font-weight:600}
/* sections */
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-400)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:0 0 var(--oa-space-300);text-wrap:balance}
.sec > .intro{margin-bottom:var(--oa-space-500)}
h3,.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;text-wrap:balance}
h4,.sub4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-500) 0 var(--oa-space-200);text-wrap:balance}
/* cards */
.cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500)}
.cards > li{min-width:0}
.card{background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-300) var(--oa-space-200);min-width:0}
@media (min-width:48em){.card{padding:var(--oa-space-400) var(--oa-space-500)}}
.card .label,.card .caption{color:var(--wink-2)}
.card-head{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-100) var(--oa-space-300)}
@media (min-width:48em){.card-head{grid-template-columns:4.5rem minmax(0,1fr)}}
.card-n{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);font-variant-numeric:tabular-nums;margin:0}
.card-h{margin:0 0 var(--oa-space-150);max-width:32ch}
.card-lede{max-width:var(--oa-layout-measure-intro-max)}
.chips{margin:0 0 var(--oa-space-200);display:flex;flex-wrap:wrap;gap:var(--oa-space-100)}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);padding:1px 6px;white-space:nowrap;color:var(--oa-color-text-primary-on-white)}
.chip--named,.chip--rec{background:var(--oa-color-palette-charcoal);color:var(--oa-color-text-primary-on-charcoal);border-color:var(--oa-color-palette-charcoal)}
.chip--out{border-style:dashed}
.chips .chip{white-space:normal}
.chip--low,.chip--flag{border-width:2px;font-weight:700}
.chip--watch{border-style:dotted}
.chip--ill{margin-right:.4em}
.honest{font:var(--oa-type-ui);font-weight:600;border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding:var(--oa-space-100) var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.card-body{margin-top:var(--oa-space-300);min-width:0}
.cols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-400) var(--oa-space-300)}
@media (min-width:40em){.cols{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:72em){.cols--cl{grid-template-columns:repeat(4,minmax(0,1fr))}.cols--ut{grid-template-columns:repeat(3,minmax(0,1fr))}}
.col{min-width:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding-top:var(--oa-space-150)}
.col--rec{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:calc(var(--oa-space-150) - 3px)}
.col-h{font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-100);color:var(--oa-color-text-primary-on-white)}
.stage{background:var(--np);color:var(--ink);padding:var(--oa-space-200);width:max-content;max-width:100%}
.stage--ch{background:var(--ch);color:var(--oa-color-text-primary-on-charcoal)}
.stage .caption,.stage figcaption{color:var(--ink-2)}
.stage--ch .caption,.stage--ch .em-lab{color:var(--oa-color-text-secondary-on-charcoal)}
.sizes{display:flex;align-items:flex-end;gap:var(--oa-space-200)}
.sizes + .sizes{margin-top:var(--oa-space-200)}
.sz{margin:0;display:flex;flex-direction:column;align-items:center;gap:var(--oa-space-100)}
.sz figcaption{font:var(--oa-type-caption);color:var(--ink-2);white-space:nowrap}
.ref{margin:var(--oa-space-100) 0 0}
img{display:block;max-width:none}
img.px{image-rendering:pixelated}
dl.figs{margin:var(--oa-space-200) 0 0;font:var(--oa-type-body-small)}
dl.figs div{padding:var(--oa-space-100) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
dl.figs dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);margin-bottom:2px}
dl.figs dd{margin:0}
dl.figs .chip{padding:0 4px;margin-left:.2em}
.cd-note{font:var(--oa-type-body-small);margin-top:var(--oa-space-150)}.cd-note .label{display:block}
.pnote{font:var(--oa-type-body-small);margin-top:var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.fewer{font:var(--oa-type-body-small);margin-top:var(--oa-space-300);border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding-top:var(--oa-space-150);max-width:var(--oa-layout-measure-intro-max)}
.fewer .label{display:block}
/* frames that keep true size */
.frame{overflow-x:auto;overflow-y:hidden;max-width:100%;min-width:0}
.frame > *{width:max-content}
.hint{margin:var(--oa-space-100) 0 0}
/* Congress */
.cg{display:grid;gap:0}
.cg-head,.cg-row{display:grid;grid-template-columns:repeat(var(--cgcols,4),16.5rem);gap:var(--oa-space-200) var(--oa-space-300)}
.cg-rowh{grid-column:1/-1;display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300)}
.cg-rowh .col-h,.cg-rowh .chips{margin:0}
.cg-head{padding-bottom:var(--oa-space-100)}
.cg-colh{font:var(--oa-type-ui);font-weight:700;margin:0;color:var(--oa-color-text-primary-on-white)}
.cg-row{border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-150) 0 var(--oa-space-300)}
.cg-row--rec{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal)}
.cg-rowh .chips{margin-bottom:var(--oa-space-100)}
.cg-sign{font:var(--oa-type-body-small);margin:0;flex-basis:100%}
.cg-cellh{display:none}
.cg-cell{min-width:0}
.cg-cell .stage{width:100%}
@media (max-width:63.99em){
  .cg-head{display:none}.cg-row{grid-template-columns:minmax(0,1fr)}.cg-cellh{display:block;font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-100)}
  .cg .stage{width:max-content}.frame > .cg{width:auto}}
@media (min-width:40em) and (max-width:63.99em){.cg-row{grid-template-columns:repeat(2,minmax(0,1fr))}.cg-rowh{grid-column:1/-1}}
.nbs{display:flex;gap:var(--oa-space-300);align-items:flex-start}
.nb{margin:0}.nb .caption{margin:var(--oa-space-100) 0 0}
.col--today .nb + .nb{margin-top:var(--oa-space-200)}
/* utility */
.tiles{display:flex;flex-wrap:wrap;gap:0}
.tile{display:inline-flex;align-items:center;gap:var(--oa-space-200);padding:var(--oa-space-150) var(--oa-space-200);background:var(--np);color:var(--oa-color-graphic-essential-on-newsprint)}
.tile--ch{background:var(--ch);color:var(--oa-color-graphic-essential-on-charcoal)}
.tile--np{background:var(--np);color:var(--oa-color-graphic-essential-on-newsprint)}
.tcap{margin:var(--oa-space-100) 0 var(--oa-space-200)}
.spec{display:flex;flex-wrap:wrap;gap:var(--oa-space-150);padding:var(--oa-space-150)}
.btn{display:inline-flex;align-items:center;gap:var(--oa-space-100);min-height:44px;padding:0 var(--oa-space-200) 0 var(--oa-space-150);border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-newsprint);font:var(--oa-type-ui);color:var(--ink)}
.fam{display:flex;flex-wrap:wrap;gap:var(--oa-space-200) var(--oa-space-300);padding:var(--oa-space-200)}
.fam-i{display:flex;flex-direction:column;align-items:center;gap:var(--oa-space-100);min-width:4.5rem}
.fam-g{display:flex;align-items:center;gap:var(--oa-space-150)}
.fam-l{font:var(--oa-type-caption);text-align:center}
.fam.tile--np .fam-l{color:var(--ink-2)}.fam.tile--ch .fam-l{color:var(--oa-color-text-secondary-on-charcoal)}
/* pillars */
.pg{display:grid;gap:0}
.pg-row{display:grid;grid-template-columns:17rem repeat(var(--cols),16.5rem);gap:var(--oa-space-300);border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-200) 0}
.pg-row--h{border-top:0;padding-top:0}
.pg-h{font:var(--oa-type-ui);font-weight:700;margin:0;color:var(--oa-color-text-primary-on-white)}
.pg-name{font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-100)}
.pg-st{display:flex;align-items:flex-end;gap:var(--oa-space-200)}
.inword{display:flex;align-items:center;gap:6px;font:var(--oa-type-ui);margin:var(--oa-space-150) 0 var(--oa-space-100);background:var(--np);padding:var(--oa-space-100) var(--oa-space-150);width:max-content}
.x2{display:grid;gap:0}
.x2-row{display:grid;grid-template-columns:9rem repeat(var(--x2cols),max-content);gap:var(--oa-space-300);align-items:end;padding:var(--oa-space-150) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white)}
.x2-row--h{border-top:0;align-items:end}
.x2-c{min-width:0}
.naming ul{margin:var(--oa-space-100) 0 0;padding-left:1.1em;font:var(--oa-type-body-small)}.naming{margin-top:var(--oa-space-300)}
/* identity */
.vw-h{max-width:none;margin:var(--oa-space-300) 0 var(--oa-space-150)}
.em-cols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300)}
@media (min-width:72em){.em-cols{grid-template-columns:repeat(2,minmax(0,1fr))}}
.em-st{display:grid;gap:var(--oa-space-150);width:100%}
.em-lab{font:var(--oa-type-caption);color:var(--ink-2);margin:0 0 2px}
.enls{display:grid;gap:var(--oa-space-200)}
.enls--em{grid-template-columns:repeat(2,max-content);gap:var(--oa-space-200) var(--oa-space-600)}
.enl-col{display:grid;gap:var(--oa-space-200);align-content:start}
.fams--short{display:flex;flex-wrap:wrap}
.pg-rec{margin-left:var(--oa-space-100)}
.enl-row .col-h{margin-bottom:var(--oa-space-100)}
.enl-cells{display:flex;gap:var(--oa-space-300);align-items:flex-end}
.enl{margin:0}.enl figcaption{margin-top:var(--oa-space-050)}
.lks{display:grid;gap:var(--oa-space-200)}
.lk-st{display:flex;align-items:flex-end;gap:var(--oa-space-400)}
.lk{margin:0;display:flex;flex-direction:column;align-items:flex-start;gap:var(--oa-space-100)}
.lk figcaption{white-space:nowrap}
.l6s{display:grid;gap:var(--oa-space-300)}.l6{margin:0}
.tw{overflow-x:auto;border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);background:var(--white);margin-top:var(--oa-space-200)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
caption{caption-side:bottom;text-align:left;padding:var(--oa-space-150) var(--oa-space-200)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-100) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--oa-color-tint-white-n55)}
tbody th{font-weight:600}
td.num{text-align:center}
td.low span:first-child{display:inline-block;min-width:1.9em;border:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);font-weight:700}
table.sc-t{min-width:40rem}table.fig-t{min-width:36rem}
/* card foot: pick, approval, scores and the answer */
.card-foot{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-400) var(--oa-space-600);margin-top:var(--oa-space-500);border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);padding-top:var(--oa-space-300)}
@media (min-width:64em){.card-foot{grid-template-columns:minmax(0,1fr) minmax(17rem,22rem)}}
.rec .label,.approve .label{display:block;margin-bottom:2px}
.rec + .rec{margin-top:var(--oa-space-300)}
.rec--a11y{border-left:var(--oa-border-width-bar) solid var(--oa-color-border-strong-on-white);padding-left:var(--oa-space-200)}
.rec-o{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-100)}
.approve{margin-top:var(--oa-space-200)}
.scores{margin-top:var(--oa-space-300)}
.lowflag{font:var(--oa-type-body-small);margin:var(--oa-space-100) 0}
.why-d,.open-d{border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);margin-top:var(--oa-space-100)}
.why-d summary,.open-d summary{cursor:pointer;min-height:var(--oa-size-target-touch);display:flex;align-items:center;font:var(--oa-type-ui)}
.why-d ul,.open-d ul{margin:0 0 var(--oa-space-200);padding-left:1.1em;font:var(--oa-type-body-small)}.why-d li,.open-d li{margin:0 0 var(--oa-space-100)}
.rs-h{font:var(--oa-type-ui);font-weight:700;margin:var(--oa-space-150) 0 var(--oa-space-050)}
.rk{font-weight:600}
.ans{margin:0;padding:0;border:0;min-width:0}
@media (min-width:64em){.ans{border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding-left:var(--oa-space-400)}}
.ans legend{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;padding:0;float:left;width:100%;margin-bottom:var(--oa-space-100);color:var(--wink-2)}
.grp-o{clear:both;display:grid}
.glab{font:var(--oa-type-ui);font-weight:600;margin:var(--oa-space-100) 0 0}
.rad{display:flex;gap:var(--oa-space-150);align-items:center;min-height:var(--oa-size-target-touch);cursor:pointer}
.rad input{width:20px;height:20px;margin:0;flex:none;accent-color:var(--oa-color-palette-charcoal)}
.chk{margin-top:var(--oa-space-100);border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);font-weight:600}
.nl{display:block;font:var(--oa-type-body-small);color:var(--wink-2);margin:var(--oa-space-200) 0 var(--oa-space-100)}
textarea{display:block;width:100%;font:var(--oa-type-body);color:var(--oa-color-text-primary-on-white);background:var(--white);
  border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);border-radius:0;padding:var(--oa-space-150);resize:vertical}
/* reply */
.reply{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);padding:var(--oa-space-400) var(--oa-space-200)}
@media (min-width:48em){.reply{padding:var(--oa-space-500)}}
.reply h3{color:inherit;margin:0 0 var(--oa-space-200)}
.reply p{color:var(--oa-color-text-primary-on-prussian);max-width:var(--oa-layout-measure-intro-max)}
.reply .label{color:var(--oa-color-text-secondary-on-prussian);display:block;margin:var(--oa-space-300) 0 var(--oa-space-100)}
.ballot{list-style:none;margin:var(--oa-space-300) 0 0;padding:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-prussian)}
.bl{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-050) var(--oa-space-300);align-items:center;padding:var(--oa-space-100) 0;border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-prussian-n62)}
@media (min-width:56em){.bl{grid-template-columns:16rem minmax(0,1fr) auto}}
.bl-n{font:var(--oa-type-ui);font-weight:600;text-decoration:none;color:var(--oa-color-text-primary-on-prussian)}
.bl-n:hover{text-decoration:underline}.bl-n .n{color:var(--oa-color-text-secondary-on-prussian);display:inline-block;min-width:1.8em}
.bl-o{display:flex;flex-wrap:wrap;gap:var(--oa-space-100) var(--oa-space-300)}
.pgrp{display:inline-flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-100)}
.pg-l{font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-prussian)}
.pill{position:relative;display:inline-flex;cursor:pointer}
.pill input{position:absolute;opacity:0;width:100%;height:100%;margin:0;cursor:pointer}
.pill span{display:inline-flex;align-items:center;min-height:44px;min-width:44px;justify-content:center;padding:0 var(--oa-space-150);font:var(--oa-type-ui);
  border:var(--oa-border-width-hairline) solid var(--oa-color-palette-newsprint);color:var(--oa-color-text-primary-on-prussian)}
.pill input:checked + span{background:var(--oa-color-palette-newsprint);color:var(--oa-color-palette-charcoal);font-weight:700}
.pill input:focus-visible + span{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring-on-prussian);outline-offset:2px}
.pill--named span{white-space:nowrap}
.reply textarea{max-width:56rem;background:var(--np);color:var(--ink);border-color:var(--np);font:500 1rem/1.55 var(--mono)}
.reply-row{display:flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-200);margin-top:var(--oa-space-200)}
.reply button{font:var(--oa-type-ui);min-height:var(--oa-size-target-touch);padding:0 var(--oa-space-300);border:0;border-radius:0;cursor:pointer;
  background:var(--oa-color-action-primary-fill-on-prussian);color:var(--oa-color-action-primary-label-on-prussian)}
#copy-status{font:var(--oa-type-body-small);color:var(--oa-color-text-primary-on-prussian)}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media print{.toc,.ans,.reply,.hint{display:none!important}.frame{overflow:visible}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''

JS = r'''
(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  // Each drawing sits on whole CSS pixels, so a 1x screen draws it as its master is drawn (D2-565).
  function snap() {
    $$('.snap').forEach(function (el) { el.style.transform = ''; });
    $$('.snap').forEach(function (el) {
      var r = el.getBoundingClientRect(); if (!r.width) return;
      var dx = Math.round(r.left) - r.left, dy = Math.round(r.top + window.scrollY) - (r.top + window.scrollY);
      if (Math.abs(dx) > 0.001 || Math.abs(dy) > 0.001) el.style.transform = 'translate(' + dx.toFixed(3) + 'px,' + dy.toFixed(3) + 'px)';
    });
  }
  // A frame takes keyboard focus only while it is wider than the window and so needs scrolling.
  function frames() {
    $$('.frame').forEach(function (f) {
      var over = f.scrollWidth > f.clientWidth + 1;
      if (over) f.setAttribute('tabindex', '0'); else f.removeAttribute('tabindex');
      var h = f.nextElementSibling; if (h && h.classList.contains('hint')) h.hidden = !over;
    });
  }
  function layout() { frames(); snap(); }
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(layout, 120); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  window.addEventListener('load', layout);
  layout();
  // Answers. A card's own controls and its line in the reply panel share one store, saved in this browser only.
  var out = document.getElementById('reply-text');
  if (!out) return;
  var KEY = 'oa-stage-b-drawings-board:' + (document.querySelector('.board') || document.body).getAttribute('data-answers');
  var store = {};
  try { store = JSON.parse(window.localStorage.getItem(KEY) || '{}') || {}; } catch (e) { store = {}; }
  function save() { try { window.localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }
  var cards = $$('.card[data-card]');
  function rec(n) { var o = store[n]; if (!o) { o = store[n] = { g: {}, named: false, note: '' }; } if (!o.g) o.g = {}; return o; }
  function paint() {
    $$('input[type=radio][data-card]').forEach(function (r) { var s = store[r.getAttribute('data-card')]; r.checked = !!(s && s.g && s.g[r.getAttribute('data-group')] === r.value); });
    $$('input[type=checkbox][data-named]').forEach(function (k) { var s = store[k.getAttribute('data-named')]; k.checked = !!(s && s.named); });
    $$('textarea[data-note]').forEach(function (t) { var s = store[t.getAttribute('data-note')]; if (document.activeElement !== t) t.value = (s && s.note) || ''; });
  }
  function compose() {
    var lines = [];
    cards.forEach(function (c) {
      var n = c.getAttribute('data-card'), s = store[n]; if (!s) return;
      var parts = [], allRec = true, any = false;
      $$('.grp-o', c).forEach(function (g) {
        var name = g.getAttribute('data-group'), v = s.g && s.g[name];
        if (!v) { allRec = false; return; }
        any = true;
        var r = c.querySelector('input[type=radio][data-group="' + name + '"][value="' + v + '"]');
        parts.push(r ? r.getAttribute('data-short') : v);
        if (v !== g.getAttribute('data-rec')) allRec = false;
      });
      var line = parts.join(', ');
      if (any && allRec) line += ', as recommended';
      if (line) line += '.';
      if (s.named) line = (line ? line + ' ' : '') + 'Approved by name.';
      var note = (s.note || '').trim(); if (note) line = line ? line + ' ' + note : note;
      if (line) lines.push('Card ' + n + ', ' + c.getAttribute('data-short') + ': ' + line);
    });
    out.value = lines.length ? lines.join('\n') : out.getAttribute('data-sample');
  }
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches && t.matches('input[type=radio][data-card]')) { rec(t.getAttribute('data-card')).g[t.getAttribute('data-group')] = t.value; }
    else if (t.matches && t.matches('input[type=checkbox][data-named]')) { rec(t.getAttribute('data-named')).named = t.checked; }
    else return;
    save(); paint(); compose();
  });
  document.addEventListener('input', function (e) {
    var t = e.target; if (!(t.matches && t.matches('textarea[data-note]'))) return;
    rec(t.getAttribute('data-note')).note = t.value; save(); compose();
  });
  paint(); compose();
  var btn = document.getElementById('copy-reply'), st = document.getElementById('copy-status');
  btn.addEventListener('click', function () {
    var done = function () { st.textContent = 'Copied. Paste it into our chat.'; };
    var fall = function () { out.focus(); out.select(); try { document.execCommand('copy') ? done() : (st.textContent = 'Press Ctrl or Command and C to copy the selected reply.'); } catch (e) { st.textContent = 'Press Ctrl or Command and C to copy the selected reply.'; } };
    try { navigator.clipboard.writeText(out.value).then(done, fall); } catch (e) { fall(); }
  });
})();
'''


def build_page(model, C, S, built):
    cards = model['cards']
    html_cards = {}
    for c in cards:
        c['lede_html'] = lede(c, C)
        html_cards[c['n']] = RENDER[c['kind']](c, model, C)
    groups_html = ''
    for gk in ('civic', 'utility', 'pillars', 'identity'):
        G = C['groups'][gk]
        inner = ''.join(f'<li>{html_cards[c["n"]]}</li>' for c in cards if c['group'] == gk)
        groups_html += (f'<section class="sec" id="g-{gk}" aria-labelledby="g-{gk}-h"><h2 class="sec-h" id="g-{gk}-h">{esc(G["title"])}</h2>'
                        f'{paras(G.get("intro"), "intro")}<ol class="cards">{inner}</ol></section>')
    toc = ''.join(f'<li><a href="#card-{c["n"]}"><span class="n">{c["n"]}</span> {esc(c["short"])}</a></li>' for c in cards)
    toc += '<li><a href="#reply"><span class="n">→</span> Your reply</a></li>'
    legend = ''.join(f'<div><p><b>{esc(x["term"])}</b>{md(fill(x["text"]))}</p></div>' for x in C['legend'])
    answers_key = hashlib.sha1(json.dumps([(c['n'], c['short'], c['groups']) for c in cards], sort_keys=True, default=str).encode()).hexdigest()[:12]
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{TOKENS.read_text()}
{CSS}</style></head>
<body><main class="board" data-view-root="overview" data-answers="{answers_key}">
<header class="cover">
<p class="mast"><b>Oath &amp; Action</b><span class="label">{esc(C["kicker"])}</span></p>
<p class="label" style="margin-top:var(--oa-space-800)">For Dustin Cathcart · {words_date(built)}</p>
<h1>{esc(C["title"])}</h1>
<div class="cover-grid"><div><p class="intro">{md(fill(C["deck"]))}</p><div class="facts">{paras(C["facts"])}</div></div>
<div class="ask"><h2>What we ask of you</h2><ol>{"".join(f"<li>{md(fill(x))}</li>" for x in C["ask"])}</ol>
<p class="caption" style="margin:0 0 var(--oa-space-050)">A reply can be this short:</p><p class="q">{esc(C["sample_reply"])}</p></div></div>
<div class="legend"><h2>{esc(C["legend_title"])}</h2>{legend}</div>
<nav class="toc" aria-label="Cards on this board"><ol>{toc}</ol></nav>
</header>
{groups_html}
{reply_section(model, C)}
<p class="foot caption">Built {words_date(built)} at {words_time(built)} UTC by <code>work/build/scripts/phase-2/stage_b_drawings_board_build.py</code> from the makers’ manifests, notes and plate pages, the creative director’s scores and the engineer’s two checks run on today’s files.</p>
</main>
<script>{JS}</script></body></html>'''
    return page


def figures_json(model, built):
    out = {'built': built.isoformat(), 'thresholds': {'flag': model['like'].flag, 'watch': model['like'].watch},
           'likeness_run': model['checks']['likeness_run'], 'cards': []}
    for c in model['cards']:
        e = {'n': c['n'], 'kind': c['kind'], 'title': c['title'], 'groups': c['groups'], 'scores_under_4': c.get('lows', [])}
        subs = []
        for s in c.get('subjects', []):
            opts = []
            for o in s['options']:
                d = {'option': o.letter, 'like': o.like}
                for k in ('change', 'within', 'shows', 'pf24', 'pf16'):
                    if hasattr(o, k):
                        d[k] = getattr(o, k)
                for k in ('red', 'black', 'f24', 'f16'):
                    if hasattr(o, k):
                        d[k] = rel(getattr(o, k))
                d['naming_cd'] = o.cd
                d['naming_maker'] = o.maker
                opts.append(d)
            subs.append({'id': s['id'], 'options': opts})
        if subs:
            e['subjects'] = subs
        if c['kind'] == 'pillars':
            e['fits'] = [{'id': p['id'], 'fit': f['fit'], 'size_px': f['size_px'], 'line_px': f['line_px'], 'like': f['like'],
                          'pixel_fit_black': f['pf_black'], 'pixel_fit_red_black': f['pf_red']} for p in c['pillars'] for f in p['fits']]
        if c.get('fewer_reason'):
            e['fewer_reason'] = c['fewer_reason']
        out['cards'].append(e)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    for k in ('content', 'scores', 'out', 'publish', 'scratch'):
        ap.add_argument(f'--{k}', type=pathlib.Path, default=DEF[k])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--reuse-checks', action='store_true', help='reuse the last check results (layout work only)')
    a = ap.parse_args()
    C = load_json(a.content, 'the content file')
    eo = C.get('editor_overrides') or []
    need(isinstance(eo, list) and all(isinstance(x, dict) and isinstance(x.get('old'), str) and x['old'] and isinstance(x.get('new'), str)
                                      for x in eo), 'content.editor_overrides: a list of {"old": "exact text", "new": "replacement"}')
    OVERRIDES[:] = [[x['old'], x['new'], 0] for x in eo]
    S = ov_deep(load_json(a.scores, 'the scores file'))
    need(isinstance(S.get('cards'), list), 'scores: no cards')
    need('—' not in json.dumps(C, ensure_ascii=False), 'content: an em dash (W21)')
    model = build_model(C, S, a.scratch, a.reuse_checks)
    number_cards(model, C)
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL.update({'built_date': words_date(built), 'built_time': words_time(built)})
    page = build_page(model, C, S, built)
    page = re.sub(r'(<(p|span|legend|th)\b[^>]*?(?:class="[^"]*\b(?:label|vw-h)\b[^"]*"|scope="col")[^>]*>|<legend>)(.*?)(</(?:p|span|legend|th)>)',
                  lambda m: m.group(1) + (m.group(3) if 'class="nc"' in m.group(3) else nx(m.group(3))) + m.group(4), page, flags=re.S)
    for o in OVERRIDES:
        if not o[2]:
            warn(f'editor override matches nothing in the makers\' files, the scores or the audit: "{o[0][:70]}"')
    # words on the board: no em dash, en dashes and flagged words warn, the tagline exact
    text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)))
    need('—' not in text, 'em dash on the board: ' + text[max(0, text.find('—') - 60):text.find('—') + 20])
    if '–' in text.replace('<td class="num"><span>–', ''):
        warn('an en dash on the board')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text, flags=re.I)})
    if flagged:
        warn('flagged words on the board: ' + ', '.join(flagged))
    if 'answers to its people' in text and TAGLINE not in text.replace('’', "'"):
        raise BoardError('the tagline is quoted inexactly (H01)')
    # the repository copy: files by path relative to the board
    out_dir = a.out.parent

    def resolve(prefix_fn):
        return re.sub(r'@@A:([^@]+)@@', lambda m: prefix_fn(m.group(1)), page)
    repo_page = resolve(lambda k: os.path.relpath(ROOT / k, out_dir).replace(os.sep, '/'))
    a.out.write_text(repo_page)
    # a check copy for dataviz_check.js with captures in the scratchpad: the same page with absolute file links
    chk_dir = a.scratch / 'check-copy'
    chk_dir.mkdir(parents=True, exist_ok=True)
    chk_page = resolve(lambda k: 'file://' + str(ROOT / k))
    (chk_dir / a.out.name).write_text(chk_page)
    # sizes
    refs = sorted(ASSET_REFS)
    names = {}
    for r in refs:
        b = pathlib.Path(r).name
        need(b not in names or names[b] == r, f'two files share the name {b}: {names.get(b)} and {r}')
        names[b] = r
    img_bytes = sum((ROOT / r).stat().st_size for r in refs)
    total = len(repo_page.encode()) + img_bytes
    if total > 15_000_000:
        warn(f'the board and its files come to {total / 1e6:.1f} MB, close to the 16 MB limit')
    need(total < LIMIT, f'the board and its files come to {total / 1e6:.1f} MB, over 16 MB')
    # every drawing the cards name is on the page
    for c in model['cards']:
        for s in c.get('subjects', []):
            for o in s['options']:
                for k in ('red', 'f24'):
                    if hasattr(o, k):
                        need(rel(getattr(o, k)) in ASSET_REFS or k == 'f24', f'card {c["n"]}: {getattr(o, k).name} is not on the page')
    # the publish copy: no document skeleton, files under img/ (D2-317)
    pub = resolve(lambda k: 'img/' + pathlib.Path(k).name)
    head, body = re.split(r'</head>\s*<body>', pub, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace(f'<title>{TITLE}</title>\n', '')
    body = re.sub(r'</body>\s*</html>\s*$', '', body)
    setup = '<script>document.documentElement.lang="en";</script>'
    a.publish.mkdir(parents=True, exist_ok=True)
    pdir = a.publish / 'img'
    if pdir.exists():
        shutil.rmtree(pdir)
    pdir.mkdir(parents=True)
    files = {}
    for r in refs:
        b = pathlib.Path(r).name
        shutil.copy2(ROOT / r, pdir / b)
        files[f'img/{b}'] = str(pdir / b)
    pub_html = a.publish / a.out.name
    pub_html.write_text(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + setup + body)
    (a.publish / 'files.json').write_text(json.dumps(files, indent=1))
    figs = figures_json(model, built)
    (out_dir / f'{DATE}_Stage-B-Drawings-Board-Figures.json').write_text(json.dumps(figs, indent=1, default=str))
    print(f'wrote {rel(a.out)} ({len(repo_page.encode()) / 1e3:.0f} kB) with {len(refs)} files ({img_bytes / 1e6:.2f} MB): '
          f'{total / 1e6:.2f} MB in all; {len(model["cards"])} cards')
    print(f'wrote {pub_html} and {len(files)} files in {pdir}; publish map in {a.publish / "files.json"}')
    print(f'wrote the check copy {chk_dir / a.out.name}')
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
