"""Build the round 2 progress page of Phase 3 (November 12, 2026; the page builder, working as the design director).

Adapted from progress_round_1_build.py, which stays as it is. Usage:
    python3 -I work/build/scripts/phase-3/progress_round_2_build.py [--reuse] [--check] [--strict] [--scratch DIR] [--out PATH]

Reads, on every run:
    work/boards/phase-3/round-2/progress/20261112_Round-2-Progress-Content.json   the page's own words and the files it reads
    work/handoffs/phase-3/20261112_Chapter-14-Plan.json         round 2's forms, their rules, makers, families and states
    a fresh strict build of the guide (guide_build.py --strict --out <scratch>/guide/), for every guide picture, each
    chart's printed title and evidence label, the wide stage's width at 1024 and 768 px, and the weights in its report
    the chart kit's own captures, built afresh into <scratch>/kit-out/ by oa-chart.mjs (one folder per chart)
    work/build/guide/chapters/14-data-visualization.json and 15-systems-graphics.json (rules, plates, captions), the rule
    plates' chart files and chapter 13's chart files in work/build/guide/specimens/ (round 1's carried items)
    work/boards/phase-3/round-1/progress/20261112_Round-1-Progress-Figures.json   which chapter 15 rules round 1 built
    work/handoffs/phase-3/20261112_Round-4-Data-Plan.md, work/build/data/ and the research ledger (round 4's frozen data)
    the creative director's scores and the newest *Round-2-CD-Rescore*.json, the three red team reports, the guide check
    results files in the session's scratch folder, and the notes files the content file names for part 10
    work/build/tokens/tokens.css (the :root tokens the page's styles name, and only those)
    work/ledger/*_Decision-Log.md and *_Open-Questions.md      every code in a reference line must exist
Writes:
    work/boards/phase-3/round-2/progress/20261112_Round-2-Progress.html            the page (no scripts; the host wraps it)
    work/boards/phase-3/round-2/progress/img/                                      every picture it shows, composed
    work/boards/phase-3/round-2/progress/20261112_Round-2-Progress-Figures.json    every figure it prints, with its source
    work/boards/phase-3/round-2/progress/20261112_Round-2-Progress-Check-Results.json  (written by dataviz_check.js)
    <scratch>/  the guide build, the kit's builds, the photographs, the measurements and the composition cache

--reuse keeps a kit capture when its spec, data, form module and the kit's shared files are unchanged, and a guide
photograph or measurement when its element's HTML, the page's styles and scripts and the window width are unchanged;
without it, every capture and photograph is made afresh. --check runs dataviz_check.js with --board --no-captures, from
work/build, twice: on the page itself, whose results file lands beside it, and on a copy in the scratch folder wrapped as
the host wraps it (doctype, <html lang="en">, charset and viewport). The page carries no <html> tag by its contract, so
axe's html-has-lang is the one failure allowed on the page itself; the wrapped copy must pass every check. Either failing
otherwise fails the build. --strict exits 1 on any warning. A part whose file is missing or still pending prints
"Waiting for". Images the page no longer names are removed from img/ on every run.
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

ROOT = pathlib.Path(__file__).resolve().parents[4]
SCRIPTS2 = ROOT / 'work/build/scripts/phase-2'
SCRIPTS3 = ROOT / 'work/build/scripts/phase-3'
sys.path.insert(0, str(SCRIPTS3))
import board_1_build as B1  # noqa: E402   board 1's Markdown readers, quoted-words rules (D3-206) and Tested-list reader

DATE = '20261112'
PAGE_DIR = ROOT / 'work/boards/phase-3/round-2/progress'
IMG = PAGE_DIR / 'img'
CONTENT = PAGE_DIR / f'{DATE}_Round-2-Progress-Content.json'
FIGURES = PAGE_DIR / f'{DATE}_Round-2-Progress-Figures.json'
OUT = PAGE_DIR / f'{DATE}_Round-2-Progress.html'
SCRATCH_DEFAULT = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2/progress-page')
LABEL_FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
NEWSPRINT = (0xDC, 0xD9, 0xD2)
LABEL_INK = (0x4E, 0x53, 0x5B)
CONTENT_W = 1280          # the widest picture that sits in the page's column at a 1440 px window with no frame scroll
REGION_W = 288            # a picture wider than a 320 px window's column scrolls in its own named frame
LIMIT_FILES = 200
LIMIT_TOTAL = 50_000_000
LIMIT_IMAGE = 15_000_000
LIMIT_PAGE = 16_000_000
FLAGGED = B1.FLAGGED
CODE_DEC = B1.CODE_DEC
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp')

C = {}
LOG = set()
SCRATCH = SCRATCH_DEFAULT
WARN, NOTES, FIG, QUOTED, LINKED = [], [], {}, [], set()
FILL = {}
IMAGES = {}
STATUS = {}
CACHE = {}
G_OK = False              # the strict build passed; a part that reads the guide is Ready only then
ACCEPT_FAILED = False     # --photos-from-failed-build: photograph a strict build that failed, to prove the method


class PageError(Exception):
    pass


def warn(msg):
    WARN.append(msg)
    print('warning', msg)


def need(cond, msg):
    if not cond:
        raise PageError(msg)


esc = B1.esc
nw = B1.nw
cap = B1.cap
join_words = B1.join_words


def rel(p):
    p = pathlib.Path(p)
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p).replace(str(SCRATCH), '[scratch]')


def read(p):
    p = ROOT / p
    return p.read_text() if p.exists() else None


def fill(s, extra=None):
    d = dict(FILL)
    if extra:
        d.update(extra)
    return re.sub(r'\{([a-z0-9_]+)\}', lambda m: str(d[m.group(1)]) if m.group(1) in d else m.group(0), s)


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


# ------------------------------------------------------------------------------------------------------- the guide
def guide_build():
    d = SCRATCH / 'guide'
    d.mkdir(parents=True, exist_ok=True)
    page = d / f'{DATE}_Progress-Guide.html'
    rep = d / f'{DATE}_Progress-Guide-Build-Report.json'
    for p in (page, rep):
        if p.exists():
            p.unlink()
    r = subprocess.run([sys.executable, '-I', str(ROOT / C['slots']['guide_build']), '--strict', '--out', str(page)], cwd=ROOT,
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    (SCRATCH / 'guide-build.log').write_text(r.stdout + r.stderr)
    ok = r.returncode == 0 and page.exists() and rep.exists()
    if not ok:
        warn(f'the strict guide build failed (exit {r.returncode}); the guide pictures wait for a passing build')
    report = json.loads(rep.read_text()) if rep.exists() else {}
    text = page.read_text() if page.exists() else ''
    usable = ok or (ACCEPT_FAILED and page.exists() and rep.exists())
    if usable and not ok:
        warn('the page’s pictures come from a strict build that failed; a method run only, never one to publish')
    FIG['guide_build'] = {'exit': r.returncode, 'bytes': report.get('bytes'), 'rules': report.get('rules'),
                          'specimens': report.get('specimens_placed'), 'warnings': len(report.get('warnings', [])), 'built': report.get('built'),
                          'pictures_from_failed_build': usable and not ok}
    global G_OK
    G_OK = ok
    return {'ok': ok, 'usable': usable, 'page': page, 'text': text, 'report': report, 'mtime': page.stat().st_mtime if page.exists() else None}


def element_html(page, el_id):
    """The source of the element with this id, its own tag balanced, so a picture's signature changes only when it does."""
    i = page.find(f'id="{el_id}"')
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


def page_frame_sig(page):
    """Every style and script of the guide page that is not a data island: what draws every element."""
    parts = re.findall(r'<style\b[^>]*>(.*?)</style>', page, flags=re.S)
    parts += re.findall(r'<script\b(?![^>]*(?:application/json|data-oa-chart-data))[^>]*>(.*?)</script>', page, flags=re.S)
    return sha(*parts)


# ------------------------------------------------------------------------------------------------------- the kit
KIT_SHARED = ['kit.js', 'parts.js', 'kit.css', 'metrics.js', 'geo.js', 'words.json', 'checks.js', 'oa-chart.mjs', 'tools/minify.mjs']


def kit_sig(sid, shared):
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
    return sha(shared, *[rel(f).encode() + b'\0' + f.read_bytes() for f in files])


