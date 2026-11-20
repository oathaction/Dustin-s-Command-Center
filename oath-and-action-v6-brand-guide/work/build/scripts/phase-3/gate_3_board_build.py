"""Build the Gate 3 board of Phase 3 (November 20, 2026; the board builder, working as the design director).

Copied from board 3's builder (board_3_build.py), which stays as it is, as every earlier builder does; its machinery for
photographs, pictures, frames and checks is kept and its panels are replaced by this board's seven. Usage:
    python3 -I work/build/scripts/phase-3/gate_3_board_build.py [--reuse] [--check] [--strict] [--scratch DIR] [--out PATH]
                                                                [--final PAGE] [--final-report FILE] [--no-browser]

Reads, on every run:
    work/boards/phase-3/gate-3/board/20261120_Gate-3-Board-Content.json   the board's own words and the files it reads
    work/ledger/20261120_Gate-3-Report.md     panel 1 (section 10), panel 2 (section 9), the score names (section 3),
                                              the data check's figure (section 4) and the Not tested list (section 7)
    work/handoffs/phase-3/20261120_Board-3-Answers.md   what each of board 3's replies approved
    the final build (slots.final_page, or --final) and its build report (slots.final_report, or --final-report): every
        "after" photograph, every weight and every rule anchor; version 13 (slots.pages.v13) for the "before" photographs
    the chart kit's own export of S14, built afresh into <scratch>/kit-out/ by oa-chart.mjs
    work/handoffs/phase-3/20261120_Label-Clearance-List.json, the four apply pass notes files (the figures each card
        names, by pattern), gate_3_scores.py's output, the apply pass rescore, the board score files, and the check files
        the content file names
    work/build/tokens/tokens.css (the :root tokens the page's styles name, and only those)
    work/ledger/*_Decision-Log.md and *_Open-Questions.md                  every code in a reference line must exist
Writes:
    work/boards/phase-3/gate-3/board/20261120_Gate-3-Board.html            the board (no scripts; the host wraps it)
    work/boards/phase-3/gate-3/board/img/                                  every picture it shows, composed
    work/boards/phase-3/gate-3/board/20261120_Gate-3-Board-Figures.json    every figure it prints, with its source
    work/boards/phase-3/gate-3/board/20261120_Gate-3-Board-Check-Results.json  (written by dataviz_check.js)
    <scratch>/  the kit's export, the photographs, the scores, the cache

--reuse keeps a photograph when its element's HTML, the page's styles and scripts, the window width and the picture's
setup are unchanged, and the kit's export while its sources are; without it, every photograph is taken afresh.
--no-browser opens no browser: it builds the page from the photographs already in scratch and shows the rest as waiting.
Before every browser run the build runs the machine's browsers.sh and waits until it prints "OK to open one". --check
runs dataviz_check.js with --board --no-captures, from work/build, on the page itself and on a copy wrapped as the host
wraps it; the page carries no <html> tag by contract, so axe's html-has-lang is the one failure allowed on the page
itself. --strict exits 1 on any warning. A part whose file is missing or still pending prints "Waiting for".
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
import time

ROOT = pathlib.Path(__file__).resolve().parents[4]
SCRIPTS2 = ROOT / 'work/build/scripts/phase-2'
SCRIPTS3 = ROOT / 'work/build/scripts/phase-3'
sys.path.insert(0, str(SCRIPTS3))
import board_1_build as B1  # noqa: E402   board 1's Markdown readers and quoted-words rules (D3-206)

DATE = '20261120'
BOARD_DIR = ROOT / 'work/boards/phase-3/gate-3/board'
IMG = BOARD_DIR / 'img'
CONTENT = BOARD_DIR / f'{DATE}_Gate-3-Board-Content.json'
FIGURES = BOARD_DIR / f'{DATE}_Gate-3-Board-Figures.json'
OUT = BOARD_DIR / f'{DATE}_Gate-3-Board.html'
SCRATCH_ROOT = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/b10533d7-1a9f-5c9c-9fa4-64f6867e8ec0/scratchpad')
SCRATCH_DEFAULT = SCRATCH_ROOT / 'c09/builder'
BROWSERS_SH = SCRATCH_ROOT / 'c09/browsers.sh'
LABEL_FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
NEWSPRINT = (0xDC, 0xD9, 0xD2)
LABEL_INK = (0x4E, 0x53, 0x5B)
CONTENT_W = 1280          # the widest picture that sits in the board's column at a 1440 px window with no frame scroll
REGION_W = 288            # a picture wider than a 320 px window's column scrolls in its own named frame
FILES_AIM = 120           # the brief: under 120 pictures
BYTES_AIM = 30_000_000    # and under 30 MB, so one publish carries it
LIMIT_IMAGE = 15_000_000
LIMIT_PAGE = 16_000_000
FLAGGED = B1.FLAGGED
CODE_DEC = B1.CODE_DEC
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp')
DESK, PHONE = 1440, 390
CRIT = ['craft', 'clarity', 'brand_fidelity', 'usefulness', 'evidence_honesty', 'accessibility']
PATH_RE = r'\b(?:work|source|deliverables|brief)/[\w./-]+|\b[\w-]+\.(?:json|md|py|mjs|js|csv|html)\b'

C = {}
LOG = set()
SCRATCH = SCRATCH_DEFAULT
WARN, NOTES, FIG, QUOTED, LINKED = [], [], {}, [], set()
FILL = {}
IMAGES = {}
STATUS = {}
CACHE = {}
PREVIEW_IDS = None        # the ids on the final page, which version 14 publishes
LINKS = []                # every link to the chapters page, one entry a link
FAILS = []                # what fails the build outright, whatever --strict says
PAGES = {}                # page key -> {'path', 'text', 'frame'}
NO_BROWSER = False
REFS = []                 # file paths and codes moved out of quoted words, for the panel's reference line
RECIPE_V = {'clip': 'clip-2', 'export': 'export-1'}   # a recipe's version: a change to it in the renderer takes its pictures again


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


def text_of(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment or ''))).strip()


def rid_anchor(rid):
    return 'rule-' + str(rid).replace('.', '-')


def rule_href(rid):
    """A rule's live entry in the chapters page (version 14); the anchor must be on the final build's page."""
    a = rid_anchor(rid)
    if PREVIEW_IDS is not None and a not in PREVIEW_IDS:
        fail(f'Rule {rid}: #{a} is not on the final build’s page')
    LINKED.add(a)
    LINKS.append(a)
    return f'{C["slots"]["preview_url"]}#{a}'


def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '-', str(s)).strip('-')


def scratch_path(s):
    """A slot's path: '[scratch]/...' under this session's scratch folder, else relative to the project."""
    if not s:
        return None
    s = str(s)
    if s.startswith('[scratch]/'):
        return SCRATCH_ROOT / s[len('[scratch]/'):]
    p = pathlib.Path(s)
    return p if p.is_absolute() else ROOT / p


# ------------------------------------------------------------------------------------------------------- the pages
def load_pages(final, final_report):
    """The final build (the board never builds the guide: it reads the page the main session names) and the earlier
    pages the content file names. -> G, the final page's record."""
    for k, v in (C['slots'].get('pages') or {}).items():
        p = ROOT / v
        PAGES[k] = {'path': p, 'text': None, 'frame': None}
        if not p.is_file():
            warn(f'the content file names {v} for {k}, and it is not there')
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
    FIG['final_build'] = {'page': rel(fp) if fp else None, 'report': rel(rp) if rp else None, 'bytes': report.get('bytes'),
                          'built': report.get('built'), 'warnings': len(report.get('warnings', [])), 'rules': report.get('rules'),
                          'specimens': report.get('specimens_placed'), 'label': C['slots'].get('final_label'),
                          'sha256': hashlib.sha256(fp.read_bytes()).hexdigest() if ok else None}
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
    for _ in range(40):
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
    """One browser at a time: gate_3_board_render.js opens each page in turn and closes the browser at the end."""
    if not jobs or not browser_gate(label):
        return
    jp = SCRATCH / f'render-jobs-{label}.json'
    jp.write_text(json.dumps(jobs))
    t0 = time.time()
    r = subprocess.run(['node', str(SCRIPTS3 / 'gate_3_board_render.js'), str(jp)], cwd=ROOT / 'work/build',
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    (SCRATCH / f'render-{label}.log').write_text(r.stdout + r.stderr)
    FIG.setdefault('render_seconds', {})[label] = round(time.time() - t0)
    for line in r.stdout.splitlines():
        if line.startswith('failed') or line.startswith('page error'):
            warn('render: ' + line)
    if r.returncode != 0 and 'failed' not in r.stdout:
        warn('the renderer stopped: ' + r.stderr[-300:])


def shot_sig(it):
    text = page_text(it['page'])
    if it.get('recipe') == 'export':
        src = pathlib.Path(it['svg']).read_text() if pathlib.Path(it['svg']).exists() else None
    else:
        src = element_html(text, it['el']) if text else None
    if src is None:
        return None
    return sha(page_frame(it['page']), it['w'], src, it['el'], it.get('draw', True), it.get('sticky', False),
               RECIPE_V.get(it.get('recipe'), '') + json.dumps(it.get('clip') or '', sort_keys=True), it.get('context', ''),
               json.dumps(it.get('actions') or []), 'g3r1')


def run_shots(items, reuse, label='guide'):
    """items: dicts {key, page, el, w, clip, recipe, draw, sticky, svg} -> {key: path}. One page load per page, window
    and setup, only for the items that changed."""
    shots = SCRATCH / 'shots'
    shots.mkdir(parents=True, exist_ok=True)
    sig_file = SCRATCH / 'shot-sigs.json'
    sigs = json.loads(sig_file.read_text()) if sig_file.exists() else {}
    paths, todo = {}, {}
    for it in items:
        p = shots / f'{it["key"]}.png'
        paths[it['key']] = p
        s = shot_sig(it)
        if s is None:
            warn(f'{it["page"]}: the page holds no element {it["el"]}')
            continue
        if reuse and p.exists() and sigs.get(it['key']) == s:
            continue
        gk = (it['page'], it['w'], bool(it.get('draw', True)), bool(it.get('sticky', False)))
        todo.setdefault(gk, []).append((it, s, p))
    jobs = []
    for (pk, w, draw, sticky), its in sorted(todo.items(), key=lambda kv: (kv[0][0], -kv[0][1])):
        jobs.append({'file': str(PAGES[pk]['path']), 'width': w, 'height': 900 if w > 600 else 844, 'static_sticky': not sticky,
                     'draw_all': draw, 'text_scale': 1,
                     'items': [{'selector': it.get('sel') or css_selector(it['el']), 'out': str(p), 'measure': False,
                                'recipe': it.get('recipe'), 'clip': it.get('clip'), 'svg': it.get('svg'), 'context': it.get('context'),
                                'actions': it.get('actions') or []}
                               for it, s, p in its]})
    if jobs:
        n = sum(len(j['items']) for j in jobs)
        print(f'photographing {n} elements on {len(jobs)} page loads ...')
        for j in jobs:
            for x in j['items']:
                if pathlib.Path(x['out']).exists():
                    pathlib.Path(x['out']).unlink()
        run_render(jobs, label)
        for it in items:
            p = paths[it['key']]
            s = shot_sig(it)
            if s is not None and p.exists():
                sigs[it['key']] = s
        sig_file.write_text(json.dumps(sigs, indent=1))
    taken = {x['out'] for j in jobs for x in j['items']}
    FIG.setdefault('shots', {})[label] = {'asked': len(items), 'taken': sum(1 for k, p in paths.items() if str(p) in taken and p.exists()),
                                          'page_loads': len(jobs), 'missing': sorted(k for k, p in paths.items() if not p.exists())[:40]}
    return paths


# ------------------------------------------------------------------------------------------------------- the kit's export
def kit_export(spec, reuse):
    """The chart kit's own build of one chart, with its SVG and PNG exports, into <scratch>/kit-out/<spec>/. Rebuilt when
    the spec, its data, its form or the kit's shared files change. -> the folder, or None."""
    S = C['slots']
    kd = ROOT / S['kit_dir']
    out = SCRATCH / 'kit-out'
    sp = kd / 'specs' / f'{spec}.json'
    J = json.loads(sp.read_text())
    files = [sp, kd / 'oa-chart.mjs', kd / 'kit.js', kd / 'kit-build.js', kd / 'parts.js', kd / 'kit.css', kd / 'checks.js',
             kd / 'forms' / f'{J.get("form")}.js', ROOT / S['tokens_css']]
    ds = J.get('dataset')
    for d in (ds if isinstance(ds, list) else [ds] if ds else []):
        for ext in ('.csv', '.meta.json'):
            if (ROOT / 'work/build/data' / f'{d}{ext}').exists():
                files.append(ROOT / 'work/build/data' / f'{d}{ext}')
    want = sha(*[f.read_bytes() for f in files if f.exists()])
    stamp = out / spec / 'board-sig.txt'
    if reuse and stamp.exists() and stamp.read_text() == want:
        return out / spec
    if not browser_gate(f'the kit, {spec}'):
        return out / spec if (out / spec).exists() else None
    r = subprocess.run(['node', str(ROOT / S['kit_command']), 'build', spec, '--out', str(out), '--date', DATE], cwd=ROOT,
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    (SCRATCH / f'kit-{spec}.log').write_text(r.stdout + r.stderr)
    if r.returncode != 0 or not re.search(r'^PASS ' + spec.upper(), r.stdout, flags=re.M):
        warn(f'the kit’s build of {spec} did not pass: ' + (r.stdout + r.stderr)[-200:])
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(want)
    FIG.setdefault('kit_builds', {})[spec] = {'out': rel(out / spec), 'line': next((l for l in r.stdout.splitlines() if l.startswith(('PASS', 'FAIL'))), '')}
    return out / spec


# ------------------------------------------------------------------------------------------------------- pictures
def png_size(p):
    return B1.png_size(p)


def img_size(p):
    from PIL import Image
    with Image.open(p) as im:
        return im.size


def compose(name, parts, cols=None, gap=24, label_h=26):
    """One picture of one or more, each part at its true size on whole pixels, its label set in Inter Medium at 13 px
    above it (D3-196), saved as a lossless WebP: every pixel as captured. parts: [(path, label)]. Grayscale parts are
    composed in one gray channel when every part is gray."""
    from PIL import Image, ImageDraw, ImageFont
    out = IMG / f'{DATE}_{name}.webp'
    parts = [(x[0], x[1]) for x in parts]
    for p, _ in parts:
        need(pathlib.Path(p).exists(), f'missing picture {rel(p)} for {name}')
    if any(img_size(p)[1] > 16000 or img_size(p)[0] > 16000 for p, _ in parts):
        out = IMG / f'{DATE}_{name}.png'
    if not any(lab for _, lab in parts):
        label_h = 0
    sig = sha(json.dumps([[str(p), file_sig(p), lab] for p, lab in parts] + [cols, gap, label_h, 'g3-webp']))
    if out.exists() and CACHE.get(out.name) == sig:
        w, h = img_size(out)
    else:
        ims = [Image.open(p) for p, _ in parts]
        gray = all(im.mode == 'L' for im in ims)
        mode = 'L' if gray else 'RGB'
        lum = lambda c: round(0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2])
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
    """The panel's reference line: its own codes, then the codes and paths moved out of quoted words."""
    moved = sorted(B1.MOVED, key=lambda c: (re.sub(r'[^A-Z]', '', c.split('-')[0]), int(re.sub(r'\D', '', c.split('-')[1]) or 0)))
    B1.MOVED.clear()
    items = [x.strip() for x in re.split(r'\s+·\s+', refs or '') if x.strip()] + moved + REFS
    REFS.clear()
    items = list(dict.fromkeys(items))
    s = ' · '.join(items)
    for c in re.findall(r'\b' + CODE_DEC + r'\b', s):
        LINKED.add(c)
        if c not in LOG:
            warn(f'{c} in the reference line of {where} is not in the decision log or the open questions')
    return f'<p class="codes">Reference: {esc(s)}</p>' if s else ''


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


# ------------------------------------------------------------------------------------------------------- quoted words
def face(s):
    """A teammate's Markdown made fit for the board's face, before B1.md_inline renders it: a parenthesis that holds only
    a file path moves to the reference line; a code span the content file gives words for takes them; any other code span
    that names a file moves to the reference line; "section N" of the report names the board's panel."""
    s = str(s or '')

    def poss(m):
        B1.MOVED.add(m.group(2))
        lead = m.group(1)
        return lead + ('The ' if not lead or lead.rstrip().endswith(('.', ';', ':')) else 'the ')
    s = re.sub(r'(^|[.;:]\s+|(?<=[\w,])\s)(' + CODE_DEC + r')(?:’|\')s\s+', poss, s)

    def mv(m):
        REFS.append(m.group(1))
        return ''
    s = re.sub(r'\s*\(`([^`]*(?:/|\.(?:md|json|py|mjs|js|csv|html))[^`]*)`\)', mv, s)
    fw = C.get('face_words', {})

    def span(m):
        v = m.group(1)
        if v in fw:
            return fw[v]
        if re.search(PATH_RE, v):
            REFS.append(v)
            warn(f'a file name in quoted words with no face words: {v}')
            return 'a file'
        return m.group(0)
    s = re.sub(r'`([^`]+)`', span, s)
    for code, w_ in (C.get('code_words') or {}).items():
        if re.search(r'\b' + re.escape(code) + r'\b', s):
            B1.MOVED.add(code)
            s = re.sub(r'\s*\(' + re.escape(code) + r'\)', '', s)
            s = re.sub(r'\b' + re.escape(code) + r'\b', w_, s)
    sp = C.get('section_to_panel', {})
    s = re.sub(r'\b(?:this report[’\']s )?section (\d+)\b', lambda m: f'panel {sp[m.group(1)]}' if m.group(1) in sp else m.group(0), s)
    return s


def curl(s):
    """Straight quotes and apostrophes curled (Master Brief section 6), outside code spans: an apostrophe after a letter or
    figure closes, one at a word's start opens; a double quote after a space, a bracket or the start opens."""
    out = []
    for k, part in enumerate(re.split(r'(`[^`]*`)', s or '')):
        if k % 2:
            out.append(part)
            continue
        part = re.sub(r"(?<=[\w.,;:!?)\]%])'", '’', part)
        part = re.sub(r"'", '‘', part)
        part = re.sub(r'(^|(?<=[\s(\[—-]))"', '“', part)
        part = part.replace('"', '”')
        out.append(part)
    return ''.join(out)


def quoted(s):
    """Quoted words rendered: codes to the reference line (board 1's rules), straight quotes curled, Markdown bold and
    code set."""
    s = curl(face(s))
    QUOTED.append(B1.strip_codes(s))
    return B1.md_inline(s, quote=True)


def report_text():
    t = read(C['slots']['report'])
    need(t, f'the Gate 3 report is not there: {C["slots"]["report"]}')
    return t


def report_section(R, n):
    return B1.md_section(R, [rf'{n}\.\s.*'])


def blocks(text):
    """A Markdown block's parts in order: ('p', text), ('table', head, rows), ('list', items), ('bold', text)."""
    out, lines, i = [], (text or '').splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
            continue
        if l.strip().startswith('|'):
            j = i
            while j < len(lines) and lines[j].strip().startswith('|'):
                j += 1
            for head, rows in B1.md_tables('\n'.join(lines[i:j])):
                out.append(('table', head, rows))
            i = j
            continue
        if re.match(r'^#+\s', l):
            out.append(('h', re.sub(r'^#+\s+', '', l).strip()))
            i += 1
            continue
        if re.match(r'^\s*[-*]\s+', l):
            j = i
            while j < len(lines) and (re.match(r'^\s*[-*]\s+', lines[j]) or (lines[j].startswith('  ') and lines[j].strip())):
                j += 1
            out.append(('list', B1.md_items('\n'.join(lines[i:j]))))
            i = j
            continue
        j = i
        para = []
        while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith('|') and not re.match(r'^(#+\s|\s*[-*]\s+)', lines[j]):
            para.append(lines[j].strip())
            j += 1
        out.append(('p', ' '.join(para)))
        i = j
    return out


def table(head, rows, caption, cls='dt', num_cols=(), first_is_head=True, extra=None):
    """A live table from quoted Markdown cells. extra: (index, head, [cell html]) inserts a column."""
    head = list(head)
    if extra:
        head.insert(extra[0], extra[1])
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if k in num_cols else ""}>{quoted(c) if not (extra and k == extra[0]) else esc(c)}</th>' for k, c in enumerate(head))
    body = ''
    for r_i, r in enumerate(rows):
        cells = list(r)
        rendered = [quoted(c) for c in cells]
        if extra:
            rendered.insert(extra[0], extra[2][r_i])
        tds = ''
        for k, c in enumerate(rendered):
            num = ' class="num"' if k in num_cols else ''
            tds += f'<th scope="row">{c}</th>' if (k == 0 and first_is_head) else f'<td{num}>{c}</td>'
        body += f'<tr>{tds}</tr>'
    QUOTED.append(caption)
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{esc(caption)}; scrolls sideways"><table class="{cls}">'
            f'<caption>{esc(caption)}</caption><thead><tr>{hd}</tr></thead><tbody>{body}</tbody></table></div>')


