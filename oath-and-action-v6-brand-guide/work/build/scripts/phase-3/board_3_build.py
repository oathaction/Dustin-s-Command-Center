"""Build board 3 of Phase 3 (November 20, 2026; the board builder, working as the design director).

Copied from board 2's builder (board_2_build.py), which stays as it is, as every earlier builder does. Usage:
    python3 -I work/build/scripts/phase-3/board_3_build.py [--reuse] [--check] [--strict] [--scratch DIR] [--out PATH]
                                                           [--decisions FILE] [--final PAGE] [--final-report FILE]
                                                           [--no-browser]

Reads, on every run:
    work/boards/phase-3/review-4-5/board-3/20261120_Board-3-Content.json   the board's own words and the files it reads
    work/handoffs/phase-3/20261120_Board-3-Decisions.json                  panel 1's items, the pages they name and the
                                                                            Rule 01.9 and DR-229 counts (the data lead's;
                                                                            --decisions reads another file, for a test only)
    the final build (the content file's slots.final_page, or --final) and its build report (slots.final_report, or
        --final-report, else the page's name with -Build-Report.json): every "final" photograph, each chart's printed
        title, evidence label, source line and table, the width it draws each chart at 1440 and 390 px, every entry's
        anchor, and every weight. The board never builds the guide itself.
    the earlier pages the decisions file names under "pages" (V9 to V12), for the "before" photographs
    work/handoffs/phase-3/20261112_Chapter-14-Plan.json                    round 4's 13 forms, by family
    the chart kit's own captures, built afresh into <scratch>/kit-out/ by oa-chart.mjs at the widths the guide draws
    work/build/guide/chapters/14-data-visualization.json and 15-systems-graphics.json: round 5's charts, chapter 15's rules
    the nine readers' reports, the creative director's scores, rescore and second pass rescore, and this board's scores
        when they land; the check files the main session names in the content file
    work/build/tokens/tokens.css (the :root tokens the page's styles name, and only those)
    work/ledger/*_Decision-Log.md and *_Open-Questions.md                  every code in a reference line must exist
Writes:
    work/boards/phase-3/review-4-5/board-3/20261120_Board-3.html           the board (no scripts; the host wraps it)
    work/boards/phase-3/review-4-5/board-3/img/                            every picture it shows, composed
    work/boards/phase-3/review-4-5/board-3/20261120_Board-3-Figures.json   every figure it prints, with its source
    work/boards/phase-3/review-4-5/board-3/20261120_Board-3-Check-Results.json  (written by dataviz_check.js)
    <scratch>/  the kit's builds, the photographs, the pictures made in scratch copies, the measurements and the cache

--reuse keeps a kit capture when its spec, data, form module, the kit's shared files and the widths asked are unchanged,
and a photograph or measurement when its element's HTML, the page's styles and scripts, the window width and the
picture's setup are unchanged; without it, every capture and photograph is made afresh. --no-browser opens no browser at
all: it builds the page from the captures already in scratch and shows the rest as waiting. Before every browser run the
build runs the machine's browsers.sh and waits until it prints "OK to open one". --check runs dataviz_check.js with
--board --no-captures, from work/build, on the page itself and on a copy wrapped as the host wraps it; the page carries no
<html> tag by contract, so axe's html-has-lang is the one failure allowed on the page itself. --strict exits 1 on any
warning. A part whose file is missing or still pending prints "Waiting for". Images the page no longer names are removed.
"""
import argparse
import datetime
import glob
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[4]
SCRIPTS2 = ROOT / 'work/build/scripts/phase-2'
SCRIPTS3 = ROOT / 'work/build/scripts/phase-3'
sys.path.insert(0, str(SCRIPTS3))
import board_1_build as B1  # noqa: E402   board 1's Markdown readers and quoted-words rules (D3-206)

DATE = '20261120'
BOARD_DIR = ROOT / 'work/boards/phase-3/review-4-5/board-3'
IMG = BOARD_DIR / 'img'
CONTENT = BOARD_DIR / f'{DATE}_Board-3-Content.json'
FIGURES = BOARD_DIR / f'{DATE}_Board-3-Figures.json'
OUT = BOARD_DIR / f'{DATE}_Board-3.html'
SCRATCH_ROOT = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad')
SCRATCH_DEFAULT = SCRATCH_ROOT / 'c08/board-3/builder'
BROWSERS_SH = SCRATCH_ROOT / 'c08/browsers.sh'
LABEL_FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
NEWSPRINT = (0xDC, 0xD9, 0xD2)
LABEL_INK = (0x4E, 0x53, 0x5B)
PAD = 16                  # B2-S12: the inner margin round a picture on Charcoal
CONTENT_W = 1280          # the widest picture that sits in the board's column at a 1440 px window with no frame scroll
REGION_W = 288            # a picture wider than a 320 px window's column scrolls in its own named frame
FILES_AIM = 260           # the brief: about 250 pictures
BYTES_AIM = 60_000_000    # and under 60 MB, so one publish carries it
LIMIT_FILES = 511
LIMIT_TOTAL = 256_000_000
LIMIT_IMAGE = 15_000_000
LIMIT_PAGE = 16_000_000
FLAGGED = B1.FLAGGED
CODE_DEC = B1.CODE_DEC
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp')
DESK, PHONE = 1440, 390   # the two windows the board shows each chart at
# studio codes a teammate's words may carry in a parenthesis; they move to the panel's reference line
STUDIO = r'(?:DR|D3|D2|D1|G1|G2|DC|Q|C|RS|CR|AX|CE|NB|ST|PR|RP|DF|DD|CA|DT|UX|R4|R5|AX-S|CR-S)-[A-Z]{0,2}\d+[a-z]?'

C = {}
D = None                  # the decisions file, or None while it is missing
LOG = set()
SCRATCH = SCRATCH_DEFAULT
WARN, NOTES, FIG, QUOTED, LINKED = [], [], {}, [], set()
FILL = {}
IMAGES = {}
STATUS = {}
CACHE = {}
ANCHORS = set()
PREVIEW_IDS = None        # the ids on the final page, which version 13 publishes
LINKS = []                # every link to the chapters page, one entry a link
FAILS = []                # B2-M6: what fails the build outright, whatever --strict says
MEAS = {}                 # spec -> {window: the guide's measure of its figure}
SPECINFO = {}             # spec -> {'form', 'title', 'rule'}
FORMPIC = {}              # spec -> (panel 2's Newsprint picture, its rule, its alt)
CHARCOAL = None           # the Charcoal ground, from tokens.css
PAGES = {}                # page key -> {'path', 'text', 'frame'}
NO_BROWSER = False
RECIPE_V = {'rail-focus': 'rail-focus-2', 'clip': 'clip-1'}   # a recipe's version: a change to it in the renderer takes its pictures again
MOVED_REFS = []           # studio codes moved out of a teammate's words, for the panel's reference line


def fail(msg):
    FAILS.append(msg)
    print('FAIL', msg)


class BoardError(Exception):
    pass


def warn(msg):
    if msg in WARN:
        return
    WARN.append(msg)
    print('warning', msg)


def need(cond, msg):
    if not cond:
        raise BoardError(msg)


esc = B1.esc
nw = B1.nw
cap = B1.cap
join_words = B1.join_words


def rel(p):
    p = pathlib.Path(p)
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p).replace(str(SCRATCH_ROOT), '[scratch]')


def read(p):
    p = ROOT / p
    return p.read_text() if p.exists() else None


def fill(s, extra=None):
    d = dict(FILL)
    if extra:
        d.update(extra)
    return re.sub(r'\{([a-z0-9_]+)\}', lambda m: str(d[m.group(1)]) if m.group(1) in d else m.group(0), s or '')


def sha(*parts):
    h = hashlib.sha1()
    for p in parts:
        h.update(p if isinstance(p, bytes) else str(p).encode())
        h.update(b'\0')
    return h.hexdigest()


def file_sig(p):
    st = pathlib.Path(p).stat()
    return f'{st.st_size}-{st.st_mtime_ns}'


def when_utc(ts):
    d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    return d.strftime('%B ') + str(d.day) + d.strftime(', %Y at %H:%M UTC')


def text_of(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment or ''))).strip()


def n_or_word(n):
    return nw(n) if isinstance(n, int) else str(n)


def rid_anchor(rid):
    return 'rule-' + str(rid).replace('.', '-')


def rule_href(rid):
    """A rule's live entry in the chapters page (version 13); the anchor must be on the final build's page."""
    a = rid_anchor(rid)
    if PREVIEW_IDS is not None and a not in PREVIEW_IDS:
        fail(f'Rule {rid}: #{a} is not on the final build’s page')
    LINKED.add(a)
    LINKS.append(a)
    return f'{C["slots"]["preview_url"]}#{a}'


def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '-', str(s)).strip('-')


# ------------------------------------------------------------------------------------------------------- the pages
def scratch_path(s):
    """A slot's path: '[scratch]/...' under this session's scratch folder, else relative to the project."""
    if not s:
        return None
    s = str(s)
    if s.startswith('[scratch]/'):
        return SCRATCH_ROOT / s[len('[scratch]/'):]
    p = pathlib.Path(s)
    return p if p.is_absolute() else ROOT / p


def load_pages(final, final_report):
    """The final build (the board never builds the guide: it reads the page the main session names) and the earlier pages
    the decisions file names. -> G, the final page's record, in board 2's shape."""
    pages = dict((D or {}).get('pages') or {})
    for k, v in list(pages.items()):
        if k == 'final':
            continue
        p = ROOT / v
        PAGES[k] = {'path': p, 'text': None, 'frame': None}
        if not p.is_file():
            warn(f'the decisions file names {v} for {k}, and it is not there')
    fp = final or scratch_path(C['slots'].get('final_page'))
    rp = final_report or scratch_path(C['slots'].get('final_report'))
    if fp and not rp:
        rp = fp.with_name(fp.stem + '-Build-Report.json')
    ok = bool(fp and fp.is_file())
    PAGES['final'] = {'path': fp, 'text': None, 'frame': None}
    report = {}
    if rp and rp.is_file():
        report = json.loads(rp.read_text())
        if ok and report.get('bytes') and report['bytes'] != fp.stat().st_size:
            warn(f'the final build’s report gives {report["bytes"]:,} bytes and its page is {fp.stat().st_size:,}')
    elif ok:
        warn(f'the final build’s report is not there: {rel(rp) if rp else "no path"}')
    if not ok:
        warn('the final build’s page is not there; every final picture waits for it')
    text = page_text('final') if ok else ''
    ANCHORS.update(re.findall(r'\sid="(rule-1[0-9]-\d+)"', text))
    FIG['final_build'] = {'page': rel(fp) if fp else None, 'report': rel(rp) if rp else None, 'bytes': report.get('bytes'),
                          'built': report.get('built'), 'warnings': len(report.get('warnings', [])), 'rules': report.get('rules'),
                          'specimens': report.get('specimens_placed'), 'label': C['slots'].get('final_label')}
    FIG['pages'] = {k: rel(v['path']) if v['path'] else None for k, v in PAGES.items()}
    return {'ok': ok and bool(report), 'usable': ok, 'page': fp, 'text': text, 'report': report,
            'mtime': fp.stat().st_mtime if ok else None}


def page_text(key):
    P = PAGES.get(key)
    if not P or not P['path'] or not P['path'].is_file():
        return ''
    if P['text'] is None:
        P['text'] = P['path'].read_text()
    return P['text']


def page_frame(key):
    P = PAGES.get(key)
    if P is None:
        return ''
    if P['frame'] is None:
        P['frame'] = page_frame_sig(page_text(key))
    return P['frame']


def element_html(page, el):
    """The source of the element an id names, or a 'tag.class' selector names (its first match), its own tag balanced,
    so a picture's signature changes only when it does."""
    el = el.lstrip('#')
    if '.' in el and not el.startswith(('fig-', 'oac-', 's-', 'rule-')):
        tag, cls = el.split('.', 1)
        m = re.search(r'<' + re.escape(tag) + r'\b[^>]*\bclass="(?:[^"]*\s)?' + re.escape(cls) + r'(?:\s[^"]*)?"', page)
        if not m:
            return None
        start = m.start()
    else:
        i = page.find(f'id="{el}"')
        if i < 0:
            return None
        start = page.rfind('<', 0, i)
    tag = re.match(r'<([a-zA-Z0-9]+)', page[start:]).group(1)
    depth = 0
    for m in re.compile(r'<(/?)' + tag + r'\b[^>]*?(/?)>').finditer(page, start):
        if m.group(1):
            depth -= 1
        elif not m.group(2):
            depth += 1
        if depth == 0:
            return page[start:m.end()]
    return page[start:]


def css_selector(el):
    el = el.lstrip('#')
    if '.' in el and not el.startswith(('fig-', 'oac-', 's-', 'rule-')):
        return el
    return f'#{el}'


def page_frame_sig(page):
    """Every style and script of the guide page that is not a data island: what draws every element."""
    parts = re.findall(r'<style\b[^>]*>(.*?)</style>', page, flags=re.S)
    parts += re.findall(r'<script\b(?![^>]*(?:application/json|data-oa-chart-data))[^>]*>(.*?)</script>', page, flags=re.S)
    return sha(*parts)


def browser_gate(label):
    """The machine's rule: before each browser run, run browsers.sh and open one only when it prints "OK to open one".
    Waits up to 20 minutes, asking every 30 seconds; its exit status is never read."""
    if NO_BROWSER:
        return False
    for k in range(40):
        r = subprocess.run(['bash', str(BROWSERS_SH)], capture_output=True, text=True)
        out = (r.stdout or '').strip()
        if 'OK to open one' in out:
            NOTES.append(f'{datetime.datetime.now(datetime.timezone.utc):%H:%M:%S} UTC {label}: {out}')
            return True
        print(f'waiting to open a browser for {label}: {out}')
        time.sleep(30)
    warn(f'no browser opened for {label}: browsers.sh never printed "OK to open one" in 20 minutes')
    return False


def run_render(jobs, label):
    """One browser at a time: board_3_render.js opens each page in turn and closes the browser at the end."""
    if not jobs or not browser_gate(label):
        return
    jp = SCRATCH / f'render-jobs-{label}.json'
    jp.write_text(json.dumps(jobs))
    t0 = time.time()
    r = subprocess.run(['node', str(SCRIPTS3 / 'board_3_render.js'), str(jp)], cwd=ROOT / 'work/build',
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    (SCRATCH / f'render-{label}.log').write_text(r.stdout + r.stderr)
    FIG.setdefault('render_seconds', {})[label] = round(time.time() - t0)
    for line in r.stdout.splitlines():
        if line.startswith('failed') or line.startswith('page error'):
            warn('render: ' + line)
    if r.returncode != 0 and 'failed' not in r.stdout:
        warn('the renderer stopped: ' + r.stderr[-300:])


def run_shots(items, reuse, label='guide'):
    """items: dicts {key, page, el, w, measure, text_scale, actions, recipe, session} -> {key: path}. One page load per
    page, window and session, only for the items that changed. Actions add up through a session's items in order."""
    shots = SCRATCH / 'shots'
    shots.mkdir(parents=True, exist_ok=True)
    sig_file = SCRATCH / 'shot-sigs.json'
    sigs = json.loads(sig_file.read_text()) if sig_file.exists() else {}
    paths, todo, prefix = {}, {}, {}
    for it in items:
        key, pk, el, w = it['key'], it['page'], it['el'], it['w']
        measure = bool(it.get('measure'))
        p = shots / (f'{key}.json' if measure else f'{key}.png')
        paths[key] = p
        text = page_text(pk)
        if not text:
            continue
        src = element_html(text, el)
        if src is None:
            warn(f'{pk}: the page holds no element {el}')
            continue
        if it.get('recipe') == 'rail-focus':
            src += element_html(text, 'nav.rail') or ''
        sess = it.get('session') or ''
        gk = (pk, w, it.get('text_scale') or 1, sess)
        acts = prefix.setdefault(gk, [])
        acts += it.get('actions') or []
        s = sha(page_frame(pk), w, src, el, 'measure' if measure else 'picture', it.get('text_scale') or 1, RECIPE_V.get(it.get('recipe'), '') + (it.get('until_text') or '') + json.dumps(it.get('clip') or '', sort_keys=True),
                json.dumps(acts), 'b3r1')
        if reuse and p.exists() and sigs.get(key) == s:
            continue
        todo.setdefault(gk, []).append((key, it, s, p, measure))
    jobs = []
    for (pk, w, ts, sess), its in sorted(todo.items(), key=lambda kv: (kv[0][0], -kv[0][1], kv[0][3])):
        if sess:
            # a session's actions add up from the page's load: every item of the session is taken again, in order
            its = [(it['key'], it, None, paths[it['key']], bool(it.get('measure'))) for it in items
                   if (it['page'], it['w'], it.get('text_scale') or 1, it.get('session') or '') == (pk, w, ts, sess)]
        setup_job = any(it.get('recipe') == 'rail-focus' for _, it, *_ in its)
        jobs.append({'file': str(PAGES[pk]['path']), 'width': w, 'height': 900 if w > 600 else 844, 'static_sticky': not setup_job,
                     'draw_all': True, 'text_scale': ts,
                     'items': [{'selector': css_selector(it['el']), 'out': str(p), 'measure': m, 'actions': it.get('actions') or [],
                                'recipe': it.get('recipe'), 'until_text': it.get('until_text'), 'clip': it.get('clip')} for key, it, s, p, m in its]})
    if jobs:
        n = sum(len(j['items']) for j in jobs)
        print(f'photographing or measuring {n} elements on {len(jobs)} page loads ...')
        for j in jobs:
            for x in j['items']:
                if pathlib.Path(x['out']).exists():
                    pathlib.Path(x['out']).unlink()
        run_render(jobs, label)
        # the signatures, worked out again for every item now on disk
        prefix = {}
        for it in items:
            gk = (it['page'], it['w'], it.get('text_scale') or 1, it.get('session') or '')
            acts = prefix.setdefault(gk, [])
            acts += it.get('actions') or []
            p = paths[it['key']]
            text = page_text(it['page'])
            src = element_html(text, it['el']) if text else None
            if src is None or not p.exists():
                continue
            if it.get('recipe') == 'rail-focus':
                src += element_html(text, 'nav.rail') or ''
            sigs[it['key']] = sha(page_frame(it['page']), it['w'], src, it['el'], 'measure' if it.get('measure') else 'picture',
                                  it.get('text_scale') or 1, RECIPE_V.get(it.get('recipe'), '') + (it.get('until_text') or '') + json.dumps(it.get('clip') or '', sort_keys=True), json.dumps(acts), 'b3r1')
        sig_file.write_text(json.dumps(sigs, indent=1))
    taken = {x['out'] for j in jobs for x in j['items']}
    FIG.setdefault('shots', {})[label] = {'asked': len(items), 'taken': sum(1 for k, p in paths.items() if str(p) in taken and p.exists()),
                                          'missing': sorted(k for k, p in paths.items() if not p.exists())[:40]}
    return paths


def guide_styles(G):
    """Every <style> of the guide page, so a board-only picture draws in the guide's own type and inks."""
    return '\n'.join(re.findall(r'<style\b[^>]*>(.*?)</style>', G['text'], flags=re.S))


def in_element(G, element, raw, width_px):
    """A fragment set in the guide's own markup: the element of the strict build with the fragment's drawings in place of
    its own, in order, and its caption's words (after the Illustrative chip) taken from the fragment's first <desc>."""
    src = element_html(G['text'], element)
    if src is None:
        warn(f'the guide holds no element #{element} to set a board picture in')
        return None
    svgs = re.findall(r'<svg\b.*?</svg>', raw, flags=re.S)
    own = re.findall(r'<svg\b.*?</svg>', src, flags=re.S)
    if len(svgs) != len(own):
        warn(f'#{element} draws {len(own)} drawings and the board picture {len(svgs)}; set as they are')
    it = iter(svgs)
    src = re.sub(r'<svg\b.*?</svg>', lambda m: next(it, m.group(0)), src, flags=re.S)
    desc = re.search(r'<desc\b[^>]*>(.*?)</desc>', raw, flags=re.S)
    if desc:
        src = re.sub(r'(<figcaption[^>]*>(?:<span class="illus">.*?</span>\s*)?)(.*?)(</figcaption>)', lambda m: m.group(1) + desc.group(1).strip() + m.group(3), src, count=1, flags=re.S)
    return (f'<div class="rule"><div class="rule-body" style="width:{width_px}px">{src}</div></div>')


def file_shots(G, reqs, reuse, shots):
    """Photograph the board-only pictures (the cartographer's files). A whole HTML page is photographed as it is (its
    element named, else its body). A fragment or an SVG is drawn in a page that carries the guide's own styles: where an
    element is named, set in that element of the strict build in place of its drawings (in_element), at the width the guide
    gives that element at the window named; else on the ground named. -> {key: path}"""
    d = SCRATCH / 'files'
    d.mkdir(parents=True, exist_ok=True)
    sig_file = SCRATCH / 'file-sigs.json'
    sigs = json.loads(sig_file.read_text()) if sig_file.exists() else {}
    styles = None
    paths, jobs = {}, []
    for key, src, width, ground, element in reqs:
        out = d / f'{key}.png'
        paths[key] = out
        raw = src.read_text()
        whole = bool(re.search(r'<!doctype|<html\b', raw[:500], flags=re.I))
        ref = shots.get(f'dec-{element}-{width}') if element else None
        wpx = png_size(ref)[0] if ref and ref.exists() else 720
        s = sha(raw, width, ground, element, whole, wpx, element_html(G['text'], element) if element else '', page_frame_sig(G['text']) if not whole else '')
        if reuse and out.exists() and sigs.get(key) == s:
            continue
        if whole:
            page, sel = src, (f'#{element}' if element else 'body')
        else:
            if styles is None:
                styles = guide_styles(G)
            page = d / f'{key}.html'
            surf = 'oa-surface-charcoal' if ground == 'charcoal' else 'oa-surface-newsprint'
            inner = in_element(G, element, raw, wpx) if element else None
            body = inner if inner else f'<div class="{surf} plate-stage" style="display:inline-block;padding:16px">{raw}</div>'
            page.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{styles}</style>'
                            f'<style>body{{margin:0;padding:24px;background:var(--oa-color-surface-newsprint)}}#pic{{display:inline-block}}</style></head>'
                            f'<body><div id="pic">{body}</div></body></html>')
            sel = f'#{element}' if inner else '#pic'
        jobs.append({'file': str(page), 'width': width, 'height': 900 if width > 600 else 844, 'static_sticky': False, 'draw_all': False,
                     'items': [{'selector': sel, 'out': str(out), 'measure': False}], '_sig': (key, s)})
    if jobs:
        print(f'photographing {len(jobs)} board-only pictures ...')
        for j in jobs:
            p = pathlib.Path(j['items'][0]['out'])
            if p.exists():
                p.unlink()
        run_render([{k: v for k, v in j.items() if k != '_sig'} for j in jobs], 'files')
        for j in jobs:
            key, s = j['_sig']
            if pathlib.Path(j['items'][0]['out']).exists():
                sigs[key] = s
        sig_file.write_text(json.dumps(sigs, indent=1))
    return paths


