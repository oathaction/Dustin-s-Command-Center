"""Build the Gate 2 evidence board (November 11, 2026, D2-1699; task 6 of work/handoffs/phase-2/20261111_Gate-2-Brief.md).

Usage:
    python3 -I work/build/scripts/phase-2/gate_2_board_build.py [--strict] [--check] [--no-render] [--out PATH]

Reads, on every run:
    work/boards/phase-2/gate-2/board/20261111_Gate-2-Board-Content.json   the board's own words and the drawings it shows
    the image files the content names (earlier boards' proofs, work/build/assets/), copied or drawn into img/ beside
    the board; work/boards/sprite-sheet.html for the fifth edition's symbols
    work/build/tokens/tokens.css and tokens.json                         the board's styles and its contrast figures
    work/boards/board-base.css                                           the studio's board base, under the tokens
    the QA files under work/build/assets/ and the checks this script runs (sprite_check.js, icon_pixel_fit_check.js)
    the slot files the content names: the accessibility evidence, the engineer's notes, the creative director's scores,
    the drift report, each teammate's Tested and Not tested lists. A slot whose file is missing prints "Waiting for".
    work/ledger/*_Decision-Log.md and *_Open-Questions.md                every code in a reference line must exist
Writes:
    work/boards/phase-2/gate-2/board/20261111_Gate-2-Board.html          the board (images by relative path)
    work/boards/phase-2/gate-2/board/img/                                every image the board shows
    work/boards/phase-2/gate-2/board/20261111_Gate-2-Board-Figures.json  every figure the board prints, with its source
    <scratch>/checks/ the raw outputs of the checks it runs

--check runs dataviz_check.js on the board with --board --no-captures and fails the build if it fails.
--no-render reuses the images already in img/ (the first run must render).
--strict exits 1 on any warning (a missing code, a studio code on the board's face, a flagged word, an en dash). An em
dash stops the build.
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
import struct
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261111'
BOARD_DIR = ROOT / 'work/boards/phase-2/gate-2/board'
IMG = BOARD_DIR / 'img'
CONTENT = BOARD_DIR / f'{DATE}_Gate-2-Board-Content.json'
FIGURES = BOARD_DIR / f'{DATE}_Gate-2-Board-Figures.json'
OUT = BOARD_DIR / f'{DATE}_Gate-2-Board.html'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/board')
SCRIPTS = ROOT / 'work/build/scripts/phase-2'
ASSETS = ROOT / 'work/build/assets'
TOKENS_CSS = ROOT / 'work/build/tokens/tokens.css'
TOKENS_JSON = ROOT / 'work/build/tokens/tokens.json'
BOARD_BASE = ROOT / 'work/boards/board-base.css'
SPRITE_SHEET = ROOT / 'work/boards/sprite-sheet.html'
GROUND = {'newsprint': '#DCD9D2', 'charcoal': '#121212', 'prussian': '#1F2D5A', 'white': '#FFFFFF'}
INK = {'charcoal': '#121212', 'newsprint': '#DCD9D2', 'white': '#FFFFFF'}
INK_FOR = {'newsprint': 'charcoal', 'white': 'charcoal', 'charcoal': 'newsprint', 'prussian': 'white'}
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat',
           'basically', 'very', 'incredibly', 'utilize', 'utilizes']
TAGLINE = 'A country that answers to its people.'
LIMIT = 16_000_000
ZOOM_MAX = 96            # a row's drawings get the twice-size view when the row asks and the drawing is this tall or less
REGION_W = 248           # a frame wider than this scrolls sideways inside a named region at phone widths
WARN, NOTES, FIG, LINKED_CODES = [], [], {}, set()
JOBS, COPIES, CROPS = [], [], []
SEEN_OUT = {}


class BoardError(Exception):
    pass


def warn(msg):
    WARN.append(msg)
    print('warning', msg)


def note(msg):
    NOTES.append(msg)


def need(cond, msg):
    if not cond:
        raise BoardError(msg)


def rel(p):
    p = pathlib.Path(p)
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def esc(s):
    return html.escape(str(s), quote=True)


def png_size(p):
    with open(p, 'rb') as f:
        head = f.read(24)
    need(head[:8] == b'\x89PNG\r\n\x1a\n', f'{rel(p)} is not a PNG')
    return struct.unpack('>II', head[16:24])


def slug(*parts):
    words = []
    for p in parts:
        for w in re.findall(r'[A-Za-z0-9]+', str(p).replace('’', '').replace("'", '')):
            words.append(w[:1].upper() + w[1:])
    return '-'.join(words)


def fill(s, extra=None):
    d = dict(FILL)
    if extra:
        d.update(extra)
    return re.sub(r'\{([a-z0-9_]+)\}', lambda m: str(d[m.group(1)]) if m.group(1) in d else m.group(0), s)


FILL = {}
WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def nw(n, zero='no'):
    """A count in running prose: words under ten (H06), figures from ten."""
    n = int(n)
    return (zero if n == 0 else WORDS[n]) if 0 <= n < 10 else f'{n:,}'


# ------------------------------------------------------------------------------------------------------- sources
def read_log():
    """Every code the decision log and the open questions define, so a reference line prints none that is missing."""
    codes = set()
    for p in glob.glob(str(ROOT / 'work/ledger/*_Decision-Log.md')) + glob.glob(str(ROOT / 'work/ledger/*_Open-Questions.md')):
        t = pathlib.Path(p).read_text()
        codes |= set(re.findall(r'^\|\s*((?:DR|D2|D1|G1|DC|Q)-\d+)\s*\|', t, flags=re.M))
        codes |= set(re.findall(r'^#+\s*((?:Q)-\d+)\b', t, flags=re.M))
    # Gate 1 IDs (I1 to I10, S1 to S10, Y1 to Y6, M1 to M6, T1 to T5) are the Gate 1 report's
    g1 = (ROOT / 'work/ledger/20261021_Gate-1-Report.md').read_text()
    codes |= set(re.findall(r'\b([ISYMT]\d{1,2})\b', g1))
    return codes


def check_refs(refs, where):
    for c in re.findall(r'\b(?:DR|D2|D1|G1|DC|Q)-\d+\b|\b[ISYMT]\d{1,2}\b', refs):
        LINKED_CODES.add(c)
        if c not in LOG:
            warn(f'{c} in the reference line of {where} is not in the decision log, the open questions or the Gate 1 report')
    for a, b in re.findall(r'\b(D2-\d+) to (D2-\d+)\b', refs):
        for c in (a, b):
            if c not in LOG:
                warn(f'{c} in {where} is missing from the log')


def tokens():
    t = TOKENS_CSS.read_text()
    pal = dict(re.findall(r'--oa-color-palette-([a-z-]+):\s*(#[0-9A-Fa-f]{6})', t))
    j = json.loads(TOKENS_JSON.read_text())
    ver = None
    for k in ('version', '$version'):
        if isinstance(j, dict) and k in j:
            ver = j[k]
    if ver is None:
        m = re.search(r'Version (\S+)', t)
        ver = m.group(1) if m else None
    return pal, ver


def contrast(a, b):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


SPRITE = None


def sprite_symbol(sid):
    global SPRITE
    if SPRITE is None:
        SPRITE = SPRITE_SHEET.read_text()
    m = re.search(r'<symbol id="%s" viewBox="([^"]+)">(.*?)</symbol>' % re.escape(sid), SPRITE, re.S)
    need(m, f'the fifth edition sprite has no symbol {sid}')
    return m.group(1), m.group(2)


# ------------------------------------------------------------------------------------------------------- images
def svg_markup(path, h):
    t = pathlib.Path(path).read_text()
    t = re.sub(r'<\?xml[^>]*\?>', '', t).strip()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', t).group(1).replace(',', ' ').split()]
    w = vb[2] * h / vb[3]
    t = re.sub(r'<svg\b', f'<svg width="{w:.3f}" height="{h}"', t, count=1)
    return t, w


def sprite_markup(sid, h):
    vb, inner = sprite_symbol(sid)
    v = [float(x) for x in vb.split()]
    w = v[2] * h / v[3]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}" height="{h}" viewBox="{vb}">{inner}</svg>', w


def image(spec, name):
    """Plan one image: returns its record {src, w, h, kind, source}. The file lands in img/ under name."""
    out = IMG / f'{DATE}_{name}.png'
    if out.name in SEEN_OUT:
        if SEEN_OUT[out.name] != json.dumps(spec, sort_keys=True):
            raise BoardError(f'two different images want the name {out.name}')
        return dict(SEEN_OUT_REC[out.name])
    SEEN_OUT[out.name] = json.dumps(spec, sort_keys=True)
    bg = spec.get('bg', 'newsprint')
    ink = spec.get('ink', INK_FOR[bg])
    rec = {'src': f'img/{out.name}', 'file': out, 'spec': spec}
    if 'copy' in spec:
        src = ROOT / spec['copy']
        need(src.exists(), f'missing image {spec["copy"]}')
        COPIES.append((src, out))
        rec['w'], rec['h'] = png_size(src)
        rec['source'] = spec['copy']
    elif 'svg' in spec or 'sprite' in spec:
        h = spec['h']
        if 'svg' in spec:
            src = ROOT / spec['svg']
            need(src.exists(), f'missing drawing {spec["svg"]}')
            mk, w = svg_markup(src, h)
            rec['source'] = spec['svg']
        else:
            mk, w = sprite_markup(spec['sprite'], h)
            rec['source'] = f'work/boards/sprite-sheet.html#{spec["sprite"]}'
        W, H = max(1, round(w + 0.499)), max(1, round(h + 0.499))
        JOBS.append({'out': str(out), 'markup': mk, 'w': W, 'h': H, 'dsf': 1, 'bg': GROUND[bg], 'ink': INK[ink]})
        rec['w'], rec['h'] = W, H
    elif 'element' in spec:
        e = spec['element']
        src = ROOT / e['file']
        need(src.exists(), f'missing page {e["file"]}')
        job = {'out': str(out), 'file': str(src), 'selector': e['selector'], 'index': e.get('index', 0), 'dsf': 1, 'w': 0, 'h': 0}
        if RENDER or not out.exists():
            run_jobs([job])
        need(out.exists(), f'the photograph of {e["file"]} was not made')
        rec['w'], rec['h'] = png_size(out)
        rec['source'] = f'{e["file"]} ({e["selector"]} {e.get("index", 0)})'
    elif 'crop' in spec:
        c = spec['crop']
        CROPS.append((ROOT / c['src'], c['box'], out))
        rec['w'], rec['h'] = c['box'][2] - c['box'][0], c['box'][3] - c['box'][1]
        rec['source'] = f'{c["src"]} (crop {c["box"]})'
    else:
        raise BoardError(f'unknown image spec {spec}')
    SEEN_OUT_REC[out.name] = rec
    ALL_IMAGES.append(rec)
    return dict(rec)


SEEN_OUT_REC = {}
ALL_IMAGES = []


RENDER = True
REUSE = False


def run_jobs(jobs):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jp = SCRATCH / 'render-jobs.json'
    jp.write_text(json.dumps(jobs))
    r = subprocess.run(['node', str(SCRIPTS / 'gate_2_board_render.js'), str(jp)], cwd=ROOT / 'work/build',
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    bad = [l for l in r.stdout.splitlines() if l.startswith('failed')]
    need(r.returncode == 0 and not bad, 'renders failed: ' + '; '.join(bad[:5]) + r.stderr[-400:])


def produce(render=True):
    IMG.mkdir(parents=True, exist_ok=True)
    for src, out in COPIES:
        if not out.exists() or out.read_bytes() != src.read_bytes():
            shutil.copyfile(src, out)
    if CROPS:
        from PIL import Image
        for src, box, out in CROPS:
            Image.open(src).crop(tuple(box)).save(out)
    if JOBS and render:
        run_jobs(JOBS)
    for rec in ALL_IMAGES:
        need(rec['file'].exists(), f'{rel(rec["file"])} was not made; run once without --no-render')
        rec['w'], rec['h'] = png_size(rec['file'])
    # images in img/ that no part of the board names any more go
    keep = {r['file'].name for r in ALL_IMAGES}
    for p in IMG.glob('*.png'):
        if p.name not in keep:
            p.unlink()
            note(f'removed {p.name}, which the board no longer shows')


# ------------------------------------------------------------------------------------------------------- figures
def frame(rec, alt, zoom=False, cls=''):
    """One drawing at its true size; zoom adds the same pixels at twice the size. Wide frames scroll in a region."""
    w, h = rec['w'], rec['h']
    out = []
    region = w > REGION_W
    attrs = f' role="region" tabindex="0" aria-label="{esc(alt)}, {w} by {h} px; scrolls sideways"' if region else ''
    out.append(f'<div class="frame{" wide" if region else ""} {cls}"{attrs}><img src="{rec["src"]}" width="{w}" height="{h}" alt="{esc(alt)}" class="px" loading="lazy" decoding="async"></div>')
    if zoom and h <= ZOOM_MAX:
        zw, zh = 2 * w, 2 * h
        zregion = zw > REGION_W
        za = f' role="region" tabindex="0" aria-label="{esc(alt)} at twice the size; scrolls sideways"' if zregion else ''
        out.append(f'<div class="frame zoom{" wide" if zregion else ""}"{za}><img src="{rec["src"]}" width="{zw}" height="{zh}" alt="" class="px" loading="lazy" decoding="async"></div>')
    return f'<div class="frames">{"".join(out)}</div>' if len(out) > 1 else out[0]


def cell_html(cell, col, item, row, zoom, k):
    label = cell.get('label') or col
    base = slug(item['id'], row['label'], label)
    if 'empty' in cell:
        return f'<figure class="shot empty"><div class="none"><p>{esc(cell["empty"])}</p></div><figcaption><b>{esc(label)}</b></figcaption></figure>'
    if 'imgs' in cell:
        names = item.get('names') or [str(i + 1) for i in range(len(cell['imgs']))]
        recs = [image(s, slug(item['id'], row['label'], label, names[i])) for i, s in enumerate(cell['imgs'])]
        strip = ''.join(f'<div class="strip-i">{frame(r, f"{names[i]}, {label}, {row["label"]}")}<span class="nm">{esc(names[i])}</span></div>' for i, r in enumerate(recs))
        zs = ''
        if zoom and all(r['h'] <= ZOOM_MAX for r in recs):
            zs = '<div class="strip zoomstrip" aria-hidden="true">' + ''.join(
                f'<div class="strip-i"><div class="frame zoom"><img src="{r["src"]}" width="{2 * r["w"]}" height="{2 * r["h"]}" alt="" class="px" loading="lazy" decoding="async"></div></div>' for r in recs) + '</div>'
        dims = f'{recs[0]["w"]} by {recs[0]["h"]} px each' if len({(r["w"], r["h"]) for r in recs}) == 1 else 'each at its own size'
        return f'<figure class="shot {"after" if k == len(item["cols"]) - 1 else "before"}"><div class="strip">{strip}</div>{zs}<figcaption><b>{esc(label)}</b> <span>{dims}</span></figcaption></figure>'
    rec = image(cell['img'], base)
    side = 'after' if (k == len(item['cols']) - 1 and not cell.get('label')) else ('overlay' if cell.get('label') else 'before')
    alt = cell['img'].get('alt') or f'{item["title"]}: {label}, {row["label"]}'
    return (f'<figure class="shot {side}">{frame(rec, alt, zoom)}'
            f'<figcaption><b>{esc(label)}</b> <span>{rec["w"]} by {rec["h"]} px</span></figcaption></figure>')


def refline(refs, where):
    check_refs(refs, where)
    return f'<p class="codes">Reference: {esc(refs)}</p>'


def rows_html(item):
    out, more = [], []
    for row in item['rows']:
        zoom = bool(row.get('zoom'))
        cells = ''.join(cell_html(c, (item['cols'][k] if k < len(item['cols']) else ''), item, row, zoom, k) for k, c in enumerate(row['cells']))
        nt = f'<p class="row-note">{esc(row["note"])}</p>' if row.get('note') else ''
        h = (f'<div class="row{" stack" if item.get("stack") else ""}"><p class="row-label">{esc(row["label"])}'
             f'</p>{nt}<div class="cells">{cells}</div></div>')
        (more if row.get('more') else out).append(h)
    if item.get('grid'):
        out = [f'<div class="rowgrid">{"".join(out)}</div>']
    if more:
        out.append(f'<details class="more"><summary>{esc(item.get("more_label", "More"))}</summary>{"".join(more)}</details>')
    return ''.join(out)


def card(item, body):
    tag = item.get('tag', '')
    tcls = ' defect' if tag == 'Defect fix' else ''
    zl = '<p class="zl">Where a drawing appears twice, the second view doubles every pixel.</p>' if 'class="frame zoom' in body else ''
    return (f'<article class="card" id="{esc(item["id"])}"><header class="card-h"><h4>{esc(item["title"])}</h4>'
            f'<span class="tag{tcls}">{esc(tag)}</span></header><p class="what">{esc(fill(item["what"]))}</p>{zl}'
            f'{body}{refline(item["refs"], item["id"])}</article>')


# ------------------------------------------------------------------------------------------------------- panel 2 specials
def fits_manifest():
    m = json.loads((ASSETS / 'civic-line-v6/fit-24/20261111_Civic-Line-24px-Fits-In-Use-Manifest.json').read_text())
    return m['fits']


def pillar_fits():
    m = json.loads((ASSETS / 'pillar-icons/20261110_Pillar-Icons-Manifest.json').read_text())
    return [i for i in m['icons'] if i.get('edition') == 'black' and i.get('in_use')]


def fits_item(item):
    fits = {f['id']: f for f in fits_manifest()}
    rows = []
    for fid in item['examples']:
        f = fits[fid]
        master = (ASSETS / 'civic-line-v6/fit-24' / f['master_from_2x']['svg']).resolve()
        rows.append({'label': id_label(fid, f['word']), 'zoom': True, 'cells': [
            {'img': {'svg': rel(master), 'h': 24}},
            {'img': {'svg': rel(ASSETS / 'civic-line-v6/fit-24' / f['svg']), 'h': 24}}]})
    it = dict(item, rows=rows, grid=True)
    return card(item, rows_html(it))


def id_label(fid, word):
    """A drawing's name first, then what its ID is (H11): a reform takes its type word."""
    return f'{word}, Reform {fid}' if fid.startswith('R-') else f'{word}, {fid}'


