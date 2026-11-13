"""Build board 2 of Phase 3 (November 13, 2026; the board builder, working as the design director).

Built on board 1's and the round 2 progress page's builders, which stay as they are. Usage:
    python3 -I work/build/scripts/phase-3/board_2_build.py [--reuse] [--check] [--strict] [--scratch DIR] [--out PATH]
                                                           [--decisions FILE]

Reads, on every run:
    work/boards/phase-3/round-3/board-2/20261113_Board-2-Content.json   the board's own words and the files it reads
    work/handoffs/phase-3/20261113_Board-2-Decisions.json               panel 1's items and the Rule 01.9 and DR-229
                                                                         counts (the data lead's; --decisions reads
                                                                         another file, for a test only)
    work/handoffs/phase-3/20261112_Chapter-14-Plan.json                 the 114 forms of rounds 1 to 3, by family
    a fresh strict build of the guide (guide_build.py --strict --out <scratch>/guide/): every guide photograph, each
        chart's printed title, evidence label, source line and table, the width the guide draws each chart at 1440 and
        390 px, every entry's anchor, and the weights in its report
    the chart kit's own captures, built afresh into <scratch>/kit-out/ by oa-chart.mjs at the widths the guide draws
        (one folder per chart: both grounds, both widths, the grayscale proofs, the check file with its weight line)
    work/boards/phase-3/round-0/specimens/                              board 1's captures, check files and exports
    work/handoffs/phase-3/board-2-pictures/                             the cartographer's board-only pictures
    work/build/guide/chapters/14-data-visualization.json                rules 14.1 to 14.14, the opener, the sketches
    the creative director's scores and rescores and the red team reports of rounds 1 to 3, the board's own scores
        when they land, the quick guide check's results file the main session names, the engineer's notes
    work/build/tokens/tokens.css (the :root tokens the page's styles name, and only those)
    work/ledger/*_Decision-Log.md and *_Open-Questions.md               every code in a reference line must exist
Writes:
    work/boards/phase-3/round-3/board-2/20261113_Board-2.html           the board (no scripts; the host wraps it)
    work/boards/phase-3/round-3/board-2/img/                            every picture it shows, composed
    work/boards/phase-3/round-3/board-2/20261113_Board-2-Figures.json   every figure it prints, with its source
    work/boards/phase-3/round-3/board-2/20261113_Board-2-Check-Results.json  (written by dataviz_check.js)
    <scratch>/  the guide build, the kit's builds, the photographs, the measurements and the composition cache
It also puts back work/build/chart-kit/plate-share.json as it found it, since the strict build rewrites its timestamp.

--reuse keeps a kit capture when its spec, data, form module, the kit's shared files and the widths asked are unchanged,
and a guide photograph or measurement when its element's HTML, the page's styles and scripts and the window width are
unchanged; without it, every capture and photograph is made afresh. --check runs dataviz_check.js with --board
--no-captures, from work/build, on the page itself and on a copy wrapped as the host wraps it; the page carries no
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

ROOT = pathlib.Path(__file__).resolve().parents[4]
SCRIPTS2 = ROOT / 'work/build/scripts/phase-2'
SCRIPTS3 = ROOT / 'work/build/scripts/phase-3'
sys.path.insert(0, str(SCRIPTS3))
import board_1_build as B1  # noqa: E402   board 1's Markdown readers and quoted-words rules (D3-206)

DATE = '20261113'
BOARD_DIR = ROOT / 'work/boards/phase-3/round-3/board-2'
IMG = BOARD_DIR / 'img'
CONTENT = BOARD_DIR / f'{DATE}_Board-2-Content.json'
FIGURES = BOARD_DIR / f'{DATE}_Board-2-Figures.json'
OUT = BOARD_DIR / f'{DATE}_Board-2.html'
SCRATCH_DEFAULT = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/builder')
SCRATCH_ROOT = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad')
LABEL_FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
NEWSPRINT = (0xDC, 0xD9, 0xD2)
LABEL_INK = (0x4E, 0x53, 0x5B)
CONTENT_W = 1280          # the widest picture that sits in the board's column at a 1440 px window with no frame scroll
REGION_W = 288            # a picture wider than a 320 px window's column scrolls in its own named frame
FILES_AIM = 330           # the brief: about 300 files
BYTES_AIM = 120_000_000   # and under 120 MB
LIMIT_FILES = 511
LIMIT_TOTAL = 256_000_000
LIMIT_IMAGE = 15_000_000
LIMIT_PAGE = 16_000_000
FLAGGED = B1.FLAGGED
CODE_DEC = B1.CODE_DEC
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp')
DESK, PHONE = 1440, 390   # the two windows the board shows each chart at

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


class BoardError(Exception):
    pass


def warn(msg):
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
    """A form's live entry in the guide preview, as board C's builder links rules; the anchor must be on today's build."""
    a = rid_anchor(rid)
    if ANCHORS and a not in ANCHORS:
        warn(f'Rule {rid}: #{a} is not on today’s strict build')
    LINKED.add(a)
    return f'{C["slots"]["preview_url"]}#{a}'