# ------------------------------------------------------------------------------------------------------- the kit
KIT_SHARED = ['kit.js', 'kit-build.js', 'parts.js', 'kit.css', 'metrics.js', 'geo.js', 'words.json', 'checks.js', 'oa-chart.mjs', 'tools/minify.mjs']


def kit_shared_sig():
    kd = ROOT / C['slots']['kit_dir']
    return sha(*[(kd / f).read_bytes() for f in KIT_SHARED if (kd / f).exists()], (ROOT / C['slots']['tokens_css']).read_bytes())


def kit_sig(sid, shared, widths):
    S = C['slots']
    sp = ROOT / S['specs_dir'] / f'{sid.lower()}.json'
    spec = json.loads(sp.read_text())
    files = [sp]
    ds = spec.get('dataset')
    for d in (ds if isinstance(ds, list) else [ds] if ds else []):
        for ext in ('.csv', '.json', '.meta.json'):
            p = ROOT / S['data_dir'] / f'{d}{ext}'
            if p.exists():
                files.append(p)
    form = ROOT / S['kit_dir'] / 'forms' / f'{spec.get("form")}.js'
    files += [form] if form.exists() else sorted((ROOT / S['kit_dir'] / 'forms').glob('*.js'))
    return sha(shared, widths, *[rel(f).encode() + b'\0' + f.read_bytes() for f in files])


def kit_build(groups, reuse):
    """The kit's own captures, one folder per chart under <scratch>/kit-out, at the window widths that give the guide's
    drawing widths. groups: {(desk_page, phone_page): [ids]}. A chart is rebuilt where its sources or widths changed."""
    S = C['slots']
    out = SCRATCH / 'kit-out'
    out.mkdir(parents=True, exist_ok=True)
    sig_file = SCRATCH / 'kit-sigs.json'
    sigs = json.loads(sig_file.read_text()) if sig_file.exists() else {}
    shared = kit_shared_sig()
    rebuilt, reused, logs = [], [], []
    for widths, ids in sorted(groups.items()):
        todo = []
        for sid in ids:
            lo = sid.lower()
            want = kit_sig(sid, shared, widths)
            have = all((out / lo / f'{lo}-{g}-{w}{x}.png').exists() for g in ('newsprint', 'charcoal') for w in widths for x in ('', '-grayscale')) \
                and (out / lo / f'{lo}-check.json').exists()
            # a social data card draws its own crops whatever the widths: its 1440 px page pictures are what it makes
            have = have or ((out / lo / f'{lo}-check.json').exists()
                            and all((out / lo / f'{lo}-{g}-1440{x}.png').exists() for g in ('newsprint', 'charcoal') for x in ('', '-grayscale')))
            if reuse and have and sigs.get(sid) == want:
                reused.append(sid)
            else:
                todo.append((sid, want))
        if not todo:
            continue
        print(f'building {len(todo)} charts with the kit at {widths[0]} and {widths[1]} px windows ...')
        for sid, _ in todo:
            shutil.rmtree(out / sid.lower(), ignore_errors=True)
        # one kit browser at a time, in batches of 12 charts, so no browser stays open long
        for k in range(0, len(todo), 12):
            batch = todo[k:k + 12]
            if not browser_gate(f'the kit, {len(batch)} charts'):
                break
            r = subprocess.run(['node', str(ROOT / S['kit_command']), 'build', *[s.lower() for s, _ in batch], '--widths', ','.join(map(str, widths)),
                                '--out', str(out), '--date', DATE], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
            logs.append(r.stdout + r.stderr)
            for sid, want in batch:
                if (out / sid.lower() / f'{sid.lower()}-check.json').exists():
                    sigs[sid] = want
                    rebuilt.append(sid)
                else:
                    warn(f'the kit made no check file for {sid}: ' + (r.stderr or r.stdout)[-200:])
            sig_file.write_text(json.dumps(sigs, indent=1))
    if logs:
        (SCRATCH / 'kit-build.log').write_text('\n'.join(logs))
    FIG['kit_builds'] = {'rebuilt': rebuilt, 'reused': reused, 'widths': {f'{a},{b}': ids for (a, b), ids in groups.items()}}
    return out


# ------------------------------------------------------------------------------------------------------- pictures
def png_size(p):
    return B1.png_size(p)


def img_size(p):
    from PIL import Image
    with Image.open(p) as im:
        return im.size


def compose(name, parts, cols=None, gap=24, label_h=26):
    """One picture of one or more, each part at its true size on whole pixels, its label set in Inter Medium at 13 px
    above it (D3-196), saved as a lossless WebP: every pixel as captured, at about a fifth of a PNG's bytes. parts:
    [(path, label)]. Grayscale parts are composed in one gray channel when every part is gray."""
    from PIL import Image, ImageDraw, ImageFont
    out = IMG / f'{DATE}_{name}.webp'
    pads = [x[2] if len(x) > 2 else None for x in parts]
    # WebP holds at most 16,383 px a side: a taller picture is saved as a lossless PNG instead
    if any(img_size(x[0])[1] > 16000 or img_size(x[0])[0] > 16000 for x in parts if pathlib.Path(x[0]).exists()):
        out = IMG / f'{DATE}_{name}.png'
    parts = [(x[0], x[1]) for x in parts]
    for p, _ in parts:
        need(pathlib.Path(p).exists(), f'missing picture {rel(p)} for {name}')
    if not any(lab for _, lab in parts):
        label_h = 0
    sig = sha(json.dumps([[str(p), file_sig(p), lab] for p, lab in parts] + [cols, gap, label_h, pads, 'b2v2-webp']))
    if out.exists() and CACHE.get(out.name) == sig:
        w, h = img_size(out)
    else:
        ims = [Image.open(p) for p, _ in parts]
        gray = all(im.mode == 'L' for im in ims)
        mode = 'L' if gray else 'RGB'
        lum = lambda c: round(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
        bg, ink = (lum(NEWSPRINT), lum(LABEL_INK)) if gray else (NEWSPRINT, LABEL_INK)
        conv = []
        for im in ims:
            if im.mode == mode:
                conv.append(im)
            elif im.mode in ('RGBA', 'LA', 'P'):
                base = Image.new('RGBA', im.size, NEWSPRINT + (255,))
                base.alpha_composite(im.convert('RGBA'))
                conv.append(base.convert(mode))
            else:
                conv.append(im.convert(mode))
        for k, pad in enumerate(pads):
            if pad:
                col = (lum(pad) if mode == 'L' else tuple(pad))
                big = Image.new(mode, (conv[k].size[0] + 2 * PAD, conv[k].size[1] + 2 * PAD), col)
                big.paste(conv[k], (PAD, PAD))
                conv[k] = big
        cols = cols or len(conv)
        rows = [conv[i:i + cols] for i in range(0, len(conv), cols)]
        col_w = [max(r[k].size[0] for r in rows if k < len(r)) for k in range(cols)]
        row_h = [max(im.size[1] for im in r) for r in rows]
        W = sum(col_w) + gap * (cols - 1)
        H = sum(h + label_h for h in row_h) + gap * (len(rows) - 1)
        canvas = Image.new(mode, (W, H), bg)
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype(LABEL_FONT, 13)
        y = 0
        for r, row in enumerate(rows):
            x = 0
            for k, im in enumerate(row):
                lab = parts[r * cols + k][1]
                if lab:
                    draw.text((x, y + 4), lab, font=font, fill=ink)
                canvas.paste(im, (x, y + label_h))
                x += col_w[k] + gap
            y += row_h[r] + label_h + gap
        if out.suffix == '.png' or W > 16383 or H > 16383:
            out = out.with_suffix('.png')
            canvas.save(out, 'PNG', optimize=True)
        else:
            canvas.save(out, 'WEBP', lossless=True, quality=100, method=4)
        CACHE[out.name] = sig
        w, h = W, H
    rec = {'src': f'img/{out.name}', 'file': out, 'w': w, 'h': h, 'source': ', '.join(rel(p) for p, _ in parts)}
    IMAGES[out.name] = rec
    return rec


def side_or_stack(paths, gap=24, extra=0):
    ws = [png_size(p)[0] + extra for p in paths]
    return len(paths) if sum(ws) + gap * (len(ws) - 1) <= CONTENT_W else 1


def frame(rec, alt, lazy=True, cls=''):
    w, h = rec['w'], rec['h']
    region = w > REGION_W
    attrs = f' role="region" tabindex="0" aria-label="{esc(alt)}, {w} by {h} px; scrolls sideways when wider than the window"' if region else ''
    ld = ' loading="lazy"' if lazy else ''
    return f'<div class="frame{(" " + cls) if cls else ""}"{attrs}><img src="{rec["src"]}" width="{w}" height="{h}" alt="{esc(alt)}"{ld} decoding="async"></div>'


def figure(rec, alt, cap_html='', lazy=True, top=False):
    if top and cap_html:
        return f'<figure class="shot"><figcaption class="top">{cap_html}</figcaption>{frame(rec, alt, lazy)}</figure>'
    return f'<figure class="shot">{frame(rec, alt, lazy)}' + (f'<figcaption>{cap_html}</figcaption>' if cap_html else '') + '</figure>'


# ------------------------------------------------------------------------------------------------------- sections
def refs_line(refs, where):
    codes = set(re.findall(r'\b' + CODE_DEC + r'\b', refs))
    moved = sorted((c for c in B1.MOVED if c in LOG and c not in codes),
                   key=lambda c: (re.sub(r'[^A-Z]', '', c.split('-')[0]), int(re.sub(r'\D', '', c.split('-')[1]) or 0)))
    B1.MOVED.clear()
    if moved:
        refs = (refs + ' · ' if refs else '') + 'from teammates’ files: ' + ' · '.join(moved)
    for c in re.findall(r'\b' + CODE_DEC + r'\b', refs):
        LINKED.add(c)
        if c not in LOG:
            warn(f'{c} in the reference line of {where} is not in the decision log or the open questions')
    return f'<p class="codes">Reference: {esc(refs)}</p>' if refs else ''


def section(key, body, status, extra_refs=''):
    P = C['sections'][key]
    STATUS[key] = status
    refs = ' · '.join(x for x in (P.get('refs', ''), extra_refs) if x)
    return (f'<section class="sec" id="p-{key}" aria-labelledby="h-{key}"><div class="sec-top"><p class="label">Panel {P["n"]}</p>{chip(status)}</div>'
            f'<h2 class="sec-h" id="h-{key}">{esc(fill(P["title"]))}</h2>{body}{refs_line(refs, "panel " + key)}</section>')


def status_words(st):
    if st == 'ready':
        return C['status_words']['ready']
    kind, who = st
    return C['status_words'][kind].format(who=C['owners'].get(who, who))


def chip(st, short=False):
    kind = st if isinstance(st, str) else st[0]
    return f'<span class="st {kind}">{esc(C["status_short"][kind] if short else status_words(st))}</span>'


def pending(text):
    return f'<div class="pending" role="status"><p>{esc(text)}</p></div>'


def plan():
    P = json.loads((ROOT / C['slots']['plan']).read_text())
    rn = [f for f in P['forms'] if f.get('round') in C['rounds']]
    need(rn, 'the plan holds no rows for rounds ' + ', '.join(map(str, C['rounds'])))
    return P, rn


def chapter14():
    ch = json.loads((ROOT / C['slots']['chapter14']).read_text())
    return ch, {r['id']: r for r in ch['rules']}


# ------------------------------------------------------------------------------------------------------- the decisions
PIC_KEYS = {}             # id(picture) -> request


def decisions():
    p = DECISIONS_PATH
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        warn(f'{rel(p)} does not parse: {e}')
        return None
    if '—' in p.read_text():
        warn(f'{rel(p)} holds an em dash')
    FIG['decisions'] = {'file': rel(p), 'state': d.get('state'), 'updated_utc': d.get('updated_utc'), 'schema': d.get('schema'),
                        'signed_off_utc': d.get('signed_off_utc')}
    return d


def all_pictures(d):
    for g in (d or {}).get('panels', []):
        for it in g.get('items', []):
            for pic in it.get('pictures', []) or []:
                yield it, pic


def item_spec(it):
    s = it.get('spec') or (it.get('id') if re.fullmatch(r'S\d\d', str(it.get('id', ''))) else None)
    return s.upper() if s else None


def item_specs(it):
    """Every chart an item covers: its specs, else its spec, else the chart ids its own id names (S54-S55)."""
    if it.get('specs'):
        return [str(x).upper() for x in it['specs']]
    ids = [x.upper() for x in re.findall(r'\bS\d\d\b', str(it.get('id', '')).replace('-', ' '))]
    s = item_spec(it)
    return list(dict.fromkeys(([s] if s else []) + ids)) if len(ids) > 1 or not s else [s]


def pic_request(it, pic):
    """Where a picture comes from, before any capture runs: {'kind': 'guide', key, page, el, w, ...}, {'kind': 'made', ...},
    {'kind': 'path', 'file'} or {'kind': 'missing', 'why', 'owner', 'how'}. A guide picture with no page reads "final"
    (the data lead's schema); a setup's focus is the rail recipe and its text_scale the page's text size."""
    kind = pic.get('kind')
    w = int(pic.get('width') or DESK)
    if kind == 'guide':
        spec = (pic.get('spec') or item_spec(it) or '').lower()
        el = pic.get('element') or (f'oac-s-14-{spec}' if spec else None)
        if not el:
            warn(f'a guide picture in item {it.get("id")} names no element or spec')
            return None
        pk = pic.get('page') or 'final'
        if pk not in PAGES:
            warn(f'a picture in item {it.get("id")} names the page {pk}, which the decisions file does not map')
            return None
        st = pic.get('setup') or {}
        req = {'kind': 'guide', 'page': pk, 'el': el, 'w': w, 'text_scale': st.get('text_scale') or 1}
        tag = ''
        if st.get('focus'):
            req['recipe'] = 'rail-focus'
            req['session'] = 'rail-focus'
            req['until_text'] = C['slots'].get('rail_focus_text')
            tag += '-railfocus'
        if st.get('text_scale') and st['text_scale'] != 1:
            tag += f'-text{int(100 * st["text_scale"])}'
        req['key'] = f'g-{pk}-{slug(el)}-{w}{tag}'
        return req
    if kind == 'to-make':
        made = (C['slots'].get('made') or {}).get(str(it.get('id')))
        mk = made_key(it, pic)
        if made and mk in MADE:
            return {'kind': 'made', 'key': mk, 'how': made.get('how', ''), 'w': w, 'sketch': bool(made.get('sketch'))}
        p = pic.get('path')
        if p and (ROOT / p).is_file():
            return {'kind': 'path', 'file': ROOT / p}
        return {'kind': 'missing', 'why': pic.get('label') or 'a picture to make', 'owner': pic.get('owner') or '', 'how': pic.get('how') or ''}
    path = pic.get('path')
    if not path:
        return {'kind': 'missing', 'why': pic.get('label') or kind}
    fp = ROOT / path
    if not fp.exists():
        return {'kind': 'missing', 'why': path}
    if fp.suffix.lower() in IMG_EXT:
        return {'kind': 'path', 'file': fp}
    return {'kind': 'missing', 'why': path}


# ------------------------------------------------------------------------------------------------------- pictures made in scratch
MADE = {}                 # key -> the photograph's path, for pictures this board makes from a scratch copy of the final build
STACK = {}                # a made picture's key -> [(photograph key, label)], stacked into one picture

# The creative director's fix round (B3-M4, B3-S1): crops to the change, before and after, for four one-approval items whose
# decision pictures are whole plates or page strips. The crops lead the item; its own pictures move into its fold. Each crop
# is the union of the blocks that hold the words, patterns or parts named, inside the element named, on the page named.
CROPS = {
    'where-to-start': [
        dict(page='v11', el='start', w=320, text_scale=2, patterns=[r'Identity\s+proofs'], overflow=True, context=140, block='span.u', role='before', row='c1',
             label='Before the fix pass, at a 320 px window with text at 200 percent: the link “Identity proofs” runs past the window’s right edge'),
        dict(page='final', el='start', w=320, text_scale=2, patterns=[r'Identity\s+proofs'], overflow=True, context=140, block='span.u', role='after', row='c1',
             label='Now: the same link wraps inside the window'),
        dict(page='v11', el='start', w=320, text_scale=2, patterns=[r'Components\s+and\s+interaction'], overflow=True, context=140, block='span.u', role='before', row='c2',
             label='Before the fix pass: the link “Components and interaction” runs past the edge too'),
        dict(page='final', el='start', w=320, text_scale=2, patterns=[r'Components\s+and\s+interaction'], overflow=True, context=140, block='span.u', role='after', row='c2',
             label='Now: it wraps inside the window'),
    ],
    '14.144-pips': [
        dict(page='v11', el='fig-s-14-144-correct', within='#fig-s-14-144-correct .cd8', w=DESK, block='div',
             texts=['Effect on quality of democracy', 'Effect on income and wealth equality'], context=12, role='before', row='card',
             label='Before the fix pass: the four effects on Reform R-06’s card at a 1440 px window, in words with no pips'),
        dict(page='final', el='fig-s-14-144-correct', within='#fig-s-14-144-correct .cd8', w=DESK, subs=['.ef8g'], context=12, role='after', row='card',
             label='Now: the same card’s effects, with pips beside each code'),
        dict(page='v11', el='fig-s-14-144-correct', within='#fig-s-14-144-correct .cd8', w=PHONE, block='div',
             texts=['Effect on quality of democracy', 'Effect on income and wealth equality'], context=12, role='before', row='phone',
             label='Before the fix pass, on a 390 px phone: the same card’s effects'),
        dict(page='final', el='fig-s-14-144-correct', w=PHONE, subs=['.ph8'], context=12, role='after', row='phone',
             label='Now, on a phone: the line-up, each family’s effects with the three reforms together'),
    ],
    'rules-14-1-to-14-14': [
        dict(page='v11', el='rule-14-6', w=DESK, texts=['In a chart, the red goes to the point'], context=24, role='before', row='r6',
             label='Rule 14.6 before the fix pass: the sentence on the red and the other marks'),
        dict(page='final', el='rule-14-6', w=DESK, texts=['In a chart, the red goes to the point', 'Every other series takes the context ink', 'Where the title names one bar'],
             context=24, role='after', row='r6', label='Rule 14.6 now: the same lines, with the role inks defined and the light fill only where the title names one bar'),
    ],
    'S40': [
        dict(page='v11', el='oac-s-14-s40', w=DESK, patterns=[r'^\d{4}-\d{2}-\d{2}, \d+ to \d+$'], open=True, block='tr', context=12, role='before', row='d',
             label='Before the fix pass: S40’s table, opened, with its five committee vote dates as numbers'),
        dict(page='final', el='oac-s-14-s40', w=DESK, patterns=[r'^[A-Z][a-z]+ \d{1,2}, \d{4}, \d+ to \d+$'], open=True, block='tr', context=12, role='after', row='d',
             label='Now: the same five cells, the dates in words'),
    ],
}
# B3-S10: the masthead's 375 px working copy shows the 16 px wordmark where the recommendation keeps the 24 px one, so it
# sits in the item's fold, for comparison only
FOLD_PICS = {('masthead-360', 'to-make', 375)}
CROP_ALT = '{label}. Photographed from {page} at a {w} px window, cropped to the change.'


def crop_items():
    out = []
    for iid, cs in CROPS.items():
        for k, c in enumerate(cs):
            clip = {x: c[x] for x in ('texts', 'patterns', 'subs', 'open', 'block', 'context', 'overflow') if x in c}
            clip['within'] = c.get('within') or css_selector(c['el'])
            out.append({'key': f'crop-{slug(iid)}-{k}', 'page': c['page'], 'el': c['el'], 'w': c['w'], 'text_scale': c.get('text_scale') or 1,
                        'recipe': 'clip', 'clip': clip, 'session': 'crops'})
    return out


def crop_html(it, shots):
    """The crops that lead an item, in rows of before and after; None where the item has none or one is missing."""
    cs = CROPS.get(str(it.get('id')))
    if not cs:
        return None
    S = C['sections']['decide']
    rows, order = {}, []
    for k, c in enumerate(cs):
        p = shots.get(f'crop-{slug(it.get("id"))}-{k}')
        if not p or not p.exists():
            return None
        rec = compose(f'Crop-{slug(it.get("id"))}-{k}', [(p, '')])
        alt = fill(CROP_ALT, {'label': c['label'], 'page': C['page_words'].get(c['page'], c['page']), 'w': c['w']})
        rw = S['role_words'].get(c['role'], '')
        QUOTED.extend([c['label'], alt])
        h = figure(rec, alt, (f'<span class="role {esc(c["role"])}">{esc(rw)}</span> ' if rw else '') + f'<b>{esc(c["label"])}</b>', top=True)
        if c['row'] not in rows:
            rows[c['row']] = []
            order.append(c['row'])
        rows[c['row']].append(h)
    return ''.join(f'<div class="pair ba">{"".join(rows[r])}</div>' for r in order)


# B3-M1's picture half: Rule 15.11 today and with the keyline, each converted to gray by luma (ITU-R 601-2, as PIL's 'L'
# mode gives), set after the keyline item's own pictures
GRAY_PAIR = {'red-target-keyline': [
    ('g-final-fig-s-15-11-correct-1440', 'Rule 15.11 today, in grayscale by luma (ITU-R 601-2)'),
    ('made-red-target-keyline-1440', 'Rule 15.11 with the keyline, in grayscale by luma (ITU-R 601-2)'),
]}


def gray_pair_html(it, shots):
    pairs = GRAY_PAIR.get(str(it.get('id')))
    if not pairs:
        return ''
    from PIL import Image
    hs = []
    for k, (key, label) in enumerate(pairs):
        src = shots.get(key) or MADE.get(key)
        if not src or not pathlib.Path(src).exists():
            return ''
        g = SCRATCH / 'made' / f'gray-{key}.png'
        if not g.exists() or g.stat().st_mtime < pathlib.Path(src).stat().st_mtime:
            Image.open(src).convert('RGB').convert('L').save(g, optimize=True)
        rec = compose(f'Gray-{slug(it.get("id"))}-{k}', [(g, '')])
        alt = f'{label}: the same plate as above in gray, so the target pills read by lightness alone.'
        QUOTED.extend([label, alt])
        hs.append(figure(rec, alt, f'<b>{esc(label)}</b>', top=True))
    return f'<div class="pair ba">{"".join(hs)}</div>'


# B3-S2: the S59 sketch moves one label only. The kit mirror's patch lifts 2026's value and keeps its old place taken, so
# the labels after it give way as they did before; this patch stands in for the content file's while the editor holds it.
KIT_PATCH = {'S59-label': {'set': {'first_value_clear': True}, 'patch': {'forms/fan-chart.js': [
    ["labels: ['apart', 'apart_label', 'key_outer', 'key_inner', 'key_median', 'y_axis', 'history', 'key_history', 'key_gap'],",
     "labels: ['apart', 'apart_label', 'key_outer', 'key_inner', 'key_median', 'y_axis', 'history', 'key_history', 'key_gap', 'first_value_clear'],"],
    ["        if (oy > vy - tick - 2 && oy < vy + 4) vy = oy - 5;",
     "        if (oy > vy - tick - 2 && oy < vy + 4) vy = oy - 5;\n        var vy0 = vy;\n"
     "        // board 3's sketch (the held item S59-label): labels.first_value_clear lifts the first value over the outer band's rising edge across its own width\n"
     "        if (L.first_value_clear && i === 0 && main.length > 1) { var hw = c.measure(K.fmt(r[ey], fy), 'tick', 600) / 2 + 3, e0 = ys(r[eoh]), e1 = ys(main[1][eoh]); vy = Math.min(vy, e0 + (e1 - e0) * Math.min(1, hw / (px(1) - px(0))) - 3); }"],
    ["        vlab.push({ x: px(i), y: vy, words: K.fmt(r[ey], fy), weight: 600, halo: true, must: i === 0 || i === main.length - 1, give: i === 0 && i !== main.length - 1 && hist.length > 0 });",
     "        vlab.push({ x: px(i), y: vy, words: K.fmt(r[ey], fy), weight: 600, halo: true, must: i === 0 || i === main.length - 1, give: i === 0 && i !== main.length - 1 && hist.length > 0, ghost: vy !== vy0 ? vy0 : undefined });"],
    ["        setl.push(b);\n        c.text(v.x, v.y, v.words,",
     "        setl.push(b);\n        if (v.ghost !== undefined) setl.push(lbox(Object.assign({}, v, { y: v.ghost })));   // the moved label's old place stays taken\n        c.text(v.x, v.y, v.words,"],
]}}}


def made_key(it, pic):
    return f'made-{slug(it.get("id"))}-{int(pic.get("width") or DESK)}'


def keyline_fragments(d):
    """Rule 15.11's correct plate from chapter 15's own generator, as built and with three_loop's keys flag set, in a
    scratch Book; the generator is imported read-only and write() is never called. Cached on the generator's bytes."""
    gen = SCRIPTS3 / 'phase3_ch15_build.py'
    sig = sha(gen.read_bytes(), (ROOT / 'work/extract/atlas-v7-data.json').read_bytes() if (ROOT / 'work/extract/atlas-v7-data.json').exists() else b'')
    cache = d / 'keyline'
    cache.mkdir(parents=True, exist_ok=True)
    a_, k_, s_ = cache / 's-15-11-correct.as-built.html', cache / 's-15-11-correct.keyline.html', cache / 'sig.txt'
    if not (a_.exists() and k_.exists() and s_.exists() and s_.read_text() == sig):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS2))
        spec = importlib.util.spec_from_file_location('ch15gen_board3', gen)
        M = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(M)
            orig = M.three_loop
            for path_, keys in ((a_, False), (k_, True)):
                M.three_loop = (lambda *a, _k=keys, **kw: orig(*a, **dict(kw, keys=True)) if _k else orig(*a, **kw))
                book = M.Book()
                M.rule_15_11(book)
                path_.write_text(book.files['s-15-11-correct'])
            M.three_loop = orig
        except Exception as e:  # noqa: BLE001   the generator's own checks stop it; the picture then waits
            warn(f'chapter 15’s generator could not make Rule 15.11 with the keyline: {e}')
            return None
        s_.write_text(sig)
    spec_file = ROOT / 'work/build/guide/specimens/s-15-11-correct.html'
    if spec_file.exists() and spec_file.read_text() != a_.read_text():
        warn('the generator’s Rule 15.11 as built differs from the committed specimen; the keyline picture is set on the generator’s')
    return a_.read_text(), k_.read_text()


