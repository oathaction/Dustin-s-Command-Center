"""Build board 1 of Phase 3 (November 12, 2026; the board builder, working as the design director).

Usage:
    python3 -I work/build/scripts/phase-3/board_1_build.py [--strict] [--check] [--no-render] [--out PATH]

Reads, on every run:
    work/boards/phase-3/round-0/board-1/20261112_Board-1-Content.json   the board's own words and the files each panel reads
    a fresh strict build of the guide (guide_build.py --strict --out <scratch>), for chapter 13's plates, its first screen
    and the weights in its build report
    work/boards/phase-3/round-0/specimens/                              the kit's captures, exports and check files
    work/build/chart-kit/specs/                                         each chart's words
    Phase 2's Explainer and stretch pages, photographed figure by figure at 1440 and 390 px
    work/boards/phase-3/round-0/palettes/                               the palette proofs and their page
    the makers' notes, the reviews, the creative director's scores and rescores, the data plan and work/build/data/
    work/build/tokens/tokens.css and tokens.json                        the board's styles and the new colors
    work/ledger/*_Decision-Log.md and *_Open-Questions.md               every code in a reference line must exist
Writes:
    work/boards/phase-3/round-0/board-1/20261112_Board-1.html           the board (images by relative path, no scripts)
    work/boards/phase-3/round-0/board-1/img/                            every image it shows
    work/boards/phase-3/round-0/board-1/20261112_Board-1-Figures.json   every figure it prints, with its source
    <scratch>/ the guide build, the photographs, the composition cache and the check outputs

A part whose file is missing prints "Waiting for". --check runs dataviz_check.js on the board with --board --no-captures
and fails the build if it fails. --no-render reuses the photographs already in the scratch folder. --strict exits 1 on any
warning. An em dash stops the build.
"""
import argparse
import csv
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
DATE = '20261112'
BOARD_DIR = ROOT / 'work/boards/phase-3/round-0/board-1'
IMG = BOARD_DIR / 'img'
CONTENT = BOARD_DIR / f'{DATE}_Board-1-Content.json'
FIGURES = BOARD_DIR / f'{DATE}_Board-1-Figures.json'
OUT = BOARD_DIR / f'{DATE}_Board-1.html'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/board-1')
SCRIPTS2 = ROOT / 'work/build/scripts/phase-2'
SCRIPTS3 = ROOT / 'work/build/scripts/phase-3'
LABEL_FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
NEWSPRINT = (0xDC, 0xD9, 0xD2)
LABEL_INK = (0x4E, 0x53, 0x5B)
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat',
           'basically', 'very', 'incredibly', 'utilize', 'utilizes']
LIMIT_PAGE = 16_000_000
LIMIT_IMAGE = 15_000_000
LIMIT_FILES = 250
LIMIT_TOTAL = 64_000_000
PHOTO_DIR = None
WEIGHT_FILE = None
REGION_W = 248
WARN, NOTES, FIG, LINKED_CODES = [], [], {}, set()
QUOTED = []
FILL = {}
WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
CODE_DEC = r'(?:DR|D1|D2|D3|G1|G2|DC|Q)-\d+'
# review findings, requests and house-rule numbers that may sit in a teammate's parenthesis
CODE_REV = (r'(?:' + CODE_DEC + r'|P2-[MS]\d+|ENG-\d+|K[MS]\d+|K\d|CD [MS]\d+|CD-S\d|M\d|S\d{1,2}(?!\d)|P\d|Q\d|E\d{1,2}|R\d|X\d|H\d\d|C\d|W\d\d'
            r'|DT-M\d|[A-Z]-\d+|tension \d+)')
MOVED = set()


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


def nw(n, zero='no'):
    """A count in running prose: words under ten (H06), figures from ten."""
    n = int(n)
    return (zero if n == 0 else WORDS[n]) if 0 <= n < 10 else f'{n:,}'


def cap(s):
    return s[:1].upper() + s[1:]


def join_words(xs):
    xs = list(dict.fromkeys(xs))
    if not xs:
        return ''
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def words_when(ts):
    d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc) if isinstance(ts, (int, float)) else ts
    return d.strftime('%B ') + str(d.day) + d.strftime(', %Y')


def words_when_time(ts):
    d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    return words_when(d) + d.strftime(' at %H:%M UTC')


def mb(b, places=2):
    return f'{b / 1e6:.{places}f}'


def read(p):
    p = ROOT / p
    return p.read_text() if p.exists() else None


# ------------------------------------------------------------------------------------------------------- quoted words
def shorten_paths(s):
    s = re.sub(r'/tmp/claude-0/[^\s`)\]]*?/scratchpad/', '[scratch]/', str(s))
    s = s.replace(str(ROOT) + '/', '')
    s = re.sub(r'/home/user/[^\s`)\]]*', '[a workspace path]', s)
    return s.replace('file://', '')


def strip_codes(s):
    """A teammate's words keep their sentences; studio codes move to the panel's reference line."""
    s = shorten_paths(s)

    def move(m):
        MOVED.update(re.findall(CODE_DEC, m.group(0)))
        return ''
    # a parenthesis that holds only codes
    s = re.sub(r'\s*\((?:' + CODE_REV + r'(?:,\s*|\s+and\s+|;\s*|\s+to\s+|\s+)?)+\)', move, s)
    # "DR-98: a reading guide ..." at the start of a sentence
    s = re.sub(r'(^|(?<=[.;]\s))(?:' + CODE_REV + r'(?:,\s*|\s+and\s+)?)+:\s+(\w)', lambda m: (MOVED.update(re.findall(CODE_DEC, m.group(0))), m.group(1) + m.group(2).upper())[1], s)
    # "waits on E22", "since E7", "until R1 and R2 land"
    kinds = {'E': 'a kit change', 'R': 'a research answer', 'X': 'a spec change'}
    s = re.sub(r'\b(since|until|after|wait(?:s|ing)? (?:on|for))\s+([ERX])(?!0)\d{1,2}(?:\s+and\s+[ERX]\d{1,2})?\b',
               lambda m: f'{m.group(1)} {kinds[m.group(2)]}', s)

    def bare(m):
        MOVED.add(m.group(2))
        return m.group(1) + ' a logged decision'
    s = re.sub(r'\b(by|in|under|per)\s+(' + CODE_DEC + r')\b', bare, s)

    def poss(m):
        MOVED.add(m.group(2))
        return m.group(1) + ('The ' if not m.group(1).strip() or m.group(1).rstrip().endswith(('.', ';', ':')) else 'the ')
    s = re.sub(r'(^|[.;:]\s+|\s)(' + CODE_DEC + r'|ENG-\d+)(?:’|\')s\s+', poss, s)
    s = re.sub(r'\b(ready for|asks? for|needs?)\s+E(?!0)\d{1,2}\b', lambda m: m.group(1) + ' a kit change', s)

    # a code inside a parenthesis that also holds words: the code goes, the words stay
    def inner(m):
        body = m.group(1)
        MOVED.update(re.findall(CODE_DEC, body))
        kept = [x for x in re.split(r',\s*|;\s*', body) if not re.fullmatch(r'\s*' + CODE_REV + r'\s*', x)]
        return f'({", ".join(kept)})' if kept and len(kept) < len(re.split(r',\s*|;\s*', body)) else m.group(0)
    s = re.sub(r'\(([^()]*\b' + CODE_DEC + r'\b[^()]*)\)', inner, s)
    # runs of bare codes: "DR-44 to DR-72, DR-93 and DR-223", "ENG-5 to ENG-7"
    run = r'(?:' + CODE_DEC + r'|ENG-\d+)(?:(?:,\s*|\s+to\s+|,?\s+and\s+)(?:' + CODE_DEC + r'|ENG-\d+))*'

    def bare_run(m):
        codes = re.findall(CODE_DEC, m.group(0))
        MOVED.update(codes)
        eng = re.findall(r'ENG-\d+', m.group(0))
        many = len(codes) + len(eng) > 1
        if eng and not codes:
            return 'requests to the engineer' if many else 'a request to the engineer'
        return 'logged decisions' if many else 'a logged decision'
    s = re.sub(r'\b' + run + r'\b', bare_run, s)
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return s