def civic_item(item):
    inv = {i['id']: i for i in json.loads((ASSETS / 'civic-line-v6/20261110_Civic-Line-V6-Inventory.json').read_text())['icons']}
    rows = []
    for p in item['pairs']:
        cl = inv[p['cl']]
        rows.append({'label': p['name'], 'zoom': True, 'cells': [
            {'img': {'sprite': p['v5'], 'h': 48}},
            {'img': {'svg': rel(civic_black(cl)), 'h': 48}}]})
    body = rows_html(dict(item, rows=rows, grid=True))
    tiles = []
    for sid, name in item['v5_set']:
        r = image({'sprite': sid, 'h': 48}, slug('V5-Topic', name, '48'))
        tiles.append(f'<li>{frame(r, f"{name}, fifth edition, 48 px")}<span class="nm">{esc(name)}</span></li>')
    body += (f'<div class="row"><p class="row-label">{esc(item["v5_set_h"])}</p><ul class="tiles">{"".join(tiles)}</ul></div>'
             f'<p class="row-note"><a href="#sheet-48">{esc(item["set_link"])}</a></p>')
    return card(item, body)


def civic_black(entry):
    fid = entry['id']
    hits = sorted((ASSETS / 'civic-line-v6/black').glob(f'*-{fid}-*-Black.svg'))
    need(hits, f'no black edition file for {fid}')
    return hits[-1]


def refinements_panel(C):
    P = C['panels']['refinements']
    groups = []
    for g in C['groups']:
        cards = []
        for item in [i for i in C['items'] if i['group'] == g['id']]:
            if item['id'] == 'fits':
                cards.append(fits_item(item))
            elif item['id'] == 'civic-line':
                cards.append(civic_item(item))
            else:
                cards.append(card(item, rows_html(item)))
        groups.append(f'<section class="grp" aria-labelledby="g-{g["id"]}"><h3 class="grp-h" id="g-{g["id"]}">{esc(g["h"])}</h3>{"".join(cards)}</section>')
    key = (f'<div class="key"><span class="k-a"><i aria-hidden="true"></i>{esc(P["key_actual"])}</span>'
           f'<span class="k-z"><i aria-hidden="true"></i>{esc(P["key_zoom"])}</span></div>')
    return panel('refinements', P, f'<p class="intro">{esc(P["lede"])}</p><p class="caption src-note">{esc(P["source_note"])}</p>{key}' + ''.join(groups), 'ready')