def make_pictures(reuse):
    """The pictures a builder can make in scratch, as the decisions file's "how" asks, for the items the content file
    names under slots.made: the masthead with the 16 px wordmark master's switch at 23.5em (376 px), in a scratch copy of
    the final build that changes that one media query; a chart the kit builds from a scratch copy of its spec with one
    opt-in key (slots.made_kit); and Rule 15.11 with chapter 15's keyline flag set (keyline_fragments). Nothing in the
    repository changes."""
    made = C['slots'].get('made') or {}
    S_ = C['sections']['decide']
    want = []
    for it, pic in all_pictures(D):
        if pic.get('kind') == 'to-make' and str(it.get('id')) in made:
            want.append((it, pic))
    if not want:
        return
    src = page_text('final')
    if not src:
        return
    d = SCRATCH / 'made'
    d.mkdir(parents=True, exist_ok=True)
    items = []
    for it, pic in want:
        iid = str(it.get('id'))
        if iid == 'masthead-360':
            copy = d / f'{DATE}_Masthead-Switch-23-5em.html'
            old = re.findall(r'@media\s*\(max-width:\s*22\.49em\)\s*\{\s*\.home \.wm-24\s*\{\s*display:\s*none\s*\}', src)
            if len(old) != 1:
                warn(f'the final build’s CSS holds {len(old)} switches for the 16 px master where one was expected; masthead pictures wait')
                continue
            new = old[0].replace('22.49em', '23.49em')
            text = src.replace(old[0], new)
            if not copy.exists() or copy.read_text() != text:
                copy.write_text(text)
            PAGES['made-masthead'] = {'path': copy, 'text': text, 'frame': None}
            mk = made_key(it, pic)
            items.append({'key': mk, 'page': 'made-masthead', 'el': 'header.masthead', 'w': int(pic.get('width') or DESK)})
        elif iid == 'related-rules':
            # a studio sketch: Rule 14.32's foot in a scratch copy of the final page with a "Related rules" line of links,
            # set in the page's own link form (the foot's "Related chapters" markup), read from chapter 14's related_rules
            rid = C['slots']['made']['related-rules'].get('rule', '14.32')
            rr = ((chapter14()[1].get(rid) or {}).get('related_rules')) or []
            fs = src.find(f'id="rule-{rid.replace(".", "-")}"')
            fe = src.find('<div class="rule"', fs + 10)
            seg = src[fs:fe]
            k = seg.find('<div class="foot-pair">')
            if not rr or fs < 0 or k < 0:
                warn(f'the related rules sketch could not be set: Rule {rid} has {len(rr)} related rules and its foot was {"found" if k >= 0 else "not found"}')
                continue
            lis = ''.join(f'<li><a class="xref" href="#rule-{x.replace(".", "-")}"><span class="n">{esc(x)}</span> {esc(rule_name(x))}</a></li>' for x in rr)
            block = f'<div class="foot-block foot-related"><p class="label">Related rules</p><ul class="rel-inline">{lis}</ul></div>'
            k += len('<div class="foot-pair">')
            text = src[:fs] + seg[:k] + block + seg[k:] + src[fe:]
            copy = d / f'{DATE}_Related-Rules-Sketch.html'
            if not copy.exists() or copy.read_text() != text:
                copy.write_text(text)
            PAGES['made-related'] = {'path': copy, 'text': text, 'frame': None}
            FIG['made_related'] = {'rule': rid, 'links': rr}
            items.append({'key': made_key(it, pic), 'page': 'made-related', 'el': f'rule-{rid.replace(".", "-")}', 'w': int(pic.get('width') or DESK)})
        elif iid == 'CE-S22-examples':
            # a studio sketch: the editor's example lines (the picture's own "lines") set under their questions in a scratch
            # copy of the final page's selection guide, in the tier words' type (.sg-t), before each question's skip link
            lines = pic.get('lines') or []
            text, done_, qmap = src, [], {}
            for ln in lines:
                m = re.search(r'<li class="sg-q" data-group="(\d+)"><p class="sg-qt" id="[^"]*">' + re.escape(html.escape(ln['question'], quote=False).replace('&#x27;', '’')) + r'</p>', text)
                if not m:
                    m = re.search(r'<li class="sg-q" data-group="(\d+)"><p class="sg-qt" id="[^"]*">' + re.escape(ln['question']) + r'</p>', text)
                if not m:
                    warn(f'CE-S22-examples: the selection guide holds no question “{ln["question"]}”')
                    continue
                g = m.group(1)
                ex = (f'<p class="sg-t sg-ex" style="margin:calc(var(--oa-space-100) - var(--oa-space-200)) 0 var(--oa-space-200);max-width:34em">'
                      f'{esc(ln["example"])}</p>')
                new = m.group(0).replace('<li class="sg-q"', f'<li class="sg-q" id="board3-sg-q-{g}"', 1) + ex
                text = text.replace(m.group(0), new, 1)
                done_.append(g)
                qmap[g] = ln['question']
            if len(done_) != len(lines) or not lines:
                continue
            copy = d / f'{DATE}_Selection-Guide-Examples-Sketch.html'
            if not copy.exists() or copy.read_text() != text:
                copy.write_text(text)
            PAGES['made-sg'] = {'path': copy, 'text': text, 'frame': None}
            parts = []
            for w_ in (DESK, PHONE):
                for g in done_:
                    k_ = f'made-sg-{g}-{w_}'
                    items.append({'key': k_, 'page': 'made-sg', 'el': f'board3-sg-q-{g}', 'w': w_})
                    parts.append((k_, fill(S_['sg_part'], {'w': f'{w_:,}', 'q': qmap[g]})))
            STACK[made_key(it, pic)] = parts
        elif iid == 'NB-S4':
            # a studio sketch: one round 4 chart's figure from the kit, as built in scratch, with the 16 px lockmark master
            # set after the credit at the source line's right end; today's figure and the sketch, source rows stacked
            sid = C['slots']['made']['NB-S4'].get('spec', 'S85').lower()
            today = SCRATCH / 'kit-out' / sid / f'{sid}.html'
            lm = ROOT / 'work/build/assets/identity/lockmark/20261028_Lockmark-16px-Master.svg'
            if not today.exists() or not lm.exists():
                warn(f'NB-S4: the kit’s figure of {sid.upper()} or the 16 px lockmark master is missing; its picture waits')
                continue
            ft = today.read_text()
            credit = re.search(r'<p class="oac-credit">(.*?)</p>', ft, flags=re.S)
            if not credit:
                warn('NB-S4: the kit’s figure prints no credit line; its picture waits')
                continue
            inner = re.sub(r'<title>.*?</title>', '', re.search(r'<svg[^>]*>(.*)</svg>', lm.read_text(), flags=re.S).group(1), flags=re.S)
            mark = (f'<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false" style="flex:none">{inner}</svg>')
            sk = ft.replace(credit.group(0), f'<p class="oac-credit" style="display:flex;align-items:center;gap:8px">{credit.group(1)}{mark}</p>', 1)
            sk_p = today.with_name(f'{sid}-lockmark-sketch.html')
            if not sk_p.exists() or sk_p.read_text() != sk:
                sk_p.write_text(sk)
            PAGES['made-nb-today'] = {'path': today, 'text': ft, 'frame': None}
            PAGES['made-nb-sketch'] = {'path': sk_p, 'text': sk, 'frame': None}
            items += [{'key': 'made-nb-today', 'page': 'made-nb-today', 'el': 'div.oac-src', 'w': DESK},
                      {'key': 'made-nb-sketch', 'page': 'made-nb-sketch', 'el': 'div.oac-src', 'w': DESK}]
            STACK[made_key(it, pic)] = [('made-nb-today', S_['nb_today']), ('made-nb-sketch', S_['nb_sketch'])]
        elif iid == 'S59-label':
            # a studio sketch: S59 drawn by a scratch mirror of the kit whose fan-chart form takes one new label key,
            # labels.history_last_below (the last history value set under its dot), from a scratch copy of the spec
            kp = KIT_PATCH.get('S59-label') or C['slots']['made']['S59-label']
            km = kit_mirror(d, kp.get('patch') or {})
            if not km:
                continue
            sid = 's59'
            w_ = int(pic.get('width') or PHONE)
            win = w_ - 64 + 32 if w_ < 600 else DESK     # the guide's phone figure is the window less 64 px; the kit's page adds 32
            sd = d / 'kit-s59'
            (sd / 'specs').mkdir(parents=True, exist_ok=True)
            spec_ = json.loads((ROOT / C['slots']['specs_dir'] / f'{sid}.json').read_text())
            spec_.setdefault('labels', {}).update(kp.get('set') or {})
            (sd / 'specs' / f'{sid}.json').write_text(json.dumps(spec_, indent=1, ensure_ascii=False))
            sig_ = sha(json.dumps(spec_, sort_keys=True), km[1], win)
            png = sd / 'out' / sid / f'{sid}-newsprint-{win}.png'
            stamp = sd / 'sig.txt'
            if not (reuse and png.exists() and stamp.exists() and stamp.read_text() == sig_):
                shutil.rmtree(sd / 'out', ignore_errors=True)
                if browser_gate('the kit mirror, S59-label'):
                    r = subprocess.run(['node', str(km[0] / 'oa-chart.mjs'), 'build', sid, '--specs', str(sd / 'specs'), '--widths', str(win),
                                        '--grounds', 'newsprint', '--no-sweep', '--out', str(sd / 'out'), '--date', DATE], cwd=km[0].parents[2],
                                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
                    (sd / 'kit.log').write_text(r.stdout + r.stderr)
                    if png.exists():
                        stamp.write_text(sig_)
            if png.exists():
                MADE[made_key(it, pic)] = png
                FIG.setdefault('made', {})[made_key(it, pic)] = rel(png)
            else:
                warn('S59-label: the kit mirror made no picture')
        elif iid in C['slots'].get('made_kit', {}):
            # a chart built by the kit from a scratch copy of its spec with one opt-in key set (the spec in the repository
            # stays as it is), at the window that gives the guide's phone drawing, on Newsprint
            mk_ = C['slots']['made_kit'][iid]
            sid = mk_['spec'].lower()
            w_ = int(pic.get('width') or PHONE)
            mp = SCRATCH / 'shots' / f'm-{sid.upper()}-{w_}.json'
            mj = json.loads(mp.read_text()) if mp.exists() else {}
            sw = mj.get('svg_w') or (round(float(mj['el_w'])) if mj.get('el_w') else None)
            if not sw:
                warn(f'{iid}: no measure of {sid.upper()} at {w_} px yet; its picture waits')
                continue
            win = int(sw) + (32 if w_ < 600 else 64)
            sd = d / f'kit-{slug(iid)}'
            (sd / 'specs').mkdir(parents=True, exist_ok=True)
            spec_ = json.loads((ROOT / C['slots']['specs_dir'] / f'{sid}.json').read_text())
            spec_.update(mk_['set'])
            (sd / 'specs' / f'{sid}.json').write_text(json.dumps(spec_, indent=1, ensure_ascii=False))
            sig_ = sha(json.dumps(spec_, sort_keys=True), kit_shared_sig(), win)
            png = sd / 'out' / sid / f'{sid}-newsprint-{win}.png'
            stamp = sd / 'sig.txt'
            if not (reuse and png.exists() and stamp.exists() and stamp.read_text() == sig_):
                shutil.rmtree(sd / 'out', ignore_errors=True)
                if browser_gate(f'the kit, {iid}'):
                    r = subprocess.run(['node', str(ROOT / C['slots']['kit_command']), 'build', sid, '--specs', str(sd / 'specs'), '--widths', str(win),
                                        '--grounds', 'newsprint', '--no-sweep', '--out', str(sd / 'out'), '--date', DATE], cwd=ROOT,
                                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
                    (sd / 'kit.log').write_text(r.stdout + r.stderr)
                    if png.exists():
                        stamp.write_text(sig_)
            if png.exists():
                MADE[made_key(it, pic)] = png
                FIG.setdefault('made', {})[made_key(it, pic)] = rel(png)
            else:
                warn(f'{iid}: the kit made no picture in scratch')
        elif iid == 'red-target-keyline':
            # Rule 15.11's correct plate with the keyline flag set: chapter 15's generator imported read-only and run for
            # this one plate into a scratch Book, never written; its two keyline rects go in after the two red pills of a
            # scratch copy of the final build, and the red arrowhead takes the 1 px ink edge Rule 15.20's styles give it
            frags = keyline_fragments(d)
            if not frags:
                continue
            built, keyed = frags
            fs = src.find('id="fig-s-15-11-correct"')
            fa = src.rfind('<', 0, fs)
            fe = src.find('</figure>', fs)
            fig = src[fa:fe]
            if built.strip()[:200] not in fig:
                warn('Rule 15.11’s plate in the final build is not the generator’s as built; the keyline picture waits')
                continue
            new_fig, n_pk = fig, 0
            for m in re.finditer(r'<rect class="pk"[^>]*/>', keyed):
                pill = keyed[keyed.rfind('<rect', 0, m.start()):m.start()]
                if new_fig.count(pill) != 1:
                    continue
                new_fig = new_fig.replace(pill, pill + m.group(0))
                n_pk += 1
            edge = re.search(r':is\(\.lv \.dw,\.kd\) \.rt \.hd\{([^}]*)\}', src)
            if not n_pk or not edge:
                warn('the keyline picture could not be set: no keyline rect or no arrowhead edge style found')
                continue
            style = f'<style>#fig-s-15-11-correct .sv .rt .hd{{{edge.group(1)}}}</style>'
            text = src[:fa] + style + new_fig + src[fe:]
            copy = d / f'{DATE}_Rule-15-11-Keyline.html'
            if not copy.exists() or copy.read_text() != text:
                copy.write_text(text)
            PAGES['made-keyline'] = {'path': copy, 'text': text, 'frame': None}
            FIG['made_keyline'] = {'keyline_rects': n_pk, 'edge': edge.group(1)}
            items.append({'key': made_key(it, pic), 'page': 'made-keyline', 'el': 'fig-s-15-11-correct', 'w': int(pic.get('width') or DESK)})
        else:
            warn(f'the content file names {iid} under made, and the build knows no way to make it')
    if items:
        shots = run_shots(items, reuse, 'made')
        for x in items:
            if shots.get(x['key']) and shots[x['key']].exists():
                MADE[x['key']] = shots[x['key']]
        FIG.setdefault('made', {}).update({x['key']: rel(MADE[x['key']]) if x['key'] in MADE else None for x in items})
    # a picture made of two photographs, stacked with their labels (NB-S4: today's source row and the sketch's)
    for mk, parts in STACK.items():
        ps = [(MADE.get(k), lab) for k, lab in parts]
        if all(x and pathlib.Path(x).exists() for x, _ in ps):
            out = d / f'{mk}.png'
            stack_png(out, ps)
            MADE[mk] = out
            FIG.setdefault('made', {})[mk] = rel(out)


def stack_png(out, parts, gap=24, label_h=26):
    """Two or more photographs one above the other, each with its label in Inter Medium 13 px above it (board 2's look)."""
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(p).convert('RGB') for p, _ in parts]
    W = max(im.size[0] for im in ims)
    H = sum(im.size[1] + label_h for im in ims) + gap * (len(ims) - 1)
    cv = Image.new('RGB', (W, H), NEWSPRINT)
    dr = ImageDraw.Draw(cv)
    font = ImageFont.truetype(LABEL_FONT, 13)
    y = 0
    for im, (_, lab) in zip(ims, parts):
        dr.text((0, y + 4), lab, font=font, fill=LABEL_INK)
        cv.paste(im, (0, y + label_h))
        y += im.size[1] + label_h + gap
    cv.save(out, 'PNG', optimize=True)


def rule_name(rid):
    """A rule's name as a related-rules link prints it: its form's name where the plan gives one, else its title."""
    P = json.loads((ROOT / C['slots']['plan']).read_text())
    f = next((x for x in P['forms'] if x['rule'] == rid), None)
    if f:
        return f['form']
    num = rid.split('.')[0]
    for fp in sorted((ROOT / 'work/build/guide/chapters').glob(f'{num}-*.json')):
        r = next((x for x in json.loads(fp.read_text()).get('rules', []) if x.get('id') == rid), None)
        if r:
            return text_of(r.get('title', '')).rstrip('.')
    return ''


def kit_mirror(d, patch):
    """A scratch mirror of the chart kit: work/build/chart-kit copied, the folders it reads from the project root linked,
    and the patch applied to the copy ({file: [[old, new], ...]}). The repository's kit is never touched. -> (kit folder,
    signature) or None."""
    src = ROOT / C['slots']['kit_dir']
    m = d / 'kit-mirror'
    kit = m / 'work/build/chart-kit'
    sig = sha(kit_shared_sig(), json.dumps(patch, sort_keys=True), *[(src / f).read_bytes() for f in sorted(patch) if (src / f).exists()])
    stamp = m / 'sig.txt'
    if not (stamp.exists() and stamp.read_text() == sig):
        shutil.rmtree(kit, ignore_errors=True)
        shutil.copytree(src, kit, ignore=shutil.ignore_patterns('node_modules'))
        for name in ('tokens', 'assets', 'data', 'guide', 'node_modules'):
            ln = m / 'work/build' / name
            if not ln.exists():
                ln.symlink_to(ROOT / 'work/build' / name, target_is_directory=True)
        ex = m / 'work/extract'
        if not ex.exists():
            ex.symlink_to(ROOT / 'work/extract', target_is_directory=True)
        for f, pairs in patch.items():
            fp = kit / f
            t = fp.read_text()
            for old, new in pairs:
                if t.count(old) != 1:
                    warn(f'the kit mirror’s patch to {f} does not apply: {old[:60]}')
                    return None
                t = t.replace(old, new)
            fp.write_text(t)
        stamp.write_text(sig)
    return kit, sig


# ------------------------------------------------------------------------------------------------------- panel 1
def move_codes(s):
    """A teammate's words keep their sentences; a parenthesis that holds only studio codes moves to the reference line."""
    if not s:
        return s

    def mv(m):
        MOVED_REFS.extend(re.findall(STUDIO, m.group(0)))
        return ''
    s = re.sub(r'\s*\((?:' + STUDIO + r')(?:(?:,\s*|\s+and\s+|;\s*|\s+to\s+)(?:' + STUDIO + r'))*\)', mv, str(s))
    return re.sub(r'\s+([.,;:])', r'\1', s)


def picture_alt(it, pic, label, req):
    """B2-S3: a picture's alt text says what it shows: the data lead's alt, else the label, where the picture comes from
    and at what window, and the item's title."""
    if pic.get('alt'):
        return move_codes(pic['alt'])
    S = C['sections']['decide']
    if req['kind'] == 'made':
        return fill(S['alt_made'], {'label': label or it.get('title', ''), 'how': req.get('how', '')})
    src = S['alt_source'].get(pic.get('kind'), '')
    if pic.get('kind') == 'guide':
        src = fill(src, {'page': C['page_words'].get(req.get('page'), req.get('page'))})
    # B3-S5: a title that quotes words keeps them in single quotes inside the alt's own double quotes
    title = move_codes(it.get('title', '')).replace('“', '‘').replace('”', '’')
    what = fill(S['alt_other'], {'src': src, 'w': int(pic.get('width') or DESK), 'title': title})
    return (f'{label}. ' if label else '') + what


def picture_html(it, pics, shots):
    """An item's pictures, each at true size with its label above it. Pictures that share a `row` sit side by side, rows
    in order of first appearance; without rows, a "before" opens a row that the "after" pictures after it join, and views
    sit in rows of their own. Pictures marked `fold` go in one closed fold at the item's end (B2-M2). A picture still to
    make shows who makes it and how."""
    S = C['sections']['decide']
    out, n = [], 0
    for pic in pics:
        req = PIC_KEYS.get(id(pic))
        label = move_codes(pic.get('label') or '')
        role = pic.get('role') or 'view'
        if req is None:
            continue
        path = None
        if req['kind'] == 'guide':
            path = shots.get(req['key'])
        elif req['kind'] == 'made':
            path = MADE.get(req['key'])
        elif req['kind'] == 'path':
            path = req['file']
        if req['kind'] == 'missing' and req.get('owner'):
            who = req['owner']
            words_ = fill(S['to_make_wait'], {'owner_cap': cap(who), 'how': req.get('how', '').rstrip('.')})
            out.append((pic, f'<figure class="shot"><figcaption class="top"><b>{esc(label)}</b></figcaption>{pending(words_)}</figure>'))
            QUOTED.extend([label, words_])
            continue
        if req['kind'] == 'missing' or not path or not pathlib.Path(path).exists():
            out.append((pic, pending(fill(S['picture_wait'], {'path': label or str(req.get('why', ''))}))))
            continue
        if req['kind'] == 'made' and req.get('sketch'):
            label = fill(S['sketch_label'], {'label': label})
        n += 1
        rec = compose(f'Decide-{slug(it.get("id"))}-{n}', [(path, '')])
        alt = picture_alt(it, pic, label, req)
        QUOTED.extend([label, alt])
        rw = S['role_words'].get(role, '')
        cap_html = (f'<span class="role {esc(role)}">{esc(rw)}</span> ' if rw else '') + (f'<b>{esc(label)}</b>' if label else '')
        out.append((pic, figure(rec, alt, cap_html, top=True)))

    def arrange(lst):
        if any('row' in p for p, _ in lst):
            rows, order = {}, []
            for k, (p, h) in enumerate(lst):
                key = p.get('row', f'_{k}')
                if key not in rows:
                    rows[key] = []
                    order.append(key)
                rows[key].append(h)
            return ''.join(f'<div class="pair ba">{"".join(rows[k])}</div>' for k in order)
        rows, cur = [], None
        for p, h in lst:
            r = p.get('role') or 'view'
            kind = 'ba' if r in ('before', 'after') else 'view'
            if cur is None or r == 'before' or cur[0] != kind:
                cur = [kind, []]
                rows.append(cur)
            cur[1].append(h)
        return ''.join(f'<div class="pair {k}">{"".join(hs)}</div>' for k, hs in rows)
    lead = crop_html(it, shots)
    fold_ = lambda p: p.get('fold') or lead is not None or (str(it.get('id')), p.get('kind'), int(p.get('width') or DESK)) in FOLD_PICS
    main_ = [(p, h) for p, h in out if not fold_(p)]
    folded = [(p, h) for p, h in out if fold_(p)]
    html_ = (lead or '') + arrange(main_) + gray_pair_html(it, shots)
    if folded:
        ft = it.get('fold_title') or S['fold_title']
        QUOTED.append(ft)
        html_ += f'<details class="more pics"><summary>{esc(ft)}</summary>{arrange(folded)}</details>'
    return html_


def prose(s):
    """A teammate's sentence as text, with its Markdown code spans and bold set (board 1's reader)."""
    return B1.md_inline(s or '', quote=False)


def words(it, key):
    v = move_codes(it.get(key))
    if v:
        QUOTED.append(v)
    return v


def rows_table(rows, caption, names=None, cls='dt'):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys and k not in ('refs',):
                keys.append(k)
    names = names or C['sections']['decide']['row_heads']
    head = ''.join(f'<th scope="col">{esc(names.get(k, cap(k.replace("_", " "))))}</th>' for k in keys)
    body = ''
    for r in rows:
        cells = []
        for i, k in enumerate(keys):
            v = r.get(k, '')
            v = ', '.join(map(str, v)) if isinstance(v, list) else ('' if v is None else str(v))
            v = move_codes(v)
            QUOTED.append(v)
            if k == 'rule' and v and rid_anchor(v) in ANCHORS:
                cell = f'<a href="{esc(rule_href(v))}">{esc(v)}</a>'
            else:
                cell = esc(v)
            cells.append(f'<th scope="row">{cell}</th>' if i == 0 else f'<td>{cell}</td>')
        body += '<tr>' + ''.join(cells) + '</tr>'
    QUOTED.append(caption)
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{esc(caption)}; scrolls sideways"><table class="{cls}">'
            f'<caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def decide_item(it, S, shots, reply_n, refs):
    rule = it.get('rule')
    rr = it.get('refs') or []
    refs += rr if isinstance(rr, list) else re.split(r'[,;]\s*|\s+·\s+', rr)
    for k in ('ledger',):
        refs += [x for x in (it.get(k) or []) if isinstance(x, str)]
    reg = it.get('register') or {}
    if reg.get('code'):
        refs.append(f'register: {reg["code"]}')
    if (it.get('decision') or {}).get('code'):
        refs.append(it['decision']['code'])
    if it.get('question'):
        refs.append(str(it['question']))
    q = bool(it.get('question_for_dustin'))
    tags = ''
    if reply_n:
        tags += f' <span class="tag rn">{esc(fill(S["reply_tag"], {"n": reply_n}))}</span>'
    if q:
        tags += f' <span class="tag q">{esc(S["tag_question"])}</span>'
    label = join_words([x for x in [("Rule " + rule) if rule else "", ', '.join(s for s in item_specs(it) if s)] if x])
    head = ((f'<p class="label">{esc(label)}</p>' if label else '')
            + f'<h4 class="dec-h">{esc(words(it, "title") or it.get("id", ""))}{tags}</h4>')
    body = ''
    if it.get('answer'):
        body += f'<p class="dec-a">{prose(words(it, "answer"))}</p>'
    rec_ = words(it, 'recommendation')
    if rec_:
        body += f'<p class="dec-rec"><span class="tag rec">{esc(S["tag_rec"])}</span> {prose(rec_)}</p>'
    # B3-S8: a teammate's view beside the recommendation, as board 2 set the creative director's view on S12
    for v in it.get('views') or []:
        vt = move_codes(v.get('text', ''))
        QUOTED.extend([vt, v.get('note', '')])
        if v.get('source'):
            refs.append(str(v['source']))
        body += (f'<blockquote class="q"><p>{prose(vt)}</p><footer>{esc(fill(S.get("view_by", "The {who}’s view."), {"who": v.get("who", "")}))}'
                 + (f' {esc(v["note"])}' if v.get('note') else '') + '</footer></blockquote>')
    dl = [(S['what_changed'], words(it, 'what_changed')), (S['why'], words(it, 'why'))]
    if it.get('shows') is False and it.get('shows_note'):
        dl.append((S['shows_no'], words(it, 'shows_note')))
    st_ = it.get('settled') or {}
    if st_.get('touches'):
        t_ = '; '.join(move_codes(x) for x in st_['touches'])
        QUOTED.append(t_)
        dl.append((S['settled_touches'], t_))
    if st_.get('respects'):
        r_ = move_codes(st_['respects'])
        QUOTED.append(r_)
        dl.append((S['settled_respects'], r_))
    dl = [(a, b) for a, b in dl if b]
    if dl:
        body += '<dl class="facts f2">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{prose(b)}</dd></div>' for a, b in dl) + '</dl>'
    if it.get('steps'):
        body += rows_table([{k: x.get(k, '') for k in ('n', 'name', 'what_happens', 'law') if k in x} for x in it['steps']],
                           fill(S['steps_caption'], {'title': move_codes(it.get('title', '')), 'rule': it.get('rule') or ''}), S['step_heads'])
    if it.get('marks'):
        mk = it['marks'] if isinstance(it['marks'], list) else [it['marks']]
        mw = '; '.join(move_codes(m if isinstance(m, str) else ' '.join(str(v) for v in m.values())) for m in mk)
        QUOTED.append(mw)
        body += f'<dl class="facts"><div><dt>{esc(S["marks_k"])}</dt><dd>{esc(mw)}</dd></div></dl>'
    if it.get('facts'):
        fpath = [f for f in it['facts'] if re.search(PATH_RE, str(f.get('value', '')))]
        shown = [f for f in it['facts'] if f not in fpath]
        refs += [f'{f.get("label", "")}: {f.get("value", "")}' for f in fpath]
        if shown:
            body += '<dl class="facts">' + ''.join(f'<div><dt>{esc(move_codes(f.get("label", "")))}</dt><dd>{esc(move_codes(f.get("value", "")))}</dd></div>' for f in shown) + '</dl>'
        QUOTED.extend(move_codes(f.get('label', '')) + ' ' + move_codes(str(f.get('value', ''))) for f in shown)
    if it.get('counts'):
        rows = [{'label': x.get('label', ''), 'value': f'{x["value"]:,}' if isinstance(x.get('value'), int) else x.get('value', '')} for x in it['counts']]
        refs += sorted({x.get('from', '') for x in it['counts'] if x.get('from') and x.get('from') != 'the same'})
        body += rows_table(rows, S['counts_caption'], {'label': S['count_heads'][0], 'value': S['count_heads'][1]})
    if it.get('verb_led'):
        body += rows_table(it['verb_led'], S['verb_caption'], S['verb_heads'])
    if it.get('top'):
        tbl = rows_table(it['top'], S['top_caption'], S['top_heads'])
        body += f'<details class="more"><summary>{esc(S["top_caption"])}</summary>{tbl}</details>'
    if it.get('source'):
        refs.append(str(it['source']))
    if it.get('rows'):
        tbl = rows_table(it['rows'], fill(S['rows_caption'], {'title': move_codes(it.get('title', ''))}))
        if len(it['rows']) > int(S.get('rows_fold_over', 6)):
            body += f'<details class="more"><summary>{esc(fill(S["rows_summary"], {"n": len(it["rows"])}))}</summary>{tbl}</details>'
        else:
            body += tbl
    missing = False
    if it.get('pictures'):
        ph = picture_html(it, it['pictures'], shots)
        missing = 'class="pending"' in ph
        body += ph
    if rule and rid_anchor(rule) in ANCHORS:
        body += f'<p class="small"><a href="{esc(rule_href(rule))}">{esc(fill(S["entry_link"], {"rule": rule}))}</a></p>'
    aid = slug(it.get('id'))
    return f'<article class="dec" id="d-{esc(aid)}">{head}{body}</article>', missing, q