def md_inline(s, quote=True):
    s = esc(strip_codes(s) if quote else s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', s)
    return s


def md_section(text, names, nth=0):
    """The lines under the nth heading whose words match one of names, to the next heading of the same or higher level."""
    if not text:
        return None
    lines = text.splitlines()
    found = 0
    for i, l in enumerate(lines):
        m = re.match(r'^(#+)\s*(.+?)\s*$', l)
        if m and any(re.fullmatch(n, m.group(2).strip(), flags=re.I) or re.fullmatch(n, re.sub(r'^\d+\.\s*', '', m.group(2).strip()), flags=re.I) for n in names):
            if found < nth:
                found += 1
                continue
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
        return [p.strip() for p in re.split(r'\n\s*\n', block) if p.strip() and not p.strip().startswith('|')]
    items, cur = [], None
    for l in (block or '').splitlines():
        m = re.match(r'^(\s*)(?:[-*]|\d+\.)\s+(.*)$', l)
        if m and len(m.group(1)) < 2:
            if cur is not None:
                items.append(cur)
            cur = m.group(2).strip()
        elif m and cur is not None:
            cur += ' ' + m.group(2).strip()
        elif cur is not None and l.strip() and l.startswith(' '):
            cur += ' ' + l.strip()
        elif cur is not None and not l.strip():
            items.append(cur)
            cur = None
    if cur is not None:
        items.append(cur)
    return items


def md_tables(block):
    """Every pipe table in a block: [(header, rows)]."""
    out, cur = [], []
    for l in (block or '').splitlines() + ['']:
        if l.strip().startswith('|'):
            cur.append(l.strip())
        elif cur:
            if len(cur) >= 2:
                cells = [[c.strip() for c in re.split(r'(?<!\\)\|', r.strip('|'))] for r in cur]
                body = [r for r in cells[1:] if not all(re.fullmatch(r':?-{2,}:?', c) for c in r if c)]
                out.append((cells[0], body))
            cur = []
    return out


def md_html(block, quote=True):
    """A small Markdown renderer for quoted sections: paragraphs, lists, tables and subheads."""
    if not block:
        return ''
    parts, lines, i = [], block.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
            continue
        if l.strip().startswith('|'):
            j = i
            while j < len(lines) and lines[j].strip().startswith('|'):
                j += 1
            for head, rows in md_tables('\n'.join(lines[i:j])):
                parts.append(table_html(head, rows, quote=quote))
            i = j
            continue
        m = re.match(r'^(#+)\s+(.*)$', l)
        if m:
            parts.append(f'<p class="qh">{md_inline(m.group(2), quote)}</p>')
            i += 1
            continue
        if re.match(r'^\s*(?:[-*]|\d+\.)\s+', l):
            j = i
            while j < len(lines) and (re.match(r'^\s*(?:[-*]|\d+\.)\s+', lines[j]) or (lines[j].startswith('  ') and lines[j].strip())):
                j += 1
            items = md_items('\n'.join(lines[i:j]))
            tag = 'ol' if re.match(r'^\s*\d+\.', l) else 'ul'
            parts.append(f'<{tag}>' + ''.join(f'<li>{md_inline(x, quote)}</li>' for x in items) + f'</{tag}>')
            i = j
            continue
        if l.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            parts.append(f'<pre class="raw">{esc(shorten_paths(chr(10).join(lines[i + 1:j])))}</pre>')
            i = j + 1
            continue
        j = i
        para = []
        while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith('|') and not re.match(r'^(#+\s|\s*(?:[-*]|\d+\.)\s+|```)', lines[j]):
            para.append(lines[j].strip())
            j += 1
        parts.append(f'<p>{md_inline(" ".join(para), quote)}</p>')
        i = j
    return ''.join(parts)


def table_html(head, rows, quote=True, caption=None, cls=''):
    hd = ''.join(f'<th scope="col">{md_inline(c, quote)}</th>' for c in head)
    body = ''.join('<tr>' + ''.join((f'<th scope="row">{md_inline(c, quote)}</th>' if k == 0 else f'<td>{md_inline(c, quote)}</td>') for k, c in enumerate(r)) + '</tr>' for r in rows)
    cp = f'<caption>{esc(caption)}</caption>' if caption else ''
    name = caption or (re.sub(r'<[^>]+>', '', head[0]) if head else 'Table')
    return (f'<div class="tw" role="region" tabindex="0" aria-label="{esc(name)}; scrolls sideways"><table class="{cls}">{cp}'
            f'<thead><tr>{hd}</tr></thead><tbody>{body}</tbody></table></div>')


def tested_lists(text):
    """Every Tested and Not tested list in a notes file, with the part of the file it sits in: headings at any level
    whose words end in "tested" ("Fix pass 2 tested", "Tested (Part 2)", "5. Tested"), lines such as "Tested:" over a
    list, run-in paragraphs such as "Tested in fix pass 2: ...", and bold-led paragraphs such as "**Tested.** ...".
    Returns [(kind, where, item)] in file order, kind 'tested' or 'not'."""
    out = []
    lines = text.splitlines()
    heads = []
    part = ''
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^(#+)\s*(.+?)\s*$', l)
        if m:
            lvl, name = len(m.group(1)), re.sub(r'^\d+\.\s*', '', m.group(2).strip())
            heads = [h for h in heads if h[0] < lvl] + [(lvl, name)]
            low = name.lower()
            kind = 'not' if re.search(r'\bnot tested\b', low) else ('tested' if re.search(r'(^|\s)tested\b', low) and 'untested' not in low else None)
            if kind:
                body = []
                for l2 in lines[i + 1:]:
                    m2 = re.match(r'^(#+)\s', l2)
                    if m2 and len(m2.group(1)) <= lvl:
                        break
                    body.append(l2)
                own_name = re.sub(r'(?i)\b(not )?tested\b', '', name).strip(' ()·,')
                trail = [h[1] for h in heads[:-1] if h[0] > 1] + ([own_name] if own_name else [])
                where = ' · '.join(x for k, x in enumerate(trail) if k == 0 or x != trail[k - 1])
                blk = '\n'.join(body)
                if kind == 'tested' and re.search(r'^(?:\*\*)?not tested\b', blk, flags=re.I | re.M):
                    a, b = re.split(r'^(?:\*\*)?not tested\b.*$', blk, flags=re.I | re.M, maxsplit=1)
                    out += [('tested', where, x) for x in md_items(a)] + [('not', where, x) for x in md_items(b)]
                else:
                    out += [(kind, where, x) for x in md_items(blk)]
            i += 1
            continue
        # "Tested:" or "Not tested:" alone on a line over a list
        m = re.match(r'^(Not tested|Tested)(?: [^:]{0,60})?:\s*$', l.strip())
        if m:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            k = j
            while k < len(lines) and (re.match(r'^\s*[-*]\s+', lines[k]) or (lines[k].startswith('  ') and lines[k].strip())):
                k += 1
            where = ' · '.join(h[1] for h in heads if h[0] > 1)
            out += [('not' if m.group(1) == 'Not tested' else 'tested', where, x) for x in md_items('\n'.join(lines[j:k]))]
            i = k
            continue
        # "Tested in the fix pass: a; b. Not tested: c; d."
        m = re.match(r'^(Tested|Not tested)\b[^:]{0,60}:\s+(.+)$', l.strip())
        if m:
            where = ' · '.join(h[1] for h in heads if h[0] > 1)
            t = m.group(2)
            if m.group(1) == 'Tested' and ' Not tested: ' in t:
                a, b = t.split(' Not tested: ', 1)
                out += [('tested', where, a.strip()), ('not', where, b.strip())]
            else:
                out.append(('not' if m.group(1) == 'Not tested' else 'tested', where, t.strip()))
            i += 1
            continue
        m = re.match(r'^\*\*(Not tested|Tested)\.\*\*\s*(.+)$', l.strip())
        if m:
            where = ' · '.join(h[1] for h in heads if h[0] > 1)
            out.append(('not' if m.group(1) == 'Not tested' else 'tested', where, m.group(2).strip()))
        i += 1
    seen, res = set(), []
    for k, w, x in out:
        if x and (k, x) not in seen and not x.startswith('(pending'):
            seen.add((k, x))
            res.append((k, w, x))
    return res


# ------------------------------------------------------------------------------------------------------- sources
def read_log():
    codes = set()
    for p in glob.glob(str(ROOT / 'work/ledger/*_Decision-Log.md')) + glob.glob(str(ROOT / 'work/ledger/*_Open-Questions.md')):
        t = pathlib.Path(p).read_text()
        codes |= set(re.findall(r'^\|\s*((?:DR|D3|D2|D1|G1|G2|DC|Q)-\d+)\s*\|', t, flags=re.M))
        codes |= set(re.findall(r'^#+\s*((?:Q)-\d+)\b', t, flags=re.M))
    return codes


def check_refs(refs, where):
    for c in re.findall(r'\b' + CODE_DEC + r'\b', refs):
        LINKED_CODES.add(c)
        if c not in LOG:
            warn(f'{c} in the reference line of {where} is not in the decision log or the open questions')


def refline(refs, where):
    check_refs(refs, where)
    return f'<p class="codes">Reference: {esc(refs)}</p>'


def css_tokens():
    """Every custom property tokens.css defines first, resolved to a literal value."""
    t = (ROOT / C['slots']['tokens_css']).read_text()
    raw = {}
    for name, val in re.findall(r'(--oa-[a-z0-9-]+):\s*([^;]+);', t):
        raw.setdefault(name, val.strip())

    def res(v, depth=0):
        m = re.fullmatch(r'var\((--oa-[a-z0-9-]+)\)', v)
        return res(raw.get(m.group(1), v), depth + 1) if m and depth < 12 else v
    return {k: res(v) for k, v in raw.items()}, raw


def contrast(a, b):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


# ------------------------------------------------------------------------------------------------------- images
IMAGES = {}      # name -> record
CACHE_FILE = SCRATCH / 'compose-cache.json'
CACHE = {}


def file_sig(p):
    st = pathlib.Path(p).stat()
    return f'{st.st_size}-{int(st.st_mtime)}'


def image_size(p):
    if pathlib.Path(p).suffix.lower() == '.png':
        return png_size(p)
    from PIL import Image
    with Image.open(p) as im:
        return im.size


IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp')


def image_copy(src, name):
    src = pathlib.Path(src)
    need(src.exists(), f'missing image {rel(src)}')
    ext = src.suffix.lower() if src.suffix.lower() in IMG_EXT else '.png'
    out = IMG / f'{DATE}_{name}{ext}'
    if not out.exists() or out.stat().st_size != src.stat().st_size or out.read_bytes() != src.read_bytes():
        shutil.copyfile(src, out)
    w, h = image_size(out)
    rec = {'src': f'img/{out.name}', 'file': out, 'w': w, 'h': h, 'source': rel(src)}
    IMAGES[out.name] = rec
    return rec


def image_compose(name, parts, cols=None, gap=24, label_h=26):
    """One picture of several, each part at its true size on whole pixels with its label set in Inter above it.
    parts: [(path, label)]. Grayscale parts stay one gray channel when every part is gray."""
    from PIL import Image, ImageDraw, ImageFont
    out = IMG / f'{DATE}_{name}.png'
    for p, _ in parts:
        need(pathlib.Path(p).exists(), f'missing picture {rel(p)} for {name}')
    sig = hashlib.sha1(json.dumps([[str(p), file_sig(p), l] for p, l in parts] + [cols, gap, label_h, 3]).encode()).hexdigest()
    if out.exists() and CACHE.get(out.name) == sig:
        w, h = png_size(out)
    else:
        ims = [Image.open(p) for p, _ in parts]
        gray = all(im.mode == 'L' for im in ims)
        mode = 'L' if gray else 'RGB'
        bg = round(0.2126 * NEWSPRINT[0] + 0.7152 * NEWSPRINT[1] + 0.0722 * NEWSPRINT[2]) if gray else NEWSPRINT
        ink = round(0.2126 * LABEL_INK[0] + 0.7152 * LABEL_INK[1] + 0.0722 * LABEL_INK[2]) if gray else LABEL_INK
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
        canvas.save(out, 'PNG', optimize=False, compress_level=9)
        CACHE[out.name] = sig
        w, h = W, H
    rec = {'src': f'img/{out.name}', 'file': out, 'w': w, 'h': h, 'source': 'composed from ' + ', '.join(rel(p) for p, _ in parts)}
    IMAGES[out.name] = rec
    return rec


def frame(rec, alt, lazy=True, cls=''):
    w, h = rec['w'], rec['h']
    region = w > REGION_W
    attrs = f' role="region" tabindex="0" aria-label="{esc(alt)}, {w} by {h} px; scrolls sideways"' if region else ''
    ld = ' loading="lazy"' if lazy else ''
    return (f'<div class="frame{" wide" if region else ""} {cls}"{attrs}><img src="{rec["src"]}" width="{w}" height="{h}" '
            f'alt="{esc(alt)}"{ld} decoding="async"></div>')


def figure(rec, alt, cap, lazy=True):
    return f'<figure class="shot">{frame(rec, alt, lazy)}<figcaption>{cap}</figcaption></figure>'


# ------------------------------------------------------------------------------------------------------- renders
def run_renders(jobs, render):
    """Photograph what the board shows from live pages, into the scratch folder."""
    todo = [j for j in jobs if render or not all(pathlib.Path(it['out']).exists() for it in j['items'])]
    if not todo:
        return
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jp = SCRATCH / 'render-jobs.json'
    jp.write_text(json.dumps(todo))
    r = subprocess.run(['node', str(SCRIPTS3 / 'board_1_render.js'), str(jp)], cwd=ROOT / 'work/build',
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    bad = [l for l in r.stdout.splitlines() if l.startswith('failed')]
    for b in bad:
        warn('render ' + b)
    if r.returncode != 0 and not bad:
        warn('the renderer stopped: ' + r.stderr[-300:])


def guide_build():
    d = SCRATCH / 'guide'
    d.mkdir(parents=True, exist_ok=True)
    page = d / f'{DATE}_Board-1-Guide.html'
    r = subprocess.run([sys.executable, '-I', str(ROOT / C['slots']['guide_build']), '--strict', '--out', str(page)], cwd=ROOT,
                       capture_output=True, text=True)
    (SCRATCH / 'guide-build.log').write_text(r.stdout + r.stderr)
    rep = d / f'{DATE}_Board-1-Guide-Build-Report.json'
    if not rep.exists():
        cand = sorted(d.glob('*Build-Report.json'), key=lambda p: p.stat().st_mtime)
        rep = cand[-1] if cand else rep
    ok = r.returncode == 0 and page.exists() and rep.exists()
    if not ok:
        warn(f'the strict guide build failed (exit {r.returncode}); chapter 13 waits for a passing build')
    report = json.loads(rep.read_text()) if rep.exists() else {}
    FIG['guide_build'] = {'exit': r.returncode, 'page_bytes': report.get('bytes'), 'warnings': len(report.get('warnings', [])),
                          'built': report.get('built'), 'report': str(rep)}
    return {'ok': ok, 'page': page, 'report': report, 'mtime': page.stat().st_mtime if page.exists() else None}


SPEC_IDS = [f'S{i:02d}' for i in range(1, 17)]


def render_jobs(G):
    S = C['slots']
    jobs = []
    p2 = {'explainer': [i for i in SPEC_IDS if i not in S['phase2']['stretch_ids']], 'stretch': S['phase2']['stretch_ids']}
    for page, ids in p2.items():
        for w, h in ((1440, 900), (390, 844)):
            jobs.append({'file': str(ROOT / S['phase2'][page]), 'hash': '#newsprint', 'width': w, 'height': h, 'static_sticky': False,
                         'items': [{'selector': f'#newsprint-{i.lower()}-fig', 'out': str(SCRATCH / 'phase-2' / f'{i}-{w}.png')} for i in ids]})
    jobs.append({'file': str(ROOT / S['palette_page']), 'hash': '', 'width': 1440, 'height': 900, 'static_sticky': False,
                 'items': [{'selector': f'#{x}', 'out': str(SCRATCH / 'palette' / f'{x}.png')} for x in
                           ('diverging-charcoal', 'div-charcoal', 'categorical-newsprint', 'categorical-charcoal', 'cat-newsprint', 'cat-charcoal')]})
    if G['ok']:
        ch = json.loads((ROOT / S['chapter13']).read_text())
        plates = ['s-13-opener'] + [ch_r[k]['specimen'] for ch_r in ch['rules'] for k in ('correct', 'failure')]
        jobs.append({'file': str(G['page']), 'hash': '', 'width': 1440, 'height': 900, 'static_sticky': True, 'prime': '#' + ch['anchor'],
                     'items': [{'selector': f'#fig-{p}', 'out': str(SCRATCH / 'plates' / f'{p}.png')} for p in plates]})
        for w, h in ((1440, 900), (390, 844)):
            jobs.append({'file': str(G['page']), 'hash': '', 'width': w, 'height': h, 'static_sticky': False,
                         'items': [{'anchor': '#' + ch['anchor'], 'out': str(SCRATCH / 'plates' / f'first-screen-{w}.png')}]})
    return jobs


# ------------------------------------------------------------------------------------------------------- engineer's numbers
def engineer_numbers():
    """The weight options as the engineer's script measured them (D3-187), the combined option once it is in, and the
    sections of the engineer's notes the board quotes."""
    S = C['slots']
    t = read(S['engineer_notes']) or ''
    out = {'found': False, 'combined': None, 'base': {}}
    globs = [g if g.startswith('/') else str(ROOT / g) for g in S['weight_options_globs']]
    cands = [str(WEIGHT_FILE)] if WEIGHT_FILE else sorted({f for g in globs for f in glob.glob(g)}, key=os.path.getmtime)
    if cands:
        J = json.loads(pathlib.Path(cands[-1]).read_text())
        opts = J.get('options', [])
        comb = next((o for o in opts if re.search(r'combin|recommend', o['option'], re.I)
                     or (re.search(r'photo', o['option'], re.I) and re.search(r'compress|data', o['option'], re.I))), None)
        if comb is None and len(opts) > 4:
            comb = opts[4]
        for key, pat in (('stands', r'as it stands'), ('islands', r'chart data'), ('tables', r'tables'), ('photos', r'photo')):
            o = next((o for o in opts if o is not comb and re.search(pat, o['option'], re.I)), None)
            if o:
                out['base'][key] = o
        out.update({'J': J, 'file': cands[-1], 'combined': comb, 'found': len(out['base']) == 4})
        ph = out['base'].get('photos', {}).get('reader_loses', '')
        m = re.search(r'\((\d+) on the page', ph)
        out['n_photos'] = int(m.group(1)) if m else None
        m = re.search(r'at ([\d,]+) px wide', ph)
        out['photo_w'] = m.group(1) if m else None
    m = re.search(r"Phase 4['’]s ([\d.]+) MB", md_section(t, [r'board 1 weight options']) or t)
    out['phase4_share'] = float(m.group(1)) if m else None
    m = re.search(r'at most (\d+) px wide', t)
    out['shown_w'] = m.group(1) if m else None
    bw = md_section(t, [r'board 1 weight options']) or ''
    tabs = [x for x in md_tables(bw) if x[0] and x[0][0].lower() == 'option']
    out['table'] = tabs[0] if tabs else None
    pil = md_section(t, [r'the drawing method \(pilot\)']) or ''
    out['pilot_tables'] = md_tables(pil)
    out['sections'] = {n: md_section(t, [re.escape(n)]) for n in ('The drawing method (pilot)', 'The weight gates', 'Weight pass', 'Board 1 weight options')}
    if not out['found']:
        warn('the engineer’s weight options JSON was not found or lacks one of its four options')
    if not out['combined']:
        note('the combined weight option is not in the engineer’s JSON yet')
    FIG['engineer_options'] = {'file': out.get('file'), 'options': out.get('J', {}).get('options'), 'combined': out['combined'],
                               'phase4_share': out['phase4_share']}
    return out


def photo_proof(it):
    """The engineer's proof of the smaller photographs, read from its manifest: for each photograph, the picture of the
    current file beside its rendition at the page's display width, and the same at twice the pixels, with bytes."""
    d = PHOTO_DIR or pathlib.Path(C['slots']['photo_proof_dir'])
    mans = sorted((m for m in d.glob('*.json') if 'Weight-Options' not in m.name), key=os.path.getmtime) if d.exists() else []
    if not mans:
        return None
    M = json.loads(mans[-1].read_text())
    out, n_shown = [], 0
    for e in M.get('photos', []):
        name = e.get('photo', '')
        x1 = sorted(d.glob(f'*{name}-1x.png'))
        x2 = sorted(d.glob(f'*{name}-2x.png'))
        if not (x1 and x2):
            warn(f'the photo proof for {name} lacks its 1x or 2x picture')
            continue
        rec = {}
        rp = ROOT / e.get('file', '')
        if rp.suffix and rp.with_suffix('.json').exists():
            rec = json.loads(rp.with_suffix('.json').read_text())
        cur, ren = e['current'], e['rendition']
        times = e.get('times_on_page', 1)
        n_shown += times
        head = fill(it['proof_photo_h'], {'rule': rec.get('for_rule', name), 'agency': rec.get('agency', ''), 'times': {1: 'once', 2: 'twice'}.get(times, f'{times} times')})
        facts = [(it['proof_facts'][0], f'{cur["pixels"][0]:,} by {cur["pixels"][1]:,} px, {cur["bytes"]:,} bytes'),
                 (fill(it['proof_facts'][1]), f'{ren["pixels"][0]:,} by {ren["pixels"][1]:,} px, {ren["bytes"]:,} bytes'),
                 (it['proof_facts'][2], f'{e.get("page_bytes_saved", 0):,} bytes')]
        r1 = image_copy(x1[-1], slug('Photo-Proof', name, '1x'))
        r2 = image_copy(x2[-1], slug('Photo-Proof', name, '2x'))
        out.append(f'<h5 class="ph-h">{esc(head)}</h5><dl class="facts kf3">' + ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in facts) + '</dl>'
                   + figure(r1, f'{head}: the current file and the {FILL.get("photo_w", "")} px copy at the page’s display width', esc(it['proof_cap_1x']))
                   + figure(r2, f'{head}: the same at twice the pixels', esc(it['proof_cap_2x'])))
    tot = M.get('page_bytes_saved_total')
    if tot is not None and FILL.get('photo_saving') and abs(tot / 1e6 - float(FILL['photo_saving'])) > 0.0005:
        warn(f'the photo proof frees {tot:,} bytes and the weight options {FILL["photo_saving"]} MB')
    FIG['photo_proof'] = {'manifest': str(mans[-1]), 'photos': [e.get('photo') for e in M.get('photos', [])], 'saved': tot, 'shown': n_shown}
    return ''.join(out) or None


# ------------------------------------------------------------------------------------------------------- panel 1
def palette_facts(TOK):
    tj = json.loads((ROOT / C['slots']['tokens_json']).read_text())
    tints = tj['oa']['color']['tint']
    new = [(k, v['$value']['hex']) for k, v in tints.items() if isinstance(v, dict) and 'Proposed' in v.get('$description', '')]
    if len(new) != 2:
        warn(f'tokens.json marks {len(new)} tints as proposed, not two')
    new.sort(key=lambda kv: -int(re.sub(r'\D', '', kv[0]) or 0))
    ch = TOK['--oa-color-palette-charcoal']
    names = {v.upper(): k.replace('--oa-color-palette-', '') for k, v in TOK.items() if k.startswith('--oa-color-palette-')}
    order = []
    for g in range(1, 5):
        v = TOK.get(f'--oa-chart-color-categorical-fill-group{g}-on-newsprint', '')
        order.append(cap(names.get(v.upper(), v)))
    FILL.update({'n56': new[0][1] if new else '?', 'n29': new[1][1] if len(new) > 1 else '?',
                 'r56': f'{contrast(new[0][1], ch):.2f}' if new else '?', 'r29': f'{contrast(new[1][1], ch):.2f}' if len(new) > 1 else '?',
                 'cat_order': join_words(order)})
    FIG['palette'] = {'new_tints': new, 'contrast_on_charcoal': [FILL['r56'], FILL['r29']], 'categorical_order': order,
                      'release': re.search(r'"version":\s*"([^"]+)"', (ROOT / C['slots']['tokens_json']).read_text()).group(1)}
    return new, order


def cd_scores():
    p = ROOT / C['slots']['cd_scores']
    first = json.loads(p.read_text()) if p.exists() else None
    rs = sorted(glob.glob(str(ROOT / C['slots']['cd_rescores_glob'])), key=os.path.getmtime)
    re_ = json.loads(pathlib.Path(rs[-1]).read_text()) if rs else None
    FIG['cd'] = {'first': rel(p) if first else None, 'rescore': rel(rs[-1]) if rs else None}
    return first, re_


def score_words(item, crit):
    return ', '.join(f'{c["name"].lower()} {item["scores"].get(c["key"], "?")}' for c in crit)


def decide_panel(G, E, TOK):
    P = C['panels']['decide']
    new, order = palette_facts(TOK)
    ch = json.loads((ROOT / C['slots']['chapter13']).read_text())
    rep = G['report'].get('weight', {})
    c13 = rep.get('chapters', {}).get('13', {})
    FILL.update({'n_rules': len(ch['rules']), 'ch13_bytes': f'{c13.get("bytes", 0):,}', 'ch13_budget': f'{int(c13.get("budget", 0)):,}',
                 'build_warnings': nw(len(G['report'].get('warnings', [])), 'no')})
    proj = rep.get('projection', {})
    unbuilt = proj.get('unbuilt', {})
    stop = unbuilt.get('14')
    FILL['stop'] = f'{stop / 1e6:.2f}' if stop else '?'
    if E['found']:
        B, J = E['base'], E['J']
        FILL.update({'ch14_now': f'{J["chapter_14_now"] / 1e6:.3f}', 'ask_stands': f'{B["stands"]["ask_of_phase_4"] / 1e6:.3f}',
                     'ask_islands': f'{B["islands"]["ask_of_phase_4"] / 1e6:.3f}', 'phase4_share': f'{E["phase4_share"]:.2f}',
                     'photo_saving': f'{J["photo_saving"] / 1e6:.3f}', 'n_photos_w': nw(E['n_photos'] or 0), 'photo_w': E['photo_w'] or '?',
                     'shown_w': E['shown_w'] or '?', 'budget_mb': f'{proj.get("budget", 0) / 1e6:.1f}'})
        comb = E['combined']
        R = J.get('recommended') if isinstance(J.get('recommended'), dict) else {}
        if comb and R:
            if R.get('chapter_14_stop') not in (None, comb['chapter_14']):
                warn('the recommended stop and the combined option’s chapter 14 differ in the weight options file')
            if R.get('phase_4_share_untouched') is False or comb.get('ask_of_phase_4'):
                warn('the recommended option takes bytes from Phase 4')
        if comb:
            room = R.get('room_left') if isinstance(R.get('room_left'), (int, float)) else None
            room = room if room is not None else next((comb[k] for k in ('room_after', 'page_room_after', 'room') if isinstance(comb.get(k), (int, float))), None)
            if room is None:
                m = re.search(r'keeps ([\d.]+) MB of room', comb.get('reader_loses', ''))
                room = float(m.group(1)) * 1e6 if m else None
            FILL['comb_room_computed'] = room is None
            if room is None:     # the page's room once the stop rises to the measured figure and the photographs free their bytes
                room = J['room'] - max(0, comb['chapter_14'] - J['stop']) + J['photo_saving']
            FILL.update({'comb_ch14': f'{R.get("chapter_14_stop", comb["chapter_14"]) / 1e6:.3f}', 'comb_room': f'{room / 1e6:.3f}'})
    # Phase 4's chapters: the unbuilt chapters that share one allocation
    alloc = {}
    for k, v in unbuilt.items():
        if k not in ('14', '15'):
            alloc.setdefault(v, []).append(k)
    p4 = max(alloc.values(), key=len) if alloc else []
    each = unbuilt.get(p4[0]) if p4 else None
    if p4 and E.get('phase4_share') and E['found']:
        if abs(len(p4) * each / 1e6 - E['phase4_share']) > 0.01:
            warn(f'Phase 4’s chapters in the build report ({len(p4)} at {each:,}) do not add to the notes’ {E["phase4_share"]} MB')
        FILL.update({'phase4_n': nw(len(p4)), 'phase4_each': f'{each / 1e6:.2f}',
                     'phase4_after_1': f'{(E["phase4_share"] - B["stands"]["ask_of_phase_4"] / 1e6) / len(p4):.2f}',
                     'phase4_after_2': f'{(E["phase4_share"] - B["islands"]["ask_of_phase_4"] / 1e6) / len(p4):.2f}'})
    PROOF['html'] = photo_proof(next(i for i in P['items'] if i['key'] == 'weight'))
    first, rescore = cd_scores()
    cards = []
    for it in P['items']:
        body = ''
        if it['key'] == 'palette':
            r1 = image_copy(SCRATCH / 'palette/diverging-charcoal.png', 'Decide-Diverging-On-Charcoal-Steps')
            r2 = image_copy(SCRATCH / 'palette/div-charcoal.png', 'Decide-Diverging-On-Charcoal-Table')
            r3 = image_copy(SCRATCH / 'palette/categorical-newsprint.png', 'Decide-Four-Inks-On-Newsprint')
            r4 = image_copy(SCRATCH / 'palette/categorical-charcoal.png', 'Decide-Four-Inks-On-Charcoal')
            r5 = image_compose('Decide-Four-Inks-In-Charts', [(SCRATCH / 'palette/cat-newsprint.png', 'On Newsprint'), (SCRATCH / 'palette/cat-charcoal.png', 'On Charcoal')], gap=16)
            body = (f'<h4 class="dec-sub">{esc(it["show_h"])}</h4>'
                    + figure(r1, f'Diverging pair B on Charcoal: five steps with their measures, the two new colors {FILL["n56"]} and {FILL["n29"]} as steps 1 and 2', 'The five steps on Charcoal, from the palette proof sheet. Steps 1 and 2 are the new colors.', lazy=False)
                    + figure(r2, 'A table of job change by industry drawn in diverging pair B on Charcoal', 'The same steps in a table on real data, from the proof sheet.')
                    + f'<h4 class="dec-sub">{esc(it["show_cat_h"])}</h4>'
                    + figure(r3, f'The four inks on Newsprint in their order, {FILL["cat_order"]}, with their measures', 'On Newsprint.')
                    + figure(r4, 'The four inks on Charcoal in their order, with their measures', 'On Charcoal, where Prussian lifts toward Newsprint so it reads on the dark ground.')
                    + figure(r5, 'Four job sectors on a line chart and in one bar, on Newsprint and on Charcoal', 'The four inks in use, each group named on the chart.'))
        elif it['key'] == 'ch13':
            if first:
                fi = next((i for i in first['items'] if i['key'] == 'ch13'), None)
                if fi:
                    body += f'<p class="small">{esc(fill(P["cd_line_first"], {"scores": score_words(fi, first["criteria"])}))}'
                    ri = next((i for i in (rescore or {}).get('items', []) if i['key'] == 'ch13'), None)
                    body += (f' {esc(fill(P["cd_line_re"], {"scores": score_words(ri, rescore["criteria"]), "ready": "ready" if ri.get("ready") else "not yet ready"}))}' if ri
                             else f' {esc(P["cd_line_wait"])}') + '</p>'
        elif it['key'] == 'weight' and E['found']:
            body += weight_body(it, E, P)
        elif it['key'] == 'payroll':
            body += payroll_body(it)
        q = fill(it['q'])
        rec = fill(it['rec_wait'] if it['key'] == 'weight' and not E.get('combined') and it.get('rec_wait') else it['rec'])
        cards.append(f'<article class="dec" id="decide-{esc(it["key"])}"><h3 class="dec-h">{esc(it["h"])}</h3><p class="dec-q">{esc(q)}</p>'
                     f'<p class="dec-rec"><span class="tag rec">Recommended</span> {esc(rec)}</p>{body}{refline(it["refs"], "decision " + it["key"])}</article>')
    body = f'<p class="intro">{esc(P["lede"])}</p><p class="reply">{esc(P["reply"])}</p>' + ''.join(cards)
    ok = E['found'] and E['combined'] and PROOF.get('html')
    return panel('decide', P, body, 'ready' if ok else ('partial', 'engineer'))


PROOF = {}


def weight_body(it, E, P):
    B, J, comb = E['base'], E['J'], E['combined']
    out = ''
    if comb:
        facts = [(it['comb_facts'][0], f'{comb["chapter_14"] / 1e6:.3f} MB'),
                 (it['comb_facts'][1], 'None' if not comb.get('ask_of_phase_4') else f'{comb["ask_of_phase_4"] / 1e6:.3f} MB'),
                 (it['comb_facts'][2], f'{J["photo_saving"] / 1e6:.3f} MB'),
                 (it['comb_facts'][3], f'{FILL["comb_room"]} MB'),
                 (it['comb_facts'][4], strip_codes(comb.get('reader_loses', '')))]
        QUOTED.append(comb.get('reader_loses', ''))
        out += (f'<h4 class="dec-sub">{esc(it["comb_h"])}</h4><dl class="facts">' + ''.join(f'<div><dt>{esc(fill(a))}</dt><dd>{esc(b)}</dd></div>' for a, b in facts) + '</dl>'
                + (f'<p class="small">{esc(it["comb_room_note"])}</p>' if FILL.get('comb_room_computed') else ''))
    else:
        out += f'<div class="pending" role="status"><p><b>Waiting for the engineer.</b> {esc(it["comb_wait"])}</p></div>'
    out += f'<h4 class="dec-sub">{esc(fill(it["proof_h"]))}</h4><p class="small">{esc(fill(it["proof_lede"]))}</p>'
    out += PROOF.get('html') or f'<div class="pending" role="status"><p><b>Waiting for the engineer.</b> {esc(it["proof_wait"])}</p></div>'
    out += f'<p class="dec-rec approve">{esc(fill(it["approve"]))}</p>'
    rows = []
    for k, o in zip(('stands', 'islands', 'tables', 'photos'), it['options']):
        x = B[k]
        ask_w = 'None' if not x['ask_of_phase_4'] else f'{x["ask_of_phase_4"] / 1e6:.3f} MB'
        pr_w = f'{x["chapter_14"] / 1e6:.3f} MB' + (f'; frees {J["photo_saving"] / 1e6:.3f} MB of the page' if k == 'photos' else '')
        rows.append(f'<tr><th scope="row">{esc(o["name"])}</th><td class="num">{ask_w}</td><td class="num">{pr_w}</td><td>{esc(o["sees"])}</td></tr>')
    hd = ''.join(f'<th scope="col">{esc(fill(c))}</th>' for c in it['cols'])
    out += (f'<h4 class="dec-sub">{esc(it["options_h"])}</h4><div class="tw" role="region" tabindex="0" aria-label="{esc(it["options_h"])}; scrolls sideways">'
            f'<table class="opts"><thead><tr>{hd}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="small">{esc(fill(it["phase4_line"]))}</p>')
    adv = cd_advice()
    if adv:
        QUOTED.append(adv)
        out += f'<h4 class="dec-sub">{esc(it["cd_h"])}</h4><blockquote class="q">{md_html(adv)}<footer>{esc(P["cd_cite"])}</footer></blockquote>'
    return out



def cd_advice():
    """The creative director's weight advice: the rescore's, where it gives one, else part 2's advice on tables."""
    t = read(C['slots']['cd_review']) or ''
    sec = md_section(t, [r'rescore: the chart kit.*']) or ''
    m = re.search(r'(\*\*Weight:.*?)(?=\n\n(?!\d+\.)[A-Z*#]|\Z)', sec, flags=re.S)
    if m:
        return m.group(1).strip()
    sec = md_section(t, [r'the weight and what to ask dustin']) or ''
    for x in md_items(sec):
        if re.search(r'compress', x, flags=re.I) and re.search(r'table', x, flags=re.I):
            return x
    warn('the creative director’s weight advice was not found')
    return None


def payroll_body(it):
    S = C['slots']
    spec = json.loads((ROOT / S['payroll_spec']).read_text())
    m = re.search(r'(shrank in (\w+) of the (\d+) months charted)', spec['title'])
    need(m, 'S14’s title no longer carries the approved count')
    approved, n_word, n_months = m.group(1), m.group(2), int(m.group(3))
    ch02 = read(S['ch02_plate']) or ''
    if approved not in ch02:
        warn('chapter 02’s plate no longer prints the approved payroll words')
    rows = list(csv.DictReader(open(ROOT / S['payroll_file'])))
    if len(rows) != n_months:
        warn(f'the payroll file holds {len(rows)} months, the sentence says {n_months}')
    drops = [r for r in rows if float(r['change_thousands']) < 0]
    if WORDS[len(drops)] != n_word if len(drops) < 10 else True:
        warn(f'the payroll file has {len(drops)} drops; the approved words say {n_word}')
    rn = read(S['research_notes']) or ''
    mi = re.search(r'plus or minus ([\d,]+)', rn)
    need(mi, 'the research notes no longer give the payroll interval')
    interval = int(mi.group(1).replace(',', ''))
    mt = re.search(r'Technical Note on bls\.gov \(the (\w+ \d{4}) release, "Last Modified Date: ([A-Za-z]+ \d{1,2}, \d{4})"\)', rn)
    ml = re.search(r'Ledger row (P7-\d+[a-z]?)\.', md_section(rn, [r'fix pass']) or '')

    def month(s):
        d = datetime.date(int(s[:4]), int(s[5:7]), 1)
        return d.strftime('%B %Y')
    passing = [month(r['month']) for r in drops if abs(float(r['change_thousands'])) * 1000 > interval]
    added = f'Only the {join_words(passing)} drops pass the survey’s margin of error.'
    sr = read(S['stats_review']) or ''
    if added.replace('’', "'") not in sr.replace('’', "'") and added[:-1].replace('’', "'").lower() not in sr.replace('’', "'").lower():
        warn('the added payroll sentence, rebuilt from the data, differs from the statistics reviewer’s words')
    FILL.update({'approved': approved, 'added': added, 'n_pass_words': cap(nw(len(passing)))})
    side = json.loads((ROOT / S['payroll_file'].replace('.csv', '.meta.json')).read_text())
    trs = ''.join(f'<tr><th scope="row">{esc(month(r["month"]))}</th><td class="num">{float(r["change_thousands"]) * 1000:+,.0f}</td>'
                  f'<td>{"Yes" if abs(float(r["change_thousands"])) * 1000 > interval else "No, inside it"}</td><td>{esc(cap(r["status"]))}</td></tr>' for r in drops)
    trs = trs.replace('+-', '−').replace('-', '−')
    FIG['payroll'] = {'months': len(rows), 'drops': [(r['month'], r['change_thousands']) for r in drops], 'interval': interval, 'passing': passing,
                      'source': S['payroll_file']}
    src_int = (f'The interval: the Bureau of Labor Statistics’ Employment Situation technical note, {mt.group(1)} release, last modified {mt.group(2)}, '
               f'which puts the 90 percent interval for a month’s change in total payrolls at plus or minus {interval:,}' + (f' (research ledger row {ml.group(1)})' if ml else '') + '.') if mt else ''
    return (f'<h4 class="dec-sub">{esc(it["evidence_h"])}</h4>'
            f'<div class="tw" role="region" tabindex="0" aria-label="Months payrolls shrank; scrolls sideways"><table><caption>The {nw(len(drops))} months payrolls shrank, January 2022 to September 2026, against plus or minus {interval:,}</caption>'
            f'<thead><tr><th scope="col">Month</th><th scope="col">Change in jobs</th><th scope="col">Past the margin of error</th><th scope="col">Status</th></tr></thead><tbody>{trs}</tbody></table></div>'
            f'<p class="small">{esc(side["printed_source_line"])} {esc(src_int)}</p>')


# ------------------------------------------------------------------------------------------------------- panel 2
def explainer_changes():
    """Per chart: what the Explainer maker logged as changed from Phase 2, then each later fix that names the chart."""
    t = read(C['slots']['explainer_notes']) or ''
    first, later = {}, {}
    for head, rows in md_tables(md_section(t, [r'specimens']) or ''):
        if head and head[0] == 'ID':
            k = next((i for i, h in enumerate(head) if h.lower().startswith('changed')), None)
            for r in rows:
                if k is not None and k < len(r):
                    first[r[0]] = r[k]
    for sec in ('fix pass', 'fix pass 2'):
        for head, rows in md_tables(md_section(t, [sec]) or ''):
            low = [h.lower() for h in head]
            sk = next((i for i, h in enumerate(low) if h.startswith('spec')), None)
            fk = next((i for i, h in enumerate(low) if h in ('fix', 'what changed')), None)
            if sk is None or fk is None:
                continue
            for r in rows:
                for sid in re.findall(r'S\d\d', r[sk]):
                    later.setdefault(sid, []).append(r[fk])
    return first, later


def form_name(stem):
    m = re.match(r'\d{8}_S\d\d-(.+?)(?:-(?:Newsprint|Charcoal)-\d+)?$', stem)
    return m.group(1).replace('-', ' ').capitalize() if m else stem


def kit_panel():
    P = C['panels']['kit']
    S = C['slots']
    d = ROOT / S['specimens_dir']
    first, later = explainer_changes()
    cards, n_pass, n_have, times, missing = [], 0, 0, [], []
    for sid in SPEC_IDS:
        lo = sid.lower()
        chk_p = d / f'{lo}-check.json'
        spec_p = ROOT / S['specs_dir'] / f'{lo}.json'
        caps = {(g, w, gr): d / f'{lo}-{g}-{w}{"-grayscale" if gr else ""}.png' for g in ('newsprint', 'charcoal') for w in (1440, 390) for gr in (False, True)}
        if not chk_p.exists() or not spec_p.exists() or not all(p.exists() for p in caps.values()):
            missing.append(sid)
            continue
        n_have += 1
        chk = json.loads(chk_p.read_text())
        spec = json.loads(spec_p.read_text())
        faults = chk.get('faults', [])
        n_pass += 0 if faults else 1
        times += [p.stat().st_mtime for p in caps.values()]
        exports = sorted([p for p in d.glob(f'*_{sid}-*') if p.suffix in ('.svg', '.png', '.csv')], key=lambda p: ('.csv', '.svg', '.png').index(p.suffix))
        fname = form_name(exports[0].stem) if exports else spec['form']
        dr = {(x['ground'], x['page']): x for x in chk.get('drawings', [])}
        b14, b39 = dr.get(('newsprint', 1440), {}), dr.get(('newsprint', 390), {})
        rn = image_compose(f'{sid}-Newsprint', [(caps[('newsprint', 1440, False)], 'At a 1440 px page'), (caps[('newsprint', 390, False)], 'At a 390 px page')])
        rc = image_compose(f'{sid}-Charcoal', [(caps[('charcoal', 1440, False)], 'At a 1440 px page'), (caps[('charcoal', 390, False)], 'At a 390 px page')])
        rg = image_compose(f'{sid}-Grayscale', [(caps[('newsprint', 1440, True)], 'Newsprint, 1440 px page'), (caps[('newsprint', 390, True)], 'Newsprint, 390 px page'),
                                                (caps[('charcoal', 1440, True)], 'Charcoal, 1440 px page'), (caps[('charcoal', 390, True)], 'Charcoal, 390 px page')], cols=2)
        p2 = [SCRATCH / 'phase-2' / f'{sid}-{w}.png' for w in (1440, 390)]
        rp = image_compose(f'{sid}-Phase-2', [(p2[0], 'Phase 2 at a 1440 px page'), (p2[1], 'Phase 2 at a 390 px page')]) if all(p.exists() for p in p2) else None
        chg = first.get(sid)
        lat = later.get(sid, [])
        chg_html = ''
        if chg or lat:
            QUOTED.append(chg or '')
            QUOTED.extend(lat)
            chg_html = (f'<div class="chg"><p class="label">{esc(P["changed_h"])}</p>' + (f'<p>{md_inline(chg)}</p>' if chg else '')
                        + (f'<p class="label sm">{esc(P["changed_later"])}</p><ul>' + ''.join(f'<li>{md_inline(x)}</li>' for x in lat) + '</ul>' if lat else '') + '</div>')
        exp = ''.join(f'<li><code>{esc(p.name)}</code> <span class="num">{p.stat().st_size:,} bytes</span></li>' for p in exports)
        fl = (f'<p class="faults"><b>{nw(len(faults)).capitalize()} {"fault" if len(faults) == 1 else "faults"} in the kit’s check.</b> '
              + esc('; '.join(shorten_paths(f) for f in faults[:4])) + (f'; and {len(faults) - 4} more.' if len(faults) > 4 else '.') + '</p>') if faults else ''
        QUOTED.extend(faults)
        facts = (f'<dl class="facts kf"><div><dt>Form</dt><dd>{esc(fname)}, {esc(spec.get("tier", ""))} tier</dd></div>'
                 f'<div><dt>Rows</dt><dd>{chk.get("rows", "?"):,} in its table and its CSV</dd></div>'
                 f'<div><dt>Checks</dt><dd>{"Passes every check" if not faults else f"{len(faults)} faults"}, {len(chk.get("drawings", []))} drawings checked</dd></div>'
                 f'<div><dt>Drawing bytes</dt><dd>{b14.get("svg_bytes", 0):,} at 1440 and {b39.get("svg_bytes", 0):,} at 390, on Newsprint</dd></div></dl>')
        rows_html = (f'<div class="krow"><p class="row-label">{esc(P["rows"]["newsprint"])}</p>{frame(rn, f"{sid} on Newsprint at a 1440 px page and at a 390 px page, left to right")}</div>'
                     + (f'<div class="krow"><p class="row-label">{esc(P["rows"]["phase2"])}</p>{chg_html}{frame(rp, f"{sid} as Phase 2 drew it on Newsprint, at a 1440 px page and at a 390 px page")}</div>' if rp else
                        f'<div class="krow"><p class="row-label">{esc(P["rows"]["phase2"])}</p>{chg_html}<div class="pending"><p>Phase 2’s picture was not made at this build.</p></div></div>')
                     + f'<div class="krow"><p class="row-label">{esc(P["rows"]["charcoal"])}</p>{frame(rc, f"{sid} on Charcoal at a 1440 px page and at a 390 px page, left to right")}</div>'
                     + f'<details class="more"><summary>{esc(P["rows"]["gray"])}</summary>{frame(rg, f"{sid} grayscale proofs: Newsprint at 1440 and 390, then Charcoal at 1440 and 390")}</details>')
        cards.append(f'<article class="kcard" id="kit-{lo}"><header class="kcard-h"><p class="kid">{sid}</p><div><p class="kev">{esc(spec.get("evidence_label", ""))}</p>'
                     f'<h3 class="ktitle">{esc(spec["title"])}</h3></div></header>{fl}{facts}'
                     f'<details class="more"><summary>{esc(P["exports_h"])}, {len(exports)} files in the board folder</summary><ul class="exports">{exp}</ul><p class="small">{esc(P["exports_note"])}</p></details>'
                     f'{rows_html}</article>')
        FIG.setdefault('kit', {})[sid] = {'faults': len(faults), 'rows': chk.get('rows'), 'svg_bytes_1440': b14.get('svg_bytes'), 'svg_bytes_390': b39.get('svg_bytes'),
                                          'exports': {p.name: p.stat().st_size for p in exports}}
    FILL.update({'n_pass': cap(nw(n_pass, 'none')), 'captured': words_when_time(max(times)) if times else 'not yet'})
    lede = f'<p class="intro">{esc(fill(P["lede"]))}</p><p>{esc(fill(P["lede_2"]))}</p>'
    idx = '<nav class="kidx" aria-label="The 16 charts"><ol>' + ''.join(f'<li><a href="#kit-{s.lower()}">{s}</a></li>' for s in SPEC_IDS if s not in missing) + '</ol></nav>'
    status = 'ready'
    if missing:
        lede += f'<div class="pending" role="status"><p><b>Waiting for the engineer.</b> Captures or check files are missing for {esc(join_words(missing))}.</p></div>'
        status = ('partial', 'engineer')
    return panel('kit', P, lede + idx + ''.join(cards), status)


# ------------------------------------------------------------------------------------------------------- panel 3
def palettes_panel():
    P = C['panels']['palettes']
    d = ROOT / C['slots']['palettes_dir']
    t = read(C['slots']['palette_notes']) or ''
    hits = re.findall(r'(\d+) of (\d+) (?:scripted )?checks pass', t)
    if hits:
        FILL.update({'checks_pass': hits[-1][0], 'checks_n': hits[-1][1]})
    else:
        warn('the palette notes give no count of checks')
    out = [f'<p class="intro">{esc(fill(P["lede"]))}</p><p>{esc(P["lede_2"])}</p>']
    for k, sec in enumerate(P['sections']):
        main = sorted(d.glob(f'*_Palette-Proofs-{sec["key"]}-1440.png'))
        if not main:
            warn(f'no palette capture for {sec["key"]}')
            continue
        r = image_copy(main[-1], f'Palette-{sec["key"]}-1440')
        part = f'<section class="psec" aria-labelledby="pal-{k}"><h3 class="sub" id="pal-{k}">{esc(sec["h"])}</h3>{frame(r, sec["h"] + ", the proof sheet at 1440 px", lazy=k > 1)}'
        others = []
        sh = sec['h']
        for v in ('Grayscale', 'Protanopia', 'Deuteranopia', 'Tritanopia'):
            if v != 'Grayscale' and sec['key'] not in P['simulate']:
                continue
            f = sorted(d.glob(f'*_Palette-Proofs-{sec["key"]}-1440-{v}.png'))
            if f:
                rv = image_copy(f[-1], f'Palette-{sec["key"]}-1440-{v}')
                others.append(f'<figure class="shot"><figcaption><b>{v}</b></figcaption>{frame(rv, f"{sh}, {v.lower()}")}</figure>')
        if others:
            part += f'<details class="more"><summary>{esc(P["other_views"] if len(others) > 1 else P["gray_view"])}</summary>{"".join(others)}</details>'
        tw = sorted(d.glob(f'*_Palette-Proofs-{sec["key"]}-1440-2x.png'))
        if tw:
            rt = image_copy(tw[-1], f'Palette-{sec["key"]}-1440-2x')
            part += f'<details class="more"><summary>{esc(P["twice"])}</summary>{frame(rt, sec["h"] + " at twice size")}</details>'
        out.append(part + '</section>')
    ph = sorted(d.glob('*_Palette-Proofs-Page-390.png'))
    if ph:
        rp = image_copy(ph[-1], 'Palette-Page-390')
        out.append(f'<details class="more"><summary>{esc(P["phone"])}</summary>{frame(rp, "The whole proof sheet at 390 px")}</details>')
    FIG['palettes'] = {'checks': hits[-1] if hits else None, 'images': sorted(n for n in IMAGES if 'Palette' in n)}
    return panel('palettes', P, ''.join(out), 'ready')


# ------------------------------------------------------------------------------------------------------- panel 4
def weight_panel(G, E):
    P = C['panels']['weight']
    rep = G['report'].get('weight', {})
    proj = rep.get('projection', {})
    FILL.update({'page_mb': mb(rep.get('bytes', 0)), 'proj_mb': mb(proj.get('projected_bytes', 0)), 'budget_mb': f'{proj.get("budget", 0) / 1e6:.1f}',
                 'pass_saved': f'{rep.get("pass", {}).get("bytes_saved", 0):,}'})
    parts = [f'<p class="intro">{esc(fill(P["lede"]))}</p>']
    if E['pilot_tables']:
        head, rows = E['pilot_tables'][0]
        parts.append(f'<h3 class="sub">{esc(P["pilot_h"])}</h3>' + table_html(head, rows, caption=P['pilot_h'], cls='wide-t'))
        QUOTED.append(' '.join(' '.join(r) for r in rows))
    if E['found']:
        L, B = P['bar_labels'], E['base']
        bars = [(L['stands'], B['stands']['chapter_14']), (L['islands'], B['islands']['chapter_14']), (L['tables'], B['tables']['chapter_14'])]
        if E['combined']:
            bars.append((L['combined'], E['combined']['chapter_14']))
        bars = [(n, v / 1e6) for n, v in bars]
        stop = E['J']['stop'] / 1e6
        mx = max([v for _, v in bars] + [stop]) * 1.1
        rows = ''.join(f'<tr><th scope="row">{esc(n)}</th><td class="barcell"><span class="bar" data-mark="bar" data-value="{v}" data-key="{esc(n)}" style="width:{100 * v / mx:.3f}%"></span></td><td class="num">{v:.3f} MB</td></tr>' for n, v in bars)
        rows += f'<tr><th scope="row">{esc(L["stop"])}</th><td class="barcell"><span class="bar budget" data-mark="bar" data-value="{stop}" data-key="stop" style="width:{100 * stop / mx:.3f}%"></span></td><td class="num">{stop:.2f} MB</td></tr>'
        parts.append(f'<h3 class="sub">{esc(P["options_h"])}</h3><figure class="wfig" data-spec="chapter-14-weight"><div class="tw" role="region" tabindex="0" aria-label="{esc(P["options_h"])}; scrolls sideways">'
                     f'<table class="wt"><caption>{esc(fill(P["fig_caption"]))}</caption><thead><tr><th scope="col">Option</th><th scope="col"><span class="vh">Bar</span></th><th scope="col">Chapter 14</th></tr></thead><tbody>{rows}</tbody></table></div></figure>')
        if E['table']:
            head, rws = E['table']
            parts.append(table_html(head, rws, caption='The options as the engineer’s notes give them', cls='wide-t'))
            QUOTED.append(' '.join(' '.join(r) for r in rws))
    parts.append(f'<h3 class="sub">{esc(P["today_h"])}</h3><p>{esc(fill(P["today"]))}</p>')
    secs = ''
    for n, blk in E['sections'].items():
        if blk:
            QUOTED.append(blk)
            secs += f'<details class="more"><summary>{esc(n)}</summary><div class="quoted">{md_html(blk)}</div></details>'
    parts.append(f'<h3 class="sub">{esc(P["notes_h"])}</h3><p class="small">{esc(C["panels"]["tested"]["path_note"])}</p>{secs}')
    FIG['weight'] = {'page_bytes': rep.get('bytes'), 'projected': proj.get('projected_bytes'), 'budget': proj.get('budget'), 'pass_saved': rep.get('pass', {}).get('bytes_saved')}
    return panel('weight', P, ''.join(parts), 'ready' if E['found'] and G['ok'] else ('partial', 'engineer' if not E['found'] else 'build'))


# ------------------------------------------------------------------------------------------------------- panel 5
def sanitize(s):
    s = re.sub(r'<(?!/?(?:strong|em|b|i)\b)[^>]+>', '', str(s))
    return s


def ch13_panel(G):
    P = C['panels']['ch13']
    ch = json.loads((ROOT / C['slots']['chapter13']).read_text())
    if not G['ok']:
        return panel('ch13', P, pending_html('build', 'a passing strict build of the guide'), ('waiting', 'build'))
    FILL['build_when'] = words_when_time(G['mtime'])
    parts = [f'<p class="intro">{esc(fill(P["lede"]))}</p><p>{esc(fill(P["lede_2"]))}</p>']
    f14, f39 = SCRATCH / 'plates/first-screen-1440.png', SCRATCH / 'plates/first-screen-390.png'
    if f14.exists() and f39.exists():
        r14 = image_copy(f14, 'Ch13-First-Screen-1440')
        r39 = image_copy(f39, 'Ch13-First-Screen-390')
        parts.append(f'<h3 class="sub">{esc(P["first_h"])}</h3><p class="small">{esc(P["first_cap"])}</p><div class="pair">'
                     f'{figure(r14, "Chapter 13’s first screen at 1440 by 900 px", "<b>1440 by 900 px</b>")}{figure(r39, "Chapter 13’s first screen at 390 by 844 px", "<b>390 by 844 px</b>")}</div>')
    op = SCRATCH / 'plates/s-13-opener.png'
    if op.exists():
        ro = image_copy(op, 'Ch13-Opener-Plate')
        parts.append(f'<h3 class="sub">{esc(P["opener_h"])}</h3>{figure(ro, "Chapter 13’s opening plate at true size", esc(P["opener_cap"]))}')
    groups = {g['before_rule']: g for g in ch['groups']}
    missing = []
    for r in ch['rules']:
        if r['id'] in groups:
            g = groups[r['id']]
            parts.append(f'<h3 class="sub grp">Group {g["number"]}. {esc(g["title"])}</h3><p class="small">{esc(g["line"])}</p>')
        figs = []
        for k in ('correct', 'failure'):
            sp = r[k]['specimen']
            f = SCRATCH / 'plates' / f'{sp}.png'
            if not f.exists():
                missing.append(sp)
                continue
            rec = image_copy(f, slug('Ch13', sp))
            capw = sanitize(r[k]['caption'])
            figs.append(f'<figure class="plate {k}"><figcaption><span class="tag{" fail" if k == "failure" else ""}">{esc(P[k])}</span> {capw}</figcaption>'
                        f'{frame(rec, ("Correct plate" if k == "correct" else "Failure plate") + " for Rule " + r["id"] + ", at true size")}</figure>')
        rule_txt = ''.join(f'<p>{sanitize(x)}</p>' for x in (r['rule'] if isinstance(r['rule'], list) else [r['rule']]))
        parts.append(f'<article class="r13" id="rule-{r["id"].replace(".", "-")}"><h4 class="r13-h"><span class="rid">Rule {esc(r["id"])}</span> {esc(r["title"])}</h4>'
                     f'<details class="more"><summary>{esc(P["rule_text"])}</summary><div class="quoted">{rule_txt}</div></details>{"".join(figs)}</article>')
    status = 'ready'
    if missing:
        warn(f'plates not photographed: {", ".join(missing)}')
        status = ('partial', 'render')
    FIG['ch13'] = {'rules': len(ch['rules']), 'plates': 2 * len(ch['rules']) - len(missing), 'bytes': FILL.get('ch13_bytes'), 'budget': FILL.get('ch13_budget')}
    return panel('ch13', P, ''.join(parts), status)


# ------------------------------------------------------------------------------------------------------- panel 6
def data_panel():
    P = C['panels']['data']
    S = C['slots']
    plan = read(S['data_plan']) or ''
    dd = ROOT / S['data_dir']
    tables = sorted([p for p in dd.iterdir() if p.suffix in ('.csv', '.json') and not p.name.endswith('.meta.json')])
    side = {}
    for p in tables:
        m = p.with_name(p.stem + '.meta.json')
        side[p.name] = json.loads(m.read_text()) if m.exists() else {}
        if not m.exists():
            warn(f'{p.name} has no record beside it')
    kinds = {}
    for s in side.values():
        kinds[s.get('kind', '?')] = kinds.get(s.get('kind', '?'), 0) + 1
    kw = {'public': 'from a public publisher', 'v7': 'read from our systems atlas', 'derived': 'derived by a studio script', 'secondary': 'from a labeled secondary source', 'illustrative': 'invented and labeled'}
    kinds_words = cap(join_words([f'{nw(n)} {kw.get(k, k)}' for k, n in sorted(kinds.items(), key=lambda kv: -kv[1])]))
    # the plan's count by domain
    sec = md_section(plan, [r'rounds 0 to 2: \d+ examples']) or ''
    dt = md_tables(sec)
    n_ex, top = None, None
    dom_html = ''
    if dt:
        head, rows = dt[0]
        tot = next((r for r in rows if re.sub(r'\*', '', r[0]).strip().lower() == 'all'), None)
        k = head.index('Total') if 'Total' in head else 4
        n_ex = int(re.sub(r'\D', '', tot[k])) if tot else None
        vals = [int(re.sub(r'\D', '', r[k])) for r in rows if r is not tot and 'atlas-wide' not in r[0].lower() and re.sub(r'\D', '', r[k])]
        top = max(vals) if vals else None
        dom_html = table_html([re.sub(r'\*', '', h) for h in head], [[re.sub(r'\*\*', '', c) for c in r] for r in rows], caption=P['domain_h'])
    FILL.update({'n_tables': len(tables), 'n_examples': n_ex or '?', 'top_domain_n': f'{top} of {n_ex}' if top else '?', 'kinds': kinds_words})
    # by state: the states each built chart's spec singles out, and the states the plan's rows name
    names = {r['code']: r['name'] for r in csv.DictReader(open(dd / 'census-cps-2024-turnout-by-state.csv'))}
    count = {}
    for sid in SPEC_IDS:
        sp = ROOT / S['specs_dir'] / f'{sid.lower()}.json'
        if sp.exists():
            for st in json.loads(sp.read_text()).get('states', []):
                count.setdefault(st, []).append(sid)
    for sname in ('round 1: 41 forms', 'round 2: 41 forms'):
        for head, rows in md_tables(md_section(plan, [re.escape(sname)]) or ''):
            if 'States' in head:
                k = head.index('States')
                st_k = head.index('Status') if 'Status' in head else None
                for r in rows:
                    if st_k is not None and st_k < len(r) and r[st_k].startswith('Built'):
                        continue      # a built chart counts once, from its spec
                    for code, nm in names.items():
                        if code != 'US' and re.search(r'\b' + re.escape(nm) + r'\b', r[k] if k < len(r) else ''):
                            count.setdefault(code, []).append(f'row {r[0]}')
    limit = int((n_ex or 0) / 5) if n_ex else None
    srows = sorted(count.items(), key=lambda kv: (-len(kv[1]), names.get(kv[0], kv[0])))
    st_html = (f'<h3 class="sub">{esc(P["state_h"])}</h3><p>{esc(P["state_lede"])} The limit is one in five, {limit} of {n_ex}.</p>'
               + table_html(P['state_cols'], [[names.get(c, c), str(len(v)), join_words(v)] for c, v in srows], quote=False, caption=P['state_h']))
    bs = re.search(r'\*\*By state\.\*\*\s*(.+)', sec)
    if bs:
        QUOTED.append(bs.group(1))
        st_html += f'<details class="more"><summary>{esc(P["plan_says"])}</summary><blockquote class="q"><p>{md_inline(bs.group(1))}</p></blockquote></details>'
    # every table
    doms = {d_['id']: d_['title'] for d_ in json.loads((ROOT / 'work/extract/atlas-v7-data.json').read_text()).get('domains', [])}
    trs = []
    for p in tables:
        s = side[p.name]
        dom = s.get('domain', '')
        trs.append([f'`{p.stem}`', s.get('kind', ''), s.get('publisher', ''), s.get('observation_period', ''), doms.get(dom, 'Every domain' if dom == 'all' else dom), s.get('ledger_row', '')])
    tbl = table_html(P['tables_cols'], trs, quote=False, caption=P['tables_open'], cls='small-t')
    # the one download
    rn = read(S['research_notes']) or ''
    dl = md_section(rn, [r'the five-download list.*']) or ''
    dl_html = ''
    for head, rows in md_tables(dl):
        dl_html += table_html(head, rows, caption='The download list')
        QUOTED.append(' '.join(' '.join(r) for r in rows))
    done = re.search(r'\*\*Done\.\*\*\s*(.+)', dl)
    if done:
        QUOTED.append(done.group(1))
        dl_html += f'<blockquote class="q"><p>{md_inline(done.group(1))}</p><footer>{esc(P["download_cite"])}</footer></blockquote>'
    fr = next((p for p in tables if p.stem == 'fred-unemployment-and-job-openings'), None)
    if fr:
        n_rows = sum(1 for _ in open(fr)) - 1
        s = side[fr.name]
        dr = s.get('date_retrieved', '')
        dr = words_when(datetime.datetime.strptime(dr, '%Y-%m-%d')) if re.fullmatch(r'\d{4}-\d\d-\d\d', dr) else dr
        dl_html += f'<p class="small">The frozen file today: <code>{esc(fr.name)}</code>, {n_rows:,} rows, read {esc(dr)}, research ledger row {esc(s.get("ledger_row", ""))}. {esc(s.get("printed_source_line", ""))}</p>'
    # the three November 3 outcomes
    fp2 = md_section(rn, [r'fix pass 2']) or ''
    blk = re.search(r'\*\*D3-98:.*?\*\*(.*?)(?:\n\*\*D3-95|\Z)', fp2, flags=re.S)
    oc_rows = []
    for x in md_items(blk.group(1) if blk else ''):
        m = re.match(r'\*\*(.+?)\*\*\s*\(([^)]*)\)[^:]*:\s*(.*?)\s*Source:\s*(.*?)\s*Retrieved ([^.]+)\.(.*)$', x)
        if m:
            led = re.search(r'Ledger (P7-\d+[a-z]?)', m.group(6))
            oc_rows.append([f'**{m.group(1)}**, {m.group(2)}', m.group(3), f'{m.group(4)} Retrieved {m.group(5)}.' + (f' Research ledger row {led.group(1)}.' if led else '')])
    if len(oc_rows) != 3:
        warn(f'found {len(oc_rows)} November 3 outcomes in the research notes, not three')
    QUOTED.append(' '.join(' '.join(r) for r in oc_rows))
    printed = ''
    for sid in ('s03', 's08'):
        sp = json.loads((ROOT / S['specs_dir'] / f'{sid}.json').read_text())
        n0 = next((n for n in sp.get('notes', []) if n.startswith('As of')), None)
        if n0:
            printed = printed or n0
            if n0 != printed:
                warn('S03 and S08 print different dated notes')
    oc_html = (f'<h3 class="sub">{esc(P["outcomes_h"])}</h3><p>{esc(P["outcomes_lede"])}</p>' + table_html(P['outcomes_cols'], oc_rows, caption=P['outcomes_h'])
               + (f'<h4 class="sheet-h">{esc(P["printed_h"])}</h4><blockquote class="q"><p>{md_inline(printed)}</p></blockquote>' if printed else ''))
    QUOTED.append(printed)
    body = (f'<p class="intro">{esc(fill(P["lede"]))}</p><h3 class="sub">{esc(P["domain_h"])}</h3>{dom_html}{st_html}'
            f'<h3 class="sub">{esc(fill(P["tables_h"]))}</h3><p>{esc(fill(P["tables_lede"]))}</p><details class="more"><summary>{esc(P["tables_open"])}</summary>{tbl}</details>'
            f'<h3 class="sub">{esc(P["download_h"])}</h3>{dl_html}{oc_html}')
    FIG['data'] = {'tables': len(tables), 'kinds': kinds, 'examples': n_ex, 'top_domain': top, 'states': {k: v for k, v in count.items()}, 'outcomes': oc_rows}
    return panel('data', P, body, 'ready' if dt and len(oc_rows) == 3 else ('partial', 'engineer'))


# ------------------------------------------------------------------------------------------------------- panel 7
def red_team_rows():
    out = []
    briefs = ' '.join(read(p) or '' for p in C['slots']['fix_briefs'])
    for rt in C['slots']['red_teams']:
        t = read(rt['file'])
        if t is None:
            out.append((rt['name'], 'waiting', None, None, None, None))
            continue
        parts = re.split(r'^## Part (\d)\b.*$', t, flags=re.M)
        chunks = [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)] if len(parts) > 1 else [('all', t)]
        for pn, ch in chunks:
            sc = None
            for l in ch.splitlines():
                if re.match(r'^#+\s.*score', l, flags=re.I):
                    m = re.search(r'\b([1-5]) of 5\b', l)
                    if m:
                        sc = int(m.group(1))
                        break
            if sc is None:
                ssec = md_section(ch, [r'.*score.*']) or ''
                m = re.search(r'\b([1-5]) of 5\b', ssec)
                sc = int(m.group(1)) if m else None

            def count(pat):
                n = 0
                for m in re.finditer(r'^(#+)\s*(?:\d+\.\s*)?(.+?)\s*$', ch, flags=re.M):
                    if re.match(pat, m.group(2), flags=re.I):
                        body = md_section(ch, [re.escape(m.group(2))]) or ''
                        n += len(re.findall(r'^(?:- )?\*\*(?:[A-Z]{1,3}\d+|P2-[MS]\d+)\.', body, flags=re.M))
                return n
            q = 0
            for m in re.finditer(r'^(#+)\s*(?:\d+\.\s*)?(questions for dustin)\s*$', ch, flags=re.M | re.I):
                body = md_section(ch, [re.escape(m.group(2))]) or ''
                q += len(re.findall(r'^(?:\*\*Q\d+\.|\d+\.\s)', body, flags=re.M))
            out.append((rt['name'], pn, sc, count(r'must fix'), count(r'should fix'), q))
    # the fix briefs' tables for the same reviews
    agree = []
    for head, rows in md_tables(briefs):
        if head and head[0] == 'Review':
            for r in rows:
                agree.append(r)
    return out, agree


def scores_panel():
    P = C['panels']['scores']
    first, rescore = cd_scores()
    parts, status = [], 'ready'
    if first:
        parts.append(cd_table(rescore or first, first if rescore else None, P))
    if not rescore:
        parts.append(f'<div class="pending" role="status"><p><b>Waiting for {esc(P["cd_rescore_wait"])}.</b> The rescore after the fix pass joins this table when its file lands; each cell then shows both scores.</p></div>')
        status = ('partial', 'cd')
    rows, agree = red_team_rows()
    pw = C['slots']['part_words']
    trs = []
    for name, pn, sc, mf, sf, q in rows:
        if pn == 'waiting':
            trs.append(f'<tr><th scope="row">{esc(name)}</th><td colspan="5">Waiting for the report</td></tr>')
            continue
        trs.append(f'<tr><th scope="row">{esc(name)}</th><td>{esc(pw.get(pn, pn))}</td><td class="num">{sc if sc else "?"} of 5</td><td class="num">{mf}</td><td class="num">{sf}</td><td class="num">{q}</td></tr>')
    FIG['red_teams'] = rows
    # the counts the fix briefs printed, checked against the reports
    mism = []
    for name, pn, sc, mf, sf, q in rows:
        for r in agree:
            key = name.split(',')[0].split(' and ')[0].lower()
            if r[0].lower().startswith(key[:10]) and ((pn == '2') == ('part 2' in r[0].lower()) or pn == 'all'):
                try:
                    if int(re.sub(r'\D', '', r[2])[:2] or -1) != mf or int(re.sub(r'\D', '', r[3].split('(')[0]) or -1) != sf:
                        mism.append(f'{name}, part {pn}: reports {mf} and {sf}, brief says {r[2]} and {r[3]}')
                except ValueError:
                    pass
    for m in mism:
        note('red team count differs from the fix brief: ' + m)
    hd = ''.join(f'<th scope="col">{esc(c)}</th>' for c in P['rt_cols'])
    parts.append(f'<h3 class="sub">{esc(P["rt_h"])}</h3><p>{esc(P["rt_lede"])}</p><div class="tw" role="region" tabindex="0" aria-label="{esc(P["rt_h"])}; scrolls sideways">'
                 f'<table><thead><tr>{hd}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'
                 f'<p class="small">{esc(P["rt_note"])}</p>')
    return panel('scores', P, ''.join(parts), status)


def cd_table(d, first, P):
    crit = d.get('criteria') or []
    items = d.get('items', [])
    head = '<th scope="col">Item</th>' + ''.join(f'<th scope="col">{esc(c["name"])}</th>' for c in crit) + '<th scope="col">Ready</th>'
    f_items = {i['key']: i for i in (first or {}).get('items', [])}
    rows = []
    for it in items:
        sc = it.get('scores', {})
        f = f_items.get(it.get('key'), {}).get('scores', {})

        def cellv(c):
            v, w = sc.get(c['key'], ''), f.get(c['key'])
            lo = isinstance(v, (int, float)) and v < 4
            if first is None:
                return f'<td class="num sc{" lo" if lo else ""}">{esc(v)}</td>'
            wlo = isinstance(w, (int, float)) and w < 4
            moved = w is not None and w != v
            fw = f'<span class="r2{" lo" if wlo else ""}">{esc(w) if w is not None else "new"}</span>'
            return f'<td class="num sc{" mv" if moved else ""}">{fw}<span class="r3{" lo" if lo else ""}">{esc(v)}</span></td>'
        rows.append(f'<tr><th scope="row">{esc(it.get("name", it.get("key")))}</th>{"".join(cellv(c) for c in crit)}<td>{"Yes" if it.get("ready") else "<b>Not yet</b>"}</td></tr>')
    nr = [i for i in items if not i.get('ready')]
    short = lambda i: P['short_names'].get(i.get('key'), i.get('name'))
    if first:
        fi = first.get('items', [])
        summ = (f'<p class="intro">The creative director first found {nw(sum(1 for i in fi if i.get("ready")), "none")} of the {nw(len(fi))} items ready. After the fix pass the rescore finds '
                + (f'all {nw(len(items))} ready' if not nr else f'{nw(len(items) - len(nr), "none")} of the {nw(len(items))} ready, with {join_words([short(i) for i in nr])} still short') + '.</p>')
    else:
        summ = (f'<p class="intro">The creative director’s first scores found {nw(len(items) - len(nr), "none")} of the {nw(len(items))} items ready'
                + (f': {join_words([short(i) for i in nr])} each had a score under 4 or a Must fix open.' if nr else '.') + '</p>')
    under = []
    for i in items:
        for c in crit:
            v = i.get('scores', {}).get(c['key'])
            if isinstance(v, (int, float)) and v < 4:
                rs = i.get('reasons', {}).get(c['key'], '')
                QUOTED.append(rs)
                under.append(f'<li><b>{esc(i["name"])}, {esc(c["name"].lower())}, {v}.</b> {md_inline(rs)}</li>')
    summ += f'<ul class="findings">{"".join(under)}</ul>' if under else ''
    legend = (P['legend_both'] if first else P['legend_first'])
    FIG['cd_scores'] = {'items': len(items), 'ready': len(items) - len(nr), 'rescore': bool(first)}
    return (f'<h3 class="sub">{esc(P["cd_h"])}</h3>{summ}<p class="small">{esc(legend)}</p>'
            f'<div class="tw" role="region" tabindex="0" aria-label="The creative director’s scores; scrolls sideways"><table class="scores"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


# ------------------------------------------------------------------------------------------------------- panel 8
def tested_panel():
    P = C['panels']['tested']
    cols, waiting = [], []
    for s in C['slots']['tested']:
        p = ROOT / s['file']
        if not p.exists():
            waiting.append(s['label'])
            continue
        items = tested_lists(p.read_text())
        ti = [(w, x) for k, w, x in items if k == 'tested']
        ni = [(w, x) for k, w, x in items if k == 'not']
        if not ti:
            waiting.append(s['label'])
            continue
        QUOTED.extend(x for _, x in ti + ni)

        def lst(xs):
            out, cur = '', None
            for w, x in xs:
                if w != cur:
                    out += (f'</ul>' if cur is not None else '') + (f'<p class="where">{esc(strip_codes(w))}</p>' if w else '') + '<ul>'
                    cur = w
                out += f'<li>{md_inline(x)}</li>'
            return out + ('</ul>' if xs else '')
        cols.append(f'<div class="tcol"><h3 class="tcol-h">{esc(s["label"])}</h3><p class="label">Not tested</p>{lst(ni) or "<p>Nothing listed.</p>"}'
                    f'<details class="more"><summary>What they tested, {len(ti)} items</summary>{lst(ti)}</details></div>')
        FIG.setdefault('tested', {})[s['file']] = {'tested': len(ti), 'not': len(ni)}
    body = f'<p class="intro">{esc(P["lede"])}</p><p class="small">{esc(P["path_note"])}</p><div class="tcols">{"".join(cols)}</div>'
    if waiting:
        body += f'<div class="pending" role="status"><p><b>Waiting for lists from {esc(join_words([w[:1].lower() + w[1:] for w in waiting]))}.</b> Each joins this panel when its notes carry a Tested list.</p></div>'
        return panel('tested', P, body, ('partial', 'notes'))
    return panel('tested', P, body, 'ready')


# ------------------------------------------------------------------------------------------------------- page
STATUS = {}
ORDER = ['decide', 'kit', 'palettes', 'weight', 'ch13', 'data', 'scores', 'tested']


def pending_html(who, filelabel):
    return f'<div class="pending" role="status"><p><b>{esc(C["status_words"]["waiting"].format(who=C["owners"].get(who, who)))}.</b> This part fills in when {esc(filelabel)} lands.</p></div>'


def panel(key, P, body, status):
    STATUS[key] = status
    refs = P['refs']
    check_refs(refs, 'panel ' + key)
    if MOVED:
        extra = sorted((c for c in MOVED if c in LOG and not re.search(r'\b' + re.escape(c) + r'\b', refs)), key=lambda c: (re.sub(r'[^A-Z]', '', c.split('-')[0]), int(re.sub(r'\D', '', c.split('-')[1]) or 0)))
        if extra:
            refs += ' · from teammates’ files: ' + ' · '.join(extra)
        MOVED.clear()
    return (f'<section class="sec" id="p-{key}" aria-labelledby="h-{key}"><div class="sec-top"><p class="label">Panel {P["n"]}</p>{status_chip(status)}</div>'
            f'<h2 class="sec-h" id="h-{key}">{esc(P["title"])}</h2>{body}<p class="codes">Reference: {esc(refs)}</p></section>')


def status_words(st):
    if st == 'ready':
        return C['status_words']['ready']
    kind, who = st
    return C['status_words'][kind].format(who=C['owners'].get(who, who))


def status_chip(st, short=False):
    kind = st if isinstance(st, str) else st[0]
    return f'<span class="st {kind}">{esc(C["status_short"][kind] if short else status_words(st))}</span>'


def cover():
    K = C['cover']
    toc = ''.join(f'<li><a href="#p-{k}"><span class="n">{C["panels"][k]["n"]:02d}</span><span class="t">{esc(C["panels"][k]["nav"])}</span></a>{status_chip(STATUS[k], short=True)}</li>' for k in ORDER)
    ready = sum(1 for k in ORDER if STATUS[k] == 'ready')
    deck = ''.join(f'<p>{esc(x)}</p>' for x in K['deck'])
    return (f'<header class="cover"><div class="mast"><b>OATH &amp; ACTION</b><span class="label">{esc(K["kicker"])}</span></div>'
            f'<p class="label for">{esc(fill(K["for_line"]))}</p><h1>{esc(K["title"])}</h1>'
            f'<div class="cover-grid"><div class="deck">{deck}<p class="caption">{esc(K["minutes"])}</p></div>'
            f'<nav class="toc" aria-labelledby="toc-h"><p class="label" id="toc-h">{esc(K["toc_h"])} · {ready} of {len(ORDER)} ready</p><ol>{toc}</ol></nav></div></header>')


CSS = r'''
:root{--m:16px;--mr:16px;--max:82rem;
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
.tw:focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
p{margin:0 0 var(--oa-space-150);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
h1,h2,h3,h4{margin:0}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.board{max-width:calc(var(--max) + var(--m) + var(--mr));margin:0 auto;padding:0 var(--mr) var(--oa-space-1300) var(--m);overflow-wrap:break-word}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0}
.caption,.small{font:var(--oa-type-caption);color:var(--ink-2)}
.small{max-width:var(--oa-layout-measure-intro-max)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max);margin-bottom:var(--oa-space-300)}
.codes{font:var(--oa-type-caption);color:var(--ink-2);margin:var(--oa-space-300) 0 0;font-variant-numeric:tabular-nums;max-width:none}
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
.toc ol{list-style:none;margin:0;padding:0}
.toc li{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-050) var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-050) 0}
.toc a{display:inline-flex;gap:var(--oa-space-150);min-height:2.75rem;align-items:center;text-decoration:none;font:var(--oa-type-ui);font-weight:600}
.toc a:hover .t{text-decoration:underline}
.toc .n{font-variant-numeric:tabular-nums;color:var(--ink-2);font-weight:400;min-width:1.6em}
.st{font:var(--oa-type-caption);font-weight:600;padding:0 .5em;max-width:100%;border:var(--oa-border-width-hairline) solid var(--strong);line-height:1.6}
.st.ready{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint);border-color:var(--oa-color-palette-charcoal)}
.st.waiting,.st.partial{background:transparent;color:var(--ink)}
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-300)}
.sec-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--oa-space-100) var(--oa-space-300)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:var(--oa-space-150) 0 var(--oa-space-400);text-wrap:balance;max-width:20ch}
.sub{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:var(--oa-space-600) 0 var(--oa-space-200);text-wrap:balance}
.sub.grp{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-200)}
.sheet-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-300) 0 var(--oa-space-100)}
.tag{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--strong);padding:2px 6px;white-space:nowrap;vertical-align:.1em}
.tag.rec{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint);border-color:var(--oa-color-palette-charcoal)}
.tag.fail{background:transparent}
.reply{font:var(--oa-type-ui);font-weight:600;max-width:var(--oa-layout-measure-intro-max)}
/* panel 1 */
.dec{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);margin-top:var(--oa-space-600);padding-top:var(--oa-space-200)}
.dec-h{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin-bottom:var(--oa-space-150)}
.dec-q{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.dec-rec{max-width:var(--oa-layout-measure-intro-max);font-weight:600}
.dec-rec.approve{border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-left:var(--oa-space-200)}
.ph-h{font:var(--oa-type-ui);font-weight:700;margin:var(--oa-space-300) 0 var(--oa-space-100)}
blockquote.q ol{margin:0 0 var(--oa-space-100);padding-left:1.2em}
.dec-sub{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-400) 0 var(--oa-space-150)}
table.opts{min-width:46rem}table.opts th[scope=row]{min-width:14rem}
table.wide-t{min-width:44rem}table.small-t{min-width:52rem}
tr.recrow th,tr.recrow td{background:var(--oa-color-tint-stone-n88)}
blockquote.q{margin:var(--oa-space-150) 0;padding:var(--oa-space-150) 0 var(--oa-space-150) var(--oa-space-300);border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);max-width:var(--oa-layout-measure-intro-max)}
blockquote.q p{margin:0 0 var(--oa-space-100)}
blockquote.q footer{font:var(--oa-type-caption);color:var(--ink-2)}
/* pictures */
.shot{margin:var(--oa-space-200) 0 var(--oa-space-300);min-width:0;max-width:100%;display:flex;flex-direction:column;gap:var(--oa-space-100)}
.shot figcaption{font:var(--oa-type-caption);color:var(--ink-2);max-width:var(--oa-layout-measure-intro-max)}
.shot figcaption b{color:var(--ink);font-weight:600}
.frame{max-width:100%;line-height:0;align-self:flex-start}
.frame.wide{overflow-x:auto;overscroll-behavior-x:contain}
.frame img{display:block;max-width:none;height:auto}
.pair{display:flex;flex-wrap:wrap;gap:0 var(--oa-space-400);align-items:flex-start}
.pair .shot{flex:0 1 auto}
/* panel 2 */
.kidx ol{list-style:none;margin:var(--oa-space-200) 0 0;padding:0;display:flex;flex-wrap:wrap;gap:var(--oa-space-100)}
.kidx a{display:inline-flex;align-items:center;justify-content:center;min-width:2.75rem;min-height:2.75rem;padding:0 .5em;border:var(--oa-border-width-hairline) solid var(--strong);text-decoration:none;font:var(--oa-type-ui);font-weight:600}
.kcard{margin-top:var(--oa-space-800);border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-200)}
.kcard-h{display:grid;grid-template-columns:auto minmax(0,1fr);gap:var(--oa-space-300);align-items:start}
.kid{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0;font-variant-numeric:tabular-nums}
.kev{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0 0 var(--oa-space-050)}
.ktitle{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);max-width:var(--oa-layout-measure-intro-max);text-wrap:balance}
.krow{margin-top:var(--oa-space-300)}
.row-label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0 0 var(--oa-space-100)}
.chg{max-width:var(--oa-layout-measure-intro-max);font:var(--oa-type-body-small);margin-bottom:var(--oa-space-200)}
.chg p{margin-bottom:var(--oa-space-100)}
.chg ul{margin:0 0 var(--oa-space-100);padding-left:1.2em}
.label.sm{margin-top:var(--oa-space-150)}
.faults{font:var(--oa-type-body-small);border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-left:var(--oa-space-150);max-width:var(--oa-layout-measure-intro-max);margin-top:var(--oa-space-200)}
.exports{list-style:none;margin:0 0 var(--oa-space-100);padding:0;font:var(--oa-type-body-small)}
.exports li{padding:var(--oa-space-050) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair);display:flex;flex-wrap:wrap;gap:0 var(--oa-space-200);justify-content:space-between}
.num{font-variant-numeric:tabular-nums}
details.more{margin-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
details.more>summary{cursor:pointer;font:var(--oa-type-ui);font-weight:600;min-height:2.75rem;display:flex;align-items:center;gap:var(--oa-space-100)}
.facts{display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-500);margin:var(--oa-space-200) 0;border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:64em){.facts.kf{grid-template-columns:repeat(4,minmax(0,1fr))}.facts.kf3{grid-template-columns:repeat(3,minmax(0,1fr))}}
.facts div{padding:var(--oa-space-100) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.facts dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2)}
.facts dd{margin:var(--oa-space-050) 0 0;font:var(--oa-type-body-small)}
/* panel 3 */
.psec .sub{margin-top:var(--oa-space-800)}
/* panel 5 */
.r13{margin-top:var(--oa-space-500);border-top:var(--oa-border-width-hairline) solid var(--strong);padding-top:var(--oa-space-200)}
.r13-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);max-width:var(--oa-layout-measure-intro-max);text-wrap:balance}
.r13-h .rid{display:block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin-bottom:var(--oa-space-050)}
.plate{margin:var(--oa-space-300) 0 0;display:flex;flex-direction:column;gap:var(--oa-space-100);max-width:100%}
.plate figcaption{font:var(--oa-type-body-small);max-width:var(--oa-layout-measure-intro-max)}
.quoted{font:var(--oa-type-body-small);max-width:var(--oa-layout-measure-intro-max)}
.quoted ul,.quoted ol{padding-left:1.2em}
.quoted .qh{font-weight:700;margin-top:var(--oa-space-200)}
/* tables */
.tw{position:relative;overflow-x:auto;background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);margin:var(--oa-space-200) 0 var(--oa-space-100)}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
caption{caption-side:top;text-align:left;padding:var(--oa-space-150) var(--oa-space-200);font:var(--oa-type-body-small);color:var(--wink-2);border-bottom:var(--oa-border-width-hairline) solid var(--whair)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-100) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--oa-color-tint-white-n55);vertical-align:bottom}
tbody th{font:var(--oa-type-body-small);font-weight:600;color:var(--wink);text-transform:none;letter-spacing:0}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
table.small-t td,table.small-t th{font:var(--oa-type-caption)}
td.sc.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong);font-weight:700}
td.sc .r2{display:inline-block;min-width:1.4em;font:var(--oa-type-caption);color:var(--wink-2);margin-right:.35em;padding:0 .2em}
td.sc .r3{display:inline-block;min-width:1.6em;font-weight:700;padding:0 .2em}
td.sc .lo{box-shadow:inset 0 0 0 var(--oa-border-width-hairline) var(--wstrong)}
td.sc .r3.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong)}
td.sc.mv .r3{background:var(--oa-color-tint-stone-n88)}
.wfig{margin:0}
.wt th{width:22rem;font-weight:600}
.barcell{width:50%;min-width:10rem}
.bar{display:block;height:1.25rem;background:var(--oa-color-palette-charcoal)}
.bar.budget{background:transparent;box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--oa-color-palette-charcoal)}
.pending{border:var(--oa-border-width-hairline) solid var(--strong);border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding:var(--oa-space-200) var(--oa-space-300);margin:var(--oa-space-200) 0;max-width:var(--oa-layout-measure-intro-max)}
.pending p{margin:0}
.findings{margin:0 0 var(--oa-space-200);padding-left:1.2em;max-width:var(--oa-layout-measure-intro-max)}
.findings li{margin-bottom:var(--oa-space-100)}
/* panel 8 */
.tcols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-500);margin-top:var(--oa-space-400)}
@media (min-width:64em){.tcols{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tcol{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-150);min-width:0}
.tcol-h{font:var(--oa-type-h4);margin-bottom:var(--oa-space-150)}
.tcol ul{margin:var(--oa-space-050) 0 var(--oa-space-200);padding-left:1.2em;font:var(--oa-type-body-small)}
.tcol li{margin-bottom:var(--oa-space-050);overflow-wrap:anywhere}
.tcol .where{font:var(--oa-type-caption);color:var(--ink-2);margin:var(--oa-space-150) 0 0}
pre.raw{white-space:pre-wrap;font-size:.875rem;background:var(--white);color:var(--wink);padding:var(--oa-space-200);border:var(--oa-border-width-hairline) solid var(--whair);max-height:28rem;overflow:auto}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:none}
@media print{.toc{display:none}details{display:block}}
'''


def strip_css(t):
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'/\*.*?\*/', '', t, flags=re.S)).strip()


