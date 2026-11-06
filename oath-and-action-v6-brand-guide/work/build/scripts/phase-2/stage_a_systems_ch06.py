"""Chapter 06 Type: copy, rules and specimens (stage board A, systems designer, November 6, 2026).

Characters per line, word-space widths, the width of a heading in its fallback face and the hang of an opening
quotation mark are measured in Chromium with the Google Fonts files the guide page loads (stage_a_systems_capture.js).
"""
import json
import re
import sys

C = sys.modules['stage_a_systems_core']

# Real Oath & Action copy. W07's rewrite in chapter 02 (an interactive version of our systems atlas, rewritten):
W07 = ('The pressure on officials to serve the whole electorate depends on a real chance of losing. In most districts the '
       'general election is easy to predict, so the contest that decides the seat is a low-turnout primary. Incumbents '
       'also help write the rules for their own races, from district maps to voting procedures.')
HEAD = 'Who decides what happens next?'            # our fifth edition's type chapter, its H2 sample line
BAL = 'What a primary decides, and who may vote in it'   # our fifth edition's balanced-heading sample
COMMIT = 'Clarity is our duty. Action is our promise.'   # locked editorial commitment (Master Brief section 3)
W02 = 'A regulator or a board approves your rate.'       # chapter 02, W02's rewrite of an Atlas V7 everyday answer

STYLES = [
    ('title', 'Title', 'Edition 06'),
    ('section', 'Section', '05 Color'),
    ('h3', 'H3', 'Text sits only on color pairs that pass.'),
    ('h4', 'H4', HEAD),
    ('quote', 'Quote', f'“{COMMIT}”'),
    ('intro', 'Intro', 'Choose a surface first, then the text and graphic colors that pass on it.'),
    ('body', 'Body', W02 + ' The council sets the hours each spring, when it passes the budget.'),
    ('bodySmall', 'Small body', 'Charcoal on Newsprint measures 13.29 to 1.'),
    ('ui', 'Interface', 'Download the lockmark'),
    ('caption', 'Caption', 'Source: U.S. Bureau of Labor Statistics, Current Employment Statistics.'),
    ('label', 'Label', 'Foundations · Chapter 06 of 28'),
    ('dataLabel', 'Data label', '3,798 · 1,640 · −245'),
    ('figure', 'Figure', '13.29'),
    ('ask', 'Ask', 'Sign up to speak'),
]


def long_sample():
    """Chapter 02's prose: every plain paragraph of the approved writing section, marks stripped."""
    md = (C.ROOT / 'work/handoffs/phase-2/20261106_Voice-Writing-Rules.md').read_text()
    md = md.split('## Before you publish')[0]
    out = []
    for line in md.splitlines():
        s = line.strip()
        if not s or s[0] in '#>*|-<' or len(s) < 60 or re.match(r'\d+\.', s):
            continue
        s = re.sub(r'\*\*|~~|\*', '', s)
        out.append(s)
    return ' '.join(out)


def probes(ctx):
    body = 'font:var(--oa-type-body)'
    ctx.probe('cpl body ideal', 'cpl', text=W07, css=f'{body};width:var(--oa-layout-measure-body-ideal)')
    ctx.probe('cpl body max', 'cpl', text=W07, css=f'{body};width:var(--oa-layout-measure-body-max)')
    ctx.probe('cpl long sample ideal', 'cpl', text=long_sample(), css=f'{body};width:var(--oa-layout-measure-body-ideal)')
    ctx.probe('cpl long sample max', 'cpl', text=long_sample(), css=f'{body};width:var(--oa-layout-measure-body-max)')
    ctx.probe('cpl intro max', 'cpl', text=W07, css='font:var(--oa-type-intro);font-size:1.375rem;width:var(--oa-layout-measure-intro-max)')
    ctx.probe('cpl v5 intro 65ch', 'cpl', text=W07, css='font:var(--oa-type-intro);font-size:1.375rem;width:65ch')
    ctx.probe('width v5 intro 65ch', 'width', text='0', css='font:var(--oa-type-intro);font-size:1.375rem;display:block;width:65ch')
    for name, tr in (('h4 0', '0em'), ('h4 -2', '-0.02em'), ('h4 -4.5', '-0.045em')):
        ctx.probe(f'space {name}', 'space', css=f'font:var(--oa-type-h4);font-size:1.5rem;letter-spacing:{tr}')
    ctx.probe('width head inter tight', 'width', text=HEAD, css='font:var(--oa-type-h3);font-size:2rem;letter-spacing:var(--oa-type-h3-letter-spacing)')
    ctx.probe('width head arial', 'width', text=HEAD, css='font:var(--oa-type-h3);font-size:2rem;font-family:Arial,sans-serif;letter-spacing:var(--oa-type-h3-letter-spacing)')
    ctx.probe('width open quote lora em', 'width', text='“', css='font:var(--oa-type-quote);font-size:100px;letter-spacing:0')
    ctx.probe('font check', 'fonts')


def ms(ctx, key):
    return ctx.m(key) or {}


# ------------------------------------------------------------------------------------------------ specimens
def hang(ctx):
    h = ctx.m('width open quote lora em')
    return (h['width'] / 100) if h else 0.42