def decide_panel(shots):
    """Panel 1 serves the decision first (B2-M1): the replies Dustin owes as a numbered list with links, then the reply
    line; then the four groups in the decisions file's order, each reply's item or group tagged with its number."""
    S = C['sections']['decide']
    if D is None:
        return section('decide', f'<p class="intro">{esc(fill(S["lede"]))}</p>' + pending(S['wait']), ('waiting', 'data_lead'))
    refs = []
    reps = D.get('replies') or []
    FILL['n_replies_w'] = cap(nw(len(reps))) if reps else 'The'
    parts = [f'<p class="intro">{esc(fill(S["lede"]))}</p>']
    FILL['n_replies_w'] = nw(len(reps))
    reply = D.get('reply_line') or S['reply']
    QUOTED.append(reply)
    rmap = {}
    if reps:
        lis = []
        for k, r in enumerate(reps, 1):
            n = r.get('n', k)
            key = str(r.get('id') if r.get('id') is not None else r.get('item') or r.get('panel'))
            rmap[key] = n
            if r.get('id') is None and r.get('panel'):
                rmap[str(r['panel'])] = n
            line, rec = move_codes(r.get('line', '')), move_codes(r.get('recommendation', ''))
            QUOTED.extend([line, rec])
            aid = slug(r.get('id') if r.get('id') is not None else r.get('panel'))
            rr_ = (f'<span class="rr"><span class="k">{esc(S["tag_rec"])}</span> {esc(rec)}</span>' if rec else '')
            lis.append(f'<li><a href="#d-{esc(aid)}"><span class="rn">{esc(fill(S["reply_tag"], {"n": n}))}</span> <span class="rb"><span class="rl">{esc(line)}</span>{rr_}</span></a></li>')
        parts.append(f'<h3 class="sub rep-h">{esc(fill(S["replies_h"], {"n": nw(len(reps))}))}</h3><ol class="replies">{"".join(lis)}</ol>')
    else:
        parts.append(pending(S['replies_wait']))
    parts.append(f'<p class="reply">{esc(reply)}</p>')
    tw = panel_words(''.join(parts))
    tm = max(1, round(tw / 200))
    FILL.update({'p1_top_words': f'{tw:,}', 'p1_top_min': f'{nw(tm)} minute' + ('' if tm == 1 else 's')})
    FIG['panel_1_top_words'] = tw
    n_items = n_q = 0
    missing = []
    for g in D.get('panels', []):
        gid = g.get('id', '')
        items = g.get('items', [])
        title = words(g, 'title') or gid
        gn = rmap.get(gid)
        gtag = f' <span class="tag rn">{esc(fill(S["reply_tag"], {"n": gn}))}</span>' if gn else ''
        inner = ''
        if g.get('lede'):
            inner += f'<p class="intro">{prose(words(g, "lede"))}</p>'
        if g.get('approval') == 'one':
            inner += f'<p class="approve">{esc(S["approval_one"])}</p>'
        elif g.get('approval') == 'each' and len(items) > 1:
            inner += f'<p class="approve">{esc(S["approval_each"])}</p>'
        if not items:
            inner += pending(S['group_wait'])
            missing.append(gid)
        grefs = []
        for it in items:
            n_items += 1
            rn_ = rmap.get(str(it.get('id')))
            h, miss, q = decide_item(it, S, shots, rn_, grefs)
            n_q += q
            if miss:
                missing.append(it.get('id'))
            inner += h
        refs += grefs
        parts.append(f'<h3 class="sub grp" id="d-{esc(slug(gid))}">{esc(title)}{gtag}</h3>{inner}')
    for item, n in rmap.items():
        if not any(str(it.get('id')) == item for g in D.get('panels', []) for it in g.get('items', [])) and not any(g.get('id') == item for g in D.get('panels', [])):
            warn(f'reply {n} names {item}, which no item or group holds')
    waiting_pics = sum(1 for it, pic in all_pictures(D) if (PIC_KEYS.get(id(pic)) or {}).get('kind') == 'missing')
    FIG['decide'] = {'items': n_items, 'questions': n_q, 'replies': len(reps), 'state': D.get('state'), 'items_waiting': missing,
                     'pictures_waiting': waiting_pics}
    FILL.update({'n_items': n_items, 'n_questions_w': nw(n_q)})
    refs = [r.strip() for r in refs + MOVED_REFS if r and r.strip()]
    MOVED_REFS.clear()
    st = ('ready' if D.get('state') == 'signed off' and not missing and reps else
          ('partial', 'data_lead' if D.get('state') != 'signed off' or not reps else 'pictures'))
    return section('decide', ''.join(parts), st, ' · '.join(dict.fromkeys(refs)))


# ------------------------------------------------------------------------------------------------------- panel 2
def printed(G, sid):
    """What the guide prints round a chart: title, evidence label, grade line, source line and table."""
    fig = element_html(G['text'], f'oac-s-14-{sid.lower()}') or ''
    get = lambda cls: (lambda m: text_of(m.group(1)) if m else None)(re.search(r'<p class="' + cls + r'"[^>]*>(.*?)</p>', fig, flags=re.S))
    tb = re.search(r'<table class="oac-table".*?</table>', fig, flags=re.S)
    return {'title': get('oac-title'), 'evidence': get('oac-ev-k'), 'grade': get('oac-ev-g'), 'source': get('oac-source'),
            'table': tb.group(0) if tb else None, 'found': bool(fig)}


def clean_table(t, name):
    """The guide's table as live text: its caption, heads and cells, with the guide's classes and data attributes left
    out and text columns marked so numbers line up."""
    t = re.sub(r'<span class="oac-vh">.*?</span>', '', t, flags=re.S)

    def tag(m):
        nm, attrs = m.group(1), m.group(2) or ''
        keep = re.findall(r'\s(scope|colspan|rowspan)="([^"]*)"', attrs)
        text_col = re.search(r'class="[^"]*\bt\b[^"]*"', attrs) and nm in ('th', 'td')
        a = ''.join(f' {k}="{v}"' for k, v in keep) + (' class="t"' if text_col else '')
        return f'<{nm}{a}>'
    t = re.sub(r'<(table|caption|thead|tbody|tfoot|tr|th|td)(\s[^>]*)?>', tag, t)
    t = re.sub(r'<(?!/?(?:table|caption|thead|tbody|tfoot|tr|th|td|b|i|em|strong|br)\b)[^>]+>', '', t)
    t = t.replace('<table>', '<table class="ft">', 1)
    return f'<div class="tw" role="region" tabindex="0" aria-label="{esc(name)}; scrolls sideways">{t}</div>'


def form_order(rn, held):
    """The plan's families in its order; within each, the avoid sketches first, then the plan's order."""
    fams = list(dict.fromkeys(f['family_section'] for f in rn))
    kind = lambda f: (held.get(f['rule'], {}).get('correct') or {}).get('kind', '')
    out = []
    for fs in fams:
        fl = [f for f in rn if f['family_section'] == fs]
        out += [f for f in fl if f['status'] == 'sketch' and kind(f) == 'avoid'] + [f for f in fl if not (f['status'] == 'sketch' and kind(f) == 'avoid')]
    return out


def sketch_print(G, specimen):
    src = element_html(G['text'], f'fig-{specimen}') or ''
    m = re.search(r'class="plate-label-t">(.*?)</span>', src, flags=re.S)
    c = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', src, flags=re.S)
    chip_, words_ = '', ''
    if c:
        k = re.search(r'<span class="illus">(.*?)</span>', c.group(1), flags=re.S)
        chip_ = text_of(k.group(1)) if k else ''
        words_ = text_of(re.sub(r'<span class="illus">.*?</span>', '', c.group(1), flags=re.S))
    return (text_of(m.group(1)) if m else None), chip_, words_


def form_head(f, held, S, extra=''):
    rid = f['rule']
    r = held.get(rid, {})
    maker = C['makers'].get(f.get('maker'), f.get('maker') or '')
    line = ' · '.join(x for x in [f'Rule {rid}', f.get('tier', ''), f'Round {f["round"]}', maker] if x)
    link = f'<a class="live" href="{esc(rule_href(rid))}">{esc(S["live"])}</a>' if rid_anchor(rid) in ANCHORS else ''
    return (f'<header class="f-h"><div class="f-top"><p class="label">{esc(line)}</p>{link}</div>'
            f'<h4 class="f-t">{esc(f["form"])}{extra}</h4>'), r


def plate_weight(G, sid):
    """The chart's bytes as the final build places it, from the build's report (board 3 has no frame measure)."""
    placed = ((G['report'].get('weight', {}).get('charts', {}).get(f's-14-{sid.lower()}') or {}).get('bytes'))
    return {'placed': placed}