# ------------------------------------------------------------------------------------------------------- the guide
def guide_build():
    d = SCRATCH / 'guide'
    d.mkdir(parents=True, exist_ok=True)
    page = d / f'{DATE}_Board-2-Guide.html'
    rep = d / f'{DATE}_Board-2-Guide-Build-Report.json'
    for p in (page, rep):
        if p.exists():
            p.unlink()
    share = ROOT / C['slots']['plate_share']
    before = share.read_bytes() if share.exists() else None
    r = subprocess.run([sys.executable, '-I', str(ROOT / C['slots']['guide_build']), '--strict', '--out', str(page)], cwd=ROOT,
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    (SCRATCH / 'guide-build.log').write_text(r.stdout + r.stderr)
    # the strict build rewrites plate-share.json; this board's build is a scratch build, so it puts back what was there
    # whenever the file holds this build's own timestamp (another owner's build since then is left as it wrote it)
    if before is not None and share.exists() and share.read_bytes() != before:
        a, b = json.loads(before), json.loads(share.read_text())
        mine = rep.exists() and b.get('built') == json.loads(rep.read_text()).get('built')
        if mine:
            share.write_bytes(before)
            if a.get('per_plate') != b.get('per_plate'):
                NOTES.append(f'this build’s share per plate is {b.get("per_plate")}; {rel(share)} keeps {a.get("per_plate")}, as found')
        else:
            warn(f'{rel(share)} changed during this build and not by it; left as it is')
    ok = r.returncode == 0 and page.exists() and rep.exists()
    if not ok:
        warn(f'the strict guide build failed (exit {r.returncode}); the guide pictures wait for a passing build')
    report = json.loads(rep.read_text()) if rep.exists() else {}
    text = page.read_text() if page.exists() else ''
    ANCHORS.update(re.findall(r'\sid="(rule-14-\d+)"', text))
    FIG['guide_build'] = {'exit': r.returncode, 'bytes': report.get('bytes'), 'rules': report.get('rules'),
                          'specimens': report.get('specimens_placed'), 'warnings': len(report.get('warnings', [])), 'built': report.get('built')}
    return {'ok': ok, 'usable': ok, 'page': page, 'text': text, 'report': report, 'mtime': page.stat().st_mtime if page.exists() else None}


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


def run_render(jobs, label):
    """One browser at a time: board_2_render.js opens each page in turn and closes the browser at the end."""
    if not jobs:
        return
    jp = SCRATCH / f'render-jobs-{label}.json'
    jp.write_text(json.dumps(jobs))
    r = subprocess.run(['node', str(SCRIPTS3 / 'board_2_render.js'), str(jp)], cwd=ROOT / 'work/build',
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    (SCRATCH / f'render-{label}.log').write_text(r.stdout + r.stderr)
    for line in r.stdout.splitlines():
        if line.startswith('failed') or line.startswith('page error'):
            warn('render: ' + line)
    if r.returncode != 0 and 'failed' not in r.stdout:
        warn('the renderer stopped: ' + r.stderr[-300:])


def run_shots(G, items, reuse):
    """items: [(key, element id, width)] or [(key, element id, width, 'measure')] -> {key: path}. One page load per width,
    only for the items that changed."""
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
    jobs = [{'file': str(G['page']), 'width': w, 'height': 900 if w > 600 else 844, 'static_sticky': True, 'draw_all': True,
             'items': [{'selector': f'#{el}', 'out': str(p), 'measure': m} for key, el, s, p, m in its]} for w, its in sorted(todo.items(), reverse=True)]
    if jobs:
        print(f'photographing or measuring {sum(len(j["items"]) for j in jobs)} elements of the guide ...')
        for its in todo.values():
            for key, el, s, p, m in its:
                if p.exists():
                    p.unlink()
        run_render(jobs, 'guide')
        for its in todo.values():
            for key, el, s, p, m in its:
                if p.exists():
                    sigs[key] = s
        sig_file.write_text(json.dumps(sigs, indent=1))
    FIG['shots'] = {'taken': sorted(k for its in todo.values() for k, *_ in its), 'reused': sorted(k for k in paths if all(k != x[0] for its in todo.values() for x in its))}
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


def board1_compare(ids, kit_out, pages):
    """Whether each board 1 chart's drawing changed since board 1, two ways. (1) Panel 1: the charts the decisions file's
    "board-1-changed" group names, in its items or rows, are the changes the data lead lists. (2) Pixels: the kit's
    drawing alone at a 1440 px window on Newsprint, at twice the pixels, compared pixel for pixel with board 1's file of
    the same drawing; where the guide draws the chart at another width, the kit draws it again at 1440 px for this test
    alone. A difference that panel 1 does not name is a warning for the data lead."""
    from PIL import Image, ImageChops
    S = C['slots']
    b1 = ROOT / S['board1_specimens']
    out = SCRATCH / 'board1-compare'
    need_run = [s for s in ids if pages.get(s, (DESK,))[0] != DESK]
    sig = sha(kit_shared_sig(), *[kit_sig(s, '', (1440,)) for s in need_run])
    stamp = out / 'sig.txt'
    if need_run and not (stamp.exists() and stamp.read_text() == sig):
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(['node', str(ROOT / S['kit_command']), 'build', *[s.lower() for s in need_run], '--widths', '1440', '--grounds', 'newsprint',
                            '--no-sweep', '--out', str(out), '--date', DATE], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        (SCRATCH / 'board1-compare.log').write_text(r.stdout + r.stderr)
        stamp.write_text(sig)
    named = {}
    for g in (D or {}).get('panels', []):
        if g.get('id') != C['sections']['forms']['b1_group']:
            continue
        for it in g.get('items', []):
            sp = item_spec(it)
            if sp:
                named.setdefault(sp, it.get('id'))
            for r_ in it.get('rows') or []:
                if r_.get('spec'):
                    named.setdefault(str(r_['spec']).upper(), it.get('id'))
    res = {}
    for sid in ids:
        lo = sid.lower()
        old = sorted(b1.glob(f'*_{sid}-*-Newsprint-1440.png'))
        new = sorted(((out if sid in need_run else kit_out) / lo).glob(f'{DATE}_{sid}-*-Newsprint-1440.png'))
        same = None
        if old and new:
            a, b = Image.open(old[-1]).convert('RGB'), Image.open(new[-1]).convert('RGB')
            same = a.size == b.size and ImageChops.difference(a, b).getbbox() is None
        else:
            warn(f'board 1 comparison for {sid}: a drawing file is missing')
        res[sid] = {'named_in_panel_1': named.get(sid), 'desk_pixels_same': same,
                    'files': [rel(old[-1]) if old else None, rel(new[-1]) if new else None]}
        if same is False and D is not None and sid not in named:
            warn(f'{sid}: its desk drawing differs from board 1’s pixel for pixel, and the decisions file’s board 1 group does not name it')
    FIG['board1_compare'] = res
    return res


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
    for p, _ in parts:
        need(pathlib.Path(p).exists(), f'missing picture {rel(p)} for {name}')
    if not any(lab for _, lab in parts):
        label_h = 0
    sig = sha(json.dumps([[str(p), file_sig(p), lab] for p, lab in parts] + [cols, gap, label_h, 'b2v2-webp']))
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
        canvas.save(out, 'WEBP', lossless=True, quality=100, method=4)
        CACHE[out.name] = sig
        w, h = W, H
    rec = {'src': f'img/{out.name}', 'file': out, 'w': w, 'h': h, 'source': ', '.join(rel(p) for p, _ in parts)}
    IMAGES[out.name] = rec
    return rec


def side_or_stack(paths, gap=24):
    ws = [png_size(p)[0] for p in paths]
    return len(paths) if sum(ws) + gap * (len(ws) - 1) <= CONTENT_W else 1


def frame(rec, alt, lazy=True):
    w, h = rec['w'], rec['h']
    region = w > REGION_W
    attrs = f' role="region" tabindex="0" aria-label="{esc(alt)}, {w} by {h} px; scrolls sideways when wider than the window"' if region else ''
    ld = ' loading="lazy"' if lazy else ''
    return f'<div class="frame"{attrs}><img src="{rec["src"]}" width="{w}" height="{h}" alt="{esc(alt)}"{ld} decoding="async"></div>'


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
PIC_KEYS = {}             # id(picture) -> (kind, key)


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
    FIG['decisions'] = {'file': rel(p), 'state': d.get('state'), 'updated_utc': d.get('updated_utc'), 'schema': d.get('schema')}
    return d


def all_pictures(d):
    for g in (d or {}).get('panels', []):
        for it in g.get('items', []):
            for pic in it.get('pictures', []) or []:
                yield it, pic


def item_spec(it):
    s = it.get('spec') or (it.get('id') if re.fullmatch(r'S\d\d', str(it.get('id', ''))) else None)
    return s.upper() if s else None


def pic_request(it, pic, n):
    """Where a picture comes from, before any capture runs: ('guide', key, element, width), ('kit', spec, ground, width),
    ('path', file) or ('file', key, path, width, ground, element)."""
    kind = pic.get('kind')
    spec = (pic.get('spec') or item_spec(it) or '').lower()
    w = int(pic.get('width') or DESK)
    g = (pic.get('ground') or 'newsprint').lower()
    if kind == 'guide':
        el = pic.get('element') or (f'oac-s-14-{spec}' if spec else None)
        if not el:
            warn(f'a guide picture in item {it.get("id")} names no element or spec')
            return None
        return ('guide', f'dec-{el}-{w}', el, w)
    if kind == 'kit':
        if not spec:
            warn(f'a kit picture in item {it.get("id")} names no spec')
            return None
        return ('kit', spec.upper(), g, w)
    path = pic.get('path')
    if not path:
        return ('missing', pic.get('label') or kind)
    fp = ROOT / path
    if not fp.exists():
        return ('missing', path)
    if fp.suffix.lower() in IMG_EXT:
        return ('path', fp)
    return ('file', f'file-{re.sub(r"[^A-Za-z0-9]+", "-", fp.stem)}-{g}-{w}', fp, w, g, pic.get('element'))


# ------------------------------------------------------------------------------------------------------- panel 1
def picture_html(it, pics, shots, fshots, kit_out, pages):
    """An item's pictures in the decisions file's order, each at true size with its label: a "before" opens a row that
    the "after" pictures following it join, so each before sits beside its afters; views sit in rows of their own."""
    out, n = [], 0
    for pic in pics:
        req = PIC_KEYS.get(id(pic))
        label = pic.get('label') or ''
        role = pic.get('role') or 'view'
        path = None
        if req is None:
            continue
        if req[0] == 'guide':
            path = shots.get(req[1])
        elif req[0] == 'kit':
            spec, g, w = req[1], req[2], req[3]
            ww = pages.get(spec, (DESK, PHONE))[0 if w >= 600 else 1]
            path = kit_out / spec.lower() / f'{spec.lower()}-{g}-{ww}.png'
        elif req[0] == 'path':
            path = req[1]
        elif req[0] == 'file':
            path = fshots.get(req[1])
        elif req[0] == 'missing':
            out.append((role, pending(fill(C['sections']['decide']['picture_wait'], {'path': req[1]}))))
            continue
        if not path or not pathlib.Path(path).exists():
            out.append((role, pending(fill(C['sections']['decide']['picture_wait'], {'path': label or req[1]}))))
            continue
        n += 1
        rec = compose(f'Decide-{re.sub(r"[^A-Za-z0-9]+", "-", str(it.get("id")))}-{n}', [(path, '')])
        alt = (f'{label}: ' if label else '') + (pic.get('alt') or it.get('title', ''))
        QUOTED.extend([label, pic.get('alt') or ''])
        rw = C['sections']['decide']['role_words'].get(role, '')
        cap_html = (f'<span class="role {esc(role)}">{esc(rw)}</span> ' if rw else '') + (f'<b>{esc(label)}</b>' if label else '')
        out.append((role, figure(rec, alt, cap_html, top=True)))
    rows, cur = [], None
    for r, h in out:
        kind = 'ba' if r in ('before', 'after') else 'view'
        if cur is None or r == 'before' or cur[0] != kind or (kind == 'ba' and r == 'before'):
            cur = [kind, []]
            rows.append(cur)
        cur[1].append(h)
    return ''.join(f'<div class="pair {k}">{"".join(hs)}</div>' for k, hs in rows)


def words(it, key):
    v = it.get(key)
    if v:
        QUOTED.append(v)
    return v


def rows_table(rows, caption):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys and k not in ('refs',):
                keys.append(k)
    names = C['sections']['decide']['row_heads']
    head = ''.join(f'<th scope="col">{esc(names.get(k, cap(k.replace("_", " "))))}</th>' for k in keys)
    body = ''
    for r in rows:
        cells = []
        for i, k in enumerate(keys):
            v = r.get(k, '')
            v = ', '.join(map(str, v)) if isinstance(v, list) else str(v)
            QUOTED.append(v)
            if k == 'rule' and v and rid_anchor(v) in ANCHORS:
                cell = f'<a href="{esc(rule_href(v))}">{esc(v)}</a>'
            else:
                cell = esc(v)
            cells.append(f'<th scope="row">{cell}</th>' if i == 0 else f'<td>{cell}</td>')
        body += '<tr>' + ''.join(cells) + '</tr>'
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{esc(caption)}; scrolls sideways"><table class="dt">'
            f'<caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def decide_panel(shots, fshots, kit_out, pages):
    S = C['sections']['decide']
    if D is None:
        return section('decide', f'<p class="intro">{esc(S["lede"])}</p>' + pending(S['wait']), ('waiting', 'data_lead'))
    refs = []
    parts = [f'<p class="intro">{esc(S["lede"])}</p>']
    toc = []
    n_items = n_q = 0
    missing = []
    for g in D.get('panels', []):
        gid = g.get('id', '')
        items = g.get('items', [])
        title = words(g, 'title') or gid
        toc.append(f'<li><a href="#d-{esc(gid)}">{esc(title)}</a> <span class="n">{len(items)}</span></li>')
        parts.append(f'<h3 class="sub grp" id="d-{esc(gid)}">{esc(title)}</h3>')
        if g.get('lede'):
            parts.append(f'<p class="intro">{esc(words(g, "lede"))}</p>')
        if g.get('approval') == 'one':
            parts.append(f'<p class="approve">{esc(S["approval_one"])}</p>')
        if not items:
            parts.append(pending(S['group_wait']))
            missing.append(gid)
        for it in items:
            n_items += 1
            spec, rule = item_spec(it), it.get('rule')
            refs += it.get('refs') or [] if isinstance(it.get('refs'), list) else re.split(r'[,;]\s*|\s+·\s+', it.get('refs') or '')
            q = bool(it.get('question_for_dustin'))
            n_q += q
            head = (f'<p class="label">{esc(join_words([x for x in [("Rule " + rule) if rule else "", spec or ""] if x]) or title)}</p>'
                    f'<h4 class="dec-h">{esc(words(it, "title") or it.get("id", ""))}'
                    + (f' <span class="tag q">{esc(S["tag_question"])}</span>' if q else '') + '</h4>')
            body = ''
            if it.get('answer'):
                body += f'<p class="dec-a">{esc(words(it, "answer"))}</p>'
            if it.get('question'):
                body += f'<p class="dec-q">{esc(words(it, "question"))}</p>'
            if it.get('recommendation'):
                body += f'<p class="dec-rec"><span class="tag rec">{esc(S["tag_rec"])}</span> {esc(words(it, "recommendation"))}</p>'
            dl = [(S['what_changed'], words(it, 'what_changed')), (S['why'], words(it, 'why'))]
            dl = [(a, b) for a, b in dl if b]
            if dl:
                body += '<dl class="facts f2">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in dl) + '</dl>'
            for v in it.get('views') or []:
                QUOTED.extend([v.get('text', ''), v.get('note', '')])
                body += (f'<blockquote class="q"><p>{esc(v.get("text", ""))}</p><footer>{esc(fill(S["view_by"], {"who": v.get("who", "")}))}'
                         + (f' {esc(v["note"])}' if v.get('note') else '') + '</footer></blockquote>')
            pr_, bu_ = (it.get('plan_row') or {}).get('said'), it.get('built')
            if pr_ or bu_:
                QUOTED.extend([pr_ or '', bu_ or ''])
                body += ('<dl class="facts f2">' + (f'<div><dt>{esc(S["plan_said"])}</dt><dd>{B1.md_inline(pr_, quote=False)}</dd></div>' if pr_ else '')
                         + (f'<div><dt>{esc(S["built_k"])}</dt><dd>{B1.md_inline(bu_, quote=False)}</dd></div>' if bu_ else '') + '</dl>')
            if it.get('old') or it.get('new'):
                body += (f'<div class="oldnew"><div><p class="row-label">{esc(S["old"])}</p><p class="was">{esc(words(it, "old") or "")}</p></div>'
                         f'<div><p class="row-label">{esc(S["new"])}</p><p class="now">{esc(words(it, "new") or "")}</p></div></div>')
            if it.get('facts'):
                # a fact whose value names a file goes to the panel's reference line, where file paths belong
                fpath = [f for f in it['facts'] if re.search(PATH_RE, str(f.get('value', '')))]
                shown = [f for f in it['facts'] if f not in fpath]
                refs += [f'{f.get("label", "")}: {f.get("value", "")}' for f in fpath]
                if shown:
                    body += '<dl class="facts">' + ''.join(f'<div><dt>{esc(f.get("label", ""))}</dt><dd>{esc(f.get("value", ""))}</dd></div>' for f in shown) + '</dl>'
                QUOTED.extend(f.get('label', '') + ' ' + str(f.get('value', '')) for f in shown)
            if it.get('rows'):
                body += rows_table(it['rows'], fill(S['rows_caption'], {'title': it.get('title', '')}))
                for r_ in it['rows']:
                    rr = r_.get('refs') or []
                    refs += rr if isinstance(rr, list) else re.split(r'[,;]\s*', rr)
            if it.get('pictures'):
                ph = picture_html(it, it['pictures'], shots, fshots, kit_out, pages)
                if 'class="pending"' in ph:
                    missing.append(it.get('id'))
                body += ph
            if rule and rid_anchor(rule) in ANCHORS:
                body += f'<p class="small"><a href="{esc(rule_href(rule))}">{esc(fill(S["entry_link"], {"rule": rule}))}</a></p>'
            parts.append(f'<article class="dec" id="d-{esc(re.sub(r"[^A-Za-z0-9-]+", "-", str(it.get("id"))))}">{head}{body}</article>')
    reply = D.get('reply_line') or S['reply']
    QUOTED.append(reply)
    parts.insert(1, f'<nav class="dtoc" aria-label="{esc(S["toc_h"])}"><ol>{"".join(toc)}</ol></nav>')
    parts.append(f'<p class="reply">{esc(reply)}</p>')
    FIG['decide'] = {'items': n_items, 'questions': n_q, 'state': D.get('state'), 'pictures_waiting': missing}
    FILL.update({'n_items': n_items, 'n_questions_w': nw(n_q)})
    refs = [r.strip() for r in refs if r and r.strip()]
    st = 'ready' if D.get('state') == 'signed off' and not missing else ('partial', 'data_lead' if D.get('state') != 'signed off' else 'pictures')
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


def form_article(G, f, held, S, kit_out, pages, b1cmp, rendered, sk_shots):
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
            body = figure(im, f'The sketch for Rule {rid}, headed “{hd}”, with its caption, as the guide prints it at a 1440 px window, at true size. {wd}', capt)
            ok = True
        else:
            body = pending(S['wait_photo'])
            ok = False
        rec.update({'kind': kind or 'sketch', 'specimen': specimen, 'heading': hd, 'caption': wd})
        return f'<article class="form sk" id="{aid}">{head}{body}</article>', rec, ok
    # a form with a specimen
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
        warn(f'{sid} was not found in the guide')
    est = ev.strip().lower() == C['sections']['forms']['estimate_label'].lower()
    head += (f'<p class="f-q"><span class="k">{esc(S["question"])}</span> {esc(q)}</p>' if q else '')
    head += f'<div class="f-ev"><span class="ev-k{" est" if est else ""}">{esc(ev)}</span><p class="f-ct">{esc(title)}</p></div></header>'
    b1 = sid in C['board1_ids']
    notes = []
    b1_link = None
    if b1:
        cmp_ = b1cmp.get(sid) or {}
        if cmp_.get('named_in_panel_1'):
            notes.append(S['b1_named'])
            b1_link = f'#d-{re.sub(r"[^A-Za-z0-9-]+", "-", str(cmp_["named_in_panel_1"]))}'
        elif cmp_.get('desk_pixels_same'):
            notes.append(S['b1_same'])
        elif cmp_.get('desk_pixels_same') is False:
            notes.append(S['b1_differs'])
        else:
            notes.append(S['b1_unknown'])
    if sid in rendered:
        notes.append(fill(S['shared_spec'], {'rule': rendered[sid]}))
    d = kit_out / lo
    chk_p = d / f'{lo}-check.json'
    dp, pw = pages.get(sid, (DESK, PHONE))
    caps = {(g, w, x): d / f'{lo}-{g}-{w}{x}.png' for g in ('newsprint', 'charcoal') for w in (dp, pw) for x in ('', '-grayscale')}
    body = ''
    if notes:
        body += '<p class="what">' + ' '.join(esc(n) for n in notes) + (f' <a href="{b1_link}">{esc(S["b1_link"])}</a>' if b1_link else '') + '</p>'
    ok = True
    if not chk_p.exists() or not all(p.exists() for p in caps.values()):
        body += pending(S['wait_kit'])
        ok = False
    else:
        chk = json.loads(chk_p.read_text())
        dw = {(x['ground'], x['page']): x['width'] for x in chk.get('drawings', [])}
        lab = lambda w: fill(S['label_desk'] if w == dp else S['label_phone'], {'px': dw.get(('newsprint', w), '?')})
        if sid in rendered:
            stem = f'Form-{sid}'
        else:
            stem = f'Form-{sid}'
        alt = text_of(spec.get('alt', ''))
        pics = []
        for g, gname in (('newsprint', S['row_newsprint']), ('charcoal', S['row_charcoal'])):
            pp = [caps[(g, dp, '')], caps[(g, pw, '')]]
            im = compose(f'{stem}-{cap(g)}', [(pp[0], lab(dp)), (pp[1], lab(pw))], cols=side_or_stack(pp))
            a = f'{f["form"]}, Rule {rid}, on {cap(g)}, drawn for a {DESK} px window and a {PHONE} px window, as the guide draws them.' + (f' {alt}' if g == 'newsprint' else '')
            pics.append(f'<p class="row-label">{esc(gname)}</p>{frame(im, a)}')
        gp = [(caps[('newsprint', dp, '-grayscale')], fill(S['gray_label'], {'g': 'Newsprint', 'w': DESK})), (caps[('newsprint', pw, '-grayscale')], fill(S['gray_label'], {'g': 'Newsprint', 'w': PHONE})),
              (caps[('charcoal', dp, '-grayscale')], fill(S['gray_label'], {'g': 'Charcoal', 'w': DESK})), (caps[('charcoal', pw, '-grayscale')], fill(S['gray_label'], {'g': 'Charcoal', 'w': PHONE}))]
        cols = 2 if side_or_stack([gp[0][0], gp[1][0]]) == 2 else 1
        im = compose(f'{stem}-Grayscale', gp, cols=cols)
        pics.append(f'<details class="more gray"><summary>{esc(S["row_gray"])}</summary>{frame(im, f"{f["form"]}, Rule {rid}, in grayscale: Newsprint and Charcoal, each at a {DESK} px window and a {PHONE} px window.")}</details>')
        body += ''.join(pics)
        faults = chk.get('faults', [])
        wt = chk.get('weight') or {}
        wf = wt.get('with_frame')
        bytes_line = fill(S['bytes_line'], {'with_frame': f'{wf:,}' if wf else '?', 'figure': f'{wt.get("figure", 0):,}'})
        result = S['kit_pass'] if not faults else fill(S['kit_faults'], {'n': nw(len(faults))})
        src = pr.get('source')
        if src:
            body += f'<p class="src">{esc(src)}</p>'
        body += f'<p class="ch-line">{esc(bytes_line)} {esc(result)}</p>'
        if faults:
            ok = False
            QUOTED.extend(faults[:3])
            body += '<ul class="faults">' + ''.join(f'<li>{esc(B1.strip_codes(str(x))[:200])}</li>' for x in faults[:3]) + '</ul>'
        rec.update({'with_frame': wf, 'figure_bytes': wt.get('figure'), 'faults': len(faults), 'kit_windows': [dp, pw], 'drawn': {f'{g} {p}': w for (g, p), w in dw.items()}})
    if pr.get('table'):
        capm = re.search(r'<caption>(.*?)</caption>', pr['table'], flags=re.S)
        cname = text_of(capm.group(1)) if capm else f'The table for Rule {rid}'
        QUOTED.append(cname)
        QUOTED.append(text_of(pr['table']))
        body += f'<details class="more"><summary>{esc(S["table_summary"])}<span class="vh">: {esc(cname)}</span></summary>{clean_table(pr["table"], cname)}</details>'
    elif G['usable']:
        warn(f'{sid}: the guide prints no table')
    rec.update({'spec': sid, 'title': title, 'evidence': ev, 'estimate': est, 'board_1': b1, 'question': q})
    rendered.setdefault(sid, rid)
    return f'<article class="form" id="{aid}">{head}{body}</article>', rec, ok


def forms_panel(G, P, rn, held, kit_out, pages, b1cmp, sk_shots):
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
        body, rec, ok = form_article(G, f, held, S, kit_out, pages, b1cmp, rendered, sk_shots)
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
    lede = f'<p class="intro">{esc(fill(S["lede"]))}</p><p>{esc(fill(S["how"]))}</p>' + (f'<p>{esc(fill(S["lede_est"]))}</p>' if est else '')
    st = 'ready' if not missing and G['ok'] else ('partial', 'build' if not G['ok'] else 'kit')
    if missing:
        lede += pending(fill(S['wait_some'], {'list': join_words(missing[:12]) + (f' and {len(missing) - 12} more' if len(missing) > 12 else '')}))
    return section('forms', lede + nav + ''.join(parts), st)


# ------------------------------------------------------------------------------------------------------- panel 3
def caption_text(x):
    return text_of(x.get('caption', '')) if isinstance(x, dict) else ''


def rules_panel(G, ch, held, shots):
    S = C['sections']['rules']
    ids = [f'14.{i}' for i in range(1, 15)]
    out, missing = [f'<p class="intro">{esc(S["lede"])}</p>'], []
    op = (ch.get('opener') or {}).get('specimen')
    if op and shots.get('ch14-opener', pathlib.Path('-')).exists():
        rec = compose('Ch14-Opener', [(shots['ch14-opener'], '')])
        ct = caption_text(ch['opener'])
        QUOTED.append(ct)
        out.append(f'<h3 class="sub">{esc(S["opener_h"])}</h3>' + figure(rec, f'Chapter 14’s opening plate at a 1440 px window. {ct}', esc(ct)))
    elif op:
        missing.append('the opener')
    for rid in ids:
        r = held.get(rid)
        if not r:
            warn(f'chapter 14 holds no Rule {rid}')
            continue
        keys = [f'plate-{rid}-{k}' for k in ('correct', 'failure') if isinstance(r.get(k), dict)]
        have = [k for k in keys if shots.get(k, pathlib.Path('-')).exists()]
        QUOTED.append(r['title'])
        link = f' <a class="live" href="{esc(rule_href(rid))}">{esc(C["sections"]["forms"]["live"])}</a>' if rid_anchor(rid) in ANCHORS else ''
        h = f'<h3 class="r-h" id="r-{rid.replace(".", "-")}"><span class="rid">Rule {esc(rid)}{link}</span> {esc(r["title"])}</h3>'
        if len(have) < len(keys) or not keys:
            missing.append(f'Rule {rid}')
            out.append(f'<article class="rule">{h}{pending(S["wait"])}</article>')
            continue
        side = side_or_stack([shots[k] for k in have])
        rec = compose(f'Rule-{rid.replace(".", "-")}-Plates', [(shots[k], '') for k in have], cols=side, gap=24 if side > 1 else 32)
        cc, fc = caption_text(r.get('correct')), caption_text(r.get('failure'))
        alt = (f'Rule {rid}: the correct plate, then the failure plate, ' + ('side by side' if side > 1 else 'one above the other')
               + f', as the guide draws them at a 1440 px window. Correct: {cc} Failure: {fc}')
        out.append(f'<article class="rule">{h}{figure(rec, alt)}</article>')
        FIG.setdefault('rules', {})[rid] = {'plates': len(have), 'layout': 'side by side' if side > 1 else 'stacked', 'size': [rec['w'], rec['h']]}
    if missing:
        warn('plates not photographed: ' + ', '.join(missing))
    return section('rules', ''.join(out), 'ready' if not missing else ('partial', 'render'))


# ------------------------------------------------------------------------------------------------------- panel 4
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


def count_panel():
    S = C['sections']['count']
    k = (D or {}).get('counts')
    if not k:
        return section('count', f'<p class="intro">{esc(S["lede"])}</p>' + pending(S['wait']), ('waiting', 'data_lead'))
    r9 = k.get('rule_01_9') or {}
    out = [f'<p class="intro">{esc(S["lede"])}</p>']
    facts = []
    if r9:
        lim = r9.get('limits', {})
        bt = (r9.get('built') or {}).get('examples')
        if bt is not None:
            facts.append((S['facts']['built'], f'{bt}'))
        facts += [(S['facts']['total'], f'{r9.get("total_examples", "?")}'), (S['facts']['ruling'], f'{r9.get("ruling_g", "?")}'),
                  (S['facts']['recount'], f'{r9.get("recount", "?")}'), (S['facts']['limits'], fill(S['limits_words'], {'d': lim.get('domain', '?'), 's': lim.get('state', '?')}))]
    out.append('<dl class="facts">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in facts) + '</dl>')
    if r9.get('note'):
        QUOTED.append(r9['note'])
        out.append(f'<p>{esc(r9["note"])}</p>')
    for key, h in (('by_domain', S['domain_h']), ('by_state', S['state_h'])):
        rows = r9.get(key) or []
        if rows:
            name_k = 'domain' if key == 'by_domain' else 'state'
            out.append(f'<h3 class="sub">{esc(h)}</h3>')
            out.append(bar_rows([(str(x.get('title') or x.get(name_k, '')), int(x.get('count', 0)), x.get('limit'), bool(x.get('passes', True))) for x in rows], S['cols'],
                                fill(S['caption'], {'what': h.lower()})))
    dr = k.get('dr_229') or {}
    if dr:
        out.append(f'<h3 class="sub">{esc(S["dr229_h"])}</h3>')
        if dr.get('test'):
            QUOTED.append(dr['test'])
            out.append(f'<p>{esc(dr["test"])}</p>')
        if dr.get('count') is not None:
            out.append(f'<p class="big">{esc(fill(S["dr229_count"], {"n": dr["count"]}))}</p>')
        df = [(lab, dr[k]) for k, lab in S['dr229_facts'].items() if dr.get(k) is not None]
        if df:
            out.append('<dl class="facts">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in df) + '</dl>')
        ex = dr.get('examples') or dr.get('forms') or []
        if ex:
            cols = [c for c in S['dr229_cols'] if any(c in x for x in ex)]
            yn = lambda v: (S['pass_words'] if v else S['fail_words']) if isinstance(v, bool) else v
            out.append(rows_table([{c: yn(x.get(c, '')) for c in cols} for x in ex], S['dr229_caption']))
        if dr.get('note'):
            QUOTED.append(dr['note'])
            out.append(f'<p>{esc(dr["note"])}</p>')
    FIG['count'] = {'recount': r9.get('recount'), 'ruling_g': r9.get('ruling_g'), 'dr_229': dr.get('count')}
    st = 'ready' if (D or {}).get('state') == 'signed off' else ('partial', 'data_lead')
    return section('count', ''.join(out), st, fill(S['script_ref'], {'script': k.get('script', '')}) if k.get('script') else '')


# ------------------------------------------------------------------------------------------------------- panel 5
def spend_panel(G, rn, kit_out):
    S = C['sections']['spend']
    if not G['report']:
        return section('spend', pending(S['wait']), ('waiting', 'build'))
    W = G['report'].get('weight', {})
    pj = W.get('projection', {})
    pp = pj.get('chapter_14_per_plate', {})
    mg = pj.get('map_geometry', {})
    cr = pj.get('chapter_14_rules', {}) or W.get('chapter_14_parts', {})
    parts = W.get('parts', {})
    kit = int(parts.get('chart kit', 0))
    stop = int(pp.get('stop') or W.get('chapters', {}).get('14', {}).get('budget') or 0)
    budget = int(pj.get('budget') or W.get('budget_page') or 0)
    rows = [(S['rows']['ch14'], int(pj.get('chapter_14_with_kit', 0)), stop),
            (S['rows']['kit'], kit, None),
            (S['rows']['geo'], int(mg.get('bytes', 0)), int(mg.get('allowance', 0))),
            (S['rows']['rules'], int(cr.get('rules_and_opener', 0)), int(cr.get('allowance', 0))),
            (S['rows']['page'], int(pj.get('projected_bytes', 0)), budget)]
    FILL.update({'ch14_kit': f'{int(pj.get("chapter_14_with_kit", 0)):,}', 'stop': f'{stop:,}', 'kit': f'{kit:,}', 'geo': f'{int(mg.get("bytes", 0)):,}',
                 'geo_allow': f'{int(mg.get("allowance", 0)):,}', 'geo_room': f'{int(mg.get("room", 0)):,}', 'rules_b': f'{int(cr.get("rules_and_opener", 0)):,}',
                 'rules_allow': f'{int(cr.get("allowance", 0)):,}', 'per_plate': f'{int(pp.get("per_plate", 0)):,}', 'to_come': pp.get('plates_to_come', '?'),
                 'proj': f'{int(pj.get("projected_bytes", 0)):,}', 'budget_mb': f'{budget / 1e6:g}', 'proj_room': f'{budget - int(pj.get("projected_bytes", 0)):,}',
                 'page_now': f'{int(W.get("bytes", 0)):,}', 'build_when': when_utc(G['mtime']) if G.get('mtime') else ''})
    trs = ''
    for name, b, lim in rows:
        share = 100 * b / lim if lim else None
        bar = (f'<span class="bar" data-mark="bar" data-value="{share:.3f}" data-key="{esc(name)}" style="width:{min(share, 100):.3f}%"></span><span class="pct">{share:.1f} percent</span>'
               if share is not None else f'<span class="pct">{esc(S["no_limit"])}</span>')
        trs += f'<tr><th scope="row">{esc(name)}</th><td class="barcell">{bar}</td><td class="num">{b:,}</td><td class="num">{"" if lim is None else f"{lim:,}"}</td></tr>'
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if i >= 2 else ""}>{esc(c)}</th>' for i, c in enumerate(S['cols']))
    body = (f'<p class="intro">{esc(fill(S["lede"]))}</p>'
            f'<figure class="wfig"><div class="tw" role="region" tabindex="0" aria-label="{esc(S["caption"])}; scrolls sideways"><table class="wt">'
            f'<caption>{esc(S["caption"])}</caption><thead><tr>{hd}</tr></thead><tbody>{trs}</tbody></table></div></figure>'
            f'<p>{esc(fill(S["per_plate"]))}</p><p>{esc(fill(S["geo_line"]))}</p><p>{esc(fill(S["page_line"]))}</p>')
    # bytes by family: each plate's bytes as the build placed it, and each sketch entry's, summed by the plan's families
    charts = W.get('charts', {})
    sk = {x['rule']: x for x in W.get('chapter_14_parts', {}).get('sketch_entries', [])}
    P = json.loads((ROOT / C['slots']['plan']).read_text())
    titles = {g.get('family_section'): g['title'] for g in P['groups']}
    fam, seen = {}, set()
    for f in rn:
        fs = f['family_section']
        e = fam.setdefault(fs, [0, 0, 0])
        if f.get('spec_id') and f['spec_id'] not in seen:
            seen.add(f['spec_id'])
            b = (charts.get(f's-14-{f["spec_id"].lower()}') or {}).get('bytes')
            if b:
                e[0] += int(b)
                e[1] += 1
        elif f['status'] == 'sketch' and f['rule'] in sk:
            e[0] += int(sk[f['rule']]['bytes'])
            e[2] += 1
    frows = ''
    mx = max([v[0] for v in fam.values()] + [1])
    for fs, (b, n, m) in fam.items():
        t = re.sub(r':.*$', '', titles.get(fs, fs))
        frows += (f'<tr><th scope="row">{esc(t)}</th><td class="barcell"><span class="bar" data-mark="bar" data-value="{b}" data-key="{esc(t)}" style="width:{100 * b / mx:.3f}%"></span></td>'
                  f'<td class="num">{n}</td><td class="num">{m}</td><td class="num">{b:,}</td></tr>')
    body += (f'<h3 class="sub">{esc(S["fam_h"])}</h3><p>{esc(S["fam_lede"])}</p><div class="tw" role="region" tabindex="0" aria-label="{esc(S["fam_caption"])}; scrolls sideways">'
             f'<table class="wt ft2"><caption>{esc(S["fam_caption"])}</caption><thead><tr>' + ''.join(f'<th scope="col"{" class=\"n\"" if i >= 2 else ""}>{esc(c)}</th>' for i, c in enumerate(S['fam_cols']))
             + f'</tr></thead><tbody>{frows}</tbody></table></div>')
    # the heaviest plates, with the kit's measure with the plate's frame
    plates = []
    for sid in sorted({f['spec_id'] for f in rn if f.get('spec_id')}):
        c = charts.get(f's-14-{sid.lower()}') or {}
        chk_p = kit_out / sid.lower() / f'{sid.lower()}-check.json'
        wf = (json.loads(chk_p.read_text()).get('weight') or {}).get('with_frame') if chk_p.exists() else None
        rule = next((f['rule'] for f in rn if f.get('spec_id') == sid), '')
        form = next((f['form'] for f in rn if f.get('spec_id') == sid), '')
        plates.append((int(c.get('bytes') or 0), sid, rule, form, wf))
    plates.sort(reverse=True)
    top = plates[:int(S.get('heaviest_n', 10))]
    hrows = ''.join(f'<tr><th scope="row">{esc(sid)}</th><td><a href="#form-{rule.replace(".", "-")}">{esc(rule)}</a></td><td>{esc(form)}</td><td class="num">{b:,}</td><td class="num">{"" if wf is None else f"{wf:,}"}</td></tr>'
                    for b, sid, rule, form, wf in top)
    body += (f'<h3 class="sub">{esc(fill(S["heavy_h"], {"n": len(top)}))}</h3><div class="tw" role="region" tabindex="0" aria-label="{esc(S["heavy_caption"])}; scrolls sideways">'
             f'<table class="wt ht"><caption>{esc(S["heavy_caption"])}</caption><thead><tr>' + ''.join(f'<th scope="col"{" class=\"n\"" if i >= 3 else ""}>{esc(c)}</th>' for i, c in enumerate(S['heavy_cols']))
             + f'</tr></thead><tbody>{hrows}</tbody></table></div><p class="small">{esc(S["heavy_note"])}</p>')
    FIG['spend'] = {'rows': rows, 'per_plate': pp.get('per_plate'), 'plates_to_come': pp.get('plates_to_come'), 'by_family': fam, 'heaviest': top}
    return section('spend', body, 'ready' if G['ok'] else ('partial', 'build'))


# ------------------------------------------------------------------------------------------------------- panel 6
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
    """The first "N of 5" under a heading that names a score, the heading's own words included; a half point kept."""
    for m in re.finditer(r'^(#+)\s*(?:\d+\.\s*)?(.*\bscore\b.*)$', part, flags=re.M | re.I):
        nxt = re.search(r'^#+\s', part[m.end():], flags=re.M)
        block = m.group(2) + '\n' + part[m.end():m.end() + (nxt.start() if nxt else len(part))]
        s = re.search(r'\b([1-5](?:\.\d)?)\s*(?:out\s+)?of\s+5\b|\b([1-5](?:\.\d)?)\s*/\s*5\b', block)
        if s:
            v = s.group(1) or s.group(2)
            return float(v) if '.' in v else int(v)
    return None


def red_team(rt):
    t = read(rt['file'])
    if t is None:
        return {'name': rt['name'], 'round': rt['round'], 'state': 'missing'}
    m = re.search(r'^##\s+(?:\d+\.\s*)?Second pass\b.*$', t, flags=re.M | re.I)
    first_part, second_part = (t[:m.start()], t[m.start():]) if m else (t, '')
    score = score_in(first_part)
    score2 = score_in(second_part) if second_part else None
    mf = findings(B1.md_section(first_part, [r'(?:\d+\.\s*)?must fix']))
    sf = findings(B1.md_section(first_part, [r'(?:\d+\.\s*)?should fix']))
    state = 'ready' if score is not None and mf is not None and sf is not None else 'waiting'
    if second_part and score2 is None:
        warn(f'round {rt["round"]} {rt["name"]}: its second pass gives no score')
    return {'name': rt['name'], 'round': rt['round'], 'state': state, 'score': score, 'must_fix': mf, 'should_fix': sf, 'second_score': score2, 'file': rt['file']}


def drop_ids(s):
    rid = r'[A-Z]{1,4}\d{0,3}(?:-[A-Z]{1,3})?-?\d{1,3}'
    return re.sub(r'\s*\((?:' + rid + r'(?:,\s*|\s+and\s+|;\s*)?)+\)', '', s or '')


def short_name(s):
    """An item's name as the scores print it: the words before its parenthesis."""
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
        fs = (f_items.get(it.get('key'), {}) or {}).get('scores') or {}

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
    out = [f'<p class="intro">{esc(S["lede"])}</p><p class="small">{esc(S["legend"])}</p>']
    status = 'ready'
    summ = []
    for rnd in C['rounds']:
        sl = C['slots']['scores'][str(rnd)]
        fp, rp = ROOT / sl['first'], ROOT / sl['rescore']
        first = json.loads(fp.read_text()) if fp.exists() else None
        rescore = json.loads(rp.read_text()) if rp.exists() else None
        if not first:
            out.append(pending(fill(S['wait_round'], {'r': rnd})))
            status = ('partial', 'cd')
            continue
        tbl, fr, nr, n = cd_table(first, rescore, fill(S['cd_caption'], {'r': rnd}))
        line = fill(S['cd_line'], {'r': rnd, 'first': nw(fr, 'none'), 'now': 'all ' + nw(nr) if nr == n else nw(nr, 'none'), 'n': nw(n)})
        out.append(f'<h3 class="sub">{esc(fill(S["cd_h"], {"r": rnd}))}</h3><p>{esc(line)}</p>{tbl}')
        summ.append({'round': rnd, 'first_ready': fr, 'now_ready': nr, 'items': n})
    # the red teams
    rts = [red_team(rt) for rt in C['slots']['red_teams']]
    trs = []
    for r in rts:
        if r['state'] != 'ready':
            trs.append(f'<tr><th scope="row">{esc(r["name"])}</th><td class="num">{r["round"]}</td><td colspan="4">{esc(S["rt_wait"])}</td></tr>')
            status = ('partial', 'red')
            continue
        s2 = f'{r["second_score"]} of 5' if r.get('second_score') is not None else esc(S['rt_wait2'])
        trs.append(f'<tr><th scope="row">{esc(r["name"])}</th><td class="num">{r["round"]}</td><td class="num">{r["score"]} of 5</td><td class="num">{r["must_fix"]}</td>'
                   f'<td class="num">{r["should_fix"]}</td><td class="num">{s2}</td></tr>')
    hd = ''.join(f'<th scope="col"{" class=\"n\"" if i >= 1 else ""}>{esc(c)}</th>' for i, c in enumerate(S['rt_cols']))
    out.append(f'<h3 class="sub">{esc(S["rt_h"])}</h3><p>{esc(S["rt_lede"])}</p>'
               f'<div class="tw" role="region" tabindex="0" aria-label="{esc(S["rt_h"])}; scrolls sideways"><table class="rt"><caption>{esc(S["rt_h"])}</caption><thead><tr>{hd}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    # the board's own score, when it lands
    bp = ROOT / C['slots']['board_scores']
    out.append(f'<h3 class="sub">{esc(S["board_h"])}</h3>')
    if bp.exists():
        try:
            B = json.loads(bp.read_text())
            tbl, fr, nr, n = cd_table(B, None, S['board_caption'])
            out.append(tbl)
            FIG['board_score'] = {'file': rel(bp), 'ready': nr, 'items': n}
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            warn(f'{rel(bp)} could not be read: {e}')
            out.append(pending(S['board_wait']))
            status = status if status != 'ready' else ('partial', 'cd_board')
    else:
        out.append(pending(S['board_wait']))
        status = status if status != 'ready' else ('partial', 'cd_board')
    FIG['scores'] = {'cd': summ, 'red_teams': rts}
    return section('scores', ''.join(out), status)


# ------------------------------------------------------------------------------------------------------- panel 7
def tested_panel(G, kit_out, all_specs):
    S = C['sections']['tested']
    rows, missing = [], []
    for it in S['tested']:
        kind, w = it.get('kind'), None
        if kind == 'build':
            rep = G['report']
            if G['ok']:
                w = fill(it['words'], {'bytes': f'{rep.get("bytes", 0):,}', 'warnings': nw(len(rep.get('warnings', []))), 'rules': rep.get('rules'),
                                       'specimens': rep.get('specimens_placed'), 'when': when_utc(G['mtime'])})
            elif rep:
                w = fill(it['words_failed'], {'exit': FIG['guide_build']['exit']})
        elif kind == 'guide_check':
            p = SCRATCH_ROOT / it['scratch_file']
            if p.exists():
                J = json.loads(p.read_text())
                runs = J.get('runs') if isinstance(J.get('runs'), list) else []
                widths = [str(r.get('width')) for r in runs if r.get('width')]
                r0 = runs[0] if runs else {}
                sp = (r0.get('specimens') or {}).get('stages') if isinstance(r0.get('specimens'), dict) else None
                an = (r0.get('anchors') or {}).get('links') if isinstance(r0.get('anchors'), dict) else None
                pg = p.with_name(re.sub(r'-Guide-Check-Results\.json$', '.html', p.name))
                w = fill(it['words'], {'widths': join_words(widths), 'failures': nw(len(J.get('failures', []))), 'specimens': f'{sp:,}' if sp else '?',
                                       'links': f'{an:,}' if an else '?', 'page_bytes': f'{pg.stat().st_size:,}' if pg.exists() else '?'})
                FIG['guide_check'] = {'file': '[scratch]/' + it['scratch_file'], 'failures': J.get('failures'), 'pass': J.get('pass'),
                                      'page_bytes': pg.stat().st_size if pg.exists() else None}
                if pg.exists() and G['report'].get('bytes') and pg.stat().st_size != G['report']['bytes']:
                    warn(f'the quick guide check ran on {pg.stat().st_size:,} bytes and this board’s strict build is {G["report"]["bytes"]:,}')
        elif kind == 'kit':
            fs = [kit_out / s.lower() / f'{s.lower()}-check.json' for s in all_specs]
            fs = [f for f in fs if f.exists()]
            if fs:
                ok_n = sum(1 for f in fs if not json.loads(f.read_text()).get('faults'))
                wn = sum(len(json.loads(f.read_text()).get('warnings') or []) for f in fs)
                w = fill(it['words'], {'pass': f'{ok_n:,}', 'n': f'{len(fs):,}', 'warnings': nw(wn)})
                FIG['kit_checks'] = {'check_files': len(fs), 'pass': ok_n, 'warnings': wn}
        elif kind == 'board_check':
            p = BOARD_DIR / f'{DATE}_Board-2-Check-Results.json'
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
            missing.append(it['label'])
            w = S['wait_words']
        rows.append(f'<li><b>{esc(it["label"])}:</b> {esc(w if w.endswith(".") else w + ".")}</li>')
        FIG.setdefault('tested', {})[it['label']] = w
    nots = ''.join(f'<li>{esc(x)}</li>' for x in S['not_tested'])
    body = (f'<p class="intro">{esc(S["lede"])}</p><div class="tcols">'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["tested_h"])}</h3><ul>{"".join(rows)}</ul></div>'
            f'<div class="tcol"><h3 class="tcol-h">{esc(S["not_h"])}</h3><ul>{nots}</ul></div></div>')
    return section('tested', body, 'ready' if not missing else ('partial', 'notes'))


def next_panel():
    S = C['sections']['next']
    return section('next', f'<p class="intro">{esc(S["line"])}</p>', 'ready')


# ------------------------------------------------------------------------------------------------------- page
ORDER = ['decide', 'forms', 'rules', 'count', 'spend', 'scores', 'tested', 'next']


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
table.ft{min-width:24rem}
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
    own_page = re.sub(r'<div class="tw"[^>]*><table class="ft">.*?</table></div>', ' ', page, flags=re.S)
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
    print('the board itself: ' + ('PASS' if not fails1 else f'{len(fails1)} failures: ' + '; '.join(fails1[:6])))
    print('the board as the host wraps it: ' + ('PASS' if not fails2 else f'{len(fails2)} failures: ' + '; '.join(fails2[:6])))
    FIG['check'] = {'page': {'failures': fails1, 'allowed': [f for f in fails1 if f not in other], 'results': rel(out.with_name(out.stem + '-Check-Results.json'))},
                    'wrapped': {'failures': fails2, 'pass': J2.get('pass'), 'results': '[scratch]/phase-3/board-2/builder/publish-view/' + wrapped.stem + '-Check-Results.json'},
                    'widths': [x.get('width') for x in J2.get('runs', [])]}
    if other:
        warn('the board check failed: ' + '; '.join(other[:6]))
    if fails2:
        warn('the wrapped board check failed: ' + '; '.join(fails2[:6]))
    return not other and not fails2


DECISIONS_PATH = None


def main():
    global C, D, LOG, SCRATCH, CACHE, DECISIONS_PATH
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--reuse', action='store_true', help='keep kit captures and guide photographs whose sources have not changed')
    ap.add_argument('--check', action='store_true', help='run dataviz_check.js --board on the board and on a wrapped copy')
    ap.add_argument('--strict', action='store_true', help='exit 1 on any warning')
    ap.add_argument('--scratch', type=pathlib.Path, default=SCRATCH_DEFAULT)
    ap.add_argument('--out', type=pathlib.Path, default=OUT)
    ap.add_argument('--decisions', type=pathlib.Path, help='read the decisions from this file, for a test only')
    a = ap.parse_args()
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
    ch, held = chapter14()
    D = decisions()
    specs = sorted({f['spec_id'] for f in rn if f.get('spec_id')}, key=lambda s: int(s[1:]))
    # 1. the guide: measure each chart's drawing at both windows, and photograph sketches, plates and panel 1's pictures
    shots = {}
    items = []
    if G['usable']:
        for sid in specs:
            items += [(f'm-{sid}-{w}', f'oac-s-14-{sid.lower()}', w, 'measure') for w in (DESK, PHONE)]
        for f in rn:
            if f['status'] == 'sketch':
                sp = f.get('sketch_id') or (held.get(f['rule'], {}).get('correct') or {}).get('specimen')
                items.append((f'sketch-{f["rule"]}', f'fig-{sp}', DESK))
        if (ch.get('opener') or {}).get('specimen'):
            items.append(('ch14-opener', f'fig-{ch["opener"]["specimen"]}', DESK))
        for i in range(1, 15):
            r = held.get(f'14.{i}', {})
            for k in ('correct', 'failure'):
                sp = (r.get(k) or {}).get('specimen')
                if sp:
                    items.append((f'plate-14.{i}-{k}', f'fig-{sp}', DESK))
    freqs = []
    for it, pic in all_pictures(D):
        req = pic_request(it, pic, 0)
        PIC_KEYS[id(pic)] = req
        if req and req[0] == 'guide' and G['usable']:
            items.append((req[1], req[2], req[3]))
        elif req and req[0] == 'file':
            freqs.append(req[1:])
            if req[5] and G['usable']:
                items.append((f'dec-{req[5]}-{req[3]}', req[5], req[3]))
    if items:
        shots = run_shots(G, list({x[0]: x for x in items}.values()), a.reuse)
    fshots = file_shots(G, list({x[0]: x for x in freqs}.values()), a.reuse, shots) if freqs and G['usable'] else {}
    # 2. the kit, at the window widths that give the guide's drawing widths
    # the kit's window for each drawing: its own 1440 px where the guide draws the chart at 720 px (the reading width), else
    # the window that gives the guide's width (the kit's gutter is 32 px a side from 600 px, 16 under it)
    pages, groups, measured = {}, {}, {}
    for sid in specs:
        mw = {}
        for w in (DESK, PHONE):
            p = shots.get(f'm-{sid}-{w}')
            mw[w] = json.loads(p.read_text()).get('svg_w') if p and p.exists() else None
        measured[sid] = mw
        dp = DESK if not mw[DESK] or int(mw[DESK]) <= 720 else int(mw[DESK]) + 64
        pw = int(mw[PHONE]) + 32 if mw[PHONE] else PHONE
        pages[sid] = (dp, pw)
        groups.setdefault((dp, pw), []).append(sid)
    FIG['guide_widths'] = measured
    kit_out = kit_build(groups, a.reuse)
    for sid in specs:
        chk = kit_out / sid.lower() / f'{sid.lower()}-check.json'
        if chk.exists() and measured[sid][DESK]:
            dw = {(x['ground'], x['page']): x['width'] for x in json.loads(chk.read_text()).get('drawings', [])}
            for w, pw in ((DESK, pages[sid][0]), (PHONE, pages[sid][1])):
                if measured[sid][w] and dw.get(('newsprint', pw)) and int(dw[('newsprint', pw)]) != int(measured[sid][w]):
                    warn(f'{sid}: the guide draws {measured[sid][w]} px at a {w} px window and the kit {dw[("newsprint", pw)]} px at {pw}')
    b1cmp = board1_compare([s for s in specs if s in C['board1_ids']], kit_out, pages)
    # 3. the panels
    parts = [decide_panel(shots, fshots, kit_out, pages), forms_panel(G, P, rn, held, kit_out, pages, b1cmp, shots),
             rules_panel(G, ch, held, shots), count_panel(), spend_panel(G, rn, kit_out), scores_panel(), tested_panel(G, kit_out, specs), next_panel()]
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
        warn(f'the folder holds {len(files)} files, past the brief’s about 300')
    if total >= BYTES_AIM:
        warn(f'the folder comes to {total / 1e6:.2f} MB, at or over 120 MB')
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
    if a.check:
        ok = run_checks(a.out, page)
        files = [p for p in BOARD_DIR.rglob('*') if p.is_file()]
        FIG.update({'folder_files': len(files), 'folder_bytes': sum(p.stat().st_size for p in files), 'warnings': WARN})
        FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
        if not ok:
            sys.exit(1)
    if WARN and a.strict:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
