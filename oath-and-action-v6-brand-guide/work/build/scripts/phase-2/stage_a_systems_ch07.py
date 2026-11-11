"""Chapter 07 Layout and spacing: copy, rules and specimens (stage board A, systems designer, November 6, 2026).

Grid geometry comes from oa.layout.grid in tokens.json. Characters per line for each column span are measured in
Chromium with 7,000 characters of chapter 02's prose at 17 px Inter (stage_a_systems_capture.js).
"""
import sys

C = sys.modules['stage_a_systems_core']
B = sys.modules['stage_a_systems_build']
SAMPLE = sys.modules['stage_a_systems_ch06'].SAMPLE        # shown on the plates (D2-248)
LONG = sys.modules['stage_a_systems_ch06'].long_sample()   # measured: 7,000 characters of chapter 02's prose

BPS = [('wide', 1440), ('desktop', 1024), ('tablet', 768), ('phone', 390), ('phoneSmall', 360)]
BNAME = {'wide': 'Wide', 'desktop': 'Desktop', 'tablet': 'Tablet', 'phone': 'Phone', 'phoneSmall': 'Small phone'}
SPACE = ['050', '100', '150', '200', '300', '400', '500', '600', '800', '1000', '1300']


def grid(ctx, name):
    T = ctx.T
    cols = int(T.value(f'oa.layout.grid.{name}.columns'))
    gut = T.px(f'oa.layout.grid.{name}.gutter')
    mar = T.px(f'oa.layout.grid.{name}.margin')
    width = T.px(f'oa.layout.breakpoint.{name}')
    colw = (width - 2 * mar - (cols - 1) * gut) / cols
    return {'cols': cols, 'gutter': gut, 'margin': mar, 'width': width, 'col': colw}


def span_w(g, n):
    return n * g['col'] + (n - 1) * g['gutter']


def candidates(g):
    if g['cols'] == 4:
        return [4]
    return list(range(3, g['cols'] + 1))


def probes(ctx):
    for name, _ in BPS:
        g = grid(ctx, name)
        for n in candidates(g):
            ctx.probe(f'cpl span {name} {n}', 'cpl', text=LONG, css=f'font:var(--oa-type-body);width:{span_w(g, n):.2f}px')
    g = grid(ctx, 'wide')
    ctx.probe('cpl 200 percent in five columns', 'cpl', text=LONG,
              css=f'font:var(--oa-type-body);font-size:2.125rem;width:{span_w(g, 5):.2f}px')
    ctx.probe('cpl 200 percent sample', 'cpl', text=SAMPLE,
              css=f'font:var(--oa-type-body);font-size:2.125rem;width:{span_w(g, 5):.2f}px')


def pick_span(ctx, name):
    g = grid(ctx, name)
    best = None
    for n in candidates(g):
        r = ctx.R.get(f'cpl span {name} {n}')
        if not r:
            continue
        ok = 60 <= r['mean'] <= 75
        score = abs(r['mean'] - 68)
        if g['cols'] == 4 or (ok and (best is None or score < best[1])):
            best = (n, score, r)
    return best


