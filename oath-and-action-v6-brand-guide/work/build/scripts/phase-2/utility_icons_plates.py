#!/usr/bin/env python3
"""Plate page for the utility icons, stage B round 1 (icon designer, utility hand, November 9, 2026).

Reads the SVG masters and manifest in work/build/assets/utility-icons/, the check results in its qa/ folder and the
Civic Line black and newsprint masters (read only), and writes
work/boards/phase-2/stage-b/drawings/utility/20261109_Utility-Icons-Plates.html for the board builder to capture.

Every option is shown at 24 and 16 px on Newsprint and Charcoal at true size, then at 2x, with its word in use, the
naming reading at 24 px and the two checks' figures. Glyphs are inline SVG symbols in currentColor, laid out on whole
CSS pixels so a capture at device scale 1 shows the reader's pixels.

Usage: python3 -I work/build/scripts/phase-2/utility_icons_plates.py
"""
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
ASSETS = os.path.join(ROOT, 'work', 'build', 'assets', 'utility-icons')
QA = os.path.join(ASSETS, 'qa')
CL = os.path.join(ROOT, 'work', 'build', 'assets', 'civic-line')
OUT_DIR = os.path.join(ROOT, 'work', 'boards', 'phase-2', 'stage-b', 'drawings', 'utility')
OUT = os.path.join(OUT_DIR, '20261109_Utility-Icons-Plates.html')

# ---------- the designer's readings and recommendations ----------
# Naming test: each option drawn at 24 px with no label; what a first-time reader would most likely call it.
# Y names the subject, P names it among other readings or names a near subject, N names something else.
NAMING = {
    'close': {'A': ('Y', 'Close.'), 'B': ('P', 'Close or clear; also reads as a cancel badge.'),
              'C': ('P', 'Close the window; may read as a box marked no.')},
    'menu': {'A': ('Y', 'Menu.'), 'B': ('Y', 'Menu.'), 'C': ('N', 'Text, or align left.')},
    'arrow': {'A': ('Y', 'Next, or go forward.'), 'B': ('Y', 'Next, or go; reads as a button.'),
              'C': ('Y', 'Next, or continue.')},
    'chevron': {'A': ('Y', 'Show more, or open the list.'), 'B': ('Y', 'Show more, or scroll down.'),
                'C': ('P', 'Open the list; small and light beside a word.')},
    'download': {'A': ('Y', 'Download.'), 'B': ('Y', 'Download, or save.'), 'C': ('P', 'Download, or move down.')},
    'another-site': {'A': ('Y', 'Open somewhere else, or open in a new tab.'),
                     'B': ('P', 'Up and to the right; may read as trending up.'),
                     'C': ('N', 'Share, or export.')},
    'search': {'A': ('Y', 'Search.'), 'B': ('Y', 'Search, or a magnifying glass.'), 'C': ('P', 'Search, or zoom.')},
    'filter': {'A': ('Y', 'Filter.'), 'B': ('Y', 'Filter.'), 'C': ('P', 'Filter; may read as a glass.')},
    'copy': {'A': ('Y', 'Copy, or duplicate.'), 'B': ('Y', 'Copy, or pages.'), 'C': ('P', 'Copy text, or documents.')},
    'play': {'A': ('Y', 'Play.'), 'B': ('Y', 'Play.'), 'C': ('P', 'Play the video.')},
    'pause': {'A': ('Y', 'Pause.'), 'B': ('Y', 'Pause.'), 'C': ('P', 'Pause the video.')},
    'reset': {'A': ('N', 'Refresh, or reload.'), 'B': ('Y', 'Undo, or reset.'), 'C': ('P', 'Undo, or turn left.')},
    'error': {'A': ('Y', 'Error, or alert.'), 'B': ('Y', 'Stop, or error.'), 'C': ('P', 'Notice, or important.')},
    'success': {'A': ('Y', 'Done, or success.'), 'B': ('Y', 'Done, or success.'),
                'C': ('N', 'A ticked box: selected, more than success.')},
    'check': {'A': ('Y', 'Check, or done.'), 'B': ('Y', 'Check, or tick.'),
              'C': ('P', 'Check, though near the chevron at this size.')},
    'full-size': {'A': ('Y', 'Full screen, or expand.'), 'B': ('Y', 'Expand; busy at 16 px.'),
                  'C': ('P', 'Expand, or resize; near the outside-link arrow.')},
    'sort': {'A': ('Y', 'Sort, or swap.'), 'B': ('P', 'Sort, or choose from a list.'),
             'C': ('N', 'Move up and down, or resize.')},
    'warning': {'A': ('Y', 'Warning, or caution.'), 'B': ('Y', 'Warning; the road sign.'),
                'C': ('Y', 'Warning, or caution.')},
}