def read_fact(f):
    """One figure from a teammate's file, by the pattern the content file gives; None, with a warning, when it is not
    there."""
    src = scratch_path('[scratch]/' + f['scratch_file']) if f.get('scratch_file') else ROOT / f['file']
    t = src.read_text() if src and src.exists() else ''
    m = re.search(f['pattern'], t, flags=re.M | re.S)
    if not m:
        warn(f'no figure for {f.get("name", "a fact")} in {rel(src) if src else "?"}: {f["pattern"][:60]}')
        return None
    FIG.setdefault('facts', {})[f.get('name', f['pattern'][:30])] = {'file': rel(src), 'value': m.groups()}
    return m


# ------------------------------------------------------------------------------------------------------- panel 1
def split_first(s, seps=(': ', '. ')):
    """The words before the first ': ' or '. ' (whichever comes first) and the rest, the separator's mark kept on the head
    only when it is a full stop."""
    best = None
    for sp in seps:
        i = s.find(sp)
        if i > 0 and (best is None or i < best[0]):
            best = (i, sp)
    if not best:
        return s.strip(), ''
    i, sp = best
    return s[:i].strip(), s[i + len(sp):].strip()


def period(s):
    """A cell from a table, made a sentence: a full stop added where it ends without one."""
    s = (s or '').strip()
    return s if not s or s.rstrip('”’"\')').endswith(('.', '?', '!')) else s + '.'