def form_article(G, f, held, S, kit_out, pages, rendered, sk_shots):
    rid, sid = f['rule'], f.get('spec_id')
    aid = f'form-{rid.replace(".", "-")}'
    rec = {'rule': rid, 'form': f['form'], 'tier': f.get('tier'), 'round': f['round'], 'maker': f.get('maker'), 'status': f['status']}
    if f['status'] == 'sketch':
        r = held.get(rid, {})
        corr = r.get('correct') or {}
        kind = corr.get('kind', '')
        tag = f' <span class="tag av">{esc(S["tag_avoid"])}</span>' if kind == 'avoid' else ''
        head, _ = form_head(f, held, S, tag)
        uw = text_of(r.get('use_when', ''))
        QUOTED.extend([uw, r.get('title', '')])
        head += (f'<p class="f-rt">{esc(r.get("title", ""))}</p>' + (f'<p class="f-q"><span class="k">{esc(S["use_when"])}</span> {esc(uw)}</p>' if uw else '') + '</header>')
        specimen = f.get('sketch_id') or corr.get('specimen')
        hd, chip_, wd = sketch_print(G, specimen) if G['usable'] else (None, '', '')
        QUOTED.extend([hd or '', chip_, wd])
        p = sk_shots.get(f'sketch-{rid}')
        if hd and p and p.exists():
            im = compose(f'Sketch-{rid.replace(".", "-")}', [(p, '')])
            capt = (f'{esc(S["heading_k"])} <b>{esc(hd)}</b><br>{esc(S["caption_k"])} ' + (f'<span class="chip">{esc(chip_)}</span> ' if chip_ else '') + esc(wd))
            body = figure(im, f'The sketch for Rule {rid}, headed “{hd}”, with its caption, as the final build prints it at a 1440 px window, at true size. {wd}', capt)
            ok = True
        else:
            body = pending(S['wait_photo'])
            ok = False
        rec.update({'kind': kind or 'sketch', 'specimen': specimen, 'heading': hd, 'caption': wd})
        return f'<article class="form sk" id="{aid}">{head}{body}</article>', rec, ok
    head, r = form_head(f, held, S)
    lo = sid.lower()
    spec = json.loads((ROOT / C['slots']['specs_dir'] / f'{lo}.json').read_text())
    q = spec.get('reader_question') or f.get('reader_question') or ''
    QUOTED.append(q)
    pr = printed(G, sid) if G['usable'] else {'found': False}
    title = pr.get('title') or spec.get('title', '')
    ev = pr.get('evidence') or spec.get('evidence_label') or ''
    QUOTED.extend([title, ev, pr.get('source') or '', pr.get('grade') or ''])
    if G['usable'] and not pr.get('found'):
        warn(f'{sid} was not found in the final build')
    est = ev.strip().lower() == C['sections']['forms']['estimate_label'].lower()
    head += (f'<p class="f-q"><span class="k">{esc(S["question"])}</span> {esc(q)}</p>' if q else '')
    head += f'<div class="f-ev"><span class="ev-k{" est" if est else ""}">{esc(ev)}</span><p class="f-ct">{esc(title)}</p></div></header>'
    notes = []
    if sid in rendered:
        notes.append(fill(S['shared_spec'], {'rule': rendered[sid]}))
    d = kit_out / lo
    chk_p = d / f'{lo}-check.json'
    dp, pw = pages.get(sid, (DESK, PHONE))
    caps = {(g, w, x): d / f'{lo}-{g}-{w}{x}.png' for g in ('newsprint', 'charcoal') for w in (dp, pw) for x in ('', '-grayscale')}
    body = ''
    if notes:
        body += '<p class="what">' + ' '.join(esc(n) for n in notes) + '</p>'
    ok = True
    # a social data card (Rule 14.141) draws its own crops at 1080 px whatever the window: the kit's page at 1440 px shows
    # both crops, on each ground, and stands in for the desk and phone pair
    card = {(g, x): d / f'{lo}-{g}-1440{x}.png' for g in ('newsprint', 'charcoal') for x in ('', '-grayscale')}
    is_card = (chk_p.exists() and not all(p.exists() for p in caps.values()) and all(p.exists() for p in card.values())
               and all(int(x.get('width', 0)) == 1080 for x in json.loads(chk_p.read_text()).get('drawings', [])))
    if is_card:
        chk = json.loads(chk_p.read_text())
        crops = join_words([f'{x["width"]:,} by {x["height"]:,}' for x in chk.get('drawings', []) if x['ground'] == 'newsprint'])
        lab = fill(S['label_card'], {'crops': crops})
        alt = text_of(spec.get('alt', ''))
        pics = []
        for g, gname in (('newsprint', S['row_newsprint']), ('charcoal', S['row_charcoal'])):
            pad = CHARCOAL if g == 'charcoal' else None
            im = compose(f'Form-{sid}-{cap(g)}', [(card[(g, '')], lab, pad)])
            a = f'{f["form"]}, Rule {rid}, on {cap(g)}: the kit’s page at a {DESK} px window with the card in its crops of {crops} px.' + (f' {alt}' if g == 'newsprint' else '')
            pics.append(f'<p class="row-label">{esc(gname)}</p>{frame(im, a)}')
            if g == 'newsprint':
                FORMPIC.setdefault(sid, (im, rid, a))
        im = compose(f'Form-{sid}-Grayscale', [(card[('newsprint', '-grayscale')], fill(S['gray_label'], {'g': 'Newsprint', 'w': DESK})),
                                               (card[('charcoal', '-grayscale')], fill(S['gray_label'], {'g': 'Charcoal', 'w': DESK}), CHARCOAL)], cols=1)
        pics.append(f'<details class="more gray"><summary>{esc(S["row_gray"])}</summary>{frame(im, f"{f["form"]}, Rule {rid}, in grayscale: Newsprint and Charcoal, the kit’s page at a {DESK} px window.")}</details>')
        body += ''.join(pics)
        faults = chk.get('faults', [])
        result = S['kit_pass'] if not faults else fill(S['kit_faults'], {'n': nw(len(faults))})
        if pr.get('source'):
            body += f'<p class="src">{esc(pr["source"])}</p>'
        W_ = plate_weight(G, sid)
        bytes_line = fill(S['bytes_line'], {'placed': f'{W_["placed"]:,}'}) if W_['placed'] is not None else S['bytes_wait']
        body += f'<p class="ch-line">{esc(bytes_line)} {esc(result)}</p>'
        ok = not faults
        rec.update({'weight': W_, 'faults': len(faults), 'card': crops})
    elif not chk_p.exists() or not all(p.exists() for p in caps.values()):
        body += pending(S['wait_kit'])
        ok = False
    else:
        chk = json.loads(chk_p.read_text())
        dw = {(x['ground'], x['page']): x['width'] for x in chk.get('drawings', [])}
        m14 = MEAS.get(sid, {}).get(DESK) or {}
        framed = m14.get('el_w') and m14.get('svg_w') and float(m14['el_w']) < float(m14['svg_w']) - 2
        lab = lambda w: fill((S['label_desk_frame'] if framed else S['label_desk']) if w == dp else S['label_phone'], {'px': dw.get(('newsprint', w), '?')})
        stem = f'Form-{sid}'
        alt = text_of(spec.get('alt', ''))
        pics = []
        for g, gname in (('newsprint', S['row_newsprint']), ('charcoal', S['row_charcoal'])):
            pp = [caps[(g, dp, '')], caps[(g, pw, '')]]
            pad = CHARCOAL if g == 'charcoal' else None
            ncol = side_or_stack(pp, extra=2 * PAD if pad else 0)
            im = compose(f'{stem}-{cap(g)}', [(pp[0], lab(dp), pad), (pp[1], lab(pw), pad)], cols=ncol)
            a = f'{f["form"]}, Rule {rid}, on {cap(g)}, drawn for a {DESK} px window and a {PHONE} px window, as the guide draws them.' + (f' {alt}' if g == 'newsprint' else '')
            hint = f'<p class="narrow-hint">{esc(S["narrow_hint"])}</p>' if ncol > 1 else ''
            pics.append(f'<p class="row-label">{esc(gname)}</p>{hint}{frame(im, a, cls="dp" if ncol > 1 else "")}')
            if g == 'newsprint':
                FORMPIC.setdefault(sid, (im, rid, a))
        gp = [(caps[('newsprint', dp, '-grayscale')], fill(S['gray_label'], {'g': 'Newsprint', 'w': DESK})), (caps[('newsprint', pw, '-grayscale')], fill(S['gray_label'], {'g': 'Newsprint', 'w': PHONE})),
              (caps[('charcoal', dp, '-grayscale')], fill(S['gray_label'], {'g': 'Charcoal', 'w': DESK}), CHARCOAL), (caps[('charcoal', pw, '-grayscale')], fill(S['gray_label'], {'g': 'Charcoal', 'w': PHONE}), CHARCOAL)]
        cols = 2 if side_or_stack([gp[0][0], gp[1][0]], extra=2 * PAD) == 2 else 1
        im = compose(f'{stem}-Grayscale', gp, cols=cols)
        pics.append(f'<details class="more gray"><summary>{esc(S["row_gray"])}</summary>{frame(im, f"{f["form"]}, Rule {rid}, in grayscale: Newsprint and Charcoal, each at a {DESK} px window and a {PHONE} px window.")}</details>')
        body += ''.join(pics)
        faults = chk.get('faults', [])
        result = S['kit_pass'] if not faults else fill(S['kit_faults'], {'n': nw(len(faults))})
        src = pr.get('source')
        if src:
            body += f'<p class="src">{esc(src)}</p>'
        W_ = plate_weight(G, sid)
        bytes_line = fill(S['bytes_line'], {'placed': f'{W_["placed"]:,}'}) if W_['placed'] is not None else S['bytes_wait']
        body += f'<p class="ch-line">{esc(bytes_line)} {esc(result)}</p>'
        if faults:
            ok = False
            QUOTED.extend(faults[:3])
            body += '<ul class="faults">' + ''.join(f'<li>{esc(B1.strip_codes(str(x))[:200])}</li>' for x in faults[:3]) + '</ul>'
        rec.update({'weight': W_, 'faults': len(faults), 'kit_windows': [dp, pw], 'drawn': {f'{g} {p}': w for (g, p), w in dw.items()}})
    if pr.get('table'):
        capm = re.search(r'<caption>(.*?)</caption>', pr['table'], flags=re.S)
        cname = text_of(capm.group(1)) if capm else f'The table for Rule {rid}'
        QUOTED.append(cname)
        QUOTED.append(text_of(pr['table']))
        body += f'<details class="more"><summary>{esc(S["table_summary"])}<span class="vh">: {esc(cname)}</span></summary>{clean_table(pr["table"], cname)}</details>'
    elif G['usable']:
        warn(f'{sid}: the final build prints no table')
    rec.update({'spec': sid, 'title': title, 'evidence': ev, 'estimate': est, 'question': q})
    rendered.setdefault(sid, rid)
    return f'<article class="form" id="{aid}">{head}{body}</article>', rec, ok


def forms_panel(G, P, rn, held, kit_out, pages, sk_shots):
    S = C['sections']['forms']
    groups = {g.get('family_section'): g for g in P['groups']}
    order = form_order(rn, held)
    parts, cur, n_ok, est, missing = [], None, 0, [], []
    idx = []
    rendered = {}
    for f in order:
        if f['family_section'] != cur:
            cur = f['family_section']
            g = groups.get(cur, {})
            QUOTED.append(g.get('title', ''))
            fl = [x for x in order if x['family_section'] == cur]
            parts.append(f'<h3 class="sub grp fam" id="fam-{cur.replace(".", "-")}">{esc(g.get("title", f["family"]))}</h3>'
                         f'<p class="small">{esc(fill(S["family_line"], {"n": len(fl), "n_w": nw(len(fl)), "s": sum(1 for x in fl if x["status"] == "sketch")}))}</p>')
            idx.append([g.get('title', f['family']), cur, []])
        body, rec, ok = form_article(G, f, held, S, kit_out, pages, rendered, sk_shots)
        parts.append(body)
        idx[-1][2].append(f)
        FIG.setdefault('forms', {})[f['rule']] = rec
        n_ok += ok
        if rec.get('estimate'):
            est.append(f['rule'])
        if not ok:
            missing.append(f['rule'])
    nav = ('<nav class="fidx" aria-label="' + esc(S['index_h']) + '">' + ''.join(
        f'<div class="fam-i"><p class="fam-n"><a href="#fam-{fs.replace(".", "-")}">{esc(re.sub(r":.*$", "", t))}</a></p><ol>'
        + ''.join(f'<li><a href="#form-{x["rule"].replace(".", "-")}"' + (' class="sk"' if x['status'] == 'sketch' else '') + f'>{esc(x["rule"])}</a></li>' for x in fl) + '</ol></div>'
        for t, fs, fl in idx) + '</nav>')
    n_sk = sum(1 for f in rn if f['status'] == 'sketch')
    n_sp = len({f['spec_id'] for f in rn if f.get('spec_id')})
    FILL.update({'n_forms': len(rn), 'n_spec_rows': sum(1 for f in rn if f.get('spec_id')), 'n_specs': n_sp, 'n_sketches': n_sk,
                 'n_est_w': nw(len(est)), 'est_rules': join_words(est), 'n_fams': len(idx)})
    FIG['forms_summary'] = {'forms': len(rn), 'shown': len(order), 'ready': n_ok, 'estimate': est, 'waiting': missing}
    lede = (f'<p class="intro">{esc(fill(S["lede"]))}</p><p>{esc(fill(S["how"]))}</p>'
            + f'<p class="measure">{esc(S["measure_line"])}</p>'
            + (f'<p>{esc(fill(S["lede_est"]))}</p>' if est else ''))
    st = 'ready' if not missing and G['ok'] else ('partial', 'final' if not G['ok'] else 'kit')
    if missing:
        lede += pending(fill(S['wait_some'], {'list': join_words(missing[:12]) + (f' and {len(missing) - 12} more' if len(missing) > 12 else '')}))
    return section('forms', lede + nav + ''.join(parts), st)


# ------------------------------------------------------------------------------------------------------- panel 3
def caption_text(x):
    return text_of(x.get('caption', '')) if isinstance(x, dict) else ''


def gkey(page, el, w):
    return f'g-{page}-{slug(el)}-{w}'


def chapter15():
    ch = json.loads((ROOT / C['slots']['chapter15']).read_text())
    return ch, {r['id']: r for r in ch['rules']}


def r5_charts(held):
    """Rules 14.142 to 14.144, each with its correct and failure plates' elements, read from chapter 14's file."""
    out = []
    for rid in ('14.142', '14.143', '14.144'):
        r = held.get(rid) or {}
        c, f = (r.get('correct') or {}).get('specimen'), (r.get('failure') or {}).get('specimen')
        out.append({'rule': rid, 'title': r.get('title', ''), 'correct': f'fig-{c}' if c else None, 'failure': f'fig-{f}' if f else None,
                    'cc': caption_text(r.get('correct')), 'fc': caption_text(r.get('failure'))})
    return out


def r5_items(held):
    """Every photograph panel 3 asks of the final build, in priority order."""
    S = C['sections']['round5']
    items = [{'key': gkey('final', 'fig-s-14-selection-guide', w), 'page': 'final', 'el': 'fig-s-14-selection-guide', 'w': w} for w in (DESK, PHONE)]
    items.append({'key': gkey('final', 'fig-s-14-palette-spec', DESK), 'page': 'final', 'el': 'fig-s-14-palette-spec', 'w': DESK})
    for ch in r5_charts(held):
        if ch['correct']:
            items += [{'key': gkey('final', ch['correct'], w), 'page': 'final', 'el': ch['correct'], 'w': w} for w in (DESK, PHONE)]
        if ch['failure']:
            items.append({'key': gkey('final', ch['failure'], DESK), 'page': 'final', 'el': ch['failure'], 'w': DESK})
        for k, stt in enumerate(S['states'].get(ch['rule'], [])):
            if stt.get('actions') and ch['correct']:
                # each action's selector is read inside the chart's own figure, since other choosers share its names
                acts = [{kk: (f'#{ch["correct"]} {vv}' if kk in ('click', 'check') else vv) for kk, vv in x.items()} for x in stt['actions']]
                items.append({'key': f'st-{slug(ch["rule"])}-{k}', 'page': 'final', 'el': ch['correct'], 'w': DESK,
                              'actions': acts, 'session': f'states-{ch["rule"]}'})
    return items


def selection_counts(G):
    fig = element_html(G['text'], 'fig-s-14-selection-guide') or ''
    hrefs = re.findall(r'<a\b[^>]*href="#([^"]+)"', fig)
    form = sum(1 for h in hrefs if re.fullmatch(r'rule-14-(\d+)', h) and 15 <= int(h.split('-')[-1]) <= 141)
    road = sum(1 for h in hrefs if re.fullmatch(r'rule-14-14[234]|rule-15-\d+', h))
    qs = len(re.findall(r'class="[^"]*\bsg-q\b', fig))
    return {'form_links': form, 'road_links': road, 'questions': qs}


def one_pic(shots, key, name, alt, label=''):
    p = shots.get(key)
    if not p or not p.exists():
        return None
    rec = compose(name, [(p, '')])
    QUOTED.extend([alt, label])
    return figure(rec, alt, f'<b>{esc(label)}</b>' if label else '', top=True)


def round5_panel(G, held, shots):
    S = C['sections']['round5']
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    missing = []
    # the selection guide
    sc = selection_counts(G) if G['usable'] else {}
    # the brief's counts are read from the check: the four-width guide check on version 13, where it has landed; the
    # board's own count of the page stands in until then, and the two must agree
    cp = scratch_path(C['slots'].get('four_width_check'))
    if cp and cp.is_file():
        sg = ((json.loads(cp.read_text()).get('runs') or [{}])[0].get('selectionGuide') or {})
        ck = {'form_links': sg.get('links'), 'road_links': sg.get('road'), 'questions': sg.get('questions')}
        if all(v is not None for v in ck.values()):
            if sc and ck != sc:
                warn(f'the selection guide: the check counts {ck} and the page {sc}')
            sc = ck
    FIG['selection_guide'] = sc
    out.append(f'<h3 class="sub grp" id="r5-guide">{esc(S["guide_h"])}</h3>')
    if sc:
        out.append(f'<p>{esc(fill(S["guide_line"], sc))}</p>')
    row = []
    for w in (DESK, PHONE):
        h = one_pic(shots, gkey('final', 'fig-s-14-selection-guide', w), f'R5-Guide-{w}',
                    f'Choose a chart, the guide that opens chapter 14, as the final build draws it at a {w} px window, at true size: '
                    f'{sc.get("questions", "the")} questions, each with its forms as named symbols and links.', f'At a {w} px window')
        if h:
            row.append(h)
        else:
            missing.append(f'the guide at {w} px')
            row.append(pending(S['wait']))
    out.append(f'<div class="pair view">{"".join(row)}</div>')
    # the palette plate
    out.append(f'<h3 class="sub grp" id="r5-palette">{esc(S["palette_h"])}</h3>')
    h = one_pic(shots, gkey('final', 'fig-s-14-palette-spec', DESK), 'R5-Palette-1440',
                'The palette plate after Rule 14.5 at a 1440 px window, at true size: the four data palettes, each with its job and its steps, '
                'with the ground and label ratios printed beside each step.', 'At a 1440 px window')
    if h:
        out.append(h)
    else:
        missing.append('the palette plate')
        out.append(pending(S['wait']))
    # the three charts in full
    out.append(f'<h3 class="sub grp" id="r5-charts">{esc(S["charts_h"])}</h3>')
    for ch in r5_charts(held):
        rid = ch['rule']
        QUOTED.append(ch['title'])
        link = f' <a class="live" href="{esc(rule_href(rid))}">{esc(S["chart_live"])}</a>' if rid_anchor(rid) in ANCHORS else ''
        art = f'<article class="rule" id="r5-{slug(rid)}"><h4 class="r-h"><span class="rid">Rule {esc(rid)}{link}</span> {esc(ch["title"])}</h4>'
        pics = []
        for w, lab in ((DESK, fill(S['correct_label'], {'w': DESK})), (PHONE, S['phone_label'])):
            h = one_pic(shots, gkey('final', ch['correct'], w), f'R5-{slug(rid)}-{w}', f'Rule {rid}’s chart in full at a {w} px window, at true size. {ch["cc"]}', lab) if ch['correct'] else None
            if h:
                pics.append(h)
            else:
                missing.append(f'Rule {rid} at {w} px')
                pics.append(pending(S['wait']))
        art += f'<div class="pair view">{"".join(pics)}</div>'
        h = one_pic(shots, gkey('final', ch['failure'], DESK), f'R5-{slug(rid)}-Failure', f'Rule {rid}’s failure plate at a 1440 px window, at true size. {ch["fc"]}', S['failure_label']) if ch['failure'] else None
        if h:
            art += h
        else:
            missing.append(f'Rule {rid}’s failure plate')
            art += pending(S['wait'])
        sts = S['states'].get(rid) or []
        if sts:
            row = []
            for k, stt in enumerate(sts):
                key = f'st-{slug(rid)}-{k}' if stt.get('actions') else gkey('final', ch['correct'], DESK)
                h = one_pic(shots, key, f'R5-{slug(rid)}-State-{k}', f'Rule {rid}’s chart in full at a 1440 px window, {stt["label"][0].lower() + stt["label"][1:]}, at true size.', stt['label'])
                if h:
                    row.append(h)
                else:
                    missing.append(f'Rule {rid}: {stt["label"]}')
                    row.append(pending(S['wait']))
            art += f'<details class="more pics"><summary>{esc(S["states_h"])}</summary><div class="pair view">{"".join(row)}</div></details>'
        out.append(art + '</article>')
    FIG['round5'] = {'missing': missing}
    return section('round5', ''.join(out), 'ready' if not missing and G['ok'] else ('partial', 'render' if G['usable'] else 'final'))


# ------------------------------------------------------------------------------------------------------- panel 4
def c15_items(held15):
    S = C['sections']['ch15']
    items = []
    for r in held15.values():
        for k in ('correct', 'failure'):
            sp = (r.get(k) or {}).get('specimen')
            if sp:
                items.append({'key': gkey('final', f'fig-{sp}', DESK), 'page': 'final', 'el': f'fig-{sp}', 'w': DESK})
    for rid in S['phone_rules']:
        sp = ((held15.get(rid) or {}).get('correct') or {}).get('specimen')
        if sp:
            items.append({'key': gkey('final', f'fig-{sp}', PHONE), 'page': 'final', 'el': f'fig-{sp}', 'w': PHONE})
    return items