# ------------------------------------------------------------------------------------------------ specimens
def s_07_1(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    ink = v('oa.color.graphic.essential.onNewsprint')
    rows = []
    for k in SPACE:
        px = ctx.T.px(f'oa.space.{k}')
        rem = ctx.T.dim(f'oa.space.{k}')[0]
        rows.append(f'<li><code>{C.css_name("oa.space." + k)}</code><span class="n">{px:g} px · {rem:g} rem</span>'
                    f'<span class="bar" style="width:{v("oa.space." + k)}"></span></li>')
    css = (f'.rl{{list-style:none;margin:0;padding:0}}'
           f'.rl li{{display:grid;grid-template-columns:10rem 7.5rem 1fr;gap:12px;align-items:center;min-height:32px;'
           f'border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'code{{{ctx.ty("caption")}}}.n{{{ctx.ty("dataLabel")}}}.bar{{display:block;height:12px;background:{ink}}}'
           f'@container (max-width:28rem){{.rl li{{grid-template-columns:1fr 1fr;padding:6px 0}}.bar{{grid-column:1 / -1}}}}'
           f'.wr{{container-type:inline-size}}' + card_css(ctx))
    html = (f'<style>{css}</style><div class="wr"><ul class="rl">{"".join(rows)}</ul>'
            f'{card(ctx, ("var(--oa-space-300)", "var(--oa-space-100)", "var(--oa-space-200)"), ("24", "8", "16"))}</div>')
    ctx.spec('s-07-1-correct', html, '07', '07.1',
             'The spacing scale at true size: eleven bars from 4 px to 104 px, each with its token name and its value in px '
             'and rem. Below it, an Illustrative story card spaced on the scale, with 24 px padding, 8 px from kicker to '
             'heading and 16 px from heading to text, each gap marked.', illustrative=True,
             notes='Bar lengths are the space tokens themselves.')
    css2 = card_css(ctx)
    html2 = f'<style>{css2}</style>{card(ctx, ("22px", "13px", "37px"), ("22", "13", "37"))}'
    ctx.spec('s-07-1-failure', html2, '07', '07.1',
             'The same Illustrative story card with gaps of 22, 13 and 37 px, each marked, none of them a step on the scale.',
             illustrative=True, width=420, notes='Off-scale gaps written in px on purpose.')


def card_css(ctx):
    v = ctx.v
    return (f'.cd{{position:relative;max-width:26rem;margin-top:32px;background:{v("oa.color.surface.white")};'
            f'box-shadow:inset 0 0 0 1px {v("oa.color.border.hairline.onNewsprint")}}}'
            f'.ey{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0;{ctx.ty("label")};color:{v("oa.color.text.secondary.onWhite")}}}'
            f'.hd{{margin:0;{ctx.ty("h4", "floor")};text-wrap:balance}}.bt{{margin:0;{ctx.ty("body")}}}'
            f'.gp{{display:block;background:{v("oa.color.tint.verdigrisN82")}}}'
            f'.ky{{display:flex;gap:8px;align-items:baseline;max-width:26rem;margin:12px 0 0;{ctx.ty("caption")};color:{v("oa.color.text.secondary.onNewsprint")}}}'
            f'.kw{{flex:none;width:12px;height:12px;background:{v("oa.color.tint.verdigrisN82")};box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}}}')


def card(ctx, gaps, labels):
    pad, a, b = gaps
    la, lb_, lc = labels
    # The gaps are drawn as tinted bands so the spacing shows; a key under the card names them.
    return (f'<div class="cd" style="padding:{pad}">'
            f'<p class="ey"><span>Act · How to take part</span>{B.ILLUS}</p>'
            f'<div class="gp" style="height:{a}"></div>'
            f'<p class="hd">Budget hearing moves to May 12</p>'
            f'<div class="gp" style="height:{b}"></div>'
            f'<p class="bt">The council will take public comment before it votes on the city budget the same night.</p></div>'
            f'<p class="ky"><span class="kw"></span>Tinted bands mark the gaps: {lb_} px from kicker to heading and {lc} px '
            f'from heading to text. The card’s padding is {la} px on every side.</p>')


def grid_svg(ctx, name, scale=0.25, highlight=None, sections=None, text_band=None, H=None):
    g = grid(ctx, name)
    W = g['width'] * scale
    H = H or (120 if not sections else 180)
    v = ctx.v
    col = v('oa.color.tint.stoneN70')
    edge = v('oa.color.border.strong.onNewsprint')
    page = v('oa.color.surface.white')
    hl = v('oa.color.tint.verdigrisN52p75')
    parts = [f'<rect x="0.5" y="0.5" width="{W - 1:.2f}" height="{H - 1}" fill="{page}" stroke="{edge}" stroke-width="1"/>']
    if sections:
        sh = (H - 8) / len(sections)
        for i, n in enumerate(sections):
            gg = dict(g)
            gg['cols'] = n
            gg['col'] = (g['width'] - 2 * g['margin'] - (n - 1) * g['gutter']) / n
            y = 4 + i * sh
            for c in range(n):
                x = (g['margin'] + c * (gg['col'] + g['gutter'])) * scale
                parts.append(f'<rect x="{x:.2f}" y="{y + 3:.2f}" width="{gg["col"] * scale:.2f}" height="{sh - 6:.2f}" fill="{col}"/>')
    else:
        for c in range(g['cols']):
            x = (g['margin'] + c * (g['col'] + g['gutter'])) * scale
            fill = hl if highlight and c < highlight else col
            parts.append(f'<rect x="{x:.2f}" y="8" width="{g["col"] * scale:.2f}" height="{H - 16}" fill="{fill}"/>')
        if text_band:
            x0 = g['margin'] * scale
            w = span_w(g, text_band) * scale
            for i in range(9):
                parts.append(f'<rect x="{x0:.2f}" y="{20 + i * 9}" width="{w:.2f}" height="3" fill="{edge}"/>')
        if highlight:
            x0 = g['margin'] * scale
            for i in range(9):
                parts.append(f'<rect x="{x0:.2f}" y="{20 + i * 9}" width="{span_w(g, highlight) * scale:.2f}" height="3" fill="{edge}"/>')
    return (f'<svg width="{W:.2f}" height="{H}" viewBox="0 0 {W:.2f} {H}" aria-hidden="true" style="display:block;max-width:none">'
            + ''.join(parts) + '</svg>'), g


def s_07_2(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    items = []
    for name, w in BPS:
        svg, g = grid_svg(ctx, name)
        items.append(f'<li>{svg}<p class="nm">{BNAME[name]}, {w:g} px</p><p class="sp">{g["cols"]} columns of '
                     f'{g["col"]:.1f} px · {g["gutter"]:g} px gutters · {g["margin"]:g} px margins</p></li>')
        ctx.fig(f'column width {name}', f'{g["col"]:.2f}', '(width − 2 × margin − (columns − 1) × gutter) ÷ columns, from tokens.json')
    css = (f'ul{{list-style:none;margin:0;padding:{v("oa.space.300")};display:flex;flex-direction:column;gap:24px}}'
           f'.nm{{margin:8px 0 0;{ctx.ty("ui")}}}.sp{{margin:2px 0 0;{ctx.ty("caption")};color:{sec}}}')
    ctx.spec('s-07-2-correct', f'<style>{css}</style><ul>{"".join(items)}</ul>', '07', '07.2',
             'The five column grids drawn at one quarter of true size, each with its columns, gutters and margins: ' +
             '; '.join(f'{BNAME[n]} {w} px, {grid(ctx, n)["cols"]} columns of {grid(ctx, n)["col"]:.1f} px' for n, w in BPS) + '.',
             width=360 + 2 * int(ctx.T.px('oa.space.300')), scale=0.25,
             notes='Drawn at one quarter of each width, so the 1440 px grid takes 360 px, inside the 24 px inset every '
                   'plate keeps (Gate 2 fix pass, CD-S6); the labels under each drawing are at true size. Column widths '
                   'computed from the grid tokens.')
    svg, g = grid_svg(ctx, 'wide', sections=[3, 5, 2])
    cssf = (f'.nm{{margin:8px 0 0;{ctx.ty("ui")}}}.sp{{margin:2px 0 0;{ctx.ty("caption")};color:{sec}}}')
    ctx.spec('s-07-2-failure', f'<style>{cssf}</style>{svg}<p class="nm">Wide, 1440 px, at one quarter size</p>'
                               f'<p class="sp">Three sections on three, five and two columns</p>', '07', '07.2',
             'A page at 1440 px drawn at one quarter size, with three sections on three, five and two columns whose edges '
             'never line up.', width=360, scale=0.25, notes='A diagram at one quarter size.')


def s_07_opener(ctx):
    """Chapter 07's opener (Gate 2 fix pass, call 3, CD-S1): Rule 07.2's five grids drawn lighter, at one eighth size and
    side by side, so their widths compare at a glance. Each frame keeps its true proportion of width, and all share one
    height. A picture that flows with the column: one row from about 45rem, wrapping below."""
    sec = ctx.v('oa.color.text.secondary.onNewsprint')
    items = []
    for name, w in BPS:
        svg, g = grid_svg(ctx, name, scale=0.125, H=88)
        items.append(f'<li>{svg}<p class="nm">{BNAME[name]}</p><p class="sp">{w:g} px · {g["cols"]} columns</p></li>')
    css = (f'.gr{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:flex-start;gap:20px 24px}}'
           f'.gr li{{min-width:6rem}}.nm{{margin:8px 0 0;{ctx.ty("ui")}}}.sp{{margin:2px 0 0;{ctx.ty("caption")};color:{sec}}}'
           f'.sc{{margin:16px 0 0;{ctx.ty("label")};color:{sec}}}')
    html = f'<style>{css}</style><ul class="gr">{"".join(items)}</ul><p class="sc">Drawn at one eighth size</p>'
    ctx.spec('s-07-opener', html, '07', None,
             'The five column grids side by side at one eighth of true size, so their widths compare: ' +
             '; '.join(f'{BNAME[n]}, {w} px, {grid(ctx, n)["cols"]} columns' for n, w in BPS) +
             '. Rule 07.2 draws each one with its gutters and margins.',
             notes='Chapter 07’s opener (Gate 2 fix pass, call 3, CD-S1): Rule 07.2’s grid drawing at one eighth size, '
                   'every frame one height, column widths from the grid tokens.')


def s_07_3(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    rows = []
    picks = {}
    for name, w in BPS:
        best = pick_span(ctx, name)
        g = grid(ctx, name)
        if not best:
            n, r = g['cols'], {'mean': 0, 'min': 0, 'max': 0}
        else:
            n, _, r = best
        picks[name] = (n, r, g)
        rows.append(f'<tr><th scope="row">{BNAME[name]}, {w:g} px</th><td data-k="Body span">{n} of {g["cols"]}</td>'
                    f'<td data-k="Span width">{span_w(g, n):.0f} px</td>'
                    f'<td data-k="Characters a line">{r["mean"]:.0f} ({r["min"]} to {r["max"]})</td></tr>')
        ctx.fig(f'body span {name}', f'{n} of {g["cols"]} columns, {span_w(g, n):.1f} px, {r["mean"]:.1f} characters a line',
                'chapter 02 prose at 17 px Inter, Chromium, full lines only')
    # the correct application: the 1440 px grid at one quarter size, with the text span marked
    svg, g = grid_svg(ctx, 'wide', highlight=picks['wide'][0])
    css = (f'.cp{{margin:8px 0 0;{ctx.ty("caption")};color:{sec}}}.nm{{margin:8px 0 0;{ctx.ty("ui")}}}')
    ctx.spec('s-07-3-correct', f'<style>{css}</style>{svg}<p class="nm">Wide, 1440 px, at one quarter size</p>'
                               f'<p class="cp">Body text spans the first {picks["wide"][0]} of 12 columns, '
                               f'{span_w(g, picks["wide"][0]):.0f} px at true size.</p>', '07', '07.3',
             f'The 1440 px grid drawn at one quarter size, with body text spanning the first {picks["wide"][0]} of 12 columns, '
             f'{span_w(g, picks["wide"][0]):.0f} px at true size.', width=360, scale=0.25,
             notes='A diagram at one quarter size; the span is the one whose measured mean sits nearest 68 within 60 to 75.')
    # the span at every width, as a readable table
    css = (f'table{{width:100%;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
           f'th,td{{text-align:left;padding:8px 12px 8px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")};vertical-align:baseline}}'
           f'thead th{{{ctx.ty("label")};border-bottom-color:{v("oa.color.border.strong.onNewsprint")}}}'
           f'tbody th{{font-weight:600}}td{{font-variant-numeric:tabular-nums}}'
           f'@container (max-width:30rem){{thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}'
           f'table,tbody,tr,th,td{{display:block}}tr{{padding:8px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'th,td{{border:0;padding:0}}td::before{{content:attr(data-k) ": ";color:{sec}}}}}.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr"><table role="table"><thead><tr><th scope="col">Width</th><th scope="col">Body span</th>'
            f'<th scope="col">Span width</th><th scope="col">Characters a line, mean (range)</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')
    ctx.spec('s-07-spans', html, '07', None,
             'A table of each width’s body span: ' + '; '.join(
                 f'{BNAME[n]} {w} px, {picks[n][0]} of {picks[n][2]["cols"]} columns, {span_w(picks[n][2], picks[n][0]):.0f} px, '
                 f'{picks[n][1]["mean"]:.0f} characters a line' for n, w in BPS) + '.', readable=True,
             notes='A readable table (D2-255). Each span picked as the one whose measured mean sits nearest 68 within 60 to '
                   '75; phones take all four columns. Measured with 7,000 characters of chapter 02’s prose.')
    full = ctx.R.get('cpl span wide 12') or {'mean': 0, 'min': 0, 'max': 0}
    svgf, _ = grid_svg(ctx, 'wide', text_band=12)
    cssf = f'.cp{{margin:8px 0 0;{ctx.ty("caption")};color:{sec}}}.nm{{margin:8px 0 0;{ctx.ty("ui")}}}'
    ctx.spec('s-07-3-failure', f'<style>{cssf}</style>{svgf}<p class="nm">Wide, 1440 px, at one quarter size</p>'
                               f'<p class="cp">The paragraph spans all 12 columns, {full["mean"]:.0f} characters a line.</p>',
             '07', '07.3',
             f'The 1440 px grid at one quarter size with a paragraph drawn across all 12 columns, measured at '
             f'{full["mean"]:.0f} characters a line.', width=360, scale=0.25,
             notes='A diagram at one quarter size, measured with chapter 02’s prose at 17 px across 1,312 px.')
    return picks, full


def s_07_4(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    for sid, above, below in (('s-07-4-correct', 'var(--oa-space-600)', 'var(--oa-space-200)'),
                              ('s-07-4-failure', 'var(--oa-space-300)', 'var(--oa-space-300)')):
        a_px = {'var(--oa-space-600)': 48, 'var(--oa-space-300)': 24}[above]
        b_px = {'var(--oa-space-200)': 16, 'var(--oa-space-300)': 24}[below]
        css = (f'.sl{{max-width:34rem}}'
               f'.bt{{margin:0;{ctx.ty("body")}}}.hd{{margin:0;{ctx.ty("h4")};text-wrap:balance}}'
               f'.gp{{display:flex;align-items:center;justify-content:flex-end;padding-right:6px;background:{v("oa.color.tint.verdigrisN82")};'
               f'color:{v("oa.color.text.primary.onNewsprint")};{ctx.ty("dataLabel")};line-height:1}}')
        html = (f'<style>{css}.il{{margin:0 0 16px}}</style><div class="sl"><p class="il">{B.ILLUS}</p>'
                f'<p class="bt">The council takes public comment before each budget vote, and anyone who signs up can speak '
                f'for three minutes.</p>'
                f'<div class="gp" style="height:{above}">{a_px} px</div>'
                f'<p class="hd">How to sign up</p>'
                f'<div class="gp" style="height:{below}">{b_px} px</div>'
                f'<p class="bt">Add your name on the clerk’s page by noon on the day of the meeting.</p>'
                f'<div class="gp" style="height:var(--oa-space-200)">16 px</div>'
                f'<p class="bt">The clerk calls speakers in the order they signed up.</p></div>')
        ctx.spec(sid, html, '07', '07.4',
                 f'A short Illustrative section with the heading How to sign up, its gaps drawn as bands: {a_px} px above '
                 f'the heading, {b_px} px below it and 16 px between paragraphs.', illustrative=True,
                 notes='Gap bands are part of the specimen.')


def layout_for(width, text_pct):
    root = 16 * text_pct / 100
    if width >= 90 * root:
        return 'wide'
    if width >= 64 * root:
        return 'desktop'
    if width >= 48 * root:
        return 'tablet'
    return 'phone'


def s_07_5(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    widths = [1440, 1024, 768]
    pcts = [100, 150, 200]
    trs = []
    for w in widths:
        cells = []
        for p in pcts:
            lay = layout_for(w, p)
            g = grid(ctx, lay if lay != 'phone' else 'phone')
            cells.append(f'<td data-k="{p} percent text">{BNAME[lay]}, {g["cols"]} columns</td>')
            ctx.fig(f'layout at {w} px and {p} percent text', lay, 'em media queries: 90em, 64em, 48em at 16 px × text percent')
        trs.append(f'<tr><th scope="row">{w} px window</th>{"".join(cells)}</tr>')
    css = (f'table{{width:100%;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
           f'th,td{{text-align:left;padding:10px 12px 10px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{ctx.ty("label")};border-bottom-color:{v("oa.color.border.strong.onNewsprint")}}}tbody th{{font-weight:600}}'
           f'@container (max-width:30rem){{thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}'
           f'table,tbody,tr,th,td{{display:block}}tr{{padding:8px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'th,td{{border:0;padding:0}}td::before{{content:attr(data-k) ": ";color:{sec}}}}}.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr"><table role="table"><thead><tr><th scope="col">Window</th>'
            + ''.join(f'<th scope="col">Text at {p} percent</th>' for p in pcts) +
            f'</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    ctx.spec('s-07-5-correct', html, '07', '07.5',
             'A table of the layout a reader gets by window width and text size: ' + '; '.join(
                 f'{w} px at ' + ', '.join(f'{p} percent {BNAME[layout_for(w, p)].lower()}' for p in pcts) for w in widths) + '.',
             readable=True, notes='A readable table (D2-255). Worked out from the em breakpoints; text percent is the '
                                  'browser’s text size setting.')
    r = ctx.R.get('cpl 200 percent in five columns') or {'mean': 0, 'min': 0, 'max': 0}
    rs = ctx.R.get('cpl 200 percent sample') or {'mean': 0, 'min': 0, 'max': 0}
    g = grid(ctx, 'wide')
    css2 = (f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
            f'.b{{margin:0;width:{span_w(g, 5):.2f}px;font-family:var(--oa-font-family-reading);font-size:2.125rem;line-height:1.6}}')
    ctx.spec('s-07-5-failure', f'<style>{css2}</style><p class="k">Five of 12 columns at 1440 px, text at 200 percent</p>'
                               f'<p class="b">{SAMPLE}</p>', '07', '07.5',
             f'The opening paragraph of chapter 02 at 34 px squeezed into five columns, {span_w(g, 5):.0f} px wide, as a '
             f'page with breakpoints in px would set it for a reader at 200 percent text: about {rs["mean"]:.0f} characters '
             f'a line.', width=round(span_w(g, 5)), exempt=['scale'],
             notes='The span a wide layout gives body text, at doubled size. Exempt from the scale check: 34 px is the body '
                   'size doubled, off the scale on purpose in a labeled failure.')
    return r, rs


def stack_table(ctx, cut=False):
    v = ctx.v
    pairs = [('charcoal', 'newsprint', 'Default body text'), ('stone', 'newsprint', 'Marks and large text only'),
             ('newsprint', 'charcoal', 'Reversed body text'), ('white', 'prussian', 'Body text in Prussian panels'),
             ('pillarRed', 'newsprint', 'Signature marks; a working mark takes a keyline')]
    name = sys.modules['stage_a_systems_ch05'].PNAME
    rows = []
    for fg, bg, use in pairs:
        r = ctx.ratio(f'oa.color.palette.{fg}', f'oa.color.palette.{bg}')
        rows.append((f'{name[fg]} on {name[bg]}', f'{r} to 1', use))
    sec = v('oa.color.text.secondary.onNewsprint')
    if not cut:
        lis = ''.join(f'<li><p class="pr">{a}</p><p class="rt">{b}</p><p class="us">{c}</p></li>' for a, b, c in rows)
        css = (f'.fr{{width:100%;padding:16px;box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}}}'
               f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
               f'ul{{list-style:none;margin:0;padding:0}}li{{padding:10px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
               f'.pr{{margin:0;{ctx.ty("ui")}}}.rt{{margin:2px 0 0;{ctx.ty("dataLabel")}}}.us{{margin:2px 0 0;{ctx.ty("bodySmall")}}}')
        return f'<style>{css}</style><div class="fr"><p class="k">Contrast, measured</p><ul>{lis}</ul></div>', rows
    trs = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    css = (f'.fr{{width:100%;padding:16px;overflow:hidden;box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}}}'
           f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
           f'table{{width:30rem;border-collapse:collapse;{ctx.ty("bodySmall")}}}td{{padding:8px 12px 8px 0;white-space:nowrap;'
           f'border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}')
    return (f'<style>{css}</style><div class="fr"><p class="k">Contrast, measured</p><table><tbody>{trs}</tbody></table></div>'), rows


def s_07_6(ctx):
    html, rows = stack_table(ctx)
    ctx.spec('s-07-6-correct', html, '07', '07.6',
             'A frame 320 px wide holding five contrast pairs as stacked cards: ' + '; '.join(f'{a}, {b}, {c}' for a, b, c in rows) + '.',
             width=320, notes='True size at the reflow width.')
    htmlf, _ = stack_table(ctx, cut=True)
    ctx.spec('s-07-6-failure', htmlf, '07', '07.6',
             'The same five pairs kept as a three-column table inside a 320 px frame, so the right part of the table, with '
             'each pair’s use, is cut off at the frame’s edge.', width=320,
             notes='The table is 30 rem wide inside a 320 px frame that hides its overflow, as V5’s contrast table was cut.')


# ------------------------------------------------------------------------------------------------ chapter
def build(ctx):
    probes(ctx)
    s_07_opener(ctx)
    s_07_1(ctx)
    s_07_2(ctx)
    picks, full = s_07_3(ctx)
    s_07_4(ctx)
    r200, r200s = s_07_5(ctx)
    s_07_6(ctx)
    gw, gd, gt, gp, gs = (grid(ctx, n) for n, _ in BPS)
    sp = {n: picks[n][0] for n, _ in BPS}
    lay150 = layout_for(1440, 150)
    lay200 = layout_for(1440, 200)
    ch = {
        'number': '07', 'anchor': 'layout', 'title': 'Layout and spacing', 'part': 'Foundations',
        'instruction': 'Build each page on the column grid and spacing scale, readable at every width.',
        'opener': 's-07-opener',
        'intro': [
            'Every page sits on a column grid and spaces its parts in steps of 8 px. The grid changes at set window widths, '
            'called breakpoints, from 12 columns on a desktop to four on a phone, and each paragraph spans the columns '
            'that keep its lines at the measure chapter 06 sets.',
            'A page also has to read at 320 px wide, and with its text at twice the size, with nothing cut off and no '
            'scrolling sideways.'],
        'rules': [
            {
                'id': '07.1', 'title': 'Space everything in steps of the 8 px scale.',
                'rule': ['Use the eleven steps of the spacing scale, from 4 px to 104 px, for every gap, padding and margin. '
                         'Spaces around text are set in rem, so they grow with the reader’s text. The grid’s gutters and '
                         'page margins stay in px.'],
                'tokens': [f'oa.space.{k}' for k in SPACE],
                'why': {'text': ['One rhythm lets the parts of different pages line up, and a reader senses the order before '
                                 'reading it. Every step is a multiple of 4 px, so its edges land on whole device pixels at '
                                 '1x, 1.5x, 2x and 3x screen density. Our fifth edition kept the same 8 px rhythm; Edition '
                                 '06 gives each step a token.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-07-1-correct',
                            'caption': 'The scale at true size, and a card spaced on it: 24 px of padding, 8 px from kicker '
                                       'to heading and 16 px from heading to text.'},
                'failure': {'specimen': 's-07-1-failure',
                            'caption': '<strong>Fails Rule 07.1.</strong> The same card with gaps of 22, 13 and 37 px. Each is '
                                       'near a step and none is one, so the card sits out of line with the page around it.'},
                'specs': [{'label': f'{C.css_name("oa.space." + k)}', 'value': f'{ctx.T.px("oa.space." + k):g} px, {ctx.T.dim("oa.space." + k)[0]:g} rem', 'token': f'oa.space.{k}'} for k in SPACE],
                'related': ['06', '12', '18'],
                'builders': ['Name a step by its multiple of 8 times 100: <code>--oa-space-300</code> is 24 px and '
                             '<code>--oa-space-050</code> is 4 px. A value between steps means the layout is off, so move to '
                             'the nearest step.'],
            },
            {
                'id': '07.2', 'title': 'Set each page on the column grid for its width.',
                'rule': [f'Lay each page on the grid for its width: 12 columns at 1440 and 1024 px, eight at 768 px and four '
                         f'on phones, with the gutters and margins in the specifications. Every section of a page shares the '
                         f'same column lines.'],
                'tokens': [f'oa.layout.grid.{n}.{p}' for n, _ in BPS for p in ('columns', 'gutter', 'margin')][:9] +
                          ['oa.layout.breakpoint.wide', 'oa.layout.breakpoint.phone'],
                'why': {'text': ['When every section uses the same column lines, the eye finds the edge of each block in the '
                                 'same place, page after page. Our fifth edition switched among two- to six-column grids from '
                                 'section to section, so no column line ran the length of a chapter.'],
                        'basis': 'Design judgment; our audit of the fifth edition, October 2026'},
                'correct': {'specimen': 's-07-2-correct',
                            'caption': 'The five grids drawn at one quarter of true size, each column’s width worked out from '
                                       'the tokens. The labels under each grid are at true size.'},
                'failure': {'specimen': 's-07-2-failure',
                            'caption': '<strong>Fails Rule 07.2.</strong> A page at 1440 px, drawn at one quarter size, whose '
                                       'three sections sit on three, five and two columns. Their edges never line up, so each '
                                       'section reads as a separate page.'},
                'specs': [{'label': f'{BNAME[n]}, {w} px', 'value': f'{grid(ctx, n)["cols"]} columns of {grid(ctx, n)["col"]:.1f} px, '
                           f'{grid(ctx, n)["gutter"]:g} px gutters, {grid(ctx, n)["margin"]:g} px margins',
                           'token': f'oa.layout.grid.{n}.columns'} for n, w in BPS],
                'related': ['03', '08', '20', '25'],
                'builders': ['Build the grid with CSS grid: <code>grid-template-columns: repeat(12, minmax(0, 1fr))</code> '
                             'with <code>column-gap: var(--oa-layout-grid-wide-gutter)</code>, and the page margin as '
                             'padding. Keep 360 px on the 4-column grid with 16 px margins; it also holds the 320 px reflow '
                             'test.'],
            },
            {
                'id': '07.3', 'title': 'Span body text across the columns that hold its measure.',
                'rule': [f'Body text spans {C.num(sp["wide"])} of 12 columns at 1440 px, {C.num(sp["desktop"])} of 12 at '
                         f'1024 px, {C.num(sp["tablet"])} of eight at 768 px and all four on phones. Those spans hold the 60 to '
                         f'75 characters a line that chapter 06 sets, and a block that spans more columns caps its text at '
                         f'the body measure.'],
                'tokens': ['oa.layout.measure.bodyIdeal', 'oa.layout.grid.wide.columns', 'oa.layout.grid.desktop.columns',
                           'oa.layout.grid.tablet.columns', 'oa.layout.grid.phone.columns'],
                'why': {'text': [f'The grid places a block, and its span keeps the lines readable. Prose run across all '
                                 f'12 columns at 1440 px measured {full["mean"]:.0f} characters a line, more than twice the '
                                 f'measure. Across the {C.num(sp["wide"])}-column span, the same prose measured '
                                 f'{picks["wide"][1]["mean"]:.0f}.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-07-3-correct',
                            'caption': f'The 1440 px grid at one quarter size. Body text takes the first '
                                       f'{C.num(sp["wide"])} of 12 columns, and the table below gives the span at every width.'},
                'failure': {'specimen': 's-07-3-failure',
                            'caption': f'<strong>Fails Rule 07.3.</strong> Drawn at one quarter size, a paragraph spanning all '
                                       f'12 columns at 1440 px. It measured {full["mean"]:.0f} characters a line.'},
                'specs': [{'label': f'{BNAME[n]}, {w} px', 'value': f'{picks[n][0]} of {picks[n][2]["cols"]} columns, '
                           f'{span_w(picks[n][2], picks[n][0]):.0f} px, {picks[n][1]["mean"]:.0f} characters a line',
                           'token': f'oa.layout.grid.{n}.columns'} for n, w in BPS] +
                         [{'label': 'Measure cap', 'value': '33.88 rem', 'token': 'oa.layout.measure.bodyIdeal'}],
                'related': ['06', '20', '24'],
                'builders': ['Give body text both a span and a cap: <code>grid-column: span 5</code> at the wide width and '
                             '<code>max-width: var(--oa-layout-measure-body-ideal)</code>. The cap is in rem, so it holds '
                             'the measure when text grows.'],
            },
            {
                'id': '07.4', 'title': 'Set a heading closer to the text it introduces than to the block above.',
                'rule': ['Leave at least twice as much space above a heading as below it. Sections part by 80 px, a label '
                         'sits 32 px below the block above it and 8 px above what it names, and paragraphs part by 16 px.'],
                'tokens': ['oa.space.1000', 'oa.space.600', 'oa.space.400', 'oa.space.200', 'oa.space.100'],
                'why': {'text': ['Readers group what sits close together, a pattern designers call proximity. A heading with '
                                 'equal space above and below seems to belong to neither block, and the reader pauses to work '
                                 'out which one it names.'],
                        'basis': 'Design judgment, from the Gestalt principle of proximity'},
                'correct': {'specimen': 's-07-4-correct',
                            'caption': 'A section at true size, its gaps drawn as bands: 48 px above the heading, 16 px below '
                                       'it and 16 px between paragraphs.'},
                'failure': {'specimen': 's-07-4-failure',
                            'caption': '<strong>Fails Rule 07.4.</strong> The same section with 24 px above and below the '
                                       'heading, so it floats between the two blocks.'},
                'specs': [
                    {'label': 'Between sections or rules', 'value': '80 px', 'token': 'oa.space.1000'},
                    {'label': 'Above a heading inside a section', 'value': '48 px', 'token': 'oa.space.600'},
                    {'label': 'Above a label', 'value': '32 px', 'token': 'oa.space.400'},
                    {'label': 'Below a heading; between paragraphs', 'value': '16 px', 'token': 'oa.space.200'},
                    {'label': 'Below a label', 'value': '8 px', 'token': 'oa.space.100'},
                ],
                'related': ['06', '12'],
                'builders': ['Put the space on the heading’s own top margin, so the gap moves with the heading wherever it '
                             'lands.'],
            },
            {
                'id': '07.5', 'title': 'Set breakpoints in em, so larger text gets fewer columns.',
                'rule': [f'A breakpoint is the window width where the layout changes, and an em is the reader’s text size, '
                         f'16 px unless they change it. Write each breakpoint in em: 90em for the wide layout, 64em for '
                         f'desktop and 48em for tablet, with the phone layout as the base. On a 1440 px screen, a reader at '
                         f'150 percent text gets the {BNAME[lay150].lower()} layout and a reader at 200 percent the '
                         f'{BNAME[lay200].lower()} layout, with fewer, wider columns for the larger words.'],
                'tokens': ['oa.layout.breakpoint.wide', 'oa.layout.breakpoint.desktop', 'oa.layout.breakpoint.tablet'],
                'why': {'text': [f'WCAG 2.2 success criterion 1.4.4 Resize Text asks that text reach 200 percent with nothing '
                                 f'lost. A breakpoint in px ignores the reader’s text size, so doubled text crowds a layout '
                                 f'drawn for smaller words: five columns at 1440 px hold about {r200["mean"]:.0f} characters '
                                 f'of 34 px text a line. In em, the layout steps down as the text grows, and the measure cap '
                                 f'in rem keeps the line length.'],
                        'basis': 'WCAG 2.2 SC 1.4.4'},
                'correct': {'specimen': 's-07-5-correct',
                            'caption': 'The layout a reader gets by window width and text size, worked out from the em '
                                       'breakpoints.'},
                'failure': {'specimen': 's-07-5-failure',
                            'caption': f'<strong>Fails Rule 07.5.</strong> With breakpoints in px, a reader at 200 '
                                       f'percent text keeps the wide layout, and body text at 34 px in a five-column span runs '
                                       f'about {r200s["mean"]:.0f} characters a line.'},
                'specs': [
                    {'label': 'Wide', 'value': '(min-width: 90em), 1440 px at 16 px text', 'token': 'oa.layout.breakpoint.wide'},
                    {'label': 'Desktop', 'value': '(min-width: 64em), 1024 px', 'token': 'oa.layout.breakpoint.desktop'},
                    {'label': 'Tablet', 'value': '(min-width: 48em), 768 px', 'token': 'oa.layout.breakpoint.tablet'},
                    {'label': 'Phone', 'value': 'The base layout, no query', 'token': 'oa.layout.breakpoint.phone'},
                ],
                'related': ['06', '19'],
                'builders': ['Media queries cannot read custom properties, so write the em value itself: '
                             '<code>@media (min-width: 64em)</code>. The token’s <code>mediaQuery</code> field in '
                             '<code>tokens.json</code> holds each one.'],
            },
            {
                'id': '07.6', 'title': 'Make every page read at 320 px wide, with nothing lost.',
                'rule': ['At 320 CSS px, the width of a small phone or a desktop window zoomed to 400 percent, a page shows '
                         'all its content without scrolling sideways. Tables stack into one card per row. Only content that '
                         'needs two dimensions, such as a wide data table or a specimen at true size, scrolls sideways inside '
                         'its own frame. That frame is a group named for what it holds, and it takes keyboard focus only '
                         'while its content overflows.'],
                'tokens': ['oa.layout.breakpoint.phoneSmall', 'oa.layout.grid.phoneSmall.margin', 'oa.layout.grid.phoneSmall.columns'],
                'why': {'text': ['WCAG 2.2 success criterion 1.4.10 Reflow asks for content at 320 CSS px with no loss of '
                                 'information and no scrolling in two directions. When we tested our fifth edition at 320 px, '
                                 'the page ran 524 px wide and its contrast table lost its last column.'],
                        'basis': 'WCAG 2.2 SC 1.4.10'},
                'correct': {'specimen': 's-07-6-correct',
                            'caption': 'A 320 px frame at true size holding contrast pairs as stacked cards. Every pair, ratio '
                                       'and use stays in view. A table that must keep its columns scrolls inside a named frame '
                                       'instead, as the wide plates in this guide do on a phone.'},
                'failure': {'specimen': 's-07-6-failure',
                            'caption': '<strong>Fails Rule 07.6.</strong> The same pairs kept as a table in a 320 px frame. The '
                                       'last column falls past the edge, and a reader on a small phone never sees what each '
                                       'pair may carry.'},
                'specs': [
                    {'label': 'Reflow width', 'value': '320 CSS px, on the small phone grid', 'token': 'oa.layout.breakpoint.phoneSmall'},
                    {'label': 'Small phone margin', 'value': '16 px', 'token': 'oa.layout.grid.phoneSmall.margin'},
                    {'label': 'Text at 200 percent', 'value': 'No clipped boxes and no sideways scroll at 1440 px', 'token': None},
                    {'label': 'A frame that scrolls', 'value': 'A group named for what it holds, such as the table’s title', 'token': None},
                    {'label': 'Keyboard focus', 'value': 'Only while its content overflows the frame, checked on load and on resize', 'token': None},
                    {'label': 'Scroll cue', 'value': 'A line above the frame saying it scrolls sideways', 'token': None},
                ],
                'related': ['18', '19', '28'],
                'builders': ['Check every page at 320, 360 and 390 px with the shared rendered check. A frame that must '
                             'scroll is a group with its own name, such as the table’s title, and takes '
                             '<code>tabindex="0"</code> only while it overflows, so a keyboard user can scroll it. '
                             'Landmarks are the regions a screen reader can jump to, such as the navigation, and a group '
                             'stays out of that list, so a page with many frames keeps it short. Write '
                             '<code>role="group"</code> and <code>aria-label="Contrast pairs, scroll sideways"</code> while '
                             '<code>scrollWidth > clientWidth</code>, and neither once the content fits.'],
            },
        ],
        'related_chapters': [
            {'chapter': '06', 'reason': 'The type scale the grid carries.'},
            {'chapter': '08', 'reason': 'The lockmark’s four fixed places on the page.'},
            {'chapter': '20', 'reason': 'Web pages on the grid.'},
            {'chapter': '25', 'reason': 'Print and slides on the grid.'},
        ],
        'extras': [
            {'after_rule': '07.3', 'specimen': 's-07-spans', 'label': 'Body span at each width',
             'caption': 'The body span at each width, measured with 7,000 characters of chapter 02’s prose in Inter at 17 px. '
                        'Phones fall under 60 characters, which suits a small screen.'},
        ],
        'sources': ['W3C, Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, success criteria 1.4.4 and '
                    '1.4.10, https://www.w3.org/TR/WCAG22/.'],
    }
    for r in ch['rules']:
        r['specs'] = [{k: x for k, x in s.items() if x is not None} for s in r['specs']]
    return ch