def kit_build(ids, reuse):
    """The kit's own captures, one folder per chart under <scratch>/kit-out, rebuilt where the chart's sources changed."""
    S = C['slots']
    out = SCRATCH / 'kit-out'
    out.mkdir(parents=True, exist_ok=True)
    sig_file = SCRATCH / 'kit-sigs.json'
    sigs = json.loads(sig_file.read_text()) if sig_file.exists() else {}
    kd = ROOT / S['kit_dir']
    shared = sha(*[(kd / f).read_bytes() for f in KIT_SHARED if (kd / f).exists()], (ROOT / S['tokens_css']).read_bytes())
    want, todo = {}, []
    for sid in ids:
        lo = sid.lower()
        want[sid] = kit_sig(sid, shared)
        have = all((out / lo / f'{lo}-{g}-{w}.png').exists() for g in ('newsprint', 'charcoal') for w in (1440, 390)) and (out / lo / f'{lo}-check.json').exists()
        if not (reuse and have and sigs.get(sid) == want[sid]):
            todo.append(sid)
    if todo:
        print(f'building {len(todo)} charts with the kit ...')
        for sid in todo:
            shutil.rmtree(out / sid.lower(), ignore_errors=True)
        r = subprocess.run(['node', str(ROOT / S['kit_command']), 'build', *[s.lower() for s in todo], '--out', str(out)], cwd=ROOT,
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        (SCRATCH / 'kit-build.log').write_text(r.stdout + r.stderr)
        for sid in todo:
            if (out / sid.lower() / f'{sid.lower()}-check.json').exists():
                sigs[sid] = want[sid]
            else:
                warn(f'the kit made no check file for {sid}: ' + (r.stderr or r.stdout)[-200:])
        sig_file.write_text(json.dumps(sigs, indent=1))
    FIG['kit_builds'] = {'rebuilt': todo, 'reused': [s for s in ids if s not in todo]}
    return out


# ------------------------------------------------------------------------------------------------------- photographs
def run_shots(G, items, reuse):
    """items: [(key, element id, width)] or [(key, element id, width, 'measure')] -> {key: path}. A measure item takes no
    picture; its file holds the plate stage's width at that window (the renderer's docstring). One page load per width,
    only for the items that changed; a width with only measure items loads the page without drawing its charts."""
    shots = SCRATCH / 'shots'
    shots.mkdir(parents=True, exist_ok=True)
    sig_file = SCRATCH / 'shot-sigs.json'
    sigs = json.loads(sig_file.read_text()) if sig_file.exists() else {}
    frame = page_frame_sig(G['text'])
    paths, todo = {}, {}
    for key, el, w, *kind in items:
        measure = bool(kind and kind[0] == 'measure')
        p = shots / (f'{key}.json' if measure else f'{key}.png')
        paths[key] = p
        src = element_html(G['text'], el)
        if src is None:
            warn(f'the guide holds no element #{el}')
            continue
        s = sha(frame, w, src, 'measure' if measure else 'picture')
        if reuse and p.exists() and sigs.get(key) == s:
            continue
        todo.setdefault(w, []).append((key, el, s, p, measure))
    jobs = [{'file': str(G['page']), 'width': w, 'height': 900 if w > 600 else 844, 'static_sticky': True,
             'draw_all': not all(x[4] for x in its),
             'items': [{'selector': f'#{el}', 'out': str(p), 'measure': m} for key, el, s, p, m in its]} for w, its in sorted(todo.items(), reverse=True)]
    if jobs:
        print(f'photographing or measuring {sum(len(j["items"]) for j in jobs)} elements of the guide ...')
        for its in todo.values():
            for key, el, s, p, m in its:
                if p.exists():
                    p.unlink()
        jp = SCRATCH / 'render-jobs.json'
        jp.write_text(json.dumps(jobs))
        r = subprocess.run(['node', str(SCRIPTS3 / 'progress_round_2_render.js'), str(jp)], cwd=ROOT / 'work/build',
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        (SCRATCH / 'render.log').write_text(r.stdout + r.stderr)
        for line in r.stdout.splitlines():
            if line.startswith('failed') or line.startswith('page error'):
                warn('render: ' + line)
        if r.returncode != 0 and 'failed' not in r.stdout:
            warn('the renderer stopped: ' + r.stderr[-300:])
        for its in todo.values():
            for key, el, s, p, m in its:
                if p.exists():
                    sigs[key] = s
        sig_file.write_text(json.dumps(sigs, indent=1))
    FIG['shots'] = {'taken': sorted(k for its in todo.values() for k, *_ in its), 'reused': sorted(k for k in paths if all(k != x[0] for its in todo.values() for x in its))}
    return paths


# ------------------------------------------------------------------------------------------------------- pictures
def png_size(p):
    return B1.png_size(p)


def compose(name, parts, cols=None, gap=24, label_h=26):
    """One picture of one or more, each part at its true size on whole pixels, its label set in Inter Medium at 13 px
    above it (D3-196), saved as a PNG with lossless compression. parts: [(path, label)]."""
    from PIL import Image, ImageDraw, ImageFont
    out = IMG / f'{DATE}_{name}.png'
    for p, _ in parts:
        need(pathlib.Path(p).exists(), f'missing picture {rel(p)} for {name}')
    if not any(lab for _, lab in parts):
        label_h = 0
    sig = sha(json.dumps([[str(p), file_sig(p), lab] for p, lab in parts] + [cols, gap, label_h, 'v2']))
    if out.exists() and CACHE.get(out.name) == sig:
        w, h = png_size(out)
    else:
        ims = [Image.open(p) for p, _ in parts]
        conv = []
        for im in ims:
            if im.mode in ('RGBA', 'LA', 'P'):
                base = Image.new('RGBA', im.size, NEWSPRINT + (255,))
                base.alpha_composite(im.convert('RGBA'))
                conv.append(base.convert('RGB'))
            else:
                conv.append(im.convert('RGB'))
        cols = cols or len(conv)
        rows = [conv[i:i + cols] for i in range(0, len(conv), cols)]
        col_w = [max(r[k].size[0] for r in rows if k < len(r)) for k in range(cols)]
        row_h = [max(im.size[1] for im in r) for r in rows]
        W = sum(col_w) + gap * (cols - 1)
        H = sum(h + label_h for h in row_h) + gap * (len(rows) - 1)
        canvas = Image.new('RGB', (W, H), NEWSPRINT)
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype(LABEL_FONT, 13)
        y = 0
        for r, row in enumerate(rows):
            x = 0
            for k, im in enumerate(row):
                lab = parts[r * cols + k][1]
                if lab:
                    draw.text((x, y + 4), lab, font=font, fill=LABEL_INK)
                canvas.paste(im, (x, y + label_h))
                x += col_w[k] + gap
            y += row_h[r] + label_h + gap
        canvas.save(out, 'PNG', optimize=True)
        CACHE[out.name] = sig
        w, h = W, H
    rec = {'src': f'img/{out.name}', 'file': out, 'w': w, 'h': h, 'source': ', '.join(rel(p) for p, _ in parts)}
    IMAGES[out.name] = rec
    return rec


def frame(rec, alt, lazy=True):
    w, h = rec['w'], rec['h']
    region = w > REGION_W
    attrs = f' role="region" tabindex="0" aria-label="{esc(alt)}, {w} by {h} px; scrolls sideways when wider than the window"' if region else ''
    ld = ' loading="lazy"' if lazy else ''
    return (f'<div class="frame"{attrs}><img src="{rec["src"]}" width="{w}" height="{h}" alt="{esc(alt)}"{ld} decoding="async"></div>')


def figure(rec, alt, cap_html='', lazy=True):
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


def section(key, body, status):
    P = C['sections'][key]
    if status == 'ready' and not G_OK and key not in ('scores', 'next'):
        status = ('partial', 'build')
    STATUS[key] = status
    return (f'<section class="sec" id="p-{key}" aria-labelledby="h-{key}"><div class="sec-top"><p class="label">Part {P["n"]}</p>{chip(status)}</div>'
            f'<h2 class="sec-h" id="h-{key}">{esc(fill(P["title"]))}</h2>{body}{refs_line(P.get("refs", ""), "part " + key)}</section>')


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
    rn = [f for f in P['forms'] if f.get('round') == C['round']]
    need(rn, f'the plan holds no rows for round {C["round"]}')
    return P, rn


def data_freeze():
    """Round 4's data, read from its plan's table "Datasets to fetch and freeze" (each line's files and the rows they
    serve) against the files in the data folder: a file is frozen when it and its sidecar are there, and a row when every
    file it needs is. The new files are those whose sidecar's ledger row comes at or after the row the plan's section
    names first ("from P7-301 on"); each of their rows must stand in the research ledger."""
    t = read(C['slots']['data_plan']) or ''
    sec = B1.md_section(t, [r'datasets to fetch and freeze']) or ''
    dd = ROOT / C['slots']['data_dir']
    need_rows, stems_all = {}, []
    for head, body in B1.md_tables(sec):
        if not head or not head[0].startswith('Dataset') or 'Rows' not in head:
            continue
        k_rows = head.index('Rows')
        for r in body:
            stems = [s for s in re.findall(r'`([a-z0-9-]+)`', r[0]) if not s.startswith('-')]
            rows = []
            for a, b in re.findall(r'(\d+)(?:\s+to\s+(\d+))?', r[k_rows] if k_rows < len(r) else ''):
                rows += list(range(int(a), int(b) + 1)) if b else [int(a)]
            for s in stems:
                stems_all.append(s)
                have = any((dd / f'{s}{e}').exists() for e in ('.csv', '.json')) and (dd / f'{s}.meta.json').exists()
                for n in rows:
                    need_rows.setdefault(n, []).append((s, have))
    if not need_rows:
        warn('the round 4 data plan’s table "Datasets to fetch and freeze" was not found')
    m = re.search(r'from (P7-(\d+)) on', sec)
    first = int(m.group(2)) if m else None
    if first is None:
        warn('the round 4 data plan does not say which ledger row its files start from')
    ledger = read(C['slots']['research_ledger']) or ''
    stems_u = list(dict.fromkeys(stems_all))
    have = [s for s in stems_u if all(h for x, h in sum(need_rows.values(), []) if x == s)]
    new, rows_new = [], []
    for s in have:
        side = json.loads((dd / f'{s}.meta.json').read_text())
        lr = str(side.get('ledger_row', ''))
        mm = re.fullmatch(r'P7-(\d+)', lr)
        if first is not None and mm and int(mm.group(1)) >= first:
            new.append(s)
            rows_new.append(lr)
            if not re.search(r'^\|\s*' + re.escape(lr) + r'\s*\|\s*' + re.escape(s) + r'\s*\|', ledger, flags=re.M):
                warn(f'{lr} for {s} is not a row of the research ledger')
    rows_new.sort(key=lambda x: int(x.split('-')[1]))
    frozen_rows = sorted(n for n, xs in need_rows.items() if all(h for _, h in xs))
    waiting = sorted(n for n in need_rows if n not in frozen_rows)
    FIG['round4'] = {'data_rows': len(need_rows), 'frozen_rows': len(frozen_rows), 'waiting_rows': waiting, 'files_named': stems_u,
                     'files_frozen': have, 'new_files': new, 'ledger_rows': rows_new}
    return {'rows': len(need_rows), 'frozen': len(frozen_rows), 'waiting': waiting, 'named': len(stems_u), 'have': len(have),
            'new': len(new), 'ledger': rows_new}


def ledger_span(rows):
    """P7-301 ... P7-310, every row in between present -> "P7-301 to P7-310"."""
    if not rows:
        return ''
    ns = [int(r.split('-')[1]) for r in rows]
    if ns == list(range(ns[0], ns[0] + len(ns))) and len(ns) > 2:
        return f'{rows[0]} to {rows[-1]}'
    return join_words(rows)


def round1_ch15():
    """The chapter 15 rules round 1 built, as round 1's page recorded them."""
    p = ROOT / C['slots']['round1_figures']
    if not p.exists():
        warn('round 1’s figures file is missing, so chapter 15’s new rules cannot be told apart')
        return []
    return json.loads(p.read_text()).get('round', {}).get('ch15_rules', [])


def new_ch15(ch15):
    done = set(round1_ch15())
    return [r for r in ch15['rules'] if r['id'] not in done]


def wide_plates(G, rules, opener=None):
    """The chapter 15 plates the guide sets on the wide stage (data-wide on the frame), in the chapter's order, the
    opening plate first when it is given."""
    out = []
    if opener:
        m = re.search(r'data-wide="(\d+)"', element_html(G['text'], f'fig-{opener}') or '')
        if m:
            out.append(('opener', 'opener', opener, int(m.group(1))))
    for r in rules:
        for k in ('correct', 'failure'):
            sp = (r.get(k) or {}).get('specimen') if isinstance(r.get(k), dict) else None
            src = element_html(G['text'], f'fig-{sp}') if sp else None
            m = re.search(r'data-wide="(\d+)"', src or '')
            if m:
                out.append((r['id'], k, sp, int(m.group(1))))
    return out


def carried(G, P, ch14, shots):
    """Round 1's carried items, each read from the file that shows it done, as (label, words, done)."""
    S = C['sections']['round']['carried']
    spec_dir = ROOT / C['slots']['plate_specs_dir']
    forms = {f.get('form_id'): f for f in P['forms']}
    out = []
    # Rule 14.9's correct plate on the interval form
    r = C['carried']['interval_rule']
    files = sorted(spec_dir.glob(f's-14-{r.split(".")[1]}-*.chart.json'))
    plate = read(f'{C["slots"]["plate_specs_dir"]}/s-14-{r.split(".")[1]}-correct.html') or ''
    hit = None
    for f in files:
        d = json.loads(f.read_text())
        if d.get('form') in forms and f.name.replace('.chart.json', '') in plate:
            hit = forms[d['form']]
    FIG.setdefault('carried', {})['interval'] = {'files': [rel(f) for f in files], 'form': hit.get('form_id') if hit else None}
    out.append((fill(S['interval_h'], {'r': r}),
                fill(S['interval'], {'r': r, 'form': hit['form'].lower(), 'form_rule': hit['rule']}) if hit else S['not_found'], bool(hit)))
    # Rule 14.3's red point
    r = C['carried']['point_rule']
    pt = None
    plate = read(f'{C["slots"]["plate_specs_dir"]}/s-14-{r.split(".")[1]}-correct.html') or ''
    for f in sorted(spec_dir.glob(f's-14-{r.split(".")[1]}-*.chart.json')):
        d = json.loads(f.read_text())
        lab = d.get('labels') or {}
        if lab.get('point') and f.name.replace('.chart.json', '') in plate:
            name = (lab.get('series') or {}).get(lab['point'], lab['point'])
            pt = (name, name.lower() in (d.get('title') or '').lower())
    FIG['carried']['point'] = pt
    out.append((fill(S['point_h'], {'r': r}),
                (fill(S['point'], {'r': r, 'name': pt[0]}) + (S['point_named'] if pt[1] else '')) if pt else S['not_found'], bool(pt)))
    # chapter 14's plate style, printed once
    parts = G['report'].get('weight', {}).get('chapter_14_parts', {})
    ok = bool(ch14.get('plate_css')) and bool(parts.get('plate_css'))
    FIG['carried']['plate_css'] = {'bytes': parts.get('plate_css'), 'rules_and_opener': parts.get('rules_and_opener'), 'allowance': parts.get('allowance')}
    out.append((S['style_h'], fill(S['style'], {'b': f'{parts.get("plate_css", 0):,}', 'ro': f'{parts.get("rules_and_opener", 0):,}',
                                                'al': f'{parts.get("allowance", 0):,}'}) if ok else S['not_found'], ok))
    # chapter 13's chart titles with a closing period
    files = sorted(spec_dir.glob('s-13-*.chart.json'))
    ends = [f for f in files if (json.loads(f.read_text()).get('title') or '').rstrip().endswith('.')]
    FIG['carried']['ch13_titles'] = {'files': [rel(f) for f in files], 'with_period': len(ends)}
    every = bool(files) and len(ends) == len(files)
    out.append((S['ch13_h'], fill(S['ch13_all'] if every else S['ch13_some'], {'k': nw(len(ends)), 'n': nw(len(files))}), every))
    # chapter 15's wide stage at 1024 and 768 px
    c15 = json.loads((ROOT / C['slots']['chapter15']).read_text())
    wides = wide_plates(G, c15['rules'], (c15.get('opener') or {}).get('specimen'))
    res = {}
    for w in C['carried']['wide_widths']:
        got = []
        for rid, k, sp, wide in wides:
            p = shots.get(f'wide-{sp}-{w}')
            if p and p.exists():
                m = json.loads(p.read_text())
                got.append(m.get('stage_w') is not None and abs(m['stage_w'] - wide) < 0.5)
        res[w] = (sum(got), len(got))
    FIG['carried']['wide_stage'] = {'plates': [f'{rid} {k}' for rid, k, *_ in wides], 'widths': {str(w): list(v) for w, v in res.items()}}
    ok = bool(wides) and all(v[0] == v[1] == len(wides) for v in res.values())
    ws = list(res)
    wide_w = wides[0][3] if wides else 0
    out.append((S['wide_h'], fill(S['wide'], {'k': 'all ' + nw(len(wides)) if ok else ' and '.join(f'{v[0]} of {v[1]}' for v in res.values()),
                                              'w1': ws[0] if ws else '', 'w2': ws[-1] if ws else '', 'px': wide_w})
                               if wides and all(v[1] for v in res.values()) else S['not_found'], ok))
    for lab, words, done in out:
        if not done:
            warn(f'round 1’s carried item “{lab}” is not shown done in its files')
    return out


def round_section(G, P, rn, shots):
    S = C['sections']['round']
    ch14 = json.loads((ROOT / C['slots']['chapter14']).read_text())
    ch15 = json.loads((ROOT / C['slots']['chapter15']).read_text())
    new = [f for f in rn if f['status'] == 'new']
    built = [f for f in rn if f['status'] == 'built']
    sk = [f for f in rn if f['status'] == 'sketch']
    held = {r['id']: r for r in ch14['rules']}
    entries = [f for f in rn if held.get(f['rule'], {}).get('entry')]
    if len(entries) != len(rn):
        warn(f'chapter 14 holds {len(entries)} of the plan’s {len(rn)} round {C["round"]} forms as entries')
    ids = sorted({f['spec_id'] for f in new}, key=lambda s: int(s[1:]))
    built_ids = [f['spec_id'] for f in built]
    r15 = new_ch15(ch15)
    p15 = sum(1 for r in r15 for k in ('correct', 'failure') if isinstance(r.get(k), dict))
    fams = list(dict.fromkeys(f['family_section'] for f in rn))
    D = data_freeze()
    rep = G['report']
    FILL.update({'n_entries': len(entries), 'n_new': len(new), 'n_built': len(built), 'n_sketch': len(sk), 'n_sketch_w': nw(len(sk)), 'new_first': ids[0], 'new_last': ids[-1],
                 'n15': len(r15), 'n15_w': nw(len(r15)), 'n15_plates': p15, 'n_fam_w': nw(len(fams))})
    sk_av = sum(1 for f in sk if (held.get(f['rule'], {}).get('correct') or {}).get('kind') == 'avoid')
    facts = [
        (S['facts']['entries'], f'{len(entries)}: {len(new)} new charts, {ids[0]} to {ids[-1]}; {nw(len(built))} charts already built, '
                                f'{join_words(built_ids)}, set in as entries; {len(sk)} sketches, {nw(sk_av)} of them forms to avoid'),
        (S['facts']['ch15'], f'{cap(nw(len(r15)))} new rules, {join_words(compact_ids([r["id"] for r in r15]))}, with {p15} plates'),
        (S['facts']['data'], (f'Frozen with their sidecars: {nw(D["new"])} new tables, research ledger rows {ledger_span(D["ledger"])}; '
                              f'{"all " + nw(D["rows"]) if D["frozen"] == D["rows"] else str(D["frozen"]) + " of " + str(D["rows"])} of its data rows have every file in the data folder'
                              + (f'. Waiting: rows {join_words([str(n) for n in D["waiting"]])}' if D['waiting'] else ''))),
    ]
    car = carried(G, P, ch14, shots)
    facts += [(a, b) for a, b, _ in car]
    if G['ok']:
        FILL['build_when'] = when_utc(G['mtime'])
        facts.append((S['facts']['build'], f'{rep.get("bytes", 0):,} bytes, {rep.get("rules", 0)} rules, {rep.get("specimens_placed", 0)} examples, '
                                           f'{nw(len(rep.get("warnings", [])))} warnings, from a strict build on {FILL["build_when"]}'))
    else:
        facts.append((S['facts']['build'], 'The strict build did not pass; see its log.'))
    FIG['round'] = {'entries': len(entries), 'new': len(new), 'built': built_ids, 'sketches': len(sk), 'avoid': sk_av, 'new_ids': ids,
                    'families': fams, 'ch15_rules': [r['id'] for r in r15], 'ch15_plates': p15}
    body = (f'<dl class="facts">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in facts) + '</dl>'
            f'<p class="nodec">{esc(C["cover"]["no_decision"])}</p>')
    done = all(d for _, _, d in car)
    return section('round', body, 'ready' if G['ok'] and done else ('partial', 'build' if not G['ok'] else 'render'))


def compact_ids(ids):
    """15.11, 15.12, 15.15, 15.16, 15.17, 15.18 -> ['15.11', '15.12', '15.15 to 15.18'] for a sentence."""
    out, run = [], []
    for x in ids + [None]:
        if x and run and x.split('.')[0] == run[-1].split('.')[0] and int(x.split('.')[1]) == int(run[-1].split('.')[1]) + 1:
            run.append(x)
            continue
        if run:
            out.extend([f'{run[0]} to {run[-1]}'] if len(run) > 2 else run)
        run = [x] if x else []
    return out


def printed_title(G, sid):
    """The title the guide prints over the chart, or, for a form that draws its one sentence in place of a title (the
    one-sentence form), the spec's title, which is that sentence. None when the chart is not in the guide."""
    fig = element_html(G['text'], f'oac-s-14-{sid.lower()}')
    if fig is None:
        return None
    m = re.search(r'<p class="oac-title"[^>]*>(.*?)</p>', fig, flags=re.S)
    if m:
        return text_of(m.group(1))
    return 'spec'


def printed_evidence(G, sid):
    """The evidence label and grade line the guide prints over the chart, as (label, grade)."""
    fig = element_html(G['text'], f'oac-s-14-{sid.lower()}') or ''
    k = re.search(r'<p class="oac-ev-k"[^>]*>(.*?)</p>', fig, flags=re.S)
    g = re.search(r'<p class="oac-ev-g"[^>]*>(.*?)</p>', fig, flags=re.S)
    return (text_of(k.group(1)) if k else None, text_of(g.group(1)) if g else None)


def short_fault(x):
    """A kit fault as the line under a chart quotes it: decision codes move to the part's reference line (D3-206),
    and the fault stops at 180 characters."""
    s = B1.strip_codes(str(x))
    return s if len(s) <= 180 else s[:179].rsplit(' ', 1)[0] + ' …'


def chart_article(G, f, kit_out, S, what=None):
    """One chart as part 2 shows it: its rule, form and maker, its title as printed, the guide's evidence label where it
    is the one the content file marks, the kit's two composed pictures and the line under them. None when the kit made
    no pictures (the article then waits)."""
    sid, lo = f['spec_id'], f['spec_id'].lower()
    weights = G['report'].get('weight', {}).get('charts', {})
    spec = json.loads((ROOT / C['slots']['specs_dir'] / f'{lo}.json').read_text())
    d = kit_out / lo
    caps = {(g, w): d / f'{lo}-{g}-{w}.png' for g in ('newsprint', 'charcoal') for w in (1440, 390)}
    chk_p = d / f'{lo}-check.json'
    title = printed_title(G, sid) if G['usable'] else None
    title_from = 'guide'
    if title in (None, 'spec'):
        if title is None and G['usable']:
            warn(f'{sid} was not found in the guide; the spec’s title prints instead')
        title, title_from = spec['title'], 'spec'
    QUOTED.append(title)
    ev, grade = printed_evidence(G, sid) if G['usable'] else (None, None)
    marked = ev is not None and ev == C['sections']['charts']['mark_label']
    if marked:
        QUOTED.append(ev)
    aid = f'chart-{f["rule"].replace(".", "-")}'
    head = (f'<header class="ch-h"><p class="label">Rule {esc(f["rule"])} · {esc(f["form"])} · {esc(fill(S["maker"], {"m": f.get("maker", "?")}))}</p>'
            + (f'<p class="ev"><span class="ev-k">{esc(ev)}</span></p>' if marked else '')
            + f'<h4 class="ch-t">{esc(title)}</h4></header>'
            + (f'<p class="what">{esc(what)}</p>' if what else ''))
    rec = {'rule': f['rule'], 'form': f['form'], 'maker': f.get('maker'), 'title': title, 'title_from': title_from, 'evidence': ev, 'marked': marked}
    if not chk_p.exists() or not all(p.exists() for p in caps.values()):
        return f'<article class="chart" id="{aid}">{head}{pending("The kit’s pictures for this chart were not made at this build.")}</article>', rec, False
    chk = json.loads(chk_p.read_text())
    faults = chk.get('faults', [])
    alt = text_of(spec.get('alt', ''))
    stem = f'Chart-{f["rule"].replace(".", "-")}'
    rn_ = compose(f'{stem}-Newsprint', [(caps[('newsprint', 1440)], S['label_1440']), (caps[('newsprint', 390)], S['label_390'])])
    rc_ = compose(f'{stem}-Charcoal', [(caps[('charcoal', 1440)], S['label_1440']), (caps[('charcoal', 390)], S['label_390'])])
    wb = weights.get(f's-14-{lo}', {}).get('bytes')
    if wb is None:
        warn(f'the build report gives no bytes for {sid}')
    nd = len(chk.get('drawings', []))
    result = ('passes every check in the kit, ' + f'{nd} drawings checked' if not faults else
              f'{nw(len(faults))} {"fault" if len(faults) == 1 else "faults"} in the kit’s check: ' + '; '.join(short_fault(x) for x in faults[:3])
              + (f'; and {len(faults) - 3} more' if len(faults) > 3 else ''))
    QUOTED.extend(short_fault(x) for x in faults[:3])
    line = (f'{wb:,} bytes in the guide' if wb is not None else 'Its bytes in the guide were not found') + f'; {result}.'
    body = (f'<article class="chart" id="{aid}">{head}'
            f'<p class="row-label">{esc(S["row_newsprint"])}</p>{frame(rn_, f"{f["form"]}, Rule {f["rule"]}, on Newsprint, drawn for a 1440 px page and for a 390 px page, side by side. {alt}", lazy=len(IMAGES) > 2)}'
            f'<p class="row-label">{esc(S["row_charcoal"])}</p>{frame(rc_, f"{f["form"]}, Rule {f["rule"]}, on Charcoal, drawn for a 1440 px page and for a 390 px page, side by side.")}'
            f'<p class="ch-line">{esc(line)}</p></article>')
    rec.update({'bytes_in_guide': wb, 'faults': len(faults), 'drawings': nd, 'rows': chk.get('rows')})
    return body, rec, not faults


def charts_section(G, P, rn, kit_out):
    S = C['sections']['charts']
    groups = {g.get('family_section'): g for g in P['groups']}
    new = [f for f in rn if f['status'] == 'new']
    parts, cur, missing, n_pass, marked = [], None, [], 0, []
    for f in new:
        if f['family_section'] != cur:
            cur = f['family_section']
            g = groups.get(cur, {})
            QUOTED.append(g.get('title', ''))
            parts.append(f'<h3 class="sub grp">{esc(g.get("title", f["family"]))}</h3>')
        body, rec, ok = chart_article(G, f, kit_out, S)
        parts.append(body)
        FIG.setdefault('charts', {})[f['spec_id']] = rec
        if 'bytes_in_guide' not in rec:
            missing.append(f'Rule {f["rule"]}')
        n_pass += 1 if ok else 0
        if rec['marked']:
            marked.append(f['spec_id'])
    FILL.update({'n_pass': n_pass, 'n_marked_w': nw(len(marked)), 'n_marked_cap': cap(nw(len(marked))), 'marked_ids': join_words(marked), 'mark_label': S['mark_label']})
    FIG['estimate_charts'] = marked
    lede = f'<p class="intro">{esc(fill(S["lede"]))}</p>' + (f'<p>{esc(fill(S["lede_mark"]))}</p>' if marked else '')
    idx = ('<nav class="idx" aria-label="The new charts by rule"><ol>' + ''.join(f'<li><a href="#chart-{f["rule"].replace(".", "-")}">{esc(f["rule"])}</a></li>' for f in new) + '</ol></nav>')
    status = 'ready'
    if missing:
        lede += pending(f'Waiting for the kit’s pictures of {join_words(missing)}.')
        status = ('partial', 'kit')
    return section('charts', lede + idx + ''.join(parts), status)


def changed_section(G, P, kit_out):
    """Round 1 charts the round changed, each as part 2 shows a chart, with the content file's line on what changed."""
    S = C['sections']['changed']
    by_id = {f.get('spec_id'): f for f in P['forms'] if f.get('spec_id')}
    out, missing = [f'<p class="intro">{esc(fill(S["lede"]))}</p>'], []
    for it in S['charts']:
        f = by_id.get(it['spec'])
        if not f:
            warn(f'the plan holds no row for {it["spec"]}')
            continue
        body, rec, ok = chart_article(G, f, kit_out, C['sections']['charts'], what=it['what'])
        out.append(body)
        FIG.setdefault('changed', {})[it['spec']] = rec
        if 'bytes_in_guide' not in rec:
            missing.append(it['spec'])
    return section('changed', ''.join(out), 'ready' if not missing else ('partial', 'kit'))


def entry_section(G, shots):
    S = C['sections']['entry']
    ch14 = json.loads((ROOT / C['slots']['chapter14']).read_text())
    r = next((x for x in ch14['rules'] if x['id'] == S['rule']), None)
    need(r is not None, f'chapter 14 holds no Rule {S["rule"]}')
    src = element_html(G['text'], f'rule-{r["id"].replace(".", "-")}') or ''
    ph = re.search(r'<p class="oac-phone-k"[^>]*>(.*?)</p>', src, flags=re.S)
    phone = text_of(ph.group(1)) if ph else ''
    if G['usable'] and not phone:
        warn(f'Rule {r["id"]} prints no desk phone drawing')
    FILL.update({'entry_rule': r['id'], 'entry_title': r['title'].rstrip('.'), 'entry_phone': phone})
    QUOTED.extend([r['title'].rstrip('.'), phone])
    body = f'<p class="intro">{esc(fill(S["lede"]))}</p>' + (f'<p>{esc(fill(S["phone_line"]))}</p>' if phone else '')
    k14, k39 = f'entry-{r["id"]}-1440', f'entry-{r["id"]}-390'
    if G['usable'] and shots.get(k14, pathlib.Path('-')).exists() and shots.get(k39, pathlib.Path('-')).exists():
        a = compose(f'Entry-{r["id"].replace(".", "-")}-1440', [(shots[k14], '')])
        b = compose(f'Entry-{r["id"].replace(".", "-")}-390', [(shots[k39], '')])
        body += (f'<div class="pair">{figure(a, f"Rule {r["id"]} as the guide prints it at a 1440 px window: the rule, use it when, use instead, why it works, the example chart with its drawing for a phone beside it, and its table", esc(S["cap_1440"]))}'
                 f'{figure(b, f"Rule {r["id"]} as the guide prints it at a 390 px window, in the same order", esc(S["cap_390"]))}</div>')
        return section('entry', body, 'ready')
    return section('entry', body + pending('Waiting for a passing guide build and its photographs.'), ('waiting', 'build'))


def sketch_print(G, spec_id):
    """The heading the guide prints over a sketch, its caption chip and its caption."""
    src = element_html(G['text'], f'fig-{spec_id}') or ''
    m = re.search(r'class="plate-label-t">(.*?)</span>', src, flags=re.S)
    c = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', src, flags=re.S)
    chip, words = '', ''
    if c:
        k = re.search(r'<span class="illus">(.*?)</span>', c.group(1), flags=re.S)
        chip = text_of(k.group(1)) if k else ''
        words = text_of(re.sub(r'<span class="illus">.*?</span>', '', c.group(1), flags=re.S))
    return (text_of(m.group(1)) if m else None), chip, words


def sketch_order(rn, ch14):
    sk = [f for f in rn if f['status'] == 'sketch']
    kind = lambda f: (ch14.get(f['rule'], {}).get('correct') or {}).get('kind', '')
    return [f for f in sk if kind(f) == 'avoid'] + [f for f in sk if kind(f) != 'avoid']


def sketches_section(G, rn, shots):
    S = C['sections']['sketches']
    ch14 = {r['id']: r for r in json.loads((ROOT / C['slots']['chapter14']).read_text())['rules']}
    sk = sketch_order(rn, ch14)
    kinds = [((ch14.get(f['rule'], {}).get('correct') or {}).get('kind', '')) for f in sk]
    n_av = sum(1 for k in kinds if k == 'avoid')
    FILL.update({'n_sketch_cap': cap(nw(len(sk))), 'n_avoid_w': nw(n_av), 'n_ref_w': nw(len(sk) - n_av)})
    out, missing = [f'<p class="intro">{esc(fill(S["lede"]))}</p>'], []
    shown = None
    for f in sk:
        r = ch14.get(f['rule'], {})
        sid = f.get('sketch_id') or (r.get('correct') or {}).get('specimen')
        kind = (r.get('correct') or {}).get('kind', '')
        if kind != shown:
            shown = kind
            out.append(f'<h3 class="sub grp">{esc(S["h_avoid"] if kind == "avoid" else S["h_reference"])}</h3>')
        head, chip, words = sketch_print(G, sid) if G['usable'] else (None, '', '')
        key = f'sketch-{f["rule"]}'
        kw = S['kind_avoid'] if kind == 'avoid' else S['kind_reference']
        QUOTED.extend([r.get('title', ''), head or '', chip, words])
        h = (f'<header class="ch-h"><p class="label">Rule {esc(f["rule"])} · {esc(kw)}</p><h4 class="ch-t">{esc(r.get("title", f["form"]))}</h4></header>')
        if head and shots.get(key, pathlib.Path('-')).exists():
            rec = compose(f'Sketch-{f["rule"].replace(".", "-")}', [(shots[key], '')])
            capt = (f'{esc(S["heading_k"])} <b>{esc(head)}</b><br>{esc(S["caption_k"])} '
                    + (f'<span class="chip">{esc(chip)}</span> ' if chip else '') + esc(words))
            out.append(f'<article class="sketch">{h}{figure(rec, f"The sketch for Rule {f["rule"]}, headed “{head}”, with its caption, as the guide prints it at a 1440 px window. {words}", capt)}</article>')
        else:
            missing.append(f['rule'])
            out.append(f'<article class="sketch">{h}{pending("Waiting for a passing guide build and its photograph.")}</article>')
        if G['usable'] and not words:
            warn(f'the sketch for Rule {f["rule"]} prints no caption')
        FIG.setdefault('sketches', {})[f['rule']] = {'specimen': sid, 'heading': head, 'kind': kind, 'caption': words}
    return section('sketches', ''.join(out), 'ready' if not missing else ('partial', 'render'))


def caption_text(x):
    return text_of(x.get('caption', '')) if isinstance(x, dict) else ''


def changed_rules():
    """The rules of 14.1 to 14.14 that round 2 changed, as the creative director's scores name them: the rule numbers in
    the parenthesis of the item the content file names (its name lists them, "(14.3, 14.6, ...)")."""
    S = C['sections']['rules']
    p = ROOT / C['slots']['cd_scores']
    if not p.exists():
        warn('the creative director’s scores are missing, so the changed rules cannot be read')
        return []
    it = next((i for i in json.loads(p.read_text()).get('items', []) if i.get('key') == S['score_key']), None)
    if not it:
        warn(f'the creative director’s scores hold no item {S["score_key"]}')
        return []
    ids = []
    for par in re.findall(r'\(([^()]*)\)', it.get('name', '')):
        ids += re.findall(r'\b14\.\d+\b', par)
    if not ids:
        warn(f'the creative director’s item {S["score_key"]} names no changed rule')
    FIG['changed_rules_from'] = {'file': rel(p), 'item': S['score_key'], 'rules': ids}
    return list(dict.fromkeys(ids))


def rules_section(G, rules, shots):
    S = C['sections']['rules']
    ch14 = json.loads((ROOT / C['slots']['chapter14']).read_text())
    held = {r['id']: r for r in ch14['rules']}
    FILL.update({'n_changed_w': nw(len(rules)), 'changed_list': join_words(rules)})
    out, missing = [f'<p class="intro">{esc(fill(S["lede"]))}</p>'], []
    op = ch14.get('opener', {}).get('specimen')
    if op and shots.get('ch14-opener', pathlib.Path('-')).exists():
        rec = compose('Ch14-Opener', [(shots['ch14-opener'], '')])
        QUOTED.append(caption_text(ch14['opener']))
        out.append(f'<h3 class="sub">{esc(S["opener_h"])}</h3>' + figure(rec, f'Chapter 14’s opening plate at a 1440 px window. {caption_text(ch14["opener"])}', esc(caption_text(ch14['opener'])), lazy=True))
    elif op:
        missing.append('the opening plate')
    for rid in rules:
        r = held.get(rid)
        if not r:
            warn(f'chapter 14 holds no Rule {rid}')
            continue
        keys = [f'plate-{rid}-{k}' for k in ('correct', 'failure') if isinstance(r.get(k), dict)]
        have = [k for k in keys if shots.get(k, pathlib.Path('-')).exists()]
        QUOTED.append(r['title'])
        h = f'<h3 class="r-h" id="rule-{rid.replace(".", "-")}"><span class="rid">Rule {esc(rid)}</span> {esc(r["title"])}</h3>'
        if len(have) < len(keys) or not keys:
            missing.append(f'Rule {rid}')
            out.append(f'<article class="rule">{h}{pending("Waiting for the photographs of this rule’s plates.")}</article>')
            continue
        ws = [png_size(shots[k])[0] for k in have]
        side = sum(ws) + 24 * (len(ws) - 1) <= CONTENT_W
        rec = compose(f'Rule-{rid.replace(".", "-")}-Plates', [(shots[k], '') for k in have], cols=len(have) if side else 1, gap=24 if side else 32)
        cc, fc = caption_text(r.get('correct')), caption_text(r.get('failure'))
        alt = (f'Rule {rid}: the correct plate, then the failure plate, ' + ('side by side' if side else 'one above the other')
               + f', as the guide draws them at a 1440 px window. Correct: {cc} Failure: {fc}')
        out.append(f'<article class="rule">{h}{figure(rec, alt)}</article>')
        FIG.setdefault('rules', {})[rid] = {'plates': len(have), 'layout': 'side by side' if side else 'stacked', 'size': [rec['w'], rec['h']]}
    if missing:
        warn('plates not photographed: ' + ', '.join(missing))
    return section('rules', ''.join(out), 'ready' if rules and not missing else ('partial', 'render' if rules else 'cd'))


def ch15_section(G, shots):
    S = C['sections']['ch15']
    ch15 = json.loads((ROOT / C['slots']['chapter15']).read_text())
    r15 = new_ch15(ch15)
    wides = wide_plates(G, r15) if G['usable'] else []
    w1 = wides[0] if wides else None
    FILL.update({'wide_rule': w1[0] if w1 else '', 'wide_kind': (S['kind_correct'] if w1[1] == 'correct' else S['kind_failure']).lower() if w1 else '',
                 'wide_px': w1[3] if w1 else ''})
    out, missing = [f'<p class="intro">{esc(fill(S["lede"]))}</p>'], []

    def pair(key, name, alt):
        a, b = shots.get(f'{key}-1440'), shots.get(f'{key}-390')
        if not (a and b and a.exists() and b.exists()):
            missing.append(name)
            return pending('Waiting for this plate’s photographs.')
        rec = compose(f'Ch15-{name}', [(a, S['label_1440']), (b, S['label_390'])])
        return figure(rec, alt)
    order = [r['id'] for r in ch15['rules']]
    starts = sorted((order.index(g['before_rule']), g) for g in ch15.get('groups', []) if g.get('before_rule') in order)
    shown = None
    for r in r15:
        rid = r['id']
        g = next((g for i, g in reversed(starts) if i <= order.index(rid)), None)
        if g and g is not shown:
            shown = g
            QUOTED.append(g['title'])
            out.append(f'<h3 class="sub grp">{esc(g["title"])}</h3>')
        figs = ''
        for k in ('correct', 'failure'):
            if isinstance(r.get(k), dict):
                figs += (f'<p class="row-label">{esc(S["kind_correct"] if k == "correct" else S["kind_failure"])}</p>'
                         + pair(f'ch15-{rid}-{k}', f'{rid.replace(".", "-")}-{cap(k)}', f'Rule {rid}’s {k} plate at a 1440 px window and at a 390 px window, side by side. {caption_text(r[k])}'))
                if w1 and (rid, k) == (w1[0], w1[1]):
                    p = shots.get(f'ch15-{rid}-{k}-1024')
                    if p and p.exists():
                        rec = compose(f'Ch15-{rid.replace(".", "-")}-{cap(k)}-1024', [(p, '')])
                        figs += (f'<p class="row-label">{esc(fill(S["wide_h"]))}</p>'
                                 + figure(rec, f'Rule {rid}’s {k} plate at a 1024 px window, on its {w1[3]} px wide stage. {caption_text(r[k])}', esc(fill(S['wide_cap']))))
                    else:
                        missing.append(f'{rid} at 1024 px')
        QUOTED.append(r['title'])
        out.append(f'<article class="rule"><h4 class="r-h"><span class="rid">Rule {esc(rid)}</span> {esc(r["title"])}</h4>{figs}</article>')
    if missing:
        warn('chapter 15 plates not photographed: ' + ', '.join(missing))
    FIG['ch15'] = {'rules': [r['id'] for r in r15], 'wide_at_1024': list(w1[:3]) if w1 else None}
    return section('ch15', ''.join(out), 'ready' if r15 and not missing else ('partial', 'render'))


# ------------------------------------------------------------------------------------------------------- scores
ID = r'[A-Z]{1,4}(?:[- ][A-Z]{1,3})?-?\d{1,3}'      # M1, SC-M1, and round 2's prefixed IDs with a space: ST M1, BC S18, AX M1


def findings(body):
    """The numbered findings under a report's Must fix or Should fix heading: bold-led or heading-led IDs (M1, SC-M1),
    else top-level numbered items. None while the section is pending."""
    if body is None:
        return None
    b = body.strip()
    if not b or re.fullmatch(r'(?i)pending\.?', b):
        return None
    if re.fullmatch(r'(?i)none\.?|no must fix\.?|no should fix\.?', b):
        return 0
    # "**M1. Title**", "**M1.** Title", "- **SC-M1:** ...", "### M1. Title"
    ids = re.findall(r'^(?:#{2,6}\s+|[-*]\s+|\d+\.\s+)?\*\*(' + ID + r')(?:[.:)]|\*\*)', b, flags=re.M)
    ids += re.findall(r'^#{2,6}\s+(' + ID + r')[.:)\s]', b, flags=re.M)
    if ids:
        return len(dict.fromkeys(ids))
    n = len(re.findall(r'^\d+\.\s+\S', b, flags=re.M))
    return n if n else len(re.findall(r'^[-*]\s+\S', b, flags=re.M))


def score_in(part):
    """The first "N of 5" under a heading that names a score, the heading's own words included (one report writes
    "## Score for this lens: 3 of 5", another "## 1. Score" over "**3 of 5.**", the second passes "### New score")."""
    for m in re.finditer(r'^(#+)\s*(?:\d+\.\s*)?(.*\bscore\b.*)$', part, flags=re.M | re.I):
        nxt = re.search(r'^#+\s', part[m.end():], flags=re.M)
        block = m.group(2) + '\n' + part[m.end():m.end() + (nxt.start() if nxt else len(part))]
        s = re.search(r'\b([1-5])(?:\.\d)?\s*(?:out\s+)?of\s+5\b|\b([1-5])\s*/\s*5\b', block)
        if s:
            return int(s.group(1) or s.group(2))
    return None


def red_team(rt):
    """A red team report: its first score and Must fix and Should fix counts, from the part before its "Second pass"
    heading, and its second score from that section."""
    t = read(rt['file'])
    if t is None:
        return {'name': rt['name'], 'state': 'missing'}
    m = re.search(r'^##\s+(?:\d+\.\s*)?Second pass\b.*$', t, flags=re.M | re.I)
    first_part, second_part = (t[:m.start()], t[m.start():]) if m else (t, '')
    score = score_in(first_part)
    score2 = score_in(second_part) if second_part else None
    mf = findings(B1.md_section(first_part, [r'must fix']))
    sf = findings(B1.md_section(first_part, [r'should fix']))
    state = 'ready' if score is not None and mf is not None and sf is not None else 'waiting'
    if state == 'ready' and (mf == 0 and (B1.md_section(first_part, [r'must fix']) or '').strip().lower() not in ('none', 'none.')):
        warn(f'{rt["name"]}: its Must fix section has text but no numbered finding was found')
    if second_part and score2 is None:
        warn(f'{rt["name"]}: its second pass gives no score')
    return {'name': rt['name'], 'state': state, 'score': score, 'must_fix': mf, 'should_fix': sf, 'second_score': score2, 'file': rt['file']}


def drop_ids(s):
    """A review's finding IDs in a parenthesis, such as "(RM1, RM2)", leave the quoted reason: a reader would not know them
    (D3-206); decision codes still move to the reference line by board 1's rule."""
    rid = r'[A-Z]{1,4}\d{0,3}(?:-[A-Z]{1,3})?-?\d{1,3}'     # M1, RM2, SC-M1, CH15-S1
    return re.sub(r'\s*\((?:' + rid + r'(?:,\s*|\s+and\s+|;\s*)?)+\)', '', s or '')


def cd_files():
    p = ROOT / C['slots']['cd_scores']
    first = json.loads(p.read_text()) if p.exists() else None
    rs = sorted(glob.glob(str(ROOT / C['slots']['cd_rescores_glob'])), key=os.path.getmtime)
    re_ = json.loads(pathlib.Path(rs[-1]).read_text()) if rs else None
    FIG['cd'] = {'first': rel(p) if first else None, 'rescore': rel(rs[-1]) if rs else None}
    return first, re_


def cd_table(first, rescore):
    S = C['sections']['scores']
    d = rescore or first
    crit = d.get('criteria') or first.get('criteria') or []
    items = d.get('items', [])
    f_items = {i['key']: i for i in (first or {}).get('items', [])}
    both = rescore is not None
    head = '<th scope="col">Part</th>' + ''.join(f'<th scope="col">{esc(c["name"])}</th>' for c in crit) + '<th scope="col">Ready</th>'
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
        rows.append(f'<tr><th scope="row">{esc(drop_ids(it.get("name", it.get("key"))))}</th>{"".join(cell(c) for c in crit)}<td>{"Yes" if it.get("ready") else "<b>Not yet</b>"}</td></tr>')
    nr = [i for i in items if not i.get('ready')]
    short = lambda i: S.get('short_names', {}).get(i.get('key'), i.get('name', i.get('key')))
    if both:
        fi = (first or {}).get('items', [])
        summ = (f'The first scores found {nw(sum(1 for i in fi if i.get("ready")), "none")} of the {nw(len(fi))} parts ready. After the fix pass, the second scores find '
                + (f'all {nw(len(items))} ready.' if not nr else f'{nw(len(items) - len(nr), "none")} of the {nw(len(items))} ready, with {join_words([short(i) for i in nr])} still short.'))
    elif len(nr) == len(items):
        summ = fill(S['none_ready'], {'n': nw(len(items))})
    else:
        summ = (f'The first scores find {nw(len(items) - len(nr), "none")} of the {nw(len(items))} parts ready'
                + (f'; {join_words([short(i) for i in nr])} each had a score under 4 or a Must fix open.' if nr else '.'))
    under = []
    for i in items:
        for c in crit:
            v = i.get('scores', {}).get(c['key'])
            if isinstance(v, (int, float)) and v < 4:
                rs = drop_ids((i.get('reasons') or {}).get(c['key'], ''))
                QUOTED.append(rs)
                under.append(f'<li><b>{esc(cap(short(i)))}, {esc(c["name"].lower())}, {v}.</b> {B1.md_inline(rs)}</li>')
    FIG['cd_scores'] = {'items': len(items), 'ready': len(items) - len(nr), 'both': both,
                        'scores': {i.get('key'): {'first': (f_items.get(i.get('key'), {}) or {}).get('scores'), 'now': i.get('scores')} for i in items}}
    return (f'<p>{esc(summ)}</p>' + (f'<ul class="findings">{"".join(under)}</ul>' if under else '')
            + f'<p class="small">{esc(S["legend_both"] if both else S["legend_first"])}</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="The creative director’s scores; scrolls sideways"><table class="scores"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def scores_section():
    S = C['sections']['scores']
    first, rescore = cd_files()
    d = rescore or first
    if d:
        crit = d.get('criteria') or (first or {}).get('criteria') or []
        FILL.update({'cd_items_w': nw(len(d.get('items', []))), 'cd_crit_w': nw(len(crit)), 'cd_crit': join_words([c['name'].lower() for c in crit])})
    n_rt = len(C['slots']['red_teams'])
    FILL.update({'n_rt_w': nw(n_rt), 'n_rt_cap': cap(nw(n_rt))})
    out = [f'<h3 class="sub">{esc(S["cd_h"])}</h3><p class="intro">{esc(fill(S["cd_lede"] if d else S["cd_lede_wait"]))}</p>']
    status = 'ready'
    if first:
        out.append(cd_table(first, rescore))
        if not rescore:
            out.append(pending(S['cd_re_wait']))
            status = ('partial', 'cd_re')
    else:
        out.append(pending(S['cd_wait']))
        status = ('waiting', 'cd')
    rts = [red_team(rt) for rt in C['slots']['red_teams']]
    trs = []
    for r in rts:
        if r['state'] != 'ready':
            trs.append(f'<tr><th scope="row">{esc(r["name"])}</th><td colspan="4">{esc(S["rt_wait"])}</td></tr>')
            continue
        s2 = f'{r["second_score"]} of 5' if r.get('second_score') else esc(S['rt_wait2'])
        trs.append(f'<tr><th scope="row">{esc(r["name"])}</th><td class="num">{r["score"]} of 5</td><td class="num">{r["must_fix"]}</td>'
                   f'<td class="num">{r["should_fix"]}</td><td class="num">{s2}</td></tr>')
    n_rt = sum(1 for r in rts if r['state'] == 'ready' and r.get('second_score'))
    FILL['second_scores'] = rts
    if not first and not n_rt:
        status = ('waiting', 'cd')
    elif not first or not rescore:
        status = ('partial', 'cd' if not first else 'cd_re')
    elif n_rt < len(rts):
        status = ('partial', 'red')
    else:
        status = 'ready'
    FIG['red_teams'] = rts
    hd = ''.join(f'<th scope="col">{esc(c)}</th>' for c in S['rt_cols'])
    out.append(f'<h3 class="sub">{esc(fill(S["rt_h"]))}</h3><p>{esc(fill(S["rt_lede"]))}</p>'
               f'<div class="tw" role="region" tabindex="0" aria-label="{esc(fill(S["rt_h"]))}; scrolls sideways"><table class="rt"><thead><tr>{hd}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'
               f'<p class="small">{esc(S["rt_note"])}</p>')
    return section('scores', ''.join(out), status)


# ------------------------------------------------------------------------------------------------------- weight
def weight_section(G):
    S = C['sections']['weight']
    if not G['report']:
        return section('weight', pending('Waiting for a guide build report.'), ('waiting', 'build'))
    W = G['report'].get('weight', {})
    ch = W.get('chapters', {})
    pj = W.get('projection', {})
    pp = pj.get('chapter_14_per_plate', {})
    c14, c15 = ch.get('14', {}), ch.get('15', {})
    stop = pp.get('stop') or c14.get('budget')
    if pp.get('stop') and c14.get('budget') and int(pp['stop']) != int(c14['budget']):
        warn(f'the build report gives chapter 14 two stops: {pp["stop"]:,} and {int(c14["budget"]):,}')
    budget = pj.get('budget') or W.get('budget_page')
    FILL['budget_mb'] = f'{(budget or 0) / 1e6:g}'
    rows = [(S['rows']['ch14'], c14.get('bytes', 0), int(stop or 0)), (S['rows']['ch15'], c15.get('bytes', 0), int(c15.get('budget', 0))),
            (S['rows']['page'], pj.get('projected_bytes', 0), int(budget or 0))]
    FILL.update({'ch14_bytes': f'{c14.get("bytes", 0):,}', 'ch14_stop': f'{int(stop or 0):,}', 'per_plate': f'{pp.get("per_plate", 0):,}',
                 'plates_to_come': pp.get('plates_to_come', '?'), 'ch15_bytes': f'{c15.get("bytes", 0):,}', 'ch15_ceiling': f'{int(c15.get("budget", 0)):,}',
                 'page_bytes': f'{W.get("bytes", 0):,}', 'proj_bytes': f'{pj.get("projected_bytes", 0):,}', 'proj_room': f'{int((budget or 0) - pj.get("projected_bytes", 0)):,}'})
    trs = ''
    for name, b, lim in rows:
        share = 100 * b / lim if lim else 0
        name = fill(name)
        trs += (f'<tr><th scope="row">{esc(name)}</th><td class="barcell"><span class="bar" data-mark="bar" data-value="{share:.3f}" data-key="{esc(name)}" '
                f'style="width:{min(share, 100):.3f}%"></span><span class="pct">{share:.1f} percent</span></td><td class="num">{b:,}</td><td class="num">{lim:,}</td></tr>')
    hd = ''.join(f'<th scope="col">{esc(c)}</th>' for c in S['cols'])
    body = (f'<p class="intro">{esc(S["lede"])}</p>'
            f'<figure class="wfig" data-spec="weight-shares"><div class="tw" role="region" tabindex="0" aria-label="{esc(S["fig_caption"])}; scrolls sideways"><table class="wt">'
            f'<caption>{esc(S["fig_caption"])}</caption><thead><tr>{hd}</tr></thead><tbody>{trs}</tbody></table></div></figure>'
            f'<p>{esc(fill(S["per_plate"]))}</p><p>{esc(fill(S["ch15_line"]))}</p><p>{esc(fill(S["page_line"]))}</p>')
    FIG['weight'] = {'chapter_14': c14.get('bytes'), 'stop': stop, 'per_plate': pp.get('per_plate'), 'plates_to_come': pp.get('plates_to_come'),
                     'chapter_15': c15.get('bytes'), 'chapter_15_ceiling': c15.get('budget'), 'page': W.get('bytes'), 'projected': pj.get('projected_bytes'), 'budget': budget}
    return section('weight', body, 'ready' if G['ok'] else ('partial', 'build'))


# ------------------------------------------------------------------------------------------------------- tested
def tested_section(G):
    """A short summary: each Tested line with its figure read from the file that records it, each Not tested line
    checked against the file that names it, and one line on where the full lists are."""
    S = C['sections']['tested']
    rows, missing, waits = [], [], []
    for it in S['tested']:
        kind, words = it.get('kind'), None
        if kind == 'build':
            rep = G['report']
            if G['ok']:
                words = fill(it['words'], {'bytes': f'{rep.get("bytes", 0):,}', 'warnings': nw(len(rep.get('warnings', [])))})
            elif rep:
                words = fill(it['words_failed'], {'bytes': f'{rep.get("bytes", 0):,}', 'warnings': nw(len(rep.get('warnings', []))),
                                                  'exit': FIG['guide_build']['exit']})
                missing.append(it['label'])
        elif kind == 'guide_check':
            cands = sorted(SCRATCH.parents[2].glob(it['scratch_glob']), key=os.path.getmtime)
            if cands:
                J = json.loads(cands[-1].read_text())
                pg = cands[-1].with_name(re.sub(r'-Guide-Check-Results\.json$', '.html', cands[-1].name))
                runs = J.get('runs') if isinstance(J.get('runs'), list) else []
                widths = [str(r.get('width')) for r in runs if r.get('width')]
                words = fill(it['words'], {'widths': join_words(widths), 'failures': nw(len(J.get('failures', []))),
                                           'page_bytes': f'{pg.stat().st_size:,}' if pg.exists() else '?'})
                FIG['guide_check'] = {'file': '[scratch]/' + str(cands[-1].relative_to(SCRATCH.parents[2])), 'checked': J.get('checked'),
                                      'failures': J.get('failures'), 'pass': J.get('pass'), 'page_bytes': pg.stat().st_size if pg.exists() else None}
                if not it.get('other_build') and pg.exists() and G['report'].get('bytes') and pg.stat().st_size != G['report']['bytes']:
                    warn(f'the quick guide check ran on {pg.stat().st_size:,} bytes and today’s strict build is {G["report"]["bytes"]:,}')
        elif kind == 'kit_checks':
            # the kit's own check files from the closing run, one per chart; the sweep is read from the engineer's notes
            fs = sorted(SCRATCH.parents[2].glob(it['scratch_glob']))
            if fs:
                ok_n = sum(1 for f in fs if not json.loads(f.read_text()).get('faults'))
                sweep = bool(re.search(it['confirm_pattern'], read(it['confirm_file']) or ''))
                if not sweep:
                    warn(f'“{it["label"]}”: {it["confirm_file"]} no longer says the sweep runs in every build')
                words = fill(it['words'] if sweep else it['words_plain'], {'pass': f'{ok_n:,}', 'n': f'{len(fs):,}'})
                FIG['kit_close'] = {'glob': '[scratch]/' + it['scratch_glob'], 'check_files': len(fs), 'pass': ok_n, 'sweep': sweep}
        elif kind == 'second_pass':
            rts = FILL.get('second_scores') or []
            got = [r for r in rts if r.get('second_score')]
            if got and len(got) == len(rts):
                sc = {r['second_score'] for r in got}
                words = (f'all {nw(len(got))} at {got[0]["second_score"]} of 5' if len(sc) == 1
                         else join_words([f'{r["name"].lower()} {r["second_score"]} of 5' for r in got]))
        elif kind == 'rescore':
            _, rs = cd_files()
            if rs:
                items = rs.get('items', [])
                k = sum(1 for x in items if x.get('ready'))
                words = fill(it['words'], {'ready': f'all {nw(k)}' if k == len(items) else f'{nw(k, "none")} of the {nw(len(items))}',
                                           'crit': nw(len(rs.get('criteria', [])))})
        else:
            parts = []
            for s in it['sources']:
                sp = SCRATCH.parents[2] / s['scratch_file'] if s.get('scratch_file') else None
                txt = (sp.read_text() if sp and sp.exists() else '') if sp else (read(s['file']) or '')
                ms = list(re.finditer(s['pattern'], txt))
                if ms:
                    g = ms[-1].groups()
                    parts.append(re.sub(r'\{(\d)\}', lambda m: f'{int(g[int(m.group(1)) - 1]):,}', s['words']))
                else:
                    warn(f'“{it["label"]}”: its figure was not found in {s.get("file") or "[scratch]/" + s["scratch_file"]}')
            words = '; '.join(parts) if len(parts) == len(it['sources']) else None
        if words is None and kind in ('second_pass', 'rescore'):
            waits.append(it['label'])
            words = S['wait_words']
        elif words is None:
            missing.append(it['label'])
            words = 'Not found in its file at this build.'
        rows.append(f'<li><b>{esc(it["label"])}:</b> {esc(words)}.</li>' if not words.endswith('.') else f'<li><b>{esc(it["label"])}:</b> {esc(words)}</li>')
        FIG.setdefault('tested', {})[it['label']] = words
    nots = []
    for it in S['not_tested']:
        txt = read(it['file']) or ''
        if not re.search(it['pattern'], txt, flags=re.I):
            warn(f'the Not tested line “{it["words"][:40]}” is no longer named in {it["file"]}')
        nots.append(f'<li>{esc(it["words"])}</li>')
    body = (f'<p class="intro">{esc(S["lede"])}</p><div class="tcols">'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["tested_h"])}</h3><ul>{"".join(rows)}</ul></div>'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["not_h"])}</h3><ul>{"".join(nots)}</ul></div></div>'
            f'<p class="small">{esc(S["full_lists"])}</p>')
    if missing:
        warn('Tested lines without their figure: ' + ', '.join(missing))
        return section('tested', body, ('partial', 'notes'))
    if waits:
        return section('tested', body, ('partial', 'red' if any('second' in w for w in waits) else 'cd_re'))
    return section('tested', body, 'ready')


def next_section():
    S = C['sections']['next']
    return section('next', f'<p class="intro">{esc(S["line"])}</p>', 'ready')


# ------------------------------------------------------------------------------------------------------- page
ORDER = ['round', 'charts', 'changed', 'entry', 'sketches', 'rules', 'ch15', 'scores', 'weight', 'tested', 'next']


def cover(rescored):
    K = C['cover']
    toc = ''.join(f'<li><a href="#p-{k}"><span class="n">{C["sections"][k]["n"]:02d}</span><span class="t">{esc(fill(C["sections"][k]["nav"]))}</span></a>'
                  f'{chip(STATUS[k], short=True)}</li>' for k in ORDER)
    return (f'<header class="cover"><div class="mast"><b>OATH &amp; ACTION</b><span class="label">{esc(K["kicker"])}</span></div>'
            f'<p class="label for">{esc(fill(K["for_line"]))}</p><h1>{esc(K["title"])}</h1>'
            f'<div class="cover-grid"><div class="deck"><p>{esc(fill(K["deck_rescored"] if rescored else K["deck_building"]))}</p><p>{esc(K["no_decision"])}</p>'
            f'<p class="caption">{esc(K["minutes"])}</p></div>'
            f'<nav class="toc" aria-labelledby="toc-h"><p class="label" id="toc-h">{esc(K["toc_h"])}</p><ol>{toc}</ol></nav></div></header>')


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
.toc ol,.idx ol{list-style:none;margin:0;padding:0}
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
.facts{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-500);margin:var(--oa-space-200) 0 var(--oa-space-300);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:64em){.facts{grid-template-columns:repeat(3,minmax(0,1fr))}}
.facts div{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.facts dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2)}
.facts dd{margin:var(--oa-space-050) 0 0;font:var(--oa-type-body-small)}
.nodec{font:var(--oa-type-ui);font-weight:600;border-left:var(--oa-border-width-bar) solid var(--charcoal);padding-left:var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.idx ol{display:flex;flex-wrap:wrap;gap:var(--oa-space-100);margin-top:var(--oa-space-200)}
.idx a{display:inline-flex;align-items:center;justify-content:center;min-width:3.5rem;min-height:2.75rem;padding:0 .5em;border:var(--oa-border-width-hairline) solid var(--strong);text-decoration:none;font:var(--oa-type-ui);font-weight:600;font-variant-numeric:tabular-nums}
.chart,.sketch{margin-top:var(--oa-space-600);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-200)}
.ch-h{margin-bottom:var(--oa-space-200)}
.ch-t{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin-top:var(--oa-space-050);max-width:var(--oa-layout-measure-intro-max);text-wrap:balance}
.row-label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:var(--oa-space-300) 0 var(--oa-space-100)}
.ch-line{font:var(--oa-type-body-small);margin-top:var(--oa-space-150);font-variant-numeric:tabular-nums}
.ev{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--oa-space-050) var(--oa-space-150);margin:var(--oa-space-100) 0 0}
.ev-k{font:var(--oa-type-caption);font-weight:600;padding:0 .5em;border:var(--oa-border-width-hairline) solid var(--strong);line-height:1.6}
.what{font:var(--oa-type-body-small);border-left:var(--oa-border-width-bar) solid var(--charcoal);padding-left:var(--oa-space-200);margin:var(--oa-space-150) 0 var(--oa-space-200)}
.shot figcaption .chip{font-weight:600;color:var(--ink);padding:0 .4em;border:var(--oa-border-width-hairline) solid var(--strong)}
.rule{margin-top:var(--oa-space-500);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-200)}
.r-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);max-width:var(--oa-layout-measure-intro-max);text-wrap:balance;margin-bottom:var(--oa-space-150)}
.r-h .rid{display:block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin-bottom:var(--oa-space-050)}
.shot{margin:var(--oa-space-200) 0 var(--oa-space-300);min-width:0;max-width:100%;display:flex;flex-direction:column;gap:var(--oa-space-100)}
.shot figcaption{font:var(--oa-type-caption);color:var(--ink-2);max-width:var(--oa-layout-measure-intro-max)}
.shot figcaption b{color:var(--ink);font-weight:600}
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
.wt td.num,.rt td.num{text-align:right}.wt thead th:nth-child(n+3),.rt thead th:nth-child(n+2){text-align:right}
table.scores{min-width:44rem}table.rt{min-width:30rem}table.wt{min-width:40rem}
td.sc.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong);font-weight:700}
td.sc .r1{display:inline-block;min-width:1.4em;font:var(--oa-type-caption);color:var(--wink-2);margin-right:.35em;padding:0 .2em}
td.sc .r2{display:inline-block;min-width:1.6em;font-weight:700;padding:0 .2em}
td.sc .lo{box-shadow:inset 0 0 0 var(--oa-border-width-hairline) var(--wstrong)}
td.sc .r2.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong)}
td.sc.mv .r2{background:var(--tint)}
.findings{margin:0 0 var(--oa-space-200);padding-left:1.2em;max-width:var(--oa-layout-measure-intro-max)}
.findings li{margin-bottom:var(--oa-space-100)}
.wfig{margin:0}
.wt th[scope=row]{width:18rem}
.barcell{width:45%;min-width:12rem}
.bar{display:block;height:1.25rem;background:var(--charcoal)}
.pct{display:block;font:var(--oa-type-caption);color:var(--wink-2);margin-top:var(--oa-space-050);font-variant-numeric:tabular-nums}
.tcols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-500);margin-top:var(--oa-space-400)}
@media (min-width:64em){.tcols{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tcol{border-top:var(--oa-border-width-bar) solid var(--charcoal);padding-top:var(--oa-space-150);min-width:0}
.tcol-h{font:var(--oa-type-h4);margin-bottom:var(--oa-space-150)}
.tcol ul{margin:var(--oa-space-050) 0 var(--oa-space-200);padding-left:1.2em;font:var(--oa-type-body-small)}
.tcol li{margin-bottom:var(--oa-space-050);overflow-wrap:anywhere}
.tcol .where{font:var(--oa-type-caption);color:var(--ink-2);margin:var(--oa-space-150) 0 0}
details.more{margin-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
details.more>summary{cursor:pointer;font:var(--oa-type-ui);font-weight:600;min-height:2.75rem;display:flex;align-items:center;gap:var(--oa-space-100)}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:none}
@media print{.toc{display:none}details{display:block}}
'''


def strip_css(t):
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'/\*.*?\*/', '', t, flags=re.S)).strip()


def token_root(css):
    """The tokens.css :root definitions the page's styles name, and the ones they name in turn, in the file's order."""
    t = (ROOT / C['slots']['tokens_css']).read_text()
    m = re.search(r'(?m)^:root\s*\{(.*?)^\}', t, flags=re.S)
    need(m, 'tokens.css has no :root block')
    defs = {}
    order = []
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
    t = re.sub(r'</?(?:p|li|ul|ol|h\d|td|th|tr|div|figure|figcaption|caption|blockquote|section|header|nav|main|table|thead|tbody|summary|details|dt|dd|dl|article|span)\b[^>]*>|<br\s*/?>', ' ', t)
    return html.unescape(re.sub(r'<[^>]+>', '', t))


def checks(page):
    text = visible_text(page)
    alts = ' '.join(html.unescape(a) for a in re.findall(r'(?:alt|aria-label)="([^"]*)"', page))
    for ch, name in (('—', 'an em dash'), ('–', 'an en dash')):
        for where, t in (('text', text), ('alt text', alts)):
            i = t.find(ch)
            if i >= 0:
                warn(f'{name} in the page’s {where}: ' + t[max(0, i - 60):i + 20])
    own_page = page
    for q in QUOTED:
        if q:
            for frag in (B1.md_inline(q), B1.md_inline(q, quote=False), esc(q)):
                own_page = own_page.replace(frag, ' ')
    own_page = re.sub(r'<div class="tcols">.*?</div>\s*(?=<p class="codes">|<div class="pending"|</section>)', ' ', own_page, flags=re.S)
    own = visible_text(own_page)
    B1.MOVED.clear()
    for leftover in re.findall(r'\{[a-z0-9_]+\}', own):
        warn(f'an unfilled field on the page: {leftover}')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', own, flags=re.I)})
    if flagged:
        warn('flagged words in the page’s own words: ' + ', '.join(flagged))
    face = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))
    stray = set(re.findall(r'\b' + CODE_DEC + r'\b', face))
    if stray:
        warn('decision codes on the page’s face: ' + ', '.join(sorted(stray)))
    for pat in (r'/home/', r'file://', r'scratchpad', r'/tmp/', r'@anthropic'):
        if re.search(pat, page):
            warn(f'a private path on the page ({pat})')
    if re.search(r'<script\b', page, flags=re.I):
        warn('a script on the page')
    for bad in (r'<!doctype', r'<html\b', r'<head\b', r'<body\b'):
        if re.search(bad, page, flags=re.I):
            warn(f'the page carries {bad.strip(chr(92) + "b")}, which the host adds itself')
    hosts = set(re.findall(r'(?:src|href|url\()\s*"?https?://([^/"\s)]+)', page))
    extra = hosts - {'fonts.googleapis.com', 'fonts.gstatic.com'}
    if extra:
        warn('loads from hosts other than Google Fonts: ' + ', '.join(sorted(extra)))
    if '@media (prefers-color-scheme' in page:
        warn('the page carries a dark-mode block')
    for v, u in re.findall(r'font-size:\s*(\d*\.?\d+)(px|rem)', strip_css(CSS)):
        if float(v) * (16 if u == 'rem' else 1) < 13:
            warn(f'a font size of {v}{u} in the page CSS, under 13 px')
    lit = re.findall(r'#[0-9a-fA-F]{3,8}\b|rgba?\(', strip_css(CSS))
    if lit:
        warn('a color in the page CSS that is not a token: ' + ', '.join(lit[:5]))
    for m in re.finditer(r'<img\b[^>]*>', page):
        if not re.search(r'alt="[^"]{12,}"', m.group(0)):
            warn('an image without alt text that says what it shows: ' + m.group(0)[:120])
    return text


def run_checks(out, page):
    """dataviz_check.js --board on the page, then on a copy wrapped as the host wraps it (see the module's docstring)."""
    def check(path):
        r = subprocess.run(['node', str(SCRIPTS2 / 'dataviz_check.js'), str(path), '--board', '--no-captures'], cwd=ROOT / 'work/build',
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        res = pathlib.Path(path).with_name(pathlib.Path(path).stem + '-Check-Results.json')
        J = json.loads(res.read_text()) if res.exists() else {}
        return r, J
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
    r2, J2 = check(wrapped)
    fails2 = J2.get('failures', ['no results file'])
    print('the page itself: ' + ('PASS' if not fails1 else f'{len(fails1)} failures: ' + '; '.join(fails1[:6])))
    print('the page as the host wraps it: ' + ('PASS' if not fails2 else f'{len(fails2)} failures: ' + '; '.join(fails2[:6])))
    FIG['check'] = {'page': {'failures': fails1, 'allowed': [f for f in fails1 if f not in other], 'results': rel(out.with_name(out.stem + '-Check-Results.json'))},
                    'wrapped': {'failures': fails2, 'pass': J2.get('pass'), 'results': '[scratch]/publish-view/' + wrapped.stem + '-Check-Results.json'},
                    'widths': [x.get('width') for x in J2.get('runs', [])]}
    if other:
        warn('the page check failed: ' + '; '.join(other[:6]))
    if fails2:
        warn('the wrapped page check failed: ' + '; '.join(fails2[:6]))
    return not other and not fails2


def main():
    global C, LOG, SCRATCH, CACHE
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--reuse', action='store_true', help='keep kit captures and guide photographs whose sources have not changed')
    ap.add_argument('--check', action='store_true', help='run dataviz_check.js --board on the page')
    ap.add_argument('--strict', action='store_true', help='exit 1 on any warning')
    ap.add_argument('--scratch', type=pathlib.Path, default=SCRATCH_DEFAULT)
    ap.add_argument('--out', type=pathlib.Path, default=OUT)
    ap.add_argument('--photos-from-failed-build', action='store_true',
                    help='photograph a strict build that failed, while the fix pass runs, to prove the method; never for the page Dustin sees')
    a = ap.parse_args()
    global ACCEPT_FAILED
    ACCEPT_FAILED = a.photos_from_failed_build
    SCRATCH = a.scratch
    SCRATCH.mkdir(parents=True, exist_ok=True)
    os.environ['TMPDIR'] = str(SCRATCH)
    raw = CONTENT.read_text()
    if '—' in raw:
        warn('the content file holds an em dash')
    C = json.loads(raw)
    LOG = B1.read_log()
    IMG.mkdir(parents=True, exist_ok=True)
    cache_file = SCRATCH / 'compose-cache.json'
    CACHE = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL['built_date'] = B1.words_when(built)
    FIG['built'] = built.isoformat()
    t0 = datetime.datetime.now()
    print('building the guide (strict) ...')
    G = guide_build()
    P, rn = plan()
    new_ids = [f['spec_id'] for f in rn if f['status'] == 'new']
    kit_out = kit_build(new_ids + [x['spec'] for x in C['sections']['changed']['charts']], a.reuse)
    ch14 = json.loads((ROOT / C['slots']['chapter14']).read_text())
    ch15 = json.loads((ROOT / C['slots']['chapter15']).read_text())
    rules = changed_rules()
    shots = {}
    if G['usable']:
        er = C['sections']['entry']['rule']
        items = [(f'entry-{er}-1440', f'rule-{er.replace(".", "-")}', 1440), (f'entry-{er}-390', f'rule-{er.replace(".", "-")}', 390)]
        held = {r['id']: r for r in ch14['rules']}
        for f in sketch_order(rn, held):
            sid = f.get('sketch_id') or (held.get(f['rule'], {}).get('correct') or {}).get('specimen')
            items.append((f'sketch-{f["rule"]}', f'fig-{sid}', 1440))
        if ch14.get('opener'):
            items.append(('ch14-opener', f'fig-{ch14["opener"]["specimen"]}', 1440))
        for rid in rules:
            for k in ('correct', 'failure'):
                sp = (held.get(rid, {}).get(k) or {}).get('specimen')
                if sp:
                    items.append((f'plate-{rid}-{k}', f'fig-{sp}', 1440))
        r15 = new_ch15(ch15)
        for r in r15:
            for k in ('correct', 'failure'):
                if isinstance(r.get(k), dict):
                    items += [(f'ch15-{r["id"]}-{k}-{w}', f'fig-{r[k]["specimen"]}', w) for w in (1440, 390)]
        w1 = (wide_plates(G, r15) or [None])[0]
        if w1:
            items.append((f'ch15-{w1[0]}-{w1[1]}-1024', f'fig-{w1[2]}', 1024))
        for rid, k, sp, wide in wide_plates(G, ch15['rules'], (ch15.get('opener') or {}).get('specimen')):
            items += [(f'wide-{sp}-{w}', f'fig-{sp}', w, 'measure') for w in C['carried']['wide_widths']]
        shots = run_shots(G, items, a.reuse)
    parts = [round_section(G, P, rn, shots), charts_section(G, P, rn, kit_out), changed_section(G, P, kit_out), entry_section(G, shots),
             sketches_section(G, rn, shots), rules_section(G, rules, shots), ch15_section(G, shots), scores_section(), weight_section(G),
             tested_section(G), next_section()]
    cache_file.write_text(json.dumps(CACHE))
    keep = set(IMAGES)
    for p in [q for q in IMG.iterdir() if q.suffix.lower() in IMG_EXT]:
        if p.name not in keep:
            p.unlink()
            NOTES.append(f'removed {p.name}, which the page no longer shows')
    rescored = bool(FIG.get('cd', {}).get('rescore'))
    page = build_page(cover(rescored) + '\n' + '\n'.join(parts))
    checks(page)
    need(len(page.encode()) < LIMIT_PAGE, 'the page is over 16 MB')
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    imgs = sorted(q for q in IMG.iterdir() if q.suffix.lower() in IMG_EXT)
    named = set(re.findall(r'src="img/([^"]+)"', page))
    if named != {p.name for p in imgs}:
        warn(f'the page names {len(named)} images and img/ holds {len(imgs)}')
    files = [p for p in PAGE_DIR.rglob('*') if p.is_file()]
    big = [p.name for p in imgs if p.stat().st_size > LIMIT_IMAGE]
    if big:
        warn('images over 15 MB: ' + ', '.join(big))
    total = sum(p.stat().st_size for p in files)
    if len(files) >= LIMIT_FILES:
        warn(f'the folder holds {len(files)} files, at or over {LIMIT_FILES}')
    if total >= LIMIT_TOTAL:
        warn(f'the folder comes to {total / 1e6:.2f} MB, at or over {LIMIT_TOTAL / 1e6:.0f} MB')
    FIG.update({'page': rel(a.out), 'html_bytes': len(page.encode()), 'images': len(imgs), 'image_bytes': sum(p.stat().st_size for p in imgs),
                'folder_files': len(files), 'folder_bytes': total, 'largest_image': max(((p.stat().st_size, p.name) for p in imgs), default=(0, None)),
                'status': {k: (v if isinstance(v, str) else list(v)) for k, v in STATUS.items()},
                'image_sources': {r['src']: r.get('source') for r in IMAGES.values()}, 'codes_in_reference_lines': sorted(LINKED),
                'notes': NOTES, 'warnings': WARN, 'seconds': round((datetime.datetime.now() - t0).total_seconds())})
    FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
    words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9’'.,-]*", visible_text(page)))
    tested_words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9’'.,-]*", visible_text(page[page.find('id="p-tested"'):page.find('id="p-next"')])))
    FIG.update({'words': words, 'words_tested_part': tested_words})
    FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
    print(f'wrote {rel(a.out)} ({len(page.encode()) / 1e3:.0f} kB, {words:,} words, part 10 {tested_words}) and {len(imgs)} images; the folder holds {len(files)} files, {total:,} bytes')
    print('parts: ' + ', '.join(f'{k} {status_words(v)}' for k, v in STATUS.items()))
    print(f'{len(WARN)} warnings')
    if a.check:
        ok = run_checks(a.out, page)
        FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
        if not ok:
            sys.exit(1)
    if WARN and a.strict:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except PageError as e:
        print('error:', e)
        sys.exit(2)