def first_sentence(s):
    m = re.match(r'^(.+?[.])\s+(.*)$', s.strip())
    if m:
        return m.group(1), m.group(2)
    return s.strip().rstrip('.') + '.', ''


def four_width():
    """The four-width guide check's results on version 14, or None."""
    p = scratch_path(C['slots'].get('four_width_check'))
    if not (p and p.is_file()):
        return None
    J = json.loads(p.read_text())
    f = J.get('failures')
    J['_n_fail'] = f if isinstance(f, int) else len(f or [])
    J['_file'] = rel(p)
    return J


def four_width_clause(s):
    """Item 1's clause on the four-width check, read from the check's own results file, so the two cannot disagree."""
    m = re.search(r'the four-width check passes on version 14 with (\d+) failures', s)
    if not m:
        return s
    J = four_width()
    if J is None:
        warn('item 1 names the four-width check, and its results file is not there')
        return s
    if int(m.group(1)) != J['_n_fail'] or not J.get('pass'):
        warn(f'the report gives the four-width check {m.group(1)} failures, and its file {J["_n_fail"]} (pass: {J.get("pass")})')
    words = (f'the four-width check passes on version 14 with {nw(J["_n_fail"])} failures' if J.get('pass')
             else f'the four-width check fails on version 14 with {nw(J["_n_fail"])} failures')
    FIG.setdefault('decide_reads', {})['four_width'] = {'file': J['_file'], 'pass': J.get('pass'), 'failures': J['_n_fail']}
    return s[:m.start()] + words + s[m.end():]


def wcag(h1, h2):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    a, b = lum(h1.lstrip('#')), lum(h2.lstrip('#'))
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


SWATCH_CSS = []


def swatches(what, G):
    """Item 4's colors on Charcoal at true size: each hex the item names with its token, drawn from tokens.css, with the
    ratios the palette plate on version 14 prints for it on Charcoal (checked here against WCAG's formula)."""
    S = C['sections']['decide']
    tk = (ROOT / C['slots']['tokens_css']).read_text()
    m = re.search(r'--oa-color-palette-charcoal:\s*(#[0-9A-Fa-f]{6})', tk)
    charcoal = m.group(1) if m else None
    plate = element_html(G['text'], 'fig-s-14-palette-spec') or '' if G.get('text') else ''
    ptxt = re.sub(r'(\s*\|\s*)+', ' | ', re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' | ', plate))))
    items = []
    for hx in dict.fromkeys(re.findall(r'#[0-9A-Fa-f]{6}', what)):
        var = next((v for v, val in re.findall(r'(--oa-color-[a-z0-9-]+):\s*([^;]+);', tk) if val.strip().upper() == hx.upper()), None)
        if not var:
            warn(f'item 4 names {hx}, which tokens.css does not define')
            continue
        cls = 'sw-' + slug(var.replace('--oa-color-', ''))
        SWATCH_CSS.append(f'.{cls}{{background:var({var})}}')
        # the plate's Charcoal column: the hex, then its mark ratio, then its label line
        pm = re.search(re.escape(hx.upper()) + r' \| ([\d.]+)\xa0?\s*to\s*1 rounded down, ([a-z ]+?) \| Label in (\w+), ([\d.]+)\s*to\s*1 rounded down, text', ptxt)
        if not pm:
            warn(f'the palette plate prints no ratio for {hx}')
            continue
        ratio, use, label_in, lratio = pm.groups()
        if charcoal:
            calc = int(wcag(hx, charcoal) * 100) / 100
            if f'{calc:.2f}' != ratio:
                warn(f'{hx} on Charcoal: the plate prints {ratio} to 1 and WCAG gives {calc:.2f}')
        items.append(fill(S['swatch_item'], {'hex': hx, 'ratio': ratio, 'use': S['swatch_use'].get(use.strip(), use.strip()), 'label_in': label_in, 'lratio': lratio}))
        items[-1] = (cls, hx, items[-1])
    if not items:
        return ''
    QUOTED.extend(x[2] for x in items)
    cells = ''.join(f'<li><span class="sw {cls}" aria-hidden="true"></span><span class="sw-t">{esc(words_)}</span></li>' for cls, hx, words_ in items)
    FIG.setdefault('decide_reads', {})['swatches'] = [x[2] for x in items]
    return (f'<figure class="swf"><figcaption>{esc(S["swatch_caption"])}</figcaption><ul class="sw-ground">{cells}</ul></figure>')


def other_choice(rec):
    """Board 3's closed alternative, as the approved recommendation prints it: the sentence that offers another reply."""
    parts = re.split(r'(?<=[.”])\s+(?=[A-Z])', rec.strip())
    keep = [x for x in parts if not re.search(r'\breply “', x)]
    gone = [x for x in parts if re.search(r'\breply “', x)]
    return ' '.join(keep), ' '.join(gone)