REC = {
    'close': ('A', 'The plain cross is the sign readers look for. The enclosed crosses read near Error and measure as near twins of the other enclosed options.'),
    'menu': ('A', 'The phone convention, as the shell draws it today. B sits on the watch line against CL-012 Election Rules, and C reads as text.'),
    'arrow': ('A', 'The arrow readers know. It turns cleanly for Previous and the sort order, and its head matches the sort arrows.'),
    'chevron': ('A', 'Clear at both sizes, and apart from the arrow, which keeps its shaft.'),
    'download': ('A', 'The tray is the download sign readers know best. B is the choice if you want the most distance from CL-001 Voting.'),
    'another-site': ('A', 'The box with an arrow leaving its corner is the known sign, and it leaves by the corner, as the audit asks, so it stays apart from CL-001 Voting.'),
    'search': ('A', 'The plain magnifier. The glint in B brings it closer to CL-023 Evidence, and C reads as zoom.'),
    'filter': ('A', 'The funnel readers know. The slanted spout keeps it from reading as a glass.'),
    'copy': ('A', 'Two sheets read as Copy at both sizes. The text lines in C crowd at 16 px.'),
    'play': ('A', 'Pick Play and Pause as a pair, by letter. The plain triangle and bars read at once; the enclosed pairs measure as near twins of each other, and C says video.'),
    'pause': ('A', 'Pick with Play, by letter. Its watch figure against CL-012 Election Rules is a blurred-shape match; side by side the two do not read alike.'),
    'reset': ('B', 'It reads as undo or reset, its upright head sits on whole pixels, and it is the furthest from CL-024 Feedback Loop. A reads as refresh.'),
    'error': ('A', 'The circle the audit asks for, apart from the Warning triangle and from the bare Close cross.'),
    'success': ('B', 'The check leaving an open circle stays apart from the closed check badges in Civic Line and from a ticked box. C reads as a checkbox.'),
    'check': ('A', 'The proportions readers know. C measures close to the chevron.'),
    'full-size': ('A', 'Four corners are the video sign for filling the screen. B blurs at 16 px, and C is near the outside-link arrow.'),
    'sort': ('A', 'The two arrows share the head of the Next arrow, which turns to show the order in use. B borrows the chevron, and C reads as resize.'),
    'warning': ('A', 'The wide triangle is the warning shape readers know. Ink only, never red.'),
}

# The word each glyph sits beside, from the accessibility audit's examples. (kind, words)
SPECIMEN = {
    'close': ('button', 'Close'), 'menu': ('button', 'Menu'), 'arrow': ('next', 'Next step'),
    'chevron': ('row', 'The lines in words'), 'download': ('button', 'Download tokens.css'),
    'another-site': ('inline', 'The bill and its record are on congress.gov'), 'search': ('button', 'Search'),
    'filter': ('button', 'Filters, 2 on'), 'copy': ('button', 'Copy #121212, Charcoal'),
    'play': ('button', 'Play'), 'pause': ('button', 'Pause'), 'reset': ('button', 'Reset the loop'),
    'error': ('line', 'Enter a ZIP code with five digits.'), 'success': ('line', 'Copied 12 lines to the clipboard.'),
    'check': ('chip', 'Housing'), 'full-size': ('button', 'View the map full size'), 'sort': ('heading', 'Date'),
    'warning': ('line', 'Checked October 15, 2026. The agency may have acted since.'),
}

# Civic Line drawings the audit names as threats to each glyph (section 1.4), shown beside the options.
THREATS = {
    'reset': ['CL-024'], 'search': ['R-44', 'CL-020', 'CL-023'], 'another-site': ['CL-001'],
    'filter': ['CL-012', 'CL-071', 'R-37'], 'error': ['R-35'], 'close': ['R-35'],
    'success': ['CL-003', 'CL-018', 'R-01'], 'check': ['R-01', 'R-34'], 'warning': ['CL-033', 'CL-037'],
    'sort': ['CL-060', 'R-44'], 'menu': ['CL-012', 'CL-039', 'R-02'], 'pause': ['CL-012'], 'download': ['CL-001', 'CL-048'],
}


