"""Build drawings board C (November 10, 2026): the Housing options, the 16 px Pause and Filter redraws, the 24 px fits for
the 37 topic and atlas drawings, and the identity designer's two proposals (a print L3 and the social sign-off at 96 px),
each at true size for Dustin's approval by name (DR-139, DR-196 to DR-198, DR-205, D2-482, D2-715).

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_drawings_board_build.py [--strict] [--reuse-checks]
        [--content PATH] [--scores PATH] [--out PATH] [--publish DIR] [--scratch DIR]

Reads, on every run (no option list, figure or file name of a drawing is written into this script):
    work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board-Content.json   the board's own words
    work/boards/phase-2/stage-c/drawings/20261110_CD-Scores.json                          scores, picks, readings; if it
                                                                                          is missing, cards say "scores pending"
    work/build/assets/civic-line-24-fit/*Manifest.json, utility-16-redraw/*Manifest.json,
    civic-line-new-topics/*Housing-Manifest.json                                          the drawings and their files
    work/build/assets/civic-line-v6/*Inventory.json and black/, utility/svg-16/          the masters and approved files
    work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md, section 10              the 37, in order
    work/handoffs/phase-2/20261110_Stage-C-Drawings-Notes.md and -Identity-Round-0-Notes.md   the designers' questions
                                                                                          (their recommended answers only)
    work/handoffs/phase-2/20261110_Stage-C-Identity-Figures.json and stage-c-identity/    identity figures, plates, captures
Runs, on today's files (every drawings figure on the board is this run's, not copied from the notes):
    icon_likeness_check.js   the 37 fits against the 124 drawings in use and each other (every pair listed); the five
                             look-alikes' masters and any master a fit is flagged beside, under neutral names; the three
                             Housing options
    icon_pixel_fit_check.js  the 37 fits at 24 px with a 1 px line, the 37 masters at 24 px (full ink), and the approved
                             and redrawn Pause and Filter at 16 px with a 1.5 px line
    Chromium (Playwright)    pictures at device scale 1 and 2 of the masters, fits, Pause, Filter and Housing, and the
                             identity plate's social cards at actual size; the open pixels counted from the 1x pictures
Writes:
    work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board.html          the board (files by relative path)
    work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board-Figures.json  every figure the board prints
    work/boards/phase-2/stage-c/drawings/renders/                                       the board's own pictures
    <scratch>/check-copy/ the board with absolute file links, for dataviz_check.js with captures in the scratchpad
    <publish>/20261110_Stage-C-Drawings-Board.html, <publish>/img/ and <publish>/files.json, the publish copy

Drawings at their own true size draw from their SVG files (D2-617); a small script moves each onto whole CSS pixels
(D2-565). A view that claims to show what a 1x screen draws is a PNG made at device scale 1 and set at its own CSS size
with image-rendering: pixelated; a 2x picture is set at its own size too, twice the drawing's, and says so.
--strict exits 1 on any warning, among them "scores pending".
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
from collections import deque

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261110'
BOARD_DIR = ROOT / 'work/boards/phase-2/stage-c/drawings'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/board')
ASSETS = ROOT / 'work/build/assets'
HANDOFFS = ROOT / 'work/handoffs/phase-2'
SCRIPTS = ROOT / 'work/build/scripts/phase-2'
STEM = f'{DATE}_Stage-C-Drawings-Board'
DEF = {
    'content': BOARD_DIR / f'{STEM}-Content.json',
    'scores': BOARD_DIR / f'{DATE}_CD-Scores.json',
    'out': BOARD_DIR / f'{STEM}.html',
    'publish': SCRATCH / 'publish',
    'scratch': SCRATCH,
}
RENDERS = BOARD_DIR / 'renders'
SRC = {
    'fits': ASSETS / 'civic-line-24-fit',
    'redraw': ASSETS / 'utility-16-redraw',
    'topics': ASSETS / 'civic-line-new-topics',
    'v6': ASSETS / 'civic-line-v6',
    'identity': ASSETS / 'identity',
    'id_plates': HANDOFFS / 'stage-c-identity',
    'id_figs': HANDOFFS / f'{DATE}_Stage-C-Identity-Figures.json',
    'icon_notes': HANDOFFS / f'{DATE}_Stage-C-Drawings-Notes.md',
    'id_notes': HANDOFFS / f'{DATE}_Stage-C-Identity-Round-0-Notes.md',
    'ch10': HANDOFFS / f'{DATE}_Stage-B-Ch10-Construction.md',
    'ch08': ROOT / 'work/build/guide/chapters/08-lockmark.json',
}
TOKENS = ROOT / 'work/build/tokens/tokens.css'
LIKENESS_JS = SCRIPTS / 'icon_likeness_check.js'
PIXELFIT_JS = SCRIPTS / 'icon_pixel_fit_check.js'
TITLE = 'Stage C Drawings Board'
RUBRIC = [('craft', 'Craft'), ('clarity', 'Clarity'), ('brand_fidelity', 'Brand fidelity'), ('usefulness', 'Usefulness'),
          ('evidence_honesty', 'Evidence honesty'), ('accessibility', 'Accessibility')]
RUBRIC_SHORT = {'brand_fidelity': 'Brand', 'evidence_honesty': 'Evidence'}
CARD_ORDER = ['housing', 'utility', 'fits', 'print_l3', 'social']
GROUP_OF = {'housing': 'drawings', 'utility': 'drawings', 'fits': 'drawings', 'print_l3': 'identity', 'social': 'identity'}
# which scores-file cards belong to which board card, matched on their id and title
SCORE_KEYS = [('housing', r'housing'), ('utility', r'pause|filter|16 ?px'), ('print_l3', r'\bl3\b|print'),
              ('social', r'social|sign[- ]?off'), ('fits', r'\b37\b|24 ?px fit|\bfits?\b')]
LOOK_ALIKES = ['CL-023', 'CL-028', 'R-08', 'R-27', 'R-45']     # D2-971, the five that draw as one shape at 24 px
HOUSING_SIZES = [128, 48, 24]
FIT_PX = 24
UT_PX = 16
GRID_MAG = 10
NP, CH = '#DCD9D2', '#121212'
TAGLINE = 'A country that answers to its people.'
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat']
LIMIT = 15_000_000
WARN = []
NOTICES = []
OVERRIDES = []


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
        return obj if key in ('id', 'option', 'file', 'svg') or re.fullmatch(r'[\w./-]+\.(svg|png|json|html|md|pdf)', obj) else ov(obj)
    if isinstance(obj, dict):
        return {k: ov_deep(v, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [ov_deep(v, key) for v in obj]
    return obj


# ------------------------------------------------------------------------------------------------ text
def copy(s):
    """Curly quotes and apostrophes, and the true minus before a figure."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    s = re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", '‘\\1’', s)
    return re.sub(r'(?<![\w.\-/])-(?=\d)', '−', s)


def esc(s):
    return html.escape(copy(s), quote=True)


def attr(s):
    return html.escape(str(s), quote=True)


N_CARDS = 0
FILL = {}


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


def fill(s, extra=None):
    """Content words with {flag} and the like filled in by the build."""
    d = dict(FILL)
    if extra:
        d.update(extra)
    try:
        return str(s).format_map(d)
    except (KeyError, IndexError, ValueError) as e:
        raise BoardError(f'content text names an unknown value {e}: {str(s)[:90]}')


def paras(x, cls='', extra=None):
    items = x if isinstance(x, list) else [x] if x else []
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<p{c}>{md(fill(p, extra))}</p>' for p in items)


def words_date(d):
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def words_time(d):
    h = d.hour % 12 or 12
    return f'{h}:{d.minute:02d} {"a.m." if d.hour < 12 else "p.m."}'


def num_words(n):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'][n] if 0 <= n <= 10 else f'{n:,}'


def join_words(items):
    items = list(items)
    if len(items) < 3:
        return ' and '.join(items)
    return ', '.join(items[:-1]) + ' and ' + items[-1]


def png_size(p):
    with open(p, 'rb') as f:
        d = f.read(24)
    return struct.unpack('>II', d[16:24])


def fmt_like(v):
    return f'{v:.3f}' if v < 1 else '1'


def fmt_pct(x):
    if x is None:
        return 'not measured'
    v = 100 * x
    if abs(v - round(v)) < 0.05:
        return f'{round(v)}%'
    return f'{v:.1f}%'


def fmt_g(v, nd=1):
    return f'{v:.{nd}f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)


# ------------------------------------------------------------------------------------------------ inputs
def load_json(p, what):
    need(pathlib.Path(p).exists(), f'{what} not found: {p}')
    try:
        return json.loads(pathlib.Path(p).read_text())
    except json.JSONDecodeError as e:
        raise BoardError(f'{what} does not parse ({e}); its owner may be writing it, so rerun once it is saved')


def one_file(folder, pattern, what):
    found = sorted(folder.glob(pattern))
    need(found, f'{what}: nothing matches {pattern} in {rel(folder)}')
    if len(found) > 1:
        warn(f'{what}: {len(found)} files match {pattern}; reading the newest, {found[-1].name}')
    return found[-1]


def md_tables(text):
    """Every Markdown table in a notes file as a list of rows {header: cell}, in file order."""
    out = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|\s*$', lines[i + 1]):
            head = [h.strip() for h in ln.strip().strip('|').split('|')]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(dict(zip(head, cells)))
                i += 1
            out.append({'head': head, 'rows': rows})
            continue
        i += 1
    return out


def section_text(text, pattern):
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
    s = re.sub(r'\*(.+?)\*', r'\1', s)
    return s.strip()


def letter_of(s):
    m = re.match(r'^\s*(?:Option\s+|Fit\s+|Redraw\s+)?([A-Z])\b', str(s))
    return m.group(1) if m else None


def fits_list(text):
    """The 37 of chapter 10's section 10, in order: (ID, Civic Line word, atlas ID)."""
    sec = section_text(text, r'^10\.')
    need(sec, f'{SRC["ch10"].name}: no section 10')
    for t in md_tables(sec):
        h = t['head']
        if h and h[0] == 'ID' and len(h) >= 3:
            return [(r[h[0]], r[h[1]], r[h[2]]) for r in t['rows']]
    raise BoardError(f'{SRC["ch10"].name}: no table of the 37 in section 10')


def designer_questions(text):
    """A designer's numbered questions for Dustin: title, words and the recommended answer, as written."""
    sec = section_text(text, r'questions for dustin')
    out = []
    for m in re.finditer(r'^(\d+)\.\s+\*\*(.+?)\*\*(.*?)(?=^\d+\.\s+\*\*|\Z)', sec, flags=re.M | re.S):
        body = m.group(3)
        r = re.search(r'\*Recommendation:\*\s*(.+)', body, flags=re.S)
        out.append({'n': int(m.group(1)), 'title': strip_md(m.group(2)), 'text': strip_md(body.split('*Recommendation:*')[0]),
                    'recommendation': strip_md(r.group(1)) if r else ''})
    return out


# ------------------------------------------------------------------------------------------------ node helpers
RENDER_JS = r'''
// Pictures for drawings board C: an SVG drawn inline at its CSS size and a device scale, as the pixel-fit check draws
// it, or one element of a page screenshot at a device scale. usage: node render.js jobs.json results.json
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const res = [];
  const b = await chromium.launch();
  const ctx = new Map();
  const page = async (dpr, w) => {
    const k = dpr + ':' + w;
    if (!ctx.has(k)) { const c = await b.newContext({ deviceScaleFactor: dpr, viewport: { width: w, height: 900 } }); ctx.set(k, await c.newPage()); }
    return ctx.get(k);
  };
  try {
    for (const j of jobs) {
      if (j.kind === 'svg') {
        const p = await page(j.dpr, 400);
        let t = fs.readFileSync(j.file, 'utf8').replace(/<\?xml[^>]*>\s*/, '');
        t = t.replace(/<svg\b([^>]*)>/, (m, a) => '<svg' + a.replace(/\s(width|height)="[^"]*"/g, '') + ` width="${j.size}" height="${j.size}">`);
        await p.setViewportSize({ width: Math.max(j.size, 16), height: Math.max(j.size, 16) });
        await p.setContent(`<!doctype html><html><body style="margin:0;background:${j.bg || 'transparent'}"><div style="position:absolute;left:0;top:0;line-height:0;color:${j.color}">${t}</div></body></html>`);
        await p.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.size, height: j.size }, omitBackground: !j.bg, animations: 'disabled' });
        res.push({ out: j.out });
      } else if (j.kind === 'element') {
        const p = await page(j.dpr, j.vw || 1380);
        await p.goto('file://' + j.html, { waitUntil: 'load' });
        await p.evaluate(() => document.fonts.ready);
        await p.waitForTimeout(300);
        const fonts = await p.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '') + ' ' + f.weight));
        const els = await p.$$(j.selector);
        if (!els[j.index]) { res.push({ out: j.out, error: 'no element ' + j.selector + ' #' + j.index }); continue; }
        const info = await els[j.index].evaluate((e) => {
          let n = e.parentElement; let h = n.previousElementSibling;
          while (h && h.tagName !== 'H2') h = h.previousElementSibling;
          const r = e.getBoundingClientRect();
          return { heading: h ? h.textContent : null, w: r.width, h: r.height, x: r.left + window.scrollX, y: r.top + window.scrollY };
        });
        // the element's own box on whole CSS pixels, so the picture is exactly its size at this device scale
        await p.screenshot({ path: j.out, fullPage: true, animations: 'disabled',
          clip: { x: Math.round(info.x), y: Math.round(info.y), width: Math.round(info.w), height: Math.round(info.h) } });
        res.push({ out: j.out, fonts, ...info });
      }
    }
  } finally { await b.close(); }
  fs.writeFileSync(process.argv[3], JSON.stringify(res, null, 1));
})();
'''


def node_env():
    env = dict(os.environ)
    if 'NODE_PATH' not in env and os.path.isdir('/opt/node-tools/node_modules'):
        env['NODE_PATH'] = '/opt/node-tools/node_modules'
    elif os.path.isdir('/opt/node-tools/node_modules') and '/opt/node-tools/node_modules' not in env['NODE_PATH']:
        env['NODE_PATH'] = env['NODE_PATH'] + os.pathsep + '/opt/node-tools/node_modules'
    return env


def render(jobs, scratch, tag):
    if not jobs:
        return []
    d = scratch / 'render'
    d.mkdir(parents=True, exist_ok=True)
    js = d / 'render.js'
    js.write_text(RENDER_JS)
    jp, rp = d / f'jobs-{tag}.json', d / f'results-{tag}.json'
    jp.write_text(json.dumps(jobs))
    for j in jobs:
        pathlib.Path(j['out']).parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(['node', str(js), str(jp), str(rp)], cwd=ROOT, capture_output=True, text=True, timeout=900, env=node_env())
    need(r.returncode == 0 and rp.exists(), f'the renderer failed ({tag}): {(r.stderr or r.stdout)[-800:]}')
    return json.loads(rp.read_text())