def decide_panel(R, G):
    S = C['sections']['decide']
    sec = report_section(R, 10)
    if not sec:
        return section('decide', pending(S['wait']), ('waiting', 'report')), 0
    bl = blocks(sec)
    by_head = lambda name: next((b for b in bl if b[0] == 'table' and len(b[1]) > 1 and b[1][1].strip().lower().startswith(name)), None)
    dec, que = by_head('decision'), by_head('question')
    words_t = next((b for b in bl if b[0] == 'table' and b[1] and b[1][0].strip().lower() == 'change'), None)
    need(dec and que, 'section 10 of the Gate 3 report holds no decisions or no questions table')
    paras = [b[1] for b in bl if b[0] == 'p']
    approve = next((p for p in paras if p.startswith('**What you approve')), '')
    # the paragraphs after the word for word table and before the questions belong to item 6
    w_notes = []
    if words_t:
        k = bl.index(words_t) + 1
        while k < len(bl) and bl[k][0] == 'p' and not bl[k][1].startswith('**'):
            w_notes.append(bl[k][1])
            k += 1
    FILL.update({'n_decisions_w': nw(len(dec[2])), 'n_questions_w': nw(len(que[2])), 'n_items_w': nw(len(dec[2]) + len(que[2]))})
    parts = [f'<p class="intro">{esc(fill(S["lede"]))}</p>']
    lis, cards_d, cards_q = [], [], []
    for row in dec[2]:
        n, what, rec = row[0], row[1], row[2]
        head, rest = split_first(what, (': ', '. ', '; '))
        ans, rests = first_sentence(four_width_clause(rec))
        lis.append(f'<li><a href="#d-{esc(n)}"><span class="rn">{esc(fill(S["item_label"], {"n": n}))}</span> <span class="rb"><span class="rl">{quoted(head)}</span>'
                   f'<span class="rr"><span class="k">{esc(S["rec_tag"])}</span> {quoted(ans)}</span></span></a></li>')
        dl = []
        if rests:
            dl.append((S['rests_k'], quoted(period(rests))))
        if rest:
            dl.append((S['covers_k'], quoted(period(cap(face(rest))))))
        m = re.search(r'\(section (\d+)\)', what)
        link = ''
        if m and m.group(1) in C.get('section_to_panel', {}):
            pn = C['section_to_panel'][m.group(1)]
            key = next(k for k, v in C['sections'].items() if v['n'] == pn)
            link = f'<p class="small"><a href="#p-{key}">{esc(fill(S["see_panel"], {"n": pn}))}</a></p>'
        extra = ''
        if re.findall(r'#[0-9A-Fa-f]{6}', what) and G.get('text'):
            extra += swatches(what, G)
        if n == '6' and words_t:
            extra += table(words_t[1], words_t[2], S['words_caption'], cls='dt ww')
            extra += ''.join(f'<p>{quoted(x)}</p>' for x in w_notes)
        cards_d.append(f'<article class="dec" id="d-{esc(n)}"><p class="label">{esc(fill(S["item_label"], {"n": n}))}</p><h4 class="dec-h">{quoted(head)}</h4>'
                       f'<p class="dec-rec"><span class="tag rec">{esc(S["rec_tag"])}</span> {quoted(ans)}</p>'
                       + ('<dl class="facts f2">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{b}</dd></div>' for a, b in dl) + '</dl>' if dl else '') + extra + link + '</article>')
    for row in que[2]:
        n, q, dft = row[0], period(row[1]), period(row[2])
        lis.append(f'<li><a href="#d-{esc(slug(n))}"><span class="rn">{esc(fill(S["question_label"], {"n": n}))}</span> <span class="rb"><span class="rl">{quoted(q)}</span>'
                   f'<span class="rr"><span class="k">{esc(S["default_tag"])}</span> {quoted(dft)}</span></span></a></li>')
        cards_q.append(f'<article class="dec" id="d-{esc(slug(n))}"><p class="label">{esc(fill(S["question_label"], {"n": n}))}</p><h4 class="dec-h">{quoted(q)}</h4>'
                       f'<p class="dec-rec"><span class="tag rec">{esc(S["default_tag"])}</span> {quoted(dft)}</p></article>')
    parts.append(f'<h3 class="sub rep-h">{esc(fill(S["list_h"]))}</h3><ol class="replies">{"".join(lis)}</ol>')
    parts.append(f'<p class="reply">{esc(S["reply"])}</p>')
    parts.append(f'<h3 class="sub grp">{esc(S["decisions_h"])}</h3>' + ''.join(cards_d))
    parts.append(f'<h3 class="sub grp">{esc(S["questions_h"])}</h3>' + ''.join(cards_q))
    if approve:
        body = re.sub(r'^\*\*What you approve at this gate\.\*\*\s*', '', approve)
        parts.append(f'<h3 class="sub grp">{esc(S["approve_h"])}</h3><p class="approve">{quoted(body)}</p>')
    parts.append(f'<p class="reply">{esc(S["reply"])}</p>')
    FIG['decide'] = {'decisions': len(dec[2]), 'questions': len(que[2]), 'word_rows': len(words_t[2]) if words_t else 0,
                     'from': C['slots']['report'] + ', section 10'}
    html_ = section('decide', ''.join(parts), 'ready')
    return html_, len(dec[2]) + len(que[2])


# ------------------------------------------------------------------------------------------------------- panel 2
def phase4_room(G):
    """Phase 4's room under 16 MB, from version 14's build report: the page's limit less the page, chapter 15's held
    allocation and Phase 5's two chapters as the projection carries them."""
    W = (G.get('report') or {}).get('weight') or {}
    pj = W.get('projection') or {}
    limit = int(W.get('limit') or LIMIT_PAGE)
    page = int(W.get('bytes') or 0)
    held = sum(int(v) for v in (pj.get('held_to_allocation') or {}).values())
    unbuilt = pj.get('unbuilt') or {}
    phase5 = sum(int(v) for k, v in unbuilt.items() if k in ('27', '28'))
    warn_line = int(W.get('budget_page') or 15_500_000)
    room = limit - page - held - phase5
    return {'limit': limit, 'page': page, 'held': held, 'phase5': phase5, 'room': room, 'room_warn': warn_line - page - held - phase5,
            'free': limit - page}


def phase4_panel(R, G):
    S = C['sections']['phase4']
    sec = report_section(R, 9)
    if not sec:
        return section('phase4', pending(S['wait']), ('waiting', 'report'))
    rm = phase4_room(G) if G['report'] else None
    out = []
    intro = sec.split('\n### ')[0]
    for b in blocks(intro):
        if b[0] == 'p':
            out.append(f'<p class="intro">{quoted(b[1])}</p>')
    caps = S.get('captions', {})
    subs = [('produces_h', r'What Phase 4 produces'), ('channels_h', r'The eight channels'), ('build_h', r'How the applications are built'),
            ('weight_h', r'Page weight'), ('chats_h', r'Chats and boards'), ('team_h', r'Team and checks')]
    alloc = {}
    for key, name in subs:
        block = B1.md_section(sec, [name])
        if block is None:
            warn(f'section 9 of the Gate 3 report has no part “{name}”')
            continue
        out.append(f'<h3 class="sub">{esc(S[key])}</h3>')
        tn = 0
        for b in blocks(block):
            if b[0] == 'p':
                out.append(f'<p>{quoted(b[1])}</p>')
            elif b[0] == 'list':
                out.append('<ul class="ul">' + ''.join(f'<li>{quoted(x)}</li>' for x in b[1]) + '</ul>')
            elif b[0] == 'table':
                head, rows = b[1], b[2]
                cap_ = (caps.get(key) or [])[tn] if tn < len(caps.get(key) or []) else S[key]
                tn += 1
                if key == 'weight_h' and rm and head and re.search(r'Allocation', head[-1]):
                    cells = []
                    for r in rows:
                        v = int(re.sub(r'\D', '', r[-1]) or 0)
                        if re.match(r'All seven', r[0]):
                            alloc['total'] = v
                        else:
                            alloc[r[0]] = v
                        share = 100 * v / rm['room'] if rm['room'] > 0 else 0
                        cells.append(f'<span class="track"><span class="lim" style="left:100%"></span><span class="bar" data-mark="bar" data-value="{share:.3f}" data-key="{esc(r[0])}" '
                                     f'style="width:{min(share, 100):.3f}%"></span></span><span class="pct">{share:.1f} percent</span>' if v else '')
                    out.append(table(head, rows, cap_, cls='dt at', num_cols=(len(head),), extra=(len(head) - 1, S['alloc_cols'][1], cells)))
                else:
                    out.append(table(head, rows, cap_, cls='dt'))
        if key == 'weight_h' and rm:
            tot = alloc.get('total') or sum(v for k, v in alloc.items() if k != 'total')
            if tot != sum(v for k, v in alloc.items() if k != 'total'):
                warn(f'the report’s allocations add up to {sum(v for k, v in alloc.items() if k != "total"):,} and its total row says {tot:,}')
            out.append(f'<p class="small">{esc(fill(S["alloc_line"], {"room": f"{rm["room"]:,}", "total": f"{tot:,}", "reserve": f"{rm["room"] - tot:,}"}))}</p>')
            said = re.search(r'have ([\d,]+) bytes between them under the page', block)
            if said and int(said.group(1).replace(',', '')) != rm['room']:
                warn(fill(S['room_mismatch'], {'said': said.group(1), 'room': f'{rm["room"]:,}'}))
            FIG['phase4'] = {'room': rm, 'allocations': alloc, 'report_room': said.group(1) if said else None}
    return section('phase4', ''.join(out), 'ready' if rm else ('partial', 'build'))


# ------------------------------------------------------------------------------------------------------- panel 3 and 4: pictures
def picture_items(pics):
    """The photographs a list of picture specs needs, in order: one a picture, or one a part of a stacked picture."""
    items = []
    for p in pics:
        if p.get('kind') == 'export':
            continue
        if p.get('parts'):
            for k, q in enumerate(p['parts']):
                items.append(shot_item(f'{p["id"]}-{k}', q))
        else:
            items.append(shot_item(p['id'], p))
    return items


def shot_item(key, p):
    it = {'key': f'p-{key}', 'page': p['page'], 'el': p['el'], 'w': int(p['w']), 'draw': p.get('draw', True), 'sticky': p.get('sticky', False)}
    if p.get('actions'):
        it['actions'] = p['actions']
    if p.get('clip'):
        c = dict(p['clip'])
        c.setdefault('within', css_selector(p['el']))
        it['clip'] = c
        it['recipe'] = 'clip'
    return it