def ch15_panel(G, ch15, held15, shots):
    S = C['sections']['ch15']
    FILL['n_15'] = len(held15)
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    missing = []
    op = (ch15.get('opener') or {}).get('specimen')
    for r in held15.values():
        rid = r['id']
        keys = [(k, f'fig-{r[k]["specimen"]}') for k in ('correct', 'failure') if isinstance(r.get(k), dict) and r[k].get('specimen')]
        have = [(k, shots[gkey('final', el, DESK)]) for k, el in keys if shots.get(gkey('final', el, DESK), pathlib.Path('-')).exists()]
        QUOTED.append(r['title'])
        link = f' <a class="live" href="{esc(rule_href(rid))}">{esc(S["live"])}</a>' if rid_anchor(rid) in ANCHORS else ''
        h = f'<h3 class="r-h" id="c15-{rid.replace(".", "-")}"><span class="rid">Rule {esc(rid)}{link}</span> {esc(r["title"])}</h3>'
        if len(have) < len(keys) or not keys:
            missing.append(f'Rule {rid}')
            out.append(f'<article class="rule">{h}{pending(S["wait"])}</article>')
            continue
        side = side_or_stack([p for _, p in have])
        rec = compose(f'C15-{rid.replace(".", "-")}-Plates', [(p, '') for _, p in have], cols=side, gap=24 if side > 1 else 32)
        cc, fc = caption_text(r.get('correct')), caption_text(r.get('failure'))
        alt = (f'Rule {rid}: the correct plate, then the failure plate, ' + ('side by side' if side > 1 else 'one above the other')
               + f', as the final build draws them at a 1440 px window. Correct: {cc} Failure: {fc}')
        out.append(f'<article class="rule">{h}{figure(rec, alt)}</article>')
        FIG.setdefault('ch15', {})[rid] = {'plates': len(have), 'layout': 'side by side' if side > 1 else 'stacked', 'size': [rec['w'], rec['h']]}
    # phone views
    out.append(f'<h3 class="sub grp" id="c15-phone">{esc(S["phone_h"])}</h3><p>{esc(S["phone_lede"])}</p>')
    row = []
    for rid in S['phone_rules']:
        sp = ((held15.get(rid) or {}).get('correct') or {}).get('specimen')
        h = one_pic(shots, gkey('final', f'fig-{sp}', PHONE), f'C15-{slug(rid)}-390',
                    f'Rule {rid}’s correct plate at a 390 px window, at true size. {caption_text((held15.get(rid) or {}).get("correct"))}', f'Rule {rid} at a 390 px window') if sp else None
        if h:
            row.append(h)
        else:
            missing.append(f'Rule {rid} at 390 px')
            row.append(pending(S['wait']))
    out.append(f'<div class="pair view">{"".join(row)}</div>')
    # the reconciliation table
    out.append(f'<h3 class="sub grp" id="c15-recon">{esc(S["recon_h"])}</h3><p>{esc(S["recon_lede"])}</p>')
    sp = ((held15.get('15.25') or {}).get('correct') or {}).get('specimen')
    fig = element_html(G['text'], f'fig-{sp}') if sp and G['usable'] else None
    tabs = re.findall(r'<table\b.*?</table>', fig or '', flags=re.S)
    v71 = 0
    for k, tb in enumerate(tabs):
        capm = re.search(r'<caption[^>]*>(.*?)</caption>', tb, flags=re.S)
        cname = text_of(capm.group(1)) if capm else f'Rule 15.25’s table {k + 1}'
        QUOTED.extend([cname, text_of(tb)])
        v71 += len(re.findall(r'<tr\b(?:(?!</tr>).)*V7\.1(?:(?!</tr>).)*</tr>', tb, flags=re.S))
        t_ = clean_table(tb, cname).replace('<table class="ft">', '<table class="ft rc">', 1)
        out.append(t_ if k == 0 else f'<details class="more"><summary>{esc(cname)}</summary>{t_}</details>')
    if not tabs:
        missing.append('the reconciliation table')
        out.append(pending(S['wait']))
    FIG['reconciliation'] = {'tables': len(tabs), 'rows_naming_v7_1': v71}
    FIG['ch15_missing'] = missing
    return section('ch15', ''.join(out), 'ready' if not missing and G['ok'] else ('partial', 'render' if G['usable'] else 'final'))


# ------------------------------------------------------------------------------------------------------- panel 5
def bar_rows(rows, cols, caption, unit=''):
    """A live table with a bar per row: rows [(name, value, limit, passes)]."""
    mx = max([v for _, v, lim, _ in rows] + [lim or 0 for _, _, lim, _ in rows] + [1])
    trs = ''
    for name, v, lim, ok in rows:
        share = 100 * v / mx
        tick = f'<span class="lim" style="left:{100 * lim / mx:.3f}%"></span>' if lim else ''
        trs += (f'<tr><th scope="row">{esc(name)}</th><td class="barcell"><span class="track">{tick}<span class="bar" data-mark="bar" data-value="{v}" data-key="{esc(name)}" style="width:{share:.3f}%"></span></span></td>'
                f'<td class="num">{v:,}{unit}</td><td class="num">{"" if lim is None else f"{lim:,}"}</td><td>{esc(C["sections"]["count"]["pass_words"] if ok else C["sections"]["count"]["fail_words"])}</td></tr>')
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if i in (2, 3) else ""}>{esc(c)}</th>' for i, c in enumerate(cols))
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{esc(caption)}; scrolls sideways"><table class="wt ct">'
            f'<caption>{esc(caption)}</caption><thead><tr>{hd}</tr></thead><tbody>{trs}</tbody></table></div>')


def spend_panel(G, P, held):
    S = C['sections']['spend']
    if not G['report']:
        return section('spend', pending(S['wait']), ('waiting', 'build'))
    W = G['report'].get('weight', {})
    pj = W.get('projection', {})
    mg = pj.get('map_geometry', {})
    cr = pj.get('chapter_14_rules', {}) or W.get('chapter_14_parts', {})
    ch14 = W.get('chapters', {}).get('14', {})
    stop = int(ch14.get('budget') or (pj.get('chapter_14_per_plate') or {}).get('stop') or 0)
    kit = int(W.get('parts', {}).get('chart kit', 0))
    with_kit = int(pj.get('chapter_14_with_kit', 0))
    budget = int(pj.get('budget') or W.get('budget_page') or 0)
    limit = int(W.get('limit') or LIMIT_PAGE)
    proj = int(pj.get('projected_bytes', 0))
    rows = [(S['rows']['ch14'], with_kit, stop),
            (S['rows']['ch14_only'], int(ch14.get('bytes', 0)), None),
            (S['rows']['kit'], kit, None),
            (S['rows']['geo'], int(mg.get('bytes', 0)), int(mg.get('allowance', 0)) or None),
            (S['rows']['rules'], int(cr.get('rules_and_opener', 0)), int(cr.get('allowance', 0)) or None),
            (S['rows']['page_now'], int(W.get('bytes', 0)), budget),
            (S['rows']['page'], proj, budget),
            (S['rows']['limit'], proj, limit)]
    diff = with_kit - stop
    FILL.update({'ch14_kit': f'{with_kit:,}', 'stop': f'{stop:,}', 'over_words': fill(S['over'] if diff > 0 else S['under'], {'n': f'{abs(diff):,}'}),
                 'proj': f'{proj:,}', 'budget_mb': f'{budget / 1e6:g}', 'proj_room': f'{budget - proj:,}', 'limit_room': f'{limit - proj:,}',
                 'page_now': f'{int(W.get("bytes", 0)):,}', 'build_when': B1.words_when(datetime.datetime.fromtimestamp(G['mtime'], datetime.timezone.utc)) if G.get('mtime') else ''})
    trs = ''
    # B3-S6: every bar on one scale that reaches the largest share, with its figure's line drawn where 100 percent falls
    top_share = max([100.0] + [100 * b / lim for _, b, lim in rows if lim])
    for name, b, lim in rows:
        share = 100 * b / lim if lim else None
        fig_at = 100 * 100 / top_share
        bar = (f'<span class="track"><span class="lim" style="left:{fig_at:.3f}%"></span><span class="bar" data-mark="bar" data-value="{share:.3f}" data-key="{esc(name)}" '
               f'style="width:{100 * share / top_share:.3f}%"></span></span><span class="pct">{share:.1f} percent</span>'
               if share is not None else f'<span class="pct">{esc(S["no_limit"])}</span>')
        trs += f'<tr><th scope="row">{esc(name)}</th><td class="barcell">{bar}</td><td class="num">{b:,}</td><td class="num">{"" if lim is None else f"{lim:,}"}</td></tr>'
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if i >= 2 else ""}>{esc(c)}</th>' for i, c in enumerate(S['cols']))
    body = (f'<p class="intro">{esc(fill(S["lede"]))}</p>'
            f'<figure class="wfig"><div class="tw" role="region" tabindex="0" aria-label="{esc(S["caption"])}; scrolls sideways"><table class="wt">'
            f'<caption>{esc(S["caption"])}</caption><thead><tr>{hd}</tr></thead><tbody>{trs}</tbody></table></div></figure>'
            f'<p>{esc(fill(S["page_line"]))}</p>')
    own, geo = int(ch14.get('bytes', 0)), int(mg.get('bytes', 0))
    if own + kit + geo == with_kit:
        body += f'<p class="small">{esc(fill(S["parts_line"], {"own": f"{own:,}", "kit": f"{kit:,}", "geo": f"{geo:,}"}))}</p>'
    else:
        warn(f'chapter 14 with the kit ({with_kit:,}) is not its entries, kit and map shapes added ({own + kit + geo:,}); the board says nothing of its parts')
    # round 5's plates
    r5 = pj.get('chapter_14_round_5') or {}
    if r5:
        rr = ''.join(f'<tr><th scope="row">{esc(S["r5_names"].get(k, k))}</th><td class="num">{int(v):,}</td></tr>' for k, v in r5.items())
        body += (f'<h3 class="sub">{esc(S["r5_h"])}</h3><div class="tw" role="region" tabindex="0" aria-label="{esc(S["r5_caption"])}; scrolls sideways">'
                 f'<table class="wt r5t"><caption>{esc(S["r5_caption"])}</caption><thead><tr><th scope="col">{esc(S["r5_cols"][0])}</th><th scope="col" class="n">{esc(S["r5_cols"][1])}</th></tr></thead><tbody>{rr}</tbody></table></div>')
    # the heaviest charts
    charts = W.get('charts', {})
    by_spec, form_name = {}, {}
    for f in P['forms']:
        if f.get('spec_id'):
            by_spec.setdefault(f['spec_id'].upper(), (f['rule'], f['form']))
        if f.get('form_id'):
            form_name.setdefault(f['form_id'], f['form'])
    # a kit chart that serves a rule outside the plan's forms (S96 on Rule 14.142): its rule from the chapter's plates, and
    # its form's name from the plan's form ids
    for rid, r in held.items():
        sp = ((r.get('correct') or {}).get('specimen') or '')
        if re.fullmatch(r's-14-s\d+', sp) and sp[5:].upper() not in by_spec:
            by_spec[sp[5:].upper()] = (rid, '')
    top = sorted(((int(v.get('bytes', 0)), k) for k, v in charts.items() if k.startswith('s-14-s')), reverse=True)[:int(S.get('heaviest_n', 10))]
    hrows = ''
    heavy = []
    for b, k in top:
        sid = k.replace('s-14-', '').upper()
        rule, form = by_spec.get(sid, ('', ''))
        form = form or form_name.get(charts[k].get('form', ''), charts[k].get('form', ''))
        heavy.append({'spec': sid, 'rule': rule, 'bytes': b})
        rl = f'<a href="{esc(rule_href(rule))}">{esc(rule)}</a>' if rule and rid_anchor(rule) in ANCHORS else esc(rule)
        hrows += f'<tr><th scope="row">{esc(sid)}</th><td>{rl}</td><td>{esc(form)}</td><td class="num">{b:,}</td></tr>'
    body += (f'<h3 class="sub">{esc(fill(S["heavy_h"], {"n": len(top)}))}</h3><div class="tw" role="region" tabindex="0" aria-label="{esc(S["heavy_caption"])}; scrolls sideways">'
             f'<table class="wt ht"><caption>{esc(S["heavy_caption"])}</caption><thead><tr>' + ''.join(f'<th scope="col"{" class=\"n\"" if i >= 3 else ""}>{esc(c)}</th>' for i, c in enumerate(S['heavy_cols']))
             + f'</tr></thead><tbody>{hrows}</tbody></table></div><p class="small">{esc(S["heavy_note"])}</p>')
    FIG['spend'] = {'rows': rows, 'round_5': r5, 'heaviest': heavy, 'ch14_with_kit_minus_figure': diff}
    return section('spend', body, 'ready' if G['ok'] else ('partial', 'build'))


# ------------------------------------------------------------------------------------------------------- panel 6
def count_panel():
    S = C['sections']['count']
    k = (D or {}).get('counts')
    if not k:
        return section('count', f'<p class="intro">{esc(S["lede"])}</p>' + pending(S['wait']), ('waiting', 'data_lead'))
    r9 = k.get('rule_01_9') or {}
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    lim = r9.get('limits', {})
    log_ = r9.get('generator_examples')
    facts = [(S['facts']['total'], f'{r9.get("total_examples", "?")}'), (S['facts']['recount'], f'{r9.get("recount", "?")}'),
             (S['facts']['log'], f'{log_}' + (', agrees row for row' if r9.get('agrees_with_generator_log') else '') if log_ is not None else '?'),
             (S['facts']['limits'], fill(S['limits_words'], {'d': lim.get('domain', '?'), 's': lim.get('state', '?')})),
             (S['facts']['atlas_wide'], f'{r9.get("atlas_wide", "?")}')]
    QUOTED.extend(b for _, b in facts)
    out.append('<dl class="facts">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in facts) + '</dl>')
    if r9.get('note'):
        n_ = move_codes(r9['note'])
        QUOTED.append(n_)
        out.append(f'<p>{esc(n_)}</p>')
    base = r9.get('total_examples', '?')
    for key, h in (('by_domain', S['domain_h']), ('by_state', S['state_h'])):
        rows = r9.get(key) or []
        if rows:
            name_k = 'domain' if key == 'by_domain' else 'state'
            out.append(f'<h3 class="sub">{esc(h)}</h3>')
            out.append(bar_rows([(str(x.get('title') or x.get(name_k, '')), int(x.get('count', 0)), x.get('limit'), bool(x.get('passes', True))) for x in rows], S['cols'],
                                fill(S['caption'], {'what': h.lower(), 'base': base})))
            QUOTED.extend(str(x.get('title') or x.get(name_k, '')) for x in rows)
    dr = k.get('dr_229') or {}
    if dr:
        out.append(f'<h3 class="sub">{esc(S["dr229_h"])}</h3>')
        if dr.get('test'):
            t_ = move_codes(dr['test'])
            QUOTED.append(t_)
            out.append(f'<p>{esc(t_)}</p>')
        if dr.get('count') is not None:
            out.append(f'<p class="big">{esc(fill(S["dr229_count"], {"n": dr["count"]}))}</p>')
        df = [(lab, dr[kk]) for kk, lab in S['dr229_facts'].items() if dr.get(kk) is not None]
        if df:
            out.append('<dl class="facts">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in df) + '</dl>')
        ex = dr.get('examples') or []
        if ex:
            cols = [c for c in S['dr229_cols'] if any(c in x for x in ex)]
            for x in ex:
                if x.get('passes') is False and re.search(S['not_applied_re'], str(x.get('test', '')), flags=re.I):
                    fail(f'the election table prints “No” for {x.get("where")}, whose test was not applied ({x.get("test")})')
            yn = lambda v: S['not_applied'] if v is None else ((S['pass_words'] if v else S['fail_words']) if isinstance(v, bool) else v)
            out.append(rows_table([{c: yn(x.get(c)) if c == 'passes' else x.get(c, '') for c in cols} for x in ex],
                                  fill(S['dr229_caption'], {'base': base, 'n': len(ex)})))
        if dr.get('note'):
            n_ = move_codes(dr['note'])
            QUOTED.append(n_)
            out.append(f'<p>{esc(n_)}</p>')
    FIG['count'] = {'total': r9.get('total_examples'), 'recount': r9.get('recount'), 'dr_229': dr.get('count')}
    st = 'ready' if (D or {}).get('state') == 'signed off' else ('partial', 'data_lead')
    refs = fill(S['script_ref'], {'script': k.get('script', '')}) if k.get('script') else ''
    refs = ' · '.join(x for x in [refs] + MOVED_REFS if x)
    MOVED_REFS.clear()
    return section('count', ''.join(out), st, refs)


# ------------------------------------------------------------------------------------------------------- panel 7
ID = r'[A-Z]{1,4}(?:[- ][A-Z]{1,3})?-?\d{1,3}'
PATH_RE = r'\b(?:work|source|deliverables|brief)/[\w./-]+|\b[\w-]+\.(?:json|md|py|mjs|js|csv|html)\b'


def findings(body):
    if body is None:
        return None
    b = body.strip()
    if not b or re.fullmatch(r'(?i)pending\.?', b):
        return None
    if re.fullmatch(r'(?i)none\.?|no must fix\.?|no should fix\.?', b):
        return 0
    ids = re.findall(r'^(?:#{2,6}\s+|[-*]\s+|\d+\.\s+)?\*\*(' + ID + r')(?:[.:)]|\*\*)', b, flags=re.M)
    ids += re.findall(r'^#{2,6}\s+(' + ID + r')[.:)\s]', b, flags=re.M)
    if ids:
        return len(dict.fromkeys(ids))
    n = len(re.findall(r'^\d+\.\s+\S', b, flags=re.M))
    return n if n else len(re.findall(r'^[-*]\s+\S', b, flags=re.M))


def score_in(part):
    """The first "N of 5" under a heading that names a score, the heading's own words included; a half point kept. Else
    a bold "Score: N of 5" line at the report's head."""
    for m in re.finditer(r'^(#+)\s*(?:\d+\.\s*)?(.*\bscore\b.*)$', part, flags=re.M | re.I):
        nxt = re.search(r'^#+\s', part[m.end():], flags=re.M)
        block = m.group(2) + '\n' + part[m.end():m.end() + (nxt.start() if nxt else len(part))]
        s = re.search(r'\b([1-5](?:\.\d)?)\s*(?:out\s+)?of\s+5\b|\b([1-5](?:\.\d)?)\s*/\s*5\b', block)
        if s:
            v = s.group(1) or s.group(2)
            return float(v) if '.' in v else int(v)
    s = re.search(r'\*\*Score:\s*([1-5](?:\.\d)?)\s*of\s*5', part)
    if s:
        v = s.group(1)
        return float(v) if '.' in v else int(v)
    return None


def reader_row(rd):
    t = read(rd['file'])
    if rd.get('cd_json'):
        p = ROOT / rd['cd_json']
        if not p.exists():
            return {'name': rd['name'], 'state': 'missing'}
        J = json.loads(p.read_text())
        items = J.get('items', [])
        ready = sum(1 for i in items if i.get('ready'))
        return {'name': rd['name'], 'state': 'ready', 'score': f'{ready} of {len(items)} items ready',
                'must_fix': sum(int(i.get('must_fix_count') or 0) for i in items), 'should_fix': sum(int(i.get('should_fix_count') or 0) for i in items),
                'file': rd['cd_json']}
    if t is None:
        return {'name': rd['name'], 'state': 'missing'}
    m = re.search(r'^##\s+(?:\d+\.\s*)?Second pass\b.*$', t, flags=re.M | re.I)
    first = t[:m.start()] if m else t
    score = score_in(first)
    mf = findings(B1.md_section(first, [r'(?:\d+\.\s*)?must fix']))
    sf = findings(B1.md_section(first, [r'(?:\d+\.\s*)?should fix']))
    state = 'ready' if score is not None and mf is not None and sf is not None else 'waiting'
    return {'name': rd['name'], 'state': state, 'score': f'{score} of 5' if score is not None else None, 'must_fix': mf, 'should_fix': sf, 'file': rd['file']}


def drop_ids(s):
    rid = r'[A-Z]{1,4}\d{0,3}(?:-[A-Z]{1,3})?-?\d{1,3}'
    return re.sub(r'\s*\((?:' + rid + r'(?:,\s*|\s+and\s+|;\s*)?)+\)', '', s or '')


def short_name(s):
    """An item's name as the scores print it: the words before its first colon or parenthesis."""
    return drop_ids(re.sub(r'\s*\(.*$', '', s or '')).strip()


def cd_table(first, rescore, caption):
    d = rescore or first
    crit = d.get('criteria') or first.get('criteria') or []
    items = d.get('items', [])
    f_items = {i['key']: i for i in (first or {}).get('items', [])}
    both = rescore is not None
    head = '<th scope="col">Item</th>' + ''.join(f'<th scope="col">{esc(c["name"])}</th>' for c in crit) + '<th scope="col">Ready</th>'
    rows = []
    for it in items:
        sc = it.get('scores', {})
        fs = (f_items.get(it.get('key'), {}) or {}).get('scores') or it.get('first_scores') or {}

        def cell(c):
            v = sc.get(c['key'], '')
            lo = isinstance(v, (int, float)) and v < 4
            if not both:
                return f'<td class="num sc{" lo" if lo else ""}">{esc(v)}</td>'
            w = fs.get(c['key'])
            wlo = isinstance(w, (int, float)) and w < 4
            moved = w is not None and w != v
            return (f'<td class="num sc{" mv" if moved else ""}"><span class="r1{" lo" if wlo else ""}">{esc(w) if w is not None else "new"}</span>'
                    f'<span class="r2{" lo" if lo else ""}">{esc(v)}</span></td>')
        nm = short_name(it.get('name', it.get('key')))
        QUOTED.append(nm)
        rows.append(f'<tr><th scope="row">{esc(nm)}</th>{"".join(cell(c) for c in crit)}<td>{"Yes" if it.get("ready") else "<b>Not yet</b>"}</td></tr>')
    first_ready = sum(1 for i in (first or {}).get('items', []) if i.get('ready'))
    now_ready = sum(1 for i in items if i.get('ready'))
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{esc(caption)}; scrolls sideways"><table class="scores"><caption>{esc(caption)}</caption>'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'), first_ready, now_ready, len(items)


def scores_panel():
    S = C['sections']['scores']
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    status = 'ready'
    rows = [reader_row(rd) for rd in C['slots']['readers']]
    trs = []
    for r in rows:
        if r['state'] != 'ready':
            trs.append(f'<tr><th scope="row">{esc(r["name"])}</th><td colspan="3">{esc(S["reader_wait"])}</td></tr>')
            status = ('partial', 'red')
            continue
        trs.append(f'<tr><th scope="row">{esc(r["name"])}</th><td class="num">{esc(r["score"])}</td><td class="num">{r["must_fix"]}</td><td class="num">{r["should_fix"]}</td></tr>')
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if i >= 1 else ""}>{esc(c)}</th>' for i, c in enumerate(S['readers_cols']))
    out.append(f'<h3 class="sub">{esc(S["readers_h"])}</h3><p>{esc(S["readers_lede"])}</p>'
               f'<div class="tw" role="region" tabindex="0" aria-label="{esc(S["readers_caption"])}; scrolls sideways"><table class="rt"><caption>{esc(S["readers_caption"])}</caption><thead><tr>{hd}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    # the creative director: first pass and rescore
    fp, rp, sp = ROOT / C['slots']['cd_first'], ROOT / C['slots']['cd_rescore'], ROOT / C['slots']['cd_second']
    first = json.loads(fp.read_text()) if fp.exists() else None
    rescore = json.loads(rp.read_text()) if rp.exists() else None
    summ = {}
    out.append(f'<h3 class="sub">{esc(S["cd_h"])}</h3><p class="small">{esc(S["legend"])}</p>')
    if first:
        tbl, fr, nr, n = cd_table(first, rescore, S['cd_caption'])
        out.append(f'<p>{esc(fill(S["cd_line"], {"first": nw(fr, "none"), "now": "all " + nw(nr) if nr == n else nw(nr, "none"), "n": nw(n)}))}</p>{tbl}')
        summ = {'first_ready': fr, 'rescore_ready': nr, 'items': n}
    else:
        out.append(pending(S['wait_cd']))
        status = ('partial', 'cd')
    out.append(f'<h3 class="sub">{esc(S["second_h"])}</h3><p>{esc(S["second_lede"])}</p>'
               + (f'<p class="small">{esc(S["second_legend"])}</p>' if S.get('second_legend') else ''))
    if sp.exists():
        try:
            SP = json.loads(sp.read_text())
            tbl, fr, nr, n = cd_table(rescore or first, SP, S['second_caption'])
            out.append(f'<p>{esc(fill(S["second_line"], {"now": nw(nr, "none"), "n": nw(n)}))}</p>{tbl}')
            summ.update({'second_ready': nr, 'second_items': n})
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            warn(f'{rel(sp)} could not be read: {e}')
            out.append(pending(S['second_wait']))
            status = status if status != 'ready' else ('partial', 'cd_second')
    else:
        out.append(pending(S['second_wait']))
        status = status if status != 'ready' else ('partial', 'cd_second')
    # the board's own score, when it lands
    bp = ROOT / C['slots']['board_scores']
    brp = ROOT / C['slots'].get('board_rescores', '-')
    out.append(f'<h3 class="sub">{esc(S["board_h"])}</h3>')
    if bp.exists():
        try:
            B = json.loads(bp.read_text())
            BR = json.loads(brp.read_text()) if brp.is_file() else None
            tbl, fr, nr, n = cd_table(B, BR, S['board_caption'])
            if n == 1:
                rw_ = lambda k: S['ready_word'] if k else S['not_ready_word']
                bl = fill(S['board_line_one'] if BR else S['board_line_one_first'], {'first': rw_(fr), 'now': rw_(nr)})
            else:
                bl = fill(S['board_line'] if BR else S['board_line_first'], {'first': nw(fr, 'none'), 'now': nw(nr, 'none'), 'n': nw(n)})
            out.append(f'<p>{esc(bl)}</p>')
            out.append(tbl)
            FIG['board_score'] = {'file': rel(bp), 'rescore': rel(brp) if BR else None, 'ready': nr, 'items': n}
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            warn(f'{rel(bp)} could not be read: {e}')
            out.append(pending(S['board_wait']))
            status = status if status != 'ready' else ('partial', 'cd_board')
    else:
        out.append(pending(S['board_wait']))
        status = status if status != 'ready' else ('partial', 'cd_board')
    FIG['scores'] = {'readers': rows, 'cd': summ}
    return section('scores', ''.join(out), status)


# ------------------------------------------------------------------------------------------------------- panel 8
def tested_panel(G):
    S = C['sections']['tested']
    rows, missing = [], []
    for it in S['tested']:
        kind, w = it.get('kind'), None
        if kind == 'build':
            rep = G['report']
            if rep:
                w = fill(it['words'], {'bytes': f'{rep.get("bytes", 0):,}', 'warnings': nw(len(rep.get('warnings', []))), 'rules': rep.get('rules'),
                                       'specimens': rep.get('specimens_placed'), 'when': B1.words_when(datetime.datetime.fromtimestamp(G['mtime'], datetime.timezone.utc)) if G.get('mtime') else ''})
        elif kind == 'check_file':
            p = scratch_path(C['slots'].get(it['slot']))
            if p and p.is_file():
                J = json.loads(p.read_text())
                runs = J.get('runs') if isinstance(J.get('runs'), list) else []
                widths = [str(r.get('width')) for r in runs if r.get('width')]
                r0 = runs[0] if runs else {}
                w = fill(it['words'], {'widths': join_words(widths) or '?', 'failures': nw(len(J.get('failures', []))),
                                       'specimens': f'{(r0.get("specimens") or {}).get("stages", 0):,}', 'links': f'{(r0.get("anchors") or {}).get("links", 0):,}'})
                FIG.setdefault('checks_read', {})[it['slot']] = {'file': rel(p), 'failures': J.get('failures'), 'pass': J.get('pass')}
        elif kind == 'v7':
            p = scratch_path(C['slots'].get(it['slot']))
            if p and p.is_file():
                J = json.loads(p.read_text())
                chs = J.get('chapters') or {}
                pg = J.get('page') or ''
                if PAGES.get('final', {}).get('path') and pg and not str(PAGES['final']['path']).endswith(pg):
                    warn(f'the atlas check read {pg}, and the board reads {rel(PAGES["final"]["path"])}')
                w = fill(it['words'], {'chips': f'{sum(int(v.get("chips", 0)) for v in chs.values()):,}', 'chapters': join_words(sorted(chs)),
                                       'specs': J.get('kit_specs', '?'), 'failures': nw(len(J.get('failures', [])))})
                FIG.setdefault('checks_read', {})[it['slot']] = {'file': rel(p), 'failures': J.get('failures')}
        elif kind == 'preview_links':
            if PREVIEW_IDS is not None:
                hit = sum(1 for a in LINKS if a in PREVIEW_IDS)
                w = fill(it['words'], {'links': f'{len(LINKS):,}', 'anchors': f'{len(set(LINKS)):,}', 'found': f'{hit:,}'})
                FIG['preview_links'] = {'links': len(LINKS), 'anchors': len(set(LINKS)), 'found': hit}
        elif kind == 'board_check':
            p = BOARD_DIR / f'{DATE}_Board-3-Check-Results.json'
            if p.exists():
                J = json.loads(p.read_text())
                fails = [f for f in J.get('failures', []) if 'html-has-lang' not in f]
                w = fill(it['words'], {'widths': join_words([str(r.get('width')) for r in J.get('runs', []) if r.get('width')]), 'failures': nw(len(fails))})
        else:
            parts = []
            for s in it.get('sources', []):
                sp = SCRATCH_ROOT / s['scratch_file'] if s.get('scratch_file') else None
                txt = (sp.read_text() if sp and sp.exists() else '') if sp else (read(s['file']) or '')
                ms = list(re.finditer(s['pattern'], txt))
                if ms:
                    g = ms[-1].groups()
                    parts.append(re.sub(r'\{(\d)\}', lambda m: g[int(m.group(1)) - 1], s['words']))
            w = '; '.join(parts) if parts and len(parts) == len(it.get('sources', [])) else None
        if w is None:
            missing.append(it.get('owner', 'notes'))
            w = S['wait_words']
        rows.append(f'<li><b>{esc(it["label"])}:</b> {esc(w if w.endswith(".") else w + ".")}</li>')
        FIG.setdefault('tested', {})[it['label']] = w
    FILL['n_links'] = f'{len(LINKS):,}'
    FILL['n_anchors'] = f'{len(set(LINKS)):,}'
    nots = ''.join(f'<li>{esc(fill(x))}</li>' for x in S['not_tested'])
    body = (f'<p class="intro">{esc(S["lede"])}</p><div class="tcols">'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["tested_h"])}</h3><ul>{"".join(rows)}</ul></div>'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["not_h"])}</h3><ul>{nots}</ul></div></div>')
    return section('tested', body, 'ready' if not missing else ('partial', missing[0]))