# ---------- data ----------
def load(name):
    with open(os.path.join(QA, name)) as fh:
        return json.load(fh)


manifest = json.load(open(os.path.join(ASSETS, '20261109_Utility-Icons-Manifest.json')))
pf = {}
for size, name in (('24', '20261109_Utility-Pixel-Fit-24px.json'), ('16', '20261109_Utility-Pixel-Fit-16px.json')):
    for r in load(name)['results']:
        pf[os.path.basename(r['file'])] = r
lik_all = load('20261109_Utility-Likeness-All-Pairs-24px.json')
lik = load('20261109_Utility-Likeness.json')
FLAG = lik['thresholds']['flag']['likeness']
WATCH = lik['thresholds']['watch']['likeness']


def base(rel):
    return os.path.basename(rel)


closest = {c['a']: c for c in lik['closest']}
pairs_master = {}
pairs_new = []
for p in lik_all['flagged'] + lik_all['watch']:
    if p['against'] == 'master':
        pairs_master[(p['a'], p['b'].split(' ')[0])] = p
    elif p['against'] == 'new':
        pairs_new.append(p)


def subject(fname):
    return re.sub(r'-Option-[ABC]-\d+px\.svg$', '', fname.replace('20261109_Utility-', ''))


def nearest_in_set(fname):
    best = None
    for p in pairs_new:
        if fname not in (p['a'], p['b']):
            continue
        other = p['b'] if p['a'] == fname else p['a']
        if subject(other) == subject(fname) or '24px' not in other:
            continue
        if best is None or p['likeness'] > best[0]:
            best = (p['likeness'], other, p['percentile'])
    return best


# Civic Line masters, read only, inlined in currentColor.
cl_files = {}
for fn in os.listdir(os.path.join(CL, 'black')):
    m = re.search(r'Civic-Line-((?:CL|R)-\d+)-(.+)-Black\.svg$', fn)
    if m:
        cl_files[m.group(1)] = (fn, m.group(2).replace('-', ' '))


def cl_symbol(cid):
    fn, _ = cl_files[cid]
    s = open(os.path.join(CL, 'black', fn)).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<title>.*?</title>|<desc>.*?</desc>', '', s, flags=re.S)
    s = re.sub(r'\sid="[^"]*"', '', s)
    s = s.replace('#121212', 'currentColor').replace('#000000', 'currentColor').replace('#FFFFFF', 'var(--cut)')
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    return '<symbol id="cl-%s" viewBox="%s">%s</symbol>' % (cid.lower(), vb, inner.strip())


def u_symbol(key, opt, size, rel):
    s = open(os.path.join(ASSETS, rel)).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1).strip()
    w = '2' if size == '24' else '1.5'
    return ('<symbol id="u-%s-%s-%s" viewBox="0 0 %s %s"><g fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g></symbol>') % (key, opt, size, size, size, w, inner)


def use(sym, px, extra=''):
    return ('<svg class="g" width="%d" height="%d" aria-hidden="true" focusable="false"%s><use href="#%s"/></svg>'
            % (px, px, extra, sym))


def e(t):
    return html.escape(t, quote=True)


def pct(p):
    n = int(round(p))
    suffix = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return '%d%s' % (n, suffix)


def pf_line(fname):
    r = pf[fname]
    s1 = r['scales']['1x']
    st = s1['straight']
    out = 'pass' if r['pass'] else 'fail'
    straight = ('%d of %d straight strokes on the pixel grid' % (st['fit'], st['total'])) if st['total'] else 'no straight strokes'
    return '%s; %s; %d%% soft pixels at 1x' % (out, straight, round(s1['soft_edges']['share'] * 100))


def lik_word(v):
    if v >= FLAG:
        return 'flag'
    if v >= WATCH:
        return 'watch'
    return 'clear'