# ------------------------------------------------------------------------------------------------------- panel 3, craft
def run_pixel_fit(C):
    """Run the pixel-fit check on today's files for each family; results land in the scratchpad and the figures file."""
    out = {}
    d = SCRATCH / 'checks'
    d.mkdir(parents=True, exist_ok=True)
    for fam in C['craft']['families']:
        files = sorted(glob.glob(str(ASSETS / fam['files'])))
        need(files, f'no files for {fam["key"]}')
        jp = d / f'pixel-fit-{fam["key"]}.json'
        if REUSE and jp.exists():
            cmd = None
        else:
            cmd = ['node', str(SCRIPTS / 'icon_pixel_fit_check.js'), '--size', str(fam['size'])]
        if cmd and fam.get('weight'):
            cmd += ['--weight', str(fam['weight'])]
        if cmd:
            cmd += ['--json', str(jp)] + files
            subprocess.run(cmd, cwd=ROOT / 'work/build', capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        need(jp.exists(), f'the pixel-fit check wrote nothing for {fam["key"]}')
        res = json.loads(jp.read_text())['results']
        thin = [r['scales']['1x']['stroke_px']['thinnest'] for r in res if r['scales']['1x']['stroke_px'].get('thinnest') is not None]
        fails = sorted({f for r in res for s in r['scales'].values() for f in s['fails']})
        out[fam['key']] = {'label': fam['label'], 'size': fam['size'], 'files': len(res), 'pass': sum(1 for r in res if r['pass']),
                           'thinnest_min': min(thin) if thin else None, 'fails': fails, 'run': json.loads(jp.read_text())['run'],
                           'weight': fam.get('weight')}
    return out


def run_sprite():
    d = SCRATCH / 'checks'
    d.mkdir(parents=True, exist_ok=True)
    jp = d / 'sprite-check.json'
    if REUSE and jp.exists():
        return json.loads(jp.read_text())
    r = subprocess.run(['node', str(SCRIPTS / 'sprite_check.js'), '--json', str(jp)], cwd=ROOT / 'work/build',
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    need(jp.exists(), 'sprite_check.js wrote nothing: ' + r.stdout[-300:] + r.stderr[-300:])
    return json.loads(jp.read_text())


def craft_panel(C, pf, sp):
    P = C['panels']['craft']
    K = C['craft']
    # pixel-fit table
    rows = []
    for fam in K['families']:
        f = pf[fam['key']]
        ok = f['pass'] == f['files']
        rows.append(f'<tr><th scope="row">{esc(f["label"])}</th><td class="num">{f["size"]} px</td><td class="num">{f["files"]}</td>'
                    f'<td class="num{" miss" if not ok else ""}">{f["pass"]} of {f["files"]}{"" if ok else " <span class=fl>Straight strokes</span>" if f["fails"] == ["straight"] else ""}</td>'
                    f'<td class="num">{f["thinnest_min"]:.2f} px</td></tr>')
    head = ''.join(f'<th scope="col">{esc(c)}</th>' for c in K['pixel_cols'])
    pixel = (f'<h3 class="sub">{esc(K["pixel_h"])}</h3><p>{esc(K["pixel_lede"])}</p>'
             f'<div class="tw" role="region" tabindex="0" aria-label="{esc(K["pixel_h"])}; scrolls sideways"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
             f'<p class="caption">{esc(K["housing_note"])}</p>')
    # sprite table
    srows = []
    fams = sp['scales']['1x']['families']
    for name, v in fams.items():
        v2 = sp['scales']['2x']['families'].get(name, {})
        largest = max(v['largest'], v2.get('largest', 0))
        srows.append(f'<tr><th scope="row">{esc(sprite_family_name(name))}</th><td class="num">{v["pairs"]}</td><td class="num">{v2.get("pairs", "")}</td><td class="num">{largest} of 255</td></tr>')
    pat = sp['scales']['1x'].get('pattern', [])
    ok1 = sum(1 for p in pat if p['ok'])
    ok15 = sum(1 for p in sp['scales'].get('1.5x', {}).get('pattern', []) if p['ok'])
    ok2 = sum(1 for p in sp['scales']['2x'].get('pattern', []) if p['ok'])
    sw_ok = min(ok1, ok15 or ok1, ok2)
    FIG['sprite'] = {'checked': sp['checked'], 'pass': sp['pass'], 'pattern_ok': [ok1, ok15, ok2], 'pattern_n': len(pat)}
    shead = ''.join(f'<th scope="col">{esc(c)}</th>' for c in K['sprite_cols'])
    sprite = (f'<h3 class="sub">{esc(K["sprite_h"])}</h3><p>{esc(K["sprite_lede"])} <b>{"It passes." if sp["pass"] else "It fails."}</b></p>'
              f'<div class="tw" role="region" tabindex="0" aria-label="{esc(K["sprite_h"])}; scrolls sideways"><table><thead><tr>{shead}</tr></thead><tbody>{"".join(srows)}</tbody></table></div>'
              f'<p class="caption">{esc(fill(K["sprite_switch"], {"ok": sw_ok, "n": len(pat)}))} Run {esc(words_when(sp["checked"]))}.</p>')
    # Civic Line QA
    v = json.loads((ASSETS / 'civic-line/qa/20261029_Civic-Line-Verify-Report.json').read_text())
    inv = json.loads((ASSETS / 'civic-line-v6/20261110_Civic-Line-V6-Inventory.json').read_text())
    unchanged = inv['counts_by_source'].get('October master, unchanged', 0)
    tm = v['tile_margins']
    qa_items = [
        ('The October trace', f'All {v["ids"]} drawings traced and reviewed, with {nw(v["states"]["todo"], "none")} left to do and {nw(len(v["errors"]))} errors. The four color editions of each drawing share one set of shapes, checked element by element in {v["edition_tree_elements_compared"]:,} places.'),
        ('Files', f'{v["svgs"]} SVG files and {v["tile_svgs"]:,} tile files, with {nw(v["id_audit"]["repeated_ids"])} repeated and {nw(v["id_audit"]["unresolved_references"])} broken internal IDs across {v["id_audit"]["files"]:,} files.'),
        ('Tiles', f'Every drawing clears the edge of its square, rounded and circle tile; the tightest margins are {tm["square"]["min_margin"]:.1f}, {tm["rounded"]["min_margin"]:.1f} and {tm["circle"]["min_margin"]:.1f} units of 128.'),
        ('The set in use', f'{inv["count"]} drawings: {unchanged} October masters unchanged and {inv["count"] - unchanged} redrawn or new drawings you approved by name, in the October order.'),
    ]
    contrast_rows = [c for c in v['contrast']]
    qa = (f'<h3 class="sub">{esc(K["qa_h"])}</h3><p>{esc(K["qa_lede"])}</p><dl class="facts">'
          + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in qa_items) + '</dl>'
          + '<div class="tw" role="region" tabindex="0" aria-label="Civic Line contrast; scrolls sideways"><table><caption>Civic Line inks on their grounds, with 3 to 1 the guideline for graphics</caption><thead><tr><th scope="col">Ink</th><th scope="col">Ground</th><th scope="col">Ratio</th><th scope="col">3 to 1</th></tr></thead><tbody>'
          + ''.join(f'<tr><th scope="row">{esc(c["ink"])}</th><td>{esc(c["ground"])}</td><td class="num">{c["ratio"]:.2f} to 1</td><td>{"Meets" if c["meets_3_to_1"] else "<b>Falls short</b>"}</td></tr>' for c in contrast_rows)
          + '</tbody></table></div><p class="caption">Pillar Red on Newsprint falls short of 3 to 1. Every red part is a drawn shape that the one-color editions carry in Charcoal or Newsprint, so red never carries a meaning alone.</p>')
    FIG['civic_line_qa'] = {'verify': rel(ASSETS / 'civic-line/qa/20261029_Civic-Line-Verify-Report.json'), 'ids': v['ids'], 'in_use': inv['count'], 'unchanged': unchanged}
    sheets = craft_sheets(C)
    small_ok = all(pf[f['key']]['pass'] == pf[f['key']]['files'] for f in K['families'] if f['size'] in (16, 24))
    if not small_ok or not sp['pass']:
        warn('the craft panel’s opening sentence says every small icon and the sprite pass, and a check now fails')
    body = f'<p class="intro">{esc(P["lede"])}</p>{sheets}{pixel}{sprite}{qa}'
    return panel('craft', P, body, 'ready')


def sprite_family_name(n):
    return {'civic-line black': 'Civic Line, black', 'civic-line red-black': 'Civic Line, red and black', 'pillar black': 'Pillar fits, black',
            'pillar red-black': 'Pillar fits, red and black', 'fit-24 black': 'The 37 pixel fits', 'utility black': 'Utility icons'}.get(n, n)


def words_when(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return d.strftime('%B ') + str(d.day) + d.strftime(', %Y')
    except Exception:
        return iso


def craft_sheets(C):
    K = C['craft']
    # 16 px: the utility icons in use and the pillar fits
    um = json.loads((ASSETS / 'utility/20261110_Utility-Icons-Manifest.json').read_text())
    t16 = []
    for u in um['icons']:
        name = u['name'].replace('-', ' ')
        f = sorted((ASSETS / 'utility/svg-16').glob(f'*_Utility-{u["name"]}-16px.svg'))
        need(f, f'no 16 px file for {u["name"]}')
        r = image({'svg': rel(f[-1]), 'h': 16}, slug('Sheet-16', name))
        t16.append((name, r))
    for p in [i for i in pillar_fits() if i['size_px'] == 16]:
        r = image({'svg': rel(ASSETS / 'pillar-icons' / p['svg']), 'h': 16}, slug('Sheet-16-Pillar', p['word']))
        t16.append((p['word'], r))
    s16 = sheet('sheet-16', K['sheet_16_h'], K['sheet_16_cap'], t16, zoom=True)
    # 24 px: the 37 fits and the four pillar fits, as 1x screens draw them
    t24 = [(p['word'], image({'svg': rel(ASSETS / 'pillar-icons' / p['svg']), 'h': 24}, slug('Sheet-24-Pillar', p['word'])))
           for p in pillar_fits() if p['size_px'] == 24]
    for f in fits_manifest():
        t24.append((id_label(f['id'], f['word']), image({'svg': rel(ASSETS / 'civic-line-v6/fit-24' / f['svg']), 'h': 24}, slug('Sheet-24', f['id']))))
    FILL['n_24'] = len(t24)
    FILL['n_fits'] = len(fits_manifest())
    s24 = sheet('sheet-24', fill(K['sheet_24_h']), K['sheet_24_cap'], t24, zoom=True)
    # 48 px: every Civic Line drawing in use
    inv = json.loads((ASSETS / 'civic-line-v6/20261110_Civic-Line-V6-Inventory.json').read_text())
    t48 = [(id_label(i['id'], i['label']), image({'svg': rel(civic_black(i)), 'h': 48}, slug('Sheet-48', i['id']))) for i in inv['icons']]
    FILL['n_civic'] = len(t48)
    s48 = sheet('sheet-48', fill(K['sheet_48_h']), K['sheet_48_cap'], t48, zoom=False, folded=True)
    return f'<h3 class="sub">{esc(K["sheets_h"])}</h3>{s16}{s24}{s48}'


def sheet(sid, h, cap, tiles, zoom, folded=False):
    lis = ''.join(f'<li>{frame(r, f"{n}, actual size", zoom=zoom)}<span class="nm">{esc(n)}</span></li>' for n, r in tiles)
    inner = f'<ul class="tiles{" zoomed" if zoom else ""}">{lis}</ul>'
    if folded:
        inner = f'<details class="more"><summary>Open the sheet of {len(tiles)}</summary>{inner}</details>'
    return f'<div class="sheet" id="{sid}"><h4 class="sheet-h">{esc(h)}</h4><p class="caption">{esc(cap)}</p>{inner}</div>'


# ------------------------------------------------------------------------------------------------------- panel 4, similarity
def similarity_panel(C):
    P = C['panels']['similarity']
    K = C['similarity']
    sim = json.loads((ROOT / 'work/handoffs/phase-2/20261028_Ampersand-B-Similarity.json').read_text())
    verdict = sim['verdict_B_refined']
    res = sim['results']['B refined (Phase 2)']
    # the sheet images and their faces, as the identity board names them
    ib = (ROOT / 'work/boards/20261028_Identity-Masters-Board.html').read_text()
    faces = {}
    for m in re.finditer(r'<img[^>]*src="phase-2/identity/04-amp-b/similarity/(sheet_g\d+\.png)"[^>]*alt="([^"]+?) ampersand, 96 px tall"', ib):
        faces[html.unescape(m.group(2))] = m.group(1)
    for m in re.finditer(r'<img[^>]*alt="([^"]+?) ampersand, 96 px tall"[^>]*src="phase-2/identity/04-amp-b/similarity/(sheet_g\d+\.png)"', ib):
        faces[html.unescape(m.group(1))] = m.group(2)
    need(faces, 'no similarity sheet names found on the identity board')
    order = sorted(res.items(), key=lambda kv: -kv[1]['silhouette_overlap_200px'])
    pick = []
    b_name = next((k for k in faces if k.startswith('B refined')), None)
    lora = 'Lora Bold (V5 master source)'
    if b_name:
        pick.append(('Ampersand B', faces[b_name], None))
    lora_key = next((k for k in faces if k.startswith('Lora Bold')), None)
    if lora_key:
        pick.append(('Lora Bold, the fifth edition’s source', faces[lora_key], verdict['recognition']['value']))
    n = 0
    for face, v in order:
        if face.startswith('Lora'):
            continue
        if face in faces:
            pick.append((face, faces[face], v['silhouette_overlap_200px']))
            n += 1
        if n >= 6:
            break
    tiles = []
    for name, fn, ov in pick:
        r = image({'copy': f'work/boards/phase-2/identity/04-amp-b/similarity/{fn}'}, slug('Amp-Similarity', name))
        val = f'<span class="ov">{ov:.3f}</span>' if ov is not None else '<span class="ov">The drawing</span>'
        tiles.append(f'<li>{frame(r, f"{name} ampersand")}<span class="nm">{esc(name)}</span>{val}</li>')
    rec, dis = verdict['recognition'], verdict['distinctness']
    FILL['calib'] = f'{sim["calibration_median"]:.3f}'
    amp = (f'<h3 class="sub">{esc(K["amp_h"])}</h3><p>{esc(fill(K["amp_lede"]))}</p>'
           f'<dl class="facts two"><div><dt>Still reads as an ampersand</dt><dd>Overlap with Lora Bold <b>{rec["value"]:.3f}</b>, over 0.70. {"Passes" if rec["pass"] else "Fails"}.</dd></div>'
           f'<div><dt>Passes for no installed font</dt><dd>Nearest other face, {esc(dis["nearest_face"])}, at <b>{dis["value"]:.3f}</b>, under {dis["threshold"]:.3f}. {"Passes" if dis["pass"] else "Fails"}. {verdict["faces_checked"]} faces in {len(verdict["families_checked"])} families checked.</dd></div></dl>'
           f'<ul class="tiles amp">{"".join(tiles)}</ul><p class="caption">{esc(K["amp_sheet_cap"])} {esc(K["amp_not"])}</p>')
    FIG['ampersand_similarity'] = {'source': 'work/handoffs/phase-2/20261028_Ampersand-B-Similarity.json', 'recognition': rec, 'distinctness': dis}
    # icons
    rows, flagged = [], []
    for run in K['runs']:
        d = json.loads((ROOT / run['file']).read_text())
        closest = max([c['likeness'] for c in d.get('closest', [])] + [0])
        rows.append(f'<tr><th scope="row">{esc(run["label"])}</th><td>{esc(against(d))}</td><td class="num">{len(d.get("flagged", []))}</td>'
                    f'<td class="num">{len(d.get("watch", []))}</td><td class="num">{closest:.3f}</td></tr>')
        for f in d.get('flagged', []):
            flagged.append((run, d, f))
        FIG.setdefault('likeness', []).append({'file': run['file'], 'flagged': d.get('flagged', []), 'watch_count': len(d.get('watch', [])), 'thresholds': d.get('thresholds')})
    d0 = json.loads((ROOT / K['runs'][0]['file']).read_text())
    head = ''.join(f'<th scope="col">{esc(c)}</th>' for c in K['icons_cols'])
    icons = (f'<h3 class="sub">{esc(K["icons_h"])}</h3><p>{esc(fill(K["icons_lede"], {"pairs": f"{d0["distribution"]["pairs"]:,}"}))} '
             f'Top 1 percent starts at {d0["thresholds"]["flag"]["likeness"]:.3f}, and top 5 percent at {d0["thresholds"]["watch"]["likeness"]:.3f}.</p>'
             f'<div class="tw" role="region" tabindex="0" aria-label="{esc(K["icons_h"])}; scrolls sideways"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    if flagged:
        fits = {f['id']: f for f in fits_manifest()}
        inv = {i['id']: i for i in json.loads((ASSETS / 'civic-line-v6/20261110_Civic-Line-V6-Inventory.json').read_text())['icons']}
        pr = []
        for run, d, f in flagged:
            a_id = re.search(r'Fit-((?:CL|R)-\d+)', f['a']).group(1)
            b_id = re.match(r'((?:CL|R)-\d+)', f['b']).group(1)
            ra = image({'svg': rel(ASSETS / 'civic-line-v6/fit-24' / fits[a_id]['svg']), 'h': 24}, slug('Sheet-24', a_id))
            rb = image({'svg': rel(civic_black(inv[b_id])), 'h': 24}, slug('Likeness', b_id, '24'))
            b_word = inv[b_id]['label']
            pr.append(f'<li class="pair"><figure class="shot">{frame(ra, f"{id_label(a_id, fits[a_id]["word"])}, the fit", zoom=True)}<figcaption><b>{esc(id_label(a_id, fits[a_id]["word"]))}</b> <span>the fit</span></figcaption></figure>'
                      f'<figure class="shot">{frame(rb, f"{id_label(b_id, b_word)}, the master at 24 px", zoom=True)}<figcaption><b>{esc(id_label(b_id, b_word))}</b> <span>the master</span></figcaption></figure>'
                      f'<p class="score">{f["likeness"]:.3f}<span>top {100 - f["percentile"]:.1f} percent</span></p></li>')
        icons += (f'<h4 class="sheet-h">{esc(K["flagged_h"])}</h4><p>{esc(K["flagged_lede"])}</p><ul class="pairs">{"".join(pr)}</ul>'
                  f'<p class="caption">Scores from the run of {esc(words_when(d0["run"]))}. Each fit stands as the guide draws it today.</p>')
    return panel('similarity', P, f'<p class="intro">{esc(P["lede"])}</p>{amp}{icons}', 'ready')


def against(d):
    m = d.get('masters') or ''
    n = d['distribution']['pairs']
    return f'The Civic Line masters, {n:,} pairs' if n else m


# ------------------------------------------------------------------------------------------------------- slots
def owner(C, key):
    return C['owners'].get(key, key)


def pending(C, who, filelabel):
    return f'<div class="pending" role="status"><p><b>{esc(C["status_words"]["waiting"].format(who=owner(C, who)))}.</b> {esc(C["pending_line"].format(who=owner(C, who), file=filelabel).split(". ", 1)[1])}</p></div>'


def md_section(text, names):
    """The lines under the first heading whose words match one of names, to the next heading of the same or higher level."""
    lines = text.splitlines()
    for i, l in enumerate(lines):
        m = re.match(r'^(#+)\s*(.+?)\s*$', l)
        if m and any(re.fullmatch(n, m.group(2).strip(), flags=re.I) for n in names):
            lvl = len(m.group(1))
            out = []
            for l2 in lines[i + 1:]:
                m2 = re.match(r'^(#+)\s', l2)
                if m2 and len(m2.group(1)) <= lvl:
                    break
                out.append(l2)
            return '\n'.join(out).strip()
    return None


def md_items(block):
    if block and not re.search(r'^\s*(?:[-*]|\d+\.)\s+', block, flags=re.M):
        return [p.strip() for p in re.split(r'\n\s*\n', block) if p.strip() and not p.strip().startswith('**')]
    items, cur = [], None
    for l in block.splitlines():
        m = re.match(r'^\s*(?:[-*]|\d+\.)\s+(.*)$', l)
        if m:
            if cur is not None:
                items.append(cur)
            cur = m.group(1).strip()
        elif cur is not None and l.strip() and l.startswith('  '):
            cur += ' ' + l.strip()
    if cur is not None:
        items.append(cur)
    return items


CODE = r'(?:DR|D2|D1|G1|DC|Q)-\d+'
MOVED = set()


def strip_codes(s):
    """Others' words keep their sentences; a parenthesis that holds only studio codes moves to the reference line."""
    def one(m):
        MOVED.update(re.findall(CODE, m.group(0)))
        return ''
    s = re.sub(r'\s*\((?:(?:' + CODE + r'|[A-Z]{1,2}\d{1,2}|[A-Z]{2}-[MS]\d+)(?:,\s*|\s+and\s+|;\s*)?)+\)', one, str(s))

    def bare(m):
        MOVED.add(m.group(2))
        return m.group(1) + ' a logged decision'
    s = re.sub(r'\b(by|in|under|per)\s+(' + CODE + r')\b', bare, s)

    def poss(m):
        MOVED.add(m.group(1))
        return 'the '
    return re.sub(r'\b(' + CODE + r')(?:’|\')s\s+', poss, s)


def md_inline(s):
    s = esc(strip_codes(s))
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


def approves_panel(C):
    P = C['panels']['approves']
    ans = ''.join(f'<li><h4>{esc(a["h"])}</h4><p>{esc(a["body"])}</p>{refline(a["refs"], "answered: " + a["h"])}</li>' for a in P['answered'])
    st = ''.join(f'<li><h4>{esc(a["h"])}</h4><p>{esc(a["body"])}</p>{refline(a["refs"], "settled: " + a["h"])}</li>' for a in P['settled'])
    p3 = C.get('phase3')
    if p3:
        paras = ''.join(f'<p>{md_inline(x)}</p>' for x in p3.get('paragraphs', []))
        dec = p3.get('decide') or []
        decide = (f'<h4 class="dec-h">{esc(p3.get("decide_h", "You decide"))}</h4><ol class="decide">' + ''.join(
            f'<li><b>{esc(d["q"])}</b> {md_inline(d.get("rec", ""))}</li>' for d in dec) + '</ol>') if dec else ''
        open_html = f'<div class="open">{paras}{decide}{refline(p3["refs"], "phase 3") if p3.get("refs") else ""}</div>'
        status = 'ready'
    else:
        open_html = f'<div class="open">{pending(C, P["phase3_pending_who"], P["phase3_pending_file"])}</div>'
        status = ('partial', P['phase3_pending_who'])
    body = (f'<p class="intro">{esc(P["lede"])}</p><div class="approve-grid">'
            f'<div class="col-open"><h3 class="sub">{esc(P["open_h"])}</h3><h4 class="open-h">{esc(P["phase3_h"])}</h4>{open_html}</div>'
            f'<div class="col-ans"><h3 class="sub">{esc(P["answered_h"])}</h3><ul class="ans">{ans}</ul></div></div>'
            f'<h3 class="sub">{esc(P["settled_h"])}</h3><p>{esc(P["settled_lede"])}</p><ul class="ans three">{st}</ul>')
    return panel('approves', P, body, status)


def a11y_status(C):
    """The accessibility lead's own checklist: {item text: done}. Their notes mark each check [x] when it is finished."""
    p = ROOT / C['slots']['contrast']['notes']
    if not p.exists():
        return {}
    return {m.group(2).strip(): m.group(1).lower() == 'x' for m in re.finditer(r'^- \[( |x|X)\]\s*(.+)$', p.read_text(), flags=re.M)}


def a11y_done(C, pattern):
    st = a11y_status(C)
    hits = [v for k, v in st.items() if re.search(pattern, k, flags=re.I)]
    return bool(hits) and all(hits)


def slot_contrast(C):
    P = C['panels']['contrast']
    S = C['slots']['contrast']
    paths = [ROOT / p for p in S['paths'] if (ROOT / p).exists()]
    if not paths or not a11y_done(C, r'^Contrast'):
        return panel('contrast', P, pending(C, P['who'], P['file_label']), ('waiting', P['who']))
    d = json.loads(paths[0].read_text())
    FIG['contrast_source'] = rel(paths[0])
    return panel('contrast', P, contrast_from(d, C), 'ready')


SURF = [('newsprint', 'Newsprint'), ('white', 'White'), ('charcoal', 'Charcoal'), ('prussian', 'Prussian')]
USE_WORD = {'text': 'Text', 'large text and graphics only': 'Large text and graphics', 'neither text nor a needed graphic': 'Neither'}


def contrast_from(d, C):
    T = d['totals']
    by = T['byResult']
    FIG['contrast'] = {'totals': T}
    pal, _ = tokens()
    hexes = {k.replace('-', ''): v.upper() for k, v in pal.items()}
    # the palette on the four grounds: a swatch of the color, its ratio and what the guide lets it do there
    head = '<th scope="col">Color</th>' + ''.join(f'<th scope="col">On {n}</th>' for _, n in SURF)
    rows = []
    for r in d['paletteMatrix']:
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', r['token'].split('.')[-1]).title()
        cells = []
        for key, sname in SURF:
            ratio, use = r.get(key), r.get(key + 'Use', '')
            g = GROUND[key]
            light = key in ('charcoal', 'prussian')
            red_on_prussian = r['hex'].upper() == '#E63946' and key == 'prussian'
            sw = '' if red_on_prussian else f'<i class="sw" style="background:{r["hex"]}" aria-hidden="true"></i>'
            word = 'Never: red stays off Prussian' if red_on_prussian else USE_WORD.get(use, use.capitalize())
            if ratio is not None and float(ratio) == 1.0:
                word = 'The same color'
            cells.append(f'<td class="mx {"lt" if light else "dk"}" style="background:{g}">{sw}<span class="r">{float(ratio):.2f}</span><span class="u">{esc(word)}</span></td>')
        rows.append(f'<tr><th scope="row"><i class="sw" style="background:{r["hex"]}" aria-hidden="true"></i>{esc(name)}<span class="hx">{esc(r["hex"])}</span></th>{"".join(cells)}</tr>')
    matrix = (f'<h3 class="sub">The palette on its four grounds</h3><p>Each cell gives the ratio and what the guide lets that color do on that ground. '
              f'Text needs 4.5 to 1, and large text, icons, borders and needed graphics need 3 to 1.</p>'
              f'<div class="tw" role="region" tabindex="0" aria-label="The palette on its four grounds; scrolls sideways" data-red="specimen"><table class="matrix"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    # every failing pair, and the pairs the guide permits under a threshold
    fails = d.get('failures', [])
    if fails:
        fl = ''.join(f'<tr><th scope="row">{esc(f.get("css") or f.get("token"))}</th><td>{esc(f.get("surface"))}</td><td>{esc(f.get("theme"))}</td><td class="num">{f.get("ratio")}</td><td class="num">{f.get("threshold")}</td></tr>' for f in fails)
        fail_html = f'<div class="tw" role="region" tabindex="0" aria-label="Failing pairs; scrolls sideways"><table><caption>Every failing pair</caption><thead><tr><th scope="col">Token</th><th scope="col">Surface</th><th scope="col">Theme</th><th scope="col">Ratio</th><th scope="col">Needs</th></tr></thead><tbody>{fl}</tbody></table></div>'
    else:
        fail_html = '<p class="nofail">No pair fails. The list of failing pairs is empty.</p>'
    groups = {}
    for p in d['permittedBelowThreshold']:
        groups.setdefault(p.get('permittedBecause') or p.get('criterion') or '', []).append(p)
    gl = ''.join(f'<tr><th scope="row">{esc(strip_codes(reason))}</th><td class="num">{len(ps)}</td><td class="toks">{esc(", ".join(sorted({p["css"].replace("--oa-", "") for p in ps})))}</td></tr>'
                 for reason, ps in sorted(groups.items(), key=lambda kv: -len(kv[1])))
    under = d['marksInsideGrounds'].get('underThreshold') or [r for r in d['marksInsideGrounds']['rows'] if r.get('result') not in ('pass',)]
    ul = ''.join(f'<tr><th scope="row">{esc(r.get("token", "").replace("oa.color.", ""))}</th><td>{esc(r.get("ground", "").replace("oa.color.", ""))}</td><td class="num">{r.get("ratio")}</td><td class="num">{r.get("threshold")}</td><td>{esc(strip_codes(r.get("note", "")))}</td></tr>' for r in under)
    ch26 = T.get('chapter26TableRatioResults', {}).get('match', 0)
    body = (f'<p class="intro">The accessibility lead measured {T["pairs"]} pairs, every color token on every surface it may sit on, in the light and the dark theme. '
            f'{nw(by.get("pass", 0))} pass, {nw(by.get("exempt", 0))} are exempt under WCAG’s own terms or carry no meaning, {nw(by.get("permitted", 0))} sit under their threshold where a stated rule of the guide covers them, and {nw(T["failures"], "none")} fail.</p>'
            f'{matrix}<h3 class="sub">Failing pairs</h3>{fail_html}'
            f'<h3 class="sub">Pairs under a threshold, and why the guide permits them</h3><p>{T["permittedBelowThreshold"]} pairs sit under the threshold a text or graphic role would need. Each falls into one of these cases.</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="Pairs under a threshold; scrolls sideways"><table><thead><tr><th scope="col">Why the guide permits it</th><th scope="col">Pairs</th><th scope="col">Tokens</th></tr></thead><tbody>{gl}</tbody></table></div>'
            f'<details class="more"><summary>{len(under)} marks under 3 to 1 on a field or band inside a surface</summary><p class="caption">{esc(strip_codes(d["marksInsideGrounds"]["note"]))}</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="Marks inside grounds; scrolls sideways"><table><thead><tr><th scope="col">Token</th><th scope="col">Ground</th><th scope="col">Ratio</th><th scope="col">Needs</th><th scope="col">Note</th></tr></thead><tbody>{ul}</tbody></table></div></details>'
            f'<dl class="facts"><div><dt>Chapter 26’s published ratios</dt><dd>{nw(ch26)} of {T.get("chapter26TableRatiosChecked", 0)} in the token table and {T.get("chapter26ProseMatches", 0)} of {T.get("chapter26ProseRatiosChecked", 0)} in its words match the recomputed ratio.</dd></div>'
            f'<div><dt>The two token files</dt><dd>{nw(T.get("cssValuesDifferingFromJson", 0)).capitalize()} values differ between tokens.css and tokens.json, and {nw(T.get("storedRatiosDiffering", 0), "none")} of {T.get("storedRatiosChecked", 0)} stored ratios differ from the measured one.</dd></div></dl>')
    return body


def slot_tokens(C):
    P = C['panels']['tokens']
    notes = ROOT / C['slots']['tokens']['notes']
    txt = notes.read_text() if notes.exists() else ''
    m = re.search(r'(work/[\w./-]*[Pp]arity[\w.-]*\.json)', txt)
    if not m or not (ROOT / m.group(1)).exists():
        return panel('tokens', P, pending(C, P['who'], P['file_label']), ('waiting', P['who']))
    d = json.loads((ROOT / m.group(1)).read_text())
    FIG['token_parity'] = {'source': m.group(1), 'pass': d.get('pass'), 'page': d.get('page'), 'page_sha256': d.get('page_sha256')}
    par = d['parity']
    steps = ''.join(f'<tr><th scope="row">{esc(s["step"].capitalize())}</th><td>{"Passes" if s["result"] == "pass" else "<b>Fails</b>"}</td><td>{esc(strip_codes(s["detail"]))}</td></tr>' for s in d['suite']['steps'])
    page = ''.join(f'<tr><th scope="row">{esc(c["check"][:1].upper() + c["check"][1:])}</th><td>{"Passes" if c["pass"] else "<b>Fails</b>"}</td><td>{esc(strip_codes(c["detail"]))}</td></tr>' for c in d.get('page_checks', []))
    tf = d['token_files']
    body = (f'<p class="intro">{"tokens.css and tokens.json agree" if par["pass"] else "The token files disagree"}: {esc(par["output"][0].split(": ", 1)[-1])}. '
            f'Release {esc(tf.get("version", ""))}, {tf["tokens.css"]["bytes"]:,} and {tf["tokens.json"]["bytes"]:,} bytes.</p>'
            f'<h3 class="sub">The token tests</h3><div class="tw" role="region" tabindex="0" aria-label="The token tests; scrolls sideways"><table><thead><tr><th scope="col">Step</th><th scope="col">Result</th><th scope="col">What it found</th></tr></thead><tbody>{steps}</tbody></table></div>'
            f'<h3 class="sub">The preview against the token files</h3><div class="tw" role="region" tabindex="0" aria-label="The preview against the token files; scrolls sideways"><table><thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">What it found</th></tr></thead><tbody>{page}</tbody></table></div>'
            f'<p class="caption">Run {esc(words_when(d["suite"].get("run", "")))} by the engineer on the Gate 2 preview.</p>')
    return panel('tokens', P, body, 'ready' if d.get('pass') else ('waiting', P['who']))


def ev_label(stem):
    s = stem.split('_', 1)[-1]
    s = re.sub(r'^Open-', '', s)
    sc = lambda x: x.replace('-', ' ')[:1].upper() + x.replace('-', ' ')[1:].lower()
    m = re.match(r'Ch(\d\d)-(.+)-(1440|390)$', s)
    if m:
        return f'Chapter {m.group(1)}, {sc(m.group(2))}', m.group(3)
    m = re.match(r'(.+)-(1440|390)$', s)
    if m:
        return sc(m.group(1)), m.group(2)
    return s.replace('-', ' '), ''


def shot_row(files, labels, region_label):
    figs = []
    for k, (p, lab) in enumerate(zip(files, labels)):
        r = image({'copy': rel(p)}, slug('Evidence', p.stem.split('_', 1)[-1]))
        figs.append(f'<figure class="phone"><img src="{r["src"]}" width="{r["w"]}" height="{r["h"]}" alt="{esc(lab)}" loading="{"eager" if k < 3 else "lazy"}" decoding="async"><figcaption>{esc(lab)}</figcaption></figure>')
    return f'<div class="phones" role="region" tabindex="0" aria-label="{esc(region_label)}; scrolls sideways">{"".join(figs)}</div>'


def a11y_findings(C):
    p = ROOT / C['slots']['screens']['notes']
    t = p.read_text() if p.exists() else ''
    out = []
    for sev in ('Should fix', 'Could fix'):
        sec = md_section(t, [re.escape(sev)]) or ''
        for m in re.finditer(r'^\*\*([A-Z]-\d+)\.\s*(.+?)\*\*', sec, flags=re.M):
            out.append((sev, m.group(1), m.group(2)))
    return out


def walk_html(d, ev, title, key):
    parts = []
    for w in ('1440', '390'):
        stops = d['widths'].get(w, [])
        if not stops:
            continue
        seen, pick = set(), []
        for s in stops:
            if s['segment'] not in seen or s['visibility'] != 'clear':
                pick.append(s)
                seen.add(s['segment'])
        files = [ev / s['screenshot'] for s in pick if s.get('screenshot') and (ev / s['screenshot']).exists()]
        labs = [f'Stop {s["stop"]}, {s["segment"]}: {s["role"]} “{s["name"] or "no name"}”, {s["visibility"]}' for s in pick if s.get('screenshot') and (ev / s['screenshot']).exists()]
        rows = ''.join(f'<tr><td class="num">{s["stop"]}</td><td>{esc(s["segment"])}</td><td>{esc(s["keys"])}</td><td>{esc(s["role"] or "")}</td><td>{esc(s["name"] or "")}</td><td>{esc(s["visibility"])}</td></tr>' for s in stops)
        parts.append(f'<h4 class="sheet-h">At {w} px: {len(stops)} stops</h4><p class="caption">The first stop of each part of the walk, and every stop whose focus was not fully clear, at true size.</p>'
                     + shot_row(files, labels=labs, region_label=f'{title} at {w} px')
                     + f'<details class="more"><summary>Every stop at {w} px, with its accessible name</summary><div class="tw" role="region" tabindex="0" aria-label="Stops at {w} px; scrolls sideways"><table><thead><tr><th scope="col">Stop</th><th scope="col">Part</th><th scope="col">Keys</th><th scope="col">Role</th><th scope="col">Accessible name</th><th scope="col">Focus</th></tr></thead><tbody>{rows}</tbody></table></div></details>')
        FIG.setdefault('keyboard', {})[f'{key}-{w}'] = {'stops': len(stops), 'shown': len(files)}
    return ''.join(parts)


def slot_screens(C):
    P = C['panels']['screens']
    d = ROOT / C['slots']['screens']['dir']
    parts, waiting = [], []
    fnd = a11y_findings(C)
    if fnd and a11y_done(C, r'.'):
        li = ''.join(f'<li><span class="sev">{esc(s)}</span> {esc(strip_codes(x).rstrip("."))}.</li>' for s, c, x in fnd)
        MOVED.update(c for _, c, _ in fnd)
        parts.append(f'<h3 class="sub">What the accessibility lead found</h3><p>{nw(len(fnd)).capitalize()} findings, none a failure of WCAG 2.2 at level AA, each with its fix and its owner in the accessibility lead’s report.</p><ul class="findings">{li}</ul>')
    if a11y_done(C, r'^Opening screens'):
        opens = sorted(d.glob('*_Open-*.png'))
        phone = [p for p in opens if p.stem.endswith('-390')]
        desk = [p for p in opens if p.stem.endswith('-1440')]
        parts.append(f'<h3 class="sub">Each chapter’s opening screen</h3><p>The opening screen of every chapter, the identity proofs and the preview’s new front page, at 390 px on a phone, in one row at true size. Each opens at 1440 px below the row.</p>'
                     + shot_row(phone, [ev_label(p.stem)[0] for p in phone], 'Opening screens at 390 px'))
        dets = []
        for p in desk:
            lab, _ = ev_label(p.stem)
            r = image({'copy': rel(p)}, slug('Evidence', p.stem.split('_', 1)[-1]))
            dets.append(f'<details class="more"><summary>{esc(lab)} at 1440 px</summary>{frame(r, lab + ", the opening screen at 1440 px")}</details>')
        parts.append(f'<div class="desk">{"".join(dets)}</div>')
        FIG['screens_open'] = len(opens)
    else:
        waiting.append('the opening screens')
    kw = d / '20261111_Gate-2-Keyboard-Walk.json'
    if a11y_done(C, r'^Keyboard walk on the frozen') and kw.exists():
        parts.append('<h3 class="sub">The keyboard walk on the chapters page</h3><p>Keys only, from the top through the skip link, the contents, a rule and its cross-reference, a live form in chapter 18, a player in chapter 17 and the token table’s search and copy in chapter 26.</p>'
                     + walk_html(json.loads(kw.read_text()), d, 'Keyboard walk', 'frozen'))
    else:
        waiting.append('the keyboard walk')
    kp = d / '20261111_Gate-2-Keyboard-Walk-Preview.json'
    if a11y_done(C, r'^Keyboard walk on the preview') and kp.exists():
        parts.append('<h3 class="sub">The keyboard walk on the preview’s front pages</h3><p>The cover, the contents and the new “Where to start” page, by keys alone.</p>'
                     + walk_html(json.loads(kp.read_text()), d, 'Keyboard walk on the preview', 'preview'))
    else:
        waiting.append('the keyboard walk on the preview')
    mf = d / '20261111_Gate-2-Motion-Frames.json'
    if a11y_done(C, r'^Reduced-motion') and mf.exists():
        m = json.loads(mf.read_text())
        rows = []
        for r in m['reduced']:
            pl = r['player']
            files = sorted(d.glob(f'*_Motion-Ch17-{pl if pl[0].isdigit() else pl.capitalize()}-*.png'))
            order = ['Reduced-Rest', 'Reduced-Final', 'Normal-Rest', 'Normal-Frame-1', 'Normal-Frame-2', 'Normal-Frame-3']
            files = sorted(files, key=lambda p: next((i for i, o in enumerate(order) if p.stem.endswith(o)), 9))
            labs = [p.stem.split(f'-{pl}-' if pl[0].isdigit() else f'-{pl.capitalize()}-', 1)[-1].replace('-', ' ').replace('Reduced', 'Reduced motion,').replace('Normal', 'Normal motion,') for p in files]
            nm = f'Player {pl.replace("-", ".", 1)}' if pl[0].isdigit() else f'The {pl.lower()} player'
            rows.append(f'<details class="more"><summary>{esc(nm)}: {esc(r["afterPlay"]["status"])}</summary>{shot_row(files, labs, nm)}</details>')
        ts = m.get('themeSwitch')
        theme = ''
        tfiles = sorted(d.glob('*_Motion-Ch18-Theme-Switch-*.png'))
        if tfiles:
            theme = f'<details class="more"><summary>Chapter 18’s theme switch, at once in both modes</summary>{shot_row(tfiles, [p.stem.split("Switch-", 1)[-1].replace("-", " ") for p in tfiles], "Theme switch")}</details>'
        parts.append(f'<h3 class="sub">Motion, normal and reduced</h3><p>With motion reduced, each of chapter 17’s {nw(len(m["reduced"]))} players lands on its last frame the moment Play is pressed, and nothing moves after. With motion on, each runs its frames. Each row opens to its pictures at true size.</p>{"".join(rows)}{theme}')
    else:
        waiting.append('motion, normal and reduced')
    fc = d / '20261111_Gate-2-Forced-Colors.json'
    if a11y_done(C, r'^Forced-colors') and fc.exists():
        f = json.loads(fc.read_text())
        files = [d / x['file'] for x in f if (d / x['file']).exists()]
        labs = [x['file'].split('Forced-Colors-', 1)[-1].replace('-1440.png', '').replace('-', ' ') for x in f if (d / x['file']).exists()]
        parts.append(f'<h3 class="sub">Forced colors</h3><p>Chapters 05, 11, 17 and 18 with the system’s forced colors on, as Windows high contrast draws them.</p><details class="more"><summary>Open {nw(len(files))} pictures at true size</summary>{shot_row(files, labs, "Forced colors")}</details>')
    else:
        waiting.append('forced colors')
    if waiting and not parts:
        return panel('screens', P, pending(C, P['who'], P['file_label']), ('waiting', P['who']))
    if waiting:
        parts.append(f'<div class="pending" role="status"><p><b>Waiting for {esc(owner(C, P["who"]))}.</b> Still to come: {esc(join_words(waiting))}.</p></div>')
        return panel('screens', P, ''.join(parts), ('partial', P['who']))
    return panel('screens', P, ''.join(parts), 'ready')


def slot_scores(C):
    P = C['panels']['scores']
    S = C['slots']['scores']
    parts, status = [], 'ready'
    cdp = ROOT / S['cd']
    if cdp.exists():
        parts.append(cd_table(json.loads(cdp.read_text())))
    else:
        parts.append(f'<h3 class="sub">The creative director’s scores</h3>{pending(C, P["who_cd"], P["cd_file_label"])}')
        status = ('waiting', P['who_cd'])
    dp = ROOT / S['drift']
    dtext = dp.read_text() if dp.exists() else ''
    sec = md_section(dtext, [r'score']) if dp.exists() else None
    m = re.search(r'\b([1-5])\b', sec or '') if sec and 'pending' not in sec.lower() else None
    if m:
        def titles(name):
            s = md_section(dtext, [name]) or ''
            return [(a, b.rstrip('.')) for a, b in re.findall(r'^\*\*([A-Z]{1,2}\d+)\.\s*(.+?)\*\*', s, flags=re.M)]
        must, should = titles(r'must fix'), titles(r'should fix')
        MOVED.update(a for a, _ in must + should)
        FIG['drift'] = {'source': rel(dp), 'score': int(m.group(1)), 'must_fix': len(must), 'should_fix': len(should)}
        lead = re.sub(r'^\*\*[^*]*\*\*\s*', '', sec.strip())
        li = lambda xs: ''.join(f'<li>{md_inline(b)}.</li>' for _, b in xs)
        parts.append(f'<h3 class="sub">The drift review</h3><div class="drift"><p class="big">{esc(m.group(1))}<span> of 5</span></p><div>'
                     + ''.join(f'<p>{md_inline(x)}</p>' for x in lead.split('\n\n') if x.strip())
                     + f'<p>{nw(len(must)).capitalize()} Must fix and {nw(len(should))} Should fix, each with its fix and its owner in the team’s report.</p></div></div>'
                     + f'<div class="tcols"><div class="tcol"><h4>Must fix</h4><ul>{li(must)}</ul></div><div class="tcol"><h4>Should fix</h4><ul>{li(should)}</ul></div></div>')
    else:
        parts.append(f'<h3 class="sub">The drift review</h3>{pending(C, P["who_drift"], P["drift_file_label"])}')
        status = ('waiting', P['who_cd']) if status != 'ready' else ('partial', P['who_drift'])
        return panel('scores', P, ''.join(parts), status)
    if status != 'ready':
        status = ('partial', P['who_cd'])
    return panel('scores', P, ''.join(parts), status)


def cd_table(d):
    crit = d.get('criteria') or [{'key': k, 'name': k} for k in ('craft', 'clarity', 'brand_fidelity', 'usefulness', 'evidence_honesty', 'accessibility')]
    items = d.get('items', [])
    head = '<th scope="col">Item</th>' + ''.join(f'<th scope="col">{esc(c["name"])}</th>' for c in crit) + '<th scope="col">Ready</th>'
    rows = []
    for it in items:
        sc = it.get('scores', {})
        cells = ''.join(f'<td class="num sc{" lo" if isinstance(sc.get(c["key"]), (int, float)) and sc.get(c["key"]) < 4 else ""}">{esc(sc.get(c["key"], ""))}</td>' for c in crit)
        rows.append(f'<tr><th scope="row">{esc(it.get("name", it.get("key")))}</th>{cells}<td>{"Yes" if it.get("ready") else "<b>Not yet</b>"}</td></tr>')
    FIG['cd_scores'] = {'items': len(items), 'ready': sum(1 for i in items if i.get('ready'))}
    tot = d.get('totals', {})
    nr = [i for i in items if not i.get('ready')]
    summ = (f'<p class="intro">{nw(len(items) - len(nr)).capitalize()} of {len(items)} items are ready.'
            + ((f' {nr[0]["name"]}, is not ready yet, with {nw(tot.get("must_fix", 0))} Must fix.' if len(nr) == 1 else
                f' {join_words([i["name"] for i in nr])} are not ready yet, with {nw(tot.get("must_fix", 0))} Must fix between them.') if nr else '')
            + f' The creative director lists {nw(tot.get("should_fix", 0))} Should fix across the guide.</p>')
    under = []
    for i in items:
        for c in crit:
            v = i.get('scores', {}).get(c['key'])
            if isinstance(v, (int, float)) and v < 4:
                under.append(f'<li><b>{esc(i["name"])}, {esc(c["name"].lower())}, {v}.</b> {md_inline(i.get("reasons", {}).get(c["key"], ""))}</li>')
    summ += f'<ul class="findings">{"".join(under)}</ul>' if under else ''
    return (f'<h3 class="sub">The creative director’s scores</h3>{summ}<p>Scores run from 1 to 5, and an item is ready at 4 or more on every criterion. A box marks a score under 4.</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="Scores; scrolls sideways"><table class="scores"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def slot_tested(C):
    P = C['panels']['tested']
    cols, waiting = [], []
    for s in C['slots']['tested']:
        p = ROOT / s['file']
        who = 'the board builder' if s['who'] == 'board' else owner(C, s['who'])
        if not p.exists():
            waiting.append(who)
            continue
        t = p.read_text()
        head = '\n'.join(t.splitlines()[:12]).lower()
        tested = md_section(t, [r'tested', r'what i tested', r'checked'])
        nott = md_section(t, [r'not tested', r'what i could not test', r'not checked'])
        both = md_section(t, [r'tested and not tested', r'tested and not tested\b.*'])
        if both is not None and (tested is None or nott is None):
            parts = re.split(r'^(?:#+\s*|\*\*)not tested\b.*$', both, flags=re.I | re.M, maxsplit=1)
            tested, nott = parts[0], (parts[1] if len(parts) > 1 else '')
        ti, ni = md_items(tested or ''), md_items(nott or '')
        unfinished = ('in progress' in head or (s['who'] == 'a11y' and not all(a11y_status(C).values() or [False]))
                      or not ti or (nott or '').strip().lower().startswith('(pending'))
        if unfinished:
            waiting.append(who)
            continue
        FIG.setdefault('tested_sources', []).append(rel(p))
        cols.append(f'<div class="tcol"><h4>{esc(who[:1].upper() + who[1:])}</h4>'
                    f'<p class="label">Not tested</p><ul>{"".join(f"<li>{md_inline(x)}</li>" for x in ni) or "<li>Nothing listed.</li>"}</ul>'
                    f'<details class="more"><summary>What {esc(who)} tested, {len(ti)} items</summary><ul>{"".join(f"<li>{md_inline(x)}</li>" for x in ti)}</ul></details></div>')
    dev = ''.join(f'<li>{esc(x)}</li>' for x in P['devices'])
    body = (f'<p class="intro">{esc(P["lede"])}</p><div class="device"><h3 class="sub">{esc(P["device_h"])}</h3><p>{esc(P["device_lede"])}</p><ul>{dev}</ul></div>'
            f'<div class="tcols">{"".join(cols)}</div>')
    if waiting:
        body += f'<div class="pending" role="status"><p><b>Waiting for lists from {esc(join_words(waiting))}.</b> Each joins this panel when its notes carry a Tested and a Not tested section.</p></div>'
        return panel('tested', P, body, ('partial', join_words(waiting)))
    return panel('tested', P, body, 'ready')


def join_words(xs):
    xs = list(dict.fromkeys(xs))
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def weight_panel(C):
    P = C['panels']['weight']
    W = C['slots']['weight']
    fz = pathlib.Path(W['frozen'])
    frozen = fz.stat().st_size if fz.exists() else W['frozen_bytes_logged']
    FIG['weight'] = {'frozen_bytes': frozen, 'frozen_source': str(fz) if fz.exists() else 'handoff V15', 'budget': W['budget_bytes'],
                     'limit': W['limit_bytes'], 'projected': W['projected_bytes']}
    pv = ROOT / W['preview']
    bars = [('The chapters page today, 16 chapters', frozen, 'now')]
    status = 'ready'
    if pv.exists():
        built_pv = datetime.datetime.fromtimestamp(pv.stat().st_mtime, datetime.timezone.utc)
        bars.append((f'The Gate 2 preview, with its fonts, as built {built_pv.strftime("%B")} {built_pv.day}', pv.stat().st_size, 'now'))
        FIG['weight']['preview_bytes'] = pv.stat().st_size
    else:
        status = ('partial', 'engineer')
    bars += [('The finished guide, as the engineer projects it', W['projected_bytes'], 'proj'),
             ('The page budget', W['budget_bytes'], 'budget'), ('The host’s limit for one page', W['limit_bytes'], 'limit')]
    mb = lambda b: f'{b / 1e6:.2f}'
    FILL.update({'frozen_mb': mb(frozen), 'projected_mb': f'{W["projected_bytes"] / 1e6:.1f}', 'budget_mb': f'{W["budget_bytes"] / 1e6:.1f}'})
    mx = W['limit_bytes']
    rows = ''.join(f'<tr><th scope="row">{esc(n)}</th><td class="barcell"><span class="bar {k}" data-mark="bar" data-value="{b}" data-key="{esc(n)}" style="width:{100 * b / mx:.3f}%"></span></td><td class="num">{mb(b)} MB</td></tr>'
                   for n, b, k in bars)
    body = (f'<p class="intro">{esc(fill(P["lede"]))}</p><figure class="wfig" data-spec="page-weight">'
            f'<div class="tw" role="region" tabindex="0" aria-label="Page weight; scrolls sideways"><table class="wt"><caption>Page weight in megabytes, each bar drawn from zero against the host’s 16 MB limit</caption>'
            f'<thead><tr><th scope="col">Page</th><th scope="col"><span class="vh">Bar</span></th><th scope="col">Size</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<figcaption class="caption">Sources: the frozen chapters page in the studio’s workspace, read by its size on disk; the engineer’s projection of November 10; the build’s budget and the host’s limit.'
            f'{"" if pv.exists() else " The preview’s bar joins when the engineer builds it."}</figcaption></figure>')
    return panel('weight', P, body, status)


# ------------------------------------------------------------------------------------------------------- page
STATUS = {}


def panel(key, P, body, status):
    STATUS[key] = status
    n = P['n']
    refs = P['refs']
    check_refs(refs, 'panel ' + key)
    if MOVED:
        refs += ' · from teammates’ files: ' + ' · '.join(sorted(MOVED, key=lambda c: (re.sub(r'[^A-Z]', '', c), int(re.sub(r'\D', '', c) or 0))))
        MOVED.clear()
    return (f'<section class="sec" id="p-{key}" aria-labelledby="h-{key}"><div class="sec-top"><p class="label">Panel {n}</p>{status_chip(status)}</div>'
            f'<h2 class="sec-h" id="h-{key}">{esc(P["title"])}</h2>{body}<p class="codes">Reference: {esc(refs)}</p></section>')


def status_chip(st, short=False):
    kind = st if isinstance(st, str) else st[0]
    words = CONTENT_DATA['status_short'][kind] if short else status_words(st)
    return f'<span class="st {kind}">{esc(words)}</span>'


def status_words(st):
    if st == 'ready':
        return CONTENT_DATA['status_words']['ready']
    kind, who = st
    w = CONTENT_DATA['owners'].get(who, who)
    return CONTENT_DATA['status_words'][kind].format(who=w)


CONTENT_DATA = {}


def cover(C, built):
    K = C['cover']
    order = ['approves', 'refinements', 'craft', 'similarity', 'contrast', 'tokens', 'screens', 'scores', 'tested', 'weight']
    toc = ''.join(f'<li><a href="#p-{k}"><span class="n">{C["panels"][k]["n"]:02d}</span><span class="t">{esc(C["panels"][k]["nav"])}</span></a>{status_chip(STATUS[k], short=True)}</li>' for k in order)
    ready = sum(1 for k in order if STATUS[k] == 'ready')
    deck = ''.join(f'<p>{esc(x)}</p>' for x in K['deck'])
    return (f'<header class="cover"><div class="mast"><b>OATH &amp; ACTION</b><span class="label">{esc(K["kicker"])}</span></div>'
            f'<p class="label for">{esc(fill(K["for_line"]))}</p><h1>{esc(K["title"])}</h1>'
            f'<div class="cover-grid"><div class="deck">{deck}<p class="caption">{esc(K["minutes"])}</p></div>'
            f'<nav class="toc" aria-labelledby="toc-h"><p class="label" id="toc-h">{esc(K["toc_h"])} · {ready} of {len(order)} ready</p><ol>{toc}</ol></nav></div></header>')


CSS = r'''
:root{--m:16px;--mr:16px;--max:80rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--np:var(--oa-color-surface-newsprint);--wink:var(--oa-color-text-primary-on-white);--wink-2:var(--oa-color-text-secondary-on-white);
--whair:var(--oa-color-border-hairline-on-white);--wstrong:var(--oa-color-border-strong-on-white);color-scheme:light}
@media (min-width:48em){:root{--m:var(--oa-layout-grid-tablet-margin);--mr:var(--oa-layout-grid-tablet-margin)}}
@media (min-width:64em){:root{--m:var(--oa-layout-grid-desktop-margin);--mr:var(--oa-layout-grid-desktop-margin)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--np);scroll-padding-top:var(--oa-space-300)}
body{margin:0;background:var(--np);color:var(--ink);font:var(--oa-type-body);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration-thickness:var(--oa-border-width-underline);text-underline-offset:.2em}
:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring-on-newsprint);outline-offset:var(--oa-border-focus-offset)}
.card :focus-visible,.tw:focus-visible,.card .frame:focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
p{margin:0 0 var(--oa-space-150);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
h1,h2,h3,h4{margin:0}
section{border-top:0;margin-top:0;padding-top:0}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.board{max-width:calc(var(--max) + var(--m) + var(--mr));margin:0 auto;padding:0 var(--mr) var(--oa-space-1300) var(--m)}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0}
.caption{font:var(--oa-type-caption);color:var(--ink-2)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max);margin-bottom:var(--oa-space-300)}
.codes{font:var(--oa-type-caption);color:var(--ink-2);margin:var(--oa-space-300) 0 0;font-variant-numeric:tabular-nums}
.card .codes{color:var(--wink-2);border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);padding-top:var(--oa-space-100);margin-top:var(--oa-space-300)}
code{font-size:.9em}
/* cover */
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);padding:var(--oa-space-300) 0 var(--oa-space-200);border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.for{margin-top:var(--oa-space-800)}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-500);max-width:11ch;text-wrap:balance}
.cover-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500) var(--oa-space-800);align-items:start}
@media (min-width:64em){.cover-grid{grid-template-columns:minmax(0,6fr) minmax(0,5fr)}}
.deck p:not(.caption){font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.toc{border-top:var(--oa-border-width-rule) solid var(--strong)}
.toc .label{padding:var(--oa-space-150) 0 var(--oa-space-100)}
.toc ol{list-style:none;margin:0;padding:0}
.toc li{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-050) var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-050) 0}
.toc a{display:inline-flex;align-items:baseline;gap:var(--oa-space-150);min-height:2.75rem;align-items:center;text-decoration:none;font:var(--oa-type-ui);font-weight:600}
.toc a:hover .t{text-decoration:underline}
.toc .n{font-variant-numeric:tabular-nums;color:var(--ink-2);font-weight:400;min-width:1.6em}
.st{font:var(--oa-type-caption);font-weight:600;padding:0 .5em;max-width:100%;border:var(--oa-border-width-hairline) solid var(--strong);line-height:1.6}
.st.ready{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint);border-color:var(--oa-color-palette-charcoal)}
.st.waiting,.st.partial{background:transparent;color:var(--ink)}
.card .st.waiting,.card .st.partial{color:var(--wink)}
/* sections */
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-300)}
.sec-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-100) var(--oa-space-300)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:var(--oa-space-150) 0 var(--oa-space-400);text-wrap:balance;max-width:18ch}
.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:var(--oa-space-600) 0 var(--oa-space-200);text-wrap:balance}
.src-note{max-width:var(--oa-layout-measure-intro-max)}
.key{display:flex;flex-wrap:wrap;gap:var(--oa-space-100) var(--oa-space-400);margin:var(--oa-space-200) 0 0}
.key span{display:inline-flex;align-items:center;gap:var(--oa-space-100);font:var(--oa-type-caption)}
.key i{display:inline-block;width:14px;height:14px;border:var(--oa-border-width-hairline) solid var(--strong)}
.key .k-z i{width:28px;height:28px;background:repeating-linear-gradient(90deg,transparent 0 6px,var(--hair) 6px 7px),repeating-linear-gradient(0deg,transparent 0 6px,var(--hair) 6px 7px)}
/* groups and cards */
.grp{margin-top:var(--oa-space-800)}
.grp-h{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);padding-bottom:var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--strong)}
.card{background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300) var(--oa-space-200);margin-top:var(--oa-space-300);min-width:0}
@media (min-width:48em){.card{padding:var(--oa-space-400)}}
.card-h{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300)}
.card-h h4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);text-wrap:balance}
.tag{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--wstrong);padding:2px 6px;white-space:nowrap}
.tag.defect{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-white);border-color:var(--oa-color-palette-charcoal)}
.what{margin:var(--oa-space-150) 0 var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
.row{border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);padding:var(--oa-space-200) 0 var(--oa-space-100)}
.row-label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);margin:0 0 var(--oa-space-150);display:flex;flex-wrap:wrap;gap:var(--oa-space-050) var(--oa-space-300);max-width:none}
.row-label .zl{text-transform:none;letter-spacing:0;font:var(--oa-type-caption)}
.row-note{font:var(--oa-type-caption);color:var(--wink-2)}
.cells{display:flex;flex-wrap:wrap;gap:var(--oa-space-300) var(--oa-space-500);align-items:flex-start}
.row.stack .cells{flex-direction:column;flex-wrap:nowrap}
.shot{margin:0;min-width:0;max-width:100%;display:flex;flex-direction:column;gap:var(--oa-space-100)}
.shot figcaption{font:var(--oa-type-caption);color:var(--wink-2);border-top:var(--oa-border-width-bar) solid var(--oa-color-tint-stone-n70);padding-top:var(--oa-space-050)}
.frames{display:flex;flex-wrap:wrap;gap:var(--oa-space-150) var(--oa-space-300);align-items:flex-end;max-width:100%}
.rowgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,11.5rem),1fr));gap:0 var(--oa-space-300)}
.rowgrid .cells{gap:var(--oa-space-200) var(--oa-space-300)}
.shot.after figcaption{border-top-color:var(--oa-color-palette-charcoal)}
.shot figcaption b{color:var(--wink);font-weight:600}
.shot figcaption span{white-space:nowrap}
.frame{max-width:100%;line-height:0;align-self:flex-start}
.frame.wide{overflow-x:auto;overscroll-behavior-x:contain}
.frame img{display:block;max-width:none;height:auto}
.frame img.px{image-rendering:pixelated}
.frame.zoom{outline:var(--oa-border-width-hairline) dashed transparent}
.empty .none{min-height:3rem;display:flex;align-items:center;border:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88);padding:var(--oa-space-100) var(--oa-space-150);max-width:18rem}
.empty .none p{font:var(--oa-type-caption);color:var(--wink-2);margin:0}
.strip{display:flex;flex-wrap:wrap;gap:var(--oa-space-200);align-items:flex-end}
.strip-i{display:flex;flex-direction:column;gap:var(--oa-space-050);align-items:flex-start}
.nm{font:var(--oa-type-caption);color:var(--wink-2)}
details.more{margin-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
details.more>summary{cursor:pointer;font:var(--oa-type-ui);font-weight:600;min-height:2.75rem;display:flex;align-items:center;gap:var(--oa-space-100)}
.tiles{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:var(--oa-space-300) var(--oa-space-300)}
.tiles li{display:flex;flex-direction:column;gap:var(--oa-space-050);align-items:flex-start;width:8.5rem;min-width:0}
.tiles.zoomed li{width:9rem}
.tiles li .frame+.frame{margin-top:var(--oa-space-050)}
.tiles.amp li{width:auto}
.tiles .ov{font:var(--oa-type-ui);font-weight:700;font-variant-numeric:tabular-nums}
.tiles.shots li{width:auto;max-width:100%}
/* panel 1 */
.approve-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-800)}
@media (min-width:64em){.approve-grid{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}}
.col-open .sub,.col-ans .sub{margin-top:var(--oa-space-300)}
.open-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-150)}
.open{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-200)}
.ans{list-style:none;margin:0;padding:0;border-top:var(--oa-border-width-hairline) solid var(--hair)}
.ans li{padding:var(--oa-space-200) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.ans h4{font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-050)}
.ans p{font:var(--oa-type-body-small);margin:0}
.ans .codes{margin-top:var(--oa-space-100)}
.ans.three{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-500)}
@media (min-width:64em){.ans.three{grid-template-columns:repeat(3,minmax(0,1fr))}}
.decide{margin:0;padding-left:1.4em}
.dec-h{font:var(--oa-type-ui);font-weight:700;margin:var(--oa-space-300) 0 var(--oa-space-100)}
.pending{border:var(--oa-border-width-hairline) solid var(--strong);border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding:var(--oa-space-200) var(--oa-space-300);margin:var(--oa-space-200) 0;max-width:var(--oa-layout-measure-intro-max)}
.pending p{margin:0}
/* tables */
.tw{position:relative;overflow-x:auto;background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);margin:var(--oa-space-200) 0 var(--oa-space-100)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
caption{caption-side:top;text-align:left;padding:var(--oa-space-150) var(--oa-space-200);font:var(--oa-type-body-small);color:var(--wink-2);border-bottom:var(--oa-border-width-hairline) solid var(--whair)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-100) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--oa-color-tint-white-n55);vertical-align:bottom;white-space:nowrap}
tbody th{font:var(--oa-type-body-small);font-weight:600;text-transform:none;letter-spacing:0;color:var(--wink)}
td.toks{font:var(--oa-type-caption);color:var(--wink-2);overflow-wrap:anywhere}
.zl{font:var(--oa-type-caption);color:var(--wink-2);margin:calc(-1*var(--oa-space-100)) 0 var(--oa-space-200)}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
td.miss{font-weight:700}
.fl{display:block;font:var(--oa-type-caption);color:var(--wink-2);font-weight:400}
td.sc.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong);font-weight:700}
.facts{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-500);margin:var(--oa-space-200) 0;border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
.facts div{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.facts dt{font:var(--oa-type-ui);font-weight:700}
.facts dd{margin:var(--oa-space-050) 0 0;font:var(--oa-type-body-small)}
.sheet{margin-top:var(--oa-space-400);background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300) var(--oa-space-200)}
@media (min-width:48em){.sheet{padding:var(--oa-space-400)}}
.sheet .caption,.sheet .nm{color:var(--wink-2)}
.sheet-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-100)}
.sheet .tiles{margin-top:var(--oa-space-300)}
.pairs{list-style:none;margin:var(--oa-space-200) 0 0;padding:0;display:grid;gap:var(--oa-space-200)}
.pair{display:flex;flex-wrap:wrap;gap:var(--oa-space-300) var(--oa-space-500);align-items:flex-end;background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300)}
.pair .shot figcaption{color:var(--wink-2)}
.score{font:var(--oa-type-h4);margin:0;font-variant-numeric:tabular-nums}
.score span{display:block;font:var(--oa-type-caption);color:var(--wink-2)}
/* panel 9, 8, 10 */
.device{background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300);margin-top:var(--oa-space-300)}
.device .sub{margin-top:0}
.device ul{margin:0;padding-left:1.2em}
.tcols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-500);margin-top:var(--oa-space-400)}
@media (min-width:64em){.tcols{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tcol{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-150)}
.tcol h4{font:var(--oa-type-h4);margin-bottom:var(--oa-space-150)}
.tcol ul{margin:var(--oa-space-050) 0 var(--oa-space-200);padding-left:1.2em;font:var(--oa-type-body-small)}
.tcol li{margin-bottom:var(--oa-space-050)}
.big{font:var(--oa-type-section);margin:0}
.drift{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200) var(--oa-space-500);align-items:start}
@media (min-width:48em){.drift{grid-template-columns:auto minmax(0,1fr)}}
.big span{font:var(--oa-type-h4)}
.wfig{margin:0}
.wt th{width:16rem;font-weight:600}
.barcell{width:60%;min-width:12rem}
.bar{display:block;height:1.25rem;background:var(--oa-color-palette-charcoal)}
.bar.proj{background:var(--oa-color-tint-stone-n55)}
.bar.budget,.bar.limit{background:transparent;box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--oa-color-palette-charcoal)}
table.matrix{min-width:46rem}
table.matrix tbody th{white-space:nowrap;vertical-align:middle}
table.matrix .hx{display:block;font:var(--oa-type-caption);color:var(--wink-2);font-variant-numeric:tabular-nums;margin-left:calc(18px + .5em)}
.sw{display:inline-block;width:18px;height:18px;vertical-align:-3px;margin-right:.5em;box-shadow:inset 0 0 0 1px rgba(18,18,18,.35)}
td.mx{vertical-align:middle;min-width:9.5rem;border-bottom:1px solid var(--oa-color-tint-stone-n88)}
td.mx .sw{width:22px;height:22px;vertical-align:-5px;box-shadow:none}
td.mx .r{font:var(--oa-type-ui);font-weight:700;font-variant-numeric:tabular-nums}
td.mx .u{display:block;font:var(--oa-type-caption)}
td.mx.dk{color:var(--oa-color-palette-charcoal)}
td.mx.lt{color:var(--oa-color-palette-newsprint)}
.nofail{font:var(--oa-type-h4);margin:var(--oa-space-100) 0 var(--oa-space-200)}
.phones{display:flex;gap:var(--oa-space-300);overflow-x:auto;padding:var(--oa-space-200);background:var(--white);border:var(--oa-border-width-hairline) solid var(--whair);margin-top:var(--oa-space-200)}
.phone{margin:0;flex:0 0 auto;display:flex;flex-direction:column;gap:var(--oa-space-100)}
.phone img{display:block;max-width:none;outline:1px solid var(--oa-color-tint-stone-n70)}
.phone figcaption{font:var(--oa-type-caption);color:var(--wink-2)}
.desk{margin-top:var(--oa-space-200);display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-400)}
@media (min-width:64em){.desk{grid-template-columns:repeat(2,minmax(0,1fr))}.desk details[open]{grid-column:1/-1}}
.findings{margin:0 0 var(--oa-space-200);padding-left:1.2em;max-width:var(--oa-layout-measure-intro-max)}
.findings li{margin-bottom:var(--oa-space-100)}
.sev{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin-right:.4em}
pre.raw{white-space:pre-wrap;font-size:.875rem;background:var(--white);color:var(--wink);padding:var(--oa-space-200);border:var(--oa-border-width-hairline) solid var(--whair);max-height:28rem;overflow:auto}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:none}
@media print{.toc{display:none}details{display:block}}
'''


def strip_css(t):
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'/\*.*?\*/', '', t, flags=re.S)).strip()


def build_page(C, sections):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(C["title"])}</title>
<meta name="chart-views" content="overview"><meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400;1,500&display=swap" rel="stylesheet">
<style>{strip_css(BOARD_BASE.read_text())}
{strip_css(TOKENS_CSS.read_text())}
{strip_css(CSS)}</style></head>
<body><main class="board" data-view-root="overview">
{sections}
<p class="foot caption">{esc(fill(C["foot"]))}</p>
</main></body></html>'''


def visible_text(page):
    t = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    t = re.sub(r'<span class="vh">[^<]*</span>', '', t)
    t = re.sub(r'</?(?:p|li|ul|ol|h\d|td|th|tr|div|figure|figcaption|caption|blockquote|section|header|nav|aside|main|table|thead|tbody|summary|details|dt|dd|dl|pre)\b[^>]*>|<br\s*/?>', ' ', t)
    return html.unescape(re.sub(r'<[^>]+>', '', t))


def checks(page):
    text = visible_text(page)
    i = text.find('—')
    need(i < 0, 'an em dash on the board: ' + text[max(0, i - 60):i + 20])
    if '–' in text:
        i = text.find('–')
        warn('an en dash on the board: ' + text[max(0, i - 40):i + 20])
    own = visible_text(re.sub(r'<(?:div class="tcols"|pre class="raw")>.*?</(?:div|pre)>(?=<div class="pending"|</section>)', ' ', page, flags=re.S))
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', own, flags=re.I)})
    if flagged:
        warn('flagged words in the board’s own words: ' + ', '.join(flagged))
    if 'answers to its people' in text and TAGLINE not in text:
        raise BoardError('the tagline is quoted inexactly (H01)')
    no_codes = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))
    no_codes = re.sub(r'<div class="tcols">.*', ' ', no_codes, flags=re.S)
    stray = set(re.findall(r'\b(?:DR|D2|D1|G1|DC|Q)-\d+\b|\b[IYSMT]\d{1,2}\b(?!\s*px)', visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))))
    if stray:
        warn('studio codes on the board’s face: ' + ', '.join(sorted(stray)))
    for pat in (r'/home/', r'file:', r'scratchpad', r'@anthropic'):
        if re.search(pat, re.sub(r'<pre class="raw".*?</pre>', '', page, flags=re.S)):
            warn(f'a private path on the board ({pat})')
    hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', page))
    extra = hosts - {'fonts.googleapis.com', 'fonts.gstatic.com'}
    if extra:
        warn('loads from hosts other than Google Fonts: ' + ', '.join(sorted(extra)))
    for v, u in re.findall(r'font-size:\s*(\d*\.?\d+)(px|rem)', strip_css(CSS)):
        if float(v) * (16 if u == 'rem' else 1) < 13:
            warn(f'a font size of {v}{u} in the board CSS, under 13 px')
    return text


def main():
    global LOG, CONTENT_DATA, RENDER, REUSE
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--no-render', action='store_true')
    ap.add_argument('--reuse-checks', action='store_true', help='reuse this session\'s pixel-fit and sprite check outputs')
    ap.add_argument('--out', type=pathlib.Path, default=OUT)
    a = ap.parse_args()
    C = json.loads(CONTENT.read_text())
    CONTENT_DATA = C
    RENDER = not a.no_render
    REUSE = a.reuse_checks
    need('—' not in CONTENT.read_text(), 'the content file holds an em dash (W21)')
    LOG = read_log()
    pal, ver = tokens()
    FILL['red_on_prussian'] = f'{contrast(pal["pillar-red"], pal["prussian"]):.2f}'
    FILL['white_on_prussian'] = f'{contrast(pal["white"], pal["prussian"]):.2f}'
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL['built_date'] = built.strftime('%B ') + str(built.day) + built.strftime(', %Y')
    FIG.update({'built': built.isoformat(), 'tokens_version': ver, 'contrast_figures': {k: FILL[k] for k in ('red_on_prussian', 'white_on_prussian')}})

    pf = run_pixel_fit(C)
    FIG['pixel_fit'] = pf
    sp = run_sprite()
    # craft first: it sets the counts the refinements' words name
    s_craft = craft_panel(C, pf, sp)
    s_ref = refinements_panel(C)
    s_sim = similarity_panel(C)
    s_app = approves_panel(C)
    s_con = slot_contrast(C)
    s_tok = slot_tokens(C)
    s_scr = slot_screens(C)
    s_sco = slot_scores(C)
    s_tes = slot_tested(C)
    s_wt = weight_panel(C)
    produce(render=not a.no_render)
    # images whose size is known only after the render: set it in the page
    sections = [s_app, s_ref, s_craft, s_sim, s_con, s_tok, s_scr, s_sco, s_tes, s_wt]
    page_body = '\n'.join(sections)
    for rec in ALL_IMAGES:
        if rec['spec'].get('element'):
            page_body = page_body.replace(f'src="{rec["src"]}" width="None" height="None"', f'src="{rec["src"]}" width="{rec["w"]}" height="{rec["h"]}"')
            page_body = page_body.replace('None by None px', f'{rec["w"]} by {rec["h"]} px')
    need('width="None"' not in page_body, 'an image has no size')
    page = build_page(C, cover(C, built) + '\n' + page_body)
    for leftover in re.findall(r'\{[a-z0-9_]+\}', visible_text(page)):
        warn(f'an unfilled field on the board: {leftover}')
    checks(page)
    need(len(page.encode()) < LIMIT, 'the board is over 16 MB')
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    files = [a.out] + sorted(IMG.glob('*.png'))
    total = sum(p.stat().st_size for p in files)
    FIG.update({'board': rel(a.out), 'html_bytes': len(page.encode()), 'images': len(files) - 1, 'folder_bytes_with_images': total,
                'status': {k: (v if isinstance(v, str) else list(v)) for k, v in STATUS.items()},
                'image_sources': {r['src']: r.get('source') for r in ALL_IMAGES}, 'codes_in_reference_lines': sorted(LINKED_CODES),
                'notes': NOTES, 'warnings': WARN, 'visible_text_sha1': hashlib.sha1(visible_text(page).encode()).hexdigest()})
    FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
    print(f'wrote {rel(a.out)} ({len(page.encode()) / 1e3:.0f} kB) and {len(files) - 1} images; {total / 1e6:.2f} MB in all')
    print('panels: ' + ', '.join(f'{k} {status_words(v)}' for k, v in STATUS.items()))
    print(f'{len(WARN)} warnings')
    if a.check:
        r = subprocess.run(['node', str(SCRIPTS / 'dataviz_check.js'), str(a.out), '--board', '--no-captures'], cwd=ROOT,
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        print(r.stdout.strip())
        if r.returncode != 0:
            sys.exit(1)
    if WARN and a.strict:
        sys.exit(1)


LOG = set()

if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