def next_panel():
    S = C['sections']['next']
    return section('next', f'<p class="intro">{esc(S["line"])}</p>', 'ready')


# ------------------------------------------------------------------------------------------------------- page
ORDER = ['decide', 'forms', 'round5', 'ch15', 'spend', 'count', 'scores', 'tested', 'next']


def panel_words(html_):
    """The words a reader meets in a panel with its folds closed: every <details> body left out, its summary kept."""
    t = re.sub(r'<details\b[^>]*>\s*(<summary>.*?</summary>).*?</details>', r'\1', html_, flags=re.S)
    t = re.sub(r'<p class="codes">.*?</p>', ' ', t, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9’'.,-]*", visible_text(t)))


def cover():
    K = C['cover']
    toc = ''.join(f'<li><a href="#p-{k}"><span class="n">{C["sections"][k]["n"]:02d}</span><span class="t">{esc(fill(C["sections"][k]["nav"]))}</span></a>'
                  f'{chip(STATUS[k], short=True)}</li>' for k in ORDER)
    ready = sum(1 for k in ORDER if STATUS[k] == 'ready')
    deck = ''.join(f'<p>{esc(fill(x))}</p>' for x in K['deck'])
    return (f'<header class="cover"><div class="mast"><b>OATH &amp; ACTION</b><span class="label">{esc(K["kicker"])}</span></div>'
            f'<p class="label for">{esc(fill(K["for_line"]))}</p><h1>{esc(K["title"])}</h1>'
            f'<div class="cover-grid"><div class="deck">{deck}<p class="caption">{esc(fill(K["minutes"]))}</p></div>'
            f'<nav class="toc" aria-labelledby="toc-h"><p class="label" id="toc-h">{esc(K["toc_h"])} · {ready} of {len(ORDER)} ready</p><ol>{toc}</ol></nav></div></header>')


CSS = r'''
:root{color-scheme:light;
--np:var(--oa-color-surface-newsprint);--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);--charcoal:var(--oa-color-palette-charcoal);
--white:var(--oa-color-surface-white);--wink:var(--oa-color-text-primary-on-white);--wink-2:var(--oa-color-text-secondary-on-white);
--whair:var(--oa-color-border-hairline-on-white);--wstrong:var(--oa-color-border-strong-on-white);--tint:var(--oa-color-tint-stone-n88);
--head-fill:var(--oa-color-tint-white-n55);--focus:var(--oa-color-focus-ring-on-newsprint);--focus-w:var(--oa-color-focus-ring-on-white)}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--np)}
body{margin:0;background:var(--np);color:var(--ink);font:var(--oa-type-body);-webkit-font-smoothing:antialiased}
.page{background:var(--np);color:var(--ink);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 var(--oa-space-1300);overflow-wrap:break-word}
.inner{max-width:82rem;margin:0 auto}
a{color:inherit;text-decoration-thickness:var(--oa-border-width-underline);text-underline-offset:.2em}
:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--focus);outline-offset:var(--oa-border-focus-offset)}
.tw:focus-visible{outline-color:var(--focus-w)}
p{margin:0 0 var(--oa-space-150);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
h1,h2,h3,h4{margin:0}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0}
.caption,.small{font:var(--oa-type-caption);color:var(--ink-2)}
.small{max-width:var(--oa-layout-measure-intro-max)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max);margin-bottom:var(--oa-space-300)}
.codes{font:var(--oa-type-caption);color:var(--ink-2);margin:var(--oa-space-300) 0 0;max-width:none}
code{font-size:max(.9em,13px);overflow-wrap:anywhere}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.for{margin-top:var(--oa-space-800)}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-500);max-width:15ch;text-wrap:balance}
.cover-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500) var(--oa-space-800);align-items:start}
@media (min-width:64em){.cover-grid{grid-template-columns:minmax(0,6fr) minmax(0,5fr)}}
.deck p:not(.caption){font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.toc{border-top:var(--oa-border-width-rule) solid var(--strong)}
.toc .label{padding:var(--oa-space-150) 0 var(--oa-space-100)}
.toc ol,.fidx ol,.dtoc ol{list-style:none;margin:0;padding:0}
.toc li{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-050) var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-050) 0}
.toc a{display:inline-flex;gap:var(--oa-space-150);min-height:2.75rem;align-items:center;text-decoration:none;font:var(--oa-type-ui);font-weight:600}
.toc a:hover .t{text-decoration:underline}
.toc .n{font-variant-numeric:tabular-nums;color:var(--ink-2);font-weight:400;min-width:1.6em}
.st{font:var(--oa-type-caption);font-weight:600;padding:0 .5em;max-width:100%;border:var(--oa-border-width-hairline) solid var(--strong);line-height:1.6}
.st.ready{background:var(--charcoal);color:var(--np);border-color:var(--charcoal)}
.st.waiting,.st.partial{background:transparent;color:var(--ink)}
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-300)}
.sec-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-100) var(--oa-space-300)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:var(--oa-space-150) 0 var(--oa-space-400);text-wrap:balance;max-width:20ch}
.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:var(--oa-space-800) 0 var(--oa-space-200);text-wrap:balance;max-width:40ch}
.sub.grp{border-top:var(--oa-border-width-bar) solid var(--charcoal);padding-top:var(--oa-space-200)}
.sub.fam{margin-top:var(--oa-space-1000)}
.facts{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-500);margin:var(--oa-space-200) 0 var(--oa-space-300);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:64em){.facts{grid-template-columns:repeat(3,minmax(0,1fr))}.facts.f2{grid-template-columns:repeat(2,minmax(0,1fr))}}
.facts div{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.facts dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2)}
.facts dd{margin:var(--oa-space-050) 0 0;font:var(--oa-type-body-small)}
.tag{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--strong);padding:2px 6px;white-space:nowrap;vertical-align:.2em}
.tag.rec,.tag.q{background:var(--charcoal);color:var(--np);border-color:var(--charcoal)}
.tag.av{background:transparent;color:var(--ink);border-width:var(--oa-border-width-rule)}
.dtoc ol{display:grid;grid-template-columns:minmax(0,1fr);border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:var(--oa-layout-measure-intro-max)}
.dtoc li{display:flex;justify-content:space-between;gap:var(--oa-space-200);border-bottom:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-050) 0}
.dtoc a{font:var(--oa-type-ui);font-weight:600;text-decoration:none;min-height:2.75rem;display:inline-flex;align-items:center}
.dtoc a:hover{text-decoration:underline}
.dtoc .n{font:var(--oa-type-caption);color:var(--ink-2);font-variant-numeric:tabular-nums;align-self:center}
.approve{font:var(--oa-type-ui);font-weight:600;border-left:var(--oa-border-width-bar) solid var(--charcoal);padding-left:var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.dec{margin-top:var(--oa-space-600);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-200)}
.dec-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-050) 0 var(--oa-space-150);max-width:var(--oa-layout-measure-intro-max);text-wrap:balance}
.dec-a{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.dec-q{font-weight:600;max-width:var(--oa-layout-measure-intro-max)}
.dec-rec{font-weight:600;max-width:var(--oa-layout-measure-intro-max);border-left:var(--oa-border-width-bar) solid var(--charcoal);padding-left:var(--oa-space-200)}
.dec-rec .tag{margin-right:var(--oa-space-050)}
blockquote.q{margin:var(--oa-space-150) 0;padding:var(--oa-space-150) 0 var(--oa-space-150) var(--oa-space-300);border-left:var(--oa-border-width-rule) solid var(--strong);max-width:var(--oa-layout-measure-intro-max)}
blockquote.q p{margin:0 0 var(--oa-space-100)}
blockquote.q footer{font:var(--oa-type-caption);color:var(--ink-2)}
.oldnew{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200) var(--oa-space-500);margin:var(--oa-space-200) 0}
@media (min-width:48em){.oldnew{grid-template-columns:repeat(2,minmax(0,1fr))}}
.oldnew p.was,.oldnew p.now{font:var(--oa-type-body-small);padding:var(--oa-space-150) var(--oa-space-200);border:var(--oa-border-width-hairline) solid var(--strong);margin:0}
.oldnew p.now{border-width:var(--oa-border-width-rule)}
.reply{font:var(--oa-type-ui);font-weight:700;margin-top:var(--oa-space-600);padding:var(--oa-space-200) var(--oa-space-300);border:var(--oa-border-width-rule) solid var(--charcoal);max-width:var(--oa-layout-measure-intro-max)}
.fidx{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-400);margin:var(--oa-space-300) 0;border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.fidx{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:80em){.fidx{grid-template-columns:repeat(3,minmax(0,1fr))}}
.fam-i{padding:var(--oa-space-100) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair);min-width:0}
.fam-n{font:var(--oa-type-ui);font-weight:600;margin:0 0 var(--oa-space-050)}
.fam-n a{text-decoration:none}.fam-n a:hover{text-decoration:underline}
.fidx ol{display:flex;flex-wrap:wrap;gap:var(--oa-space-050)}
.fidx li a{display:inline-flex;align-items:center;justify-content:center;min-width:3.5rem;min-height:2.75rem;padding:0 .4em;border:var(--oa-border-width-hairline) solid var(--strong);text-decoration:none;font:var(--oa-type-caption);font-weight:600;font-variant-numeric:tabular-nums}
.fidx li a.sk{border-style:dashed}
.form{margin-top:var(--oa-space-800);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-200)}
.f-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-050) var(--oa-space-300)}
.live{font:var(--oa-type-caption);font-weight:600;display:inline-flex;align-items:center;min-height:2.75rem}
.f-t{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:var(--oa-space-050) 0 var(--oa-space-150);text-wrap:balance;max-width:var(--oa-layout-measure-intro-max)}
.f-t .tag{margin-left:var(--oa-space-100)}
.f-q,.f-rt{font:var(--oa-type-body-small);max-width:var(--oa-layout-measure-intro-max);margin-bottom:var(--oa-space-150)}
.f-q .k{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin-right:var(--oa-space-100)}
.f-ev{margin:var(--oa-space-200) 0 var(--oa-space-100)}
.ev-k{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;padding:2px 6px;border:var(--oa-border-width-hairline) solid var(--strong)}
.ev-k.est{background:var(--charcoal);color:var(--np);border-color:var(--charcoal)}
.f-ct{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-100) 0 0;max-width:var(--oa-layout-measure-intro-max);text-wrap:pretty}
.row-label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:var(--oa-space-300) 0 var(--oa-space-100)}
.ch-line{font:var(--oa-type-body-small);margin-top:var(--oa-space-150);font-variant-numeric:tabular-nums}
.src{font:var(--oa-type-caption);color:var(--ink-2);max-width:var(--oa-layout-measure-intro-max);margin-top:var(--oa-space-200)}
.what{font:var(--oa-type-body-small);border-left:var(--oa-border-width-bar) solid var(--charcoal);padding-left:var(--oa-space-200);margin:var(--oa-space-150) 0 var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.faults{font:var(--oa-type-body-small);max-width:var(--oa-layout-measure-intro-max)}
.shot figcaption .chip{font-weight:600;color:var(--ink);padding:0 .4em;border:var(--oa-border-width-hairline) solid var(--strong)}
.rule{margin-top:var(--oa-space-500);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-200)}
.r-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);max-width:var(--oa-layout-measure-intro-max);text-wrap:balance;margin-bottom:var(--oa-space-150)}
.r-h .rid{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:0 var(--oa-space-300);font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin-bottom:var(--oa-space-050)}
.r-h .rid .live{text-transform:none;letter-spacing:0;color:var(--ink)}
.shot{margin:var(--oa-space-200) 0 var(--oa-space-300);min-width:0;max-width:100%;display:flex;flex-direction:column;gap:var(--oa-space-100)}
.shot figcaption{font:var(--oa-type-caption);color:var(--ink-2);max-width:var(--oa-layout-measure-intro-max)}
.shot figcaption b{color:var(--ink);font-weight:600}
.shot figcaption.top{font:var(--oa-type-body-small);color:var(--ink)}
.role{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;padding:1px 6px;margin-right:var(--oa-space-050);border:var(--oa-border-width-hairline) solid var(--strong)}
.role.after{background:var(--charcoal);color:var(--np);border-color:var(--charcoal)}
.pair.ba{border-top:var(--oa-border-width-hairline) solid var(--hair);margin-top:var(--oa-space-200)}
.rep-h{margin-top:var(--oa-space-300)}
ol.replies{list-style:none;margin:0 0 var(--oa-space-300);padding:0;border-top:var(--oa-border-width-rule) solid var(--strong);max-width:var(--oa-layout-measure-intro-max)}
ol.replies li{border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
ol.replies a{display:flex;gap:var(--oa-space-200);align-items:baseline;padding:var(--oa-space-150) 0;text-decoration:none;min-height:2.75rem}
ol.replies a:hover .rl{text-decoration:underline}
ol.replies .rn{flex:0 0 auto;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;background:var(--charcoal);color:var(--np);padding:2px 6px;white-space:nowrap}
ol.replies .rb{display:flex;flex-direction:column;gap:var(--oa-space-050)}
ol.replies .rl{font:var(--oa-type-ui);font-weight:600}
ol.replies .rr{font:var(--oa-type-body-small)}
ol.replies .rr .k{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin-right:var(--oa-space-100)}
.tag.rn{background:transparent;color:var(--ink);border-width:var(--oa-border-width-rule)}
.tag.done{background:var(--charcoal);color:var(--np);border-color:var(--charcoal)}
details.done-g{margin-top:var(--oa-space-1000);border-top:var(--oa-border-width-bar) solid var(--charcoal)}
details.done-g>summary{cursor:pointer;display:flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-100) var(--oa-space-200);min-height:2.75rem;padding:var(--oa-space-200) 0;font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing)}
details.done-g>summary .n{font:var(--oa-type-caption);color:var(--ink-2)}
.dec-done{font-weight:600;max-width:var(--oa-layout-measure-intro-max)}
details.pics{margin-top:var(--oa-space-300)}
.dec>.small>a{display:inline-flex;align-items:center;min-height:2.75rem}
details.pics{margin-bottom:var(--oa-space-200)}
.measure{font:var(--oa-type-ui);font-weight:600;border-left:var(--oa-border-width-bar) solid var(--charcoal);padding-left:var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.narrow-hint{display:none;font:var(--oa-type-caption);color:var(--ink-2);margin:0 0 var(--oa-space-100)}
@media (max-width:47.49em){.narrow-hint{display:block}.frame.dp{direction:rtl}}
.frame{max-width:100%;line-height:0;overflow-x:auto;overscroll-behavior-x:contain;align-self:flex-start}
.frame img{display:block;max-width:none;height:auto}
.pair{display:flex;flex-wrap:wrap;gap:0 var(--oa-space-400);align-items:flex-start}
.pair .shot{flex:0 1 auto}
.pending{border:var(--oa-border-width-hairline) solid var(--strong);border-left:var(--oa-border-width-bar) solid var(--charcoal);padding:var(--oa-space-200) var(--oa-space-300);margin:var(--oa-space-200) 0;max-width:var(--oa-layout-measure-intro-max)}
.pending p{margin:0}
.tw{position:relative;overflow-x:auto;background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);margin:var(--oa-space-200) 0 var(--oa-space-100)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
caption{caption-side:top;text-align:left;padding:var(--oa-space-150) var(--oa-space-200);font:var(--oa-type-body-small);color:var(--wink-2);border-bottom:var(--oa-border-width-hairline) solid var(--whair)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-100) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--tint)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--head-fill);vertical-align:bottom}
tbody th{font:var(--oa-type-body-small);font-weight:600;color:var(--wink)}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
table.ft td:not(.t),table.ft th[scope=col]:not(.t){text-align:right;font-variant-numeric:tabular-nums}
table.ft{min-width:24rem}table.ft.rc{min-width:56rem}table.ft.rc td,table.ft.rc th{text-align:left!important}
.wt td.num,.rt td.num,.ft2 td.num,.ht td.num{text-align:right}
th.n{text-align:right}
table.scores{min-width:44rem}table.rt{min-width:36rem}table.wt{min-width:40rem}table.dt{min-width:36rem}
td.sc.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong);font-weight:700}
td.sc .r1{display:inline-block;min-width:1.4em;font:var(--oa-type-caption);color:var(--wink-2);margin-right:.35em;padding:0 .2em}
td.sc .r2{display:inline-block;min-width:1.6em;font-weight:700;padding:0 .2em}
td.sc .lo{box-shadow:inset 0 0 0 var(--oa-border-width-hairline) var(--wstrong)}
td.sc .r2.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong)}
td.sc.mv .r2{background:var(--tint)}
.wfig{margin:0}
.wt th[scope=row]{width:18rem}
.barcell{width:45%;min-width:12rem}
.bar{display:block;height:1.25rem;background:var(--charcoal)}
.track{position:relative;display:block}
.lim{position:absolute;top:-4px;bottom:-4px;width:0;border-left:var(--oa-border-width-rule) dashed var(--wstrong)}
.pct{display:block;font:var(--oa-type-caption);color:var(--wink-2);margin-top:var(--oa-space-050);font-variant-numeric:tabular-nums}
.big{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing)}
.tcols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-500);margin-top:var(--oa-space-400)}
@media (min-width:64em){.tcols{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tcol{border-top:var(--oa-border-width-bar) solid var(--charcoal);padding-top:var(--oa-space-150);min-width:0}
.tcol-h{font:var(--oa-type-h4);margin-bottom:var(--oa-space-150)}
.tcol ul{margin:var(--oa-space-050) 0 var(--oa-space-200);padding-left:1.2em;font:var(--oa-type-body-small)}
.tcol li{margin-bottom:var(--oa-space-100);overflow-wrap:anywhere}
details.more{margin-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
details.more>summary{cursor:pointer;font:var(--oa-type-ui);font-weight:600;min-height:2.75rem;display:flex;align-items:center;gap:var(--oa-space-100)}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:none}
@media print{.toc,.fidx{display:none}details{display:block}}
'''


def strip_css(t):
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'/\*.*?\*/', '', t, flags=re.S)).strip()