# ------------------------------------------------------------------------------------------------ the checks
def run_checks(I, scratch, reuse):
    """The engineer's two checks on today's files. Independent runs go in parallel; the neutral-name run of the masters
    follows the fits' run, since it takes in any master a fit is flagged beside."""
    cdir = scratch / 'checks'
    cdir.mkdir(parents=True, exist_ok=True)
    fits = [ROOT / f['svg'] for f in I['fit_rows']]
    masters = [f['master_path'] for f in I['fit_rows']]
    housing = [ROOT / o['svg']['black'] for o in I['housing']['options']]
    util = [u['path'] for u in I['util_files']]
    runs = {
        'likeness_fits': [str(LIKENESS_JS), *map(str, fits), '--watch', '0.01', '--json', str(cdir / 'likeness-fits.json'), '--quiet'],
        'likeness_housing': [str(LIKENESS_JS), *map(str, housing), '--watch', '0.01', '--json', str(cdir / 'likeness-housing.json'), '--quiet'],
        'pixel_fit_fits': [str(PIXELFIT_JS), '--size', str(FIT_PX), '--weight', '1', '--quiet', '--json', str(cdir / 'pixel-fit-fits.json'), *map(str, fits)],
        'pixel_fit_masters': [str(PIXELFIT_JS), '--size', str(FIT_PX), '--quiet', '--json', str(cdir / 'pixel-fit-masters.json'), *map(str, masters)],
        'pixel_fit_utility': [str(PIXELFIT_JS), '--size', str(UT_PX), '--weight', '1.5', '--quiet', '--json', str(cdir / 'pixel-fit-utility.json'), *map(str, util)],
    }
    outs = {k: pathlib.Path(v[v.index('--json') + 1]) for k, v in runs.items()}
    codes = {}
    if reuse:
        warn('check results reused from an earlier run (--reuse-checks)')
        for k, p in outs.items():
            need(p.exists(), f'--reuse-checks: no earlier {k} results')
        codes = json.loads((cdir / 'exit-codes.json').read_text()) if (cdir / 'exit-codes.json').exists() else {}
    else:
        procs = {}
        for k, args in runs.items():
            if outs[k].exists():
                outs[k].unlink()
            procs[k] = subprocess.Popen(['node', *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=node_env())
        for k, p in procs.items():
            so, se = p.communicate(timeout=1800)
            codes[k] = p.returncode
            need(p.returncode in (0, 1) and outs[k].exists(), f'{k} failed to run: {(se or so)[-800:]}')
    R = {k: load_json(p, k) for k, p in outs.items()}
    # the masters' own figures for the pairs the board prints: the five look-alikes and any master a fit is flagged
    # beside, copied under neutral names so the check compares them as new drawings, every pair listed
    flag = R['likeness_fits']['thresholds']['flag']['likeness']
    fit_id = {pathlib.Path(f['svg']).name: f['id'] for f in I['fit_rows']}
    want = list(LOOK_ALIKES)
    for x in R['likeness_fits']['flagged']:
        if x.get('against') == 'master':
            for i in (fit_id[x['a']], x['b'].split()[0]):
                if i not in want:
                    want.append(i)
    nd = cdir / 'neutral-masters'
    np_json = cdir / 'likeness-neutral-masters.json'
    neutral = {}
    for i in want:
        neutral[f'Neutral-{I["inv"][i]["slug"]}.svg'] = i
    if not reuse:
        shutil.rmtree(nd, ignore_errors=True)
        nd.mkdir(parents=True)
        for n, i in neutral.items():
            shutil.copyfile(I['master_path'](i), nd / n)
        if np_json.exists():
            np_json.unlink()
        r = subprocess.run(['node', str(LIKENESS_JS), str(nd), '--watch', '0.01', '--json', str(np_json), '--quiet'],
                           cwd=ROOT, capture_output=True, text=True, timeout=1800, env=node_env())
        codes['likeness_neutral_masters'] = r.returncode
        need(r.returncode in (0, 1) and np_json.exists(), f'the neutral masters run failed: {(r.stderr or r.stdout)[-800:]}')
        (cdir / 'exit-codes.json').write_text(json.dumps(codes, indent=1))
    else:
        need(np_json.exists(), '--reuse-checks: no earlier neutral masters results')
    R['likeness_neutral_masters'] = load_json(np_json, 'neutral masters likeness')
    R['neutral'] = neutral
    R['codes'] = codes
    R['commands'] = {k: 'node ' + ' '.join(rel(a) if a.startswith(str(ROOT)) else a for a in v) for k, v in runs.items()}
    R['commands']['likeness_neutral_masters'] = f'node {rel(LIKENESS_JS)} <{len(neutral)} masters copied under neutral names> --watch 0.01'
    R['files'] = {k: str(p) for k, p in outs.items()} | {'likeness_neutral_masters': str(np_json)}
    return R


# ------------------------------------------------------------------------------------------------ measures
def full_ink(r, scale='1x'):
    s = r['scales'][scale]['soft_edges']
    ink, part = s['ink_px'], s['partial_px']
    return {'share': (ink - part) / ink if ink else None, 'full_px': ink - part, 'ink_px': ink}


PF_WORDS = {'no ink': 'it draws no ink', 'width': 'a line is under one device pixel', 'soft': 'most of its pixels are soft',
            'straight': 'a straight edge sits off the pixel grid', 'gap': 'a gap is under one device pixel',
            'counters': 'an enclosed space fills in', 'weight': 'its main line differs from the set’s'}


def pf_words(r, size):
    if r is None:
        return 'Not run'
    if r['pass']:
        return f'Passes at {size} px, 1x and 2x'
    by = {}
    for sc in ('1x', '2x'):
        for c in r['scales'][sc]['fails']:
            by.setdefault(c, []).append(sc)
    return f'Fails at {size} px: ' + '; '.join(f'{PF_WORDS.get(c, c)} at {join_words(s)}' for c, s in by.items())


def counters_hi(path, K):
    """Enclosed spaces in a picture drawn at K device pixels per pixel: low-ink pixels the page's edge cannot reach."""
    from PIL import Image
    im = Image.open(path).convert('RGBA')
    W, H = im.size
    A = im.getchannel('A').load()
    lab = [[0] * W for _ in range(H)]
    q = deque()
    for x in range(W):
        for y in (0, H - 1):
            if A[x, y] < 128 and not lab[y][x]:
                lab[y][x] = -1
                q.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if A[x, y] < 128 and not lab[y][x]:
                lab[y][x] = -1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for u, v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= u < W and 0 <= v < H and not lab[v][u] and A[u, v] < 128:
                lab[v][u] = -1
                q.append((u, v))
    comps = []
    for y in range(H):
        for x in range(W):
            if not lab[y][x] and A[x, y] < 128:
                pts = []
                lab[y][x] = len(comps) + 1
                q.append((x, y))
                while q:
                    a, b = q.popleft()
                    pts.append((a, b))
                    for u, v in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= u < W and 0 <= v < H and not lab[v][u] and A[u, v] < 128:
                            lab[v][u] = lab[y][x]
                            q.append((u, v))
                if len(pts) >= K * K / 2:
                    comps.append(pts)
    return comps


def open_pixels(lo_path, hi_path, K, S):
    """For each enclosed space: the rows of pixels where it runs at its narrowest between straight sides (inside a bar,
    down a spout), and on how many of those rows a 1x screen leaves a pixel fully open (alpha under 8)."""
    from PIL import Image
    lo = Image.open(lo_path).convert('RGBA').getchannel('A').load()
    out = []
    for comp in sorted(counters_hi(hi_path, K), key=lambda c: min(p[0] for p in c)):
        by = {}
        for x, y in comp:
            by.setdefault(y, []).append(x)
        rows = []
        for r in range(S):
            sub = [by.get(r * K + i) for i in range(K)]
            if not all(sub):
                continue
            width = max(max(s) - min(s) + 1 for s in sub) / K
            cols = sorted({x // K for i in range(K) for x in by[r * K + i]})
            rows.append({'row': r, 'width_px': round(width, 3), 'alpha': [lo[c, r] for c in cols], 'cols': cols})
        if not rows:
            continue
        narrow = min(x['width_px'] for x in rows)
        band = [x for x in rows if x['width_px'] <= narrow + 0.1]
        opened = [x for x in band if any(a < 8 for a in x['alpha'])]
        mid = min(band, key=lambda x: (abs(x['row'] - S // 2), x['row']))
        out.append({'rows': [band[0]['row'], band[-1]['row']], 'n_rows': len(band), 'rows_open': len(opened),
                    'width_px': narrow, 'mid_row': mid['row'], 'mid_alpha': mid['alpha'],
                    'open_per_row': sorted({sum(1 for a in x['alpha'] if a < 8) for x in band})})
    return out


# ------------------------------------------------------------------------------------------------ scores
def score_cards(S):
    """The scores file's cards, sorted to the board's cards by their id and title."""
    out = {k: [] for k in CARD_ORDER}
    if not S:
        return out
    for c in S.get('cards', []):
        key = f'{c.get("id", "")} {c.get("title", "")}'.lower()
        for k, pat in SCORE_KEYS:
            if re.search(pat, key):
                out[k].append(c)
                break
        else:
            warn(f'the scores file holds a card the board does not show: {c.get("id") or c.get("title")}')
    return out


def verdict_text(x):
    if isinstance(x, str):
        return x.strip()
    if not isinstance(x, dict):
        return ''
    v = x.get('verdict') or x.get('creative_director_verdict') or x.get('cd_verdict') or x.get('reading') or ''
    n = x.get('note') or x.get('notes') or x.get('reason') or ''
    if isinstance(v, dict):
        v = v.get('text') or v.get('verdict') or ''
    v, n = str(v).strip(), str(n).strip() if isinstance(n, str) else ''
    if v and n and n.lower() not in v.lower():
        return f'{v.rstrip(".")}. {n}'
    return v or n


def row_verdicts(cards, ids):
    """The creative director's verdict on each of the 37, wherever the scores card keeps them: a list of entries with an
    id, or a map keyed by id."""
    out = {}

    def visit(o, depth=0):
        if depth > 6:
            return
        if isinstance(o, dict):
            hits = [k for k in o if k in ids]
            if len(hits) >= 3:
                for k in hits:
                    v = verdict_text(o[k])
                    if v:
                        out.setdefault(k, v)
            idv = o.get('id') or o.get('drawing') or o.get('icon')
            if isinstance(idv, str):
                m = re.match(r'((?:CL|R)-\d+)', idv)
                if m and m.group(1) in ids and depth > 0:
                    v = verdict_text(o)
                    if v:
                        out.setdefault(m.group(1), v)
            for k, v in o.items():
                if k not in ('scores',):
                    visit(v, depth + 1)
        elif isinstance(o, list):
            for v in o:
                visit(v, depth + 1)
    for c in cards:
        visit(c)
    return out


def option_scores(cards):
    """Per-option scores, from an option_scores map in a scores card, or options that carry their own scores."""
    out = {}
    for c in cards:
        for k, v in (c.get('option_scores') or {}).items():
            if isinstance(v, dict):
                out[str(k)] = {'scores': v, 'must_fix': [], 'ready_for_board': c.get('ready_for_board')}
        for o in c.get('options', []) or []:
            if isinstance(o, dict) and o.get('scores') and str(o.get('option')) not in out:
                out[str(o.get('option'))] = o
    return out


def cd_rec_text(cards):
    for c in cards:
        r = (c.get('recommended') or {})
        if r.get('option') or r.get('reason'):
            return str(r.get('option', '')), str(r.get('reason', ''))
    return None, None


def cd_naming(cards, letter):
    for c in cards:
        for n in c.get('naming_test', []) or []:
            if str(n.get('option')) == letter or letter_of(n.get('option')) == letter:
                return n
    return None


# ------------------------------------------------------------------------------------------------ page parts
ASSET_REFS = {}
INLINE_N = [0]


def src(p):
    p = pathlib.Path(p).resolve()
    need(p.exists(), f'the board shows {p}, which does not exist')
    k = rel(p)
    ASSET_REFS[k] = True
    return f'@@A:{k}@@'


def img(p, w, h, alt, cls='', srcset2x=None, px=False):
    ss = f' srcset="{src(p)} 1x, {src(srcset2x)} 2x"' if srcset2x else ''
    c = ' '.join(x for x in ('snap', cls, 'px' if px else '') if x)
    return (f'<img class="{c}" src="{src(p)}"{ss} width="{fmt_g(float(w), 2)}" height="{fmt_g(float(h), 2)}" alt="{attr(copy(alt))}" '
            f'loading="eager" decoding="async">')


def inline_svg(p, w, h, cls='', style='', label=None):
    """An SVG file drawn inline at w by h px, so it takes currentColor and the page's custom properties."""
    t = pathlib.Path(p).read_text()
    t = re.sub(r'<\?xml[^>]*>|<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<title>.*?</title>|<desc>.*?</desc>', '', t, flags=re.S)
    ids = re.findall(r'\sid="([^"]+)"', t)
    if ids:
        INLINE_N[0] += 1
        for i in ids:
            j = f'{i}-i{INLINE_N[0]}'
            t = t.replace(f'id="{i}"', f'id="{j}"').replace(f'url(#{i})', f'url(#{j})').replace(f'href="#{i}"', f'href="#{j}"')
    m = re.search(r'<svg\b([^>]*)>', t)
    need(m, f'{p}: no <svg> element')
    a = re.sub(r'\s(width|height|class|style|aria-hidden|focusable|role)="[^"]*"', '', m.group(1))
    lab = f' role="img" aria-label="{attr(copy(label))}"' if label else ' aria-hidden="true"'
    st = f' style="{style}"' if style else ''
    head = f'<svg{a} width="{fmt_g(float(w), 3)}" height="{fmt_g(float(h), 3)}" class="snap {cls}" focusable="false"{lab}{st}>'
    return (t[:m.start()] + head + t[m.end():]).strip()


def nx(h):
    return re.sub(r'\b([123])x\b', r'<span class="nc">\1x</span>', h)


def chip(t, cls=''):
    return f'<span class="chip{" " + cls if cls else ""}">{nx(esc(t))}</span>'


def dl(rows, cls='figs'):
    return f'<dl class="{cls}">' + ''.join(f'<div><dt>{nx(esc(k))}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


def frame(inner, name):
    return (f'<div class="frame" role="region" tabindex="0" aria-label="{attr(copy(name))}, true size">{inner}</div>'
            f'<p class="hint caption" hidden>Wider than this window. Scroll sideways inside the frame to see all of it at true size.</p>')


def scores_block(subjects, title='The creative director’s scores, 1 to 5'):
    rows, reasons, lows = '', '', []
    for name, sc in subjects:
        if not sc or not sc.get('scores'):
            rows += f'<tr><th scope="row">{esc(name)}</th><td colspan="6">Pending</td></tr>'
            continue
        cells = ''
        for k, lab in RUBRIC:
            x = (sc.get('scores') or {}).get(k) or {}
            v = x.get('score') if isinstance(x, dict) else x
            low = isinstance(v, (int, float)) and v < 4
            if low:
                lows.append(f'{name}, {lab.lower()} {v}')
            cells += (f'<td class="num{" low" if low else ""}"><span>{v if v is not None else "–"}</span>'
                      f'{"<span class=vh> (under 4)</span>" if low else ""}</td>')
        rows += f'<tr><th scope="row">{esc(name)}</th>{cells}</tr>'
        li = ''
        for k, lab in RUBRIC:
            x = (sc.get('scores') or {}).get(k) or {}
            if isinstance(x, dict):
                li += f'<li><span class="rk">{esc(lab)} {x.get("score", "")}</span> {esc(x.get("reason", ""))}</li>'
        reasons += f'<p class="rs-h">{esc(name)}</p><ul>{li}</ul>'
    head = ''.join(f'<th scope="col">{esc(RUBRIC_SHORT.get(k, lab))}</th>' for k, lab in RUBRIC)
    flag = (f'<p class="lowflag"><span class="chip chip--low">Under 4</span> {esc(join_words(lows))}. '
            'The guide ships at 4 or more on every criterion.</p>') if lows else ''
    why = f'<details class="why-d"><summary>Every score with its reason</summary>{reasons}</details>' if reasons else ''
    return (f'<div class="scores"><p class="label">{esc(title)}</p>{flag}'
            f'<div class="tw" role="region" tabindex="0" aria-label="Scores"><table class="sc-t"><thead><tr><th scope="col">Drawing</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>{why}</div>'), lows


def mini_scores(sc):
    """Six scores in one line, for a Housing option."""
    if not sc or not sc.get('scores'):
        return 'Pending'
    parts = []
    for k, lab in RUBRIC:
        x = (sc.get('scores') or {}).get(k) or {}
        v = x.get('score') if isinstance(x, dict) else x
        low = isinstance(v, (int, float)) and v < 4
        parts.append(f'<span class="ms{" ms--low" if low else ""}">{esc(RUBRIC_SHORT.get(k, lab))} <b class="num">{v}</b>{"<span class=vh> (under 4)</span>" if low else ""}</span>')
    return '<span class="mss">' + ' '.join(parts) + '</span>'


def open_items(subjects):
    items = []
    for name, sc in subjects:
        for m in (sc or {}).get('must_fix') or []:
            if isinstance(m, str):
                items.append((name, '', m))
            else:
                items.append((name, m.get('owner', ''), m.get('fix', '')))
    if not items:
        return ''
    li = ''.join(f'<li><b>{esc(n)}</b>{" (" + esc(o.lower()) + ")" if o else ""}: {esc(f)}</li>' for n, o, f in items)
    return (f'<details class="open-d"><summary>{num_words(len(items)).capitalize()} item{"s" if len(items) != 1 else ""} the creative director '
            f'still lists as Must fix</summary><ul>{li}</ul></details>')


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
    holds = '<p class="caption holds-l" data-holds="{0}">Held back: none</p>'.format(n) if card.get('holds') else ''
    return (f'<fieldset class="ans"><legend>Your answer to card {n}</legend>{groups}{holds}'
            f'<label class="rad chk"><input type="checkbox" data-named="{n}"><span>I approve card {n} by name</span></label>'
            f'<label class="nl" for="note-{n}">A note, or an answer of your own</label>'
            f'<textarea id="note-{n}" rows="2" data-note="{n}"></textarea></fieldset>')


def rec_html(card):
    out = ''
    for who, r in card['recs']:
        if not r:
            continue
        out += (f'<div class="rec{" rec--cd" if who == "cd" else ""}"><p class="label">{esc(r["label"])}</p>'
                f'<p class="rec-o">{esc(r["option"])}</p><p>{esc(r["reason"])}</p></div>')
    return out


def card_shell(card, body, head_extra=''):
    n = card['n']
    flags = chip('Needs your approval by name', 'chip--named')
    if card.get('pending'):
        flags += chip('Scores pending', 'chip--low')
    if card.get('lows'):
        flags += chip('A score under 4', 'chip--low')
    if card.get('not_ready'):
        flags += chip('Not signed off by the creative director', 'chip--low')
    return f'''<article class="card" id="card-{n}" data-card="{n}" data-short="{attr(copy(card["short"]))}" aria-labelledby="card-{n}-h">
<header class="card-head"><p class="card-n" aria-hidden="true">{n}</p><div><h3 class="card-h" id="card-{n}-h"><span class="vh">Card {n}. </span>{esc(card["title"])}</h3>
<p class="chips">{flags}</p>{card.get("lede_html", "")}{head_extra}</div></header>
<div class="card-body">{body}</div>
<div class="card-foot"><div class="foot-main">{rec_html(card)}<div class="approve"><p class="label">What you approve by name</p><p>{esc(card["approve"])}</p></div>{card.get("foot_extra", "")}</div>
{answer_block(card)}</div></article>'''


# ------------------------------------------------------------------------------------------------ the model
def build_inputs(C):
    I = {}
    inv_path = one_file(SRC['v6'], '*Inventory.json', 'the Civic Line inventory in use')
    inv = load_json(inv_path, 'the Civic Line inventory')
    I['inv'] = {r['id']: r for r in inv['icons']}
    I['n_masters'] = len(I['inv'])

    def master_path(i, ed='black'):
        r = I['inv'][i]
        key = {'black': 'svg_black', 'red-black': 'svg_red_black', 'newsprint': 'svg_newsprint', 'red-newsprint': 'svg_red_newsprint'}[ed]
        return SRC['v6'] / ed / r['exports'][key]
    I['master_path'] = master_path
    # the 37, in chapter 10's order, and their fits
    lst = fits_list(SRC['ch10'].read_text())
    fm_path = one_file(SRC['fits'], '*Manifest.json', 'the 24 px fits manifest')
    fm = load_json(fm_path, 'the 24 px fits manifest')
    by = {f['id']: f for f in fm['fits']}
    rows = []
    for i, word, atlas in lst:
        need(i in by, f'{i} is on chapter 10’s list but not in {fm_path.name}')
        need(i in I['inv'], f'{i} is not in the inventory in use')
        f = by[i]
        mp = master_path(i)
        if f.get('master_black') and rel(mp) != f['master_black']:
            warn(f'{i}: the fits manifest names {f["master_black"]} as its master; the board uses {rel(mp)}')
        need((ROOT / f['svg']).exists(), f'{i}: {f["svg"]} is missing')
        rows.append({'id': i, 'word': word, 'atlas': atlas, 'svg': f['svg'], 'master_path': mp, 'kept': f.get('kept', '')})
    extra = sorted(set(by) - {r['id'] for r in rows})
    if extra:
        warn(f'the fits manifest holds {join_words(extra)}, which chapter 10’s list does not')
    if [r['id'] for r in rows] != [f['id'] for f in fm['fits'] if f['id'] in {r['id'] for r in rows}]:
        warn('the fits manifest lists the 37 in another order than chapter 10; the board follows chapter 10')
    I['fit_rows'] = rows
    I['fits_manifest'] = fm_path
    # Pause and Filter: the approved files and the redraws, from the redraw manifest
    um_path = one_file(SRC['redraw'], '*Manifest.json', 'the 16 px redraw manifest')
    um = load_json(um_path, 'the 16 px redraw manifest')
    util, seen = [], set()
    for r in um['redraws']:
        ap = ROOT / r['approved_file']
        if ap not in seen:
            seen.add(ap)
            util.append({'name': r['name'], 'role': 'approved', 'label': 'Approved file', 'path': ap, 'what': ''})
        m = re.search(r'Redraw-([A-Z])\.svg$', r['file'])
        util.append({'name': r['name'], 'role': m.group(1) if m else 'redraw', 'label': f'Option {m.group(1)}' if m else 'Redraw',
                     'path': ROOT / r['file'], 'what': r.get('what', '')})
    for u in util:
        need(u['path'].exists(), f'{u["name"]}: {u["path"]} is missing')
    I['util_files'] = util
    I['util_manifest'] = um_path
    # Housing
    hm_path = one_file(SRC['topics'], '*Housing-Manifest.json', 'the Housing manifest')
    hm = load_json(hm_path, 'the Housing manifest')
    for o in hm['options']:
        for ed, p in o['svg'].items():
            need((ROOT / p).exists(), f'Housing {o["option"]}: {p} is missing')
    I['housing'] = hm
    I['housing_manifest'] = hm_path
    # identity
    I['idf'] = load_json(SRC['id_figs'], 'the identity figures')
    I['icon_q'] = designer_questions(SRC['icon_notes'].read_text()) if SRC['icon_notes'].exists() else []
    I['id_q'] = designer_questions(SRC['id_notes'].read_text()) if SRC['id_notes'].exists() else []
    if not I['icon_q']:
        warn('no questions found in the icon designer’s notes')
    if not I['id_q']:
        warn('no questions found in the identity designer’s notes')
    return I


def designer_recs(I):
    """The designers' recommended answers, read from their questions for Dustin (the values only; the words on the board
    are the board's own, with this run's figures)."""
    out = {}
    for q in I['icon_q']:
        t, r = q['title'].lower(), q['recommendation'].lower()
        if 'r-06' in t:
            out['r06_skipped'] = q['n']
            continue
        if '37' in t or 'fits' in t:
            out['fits'] = 'some' if re.search(r'\bbut\b|except|hold', r) else 'all'
        elif 'pause' in t:
            out['pause'] = 'keep' if r.startswith('keep') else 'approve'
        elif 'filter' in t:
            out['filter'] = letter_of(q['recommendation']) or ''
        elif 'housing' in t and '24' in t:
            out['h24'] = 'keep' if re.search(r'48 px and up|keep', r) else 'add'
        elif 'housing' in t:
            out['housing'] = letter_of(q['recommendation']) or ''
    for q in I['id_q']:
        t, r = q['title'].lower(), q['recommendation'].lower()
        key = 'print_l3' if 'l3' in t else 'social' if 'sign-off' in t or 'social' in t else None
        if key:
            out[key] = 'keep' if r.startswith('keep') else 'approve'
    return out


def build_model(C, S, I, scratch, reuse):
    R = run_checks(I, scratch, reuse)
    Lf = R['likeness_fits']
    flag = Lf['thresholds']['flag']['likeness']
    watch = Lf['distribution']['p95']
    need(abs(Lf['thresholds']['flag']['percentile'] - 99) < 1e-9, 'the fits run did not flag at the 99th percentile')

    def status(v):
        return 'flag' if v >= flag else 'watch' if v >= watch else ''
    fit_name = {pathlib.Path(f['svg']).name: f['id'] for f in I['fit_rows']}
    label = {i: f'{i} {r["label"]}' for i, r in I['inv'].items()}
    # ---- the fits' figures
    pf_f = {pathlib.Path(r['file']).name: r for r in R['pixel_fit_fits']['results']}
    pf_m = {pathlib.Path(r['file']).name: r for r in R['pixel_fit_masters']['results']}
    own = {x['a']: x['likeness'] for x in Lf['own']}
    closest = {x['a']: x for x in Lf['closest']}
    fit_flags = {}
    n_watch = 0
    for x in Lf['flagged'] + Lf['watch']:
        if x['likeness'] < watch:
            continue
        a = fit_name[x['a']]
        b = fit_name.get(x['b']) or x['b'].split()[0]
        if x['likeness'] >= flag:
            fit_flags.setdefault(a, []).append((b, x['likeness']))
            if x['b'] in fit_name:
                fit_flags.setdefault(b, []).append((a, x['likeness']))
        else:
            n_watch += 1
    n_flag = len([x for x in Lf['flagged']])
    # pairs among the fits (new) and between neutral masters
    fit_pairs = {}
    for x in Lf['flagged'] + Lf['watch']:
        if x.get('against') == 'new':
            a, b = fit_name[x['a']], fit_name[x['b']]
            fit_pairs[(a, b)] = fit_pairs[(b, a)] = x['likeness']
    Ln = R['likeness_neutral_masters']
    master_pairs = {}
    for x in Ln['flagged'] + Ln['watch']:
        if x.get('against') == 'new':
            a, b = R['neutral'][x['a']], R['neutral'][x['b']]
            master_pairs[(a, b)] = master_pairs[(b, a)] = x['likeness']
    rows = []
    for f in I['fit_rows']:
        fn = pathlib.Path(f['svg']).name
        mn = f['master_path'].name
        need(fn in pf_f and mn in pf_m, f'{f["id"]}: no pixel-fit result')
        fl = []
        for b, v in sorted(fit_flags.get(f['id'], []), key=lambda t: -t[1]):
            fl.append({'with': b, 'label': label.get(b, b), 'likeness': v, 'masters': master_pairs.get((f['id'], b))})
        c = closest.get(fn)
        rows.append(f | {'master_path': str(f['master_path']), 'full_master': full_ink(pf_m[mn]), 'full_fit': full_ink(pf_f[fn]),
                         'pf_fit': {'pass': pf_f[fn]['pass'], 'fails': {s: pf_f[fn]['scales'][s]['fails'] for s in ('1x', '2x')}},
                         'pf_master_pass': pf_m[mn]['pass'], 'master_line_px_1x': pf_m[mn]['scales']['1x']['stroke_px']['main'],
                         'like_own': own.get(fn), 'closest': {'name': c['b'], 'likeness': c['likeness']} if c else None,
                         'flags': fl, 'five': f['id'] in LOOK_ALIKES})
    five = []
    for k, a in enumerate(LOOK_ALIKES):
        for b in LOOK_ALIKES[k + 1:]:
            m, ft = master_pairs.get((a, b)), fit_pairs.get((a, b))
            if m is None or ft is None:
                warn(f'the five look-alikes: no figure for {a} and {b} ({"masters" if m is None else "fits"})')
            five.append({'a': a, 'b': b, 'masters': m, 'fits': ft})
    five.sort(key=lambda p: -(p['masters'] or 0))
    # ---- Pause and Filter: pixel fit at 16 px, pictures and open pixels
    pf_u = {pathlib.Path(r['file']).name: r for r in R['pixel_fit_utility']['results']}
    for u in I['util_files']:
        r = pf_u.get(u['path'].name)
        u['pf'] = {'pass': r['pass'], 'fails': {s: r['scales'][s]['fails'] for s in ('1x', '2x')}} if r else None
    # ---- Housing likeness
    Lh = R['likeness_housing']
    hname = {pathlib.Path(o['svg']['black']).name: o['option'] for o in I['housing']['options']}
    h = {}
    for o in I['housing']['options']:
        n = pathlib.Path(o['svg']['black']).name
        c = next((x for x in Lh['closest'] if x['a'] == n), None)
        against = {}
        for x in Lh['flagged'] + Lh['watch']:
            if x['a'] == n and x.get('against') == 'master':
                against[x['b'].split()[0]] = x['likeness']
        sib = []
        for x in Lh['options'] + Lh['flagged'] + Lh['watch']:
            if x.get('against') in ('new', None) and n in (x['a'], x['b']) and x['a'] in hname and x['b'] in hname:
                other = hname[x['b'] if x['a'] == n else x['a']]
                sib.append((other, x['likeness']))
        sib = sorted(set(sib), key=lambda t: -t[1])
        h[o['option']] = {'closest': {'name': c['b'], 'likeness': c['likeness'], 'percentile': c['percentile'], 'status': status(c['likeness'])} if c else None,
                          'against': against, 'sibling': {'option': sib[0][0], 'likeness': sib[0][1]} if sib else None,
                          'flagged': [x['b'] for x in Lh['flagged'] if x['a'] == n]}
    for nb in I['housing'].get('neighbors_on_the_board', []):
        for o in h:
            if nb not in h[o]['against']:
                warn(f'Housing {o}: no look-alike figure against {nb}')
    return {'R': R, 'flag': flag, 'watch': watch, 'status': status, 'rows': rows, 'five': five, 'n_flag': n_flag, 'n_watch': n_watch,
            'fit_flags_listed': fit_flags, 'housing_like': h, 'pairs': Lf['distribution']['pairs'], 'label': label}


# ------------------------------------------------------------------------------------------------ pictures
def make_pictures(I, M, scratch):
    """Every picture the board shows as a 1x or 2x screen draws it, made in this run from today's files, and the
    measurement pictures for the open pixels. Display pictures go to renders/ beside the board."""
    RENDERS.mkdir(parents=True, exist_ok=True)
    for old in RENDERS.glob(f'{DATE}_Board-C-*.png'):
        old.unlink()
    mdir = scratch / 'measure'
    jobs, pics = [], {}

    def add(key, file, size, dpr, bg, color, out):
        jobs.append({'kind': 'svg', 'file': str(file), 'size': size, 'dpr': dpr, 'bg': bg, 'color': color, 'out': str(out)})
        pics[key] = out
    for r in M['rows']:
        i = r['id']
        add(('fit', i, 'master', 1), r['master_path'], FIT_PX, 1, NP, CH, RENDERS / f'{DATE}_Board-C-Fit-Row-{i}-Master-1x.png')
        add(('fit', i, 'fit', 1), ROOT / r['svg'], FIT_PX, 1, NP, CH, RENDERS / f'{DATE}_Board-C-Fit-Row-{i}-Fit-1x.png')
        add(('fit', i, 'master', 2), r['master_path'], FIT_PX, 2, NP, CH, RENDERS / f'{DATE}_Board-C-Fit-Row-{i}-Master-2x.png')
    for u in I['util_files']:
        stem = f'{u["name"]}-{"Approved" if u["role"] == "approved" else "Redraw" if u["role"] == "redraw" else "Redraw-" + u["role"]}'
        u['stem'] = stem
        for sname, bg, ink in (('Newsprint', NP, CH), ('Charcoal', CH, NP)):
            for d in (1, 2):
                add(('ut', stem, sname, d), u['path'], UT_PX, d, bg, ink, RENDERS / f'{DATE}_Board-C-Utility-{stem}-{sname}-{d}x.png')
        add(('ut-m', stem, 1), u['path'], UT_PX, 1, None, CH, mdir / f'{stem}-alpha-1x.png')
        add(('ut-m', stem, 16), u['path'], UT_PX, 16, None, CH, mdir / f'{stem}-alpha-16x.png')
    for o in I['housing']['options']:
        for d in (1, 2):
            add(('h24', o['option'], d), ROOT / o['svg']['black'], FIT_PX, d, NP, CH, RENDERS / f'{DATE}_Board-C-Housing-Option-{o["option"]}-24px-Black-{d}x.png')
    render(jobs, scratch, 'drawings')
    for u in I['util_files']:
        u['open'] = open_pixels(pics[('ut-m', u['stem'], 1)], pics[('ut-m', u['stem'], 16)], 16, UT_PX)
        if not u['open']:
            warn(f'{u["stem"]}: no opening found to count')
    # the social cards at actual size, from the identity designer's plate, at 1x and 2x
    plate = SRC['id_plates'] / f'{DATE}_Social-Sign-Off-Comparison.html'
    want = [('Today', 'Newsprint-48px', 'Today’s card'), ('Proposal', 'Newsprint-96px', 'The proposal, actual'), ('Proposal', 'Charcoal-96px', 'The proposal on Charcoal')]
    ejobs = []
    for k, (who, stem, head) in enumerate(want):
        for d in (1, 2):
            out = RENDERS / f'{DATE}_Board-C-Social-Card-{stem}-Actual-Size-{d}x.png'
            ejobs.append({'kind': 'element', 'html': str(plate), 'selector': 'div.oai > div[style*="width:1200px"]', 'index': k, 'dpr': d, 'out': str(out), 'vw': 1380})
            pics[('card', stem, d)] = out
    res = render(ejobs, scratch, 'plate') if plate.exists() else []
    if not plate.exists():
        warn(f'{plate.name} is missing; the social card at actual size cannot show')
    cards = []
    for k, (who, stem, head) in enumerate(want):
        r1 = res[2 * k] if len(res) > 2 * k else {}
        if r1.get('error'):
            warn(f'social plate: {r1["error"]}')
            continue
        if not str(r1.get('heading') or '').startswith(head):
            warn(f'social plate: card {k + 1} sits under "{r1.get("heading")}", expected "{head}"')
        fonts = ' '.join(r1.get('fonts') or [])
        if 'Inter' not in fonts:
            warn(f'social plate: Inter did not load for the card pictures ({fonts or "no fonts"})')
        cards.append({'who': who, 'stem': stem, 'w': r1.get('w'), 'h': r1.get('h'), 'fonts': r1.get('fonts')})
    M['social_cards'] = cards
    M['pics'] = pics
    return pics


# ------------------------------------------------------------------------------------------------ cards
def fit_figures(M, I):
    rows = M['rows']
    fm = [r['full_master']['share'] for r in rows]
    ff = [r['full_fit']['share'] for r in rows]
    return {
        'n_fits': len(rows), 'pf_fits_pass': sum(1 for r in rows if r['pf_fit']['pass']),
        'pf_masters_pass': sum(1 for r in rows if r['pf_master_pass']),
        'fits_full_min': fmt_pct(min(ff)), 'masters_full_min': fmt_pct(min(fm)), 'masters_full_max': fmt_pct(max(fm)),
        'n_flagged': f'{M["n_flag"]} pair{"s" if M["n_flag"] != 1 else ""}', 'n_watched': f'{M["n_watch"]} more',
    }


def housing_card(card, C, I, M, SC):
    W = C['cards']['housing']
    hm = I['housing']
    sc_list = SC['housing']
    letters = [o['option'] for o in hm['options']]
    # per-option scores: a scores card per option, or options with their own scores inside one card
    per = {}
    for k, v in option_scores(sc_list).items():
        if letter_of(k):
            per[letter_of(k)] = v
    for c in sc_list:
        m = re.search(r'(?:option|housing)[\s_-]*([A-C])\b', f'{c.get("id", "")} {c.get("title", "")}', flags=re.I)
        if m and c.get('scores') and m.group(1).upper() not in per:
            per[m.group(1).upper()] = c
    card_level = [c for c in sc_list if c.get('scores') and not per]
    cd_opt, cd_reason = cd_rec_text(sc_list)
    cd_letter = letter_of(cd_opt) if cd_opt else None
    rec_letter = cd_letter or card['designer']['housing']
    hl = M['housing_like']
    cols = ''
    for o in hm['options']:
        L = o['option']
        lk = hl[L]
        chips = ''
        if L == rec_letter:
            chips += chip('Recommended', 'chip--rec')
        if lk['flagged']:
            chips += chip('Flagged look-alike', 'chip--flag')
        stage_np, stage_ch = '', ''
        for ed, lab in (('red-black', 'Red edition'), ('black', 'Black edition')):
            figs = ''.join(f'<figure class="sz">{img(ROOT / o["svg"][ed], s, s, f"Housing option {L}, {lab.lower()}, at {s} px on Newsprint")}<figcaption>{s}</figcaption></figure>' for s in HOUSING_SIZES)
            stage_np += f'<p class="st-l">{esc(lab)}</p><div class="sizes">{figs}</div>'
        for ed, lab in (('red-newsprint', 'Red edition'), ('newsprint', 'One color')):
            figs = ''.join(f'<figure class="sz">{img(ROOT / o["svg"][ed], s, s, f"Housing option {L}, {lab.lower()}, at {s} px on Charcoal")}<figcaption>{s}</figcaption></figure>' for s in HOUSING_SIZES)
            stage_ch += f'<p class="st-l">{esc(lab)}</p><div class="sizes">{figs}</div>'
        rows = [('What it shows', esc(ov(o.get('shows', ''))))]
        n = cd_naming(sc_list, L)
        if n:
            rows.append(('Naming test at 48 px', f'“{esc(str(n.get("creative_director_reading", "")).rstrip("."))}.” {esc(n.get("creative_director_verdict", ""))}.'))
            if n.get('maker_verdict'):
                rows.append(('The icon designer’s verdict', f'{esc(n["maker_verdict"])}.'))
        else:
            rows.append(('Naming test at 48 px', 'The creative director’s reading is pending.'))
            card['naming_missing'] = True
        c = lk['closest']
        if c:
            st = M['status'](c['likeness'])
            rows.append(('Closest settled drawing', f'{esc(c["name"])}, <span class="num">{fmt_like(c["likeness"])}</span>'
                         + (' ' + chip({'flag': 'flagged', 'watch': 'to watch'}[st], 'chip--' + st) if st else '')))
        if 'CL-054' in lk['against']:
            rows.append(('Against CL-054 Home Equity', f'<span class="num">{fmt_like(lk["against"]["CL-054"])}</span>'))
        if lk['sibling']:
            rows.append(('Closest other option', f'Option {esc(lk["sibling"]["option"])}, <span class="num">{fmt_like(lk["sibling"]["likeness"])}</span>'))
        rows.append(('Scores, 1 to 5', mini_scores(per.get(L)) if per.get(L) else ('Scored as one card, below' if card_level else 'Pending')))
        cols += (f'<div class="col{" col--rec" if L == rec_letter else ""}"><p class="col-h">Option {esc(L)}</p><p class="chips">{chips}</p>'
                 f'<div class="stage"><p class="st-h">On Newsprint</p>{stage_np}</div>'
                 f'<div class="stage stage--ch"><p class="st-h">On Charcoal</p>{stage_ch}</div>'
                 f'<p class="ref caption">24 px: reference size only</p>{dl(rows)}</div>')
    body = f'<div class="cols cols--h">{cols}</div>'
    # the settled neighbours
    nbs = ''
    for nb in hm.get('neighbors_on_the_board', []):
        need(nb in I['inv'], f'Housing neighbour {nb} is not in the inventory')
        lab = M['label'][nb]
        figs = ''.join(f'<figure class="sz">{img(I["master_path"](nb, "red-black"), s, s, f"{lab}, at {s} px")}<figcaption>{s}</figcaption></figure>' for s in HOUSING_SIZES)
        lk = ' · '.join(f'{L} <span class="num">{fmt_like(hl[L]["against"][nb])}</span>' for L in letters if nb in hl[L]['against'])
        nbs += f'<div class="nb"><div class="stage">{"<div class=sizes>" + figs + "</div>"}</div><p class="nb-l"><b>{esc(lab)}</b></p><p class="caption">{lk}</p></div>'
    body += (f'<h4 class="sub4">{esc(W["neighbors_title"])}</h4><p class="pnote">{esc(W["neighbors_text"])}</p>'
             f'<div class="nbs">{nbs}</div>')
    # the 24 px question
    h24 = ''
    for o in hm['options']:
        L = o['option']
        p1, p2 = M['pics'][('h24', L, 1)], M['pics'][('h24', L, 2)]
        h24 += (f'<div class="h24-o"><p class="col-h">Option {esc(L)}</p><div class="stage pxs">'
                f'<figure class="sz">{img(p1, FIT_PX, FIT_PX, f"Housing option {L} at 24 px as a 1x screen draws it", px=True)}<figcaption>1x</figcaption></figure>'
                f'<figure class="sz">{img(p2, FIT_PX * 2, FIT_PX * 2, f"Housing option {L} at 24 px as a 2x screen draws it, shown at twice its size", px=True)}<figcaption>2x, twice size</figcaption></figure></div></div>')
    body += (f'<h4 class="sub4">{esc(W["h24_title"])}</h4>{paras(W["h24_text"], "pnote")}<div class="h24s">{h24}</div>'
             f'<p class="caption pnote">Each picture is the black edition, the one used under 48 px, on Newsprint. The 2x picture is set at its own size, twice the drawing’s, so each of its pixels shows.</p>')
    subjects = [(f'Housing, option {L}', per[L]) for L in letters if L in per] + [(card['short'], c) for c in card_level]
    if not subjects:
        subjects = [('Housing', None)]
    sh, lows = scores_block(subjects)
    card['lows'] = lows
    card['foot_extra'] = sh + open_items([(card['short'], c) for c in sc_list])
    card['not_ready'] = any(c.get('ready_for_board') is False for c in sc_list)
    fill_h = {f'{L}_{nb.replace("-", "")}': fmt_like(hl[L]['against'][nb]) for L in letters for nb in hl[L]['against']}
    card['recs'] = [('designer', {'label': 'The icon designer recommends', 'option': f'Option {card["designer"]["housing"]}',
                                  'reason': fill(W['designer_rec']['text'], fill_h)})]
    if cd_opt:
        card['recs'].append(('cd', {'label': 'The creative director recommends', 'option': f'Option {cd_letter}' if cd_letter else cd_opt, 'reason': cd_reason}))
    h24_rec = card['designer']['h24']
    card['groups'] = [
        {'name': 'opt', 'label': 'Option', 'rec': rec_letter, 'options': [(L, f'Option {L}', f'option {L}') for L in letters]},
        {'name': 'h24', 'label': W['h24_label'], 'rec': h24_rec, 'options': [(k, W['h24_options'][k][0], W['h24_options'][k][1]) for k in ('keep', 'add')]},
    ]
    card['figs'] = {'likeness': hl, 'neighbors': hm.get('neighbors_on_the_board', [])}
    return card_shell(card, body)


def utility_card(card, C, I, M, SC):
    W = C['cards']['utility']
    sc_list = SC['utility']
    names = []
    for u in I['util_files']:
        if u['name'] not in names:
            names.append(u['name'])
    blocks = ''
    figs_out = {}
    for name in names:
        us = [u for u in I['util_files'] if u['name'] == name]
        cols = ''
        for u in us:
            st = u['stem']
            p = M['pics']
            views = ''
            for sname, cls in (('Newsprint', ''), ('Charcoal', ' stage--ch')):
                views += (f'<div class="stage pxs{cls}">'
                          f'<figure class="sz">{img(p[("ut", st, sname, 1)], UT_PX, UT_PX, f"{name}, {u["label"].lower()}, at 16 px on {sname}, as a 1x screen draws it", px=True)}<figcaption>1x</figcaption></figure>'
                          f'<figure class="sz">{img(p[("ut", st, sname, 2)], UT_PX * 2, UT_PX * 2, f"{name}, {u["label"].lower()}, at 16 px on {sname}, as a 2x screen draws it, at twice its size", px=True)}<figcaption>2x, twice size</figcaption></figure></div>')
            enl = ''
            for sname, cls in (('Newsprint', 'grid--np'), ('Charcoal', 'grid--ch')):
                enl += (f'<figure class="grid {cls}">{img(p[("ut", st, sname, 1)], UT_PX * GRID_MAG, UT_PX * GRID_MAG, f"{name}, {u["label"].lower()}, the 1x picture on {sname}, {num_words(GRID_MAG)} times larger with a pixel grid", px=True)}'
                        f'<figcaption class="caption">{sname}, {num_words(GRID_MAG)} times</figcaption></figure>')
            op = u['open']
            rows = []
            if op:
                parts = []
                for k, o in enumerate(op):
                    where = ('inside each bar' if len(op) > 1 else 'down the spout' if name.lower() == 'filter' else 'inside the opening')
                    parts.append(f'{o["rows_open"]} of {o["n_rows"]} rows' + ('' if len(op) > 1 else f' {where}'))
                same = len({x for x in parts}) == 1
                txt = (f'{parts[0]} inside each bar' if len(op) > 1 and same else '; '.join(parts))
                if all(o['rows_open'] == 0 for o in op):
                    txt = 'None: ' + txt
                rows.append(('Open pixels at 1x', esc(txt)))
                o = op[0]
                rows.append((f'Across the opening, {o["mid_row"]} px down', f'<span class="num">{", ".join(str(a) for a in o["mid_alpha"])}</span> <span class="caption">(0 is open, 255 is full ink)</span>'))
            pf = u.get('pf')
            rows.append(('Pixel-fit check, 1.5 px line', esc(pf_words(pf, UT_PX) if pf else 'Not run')))
            if u['role'] != 'approved':
                key = f'{name} redraw' if u['role'] == 'redraw' else f'{name} {u["role"]}'
                n = next((x for x in (sc_list[0].get('naming_test') or [] if sc_list else []) if str(x.get('option', '')).lower() == key.lower()), None)
                if n:
                    rows.append(('Naming test at 16 px', f'“{esc(str(n.get("creative_director_reading", "")).rstrip("."))}.” {esc(n.get("creative_director_verdict", ""))}.'))
                os_ = {k.lower(): v for k, v in option_scores(sc_list).items()}
                rows.append(('Scores, 1 to 5', mini_scores(os_.get(key.lower())) if os_.get(key.lower()) else 'Pending'))
            what = ''
            figs_out[st] = {'file': rel(u['path']), 'open': op, 'pixel_fit': pf}
            rec = (name.lower() == 'filter' and u['role'] == card['rec_filter']) or (name.lower() == 'pause' and u['role'] != 'approved' and card['rec_pause'] == 'approve')
            chips = chip('Recommended', 'chip--rec') if rec else (chip('In use today') if u['role'] == 'approved' else '')
            cols += (f'<div class="col col--u{" col--rec" if rec else ""}"><p class="col-h">{esc(u["label"])}</p><p class="chips">{chips}</p>{what}'
                     f'{views}<div class="grids">{enl}</div>{dl(rows)}</div>')
        blocks += f'<h4 class="sub4">{esc(name)}</h4><div class="cols cols--u">{cols}</div>'
    blocks += (f'<p class="caption pnote">{esc(fill(W["grid_caption"], {"mag": num_words(GRID_MAG)}))} {esc(W["open_rule"])} '
               'The figures across the opening are the ink of each pixel on the row whose top edge sits 8 px below the top of the 16 px box.</p>')
    ops = option_scores(sc_list)
    subjects = [(k, v) for k, v in ops.items()] or [(card['short'], c) for c in sc_list] or [('Pause and Filter', None)]
    sh, lows = scores_block(subjects)
    card['lows'] = lows
    card['foot_extra'] = sh + open_items([(card['short'], c) for c in sc_list])
    card['not_ready'] = any(c.get('ready_for_board') is False for c in sc_list)
    d = card['designer']
    pause = next(u for u in I['util_files'] if u['name'].lower() == 'pause' and u['role'] != 'approved')
    pause_ap = next(u for u in I['util_files'] if u['name'].lower() == 'pause' and u['role'] == 'approved')
    fA = next((u for u in I['util_files'] if u['name'].lower() == 'filter' and u['role'] == 'A'), None)
    fB = next((u for u in I['util_files'] if u['name'].lower() == 'filter' and u['role'] == 'B'), None)

    def rows_of(u):
        o = u['open'][0] if u and u['open'] else None
        return f'{o["rows_open"]} of {o["n_rows"]}' if o else 'none'
    pr = rows_of(pause_ap)
    fl = {'pause_rows': rows_of(pause), 'pause_rows_today': 'none' if pr.startswith('0 ') else pr,
          'filter_A_rows': rows_of(fA), 'filter_B_rows': rows_of(fB)}
    card['recs'] = [('designer', {'label': 'The icon designer recommends', 'option': f'The Pause redraw, Filter option {d["filter"]}',
                                  'reason': fill(W['designer_rec']['text'], fl)})]
    cd_opt, cd_reason = cd_rec_text(sc_list)
    if cd_opt:
        card['recs'].append(('cd', {'label': 'The creative director recommends', 'option': cd_opt, 'reason': cd_reason}))
    letters = [u['role'] for u in I['util_files'] if u['name'].lower() == 'filter' and u['role'] not in ('approved', 'redraw')]
    card['groups'] = [
        {'name': 'pause', 'label': W['pause_label'], 'rec': card['rec_pause'], 'options': [(k, W['pause_options'][k][0], W['pause_options'][k][1]) for k in ('approve', 'keep')]},
        {'name': 'filter', 'label': W['filter_label'], 'rec': card['rec_filter'],
         'options': [(L, W['filter_options'][L][0], W['filter_options'][L][1]) for L in letters] + [('keep', W['filter_options']['keep'][0], W['filter_options']['keep'][1])]},
    ]
    card['figs'] = figs_out | {'open_pixel_figures': fl}
    return card_shell(card, f'<div class="ut">{blocks}</div>')


def fits_card(card, C, I, M, SC):
    W = C['cards']['fits']
    sc_list = SC['fits']
    ids = [r['id'] for r in M['rows']]
    verdicts = row_verdicts(sc_list, set(ids))
    if sc_list and len(verdicts) < len(ids):
        missing = [i for i in ids if i not in verdicts]
        warn(f'card {card["n"]}: no verdict from the creative director for {len(missing)} of the {len(ids)} rows ({", ".join(missing[:6])}{"…" if len(missing) > 6 else ""})')
    cols = W['cols']
    head = ''.join(f'<span class="fr-h">{nx(esc(c))}</span>' for c in cols)
    lis = ''
    p = M['pics']
    for r in M['rows']:
        i = r['id']
        lab = f'{i} {r["word"]}'
        chips = chip('Look-alike', 'chip--watch') if r['five'] else ''
        if r['flags']:
            chips += chip('Flagged', 'chip--flag')
        atlas = f'<span class="fr-at">Atlas {esc(r["atlas"])}</span>' if r['atlas'] and r['atlas'] != i else ''
        fm, ff = r['full_master'], r['full_fit']
        ink = (f'<span class="num">{fmt_pct(fm["share"])}</span> <span class="fr-to">to</span> <span class="num">{fmt_pct(ff["share"])}</span>'
               f'<span class="fr-sub">{fm["full_px"]} of {fm["ink_px"]} px; {ff["full_px"]} of {ff["ink_px"]}</span>')
        pf = 'Passes' if r['pf_fit']['pass'] else esc(pf_words({'pass': False, 'scales': {s: {'fails': r['pf_fit']['fails'][s]} for s in ('1x', '2x')}}, FIT_PX))
        v = verdicts.get(i)
        cd = esc(ov(v)) if v else '<span class="caption">Pending</span>'
        note = ''
        if r['five']:
            others = [x for x in M['five'] if i in (x['a'], x['b'])]
            bits = []
            for x in others:
                o = x['b'] if x['a'] == i else x['a']
                if x['masters'] is not None and x['fits'] is not None:
                    bits.append(f'{o} {fmt_like(x["masters"])} to {fmt_like(x["fits"])}')
            note += f'<p class="fr-note"><span class="label">Against the other four, master to fit</span> {esc("; ".join(bits))}</p>'
        if r['flags']:
            pairs = join_words(f'{f["label"]} ({fmt_like(f["likeness"])})' for f in r['flags'])
            ms = [f for f in r['flags'] if f['masters'] is not None]
            masters = join_words(f'{fmt_like(f["masters"])} against {f["with"]}' for f in ms) if ms else 'no figure'
            note += f'<p class="fr-note">{esc(fill(W["flag_note"], {"pairs": pairs, "masters": masters}))}</p>'
        hold = (f'<label class="hold"><input type="checkbox" data-hold="{attr(i)}" data-card="{card["n"]}" data-label="{attr(copy(lab))}" '
                f'aria-label="Hold back {attr(copy(lab))}"><span>{esc(W["hold_label"])}</span></label>')
        lis += (f'<li class="fr{" fr--five" if r["five"] else ""}" id="fit-{attr(i)}">'
                f'<div class="fr-id"><p class="fr-name"><b>{esc(i)}</b> {esc(r["word"])}</p>{atlas}{" <span class=chips-in>" + chips + "</span>" if chips else ""}</div>'
                f'<div class="fr-pics stage">'
                f'<figure class="fr-p">{img(p[("fit", i, "master", 1)], FIT_PX, FIT_PX, f"{lab}, the master at 24 px as a 1x screen draws it", px=True)}<figcaption class="fr-l">Master, 1x</figcaption></figure>'
                f'<figure class="fr-p">{img(p[("fit", i, "fit", 1)], FIT_PX, FIT_PX, f"{lab}, the fit at 24 px as a 1x screen draws it", px=True)}<figcaption class="fr-l">Fit, 1x</figcaption></figure>'
                f'<figure class="fr-p">{img(p[("fit", i, "master", 2)], FIT_PX * 2, FIT_PX * 2, f"{lab}, the master at 24 px as a 2x screen draws it, shown at twice its size", px=True)}<figcaption class="fr-l">2x, twice size</figcaption></figure></div>'
                f'<div class="fr-ink"><span class="fr-l">Full ink, master to fit</span>{ink}</div>'
                f'<div class="fr-pf"><span class="fr-l">Pixel fit</span>{pf}</div>'
                f'<div class="fr-cd"><span class="fr-l">The creative director</span>{cd}</div>'
                f'<div class="fr-hold">{hold}</div>{note}</li>')
    table = f'<div class="fr-head" aria-hidden="true">{head}</div><ol class="frs">{lis}</ol>'
    body = table + ('<p class="caption pnote">Each row’s pictures sit on Newsprint as made: the master and the fit at 24 px as a 1x screen draws them, '
                    'then the master as a 2x screen draws it, set at its own size, twice the drawing’s. Full ink counts pixels inked 97 percent or more '
                    'among those inked 3 percent or more.</p>')
    # head: the summary, the five, and the scores for the set
    ff = fit_figures(M, I)
    five_rows = ''
    for x in M['five']:
        if x['masters'] is None or x['fits'] is None:
            continue
        d = x['fits'] - x['masters']
        sm, sf = M['status'](x['masters']), M['status'](x['fits'])
        five_rows += (f'<tr><th scope="row">{esc(x["a"])} and {esc(x["b"])}</th>'
                      f'<td class="num">{fmt_like(x["masters"])}{" " + chip({"flag": "flagged", "watch": "to watch"}[sm], "chip--" + sm) if sm else ""}</td>'
                      f'<td class="num">{fmt_like(x["fits"])}{" " + chip({"flag": "flagged", "watch": "to watch"}[sf], "chip--" + sf) if sf else ""}</td>'
                      f'<td class="num">{esc(f"{d:+.3f}")}</td></tr>')
    five = (f'<h4 class="sub4">{esc(W["five_title"])}</h4><p class="pnote">{esc(W["five_text"])}</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="The five look-alikes"><table class="fig-t"><thead><tr><th scope="col">Pair</th><th scope="col">Masters</th>'
            f'<th scope="col">Fits</th><th scope="col">Change</th></tr></thead><tbody>{five_rows}</tbody></table></div>')
    subjects = [(card['short'], c) for c in sc_list] or [(card['short'], None)]
    sh, lows = scores_block(subjects, 'The creative director’s scores for the set, 1 to 5')
    card['lows'] = lows
    card['not_ready'] = any(c.get('ready_for_board') is False for c in sc_list)
    head_extra = f'<p class="pnote summ">{esc(fill(W["summary"], ff))}</p>{sh}{open_items(subjects)}{five}'
    d = card['designer']
    card['recs'] = [('designer', {'label': 'The icon designer recommends', 'option': fill(W['options']['all'][0], ff),
                                  'reason': fill(W['designer_rec']['text'], ff)})]
    cd_opt, cd_reason = cd_rec_text(sc_list)
    rec = d['fits']
    if cd_opt:
        card['recs'].append(('cd', {'label': 'The creative director recommends', 'option': cd_opt, 'reason': cd_reason}))
        if re.search(r'\bbut\b|except|hold', cd_opt.lower()):
            rec = 'some'
    card['holds'] = True
    card['groups'] = [{'name': 'fits', 'label': None, 'rec': rec,
                       'options': [(k, fill(W['options'][k][0], ff), fill(W['options'][k][1], ff)) for k in ('all', 'some')]}]
    card['figs'] = {'summary': ff, 'rows': [{k: r[k] for k in ('id', 'word', 'atlas', 'full_master', 'full_fit', 'pf_fit', 'pf_master_pass',
                                                                 'master_line_px_1x', 'like_own', 'closest', 'flags', 'five')} | {'verdict': verdicts.get(r['id'])}
                                            for r in M['rows']], 'five': M['five']}
    return card_shell(card, body, head_extra)


def gain_cost(gain, cost):
    return (f'<div class="gc"><div class="gc-g"><p class="label">What it gains</p><p>{esc(gain)}</p></div>'
            f'<div class="gc-c"><p class="label">What it costs</p><p>{esc(cost)}</p></div></div>')


def l3_card(card, C, I, M, SC):
    W = C['cards']['print_l3']
    sc_list = SC['print_l3']
    pf = I['idf']['proposals']['print_l3']
    oct_, mast = pf['october_master'], pf['masthead_master']
    prop_key = next(k for k in pf if k.startswith('lockups/'))
    prus_key = next(k for k in pf if k.startswith('prussian/'))
    prop = pf[prop_key]
    iddir = SRC['identity']
    f_prop, f_prop_w = iddir / prop_key, iddir / prus_key
    f_oct, f_oct_w = iddir / prop['source'], iddir / pf[prus_key]['source']
    f_mast = iddir / mast['file']
    for f in (f_prop, f_prop_w, f_oct, f_oct_w, f_mast):
        need(f.exists(), f'print L3: {rel(f)} is missing')
    o_w, p_w = oct_['width_units'], prop['width_units']
    o_h, p_h = oct_['lockmark_units'], prop['lockmark_units']
    smaller = 100 * (1 - p_h / o_h)
    o5, p5 = pf['october_at_1.55_in'], pf['proposal_at_1.55_in']
    fl = {'masthead_ratio': f'{mast["lockmark_over_capitals"]:.2f}', 'october_ratio': fmt_g(float(oct_['lockmark_over_capitals']), 2),
          'proposal_ratio': f'{prop["lockmark_over_capitals"]:.2f}', 'smaller_pct': f'{smaller:.1f}',
          'prop_lock_in': f'{p5["lockmark_in"]:.3f}', 'oct_lock_in': f'{o5["lockmark_in"]:.3f}', 'oct_caps_mm': f'{o5["capitals_mm"]:.2f}', 'prop_caps_mm': f'{p5["capitals_mm"]:.2f}'}
    ch08 = SRC['ch08'].read_text().replace('\u00a0', ' ') if SRC['ch08'].exists() else ''
    if '0.25 in in print' not in ch08:
        warn('chapter 08 no longer gives the lockmark a 0.25 in print minimum; check the cost line on the print L3 card')
    ink = 'color:var(--oa-color-graphic-essential-on-newsprint)'
    # at the masthead's 282 px
    def at_w(f, units_w, units_h, w, lab, label):
        h = w * units_h / units_w
        caps = w * 100 / units_w
        return (f'<figure class="l3"><div class="l3-d">{inline_svg(f, w, h, style=ink, label=label)}</div>'
                f'<figcaption class="caption">{esc(lab)}, {fmt_g(round(w, 1))} by {h:.1f} px, capitals {caps:.1f} px</figcaption></figure>')
    m_w, m_h = 282, mast['lockmark_px']
    row282 = (f'<figure class="l3"><div class="l3-d">{inline_svg(f_mast, m_w, m_h, style=ink, label="The masthead master, in use on screen")}</div>'
              f'<figcaption class="caption">In use on screen: the masthead master, {m_w} by {m_h} px, capitals {mast["capitals_px"]} px</figcaption></figure>'
              + at_w(f_oct, o_w, o_h, 282, 'In use for print: the October master', 'The October L3 master at 282 px wide')
              + at_w(f_prop, p_w, p_h, 282, 'Proposal: the print L3', 'The proposed print L3 at 282 px wide'))
    card['lede_html'] = paras(W['lede'], 'card-lede', fl)
    body = gain_cost(fill(W['gain'], fl), fill(W['cost'], fl))
    body += f'<h4 class="sub4">{esc(W["row282"])}</h4><p class="pnote">{esc(W["row282_text"])}</p>' + frame(f'<div class="stage l3s" data-red="identity">{row282}</div>', W['row282'])
    s = 0.48     # 48 px capitals on 100-unit capitals
    row48 = (f'<figure class="l3"><div class="l3-d">{inline_svg(f_oct, o_w * s, o_h * s, style=ink, label="The October L3 master at 48 px capitals")}</div>'
             f'<figcaption class="caption">In use for print: the October master, lockmark at {fl["october_ratio"]} cap heights; {o_w * s:.0f} by {o_h * s:.0f} px</figcaption></figure>'
             f'<figure class="l3"><div class="l3-d">{inline_svg(f_prop, p_w * s, p_h * s, style=ink, label="The proposed print L3 at 48 px capitals")}</div>'
             f'<figcaption class="caption">Proposal: the print L3, lockmark at {fl["proposal_ratio"]} cap heights; {p_w * s:.0f} by {p_h * s:.0f} px</figcaption></figure>')
    body += f'<h4 class="sub4">{esc(W["row48"])}</h4>' + frame(f'<div class="stage l3s" data-red="identity">{row48}</div>', W['row48'])
    # the overlay: the October master in Stone under the proposal, the wordmarks together
    def vb_y(f):
        return float(re.search(r'<svg\b[^>]*\sviewBox="([^"]+)"', f.read_text()).group(1).split()[1])
    stone = 'color:var(--oa-color-palette-stone);--amp:var(--oa-color-palette-stone);--lever:var(--oa-color-palette-stone);--link:var(--oa-color-palette-stone)'
    dy = (vb_y(f_prop) - vb_y(f_oct)) * s     # the wordmark sits at the same units in both files
    ovl = (f'<div class="ovl" style="width:{o_w * s:.2f}px;height:{o_h * s:.2f}px">'
           f'<div class="ovl-a">{inline_svg(f_oct, o_w * s, o_h * s, style=stone)}</div>'
           f'<div class="ovl-b" style="top:{dy:.3f}px">{inline_svg(f_prop, p_w * s, p_h * s, style=ink)}</div></div>')
    body += (f'<h4 class="sub4">{esc(W["overlay"])}</h4><p class="pnote">{esc(W["overlay_text"])}</p>'
             + frame(f'<div class="stage l3s" data-red="identity" role="img" aria-label="The October master in Stone with the proposed print L3 over it, at 48 px capitals">{ovl}</div>', W['overlay']))
    roww = (f'<figure class="l3"><div class="l3-d">{inline_svg(f_oct_w, o_w * s, o_h * s, label="The October L3 master in White on Prussian")}</div>'
            f'<figcaption class="caption">The October master’s White file</figcaption></figure>'
            f'<figure class="l3"><div class="l3-d">{inline_svg(f_prop_w, p_w * s, p_h * s, label="The proposed print L3 in White on Prussian")}</div>'
            f'<figcaption class="caption">The proposal’s White file</figcaption></figure>')
    body += f'<h4 class="sub4">{esc(W["prussian"])}</h4>' + frame(f'<div class="stage stage--pr l3s">{roww}</div>', W['prussian'])
    pdf = SRC['id_plates'] / f'{DATE}_Print-L3-Comparison-Print.pdf'
    cap = SRC['id_plates'] / f'{DATE}_Print-L3-Comparison-1x.png'
    links = []
    if pdf.exists():
        links.append(f'<a href="{src(pdf)}">The print proof, as a PDF</a>')
    else:
        warn(f'{pdf.name} is missing')
    if cap.exists():
        links.append(f'<a href="{src(cap)}">The identity designer’s full plate</a>')
    body += f'<p class="pnote links">{" · ".join(links)}. {esc(W["links_text"])}</p>'
    rows = [('Lockmark over capitals', f'October master <span class="num">{fl["october_ratio"]}</span>; proposal <span class="num">{fl["proposal_ratio"]}</span>; masthead <span class="num">{fl["masthead_ratio"]}</span>'),
            ('Width, in cap heights', f'October master <span class="num">{oct_["width_over_capitals"]:.2f}</span>; proposal <span class="num">{prop["width_over_capitals"]:.2f}</span>'),
            ('At 1.55 in wide', f'October master: capitals {o5["capitals_mm"]:.2f} mm, lockmark {o5["lockmark_in"]:.3f} in. Proposal: capitals {p5["capitals_mm"]:.2f} mm, lockmark {p5["lockmark_in"]:.3f} in')]
    body += dl(rows)
    subjects = [(card['short'], c) for c in sc_list] or [(card['short'], None)]
    sh, lows = scores_block(subjects)
    card['lows'] = lows
    card['foot_extra'] = sh + open_items(subjects)
    card['not_ready'] = any(c.get('ready_for_board') is False for c in sc_list)
    d = card['designer']['print_l3']
    card['recs'] = [('designer', {'label': 'The identity designer recommends', 'option': W['options'][d][0],
                                  'reason': 'L3 then has one proportion in every medium, the change touches nothing but the lockmark’s size and place, and at L3’s print minimum the lockmark stays over its own.'})]
    cd_opt, cd_reason = cd_rec_text(sc_list)
    rec = d
    if cd_opt:
        card['recs'].append(('cd', {'label': 'The creative director recommends', 'option': cd_opt, 'reason': cd_reason}))
        rec = 'keep' if re.search(r'\bkeep\b', cd_opt.lower()) else 'approve'
    card['groups'] = [{'name': 'l3', 'label': None, 'rec': rec, 'options': [(k, W['options'][k][0], W['options'][k][1]) for k in ('approve', 'keep')]}]
    card['figs'] = {'from': rel(SRC['id_figs']), 'print_l3': pf, 'derived': fl}
    return card_shell(card, body)


def social_card(card, C, I, M, SC):
    W = C['cards']['social']
    sc_list = SC['social']
    so = I['idf']['proposals']['social_sign_off_96']
    n48, n96, c48, c96 = so['newsprint-48'], so['newsprint-96'], so['charcoal-48'], so['charcoal-96']
    widths = I['idf']['feed']['widths']['newsprint'].get('lever_red_by_width') or {}
    n_w = len(widths) or 301
    fl = {'lock_360_today': fmt_g(float(n48['lockmark_px_at']['360'])), 'lock_360_96': fmt_g(float(n96['lockmark_px_at']['360'])),
          'red_360_today': n48['at_360']['lever_red_px'], 'red_360_jpeg_today': n48['at_360_then_jpeg_q75_420']['lever_red_px'],
          'red_360_jpeg_96': n96['at_360_then_jpeg_q75_420']['lever_red_px'], 'n_widths': n_w,
          'fail_96_np': len(n96['lanczos_fail_widths_300_to_600']), 'fail_48_np': len(n48['lanczos_fail_widths_300_to_600']),
          'fail_96_ch': len(c96['lanczos_fail_widths_300_to_600']), 'fail_48_ch': len(c48['lanczos_fail_widths_300_to_600']),
          'ratio48': f'{so["lockmark_over_wordmark_capitals"]["48"]:.2f}', 'ratio96': f'{so["lockmark_over_wordmark_capitals"]["96"]:.2f}'}
    card['lede_html'] = paras(W['lede'], 'card-lede', fl)
    body = gain_cost(fill(W['gain'], fl), fill(W['cost'], fl))
    # the cards at actual size
    full = ''
    caps = {'Newsprint-48px': 'Today, on Newsprint: the sign-off at 48 px', 'Newsprint-96px': 'Proposal, on Newsprint: the sign-off at 96 px',
            'Charcoal-96px': 'Proposal, on Charcoal: the sign-off at 96 px'}
    for c in M['social_cards']:
        p1, p2 = M['pics'][('card', c['stem'], 1)], M['pics'][('card', c['stem'], 2)]
        w, h = png_size(p1)
        full += (f'<figure class="full">{img(p1, w, h, caps[c["stem"]] + ", the whole card at actual size", srcset2x=p2)}'
                 f'<figcaption class="caption">{esc(caps[c["stem"]])}, {w:,} by {h} px</figcaption></figure>')
    body += f'<h4 class="sub4">{esc(W["full_title"])}</h4>' + frame(f'<div class="fulls">{full}</div>', W['full_title'])
    # in a feed
    pd = SRC['id_plates']
    feed = ''
    for ground in ('Newsprint', 'Charcoal'):
        cols = ''
        for size, lab in ((48, 'Today, 48 px'), (96, 'Proposal, 96 px')):
            f = so[f'{ground.lower()}-{size}']
            cells = ''
            for wpx in (500, 360):
                pth = pd / f'{DATE}_Social-Card-{ground}-{size}px-At-{wpx}.png'
                need(pth.exists(), f'{pth.name} is missing')
                w, h = png_size(pth)
                r = f[f'at_{wpx}']
                cells += (f'<figure class="feedc">{img(pth, w, h, f"{lab} on {ground}, the card at {wpx} px wide as a 1x screen draws it", px=True)}'
                          f'<figcaption class="caption">At {wpx} px: {r["nodes_kept"]} of 8 nodes, {r["lever_red_px"]} red pixels; the lockmark {fmt_g(float(f["lockmark_px_at"][str(wpx)]))} px, '
                          f'{"under" if float(f["lockmark_px_at"][str(wpx)]) < 16 else "over"} its 16 px floor</figcaption></figure>')
            enl = ''
            for wpx in (500, 360):
                for jp in (False, True):
                    pth = pd / f'{DATE}_Sign-Off-{ground}-{size}px-At-{wpx}{"-Thumbnail-Jpeg" if jp else ""}-8x.png'
                    if not pth.exists():
                        warn(f'{pth.name} is missing')
                        continue
                    w, h = png_size(pth)
                    # the identity designer's pictures are eight times; set at half their pixel size they show each
                    # pixel of the reduced card as an exact 4 by 4 block (8 by 8 device pixels on a 2x screen)
                    need(w % 2 == 0 and h % 2 == 0, f'{pth.name}: odd size')
                    r = f[f'at_{wpx}_then_jpeg_q75_420' if jp else f'at_{wpx}']
                    t = f'{wpx} px{", then JPEG" if jp else ""}: {r["lever_red_px"]} red'
                    enl += (f'<figure class="enl">{img(pth, w // 2, h // 2, f"{lab} on {ground}, the corner at {wpx} px{" after the shrunk card is saved as a JPEG" if jp else ""}, four times larger", px=True)}'
                            f'<figcaption class="caption">{esc(t)}</figcaption></figure>')
            cols += (f'<div class="feed-col"><p class="col-h">{esc(lab)}</p><div class="stage stage--w">{cells}</div>'
                     f'<p class="st-l">The corner, four times</p><div class="enls">{enl}</div></div>')
        feed += f'<p class="vw-h label">On {ground}</p><div class="feed-row">{cols}</div>'
    body += f'<h4 class="sub4">{esc(W["feed_title"])}</h4><p class="pnote">{esc(W["feed_text"])} {esc(W["feed_test"])}</p>' + frame(feed, W['feed_title'])
    # the mark alone
    lm = SRC['identity'] / I['idf']['feed']['lockmark_master']
    need(lm.exists(), f'{lm} is missing')
    marks = ''
    for ground, cls, style in (('Newsprint', '', 'color:var(--oa-color-graphic-essential-on-newsprint)'),
                               ('Charcoal', ' stage--ch', 'color:var(--oa-color-graphic-essential-on-charcoal);--link:var(--oa-color-graphic-essential-on-charcoal)')):
        cells = ''
        for s, lab in ((48, 'Today, 48 px'), (96, 'Proposal, 96 px')):
            cells += f'<figure class="lk">{inline_svg(lm, s, s, style=style, label=f"The lockmark from the 48 px master at {s} px on {ground}")}<figcaption class="caption">{esc(lab)}</figcaption></figure>'
        marks += f'<div class="stage lk-st{cls}" data-red="signature">{cells}</div>'
    body += f'<h4 class="sub4">{esc(W["mark_title"])}</h4><p class="pnote">{esc(W["mark_text"])}</p><div class="marks">{marks}</div>'
    cap = pd / f'{DATE}_Social-Sign-Off-Comparison-1x.png'
    if cap.exists():
        body += f'<p class="pnote links"><a href="{src(cap)}">The identity designer’s full plate</a>. {esc(W["links_text"])}</p>'
    t48 = so['newsprint-48']['thumbnail_jpeg_q75_420_fail_widths_every_4th_300_to_600']
    t96 = so['newsprint-96']['thumbnail_jpeg_q75_420_fail_widths_every_4th_300_to_600']
    tc48 = so['charcoal-48']['thumbnail_jpeg_q75_420_fail_widths_every_4th_300_to_600']
    tc96 = so['charcoal-96']['thumbnail_jpeg_q75_420_fail_widths_every_4th_300_to_600']
    rows = [('Widths from 300 to 600 px that fail the test', f'Newsprint: today {fl["fail_48_np"]}, proposal {fl["fail_96_np"]}. Charcoal: today {fl["fail_48_ch"]}, proposal {fl["fail_96_ch"]}. Of {n_w}'),
            ('Shrunk, then saved as a JPEG, every fourth width', f'Newsprint: today fails at {t48["fails"]} of {t48["of"]}, the proposal at {t96["fails"]}. Charcoal: today {tc48["fails"]} of {tc48["of"]}, the proposal {tc96["fails"]}'),
            ('Lockmark against the card’s capitals', f'Today <span class="num">{fl["ratio48"]}</span> times; proposal <span class="num">{fl["ratio96"]}</span> times')]
    body += dl(rows)
    subjects = [(card['short'], c) for c in sc_list] or [(card['short'], None)]
    sh, lows = scores_block(subjects)
    card['lows'] = lows
    card['foot_extra'] = sh + open_items(subjects)
    card['not_ready'] = any(c.get('ready_for_board') is False for c in sc_list)
    d = card['designer']['social']
    card['recs'] = [('designer', {'label': 'The identity designer recommends', 'option': W['options'][d][0],
                                  'reason': f'At 96 px the card passes at every width from 300 to 600 px and through the shrunk JPEG, with no new drawing, and the corners keep L3’s proportion. If you keep 48 px, the risk stays as measured until a real upload in Phase 3 shows whether any feed saves a shrunk JPEG.'})]
    cd_opt, cd_reason = cd_rec_text(sc_list)
    rec = d
    if cd_opt:
        card['recs'].append(('cd', {'label': 'The creative director recommends', 'option': cd_opt, 'reason': cd_reason}))
        rec = 'keep' if re.search(r'\bkeep\b', cd_opt.lower()) else 'approve'
    card['groups'] = [{'name': 'so', 'label': None, 'rec': rec, 'options': [(k, W['options'][k][0], W['options'][k][1]) for k in ('approve', 'keep')]}]
    card['figs'] = {'from': rel(SRC['id_figs']), 'social_sign_off_96': {k: v for k, v in so.items() if k != 'method'}, 'derived': fl,
                    'cards_at_actual_size': M['social_cards']}
    return card_shell(card, body)


RENDER_CARD = {'housing': housing_card, 'utility': utility_card, 'fits': fits_card, 'print_l3': l3_card, 'social': social_card}


# ------------------------------------------------------------------------------------------------ assemble
def reply_section(cards, C):
    W = C['reply']
    lines = ''
    for c in cards:
        gs = ''
        for g in c['groups']:
            opts = ''.join(f'<label class="pill"><input type="radio" name="p{c["n"]}-{g["name"]}" value="{attr(v)}" data-card="{c["n"]}" '
                           f'data-group="{g["name"]}" aria-label="Card {c["n"]}, {attr(copy(g["label"] + ", " if g.get("label") else ""))}{attr(copy(lab))}"><span>{esc(short_label(lab))}</span></label>'
                           for v, lab, _ in g['options'])
            gl = f'<span class="pg-l">{esc(g["label"])}</span>' if g.get('label') else ''
            rl = next((short_label(lab) for v, lab, _ in g['options'] if v == g['rec']), None)
            rc = f'<span class="pg-l pg-rec">Recommended: {esc(rl)}</span>' if rl else ''
            gs += f'<span class="pgrp">{gl}{opts}{rc}</span>'
        if c.get('holds'):
            gs += f'<span class="pg-l" data-holds="{c["n"]}">Held back: none</span>'
        lines += (f'<li class="bl" data-line="{c["n"]}"><a class="bl-n" href="#card-{c["n"]}"><span class="n">{c["n"]}</span> {esc(c["short"])}</a>'
                  f'<span class="bl-o">{gs}</span><label class="pill pill--named"><input type="checkbox" data-named="{c["n"]}" aria-label="I approve card {c["n"]} by name">'
                  f'<span>I approve by name</span></label></li>')
    box = f'''<div class="reply oa-surface-prussian" id="reply-box" role="region" aria-labelledby="reply-h">
<h3 id="reply-h">{esc(W["title"])}</h3>{paras(W["text"])}<p>{esc(W["storage"])}</p>
<ol class="ballot">{lines}</ol>
<label class="label" for="reply-text">Reply</label>
<textarea id="reply-text" rows="9" readonly data-sample="{attr(copy(C["sample_reply"]))}">{esc(C["sample_reply"])}</textarea>
<div class="reply-row"><button type="button" id="copy-reply">Copy the reply</button><span id="copy-status" role="status" aria-live="polite"></span></div></div>'''
    return f'<section class="sec" id="reply" aria-labelledby="reply-sh"><h2 class="sec-h" id="reply-sh">Your reply</h2>{box}</section>'


def short_label(lab):
    m = re.match(r'^(Option) ([A-Z])\b', lab)
    return m.group(2) if m else lab.split(',')[0]


CSS = r'''
/* Drawings board C. The stage B drawings board's shell on Newsprint: the grid margins of tokens.css, White cards for
   words, Newsprint and Charcoal stages that hold the drawings at true size, one Prussian panel for the reply. One light
   look with every color set explicitly (D2-1097). No red of the board's own: Pillar Red appears only inside drawings. */
:root{--m:var(--oa-layout-grid-phone-small-margin);--g:var(--oa-layout-grid-phone-small-gutter);--max:82rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--np:var(--oa-color-surface-newsprint);--ch:var(--oa-color-surface-charcoal);
--wink-2:var(--oa-color-text-secondary-on-white);--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;color-scheme:light}
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
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.cover{padding:var(--oa-space-800) 0 0}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-400);max-width:16ch;text-wrap:balance}
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
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-400)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:0 0 var(--oa-space-300);text-wrap:balance}
.sec > .intro{margin-bottom:var(--oa-space-500)}
h3{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;text-wrap:balance}
h4,.sub4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-500) 0 var(--oa-space-200);text-wrap:balance}
.cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500)}
.cards > li{min-width:0}
.card{background:var(--white);color:var(--oa-color-text-primary-on-white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-300) var(--oa-space-200);min-width:0}
@media (min-width:48em){.card{padding:var(--oa-space-400) var(--oa-space-500)}}
.card .label,.card .caption{color:var(--wink-2)}
.card-head{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-100) var(--oa-space-300)}
@media (min-width:48em){.card-head{grid-template-columns:4.5rem minmax(0,1fr)}}
.card-head > div{min-width:0}
.card-n{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);font-variant-numeric:tabular-nums;margin:0}
.card-h{margin:0 0 var(--oa-space-150);max-width:32ch}
.card-lede{max-width:var(--oa-layout-measure-intro-max)}
.chips{margin:0 0 var(--oa-space-200);display:flex;flex-wrap:wrap;gap:var(--oa-space-100)}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);padding:1px 6px;white-space:nowrap;color:var(--oa-color-text-primary-on-white);background:var(--white)}
.chip--named,.chip--rec{background:var(--oa-color-palette-charcoal);color:var(--oa-color-text-primary-on-charcoal);border-color:var(--oa-color-palette-charcoal)}
.chips .chip{white-space:normal}
.chip--low,.chip--flag{border-width:2px;font-weight:700}
.chip--watch{border-style:dotted}
.card-body{margin-top:var(--oa-space-300);min-width:0}
.cols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-400) var(--oa-space-300)}
@media (min-width:40em){.cols--u{grid-template-columns:repeat(auto-fill,minmax(14rem,1fr))}}
@media (min-width:72em){.cols--h{grid-template-columns:repeat(3,minmax(0,1fr))}}
.col{min-width:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding-top:var(--oa-space-150)}
.col--rec{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:calc(var(--oa-space-150) - 3px)}
.col-h{font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-100);color:var(--oa-color-text-primary-on-white)}
.stage{background:var(--np);color:var(--ink);padding:var(--oa-space-200);width:max-content;max-width:100%}
.stage + .stage{margin-top:var(--oa-space-100)}
.stage--ch{background:var(--ch);color:var(--oa-color-text-primary-on-charcoal)}
.stage--pr{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian)}
.stage--w{background:var(--white);padding:0}
.stage .caption,.stage figcaption,.stage .st-l,.stage .st-h{color:var(--ink-2)}
.stage--ch .caption,.stage--ch figcaption,.stage--ch .st-l,.stage--ch .st-h{color:var(--oa-color-text-secondary-on-charcoal)}
.stage--pr .caption,.stage--pr figcaption{color:var(--oa-color-text-secondary-on-prussian)}
.st-h{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;margin:0 0 var(--oa-space-100)}
.st-l{font:var(--oa-type-caption);margin:var(--oa-space-100) 0 var(--oa-space-050)}
.sizes{display:flex;align-items:flex-end;gap:var(--oa-space-200)}
.sz{margin:0;display:flex;flex-direction:column;align-items:center;gap:var(--oa-space-100)}
.sz figcaption{font:var(--oa-type-caption);white-space:nowrap}
.ref{margin:var(--oa-space-100) 0 0}
img{display:block;max-width:none}
img.px{image-rendering:pixelated}
dl.figs{margin:var(--oa-space-200) 0 0;font:var(--oa-type-body-small)}
dl.figs div{padding:var(--oa-space-100) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
dl.figs dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);margin-bottom:2px}
dl.figs dd{margin:0}
dl.figs .chip{padding:0 4px;margin-left:.2em}
.mss{display:flex;flex-wrap:wrap;gap:2px var(--oa-space-150)}.ms{white-space:nowrap}.ms--low b{border:2px solid var(--oa-color-border-strong-on-white);padding:0 3px}
.pnote{font:var(--oa-type-body-small);margin-top:var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.frame{overflow-x:auto;overflow-y:hidden;max-width:100%;min-width:0}
.frame > *{width:max-content}
.hint{margin:var(--oa-space-100) 0 0}
/* Housing */
.nbs{display:flex;flex-wrap:wrap;gap:var(--oa-space-300)}
.nb{margin:0;min-width:0}.nb-l{font:var(--oa-type-body-small);margin:var(--oa-space-100) 0 0}.nb .caption{margin:0}
.h24s{display:flex;flex-wrap:wrap;gap:var(--oa-space-300)}
.pxs{display:flex;align-items:flex-end;gap:var(--oa-space-200)}
/* Pause and Filter */
.grids{display:flex;flex-wrap:wrap;gap:var(--oa-space-150);margin-top:var(--oa-space-150)}
.grid{margin:0;position:relative;width:max-content}
.grid::after{content:"";position:absolute;left:0;top:0;width:160px;height:160px;pointer-events:none;
  background-image:linear-gradient(to right,var(--gl) 1px,transparent 1px),linear-gradient(to bottom,var(--gl) 1px,transparent 1px);background-size:10px 10px}
.grid--np{--gl:rgba(93,99,109,.55)}.grid--ch{--gl:rgba(150,150,150,.6)}
.grid figcaption{margin-top:var(--oa-space-050)}
/* the 37 */
.summ{margin-top:var(--oa-space-200)}
.frs{list-style:none;margin:0;padding:0}
.fr-head{display:none}
.fr{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-100) var(--oa-space-200);padding:var(--oa-space-150) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);align-items:center}
.fr--five{background:linear-gradient(to right,var(--oa-color-tint-stone-n88) 0,var(--oa-color-tint-stone-n88) 4px,transparent 4px)}
.fr--five .fr-id{padding-left:var(--oa-space-150)}
.fr-name{margin:0;font:var(--oa-type-ui)}.fr-at{font:var(--oa-type-caption);color:var(--wink-2);display:block}
.chips-in .chip{margin:2px 4px 0 0}
.fr-pics{display:flex;align-items:center;gap:var(--oa-space-200);padding:var(--oa-space-100) var(--oa-space-150)}
.fr-p{margin:0;display:flex;flex-direction:column;align-items:center;gap:2px}
.fr-l{font:var(--oa-type-caption);color:var(--wink-2);display:block}
.fr-pics .fr-l{color:var(--ink-2)}
.fr-ink .num{font-weight:600}.fr-to{color:var(--wink-2)}.fr-sub{display:block;font:var(--oa-type-caption);color:var(--wink-2)}
.fr-pf,.fr-cd,.fr-ink{font:var(--oa-type-body-small);min-width:0}
.fr-note{grid-column:1/-1;font:var(--oa-type-body-small);margin:0;max-width:none}.fr-note .label{display:inline;margin-right:.4em}
.hold{display:inline-flex;align-items:center;gap:var(--oa-space-100);min-height:var(--oa-size-target-touch);cursor:pointer;font:var(--oa-type-body-small)}
.hold input{width:20px;height:20px;margin:0;accent-color:var(--oa-color-palette-charcoal)}
@media (min-width:64em){
  .fr-head,.fr{grid-template-columns:13rem 9.5rem 9rem 7rem minmax(0,1fr) 6.5rem}
  .fr-head{display:grid;gap:var(--oa-space-100) var(--oa-space-200);padding:0 0 var(--oa-space-100);margin-top:var(--oa-space-400)}
  .fr-h{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2)}
  .fr-pics .fr-l{display:none}
  .fr .fr-ink > .fr-l,.fr .fr-pf > .fr-l,.fr .fr-cd > .fr-l{display:none}
  .fr-pics{grid-column:2}
}
@media (max-width:63.99em){.fr-head{display:none}.fr-pics{width:max-content}
  .fr{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.fr-id,.fr-pics,.fr-cd,.fr-note{grid-column:1/-1}.fr-hold{grid-column:1/-1}}
/* identity */
.gc{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200) var(--oa-space-400);margin:var(--oa-space-100) 0 var(--oa-space-200)}
@media (min-width:56em){.gc{grid-template-columns:repeat(2,minmax(0,1fr))}}
.gc > div{border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding:var(--oa-space-050) var(--oa-space-200)}
.gc .gc-c{border-left-style:double;border-left-width:6px}
.gc p{margin:0;font:var(--oa-type-body-small)}.gc .label{display:block;margin-bottom:2px}
.l3s{display:grid;gap:var(--oa-space-300);width:max-content}
.l3{margin:0}.l3 figcaption{margin-top:var(--oa-space-100)}
.ovl{position:relative}.ovl-a,.ovl-b{position:absolute;left:0;top:0;line-height:0}
.fulls{display:grid;gap:var(--oa-space-300)}.full{margin:0}.full figcaption{margin-top:var(--oa-space-100)}
.feed-row{display:grid;grid-template-columns:repeat(2,max-content);gap:var(--oa-space-400)}
.feed-col{min-width:0}
.feedc{margin:0 0 var(--oa-space-150)}.feedc figcaption{margin-top:var(--oa-space-050);max-width:500px}
.enls{display:flex;flex-wrap:wrap;gap:var(--oa-space-150);align-items:flex-end;max-width:520px}
.enl{margin:0}.enl figcaption{margin-top:var(--oa-space-050);max-width:200px}
.vw-h{max-width:none;margin:var(--oa-space-300) 0 var(--oa-space-150)}
.marks{display:flex;flex-wrap:wrap;gap:var(--oa-space-200)}
.lk-st{display:flex;align-items:flex-end;gap:var(--oa-space-400)}
.lk{margin:0;display:flex;flex-direction:column;align-items:flex-start;gap:var(--oa-space-100)}
.links a{font-weight:600}
.tw{overflow-x:auto;border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);background:var(--white);margin-top:var(--oa-space-200)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-100) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--oa-color-tint-white-n55)}
tbody th{font-weight:600}
td.num{text-align:center}
td.low span:first-child{display:inline-block;min-width:1.9em;border:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);font-weight:700}
table.sc-t{min-width:40rem}table.fig-t{min-width:28rem}
.card-foot{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-400) var(--oa-space-600);margin-top:var(--oa-space-500);border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);padding-top:var(--oa-space-300)}
@media (min-width:64em){.card-foot{grid-template-columns:minmax(0,1fr) minmax(17rem,22rem)}}
.foot-main{min-width:0}
.rec .label,.approve .label{display:block;margin-bottom:2px}
.rec + .rec{margin-top:var(--oa-space-300)}
.rec--cd{border-left:var(--oa-border-width-bar) solid var(--oa-color-border-strong-on-white);padding-left:var(--oa-space-200)}
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
.holds-l{margin:var(--oa-space-100) 0 0}
.nl{display:block;font:var(--oa-type-body-small);color:var(--wink-2);margin:var(--oa-space-200) 0 var(--oa-space-100)}
textarea{display:block;width:100%;font:var(--oa-type-body);color:var(--oa-color-text-primary-on-white);background:var(--white);
  border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong-on-white);border-radius:0;padding:var(--oa-space-150);resize:vertical}
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
.pg-l{font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-prussian);align-self:center}
.pg-rec{margin-left:var(--oa-space-100)}
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
.foot p{font:var(--oa-type-caption);color:var(--ink-2);max-width:none}
@media print{.toc,.ans,.reply,.hint,.fr-hold{display:none!important}.frame{overflow:visible}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''

JS = r'''
(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  // Each drawing sits on whole CSS pixels, so a 1x screen draws it as its file is drawn (D2-565).
  function snap() {
    $$('.snap').forEach(function (el) { el.style.transform = ''; });
    $$('.snap').forEach(function (el) {
      if (el.closest('.ovl')) return;
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
  // Answers. A card's controls and its line in the reply panel share one store, saved in this browser only.
  var out = document.getElementById('reply-text');
  if (!out) return;
  var KEY = 'oa-stage-c-drawings-board:' + (document.querySelector('.board') || document.body).getAttribute('data-answers');
  var store = {};
  try { store = JSON.parse(window.localStorage.getItem(KEY) || '{}') || {}; } catch (e) { store = {}; }
  function save() { try { window.localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }
  var cards = $$('.card[data-card]');
  function rec(n) { var o = store[n]; if (!o) { o = store[n] = { g: {}, named: false, note: '', holds: [] }; } if (!o.g) o.g = {}; if (!o.holds) o.holds = []; return o; }
  function words(a) { return a.length < 3 ? a.join(' and ') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]; }
  function holdLabels(n) {
    var s = store[n]; if (!s || !s.holds || !s.holds.length) return [];
    return s.holds.map(function (id) { var b = document.querySelector('input[data-hold="' + id + '"][data-card="' + n + '"]'); return b ? b.getAttribute('data-label') : id; });
  }
  function paint() {
    $$('input[type=radio][data-card]').forEach(function (r) { var s = store[r.getAttribute('data-card')]; r.checked = !!(s && s.g && s.g[r.getAttribute('data-group')] === r.value); });
    $$('input[type=checkbox][data-named]').forEach(function (k) { var s = store[k.getAttribute('data-named')]; k.checked = !!(s && s.named); });
    $$('input[type=checkbox][data-hold]').forEach(function (k) { var s = store[k.getAttribute('data-card')]; k.checked = !!(s && s.holds && s.holds.indexOf(k.getAttribute('data-hold')) >= 0); });
    $$('textarea[data-note]').forEach(function (t) { var s = store[t.getAttribute('data-note')]; if (document.activeElement !== t) t.value = (s && s.note) || ''; });
    $$('[data-holds]').forEach(function (el) { var h = holdLabels(el.getAttribute('data-holds')); el.textContent = 'Held back: ' + (h.length ? words(h) : 'none'); });
  }
  function compose() {
    var lines = [];
    cards.forEach(function (c) {
      var n = c.getAttribute('data-card'), s = store[n]; if (!s) return;
      var parts = [], allRec = true, any = false, holds = holdLabels(n);
      $$('.grp-o', c).forEach(function (g) {
        var name = g.getAttribute('data-group'), v = s.g && s.g[name];
        if (!v) { allRec = false; return; }
        any = true;
        var r = c.querySelector('input[type=radio][data-group="' + name + '"][value="' + v + '"]');
        var t = r ? r.getAttribute('data-short') : v;
        if (holds.length && v === 'some') t += ', all but ' + words(holds) + ', which I hold back';
        parts.push(t);
        if (v !== g.getAttribute('data-rec')) allRec = false;
      });
      if (holds.length && !any) parts.push('I hold back ' + words(holds));
      var line = parts.join('; ');
      if (any && allRec && !holds.length) line += ', as recommended';
      if (line) line += '.';
      if (s.named) line = (line ? line + ' ' : '') + 'Approved by name.';
      var note = (s.note || '').trim(); if (note) line = line ? line + ' ' + note : note;
      if (line) lines.push('Card ' + n + ', ' + c.getAttribute('data-short') + ': ' + line);
    });
    out.value = lines.length ? lines.join('\n') : out.getAttribute('data-sample');
  }
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches && t.matches('input[type=radio][data-card]')) {
      var o = rec(t.getAttribute('data-card'));
      o.g[t.getAttribute('data-group')] = t.value;
      if (t.value === 'all') o.holds = [];
    } else if (t.matches && t.matches('input[type=checkbox][data-named]')) { rec(t.getAttribute('data-named')).named = t.checked; }
    else if (t.matches && t.matches('input[type=checkbox][data-hold]')) {
      var h = rec(t.getAttribute('data-card')), id = t.getAttribute('data-hold');
      h.holds = h.holds.filter(function (x) { return x !== id; });
      if (t.checked) { h.holds.push(id); h.g.fits = 'some'; }
    }
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


def build_page(cards, C, built):
    html_cards = {c['n']: c['html'] for c in cards}
    groups_html = ''
    for gk in ('drawings', 'identity'):
        G = C['groups'][gk]
        inner = ''.join(f'<li>{html_cards[c["n"]]}</li>' for c in cards if GROUP_OF[c['key']] == gk)
        groups_html += (f'<section class="sec" id="g-{gk}" aria-labelledby="g-{gk}-h"><h2 class="sec-h" id="g-{gk}-h">{esc(G["title"])}</h2>'
                        f'{paras(G.get("intro"), "intro")}<ol class="cards">{inner}</ol></section>')
    toc = ''.join(f'<li><a href="#card-{c["n"]}"><span class="n">{c["n"]}</span> {esc(c["short"])}</a></li>' for c in cards)
    toc += '<li><a href="#reply"><span class="n">→</span> Your reply</a></li>'
    legend = ''.join(f'<div><p><b>{esc(x["term"])}</b>{md(fill(x["text"]))}</p></div>' for x in C['legend'])
    answers_key = hashlib.sha1(json.dumps([(c['n'], c['short'], c['groups']) for c in cards], sort_keys=True, default=str).encode()).hexdigest()[:12]
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview"><meta name="color-scheme" content="light">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{TOKENS.read_text()}
{CSS}</style></head>
<body><main class="board" data-view-root="overview" data-answers="{answers_key}">
<header class="cover">
<p class="mast"><b>Oath &amp; Action</b><span class="label">{esc(C["kicker"])}</span></p>
<p class="label" style="margin-top:var(--oa-space-800)">For Dustin Cathcart · {words_date(built)}</p>
<h1>{esc(fill(C["title"]))}</h1>
<div class="cover-grid"><div><p class="intro">{md(fill(C["deck"]))}</p><div class="facts">{paras(C["facts"])}</div></div>
<div class="ask"><h2>What we ask of you</h2><ol>{"".join(f"<li>{md(fill(x))}</li>" for x in C["ask"])}</ol>
<p class="caption" style="margin:0 0 var(--oa-space-050)">A reply can be this short:</p><p class="q">{esc(C["sample_reply"])}</p></div></div>
<div class="legend"><h2>{esc(C["legend_title"])}</h2>{legend}</div>
<nav class="toc" aria-label="Cards on this board"><ol>{toc}</ol></nav>
</header>
{groups_html}
{reply_section(cards, C)}
<footer class="foot"><p>{esc(C["footer"])}</p><p>Built {words_date(built)} at {words_time(built)} UTC by <code>work/build/scripts/phase-2/stage_c_drawings_board_build.py</code> from the designers’ manifests and files, the creative director’s scores, the identity designer’s figures and plates, and the engineer’s two checks run on today’s files.</p></footer>
</main>
<script>{JS}</script></body></html>'''


def main():
    global N_CARDS
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    for k in ('content', 'scores', 'out', 'publish', 'scratch'):
        ap.add_argument(f'--{k}', type=pathlib.Path, default=DEF[k])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--reuse-checks', action='store_true', help='reuse the last check results (layout work only)')
    a = ap.parse_args()
    C = load_json(a.content, 'the content file')
    eo = C.get('editor_overrides') or []
    need(isinstance(eo, list) and all(isinstance(x, dict) and isinstance(x.get('old'), str) and x['old'] and isinstance(x.get('new'), str) for x in eo),
         'content.editor_overrides: a list of {"old": "exact text", "new": "replacement"}')
    OVERRIDES[:] = [[x['old'], x['new'], 0] for x in eo]
    need('—' not in json.dumps(C, ensure_ascii=False), 'content: an em dash')
    S = None
    if a.scores.exists():
        S = ov_deep(load_json(a.scores, 'the scores file'))
        need(isinstance(S.get('cards'), list), 'scores: no cards')
    else:
        warn(f'scores pending: {rel(a.scores) if str(a.scores).startswith(str(ROOT)) else a.scores} does not exist yet')
    SC = score_cards(S)
    I = build_inputs(C)
    DR = designer_recs(I)
    for k, v in (('housing', C['cards']['housing']['designer_rec']['option']), ('filter', C['cards']['utility']['designer_rec']['filter']),
                 ('pause', C['cards']['utility']['designer_rec']['pause']), ('fits', C['cards']['fits']['designer_rec']['option'])):
        if DR.get(k) and DR[k] != v:
            warn(f'the content file says the icon designer recommends {v} for {k}; the notes say {DR[k]}')
    for k in ('housing', 'filter', 'pause', 'fits', 'h24', 'print_l3', 'social'):
        if k not in DR:
            warn(f'no recommendation for {k} in the designers’ questions')
    if 'r06_skipped' not in DR:
        NOTICES.append('the icon designer’s notes have no R-06 question; nothing to leave off the board')
    M = build_model(C, S, I, a.scratch, a.reuse_checks)
    make_pictures(I, M, a.scratch)
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL.update({'built_date': words_date(built), 'built_time': words_time(built), 'n_fits': len(M['rows']), 'flag': fmt_like(M['flag']),
                 'watch': fmt_like(M['watch']), 'pairs': f'{M["pairs"]:,}', 'n_masters': I['n_masters']})
    cards = []
    for n, k in enumerate(CARD_ORDER, 1):
        W = C['cards'][k]
        cards.append({'n': n, 'key': k, 'short': fill(W['short']), 'title': fill(W['title']), 'approve': fill(W['approve']),
                      'pending': not SC[k], 'designer': {'housing': DR.get('housing') or W.get('designer_rec', {}).get('option'),
                                                          'h24': DR.get('h24', 'keep'), 'filter': DR.get('filter'), 'pause': DR.get('pause'),
                                                          'fits': DR.get('fits', 'all'), 'print_l3': DR.get('print_l3', 'approve'), 'social': DR.get('social', 'approve')}})
        if not SC[k] and S is not None:
            warn(f'card {n} ({cards[-1]["short"]}): the scores file has no card for it, so it shows "scores pending"')
    N_CARDS = len(cards)
    for c in cards:
        k = c['key']
        W = C['cards'][k]
        if k == 'utility':
            cd_opt, _ = cd_rec_text(SC[k])
            c['rec_pause'] = c['designer']['pause'] or 'approve'
            c['rec_filter'] = c['designer']['filter'] or 'A'
            if cd_opt:
                m = re.search(r'filter[^.;]*?\b(?:option\s+|redraw\s+)?([AB])\b', cd_opt, flags=re.I) or re.search(r'\b(?:option|redraw)\s+([AB])\b', cd_opt, flags=re.I)
                if m:
                    c['rec_filter'] = m.group(1).upper()
                if re.search(r'keep[^.;]*pause|pause[^.;]*keep', cd_opt, flags=re.I):
                    c['rec_pause'] = 'keep'
        if k not in ('print_l3', 'social'):     # the identity cards fill their ledes from the figures file
            c['lede_html'] = paras(W.get('lede'), 'card-lede')
        c['html'] = RENDER_CARD[k](c, C, I, M, SC)
    for c in cards:
        if c.get('lows'):
            warn(f'card {c["n"]} ({c["short"]}): scores under 4 ({join_words(c["lows"])}); the brief sends the drawing back before the board is published')
        if c.get('not_ready'):
            warn(f'card {c["n"]} ({c["short"]}): not ready for the board in the scores file')
        if c.get('naming_missing') and S is not None:
            warn(f'card {c["n"]}: no naming test from the creative director for one or more Housing options')
    page = build_page(cards, C, built)
    page = re.sub(r'(<(p|span|legend|th)\b[^>]*?(?:class="[^"]*\b(?:label|vw-h|st-h|fr-h)\b[^"]*"|scope="col")[^>]*>|<legend>)(.*?)(</(?:p|span|legend|th)>)',
                  lambda m: m.group(1) + (m.group(3) if 'class="nc"' in m.group(3) else nx(m.group(3))) + m.group(4), page, flags=re.S)
    for o in OVERRIDES:
        if not o[2]:
            warn(f'editor override matches nothing in the other owners’ words: "{o[0][:70]}"')
    text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)))
    need('—' not in text, 'em dash on the board: ' + text[max(0, text.find('—') - 60):text.find('—') + 20])
    if '–' in text.replace('<td class="num"><span>–', ''):
        i = text.find('–')
        warn('an en dash on the board: ' + text[max(0, i - 40):i + 20])
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text, flags=re.I)})
    if flagged:
        warn('flagged words on the board: ' + ', '.join(flagged))
    if 'answers to its people' in text and TAGLINE not in text.replace('’', "'"):
        raise BoardError('the tagline is quoted inexactly')
    codes = sorted(set(re.findall(r'\b(?:DR|D2)-\d+\b', text)))
    foot = html.unescape(C['footer'])
    stray = [x for x in codes if x not in foot]
    if stray:
        warn('decision numbers outside the footer, in words from other owners’ files: ' + ', '.join(stray))
    # figures the creative director's words cite that this run did not measure (reported, not warned: they are the
    # creative director's own words)
    measured = {fmt_like(M['flag']), fmt_like(M['watch'])}
    for key in ('likeness_fits', 'likeness_housing', 'likeness_neutral_masters'):
        L = M['R'][key]
        for x in L.get('flagged', []) + L.get('watch', []) + L.get('own', []) + L.get('options', []) + L.get('closest', []):
            measured.add(fmt_like(x['likeness']))
    for v in re.findall(r'(?<![\d.])(\d+\.\d+)', json.dumps(I['idf'])):
        measured.add(v[:5])
        measured.add(f'{float(v):.3f}')
    for r in M['rows']:
        for x in [r['like_own']] + [f['likeness'] for f in r['flags']] + [f['masters'] for f in r['flags']]:
            if x is not None:
                measured.add(fmt_like(x))
    for x in M['five']:
        for v in (x['masters'], x['fits']):
            if v is not None:
                measured.add(fmt_like(v))
    for L, h in M['housing_like'].items():
        for v in list(h['against'].values()) + [(h['closest'] or {}).get('likeness'), (h['sibling'] or {}).get('likeness')]:
            if v is not None:
                measured.add(fmt_like(v))
    cd_words = json.dumps(S, ensure_ascii=False) if S else ''
    unmeasured = sorted({x for x in re.findall(r'\b0\.\d{3}\b', cd_words) if x not in measured})
    if unmeasured:
        NOTICES.append('figures in the creative director’s words that neither this run nor the identity figures file holds: ' + ', '.join(unmeasured[:20]))
    # outputs
    out_dir = a.out.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    def resolve(prefix_fn):
        return re.sub(r'@@A:([^@]+)@@', lambda m: prefix_fn(m.group(1)), page)
    repo_page = resolve(lambda k: os.path.relpath(ROOT / k, out_dir).replace(os.sep, '/'))
    a.out.write_text(repo_page)
    chk_dir = a.scratch / 'check-copy'
    chk_dir.mkdir(parents=True, exist_ok=True)
    (chk_dir / a.out.name).write_text(resolve(lambda k: 'file://' + str(ROOT / k)))
    refs = sorted(ASSET_REFS)
    names = {}
    for r in refs:
        b = pathlib.Path(r).name
        need(b not in names or names[b] == r, f'two files share the name {b}: {names.get(b)} and {r}')
        names[b] = r
    img_bytes = sum((ROOT / r).stat().st_size for r in refs)
    total = len(repo_page.encode()) + img_bytes
    need(total < LIMIT, f'the board and its files come to {total / 1e6:.1f} MB, over 15 MB')
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
    figs = {'built': built.isoformat(), 'scores_file': rel(a.scores) if a.scores.exists() else None,
            'thresholds': {'flag': M['flag'], 'watch': M['watch'], 'pairs': M['pairs'], 'masters': I['n_masters']},
            'checks': {'commands': M['R']['commands'], 'exit_codes': M['R']['codes'], 'results': M['R']['files'],
                       'likeness_run': M['R']['likeness_fits'].get('run'), 'renderer': M['R']['likeness_fits'].get('renderer')},
            'designer_recommendations': DR, 'notices': NOTICES, 'warnings': WARN,
            'cards': [{'n': c['n'], 'key': c['key'], 'title': c['title'], 'groups': c['groups'], 'scores_pending': c['pending'],
                       'scores_under_4': c.get('lows', []), 'recommendations': c['recs'], 'figures': c.get('figs')} for c in cards],
            'files': refs, 'bytes': {'page': len(repo_page.encode()), 'files': img_bytes, 'total': total}}
    (out_dir / f'{STEM}-Figures.json').write_text(json.dumps(figs, indent=1, default=str, ensure_ascii=False))
    print(f'wrote {rel(a.out)} ({len(repo_page.encode()) / 1e3:.0f} kB) with {len(refs)} files ({img_bytes / 1e6:.2f} MB): {total / 1e6:.2f} MB in all; {len(cards)} cards')
    print(f'wrote {pub_html} and {len(files)} files in {pdir}; publish map in {a.publish / "files.json"}')
    print(f'wrote the check copy {chk_dir / a.out.name}')
    for n in NOTICES:
        print('notice', n)
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