def export_item(p, kit_dir):
    stem = next(iter(sorted(kit_dir.glob(f'{DATE}_{p["spec"].upper()}-*-{cap(p["ground"])}-{p["w"]}.svg'))), None) if kit_dir else None
    page = kit_dir / f'{p["spec"]}.html' if kit_dir else None
    if not stem or not page or not page.exists():
        return None
    pk = f'kit-{p["spec"]}'
    PAGES.setdefault(pk, {'path': page, 'text': None, 'frame': None})
    return {'key': f'p-{p["id"]}', 'page': pk, 'el': 'body', 'w': int(p['w']), 'recipe': 'export', 'svg': str(stem), 'context': p.get('context', 40),
            'sel': 'body', 'draw': False, 'sticky': True}


def gray_copy(src):
    from PIL import Image
    g = SCRATCH / 'made' / f'luma-{pathlib.Path(src).stem}.png'
    g.parent.mkdir(parents=True, exist_ok=True)
    if not g.exists() or g.stat().st_mtime < pathlib.Path(src).stat().st_mtime:
        Image.open(src).convert('RGB').convert('L').save(g, optimize=True)
    return g


def tidy(src, t):
    """A text crop cut to its own block: the rows of the matched block (the crop less its context), and with `column` the
    block's own column (from its first ink to the first gap 24 px wide), then `pad` px of the block's own ground on every
    side. Board-only; the photograph in scratch is kept."""
    from PIL import Image
    out = SCRATCH / 'made' / f'tidy-{pathlib.Path(src).stem}.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_mtime >= pathlib.Path(src).stat().st_mtime and CACHE.get(out.name) == json.dumps(t, sort_keys=True):
        return out
    im = Image.open(src).convert('RGB')
    W, H = im.size
    px = im.load()
    ctx = int(t.get('context', 8))
    y0, y1 = ctx, H - ctx
    dark = lambda c: sum(c) / 3 < 140
    always = {x for x in range(W) if sum(1 for y in range(H) if dark(px[x, y])) > 0.9 * H}
    cols = [x for x in range(W) if x not in always and any(dark(px[x, y]) for y in range(y0, y1))]
    if not cols:
        return src
    x0 = min(cols)
    x1 = max(cols) + 1
    if t.get('column'):
        gap, x = 0, x0
        while x < W:
            gap = gap + 1 if x not in cols else 0
            if gap >= 24:
                x1 = x - gap + 1
                break
            x += 1
    from collections import Counter
    ground = Counter(px[x, y] for x in range(x0, x1) for y in range(y0, y1)).most_common(1)[0][0]
    pad = int(t.get('pad', 16))
    box = im.crop((x0, y0, x1, y1))
    cv = Image.new('RGB', (box.size[0] + 2 * pad, box.size[1] + 2 * pad), ground)
    cv.paste(box, (pad, pad))
    cv.save(out, optimize=True)
    CACHE[out.name] = json.dumps(t, sort_keys=True)
    return out


def pic_html(p, shots, S, luma=False):
    """One picture at true size with its label above it, or a waiting line."""
    label = p.get('label', '')
    if p.get('parts'):
        paths = [shots.get(f'p-{p["id"]}-{k}') for k in range(len(p['parts']))]
        if not all(x and x.exists() for x in paths):
            return None
        rec = compose(f'Pic-{slug(p["id"])}', [(x, q.get('label', '')) for x, q in zip(paths, p['parts'])], cols=1)
    else:
        path = shots.get(f'p-{p["id"]}')
        if not path or not path.exists():
            return None
        if p.get('tidy'):
            path = tidy(path, p['tidy'])
        if luma:
            path = gray_copy(path)
        rec = compose(f'Pic-{slug(p["id"])}' + ('-Luma' if luma else ''), [(path, '')])
    if luma:
        alt = fill(S['luma_alt'], {'label': label})
        label = fill(S['luma_label'], {'label': label})
    elif p.get('alt'):
        alt = p['alt']
    elif p.get('kind') == 'export':
        alt = fill(S['export_alt'], {'label': label})
    else:
        alt = fill(S['alt_auto'], {'label': label, 'page': C['page_words'].get(p.get('page'), p.get('page')), 'w': p.get('w')})
    role = '' if luma else p.get('role', 'view')
    if role == 'none':
        role = ''
    rw = C['role_words'].get(role, '')
    cap_html = (f'<span class="role {esc(role)}">{esc(rw)}</span> ' if rw else '') + f'<b>{esc(label)}</b>'
    FIG.setdefault('pictures', {})[p['id'] + ('-luma' if luma else '')] = {'src': rec['src'], 'w': rec['w'], 'h': rec['h']}
    return figure(rec, alt, cap_html, top=True)


def rows_html(pics, shots, S):
    """Pictures in rows: those that share a `row` sit side by side, rows in order of first appearance."""
    rows, order, missing = {}, [], []
    for p in pics:
        h = pic_html(p, shots, S)
        if h is None:
            h = pending(fill(S['picture_wait'], {'label': p.get('label', p['id'])}))
            missing.append(p['id'])
        r = p.get('row', p['id'])
        if r not in rows:
            rows[r] = []
            order.append(r)
        rows[r].append(h)
    return ''.join(f'<div class="pair ba">{"".join(rows[r])}</div>' for r in order), missing


# ------------------------------------------------------------------------------------------------------- panel 3
def answers_rows():
    """Board 3's replies as the answers file lists them: {n: (item title, item code, approved recommendation)}."""
    t = read(C['slots']['answers'])
    need(t, f'the answers file is not there: {C["slots"]["answers"]}')
    out = {}
    for head, rows in B1.md_tables(t):
        if head and head[0].strip().lower() == 'reply':
            for r in rows:
                m = re.match(r'^(.*?)\s*\(`([^`]*)`\)\s*$', r[1])
                title, code = (m.group(1), m.group(2)) if m else (r[1], '')
                out[int(r[0])] = (title, '' if code == 'None' else code, r[2])
    return out


def card_facts(card):
    vals = {}
    ok = True
    for f in card.get('facts') or []:
        m = read_fact(f)
        if m:
            vals[f['name']] = m.group(1)
        else:
            ok = False
    return vals, ok


def answers_panel(shots):
    S = C['sections']['answers']
    A = answers_rows()
    cards = S['cards']
    need(sorted(c['n'] for c in cards) == sorted(A), f'the content file’s cards ({len(cards)}) do not match the answers file’s replies ({len(A)})')
    nones = [c for c in cards if c.get('none')]
    FILL.update({'n_answers': len(A), 'n_none_w': nw(len(nones))})
    out = [f'<p class="intro">{esc(fill(S["lede"]))}</p>']
    refs, missing, facts_missing = [], [], []
    none_lis = []
    body_cards = []
    for c in sorted(cards, key=lambda x: x['n']):
        n = c['n']
        title, code, rec = A[n]
        if code:
            refs.append(code)
        if c.get('refs'):
            refs += [x.strip() for x in c['refs'].split('·')]
        vals, ok = card_facts(c)
        if not ok:
            facts_missing.append(n)
        if c.get('none'):
            line = fill(c['none'], vals)
            none_lis.append(f'<li id="r-{n}"><span class="tag rn">{esc(fill(S["reply_tag"], {"n": n}))}</span> <b>{quoted(period(title))}</b> {esc(line)}</li>')
            continue
        rec_, other = other_choice(rec)
        h = (f'<article class="dec" id="r-{n}"><p class="label">{esc(fill(S["reply_tag"], {"n": n}))}</p><h4 class="dec-h">{quoted(title)}</h4>'
             f'<dl class="facts f2"><div><dt>{esc(S["approved_k"])}</dt><dd>{quoted(rec_)}</dd></div>'
             f'<div><dt>{esc(S["changed_k"])}</dt><dd>{esc(fill(c["changed"], vals))}</dd></div></dl>')
        if other:
            h += f'<p class="small"><b>{esc(S["other_k"])}.</b> {quoted(other)}</p>'
        if c.get('checked'):
            h += f'<p class="what"><b>{esc(S["checked_k"])}.</b> {esc(fill(c["checked"], vals))}</p>'
        if c.get('panel'):
            pn = C['sections'][c['panel']]['n']
            h += f'<p class="small"><a href="#p-{c["panel"]}">{esc(fill(S["panel_link"], {"n": pn}))}</a></p>'
        if c.get('pictures'):
            rh, miss = rows_html(c['pictures'], shots, S)
            h += rh
            missing += miss
            if c.get('luma'):
                lp = [next(p for p in c['pictures'] if p['id'] == k) for k in c['luma']]
                lh = [pic_html(p, shots, S, luma=True) for p in lp]
                if all(lh):
                    h += f'<h5 class="luma-h">{esc(S["luma_h"])}</h5><p class="what">{esc(S["luma_note"])}</p><div class="pair ba">{"".join(lh)}</div>'
                else:
                    missing.append(f'luma {n}')
        if c.get('rule'):
            links = ' · '.join(f'<a href="{esc(rule_href(r))}">{esc(fill(S["rule_link"], {"rule": r}))}</a>' for r in c['rule'])
            h += f'<p class="small rl">{links}</p>'
        h += '</article>'
        body_cards.append(h)
    out += body_cards
    out.append(f'<h3 class="sub grp">{esc(S["none_h"])}</h3><ul class="nones">{"".join(none_lis)}</ul>')
    FIG['answers'] = {'replies': len(A), 'cards': len(body_cards), 'one_line': len(nones), 'pictures_waiting': missing, 'facts_missing': facts_missing}
    st = 'ready' if not missing and not facts_missing else ('partial', 'render' if missing else 'facts')
    return section('answers', ''.join(out), st, ' · '.join(dict.fromkeys(refs)))