def token_root(css):
    """The tokens.css :root definitions the page's styles name, and the ones they name in turn, in the file's order."""
    t = (ROOT / C['slots']['tokens_css']).read_text()
    m = re.search(r'(?m)^:root\s*\{(.*?)^\}', t, flags=re.S)
    need(m, 'tokens.css has no :root block')
    defs, order = {}, []
    for name, val in re.findall(r'(--oa-[a-z0-9-]+):\s*([^;]+);', m.group(1)):
        if name not in defs:
            defs[name] = val.strip()
            order.append(name)
    want, todo = set(), set(re.findall(r'var\((--oa-[a-z0-9-]+)\)', css))
    while todo:
        n = todo.pop()
        if n in want:
            continue
        if n not in defs:
            warn(f'the page names {n}, which tokens.css’s :root does not define')
            continue
        want.add(n)
        todo |= set(re.findall(r'var\((--oa-[a-z0-9-]+)\)', defs[n])) - want
    FIG['tokens_used'] = len(want)
    return ':root{' + ';'.join(f'{n}:{defs[n]}' for n in order if n in want) + '}'


FONTS = 'https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap'


def build_page(body):
    css = strip_css(CSS)
    return (f'<title>{esc(C["title"])}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="chart-views" content="overview">\n'
            f'<style>@import url("{FONTS}");\n{token_root(css)}\n{css}</style>\n'
            f'<div class="page" data-view-root="overview"><main class="inner">\n{body}\n<p class="foot caption">{esc(fill(C["foot"]))}</p>\n</main></div>\n')


def visible_text(page):
    t = re.sub(r'<(script|style|title)\b.*?</\1>', '', page, flags=re.S)
    t = re.sub(r'</?(?:p|li|ul|ol|h\d|td|th|tr|div|figure|figcaption|caption|blockquote|section|header|nav|main|table|thead|tbody|summary|details|dt|dd|dl|article|span|footer)\b[^>]*>|<br\s*/?>', ' ', t)
    return html.unescape(re.sub(r'<[^>]+>', '', t))


def checks(page):
    text = visible_text(page)
    alts = ' '.join(html.unescape(a) for a in re.findall(r'(?:alt|aria-label)="([^"]*)"', page))
    for ch, name in (('—', 'an em dash'),):
        for where, t in (('text', text), ('alt text', alts)):
            i = t.find(ch)
            if i >= 0:
                warn(f'{name} in the board’s {where}: ' + t[max(0, i - 60):i + 20])
    own_page = re.sub(r'<div class="tw"[^>]*><table class="ft[^"]*">.*?</table></div>', ' ', page, flags=re.S)
    for q in sorted({q for q in QUOTED if q}, key=len, reverse=True):
        for frag in (B1.md_inline(q), B1.md_inline(q, quote=False), esc(q)):
            own_page = own_page.replace(frag, ' ')
    own = visible_text(own_page)
    B1.MOVED.clear()
    if '–' in own:
        i = own.find('–')
        warn('an en dash in the board’s own words: ' + own[max(0, i - 40):i + 20])
    for leftover in re.findall(r'\{[a-z0-9_]+\}', own):
        warn(f'an unfilled field on the board: {leftover}')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', own, flags=re.I)})
    if flagged:
        warn('flagged words in the board’s own words: ' + ', '.join(flagged))
    face = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', own_page, flags=re.S))
    stray = set(re.findall(r'\b' + CODE_DEC + r'\b', face))
    if stray:
        warn('decision codes on the board’s face: ' + ', '.join(sorted(stray)))
    face_all = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))
    quoted_codes = set(re.findall(r'\b' + CODE_DEC + r'\b', face_all)) - stray
    if quoted_codes:
        warn('decision codes in the words the board quotes from teammates’ files, on its face: ' + ', '.join(sorted(quoted_codes)))
    paths = sorted(set(re.findall(PATH_RE, face_all)))
    if paths:
        warn('file paths on the board’s face, which belong in reference lines: ' + ', '.join(paths[:8]) + (f' and {len(paths) - 8} more' if len(paths) > 8 else ''))
    for pat in (r'/home/', r'file://', r'scratchpad', r'/tmp/', r'@anthropic'):
        if re.search(pat, page):
            warn(f'a private path on the board ({pat})')
    if re.search(r'<script\b', page, flags=re.I):
        warn('a script on the board')
    for bad in (r'<!doctype', r'<html\b', r'<head\b', r'<body\b'):
        if re.search(bad, page, flags=re.I):
            warn(f'the board carries {bad.strip(chr(92) + "b")}, which the host adds itself')
    hosts = set(re.findall(r'(?:src|url\()\s*"?https?://([^/"\s)]+)', page))
    hosts |= {h for h in re.findall(r'<link[^>]+href="https?://([^/"]+)', page)}
    extra = hosts - {'fonts.googleapis.com', 'fonts.gstatic.com'}
    if extra:
        warn('loads from hosts other than Google Fonts: ' + ', '.join(sorted(extra)))
    links = set(re.findall(r'<a [^>]*href="https?://([^/"]+)', page))
    if links - {'claude.ai'}:
        warn('links to hosts other than the guide preview: ' + ', '.join(sorted(links - {'claude.ai'})))
    if '@media (prefers-color-scheme' in page:
        warn('the board carries a dark-mode block')
    for v, u in re.findall(r'font-size:\s*(\d*\.?\d+)(px|rem)', strip_css(CSS)):
        if float(v) * (16 if u == 'rem' else 1) < 13:
            warn(f'a font size of {v}{u} in the board CSS, under 13 px')
    lit = re.findall(r'#[0-9a-fA-F]{3,8}\b|rgba?\(', strip_css(CSS))
    if lit:
        warn('a color in the board CSS that is not a token: ' + ', '.join(lit[:5]))
    for m in re.finditer(r'<img\b[^>]*>', page):
        tag = m.group(0)
        if not re.search(r'alt="[^"]{12,}"', tag):
            warn('an image without alt text that says what it shows: ' + tag[:120])
        if not (re.search(r'\swidth="\d+"', tag) and re.search(r'\sheight="\d+"', tag) and 'loading="lazy"' in tag):
            warn('an image without its width, height or loading="lazy": ' + tag[:120])
    return text


def run_checks(out, page):
    """dataviz_check.js --board on the page, then on a copy wrapped as the host wraps it."""
    def check(path):
        r = subprocess.run(['node', str(SCRIPTS2 / 'dataviz_check.js'), str(path), '--board', '--no-captures'], cwd=ROOT / 'work/build',
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        res = pathlib.Path(path).with_name(pathlib.Path(path).stem + '-Check-Results.json')
        J = json.loads(res.read_text()) if res.exists() else {}
        (SCRATCH / f'check-{pathlib.Path(path).parent.name}.log').write_text(r.stdout + r.stderr)
        return r, J
    if not browser_gate('the board check'):
        warn('the board check did not run: no browser could open')
        return False
    r1, J1 = check(out)
    fails1 = J1.get('failures', ['no results file'])
    other = [f for f in fails1 if not re.search(r'axe html-has-lang', f)]
    wrap_dir = SCRATCH / 'publish-view'
    wrap_dir.mkdir(parents=True, exist_ok=True)
    link = wrap_dir / 'img'
    if link.is_symlink() or link.exists():
        link.unlink() if link.is_symlink() else shutil.rmtree(link)
    link.symlink_to(IMG, target_is_directory=True)
    wrapped = wrap_dir / out.name
    wrapped.write_text('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head>\n<body>\n' + page + '</body></html>\n')
    if not browser_gate('the wrapped board check'):
        warn('the wrapped board check did not run: no browser could open')
        return False
    r2, J2 = check(wrapped)
    fails2 = J2.get('failures', ['no results file'])
    print('the board itself: ' + ('PASS' if not fails1 else f'{len(fails1)} failures: ' + '; '.join(fails1[:6])))
    print('the board as the host wraps it: ' + ('PASS' if not fails2 else f'{len(fails2)} failures: ' + '; '.join(fails2[:6])))
    FIG['check'] = {'page': {'failures': fails1, 'allowed': [f for f in fails1 if f not in other], 'results': rel(out.with_name(out.stem + '-Check-Results.json'))},
                    'wrapped': {'failures': fails2, 'pass': J2.get('pass'), 'results': '[scratch]/c08/board-3/builder/publish-view/' + wrapped.stem + '-Check-Results.json'},
                    'widths': [x.get('width') for x in J2.get('runs', [])]}
    if other:
        warn('the board check failed: ' + '; '.join(other[:6]))
    if fails2:
        warn('the wrapped board check failed: ' + '; '.join(fails2[:6]))
    return not other and not fails2


DECISIONS_PATH = None


def main():
    global C, D, LOG, SCRATCH, CACHE, DECISIONS_PATH, NO_BROWSER, PREVIEW_IDS, CHARCOAL
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--reuse', action='store_true', help='keep kit captures and photographs whose sources have not changed')
    ap.add_argument('--check', action='store_true', help='run dataviz_check.js --board on the board and on a wrapped copy')
    ap.add_argument('--strict', action='store_true', help='exit 1 on any warning')
    ap.add_argument('--scratch', type=pathlib.Path, default=SCRATCH_DEFAULT)
    ap.add_argument('--out', type=pathlib.Path, default=OUT)
    ap.add_argument('--decisions', type=pathlib.Path, help='read the decisions from this file, for a test only')
    ap.add_argument('--final', type=pathlib.Path, help='the final build’s page (else the content file’s slots.final_page)')
    ap.add_argument('--final-report', type=pathlib.Path, help='its build report (else slots.final_report, else beside the page)')
    ap.add_argument('--no-browser', action='store_true', help='open no browser: build from the captures already in scratch')
    a = ap.parse_args()
    NO_BROWSER = a.no_browser
    SCRATCH = a.scratch
    SCRATCH.mkdir(parents=True, exist_ok=True)
    os.environ['TMPDIR'] = str(SCRATCH)
    raw = CONTENT.read_text()
    if '—' in raw:
        warn('the content file holds an em dash')
    C = json.loads(raw)
    DECISIONS_PATH = a.decisions or (ROOT / C['slots']['decisions'])
    if a.decisions:
        warn(f'the decisions come from {rel(a.decisions)}, a test file; never a board to publish')
    if a.final:
        NOTES.append(f'the final build named on the command line: {rel(a.final)}')
    LOG = B1.read_log()
    IMG.mkdir(parents=True, exist_ok=True)
    cache_file = SCRATCH / 'compose-cache.json'
    CACHE = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL['built_date'] = B1.words_when(built)
    FIG['built'] = built.isoformat()
    t0 = datetime.datetime.now()
    D = decisions()
    G = load_pages(a.final.resolve() if a.final else None, a.final_report.resolve() if a.final_report else None)
    if G['usable']:
        PREVIEW_IDS = set(re.findall(r'\sid="([^"]+)"', G['text']))
    P, rn = plan()
    ch, held = chapter14()
    ch15, held15 = chapter15()
    FILL['n_15'] = len(held15)
    specs = sorted({f['spec_id'] for f in rn if f.get('spec_id')}, key=lambda s: int(s[1:]))
    m = re.search(r'--oa-color-palette-charcoal:\s*#([0-9A-Fa-f]{6})', (ROOT / C['slots']['tokens_css']).read_text())
    need(m, 'tokens.css names no Charcoal')
    CHARCOAL = tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
    for f in rn:
        if f.get('spec_id') and f['spec_id'] not in SPECINFO:
            sj = json.loads((ROOT / C['slots']['specs_dir'] / f'{f["spec_id"].lower()}.json').read_text())
            SPECINFO[f['spec_id']] = {'form': f['form'], 'title': sj.get('title', ''), 'rule': f['rule']}
    # 1. what to photograph, in the brief's priority order: panel 1's pictures, the forms' measures and sketches, round 5,
    #    chapter 15. One list per page, so each page loads once a window.
    items = []
    for it, pic in all_pictures(D):
        req = pic_request(it, pic)
        PIC_KEYS[id(pic)] = req
        if req and req['kind'] == 'guide':
            items.append({k: req[k] for k in ('key', 'page', 'el', 'w', 'text_scale', 'recipe', 'session', 'until_text') if k in req})
    for sid in specs:
        items += [{'key': f'm-{sid}-{w}', 'page': 'final', 'el': f'oac-s-14-{sid.lower()}', 'w': w, 'measure': True} for w in (DESK, PHONE)]
    for f in rn:
        if f['status'] == 'sketch':
            sp = f.get('sketch_id') or (held.get(f['rule'], {}).get('correct') or {}).get('specimen')
            items.append({'key': f'sketch-{f["rule"]}', 'page': 'final', 'el': f'fig-{sp}', 'w': DESK})
    items += r5_items(held)
    items += c15_items(held15)
    items += crop_items()
    seen, uniq = set(), []
    for x in items:
        if x['key'] not in seen:
            seen.add(x['key'])
            uniq.append(x)
    FIG['photographs_asked'] = len(uniq)
    shots = run_shots(uniq, a.reuse) if G['usable'] or any(x['page'] != 'final' for x in uniq) else {}
    make_pictures(a.reuse)
    for it, pic in all_pictures(D):
        if pic.get('kind') == 'to-make':
            PIC_KEYS[id(pic)] = pic_request(it, pic)
    # 2. the kit, at the window widths that give the guide's drawing widths: its own 1440 px where the guide draws the chart
    #    at 720 px (the reading width), else the window that gives the guide's width (the kit's gutter is 32 px a side
    #    from 600 px, 16 under it)
    pages, groups, measured = {}, {}, {}
    for sid in specs:
        mw = {}
        for w in (DESK, PHONE):
            p = shots.get(f'm-{sid}-{w}')
            # a form drawn in HTML has no svg.oac-svg: its figure's own width stands in (S90 to S92's cards)
            mj = json.loads(p.read_text()) if p and p.exists() else {}
            mw[w] = mj.get('svg_w') or (round(float(mj['el_w'])) if mj.get('el_w') else None)
        measured[sid] = mw
        MEAS[sid] = {w: (json.loads(shots[f'm-{sid}-{w}'].read_text()) if shots.get(f'm-{sid}-{w}') and shots[f'm-{sid}-{w}'].exists() else {}) for w in (DESK, PHONE)}
        if not (mw[DESK] and mw[PHONE]):
            continue
        dp = DESK if int(mw[DESK]) <= 720 else int(mw[DESK]) + 64
        pw = int(mw[PHONE]) + 32
        pages[sid] = (dp, pw)
        groups.setdefault((dp, pw), []).append(sid)
    FIG['guide_widths'] = measured
    kit_out = kit_build(groups, a.reuse) if groups else SCRATCH / 'kit-out'
    for sid in pages:
        chk = kit_out / sid.lower() / f'{sid.lower()}-check.json'
        if chk.exists():
            dw = {(x['ground'], x['page']): x['width'] for x in json.loads(chk.read_text()).get('drawings', [])}
            for w, pw in ((DESK, pages[sid][0]), (PHONE, pages[sid][1])):
                if measured[sid][w] and dw.get(('newsprint', pw)) and int(dw[('newsprint', pw)]) != int(measured[sid][w]):
                    warn(f'{sid}: the guide draws {measured[sid][w]} px at a {w} px window and the kit {dw[("newsprint", pw)]} px at {pw}')
    # 3. the panels: the forms first, so panel 1 could show their pictures; the tested panel last of all
    s_forms = forms_panel(G, P, rn, held, kit_out, pages, shots)
    s_decide = decide_panel(shots)
    w1 = panel_words(s_decide)
    FILL.update({'p1_words': f'{w1:,}', 'p1_min': max(1, round(w1 / 200))})
    FIG['panel_1_words'] = w1
    others = [round5_panel(G, held, shots), ch15_panel(G, ch15, held15, shots), spend_panel(G, P, held), count_panel(), scores_panel()]
    parts = [s_decide, s_forms] + others + [tested_panel(G), next_panel()]
    cache_file.write_text(json.dumps(CACHE))
    keep = set(IMAGES)
    for p in [q for q in IMG.iterdir() if q.suffix.lower() in IMG_EXT]:
        if p.name not in keep:
            p.unlink()
            NOTES.append(f'removed {p.name}, which the board no longer shows')
    page = build_page(cover() + '\n' + '\n'.join(parts))
    checks(page)
    need(len(page.encode()) < LIMIT_PAGE, 'the board is over 16 MB')
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    imgs = sorted(q for q in IMG.iterdir() if q.suffix.lower() in IMG_EXT)
    named = set(re.findall(r'src="img/([^"]+)"', page))
    if named != {p.name for p in imgs}:
        warn(f'the board names {len(named)} images and img/ holds {len(imgs)}')
    files = [p for p in BOARD_DIR.rglob('*') if p.is_file()]
    big = [p.name for p in imgs if p.stat().st_size > LIMIT_IMAGE]
    if big:
        warn('images over 15 MB: ' + ', '.join(big))
    total = sum(p.stat().st_size for p in files)
    if len(files) > FILES_AIM:
        warn(f'the folder holds {len(files)} files, past the brief’s about 250')
    if total >= BYTES_AIM:
        warn(f'the folder comes to {total / 1e6:.2f} MB, at or over 60 MB')
    FIG.update({'page': rel(a.out), 'html_bytes': len(page.encode()), 'images': len(imgs), 'image_bytes': sum(p.stat().st_size for p in imgs),
                'folder_files': len(files), 'folder_bytes': total, 'largest_image': max(((p.stat().st_size, p.name) for p in imgs), default=(0, None)),
                'status': {k: (v if isinstance(v, str) else list(v)) for k, v in STATUS.items()},
                'image_sources': {r['src']: r.get('source') for r in IMAGES.values()}, 'codes_in_reference_lines': sorted(c for c in LINKED if not c.startswith('rule-')),
                'anchors_linked': sorted(c for c in LINKED if c.startswith('rule-')), 'notes': NOTES, 'warnings': WARN,
                'seconds': round((datetime.datetime.now() - t0).total_seconds())})
    wcount = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9’'.,-]*", visible_text(page)))
    FIG['words'] = wcount
    FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
    print(f'wrote {rel(a.out)} ({len(page.encode()) / 1e3:.0f} kB, {wcount:,} words) and {len(imgs)} images; the folder holds {len(files)} files, {total:,} bytes')
    print('panels: ' + ', '.join(f'{k} {status_words(v)}' for k, v in STATUS.items()))
    print(f'{len(WARN)} warnings')
    ok = True
    if a.check:
        ok = run_checks(a.out, page)
        files = [p for p in BOARD_DIR.rglob('*') if p.is_file()]
        FIG.update({'folder_files': len(files), 'folder_bytes': sum(p.stat().st_size for p in files), 'warnings': WARN})
    FIG['fails'] = FAILS
    FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
    if FAILS:
        print(f'{len(FAILS)} failures: ' + '; '.join(FAILS))
    if FAILS or not ok:
        sys.exit(1)
    if WARN and a.strict:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
