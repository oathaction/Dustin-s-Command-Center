"""Read Dustin's saved Department of Labor state minimum wage history page and freeze its table (round 3 row 113).

Research lead's script, Phase 3 round 1 (download item 2, decision log D3-459). It imports nothing of the engineer's.

Usage:
    python3 -I work/build/scripts/phase-3/research_dol_freeze.py <saved page .htm> --explore <scratch dir>
    python3 -I work/build/scripts/phase-3/research_dol_freeze.py <saved page .htm> --freeze

The page is untrusted data. It is read only with Python's own HTML parser (html.parser), which runs no script and
fetches nothing; the contents of script, style and similar elements are skipped. The file's byte count and SHA-256
are checked against its download record (the .json beside it) before anything is parsed, and the script stops on a
mismatch. The structure is asserted (title, six tables, one heading row each, the same 55 rows in the same order,
every footnote mark defined in the page's key), so a different page stops the script instead of freezing wrong.

--explore writes a structure dump (every table's cells, with bold, and the text outside tables) to the scratch dir.
--freeze writes, in work/build/data/, and nothing else:
  dol-state-minimum-wage-history.csv        the publisher's table as published, one row per jurisdiction and year
  dol-state-minimum-wage-history.meta.json  its sidecar (contract C1)
  dol-state-minimum-wage-classes.csv        derived: data lead change 10's three classes, 50 states and DC, 2010 to 2024
  dol-state-minimum-wage-classes.meta.json  its sidecar
then reads both CSV files back and checks them against the parsed page.
"""
import collections
import csv
import decimal
import hashlib
import html.parser
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / 'work/build/data'
RETRIEVED = '2026-11-12'
LEDGER = 'P7-223'
PAGE_URL = 'https://www.dol.gov/agencies/whd/state/minimum-wage/history'
TITLE = ('Changes in Basic Minimum Wages in Non-Farm Employment Under State Law: Selected Years 1968 to 2024 '
         '| U.S. Department of Labor')
TABLE_TITLE = 'Changes in Basic Minimum Wages in Non-Farm Employment Under State Law: Selected Years 1968 to 2024'
FEDERAL = decimal.Decimal('7.25')
FEDERAL_DATE = 'July 24, 2009'
FIRST_CLASS_YEAR = 2010   # the first January 1 column after July 24, 2009 (data lead change 10)

CODE = {
    'Federal (FLSA)': 'US', 'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY',
    'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC', 'Guam': 'GU', 'Puerto Rico': 'PR', 'U.S. Virgin Islands': 'VI'}
STATES_AND_DC = [n for n in CODE if n not in ('Federal (FLSA)', 'Guam', 'Puerto Rico', 'U.S. Virgin Islands')]
MARK_RE = re.compile(r'[(\[]([^)\]]*)[)\]]')


def verify(page):
    rec = json.loads(page.with_suffix('.json').read_text(encoding='utf-8'))
    raw = page.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != rec['sha256'] or len(raw) != rec['bytes']:
        sys.exit(f'STOP: {page.name} is {len(raw)} bytes with SHA-256 {got}; its record says {rec["bytes"]} and {rec["sha256"]}')
    return raw, rec, got