# ---------- page ----------
symbols = []
cards = []
rec_syms = []
for a in manifest:
    key = a['key']
    rec_opt, rec_why = REC[key]
    opts_html = []
    for o in a['options']:
        opt = o['option']
        f24, f16 = base(o['files']['24']), base(o['files']['16'])
        s24, s16 = 'u-%s-%s-24' % (key, opt), 'u-%s-%s-16' % (key, opt)
        symbols.append(u_symbol(key, opt, '24', o['files']['24']))
        symbols.append(u_symbol(key, opt, '16', o['files']['16']))
        if opt == rec_opt:
            rec_syms.append((key, a['word'], s24, s16))
        verdict, reading = NAMING[key][opt]
        vword = {'Y': 'Names the subject', 'P': 'Partly', 'N': 'Names something else'}[verdict]
        c = closest.get(f24)
        cl_txt = '%s %s, %.3f (%s percentile), %s' % (c['b'].split(' ')[0], ' '.join(c['b'].split(' ')[1:]), c['likeness'],
                                                      pct(c['percentile']), lik_word(c['likeness'])) if c else 'none'
        near = nearest_in_set(f24)
        near_txt = ''
        if near and near[0] >= WATCH:
            near_txt = ('<dt>Nearest in the set</dt><dd>%s, %.3f, %s</dd>'
                        % (e(subject(near[1]).replace('-', ' ') + ' ' + re.search(r'Option-([ABC])', near[1]).group(1)),
                           near[0], lik_word(near[0])))
        opts_html.append((opt, o['shows'], s24, s16, f24, f16, verdict, vword, reading, cl_txt, near_txt))
    cards.append((a, rec_opt, rec_why, opts_html))


def specimen(key, s24, s16):
    kind, words = SPECIMEN[key]
    if kind == 'button':
        return '<span class="btn">%s<span>%s</span></span>' % (use(s24, 24), e(words))
    if kind == 'next':
        return ('<span class="btn">%s<span>Previous step</span></span> <span class="btn"><span>%s</span>%s</span>'
                % (use(s24, 24, ' style="transform:scaleX(-1)"'), e(words), use(s24, 24)))
    if kind == 'row':
        return ('<span class="row"><span>%s</span>%s</span><span class="row"><span>%s</span>%s</span>'
                % (e(words), use(s24, 24), e(words), use(s24, 24, ' style="transform:rotate(180deg)"')))
    if kind == 'inline':
        head, last = words.rsplit(' ', 1)
        return '<span class="inline">%s <span class="nowrap">%s%s</span></span>' % (e(head), e(last), use(s16, 16))
    if kind == 'line':
        return '<span class="line">%s<span>%s</span></span>' % (use(s24, 24), e(words))
    if kind == 'chip':
        return '<span class="chip" aria-pressed="true">%s<span>%s</span></span>' % (use(s24, 24), e(words))
    if kind == 'heading':
        return '<span class="th"><span>%s</span>%s</span>' % (e(words), use(s16, 16))
    return ''


def extra_uses(key, opt, s24, s16):
    """Turned and mirrored uses of one drawing, shown once per option."""
    if key == 'arrow':
        rows = [('Next', ''), ('Previous', 'transform:scaleX(-1)'), ('Sorted up', 'transform:rotate(-90deg)'),
                ('Sorted down', 'transform:rotate(90deg)')]
    elif key == 'chevron':
        rows = [('Closed', ''), ('Open', 'transform:rotate(180deg)')]
    else:
        return ''
    cells = ''.join('<span class="use"><span class="sw np">%s%s</span><span class="lbl">%s</span></span>'
                    % (use(s24, 24, ' style="%s"' % t if t else ''), use(s16, 16, ' style="%s"' % t if t else ''), n)
                    for n, t in rows)
    return '<div class="uses">%s</div>' % cells


def opt_block(key, rec_opt, item):
    (opt, shows, s24, s16, f24, f16, verdict, vword, reading, cl_txt, near_txt) = item
    rec = opt == rec_opt
    return '''
      <article class="opt%s" data-option="%s">
        <h3>Option %s%s</h3>
        <p class="shows">%s</p>
        <div class="pair" aria-label="True size">
          <span class="sw np">%s%s</span><span class="sw ch">%s%s</span>
        </div>
        <p class="lbl">True size: 24 and 16 px, on Newsprint and on Charcoal</p>
        <div class="pair x2">
          <span class="sw np">%s%s</span><span class="sw ch">%s%s</span>
        </div>
        <p class="lbl">2x: the 24 px master at 48, the 16 px master at 32</p>
        %s
        <div class="spec">%s</div>
        <dl class="figs">
          <dt>Naming at 24 px</dt><dd><span class="v v%s">%s</span> %s</dd>
          <dt>Pixel fit, 24 px</dt><dd>%s</dd>
          <dt>Pixel fit, 16 px</dt><dd>%s</dd>
          <dt>Closest Civic Line</dt><dd>%s</dd>
          %s
        </dl>
        <p class="files">%s<br>%s</p>
      </article>''' % (' rec' if rec else '', opt, opt, ' <span class="tag">Recommended</span>' if rec else '', e(shows),
                       use(s24, 24), use(s16, 16), use(s24, 24), use(s16, 16),
                       use(s24, 48), use(s16, 32), use(s24, 48), use(s16, 32),
                       extra_uses(key, opt, s24, s16), specimen(key, s24, s16),
                       verdict, vword, e(reading), pf_line(f24), pf_line(f16), e(cl_txt), near_txt,
                       e(f24), e(f16))