# ------------------------------------------------------------------------------------------------------- panel 4
def clearance_panel(shots):
    S = C['sections']['clearance']
    p = ROOT / C['slots']['label_list']
    if not p.exists():
        return section('clearance', pending('Waiting for the label clearance list.'), ('waiting', 'facts'))
    L = json.loads(p.read_text())
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    moves = L.get('charts_it_would_move') or []
    out.append(f'<p class="big">{esc(fill(S["result_line"], {"specs": L.get("specs_checked"), "drawings": f"{L.get("drawings_checked", 0):,}"}))}</p>')
    rows = []
    for c in moves:
        rows.append([c.get('id', ''), c.get('rule', ''), c.get('label', ''), c.get('widths_px', ''), str(c.get('widths_count', ''))])
    cols = S['cols']
    if rows:
        out.append(table(cols, rows, S['caption']))
    before = (L.get('before_s59s_key') or {}).get('charts') or []
    out.append(f'<h3 class="sub">{esc(S["before_h"])}</h3>')
    if before:
        b0 = before[0]
        out.append(f'<p>{esc(fill(S["before_lede"], {"count": b0.get("widths_count")}))}</p>')
        brow = [[c.get('id', ''), c.get('rule', ''), f'“{c.get("label", "")}”', f'{c.get("widths_px", "")} px', f'{c.get("widths_count", 0):,}'] for c in before]
        out.append(table(cols, brow, S['caption'] + ', before S59’s setting', num_cols=(4,)))
    out.append(f'<p>{esc(S["pic_lede"])}</p>')
    rh, miss = rows_html(S['pictures'], shots, C['sections']['answers'])
    out.append(rh)
    out.append(f'<p class="small rl"><a href="{esc(rule_href("14.77"))}">{esc(fill(C["sections"]["answers"]["rule_link"], {"rule": "14.77"}))}</a></p>')
    FIG['clearance'] = {'file': C['slots']['label_list'], 'specs': L.get('specs_checked'), 'drawings': L.get('drawings_checked'), 'would_move': moves,
                        'before': before, 'pictures_waiting': miss}
    return section('clearance', ''.join(out), 'ready' if not miss else ('partial', 'render'))