class Reader(html.parser.HTMLParser):
    """Collects text by block, tables as rows of cells (with bold kept per cell), and the page title."""

    SKIP = {'script', 'style', 'noscript', 'template', 'svg', 'iframe', 'object'}
    BLOCK = {'p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'caption', 'dt', 'dd', 'section', 'article', 'br',
             'header', 'footer', 'ul', 'ol', 'blockquote'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.title = ''
        self.in_title = False
        self.tables = []
        self.stack = []
        self.cell = None
        self.bold = 0
        self.blocks = []
        self.buf = ''
        self.in_caption = False
        self.cap_buf = ''

    def flush(self):
        t = ' '.join(self.buf.split())
        if t and not self.stack:
            self.blocks.append(t)
        self.buf = ''

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        a = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag in self.BLOCK and not self.stack:
            self.flush()
        if tag == 'table':
            self.flush()
            self.stack.append({'rows': [], 'caption': '', 'summary': a.get('summary') or ''})
        elif tag == 'tr' and self.stack:
            self.stack[-1]['rows'].append([])
        elif tag in ('td', 'th') and self.stack:
            self.cell = {'tag': tag, 'text': '', 'bold_text': ''}
        elif tag in ('b', 'strong'):
            self.bold += 1
        elif tag == 'caption' and self.stack:
            self.in_caption = True
            self.cap_buf = ''
        elif tag == 'br' and self.cell is not None:
            self.cell['text'] += ' '

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == 'title':
            self.in_title = False
        elif tag in ('b', 'strong'):
            self.bold = max(0, self.bold - 1)
        elif tag in ('td', 'th') and self.cell is not None and self.stack:
            c = self.cell
            c['text'] = ' '.join(c['text'].split())
            c['bold_text'] = ' '.join(c['bold_text'].split())
            if not self.stack[-1]['rows']:
                self.stack[-1]['rows'].append([])
            self.stack[-1]['rows'][-1].append(c)
            self.cell = None
        elif tag == 'caption' and self.in_caption:
            self.in_caption = False
            self.stack[-1]['caption'] = ' '.join(self.cap_buf.split())
        elif tag == 'table' and self.stack:
            self.tables.append(self.stack.pop())
        elif tag in self.BLOCK and not self.stack:
            self.flush()

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_title:
            self.title += data
        if self.in_caption:
            self.cap_buf += data
        if self.cell is not None:
            self.cell['text'] += data
            if self.bold:
                self.cell['bold_text'] += data
        elif not self.stack:
            self.buf += data


def read_page(raw):
    r = Reader()
    r.feed(raw.decode('utf-8'))
    r.close()
    r.flush()
    return r


def explore(page, outdir):
    raw, rec, sha = verify(page)
    r = read_page(raw)
    outdir.mkdir(parents=True, exist_ok=True)
    dump = {'sha256': sha, 'title': ' '.join(r.title.split()), 'blocks': r.blocks,
            'tables': [{'summary': t['summary'], 'caption': t['caption'], 'rows': t['rows']} for t in r.tables]}
    (outdir / 'dol-structure.json').write_text(json.dumps(dump, ensure_ascii=False, indent=1), encoding='utf-8')
    print('title:', dump['title'])
    print('tables:', len(r.tables), [len(t['rows']) for t in r.tables])
    print('wrote', outdir / 'dol-structure.json')


# ---------------------------------------------------------------- reading the page into rows

def page_notes(blocks):
    """The page's sources, note, key and revision line, by position after the table title heading."""
    i = blocks.index('Sources:')
    j = blocks.index('Prepared By:')
    part = blocks[i:j]
    sources = [b for b in part if re.match(r'\d\) ', b)]
    note = part[part.index('Note:') + 1]
    key_lines = part[part.index('Key:') + 1:]
    key, label = {}, {}
    for line in key_lines:
        m = re.match(r'^(\.\.\.|N\.A\.|[(\[][a-z0-9]+[)\]]) - (.+)$', line)
        assert m, ('key line not read', line)
        k = m.group(1).strip('()[]') if m.group(1)[0] in '([' else m.group(1)
        key[k], label[k] = m.group(2), m.group(1)
    revised = [b for b in blocks if b.startswith('This document was last revised')]
    assert len(revised) == 1
    prepared = blocks[j + 1:j + 4]
    return {'sources': sources, 'note': note, 'key': key, 'label': label, 'revised': revised[0], 'prepared_by': prepared}


def marks_of(text):
    out = []
    for g in MARK_RE.findall(text):
        for p in re.split(r'[,\s]+', g):
            if p and p not in out:
                out.append(p)
    return out


def read_rate(text):
    """Return (cell_status, low, high, reading_note) for a published cell; numbers only where the cell reads plainly
    as hourly dollars, as Decimals."""
    core = MARK_RE.sub('', text).strip()
    if core == '...':
        return 'not applicable', None, None, ''
    if core == 'NA':
        return 'not available', None, None, ''
    if '/wk' in core:
        return 'range or two rates', None, None, 'weekly rate as printed (/wk), not an hourly rate'
    if '/day' in core:
        return 'one rate', None, None, 'daily rate as printed (/day), not an hourly rate'
    num = r'\$?(\d*\.\d\d)'
    m = re.fullmatch(num, core)
    if m:
        v = decimal.Decimal(m.group(1))
        return 'one rate', v, v, ''
    m = re.fullmatch(num + r'\s*(?:-|\u2013|/|&)\s*' + num, core)
    if m:
        lo, hi = decimal.Decimal(m.group(1)), decimal.Decimal(m.group(2))
        return 'range or two rates', min(lo, hi), max(lo, hi), ''
    return 'one rate' if '..' in core or '`' in core else 'unread', None, None, f'not read as a number: the page prints {core!r}'


def parse(raw):
    r = read_page(raw)
    title = ' '.join(r.title.split())
    assert title == TITLE, title
    assert TABLE_TITLE in r.blocks, 'table title heading not found'
    assert len(r.tables) == 6, len(r.tables)
    notes = page_notes(r.blocks)
    order = None
    cells = []
    years_seen = []
    for t in r.tables:
        head, body = t['rows'][0], t['rows'][1:]
        assert all(c['tag'] == 'th' for c in head) and head[0]['text'] == 'State or other jurisdiction'
        names = [row[0]['text'] for row in body]
        assert all(c['tag'] == 'td' for row in body for c in row)
        if order is None:
            order = names
            assert set(order) == set(CODE) and len(order) == 55, set(order) ^ set(CODE)
        assert names == order, 'row order differs between tables'
        for k, h in enumerate(head[1:], start=1):
            m = re.fullmatch(r'(\d{4})(?: \(([a-z])\))?', h['text'])
            assert m, h['text']
            year = int(m.group(1))
            assert year not in years_seen
            years_seen.append(year)
            for row in body:
                assert len(row) == len(head), (row[0]['text'], year)
                c = row[k]
                cells.append({'name': row[0]['text'], 'year': year, 'year_heading': h['text'], 'text': c['text'],
                              'bold': bool(c['bold_text']), 'bold_text': c['bold_text']})
    assert years_seen == sorted(years_seen)
    defined = set(notes['key']) - {'...', 'N.A.'}
    used = collections.Counter(m for c in cells for m in marks_of(c['text']))
    head_marks = collections.Counter(m for c in cells for m in marks_of(c['year_heading']))
    assert set(used) | set(head_marks) <= defined, set(used) - defined
    return {'title': title, 'order': order, 'years': years_seen, 'cells': cells, 'notes': notes, 'marks_used': used,
            'tables': r.tables}


# ---------------------------------------------------------------- words

def curl(line):
    """Set a printed line's apostrophes and double quotes curly (D3-175, D3-429)."""
    line = line.replace("'", '\u2019')
    line = re.sub(r'(^|[\s(\[])"', '\\1\u201c', line)
    return line.replace('"', '\u201d')


def dec(v):
    return '' if v is None else f'{v:.2f}'


def col(t, d, unit=None):
    o = {'type': t, 'description': d}
    if unit:
        o['unit'] = unit
    return o


def g_clause(g_note, state):
    """The clause of the page's note (g) that names one state, quoted as printed."""
    parts = [p.strip() for p in g_note.split(';')]
    hit = [p for p in parts if re.search(r'\b' + re.escape(state) + r'\b', p)]
    assert len(hit) == 1, (state, hit)
    p = hit[0]
    p = re.sub(r'^and ', '', p).rstrip('.')
    return p + '.'


# ---------------------------------------------------------------- the files

def spans(years):
    """'1981, 2001 to 2013, 2015 to 2024' from a sorted list of years."""
    out, start, last = [], None, None
    for y in years:
        if start is None:
            start = last = y
        elif y == last + 1:
            last = y
        else:
            out.append(f'{start}' if start == last else f'{start} to {last}')
            start = last = y
    if start is not None:
        out.append(f'{start}' if start == last else f'{start} to {last}')
    return ', '.join(out)


SHORT = {'above $7.25': 'above', 'at $7.25': 'at', 'below $7.25 or no state minimum': 'below or none'}


def as_of(year):
    return f'{year}-02' if year in (1968, 1972) else f'{year}-01-01'


def history_rows(P):
    rows = []
    for c in P['cells']:
        status, lo, hi, rnote = read_rate(c['text'])
        shown = c['text']
        if status == 'not available':
            assert shown == 'NA', shown
            shown, rnote = '', 'the page prints NA (not available); C1 keeps a missing value as an empty cell'
        rows.append({'code': CODE[c['name']], 'name': c['name'], 'year': str(c['year']), 'year_heading': c['year_heading'],
                     'as_of': as_of(c['year']), 'rate_as_published': shown, 'rate_low': dec(lo), 'rate_high': dec(hi),
                     'marks': '; '.join(marks_of(c['text'])), 'bold': 'true' if c['bold'] else 'false',
                     'cell_status': status, 'reading_note': rnote})
    order = {n: i for i, n in enumerate(P['order'])}
    rows.sort(key=lambda r: (order[r['name']], int(r['year'])))
    return rows


def class_rows(P, hist):
    key, label = P['notes']['key'], P['notes']['label']
    size_words = {m: key[m] for m in ('c', 'd', 'e')}
    size_words['d'] = key['d'].split('. ')[0].rstrip('.') + '.'   # the West Virginia sentence names no Georgia rule
    out = []
    for r in hist:
        y = int(r['year'])
        if r['name'] not in STATES_AND_DC or y < FIRST_CLASS_YEAR:
            continue
        marks = [m for m in r['marks'].split('; ') if m]
        quals = []
        if r['cell_status'] == 'not applicable':
            cls, basis = 'below $7.25 or no state minimum', 'no state rate on the page'
            quals.append('The page marks the state "..." (not applicable) and lists no state rate.')
        else:
            assert r['rate_high'], r
            hi = decimal.Decimal(r['rate_high'])
            cls = 'above $7.25' if hi > FEDERAL else 'at $7.25' if hi == FEDERAL else 'below $7.25 or no state minimum'
            basis = 'one rate' if r['cell_status'] == 'one rate' else 'highest rate of the range'
        for m in marks:
            if m in size_words:
                quals.append(f'Note {label[m]}: {size_words[m]}')
            elif m == 'g':
                quals.append(f'Note (g): {g_clause(key["g"], r["name"])}')
            else:
                raise AssertionError(('unhandled mark for a state', r))
        if r['cell_status'] == 'range or two rates' and 'g' not in marks:
            quals.append('The page prints two rates with no footnote; its note says a range reflects rates that differ '
                         'by industry, occupation or other factors.')
        out.append({'code': r['code'], 'name': r['name'], 'year': r['year'], 'as_of': r['as_of'],
                    'rate_as_published': r['rate_as_published'], 'rate_low': r['rate_low'], 'rate_high': r['rate_high'],
                    'marks': r['marks'], 'class': cls, 'class_basis': basis,
                    'lower_rate_noted': 'true' if (r['cell_status'] == 'range or two rates' or 'g' in marks) else 'false',
                    'employer_size_limit': 'true' if any(m in size_words for m in marks) else 'false',
                    'qualification': ' '.join(quals)})
    return out


def write_csv(path, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    text = buf.getvalue()
    for bad in ('\u2014', '\u2011'):
        assert bad not in text, (path.name, bad)
    path.write_bytes(text.encode('utf-8'))


def write_meta(path, meta):
    meta['printed_source_line'] = curl(meta['printed_source_line'])
    if 'source_line_variants' in meta:
        meta['source_line_variants'] = {k: curl(v) for k, v in meta['source_line_variants'].items()}
    txt = json.dumps(meta, ensure_ascii=False, indent=1)
    assert '\u2014' not in txt and '\u2011' not in txt and 'isclos' not in txt, path.name
    path.write_text(txt + '\n', encoding='utf-8')


def counts(rows, year):
    c = collections.Counter(r['class'] for r in rows if int(r['year']) == year)
    return {k: c.get(k, 0) for k in ('above $7.25', 'at $7.25', 'below $7.25 or no state minimum')}


def freeze(page):
    raw, rec, sha = verify(page)
    P = parse(raw)
    notes = P['notes']
    key, label = notes['key'], notes['label']
    hist = history_rows(P)
    assert not [r for r in hist if r['cell_status'] == 'unread'], 'a cell the reader does not know'
    assert len(hist) == 55 * len(P['years']), len(hist)
    fed = {int(r['year']): r for r in hist if r['code'] == 'US'}
    assert fed[2009]['rate_high'] == '6.55' and all(fed[y]['rate_high'] == '7.25' for y in P['years'] if y >= 2010)
    assert re.search(r'Wage rates are for January 1 of each year except 1968 and 1972, which show rates as of February\.', notes['note'])
    cls = class_rows(P, hist)
    class_years = [y for y in P['years'] if y >= FIRST_CLASS_YEAR]
    assert class_years == list(range(2010, 2025)), class_years
    assert len(cls) == 51 * len(class_years)

    # bold against the published values: the note says bold marks an increase over the previous year's rate
    # compared with the previous column the page lists (for 1970 to 1998 that column can be several years back)
    by_cell = {(r['code'], int(r['year'])): r for r in hist}
    prev_year = dict(zip(P['years'][1:], P['years'][:-1]))
    bold_agree, bold_off = 0, collections.Counter()
    for r in hist:
        y = int(r['year'])
        if y not in prev_year:
            continue
        q = by_cell[(r['code'], prev_year[y])]
        if not (r['rate_high'] and q['rate_high']):
            continue
        rose = (decimal.Decimal(r['rate_high']) > decimal.Decimal(q['rate_high'])
                or decimal.Decimal(r['rate_low']) > decimal.Decimal(q['rate_low']))
        if rose == (r['bold'] == 'true'):
            bold_agree += 1
        else:
            bold_off[y] += 1
    bold_years = sorted({int(r['year']) for r in hist if r['bold'] == 'true'})
    bold_before_2001 = sum(1 for r in hist if r['bold'] == 'true' and int(r['year']) < 2001)
    bold_disagree = [f'{y}: {n}' for y, n in sorted(bold_off.items())]

    g_states = sorted({r['name'] for r in cls if 'g' in r['marks'].split('; ')})
    ranges_unmarked = sorted({f"{r['name']} {r['year']} ({r['rate_as_published']})" for r in cls
                              if r['lower_rate_noted'] == 'true' and 'g' not in r['marks'].split('; ')})
    um = collections.defaultdict(list)
    for r in cls:
        if r['lower_rate_noted'] == 'true' and 'g' not in r['marks'].split('; '):
            um[r['name']].append(int(r['year']))
    unmarked_spans = [f'{n} {spans(sorted(ys))}' for n, ys in sorted(um.items())]
    size = collections.defaultdict(list)
    for r in cls:
        for m in r['marks'].split('; '):
            if m in ('c', 'd', 'e'):
                size[(r['name'], m)].append(int(r['year']))
    size_lines = [f'{n} {label[m]}, {min(ys)} to {max(ys)}' if len(ys) > 1 else f'{n} {label[m]}, {ys[0]}' for (n, m), ys in sorted(size.items())]
    for (n, m), ys in size.items():
        assert ys == list(range(min(ys), max(ys) + 1)), (n, m, ys)
    none_states = sorted({r['name'] for r in cls if r['class_basis'] == 'no state rate on the page'})
    none_all_years = all(sum(1 for r in cls if r['name'] == n and r['class_basis'] == 'no state rate on the page') == len(class_years) for n in none_states)
    below = collections.defaultdict(list)
    for r in cls:
        if r['class'].startswith('below') and r['class_basis'] != 'no state rate on the page':
            below[r['name']].append((int(r['year']), r['rate_as_published']))
    below_states = []
    for n, ys in sorted(below.items()):
        yrs = [y for y, _ in ys]
        assert yrs == list(range(min(yrs), max(yrs) + 1)), (n, yrs)
        rates = sorted({v for _, v in ys})
        below_states.append(f'{n} {min(yrs)}' + (f' to {max(yrs)}' if len(yrs) > 1 else '') + f' ({", ".join(rates)})')
    year_counts = {y: counts(cls, y) for y in class_years}
    cls_by = {(r['code'], int(r['year'])): r['class'] for r in cls}
    codes = sorted({r['code'] for r in cls})
    moves = []
    for y in class_years[1:]:
        for k in codes:
            if cls_by[(k, y)] != cls_by[(k, y - 1)]:
                moves.append((y, k, cls_by[(k, y - 1)], cls_by[(k, y)]))
    same_2015_2020 = all(cls_by[(k, 2015)] == cls_by[(k, 2020)] for k in codes)
    panel_counts = {y: counts(cls, y) for y in (2010, 2015, 2020, 2024)}
    wv_marked = [r for r in cls if r['code'] == 'WV' and r['marks']]

    raw_name = page.name
    vintage = (f'The page as Dustin Cathcart saved it from dol.gov and attached it on November 12, 2026 (download item 2, '
               f'D3-459), {rec["bytes"]} bytes, SHA-256 {sha}. The page says "{notes["revised"]}"')
    sources_words = ' '.join(notes['sources'])
    key_words = '; '.join(f'{label[k]} - {v}' for k, v in key.items())
    slips = [f"{r['name']} {r['year']}, {r['rate_as_published']!r}" for r in hist if r['reading_note'] and 'not read' in r['reading_note']]
    nonhourly = [f"{r['name']} {r['year']}, {r['rate_as_published']!r}" for r in hist if r['reading_note'] and 'not an hourly' in r['reading_note']]
    en_dash = sorted({r['name'] for r in hist if '\u2013' in r['rate_as_published']})
    na_cells = [f"{r['name']} {r['year']}" for r in hist if r['cell_status'] == 'not available']
    common_quals = [
        f'The page\'s note: "{notes["note"]}"',
        f'The page\'s sources: {sources_words}',
        f'The page\'s key, as printed: {key_words}',
        'The page gives each state\'s basic rate under state law for non-farm employment. It lists no tipped, youth, '
        'training or farm rates and no city or county minimums, so none is in these files.',
        'Wherever a state rate is below the federal rate, or a state has none, employers the federal law covers pay the '
        'federal rate; Atlas V7 claim CL1516, from the Department of Labor\'s state page of July 1, 2026, says the same '
        '("where the federal rate applies to covered employers") and that federal coverage "depends on employer size and '
        'interstate commerce".',
    ]

    hist_cols = {
        'code': col('code', 'USPS code of the jurisdiction; US for the federal row'),
        'name': col('text', 'the jurisdiction as the page names it ("Federal (FLSA)" for the federal rate)'),
        'year': col('year', 'the column\'s year'),
        'year_heading': col('text', 'the column heading as printed, footnote mark included ("1968 (a)")'),
        'as_of': col('text', 'the column\'s as-of day per the page\'s note: YYYY-MM-DD for January 1; YYYY-MM for 1968 and 1972, which the page dates to February only'),
        'rate_as_published': col('text', 'the cell exactly as the page displays it, footnote marks included, runs of white space as one space; empty where the page prints NA (see cell_status)'),
        'rate_low': col('number', 'the lower (or only) hourly rate read from the cell; empty where the page prints no hourly rate (see cell_status and reading_note)', 'dollars per hour'),
        'rate_high': col('number', 'the higher (or only) hourly rate read from the cell', 'dollars per hour'),
        'marks': col('text', 'the cell\'s footnote marks, letters only, joined by "; " (the key is in the sidecar\'s qualification)'),
        'bold': col('boolean', 'true where the page sets the rate in bold, which its note says marks an increase over the previous year\'s rate'),
        'cell_status': col('category', 'one rate; range or two rates (a dash, en dash, slash or ampersand between two rates); not applicable (the page\'s "..."); not available (the page prints NA)'),
        'reading_note': col('text', 'why a cell has no number: a weekly or daily rate, characters the script does not read as a number, or the page\'s NA'),
    }
    hist_meta = {
        'file': 'dol-state-minimum-wage-history.csv',
        'kind': 'public',
        'publisher': 'U.S. Department of Labor, Wage and Hour Division',
        'title_or_table': TABLE_TITLE,
        'table_id': 'WHD state minimum wage history table (six tables on one page: 1968 to 1981, 1988 to 1998, 2000 to 2006, 2007 to 2013, 2014 to 2019, 2020 to 2024)',
        'url': [PAGE_URL],
        'observation_period': f'Selected years 1968 to 1998 and every year 2000 to 2024 ({len(P["years"])} columns), each as of January 1 except 1968 and 1972 (February)',
        'geography': 'The federal rate (code US), 50 states, the District of Columbia, Guam, Puerto Rico and the U.S. Virgin Islands (55 rows a year)',
        'universe_or_base': 'Basic minimum wage rates in non-farm employment under each state\'s law, and the federal rate under the Fair Labor Standards Act',
        'unit': 'dollars per hour (rate_low and rate_high); the published cell text kept beside them',
        'date_retrieved': RETRIEVED,
        'vintage': vintage,
        'qualification': ' '.join(common_quals[:2] + [common_quals[3]]) + ' Some rates apply only to employers above a size, and a range means rates that differ by employer, industry or occupation; the key gives each mark\'s words.',
        'columns': hist_cols,
        'printed_source_line': ('Source: U.S. Department of Labor, Wage and Hour Division, Changes in Basic Minimum Wages in Non-Farm '
                                'Employment Under State Law: Selected Years 1968 to 2024, rates as of January 1 (February in 1968 '
                                'and 1972), federal, 50 states, DC, Guam, Puerto Rico and the U.S. Virgin Islands. Retrieved '
                                'November 12, 2026. State law only; some rates apply only to larger employers.'),
        'source_line_variants': {
            'states_and_dc_2010_to_2024': ('Source: U.S. Department of Labor, Wage and Hour Division, Changes in Basic Minimum '
                                           'Wages in Non-Farm Employment Under State Law, rates as of January 1, 2010 to 2024, '
                                           '50 states and DC. Retrieved November 12, 2026. State law only; some rates apply '
                                           'only to larger employers.'),
        },
        'ledger_row': LEDGER,
        'domain': 'D07',
        'domain_note': 'V7 I104, "A fixed minimum wage buys less every year", in work, pay and bargaining power',
        'states': [],
        'breaks_in_series': f'The page\'s sources change in 2000: {sources_words}',
        'raw_files_sha256_prefix': {raw_name: sha[:16]},
        'notes': [f'The page\'s key, as printed: {label[k]} - {v}' for k, v in key.items()] + [
            'Every footnote mark in a cell is one the key defines (asserted by the script). Marks as used: '
            + ', '.join(f'{label[m]} {n} cell' + ('s' if n != 1 else '') for m, n in sorted(P['marks_used'].items())) + '; the 1968, 1970 and 1976 headings carry (a).',
            'The latest column is 2024 (January 1, 2024), and the page has no 2025 or 2026 column. Its title reads "Selected Years 1968 to 2024", '
            f'and its last line reads "{notes["revised"]}" The download record\'s "1961" and "2025" come from note (a) and that line.',
            'Cells kept as the page prints them. Not read as a number (rate_low and rate_high empty): ' + '; '.join(slips) + '. '
            'Weekly or daily rates, kept as text with no hourly number: ' + '; '.join(nonhourly) + '. '
            'Ranges printed with an en dash: ' + ', '.join(en_dash) + '. '
            'The page prints NA (not available) in ' + '; '.join(na_cells) + '; contract C1 keeps a missing value as an empty cell, so rate_as_published is empty there and cell_status reads "not available".',
            f'Bold, kept as published, against the page\'s note: compared with the previous column the page lists, {bold_agree} cells agree (bold where a rate rose, plain where none did) '
            f'and {sum(bold_off.values())} do not. The page sets bold only in {spans(bold_years)} ({bold_before_2001} cells before 2001), so nearly every rise before 2001, and every rise in 2014, is plain; '
            'cells that disagree, by column: ' + '; '.join(bold_disagree) + '. Read a change from the rates, not the bold.',
            'Note (g)\'s dollar amounts and dates end at January 1, 2005, but the page still marks later cells (g) for Minnesota, Montana and Oklahoma, and those cells print their own lower rate where they print a range.',
            'Note (d) names West Virginia, but no West Virginia cell from 2010 to 2024 carries a mark.' if not wv_marked else 'West Virginia carries (d) in some cells from 2010.',
        ],
    }

    cls_cols = {
        'code': col('code', 'USPS state code'),
        'name': col('text', 'state name as the page prints it'),
        'year': col('year', 'the column\'s year'),
        'as_of': col('date', 'January 1 of the year, the page\'s as-of day for every column from 1976 on'),
        'rate_as_published': col('text', 'the cell exactly as the page displays it, footnote marks included'),
        'rate_low': col('number', 'the lower (or only) hourly rate in the cell', 'dollars per hour'),
        'rate_high': col('number', 'the higher (or only) hourly rate in the cell; the class is read from it', 'dollars per hour'),
        'marks': col('text', 'the cell\'s footnote marks, letters only, joined by "; "'),
        'class': col('category', 'data lead change 10\'s three classes: above $7.25; at $7.25; below $7.25 or no state minimum'),
        'class_basis': col('category', 'one rate; highest rate of the range; no state rate on the page'),
        'lower_rate_noted': col('boolean', 'true where the cell prints two rates or carries note (g), which names a lower rate for smaller employers'),
        'employer_size_limit': col('boolean', 'true where the cell carries note (c), (d) or (e): the rate applies only to employers of four, six or two or more'),
        'qualification': col('text', 'the page\'s words for each mark in the cell, quoted, and the range or "..." reading; empty where the cell carries none'),
    }
    c10 = panel_counts[2010]
    c24 = panel_counts[2024]
    cls_meta = {
        'file': 'dol-state-minimum-wage-classes.csv',
        'kind': 'derived',
        'publisher': 'U.S. Department of Labor, Wage and Hour Division',
        'title_or_table': TABLE_TITLE + ', columns 2010 to 2024, each state classed against the federal $7.25',
        'table_id': 'WHD state minimum wage history table, tables for 2007 to 2013, 2014 to 2019 and 2020 to 2024',
        'url': [PAGE_URL],
        'observation_period': 'January 1 of each year, 2010 to 2024 (the first January 1 after the federal $7.25 took effect on July 24, 2009, to the page\'s latest column)',
        'geography': '50 states and the District of Columbia (51 rows a year)',
        'universe_or_base': 'Each state\'s basic minimum wage under state law for non-farm employment, as the page lists it',
        'unit': 'dollars per hour; class is a category',
        'date_retrieved': RETRIEVED,
        'vintage': vintage,
        'qualification': ('Classes by Oath & Action from the highest rate each cell prints: above $7.25, at $7.25, or below $7.25 or no '
                          'state minimum (the page\'s "..."). A state whose cell prints two rates has a lower rate for some employers '
                          'or workers (lower_rate_noted), and some rates apply only to employers above a size (employer_size_limit); '
                          'each row quotes the page\'s note for its marks. ' + common_quals[4] + ' ' + common_quals[3]),
        'columns': cls_cols,
        'printed_source_line': ('Source: U.S. Department of Labor, Wage and Hour Division, Changes in Basic Minimum Wages in Non-Farm '
                                'Employment Under State Law, rates as of January 1, 2010 to 2024, 50 states and DC. Retrieved '
                                'November 12, 2026. Classes by Oath & Action from each state\'s highest listed rate; some rates '
                                'apply only to larger employers, and where a state is below $7.25 or has none, covered employers pay '
                                'the federal rate.'),
        'source_line_variants': {
            'panels_2010_2015_2020_2024': ('Source: U.S. Department of Labor, Wage and Hour Division, Changes in Basic Minimum '
                                           'Wages in Non-Farm Employment Under State Law, rates as of January 1, 2010, 2015, 2020 '
                                           'and 2024, 50 states and DC. Retrieved November 12, 2026. Classes by Oath & Action from '
                                           'each state\'s highest listed rate; some rates apply only to larger employers, and where '
                                           'a state is below $7.25 or has none, covered employers pay the federal rate.'),
        },
        'ledger_row': LEDGER,
        'domain': 'D07',
        'domain_note': 'V7 I104, "A fixed minimum wage buys less every year", in work, pay and bargaining power',
        'states': [],
        'derived_from': ['dol-state-minimum-wage-history.csv'],
        'derivation': ('For each state and DC in each January 1 column from 2010 to 2024, the class of the highest hourly rate the '
                       'cell prints against the federal $7.25 (a cell marked "..." classed with below), with flags and the page\'s '
                       'note words for every footnote mark and range.'),
        'which_vintage_to_chart': ('Panels at one as-of day after July 24, 2009 (data lead change 10): any January 1 from 2010 to 2024. '
                                   'The page has no 2025 or 2026 column; its latest is January 1, 2024.'),
        'raw_files_sha256_prefix': {raw_name: sha[:16]},
        'notes': [
            'Counts by class, January 1, of 51: ' + '; '.join(
                f'{y}: {c["above $7.25"]} above, {c["at $7.25"]} at, {c["below $7.25 or no state minimum"]} below or none'
                for y, c in year_counts.items()) + '.',
            'Every change of class from one January 1 to the next (above, at, or below or none): ' + '; '.join(
                f'{y} {k}, {SHORT[a]} to {SHORT[b]}' for y, k, a, b in moves) + '. '
            + ('No state changes class between 2015 and 2020, so panels for those two years look the same.' if same_2015_2020 else ''),
            f'Below $7.25 with a state rate: {"; ".join(below_states)}.',
            f'Marked "..." in every column from 2010 to 2024: {", ".join(none_states)}. The page\'s key reads "... - not applicable"; '
            'it does not say "no law". Atlas V7 claim CL1516 counts five states with no minimum wage law on the Department of Labor\'s state page of July 1, 2026, without naming them in the claim.'
            if none_all_years else f'Marked "..." in some columns: {", ".join(none_states)}.',
            f'Cells with note (g), a lower rate for smaller employers: {", ".join(g_states)}.',
            'Two rates with no footnote: ' + '; '.join(unmarked_spans) + '. The page gives no reason for these; its note says a range reflects rates that differ by industry, occupation or other factors.',
            'Employer-size limits: ' + '; '.join(size_lines) + '. Their words: ' + '; '.join(f'{label[m]} {key[m].rstrip(".")}' for m in ('c', 'd', 'e')) + '.',
            'The class reads the highest rate a cell prints. For a cell with note (g), that is the rate for employers above the size the note names; for Nevada\'s and Ohio\'s unmarked pairs the page gives no reason. '
            'A maker who shows the lower tier reads rate_low and lower_rate_noted.',
            'January 1, 2024\'s counts equal Atlas V7 claim CL1516\'s for July 1, 2026: 30 states and DC above $7.25, 13 at $7.25, Georgia and Wyoming at $5.15 and five with no state rate. '
            'Equal counts do not show that the same states sit in each class.' if (c24['above $7.25'], c24['at $7.25'], c24['below $7.25 or no state minimum']) == (31, 13, 7) else
            'January 1, 2024\'s counts differ from Atlas V7 claim CL1516\'s for July 1, 2026.',
            'No July 1, 2026 column: the July 1, 2026 state table that chapter 01 cites (Atlas V7 source K1508, "State Minimum Wage Laws", accessed October 15, 2026) is not frozen in the data folder; '
            'V7 keeps only its counts (claim CL1516: 30 states and DC above $7.25, 13 at $7.25, Georgia and Wyoming at $5.15, five with no minimum wage law).',
        ],
    }

    hp, cp = OUT / 'dol-state-minimum-wage-history.csv', OUT / 'dol-state-minimum-wage-classes.csv'
    write_csv(hp, hist)
    write_meta(OUT / 'dol-state-minimum-wage-history.meta.json', hist_meta)
    write_csv(cp, cls)
    write_meta(OUT / 'dol-state-minimum-wage-classes.meta.json', cls_meta)

    # read back: every published cell, in order, and the classes recomputed from the frozen history file
    with hp.open(encoding='utf-8', newline='') as f:
        back = list(csv.DictReader(f))
    by_cell = {(c['name'], c['year']): c['text'] for c in P['cells']}
    assert len(back) == len(P['cells'])
    assert all(b['rate_as_published'] == by_cell[(b['name'], int(b['year']))] or (b['cell_status'] == 'not available' and
               by_cell[(b['name'], int(b['year']))] == 'NA' and b['rate_as_published'] == '') for b in back)
    assert hp.read_bytes()[:3] != b'\xef\xbb\xbf'
    with cp.open(encoding='utf-8', newline='') as f:
        cback = list(csv.DictReader(f))
    hist_by = {(b['code'], b['year']): b for b in back}
    for b in cback:
        h = hist_by[(b['code'], b['year'])]
        assert b['rate_as_published'] == h['rate_as_published'] and b['rate_high'] == h['rate_high']
        if h['cell_status'] == 'not applicable':
            want = 'below $7.25 or no state minimum'
        else:
            v = decimal.Decimal(h['rate_high'])
            want = 'above $7.25' if v > FEDERAL else 'at $7.25' if v == FEDERAL else 'below $7.25 or no state minimum'
        assert b['class'] == want, b
    print(f'{hp.relative_to(ROOT)}: {len(back)} rows, {len(P["years"])} years, 55 jurisdictions')
    print(f'{cp.relative_to(ROOT)}: {len(cback)} rows, years {class_years[0]} to {class_years[-1]}, 51 states and DC')
    for y, c in panel_counts.items():
        print(f'  January 1, {y}: {c}')
    print('  class moves:', len(moves), '; 2015 and 2020 the same:', same_2015_2020)
    print('  bold agrees', bold_agree, 'disagrees', sum(bold_off.values()), 'by column', dict(bold_off))
    print('  unmarked two-rate cells:', ranges_unmarked)
    print('  below with a state rate:', below_states)
    print('  read back: every published cell equal; every class recomputed from the frozen file equal')


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    page = pathlib.Path(sys.argv[1]).resolve()
    if sys.argv[2] == '--explore' and len(sys.argv) == 4:
        explore(page, pathlib.Path(sys.argv[3]).resolve())
    elif sys.argv[2] == '--freeze':
        freeze(page)
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
