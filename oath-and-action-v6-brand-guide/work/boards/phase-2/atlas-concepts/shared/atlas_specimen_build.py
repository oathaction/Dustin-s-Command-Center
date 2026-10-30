"""Build the shared atlas type and line specimen (October 30, 2026).

Writes 20261030_Atlas-Type-And-Line-Specimen.html beside this file. Every label, sign, grade and delay printed
on the page is read from the model export; every contrast ratio is computed here from the locked hex values.
The wordmark and the Civic Line icons are inlined from their approved masters, unchanged.

Run from the project root:
    python3 -I work/boards/phase-2/atlas-concepts/shared/atlas_specimen_build.py
"""
import html
import math
import importlib.util
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
spec = importlib.util.spec_from_file_location('acc', ROOT / 'work/build/scripts/phase-2/atlas_concepts_common.py')
acc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc)

M = acc.load_model()
P = acc.PALETTE
NP, CH, RED, PR, ST, VG, WH, DS = (P['newsprint'], P['charcoal'], P['pillar_red'], P['prussian'], P['stone'],
                                    P['verdigris'], P['white'], P['deep_stone'])
MINUS = '−'
e = html.escape


# ---------------------------------------------------------------- contrast
def _lum(hexv):
    c = [int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def r2(a, b):
    return f'{ratio(a, b):.2f}'


# ---------------------------------------------------------------- model text
G = M['generated']
COUNTS = G['counts']
AREA_C = next(a for a in M['areas'] if a['id'] == 'C')
R10 = M['loops']['R10']
L25 = M['links']['L25']
LE02 = M['links']['LE02']
N = M['nodes']
R01 = M['reforms']['R-01']
STEP_NO = next(st['index'] for st in R10['steps'] if st['id'] == 'L25')
SNAP = 'October 15, 2026'  # G['snapshot'] is 2026-10-15
assert G['snapshot'] == '2026-10-15'
SOURCE = (f'{G["title"]} Systems Atlas V7, snapshot {SNAP}. '
          f'<span data-count="variables">{COUNTS["variables"]}</span> variables, '
          f'<span data-count="connections">{COUNTS["connections"]}</span> connections, '
          f'<span data-count="loops">{COUNTS["loops"]}</span> loops, '
          f'<span data-count="reforms">{COUNTS["reforms"]}</span> reforms.')


def grade_word(g):
    return acc.GRADES[g][0]


def grade_gloss(g):
    return acc.GRADES[g][1]


def sign_char(p):
    return {'+': '+', '-': MINUS}.get(p, '')


# ---------------------------------------------------------------- identity master
def wordmark(height=24, master='wordmark/20261028_Wordmark-24px-Master.svg', ink=CH):
    src = (ROOT / 'work/build/assets/identity' / master).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w = float(vb[2]) * height / float(vb[3])
    src = re.sub(r'<title>.*?</title>', '', src, flags=re.S)
    src = src.replace('<svg ', f'<svg width="{w:.0f}" height="{height}" role="img" aria-label="Oath &amp; Action" '
                      f'style="color:{ink};display:block" ', 1)
    return src, w


# ---------------------------------------------------------------- line geometry
WEIGHTS = (2, 3, 6)
ARROW = {2: (10, 8), 3: (13, 11), 6: (22, 18)}          # length along the line, base width
TAG = {2: (14, 6, 16, 8, 2), 3: (15, 6, 17, 9, 3), 6: (18, 8, 22, 10, 2)}   # body, point, height, sign length, sign bar


def snap(y, w):
    """Odd widths sit on half pixels, even widths on whole pixels, so strokes render crisp."""
    return math.floor(y) + 0.5 if round(w) % 2 == 1 else round(y)


def pattern(texture, w):
    if texture == 'dashed':
        return [4 * w, 2 * w], 'butt'
    if texture == 'dash-dot':
        return [4 * w, 1.5 * w, w, 1.5 * w], 'butt'
    if texture == 'dotted':
        return [0, 2.5 * w], 'round'
    return None, 'butt'


def fitted(texture, w, length):
    """Scale the pattern so the line starts and ends on ink (rule 3.4 of the memo)."""
    arr, cap = pattern(texture, w)
    if arr is None:
        return '', cap
    if texture == 'dotted':
        n = max(1, round(length / arr[1]))
        return f'0 {length / n:.3f}', cap
    per = sum(arr)
    n = max(1, round((length - arr[0]) / per))
    k = length / (n * per + arr[0])
    return ' '.join(f'{x * k:.3f}' for x in arr), cap


def coded_line(x0, x1, y, w, texture, ink, arrow=True, extra=''):
    """A horizontal connection from x0 to the arrow tip at x1, drawn as path plus separate head."""
    al, ab = ARROW[w]
    y = snap(y, w)
    base = x1 - al if arrow else x1
    inset = w / 2 if texture == 'dotted' else 0
    end_inset = 1.5 * w if (texture == 'dotted' and arrow) else inset   # the last dot clears the head
    length = base - x0 - inset - end_inset
    da, cap = fitted(texture, w, length)
    dash = f' stroke-dasharray="{da}"' if da else ''
    out = (f'<path d="M{x0 + inset:.2f} {y}H{base - end_inset:.2f}" fill="none" stroke="{ink}" stroke-width="{w}" '
           f'stroke-linecap="{cap}"{dash}{extra}/>')
    if arrow:
        out += f'<path d="M{base:.2f} {y - ab / 2:.2f}L{x1:.2f} {y}L{base:.2f} {y + ab / 2:.2f}Z" fill="{ink}"/>'
    return out


def sign_tag(cx, cy, sign, w, fill, glyph, halo, direction=1):
    a, p, h, sl, sb = TAG[w]
    L = a + p
    x0 = round(cx - L / 2)
    if direction == 1:
        pts = [(x0, cy - h / 2), (x0 + a, cy - h / 2), (x0 + L, cy), (x0 + a, cy + h / 2), (x0, cy + h / 2)]
        bx = x0 + a / 2
    else:
        pts = [(x0 + L, cy - h / 2), (x0 + p, cy - h / 2), (x0, cy), (x0 + p, cy + h / 2), (x0 + L, cy + h / 2)]
        bx = x0 + p + a / 2
    poly = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    s = (f'<polygon points="{poly}" fill="{fill}" stroke="{halo}" stroke-width="4" stroke-linejoin="round" '
         f'paint-order="stroke"/>')
    s += f'<rect x="{bx - sl / 2:.2f}" y="{cy - sb / 2:.2f}" width="{sl}" height="{sb}" fill="{glyph}"/>'
    if sign == '+':
        s += f'<rect x="{bx - sb / 2:.2f}" y="{cy - sl / 2:.2f}" width="{sb}" height="{sl}" fill="{glyph}"/>'
    return f'<g data-sign="{e(sign)}">{s}</g>'


def ticks(x, y, count, w, ink):
    half = w / 2 + 4
    return ''.join(f'<rect x="{x + i * 5:.2f}" y="{y - half:.2f}" width="2" height="{2 * half:.2f}" fill="{ink}"/>'
                   for i in range(count))


def diamond(tip_x, y, ink, ground, size=12):
    hx = size / 2
    cx = tip_x - hx
    return (f'<path d="M{cx - hx:.2f} {y}L{cx:.2f} {y - hx * 0.8:.2f}L{tip_x:.2f} {y}L{cx:.2f} {y + hx * 0.8:.2f}Z" '
            f'fill="{ground}" stroke="{ink}" stroke-width="2" stroke-linejoin="miter"/>')


def svg_chip(x, y, word, code, ink, cell, compact=True):
    """A two-part chip drawn in SVG: type word in an ink cell, code in an outlined cell (M3). y is the top."""
    h = 22 if compact else 26
    wpx = round(len(word) * 9.7 + 14)
    cpx = round(len(code) * 8.6 + 16)
    cy = y + h / 2
    return (f'<g class="svgchip"><rect x="{x}" y="{y}" width="{wpx:.1f}" height="{h}" fill="{ink}"/>'
            f'<text x="{x + 7}" y="{cy}" dominant-baseline="central" class="sc-k" fill="{cell}">{e(word.upper())}</text>'
            f'<rect x="{x + wpx:.1f}" y="{y + 0.75}" width="{cpx - 0.75:.1f}" height="{h - 1.5}" fill="none" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<text x="{x + wpx + cpx / 2:.1f}" y="{cy}" dominant-baseline="central" text-anchor="middle" class="sc-c" '
            f'fill="{ink}">{e(code)}</text></g>'), wpx + cpx


def chip(word, code, cls=''):
    return (f'<span class="chip {cls}"><span class="k">{e(word)}</span><span class="c">{e(code)}</span></span>')


# ---------------------------------------------------------------- sections
def section_frame():
    s = 1 / 3
    col = (1312 - 11 * 24) / 12

    def cx(c):
        return 64 + (c - 1) * (col + 24)

    def rect(x, y, w, h, cls='z', fill='none'):
        return (f'<rect x="{x * s:.1f}" y="{y * s:.1f}" width="{w * s:.1f}" height="{h * s:.1f}" class="{cls}" '
                f'fill="{fill}"/>')

    cols = ''.join(f'<rect x="{cx(c) * s:.1f}" y="0" width="{col * s:.1f}" height="{960 * s:.1f}" fill="{WH}"/>'
                   for c in range(1, 13))
    zones = [
        ('Masthead, 72 px', 0, 72, rect(64, 0, 1312, 72)),
        ('Breadcrumb', 88, 106, rect(64, 88, cx(7) - 64 - 24, 18)),
        ('Headline and deck, columns 1 to 8', 120, 300, rect(64, 120, cx(9) - 24 - 64, 180)),
        ('Key, columns 9 to 12', 120, 300, rect(cx(9), 120, 1376 - cx(9), 180)),
        ('Drawing field, 12 columns', 324, 876, rect(64, 324, 1312, 552)),
        ('Footer and source line', 908, 948, rect(64, 908, 1312, 40)),
    ]
    marks = (rect(64, 24, 221, 24, 'blk', CH) + rect(cx(4), 30, 300, 12, 'blk2', DS) +
             rect(cx(9) + 80, 28, 1376 - cx(9) - 80, 16, 'blk2', DS))
    body = cols + marks + ''.join(z[3] for z in zones)
    body += f'<line x1="0" x2="{1440 * s}" y1="{900 * s}" y2="{900 * s}" class="fold"/>'
    labels = ''
    edge = 1376 * s
    for name, ay, yl in (('Masthead, 72 px', 36 * s, 12), ('Breadcrumb', 97 * s, 34),
                         ('Fold at 900 px', 900 * s, 300), ('Footer and source line', 928 * s, 324)):
        x_from = edge + 2 if 'Fold' not in name else 1440 * s + 2
        labels += (f'<path d="M{x_from:.1f} {ay:.1f}H{1440 * s + 10:.1f}L{1440 * s + 22:.1f} {yl:.1f}'
                   f'H{1440 * s + 30:.1f}" class="leader"/><text x="{1440 * s + 34:.1f}" y="{yl}" '
                   f'dominant-baseline="central" class="lab">{e(name)}</text>')
    for name, x, y in (('Headline and deck', 64, 120), ('columns 1 to 8', 64, 120 + 54),
                       ('Key, columns 9 to 12', cx(9), 120), ('Drawing field, 12 columns', 64, 324)):
        labels += (f'<text x="{x * s + 8:.1f}" y="{y * s + 16:.1f}" class="lab in">{e(name)}</text>')
    wide = (f'<svg data-view="frame-1440" class="frame" width="{1440 * s + 270:.0f}" height="{960 * s + 22:.0f}" '
            f'viewBox="0 -1 {1440 * s + 270:.0f} {960 * s + 22:.0f}" role="img" aria-label="Page frame at 1440 px, '
            f'drawn at one third size: masthead, breadcrumb, headline and key, drawing field, footer.">'
            f'<rect x="0" y="0" width="{1440 * s}" height="{960 * s}" fill="{NP}" class="z"/>{body}{labels}</svg>')

    # phone, same scale
    pc = (390 - 40 - 3 * 16) / 4
    pcols = ''.join(f'<rect x="{(20 + i * (pc + 16)) * s:.1f}" y="0" width="{pc * s:.1f}" height="{844 * s:.1f}" '
                    f'fill="{WH}"/>' for i in range(4))
    pz = [
        ('Masthead, 56 px', 0, 56, rect(20, 0, 350, 56)),
        ('View switch, 44 px targets', 56, 104, rect(20, 60, 350, 44)),
        ('Back link', 112, 136, rect(20, 112, 200, 24)),
        ('Headline and deck', 148, 300, rect(20, 148, 350, 152)),
        ('Drawing region, scrolls inside', 316, 748, rect(20, 316, 350, 432)),
        ('The lines in words', 764, 844, rect(20, 764, 350, 80)),
    ]
    pbody = pcols + rect(20, 20, 152, 16, 'blk', CH) + ''.join(z[3] for z in pz)
    plabels = ''
    ply = [8, 28, 48, 74, 177, 268]
    for (name, y0, y1, _), yl in zip(pz, ply):
        ay = (y0 + y1) / 2 * s
        plabels += (f'<path d="M{370 * s + 2:.1f} {ay:.1f}H{390 * s + 10:.1f}L{390 * s + 22:.1f} {yl:.1f}'
                    f'H{390 * s + 30:.1f}" class="leader"/><text x="{390 * s + 34:.1f}" y="{yl}" '
                    f'dominant-baseline="central" class="lab">{e(name)}</text>')
    phone = (f'<svg data-view="frame-390" class="frame" width="{390 * s + 250:.0f}" height="{844 * s + 2:.0f}" '
             f'viewBox="0 -1 {390 * s + 250:.0f} {844 * s + 2:.0f}" role="img" aria-label="Page frame at 390 px, '
             f'drawn at one third size: masthead, view switch, back link, headline, drawing region, the lines in words.">'
             f'<rect x="0" y="0" width="{390 * s}" height="{844 * s}" fill="{NP}" class="z"/>{pbody}{plabels}</svg>')

    return f'''
<section id="frame" class="sec" aria-labelledby="h-frame">
  <p class="eyebrow">01 Page frame</p>
  <h2 class="headline" id="h-frame">The page frame at 1440 and 390 px</h2>
  <div class="frames">
    <figure class="fig-wide"><div class="scroll" role="region" tabindex="0" aria-label="Frame at 1440 px">{wide}</div>
      <figcaption class="caption">1440 px: 12 columns of 87.33 px, 24 px gutters, 64 px margins. White bands are the columns. The Charcoal block is where the wordmark sits; a schematic never draws the mark itself below its minimum.</figcaption></figure>
    <figure class="fig-phone"><div class="scroll" role="region" tabindex="0" aria-label="Frame at 390 px">{phone}</div>
      <figcaption class="caption">390 px: 4 columns of 75.5 px, 16 px gutters, 20 px margins. One third scale, like the frame beside it.</figcaption></figure>
  </div>
</section>'''


def type_rows():
    q = R10['how_to_read']
    rows = [
        ('Display', 'Overview headline', 'Inter Tight 800', '56/60', '36/40', '−0.035 em', 't-display', e(G['title'])),
        ('Headline', 'Close-up and section titles', 'Inter Tight 800', '40/44', '30/34', '−0.03 em', 't-headline', e(R10['title'])),
        ('Deck', 'Under a headline, 62 characters a line at most', 'Inter 400', '19/28', '17/25', '0', 't-deck', e(AREA_C['text'])),
        ('Panel head', 'Cards, panels, the key', 'Inter Tight 800', '22/26', '20/24', '−0.02 em', 't-panel', e(AREA_C['title'])),
        ('Eyebrow', 'Section labels, in capitals', 'Inter 700', '13/18', '13/18', '+0.06 em', 't-eyebrow', 'Where a reform acts'),
        ('Body', 'Reading text in panels and notes', 'Inter 400', '17/27', '16/25', '0', 't-body', e(R10['summary'])),
        ('Panel text', 'Short text inside cards', 'Inter 400', '15/23', '15/23', '0', 't-ptext', e(R10['qualification'])),
        ('Quote', 'V7 sentences quoted whole', 'Lora Italic 400', '22/31', '19/27', '−0.005 em', 't-quote', '“' + e(q) + '”'),
        ('Figure', 'Counts printed from the model', 'Inter Tight 800, tabular', '40/40', '32/32', '−0.03 em', 't-figure',
         f'<span data-count="connections">{COUNTS["connections"]}</span> <span class="t-legend">connections</span>'),
        ('Station label', 'Diagram size 1: variables in a close-up', 'Inter Tight 700', '20/22', '18/20', '−0.01 em', 't-station', e(N['C2']['label'])),
        ('Map label', 'Diagram size 2: variables on a map, connection names', 'Inter 600', '15/18', '15/18', '0', 't-map', e(L25['name'])),
        ('Note', 'Diagram size 3: grade, delay, counts on wires', 'Inter 400; 500 on dark grounds', '13/16', '13/16', '+0.01 em', 't-note',
         f'{grade_word(L25["evidence"])}: {grade_gloss(L25["evidence"])}. {acc.DELAYS[L25["delay"]].capitalize()}.'),
        ('Caption', 'Under a drawing', 'Inter 400', '14/20', '14/20', '0', 't-caption',
         'The loop’s own route at full size. Tags show each step’s sign and the way it runs.'),
        ('Legend', 'Key entries', 'Inter 500', '13/18', '13/18', '0', 't-legend',
         f'Dashed: {grade_word("plausible")}, {grade_gloss("plausible")}'),
        ('Source line', 'Footer of every view', 'Inter 400, Deep Stone on Newsprint', '13/18', '13/18', '0', 't-source', SOURCE),
    ]
    out = ''
    for name, use, face, s1, s2, tr, cls, sample in rows:
        out += f'''
    <div class="trow">
      <div class="tspec"><p class="t-panel-s">{name}</p><p class="t-legend dim">{use}</p>
        <p class="t-legend mono">{face}<br>1440: {s1} px · 390: {s2} px<br>Tracking {tr}</p></div>
      <div class="tsample"><p class="{cls}">{sample}</p></div>
    </div>'''
    return out


def section_type():
    chips = ' '.join([chip('Variable', 'C1'), chip('Loop', 'R10'), chip('Reform', 'R-01'), chip('Connection', 'L25'),
                      chip('Area', 'C')])
    small = ' '.join([chip('Variable', 'C2', 'compact'), chip('Loop', 'B4', 'compact'), chip('Reform', 'R-01', 'compact')])
    return f'''
<section id="type" class="sec" aria-labelledby="h-type">
  <p class="eyebrow">02 Type scale</p>
  <h2 class="headline" id="h-type">Type for atlas pages</h2>
  <p class="t-deck measure">Three faces and sixteen styles. Nothing on the page sets under 13 px, measured at its rendered size, SVG text included. Every sample below is text from the model, except the caption and the eyebrow.</p>
  <div class="tlist">{type_rows()}
    <div class="trow">
      <div class="tspec"><p class="t-panel-s">ID chip</p><p class="t-legend dim">Every ID in text, panels, keys and lists (Gate 1, M3)</p>
        <p class="t-legend mono">Type word: Inter 600, 13 px, capitals, +0.06 em, in an ink cell<br>Code: Inter 700, 14 px, tabular, in a 1.5 px outlined cell<br>26 px tall; compact 22 px with a 13 px code</p></div>
      <div class="tsample"><p class="chips">{chips}</p><p class="chips">{small}</p></div>
    </div>
  </div>
</section>'''


def section_lines():
    grades = ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis']
    head = ''.join(f'<div class="lhead"><p class="t-panel-s">{w} px</p><p class="t-legend dim">{d}</p></div>'
                   for w, d in zip(WEIGHTS, ['Overview and context lines', 'A step in a close-up', 'The lit route']))
    rows = ''
    cw = 300
    for g in grades:
        word, gloss, tex = acc.GRADES[g]
        texname = {'solid': 'Solid', 'dashed': 'Dashed', 'dash-dot': 'Dash-dot', 'dotted': 'Dotted'}[tex]
        rec = '<span class="rec" aria-hidden="true"></span>' if g == 'documented' else ''
        cells = ''
        for w in WEIGHTS:
            x1 = cw - 8
            ln = coded_line(4, x1, 20, w, tex, CH)
            arr, cap = pattern(tex, w)
            arr_t = 'none' if arr is None else ' '.join(f'{x:g}' for x in arr)
            cells += (f'<div class="lcell"><svg data-view="line-{g}-{w}" width="{cw}" height="40" viewBox="0 0 {cw} 40" '
                      f'role="img" aria-label="{word}, {texname.lower()} line at {w} px">{ln}</svg>'
                      f'<p class="t-legend dim">Pattern {arr_t}{", round caps" if cap == "round" else ""}</p></div>')
        rows += (f'<div class="lrow"><div class="lspec"><p class="t-map">{rec}{word}</p>'
                 f'<p class="t-legend dim">{gloss.capitalize()}. {texname}. V7 value <code>{g}</code></p></div>{cells}</div>')
    # hollow line for conceptual steps
    hollow = ''
    for w in WEIGHTS:
        rail = 1 if w <= 3 else 2
        tot = w + 2 * rail
        yy = snap(20, tot)
        hollow += (f'<div class="lcell"><svg data-view="line-conceptual-{w}" width="{cw}" height="40" viewBox="0 0 {cw} 40" '
                   f'role="img" aria-label="Conceptual step, hollow line at {w} px">'
                   f'<path d="M4 {yy}H{cw - 8 - ARROW[w][0]}" stroke="{CH}" stroke-width="{tot}" fill="none"/>'
                   f'<path d="M4 {yy}H{cw - 8 - ARROW[w][0]}" stroke="{NP}" stroke-width="{w}" fill="none"/>'
                   f'<path d="M{cw - 8 - ARROW[w][0]} {yy - ARROW[w][1] / 2}L{cw - 8} {yy}L{cw - 8 - ARROW[w][0]} '
                   f'{yy + ARROW[w][1] / 2}Z" fill="{CH}"/></svg>'
                   f'<p class="t-legend dim">Rails {rail} px, gap {w} px</p></div>')
    rows += (f'<div class="lrow"><div class="lspec"><p class="t-map">Conceptual step</p><p class="t-legend dim">No '
             f'numbered connection yet, as in the sketched loops B2, B3 and R9. Hollow line (Gate 1, M1)</p></div>{hollow}</div>')

    # small-size proof: all textures at 2 px in 56 px runs
    tiny = ''
    for g in ['well-supported', 'plausible', 'plausible_contested', 'hypothesis']:
        word, gloss, tex = acc.GRADES[g]
        tiny += (f'<div class="tiny"><svg data-view="tiny-{g}" width="64" height="20" viewBox="0 0 64 20" role="img" '
                 f'aria-label="{word} at 2 px in a 56 px run">{coded_line(2, 62, 10, 2, tex, CH)}</svg>'
                 f'<span class="t-legend">{word}</span></div>')
    return f'''
<section id="lines" class="sec" aria-labelledby="h-lines">
  <p class="eyebrow">03 Evidence lines</p>
  <h2 class="headline" id="h-lines">The V7 evidence code at three weights</h2>
  <p class="t-deck measure">Each pattern is a multiple of its line’s width, so a texture keeps its shape from the overview to the lit route. The build stretches each pattern a little so every line starts and ends on ink. Charcoal on Newsprint, actual size.</p>
  <div class="ltable" role="group" aria-label="Evidence line textures">
    <div class="lrow lrow-head"><div class="lspec"><p class="t-legend dim">Grade, gloss and texture</p></div>{head}</div>
    {rows}
  </div>
  <div class="tinyrow"><p class="t-legend dim">The shortest run a texture may take: three full periods, here 56 px at 2 px.</p>{tiny}</div>
</section>'''


def step_figure(ground, ink, sub, cell, wid='step', red_target=False):
    """One step of R10, fully dressed: C2 to C3 over L25, read from the model."""
    a, b = N[L25['from']], N[L25['to']]
    W = 640
    y = 70
    ys = snap(y, 3)
    ax0, ax1 = 74, 146
    bx0, bx1 = 494, 566
    tex = acc.GRADES[L25['evidence']][2]
    line = coded_line(ax1 + 2, bx0 - 2, y, 3, tex, ink)
    tag = sign_tag(320, ys, L25['polarity'], 3, ink, ground, ground, 1)
    tk = ticks(ax1 + 14, ys, {'S': 1, 'M': 2, 'L': 3}[L25['delay']], 3, ink)
    node = lambda x0, x1, code: (f'<g data-node="{code}"><rect x="{x0}" y="{ys - 16.5}" width="{x1 - x0}" height="33" rx="16.5" '
                                 f'fill="{cell}" stroke="{ink}" stroke-width="2"/><text x="{(x0 + x1) / 2}" y="{ys}" '
                                 f'dominant-baseline="central" text-anchor="middle" class="nd" fill="{ink}">{code}</text></g>')
    ch, cw = svg_chip(0, 0, 'Connection', L25['id'], ink, ground)
    chip_g = f'<g transform="translate({round(320 - cw / 2)},{y + 23})">{ch}</g>'
    note = f'{grade_word(L25["evidence"])}: {grade_gloss(L25["evidence"])}. {acc.DELAYS[L25["delay"]].capitalize()}.'
    return f'''<svg data-view="{wid}" class="stepfig" width="{W}" height="176" viewBox="0 0 {W} 176" role="img"
      aria-label="Variable {a['id']}, {e(a['label'])}, {acc.SIGN_WORDS[L25['polarity']]} variable {b['id']}, {e(b['label'])}, over connection {L25['id']}: {e(L25['name'])}. {e(note)}">
      <text x="{(ax0 + ax1) / 2}" y="26" text-anchor="middle" class="st" fill="{ink}" data-name="{e(a['label'])}">{e(a['label'])}</text>
      <text x="{(bx0 + bx1) / 2}" y="26" text-anchor="middle" class="st" fill="{ink}" data-name="{e(b['label'])}">{e(b['label'])}</text>
      <g data-link="{L25['id']}" data-sign="{e(L25['polarity'])}" data-grade="{L25['evidence']}" data-delay="{L25['delay']}">{line}{tk}{tag}</g>
      {node(ax0, ax1, a['id'])}{node(bx0, bx1, b['id'])}{chip_g}
      <text x="320" y="{y + 66}" text-anchor="middle" class="mp" fill="{ink}">{e(L25['name'])}</text>
      <text x="320" y="{y + 88}" text-anchor="middle" class="nt" fill="{sub}">{e(note)}</text>
    </svg>'''


def section_signs():
    sign_rule = e(acc.SIGN_RULE)
    tags = ''
    for w in WEIGHTS:
        tags += (f'<svg data-view="tags-{w}" width="300" height="44" viewBox="0 0 300 44" role="img" '
                 f'aria-label="Plus and minus tags on a {w} px line">'
                 f'{coded_line(6, 140, 22, w, "solid", CH)}{sign_tag(70, snap(22, w), "+", w, CH, NP, NP, 1)}'
                 f'{coded_line(160, 294, 22, w, "solid", CH)}{sign_tag(227, snap(22, w), "-", w, CH, NP, NP, 1)}</svg>')
    arrows = ''
    for w in WEIGHTS:
        al, ab = ARROW[w]
        arrows += (f'<div class="ar"><svg data-view="arrow-{w}" width="96" height="40" viewBox="0 0 96 40" role="img" '
                   f'aria-label="Arrowhead for a {w} px line">{coded_line(6, 90, 20, w, "solid", CH)}</svg>'
                   f'<p class="t-legend dim">{w} px line: head {al} × {ab} px</p></div>')
    delays = ''
    for d, n in (('S', 1), ('M', 2), ('L', 3)):
        delays += (f'<div class="ar"><svg data-view="delay-{d}" width="96" height="40" viewBox="0 0 96 40" role="img" '
                   f'aria-label="Delay {acc.DELAYS[d]}: {n} tick{"s" if n > 1 else ""}">'
                   f'{coded_line(6, 90, 20, 3, "solid", CH)}{ticks(20, snap(20, 3), n, 3, CH)}</svg>'
                   f'<p class="t-legend dim">{acc.DELAYS[d].capitalize()}: {n} tick{"s" if n > 1 else ""}</p></div>')
    auth = (f'<svg data-view="authority" width="300" height="40" viewBox="0 0 300 40" role="img" '
            f'aria-label="Authority connection: open diamond, no sign">'
            f'<g data-link="{LE02["id"]}" data-sign="none" data-grade="{LE02["evidence"]}" data-delay="{LE02["delay"]}">'
            f'<path d="M6 20H282" stroke="{CH}" stroke-width="3" fill="none"/>{diamond(294, 20, CH, NP, 14)}</g></svg>')
    reds = ''
    for gname, g, ink, keyline in (('Newsprint', NP, CH, True), ('White', WH, CH, False),
                                    ('Charcoal', CH, NP, False), ('Prussian', PR, WH, None)):
        if keyline is None:
            mark = (f'<path d="M12 22H136" stroke="{WH}" stroke-width="6" fill="none"/>')
            note = f'No red. The job moves to a 6 px White line ({r2(WH, PR)}:1)'
        else:
            under = f'<path d="M12 22H136" stroke="{CH}" stroke-width="5" fill="none"/>' if keyline else ''
            mark = (f'<g data-red="working" data-red-job="specimen">{under}'
                    f'<path d="M12 22H136" stroke="{RED}" stroke-width="3" fill="none"/></g>')
            note = (f'Red {r2(RED, g)}:1, so a 1 px Charcoal keyline' if keyline else f'Red {r2(RED, g)}:1, bare')
        reds += (f'<div class="redsw"><svg data-view="red-{gname.lower()}" width="148" height="44" viewBox="0 0 148 44" '
                 f'role="img" aria-label="Working red on {gname}"><rect width="148" height="44" fill="{g}"/>{mark}</svg>'
                 f'<p class="t-legend"><strong>{gname}</strong></p><p class="t-legend dim">{note}</p></div>')
    return f'''
<section id="signs" class="sec" aria-labelledby="h-signs">
  <p class="eyebrow">04 Signs, ends and delay</p>
  <h2 class="headline" id="h-signs">One step, fully dressed</h2>
  <p class="t-deck measure">Step {STEP_NO} of {chip('Loop', 'R10', 'compact')}, read from the model. The sign rides the line in a pointing tag; one tick counts the delay; the label sits clear of every stroke.</p>
  <div class="stepgrid">
    <div class="stepwrap scroll" role="region" tabindex="0" aria-label="One step of Loop R10">{step_figure(WH, CH, DS, WH)}</div>
    <div class="stepkey">
      <p class="eyebrow">Key</p>
      <ul class="t-legend">
        <li><strong>Pill:</strong> a variable. Its code stands alone because this key names the type.</li>
        <li><strong>Tag:</strong> the step’s sign, pointing the way the step runs.</li>
        <li><strong>Tick:</strong> one per delay band. One tick: {acc.DELAYS['S']}.</li>
        <li><strong>Texture:</strong> the grade. Solid here: {grade_word(L25['evidence']).lower()}.</li>
      </ul>
      <p class="caption">{sign_rule}</p>
    </div>
  </div>
  <div class="signgrid">
    <div class="sg"><p class="t-panel-s">Sign tags</p><p class="t-legend dim">Tags 16 × 20 px on 2 px lines, 17 × 21 px on 3 px lines, 22 × 26 px on the lit route. The sign is drawn, its bars as heavy as the line up to 3 px. Never colored.</p>{tags}</div>
    <div class="sg"><p class="t-panel-s">Arrowheads</p><p class="t-legend dim">One closed, filled head, sized by weight. The line stops at the head’s base. Tip 2 px off the target’s edge.</p><div class="arrows">{arrows}</div></div>
    <div class="sg"><p class="t-panel-s">Delay</p><p class="t-legend dim">Ticks 2 px wide, 5 px apart, 12 px after the tail, with the words in the label.</p><div class="arrows">{delays}</div></div>
    <div class="sg"><p class="t-panel-s">Authority</p><p class="t-legend dim">An open diamond, no sign, never part of a loop. Example from the model:</p><p class="chips">{chip('Connection', LE02['id'], 'compact')}</p><p class="t-legend" style="margin:6px 0 10px">{e(LE02['name'])}</p>{auth}</div>
  </div>
  <div class="redrow"><p class="t-panel-s">Working red on each ground</p><p class="t-legend dim">Specimens, which Rule 05.3 does not count.</p><div class="reds">{reds}</div></div>
</section>'''


def section_grounds():
    grounds = [
        ('Newsprint', NP, CH, DS, 'Deep Stone', ST, 'red-black', 'black', True,
         'The brand’s lead ground. Overviews read as a broadsheet, the loop catalog, long reading.'),
        ('White', WH, CH, DS, 'Deep Stone', ST, 'red-black', 'black', True,
         'Cards and panels on Newsprint, dense close-ups, plates meant for print.'),
        ('Charcoal', CH, NP, NP, 'Newsprint', ST, 'red-newsprint', 'newsprint', True,
         'Night schematics and dense wiring, where light lines separate cleanly.'),
        ('Prussian', PR, WH, NP, 'Newsprint', None, 'newsprint', 'newsprint', False,
         'Wall and poster grounds. No red of any kind: weight and fill carry selection.'),
    ]
    panels = ''
    for i, (name, g, ink, sub, subname, ctx, ed_cur, ed_other, red_ok, suits) in enumerate(grounds):
        dark = name in ('Charcoal', 'Prussian')
        inkname = {CH: 'Charcoal', NP: 'Newsprint', WH: 'White'}[ink]
        ctx_line = (f'<path d="M0 50H120" stroke="{ctx}" stroke-width="2"/>' if ctx else
                    f'<path d="M0 50H120" stroke="{sub}" stroke-width="2"/>')
        ctx_name = (f'Stone {r2(ctx, g)}:1, 2 px or heavier' if ctx else f'{subname} {r2(sub, g)}:1, by weight alone')
        lines = (f'<svg data-view="ground-lines-{name.lower()}" width="260" height="64" viewBox="0 0 260 64" role="img" '
                 f'aria-label="Lines on {name}">'
                 f'{coded_line(0, 120, 14, 3, "solid", ink)}{coded_line(136, 256, 14, 3, "dashed", ink)}'
                 f'{ctx_line}<path d="M136 50.5H256" stroke="{ink}" stroke-width="1"/></svg>')
        cur = acc.icon_svg(acc.VARIABLE_ICON['C1'], ed_cur, uid=f'g{i}a', size=64)
        oth = acc.icon_svg(acc.VARIABLE_ICON['C2'], ed_other, uid=f'g{i}b', size=64)
        red_attr = ' data-red="working" data-red-job="current item"' if red_ok else ''
        if red_ok:
            red_note = (f'Current icon keeps its red ({r2(RED, g)}:1). '
                        + ('Red marks need a 1 px Charcoal keyline here.' if name == 'Newsprint' else 'Red marks sit bare.'))
        else:
            red_note = 'Red never sits on Prussian, so both icons go one color.'
        ch_cell = {NP: NP, WH: WH, CH: CH, PR: PR}[g]
        panels += f'''
    <div class="ground g-{name.lower()}" style="background:{g};color:{ink}">
      <p class="t-panel">{name}</p>
      <p class="t-legend gsub">{g} · {e(suits)}</p>
      <p class="chips">{chip('Variable', 'C1', 'on-' + name.lower())}</p>
      <dl class="gratios">
        <div><dt class="t-ptext">Primary text</dt><dd class="t-legend">{inkname} {r2(ink, g)}:1</dd></div>
        <div><dt class="t-ptext" style="color:{sub}">Secondary text</dt><dd class="t-legend">{subname} {r2(sub, g)}:1</dd></div>
      </dl>
      {lines}
      <p class="t-legend gsub">Top: essential lines, {inkname} {r2(ink, g)}:1. Bottom: context, {ctx_name}; hairline 1 px.</p>
      <div class="icons" role="list">
        <div class="ic cur" role="listitem"><span class="icw"{red_attr}>{cur}</span><span class="t-map icl" data-node="C1" data-name="{e(N['C1']['label'])}">{e(N['C1']['label'])}</span><span class="t-legend">Current</span></div>
        <div class="ic" role="listitem"><span class="icw">{oth}</span><span class="t-map icl2" data-node="C2" data-name="{e(N['C2']['label'])}">{e(N['C2']['label'])}</span></div>
      </div>
      <p class="t-legend gsub">{e(red_note)} Icons at 64 px. The floor is 48 px for this icon and for any red edition.</p>
    </div>'''
    return f'''
<section id="grounds" class="sec" aria-labelledby="h-grounds">
  <p class="eyebrow">05 Grounds and icons</p>
  <h2 class="headline" id="h-grounds">Four grounds, two Civic Line icons on each</h2>
  <p class="t-deck measure">Ratios are computed from the locked hex values with the WCAG formula. The row shows {e(N['C1']['label'])} as the current item, so only its icon keeps the red.</p>
  <div class="grounds">{panels}</div>
</section>'''


# ---------------------------------------------------------------- page
CSS = f'''
:root{{--np:{NP};--ch:{CH};--red:{RED};--pr:{PR};--st:{ST};--vg:{VG};--wh:{WH};--ds:{DS};
--disp:"Inter Tight",system-ui,sans-serif;--body:"Inter",system-ui,sans-serif;--quote:"Lora",Georgia,serif}}
*{{box-sizing:border-box}}
.lede>*,.frames>*,.trow>*,.lrow>*,.signgrid>*,.grounds>*,.reds>*,.stepgrid>*,.mast>*,footer>*{{min-width:0}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--np);color:var(--ch);font:400 17px/27px var(--body);font-feature-settings:"kern" 1}}
.wrap{{max-width:1440px;margin:0 auto;padding:0 64px}}
a{{color:inherit}}
a:focus-visible,[tabindex]:focus-visible{{outline:2px solid var(--vg);outline-offset:2px}}
p,dl,dd,figure{{margin:0}}
h1,h2{{margin:0}}
/* masthead */
.mast{{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:center;height:72px;border-bottom:1px solid var(--st)}}
.wm{{grid-column:1/4;display:block;width:221px;padding:0;align-self:start;margin-top:24px}}
.wm .wm16{{display:none!important}}
.runhead{{grid-column:4/8;font:700 13px/18px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--ds)}}
.views{{grid-column:8/13;justify-self:end;display:flex;gap:4px}}
.views a{{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;font:600 15px/18px var(--body);text-decoration:none;color:var(--ds);border-bottom:3px solid transparent}}
.views a[aria-current]{{color:var(--ch);border-bottom-color:var(--ch)}}
.views a:hover{{text-decoration:underline;text-underline-offset:4px}}
.crumbs ol{{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:0 8px;font:500 14px/20px var(--body);color:var(--ds)}}
.crumbs li+li::before{{content:"/";margin-right:8px;color:var(--ds)}}
.crumbs a{{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}}
.crumbs [aria-current]{{color:var(--ch);font-weight:600}}
.lede{{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;margin-top:24px;padding-bottom:40px;border-bottom:1px solid var(--st)}}
.lede-main{{grid-column:1/9}}
.lede-key{{grid-column:9/13;padding-top:8px}}
.lede-key li{{margin-bottom:6px}}
.lede-key ul{{margin:8px 0 0;padding:0;list-style:none}}
/* type styles */
.t-display{{font:800 56px/60px var(--disp);letter-spacing:-.035em;margin-left:-.04em;text-wrap:balance}}
.t-headline,.headline{{font:800 40px/44px var(--disp);letter-spacing:-.03em;text-wrap:balance}}
.t-deck{{font:400 19px/28px var(--body)}}
.measure{{max-width:40rem}}
.t-panel{{font:800 22px/26px var(--disp);letter-spacing:-.02em}}
.t-panel-s{{font:800 18px/22px var(--disp);letter-spacing:-.015em}}
.t-eyebrow,.eyebrow{{font:700 13px/18px var(--body);letter-spacing:.06em;text-transform:uppercase}}
.t-body{{font:400 17px/27px var(--body);max-width:42rem}}
.t-ptext{{font:400 15px/23px var(--body);max-width:36rem}}
.t-quote{{font:italic 400 22px/31px var(--quote);letter-spacing:-.005em;max-width:44rem}}
.t-figure{{font:800 40px/40px var(--disp);letter-spacing:-.03em;font-feature-settings:"tnum" 1}}
.t-figure .t-legend{{letter-spacing:0;margin-left:6px}}
.t-station{{font:700 20px/22px var(--disp);letter-spacing:-.01em}}
.t-map{{font:600 15px/18px var(--body)}}
.t-note{{font:400 13px/16px var(--body);letter-spacing:.01em}}
.t-caption,.caption{{font:400 14px/20px var(--body)}}
.t-legend{{font:500 13px/18px var(--body)}}
.t-source{{font:400 13px/18px var(--body);color:var(--ds)}}
.dim{{color:var(--ds)}}
.mono{{font-feature-settings:"tnum" 1;margin-top:4px}}
code{{font:500 13px/18px var(--body);font-feature-settings:"tnum" 1}}
/* chips */
.chip{{display:inline-flex;align-items:stretch;min-height:26px;vertical-align:middle;white-space:nowrap;color:var(--ch)}}
.chip .k{{display:inline-flex;align-items:center;padding:0 7px;background:var(--ch);color:var(--np);border:1.5px solid var(--ch);font:600 13px/1 var(--body);letter-spacing:.06em;text-transform:uppercase}}
.chip .c{{display:inline-flex;align-items:center;padding:0 8px;border:1.5px solid var(--ch);border-left:0;font:700 14px/1 var(--body);font-feature-settings:"tnum" 1}}
.chip.compact{{min-height:22px}}
.chip.compact .c{{font-size:13px;padding:0 7px}}
.chip.on-white .k{{color:var(--wh)}}
.chip.on-charcoal .k{{background:var(--np);color:var(--ch);border-color:var(--np)}}
.chip.on-charcoal .c{{color:var(--np);border-color:var(--np)}}
.chip.on-prussian .k{{background:var(--wh);color:var(--pr);border-color:var(--wh)}}
.chip.on-prussian .c{{color:var(--wh);border-color:var(--wh)}}
.chips{{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center}}
.chips+.chips{{margin-top:12px}}
/* sections */
.sec{{padding:56px 0;border-bottom:1px solid var(--st)}}
.sec .headline{{margin:8px 0 12px}}
.sec .t-deck{{margin-bottom:32px}}
.frames{{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:start}}
.fig-wide{{grid-column:1/9}}
.fig-phone{{grid-column:9/13}}
.frames figcaption{{margin-top:12px;max-width:38rem}}
.frame .z{{stroke:var(--st);stroke-width:1}}
.frame .blk2{{opacity:1}}
.frame .fold{{stroke:var(--ch);stroke-width:1}}
.frame .leader{{fill:none;stroke:var(--st);stroke-width:1}}
.frame .lab{{font:500 13px/18px var(--body);fill:var(--ch)}}
.frame .lab.in{{font-weight:600}}
.scroll{{overflow-x:auto;max-width:100%}}
.tlist{{border-top:1px solid var(--st)}}
.trow{{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;padding:20px 0;border-bottom:1px solid var(--st);align-items:baseline}}
.tspec{{grid-column:1/4}}
.tsample{{grid-column:4/13}}
.tspec .t-legend{{margin-top:4px}}
/* lines */
.ltable{{border-top:1px solid var(--st)}}
.lrow{{display:grid;grid-template-columns:3fr 3fr 3fr 3fr;column-gap:24px;padding:16px 0;border-bottom:1px solid var(--st);align-items:center}}
.lrow-head{{padding:12px 0}}
.lspec .t-legend{{margin-top:4px}}
.lcell svg{{display:block}}
.lcell .t-legend{{margin-top:2px}}
.rec{{display:inline-block;width:7px;height:7px;background:var(--ch);margin-right:7px;vertical-align:2px}}
.tinyrow{{display:flex;flex-wrap:wrap;gap:12px 32px;align-items:center;margin-top:20px}}
.tiny{{display:flex;align-items:center;gap:8px}}
/* signs */
.stepgrid{{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:start}}
.stepwrap{{grid-column:1/9;background:var(--wh);padding:20px 24px 12px}}
.stepwrap svg{{display:block;margin:0 auto}}
.stepkey{{grid-column:9/13;padding-top:4px}}
.stepkey ul{{list-style:none;margin:8px 0 16px;padding:0}}
.stepkey li{{padding:6px 0;border-top:1px solid var(--st)}}
.stepkey strong{{font-weight:700}}
.stepfig .st{{font:700 20px/22px var(--disp);letter-spacing:-.01em}}
.stepfig .nd{{font:700 14px/1 var(--body);font-feature-settings:"tnum" 1}}
.stepfig .mp{{font:600 15px/18px var(--body);paint-order:stroke;stroke:var(--wh);stroke-width:4px;stroke-linejoin:round}}
.stepfig .nt{{font:400 13px/16px var(--body);letter-spacing:.01em}}
.svgchip .sc-k{{font:600 13px/1 var(--body);letter-spacing:.06em}}
.svgchip .sc-c{{font:700 13px/1 var(--body);font-feature-settings:"tnum" 1}}
.signgrid{{display:grid;grid-template-columns:repeat(4,1fr);column-gap:24px;row-gap:32px;margin-top:40px}}
.sg .t-legend{{margin:4px 0 12px}}
.sg svg{{display:block;margin-bottom:8px}}
.arrows{{display:flex;flex-direction:column;gap:4px}}
.ar .t-legend{{margin:0 0 4px}}
.redrow{{margin-top:40px}}
.redrow>.t-legend{{margin:4px 0 12px}}
.reds{{display:grid;grid-template-columns:repeat(4,1fr);column-gap:24px}}
.redsw svg{{display:block;margin-bottom:8px}}
/* grounds */
.grounds{{display:grid;grid-template-columns:repeat(4,1fr);column-gap:24px;row-gap:24px}}
.ground{{padding:24px;min-height:100%}}
.g-newsprint{{box-shadow:inset 0 0 0 1px var(--st)}}
.ground .gsub{{margin:6px 0 16px}}
.ground .chips{{margin-bottom:16px}}
.gratios div{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:6px 0;border-top:1px solid currentColor}}
.gratios{{margin-bottom:16px}}
.gratios dd{{font-feature-settings:"tnum" 1}}
.ground svg{{display:block}}
.g-charcoal .t-legend,.g-prussian .t-legend,.g-charcoal .t-ptext,.g-prussian .t-ptext{{font-weight:500}}
.g-newsprint .gsub,.g-white .gsub{{color:var(--ds)}}
.icons{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:8px 0 4px}}
.ic{{display:flex;flex-direction:column;align-items:flex-start;gap:6px}}
.ic .icw{{display:block;width:64px;height:64px}}
.ic.cur .icl{{font-weight:700;padding-bottom:4px;border-bottom:3px solid currentColor}}
.ic .icl2{{padding-bottom:7px}}
footer{{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;padding:16px 0 40px}}
footer .t-source{{grid-column:1/9}}
footer .right{{grid-column:9/13;text-align:right}}
@media (max-width:1180px){{
 .signgrid{{grid-template-columns:repeat(2,1fr)}}
 .grounds,.reds{{grid-template-columns:repeat(2,1fr)}}
 .lrow{{grid-template-columns:1fr 1fr}} .lrow .lspec{{grid-column:1/-1}} .lrow-head{{display:none}}
}}
@media (max-width:600px){{
 .wrap{{padding:0 20px}}
 .mast{{grid-template-columns:repeat(4,1fr);column-gap:16px;height:auto;padding:20px 0 0;row-gap:16px;border-bottom:0}}
 .wm{{grid-column:1/-1;width:152px;margin-top:0}}
 .wm .wm24{{display:none!important}} .wm .wm16{{display:block!important}}
 .runhead{{display:none}}
 .views{{grid-column:1/-1;justify-self:stretch;display:grid;grid-template-columns:1fr 1fr 1fr;gap:0 16px;border-bottom:1px solid var(--st)}}
 .views a{{padding:0}}
 .lede{{grid-template-columns:1fr;row-gap:24px}} .lede-main,.lede-key{{grid-column:1/-1}}
 .t-display{{font-size:36px;line-height:40px;letter-spacing:-.03em}}
 .t-headline,.headline{{font-size:30px;line-height:34px}}
 .t-deck{{font-size:17px;line-height:25px}}
 .t-panel{{font-size:20px;line-height:24px}}
 .t-body{{font-size:16px;line-height:25px}}
 .t-quote{{font-size:19px;line-height:27px}}
 .t-figure{{font-size:32px;line-height:32px}}
 .t-station{{font-size:18px;line-height:20px}}
 .frames,.trow,.stepgrid{{grid-template-columns:1fr}} .fig-wide,.fig-phone,.tspec,.tsample,.stepwrap,.stepkey{{grid-column:1/-1}}
 .stepwrap{{padding:16px}} .stepkey{{margin-top:16px}}
 .fig-phone{{margin-top:32px}} .tsample{{margin-top:12px}}
 .lrow{{grid-template-columns:1fr}}
 .signgrid,.grounds,.reds{{grid-template-columns:1fr}}
 .sec{{padding:40px 0}}
 footer{{grid-template-columns:1fr;row-gap:8px}} footer .t-source,footer .right{{grid-column:1/-1;text-align:left}}
}}
'''


def build():
    wm, wm_w = wordmark()
    wm16, wm16_w = wordmark(16, 'wordmark/20261028_Wordmark-16px-Master.svg')
    assert abs(wm_w - 221) < 1 and abs(wm16_w - 152) < 1
    wm = wm.replace('<svg ', '<svg class="wm24" ', 1)
    wm16 = wm16.replace('<svg ', '<svg class="wm16" ', 1)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas Type and Line Specimen</title>
<meta name="description" content="The shared craft layer for the twelve atlas concepts: type scale, ID chips, evidence lines, sign marks, grounds and icons.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap" id="top">
<header class="mast">
  <a class="wm" href="#top" data-red="signature">{wm}{wm16}</a>
  <p class="runhead">Atlas concepts / Shared frame</p>
  <nav class="views" aria-label="Sections">
    <a href="#frame" aria-current="page">Frame</a><a href="#type">Type</a><a href="#lines">Lines</a><a href="#signs">Signs</a><a href="#grounds">Grounds</a>
  </nav>
</header>
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="#top">Atlas concepts</a></li><li><a href="#top">Shared frame</a></li><li aria-current="page">Type and line specimen</li></ol></nav>
<main>
<div class="lede">
  <div class="lede-main">
    <h1 class="t-display">The atlas type and line specimen</h1>
    <p class="t-deck measure" style="margin-top:16px">Twelve concepts share these sizes, strokes, marks and grounds, so each one differs only in its big idea. Everything here sits at actual size for a 1440 px screen, and the 390 px sizes switch in on a phone. Read it beside the design frame memo of October 30, 2026.</p>
  </div>
  <div class="lede-key">
    <p class="eyebrow">This page holds</p>
    <ul class="t-legend">
      <li>The page frame at 1440 and 390 px</li>
      <li>Sixteen type styles and the ID chip</li>
      <li>Five grades at 2, 3 and 6 px</li>
      <li>Sign tags, arrowheads, delay, authority</li>
      <li>Four grounds with measured ratios</li>
    </ul>
  </div>
</div>
{section_frame()}
{section_type()}
{section_lines()}
{section_signs()}
{section_grounds()}
</main>
<footer><p class="t-source">{SOURCE}</p><p class="t-source right">Shared frame specimen. Studio draft, October 30, 2026.</p></footer>
</div>
</body>
</html>
'''
    out = HERE / '20261030_Atlas-Type-And-Line-Specimen.html'
    out.write_text(page)
    print('wrote', out.relative_to(ROOT), len(page), 'bytes')


if __name__ == '__main__':
    build()