card_html = []
for n, (a, rec_opt, rec_why, items) in enumerate(cards, 1):
    key = a['key']
    blocks = ''.join(opt_block(key, rec_opt, it) for it in items)
    card_html.append('''
    <section class="card" id="u-%s">
      <header class="ch-head">
        <p class="num">%d</p>
        <div><h2>%s</h2><p class="asked">%s. The audit asks for: %s. Audit rank %s.</p></div>
      </header>
      <div class="opts">%s</div>
      <p class="why"><strong>Recommended: option %s.</strong> %s</p>
    </section>''' % (key, n, e(a['word'].replace('-', ' ')), e(a['label']), e(a['asked'].lower()), e(a['rank']), blocks,
                     rec_opt, e(rec_why)))

# Look-alike section: audit-named Civic Line threats beside each option, at 24 px.
cl_needed = set()
la_rows = []
for a in manifest:
    key = a['key']
    if key not in THREATS:
        continue
    for cid in THREATS[key]:
        if cid not in cl_files:
            continue
        cl_needed.add(cid)
        cells = []
        for o in a['options']:
            f24 = base(o['files']['24'])
            p = pairs_master.get((f24, cid))
            fig = ('%.3f, %s percentile' % (p['likeness'], pct(p['percentile']))) if p else 'under the 1st percentile'
            cells.append('<td><span class="sw np">%s</span><span class="fig">%s %s</span></td>'
                         % (use('u-%s-%s-24' % (key, o['option']), 24), o['option'], fig))
        la_rows.append('<tr><th scope="row">%s</th><td><span class="sw np">%s</span><span class="fig">%s %s</span></td>%s</tr>'
                       % (e(a['word'].replace('-', ' ')), use('cl-' + cid.lower(), 24), cid, e(cl_files[cid][1]), ''.join(cells)))

# Enclosed options measured against each other.
twin_pairs = sorted([p for p in lik['flagged'] if p['against'] == 'new' and '24px' in p['a'] and '24px' in p['b']],
                    key=lambda p: -p['likeness'])[:6]
twin_rows = []
for p in twin_pairs:
    def sym_of(fn):
        subj = subject(fn)
        k = [x['key'] for x in manifest if x['word'] == subj][0]
        o = re.search(r'Option-([ABC])', fn).group(1)
        return 'u-%s-%s-24' % (k, o), subj.replace('-', ' ') + ' ' + o
    sa, na = sym_of(p['a'])
    sb, nb = sym_of(p['b'])
    twin_rows.append('<li><span class="sw np">%s%s</span><span class="fig">%s and %s: %.3f</span></li>'
                     % (use(sa, 24), use(sb, 24), e(na), e(nb), p['likeness']))

# The recommended set as one family, and beside Civic Line.
fam_np = ''.join(use(s24, 24) for _, _, s24, _ in rec_syms)
fam_np16 = ''.join(use(s16, 16) for _, _, _, s16 in rec_syms)
for cid in ('CL-001', 'CL-012', 'CL-020', 'CL-024'):
    cl_needed.add(cid)
beside = ''.join(use('cl-' + c.lower(), 48) for c in ('CL-001', 'CL-012', 'CL-020', 'CL-024'))
rec_names = ', '.join('%s %s' % (w.replace('-', ' '), REC[k][0]) for k, w, _, _ in rec_syms)

symbols += [cl_symbol(c) for c in sorted(cl_needed)]

