#!/usr/bin/env python3
"""Plate page for the utility icons, stage B round 1 and its fix round (icon designer, utility hand, November 9, 2026).

Reads the SVG masters and manifest in work/build/assets/utility-icons/, the check results in its qa/ folder and the
Civic Line black masters (read only), and writes
work/boards/phase-2/stage-b/drawings/utility/20261109_Utility-Icons-Plates.html for the board builder to capture.

The page opens with the family card (D2-621): the recommended picks drawn bare, with Error, Success and Warning in
their shapes, beside the same set with every action in a ring, at 24 and 16 px on Newsprint and Charcoal. Then one card
per drawing: every option at 24 and 16 px on both grounds at true size and at 2x, its word in use, the naming reading
at 24 px, both checks' figures, the look-alike figures between the card's own options, and the one-line reason when a
card shows fewer than three options (D2-622). Glyphs are inline SVG symbols in currentColor, snapped to whole CSS
pixels so a capture at device scale 1 shows the reader's pixels.

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
    'close': {'A': ('Y', 'Close.')},
    'menu': {'A': ('Y', 'Menu.'),
             'B': ('P', 'Alone, an equals sign or a drag handle; beside its word, Menu at once.')},
    'arrow': {'A': ('Y', 'Next, or go forward.'), 'B': ('Y', 'Next, or go.')},
    'chevron': {'A': ('Y', 'Show more, or open the list.'), 'B': ('Y', 'Open the list: the dropdown sign.')},
    'download': {'A': ('Y', 'Download.'), 'B': ('Y', 'Download, or save.'), 'C': ('Y', 'Download the file.')},
    'another-site': {'A': ('Y', 'Open somewhere else, or open in a new tab.'),
                     'B': ('P', 'Up and to the right; may read as trending up.')},
    'search': {'A': ('Y', 'Search.')},
    'filter': {'A': ('Y', 'Filter.'), 'B': ('P', 'Filter, or sort: the list-filter sign.')},
    'copy': {'A': ('Y', 'Copy, or duplicate.'), 'B': ('Y', 'Copy, or pages.'), 'C': ('P', 'Copy text, or documents.')},
    'play': {'A': ('Y', 'Play.')},
    'pause': {'A': ('Y', 'Pause.')},
    'reset': {'A': ('P', 'Undo, a near subject.'), 'B': ('Y', 'Undo, or reset.'), 'C': ('P', 'Undo, or turn left.')},
    'error': {'A': ('Y', 'Error, or alert.'), 'B': ('Y', 'Stop, or error.'), 'C': ('P', 'Notice, or important.')},
    'success': {'A': ('Y', 'Done, or success.'), 'B': ('Y', 'Done, or success.')},
    'check': {'A': ('Y', 'Check, or done.'), 'B': ('Y', 'A ticked box: selected.')},
    'full-size': {'A': ('Y', 'Full screen, or expand.'), 'B': ('Y', 'Expand.'),
                  'C': ('P', 'Expand, or resize; near the outside-link arrow.')},
    'sort': {'A': ('Y', 'Sort, or swap.'), 'B': ('P', 'Sort, or choose from a list.'),
             'C': ('P', 'Sort; reads as sorted downward, an order in use.')},
    'warning': {'A': ('Y', 'Warning, or caution.'), 'B': ('Y', 'Warning: the road sign.')},
}

REC = {
    'close': ('A', 'The bare cross is the sign readers look for when they want out.'),
    'menu': ('A', 'Three even bars are the menu sign on every phone, and the guide already draws them. Two bars read as Menu only beside the word.'),
    'arrow': ('A', 'The open head matches the sort arrows and the chevron\'s arms. The closed head is a heavier, sign-like arrow.'),
    'chevron': ('A', 'The chevron is the expand sign readers know, and it stays apart from the arrow, which keeps its shaft. The triangle reads as a dropdown.'),
    'download': ('A', 'The tray is the download sign readers know best. B is the pick if you want the most distance from CL-001 Voting; C says a file.'),
    'another-site': ('A', 'The box with an arrow leaving its corner is the known sign, and it leaves by the corner, as the audit asks, so it stays apart from CL-001 Voting. B can read as trending up.'),
    'search': ('A', 'The plain magnifier is the sign readers scan for.'),
    'filter': ('A', 'The funnel is the sign the audit asks for. The list-filter lines can read as sort.'),
    'copy': ('A', 'Two square sheets read as Copy at both sizes.'),
    'play': ('A', 'The plain triangle, picked with Pause A as a pair.'),
    'pause': ('A', 'Two plain bars, picked with Play A as a pair. Their watch figure against CL-012 Election Rules is a blurred-shape match; side by side the two do not read alike.'),
    'reset': ('B', 'It reads as undo or reset, its upright head sits on whole pixels, and it is the furthest from CL-024 Feedback Loop. A reads as undo, a near subject.'),
    'error': ('A', 'The circle the audit asks for, apart from the Warning triangle and the bare Close cross. The octagon sits between the circle and the square at 16 px.'),
    'success': ('B', 'The open circle reads as done and differs from the error mark\'s closed circle with no second weight. A solid disc would need solid partners for Error and Warning.'),
    'check': ('A', 'The bare check is the selected mark readers know. The ticked box doubles a chip\'s own outline.'),
    'full-size': ('A', 'Four corners are the video sign for filling the screen.'),
    'sort': ('A', 'The two arrows share the head of the Next arrow, which turns to show the order in use. B borrows the chevron, and C already shows an order.'),
    'warning': ('A', 'The triangle is the warning shape readers know. Ink only, never red.'),
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

STATUS = ('error', 'success', 'warning')


# ---------- data ----------
def load(name):
    with open(os.path.join(QA, name)) as fh:
        return json.load(fh)


manifest = json.load(open(os.path.join(ASSETS, '20261109_Utility-Icons-Manifest.json')))
cards_m = manifest['cards']
pf = {}
for name in ('20261109_Utility-Pixel-Fit-24px.json', '20261109_Utility-Pixel-Fit-16px.json',
             '20261109_Utility-Pixel-Fit-Ringed-24px.json', '20261109_Utility-Pixel-Fit-Ringed-16px.json'):
    for r in load(name)['results']:
        pf[os.path.basename(r['file'])] = r
pf_solid = {}
for name in ('20261109_Utility-Pixel-Fit-Solid-24px.json', '20261109_Utility-Pixel-Fit-Solid-16px.json'):
    for r in load(name)['results']:
        pf_solid[os.path.basename(r['file'])] = r
lik = load('20261109_Utility-Likeness.json')
lik_all = load('20261109_Utility-Likeness-All-Pairs-24px.json')
fam_bare = load('20261109_Utility-Likeness-Family-Bare-24px.json')
fam_ring = load('20261109_Utility-Likeness-Family-Ringed-24px.json')
FLAG = lik['thresholds']['flag']['likeness']
WATCH = lik['thresholds']['watch']['likeness']
MASTER_MAX = lik['distribution']['max']


def base(rel):
    return os.path.basename(rel)


closest = {c['a']: c for c in lik['closest']}
pairs_master = {}
for p in lik_all['flagged'] + lik_all['watch']:
    if p['against'] == 'master':
        pairs_master[(p['a'], p['b'].split(' ')[0])] = p

# Option-to-option figures on one card, at 24 and at 16 px (both drawn at 24 px by the check).
OPT = {}
for p in lik['options']:
    ma = re.match(r'20261109_Utility-(.+)-Option-([ABC])-(\d+)px\.svg', p['a'])
    mb = re.match(r'20261109_Utility-(.+)-Option-([ABC])-(\d+)px\.svg', p['b'])
    if not (ma and mb) or ma.group(1) != mb.group(1) or ma.group(3) != mb.group(3) or ma.group(2) == mb.group(2):
        continue
    OPT[(ma.group(1), ma.group(3), frozenset((ma.group(2), mb.group(2))))] = p['likeness']

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


def u_symbol(sym, size, rel):
    s = open(os.path.join(ASSETS, rel)).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1).strip()
    w = '2' if size == '24' else '1.5'
    return ('<symbol id="%s" viewBox="0 0 %s %s"><g fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g></symbol>') % (sym, size, size, w, inner)


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
    fails = sorted(set(r['scales']['1x']['fails']) | set(r['scales']['2x']['fails']))
    straight = ('straight strokes on whole pixels %d of %d' % (st['fit'], st['total'])) if st['total'] else 'no straight strokes'
    if r['pass']:
        out = 'pass'
    elif fails == ['weight'] and fname in pf_solid and pf_solid[fname]['pass']:
        out = 'pass on every measure but line weight, which a solid shape cannot meet'
    else:
        out = 'fail: ' + ', '.join(fails)
    return '%s; %s; soft pixels at 1x %d%%' % (out, straight, round(s1['soft_edges']['share'] * 100))


def lik_word(v):
    if v >= FLAG:
        return 'flag'
    if v >= WATCH:
        return 'watch'
    return 'clear'


# ---------- symbols ----------
symbols = []
SYM = {}
for a in cards_m:
    for o in a['options']:
        for size in ('24', '16'):
            sym = 'u-%s-%s-%s' % (a['key'], o['option'], size)
            symbols.append(u_symbol(sym, size, o['files'][size]))
for k, files in manifest['family_ringed'].items():
    for size in ('24', '16'):
        symbols.append(u_symbol('r-%s-%s' % (k, size), size, files[size]))
for k, files in manifest['solid_partners'].items():
    for size in ('24', '16'):
        symbols.append(u_symbol('s-%s-%s' % (k, size), size, files[size]))


# ---------- specimens ----------
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
        return '<span class="chip">%s<span>%s</span></span>' % (use(s24, 24), e(words))
    if kind == 'heading':
        return '<span class="th"><span>%s</span>%s</span>' % (e(words), use(s16, 16))
    return ''


def extra_uses(key, s24, s16):
    """Turned and mirrored uses of one drawing."""
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


def near_options(word, opt, letters):
    parts = []
    for other in letters:
        if other == opt:
            continue
        v24 = OPT.get((word, '24', frozenset((opt, other))))
        v16 = OPT.get((word, '16', frozenset((opt, other))))
        if v24 is None:
            continue
        parts.append('%s: %.3f at 24 px, %.3f at 16 px, %s' % (other, v24, v16, lik_word(max(v24, v16))))
    return '; '.join(parts)


def opt_block(a, o, rec_opt, letters):
    key, word, opt = a['key'], a['word'], o['option']
    s24, s16 = 'u-%s-%s-24' % (key, opt), 'u-%s-%s-16' % (key, opt)
    f24, f16 = base(o['files']['24']), base(o['files']['16'])
    verdict, reading = NAMING[key][opt]
    vword = {'Y': 'Names the subject', 'P': 'Partly', 'N': 'Names something else'}[verdict]
    c = closest.get(f24)
    cl_txt = ('%s, %.3f (%s percentile), %s' % (c['b'], c['likeness'], pct(c['percentile']), lik_word(c['likeness']))) if c else 'none'
    near = near_options(word, opt, letters)
    near_html = '<dt>Other options here</dt><dd>%s</dd>' % e(near) if near else ''
    rec = opt == rec_opt
    return '''
      <article class="opt%s" data-option="%s">
        <h3>Option %s%s</h3>
        <p class="shows">%s</p>
        <div class="pair"><span class="sw np">%s%s</span><span class="sw ch">%s%s</span></div>
        <p class="lbl">True size: 24 and 16 px, on Newsprint and on Charcoal</p>
        <div class="pair x2"><span class="sw np">%s%s</span><span class="sw ch">%s%s</span></div>
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
      </article>''' % (' rec' if rec else '', opt, opt, ' <span class="tag">Recommended</span>' if rec else '', e(o['shows']),
                       use(s24, 24), use(s16, 16), use(s24, 24), use(s16, 16),
                       use(s24, 48), use(s16, 32), use(s24, 48), use(s16, 32),
                       extra_uses(key, s24, s16), specimen(key, s24, s16),
                       verdict, vword, e(reading), pf_line(f24), pf_line(f16), e(cl_txt), near_html, e(f24), e(f16))


def solid_row():
    cells = []
    for k, files in manifest['solid_partners'].items():
        name = k.capitalize()
        cells.append('<span class="use"><span class="pair"><span class="sw np">%s%s</span><span class="sw ch">%s%s</span></span>'
                     '<span class="lbl">%s, solid partner</span></span>'
                     % (use('s-%s-24' % k, 24), use('s-%s-16' % k, 16), use('s-%s-24' % k, 24), use('s-%s-16' % k, 16), name))
    cells.insert(0, '<span class="use"><span class="pair"><span class="sw np">%s%s</span><span class="sw ch">%s%s</span></span>'
                    '<span class="lbl">Success A</span></span>'
                 % (use('u-success-A-24', 24), use('u-success-A-16', 16), use('u-success-A-24', 24), use('u-success-A-16', 16)))
    return ('<div class="partners"><h3>If you pick A: solid partners for Error and Warning</h3>'
            '<p class="note">The three marks stay one kind only if all three go solid. Each partner cuts its mark out of the '
            'shape with the 2 px line, 2 px at 16 px as well, since a cut reads thinner than an inked line. They pass the '
            'pixel-fit check on every measure but line weight, which a solid shape cannot meet.</p>'
            '<div class="uses">%s</div></div>' % ''.join(cells))


card_html = []
for n, a in enumerate(cards_m, 1):
    key = a['key']
    rec_opt, rec_why = REC[key]
    letters = [o['option'] for o in a['options']]
    blocks = ''.join(opt_block(a, o, rec_opt, letters) for o in a['options'])
    fewer = ('<p class="fewer"><strong>Why %s.</strong> %s</p>'
             % ('one option' if len(letters) == 1 else 'two options', e(a['fewer_reason']))) if a.get('fewer_reason') else ''
    extra = solid_row() if key == 'success' else ''
    card_html.append('''
    <section class="card" id="u-%s">
      <header class="ch-head">
        <p class="num">%d</p>
        <div><h2>%s</h2><p class="asked">%s. The audit asks for: %s. Audit rank %s.</p></div>
      </header>
      <div class="opts">%s</div>
      %s%s
      <p class="why"><strong>Recommended: option %s.</strong> %s</p>
    </section>''' % (key, n, e(a['word'].replace('-', ' ')), e(a['label']), e(a['asked'].lower()), e(a['rank']), blocks,
                     fewer, extra, rec_opt, e(rec_why)))

# ---------- the family card (D2-621) ----------
order = [a['key'] for a in cards_m]
bare_syms = {a['key']: 'u-%s-%s' % (a['key'], REC[a['key']][0]) for a in cards_m}


def fam_row(kind, size):
    out = []
    for k in order:
        if kind == 'ringed' and k not in STATUS:
            out.append(use('r-%s-%s' % (k, size), int(size)))
        else:
            out.append(use('%s-%s' % (bare_syms[k], size), int(size)))
    return ''.join(out)


def top_pair(d):
    nn = sorted([p for p in d['flagged'] + d['watch'] if p['against'] == 'new'], key=lambda p: -p['likeness'])
    n_flag = sum(1 for p in nn if p['likeness'] >= FLAG)
    nm = lambda f: re.sub(r'^20261109_Utility-|-24px\.svg$', '', f).replace('-', ' ')
    return n_flag, nm(nn[0]['a']), nm(nn[0]['b']), nn[0]['likeness']


bf, ba, bb, bv = top_pair(fam_bare)
rf, ra, rb, rv = top_pair(fam_ring)


def stepper(kind):
    """The atlas stepper row from the audit: Play, Previous step, Next step, Reset."""
    def g(k, extra=''):
        sym = ('r-%s-24' % k) if kind == 'ringed' else '%s-24' % bare_syms[k]
        return use(sym, 24, extra)
    return ('<span class="btn">%s<span>Play</span></span><span class="btn">%s<span>Previous step</span></span>'
            '<span class="btn"><span>Next step</span>%s</span><span class="btn">%s<span>Reset</span></span>'
            % (g('play'), g('arrow', ' style="transform:scaleX(-1)"'), g('arrow'), g('reset')))


cl_beside = ('CL-001', 'CL-012', 'CL-020', 'CL-024')
family = '''
  <section class="card fam-card" id="family-card">
    <header class="ch-head"><p class="num">0</p><div><h2>Bare actions, or every action in a ring</h2>
    <p class="asked">Decide this once, before the icons. Each action card below then offers bare pictures only (D2-621). Error, Success and Warning keep their own shapes in both rows: a closed circle, an open circle and a triangle, so they read apart without color.</p></div></header>
    <h3>Bare actions, shaped marks</h3>
    <div class="fam"><span class="sw np">%s</span><span class="sw ch">%s</span></div>
    <div class="fam"><span class="sw np">%s</span><span class="sw ch">%s</span></div>
    <p class="lbl">24 and 16 px, on Newsprint and on Charcoal. %s</p>
    <div class="spec wide">%s</div>
    <h3>Every action in a ring</h3>
    <div class="fam"><span class="sw np">%s</span><span class="sw ch">%s</span></div>
    <div class="fam"><span class="sw np">%s</span><span class="sw ch">%s</span></div>
    <p class="lbl">24 and 16 px, on Newsprint and on Charcoal. The ring is the one the round 1 ring options used: 20 px across at 24 px, the action redrawn smaller inside it.</p>
    <div class="spec wide">%s</div>
    <dl class="figs fam-figs">
      <dt>Bare set</dt><dd>%s pairs reach the look-alike flag (%.3f). The closest are %s and %s at %.3f.</dd>
      <dt>Ringed set</dt><dd>%d pairs reach the flag. The closest are %s and %s at %.3f, closer than any two of the 122 Civic Line drawings (%.3f). In this row the Error mark reads as one more ringed glyph.</dd>
      <dt>Pixel fit</dt><dd>Both rows pass at 24 and 16 px. Inside a ring at 16 px the action has about 9 px to draw in, and View full size closes into a square.</dd>
    </dl>
    <p class="why"><strong>Recommended: bare actions, shaped marks.</strong> Every control already has its own 44 px target and outline, so a ring repeats it, and ringed actions lose the outlines a reader tells apart.</p>
    <div class="fam"><span class="sw np">%s%s</span></div>
    <p class="lbl">Beside Civic Line at the sizes they meet: CL-001 Voting, CL-012 Election Rules, CL-020 Track and CL-024 Feedback Loop at 48 px, then Download, Filter, Search and Reset at 24 px</p>
  </section>''' % (fam_row('bare', '24'), fam_row('bare', '24'), fam_row('bare', '16'), fam_row('bare', '16'),
                   e('Close, Menu, Arrow, Chevron, Download, Another site, Search, Filter, Copy, Play, Pause, Reset, Error, Success, Selected check, View full size, Sort, Warning.'),
                   stepper('bare'),
                   fam_row('ringed', '24'), fam_row('ringed', '24'), fam_row('ringed', '16'), fam_row('ringed', '16'),
                   stepper('ringed'),
                   'No' if bf == 0 else str(bf), FLAG, ba, bb, bv, rf, ra, rb, rv, MASTER_MAX,
                   ''.join(use('cl-' + c.lower(), 48) for c in cl_beside),
                   ''.join(use('%s-24' % bare_syms[k], 24) for k in ('download', 'filter', 'search', 'reset')))

# ---------- look-alikes against the Civic Line drawings the audit names ----------
cl_needed = set(cl_beside)
la_rows = []
for a in cards_m:
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
        cells += ['<td></td>'] * (3 - len(a['options']))
        la_rows.append('<tr><th scope="row">%s</th><td><span class="sw np">%s%s</span><span class="fig">%s %s, at 24 and 48 px</span></td>%s</tr>'
                       % (e(a['word'].replace('-', ' ')), use('cl-' + cid.lower(), 24), use('cl-' + cid.lower(), 48), cid,
                          e(cl_files[cid][1]), ''.join(cells)))

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
.lede{max-width:720px;margin:0 0 8px}
.note{max-width:720px;margin:0 0 8px;color:var(--deep);font-size:14px;line-height:20px}
.card{border-top:2px solid var(--chc);padding:24px 0 32px}
.ch-head{display:flex;gap:16px;align-items:flex-start;margin-bottom:16px}
.num{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;font-size:26px;line-height:32px;margin:0;width:40px}
h2{font-family:"Inter Tight",Inter,sans-serif;font-weight:800;font-size:26px;line-height:32px;margin:0}
.asked{margin:4px 0 0;color:var(--deep);font-size:14px;line-height:20px;max-width:900px}
.opts{display:grid;grid-template-columns:repeat(3,360px);gap:24px}
.opt{border:1px solid var(--dimnp);padding:16px;background:var(--white)}
.opt.rec{border:2px solid var(--chc);padding:15px}
h3{font-size:17px;line-height:24px;margin:0;font-weight:700}
.fam-card h3,.partners h3{margin:16px 0 8px}
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
.spec.wide{max-width:760px}
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
.fam-figs{grid-template-columns:116px 760px;margin:8px 0 0}
.figs dt{color:var(--deep)}
.figs dd{margin:0}
.v{font-weight:600}
.vN{text-decoration:underline}
.files{margin:12px 0 0;font-size:13px;line-height:20px;color:var(--deep)}
.fewer{margin:16px 0 0;max-width:900px}
.partners{margin:16px 0 0}
.why{margin:16px 0 0;max-width:900px}
table{border-collapse:collapse;margin:12px 0 0}
th,td{text-align:left;vertical-align:top;padding:8px 12px 8px 0;font-size:13px;line-height:20px;border-bottom:1px solid var(--dimnp)}
td .sw{padding:8px}
.fig{display:block;margin-top:4px}
.fam{display:flex;flex-wrap:wrap;gap:0;margin:0 0 4px}
.fam .sw{gap:16px}
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
  <h1>Utility icons: the family card, then the options for each drawing</h1>
  <p class="lede">Eighteen drawings for seventeen interface actions, as the accessibility audit lists them (DR-134, DR-146). The family card comes first and settles one question for the whole set: bare actions, or every action in a ring. Each card after it offers bare pictures only: three where three real choices exist, fewer with a one-line reason (D2-622).</p>
  <p class="note">Construction: a 24-unit grid with a 2 px line at 24 px (the token <code>--oa-component-icon-utility-line-medium</code>) and a 1.5 px line on its own 16 px master. Round caps and joins, one color through currentColor, no red. Every straight line sits on whole pixels. The first row of each option is true size; capture this page at device scale 1. Specimen words are examples from the audit.</p>
  <p class="note">Naming at 24 px is the designer's own reading of each option with no label, before any reader sees it. Likeness is the engineer's look-alike check at 24 px: it watches from %.3f (95th percentile of the pairs among the 122 Civic Line masters) and flags from %.3f (99th). Each card prints the figures between its own options.</p>
  %s
  %s
  <section class="card" id="look-alikes">
    <header class="ch-head"><p class="num">19</p><div><h2>Beside the Civic Line drawings the audit names</h2>
    <p class="asked">Each option at 24 px beside the topic drawing a reader could take for it, with the look-alike figure. The check compares both at 24 px, where the Civic Line line is 0.63 px; the 48 px drawing is there so you can tell which one it is.</p></div></header>
    <table><thead><tr><th scope="col">Drawing</th><th scope="col">Civic Line</th><th scope="col">Option A</th><th scope="col">Option B</th><th scope="col">Option C</th></tr></thead>
    <tbody>%s</tbody></table>
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
''' % (CSS, SYMBOLS, WATCH, FLAG, family, ''.join(card_html), ''.join(la_rows))

if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, 'w') as fh:
        fh.write(page)
    print('wrote %s (%d KB)' % (OUT, len(page) // 1024))