# ------------------------------------------------------------------------------------------------------- panel 5
def run_scores():
    out = SCRATCH / 'scores.json'
    r = subprocess.run([sys.executable, '-I', str(ROOT / C['slots']['scores_script']), '--out', str(out)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        warn('gate_3_scores.py did not run: ' + (r.stderr or r.stdout)[-200:])
        return None
    return json.loads(out.read_text())


def score_cell(v, w=None, both=False):
    lo = isinstance(v, (int, float)) and v < 4
    if not both:
        return f'<td class="num sc{" lo" if lo else ""}">{esc(v)}</td>'
    wlo = isinstance(w, (int, float)) and w < 4
    moved = w is not None and w != v
    return (f'<td class="num sc{" mv" if moved else ""}"><span class="r1{" lo" if wlo else ""}">{esc(w) if w is not None else "new"}</span>'
            f'<span class="r2{" lo" if lo else ""}">{esc(v)}</span></td>')


def scores_panel(R):
    S = C['sections']['scores']
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    status = 'ready'
    J = run_scores()
    # the report's section 3 table gives each item's short name and "Last scored in", row for row
    names = []
    sec = report_section(R, 3) or ''
    for head, rows in B1.md_tables(sec):
        if head and head[0] == 'Item':
            names = rows
            break
    if J:
        items = J['items']
        use_report = len(names) == len(items)
        if not use_report:
            warn(f'the report’s section 3 table has {len(names)} rows and the scores {len(items)}; names read from the score files')
        trs = []
        for k, it in enumerate(items):
            sc = it['scores']
            if use_report:
                nm, rnd, last = names[k][0], names[k][1], names[k][-1]
                rep = [int(x) if x.isdigit() else x for x in names[k][2:8]]
                if rep != [sc[c] for c in CRIT]:
                    warn(f'the report’s scores for “{nm}” ({rep}) differ from the score files’ ({[sc[c] for c in CRIT]})')
                if rnd != it['round']:
                    warn(f'the report puts “{nm}” in {rnd} and the score files in {it["round"]}')
            else:
                nm, rnd, last = it['name'], it['round'], S['file_words'].get(it['file'], it['file'])
            if S['file_words'].get(it['file']) and use_report and S['file_words'][it['file']] != last:
                warn(f'“{nm}”: the report says last scored in “{last}”, the score files say {it["file"]}')
            QUOTED.extend([nm, last])
            trs.append(f'<tr><th scope="row">{quoted(nm)}</th><td>{esc(rnd)}</td>' + ''.join(score_cell(sc[c]) for c in CRIT) + f'<td>{esc(last)}</td></tr>')
        hd = ''.join(f'<th scope="col"{" class=\"n\"" if 2 <= k <= 7 else ""}>{esc(c)}</th>' for k, c in enumerate(S['items_cols']))
        ok = J.get('items_at_4_or_more')
        out.append(f'<h3 class="sub">{esc(S["items_h"])}</h3><p class="big">{esc(fill(S["items_line_all"] if ok == J.get("items_count") else S["items_line"], {"ok": ok, "n": J.get("items_count")}))}</p>'
                   f'<div class="tw" role="region" tabindex="0" aria-label="{esc(S["items_caption"])}; scrolls sideways"><table class="scores"><caption>{esc(S["items_caption"])}</caption>'
                   f'<thead><tr>{hd}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
        FIG['scores'] = {'items': J.get('items_count'), 'at_4_or_more': ok, 'files_read': J.get('files_read'), 'names_from_report': use_report}
    else:
        status = ('partial', 'facts')
        out.append(pending('Waiting for the scores script.'))
    # this gate's rescore
    ap = ROOT / C['slots']['apply_rescore']
    if ap.exists():
        A = json.loads(ap.read_text())
        its = A.get('items', [])
        rose = sum(1 for i in its for c in CRIT if (i.get('first_scores') or {}).get(c) is not None and i['scores'][c] > i['first_scores'][c])
        fell = sum(1 for i in its for c in CRIT if (i.get('first_scores') or {}).get(c) is not None and i['scores'][c] < i['first_scores'][c])
        ready = sum(1 for i in its if i.get('ready'))
        trs = []
        for i in its:
            nm = i.get('name', i['key'])
            QUOTED.append(nm)
            trs.append(f'<tr><th scope="row">{quoted(nm)}</th><td>{esc(i.get("round", ""))}</td>' + ''.join(score_cell(i['scores'][c], (i.get('first_scores') or {}).get(c), True) for c in CRIT) + '</tr>')
        hd = ''.join(f'<th scope="col"{" class=\"n\"" if 2 <= k <= 7 else ""}>{esc(c)}</th>' for k, c in enumerate(S['items_cols'][:8]))
        out.append(f'<h3 class="sub">{esc(S["apply_h"])}</h3><p>{esc(fill(S["apply_lede"], {"n": nw(len(its))}))}</p>'
                   f'<p class="big">{esc(fill(S["apply_line_all"] if ready == len(its) else S["apply_line"], {"ready": nw(ready), "n": nw(len(its)), "rose": nw(rose, "no"), "fell": nw(fell, "none")}))}</p>'
                   f'<p class="small">{esc(S["legend"])}</p>'
                   f'<div class="tw" role="region" tabindex="0" aria-label="{esc(S["apply_caption"])}; scrolls sideways"><table class="scores"><caption>{esc(S["apply_caption"])}</caption>'
                   f'<thead><tr>{hd}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
        FIG['apply_rescore'] = {'file': C['slots']['apply_rescore'], 'items': len(its), 'ready': ready, 'rose': rose, 'fell': fell}
    # the boards
    bd = {}
    for b in (J or {}).get('boards', []):
        bd.setdefault(b['key'], []).append(b)
    rows = []
    for key in ('board_2', 'board_3'):
        bs = bd.get(key) or []
        first, last = None, None
        if key == 'board_3':
            p3 = ROOT / 'work/handoffs/phase-3/20261120_Board-3-CD-Scores.json'
            if p3.exists():
                B3 = json.loads(p3.read_text())['items'][0]
                first, last = B3.get('first_scores'), B3.get('scores')
        elif len(bs) >= 2:
            first, last = bs[0]['scores'], bs[-1]['scores']
        if first and last:
            rows.append(f'<tr><th scope="row">{esc(S["board_names"][key])}</th>' + ''.join(score_cell(last[c], first[c], True) for c in CRIT) + '</tr>')
    if rows:
        hd = ''.join(f'<th scope="col"{" class=\"n\"" if k >= 1 else ""}>{esc(c)}</th>' for k, c in enumerate(S['boards_cols']))
        out.append(f'<h3 class="sub">{esc(S["boards_h"])}</h3><p>{esc(S["boards_lede"])}</p>'
                   f'<div class="tw" role="region" tabindex="0" aria-label="{esc(S["boards_caption"])}; scrolls sideways"><table class="scores sb"><caption>{esc(S["boards_caption"])}</caption>'
                   f'<thead><tr>{hd}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    # this board
    out.append(f'<h3 class="sub">{esc(S["this_h"])}</h3>')
    bp = ROOT / C['slots']['board_scores']
    Bj = None
    if bp.exists():
        try:
            Bj = json.loads(bp.read_text())
        except json.JSONDecodeError as e:
            warn(f'{rel(bp)} could not be read: {e}')
    if Bj is not None and not any(Bj.get(k) for k in C['slots'].get('board_rescore_keys', [])):
        Bj = None
        FIG['board_score'] = {'file': C['slots']['board_scores'], 'state': 'first score only; the slot waits for the rescore'}
    if Bj is not None:
        try:
            it = Bj['items'][0]
            first, last = it.get('first_scores') or it.get('scores'), it.get('scores')
            hd = ''.join(f'<th scope="col"{" class=\"n\"" if k >= 1 else ""}>{esc(c)}</th>' for k, c in enumerate(S['boards_cols']))
            out.append(f'<p>{esc(S["this_line"])}</p><div class="tw" role="region" tabindex="0" aria-label="{esc(S["this_h"])}; scrolls sideways"><table class="scores sb"><caption>{esc(S["this_h"])}</caption>'
                       f'<thead><tr>{hd}</tr></thead><tbody><tr><th scope="row">{esc(S["board_names"]["gate_3_board"])}</th>'
                       + ''.join(score_cell(last[c], first[c] if it.get('first_scores') else None, bool(it.get('first_scores'))) for c in CRIT) + '</tr></tbody></table></div>')
            FIG['board_score'] = {'file': C['slots']['board_scores'], 'scores': last}
        except (json.JSONDecodeError, KeyError, TypeError, IndexError) as e:
            warn(f'{rel(bp)} could not be read: {e}')
            out.append(pending(S['this_wait']))
            status = ('partial', 'cd_board')
    else:
        out.append(pending(S['this_wait']))
        status = status if status != 'ready' else ('partial', 'cd_board')
    return section('scores', ''.join(out), status)


# ------------------------------------------------------------------------------------------------------- panel 6
def bar_table(rows, cols, caption, cls='wt'):
    """rows: [(name, bytes, figure or None)]; every bar on one scale that reaches the largest share, with its figure's
    line drawn where 100 percent falls (board 3's B3-S6)."""
    top = max([100.0] + [100 * b / lim for _, b, lim in rows if lim])
    trs = ''
    for name, b, lim in rows:
        share = 100 * b / lim if lim else None
        fig_at = 100 * 100 / top
        bar = (f'<span class="track"><span class="lim" style="left:{fig_at:.3f}%"></span><span class="bar" data-mark="bar" data-value="{share:.3f}" data-key="{esc(name)}" '
               f'style="width:{100 * share / top:.3f}%"></span></span><span class="pct">{share:.1f} percent</span>' if share is not None else '')
        trs += f'<tr><th scope="row">{esc(name)}</th><td class="barcell">{bar}</td><td class="num">{b:,}</td><td class="num">{"" if lim is None else f"{int(lim):,}"}</td></tr>'
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if i >= 2 else ""}>{esc(c)}</th>' for i, c in enumerate(cols))
    return (f'<figure class="wfig"><div class="tw" role="region" tabindex="0" aria-label="{esc(caption)}; scrolls sideways"><table class="{cls}">'
            f'<caption>{esc(caption)}</caption><thead><tr>{hd}</tr></thead><tbody>{trs}</tbody></table></div></figure>')


def weight_panel(G, R):
    S = C['sections']['weight']
    if not G['report']:
        return section('weight', pending(S['wait']), ('waiting', 'build'))
    W = G['report']['weight']
    pj = W.get('projection', {})
    ch = W.get('chapters', {})
    stop = int(ch.get('14', {}).get('budget') or 0)
    with_kit = int(pj.get('chapter_14_with_kit', 0))
    kit = int(W.get('parts', {}).get('chart kit', 0))
    m = None
    for n in G['report'].get('notes', []):
        m = re.search(S['kit_note_re'], n) or m
    kit_fig = int(m.group(2).replace(',', '')) if m else None
    if m and int(m.group(1).replace(',', '')) != kit:
        warn(f'the build report’s note gives the kit {m.group(1)} bytes and its parts {kit:,}')
    limit, warn_line, page = int(W.get('limit')), int(W.get('budget_page')), int(W.get('bytes'))
    proj = int(pj.get('projected_bytes', 0))
    built = G['report'].get('built', '')
    try:
        bw = B1.words_when(datetime.datetime.fromisoformat(built))
    except ValueError:
        bw = built
    FILL.update({'page': f'{page:,}', 'built': bw})
    out = [f'<p class="intro">{esc(fill(S["lede"]))}</p>']
    unb = pj.get('unbuilt') or {}
    p4 = sorted({int(v) for k, v in unb.items() if k not in ('27', '28')})
    each = f'{p4[0]:,}' if len(p4) == 1 else join_words(f'{v:,}' for v in p4)
    rm = phase4_room(G)
    alloc = (FIG.get('phase4') or {}).get('allocations', {}).get('total')
    with_alloc = page + rm['held'] + rm['phase5'] + alloc if alloc else None
    rows = [(S['rows']['page_limit'], page, limit), (fill(S['rows']['proj_limit'], {'each': each}), proj, limit),
            (fill(S['rows']['proj_warn'], {'each': each}), proj, warn_line)]
    if with_alloc:
        rows += [(S['rows']['alloc_limit'], with_alloc, limit), (S['rows']['alloc_warn'], with_alloc, warn_line)]
        said = re.search(r'the page projects to ([\d,]+) bytes', B1.md_section(report_section(R, 9) or '', ['Page weight']) or '')
        if said and int(said.group(1).replace(',', '')) != with_alloc:
            warn(f'the report projects the page with its allocations at {said.group(1)} bytes, and the board at {with_alloc:,}')
    rows.append((S['rows']['ch14'], with_kit, stop))
    if kit_fig:
        rows.append((S['rows']['kit'], kit, kit_fig))
    out.append(bar_table(rows, S['cols'], S['top_caption']))
    crow = [(fill(S['chapter_14_word'] if k == '14' else S['chapter_word'], {'n': k, 'pct': f'{100 * with_kit / stop:.1f}' if stop else '?'}), int(v['bytes']),
             int(v['budget']) if v.get('budget') else None) for k, v in sorted(ch.items())]
    out.append(f'<h3 class="sub">{esc(S["chapters_h"])}</h3>' + bar_table(crow, S['cols'], S['chapters_caption']))
    out.append(f'<h3 class="sub">{esc(S["room_h"])}</h3><p>{esc(fill(S["room_line"], {"free": f"{rm["free"]:,}", "held": f"{rm["held"]:,}", "phase5": f"{rm["phase5"]:,}", "room": f"{rm["room"]:,}", "room_warn": f"{rm["room_warn"]:,}", "alloc": f"{alloc:,}" if alloc else "?"}))}</p>')
    FIG['weight'] = {'page': page, 'limit': limit, 'warn_line': warn_line, 'projected': proj, 'projected_with_allocations': with_alloc, 'phase4_each_in_projection': p4, 'ch14_with_kit': with_kit, 'ch14_stop': stop, 'kit': kit,
                     'kit_figure': kit_fig, 'chapters': {k: v for k, v in ch.items()}, 'phase4_room': rm}
    return section('weight', ''.join(out), 'ready')


# ------------------------------------------------------------------------------------------------------- panel 7
def tested_panel(G, R):
    S = C['sections']['tested']
    rows, missing = [], []
    for it in S['tested']:
        kind, w = it.get('kind'), None
        if kind == 'build':
            rep = G['report']
            if rep:
                try:
                    when = B1.words_when(datetime.datetime.fromisoformat(rep.get('built', ''))) + ' at ' + rep['built'][11:16] + ' UTC'
                except (ValueError, KeyError):
                    when = rep.get('built', '')
                w = fill(it['words'], {'bytes': f'{rep.get("bytes", 0):,}', 'warnings': nw(len(rep.get('warnings', []))), 'rules': rep.get('rules'),
                                       'specimens': rep.get('specimens_placed'), 'when': when})
        elif kind == 'check_file':
            p = scratch_path(C['slots'].get(it['slot']))
            if p and p.is_file():
                J = json.loads(p.read_text())
                runs = J.get('runs') if isinstance(J.get('runs'), list) else []
                widths = [str(r.get('width')) for r in runs if r.get('width')]
                r0 = runs[0] if runs else {}
                fl = J.get('failures', [])
                nf = fl if isinstance(fl, int) else len(fl or [])
                extra = {}
                if it.get('window'):
                    m = read_fact({'name': it['label'] + ' window', **it['window']})
                    extra = {'start': m.group(1), 'end': m.group(2)} if m else {}
                ck = J.get('checked', '')
                w = fill(it['words'], {'widths': join_words(widths) or '?', 'failures': nw(nf), 'checked': ck[11:16] if len(ck) > 16 else ck,
                                       'specimens': f'{(r0.get("specimens") or {}).get("stages", 0):,}', 'links': f'{(r0.get("anchors") or {}).get("links", 0):,}',
                                       'pass': 'passes' if J.get('pass') else 'fails', **extra})
                FIG.setdefault('checks_read', {})[it['slot']] = {'file': rel(p), 'failures': J.get('failures'), 'pass': J.get('pass')}
        elif kind == 'count':
            p = scratch_path('[scratch]/' + it['scratch_file'])
            if p and p.is_file():
                t = p.read_text()
                w = fill(it['words'], {'pass': len(re.findall(it['pass'], t, flags=re.M)), 'fail': nw(len(re.findall(it['fail'], t, flags=re.M)), 'none')})
                FIG.setdefault('checks_read', {})[it['label']] = {'file': rel(p), 'words': w}
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
            p = BOARD_DIR / f'{DATE}_Gate-3-Board-Check-Results.json'
            if p.exists():
                J = json.loads(p.read_text())
                fails = [f for f in J.get('failures', []) if 'html-has-lang' not in f]
                w = fill(it['words'], {'widths': join_words([str(r.get('width')) for r in J.get('runs', []) if r.get('width')]), 'failures': nw(len(fails))})
        else:
            parts = []
            for s in it.get('sources', []):
                m = read_fact({'name': it['label'], **s})
                if m:
                    parts.append(re.sub(r'\{(\d)\}', lambda x: m.groups()[int(x.group(1)) - 1], s['words']))
            w = '; '.join(parts) if parts and len(parts) == len(it.get('sources', [])) else None
        if w is None:
            missing.append(it.get('owner', 'main'))
            w = S['wait_words']
        rows.append(f'<li><b>{esc(it["label"])}:</b> {esc(w if w.endswith(".") else w + ".")}</li>')
        FIG.setdefault('tested', {})[it['label']] = w
    # Not tested: the report's own list (section 7), then the board's
    sec7 = report_section(R, 7) or ''
    nt = B1.md_section(sec7, [r'Not tested']) or ''
    items = B1.md_items(nt)
    if not items:
        warn('the Gate 3 report’s Not tested list is empty or missing')
    nots = ''.join(f'<li>{quoted(x)}</li>' for x in items)
    nots_b = ''.join(f'<li>{esc(fill(x))}</li>' for x in S['not_tested_board'])
    body = (f'<p class="intro">{esc(S["lede"])}</p><div class="tcols">'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["tested_h"])}</h3><ul>{"".join(rows)}</ul></div>'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["not_h"])}</h3><ul>{nots}</ul><p class="label tb">{esc(S["board_not_h"])}</p><ul>{nots_b}</ul></div></div>')
    return section('tested', body, 'ready' if not missing else ('partial', missing[0]))


# ------------------------------------------------------------------------------------------------------- page
ORDER = ['decide', 'phase4', 'answers', 'clearance', 'scores', 'weight', 'tested']


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
CSS += r'''
.ul{margin:var(--oa-space-100) 0 var(--oa-space-200);padding-left:1.2em;font:var(--oa-type-body-small);max-width:var(--oa-layout-measure-intro-max)}
.ul li{margin-bottom:var(--oa-space-050)}
table.dt.at{min-width:48rem}
table.dt.at .track{min-width:10rem}
table.scores.sb{min-width:36rem}
ul.nones{list-style:none;margin:0;padding:0;border-top:var(--oa-border-width-rule) solid var(--strong);max-width:var(--oa-layout-measure-intro-max)}
ul.nones li{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair);font:var(--oa-type-body-small)}
ul.nones .tag{margin-right:var(--oa-space-100)}
.luma-h{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:var(--oa-space-400) 0 0}
.rl a{display:inline-flex;align-items:center;min-height:2.75rem}
.tb{margin-top:var(--oa-space-300)}
.swf{margin:var(--oa-space-300) 0}
.swf figcaption{font:var(--oa-type-caption);color:var(--ink-2);margin-bottom:var(--oa-space-100);max-width:var(--oa-layout-measure-intro-max)}
.sw-ground{list-style:none;margin:0;padding:var(--oa-space-300);display:flex;flex-wrap:wrap;gap:var(--oa-space-300) var(--oa-space-500);background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);max-width:var(--oa-layout-measure-intro-max)}
.sw-ground li{flex:1 1 12rem;min-width:0}
.sw{display:block;width:96px;height:56px}
.sw-t{display:block;font:var(--oa-type-body-small);margin-top:var(--oa-space-100)}
table.dt.ww{min-width:44rem}
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
    css = strip_css(CSS + '\n'.join(dict.fromkeys(SWATCH_CSS)))
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
    for where, t in (('text', text), ('alt text', alts)):
        i = t.find('—')
        if i >= 0:
            warn('an em dash in the board’s ' + where + ': ' + t[max(0, i - 60):i + 20])
    vis = visible_text(re.sub(r'<code>.*?</code>', ' ', page, flags=re.S))
    straight = re.findall(r".{0,30}['\"].{0,10}", vis)
    if straight:
        warn('straight quotes or apostrophes on the board: ' + ' | '.join(x.strip() for x in straight[:4]))
    own_page = page
    for q in sorted({q for q in QUOTED if q}, key=len, reverse=True):
        for frag in (B1.md_inline(q), B1.md_inline(q, quote=False), esc(q)):
            own_page = own_page.replace(frag, ' ')
    own = visible_text(own_page)
    B1.MOVED.clear()
    if '–' in own:
        i = own.find('–')
        warn('an en dash in the board’s own words: ' + own[max(0, i - 40):i + 20])
    for leftover in re.findall(r'\{[a-z0-9_]+\}', visible_text(page)):
        warn(f'an unfilled field on the board: {leftover}')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', own, flags=re.I)})
    if flagged:
        warn('flagged words in the board’s own words: ' + ', '.join(flagged))
    face_all = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))
    stray = set(re.findall(r'\b' + CODE_DEC + r'\b', face_all))
    if stray:
        warn('decision codes on the board’s face: ' + ', '.join(sorted(stray)))
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
    ids = re.findall(r'\sid="([^"]+)"', page)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        warn('ids used twice on the board: ' + ', '.join(dup[:6]))
    for a in re.findall(r'href="#([^"]+)"', page):
        if a not in ids:
            warn(f'a link on the board to #{a}, which the board does not hold')
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
                    'wrapped': {'failures': fails2, 'pass': J2.get('pass'), 'results': '[scratch]/c09/builder/publish-view/' + wrapped.stem + '-Check-Results.json'},
                    'widths': [x.get('width') for x in J2.get('runs', [])]}
    if other:
        warn('the board check failed: ' + '; '.join(other[:6]))
    if fails2:
        warn('the wrapped board check failed: ' + '; '.join(fails2[:6]))
    return not other and not fails2


def main():
    global C, LOG, SCRATCH, CACHE, NO_BROWSER, PREVIEW_IDS
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--reuse', action='store_true', help='keep photographs and the kit’s export whose sources have not changed')
    ap.add_argument('--check', action='store_true', help='run dataviz_check.js --board on the board and on a wrapped copy')
    ap.add_argument('--strict', action='store_true', help='exit 1 on any warning')
    ap.add_argument('--scratch', type=pathlib.Path, default=SCRATCH_DEFAULT)
    ap.add_argument('--out', type=pathlib.Path, default=OUT)
    ap.add_argument('--final', type=pathlib.Path, help='the final build’s page (else the content file’s slots.final_page)')
    ap.add_argument('--final-report', type=pathlib.Path, help='its build report (else slots.final_report, else beside the page)')
    ap.add_argument('--no-browser', action='store_true', help='open no browser: build from the photographs already in scratch')
    a = ap.parse_args()
    NO_BROWSER = a.no_browser
    SCRATCH = a.scratch
    SCRATCH.mkdir(parents=True, exist_ok=True)
    os.environ['TMPDIR'] = str(SCRATCH)
    raw = CONTENT.read_text()
    if '—' in raw:
        warn('the content file holds an em dash')
    C = json.loads(raw)
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
    G = load_pages(a.final.resolve() if a.final else None, a.final_report.resolve() if a.final_report else None)
    if G['usable']:
        PREVIEW_IDS = set(re.findall(r'\sid="([^"]+)"', G['text']))
    R = report_text()
    FIG['report'] = {'file': C['slots']['report'], 'bytes': len(R.encode()), 'placeholders': sorted(set(re.findall(r'\{[A-Z_0-9]+\}', R)))}
    # 1. what to photograph, in the brief's priority order: panel 3's cards in reply order, then panel 4's pair
    S3 = C['sections']['answers']
    pics = [p for c in sorted(S3['cards'], key=lambda x: x['n']) for p in (c.get('pictures') or [])] + C['sections']['clearance']['pictures']
    items = picture_items(pics)
    kit_dirs = {}
    for p in pics:
        if p.get('kind') == 'export':
            if p['spec'] not in kit_dirs:
                kit_dirs[p['spec']] = kit_export(p['spec'], a.reuse)
            ei = export_item(p, kit_dirs[p['spec']])
            if ei:
                items.insert(0, ei)
            else:
                warn(f'no export of {p["spec"]} for {p["id"]}')
    FIG['photographs_asked'] = len(items)
    shots = run_shots(items, a.reuse) if G['usable'] else {}
    # 2. the panels
    s_decide, n_items = decide_panel(R, G)
    w1 = panel_words(s_decide)
    FILL.update({'p1_words': f'{w1:,}', 'p1_min': f'{nw(max(1, round(w1 / 200)))} minute' + ('' if max(1, round(w1 / 200)) == 1 else 's')})
    FIG['panel_1_words'] = w1
    s_phase4 = phase4_panel(R, G)
    s_answers = answers_panel(shots)
    s_clear = clearance_panel(shots)
    s_scores = scores_panel(R)
    s_weight = weight_panel(G, R)
    s_tested = tested_panel(G, R)
    parts = [s_decide, s_phase4, s_answers, s_clear, s_scores, s_weight, s_tested]
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
    if len(imgs) >= FILES_AIM:
        warn(f'the board shows {len(imgs)} pictures, at or past the brief’s 120')
    if total >= BYTES_AIM:
        warn(f'the folder comes to {total / 1e6:.2f} MB, at or over 30 MB')
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
        FIG.update({'folder_files': len(files), 'folder_bytes': sum(p.stat().st_size for p in files), 'warnings': WARN, 'html_bytes': len(page.encode())})
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