CSS = '''
:root{
  --np:var(--oa-color-palette-newsprint,#DCD9D2); --chc:var(--oa-color-palette-charcoal,#121212);
  --stone:var(--oa-color-palette-stone,#5D636D); --deep:var(--oa-color-derived-deep-stone,#4E535B);
  --dimnp:var(--oa-color-derived-dim-newsprint,#A3A19C); --white:var(--oa-color-palette-white,#FFFFFF);
  --cut:var(--np);
}
*{box-sizing:border-box}
html{background:var(--white)}
body{margin:0;background:var(--white);color:var(--chc);font-family:Inter,system-ui,sans-serif;font-size:15px;line-height:22px;
  font-variant-numeric:tabular-nums}
.page{width:1176px;margin:0 auto;padding:40px 24px 64px}
h1{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;font-size:32px;line-height:40px;margin:0 0 12px}
.lede{max-width:720px;margin:0 0 8px;color:var(--chc)}
.note{max-width:720px;margin:0 0 8px;color:var(--deep);font-size:14px;line-height:20px}
.card{border-top:2px solid var(--chc);padding:24px 0 32px}
.ch-head{display:flex;gap:16px;align-items:flex-start;margin-bottom:16px}
.num{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;font-size:26px;line-height:32px;margin:0;width:40px}
h2{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;font-size:26px;line-height:32px;margin:0}
.asked{margin:4px 0 0;color:var(--deep);font-size:14px;line-height:20px}
.opts{display:grid;grid-template-columns:repeat(3,360px);gap:24px}
.opt{border:1px solid var(--dimnp);padding:16px;background:var(--white)}
.opt.rec{border:2px solid var(--chc);padding:15px}
h3{font-size:17px;line-height:24px;margin:0;font-weight:700}
.tag{display:inline-block;font-size:13px;line-height:20px;font-weight:600;border:1px solid var(--chc);padding:0 6px;margin-left:8px}
.shows{margin:2px 0 12px;font-size:14px;line-height:20px}
.pair{display:flex;gap:0}
.sw{display:inline-flex;align-items:center;gap:16px;padding:12px 16px;line-height:0}
.np{background:var(--np);color:var(--chc)}
.ch{background:var(--chc);color:var(--np)}
.g{display:block;flex:none}
.lbl{margin:4px 0 12px;font-size:13px;line-height:20px;color:var(--deep)}
.uses{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}
.use{display:flex;flex-direction:column}
.use .lbl{margin:4px 0 0}
.spec{background:var(--np);padding:12px 16px;margin:0 0 12px;display:flex;flex-wrap:wrap;gap:8px;min-height:68px;align-items:center}
.btn{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 14px 0 12px;border:1px solid var(--chc);
  font-weight:500;font-size:16px;line-height:24px;white-space:nowrap}
.row{display:flex;align-items:center;justify-content:space-between;gap:8px;height:44px;width:100%;border-bottom:1px solid var(--stone);
  font-size:16px;line-height:24px}
.inline{font-size:16px;line-height:24px}
.nowrap{white-space:nowrap}
.nowrap .g{display:inline-block;vertical-align:-2px;margin-left:4px}
.line{display:flex;align-items:center;gap:8px;font-size:15px;line-height:22px}
.chip{display:inline-flex;align-items:center;gap:6px;height:44px;padding:0 14px 0 10px;border:2px solid var(--chc);border-radius:22px;
  font-weight:500;font-size:16px;line-height:24px}
.th{display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:15px;line-height:22px;border-bottom:2px solid var(--chc);padding:4px 0}
.figs{display:grid;grid-template-columns:116px 1fr;gap:4px 8px;margin:0;font-size:13px;line-height:20px}
.figs dt{color:var(--deep)}
.figs dd{margin:0}
.v{font-weight:600}
.vN{text-decoration:underline}
.files{margin:12px 0 0;font-size:13px;line-height:20px;color:var(--deep)}
.why{margin:16px 0 0;max-width:900px}
table{border-collapse:collapse;margin:12px 0 0}
th,td{text-align:left;vertical-align:top;padding:8px 12px 8px 0;font-size:13px;line-height:20px;border-bottom:1px solid var(--dimnp)}
td .sw{padding:8px}
.fig{display:block;margin-top:4px}
.twins{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(3,360px);gap:12px 24px}
.twins .sw{gap:8px;padding:8px}
.fam{display:flex;flex-wrap:wrap;gap:16px}
.fam .sw{flex-wrap:wrap}
.legend{display:flex;gap:24px;font-size:13px;line-height:20px;color:var(--deep);margin:8px 0 0}
'''