def build_page(sections):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(C["title"])}</title>
<meta name="chart-views" content="overview"><meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400;1,500&display=swap" rel="stylesheet">
<style>{strip_css((ROOT / C["slots"]["board_base"]).read_text())}
{strip_css((ROOT / C["slots"]["tokens_css"]).read_text())}
{strip_css(CSS)}</style></head>
<body><main class="board" data-view-root="overview">
{sections}
<p class="foot caption">{esc(fill(C["foot"]))}</p>
</main></body></html>'''


def visible_text(page):
    t = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    t = re.sub(r'<span class="vh">[^<]*</span>', '', t)
    t = re.sub(r'</?(?:p|li|ul|ol|h\d|td|th|tr|div|figure|figcaption|caption|blockquote|section|header|nav|aside|main|table|thead|tbody|summary|details|dt|dd|dl|pre|article|footer)\b[^>]*>|<br\s*/?>', ' ', t)
    return html.unescape(re.sub(r'<[^>]+>', '', t))


def checks(page):
    text = visible_text(page)
    i = text.find('—')
    need(i < 0, 'an em dash on the board: ' + text[max(0, i - 60):i + 20])
    if '–' in text:
        i = text.find('–')
        warn('an en dash on the board: ' + text[max(0, i - 40):i + 20])
    own_page = page
    for q in QUOTED:
        if q:
            for frag in (md_inline(q), md_inline(q, quote=False)):
                own_page = own_page.replace(frag, ' ')
    own_page = re.sub(r'<div class="tcols">.*?</div>\s*(?=<p class="codes">|<div class="pending")', ' ', own_page, flags=re.S)
    own_page = re.sub(r'<div class="quoted">.*?</div>', ' ', own_page, flags=re.S)
    own = visible_text(own_page)
    for leftover in re.findall(r'\{[a-z0-9_]+\}', own):
        warn(f'an unfilled field on the board: {leftover}')
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', own, flags=re.I)})
    if flagged:
        warn('flagged words in the board’s own words: ' + ', '.join(flagged))
    face = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))
    stray = set(re.findall(r'\b' + CODE_DEC + r'\b|\b[IYSMT][1-9]\b(?!\s*px)|\b[IYMT]10\b', face))
    quoted_stray = set(re.findall(r'\b[IYSMT][1-9]\b', face)) - set(re.findall(r'\b[IYSMT][1-9]\b(?!\s*px)', own))
    stray -= quoted_stray
    if stray:
        warn('studio codes on the board’s face: ' + ', '.join(sorted(stray)))
    rev = set(re.findall(r'\bK[MS]\d+\b|\bP2-[MS]\d+\b|\bENG-\d+\b', face))
    if rev:
        warn('review or request IDs on the board’s face: ' + ', '.join(sorted(rev)))
    for pat in (r'/home/', r'file://', r'scratchpad', r'/tmp/', r'@anthropic'):
        if re.search(pat, page):
            warn(f'a private path on the board ({pat})')
    if re.search(r'<script\b', page, flags=re.I):
        warn('a script on the board')
    hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', page))
    extra = hosts - {'fonts.googleapis.com', 'fonts.gstatic.com'}
    if extra:
        warn('loads from hosts other than Google Fonts: ' + ', '.join(sorted(extra)))
    for v, u in re.findall(r'font-size:\s*(\d*\.?\d+)(px|rem)', strip_css(CSS)):
        if float(v) * (16 if u == 'rem' else 1) < 13:
            warn(f'a font size of {v}{u} in the board CSS, under 13 px')
    return text


def main():
    global LOG, C, CACHE, PHOTO_DIR, WEIGHT_FILE
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--no-render', action='store_true')
    ap.add_argument('--out', type=pathlib.Path, default=OUT)
    ap.add_argument('--photo-proof', type=pathlib.Path, help='read the photo proof from this folder (for a test)')
    ap.add_argument('--weight-options', type=pathlib.Path, help='read the weight options from this file (for a test)')
    a = ap.parse_args()
    PHOTO_DIR, WEIGHT_FILE = a.photo_proof, a.weight_options
    raw = CONTENT.read_text()
    need('—' not in raw, 'the content file holds an em dash')
    C = json.loads(raw)
    LOG = read_log()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    CACHE = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL['built_date'] = words_when(built)
    TOK, _ = css_tokens()
    print('building the guide (strict) ...')
    G = guide_build()
    print('photographing ...')
    run_renders(render_jobs(G), render=not a.no_render)
    E = engineer_numbers()
    FIG.update({'built': built.isoformat()})
    s_dec = decide_panel(G, E, TOK)
    s_kit = kit_panel()
    s_pal = palettes_panel()
    s_wt = weight_panel(G, E)
    s_13 = ch13_panel(G)
    s_dat = data_panel()
    s_sco = scores_panel()
    s_tes = tested_panel()
    CACHE_FILE.write_text(json.dumps(CACHE))
    keep = set(IMAGES)
    for p in [q for q in IMG.iterdir() if q.suffix.lower() in IMG_EXT]:
        if p.name not in keep:
            p.unlink()
            note(f'removed {p.name}, which the board no longer shows')
    body = '\n'.join([s_dec, s_kit, s_pal, s_wt, s_13, s_dat, s_sco, s_tes])
    page = build_page(cover() + '\n' + body)
    checks(page)
    need(len(page.encode()) < LIMIT_PAGE, 'the board page is over 16 MB')
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    files = [a.out] + sorted(q for q in IMG.iterdir() if q.suffix.lower() in IMG_EXT)
    big = [p.name for p in files if p.stat().st_size > LIMIT_IMAGE]
    if big:
        warn('images over 15 MB: ' + ', '.join(big))
    if len(files) >= LIMIT_FILES:
        warn(f'{len(files)} files, at or over {LIMIT_FILES}')
    total = sum(p.stat().st_size for p in files)
    if total >= LIMIT_TOTAL:
        warn(f'the page and its images come to {total / 1e6:.2f} MB, at or over {LIMIT_TOTAL / 1e6:.0f} MB for one publish')
    FIG.update({'board': rel(a.out), 'html_bytes': len(page.encode()), 'images': len(files) - 1, 'folder_bytes_with_images': total,
                'largest_image': max(((p.stat().st_size, p.name) for p in files[1:]), default=(0, None)),
                'status': {k: (v if isinstance(v, str) else list(v)) for k, v in STATUS.items()},
                'image_sources': {r['src']: r.get('source') for r in IMAGES.values()}, 'codes_in_reference_lines': sorted(LINKED_CODES),
                'notes': NOTES, 'warnings': WARN, 'visible_text_sha1': hashlib.sha1(visible_text(page).encode()).hexdigest()})
    FIGURES.write_text(json.dumps(FIG, indent=1, ensure_ascii=False, default=str))
    print(f'wrote {rel(a.out)} ({len(page.encode()) / 1e3:.0f} kB) and {len(files) - 1} images; {total / 1e6:.2f} MB in all')
    print('panels: ' + ', '.join(f'{k} {status_words(v)}' for k, v in STATUS.items()))
    print(f'{len(WARN)} warnings')
    if a.check:
        r = subprocess.run(['node', str(SCRIPTS2 / 'dataviz_check.js'), str(a.out), '--board', '--no-captures'], cwd=ROOT,
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
        print(r.stdout.strip()[-3000:])
        if r.returncode != 0:
            sys.exit(1)
    if WARN and a.strict:
        sys.exit(1)


LOG = set()
C = {}

if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