def s_06_1(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    css = (f'.fc{{display:grid;gap:32px}}.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
           f'.d{{margin:0;{ctx.ty("h3")};text-wrap:balance}}.b{{margin:0;{ctx.ty("body")}}}'
           f'.u{{display:inline-flex;margin-top:12px;align-items:center;min-height:44px;padding:0 16px;'
           f'background:{v("oa.component.button.primary.fill.onNewsprint")};color:{v("oa.component.button.primary.label.onNewsprint")};{ctx.ty("ui")}}}'
           f'.l{{display:block;margin-top:12px;{ctx.ty("label")}}}'
           f'.q{{margin:0;{ctx.ty("quote")};text-indent:-{hang(ctx):.3f}em}}'
           f'.t{{margin:8px 0 0;{ctx.ty("caption")};color:{sec}}}')
    html = (f'<style>{css}</style><div class="fc">'
            f'<div><p class="k">Inter Tight 800 · display</p><p class="d">{HEAD}</p>'
            f'<p class="t">Titles, headings and big figures</p></div>'
            f'<div><p class="k">Inter 400, 600 and 700 · reading and interface</p><p class="b">{W02}</p>'
            f'<span class="u">Download the lockmark</span><span class="l">Explain · Local utilities</span>'
            f'<p class="t">Body text, buttons, labels, captions, tables and chart text</p></div>'
            f'<div><p class="k">Lora Italic 400 · quotation</p><p class="q">“{COMMIT}”</p>'
            f'<p class="t">Only words we quote: pull quotes and quote cards</p></div></div>')
    ctx.spec('s-06-1-correct', html, '06', '06.1',
             f'The three faces at true size. Inter Tight 800 sets the heading {HEAD} Inter sets the sentence {W02}, a button '
             f'labeled Download the lockmark and a label in capitals. Lora Italic sets our editorial commitment, “{COMMIT}”',
             notes='The heading line is our fifth edition’s type sample; the body line is chapter 02’s W02 rewrite.')
    cssf = (f'.d{{margin:0;{ctx.ty("h3")};font-family:var(--oa-font-family-quote);font-style:italic;font-weight:var(--oa-font-weight-regular);text-wrap:balance}}'
            f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}.b{{margin:12px 0 0;{ctx.ty("body")}}}')
    htmlf = (f'<style>{cssf}</style><p class="k">Explain · Local utilities</p><p class="d">{HEAD}</p>'
             f'<p class="b">{W02}</p>')
    ctx.spec('s-06-1-failure', htmlf, '06', '06.1',
             f'The heading {HEAD} set in Lora Italic above the sentence {W02}, so the heading looks like a quotation.',
             notes='A labeled failure: the face does a job that is not its own.')


def s_06_2(ctx):
    v = ctx.v
    T = ctx.T
    sec = v('oa.color.text.secondary.onNewsprint')
    rows = []
    for key, name, sample in STYLES:
        node = T.node(f'oa.type.{key}')
        ext = T.ext(f'oa.type.{key}')
        val = node['$value']
        fam = T.value(val['fontFamily'][1:-1])[0] if isinstance(val['fontFamily'], str) else val['fontFamily'][0]
        wt = T.value(val['fontWeight'][1:-1]) if isinstance(val['fontWeight'], str) else val['fontWeight']
        lh = val['lineHeight']
        tr = ext.get('trackingEm', 0)
        fs = val['fontSize']
        mx = fs['value'] if fs['unit'] == 'rem' else fs['value'] / 16
        mn = ext.get('minFontSize', {}).get('value', mx)
        size = (f'{mn * 16:g} to {mx * 16:g} px ({mn:g} to {mx:g} rem)' if mx and mx != mn else f'{mn * 16:g} px ({mn:g} rem)')
        face = fam + (' Italic' if key == 'quote' else '')
        trk = 'tracking 0' if not tr else f'tracking {C.MINUS if tr < 0 else "+"}{abs(tr) * 100:g}%'
        extra = []
        if ext.get('numeric'):
            extra.append('tabular figures')
        if ext.get('textTransform') == 'uppercase':
            extra.append('capitals')
        spec = f'{face} {wt} · {size} · line height {lh:g} · {trk}' + (' · ' + ', '.join(extra) if extra else '')
        ctx.fig(f'type scale {key}', spec, 'tokens.json oa.type')
        cls = 'smp'
        rows.append(f'<li><p class="nm">{name}<code>{C.css_name("oa.type." + key)}</code></p><p class="sp">{spec}</p>'
                    f'<p class="{cls}" style="{ctx.ty(key)}">{sample}</p></li>')
    css = (f'ul{{list-style:none;margin:0;padding:0}}'
           f'li{{display:grid;grid-template-columns:minmax(0,13rem) minmax(0,1fr);gap:4px 32px;align-items:baseline;padding:20px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'.nm{{margin:0;{ctx.ty("ui")}}}.nm code{{display:block;{ctx.ty("caption")};color:{sec}}}'
           f'.sp{{margin:0;grid-column:1;{ctx.ty("caption")};color:{sec}}}'
           f'.smp{{margin:0;grid-column:2;grid-row:1 / span 2;text-wrap:balance;overflow-wrap:break-word;min-width:0}}'
           f'@container (max-width:40rem){{li{{grid-template-columns:1fr}}.smp{{grid-column:1;grid-row:auto;margin-top:8px}}}}'
           f'.wr{{container-type:inline-size}}')
    html = f'<style>{css}</style><div class="wr"><ul>{"".join(rows)}</ul></div>'
    ctx.spec('s-06-2-correct', html, '06', '06.2',
             'The type scale, fourteen styles from Title to Ask, each with its token name, face, size in px and rem, line '
             'height and tracking, and a sample line drawn live in the style.', interactive=True,
             notes='Every spec line is read from tokens.json; every sample uses the token’s CSS custom properties.')
    # failure: what 200 percent text does to px and rem
    cssf = (f'.pr{{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr))}}'
            f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
            f'.r{{margin:0;font-family:var(--oa-font-family-reading);font-size:2.125rem;line-height:1.6}}'
            f'.p{{margin:0;font-family:var(--oa-font-family-reading);font-size:1.0625rem;line-height:1.6}}')
    htmlf = (f'<style>{cssf}</style><div class="pr"><div><p class="k">Set in rem, at 34 px</p><p class="r">{W02}</p></div>'
             f'<div><p class="k">Set in px, still 17 px</p><p class="p">{W02}</p></div></div>')
    ctx.spec('s-06-2-failure', htmlf, '06', '06.2',
             f'Two columns showing the sentence {W02} as a reader sees it with text set to 200 percent: on the left, set in '
             f'rem, it has grown to 34 px; on the right, set in px, it is still 17 px.',
             notes='A depiction: both columns are drawn at the sizes a 200 percent text setting produces, since the guide '
                   'page itself runs at the reader’s own setting.')


def s_06_3(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    edge = v('oa.color.border.strong.onNewsprint')
    css = (f'ul{{list-style:none;margin:0;padding:0;display:grid;gap:20px}}'
           f'li{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:4px 24px;align-items:baseline;padding-bottom:16px;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'.lb{{{ctx.ty("label")}}}.dl{{{ctx.ty("dataLabel")}}}'
           f'.tag{{justify-self:start;padding:0 6px;border:1px solid {edge};{ctx.ty("label")};line-height:1.6}}'
           f'.n{{{ctx.ty("caption")};color:{sec}}}'
           f'@container (max-width:30rem){{li{{grid-template-columns:1fr}}}}.wr{{container-type:inline-size}}')
    items = [('<span class="lb">Foundations · Chapter 06 of 28</span>', 'Location line: Inter 700, capitals, 13 px, 6% tracking'),
             ('<span class="lb">Ratio</span>', 'Column head: the same label style'),
             ('<span class="tag">Illustrative</span>', 'Tag: the label style inside a 1 px Charcoal edge'),
             (f'<span class="dl">13.29 · {C.MINUS}245 · 3,798</span>', 'Data label: Inter 600, 13 px, tabular figures')]
    html = (f'<style>{css}</style><div class="wr"><ul>' + ''.join(f'<li>{a}<span class="n">{b}</span></li>' for a, b in items)
            + '</ul></div>')
    ctx.spec('s-06-3-correct', html, '06', '06.3',
             'Four labels at true size, all 13 px: the location line Foundations, Chapter 06 of 28 in capitals, the column '
             'head Ratio, an Illustrative tag in a Charcoal edge and a data label reading 13.29, minus 245 and 3,798, each '
             'with a note on its style.', notes='Every label at the floor, 0.8125 rem.')
    cssf = (f'.v{{display:grid;gap:16px}}.e{{margin:0;font-family:var(--oa-font-family-reading);font-weight:700;font-size:.6875rem;'
            f'letter-spacing:.13em;text-transform:uppercase}}'
            f'.f{{margin:0;font-family:var(--oa-font-family-reading);font-weight:400;font-size:.625rem;letter-spacing:.1em}}'
            f'.n{{margin:4px 0 0;{ctx.ty("caption")};color:{sec}}}')
    htmlf = (f'<style>{cssf}</style><div class="v"><div><p class="e">06 / Type</p><p class="n">Eyebrow: 11 px, Inter 700, '
             f'13 percent tracking</p></div><div><p class="f">OATH &amp; ACTION · Type / 06</p><p class="n">Footer line: 10 px, '
             f'Inter 400</p></div></div>')
    ctx.spec('s-06-3-failure', htmlf, '06', '06.3',
             'A graphic at true size of two labels from our fifth edition: the eyebrow 06 / Type at 11 px in capitals with '
             'wide tracking, and the footer line Oath & Action, Type / 06 at 10 px.', exempt=['size'],
             notes='Sizes and tracking from the V5 text census (eyebrow 11 px, 700, 1.43 px tracking; footer 10 px).')


def s_06_4(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    for sid, tr, label in (('s-06-4-correct', 'var(--oa-type-h4-letter-spacing)', 'H4 at −2 percent tracking'),
                           ('s-06-4-failure', '-0.045em', 'H4 at −4.5 percent tracking')):
        css = (f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
               f'.h{{margin:0;{ctx.ty("h4")};font-size:1.5rem;letter-spacing:{tr};text-wrap:balance}}'
               f'.b{{margin:12px 0 0;{ctx.ty("body")}}}')
        html = f'<style>{css}</style><p class="k">{label}</p><p class="h">{HEAD}</p><p class="b">{W02}</p>'
        ctx.spec(sid, html, '06', '06.4',
                 f'The heading {HEAD} in Inter Tight 800 at 24 px with ' + ('minus 2 percent tracking, its word spaces open.'
                                                                          if sid.endswith('correct') else
                                                                          'minus 4.5 percent tracking, its word spaces closing up.'),
                 notes='Set at 24 px, the H4 size at 1440 px, so the measured word spaces apply.')


def jobs():
    d = json.loads((C.ROOT / 'work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json').read_text())
    ds = d['datasets']['payrolls-by-sector']
    pick = ['CES6562000001', 'USLAH', 'USGOVT', 'USCONS', 'MANEMP', 'USINFO']
    rows = {r['series_id']: r for r in ds['rows'] if r['date'] == '2026-09-01'}
    return [rows[s] for s in pick], ds['source_line']


def s_06_5(ctx):
    v = ctx.v
    rows, src = jobs()
    sec = v('oa.color.text.secondary.onNewsprint')

    def table(good):
        trs = []
        for r in rows:
            ch = r['change_since_2022_01_thousands']
            pc = r['pct_change_since_2022_01']
            if good:
                a, b = C.signed(ch, 0), C.signed(pc, 1)
            else:
                a = (f'{ch:,.0f}' if ch >= 0 else f'-{abs(ch):,.0f}')
                b = (f'{pc:g}' if pc >= 0 else f'-{abs(pc):g}')
            trs.append(f'<tr><th scope="row">{r["sector"]}</th><td>{a}</td><td>{b}</td></tr>')
        num = 'tabular-nums' if good else 'proportional-nums'
        align = 'right' if good else 'left'
        css = (f'.k{{margin:0;{ctx.ty("label")};color:{sec}}}.t{{margin:6px 0 12px;{ctx.ty("h4")};text-wrap:balance}}'
               f'table{{width:100%;max-width:40rem;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
               f'th,td{{padding:8px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")};vertical-align:baseline}}'
               f'thead th{{{ctx.ty("label")};border-bottom-color:{v("oa.color.border.strong.onNewsprint")}}}'
               f'tbody th{{font-weight:400;text-align:left;padding-right:16px}}'
               f'td,thead th.n{{text-align:{align};font-variant-numeric:{num};padding-left:16px;white-space:nowrap}}'
               f'thead th:first-child{{text-align:left}}'
               f'.so{{margin:12px 0 0;max-width:40rem;{ctx.ty("caption")};color:{sec}}}')
        return (f'<style>{css}</style><p class="k">Finding</p><p class="t">Change in payroll jobs by sector, January 2022 to '
                f'September 2026</p><table><thead><tr><th scope="col">Sector</th><th scope="col" class="n">Thousands</th>'
                f'<th scope="col" class="n">Percent</th></tr></thead><tbody>{"".join(trs)}</tbody></table>'
                f'<p class="so">{src}</p>')
    vals = '; '.join(f'{r["sector"]} {C.signed(r["change_since_2022_01_thousands"], 0)} thousand, {C.signed(r["pct_change_since_2022_01"], 1)} percent' for r in rows)
    ctx.spec('s-06-5-correct', table(True), '06', '06.5',
             f'A table titled Change in payroll jobs by sector, January 2022 to September 2026, with tabular figures aligned '
             f'right and the true minus sign. {vals}. Source line below.', interactive=True,
             notes='Data: payrolls-by-sector in the shared chart data, September 2026 row.')
    ctx.spec('s-06-5-failure', table(False), '06', '06.5',
             'The same table with proportional figures aligned left and a hyphen for each minus sign, so the columns no '
             'longer line up.', notes='A labeled failure: hyphen-minus on purpose.')
    return src


def s_06_6(ctx):
    sec = ctx.v('oa.color.text.secondary.onNewsprint')
    for sid, good in (('s-06-6-correct', True), ('s-06-6-failure', False)):
        text = BAL if good else BAL.rsplit(' ', 1)[0] + '<br>' + BAL.rsplit(' ', 1)[1]
        css = (f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
               f'.h{{margin:0;max-width:22rem;{ctx.ty("h3")};text-wrap:{"balance" if good else "wrap"}}}')
        html = f'<style>{css}</style><p class="k">Explain · Primaries</p><p class="h">{text}</p>'
        ctx.spec(sid, html, '06', '06.6',
                 f'The heading {BAL} in Inter Tight 800, ' + ('broken into lines of near equal length.' if good else
                                                             'with the single word it alone on its last line.'),
                 notes='The heading is our fifth edition’s balanced-heading sample.' + ('' if good else
                       ' The widow is set with a line break so it shows at every window width; ordinary wrapping produces '
                       'the same break at some widths.'))


def s_06_7(ctx):
    v = ctx.v
    hang_em = hang(ctx)
    ctx.fig('hang of the opening mark, em', f'{hang_em:.3f}', 'width of “ in Lora Italic 400, rendered at 100 px')
    for sid, good in (('s-06-7-correct', True), ('s-06-7-failure', False)):
        css = (f'.wr{{position:relative;padding-left:24px;max-width:30rem}}'
               f'.q{{position:relative;margin:0;{ctx.ty("quote")};text-wrap:balance;{"text-indent:-" + format(hang_em, ".3f") + "em" if good else ""}}}'
               f'.q::before{{content:"";position:absolute;left:0;top:-8px;bottom:-8px;border-left:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
               f'.k{{margin:20px 0 0;{ctx.ty("caption")};color:{v("oa.color.text.secondary.onNewsprint")}}}')
        html = (f'<style>{css}</style><div class="wr"><p class="q">“{COMMIT}”</p>'
                f'<p class="k">Our editorial commitment</p></div>')
        ctx.spec(sid, html, '06', '06.7',
                 f'Our editorial commitment, “{COMMIT}”, set as a pull quote in Lora Italic beside a hairline that marks the '
                 f'text edge, ' + ('with the opening mark hanging outside the line.' if good else
                                   'with the opening mark inside the edge, so the first line starts to the right of the second.'),
                 notes='The hang is the measured width of the opening mark in Lora Italic.')
    return hang_em


def s_06_8(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    css = (f'.k{{margin:0 0 12px;{ctx.ty("label")};color:{sec}}}'
           f'.b{{margin:0;{ctx.ty("body")};max-width:var(--oa-layout-measure-body-ideal)}}')
    ctx.spec('s-06-8-correct', f'<style>{css}</style><p class="k">Body, 17 px, at the body measure</p><p class="b">{W07}</p>',
             '06', '06.8', f'A paragraph in Inter at 17 px set to the body measure of 33.88 rem: {W07}',
             notes='The paragraph is W07’s rewrite in chapter 02.')
    w = ctx.m('width v5 intro 65ch')
    wpx = round(w['width']) if w else 880
    cssf = (f'.k{{margin:0 0 12px;{ctx.ty("label")};color:{sec}}}'
            f'.b{{margin:0;font:var(--oa-type-intro);font-size:1.375rem;width:65ch;max-width:none}}')
    ctx.spec('s-06-8-failure', f'<style>{cssf}</style><p class="k">Intro, 22 px, at 65ch</p><p class="b">{W07}</p>',
             '06', '06.8', f'The same paragraph at 22 px in a column 65ch wide, as our fifth edition set its intros, so the lines run long.',
             width=wpx + 0, notes=f'Width 65ch at 22 px measured at {wpx} px; shown at true size, so it scrolls inside its frame on narrow screens.')


def s_06_9(ctx):
    v = ctx.v
    W = 'oa.color.text.primary.onWhite'
    S = 'oa.color.text.secondary.onWhite'
    for sid, good in (('s-06-9-correct', True), ('s-06-9-failure', False)):
        hfam = 'var(--oa-font-family-email-sans)' if good else '"Inter Tight Unavailable", serif'
        css = (f'.em{{background:{v("oa.color.surface.white")};color:{v(W)};padding:32px 24px;max-width:600px}}'
               f'.mh{{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-bottom:16px;border-bottom:1px solid {v("oa.color.border.hairline.onWhite")}}}'
               f'.is{{font-family:var(--oa-font-family-email-sans);font-size:.875rem;color:{v(S)}}}'
               f'.h{{margin:24px 0 0;font-family:{hfam};font-weight:700;font-size:1.75rem;line-height:1.15}}'
               f'.b{{margin:16px 0 0;font-family:var(--oa-font-family-email-sans);font-size:1.0625rem;line-height:1.6}}'
               f'.q{{margin:24px 0 0;font-family:var(--oa-font-family-email-quote);font-style:italic;font-size:1.375rem;line-height:1.35}}')
        html = (f'<style>{css}</style><div class="em"><div class="mh">'
                f'<img data-inline src="work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg" width="152" height="16" alt="" data-red="signature">'
                f'<span class="is">Sample issue</span></div>'
                f'<p class="h">The school board votes on the new bell schedule April 14.</p>'
                f'<p class="b">Sign up with the board clerk by April 10 to speak before the vote.</p>'
                f'<p class="q">“{COMMIT}”</p></div>')
        ctx.spec(sid, html, '06', '06.9',
                 ('An email header at 600 px on White, set in the system stack: the wordmark, the label Sample issue, the '
                  'headline The school board votes on the new bell schedule April 14 in Helvetica or Arial bold, a sentence '
                  'of body text, and our editorial commitment in Georgia Italic.') if good else
                 ('The same email header with its headline set in Inter Tight and no web font loaded, so it shows in the '
                  'mail app’s default serif.'),
                 width=600, illustrative=True, surface='white',
                 notes='Headline and body from chapter 02, W08 (Illustrative).' + ('' if good else
                       ' The failure names a face no page loads, so every browser falls to its default serif, as a mail app does.'))


def w_fallback(ctx):
    a = (ctx.m('width head arial') or {}).get('width') or 520
    b = (ctx.m('width head inter tight') or {}).get('width') or 480
    return int(-(-max(a, b) // 8) * 8 + 8)


def s_06_10(ctx):
    sec = ctx.v('oa.color.text.secondary.onNewsprint')
    for sid, good in (('s-06-10-correct', True), ('s-06-10-failure', False)):
        fam = '' if good else 'font-family:Arial,sans-serif;'
        css = (f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}.h{{margin:0;{ctx.ty("h3")};{fam}text-wrap:balance}}'
               f'.s{{margin:12px 0 0;{ctx.ty("caption")};color:{sec}}}')
        lab = 'Inter Tight 800' if good else 'Arial, the fallback'
        html = (f'<style>{css}</style><p class="k">{lab}</p><p class="h">{HEAD}</p>'
                f'<p class="s">{"Loaded from the published Inter Tight files" if good else "Shown when Inter Tight fails to load"}</p>')
        ctx.spec(sid, html, '06', '06.10',
                 f'The heading {HEAD} set in ' + ('Inter Tight 800.' if good else 'Arial bold, about the same width, with plainer letters than Inter Tight.'),
                 notes='Widths measured at 32 px, the H3 size at 1440 px, on one line.')


# ------------------------------------------------------------------------------------------------ chapter
def build(ctx):
    probes(ctx)
    T = ctx.T
    s_06_1(ctx)
    s_06_2(ctx)
    s_06_3(ctx)
    s_06_4(ctx)
    src = s_06_5(ctx)
    s_06_6(ctx)
    hang_em = s_06_7(ctx)
    s_06_8(ctx)
    s_06_9(ctx)
    s_06_10(ctx)

    def cpl(key):
        r = ms(ctx, key)
        return r.get('mean', 0), r.get('min', 0), r.get('max', 0), r.get('chars', 0), r.get('lines', 0)

    bi = cpl('cpl body ideal')
    bm = cpl('cpl body max')
    li = cpl('cpl long sample ideal')
    lm = cpl('cpl long sample max')
    v5 = cpl('cpl v5 intro 65ch')
    im = cpl('cpl intro max')
    sp = {k: (ms(ctx, f'space {k}').get('width') or 0) for k in ('h4 0', 'h4 -2', 'h4 -4.5')}
    wi = ms(ctx, 'width head inter tight').get('width') or 1
    wa = ms(ctx, 'width head arial').get('width') or 1
    wider = (wa / wi - 1) * 100
    cut = (1 - sp['h4 -4.5'] / sp['h4 0']) * 100 if sp['h4 0'] else 0
    for k, val in (('space h4 0', sp['h4 0']), ('space h4 -2', sp['h4 -2']), ('space h4 -4.5', sp['h4 -4.5'])):
        ctx.fig(k + ' px', f'{val:.2f}', 'width("a b") minus width("ab") in Inter Tight 800 at 24 px, Chromium')
    ctx.fig('Arial over Inter Tight width, percent', f'{wider:.1f}', 'rendered width of the heading at 32 px')
    ctx.fig('word space cut at -4.5 percent, percent', f'{cut:.0f}', 'from the two space widths')
    phone = ctx.R.get('cpl span phone 4') or {}
    phone_s = ctx.R.get('cpl span phoneSmall 4') or {}
    ph_lo = round(min(phone_s.get('mean', 0), phone.get('mean', 0)))
    ph_hi = round(max(phone_s.get('mean', 0), phone.get('mean', 0)))
    sec = 'oa.color.text.secondary.onNewsprint'
    ch_n = ctx.ratio('oa.color.text.primary.onNewsprint', 'oa.color.surface.newsprint')
    lab_r = ctx.ratio(sec, 'oa.color.surface.newsprint')
    fonts = ctx.R.get('font check', {})
    ch = {
        'number': '06', 'anchor': 'type', 'title': 'Type', 'part': 'Foundations',
        'instruction': 'Set every word at a readable size with the three faces and the type scale.',
        'intro': [
            'Three typefaces carry every word we publish: Inter Tight for headlines and big figures, Inter for reading and '
            'the interface, and Lora Italic for the words we quote. Each has a single job, so a reader can tell a headline '
            'from a quotation before reading either.',
            'We set sizes in rem, a unit tied to the reader’s own text setting, which is 16 px unless they change it. A '
            'reader who enlarges text gets larger type everywhere, and no text on screen sets below 13 px.'],
        'rules': [
            {
                'id': '06.1', 'title': 'Each typeface keeps its one job.',
                'rule': ['Inter Tight 800 sets titles, headings and big figures. Inter sets body text, the interface, labels, '
                         'captions, tables and chart text, at 400, 600 and 700. Lora Italic sets only quoted words, such as a '
                         'pull quote or a quote card, at 400, or at 500 on a quote card.'],
                'tokens': ['oa.font.family.display', 'oa.font.family.reading', 'oa.font.family.quote',
                           'oa.font.weight.extrabold', 'oa.font.weight.regular', 'oa.font.weight.semibold',
                           'oa.font.weight.bold', 'oa.font.weight.medium'],
                'why': {'text': ['One face for each job lets a reader tell a headline from a quotation at a glance. The '
                                 'wordmark is drawn from Inter Tight 800, so our headings share its voice, and the page still '
                                 'reads as ours with the logo covered. Charts follow the same split: Inter Tight for titles, '
                                 'Inter for labels and numbers, and Lora Italic only for quoted words.'],
                        'basis': 'Design judgment; Master Brief section 3; decision DR-47'},
                'correct': {'specimen': 's-06-1-correct',
                            'caption': 'The three faces at true size, each in its job: a heading in Inter Tight 800, a '
                                       'sentence, a button and a label in Inter, and our editorial commitment quoted in Lora '
                                       'Italic.'},
                'failure': {'specimen': 's-06-1-failure',
                            'caption': '<strong>Fails the faces’ jobs.</strong> Set in Lora Italic, the heading reads as a '
                                       'quotation, and the reader looks for the person who said it.'},
                'specs': [
                    {'label': 'Display', 'value': 'Inter Tight 800; fallback Arial, sans-serif', 'token': 'oa.font.family.display'},
                    {'label': 'Reading and interface', 'value': 'Inter 400, 600 and 700; fallback Arial, sans-serif', 'token': 'oa.font.family.reading'},
                    {'label': 'Quotation', 'value': 'Lora Italic 400, and 500 on quote cards; fallback Georgia, serif', 'token': 'oa.font.family.quote'},
                    {'label': 'Source', 'value': 'Google Fonts, SIL Open Font License', 'token': None},
                ],
                'related': ['03', '14', '22'],
                'builders': ['Load all three with one link: <code>https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700'
                             '&amp;family=Inter+Tight:wght@800&amp;family=Lora:ital,wght@1,400;1,500&amp;display=swap</code>. '
                             'Then set faces only through <code>--oa-font-family-display</code>, '
                             '<code>--oa-font-family-reading</code> and <code>--oa-font-family-quote</code>.'],
            },
            {
                'id': '06.2', 'title': 'Every size comes from the type scale.',
                'rule': ['Set text in the fourteen styles of the scale, with no sizes between them. Display styles grow with '
                         'the window from 390 to 1440 px wide, reading styles hold one size, and every size is in rem so it '
                         'follows the reader’s text setting.'],
                'tokens': [f'oa.type.{k}' for k, _, _ in STYLES],
                'why': {'text': ['WCAG 2.2 success criterion 1.4.4 Resize Text asks that text grow to 200 percent with '
                                 'nothing lost. A size in rem grows when a reader raises the browser’s text size, and a size '
                                 'fixed in px stays where it is. Our fifth edition set every size in px, and when we doubled its '
                                 'root text size in a test, none of its 2,383 text elements grew.'],
                        'basis': 'WCAG 2.2 SC 1.4.4'},
                'correct': {'specimen': 's-06-2-correct',
                            'caption': 'The fourteen styles, each drawn live at true size for this window. Display sizes move '
                                       'between their floor at 390 px and their ceiling at 1440 px, so the samples match the '
                                       'screen you are reading on.'},
                'failure': {'specimen': 's-06-2-failure',
                            'caption': '<strong>Fails 1.4.4.</strong> Two columns as a reader sees them with text set to 200 '
                                       'percent. The column set in rem has grown to 34 px; the column set in px is still 17 px.'},
                'specs': [
                    {'label': 'Text size base', 'value': '16 px, the browser default; every size is a multiple in rem', 'token': None},
                    {'label': 'Fluid range', 'value': 'Display sizes grow from 390 px to 1440 px wide', 'token': 'oa.type.title'},
                    {'label': 'Body', 'value': 'Inter 400, 17 px (1.0625 rem), line height 1.6', 'token': 'oa.type.body'},
                    {'label': 'Intro', 'value': 'Inter 400, 19 to 22 px, line height 1.5', 'token': 'oa.type.intro'},
                    {'label': 'H3', 'value': 'Inter Tight 800, 26 to 32 px, line height 1.08', 'token': 'oa.type.h3'},
                    {'label': 'Print', 'value': 'A point scale follows in chapter 25, Phase 4', 'token': None},
                ],
                'related': ['07', '19', '25'],
                'builders': ['Set a style with its shorthand and its parts: <code>font: var(--oa-type-body)</code> carries '
                             'face, weight, size and line height, and <code>letter-spacing</code>, '
                             '<code>text-transform</code> and <code>font-variant-numeric</code> each have their own property, '
                             'such as <code>--oa-type-label-letter-spacing</code>. Never write a font size in px.'],
            },
            {
                'id': '06.3', 'title': 'No text on screen sets below 13 px.',
                'rule': ['The smallest text on screen is 13 px, or 0.8125 rem: labels, tags and data labels. A label in '
                         'capitals at 13 px takes Inter 700 with 6 percent tracking. A specimen that shows a mark or a minimum '
                         'size at true size is a graphic, and its caption says so.'],
                'tokens': ['oa.type.label', 'oa.type.dataLabel', 'oa.type.caption'],
                'why': {'text': ['Our fifth edition set its labels at 10 to 12 px, and its text census counted 833 of 2,346 '
                                 'rendered text elements under 13 px. A floor with no screen exceptions keeps eyebrows, tags '
                                 'and navigation readable without zoom. At 13 px, capitals need less tracking than they did at '
                                 '10 px, so 6 percent keeps them open without pulling a word apart.'],
                        'basis': 'Design judgment; Master Brief section 8, tension 1; decision T-9'},
                'correct': {'specimen': 's-06-3-correct',
                            'caption': f'Four labels at true size, all at 13 px. The location line is secondary text at '
                                       f'{lab_r} to 1; the column head, tag and data label are primary text at {ch_n} to 1.'},
                'failure': {'specimen': 's-06-3-failure',
                            'caption': '<strong>Fails the 13 px floor.</strong> A graphic at true size of two labels from our '
                                       'fifth edition: the chapter eyebrow at 11 px with 13 percent tracking, and the footer '
                                       'line at 10 px.'},
                'specs': [
                    {'label': 'Floor', 'value': '13 px (0.8125 rem), no screen exceptions', 'token': 'oa.type.label'},
                    {'label': 'Label', 'value': 'Inter 700, capitals, 13 px, line height 1.4, +6% tracking', 'token': 'oa.type.label'},
                    {'label': 'Data label', 'value': 'Inter 600, 13 px, line height 1.3, tabular figures', 'token': 'oa.type.dataLabel'},
                    {'label': 'Caption', 'value': 'Inter 400, 14 px, line height 1.5', 'token': 'oa.type.caption'},
                    {'label': 'Print floor', 'value': 'Taglines 7 pt, capitals 3 mm in identity marks', 'token': None},
                ],
                'related': ['03', '19', '28'],
                'builders': ['The shared check fails any text under 12.95 px, with SVG text measured at its rendered scale. '
                             'A chart drawn in SVG has to keep its labels at 13 px on a phone, so draw a phone version rather '
                             'than shrinking the desktop one.'],
            },
            {
                'id': '06.4', 'title': 'Tracking tightens only as headings grow.',
                'rule': ['Tracking is the space added to or taken from every pair of letters. Display styles take negative '
                         f'tracking that eases as the size drops: {C.MINUS}4.5 percent for titles, {C.MINUS}4 percent for '
                         f'sections, {C.MINUS}3 percent for H3 and {C.MINUS}2 percent for H4. Reading styles keep the '
                         f'font’s own spacing, and labels in capitals open to +6 percent.'],
                'tokens': ['oa.type.title', 'oa.type.section', 'oa.type.h3', 'oa.type.h4', 'oa.type.label'],
                'why': {'text': [f'Large type looks loose at the font’s own spacing, and small type looks cramped when it is '
                                 f'pulled tight. Our fifth edition used {C.MINUS}4.5 percent at every heading size from 24 to '
                                 f'110 px. Measured at 24 px in Inter Tight 800, that shrinks a word space from '
                                 f'{sp["h4 0"]:.1f} px to {sp["h4 -4.5"]:.1f} px, a cut of {cut:.0f} percent, while the '
                                 f'letters close up too.'],
                        'basis': 'Design judgment; our audit of the fifth edition, October 2026'},
                'correct': {'specimen': 's-06-4-correct',
                            'caption': f'An H4 at true size, 24 px with {C.MINUS}2 percent tracking. Its word spaces measure '
                                       f'{sp["h4 -2"]:.1f} px, and each word stands on its own.'},
                'failure': {'specimen': 's-06-4-failure',
                            'caption': f'<strong>Fails the tracking scale.</strong> The same H4 at {C.MINUS}4.5 percent. Its '
                                       f'word spaces shrink to {sp["h4 -4.5"]:.1f} px and the words begin to run together.'},
                'specs': [
                    {'label': 'Title', 'value': f'{C.MINUS}4.5% (−0.045 em)', 'token': 'oa.type.title'},
                    {'label': 'Section', 'value': f'{C.MINUS}4%', 'token': 'oa.type.section'},
                    {'label': 'H3', 'value': f'{C.MINUS}3%', 'token': 'oa.type.h3'},
                    {'label': 'H4', 'value': f'{C.MINUS}2%', 'token': 'oa.type.h4'},
                    {'label': 'Reading styles', 'value': '0, the font’s own spacing', 'token': 'oa.type.body'},
                    {'label': 'Label', 'value': '+6%', 'token': 'oa.type.label'},
                ],
                'related': ['03', '04'],
                'builders': ['Tracking lives in each style’s <code>letter-spacing</code> property, in em, so it scales with '
                             'the size: <code>letter-spacing: var(--oa-type-h3-letter-spacing)</code>. Never track body text.'],
            },
            {
                'id': '06.5', 'title': 'Figures line up in tables, and negatives take the true minus sign.',
                'rule': ['Tables, trackers, scorecards and chart labels set tabular figures, which give every digit the same '
                         'width so a column lines up. A negative number takes the minus sign (−, U+2212), never a hyphen, '
                         'and the numbers in one column carry the same number of decimals.'],
                'tokens': ['oa.type.dataLabel', 'oa.type.figure', 'oa.type.bodySmall'],
                'why': {'text': ['A reader compares a column by its right edge, and proportional figures move that edge digit '
                                 'by digit. The hyphen is shorter than the minus and sits lower, so a hyphen before 245 can '
                                 'read as a dash. Chapter 02’s house rule H07 asks for the true minus in prose as well.'],
                        'basis': 'Design judgment; chapter 02, house rule H07'},
                'correct': {'specimen': 's-06-5-correct',
                            'caption': 'A finding at true size, set in Inter with tabular figures. The figures align on the '
                                       'right, and the one fall, in information jobs, takes the true minus.'},
                'failure': {'specimen': 's-06-5-failure',
                            'caption': '<strong>Fails the figure rule.</strong> The same table with proportional figures, '
                                       'columns aligned left and a hyphen for each minus. The digits no longer stack, and the '
                                       'two minus signs read like dashes.'},
                'specs': [
                    {'label': 'Figures in tables and charts', 'value': 'Tabular, font-variant-numeric: tabular-nums', 'token': 'oa.type.dataLabel'},
                    {'label': 'Big figures', 'value': 'Inter Tight 800, tabular', 'token': 'oa.type.figure'},
                    {'label': 'Minus sign', 'value': '− (U+2212); plus sign + (U+002B) where a sign is printed', 'token': None},
                    {'label': 'Ligatures', 'value': 'Common on, discretionary off', 'token': None},
                ],
                'related': ['02', '14'],
                'builders': ['In a template, write the minus as <code>&amp;minus;</code> or <code>\\2212</code>. A chart script '
                             'should format negatives itself, since a number converted to text takes a hyphen.'],
            },
            {
                'id': '06.6', 'title': 'Headings balance their lines and never end on one word.',
                'rule': ['A heading that runs to two or more lines splits into lines of near equal length, and its last line '
                         'holds at least two words. Body text wraps so its last line never holds one short word.'],
                'tokens': ['oa.type.h3', 'oa.type.section'],
                'why': {'text': ['A lone word on a heading’s last line, called a widow, reads as an afterthought and pulls the '
                                 'eye down a line for one word. Balanced lines let a reader take in a heading at a glance.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-06-6-correct',
                            'caption': 'A heading from our fifth edition’s type chapter at true size, its two lines balanced.'},
                'failure': {'specimen': 's-06-6-failure',
                            'caption': '<strong>Fails the widow rule.</strong> The same heading wrapped by width alone, which '
                                       'leaves one word on its last line.'},
                'specs': [
                    {'label': 'Headings', 'value': 'text-wrap: balance', 'token': 'oa.type.h3'},
                    {'label': 'Body text', 'value': 'text-wrap: pretty', 'token': 'oa.type.body'},
                ],
                'related': ['02', '07'],
                'builders': ['Older browsers ignore <code>text-wrap</code> and wrap as usual, so check the longest real '
                             'heading at 360 px and, where a widow appears, join its last two words with a no-break space.'],
            },
            {
                'id': '06.7', 'title': 'Opening quotation marks hang outside the text edge.',
                'rule': ['In a pull quote or a quote card, the opening mark sits in the margin, so the first letter of every '
                         'line starts on the same edge. Use curly quotation marks and apostrophes, never straight ones, and '
                         'keep common ligatures on and discretionary ligatures off.'],
                'tokens': ['oa.type.quote'],
                'why': {'text': ['When the mark sits inside the edge, the first line starts a mark’s width to the right of the '
                                 'rest, and the block looks indented by accident. Straight marks come from the typewriter; '
                                 'curly marks are the ones readers know from print.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-06-7-correct',
                            'caption': f'Our editorial commitment as a pull quote at true size. The opening mark hangs '
                                       f'{hang_em:.2f} em into the margin, its measured width, and every line starts on the '
                                       f'hairline.'},
                'failure': {'specimen': 's-06-7-failure',
                            'caption': '<strong>Fails the hanging rule.</strong> With the mark inside the edge, the first line '
                                       'starts a mark’s width to the right of the second.'},
                'specs': [
                    {'label': 'Hang', 'value': f'{hang_em:.2f} em in Lora Italic 400, measured', 'token': 'oa.type.quote'},
                    {'label': 'Marks', 'value': '“ ” ‘ ’ (U+201C, U+201D, U+2018, U+2019)', 'token': None},
                ],
                'related': ['02', '23'],
                'builders': ['Set <code>hanging-punctuation: first</code> where the browser supports it, and a negative '
                             f'<code>text-indent</code> of {hang_em:.2f} em on the quote where it does not.'],
            },
            {
                'id': '06.8', 'title': 'Body text runs 60 to 75 characters a line.',
                'rule': [f'Set body text to a measure of 60 to 75 characters a line on wider screens, and intro '
                         f'text to 65 at most. A phone gives about {ph_lo} to {ph_hi} characters, which suits a small screen. '
                         f'Chapter 07 gives the column spans that deliver these measures at each width.'],
                'tokens': ['oa.layout.measure.bodyIdeal', 'oa.layout.measure.bodyMax', 'oa.layout.measure.introMax',
                           'oa.type.body', 'oa.type.intro'],
                'why': {'text': [f'Lines far past 75 characters make the eye lose its place on the way back to the next one. '
                                 f'The ch unit, the width of a zero, runs wider than Inter’s average letter, so an intro set '
                                 f'to 65ch, as in our fifth edition, measured {v5[1]} to {v5[2]} characters a line when we '
                                 f'set it at 22 px.'],
                        'basis': 'Design judgment, with WCAG 2.2 SC 1.4.8 (AAA, advisory)'},
                'correct': {'specimen': 's-06-8-correct',
                            'caption': f'A paragraph at true size and the body measure, 33.88 rem. Its full lines measure '
                                       f'{bi[1]} to {bi[2]} characters. Over {li[3]:,} characters of chapter 02’s prose at the '
                                       f'same width, lines average {li[0]:.0f}, and at the widest body measure, '
                                       f'{lm[0]:.0f}.'},
                'failure': {'specimen': 's-06-8-failure',
                            'caption': f'<strong>Fails the measure.</strong> The same paragraph as our fifth edition set its '
                                       f'intros, at 22 px and 65ch. Its full lines run {v5[1]} to {v5[2]} characters, and the '
                                       f'eye has far to travel back to the start of each.'},
                'specs': [
                    {'label': 'Body measure', 'value': f'33.88 rem, 542 px at 16 px text; lines average {li[0]:.0f} characters', 'token': 'oa.layout.measure.bodyIdeal'},
                    {'label': 'Widest body measure', 'value': f'37.37 rem; lines average {lm[0]:.0f} characters', 'token': 'oa.layout.measure.bodyMax'},
                    {'label': 'Widest intro measure', 'value': f'41.91 rem; at 22 px, lines of {im[1]} to {im[2]} characters', 'token': 'oa.layout.measure.introMax'},
                    {'label': 'Phones', 'value': f'About {ph_lo} to {ph_hi} characters at 360 and 390 px', 'token': 'oa.layout.grid.phone.margin'},
                ],
                'related': ['07', '19'],
                'builders': ['Cap a text block with <code>max-width: var(--oa-layout-measure-body-ideal)</code>. The measure '
                             'is in rem, so a reader who enlarges text keeps the same characters a line.'],
            },
            {
                'id': '06.9', 'title': 'Email sets its type in the system stack.',
                'rule': ['Many mail apps ignore web fonts, so email sets headlines and body text in Helvetica, Arial, '
                         'sans-serif, and quotations in Georgia Italic. The scale’s sizes and weights still apply, and '
                         'chapter 22 shows the full template.'],
                'tokens': ['oa.font.family.emailSans', 'oa.font.family.emailQuote'],
                'why': {'text': ['A mail app that cannot load a web font falls back to a face of its own choosing, often a '
                                 'serif. The system stack names the fallback in advance, so every reader sees a face we chose. '
                                 'Our fifth edition kept this rule and then set its own email headline in Inter Tight.'],
                        'basis': 'Design judgment; Master Brief section 10'},
                'correct': {'specimen': 's-06-9-correct',
                            'caption': 'An email header at its true width of 600 px on White, set in the system stack: the '
                                       'headline and body in Helvetica or Arial, the quote in Georgia Italic.'},
                'failure': {'specimen': 's-06-9-failure',
                            'caption': '<strong>Fails the email rule.</strong> The headline set in Inter Tight, as a mail app '
                                       'shows it when the web font does not load: in the app’s default serif.'},
                'specs': [
                    {'label': 'Headlines and body', 'value': 'Helvetica, Arial, sans-serif', 'token': 'oa.font.family.emailSans'},
                    {'label': 'Quotation', 'value': 'Georgia, serif, italic', 'token': 'oa.font.family.emailQuote'},
                    {'label': 'Width', 'value': '600 px', 'token': None},
                ],
                'related': ['02', '22'],
                'builders': ['Write the stack on every text element of an email, inline, since many mail apps strip a '
                             'style block. The wordmark goes in as an image with its name as alt text.'],
            },
            {
                'id': '06.10', 'title': 'Pages load the three faces and never substitute another.',
                'rule': ['Pages load Inter Tight, Inter and Lora from their published files, in the weights the scale uses. '
                         'Arial and Georgia appear only as fallbacks inside the font stacks. No other face stands in for '
                         'ours, including Spectral, Source Sans, Public Sans, IBM Plex, Libre Baskerville, Playfair Display, '
                         'Cormorant, Helvetica Neue for display, Times New Roman, Calibri, Roboto, Open Sans and Montserrat.'],
                'tokens': ['oa.font.family.display', 'oa.font.family.reading', 'oa.font.family.quote'],
                'why': {'text': [f'Master Brief section 3 says a font substitution is never a finished identity decision. A '
                                 f'fallback keeps a page readable when a font fails to load, and that is its only job. '
                                 f'Measured at 32 px, the heading here sets {wi:.0f} px wide in Inter Tight and {wa:.0f} px in '
                                 f'Arial, {wider:.1f} percent wider, which is why a page that failed to '
                                 f'load Inter Tight can look finished: only the letters show it. The list carries our fifth '
                                 f'edition’s never-substitute list forward.'],
                        'basis': 'Master Brief section 3; design judgment'},
                'correct': {'specimen': 's-06-10-correct',
                            'caption': f'A heading at true size in Inter Tight 800, {wi:.0f} px wide at 32 px.'},
                'failure': {'specimen': 's-06-10-failure',
                            'caption': f'<strong>Fails the face rule.</strong> The same heading in Arial, the fallback that '
                                       f'shows when Inter Tight fails to load. It sets {wa:.0f} px wide, close to the '
                                       f'original, and its letters lose the cut of the wordmark’s face.'},
                'specs': [
                    {'label': 'Display stack', 'value': '<code>"Inter Tight", Arial, sans-serif</code>', 'token': 'oa.font.family.display'},
                    {'label': 'Reading stack', 'value': 'Inter, Arial, sans-serif', 'token': 'oa.font.family.reading'},
                    {'label': 'Quotation stack', 'value': 'Lora, Georgia, serif', 'token': 'oa.font.family.quote'},
                ],
                'related': ['03', '27'],
                'builders': ['Use <code>font-display: swap</code>, as the Google Fonts link sets it, so text shows at once in '
                             'the fallback and changes face when the file arrives. Ship the font license with any package that '
                             'carries the files.'],
            },
        ],
        'extras': [],
        'sources': [src,
                    'W3C, Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, success criteria 1.4.4 and '
                    '1.4.8, https://www.w3.org/TR/WCAG22/.'],
    }
    for r in ch['rules']:
        r['specs'] = [{k: x for k, x in s.items() if x is not None} for s in r['specs']]
    ctx.fig('fonts loaded in the render', json.dumps(fonts), 'document.fonts.check in Chromium')
    return ch