SYMBOLS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">%s</svg>' % ''.join(symbols)

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Utility Icons Plates</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../../../../build/tokens/tokens.css">
<style>%s</style>
</head>
<body>
%s
<main class="page">
  <h1>Utility icons: three options for each drawing</h1>
  <p class="lede">Eighteen drawings for seventeen interface actions, as the accessibility audit lists them, with three options each (DR-134, DR-146). Every option of one action shares the grid and the line, so the set stays one family whichever you pick. The options differ in the picture.</p>
  <p class="note">Construction: a 24-unit grid with a 2 px line at 24 px (the token <code>--oa-component-icon-utility-line-medium</code>) and a 1.5 px line on its own 16 px master. Round caps and joins, one color through currentColor, no red. Every straight line sits on whole pixels. The first row of each option is true size; capture this page at device scale 1. Specimen words are examples from the audit.</p>
  <p class="note">Naming at 24 px is the designer's own reading of each option with no label, before any reader sees it. Likeness is the engineer's look-alike check at 24 px against the 122 Civic Line masters: it watches from %.3f (95th percentile of the master pairs) and flags from %.3f (99th).</p>
  %s
  <section class="card" id="look-alikes">
    <header class="ch-head"><p class="num">19</p><div><h2>Beside the Civic Line drawings the audit names</h2>
    <p class="asked">Each option at 24 px beside the topic drawing a reader could take for it, with the look-alike figure.</p></div></header>
    <table><thead><tr><th scope="col">Drawing</th><th scope="col">Civic Line</th><th scope="col">Option A</th><th scope="col">Option B</th><th scope="col">Option C</th></tr></thead>
    <tbody>%s</tbody></table>
  </section>
  <section class="card" id="twins">
    <header class="ch-head"><p class="num">20</p><div><h2>Enclosed options look alike to each other</h2>
    <p class="asked">The ring or frame carries most of the shape at 24 px, so options drawn inside one measure as near twins. The closest pair among the 122 masters measures 0.964. This is why the recommendations keep the actions bare and enclose only the error and success marks.</p></div></header>
    <ul class="twins">%s</ul>
  </section>
  <section class="card" id="family">
    <header class="ch-head"><p class="num">21</p><div><h2>The recommended set as one family</h2>
    <p class="asked">%s.</p></div></header>
    <div class="fam"><span class="sw np">%s</span><span class="sw ch">%s</span></div>
    <p class="lbl">24 px, on Newsprint and on Charcoal</p>
    <div class="fam"><span class="sw np">%s</span><span class="sw ch">%s</span></div>
    <p class="lbl">16 px masters</p>
    <div class="fam"><span class="sw np">%s%s</span></div>
    <p class="lbl">Beside Civic Line at the sizes they meet: CL-001 Voting, CL-012 Election Rules, CL-020 Track and CL-024 Feedback Loop at 48 px, then Download, Filter, Search and Reset at 24 px</p>
  </section>
</main>
<script>
// Pixel snap: text before a glyph can leave it on a fraction of a pixel. Each glyph moves by under one pixel so it
// sits on whole CSS pixels, as the guide places icons; the plate is then true to the masters' pixels.
function snap(){
  for (const s of document.querySelectorAll('svg.g')) {
    s.style.translate = '';
    const r = s.getBoundingClientRect();
    const x = r.left + window.scrollX, y = r.top + window.scrollY;
    const dx = Math.round(x) - x, dy = Math.round(y) - y;
    if (Math.abs(dx) > 0.001 || Math.abs(dy) > 0.001) s.style.translate = dx.toFixed(3) + 'px ' + dy.toFixed(3) + 'px';
  }
  document.documentElement.dataset.snapped = '1';
}
document.fonts.ready.then(snap);
window.addEventListener('resize', snap);
</script>
</body>
</html>
''' % (CSS, SYMBOLS, WATCH, FLAG, ''.join(card_html), ''.join(la_rows), ''.join(twin_rows), e(rec_names),
       fam_np, fam_np, fam_np16, fam_np16, beside,
       ''.join(use('u-%s-%s-24' % (k, REC[k][0]), 24) for k in ('download', 'filter', 'search', 'reset')))

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT, 'w') as fh:
    fh.write(page)
print('wrote %s (%d KB)' % (OUT, len(page) // 1024))
